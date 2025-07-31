# Quartz

![Quartz logo](https://github.com/thatcosmicstorm/Quartz/blob/main/Quartz_Logo.png)

## i. Introduction

- Welcome to Quartz!
- Quartz is a **high-level** *interpreted* language.
- Quartz's forte is pipe-based composition, i.e., taking data through a "pipe" of chained functions.

## ii. Example Code

- Take the following Python code.

``` py
print(" HELLO WORLD ".strip().lower())
```

- In contrast, here's how you would write it in Quartz.

``` qrtz
" HELLO WORLD " >> trim >> lower :> print
```

- Comparing the two, Quartz conveys a much easier flow of functions.
  - First, you show the data you want to transform or perform an action with.
  - Then, you show each transformation and/or action step-by-step.

## iii. Contributing to Quartz

- Have any ideas/suggestions to improve Quartz?
- Open an issue on GitHub (with the appropriate label, of course)!
  - I'll respond as soon as I am able and can formulate a good response.

## iv. WORK IN PROGRESS

- Everything shown about Quartz is incomplete and subject to change.
- The language is mainly a concept, so you can't play around with it *yet*.
- To move on to the actual semantics of Quartz, go to the GitHub Wiki.
