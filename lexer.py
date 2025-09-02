"""*The Quartz lexer.*
"""

##############################
# TOKEN DEFINITIONS
##############################

DIGITS = "0123456789"

KEYWORDS = {
    "if": "KW_IF",
    "else": "KW_ELSE",
    "while": "KW_WHILE",
    "until": "KW_UNTIL",
    "define": "KW_DEFINE",
    "return": "KW_RETURN",
    "is": "KW_IS",
    "in": "KW_IN",
    "not": "KW_NOT",
    "and": "KW_AND",
    "or": "KW_OR",
    "alias": "KW_ALIAS",
    "str": "KW_STR",
    "int": "KW_INT",
    "float": "KW_FLOAT",
    "list": "KW_LIST",
    "hash": "KW_HASH",
    "set": "KW_SET",
    "bool": "KW_BOOL",
    "True": "KW_TRUE",
    "False": "KW_FALSE",
    "None": "KW_NONE",
    "assert": "KW_ASSERT",
    "break": "KW_BREAK",
    "continue": "KW_CONTINUE",
    "pass": "KW_PASS",
    "match": "KW_MATCH",
    "case": "KW_CASE",
}

ESCAPE_LIST = {
    "\\", '"', "'",
    "a", "b", "f", "n", "r", "t", "v",
    "o", "x", "u", "U"
}

##############################
# LEXER
##############################

class Lexer:
    """*The functions behind the Quartz lexer.*
    """

    def __init__(self, program: str):
        self.program: str = program + " "
        self.token_dict: dict = {}
        self.index = 0 ; self.i = self.index
        self.length: int = len(self.program) ; self.n = self.length
        self.char: str = self.program[self.i]
        self.eof = False

    ##########################
    # Helper Functions
    ##########################

    def check_eof(self):
        if self.i < self.n:
            self.eof = False
        else:
            self.eof = True

    def next(self):
        self.i += 1
        self.check_eof()
        if not self.eof:
            self.char = self.program[self.i]
        else:
            self.char = ""

    def add_token(self, tok: str, start=None, end=None):
        if self.eof:
            return

        if start is None and end is None:
            loc = self.i
        else:
            loc = (start, end)

        self.token_dict[loc] = tok

    ##########################
    # Main Functions
    ##########################

    def lexer(self) -> dict:
        if self.n == 0:
            self.eof = True
            return self.token_dict

        while (self.i < self.n) and not self.eof:
            if self.char.isspace() and self.char != "\n":
                self.next()
                continue
            self.match_char()
        return self.token_dict

    def match_char(self):
        match self.char:
            case "\n":
                self.newline()
            case '"' | "'":
                self.string()
            case _ if self.char.isalpha() or self.char == "_":
                self.identifier()
            case _ if self.char in DIGITS:
                start = self.i
                self.integer(start)
            case "=":
                self.equal()
            case "(":
                self.add_token("L_PAREN")
                self.next()
            case ")":
                self.add_token("R_PAREN")
                self.next()
            case "[":
                self.add_token("L_BRACKET")
                self.next()
            case "]":
                self.add_token("R_BRACKET")
                self.next()
            case "{":
                self.add_token("L_BRACE")
                self.next()
            case "}":
                self.add_token("R_BRACE")
                self.next()
            case "|":
                self.pipe_char()
            case ";":
                self.add_token("SEMICOLON")
                self.next()
            case ":":
                self.colon()
            case ".":
                self.period()
            case ",":
                self.add_token("COMMA")
                self.next()
            case "!":
                self.bang()
            case "%":
                self.percent()
            case "*":
                self.asterisk()
            case "+":
                self.plus()
            case "<":
                self.l_angle()
            case ">":
                self.r_angle()
            case "^":
                self.caret()
            case "\\":
                self.backslash()
            case "~":
                self.tilde()
            case "-":
                self.minus()
            case "/":
                self.slash()
            case "&":
                self.ampersand()
            case "#":
                while self.char != "\n":
                    self.next()
            case _:
                raise Exception("Lexer Error: No token associated")

    ##########################
    # Case Functions
    ##########################

    def newline(self):
        self.add_token("NEWLINE")
        self.next()
        spaces = 0
        while True:
            if self.char != " ":
                return
            spaces += 1
            if spaces == 4:
                self.add_token("INDENT")
                spaces = 0
            self.next()

    def string(self):
        if self.char == '"':
            quote = '"'
        else:
            quote = "'"
        start = self.i
        while True:
            self.next()
            if self.char == quote:
                break
            elif self.char == "\\":
                self.backslash()
        self.add_token("STRING", start=start, end=self.i-1)

    def backslash(self):
        start = self.i
        self.next()
        if self.char not in ESCAPE_LIST:
            return
        else:
            self.add_token("ESCAPE", start=start, end=self.i)

    def identifier(self):
        start = self.i
        while self.char.isalnum() or self.char == "_":
            self.next()
        ident = self.program[start:self.i]
        if ident in KEYWORDS:
            self.add_token(KEYWORDS[ident], start=start, end=self.i-1)
        else:
            self.add_token("IDENT", start=start, end=self.i-1)

    def integer(self, start: int):
        self.next()
        if self.char == ".":
            self.int_period(start)
        elif self.char in DIGITS or self.char == "_":
            self.integer(start)
        else:
            self.add_token("INT", start=start, end=self.i)

    def int_period(self, start: int):
        self.next()
        if self.char in DIGITS or self.char == "_":
            self.float_num(start)
        else:
            self.i -= 1
            self.add_token("INT", start=start, end=self.i)
            self.period()

    def float_num(self, start: int):
        self.next()
        if self.char in DIGITS or self.char == "_":
            self.float_num(start)
        else:
            self.add_token("FLOAT", start=start, end=self.i)

    def period(self):
        self.next()
        if self.char == ".":
            self.period_period()
        else:
            self.add_token("PERIOD")

    def period_period(self):
        self.next()
        if self.char == "=":
            self.add_token("PERIOD_PERIOD_EQUAL")
        elif self.char == ".":
            self.add_token("PERIOD_PERIOD_PERIOD")
        else:
            self.add_token("PERIOD_PERIOD")

    ##########################
    # Template Functions
    ##########################

    def template(
        self, char: str, if_tok: str, else_tok: str,
        deep_char="", deep_if_tok=""
    ):
        self.next()
        if self.char != char:
            self.add_token(else_tok)
            return

        if not deep_char:
            self.add_token(if_tok)
            self.next()
        if deep_char:
            self.template(
                char=deep_char,
                if_tok=deep_if_tok,
                else_tok=else_tok
            )

    def equal_temp(self, char: str):
        self.template("=", char + "_EQUAL", char)

    ##########################

    def equal(self):
        self.next()
        if self.char == "=":
            self.add_token("EQUAL_EQUAL")
        elif self.char == ">":
            self.add_token("EQUAL_ARROW")
        else:
            self.add_token("EQUAL")

    def pipe_char(self):
        self.equal_temp("PIPE")

    def colon(self):
        self.template(
            "=", "COLON_EQUAL", "COLON",
            ">", "COLON_EQUAL_ARROW"
        )

    def bang(self):
        self.next()
        if self.char == "=":
            self.add_token("BANG_EQUAL")
        else:
            raise Exception("Lexer Error: No token associated")

    def percent(self):
        self.next()
        if self.char == "=":
            self.add_token("PERCENT_EQUAL")
        elif self.char == "{":
            self.add_token("PERCENT_L_BRACE")
        else:
            self.add_token("PERCENT")

    def asterisk(self):
        self.template(
            "*", "ASTERISK_ASTERISK", "ASTERISK",
            "=", "ASTERISK_ASTERISK_EQUAL"
        )

    def plus(self):
        self.equal_temp("PLUS")

    def l_angle(self):
        self.next()
        if self.char == "=":
            self.add_token("L_ANGLE_EQUAL")
        elif self.char == "<":
            self.equal_temp("L_ANGLE_L_ANGLE")
        else:
            self.add_token("L_ANGLE")

    def r_angle(self):
        self.next()
        if self.char == "=":
            self.add_token("R_ANGLE_EQUAL")
        elif self.char == ">":
            self.equal_temp("R_ANGLE_R_ANGLE")
        else:
            self.add_token("R_ANGLE")

    def caret(self):
        self.equal_temp("CARET")

    def tilde(self):
        self.next()
        if self.char == "=":
            self.add_token("TILDE_EQUAL")
        elif self.char == ">":
            self.add_token("TILDE_R_ANGLE")
        else:
            self.add_token("TILDE")

    def slash(self):
        self.equal_temp("SLASH")

    def ampersand(self):
        self.equal_temp("AMPERSAND")
