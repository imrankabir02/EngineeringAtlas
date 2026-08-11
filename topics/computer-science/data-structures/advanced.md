# Data structures — advanced

Where this topic goes at Levels 3–5, what is genuinely still open, and what to defer.

[← Data structures](README.md) · [Concepts](concepts.md) ·
[Resources](resources.md)

---

## The three directions this topic branches into

Unlike the Level 0 and 1 topics, this one *does* have real advanced material — but it goes
three separate ways, and each way is a different topic with its own prerequisites.

### 1. Down, to the hardware

Structures stop being abstract and become memory layouts whose performance is dictated by
cache behaviour.

- **Cache-oblivious structures** — designed to perform well at every level of the memory
  hierarchy without knowing the block size. Van Emde Boas layouts, cache-oblivious B-trees.
- **Data-oriented design** — struct-of-arrays instead of array-of-structs, so that iterating one
  field touches only contiguous memory. Standard practice in game engines and increasingly in
  databases.
- **SIMD-friendly layouts** — arranging data so vector instructions can process several elements
  per cycle.
- **False sharing** — two threads writing different variables in the same cache line, and the
  coherence traffic that destroys performance for no logical reason.

**Prerequisites:** `memory-management` (L3), `performance-engineering` (L4).
Start with the [cache effects](resources.md) experiments — that is the on-ramp.

### 2. Out, to disk and across machines

Structures whose working set exceeds memory, or spans machines.

- **B-trees and LSM trees** — the two dominant on-disk index structures, with opposite
  read/write trade-offs. Every database you use is built on one of them.
- **Write-ahead logs** — an append-only structure whose entire purpose is crash recovery.
- **Consistent hashing** — mapping keys to machines so that adding or removing one moves as few
  keys as possible. The difference between it and modulo hashing is dramatic and measurable.
- **Merkle trees** — hash trees that let two parties find their differences cheaply. Used in
  Git, in replication protocols, and in blockchains.
- **CRDTs** — structures that can be modified independently on several machines and merged
  without conflict, by construction.

**Prerequisites:** `database-internals` (L4), `distributed-systems-fundamentals` (L3),
`partitioning-and-sharding` (L4).

This is the direction most working engineers actually need, because it is where the structures
you understand become the systems you operate.

### 3. Sideways, to approximation and concurrency

- **Probabilistic structures** — Bloom and cuckoo filters, HyperLogLog, count-min sketch,
  t-digest for percentiles. All trade exactness for a large space saving, and all appear inside
  infrastructure you already use.
- **Succinct structures** — storing data in close to the information-theoretic minimum while
  keeping it queryable. Wavelet trees, FM-indexes.
- **Concurrent and lock-free structures** — atomic compare-and-swap, ABA problems, memory
  ordering, hazard pointers, epoch-based reclamation.

**Prerequisites:** `advanced-algorithms` (L3), `concurrency-and-parallelism` (L3),
`information-theory` (L4).

**A specific warning about lock-free structures.** They are the most seductive material in this
list and the most dangerous to attempt early. A lock-free queue that passes tests is not a
correct lock-free queue — the failure modes depend on memory-ordering guarantees and thread
interleavings that testing cannot cover. This is genuinely one of the areas where the standard
professional advice is "use the library", and where `distributed-systems-verification` at Level
5 exists because testing is insufficient.

---

## Where each concept gets deeper treatment

| The question you now have | Where | Level |
|---|---|---|
| Why is my correct-complexity code slow? | `performance-engineering` | 4 |
| Where do objects actually live, and what does allocation cost? | `memory-management` | 3 |
| How do structures work when they exceed memory? | `database-internals` | 4 |
| Which index should this query use, and why does the planner disagree? | `indexing-and-query-optimization` | 3 |
| How do I make a structure safe under concurrency? | `concurrency-and-parallelism` | 3 |
| How do I distribute a structure across machines? | `partitioning-and-sharding` | 4 |
| What algorithms exploit these structures? | `algorithms`, `advanced-algorithms` | 2–3 |
| How do I formalise the costs I measured? | `complexity-analysis` | 2 |
| How do I prove a concurrent structure correct? | `distributed-systems-verification` | 5 |

---

## What is actually still open

Worth knowing that this is not a closed subject, because it is usually taught as if it were.

**Learned index structures.** Replace a B-tree with a model that *predicts* a key's position,
falling back to a search when the prediction is off. Under some distributions this beats
B-trees substantially; the open questions are updates, worst-case guarantees, and adversarial
inputs. Active research since roughly 2018 and moving into real systems.

**Adaptive structures.** Structures that reorganise based on observed access patterns —
splay trees are the classic, and modern work extends the idea to indexes that adapt to a
workload without being told about it.

**Persistent memory structures.** Byte-addressable non-volatile memory sits between RAM and
disk in the hierarchy and invalidates assumptions on both sides. What a crash-consistent
structure looks like when memory itself is durable is not settled.

**Verified structures.** Machine-checked proofs of correctness for concurrent structures.
Progress is real and the cost is still high.

If any of these interests you, that interest is what `reading-research-papers` (L4) and
`research-engineering` (L5) are for. The honest path to working on them is Levels 3 and 4 first.

---

## Two things worth doing now

Neither needs new prerequisites, and both extend this topic rather than starting a new one.

### Run the cache-effects experiments

Igor Ostrovsky's gallery (in [resources.md](resources.md)) is seven small programs where the
only variable is the memory access pattern and the runtime changes by an order of magnitude.
Run them. Predict each result first.

Example 1 alone is worth the time: a loop that touches every element of an array versus one
that touches every 16th. Same array, 16× fewer operations, **almost identical runtime**, because
the cost is fetching cache blocks, not touching elements. Nothing in Big-O predicts that, and
once you have seen it you cannot unsee it.

This is the most direct available bridge from "data structures" to
`performance-engineering`, and it is the reason `memory-layout` is marked `deep` in
[concepts.md](concepts.md).

### Add one structure to your project, chosen for a reason

Extend [ds-from-scratch](../../../projects/ds-from-scratch/README.md) with **one** of:

- **A trie**, then compare it with your hash table for prefix queries. The hash table cannot
  compete at all, which is a much stronger lesson than one where it merely loses.
- **A Bloom filter**, then measure the false-positive rate against the theoretical prediction
  `(1 - e^(-kn/m))^k`. Your first probabilistic structure and your first check of a formula
  against reality.
- **Open addressing** alongside your chaining implementation, compared at load factor 0.9. Open
  addressing usually wins on locality until it suddenly does not, and finding the crossover is a
  genuine experiment.

**One**, not all three. A single structure implemented and measured properly teaches more than
three implemented and moved past.

---

## Questions worth deferring

Add these to the questions file you started in
[`programming-fundamentals`](../../programming/programming-fundamentals/advanced.md).

1. My hash table is O(1) and the database's index is O(log n). Why does the database use a tree?
   *(Disk block reads, range queries, and the fact that log₍₂₅₆₎ of a billion is about four —
   `database-internals`.)*
2. If cache locality matters this much, why are linked lists in every textbook?
   *(Partly history, partly that they are the mechanism inside other structures, partly that
   textbooks predate the current memory-hierarchy ratios.)*
3. How does a structure stay correct if the process crashes halfway through an update?
   *(Write-ahead logging — `filesystems-and-storage`, `transactions-and-isolation`.)*
4. Two threads insert into my hash table simultaneously. What exactly breaks?
   *(`concurrency-and-parallelism`. You will cause this deliberately in the
   [cache project](../../../projects/in-memory-cache/README.md).)*
5. Is there a structure that is optimal for everything? *(No, and there is a body of theory
   about why — lower bounds and the cell-probe model, in `computation-theory`.)*

---

## Next

| Next | Why |
|---|---|
| `algorithms` | The techniques that operate on these structures |
| `complexity-analysis` | Formalise the shapes you measured, so you can predict without measuring |
| `sql` | Structures you query, with durability. Indexing will land immediately |
| [`caching`](../../backend/caching/README.md) | Hash table + linked list = LRU cache. Your first real system |
