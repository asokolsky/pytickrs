"""
Run pytickrs
    python -m pytickrs --version
"""

import sys
from argparse import ArgumentParser, RawTextHelpFormatter

from . import __version__

epilog = """Examples:
    python -m pytickrs --version
"""


def main() -> int:
    """
    Run the simulation
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
        '--once',
        action='store_true',
        default=False,
        help='One-time tickers info and recommendations',
    )
    ap.add_argument(
        '--version',
        action='store_true',
        help='Display module version and exit.',
    )
    args = ap.parse_args()
    if args.version:
        print(__version__)
        return 0
    if args.once:
        from .once import run_once

        return run_once(args.verbose)

    from .tui import run_tui

    return run_tui(args.verbose)


if __name__ == '__main__':
    sys.exit(main())
