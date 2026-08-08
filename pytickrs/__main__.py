"""
Run pytickrs
    python -m pytickrs --version
"""

import logging
import sys
from argparse import ArgumentParser, ArgumentTypeError, RawTextHelpFormatter
from pathlib import Path

from . import __version__
from .once import run_once
from .tickers import load_tickers
from .tui import run_tui

epilog = """Examples:
    python -m pytickrs --version
    python -m pytickrs --once --ticker=AAPL,MSFT,GOOG
"""

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DETAILS_TEMPLATE = PROJECT_ROOT / 'details-template.md'
DEFAULT_TICKERS_FILE = PROJECT_ROOT / 'tickers.txt'


def existing_file_path(path: str) -> str:
    """
    Custom type function for argparse to validate an existing file path.
    """
    p = Path(path)
    if not p.exists():
        raise ArgumentTypeError(f"File '{path}' does not exist.")
    if not p.is_file():
        raise ArgumentTypeError(f"'{path}' is not a file.")
    return path


def comma_separated_list(arg: str) -> list[str]:
    return arg.strip().split(',')


def main() -> int:
    """
    Get the tickers info and act on it
    """
    ap = ArgumentParser(
        prog='pytickrs',
        description='pytickrs cli v' + __version__,
        formatter_class=RawTextHelpFormatter,
        epilog=epilog,
    )
    ap.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        default=False,
        help='Tell more about what is going on',
    )
    ap.add_argument(
        '--version',
        action='store_true',
        help='Display module version and exit.',
    )
    #
    # '--once' and '--details-template' are mutually exclusive
    #
    group1 = ap.add_mutually_exclusive_group()
    group1.add_argument(
        '--once',
        action='store_true',
        default=False,
        help='One-time tickers info and recommendations',
    )
    group1.add_argument(
        '--details-template',
        type=existing_file_path,
        default=str(DEFAULT_DETAILS_TEMPLATE),
        help='Path to the Jinja details template, default: details-template.md',
    )
    #
    # '--tickers' and '--tickers-from' are mutually exclusive
    #
    group2 = ap.add_mutually_exclusive_group()
    group2.add_argument(
        '--tickers', type=comma_separated_list, help='A comma-separated list of tickers'
    )
    group2.add_argument(
        '--tickers-from',
        type=existing_file_path,
        default=str(DEFAULT_TICKERS_FILE),
        help='Path to a file with tickers (one per line), default: tickers.txt',
    )

    args = ap.parse_args()
    if args.version:
        print(__version__)
        return 0

    level = logging.DEBUG if args.verbose else logging.INFO
    tickers = args.tickers or load_tickers(args.tickers_from)
    if args.once:
        return run_once(level, tickers)

    return run_tui(level, tickers, args.details_template)


if __name__ == '__main__':
    sys.exit(main())
