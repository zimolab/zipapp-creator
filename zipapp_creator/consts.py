from pathlib import Path

import platformdirs


APP_NAME = "zipapp-creator"
APP_VERSION = "0.1.0"
APP_DESCRIPTION = (
    "A tool to package your Python project into zipapp with its dependencies."
)
APP_LICENSE = "MIT License"
APP_COPYRIGHT = "Copyright (c) 2025 zimolab"
APP_AUTHOR = "zimolab"
APP_REPO = "https://github.com/zimolab/zipapp-creator"

APP_DATADIR = Path(platformdirs.user_data_dir(APP_NAME, ensure_exists=True))
APP_LOCALES_DIR = APP_DATADIR / "locales"
APP_CONFIG_FILE = APP_DATADIR / "config.json"


DEFAULT_TARGET_NAME = "{SOURCE}.pyz"
DEFAULT_ENTRY_POINT = "main.py"
DEFAULT_SHEBANG = "#!/usr/bin/env python3"
DEFAULT_HOST_INTERPRETER = "python3"
DEFAULT_COPY_EXCLUDE_PATTERNS = [
    "venv",
    ".venv",
    ".git",
    ".svn",
    ".hg",
    ".vscode",
    ".idea",
    "build",
    "dist",
]
DEFAULT_PACKAGING_EXCLUDE_PATTERNS = [
    "venv",
    ".venv",
    ".git",
    ".svn",
    ".hg",
    ".vscode",
    ".idea",
    "build/",
    "dist/",
    "poetry.lock",
    "pyproject.toml",
    "requirements.txt",
    "*.egg-info",
]

DIST_DIR = "zipapp_dist"

START_SCRIPT_TEMPLATE = "startup_template.vbs"
