How to run: plain Python 3, no extra libraries. Just `python main.py`.

How input works: 
in the console I type a line like `size x y direction`, for example `3 4 5 n`. 
Size can be 1,2,3,4, coordinates 0..9, direction n/e/s/w. 
ship_input keeps asking until all ships are placed.

How placement is validated: 
each ship is built from the start cell and direction; 
it must stay on the 10x10 board and not touch any other ship, even diagonally. 
If it fails, I re-enter. When it passes, it is saved to data/player_ships.csv.

How game state is updated/shown: 
the bot layout is generated with the same rules into data/bot_ships.csv. 
gameplay runs turn by turn and appends to data/game_state.csv 
(turn number, moves, results, board snapshots). 
After each shot it prints the relevant board with symbols . M H X; 
my board is green, the bot board is blue.

Design choices/trade-offs: 
kept code as simple as possible, avoided type hints and heavy classes, 
used dicts/lists for the boards. 
Bot shoots randomly, then after a hit tries neighbors and along the line. 
CSV files are used because they are easy to read by eye.
