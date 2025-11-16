import logging
import sys

# import time
from argparse import ArgumentParser, RawTextHelpFormatter
from typing import Any

import yfinance as yf
from tabulate import tabulate

from .tickers import analyze_ticker, headers, load_tickers

logger = logging.getLogger(__name__)


def eprint(*args: Any) -> None:
    print(*args, file=sys.stderr)


epilog = """Examples:
    $ fin-cli min-max --help
"""


def process_tickers(logger: logging.Logger, tickers: set[str]) -> None:
    """
    Process tickers
    """
    tkrs = yf.Tickers(list(tickers))
    tkrs.history(period='1d', repair=True, progress=False)

    # Define the headers for the table

    table_data = []
    for ticker in tkrs.tickers.values():
        info = ticker.info
        # print(info)
        table_data.append(
            [
                ticker.ticker,
                info.get('fiftyTwoWeekLow'),
                info.get('dayLow'),
                # the highest price a buyer is ready to pay
                info.get('bid'),
                info.get('currentPrice'),
                # the lowest price a seller is ready to accept
                info.get('ask'),
                info.get('dayHigh'),
                info.get('fiftyTwoWeekHigh'),
                info.get('regularMarketChange'),
                info.get('regularMarketChangePercent'),
                '; '.join(analyze_ticker(ticker)),
            ]
        )

    # sort by ticker
    sorted_data = sorted(table_data, key=lambda x: x[0])
    print(tabulate(sorted_data, headers=headers, tablefmt='simple'))
    return


def run_once(verbose: bool) -> int:
    """
    Main entry point
    """
    #
    # parse the command line
    #
    level = logging.INFO
    if verbose:
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
