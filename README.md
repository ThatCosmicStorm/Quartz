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

## Design (in comparison w/ Python)

- Embraces the offside rule
  - Neither colons nor one-liners
- Pipeline operator `->`
  - Function return type arrow is `~>`
- `define` instead of `def`
- `else if` instead of `elif`
- `until` alongside `while` loops
- Distinguishes initialization from assignment
- Cloning implicit, aliasing explicit
- Range operators `..` and `..=` instead of `range()`
- `for` loops can look like `for 0..5` instead of `for _ in range(0, 5)`
- `construct` is used to create an instance of an object
  - This plants the seed for a more extreme concept in the future

## Completed Features

- [x] Lexer
- [x] Parser
- [ ] Implementation

## Contributing to Quartz

- Have any ideas/suggestions to improve Quartz?
- Open an issue on GitHub!

## WORK IN PROGRESS

- For now, Quartz is mainly theoretical, so you can't play around with it *yet*.
  - Everything is subject to change.
- Quartz docs are unfinished and quite outdated for the moment.
  - After a working implementation is established, this is my next focus.
