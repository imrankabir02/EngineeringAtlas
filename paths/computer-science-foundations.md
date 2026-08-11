# Computer science foundations

**Level 2 → Level 4** · roughly 8–14 months part-time · assumes you build working software

Machine-readable steps: [`computer-science-foundations.yml`](computer-science-foundations.yml)
Prerequisite path: [programming-foundations](programming-foundations.md)

---

## Who this is for

A working programmer who wants the theory that **predicts behaviour** — rather than the theory that
appears in exams.

The distinction is the whole design of this path. Formal computer science is large, and most of it
will not change how you work. What follows is the subset that repeatedly does: knowing what your
code costs before running it, choosing structures from access patterns, recognising an intractable
problem, and being able to read a paper when the documentation runs out.

The path ends here:

> You can read an algorithms or systems paper and judge whether it applies to your system, and you
> can recognise when a problem is intractable and needs an approximation rather than more effort.

---

## Why this material, and why in this order

**Measurement before formalism.** [`data-structures`](../topics/computer-science/data-structures/README.md)
comes with a build-and-benchmark project, and `complexity-analysis` comes *before* it so you have
the notation — but the topic deliberately makes the analysis a soft rather than hard prerequisite,
because measuring first and formalising second works better than the reverse. You will discover
that a linked list and an array have identical complexity and 10× different speed, and that
discovery is what makes the notation useful rather than academic.

**`reading-research-papers` is placed early, not last.** It is normally treated as an advanced
skill and it is mostly a *habit*, gated by nothing except being willing to be confused for an hour.
Placing it in the middle of this path means you practise it on algorithms papers, where the
contribution is usually crisp and checkable, before you need it on systems papers where it is not.

**Two Level 4 topics are included** — `computation-theory` and `information-theory` — which is why
the path's exit level is 4. Neither is needed for most engineering work. Both are here because they
answer questions that otherwise stay permanently open: *is this problem actually hard, or am I bad
at it?* and *why can this not be compressed further?*

---

## Phase 1 — cost, and the structures that determine it

**Steps 1–4 · roughly 5–8 months**

| Step | What you get |
|---|---|
| `discrete-math-for-engineers` | Induction, counting, modular arithmetic, graph theory — enough to read papers |
| `complexity-analysis` | Predicting how cost grows, and the notation's limits |
| [`data-structures`](../topics/computer-science/data-structures/README.md) | Layout, and what each structure makes cheap |
| `algorithms` | The techniques, not the solutions |

Start with `discrete-math-for-engineers`, and be ruthless about scope: only the parts that appear
in engineering. Sets and relations, propositional logic, proof by induction, combinatorics for
counting cases, modular arithmetic for hashing and wrapping, and graph theory. **Skip anything you
cannot connect to a program you might plausibly write.** The full discipline is enormous and most
of it is not relevant to you.

`complexity-analysis` is short and worth doing carefully. Learn the notation, and learn its limits
in the same week — constants, cache behaviour, and real input distributions all matter, and none of
them appears in O(n). An engineer who knows Big-O but not that will write elegant slow code and be
confused by profiles.

`data-structures` is the largest step and the one with the project. Build a dynamic array, hash
table, BST, and heap from primitives, then benchmark them against your language's built-ins and
explain every gap. Your implementations will be much slower despite identical complexity, and
explaining *why* — compiled versus interpreted, contiguous versus boxed, specialised fast paths — is
the deliverable. That is the moment Big-O stops being the whole story, which is the beginning of
engineering judgment and cannot be reached by reading.

`algorithms` last. Study the *techniques* — divide and conquer, greedy choice, loop invariants,
dynamic programming's overlapping subproblems — rather than memorising solutions. Your standard
library has the implementations; what does not come from a library is the ability to recognise which
technique a new problem wants.

**Milestone.** You can choose a data structure from a stated access pattern and defend it against
an alternative, state the complexity of your own code, and explain a case where measurement
contradicted your analysis.

---

## Phase 2 — the parts that tell you where the limits are

**Steps 5–8 · roughly 3–6 months**

| Step | What you get |
|---|---|
| `advanced-algorithms` | Graphs, DP, string algorithms, probabilistic structures |
| `reading-research-papers` | The ability to use primary sources when documentation runs out |
| `computation-theory` | Recognising a problem that cannot be solved exactly |
| `information-theory` | Why compression, hashing, and error detection behave as they do |

`advanced-algorithms` is chosen for a specific reason: **every technique in it appears inside
infrastructure you already use.** Bloom filters in your database's index lookups. HyperLogLog in
your analytics system's distinct counts. Consistent hashing in your cache cluster. Topological sort
in your build tool. Learn them by finding them in real systems, which is far more motivating than
learning them as exercises.

`reading-research-papers` — read one algorithms paper and answer four questions in writing: what is
the contribution (one sentence, not the abstract), what assumption makes it work, what does it cost,
does it apply to a system you have built? That is the whole method, and doing it four or five times
converts papers from intimidating to useful.

`computation-theory`'s practical payoff is narrow and real: **recognising that a problem is
NP-hard so you stop trying to solve it exactly and start looking for an approximation, a heuristic,
or a reformulation.** Scheduling, packing, routing, and constraint problems all have this shape, and
engineers who cannot recognise it lose weeks. Reductions and NP-completeness matter here; automata
theory much less.

`information-theory` answers the "why can this not be better" questions. Entropy sets a floor on
compression, which explains why your compression ratio stopped improving. Hash collision behaviour
follows from counting. Error-detecting codes explain how networks and storage survive corrupted
bits. It also gives you the vocabulary for a surprising amount of machine learning.

**Milestone.** You can read an algorithms or systems paper and judge whether it applies to your
system, and you can recognise when a problem is intractable and needs an approximation rather than
more effort.

---

## Where people stall

**Trying to learn all of discrete mathematics.** The classic failure here. The material is
genuinely large and interesting, and you can spend a year on it with almost no engineering payoff.
Use the "can I connect this to a program I might write?" test aggressively.

**Grinding competitive-programming problems instead of doing the project.** They train retrieval on
a fixed problem set, which is not the skill this path builds, and they will make you feel incapable
for reasons unrelated to your progress. See
[interview.md](../topics/computer-science/data-structures/interview.md#on-grinding-problem-sets).

**Skipping stage 5 of the data-structures project.** Four implementations with no benchmark is
transcription. The measurement and the written explanation are the entire point.

**Reading CLRS front to back.** It is a reference for a rigorous course, not a self-study path.
Sedgewick, or Open Data Structures, and CLRS for lookup.

**Assuming this path is required.** It is not, for most jobs. If your goal is shipping backend
services, [software-engineering-core](software-engineering-core.md) is the better spine and it
includes the data-structures and complexity topics. Take this path when you want the depth for its
own sake, or because you are aimed at systems, research, or infrastructure work.

---

## Honest effort estimate

| Step | Focused hours | Calendar, at ~8 h/week |
|---|---|---|
| `discrete-math-for-engineers` | ~60 | 8 weeks |
| `complexity-analysis` | ~30 | 4 weeks |
| `data-structures` (incl. project) | ~80 | 10 weeks |
| `algorithms` | ~80 | 10 weeks |
| `advanced-algorithms` | ~80 | 10 weeks |
| `reading-research-papers` | ~30 | 4 weeks |
| `computation-theory` | ~60 | 8 weeks |
| `information-theory` | ~50 | 6 weeks |
| **Total** | **~470** | **~60 weeks (13–14 months)** |

The last three steps are genuinely optional for most engineering careers. Stopping after
`reading-research-papers` — roughly eight months — leaves you with the whole practical payoff of this
path, and the last two are for when the "why is this the limit" questions start bothering you.

---

## What comes next

| Next | Why |
|---|---|
| [Software engineering core](software-engineering-core.md), phase 4 | Apply this to real systems: concurrency, databases, caching, distributed systems |
| [`caching`](../topics/backend/caching/README.md) | The most direct application: your hash table plus your linked list becomes a real system |
| `database-internals` | Where these structures live on disk. B-trees, LSM trees, and buffer pools |
| `performance-engineering` | The professional version of the measurement discipline this path taught |
| `research-engineering` (L5) | If the last two steps were the interesting part rather than the optional part |

**The most common good next step** is `caching`, because it is where the theory becomes a system you
operate — and it is where you learn that adding a component adds a failure mode, which is the
defining lesson of Level 3.
