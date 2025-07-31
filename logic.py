"""_Token definitions, tokenizer, lexer, and a parser._
"""

##############################
# TOKEN DEFINITIONS
##############################

DIGITS = "0123456789"

OPERATORS = {
    "=", "<-", "->",
    ">>", ":>", "=>", "~>",
    "+", "-", "*", "/",
    "**", "%",
    "==", "!=",
    "<", ">", "<=", ">=",
    "..", "..=",
    "&", "|", "~", "^",
    ">>>", "<<<",
    "&&", "||", "!",
}

SYMBOLS = {
    "{", "#{",
    "%{", "}",
    "(", ")",
    "[", "]",
    ":", ";",
    ".", ",",
}

KEYWORDS = {
    "if", "else",
    "for", "forEach",
    "while",
    "define", "return",
    "is", "in", "not",
    "and", "or",
    "map",
}

DATA_TYPES = {
    "str",
    "int", "float",
    "tuple", "list", "hash",
    "bool",
    "NONE",
}

##############################
# LEXER
##############################


def tokenize(program: str) -> list:
    """_Organize a program into its tokens and types._

    Args:
        program (str): _The entire program in one complete string._

    Returns:
        list: _Each token and its type are grouped into an item._
    """

    tokens = []
    index, length = 0, len(program)
    i, n = index, length
    big_ops_first = sorted(OPERATORS | SYMBOLS, key=len, reverse=True)

    while i < n:
        char = program[i]
        next_char = program[i+1] if i+1 != n else ""

        if char.isspace():
            i += 1
            continue

        if char=="/" and next_char=="/":
            while i<n and program[i]!="\n":
                i += 1
            continue

        if char=="/" and next_char=="*":
            while (i < n
                   and (program[i] == "*"
                        and next_char == "/")):
                i += 1
                next_char = program[i+1] if i+1 != n else ""
            i += 1
            continue

        if char.isalpha() or char == "_":
            start = i
            while (i < n
                   and (program[i].isalnum()
                        or program[i] == "_")):
                i += 1
            token_content = program[start:i]
            current_token = [token_content]
            if token_content in KEYWORDS:
                current_token.append("Keyword")
            elif token_content in DATA_TYPES:
                current_token.append("Data Type")
            elif token_content in {"TRUE", "FALSE"}:
                current_token.append("Boolean")
            else:
                current_token.append("Identifier")
            tokens.append(current_token)
            continue

        if (char.isdigit()
                or (char=="." and next_char.isdigit())):
            start = i
            has_dot = False
            while (i < n
                   and (program[i].isdigit()
                        or (program[i]=="." and not has_dot))):
                if program[i] == ".":
                    if program[i+1] == ".":
                        break
                    else:
                        has_dot = True
                i += 1
            current_token = [program[start:i]]
            if "." in current_token[0]:
                current_token.append("Float")
            else:
                current_token.append("Integer")
            tokens.append(current_token)
            continue

        if char == '"':
            start = i
            i += 1
            while i<n and program[i]!='"':
                i += 1
            i += 1
            current_token = [program[start:i], "String"]
            tokens.append(current_token)
            i += 1
            continue

        for candidate in big_ops_first:
            if program.startswith(candidate, i):
                current_token = [candidate]
                if candidate in SYMBOLS:
                    current_token.append("Symbol")
                elif candidate in OPERATORS:
                    current_token.append("Operator")
                tokens.append(current_token)
                i += len(candidate)
                break

    return tokens





