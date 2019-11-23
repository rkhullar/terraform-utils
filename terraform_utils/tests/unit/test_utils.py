from nose.tools import assert_equal, assert_is_not_none
from parameterized import parameterized
from unittest import TestCase
from pathlib import Path
from ...utils import *
import tempfile


class UtilsTest(TestCase):

    def test_canary(self):
        assert_equal(1, 1)

    def test_read_hello_txt(self):
        assert_equal(read_hello_txt(), 'hello world')

    @parameterized.expand([
        ('x', '1', 'x = 1'),
        ('x', '1', '"x" = "1"'),
        ('x', '1', '  x=1   '),
        ('x', '1', '  x   =    "1"   '),
        ('email', 'noreply@example.com', 'email = noreply@example.com'),
        ('message', 'hello_world', 'message = hello_world'),
        # ('message', 'hello world', 'message = "hello world"'),
    ])
    def test_variable(self, key, val, expression):
        pattern = Variable.build_pattern()
        match_object = pattern.match(expression)
        assert_is_not_none(match_object)
        assert_equal(dict(key=key, val=val), match_object.groupdict())

    def test_find_target(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root_dir = Path(temp_dir)
            start_dir = root_dir / 'live' / 'sbx' / 'network'
            start_dir.mkdir(exist_ok=True, parents=True)
            target = 'common.tfvars'
            target_path = root_dir / 'live' / target
            target_path.touch(exist_ok=True)
            result = find_target(name=target, start_dir=start_dir, root_dir=root_dir)
            assert_equal(target_path, result)
