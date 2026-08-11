# Data structures — exercises

Twenty-eight drills. The measurement ones are the point; do not skip them.

**Rules:**

- **Predict before measuring.** Write the number down, unedited.
- Use your language's built-ins for exercises 1–20. Implementations come in the
  [project](projects.md).
- Assertions, not eyeballed print statements.

[← Data structures](README.md) · [Concepts](concepts.md) ·
[Practical](practical.md) · [Projects](projects.md)

---

## Choosing

**1.** For each requirement, name the structure and one alternative you rejected, with a
reason:

- a leaderboard showing the top 10 of 5 million players, updated continuously
- a spellchecker deciding whether a word is in a 500,000-word dictionary
- an autocomplete suggesting completions of a typed prefix
- an undo history with unlimited depth
- a set of banned IP addresses, checked on every request
- a phone book supporting "all names starting with 'Ka'"
- a job queue where higher-priority jobs run first
- deduplicating 100 million records that do not fit in memory

The last one is deliberately a trick. It is not an in-memory structure problem.

**2.** You have 30 items looked up by key in a hot loop. Argue for a linear scan over an
array rather than a hash table. Then measure both. Which won, and by how much?

**3.** Design the structures for a URL shortener that must map codes to URLs (10,000
lookups/sec), count clicks per code, and list the top 10 most-clicked. Name every structure
and what property it provides. Justify each against one alternative.

---

## Arrays and lists

**4.** Time appending 1,000,000 items to a dynamic list. Then time inserting 100,000 items at
position 0. Predict the ratio first. Explain the difference in terms of shifting.

**5.** Record per-append latency across 1,000,000 appends and produce a simple histogram or
plot. Identify the spikes. At what indices do they occur, and why those?

**6.** Write a function that removes all items matching a condition from a list. Do it once by
repeatedly calling remove-at (O(n²)) and once by building a new list (O(n)). Measure both at
100,000 items.

**7.** Iterate a 1000×1000 2D array by rows, then by columns, summing every element. Predict
the ratio, measure it, and explain the result using cache blocks.

---

## Hash tables and sets

**8.** Build a dict mapping 1,000,000 integers to strings. Measure lookup for a present key
and an absent key. Are they the same? Explain.

**9.** Write two duplicate-finders — one scanning a list, one using a set. Assert they agree on
random input, then measure both at 1,000 and 100,000 items. Predict the ratio first. Explain
the *shape* of the difference, not just which is faster.

**10.** Count word frequencies in a large text file two ways: with a plain dict, and with your
language's counter type if it has one. Compare readability and speed.

**11.** Use a mutable object as a dict key (a list, or a class with a hash based on a mutable
field). Insert it, mutate it, then look it up. Predict what happens, then explain the
mechanism.

**12.** Find your language's hash function for strings and determine whether it is randomised
per process. Run the same program twice and compare the hash of the same string. Explain what
the randomisation defends against.

**13.** Construct 10,000 keys that collide in a simple hash function you write yourself
(`hash(s) = len(s)` will do). Insert them into a dict-like structure using your hash and
measure lookup. This is a preview of the project's `break_it` stage.

---

## Trees and heaps

**14.** Using a sorted list, implement binary search. Measure lookup at 1,000 and 1,000,000
items. Confirm the shape is logarithmic — a thousandfold size increase should cost about ten
more steps.

**15.** Insert 10,000 random integers into a sorted list, keeping it sorted, measuring total
time. Then do the same with a dict for comparison. Explain why the sorted list is much slower
and what you would use if you needed both order and fast insertion.

**16.** Use your language's heap to find the 10 largest values in a stream of 1,000,000
numbers without holding them all in memory. Compare with sorting everything. Report memory as
well as time.

**17.** Implement a "median maintenance" structure using two heaps — a max-heap of the lower
half and a min-heap of the upper half — that reports the running median in O(log n) per
insertion. Predict how you would do this with a sorted list and why it is worse.

**18.** Using a tree-backed map if your language has one, list all keys in a range. Then do the
same with a hash map. Explain why the second requires examining everything.

---

## Graphs and strings

**19.** Represent a small graph — 8 vertices — as both an adjacency list and an adjacency
matrix. Compute the memory each uses. Then compute the same for 1,000,000 vertices with 20
edges each.

**20.** Implement BFS and DFS over an adjacency list. Use BFS to find the shortest path between
two vertices, and DFS to detect a cycle.

**21.** Build a 100,000-character string in a loop using `+=`, then using join. Measure both.
Explain why one is quadratic in terms of immutability and copying.

**22.** Given 100,000 words, answer "how many start with 'pre'?" using a sorted list with
binary search, and then using a dict. Explain why the dict cannot help at all, and what
structure would.

---

## Break it

`break` gates. Predict every outcome in writing first.

**B1.** Insert integers `1..10000` in sorted order into a BST implementation (yours, or a
minimal one). Measure the height. Compare with `log2(10000) ≈ 13.3`. Explain what a balanced
variant would fix and roughly how.

**B2.** Fill a dict to just below its resize threshold, then insert one more item and time that
single insertion against the average. Find the spike.

**B3.** Take exercise 13's colliding keys further: 100,000 of them. Measure lookup time and
plot it against the number of keys inserted. Explain the curve you get.

**B4.** Allocate a list of 100,000,000 integers, or as many as your machine allows. Observe
what happens as memory runs out — the order of events matters. Then compute the per-item
overhead your language imposes and compare with a raw byte array.

**B5.** Write a recursive tree traversal and run it on a degenerate tree of depth 100,000.
Explain the failure, then convert it to an iterative traversal with an explicit stack.

---

## Measure and explain

`benchmark` and `explain` gates. Write these up properly; they are the deliverables.

**M1.** Measure hash-table lookup time at load factors 0.3, 0.5, 0.7, 0.9, and 0.99. Plot it.
Identify the knee. Explain why implementations resize around 0.7 rather than 0.9.

You will need your own hash table for this — your language's resizes automatically and will not
let you hold a high load factor. This is the strongest argument for doing the
[project](../../../projects/ds-from-scratch/README.md).

**M2.** Traverse a contiguous array of 10,000,000 integers and sum them. Then traverse a linked
list of the same 10,000,000 integers. **Predict the ratio.** Measure. Explain the gap using
cache blocks and prefetching.

Most people predict 1–2×. The real answer is often 5–20×. If your prediction was 1×, you have
just learned the most valuable thing in this topic.

**M3.** Write up, in two paragraphs each:

- Why amortised O(1) append is not the same as O(1) append, using your graph from exercise 5.
- Why a hash table is O(1) average and O(n) worst case, and what makes the worst case reachable
  in practice rather than only in theory.

**M4.** Explain to a peer why a hand-written structure with the same complexity as a built-in is
much slower. Name a mechanism. If you cannot name one, you are not finished.

---

## Answers to check yourself

<details>
<summary>Expand after attempting</summary>

**1.** Leaderboard: hash map for scores plus a size-10 heap (or a sorted structure) for the top
— rejected sorting everything, which is O(n log n) per update. Spellchecker: set — rejected a
sorted list with binary search, which is O(log n) instead of O(1) and no simpler. Autocomplete:
trie — rejected hash map, which cannot do prefixes at all. Undo: stack, i.e. a dynamic array —
rejected a linked list, which has worse locality and no benefit here. Banned IPs: set, or a
Bloom filter in front if the set is huge and false positives can be re-checked. Phone book:
sorted structure or tree-backed map — rejected hash map, which cannot answer range queries.
Job queue: heap — rejected a sorted list, whose insertion is O(n). **100 million records: not
an in-memory structure problem** — external sort, or a database, or a Bloom filter plus disk
verification.

**2.** For ~30 items the array often wins, because 30 contiguous integers fit in a couple of
cache blocks, while a hash table costs a hash computation plus a scattered access. The exact
crossover depends on key type and language, which is why the exercise says measure.

**8.** Roughly the same, and that is the point: a hit and a miss both cost one hash plus a
small number of probes. This is a property people find surprising and it is why negative
caching is useful.

**9.** List version O(n²), set version O(n). At 1,000 the difference is small; at 100,000 the
list version is roughly 100× worse. The *shape*: 100× the input made the list version 10,000×
slower and the set version 100× slower.

**11.** The object's hash changed after insertion, so lookup computes a different slot. The
entry is still in the table and permanently unreachable. Python raises `TypeError` for lists
specifically to prevent this; a custom class with a mutable-field hash will not be protected.

**14.** 1,000 items ≈ 10 comparisons; 1,000,000 ≈ 20. A thousandfold increase costs ten more
steps, which is what logarithmic means and is worth seeing rather than being told.

**19.** 8 vertices: list ≈ 8 + 2E entries; matrix = 64 booleans. The matrix is competitive at
this size. 1,000,000 vertices × 20 edges: list ≈ 2×10⁷ entries; matrix = 10¹² booleans, which
is a terabyte at one byte each. Not close.

**22.** A dict hashes the whole key, so it cannot find keys by prefix — hashing destroys exactly
the structure a prefix query needs. Binary search on a sorted list works (find the first match,
scan forward). A trie is the purpose-built answer.

**B1.** Height 10,000, not 13. Sorted insertion always goes right, producing a linked list.
Balancing rotates subtrees during insertion to keep height at O(log n).

**B4.** Order of events: memory fills, the OS starts swapping to disk, everything slows
dramatically, and eventually the process is killed. Per-item overhead: a Python integer object
is ~28 bytes plus 8 for the list's pointer, versus 4 or 8 for a raw array element — roughly a
4–9× difference, which is why numeric work uses array libraries.

**M2.** Typically 5–20×. Same operation count, same complexity. The array lets the CPU prefetch
the next block while it works on the current one; the linked list's next address is unknowable
until the current node is read, so every step risks a full memory latency.

**M4.** Acceptable mechanisms: the built-in is compiled C rather than interpreted; it stores
values contiguously rather than as pointers to boxed objects; it has a specialised fast path for
common key types; it avoids per-object allocation overhead. "It's optimised" is not a mechanism.

</details>

---

## Next

[projects.md](projects.md) — build them from scratch, and measure.
