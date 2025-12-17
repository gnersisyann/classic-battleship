import sys
from pathlib import Path
import bot_generation
import gameplay
import ship_input
from utils import data_path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.append(str(SRC))


def want_fresh_layout(path: Path) -> bool:
    if not path.exists():
        return True
    choice = input("Use existing player ship layout? [Y/n]: ").strip().lower()
    return choice not in ("", "y", "yes")


def main():
    player_path = data_path("player_ships.csv")
    if want_fresh_layout(player_path):
        ship_input.main()
    bot_generation.main()
    gameplay.play()


if __name__ == "__main__":
    main()
