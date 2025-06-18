# III. Variables
- In ReadAbl, there are basically only two commands that you need to set up variables.
	1. `init`
		- Used to declare variables and assigns an initial value.
	2. `resign`
		- Used to reassign (hereinafter written "resign") a new value to a declared variable.
## III.i. SO MANY EQUALS SIGNS >:(
- **WARNING: RANT AHEAD!**
- While Python is quite readable even to beginners (disregarding OOP stuff like classes), there is one thing I see littered everywhere... ***EQUALS SIGNS!!!***
- EVERYWHERE you look in a Python program, you see `x = y`.
- Now, why do I hate this even as an avid Python programmer?
- Because in a large program (>1000 lines of code) it's hard to keep track of the age of variables.
	- Average line of thought:
		- Have I seen `variable_1` before?
		- Has `variable_1` been used yet?
		- Or did I just define it...?
- In ReadAbl, you **have to** distinguish between when you first define a variable and when you're just changing the value.
## III.A. Initialization
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
- Did you notice there wasn't a symbol between the variables and the values?
	- The `init` command already implies that you are defining the variable and assigning it the attached value.
### III.A.1. Empty Variables/Values
- Sometimes you just want to make a variable but don't care what value it's assigned at initialization.
	- Use the condition word `empty` and the data type of the variable to accomplish this.
```
init :: empty :
{
	int   var1 ; // var1 = 0
	float var2 ; // var2 = 0.0
	str   var3 ; // var3 = ""
	arr   var4 ; // var4 = arr ()
	list  var5 ; // var5 = list ()
	bool  var6 ; // var6 = False
}
```
### III.A.2. Sets
- You can specially rewrite the `init` command for sets.
```
// Variable condition
init :: list this_is_a_list :
{
    1 ;
    2 ;
    3 ;
}
// Values condition
init :: list ( 1 , 2 , 3 ) : // Commas separate values in sets
{
    this_is_a_list ;
}
```
- Personally, the first form looks more *readable*.
- Make sure to use the condition word `arr` or `list` before the variable name to define what type of set it is.
### III.A.3 Modes
- Using the data types we saw earlier, we can initialize a variable in a specific mode, meaning it can only be resigned a value of the data type associated with that mode.
	- `@m` means mode, so `int @m` means a variable is in `int` mode and can only be resigned `int`.
	- Even though ReadAbl is dynamically typed, we use `@m` to specify that the data types do not refer to the value of the variables but, in fact, the mode of the variable.
```
init :
{
    num            3 ; // No mode
    int @m num2    4 ; // int mode
    float @m num3  5 ; // Float mode
}
```
- The initial value of `num3` is an integer, but it can only be resigned floating-point numbers.
### III.A.4 Locking
- We can lock a property of a variable at initialization.
	- This is similar to immutability, except we can lock a *specific* property at any time.
	- Here's a few basic properties: `@m`, mode; `@r`, resignability; `@mod`, modifiability.
	- Simply put `lock` and a property before the variable to lock that property
```
init :
{
    num4          5 ;
    lock @r num5  7 ; // num5 cannot be resigned!
}
```
## III.B. Resign
- To resign an initialized variable, use `resign`.
```
resign :
{
    var1  9 ;
}
```
- When assigning one value to multiple variables, we can put the **value** as a condition and the **variables** as arguments.
- Let's go through the `num` variables we initialized earlier.
```
resign :: 9 :
{
    num  ; // num = 9
    num2 ; // num2 = 9 (because it's in int mode)
    num3 ; // ERROR: Float mode
    num4 ; // num4 = 9
    num5 ; // ERROR: Locked
}
```
### III.B.1. Sets
- You can actually flip the syntax for `resign` when sets are involved.
	- The **variable** is now the condition while the **values** are the arguments.
```
resign :: list lst1 : // Make sure to include that `list` condition word
{
    1 ;
    3 ;
    4 ;
}
```
- Just like with `init`, you can also write it like this.
```
resign :: list ( 1 , 3 , 4 ) :
{
    list_name ;
}
```
## III.C. Modify Properties
- The `resign` command can only change a variable's value.
- To *modify* a variable's properties, e.g., mode, we need a separate command: `mod`.
```
// `mod` syntax
mod :: @property variable : { argument }
```
### III.C.1. Modes
- With `@m`, we can change a variable's mode.
- Let's simply look at some example code.
```
mod :: @m num3 : { rid @c } // Removed current mode (float)
mod :: @m num3 : { add float } // Added float mode
mod :: @m num3 : { float -> int } // Change float mode to int mode
mod :: @m num3 : { add-on float } // num3 is now in int mode AND float mode
```
- Notice that we can use `@c` to call the current value for that property.
## III.D. Lock
- If we initialized a variable but wanted to lock a certain property later, we can use `lock`.
### III.D.1. Resignability
- Use the condition word `@r` for resignability.
```
init : { num5  7 }

lock :: @r : { num 5 } // Resignability locked

resign : { num5  5 } // ERROR: Resignability locked
```
### III.D.2. Modifiability
- Same deal, use `@mod` instead.
```
lock :: @mod : { var1 }

mod :: @m var1 : { add int } // ERROR: Modifiability locked
```