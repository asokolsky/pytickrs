import logging
import sys

# import time
from argparse import ArgumentParser, RawTextHelpFormatter
from pathlib import Path
from typing import Any

import yfinance as yf
from tabulate import tabulate

logger = logging.getLogger(__name__)


def eprint(*args: Any) -> None:
    print(*args, file=sys.stderr)


epilog = """Examples:
    $ fin-cli min-max --help
"""


def load_tickers(fname: str) -> set[str]:
    """
    Load tickers from a file
    """
    tickers: set[str] = set()
    path: Path = Path(fname)
    with path.open(encoding='utf-8') as f:
        for line1 in f:
            line = line1.strip()
            if line and not line.startswith('#'):
                tickers.add(line)
    return tickers


def process_tickers(logger: logging.Logger, tickers: set[str]) -> None:
    """
    Process tickers
    """
    tkrs = yf.Tickers(list(tickers))
    tkrs.history(period='1y', repair=True)

    # Define the headers for the table
    table_data = [
        # headers
        ['TKR', '52w low', 'Price', '52w high', 'TODO']
    ]
    for ticker in tkrs.tickers.values():
        info = ticker.info
        fifty_two_week_high = info.get('fiftyTwoWeekHigh')
        currentPrice = info.get('currentPrice')
        fifty_two_week_low = info.get('fiftyTwoWeekLow')
        table_data.append(
            [
                ticker.ticker,
                fifty_two_week_low,
                currentPrice,
                fifty_two_week_high,
                'n/a',
            ]
        )

    print(tabulate(table_data, headers='firstrow', tablefmt='simple'))  # "fancy_grid"))
    return


def main() -> int:
    """
    Main entry point
    """
    ap = ArgumentParser(
        prog='fin-cli',
        description='Fast finance cli',
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
    #
    # parse the command line
    #
    args = ap.parse_args()
    level = logging.INFO
    if args.verbose:
        level = logging.DEBUG
    logging.basicConfig(level=level)
    logger = logging.getLogger(__name__)
    try:
        tickers = load_tickers('tickers.txt')
        process_tickers(logger, tickers)

        return 0

    except KeyboardInterrupt:
        eprint('Caught KeyboardInterrupt')

    return 1


if __name__ == '__main__':
    sys.exit(main())
