"""*Carries all Quartz AST Nodes*."""

##############################
# IMPORTS
##############################

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .tokendef import Tag

##############################
# NODES
##############################


type Expr = Node | BinaryOp


@dataclass(frozen=True, slots=True)
class Node:
    """*All statements and almost all expressions*.

    Expressions which are binary or unary operations have their own base node.
    """


@dataclass(frozen=True, slots=True)
class BinaryOp:
    """*Binary operation: two operands*.

    Can also store unary operations by setting `left=None`.
    """

    op: str | Tag
    left: Expr | None
    right: Expr


@dataclass(frozen=True, slots=True)
class Program:
    """*Contains all statements and expressions for the program*."""

    statements: list[Node | BinaryOp]


@dataclass(frozen=True, slots=True)
class Ident(Node):
    """*Identifier*."""

    name: str


@dataclass(frozen=True, slots=True)
class Integer(Node):
    """*Integer*."""

    value: int


##############################
# END OF FILE
##############################
