DIGITS = "0123456789"

token_dict = {
    "+" : "PLUS",
    "-" : "MINUS",
    "*" : "MUL",
    "/" : "DIV",
    "{" : "L_BRACE",
    "}" : "R_BRACE",
    ":" : "COLON",
    ";" : "SEMI"
}


def tokens(program):
    program = str(program)
    tokens = []
    characters = []
    chars = characters
    word = ""

    for char in range(0, len(program)):
        chars.append(program[char])

    for char in range(0, len(chars)):
        if chars[char] != " ":
            word += chars[char]
        else:
            tokens.append(word)
            word = ""
    tokens.append(word)

    return tokens


def label(value, string, lst):
    label = value + " : " + string
    lst.append(label)


def digit_check(string):
    digit = 0
    for i in range(0, len(string)):
        if string[i] in DIGITS: digit += 1
    if digit == len(string): return "INT"
    else: return "UNKNOWN"


def lexer(program):
    token_list = tokens(program)
    labels = []

    for tok in range(0, len(token_list)):
        if token_list[tok] in token_dict:
            label(
                token_dict[token_list[tok]],
                token_list[tok],
                labels
            )

        else:
            label(
                digit_check(token_list[tok]),
                token_list[tok],
                labels
            )

    return print(labels)