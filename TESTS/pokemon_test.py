import unittest
from unittest import mock
from pokemon import Pokemon
from moves import Move

pound = Move(
    "Pound", "Deals damage with no additional effect.", "Normal", "Physical",
    40, 100, 35
)
leer = Move(
    "Leer", "Lowers the target's Defense by 1 stage.", "Normal", "Status",
    0, 100, 30
)
sing = Move(
    "Sing", "Puts the target to sleep.", "Normal", "Status",
    0, 55, 15
)
supersonic = Move(
    "Supersonic", "Confuses the target.", "Normal", "Status",
    0, 55, 20
)
example_moves = [pound, leer, sing, supersonic]


class TestDetermineStats(unittest.TestCase):
    def test_each_stat_correctly_divided(self):
        # Example Pokémon (from bulbapedia.bulbagarden.net/wiki/Statistic)
        garchomp = Pokemon(
            "Garchomp", "Male", 78, example_moves, "Adamant",
            [24, 12, 30, 16, 23, 5],
            [74, 190, 91, 48, 84, 23]
        )
        self.assertEqual(garchomp.hp, 289)
        self.assertEqual(garchomp.attack, 278)
        self.assertEqual(garchomp.defense, 193)
        self.assertEqual(garchomp.spatk, 135)
        self.assertEqual(garchomp.spdef, 171)
        self.assertEqual(garchomp.speed, 171)


class TestCalculateEffectiveness(unittest.TestCase):
    def test_correct_eff_dict_creation(self):
        # Example Pokémon Litleo (Fire/Normal) and Misdreavus (Ghost)
        litleo = Pokemon(
            "Litleo", "Female", 100, example_moves, "Adamant",
            [31, 31, 31, 31, 31, 31],
            [252, 0, 0, 252, 0, 4]
        )
        misdreavus = Pokemon(
            "Misdreavus", "Female", 100, example_moves, "Adamant",
            [31, 31, 31, 31, 31, 31],
            [252, 0, 0, 252, 0, 4]
        )

        # Example Pokémon correct type effectiveness dictionaries
        litleo_effectiveness = {
            "Normal": 1, "Fire": 0.5, "Water": 2, "Electric": 1,
            "Grass": 0.5, "Ice": 0.5, "Fighting": 2, "Poison": 1,
            "Ground": 2, "Flying": 1, "Psychic": 1, "Bug": 0.5,
            "Rock": 2, "Ghost": 0, "Dragon": 1, "Dark": 1,
            "Steel": 0.5, "Fairy": 0.5
        }
        misdreavus_effectiveness = {
            "Normal": 0, "Fire": 1, "Water": 1, "Electric": 1,
            "Grass": 1, "Ice": 1, "Fighting": 0, "Poison": 0.5,
            "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 0.5,
            "Rock": 1, "Ghost": 2, "Dragon": 1, "Dark": 2,
            "Steel": 1, "Fairy": 1
        }

        self.assertDictEqual(litleo.type_effect, litleo_effectiveness)
        self.assertDictEqual(misdreavus.type_effect, misdreavus_effectiveness)


if __name__ == '__main__':
    unittest.main()
