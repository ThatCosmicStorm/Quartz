# Quartz

<img src="https://github.com/thatcosmicstorm/Quartz/blob/main/Quartz_Logo.png" alt="Quartz logo" width="25%" height="auto">

## Introduction

- Welcome to Quartz!
- Quartz is a **high-level interpreted** language.
- Its defining feature is *pipe-based composition*.

## Code Snippets

- Take the following Python code.

``` py
string = " HELLO WORLD "
print(" HELLO WORLD ".strip().lower())
```

- In contrast, here's how you would, or should, write it in Quartz.

``` qrtz
string := " HELLO WORLD "
string -> trim -> lower -> print
```

- Comparing the two, Quartz conveys a much more understandable flow of functions.

## Goals

### Main

- **Create a functioning, turing-complete version**

### Design

- Simplistic look and feel, akin to Python
  - No need for braces and semicolons to flood the program
- Embraces the off-side rule
  - No unnecessary colons or "end" keywords
- Pipe-based composition
  - The superior way of representing chained functions

## Contributing to Quartz

- Have any ideas/suggestions to improve Quartz?
- Open an issue on GitHub!

## WORK IN PROGRESS

- For now, Quartz is largely theoretical, so you can't play around with it *yet*.
- Keep in mind, at this stage, everything is subject to change.
- To read the Quartz documentation, go to the Docs folder.
