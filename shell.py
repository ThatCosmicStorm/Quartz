"""
Shell for Quartz
"""
import os
from pprint import pprint
from logic import lexer
os.system("cls" if os.name == "nt" else "clear")

VERSION = "InDev"
VERSION_DATE = "July 31, 2025"

print(f"Quartz {VERSION} ({VERSION_DATE})")

RUNNING = True
while RUNNING:
    program = input(">>> ")
    tokens = lexer(program)
    pprint(tokens)
