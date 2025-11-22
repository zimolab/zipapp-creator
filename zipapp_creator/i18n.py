import io
from pathlib import Path
from typing import Optional

from pyguiadapterlite.assets import copy_assets_tree
from pyguiadapterlite.i18n import I18N

from .assets import LOCALES_DIR_NAME

DEFAULT_DOMAIN = "zc"
DEFAULT_LOCALE_CODE = "auto"
DEFAULT_LOCALE_DIR = ""
EXPORT_LOCALES = False


class ZipappCreatorI18N(I18N):
    def __init__(
        self,
        localedir: Optional[str] = DEFAULT_LOCALE_DIR,
        locale_code: Optional[str] = DEFAULT_LOCALE_CODE,
        export_locales: bool = EXPORT_LOCALES,
    ):
        super().__init__(
            domain=DEFAULT_DOMAIN,
            localedir=localedir,
            locale_code=locale_code,
            export_locales=export_locales,
        )

    def load_builtin_locale_file(
        self, domain: str, locale_code: str
    ) -> Optional[io.BytesIO]:

        from .assets import load_locale_file

        """加载内部locale文件"""
        locale_file_data = load_locale_file(domain, locale_code)
        if not locale_file_data:
            return None
        return io.BytesIO(locale_file_data)

    def export_builtin_locales(self, target_dir: str, overwrite: bool = False) -> None:
        target_dir = Path(target_dir)
        if target_dir.is_dir() and not overwrite:
            return
        target_dir.mkdir(parents=True, exist_ok=True)
        copy_assets_tree(LOCALES_DIR_NAME, target_dir.as_posix(), dirs_exist_ok=True)
