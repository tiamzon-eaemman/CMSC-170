

# TEST TEST TEST
# TEST TEST TEST

# TEST TEST TEST


with open("input.txt", "r") as file_object:

	content = file_object.read()	# read the input.txt file

	number_array = content.strip().replace("\n", ";").split(";")	# convert the contents of the input.txt file into an array
	number_array = [int(x) for x in number_array]
	print(number_array)

	# MAIN CODE

	# the 
	def main_board():	
		board = number_array[:]	# use the number array as the main board

		if is_solvable(board) and not is_solved(board):		# check first if the board is solvable or already solved
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
		return inversions % 2 == 0		# check if the board is solvable even = solvable and odd = not

	def is_solved(board):
		return board == list(range(1, 9)) + [0]		# format of solved board

	def show(board):	# show the gui of the board
		for i in range(0, 9, 3):
			row = [" " if x == 0 else str(x) for x in board[i:i+3]]
			print(" | ".join(row))
			if i < 6:
				print("--|---|--")
				print()

	def move(board, direction):	
		blankIndex = board.index(0)	# store position of blank space
		blank_row, blank_col = divmod(blankIndex, 3)	# conversion of 1D array to 2D array coordinates
     
		moves = {'w': (1, 0), 'x': (-1, 0), 'a': (0, 1), 'd': (0, -1)}
  
		if direction in moves:	# check if input is valid
			row_change, col_change = moves[direction]	# get the coordinates
			new_row, new_col = blank_row + row_change, blank_col + col_change	# this is the new position of the tile to move
			if 0 <= new_row < 3 and 0 <= new_col < 3:	# for boundaries of the board
				new_index = new_row * 3 + new_col	# 2D to 1D conversion
				board[blankIndex], board[new_index] = board[new_index], board[blankIndex]	# swap the blank space and adjacecnt tile
			else:
				print("Invalid move")
		else:
			print("Invalid move")

	def play():
		board = main_board()
  
		while True:	
			show(board)
			if is_solved(board):
				print("You solved it!")
				break
			move(board, input("Move (w/a/x/d): ").lower())

	if __name__ == "__main__":
		play()

# the file is automatically closed outside the with block