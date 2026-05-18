"""*The Python AST compiler for the Quartz programming language*."""

##############################
# IMPORTS
##############################

import ast as py
from typing import TYPE_CHECKING, Any

import quartz.ast as q

from .tokendef import Error, Tag

if TYPE_CHECKING:
    from collections.abc import Callable

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
# MAIN CLASS
##############################


class ASTCompile:
    """The Quartz AST Compiler."""

    def __init__(self, program: q.Program) -> None:
        """*Compiles Python AST from Quartz `Node`'s*.

        Args:
            program (Program): *A Quartz `Program`*

        Returns:
            Node: *Every statement and expression*

        """
        self._stmt_handlers: dict[Any, Callable[[Any], Any]] = {
            q.ExprStmt: lambda stmt: py.Expr(self._expr(stmt.expr)),
            q.Assign: lambda stmt: py.Assign(
                [self._expr(trgt, py.Store()) for trgt in stmt.targets],
                self._expr(stmt.value),
            ),
            q.Delete: lambda stmt: py.Delete(
                [self._expr(trgt, py.Del()) for trgt in stmt.targets],
            ),
            q.Return: lambda stmt: py.Return(
                self._expr(stmt.value) if stmt.value else None,
            ),
            q.If: lambda stmt: py.If(
                test=self._expr(stmt.test),
                body=[self._stmt(sttmnt) for sttmnt in stmt.body],
                orelse=[self._stmt(sttmnt) for sttmnt in stmt.orelse],
            ),
            q.While: lambda stmt: py.While(
                test=self._expr(stmt.test),
                body=[self._stmt(sttmnt) for sttmnt in stmt.body],
                orelse=[self._stmt(sttmnt) for sttmnt in stmt.orelse],
            ),
            q.For: lambda stmt: py.For(
                target=self._expr(stmt.target, ctx=py.Store()),
                iter=self._expr(stmt.iter_),
                body=[self._stmt(sttmnt) for sttmnt in stmt.body],
                orelse=[self._stmt(sttmnt) for sttmnt in stmt.orelse],
            ),
            q.FunctionDefinition: lambda stmt: py.FunctionDef(
                name=stmt.name,
                args=self._arguments(stmt.args),
                body=[self._stmt(sttmnt) for sttmnt in stmt.body],
                decorator_list=[],
            ),
        }
        self._expr_handlers: dict[Any, Callable[[Any], Any]] = {
            q.Constant: lambda node: py.Constant(node.value),
            q.Ident: lambda node: py.Name(node.name, self._get_ctx()),
            q.BoolOp: lambda node: py.BoolOp(
                op=(py.Or if node.op == Tag.OR else py.And)(),
                values=[self._expr(value) for value in node.values],
            ),
            q.BinaryOp: lambda node: py.BinOp(
                left=self._expr(node.left),
                op=BINARY_OPERATORS[node.op](),
                right=self._expr(node.right),
            ),
            q.UnaryOp: lambda node: py.UnaryOp(
                op=UNARY_OPERATORS[node.op](),
                operand=self._expr(node.operand),
            ),
            q.Comparison: lambda node: py.Compare(
                self._expr(node.left),
                [COMPARE_OPERATORS[op]() for op in node.ops],
                [self._expr(expr) for expr in node.comparators],
            ),
            q.TernaryOp: lambda node: py.IfExp(
                self._expr(node.test),
                self._expr(node.body),
                self._expr(node.orelse),
            ),
            q.List: self._list,
            q.Tuple: self._tuple,
            q.Set: lambda node: py.Set(
                [self._expr(elt) for elt in node.elements],
            ),
            q.Dict: lambda node: py.Dict(
                [self._expr(key) for key in node.keys],
                [self._expr(value) for value in node.values],
            ),
            q.Call: lambda node: py.Call(
                self._expr(node.func),
                [self._expr(arg) for arg in node.args],
                [self._keyword(kw) for kw in node.keywords],
            ),
            q.Keyword: self._keyword,
            q.Attribute: self._attribute,
            q.Subscript: self._subscript,
            q.Slice: lambda node: py.Slice(
                self._expr(node.lower) if node.lower else None,
                self._expr(node.upper) if node.upper else None,
                self._expr(node.step) if node.step else None,
            ),
            q.Lambda: lambda node: py.Lambda(
                self._arguments(node.args),
                self._expr(node.body),
            ),
        }
        self._context: py.expr_context = py.Load()
        statements: list[py.stmt] = [
            self._stmt(node) for node in program.statements
        ]
        self._module: py.Module = py.Module(body=statements, type_ignores=[])

    ##########################
    # Helper Functions
    ##########################

    def _get_ctx(self) -> py.expr_context:
        return self._context

    ##########################
    # Main Getter Function
    ##########################

    def get_module(self) -> py.Module:
        """*Return the output of the AST compiler*.

        Returns:
            py.Module: *AST compiler output*.

        """
        return self._module

    ##########################
    # Match Functions
    ##########################

    def _stmt(self, stmt: q.Stmt) -> py.stmt:
        return self._stmt_handlers[type(stmt)](stmt)

    def _expr(
        self,
        expr: q.Expr,
        ctx: py.expr_context | None = None,
    ) -> py.expr:
        self._context: py.expr_context = ctx or py.Load()
        return self._expr_handlers[type(expr)](expr)

    def _arguments(self, args: q.Arguments) -> py.arguments:
        return py.arguments(
            posonlyargs=[],
            args=[self._arg(arg) for arg in args.args],
            kwonlyargs=[],
            vararg=None,
            kwarg=None,
            kw_defaults=[],
            defaults=[self._expr(dflt) for dflt in args.defaults],
        )

    def _arg(self, arg: q.Arg) -> py.arg:
        if arg.annotation is None:
            return py.arg(arg=arg.arg)
        return py.arg(
            arg=arg.arg,
            annotation=self._expr(arg.annotation),
        )

    def _list(self, node: q.List) -> py.List:
        ctx: py.expr_context = self._get_ctx()
        return py.List([self._expr(elt) for elt in node.elements], ctx)

    def _tuple(self, node: q.Tuple) -> py.Tuple:
        ctx: py.expr_context = self._get_ctx()
        return py.Tuple([self._expr(elt) for elt in node.elements], ctx)

    def _keyword(self, node: q.Keyword) -> py.keyword:
        return py.keyword(node.arg, self._expr(node.value))

    def _attribute(self, node: q.Attribute) -> py.Attribute:
        ctx: py.expr_context = self._get_ctx()
        return py.Attribute(
            self._expr(node.value),
            node.attr,
            ctx,
        )

    def _subscript(self, node: q.Subscript) -> py.Subscript:
        ctx: py.expr_context = self._get_ctx()
        return py.Subscript(
            self._expr(node.value),
            self._expr(node.slice_),
            ctx,
        )
