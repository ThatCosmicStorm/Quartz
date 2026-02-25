# Quartz

![Quartz logo](https://github.com/thatcosmicstorm/Quartz/blob/main/Quartz_Logo.png)

## Introduction

- Welcome to Quartz!
- Quartz is a syntactic and structural transformation over Python.
- Its defining feature is *pipelines*.

## Installation

- Requires Python 3.12 or newer

```bash
git clone https://github.com/thatcosmicstorm/quartz.git
cd quartz
pip install -e .
```

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

## Contributing to Quartz

- Have any ideas/suggestions to improve Quartz?
- Is everything breaking when you run your program?
- Open an issue on GitHub!

## WORK IN PROGRESS

- For now, Quartz is mainly theoretical, so you can't play around with it *yet*.
  - *Everything is subject to change.*
- After a working implementation is established, my next focus will be on docs.
