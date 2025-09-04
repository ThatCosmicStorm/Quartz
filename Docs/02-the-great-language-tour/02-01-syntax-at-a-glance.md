# Syntax at a Glance

- Oh, you *are* actually interested?
- Let's get started[^1]!

## Comments

- If you haven't already noticed[^2], `#` signifies comments:

```qrtz
# Single-line
x := 5 # In-line

# Multi-line
# comment
```

## Indentation Rules

- Here at Quartz, we want to empower you to write clean, readable code[^3].
- That starts with the indentation.
- An indent is hard-coded[^4] as **exactly 4 spaces**: NOT TABS!

## Example Program

- Let's *actually* look at Quartz "syntax at a glance."

```qrtz
# Dice Roller + REPL


define rollDie(sides: int) int
    return rand(1..=sides)

    # `rand` returns a random `int` in a given range


define rollALot(rolls: int) list
    results := []

    for i in 1..=rolls
        die_num := rollDie(6)
        results -> append die_num

        roll_num := i -> str

        if die_num == 6
            print("Wow! You rolled a six on Roll #" + roll_num + ".")
        else
            print("Roll #" + roll_num + ": " + die_num)

    return results


define rollAvg(results: list) int
    sum := 0

    for result in results:
        sum += result

    roll_num = results -> len

    # The expression is treated as (sum / roll_num) -> int
    average := sum / roll_num -> int

    return average


define main()
    print("Welcome to the Dice Roller!")

    RUNNING := True
    while RUNNING
        print("How many rolls would you like to do?")

        rolls := input -> int

        if rolls:
            results := rollALot(rolls)
        else:
            print("No rolls? Feeling unlucky today? I get it.")

        print("Would you like to know your average roll? (y/n)")

        if input() == "y":
            results -> rollAvg -> print


main()

```

- In one program, we've used these concepts:
  - Comments
  - Variables
  - Functions
  - Collections
  - Loops
  - Conditionals
  - Output
  - Expressions
- Hopefully, this gives you a better feel for how the syntax works in practice.
- You don't have to understand what's going on yet[^5]!
- We'll delve into each of these features individually and more!

---

[^1]: But before we can talk about the fun stuff (pipelines), we have to get through the boilerplate of programming concepts.
  It's unfortunate, but you just need patience.
[^2]: We just want to clarify everything as is the goal of Quartz ;\)
[^3]: What an original, revolutionary goal!
  No one has ever thought of this!
[^4]: Hard-coded indentation ensures consistency across not only your own program but across all programs ever written.
[^5]: If you already can read this code, keep reading anyway!
