import os
import subprocess
import sys
import tkinter
from pathlib import Path
from typing import Optional, Union


def move_to_desktop_center(window: Union[tkinter.Tk, tkinter.Toplevel]):
    """将窗口移动到屏幕中心"""
    window.withdraw()
    # window.update_idletasks()
    window.update()
    w, h = window.winfo_width(), window.winfo_height()
    x = (window.winfo_screenwidth() - w) // 2
    y = (window.winfo_screenheight() - h) // 2
    window.geometry(f"+{int(x)}+{int(y)}")
    window.deiconify()


def move_to_center_of(
    window: Union[tkinter.Tk, tkinter.Toplevel],
    ref_window: Optional[Union[tkinter.Tk, tkinter.Toplevel]] = None,
):
    """将窗口移动到另一个窗口的中心位置"""
    if ref_window is None:
        move_to_desktop_center(window)
        return
    window.withdraw()
    window.update()
    ref_window.update()
    x = (
        ref_window.winfo_rootx()
        + ref_window.winfo_width() // 2
        - window.winfo_width() // 2
    )
    y = (
        ref_window.winfo_rooty()
        + ref_window.winfo_height() // 2
        - window.winfo_height() // 2
    )
    window.geometry(f"+{int(x)}+{int(y)}")
    window.deiconify()


def open_file_in_editor(file_path: Union[str, Path]):
    """
    使用系统默认文本编辑器打开文件
    """
    file_path = str(Path(file_path).resolve())
    if sys.platform.startswith("win"):
        # Windows 系统
        os.startfile(file_path)
    elif sys.platform.startswith("darwin"):
        # macOS 系统
        subprocess.run(["open", file_path])
    else:
        # Linux 和其他 Unix 系统
        subprocess.run(["xdg-open", file_path])
