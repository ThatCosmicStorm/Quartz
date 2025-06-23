# Quartz

![Quartz logo](https://github.com/thatcosmicstorm/Quartz/blob/main/Quartz_Logo.png)

## i. Introduction

- Welcome to Quartz!
- Quartz (formerly known as ReadAbl) is a high-level interpreted language.
- Inspired by flow-based programming, Quartz is based on pipe-based composition, that is, taking data through a "pipe" of chained functions!
- Quartz also likes to emphasize readability, in-line transformation, and functional clarity.

## ii. Why Quartz?

- Readable by default
  - Transforms data like you're telling a story
- Functional pipelines
  - Clear, modular composition with `>>`
- Expressive branching
  - Inline syntax with `then` / `if` and `else`
- Eases debugging
  - Tools like `tap()` allow you to observe the data as it goes through the pipe

## iii. FizzBuzz Example Code

``` qrtz
define FizzBuzz(n) {
    for item in 1..(n+1) {
        item
        >> then
            if _ % 15 == 0 => "FizzBuzz" // Underscore represents `item`
            otif % 3  == 0 => "Fizz" // Underscore is actually optional!
            otif % 5  == 0 => "Buzz"
            else           => _
        >> write
    }
}
```

## iv. Contributing to Quartz (WARNING!)

- WARNING: Quartz may suck.
- I am giving you explicit permission to **flame me for anything** that sucks or doesn't make sense.
  - You may see **a lot** of things lol.
- Have any ideas/suggestions to improve Quartz?
- Open an issue on GitHub or contact me directly!
  - I'm friendly, promise :)

## v. WORK IN PROGRESS

- Everything shown about Quartz is incomplete and subject to change.
- The language is mainly a concept, so you can't play around with it *yet*.
- To move on to the actual semantics of Quartz, go to the GitHub Wiki.
