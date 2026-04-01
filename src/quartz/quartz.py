#! /usr/bin/env python

"""*The Quartz Interpreter*.

Currently only displays the output of the lexer.
"""

##############################
# IMPORTS
##############################
import ast
import sys
from pathlib import Path
from pprint import pprint
from typing import TYPE_CHECKING, Literal

import quartz.astcompile
import quartz.lexer
import quartz.parser

if TYPE_CHECKING:
    from types import CodeType

    from .ast import Program
    from .tokendef import Token

NUM_OF_VALID_ARGS: Literal[2] = 2

##############################
# ERROR & CLEAR TERMINAL
##############################


class _NumberOfArgsError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Usage: `quartz` `filename` [`flag`]",
        )


def _clear_terminal() -> None:
    print("\033[H\033[2J", end="")


##############################
# QUARTZ
##############################


def _quartz(program: str, filename: Path, *, debug: bool) -> None:
    if debug:
        print("File input:")
        pprint(program)
    tokens: list[Token] = quartz.lexer.main(program)
    if debug:
        print("\n" + "Lexer:")
        pprint(tokens)
    prog: Program = quartz.parser.main(tokens)
    if debug:
        print("\n" + "Parser:")
        for stmt in prog.statements:
            pprint(stmt)
    module: ast.Module = quartz.astcompile.main(prog)
    if debug:
        print("\n" + "AST Compile:")
        print(ast.dump(module, indent=4))
    ast.fix_missing_locations(module)
    code: CodeType = compile(module, filename=filename, mode="exec")
    if debug:
        print("\n" + "Output:")
    exec(code)  # noqa: S102


##############################
# MAIN FUNCTION
##############################


def main(
    filename: str = "",
) -> None:
    """*Use `quartz.py` in the command line*.

    No interpreter mode yet.

    Args:
        filename (str): *Path to Quartz file*

    Raises:
        _NumberOfArgsError: *Only takes two arguments*

    """
    _clear_terminal()

    num_of_args: int = len(sys.argv)
    if num_of_args < NUM_OF_VALID_ARGS:
        raise _NumberOfArgsError

    file: Path = Path(filename) if filename else Path(sys.argv[1])
    debug: bool = (
        bool(sys.argv[2] == "-debug")
        if num_of_args > NUM_OF_VALID_ARGS
        else False
    )
    try:
        with Path.open(file, encoding="utf8") as f:
            _quartz(f.read(), file, debug=debug)
    except FileNotFoundError:
        sys.exit(
            f"Error: File '{sys.argv[1]}' not found",
        )


##############################
# END OF FILE
##############################
