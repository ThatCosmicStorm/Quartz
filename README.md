# Quartz

![Quartz logo](https://github.com/thatcosmicstorm/Quartz/blob/main/Quartz_Logo.png)

## Introduction

- Welcome to Quartz!
- Quartz is a syntactic and structural transformation over Python.
- Its defining feature is *pipelines*.

## Code Snippets

<table>
<tr>
<th>Python</th>
<th>Quartz</th>
</tr>
<tr>
<td>

```py
print(" HELLO WORLD ".strip().lower())
```

</td>
<td>

```qrtz
" HELLO WORLD " -> .strip -> .lower -> print
```

</td>
</tr>
</table>

- Both programs accomplish the same task.
- Comparing the two, Quartz conveys a much more understandable flow of functions.

## Installation

- Requires Python 3.10 or newer

```bash
git clone https://github.com/thatcosmicstorm/quartz.git
cd quartz
pip install -e .
```

## WORK IN PROGRESS

- Pay attention to the `working-grammar.md` file, as it contains all the grammar for currently implemented features.
  - Eventually, the goal is to have `working-grammar.md` *match* `formal-grammar.md`.
- **Open issues on GitHub if there are any problems, ideas, suggestions, comments, etc.**
