# Data structures

**Level 2** · Computer Science · ~80 focused hours · 6–10 weeks

How data is arranged in memory, and what that arrangement makes cheap or expensive.

[Fundamentals](fundamentals.md) · [Concepts](concepts.md) ·
[Practical](practical.md) · [Exercises](exercises.md) · [Projects](projects.md) ·
[Interview](interview.md) · [Advanced](advanced.md) · [Resources](resources.md)

---

## What this is

Arrays, linked lists, hash tables, trees, heaps, and graphs — what each one is, what each
makes fast, and what it costs you in exchange.

You have already used most of these. Your language calls them lists, dicts, and sets, and
they work. This topic is about what is inside them and why it matters.

## Why it matters

**The wrong structure is the most common cause of code that is correct at 1,000 items and
unusable at 1,000,000.** Not a bug — a choice, made early, that only reveals itself under
real data. By the time it does, the choice is embedded in a lot of code.

But the deeper reason is different from what most courses claim. You will almost never
implement a hash table professionally; your language's is better than yours will be. The
value is **prediction**: given a problem, knowing which structure makes the operations you
need cheap, and being able to say so before writing the code.

And there is a third reason, which is the most important one and is usually left out.
This is the first topic where **theory and measurement openly disagree.** A linked list
and an array have the same asymptotic traversal cost and the array is often ten times
faster, because the machine reads memory in blocks. Discovering that — with your own
numbers — is the beginning of engineering judgment, because it is where you learn that
analysis narrows the candidates and measurement decides.

## Prerequisites

**Hard:**

- [`programming-fundamentals`](../../programming/programming-fundamentals/README.md) — you
  need enough fluency that implementing a linked list is about pointers and invariants
  rather than about syntax. The `collections` and `mutability-and-aliasing` concepts
  especially: this topic explains what you have been using, and pointer-based structures
  are aliasing made deliberate.

**Soft:**

- `discrete-math-for-engineers` — induction and counting make complexity arguments provable
  rather than plausible.
- `complexity-analysis` — deliberately soft. Measuring first and formalising second works
  better than the reverse, which is why the project comes before the notation.

If a structure's *implementation* is confusing rather than its *purpose*, the gap is
usually in programming fundamentals — specifically the binding model. Go back one level;
it is faster than pushing through.

## How deeply to learn this

Depth per concept is in [concepts.md](concepts.md). The shape:

**Deep** (6) — memory layout and locality, dynamic arrays, linked lists, hash tables, trees
and BSTs, and choosing a structure. `hash-tables` and `choosing-a-structure` are the two
that pay off daily for the rest of your career.

**Working** (4) — heaps, graphs, sets and maps as interfaces, strings as structures.

**Aware** (4) — balanced trees, probabilistic structures, persistent structures, concurrent
structures. Know what problem each solves; do not implement them now.

`balanced-trees` is worth a specific note. You should know **what rebalancing fixes** —
because sorted insertion is not an exotic input, it is what happens when you insert by
timestamp or auto-increment ID — but you do not need to implement an AVL or red-black tree.
That implementation effort is much better spent when you reach `database-internals` and
B-trees, where the mechanism has direct consequences you can measure.

## Reading order

1. [fundamentals.md](fundamentals.md) — the structures derived from how memory works.
2. [concepts.md](concepts.md) — the inventory with depth per concept.
3. [practical.md](practical.md) — what your language actually gives you, and choosing under
   real constraints.
4. [exercises.md](exercises.md) — drills, including the measurement ones.
5. [projects.md](projects.md) — the build-from-scratch project.
6. [interview.md](interview.md) — where this topic dominates technical interviews.
7. [resources.md](resources.md) — eight resources.
8. [advanced.md](advanced.md) — where the depth goes next.

## How you know you have it

Full gates in [`topic.yml`](topic.yml). The distinguishing ones:

- **Explain amortised O(1) append using your own latency graph**, not a definition.
- **Explain why a hash table is O(1) average and O(n) worst case**, and what makes the
  worst case reachable in practice rather than in theory.
- **Explain why your hand-written structure is far slower than the built-in** despite
  identical complexity — naming a mechanism, not just observing the fact.
- **Measure** hash-table lookup across load factors, find the knee, and say why real
  implementations resize around 0.7.
- **Design**: choose structures for "top 10 trending items from 100,000 events per second"
  and justify each against one alternative.

The last one is what interviews actually test, and it is a different skill from
implementation.

## What comes next

| Next | Why |
|---|---|
| `algorithms` | You have the structures; algorithms are the techniques that operate on them |
| `complexity-analysis` | You have measured the shapes. Now formalise them so you can predict without measuring |
| `sql` | A database is data structures you query. Indexing will make immediate sense |
| [`caching`](../../backend/caching/README.md) | Your hash table plus your linked list *is* an LRU cache. That is the next real system |
