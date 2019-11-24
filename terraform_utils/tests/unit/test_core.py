from ...utils import build_default_common_values
from nose.tools import assert_equal, assert_true
from parameterized import parameterized
from unittest import TestCase
from pathlib import Path
from ...core import *
import tempfile


class CoreTest(TestCase):

    def test_canary(self):
        assert_equal(1, 1)

    def test_setup_project(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            live_dir = Path(temp_dir) / 'live'
            setup_project(path=live_dir, constructs=['network'], envs=['stg'])
            project_files = [
                live_dir / 'terragrunt.hcl',
                live_dir / 'common.tfvars',
                live_dir / 'stg' / 'network' / 'terragrunt.hcl'
            ]
            for path in project_files:
                assert_true(path.exists())

    def test_infer_params(self):
        expected = dict(app_env='stg', construct='network')
        with tempfile.TemporaryDirectory() as temp_dir:
            live_dir = Path(temp_dir) / 'live'
            setup_project(path=live_dir, constructs=['network'], envs=['stg'])
            actual = infer_params(project_dir=live_dir, work_dir=live_dir / 'stg' / 'network',
                                  app_env_var='app_env', construct_var='construct', app_env_pos=0)
            assert_equal(expected, actual)

    def test_build_output_for_key(self):
        common_values = build_default_common_values()
        inferred_params = dict(app_env='stg', construct='network')
        data = {**common_values, **inferred_params}
        for key, val in data.items():
            result = build_output(data, key=key)
            assert_equal(val, result)

    @parameterized.expand([
        ('stg', 'network', 'env', 'stg'),
        ('stg', 'network', 'bucket', 'example-terraformstate-stg-company'),
        ('stg', 'network', 'table', 'example-terraformlock-stg-company'),
        ('stg', 'network', 'object', 'network/terraform.tfstate')
    ])
    def test_build_output_for_components(self, app_env: str, construct: str, component: str, expected: str):
        common_values = build_default_common_values()
        inferred_params = dict(app_env=app_env, construct=construct)
        data = {**common_values, **inferred_params}
        actual = build_output(data, component=component)
        assert_equal(expected, actual)
