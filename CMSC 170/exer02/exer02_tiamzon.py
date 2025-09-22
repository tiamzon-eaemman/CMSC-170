'''
"Responsible Use of AI"
1. How much AI did you use in your work?

- I used AI specifically for checking bugs and the possible logical structure of my code.

- I also used AI in the get_neighbors and solve_star functions since their state representations were not the same, 
  so I needed an alternative algorithm that could satisfy both functions.

- I also used AI to explain certain blocks of code and their structure, 
  since I still had some confusion when trying to implement the code solely from pseudocode.

2. Which parts of your work involved the use of AI tools?

- Functions like get_neighbors and solve_star, because I realized that if their algorithms had different approaches, 
  it would be difficult to solve the problem consistently, and there were many errors that needed debugging.

Responsible Use Justification:
- I used AI responsibly and ethically by limiting its role to explanation, debugging assistance, 
 and providing insights into logic structure. I relied on AI mainly to help me understand complex errors, 
 clarify confusing parts of the code, and guide me in debugging, rather than letting it do the work entirely.

Failure to provide this disclosure will result in the work being subject to further review.

'''

'''
Submitted by: Tiamzon, Edgar Alan Emmanuel III B.
CMSC 170 - Exercise #1 - Solving 8-puzzle using A* search
09-06-25
EF-5L
'''

global flat_tiles

class Puzzle:
    def __init__(self, tiles):
        
        # normalize to 1D
        if isinstance(tiles[0], list): # if the input is 2D, flatten is necessary
            self.tiles = [x for row in tiles for x in row]
        
        else:
            self.tiles = list(tiles) # just makes a copy of tiles
        
        self.prev = None

        print("\ninitial state 1D: ", self.tiles)

        # calls the functin if its solvable
        if not self.is_solvable(self.tiles):
            raise ValueError("\n8-puzzle is not solvable!\n")

        # calles the function if its already solved
        if self.is_solved():
            raise SystemExit

    # checks if the puzzle is solvable
    def is_solvable(self, flat_tiles):
        inversions = 0 # count for inversions
        N = len(flat_tiles)

        for i in range(N):
            for j in range (i + 1, N):
                # does not include blank tile (0) in counting inversions
                if flat_tiles[i] != 0 and flat_tiles[j] != 0 and flat_tiles[i] > flat_tiles[j]:
                    inversions += 1
        
        return inversions % 2 == 0

    def is_solved(self):

        # checks if the puzzle already reach the goal state
        goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        return self.tiles == goal_state
    
    def move(self, direction):
        blank_row, blank_col = -1, -1

        # iterates each row and col in order to determine where the blank tile (0) is currently located
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
        
        # If a state is passed in, use it. Otherwise, use the object's tiles
        if state is not None:
            board = state
        else:
            board = self.tiles

        # Print a blank line before the board
        print("\n")

        # Loop through each row (0, 1, 2)
        for r in range(3):
            # Slice the board to get the row (3 elements)
            row_start = r * 3
            row_end = (r + 1) * 3
            row = board[row_start:row_end]

            # Convert each tile into a string
            display_row = []
            for x in row:
                if x != 0:
                    display_row.append(str(x))   # numbers stay as string numbers
                else:
                    display_row.append(" ")      # blank tile shown as a space

            # Join the elements with vertical separators
            row_str = " | ".join(display_row)

            # Print the row
            print(row_str)

            # Print separator after rows 0 and 1
            if r < 2:
                print("==|===|==")
                print()


    def get_neighbors(self, state):
        
        neighbors = [] # holds the reachable state
        idx = state.index(0) # finds the position of 0 or blank tile

        # row idx // 3
        # col idx % 3
        row, col = divmod(idx, 3) # converts 1D to 2D puzzle

        # movement: up down left right
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # loop over reach possible direction
        for dir_row, dir_col in moves:

            # computes the target row and col if 0 moves in that direction
            r1, c1 = row + dir_row, col + dir_col

            # checks the 3x3 grid boundary
            if 0 <= r1 < 3 and 0 <= c1 < 3:
                new_index = r1 * 3 + c1 # conversion to 1D
                new_state = state[:] # copies the entire array

                # swap the blank tile to other tile producing new neighbor state
                new_state[idx], new_state[new_index] = new_state[new_index], new_state[idx]
                
                neighbors.append(new_state) # appends to the list of new neighbor list

        return neighbors        

   
    # BFS implementation
    def solve_bfs(self, initial_state):
        goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]

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
        
        # why this is the return statement?
        # since it can return garbage statement when the while loop does not
        # reach its goal
        return None, 0, len(visited) # signal that the search have failed


    # DFS implementation
    # algorithm same as 
    def solve_dfs(self, initial_state):
        goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]


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
                  # .append is used since neighbors can be a list
                  # multiple neighbors (multiple nodes) can be consider
                  # path + [state]
                  # path considers two state where it come from and its destination
                  # [state] = current state (kung nasaan ka ngayon)
                  # add new state into frontier
                    frontier.append((neighbors, path + [state]))
        
        # why this is the return statement?
        # since it can return garbage statement when the while loop does not
        # reach its goal
        return None, 0, len(visited) # signal that the search have failed
    
    # counts the number of tiles that are not in their correct position
    def misplaced_tiles(self, state):
        goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        h1_count = 0 # counts the number of misplaced tiles

        for node in range(len(state)):

            # exclude 0 tile or empty value
            if state[node] != 0 and state[node] != goal[node]:
                h1_count += 1

            #print("TEST: misplaced tiles = ", h1_count)

        return h1_count 
    
    def manhattan_dist(self, state):

        # using 2D dicitionary solution
        goal_state_dict = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (2, 0), 8: (2, 1), 0: (2, 2)
        }

        manhattan_dst = 0

        # enumerate() is used to loop through a list
        for i, curr_tile in enumerate(state):
            
            if curr_tile != 0:
                #current position of the tile
                row, col = divmod(i , 3)
                
                # goal position of the tile
                goal_row, goal_col = goal_state_dict[curr_tile]

                # solution for manhattan distance
                manhattan_dst += abs(row - goal_row) + abs(col - goal_col)

        return manhattan_dst
   
    # recheck algorithm
    def non_adjacent(self, state):
        goal = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        adjacent_pairs = [
            [1, 2], [2, 3], [4, 5], [5, 6], [7, 8],
            [1, 4], [4, 7], [2, 5], [5, 8], [3, 6]
        ]

        # ensures each designated pairs
        paired_tile = set()

        for index in range(len(state)):
            current_tile = state[index]
            
            # ignore the blank tile
            if current_tile == 0:
                continue 
            
            # search for horizontal pairs
            if (index % 3) != 2:
                Htile = state[index + 1]
            
                if Htile != 0:
                    pair = (current_tile, Htile) if current_tile < Htile else (Htile, current_tile)
                    paired_tile.add(pair)

            # search for vertical pairs
            if index < 6:
                Vtile = state[index + 3]
                if Vtile != 0:
                    pair = (current_tile, Vtile) if current_tile < Vtile else (Vtile, current_tile)
                    paired_tile.add(pair)

        # this counts the paired or adjacent tiles that are missing 
        # in the current state
        missing_pairs = 0
        for pair in adjacent_pairs:
            if (pair[0], pair[1]) not in paired_tile:
                missing_pairs +=1
        
        return missing_pairs


    def solve_star(self, initial_state, heuristic):

        goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

        print(initial_state)

        #  selection for heuristic approach
        if heuristic == 1:
            selectedHeuristic = self.misplaced_tiles(initial_state)

        elif heuristic == 2:
            selectedHeuristic = self.manhattan_dist(initial_state)
        
        elif heuristic == 3:
            selectedHeuristic = self.non_adjacent(initial_state)

        else:
            print("Invalid choice, default choice would be Manhattan Distance")
            heuristic = 2
            selectedHeuristic = self.manhattan_dist(initial_state)

        # GOAL: f(n) = g(n) + h(n)
        # initialized open list and closed list
        # actual current state (open_list)   
                 # initial state,  path, g(n),   h(n),              f(n)
        open_list = [(initial_state, [], 0, selectedHeuristic, selectedHeuristic )]
        close_list = []

        while open_list:
            # node with the minimum value
            min_value = 0

            for i in range(1, len(open_list)):

                # check first if the f(n) of child nodes are less than
                # the inital state (parent node)
                if open_list[i][4] < open_list[min_value][4]:
                    min_value = i # set that node as the minimum value
                
                # check if parent and child nodes have the same f(n)
                elif open_list[i][4] == open_list[min_value][4]:
                    min_value = i   # set that node as the minimum value
            
            bestNode = open_list.pop(min_value) # pop the minimum node

            # after popping the node, this decides the nodes that will be explore next
            # identifying its best node, this node will be the one to be explore and expand
            curr_state = bestNode[0]
            path = bestNode[1]
            g = bestNode[2]

            # close list the visited / expanded list since this node
            # should not be use / consider again
            # this can also contain the suboptimal nodes or dead-end nodes
            close_list.append(curr_state)

            if curr_state == goal_state:
                # returns the list of moves that lead to goal state
                return path + [curr_state], len(path), len(close_list)
            
            # getting the current state which can be expand unless already the goal state
            # this comes with possible new nodes
            # this new nodes are the new neighbors to goal state
            new_neighbors = self.get_neighbors(curr_state)

            # iterate each neighbors
            for neighbor in new_neighbors:
                # this will add new sublevel or nodes
                newG = g + 1

                # this new nodes or neighbors will do again the heuristic options
                if heuristic == 1:
                    newH = self.misplaced_tiles(neighbor)
                
                elif heuristic == 2:
                    newH = self.manhattan_dist(neighbor)
                
                elif heuristic == 3:
                    newH = self.non_adjacent(neighbor)
                
                else:
                    # set as default
                    newH = self.manhattan_dist(neighbor)

                # calculates the total cost for each neighbor
                newF = newG + newH 

                
                if neighbor in close_list:
                    continue

                found_index = -1
                for idx, entry in enumerate(open_list):

                    # if neighbor mathches in one those states,
                    # store the index in found_index
                    if neighbor == entry[0]: # entry[0] is the actual state
                        found_index = idx

                        # if not, stays at -1
                        break
                
                
                # if the neighbor is not yet in the open list
                # add them
                if found_index == -1:
                    open_list.append((neighbor, path + [curr_state], newG, newH, newF))

                    # adding new neighbor could result in comparing previous neighbor
                    # so this compares a better path from the already placed neighbor
                    # to new added neighbor


                else:
                    '''
                    breakdown of the condition
                    1. newF < open_list[check_duplicate][4] checks if the new calculated f(n) = newF
                    for the neighbor is less than the duplicate node that is alredy in the open list
                    meaning, we find the shortest path

                    2. newF == open_list[check_duplicate][4] and newH < open_list[check_dupliicate][3]
                    tie breaker rule:
                    so if the newF is just equal to current f(n)
                    this suggests the comparing the lower heuristic value
                    '''
                    if newF < open_list[found_index][4] or (newF == open_list[found_index][4] and newH < open_list[found_index][3]):
                        
                        # updates the open list as a better path
                        open_list[found_index] = (neighbor, path + [curr_state], newG, newH, newF)
    
        return [], 0, len(close_list) # return if there is no solution found


   
    def play(self):
        board = self.tiles  
        initial_state = board

        # main UI
        print("\n++++++==========+++++")
        print("  8 puzzle solver")
        print("++++++==========+++++")
        print("[1] Solve using BFS")
        print("[2] Solve using DFS")
        print("[3] Solve using A* search")
        choice = int(input("Enter choice: "))

        
        if choice == 1:
            path, cost, visited = self.solve_bfs(initial_state)
        
        elif choice == 2:
            path, cost, visited = self.solve_dfs(initial_state)
        
        elif choice == 3:
            print("\n[1] Number of Misplaced tiles")
            print("[2] Number of Manhattan distance tiles")
            print("[3] Number of Non-adjacent tiles")

            choice1 = int(input("Enter choice: "))
            print("")
            path, cost, visited = self.solve_star(initial_state, choice1)

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

            game = Puzzle(num_array_1d)
            game.play()

    except FileNotFoundError:
        print("Error: 'input.txt' not found.")
    except (ValueError, IndexError):
        print("Error: Invalid content.")
