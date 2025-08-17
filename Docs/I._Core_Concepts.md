# I. Core Concepts

## I.i. Comments

- Use `//` for single-line and in-line comments.
- Use `/*` and `*/` for multi-line comments.

``` qrtz
// Single-line comment
code stuff // In-line comment

/*
Multi-line
comment
*/
```

## I.A. Pipelines

- The **heart of Quartz** is pipelines.
- It lets you pass values from one transformation and/or action to the next.
- As a *simple sequence of steps*, the code becomes more readable.
  - `>>` is used for data transformations
  - `:>` is used for actions done with the data

``` qrtz
// Through the pipe
" HELLO WORLD " >> trim >> lower :> print

// Down the pipe
" HELLO WORLD "
>> trim
>> lower
:> print
```

- There are no methods in Quartz: only functions.
- No nested calls, no clutter.

### I.A.1. Implying the First Argument

- Each step receives the *value from the previous step* as input.

``` qrtz
a >> f            // -> f(a)
a >> f b          // -> f(a, b)

a >> f >> f b     // -> f(f(a), b)
```

- This means functions like `append` are now **clearer** (in pipelines).

``` qrtz
// `append` can be written like so
append([], ".")

// But in a pipeline, the first argument is already implied
[] >> append "."
```

## I.B. Variables

### I.B.1. Binding

- You can bind a value to a variable using `=`.
  - Use *all caps* to convey a constant.

``` qrtz
username = "Randi"     // Variable by default
NUM = 5                // All caps case makes it a constant
```

#### I.B.1.a. Pipelines

- You can also bind a value using the `=>` pipeline operator.
  - This is especially helpful inside a pipeline.

``` qrtz
" HELLO WORLD "
>> trim
>> lower
=> message
:> print
```

### I.B.2. Assignment

- Assigning a new value to a variable is done with `<-`.
  - A constant cannot be assigned a new value.

``` qrtz
username <- "Jane"     // Variable assigned the value `"Jane"`
NUM <- 10              // ERROR: Cannot assign to a constant
```

#### I.B.2.a. Pipelines

- To take the result of a pipeline and assign it to a variable...
  - If the variable comes first, `<-` comes before the name.
  - If it's in the middle of a pipeline, `<-` comes after the name.

``` qrtz
// Before
<- username >> upper

" kendra "
>> upper
>> username <-     // Middle
:> print
```

#### I.B.2.b. Other Operators

- The usual math operators and more can be used in conjunction with `<-`.

``` qrtz
x = -1
x <- 0  // Basic
x +<- 1 // Same as x <- x + 1
```
