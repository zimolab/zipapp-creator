import builtins
from typing import Callable

from zipapp_creator.consts import (
    GLOBAL_VARNAME_TR_FUNC,
    GLOBAL_VARNAME_NTR_FUNC,
    GLOBAL_VARNAME_APPSETTINGS,
)


def default_tr(text: str) -> str:
    return text


def default_ntr(text: str, text_plural: str, count: int) -> str:
    if count == 1:
        return text
    else:
        return text_plural


def trfunc() -> Callable[[str], str]:
    func = getattr(builtins, GLOBAL_VARNAME_TR_FUNC, None)
    if func is None:
        print(
            "__tr__ function not found, i18n not prepared, a default function will be used"
        )
        func = default_tr
    return func


def ntrfunc() -> Callable[[str, str, int], str]:
    func = getattr(builtins, GLOBAL_VARNAME_NTR_FUNC, None)
    if func is None:
        print(
            "__ntr__ function not found, i18n not prepared, a default function will be used"
        )
        func = default_ntr
    return func


def get_appsettings():
    appsettings = getattr(builtins, GLOBAL_VARNAME_APPSETTINGS, None)
    if appsettings is None:
        raise RuntimeError(
            "application is not initialized, please start the app from main.py"
        )
    return appsettings
