'''
Design Tic Tac tOE
NXN
Default n = 3, but can be changed to anything

antidiagonal = row+col = n
X=1
O=-1
x ALWAYS starts
'''

class Game:
    def __init__(self, n: int = 3):
        self.n = n
        self.board = [[None for _ in range(n)] for _ in range(n)]
        self.isEnd = False
        self.turn = 'X'

        self.row = [0]*n
        self.col = [0]*n
        self.diagonal = 0
        self.antidiagonal = 0
        self.number_of_moves = 0

    def isWinner(self,row,col)-> bool: 
        if abs(self.row[row]) == (self.n):
            return True
        
        if abs(self.col[col]) == (self.n):
            return True
        
        if abs(self.diagonal)==(self.n):
            return True
        
        if abs(self.antidiagonal) == (self.n):
            return True
        
        return False

    def isDraw(self)->bool:
        return True if self.number_of_moves == (self.n*self.n) else False

    def play_move(self, row,col)-> None:
        if self.isEnd:
            return
        
        if row<0 or row>=self.n or col<0 or col>=self.n:
            print("Invalid move")
            return 
        
        if self.board[row][col]:
            print("Invalid block")
            return
        
        #now everything should be done

        self.board[row][col] = self.turn

        self.row[row] += 1 if self.turn == 'X' else -1
        self.col[col] += 1 if self.turn == 'X' else -1

        if (row-col)==0:
            self.diagonal += 1 if self.turn == 'X' else -1
        
        if (row+col)+1==self.n:
            self.antidiagonal += 1 if self.turn == 'X' else -1

        if self.isWinner(row,col):
            if self.turn == 'X':
                print('X')
            else:
                print('O')
            self.isEnd=True
            return
        
        self.number_of_moves +=1
        
        if self.isDraw():
            print('DRAW')
            self.isEnd = True

        if self.turn == 'X':
            self.turn = 'O'
        else:
            self.turn = 'X'


def print_board(game):
    n = game.n
    print()
    for r in range(n):
        print(' | '.join(cell if cell else '.' for cell in game.board[r]))
        if r < n - 1:
            print('-' * (4 * n - 3))
    print()


def main():
    game = Game()
    print("Tic Tac Toe — enter moves as: row col (0-indexed)")
    print_board(game)

    while not game.isEnd:
        try:
            move = input(f"{game.turn}'s turn > ").split()
            row, col = int(move[0]), int(move[1])
        except (ValueError, IndexError):
            print("Enter two numbers separated by a space, e.g. '0 2'")
            continue
        game.play_move(row, col)
        print_board(game)


if __name__ == "__main__":
    main()
        



    
