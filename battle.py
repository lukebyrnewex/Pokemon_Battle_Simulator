import moves
import pokemon


class Battle:
    def __init__(self, pokemon1, pokemon2):
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2

    def battling_pokemon(self):
        print(f'{self.pokemon1.name} and {self.pokemon2.name} are battling!')


# Select a move to use in battle (returns number of move)
def move_select(pkmn):
    print(len(pkmn.moves))
    move_number = 0
    for move in pkmn.moves:
        move_number += 1
        print(f'{move_number}. {move.name}')
    selection = moves.move_input_parser(len(pkmn.moves))
    return selection


# Initialise a battle sequence by selecting Pokémon
def create_battle():
    pokemon1 = pokemon.pick_pokemon()
    pokemon2 = pokemon.pick_pokemon()
    pokemon1.print_pokemon()
    print("\nvs.\n")
    pokemon2.print_pokemon()
    return Battle(pokemon1, pokemon2)


# (Very basic) implementation of an attack
def attack(atk_pkmn, def_pkmn):
    # Calculate the damage based on the move
    move_no = move_select(atk_pkmn)
    selected_move = atk_pkmn.moves[move_no - 1]
    if isinstance(selected_move, moves.Move):
        damage_formula_num = (
                ((((2 * atk_pkmn.level) / 5) + 2)
                 * selected_move.power)
                * (atk_pkmn.attack / def_pkmn.defense))
    modifier = 1  # TODO: this includes CRIT, STAB, super effective, etc.
    damage = ((damage_formula_num / 50) + 2) * modifier

    # Reduce the opponent's HP by damage amount
    def_pkmn.current_hp -= damage

    # Print out the resulting HP
    print(f'HP: {def_pkmn.current_hp}/{def_pkmn.hp}')
