import csv
import random
import time

from utils import BOARD_SIZE, board_to_string, data_path, empty_board, load_ships, render_board

PLAYER_COLOR = "\033[92m"
BOT_COLOR = "\033[94m"
RESET_COLOR = "\033[0m"


def format_coord(coord):
    if coord is None:
        return ""
    x, y = coord
    return f"{x},{y}"


def build_board(ships, show_ships=False):
    grid = empty_board(".")
    ship_sets = [set(ship) for ship in ships]
    coord_to_ship = {}
    for idx, ship in enumerate(ship_sets):
        for coord in ship:
            coord_to_ship[coord] = idx
            if show_ships:
                x, y = coord
                grid[y][x] = "S"
    return {
        "ships": ship_sets,
        "coord_to_ship": coord_to_ship,
        "hits": [set() for _ in ships],
        "sunk": [False for _ in ships],
        "grid": grid,
        "shots": set(),
    }


def add_surrounding_misses(board, ship_cells):
    for cx, cy in ship_cells:
        for nx in range(cx - 1, cx + 2):
            for ny in range(cy - 1, cy + 2):
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                    if board["grid"][ny][nx] in ("H", "X"):
                        continue
                    board["grid"][ny][nx] = "M"
                    board["shots"].add((nx, ny))


def apply_shot(board, coord):
    if coord in board["shots"]:
        return "repeat"
    board["shots"].add(coord)
    x, y = coord
    if coord in board["coord_to_ship"]:
        ship_idx = board["coord_to_ship"][coord]
        board["hits"][ship_idx].add(coord)
        if len(board["hits"][ship_idx]) == len(board["ships"][ship_idx]):
            board["sunk"][ship_idx] = True
            for cx, cy in board["ships"][ship_idx]:
                board["grid"][cy][cx] = "X"
                board["shots"].add((cx, cy))
            add_surrounding_misses(board, board["ships"][ship_idx])
            return "sunk"
        board["grid"][y][x] = "H"
        return "hit"
    board["grid"][y][x] = "M"
    return "miss"


def all_sunk(board):
    return all(board["sunk"])


def available_targets(board):
    coords = []
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if (x, y) not in board["shots"]:
                coords.append((x, y))
    return coords


def board_snapshot(board):
    return board_to_string(board["grid"])


def board_display(board):
    return render_board(board["grid"])


class BotAI:
    def __init__(self):
        self.active_hits = []
        self.axis = None

    def choose_move(self, target_board):
        if self.axis and self.active_hits:
            move = self._axis_move(target_board)
            if move:
                return move
        if self.active_hits:
            move = self._neighbor_move(target_board)
            if move:
                return move
        return self._random_move(target_board)

    def record_result(self, coord, result):
        if result in ("hit", "sunk") and coord not in self.active_hits:
            self.active_hits.append(coord)
        if result == "sunk":
            self.active_hits.clear()
            self.axis = None
            return
        if len(self.active_hits) >= 2 and self.axis is None:
            x0, y0 = self.active_hits[0]
            x1, y1 = self.active_hits[1]
            if x0 == x1:
                self.axis = (0, 1)
            elif y0 == y1:
                self.axis = (1, 0)

    def _neighbor_move(self, target_board):
        candidates = []
        for hx, hy in self.active_hits:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = hx + dx, hy + dy
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                    if (nx, ny) not in target_board["shots"]:
                        candidates.append((nx, ny))
        if not candidates:
            return None
        return random.choice(candidates)

    def _axis_move(self, target_board):
        if not self.axis:
            return None
        dx, dy = self.axis
        if dx != 0:
            hits_sorted = sorted(self.active_hits, key=lambda c: c[0])
        else:
            hits_sorted = sorted(self.active_hits, key=lambda c: c[1])
        first = hits_sorted[0]
        last = hits_sorted[-1]
        forward = (last[0] + dx, last[1] + dy)
        backward = (first[0] - dx, first[1] - dy)
        for candidate in (forward, backward):
            cx, cy = candidate
            if 0 <= cx < BOARD_SIZE and 0 <= cy < BOARD_SIZE:
                if (cx, cy) not in target_board["shots"]:
                    return candidate
        return None

    def _random_move(self, target_board):
        options = available_targets(target_board)
        return random.choice(options)


def reset_game_state(path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "turn",
                "player_move",
                "player_result",
                "bot_move",
                "bot_result",
                "player_board",
                "bot_board",
            ]
        )


def record_state(
    path,
    turn,
    player_move,
    player_result,
    bot_move,
    bot_result,
    player_board,
    bot_board,
):
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                turn,
                format_coord(player_move),
                player_result,
                format_coord(bot_move),
                bot_result,
                board_snapshot(player_board),
                board_snapshot(bot_board),
            ]
        )


def print_boards(player_board, bot_board):
    print_player_board(player_board)
    print()
    print_bot_board(bot_board)


def print_player_board(player_board):
    print(PLAYER_COLOR + "Your board:" + RESET_COLOR)
    print(PLAYER_COLOR + board_display(player_board) + RESET_COLOR)


def print_bot_board(bot_board):
    print(BOT_COLOR + "Bot board:" + RESET_COLOR)
    print(BOT_COLOR + board_display(bot_board) + RESET_COLOR)


def prompt_player_move(bot_board):
    while True:
        raw = input("Enter target as 'x y' (0-9 0-9): ").strip()
        parts = raw.replace(",", " ").split()
        if len(parts) != 2 or not all(p.isdigit() for p in parts):
            print("Invalid input, expected two numbers like '3 7'")
            continue
        x, y = int(parts[0]), int(parts[1])
        if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
            print("Coordinates out of bounds, try again")
            continue
        if (x, y) in bot_board["shots"]:
            print("You already tried that cell, pick another")
            continue
        return (x, y)


def play():
    player_ships = load_ships(data_path("player_ships.csv"))
    bot_ships = load_ships(data_path("bot_ships.csv"))
    player_board = build_board(player_ships, show_ships=True)
    bot_board = build_board(bot_ships, show_ships=False)
    bot_ai = BotAI()
    game_state_path = data_path("game_state.csv")
    reset_game_state(game_state_path)

    turn = 1
    print("Starting Battleship!")
    print_boards(player_board, bot_board)

    while True:
        player_move = prompt_player_move(bot_board)
        player_result = apply_shot(bot_board, player_move)
        print(f"You fired at {format_coord(player_move)} -> {player_result}")
        print_bot_board(bot_board)
        record_state(
            game_state_path,
            turn,
            player_move,
            player_result,
            None,
            "",
            player_board,
            bot_board,
        )
        turn += 1

        if all_sunk(bot_board):
            print("You win! All bot ships destroyed.")
            break

        if player_result in ("hit", "sunk"):
            continue

        while True:
            bot_move = bot_ai.choose_move(player_board)
            bot_result = apply_shot(player_board, bot_move)
            bot_ai.record_result(bot_move, bot_result)
            print(f"Bot fired at {format_coord(bot_move)} -> {bot_result}")
            print_player_board(player_board)
            record_state(
                game_state_path,
                turn,
                None,
                "",
                bot_move,
                bot_result,
                player_board,
                bot_board,
            )
            turn += 1
            if all_sunk(player_board):
                print("Bot wins! Your fleet is sunk.")
                return
            if bot_result not in ("hit", "sunk"):
                break
            time.sleep(1)


if __name__ == "__main__":
    play()
