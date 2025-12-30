# Classic Battleship (CLI)

A console **Battleship** game written in pure Python: manual ship placement, a bot with random search and hit-focused targeting, and state saving to CSV.

## Features

* 10×10 board, classic fleet layout: 1×4, 2×3, 3×2, 4×1 cells.
* Placement validation: ships stay within the board and do not touch each other, even diagonally.
* Colored boards in the terminal: green — yours, blue — the bot’s; symbols `.`, `M`, `H`, `X`.
* The bot fires randomly, and after a hit it finishes ships by checking neighbors and extending along the detected axis.
* All actions are logged to CSV files for easy reading or analysis.

## Requirements

* Python 3, no additional packages required.

## Running the Game

* Go to the project root and make sure the `data/` folder exists (create it if needed).
* Run `python main.py`.
* If `data/player_ships.csv` exists, the game will ask whether to use it or place ships again.

## Ship Placement

* Input format: `size x y direction`, e.g. `3 4 5 n`.
* `size`: 1/2/3/4; coordinates `x, y`: 0..9; `direction`: `n`/`e`/`s`/`w`.
* On formatting errors, out-of-bounds placement, or touching another ship, the program will ask for input again.

## Gameplay

* Fire with: `x y` (e.g. `2 7`). Repeated cells are not accepted.
* After each shot, the corresponding board is shown:

  * `.` — unknown
  * `M` — miss
  * `H` — hit
  * `X` — sunk (with surrounding cells marked)
* The bot continues shooting while it hits; the winner is the one who sinks all opponent ships first.

## Data Files

* `data/player_ships.csv` — your ship coordinates.
* `data/bot_ships.csv` — the bot’s layout (generated on each run).
* `data/game_state.csv` — turn number, shot coordinates and results, board snapshots.

## Project Structure

* `main.py` — entry point and choice of using saved placement.
* `src/ship_input.py` — user input handling and placement validation.
* `src/bot_generation.py` — bot ship placement generation using the same rules.
* `src/gameplay.py` — game loop, bot logic, board rendering, and state logging.
* `src/utils.py` — shared utilities (validation, rendering, CSV handling).

## Good to Know

* CSV files are ignored by Git (`.gitignore`); you can delete them to fully reset the game state.
* Logic and data are separated: placements and move history are saved independently and are easy to inspect manually.
