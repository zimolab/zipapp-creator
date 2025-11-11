from pyguiadapterlite import FnExecuteWindow

from ..common import get_appconfig


def after_window_create(window: FnExecuteWindow):
    app_config = get_appconfig()
    window.set_always_on_top(app_config.always_on_top)


def before_window_close(window: FnExecuteWindow):
    print("Window closing")
    return True
