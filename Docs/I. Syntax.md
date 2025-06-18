# I. Syntax
## I.A. Comments
- Both full-line and in-line comments are supported in ReadAbl.
- Simply use `//`, and anything after it will be seen as a comment.
	- I found `//` to be in the most ergonomic position compared to other popular syntax.
```
// This is a comment.
{code stuff} // This is also a comment!
```
## I.B. Token Spacing
- A large part of ReadAbl is token spacing.
- (Almost) Every single token is spaced out.
- Personally, it is easier to mentally parse code this way.
```
// "Normal" Spacing
cmd:{arg}     // #1

// ReadAbl Spacing
cmd : { arg } // #2
```
- To me, #1 just looks smushed and less readable.
## I.C. Forms
- IMPORTANT: indents are 4 spaces long.
---
- The syntax for a command can be represented through two forms
```
// Default form (1)
cmd :
{
    arg ; // Semicolon REQUIRED
}

// Condensed form (2)
cmd : { arg } // Semicolon OPTIONAL
cmd : { arg ; }
```
- While both forms are valid, it may be better to use them at different times to improve readability.
### I.C.1. Default Form (1)
- It is used when there are more than two arguments to display or if the entire command is simply long (up to you to determine).
```
// Form 1
cmd :
{
    arg1 ;
    arg2 ;
    arg3 ;
}

cmd :
{
    this_is_a_long_argument_name_fr_fr_ong_ngl ;
}
```
### I.C.2. Condensed Form (2)
- It is used to condense the syntax needed when you have a single argument (or even two) to display.
```
// Form 2
cmd : { arg }

cmd : { arg1 ; arg2 } // Semicolon required to separate arguments
```
### I.C.3. Form Flexability
- While I do give recommendations, **you** can choose whichever form **you** think will improve readability the most.
	- ReadAbl isn't *just* strict syntax; we give some flexability :)
## I.D. Conditions
- Now, let's look at commands with an argument **and** a condition, used for commands like `if` statements (see V. Control Structures).
```
// Form 1
cmd :: cond :
{
    arg ;
}

// Form 2
cmd :: cond : { arg }
```
## I.E. Lining Up
- It's recommended in ReadAbl to line up your semicolons.
	- Get mad. Don't do it. It's **not required** in the slightest.
	- Just remember what ReadAbl is about: *readability!*
```
// Unordered
cmd :
{
    arg1 ;
    argument1 ;
    this_is_an_argument1 ;
}
// Lined up
cmd :
{
    arg1                 ;
    argument1            ;
    this_is_an_argument1 ;
}
```
#### I.E.1. Columns
- It's also recommended but **not required** to line up certain values to one another.
```
// Unordered
cmd :
{
    arg1  val1 ;
    argument1  value1 ;
    this_is_an_argument1  this_is_a_value1 ;
}
// Columns
cmd :
{
    arg1                  val1             ;
    argument1             value1           ;
    this_is_an_argument1  this_is_a_value1 ;
}
```
- You may notice that there isn't a symbol between the arguments and the values.
	- In Readabl, you don't need it (for some commands like `init` [see III.A. Initialization])
	- All you need is a minimum of two spaces to separate them.
	- This leaves the equals sign operator to do its actual job: to compare!
- Do you notice how the unique ReadAbl spacing creates separate columns w/o any need for a separator symbol, e.g., `|`?
- Now, of course, it's quite inconvenient to do this when you are dealing with >10 arguments/values in a single command.
- In that case, I recommend (again, **not required**) splitting the command into multiple commands.
```
// One bulky command
cmd :
{
    arg1                  val1             ;
    argument1             value1           ;
    this_is_an_argument1  this_is_a_value1 ;
    arg2                  val2             ;
    argument2             value2           ;
    this_is_an_argument2  this_is_a_value2 ;
    arg3                  val3             ;
    argument3             value3           ;
    this_is_an_argument3  this_is_a_value3 ;
}
// Separate smaller commands
cmd :
{
    arg1                  val1             ;
    argument1             value1           ;
    this_is_an_argument1  this_is_a_value1 ;
}
cmd :
{
    arg2                  val2             ;
    argument2             value2           ;
    this_is_an_argument2  this_is_a_value2 ;
}
cmd :
{
    arg3                  val3             ;
    argument3             value3           ;
    this_is_an_argument3  this_is_a_value3 ;
}
```