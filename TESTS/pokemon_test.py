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
            [74, 190, 91, 48, 84, 23])
        self.assertEqual(garchomp.hp, 289)
        self.assertEqual(garchomp.attack, 278)
        self.assertEqual(garchomp.defense, 193)
        self.assertEqual(garchomp.spatk, 135)
        self.assertEqual(garchomp.spdef, 171)
        self.assertEqual(garchomp.speed, 171)


if __name__ == '__main__':
    unittest.main()
