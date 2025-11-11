from tkinter import Tk, Toplevel, Widget
from tkinter.ttk import Frame, Label
from typing import Union

from pyguiadapterlite import BaseSimpleDialog

from ..consts import (
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION,
    APP_COPYRIGHT,
    APP_REPO,
    APP_LICENSE,
)


class AboutFrame(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.license_label = None
        self.website_label = None
        self.copyright_label = None
        self.description_label = None
        self.version_label = None
        self.title_label = None
        self.parent = parent

        # 默认的about内容
        self.about_data = {
            "title": APP_NAME,
            "version": APP_VERSION,
            "description": APP_DESCRIPTION,
            "copyright": APP_COPYRIGHT,
            "website": APP_REPO,
            "license": APP_LICENSE,
        }

        self.create_widgets()
        self.update_content()

    def create_widgets(self):
        """创建界面组件"""
        # 标题
        self.title_label = Label(self, font=("Arial", 16, "bold"), foreground="#2c3e50")
        self.title_label.pack(pady=(20, 5))

        # 版本
        self.version_label = Label(self, font=("Arial", 10), foreground="#7f8c8d")
        self.version_label.pack(pady=(0, 15))

        # 描述
        self.description_label = Label(
            self,
            font=("Arial", 10),
            foreground="#34495e",
            wraplength=350,
            justify="center",
        )
        self.description_label.pack(pady=(0, 10), padx=20)

        # 版权信息
        self.copyright_label = Label(self, font=("Arial", 9), foreground="#95a5a6")
        self.copyright_label.pack(pady=(10, 5))

        # 网站链接
        self.website_label = Label(
            self, font=("Arial", 9, "underline"), foreground="#3498db", cursor="hand2"
        )
        self.website_label.pack(pady=(0, 5))

        # 许可证信息
        self.license_label = Label(self, font=("Arial", 8), foreground="#bdc3c7")
        self.license_label.pack(pady=(5, 20))

        # 绑定网站标签点击事件
        self.website_label.bind("<Button-1>", self.open_website)

    def update_content(self):
        """更新界面内容"""
        self.title_label.config(text=self.about_data["title"])
        self.version_label.config(text=f"version {self.about_data['version']}")
        self.description_label.config(text=self.about_data["description"])
        self.copyright_label.config(text=self.about_data["copyright"])
        self.website_label.config(text=self.about_data["website"])
        self.license_label.config(text=self.about_data["license"])

    def set_content(self, **kwargs):
        """
        设置about内容

        参数:
            title: 应用程序标题
            version: 版本号
            description: 描述信息
            copyright: 版权信息
            website: 网站链接
            license: 许可证信息
        """
        self.about_data.update(kwargs)
        self.update_content()

    def open_website(self, event=None):
        """打开网站链接"""
        import webbrowser

        webbrowser.open(self.about_data["website"])


class AboutDialog(BaseSimpleDialog):
    def __init__(
        self,
        parent: Union[Tk, Widget] = None,
        title: str = "",
        size: tuple = (400, 300),
        resizable: bool = True,
        ok_text: str = "Ok",
        cancel_text: str = "Cancel",
    ):
        super().__init__(parent, title, size, resizable, ok_text, cancel_text)

    def on_create_content_area(self, dialog: Toplevel):
        self._content_area = AboutFrame(dialog)
        self._content_area.pack(fill="both", expand=True)

    def on_ok(self):
        self.on_cancel()
