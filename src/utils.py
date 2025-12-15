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

def get_ship_coords(size, x, y, direction):
    x = int(x)
    y = int(y)
    dx = 0
    dy = 0
    match direction:
        case 'n':
            dy = -1
        case 's':
            dy = 1
        case 'e':
            dx = 1
        case 'w':
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

def save_ships(ships, path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["size", "coords"])
        for coords in ships:
            size = len(coords)
            coords_str = " ".join(f"({x};{y})" for x, y in coords)
            writer.writerow([size, coords_str])
