# Programming fundamentals — advanced

Where the depth lives, what to defer, and the two things worth doing now if you have
finished the gates.

[← Programming fundamentals](README.md) · [Concepts](concepts.md) ·
[Resources](resources.md)

---

## There is no advanced version of this topic

There is a *deeper* version of every concept in it, and each of those belongs to a
different topic with prerequisites you do not yet have.

That is not a limitation of this file. It is the structure of the subject: "programming
fundamentals" is a broad shallow layer that everything else grows out of. Deepening it
means going into memory, types, concurrency, or compilers — and those are separate topics
because they need separate foundations.

So this file is a map, plus an honest account of what happens if you ignore it.

---

## Where each concept gets its real treatment

| The question you now have | Where it is answered | Level |
|---|---|---|
| What is actually happening when I assign a variable? Where does the object live? | `memory-management` | 3 |
| Why do some languages catch my type errors before running? | `type-systems` | 2 |
| How do I organise code once there are 50 files? | `software-design-principles`, `software-architecture` | 2–3 |
| What makes a test *valuable*, not just present? | `testing-fundamentals`, then `test-strategy` | 2–3 |
| How do I debug something systematically instead of by feel? | `debugging-fundamentals` | 1 |
| What does my loop actually cost, formally? | `complexity-analysis` | 2 |
| Which data structure, and why, with the internals? | `data-structures` | 2 |
| How does my source become instructions? | `compilers-and-interpreters` | 4 |
| What happens when two things run at once? | `concurrency-and-parallelism` | 3 |
| Why is my correct-looking code slow? | `performance-engineering` — usually memory layout | 4 |
| How do I design an error taxonomy for a real system? | `error-handling`, then `api-design` | 1, 3 |
| How do I read a large codebase I did not write? | `reading-source-code` | 4 |

Each of those has hard prerequisites. Reading them now produces the sensation of learning
without the substance — see
[tutorial hell](../../../docs/philosophy.md#tutorial-hell).

---

## Second language, and why it is the real graduation

The most valuable thing you can do after this topic is not more of this topic. It is a
**second language chosen to be different from your first.**

The reason: right now you cannot tell which of your knowledge is *programming* and which
is *your language*. That distinction is invisible from inside one language, and it is
exactly what determines whether your skills transfer.

Choose for contrast, not for familiarity or for the job market:

| If you started with | Learn next | Because it forces you to confront |
|---|---|---|
| Python | **C** | Memory is yours. Nothing is hidden. Arrays do not know their length |
| Python | **Go** | Static types, explicit errors as values, concurrency as a language feature |
| JavaScript | **Python** | Coherent design, real integers, and one obvious way to do most things |
| JavaScript | **TypeScript** | The same runtime with a type system bolted on — you see exactly what types buy |
| C | **Python** | How much the language can do for you, and what that costs in control |
| Anything | **A Lisp, or Haskell** | Code as data; or purity and types as design tools. Genuinely different models |

Aim for **one small program**, not fluency. Reimplement your
[calculator](../../../projects/cli-calculator/README.md) in the new language. The
comparison is the lesson: which parts were hard again (the language) and which were
already solved (programming)?

Expect to find that roughly 80% transferred. That number is the payoff of having learned
this topic properly, and finding it out for yourself is more convincing than being told.

---

## Questions worth writing down and deferring

Keep a file of questions you cannot answer yet. It is the best possible curriculum for six
months from now, and the habit is worth having permanently.

Good candidates from this topic:

1. When I write `a = [1,2,3]`, where does the list live, and what happens to it when the
   last name referring to it goes away? *(`memory-management`)*
2. Why is a dict lookup fast? What is it actually doing? *(`data-structures` — and the
   answer will make you re-examine what you assumed about "constant time")*
3. My recursive function crashed at a few thousand levels deep, but my loop handled a
   million iterations. Why is the stack so much smaller than the heap?
   *(`operating-systems-fundamentals`)*
4. If I run the same program twice with the same input, is it guaranteed to behave the
   same? *(Mostly yes now; emphatically no once concurrency, time, and networks are
   involved — `concurrency-and-parallelism`, `distributed-systems-fundamentals`)*
5. Why do some languages make me declare types and others do not? Who is right?
   *(`type-systems` — and the answer is "the question is wrong", which is more interesting)*
6. My string concatenation in a loop got slow. Why exactly? *(Immutability plus
   reallocation — the full picture is in `memory-management`)*

---

## Two things worth doing now instead

If you have finished both projects and all the gates and want more depth without moving
on, these two do not require new prerequisites.

### Read code you did not write

Pick a small, well-regarded library in your language — a few thousand lines, not a
framework. Read it with a specific question: *how does it handle errors?* Or: *where does
it validate input?*

You will not understand all of it and that is not the goal. The goal is to discover that
reading code is a skill you can practise, and that most real code looks less tidy than
tutorials suggest. This is the seed of `reading-source-code` at Level 4, and starting
early is pure advantage.

Good targets: a CLI argument parser, a small HTTP client, a date-formatting library.
Avoid: anything with "framework" in the name, anything over 20,000 lines.

### Rewrite your calculator from memory

Delete it. Wait a week. Write it again from a blank file without looking at the original.

This is uncomfortable and unusually effective. The second version will be shorter and
better structured, because you now know which decisions mattered. What you *cannot*
remember is precisely what you had not internalised, which makes this the most accurate
self-assessment available to you.

It also breaks the illusion that finishing something once means you can do it. That
illusion is the mechanism behind most inflated self-assessment at Levels 1 and 2.

---

## What not to do next

Two paths that feel like progress and are not.

**Do not go to a web framework.** Django, Rails, Express, and React all work fine until
something breaks one layer below where you are looking, at which point it is
unrecoverable, because you have no model of what is underneath. The prerequisite graph
exists to prevent exactly this — see
[framework-first learning](../../../docs/philosophy.md#framework-first-learning). Go
through `version-control-git`, `data-structures`, `http`, and `sql` first. It is not much
longer and it is the difference between using a framework and being trapped in one.

**Do not start a third language.** Two is calibration; three at 20% is
[technology hopping](../../../docs/philosophy.md#technology-hopping). Depth transfers;
breadth does not.

---

## Next

| Next | Why |
|---|---|
| `version-control-git` | You now write code worth not losing, and need to see what changed |
| [`data-structures`](../../computer-science/data-structures/README.md) | You have used lists and dicts. Next is what they cost, and why |
| `debugging-fundamentals` | The highest-leverage skill available to you right now |
| `linux-fundamentals` | Removes the environment as a permanent source of mystery |
