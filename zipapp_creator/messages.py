class _Messages(object):
    def __init__(self):
        from .common import trfunc

        tr = trfunc()

        self.MSG_SAVE_PARAMS_TITLE = tr("Save Parameters")
        self.MSG_LOAD_PARAMS_TITLE = tr("Load Parameters")
        self.MSG_JSON_FILE_FILTER = tr("JSON Files")
        self.MSG_ALL_FILES_FILTER = tr("All Files")
        self.MSG_SAVE_PARAMS_SUCCESS = tr("Parameters saved to file: {}")
        self.MSG_LOAD_PARAMS_SUCCESS = tr("Parameters loaded from file: {}")
        self.MSG_SAVE_PARAMS_ERROR = tr("Failed to save parameters to file: {}")
        self.MSG_LOAD_PARAMS_ERROR = tr("Failed to load parameters from file: {}")
        self.MSG_INVALID_PARAMS_IN_FILE = tr("Invalid parameters in file: {}")
        self.MSG_ABOUT_TITLE = tr("About")
        self.MSG_LICENSE_TITLE = tr("License")
        self.MSG_LICENSE_HINT = tr("This project is under the MIT license.")
        self.MSG_EDIT_APP_CONFIG_HINT = tr(
            "Changes to the configuration file will be take effect after restarting the program!"
        )
        self.MSG_ACTION_SAVE_PARAMS = tr("Save Parameters")
        self.MSG_ACTION_LOAD_PARAMS = tr("Load Parameters")
        self.MSG_ACTION_EXIT = tr("Exit")
        self.MSG_ACTION_ALWAYS_ON_TOP = tr("Always on Top")
        self.MSG_ACTION_ABOUT = tr("About")
        self.MSG_ACTION_LICENSE = tr("License")
        self.MSG_ACTION_EDIT_CONFIG = tr("Edit Config")
        self.MSG_MENU_FILE = tr("File")
        self.MSG_MENU_VIEW = tr("View")
        self.MSG_MENU_HELP = tr("Help")


_messages = None


def messages() -> _Messages:
    global _messages
    if _messages is None:
        _messages = _Messages()
    return _messages
