"""
The logic behind Quartz.
This module currently includes token definitions and a lexer.
"""

##############################
# TOKEN DEFINITIONS
##############################

DIGITS = "0123456789"

SINGLE_CHAR = {
    "{" : "LBRACE",
    "}" : "RBRACE",
    "(" : "LPAREN",
    ")" : "RPAREN",
    "[" : "LBRACK",
    "]" : "RBRACK",
    ":" : "COLON",
    ";" : "SEMICOLON",
    "," : "COMMA",
    "." : "PERIOD",
    "=" : "EQUALS_SIGN",
    "\'" : "SINGLE_QUOTE",
    "\"" : "DOUBLE_QUOTE",
    "+" : "ADD",
    "-" : "SUBTRACT",
    "*" : "MULTIPLY",
    "/" : "DIVIDE",
    "%" : "MODULO",
    "&" : "BITAND",
    "|" : "BITOR",
    "~" : "BITNOT",
    "^" : "BITXOR",
    "<" : "LESS_THAN",
    ">" : "GREATER_THAN",
    "!" : "NOT"
}

MULTI_CHAR = {
    ">>" : "PIPE",
    "~>" : "MATCH_ARROW",
    "==" : "EQUALS",
    "!=" : "NOT_EQUALS",
    ">=" : "GREAT_OR_EQUAL",
    "<=" : "LESS_OR_EQUAL",
    "//" : "FLOOR_DIVIDE",
    "**" : "EXPONENTIATE",
    ".." : "RANGE",
    "..=" : "RANGEINCLUDE",
    "#{" : "HASHSTART",
    "&&" : "AND",
    "||" : "OR",
    ">>>" : "BITRSHIFT",
    "<<<" : "BITLSHIFT",
}

DATA_TYPES = {
    "str" : "STRING",
    "int" : "INTEGER",
    "float" : "FLOAT",
    "tuple" : "TUPLE",
    "list" : "LIST",
    "hash" : "HASHMAP",
    "bool" : "BOOLEAN",
    "None" : "NONE"
}

ESSENTIALS = {
    "if" : "IF",
    "else" : "ELSE",
    "for" : "FOR",
    "forEach" : "FOR_EACH",
    "while" : "WHILE",
    "define" : "DEFINE",
    "TRUE" : "TRUE",
    "FALSE" : "FALSE",
    "and" : "AND",
    "or" : "OR",
    "not" : "NOT",
    "is" : "IS",
    "in" : "IN"
}

COMMANDS = {
    "print" : "PRINT",
    "append" : "APPEND",
    "appendTo" : "APPEND_TO"
}

LEXEME_DICT = SINGLE_CHAR | MULTI_CHAR | DATA_TYPES | ESSENTIALS | COMMANDS

##############################
# LEXER
##############################


def lexer(program: str) -> dict:
    """
    Separate lexemes in a program.
    """
    whitespace = " "
    prog = program + whitespace
    lex_list = []
    lex_dict = {}
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
                or next_char in LEXEME_DICT
                or lexeme in LEXEME_DICT):

            poss_lexeme = lexeme + next_char if next_char is not None else ""

            # Prevents multi-char tokens from being split up.
            if poss_lexeme in LEXEME_DICT:
                continue

            if lexeme:
                lex_list.append(lexeme)
                lexeme = ""

    for i, char in enumerate(lex_list):
        if char in LEXEME_DICT:
            lex_dict[char] = LEXEME_DICT[char]
        else:
            lex_dict[char] = "UNKNOWN"

    return lex_dict
