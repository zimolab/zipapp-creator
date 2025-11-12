from pyguiadapterlite import FnExecuteWindow

from ..common import get_appconfig


def after_window_create(window: FnExecuteWindow):
    app_config = get_appconfig()
    window.set_always_on_top(app_config.always_on_top)


# noinspection PyUnusedLocal
def before_window_close(window: FnExecuteWindow):
    app_config = get_appconfig()
    app_config.save(encoding="utf-8", ensure_ascii=False, indent=2)
    return True
