'''
"Responsible Use of AI"
1. How much AI did you use in your work?

- I used an AI (specifically, chatgpt or gemini) to explain the logic of alpha-beta pruning. 
It helped me understand how the pseudocode would work with my existing code from a previous exercise.

- I also used an AI for the implementation of the best_move function. 
This function uses the alpha-beta-pruning function to evaluate the best move for the current player during the game. 
While the AI guided the logical structure, I implemented the code myself and used it for debugging.

2. Which parts of your work involved the use of AI tools?

- The alpha_beta_prune and best_move functions involved the use of AI tools. 
 I had a hard time making these functions compatible with my base code because their logical structure didn't align with my initial implementation. 
 The AI helped me understand and debug these functions to ensure they ran correctly.

Responsible Use Justification:
- I used AI responsibly and ethically by limiting its role to explanation, debugging assistance, 
 and providing insights into logic structure. I relied on AI mainly to help me understand complex errors, 
 clarify confusing parts of the code, and guide me in debugging, rather than letting it do the work entirely.

Failure to provide this disclosure will result in the work being subject to further review.

'''

'''
Submitted by: Tiamzon, Edgar Alan Emmanuel III B.
CMSC 170 - Exercise 3: Designing an AI agent for a Tic-Tac-Toe Game
09-15-25
'''

# import that randomizes the move of AI
import random

class TicTacToe:
    # Comments from your original code are preserved below.

    def __init__(self):
        self.state = [" "] * 9
        self.curr_player = 'X'
        self.winner_player = None
        self.gameRunning = True
        self.EMPTY = " "

    # print state
    def print_board(self):
        # start at index 0
        # stop before index 9
        # print each line to 3
        for i in range(0, 9, 3):
            print(" | ".join(self.state[i:i+3]))

            # i = 0 and i = 3 will print this
            # until less than 6
            # since each line is printed by 3 indices
            if i < 6:
                print ("==+==+==")

    # checks the player input position
    # identifies the player whose next to move
    def to_move(self, position):
        if self.state[position] == self.EMPTY:
            self.state[position] = self.curr_player
            return True
        else:
            print("Spot is taken!")
            return False

    # check the winning pattern
    def goal_test(self, state):
        winning_patterns = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), # horizonal
            (0, 3, 6), (1, 4 , 7), (2, 5, 8), # vertical
            (0, 4, 8), (2, 4, 6) # diagonal
        ]

        # winning patterns for each cell
        for cells in winning_patterns:
            if state[cells[0]] == state[cells[1]] == state[cells[2]] != " ":
                return state[cells[0]]
        
        # none is game over
        return None

    def utility(self, state):
        # assign numerical value to each terminal state
        winner = self.goal_test(state)
         
         # win for MAX
        if winner == 'X':
            return 1 
        
        # win for MIN
        elif winner == 'O':
            return -1

         # game draw 
        elif self.EMPTY not in state:
            return 0 
        
        return None

    # determines all the legal moves available from the given states
    def actions(self, state):
        return [i for i, cell in enumerate(state) if cell == self.EMPTY]
    

    # specifies the state that follows when action is taken
    def result(self, state, a, player):
        
        new_board = list(state) # this creates a copy of the current state
        
        # this marks the player's 'X' or 'O' on a specified action(a) on the copied state
        new_board[a] = player 
        return new_board # return the new state after a move has been made

    def alpha_beta_prune(self, state, alpha, beta, player):
        
        # this checks if the current state is a terminal state
        # using utility it determines the final score of a player
        # +1 for a win, -1 for a loss, and 0 for a draw
        score = self.utility(state)
        if score is not None:
            return score
        
        # for maximizing player
        if player == 'X': 
            best_eval = -99999 # goal is to find the maximium possible score
            
            # iterates possible moves using actions function
            for move in self.actions(state):
                
                # explores state without changing the current game board
                new_board = self.result(state, move, player)

                # recursive step 
                eval = self.alpha_beta_prune(new_board, alpha, beta, 'O')

                # updates the best evaluation with the minimum score found
                best_eval = max(best_eval, eval)

                # updates alpha, the best score the maximizing player can guarantee
                alpha = max(alpha, best_eval)

                # if the condition is met, it breaks the loop to prune the branch
                if beta <= alpha:
                    break 
                
            # returns the best evaluation found for the maximizing player
            return best_eval
        
        # for minimizing player
        else: 
            best_eval = 99999 # goal is to find the minimum possible score
            for move in self.actions(state):
                
                # explores state without changing the current game board
                new_board = self.result(state, move, player)

                # recursive step 
                eval = self.alpha_beta_prune(new_board, alpha, beta, 'X')

                # updates the best evaluation with the minimum score found
                best_eval = min(best_eval, eval)

                 # updates beta, the best score the minimizing player can guarantee
                beta = min(beta, best_eval)
                if beta <= alpha:
                    break
                
            # returns the best evaluation found for the minimizing player
            return best_eval

    def best_move(self):
        # this function used the alpha_beta_prune function in finding the best move
        # where from the game instance, is the current player
        
        # randomize position of AI 
        if len(self.actions(self.state)) == 9:
            
            # if it's the first move, a random choice is made
            return random.choice(self.actions(self.state))

        # set initial best_eval based on the current player
        # -99999 for the maximizing player ('X') and 99999 for the minimizing player ('O')
        if self.curr_player == 'X':
            best_eval = -99999
        else:
            best_eval = 99999

        # an empty list to store all moves that have the best evaluation score
        best_moves = []
        

        for move in self.actions(self.state):
            
            # get the new board state after making the current move
            new_board = self.result(self.state, move, self.curr_player)

            # call the alpha-beta pruning function to get the score of this move
            # the function is called for the opponent's turn
            eval = self.alpha_beta_prune(new_board, -99999, 99999, 'O' if self.curr_player == 'X' else 'X')
            

            if (self.curr_player == 'X' and eval > best_eval) or \
               (self.curr_player == 'O' and eval < best_eval):
                
                # if it's a new best score, update best_eval and start a new list for best moves
                best_eval = eval
                best_moves = [move]

            # if the score is equally as good as the best, add it to the list
            elif eval == best_eval:
                best_moves.append(move)

        # randomly select a move from the list of best moves to break ties
        return random.choice(best_moves)

    def play(self):
        # User Interaction: Human can choose to play first/second
        choice = ''
        while choice not in ['1', '2']:
            choice = input("\nChoose (1) to play first or second (2)? (AI is 'X', you are 'O'): ")

        if choice == '2':
            self.curr_player = 'X'
        else:
            self.curr_player = 'O'
            
        while self.gameRunning:
            print("\n")
            self.print_board()

            if self.curr_player == 'O': # Human player's turn
                try:
                    valid_move = int(input(f"\nPlayer {self.curr_player}, choose a spot from 0-8: "))
                except ValueError:
                    print("\nInvalid input. Please enter a valid position from 0-8.")
                    continue

                if valid_move < 0 or valid_move > 8:
                    print("\nError: Position out of range! Choose between 0 to 8: ")
                    continue

                if self.to_move(valid_move):
                    if self.goal_test(self.state):
                        self.print_board()
                        print(f"\nPlayer {self.curr_player} wins!\n")
                        return
                    
                    if self.EMPTY not in self.state:
                        self.print_board()
                        print ("\nIt is a draw!\n")
                        return
                    
                    self.curr_player = "X"
            
            else: # AI's turn
                best_move = self.best_move()
                self.to_move(best_move)
                print(f"AI chose spot {best_move}")
                
                if self.goal_test(self.state):
                    self.print_board()
                    print(f"\nPlayer {self.curr_player} wins!\n")
                    return
                
                if self.EMPTY not in self.state:
                    self.print_board()
                    print ("\nIt is a draw!\n")
                    return
                
                self.curr_player = "O"
            
if __name__ == "__main__":
    game = TicTacToe()
    game.play()