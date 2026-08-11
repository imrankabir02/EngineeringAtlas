# Data structures — projects

[← Data structures](README.md) · [Exercises](exercises.md) ·
[Interview](interview.md)

---

## Core project

### [Data structures from scratch](../../../projects/ds-from-scratch/README.md)

**Level 2** · validates `dynamic-arrays`, `hash-tables`, `trees-and-bst`, `heaps`,
`memory-layout`

Implement a dynamic array, hash table, binary search tree, and binary heap from fixed-size
arrays and objects. Then benchmark them against your language's built-ins and explain every
difference you measure.

**The constraint:** no built-in dynamic list, dict, set, or sorted container *inside* your
implementations.

---

### Why this project, given that your language's versions are better

They are better. Faster, more tested, written in C. You will never ship yours.

That objection is worth answering directly, because it is correct and beside the point.

**What you cannot get any other way:**

**The invariant becomes real.** Reading "a hash table resizes when the load factor exceeds a
threshold" takes ten seconds and teaches nothing. *Deciding* your threshold, discovering that
resizing means rehashing every key rather than copying slots, and then finding that your
deletion broke lookups for keys that collided — that is understanding, and it only arrives
through the implementation.

**The gap between analysis and measurement becomes undeniable.** Your structures will be
much slower than the built-ins despite identical complexity. Explaining *why* — compiled versus
interpreted, contiguous versus boxed, specialised fast paths — is the deliverable, and it is the
moment Big-O stops being the whole story. That moment is the beginning of engineering judgment,
and there is no way to reach it by reading.

**You get to hold a high load factor.** Your language's dict resizes automatically and will not
let you observe the degradation curve. Measuring lookup time at load factors 0.3 through 0.99,
finding the knee, and understanding why every real implementation resizes around 0.7 requires a
structure whose resizing you control. This is a
[benchmark gate](exercises.md#measure-and-explain) and the project is the only way to pass it
honestly.

**Every degradation becomes something you have seen.** A BST reaching height 10,000 on sorted
input. A hash table becoming a linked list under colliding keys. Append latency spiking at
powers of two. Read about these and they are facts; cause them and they are memories, and
memories are what you reason from under pressure.

---

## The stages, and what each one is for

The full specification is in the
[project README](../../../projects/ds-from-scratch/README.md). What each stage is *for*:

| Stage | The lesson |
|---|---|
| **Dynamic array** | Amortised complexity, seen rather than defined. Try `+1` growth first, measure it, then switch to doubling — the difference between O(n²) and O(n) build cost is dramatic and you should feel it |
| **Hash table** | The most valuable structure in practice, and the one with the most subtleties: collisions, load factor, rehashing, and a deletion bug that breaks other keys |
| **Binary search tree** | Ordered operations, and the honest worst case. Includes the two-child delete case that everyone skips — do not skip it |
| **Binary heap** | A weaker invariant is cheaper to maintain. Array-backed, so locality works for you. Derive why heapify is O(n) yourself |
| **Benchmark and explain** | The stage that matters most. Predict, measure, and explain every gap with a named mechanism |

**Do not skip stage 5.** Four implementations without measurement is an exercise in
transcription. The measurement is where this becomes a Level 2 project rather than a Level 1
one.

---

## Stretch project

### [In-memory cache](../../../projects/in-memory-cache/README.md)

**Level 3** · validates `hash-tables`, `linked-lists`, `choosing-a-structure`

An LRU cache with O(1) `get` and `put`, thread safety, and a benchmark harness.

**Why it is the right follow-on:** an LRU cache is a hash table plus a doubly linked list, and
neither structure alone can do the job. The hash table gives O(1) lookup but no ordering; the
list gives O(1) reordering and eviction but no lookup. **Combining two structures because
neither provides both properties you need** is the single most valuable pattern in this topic,
and this is the cleanest example of it that exists.

It is a Level 3 project because it adds concurrency and real benchmarking on top. Doing it now
is legitimate if the core project felt easy — take the single-threaded stages and leave the
concurrency for when you reach [`caching`](../../backend/caching/README.md) properly.

---

## What "done" means

Full checklist in the
[project README](../../../projects/ds-from-scratch/README.md#done-when). The four that matter
most:

1. **You worked from the invariant, not from a copied implementation.** Slower, and the only
   version that produces understanding. Nobody will check; you will know.
2. **The load-factor curve exists and you can explain the knee.** This is the measurement that
   makes "O(1) average" mean something.
3. **You have the linked-list-versus-array traversal ratio**, and it surprised you. Most people
   predict 1–2× and measure 5–20×.
4. **Your written analysis names a mechanism for every gap** against the built-ins. "The
   built-in is optimised" is not a mechanism and does not pass.

---

## Anti-patterns specific to this project

**Wrapping the built-in.** If your dynamic array holds a Python `list` or a JS `Array`, there
is no project. The whole point is the layer underneath.

**Copying an implementation from a textbook or a search result.** You will produce working code
and learn nothing, and you will not notice the difference until an interview or a production
incident.

**Benchmarking only with uniform random keys.** Every hash table looks good on uniform keys.
Real distributions are skewed — use a Zipfian generator for at least one measurement.

**Concluding "the built-in is faster" and stopping.** That was known before you started. The
mechanism is the finding.

**Skipping the two-child BST delete.** It is the case with actual difficulty, and skipping it
means you implemented the easy 70% of a tree.

---

## After the project

Return to [`topic.yml`](topic.yml) for the remaining gates. Two deserve particular attention:

**The `design` gate** — choose structures for "top 10 trending items from 100,000 events per
second" and justify each against an alternative. This is what interviews actually test, and it
is a different skill from implementation. You can implement a heap and still fail this if you
have not practised reasoning from access patterns.

**The `review` gate** — read a standard library's hash map or list implementation and find one
decision that trades memory for speed. Start with the CPython `dictobject.c` header comment,
which is unusually well documented. Pick one question and answer only that; this is the method
of `reading-source-code` at Level 4, practised early on something you now understand from the
inside.
