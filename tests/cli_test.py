import subprocess
import tempfile
import unittest
from pathlib import Path

from pytickrs import __version__, setup_logging
from pytickrs.__main__ import comma_separated_list
from pytickrs.tickers import analyze_ticker, load_tickers

log = setup_logging(__name__)


class TestTicker:
    def __init__(self, info: dict[str, object]) -> None:
        self.info = info


def run_cli(
    args: list[str] = [], timeout: float = 10.0, cmds: list[str] = []
) -> tuple[int, str, str]:
    """
    Returns tuple: ec, stdout_str, stderr_str
    """
    command_line = ['.venv/bin/python3', '-m', 'pytickrs', *args]
    parent_dir = Path(__file__).absolute().parents[1]
    popen = subprocess.Popen(
        command_line,
        cwd=parent_dir,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert popen is not None
    # retrieve stdout and stderr
    stdin_value = '\n'.join(cmds)
    try:
        # Apply the timeout while exchanging data so a hung CLI cannot block the test.
        stdout_value, stderr_value = popen.communicate(
            input=stdin_value, timeout=timeout
        )
    except subprocess.TimeoutExpired:
        log.info('CLI process %s timed out after %.3f secs', popen.pid, timeout)
        # Kill and reap the child to close its pipes and avoid leaving a stray process.
        popen.kill()
        popen.communicate()
        return -1, '', ''

    return popen.returncode, stdout_value, stderr_value


class TestCLI(unittest.TestCase):
    """
    Verify CLI
    """

    def test_version(self) -> None:
        ec, out, _ = run_cli(args=['--version'])
        self.assertEqual(ec, 0)
        # print('out', out)
        # print('err', err)
        self.assertEqual(out.strip(), __version__)
        return

    def test_help(self) -> None:
        ec, out, err = run_cli(args=['-h'])
        self.assertEqual(ec, 0)
        self.assertNotEqual(out, '')
        self.assertEqual(err, '')
        # print('out', out)
        # print('err', err)
        return

    def test_load_tickers(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            tickers_file = Path(temp_dir) / 'tickers.txt'
            tickers_file.write_text('# Watchlist\n\naapl\nMSFT\n', encoding='utf-8')
            self.assertEqual(load_tickers(str(tickers_file)), {'AAPL', 'MSFT'})

    def test_comma_separated_tickers_are_normalized(self) -> None:
        self.assertEqual(comma_separated_list(' aapl, MSFT,,aapl '), {'AAPL', 'MSFT'})

    def test_comma_separated_tickers_reject_empty_input(self) -> None:
        ec, _, err = run_cli(args=['--tickers= , '])
        self.assertEqual(ec, 2)
        self.assertIn('At least one ticker symbol is required.', err)

    def test_analyze_ticker_with_missing_data(self) -> None:
        self.assertEqual(analyze_ticker(TestTicker({})), [])
        self.assertEqual(
            analyze_ticker(
                TestTicker({'fiftyTwoWeekLow': 100, 'fiftyTwoWeekHigh': 100})
            ),
            [],
        )

    def test_analyze_ticker_near_yearly_limits(self) -> None:
        ticker = TestTicker(
            {
                'fiftyTwoWeekLow': 100,
                'fiftyTwoWeekHigh': 200,
                'bid': 181,
                'ask': 119,
            }
        )
        self.assertEqual(
            analyze_ticker(ticker), ['sell, close to high', 'buy, close to low']
        )

    def test_single_ticker(self) -> None:
        ec, out, err = run_cli(args=['--once', '--tickers=AAPL'])
        self.assertEqual(ec, 0)
        self.assertNotEqual(out, '')
        self.assertEqual(err, '')
        # print('out', out)
        # print('err', err)
        return
