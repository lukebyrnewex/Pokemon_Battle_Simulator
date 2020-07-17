import csv
import math
import moves
import utilities
from pathlib import Path

TEST_LEVEL = 100
STAT_AMOUNT = 6
IV_MAX = 31
IV_MAX_TOTAL = IV_MAX * 6
EV_MAX = 255
EV_MAX_TOTAL = EV_MAX * 2

data_folder = Path("D:/Luke/Documents/Programming/Python/Pokemon_Battle_Simulator/CSV/")
file_pokemon_list = data_folder / "pokemon_list.csv"
file_pokemon_lore = data_folder / "pokemon_lore.csv"
file_pokemon_natures = data_folder / "pokemon_natures.csv"
file_effectiveness = data_folder / "pokemon_type_effectiveness.csv"


# The actual Pokémon and their stats
class Pokemon:
    def __init__(
            self, pokedex, name, level, types,
            base_stats, pokemon_moves, nature, ivs, evs):
        # Basic Information
        self.pokedex = pokedex
        self.name = name
        self.level = level

        # Typing
        self.types = types
        self.type_effect = self.calculate_effectiveness()

        # Base stats
        self.base_stats = base_stats

        # Known Moves (<=4)
        self.moves = pokemon_moves

        # Complex values to Pokémon
        self.nature = nature
        self.ivs = ivs
        self.evs = evs

        # Determined stats = Base stats + IV/EV/Nature/Level etc.
        determined_stats = self.determine_stats()
        self.hp = determined_stats[0]
        self.attack = determined_stats[1]
        self.defense = determined_stats[2]
        self.spatk = determined_stats[3]
        self.spdef = determined_stats[4]
        self.speed = determined_stats[5]

        # TODO: Future additions to the Pokémon (for Battle) - create objects for these
        self.ability = "token ability"
        self.item = "token item"
        self.gender = "token gender"

    def determine_stats(self):
        determined_stats = []
        pro, con = define_nature(self.nature)

        for i in range(STAT_AMOUNT):
            common_formula = (
                math.floor(
                    ((((2 * self.base_stats[i]) + self.ivs[i])
                      + math.floor(self.evs[i] / 4)) * self.level) / 100))
            if i == 0:  # HP
                determined_stats.append(common_formula + self.level + 10)
            elif i == pro:
                determined_stats.append(math.floor((common_formula + 5) * 1.1))
            elif i == con:
                determined_stats.append(math.floor((common_formula + 5) * 0.9))
            else:
                determined_stats.append(math.floor((common_formula + 5) * 1.0))
        return determined_stats

    # Return dictionary of effectiveness of moves against this Pokémon
    def calculate_effectiveness(self):
        type_dict = {}
        type_idx = []
        with open(file_effectiveness) as effect_chart:
            effect_reader = csv.reader(effect_chart, delimiter=",")
            pkmn_type_row = next(effect_reader)
            for idx, column in enumerate(pkmn_type_row):
                if column in self.types:
                    type_idx.append(idx)
            for row in effect_reader:
                if len(type_idx) > 1:
                    type_dict[row[0]] = float(float(row[type_idx[0]]) * float(row[type_idx[1]]))
                else:
                    type_dict[row[0]] = float(row[type_idx[0]])
            return type_dict


    def print_pokemon(self):
        pokedex_no = int(self.pokedex)
        if pokedex_no < 10:
            pokedex_str = f'#00{self.pokedex}'
        elif pokedex_no < 100:
            pokedex_str = f'#0{self.pokedex}'
        else:
            pokedex_str = f'#{self.pokedex}'
        print(f'{pokedex_str} {self.name} @ {self.item}')
        if len(self.types[1]) < 1:
            print(f'{self.types[0]} Pokémon with {self.ability} Ability')
        else:
            print(f'{self.types[0]}/{self.types[1]} Pokémon with {self.ability} Ability')
        print(f'Level: {self.level}')
        print(
            f'EVs: {self.evs[0]} HP / {self.evs[1]} Atk / '
            f'{self.evs[2]} Def / {self.evs[3]} SpA / '
            f'{self.evs[4]} SpD / {self.evs[5]} Spe')
        print(f'{self.nature.capitalize()} Nature')
        print(
            f'IVs: {self.ivs[0]} HP / {self.ivs[1]} Atk / {self.ivs[2]} Def /'
            f'{self.ivs[3]} SpA / {self.ivs[4]} SpD / {self.ivs[5]} Spe')
        for move in self.moves:
            print(
                f'—{move.name} ({move.move_type}, '
                f'Power: {move.power} @ {move.accuracy})')

    def show_moves(self):
        print(
            f'{self.moves[0].name}\t{self.moves[1].name}'
            f'\n{self.moves[2]}\t{self.moves[3]}\t')


def pick_pokemon():
    with open(file_pokemon_list) as pokemon_csv:
        csv_reader = csv.reader(pokemon_csv, delimiter=',')
        pokemon_choice = input("Type a Pokémon's name:")
        for row in csv_reader:
            if pokemon_choice == row[1]:
                typing = [row[2], row[3]]
                base_stats = [
                    row[4], row[5], row[6],  # HP, Attack, Defense
                    row[7], row[8], row[9],  # SpAtk, SpDef, Speed
                    row[10]]  # Base Stat Total
                base_stats = utilities.str_list_to_int(base_stats)
                selected_moves = moves.pick_moves()
                nature, ivs, evs = pick_stats()
                return Pokemon(
                    int(row[0]), row[1], TEST_LEVEL,
                    typing, base_stats, selected_moves,
                    nature, ivs, evs)
        print(f'{pokemon_choice} could not be found. Try again.')
        pick_pokemon()


def pick_stats():
    # Nature
    print_all_natures()
    print(
        f'Firstly, we much select a nature.'
        f'\n{utilities.csv_extractor(file_pokemon_lore, "title", "description", "nature_values")}')
    selected_nature = pick_nature_parser()

    # IVs and EVs
    print(utilities.csv_extractor(file_pokemon_lore, "title", "description", "individual_values"))

    print(utilities.csv_extractor(file_pokemon_lore, "title", "description", "effort_values"))
    selected_ivs, selected_evs = pokemon_value_input("iv"), pokemon_value_input("ev")

    return selected_nature, selected_ivs, selected_evs


def print_nature(nature):
    with open(file_pokemon_natures) as natures_csv:
        natures_reader = csv.reader(natures_csv, delimiter=',')
        for row in natures_reader:
            if row[0] == nature:
                print(f"{nature} (+{row[1].strip()}, -{row[2].strip()})")
                return
        print("You've inputted an incorrect nature. Try again.")


def print_all_natures():
    with open(file_pokemon_natures) as natures_csv:
        csv_reader = csv.reader(natures_csv, delimiter=',')
        for row in csv_reader:
            print(f'{row[0]} (+{row[1]}, -{row[2]}')


def pick_nature_parser():
    # Documenting accepted natures
    accepted_natures = []
    with open(file_pokemon_natures) as natures_csv:
        natures_reader = csv.reader(natures_csv, delimiter=',')
        next(natures_reader)  # Skip first line
        for row in natures_reader:
            accepted_natures.append(row[0])

    while True:
        try:
            nature_input = input("Choose a nature from the list:")
            if nature_input not in accepted_natures:
                print(f'Please choose an accepted nature.')
            else:
                return nature_input
        except ValueError:
            print("That's not a correct nature! Try again.")


def define_nature(nature):
    nature_dict = {
        "Attack": 1,
        "Defense": 2,
        "SpAttack": 3,
        "SpDefense": 4,
        "Speed": 5
    }

    with open(file_pokemon_natures) as pokemon_natures:
        natures_reader = csv.reader(pokemon_natures, delimiter=",")
        for row in natures_reader:
            if row[0].strip() == nature:
                pro = nature_dict[row[1].strip()]
                con = nature_dict[row[2].strip()]
        return pro, con


def pokemon_value_input(value_type):
    value_type = value_type.upper()
    print(f"All {value_type} values should be inputted in the order and format:"
          "\nHP/Attack/Defense/Special Attack/Special Defense/Speed.")

    if utilities.check_value_type(value_type):
        while True:
            # Input EVs
            inputted_values = input("Please select your 6 values:")
            delimited_values = inputted_values.split("/")
            print(len(delimited_values))

            # Check amount of values and convert to ints
            if len(delimited_values) == STAT_AMOUNT:
                delimited_values = utilities.str_list_to_int(delimited_values)

                # Check that they're within the correct range
                if pokemon_value_parser(value_type, delimited_values):
                    return delimited_values
            else:
                print("You have inputted an incorrect amount of IVs. Try again.")
    else:
        print("Please input either 'IV' or 'EV' into function.")
        return None


# Returns True if all values are within their appropriate boundaries, False if not (with explanation)
def pokemon_value_parser(value_type, value_list):
    # Find appropriate max value amounts
    running_total = 0
    value_type = value_type.upper()
    if utilities.check_value_type(value_type):
        if value_type == "IV":
            value_max = IV_MAX
            value_total_max = IV_MAX_TOTAL
        elif value_type == "EV":
            value_max = EV_MAX
            value_total_max = EV_MAX_TOTAL
    else:
        print("You haven't entered an appropriate value type (IV or EV). Try again.")
        return False

    # Check they're within appropriate boundaries
    for i in range(STAT_AMOUNT):
        if 0 <= value_list[i] <= value_max:
            running_total += value_list[i]
            if running_total > value_total_max:
                print(f'You have too many {value_type}s. Try again.')
                return False
            pass
        else:
            print(f'One of your {value_type}s is outside the appropriate range of 0-{value_max}. Try again.')
            return False
    return True
