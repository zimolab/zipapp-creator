from typing import Optional

from pyguiadapterlite import JsonSettingsBase
from pyguiadapterlite.types import LooseChoiceValue, BoolValue2

from zipapp_creator.messages import messages


class AppSettings(JsonSettingsBase):
    _msgs = messages()

    locale = LooseChoiceValue(
        label=_msgs.MSG_LANGUAGE_FIELD,
        choices=["auto", "en_US", "zh_CN"],
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

    @classmethod
    def default(cls) -> "AppSettings":
        return cls()
