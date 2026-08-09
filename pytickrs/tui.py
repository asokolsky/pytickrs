import logging
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from typing import ClassVar

import yfinance as yf
from jinja2 import Environment, FileSystemLoader, Template
from jinja2.exceptions import TemplateSyntaxError, UndefinedError
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.message import Message
from textual.widgets import DataTable, Footer, Header, Label, MarkdownViewer
from textual.worker import Worker

from .log import eprint, setup_logging
from .split_pane import SplitContainer
from .tickers import (
    analyze_info,
    header2ticker_info,
    headers,
    ticker_info_sanitize_keys,
)

log: logging.Logger | None = None

CSS = """
Horizontal#footer-outer {
    height: 1;
    dock: bottom;
}
/* Reserve the rest of the footer row for Textual's key-binding hints. */
Horizontal#footer-inner {
    width: 66%;
    dock: right;
}
Label#status {
    width: 33%;
    text-align: left;
    dock: left;
}
"""


class TaskCompleteMessage(Message):
    """A message indicating the background task is complete."""

    def __init__(
        self,
        ticker_info: dict[str, dict[str, object]],
        errors: dict[str, str],
    ) -> None:
        super().__init__()
        self.ticker_info = ticker_info
        self.errors = errors


class TaskFailedMessage(Message):
    """A message indicating the background task failed."""

    def __init__(self, error: Exception) -> None:
        super().__init__()
        self.error = error


class TheApp(App):
    """
    A simple Textual app using yfinance to retrieve and display stock data.
    1. Load tickers from a file
    2. Display tickers in a table
    3. Update ticker data on user command
    4. Sort table by column on header click
    5. Quit app on user command
    6. Log actions to a file
    7. Use yfinance to fetch ticker data
    """

    TITLE = 'Stock Analyzer'
    SUB_TITLE = 'The most important app you will ever need'
    CSS = CSS

    BINDINGS: ClassVar = [
        ('q', 'quit_app', 'Quit'),
        ('u', 'update', 'Update'),
    ]

    def __init__(self, tickers: set[str], details_template: Template) -> None:
        super().__init__()
        self.column_index_selected = 0
        self.column_sort_reverse = False
        self.tickers = tickers
        assert self.tickers
        self.details_template = details_template
        assert self.details_template
        self.ticker_info: dict[str, dict[str, object]] = {}
        return

    def compose(self) -> ComposeResult:
        """
        Create child widgets for the app.
        """
        assert log is not None
        log.debug('compose %s', self)
        yield Header()
        yield SplitContainer(
            before=DataTable(cursor_type='row', zebra_stripes=True, id='tickers'),
            after=MarkdownViewer(
                id='details', show_table_of_contents=False, open_links=False
            ),
        )
        with Horizontal(id='footer-outer'):
            yield Label('Updating...', id='status')
            with Horizontal(id='footer-inner'):
                yield Footer(id='footer')
        return

    def on_mount(self) -> None:
        assert log is not None
        log.debug('on_mount %s', self)

        def fill_table(table: DataTable, headers: list[str], rows: list[str]) -> None:
            # add columns and set column key
            for h in headers:
                table.add_column(h, key=h)

            # add rows and set row key
            for row in rows:
                r = [row if h == headers[0] else '.' for h in headers]
                table.add_row(*r, key=row)
            return

        self.tickers_table = self.query_one('#tickers', DataTable)
        self.details = self.query_one('#details', MarkdownViewer)
        self.status = self.query_one('#status', Label)
        # self.footer_inner = self.query_one('#footer-inner')
        self.footer = self.query_one('#footer', Footer)
        fill_table(self.tickers_table, list(headers), sorted(self.tickers))

        # adjust footer status styles
        self.status.styles.background = self.footer.styles.background
        self.status.styles.color = self.footer.styles.color
        self.call_after_refresh(self.action_update)
        return

    def on_data_table_header_selected(self, message: DataTable.HeaderSelected) -> None:
        """
        Handles a click on a column header.
        """
        assert log is not None
        log.debug('on_data_table_header_selected %s', message.data_table.id)
        if message.data_table != self.tickers_table:
            log.debug('Ignoring message: %s', message)
            return
        if self.column_index_selected != message.column_index:
            self.column_sort_reverse = False
            self.column_index_selected = message.column_index
        else:
            self.column_sort_reverse = not self.column_sort_reverse

        try:
            self.tickers_table.sort(
                message.column_key, reverse=self.column_sort_reverse
            )
        except Exception:
            log.exception('Error sorting table:')
        return

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        """
        Row in the DataTable is highlighted.
        """
        row_key = event.row_key
        assert log is not None
        log.debug('Row highlighted: %s %s', row_key.value, event.data_table.id)
        if event.data_table != self.tickers_table:
            log.debug('Ignoring event: %s', event)
            return
        symbol = row_key.value
        if symbol is None:
            return
        info = self.ticker_info.get(symbol)
        if info is not None:
            self.update_details(info)
            self.set_status(str(info.get('longName', symbol)))
            return
        self.set_status(symbol)
        return

    def update_details(self, info: Mapping[str, object]) -> None:
        """
        Update the details table with info from the selected ticker.
        """
        assert log is not None
        log.debug('update_details')
        tvars = dict(info.items())
        log.debug('corporateActions: %s', tvars.get('corporateActions'))
        # sanitize data - these are broken for NTDOY
        for key in ticker_info_sanitize_keys:
            if key not in tvars:
                tvars[key] = 0
            elif tvars[key] == '':
                tvars[key] = 0
        markdown = self.details_template.render(tvars)
        log.debug('markdown %s', markdown)
        self.details.document.update(markdown)
        return

    # def on_timer(self, message: Timer) -> None:
    #    """Handles a Timer event."""
    #    log.debug('on_timer %s', message)
    #    return

    # def on_idle(self, message: Idle) -> None:
    #    """Handles an Idle event."""
    #    # log.debug('on_idle %s', message)
    #    return

    def action_quit_app(self) -> None:
        """An action to quit the application."""
        assert log is not None
        log.debug('action_quit_app %s', self)
        self.exit()

    def action_update(self) -> None:
        """
        Update the values for tickers
        """
        assert log is not None
        log.debug('action_update %s', self)
        self.set_status('Updating...')
        self.run_long_task()
        return

    @work(group='yfinance', exclusive=True, thread=True)
    def run_long_task(self) -> None:
        """
        Download ticker info in the background.
        group: A short string to identify a group of workers.
        exclusive: Cancel all workers in the same group.
        thread: Mark the method as a thread worker.
        """
        assert log is not None
        try:
            tickers = yf.Tickers(list(self.tickers))
            tickers.history(period='1d', repair=True, progress=False)
            ticker_info: dict[str, dict[str, object]] = {}
            errors: dict[str, str] = {}

            def fetch_info(ticker: yf.Ticker) -> tuple[str, dict[str, object]]:
                return ticker.ticker, dict(ticker.info)

            workers = min(6, len(tickers.tickers))
            with ThreadPoolExecutor(max_workers=workers) as executor:
                futures = {
                    executor.submit(fetch_info, ticker): ticker.ticker
                    for ticker in tickers.tickers.values()
                }
                for future in as_completed(futures):
                    symbol = futures[future]
                    try:
                        ticker_symbol, info = future.result()
                        ticker_info[ticker_symbol] = info
                    except Exception as error:
                        log.exception('Failed to fetch info for %s', symbol)
                        errors[symbol] = str(error) or type(error).__name__

            self.post_message(TaskCompleteMessage(ticker_info, errors))
        except Exception as error:
            log.exception('Failed to update ticker data')
            self.post_message(TaskFailedMessage(error))
        return

    def on_task_complete_message(self, message: TaskCompleteMessage) -> None:
        """
        Called when the background task is complete.
        """
        self.notify('Background task finished!')

        def update_table(
            table: DataTable, ticker_info: Mapping[str, Mapping[str, object]]
        ) -> None:
            for symbol, info in ticker_info.items():
                for k, v in header2ticker_info.items():
                    if table.get_cell(symbol, k) is None:
                        continue
                    if info.get(v) is None:
                        continue
                    table.update_cell(symbol, k, info.get(v))
                table.update_cell(
                    symbol,
                    headers[-1],
                    '; '.join(analyze_info(info)),
                    update_width=True,
                )

            return

        try:
            # Only successful responses are included in message.ticker_info. Merge them
            # into the cache so a transient failure keeps the symbol's last known details.
            self.ticker_info.update(message.ticker_info)
            update_table(self.tickers_table, message.ticker_info)
        except Exception as error:
            assert log is not None
            log.exception('Failed to apply ticker data')
            self.on_task_failed_message(TaskFailedMessage(error))
            return
        updated = len(message.ticker_info)
        failed = len(message.errors)
        if failed:
            failed_symbols = ', '.join(sorted(message.errors))
            self.set_status(f'Updated {updated}; failed {failed}: {failed_symbols}')
            self.notify(
                failed_symbols,
                title=f'{failed} ticker updates failed',
                severity='warning',
            )
        else:
            self.set_status(f'Updated {updated} tickers')
        # self.status.styles.width = '25%'
        # self.footer_inner.styles.width = '75%'
        assert log is not None
        log.debug('action_update DONE')
        return

    def on_task_failed_message(self, message: TaskFailedMessage) -> None:
        """Report a background refresh failure without exiting the app."""
        error_text = str(message.error) or type(message.error).__name__
        self.set_status(f'Update failed: {error_text}')
        self.notify(error_text, title='Ticker update failed', severity='error')

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Called when the worker state changes."""
        assert log is not None
        log.debug('on_worker_state_changed %s', event)
        return

    def set_status(self, text: str) -> None:
        """Set the status label text."""
        assert log is not None
        log.debug('set_status %s', text)
        # self.status.styles.width = '75%'
        # self.footer_inner.styles.width = '25%'
        self.status.update(text)
        return


#
# Custom global functions for use in the jinja template
#
def format_num(num: str) -> str:
    try:
        val = int(num)
        if val < 10000:
            return f'{val:,d}'
        if val < 10000000:
            val = val // 1000
            return f'{val:,d}K'
        if val < 10000000000:
            val = val // 1000000
            return f'{val:,d}M'
        if val < 10000000000000:
            val = val // 1000000000
            return f'{val:,d}B'
        val = val // 1000000000000
        return f'{val:,d}T'
    except (UndefinedError, ValueError):
        pass
    return ''


def format_date(val: str) -> str:
    try:
        return datetime.fromtimestamp(int(val), tz=UTC).strftime('%Y-%m-%d')
    except (UndefinedError, ValueError):
        pass
    return ''


def safe(val: str) -> str:
    try:
        return val
    except UndefinedError:
        pass
    return ''


def is_defined(val: str) -> bool:
    try:
        return True
    except UndefinedError:
        pass
    return False


def run_tui(log_level: int, tickers: set[str], details_path: str) -> int:
    """
    Main TUI entry point
    """
    global log
    log = setup_logging(__name__, log_level)
    log.info('Logger: %s', log)
    # log.info('Details Template: %s', details)

    try:
        template_path = Path(details_path)
        env = Environment(
            autoescape=True, loader=FileSystemLoader(str(template_path.parent))
        )
        # define custom global functions for use in the template
        log.debug('Environment: %s', env)
        log.debug('Environment.globals: %s', env.globals)
        env.globals['format_num'] = format_num
        env.globals['format_date'] = format_date
        env.globals['is_defined'] = is_defined
        env.globals['safe'] = safe
        details_template = env.get_template(template_path.name)
        app = TheApp(tickers, details_template)
        app.run()
        return 0

    except TemplateSyntaxError as err:
        eprint(f"ERROR: syntax error in '{details_path}'")
        eprint(err)

    return 1
