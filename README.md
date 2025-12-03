# Quartz

![Quartz logo](https://github.com/thatcosmicstorm/Quartz/blob/main/Quartz_Logo.png)

## Introduction

- Welcome to Quartz!
- Quartz is a **high-level interpreted** language.
- Its defining feature is *pipe-based composition*.

## Code Snippets

<table>
<tr>
<th>Python</th>
<th>Quartz</th>
</tr>
<tr>
<td>

```py
string = " HELLO WORLD "
print(string.strip().lower())
```
  
</td>
<td>

```qrtz
string := " HELLO WORLD "
string -> .strip -> .lower -> print
```

</td>
</tr>
</table>

- Both programs accomplish the same task.
- Comparing the two, Quartz conveys a much more understandable flow of functions.

## Current Design (compared w/ basic Python)

- Embraces the offside rule
  - Neither colons nor one-liners
- Pipeline operator `->`
  - Function return type arrow is `~>`
- `define`, not `def`
- `else if`, not `elif`
- `hash`, not `dict`
- `^`, not `**` (exponentiation)
  - `~`, not `^` (binary XOR)
  - `~` is also still binary NOT
- `%{}`, not `{}`, for `set` and `hash`
- `while` AND `until` loops
- Initialization (`:=`) is different from (re)assignment (`=`)
- Cloning implicit, aliasing explicit
  - Aliasing can be done at initialization
    - `index as i := 0`
  - Or as a standalone statement
    - `alias i := index`
- Range operators `..` (exclusive) and `..=` (inclusive), not `range()`
- `for` loops can look like `for 0..5` instead of `for _ in range(0, 5)`
  - A variable can still be used like `for i in 0..5`
- `construct` is used to create an instance of an object from a class
  - This plants the seed for a more extreme concept in the future
  - `construct MyObject as mb`, not `mb = MyObject()`
  - No alias is required (`construct MyObject`)
    - You can directly call methods like `MyObject.method()`

## Completed Features

- [x] Lexer
- [x] Parser
- [ ] Implementation

## Contributing to Quartz

- Have any ideas/suggestions to improve Quartz?
- Is everything breaking when you run your program?
- Open an issue on GitHub!

## WORK IN PROGRESS

- For now, Quartz is mainly theoretical, so you can't play around with it *yet*.
  - *Everything is subject to change.*
- Quartz **docs are unfinished and quite outdated** for the moment.
  - After a working implementation is established, this is my next focus.
