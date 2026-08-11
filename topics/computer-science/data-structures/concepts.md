# Data structures — concepts

Fourteen concepts with a required depth for each. This file answers *how deeply should I
learn it?*

[← Data structures](README.md) · [Fundamentals](fundamentals.md) ·
[Practical](practical.md)

---

## Depth vocabulary

| Depth | Means | Test |
|---|---|---|
| `aware` | You know it exists and roughly what it does | You would not be surprised by the term, and you know when to go read about it |
| `working` | You can use it correctly and explain the trade-off without notes | You can apply it to a new problem |
| `deep` | You understand the mechanism well enough to debug it and predict failures | You can explain *how* it works and where it breaks |

**The four `aware` markings save you the most time.** Balanced trees, probabilistic
structures, persistent structures, and concurrent structures are each a rabbit hole deep
enough to consume a month, and none of them is what makes you better at this level.

---

## The inventory

| Concept | Depth | The one thing to take from it |
|---|---|---|
| [Memory layout and locality](#memory-layout-and-locality) | **deep** | Layout decides the constant factor; the constant factor decides your choice |
| [Dynamic arrays](#dynamic-arrays) | **deep** | Multiplicative growth; amortised O(1); visible resize spikes |
| [Linked lists](#linked-lists) | **deep** | O(1) insert given a node; terrible locality; a mechanism, not a choice |
| [Hash tables](#hash-tables) | **deep** | Collisions, load factor, resizing, and a reachable O(n) worst case |
| [Trees and BSTs](#trees-and-binary-search-trees) | **deep** | O(log n) if balanced. Sorted input destroys it |
| [Choosing a structure](#choosing-a-structure) | **deep** | Start from the access pattern, never from the structure |
| [Heaps](#heaps-and-priority-queues) | working | Weaker invariant, cheaper to maintain, array-backed |
| [Graphs](#graphs) | working | Adjacency list for sparse; BFS and DFS |
| [Sets and maps as interfaces](#sets-and-maps-as-interfaces) | working | Interface vs. implementation is the durable idea |
| [Strings as structures](#strings-as-data-structures) | working | Immutable, so loop concatenation is quadratic |
| [Balanced trees](#balanced-trees) | aware | Know what rotation fixes. Do not implement one yet |
| [Probabilistic structures](#probabilistic-structures) | aware | They trade exactness for space. Know they exist |
| [Persistent structures](#persistent-and-immutable-structures) | aware | New version, shared storage. Know the idea |
| [Concurrent structures](#concurrent-data-structures) | aware | A separate hard problem. Do not start |

---

## Memory layout and locality

**Depth: deep.** The concept that makes this topic professional rather than academic.

The machine reads memory in blocks (~64 bytes) and prefetches ahead. Contiguous data
therefore costs far less to traverse than scattered data, at the same operation count.

What `deep` requires — you can:

- explain why an array traversal beats a linked-list traversal of equal length, and give a
  rough factor
- predict which of two implementations will be faster when their complexities are equal
- explain why a small array can beat a hash table for lookup below ~10–100 items
- explain why iterating a 2D array by rows beats iterating by columns
- state the working conclusion: analysis narrows the candidates, measurement decides

**Test yourself:** you have 50 items, looked up by key, in a hot loop. Hash table or a
linear scan of an array? The answer is "measure", and the reason you would even consider the
array is this concept.

---

## Dynamic arrays

**Depth: deep.**

What `deep` requires — you can:

- explain why capacity grows multiplicatively and what `+1` growth costs (O(n²) to build)
- explain amortised O(1) using your own latency graph, not a definition
- state what you traded for it: wasted memory and occasional latency spikes
- say when the spikes matter — a strict tail-latency budget makes an unpredictable pause
  worse than a consistently slower structure
- state the cost of `insert(0, x)` versus `append(x)` and why they differ

**Test yourself:** you append a million items to an empty list. How many total element
copies happen with doubling? *(Roughly 2n — each item is copied at most twice on average.
Deriving that is the exercise.)*

---

## Linked lists

**Depth: deep** — the mechanism, not because you will choose one.

What `deep` requires — you can:

- implement singly and doubly linked insertion and deletion correctly, including at the head
  and tail
- explain why finding item N is O(n) with no arithmetic shortcut
- explain the locality penalty and roughly its size
- name two real structures that use a linked list internally (LRU cache, hash-table
  chaining, adjacency lists)
- explain why you rarely choose one directly despite its good insertion complexity

**Test yourself:** why does an LRU cache need a doubly linked list rather than an array? *(It
needs O(1) removal from the middle given a node — an array cannot, and finding the node is
what the hash table is for.)* You will build exactly this in
[`caching`](../../backend/caching/README.md).

---

## Hash tables

**Depth: deep.** The most valuable single concept in the topic.

What `deep` requires — you can:

- explain hashing, and why a hash function must be fast, deterministic, and well-distributed
- implement one collision strategy and describe the other, with trade-offs
- explain load factor and why implementations resize around 0.7
- explain resizing and why every key must be rehashed rather than copied
- explain why deletion under open addressing needs tombstones, and what breaks without them
- explain the O(n) worst case and what makes it *reachable in practice* — adversarial keys,
  and hash randomisation as the mitigation
- explain why a mutable object is a dangerous hash key

**Test yourself:** you insert a key, mutate the object you used as the key, then look it up
and it is gone. Why? *(The hash changed, so you are looking in a different slot from the one
it is stored in. It is still there and unreachable.)* This is a gate, and it is a real bug
people ship.

---

## Trees and binary search trees

**Depth: deep.**

What `deep` requires — you can:

- state the BST invariant and check it
- implement insert, search, and delete — including the two-child case, which is the one
  people skip
- explain why sorted insertion degrades the tree to a list, and demonstrate it with a
  measured height
- explain what balancing fixes, without needing to implement it
- explain when a BST beats a hash table (ordered iteration, range queries,
  next-largest-key) and when it does not (plain lookup)

**Test yourself:** name two queries a hash table cannot answer without scanning everything.
*(Range queries; next-largest key. Both are why database indexes are trees and not hash
tables.)*

---

## Choosing a structure

**Depth: deep.** The skill interviews actually probe, and the one that transfers.

What `deep` requires — you can:

- start from the access pattern rather than the structure
- state the operations and their frequencies before deciding
- justify a choice against at least one named alternative
- recognise when you need **two structures combined**, and say which property each provides
- change your mind when a measurement contradicts your analysis

**Test yourself:** top 10 trending items from 100,000 events per second. What do you use?
*(A hash table for counts plus a size-10 heap for the top — neither alone gives you both
O(1) counting and cheap top-k. Recognising that is the whole skill.)* This is the `design`
gate in [`topic.yml`](topic.yml).

---

## Heaps and priority queues

**Depth: working.**

- state the heap invariant and why it is weaker than a BST's
- implement push, pop, and heapify; check the invariant after every operation in a test
- explain why heapify is O(n) rather than O(n log n)
- explain why the array backing gives it good locality
- use it for top-k over a stream and explain why sorting would be worse

**Deferred:** Fibonacci heaps, pairing heaps, and the theoretical improvements to Dijkstra.
`advanced-algorithms`.

---

## Graphs

**Depth: working** — the representations and the two traversals.

- choose between adjacency list and matrix, with the sparsity argument and the numbers
- implement BFS and DFS
- state what each finds: BFS gives shortest paths in unweighted graphs; DFS gives cycles and
  topological order
- recognise a graph problem when it is not described as one — dependencies, permissions
  inheritance, friend recommendations

**Deferred:** Dijkstra, A*, minimum spanning trees, max flow, strongly connected components.
`algorithms` and `advanced-algorithms`.

---

## Sets and maps as interfaces

**Depth: working.** Small concept, disproportionate payoff.

A *map* is an interface: keys to values, with lookup, insert, delete. A *hash table* is one
implementation; a *balanced tree* is another. Same interface, different guarantees — the tree
version gives you ordered iteration and O(log n); the hash version gives O(1) and no order.

- name your language's map and set types and say which implementation each uses
- know whether your language's map preserves insertion order, and whether that is a
  guarantee or an implementation detail you must not rely on
- choose the tree-backed variant when you need ordered iteration

**Why this matters more than it looks:** separating interface from implementation is the idea
behind `software-design-principles`, and this is the cleanest small example of it you will
meet.

---

## Strings as data structures

**Depth: working.**

- explain why strings are usually immutable, and why `s += x` in a loop is O(n²)
- use join or a builder instead, and explain why it is O(n)
- know that "length" is ambiguous — bytes, code points, and user-perceived characters
- know what a trie is for (prefix queries, which hashing cannot do at all) without
  implementing one now

**Deferred:** ropes, suffix arrays, KMP and Boyer-Moore, Unicode normalisation.
`advanced-algorithms`.

---

## Balanced trees

**Depth: aware.** Deliberately capped, and this is the cap most worth respecting.

Rotations keep a tree's height at O(log n) despite adversarial insertion order. AVL keeps
strict balance (faster lookups, more rotations); red-black keeps looser balance (fewer
rotations, slightly taller). B-trees are the multi-way version used by databases and
filesystems, because they match how storage reads blocks.

**What you need:** know that sorted insertion breaks a plain BST, that rebalancing fixes it,
and roughly that it works by rotating subtrees.

**What you do not need:** to implement one. It is genuinely fiddly, and the effort pays off
far better at `database-internals`, where B-trees are the mechanism behind every index you
create, the block size has a physical reason, and you can measure the consequences of getting
it wrong.

If your project needs a balanced tree, use your language's — that is the correct
professional decision as well as the correct learning decision.

---

## Probabilistic structures

**Depth: aware.**

Structures that give up exactness for a large space saving:

- **Bloom filter** — "definitely not present" or "probably present". No false negatives.
  Databases use them to skip disk reads for keys that cannot be there.
- **HyperLogLog** — approximate distinct counts in kilobytes instead of gigabytes.
- **Count-min sketch** — approximate frequencies in a stream.

**What you need:** know they exist, know the trade (exactness for space), and recognise when
a problem tolerates approximation. "How many unique visitors, roughly?" tolerates it. "How
much does this customer owe?" does not.

`advanced-algorithms` treats them properly. The Bloom filter is the stretch goal in the
[project](../../../projects/ds-from-scratch/README.md) if you want a taste.

---

## Persistent and immutable structures

**Depth: aware.**

Structures where an "update" returns a new version, sharing most of its storage with the old
one. Git's object model works this way. So do the collections in Clojure and Scala.

**What you need:** the idea that immutability need not mean copying everything, because
structure sharing makes it cheap.

`functional-programming` covers why you would want this; `memory-management` covers how it is
made efficient.

---

## Concurrent data structures

**Depth: aware.** Deliberately capped, and the cap matters most here.

Making a structure safe for simultaneous access from multiple threads is a **separate hard
problem** — not an extension of this topic. Locks, lock-free algorithms with atomic
compare-and-swap, and the memory-ordering guarantees the hardware provides.

**What you need:** know that a structure correct in a single thread can be corrupted by two
threads, and that fixing it is its own discipline.

**Do not start here.** `concurrency-and-parallelism` is Level 3 and requires
`operating-systems-fundamentals`, because concurrency bugs cannot be reasoned about without a
model of threads, scheduling, and memory visibility. Attempting a lock-free structure now
produces code that works by luck, plus the belief that it works because a test passed.

You will meet the concrete version in the
[in-memory cache project](../../../projects/in-memory-cache/README.md), where you will
corrupt a linked list with two threads on purpose and then fix it with a single lock. That is
the right first exposure — one lock, one demonstrated race — and it is enough.

---

## Using this file

Before each study session, check the depth marking for what you are about to read. `aware`
means twenty minutes and move on. `deep` means hours, and probably more than one pass.

The failure mode this file prevents: spending three weeks implementing a red-black tree
(`aware`) while still unable to say which structure to use for a stated access pattern
(`deep`). That trade feels like rigour and it is the wrong one.

---

## Next

[practical.md](practical.md) — what your language actually gives you, and how to choose under
real constraints.
