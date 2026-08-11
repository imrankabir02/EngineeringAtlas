# Caching — fundamentals

The full chain, from "why is this slow?" to Redis. Every step is a problem the next step
answers.

[← Caching](README.md) · [Concepts](concepts.md) · [Practical](practical.md)

---

## Step 0: measure, before anything else

The chain does not start with "add a cache." It starts with a question.

> Why is this request slow?

Answer it with a profiler or a trace, not with intuition. Engineers are consistently wrong
about where time goes — including experienced ones — which is why profilers exist.

This step is not a formality. It has a specific outcome: **you find out whether caching is the
right tool at all.** The three most common findings, and only one of them says "cache":

| Finding | Correct response |
|---|---|
| One query takes 4 seconds because it is missing an index | Fix the query. Caching it gives you a 4-second query that fires on every miss, at the worst moment |
| The endpoint makes 200 queries in a loop | Fix the N+1. A cache hides it until the cache is cold, then the collapse is worse |
| One reasonably fast query is called 50,000 times a second | **Now** consider a cache |

**Caching a slow query is the single most common misuse of this topic.** The query is still
slow; you have only arranged for fewer people to experience it, and for those who do to
experience it during a cache stampede when the system is already struggling.

---

## Step 1: some of that time is distance

From [`computer-basics`](../../foundations/computer-basics/README.md):

```text
                          time          relative to memory
  CPU cache               ~1-40 ns      much faster
  memory (RAM)            ~100 ns       1×
  local SSD               ~100 µs       ~1,000× slower
  network, same DC        ~500 µs       ~5,000× slower
  network, cross-region   ~100+ ms      ~1,000,000× slower
```

A database query from your application typically costs: a network round trip to the database,
query parsing and planning, one or more page reads (from the database's own buffer cache if
lucky, from disk if not), and a round trip back. Milliseconds, in the good case.

The same value held in your process's memory costs ~100 ns.

**That gap — three to five orders of magnitude — is the entire opportunity.** Everything else
in this topic is about whether you can safely take it.

---

## Step 2: locality is the precondition

Here is the property without which none of this works:

> **Some data is read far more often than it changes.**

This is called **locality of reference**, and it comes in two forms:

- **Temporal locality** — data accessed recently is likely to be accessed again soon. A user
  who loads their profile will probably load it again in the next minute.
- **Spatial locality** — data near recently accessed data is likely to be accessed. Reading
  record 100 suggests you may read 101.

Caching works *only* to the extent that your workload has locality. And the crucial
consequence, which is the most under-taught idea in this whole subject:

> **Hit ratio is a property of the workload, not of the cache.**

Concretely, and you will measure this yourself:

| Workload | 1,000-entry cache over 10,000 keys | Verdict |
|---|---|---|
| **Uniform random** access across all keys | ~10% hit ratio | Cache is nearly useless. You added a network hop and a failure mode |
| **Zipfian** (a few keys are very hot) | ~85–90% hit ratio | Cache is transformative |

**The cache did not change. The workload did.**

Real traffic is almost always skewed — a small fraction of products, users, or pages account
for most requests. But "almost always" is not "always", and the way to find out is to look at
your access logs and plot the distribution.

This also explains a real and confusing phenomenon: a cache that works beautifully in staging
(where synthetic load is uniform) can be worthless in production, or the reverse. If you
cannot explain your hit ratio in terms of your access distribution, you do not yet know
whether the cache is helping.

---

## Step 3: so keep a copy closer

```text
        ┌────────┐   miss    ┌───────┐   query   ┌──────────┐
 read ─►│ cache  │──────────►│  app  │──────────►│ database │
        │        │◄──────────│       │◄──────────│          │
        └────────┘   store   └───────┘  result   └──────────┘
             │
             └── hit: return in ~100 ns instead of ~5 ms
```

That is a cache. The mechanism is trivial. Everything difficult follows from one fact:

> **There are now two copies of the truth, and one of them can be wrong.**

---

## Step 4: invalidation — the hard part

The cached copy was correct when you stored it. The underlying data has since changed. Your
cache is now lying, confidently and quickly.

There is no general solution. There are four strategies, each moving the problem somewhere
different.

### TTL (time to live)

Discard entries after N seconds.

**What it gives you:** simplicity, and a *bounded* staleness you can reason about and state to
other people.
**What it costs:** data is wrong for up to N seconds, every time it changes.

TTL is the default answer and it is usually right, because it converts "the cache might be
wrong" into "the cache is wrong for at most 60 seconds", and the second statement is something
a product owner can agree to.

**That conversation is real engineering work**, and it is a gate in this topic: explain to a
product owner what "up to 60 seconds stale" means for their feature, without using the word
cache. Different data has wildly different tolerance — a product description can be an hour
stale; a stock level cannot be five seconds stale without overselling.

### Explicit invalidation

When you write, delete the cache entry.

**What it gives you:** freshness almost immediately.
**What it costs:** you must find *every* write path. Every one. Including the admin tool, the
batch import, the migration script, and the colleague's new endpoint written six months later
who did not know the cache existed.

It also has a genuine race condition, which is subtle enough that most people do not see it
until it bites:

```text
Thread A (read)                     Thread B (write)
  cache miss
  read value V1 from database
                                      write V2 to database
                                      delete cache entry
  store V1 in cache          ← the cache now holds V1 forever
```

The reader's store lands *after* the writer's delete, so a stale value is cached with no TTL
to save it. Mitigations exist — versioned keys, write-through, or simply always having a TTL as
a backstop — and the reason to always have a TTL becomes obvious once you have seen this.

### Write-through

Write to the cache and the database together, in the same operation.

**What it gives you:** the cache is never stale, because it is never bypassed.
**What it costs:** writes are slower, both systems must succeed (or you need to handle partial
failure), and it only works if *every* write goes through your code. Direct database access by
anything — a migration, a script, another service — breaks the guarantee silently.

### Versioned keys

Include a version or timestamp in the key: `user:123:v7`. A write increments the version, so
old entries become unreachable and expire naturally.

**What it gives you:** no invalidation race, and no need to delete anything.
**What it costs:** you must store and read the version from somewhere (which is itself a
lookup), and old entries occupy memory until evicted.

### Choosing

| Strategy | Freshness | Complexity | Fails when |
|---|---|---|---|
| TTL | Bounded staleness | Lowest | Staleness is unacceptable |
| Explicit invalidation | Nearly immediate | Medium | You miss a write path — and you will |
| Write-through | Always fresh | Medium | Anything writes without going through you |
| Versioned keys | Always fresh | Higher | Version lookup becomes the new bottleneck |

**In practice: TTL plus explicit invalidation for the paths you control.** The TTL is the
backstop for the write paths you missed, and you *have* missed some.

Phil Karlton's line — that the two hard things in computer science are cache invalidation and
naming things — is a joke that has survived because the first half is true. Everything else in
this topic is mechanical.

---

## Step 5: eviction — the copy is smaller than the truth

Memory is finite. When the cache is full and you want to add an entry, something must go.

| Policy | Discards | Good when | Bad when |
|---|---|---|---|
| **LRU** (least recently used) | The item unused for longest | Temporal locality — most workloads | A single large scan touches everything and flushes the useful entries |
| **LFU** (least frequently used) | The item accessed least often | Stable popularity | Popularity shifts — yesterday's hit keeps a dead item resident |
| **FIFO** | The oldest inserted | Almost never. Ignores usage entirely | Anything with locality |
| **TTL only** | Whatever expires | Freshness matters more than hit ratio | Memory fills with unexpired but unused entries |
| **Random** | An arbitrary item | Genuinely fine at scale, and very cheap | You need predictability |

**LRU is the default**, and worth understanding deeply enough to implement in O(1) — a hash
map for lookup plus a doubly linked list for recency, because neither structure alone provides
both. You will build this in the
[project](../../../projects/in-memory-cache/README.md).

Two things worth knowing that most treatments omit:

**Random eviction is respectable.** At scale, with good locality, random is nearly as effective
as LRU and dramatically cheaper — no ordering to maintain, no lock contention on a shared list.
Redis's default policies are *approximate* LRU implemented by sampling a handful of keys and
evicting the oldest of those, precisely because maintaining exact LRU order in a single-threaded
server is too expensive. That is a real implementation choosing an approximation, and it is
worth reading about after you have implemented the exact version.

**The unit of capacity matters.** Bounding by *entry count* is wrong when values vary in size —
you can hold 1,000 entries and use 40 GB. Real caches bound by bytes. You will discover this
in a `break` gate, which is a better way to learn it than being told.

---

## Step 6: stampedes — everyone misses at once

The cache is empty and 500 requests arrive for the same key.

All 500 miss. All 500 query the origin. The origin, which was comfortable serving 5% of
requests, now gets 100% of them simultaneously — and it is often the moment the whole system
falls over.

Three shapes of the same problem:

**Concurrent miss on a hot key.** One key expires, and every in-flight request for it goes to
the origin.

**Mass simultaneous expiry.** You populated 10,000 entries at once — during a deploy, or a
warm-up — all with a 300-second TTL. All 10,000 expire in the same second. This is the version
that surprises people, and it is why TTLs need jitter.

**Cold start.** The cache restarts, or a new instance joins. Everything misses at once. The
cache was protecting the origin from load the origin can no longer handle, which is a specific
and nasty kind of coupling: the system's capacity now depends on the cache being warm.

### Mitigations

| Mitigation | Mechanism | Cost |
|---|---|---|
| **Single-flight** | First miss takes a per-key lock; other requests wait for its result | One origin call. Waiters block, so a slow origin now blocks many requests |
| **Stale-while-revalidate** | Serve the expired value; refresh in the background | No latency spike, no herd. You knowingly serve stale data |
| **Jittered TTLs** | Randomise expiry: 300 s becomes 270–330 s | Prevents *mass* expiry. Does nothing for a single hot key |
| **Probabilistic early expiration** | Refresh before expiry with a probability that rises as expiry approaches | Elegant, one line of arithmetic, and spreads refreshes naturally |
| **Pre-warming** | Populate before taking traffic | Solves cold start. Needs to know what to load, and takes time |

**Cause a stampede yourself.** It is a gate, and the graph of 500 origin calls collapsing to 1
after you add single-flight is the most satisfying measurement in the topic.

---

## Step 7: one machine is not enough

Your cache outgrows one process's memory, or you have 20 application servers each with their
own cache and 20 divergent copies.

So the cache moves to its own machines. Now: **which machine holds which key?**

**Modulo hashing** — `server = hash(key) % N` — is the obvious answer and it is wrong for a
reason worth internalising. With N = 4 and a server failing, N becomes 3, and *almost every
key's assignment changes*. The entire cache is effectively invalidated at the moment you were
least able to afford it.

**Consistent hashing** places servers and keys on a conceptual ring; a key belongs to the next
server clockwise. Removing a server moves only *its* keys — roughly 1/N of the total — and
leaves the rest where they are.

The difference is not marginal:

| | Keys relocated when one of 4 servers fails |
|---|---|
| Modulo hashing | ~75% |
| Consistent hashing | ~25% |

Measure this yourself; it is a stretch goal in the
[project](../../../projects/in-memory-cache/README.md), and the numbers are more persuasive
than the argument.

Two other realities of distributed caching:

**Hot keys break the model.** Consistent hashing distributes *keys* evenly, not *load*. One
extremely popular key sends all its traffic to one server. Mitigations: replicate hot keys
across several nodes, or add a small local cache in front of the shared one — which reintroduces
the divergence problem you moved the cache out to solve. There is no free answer, only a choice.

**A shared cache is a shared failure domain.** Twenty servers depending on one cache cluster
means the cache is now a system-wide dependency. **Decide deliberately what happens when it is
unavailable** — degrade to the origin, fail fast, or serve stale — and write the decision down.
Discovering your default during an incident is how a cache outage becomes a total outage.

---

## Step 8: this is what the products are

Everything above is a set of decisions. Real caches are specific answers to them.

| Product | Answers |
|---|---|
| **CPU L1/L2/L3 cache** | Hardware LRU-ish, cache-line granularity, coherence protocols between cores |
| **OS page cache** | Caches file contents in unused RAM, LRU-ish, invalidated on write. You measured this in `computer-basics` |
| **Database buffer pool** | Caches disk pages, LRU variants, invalidated by the database's own writes |
| **Memcached** | Distributed, LRU, string values, multi-threaded, deliberately minimal |
| **Redis** | Distributed, several eviction policies, rich data structures, optional persistence, single-threaded command execution |
| **CDN** | Geographically distributed, HTTP-semantics-driven, TTL plus purge |
| **HTTP client / browser cache** | RFC 9111 semantics: `Cache-Control`, `ETag`, conditional requests |

Notice that **HTTP caching is the cheapest cache available**, because someone else operates it.
A correct `Cache-Control` header can eliminate a request entirely — no origin, no cache
cluster, no invalidation code. Before building an application cache, check whether an HTTP
header would do the job. This is genuinely under-used, and it is why RFC 9111 is Tier 1 in
[resources.md](resources.md).

---

## Putting it together

```text
Why is this slow?  ── measure ──►  is it a slow query, an N+1, or high volume?
                                            │
                        only the third one wants a cache
                                            ▼
Memory is 1,000-1,000,000× closer than the alternatives.
                                            ▼
Does the workload have locality?  ── no ──► do not add a cache
                                  ── yes ─►
                                            ▼
Keep a copy closer.                              → the cache
Two copies exist; one can be wrong.              → invalidation (the hard part)
The copy is smaller than the truth.              → eviction
Many readers can miss at once.                   → stampedes
One machine's memory is not enough.              → distribution, consistent hashing
                                            ▼
Redis, Memcached, CDNs, and your CPU are
particular answers to these questions.
```

Every claim you will meet about caching — in a blog post, a vendor page, or a design review —
occupies a place in that chain. When something confuses you, find where it sits.

---

## Next

[concepts.md](concepts.md) for depth per concept, then [practical.md](practical.md) for real
caches and the selection rubric.
