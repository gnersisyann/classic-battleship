import csv
from pathlib import Path

BOARD_SIZE = 10

SIZE_1_COUNT = 4
SIZE_2_COUNT = 3
SIZE_3_COUNT = 2
SIZE_4_COUNT = 1

SHIP_SIZES = {
    1: SIZE_1_COUNT,
    2: SIZE_2_COUNT,
    3: SIZE_3_COUNT,
    4: SIZE_4_COUNT,
}

SHIP_LAYOUT = [size for size in (4, 3, 2, 1) for _ in range(SHIP_SIZES[size])]

def data_path(filename):
    base = Path(__file__).resolve().parents[1]
    return base / "data" / filename

def save_ships(ships, path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["size", "coords"])
        for coords in ships:
            size = len(coords)
            coords_str = " ".join(f"({x};{y})" for x, y in coords)
            writer.writerow([size, coords_str])


def load_ships(path):
    ships = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw = row["coords"]
            coords = []
            for pair in raw.split():
                cleaned = pair.strip("()")
                if not cleaned:
                    continue
                x_str, y_str = cleaned.split(";")
                coords.append((int(x_str), int(y_str)))
            ships.append(coords)
    return ships


def get_ship_coords(size, x, y, direction):
    x = int(x)
    y = int(y)
    dx = dy = 0
    if direction == "n":
        dy = -1
    elif direction == "s":
        dy = 1
    elif direction == "e":
        dx = 1
    elif direction == "w":
        dx = -1

    coords = []
    for i in range(size):
        cx = x + dx * i
        cy = y + dy * i
        if cx < 0 or cx >= BOARD_SIZE or cy < 0 or cy >= BOARD_SIZE:
            return None
        coords.append((cx, cy))
    return coords


def is_valid_ship(coords, occupied):
    for cx, cy in coords:
        for nx in range(cx - 1, cx + 2):
            for ny in range(cy - 1, cy + 2):
                if (nx, ny) in occupied:
                    return False
    return True


def empty_board(fill="."):
    return [[fill for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def board_to_string(board):
    return "".join("".join(row) for row in board)


def render_board(board):
    top = "    " + " ".join(str(i) for i in range(BOARD_SIZE))
    lines = [top]
    for y, row in enumerate(board):
        lines.append(f"{y:2} |" + " ".join(row))
    return "\n".join(lines)


def render_occupied(occupied):
    board = empty_board(".")
    for x, y in occupied:
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            board[y][x] = "S"
    return render_board(board)
