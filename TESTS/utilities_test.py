import unittest
from pathlib import Path
from utilities import str_list_to_int, csv_extractor

# File Processing
data_folder = Path(
    "D:/Luke/Documents/Programming/Python/Pokemon_Battle_Simulator/CSV/")
file_pokemon_csv = data_folder / "pokemon_list.csv"


class TestUtilities(unittest.TestCase):
    def test_str_list_to_int(self):
        """Tests to see whether conversion occurs correctly."""
        self.assertEqual(str_list_to_int(
            ["1", "5", "20", "50"]), [1, 5, 20, 50])
        self.assertEqual(str_list_to_int(
            ["-1", "-5", "-20", "-50"]), [-1, -5, -20, -50])
        self.assertEqual(str_list_to_int(
            ["1"]), [1])
        self.assertEqual(str_list_to_int(
            "1"), [1])

    def test_csv_extractor(self):
        """Tests to see whether correct information is extracted."""
        self.assertEqual(csv_extractor(
            file_pokemon_csv, "Name", "Misdreavus", "Generation"), 2)
        self.assertEqual(csv_extractor(
            file_pokemon_csv, "Name", "Scizor", "Attack"), 130)


if __name__ == '__main__':
    unittest.main()
