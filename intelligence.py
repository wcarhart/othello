import sys
import random
import othello
import time

CORNERS = [0, 7, 56, 63]
X_SQUARES = [9, 14, 49, 54]
C_SQUARES = [1, 6, 8, 15, 48, 55, 57, 62]
SWEET_16 = [18, 19, 20, 21, 26, 27, 28, 29, 34, 35, 36, 37, 42, 43, 44, 45]
NORTH_EDGES = [0, 1, 2, 3, 4, 5, 6, 7]
SOUTH_EDGES = [56, 57, 58, 59, 60, 61, 62, 63]

def acquire_move_from_intelligence(tiles, adversary, adversary_color):
	"""Switch on which AI we're using"""

	if adversary.lower() == 'euclid':
		return euclid(tiles, adversary_color)
	elif adversary.lower() == 'lovelace':
		return lovelace(tiles, adversary_color)
	elif adversary.lower() == 'dijkstra':
		return dijkstra(tiles, adversary_color)
	elif adversary.lower() == 'turing':
		return turing(tiles, adversary_color)
	else:
		return -1

def euclid(tiles, adversary_color):
	"""Simple AI, makes a random move from its potential moves"""

	print("{} is thinking...".format(othello.color(adversary_color, "Euclid")))
	time.sleep(2)

	potential_moves = []
	for index in range(64):
		if othello.is_valid_move(index, 2, adversary=True, b=tiles) and tiles[index] == 0:
			potential_moves.append(index)

	move = random.choice(potential_moves)
	print("{} moved to {}!".format(othello.color(adversary_color, "Euclid"), othello.get_coordinate_from_index(move)))
	time.sleep(2)
	return move

def lovelace(tiles, adversary_color):
	"""Easy AI, makes a move that maximizes its number of pieces on the board"""

	print("{} is thinking...".format(othello.color(adversary_color, "Ada Lovelace")))
	time.sleep(2)
	
	potential_moves = []
	for index in range(64):
		if othello.is_valid_move(index, 2, adversary=True, b=tiles) and tiles[index] == 0:
			potential_moves.append(index)

	best_move = 0
	best_total = 0
	for move in potential_moves:
		copy = [tile for tile in tiles]
		board = othello.propogate_flips(move, 2, adversary=True, b=copy)
		number_of_tiles = len([tile for tile in board if tile == 2])
		if number_of_tiles > best_total:
			best_total = number_of_tiles
			best_move = move

	print("{} moved to {}!".format(othello.color(adversary_color, "Ada Lovelace"), othello.get_coordinate_from_index(best_move)))
	time.sleep(2)
	return best_move

def dijkstra(tiles, adversary_color):
	"""Medium AI, makes a move that minimizes the other player's mobility"""
	# mobility is defined as the other player's possible moves

	print("{} is thinking...".format(othello.color(adversary_color, "Edsger Dijkstra")))
	time.sleep(2)

	potential_moves = []
	for index in range(64):
		if othello.is_valid_move(index, 2, adversary=True, b=tiles) and tiles[index] == 0:
			potential_moves.append(index)

	best_move = 0
	worst_mobility = sys.maxsize
	for move in potential_moves:
		copy = [tile for tile in tiles]
		board = othello.propogate_flips(move, 2, adversary=True, b=copy)
		mobility = len([index for index in range(64) if othello.is_valid_move(index, 1, adversary=True, b=board) and board[index] == 0])
		if mobility < worst_mobility:
			worst_mobility = mobility
			best_move = move

	print("{} moved to {}!".format(othello.color(adversary_color, "Edsger Dijkstra"), othello.get_coordinate_from_index(best_move)))
	time.sleep(2)
	return best_move

def turing(tiles, adversary_color):
	"""Hard AI, makes a move that minimizes the other player's mobility, maximizes its own mobility, and avoids giving the other user corners"""

	# Priorities:
	#  1. If corner is available, take it
	#  2. If a move gives opponent a corner, don't consider it (unless necessary)
	#  3. Don't play in C Squares (unless necessary)
	#  4. Maximize our mobility
	#  5. Minimize opponent's mobility
	#  6. Control the sweet 16

	# If you wanted to improve this more, here are other, not currently, explicitly implemented considerations:
	#  - consider interior vs. frontior disks
	#  - consider A- and B-squares (prioritize taking wall moves more)
	#  - consider power moves/attacks for taking corners
	
	print("{} is thinking...".format(othello.color(adversary_color, "Alan Turing")))
	time.sleep(2)

	potential_moves = []
	for index in range(64):
		if othello.is_valid_move(index, 2, adversary=True, b=tiles) and tiles[index] == 0:
			potential_moves.append(index)

	# STEP 1
	# determine if moves could give opponent a corner
	bad_corner_moves = []
	for move in potential_moves:
		copy = [tile for tile in tiles]
		board = othello.propogate_flips(move, 2, adversary=True, b=copy)

		if not len([index for index in range(64) if othello.is_valid_move(index, 1, adversary=True, b=board) and board[index] == 0 and index in CORNERS]) == 0:
			bad_corner_moves.append(move)
			
	# determine if can get a corner right now
	good_corner_moves = []
	for move in potential_moves:
		if move in CORNERS:
			good_corner_moves.append(move)

	# STEP 2
	# begin evaluating move candidates to find best move
	best_move = -1
	if not len(good_corner_moves) == 0:
		# we can take a corner
		most_tiles = 0
		best_move = good_corner_moves[0]
		for corner_move in good_corner_moves:
			copy = [tile for tile in tiles]
			board = othello.propogate_flips(move, 2, adversary=True, b=copy)
			number_of_tiles = len([tile for tile in board if tile == 2])
			if number_of_tiles > most_tiles:
				most_tiles = number_of_tiles
				best_move = corner_move
	else:
		# we can't take a corner
		good_moves = [move for move in potential_moves if not move in bad_corner_moves and not move in X_SQUARES and not move in C_SQUARES]
		if len(good_moves) == 0:
			good_moves = [move for move in potential_moves if not move in bad_corner_moves and not move in X_SQUARES]
			if len(good_moves) == 0:
				good_moves = [move for move in potential_moves if not move in bad_corner_moves]
				if len(good_moves) == 0:
					good_moves = potential_moves

		# begin mobility score calculation
		temp_mobility_scores = {}
		max_my_mobility = 0
		min_your_mobility = sys.maxsize
		max_sweet_score = 0

		# go through all moves and calculate increases in my mobility and decreases in your mobility
		for move in good_moves:
			copy = [tile for tile in tiles]
			board = othello.propogate_flips(move, 2, adversary=True, b=copy)

			temp_my_mobility = calculate_my_mobility(board, 2)
			max_my_mobility = temp_my_mobility if temp_my_mobility > max_my_mobility else max_my_mobility

			temp_your_mobility = calculate_your_mobility(board, 1)
			min_your_mobility = temp_your_mobility if temp_your_mobility < min_your_mobility else min_your_mobility

			temp_sweet_score = calculate_sweet_16_score(board, 2)
			max_sweet_score = temp_sweet_score if temp_sweet_score > max_sweet_score else max_sweet_score

			temp_mobility_scores[move] = (temp_my_mobility, temp_your_mobility, temp_sweet_score)

		# bound mobility scores between 0 and 1
		mobility_scores = {}
		for move, scores in temp_mobility_scores.items():
			mobility_scores[move] = ((scores[0]/max_my_mobility), (scores[1]/min_your_mobility), (scores[2])/max_sweet_score)

		# give each move a final mobility score to rank them
		best_move = 0
		best_mobility_score = 0
		for move, scores in mobility_scores.items():
			# weighted sum: 50% my increased mobility, 25% your decreased mobility, 25% sweet 16 control increase
			mobility_score = (0.5 * scores[0]) + (0.25 * scores[1]) + (0.25 * scores[2])
			if mobility_score > best_mobility_score:
				best_move = move
				best_mobility_score = mobility_score

	if best_move == -1:
		print("ERROR: Alan Turing couldn't find a move!")
		sys.exit(0)

	print("{} moved to {}!".format(othello.color(adversary_color, "Alan Turing"), othello.get_coordinate_from_index(best_move)))
	time.sleep(2)
	return best_move

def calculate_sweet_16_score(board, player):
	score = 0
	for tile in SWEET_16:
		if board[tile] == player:
			score += 1
	return score

def calculate_my_mobility(board, player):
	mobility = len([index for index in range(64) if othello.is_valid_move(index, player, adversary=True, b=board) and board[index] == 0])
	return mobility

def calculate_your_mobility(board, player):
	mobility = len([index for index in range(64) if othello.is_valid_move(index, player if player == 2 else 1, adversary=True, b=board) and board[index] == 0])
	return mobility
