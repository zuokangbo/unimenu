import unreal
import json
import warnings
from pathlib import Path


# def setup(path: (str, Path)):
#     """setup menu"""
#     path = str(path)
#     if path.lower().endswith('.json'):
#         return setup_from_json(path)
#     elif path.lower().endswith('.yaml'):
#         return setup_from_yaml(path)
#
#
# def setup_from_json(config_path):
#     with open(config_path) as file:
#         data = json.load(file)
#     return setup_menu(data)
#
#
# def setup_from_yaml(config_path):
#     import yaml
#
#     with open(config_path) as file:
#         data = yaml.load(file, Loader=yaml.SafeLoader)
#     return setup_menu(data)


def setup_menu(data):
    parent_menu_name = data.get('parent', "LevelEditor.MainMenu")
    unreal_menus = unreal.ToolMenus.get()
    parent_menu = unreal_menus.find_menu(parent_menu_name)
    if not parent_menu:
        warnings.warn(f"Parent menu '{parent_menu_name}' not found, couldn't setup menu")

    _setup_menu_items(parent_menu, data.get('items'))
    unreal_menus.refresh_all_widgets()
    # TODO decide to return success/failure, or the menu object


def _setup_menu_items(parent_menu, items: list):
    # go over all items in the menu and add them to the menu
    # if there are subitems, call self on data recursively
    for item in items:
        name = item.get('name')
        command = item.get('command', None)
        if command:
            add_to_menu(parent_menu, name, command)
        else:  # submenu
            items = item.get('items', [])
            sub_menu = parent_menu.add_sub_menu(owner=parent_menu.menu_name,
                                                section_name="PythonTools",
                                                name=name,
                                                label=name,  # todo add label support
                                                )
            _setup_menu_items(sub_menu, items)


def add_to_menu(script_menu, label: str, command: str):
    """add a menu item to the script menu"""
    entry = unreal.ToolMenuEntry(
        # name="Python.MyCoolTool",  # this needs to be unique! if not set, it's autogenerated
        type=unreal.MultiBlockType.MENU_ENTRY,
        insert_position=unreal.ToolMenuInsert("", unreal.ToolMenuInsertType.FIRST),
    )
    entry.set_label(label)
    entry.set_string_command(
        type=unreal.ToolMenuStringCommandType.PYTHON,
        string=command,
        custom_type=unreal.Name("_placeholder_"),
    )  # hack: unsure what custom_type does, but it's needed
    script_menu.add_menu_entry("Scripts", entry)


def breakdown():
    """remove from menu"""
    raise NotImplementedError("not yet implemented")
