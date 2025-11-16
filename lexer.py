"""*The Quartz lexer.*
"""

from tokendef import Token, Tag

##############################
# SOME TOKEN DEFINITIONS
##############################

DIGITS = "0123456789"

KEYWORDS = {
    "if",
    "else",
    "while",
    "until",
    "define",
    "return",
    "is",
    "in",
    "not",
    "and",
    "or",
    "alias",
    "str",
    "int",
    "float",
    "list",
    "hash",
    "set",
    "bool",
    "True",
    "False",
    "None",
    "import",
    "as",
    "from",
    "assert",
    "break",
    "continue",
    "pass",
    "match",
    "case",
}

##############################
# LEXER
##############################


class Lexer:
    def __init__(self, program: str):
        self.program: str = self.clean_program(program)
        self.index = 0 ; self.i = self.index
        self.length: int = len(self.program) ; self.n = self.length
        self.char: str = self.program[self.i]
        self.tokens: list[Token] = []
        self.is_eof = False
        self.indent_stack = [0]
        self.in_parens = 0
        self.line_start = 0

    def clean_program(self, program: str):
        return "\n".join(
            line for line in program.splitlines() if line.strip() != ""
        )

    ##########################
    # Helper Functions
    ##########################

    def next(self):
        self.i += 1
        if self.i != self.n:
            self.char = self.program[self.i]
        else:
            self.is_eof = True

    def eof(self):
        while self.indent_stack != [0]:
            self.indent_stack.pop()
            self.token(Tag.DEDENT)
        self.token(Tag.EOF)

    def token(self, tag, tok=None):
        self.tokens.append(Token(tag, tok))

    ##########################
    # Main Functions
    ##########################

    def lexer(self) -> list[Token]:
        if self.n == 0:
            self.eof()
            return self.tokens
        while not self.is_eof:
            self.match_char()
        return self.tokens

    def match_char(self):
        match self.char:
            case "\n":
                self.newline()
            case _ if self.char.isspace():
                self.next()
                if self.is_eof:
                    self.eof()
            case _ if self.char.isalpha() or self.char == "_":
                self.identifier()
            case _ if self.char in DIGITS:
                self.integer()
            case '"' | "'":
                self.string()
            case "(":
                self.token(Tag.L_PAREN)
                self.in_parens += 1
                self.next()
                if self.is_eof:
                    self.eof()
            case ")":
                self.token(Tag.R_PAREN)
                self.in_parens -= 1
                self.next()
                if self.is_eof:
                    self.eof()
            case "[":
                self.token(Tag.L_BRACKET)
                self.in_parens += 1
                self.next()
                if self.is_eof:
                    self.eof()
            case "]":
                self.token(Tag.R_BRACKET)
                self.in_parens -= 1
                self.next()
                if self.is_eof:
                    self.eof()
            case "{":
                self.token(Tag.L_BRACE)
                self.in_parens += 1
                self.next()
                if self.is_eof:
                    self.eof()
            case "}":
                self.token(Tag.R_BRACE)
                self.in_parens -= 1
                self.next()
                if self.is_eof:
                    self.eof()
            case ";":
                self.token(Tag.SEMICOLON)
                self.next()
                if self.is_eof:
                    self.eof()
            case ",":
                self.token(Tag.COMMA)
                self.next()
                if self.is_eof:
                    self.eof()
            case "\\":
                self.backslash()
            case ".":
                self.period()
            case "=":
                self.equal()
            case "|":
                self.pipe()
            case ":":
                self.colon()
            case "%":
                self.percent()
            case "*":
                self.asterisk()
            case "+":
                self.plus()
            case "-":
                self.minus()
            case "<":
                self.l_angle()
            case ">":
                self.r_angle()
            case "^":
                self.caret()
            case "~":
                self.tilde()
            case "/":
                self.slash()
            case "&":
                self.ampersand()
            case "!":
                self.bang()
            case "#":
                self.hashtag()
            case _:
                self.next()
                if self.is_eof:
                    self.eof()

    ##########################
    # Case Functions
    ##########################

    def newline(self):
        if self.in_parens:
            self.next()
            if self.is_eof:
                self.eof()
            return
        self.token(Tag.NEWLINE)
        self.next()
        if self.is_eof:
            self.eof()
            return
        self.indent()

    def indent(self):
        spaces = 0
        while not self.is_eof and self.char == " ":
            spaces += 1
            self.next()
        indents = spaces // 4
        if indents > self.indent_stack[-1]:
            self.indent_stack.append(indents)
            self.token(Tag.INDENT)
        if indents < self.indent_stack[-1]:
            while indents < self.indent_stack[-1]:
                self.indent_stack.pop()
                self.token(Tag.DEDENT)
            if indents != self.indent_stack[-1]:
                raise Exception("Inconsistent indentation.")
        if self.is_eof:
            self.eof()

    def backslash(self):
        self.next()
        if self.is_eof:
            self.eof()
            return
        if self.char != "\n":
            return
        self.next()
        if self.is_eof:
            self.eof()
            return

    def hashtag(self):
        while self.char != "\n":
            self.next()
            if self.is_eof:
                self.eof()
                return
        if self.char == "\n":
            self.newline()

    def identifier(self):
        start = self.i
        while not self.is_eof and (self.char.isalnum() or self.char == "_"):
            self.next()
        ident = self.program[start : self.i]
        if ident:
            if ident in KEYWORDS:
                self.token(Tag.KEYWORD, ident)
            else:
                self.token(Tag.IDENTIFIER, ident)
        if self.is_eof:
            self.eof()

    def integer(self):
        start = self.i
        while not self.is_eof and self.char in DIGITS:
            self.next()
            if self.char == ".":
                self.int_period(start, end=self.i)
                return
        number = self.program[start : self.i]
        if number and self.char != ".":
            self.token(Tag.INTEGER, number)
        if self.is_eof:
            self.eof()

    def int_period(self, start=0, end=0):
        self.next()
        if self.is_eof:
            self.eof()
            return
        integer = self.program[start : end]
        if self.char == ".":
            self.token(Tag.INTEGER, integer)
            self.period_period()
            return
        while not self.is_eof and self.char in DIGITS:
            self.next()
        number = self.program[start : self.i]
        self.token(Tag.FLOAT, number)
        if self.is_eof:
            self.eof()

    def period(self):
        self.next()
        if self.is_eof:
            self.eof()
            return
        if self.char == ".":
            self.period_period()
            return
        elif self.char in DIGITS:
            self.period_int()
            return
        else:
            self.token(Tag.PERIOD)
        self.next()

    def period_int(self):
        start = self.i - 1
        while not self.is_eof and self.char in DIGITS:
            self.next()
        number = self.program[start : self.i]
        self.token(Tag.FLOAT, number)
        if self.is_eof:
            self.eof()

    def period_period(self):
        self.next()
        if self.is_eof:
            self.eof()
            return
        if self.char == "=":
            self.token(Tag.PERIOD_PERIOD_EQUAL)
            self.next()
            if self.is_eof:
                self.eof()
        elif self.char == ".":
            self.token(Tag.PERIOD_PERIOD_PERIOD)
            self.next()
            if self.is_eof:
                self.eof()
        else:
            self.token(Tag.PERIOD_PERIOD)

    def string(self):
        if self.char == '"':
            quote = '"'
        else:
            quote = "'"
        start = self.i
        self.next()
        if self.is_eof:
            self.eof()
            return
        while not self.is_eof and self.char != quote:
            self.next()
        string = self.program[start : self.i + 1]
        if self.program[start] == self.program[self.i]:
            self.token(Tag.STRING, string)
            self.next()
            if self.is_eof:
                self.eof()
                return
        if self.is_eof:
            self.eof()

    ##########################
    # Template Functions
    ##########################

    def equal(self):
        self.next()
        if self.is_eof:
            self.eof()
            return
        if self.char == "=":
            self.token(Tag.EQUAL_EQUAL)
            self.next()
            if self.is_eof:
                self.eof()
        elif self.char == ">":
            self.token(Tag.EQUAL_ARROW)
            self.next()
            if self.is_eof:
                self.eof()
        else:
            self.token(Tag.EQUAL)

    def pipe(self):
        self.next()
        if self.is_eof:
            self.eof()
            return
        if self.char == "=":
            self.token(Tag.PIPE_EQUAL)
            self.next()
            if self.is_eof:
                self.eof()
        else:
            self.token(Tag.PIPE)

    def colon(self):
        self.next()
        if self.is_eof:
            self.eof()
            return
        if self.char == "=":
            self.token(Tag.COLON_EQUAL)
            self.next()
            if self.is_eof:
                self.eof()
            return
        self.token(Tag.COLON)

    def percent(self):
        self.next()
        if self.is_eof:
            self.eof()
            return
        if self.char == "=":
            self.token(Tag.PERCENT_EQUAL)
            self.next()
            if self.is_eof:
                self.eof()
        elif self.char == "{":
            self.token(Tag.PERCENT_L_BRACE)
            self.next()
            if self.is_eof:
                self.eof()
        else:
            self.token(Tag.PERCENT)

    def asterisk(self):
        self.next()
        if self.is_eof:
            self.eof()
            return
        if self.char == "=":
            self.token(Tag.ASTERISK_EQUAL)
            self.next()
            if self.is_eof:
                self.eof()
        else:
            self.token(Tag.ASTERISK)

    def plus(self):
        self.next()
        if self.is_eof:
            self.eof()
            return
        if self.char == "=":
            self.token(Tag.PLUS_EQUAL)
            self.next()
            if self.is_eof:
                self.eof()
        else:
            self.token(Tag.PLUS)

    def minus(self):
        self.next()
        if self.is_eof:
            self.eof()
            return
        if self.char == "=":
            self.token(Tag.MINUS_EQUAL)
            self.next()
            if self.is_eof:
                self.eof()
        elif self.char == ">":
            self.token(Tag.ARROW)
            self.next()
            if self.is_eof:
                self.eof()
        else:
            self.token(Tag.MINUS)

    def l_angle(self):
        self.next()
        if self.is_eof:
            self.eof()
            return
        if self.char == "=":
            self.token(Tag.L_ANGLE_EQUAL)
            self.next()
            if self.is_eof:
                self.eof()
        elif self.char == "<":
            self.l_angle_l_angle()
            return
        self.token(Tag.L_ANGLE)

    def l_angle_l_angle(self):
        self.next()
        if self.is_eof:
            self.eof()
            return
        if self.char == "=":
            self.token(Tag.L_ANGLE_L_ANGLE_EQUAL)
            self.next()
            if self.is_eof:
                self.eof()
        else:
            self.token(Tag.L_ANGLE_L_ANGLE)

    def r_angle(self):
        self.next()
        if self.is_eof:
            self.eof()
            return
        if self.char == "=":
            self.token(Tag.R_ANGLE_EQUAL)
            self.next()
            if self.is_eof:
                self.eof()
        elif self.char == "<":
            self.r_angle_r_angle()
            return
        self.token(Tag.R_ANGLE)

    def r_angle_r_angle(self):
        self.next()
        if self.is_eof:
            self.eof()
            return
        if self.char == "=":
            self.token(Tag.R_ANGLE_R_ANGLE_EQUAL)
            self.next()
            if self.is_eof:
                self.eof()
        else:
            self.token(Tag.R_ANGLE_R_ANGLE)

    def caret(self):
        self.next()
        if self.is_eof:
            self.eof()
            return
        if self.char == "=":
            self.token(Tag.CARET_EQUAL)
            self.next()
            if self.is_eof:
                self.eof()
        else:
            self.token(Tag.CARET)

    def tilde(self):
        self.next()
        if self.is_eof:
            self.eof()
            return
        if self.char == "=":
            self.token(Tag.TILDE_EQUAL)
            self.next()
            if self.is_eof:
                self.eof()
        elif self.char == ">":
            self.token(Tag.TILDE_ARROW)
            self.next()
            if self.is_eof:
                self.eof()
        else:
            self.token(Tag.TILDE)

    def slash(self):
        self.next()
        if self.is_eof:
            self.eof()
            return
        if self.char == "=":
            self.token(Tag.SLASH_EQUAL)
            self.next()
            if self.is_eof:
                self.eof()
        elif self.char == "/":
            self.token(Tag.SLASH_SLASH)
            self.next()
            if self.is_eof:
                self.eof()
        else:
            self.token(Tag.SLASH)

    def ampersand(self):
        self.next()
        if self.is_eof:
            self.eof()
            return
        if self.char == "=":
            self.token(Tag.AMPERSAND_EQUAL)
            self.next()
            if self.is_eof:
                self.eof()
        else:
            self.token(Tag.AMPERSAND)

    def bang(self):
        self.next()
        if self.is_eof:
            self.eof()
            return
        if self.char == "=":
            self.token(Tag.BANG_EQUAL)
            self.next()
            if self.is_eof:
                self.eof()
        else:
            raise Exception("Unknown token")
