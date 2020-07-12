import unittest

from utilities import str_list_to_int


class TestStrListToInt(unittest.TestCase):
    def test_conversion(self):
        # Test whether correct list inputs produces correct output
        self.assertEqual(str_list_to_int(["1", "5", "20", "50"]), [1, 5, 20, 50])
        self.assertEqual(str_list_to_int(["-1", "-5", "-20", "-50"]), [-1, -5, -20, -50])
        self.assertEqual(str_list_to_int(["1"]), [1])
        self.assertEqual(str_list_to_int("1"), [1])


if __name__ == '__main__':
    unittest.main()
