"""
Command line implementation of the game Othello (also known as Reversi)
"""

import sys
import argparse
import random
import intelligence

# constants
tiles = []
WEST_EDGES = [0, 8, 16, 24, 32, 40, 48, 56]
EAST_EDGES = [7, 15, 23, 31, 39, 47, 55]

player_one_name = "Player 1"
player_one_color = "red"
player_two_name = "Player 2"
player_two_color = "green"
adversary_name = ""
adversary_color = ""

# converts text to flashing
def flashing(text):
	return "\033[5m{}\033[0m".format(text)

# converts text to grey 
def grey(text):
	return "\033[90m{}\033[0m".format(text)

# converts text to red
def red(text):
	return "\033[91m{}\033[0m".format(text)

# converts text to green
def green(text):
	return "\033[92m{}\033[0m".format(text)

# converts text to yellow
def yellow(text):
	return "\033[93m{}\033[0m".format(text)

# converts text to blue
def blue(text):
	return "\033[94m{}\033[0m".format(text)

# converts text to pink
def pink(text):
	return "\033[95m{}\033[0m".format(text)

# converts text to teal
def teal(text):
	return "\033[96m{}\033[0m".format(text)

# converts text to white
def white(text):
	return "\033[97m{}\033[0m".format(text)

def color(color, text):
	"""Changes color of provided texted to a specified color"""
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

def spectate_game_loop():
	"""Game loop for spectating"""

	# set up players
	name_one = color(player_one_color, player_one_name)
	name_two = color(player_two_color, player_two_name)
	print("{} vs. {}".format(name_one, name_two))
	print("{} says: {}".format(name_one, get_taunts(player_one_name, 'start')))
	print("{} says: {}".format(name_two, get_taunts(player_two_name, 'start')))

	turn = 1
	game_over = False
	while not game_over:
		# print board for user to see
		print_board()

		if has_any_moves(turn):
			if turn == 1:
				move = intelligence.acquire_move_from_intelligence(tiles, player_one_name, player_one_color, player=turn)
			else:
				move = intelligence.acquire_move_from_intelligence(tiles, player_two_name, player_two_color, player=turn)
		else:
			turn = 1 if turn == 2 else 2
			if has_any_moves(turn):
				if turn == 1:
					player_name = color(player_one_color, player_one_name)
					print("Sorry {}, you don't have any moves left!".format(player_name))
					move = intelligence.acquire_move_from_intelligence(tiles, player_two_name, player_two_color, player=turn)
				else:
					player_name = color(player_two_color, player_two_name)
					print("Sorry {}, you don't have any moves left!".format(player_name))
					move = intelligence.acquire_move_from_intelligence(tiles, player_one_name, player_one_color, player=turn)
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
		adversary_score = len([tile for tile in tiles if tile == 2])
		if player_one_score > player_two_score:
			print("{} wins!".format(color(player_one_color, player_one_name)))
			print("{} says: {}".format(color(player_one_color, player_one_name), get_taunts(player_one_name, 'lose')))
		elif player_two_score > player_one_score:
			print("{} wins!".format(color(player_two_color, player_two_name)))
			print("{} says: {}".format(color(player_two_color, player_two_name), get_taunts(player_two_name, 'win')))
		else:
			print("It's a tie!")
		print("  {}'s score: {}".format(color(player_one_color, player_one_name), player_one_score))
		print("  {}'s score: {}".format(color(player_two_color, player_two_name), player_two_score))

def adversary_game_loop(adversary):
	"""Game loop for one human player and one computer adversary"""
	player_name = color(player_one_color, player_one_name)
	print("{} vs. {}".format(color(player_one_color, player_one_name), color(adversary_color, adversary_name)))
	print("{} says: {}".format(color(adversary_color, adversary_name), get_taunts(adversary, 'start')))

	turn = 1
	game_over = False
	while not game_over:
		# print board for player to see
		print_board()

		if turn == 1:
			if has_any_moves(turn):
				move = acquire_move(turn)
			else:
				turn = 2
				if has_any_moves(turn):
					print("Sorry {}, you don't have any moves left!".format(player_name))
					move = intelligence.acquire_move_from_intelligence(tiles, adversary, adversary_color)
				else:
					game_over = True
					break
		else:
			move = intelligence.acquire_move_from_intelligence(tiles, adversary, adversary_color)

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
		adversary_score = len([tile for tile in tiles if tile == 2])
		if player_one_score > adversary_score:
			print("{} wins!".format(color(player_one_color, player_one_name)))
			print("{} says: {}".format(color(adversary_color, adversary_name), get_taunts(adversary, 'lose')))
		elif adversary_score > player_one_score:
			print("{} wins!".format(color(adversary_color, adversary_name)))
			print("{} says: {}".format(color(adversary_color, adversary_name), get_taunts(adversary, 'win')))
		else:
			print("It's a tie!")
		print("  {}'s score: {}".format(color(player_one_color, player_one_name), player_one_score))
		print("  {}'s score: {}".format(color(adversary_color, adversary_name), adversary_score))

def get_taunts(adversary, state):
	"""Returns a taunt based on the computer adversary and game state"""
	if state == 'start':
		if adversary.lower() == 'euclid':
			return "The Euclidian algorithm isn't the only one I know!"
		elif adversary.lower() == 'lovelace':
			return "My Difference Engine is ready to compute your defeat!"
		elif adversary.lower() == 'dijkstra':
			return "I'll find the quickest path to your defeat!"
		elif adversary.lower() == 'turing':
			return "My bombes will win this game in no time!"
	elif state == 'win':
		if adversary.lower() == 'euclid':
			return "Looks like you need to go back to geometry!"
		elif adversary.lower() == 'lovelace':
			return "You wouldn't even be a match for my dear Charles Babbage!"
		elif adversary.lower() == 'dijkstra':
			return "Looks like you need an easier opponent, try playing Bellman and Ford!"
		elif adversary.lower() == 'turing':
			return "How you even fathomed the idea that you could beat me is an enigma!"
	elif state == 'lose':
		if adversary.lower() == 'euclid':
			return "Guess I better stick to philosophy!"
		elif adversary.lower() == 'lovelace':
			return "I'll have to attempt this challenge again on a better Analytical Engine!"
		elif adversary.lower() == 'dijkstra':
			return "Well, I guess I was being a little greedy!"
		elif adversary.lower() == 'turing':
			return "Nonsense, I must return to Bletchley at once to continue my research on this wretched game!"

def game_loop():
	"""Main game loop for a regular game"""
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
	"""Determines if a specified player has any valid moves"""
	temp_board = [0]*64
	for index in range(64):
		if is_valid_move(index, player) and tiles[index] == 0:
			return True
	return False

def update_game(move, turn):
	"""Updates the game based on a certain move"""

	# add new tile to board
	tiles[move] = turn

	# update tiles already on board
	propogate_flips(move, turn)

def get_index_from_coordinate(coordinate):
	"""Converts numeric index to board coordinate"""
	row = coordinate[0].lower()
	col = coordinate[1]
	rows = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
	col_index = int(col)
	row_index = rows.index(row)
	index = (row_index*8 + col_index) - 1
	return index

def get_coordinate_from_index(index):
	"""Converts board coordinate to numeric index"""
	coordinate = ''
	tens = index // 8
	if tens == 0:
		coordinate += 'A'
	elif tens == 1:
		coordinate += 'B'
	elif tens == 2:
		coordinate += 'C'
	elif tens == 3:
		coordinate += 'D'
	elif tens == 4:
		coordinate += 'E'
	elif tens == 5:
		coordinate += 'F'
	elif tens == 6:
		coordinate += 'G'
	elif tens == 7:
		coordinate += 'H'

	ones = (index+1) % 8
	coordinate += str(ones)

	return coordinate

def propogate_flips(move, player, adversary=False, b=[]):
	"""Propogate flips as a result of a move"""

	# go in all eight directions and look for another piece of the same color as `turn`
	# if we find one, flip all in between, if we don't, move on

	to_flip = []

	if adversary:
		board = b
	else:
		board = tiles

	# west
	index = move - 1
	candidates = []
	while index < 64 and index > -1:
		candidate = board[index]
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
		candidate = board[index]
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
		candidate = board[index]
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
		candidate = board[index]
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
		candidate = board[index]
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
		candidate = board[index]
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
		candidate = board[index]
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
		candidate = board[index]
		if candidate == 0:
			break
		if not candidate == player:
			candidates.append(index)
		elif candidate == player:
			to_flip += candidates
			break
		index += 7

	if adversary:
		return mock_flip(b, to_flip)
	else:
		flip(to_flip)

def flip(indices):
	"""Flip a specific set of tiles"""
	for index in indices:
		tiles[index] = 1 if tiles[index] == 2 else 2

def mock_flip(board, indices):
	"""Return a copy of the board with specific tiles flipped"""
	for index in indices:
		board[index] = 1 if board[index] == 2 else 2
	return board

def check_game_status():
	"""CHeck if game has ended or not"""
	empty_spaces = len([tile for tile in tiles if tile == 0])
	if empty_spaces == 0:
		return True
	else:
		return False

def change_color(player):
	"""Change a player's color"""
	global player_one_color
	global player_one_name
	global player_two_color
	global player_two_name
	if player == 1:
		player_name = color(player_one_color, player_one_name)
	else:
		player_name = color(player_two_color, player_two_name)

	response = input("{}, would you like to change your color? (Y/N) ".format(player_name))
	if response.lower().strip() == 'n' or response.lower().strip() == 'no':
		return
	else:
		response = 'no'
	while not response.lower().strip() == 'y' and not response.lower().strip() == 'yes':
		potential_color = input("Okay, what do you want your color to be? You can pick from {}, {}, {}, {}, {}, {}, {}, or white: ".format(
			grey("grey"),
			red("red"),
			green("green"),
			yellow("yellow"),
			blue("blue"),
			pink("pink"),
			teal("teal")
		))
		response = input("Okay, so you'd like to change your color to {}? (Y/N) ".format(color(potential_color.lower(), potential_color)))
		if adversary_name.lower() == 'none':
			if potential_color == adversary_color and (response.lower() == 'yes' or response.lower() == 'y'):
				response = 'no'
				print("Sorry, {} is already using {} for their color".format(adversary_name, adversary_color))
		else:
			if player == 1:
				if potential_color == player_two_color and (response.lower() == 'yes' or response.lower() == 'y'):
					response = 'no'
					print("Sorry, {} is already using {} for their color".format(player_two_name, player_two_color))
			else:
				if potential_color == player_one_color and (response.lower() == 'yes' or response.lower() == 'y'):
					response = 'no'
					print("Sorry, {} is already using {} for their color".format(player_one_name, player_one_color))

	if player == 1:
		player_one_color = potential_color
	else:
		player_two_color = potential_color

def acquire_move(turn):
	"""Acquire user input and parse command"""
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
		if attempt.lower().strip() == 'where' or attempt.lower().strip().strip('?') == 'where can i go':
			print_board_with_hints(turn)
			continue

		# show commands
		if attempt.lower().strip() == 'help' or attempt.lower().strip() == 'commands' or attempt.lower().strip() == 'command':
			show_commands()
			continue

		# change color
		if attempt.lower().strip() == 'color':
			change_color(turn)
			continue

		# clear screen
		if attempt.lower().strip() == 'clear':
			print(chr(27) + "[2J")
			continue

		# show score
		if attempt.lower().strip() == 'score' or attempt.lower().strip().strip('?') == 'who\'s winning':
			player_one_score = len([tile for tile in tiles if tile == 1])
			player_two_score = len([tile for tile in tiles if tile == 2])
			print("  {}: {}".format(color(player_one_color, player_one_name), player_one_score))
			if adversary_name == "":
				print("  {}: {}".format(color(player_two_color, player_two_name), player_two_score))
			else:
				print("  {}: {}".format(color(adversary_color, adversary_name), player_two_score))
			continue

		# incorrect length
		if not len(attempt) == 2:
			print(" Invalid input, must be in the form of 'xN', where 'x' (row) is a letter between A and H and 'N' (column) is a number between 1 and 8, or type `help` for help")
			continue
		else:
			row = attempt[0].lower()
			col = attempt[1]

			# make sure col is a number
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
	"""Show commands menu during game loop"""
	print("====Command list====")
	print(" B6     -> attempts to place new tile on location B6")
	print(" show   -> redraws the current board")
	print(" where  -> shows possible moves for the current player (you can also use 'hint' or 'where can I go?')")
	print(" help   -> shows this menu and list of commands (you can also use 'command' or 'commands')")
	print(" clear  -> clears the screen")
	print(" score  -> show how many tiles each player has (you can also use 'who's winning?')")
	print(" color  -> changes the current player's color")
	print(" exit   -> ends the game (you can also use 'done')")

def is_valid_move(index, player, adversary=False, b=[]):
	"""Determine if an inputted move is valid for a specific character"""

	# go through each tile on the board, check eight directions and see if there's a valid sandwich

	if adversary:
		board = b
	else:
		board = tiles

	# west
	temp = index - 1
	fillings = 0
	while temp < 64 and temp > -1:
		tile_value = board[temp]
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
		tile_value = board[temp]
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
		tile_value = board[temp]
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
		tile_value = board[temp]
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
		tile_value = board[temp]
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
		tile_value = board[temp]
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
		tile_value = board[temp]
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
		tile_value = board[temp]
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
	"""Build CLI parser"""
	parser = argparse.ArgumentParser(description=__doc__, formatter_class = argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--setup', action='store_true', default=False, required=False, help="Set up player configuration before starting the game")
	parser.add_argument('--list-commands', action='store_true', default=False, required=False, help="Show the available commands you can type during the game")
	group = parser.add_mutually_exclusive_group(required=False)
	group.add_argument('--adversary', type=str, choices=["None", "Euclid", "Lovelace", "Dijkstra", "Turing"], default="None", required=False, help="If included, game will be against the computer of the specified difficulty")
	group.add_argument('--spectate', action='store_true', default=False, required=False, help='If included, human will spectate to specified adversaries')
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

	# TODO: for testing only
	#coordinates = {'e4': 1, 'd5': 1, 'd4': 2, 'e5': 2, 'c5': 2, 'b6': 2}
	#test_configuration(coordinates)

	# intro
	print("\nWelcome to Othello!")

	if args.spectate:
		start_spectate()
	else:
		# start main game loop
		if args.adversary.lower() == 'none':
			game_loop()
		else:
			adversary_game_loop(args.adversary)

def test_configuration(coordinates):
	"""Build a specific game board"""

	# FOR TESTING PURPOSES ONLY
	for coordinate, value in coordinates.items():
		tiles[get_index_from_coordinate(coordinate)] = int(value)

def start_spectate():
	"""Set up spectate mode"""
	global player_one_name
	global player_one_color
	global player_two_name
	global player_two_color

	available_colors = ['red', 'green', 'yellow', 'grey', 'blue', 'teal', 'pink']
	random.shuffle(available_colors)

	valid_response = False
	potential_player = input("Who should be the first player? You can pick from Euclid, Lovelace, Dijkstra, or Turing: ")
	while not valid_response:
		if not (potential_player.lower().strip() == 'euclid' or potential_player.lower().strip() == 'lovelace' or potential_player.lower().strip() == 'dijkstra' or potential_player.lower().strip() == 'turing'):
			valid_response = False
			potential_player = input("Please pick from Euclid, Lovelace, Dijkstra, or Turing: ")
		else:
			valid_response = True
	if potential_player.lower().strip() == 'euclid':
		player_one_name = "Euclid"
	elif potential_player.lower().strip() == 'lovelace':
		player_one_name = "Lovelace"
	elif potential_player.lower().strip() == 'dijkstra':
		player_one_name = "Dijkstra"
	elif potential_player.lower().strip() == 'turing':
		player_one_name = "Turing"
	player_one_color = available_colors[0]

	valid_response = False
	potential_player = input("Who should be the second player? You can pick from Euclid, Lovelace, Dijkstra, or Turing: ")
	while not valid_response:
		if not (potential_player.lower().strip() == 'euclid' or potential_player.lower().strip() == 'lovelace' or potential_player.lower().strip() == 'dijkstra' or potential_player.lower().strip() == 'turing'):
			valid_response = False
			potential_player = input("Please pick from Euclid, Lovelace, Dijkstra, or Turing: ")
		else:
			valid_response = True
	if potential_player.lower().strip() == 'euclid':
		player_two_name = "Euclid"
	elif potential_player.lower().strip() == 'lovelace':
		player_two_name = "Lovelace"
	elif potential_player.lower().strip() == 'dijkstra':
		player_two_name = "Dijkstra"
	elif potential_player.lower().strip() == 'turing':
		player_two_name = "Turing"
	player_two_color = available_colors[1]

	spectate_game_loop()

def compose_adversary(adversary):
	"""Set up computer adversary"""
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
	"""Print board with possible moves flashing"""

	# determine possible moves
	temp_board = [0]*64
	for index in range(64):
		if is_valid_move(index, player) and tiles[index] == 0:
			temp_board[index] = -1
		else:
			temp_board[index] = tiles[index]

	potential_moves = []

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
				potential_moves.append(get_coordinate_from_index(index))
			
			print("{} ".format(text), end='', flush=True)
		print("")

	if player == 1:
		player_name = color(player_one_color, player_one_name)
	else:
		player_name = color(player_two_color, player_two_name)
	print("{}, you can move to any of the above {}".format(player_name, flashing("flashing locations")))
	
	if not len(potential_moves) == 0:
		movelist = ", ".join(potential_moves)
		print("You can move to {}".format(movelist))

def print_board():
	"""Print board"""

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
	"""Set up players if --setup option is used"""
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
