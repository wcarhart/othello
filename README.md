# othello
Command line implementation of the board game [Othello](https://en.wikipedia.org/wiki/Reversi) (also known as Reversi).

## Install and setup
Simply clone or download this repo, and make sure you're using [Python 3](https://docs.python-guide.org/starting/installation/).

## Usage
Run a simple game of othello with:
```
python3 othello.py
```

Use the `-h` option for the full help menu: `python3 othello.py -h` or `python3 othello.py --help`
```
usage: othello.py [-h] [--setup] [--list-commands]
                  [--adversary {None,Euclid,Lovelace,Dijkstra,Turing} | --spectate]

optional arguments:
  -h, --help            show this help message and exit
  --setup               Set up player configuration before starting the game
                        (default: False)
  --list-commands       Show the available commands you can type during the
                        game (default: False)
  --adversary {None,Euclid,Lovelace,Dijkstra,Turing}
                        If included, game will be against the computer of the
                        specified difficulty (default: None)
  --spectate            If included, human will spectate to specified
                        adversaries (default: False)
   
```

**`--setup`**

Allows the user to set up players' names and colors, so they are not the default of `Player 1` (Red) and `Player 2` (Green).

**`--list-commands`**

Show the available commands as the game begins:
```
====Command list====
 B6     -> attempts to place new tile on location B6
 show   -> redraws the current board
 where  -> shows possible moves for the current player (you can also use 'hint' or 'where can I go?')
 help   -> shows this menu and list of commands (you can also use 'command' or 'commands')
 clear  -> clears the screen
 score  -> show how many tiles each player has (you can also use 'who's winning?')
 color  -> changes the current player's color
 exit   -> ends the game (you can also use 'done')
```

**`--adversary`**

Allows the user to play a computer adversary rather than another human player:
 * `Euclid` - Novice
 * `Lovelace` - Easy
 * `Dijkstra` - Medium
 * `Turing` - Hard
 
**`--spectate`**

Allows the user to spectate a match between two computer adversaries.
