# Caching — exercises

Twenty-four drills. The measurement and break-it groups are where the topic actually lands.

**Rules:**

- **Predict every number before measuring.** Write it down, unedited.
- Anything in front of a "cache" must front something with **real cost** — a database, a file
  read, or a function with injected latency. A stub returning a constant makes every measurement
  meaningless.
- Use an injected clock for expiry tests. No `sleep`.

[← Caching](README.md) · [Concepts](concepts.md) ·
[Practical](practical.md) · [Projects](projects.md)

---

## Decide whether to cache at all

**1.** For each scenario, decide whether to add a cache, and state the deciding factor:

- a product page read 10,000 times/second, updated twice a day
- a report aggregating every order ever placed, run once a month
- a user's notification count, read on every page load, changing several times a minute
- a query taking 4 seconds because of a missing index
- an endpoint making 200 database queries in a loop
- a currency conversion table, read constantly, updated daily
- a bank account balance, read frequently, must be exact

Two of these should be "no", and one should be "fix something else first".

**2.** Take a real access log — your own project's, or generate one — and plot request counts per
key, sorted descending. Is the distribution flat or skewed? What hit ratio would a cache holding
10% of the keys achieve? Compute it from the data.

**3.** For a piece of data in a system you have built, write down the staleness budget in seconds
and one sentence justifying it. Then write the sentence you would say to a non-technical
stakeholder to get their agreement.

---

## Invalidation

**4.** Implement cache-aside over a real datastore. Write to the datastore directly, bypassing
the cache, then read through the cache and **measure how long the wrong value is served.**

**5.** Reproduce the populate-after-write race from
[fundamentals.md](fundamentals.md#explicit-invalidation): a reader reads V1, a writer writes V2
and invalidates, then the reader stores V1. You will need to control the interleaving —
instrument the code with a pause point. Then explain why a TTL is a necessary backstop.

**6.** Implement versioned keys (`user:123:v7`) and demonstrate that the race in exercise 5
cannot occur. Then state what the version scheme costs you.

**7.** Take a system you have built and find **every** write path to one cached entity. Include
admin tools, scripts, and migrations. Write them down. Were you confident you had them all
before you started looking?

**8.** Implement write-through, then kill the process between the cache write and the datastore
write. What state are you in? Now do write-behind and kill it before the flush. Which failure is
worse, and for what kind of data?

---

## Eviction

**9.** Implement LRU with O(1) `get` and `put`. Write a test asserting **which** key was evicted,
not merely that eviction happened.

**10.** Set capacity to 1 and drive a workload alternating between two equally hot keys. Predict
the hit ratio, measure it, and explain the number.

**11.** Implement LFU alongside your LRU. Compare hit ratios on a Zipfian workload. Then shift
the popular set halfway through the run — which policy adapts, and which does not?

**12.** Implement random eviction. Compare its hit ratio with LRU on a Zipfian workload. Predict
the gap first; most people expect random to be far worse than it is.

**13.** Bound your cache by entry count, then store values of wildly varying size until memory is
exhausted. Then re-bound by bytes. Explain why real caches do the second.

---

## Stampedes

**14.** With a cold cache, fire 500 concurrent requests for the same key against an origin that
takes 50 ms and counts its calls. Predict the count. Measure it. Explain.

**15.** Implement single-flight and repeat exercise 14. Report the new origin call count and the
p99 latency of the waiters. What did you trade?

**16.** Populate 10,000 entries with an identical TTL. Wait for expiry under load. Measure origin
requests per second at that moment. Then add jitter and repeat.

**17.** Implement stale-while-revalidate. Demonstrate that no request waits for the refresh, then
state precisely which guarantee you gave up and for how long.

**18.** Restart your process under sustained load with a cold cache. Graph origin latency and
error rate during recovery. How long until it stabilises?

---

## Layers and HTTP

**19.** Serve a file over HTTP with `Cache-Control: max-age=60` and observe, in browser devtools,
that a reload within 60 seconds makes no request. Then add an `ETag` and observe the `304` on
revalidation. What did the `304` save?

**20.** Set up the content-addressed pattern: a filename containing a content hash and a
one-year `immutable` TTL. Change the file, change the URL, and observe that no purge was needed.

**21.** Find three caches in a system you have built that you did not add. Name what each caches
and what invalidates it.

**22.** Write a cache key for a product page that varies by product, locale, currency, and
whether the user is logged in. Then write the key someone would carelessly write, and describe
the security bug it causes.

---

## Break it

`break` gates. Predict everything first.

**B1.** Exercise 14, and keep the graph.

**B2.** Exercise 10, and explain the hit ratio you measured.

**B3.** Exercise 4, and record the staleness duration.

**B4.** Exercise 18, the cold restart under load.

**B5.** Exercise 13, memory exhaustion under an entry-count bound.

**B6.** Make your origin 2 seconds slow. Determine whether your cache **absorbs or amplifies**
the latency on the miss path. If you have single-flight, note that 500 waiters now all wait 2
seconds — is that better or worse than 500 concurrent origin calls? Argue both sides.

**B7.** Cache a value under a key that omits the locale. Request the page as two users with
different locales and observe the wrong content served. This is the security bug from exercise
22, made real.

---

## Measure and explain

`benchmark` and `explain` gates. These are the deliverables.

**M1.** Report p50/p95/p99 for the **hit path**, the **miss path**, and **cache disabled**.
Exclude warm-up. Record the setup. Explain why a blended percentile across hits and misses is
meaningless.

**M2.** Measure hit ratio with the same cache under a **uniform** and a **Zipfian** key
distribution. Predict both first. Explain the gap.

This is the most important measurement in the topic. If your two numbers are similar, your
"Zipfian" generator is probably not skewed — check that a small number of keys really do account
for most requests.

**M3.** Measure the marginal value of capacity: hit ratio at 1%, 5%, 10%, 25%, and 50% of the
keyspace. Plot it. Where does doubling the memory stop being worth it? This is how cache capacity
is actually decided.

**M4.** Write up, one to two paragraphs each:

- Cache-aside versus write-through, and when each is wrong.
- Why hit ratio is a property of the workload, using your M2 numbers.
- What "up to 60 seconds stale" means for a specific feature — **without using the word cache**.
  Aim it at a product owner.

**M5.** *(Design gate.)* Design the caching strategy for a product page showing live stock levels
and a slowly-changing description. State what you cache, for how long, what you deliberately do
not cache, and how the page composes both. Then state what breaks if stock is cached for 60
seconds.

---

## Answers to check yourself

<details>
<summary>Expand after attempting</summary>

**1.** Product page: **yes** — high read/write ratio, ideal. Monthly report: **no** — no temporal
locality, one read per month; a materialised view or a scheduled job is the right tool.
Notification count: **borderline** — high read rate but frequent invalidation; a very short TTL
(a few seconds) or accepting a slightly stale count is defensible, and it should be a product
decision. Missing index: **fix the index first** — caching a 4-second query gives you a 4-second
query on every miss. N+1 in a loop: **fix the N+1** — a cache hides it until it is cold, when the
collapse is worse. Currency table: **yes**, and in-process, since it is small and shared by every
request. Bank balance: **no** for the authoritative read — though caching for display with a
visible "as of" timestamp is a legitimate product decision.

**5.** The reader's `set` lands after the writer's `delete`, so V1 is cached with no expiry. A TTL
bounds the damage. Versioned keys eliminate it, because the reader would be writing to a key
nobody reads any more.

**8.** Write-through killed mid-operation: the cache has V2 and the datastore has V1 — the cache
is *ahead* of the truth, which is unusual and confusing, and a subsequent invalidation makes it
self-correct. Write-behind killed before flush: the write is **lost**, and it was acknowledged to
the client. Far worse for anything a user or auditor will check; acceptable for click counters.

**10.** Roughly 0%. With capacity 1 and two alternating keys, every access evicts the key you are
about to need. This is called thrashing, and it is why a cache smaller than the working set can be
worse than no cache at all.

**12.** Random is usually within a few percentage points of LRU on skewed workloads, because a hot
key is likely to be re-inserted immediately after being evicted, while cold keys are not. It is
much cheaper — no ordering, no lock on a shared list — which is why it is a serious choice at scale.

**14.** 500 origin calls. Nothing coordinates the misses. On a real system this is how a cache
restart takes down the database it was protecting.

**15.** 1 origin call. The trade: 499 requests now block waiting for one origin call, so their p99
is the origin's latency rather than 500 concurrent origin calls' latency. Usually a good trade;
see B6 for when it is not.

**19.** The `304` saved the response *body* — the round trip still happened, but no payload was
transferred and the origin did not have to render. Useful for large resources, of limited value
for small ones where headers dominate.

**22.** The careless key is `product:123`. With locale and currency omitted, the first user to
request the page populates the cache, and every subsequent user gets that user's locale, currency,
and — if login state is also omitted — potentially their personalised content. The last case is a
data-leak vulnerability, not a display bug.

**B6.** Neither answer is universally right. 500 concurrent origin calls may crush the origin,
making everyone's latency far worse than 2 seconds. 500 waiters on one call gives predictable
2-second latency and a healthy origin, but if the origin hangs entirely, all 500 hang with it —
which is why single-flight needs a timeout on the waiters.

**M2.** Uniform over a keyspace 10× the cache size gives roughly 10%. Zipfian with skew near 1.0
gives 80–90% with the same cache. The cache is identical; the workload decided.

</details>

---

## Next

[projects.md](projects.md) — build it, then break it.
