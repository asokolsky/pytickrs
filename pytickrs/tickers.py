from pathlib import Path

import yfinance as yf

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
    # currentPrice = info.get('currentPrice')
    # the highest price a buyer is ready to pay
    bid = info.get('bid')
    # the lowest price a seller is ready to accept
    ask = info.get('ask')
    fifty_two_week_low = info.get('fiftyTwoWeekLow')
    dayLow = info.get('dayLow')
    dayHigh = info.get('dayHigh')
    yearly_range = fifty_two_week_high - fifty_two_week_low
    assert yearly_range > 0
    if dayHigh == fifty_two_week_high or bid > fifty_two_week_high:
        recommendations.append('sell, 1y high')
    elif bid > fifty_two_week_high - (yearly_range * high_low_proximity_percent / 100):
        recommendations.append('sell, close to high')
    if dayLow == fifty_two_week_low or ask < fifty_two_week_low:
        recommendations.append('buy, 1y low')
    elif ask < fifty_two_week_low + (yearly_range * high_low_proximity_percent / 100):
        recommendations.append('buy, close to low')
    return recommendations
