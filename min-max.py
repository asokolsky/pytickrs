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
    Load tickers from file fname
    """
    tickers: set[str] = set()
    path: Path = Path(fname)
    with path.open(encoding='utf-8') as f:
        for line1 in f:
            line = line1.strip()
            if line and not line.startswith('#'):
                tickers.add(line)
    return tickers

def analyze_ticker(ticker: yf.Ticker) -> list[str]:
    recommendations = []
    high_low_proximity_percent = 20
    info = ticker.info
    fifty_two_week_high = info.get('fiftyTwoWeekHigh')
    currentPrice = info.get('currentPrice')
    # the highest price a buyer is ready to pay
    bid = info.get('bid')
    currentPrice = info.get('currentPrice')
    # the lowest price a seller is ready to accept
    ask = info.get('ask')
    fifty_two_week_low = info.get('fiftyTwoWeekLow')
    yearly_range = fifty_two_week_high - fifty_two_week_low
    assert yearly_range > 0
    if bid > fifty_two_week_high:
        recommendations.append('sell, all time high')
    if bid > fifty_two_week_high - (yearly_range * high_low_proximity_percent / 100):
        recommendations.append('sell, close to high')
    if ask < fifty_two_week_low + (yearly_range * high_low_proximity_percent / 100):
        recommendations.append('buy, close to low')
    if ask < fifty_two_week_low:
        recommendations.append('buy, all time low')
    return recommendations

def process_tickers(logger: logging.Logger, tickers: set[str]) -> None:
    """
    Process tickers
    """
    tkrs = yf.Tickers(list(tickers))
    tkrs.history(period='1d', repair=True, progress=False)

    # Define the headers for the table
    headers = ['TKR', 'Low52w', 'Bid', 'Price', 'Ask', 'High52w', 'Thoughts']
    table_data = []
    for ticker in tkrs.tickers.values():
        info = ticker.info
        fifty_two_week_high = info.get('fiftyTwoWeekHigh')
        currentPrice = info.get('currentPrice')
        # the highest price a buyer is ready to pay
        bid = info.get('bid')
        currentPrice = info.get('currentPrice')
        # the lowest price a seller is ready to accept
        ask = info.get('ask')
        fifty_two_week_low = info.get('fiftyTwoWeekLow')
        table_data.append(
            [
                ticker.ticker,
                fifty_two_week_low,
                bid,
                currentPrice,
                ask,
                fifty_two_week_high,
                '; '.join(analyze_ticker(ticker))
            ]
        )

    # sort by ticker
    sorted_data = sorted(table_data, key=lambda x: x[0])
    print(tabulate(sorted_data, headers=headers, tablefmt='simple'))
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
