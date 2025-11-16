# (Almost) Context-free Grammar

## Definitions

### Grammatical Rules

- The grammatical syntax for Quartz is defined below
  - `...` denotes contents

| Symbol | Definition |
| - | - |
| INDENT | "is defined as" |
| `#` | Comment (no meaning) |
| `\|` | "or" |
| `+` | "one or more" |
| `?` | "optional" (zero or one) |
| `(...)` | Grouping |
| `{...}` | "zero or more" (repetition) |
| `"..."` | Literal characters / keywords |
| `/.../` | Regex |

### Regex

- Some of the rules for regex are defined below
  - `...` denotes contents
  - May not be entirely accurate

| Symbol | Defintion |
| - | - |
| `[...]` | Match *one* character from `...` |
| `[a-z]` | Any lowercase letter |
| `[^...]` | Any character *not* inside `...` |
| `(...)` | Grouping |
| `+` | One or more |
| `?` | Zero or one (optional) |
| `*` | Zero or more (repetition) |
| `\d` | Digit (0-9) |
| `\w` | Alphanumeric + underscore `[a-zA-Z0-9_]` |
| `\n` | Newline |
| `\\` | Literal backslash |
| `\.` | Literal dot |
| `.` | Any character (wildcard) |

## Notes

- The formal grammar laid out below is, in fact, not entirely context-free.
  - The INDENT/DEDENT tokens depend on contextual information of the prior indent level.

## Grammar

```gram

program
    statement+

# ---- Statements ----
statement
    simple_stmt | compound_stmt

simple_stmt
    (initialization | alias
                    | construct
                    | assignment
                    | func_call
                    | method_call
                    | pipeline
                    | import
                    | return) stmt_end

compound_stmt
    if_stmt | while_stmt | for_stmt | func_def

# ---- Simple Cases ----

initialization
    "imm"? IDENT ("as" IDENT)? (":" TYPE)? ":=" expr_pipe
alias
    "alias" IDENT ":=" IDENT
construct
    "construct" IDENT ("as" IDENT)?
assignment
    IDENT ((ASSIGNMENT_OP expr_pipe) | pipe_assign)
func_call
    IDENT "(" call_params? ")"
method_call
    (IDENT ".")+ func_call
pipeline
    expr ("->" pipe_stage)+
import
    basic_import | selective_import
basic_import
    "import" IDENT ("as" IDENT)?
selective_import
    "from" IDENT "import" ("*" | import_params)
return
    "return" expr

# ---- Compound Cases ----

if_stmt
    "if" expr_pipe suite {"else" "if" expr_pipe suite} ("else" suite)?
while_stmt
    ("while" | "until") expr_pipe suite
for_stmt
    "for" ((IDENT "in" range) | range) suite
func_def
    "define" IDENT "(" def_params? ")" suite

# ---- Statement Parts ----

stmt_end
    NEWLINE | ;
pipe_assign
    "->=" (pipe_stage)+
call_parameter
    expr_pipe | (IDENT ("=" expr_pipe)?)
call_params
    call_parameter {"," call_parameter}
pipe_stage
    (IDENT {expr}) | ("."? func_call) | (method_call)
import_parameter
    IDENT ("as" IDENT)?
import_params
    import_parameter {"," import_parameter}
range
    (IDENT | int) (".." | "..=") (IDENT | int)
def_parameter
    IDENT (":" TYPE)? ("=" expr_pipe)?
def_params
    def_parameter {"," def_parameter}

# ---- Blocks ----
suite
    NEWLINE INDENT statement+ DEDENT

# ---- Expressions ----

expr_pipe
    expr | pipeline

# `expr` could be expanded later.
# That's why it just
# jumps straight to `disjunction`.
expr
    disjunction

disjunction
    conjunction {"or" conjuction}
conjunction
    inversion {"and" inversion}
inversion
    ("not" inversion) | comparison

comparison
    bitwise_or {COMPARISON_OP bitwise_or}
bitwise_or
    bitwise_xor {"|" bitwise_xor}
bitwise_xor
    bitwise_and {"~" bitwise_and}
bitwise_and
    bitwise_shift {"&" bitwise_shift}
bitwise_shift
    sum {(">>" | "<<") sum}
sum
    term {("+" | "-") term}
term
    factor {("*" | "/" | "//" | "%") factor}
factor
    (("+" | "-" | "~")? factor) | power
power
    primary {"^" factor}
primary
    NUMBER | STRING
           | IDENT
           | "(" expr_pipe ")"
           | func_call
           | method_call

# ---- Lexical tokens (regex) ----
IDENT
    /[a-zA-Z_]\w*\??/
NUMBER
    /\d+(\.\d+)?/
STRING
    /("(\\.|[^"\\])*")|('(\\.|[^'\\])')/
NEWLINE
    /\n+/

# ---- Shorthand tokens ----
TYPE
    "int" | "float" | "str" | "bool" | "None"
          | (("list" | "set" | "hash") ("[" TYPE {"," TYPE} "]")?)

# Excludes "pipe assign" operator `->=`
ASSIGNMENT_OP
    "=" | "+=" | "-=" | "*="
        | "/=" | "^=" | "%=" | "&="
        | "|=" | "~=" | ">>=" | "<<="
COMPARISON_OP
    "<" | ">" | "==" | "!=" | "<=" | ">="
        | "is" | "is not" | "in" | "not in"

# ---- Non-context-free tokens ----
INDENT/DEDENT
    Produced by Lexer based on leading whitespace

```
