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

##############################
# LEXER
##############################


def tokenize(program):
    """
    Turn raw text into a list of tokens (strings).
    """

    tokens = []
    i, n = 0, len(program)

    while i < n:
        char = program[i]

        # Skip whitespace
        if char.isspace():
            i += 1
            continue

        matched = False

        # Match multi-char operators/symbols first.
        for cand in sorted(OPERATORS | SYMBOLS, key=len, reverse=True):
            if program.startswith(cand, i):
                tokens.append(cand)
                i += len(cand)
                matched = True
                break
        if matched:
            continue

        if char.isdigit():
            start = i
            has_dot = False
            while (i < n and (program[i].isdigit()
                        or (program[i]=="." and not has_dot))):
                if program[i] == ".":
                    has_dot = True
                i += 1
            tokens.append(program[start:i])
            continue

        if char.isalpha() or char == "_":
            start = i
            while (i < n and (program[i].isalnum() or program[i] == "_")):
                i += 1
            tokens.append(program[start:i])
            continue

        if char == '"':
            start = i
            i += 1
            while i < n and program[i] != '"':
                i += 1
            i += 1
            tokens.append(program[start:i])
            i += 1
            continue

        tokens.append(char)
        i += 1

    return tokens


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

    lexemes = tokenize(program)
    token_list = []

    for i, char in enumerate(lexemes):
        if char in OPERATORS:
            typ =  "Operator"
        elif char in SYMBOLS:
            typ = "Symbol"
        elif char in KEYWORDS:
            typ = "Keyword"
        elif char in DATA_TYPES:
            typ = "Data Type"
        elif char in {"TRUE", "FALSE"}:
            typ = "Boolean"
        elif char.startswith('"'):
            typ = "String"
        elif char.replace(".", "", 1).isdigit():
            typ = "Float" if "." in char else "Integer"
        else:
            typ = "Identifier"

        token_list.append(Token(i, char, typ))

    return token_list
