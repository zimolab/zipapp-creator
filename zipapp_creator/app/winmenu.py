import json
import sys
from pathlib import Path

from pyguiadapterlite import Menu, Action, FnExecuteWindow, Separator
from pyguiadapterlite.components.textview import SimpleTextViewer

from .aboutdlg import AboutDialog
from .. import assets
from ..common import get_appconfig
from ..messages import messages
from ..utils import move_to_center_of

LICENSE_FILE = "LICENSE"


_menus = None


# noinspection PyUnusedLocal
def _on_action_save_params(window: FnExecuteWindow, action: Action):
    msgs = messages()
    save_filepath = window.select_save_file(
        title=msgs.MSG_SAVE_PARAMS_TITLE,
        filetypes=[
            (msgs.MSG_JSON_FILE_FILTER, "*.json"),
            (msgs.MSG_ALL_FILES_FILTER, "*"),
        ],
    )
    if not save_filepath:
        return
    save_filepath = Path(save_filepath)
    param_values = window.get_parameter_values()
    ret = window.check_invalid_parameters(param_values)
    if not ret:
        return
    try:
        with open(save_filepath, "w", encoding="utf-8") as f:
            json.dump(param_values, f, indent=2, ensure_ascii=False)
    except BaseException as e:
        window.show_error(
            msgs.MSG_SAVE_PARAMS_ERROR.format(save_filepath), detail=str(e)
        )
    else:
        window.show_information(msgs.MSG_SAVE_PARAMS_SUCCESS.format(save_filepath))


# noinspection PyUnusedLocal
def _on_action_load_params(window: FnExecuteWindow, action: Action):
    msgs = messages()
    load_filepath = window.select_open_file(
        title=msgs.MSG_LOAD_PARAMS_TITLE,
        filetypes=[
            (msgs.MSG_JSON_FILE_FILTER, "*.json"),
            (msgs.MSG_ALL_FILES_FILTER, "*"),
        ],
    )
    if not load_filepath:
        return
    load_filepath = Path(load_filepath)
    try:
        with open(load_filepath, "r", encoding="utf-8") as f:
            param_values = json.load(f)
    except BaseException as e:
        window.show_error(
            msgs.MSG_LOAD_PARAMS_ERROR.format(load_filepath),
            detail=str(e),
        )
    else:
        ret = window.set_parameter_values(param_values)
        if not ret:
            window.show_error(msgs.MSG_INVALID_PARAMS_IN_FILE.format(load_filepath))
        else:
            window.show_information(msgs.MSG_LOAD_PARAMS_SUCCESS.format(load_filepath))


# noinspection PyUnusedLocal
def _on_action_exit(window: FnExecuteWindow, action: Action):
    window.close()


def _on_action_always_on_top(window: FnExecuteWindow, action: Action):
    app_config = get_appconfig()
    app_config.always_on_top = action.is_checked()
    window.set_always_on_top(app_config.always_on_top)
    app_config.save(indent=2, encoding="utf-8", ensure_ascii=False)


# noinspection PyUnusedLocal
def _on_action_about(window: FnExecuteWindow, action: Action):
    msgs = messages()
    window.show_custom_dialog(AboutDialog, title=msgs.MSG_ABOUT_TITLE)


# noinspection PyUnusedLocal
def _on_action_license(window: FnExecuteWindow, action: Action):
    msgs = messages()
    try:
        text = assets.read_asset_text(LICENSE_FILE)
    except Exception as e:
        print(e, file=sys.stderr)
        window.show_error(message=msgs.MSG_LICENSE_HINT)
        return

    viewer = SimpleTextViewer(
        title=msgs.MSG_LICENSE_TITLE,
        width=800,
        height=600,
    )
    move_to_center_of(viewer, window.parent)
    viewer.set_text(text)
    viewer.show_modal()


# noinspection PyUnusedLocal
def _on_action_edit_config(window: FnExecuteWindow, action: Action):
    app_config = get_appconfig()
    window.show_information(message=messages().MSG_EDIT_APP_CONFIG_HINT)
    try:
        app_config.open_in_editor()
    except Exception as e:
        window.show_error(str(e))


def _create_file_actions() -> list[Action]:
    msgs = messages()

    return [
        Action(msgs.MSG_ACTION_SAVE_PARAMS, _on_action_save_params),
        Action(msgs.MSG_ACTION_LOAD_PARAMS, _on_action_load_params),
        Separator(),
        Action(msgs.MSG_ACTION_EXIT, _on_action_exit),
    ]


def _create_view_actions() -> list[Action]:
    msgs = messages()

    app_config = get_appconfig()
    return [
        Action(
            msgs.MSG_ACTION_ALWAYS_ON_TOP,
            on_triggered=_on_action_always_on_top,
            checkable=True,
            initial_checked=app_config.always_on_top,
        ),
        Separator(),
        Action(msgs.MSG_ACTION_EDIT_CONFIG, on_triggered=_on_action_edit_config),
    ]


def _create_help_actions() -> list[Action]:
    msgs = messages()
    return [
        Action(msgs.MSG_ACTION_ABOUT, on_triggered=_on_action_about),
        Action(msgs.MSG_ACTION_LICENSE, on_triggered=_on_action_license),
    ]


def create_menus() -> list[Menu]:
    global _menus
    if not _menus:
        msgs = messages()
        _menus = [
            Menu(msgs.MSG_MENU_FILE, actions=_create_file_actions()),
            Menu(msgs.MSG_MENU_VIEW, actions=_create_view_actions()),
            Menu(msgs.MSG_MENU_HELP, actions=_create_help_actions()),
        ]
    return _menus
