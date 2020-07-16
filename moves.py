import csv
from pathlib import Path

MOVES_PER_POKEMON = 4

data_folder = Path("D:/Luke/Documents/Programming/Python/Pokemon_Battle_Simulator/CSV/")
file_moves_csv = data_folder / "pokemon_moves.csv"


with open(file_moves_csv) as pokemon_moves:
    csv_reader = csv.reader(pokemon_moves, delimiter=',')
    MOVE_TOTAL = len(list(csv_reader)) - 2


class Move:
    def __init__(self, name, effect, move_type, kind, power, accuracy, pp):
        self.name = name
        self.effect = effect
        self.move_type = move_type
        self.kind = kind
        self.power = power
        self.accuracy = accuracy
        self.pp = pp

    def print_move(self):
        print(f'{self.name} (BP: {self.power}, Accuracy: {self.accuracy})'
              f'\nType: {self.move_type}\tKind: {self.kind}'
              f'\nDescription: {self.effect}')


def pick_moves():
    moves = []
    with open(file_moves_csv) as pokemon_moves_list:
        movelist = csv.reader(pokemon_moves_list, delimiter=',')
        print_movelist()

        # User input selecting 4 moves from the total amount of moves
        inputted_move_numbers = []
        for x in range(MOVES_PER_POKEMON):
            inputted_move_numbers.append(move_input_parser(MOVE_TOTAL))

        # Creation of move objects
        next(movelist)  # Skip first line
        for row in movelist:
            for move_no in inputted_move_numbers:
                if int(row[0]) == move_no:
                    moves.append(Move(row[1], row[2], row[3],
                                      row[4], row[5], row[6],
                                      row[7]))
    return moves


def print_movelist():
    with open(file_moves_csv) as movelist_csv:
        movelist = csv.reader(movelist_csv, delimiter=',')
        for row in movelist:
            print(f'#{row[0]}\t{row[1]}')


# Returns an accurate number for processing Pokémon Moves
def move_input_parser(move_amount):
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
