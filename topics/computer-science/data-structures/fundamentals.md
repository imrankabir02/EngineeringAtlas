# Data structures — fundamentals

Every structure is a different answer to one question: given how memory works, what do
you want to be cheap?

[← Data structures](README.md) · [Concepts](concepts.md) ·
[Practical](practical.md)

---

## Starting point: what memory actually is

From [`computer-basics`](../../foundations/computer-basics/README.md): memory is a huge
numbered sequence of slots. Two facts about it drive everything in this topic.

**Fact 1: reaching a slot by its number is fast and constant.** Slot 5 and slot 5,000,000
cost the same to access. The hardware computes an address; there is no searching.

**Fact 2: the machine does not fetch one byte at a time.** It fetches a **block** —
typically 64 bytes — into the CPU cache, on the assumption that if you wanted byte 100 you
will probably want byte 101 soon. That assumption is called **spatial locality**, and it is
correct often enough that all modern hardware is built around it.

Fact 1 is in every textbook. **Fact 2 is why measured performance frequently contradicts
asymptotic analysis**, and it is left out of most treatments of this subject. Keep it in
mind throughout; it is the answer to most of the surprises in the
[project](../../../projects/ds-from-scratch/README.md).

---

## Problem 1: store many items → the array

Put items in consecutive slots. Then item `i` lives at `base + i × size`, which is
arithmetic, not searching.

```text
index:    0     1     2     3     4
        ┌─────┬─────┬─────┬─────┬─────┐
        │  17 │   3 │  42 │   8 │  99 │
        └─────┴─────┴─────┴─────┴─────┘
address: 1000  1004  1008  1012  1016
```

**Cheap:** access by index — O(1). Iterating in order, which is *also* fast for the
separate reason that consecutive items share cache blocks.

**Expensive:** inserting or deleting anywhere but the end, because everything after must
shift — O(n). And growing at all, because the next slot may belong to something else.

That last constraint is the interesting one. An array's size is fixed at creation. Which
raises the next problem.

---

## Problem 2: arrays cannot grow → the dynamic array

Allocate more space than you need. Track `size` (used) separately from `capacity`
(allocated). When they meet, allocate a bigger block and copy.

**How much bigger?** This is a real decision with a measurable answer.

Add one slot each time: appending n items copies 1 + 2 + ... + n items in total, which is
n(n+1)/2 — **O(n²)** to build a list. A million appends does about 500 billion copies.

Double the capacity: each item is copied at most a constant number of times on average, so
building the list is **O(n)** and each append is **amortised O(1)**.

"Amortised" means *averaged over a sequence of operations*. Most appends are instant; the
ones that trigger a resize are expensive; the average is constant. This is not a
hand-wave — you can see it:

```text
append latency over 1,000,000 appends

  │                                                          ▐
  │                                    ▐                     │
  │              ▐                     │                     │
  │      ▐       │                     │                     │
  │  ▐▄▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
  └────────────────────────────────────────────────────────────►
    spikes at powers of two: each twice as tall, half as often
```

Each spike is twice as expensive as the last and happens half as often — so their total
contribution stays proportional to n, which is exactly what "amortised O(1)" means.

**Draw this graph yourself** in the [project](../../../projects/ds-from-scratch/README.md).
Seeing it once makes the concept permanent in a way the definition does not.

**The cost you accepted:** wasted memory (up to half the allocated space unused) and
occasional latency spikes. For a system with a strict latency budget, an unpredictable
100 ms spike may be worse than a consistently slower structure — which is a real
engineering trade-off, not a footnote.

This is what your language's list, vector, or slice is.

---

## Problem 3: insertion is expensive → the linked list

If shifting is the problem, stop requiring items to be adjacent. Let each item store the
location of the next one.

```text
head
 │
 ▼
┌────┬───┐   ┌────┬───┐   ┌────┬───┐
│ 17 │ ●─┼──►│  3 │ ●─┼──►│ 42 │ ∅ │
└────┴───┘   └────┴───┘   └────┴───┘
  (anywhere in memory, in any order)
```

**Cheap:** inserting or deleting **given a reference to the node** — O(1). Just rewrite two
pointers. No shifting, no reallocation.

**Expensive:** finding item N — you must walk N links, O(n). There is no arithmetic that
gets you there.

**And a cost that does not appear in the complexity at all:** each node is a separate
allocation, potentially anywhere in memory. Traversing means following pointers to
unpredictable addresses, so the CPU cache prefetching from Fact 2 helps not at all. Every
step may be a cache miss.

The practical consequence, and it surprises people:

> Traversing a linked list of a million integers can be **5 to 20 times slower** than
> traversing an array of a million integers, even though both are O(n).

Same operation count. Different memory layout. That is Fact 2 being decisive, and it is why
linked lists are far rarer in real code than their prominence in courses suggests.

**So why learn them?** Because they are the *mechanism inside* things you will build:

- An **LRU cache** is a hash table plus a doubly linked list — the list gives O(1)
  move-to-front and O(1) eviction from the tail, which no array can. You will build exactly
  this in [`caching`](../../backend/caching/README.md).
- **Adjacency lists** for graphs.
- **Hash table chaining** for collisions.

You will rarely choose a linked list. You will frequently need to understand one.

**The general lesson**, and it is the most important sentence in this file:

> There is no best structure. Every layout makes some operations cheap by making others
> expensive. The question is never "which structure is best" but "which operations do I
> need to be cheap, and what am I willing to pay?"

---

## Problem 4: finding by value, not position → the hash table

Both structures so far find things by *position*. Real problems ask by *value*: "is this
username taken?", "what is the price of product X?"

Both require scanning — O(n).

The idea: **compute the location from the value itself.**

```text
"alice" ──hash()──► 3,847,291 ──% 8──► slot 3

        ┌─────┬─────┬─────┬───────┬─────┬─────┬─────┬─────┐
  slot: │  0  │  1  │  2  │   3   │  4  │  5  │  6  │  7  │
        └─────┴─────┴─────┴───────┴─────┴─────┴─────┴─────┘
                             alice
```

Store `alice` at slot 3. To look her up, hash again, get 3, look there. **One computation,
one array access.** Not a search.

This is the most important data structure in practical programming. It is your language's
dict, map, object, or hash.

### The three complications

**1. Collisions.** Two different keys can hash to the same slot. This is not an edge case;
with 8 slots and 5 keys it is likely. Two strategies:

| Strategy | How | Trade-off |
|---|---|---|
| **Chaining** | Each slot holds a small list of entries | Simple; degrades gracefully; poor locality (back to pointer-chasing) |
| **Open addressing** | On collision, probe for the next free slot | Excellent locality; deletion needs tombstones; degrades sharply when nearly full |

Modern implementations mostly favour open addressing precisely because of Fact 2.

**2. Load factor.** How full the table is (`entries / slots`). As it rises, collisions rise,
and lookup drifts from one step toward several.

```text
lookup time vs load factor

  │                                              ╱
  │                                          ╱
  │                                    ╱
  │  ────────────────────────────╱
  └──────┬──────┬──────┬──────┬──────┬──────►
        0.3    0.5    0.7    0.8    0.9   0.99
                       ↑
                  the knee -- real implementations resize here
```

Flat, then a knee, then bad. **Measure this curve yourself** — it is a gate — and you will
understand why every hash table implementation resizes at around 0.7 rather than waiting
until full.

**3. Resizing.** Crossing the threshold means allocating a bigger array and **rehashing
every key**, because the slot depends on the table size. Amortised O(1) again, with the
same latency-spike caveat as the dynamic array.

### The worst case is reachable

Average O(1) assumes keys spread out. If every key hashes to the same slot, lookup becomes
O(n) — a linked list with extra steps.

This is not hypothetical. It was a real denial-of-service technique: send a web request
with hundreds of form parameters engineered to collide in the framework's hash function,
and the server spends quadratic time parsing it. The fix, now standard, is **hash
randomisation** — a per-process random seed so an attacker cannot predict which keys
collide.

**Cause this yourself** — it is a gate. Watching your "O(1)" structure become O(n) is the
most memorable thing in the topic.

---

## Problem 5: order plus fast lookup → trees

A hash table has no order. It cannot answer "what is the next largest key?" or "all keys
between 10 and 20" without examining everything.

Sorted arrays give you binary search — O(log n) — but insertion is O(n) shifting.

A **binary search tree** keeps the ordering as structure:

```text
                 (50)
                /    \
            (30)      (70)
            /  \      /  \
        (20)  (40) (60)  (80)
```

**The invariant:** for every node, everything on the left is smaller and everything on the
right is larger.

Searching walks down, discarding half the remaining tree at each step — O(log n) *if the
tree is balanced*. Insertion and deletion also O(log n), and in-order traversal produces
sorted output for free.

### The honest worst case

Insert `1, 2, 3, ..., 10000` in that order:

```text
(1)
   \
    (2)
       \
        (3)
           \
            ... 10,000 levels deep
```

You have built a linked list with worse cache behaviour than a linked list. Height 10,000,
not 14. Search is O(n).

**Sorted insertion order is not an exotic input.** It is what happens when you insert
records by timestamp, by auto-increment ID, or from an already-sorted file. This is why
**self-balancing trees** exist — AVL, red-black — which rotate the structure during
insertion to keep height at O(log n).

You should know what rebalancing fixes and roughly how. You do **not** need to implement
one now; that effort pays off far better at `database-internals`, where B-trees are the
mechanism behind every index you will ever create, and where the cost of getting it wrong
is measurable in production.

**Cause the degradation yourself** — it is a gate — and measure the height. Reading that a
BST degrades is forgettable; watching your height counter reach 10,000 is not.

---

## Problem 6: only the smallest, quickly → the heap

Sometimes you do not need full order. A task scheduler needs the highest-priority task and
does not care about the ordering of the rest.

Full ordering is expensive to maintain. So use a **weaker invariant**: every parent is
smaller than its children. Nothing is said about siblings.

```text
                 (2)
                /   \
             (5)     (3)
             / \     /
          (9) (7) (4)

stored as a plain array:  [2, 5, 3, 9, 7, 4]
node i has children at 2i+1 and 2i+2
```

Two properties worth noticing:

- **The weaker invariant is cheaper.** Push and pop are O(log n), and there is no
  rebalancing machinery, because the shape is always a complete tree.
- **No pointers at all.** It lives in a flat array, so Fact 2 works in its favour. Heaps are
  fast in practice, not only in analysis.

**Why `heapify` is O(n), not O(n log n)** — worth deriving yourself rather than being told:
most nodes are near the bottom, and nodes near the bottom sift down a very short distance.
Half the nodes are leaves and move zero levels; a quarter move at most one; and so on. The
sum converges. Working this out is a real complexity-analysis exercise, unlike reciting the
result.

**Where it wins decisively:** the 10 largest values from a stream of 10 million. Sorting is
O(n log n) and needs everything in memory. A heap of size 10 is O(n log 10) and holds ten
items. That contrast is the reason heaps exist.

---

## Problem 7: relationships, not sequence → graphs

Some data is not a sequence or a hierarchy. Social connections, road networks, dependencies
between packages, references between web pages — the *relationships* are the data.

A graph is vertices plus edges. Two representations:

| Representation | Storage | Good for |
|---|---|---|
| **Adjacency list** — each vertex stores its neighbours | O(V + E) | Sparse graphs, which is nearly all real ones. Iterating a vertex's neighbours |
| **Adjacency matrix** — a V×V table of booleans | O(V²) | Dense graphs. Constant-time "is there an edge between A and B?" |

For a social network with 1 billion users and 200 friends each, an adjacency list holds
2×10¹¹ entries. A matrix would hold 10¹⁸. The choice is not close, and knowing *why* is
more useful than knowing which.

The two traversals:

- **Breadth-first** — explore all neighbours, then their neighbours. Uses a queue. Finds
  shortest paths in unweighted graphs.
- **Depth-first** — follow one path to the end, then back up. Uses a stack, or recursion.
  Finds cycles and topological orderings.

The algorithms built on these — Dijkstra, topological sort, minimum spanning trees — belong
to `algorithms` and `advanced-algorithms`. Here, you need the representations and the two
traversals.

---

## The thing that decides: memory layout

Back to Fact 2, because this is where the topic stops being a textbook subject.

Two structures with identical asymptotic complexity can differ by 10× in wall-clock time,
and the reason is always the same: **the machine reads memory in blocks, and it guesses
what you will want next.**

| Layout | What the CPU can do | Result |
|---|---|---|
| Contiguous (array) | Prefetch the next block while you use this one | Near-zero waiting |
| Scattered (pointers) | Cannot predict the next address | A cache miss per step, each ~100× a cache hit |

Consequences that will surprise you until they do not:

- **An array of structs often beats a linked list of the same structs**, at any size that
  fits in memory.
- **An array is often faster than a hash table for small collections** — under roughly 10 to
  100 items, scanning contiguous memory beats hashing plus one scattered access.
- **Struct field order changes performance**, because padding changes how many items fit in
  a cache block. See the structure-packing resource in
  [resources.md](resources.md).
- **Iterating a 2D array by rows is much faster than by columns**, because rows are
  contiguous and columns stride across memory.

None of that appears in Big-O, and all of it is real.

**The working conclusion, which is the professional habit this topic exists to build:**

> Complexity analysis tells you which structures to *consider*. Measurement on realistic
> data tells you which to *use*. Skipping either one produces bad decisions — analysis alone
> gives you elegant slow code, measurement alone gives you code that collapses when the
> input grows.

Run the cache-effects experiments in [resources.md](resources.md). Seven small programs
where the only change is the access pattern and the runtime changes tenfold. It is the most
convincing demonstration available that complexity is not the whole story.

---

## Choosing: the only question that matters

Do not start from the structure. Start from the **access pattern**.

Write down, before choosing anything:

1. What operations do I perform, and roughly how often each?
2. How many items, at realistic scale — not today's scale?
3. Do I need order? Uniqueness? Lookup by key?
4. Which operation is on the critical path?

Then:

| I need to... | Use | Because |
|---|---|---|
| Look up by key | Hash table | O(1) average, and this is most problems |
| Keep insertion order and iterate | Dynamic array | O(1) append, excellent locality |
| Test membership | Set | O(1), and it documents the intent |
| Keep items sorted with inserts | Balanced tree, or sorted array if writes are rare | O(log n) both ways |
| Always get the min or max | Heap | O(log n), and cheaper than full ordering |
| Get the min *and* look up by key | Heap + hash table | Neither alone does both |
| Insert and remove at both ends | Deque | O(1) at both ends |
| Model relationships | Graph (adjacency list) | Edges are the data |
| Find by prefix | Trie | Hashing cannot do prefixes at all |
| Test membership approximately, in tiny space | Bloom filter | Trades exactness for space, deliberately |

Two rows deserve emphasis. **"Heap + hash table"** and **"hash table + linked list"** — real
systems combine structures because no single one provides two properties you need at once.
Recognising when you need a combination is a Level 3 skill and it is the one this topic is
really preparing you for.

---

## Putting it together

```text
Memory is numbered slots; reaching one by number is fast.
Memory is read in blocks; nearby data comes along free.
                          ↓
Store items consecutively.                     → array: O(1) index, O(n) insert
Arrays cannot grow.                            → dynamic array: amortised O(1) append
Shifting is expensive.                         → linked list: O(1) insert, O(n) find, bad locality
Find by value, not position.                   → hash table: O(1) average, O(n) adversarial
Need order too.                                → BST: O(log n) if balanced, O(n) if not
Only need the extreme.                         → heap: weaker invariant, cheaper, array-backed
Relationships are the data.                    → graph: adjacency list for sparse
                          ↓
And underneath all of it: layout decides the constant factor,
and the constant factor decides which one you actually use.
```

---

## Next

[concepts.md](concepts.md) for depth per concept, then
[practical.md](practical.md) for what your language actually gives you.
