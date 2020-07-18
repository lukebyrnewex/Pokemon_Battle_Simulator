import unittest
import csv
from pathlib import Path
from utilities import str_list_to_int, csv_extractor

data_folder = Path(
    "D:/Luke/Documents/Programming/Python/Pokemon_Battle_Simulator/CSV/")
file_pokemon_csv = data_folder / "pokemon_list.csv"


class TestUtilities(unittest.TestCase):
    def test_str_list_to_int(self):
        # TODO: docstring
        self.assertEqual(str_list_to_int(["1", "5", "20", "50"]), [1, 5, 20, 50])
        self.assertEqual(str_list_to_int(["-1", "-5", "-20", "-50"]), [-1, -5, -20, -50])
        self.assertEqual(str_list_to_int(["1"]), [1])
        self.assertEqual(str_list_to_int("1"), [1])

    def test_csv_extractor(self):
        # TODO: docstring
        self.assertEqual(csv_extractor(
            file_pokemon_csv, "Name", "Misdreavus", "Generation"), 2)
        self.assertEqual(csv_extractor(
            file_pokemon_csv, "Name", "Scizor", "Attack"), 130)

    #def test_find_key_index(self):
        # TODO: docstring, tests


if __name__ == '__main__':
    unittest.main()
