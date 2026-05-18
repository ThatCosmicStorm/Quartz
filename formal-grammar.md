# Formal Grammar

- The grammar for all *currently* implemented features of the Quartz programming language.

## Syntax

| Symbol | Definition |
| - | - |
| INDENT | Contents |
| `#` | Comment (no meaning) |
| `\|` | Or |
| `+` | One or more |
| `(...)` | Grouping |
| `[...]` | Zero or one |
| `{...}` | Zero or more |
| `"..."` | Literal characters |
| `/.../` | Regex |

## Grammar

```gram

program
    {statement}

# ---- Statements ----
statement
    (expr | simple) stmt_end
    | compound

simple
    assign
    | delete
    | return

compound
    if
    | for
    | function_definition
    | while

# ---- Simple Cases ----
assign
    expr ("=" expr)+
delete
    "del" expr {"," expr}
return
    [expr] "<<<" [("if" | "unless") expr]

# ---- Compound Cases ----
if
    "if" expr suite {"else if" expr suite} ["else" suite]
    | "unless" expr suite
for
    "for" [expr "in"] expr suite ["else" suite]
function_definition
    "fn" IDENT "(" [def_params] ")" [type] func_suite
while
    ("while" | "until") expr suite ["else" suite]

# ---- Statement Parts ----
call_params
    call_parameter {"," call_parameter} [","]
call_parameter
    expr
    | (IDENT ["=" expr])

def_params
    def_parameter {"," def_parameter} {"," def_default_param} [","]
def_default_param
    def_parameter "=" expr
def_parameter
    IDENT [":" type]

pipe_stage
    ["."] postfix
stmt_end
    NEWLINE
type
    postfix {"|" postfix}

# ---- Blocks ----
suite
    NEWLINE INDENT statement+ DEDENT

# ---- Expressions ----
expr
    base_expr {pipe}

pipe
    "->" pipe_stage

base_expr
    lambda
    | ternary

lambda
    "fn" "(" [lambda_params] ")" "=>" expr
lambda_params
    IDENT {"," IDENT} [","]
ternary
    disjunction ["<->" expr "if" expr]

disjunction
    conjunction {"or" conjunction}
conjunction
    inversion {"and" inversion}
inversion
    "not" inversion
    | comparison

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
    power
    | ("+" | "-" | "~") factor
power
    postfix {"^" factor}
postfix
    primary {postfix_op}
postfix_op
    "." IDENT
    | "(" [call_params] ")"
    | "[" subscript_list "]"
subscript_list
    subscript {"," subscript} [","]
subscript
    slice
    | expr
slice
    [expr] ":" [expr] [":" [expr]]
primary
    constant
    | collection
    | "(" expr ")"
collection
    dict
    | list
    | set
    | tuple
constant
    BOOLEAN
    | ELLIPSIS
    | FLOAT
    | INTEGER
    | NONE
    | STRING

# ---- Other Tokens ----
tuple
    "(" [collection_items | (expr ",")] ")"
list
    "[" [collection_items] "]"
set
    "${" [collection_items] "}"
dict
    "%{" [dict_items] "}"
collection_items
    expr {"," expr} [","]
dict_items
    expr ":" expr {"," expr ":" expr} [","]

BOOLEAN
    "True"
    | "False"

NONE
    "None"

ELLIPSIS
    "..."

COMPARISON_OP
    "<"
    | ">"
    | "=="
    | "!="
    | "<="
    | ">="
    | "is"
    | ("is" "not")
    | "in"
    | ("not" "in")

# ---- Lexical tokens (regex) ----
IDENT
    /([a-zA-Z_]\w*\??)/
INTEGER
    /\d+/
FLOAT
    /(\d+\.\d*|\.\d+)/
STRING
    /("(\\.|[^"\\])*")|('(\\.|[^'\\])')/
NEWLINE
    /\n+/

# ---- Non-context-free tokens ----
INDENT/DEDENT
    Produced by Lexer based on leading whitespace

```
