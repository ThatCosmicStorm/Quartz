"""*Compiles a Python AST from the Quartz AST*."""

##############################
# IMPORTS
##############################

import ast
from typing import TYPE_CHECKING

from nodes import Integer

if TYPE_CHECKING:
    from nodes import BinaryOp, Expr, Node, Program


##############################
# STATE
##############################


class _State:
    program: Program


_self: _State = _State()


##############################
# HELPER FUNCTIONS
##############################


##############################
# MAIN FUNCTION
##############################


def main(program: Program) -> ast.Module:
    """*Compiles a Python AST from Quartz `Node`s*.

    Args:
        program (Program): *A Quartz `Program`*

    Returns:
        Node: *Every statement and expression*

    """
    _self.program: Program = program
    statements: list[ast.stmt] = [
        _match(node) for node in _self.program.statements
    ]
    return ast.Module(body=statements)


##############################
# MATCH FUNCTIONS
##############################


def _match(stmt: Node | BinaryOp) -> ast.stmt:
    # For now, just return an expression
    return _expr(stmt)


def _expr(stmt: Expr) -> ast.stmt:
    expr: ast.Constant
    if isinstance(stmt, Integer):
        expr = ast.Constant(stmt.value)
    return ast.Expr(expr)
