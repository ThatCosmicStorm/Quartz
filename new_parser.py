"""*The Quartz Parser*."""

##############################
# IMPORTS
##############################

from collections.abc import Callable
from io import StringIO
from typing import NoReturn

from nodes import BinaryOp, Node
from tokendef import Error, Tag, Token

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

COMPARISON_OPS: set[str | Tag] = {
    "in",
    "is",
    "not",
    Tag.BANG_EQUAL,
    Tag.EQUAL_EQUAL,
    Tag.L_ANGLE,
    Tag.L_ANGLE_EQUAL,
    Tag.R_ANGLE,
    Tag.R_ANGLE_EQUAL,
}

COMPOUND_WORDS: set[str] = {
    "class",
    "define",
    "for",
    "if",
    "until",
    "while",
    "wrap",
}

##############################
# ERROR DEFINITION
##############################


class _ParserError(Error):
    pass


##############################
# TYPE ALIASES
##############################

type StmtHandler = Callable[[], Node]

type Expr = Node | BinaryOp

type ExprHandler = Callable[[], Expr]

type Logic = list[Expr] | list[dict[str, Expr]]

##############################
# PARSER CLASS
##############################


class Parser:
    """*The Quartz Parser class*."""

    def __init__(self, tokens: list[Token]) -> None:
        """*Initialize a ready-to-use parser*.

        Args:
            tokens (list[Token]): *Lexer output*

        """
        self._tokens: list[Token] = tokens

        self._index: int = 0
        # Official alias
        self._i: int = self._index

        self._token: Token = self._tokens[self._i]

        self._length: int = len(self._tokens)

        self._KEYWORD_STMTS: dict[str, StmtHandler] = {
            "<<<": self._return_,
            "alias": self._alias,
            "assert": self._assert,
            "class": self._class,
            "fn": self._function_definition,
            "for": self._for,
            "from": self._selective_import,
            "if": self._if,
            "import": self._basic_import,
            "pub": self._public,
            "return": self._return_,
            "until": self._while,
            "while": self._while,
            "wrap": self._wrap,
        }

        self._KEYWORD_EXPRS: dict[Tag, ExprHandler] = {
            Tag.FLOAT: self._float,
            Tag.INTEGER: self._integer,
            Tag.STRING: self._string,
            Tag.IDENT: self._ident,
            Tag.L_PAREN: self._parens,
            Tag.L_BRACKET: self._list,
            Tag.DOLLAR_L_BRACE: self._set,
            Tag.PERCENT_L_BRACE: self._dict,
        }

    ##########################
    # Helper Functions
    ##########################

    def _raise_error(self, message: str) -> NoReturn:
        raise _ParserError(
            self._token.ln,
            self._token.col,
            self._token.line,
            message,
        )

    def _next(self, num: int = 1) -> Token:
        """*Increment index by `num`*.

        Args:
            num (int, optional): *Increment value*. \
            Defaults to 1.

        Returns:
            Token: *Token at old index value*.

        """
        if self._i + num >= self._length:
            self._raise_error(
                f"""No token found at index #{self._i + num}""",
            )

        past_token: Token = self._token
        self._i += num
        self._token = self._tokens[self._i]
        return past_token

    def _check(self, type_: str | Tag) -> bool:
        """*Compare `type_` to current token*.

        Regardless of match, do not call `_next()`.
        """
        return type_ in {
            self._token.tag,
            self._token.tok,
        }

    def _in(
        self,
        set_: set[Tag] | set[str] | set[str | Tag],
    ) -> bool:
        return self._token.tag in set_ or self._token.tok in set_

    def _match(self, type_: str | Tag) -> Token | None:
        """*Compare `type_` to current token*.

        Call `_next()` if it matches.
        """
        if type_ in {
            self._token.tag,
            self._token.tok,
        }:
            return self._next()
        return None

    def _expect(self, type_: str | Tag) -> Token:
        """*Expect `type_` to match current token*.

        Call `_next()` if it matches.
        Raise `_ParserError` if no match.
        """
        if type_ in {
            self._token.tok,
            self._token.tag,
        }:
            return self._next()

        return self._raise_error(
            f"""Expected {type_}, got {self._token.tok or self._token.tag}.""",
        )

    def _check_ahead(self, value: str | Tag, num: int = 1) -> bool:
        i: int = self._i + num
        ahead: bool = i < self._length
        in_: bool = value in {
            self._tokens[i].tag,
            self._tokens[i].tok,
        }
        return ahead and in_

    def _in_ahead(
        self,
        set_: set[Tag] | set[str] | set[str | Tag],
        num: int = 1,
    ) -> bool:
        i: int = self._i + num
        ahead: bool = i < self._length
        tag: bool = self._tokens[i].tag in set_
        tok: bool = self._tokens[i].tok in set_
        return ahead and (tag or tok)

    ##########################
    # Public Function
    ##########################

    def parse(self) -> Node:
        """*Parse a list of Quartz tokens*.

        Returns:
            Node: *Every statement and expression*

        """
        statements: list[Node] = []
        while not self._check(Tag.EOF):
            statements.append(
                self._statement(),
            )

        return Node(
            "program",
            statements,
        )

    ##########################
    # Statements
    ##########################

    ##########################
    # Compound Cases
    ##########################

    def _for(self) -> Node:
        return Node(
            self._expect("for").tok,
            {"range": self._range(), "suite": self._suite()},
        )

    def _function_definition(self) -> Node:
        pub: bool = bool(self._match("pub"))
        self._expect("fn")
        name: str = self._expect(Tag.IDENT).tok
        self._expect(Tag.L_PAREN)
        if not self._check(Tag.R_PAREN):
            params: Node = self._def_params()
        self._expect(Tag.R_PAREN)
        if self._match(Tag.TILDE_ARROW):
            return_: Node = self._def_return()
        return Node(
            "function_definition",
            {
                "pub": pub,
                "name": name,
                "params": params,
                "return_": return_,
                "suite": self._suite(),
            },
        )

    def _if(self) -> Node:
        self._expect("if")
        condition: Expr = self._expr()
        suite: Node = self._suite()
        if not self._check("else"):
            return Node(
                "if",
                {"condition": condition, "suite": suite},
            )
        else_ifs: list[Node] = []
        else_: Node | None = None
        while self._match("else"):
            if self._match("if"):
                else_ifs.append(self._else_if())
            else:
                else_ = self._else()
        return Node(
            "if",
            {
                "condition": condition,
                "suite": suite,
                "else_if": else_ifs,
                "else": else_,
            },
        )

    def _else_if(self) -> Node:
        return Node(
            "else_if",
            {"condition": self._expr(), "suite": self._suite()},
        )

    def _else(self) -> Node:
        return Node(
            "else",
            self._suite(),
        )

    def _match_(self) -> Node:
        return Node(
            self._expect("match").tok,
            {"target": self._expr(), "suite": self._match_suite()},
        )

    def _main(self) -> Node:
        return Node(
            self._expect("main").tok,
            self._suite(),
        )

    def _while(self) -> Node:
        if self._match("while"):
            until: bool = False
        elif self._match("until"):
            until: bool = True
        return Node(
            "while",
            {
                "until": until,
                "condition": self._expr(),
                "suite": self._suite(),
            },
        )

    def _wrap(self) -> Node:
        self._expect("wrap")
        targets: list[Node] = [self._target()]
        while self._match(Tag.COMMA):
            if self._check(Tag.NEWLINE):
                break
            targets.append(self._target())
        return Node(
            "wrap",
            {"targets": targets, "suite": self._wrap_suite()},
        )

    ##########################
    # Statement Parts
    ##########################

    def _call_parameter(self) -> Node:
        if self._check(Tag.IDENT) and self._check_ahead(Tag.EQUAL):
            return Node(
                "call_parameter",
                {"name": self._next(2).tok, "value": self._expr()},
            )
        return Node(
            "call_parameter",
            {"name": None, "value": self._expr()},
        )

    def _call_params(self) -> Node:
        return Node(
            "call_params",
            self._listed(self._call_parameter),
        )

    def _def_parameter(self) -> Node:
        name: str = self._expect(Tag.IDENT).tok
        annotation: Node | None = None
        if self._match(Tag.COLON):
            annotation = self._type()
        default: Expr | None = None
        if self._match(Tag.EQUAL):
            default = self._expr()
        return Node(
            "def_parameter",
            {"name": name, "annotation": annotation, "default": default},
        )

    def _def_params(self) -> Node:
        params: list[Node] = [self._def_parameter()]
        while self._match(Tag.COMMA):
            if self._check(Tag.R_PAREN):
                break
            params.append(self._def_parameter())
        return Node(
            "def_params",
            self._listed(self._def_parameter),
        )

    def _def_return(self) -> Node:
        self._expect(Tag.TILDE_ARROW)
        typ: Node = self._type()
        default: Expr | None = None
        if self._match(Tag.L_BRACE):
            default = self._expr()
            self._expect(Tag.R_BRACE)
        return Node(
            "def_return",
            {"type": typ, "default": default},
        )

    def _import_parameter(self) -> Node:
        name: str = self._next().tok
        if self._match("as"):
            alias: str = self._next().tok
        return Node(
            "import_parameter",
            {"name": name, "alias": alias},
        )

    def _import_params(self) -> Node:
        lst: list[Node] = [self._import_parameter()]
        while self._match(Tag.COMMA):
            lst.append(self._import_parameter())
        return Node(
            "import_params",
            lst,
        )

    def _pipe_assign(self) -> Node:
        self._expect(Tag.ARROW_EQUAL)
        stages: list[Node] = [self._pipe_stage()]
        while self._match(Tag.ARROW):
            stages.append(self._pipe_stage())
        return Node(
            "pipe_assign",
            stages,
        )

    def _pipe_attribute(self) -> Node:
        self_: bool = False
        if self._match(Tag.PERIOD):
            self_ = True
        object_: list[str] = []
        while self._check(Tag.IDENT) and self._check_ahead(Tag.PERIOD):
            object_.append(self._next(2).tok)
        object_.append(self._expect(Tag.IDENT).tok)
        return Node(
            "pipe_attribute",
            {"self": self_, "object": object_},
        )

    def _pipe_stage(self) -> Node:
        name: Node = self._pipe_attribute()
        if self._match(Tag.L_PAREN):
            if not self._check(Tag.R_PAREN):
                params: Node = self._call_params()
            return Node(
                "pipe_stage",
                {"name": name, "params": params},
            )
        if not self._match(Tag.COLON):
            return Node(
                "pipe_stage",
                {"name": name, "params": None},
            )
        params: list[Expr] = [self._expr()]
        while self._match(Tag.COMMA):
            params.append(self._expr())
        return Node(
            "pipe_stage",
            {"name": name, "params": params},
        )

    def _stmt_end(self, func: Expr) -> Expr:
        if self._match(Tag.NEWLINE):
            return func
        return self._raise_error(
            """\
            More than one statement on the same line.

            Possible solutions:
              - Put statements on separate lines.
              - Separate statements with a semicolon.""",
        )

    def _target(self) -> Node:
        name: str = self._expect(Tag.IDENT).tok
        if not self._check(Tag.L_PAREN):
            return Node(
                "target",
                {"name": name, "parameters": None},
            )
        self._expect(Tag.L_PAREN)
        parameters: Node = self._call_params()
        self._expect(Tag.R_PAREN)
        return Node(
            "target",
            {"name": name, "parameters": parameters},
        )

    ##########################
    # Blocks
    ##########################

    def _template_suite(self, logic: Callable[[], Logic]) -> Logic:
        self._expect(Tag.NEWLINE)
        self._expect(Tag.INDENT)
        lst: Logic = logic()
        self._expect(Tag.DEDENT)
        return lst

    def _suite(self) -> Node:
        return Node(
            "suite",
            self._template_suite(self._suite_logic),
        )

    def _match_suite(self) -> Node:
        return Node(
            "match_suite",
            self._template_suite(self._match_logic),
        )

    def _suite_logic(self) -> list[Expr]:
        stmts: list[Expr] = []
        while not self._check(Tag.DEDENT):
            stmts.append(self._statement())
        if not stmts:
            self._raise_error(
                """No statements within an indented block.""",
            )
        return stmts

    def _match_logic(self) -> list[dict[str, Expr]]:
        cases: list[dict[str, Expr]] = []
        self._expect("case")
        cases.append(
            {"case": self._expr(), "suite": self._suite()},
        )
        while self._match("case"):
            cases.append(
                {"case": self._expr(), "suite": self._suite()},
            )
        return cases

    ##########################
    # Expressions
    ##########################

    def _expr(self) -> Expr:
        expr: Expr = self._ternary()
        if not self._check(Tag.ARROW):
            return expr
        data: list[Expr] = []
        while self._match(Tag.ARROW):
            data.append(self._pipe_stage())
        return Node(
            "pipeline",
            data,
        )

    def _ternary(self) -> Expr:
        expr: Expr = self._disjunction()
        if not self._match(Tag.EROTEME_EROTEME):
            return expr
        if_: Expr = self._expr()
        self._expect(Tag.BANG_BANG)
        return Node(
            "ternary",
            {"condition": expr, "if": if_, "else": self._expr()},
        )

    def _disjunction(self) -> Expr:
        expr: Expr = self._conjunction()
        if not self._match("or"):
            return expr
        expr: BinaryOp = BinaryOp(
            "or",
            expr,
            self._conjunction(),
        )
        while self._match("or"):
            expr = BinaryOp(
                "or",
                expr,
                self._conjunction(),
            )
        return expr

    def _conjunction(self) -> Expr:
        expr: Expr = self._inversion()
        if not self._match("and"):
            return expr
        expr: BinaryOp = BinaryOp(
            "and",
            expr,
            self._inversion(),
        )
        while self._match("and"):
            expr = BinaryOp(
                "and",
                expr,
                self._inversion(),
            )
        return expr

    def _inversion(self) -> Expr:
        if self._match("not"):
            return BinaryOp(
                "not",
                None,
                self._inversion(),
            )
        return self._comparison()

    def _range(self) -> Node:
        first: Expr = self._expr()
        second: Expr | None = None
        if self._match("in"):
            second: Expr = self._expr()

    def _range1(self) -> Node:
        start: Expr = self._expr()
        if not (
            self._check(Tag.PERIOD_PERIOD)
            or self._check(Tag.PERIOD_PERIOD_EQUAL)
        ):
            return Node(
                "range",
                {"start": start, "inclusive": None, "stop": None},
            )
        if self._match(Tag.PERIOD_PERIOD):
            inclusive: bool = False
        elif self._match(Tag.PERIOD_PERIOD_EQUAL):
            inclusive: bool = True
        return Node(
            "range",
            {"start": start, "inclusive": inclusive, "stop": self._expr()},
        )

    def _comparison(self) -> Expr:
        expr: Expr = self._bitwise_or()
        if not self._in(COMPARISON_OPS):
            return expr
        expr: BinaryOp = BinaryOp(
            self._comparison_special_cases(),
            expr,
            self._bitwise_or(),
        )
        while self._in(COMPARISON_OPS):
            expr = BinaryOp(
                self._comparison_special_cases(),
                expr,
                self._bitwise_or(),
            )
        return expr

    def _comparison_special_cases(self) -> Tag | str:
        if self._check("is") and self._check_ahead("not"):
            self._next(2)
            return "is not"
        if self._check("not") and self._check_ahead("in"):
            self._next(2)
            return "not in"
        if self._token.tag in COMPARISON_OPS:
            return self._next().tag
        if self._token.tok in COMPARISON_OPS:
            return self._next().tok
        return self._raise_error(
            """Unknown comparison operator.""",
        )

    def _bitwise_or(self) -> Expr:
        expr: Expr = self._bitwise_xor()
        if not self._match(Tag.PIPE):
            return expr
        expr: BinaryOp = BinaryOp(
            Tag.PIPE,
            expr,
            self._bitwise_xor(),
        )
        while self._match(Tag.PIPE):
            expr = BinaryOp(
                Tag.PIPE,
                expr,
                self._bitwise_xor(),
            )
        return expr

    def _bitwise_xor(self) -> Expr:
        expr: Expr = self._bitwise_and()
        if not self._match(Tag.TILDE):
            return expr
        expr: BinaryOp = BinaryOp(
            Tag.TILDE,
            expr,
            self._bitwise_and(),
        )
        while self._match(Tag.TILDE):
            expr = BinaryOp(
                Tag.TILDE,
                expr,
                self._bitwise_and(),
            )
        return expr

    def _bitwise_and(self) -> Expr:
        expr: Expr = self._bitwise_shift()
        if not self._match(Tag.AMPERSAND):
            return expr
        expr: BinaryOp = BinaryOp(
            Tag.AMPERSAND,
            expr,
            self._bitwise_shift(),
        )
        while self._match(Tag.AMPERSAND):
            expr = BinaryOp(
                Tag.AMPERSAND,
                expr,
                self._bitwise_shift(),
            )
        return expr

    def _bitwise_shift(self) -> Expr:
        expr: Expr = self._sum_()
        if not (
            self._check(Tag.L_ANGLE_L_ANGLE)
            or self._check(Tag.R_ANGLE_R_ANGLE)
        ):
            return expr
        expr: BinaryOp = BinaryOp(
            self._next().tag,
            expr,
            self._bitwise_shift(),
        )
        while self._check(Tag.L_ANGLE_L_ANGLE) or self._check(
            Tag.R_ANGLE_R_ANGLE,
        ):
            expr = BinaryOp(
                self._next().tag,
                expr,
                self._bitwise_shift(),
            )
        return expr

    def _sum_(self) -> Expr:
        expr: Expr = self._term()
        if not (self._check(Tag.PLUS) or self._check(Tag.MINUS)):
            return expr
        expr: BinaryOp = BinaryOp(
            self._next().tag,
            expr,
            self._term(),
        )
        while self._check(Tag.PLUS) or self._check(Tag.MINUS):
            expr = BinaryOp(
                self._next().tag,
                expr,
                self._term(),
            )
        return expr

    def _term(self) -> Expr:
        expr: Expr = self._factor()
        if not (
            self._check(Tag.SLASH_SLASH)
            or self._check(Tag.ASTERISK)
            or self._check(Tag.PERCENT)
            or self._check(Tag.SLASH)
        ):
            return expr
        expr: BinaryOp = BinaryOp(
            self._next().tag,
            expr,
            self._factor(),
        )
        while (
            self._check(Tag.SLASH_SLASH)
            or self._check(Tag.ASTERISK)
            or self._check(Tag.PERCENT)
            or self._check(Tag.SLASH)
        ):
            expr = BinaryOp(
                self._next().tag,
                expr,
                self._factor(),
            )
        return expr

    def _factor(self) -> Expr:
        if not (
            self._check(Tag.PLUS)
            or self._check(Tag.MINUS)
            or self._check(Tag.TILDE)
        ):
            return self._power()
        return BinaryOp(self._next().tag, None, self._factor())

    def _power(self) -> Expr:
        expr: Expr = self._postfix()
        if not self._match(Tag.CARET):
            return expr
        expr: BinaryOp = BinaryOp(
            Tag.CARET,
            expr,
            self._factor(),
        )
        while self._match(Tag.CARET):
            expr = BinaryOp(
                Tag.CARET,
                expr,
                self._factor(),
            )
        return expr

    def _postfix(self) -> Expr:
        expr: Expr = self._primary()
        if not (
            self._check(Tag.PERIOD)
            or self._check(Tag.L_PAREN)
            or self._check(Tag.L_BRACKET)
        ):
            return expr
        ops: list[Expr] = [self._postfix_op()]
        while (
            self._check(Tag.PERIOD)
            or self._check(Tag.L_PAREN)
            or self._check(Tag.L_BRACKET)
        ):
            ops.append(self._postfix_op())
        return Node(
            "postfix",
            ops,
        )

    def _postfix_op(self) -> Node:
        if self._match(Tag.PERIOD):
            return Node(
                "attribute_access",
                self._expect(Tag.IDENT).tok,
            )
        if self._match(Tag.L_PAREN):
            return Node("function_call", self._call_params())
        if self._match(Tag.L_BRACKET):
            return Node("indexing_slicing", self._subscript_list())
        return self._raise_error(
            """\
                Unknown postfix operation.
                Postfix operations:
                  - Attribute access `x.y`
                  - Function call `x(y)`
                  - Indexing and slicing `x[y]`""",
        )

    def _subscript_list(self) -> Node:
        lst: list[Expr] = [self._subscript()]
        while self._match(Tag.COMMA):
            if self._check(Tag.R_BRACKET):
                break
            lst.append(self._subscript())
        return Node(
            "subscript_list",
            lst,
        )

    def _subscript(self) -> Expr:
        if self._check(Tag.COLON):
            return self._slice()
        expr: Expr = self._disjunction()
        if self._check(Tag.COLON):
            return self._slice(expr=expr)
        return expr

    def _slice(self, expr: Expr | None = None) -> Node:
        start: Expr | None = expr if expr is not None else None
        self._expect(Tag.COLON)
        stop: Expr | None = None
        if not (self._check(Tag.COMMA) or self._check(Tag.L_BRACKET)):
            stop = self._expr()
        step: Expr | None = None
        if self._check(Tag.COLON) and not (
            self._check_ahead(Tag.COMMA) or self._check_ahead(Tag.L_BRACKET)
        ):
            self._expect(Tag.COLON)
            step = self._expr()
        return Node(
            "slice",
            {"start": start, "stop": stop, "step": step},
        )

    def _primary(self) -> Expr:
        if self._token.tag in self._KEYWORD_EXPRS:
            func: ExprHandler | None = self._KEYWORD_EXPRS.get(
                self._token.tag,
            )
            if func is not None:
                return func()
        if self._in({"True", "False"}):
            return self._boolean()
        return self._raise_error(
            """Encountered an unknown primary value.""",
        )

    ##########################
    # Other Tokens
    ##########################

    def _integer(self) -> Node:
        return Node(
            "INTEGER",
            int(self._next().tok),
        )

    def _float(self) -> Node:
        return Node(
            "FLOAT",
            float(self._next().tok),
        )

    def _string(self) -> Node:
        return Node(
            "STRING",
            self._next().tok,
        )

    def _ident(self) -> Node:
        return Node(
            "IDENT",
            self._next().tok,
        )

    def _boolean(self) -> Node:
        if self._check("True"):
            data: bool = True
        elif self._check("False"):
            data: bool = False
        self._next()
        return Node(
            "BOOLEAN",
            data,
        )

    def _parens(self) -> Expr:
        self._expect(Tag.L_PAREN)
        if self._match(Tag.R_PAREN):
            return Node(
                "TUPLE",
                (),
            )
        expr: Expr = self._expr()
        if self._match(Tag.R_PAREN):
            return expr
        lst: list[Expr] = [expr]
        while self._match(Tag.COMMA):
            if self._check(Tag.R_PAREN):
                break
            lst.append(self._expr())
        return Node(
            "TUPLE",
            tuple(lst),
        )

    def _list(self) -> Node:
        self._expect(Tag.L_BRACKET)
        lst: list[Expr] = []
        if not self._check(Tag.R_BRACKET):
            lst.append(self._expr())
        while self._match(Tag.COMMA):
            if self._check(Tag.R_BRACE):
                break
            lst.append(self._expr())
        self._expect(Tag.R_BRACKET)
        return Node(
            "LIST",
            lst,
        )

    def _set(self) -> Node:
        self._expect(Tag.DOLLAR_L_BRACE)
        set_: set[Expr] = set()
        if not self._check(Tag.R_BRACE):
            set_.add(self._expr())
        while self._match(Tag.COMMA):
            if self._check(Tag.R_BRACE):
                break
            set_.add(self._expr())
        self._expect(Tag.R_BRACE)
        return Node(
            "SET",
            set_,
        )

    def _dict(self) -> Node:
        self._expect(Tag.PERCENT_L_BRACE)
        dict_: dict[Expr, Expr] = {}
        if not self._check(Tag.R_BRACE):
            dict_[self._expr()] = self._expr()
        while self._match(Tag.COMMA):
            if self._check(Tag.R_BRACE):
                break
            dict_[self._expr()] = self._expr()
        self._expect(Tag.R_BRACE)
        return Node(
            "DICT",
            dict_,
        )

    def _type(self) -> Node:
        return Node(
            "TYPE",
            self._node_type().getvalue(),
        )

    def _node_type(self) -> StringIO:
        inner: StringIO = self._inner_type()
        while self._check(Tag.PIPE):
            inner.write(self._next().tok)
            inner.write(self._inner_type().getvalue())
        return inner

    def _inner_type(self) -> StringIO:
        main: StringIO = StringIO(
            self._expect(Tag.IDENT).tok,
        )
        if not self._check(Tag.L_BRACKET):
            return main
        if self._match(Tag.R_BRACKET):
            main.write("]")
            return main
        main.write(self._next().tok)
        main.write(self._more_type().getvalue())
        main.write(self._expect(Tag.R_BRACKET).tok)
        return main

    def _more_type(self) -> StringIO:
        or_: StringIO = self._or_type()
        while self._match(Tag.COMMA):
            if self._check(Tag.R_BRACKET):
                break
            or_.write(self._or_type().getvalue())
        return or_

    def _or_type(self) -> StringIO:
        first: StringIO = self._node_type()
        while self._match(Tag.PIPE):
            first.write(self._node_type().getvalue())
        return first


##############################
# END OF FILE
##############################
