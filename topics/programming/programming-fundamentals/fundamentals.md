# Programming fundamentals — fundamentals

Every construct in every programming language exists to solve a problem created by the
previous one. This file derives them in order.

[← Programming fundamentals](README.md) · [Concepts](concepts.md) ·
[Practical](practical.md)

---

## Starting point

From [`computer-basics`](../../foundations/computer-basics/README.md): a machine
executes simple instructions in sequence on data.

That is enough to compute anything computable. It is also unusable for writing
anything, and the reason is worth stating precisely: instructions refer to data by its
*location*, so any change to the layout of your data invalidates every instruction that
touches it. Programming languages exist to remove that coupling, one construct at a
time.

Each section below is a problem, then the construct that answers it. That is the shape
of every good explanation in this repository, and it is worth noticing as a pattern
because you will use it when you have to explain things yourself.

---

## Problem 1: data needs names → variables and binding

Referring to "the number at location 4823" is unworkable. So you give data a name.

```python
count = 10
```

Here is where nearly every course goes wrong, and the error costs people months later.
The usual explanation:

> A variable is a box that holds a value.

**In most modern languages this is wrong**, and it causes three separate confusions
later. The accurate model:

> A variable is a **name bound to a value**. The name is a label; the value exists
> independently.

The difference is invisible with numbers and glaring with anything larger:

```python
a = [1, 2, 3]
b = a           # b is a second name for the SAME list
b.append(4)
print(a)        # [1, 2, 3, 4]  -- a "changed", though nothing touched a
```

If variables were boxes, `b = a` would copy the contents and `a` would be unchanged.
They are not boxes. `b = a` binds a second name to one list. This is called
**aliasing**, and it is the single most common source of baffling bugs at Level 1 and
2.

Compare:

```python
a = [1, 2, 3]
b = a
b = [9, 9]      # REBINDS b to a different list
print(a)        # [1, 2, 3]  -- unchanged
```

`b.append(4)` **mutates the value**. `b = [9, 9]` **rebinds the name**. Two completely
different operations that look similar. Once you see them as different, aliasing bugs
stop being mysterious.

Languages differ here, and the differences are informative rather than arbitrary. C
gives you the address explicitly, so the model is unavoidable. Rust tracks *ownership*
so the compiler rejects the aliasing bug at compile time. Functional languages mostly
forbid mutation, which makes the question disappear. Each is a different answer to the
problem you just met.

**Do the aliasing exercises in [exercises.md](exercises.md) until this is automatic.**
It is the highest-value ten minutes in the topic.

---

## Problem 2: data has kinds → values and types

`5 + 3` is 8. `"5" + "3"` might be `"53"`, or an error, or `8`, depending on the
language. So values have **types**: a set of possible values plus the operations allowed
on them.

The types you need now: integers, floating-point numbers, strings, booleans, and "no
value" (`None`, `null`, `nil`, `undefined` — every language spells it differently and
some have two, which is its own lesson).

### The floating-point surprise

```python
>>> 0.1 + 0.2
0.30000000000000004
```

This is not a bug in your code, in Python, or in your computer. It is the first time a
machine limitation will bite you, and understanding it now saves real pain.

Floats are stored in binary. In binary, `0.1` is a repeating fraction — exactly as `1/3`
is `0.3333...` in decimal. It has to be truncated, so `0.1` is stored as a value very
slightly off. Add two such values and the error is visible.

Consequences you must internalise now:

- **Never test floats for equality.** Compare with a tolerance:
  `abs(a - b) < 1e-9`.
- **Never use floats for money.** `0.10 + 0.20 != 0.30` is a rounding error in a
  ledger. Use integer cents, or a decimal type designed for this.
- Order of operations changes the result: `(a + b) + c` can differ from `a + (b + c)`.

Read the first two sections of Goldberg's paper (in [resources.md](resources.md)) *now*,
while you are surprised. The rest is for later.

### Static and dynamic typing

Does the language check types before running, or while running?

|  | Checked at | Consequence |
|---|---|---|
| **Static** (C, Java, Rust, Go, TypeScript) | Compile time | Whole error classes are impossible; more up-front writing |
| **Dynamic** (Python, JavaScript, Ruby) | Run time | Faster to write; type errors appear when the code runs, possibly in production |

Neither is correct in general and the argument is not worth your attention yet. Note
that the industry trend is toward adding optional static checking to dynamic languages —
Python type hints, TypeScript — which tells you something about where the value lies as
programs get large. `type-systems` at Level 2 does this properly.

---

## Problem 3: decisions → conditions

A program that always does the same thing is a fixed calculation. You need to branch on
the data.

```python
if temperature > 30:
    print("hot")
elif temperature > 15:
    print("mild")
else:
    print("cold")
```

Two things worth attention.

**Short-circuit evaluation.** In `a and b`, if `a` is false, `b` is never evaluated.
This is not an optimisation detail — it is load-bearing:

```python
if user is not None and user.name == "admin":   # safe
if user.name == "admin" and user is not None:   # crashes when user is None
```

The order matters because the second condition is only reached when the first is true.

**Truthiness.** Many languages treat non-boolean values as true or false in a
condition. `if items:` means "if the list is non-empty". Convenient, and the source of a
real bug class: `0`, `""`, and `[]` are all falsy, so `if count:` is false when
`count == 0`, which is usually not what you meant. Know your language's rules exactly.

---

## Problem 4: repetition → loops

Writing an instruction a thousand times is not viable.

```python
for item in items:      # iterate over a collection -- prefer this
    process(item)

while not done:          # repeat until a condition changes
    done = step()
```

Prefer iterating over a collection to counting an index. `for i in range(len(items))`
followed by `items[i]` is how off-by-one errors happen, and it is noisier to read.

**Off-by-one errors** are the characteristic Level 1 bug, and they come from ranges
being half-open in most languages: `range(0, 5)` gives `0,1,2,3,4` — five values, not
including 5. This convention is deliberate (it makes `range(a, b)` have `b - a`
elements, and adjacent ranges join without overlap) but it must be learned explicitly.

**Loop invariants** are the tool for getting loops right without running them. Ask:
*what is true at the start of every iteration?* For a running sum: "`total` holds the
sum of every item seen so far." If that is true before the loop and each iteration
preserves it, the result is correct by construction. Stating the invariant catches more
bugs than testing does, and it is a technique that keeps paying off through
`algorithms` and beyond.

---

## Problem 5: naming and reuse → functions

A group of instructions you use in several places, or that deserves a name, becomes a
function.

```python
def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32
```

Functions do three things at once, and the third is the one that matters most:

1. **Reuse** — write once, call many times.
2. **Naming** — `celsius_to_fahrenheit(x)` says what it does; the arithmetic does not.
3. **Isolation** — a function's local names are its own. You can reason about it
   without reading the rest of the program. This is the property that makes large
   programs possible at all.

### The habit that separates good from bad code

**A function should do one thing you can name.**

If naming it requires "and", it is two functions.

```python
def process_and_save_and_email(data):     # three functions
```

The specific version worth internalising now: **separate computing from doing.**

```python
def average(numbers):                      # computes. Testable in one line.
    return sum(numbers) / len(numbers)

print(f"Average: {average(scores)}")       # does. Not mixed in.
```

Compare:

```python
def print_average(numbers):                # computes AND prints
    print(f"Average: {sum(numbers) / len(numbers)}")
```

The second cannot be tested without capturing output, cannot be reused when you need
the value for something else, and cannot be called from code that has no console. This
single habit — pure computation separated from input and output — is why some codebases
are testable and others are not, and it is worth adopting before you have any reason to
care about testing.

### Scope

Names defined inside a function are invisible outside it. This is what makes isolation
work.

Reading a global variable from inside a function usually works and is usually a
mistake: it makes the function's behaviour depend on invisible state, so it can no
longer be understood or tested alone. Pass what you need as parameters.

---

## Problem 6: many values → collections

You rarely know how many things there will be when you write the code.

| Collection | Ordered? | Lookup by | Use when |
|---|---|---|---|
| **List / array** | yes | position | Order matters, or you will iterate over everything |
| **Dictionary / map** | no (or insertion order) | key | You look things up by a name or ID |
| **Set** | no | membership only | You need uniqueness or "is this in it?" |
| **Tuple** | yes | position | A fixed-size group that belongs together, unchanging |

The one cost you must know now:

```python
if name in big_list:      # scans -- checks every item until found
if name in big_set:       # hashes -- roughly one step, regardless of size
```

At 100 items, indistinguishable. At 100,000 in a loop, the difference is between
instant and unusable. You will measure exactly this in the benchmark gate, and the
formal treatment is [`data-structures`](../../computer-science/data-structures/README.md)
at Level 2.

Do not skip the measurement. "A set lookup is faster" is a fact you can recite; the
*shape* of the curve as input grows is a model you can use.

---

## Problem 7: things go wrong → errors

Opening a file can fail. Parsing input can fail. The network can fail. Failure is not
exceptional; it is the common case in any program that touches the outside world.

```python
try:
    with open(path) as f:
        data = f.read()
except FileNotFoundError:
    print(f"error: {path} does not exist")
```

Three rules that will save you more time than any other advice at this level:

**Fail loudly.** A program that silently continues after an error produces wrong
answers, which is worse than crashing. A crash tells you where and when.

**Catch specific errors.** `except Exception:` catches your own bugs too — typos,
`None` dereferences, logic errors — and hides them behind a generic message. You then
debug a program that refuses to tell you what is wrong.

**Never swallow silently.** `except: pass` is the most expensive two words in software.
It converts a findable bug into permanently mysterious behaviour.

`error-handling` at Level 1 covers the design questions: where to handle, where to
propagate, and errors as return values versus exceptions.

---

## Problem 8: programs outgrow one file → modules

At a few hundred lines, one file stops working: you cannot find anything, names
collide, and you cannot reuse a piece without dragging everything.

Modules split code across files and give each file its own namespace, so two files can
both define `parse` without conflict.

Organise by **what things are about**, not by what kind of thing they are. `orders.py`
containing everything about orders beats splitting the same logic across `models.py`,
`helpers.py`, and `utils.py`. A file called `utils.py` is where code goes when nobody
decided where it belongs, and it grows forever.

---

## Problem 9: some problems nest → recursion

A function can call itself.

```python
def countdown(n):
    if n <= 0:          # base case -- without this it never stops
        return
    print(n)
    countdown(n - 1)
```

The base case is not optional. Without it you exhaust the call stack, which is a
finite resource — you will do this on purpose in the
[calculator project](../../../projects/cli-calculator/README.md) and it is a useful
thing to have seen.

Use recursion when the problem is genuinely nested: a directory containing
directories, an expression containing expressions, a tree. Forcing recursion onto a
flat loop is a common way to make simple code hard to read.

---

## Choosing a first language

You need one. Which one matters less than finishing.

The three defensible starting points, and what each choice actually costs:

**Python.** Fastest path from idea to working program, and the concepts in this file
appear with the least syntactic noise. The cost is real: it hides memory, types, and
concurrency so thoroughly that you can be productive for years without a model of any
of them. That is fine *if* you learn them deliberately later, in
`memory-management` and `concurrency-and-parallelism`. If you do not, they become
permanent blind spots.

**JavaScript.** Your work runs in a browser and is immediately visible, which is
genuinely motivating. The cost is noise: historical inconsistencies (`==` versus `===`,
`this` binding, `NaN`), and a toolchain that changes fast enough to be a distraction
while you are learning to think. Both are survivable; neither helps you today.

**C.** You will understand the machine, because C makes you manage memory yourself and
nothing is hidden. The cost is time: real hours spent on pointers and manual allocation
before you write anything interesting. Choose it if that trade appeals or if you are
aimed at systems or embedded work — not out of a belief that harder is better.

**For most people: Python first.** Then a second language chosen to be *different*,
because that is where you discover which of your knowledge was the language and which
was programming.

One honest warning: switching languages when a topic gets hard is
[technology hopping](../../../docs/philosophy.md#technology-hopping), and it feels
identical from the inside to making a good choice. The test is whether you are
switching *before* or *after* the difficulty. Finish both projects in one language
first.

---

## Putting it together

```text
A machine executes instructions on data, referring to it by location.
                          ↓
Data needs names, or layout changes break everything.        → variables, binding
Data has kinds with different operations.                    → types
Behaviour must depend on data.                               → conditions
Repetition must not be written out.                          → loops
Instruction groups need names, parameters, isolation.        → functions
Quantities are unknown when writing the code.                → collections
Two names can share one value.                               → mutability, aliasing
Anything touching the world can fail.                        → errors
Programs outgrow one file and one author.                    → modules
Some problems nest arbitrarily.                              → recursion
                          ↓
Every language is a set of choices about which of these
to make easy, safe, or explicit.
```

That last line is the point of the whole file. When you meet your second language, you
will not be learning new concepts — you will be learning which choices its designers
made, and why. That is a week of work rather than a year.

---

## Next

[concepts.md](concepts.md) for depth per concept, then
[practical.md](practical.md) for the environment and the habits.
