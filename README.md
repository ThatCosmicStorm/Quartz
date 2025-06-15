# ReadAbl
![ReadAbl logo](https://github.com/thatcosmicstorm/ReadAbl/blob/main/ReadAbl_Logo2.png)
## i. Background Info
- Here's a guide to learning the ReadAbl Programming Language!
- ReadAbl is a high-level, interpreted programming language similar to Python (except w/o OOP, ew).
- The "why" of ReadAbl is to make a programming language that places a *large* emphasis on **readability** and **clear syntax**.
- For right now, consider this a preview of a language that could exist if given enough support.
## ii. Other Names
- I acknowledge that ReadAbl may not be the best name in the world for a programming language, so here are a few alternatives I made.
	- Priman
		- Same name as a conlang I made a few years ago
		- Just sounds pretty cool
	- SpaCeR
		- "C" because the family gave inspiration for the braces and semicolons.
		- "R" because it stands for Readability :)
- If you have any suggestions, please let me know.
- Or if you like ReadAbl as is, also let me know.
## iii. Comments
- Both full-line and in-line comments are supported in ReadAbl.
- Simply use `//`, and anything after it will be seen as a comment.
```
// This is a comment.
{code stuff} // This is also a comment!
```
## I. Universal Command Syntax
- IMPORTANT: Indents are 4 spaces long.
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
- You'll quickly notice that everything is spaced out.
- This is because, personally, it's easier to mentally parse code when **each token is already separated**.
- Let's give a side-by-side comparison, so you can hopefully understand.
```
// "Normal"
cmd:{arg}     // #1

// ReadAbl
cmd : { arg } // #2
```
- To me, #1 just looks smushed and less readable.
### I.A. When to Use Each Form
- While both forms are syntactically correct, it may be better to use Form 1 and 2 at different times to improve readability.
#### I.A.1. Form 1
- Default form, a.k.a., Form 1 will usually be the main form you'll use.
- It is used when there are multiple arguments to display or if a single argument simply has a long name (> 25 characters).
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
    this_is_a_long_argument_name ;
}
```
#### 1.A.2. Form 2
- Condensed form, a.k.a., Form 2, will usually be the more uncommon form you'll use, but it still has its place.
- It is used when you have a single, small argument to display, or even multiple, small arguments.
```
// Form 2
cmd : { arg }

cmd : { arg1 ; arg2 } // Semicolon required to separate arguments
```
### I.B. Conditions
- Now, let's look at commands with an argument **and** a condition, used for commands like `if` statements.
```
// Form 1
cmd :: cond :
{
    arg ;
}

// Form 2
cmd :: cond : { arg }
```
## II. Variables and Data Types
- In ReadAbl, there are basically only two commands that you need to set up variables.
	1. `init`
		- Used to declare variables and assigns an initial value.
	2. `resign`
		- Used to reassign (herby referred to as resign) a new value to a declared variable.
### II.A. Data Types
- The data types in ReadAbl are:
	- `int` for integers
	- `float` for floating-point numbers
	- `str` for strings
	- `array` for arrays
	- `list` for lists
	- `bool` for Boolean values
	- `cond` for conditional statements
	- `func` for functions
#### II.A.1. Arrays vs Lists 
- `array` and `list` both hold multiple pieces of data in an organized, indexed set.
- But...
	- `array` can only hold the same type of data
- While...
	- `list` can hold multiple types
### II.B. Variables
#### II.B.i. SO MANY EQUALS SIGNS >:(
- Rant time :)
- While Python is quite readable even to beginners (disregarding OOP stuff like classes), there is one thing I see littered everywhere... ***EQUALS SIGNS!!!***
- EVERYWHERE you look in a Python program, you see `x = y`.
- Now, why do I hate this even as an avid Python programmer?
- Because in a large program (>1000 lines of code) it's hard to keep track of the age of variables.
	- Average line of thought:
		- Have I seen `variable_1` before?
		- Has `variable_1` been used yet?
		- Or did I just define it...?
- In ReadAbl, you **have to** distinguish between when you first define a variable and when you're just changing the value.
#### II.B.1. Initializing a Variable
- To initialize a variable, use `init` like so.
```
// Form 1
init :
{
    var1  4          ; // var1 = 4
    var2  "among us" ; // var2 = "among us"
}

// Form 2
init : { variable1  4 ; var 2  "among us" }
```
- It's recommended in ReadAbl to line up your semicolons.
	- Get mad. Don't do it. It's not required in the slightest.
	- Just remember what ReadAbl is about: readability!
- Did you notice there wasn't a symbol between the variables and the values?
	- In ReadAbl, you don't need it!
	- The `init` command already implies that you are defining the variable and assigning it the attached value.
	- All you need is a minimum of two spaces.
	- This leaves the equals sign operator to do its actual job: to compare!
---
- For the sake of brevity, all subsequent commands will be written in **Form 1**.
	- Notwithstanding this, feel free to use Form 2 wherever you see fit.
### II.C. Intro to Modes and Resignability
#### II.C.1. Modes
- Using the data types we saw earlier, we can initialize a variable in a specific mode, meaning it can only be resigned a value of the data type associated with that mode.
	- Ex. `int mode` means the value can only be resigned another integer
```
init :
{
    num         3   ; // No mode
    int num2    4   ; // int mode
    float num3  5.0 ; // float mode
}
```
- Do you notice how the unique ReadAbl spacing creates separate columns w/o any need for separators?
#### II.C.2. Resignability
- We can initialize a variable w/o the ability to be resigned.
	- This is similar to immutability in Python, except we can assign this property whenever, wherever.
	- `-r` means Not Resignable.
```
init :
{
    num4      5 ;
    -r num5   7 ; // Cannot be resigned
}
```
### II.D. Resigning a Variable
- To resign an initialized variable, use `resign`.
```
// Let's go through the `num` variables we initialized earlier.
resign :: 9 :
{
    num  ; // num = 9
    num2 ; // num2 = 9 (because it's in int mode)
    num3 ; // ERROR: Float mode
    num4 ; // num4 = 9
    num5 ; // ERROR: Not Resignable
}
```
### II.E. Modifying a Variable's Properties
- The `resign` command can only change a variable's value.
- So to change a variable's properties, e.g., mode, resignability, etc., we need a separate command: `prop`.
#### II.E.1. Modes
- With the condition word `mode`, we can change a variable's mode.
- To rid a variable of its current mode, put the condition word `rid` before `mode`.
```
prop :: rid mode :
{
    num3 ; // Removed float mode
}
```
- To add a mode to a variable, put the condition word `add` before `mode` and the data type after.
	- Variables can have multiple modes simultaneously!
```
prop :: add mode int :
{
    num3 ; // Added int mode
}

prop :: add mode float :
{
    num3 ; // Added float mode alongside int mode
}
```
#### II.E.2. Resignability
- Remember how `-r` means Not Resignable?
- Likewise, `+r` means Resignable.
```
prop :: +r :
{
    num5 ; // num5 is now Resignable!
}

prop :: -r :
{
    num5 ; // Back to Not Resignable.
}
```
#### II.E.3. Modifiability
- Taking the same logic as Resignability, you can use `-m` to make a variable Not Modifiable and `+m` to make it Modifiable.
```
prop :: -m :
{
    var1 ; // Not Modifiable
}

prop :: add mode int :
{
    var1 ; // ERROR: Not Modifiable
}

prop :: +m :
{
    var1 ; // Modifiable
}

prop :: add mode int :
{
    var1 ; // Added int mode
}
```
## III. Conditional Statements
- `if`, `elif`, and `else` work like Python.
	- `print` also works the same
```
if :: x = 5 : // The equals sign doing its intended purpose :)
{
    print :
    {
        "x is equal to 5" ;
    }
}

elif :: x = 7 :
{
    print :
    {
        "x is equal to 7"
    }
}

else :
{
    print :
    {
        "x is not equal to 5 or 7" ;
    }
}
```
### III.A. Conditional Operators
- Most conditional operators are the same as Python, but pay attention!

| Sign | Name                  |
| ---- | --------------------- |
| &    | Bitwise AND           |
| #    | Bitwise XOR\*         |
| \|   | Bitwise OR            |
| =    | Equals                |
| !=   | Does not equal        |
| <    | Less than             |
| <=   | Less than or equal to |
| >    | More than             |
| >=   | More than or equal to |
| NOT  | Boolean NOT           |
| AND  | Boolean AND           |
| OR   | Boolean OR            |
- \* I'm leaving the caret symbol `^` to represent exponentiation, again, having the proper symbol do its job.

# WORK IN PROGRESS...
- I will definitely split these main sections into their own files later.
