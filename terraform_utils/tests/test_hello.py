from nose.tools import assert_equal
from unittest import TestCase
from ..hello import read_data


class HelloTest(TestCase):

    def test_canary(self):
        self.assertEqual(1, 1)

    def test_read_data(self):
        assert_equal(read_data(), 'hello world')
