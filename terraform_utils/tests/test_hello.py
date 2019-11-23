from nose.tools import assert_equal
from unittest import TestCase
from ..utils import *


class UtilsTest(TestCase):

    def test_canary(self):
        self.assertEqual(1, 1)

    def test_read_hello_txt(self):
        assert_equal(read_hello_txt(), 'hello world')
