from pyguiadapterlite import FnExecuteWindowConfig

from ..common import trfunc
from ..consts import APP_NAME, APP_VERSION
from .winevents import after_window_create, before_window_close

_window_config: FnExecuteWindowConfig | None = None


def get_window_config() -> FnExecuteWindowConfig:
    global _window_config
    if _window_config is None:
        tr = trfunc()
        _window_config = FnExecuteWindowConfig(
            title=APP_NAME.replace("-", " ").title() + f" - V{APP_VERSION}",
            print_function_result=False,
            show_function_result=False,
            document_tab_title=tr("Description"),
            output_tab_title=tr("Output"),
            execute_button_text=tr("Start"),
            clear_button_text=tr("Clear Output"),
            clear_checkbox_text=tr("clear output before start"),
            cancel_button_text=tr("Cancel"),
            after_window_create_callback=after_window_create,
            before_window_close_callback=before_window_close,
        )

    return _window_config
