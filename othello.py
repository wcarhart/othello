import os
import sys
import logging
import argparse

tiles = []

def red(text):
	return "\033[91m{}\033[0m".format(text)

def green(text):
	return "\033[92m{}\033[0m".format(text)

def grey(text):
	return "\033[90m{}\033[0m".format(text)

def game_loop():
	turn = 1
	game_over = False
	while not game_over:
		# print board for players to see
		print_board()

		# acquire next move
		move = acquire_move(turn)

		# need to check if move is valid for this game (i.e. if that tile is taken, if player is allowed to move there)
		# TODO

		# update the game board
		update_game(move, turn)

		# change turns to next player
		turn = 1 if turn == 2 else 2

		# check if game has ended
		game_over = check_game_status()

def update_game(move, turn):
	tiles[move] = turn
	propogate_flips(move, turn)

def propogate_flips(move, turn):
	# TODO
	return

def check_game_status():
	empty_spaces = len([tile for tile in tiles if tile == 0])
	if empty_spaces == 0:
		return True
	else:
		return False

def acquire_move(turn):
	valid_input = False

	# TODO: refactor to make look less like spaghetti
	while not valid_input:
		if turn == 1:
			player_name = red("Player 1")
		else:
			player_name = green("Player 2")
		attempt = input("{}, where do you want to move? ".format(player_name))

		if attempt == 'exit' or attempt == 'done':
			sys.exit(0)

		if not len(attempt) == 2:
			print("Invalid input, invalid format - must be in the form of 'xN', where 'x' is a letter between A and H and 'N' is a number between 1 and 8")
			continue
		else:
			col = attempt[0].lower()
			row = attempt[1]
			cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
			if not col in cols:
				print("Invalid input, column index must be between A and H")
				continue

			try:
				row_index = int(row)
				if row_index < 1 or row_index > 8:
					print("Invalid input, row index must be between 1 and 8")
					continue
			except Exception as e:
				print("Invalid input, row index must be a number")
				continue

			# now we know input is valid
			col_index = cols.index(col)
			index = (col_index*8 + row_index) - 1

		# now we need to check if the inputted move is valid for this game
		if not tiles[index] == 0:
			print("Invalid move, there's already a piece in {}!".format(attempt))
			continue
		elif not is_valid_move(index):
			print("Invalid move, Player {} can't move to {}".format(turn, attempt))
			continue

		valid_input = True

	return index

def is_valid_move(index):
	# TODO
	return True

def build_parser():
	return

def main():
	# define game board
	global tiles
	tiles = tiles + [0]*64
	tiles[27] = 1
	tiles[28] = 2
	tiles[35] = 2
	tiles[36] = 1

	# start main game loop
	game_loop()

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
				# TODO: log error if here
				pass
			
			print("{} ".format(text), end='', flush=True)
		print("")


if __name__ == '__main__':
	main()