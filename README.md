# pytickrs README

Run CLI to get data and act on these quick, e.g.:

```sh
uv run python -m pytickrs --once
```

Alternatively use console text UI:
```sh
uv run python -m pytickrs --tickers=AAPL,GOOG
```
and press `u` to update.

## Dependencies

* [jinja2](https://jinja.palletsprojects.com/en/stable/)
* [textual](https://textual.textualize.io/)
* [yfinance](https://github.com/ranaroussi/yfinance) -  consider alternative [stockdex](https://github.com/ahnazary/stockdex).

### jinja

Just a templating engine.

### textual

To run textual demo:
```sh
uv run python -m textual
```

### yfinance

Cache location:

OS|Location
--|--------
Linux|~/.cache/py-yfinance
macOS|~/Library/Caches/py-yfinance

example ticker info:

```json
{
    'phone': '+1 8884938631',
    'longBusinessSummary': 'The fund invests at least 80% of its total assets in the securities of the underlying index and in American Depositary Receipts ("ADRs") and Global Depositary Receipts ("GDRs") based on the securities in the underlying index. The index tracks the segment of the largest and most actively traded companies - known as blue chips - on the German equities market. The fund is non-diversified.',
    'companyOfficers': [],
    'executiveTeam': [],
    'maxAge': 86400,
    'priceHint': 2,
    'previousClose': 44.275,
    'open': 44.15,
    'dayLow': 43.82,
    'dayHigh': 44.15,
    'regularMarketPreviousClose': 44.275,
    'regularMarketOpen': 44.15,
    'regularMarketDayLow': 43.82,
    'regularMarketDayHigh': 44.15,
    'trailingPE': 18.722843,
    'volume': 28690,
    'regularMarketVolume': 28690,
    'averageVolume': 56914,
    'averageVolume10days': 35310,
    'averageDailyVolume10Day': 35310,
    'bid': 43.66,
    'ask': 44.31,
    'bidSize': 2,
    'askSize': 2,
    'yield': 0.0152,
    'totalAssets': 287715392,
    'fiftyTwoWeekLow': 32.33,
    'fiftyTwoWeekHigh': 46.089,
    'allTimeHigh': 46.089,
    'allTimeLow': 17.0,
    'fiftyDayAverage': 44.6102,
    'twoHundredDayAverage': 42.249454,
    'navPrice': 45.01,
    'currency': 'USD',
    'tradeable': False,
    'category': 'Miscellaneous Region',
    'ytdReturn': 35.40144,
    'beta3Year': 1.18,
    'fundFamily': 'Global X Funds',
    'fundInceptionDate': 1413936000,
    'legalType': 'Exchange Traded Fund',
    'threeYearAverageReturn': 0.3077503,
    'fiveYearAverageReturn': 0.1271777,
    'quoteType': 'ETF',
    'symbol': 'DAX',
    'language': 'en-US',
    'region': 'US',
    'typeDisp': 'ETF',
    'quoteSourceName': 'Nasdaq Real Time Price',
    'triggerable': True,
    'customPriceAlertConfidence': 'HIGH',
    'exchange': 'NGM',
    'messageBoardId': 'finmb_271593092',
    'exchangeTimezoneName': 'America/New_York',
    'exchangeTimezoneShortName': 'EDT',
    'gmtOffSetMilliseconds': -14400000,
    'market': 'us_market',
    'esgPopulated': False,
    'regularMarketChangePercent': -0.711468,
    'regularMarketPrice': 43.96,
    'hasPrePostMarketData': True,
    'firstTradeDateMilliseconds': 1414071000000,
    'corporateActions': [],
    'postMarketTime': 1761942552,
    'regularMarketTime': 1761940802,
    'postMarketChangePercent': -0.06824108,
    'postMarketPrice': 43.93,
    'postMarketChange': -0.02999878,
    'regularMarketChange': -0.31500244,
    'regularMarketDayRange': '43.82 - 44.15',
    'fullExchangeName': 'NasdaqGM',
    'averageDailyVolume3Month': 56914,
    'fiftyTwoWeekLowChange': 11.629997,
    'fiftyTwoWeekLowChangePercent': 0.3597277,
    'fiftyTwoWeekRange': '32.33 - 46.089',
    'fiftyTwoWeekHighChange': -2.1290016,
    'fiftyTwoWeekHighChangePercent': -0.04619327,
    'fiftyTwoWeekChangePercent': 30.04763,
    'dividendDate': 1482796800,
    'dividendYield': 1.52,
    'trailingThreeMonthReturns': -0.0671,
    'trailingThreeMonthNavReturns': -0.0671,
    'netAssets': 287715392.0,
    'epsTrailingTwelveMonths': 2.347934,
    'fiftyDayAverageChange': -0.6501999,
    'fiftyDayAverageChangePercent': -0.01457514,
    'twoHundredDayAverageChange': 1.7105446,
    'twoHundredDayAverageChangePercent': 0.040486787,
    'netExpenseRatio': 0.2,
    'sourceInterval': 15,
    'exchangeDataDelayedBy': 0,
    'marketState': 'CLOSED',
    'shortName': 'Global X DAX Germany ETF',
    'longName': 'Global X DAX Germany ETF',
    'cryptoTradeable': False,
    'trailingPegRatio': None
}
```
