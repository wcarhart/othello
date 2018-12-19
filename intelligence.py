import sys
import random
import othello
import time

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
	"""
	print("{} is thinking...".format(othello.color(adversary_color, "Alan Turing")))
	time.sleep(2)

	potential_moves = []
	for index in range(64):
		if othello.is_valid_move(index, 2, adversary=True, b=tiles) and tiles[index] == 0:
			potential_moves.append(index)
	"""
	return