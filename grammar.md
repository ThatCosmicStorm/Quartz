# Functional Grammar

- The theoretical grammar for the new version of the Quartz programming language.

## Syntax

| Symbol | Definition |
| - | - |
| `# ...` | Comment (no meaning) |
| `p` | Nonterminal symbol |
| `p1 p2` | Sequence |
| `p1 \| p2` | Or |
| `p+` | One or more |
| `(...)` | Grouping |
| `[...]` | Zero or one |
| `{...}` | Zero or more |
| `"..."` | Terminal symbol |
| `/.../` | Regex |

- Note:
  - Sequences like `p1 p2 | p3 p4` are parsed as `(p1 p2) | (p3 p4)`
  - I.e., the sequence before `|` OR the sequence after `|`

## Grammar

```gram

program
    {statement}

# ---- Statements ----
statement
    assign
    | class
    | export
    | function
    | import
    | type_alias

assign
    assign_regular
    | assign_unpack
assign_regular
    IDENT [":" type] "=" expr NEWLINE
assign_unpack
    IDENT ("," IDENT)+ "=" expr NEWLINE

class
    {decorator} "class" IDENT ["(" ")"] class_suite

decorator
    IDENT ["(" ")"] NEWLINE

export
    "export" IDENT {"," IDENT}

function
    {decorator} [type_signature] IDENT "(" def_params ")" "=" or_suite

import
    import_basic
    | import_selective
import_basic
    "import" expr ["as" IDENT]
import_selective
    "from" expr "import" (IDENT "as" IDENT | IDENT {"," IDENT})

type_alias
    "type" expr "=" expr

type_signature
    "::" type {"," type} "::" type NEWLINE

# ---- Statement Helpers
or_suite
    expr NEWLINE
    | suite
suite
    NEWLINE INDENT expr DEDENT

# ---- Expressions ----
expr
    constant

atom
    constant
    | IDENT

constant
    BOOLEAN
    | ELLIPSIS
    | FLOAT
    | INTEGER
    | NONE
    | STRING

BOOLEAN
    "True"
    | "False"

NONE
    "None"

ELLIPSIS
    "..."

# ---- Lexical tokens ----
IDENT
    /(_)|([@!]?[a-zA-Z_]\w*\??)/
INTEGER
    /\d+/
FLOAT
    /((\d+\.\d*)|(\.\d+))([eE][\+-]?\d+)?/
STRING
    /("((\\.)|[^"\\])*")|('((\\.)|[^'\\])*')|("""((\\.)|[^"""\\])*""")/
NEWLINE
    /(\r\n)|(\r)|(\n)/

# ---- Context-necessary tokens ----
INDENT/DEDENT
    Produced by Lexer based on leading whitespace

```
