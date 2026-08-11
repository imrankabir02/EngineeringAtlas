# Caching — advanced

Where caching goes at Levels 4 and 5, what is genuinely unsolved, and what to defer.

[← Caching](README.md) · [Concepts](concepts.md) ·
[Resources](resources.md)

---

## The shift at Level 4

At Level 3, caching is a component you add to a system. At Level 4 it becomes something
different: **a consistency decision with an operational and financial cost**, made across a whole
architecture rather than in one endpoint.

The questions change:

| Level 3 asks | Level 4 asks |
|---|---|
| Should I cache this? | What is our organisation-wide policy on staleness, and who decides? |
| What TTL? | What is the *composed* staleness across seven cache layers, and can we bound it? |
| Is the hit ratio good? | What does each additional point of hit ratio cost in memory, and where does the curve stop being worth it? |
| Does it work? | What happens during a region failover, and have we tested it? |
| How fast is a hit? | What is the p99.9, and what is our tail-latency budget for the whole request path? |

The recurring theme: caching stops being local. A staleness decision in one service becomes a
correctness problem in another, and nobody owns the composition.

---

## Where it goes

### Multi-tier caching

Local in-process cache in front of a shared cache in front of a database.

The tension is unavoidable: the local tier is ~5,000× faster than the shared tier, and it
reintroduces the divergence between processes that you moved the cache out to solve. So you get a
new question — how do you invalidate the local tiers? Options: very short local TTLs (simple,
bounded divergence), a pub/sub invalidation broadcast (fast, and now you depend on message
delivery for correctness), or versioned keys (correct, at the cost of a version read).

**Prerequisites:** `distributed-systems-fundamentals`, `message-queues-and-streaming`.

### Cache coherence at application scale

The same problem hardware solved for CPU cores, at a much larger scale and without the hardware's
guarantees. Lease-based invalidation — as used in the Facebook Memcache paper — is the best-known
production approach: a client holds a short lease on a key, and the cache can reject stale
populations.

Read that paper (in [resources.md](resources.md)) *after* you have caused the
populate-after-write race yourself. It answers a question you will have.

**Prerequisites:** `replication-and-consistency`, `consensus` for the harder variants.

### Tail latency

At Level 4, p99.9 matters, and caching cuts both ways. It reduces the median dramatically and can
*worsen* the tail: a miss pays cache lookup plus origin, an eviction storm produces a burst of
misses, and a cache-level pause (GC, or a single-threaded server blocked on one command) stalls
everything.

The relevant literature is about latency amplification in fan-out systems — a request touching 100
services waits for the slowest, so a 1% slow rate per service becomes a near-certainty overall.
Dean and Barroso's *The Tail at Scale* is the canonical treatment.

**Prerequisites:** `performance-engineering`, `capacity-planning`.

### Cost as a design constraint

Memory is expensive. At scale, the question is not "what hit ratio can we achieve" but "what is
the marginal cost per point of hit ratio, and where do we stop?"

The curve is concave: the first 10% of your keyspace in cache might buy 70% hit ratio, and the next
40% might buy 15 more points. Knowing where the knee is — for your workload — is how cache capacity
is actually budgeted, and it is measurable.

**Prerequisites:** `cost-optimization`, `capacity-planning`.

### Caching in the CDN and at the edge

Moving computation, not just data, to the edge. Edge workers with their own caches, stale-while-
revalidate at the CDN layer, and cache keys derived from request attributes.

The operational reality that surprises people: **purges are slow and not atomic**. A purge takes
seconds to minutes to propagate to every edge, so it cannot be used as a correctness mechanism.
Design for TTL expiry or content-addressed URLs.

**Prerequisites:** `cloud-architecture`, `frontend-performance`.

### Better eviction policies

There is real research here, and the gains are real but usually smaller than fixing your key
design or your TTLs.

- **ARC** (adaptive replacement cache) — balances recency and frequency automatically.
- **W-TinyLFU** — an admission filter that decides whether a new item *deserves* to displace an
  existing one, using a compact frequency sketch. Used by Caffeine, and it beats LRU meaningfully
  on skewed workloads.
- **CLOCK-Pro, 2Q, SLRU** — variants addressing LRU's weakness against scans.
- **Learned eviction** — models predicting reuse distance, an active research area.

**The honest ordering:** measure your hit ratio, fix your key design, right-size your capacity, and
*then* consider a better policy. Reaching for W-TinyLFU while your keys omit the locale is
optimising the wrong thing.

**Prerequisites:** `advanced-algorithms`, `performance-engineering`.

---

## Where each thread continues

| The question you now have | Where | Level |
|---|---|---|
| How do I keep caches consistent across machines? | `replication-and-consistency` | 4 |
| What does "eventually consistent" formally mean? | `replication-and-consistency` | 4 |
| How do I decide which node holds which key, at scale? | `partitioning-and-sharding` | 4 |
| Why is my cache the p99 bottleneck? | `performance-engineering` | 4 |
| How much cache should we buy? | `capacity-planning`, `cost-optimization` | 4 |
| How does the database's own buffer pool work? | `database-internals` | 4 |
| How do I shed origin load without copying data? | `message-queues-and-streaming` | 3 |
| How do CPU caches interact with my data layout? | `memory-management` | 3 |
| How do I make a cache safe under heavy concurrency? | `concurrency-and-parallelism` | 3 |
| How do I prove an invalidation scheme correct? | `distributed-systems-verification` | 5 |

---

## What is genuinely unsolved

Caching is old and its hard parts are still hard. Worth knowing, because it is usually presented
as settled.

**Invalidation at scale.** There is still no general solution. Every large system uses a
combination of TTLs, explicit invalidation, versioning, and accepted staleness, tuned by hand per
data type. Nobody has produced an approach that is correct, fast, and does not require the
application to know about the cache.

**Composed staleness.** With seven cache layers, each with its own TTL and its own invalidation,
the total worst-case staleness is the sum — and almost nobody can state it for their own system.
There is no standard tooling for computing or bounding it, which means most organisations do not
know how stale their data can be.

**Automatic cache sizing.** Deciding capacity from a workload, dynamically, is not solved in
general. Most systems are sized by measurement and adjusted by hand, which is the honest answer
rather than a gap in your knowledge.

**Cache-aware application design.** Whether an application should know it is cached is genuinely
contested. Transparent caching is easier to adopt and produces surprises; explicit caching is
harder and more predictable. There is no consensus, and the disagreement is real rather than a
failure to have read the right paper.

If any of this interests you, that is what `reading-research-papers` (L4) and
`research-engineering` (L5) are for.

---

## Two things worth doing now

Neither needs new prerequisites, and both extend this topic rather than starting a new one.

### Read the Facebook Memcache paper properly

*Scaling Memcache at Facebook* (in [resources.md](resources.md)) is the best available paper on
what caching becomes at scale, and it is unusually readable because the problems are ones you have
now caused yourself.

Read section 3 first, and answer in writing:

1. What is the contribution? One sentence, not the abstract.
2. What assumption makes leases work?
3. What did they choose to give up? (They are explicit about it, which is rare and admirable.)
4. Which of their problems have you personally caused in the
   [project](../../../projects/in-memory-cache/README.md)?

That is the `research` gate format from
[competency-gates.md](../../../docs/competency-gates.md#research-exercises), and this paper is an
unusually good first one — concrete, well written, and about something you now understand from the
inside.

### Measure the marginal value of capacity

Take your cache and measure hit ratio at 1%, 5%, 10%, 25%, and 50% of the keyspace. Plot it.

You will get a concave curve. Find the knee. Then compute what each additional point of hit ratio
costs in memory.

This is exercise M3 in [exercises.md](exercises.md), and it is worth calling out here because it
is the single most Level-4 thing available at Level 3: it converts a technical property into a
budgeting decision, which is what accountability for a system actually feels like.

---

## Questions worth deferring

Add these to your questions file.

1. My application cache, the database buffer pool, and the OS page cache all hold copies of the
   same row. Who invalidates whom? *(Mostly: nobody coordinates, and each layer's invalidation is
   independent — `database-internals`.)*
2. If a cache makes my system eventually consistent, what exactly did I promise users?
   *(`replication-and-consistency` — and "read-your-writes" is the guarantee they notice.)*
3. Two datacentres each have a cache. A write happens in one. What should the other do?
   *(There is no good answer, which is why cross-region caching is hard — `cloud-architecture`.)*
4. Could I prove my invalidation scheme correct rather than testing it?
   *(Sometimes, with model checking — `distributed-systems-verification`.)*
5. Why does my p99 get worse as my hit ratio improves? *(Fewer, more clustered misses, and a
   thinner tail sample — `performance-engineering`.)*

---

## Next

| Next | Why |
|---|---|
| `message-queues-and-streaming` | Shed origin load by decoupling in time rather than by copying |
| `distributed-systems-fundamentals` | You have two copies of the truth on purpose. This is the door |
| `system-design-fundamentals` | Caching was your first deliberate component choice with stated trade-offs |
| `performance-engineering` | You measured percentiles and found a bottleneck. Now do it systematically |
