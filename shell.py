"""
Shell for Quartz
"""
import os
import logic

os.system("cls" if os.name == "nt" else "clear")

VERSION = "InDev"
VERSION_DATE = "June 27, 2025"

print(f"Quartz {VERSION} ({VERSION_DATE})")

RUNNING = True
while RUNNING:
    program = input(">>> ")
    output = logic.lexer(program)
    print(output)
