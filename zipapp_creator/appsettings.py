import builtins
from typing import Optional

from pyguiadapterlite import JsonSettingsBase
from pyguiadapterlite.types import LooseChoiceValue, BoolValue2

from zipapp_creator.i18n import ZipappCreatorI18N


class AppSettings(JsonSettingsBase):
    locale = LooseChoiceValue(
        label="Language", choices=["auto", "en_US", "zh_CN"], default_value="auto"
    )
    always_on_top = BoolValue2(label="Always on Top", default_value=False)
    hdpi_mode = BoolValue2(label="High DPI Mode(Windows Only)", default_value=False)
    confirm_exit = BoolValue2(label="Exit Confirmation", default_value=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._i18n = None
        self._filepath = None

    def set_filepath(self, file_path: str):
        self._filepath = file_path

    @property
    def filepath(self) -> Optional[str]:
        return self._filepath

    def save(
        self,
        file_path: str = None,
        ensure_ascii=True,
        indent=4,
        encoding="utf-8",
        **kwargs,
    ):
        if not file_path:
            file_path = self._filepath

        if not file_path:
            raise FileNotFoundError("please specify save filepath")
        super().save(
            file_path=file_path,
            ensure_ascii=ensure_ascii,
            indent=indent,
            encoding=encoding,
            **kwargs,
        )

    @classmethod
    def load(
        cls,
        file_path: str,
        encoding="utf-8",
        **kwargs,
    ) -> "AppSettings":
        settings = super().load(file_path=file_path, encoding=encoding, **kwargs)
        assert isinstance(settings, AppSettings)
        settings.set_filepath(file_path)
        return settings

    def setup_i18n(self, locale_dir):
        self._i18n = ZipappCreatorI18N(localedir=locale_dir, locale_code=self.locale)
        # 把当前_i18n的翻译函数注入到全局空间
        # 之后，可以使用common.trfunc()/common.ntrfunc()来获取到下面两个翻译函数
        setattr(builtins, "__tr__", self.gettext)
        setattr(builtins, "__ntr__", self.ngettext)

    def gettext(self, string_id: str) -> str:
        if self._i18n is None:
            return string_id
        return self._i18n.gettext(string_id)

    def ngettext(self, singular: str, plural: str, n: int) -> str:
        if self._i18n is None:
            return singular if n == 1 else plural
        return self._i18n.ngettext(singular, plural, n)

    def tr(self, string_id: str) -> str:
        return self.gettext(string_id)

    def ntr(self, singular: str, plural: str, n: int) -> str:
        return self.ngettext(singular, plural, n)

    @classmethod
    def default(cls) -> "AppSettings":
        return cls()
