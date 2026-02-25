# Formal Grammar

## Grammar Syntax

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
    ((expr | simple) stmt_end)
    | compound

simple
    alias
    | assert
    | assignment
    | basic_import
    | channeled_assignment
    | initialization
    | raise
    | return
    | selective_import
    | type_alias
    | yield

compound
    class
    | for
    | function_definition
    | if
    | match
    | while
    | wrap

# ---- Simple Cases ----
annotated_assign
    expr ":" TYPE ["=" expr]
assert
    "assert" expr ["," STRING]
assign
    annotated_assign | augmented_assign | regular_assign
augmented_assign
    expr ((ASSIGNMENT_OP expr) | pipe_assign)
basic_import
    "import" expr ["as" IDENT] {"," expr ["as" IDENT]}
break
    "break"
continue
    "continue"
delete
    "del" expr
import
    basic_import | selective_import
pass
    "pass"
raise
    "raise" [expr ["from" expr]]
regular_assign
    expr "=" expr
return
    [expr] "<<<" ["if" expr ["else" expr]]
selective_import
    "from" expr "import" ("*" | import_params)
type_alias
    "type" IDENT "=" TYPE
yield
    "yield" expr

# ---- Compound Cases ----
class
    ["pub"] "class" IDENT ["(" IDENT {"," IDENT} [","] ")"] class_suite
decorator
    "@" IDENT NEWLINE (decorator | function_definition)
for
    "for" [expr "in"] expr suite
function_definition
    ["pub"] "fn" IDENT "(" [def_params] ")" ["~>" TYPE] func_suite
if
    "if" expr suite {"else" "if" expr suite} ["else" suite]
match
    "match" expr match_suite
struct
    ["pub"] "struct" IDENT class_suite
while
    ("while" | "until") expr suite

# ---- Statement Parts ----
call_parameter
    expr
    | (IDENT ["=" expr])
call_params
    call_parameter {"," call_parameter} [","]
def_parameter
    IDENT [":" TYPE] ["=" expr]
def_params
    def_parameter {"," def_parameter} [","]
import_parameter
    IDENT ["as" IDENT]
import_params
    import_parameter {"," import_parameter}
pipe_assign
    "->=" pipe_stage {"->" pipe_stage}
pipe_attribute
    ["."] {IDENT "."} IDENT
pipe_stage
    pipe_attribute [("(" [call_params] ")") | (":" expr {"," expr})]
stmt_end
    NEWLINE
target
    IDENT ["(" call_params ")"]

# ---- Blocks ----
suite
    NEWLINE INDENT statement+ DEDENT
class_suite
    NEWLINE INDENT [DOCSTRING NEWLINE] (IDENT ":" TYPE ["=" expr] NEWLINE)+ function_definition+ DEDENT
func_suite
    NEWLINE INDENT [DOCSTRING NEWLINE] statement+ DEDENT
match_suite
    NEWLINE INDENT ("case" expr suite)+ DEDENT

# ---- Expressions ----
expr
    ternary {"->" pipe_stage}

ternary
    disjunction ["if" expr "else" expr]
disjunction
    conjunction {"or" conjunction}
conjunction
    inversion {"and" inversion}
inversion
    "not" inversion

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
    power | (["+" | "-" | "~"] factor)
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
    [disjunction] ":" [expr] [":" [expr]]
primary
    BOOLEAN | DICT
            | DICT_COMPREHENSION
            | DOCSTRING
            | FLOAT
            | GENERATOR_COMPREHENSION
            | IDENT
            | INTEGER
            | LIST
            | LIST_COMPREHENSION
            | SET
            | SET_COMPREHENSION
            | STRING
            | TUPLE
            | "(" expr ")"

# ---- Other Tokens ----
TYPE
    INNER_TYPE {"|" INNER_TYPE}
INNER_TYPE
    IDENT ["[" [MORE_TYPE] "]"]
MORE_TYPE
    OR_TYPE {"," OR_TYPE} [","]
OR_TYPE
    TYPE {"|" TYPE}

BOOLEAN
    "True"
    | "False"

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

GENERATOR_COMPREHENSION
    "(" COMPREHENSION ")"
LIST_COMPREHENSION
    "[" COMPREHENSION "]"
SET_COMPREHENSION
    "${" COMPREHENSION "}"
DICT_COMPREHENSION
    "%{" DICT_COMP "}"
COMPREHENSION
    expr ("for" expr "in" expr)+ {"if" expr}
DICT_COMP
    expr ":" expr ("for" expr "in" expr)+ {"if" expr}

# Excludes "pipe assign" operator `->=`
ASSIGNMENT_OP
    "="
    | "+="
    | "-="
    | "*="
    | "/="
    | "^="
    | "%="
    | "&="
    | "|="
    | "~="
    | ">>="
    | "<<="
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
DOCSTRING
    /f?"""(\\.|[^"\\])*"""/
NEWLINE
    /\n+/

# ---- Non-context-free tokens ----
INDENT/DEDENT
    Produced by Lexer based on leading whitespace

```
