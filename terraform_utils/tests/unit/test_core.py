from nose.tools import assert_equal
from unittest import TestCase


class CoreTest(TestCase):

    def test_canary(self):
        assert_equal(1, 1)
