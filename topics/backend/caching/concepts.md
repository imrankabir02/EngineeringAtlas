# Caching — concepts

Fifteen concepts with a required depth for each. This file answers *how deeply should I learn
it?*

[← Caching](README.md) · [Fundamentals](fundamentals.md) ·
[Practical](practical.md)

---

## Depth vocabulary

| Depth | Means | Test |
|---|---|---|
| `aware` | You know it exists and roughly what it does | You would not be surprised by the term, and you know when to go read about it |
| `working` | You can use it correctly and explain the trade-off without notes | You can apply it to a new problem |
| `deep` | You understand the mechanism well enough to debug it and predict failures | You can explain *how* it works and where it breaks |

---

## The inventory

| Concept | Depth | The one thing to take from it |
|---|---|---|
| [Locality](#locality-of-reference) | **deep** | Without it, a cache is pure overhead |
| [Hit ratio](#hit-ratio-and-its-dependence-on-workload) | **deep** | A property of the workload, not of the cache |
| [Invalidation](#invalidation) | **deep** | Four strategies, none of which solves it — they relocate it |
| [Caching patterns](#cache-aside-read-through-write-through-write-behind) | **deep** | Where the cache sits relative to the write path |
| [Stampedes](#stampedes-and-thundering-herds) | **deep** | Three shapes, five mitigations, each with a cost |
| [Measuring a cache](#measuring-a-cache) | **deep** | An unmeasured cache is a guess with extra failure modes |
| [Eviction policies](#eviction-policies) | working | LRU deeply; the others by shape |
| [The layers you already have](#the-layers-you-already-have) | working | Debugging means identifying *which* copy lied |
| [HTTP caching](#http-caching) | working | The cheapest cache, because someone else runs it |
| [Distributed caching](#distributed-caching) | working | Consistent hashing, hot keys, shared failure domain |
| [Negative caching](#negative-caching) | working | Necessary against miss floods; introduces its own bug |
| [Key design](#key-design) | working | A key that omits an input serves the wrong user's data |
| [Hardware cache coherence](#hardware-cache-coherence) | aware | It exists and costs real time. Stop there |
| [CDN internals](#cdn-internals) | aware | A distributed cache with slow purges |
| [Formal consistency models](#formal-consistency-models) | aware | "Eventually consistent" has a precise meaning. Later |

---

## Locality of reference

**Depth: deep.** The precondition for the entire topic.

Temporal locality: recently accessed data is likely to be accessed again. Spatial locality:
nearby data is likely to be accessed next.

What `deep` requires — you can:

- define both kinds and give an example of each from a system you have worked on
- explain why a cache over a uniform-random access pattern is worthless, with arithmetic
- inspect an access log and judge whether the workload has locality
- name a workload with *no* useful locality (a full table scan, a report over all records, a
  one-time import) and say why a cache would hurt rather than help
- explain why a large scan can *destroy* a cache's usefulness by evicting the hot set

**Test yourself:** you have 1,000 cache slots and 10,000 equally-likely keys. What hit ratio do
you expect, and is the cache worth having? *(~10%; almost certainly not — you added a hop and a
dependency to avoid 10% of the work.)*

---

## Hit ratio and its dependence on workload

**Depth: deep.** The most under-taught idea in the subject.

What `deep` requires — you can:

- state that hit ratio is determined by the access distribution, not the cache implementation
- measure hit ratio under two different distributions with the same cache and explain the gap
- explain why a cache can work in staging and fail in production, or the reverse
- compute the *marginal* value of more cache capacity — doubling memory rarely doubles the hit
  ratio, and knowing the shape of that curve is how capacity is actually decided
- decide, from a measured hit ratio, whether to tune the cache or remove it

**Test yourself:** your cache has a 2% hit ratio. What do you do? *(Investigate the
distribution. If access is genuinely uniform, remove the cache — it is costing latency and
reliability for nothing. If there is a hot set your keys are failing to capture, the key design
is wrong.)* This is a `debug` gate.

---

## Invalidation

**Depth: deep.** The hard part.

What `deep` requires — you can:

- describe TTL, explicit invalidation, write-through, and versioned keys, with the cost of each
- explain the read-populate-after-write race, and why a TTL should always exist as a backstop
- find every write path in a system you did not write, and know that you have probably missed
  one
- state a staleness budget for a specific piece of data, and defend it
- **explain the staleness to a non-technical stakeholder** — because this is a product decision,
  not a technical one, and someone has to agree to it

**Test yourself:** you cache a user's profile with explicit invalidation on update and no TTL.
An admin edits the record directly in the database during an incident. What now? *(Stale
forever. This is why a TTL backstop is not optional, and why "we invalidate on write" is a
statement about the paths you know.)*

---

## Cache-aside, read-through, write-through, write-behind

**Depth: deep.**

| Pattern | Read path | Write path |
|---|---|---|
| **Cache-aside** | App checks cache, on miss reads origin and populates | App writes origin, then invalidates cache |
| **Read-through** | Cache itself fetches from origin on a miss | Usually paired with write-through |
| **Write-through** | Same as read-through | App writes cache; cache writes origin synchronously |
| **Write-behind** | Same | App writes cache; cache writes origin *asynchronously* |

What `deep` requires — you can:

- draw each pattern's read and write path
- state which failure each pattern makes possible: cache-aside has the populate-after-write
  race; write-through couples write latency to two systems; **write-behind can lose
  acknowledged writes** if the cache dies before flushing
- explain why cache-aside is the common default (the application stays in control and a cache
  outage degrades rather than breaks)
- say when write-behind is acceptable (metrics, counters, analytics — data where losing a
  second is tolerable) and when it is not (anything a user or an auditor will check)

**Test yourself:** which pattern would you use for a click counter, and which for an account
balance? *(Write-behind is reasonable for clicks — losing a second of counts is survivable.
Never for a balance.)*

---

## Stampedes and thundering herds

**Depth: deep.**

What `deep` requires — you can:

- describe all three shapes: concurrent miss on a hot key, mass simultaneous expiry, cold start
- explain why mass expiry happens even with sensible TTLs, and why jitter fixes it
- implement single-flight and state its cost (waiters block, so a slow origin blocks many
  requests)
- explain stale-while-revalidate and precisely which guarantee it trades away
- explain why a cold cache can take down an origin that was previously coping — the system's
  capacity depends on the cache being warm, which is a hidden coupling

**Test yourself:** you populate 50,000 entries during a deploy, all with a 300-second TTL. What
happens in 300 seconds? *(All 50,000 expire together and the origin receives 50,000 simultaneous
requests. Jittered TTLs — 270 to 330 seconds — spread it out.)*

---

## Measuring a cache

**Depth: deep.**

What `deep` requires — you can name and instrument the metrics that matter:

| Metric | Why |
|---|---|
| Hit ratio | Whether the cache is doing anything |
| p50/p95/p99 on the **hit path** | Is a hit actually fast? A slow shared cache may not beat the origin |
| p50/p95/p99 on the **miss path** | The miss pays cache lookup *plus* origin cost |
| Origin request rate | The load you are actually shedding — the number that justifies the cache |
| Eviction rate | High evictions with a low hit ratio means the cache is too small or the keys are wrong |
| Memory used, and fragmentation | The real limit, not entry count |

And you can:

- explain why a mean latency is meaningless here — hits and misses are two distinct populations,
  so the distribution is bimodal by construction
- measure with the cache cold, warm, and disabled, and know why all three are needed
- avoid coordinated omission in your load generator

**Test yourself:** hit ratio is 95% and p99 latency got worse after adding the cache. How?
*(The 5% of misses now pay cache lookup plus origin cost, and if the cache is a network hop,
that addition lands squarely in the tail.)*

---

## Eviction policies

**Depth: working.** Except LRU, which you implement.

- implement LRU in O(1) using a hash map plus a doubly linked list, and explain why neither
  structure alone suffices
- describe LFU, FIFO, TTL-only, and random, and name a workload suiting each
- explain why **random eviction is respectable at scale** — nearly as effective as LRU with good
  locality, and far cheaper because there is no shared ordering to maintain or lock
- explain why Redis approximates LRU by sampling rather than maintaining exact order
- explain why bounding by entry count is wrong for variable-size values

**Deferred:** ARC, 2Q, W-TinyLFU, CLOCK-Pro. Know that better policies exist and that the gains
are usually small compared with fixing your key design. [advanced.md](advanced.md) has the
pointers.

---

## The layers you already have

**Depth: working.** This is a debugging skill.

| Layer | Caches | Invalidated by |
|---|---|---|
| CPU L1/L2/L3 | Memory lines | Coherence protocol |
| OS page cache | File contents | Writes, memory pressure |
| Database buffer pool | Disk pages | The database itself |
| ORM identity map / session | Objects within a transaction | Transaction end |
| Your application cache | Whatever you chose | You |
| HTTP client / browser | Responses | `Cache-Control`, `ETag` |
| CDN | Responses | TTL, purge |
| DNS resolver | Records | TTL — and often ignored TTLs |

What `working` requires: given a stale-data report, you can enumerate these, decide which are
plausible, and design an experiment that identifies the culprit. That is the `debug` gate.

The two that catch people out: **DNS**, because resolvers and libraries frequently ignore short
TTLs and cache far longer than you intended, and **the ORM identity map**, because it makes
reads within one transaction return an object that no longer matches the database.

---

## HTTP caching

**Depth: working.** The cheapest cache available.

- use `Cache-Control` correctly: `max-age`, `no-cache` (revalidate, *not* "do not store"),
  `no-store`, `private` versus `public`, `immutable`
- use `ETag` and `If-None-Match` for conditional requests, and explain what a `304` saves
- explain the difference between a private cache (one browser) and a shared cache (a CDN or
  proxy), and why `private` matters for anything user-specific
- use `Vary` correctly, and know that a missing `Vary` on a content-negotiated response means a
  shared cache can serve one user's variant to another
- know the content-addressed-URL pattern: hash the filename and set a one-year `immutable` TTL,
  so invalidation happens by changing the URL rather than by purging

**Why this deserves your attention:** a correct header can eliminate the request entirely — no
origin, no cache cluster, no invalidation code, no operational burden. Check whether HTTP
caching solves your problem *before* building an application cache. RFC 9111 is Tier 1 in
[resources.md](resources.md) for this reason.

---

## Distributed caching

**Depth: working.**

- explain why modulo hashing relocates ~75% of keys when one of four servers fails, and why
  consistent hashing relocates ~25%
- explain hot keys: consistent hashing balances *keys*, not *load*
- name the mitigations for hot keys (replicate the key, or add a small local cache in front) and
  the cost of each — the local cache reintroduces divergence
- state what happens when the shared cache is unavailable, as a deliberate decision: degrade to
  origin, fail fast, or serve stale
- explain why a shared cache is a shared failure domain, and what that means for capacity
  planning

**Test yourself:** your cache cluster is down and the origin cannot handle full traffic. What
should the application do? *(There is no comfortable answer, which is the point. Serving stale
if you have it, shedding load with a fast 503, or degrading features are all defensible. Falling
back silently to the origin and collapsing is the one that turns a cache outage into a total
outage, and it is the default if you do not choose.)*

---

## Negative caching

**Depth: working.**

Caching the *absence* of a value.

- explain why it is necessary: a flood of requests for nonexistent keys misses every time and
  hits the origin every time, which is a denial-of-service vector
- explain the bug it introduces: the key is created, and you are now serving "does not exist"
  for a thing that exists
- state the standard mitigation: much shorter TTLs for negative entries than positive ones
- know that Bloom filters are the industrial version of this idea — databases use them to avoid
  disk reads for keys that cannot be present

---

## Key design

**Depth: working.** Small concept, expensive mistakes.

- include **every input that affects the value**. A key of `product:123` for a response that
  varies by currency, locale, or logged-in user will serve one user another user's data. This is
  a real and serious class of security bug
- namespace keys so you can reason about and purge groups: `v2:product:123:en-GB`
- include a schema version so a deploy that changes the value's shape does not read entries
  written by the old code
- keep keys short — they consume memory too, and at millions of entries the key size matters
- know that you usually cannot enumerate keys by pattern efficiently, which is why "invalidate
  everything for user X" needs to be designed in from the start, not discovered later

---

## Hardware cache coherence

**Depth: aware.** Deliberately capped.

CPU cores each have caches, and keeping them consistent costs real time and inter-core traffic.
Two threads writing different variables that share a cache line cause coherence traffic for no
logical reason — false sharing.

**What you need:** know it exists, and that it is why memory layout affects multi-threaded
performance.

`memory-management` (L3) and `performance-engineering` (L4) go deeper, with measurement.

---

## CDN internals

**Depth: aware.**

A geographically distributed cache with its own eviction, its own tiering (edge and shield
layers), and its own invalidation.

**What you need:** know that a CDN is a cache and obeys everything in this topic; know that
**purges are slower than you expect** — often seconds to minutes across all edges — so purging is
not a reliable correctness mechanism; and know that a cache miss at the edge may still hit a
regional tier before reaching your origin.

`frontend-performance` and `cloud-architecture` treat it properly.

---

## Formal consistency models

**Depth: aware.**

"Eventually consistent" has precise definitions, and a family of related ones: read-your-writes,
monotonic reads, causal consistency, linearizability.

**What you need:** know that adding a cache makes your system eventually consistent, and that
this has a formal meaning rather than being a vague apology. Know that "read-your-writes" is the
guarantee users notice most — a user who edits their profile and immediately sees the old version
will file a bug, and the fix is usually to bypass the cache for that user's own data for a short
window.

`replication-and-consistency` (L4) is where this belongs, with the vocabulary and the proofs.

---

## Using this file

The three `aware` concepts are each a genuine rabbit hole. Coherence protocols and consistency
models in particular are fascinating and will consume weeks without making you better at
caching.

The failure mode this file prevents: reading about linearizability while your cache still has no
hit-ratio metric.

---

## Next

[practical.md](practical.md) — real caches, the selection rubric, and operating one.
