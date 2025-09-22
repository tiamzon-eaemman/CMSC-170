import math
import random

# Constants for players, using numerical values for the minimax algorithm
X_PLAYER = 1
O_PLAYER = -1
EMPTY = " "

class TicTacToe:
    # Comments from your original code are preserved below.
    
    def __init__(self):
        self.board = [EMPTY] * 9
        self.curr_player = 'X'
        self.winner_player = None # not used
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
    # identifies the player whose next to move
    def to_move(self, position):
        if self.board[position] == EMPTY:
            self.board[position] = self.curr_player
            return True
        else:
            print("Spot is taken!")
            return False

    # check the winning pattern
    def is_winner(self):
        winning_patterns = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), # horizonal
            (0, 3, 6), (1, 4 , 7), (2, 5, 8), # vertical
            (0, 4, 8), (2, 4, 6) # diagonal
        ]

        # winning patterns for each cell
        for cells in winning_patterns:
            if self.board[cells[0]] == self.board[cells[1]] == self.board[cells[2]] != EMPTY:
                return self.board[cells[0]]
        return None

    # This method is not needed for the minimax algorithm if the logic is handled in `is_terminal`.
    # It has been removed to simplify the code and avoid redundancy.
    
    def actions(self, state):
        # determines the legal moves available from the given states
        # list of all possible moves
        return [i for i, cell in enumerate(state) if cell == EMPTY]

    def result(self, state, move, player):
        # specifies the state that follows when action is taken
        new_board = list(state)
        new_board[move] = player
        return new_board

    def minimax(self, state, player):
        # This function is not used when alpha-beta pruning is implemented.
        # It's kept here for reference but can be removed.
        score = self.utility(state)
        if score is not None:
            return score
        
        # for max nodes
        if player == X_PLAYER:
            max_eval = -math.inf
            for move in self.actions(state):
                new_board = self.result(state, move, player)
                to_eval = self.minimax(new_board, O_PLAYER)
                max_eval = max(max_eval, to_eval)
            return max_eval

        # for min nodes
        else: # player == O_PLAYER
            min_eval = math.inf
            for move in self.actions(state):
                new_board = self.result(state, move, player)
                to_eval = self.minimax(new_board, X_PLAYER)
                min_eval = min(min_eval, to_eval)
            return min_eval

    def utility(self, board):
        winner = self.is_winner()
        if winner == 'X':
            return 1
        elif winner == 'O':
            return -1
        elif EMPTY not in board:
            return 0  # Draw
        return None

    def alpha_beta_prune(self, state, alpha, beta, player):
        score = self.utility(state)
        if score is not None:
            return score
        
        if player == X_PLAYER:
            # For the maximizing player
            best_eval = -math.inf
            for move in self.actions(state):
                new_board = self.result(state, move, player)
                eval = self.alpha_beta_prune(new_board, alpha, beta, O_PLAYER)
                best_eval = max(best_eval, eval)
                alpha = max(alpha, best_eval)
                # if v>=β: return m
                if beta <= alpha:
                    break
            return best_eval
        else:
            # For the minimizing player
            best_eval = math.inf
            for move in self.actions(state):
                new_board = self.result(state, move, player)
                eval = self.alpha_beta_prune(new_board, alpha, beta, X_PLAYER)
                best_eval = min(best_eval, eval)
                beta = min(beta, best_eval)
                # if v<=α: return m
                if beta <= alpha:
                    break
            return best_eval

    def find_best_move(self):
        # This method uses the alpha_beta_prune function to find the best move
        # for the current player of the game instance.
        
        # Convert the board to a numerical representation for the algorithm
        board_numerical = []
        for cell in self.board:
            if cell == 'X':
                board_numerical.append(X_PLAYER)
            elif cell == 'O':
                board_numerical.append(O_PLAYER)
            else:
                board_numerical.append(EMPTY)

        if self.curr_player == 'X':
            best_eval = -math.inf
            player_val = X_PLAYER
        else:
            best_eval = math.inf
            player_val = O_PLAYER

        best_move = []
        
        for move in self.actions(board_numerical):
            new_board = self.result(board_numerical, move, player_val)
            eval = self.alpha_beta_prune(new_board, -math.inf, math.inf, -player_val)
            
            if (player_val == X_PLAYER and eval > best_eval) or \
               (player_val == O_PLAYER and eval < best_eval):
                best_eval = eval
                best_move = [move]
    
        return random.choice(best_move)

    def play(self):
        while self.gameRunning:
            print("\n")
            self.print_board()

            if self.curr_player == 'X':
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
                        self.print_board()
                        print(f"\nPlayer {self.curr_player} wins!\n")
                        return
                    
                    if " " not in self.board:
                        self.print_board()
                        print ("\nIt is a draw!\n")
                        return
                    
                    self.curr_player = "O"
            
            else: # AI's turn
                print("\nAI is making a move...")
                best_move = self.find_best_move()
                self.to_move(best_move)
                print(f"AI chose spot {best_move}")
                
                if self.is_winner():
                    self.print_board()
                    print(f"\nPlayer {self.curr_player} wins!\n")
                    return
                
                if " " not in self.board:
                    self.print_board()
                    print ("\nIt is a draw!\n")
                    return
                
                self.curr_player = "X"
            
if __name__ == "__main__":
    game = TicTacToe()
    game.play()