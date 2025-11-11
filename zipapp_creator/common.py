import builtins
import dataclasses
import json
from pathlib import Path
from typing import Union, Optional, Callable


@dataclasses.dataclass
class Serializable(object):

    def __post_init__(self):
        self._filepath: Optional[str] = None

    def _set_filepath(self, file_path: str):
        self._filepath = file_path

    def serialize(self, **kwargs) -> Union[str, bytes]:
        obj = dataclasses.asdict(self)
        return json.dumps(obj, **kwargs)

    @property
    def filepath(self) -> Optional[str]:
        return self._filepath

    @classmethod
    def deserialize(cls, data: Union[str, bytes], **kwargs) -> "Serializable":
        if isinstance(data, str):
            obj = json.loads(data, **kwargs)
        else:
            obj = json.loads(
                data.decode(encoding=kwargs.get("encoding", "utf-8")), **kwargs
            )
        if not isinstance(obj, dict):
            raise ValueError("invalid data format")
        return cls(**obj)

    def save(
        self,
        filepath: Union[str, Path, None] = None,
        remember_filepath: bool = True,
        encoding: str = "utf-8",
        **kwargs,
    ):
        if not filepath:
            filepath = self._filepath

        if not filepath:
            raise FileNotFoundError("please specify save filepath")

        data = self.serialize(**kwargs)
        if isinstance(data, bytes):
            data = data.decode(encoding=encoding)
        with open(filepath, "w", encoding=encoding) as f:
            f.write(data)
            # if save success and remember_filepath is True, we can set the filepath property
            # next time, we can load the schema from the same file with filepath=None
            if remember_filepath:
                self._set_filepath(filepath)

    @classmethod
    def load(
        cls, filepath: Union[str, Path], encoding: str = "utf-8", **kwargs
    ) -> "Serializable":
        with open(filepath, "r", encoding=encoding) as f:
            data = f.read()
            obj = cls.deserialize(data, **kwargs)
            obj._set_filepath(filepath)
            return obj


def default_tr(text: str) -> str:
    return text


def default_ntr(text: str, text_plural: str, count: int) -> str:
    if count == 1:
        return text
    else:
        return text_plural


def trfunc() -> Callable[[str], str]:
    func = getattr(builtins, "__tr__", None)
    if func is None:
        print(
            "__tr__ function not found, i18n not prepared, a default function will be used"
        )
        func = default_tr
    return func


def ntrfunc() -> Callable[[str, str, int], str]:
    func = getattr(builtins, "__ntr__", None)
    if func is None:
        print(
            "__ntr__ function not found, i18n not prepared, a default function will be used"
        )
        func = default_ntr
    return func


def get_appconfig():
    config = getattr(builtins, "_zipapp_creator_app_config_", None)
    if config is None:
        raise RuntimeError(
            "application is not initialized, please start the app from main.py"
        )
    return config
