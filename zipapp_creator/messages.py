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
        self.MSG_START_PACKAGING = tr("Start packaging...")
        self.MSG_COPY_SOURCE_FILES = tr("Start copying source files to {}...")
        self.MSG_PIP_INSTALL_FAILURE = tr("Failed to install dependencies: {}")
        self.MSG_CREATING_ZIPAPP = tr("Start creating zipapp file {}...")
        self.MSG_ZIPAPP_CREATED = tr("Zipapp file created: {}")
        self.MSG_CREATING_STARTUP_SCRIPT = tr(
            "Creating startup script for Windows os..."
        )
        self.MSG_STARTUP_SCRIPT_CREATED = tr("Startup script created: {}")
        self.MSG_CREATE_ZIPAPP_FAILURE = tr("Failed to create zipapp file: {}")

        self.MSG_SOURCE_DIR_REQUIRED = tr("Please specify the source directory!")
        self.MSG_SOURCE_DIR_NOT_FOUND = tr("The source directory does not exist!")
        self.MSG_MAIN_FILE_NOT_ALLOWED = tr(
            "A __main__.py file is found in the source directory, "
            "which is not allowed when creating a self-extracting zipapp!"
        )
        self.MSG_VALID_ENTRY_FILE_REQUIRED = tr(
            "Please specify a valid entry file when creating a self-extracting zipapp!"
        )
        self.MSG_ENTRY_REQUIRED = tr(
            "The entry must be specified(in the form of 'pkg.module:fn' or 'module:fn') "
            "if there is no __main__.py file in the source directory!"
        )
        self.MSG_INVALID_ENTRY_FORMAT = tr(
            "The entry should be in the form of 'pkg.module:fn' or 'module:fn', not a file path!"
            "Or you can just leave it empty if there is a __main__.py file in the source directory!"
        )
        self.MSG_HOST_PYTHON_REQUIRED = tr(
            "Please specify the host python interpreter which will be used for pip-install!"
        )
        self.MSG_REQUIREMENTS_FILE_NOT_FOUND = tr(
            "The requirements file not found in the source directory!"
        )
        self.MSG_SCRIPT_PYTHON_REQUIRED = tr(
            "Please specify the python command which will be used in the startup script for starting the "
            "output zipapp."
        )
        self.MSG_CLEANUP_DEPENDENCIES = tr("Cleaning up dependencies...")
        self.MSG_REMOVING = tr("Removing: {}")
        self.MSG_CLEANUP_DEPENDENCIES_DONE = tr("Cleanup done!")

        self.MSG_START_PIP_INSTALL = tr("Installing dependencies with pip...")
        self.MSG_PIP_INSTALL_FAILURE = tr("Failed to install dependencies: {}")
        self.MSG_PIP_INSTALL_SUCCESS = tr("Dependencies installed successfully!")
        self.MSG_PIP_INSTALL_CANCELLED = tr("User cancelled the pip-install process!")

        self.MSG_PARAM_GROUP_MAIN = tr("Main")
        self.MSG_PARAM_GROUP_EXCLUDE = tr("Exclude")
        self.MSG_PARAM_GROUP_PACKAGING = tr("Packaging")

        self.MSG_PARAM_SRC_DIR = tr("Source")
        self.MSG_PARAM_TARGET = tr("Target")
        self.MSG_PARAM_ENTRY = tr("Entry")
        self.MSG_PARAM_SHEBANG = tr("Shebang")
        self.MSG_PARAM_REQUIREMENTS = tr("Requirements")
        self.MSG_PARAM_HOST_PYTHON = tr("Host Python")
        self.MSG_PARAM_DEFLATE_COMPRESSION = tr("Deflate Compression")
        self.MSG_PARAM_SELF_EXTRACTING = tr("Self-Extracting Mode")
        self.MSG_PARAM_START_SCRIPT = tr("Start Script for Windows")
        self.MSG_STRAT_SCRIPT_PYTHON = tr("Python for Start Script")
        self.MSG_PARMA_EXCLUDE_FROM_COPY = tr("Exclude from Copy")
        self.MSG_PARAM_EXCLUDE_FROM_PACKAGING = tr("Exclude from Packaging")
        self.MSG_PARAM_PIP_INDEX_URL = tr("PIP Index URL")
        self.MSG_PARMA_CLEANUP_DEPENDENCIES = tr(
            "Cleanup dependencies after pip install"
        )

        self.MSG_PARAM_DESC_SRC_DIR = tr(
            "The name of a directory, in which case a new application\n"
            "archive will be created from the content of that directory."
        )
        self.MSG_PARAM_DESC_TARGET = tr(
            "This argument determines where the resulting archive\n"
            "will be written.If this argument is omitted, the target \n"
            "will be a file with the same name as the source, with a .pyz\n"
            "extension added."
        )
        self.MSG_PARAM_DESC_SHEBANG = tr(
            "This argument specifies the name of python interpreter \n"
            "with which the archive will be executed. It is written as a \n"
            "“shebang” line at the start of the archive.On POSIX, this will \n"
            "be interpreted by the OS, and on Windows it will be handled\n"
            "by the Python launcher. Omitting this argument results in no \n"
            "shebang line being written. If an shebang is specified, \n"
            "and the target is a filename, the executable bit of the target \n"
            "file will be set."
        )
        self.MSG_PARAM_DESC_DEFLATE_COMPRESSION = tr(
            "This argument determines whether files are compressed. If selected, \n"
            "files in the archive are compressed with the deflate method; otherwise, \n"
            "files are stored uncompressed."
        )
        self.MSG_PARAM_DESC_SELF_EXTRACTING = tr(
            "This argument determines whether the resulting archive is a 'self-extracting'\n"
            "archive. A self-extracting archive contains a auto-generated python script as \n"
            "the actual entry point of the application. When executed, this script will be \n"
            "executed first. This script literally does two things: first of all it extracts \n"
            "the contents of the archive to a temporary directory, and then start the entry \n"
            "point file you specified. If this argument is selected, you must specify an \n"
            "entry point file and make sure that there is no __main__.py file in the source \n"
            "directory. If this argument is not selected, you need to provide an entry point \n"
            "in the form of 'pkg.module:fn' or 'module:fn', or just leave the entry point argument empty \n"
            "if there is a __main__.py file in the source directory. An self-extracting archive \n"
            "is very useful if you have c extensions in your dependencies."
        )
        self.MSG_PARAM_DESC_START_SCRIPT = tr(
            "This argument determines whether a startup script will be created for Windows operating \n"
            "system. The startup script will be a vbs file with the same name as the target archive, \n"
            "For example, if the target archive is 'app.pyz', the startup script will be 'app.vbs'. \n"
            "The startup script starts the output zipapp by using the python command you specified, and \n"
            "it hides the console window which makes your zipapp look more like a native application. \n"
            "If this argument is selected, you must specify the python command to start the output zipapp. "
        )
        self.MSG_PARAM_DESC_SCRIPT_PYTHON = tr(
            "This argument specifies the python command to start the output zipapp in the startup script. \n"
            "For example, if you want to use python 3 to start the output zipapp, you can specify 'python3'. \n"
            "It is not recommented to specify an absolute path to the python interpreter, it may not work \n"
            "in other machines. It is recommended to use 'python'/ 'python3'/ 'python.exe' and make sure the \n"
            "python interpreter is in the system PATH."
        )
        self.MSG_PARAM_DESC_EXCLUDE_FROM_COPY = tr(
            "Everytime you create a new application archive, the source directory is copied to the `zipapp_dist` \n"
            "directory to keep your source directory clean and uncompromised. This argument let you exclude the \n"
            "files and directories you don't want to be copied to the `zipapp_dist` directory. For example, you \n"
            "probably don't want the virtual environment directory(normally named venv or .venv) being copied to the."
            "zipapp_dist directory. "
        )
        self.MSG_PARAM_DESC_EXCLUDE_FROM_PACKAGING = tr(
            "Sometimes some files is required for packaging, but not necessary in the runtime. For example, a \n"
            "requirements.txt is needed for if you want to installing the dependencies during the packaging \n "
            "process, but it is not necessary in the runtime. This argument let you specify the patterns of files \n"
            "and directories will be excluded from the target zipapp archive."
        )
        self.MSG_PARAM_DESC_HOST_PYTHON = tr(
            "This argument specifies the Python interpreter to be used for pip-install during the packaging process."
        )
        self.MSG_PARAM_DESC_REQUIREMENTS = tr(
            "This argument specifies the requirements file to be used for pip-install during the packaging process. \n"
            "The requirements file should be located in the source directory. If it is omitted, zipapp-creator will try \n"
            "to find a default requirements file named 'requirements.txt' in the source directory. If it is not found, \n"
            "the pip-install process will be skipped."
        )
        self.MSG_PARAM_DESC_PIP_INDEX_URL = tr(
            "This argument specifies the pip index url to be used for pip-install during the packaging process. \n"
            "If it is omitted, the pip-install process will use the default pip index url."
        )
        self.MSG_PARAM_DESC_CLEANUP_DEPENDENCIES = tr(
            "This argument specifies whether to cleanup the dependencies after pip-install. If it is selected, \n"
            "zipapp-creator will try to find and delete 'unnecessary' files and directories in the installed \n"
            "dependencies, such as *.dist-info, __pycache__, etc., to reduce the size of the final zipapp archive."
        )
        self.MSG_PARAM_DESC_ENTRY = tr(
            "This argument specifies the entry point of the zipapp. \n\n"
            "If you are creating a non-self-extracting zipapp: \n"
            "1) the entry point should be in the form of 'pkg.module:fn' or 'module:fn' or \n"
            "2) just leave it empty if there is a __main__.py file in the source directory. \n\n"
            "If you are creating a self-extracting zipapp: \n"
            "1) the entry point should be the name of the main python file in the source directory and \n"
            "2) there should be no __main__.py file in the source directory. "
        )


_messages = None


def messages() -> _Messages:
    global _messages
    if _messages is None:
        _messages = _Messages()
    return _messages
