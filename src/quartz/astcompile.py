"""*Compiles a Python AST from the Quartz AST*."""

##############################
# IMPORTS
##############################

import ast as py
from collections.abc import Callable
from enum import Enum
from typing import Any

import quartz.ast as q

from .tokendef import Error, Tag

##############################
# SET CONSTANTS
##############################

BINARY_OPERATORS: dict[Tag, Any] = {
    Tag.AMPERSAND: py.BitAnd,
    Tag.ASTERISK: py.Mult,
    Tag.CARET: py.Pow,
    Tag.MINUS: py.Sub,
    Tag.L_ANGLE_L_ANGLE: py.LShift,
    Tag.PERCENT: py.Mod,
    Tag.PIPE: py.BitOr,
    Tag.PLUS: py.Add,
    Tag.R_ANGLE_R_ANGLE: py.RShift,
    Tag.SLASH: py.Div,
    Tag.SLASH_SLASH: py.FloorDiv,
    Tag.TILDE: py.BitXor,
}

UNARY_OPERATORS: dict[Tag, Any] = {
    Tag.MINUS: py.USub,
    Tag.NOT: py.Not,
    Tag.PLUS: py.UAdd,
    Tag.TILDE: py.Invert,
}

COMPARE_OPERATORS: dict[Tag, Any] = {
    Tag.EQUAL_EQUAL: py.Eq,
    Tag.BANG_EQUAL: py.NotEq,
    Tag.L_ANGLE: py.Lt,
    Tag.L_ANGLE_EQUAL: py.LtE,
    Tag.R_ANGLE: py.Gt,
    Tag.R_ANGLE_EQUAL: py.GtE,
    Tag.IS: py.Is,
    Tag.IS_NOT: py.IsNot,
    Tag.IN: py.In,
    Tag.NOT_IN: py.NotIn,
}

##############################
# ERROR DEFINITION
##############################


class _TranspilerError(Error):
    pass


##############################
# STATE
##############################


class _Ctx(Enum):
    LOAD = py.Load
    STORE = py.Store
    DEL = py.Del


class _State:
    expr_nodes: dict[Any, Callable[[Any], Any]]
    ctx: _Ctx = _Ctx.LOAD


_self: _State = _State()

##############################
# HELPER FUNCTIONS
##############################


def _ctx() -> py.Load | py.Store | py.Del:
    return _self.ctx.value()


# help wanted... :(


##############################
# MAIN FUNCTION
##############################


def main(program: q.Program) -> py.Module:
    """*Compiles py Python AST from Quartz `Node`s*.

    Args:
        program (Program): *A Quartz `Program`*

    Returns:
        Node: *Every statement and expression*

    """
    _self.expr_nodes: dict[Any, Callable[[Any], Any]] = {
        q.Constant: _constant,
        q.Ident: _name,
        q.BinaryOp: _binary_op,
        q.UnaryOp: _unary_op,
        q.BoolOp: _bool_op,
        q.Comparison: _comparison,
        q.TernaryOp: _ternary_op,
        q.List: _list,
        q.Tuple: _tuple,
        q.Set: _set,
        q.Dict: _dict,
        q.Call: _call,
        q.Keyword: _keyword,
        q.Attribute: _attribute,
        q.Subscript: _subscript,
        q.Slice: _slice,
    }
    statements: list[py.stmt] = [_match(node) for node in program.statements]
    return py.Module(body=statements, type_ignores=[])


##############################
# MATCH FUNCTIONS
##############################


def _match(stmt: q.Stmt) -> py.stmt:
    # For now, just return an expression statement
    if isinstance(stmt, q.ExprStmt):
        return py.Expr(_expr(stmt.expr))
    if isinstance(stmt, q.Assign):
        return py.Assign(
            [_expr(trgt, _Ctx.STORE) for trgt in stmt.targets],
            _expr(stmt.value),
        )
    raise _TranspilerError


def _expr(expr: q.Expr, ctx: _Ctx | None = None) -> py.expr:
    _self.ctx: _Ctx = ctx or _Ctx.LOAD
    for node, func in _self.expr_nodes.items():
        if isinstance(expr, node):
            return func(expr)
    raise _TranspilerError


def _constant(node: q.Constant) -> py.Constant:
    return py.Constant(node.value)


def _name(node: q.Ident) -> py.Name:
    return py.Name(node.name, _ctx())


def _bool_op(node: q.BoolOp) -> py.BoolOp:
    return py.BoolOp(
        op=(py.Or if node.op == Tag.OR else py.And)(),
        values=[_expr(value) for value in node.values],
    )


def _binary_op(node: q.BinaryOp) -> py.BinOp:
    return py.BinOp(
        left=_expr(node.left),
        op=BINARY_OPERATORS[node.op](),
        right=_expr(node.right),
    )


def _unary_op(node: q.UnaryOp) -> py.UnaryOp:
    return py.UnaryOp(
        op=UNARY_OPERATORS[node.op](),
        operand=_expr(node.operand),
    )


def _comparison(node: q.Comparison) -> py.Compare:
    return py.Compare(
        _expr(node.left),
        [COMPARE_OPERATORS[op]() for op in node.ops],
        [_expr(expr) for expr in node.comparators],
    )


def _ternary_op(node: q.TernaryOp) -> py.IfExp:
    return py.IfExp(
        _expr(node.test),
        _expr(node.body),
        _expr(node.orelse),
    )


def _list(node: q.List) -> py.List:
    ctx: py.Load | py.Store | py.Del = _ctx()
    return py.List([_expr(elt) for elt in node.elements], ctx)


def _tuple(node: q.Tuple) -> py.Tuple:
    ctx: py.Load | py.Store | py.Del = _ctx()
    return py.Tuple([_expr(elt) for elt in node.elements], ctx)


def _set(node: q.Set) -> py.Set:
    return py.Set([_expr(elt) for elt in node.elements])


def _dict(node: q.Dict) -> py.Dict:
    return py.Dict(
        [_expr(key) for key in node.keys],
        [_expr(value) for value in node.values],
    )


def _call(node: q.Call) -> py.Call:
    return py.Call(
        _expr(node.func),
        [_expr(arg) for arg in node.args],
        [_keyword(kw) for kw in node.keywords],
    )


def _keyword(node: q.Keyword) -> py.keyword:
    return py.keyword(node.arg, _expr(node.value))


def _attribute(node: q.Attribute) -> py.Attribute:
    ctx: py.Load | py.Store | py.Del = _ctx()
    return py.Attribute(
        _expr(node.value),
        node.attr,
        ctx,
    )


def _subscript(node: q.Subscript) -> py.Subscript:
    ctx: py.Load | py.Store | py.Del = _ctx()
    return py.Subscript(
        _expr(node.value),
        _expr(node.slice_),
        ctx,
    )


def _slice(node: q.Slice) -> py.Slice:
    return py.Slice(
        _expr(node.lower) if node.lower else None,
        _expr(node.upper) if node.upper else None,
        _expr(node.step) if node.step else None,
    )
