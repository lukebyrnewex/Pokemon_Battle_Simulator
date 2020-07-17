import unittest
import pokemon


class TestPokemon(unittest.TestCase):
    def test_determine_stats(self):
        # Example Pokémon (from https://bulbapedia.bulbagarden.net/wiki/Statistic)
        garchomp = pokemon.Pokemon(
            445, "Garchomp", 78, ["Ice"],
            [108, 130, 95, 80, 85, 102, 600],
            ["Pound", "Fire Punch", "Ice Punch", "ThunderPunch"],
            "Adamant",
            [24, 12, 30, 16, 23, 5],
            [74, 190, 91, 48, 84, 23]
        )
        self.assertEqual(garchomp.hp, 289)
        self.assertEqual(garchomp.attack, 278)
        self.assertEqual(garchomp.defense, 193)
        self.assertEqual(garchomp.spatk, 135)
        self.assertEqual(garchomp.spdef, 171)
        self.assertEqual(garchomp.speed, 171)

    def test_calculate_effectiveness(self):
        # Example Pokémon Litleo (Fire/Normal) and Misdreavus (Ghost)
        litleo = pokemon.Pokemon(
            667, "Litleo", 100, ["Fire", "Normal"],
            [62, 50, 58, 73, 54, 72, 369],
            ["Pound", "Fire Punch", "Ice Punch", "ThunderPunch"],
            "Adamant",
            [31, 31, 31, 31, 31, 31],
            [252, 0, 0, 252, 0, 4]
        )
        misdreavus = pokemon.Pokemon(
            200, "Misdreavus", 100, ["Ghost"],
            [60, 60, 60, 85, 85, 85, 435],
            ["Pound", "Fire Punch", "Ice Punch", "ThunderPunch"],
            "Adamant",
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
