"""
Shell for Quartz
"""
import os
from pprint import pprint
from logic import tokenize
os.system("cls" if os.name == "nt" else "clear")

VERSION = "InDev"
VERSION_DATE = "July 30, 2025"

print(f"Quartz {VERSION} ({VERSION_DATE})")

RUNNING = True
while RUNNING:
    program = input(">>> ")
    tokens = tokenize(program)
    pprint(tokens)
