import csv
import math
import moves
import utilities
from pathlib import Path

# Module Constant Data
TEST_LEVEL = 100
STAT_AMOUNT = 6
IV_MAX = 31
IV_MAX_TOTAL = IV_MAX * 6
EV_MAX = 255
EV_MAX_TOTAL = EV_MAX * 2

# File Processing
data_folder = Path(
    "D:/Luke/Documents/Programming/Python/Pokemon_Battle_Simulator/CSV/")
file_pokemon_list = data_folder / "pokemon_list.csv"
file_pokemon_lore = data_folder / "pokemon_lore.csv"
file_pokemon_natures = data_folder / "pokemon_natures.csv"
file_effectiveness = data_folder / "pokemon_type_effectiveness.csv"


class Pokemon:
    # TODO: class-level docstring
    def __init__(
            self, pokedex, name, level, types,
            base_stats, pokemon_moves, nature, ivs, evs, gender):
        """Constructor for the Pokémon class. Included within is every
        characteristic that a Pokémon possesses.

        Args:
            pokedex (int): The Pokémon's Pokédex number.
            name (str): The Pokémon's name.
            level (int): The Pokémon's level.
            types (list[str]): The Pokémon's type (or types), max. 2 types.
            base_stats (list[int]): The Pokémon's standard, basic statistics.
            pokemon_moves (list[moves.Move]): The Pokémon's moves.
            nature (str): The Pokémon's nature (boosts/weakens specific stats).
            ivs (list[int]): The Pokémon's "Individual Values" (genetic stats).
            evs (list[int]): The Pokémon's "Effort Values" (trained stats).

        Attributes:
            pokedex (int): The Pokémon's Pokédex number.
            name (str): The Pokémon's name.
            level (int): The Pokémon's level.
            types (list[str]): The Pokémon's type (or types), max. 2 types.
            type_effect (list[float]): Type effectiveness against this Pokémon.
            base_stats (list[int]): The Pokémon's standard, basic statistics.
            pokemon_moves (list[moves.Move]): The Pokémon's moves.
            nature (str): The Pokémon's nature (boosts/weakens specific stats).
            ivs (list[int]): The Pokémon's "Individual Values" (genetic stats).
            evs (list[int]): The Pokémon's "Effort Values" (trained stats).
            hp (int): Pokémon's Health Points including IVs and EVs.
            attack (int): Pokémon's Attack Points incl. nature/IVs/EVs.
            defense (int): Pokémon's Defense Points incl. nature/IVs/EVs.
            spatk (int): Pokémon's Special Attack Points incl. nature/IVs/EVs.
            spdef (int): Pokémon's Special Defense Points incl. nature/IVs/EVs.
            speed (int): Pokémon's Speed Points incl. nature/IVs/EVs.
            # item (?): The Pokémon's held item, which may effect stats etc.
            # abiliity (?): The Pokémon's ability, which may effect stats etc.
            # gender (?): The Pokémon's gender, either Male/Female/Genderless.
            # non_vol_status (?): Status such as Burn and Freeze.
            # vol_status (?): Status such as Infatuation and Confusion.
            # vol_btl_status (?): Battle status such as Follow Me.

        """
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

        # TODO: Future battle additions -- create objects/CSVs for these
        self.item = "token item"
        self.ability = "token ability"

        # Battle statuses and related variables
        self.gender = gender
        self.non_vol_status = "nan/BRN/FRZ/PAR/PSN/BPSN/SLP"
        self.vol_status = "bound/curse/infatuation...etc."
        self.vol_btl_status = "aqua ring/move charge/follow me"

    def determine_stats(self):
        """
        Using Base Stats, Nature, EVs & IVs, use formulae to find the
        final calculated stats for this Pokémon.
        """
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

    def calculate_effectiveness(self):
        """
        Return dictionary of effectiveness of each move type
        against this Pokémon.
        """
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
                    type_dict[row[0]] = float(
                        float(row[type_idx[0]]) * float(row[type_idx[1]]))
                else:
                    type_dict[row[0]] = float(
                        row[type_idx[0]])
            return type_dict

    def print_pokemon(self):
        """Pretty print Pokémon's information and statistics."""
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
            print(f'{self.types[0]}/{self.types[1]} '
                  f'Pokémon with {self.ability} Ability')
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
        """Print this Pokémon's moves."""
        # TODO: include power etc.
        print(
            f'{self.moves[0].name}\t{self.moves[1].name}'
            f'\n{self.moves[2].name}\t{self.moves[3].name}\t')


def pick_pokemon():
    """
    User inputs a Pokémon name, and selects its moves, nature, IVs and EVs.

    Returns:
         Pokemon (pokemon.Pokemon): Selected Pokémon with inputted statistics.
    """
    with open(file_pokemon_list) as pokemon_csv:
        csv_reader = csv.reader(pokemon_csv, delimiter=',')
        pokemon_choice = input("Type a Pokémon's name:")  # TODO: str-check
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
                gender = define_gender(int(row[0]), row[1])
                return Pokemon(
                    int(row[0]), row[1], TEST_LEVEL,
                    typing, base_stats, selected_moves,
                    nature, ivs, evs, gender)
        print(f'{pokemon_choice} could not be found. Try again.')
        pick_pokemon()


def pick_stats():
    """Calls functions to select and describe a Pokémon's nature, IVs & EVs."""
    print_all_natures()
    print(utilities.csv_extractor(
        file_pokemon_lore, "title", "nature_values", "description"))
    selected_nature = pick_nature_parser()

    # IVs and EVs
    print(utilities.csv_extractor(
        file_pokemon_lore, "title", "individual_values", "description"))
    print(utilities.csv_extractor(
        file_pokemon_lore, "title", "effort_values", "description"))
    selected_ivs, selected_evs = (
        pokemon_value_input("iv"), pokemon_value_input("ev"))
    return selected_nature, selected_ivs, selected_evs


def print_nature(nature):
    """Pretty prints the nature's boosted and weakened statistics."""
    with open(file_pokemon_natures) as natures_csv:
        natures_reader = csv.reader(natures_csv, delimiter=',')
        for row in natures_reader:
            if row[0] == nature:
                print(f"{nature} (+{row[1].strip()}, -{row[2].strip()})")
                return
        print("You've inputted an incorrect nature. Try again.")


def print_all_natures():
    """Prints all the natures, including their boosted and weakened stats."""
    with open(file_pokemon_natures) as natures_csv:
        csv_reader = csv.reader(natures_csv, delimiter=',')
        for row in csv_reader:
            print(f'{row[0]} (+{row[1]}, -{row[2]}')


def pick_nature_parser():
    """
    Parser to whether an inputted nature is found within the list.

    Returns:
        nature_input (str): Returns a nature, which has been deemed acceptable.

    """
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
    """
    Gives to each Pokémon statistic an integer corresponding to the common
    ordering of Pokémon statistics (HP/PhysAtk&Def/SpecialAtk&Def/Speed).
    This function in particular returns the integer value, according to a
    dictionary, of the boosted stat and the weakened stat according to the
    nature.

    Args:
        nature (str): The nature to be defined numerically by the function.

    Returns:
        pro (int): The integer value, in the dictionary, of the boosted stat.
        con (int): The integer value, in the dictionary, of the weakened stat.

    """
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


def define_gender(pokedex_number, pokemon_name):
    """Function which checks whether the Pokémon has a specified gender:
    if not, the user will select one.

    Args:
        pokedex_number (int): The Pokémon's number.
        pokemon_name (str): The Pokémon's name, as some Pokémon, such as
            Indeedee, have two separate gendered forms under the same Pokédex.

    Returns:
        gender_choice (str): The selected gender, whether pre-defined or
            user-inputted.
    """
    gender_options = ["Male", "Female", "Genderless"]
    with open(file_pokemon_list) as gender_list:
        gender_reader = csv.reader(gender_list, delimiter=",")
        next(gender_reader)  # Skip header line
        for row in gender_reader:
            if int(row[0]) == pokedex_number and row[1] == pokemon_name:
                if row[12] == "Undefined":
                    # If Pokémon's gender is not pre-set, then select one
                    while True:
                        gender_choice = input(
                            "Please input 'Male', 'Female' or 'Genderless'"
                        )
                        if gender_choice not in gender_options:
                            print(
                                "That gender is not yet in the Pokémon world, "
                                "please try again."
                            )
                        else:
                            return gender_choice
                else:
                    return row[12]


def pokemon_value_input(value_type):
    """
    Method for inputting the desired IVs and EVs, including error checking
    for format and amount and conversion to integer list.

    Args:
        value_type (str): Input of either "IV" or "EV", depending on value.

    Returns:
        delimited_values (list[int]): Integer list of desired values.
    """
    value_type = value_type.upper()
    print(f"All {value_type} values should be inputted in this format:"
          "\nHP/Attack/Defense/Special Attack/Special Defense/Speed.")

    if check_if_iv_or_ev(value_type):
        while True:
            # Input values
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
                print("You have inputted an incorrect amount of IVs.")
    else:
        print("Please input either 'IV' or 'EV' into function.")
        return None


def pokemon_value_parser(value_type, value_list):
    """Parser for Pokémon IVs and EVs, which verifies they are within the
    correct bounds, and informs the user of their mistake otherwise.

    Args:
        value_type (str): Whether it's an IV or EV being parsed.
        value_list (list[int]): The list of IVs or EVs.

    Returns:
        bool: True if within bounds, False if not.
    """
    # Find appropriate max value amounts
    value_max, value_total_max, running_total = 0, 0, 0
    value_type = value_type.upper()
    if check_if_iv_or_ev(value_type):
        if value_type == "IV":
            value_max = IV_MAX
            value_total_max = IV_MAX_TOTAL
        elif value_type == "EV":
            value_max = EV_MAX
            value_total_max = EV_MAX_TOTAL
    else:
        print("You haven't entered an appropriate value type (IV or EV).")
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
            print(f'One of your {value_type}s is outside '
                  f'the appropriate range of 0-{value_max}. Try again.')
            return False
    return True


def check_if_iv_or_ev(value):
    """Simple function to verify whether the values are EVs or IVs.

        Args:
            value (str): str to verify.

        Returns:
            bool: whether it says EV or IV (True) or not (False).
        """
    value = value.upper()
    pokemon_value_types = ["IV", "EV"]
    if value in pokemon_value_types:
        return True
    return False
