# "Responsible Use of AI"

'''
Submitted by: Tiamzon, Edgar Alan Emmanuel III B.
CMSC 170 - Diagnostic Exercise
08-22-25

'''

class TicTacToe:

  def __init__(self):
    self.board = [" "] *  9
    self.curr_player = 'X'
    self.winner_player = None
    self.gameRunning = True

  # print board

  def print_board(self):

    # start at index 0
    # stop before index 9
    # print each line to 3
    for i in range(0, 9, 3):
      print(" | ".join(self.board[i:i+3]))

      # i = 0 and i = 3 will print this
      # until less than 6
      # since each line is printed by 3 indices
      if i < 6:
        print ("==+==+==")


  # checks the player input position
  def to_move(self, position):
      if self.board[position] == " ":
        self.board[position] = self.curr_player
        return True
      
      else:
        print("Spot is taken!")


  # check the winning pattern
  def is_winner(self):

    winning_patterns = [
      # horizonal
      (0, 1, 2), (3, 4, 5), (6, 7, 8),

      # vertical
      (0, 3, 6), (1, 4 , 7), (2, 5, 8),

      # diagonal
      (0, 4, 8), (2, 4, 6)

    ]

    # winning patters for each cell 
    '''
    ex.
    there SHOULD be no empty string " "
    cell1 = 0, cell2 = 4, cell3 = 8 (valid for diagonal)
    then it is valid (True)
    '''
    for cell1, cell2, cell3 in winning_patterns:
      if self.board[cell1] == self.board[cell2] == self.board[cell3] != " ":
        return True
    return False

  def play(self):

    while self.gameRunning:
      print("\n")
      self.print_board()

      try:
        valid_move = int(input(f"\nPlayer {self.curr_player}, choose a spot from 0-8: "))

      except ValueError:
        print("\nInvalid input. Please enter a valid position from 0-8.")
        continue

      if valid_move < 0 or valid_move > 8:
        print("\nError: Position out of range! Choose between 0 to 8: ")
        continue

      if self.to_move(valid_move):
        
        if self.is_winner():
          print(f"\nPlayer {self.curr_player} wins!\n")
          return
        
        if self.curr_player == "X":
          self.curr_player = "O"
        
        else:
          self.curr_player = "X"

        if " " not in self.board:
          self.print_board()
          print ("\nIt is a draw!\n")
          return


if __name__ == "__main__":
  game = TicTacToe()
  game.play()