#! /usr/bin/env python
# Copyright (c) Randall "R2" Dunkin
# Licensed under the MIT License.
"""*The interpreter for the Quartz programming language*."""

# ruff: disable[F401]
import ast
import sys
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING, Literal, Never

from .lexer import lex
from .parser import parse
from .tokendef import Error

if TYPE_CHECKING:
    from types import CodeType

    from .ast import Program
    from .tokendef import Position, Token
# ruff: enable[F401]

MINIMUM_ARGS: Literal[2] = 2


def main() -> None:
    """*Use `quartz.py` in the command line*."""

    def raise_error(message: str, pos: Position, code: str) -> Never:
        sys.exit(
            dedent(
                f"""\
                Ln {pos.ln}, col {pos.col}

                {code.split("\n")[pos.ln - 1]}
                {(" " * pos.col)[:-2]}^

                {message}\n""",
            ),
        )

    def print_debug_info(
        lexed: list[Token],
        parsed: Program,
    ) -> None:
        lex_info: str = "\nLexer Output:\n" + "\n".join(
            dedent(
                f"""{token.tag:<10}\
                {(token.tok if token.tag != "NEWLINE" else ""):<30}\
                Ln {token.pos.ln:<5}\
                Col {token.pos.col}""",
            )
            for token in lexed
        )
        parsed_info: str = "\nParser Output:\n" + "\n".join(
            map(repr, parsed.statements),
        )

        print(lex_info + parsed_info)

        # module_info = "\nAST Compiler Output:\n" + ast.dump(
        #     module,
        #     indent=4,
        # )

        # print(lex_info + parsed_info + module_info)

    def quartz(program: str, _filename: Path, *, debug: bool) -> None:
        lexed: Error | list[Token] = lex(program)
        if isinstance(lexed, Error):
            raise_error(lexed.msg, lexed.pos, program)
        parsed: Error | Program = parse(lexed)
        if isinstance(parsed, Error):
            raise_error(parsed.msg, parsed.pos, program)

        if debug:
            print_debug_info(lexed, parsed)

        # module: ast.Module = ast.Module()
        # ast.fix_missing_locations(module)

        # if debug:
        #     print_debug_info(lexed, parsed, module)

        # code: CodeType = compile(module, filename=filename, mode="exec")
        # exec(code, globals={})

    # Clear terminal
    print("\033[H\033[2J", end="")

    try:
        file: Path = Path(sys.argv[1])
    except IndexError:
        sys.exit(
            dedent(
                """\
                Usage: `quartz` `filename` [`-debug`]
                Please provide an existing path for `filename`.""",
            ),
        )
    try:
        with Path.open(file, encoding="utf8") as f:
            quartz(
                f.read(),
                file,
                debug=sys.argv[2] == "-debug"
                if len(sys.argv) >= MINIMUM_ARGS + 1
                else False,
            )
    except FileNotFoundError:
        sys.exit(f"File '{sys.argv[1]}' not found")
