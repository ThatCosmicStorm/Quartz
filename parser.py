"""*The Quartz Parser*."""

##############################
# IMPORTS
##############################

from collections.abc import Callable
from io import StringIO
from typing import NoReturn

from nodes import BinaryOp, Node
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
    initialized: bool = False
    tokens: list[Token]
    i: int = 0
    token: Token
    length: int
    keyword_stmts: dict[str, StmtHandler]
    keyword_exprs: dict[Tag, ExprHandler]


_self: _State = _State()


##############################
# INITIALIZE
##############################


def init(tokens: list[Token]) -> None:
    """*Initialize the thing exactly once*.

    Args:
        tokens (list[Token]): *Quartz `Token`'s*

    Raises:
        RuntimeError: *If already initialized*

    """
    if _self.initialized:
        msg: str = "Already initialized!"
        raise RuntimeError(msg)

    _self.tokens: list[Token] = tokens
    _self.token: Token = _self.tokens[_self.i]
    _self.length: int = len(_self.tokens)

    _self.initialized = True


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


def _check(type_: str | Tag) -> bool:
    return type_ in {_self.token.tag, _self.token.tok}


def _in(set_: set[Tag] | set[str] | set[str | Tag]) -> bool:
    return _self.token.tag in set_ or _self.token.tok in set_


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


def _check_ahead(value: str | Tag, num: int = 1) -> bool:
    i: int = _self.i + num
    ahead: bool = i < _self.length
    in_: bool = value in {_self.tokens[i].tag, _self.tokens[i].tok}
    return ahead and in_


def _in_ahead(
    set_: set[Tag] | set[str] | set[str | Tag],
    num: int = 1,
) -> bool:
    i: int = _self.i + num
    ahead: bool = i < _self.length
    tag: bool = _self.tokens[i].tag in set_
    tok: bool = _self.tokens[i].tok in set_
    return ahead and (tag or tok)


def _for() -> Node:
    return Node(
        _expect("for").tok,
        {"range": _range(), "suite": _suite()},
    )


def _function_definition() -> Node:
    pub: bool = bool(_match("pub"))
    _expect("fn")
    name: str = _expect(Tag.IDENT).tok
    _expect(Tag.L_PAREN)
    if not _check(Tag.R_PAREN):
        params: Node = _def_params()
    _expect(Tag.R_PAREN)
    if _match(Tag.TILDE_ARROW):
        return_: Node = _def_return()
    return Node(
        "function_definition",
        {
            "pub": pub,
            "name": name,
            "params": params,
            "return_": return_,
            "suite": _suite(),
        },
    )


def _if() -> Node:
    _expect("if")
    condition: Expr = _expr()
    suite: Node = _suite()
    if not _check("else"):
        return Node(
            "if",
            {"condition": condition, "suite": suite},
        )
    else_ifs: list[Node] = []
    else_: Node | None = None
    while _match("else"):
        if _match("if"):
            else_ifs.append(
                Node(
                    "else_if",
                    {"condition": _expr(), "suite": _suite()},
                ),
            )
        else:
            else_: Node = Node("else", _suite())
    return Node(
        "if",
        {
            "condition": condition,
            "suite": suite,
            "else_if": else_ifs,
            "else": else_,
        },
    )


def _match_() -> Node:
    return Node(
        _expect("match").tok,
        {"target": _expr(), "suite": _match_suite()},
    )


def _main() -> Node:
    return Node(_expect("main").tok, _suite())


def _while() -> Node:
    if _match("while"):
        until: bool = False
    elif _match("until"):
        until: bool = True
    return Node(
        "while",
        {
            "until": until,
            "condition": _expr(),
            "suite": _suite(),
        },
    )


def _wrap() -> Node:
    _expect("wrap")
    targets: list[Node] = [_target()]
    while _match(Tag.COMMA):
        if _check(Tag.NEWLINE):
            break
        targets.append(_target())
    return Node(
        "wrap",
        {"targets": targets, "suite": _wrap_suite()},
    )


def _call_parameter() -> Node:
    if _check(Tag.IDENT) and _check_ahead(Tag.EQUAL):
        return Node(
            "call_parameter",
            {"name": _next(2).tok, "value": _expr()},
        )
    return Node(
        "call_parameter",
        {"name": None, "value": _expr()},
    )


def _call_params() -> Node:
    return Node(
        "call_params",
        _listed(_call_parameter),
    )


def _def_parameter() -> Node:
    name: str = _expect(Tag.IDENT).tok
    annotation: Node | None = None
    if _match(Tag.COLON):
        annotation: Node = _type()
    default: Expr | None = None
    if _match(Tag.EQUAL):
        default: Expr = _expr()
    return Node(
        "def_parameter",
        {"name": name, "annotation": annotation, "default": default},
    )


def _def_params() -> Node:
    params: list[Node] = [_def_parameter()]
    while _match(Tag.COMMA):
        if _check(Tag.R_PAREN):
            break
        params.append(_def_parameter())
    return Node(
        "def_params",
        _listed(_def_parameter),
    )


def _def_return() -> Node:
    _expect(Tag.TILDE_ARROW)
    typ: Node = _type()
    default: Expr | None = None
    if _match(Tag.L_BRACE):
        default: Expr = _expr()
        _expect(Tag.R_BRACE)
    return Node(
        "def_return",
        {"type": typ, "default": default},
    )


##############################
# MAIN FUNCTION
##############################


def main() -> Node:
    """*Parse a list of Quartz tokens*.

    Raises:
        RuntimeError: *If called before initialization*

    Returns:
        Node: *Every statement and expression*

    """
    if not _self.initialized:
        msg: str = "Called before initialization!"
        raise RuntimeError(msg)

    statements: list[Node] = []
    while not _check(Tag.EOF):
        statements.append(_statement())
    return Node("program", statements)
