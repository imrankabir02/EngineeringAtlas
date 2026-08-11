# How computers work — advanced

**This file is short, and that is the correct outcome.**

[← How computers work](README.md) · [Concepts](concepts.md) ·
[Resources](resources.md)

---

## Why this file is short

`computer-basics` has no advanced dimension *of its own*. It is an orientation topic: its
job is to install a physical model of the machine so that later topics have something to
attach to. There is no deeper version of "RAM is faster than disk" — there is only the
deeper machinery underneath, and that machinery belongs to topics with prerequisites you
do not yet have.

Padding this file with cache-line sizes and pipeline diagrams would be a disservice. You
would read interesting material, retain very little of it, and spend a week not doing the
[project](../../../projects/machine-anatomy/README.md), which is where the value in this
topic actually is.

So instead of content, this file is a **map of where the depth lives**, and a list of
questions worth deferring.

---

## Where each concept gets its real treatment

| The question you now have | Where it is answered | Level |
|---|---|---|
| How does the CPU cache actually work? Cache lines, associativity, false sharing | `memory-management`, `performance-engineering` | 3–4 |
| How does the OS give each process private memory? | `operating-systems-fundamentals` (virtual memory, page tables) | 3 |
| How does the OS decide which process runs? | `processes-and-scheduling` | 3 |
| What happens between `write()` and the data being durable? | `filesystems-and-storage` | 3 |
| How do multiple cores agree on the contents of memory? | `concurrency-and-parallelism`, then `memory-management` | 3 |
| How does a program get turned into instructions? | `compilers-and-interpreters` | 4 |
| What is the theoretical limit of computation? | `computation-theory` | 4 |
| Why is my program slow when the algorithm looks fine? | `performance-engineering` — usually the answer is memory layout | 4 |
| How do I design an experiment that answers a performance question honestly? | `experiment-design-and-benchmarking` | 5 |

Each of those has hard prerequisites you do not have yet. Reading them today produces the
sensation of learning without the substance, which is the exact failure mode described in
[philosophy.md](../../../docs/philosophy.md#tutorial-hell).

---

## Questions worth writing down and deferring

Start a file — a notes file, a text document, anything durable — and put deferred questions
in it. This is a habit worth having for your whole career: the questions you cannot answer
yet are the best possible curriculum for six months from now.

Good candidates from this topic:

1. Why is 32 KB a common L1 cache size? What sets that number? *(Answered in
   `memory-management`: latency scales with size and it must fit within a single-cycle-ish
   access budget.)*
2. If the OS can move my data to disk without telling me, how can any program reason about
   its own performance? *(`operating-systems-fundamentals` — and the honest answer is
   "imperfectly", which is why measurement beats reasoning.)*
3. Two cores both have a copy of the same memory in their caches. One changes it. What
   happens? *(Cache coherence, in `concurrency-and-parallelism`. The answer is a protocol,
   and it costs real time.)*
4. My disk read measurements varied between runs. Why, and how would I get a trustworthy
   number? *(`experiment-design-and-benchmarking` at Level 5 — and the fact that you asked
   is a good sign.)*
5. If a byte holds 256 values, how are numbers larger than 255 stored? Negative numbers?
   Fractions? *(`programming-fundamentals` covers the practical answer within weeks; the
   floating-point surprises are worth meeting early.)*

---

## Two things worth doing now instead

If you have finished the project and gates and want more, neither of these requires new
prerequisites.

**Build a computer from switches, conceptually.** Petzold's *Code* (see
[resources.md](resources.md)) constructs a working computer from relays, one step at a
time. It is the only accessible treatment that never asks you to accept something on
faith, and finishing it removes the residual sense that there is magic somewhere in the
stack. Roughly 15 hours, and it pays off for years.

**Take one more measurement, more carefully.** Repeat the 1 GB read ten times and look at
the variance. Then ask why the numbers differ, and what you would have to control to make
them stable — file size, cache state, other processes, CPU frequency scaling, filesystem
choice. You will not get a clean answer, and discovering that measurement is *hard* is a
genuinely advanced lesson available at Level 0. It is the seed of everything in
`experiment-design-and-benchmarking`.

---

## Next

Go to `what-programming-is`. You have the model of the machine; the next question is how
you tell it what to do.
