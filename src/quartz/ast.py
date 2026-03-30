"""*Carries all Quartz AST Nodes*."""

##############################
# IMPORTS
##############################

from dataclasses import dataclass, field
from types import EllipsisType

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
    """*Statement containing only a bare expression*."""

    expr: Expr


@dataclass(frozen=True, slots=True)
class List(Expr):
    """*A list*."""

    elements: list[Expr] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class Tuple(Expr):
    """*A tuple*."""

    elements: list[Expr] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class Set(Expr):
    """*A set*."""

    elements: list[Expr] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class Dict(Expr):
    """*A dictionary*."""

    keys: list[Expr] = field(default_factory=list)
    values: list[Expr] = field(default_factory=list)


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
class UnaryOp(Op):
    """*Unary operation*."""

    op: Tag
    operand: Expr


@dataclass(frozen=True, slots=True)
class BoolOp(Op):
    """*Boolean operation: `or` or `and`*."""

    op: Tag
    values: list[Expr]


@dataclass(frozen=True, slots=True)
class Comparison(Op):
    """*Comparison of two or more values*."""

    left: Expr
    ops: list[Tag]
    comparators: list[Expr]


@dataclass(frozen=True, slots=True)
class Keyword(Expr):
    """*A keyword argument for function calls or class definitions*."""

    arg: str
    value: Expr


@dataclass(frozen=True, slots=True)
class Call(Expr):
    """*A function call*."""

    func: Expr
    args: list[Expr] = field(default_factory=list)
    keywords: list[Keyword] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class TernaryOp(Op):
    """*Ternary operation: a if b else c*."""

    test: Expr  # a
    body: Expr  # b
    orelse: Expr  # c


@dataclass(frozen=True, slots=True)
class Attribute(Expr):
    """*Attribute access*."""

    value: Expr
    attr: str


@dataclass(frozen=True, slots=True)
class Subscript(Expr):
    """*A subscript*."""

    value: Expr
    slice_: Expr


@dataclass(frozen=True, slots=True)
class Slice(Expr):
    """*Slice*."""

    lower: Expr | None = None
    upper: Expr | None = None
    step: Expr | None = None


@dataclass(frozen=True, slots=True)
class Constant(Expr):
    """*Integer, float, string, boolean, Ellipsis or None*."""

    value: int | float | str | bool | EllipsisType | None = None


@dataclass(frozen=True, slots=True)
class Ident(Expr):
    """*Identifier*."""

    name: str


##############################
# END OF FILE
##############################
