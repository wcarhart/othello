import sys
import argparse
import random

tiles = []
CORNERS = [0, 7, 56, 63]
WEST_EDGES = [0, 8, 16, 24, 32, 40, 48, 56]
NORTH_EDGES = [0, 1, 2, 3, 4, 5, 6, 7]
EAST_EDGES = [7, 15, 23, 31, 39, 47, 55]
SOUTH_EDGES = [56, 57, 58, 59, 60, 61, 62, 63]

player_one_name = "Player 1"
player_one_color = "red"
player_two_name = "Player 2"
player_two_color = "green"
adversary_name = ""
adversary_color = ""

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

def color(color, text):
	if color.lower() == 'grey':
		return grey(text)
	elif color.lower() == 'red':
		return red(text)
	elif color.lower() == 'green':
		return green(text)
	elif color.lower() == 'yellow':
		return yellow(text)
	elif color.lower() == 'blue':
		return blue(text)
	elif color.lower() == 'pink':
		return pink(text)
	elif color.lower() == 'teal':
		return teal(text)
	elif color.lower() == 'white':
		return white(text)
	else:
		return text

def adversary_game_loop(adversary):
	player_name = color(player_one_color, player_one_name)
	print("{} vs. {}".format(color(player_one_color, player_one_name), color(adversary_color, adversary_name)))

	turn = 1
	game_over = False
	while not game_over:
		# print board for players to see
		print_board()

		if turn == 1:
			if has_any_moves(turn):
				move = acquire_move(turn)
			else:
				turn = 2
				if has_any_moves(turn):
					print("Sorry {}, you don't have any moves left!".format(player_name))
					move = acquire_move_from_intelligence(tiles, adversary)
				else:
					game_over = True
					break
		else:
			move = acquire_move_from_intelligence(tiles, adversary)

		# update the game board
		update_game(move, turn)

		# change turns to next player
		turn = 1 if turn == 2 else 2

		# check if game has ended
		game_over = check_game_status()

	if game_over:
		print_board()
		print("")
		player_one_score = len([tile for tile in tiles if tile == 1])
		player_two_score = len([tile for tile in tiles if tile == 2])
		if player_one_score > player_two_score:
			print("{} wins!".format(color(player_one_color, player_one_name)))
		elif player_two_score > player_one_score:
			print("{} wins!".format(color(player_two_color, player_two_name)))
		else:
			print("It's a tie!")
		print("  {}'s score: {}".format(color(player_one_color, player_one_name), player_one_score))
		print("  {}'s score: {}".format(color(player_two_color, player_two_name), player_two_score))

def game_loop():
	print("{} vs. {}".format(color(player_one_color, player_one_name), color(player_two_color, player_two_name)))

	turn = 1
	game_over = False
	while not game_over:
		# print board for players to see
		print_board()

		# acquire next move
		if has_any_moves(turn):
			move = acquire_move(turn)
		else:
			turn = 1 if turn == 2 else 2
			if has_any_moves(turn):
				if turn == 1:
					player_name = color(player_one_color, player_one_name)
				else:
					player_name = color(player_two_color, player_two_name)
				print("Sorry {}, you don't have any moves left!".format(player_name))
				move = acquire_move(turn)
			else:
				game_over = True
				break

		# update the game board
		update_game(move, turn)

		# change turns to next player
		turn = 1 if turn == 2 else 2

		# check if game has ended
		game_over = check_game_status()

	if game_over:
		print_board()
		print("")
		player_one_score = len([tile for tile in tiles if tile == 1])
		player_two_score = len([tile for tile in tiles if tile == 2])
		if player_one_score > player_two_score:
			print("{} wins!".format(color(player_one_color, player_one_name)))
		elif player_two_score > player_one_score:
			print("{} wins!".format(color(player_two_color, player_two_name)))
		else:
			print("It's a tie!")
		print("  {}'s score: {}".format(color(player_one_color, player_one_name), player_one_score))
		print("  {}'s score: {}".format(color(player_two_color, player_two_name), player_two_score))

def has_any_moves(player):
	temp_board = [0]*64
	for index in range(64):
		if is_valid_move(index, player) and tiles[index] == 0:
			return True
	return False

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
			player_name = color(player_one_color, player_one_name)
		else:
			player_name = color(player_two_color, player_two_name)

		# prompt user for move
		attempt = input("{}, where do you want to move? ".format(player_name))

		# exit
		if attempt.lower().strip() == 'exit' or attempt.lower().strip() == 'done':
			sys.exit(0)

		# show board again
		if attempt.lower().strip() == 'show':
			print_board()
			continue

		# display possible moves
		if attempt.lower().strip() == 'where' or attempt.lower().strip() == 'where can i go' or attempt.lower().strip() == 'where can i go?':
			print_board_with_hints(turn)
			continue

		# show commands
		if attempt.lower().strip() == 'help' or attempt.lower().strip() == 'commands' or attempt.lower().strip() == 'command':
			show_commands()
			continue

		# clear screen
		if attempt.lower().strip() == 'clear':
			print(chr(27) + "[2J")
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

def show_commands():
	print("====Command list====")
	print(" B6     -> will attempt to place new tile on location B6")
	print(" show   -> will redraw the current board")
	print(" where  -> will show possible moves for the current player (you can also use 'hint' or 'where can I go?')")
	print(" help   -> show this menu and list of commands (you can also use 'command' or 'commands')")
	print(" clear  -> clear the screen")
	print(" exit   -> will end the game (you can also use 'done')")

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
		if temp in WEST_EDGES:
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
		if temp in EAST_EDGES:
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
		if temp in EAST_EDGES:
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
		if temp in WEST_EDGES:
			break
		temp += 7

	return False

def build_parser():
	parser = argparse.ArgumentParser(description=__doc__, formatter_class = argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--setup', action='store_true', default=False, required=False, help="Set up player configuration before starting the game")
	parser.add_argument('--list-commands', action='store_true', default=False, required=False, help="Show the available commands you can type during the game")
	parser.add_argument('--adversary', type=str, choices=["None", "Euclid", "Lovelace", "Dijkstra", "Turing"], default="None", required = False, help="If included, game will be against the computer of the specified difficulty")
	return parser

def main():
	# parse command line arguments
	parser = build_parser()
	args = parser.parse_args()

	if args.setup:
		configure_players()

	if args.list_commands:
		show_commands()

	if not args.adversary.lower() == 'none':
		compose_adversary(args.adversary)
	else:
		global against_adversary
		against_adversary = False

	# define game board
	global tiles
	tiles = tiles + [0]*64

	# fill initial 4 spaces on board
	tiles[27] = 2
	tiles[28] = 1
	tiles[35] = 1
	tiles[36] = 2

	# intro
	print("Welcome to Othello!")

	# start main game loop
	if args.adversary.lower() == 'none':
		game_loop()
	else:
		adversary_game_loop(args.adversary)

def compose_adversary(adversary):
	global adversary_name
	global adversary_color
	global against_adversary
	against_adversary = True
	global player_one_name
	global player_one_color
	response = input("So, you'd like to challenge {}? (Y/N) ".format(adversary))
	if response.lower().strip() == 'y' or response.lower().strip() == 'yes':

		# player info
		potential_name = input("What is your name? ")
		response = input("Okay, so your name is {}? (Y/N) ".format(potential_name))
		while not response.lower().strip() == 'y' and not response.lower().strip() == 'yes':
			potential_name = input("Please enter your name: ")
			response = input("Okay, so your name is {}? (Y/N) ".format(potential_name))
		player_one_name = potential_name

		potential_color = input("Okay, what is your color? You can pick from {}, {}, {}, {}, {}, {}, {}, or white: ".format(
			grey("grey"),
			red("red"),
			green("green"),
			yellow("yellow"),
			blue("blue"),
			pink("pink"),
			teal("teal")
		))
		response = input("Okay so your color is {}? (Y/N) ".format(color(potential_color.lower(), potential_color)))
		while not response.lower().strip() == 'y' and not response.lower().strip() == 'yes':
			potential_color = input("Please enter your color: ")
			response = input("Okay, so your color is {}? (Y/N) ".format(color(potential_color.lower(), potential_color)))
		player_one_color = potential_color

		# adversary info
		adversary_name = adversary
		colors = ['red', 'green', 'grey', 'yellow', 'blue', 'pink', 'teal']
		if player_one_color in colors:
			colors.remove(player_one_color)
		adversary_color = random.choice(colors)
	else:
		print("Very well, better luck next time")
		sys.exit(0)


def print_board_with_hints(player):
	# determine possible moves
	temp_board = [0]*64
	for index in range(64):
		if is_valid_move(index, player) and tiles[index] == 0:
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
				text = color(player_one_color, "*")
			elif temp_board[index] == 2:
				if against_adversary:
					text = color(adversary_color, "*")
				else:
					text = color(player_two_color, "*")
			else:
				text = flashing(white("*"))
			
			print("{} ".format(text), end='', flush=True)
		print("")
	if player == 1:
		player_name = color(player_one_color, player_one_name)
	else:
		player_name = color(player_two_color, player_two_name)
	print("{}, you can move to any of the above {}".format(player_name, flashing("flashing locations")))

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
				text = color(player_one_color, "*")
			elif tiles[index] == 2:
				if against_adversary:
					text = color(adversary_color, "*")
				else:
					text = color(player_two_color, "*")
			else:
				# error
				pass
			
			print("{} ".format(text), end='', flush=True)
		print("")

def configure_players():
	global player_one_name
	global player_one_color
	global player_two_name
	global player_two_color

	# player one
	potential_name = input("Hi there, what is player one's name? ")
	response = input("Okay, so your name is {}? (Y/N) ".format(potential_name))
	while not response.lower().strip() == 'y' and not response.lower().strip() == 'yes':
		potential_name = input("Please enter player one's name: ")
		response = input("Okay, so your name is {}? (Y/N) ".format(potential_name))
	player_one_name = potential_name

	potential_color = input("Okay, what is {}'s color? You can pick from {}, {}, {}, {}, {}, {}, {}, or white: ".format(
		player_one_name, 
		grey("grey"),
		red("red"),
		green("green"),
		yellow("yellow"),
		blue("blue"),
		pink("pink"),
		teal("teal")
	))
	response = input("Okay so {}'s color is {}? (Y/N) ".format(player_one_name, color(potential_color.lower(), potential_color)))
	while not response.lower().strip() == 'y' and not response.lower().strip() == 'yes':
		potential_color = input("Please enter {}'s color: ".format(player_one_name))
		response = input("Okay, so {}'s color is {}? (Y/N) ".format(player_one_name, color(potential_color.lower(), potential_color)))
	player_one_color = potential_color

	# player two
	print("")
	potential_name = input("And now what is player two's name? ")
	response = input("Okay, so your name is {}? (Y/N) ".format(potential_name))
	while not response.lower().strip() == 'y' and not response.lower().strip() == 'yes':
		potential_name = input("Please enter player two's name: ")
		response = input("Okay, so your name is {}? (Y/N) ".format(potential_name))
	player_two_name = potential_name

	potential_color = input("Okay, what is {}'s color? You can pick from {}, {}, {}, {}, {}, {}, {}, or white: ".format(
		player_two_name, 
		grey("grey"),
		red("red"),
		green("green"),
		yellow("yellow"),
		blue("blue"),
		pink("pink"),
		teal("teal")
	))
	response = input("Okay so {}'s color is {}? (Y/N) ".format(player_two_name, color(potential_color.lower(), potential_color)))
	if potential_color == player_one_color:
		response = 'no'
		print("Sorry, {} is already using {} for their color".format(player_one_name, color(player_one_color, player_one_color)))
	while not response.lower().strip() == 'y' and not response.lower().strip() == 'yes':
		potential_color = input("Please enter {}'s color: ".format(player_two_name))
		response = input("Okay, so {}'s color is {}? (Y/N) ".format(player_two_name, color(potential_color.lower(), potential_color)))
		if potential_color == player_one_color and (response.lower() == 'yes' or response.lower() == 'y'):
			response = 'no'
			print("Sorry, {} is already using {} for their color".format(player_one_name, player_one_color))
	player_two_color = potential_color

if __name__ == '__main__':
	main()