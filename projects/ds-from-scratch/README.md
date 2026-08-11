# Data structures from scratch

**Level 2** · validates
[`data-structures`](../../topics/computer-science/data-structures/README.md)
· any language with fixed-size arrays

Implement four structures from primitives, then benchmark them against your
language's built-ins and explain every difference you measure.

**The constraint: no built-in dynamic list, dictionary, set, or sorted container
inside your implementations.** You get fixed-size arrays and objects. That is what
the built-ins were built from, and building on them is how the trade-offs become
real rather than memorised.

---

## Why this project exists

You can already use a hash table. Your language has one and it is better than
anything you will write here — faster, more tested, written in C.

That is not the point. The point is that after this project you will know:

- **why** a hash table is O(1) on average and what makes it stop being O(1)
- **why** appending to a dynamic list is "amortised" O(1) and what the word costs
- **why** your BST becomes a linked list on sorted input, having watched it happen
- **why** the built-in beats your version by 20× even though the algorithm is
  identical — which is the most valuable lesson here, because it is where you learn
  that Big-O is a prediction about growth, not about speed

The final stage is where the learning concentrates: **predict every benchmark
result before measuring.** Your wrong predictions are the deliverable.

---

## Stage 1 — Dynamic array

A list that grows, built on fixed-size arrays.

The invariant: you hold an array of `capacity`, and `size` slots are in use. When
`size == capacity`, allocate a bigger array and copy.

**How much bigger?** Try `capacity + 1` first. Append a million items and time it.
Then switch to `capacity * 2` and do it again. The difference is dramatic and you
should be able to explain it before you look up the answer.

The reason: with `+1`, appending n items copies 1 + 2 + ... + n items in total,
which is O(n²). With `*2`, each item is copied at most a constant number of times
on average, giving O(n) total and **amortised O(1)** per append. "Amortised" means
individual appends are occasionally expensive — the ones that resize — but the
average over any sequence is constant.

Do not accept that from this document. Measure the per-append latency over a million
appends and look at the spikes. You will see them at powers of two, each one twice
as tall as the last and half as frequent. That picture is what "amortised" means.

Implement: `append`, `get(i)`, `set(i, v)`, `insert(i, v)`, `delete(i)`, `len`.
State the complexity of each in a comment. Note that `insert(0, v)` is O(n) and
`append` is O(1) — this asymmetry is why arrays and linked lists both exist.

---

## Stage 2 — Hash table

The structure that makes the rest of your career possible.

The idea: a function maps a key to an array index, so lookup is one computation and
one array access instead of a scan. The complication: two keys can map to the same
index.

**Collision handling** — implement one, be able to describe the other:

| Strategy | How | Trade-off |
|---|---|---|
| **Chaining** | Each slot holds a list of entries | Simple, degrades gracefully, poor cache locality |
| **Open addressing** | On collision, probe for the next free slot | Better cache locality, but deletion needs tombstones and it degrades sharply near full |

Implement `insert`, `lookup`, `delete`, and iteration. **Test deleting a key that
collided with another** — this is where most hand-written hash tables are broken, and
with open addressing a naive delete makes other keys unreachable.

**Resizing.** When the load factor (`size / capacity`) crosses a threshold, allocate
a larger array and **rehash every key** — indices depend on capacity, so you cannot
copy slots across. Verify with a test that inserts 10,000 keys, forces several
resizes, and confirms every key is still findable.

**The measurement that matters.** Time lookups at load factors 0.3, 0.7, 0.9, and
0.99. Plot it. The curve is flat and then it is not. That knee is why real hash
tables resize at around 0.7 rather than waiting until full, and it is the concrete
version of "O(1) on average".

Then make it degrade on purpose: construct 100,000 keys that all hash to the same
slot. Lookup becomes O(n). Your "O(1)" structure is now a linked list. This is not
hypothetical — it is a real denial-of-service technique against web frameworks that
hash user-supplied keys, which is why languages added hash randomisation.

---

## Stage 3 — Binary search tree

Ordered operations: find, plus find-the-next-largest, plus in-order traversal.

The invariant: for every node, everything in the left subtree is smaller and
everything in the right is larger. Every operation must preserve it.

Implement `insert`, `search`, `delete`, and in-order traversal. Delete has three
cases — leaf, one child, two children — and the two-child case (replace with the
in-order successor) is the one people skip. Do not skip it.

**Then break it deliberately:** insert `1, 2, 3, ..., 10000` in order. Measure the
tree's height. It is 10,000, not 14. You have built a linked list with extra
pointers and worse cache behaviour, and searching it is O(n).

This is the entire motivation for balanced trees (AVL, red-black) and for the
B-trees your database uses. You do not have to implement one, but you must be able to
say what it fixes and roughly how — because "sorted insertion order" is not an exotic
input, it is what happens when you insert records by timestamp or auto-increment ID.

---

## Stage 4 — Binary heap

A priority queue: get the smallest element fast, without keeping everything sorted.

The invariant: every parent is smaller than its children — weaker than a BST's
invariant, and that weakness is what makes it cheap to maintain. Stored in a flat
array, where node `i` has children at `2i+1` and `2i+2`; no pointers at all, which
is excellent for cache locality.

Implement `push`, `pop`, `peek`, and `heapify` from an existing array. Check the
invariant in a test after every operation — the sift-up and sift-down loops are easy
to get subtly wrong.

**`heapify` is O(n), not O(n log n).** Work out why before looking it up. The hint:
most nodes are near the bottom, and nodes near the bottom sift down a very short
distance. Being able to derive this is a real complexity-analysis exercise, unlike
reciting the result.

Then use it for something: find the 10 largest values in a 10-million-element stream
using a heap of size 10. Sorting the whole stream would be O(n log n) and require it
all in memory; the heap is O(n log 10) and holds ten items. That contrast is why heaps
exist.

---

## Stage 5 — Benchmark and explain

The most important stage.

**Predict first, in writing.** For each structure, how much slower than the built-in
will yours be? 2×? 10×? 100×? Commit to numbers.

Then measure, with discipline:

- **Exclude warm-up.** JIT compilation, cache warming, and allocator behaviour all
  make the first iterations unrepresentative.
- **Report p50 and p99,** never a mean. For the dynamic array especially, the mean
  hides the resize spikes, and the spikes are the interesting part.
- **Record the setup:** machine, language version, data size, key distribution.
- **Use realistic key distributions.** Uniform random keys flatter every hash table.
  Real keys are skewed, clustered, and sometimes adversarial.
- **One variable at a time.**

Then write the analysis. Expect your implementations to be considerably slower, and
explain each gap. The usual causes:

- The built-in is implemented in C, yours in the host language.
- The built-in exploits memory layout: contiguous storage, fewer pointer hops,
  fewer cache misses. Same asymptotic complexity, much better constants.
- Your objects have per-object overhead the built-in avoids.
- The built-in has a specialised fast path for common key types.

**"The built-in is faster" is not the finding. Why it is faster is the finding.** If
your analysis does not name a mechanism, keep going.

---

## Break it

1. **100,000 colliding keys** into the hash table. Measure. Explain the shape.
2. **Sorted insertion** into the BST. Measure the height against `log2(n)`.
3. **Append latency over time** in the dynamic array. Graph it; identify the spikes.
4. **A mutable object as a hash key.** Insert it, mutate it, look it up. It has
   vanished — it is in the bucket for its old hash. This is why keys should be
   immutable, and it is a bug you will otherwise meet in production.
5. **Grow the heap** until memory pressure is visible. Observe what the allocator
   and the OS do as you approach the limit.

---

## Done when

- [ ] All four structures pass tests, including hash-table deletion under collision
      and BST deletion with two children.
- [ ] Each operation has a stated complexity and a test or measurement supporting it.
- [ ] You can explain "amortised O(1)" using your own graph.
- [ ] You have the load-factor curve and can explain the knee.
- [ ] Benchmark report has p50/p99, a recorded setup, and predictions made beforehand.
- [ ] Your written analysis names a *mechanism* for every gap against the built-ins.

---

## Anti-patterns

**Wrapping the built-in.** If your dynamic array holds a Python `list` or a JS
`Array`, there is no project here.

**Copying an implementation.** Work from the invariant. Slower, and it is the only
version that produces understanding.

**Uniform random keys only.** Every hash table looks good on uniform keys.

**Reporting means.** The dynamic array's cost distribution is the lesson.

**Stopping at "the built-in wins".** That was known in advance. The mechanism is the
deliverable.

---

## Stretch

- Implement **open addressing** as well as chaining, then compare at load factor
  0.9. Open addressing usually wins on cache locality until it suddenly does not.
- Add an **AVL or red-black tree** and measure the height on sorted input against
  your plain BST.
- Implement a **trie** and compare with your hash table for prefix queries — a case
  where hashing simply cannot compete.
- Implement a **Bloom filter** and measure the false-positive rate against the
  theoretical prediction. Your first probabilistic data structure, and the entry
  point to how databases avoid pointless disk reads.

---

## Next

Return to [`data-structures`](../../topics/computer-science/data-structures/README.md)
for the gates. Then `algorithms`, or jump to
[`caching`](../../topics/backend/caching/README.md), where your hash table becomes
the core of something real.
