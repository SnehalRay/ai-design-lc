import unittest
from io import StringIO
from unittest.mock import patch
from code import Game


class TestGame(unittest.TestCase):

    def test_initial_state(self):
        game = Game()
        self.assertEqual(game.turn, 'X')
        self.assertFalse(game.isEnd)
        for row in game.board:
            for cell in row:
                self.assertIsNone(cell)

    def test_x_wins_row(self):
        # X: (0,0), (0,1), (0,2) — O fills col 1 then col 2
        game = Game()
        with patch('sys.stdout', new_callable=StringIO) as mock_out:
            game.play_move(0, 0)  # X
            game.play_move(1, 0)  # O
            game.play_move(0, 1)  # X
            game.play_move(1, 1)  # O
            game.play_move(0, 2)  # X wins row 0
        self.assertIn('X', mock_out.getvalue())
        self.assertTrue(game.isEnd)

    def test_o_wins_col(self):
        # O wins column 1
        game = Game()
        with patch('sys.stdout', new_callable=StringIO) as mock_out:
            game.play_move(0, 0)  # X
            game.play_move(0, 1)  # O
            game.play_move(2, 0)  # X
            game.play_move(1, 1)  # O
            game.play_move(2, 2)  # X
            game.play_move(2, 1)  # O wins col 1
        self.assertIn('O', mock_out.getvalue())
        self.assertTrue(game.isEnd)

    def test_x_wins_main_diagonal(self):
        # X wins (0,0), (1,1), (2,2)
        game = Game()
        with patch('sys.stdout', new_callable=StringIO) as mock_out:
            game.play_move(0, 0)  # X
            game.play_move(0, 1)  # O
            game.play_move(1, 1)  # X
            game.play_move(0, 2)  # O
            game.play_move(2, 2)  # X wins diagonal
        self.assertIn('X', mock_out.getvalue())
        self.assertTrue(game.isEnd)

    def test_o_wins_antidiagonal(self):
        # O wins (0,2), (1,1), (2,0)
        game = Game()
        with patch('sys.stdout', new_callable=StringIO) as mock_out:
            game.play_move(0, 0)  # X
            game.play_move(0, 2)  # O
            game.play_move(1, 0)  # X
            game.play_move(1, 1)  # O
            game.play_move(2, 2)  # X
            game.play_move(2, 0)  # O wins antidiagonal
        self.assertIn('O', mock_out.getvalue())
        self.assertTrue(game.isEnd)

    def test_draw(self):
        # X O X
        # X X O
        # O X O  — no winner, all cells filled
        game = Game()
        with patch('sys.stdout', new_callable=StringIO) as mock_out:
            game.play_move(0, 0)  # X
            game.play_move(0, 1)  # O
            game.play_move(0, 2)  # X
            game.play_move(1, 2)  # O
            game.play_move(1, 0)  # X
            game.play_move(2, 0)  # O
            game.play_move(1, 1)  # X
            game.play_move(2, 2)  # O
            game.play_move(2, 1)  # X — board full, draw
        self.assertIn('DRAW', mock_out.getvalue())
        self.assertTrue(game.isEnd)

    def test_invalid_occupied_cell(self):
        game = Game()
        game.play_move(0, 0)  # X
        with patch('sys.stdout', new_callable=StringIO) as mock_out:
            game.play_move(0, 0)  # O tries same cell
        self.assertEqual(game.board[0][0], 'X')  # cell unchanged
        self.assertFalse(game.isEnd)

    def test_no_move_after_game_over(self):
        # X wins, then another move is attempted
        game = Game()
        game.play_move(0, 0)  # X
        game.play_move(1, 0)  # O
        game.play_move(0, 1)  # X
        game.play_move(1, 1)  # O
        game.play_move(0, 2)  # X wins

        with patch('sys.stdout', new_callable=StringIO):
            game.play_move(2, 2)  # should be rejected

        self.assertIsNone(game.board[2][2])  # cell must remain empty

    def test_4x4_board(self):
        # X fills entire row 0 of a 4x4 board
        game = Game(4)
        with patch('sys.stdout', new_callable=StringIO) as mock_out:
            game.play_move(0, 0)  # X
            game.play_move(1, 0)  # O
            game.play_move(0, 1)  # X
            game.play_move(1, 1)  # O
            game.play_move(0, 2)  # X
            game.play_move(1, 2)  # O
            game.play_move(0, 3)  # X wins row 0
        self.assertIn('X', mock_out.getvalue())
        self.assertTrue(game.isEnd)


if __name__ == '__main__':
    unittest.main()
