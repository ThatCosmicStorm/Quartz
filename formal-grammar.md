# Context-free Grammar

- Defining formal grammar, or at least some fundamentals, is incredibly helpful when making abstract syntax trees (ASTs), a method of representing program structure.
  - It took me roughly a week to comprehend the succeeding concepts and write this draft.

## Definitions

### Augmented EBNF

- The grammar is structured using an augmented form of extended Backus-Naur form (EBNF), a common syntax used for context-free grammar.
- My augmented EBNF rules are defined below, using `...` to denote contents:

| Symbol | Definition |
| - | - |
| `=` | "is defined as" |
| `#` | Comment (no meaning) |
| `\|` | "or" |
| `+` | "one or more" |
| `?` | "optional" (zero or one) |
| `{...}` or `*` | "zero or more" (repetition) |
| `"..."` | Literal characters / keywords |
| `/.../` | Regular-expression notation (regex) |

### Augmented Regex

- Regex is used for defining lexicographical rules, a limitation of EBNF.
- My augmented regex rules are defined below, `...` again denoting contents:

| Symbol | Defintion |
| - | - |
| `[...]` | Match *one* character from `...` |
| `[a-z]` | Any lowercase letter |
| `[^...]` | Any character *not* inside |
| `\d` | Digit (0-9) |
| `\w` | Alphanumeric + underscore `[a-zA-Z0-9_]` |
| `\n` | Newline |
| `\\` | Literal backslash |
| `\.` | Literal dot |
| `.` | Any character |

- Any regex syntax not defined here borrows its definition from the augmented EBNF.

## Current Draft

``` ebnf
program         = statement+

# ---- Statements ----
statement       = simple_stmt | compound_stmt

simple_stmt     = (assignment | expr | func_call | pipeline) NEWLINE | ";"
declaration     = IDENT ":=" (expr | func_call | pipeline)
assignment      = IDENT ("="
                | "+=" | "-=" | "*=" | "/=" |"**=" | "%="
                | "&=" | "|=" | "~=" | "^=" | ">>=" | "<<=" ) (expr
                | func_call | pipeline)
func_call       = IDENT "(" expr ")"
pipeline        = IDENT (("->" IDENT IDENT?) | ("->" func_call))+

compound_stmt   = if_stmt | while_stmt | func_def
if_stmt         = "if" expr suite {"else" "if" expr suite} ["else" suite]
while_stmt      = ("while" | "until") expr suite
func_def        = "define" IDENT "(" parameters? ")" suite

parameters      = IDENT {"," IDENT}

# ---- Blocks ----
suite           = simple_stmt | NEWLINE INDENT statement+ DEDENT

# ---- Expressions ----
expr            = comparison {("and" | "or") comparison}
comparison      = arith {("<" | ">" | "==" | "!=" | "<=" | ">="
                | "is" | "is" "not" | in | "not" "in") arith}
arith           = term {("+" | "-") term}
term            = factor {("*" | "/" | "%") factor}
factor          = ("+" | "-" | "not") factor | primary
primary         = NUMBER | STRING | IDENT | "(" expr ")"

# ---- Lexical tokens ----
IDENT           = / [a-zA-Z_]{\w} /
NUMBER          = / \d+ [\. \d+]? /
STRING          = / "{[^"\\] | \\.}" | '{[^'\\] | \\.}' /
NEWLINE         = / \n+ /
INDENT/DEDENT   = produced by lexer based on leading whitespace
```

## Endnotes

- To clarify, the quotes used in the `STRING` definitions represent literal quotes.
- Whitespace has neither grammatical nor lexical significance.
  - In this instance, it is solely used to introduce more readability.
