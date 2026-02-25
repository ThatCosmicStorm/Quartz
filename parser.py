"""*The Quartz Parser*."""

##############################
# IMPORTS
##############################

from collections.abc import Callable
from typing import NoReturn

from nodes import BinaryOp, Ident, Integer, Node, Program
from tokendef import Error, Tag, Token

##############################
# SET CONSTANTS
##############################

# All sets declared here and in the main class
# that deal with words and letters
# are organized in alphabetical order,
# with non-alphabetical symbols coming first in no particular order.

ASSIGNMENT_OPS: set[Tag] = {
    Tag.AMPERSAND_EQUAL,
    Tag.ARROW_EQUAL,
    Tag.ASTERISK_EQUAL,
    Tag.CARET_EQUAL,
    Tag.EQUAL,
    Tag.L_ANGLE_L_ANGLE_EQUAL,
    Tag.MINUS_EQUAL,
    Tag.PERCENT_EQUAL,
    Tag.PIPE_EQUAL,
    Tag.PLUS_EQUAL,
    Tag.R_ANGLE_R_ANGLE_EQUAL,
    Tag.SLASH_EQUAL,
    Tag.TILDE_EQUAL,
}

COMPARISON_OPS: set[str | Tag] = {
    "in",
    "is",
    "not",
    Tag.BANG_EQUAL,
    Tag.EQUAL_EQUAL,
    Tag.L_ANGLE,
    Tag.L_ANGLE_EQUAL,
    Tag.R_ANGLE,
    Tag.R_ANGLE_EQUAL,
}

COMPOUND_WORDS: set[str] = {
    "class",
    "define",
    "for",
    "if",
    "until",
    "while",
    "wrap",
}

##############################
# ERROR DEFINITION
##############################


class _ParserError(Error):
    pass


##############################
# TYPE ALIASES
##############################

type StmtHandler = Callable[[], Node]

type Expr = Node | BinaryOp

type ExprHandler = Callable[[], Expr]

type Logic = list[Expr] | list[dict[str, Expr]]

##############################
# PARSER CLASS
##############################


class _State:
    tokens: list[Token]
    i: int = 0
    token: Token
    length: int
    keyword_stmts: dict[str, StmtHandler]
    keyword_exprs: dict[Tag, ExprHandler]


_self: _State = _State()


##############################
# HELPER FUNCTIONS
##############################


def _raise_error(message: str) -> NoReturn:
    raise _ParserError(
        _self.token.ln,
        _self.token.col,
        _self.token.line,
        message,
    )


def _next(num: int = 1) -> Token:
    if _self.i + num >= _self.length:
        _raise_error(f"No token found at index #{_self.i + num}")
    past_token: Token = _self.token
    _self.i += num
    _self.token: Token = _self.tokens[_self.i]
    return past_token


def _check(type_: str | Tag, ahead: int = 0) -> bool:
    i: int = _self.i + ahead
    if_ahead: bool = i < _self.length
    in_: bool = type_ in {_self.tokens[i].tag, _self.tokens[i].tok}
    return if_ahead and in_


def _in(set_: set[Tag] | set[str] | set[str | Tag], ahead: int = 0) -> bool:
    i: int = _self.i + ahead
    if_ahead: bool = i < _self.length
    tag: bool = _self.tokens[i].tag in set_
    tok: bool = _self.tokens[i].tok in set_
    return if_ahead and (tag or tok)


def _match(type_: str | Tag) -> Token | None:
    if type_ in {_self.token.tag, _self.token.tok}:
        return _next()
    return None


def _expect(type_: str | Tag) -> Token:
    if type_ in {_self.token.tok, _self.token.tag}:
        return _next()
    return _raise_error(
        f"Expected {type_}, got {_self.token.tok or _self.token.tag}",
    )


##############################
# MAIN FUNCTION
##############################


def main(tokens: list[Token]) -> Program:
    """*Parse a list of Quartz tokens*.

    Args:
        tokens (list[Token]): *Quartz `Token`'s*

    Returns:
        Node: *Every statement and expression*

    """
    _self.tokens: list[Token] = tokens
    _self.token: Token = _self.tokens[_self.i]
    _self.length: int = len(_self.tokens)

    # _self.parse_statements: dict[str, Callable[[], Node]] = {
    #     "assert": _assert,
    #     "import": _basic_import,
    #     "break": _break,
    #     "continue": _continue,
    #     "delete": _del,
    #     "pass": _pass,
    #     "raise": _raise,
    #     "<<<": _return,
    #     "from": _selective_import,
    #     "type": _type_alias,
    #     "yield": _yield,
    #     "pub": _public,
    #     "@": _decorator,
    #     "for": _for,
    #     "fn": _function_definition,
    #     "if": _if,
    #     "match": _match,
    #     "struct": _struct,
    #     "while": _while,
    #     "until": _while,
    # }
    # _self.keywords: set[str] = _self.parse_statements.keys()

    statements: list[Expr] = []
    while not _check(Tag.EOF):
        statements.append(_expr())
    return Program(statements)


def _expr() -> Expr:
    return _primary()


class _UnknownPrimaryError(Exception):
    pass


def _primary() -> Node:
    if _check(Tag.INTEGER):
        return Integer(int(_next().tok))
    if _check(Tag.IDENT):
        return Ident(_next().tok)
    raise _UnknownPrimaryError


##############################
# END OF FILE
##############################
