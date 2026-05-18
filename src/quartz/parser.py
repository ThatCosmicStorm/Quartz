"""*The parser for the Quartz programming language*."""

##############################
# IMPORTS
##############################

from typing import TYPE_CHECKING, Any, NoReturn

import quartz.ast as q

from .tokendef import Error, Tag, Token

if TYPE_CHECKING:
    from collections.abc import Callable

##############################
# SET CONSTANTS
##############################

# All sets declared here and in the main class
# that deal with words and letters
# are organized in alphabetical order,
# with non-alphabetical symbols coming first in no particular order.

ASSIGNMENT_OPS: set[Tag] = {
    Tag.AMPERSAND_EQUAL,
    Tag.ARROW_EQUAL,
    Tag.ASTERISK_EQUAL,
    Tag.CARET_EQUAL,
    Tag.EQUAL,
    Tag.L_ANGLE_L_ANGLE_EQUAL,
    Tag.MINUS_EQUAL,
    Tag.PERCENT_EQUAL,
    Tag.PIPE_EQUAL,
    Tag.PLUS_EQUAL,
    Tag.R_ANGLE_R_ANGLE_EQUAL,
    Tag.SLASH_EQUAL,
    Tag.TILDE_EQUAL,
}

COMPARISON_OPS: set[Tag] = {
    Tag.BANG_EQUAL,
    Tag.EQUAL_EQUAL,
    Tag.IN,
    Tag.IS,
    Tag.IS_NOT,
    Tag.L_ANGLE,
    Tag.L_ANGLE_EQUAL,
    Tag.NOT,
    Tag.NOT_IN,
    Tag.R_ANGLE,
    Tag.R_ANGLE_EQUAL,
}

##############################
# ERROR DEFINITION
##############################


class _ParserError(Error):
    pass


##############################
# MAIN CLASS
##############################


class Parser:
    """*The Quartz Parser*."""

    def __init__(self, tokens: list[Token]) -> None:
        """*Parse a list of Quartz tokens*.

        Args:
            tokens (list[Token]): *List of Quartz tokens*

        """
        self._i: int = 0

        self._tokens: list[Token] = tokens
        self._token: Token = self._tokens[self._i]
        self._length: int = len(self._tokens)

        self._parse_statements: dict[str, Callable[[], q.Stmt]] = {
            "del": self._del,
            "fn": self._function_definition,
            "for": self._for,
            "if": self._if,
            "unless": self._if,
            "until": self._while,
            "while": self._while,
        }
        self._keywords: set[str] = set(self._parse_statements.keys())

        self._simple_statements: set[Any] = {
            q.Assign,
            q.Delete,
            q.ExprStmt,
            q.Return,
        }

        self._primary_dict: dict[Tag, Callable[[], q.Constant]] = {
            Tag.ELLIPSIS: self._ellipsis,
            Tag.FALSE: self._false,
            Tag.FLOAT: self._float,
            Tag.INTEGER: self._integer,
            Tag.NONE: self._none,
            Tag.STRING: self._string,
            Tag.TRUE: self._true,
        }
        self._primary_dict_keys: set[Tag] = set(self._primary_dict.keys())

        self._program: q.Program = q.Program(self._statements())

    ##########################
    # Helper Functions
    ##########################

    def _raise_error(self, message: str = "") -> NoReturn:
        raise _ParserError(
            self._token.ln,
            self._token.col,
            self._token.line,
            message,
        )

    def _next(self, num: int = 1) -> Token:
        if (next_i := self._i + num) >= self._length:
            self._raise_error(f"No token found at index #{next_i}")
        past_token: Token = self._token
        self._i: int = next_i
        self._token: Token = self._tokens[self._i]
        return past_token

    def _check(self, *types: str | Tag, ahead: int = 0) -> bool:
        i: int = self._i + ahead
        if_ahead: bool = i < self._length
        in_: bool = any(
            typ in {self._tokens[i].tag, self._tokens[i].tok} for typ in types
        )
        return if_ahead and in_

    def _in(self, set_: set[Tag] | set[str], ahead: int = 0) -> bool:
        i: int = self._i + ahead
        if_ahead: bool = i < self._length
        tag: bool = self._tokens[i].tag in set_
        tok: bool = self._tokens[i].tok in set_
        return if_ahead and (tag or tok)

    def _match(self, type_: str | Tag) -> Token | None:
        if type_ in {self._token.tag, self._token.tok}:
            return self._next()
        return None

    def _expect(self, type_: str | Tag) -> Token:
        if type_ in {self._token.tok, self._token.tag}:
            return self._next()
        return self._raise_error(
            f"Expected {type_}, got {self._token.tok or self._token.tag}",
        )

    ##########################
    # Main Getter Function
    ##########################

    def get_program(self) -> q.Program:
        """*Return the output of the parser*.

        Returns:
            q.Program: *Parser output*

        """
        return self._program

    ##########################
    # Statements
    ##########################

    def _statements(self) -> list[q.Stmt]:
        statements: list[q.Stmt] = []
        while not self._check(Tag.EOF):
            statements.append(self._stmt())
        return statements

    def _stmt(self) -> q.Stmt:
        stmt: q.Stmt = self._match_stmt()
        if type(stmt) in self._simple_statements:
            self._expect(Tag.NEWLINE)
        return stmt

    def _match_stmt(self) -> q.Stmt:
        if self._in(self._keywords):
            return self._parse_statements[self._token.tok]()
        expr: q.Expr = self._expr()
        if self._match(Tag.EQUAL):
            return self._assign(expr)
        return q.ExprStmt(expr)

    ##############################
    # SIMPLE CASES
    ##############################

    def _assign(self, first: q.Expr) -> q.Assign:
        targets: list[q.Expr] = [first, self._expr()]
        while self._match(Tag.EQUAL):
            targets.append(self._expr())
        value: q.Expr = targets.pop()
        return q.Assign(targets, value)

    def _del(self) -> q.Delete:
        self._expect("del")
        targets: list[q.Expr] = [self._expr()]
        while self._match(Tag.COMMA):
            targets.append(self._expr())
        return q.Delete(targets)

    def _return(self) -> q.Return:
        self._expect("return")
        if self._check(Tag.NEWLINE):
            return q.Return()
        return q.Return(self._expr())

    ##############################
    # COMPOUND CASES
    ##############################

    def _if(self) -> q.If:
        if self._match("unless"):
            test: q.UnaryOp = q.UnaryOp(Tag.NOT, self._expr())
            body: list[q.Stmt] = self._suite()
            return q.If(test, body, [])
        self._expect("if")
        test: q.Expr = self._expr()
        body: list[q.Stmt] = self._suite()
        orelse: list[q.Stmt] = []
        while self._check("else") and self._check("if", ahead=1):
            self._next()
            orelse: list[q.Stmt] = [self._if()]
        if self._match("else"):
            orelse: list[q.Stmt] = self._suite()
        return q.If(test, body, orelse)

    def _for(self) -> q.For:
        self._expect("for")
        target: q.Expr | None = None
        iter_: q.Expr = self._postfix()
        if self._match(Tag.IN):
            target: q.Expr = iter_
            iter_: q.Expr = self._expr()
        body: list[q.Stmt] = self._suite()
        orelse: list[q.Stmt] = []
        if self._match("else"):
            orelse: list[q.Stmt] = self._suite()
        return q.For(target or q.Ident("_"), iter_, body, orelse)

    def _while(self) -> q.While:
        word: str = self._next().tok
        test: q.Expr = self._expr()
        body: list[q.Stmt] = self._suite()
        orelse: list[q.Stmt] = []
        if self._match("else"):
            orelse: list[q.Stmt] = self._suite()
        return q.While(
            test if word == "while" else q.UnaryOp(Tag.NOT, test),
            body,
            orelse,
        )

    def _function_definition(self) -> q.FunctionDefinition:
        self._expect("fn")
        name: str = self._expect(Tag.IDENT).tok
        self._expect(Tag.L_PAREN)
        args: q.Arguments = q.Arguments()
        if not self._check(Tag.R_PAREN):
            args: q.Arguments = self._def_params()
        self._expect(Tag.R_PAREN)
        returns: q.Expr = q.Constant()
        if not self._check(Tag.NEWLINE):
            returns: q.Expr = self._type()
        body: list[q.Stmt] = self._suite()
        return q.FunctionDefinition(name, args, body, returns)

    ##############################
    # STATEMENT PARTS
    ##############################

    def _call_params(self) -> tuple[list[q.Expr], list[q.Keyword]]:
        lst: list[q.Expr] = [self._call_parameter()]
        while self._match(Tag.COMMA) and not self._check(Tag.R_PAREN):
            lst.append(self._call_parameter())
        self._match(Tag.COMMA)
        args: list[q.Expr] = [
            arg for arg in lst if not isinstance(arg, q.Keyword)
        ]
        keywords: list[q.Keyword] = [
            arg for arg in lst if isinstance(arg, q.Keyword)
        ]
        return (args, keywords)

    def _call_parameter(self) -> q.Expr:
        if self._check(Tag.IDENT) and self._check(Tag.EQUAL, ahead=1):
            return q.Keyword(self._next(2).tok, self._expr())
        return self._expr()

    def _def_params(self) -> q.Arguments:
        lst: list[q.Arg] = [self._def_parameter()]
        defaults: list[q.Expr] = []
        while self._match(Tag.COMMA) and not self._check(Tag.R_PAREN):
            lst.append(self._def_parameter())
            if self._match(Tag.EQUAL):
                default_params: tuple[
                    list[q.Arg],
                    list[q.Expr],
                ] = self._def_default_params(lst[-1])
                lst.extend(default_params[0])
                defaults: list[q.Expr] = default_params[1]
                break
        self._match(Tag.COMMA)
        return q.Arguments(args=lst, defaults=defaults)

    def _def_default_params(
        self,
        first_arg: q.Arg,
    ) -> tuple[list[q.Arg], list[q.Expr]]:
        args: list[q.Arg] = [first_arg]
        defaults: list[q.Expr] = [self._expr()]
        while self._match(Tag.COMMA) and not self._check(Tag.R_PAREN):
            args.append(self._def_parameter())
            self._expect(Tag.EQUAL)
            defaults.append(self._expr())
        self._match(Tag.COMMA)
        return (args, defaults)

    def _def_parameter(self) -> q.Arg:
        arg: str = self._expect(Tag.IDENT).tok
        annotation: q.Expr | None = None
        if self._match(Tag.COLON):
            annotation: q.Expr = self._type()
        return q.Arg(arg, annotation)

    def _type(self) -> q.Expr:
        typ: q.Expr = self._postfix()
        while self._match(Tag.PIPE):
            typ: q.BinaryOp = q.BinaryOp(Tag.PIPE, typ, self._postfix())
        return typ

    ##############################
    # BLOCKS
    ##############################

    def _suite(self) -> list[q.Stmt]:
        self._expect(Tag.NEWLINE)
        self._expect(Tag.INDENT)
        stmts: list[q.Stmt] = [self._stmt()]
        while not self._check(Tag.DEDENT):
            stmts.append(self._stmt())
        self._expect(Tag.DEDENT)
        return stmts

    ##############################
    # EXPRESSIONS
    ##############################

    def _expr(self) -> q.Expr:
        expr: q.Expr = self._ternary()
        if not self._check(Tag.ARROW):
            return expr
        return self._pipeline(expr)

    def _pipeline(self, first: q.Expr) -> q.Expr:
        stage: q.Expr = first
        while self._match(Tag.ARROW):
            args: list[q.Expr] = []
            if self._match(Tag.PERIOD):
                stage = q.Attribute(stage, self._expect(Tag.IDENT).tok)
                pf: q.Expr = self._postfix(stage)
            else:
                args.append(stage)
                pf: q.Expr = self._postfix()
            kws: list[q.Keyword] = []
            if isinstance(pf, q.Call):
                args.extend(arg for arg in pf.args)
                kws: list[q.Keyword] = pf.keywords
            stage = q.Call(
                pf.func if isinstance(pf, q.Call) else pf,
                args=args,
                keywords=kws,
            )
        return stage

    def _ternary(self) -> q.Expr:
        body: q.Expr = self._disjunction()
        if not self._check(Tag.L_ANGLE_MINUS_R_ANGLE):
            return body
        self._expect(Tag.L_ANGLE_MINUS_R_ANGLE)
        orelse: q.Expr = self._expr()
        self._expect("if")
        test: q.Expr = self._expr()
        return q.TernaryOp(body, test, orelse)

    def _disjunction(self) -> q.Expr:
        expr: q.Expr = self._conjunction()
        if not self._check(Tag.OR):
            return expr
        self._expect(Tag.OR)
        values: list[q.Expr] = [expr, self._conjunction()]
        while self._match(Tag.OR):
            values.append(self._conjunction())
        return q.BoolOp(Tag.OR, values)

    def _conjunction(self) -> q.Expr:
        expr: q.Expr = self._inversion()
        if not self._check(Tag.AND):
            return expr
        self._expect(Tag.AND)
        values: list[q.Expr] = [expr, self._inversion()]
        while self._match(Tag.AND):
            values.append(self._inversion())
        return q.BoolOp(Tag.AND, values)

    def _inversion(self) -> q.Expr:
        if not self._check(Tag.NOT):
            return self._comparison()
        return q.UnaryOp(self._next().tag, self._inversion())

    def _comparison(self) -> q.Expr:
        expr: q.Expr = self._bitwise_or()
        if not self._in(COMPARISON_OPS):
            return expr
        ops: list[Tag] = [self._next().tag]
        comparators: list[q.Expr] = [self._bitwise_or()]
        while self._in(COMPARISON_OPS):
            ops.append(self._next().tag)
            comparators.append(self._bitwise_or())
        return q.Comparison(expr, ops, comparators)

    def _bitwise_or(self) -> q.Expr:
        expr: q.Expr = self._bitwise_xor()
        while self._check(Tag.PIPE):
            expr = q.BinaryOp(self._next().tag, expr, self._bitwise_xor())
        return expr

    def _bitwise_xor(self) -> q.Expr:
        expr: q.Expr = self._bitwise_and()
        while self._check(Tag.TILDE):
            expr = q.BinaryOp(self._next().tag, expr, self._bitwise_and())
        return expr

    def _bitwise_and(self) -> q.Expr:
        expr: q.Expr = self._bitwise_shift()
        while self._check(Tag.AMPERSAND):
            expr = q.BinaryOp(self._next().tag, expr, self._bitwise_shift())
        return expr

    def _bitwise_shift(self) -> q.Expr:
        expr: q.Expr = self._sum()
        while self._check(Tag.L_ANGLE_L_ANGLE, Tag.R_ANGLE_R_ANGLE):
            expr = q.BinaryOp(self._next().tag, expr, self._sum())
        return expr

    def _sum(self) -> q.Expr:
        expr: q.Expr = self._term()
        while self._check(Tag.PLUS, Tag.MINUS):
            expr = q.BinaryOp(self._next().tag, expr, self._term())
        return expr

    def _term(self) -> q.Expr:
        expr: q.Expr = self._factor()
        while self._check(
            Tag.ASTERISK,
            Tag.SLASH,
            Tag.SLASH_SLASH,
            Tag.PERCENT,
        ):
            expr = q.BinaryOp(self._next().tag, expr, self._factor())
        return expr

    def _factor(self) -> q.Expr:
        if not self._check(Tag.PLUS, Tag.MINUS, Tag.TILDE):
            return self._power()
        return q.UnaryOp(self._next().tag, self._factor())

    def _power(self) -> q.Expr:
        expr: q.Expr = self._postfix()
        while self._check(Tag.CARET):
            expr = q.BinaryOp(self._next().tag, expr, self._factor())
        return expr

    def _postfix(self, first: q.Expr | None = None) -> q.Expr:
        expr: q.Expr = first or self._primary()
        while self._check(Tag.PERIOD, Tag.L_PAREN, Tag.L_BRACKET):
            if self._match(Tag.PERIOD):
                expr = q.Attribute(expr, self._expect(Tag.IDENT).tok)
            elif self._match(Tag.L_PAREN):
                if self._match(Tag.R_PAREN):
                    expr = q.Call(expr)
                else:
                    expr = q.Call(expr, *self._call_params())
                    self._expect(Tag.R_PAREN)
            elif self._match(Tag.L_BRACKET):
                expr = q.Subscript(expr, self._slice())
                self._expect(Tag.R_BRACKET)
        return expr

    def _slice(self) -> q.Expr:
        lower: q.Expr | None = None
        upper: q.Expr | None = None
        step: q.Expr | None = None
        if not self._check(Tag.COLON):
            lower: q.Expr = self._expr()
            expr: q.Expr = lower
        if not self._check(Tag.COLON):
            return expr
        self._expect(Tag.COLON)
        if not self._check(Tag.COMMA, Tag.COLON, Tag.R_BRACKET):
            upper: q.Expr = self._expr()
        if self._match(Tag.COLON):  # noqa: SIM102
            if not (self._check(Tag.COMMA, Tag.R_BRACKET)):
                step: q.Expr = self._expr()
        return q.Slice(lower, upper, step)

    def _primary(self) -> q.Expr:  # noqa: PLR0911
        if self._token.tag in self._primary_dict:
            return self._primary_dict[self._token.tag]()
        if self._check(Tag.IDENT):
            return q.Ident(self._next().tok)
        if self._match(Tag.L_PAREN):
            return self._tuple()
        if self._match(Tag.L_BRACKET):
            return self._list()
        if self._match(Tag.DOLLAR_L_BRACE):
            return self._set()
        if self._match(Tag.PERCENT_L_BRACE):
            return self._dict()
        return self._raise_error(
            f"UnknownPrimary: {self._token.tag} {self._token.tok}",
        )

    def _integer(self) -> q.Constant:
        return q.Constant(int(self._next().tok))

    def _float(self) -> q.Constant:
        return q.Constant(float(self._next().tok))

    def _string(self) -> q.Constant:
        return q.Constant(self._next().tok)

    def _true(self) -> q.Constant:
        self._next()
        return q.Constant(value=True)

    def _false(self) -> q.Constant:
        self._next()
        return q.Constant(value=False)

    def _none(self) -> q.Constant:
        self._next()
        return q.Constant()

    def _ellipsis(self) -> q.Constant:
        self._next()
        return q.Constant(Ellipsis)

    def _list(self) -> q.List:
        if self._match(Tag.R_BRACKET):
            return q.List()
        lst: list[q.Expr] = [self._expr()]
        while self._match(Tag.COMMA) and not self._check(Tag.R_BRACKET):
            lst.append(self._expr())
        self._match(Tag.COMMA)
        self._expect(Tag.R_BRACKET)
        return q.List(lst)

    def _tuple(self) -> q.Expr:
        if self._match(Tag.R_PAREN):
            return q.Tuple()
        expr: q.Expr = self._expr()
        if self._match(Tag.R_PAREN):
            return expr
        lst: list[q.Expr] = [expr]
        while self._match(Tag.COMMA) and not self._check(Tag.R_PAREN):
            lst.append(self._expr())
        self._match(Tag.COMMA)
        self._expect(Tag.R_PAREN)
        return q.Tuple(lst)

    def _set(self) -> q.Set:
        if self._match(Tag.R_BRACE):
            return q.Set()
        lst: list[q.Expr] = [self._expr()]
        while self._match(Tag.COMMA) and not self._check(Tag.R_BRACE):
            lst.append(self._expr())
        self._match(Tag.COMMA)
        self._expect(Tag.R_BRACE)
        return q.Set(lst)

    def _dict(self) -> q.Dict:
        if self._match(Tag.R_BRACE):
            return q.Dict()
        lst: list[tuple[q.Expr, q.Expr]] = []
        key: q.Expr = self._expr()
        self._expect(Tag.COLON)
        lst.append((key, self._expr()))
        while self._match(Tag.COMMA) and not self._check(Tag.R_BRACE):
            key: q.Expr = self._expr()
            self._expect(Tag.COLON)
            lst.append((key, self._expr()))
        self._match(Tag.COMMA)
        self._expect(Tag.R_BRACE)
        return q.Dict([pair[0] for pair in lst], [pair[1] for pair in lst])
