class WordGame:
    def __init__(self, word, tries=6):
        self.word = word.upper()
        self.letter_map = self._build_letter_map()
        self.tries = tries
        self.revealed = [None] * len(self.word)
        self.guesses = set()
        self.game_over = False

    def _build_letter_map(self):
        letter_map = {}
        for i, letter in enumerate(self.word):
            letter = letter.upper()
            if letter not in letter_map:
                letter_map[letter] = []
            letter_map[letter].append(i)
        return letter_map

    def guess_letter(self, letter):
        if self.game_over:
            return
        if self.is_over():
            print("Game over")
            self.game_over = True
            return
        letter = letter.upper()
        if letter in self.guesses:
                print(f"Already guessed '{letter}'")
                return
        if letter in self.letter_map:
            
            for i in self.letter_map[letter]:
                self.revealed[i] = letter
        else:
            self.guesses.add(letter)
            self.tries -= 1
            print(f"'{letter}' is not in the word. {self.tries} tries left.")
        self.guesses.add(letter)
        self.print_attempt()
        if self.hasWon():
            print("Congratulations!")
            self.game_over = True
            

    def print_attempt(self):
        attempt = ''
        for i in self.revealed:
            if not i:
                attempt+='_'
            else:
                attempt+=i
        print(attempt)
        return attempt
    
    def hasWon(self):
        if None not in self.revealed:
            return True
        return False



    def is_over(self):
        return self.tries == 0 or None not in self.revealed


if __name__ == "__main__":
    game = WordGame("SPOOF")
    guesses = ["O", "S", "X", "P", "F"]

    for letter in guesses:
        print(f"Guessing: {letter}")
        game.guess_letter(letter)
