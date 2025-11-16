"""*The Quartz Interpreter:*
Currently only displays the output of the lexer.
"""

import os
import sys
from pprint import pprint
from tokendef import Token
from nodes import Program
from lexer import Lexer
from parser import Parser

os.system("cls" if os.name == "nt" else "clear")

VERSION = "InDev"
VERSION_DATE = """November 16, 2025
(it's 6:20 AM rn. i didn't wake up, i stayed up.)"""


def quartz(program):
    tokens: list[Token] = Lexer(program).lexer()
    parsed: Program = Parser(tokens).parse()
    """
    Okay, we got the parser done.
    So I'ma just print whatever gets parsed.

    Last stop, implementation!!!
    (and a bunch of other features here and there)
    """
    pprint(parsed)


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
            sys.exit(
                f"Error: File '{sys.argv[1]}' not found"
            )
        return

    print(f"Quartz {VERSION} ({VERSION_DATE})")

    RUNNING = True
    while RUNNING:
        program = input(">>> ")
        quartz(program)


if __name__ == "__main__":
    main(
        filename=".\\parsetest.qrtz",
        debugging=True,
    )
