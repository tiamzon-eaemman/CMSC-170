# "Responsible Use of AI"

class TicTacToe:
    def __init__(self):
        # empty 3x3 
        self.board = [" "] * 9

        self.current_player = "X"	# X always starts first

    def show_board(self):
        # print the current state of the board
        for i in range(0, 9, 3):
            print(" | ".join(self.board[i:i+3]))  # print each row
            if i < 6:  # for removing the extra lines
                print("--+---+--")

    def make_move(self, position):
        # check if the spotis already taken
        if self.board[position] == " ":
            self.board[position] = self.current_player
            return True
        else:
            print("That spot taken!!")
            return False

    def check_winner(self):
       
        # all the winning patterns
        win_patterns = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # horizontal
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # vertical
            (0, 4, 8), (2, 4, 6)              # diagonal
        ]

        # Check if all 3 cells in any pattern match the current player
        for a, b, c in win_patterns:
            if self.board[a] == self.board[b] == self.board[c] != " ":
                return True
        return False

    def play(self):
        # game loop
        for _ in range(9):  # 9 move max
            self.show_board()  # print board every turn

            # ask current player their move
            try:
                move = int(input(f"Player {self.current_player}, choose a spot (0-8): "))
            except ValueError:
                print("Invalid input. Please enter a number from 0 to 8.")
                continue

            if move < 0 or move > 8:
                print("Position out of range! Choose between 0 and 8.")
                continue

            # place the move in the board
            if self.make_move(move):
                # check if move is a win
                if self.check_winner():
                    self.show_board()
                    print(f"Player {self.current_player} wins!")
                    return
                # switch player if no win
                self.current_player = "O" if self.current_player == "X" else "X"

        self.show_board()
        print("It's a draw!")

# Run the game
if __name__ == "__main__":
    game = TicTacToe()
    game.play()