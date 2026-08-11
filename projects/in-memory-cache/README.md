# In-memory cache with eviction

**Level 3** · validates [`caching`](../../topics/backend/caching/README.md)
· any language with threads or an event loop

Build a cache library — LRU eviction in O(1), TTLs, thread safety, metrics — put it
in front of something real, and then break it on purpose.

**Constraints:** no third-party cache library, and both `get` and `put` must be O(1).
The eviction logic *is* the project. A dictionary with no eviction is a memory leak
with good latency.

---

## Why this project exists

Everyone has used a cache. Almost nobody has watched one fail.

This project makes you cause the three failures that define the topic:

1. **A stampede** — 500 concurrent misses on one cold key, all reaching the origin
   at once, at the worst possible moment.
2. **A stale read** — the cache serving a value that is no longer true, and you
   measuring exactly how long the lie lasts.
3. **A useless cache** — a hit ratio so low that the cache is pure overhead, which
   teaches you that "add a cache" is a hypothesis, not a solution.

The other half of the project is measurement. Caching is the topic where intuition
fails hardest: everyone believes their cache helps, and the number is often
disappointing until the key distribution is understood. You will predict every
result and record how wrong you were.

---

## Stage 1 — Correct

A fixed-capacity cache with LRU eviction, single-threaded.

### The O(1) requirement

The naive design stores an access timestamp per entry and scans to find the oldest.
That is O(n) per eviction and it is exactly what the constraint forbids.

The standard solution combines two structures:

```text
hash map:      key -> node          O(1) lookup
doubly linked list: MRU <-> ... <-> LRU   O(1) move-to-front, O(1) evict-from-tail
```

On `get`: look up the node in the map, unlink it, push it to the head. All O(1)
because the map hands you the node directly — no traversal.
On `put` past capacity: drop the tail node and remove its key from the map.

The insight worth carrying forward: **you needed two structures because neither
alone provides both fast lookup and fast ordering.** That combination — a map for
identity plus a list for order — recurs throughout systems engineering.

Your dynamic array and hash table from
[`ds-from-scratch`](../ds-from-scratch/README.md) are exactly the prerequisites
here. You may use built-ins for the map at this level; the eviction structure is
what must be yours.

### Tests that actually discriminate

| Case | Why it catches bugs |
|---|---|
| Capacity 1, two alternating keys | Every access evicts; exposes ordering errors immediately |
| Capacity 0 | Should either reject construction or never store. Decide and document |
| Update an existing key at capacity | Must not evict anything — it is a replacement, not an insertion |
| Get an evicted key | Must be a miss, and the entry must be gone from *both* structures |
| Get then put then get | Verifies `get` counts as a use for ordering purposes |

That last one is the classic bug: implementing `get` without moving the node makes
it an insertion-order cache, not an LRU. Write a test that asserts **which** key
was evicted, not merely that eviction happened.

---

## Stage 2 — Expiring

Time-based invalidation: an entry can be resident and still wrong.

**Lazy versus active expiry** — decide, and write down what you accepted:

- **Lazy**: check the TTL on read; expired entries are misses. Cheap, but a key
  written once and never read again occupies memory forever.
- **Active**: a background sweep removes expired entries. Reclaims memory, costs a
  thread and adds contention with readers.

Real caches do both. Redis samples keys randomly for active expiry rather than
scanning, because scanning a large keyspace blocks a single-threaded server —
a detail worth understanding, because it is a design constraint leaking into an API.

**Inject the clock.** Do not use `sleep` in expiry tests:

```text
cache = Cache(capacity=10, clock=FakeClock())
cache.put("k", "v", ttl=60)
clock.advance(61)
assert cache.get("k") is MISS
```

A test suite with sleeps is slow, flaky, and will be deleted by whoever inherits it.
Injecting the clock is a testability technique you will reuse constantly.

---

## Stage 3 — Concurrent

**Requirement: you must produce the broken version first.**

Run 8 threads doing mixed `get` and `put` against a cache with no synchronisation,
capacity 100, over a small key space. Then assert an invariant afterwards — that the
linked list length equals the map size, and that the list has no cycles.

It will fail. Then explain *why*, by naming the interleaving:

> Thread A unlinks node X to move it to the head. Between updating `X.prev.next` and
> `X.next.prev`, thread B traverses from the tail. B follows a pointer into a node
> that is half-unlinked, and the list is now corrupt — or cyclic, in which case a
> later traversal never terminates.

Then add synchronisation and show the test passing. Keep both versions in the
repository, with the broken one skipped by default. It is the most valuable artifact
you will produce here, and it is the difference between knowing that locks are
necessary and knowing what they prevent.

**Lock scope.** Start with one lock around the whole cache. Then justify it: the
linked list is a single shared structure, so per-entry locks do not help — every
`get` mutates the list head. This is why sharded caches exist: split into N
independent caches by key hash, each with its own lock, and contention drops by
roughly N. Note that this changes eviction semantics (each shard evicts
independently) — a real trade-off, and exactly the kind that
[`architecture-tradeoffs`](../../docs/levels.md) is about.

---

## Stage 4 — Measured

### Front something real

The origin must have real cost — a Postgres query, a file read, or an HTTP call with
injected latency. A stub returning a constant makes every number meaningless,
because there was nothing to avoid.

Simplest honest setup: an origin function that sleeps 20 ms and increments a counter.
The counter is how you measure stampedes.

### Predict, then measure

Write down, before running:

- p50 and p99 on the hit path
- p50 and p99 on the miss path
- hit ratio with 10,000 keys, 100,000 requests, uniform random
- the same with a Zipfian distribution (skew ~1.0)

Then measure, reporting **p50, p95, p99** for hit path, miss path, and cache
disabled. Exclude warm-up. Record the setup in the output.

### The result that teaches the most

Uniform random keys over a keyspace much larger than the cache gives a hit ratio
close to `capacity / keyspace` — with 1,000 slots and 10,000 keys, roughly 10%. Your
cache is nearly useless and you added a failure mode.

Switch to a Zipfian distribution — where a few keys are requested far more often,
which is what real traffic looks like — and the same cache reaches 80–90%.

**The cache did not change. The workload did.** That is the central lesson: a cache's
value is a property of the access distribution, not of the cache. It is why "should
we add a cache?" is answered by measuring your key distribution, and why a cache
that works in staging (uniform synthetic load) can be worthless in production, or
the reverse.

---

## Stage 5 — Broken and understood

### The stampede

Cold cache. 500 concurrent requests for the same key.

Measure origin calls. You will see 500 — every request misses, and every one goes to
the origin, because nothing coordinates them. On a real system this is how a cache
restart takes down the database it was protecting.

Then implement one mitigation and measure it:

| Mitigation | Mechanism | Cost |
|---|---|---|
| **Single-flight** | First miss takes a per-key lock; others wait for its result | One origin call; waiters block, and a slow origin now blocks many requests |
| **Stale-while-revalidate** | Serve the expired value; refresh in the background | No latency spike; you knowingly serve stale data |
| **Jittered TTLs** | Randomise expiry so keys do not expire together | Prevents *mass* expiry, does nothing for a single hot key |

Single-flight should take you from 500 origin calls to 1. Get the graph.

### The stale read

Write directly to the datastore, bypassing the cache. Then read through the cache
and record how long the wrong value is served.

The answer is "until the TTL expires", which is the honest cost of caching, and it
is why every cache design must answer: *who invalidates, and what happens between
the write and the invalidation?*

Write up the mechanism. This is the `explain` gate.

### The cold restart

Restart the process under load. Measure origin latency during recovery. This is the
same shape as the stampede but system-wide, and it is why production caches are
warmed before receiving traffic.

### The wrong limit

Store values large enough to exhaust memory while staying under the entry-count
capacity. Discover that capacity-by-count was the wrong limit for variable-size
values, and that real caches bound by bytes. Then decide what yours does.

---

## Done when

- [ ] `get` and `put` are O(1) and you can point at why.
- [ ] Eviction-order tests assert *which* key was evicted.
- [ ] TTL tests use an injected clock, no sleeps.
- [ ] A concurrency test fails without the lock and passes with it, both preserved.
- [ ] You can name the interleaving that corrupts the list.
- [ ] Benchmark reports p50/p95/p99 with warm-up excluded and setup recorded.
- [ ] Hit ratio measured under uniform *and* Zipfian, with the difference explained.
- [ ] You have a stampede graph, a mitigation, and its measured effect.
- [ ] You have a written stale-read analysis.
- [ ] Predictions recorded before measurement, unedited.

---

## Anti-patterns

**A dictionary with no eviction.** Not a cache. A memory leak that gets faster.

**Scanning for the LRU entry.** O(n) eviction defeats the purpose and violates the
constraint.

**Sleeps in tests.** Slow, flaky, and the reason nobody trusts the suite.

**A stub origin.** Removes all cost from a miss, so every measurement is fiction.

**Reporting means.** Cache latency is bimodal by construction — hits and misses are
different populations. A mean describes neither.

**Testing only hits.** The miss path under concurrency is where the bugs live.

---

## Stretch

- **A second eviction policy** (LFU, or a small ARC) compared on the same Zipfian
  workload. LFU usually wins on skewed traffic and loses badly when the popular set
  shifts — a real trade-off you can now measure.
- **Negative caching** for missing keys. Then find the bug it introduces the moment
  the key is created, and decide how to fix it.
- **Distribute it** across two processes with consistent hashing. Remove a node and
  measure how many keys move. Then compute what modulo hashing would have moved. That
  difference is why consistent hashing exists.
- **Stale-while-revalidate**, and a precise written statement of the guarantee you
  gave up.

---

## Next

Return to [`caching`](../../topics/backend/caching/README.md) for the gates. Then
[`url-shortener`](../url-shortener/README.md), which puts this cache into a complete
system, or `message-queues-and-streaming` for the next tool for shedding origin load.
