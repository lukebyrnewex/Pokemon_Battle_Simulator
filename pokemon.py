import csv
import math
import moves
import pandas as pd
from pathlib import Path
from utilities import pandas_series_to_int_list

# Module Constant Data
STAT_AMOUNT = 6
IV_MAX = 31
EV_MAX = 255
EV_MAX_TOTAL = EV_MAX * 2

# File Processing
data_folder = Path(
	"D:/Luke/Documents/Programming/Python/Pokemon_Battle_Simulator/CSV/"
)
file_pokemon_list = data_folder / "pokemon_list.csv"
file_pokemon_natures = data_folder / "pokemon_natures.csv"
file_effectiveness = data_folder / "pokemon_type_effectiveness.csv"
file_pokemon_moves = data_folder / "pokemon_moves.csv"

# Pokémon List database
pokemon_df = pd.read_csv(
	file_pokemon_list,
	encoding="ISO-8859-1",
	names=[
		'#', 'Name', 'Type 1', 'Type 2',
		'HP', 'Attack', 'Defense', 'Sp. Attack', 'Sp. Defense',
		'Speed', 'Total', 'Generation', 'Gender'
	],
	index_col='Name'
)

nature_df = pd.read_csv(
	file_pokemon_natures, encoding="ISO-8859-1",
	names=['Nature', 'Boosts', 'Lowers'],
	index_col='Nature'
)


class Pokemon:
	def __init__(self, name, gender, level, pokemon_moves, nature, ivs, evs):
		"""Constructor for the Pokémon class. Included within is every
		characteristic that a Pokémon possesses.

		Args:
		name (str): Pokémon's name, the most important input.
		gender (str): Either Male or Female, __init__ will verify whether
			it is ha, and check if specifically Genderless.
		level (int): The Pokémon's level, between 1 and 100.
		pokemon_moves (list[moves.Move]): The Pokémon's moves.
		nature (str): The nature of the Pokémon, found in the CSV file.
		ivs (list[int]): The Pokémon's "Individual Values" (genetic stats).
		evs (list[int]): The Pokémon's "Effort Values" (trained stats).

		Attributes:
		pokedex (int): The Pokémon's Pokédex number.
		name (str): The Pokémon's name.
		types (list[str]): The Pokémon's type (or types), max. 2 types.
		base_stats (list[int]): The Pokémon's standard, basic statistics.
		gender (str): The Pokémon's gender, either Male/Female/Genderless.
		level (int): The Pokémon's level.
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
		type_effect (list[float]): Type effectiveness against this Pokémon.

		"""
		# Find Pokémon in data frame, and create pandas Series for it from CSV
		try:
			self.info = pokemon_df.loc[name.capitalize()]
		except KeyError:
			print("Your Pokémon could not be found, and thus not initialised.")

		# Basic Pokémon information obtained within data frame
		self.pokedex = int(self.info[0])
		self.name = name.capitalize()
		self.types = [self.info[1], self.info[2]]
		self.base_stats = pandas_series_to_int_list(self.info[3:10])
		self.generation = self.info[10]
		self.gender = gender.capitalize()
		self.check_gender()

		# User-generated information for Pokémon
		self.level = level
		self.moves = pokemon_moves
		self.nature = nature.capitalize()
		self.pro_nat, self.con_nat = None, None
		self.ivs = ivs
		self.evs = evs

		# Check user-generated information for various metrics
		self.check_level()
		self.check_moves()
		self.check_nature()
		self.check_ivs()
		self.check_evs()

		# From these, we can verify derive the final stats of the Pokémon
		self.type_effect = self.calculate_effectiveness()

		final_stats = self.determine_stats()
		self.hp = final_stats[0]
		self.attack = final_stats[1]
		self.defense = final_stats[2]
		self.spatk = final_stats[3]
		self.spdef = final_stats[4]
		self.speed = final_stats[5]

		print(f'{self.name.capitalize()} has successfully initialised.')

	# GENDER #
	def get_gender(self):
		"""Getter for Pokémon's gender."""
		return self.gender

	def set_gender(self, gender):
		"""Setter for Pokémon's gender."""
		gender_options = ["Male", "Female"]
		if gender.capitalize() in gender_options:
			self.gender = gender.capitalize()
		else:
			gender_set = True
			while gender_set:
				gender_input = input("Please select either Male or Female:")
				if gender_input in gender_options:
					self.gender = gender_input
					gender_set = False

	def check_gender(self):
		"""Verification that gender is inputted correctly: rectify if not."""
		if self.info[11] != "Undefined":
			self.gender = self.info[11]
		self.set_gender(self.gender)

	# LEVEL #
	def get_level(self):
		"""Getter for Pokémon's level."""
		return self.level

	def set_level(self, level):
		"""Setter for Pokémon's level."""
		try:
			self.level = int(level)
			self.check_level()
		except ValueError:
			print("Your level was not an integer. Try again.")

	def check_level(self):
		"""Verification that level is within its correct bounds,
		rectify if not."""
		level_bool = True
		while level_bool:
			if 0 < self.level <= 100:
				level_bool = False
			else:
				level_input = input("Please input a correct level:")
				self.level = int(level_input)

	# MOVES #
	def get_moves(self):
		"""Getter for Pokémon moves (in object form)."""
		return self.moves

	def set_moves(self, pokemon_moves):
		"""Setter for Pokémon moves (from moves.py)."""
		self.moves = pokemon_moves
		self.check_moves()

	def check_moves(self):
		"""Verification that moves are correct."""
		if isinstance(self.moves, list):
			for move in self.moves:
				if isinstance(move, moves.Move):
					continue
			print("Your moves are correct.")
		else:
			self.moves = moves.set_moves()

	# NATURE #
	def get_nature(self):
		"""Getter for Pokémon nature."""
		return self.nature

	def set_nature(self, nature):
		"""Setter for Pokémon nature."""
		# Check input
		self.nature = nature
		self.check_nature()

	def check_nature(self):
		"""Verify nature, and document which stats it boosts and weakens."""
		try:
			this_nature = nature_df.loc[self.nature.capitalize()]
			self.pro_nat, self.con_nat = this_nature[0], this_nature[1]
			print("Your nature is correct.")
		except KeyError:
			nature_input = input(
				"Your nature could not be found. Please enter another:"
			)
			self.set_nature(nature_input)

	# IVs #
	def get_ivs(self):
		"""Getter for Pokémon IVs."""
		return self.ivs

	def set_ivs(self, ivs):
		"""Setter for Pokémon IVs."""
		if ivs != "reset":
			self.check_ivs()
		else:
			ivs_set = True
			while ivs_set:
				ivs_input = input(
					"Please input 6 IVs, divided by forward-slashes '/': "
					"HP/Attack/Defense/Sp. Attack/Sp. Defense/Speed."
				)
				ivs_list = ivs_input.split("/")
				try:
					ivs_list = [int(i) for i in evs_list]  # Convert EVs to int
					self.check_ivs()
				except ValueError:
					print("You inputted a non-numeric character.")
					self.ivs = "reset"
					self.set_ivs()

	def check_ivs(self):
		"""Verify that IVs respect their bounds."""
		# Amount
		reset_ivs = "reset"
		if len(self.ivs) != STAT_AMOUNT:
			print("You don't have 6 IVs. Try again.")
			self.set_evs(reset_ivs)

		# Values
		try:
			for value in self.ivs:
				if 0 < value <= IV_MAX and isinstance(int, value):
					continue
			print("Your IVs are correct.")
		except ValueError:
			print("One of your IVs is not between 0 and 31.")
			self.set_ivs(reset_ivs)

	# EVs #
	def get_evs(self):
		"""Getter for Pokémon Effort Values (EVs)."""
		return self.evs

	def set_evs(self, evs):
		"""Setter for Pokémon Effort Values (EVs)."""
		if evs != "reset":
			self.check_evs()
		else:
			evs_set = True
			while evs_set:
				evs_input = input(
					"Please input 6 EVs, divided by forward-slashes '/': "
					"HP/Attack/Defense/Sp. Attack/Sp. Defense/Speed."
				)
				evs_list = evs_input.split("/")
				try:
					evs_list = [int(i) for i in evs_list]  # Convert EVs to int
					self.check_evs()
				except ValueError:
					print("You inputted a non-numeric character.")
					self.evs = "reset"
					self.set_evs()

	def check_evs(self):
		"""Verify that EVs respect their bounds."""
		# Amount
		reset_evs = "reset"
		if len(self.evs) != STAT_AMOUNT:
			print("You don't have 6 EVs. Try again.")
			self.set_evs(reset_evs)

		# Values
		ev_total = 0
		try:
			for value in self.evs:
				if 0 < value <= EV_MAX and isinstance(int, value):
					ev_total += value
					if ev_total > EV_MAX_TOTAL:
						print(f'You have too many EVs (max {EV_MAX_TOTAL})')
						self.set_evs(reset_evs)
			print("Your EVs are correct.")
		except ValueError:
			print("One of your IVs is not between 0 and 31, or not an int.")
			self.set_evs(reset_evs)

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
			print("Your Pokémon's type effectiveness has been calculated.")
			return type_dict

	def determine_stats(self):
		"""
		Using Base Stats, Nature, EVs & IVs, use formulae to find the
		final calculated stats for this Pokémon.
		"""
		# Nature processing
		nature_dict = {
			"Attack": 1,
			"Defense": 2,
			"SpAttack": 3,
			"SpDefense": 4,
			"Speed": 5
		}
		pro, con = nature_dict[self.pro_nat], nature_dict[self.con_nat]

		determined_stats = []
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
		print("Your Pokémon's final statistics have been determined.")
		return determined_stats
