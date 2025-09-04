# Variables

- Declaring a variable is done with `:=`.

```qrtz
new_var := 5
```

- To reassign a value to a declared variable, use `=`.

```qrtz
new_var = 3
```

## Declaration Rules

- Variables are mutable, i.e., they *can* be changed after declaration.
- Constants are immutable, i.e., they *cannot* be changed.

```qrtz
NEW_CONST := 5

NEW_CONST = 2  # ERROR
```

- A constant is declared the same as a variable, but you use **ALL CAPS** instead.

## Scope

- Scope is entirely determined by the *level* of indentation[^1].

```qrtz
define function()
    # inside the scope of the function
# outside
```

- Let's go deeper.

```qrtz
define function()
    # inside function scope

    if cond
        # inside if statement

    # outside if but inside function

# outside both
```

## Aliasing vs. Cloning

### Cloning

- When you write a statement like this:

```qrtz
old_var := 4

new_var := old_var
```

- The default behavior is cloning.
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

## WORK IN PROGRESS

---

[^1]: Here at Quartz, we are a *complete* advocate of the off-side rule.
