
from dataclasses import dataclass
from enum import Enum


##############################
# TOKEN DEFINITIONS
##############################


class Tag(Enum):
    EOF = "EOF"
    NEWLINE = "NEWLINE"
    STRING = "STRING"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"

    INDENT = "INDENT"
    DEDENT = "DEDENT"

    EQUAL = "="
    EQUAL_EQUAL = "=="
    EQUAL_ARROW = "=>"
    L_PAREN = "("
    R_PAREN = ")"
    L_BRACKET = "["
    R_BRACKET = "]"
    L_BRACE = "{"
    R_BRACE = "}"
    PIPE = "|"
    PIPE_EQUAL = "|="
    SEMICOLON = ";"
    COLON = ":"
    COLON_EQUAL = ":="
    PERIOD = "."
    PERIOD_PERIOD = ".."
    PERIOD_PERIOD_EQUAL = "..="
    PERIOD_PERIOD_PERIOD = "..."
    COMMA = ","
    PERCENT = "%"
    PERCENT_EQUAL = "%="
    PERCENT_L_BRACE = "%{"
    ASTERISK = "*"
    ASTERISK_EQUAL = "*="
    PLUS = "+"
    PLUS_EQUAL = "+="
    MINUS = "-"
    MINUS_EQUAL = "-="
    ARROW = "->"
    ARROW_EQUAL = "->="
    L_ANGLE = "<"
    L_ANGLE_EQUAL = "<="
    L_ANGLE_L_ANGLE = "<<"
    L_ANGLE_L_ANGLE_EQUAL = "<<="
    R_ANGLE = ">"
    R_ANGLE_EQUAL = ">="
    R_ANGLE_R_ANGLE = ">>"
    R_ANGLE_R_ANGLE_EQUAL = ">>="
    CARET = "^"
    CARET_EQUAL = "^="
    TILDE = "~"
    TILDE_EQUAL = "~="
    TILDE_ARROW = "~>"
    SLASH = "/"
    SLASH_EQUAL = "/="
    SLASH_SLASH = "//"
    AMPERSAND = "&"
    AMPERSAND_EQUAL = "&="
    BANG_EQUAL = "!="


@dataclass(slots=True, frozen=True)
class Token:
    tag: Tag | str
    tok: str | None = None
    ln: int = 1
    col: int = 1
    line: str = ""
