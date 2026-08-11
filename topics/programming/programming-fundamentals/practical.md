# Programming fundamentals — practical

Environment, tooling, reading errors, and the working habits that determine how fast
you progress. Examples are in Python; the ideas are not.

[← Programming fundamentals](README.md) · [Fundamentals](fundamentals.md) ·
[Concepts](concepts.md) · [Exercises](exercises.md)

---

## Setting up

Keep this minimal. Elaborate tooling is a way to feel productive without programming,
and you can add tools later when you feel their absence.

**What you need:** the language runtime, a text editor, and a terminal.

**What you do not need yet:** linters with 200 rules, formatters in a pre-commit hook, a
type checker, virtual-environment managers with lockfiles, containers, or an IDE whose
features you cannot name. Each of these is genuinely useful and each one is a thing that
can break while you are trying to learn something else.

```console
$ python3 --version
Python 3.12.3
```

Editor: VS Code or any editor you already have. Turn on syntax highlighting and
whatever inline error display it offers. Learn two things and stop: **jump to
definition**, and **run the file**.

### Verify you can run code three ways

```console
$ python3 hello.py                  # run a file
$ python3 -c "print(2+2)"           # run an expression
$ python3                           # interactive prompt (REPL); Ctrl-D to exit
>>> 2 + 2
4
```

The REPL is the most underused tool at this level. When you are unsure what an operation
does, do not reason about it and do not search for it — try it. Ten seconds in a REPL
beats five minutes of guessing, and it builds a habit of checking rather than assuming.

---

## Reading errors

The single most valuable practical skill in this topic. A beginner sees a wall of red
and panics; a competent programmer reads three lines and knows where to look.

```text
Traceback (most recent call last):
  File "/home/alice/organizer.py", line 42, in <module>
    main()
  File "/home/alice/organizer.py", line 31, in main
    move_files(plan)
  File "/home/alice/organizer.py", line 18, in move_files
    shutil.move(src, dst)
FileNotFoundError: [Errno 2] No such file or directory: 'documents/'
```

Read it in this order:

1. **The last line.** The error *type* (`FileNotFoundError`) and the *message*
   (`No such file or directory: 'documents/'`). This is what went wrong.
2. **The bottom of the stack.** `line 18, in move_files` — where it went wrong.
3. **Upwards through the stack**, to find **the first frame you wrote**. If the bottom
   frames are inside a library, the bug is almost always in the last line of *your* code
   that called into it — in this example, line 18.

The stack reads top-down as the call chain: `main()` called `move_files(plan)` which
called `shutil.move(...)`. Some languages print it in the opposite order; check which
yours does once and remember.

**Do not skip to searching the internet.** Read the message first. `FileNotFoundError:
'documents/'` means the destination directory does not exist — you can fix that without
help, and doing so builds the skill. Searching first trains you to outsource
comprehension, and the wall you hit at Level 2 is made of problems nobody has posted
about.

Error messages you will misread at first, and what they mean:

| Message pattern | Usually means |
|---|---|
| `NoneType has no attribute X` | Something returned nothing where you expected a value. Find what |
| `list index out of range` | An off-by-one, or an empty collection you assumed was non-empty |
| `KeyError: 'x'` | The key is genuinely absent. Check spelling, then check where it should have been set |
| `TypeError: unsupported operand` | You mixed types, often a string that should be a number |
| `IndentationError` / `SyntaxError` | The error is often on the line *before* the one reported |
| `RecursionError` / stack overflow | Missing or unreachable base case |

---

## Using a debugger

If you have only ever used print statements, learn this now. It takes twenty minutes and
it changes what bugs you can find.

```python
import pdb; pdb.set_trace()      # execution stops here, drops to a prompt
```

Or in modern Python, just `breakpoint()`.

At the prompt: `n` for the next line, `s` to step into a call, `c` to continue, `p x` to
print a variable, `l` to see where you are, `q` to quit.

Your editor almost certainly does this graphically: click a line number to set a
breakpoint, press the run-with-debugger key, and step through while watching variables
change. Learn your editor's version once.

**When a debugger beats print statements:** when you do not know *where* the problem is,
when the state is large and you want to poke at it, when you want to inspect the call
stack, and when the bug is in code you did not write.

**When print beats a debugger:** when you already know where to look, when the problem
is timing-dependent, when you need a history of many iterations rather than one moment.

Both are legitimate. What is not legitimate is only knowing one, because then you are
choosing by default instead of by fit.

---

## Working habits that make the difference

These matter more than any tool. They are the actual difference between people who
progress at this level and people who stall.

### Predict before you run

Before pressing run, say what you expect to happen. Out loud is better.

When you are right, you confirmed your model. When you are wrong, you found a gap
immediately, at the cheapest possible moment — instead of ten minutes later when three
more things have changed.

This is the same habit as the prediction discipline in
[`computer-basics`](../../foundations/computer-basics/README.md), and it is the same one
that appears at Level 5 as
[experiment design](../../../docs/competency-gates.md#7-benchmark). It scales.

### Change one thing at a time

When something is broken, change exactly one thing, then run. If you change three things
and it works, you do not know why, and you have learned nothing.

This is genuinely hard to follow when frustrated, which is exactly when it matters most.

### Trace on paper

For any loop or recursion you do not understand, write out the variables and their
values for each iteration, by hand, on paper.

It feels slow and it is faster than the alternative, because it works on the *cause* of
your confusion rather than its symptoms. It also builds the ability to read code and
know what it does, which is what you will spend most of your career doing.

### Write the smallest failing case

A bug in a 200-line program is hard to find. The same bug in five lines is obvious.

Cut everything not needed to reproduce it. Half the time the bug becomes clear during
the cutting. This is bisection applied to code, and it is the same technique as
`git bisect` and binary search — one idea, many applications.

### Name things properly, from the start

`d`, `temp`, `data`, `x2`, `thing` — these are how a program becomes unreadable, and it
happens within days rather than months. `days_remaining` costs three seconds to type and
saves you rereading the logic to remember what `d` was.

You are the main beneficiary. Code you wrote three weeks ago is code written by a
stranger.

### Delete and rewrite

When a piece of code is confusing, delete it and write it again from what you know now.

This feels wasteful and is usually faster than untangling it, and the second version is
almost always better because you understand the problem now in a way you did not when
you started. Getting comfortable with deleting your own code is a durable professional
advantage.

---

## Testing, minimally

You do not need a testing framework yet. You do need to stop verifying by hand.

```python
def test_average():
    assert average([1, 2, 3]) == 2
    assert average([5]) == 5
    assert average([-1, 1]) == 0
```

Run it. If nothing prints, it passed.

The value is not correctness proof. It is that **you can now change the code without
re-testing everything by hand.** That is the thing that makes a program you can keep
working on, and you will feel the difference in the second project.

Write assertions for the cases you keep checking manually. When there are more than a
dozen, look at your language's test runner (`pytest`, `jest`, `go test`).
`testing-fundamentals` at Level 2 covers what makes a test *valuable*, which is a
different and harder question.

---

## Version control, minimally

Learn four commands now; the real topic is `version-control-git`.

```console
$ git init
$ git add .
$ git commit -m "working calculator with precedence"
$ git log --oneline
```

Commit whenever something works. That is the whole discipline at this stage.

The immediate payoff: you can experiment freely, because you can always get back to the
last working state. Programmers without version control edit timidly, and timid editing
is slow.

---

## Language-specific notes

Applies to the language you chose. Read only yours.

### Python

- Indentation is syntax. Configure your editor for 4 spaces and never mix tabs.
- `f"{name}"` strings for formatting. Avoid `%` and `.format()` in new code.
- Use `with open(...) as f:` so files close even when something raises.
- **The default-mutable-argument trap** is real: `def f(items=[])` creates one list at
  definition time, shared by every call. See
  [concepts.md](concepts.md#mutability-and-aliasing).
- `list.sort()` sorts in place and returns `None`; `sorted(list)` returns a new list.
  This pattern — mutating methods return `None` — is consistent and worth knowing.
- Read the tutorial ([resources.md](resources.md)). It is short, official, and correct.

### JavaScript

- Use `const` by default, `let` when you must reassign, and never `var`.
- Use `===`, never `==`. The coercion rules of `==` are a documented mistake.
- `NaN !== NaN`. Use `Number.isNaN()`.
- Array methods (`map`, `filter`, `reduce`) are the idiom. Learn them properly; they are
  how the language expects you to iterate.
- `async`/`await` will appear early because the language forces it on you. Learn the
  mechanics you need and treat the rest as deferred to Level 3 — see
  [concepts.md](concepts.md#that-concurrency-exists).
- Run in Node for this topic. Browser work belongs to `dom-and-browser`, later.

### C

- Compile with warnings on and treat them as errors:
  `gcc -Wall -Wextra -Werror -g`.
- Use `-g` and learn `gdb` early. In C, a wrong pointer corrupts memory silently and the
  crash appears somewhere unrelated — a debugger is not optional.
- Every `malloc` needs a matching `free`. Run under `valgrind` from the first program;
  finding leaks later is much harder.
- Arrays do not know their own length. Passing the length alongside is not
  boilerplate — it is the interface.
- Strings are null-terminated byte arrays. `strlen` walks the whole string every call, so
  `strlen` inside a loop condition is a quadratic bug that looks innocent.

---

## When you are stuck

In order. Do not skip steps — the order is what builds capability.

1. **Read the error message.** Properly, all of it, including the file and line.
2. **Print or inspect the state** just before the failure. Is it what you assumed?
3. **Reduce to the smallest failing case.**
4. **Write down what you believe is happening,** then find the cheapest observation that
   would disprove it.
5. **Check the official documentation** for the function involved. Not a tutorial — the
   documentation.
6. **Explain the problem out loud,** to a person or to nobody. This solves a
   surprising share of bugs, because articulating a problem requires you to state
   assumptions, and one of them is wrong.
7. **Then search.** Include the error type, not your whole message with your paths in it.
8. **Then ask,** with a minimal reproduction, what you expected, what happened, and what
   you already tried. Asking well is a skill and it is being assessed for the rest of
   your career.

Fifteen minutes stuck is normal and productive. Two hours stuck on the same thing means
step 3 was skipped.

---

## Next

[exercises.md](exercises.md) — 30 graded drills, then
[projects.md](projects.md).
