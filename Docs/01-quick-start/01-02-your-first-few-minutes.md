# Your First Few Minutes

- **Your time is precious**[^1], so let's quickly show you the ropes.

## "Hello World."

- Below is a simple program that prints "Hello World."

```qrtz
print("Hello World.")
```

- Simple, right?

## Variables

- Here's how to create a variable.

```qrtz
variable := 0
```

- Now, what about changing the value?

```qrtz
variable = 11
```

## Functions

- Let's make a function.

```qrtz
define functionName(parameter, parameter2)
    print(parameter)
    print(parameter2)
```

## Control Flow

- If x is equal to 5, change x to 2.

```qrtz
if x == 5
    x = 2
```

- Otherwise if x is equal to 7, change x to 5.

```qrtz
else if x == 7
    x = 5
```

- Otherwise, print "this!"

```qrtz
else
    print("this!")
```

- All together now!

```qrtz
x := 5

if x == 5
    x = 2
else if x == 7
    x = 5
else
    print("this!")
```

## Pipelines

- Instead of having ugly code like this...

```py
string = " HELLO WORLD. "
print(string.strip().lower())
```

- You can make it pretty!

```qrtz
string := " HELLO WORLD. "
string -> strip -> lower -> print
```

- Isn't that pretty[^2]?

## That's it

- Welp, those are the basic basics.
- If you're intrigued[^3], we recommend moving on to the rest of the documentation.

---

[^1]: Here at Quartz, we know you're a busy person with a packed schedule.
  So we made a *lightning fast* intro!
  If that's not your style... keep in mind, it's not ours either.
  Keep reading onward!
[^2]: You have to agree!
[^3]: We bet you're intrigued.
  Did you see those pipelines?! \\(OoO)/
