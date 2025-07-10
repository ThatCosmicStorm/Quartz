"""
The logic behind Quartz.
This module currently includes token definitions and a lexer.
"""

from dataclasses import dataclass

##############################
# TOKEN DEFINITIONS
##############################

DIGITS = "0123456789"

OPERATORS = {
    "=", "<-",
    ">>", "??", "::", ";;", "~>",
    "+", "-", "*", "/",
    "**", "%",
    "==", "!=",
    "<", ">", "<=", ">=",
    "..", "..="
    "&", "|", "~", "^",
    ">>>", "<<<",
    "&&", "||", "!"
}

SYMBOLS = {
    "{", "#{", "}",
    "(", ")",
    "[", "]",
    ":", ";",
    ".", ",",
    "//"
}

KEYWORDS = {
    "if", "else",
    "for", "forEach",
    "while",
    "define", "return",
    "is", "in", "not"
    "and", "or"
}

DATA_TYPES = {
    "str",
    "int", "float",
    "tuple", "list", "hash",
    "bool",
    "None"
}

IDENTIFIERS = {
    "print",
    "append", "appendTo"
}

LEXEME_LIST = OPERATORS + SYMBOLS + KEYWORDS + DATA_TYPES + IDENTIFIERS

##############################
# LEXER
##############################


def separate_lexemes(program: str) -> list:
    """
    Separate lexemes in a program.
    """
    whitespace = " "
    prog = program + whitespace
    lex_list = []
    lexeme = ''

    for i, char in enumerate(prog):

        # If the character isn't whitespace, concatenate it.
        if char != whitespace:
            lexeme += char

        if i+1 < len(prog):
            next_char = prog[i + 1]
        else:
            next_char = None     # Prevents invalid index error.

        if (next_char is None
                or next_char == whitespace
                or next_char in LEXEME_LIST
                or lexeme in LEXEME_LIST):

            poss_lexeme = lexeme + next_char if next_char is not None else ""

            if char in DIGITS and next_char == ".":
                continue

            if char == "." and next_char in DIGITS:
                continue

            # Prevents multi-char tokens from being split up.
            if poss_lexeme in LEXEME_LIST:
                continue

            if lexeme:
                lex_list.append(lexeme)
                lexeme = ""

    return lex_list


@dataclass
class Token:
    """
    Stores token info.
    """
    number: int
    char: str
    type: str


def lexer(program: str) -> list:
    """
    Loosely categorizes lexemes.
    """

    lexemes = separate_lexemes(program)
    digit_check = 0
    token_list = []

    for i, char in enumerate(lexemes):
        if char in OPERATORS:
            token_list.append(Token(i, char, "Operator"))
        elif char in SYMBOLS:
            token_list.append(Token(i, char, "Symbol"))
        elif char in KEYWORDS:
            token_list.append(Token(i, char, "Keyword"))
        elif char in DATA_TYPES:
            token_list.append(Token(i, char, "Data Type"))

        elif char in ("TRUE", "FALSE"):
            token_list.append(Token(i, char, "Boolean"))

        elif char[0] == "\"" and char[-1] == "\"":
            token_list.append(Token(i, char, "String"))

        elif char[0] in DIGITS:
            for tup in enumerate(char):
                if tup[1] in DIGITS:
                    digit_check += 1
            if digit_check == len(char):
                token_list.append(Token(i, char, "Integer"))
            elif "." in char:
                token_list.append(Token(i, char, "Float"))

        elif "." in char:
            token_list.append(Token(i, char, "Float"))

        else:
            token_list.append(Token(i, char, "Identifier"))

    return token_list
