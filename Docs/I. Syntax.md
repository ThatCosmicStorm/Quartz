# I. Syntax

## I.A. Comments

- Both full-line and in-line comments are supported in ReadAbl.
- Simply use `//`, and anything after it will be seen as a comment.
  - I found the slash key to be in the most ergonomic position compared to other popular syntax.

``` rdbl
// This is a comment.
{code stuff} // This is also a comment!
```

## I.B. Token Spacing

- A large part of ReadAbl is token spacing.
- Almost ***every*** single token is spaced out.
- Personally, it is easier to mentally parse code this way.

``` rdbl
// "Normal" Spacing
func{arg}     // #1

// ReadAbl Spacing
func { arg } // #2
```

- To me, #1 just looks smushed and less readable.

## I.C. Forms

- IMPORTANT: indents are 4 spaces long.

---

- The syntax for a function can be represented through three forms.

``` rdbl
// Default form (1)
func
{
    arg1 ; // Semicolon REQUIRED
    arg2 ;
}

// Condensed (C) form (2)
func {
    arg1 ; // Semicolon REQUIRED
    arg2 ;
}

// Compact form (3)
func { arg } // Semicolon OPTIONAL
func { arg1 ; arg2 } // Semicolon REQUIRED
```

- While all forms are valid, it may be better to use them at different times to improve readability.
- **You** can choose whichever form **you** think will improve readability the most.
  - ReadAbl offers *flexability* for readability :)

## I.D. Macros and Conditions

- As we know, functions like `if` aren't really functions, so they get their own syntax as macros.
- Essentially, the same as a function except now requiring a condition.
  - Conditions are statements that get evaluated as True or False.
  - See V. Control Stuctures.

```rdbl
// Form 1
macro :: cond
{
    arg ;
}

// Form 2

macro :: cond {
    arg ;
}

// Form 3
macro :: cond { arg }
```

## I.E. Lining Up (Stylistic Choice)

- It's *recommended* in ReadAbl to line up your semicolons.
  - Get mad. Don't do it. It's **not required** in the slightest.
  - Just remember what ReadAbl is about: *readability!*

``` rdbl
// Unordered
func
{
    arg1 ;
    argument1 ;
    this_is_an_argument1 ;
}
// Lined up
func
{
    arg1                 ;
    argument1            ;
    this_is_an_argument1 ;
}
```

### I.E.1. Columns

- It's also *recommended* but **not required** to line up certain values to one another.

``` rdbl
// Unordered
func
{
    [ i1 , i2 ] ;
    [ item1 , item2 ] ;
    [ this_is_an_item1 , this_is_another_item2 ] ;
}
// Columns
func
{
    [ i1               , i2                    ] ;
    [ item1            , item2                 ] ;
    [ this_is_an_item1 , this_is_another_item2 ] ;
}
```

- Do you notice how the unique ReadAbl spacing creates separate columns w/o any need for a separator symbol?
