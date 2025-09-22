# "Responsible Use of AI"
'''
searched for a function that removes all the duplicates for the explored - set() (line 72)

bfs and dfs has same implementation just different in data structure used
'''

with open("input.txt", "r") as file_object:
    content = file_object.read()  # read the input.txt file
    number_array = content.strip().replace("\n", ";").split(";")
    number_array = [int(x) for x in number_array]
    print(number_array)

def main_board():
    board = number_array[:]  # use the number array as the main board
    if is_solvable(board) and not is_solved(board):	# check first if the board is solvable or already solved
        return board
    else:
        print("Board not solvable or already solved...")
        exit()

def is_solvable(board):
    inversions = 0
    for i in range(9):
        for j in range(i + 1, 9):
            if board[i] and board[j] and board[i] > board[j]:
                inversions += 1
    return inversions % 2 == 0  # even = solvable, odd = not

def is_solved(board):
    return board == list(range(1, 9)) + [0]

def show(board):
    for i in range(0, 9, 3):
        row = [" " if x == 0 else str(x) for x in board[i:i+3]]
        print(" | ".join(row))
        if i < 6:
            print("--|---|--")
    print()

def move(board, direction):
    blankIndex = board.index(0)  # position of blank space
    blank_row, blank_col = divmod(blankIndex, 3)

    moves = {'w': (1, 0), 'x': (-1, 0), 'a': (0, 1), 'd': (0, -1)}
    if direction in moves:
        row_change, col_change = moves[direction]
        new_row, new_col = blank_row + row_change, blank_col + col_change
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_index = new_row * 3 + new_col
            board[blankIndex], board[new_index] = board[new_index], board[blankIndex]
        else:
            print("Invalid move")
    else:
        print("Invalid move")



def get_neighbors(state):
    neighbors = []
    index = state.index(0)
    row, col = divmod(index, 3)
    moves = [(-1,0), (1,0), (0,-1), (0,1)]  
    for dr, dc in moves:
        r, c = row + dr, col + dc
        if 0 <= r < 3 and 0 <= c < 3:
            new_index = r * 3 + c
            new_state = state[:]  # copy entire array
            new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
            neighbors.append(new_state)
    return neighbors

def solve_bfs(initial_state):
    goal = list(range(1, 9)) + [0]
    frontier = [(initial_state, [])]  
    explored = set()

    while frontier:
        state, path = frontier.pop(0)  # use queue (pop always the first)
        if state == goal:
            return path + [state], len(path), len(explored)
        if str(state) in explored:
            continue
        explored.add(str(state))
        for neighbor in get_neighbors(state):
            if str(neighbor) not in explored:
                frontier.append((neighbor, path + [state]))
    return goal, frontier, explored

def solve_dfs(initial_state):
    goal = list(range(1, 9)) + [0]
    frontier = [(initial_state, [])]  
    explored = set()

    while frontier:
        state, path = frontier.pop()  # use stack (pop always the last)
        if state == goal:
            return path + [state], len(path), len(explored)
        if str(state) in explored:
            continue
        explored.add(str(state))
        for neighbor in get_neighbors(state):
            if str(neighbor) not in explored:
                frontier.append((neighbor, path + [state]))
    return goal, frontier, explored

# function for heuristic function number of misplaced tiles
def hOne(state):
    # count the number of misplaced tiles (compare initial state to goal state)
    goal_state = list(range(1,9)) + [0]
    count = 0
    for index in range(len(state)):
        if state[index] != 0 and state[index] != goal_state[index]:
            count += 1

    return count

# function for heuristic function manhattan distance
def hTwo(state):
    distance = 0
    for current_index in range(len(state)):
        tile = state[current_index]

        if tile != 0:  # skip the blank tile or 0
            # calculate goal index 
            goal_index = tile - 1  # current index for loop iterates from 1 to 8, then subtract 1 to get the goal index based on the array

            # current position (row, col)
            current_row = current_index // 3
            current_col = current_index % 3

            # goal position (row, col)
            goal_row = goal_index // 3
            goal_col = goal_index % 3

            # distance = vertical + horizontal 
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)

    return distance

# function for heuristic function number of non-adjacent tiles
def hThree(state):
    goal = list(range(1, 9)) + [0]

    # Use goal adjacent pairs from the slide (horizontal + vertical)
    goal_adjacent_pairs = [
        [1, 2], [2, 3], [4, 5], [5, 6], [7, 8],
        [1, 4], [4, 7], [2, 5], [5, 8], [3, 6]
    ]

    # find current adjacent tile pairs in the given state
    current_pairs = set()

    for i in range(len(state)):
        tile = state[i]
        if tile == 0:
            continue  # skip blank

        # check horizontal pairs
        if (i % 3) != 2:
            right_tile = state[i + 1]
            if right_tile != 0:
                pair = (tile, right_tile) if tile < right_tile else (right_tile, tile)
                current_pairs.add(pair)

        # check vertical pairs
        if i < 6:
            down_tile = state[i + 3]
            if down_tile != 0:
                pair = (tile, down_tile) if tile < down_tile else (down_tile, tile)
                current_pairs.add(pair)

    # count goal-adjacent pairs that are missing in the current state
    missing_goal_pairs = 0
    for pair in goal_adjacent_pairs:
        if (pair[0], pair[1]) not in current_pairs:
            missing_goal_pairs += 1

    return missing_goal_pairs




def astar_search(initial_state, heuristic):
    goal_state = list(range(1,9)) + [0]

    if heuristic == 1:
        chosenHeuristic = hOne(initial_state)
    elif heuristic == 2:
        chosenHeuristic = hTwo(initial_state)
    elif heuristic == 3:
        chosenHeuristic = hThree(initial_state)
    else:
        print("Invalid choice, default would be Misplaced Tiles")
        heuristic = 2
        chosenHeuristic = hTwo(initial_state)

    # initialize open and closed list
    #            initial state, path, g,          h,                 f
    open_list = [(initial_state, [],  0, chosenHeuristic, chosenHeuristic)]
    closed_list = []

    # start of the logic
    # while open is not empty
    while open_list:
        # get the index of the state with the lowest total cost f (tie-break on lower h)
        min_index = 0
        for i in range(1,len(open_list)):   # iterate over all the nodes in the open_list
            if open_list[i][4] < open_list[min_index][4]:
                min_index = i
                
            elif open_list[i][4] == open_list[min_index][4] and open_list[i][3] < open_list[min_index][3]:
                min_index = i
        best_node = open_list.pop(min_index)
        
        # store state, path, and g
        current_state = best_node[0]
        path = best_node[1]
        g = best_node[2]    
        
        # add to explore after removing from the open_list
        closed_list.append(current_state)
        
        # check if goal reached
        if current_state == goal_state:
            return path + [current_state], len(path), len(closed_list)

        # get the neighbors of the current state
        neighbors = get_neighbors(current_state)
        
        # update the costs of each neighbor
            # add 1 to g (this means going down the level)
            # store new heuristic using heuristic function
            # to get f add g and h
        for neighbor in neighbors:
            newG = g + 1    # to update what level we are in (cost so far)

            if heuristic == 1:
                newH = hOne(neighbor)
            elif heuristic == 2:
                newH = hTwo(neighbor)
            elif heuristic == 3:
                newH = hThree(neighbor)
            else:
                newH = hOne(neighbor) # default is misplaced tiles
            
            newF = newG + newH  # calculate the total cost for each neighbor
            
            # check if then neighbor is already in close_list (explored) 
            # this prevents duplicate states in closed_list
            in_closed = False
            for closed in closed_list:
                if neighbor == closed:
                    in_closed = True
                    break
            if in_closed:
                continue
            
            # check if neighbor is already in open_list and find the index of the repeated/duplicate state
            in_open = False 
            duplicate_index = -1
            for i in range(len(open_list)):
                if neighbor == open_list[i][0]:
                    in_open = True
                    duplicate_index = i
                    break

            # add the neighbor to open_list if not there
            if not in_open:
                open_list.append((neighbor, path + [current_state], newG, newH, newF))
            else:
                # if already in open_list but found a better path then update it
                if newF < open_list[duplicate_index][4] or (newF == open_list[duplicate_index][4] and newH < open_list[duplicate_index][3]):
                    open_list[duplicate_index] = (neighbor, path + [current_state], newG, newH, newF)
    
    return [], 0, len(closed_list)  # if no solution found

def play():
    board = main_board()
    initial_state = board[:]  

    print("[1] Solve using BFS")
    print("[2] Solve using DFS")
    print("[3] Solve using A* search")
    choice = int(input("Enter choice: "))

    if choice == 1:
        path, cost, explored = solve_bfs(initial_state)
    elif choice == 2:
        path, cost, explored = solve_dfs(initial_state)
    elif choice == 3:
        print("\n[1] Number of Misplaced Tiles")
        print("[2] Manhattan Distance")
        print("[3] Number of non-adjacent Tiles")
        func_choice = int(input("Enter choice: "))
        print("")
        path, cost, explored = astar_search(initial_state, func_choice)
    else:
        print("Invalid choice.")
        return

    if path:
        print("\nSolution found!")
        print("Path cost:", cost)
        print("Explored states:", explored)
        print("\nSolution path:\n")
        for step in path:
            show(step)
    else:
        print("No solution found.")

if __name__ == "__main__":
    play()

