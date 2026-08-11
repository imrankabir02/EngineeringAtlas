# Expression calculator

**Level 1** · validates
[`programming-fundamentals`](../../topics/programming/programming-fundamentals/README.md)
· any language

Build a command-line program that evaluates arithmetic expressions:

```console
$ calc "2 + 3 * 4"
14
$ calc "(2 + 3) * 4"
20
$ calc "2 + "
error: unexpected end of input at position 4
```

**The constraint that makes this a project rather than an exercise: no `eval`.**
No `exec`, no `Function()`, no expression-evaluator library. You will write the
tokeniser and the parser yourself.

---

## Why this project exists

A calculator sounds trivial and is not. `2 + 3 * 4` is where it stops being
trivial, because getting `14` rather than `20` requires you to represent the
*structure* of the expression, not just scan it left to right.

That single requirement forces you to use, together and for real:

- **Decomposition** — a string becomes tokens, tokens become structure, structure
  becomes a number. Three stages with clean interfaces.
- **Recursion** — parentheses nest arbitrarily. Loops handle this badly; recursion
  handles it naturally, and you will understand why after you try both.
- **Error handling as design** — most inputs a user types are wrong. Errors are
  the main path, not an afterthought.
- **Testing** — precedence bugs are invisible until you write the case that catches
  them.

You will also, without being told, have implemented the front half of an
interpreter. That connection is worth noticing.

---

## Stage 1 — Tokenise

Turn `"12 + 3.5"` into a list:

```text
[NUMBER 12] [PLUS] [NUMBER 3.5]
```

A tokeniser walks the string once, deciding what each character starts. Digits
start a number, and you keep consuming digits (and at most one decimal point)
until they stop. Whitespace is skipped. Anything unrecognised is an error.

Keep the **position** of each token. You need it for error messages, and adding it
later means touching every line you wrote.

```text
tokenise("1 + $")  ->  error: unexpected character '$' at position 4
```

**Tests before moving on:** empty string, only whitespace, a lone operator, a
number with two decimal points, and a very long number.

---

## Stage 2 — Parse and evaluate

This is the interesting part. Precedence means `*` binds tighter than `+`, so
`2 + 3 * 4` must group as `2 + (3 * 4)`.

The standard approach is **recursive descent**: one function per precedence level,
each calling the next-tighter one.

```text
expression  ->  term  (('+' | '-')  term)*
term        ->  factor  (('*' | '/')  factor)*
factor      ->  NUMBER  |  '-' factor  |  '(' expression ')'
```

Read that grammar carefully — it *is* the program. Three functions, one per line.
Each consumes tokens and returns a value (or a tree node). The recursion appears in
exactly one place: `factor` calls `expression` when it sees an opening parenthesis,
which is how nesting works to any depth.

Precedence falls out of the call structure. `expression` cannot see the `3` in
`2 + 3 * 4` until `term` has finished with it, and `term` will not stop while there
is a `*` in front of it. Nobody wrote a precedence rule; the shape of the calls is
the rule.

You have a choice: evaluate as you parse (simpler, returns a number), or build a
tree and evaluate it afterwards (more code, but you can print the tree, which makes
debugging dramatically easier and enables the stretch goals). Either is fine.
Choose deliberately and write down why.

**Correctness checks:**

| Input | Expected | Catches |
|---|---|---|
| `2 + 3 * 4` | `14` | precedence |
| `(2 + 3) * 4` | `20` | parentheses |
| `10 - 2 - 3` | `5` | left-associativity — `5`, not `11` |
| `-3 + 2` | `-1` | unary minus |
| `2 * -3` | `-6` | unary minus after an operator |
| `-(-3)` | `3` | nested unary |
| `(2 + 3` | error at position 6 | unbalanced parentheses |
| `2 ** 3 ** 2` | `512` if implemented | right-associativity — not `64` |

The `10 - 2 - 3` case catches a real and common bug: if you implement subtraction
with recursion instead of a loop, you get right-associativity and the wrong answer.

---

## Stage 3 — Harden

The program must never produce a traceback. Every failure is a message with a
position.

- **Division by zero** — an error, not `inf` and not a crash.
- **Deep nesting** — `((((...))))` five thousand deep will exhaust the call stack
  in most languages. Decide what to do: impose a depth limit with a clear message,
  or convert to an iterative parser. Either is a legitimate engineering answer;
  *crashing is not*.
- **Every single character** as input, including punctuation and non-ASCII.
- **No arguments at all** — print usage.

Aim for 20+ tests with at least 8 error cases. If your error tests only assert
"raises an error", strengthen them: assert the message and the position, because
that is the behaviour a user depends on.

---

## Break it

1. **5,000 nested parentheses.** Whatever happens, explain the mechanism — this is
   your first encounter with the call stack being a finite resource — then handle it
   deliberately.
2. **A 1 MB expression.** Something will get slow. Find out which stage, by timing
   them separately. If your tokeniser builds strings by repeated concatenation, you
   have just discovered why that is quadratic.
3. **`1 +++ 2` and `1 2 3`.** Both invalid, for different reasons. Your messages
   should distinguish them. "Invalid input" for both means you threw away the
   information your parser already had.
4. **`0.1 + 0.2`.** You will get `0.30000000000000004`. This is not a bug in your
   code. Find out what floating point is and why this happens, then decide what
   your calculator should print. Whatever you decide, write down the reason.

---

## Done when

- [ ] Every table row in stage 2 passes.
- [ ] No input produces a traceback. You have tried hard to find one.
- [ ] Error messages name a position, and you have tested those messages.
- [ ] You can explain, out loud, why recursive descent produces correct precedence.
- [ ] You wrote it from a blank file. No tutorial, no starter repository.

---

## Anti-patterns

**Using `eval`.** The program works and you learned nothing. The parser is the
assignment.

**One long function.** The three stages have boundaries so that each is testable
alone. When precedence is wrong, you want to know whether the tokeniser or the
parser is at fault.

**Sentinel error values.** Returning `-1` or `0` on failure makes errors
indistinguishable from results — `calc "0"` is a legitimate `0`. Use your
language's error mechanism.

**Catch-all error handling.** `except: print("invalid input")` throws away the
position and the reason, which is the entire value of the error path. It also hides
your own bugs, which is how a project like this becomes unfixable.

---

## Stretch

- **Variables and assignment** (`x = 5`, then `x * 2`). Requires state that
  survives between inputs, and a decision about undefined variables.
- **Functions** (`sqrt(2)`, `min(1, 2)`). Requires a new grammar rule and argument
  lists.
- **`--tree` flag** that prints the parse tree. Then use it to explain a precedence
  bug to someone else — that is the `explain` gate.
- **Reimplement with shunting-yard.** Same output, completely different technique.
  Comparing what each makes easy is a genuine design lesson, and it is the cheapest
  way to learn that "the algorithm" is usually "an algorithm".

---

## Next

Return to
[`programming-fundamentals`](../../topics/programming/programming-fundamentals/README.md)
for the gates, then [`file-organizer`](../file-organizer/README.md) for a project
that touches the outside world instead of only strings.
