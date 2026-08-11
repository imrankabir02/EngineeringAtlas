# Data structures — practical

What your language actually gives you, how to choose under real constraints, and how to
measure so the numbers mean something.

[← Data structures](README.md) · [Fundamentals](fundamentals.md) ·
[Concepts](concepts.md) · [Exercises](exercises.md)

---

## What you already have

You will rarely implement these professionally. Knowing precisely what your standard library
provides — and what it guarantees — is the practical skill.

| Concept | Python | JavaScript | Java | Go | C++ |
|---|---|---|---|---|---|
| Dynamic array | `list` | `Array` | `ArrayList` | slice | `vector` |
| Hash map | `dict` | `Map`, `{}` | `HashMap` | `map` | `unordered_map` |
| Ordered map (tree) | — | — | `TreeMap` | — | `map` |
| Set | `set` | `Set` | `HashSet` | `map[T]struct{}` | `unordered_set` |
| Deque | `collections.deque` | `Array` (poorly) | `ArrayDeque` | slice (manually) | `deque` |
| Heap | `heapq` | — | `PriorityQueue` | `container/heap` | `priority_queue` |
| Counter | `collections.Counter` | — | — | — | — |

Two things to notice, because both cause real bugs:

**Python and Go have no built-in ordered map.** If you need sorted iteration you sort the keys
each time (O(n log n) per iteration) or use a third-party sorted container. Discovering this
after building on the assumption is unpleasant.

**JavaScript has no built-in heap.** Priority-queue problems require an implementation or a
dependency.

### What is actually guaranteed

Read your language's documentation, not folklore. Some specifics that matter:

- **Python `dict` preserves insertion order** — a language guarantee since 3.7, not an
  implementation detail. `set` does **not**, and code that appears to work because a small set
  happens to iterate in a convenient order will break later.
- **JavaScript object keys** have complicated ordering rules (integer-like keys sort
  numerically and come first). Use `Map` when order matters.
- **Java `HashMap`** converts a bucket to a tree once it holds 8 colliding entries,
  specifically to bound the adversarial worst case at O(log n) instead of O(n). This is
  documented, and it is a good example of a real implementation defending against the attack
  described in [fundamentals.md](fundamentals.md#the-worst-case-is-reachable).
- **Go map iteration order is deliberately randomised** on every iteration, to stop you
  depending on it. An unusually honest design decision.

Reading these guarantees is the Tier 1 habit from
[resource-tiers.md](../../../docs/resource-tiers.md), applied to something you use daily.

---

## Choosing, in practice

The method, in order. Do not skip to the table.

### 1. Write down the operations and their frequencies

Not "I need a collection of users." Something like:

```text
- look up a user by ID          ~10,000/sec    ← critical path
- add a user                    ~10/sec
- iterate all users             ~1/hour        (a report)
- list users sorted by name     ~100/sec       ← also matters
```

The frequencies do the deciding. Lookup by ID at 10,000/sec says hash table. Sorted-by-name
at 100/sec says you need order too — so either a second index (a sorted list of names, kept
up to date) or a tree-backed map. Two structures, because no single one gives both.

### 2. Establish the realistic scale

Not today's scale. The scale where this code still has to work.

- **Under ~100 items:** almost any structure is fine. Choose for readability. Do not optimise.
- **Thousands:** structure choice starts showing up in profiles.
- **Millions:** structure choice dominates, and memory becomes a constraint of its own.
- **Beyond memory:** you are no longer choosing a data structure, you are choosing a
  database. Go to `databases-introduction` and `indexing-and-query-optimization`.

That last row is a real and frequently missed transition. A hash table that does not fit in
RAM is not a hash table problem.

### 3. Ask three questions

- **Do I need order?** If yes, a hash table alone is insufficient.
- **Do I need uniqueness?** If yes, a set says so in the code as well as enforcing it.
- **Do I look up by key or scan?** If by key, hash. If scanning anyway, an array's locality
  usually wins.

### 4. Then choose, and write down why

The choice belongs in a comment or a design note, because the next person — including you —
will otherwise assume it was arbitrary and change it.

```python
# Hash map keyed by user id: lookup is on the request path (~10k/s).
# A second sorted index on name serves the directory page; names change
# rarely enough that maintaining it on write is cheaper than sorting on read.
```

---

## Common mistakes, with their symptoms

These are the ones that actually appear in real code.

### A list where a set belongs

```python
if user_id in seen_users:        # seen_users is a list -- O(n) scan
    continue
seen_users.append(user_id)
```

Inside a loop over the same data this is O(n²). Correct at 100, unusable at 100,000.

**Symptom:** fast in tests, times out in production. The most common performance bug at
Level 2, and the reason exercise 22 in [exercises.md](exercises.md) exists.

**Fix:** a set. One character of thought, orders of magnitude of difference.

### String concatenation in a loop

```python
result = ""
for row in rows:
    result += format(row)        # O(n^2) -- new string every time
```

Strings are immutable, so each `+=` allocates and copies everything so far.

**Symptom:** slow with large inputs, and profiles blame string operations that look innocent.

**Fix:** collect into a list and `join` once, or use your language's builder.

### Sorting inside a loop

```python
for item in items:
    ranked = sorted(scores)      # sorts the whole thing every iteration
```

**Fix:** sort once outside the loop, or keep the collection sorted, or use a heap if you only
need the extremes.

### Rebuilding a lookup structure repeatedly

```python
for order in orders:
    user = next(u for u in users if u.id == order.user_id)   # scans users, every order
```

**Fix:** build a dict once before the loop. This turns O(n×m) into O(n+m), and it is probably
the single highest-value refactor you will apply in your career, because the bad version reads
perfectly naturally.

### Premature structure optimisation

Writing a custom structure for 50 items, or reaching for a trie when a dict would do.

**Symptom:** code that is hard to read and no faster, with a comment claiming it is optimised.

**Fix:** measure first. Below a few hundred items the difference is unmeasurable, and
readability is the property that actually pays.

---

## Measuring properly

Complexity analysis narrows the candidates. Measurement decides. But bad measurement is worse
than none, because it produces confident wrong conclusions.

### The rules

**Predict first, in writing.** The gap between prediction and result is the whole value.
Write the number down and do not edit it afterwards.

**Exclude warm-up.** The first iterations pay for JIT compilation, cache warming, and
allocator growth. Run a few thousand throwaway iterations first.

**Report percentiles, not means.** For a dynamic array, the mean hides the resize spikes,
which are the interesting part. Report p50, p95, p99, max.

**Use realistic data.** Uniformly random keys flatter every hash table. Real keys are
clustered and skewed — a Zipfian distribution is a much better model of real access patterns,
and it changes conclusions.

**Change one variable.** Otherwise you have an anecdote.

**Record the setup.** Language version, machine, data size and shape, iteration count. A
measurement you cannot reproduce is a claim.

**Measure at two sizes at least.** One measurement tells you a speed. Two tell you a *shape*,
and the shape is what predicts behaviour at a size you have not tried.

### A minimal harness

```python
import time, random, statistics

def measure(fn, arg, warmup=1000, runs=10000):
    for _ in range(warmup):
        fn(arg)
    samples = []
    for _ in range(runs):
        start = time.perf_counter_ns()
        fn(arg)
        samples.append(time.perf_counter_ns() - start)
    samples.sort()
    return {
        "p50": samples[len(samples) // 2],
        "p95": samples[int(len(samples) * 0.95)],
        "p99": samples[int(len(samples) * 0.99)],
        "max": samples[-1],
    }
```

Use `perf_counter_ns` or your language's monotonic high-resolution clock, never wall-clock
time. Beware measuring an operation so fast that timer overhead dominates — if a single call
is a few nanoseconds, time a batch of them and divide.

### Where to look when you are wrong

You will predict wrong. The usual reasons, in order of frequency:

1. **Locality.** Your scattered structure lost to a contiguous one despite better complexity.
2. **Constant factors.** The built-in is written in C, yours in the host language.
3. **The input was too small.** Asymptotic behaviour needs enough n to show up.
4. **You measured something else.** Setup cost, allocation, or the timer.
5. **Your data was unrealistic.** Uniform random when real keys are skewed.

Working out which one applies is the actual skill, and it is what
`performance-engineering` at Level 4 formalises.

---

## Reading a real implementation

A `review` gate: read a standard library structure and find one decision that trades memory
for speed.

Good targets, in increasing difficulty:

- **CPython `Objects/dictobject.c`** — read the long header comment on compact dicts, not the
  whole file. It explains a real space-versus-time decision in the words of the people who
  made it.
- **Java `HashMap`** source — find `TREEIFY_THRESHOLD` and work out why the number is 8.
- **Go `runtime/map.go`** — read the comment block at the top on bucket layout and the
  reasoning about cache lines.

Do not try to understand all of it. Pick one question — *how does it decide when to resize?* —
and answer only that. That approach is the whole method of `reading-source-code` at Level 4,
and starting it here on a structure you understand is the cheapest possible introduction.

---

## When you outgrow in-memory structures

Worth naming explicitly, because it is a transition people miss.

If your data does not fit in memory, or must survive a restart, or must be shared between
processes, **you no longer have a data structure problem.** You have a database problem, and
the answer is a database — which is data structures on disk with a query language and
durability guarantees.

The mapping is direct and knowing it makes databases much less mysterious:

| In memory | On disk |
|---|---|
| Hash table | Hash index |
| Balanced tree | B-tree index (the default in every relational database) |
| Sorted array | Clustered index / sorted file |
| Append-only list | Write-ahead log, LSM tree |

Every one of those is in `indexing-and-query-optimization` and
`database-internals`. When you get there, you will be learning where the structures live, not
what they are — which is why this topic is a prerequisite for both.

---

## Next

[exercises.md](exercises.md) — drills including the measurement ones, then
[projects.md](projects.md).
