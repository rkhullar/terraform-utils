from ...utils import write_common_values, mock_input_output
from ...command_line import build_parser, main
from parameterized import parameterized
from nose.tools import assert_equal
from ...core import setup_project
from unittest import TestCase
from pathlib import Path
from typing import List
import tempfile
import sys
import os


class ParserTest(TestCase):

    def test_canary(self):
        assert_equal(1, 1)

    def test_parser(self):
        parser = build_parser()
        namespace = parser.parse_args(['--component', 'bucket'])
        assert_equal('bucket', namespace.component)


class MainTest(TestCase):

    def test_canary(self):
        assert_equal(1, 1)

    @parameterized.expand([
        ('stg', 'network', [], ''),
        ('stg', 'network', ['-c', 'bucket'], 'example-terraformstate-stg-company'),
        ('stg', 'network', ['-c', 'object'], 'network/terraform.tfstate'),
        ('stg', 'network', ['-c', 'table'], 'example-terraformlock-stg-company'),
        ('stg', 'network', ['-k', 'region'], 'us-east-1'),
        ('stg', 'network', ['-k', 'app_name'], 'example'),
        ('stg', 'network', ['-c', 'env'], 'stg'),
        ('stg', 'network', ['-k', 'owner'], 'noreply@example.com'),
    ])
    def test_main(self, app_env: str, construct: str, args: List[str], expected: str):
        with tempfile.TemporaryDirectory() as temp_dir, mock_input_output() as mocked:
            live_dir = Path(temp_dir) / 'live'
            setup_project(path=live_dir, constructs=[construct], envs=[app_env])
            write_common_values(live_dir / 'common.tfvars')
            os.chdir(live_dir / app_env / construct)
            sys.argv[1:] = args
            main()
        assert_equal(expected, mocked.stdout.read())
