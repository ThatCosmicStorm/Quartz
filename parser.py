
from tokendef import Tag, Token, Error
from nodes import *

##############################
# SOME SETS
##############################

ASSIGNMENT_OPS: set[Tag] = {
    Tag.EQUAL,
    Tag.ARROW_EQUAL,
    Tag.PIPE_EQUAL,
    Tag.PERCENT_EQUAL,
    Tag.ASTERISK_EQUAL,
    Tag.PLUS_EQUAL,
    Tag.MINUS_EQUAL,
    Tag.L_ANGLE_L_ANGLE_EQUAL,
    Tag.R_ANGLE_R_ANGLE_EQUAL,
    Tag.CARET_EQUAL,
    Tag.TILDE_EQUAL,
    Tag.SLASH_EQUAL,
    Tag.AMPERSAND_EQUAL,
}

COMPARISON_OPS: set[Tag | str] = {
    Tag.L_ANGLE,
    Tag.L_ANGLE_EQUAL,
    Tag.R_ANGLE,
    Tag.R_ANGLE_EQUAL,
    Tag.EQUAL_EQUAL,
    Tag.BANG_EQUAL,
    "not", "is", "in",
}

DATA_TYPES: set[str] = {
    "str",
    "int",
    "float",
    "list",
    "hash",
    "set",
    "bool",
    "None",
}

DATA_FUNCS: set[str] = {
    "str",
    "int",
    "float",
    "list",
    "hash",
    "set",
}

COMPOUND_WORDS: set[str] = {
    "define",
    "if",
    "while",
    "until",
    "for",
}

##############################
# ERROR DEF
##############################


class ParserError(Error):
    pass


##############################
# PARSER
##############################


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens
        
        self.index: int = 0
        # Official alias
        self.i: int = self.index

        self.token: Token = self.tokens[self.i]

        self.length: int = len(self.tokens)
        # Official alias
        self.n: int = self.length

    ##########################
    # Helper Functions
    ##########################

    def next(self, num: int = 1) -> Token:
        """*Returns current token, \
        then increments index by `num`: 1 by default*.
        """
        past_token: Token = self.token
        self.i += num
        if self.i < self.n:
            self.token = self.tokens[self.i]
        else:
            self.token = None

        return past_token

    def check(self, type_: Tag | str) -> bool:
        """*Compares `type_` to current token, \
        returns `Boolean`*.
        """
        if self.token.tag == type_ \
                or self.token.tok == type_:

            return True

        return False

    def is_in(self, set_: set) -> bool:
        if self.token.tag in set_ \
                or self.token.tok in set_:

            return True

        return False

    def match(self, type_: Tag | str) -> Token | None:
        """*Compares `type_` to current token, \
        `next()` if it matches*.
        """
        if self.token.tag == type_ \
                or self.token.tok == type_:

            return self.next()

        return None

    def expect(self, type_: Tag | str) -> Token:
        """*Expects `type_` to match current token: \
        `next()` if match, raises `Error` if not*.
        """
        tok: Token = self.token
        if tok.tag == type_ \
                or tok.tok == type_:

            return self.next()

        if tok.tok:
            unexpected = tok.tok
        else:
            unexpected = tok.tag

        raise ParserError(
            tok.ln,
            tok.col,
            tok.line,
            f"""
            Expected {type_}, got {unexpected}."""
        )

    def ahead_is(
            self, value: str | Tag, num: int = 1
                ) -> bool:
        is_ahead: bool = self.i + num < self.n
        tok_ahead: Token = self.tokens[self.i + num]
        match_tag: bool = tok_ahead.tag == value
        match_tok: bool = tok_ahead.tok == value

        return is_ahead and (
            match_tag or match_tok
        )

    def ahead_is_in(
            self, set_: set, num: int = 1
                ) -> bool:
        is_ahead: bool = self.i + num < self.n
        tok_ahead: Token = self.tokens[self.i + num]
        tag_in: bool = tok_ahead.tag in set_
        tok_in: bool = tok_ahead.tok in set_

        return is_ahead and (
            tag_in or tok_in
        )

    def data_type(self) -> str:
        if not self.is_in(DATA_TYPES):

            raise ParserError(
                self.token.ln,
                self.token.col,
                self.token.line,
                """
            Unknown data type."""
            )

        type_: str = self.next().tok
        if type_ not in {"list", "hash", "set"}:

            return type_

        if self.match(Tag.L_BRACKET):
            type_ += "["
            type_ += self.data_type()
            while self.match(Tag.COMMA):
                type_ += ", "
                type_ += self.data_type()

            self.expect(Tag.R_BRACKET)

            type_ += "]"

        return type_

    def stmt_end(self, func) -> Token:
        is_newline: bool = self.token.tag == Tag.NEWLINE
        is_semi: bool = self.token.tag == Tag.SEMICOLON
        if is_newline or is_semi:
            self.next()

            return func

        raise ParserError(
            self.token.ln,
            self.token.col,
            self.token.line,
            """
        More than one statement on the same line.

        Possible solutions:
          - Put statements on separate lines.
          - Separate statements with a semicolon."""
        )

    ##########################
    # Main function (i.e., Program)
    ##########################

    def parse(self) -> Program:
        statements: list[Stmt] = []
        while not self.check(Tag.EOF):
            statements.append(
                self.statement()
            )

        return Program(
            body=statements,
        )

    ##########################
    # Statements
    ##########################

    def statement(self) -> Stmt:
        if self.is_in(COMPOUND_WORDS):

            return self.compound_stmt()

        return self.stmt_end(
            self.simple_stmt()
        )

    def compound_stmt(self) -> Stmt:
        match self.token.tok:
            case "define":

                return self.func_def()

            case "if":

                return self.if_stmt()

            case "while" | "until":

                return self.while_stmt()

            case "for":

                return self.for_stmt()

    def simple_stmt(self) -> Stmt:
        match self.token.tok:
            case "imm":

                return self.initialization()

            case "alias":

                return self.alias()

            case "construct":

                return self.construct()

            case "import":

                return self.basic_import()

            case "from":

                return self.selective_import()

            case "return":

                return self.return_()

        if self.check(Tag.IDENTIFIER):
            if self.ahead_is(Tag.COLON_EQUAL) \
                    or self.ahead_is(Tag.COLON) \
                        or self.ahead_is("as"):

                return self.initialization()

            if self.ahead_is_in(ASSIGNMENT_OPS):

                return self.assignment()

        return self.expr_pipe()

    ##########################
    # Simple Cases
    ##########################

    def initialization(self) -> Initialization:
        immutable: bool = False
        if self.match("imm"):
            immutable = True

        name: Identifier = Identifier(
            self.expect(Tag.IDENTIFIER).tok
        )

        alias: Identifier | None = None
        if self.match("as"):
            alias = Identifier(
                self.expect(Tag.IDENTIFIER).tok
            )

        type_: str | None = None
        if self.match(Tag.COLON):
            if not self.is_in(DATA_TYPES):

                raise ParserError(
                    self.token.ln,
                    self.token.col,
                    self.token.line,
                    """
                Unknown or missing type hint."""
                )

            type_ = self.data_type()

        self.expect(Tag.COLON_EQUAL)

        return Initialization(
            name=name,
            value=self.expr_pipe(),
            alias=alias,
            type_=type_,
            immutable=immutable,
        )

    def alias(self) -> Alias:
        self.expect("alias")

        alias_of: Identifier = Identifier(
            self.expect(Tag.IDENTIFIER).tok
        )

        self.expect(Tag.COLON_EQUAL)

        name: Identifier = Identifier(
            self.expect(Tag.IDENTIFIER.tok)
        )
        return Alias(
            name=name,
            alias_of=alias_of,
        )

    def construct(self) -> Construct:
        self.expect("construct")

        name: Identifier = Identifier(
            self.expect(Tag.IDENTIFIER).tok
        )

        alias: Identifier | None = None
        if self.match("as"):
            alias = Identifier(
                self.expect(Tag.IDENTIFIER).tok
            )

        return Construct(
            name=name,
            alias=alias,
        )

    def assignment(self) -> Assignment:
        target: Identifier = Identifier(
            self.expect(Tag.IDENTIFIER).tok
        )

        op: Tag = self.next().tag
        if op == Tag.ARROW_EQUAL:
            value: Expr = self.pipe_assign(target)
        else:
            value: Expr = self.expr_pipe()

        return Assignment(
            target=target,
            op=op,
            value=value,
        )

    def func_call(self) -> FuncCall:
        name: Identifier = Identifier(
            self.expect(Tag.IDENTIFIER).tok
        )

        args: list[CallParameter] = []

        self.expect(Tag.L_PAREN)

        if not self.check(Tag.R_PAREN):
            args.append(
                self.call_param()
            )
            while self.match(Tag.COMMA):
                args.append(
                    self.call_param()
                )

        self.expect(Tag.R_PAREN)

        return FuncCall(
            name=name,
            args=args
        )

    def method_call(self) -> MethodCall:
        object_: str = self.expect(Tag.IDENTIFIER).tok

        self.expect(Tag.PERIOD)

        object_ += "."
        while self.check(Tag.IDENTIFIER) \
                and self.ahead_is(Tag.PERIOD):
            object_ += self.expect(Tag.IDENTIFIER).tok

            self.expect(Tag.PERIOD)

            object_ += "."

        return MethodCall(
            object_=Identifier(object_),
            call=self.func_call(),
        )

    def pipeline(self, pre_expr=None) -> Pipeline:
        if pre_expr:
            expr: Expr = pre_expr
        else:
            expr: Expr = self.expr()
        stages: list[PipelineStage] = []

        self.expect(Tag.ARROW)

        stages.append(
            self.pipeline_stage()
        )
        while self.match(Tag.ARROW):
            stages.append(
                self.pipeline_stage()
            )

        return Pipeline(
            source=expr,
            stages=stages,
        )

    def basic_import(self) -> BasicImport:
        self.expect("import")

        module: Identifier = Identifier(
            self.expect(Tag.IDENTIFIER).tok
        )

        alias: Identifier | None = None
        if self.match("as"):
            alias = Identifier(
                self.expect(Tag.IDENTIFIER).tok
            )

        return BasicImport(
            module=module,
            alias=alias,
        )

    def selective_import(self) -> SelectiveImport:
        self.expect("from")

        origin: Identifier = Identifier(
            self.expect(Tag.IDENTIFIER).tok
        )

        self.expect("import")

        if self.match(Tag.ASTERISK):
            return SelectiveImport(
                origin=origin,
                all_=True,
                imports=None,
            )

        imports: list[list[Identifier]] = [
            self.import_param()
        ]
        while self.match(Tag.COMMA):
            imports.append(
                self.import_param()
            )

        return SelectiveImport(
            origin=origin,
            all_=False,
            imports=imports,
        )

    def return_(self) -> Return:
        self.expect("return")

        return Return(
            value=self.expr_pipe(),
        )

    ##########################
    # Complex Cases
    ##########################

    def if_stmt(self) -> IfStmt:
        self.expect("if")

        branches: list[IfBranch] = []
        condition: Expr = self.expr_pipe()
        body: list[Stmt] = self.suite()
        branches.append(
            IfBranch(
                condition=condition,
                body=body,
            )
        )
        while self.match("else"):
            if self.match("if"):
                condition = self.expr_pipe()
                body = self.suite()
                branches.append(
                    IfBranch(
                        condition=condition,
                        body=body,
                    )
                )
            else:
                else_body: list[Stmt] = self.suite()

                return IfStmt(
                    branches=branches,
                    else_body=else_body,
                )

        return IfStmt(
            branches=branches,
        )

    def while_stmt(self) -> WhileStmt:
        if self.match("until"):
            until: bool = True
        elif self.match("while"):
            until: bool = False
        condition: Expr = self.expr_pipe()
        body: list[Stmt] = self.suite()

        return WhileStmt(
            condition=condition,
            body=body,
            until=until,
        )

    def for_stmt(self) -> ForStmt:
        self.expect("for")

        if self.check(Tag.IDENTIFIER):
            var: Identifier = Identifier(
                self.next().tok
            )

            self.expect("in")

        range_: list[Identifier | Integer | Tag] \
            = self.range_()
        body: list[Stmt] = self.suite()

        return ForStmt(
            var=var,
            range_=range_,
            body=body,
        )

    def func_def(self) -> FuncDef:
        self.expect("define")

        name: Identifier = Identifier(
            self.expect(Tag.IDENTIFIER).tok
        )

        self.expect(Tag.L_PAREN)

        parameters: list[Parameter] = []
        if not self.check(Tag.R_PAREN):
            parameters.append(
                self.parameter()
            )
            while self.match(Tag.COMMA):
                parameters.append(
                    self.parameter()
                )

        self.expect(Tag.R_PAREN)

        returns: list[str] = ["None"]
        if self.match(Tag.TILDE_ARROW):
            if not self.is_in(DATA_TYPES):

                raise ParserError(
                    self.token.ln,
                    self.token.col,
                    self.token.line,
                    """
                Unknown data type."""
                )

            returns[0] = self.data_type()
            while self.match(Tag.PIPE):
                returns.append(self.data_type())
        body: list[Stmt] = self.suite()

        return FuncDef(
            name=name,
            parameters=parameters,
            body=body,
            returns=returns,
        )

    ##########################
    # Statement Fragments
    ##########################

    def pipe_assign(self, ident: Identifier) -> Pipeline:
        expr: Identifier = ident
        stages: list[PipelineStage] = [
            self.pipeline_stage()
        ]
        while self.match(Tag.ARROW):
            stages.append(
                self.pipeline_stage()
            )

        return Pipeline(
            source=expr,
            stages=stages,
        )

    def call_param(self) -> CallParameter:
        if self.check(Tag.IDENTIFIER) \
                and self.ahead_is(Tag.EQUAL):
            argument: Identifier | None = Identifier(
                self.next(2).tok
            )
        else:
            argument: Identifier | None = None

        return CallParameter(
            value=self.expr(),
            argument=argument,
        )

    def pipeline_stage(self) -> PipelineStage:
        self_: bool = False
        object_ : Identifier | None = None
        stage: FuncCall | MethodCall | None = None
        if self.check(Tag.PERIOD) \
            and self.ahead_is(Tag.IDENTIFIER) \
                and self.ahead_is(Tag.L_PAREN, 2):
            self.next()
            stage = self.func_call()
            func: Identifier = stage.name
            params: list[CallParameter] = stage.args

            return PipelineStage(
                func=func,
                params=params,
                self_=True,
                object_=object_,
            )

        # Something weird with the data types
        if self.check(Tag.IDENTIFIER) \
                and self.ahead_is(Tag.PERIOD):
            stage = self.method_call()
            func: Identifier = stage.call.name
            params: list[CallParameter] = stage.call.args
            object_ = stage.object_
        elif (self.check(Tag.IDENTIFIER)
                    or self.is_in(DATA_FUNCS)) \
                        and self.ahead_is(Tag.L_PAREN):
            stage = self.func_call()
            func: Identifier = stage.name
            params: list[CallParameter] = stage.args
        elif self.check(Tag.IDENTIFIER) \
                or self.is_in(DATA_FUNCS):
            func: Identifier = Identifier(
                self.next().tok
            )
            params: Expr | None = None
            if not self.check(Tag.ARROW) \
                    and not (self.check(Tag.NEWLINE)
                            or self.check(Tag.SEMICOLON)):
                params = self.expr()
        else:

            raise ParserError(
                self.token.ln,
                self.token.col,
                self.token.line,
                """
            Missing function/method identifier."""
            )

        return PipelineStage(
            func=func,
            params=params,
            self_=self_,
            object_=object_,
        )

    def import_param(self) -> list[Identifier]:
        import_params: list[Identifier] = [
            self.expect(Tag.IDENTIFIER).tok
        ]

        if self.match("as"):
            import_params.append(
                self.expect(Tag.IDENTIFIER).tok
            )

        return import_params

    def range_(self) -> list[Identifier | Integer | Tag]:
        if not (self.check(Tag.IDENTIFIER)
                    or self.check(Tag.INTEGER)):

            raise ParserError(
                self.token.ln,
                self.token.col,
                self.token.line,
                """
            Invalid type in range. Only use `int`."""
            )

        range_: list[Identifier | Integer | Tag] = []
        if self.check(Tag.IDENTIFIER):
            range_.append(
                Identifier(self.next().tok)
            )
        elif self.check(Tag.INTEGER):
            range_.append(
                Integer(self.next().tok)
            )

        if not (self.check(Tag.PERIOD_PERIOD_EQUAL)
                    or self.check(Tag.PERIOD_PERIOD)):

            raise ParserError(
                self.token.ln,
                self.token.col,
                self.token.line,
                """
            Invalid range operator.

            Solutions:
              - Use `..` (inclusive)
              - Use `..=` (exclusive)."""
            )

        range_.append(self.next().tag)
        if not (self.check(Tag.IDENTIFIER)
                    or self.check(Tag.INTEGER)):

            raise ParserError(
                self.token.ln,
                self.token.tok,
                self.token.line,
                """
            Invalid type in range. Only use `int`."""
            )

        if self.check(Tag.IDENTIFIER):
            range_.append(
                Identifier(self.next().tok)
            )
        elif self.check(Tag.INTEGER):
            range_.append(
                Integer(self.next().tok)
            )

        return range_

    def parameter(self) -> Parameter:
        name: Identifier = Identifier(
            self.expect(Tag.IDENTIFIER).tok
        )

        type_: str | None = None
        preset: Expr | None = None
        if self.match(Tag.COLON):
            if not self.is_in(DATA_TYPES):

                raise ParserError(
                    self.token.ln,
                    self.token.col,
                    self.token.line,
                    """
                Unknown data type."""
                )

            type_ = self.data_type()
        if self.match(Tag.EQUAL):
            preset = self.expr_pipe()

        return Parameter(
            name=name,
            type_=type_,
            preset=preset,
        )

    ##########################
    # Blocks
    ##########################

    def suite(self) -> list[Stmt]:
        self.expect(Tag.NEWLINE)
        self.expect(Tag.INDENT)
        stmts: list[Stmt] = []
        while not self.check(Tag.DEDENT):
            stmts.append(self.statement())
        self.expect(Tag.DEDENT)

        return stmts

    ##########################
    # Expressions
    ##########################

    def expr_pipe(self) -> Expr | Pipeline:
        value: Expr = self.expr()
        if self.check(Tag.ARROW):

            return self.pipeline(
                pre_expr=value,
            )

        return value

    def expr(self) -> Expr:

        return self.disjunction()

    def disjunction(self) -> Expr:
        expr: Expr = self.conjunction()
        if not self.match("or"):

            return expr

        op: str = "or"
        right: Expr = self.conjunction()
        expr = BinaryOp(expr, op, right)
        while self.match("or"):
            right = self.conjunction()
            expr = BinaryOp(expr, op, right)

        return expr

    def conjunction(self) -> Expr:
        expr: Expr = self.inversion()
        if not self.match("and"):

            return expr

        op: str = "and"
        right: Expr = self.inversion()
        expr = BinaryOp(expr, op, right)
        while self.match("and"):
            right = self.inversion()
            expr = BinaryOp(expr, op, right)

        return expr

    def inversion(self) -> Expr:
        if self.match("not"):

            return UnaryOp("not", self.inversion())

        return self.comparison()

    def comparison(self) -> Expr:
        expr: Expr = self.bitwise_or()
        if not (self.token.tag in COMPARISON_OPS
                    or self.token.tok in COMPARISON_OPS):

            return expr

        op: Tag | str = self.comparison_special_cases()
        right: Expr = self.bitwise_or()
        expr = BinaryOp(expr, op, right)
        while self.token.tag in COMPARISON_OPS \
                or self.token.tok in COMPARISON_OPS:
            op = self.comparison_special_cases()
            right = self.bitwise_or()
            expr = BinaryOp(expr, op, right)

        return expr

    def comparison_special_cases(self) -> Tag | str:
        if self.check("is") \
                and self.ahead_is("not"):
            self.next(2)

            return "is not"

        if self.check("not") \
                and self.ahead_is("in"):
            self.next(2)

            return "not in"

        if self.token.tag in COMPARISON_OPS:

            return self.next().tag

        if self.token.tok in COMPARISON_OPS:

            return self.next().tok

        raise ParserError(
            self.token.ln,
            self.token.col,
            self.token.line,
            """Unknown comparison operator."""
        )

    def bitwise_or(self) -> Expr:
        expr: Expr = self.bitwise_xor()
        if not self.match(Tag.PIPE):

            return expr

        op: Tag = Tag.PIPE
        right: Expr = self.bitwise_xor()
        expr = BinaryOp(expr, op, right)
        while self.match(Tag.PIPE):
            right = self.bitwise_xor()
            expr = BinaryOp(expr, op, right)

        return expr

    def bitwise_xor(self) -> Expr:
        expr: Expr = self.bitwise_and()
        if not self.match(Tag.TILDE):

            return expr

        op: Tag = Tag.TILDE
        right: Expr = self.bitwise_and()
        expr = BinaryOp(expr, op, right)
        while self.match(Tag.TILDE):
            right = self.bitwise_and()
            expr = BinaryOp(expr, op, right)

        return expr

    def bitwise_and(self) -> Expr:
        expr: Expr = self.bitwise_shift()
        if not self.match(Tag.AMPERSAND):

            return expr

        op: Tag = Tag.AMPERSAND
        right: Expr = self.bitwise_shift()
        expr = BinaryOp(expr, op, right)
        while self.match(Tag.AMPERSAND):
            right = self.bitwise_shift()
            expr = BinaryOp(expr, op, right)

        return expr

    def bitwise_shift(self) -> Expr:
        expr: Expr = self.sum_()
        if not (self.check(Tag.L_ANGLE_L_ANGLE)
                    or self.check(Tag.R_ANGLE_R_ANGLE)):

            return expr

        op: Tag = self.next().tag
        right: Expr = self.sum_()
        expr = BinaryOp(expr, op, right)
        while self.check(Tag.L_ANGLE_L_ANGLE) \
                or self.check(Tag.R_ANGLE_R_ANGLE):
            op = self.next().tag
            right = self.sum_()
            expr = BinaryOp(expr, op, right)

        return expr

    def sum_(self) -> Expr:
        expr: Expr = self.term()
        if not (self.check(Tag.PLUS)
                    or self.check(Tag.MINUS)):

            return expr

        op: Tag = self.next().tag
        right: Expr = self.term()
        expr = BinaryOp(expr, op, right)
        while self.check(Tag.PLUS) \
                    or self.check(Tag.MINUS):
            op = self.next().tag
            right = self.term()
            expr = BinaryOp(expr, op, right)

        return expr

    def term(self) -> Expr:
        expr: Expr = self.factor()
        if not (self.check(Tag.SLASH_SLASH)
                    or self.check(Tag.ASTERISK)
                        or self.check(Tag.PERCENT)
                            or self.check(Tag.SLASH)):

            return expr

        op: Tag = self.next().tag
        right: Expr = self.factor()
        expr = BinaryOp(expr, op, right)
        while self.check(Tag.SLASH_SLASH) \
                or self.check(Tag.ASTERISK) \
                    or self.check(Tag.PERCENT) \
                        or self.check(Tag.SLASH):
            op = self.next().tag
            right = self.factor()
            expr = BinaryOp(expr, op, right)

        return expr

    def factor(self) -> Expr:
        if not (self.check(Tag.PLUS)
                    or self.check(Tag.MINUS)
                        or self.check(Tag.TILDE)):

            return self.power()

        op: Tag = self.next().tag
        operand: Expr = self.factor()

        return UnaryOp(op, operand)

    def power(self) -> Expr:
        expr: Expr = self.primary()
        if not self.match(Tag.CARET):

            return expr

        op: Tag = Tag.CARET
        right: Expr = self.factor()
        expr = BinaryOp(expr, op, right)
        while self.match(Tag.CARET):
            right = self.factor()
            expr = BinaryOp(expr, op, right)

        return expr

    def primary(self) -> Expr:
        if self.check(Tag.INTEGER):

            return Integer(self.next().tok)

        if self.check(Tag.FLOAT):

            return Float(self.next().tok)

        if self.check(Tag.STRING):

            return String(self.next().tok)

        if self.check(Tag.IDENTIFIER) \
                and self.ahead_is(Tag.L_PAREN):

            return self.func_call()

        if self.check(Tag.IDENTIFIER) \
                and self.ahead_is(Tag.PERIOD):

            return self.method_call()

        if self.is_in({"True", "False"}):

            return Boolean(self.next().tok)

        if self.check(Tag.IDENTIFIER):

            return Identifier(self.next().tok)

        if self.check(Tag.L_PAREN):
            self.expect(Tag.L_PAREN)
            expr = self.expr()
            self.expect(Tag.R_PAREN)

            return expr

        raise ParserError(
            self.token.ln,
            self.token.col,
            self.token.line,
            """Encountered an unknown primary value."""
        )
