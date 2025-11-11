import builtins
import os
from pathlib import Path

from zipapp_creator.consts import APP_CONFIG_FILE, APP_DATADIR, APP_LOCALES_DIR

_DEBUG_MODE = True


def _debug(msg):
    if not _DEBUG_MODE:
        return
    print(f"[DEBUG] {msg}")


def _error(msg):
    if not _DEBUG_MODE:
        return
    print(f"[ERROR] {msg}")


# Add debug functions to builtins, so they can be accessed from anywhere
setattr(builtins, "_zipapp_creator_debug_", _debug)
setattr(builtins, "_zipapp_creator_error_", _error)


def _load_app_config():
    from zipapp_creator.appconfig import AppConfig

    _debug(f"Loading app config from: {APP_CONFIG_FILE}")
    app_config_path = Path(APP_CONFIG_FILE)
    if not app_config_path.is_file():
        _debug(f"App config file not found")
        app_config = AppConfig.default()
        _debug(f"Creating new app config file: {app_config_path.as_posix()}")
        app_config_path.parent.mkdir(parents=True, exist_ok=True)
        app_config.save(
            app_config_path.as_posix(), encoding="utf-8", ensure_ascii=False, indent=2
        )
        return app_config
    try:
        app_config = AppConfig.load(app_config_path.as_posix())
        return app_config
    except Exception as e:
        _error(
            f"Failed to load app config from file: {app_config_path.as_posix()}: {e}"
        )
        app_config = AppConfig.default()
        app_config.save(
            app_config_path.as_posix(), encoding="utf-8", ensure_ascii=False, indent=2
        )
        return app_config


# Load app config
_app_config = _load_app_config()
# add app_config to builtins, so it can be accessed from anywhere
setattr(builtins, "_zipapp_creator_app_config_", _app_config)


def _setup_env():
    global _app_config
    # Set environment variables
    _debug(f"Setting environment variables...")
    # MAKE SURE SETTING ENVIRONMENT VARIABLES BEFORE IMPORTING PYGUIADAPTERLITE AND ANY SUB PACKAGES OR MODULES OF IT
    # OTHERWISE I18N WON'T WORK PROPERLY
    os.environ["PYGUIADAPTERLITE_LOGGING_MESSAGE"] = "0"
    os.environ["PYGUIADAPTERLITE_LOCALE"] = _app_config.locale
    import pyguiadapterlite

    pyguiadapterlite.set_default_parameter_label_justify("left")


_setup_env()


def _check_dirs():
    _debug(f"Checking app data directories...")
    app_data_dir = Path(APP_DATADIR)
    if not app_data_dir.is_dir():
        _debug(f"Creating app data directory: {app_data_dir.as_posix()}")
        app_data_dir.mkdir(parents=True)

    app_locale_dir = Path(APP_DATADIR)
    if not app_locale_dir.is_dir():
        _debug(f"Creating app locale directory: {app_locale_dir.as_posix()}")
        app_locale_dir.mkdir(parents=True)


_check_dirs()


def _initialize_locale():
    global _app_config
    _debug(f"Initializing app locale...")
    app_locale_dir = Path(APP_LOCALES_DIR)
    if not app_locale_dir.is_dir():
        _debug(f"Creating app locale directory: {app_locale_dir.as_posix()}")
        app_locale_dir.mkdir(parents=True)

    if not os.listdir(app_locale_dir.as_posix()):
        _debug(f"No locale files found in {app_locale_dir.as_posix()}")
        _debug(f"Copying default locale files to {app_locale_dir.as_posix()}")

        from zipapp_creator import assets

        assets.export_builtin_locales(app_locale_dir.as_posix(), overwrite=True)

    _debug(f"Setting app locale: {_app_config.locale}")
    _app_config.setup_i18n(app_locale_dir.as_posix())


_initialize_locale()


def main():
    from zipapp_creator.app import ZipAppCreator

    _debug("Starting ZipAppCreator")
    creator = ZipAppCreator(app_config=_app_config)
    creator.run()


if __name__ == "__main__":
    main()
