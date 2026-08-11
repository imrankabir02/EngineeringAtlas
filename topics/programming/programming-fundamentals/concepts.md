# Programming fundamentals — concepts

Fifteen concepts, each with a required depth. This file answers *how deeply should I
learn it?*

[← Programming fundamentals](README.md) · [Fundamentals](fundamentals.md) ·
[Practical](practical.md)

---

## Depth vocabulary

| Depth | Means | Test |
|---|---|---|
| `aware` | You know it exists and roughly what it does | You would not be surprised by the term, and you know when to go read about it |
| `working` | You can use it correctly and explain the trade-off without notes | You can apply it to a new problem |
| `deep` | You understand the mechanism well enough to debug it and predict failures | You can explain *how* it works and where it breaks |

Six concepts here are `deep`, six `working`, three `aware`. **The `aware` markings are
the useful ones** — they tell you what to leave alone, and leaving things alone is how
you finish this topic in months rather than years.

---

## The inventory

| Concept | Depth | The one thing to take from it |
|---|---|---|
| [Values and types](#values-and-types) | **deep** | A type is a set of values plus allowed operations. Floats are not decimals |
| [Variables and binding](#variables-and-binding) | **deep** | A variable is a name bound to a value, not a box |
| [Conditions and loops](#conditions-and-loops) | **deep** | Short-circuiting, half-open ranges, loop invariants |
| [Functions](#functions) | **deep** | One thing you can name. Separate computing from doing |
| [Collections](#collections) | **deep** | Which structure for which access pattern, and what a scan costs |
| [Mutability and aliasing](#mutability-and-aliasing) | **deep** | Two names, one value. Mutation vs. rebinding |
| [Errors and failure](#errors-and-failure) | working | Fail loudly, catch specifically, never swallow |
| [Debugging](#debugging) | working | Hypothesis, then evidence. Bisect. Use a debugger |
| [Modules and namespaces](#modules-and-namespaces) | working | Organise by subject, not by kind of thing |
| [Strings and text](#strings-and-text) | working | "Length" is ambiguous: bytes, code points, characters |
| [Input, output, files](#input-output-and-files) | working | I/O is where the world stops cooperating |
| [Recursion](#recursion) | working | Base case first. The stack is finite |
| [Cost intuition](#cost-intuition) | aware | Notice nested loops over the same data. No formal notation yet |
| [How memory is managed](#how-the-language-manages-memory) | aware | Something handles it. Stop there |
| [That concurrency exists](#that-concurrency-exists) | aware | Know the word. Do not start |

---

## Values and types

**Depth: deep.**

A type is the set of values something can be, plus the operations allowed on them.

What `deep` requires — you can:

- name your language's basic types and say which operations each supports
- predict what integer division does versus float division, in your language
- explain why `0.1 + 0.2 != 0.3`, from the binary representation
- state what to use for money instead of floats, and why
- explain the difference between static and dynamic typing and what each catches
- say what your language's "no value" is, and what happens when you operate on it

**Test yourself:** what does `7 / 2` give in your language? What about `7 // 2` or
`(int) (7 / 2)`? If you have to run it to find out, run it — then remember, because
this is a real bug source in code that computes indices or page counts.

---

## Variables and binding

**Depth: deep.** The highest-value concept in the topic.

A variable is a **name bound to a value.** Not a box containing one.

What `deep` requires — you can:

- predict the output of any aliasing example without running it
- distinguish **mutation** (`b.append(4)` — changes the value) from **rebinding**
  (`b = [9]` — points the name elsewhere)
- explain what happens when you pass a mutable object to a function that changes it
- explain why the "box" model gives wrong predictions, and where
- say what your language's assignment operator actually does

**Test yourself:**

```python
def add_item(items):
    items.append("new")

my_list = ["a"]
add_item(my_list)
print(my_list)        # what prints, and why?
```

If you predicted `["a", "new"]` and can explain *why* in terms of names and values, you
have it. If you expected `["a"]`, reread
[fundamentals.md](fundamentals.md#problem-1-data-needs-names--variables-and-binding)
and do the aliasing drills — this exact confusion causes bugs at Level 2 and 3 that are
very hard to find, because the code that breaks is not the code that caused it.

Use [Python Tutor](https://pythontutor.com/) for ten confusing lines. Seeing the arrows
fixes the model faster than any explanation.

---

## Conditions and loops

**Depth: deep.**

What `deep` requires — you can:

- trace a nested loop on paper and get the right answer without running it
- explain short-circuit evaluation and write a null check that depends on it
- state your language's truthiness rules exactly, including whether `0` and `""` are
  falsy
- explain why ranges are half-open, and use that to avoid off-by-one errors
- state a loop invariant for a loop you wrote

**Test yourself:** how many times does the body run?

```python
for i in range(1, 10, 2):
    for j in range(i):
        body()
```

Work it out on paper. Then check. Being able to do this is the difference between
reasoning about code and running it to see.

---

## Functions

**Depth: deep.**

What `deep` requires — you can:

- explain the three jobs of a function: reuse, naming, isolation
- take a function that does two things and split it, and say why the split helps
- explain why a function that computes *and* prints is harder to test than one that
  only computes
- explain scope, and why reading a global from inside a function is usually a mistake
- pass a function as an argument to another function, and say when that is useful

**Test yourself:** find a function in your own code that needs "and" to describe. Split
it. Notice that the parts are individually testable and one of them is reusable — that
is not a coincidence, it is the whole argument.

---

## Collections

**Depth: deep** — the *choosing*, not the internals.

What `deep` requires — you can:

- choose between list, dict, set, and tuple for a stated access pattern, and defend it
- explain why `x in some_set` is fast and `x in some_list` is not
- convert between them and know what is lost each way (a set loses order and duplicates)
- pick the right one for "count occurrences of each word in a document" without
  hesitating
- explain when a list of tuples beats a dict, and vice versa

**Not required yet:** how a hash table works internally, hash collisions, load factors,
tree structures. That is
[`data-structures`](../../computer-science/data-structures/README.md) at Level 2, and it
is much more rewarding once you have felt the need for it.

**Test yourself:** you have a million records and must check membership repeatedly.
Which structure, and what is the difference at that scale? You will measure this in the
benchmark gate.

---

## Mutability and aliasing

**Depth: deep.** The bug factory.

What `deep` requires — you can:

- predict whether an operation mutates in place or returns a new value, in your language
- copy a collection deliberately, and explain shallow versus deep copy
- explain the default-mutable-argument trap if your language has one (Python's
  `def f(items=[])` is the classic; the default is created once, at definition time, and
  shared across every call)
- explain why immutability makes code easier to reason about
- demonstrate an aliasing bug to someone else on purpose

**Test yourself:**

```python
def append_to(item, target=[]):
    target.append(item)
    return target

print(append_to(1))      # [1]
print(append_to(2))      # [1, 2]  -- surprised?
```

If that surprises you, you have found something important. The default list is created
once when the function is defined, not per call, so every call shares it.

---

## Errors and failure

**Depth: working.**

- raise, catch, and let errors propagate
- catch **specific** exception types, never a bare catch-all
- write an error message that names what failed and where
- know that `except: pass` converts a findable bug into permanent mystery
- use your language's cleanup mechanism (`with`, `defer`, `finally`) so resources are
  released even on failure

**Deferred:** designing an error taxonomy, errors as return values versus exceptions,
retries and backoff. `error-handling` (Level 1) and later
`distributed-systems-fundamentals` handle those.

---

## Debugging

**Depth: working.** Deepened deliberately in `debugging-fundamentals`.

- read a stack trace and identify the failing line, the immediate cause, and the first
  frame you wrote
- form a hypothesis *before* changing anything, and find the cheapest observation that
  would disprove it
- bisect: comment out half, or `git bisect`, or halve the input
- use a real debugger — breakpoints, stepping, inspecting variables — not only print
  statements

Print statements are legitimate and often fastest. But if you have never used a
debugger, you are choosing print by default rather than on merit, and there are bugs
print cannot practically find.

**Test yourself:** take a program you wrote a week ago, break it deliberately in a
subtle way, and find it with a debugger. That is a gate in [`topic.yml`](topic.yml).

---

## Modules and namespaces

**Depth: working.**

- split a program across files and import between them
- explain what a namespace prevents
- organise by subject (`orders.py`) not by kind (`helpers.py`)
- know why `utils.py` grows forever: it is where code goes when nobody decided

**Deferred:** packaging, dependency resolution, circular imports at scale, public
interfaces. `package-management` at Level 2.

---

## Strings and text

**Depth: working.**

- index, slice, split, join, and format strings
- know that strings are usually immutable, so "modifying" one creates a new one — which
  is why building a string in a loop with `+=` is quadratic
- know that **"length" is ambiguous**: bytes, code points, and user-perceived characters
  are three different counts, and an emoji can be one character, several code points,
  and many bytes
- read a file with an explicit encoding rather than the platform default

**Test yourself:** what is the length of a string containing one emoji, in your
language? Try a family emoji. The answer is surprising and it is the reason text bugs
are so persistent.

---

## Input, output, and files

**Depth: working.**

- read command-line arguments, standard input, and standard output
- read and write files, closing them reliably even on error
- distinguish text mode from binary mode, and specify the encoding
- handle the file not existing, not being readable, and being a directory
- know that I/O is slow relative to computation — from
  [`computer-basics`](../../foundations/computer-basics/README.md), roughly a thousand
  times

I/O is where your program meets a world that does not cooperate. Every function that
does I/O needs an error path, and that is not pessimism — it is the common case.

---

## Recursion

**Depth: working.**

- write a recursive function with a correct base case
- trace a small recursion by hand
- recognise naturally recursive problems: trees, nested structures, expressions
- know the call stack is finite and what exhausting it looks like
- convert simple recursion to iteration, and say why you might want to

**Deferred:** tail-call optimisation, memoisation as a technique, dynamic programming.
`algorithms` and `advanced-algorithms` at Levels 2–3.

---

## Cost intuition

**Depth: aware.** Deliberately capped.

Notice when work grows faster than input. A loop inside a loop over the same data
touches every pair, so doubling the input quadruples the work. Searching a list gets
slower as the list grows; a dict lookup does not.

That is all you need. **No formal notation yet.**

`complexity-analysis` at Level 2 does Big-O properly, and doing it now means learning
notation with no experience to attach it to. The benchmark gate in this topic gives you
the experience; the notation will then describe something you have seen.

---

## How the language manages memory

**Depth: aware.** Deliberately capped.

Something manages memory for you. Objects live somewhere and are cleaned up when
nothing refers to them.

That is the whole assignment at Level 1.

**Not now:** reference counting, garbage collection algorithms, generational collection,
stack versus heap allocation, ownership and borrowing. `memory-management` at Level 3
covers these with the prerequisites that make them stick.

If you are working in C, you cannot avoid manual memory management and will learn
`malloc`/`free` as part of the language. That is fine, and it is one of the reasons C
takes longer.

---

## That concurrency exists

**Depth: aware.** Deliberately capped, and the cap matters.

Programs can do more than one thing at a time. This introduces problems your sequential
reasoning does not cover: two things changing the same data, ordering you cannot rely
on, and bugs that appear only sometimes.

Know the word exists. **Do not start here.**

`concurrency-and-parallelism` is Level 3 and requires `operating-systems-fundamentals`,
for a good reason: concurrency bugs are nearly impossible to reason about without a
model of threads, scheduling, and memory. Attempting it now produces code that works by
luck, and the habit of believing it works because the test passed once.

If you are writing JavaScript you will meet `async`/`await` early because the language
forces it on you. Learn the mechanics you need — that a promise represents a future
value and `await` waits for it — and treat the rest as deferred. That is `async-programming`
at Level 3.

---

## Using this file

Before starting a study session, look at the depth marking for what you are about to
read. If it is `aware`, give it twenty minutes and move on. If it is `deep`, expect to
spend hours and come back to it more than once.

The failure mode this file exists to prevent: spending two weeks reading about garbage
collection (`aware`) while still unable to predict what an aliased list does (`deep`).
That happens constantly, it feels like diligence, and it leaves you unable to write the
programs the topic is for.

---

## Next

[practical.md](practical.md) — environment, tooling, reading errors, and the habits
that determine your pace.
