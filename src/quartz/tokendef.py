# Copyright (c) Randall "R2" Dunkin
# Licensed under the MIT License.
"""`Token`, `Position`, and `Error`."""

from typing import NamedTuple


class Position(NamedTuple):
    """*Character position in file*."""

    ln: int
    col: int


class Error(NamedTuple):
    """*High-level error*."""

    msg: str
    pos: Position


class Token(NamedTuple):
    """*Lexer token*."""

    tag: str
    tok: str
    pos: Position
