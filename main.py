import builtins
import json
from pathlib import Path

from zipapp_creator.consts import APP_SETTINGS_FILE, APP_DATADIR, APP_LOCALES_DIR

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


def _setup_app_locale():
    import os
    from zipapp_creator.i18n import ZipappCreatorI18N, DEFAULT_LOCALE_CODE
    from zipapp_creator import assets

    _debug(f"Initializing app locale...")
    app_locale_dir = Path(APP_LOCALES_DIR)

    if _DEBUG_MODE:
        _debug("Remove all locale files in debug mode")
        if app_locale_dir.is_dir():
            import shutil

            shutil.rmtree(app_locale_dir.as_posix(), ignore_errors=True)

    if not app_locale_dir.is_dir():
        _debug(f"Creating app locale directory: {app_locale_dir.as_posix()}")
        app_locale_dir.mkdir(parents=True)

    if not os.listdir(app_locale_dir.as_posix()):
        _debug(f"No locale files found in {app_locale_dir.as_posix()}")
        _debug(f"Copying default locale files to {app_locale_dir.as_posix()}")

        assets.export_builtin_locales(app_locale_dir.as_posix(), overwrite=True)

    lang = DEFAULT_LOCALE_CODE
    try:
        with open(APP_SETTINGS_FILE, "r", encoding="utf-8") as f:
            appsettings_obj = json.load(f)
            lang = str(appsettings_obj.get("locale", DEFAULT_LOCALE_CODE)).strip()
    except Exception as e:
        _error(
            f"Failed to load app settings from file, use default locale: {APP_SETTINGS_FILE}: {e}"
        )

    _debug(f"Setting app locale to:  {lang}")

    i18n = ZipappCreatorI18N(localedir=app_locale_dir.as_posix(), locale_code=lang)

    def gettext(string_id: str) -> str:
        if i18n is None:
            return string_id
        return i18n.gettext(string_id)

    def ngettext(singular: str, plural: str, n: int) -> str:
        if i18n is None:
            return singular if n == 1 else plural
        return i18n.ngettext(singular, plural, n)

    # 把当前i18n的翻译函数注入到全局空间
    # 之后，可以使用common.trfunc()/common.ntrfunc()来获取到下面两个翻译函数
    setattr(builtins, "__tr__", gettext)
    setattr(builtins, "__ntr__", ngettext)


_setup_app_locale()


def _load_appsettings():
    from zipapp_creator.appsettings import AppSettings

    _debug(f"Loading app settings from: {APP_SETTINGS_FILE}")
    appsettings_path = Path(APP_SETTINGS_FILE)
    if not appsettings_path.is_file():
        _debug(f"App settings file not found")
        appsettings = AppSettings.default()
        _debug(f"Creating new app config file: {appsettings_path.as_posix()}")
        appsettings_path.parent.mkdir(parents=True, exist_ok=True)
        appsettings.save(
            appsettings_path.as_posix(), encoding="utf-8", ensure_ascii=False, indent=2
        )
        return appsettings

    try:
        appsettings = AppSettings.load(appsettings_path.as_posix())
        return appsettings
    except Exception as e:
        _error(
            f"Failed to load app settings from file: {appsettings_path.as_posix()}: {e}"
        )
        appsettings = AppSettings.default()
        appsettings.save(
            appsettings_path.as_posix(), encoding="utf-8", ensure_ascii=False, indent=2
        )
        return appsettings


# Load app settings
_appsettings = _load_appsettings()
# add appsettings to builtins namespace,
# so that it can be accessed from anywhere
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


def main():
    from zipapp_creator.app import ZipAppCreator

    _debug("Starting ZipAppCreator")
    creator = ZipAppCreator(appsettings=_appsettings)
    creator.run()


if __name__ == "__main__":
    main()
