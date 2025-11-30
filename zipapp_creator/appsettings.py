from pathlib import Path
from typing import Optional, Union

from pyguiadapterlite import JsonSettingsBase
from pyguiadapterlite.types import LooseChoiceValue, BoolValue2

from zipapp_creator.messages import messages

ALL_LANGS = ["auto", "en_US", "zh_CN"]


class AppSettings(JsonSettingsBase):
    _msgs = messages()

    locale = LooseChoiceValue(
        label=_msgs.MSG_LANGUAGE_FIELD,
        choices=ALL_LANGS,
        default_value="auto",
    )
    always_on_top = BoolValue2(
        label=_msgs.MSG_ACTION_ALWAYS_ON_TOP, default_value=False
    )
    hdpi_mode = BoolValue2(label=_msgs.MSG_HDPI_MODE_FIELD, default_value=False)
    confirm_exit = BoolValue2(label=_msgs.MSG_CONFIRM_EXIT_FIELD, default_value=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._filepath = None

    def set_filepath(self, file_path: Union[str, Path]):
        self._filepath = Path(file_path).absolute().as_posix()

    @property
    def filepath(self) -> Optional[str]:
        return self._filepath

    def save(
        self,
        file_path: str = None,
        ensure_ascii=False,
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
        self.set_filepath(file_path)

    @classmethod
    def load(
        cls,
        file_path: str,
        encoding="utf-8",
        **kwargs,
    ) -> "AppSettings":
        settings = super().load(file_path=file_path, encoding=encoding, **kwargs)
        assert isinstance(settings, cls)
        settings.set_filepath(file_path)
        return settings

    @classmethod
    def default(cls) -> "AppSettings":
        return cls()
