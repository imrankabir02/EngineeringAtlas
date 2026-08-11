# Data structures — resources

Eight resources. Two of them are source code, which is deliberate.

Selection rules: [resource-tiers.md](../../../docs/resource-tiers.md).

[← Data structures](README.md) · [Fundamentals](fundamentals.md) ·
[Advanced](advanced.md)

---

## Tier 1 — Primary sources

For this topic, the primary source is the implementation.

### [CPython source — `Objects/dictobject.c`](https://github.com/python/cpython/blob/main/Objects/dictobject.c)

A production hash table with its reasoning written down by the people who made it.

**Read the header comment, not the whole file.** The first few hundred lines explain the design
of compact dicts: why the table stores indices into a dense array of entries rather than the
entries themselves, what that saves in memory, and what it costs. It is a real space-versus-time
decision, annotated by the engineers who argued about it.

Also find where it decides to resize and note the threshold. Compare it with your own choice in
the [project](../../../projects/ds-from-scratch/README.md).

**Why this and not another explanation of chaining:** you have read explanations. Reading an
implementation that serves billions of programs, with its trade-offs stated as comments, is a
different and more valuable experience. It is also the gentlest possible introduction to
`reading-source-code` at Level 4, because you already understand the structure from the inside.

### [Java SE API — `HashMap`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashMap.html)

Read the class-level documentation.

A rare case where official documentation makes a structure's **performance contract precise
enough to reason about**: it states the default load factor (0.75), the resizing behaviour, and
the treeification threshold — the point at which a heavily colliding bucket becomes a tree to
bound the worst case at O(log n) instead of O(n).

That last detail is a real implementation defending against the denial-of-service technique
described in [fundamentals.md](fundamentals.md#the-worst-case-is-reachable). Seeing a mitigation
documented in an API reference connects the theory to something that shipped.

---

## Tier 2 — High-quality learning material

### [Algorithms, 4th edition — Sedgewick and Wayne](https://algs4.cs.princeton.edu/home/)

**The best single book for this topic.** Chapters 1–3 cover everything here.

What distinguishes it: it presents **empirical measurement alongside the analysis**, as a matter
of course. Most texts give you the asymptotic result and stop; Sedgewick gives you the result
*and* the measured running times *and* discusses when they disagree. That is exactly the habit
this topic is trying to build.

The site includes the full text of key sections, all the code in Java, and the exercises. Free.

**How to use it:** read a section, implement the structure yourself before looking at their
implementation, then compare. The comparison is where the learning concentrates.

### [Open Data Structures — Pat Morin](https://opendatastructures.org/)

Free, rigorous, and unusually direct about the cost of each operation. Pseudocode plus real
implementations in Java, C++, and Python.

**Best used as the reference you check against while doing the project.** When your BST delete
is wrong, its treatment is precise enough to find your mistake — it states invariants explicitly
rather than relying on the code to convey them.

More formal than Sedgewick and less discursive. Some people prefer it for exactly that reason.

### [MIT 6.006 Introduction to Algorithms (OCW)](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/)

Lectures, notes, and problem sets from a course that **derives** structures from their
invariants rather than presenting them as recipes.

**Use the problem sets.** They are where the learning is, and they are harder than they look.
The lectures are good; the problem sets are what change your capability.

Relevant lectures for this topic: the sequences-and-sets interface framing (which is the
`sets-and-maps-as-interfaces` concept, done properly), hashing, and binary trees.

### [The Lost Art of Structure Packing — Eric Raymond](http://www.catb.org/esr/structure-packing/)

Short, and the most direct available bridge from "data structures" to "why is my code slow".

Explains why the same fields in a different order occupy different amounts of memory, and why
that changes how many items fit in a cache block — and therefore performance. Concrete, with
numbers.

Read it after you have measured the array-versus-linked-list traversal gap, when you are already
suspicious that layout matters more than you were taught.

---

## Tier 3 — Practical

### [Visualgo — data structure visualisations](https://visualgo.net/en)

Animates insertion, deletion, and rebalancing step by step.

**Use it when a specific operation will not resolve in your head** — BST delete with two
children, or heap sift-down, are the usual candidates. Ten minutes watching the animation beats
an hour rereading prose.

Do not browse it. It is a debugging tool for your mental model, not a course.

### [A Gallery of Processor Cache Effects — Igor Ostrovsky](https://igoro.com/archive/gallery-of-processor-cache-effects/)

**Run these. Do not just read them.** Seven small experiments where the only change is the
memory access pattern and the runtime changes by an order of magnitude.

Example 1 is the one that reorganises your thinking: a loop touching every element of an array
versus one touching every 16th element. Sixteen times fewer operations, **almost the same
runtime**, because the cost is fetching cache blocks rather than touching elements.

Nothing in Big-O predicts that. This is the most convincing demonstration available that
complexity analysis is not the whole story, and it is why `memory-layout` is marked `deep` in
[concepts.md](concepts.md).

Predict each result before running it. You will be wrong on at least three.

---

## What is deliberately not here

The reasons are more useful than more links.

**CLRS (*Introduction to Algorithms*, Cormen et al.).** The standard reference, and genuinely
excellent — as a *reference*. It is written for a rigorous algorithms course with mathematical
maturity assumed, and reading it front to back at Level 2 is a common way to stall. Get it when
you reach `algorithms` and `advanced-algorithms`, and use it to look things up.

**LeetCode, HackerRank, Codeforces.** Useful later for `algorithms`, unhelpful now. They train
retrieval of solutions on a fixed problem set, which is not the skill this topic builds, and
they will make you feel incapable for reasons unrelated to your progress. See
[interview.md](interview.md#on-grinding-problem-sets).

**"Top 10 data structures every developer must know" articles.** Every one is a worse version of
[fundamentals.md](fundamentals.md), and none of them will tell you that a linked list is 10×
slower than an array at the same complexity.

**Language-specific "data structures in X" tutorials.** They teach the syntax of your standard
library, which is a five-minute lookup, not a topic.

**Videos explaining individual structures.** Adequate for a first exposure and a poor use of
time compared with implementing one. If a structure will not click, use Visualgo — it is the
same benefit in ten minutes instead of forty.

---

## A working plan

Roughly 8 weeks at 8–10 hours per week. Adjust the pace, keep the order.

**Weeks 1–2 — the model.** Read [fundamentals.md](fundamentals.md) and Sedgewick chapter 1. Do
[exercises.md](exercises.md) 1–7. Run the cache-effects experiments now rather than later; they
reframe everything that follows.

**Weeks 3–4 — hash tables and trees.** Sedgewick chapter 3, or Open Data Structures chapters 5
and 6. Exercises 8–18. Read the CPython `dictobject.c` header comment.

**Weeks 5–7 — the project.** [ds-from-scratch](../../../projects/ds-from-scratch/README.md),
including all five stages. **Do not skip stage 5** — the benchmark and the written analysis are
what make this a Level 2 project.

**Week 8 — consolidate.** Finish the exercises, including all Break-it and Measure items. Work
the [`topic.yml`](topic.yml) gates, particularly `design` and `review`. Write up the load-factor
curve and the traversal-ratio measurement properly; they are the two artifacts that will make you
credible about this topic for years.

---

## If you only have ten hours

1. Read [fundamentals.md](fundamentals.md) properly. — 2 hours
2. Run the cache-effects experiments, predicting each. — 1 hour
3. Implement the hash table stage of the project, including resizing and collision deletion.
   — 4 hours
4. Measure the load-factor curve and write the explanation. — 2 hours
5. Do exercise 1 (the eight choosing scenarios) and exercise 9. — 1 hour

Not the full topic, but it gives you the two `deep` concepts that matter most — `hash-tables`
and `memory-layout` — plus one real measurement. That is honest progress.
