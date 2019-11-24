from contextlib import contextmanager
from typing import NamedTuple
from io import StringIO
import sys


class MockedIO(NamedTuple):
    stdin: StringIO
    stdout: StringIO
    stderr: StringIO

    def seek(self):
        self.stdout.seek(0)
        self.stderr.seek(0)


@contextmanager
def mock_input_output():
    real = MockedIO(sys.stdin, sys.stdout, sys.stderr)
    fake = MockedIO(StringIO(), StringIO(), StringIO())
    sys.stdin, sys.stdout, sys.stderr = fake
    yield fake
    sys.stdin, sys.stdout, sys.stderr = real
    fake.seek()
