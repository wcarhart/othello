import os
import sys
import argparse

tiles = []

def flashing(text):
	return "\033[5m{}\033[0m".format(text)

def grey(text):
	return "\033[90m{}\033[0m".format(text)

def red(text):
	return "\033[91m{}\033[0m".format(text)

def green(text):
	return "\033[92m{}\033[0m".format(text)

def yellow(text):
	return "\033[93m{}\033[0m".format(text)

def blue(text):
	return "\033[94m{}\033[0m".format(text)

def pink(text):
	return "\033[95m{}\033[0m".format(text)

def teal(text):
	return "\033[96m{}\033[0m".format(text)

def white(text):
	return "\033[97m{}\033[0m".format(text)

def game_loop():
	turn = 1
	game_over = False
	while not game_over:
		# print board for players to see
		print_board()

		# acquire next move
		move = acquire_move(turn)

		# update the game board
		update_game(move, turn)

		# change turns to next player
		turn = 1 if turn == 2 else 2

		# check if game has ended
		game_over = check_game_status()

def update_game(move, turn):
	# add new tile to board
	tiles[move] = turn

	# update tiles already on board
	propogate_flips(move, turn)

def propogate_flips(move, player):
	# go in all eight directions and look for another piece of the same color as `turn`
	# if we find one, flip all in between, if we don't, move on

	to_flip = []

	# west
	index = move - 1
	candidates = []
	while index < 64 and index > -1:
		candidate = tiles[index]
		if candidate == 0:
			break
		if not candidate == player:
			candidates.append(index)
		elif candidate == player:
			to_flip += candidates
			break
		index -= 1

	# east
	index = move + 1
	candidates = []
	while index < 64 and index > -1:
		candidate = tiles[index]
		if candidate == 0:
			break
		if not candidate == player:
			candidates.append(index)
		elif candidate == player:
			to_flip += candidates
			break
		index += 1

	# north
	index = move - 8
	candidates = []
	while index < 64 and index > -1:
		candidate = tiles[index]
		if candidate == 0:
			break
		if not candidate == player:
			candidates.append(index)
		elif candidate == player:
			to_flip += candidates
			break
		index -= 8

	# south
	index = move + 8
	candidates = []
	while index < 64 and index > -1:
		candidate = tiles[index]
		if candidate == 0:
			break
		if not candidate == player:
			candidates.append(index)
		elif candidate == player:
			to_flip += candidates
			break
		index += 8

	# northwest
	index = move - 9
	candidates = []
	while index < 64 and index > -1:
		candidate = tiles[index]
		if candidate == 0:
			break
		if not candidate == player:
			candidates.append(index)
		elif candidate == player:
			to_flip += candidates
			break
		index -= 9

	# northeast
	index = move - 7
	candidates = []
	while index < 64 and index > -1:
		candidate = tiles[index]
		if candidate == 0:
			break
		if not candidate == player:
			candidates.append(index)
		elif candidate == player:
			to_flip += candidates
			break
		index -= 7

	# southeast
	index = move + 9
	candidates = []
	while index < 64 and index > -1:
		candidate = tiles[index]
		if candidate == 0:
			break
		if not candidate == player:
			candidates.append(index)
		elif candidate == player:
			to_flip += candidates
			break
		index += 9

	# southwest
	index = move + 7
	candidates = []
	while index < 64 and index > -1:
		candidate = tiles[index]
		if candidate == 0:
			break
		if not candidate == player:
			candidates.append(index)
		elif candidate == player:
			to_flip += candidates
			break
		index += 7

	flip(to_flip)

def flip(indices):
	for index in indices:
		tiles[index] = 1 if tiles[index] == 2 else 2

def check_game_status():
	empty_spaces = len([tile for tile in tiles if tile == 0])
	if empty_spaces == 0:
		return True
	else:
		return False

def acquire_move(turn):
	valid_input = False

	while not valid_input:
		# determine whose turn it is
		if turn == 1:
			player_name = red("Player 1")
		else:
			player_name = green("Player 2")

		# prompt user for move
		attempt = input("{}, where do you want to move? ".format(player_name))

		# exit
		if attempt == 'exit' or attempt == 'done':
			sys.exit(0)

		# show board again
		if attempt == 'show':
			print_board()
			continue

		# display possible moves
		if attempt == 'where':
			print_board_with_hints(turn)
			continue

		# incorrect length
		if not len(attempt) == 2:
			print(" Invalid input, must be in the form of 'xN', where 'x' (row) is a letter between A and H and 'N' (column) is a number between 1 and 8")
			continue
		else:
			row = attempt[0].lower()
			col = attempt[1]

			# make sure col
			rows = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
			if not row in rows:
				print(" Invalid input, row index must be between A and H")
				continue
			try:
				col_index = int(col)
				if col_index < 1 or col_index > 8:
					print(" Invalid input, column index must be between 1 and 8")
					continue
			except Exception as e:
				print(" Invalid input, column index must be a number")
				continue

			# now we know input is valid
			row_index = rows.index(row)
			index = (row_index*8 + col_index) - 1

		# now we need to check if the inputted move is valid for this game
		if not tiles[index] == 0:
			print(" Invalid move, there's already a piece in {}{}!".format(attempt[0].upper(), attempt[1]))
			continue
		elif not is_valid_move(index, turn):
			print(" Invalid move, {} can't move to {}{}".format(player_name, attempt[0].upper(), attempt[1]))
			continue

		valid_input = True

	return index

def is_valid_move(index, player):
	# go through each tile on the board, check eight directions and see if there's a valid sandwich

	# west
	temp = index - 1
	fillings = 0
	while temp < 64 and temp > -1:
		tile_value = tiles[temp]
		if tile_value == 0:
			break
		if not tile_value == player:
			fillings += 1
		elif tile_value == player:
			if not fillings == 0:
				return True
			else:
				break
		temp -= 1

	# east
	temp = index + 1
	fillings = 0
	while temp < 64 and temp > -1:
		tile_value = tiles[temp]
		if tile_value == 0:
			break
		if not tile_value == player:
			fillings += 1
		elif tile_value == player:
			if not fillings == 0:
				return True
			else:
				break
		temp += 1

	# north
	temp = index - 8
	fillings = 0
	while temp < 64 and temp > -1:
		tile_value = tiles[temp]
		if tile_value == 0:
			break
		if not tile_value == player:
			fillings += 1
		elif tile_value == player:
			if not fillings == 0:
				return True
			else:
				break
		temp -= 8

	# south
	temp = index + 8
	fillings = 0
	while temp < 64 and temp > -1:
		tile_value = tiles[temp]
		if tile_value == 0:
			break
		if not tile_value == player:
			fillings += 1
		elif tile_value == player:
			if not fillings == 0:
				return True
			else:
				break
		temp += 8

	# northwest
	temp = index - 9
	fillings = 0
	while temp < 64 and temp > -1:
		tile_value = tiles[temp]
		if tile_value == 0:
			break
		if not tile_value == player:
			fillings += 1
		elif tile_value == player:
			if not fillings == 0:
				return True
			else:
				break
		temp -= 9

	# northeast
	temp = index - 7
	fillings = 0
	while temp < 64 and temp > -1:
		tile_value = tiles[temp]
		if tile_value == 0:
			break
		if not tile_value == player:
			fillings += 1
		elif tile_value == player:
			if not fillings == 0:
				return True
			else:
				break
		temp -= 7

	# southeast
	temp = index + 9
	fillings = 0
	while temp < 64 and temp > -1:
		tile_value = tiles[temp]
		if tile_value == 0:
			break
		if not tile_value == player:
			fillings += 1
		elif tile_value == player:
			if not fillings == 0:
				return True
			else:
				break
		temp += 9

	# southwest
	temp = index + 7
	fillings = 0
	while temp < 64 and temp > -1:
		tile_value = tiles[temp]
		if tile_value == 0:
			break
		if not tile_value == player:
			fillings += 1
		elif tile_value == player:
			if not fillings == 0:
				return True
			else:
				break
		temp += 7

	return False

def build_parser():
	parser = argparse.ArgumentParser(description=__doc__, formatter_class = argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-c', '--config', action='store_true', default=False, required=False, help="Set up player configuration before starting the game")
	return parser

def main():
	# parse command line arguments
	parser = build_parser()
	args = parser.parse_args()

	if args.config:
		# TODO
		pass

	# define game board
	global tiles
	tiles = tiles + [0]*64
	tiles[27] = 1
	tiles[28] = 2
	tiles[35] = 2
	tiles[36] = 1

	# start main game loop
	game_loop()

def print_board_with_hints(player):
	# determine possible moves
	temp_board = [0]*64
	for index in range(64):
		if is_valid_move(index, player):
			temp_board[index] = -1
		else:
			temp_board[index] = tiles[index]

	# display board
	print("\n  1 2 3 4 5 6 7 8")
	cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
	for i in range(8):
		print("{} ".format(cols[i]), end='', flush=True)
		for j in range(8):
			index = i*8+j
			if temp_board[index] == 0:
				text = grey("-")
			elif temp_board[index] == 1:
				text = red("*")
			elif temp_board[index] == 2:
				text = green("*")
			else:
				text = flashing(white("*"))
			
			print("{} ".format(text), end='', flush=True)
		print("")

def print_board():
	print("\n  1 2 3 4 5 6 7 8")
	cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
	for i in range(8):
		print("{} ".format(cols[i]), end='', flush=True)
		for j in range(8):
			index = i*8+j
			if tiles[index] == 0:
				text = grey("-")
			elif tiles[index] == 1:
				text = red("*")
			elif tiles[index] == 2:
				text = green("*")
			else:
				# error
				pass
			
			print("{} ".format(text), end='', flush=True)
		print("")


if __name__ == '__main__':
	main()