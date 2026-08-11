# Caching — resources

Nine resources, including one specification and one paper. Read four or five of them properly
rather than skimming all nine.

Selection rules: [resource-tiers.md](../../../docs/resource-tiers.md).

[← Caching](README.md) · [Fundamentals](fundamentals.md) ·
[Advanced](advanced.md)

---

## Tier 1 — Primary sources

### [RFC 9111 — HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111.html)

**The specification for the cache you get for free.**

Read **section 4** (constructing responses from caches) and **section 5** (the header field
definitions). Skip the rest for now.

Why this is the first resource and not an afterthought: HTTP caching is the cheapest cache
available — someone else operates it, and a correct header eliminates the request entirely. It is
also the clearest existing statement of what *freshness*, *validation*, and *staleness* mean, and
every application-level cache reinvents these concepts, usually worse.

Two specifics that surprise almost everyone and are stated plainly here: `no-cache` means
"revalidate before using", **not** "do not store" — that is `no-store`. And `Vary` is what stops a
shared cache serving one user's content-negotiated variant to another; omitting it is a real bug
with real consequences.

Reading an RFC is a skill, and this is a good one to start on: it is well organised, the sections
are short, and you can verify what you learn in your browser's devtools in ten minutes.

### [Redis documentation — key eviction](https://redis.io/docs/latest/develop/reference/eviction/)

The authoritative description of a real eviction implementation.

**Read it after implementing exact LRU yourself.** Then the interesting part is visible: Redis
does *not* maintain exact LRU order. It samples a handful of keys and evicts the oldest of those,
because maintaining exact ordering in a single-threaded server costs too much. That is a design
constraint leaking into an API, documented honestly, and it is a better lesson about engineering
than any explanation of LRU.

Also note the policy list — `allkeys-lru`, `volatile-lru`, `allkeys-random`, `noeviction` and the
rest — and that **`noeviction` is the default**, meaning writes fail rather than evicting. Setting
`maxmemory-policy` explicitly is not optional.

*Verified against Redis 7.2 (2026-08).*

### [Cache-Aside pattern — Microsoft Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside)

Short, precise, and vendor-neutral despite where it is hosted.

Listed because it spells out the **consistency consequences** of the pattern rather than just the
mechanics — including the race between a write and a concurrent read populating the cache, which
is the subtlest thing in
[fundamentals.md](fundamentals.md#explicit-invalidation) and which most tutorials omit entirely.

Ten minutes. Read it before you write your cache-aside path.

---

## Tier 2 — High-quality learning material

### [Designing Data-Intensive Applications — Martin Kleppmann, chapters 1–3](https://dataintensive.net/)

**The best single book for Level 3 and 4 backend work**, and chapters 1–3 are directly relevant
here.

What it does for this topic: it places caching inside the wider picture of latency, storage, and
replication, so you stop seeing it as a trick and start seeing it as one point on a
consistency-versus-performance spectrum. Chapter 1's treatment of **percentiles and tail latency**
is directly applicable to your benchmark gate and is the clearest explanation of why the mean lies
that exists in book form.

Paid. It is the one book on this list worth buying, and everything essential in this topic is
covered by the free resources here if it is not available to you.

### [Scaling Memcache at Facebook (NSDI 2013)](https://www.usenix.org/system/files/conference/nsdi13/nsdi13-final170_update.pdf)

**The best available paper on what caching becomes at scale.** Free.

Read **section 3** first. It covers leases to prevent stampedes, handling of cold clusters, and —
unusually and admirably — an explicit acknowledgement that they chose to serve stale data and why.

Why it is a good *first* systems paper: every problem in it is one you will have caused yourself in
the [project](../../../projects/in-memory-cache/README.md). You will read about the thundering herd
having produced one, and about lease-based invalidation having hit the populate-after-write race.
That makes the paper legible in a way most papers are not on first contact.

Use the `research` gate format from
[competency-gates.md](../../../docs/competency-gates.md#research-exercises): what is the
contribution, what assumption makes it work, what does it cost, and does it apply to you?

### [Linux memory management concepts — the page cache](https://docs.kernel.org/admin-guide/mm/concepts.html)

The cache you already depend on and never configured.

Read this to understand why your file read was fast the second time — you measured this in
[`computer-basics`](../../foundations/computer-basics/README.md) — and why low "free memory" is not
a problem. It is also the cleanest example of a cache with **no invalidation problem**, because the
kernel controls every write path, which is worth noticing: invalidation is hard precisely when you
do *not* own all the writes.

Short. Read the page cache and memory-reclaim sections.

---

## Tier 3 — Practical

### [Netflix EVCache — the hidden microservice](https://netflixtechblog.com/announcing-evcache-distributed-in-memory-datastore-for-cloud-c42d99f8ab5f)

A production distributed cache with its constraints stated: multi-zone replication, cold-start
warming, and what happens when an availability zone is lost.

Useful for seeing that at scale **the operational concerns dominate the algorithmic ones**. Nothing
in it is about eviction policy; all of it is about failure, warming, and topology. That reordering
of priorities is the Level 4 shift described in [advanced.md](advanced.md).

### [Cache stampede mitigation — optimal probabilistic early expiration](https://cseweb.ucsd.edu/~avattani/papers/cache_stampede.pdf)

Six pages on a single problem you will have caused, with a solution that is one line of arithmetic:
refresh early with a probability that rises as expiry approaches, so refreshes spread out
naturally instead of clustering at the TTL boundary.

Included because it is a good demonstration that **some production problems have small, provable
answers** — a useful counterweight to the impression that everything at this level is
tuning and folklore. Also short enough to read in one sitting, which makes it a gentle second
paper after the Memcache one.

---

## What is deliberately not here

The reasons are more useful than more links.

**"Top 5 caching strategies" blog posts.** There are thousands, they all cover the same four
patterns, and none of them mentions the populate-after-write race, stampedes, or that hit ratio is
a property of the workload. [fundamentals.md](fundamentals.md) is a better version.

**Redis command references and "Redis in 100 seconds" content.** The commands are a lookup, not a
topic. Learning `SETEX` is five seconds of work; learning when a cache is the wrong answer is 40
hours.

**Redis University / vendor training.** Competent, and aimed at making you effective with a
specific product rather than at the concepts. Useful *after* this topic if you will operate Redis
professionally.

**Distributed-systems textbooks.** Excellent and premature. Caching leads to
`distributed-systems-fundamentals` and `replication-and-consistency`, which is where those books
belong.

**Papers on advanced eviction policies** (ARC, W-TinyLFU). Genuinely interesting, and the gains are
smaller than fixing your key design or capacity. Pointers are in
[advanced.md](advanced.md#better-eviction-policies) for when you have exhausted the cheaper wins.

**Anything claiming caching is simple.** The mechanism is simple. Invalidation is not, and a
resource that does not say so is not worth your time.

---

## A working plan

Roughly 4 weeks at 8–10 hours per week.

**Week 1 — the chain.** Read [fundamentals.md](fundamentals.md) properly; it is the file that
carries this topic. Then the Cache-Aside page and RFC 9111 sections 4–5. Do
[exercises.md](exercises.md) 1–3 against a real access log, and 19–22 in your browser.

**Weeks 2–3 — the project.**
[in-memory-cache](../../../projects/in-memory-cache/README.md), all five stages. Read the Redis
eviction documentation after stage 1, when your own LRU exists to compare against. Read the page
cache documentation while you wait for a benchmark to finish.

**Week 4 — measure, break, and write up.** Exercises B1–B7 and M1–M5. Then read the Memcache paper
and answer the four research questions. Work the [`topic.yml`](topic.yml) gates, especially the
product-owner `explain` gate and the `design` gate.

Kleppmann chapters 1–3 fit anywhere and are worth reading twice.

---

## If you only have twelve hours

1. Read [fundamentals.md](fundamentals.md). — 2 hours
2. Implement the O(1) LRU with TTLs, single-threaded, in front of a real datastore. — 4 hours
3. Cause a stampede (500 concurrent misses), add single-flight, measure both. — 2 hours
4. Measure hit ratio under uniform and Zipfian distributions. — 2 hours
5. Write up the product-owner explanation of "up to 60 seconds stale". — 1 hour
6. Read RFC 9111 section 5. — 1 hour

That is not the full topic, but it gives you the two measurements that matter — the stampede graph
and the distribution comparison — plus the staleness conversation. Those three artifacts are what
make the topic real.
