"""
Shell for Quartz
"""
import os
import logic

os.system("cls" if os.name == "nt" else "clear")

VERSION = "InDev"
VERSION_DATE = "July 10, 2025"

print(f"Quartz {VERSION} ({VERSION_DATE})")

RUNNING = True
while RUNNING:
    program = input(">>> ")
    output = logic.lexer(program)
    for i, char in enumerate(output):
        print(char)
