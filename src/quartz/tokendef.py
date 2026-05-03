"""`Error`, `Tag`, and `Token` definitions."""

##############################
# IMPORTS
##############################

from enum import Enum
from textwrap import dedent
from typing import NamedTuple

##############################
# TAGS
##############################


class Tag(Enum):
    """Word and character connections.

    Stored in alphabetical order.
    """

    AND = "and"
    AMPERSAND = "&"
    AMPERSAND_EQUAL = "&="
    ARROW = "->"
    ARROW_EQUAL = "->="
    ASTERISK = "*"
    ASTERISK_EQUAL = "*="
    AT_SIGN = "@"
    BANG_EQUAL = "!="
    CARET = "^"
    CARET_EQUAL = "^="
    COLON = ":"
    COLON_EQUAL = ":="
    COMMA = ","
    DEDENT = "DEDENT"
    DOCSTRING = "DOCSTRING"
    DOLLAR_L_BRACE = "${"
    ELLIPSIS = "..."
    EOF = "EOF"
    EQUAL = "="
    EQUAL_ARROW = "=>"
    EQUAL_EQUAL = "=="
    FALSE = "False"
    FLOAT = "FLOAT"
    IDENT = "IDENTIFIER"
    IN = "in"
    INDENT = "INDENT"
    INTEGER = "INTEGER"
    IS = "is"
    IS_NOT = "is not"
    KEYWORD = "KEYWORD"
    L_ANGLE = "<"
    L_ANGLE_EQUAL = "<="
    L_ANGLE_L_ANGLE = "<<"
    L_ANGLE_L_ANGLE_EQUAL = "<<="
    L_ANGLE_L_ANGLE_L_ANGLE = "<<<"
    L_BRACE = "{"
    L_BRACKET = "["
    L_PAREN = "("
    MINUS = "-"
    MINUS_EQUAL = "-="
    NEWLINE = "NEWLINE"
    NONE = "None"
    NOT = "not"
    NOT_IN = "not in"
    OR = "or"
    PERCENT = "%"
    PERCENT_EQUAL = "%="
    PERCENT_L_BRACE = "%{"
    PERIOD = "."
    PIPE = "|"
    PIPE_EQUAL = "|="
    PLUS = "+"
    PLUS_EQUAL = "+="
    R_ANGLE = ">"
    R_ANGLE_EQUAL = ">="
    R_ANGLE_R_ANGLE = ">>"
    R_ANGLE_R_ANGLE_EQUAL = ">>="
    R_BRACE = "}"
    R_BRACKET = "]"
    R_PAREN = ")"
    SEMICOLON = ";"
    SLASH = "/"
    SLASH_EQUAL = "/="
    SLASH_SLASH = "//"
    STRING = "STRING"
    TILDE = "~"
    TILDE_ARROW = "~>"
    TILDE_EQUAL = "~="
    TRUE = "True"


##############################
# TOKEN
##############################


class Token(NamedTuple):
    """A Quartz token."""

    tag: Tag
    tok: str
    ln: int
    col: int
    line: str


##############################
# ERROR
##############################


class Error(Exception):
    """Base class for all Quartz Exceptions."""

    def __init__(
        self,
        ln: int,
        col: int,
        line: str,
        message: str = "",
    ) -> None:
        """Raise an Error."""
        pointer: str = " " * col
        pointer: str = pointer[:-2] + "^"
        super().__init__(
            dedent(
                f"""\
                Ln {ln}, col {col}

                {line}
                {pointer}

                {dedent(message)}\n""",
            ),
        )
