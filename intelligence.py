import sys

def acquire_move_from_intelligence(tiles, adversary):
	if adversary.lower() == 'euclid':
		return euclid(tiles)
	elif adversary.lower() == 'lovelace':
		return lovelace(tiles)
	elif adversary.lower() == 'dijkstra':
		return dijkstra(tiles)
	elif adversary.lower() == 'turing':
		return turing(tiles)
	else:
		return -1

def euclid(tiles):
	return

def lovelace(tiles):
	return

def dijkstra(tiles):
	return

def turing(tiles):
	return
