"""*The Quartz Parser*."""

##############################
# IMPORTS
##############################

from collections.abc import Callable
from typing import NoReturn

import quartz.ast as q

from .tokendef import Error, Tag, Token

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

COMPARISON_OPS: set[Tag] = {
    Tag.BANG_EQUAL,
    Tag.EQUAL_EQUAL,
    Tag.IN,
    Tag.IS,
    Tag.IS_NOT,
    Tag.L_ANGLE,
    Tag.L_ANGLE_EQUAL,
    Tag.NOT,
    Tag.NOT_IN,
    Tag.R_ANGLE,
    Tag.R_ANGLE_EQUAL,
}

COMPOUND_WORDS: set[str] = {
    "class",
    "for",
    "fn",
    "if",
    "pub",
    "struct",
    "until",
    "while",
}

##############################
# ERROR DEFINITION
##############################


class _ParserError(Error):
    pass


##############################
# STATE
##############################


class _State:
    tokens: list[Token]
    i: int = 0
    token: Token
    length: int
    parse_statements: dict[str, Callable[[], q.Stmt]]
    keywords: set[str]
    primary_dict: dict[Tag, Callable[[], q.Constant]]
    primary_dict_keys: set[Tag]


_self: _State = _State()

##############################
# HELPER FUNCTIONS
##############################


def _raise_error(message: str = "") -> NoReturn:
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


def _check(*types: str | Tag, ahead: int = 0) -> bool:
    i: int = _self.i + ahead
    if_ahead: bool = i < _self.length
    in_: bool = any(
        typ in {_self.tokens[i].tag, _self.tokens[i].tok} for typ in types
    )
    return if_ahead and in_


def _in(set_: set[Tag] | set[str], ahead: int = 0) -> bool:
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


def main(tokens: list[Token]) -> q.Program:
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
    # _self.keywords: set[str] = set(_self.parse_statements.keys())

    _self.primary_dict: dict[Tag, Callable[[], q.Constant]] = {
        Tag.INTEGER: _integer,
        Tag.FALSE: _false,
        Tag.FLOAT: _float,
        Tag.NONE: _none,
        Tag.STRING: _string,
        Tag.TRUE: _true,
        Tag.ELLIPSIS: _ellipsis,
    }
    _self.primary_dict_keys: set[Tag] = set(_self.primary_dict.keys())

    statements: list[q.Stmt] = []
    while not _check(Tag.EOF):
        statements.append(_stmt())
        print(statements[-1])
    return q.Program(statements)


##############################
# STATEMENTS
##############################


def _stmt() -> q.Stmt:
    # For now, we're just focusing on expressions.
    expr: q.Expr = _expr()
    _expect(Tag.NEWLINE)
    return q.ExprStmt(expr)


##############################
# SIMPLE CASES
##############################

##############################
# COMPOUND CASES
##############################

##############################
# STATEMENT PARTS
##############################


def _call_parameter() -> q.Expr:
    if _check(Tag.IDENT) and _check(Tag.EQUAL, ahead=1):
        return q.Keyword(_next(2).tok, _expr())
    return _expr()


def _call_params() -> tuple[list[q.Expr], list[q.Keyword]]:
    lst: list[q.Expr] = [_call_parameter()]
    while _match(Tag.COMMA) and not _check(Tag.R_PAREN):
        lst.append(_call_parameter())
    _match(Tag.COMMA)
    args: list[q.Expr] = [arg for arg in lst if not isinstance(arg, q.Keyword)]
    keywords: list[q.Keyword] = [
        arg for arg in lst if isinstance(arg, q.Keyword)
    ]
    return (args, keywords)


##############################
# BLOCKS
##############################

##############################
# EXPRESSIONS
##############################


def _expr() -> q.Expr:
    return _ternary()

    # expr: q.Expr = _ternary()
    # if not _check(Tag.ARROW):
    #     return expr
    # lst: list[q.Expr] = []
    # while _match(Tag.ARROW):
    #     lst.append(_pipe_stage())
    # return q.Pipeline(expr, lst)


def _ternary() -> q.Expr:
    body: q.Expr = _disjunction()
    if not _check("if"):
        return body
    _expect("if")
    test: q.Expr = _expr()
    _expect("else")
    orelse: q.Expr = _expr()
    return q.TernaryOp(body, test, orelse)


def _disjunction() -> q.Expr:
    expr: q.Expr = _conjunction()
    if not _check(Tag.OR):
        return expr
    _expect(Tag.OR)
    values: list[q.Expr] = [expr, _conjunction()]
    while _match(Tag.OR):
        values.append(_conjunction())
    return q.BoolOp(Tag.OR, values)


def _conjunction() -> q.Expr:
    expr: q.Expr = _inversion()
    if not _check(Tag.AND):
        return expr
    _expect(Tag.AND)
    values: list[q.Expr] = [expr, _inversion()]
    while _match(Tag.AND):
        values.append(_inversion())
    return q.BoolOp(Tag.AND, values)


def _inversion() -> q.Expr:
    if not _check(Tag.NOT):
        return _comparison()
    return q.UnaryOp(_next().tag, _inversion())


def _comparison() -> q.Expr:
    expr: q.Expr = _bitwise_or()
    if not _in(COMPARISON_OPS):
        return expr
    ops: list[Tag] = [_next().tag]
    comparators: list[q.Expr] = [_bitwise_or()]
    while _in(COMPARISON_OPS):
        ops.append(_next().tag)
        comparators.append(_bitwise_or())
    return q.Comparison(expr, ops, comparators)


def _bitwise_or() -> q.Expr:
    expr: q.Expr = _bitwise_xor()
    while _check(Tag.PIPE):
        expr = q.BinaryOp(_next().tag, expr, _bitwise_xor())
    return expr


def _bitwise_xor() -> q.Expr:
    expr: q.Expr = _bitwise_and()
    while _check(Tag.TILDE):
        expr = q.BinaryOp(_next().tag, expr, _bitwise_and())
    return expr


def _bitwise_and() -> q.Expr:
    expr: q.Expr = _bitwise_shift()
    while _check(Tag.AMPERSAND):
        expr = q.BinaryOp(_next().tag, expr, _bitwise_shift())
    return expr


def _bitwise_shift() -> q.Expr:
    expr: q.Expr = _sum()
    while _check(Tag.L_ANGLE_L_ANGLE, Tag.R_ANGLE_R_ANGLE):
        expr = q.BinaryOp(_next().tag, expr, _sum())
    return expr


def _sum() -> q.Expr:
    expr: q.Expr = _term()
    while _check(Tag.PLUS, Tag.MINUS):
        expr = q.BinaryOp(_next().tag, expr, _term())
    return expr


def _term() -> q.Expr:
    expr: q.Expr = _factor()
    while _check(Tag.ASTERISK, Tag.SLASH, Tag.SLASH_SLASH, Tag.PERCENT):
        expr = q.BinaryOp(_next().tag, expr, _factor())
    return expr


def _factor() -> q.Expr:
    if not _check(Tag.PLUS, Tag.MINUS, Tag.TILDE):
        return _power()
    return q.UnaryOp(_next().tag, _factor())


def _power() -> q.Expr:
    expr: q.Expr = _postfix()
    while _check(Tag.CARET):
        expr = q.BinaryOp(_next().tag, expr, _factor())
    return expr


def _postfix() -> q.Expr:
    expr: q.Expr = _primary()
    while _check(Tag.PERIOD, Tag.L_PAREN, Tag.L_BRACKET):
        if _match(Tag.PERIOD):
            expr = q.Attribute(expr, _expect(Tag.IDENT).tok)
        elif _match(Tag.L_PAREN):
            if _match(Tag.R_PAREN):
                expr = q.Call(expr)
            else:
                expr = q.Call(expr, *_call_params())
                _expect(Tag.R_PAREN)
        elif _match(Tag.L_BRACKET):
            expr = q.Subscript(expr, _slice())
            _expect(Tag.R_BRACKET)
    return expr


def _slice() -> q.Expr:
    lower: q.Expr | None = None
    upper: q.Expr | None = None
    step: q.Expr | None = None
    if not _check(Tag.COLON):
        lower: q.Expr = _expr()
        expr: q.Expr = lower
    if not _check(Tag.COLON):
        return expr
    _expect(Tag.COLON)
    if not _check(Tag.COMMA, Tag.COLON, Tag.R_BRACKET):
        upper: q.Expr = _expr()
    if _match(Tag.COLON):  # noqa: SIM102
        if not (_check(Tag.COMMA, Tag.R_BRACKET)):
            step: q.Expr = _expr()
    return q.Slice(lower, upper, step)


def _primary() -> q.Expr:  # noqa: PLR0911
    if _self.token.tag in _self.primary_dict:
        return _self.primary_dict[_self.token.tag]()
    if _check(Tag.IDENT):
        return q.Ident(_next().tok)
    if _match(Tag.L_PAREN):
        return _tuple()
    if _match(Tag.L_BRACKET):
        return _list()
    if _match(Tag.DOLLAR_L_BRACE):
        return _set()
    if _match(Tag.PERCENT_L_BRACE):
        return _dict()
    return _raise_error("UnknownPrimary")


def _integer() -> q.Constant:
    return q.Constant(int(_next().tok))


def _float() -> q.Constant:
    return q.Constant(float(_next().tok))


def _string() -> q.Constant:
    return q.Constant(_next().tok)


def _true() -> q.Constant:
    _next()
    return q.Constant(value=True)


def _false() -> q.Constant:
    _next()
    return q.Constant(value=False)


def _none() -> q.Constant:
    _next()
    return q.Constant()


def _ellipsis() -> q.Constant:
    return q.Constant(Ellipsis)


def _list() -> q.List:
    if _match(Tag.R_BRACKET):
        return q.List()
    lst: list[q.Expr] = [_expr()]
    while _match(Tag.COMMA) and not _check(Tag.R_BRACKET):
        lst.append(_expr())
    _match(Tag.COMMA)
    _expect(Tag.R_BRACKET)
    return q.List(lst)


def _tuple() -> q.Expr:
    if _match(Tag.R_PAREN):
        return q.Tuple()
    expr: q.Expr = _expr()
    if _match(Tag.R_PAREN):
        return expr
    lst: list[q.Expr] = [expr]
    while _match(Tag.COMMA) and not _check(Tag.R_PAREN):
        lst.append(_expr())
    _match(Tag.COMMA)
    _expect(Tag.R_PAREN)
    return q.Tuple(lst)


def _set() -> q.Set:
    if _match(Tag.R_BRACE):
        return q.Set()
    lst: list[q.Expr] = [_expr()]
    while _match(Tag.COMMA) and not _check(Tag.R_BRACE):
        lst.append(_expr())
    _match(Tag.COMMA)
    _expect(Tag.R_BRACE)
    return q.Set(lst)


def _dict() -> q.Dict:
    if _match(Tag.R_BRACE):
        return q.Dict()
    lst: list[tuple[q.Expr, q.Expr]] = []
    key: q.Expr = _expr()
    _expect(Tag.COLON)
    lst.append((key, _expr()))
    while _match(Tag.COMMA) and not _check(Tag.R_BRACE):
        key: q.Expr = _expr()
        _expect(Tag.COLON)
        lst.append((key, _expr()))
    _match(Tag.COMMA)
    _expect(Tag.R_BRACE)
    return q.Dict([pair[0] for pair in lst], [pair[1] for pair in lst])


def _type() -> q.Expr:
    typ: q.Expr = _postfix()
    while _match(Tag.PIPE):
        typ: q.BinaryOp = q.BinaryOp(Tag.PIPE, typ, _postfix())
    return typ


##############################
# END OF FILE
##############################
