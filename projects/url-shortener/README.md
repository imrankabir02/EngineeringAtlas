# URL shortener

**Level 3** · validates [`caching`](../../topics/backend/caching/README.md),
`backend-development`, `system-design-fundamentals` · any language, real database
required

```console
$ curl -X POST localhost:8000/api/links -d '{"url":"https://example.com/very/long"}'
{"code":"7Kx9mQ","short_url":"http://localhost:8000/7Kx9mQ"}

$ curl -i localhost:8000/7Kx9mQ
HTTP/1.1 302 Found
Location: https://example.com/very/long
```

---

## Why this project exists

A URL shortener is the standard system design interview question, and the reason is
sound: it is small enough to build in a week and contains almost every problem a
real read-heavy service has.

- **Read/write ratio of roughly 1000:1** — the textbook case for caching, and you get
  to verify the textbook with your own numbers.
- **ID generation** — a genuine design decision with three defensible answers and
  different failure modes.
- **Counting under concurrency** — the simplest possible distributed-counter problem,
  and the place where read-modify-write silently loses data.
- **Abuse** — it is a public endpoint that stores user-supplied URLs, so SSRF, open
  redirects, and rate limiting are all real.
- **A findable saturation point** — small enough that you can load test it to
  failure on one machine and identify what broke.

The point is not to have a URL shortener. It is to have measured one.

---

## Stage 1 — Working

Two endpoints, persisted to a real database — Postgres or SQLite, not a process-local
map. An in-memory map removes persistence, concurrency, and every problem worth
having.

**Choose your redirect status code deliberately.** This is the first decision with
real consequences:

| Code | Meaning | Consequence |
|---|---|---|
| `301` Moved Permanently | Cacheable indefinitely by browsers and proxies | Fast for users; **your analytics stop working** because repeat visits never reach you, and you cannot change the target |
| `302` Found | Temporary, not cached by default | Every click reaches you — analytics work, target is changeable, more load |
| `307` Temporary Redirect | Like 302 but preserves the request method | Correct if non-GET requests could be redirected |

Most shorteners use `302` precisely because they want the click. Write down which you
chose and why. If you picked `301` and also want analytics, you have a contradiction
to resolve — and noticing it is the lesson.

**Validate input.** Reject non-`http(s)` schemes (`javascript:` and `data:` URLs are
how an open redirect becomes stored XSS), reject URLs pointing at your own host
(redirect loop), and cap length. See "Break it" for the SSRF case.

---

## Stage 2 — Identified

How do you generate `7Kx9mQ`? Three strategies, and you must compare all three in
writing before choosing:

| Strategy | Mechanism | Good | Bad |
|---|---|---|---|
| **Sequential, base62-encoded** | Auto-increment ID → base62 | Shortest codes, no collisions, no coordination beyond the DB | **Enumerable.** `abc` implies `abd` exists. Anyone can crawl every link, including private ones. Also leaks your total volume |
| **Random** | N random base62 characters | Not guessable, no coordination | Collisions are possible; needs a uniqueness check, which is a read before every write |
| **Hash of URL** | Truncated hash | Same URL → same code, natural deduplication | Truncation causes collisions; two different URLs colliding is a **correctness** bug, not a retry. Also means you cannot have two codes for one URL |

The collision arithmetic matters. With 6 base62 characters there are 62⁶ ≈ 5.7×10¹⁰
codes. By the birthday bound, collisions become likely around √(5.7×10¹⁰) ≈ 240,000
insertions — far sooner than intuition suggests. **Handle collisions explicitly:**
insert with a unique constraint and retry on violation. Do not check-then-insert; that
is a race, and the database constraint is the only thing that actually guarantees
uniqueness.

Test with 100,000 insertions and confirm no duplicates or correct retry behaviour.

**State your threat model.** Enumerable codes are fine for public marketing links
and unacceptable for anything a user assumed was private. The answer is a
requirement, not a preference.

---

## Stage 3 — Fast

Now the caching topic pays off.

First **measure without a cache**: p50, p95, p99 for the redirect path under
concurrent load. You need this baseline or the rest is theatre.

Then add the cache — your own from
[`in-memory-cache`](../in-memory-cache/README.md), or Redis. Measure again. Report
hit ratio.

The redirect lookup is close to an ideal caching candidate: the value never changes
for a given key (unless the link is edited or deleted), the read/write ratio is
enormous, and the working set — recently created and currently popular links — is far
smaller than the total. Be able to state all three of those properties as the
*reason* the cache works here, rather than as a description of what you did.

**Invalidation.** When a link is deleted or edited, the cache must be updated or the
entry removed. Test it. A deleted link that still redirects is a real bug with real
consequences — it is how takedown requests fail.

---

## Stage 4 — Counted

Count clicks without losing any and without slowing the redirect.

**The bug you must avoid:**

```text
count = SELECT clicks FROM links WHERE code = ?
UPDATE links SET clicks = count + 1 WHERE code = ?
```

Under concurrency this loses updates. Two requests read 5, both write 6, and one
click has vanished. It is a lost-update anomaly, and it is the most common
concurrency bug in application code.

Three correct approaches:

| Approach | Mechanism | Trade-off |
|---|---|---|
| Atomic increment in the DB | `UPDATE ... SET clicks = clicks + 1` | Correct and simple; one write per redirect, contention on hot rows |
| Append-only events | Insert a click row; aggregate later | Correct, gives you timestamps and referrers; more storage, count needs a query or rollup |
| Buffer in memory, flush periodically | Increment a local counter, flush every second | Fast, no per-click write; **you lose the buffer if the process dies** |

The third is what high-volume systems do, and it makes the trade-off explicit:
losing up to a second of click counts is usually acceptable; losing a payment is not.
Whichever you choose, **write down what you accepted.**

**Prove it.** Fire 1,000 concurrent redirects for one code and assert the count is
exactly 1,000. Then confirm counting adds no measurable latency to the redirect path,
with numbers.

---

## Stage 5 — Defended

**Rate limiting.** Limit by IP on the creation endpoint. Return `429` with a
`Retry-After` header. A fixed window is simplest; a sliding window or token bucket is
better and explains why — a fixed window allows a burst of 2× the limit across a
boundary. Show it rejecting traffic in a test.

**Find the saturation point.** Load test with increasing concurrency until p99
degrades sharply.

**Predict which resource saturates first.** Write it down before testing. Candidates:
database connection pool, CPU on serialisation, network, the event loop, file
descriptors. Then find out. Most people guess CPU and discover it was the connection
pool.

Do not load test from the same machine as the service — you will be measuring your
load generator's contention as much as the service. And when you report throughput,
always state the latency at that throughput. "10,000 requests per second" with a p99
of 4 seconds is not 10,000 requests per second in any sense a user cares about.

**Behaviour past saturation must be deliberate.** A system that sheds load — returning
`503` quickly — is healthier than one that accepts everything and times out, because
queued requests hold resources while nobody is being served.

---

## Break it

Predict each outcome first.

1. **Load to degradation.** Which resource saturated? Were you right?
2. **Kill the database** while serving traffic. Decide what should happen: serve from
   cache and fail writes, or return `503`? Then make it do that deliberately, rather
   than whatever the driver's default timeout produces.
3. **Kill the cache** under load. Measure the latency step and the database load
   spike. This is the cold-start stampede in a real system.
4. **1,000 concurrent redirects on one code.** Count must be exactly 1,000.
5. **SSRF and loops.** Submit `http://localhost:8000/abc` (loop) and
   `http://169.254.169.254/latest/meta-data/` (the cloud metadata endpoint — the
   classic SSRF target). If your service ever fetches submitted URLs, for example to
   generate previews, this is a live vulnerability. Decide what you block and why.
6. **Garbage input.** A 100,000-character URL. A nonexistent code requested 10,000
   times — note that misses may bypass your cache entirely and hit the database every
   time, which is a denial-of-service vector fixed by negative caching.

---

## Done when

- [ ] Persisted to a real database; survives restart.
- [ ] Redirect status code chosen with a written justification.
- [ ] Three ID strategies compared in writing; collisions handled by a DB constraint.
- [ ] 100,000 insertions with no duplicates.
- [ ] p50/p95/p99 for the redirect path, cache on and off, with hit ratio.
- [ ] Cache invalidation on delete tested.
- [ ] 1,000 concurrent clicks counted exactly.
- [ ] Rate limiting returns `429` with `Retry-After`, tested.
- [ ] Saturation point found, saturating resource named, prediction recorded.
- [ ] Past-saturation behaviour is deliberate.

---

## Anti-patterns

**A process-local map for storage.** Removes every problem the project exists for.

**Auto-increment IDs in URLs without considering enumeration.** Sometimes correct —
but only if you decided.

**Read-modify-write counters.** Loses data under exactly the load you built it for.

**Adding a cache without a before-and-after measurement.** You do not know if it
helped, and you cannot tell your reviewer either.

**Load testing from the service's own machine.** You are measuring your test harness.

**Throughput without latency.** Meaningless in isolation.

---

## Stretch

- **Custom aliases** — introduces reserved words, squatting, and abuse.
- **Expiring links** — decide how expiry interacts with the cache TTL. There are two
  clocks now; that is where the bugs are.
- **Per-user analytics queries** — make one fast with an index, then verify with the
  execution plan that the index is actually used. Your entry to
  `indexing-and-query-optimization`.
- **Two instances behind a load balancer.** Find every piece of state that stopped
  working: your in-process cache is now two divergent caches, your in-memory rate
  limiter allows 2× the limit, and your buffered click counter has two buffers. This
  single exercise is the best possible introduction to
  `distributed-systems-fundamentals`.

---

## Next

Return to [`caching`](../../topics/backend/caching/README.md) for the gates. The
two-instance stretch goal leads directly into `distributed-systems-fundamentals` and
`system-design-fundamentals`.
