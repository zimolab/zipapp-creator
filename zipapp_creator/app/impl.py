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
    is_valid_entry_point,
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
from ..messages import messages
from ..selfextracting import create_startup_script


class CanceledByUser(RuntimeError):
    pass


class ZipAppCreator(object):

    def __init__(self, app_config: AppConfig):
        self._app_config = app_config
        self._startup_script_template = Template(read_asset_text(START_SCRIPT_TEMPLATE))
        self._msgs = messages()

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
        host_py: file_t,
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
        info(self._msgs.MSG_START_PACKAGING)

        dist_root_dir = (source / Path(DIST_DIR)).absolute()
        dist_proj_dir = (dist_root_dir / source.name).absolute()
        info(self._msgs.MSG_COPY_SOURCE_FILES.format(dist_proj_dir.as_posix()))

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
                    py=host_py,
                    requirements=requirements,
                    target_dir=dist_proj_dir,
                    index_url=pip_index_url,
                )
            except CanceledByUser as e:
                error(str(e))
                return
            except Exception as e:
                error(self._msgs.MSG_PIP_INSTALL_FAILURE.format(str(e)))
                return
            if cleanup_dependencies:
                cleanup_dependency(target_dir=dist_proj_dir)

        try:

            target = target.strip() or "{SOURCE}.pyz"
            target = target.format(SOURCE=source.name)
            target = Path(dist_root_dir) / target
            info(self._msgs.MSG_CREATING_ZIPAPP)

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
            success(self._msgs.MSG_ZIPAPP_CREATED.format(target.as_posix()))

            if start_script:
                info(self._msgs.MSG_CREATING_STARTUP_SCRIPT)
                script_path = self._create_start_script(
                    target.as_posix(), start_script_py
                )
                success(
                    self._msgs.MSG_STARTUP_SCRIPT_CREATED.format(script_path.as_posix())
                )

        except Exception as e:
            traceback.print_exc()
            error(self._msgs.MSG_CREATE_ZIPAPP_FAILURE.format(str(e)))
            return

    # noinspection PyUnusedLocal
    def _parameter_validator(
        self,
        func_name: str,
        source: dir_t,
        entry: str,
        self_extract: bool_t,
        host_py: file_t,
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
            invalid_params["source"] = self._msgs.MSG_SOURCE_DIR_REQUIRED
        else:
            if not Path(source).is_dir():
                invalid_params["source"] = self._msgs.MSG_SOURCE_DIR_NOT_FOUND

        entry = entry.strip()
        if source:
            main_file = Path(source) / "__main__.py"
            if self_extract:
                if main_file.is_file():
                    invalid_params["self_extract"] = (
                        self._msgs.MSG_MAIN_FILE_NOT_ALLOWED
                    )
                if not entry or not (Path(source) / entry).is_file():
                    invalid_params["entry"] = self._msgs.MSG_VALID_ENTRY_FILE_REQUIRED
            else:
                if not entry:
                    if not main_file.is_file():
                        invalid_params["entry"] = self._msgs.MSG_ENTRY_REQUIRED
                else:
                    if (Path(source) / entry).is_file():
                        invalid_params["entry"] = self._msgs.MSG_INVALID_ENTRY_FORMAT
                    elif not is_valid_entry_point(entry):
                        invalid_params["entry"] = self._msgs.MSG_INVALID_ENTRY_FORMAT

        host_py = host_py.strip()
        if not host_py:
            invalid_params["host_py"] = self._msgs.MSG_HOST_PYTHON_REQUIRED

        requirements = requirements.strip()
        if source and requirements:
            requirements = Path(source) / requirements
            if not requirements.is_file():
                invalid_params["requirements"] = (
                    self._msgs.MSG_REQUIREMENTS_FILE_NOT_FOUND
                )

        start_script_py = start_script_py.strip()
        if start_script and not start_script_py:
            invalid_params["start_script_py"] = self._msgs.MSG_SCRIPT_PYTHON_REQUIRED

        return invalid_params

    def run(self):
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
                label=self._msgs.MSG_PARAM_SRC_DIR,
                default_value=Path.cwd().as_posix(),
                group=self._msgs.MSG_PARAM_GROUP_MAIN,
                description=self._msgs.MSG_PARAM_DESC_SRC_DIR,
            ),
            target=StringValue(
                label=self._msgs.MSG_PARAM_TARGET,
                default_value=DEFAULT_TARGET_NAME,
                group=self._msgs.MSG_PARAM_GROUP_MAIN,
                description=self._msgs.MSG_PARAM_DESC_TARGET,
            ),
            entry=StringValue(
                label=self._msgs.MSG_PARAM_ENTRY,
                description=self._msgs.MSG_PARAM_DESC_ENTRY,
                default_value=DEFAULT_ENTRY_POINT,
                group=self._msgs.MSG_PARAM_GROUP_MAIN,
            ),
            shebang=StringValue(
                label=self._msgs.MSG_PARAM_SHEBANG,
                default_value=DEFAULT_SHEBANG,
                group=self._msgs.MSG_PARAM_GROUP_MAIN,
                description=self._msgs.MSG_PARAM_DESC_SHEBANG,
            ),
            compressed=BoolValue2(
                label=self._msgs.MSG_PARAM_DEFLATE_COMPRESSION,
                default_value=True,
                group=self._msgs.MSG_PARAM_GROUP_MAIN,
                description=self._msgs.MSG_PARAM_DESC_DEFLATE_COMPRESSION,
            ),
            self_extract=BoolValue2(
                label=self._msgs.MSG_PARAM_SELF_EXTRACTING,
                default_value=False,
                group=self._msgs.MSG_PARAM_GROUP_MAIN,
                description=self._msgs.MSG_PARAM_DESC_SELF_EXTRACTING,
            ),
            start_script=BoolValue2(
                label=self._msgs.MSG_PARAM_START_SCRIPT,
                default_value=False,
                group=self._msgs.MSG_PARAM_GROUP_MAIN,
                description=self._msgs.MSG_PARAM_DESC_START_SCRIPT,
            ),
            start_script_py=StringValue(
                label=self._msgs.MSG_STRAT_SCRIPT_PYTHON,
                default_value=DEFAULT_HOST_INTERPRETER,
                group=self._msgs.MSG_PARAM_GROUP_MAIN,
                description=self._msgs.MSG_PARAM_DESC_SCRIPT_PYTHON,
            ),
            exclude_from_copy=StringListValue(
                label=self._msgs.MSG_PARMA_EXCLUDE_FROM_COPY,
                default_value=DEFAULT_COPY_EXCLUDE_PATTERNS,
                hide_label=True,
                group=self._msgs.MSG_PARAM_GROUP_EXCLUDE,
                description=self._msgs.MSG_PARAM_DESC_EXCLUDE_FROM_COPY,
            ),
            exclude_from_packaging=StringListValue(
                label=self._msgs.MSG_PARAM_EXCLUDE_FROM_PACKAGING,
                default_value=DEFAULT_PACKAGING_EXCLUDE_PATTERNS,
                hide_label=True,
                group=self._msgs.MSG_PARAM_GROUP_EXCLUDE,
                description=self._msgs.MSG_PARAM_DESC_EXCLUDE_FROM_PACKAGING,
            ),
            host_py=FileValue(
                label=self._msgs.MSG_PARAM_HOST_PYTHON,
                default_value=DEFAULT_HOST_INTERPRETER,
                group=self._msgs.MSG_PARAM_GROUP_PACKAGING,
                description=self._msgs.MSG_PARAM_DESC_HOST_PYTHON,
            ),
            requirements=FileValue(
                label=self._msgs.MSG_PARAM_REQUIREMENTS,
                group=self._msgs.MSG_PARAM_GROUP_PACKAGING,
                description=self._msgs.MSG_PARAM_DESC_REQUIREMENTS,
            ),
            pip_index_url=StringValue(
                label=self._msgs.MSG_PARAM_PIP_INDEX_URL,
                group=self._msgs.MSG_PARAM_GROUP_PACKAGING,
                description=self._msgs.MSG_PARAM_DESC_PIP_INDEX_URL,
            ),
            cleanup_dependencies=BoolValue2(
                label=self._msgs.MSG_PARMA_CLEANUP_DEPENDENCIES,
                default_value=True,
                group=self._msgs.MSG_PARAM_GROUP_PACKAGING,
                description=self._msgs.MSG_PARAM_DESC_CLEANUP_DEPENDENCIES,
            ),
        )
        adapter.run()
