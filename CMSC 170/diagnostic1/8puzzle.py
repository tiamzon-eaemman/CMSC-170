# "Responsible Use of AI"


'''
Submitted by: Tiamzon, Edgar Alan Emmanuel III B.
CMSC 170 - Diagnostic Exercise
08-22-25

'''


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
        N = len(flat_tiles) # length of the tile

        # iterates each tile
        for i in range(N):
            for j in range(i + 1, N):
                if flat_tiles[i] > flat_tiles[j]:
                    inversion += 1
        
        return inversion % 2 == 0

    def is_solved(self):
        # Solved state using " " as the blank space
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
            w = -1 since it decreaases the value of a 2D list (up movement)
            x = +1 since it increses the value of a 2D list (down movement)
            a = -1 since it decreaases the value of a 2D list (left movement)
            d = +1 since it increses the value of a 2D list (right movement)

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

    def print_tiles(self):
        for r in range(3):
            # join the elements of the inner list for each row
            row_str = " | ".join([str(x) if x != 0 else " " for x in self.tiles[r]])
            print(row_str.replace('0', ' ').replace('\' \'', ' '))
            if r < 2:
                print("==|===|==")
                print()

    # start the 8puzzle game
    def play(self):
        while not self.is_solved():
            self.print_tiles()
            direction = input("\nMove the tile (w/a/x/d): ").lower()
            self.move(direction)

        self.print_tiles()
        print("\nPuzzle solved!")

if __name__ == "__main__":
    try:
        with open("input.txt", "r") as file_object:
            content = file_object.read()

            # this line converts the 1D input into a 2D list of numbers and strings
            num_array_1d = [int(x) if x.isdigit() else x for x in content.strip().replace("\n", ";").split(";") if x]
            
            # key change: create a 2D list for the class
            num_array_2d = [num_array_1d[i:i+3] for i in range(0, 9, 3)]

            print(f"Original 1D array: {num_array_1d}")
            game = Puzzle(num_array_2d)
            game.play()

    except FileNotFoundError:
        print("Error: 'input.txt' not found.")
    except (ValueError, IndexError):
        print("Error: Invalid content.")