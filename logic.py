"""
The logic behind Quartz.
This module currently includes token definitions and a lexer.
"""

##############################
# TOKEN DEFINITIONS
##############################

DIGITS = "0123456789"

SINGLE_CHAR = [
    "{", "}",
    "(", ")",
    "[", "]",
    ":", ";",
    ",", ".",
    "_",
    "=",
    "\'", "\"",
    "+", "-",
    "*",
    "/", "%",
    "&", "|",
    "^", "~",
    "<", ">"
]
MULTI_CHAR = [
    ">>",
    "~>",
    "//",
    "..",
    "#[",
    "**",
    "==",
    "!=",
    ">=",
    "<=",
    "&&",
    "||",
    "!!",
    ">>>",
    "<<<",

]
KEYWORDS = [
    "if",
    "else",
    "for",
    "forEach",
    "while",
    "print",
    "append",
    "appendTo",
    "TRUE",
    "FALSE",
    "AND",
    "OR",
    "NOT",
    "is",
    "in",
    "not"
]
TOKEN_LIST = SINGLE_CHAR + MULTI_CHAR + KEYWORDS

##############################
# LEXER
##############################


def lexer(program: str) -> list:
    """
    Separate tokens in a program.
    """
    whitespace = " "
    prog = program + whitespace
    lex_list = []
    token = ''

    for i, char in enumerate(prog):

        # If the character isn't whitespace, concatenate it.
        if char != whitespace:
            token += char

        if i+1 < len(prog):
            next_char = prog[i + 1]
        else:
            next_char = None     # Prevents invalid index error.

        if (next_char is None
                or next_char == whitespace
                or next_char in TOKEN_LIST
                or token in TOKEN_LIST):

            poss_token = token + next_char if next_char is not None else ""

            # Prevents multi-char tokens from being split up.
            if poss_token in TOKEN_LIST:
                continue

            if token:
                lex_list.append(token)
                token = ''

    return lex_list
