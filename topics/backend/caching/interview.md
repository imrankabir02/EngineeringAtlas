# Caching — interview

Caching appears in nearly every system design interview, and the difference between a strong and
weak candidate is almost never knowledge of Redis commands.

**This is not a question bank.** What follows are discussion shapes: what a competent answer
contains, and what a shallow one reveals.

[← Caching](README.md) · [Concepts](concepts.md) ·
[Advanced](advanced.md)

---

## What is being assessed

At Level 3 and above, interviews test **judgment**, and caching is a good instrument for it
because the naive answer is always available and always incomplete.

Three things being watched:

1. **Do you add a cache reflexively, or after establishing that it helps?** The reflex is the
   most common weak signal in system design interviews.
2. **Do you volunteer the costs?** Anyone can say "add a cache". Naming staleness, stampedes, and
   the new failure domain unprompted is what separates levels.
3. **Can you turn a technical trade-off into a product decision?** "How stale can this be?" is
   the question strong candidates ask and weak ones never do.

---

## Discussion 1 — "This endpoint is slow. What do you do?"

**A shallow answer:** "Add a cache."

This is the single most common way to lose credit in a system design interview, and it is almost
a reflex for people who have read about caching without operating one.

**A competent answer:**

> First I'd want to know *why* it is slow — I'd look at a trace or a profile. There are three
> common answers and only one of them wants a cache.
>
> If one query is slow because of a missing index, caching it gives me a slow query that fires on
> every miss, at the worst possible moment. If the endpoint is making 200 queries in a loop, a
> cache hides the N+1 until the cache is cold, and then the collapse is worse than the original
> problem. If it is a reasonably fast query called 50,000 times a second, *now* a cache is the
> right tool.
>
> Assuming it is the third case, before designing I'd want to know how skewed the access pattern
> is, because hit ratio is a property of the workload rather than of the cache — and how stale the
> data can be, which is a product question.

**The tells:** refusing to skip the diagnosis, and naming the two cases where caching is the wrong
answer. Interviewers are frequently *hoping* you will say "add a cache" so they can ask what
happens when the query is genuinely slow.

---

## Discussion 2 — "How do you handle cache invalidation?"

**A shallow answer:** "Set a TTL." Or worse: "Invalidate on write."

**A competent answer:**

> Four options, and the choice depends on how stale the data can be.
>
> TTL is the default: simple, and it converts "the cache might be wrong" into "the cache is wrong
> for at most 60 seconds", which is a statement a product owner can agree to. Explicit
> invalidation on write is fresher but requires finding every write path — including admin tools,
> batch imports, and migrations, and there is usually one you missed. Write-through keeps the cache
> never-stale but only works if everything writes through your code. Versioned keys avoid the
> races entirely at the cost of a version lookup.
>
> In practice I'd use TTL plus explicit invalidation on the paths I control, with the TTL as the
> backstop for the paths I missed.
>
> There's also a race in cache-aside that is worth mentioning: a reader can miss, read the old
> value, and then store it *after* a concurrent writer has invalidated — so a stale value gets
> cached with nothing to expire it. That's a specific reason never to rely on invalidation alone.

**The tells:** four options with trade-offs rather than one answer; the phrase "the paths I
missed"; and the populate-after-write race, which most candidates have never encountered and which
demonstrates you have thought about concurrency in a cache.

---

## Discussion 3 — "Design a caching layer for a product catalogue"

This is a design question, and the structure of your answer matters more than your conclusions.

**A competent approach:**

> I'd start by separating the data by how it behaves. A product page usually contains several
> things with very different staleness tolerances: the description and images change rarely and can
> be cached for hours; the price changes occasionally and might tolerate minutes; the stock level
> changes constantly and probably cannot be cached at all, or only for a couple of seconds.
>
> So I would not cache "the product page" as one object. I'd cache the slow-changing parts
> aggressively and compose the volatile parts on each request. If stock is cached for 60 seconds,
> we oversell, and that is a business cost someone has to accept explicitly.
>
> For placement, I'd work from cheapest upward: images and static assets go to a CDN with
> content-addressed URLs and a one-year TTL, which needs no invalidation at all. The product
> description could be an HTTP-cacheable response. Only what's left needs an application cache.
>
> For keys, everything that affects the value has to be in the key — product ID, locale, currency,
> and whether the user is logged in if we personalise. Missing one of those means serving one
> user's content to another, which is a security bug rather than a performance bug.

**The tells:** decomposing by staleness tolerance rather than caching the page; naming the
business consequence of caching stock; working from cheapest layer upward; and the key-design
security point.

---

## Discussion 4 — "What happens when your cache goes down?"

Frequently asked, and it separates people who have operated a cache from people who have added
one.

**A shallow answer:** "Requests go to the database."

Which is often true and is a description, not a decision.

**A competent answer:**

> That depends on whether the database can handle full traffic, and usually it cannot — that is why
> the cache exists. So "fall through to the origin" can turn a cache outage into a total outage.
>
> It needs to be a deliberate decision, made in advance. The options are: degrade to the origin if
> it can cope, possibly with load shedding so we serve some requests properly rather than all
> requests badly; fail fast with a 503, which is unpleasant but keeps the database alive; or serve
> stale data from a local in-process cache if we have one, which is often the best answer for
> reads.
>
> The related failure is a cold start — the cache comes back empty and everything misses at once.
> That is the same stampede shape system-wide, which is why high-traffic systems pre-warm before
> taking traffic.
>
> The general point is that the cache became a system-wide dependency, so it needs the same
> availability thinking as the database.

**The tells:** recognising that falling through can be worse than failing; treating it as a
decision rather than a default; and connecting a cache outage to a cold-start stampede.

---

## Discussion 5 — "Your cache has a 99% hit ratio but p99 latency got worse. Explain."

A good diagnostic question, and it rewards having measured something.

**A competent answer:**

> Most likely the 1% of misses. They now pay the cache lookup *plus* the origin cost, and if the
> cache is a network hop that addition lands squarely in the tail. Before the cache, everything
> paid the origin cost; now 1% pays slightly more than that, and p99 is exactly where that shows.
>
> Other possibilities: the cache itself is becoming a bottleneck — if it is single-threaded, one
> slow command blocks everything else, so I'd check for blocked clients and slow commands. Or
> misses are clustered rather than uniformly distributed, so there is a stampede that a blended hit
> ratio hides.
>
> The way to tell them apart is to measure hit and miss paths separately. A blended p99 across
> hits and misses is a number about nothing, because the distribution is bimodal by construction.

**The tell:** the bimodal-distribution point. It shows you have measured a cache rather than read
about one, and it is the single most useful measurement discipline in the topic.

---

## Discussion 6 — "Redis or Memcached?"

**A shallow answer:** "Redis, it's more popular." Or a feature list.

**A competent answer:**

> It depends what I need beyond a cache. If it is purely a cache of simple values, Memcached is
> multi-threaded, simpler, and has fewer features to misuse — which is a genuine advantage.
>
> Redis wins when I need its data structures: sorted sets for leaderboards or sliding-window rate
> limits, sets for membership, streams for a simple log. That, not raw speed, is usually the
> deciding factor.
>
> Two things I'd be careful about with Redis. Command execution is single-threaded, which gives
> nice atomicity but means one expensive command — a `KEYS *` or a heavy Lua script — blocks every
> other client. And it is not a durable store: the persistence options exist but the failure mode
> on an unclean shutdown is losing recent writes, so it should not hold the only copy of anything
> that matters.
>
> I'd also ask whether I need a separate cache at all. An in-process LRU is faster and simpler if
> only one process needs it, and a `Cache-Control` header is free if the data is public and
> URL-addressable.

**The tells:** asking what is needed beyond caching; naming the single-threaded consequence;
stating the durability limit; and questioning whether the component is needed at all. That last
move is consistently the strongest thing a candidate can do.

---

## Shallow-answer tells, generally

In roughly increasing severity:

**Adding a cache before diagnosing.** The most common weak signal in this area.

**Naming products instead of properties.** "I'd use Redis" before establishing what needs to be
fast, how stale it can be, and whether the workload has locality.

**No mention of staleness.** A caching design that never says how wrong the data can be is
incomplete, and it signals the candidate has not owned one in production.

**No mention of stampedes or cold starts.** These are the failures that cause incidents. Not
mentioning them suggests the cache has never actually failed on you.

**Treating hit ratio as a property of the cache.** "We'll get 90%" without reference to the access
distribution.

**Forgetting the key.** Not asking what the value varies by. In a real system this is a data-leak
bug.

**No metrics.** A design with no hit-ratio measurement cannot be evaluated or tuned, and will be
kept forever out of superstition.

---

## Where caching appears in system design interviews

Almost everywhere, usually as one part of a larger design. In the standard exercises:

| Exercise | The caching question |
|---|---|
| URL shortener | Read-heavy, immutable values. Nearly ideal — and the interesting part is negative caching against nonexistent-code floods |
| News feed | What is cacheable when every user's feed differs? Fan-out on write versus read, and caching the *components* rather than the feed |
| E-commerce product page | Different staleness per field. The stock-level problem from discussion 3 |
| Rate limiter | The cache *is* the system, and now it must be strongly consistent enough to count — which caches are bad at |
| Video streaming | CDN, and the fact that content-addressed URLs make invalidation free |
| Search | Caching results per query, and the long tail of unique queries destroying your hit ratio |

The last row is worth internalising: **search queries have a long tail**, so a naive
cache-the-results-per-query design has a poor hit ratio no matter how much memory you give it.
Recognising a workload that resists caching is as valuable as recognising one that suits it.

---

## Practising this properly

Two things, in order.

**Do [the project](projects.md).** It gives you sentences nobody else has: "I measured 500 origin
calls on a cold key, added single-flight, and got 1." "I measured 10% hit ratio on uniform traffic
and 90% on Zipfian with the same cache." Concrete measurements you took are worth more than any
amount of fluent theory, and interviewers can tell the difference immediately.

**Work the `explain` and `design` gates out loud.** Particularly the product-owner one —
explaining "up to 60 seconds stale" without using the word cache. It is a genuine skill, it is
assessed in senior interviews, and it is nearly impossible to do well without having rehearsed it.

Per [philosophy.md](../../../docs/philosophy.md#interview-question-memorisation): do not memorise
system design answers. They collapse the moment the interviewer changes a constraint, and changing
a constraint is precisely what they are there to do. Derive from the chain in
[fundamentals.md](fundamentals.md) instead — locality, then invalidation, then eviction, then
stampedes — and you can answer questions nobody has posted.
