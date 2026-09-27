# Copyright (c) Randall "R2" Dunkin
# Licensed under the MIT License.
"""*The FP-style parser*."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

import quartz.ast as q

if TYPE_CHECKING:
    from collections.abc import Callable

    from .tokendef import Error, Position, Token


def parse(lexed: list[Token]) -> Error | q.Program:  # noqa: C901
    """_summary_.

    Args:
        lexed (list[Tok]): **

    Returns:
        q.Program: **

    """
    type Toks = list[Token]

    class Result[T](Protocol):
        """*Monad that stores valuable error info*."""

        def __floordiv__[U](
            self,
            func: Callable[[list[T]], list[U]],
        ) -> Result[U]:
            """*Map*."""

        def __or__[U](self, other: Result[U]) -> Result[T] | Result[U]:
            """*Or*."""

    @dataclass(frozen=True, slots=True)
    class Left[T](Result):
        """*Failure*."""

        msg: str
        pos: Position

        def __floordiv__[U](
            self,
            func: Callable[[list[T]], list[U]],
        ) -> Result[U]:
            return Left(self.msg, self.pos)

        def __or__[U](self, other: Result[U]) -> Result[T] | Result[U]:
            return other

    @dataclass(frozen=True, slots=True)
    class Right[T](Result):
        """*Success*."""

        fst: list[T]
        rst: Toks

        def __floordiv__[U](
            self,
            func: Callable[[list[T]], list[U]],
        ) -> Result[U]:
            return Right(func(self.fst), self.rst)

        def __or__[U](self, other: Result[U]) -> Result[T] | Result[U]:
            return self

    class Parser[T]:
        def __init__(self, fn: Callable[[Toks], Result[T]]) -> None:
            self.fn = fn

        def __call__(self, stream: Toks) -> Result[T]:
            return self.fn(stream)

        def __floordiv__[U](
            self,
            func: Callable[[list[T]], list[U]],
        ) -> Parser[U]:
            return Parser(lambda toks: self(toks) // func)

        def __or__[U](self, other: Parser[U]) -> Parser[T] | Parser[U]:
            return Parser(lambda toks: self(toks) | other(toks))

    def tag(expected: str) -> Parser[Token]:
        def parser(stream: Toks) -> Result[Token]:
            first: Token = stream[0]
            if not stream or first.tag != expected:
                return Left(f"Expected token type '{expected}'", first.pos)
            return Right([first], stream[1:])

        return Parser(parser)

    def tok(expected: str) -> Parser[Token]:
        def parser(stream: Toks) -> Result[Token]:
            first: Token = stream[0]
            if not stream or first.tok != expected:
                return Left(f"Expected literal type '{expected}'", first.pos)
            return Right([first], stream[1:])

        return Parser(parser)

    ident: Parser[q.Ident] = Parser(
        tag("IDENT") // (lambda toks: [q.Ident(toks[-1].tok)]),
    )

    boolean: Parser[q.Constant] = Parser(
        (tok("True") | tok("False"))
        // (lambda toks: [q.Constant(toks[-1].tok == "True")]),
    )

    ellipsis: Parser[q.Constant] = Parser(
        tok("...") // (lambda _: [q.Constant(...)]),
    )

    float_p: Parser[q.Constant] = Parser(
        tag("FLOAT") // (lambda toks: [q.Constant(float(toks[-1].tok))]),
    )

    integer: Parser[q.Constant] = Parser(
        tag("INTEGER") // (lambda toks: [q.Constant(int(toks[-1].tok))]),
    )

    none: Parser[q.Constant] = Parser(
        tok("None") // (lambda _: [q.Constant(None)]),
    )

    string: Parser[q.Constant] = Parser(
        tag("STRING") // (lambda toks: [q.Constant(toks[-1].tok)]),
    )

    constant: Parser[q.Constant] = (
        boolean | ellipsis | float_p | integer | none | string
    )

    atom: Parser[q.Constant] | Parser[q.Ident] = constant | ident

    def program(parse_input: list[Token]) -> Error | q.Program:
        return q.Program(atom(parse_input))

    return program(lexed)
