import json
import sys
from pathlib import Path
from typing import List, Union

from functools import partial
from pyguiadapterlite import Menu, Action, FnExecuteWindow, Separator
from pyguiadapterlite.components.textview import SimpleTextViewer
from pyguiadapterlite.windows.settingswindow import SettingsWindow

from .dialogs import AboutDialog
from .. import assets
from ..appsettings import AppSettings
from ..common import get_appsettings
from ..consts import APP_SETTINGS_FILE
from ..messages import messages
from ..utils import move_to_center_of

LICENSE_FILE = "LICENSE"


class WindowMenus(object):

    HIDDEN_APPSETTINGS_FIELDS = (AppSettings.always_on_top,)

    def __init__(self):
        self._appsettings = get_appsettings()
        self._visible_fields = {
            field_name: field_def
            for field_name, field_def in AppSettings.fields().items()
            if field_def not in self.__class__.HIDDEN_APPSETTINGS_FIELDS
        }

        self._menus = None
        self._msgs = messages()

    # noinspection PyUnusedLocal
    def show_about_dialog(self, window: FnExecuteWindow, action: Action):
        window.show_custom_dialog(AboutDialog, title=self._msgs.MSG_ABOUT_TITLE)

    # noinspection PyUnusedLocal
    def show_license_dialog(self, window: FnExecuteWindow, action: Action):
        try:
            text = assets.read_asset_text(LICENSE_FILE)
        except Exception as e:
            print(e, file=sys.stderr)
            window.show_error(message=self._msgs.MSG_LICENSE_HINT)
            return

        viewer = SimpleTextViewer(
            title=self._msgs.MSG_LICENSE_TITLE,
            width=800,
            height=600,
        )
        move_to_center_of(viewer, window.parent)
        viewer.set_text(text)
        viewer.show_modal()

    def _after_settings_window_confirmed(
        self, window: FnExecuteWindow, appsettings: AppSettings
    ):
        try:
            appsettings.save(APP_SETTINGS_FILE)
        except BaseException as e:
            window.show_error(self._msgs.MSG_SAVE_SETTINGS_ERROR, detail=str(e))
        else:
            window.show_information(self._msgs.MSG_SETTINGS_SAVED)

    # noinspection PyUnusedLocal
    def show_settings_window(self, window: FnExecuteWindow, action: Action):
        window.show_sub_window(
            SettingsWindow,
            config=None,
            modal=True,
            settings=self._appsettings,
            setting_fields=self._visible_fields,
            after_save_callback=partial(self._after_settings_window_confirmed, window),
        )

    def always_on_top_changed(self, window: FnExecuteWindow, action: Action):
        self._appsettings.always_on_top = action.is_checked()
        window.set_always_on_top(self._appsettings.always_on_top)

    # noinspection PyUnusedLocal
    def save_parameters(self, window: FnExecuteWindow, action: Action):
        save_filepath = window.select_save_file(
            title=self._msgs.MSG_SAVE_PARAMS_TITLE,
            filetypes=[
                (self._msgs.MSG_JSON_FILE_FILTER, "*.json"),
                (self._msgs.MSG_ALL_FILES_FILTER, "*"),
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
                self._msgs.MSG_SAVE_PARAMS_ERROR.format(save_filepath), detail=str(e)
            )
        else:
            window.show_information(
                self._msgs.MSG_SAVE_PARAMS_SUCCESS.format(save_filepath)
            )

    # noinspection PyUnusedLocal
    def load_parameters(self, window: FnExecuteWindow, action: Action):
        load_filepath = window.select_open_file(
            title=self._msgs.MSG_LOAD_PARAMS_TITLE,
            filetypes=[
                (self._msgs.MSG_JSON_FILE_FILTER, "*.json"),
                (self._msgs.MSG_ALL_FILES_FILTER, "*"),
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
                self._msgs.MSG_LOAD_PARAMS_ERROR.format(load_filepath),
                detail=str(e),
            )
        else:
            ret = window.set_parameter_values(param_values)
            if not ret:
                window.show_error(
                    self._msgs.MSG_INVALID_PARAMS_IN_FILE.format(load_filepath)
                )
            else:
                window.show_information(
                    self._msgs.MSG_LOAD_PARAMS_SUCCESS.format(load_filepath)
                )

    # noinspection PyUnusedLocal,PyMethodMayBeStatic
    def request_exit(self, window: FnExecuteWindow, action: Action):
        window.close()

    def _create_file_actions(self) -> List[Union[Action, Separator]]:
        return [
            Action(self._msgs.MSG_ACTION_SAVE_PARAMS, self.save_parameters),
            Action(self._msgs.MSG_ACTION_LOAD_PARAMS, self.load_parameters),
            Separator(),
            Action(self._msgs.MSG_ACTION_SETTINGS, self.show_settings_window),
            Separator(),
            Action(self._msgs.MSG_ACTION_EXIT, self.request_exit),
        ]

    def _create_view_actions(self) -> List[Union[Action, Separator]]:
        return [
            Action(
                self._msgs.MSG_ACTION_ALWAYS_ON_TOP,
                on_triggered=self.always_on_top_changed,
                checkable=True,
                initial_checked=self._appsettings.always_on_top,
            )
        ]

    def _create_help_actions(self) -> List[Union[Action, Separator]]:
        return [
            Action(
                self._msgs.MSG_ACTION_ABOUT,
                on_triggered=self.show_about_dialog,
            ),
            Action(
                self._msgs.MSG_ACTION_LICENSE,
                on_triggered=self.show_license_dialog,
            ),
        ]

    def create(self) -> List[Menu]:
        if self._menus:
            return self._menus
        self._menus = [
            Menu(title=self._msgs.MSG_MENU_FILE, actions=self._create_file_actions()),
            Menu(title=self._msgs.MSG_MENU_VIEW, actions=self._create_view_actions()),
            Menu(title=self._msgs.MSG_MENU_HELP, actions=self._create_help_actions()),
        ]
        return self._menus
