import re
from utils import BOARD_SIZE, SHIP_SIZES, save_ships, data_path
from utils import get_ship_coords, is_valid_ship

PATTERN_STRING = r"^(?:1|2|3|4)\s+\d+\s+\d+\s+[nsew]$"


def getinput():
    info = input()
    while not bool(re.fullmatch(PATTERN_STRING, info)):
        print("Invalid input format, try 'size x y direction'")
        info = input()
    return info


def collect_player_ships():
    remaining = SHIP_SIZES.copy()
    inputs = []
    occupied = set()

    print("Input format: size x y direction \n" \
		f"x,y number from [0;{BOARD_SIZE-1}] \n" \
		"direction is character from [n,e,s,w]")

    while sum(remaining.values()) > 0:
        raw = getinput()
        size, x, y, direction = raw.split()
        size = int(size)
        if remaining[size] == 0:
            print(f"All ships of size {size} is placed")
            continue

        coords = get_ship_coords(size, x, y, direction)
        if coords is None:
            print("Ship goes out of bounds, try again")
            continue

        if not is_valid_ship(coords, occupied):
            print("Ship overlaps or touches another ship, try again")
            continue

        inputs.append(coords)
        for c in coords:
            occupied.add(c)
        remaining[size] -= 1

    return inputs


def main():
    ships = collect_player_ships()
    save_ships(ships, data_path("player_ships.csv"))
    print("your ships")
    print(ships)


if __name__ == "__main__":
    main()
