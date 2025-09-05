"""*The Quartz Interpreter:*
Currently only displays the output of the lexer.
"""

import os
import sys
from lexer import Lexer
os.system("cls" if os.name == "nt" else "clear")

VERSION = "InDev"
VERSION_DATE = "September 1, 2025"


def quartz(program):
    tokens = Lexer(program).lexer()
    for token in tokens:
        print(token)


def main(filename=None, debugging=False):
    if len(sys.argv) == 2 or debugging:
        if filename is not None:
            file = filename
        else:
            file = sys.argv[1]
        try:
            with open(file, "r", encoding="utf8") as f:
                quartz(f.read())
        except FileNotFoundError:
            sys.exit(f"Error: File '{sys.argv[1]}' not found")
        return

    print(f"Quartz {VERSION} ({VERSION_DATE})")

    RUNNING = True
    while RUNNING:
        program = input(">>> ")
        quartz(program)


if __name__ == "__main__":
    main(".\\diceroller.qrtz", True)
