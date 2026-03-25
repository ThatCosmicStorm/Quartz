# Formal Grammar

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
    {expr stmt_end}

# ---- Statement Parts ----
call_parameter
    expr
    | (IDENT ["=" expr])
call_params
    call_parameter {"," call_parameter} [","]
stmt_end
    NEWLINE

# ---- Expressions ----
expr
    ternary

ternary
    disjunction ["if" expr "else" expr]
disjunction
    conjunction {"or" conjunction}
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
    power | (("+" | "-" | "~") factor)
power
    postfix {"^" factor}
postfix
    primary {postfix_op}
postfix_op
    ("." IDENT)
    | ("(" [call_params] ")")
    | ("[" subscript_list "]")
subscript_list
    subscript {"," subscript} [","]
subscript
    slice | expr
slice
    [expr] ":" [expr] [":" [expr]]
primary
    BOOLEAN
    | DICT
    | ELLIPSIS
    | FLOAT
    | IDENT
    | INTEGER
    | LIST
    | NONE
    | SET
    | STRING
    | TUPLE
    | "(" expr ")"

# ---- Other Tokens ----
TYPE
    postfix {"|" postfix}

BOOLEAN
    "True"
    | "False"

NONE
    "None"

ELLIPSIS
    "..."

TUPLE
    "(" [COLLECTION_ITEMS | (expr ",")] ")"
LIST
    "[" [COLLECTION_ITEMS] "]"
SET
    "${" [COLLECTION_ITEMS] "}"
DICT
    "%{" [DICT_ITEMS] "}"
COLLECTION_ITEMS
    expr {"," expr} [","]
DICT_ITEMS
    expr ":" expr {"," expr ":" expr} [","]

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
    /f?(("(\\.|[^"\\])*")|('(\\.|[^'\\])'))/
NEWLINE
    /\n+/

# ---- Non-context-free tokens ----
INDENT/DEDENT
    Produced by Lexer based on leading whitespace

```
