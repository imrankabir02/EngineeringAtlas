# Caching — practical

Choosing a cache, placing it, operating it, and the failure modes you will actually meet.

[← Caching](README.md) · [Fundamentals](fundamentals.md) ·
[Concepts](concepts.md) · [Exercises](exercises.md)

---

## Before you add a cache

Four questions. If you cannot answer them, you are not ready to add one.

**1. What is slow, according to a measurement?**
Not a guess. A profile or a trace. See
[fundamentals.md step 0](fundamentals.md#step-0-measure-before-anything-else) — the answer is
often a missing index or an N+1 query, and caching either of those makes the system worse.

**2. Does the workload have locality?**
Look at your access logs. Plot request counts per key. If the distribution is flat, a cache
will not help, and adding one costs you latency on the miss path plus a new dependency.

**3. How stale can this data be?**
A number, in seconds, agreed with whoever owns the feature. "As fresh as possible" is not an
answer — it is a refusal to make the decision, and it will be made for you by whatever TTL
someone types.

**4. What happens when the cache is unavailable?**
Decide now, on paper: degrade to origin, fail fast, or serve stale. If you do not decide, the
answer will be "whatever the client library's default timeout does", discovered during an
incident.

---

## Where to put it

Ordered from cheapest to most complex. **Work down this list, not up it.**

### 1. An HTTP header (free)

If the data is addressable by URL and not user-specific, the correct answer may be a header:

```http
Cache-Control: public, max-age=3600
ETag: "a7f3c9"
```

Browsers, proxies, and CDNs then cache it. **No code, no infrastructure, no invalidation
logic** — and the request never reaches you at all, which no application cache can match.

The content-addressed pattern for static assets:

```http
GET /assets/app.a7f3c9d2.js
Cache-Control: public, max-age=31536000, immutable
```

The filename contains a content hash, so invalidation happens by changing the URL. A year-long
TTL is safe because a changed file is a different URL. This is the single best caching pattern
in existence and it costs nothing.

**Check this option first, every time.** It is regularly overlooked in favour of building
something.

### 2. In-process memory (nearly free)

A map, or an LRU, inside your application process.

**Fastest possible** — no serialisation, no network. Also the simplest to reason about.

**Costs:** each process has its own copy, so N processes means N divergent caches and N× the
memory; and it is empty after every restart or deploy.

Right for: reference data that changes rarely (configuration, feature flags, currency codes,
lookup tables), and computed values that are expensive but small.

Wrong for: anything where divergence between processes is visible to users, and anything large.

### 3. A shared cache (Redis, Memcached)

One copy, all processes see it, survives application restarts.

**Costs:** a network round trip per operation (~0.5 ms rather than ~100 ns), serialisation, and
a new service to deploy, monitor, secure, and be paged about.

Right for: session data, computed results shared across processes, rate-limit counters,
anything where all processes must agree.

**Note the ~5,000× latency difference from option 2.** A shared cache is fast compared with a
database and slow compared with local memory. For very hot data, a two-tier arrangement — small
local cache in front of the shared one — is common, and it reintroduces the divergence problem.
That is a real trade-off, not an oversight.

### 4. A CDN

Geographically distributed HTTP caching. Right for static assets and public cacheable
responses; increasingly used for dynamic content at the edge.

**Costs:** purges are slow (seconds to minutes across all edges), so purging is not a reliable
correctness mechanism. Design for TTL expiry or content-addressed URLs instead.

---

## Selection: Redis versus the alternatives

The full rubric is in
[technology-selection.md](../../../docs/technology-selection.md#worked-example-redis), which
uses Redis as its worked example — read it, it is the eight-question treatment this topic
depends on.

The short version:

| Option | Choose when |
|---|---|
| **In-process LRU** | One process needs it; no sharing required. **Always try this first** |
| **Memcached** | Pure cache, simple values, multi-threaded scaling, and you want fewer features to misuse |
| **Redis** | You need sharing *and* data structures — sorted sets for leaderboards and sliding windows, sets for membership, streams for a simple log. This, not raw speed, is why Redis usually wins |
| **The database itself** | A materialised view, a better index, or the DB's own buffer cache may be enough. Measure before adding a tier |
| **CDN / HTTP caching** | The data is public and URL-addressable. Then the cache is free and global |
| **Valkey** | You want Redis semantics under a BSD licence with foundation governance, after the 2024 licence change |

**When not to use Redis** (the question vendors never answer):

- It would be your only copy of important data. The durability model is weaker than a database's,
  and the failure mode is silent loss of recent writes on an unclean shutdown.
- A single process needs the cache. Local memory is faster and simpler.
- The dataset does not fit in memory and you were relying on eviction to hide that. You will get
  a poor hit ratio, unpredictable latency, and a large bill.
- **The underlying query is slow because it is badly written.** Fix the query.
- You need queries. If you are maintaining secondary indexes by hand in application code, you
  have reimplemented a database badly.
- You need strong consistency across a cluster. Redis Cluster replicates asynchronously; a
  failover can lose acknowledged writes.

---

## Writing the cache-aside path

The default pattern, with the mistakes marked.

```python
def get_product(product_id: str) -> Product | None:
    key = f"v2:product:{product_id}"

    cached = cache.get(key)
    if cached is not None:
        metrics.increment("cache.hit")
        return deserialize(cached)

    metrics.increment("cache.miss")
    product = db.query_product(product_id)
    if product is None:
        # Negative caching, with a much shorter TTL than positive entries.
        cache.set(key, NOT_FOUND, ttl=30)
        return None

    cache.set(key, serialize(product), ttl=jitter(300))
    return product
```

What is load-bearing here:

- **`v2:` in the key.** A schema version. When the serialised shape changes, a deploy must not
  read entries written by the old code. Without this, a rollout means deserialisation errors on
  every hit.
- **`cached is not None`, not `if cached:`.** A cached value of `0`, `""`, or `[]` is falsy and
  would be treated as a miss forever. This is a real bug that survives in codebases for years.
- **Metrics on both paths.** Hit ratio is not observable otherwise, and hit ratio is the number
  that tells you whether any of this was worth doing.
- **Negative caching with a shorter TTL.** Without it, a flood of requests for nonexistent IDs
  bypasses the cache entirely — a cheap denial-of-service vector. With too long a TTL, newly
  created records appear not to exist.
- **`jitter(300)`.** Because 50,000 entries populated during a deploy with an identical TTL all
  expire in the same second.

What is still missing, deliberately, so you can see it:

- **Single-flight.** Concurrent misses on the same key all hit the database. Add it when the
  origin call is expensive.
- **Error handling around `cache.get`.** If the cache is unreachable, this raises and takes down
  your endpoint. Wrap it, log it, fall through to the origin — *if* the origin can take the
  load. That is the decision from question 4 above.

---

## Operating a cache

### Metrics you need from day one

| Metric | Alert when |
|---|---|
| Hit ratio | Drops sharply — a deploy changed key formats, or the working set grew |
| Origin request rate | Rises — the cache is shedding less load than it was |
| p99 on the hit path | Rises — the cache itself is struggling |
| Eviction rate | High while hit ratio is low — too small, or the keys are wrong |
| Memory used and fragmentation ratio | Approaching the limit; fragmentation means real usage exceeds your arithmetic |
| Connection count / blocked clients | Rising — pool exhaustion or a slow command blocking the server |

**Hit ratio alone is not enough.** A 99% hit ratio with a rising origin rate means total traffic
grew; a 99% hit ratio with a rising p99 means the cache is the new bottleneck.

### Configuration that is not optional

For Redis specifically:

- **`maxmemory` and `maxmemory-policy`.** Set both explicitly. *Verified against Redis 7.2
  (2026-08):* the default policy is `noeviction`, which means writes fail with an error once the
  limit is reached rather than evicting. That is almost certainly not what you want from a cache,
  and discovering it under load is unpleasant.
- **Never expose it to a network you do not control.** Redis historically assumed a trusted
  network; internet-reachable instances are compromised routinely and quickly.
- **Test a restore, not just a backup.** A backup you have never restored is a hope.
- **Decide your `SCAN`-versus-`KEYS` policy before an incident.** `KEYS *` blocks the
  single-threaded server for the duration and has taken down production systems.

### Deploys break caches

Three specific hazards:

1. **Changing the serialised shape** while old entries exist. Fixed by the `v2:` key prefix.
2. **Changing the key format**, which silently invalidates everything and gives you a cold cache
   under full traffic. Plan for it, and deploy when you can absorb the origin load.
3. **A restart with no warming.** The cache was protecting the origin from load the origin can
   no longer handle.

Pre-warming — populating the cache before taking traffic — is the standard answer for high-traffic
systems, and it needs to know what to load, which means tracking your hot keys.

---

## Debugging stale data

The `debug` gate. A user reports seeing old data. Work through the layers systematically —
guessing is what makes these bugs take days.

```text
Is it stale for one user or everyone?
  one user  ──► their browser cache, or a per-user cache key
  everyone  ──► shared layer: CDN, app cache, or database replica lag

Does it correct itself after a known interval?
  yes  ──► a TTL. Find which layer has that TTL
  no   ──► an invalidation that never happened, with no TTL backstop

Does it correct on a hard refresh?
  yes  ──► browser or CDN
  no   ──► server-side

Does bypassing your app cache (a debug flag, or a direct query) give the right value?
  yes  ──► your cache
  no   ──► further down: read replica lag, or the ORM identity map
```

The two that catch people out:

**Read replica lag.** Not a cache in the usual sense, and behaves exactly like one. A user
writes to the primary and reads from a replica that has not caught up. The symptom is
indistinguishable from a stale cache, and the fix is different: route reads-after-write to the
primary for a short window.

**DNS.** Resolvers and language runtimes frequently ignore short TTLs. If a failover did not
take effect, suspect DNS caching before suspecting the failover.

---

## Measuring properly

The rules from
[competency-gates.md](../../../docs/competency-gates.md#7-benchmark) apply, with three specific
to caching:

**Measure hit and miss paths separately.** Latency here is bimodal by construction — hits and
misses are two different populations. A blended p99 is a number about nothing.

**Measure with the cache cold, warm, and disabled.** Cold tells you the recovery behaviour, warm
tells you the steady state, disabled tells you what the cache is actually buying. All three are
needed to justify the component.

**Use a realistic key distribution.** Uniform random flatters every cache. Generate Zipfian
traffic for at least one measurement — and if you can, replay real access logs, which is better
than any synthetic distribution.

Watch for coordinated omission: a load generator that waits for each response before sending the
next will not record the latency of requests it failed to send, which makes an overloaded system
look fast.

---

## Anti-patterns

**Caching to hide a slow query.** The query is still slow, and now it fires during a stampede
when the system is already struggling. Fix the query.

**No metrics.** You cannot tell whether the cache is helping, and you will keep it forever out
of superstition.

**No TTL, relying entirely on explicit invalidation.** You will miss a write path. Everyone
does. The TTL is the backstop.

**Truthiness checks on cached values.** `if cached:` treats a legitimately cached `0` or `""` as
a miss.

**Caching per-request data.** Anything varying by user, locale, currency, or permissions must
include it in the key, or you will serve one user another user's data. This is a security bug,
not a performance bug.

**Unbounded caches.** A map with no eviction is a memory leak with good latency.

**Bounding by entry count when values vary in size.** 1,000 entries can be 40 GB.

**A cache in front of a cache in front of a cache**, each with different TTLs and none
documented. Every layer multiplies the worst-case staleness and the debugging surface.

**Silent fallthrough on cache errors** into an origin that cannot take the load. This turns a
cache outage into a total outage.

---

## Next

[exercises.md](exercises.md) — drills including the stampede and distribution measurements, then
[projects.md](projects.md).
