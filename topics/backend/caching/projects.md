# Caching — projects

[← Caching](README.md) · [Exercises](exercises.md) ·
[Interview](interview.md)

---

## Core project

### [In-memory cache with eviction](../../../projects/in-memory-cache/README.md)

**Level 3** · validates `locality`, `eviction`, `invalidation`, `stampede`,
`measuring-caches`

A cache library — O(1) LRU, TTLs, thread safety, metrics — placed in front of something with real
cost, then deliberately broken.

**Constraints:** no third-party cache library; both `get` and `put` must be O(1); it must front a
real datastore rather than a stub.

---

### Why this project

Everyone has used a cache. Almost nobody has watched one fail. This project makes you cause the
three failures that define the topic, in an environment where the consequences are yours and
cheap.

**The stampede.** 500 concurrent misses on one cold key, all reaching the origin at once. You
will see 500 origin calls, add single-flight, and see 1. That before-and-after graph is the most
convincing artifact you will produce in this topic, and it is a real production failure mode
reproduced on your laptop.

**The stale read.** Write to the datastore directly, read through the cache, and measure how long
the wrong value is served. Reading "caches can be stale" is a fact; watching your own system lie
for 300 seconds and knowing exactly why is understanding.

**The useless cache.** Measure the hit ratio under a uniform key distribution and find it near
10%. Switch to a Zipfian distribution and find 90%. **The cache did not change.** That single
comparison is the most valuable thing in the topic, because it converts "add a cache" from a
reflex into a hypothesis about your workload.

The fourth thing the project gives you is the O(1) requirement. The naive implementation stores a
timestamp per entry and scans to find the oldest — O(n) per eviction. Getting to O(1) forces the
hash-map-plus-doubly-linked-list combination, and the insight generalises far beyond caching:

> You needed two structures because neither alone provides both fast lookup and fast ordering.

That pattern — combining structures because no single one has all the properties you need —
recurs constantly at Level 3 and above. Your work in
[`data-structures`](../../computer-science/data-structures/README.md) is exactly the preparation.

---

## The stages, and what each is for

Full specification in the
[project README](../../../projects/in-memory-cache/README.md). What each stage teaches:

| Stage | The lesson |
|---|---|
| **Correct** | O(1) eviction, and tests that assert *which* key was evicted. The classic bug is a `get` that does not reorder, making it an insertion-order cache |
| **Expiring** | Lazy versus active expiry, and clock injection instead of `sleep` — a testability technique you will reuse for years |
| **Concurrent** | You must produce the **broken version first** and name the interleaving that corrupts the list. Both versions stay in the repository |
| **Measured** | Percentiles, warm-up exclusion, and the uniform-versus-Zipfian comparison |
| **Broken and understood** | The stampede, the mitigation, the stale-read write-up |

**Stage 3 deserves emphasis.** The requirement is not "make it thread-safe" — it is *demonstrate
the race, then fix it*. Run 8 threads with no synchronisation and assert afterwards that the
linked list length matches the map size and the list has no cycles. It will fail. Then explain
why:

> Thread A unlinks node X to move it to the head. Between updating `X.prev.next` and
> `X.next.prev`, thread B traverses from the tail, follows a pointer into a half-unlinked node,
> and the list is now corrupt — or cyclic, in which case a later traversal never terminates.

Keeping the broken version, skipped by default, is the most valuable artifact in the project. It
is the difference between knowing that locks are necessary and knowing what they prevent.

**Do not skip stages 4 and 5.** A working LRU with no measurements and no induced failures is a
Level 2 exercise. The measurement and the deliberate breakage are what make it Level 3.

---

## Stretch project

### [URL shortener](../../../projects/url-shortener/README.md)

**Level 3** · validates `hit-ratio`, `caching-patterns`, `cache-key-design`

A complete read-heavy service: ID generation, redirects, caching, analytics, rate limiting, and a
load test that finds its saturation point.

**Why it follows well:** the cache project teaches caching in isolation. This one puts a cache
inside a system that has other problems — a database, concurrency on a counter, abuse, and a
capacity limit — so you have to decide where the cache belongs and justify it against a measured
baseline.

Two specific pay-offs:

- **You measure without a cache first**, then with. That baseline discipline is what makes a
  caching claim credible, and it is skipped almost universally.
- **The two-instance stretch goal** — run it behind a load balancer — reveals every piece of state
  that quietly stopped working: your in-process cache is now two divergent caches, your in-memory
  rate limiter allows 2× the limit, and your buffered counter has two buffers. It is the best
  possible introduction to `distributed-systems-fundamentals`.

---

## What "done" means

Full checklist in the
[project README](../../../projects/in-memory-cache/README.md#done-when). The five that matter
most:

1. **The stampede graph exists** — origin calls before and after the mitigation.
2. **The uniform-versus-Zipfian hit-ratio comparison exists**, with predictions recorded
   beforehand.
3. **The concurrency test fails without the lock and passes with it**, and both versions are
   preserved.
4. **You can name the interleaving** that corrupts the list, in a sentence.
5. **The origin is real.** A stub returning a constant invalidates every measurement, because
   there was no cost to avoid.

---

## Anti-patterns specific to these projects

**A dictionary with no eviction.** Not a cache. A memory leak that gets faster.

**Scanning for the LRU entry.** O(n) eviction violates the constraint and misses the lesson.

**A stub origin.** The most common way to produce a project that looks complete and measures
nothing.

**`sleep` in expiry tests.** Slow, flaky, and the reason nobody trusts the suite. Inject the
clock.

**Reporting mean latency.** Hits and misses are two populations; the mean describes neither.

**Testing only the hit path.** The miss path under concurrency is where the interesting failures
are.

**Skipping the broken concurrency version.** Adding a lock because you were told to is not the
same as adding one because you saw what happens without it.

---

## After the projects

Return to [`topic.yml`](topic.yml) for the remaining gates. Three deserve attention:

**The `explain` gate aimed at a product owner** — "what does 'up to 60 seconds stale' mean for
this feature", without using the word cache. This is harder than it sounds and it is real work:
staleness is a product decision, and someone non-technical has to understand and agree to it.
Engineers who can have that conversation get to make architectural decisions; engineers who
cannot have them made for them.

**The `design` gate** — a caching strategy for a page with live stock levels and slowly-changing
descriptions, including what you deliberately do *not* cache. The answer involves caching parts
of a page at different TTLs, which is a genuinely useful pattern and the entry point to
`system-design-fundamentals`.

**The `review` gate** — find one invalidation hazard and one missing measurement in a peer's
caching layer, or an open-source one. Evaluating someone else's cache is a different skill from
building yours, and it is the one that transfers into judgment.
