import builtins
from typing import Callable


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


def get_appsettings():
    appsettings = getattr(builtins, "_zipapp_creator_appsettings_", None)
    if appsettings is None:
        raise RuntimeError(
            "application is not initialized, please start the app from main.py"
        )
    return appsettings
