import builtins
import os
import shutil
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


def _load_appsettings():
    from zipapp_creator.appsettings import AppSettings

    _debug(f"Loading app config from: {APP_CONFIG_FILE}")
    app_config_path = Path(APP_CONFIG_FILE)
    if not app_config_path.is_file():
        _debug(f"App config file not found")
        app_config = AppSettings.default()
        _debug(f"Creating new app config file: {app_config_path.as_posix()}")
        app_config_path.parent.mkdir(parents=True, exist_ok=True)
        app_config.save(
            app_config_path.as_posix(), encoding="utf-8", ensure_ascii=False, indent=2
        )
        return app_config
    try:
        app_config = AppSettings.load(app_config_path.as_posix())
        return app_config
    except Exception as e:
        _error(
            f"Failed to load app config from file: {app_config_path.as_posix()}: {e}"
        )
        app_config = AppSettings.default()
        app_config.save(
            app_config_path.as_posix(), encoding="utf-8", ensure_ascii=False, indent=2
        )
        return app_config


# Load app config
_appsettings = _load_appsettings()
# add appsettings to builtins, so it can be accessed from anywhere
setattr(builtins, "_zipapp_creator_appsettings_", _appsettings)


def _pyguiadapter_init():
    import pyguiadapterlite

    global _appsettings
    _debug(f"Initializing PyGUIAdapterLite...")

    pyguiadapterlite.set_logging_enabled(False)
    pyguiadapterlite.set_locale_code(_appsettings.locale)
    pyguiadapterlite.set_default_parameter_label_justify("left")


_pyguiadapter_init()


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
    global _appsettings
    _debug(f"Initializing app locale...")
    app_locale_dir = Path(APP_LOCALES_DIR)

    if _DEBUG_MODE:
        _debug("Remove all locale files in debug mode")
        if app_locale_dir.is_dir():
            shutil.rmtree(app_locale_dir.as_posix(), ignore_errors=True)

    if not app_locale_dir.is_dir():
        _debug(f"Creating app locale directory: {app_locale_dir.as_posix()}")
        app_locale_dir.mkdir(parents=True)

    if not os.listdir(app_locale_dir.as_posix()):
        _debug(f"No locale files found in {app_locale_dir.as_posix()}")
        _debug(f"Copying default locale files to {app_locale_dir.as_posix()}")

        from zipapp_creator import assets

        assets.export_builtin_locales(app_locale_dir.as_posix(), overwrite=True)

    _debug(f"Setting app locale: {_appsettings.locale}")
    _appsettings.setup_i18n(app_locale_dir.as_posix())


_initialize_locale()


def main():
    from zipapp_creator.app import ZipAppCreator

    _debug("Starting ZipAppCreator")
    creator = ZipAppCreator(appsettings=_appsettings)
    creator.run()


if __name__ == "__main__":
    main()
