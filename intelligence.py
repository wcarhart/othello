import sys
import random
import othello

def acquire_move_from_intelligence(tiles, adversary, adversary_color):
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
	print("{} is thinking...".format(othello.color(adversary_color, "Euclid")))

	potential_moves = []
	for index in range(64):
		if othello.is_valid_move(index, 2, new=True, b=tiles) and tiles[index] == 0:
			potential_moves.append(index)

	move = random.choice(potential_moves)
	print("{} moved to {}!".format(othello.color(adversary_color, "Euclid"), othello.get_coordinate_from_index(move)))
	return move

def lovelace(tiles, adversary_color):
	return

def dijkstra(tiles, adversary_color):
	return

def turing(tiles, adversary_color):
	return