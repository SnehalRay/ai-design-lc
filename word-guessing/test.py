import unittest
from unittest.mock import patch
from code import WordGame


class TestWordGame(unittest.TestCase):

    # 1. Duplicate correct guess — tries must not change, board must not re-print meaningfully
    def test_duplicate_correct_guess(self):
        game = WordGame("SPOOF")
        with patch("builtins.print"):
            game.guess_letter("O")
            tries_after_first = game.tries
            game.guess_letter("O")
        self.assertEqual(game.tries, tries_after_first)
        self.assertEqual(game.revealed[2], "O")
        self.assertEqual(game.revealed[3], "O")

    # 2. Duplicate wrong guess — tries decremented only once
    def test_duplicate_wrong_guess(self):
        game = WordGame("SPOOF")
        with patch("builtins.print"):
            game.guess_letter("X")
            game.guess_letter("X")
        self.assertEqual(game.tries, 5)

    # 3. Letter with multiple occurrences — all positions revealed in one guess
    def test_multiple_occurrences(self):
        game = WordGame("SPOOF")
        with patch("builtins.print"):
            game.guess_letter("O")
        self.assertEqual(game.revealed[2], "O")
        self.assertEqual(game.revealed[3], "O")

    # 4. Lowercase input — treated same as uppercase
    def test_lowercase_input(self):
        game = WordGame("SPOOF")
        with patch("builtins.print"):
            game.guess_letter("o")
        self.assertEqual(game.revealed[2], "O")
        self.assertEqual(game.revealed[3], "O")

    # 5. Win condition — all letters guessed correctly
    def test_win_condition(self):
        game = WordGame("SPOOF")
        with patch("builtins.print"):
            for letter in ["S", "P", "O", "F"]:
                game.guess_letter(letter)
        self.assertTrue(game.is_over())
        self.assertNotIn(None, game.revealed)

    # 6. Loss condition — tries exhausted on wrong guesses
    def test_loss_condition(self):
        game = WordGame("SPOOF", tries=3)
        with patch("builtins.print"):
            for letter in ["X", "Y", "Z"]:
                game.guess_letter(letter)
        self.assertTrue(game.is_over())
        self.assertEqual(game.tries, 0)

    # 7. Single-letter word — one correct guess ends the game
    def test_single_letter_word(self):
        game = WordGame("A")
        with patch("builtins.print"):
            game.guess_letter("A")
        self.assertTrue(game.is_over())
        self.assertEqual(game.revealed, ["A"])

    # 8. All-same-letter word — single guess wins
    def test_all_same_letter_word(self):
        game = WordGame("AAA")
        self.assertEqual(game.letter_map, {"A": [0, 1, 2]})
        with patch("builtins.print"):
            game.guess_letter("A")
        self.assertTrue(game.is_over())
        self.assertEqual(game.revealed, ["A", "A", "A"])

    # 9. Guessing after game is over — tries must not go below 0
    def test_guess_after_game_over(self):
        game = WordGame("SPOOF", tries=1)
        with patch("builtins.print"):
            game.guess_letter("X")  # game over — tries = 0
            self.assertTrue(game.is_over())
            game.guess_letter("Y")  # should not decrement further
        self.assertEqual(game.tries, 0)


if __name__ == "__main__":
    unittest.main()
