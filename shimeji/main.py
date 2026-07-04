import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

from core.character import Character
from core.pet_window import PetWindow


def get_app_root() -> Path:
    """Characters folder lives next to the exe/script."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).parent


def parse_chara_arg(argv: list[str]) -> str:
    for arg in argv:
        if arg.startswith("--chara="):
            return arg.split("=", 1)[1]
    raise ValueError("Missing --chara=<folder_name> argument")


def main():
    chara_name = parse_chara_arg(sys.argv[1:])
    characters_root = get_app_root() / "characters"

    app = QApplication(sys.argv)

    character = Character.load(chara_name, characters_root)
    window = PetWindow(character)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()