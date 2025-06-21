import logic, os

os.system("cls" if os.name == "nt" else "clear")

version = "InDev"
version_date = "June 20, 2025"

print(f"ReadAbl {version} ({version_date})")

running = True
while running:
    program = input(">>> ")
    logic.lexer(program)