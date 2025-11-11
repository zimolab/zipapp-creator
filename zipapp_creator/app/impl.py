import traceback
import zipapp
from pathlib import Path
from string import Template
from typing import Callable

from pyguiadapterlite import GUIAdapter
from pyguiadapterlite.types import (
    dir_t,
    DirectoryValue,
    StringValue,
    file_t,
    FileValue,
    BoolValue2,
    bool_t,
    string_list,
    StringListValue,
)

from . import winconfig, winmenu
from .utils import (
    info,
    error,
    success,
    pip_install,
    cleanup_dependency,
    copy_source_tree,
    ignored_files,
)
from ..appconfig import AppConfig
from ..assets import read_asset_text
from ..common import trfunc
from ..consts import (
    DEFAULT_TARGET_NAME,
    DEFAULT_SHEBANG,
    DEFAULT_HOST_INTERPRETER,
    DIST_DIR,
    DEFAULT_COPY_EXCLUDE_PATTERNS,
    DEFAULT_PACKAGING_EXCLUDE_PATTERNS,
    DEFAULT_ENTRY_POINT,
    START_SCRIPT_TEMPLATE,
)
from ..selfextracting import create_startup_script


class CanceledByUser(RuntimeError):
    pass


class ZipAppCreator(object):

    def __init__(self, app_config: AppConfig):
        self._app_config = app_config
        self._startup_script_template = Template(read_asset_text(START_SCRIPT_TEMPLATE))

    @staticmethod
    def _packaging_filter(
        exclude_patterns: string_list, target_dir: Path
    ) -> Callable[[str | Path], bool]:

        ignored = ignored_files(
            target_dir, exclude_patterns, path_type="relative", posix=True
        )

        def _filter(path: Path) -> bool:
            return path.as_posix() not in ignored

        return _filter

    def _create_start_script(
        self, zipapp_file: str | Path, start_script_py: str
    ) -> Path:
        zipapp_file = Path(zipapp_file)
        zipapp_dir = zipapp_file.parent
        script_name = f"{zipapp_file.stem}.vbs"
        script_file = zipapp_dir / script_name
        script_content = self._startup_script_template.substitute(
            PYTHON_EXE=start_script_py, ZIPAPP_FILE=zipapp_file.name
        )
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_file

    def _on_run(
        self,
        source: dir_t,
        entry: str,
        target: str,
        shebang: str,
        compressed: bool_t,
        exclude_from_copy: string_list,
        exclude_from_packaging: string_list,
        interpreter: file_t,
        requirements: file_t,
        pip_index_url: str,
        cleanup_dependencies: bool_t,
        self_extract: bool_t,
        start_script: bool_t,
        start_script_py: str,
    ):

        cleanup_dependencies = bool(cleanup_dependencies)
        self_extract = bool(self_extract)

        source = Path(source).absolute()
        info(f"Start creating zipapp for {source.as_posix()}...")

        dist_root_dir = (source / Path(DIST_DIR)).absolute()
        dist_proj_dir = (dist_root_dir / source.name).absolute()
        info(f"Copying source files to {dist_proj_dir.as_posix()}...")

        exclude_from_copy = exclude_from_copy or []
        exclude_from_copy.append(f"{dist_root_dir.name.lstrip('/')}")

        copy_source_tree(source, dist_proj_dir, exclude_from_copy)

        requirements = requirements.strip()
        if not requirements:
            requirements = (dist_proj_dir / "requirements.txt").absolute()
            if not requirements.is_file():
                requirements = ""

        if requirements:
            try:
                pip_install(
                    py=interpreter,
                    requirements=requirements,
                    target_dir=dist_proj_dir,
                    index_url=pip_index_url,
                )
            except CanceledByUser as e:
                error(str(e))
                return
            except Exception as e:
                error(f"Failed to install dependencies: {e}")
                return
            if cleanup_dependencies:
                cleanup_dependency(target_dir=dist_proj_dir)

        try:

            target = target.strip() or "{SOURCE}.pyz"
            target = target.format(SOURCE=source.name)
            target = Path(dist_root_dir) / target
            info(f"Creating zipapp...")

            if self_extract:
                start_script = create_startup_script(dist_proj_dir, entry)
                entry = f"{start_script.stem}:main"

            zipapp.create_archive(
                source=dist_proj_dir.as_posix(),
                target=target.as_posix(),
                interpreter=shebang,
                main=entry,
                compressed=bool(compressed),
                filter=self._packaging_filter(exclude_from_packaging, dist_proj_dir),
            )
            success(f"Zipapp created successfully!")
            info(f"Zipapp file: {target.as_posix()}")

            if start_script:
                info(f"Creating start script for Windows...")
                script_path = self._create_start_script(
                    target.as_posix(), start_script_py
                )
                success(f"Start script created successfully!")
                info(f"Start script file: {script_path.as_posix()}")

        except Exception as e:
            traceback.print_exc()
            error(f"Failed to create zipapp: {e}")
            return

    # noinspection PyUnusedLocal
    @staticmethod
    def _parameter_validator(
        func_name: str,
        source: dir_t,
        entry: str,
        self_extract: bool_t,
        interpreter: file_t,
        requirements: file_t,
        start_script: bool_t,
        start_script_py: str,
        **kwargs,
    ) -> dict[str, str]:
        tr = trfunc()
        _ = func_name
        invalid_params = {}

        source = source.strip()
        if not source:
            invalid_params["source"] = tr("Source Directory is required")
        else:
            if not Path(source).is_dir():
                invalid_params["source"] = tr("Please specify a valid source directory")

        entry = entry.strip()
        if source:
            main_file = Path(source) / "__main__.py"
            if self_extract:
                if main_file.is_file():
                    invalid_params["self_extract"] = tr(
                        "An explicit __main__.py is not allowed in self-extracting zipapp, please consider remove it "
                        "and specify the entry point python file instead!"
                    )
                if not entry or not (Path(source) / entry).is_file():
                    invalid_params["entry"] = tr(
                        "Please specify a valid entry point python file in the source directory"
                    )
            else:
                if not main_file.is_file():
                    invalid_params["entry"] = tr(
                        "Please specify the entry point if there is no default entry point file(__main__.py)"
                        " in the source directory"
                    )

        interpreter = interpreter.strip()
        if not interpreter:
            invalid_params["interpreter"] = tr(
                "The host python interpreter is required for installing dependencies via pip!"
            )

        requirements = requirements.strip()
        if source and requirements:
            requirements = Path(source) / requirements
            if not requirements.is_file():
                invalid_params["requirements"] = tr(
                    "The requirements file is not found in the source directory"
                )

        start_script_py = start_script_py.strip()
        if start_script and not start_script_py:
            invalid_params["start_script_py"] = tr(
                "Please specify the Python command you want to use in the windows start script!"
            )

        return invalid_params

    def run(self):
        tr = trfunc()

        hdpi_factor = self._app_config.hdpi_factor
        if hdpi_factor <= 0:
            hdpi_factor = 100
        adapter = GUIAdapter(
            hdpi_mode=self._app_config.hdpi_mode, scale_factor_divisor=hdpi_factor
        )
        adapter.add(
            self._on_run,
            cancelable=True,
            # parameter validator
            parameters_validator=self._parameter_validator,
            # menus
            window_menus=winmenu.create_menus(),
            # window config
            window_config=winconfig.get_window_config(),
            # parameter configs below
            source=DirectoryValue(
                label=tr("Source Directory"),
                default_value=Path.cwd().as_posix(),
                group=tr("Main"),
            ),
            target=StringValue(
                label=tr("Target Filename"),
                default_value=DEFAULT_TARGET_NAME,
                group=tr("Main"),
            ),
            entry=StringValue(
                label=tr("Entry Point"),
                description=tr(
                    "The entry point of the application, usually __main__.py"
                ),
                default_value=DEFAULT_ENTRY_POINT,
                group=tr("Main"),
            ),
            shebang=StringValue(
                label=tr("Shebang"),
                default_value=DEFAULT_SHEBANG,
                group=tr("Main"),
            ),
            compressed=BoolValue2(
                label=tr("Enable deflate compression"),
                default_value=True,
                group=tr("Main"),
            ),
            self_extract=BoolValue2(
                label=tr("Create self-extracting zipapp"),
                default_value=False,
                group=tr("Main"),
            ),
            start_script=BoolValue2(
                label=tr("Create start script for Windows"),
                default_value=False,
                group=tr("Main"),
            ),
            start_script_py=StringValue(
                label=tr("Python for start script"),
                default_value=DEFAULT_HOST_INTERPRETER,
                group=tr("Main"),
            ),
            exclude_from_copy=StringListValue(
                label=tr("Exclude from Copy"),
                default_value=DEFAULT_COPY_EXCLUDE_PATTERNS,
                hide_label=True,
                group=tr("Exclude"),
            ),
            exclude_from_packaging=StringListValue(
                label=tr("Exclude from Packaging"),
                default_value=DEFAULT_PACKAGING_EXCLUDE_PATTERNS,
                hide_label=True,
                group=tr("Exclude"),
            ),
            interpreter=FileValue(
                label=tr("Host Interpreter"),
                default_value=DEFAULT_HOST_INTERPRETER,
                group=tr("Packaging"),
            ),
            requirements=FileValue(
                label=tr("Requirements File"),
                group=tr("Packaging"),
            ),
            pip_index_url=StringValue(
                label=tr("PIP Index URL"),
                group=tr("Packaging"),
            ),
            cleanup_dependencies=BoolValue2(
                label=tr("Cleanup dependencies after installation"),
                default_value=True,
                group=tr("Packaging"),
            ),
        )
        adapter.run()
