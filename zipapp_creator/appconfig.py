import builtins
import dataclasses
from typing import Dict, Any, Callable

from .common import Serializable
from .utils import open_file_in_editor


@dataclasses.dataclass
class AppConfig(Serializable):
    locale: str = "auto"
    clear_output_on_run: bool = True
    always_on_top: bool = False
    hdpi_mode: bool = False
    hdpi_factor: int = 80

    def __post_init__(self):
        self._i18n = None

    def setup_i18n(self, locale_dir):
        from . import i18n

        self._i18n = i18n.create(localedir=locale_dir, locale_code=self.locale)
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
    def default(cls) -> "AppConfig":
        return cls()

    @staticmethod
    def _to_bool(value: str) -> bool:
        return value.strip().lower() in ["true", "yes", "1"]

    @staticmethod
    def _to_str(value: str) -> str:
        return str(value)

    @staticmethod
    def _to_int(value: str) -> int:
        return int(value)

    def _value_converter(self, field_type: str) -> Callable[[str], Any]:
        if field_type == "bool":
            return self._to_bool
        elif field_type == "str":
            return self._to_str
        elif field_type == "int":
            return self._to_int
        else:
            return self._to_str

    def open_in_editor(self):
        if self.filepath is None:
            raise RuntimeError("current config has not been bound to a cfile")
        open_file_in_editor(self.filepath)

    def list(self) -> str:
        fields_names = [
            f.name for f in dataclasses.fields(self) if not f.name.startswith("_")
        ]
        ls = []
        for field_name in fields_names:
            value = getattr(self, field_name)
            ls.append(field_name.ljust(20) + f"= {value}")
        return "\n".join(ls)

    def set(self, new_configs: Dict[str, str]):
        fields_types = {
            f.name: f.type
            for f in dataclasses.fields(self)
            if not f.name.startswith("_")
        }
        fields_names = [
            f.name for f in dataclasses.fields(self) if not f.name.startswith("_")
        ]

        for key, value in new_configs.items():
            if key not in fields_names:
                print(f"Skipping: {key}")
                continue
            filed_type = fields_types.get(key, str)
            conv = self._value_converter(filed_type.__name__)
            print(f"Setting: {key.ljust(20)} = {value}")
            try:
                value = conv(value)
            except ValueError:
                print(f"invalid value: {value}")
                continue
            setattr(self, key, value)
