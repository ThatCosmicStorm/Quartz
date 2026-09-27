# Copyright (c) Randall "R2" Dunkin
# Licensed under the MIT License.
"""*The Quartz lexer*."""

import re
from typing import Final

from .tokendef import Error, Position, Token

PATTERNS: Final[dict[str, str]] = {
    "NEWLINE": r"(?:\r?\n|\r)[ \t]*",
    "PIPE_GT_EQ": r"\|>=",
    "GT_GT_EQ": r">>=",
    "LT_LT_EQ": r"<<=",
    "ELLIPSIS": r"\.\.\.",
    "DOLLAR_L_BRACE": r"\$\{",
    "PERCENT_L_BRACE": r"%\{",
    "PIPE_GT": r"\|>",
    "PIPE_LT": r"<\|",
    "EQ_GT": r"=>",
    "DASH_GT": r"->",
    "GT_GT": r">>",
    "LT_LT": r"<<",
    "TILDE_GT": r"~>",
    "PLUS_EQ": r"\+=",
    "DASH_EQ": r"-=",
    "AST_EQ": r"\*=",
    "SLASH_EQ": r"/=",
    "CARET_EQ": r"\^=",
    "PERCENT_EQ": r"%=",
    "AMP_EQ": r"&=",
    "PIPE_EQ": r"\|=",
    "TILDE_EQ": r"~=",
    "EQ_EQ": r"==",
    "BANG_EQ": r"!=",
    "LT_EQ": r"<=",
    "GT_EQ": r">=",
    "AST_AST": r"\*\*",
    "COLON": r":",
    "EQ": r"=",
    "COMMA": r",",
    "PIPE": r"\|",
    "L_PAREN": r"\(",
    "R_PAREN": r"\)",
    "L_BRACE": r"\{",
    "R_BRACE": r"\}",
    "BACK": r"\\",
    "AST": r"\*",
    "TILDE": r"~",
    "AMP": r"&",
    "PLUS": r"\+",
    "DASH": r"-",
    "SLASH": r"/",
    "SLASH_SLASH": r"//",
    "PERCENT": r"%",
    "DOT": r"\.",
    "CARET": r"\^",
    "L_BRACK": r"\[",
    "R_BRACK": r"\]",
    "LT": r"<",
    "GT": r">",
    "IDENT": r"[@!]?[a-zA-Z_]\w*\??",
    "INTEGER": r"\d+",
    "FLOAT": r"(\d+\.\d*|\.\d+|\d+)[eE][+\-]?\d+|\d+\.\d*|\.\d+",
    "STRING": r"""(\"\"\".*?\"\"\"|'''.*?''\
|\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')""",
    "WHITESPACE": r"\s+",
    "EOF": r"\z",
    "MISMATCH": r".",
}

KEYWORDS: Final[set[str]] = {
    "continue",
    "finally",
    "delete",
    "except",
    "import",
    "return",
    "unless",
    "break",
    "match",
    "raise",
    "until",
    "while",
    "yield",
    "False",
    "case",
    "else",
    "from",
    "pass",
    "then",
    "type",
    "with",
    "None",
    "True",
    "and",
    "for",
    "has",
    "not",
    "pub",
    "try",
    "var",
    "as",
    "fn",
    "if",
    "in",
    "or",
}


def lex(
    code: str,
) -> Error | list[Token]:
    """*Pure lexer function*.

    Args:
        patterns (dict[str, str]): **
        keywords (set[str]): **
        code (str): **

    Returns:
        list[LexResult]: **

    """

    def get_position(code: str, index: int) -> Position:
        prefix: str = code[:index]
        last: int = prefix.rfind("\n")
        return Position(
            ln=prefix.count("\n") + 1,
            col=index + 1 if last == -1 else index - last,
        )

    def match_to_result(code: str, match: re.Match[str]) -> Token:
        char: str = match.group()
        pos: Position = get_position(code, match.start())
        kind: str | None = match.lastgroup
        return Token(
            "ERROR"
            if kind is None or kind == "MISMATCH"
            else kind
            if char not in KEYWORDS
            else char.upper(),
            char,
            pos,
        )

    master_regex: re.Pattern[str] = re.compile(
        r"|".join(
            f"(?P<{name}>{pattern})" for name, pattern in PATTERNS.items()
        ),
    )

    results: list[Token] = [
        match_to_result(code, match) for match in master_regex.finditer(code)
    ]

    return next(
        (
            Error(f"Unexpected character '{res.tok}'", res.pos)
            for res in results
            if res.tag == "ERROR"
        ),
        results,
    )
