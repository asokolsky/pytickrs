from collections.abc import Mapping
from pathlib import Path
from typing import Protocol


class Ticker(Protocol):
    @property
    def info(self) -> Mapping[str, object]: ...


headers = (
    'TIKR',
    'Low1y',
    'Low1d',
    'Bid',
    'Price',
    'Ask',
    'High1d',
    'High1y',
    'Change',
    'Change %',
    'Thoughts',
)
header2ticker_info = {
    'Low1y': 'fiftyTwoWeekLow',
    'Low1d': 'dayLow',
    'Bid': 'bid',
    'Price': 'currentPrice',
    'Ask': 'ask',
    'High1d': 'dayHigh',
    'High1y': 'fiftyTwoWeekHigh',
    'Change': 'regularMarketChange',
    'Change %': 'regularMarketChangePercent',
}

#
# Ensure these are present to avoid issues with details display
#
ticker_info_sanitize_keys = [
    'postMarketPrice',
    'postMarketChange',
    'postMarketChangePercent',
    'targetMeanPrice',
    'trailingPE',
    'epsTrailingTwelveMonths',
    'dividendRate',
    'dividendYield',
]


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
                tickers.add(line.upper())
    return tickers


def _number(info: Mapping[str, object], key: str) -> float | None:
    value = info.get(key)
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    return float(value)


def analyze_info(info: Mapping[str, object]) -> list[str]:
    recommendations: list[str] = []
    high_low_proximity_percent = 20
    fifty_two_week_high = _number(info, 'fiftyTwoWeekHigh')
    fifty_two_week_low = _number(info, 'fiftyTwoWeekLow')
    if fifty_two_week_high is None or fifty_two_week_low is None:
        return recommendations

    yearly_range = fifty_two_week_high - fifty_two_week_low
    if yearly_range <= 0:
        return recommendations

    # the highest price a buyer is ready to pay
    bid = _number(info, 'bid')
    # the lowest price a seller is ready to accept
    ask = _number(info, 'ask')
    day_low = _number(info, 'dayLow')
    day_high = _number(info, 'dayHigh')

    if day_high == fifty_two_week_high or (
        bid is not None and bid > fifty_two_week_high
    ):
        recommendations.append('sell, 1y high')
    elif bid is not None and bid > fifty_two_week_high - (
        yearly_range * high_low_proximity_percent / 100
    ):
        recommendations.append('sell, close to high')
    if day_low == fifty_two_week_low or (ask is not None and ask < fifty_two_week_low):
        recommendations.append('buy, 1y low')
    elif ask is not None and ask < fifty_two_week_low + (
        yearly_range * high_low_proximity_percent / 100
    ):
        recommendations.append('buy, close to low')
    return recommendations


def analyze_ticker(ticker: Ticker) -> list[str]:
    return analyze_info(ticker.info)
