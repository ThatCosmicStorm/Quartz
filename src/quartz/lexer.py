"""*The lexer for the Quartz programming language*."""

##############################
# IMPORTS
##############################

from typing import TYPE_CHECKING, NoReturn

from .tokendef import Error, Tag, Token

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

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
    "and",
    "as",
    "assert",
    "break",
    "case",
    "class",
    "continue",
    "del",
    "dict",
    "else",
    "False",
    "float",
    "fn",
    "for",
    "from",
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
    "set",
    "str",
    "struct",
    "True",
    "tuple",
    "type",
    "until",
    "while",
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
# MAIN CLASS
##############################


class Lexer:
    """*The Quartz Lexer*."""

    def __init__(self, program: str) -> None:
        """*Lex a Quartz program*.

        Args:
            program (str): *File input*

        """
        self._i: int = 0
        self._tokens: list[Token] = []
        self._is_eof: bool = False
        self._indent_stack: list[int] = [0]
        self._in_parens: int = 0
        self._line_start: int = 0
        self._line: int = 1
        self._column: int = 1

        self._program: str = program + "\n"
        self._program_lines: Iterator[str] = iter(
            self._program.replace(" ", "·").splitlines(),
        )
        self._program_line: str = next(
            self._program_lines,
        )
        self._length: int = len(self._program)
        self._char: str = self._program[0] if self._length > 0 else ""

        self._match_symbols: dict[str, Callable[[], None]] = {
            "&": self._ampersand,
            "*": self._asterisk,
            "@": self._match_at_sign,
            "\\": self._backslash,
            "!": self._bang,
            "^": self._caret,
            ":": self._colon,
            "$": self._dollar,
            "=": self._equal,
            "#": self._hashtag,
            "<": self._l_angle,
            ",": self._match_comma,
            ";": self._match_semicolon,
            "-": self._minus,
            "%": self._percent,
            ".": self._period,
            "|": self._pipe,
            "+": self._plus,
            ">": self._r_angle,
            "/": self._slash,
            "~": self._tilde,
        }
        self._symbols: set[str] = set(self._match_symbols.keys())

        if self._length == 0:
            self._eof()
            return
        while self._check("\n"):
            self._next_eof()
        while not self._is_eof:
            self._match_char()

    ##########################
    # Helper Functions
    ##########################

    def _raise_error(self, message: str) -> NoReturn:
        raise _LexerError(
            self._line,
            self._column,
            self._program_line,
            message,
        )

    def _check(self, char: str) -> bool:
        return self._char == char

    def _in(self, set_: set[str]) -> bool:
        return self._char in set_

    def _next(self) -> None:
        self._i += 1
        self._column += 1
        if self._check("\n"):
            if self._i != self._length:
                self._program_line: str = next(
                    self._program_lines,
                )
            self._line += 1
            self._column = 1
        if self._i != self._length:
            self._char: str = self._program[self._i]
        else:
            self._is_eof = True

    def _token(self, tag: Tag, tok: str = "") -> None:
        self._tokens.append(
            Token(
                tag,
                tok,
                self._line,
                self._column,
                self._program_line,
            ),
        )

    def _eof(self) -> None:
        while self._indent_stack != [0]:
            self._indent_stack.pop()
            self._token(Tag.DEDENT)
        self._token(Tag.EOF)

    def _next_eof(self) -> bool:
        self._next()
        if self._is_eof:
            self._eof()
            return True
        return False

    ##########################
    # Main Getter Method
    ##########################

    def get_tokens(self) -> list[Token]:
        """*Return the output of the lexer*.

        Returns:
            list[Token]: *Lexer output*

        """
        return self._tokens

    ##########################
    # Match Functions
    ##########################

    def _match_char(self) -> None:
        if self._check("\n"):
            self._newline()
        elif self._char.isspace():
            self._next_eof()
        elif self._char.isalpha() or self._check("_"):
            self._ident()
        elif self._in(DIGITS):
            self._integer()
        elif self._check('"') or self._check("'"):
            self._string()
        else:
            self._match_brackets()

    def _match_brackets(self) -> None:
        if self._in(OPEN_BRACKETS):
            self._in_parens += 1
        elif self._in(CLOSED_BRACKETS):
            self._in_parens -= 1
        else:
            self._match_remainders()
            return

        match self._char:
            case "(":
                self._token(Tag.L_PAREN)
            case ")":
                self._token(Tag.R_PAREN)
            case "[":
                self._token(Tag.L_BRACKET)
            case "]":
                self._token(Tag.R_BRACKET)
            case "{":
                self._token(Tag.L_BRACE)
            case "}":
                self._token(Tag.R_BRACE)

        self._next_eof()

    def _match_remainders(self) -> None:
        if not self._in(self._symbols):
            self._next_eof()
            return
        self._match_symbols[self._char]()

    def _match_semicolon(self) -> None:
        self._token(Tag.SEMICOLON)
        self._next_eof()

    def _match_comma(self) -> None:
        self._token(Tag.COMMA)
        self._next_eof()

    def _match_at_sign(self) -> None:
        self._token(Tag.AT_SIGN)
        self._next_eof()

    ##############################
    # Case Functions
    ##############################

    def _newline(self) -> None:
        if self._in_parens:
            self._next_eof()
            return
        if self._tokens:  # noqa: SIM102
            if self._tokens[-1].tag != Tag.NEWLINE:
                self._token(Tag.NEWLINE)
        self._next_eof()
        if not self._check("\n"):
            self._indent()

    def _indent(self) -> None:
        spaces: int = 0
        while not self._is_eof and self._check(" "):
            spaces += 1
            self._next()
        if spaces % 4 != 0:
            self._raise_error(
                """\
                Inconsistent indentation.
                Each indent level must be:
                - FOUR characters long
                - SPACES, not tabs""",
            )
        indents: int = int(spaces / 4)
        if indents > self._indent_stack[-1]:
            self._indent_stack.append(indents)
            self._token(Tag.INDENT)
        if indents < self._indent_stack[-1]:
            while indents < self._indent_stack[-1]:
                del self._indent_stack[-1]
                self._token(Tag.DEDENT)
            if indents != self._indent_stack[-1]:
                self._raise_error(
                    """\
                    Inconsistent indentation.
                    Each indent level must be:
                    - FOUR characters long
                    - SPACES, not tabs""",
                )
        if self._is_eof:
            self._eof()

    def _backslash(self) -> None:
        if self._next_eof():
            return
        if not self._check("\n"):
            return
        self._next_eof()

    def _hashtag(self) -> None:
        while not self._check("\n"):
            if self._next_eof():
                return
        if self._check("\n"):
            self._next()
            self._indent()

    def _ident(self) -> None:
        start: int = self._i
        while not self._is_eof and (self._char.isalnum() or self._check("_")):
            self._next()
        if self._check("?"):
            self._next()
        ident: str = self._program[start : self._i]
        if ident:
            if ident in KEYWORDS:
                self._keyword(ident)
            else:
                self._token(Tag.IDENT, ident)
        if self._is_eof:
            self._eof()

    def _keyword(self, ident: str) -> None:  # noqa: C901, PLR0912
        match ident:
            case "and":
                self._token(Tag.AND)
            case "or":
                self._token(Tag.OR)
            case "not":
                if self._tokens[-1].tag == Tag.IS:
                    del self._tokens[-1]
                    self._token(Tag.IS_NOT)
                else:
                    self._token(Tag.NOT)
            case "is":
                self._token(Tag.IS)
            case "in":
                if self._tokens[-1].tag == Tag.NOT:
                    del self._tokens[-1]
                    self._token(Tag.NOT_IN)
                else:
                    self._token(Tag.IN)
            case "True":
                self._token(Tag.TRUE)
            case "False":
                self._token(Tag.FALSE)
            case "None":
                self._token(Tag.NONE)
            case _:
                self._token(Tag.KEYWORD, ident)

    def _integer(self) -> None:
        start: int = self._i
        while not self._is_eof and self._in(DIGITS):
            self._next()
            if self._check("."):
                self._int_period(start)
                return
        number: str = self._program[start : self._i]
        if number and not self._check("."):
            self._token(Tag.INTEGER, number)
        if self._is_eof:
            self._eof()

    def _int_period(self, start: int = 0) -> None:
        if self._next_eof():
            return
        while not self._is_eof and self._in(DIGITS):
            self._next()
        number: str = self._program[start : self._i]
        self._token(Tag.FLOAT, number)
        if self._is_eof:
            self._eof()

    def _period(self) -> None:
        if self._next_eof():
            return
        if self._in(DIGITS):
            self._period_int()
        if not self._check("."):
            self._token(Tag.PERIOD)
            return
        if self._next_eof():
            return
        if not self._check("."):
            self._raise_error(
                """\
                `..` is not a valid token.
                Did you mean `.` or `...`?""",
            )
        self._token(Tag.ELLIPSIS)

    def _period_int(self) -> None:
        start: int = self._i - 1
        while not self._is_eof and self._in(DIGITS):
            self._next()
        number: str = self._program[start : self._i]
        self._token(Tag.FLOAT, number)
        if self._is_eof:
            self._eof()

    def _string(self) -> None:
        quote: str = '"' if self._check('"') else "'"
        start: int = self._i
        if self._next_eof():
            return
        while not (self._is_eof or self._check(quote)):
            self._next()
        string: str = self._program[start + 1 : self._i]
        if self._program[start] == self._program[self._i]:
            self._token(Tag.STRING, string)
            if self._next_eof():
                return
        if self._is_eof:
            self._eof()

    ##############################
    # Template Functions
    ##############################

    def _check_next(self, char: str, tag: Tag) -> bool:
        if not self._check(char):
            return False
        self._token(tag)
        self._next_eof()
        return True

    def _equal(self) -> None:
        if self._next_eof():
            return
        if self._check_next("=", Tag.EQUAL_EQUAL):
            return
        if not self._check_next(">", Tag.EQUAL_ARROW):
            self._token(Tag.EQUAL)

    def _pipe(self) -> None:
        if self._next_eof():
            return
        if not self._check_next("=", Tag.PIPE_EQUAL):
            self._token(Tag.PIPE)

    def _colon(self) -> None:
        if self._next_eof():
            return
        if not self._check_next("=", Tag.COLON_EQUAL):
            self._token(Tag.COLON)

    def _percent(self) -> None:
        if self._next_eof():
            return
        if self._check_next("=", Tag.PERCENT_EQUAL):
            return
        if self._check_next("{", Tag.PERCENT_L_BRACE):
            self._in_parens += 1
            return
        self._token(Tag.PERCENT)

    def _asterisk(self) -> None:
        if self._next_eof():
            return
        if not self._check_next("=", Tag.ASTERISK_EQUAL):
            self._token(Tag.ASTERISK)

    def _plus(self) -> None:
        if self._next_eof():
            return
        if not self._check_next("=", Tag.PLUS_EQUAL):
            self._token(Tag.PLUS)

    def _minus(self) -> None:
        if self._next_eof():
            return
        if self._check_next("=", Tag.MINUS_EQUAL):
            return
        if self._check(">"):
            self._arrow()
        else:
            self._token(Tag.MINUS)

    def _arrow(self) -> None:
        if self._next_eof():
            return
        if not self._check_next("=", Tag.ARROW_EQUAL):
            self._token(Tag.ARROW)

    def _l_angle(self) -> None:
        if self._next_eof():
            return
        if self._check_next("=", Tag.L_ANGLE_EQUAL):
            return
        if self._check("<"):
            self._l_angle_l_angle()
        else:
            self._token(Tag.L_ANGLE)

    def _l_angle_l_angle(self) -> None:
        if self._next_eof():
            return
        if self._check_next("<", Tag.L_ANGLE_L_ANGLE_L_ANGLE):
            return
        if not self._check_next("=", Tag.L_ANGLE_L_ANGLE_EQUAL):
            self._token(Tag.L_ANGLE_L_ANGLE)

    def _r_angle(self) -> None:
        if self._next_eof():
            return
        if self._check_next("=", Tag.R_ANGLE_EQUAL):
            return
        if self._check(">"):
            self._r_angle_r_angle()
        else:
            self._token(Tag.R_ANGLE)

    def _r_angle_r_angle(self) -> None:
        if self._next_eof():
            return
        if not self._check_next("=", Tag.R_ANGLE_R_ANGLE_EQUAL):
            self._token(Tag.R_ANGLE_R_ANGLE)

    def _caret(self) -> None:
        if self._next_eof():
            return
        if not self._check_next("=", Tag.CARET_EQUAL):
            self._token(Tag.CARET)

    def _tilde(self) -> None:
        if self._next_eof():
            return
        if self._check_next("=", Tag.TILDE_EQUAL):
            return
        if not self._check_next(">", Tag.TILDE_ARROW):
            self._token(Tag.TILDE)

    def _slash(self) -> None:
        if self._next_eof():
            return
        if self._check_next("=", Tag.SLASH_EQUAL):
            return
        if not self._check_next("/", Tag.SLASH_SLASH):
            self._token(Tag.SLASH)

    def _ampersand(self) -> None:
        if self._next_eof():
            return
        if not self._check_next("=", Tag.AMPERSAND_EQUAL):
            self._token(Tag.AMPERSAND)

    def _bang(self) -> None:
        if self._next_eof():
            return
        if not self._check_next("=", Tag.BANG_EQUAL):
            self._raise_error(
                """\
                `!` is not an operator.
                Did you mean `!=` or `not`?""",
            )

    def _dollar(self) -> None:
        if self._next_eof():
            return
        if self._check_next("{", Tag.DOLLAR_L_BRACE):
            self._in_parens += 1
            return
        self._raise_error(
            """\
            `$` is not an identifiable token.
            Did you mean `${` for a set?""",
        )
