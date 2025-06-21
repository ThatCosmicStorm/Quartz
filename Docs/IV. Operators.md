# IV. Operators

- Pay attention!
- A lot of these are the same as Python but some **are not**.
- All operators will occur with the same syntactic spacing as shown below.

``` rdbl
`x` sign `y`
```

## IV.A. Essential

| Sign | Name                      |
| ---- | ------------------------- |
| {    | Function start            |
| }    | Function end              |
| ;    | Argument end/separator    |
| ::   | Macro/Condition separator |

## IV.B. Arithmetic

| Sign | Name           |
| ---- | -------------- |
| +    | Addition       |
| -    | Subtraction    |
| *    | Multiplication |
| ^    | Exponentiation |
| /    | Division       |
| %    | Modulus        |
| %%   | Floor division |
| /%/  | Round division |

## IV.C. Resign

| Sign | Operation         |
| ---- | ----------------- |
| ->   | Resign `y` to `x` |
| <-   | Resign `x` to `y` |

## IV.D. Comparison

| Sign | Name                     |
| ---- | ------------------------ |
| =    | Equal                    |
| !=   | Not equal                |
| >    | Greater than             |
| <    | Less than                |
| >=   | Greater than or equal to |
| <=   | Less than or equal to    |

## IV.E. Boolean

### IV.E.1. Logical

| Sign | Returns True When      |
| ---- | ---------------------- |
| AND  | Both are true          |
| OR   | At least one is true   |
| NOT  | Reverses boolean value |

### IV.E.2. Identity

| Sign   | Returns True When             |
| ------ | ----------------------------- |
| is     | Both refer to the same object |
| is not | Refer to different objects    |

### IV.E.3. Membership

| Sign   | Returns True When    |
| ------ | -------------------- |
| in     | If `x` is in `y`     |
| not in | If `x` is not in `y` |

## IV.F. Bitwise

| Sign | Name          |
| ---- | ------------- |
| &    | Bitwise AND   |
| \|   | Bitwise OR    |
| #    | Bitwise XOR\* |
| ~    | Bitwise NOT   |
| <<   | Left shift    |
| >>   | Right shift   |

- \* I'm leaving the caret symbol `^` to represent exponentiation, again, having the proper symbol do its job.
