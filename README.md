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

Just a templating engine.  Used to display the selected security details: [details-template.md](details-template.md)

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

For the list of the fields exposed by yfinance for use in the details page see [details-template-vars.txt](details-template-vars.txt)
