import csv
from pathlib import Path

# File Processing
data_folder = Path(
    "D:/Luke/Documents/Programming/Python/Pokemon_Battle_Simulator/CSV/")
file_moves_csv = data_folder / "pokemon_moves.csv"

# Module Constant Data
MOVES_PER_POKEMON = 4
with open(file_moves_csv) as pokemon_moves:
    csv_reader = csv.reader(pokemon_moves, delimiter=',')
    MOVE_TOTAL = len(list(csv_reader)) - 2


class Move:
    def __init__(self, name, effect, move_type, category, power, accuracy, pp):
        """Constructor for a Pokémon move.

        Args:
            name (str): The name of the move.
            effect (str): The description of the move and its effects.
            move_type (str): The move type, such as Water or Grass.
            category (str): The move category [Physical, Special or Status].
            power (int): The move's base power, used in damage calculation.
            accuracy (int): A percentage of how often a move will hit.
            pp (int): Power points, or how many times the move can be used.

        """
        self.name = name
        self.effect = effect
        self.move_type = move_type
        self.category = category
        self.power = power
        self.accuracy = accuracy
        self.pp = pp

    def print_move(self):
        """Pretty prints the Move constructor's information."""
        print(f'{self.name} (BP: {self.power}, Accuracy: {self.accuracy})'
              f'\nType: {self.move_type}\tKind: {self.category}'
              f'\nDescription: {self.effect}')


def pick_moves():
    """Selects a Pokémon's move from the list and returns them."""
    # TODO: ensure the same move isn't selected twice
    moves = []
    with open(file_moves_csv) as pokemon_moves_list:
        movelist = csv.reader(pokemon_moves_list, delimiter=',')
        print_movelist()

        # User input selecting 4 diff. moves from the total amount of moves
        inputted_move_numbers = []
        while len(inputted_move_numbers) < MOVES_PER_POKEMON:
            parsed_move_no = move_input_parser(MOVE_TOTAL)
            if parsed_move_no not in inputted_move_numbers:
                inputted_move_numbers.append(parsed_move_no)
            else:
                print("You already have that move! Pick another.")

        # Creation of move objects
        next(movelist)  # Skip first line
        for row in movelist:
            for move_no in inputted_move_numbers:
                if int(row[0]) == move_no:
                    moves.append(Move(row[1], row[2], row[3], row[4],
                                      int(row[5]), int(row[6]), int(row[7])))
    return moves


def print_movelist():
    """Prints the number and name of every Pokémon move."""
    with open(file_moves_csv) as movelist_csv:
        movelist = csv.reader(movelist_csv, delimiter=',')
        for row in movelist:
            print(f'#{row[0]}\t{row[1]}')


def move_input_parser(move_amount):
    """Function ensures the inputted move number is within the given bounds.

    Args:
        move_amount (int): The total amount of Pokémon moves.

    Returns:
        move_number (int): The selected move's number.

    """
    while True:
        try:
            move_input = input("Choose a move number from the list:")
            move_number = int(move_input)
            if move_number < 1 or move_number > move_amount:
                print(f'Please choose a number between 1 and {move_amount}.')
            else:
                return move_number
        except ValueError:
            print("That's not a number! Try again.")
