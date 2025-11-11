import io
import os
from pathlib import Path
from typing import Optional


DEFAULT_DOMAIN = "zc"
DEFAULT_LOCALE_CODE = "auto"
DEFAULT_LOCALE_DIR = ""

ENV_AUTO_EXPORT = "ZC_EXPORT_LOCALES"
ENV_LOCALE = "ZC_LOCALE"
ENV_LOCALE_DIR = "ZC_LOCALE_DIR"

_I18N_CLASS = None


def get_i18n_class():
    global _I18N_CLASS
    if _I18N_CLASS is None:
        from pyguiadapterlite.i18n import I18N

        class _I18N(I18N):

            def __init__(
                self,
                domain: str = DEFAULT_DOMAIN,
                localedir: str = DEFAULT_LOCALE_DIR,
                locale_code: str = DEFAULT_LOCALE_CODE,
            ):
                super().__init__(domain, localedir, locale_code)

            def export_builtin_locales(
                self, target_dir: str, overwrite: bool = False
            ) -> None:
                from pyguiadapterlite.assets import copy_assets_tree
                from .assets import LOCALES_DIR_NAME

                target_dir = Path(target_dir)
                if target_dir.is_dir() and not overwrite:
                    return
                target_dir.mkdir(parents=True, exist_ok=True)
                copy_assets_tree(
                    LOCALES_DIR_NAME, target_dir.as_posix(), dirs_exist_ok=True
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

            def get_domain_from_env(self, default: str = DEFAULT_DOMAIN) -> str:
                return DEFAULT_DOMAIN

            def get_locale_code_from_env(
                self, default: str = DEFAULT_LOCALE_CODE
            ) -> str:
                return os.environ.get(ENV_LOCALE, default).strip()

            def get_locales_dir_from_env(
                self, default: str = DEFAULT_LOCALE_DIR
            ) -> str:
                return os.environ.get(ENV_LOCALE_DIR, default).strip()

            def should_export_locales(self) -> bool:
                return os.environ.get(ENV_AUTO_EXPORT, "false").lower() == "true"

        _I18N_CLASS = _I18N
    return _I18N_CLASS


def create(**kwargs):
    clazz = get_i18n_class()
    return clazz(**kwargs)
