"""*The Quartz Interpreter:*
Currently only displays the output of the lexer.
"""

import os
from pprint import pprint
from lexer import Lexer
os.system("cls" if os.name == "nt" else "clear")

VERSION = "InDev"
VERSION_DATE = "September 1, 2025"

print(f"Quartz {VERSION} ({VERSION_DATE})")

RUNNING = True
while RUNNING:
    program = input(">>> ")
    tokens = Lexer(program).lexer()
    pprint(tokens)
