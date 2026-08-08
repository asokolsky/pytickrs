"""
Playing with yfinance and textual
"""

import tomllib
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from .log import setup_logging

try:
    __version__ = version('pytickrs')
except PackageNotFoundError:
    pyproject_path = Path(__file__).parents[1] / 'pyproject.toml'
    with pyproject_path.open('rb') as pyproject_file:
        __version__ = str(tomllib.load(pyproject_file)['project']['version'])

__all__ = [
    # log.py
    'setup_logging'
    #'print_logging_tree',
]
