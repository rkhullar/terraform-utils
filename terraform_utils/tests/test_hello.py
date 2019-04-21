import unittest


class TestHello(unittest.TestCase):

    def test_canary(self):
        self.assertEqual(1, 1)
