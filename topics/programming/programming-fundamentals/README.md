# Programming fundamentals

**Level 1** · Programming · ~120 focused hours · 8–16 weeks

The concepts every language shares. Learn them once here, reuse them everywhere.

[Fundamentals](fundamentals.md) · [Concepts](concepts.md) ·
[Practical](practical.md) · [Exercises](exercises.md) · [Projects](projects.md) ·
[Interview](interview.md) · [Advanced](advanced.md) · [Resources](resources.md)

---

## What this is

Values and types, variables and binding, conditions, loops, functions, collections,
mutability, modules, and errors — the ideas that appear in every programming language
that has ever mattered.

This topic is **language-agnostic by design**. You will learn it *through* a language,
because there is no other way, but the material is about programming. Which language
you pick matters much less than finishing.

## Why it matters

Everything after this sits on top of it. That is the boring reason. Here are the two
that should change how you approach it.

**This is the most commonly learned-badly topic in software.** It is entirely possible
to produce working code by pattern-matching against examples — copy the shape, change
the names, run it. It feels like progress and produces a specific, brutal failure: you
hit the first problem no example covers, which is every real problem, and you have
nothing to fall back on. The tell is being able to read code fluently and freeze in
front of an empty file.

**Done properly, this is the last time you learn most of it.** Someone who genuinely
understands binding, scope, mutability, and control flow picks up a second language in
weeks — the syntax is a lookup table and the concepts already transferred. Someone who
learned "Python" instead of "programming" starts over each time, which is why some
people have six languages at 20% and no way out.

So: **go slowly here.** This is the one topic where rushing costs the most.

## Prerequisites

**Hard:**

- `what-programming-is` — you need the idea that a program is a precise description of
  a process, or you will treat code as incantations that sometimes work.
- `command-line-basics` — you must be able to run a program, pass arguments, and read
  output and errors. Without this, every error message is invisible and you end up
  developing inside an IDE button whose behaviour you cannot inspect.

**Soft:**

- `problem-solving-basics` — decomposition and tracing state by hand. Learnable
  alongside, but the drills are the difference between debugging and guessing.

## Which language

Pick **one** and finish it. Which one matters far less than that.

| Language | Why it exists | Choose it if | What it costs you |
|---|---|---|---|
| **Python** | Readability and breadth | You want the shortest path from idea to working program; aimed at backend, data, or ML | Hides memory, types, and concurrency. You must learn them later, deliberately, or they become permanent blind spots |
| **JavaScript** | The browser needed a scripting language, then it escaped | Aimed at frontend or full-stack; you want your work visible in a browser immediately | Historical inconsistencies and a large churning toolchain add noise while you are learning to think |
| **C** | A portable abstraction over the machine | You want to understand the machine, or are aimed at systems or embedded work | Slowest path to a working program. Real time spent on memory before you write anything interesting |

**Recommendation for most people: Python.** Then a second language chosen to be
*different* — C for the machine, JavaScript for the browser, Go for concurrency, a Lisp
or Haskell for a genuinely different model. The second language is where you find out
what was the language and what was programming.

Full reasoning, including how to tell you are avoiding difficulty rather than choosing:
[fundamentals.md](fundamentals.md#choosing-a-first-language).

## How deeply to learn this

Depth per concept is in [concepts.md](concepts.md). The shape of the answer:

**Deep** (6 concepts) — values and types, variables and binding, control flow,
functions, collections, mutability and aliasing. These are the load-bearing ones. You
should be able to explain each without notes and predict a program's behaviour by
reading it.

**Working** (6) — errors, debugging, modules, strings and text, I/O, recursion.

**Aware** (3) — cost intuition, how the language manages memory, that concurrency
exists. Know the words. Do not go down these holes yet; each is a Level 2–3 topic with
prerequisites you do not have, and starting them now is the most common way to spend a
month here and finish no better prepared.

`variables-and-binding` deserves special attention. Nearly everyone learns it as "a
variable is a box holding a value", which is wrong in most modern languages and causes
three separate confusions later — aliasing, parameter passing, and closures. Getting it
right now means those confusions never happen.

## Reading order

1. [fundamentals.md](fundamentals.md) — the concepts derived from what a machine does.
2. [concepts.md](concepts.md) — the inventory with depth per concept.
3. [practical.md](practical.md) — environment, tooling, reading errors, and the habits
   that make the difference.
4. [exercises.md](exercises.md) — 30 graded drills. Do these before the projects.
5. [projects.md](projects.md) — the two core projects.
6. [interview.md](interview.md) — what competent discussion sounds like.
7. [resources.md](resources.md) — nine resources, no more.
8. [advanced.md](advanced.md) — where the depth lives, and what to defer.

## How you know you have it

Full gates in [`topic.yml`](topic.yml). The honest test:

**Open a blank file and write a 300-line program that solves a problem you chose, with
no tutorial.** Not a tutorial project. Not something you have written before. When it
breaks, diagnose it yourself and describe the cause in one sentence.

If that is uncomfortable to attempt, you are not done — and the discomfort is the
answer, not a reason to read more.

The other gates worth naming: explain why `0.1 + 0.2 != 0.3` and what to do about
money; demonstrate the aliasing surprise to someone; measure a list-scan against a set
lookup at two input sizes and explain the shape of the difference.

## What comes next

| Next | Why |
|---|---|
| `version-control-git` | You now write code worth not losing, and need to see what changed |
| [`data-structures`](../../computer-science/data-structures/README.md) | You have used lists and dicts. Next is what they cost and why |
| `debugging-fundamentals` | You have debugged by necessity. Doing it deliberately is the highest-leverage skill available now |
| `linux-fundamentals` | Your programs run on a system; fluency there removes a permanent source of mystery |

Do **not** go to a web framework next. See
[philosophy.md](../../../docs/philosophy.md#framework-first-learning) for why that path
works right up until it becomes unrecoverable.
