import re

PATTERN_STRING = r"^(?:1|2|3|4)\s+\d+\s+\d+\s+[nsew]$"

SIZE_4_COUNT = 0
SIZE_3_COUNT = 0
SIZE_2_COUNT = 0
SIZE_1_COUNT = 1
    
remaining = {1: SIZE_1_COUNT, 2: SIZE_2_COUNT, 3: SIZE_3_COUNT, 4: SIZE_4_COUNT}

def getinput():
    info = input()
    while not bool(re.fullmatch(PATTERN_STRING, info)):
        print("Invalid input format, try 'size x y direction'")
        info = input()
    return info

def get_ship_coords(size, x, y, direction):
    x = int(x)
    y = int(y)
    dx = 0
    dy = 0
    match direction:
        case 'n':
            dy = 1
        case 's':
            dy = -1
        case 'e':
            dx = 1
        case 'w':
            dx = -1
inputs = []

print("Input format: size x y direction \n" \
		"x,y number from [0;9] \n" \
		"direction is character from [n,e,s,w]")
i = 0

while sum(remaining.values()) > 0:
    raw = getinput()
    size, x, y, direction = raw.split()
    size = int(size)
    if remaining[size] == 0:
        print(f"All ships of size {size} is placed")
        continue	
	# validate borders
    coords = get_ship_coords(size,x,y,direction)
    inputs.append(coords)
    remaining[size] -= 1
    
print(inputs)


