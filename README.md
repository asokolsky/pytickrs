# pytickrs README

Install the configured tools and project dependencies:

```sh
mise trust
mise install
mise run venv
```

Run the CLI once to print the current ticker data and recommendations:

```sh
mise run pytickrs -- --once
```

Alternatively, launch the console text UI:

```sh
mise run pytickrs -- --tickers=AAPL,GOOG
```

Press `u` to update.

## Configuration files

### `tickers.txt`

The default watchlist. Add one ticker symbol per line; blank lines and lines
beginning with `#` are ignored. Symbols are normalized to uppercase and
duplicates are removed. Use a different watchlist with `--tickers-from`:

```sh
mise run pytickrs -- --tickers-from=watchlist.txt
```

The `--tickers` option can be used instead for a comma-separated list supplied
on the command line.

### `details-template.md`

The Jinja template used to render the selected ticker in the TUI details pane.
It produces Markdown and can reference fields returned by `yfinance`, such as
`longName`, `currentPrice`, and `longBusinessSummary`. Start the TUI with a
different template using `--details-template`:

```sh
mise run pytickrs -- --details-template=custom-details.md
```

### `details-template-vars.txt`

A reference snapshot of the `yfinance` fields available to the details
template, including example values and nested structures. Use it when adding or
changing expressions in `details-template.md`. The available fields can vary by
security and over time, so templates should account for missing values.

## Development

Use the configured mise tasks for routine development:

```sh
mise run format
mise run lint
mise run mypy
mise run tests
```

## Dependencies

* [jinja2](https://jinja.palletsprojects.com/en/stable/)
* [textual](https://textual.textualize.io/)
* [yfinance](https://github.com/ranaroussi/yfinance) -  consider alternative [stockdex](https://github.com/ahnazary/stockdex).

### jinja

Just a templating engine.  Used to display the selected security details: [details-template.md](details-template.md)

### textual

To run textual demo:
```sh
mise exec -- python -m textual
```

### yfinance

Cache location:

OS|Location
--|--------
Linux|~/.cache/py-yfinance
macOS|~/Library/Caches/py-yfinance

For the list of the fields exposed by yfinance for use in the details page see [details-template-vars.txt](details-template-vars.txt)
