import subprocess
import time
import unittest
from pathlib import Path

from pytickrs import __version__, setup_logging

#from .process_session import ProcessSession

log = setup_logging(__name__)


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
    stdout_value = ''
    stderr_value = ''
    try:
        stdout_value, stderr_value = popen.communicate(input=stdin_value)
    except Exception as err:
        log.info(f'Caught while tying to communicate with {popen.pid}: {err}')

    if popen.returncode is None:
        # now wait for the process to complete
        try:
            log.info(f'Waiting for upto {timeout} secs for {popen.pid}...')
            start = time.time()
            popen.wait(timeout)
            # the process has terminated
            elapsed = time.time() - start
            log.info(
                f'{popen.pid} terminated after {elapsed:.3f} secs, ec: {popen.returncode}'
            )

        except subprocess.TimeoutExpired:
            elapsed = time.time() - start
            log.info(f'Waiting for {popen.pid} timed out after {elapsed} secs')
            return -1, '', ''

    return popen.returncode, stdout_value, stderr_value


class TestCLI(unittest.TestCase):
    """
    Verify simultons CLI
    """

    def test_version(self) -> None:
        ec, out, _ = run_cli(args=['--version'])
        self.assertEqual(ec, 0)
        # print('out', out)
        # print('err', err)
        self.assertEqual(out.strip(), __version__)
        return
