'''
"Responsible Use of AI"
1. How much AI did you use in your work?
    - I used AI for checking all of my logical expression including syntax,
    semantics, and parameters that is needed to use since I used OOP python 
    where I'm new into this method. 
    I also consider of using AI on how can I solve bfs and dfs according
    to my algorithm. 

2. Which parts of your work involved the use of AI tools?
    - solve_bfs, solve_dfs, and get_neighbors

Responsible Use Justification:
Explain how you used AI responsibly and ethically in completing the task.
    - I used AI fix the errors by copy pasting to chatGPT and then I copied it
    while considering there were no changes on my algorithm, it was just on the
    specific line of code that I need to solve. 

Failure to provide this disclosure will result in the work being subject to further review.

I also used the reference in YouTube:
https://www.youtube.com/watch?v=DDdYFmSXrm0
'''

'''
Submitted by: Tiamzon, Edgar Alan Emmanuel III B.
CMSC 170 - Diagnostic Exercise
08-22-25
EF-5L
'''

global flat_tiles

class Puzzle:
    def __init__(self, tiles):
        self.tiles = tiles
        self.prev = None
        
        # 1D flattened list to check solvability
        # self.tiles = [[1,2,3], [4,5,6], [7,8,0]]
        # flat_tiles = [1,2,3,4,5,6,7,8,0]
        flat_tiles = [item for sublist in self.tiles for item in sublist]
        
        # remove the blank tile for inversion count
        # since it cannot compare into numerical values
        if 0 in flat_tiles:
            flat_tiles.remove(0)
        elif " " in flat_tiles:
            flat_tiles.remove(" ")

        if not self.is_solvable(flat_tiles):
            print("8-puzzle is not solvable!")
            exit()

        if self.is_solved():
            print("8-puzzle already solved!")
            exit()

    def is_solvable(self, flat_tiles):
        inversion = 0 # count for switching pair
        N = len(flat_tiles) # 1D length of the tile

       # print(flat_tiles)

        # iterates each tile
        for i in range(N):
            for j in range(i + 1, N):
                if flat_tiles[i] > flat_tiles[j]:
                    inversion += 1
        
        return inversion % 2 == 0

    def is_solved(self):
        # solved state using " " as the blank space
        solved_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        return self.tiles == solved_state
    
    def move(self, direction):
        blank_row, blank_col = -1, -1

        for r in range(3):
            for c in range(3):
                if self.tiles[r][c] == 0:
                    blank_row = r
                    blank_col = c
                    break
            if blank_row != -1:
                break

        moves = {'w':[-1, 0], 'x':[1,0], 'a':[0, -1], 'd':[0,1]}
        '''
            w = -1 since it decreases the value of a 2D list (up movement)
            x = +1 since it increases the value of a 2D list (down movement)
            a = -1 since it decreases the value of a 2D list (left movement)
            d = +1 since it increases the value of a 2D list (right movement)
        '''

        if direction in moves:

            change_row, change_col = moves[direction]

            # corresponds to the changing row and col based on the move direction
            '''
                1 3 2  user type = w     1 3 3
                8 5 6                    0 5 6
                0 7 4                    8 7 4   

                current pos. (3, 0) - (-1, 0)
                            = (2, 3)
            '''

            new_row, new_col = blank_row + change_row, blank_col + change_col

            # 0 to 2 indices only
            if 0 <= new_row < 3 and 0 <= new_col < 3: # checks the 3x3 boundaries of the puzzle
                # swap operation for 2D list
                self.tiles[blank_row][blank_col], self.tiles[new_row][new_col] = \
                    self.tiles[new_row][new_col], self.tiles[blank_row][blank_col]
            else:
                print("Invalid move!")
        else:
            print("Invalid move!")

    def print_tiles(self, state=None):
        board = state if state else self.tiles

        print("\n")

        for r in range(3):
            # join the elements of the inner list for each row
            row_str = " | ".join([str(x) if x != 0 else " " for x in board[r]])
            print(row_str)
            if r < 2:
                print("==|===|==")
                print()

    def get_neighbors(self, state):
        neighbors = []
        N = len(state)

        # find the row and column with a blank
        row, col = -1, -1
        for i in range(N):
            for j in range(N):
                if state[i][j] == 0:   # use 0 as blank
                    row, col = i, j
                    break
            if row != -1:
                break

        # swap this index from the possible neighbors of row and col
        # position in up, down, left, and right
        for [i ,j] in [[row-1, col],[row+1, col],[row, col-1],[row, col+1]]:
            if i >= 0 and j>=0 and i < N and j < N: # valid 3x3 boundaries
                # copy the whole state
                n_tiles = [r[:] for r in state]

                # swap positions
                n_tiles[row][col], n_tiles[i][j] = n_tiles[i][j], n_tiles[row][col]
                
                # append the new value from swapped position into neighbors
                neighbors.append(n_tiles)
        return neighbors            

   
    # BFS implementation
    def solve_bfs(self, initial_state):
        goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

        # path is in 2D array
        frontier = [(initial_state, [])] # [initial state, path[]]
        visited = set()

        # this will iterate each possible state
        while frontier:
            state, path = frontier.pop(0) # always pop the first node
            

            # if the state already visited, continue and add as visited
            state_str = str(state)
            if state_str in visited:
                continue

            # .add() refers to one whole node (state)
            visited.add(state_str)

            # if the current state reach the goal return the state and its path
            if state == goal:
                return path + [state], len(path), len(visited)
            
            # expand neighbors
            for neighbors in self.get_neighbors(state):
                if str(neighbors) not in visited:
                  # .append is used since neighbors can be a list
                  # multiple neighbors (multiple nodes) can be consider
                  # path + [state]
                  # path considers two state where it come from and its destination
                  # [state] = current state (kung nasaan ka ngayon)
                  # add new state into frontier
                  frontier.append((neighbors, path + [state]))
        
        return None, 0, len(visited)

    # DFS implementation
    # algorithm same as 
    def solve_dfs(self, initial_state):
        goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

        frontier = [(initial_state, [])]
        visited = set()

        while frontier:
            state, path = frontier.pop() # stack behavior
            

            state_str = str(state)
            if state_str in visited:
                continue

            visited.add(state_str)

            if state == goal:
                return path + [state], len(path), len(visited)
            
            for neighbors in self.get_neighbors(state):
                if str(neighbors) not in visited:
                    frontier.append((neighbors, path + [state]))
        
        return None, 0, len(visited)
   
    def play(self):
        board = self.tiles  
        initial_state = board

        # main UI
        print("\n++++++==========+++++")
        print("  8 puzzle solver")
        print("++++++==========+++++")
        print("[1] Solve using BFS")
        print("[2] Solve using DFS")
        print("Enter choice: ")

        choice = int(input())
        
        if choice == 1:
            path, cost, visited = self.solve_bfs(initial_state)
        
        elif choice == 2:
            path, cost, visited = self.solve_dfs(initial_state)

        else:
            print("\nERROR: Invalid choice!")
            return

        if path:
            print("\nSolution found!")
            print("Path cost:", cost)
            print("Explored states:", visited)
            print("\nSolution path:")

            for step in path:
                self.print_tiles(step)
                print()
        else:
            print("No solution found.")


if __name__ == "__main__":
    try:
        with open("input.txt", "r") as file_object:
            content = file_object.read()

            # this line converts the 1D input into a 2D list of numbers and strings
            num_array_1d = [int(x) if x.isdigit() else x for x in content.strip().replace("\n", ";").split(";") if x]
            
            # key change: create a 2D list for the class
            num_array_2d = [num_array_1d[i:i+3] for i in range(0, 9, 3)]

            print(f"\nOriginal 1D array: {num_array_1d}")
            game = Puzzle(num_array_2d)
            game.play()

    except FileNotFoundError:
        print("Error: 'input.txt' not found.")
    except (ValueError, IndexError):
        print("Error: Invalid content.")
