from nose.tools import assert_equal, assert_is_not_none
from parameterized import parameterized
from ...core import setup_project
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
        ('ABC_def', '012xyz_JK', 'ABC_def = 012xyz_JK'),
    ])
    def test_variable(self, key, val, expression):
        pattern = Variable.build_pattern()
        match_object = pattern.match(expression)
        assert_is_not_none(match_object)
        assert_equal(dict(key=key, val=val), match_object.groupdict())

    def test_variable_list(self):
        data = {'x': '1', 'y': '2'}
        expected = {Variable('x', '1'), Variable('y', '2')}
        actual = set(Variable.from_dict(data))
        assert_equal(expected, actual)

    def test_find_target(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            live_dir = Path(temp_dir) / 'live'
            setup_project(live_dir)
            result = find_target(name='common.tfvars', start_dir=live_dir / 'sbx' / 'network', root_dir=Path(temp_dir))
            assert_equal(live_dir / 'common.tfvars', result)

    def test_load_config(self):
        target = Path(__file__).parents[2] / 'data' / 'common.tfvars'
        assert_equal(build_default_common_values(), load_config(target))

    def test_write_common_values(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / 'common.tfvars'
            values = build_default_common_values()
            write_common_values(target, values)
            config = load_config(target)
            assert_equal(config, values)
