import unittest
from unittest import mock, TestCase
from moves import Move, pick_moves, move_input_parser, MOVES_PER_POKEMON

# Example Moves
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


class TestMoves(TestCase):
	@mock.patch('moves.input', side_effect=[5, -1, 0, "hello", 4])
	def test_parser_bounds_and_int_input(self, mock_input):
		"""Check that incorrect input (strings, minus & out-of-bounds integers)
		are skipped."""
		self.assertEqual(move_input_parser(MOVES_PER_POKEMON), 4)

	@mock.patch('moves.input', side_effect=[1, 1, 43, 1, 43, 47, 43, 48])
	def test_pick_moves_functionality(self, mock_input):
		"""Ensure that move attributes are inputted correctly, and that
		repeated inputs are skipped."""
		picked_moves = pick_moves()
		for i in range(MOVES_PER_POKEMON - 1):
			self.assertTrue(example_moves[i].__dict__, picked_moves[i].__dict__)


if __name__ == '__main__':
	unittest.main()
