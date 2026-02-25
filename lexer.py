"""The Quartz Lexer."""

##############################
# IMPORTS
##############################

from collections.abc import Callable, Iterator
from io import StringIO
from typing import ClassVar, Literal, NoReturn

from tokendef import Error, Tag, Token

##############################
# SET CONSTANTS
##############################

# All sets declared here and in the main class
# that deal with words and letters
# are organized in alphabetical order,
# with non-alphabetical symbols coming first in no particular order.

DIGITS: set[str] = {
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
}

KEYWORDS: set[str] = {
    "alias",
    "and",
    "as",
    "assert",
    "break",
    "case",
    "class",
    "continue",
    "else",
    "False",
    "float",
    "fn",
    "for",
    "from",
    "hash",
    "if",
    "import",
    "in",
    "int",
    "is",
    "list",
    "match",
    "None",
    "not",
    "or",
    "pass",
    "pub",
    "raise",
    "return",
    "set",
    "str",
    "True",
    "tuple",
    "type",
    "until",
    "while",
    "wrap",
    "yield",
}

OPEN_BRACKETS: set[str] = {
    "(",
    "[",
    "{",
}

CLOSED_BRACKETS: set[str] = {
    ")",
    "]",
    "}",
}

##############################
# ERROR DEFINITION
##############################


class _LexerError(Error):
    pass


##############################
# STATE
##############################


class _State:
    initialized: bool = False
    program: str
    program_lines: Iterator[str]
    program_line: str
    # Index
    i: int = 0
    length: int
    char: str
    tokens: ClassVar[list[Token]] = []
    is_eof: bool = False
    indent_stack: ClassVar[list[int]] = [0]
    in_parens: int = 0
    consecutive_strings: int = 0
    line_start: int = 0
    line: int = 1
    column: int = 1
    consec_string_for_doc: Literal[2] = 2
    match_symbols: dict[str, Callable[[], None]]
    symbols: set[str]


_self: _State = _State()


##############################
# INITIALIZE
##############################


def init(program: str) -> None:
    """*Initialize the thing exactly once*.

    Args:
        program (str): *Quartz program*

    Raises:
        RuntimeError: *If already initialized*

    """
    if _self.initialized:
        msg: str = "Already initialized!"
        raise RuntimeError(msg)

    _self.program: str = program + "\n"

    _self.program_lines: Iterator[str] = iter(
        _self.program.replace(" ", "·").splitlines(),
    )
    _self.program_line: str = next(
        _self.program_lines,
    )
    _self.length: int = len(_self.program)
    _self.char: str = _self.program[_self.i] if _self.length > 0 else ""

    _self.initialized = True


##############################
# HELPER FUNCTIONS
##############################


def _raise_error(message: str) -> NoReturn:
    raise _LexerError(
        _self.line,
        _self.column,
        _self.program_line,
        message,
    )


def _check(char: str = "") -> bool:
    return _self.char == char


def _in(set_: set[str]) -> bool:
    return _self.char in set_


def _next() -> None:
    _self.i += 1
    _self.column += 1
    if _check("\n"):
        if _self.i != _self.length:
            _self.program_line: str = next(
                _self.program_lines,
            )
        _self.line += 1
        _self.column = 1
    if _self.i != _self.length:
        _self.char: str = _self.program[_self.i]
    else:
        _self.is_eof = True


def _token(tag: Tag, tok: str = "") -> None:
    _self.tokens.append(
        Token(
            tag,
            tok,
            _self.line,
            _self.column,
            _self.program_line,
        ),
    )


def _eof() -> None:
    while _self.indent_stack != [0]:
        _self.indent_stack.pop()
        _token(Tag.DEDENT)
    _token(Tag.EOF)


def _next_eof() -> bool:
    _next()
    if _self.is_eof:
        _eof()
        return True
    return False


##############################
# MAIN FUNCTION
##############################


def main() -> list[Token]:
    """*Lex a Quartz program*.

    Raises:
        RuntimeError: *If called before initialization*

    Returns:
        list[Token]: *Quartz `Token`'s*

    """
    if not _self.initialized:
        msg: str = "Called before initialization!"
        raise RuntimeError(msg)

    _self.match_symbols: dict[str, Callable[[], None]] = {
        "&": _ampersand,
        "*": _asterisk,
        "\\": _backslash,
        "!": _bang,
        "^": _caret,
        ":": _colon,
        "=": _equal,
        "#": _hashtag,
        "<": _l_angle,
        ",": _match_comma,
        ";": _match_semicolon,
        "-": _minus,
        "%": _percent,
        ".": _period,
        "|": _pipe,
        "+": _plus,
        ">": _r_angle,
        "/": _slash,
        "~": _tilde,
    }
    _self.symbols: set[str] = _self.match_symbols.keys()

    if _self.length == 0:
        _eof()
        return _self.tokens
    while _check("\n"):
        _next_eof()
    while not _self.is_eof:
        _match_char()
    return _self.tokens


##############################
# MATCH FUNCTIONS
##############################


def _match_char() -> None:
    if _check("\n"):
        _newline()
    elif _self.char.isspace():
        _next_eof()
    elif _self.char.isalpha() or _check("_") or _check("@"):
        _ident()
    elif _in(DIGITS):
        _integer()
    elif _check('"') or _check("'"):
        _string()
    else:
        _match_brackets()


def _match_brackets() -> None:
    if _in(OPEN_BRACKETS):
        _self.in_parens += 1
    elif _in(CLOSED_BRACKETS):
        _self.in_parens -= 1
    else:
        _match_remainders()
        return

    match _self.char:
        case "(":
            _token(Tag.L_PAREN)
        case ")":
            _token(Tag.R_PAREN)
        case "[":
            _token(Tag.L_BRACKET)
        case "]":
            _token(Tag.R_BRACKET)
        case "{":
            _token(Tag.L_BRACE)
        case "}":
            _token(Tag.R_BRACE)
        # The `else` block at the top already takes care of this.
        case _:
            pass

    _next_eof()


def _match_remainders() -> None:
    if not _in(_self.symbols):
        _next_eof()
        return
    _self.match_symbols[_self.char]()


def _match_semicolon() -> None:
    _token(Tag.SEMICOLON)
    _next_eof()


def _match_comma() -> None:
    _token(Tag.COMMA)
    _next_eof()


##############################
# CASE FUNCTIONS
##############################


def _newline() -> None:
    if _self.in_parens:
        _next_eof()
        return
    if _self.tokens:  # noqa: SIM102
        if _self.tokens[-1].tag != Tag.NEWLINE:
            _token(Tag.NEWLINE)
    _next_eof()
    if not _check("\n"):
        _indent()


def _indent() -> None:
    spaces: int = 0
    while not _self.is_eof and _check(" "):
        spaces += 1
        _next()
    if spaces % 4 != 0:
        _raise_error(
            """\
            Inconsistent indentation.
            Each indent level must be:
              - FOUR characters long
              - SPACES, not tabs""",
        )
    indents: int = int(spaces / 4)
    if indents > _self.indent_stack[-1]:
        _self.indent_stack.append(indents)
        _token(Tag.INDENT)
    if indents < _self.indent_stack[-1]:
        while indents < _self.indent_stack[-1]:
            _self.indent_stack.pop()
            _token(Tag.DEDENT)
        if indents != _self.indent_stack[-1]:
            _raise_error(
                """\
                Inconsistent indentation.
                Each indent level must be:
                  - FOUR characters long
                  - SPACES, not tabs""",
            )
    if _self.is_eof:
        _eof()


def _backslash() -> None:
    if _next_eof():
        return
    if not _check("\n"):
        return
    _next_eof()


def _hashtag() -> None:
    while not _check("\n"):
        if _next_eof():
            return
    if _check("\n"):
        _next()
        _indent()


def _ident() -> None:
    start: int = _self.i
    while not _self.is_eof and (_self.char.isalnum() or _check("_")):
        _next()
    if _check("?"):
        _next()
    ident: str = _self.program[start : _self.i]
    if ident:
        if ident in KEYWORDS:
            _token(Tag.KEYWORD, ident)
        else:
            _token(Tag.IDENT, ident)
    if _self.is_eof:
        _eof()


def _integer() -> None:
    start: int = _self.i
    while not _self.is_eof and _in(DIGITS):
        _next()
        if _check("."):
            _int_period(start, end=_self.i)
            return
    number: str = _self.program[start : _self.i]
    if number and not _check("."):
        _token(Tag.INTEGER, number)
    if _self.is_eof:
        _eof()


def _int_period(start: int = 0, end: int = 0) -> None:
    if _next_eof():
        return
    integer: str = _self.program[start:end]
    if _check("."):
        _token(Tag.INTEGER, integer)
        _period_period()
        return
    while not _self.is_eof and _in(DIGITS):
        _next()
    number: str = _self.program[start : _self.i]
    _token(Tag.FLOAT, number)
    if _self.is_eof:
        _eof()


def _period() -> None:
    if _next_eof():
        return
    if _check("."):
        _period_period()
    elif _in(DIGITS):
        _period_int()
    else:
        _token(Tag.PERIOD)


def _period_int() -> None:
    start: int = _self.i - 1
    while not _self.is_eof and _in(DIGITS):
        _next()
    number: str = _self.program[start : _self.i]
    _token(Tag.FLOAT, number)
    if _self.is_eof:
        _eof()


def _period_period() -> None:
    if _next_eof():
        return
    if _check("="):
        _token(Tag.PERIOD_PERIOD_EQUAL)
        _next_eof()
    elif _check("."):
        _token(Tag.PERIOD_PERIOD_PERIOD)
        _next_eof()
    else:
        _token(Tag.PERIOD_PERIOD)


def _string() -> None:
    quote: str = '"' if _check('"') else "'"
    start: int = _self.i
    if _next_eof():
        return
    while not (_self.is_eof or _check(quote)):
        _next()
    string: str = _self.program[start + 1 : _self.i]
    if _self.program[start] == _self.program[_self.i]:
        _token(Tag.STRING, string)
        if _next_eof():
            return
    if _self.is_eof:
        _eof()


##############################
# TEMPLATE FUNCTIONS
##############################


def _check_next(char: str, tag: Tag) -> bool:
    if not _check(char):
        return False
    _token(tag)
    _next_eof()
    return True


def _equal() -> None:
    if _next_eof():
        return
    if _check_next("=", Tag.EQUAL_EQUAL):
        return
    if not _check_next(">", Tag.EQUAL_ARROW):
        _token(Tag.EQUAL)


def _pipe() -> None:
    if _next_eof():
        return
    if not _check_next("=", Tag.PIPE_EQUAL):
        _token(Tag.PIPE)


def _colon() -> None:
    if _next_eof():
        return
    if not _check_next("=", Tag.COLON_EQUAL):
        _token(Tag.COLON)


def _percent() -> None:
    if _next_eof():
        return
    if _check_next("=", Tag.PERCENT_EQUAL):
        return
    if not _check_next("{", Tag.PERCENT_L_BRACE):
        _token(Tag.PERCENT)


def _asterisk() -> None:
    if _next_eof():
        return
    if not _check_next("=", Tag.ASTERISK_EQUAL):
        _token(Tag.ASTERISK)


def _plus() -> None:
    if _next_eof():
        return
    if not _check_next("=", Tag.PLUS_EQUAL):
        _token(Tag.PLUS)


def _minus() -> None:
    if _next_eof():
        return
    if _check_next("=", Tag.MINUS_EQUAL):
        return
    if _check(">"):
        _arrow()
    else:
        _token(Tag.MINUS)


def _arrow() -> None:
    if _next_eof():
        return
    if not _check_next("=", Tag.ARROW_EQUAL):
        _token(Tag.ARROW)


def _l_angle() -> None:
    if _next_eof():
        return
    if _check_next("=", Tag.L_ANGLE_EQUAL):
        return
    if _check("<"):
        _l_angle_l_angle()
    else:
        _token(Tag.L_ANGLE)


def _l_angle_l_angle() -> None:
    if _next_eof():
        return
    if _check_next("<", Tag.L_ANGLE_L_ANGLE_L_ANGLE):
        return
    if not _check_next("=", Tag.L_ANGLE_L_ANGLE_EQUAL):
        _token(Tag.L_ANGLE_L_ANGLE)


def _r_angle() -> None:
    if _next_eof():
        return
    if _check_next("=", Tag.R_ANGLE_EQUAL):
        return
    if _check(">"):
        _r_angle_r_angle()
    else:
        _token(Tag.R_ANGLE)


def _r_angle_r_angle() -> None:
    if _next_eof():
        return
    if not _check_next(
        "=",
        Tag.R_ANGLE_R_ANGLE_EQUAL,
    ):
        _token(Tag.R_ANGLE_R_ANGLE)


def _caret() -> None:
    if _next_eof():
        return
    if not _check_next("=", Tag.CARET_EQUAL):
        _token(Tag.CARET)


def _tilde() -> None:
    if _next_eof():
        return
    if _check_next("=", Tag.TILDE_EQUAL):
        return
    if not _check_next(">", Tag.TILDE_ARROW):
        _token(Tag.TILDE)


def _slash() -> None:
    if _next_eof():
        return
    if _check_next("=", Tag.SLASH_EQUAL):
        return
    if not _check_next("/", Tag.SLASH_SLASH):
        _token(Tag.SLASH)


def _ampersand() -> None:
    if _next_eof():
        return
    if not _check_next("=", Tag.AMPERSAND_EQUAL):
        _token(Tag.AMPERSAND)


def _bang() -> None:
    if _next_eof():
        return
    if _check_next("=", Tag.BANG_EQUAL):
        _raise_error(
            """\
            `!` is not an operator.
            Did you mean `!=` or `not`?""",
        )


def _dollar() -> None:
    if _next_eof():
        return
    if _check_next("{", Tag.DOLLAR_L_BRACE):
        _token(Tag.IDENT, "$")


##############################
# END OF FILE
##############################
