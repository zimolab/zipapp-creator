import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Literal, Union, List, Set

from pyguiadapterlite import uprint, is_function_cancelled

from zipapp_creator.messages import messages

_MSG_LABEL_INFO = "INFO".ljust(7)
_MSG_LABEL_ERROR = "ERROR".ljust(7)
_MSG_LABEL_WARNING = "WARNING".ljust(7)
_MSG_LABEL_SUCCESS = "SUCCESS".ljust(7)

_ENTRY_POINT_REGEX = re.compile(r"^([a-zA-Z0-9_]+\.)*([a-zA-Z0-9_]+)(:[a-zA-Z0-9_]+)?$")


class CanceledByUser(RuntimeError):
    pass


def info(msg: str, end="\n"):
    uprint(f"\033[1m{_MSG_LABEL_INFO} {msg}\033[0m", end=end)


def error(msg: str, end="\n"):
    uprint(f"\033[1m\033[31m{_MSG_LABEL_ERROR} {msg}\033[0m", end=end)


def warning(msg: str, end="\n"):
    uprint(f"\033[1m\033[33m{_MSG_LABEL_WARNING} {msg}\033[0m", end=end)


def success(msg: str, end="\n"):
    uprint(f"\033[1m\033[32m{_MSG_LABEL_SUCCESS} {msg}\033[0m", end=end)


def terminate_process(process: subprocess.Popen):
    if sys.platform == "win32":
        process.terminate()
    else:
        os.kill(process.pid, signal.SIGTERM)

    for _ in range(10):
        if process.poll() is not None:
            break
        time.sleep(0.1)
    if process.poll() is None:
        process.kill()


def read_process_output(process: subprocess.Popen) -> bool:
    cancelled = False

    lock = threading.Lock()

    def do_read():
        nonlocal cancelled
        uprint()
        while process.poll() is None:
            with lock:
                if cancelled:
                    break
            line = process.stdout.readline()
            if line:
                uprint(line, end="")
            time.sleep(0.01)
        uprint()

    read_thread = threading.Thread(target=do_read, daemon=True)
    read_thread.start()

    while read_thread.is_alive():
        if is_function_cancelled():
            terminate_process(process)
            with lock:
                cancelled = True
            break
        time.sleep(0.1)
    return cancelled


def pip_install(
    py: Union[str, Path],
    requirements: Union[str, Path],
    target_dir: Union[str, Path],
    index_url: str = None,
):
    msgs = messages()
    cmd = [
        str(py),
        "-m",
        "pip",
        "install",
        "-r",
        Path(requirements).as_posix(),
        "--target",
        Path(target_dir).as_posix(),
    ]
    if index_url:
        cmd.extend(["--index-url", index_url])
    info(msgs.MSG_START_PIP_INSTALL)

    uprint()
    uprint(shlex.join(cmd))
    uprint()

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )
    cancelled = read_process_output(process)
    if cancelled:
        raise CanceledByUser(msgs.MSG_PIP_INSTALL_CANCELLED)

    if process.returncode != 0:
        uprint(process.stdout.read())
        raise RuntimeError(f"non-zero exit code from pip install: {process.returncode}")

    success(msgs.MSG_PIP_INSTALL_SUCCESS)


def cleanup_dependency(target_dir: Union[str, Path]):
    target_dir = Path(target_dir)
    msgs = messages()
    info(msgs.MSG_CLEANUP_DEPENDENCIES)

    # 删除所有 .dist-info 目录
    for dist_info in target_dir.glob("*.dist-info"):
        if dist_info.is_dir():
            shutil.rmtree(dist_info)
            info(msgs.MSG_REMOVING.format(dist_info.as_posix()))

    # 删除所有 __pycache__ 目录
    for pycache in target_dir.rglob("__pycache__"):
        if pycache.is_dir():
            shutil.rmtree(pycache)
            info(msgs.MSG_REMOVING.format(pycache.as_posix()))

    # 删除所有 .pyc 文件
    for pyc_file in target_dir.rglob("*.pyc"):
        pyc_file.unlink()
        info(msgs.MSG_REMOVING.format(pyc_file.as_posix()))

    success(msgs.MSG_CLEANUP_DEPENDENCIES_DONE)


def copy_source_tree(
    source_dir: Union[str, Path], dist_dir: Union[str, Path], ignore_patterns: List[str]
):
    source_dir = os.path.normpath(Path(source_dir).absolute().as_posix())
    dist_dir = os.path.normpath(Path(dist_dir).absolute().as_posix())

    if os.path.isdir(dist_dir):
        shutil.rmtree(dist_dir, ignore_errors=True)

    if not os.path.isdir(dist_dir):
        os.makedirs(dist_dir, exist_ok=True)

    shutil.copytree(
        source_dir,
        dist_dir,
        ignore=shutil.ignore_patterns(*ignore_patterns),
        dirs_exist_ok=True,
    )


def ignored_files(
    start_dir: Union[str, Path],
    patterns: List[str],
    path_type: Literal["Path", "absolute", "relative"] = "Path",
    posix: bool = True,
) -> Set[Path]:
    start_dir = Path(start_dir)
    ignored = set()
    for pattern in patterns:
        selected = start_dir.rglob(pattern)
        if path_type == "Path":
            ignored.update(selected)
        elif path_type == "absolute":
            ignored.update(
                (p.absolute().as_posix() if posix else p.absolute()) for p in selected
            )
        elif path_type == "relative":
            ignored.update(
                (
                    p.relative_to(start_dir).as_posix()
                    if posix
                    else p.relative_to(start_dir)
                )
                for p in selected
            )
        else:
            raise ValueError(f"invalid path_type: {path_type}")
    return ignored


def is_valid_entry_point(entry_point: str) -> bool:
    entry_point = entry_point.strip()
    if not entry_point:
        return False
    # "pkg.module:func" or "pkg.module"
    return _ENTRY_POINT_REGEX.match(entry_point) is not None
