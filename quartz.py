#! /usr/bin/env python

"""*The Quartz Interpreter*.

Currently only displays the output of the lexer.
"""

##############################
# IMPORTS
##############################

import sys
from pathlib import Path
from pprint import pprint
from typing import TYPE_CHECKING, Literal

import lexer
import parser

if TYPE_CHECKING:
    from nodes import Node
    from tokendef import Token

NUM_OF_VALID_ARGS: Literal[2] = 2

##############################
# ERROR & CLEAR TERMINAL
##############################


class _NumberOfArgsError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Usage: `quartz` `filename`",
        )


def _clear_terminal() -> None:
    print("\033[H\033[2J", end="")


##############################
# QUARTZ
##############################


def _quartz(program: str) -> None:
    lexer.init(program)
    tokens: list[Token] = lexer.main()
    pprint(tokens)


##############################
# MAIN FUNCTION
##############################


def main(
    *,
    filename: str = "",
    debugging: bool = False,
) -> None:
    """*Use `quartz.py` in the command line*.

    No interpreter mode yet.

    Args:
        filename (str): *Path to Quartz file*
        debugging (bool): *Removes argument requirements*

    Raises:
        _NumberOfArgsError: *Only takes two arguments*

    """
    _clear_terminal()

    if not debugging:
        num_of_args: int = len(sys.argv)
        if num_of_args != NUM_OF_VALID_ARGS:
            raise _NumberOfArgsError

    file: Path = Path(filename) if filename else Path(sys.argv[1])
    try:
        with Path.open(file, encoding="utf8") as f:
            _quartz(f.read())
    except FileNotFoundError:
        sys.exit(
            f"Error: File '{sys.argv[1]}' not found",
        )


if __name__ == "__main__":
    main(
        filename=".\\parsetest.qrtz",
        debugging=True,
    )

##############################
# END OF FILE
##############################
