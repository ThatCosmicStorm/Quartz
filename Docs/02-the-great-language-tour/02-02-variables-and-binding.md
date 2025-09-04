# Variables and Binding

- Declaring a variable is done with `:=`.

```qrtz
new_var := 5
```

- To reassign a value to a declared variable, use `=`.

```qrtz
new_var = 3
```

## Constants

- A constant is declared the same as a variable, but it has distinctive ALL CAPS.

```qrtz
NEW_CONST := 5
```

### Mutability

- Variables are mutable, i.e., they *can* be changed after declaration.
- Constants are immutable, i.e., they *cannot* be changed.

```qrtz
new_var := 5
NEW_CONST := 5

new_var = 3
NEW_CONST = 2  # ERROR
```

- Although variables are mutable, it is good practice to declare new variables instead of changing the old one over and over again.

### Usage

- For constants, there are two use cases:
  1. You want a variable that *never changes under any circumstance*
  2. You want to represent an actual constant, e.g., Pi, Euler's constant, etc.

## Aliasing vs. Cloning

### Cloning

- When you write a statement like this:

```qrtz
old_var := 4

new_var := old_var
```

- The default behavior is cloning[^1].
- `new_var` is now a *separate* **copy** of `old_var`
- Anything that happens to `old_var` doesn't affect `new_var`

### Aliasing

- But what if you did want both variables to change?
- Then you would want to make `new_var` an alias of `old_var` like so:

```qrtz
old_var := 4

alias new_var := old_var
```

- Now, if `old_var` is assigned a new value, `new_var` is also assigned that same value, and *vice versa*.

## Type Hints

- If you want to make sure a variable only gets a certain type of data, use type hints.

```qrtz
number: int := 0

number = "i am a string"  # ERROR
```

### Clarification

- Type hints can also be used in contexts where the data type is not immediately obvious.

```qrtz
result: int = function()

# Unnecessary
other_var: int = 0
```

- In cases like `other_var`, it's very obvious what data type its holding.

---

[^1]: Personally, this should be the default behavior in all languages.
  But, alas, we don't live in a perfect world.
