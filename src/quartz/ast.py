"""*Carries all Quartz AST Nodes*."""

##############################
# IMPORTS
##############################

from dataclasses import dataclass

from .tokendef import Tag

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
class ExprStmt(Stmt):
    """*Contains one expression*."""

    expr: Expr


@dataclass(frozen=True, slots=True)
class Op(Expr):
    """*Operation with one or more operands*."""


@dataclass(frozen=True, slots=True)
class BinaryOp(Op):
    """*Binary operation*."""

    op: Tag
    left: Expr
    right: Expr


@dataclass(frozen=True, slots=True)
class BoolOp(Op):
    """*A boolean operation, `or` or `and`*."""

    op: str
    left: Expr
    right: Expr


@dataclass(frozen=True, slots=True)
class UnaryOp(Op):
    """*Unary operation*."""

    op: Tag
    operand: Expr


@dataclass(frozen=True, slots=True)
class Constant(Expr):
    """*Integer, float, string, boolean, or None*."""

    value: int | float | str | bool | None


##############################
# END OF FILE
##############################
