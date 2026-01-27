"""Carries `Error`, `Tag`, and `Token`."""

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

    AMPERSAND = "&"
    AMPERSAND_EQUAL = "&="
    ARROW = "->"
    ARROW_EQUAL = "->="
    ASTERISK = "*"
    ASTERISK_EQUAL = "*="
    BANG_BANG = "!!"
    BANG_EQUAL = "!="
    CARET = "^"
    CARET_EQUAL = "^="
    COLON = ":"
    COLON_EQUAL = ":="
    COMMA = ","
    DEDENT = "DEDENT"
    DOCSTRING = "DOCSTRING"
    DOLLAR_L_BRACE = "${"
    EOF = "EOF"
    EQUAL = "="
    EQUAL_ARROW = "=>"
    EQUAL_EQUAL = "=="
    EROTEME_EROTEME = "??"
    FLOAT = "FLOAT"
    IDENT = "IDENTIFIER"
    INDENT = "INDENT"
    INTEGER = "INTEGER"
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
    PERCENT = "%"
    PERCENT_EQUAL = "%="
    PERCENT_L_BRACE = "%{"
    PERIOD = "."
    PERIOD_PERIOD = ".."
    PERIOD_PERIOD_EQUAL = "..="
    PERIOD_PERIOD_PERIOD = "..."
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


##############################
# TOKEN
##############################


class Token(NamedTuple):
    """The sole Quartz Token class."""

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
        pointer = pointer[:-2] + "^"
        super().__init__(
            dedent(
                f"""\
                Ln {ln}, col {col}

                {line}
                {pointer}

                {dedent(message)}\n""",
            ),
        )

##############################
# END OF FILE
##############################
