# Caching

**Level 3** · Backend · ~40 focused hours · 3–5 weeks

Keeping a copy of data closer to its reader. What that buys, and what it costs.

[Fundamentals](fundamentals.md) · [Concepts](concepts.md) ·
[Practical](practical.md) · [Exercises](exercises.md) · [Projects](projects.md) ·
[Interview](interview.md) · [Advanced](advanced.md) · [Resources](resources.md)

---

## What this is

The complete chain: why caching works at all, where to put a cache, what to discard when it
is full, how to know when the copy is wrong, and what happens when many readers miss at once.

Redis, Memcached, your CDN, and your CPU's L1 cache are all implementations of the same set
of decisions. This topic is about the decisions.

## Why it matters

**You are already relying on caches you did not configure.** The CPU caches memory. The
operating system caches file contents. Your database caches pages in its buffer pool. Your
ORM caches objects within a transaction. Your HTTP client caches responses. Your DNS
resolver caches records.

That matters practically: when a user reports stale data, the question is *which copy of the
truth is wrong*, and you cannot answer it without knowing which layers exist.

**Caching is the standard tool for making reads fast**, and the standard tool is worth
knowing well rather than approximately.

And the reason this topic is worth its 40 hours rather than an afternoon:

> Caching is where you learn that adding a component adds a failure mode.

A cache makes the happy path faster and introduces stale reads, stampedes, cold-start
collapse, and an entire new thing that can be down. Working through those deliberately — in a
project where the consequences are yours and cheap — is the most efficient introduction to
Level 3 thinking available. Every topic after this one has the same shape.

## Prerequisites

**Hard:**

- `networking-fundamentals` — a cache trades one cost for another, and the cost it removes is
  usually a network round trip. Without knowing what a round trip costs, you cannot judge
  whether a cache earns its complexity.
- `sql` — the canonical cache sits in front of a database. You need to know what it is
  protecting, and you must be able to distinguish *a slow query* from *a query called too
  often*. The fixes are different, and caching the first one is the single most common misuse
  of this topic.

**Soft:**

- `operating-systems-fundamentals` — the page cache is a cache you already depend on, and
  seeing it makes eviction and locality concrete.
- [`data-structures`](../../computer-science/data-structures/README.md) — an LRU cache is a
  hash table plus a doubly linked list. The project is much easier if you have built both.

## How deeply to learn this

Depth per concept is in [concepts.md](concepts.md).

**Deep** (6) — locality, hit ratio and its dependence on workload, invalidation, caching
patterns, stampedes, and measuring a cache.

Two of those deserve emphasis, because they are the ones that most change how you work:

- **`hit-ratio`** — a hit ratio is a property of *the access distribution*, not of the cache.
  The same cache is 10% effective on uniform traffic and 90% on skewed traffic. This means
  "should we add a cache?" is answered by measuring your workload, not by reasoning about the
  cache.
- **`invalidation`** — the hard part, and where the worst bugs live. Everything else in this
  topic is mechanical by comparison.

**Working** (6) — eviction policies, the cache layers you already have, HTTP caching,
distributed caching, negative caching, key design.

**Aware** (3) — hardware cache coherence, CDN internals, formal consistency models. Each is a
Level 3–4 topic elsewhere; know the words and move on.

## Reading order

1. [fundamentals.md](fundamentals.md) — the full first-principles chain. This is the file that
   matters most in this topic.
2. [concepts.md](concepts.md) — the inventory with depth per concept.
3. [practical.md](practical.md) — real caches, the selection rubric, and operating one.
4. [exercises.md](exercises.md) — drills, including the measurement ones.
5. [projects.md](projects.md) — the cache you build and then break.
6. [interview.md](interview.md) — where caching appears in system design interviews.
7. [resources.md](resources.md) — nine resources including one paper.
8. [advanced.md](advanced.md) — where this goes at Levels 4–5.

## How you know you have it

Full gates in [`topic.yml`](topic.yml). The distinguishing ones:

- **You caused a stampede** — 500 concurrent misses on one key — have the origin-load graph,
  implemented a mitigation, and measured the improvement.
- **You measured hit ratio under uniform and Zipfian distributions** with the same cache, and
  can explain the gap. This is the measurement that makes the topic click.
- **You served stale data on purpose** and measured how long the lie lasted.
- **You can explain "up to 60 seconds stale" to a product owner** without using the word
  cache. Staleness is a product decision and someone non-technical has to agree to it.
- **`design` gate:** a caching strategy for a product page with live stock levels and
  tolerably stale descriptions — including what you deliberately do *not* cache.

## What comes next

| Next | Why |
|---|---|
| `message-queues-and-streaming` | The next tool for keeping load off the origin — decoupling in time rather than by copying |
| `distributed-systems-fundamentals` | You now have two copies of the truth on purpose. That is the door to consistency and partial failure |
| `system-design-fundamentals` | Caching is the first component you chose deliberately with stated trade-offs. That *is* system design |
| `performance-engineering` | You measured percentiles and found a bottleneck. Doing it systematically is the next skill |
