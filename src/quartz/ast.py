# Copyright (c) Randall "R2" Dunkin
# Licensed under the MIT License.
"""*The AST for the Quartz programming language*."""

##############################
# IMPORTS
##############################

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import EllipsisType

##############################
# NODES
##############################


@dataclass(frozen=True, slots=True)
class Node:
    """*Adam*."""


@dataclass(frozen=True, slots=True)
class Expr(Node):
    """*Expression*."""


@dataclass(frozen=True, slots=True)
class Stmt(Node):
    """*Statement*."""


@dataclass(frozen=True, slots=True)
class Program:
    """*Contains all statements and expressions for the program*."""

    statements: list[Stmt]


@dataclass(frozen=True, slots=True)
class Constant(Expr):
    """*Integer, float, string, boolean, Ellipsis or None*."""

    value: int | float | str | bool | EllipsisType | None


@dataclass(frozen=True, slots=True)
class Ident(Expr):
    """*Identifier*."""

    name: str
