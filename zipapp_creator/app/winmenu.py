import sys

from pyguiadapterlite import Menu, Action, FnExecuteWindow, Separator
from pyguiadapterlite.components.textview import SimpleTextViewer

from .aboutdlg import AboutDialog
from .. import assets
from ..common import trfunc, get_appconfig
from ..utils import move_to_center_of

LICENSE_FILE = "LICENSE"


_menus = None


def _on_action_save_params(window: FnExecuteWindow, action: Action):
    pass


def _on_action_load_params(window: FnExecuteWindow, action: Action):
    pass


def _on_action_exit(window: FnExecuteWindow, action: Action):
    window.close()


def _on_action_always_on_top(window: FnExecuteWindow, action: Action):
    app_config = get_appconfig()
    app_config.always_on_top = action.is_checked()
    window.set_always_on_top(app_config.always_on_top)
    app_config.save(indent=2, encoding="utf-8", ensure_ascii=False)


# noinspection PyUnusedLocal
def _on_action_about(window: FnExecuteWindow, action: Action):
    tr = trfunc()
    window.show_custom_dialog(AboutDialog, title=tr("About"))


def _on_action_license(window: FnExecuteWindow, action: Action):
    tr = trfunc()
    try:
        text = assets.read_asset_text(LICENSE_FILE)
    except Exception as e:
        print(e, file=sys.stderr)
        window.show_error(
            message="This project is under the MIT license.", title=tr("Error")
        )
        return

    viewer = SimpleTextViewer(
        title=tr("License"),
        width=800,
        height=600,
    )
    move_to_center_of(viewer, window.parent)
    viewer.set_text(text)
    viewer.show_modal()


def _on_action_edit_config(window: FnExecuteWindow, action: Action):
    app_config = get_appconfig()
    tr = trfunc()
    window.show_information(
        tr(
            "Changes to the configuration file will be take effect after restarting the program!"
        )
    )
    try:
        app_config.open_in_editor()
    except Exception as e:
        window.show_error(str(e))


def _create_file_actions() -> list[Action]:
    tr = trfunc()
    return [
        Action(tr("Save Parameters"), _on_action_save_params),
        Action(tr("Load Parameters"), _on_action_load_params),
        Separator(),
        Action(tr("Exit"), _on_action_exit),
    ]


def _create_view_actions() -> list[Action]:
    tr = trfunc()
    app_config = get_appconfig()
    return [
        Action(
            tr("Always on Top"),
            on_triggered=_on_action_always_on_top,
            checkable=True,
            initial_checked=app_config.always_on_top,
        ),
        Separator(),
        Action(tr("Edit Config"), on_triggered=_on_action_edit_config),
    ]


def _create_help_actions() -> list[Action]:
    tr = trfunc()
    return [
        Action(tr("About"), on_triggered=_on_action_about),
        Action(tr("License"), on_triggered=_on_action_license),
    ]


def create_menus() -> list[Menu]:
    global _menus
    if not _menus:
        tr = trfunc()
        _menus = [
            Menu(tr("File"), actions=_create_file_actions()),
            Menu(tr("View"), actions=_create_view_actions()),
            Menu(tr("Help"), actions=_create_help_actions()),
        ]
    return _menus
