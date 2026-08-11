# Data structures — interview

This topic dominates technical interviews more than any other, and it is also the topic
where memorisation is most tempting and most transparent.

**This is not a question bank.** What follows are discussion shapes: what a competent answer
contains, and the tells that separate reasoning from recall.

[← Data structures](README.md) · [Concepts](concepts.md) ·
[Advanced](advanced.md)

---

## What is actually being assessed

Not whether you can implement a red-black tree. Three things:

1. **Can you choose a structure from an access pattern?** By far the most common assessment,
   and the most job-relevant.
2. **Do you know the costs, including the worst cases?** Especially whether the worst case is
   reachable in practice.
3. **Can you reason about the gap between theory and reality?** This is what distinguishes a
   strong Level 2 candidate from a memoriser, and almost nobody prepares for it.

The third one is your advantage. Everyone has memorised that a hash table is O(1). Almost
nobody can explain why their implementation was 20× slower than the standard library's, and
saying so credibly marks you immediately.

---

## Discussion 1 — "How would you find the top 10 items from a stream of a million events?"

**A shallow answer:** "Sort them and take the first ten."

Correct output, wrong engineering, and it signals no cost awareness.

**A competent answer:**

> Sorting is O(n log n) and needs all million in memory. If I only need ten, a min-heap of size
> 10 is better: for each item, if it beats the heap's minimum, replace it. That is O(n log 10),
> which is effectively O(n), and it holds ten items regardless of stream size — so it also works
> when the stream does not fit in memory.
>
> If I need counts per item first — "top 10 most frequent" rather than "top 10 largest" — I need
> a hash map for the counts as well, and then the heap over that. And if the key space is huge
> and approximate answers are acceptable, a count-min sketch would bound the memory.

**The tells:** choosing the heap for a stated reason, noting the memory property, distinguishing
*largest* from *most frequent*, and mentioning the approximate option as a possibility rather
than a recommendation.

**Follow-up you should survive:** *"What if you need the top 10 for each of a million
categories?"* Now you have a million heaps and memory is the constraint. Good answers start
questioning the requirement, discussing bounded per-category state, or moving to a streaming
system. Recognising when a problem has outgrown in-memory structures is a real signal.

---

## Discussion 2 — "Why is a hash table O(1)? Is it always?"

**A shallow answer:** "Because hashing gives you the index directly."

Half the answer, and it omits every interesting part.

**A competent answer:**

> On average, because the hash spreads keys across slots so a lookup is one hash computation
> plus a small constant number of probes. It is not always: if many keys collide, lookups
> degrade toward O(n), and in the worst case — every key in one slot — it *is* O(n).
>
> That worst case is reachable in practice, not just in theory. It was a real
> denial-of-service technique: send a request with hundreds of parameters engineered to collide
> in the framework's hash function, and the server spends quadratic time parsing it. The
> standard mitigation is hash randomisation, a per-process seed so an attacker cannot predict
> collisions. Java's HashMap also converts a bucket to a tree after 8 collisions, which bounds
> the worst case at O(log n).
>
> The other thing that stops it being O(1) is load factor. As the table fills, collisions rise,
> and the curve is flat and then it isn't. Implementations resize around 0.7 for that reason. I
> measured the curve myself — it's flat to about 0.7 and then climbs sharply.

**The tells:** naming a *reachable* worst case with a real-world example, knowing the
mitigations, and having measured the load-factor curve. That last clause is unusual and it lands.

---

## Discussion 3 — "When would you use a tree instead of a hash table?"

**A shallow answer:** "When you need it sorted."

Correct and thin.

**A competent answer:**

> When I need any operation that depends on order: sorted iteration, range queries — "all keys
> between X and Y" — or next-largest-key. A hash table cannot answer any of those without
> examining every entry, because hashing deliberately destroys the ordering.
>
> The trade is O(log n) instead of O(1) for plain lookup, plus worse locality from the pointer
> chasing. So: hash table by default, tree when order is a requirement.
>
> It is also why database indexes are B-trees rather than hash indexes — `WHERE created_at >
> '2026-01-01'` is a range query, and that is most real queries. Some databases offer hash
> indexes for exact-match-only workloads, and they are rarely worth the loss of flexibility.

**The tell:** the database connection. It shows the concept is connected to something real
rather than held in isolation, and it is the natural bridge to
`indexing-and-query-optimization`.

---

## Discussion 4 — "Implement an LRU cache"

The most common structural-design question at this level, and it is a good one.

**A weak answer** reaches for a dict plus timestamps, then scans to find the oldest — O(n) per
eviction.

**A competent answer** identifies the requirement first:

> I need O(1) lookup by key *and* O(1) identification and removal of the least recently used
> item. No single structure gives me both: a hash map has no ordering, and a list has no fast
> lookup.
>
> So I combine them. A hash map from key to node, and a doubly linked list ordered by recency.
> On `get`, the map gives me the node directly, I unlink it and push it to the head — O(1)
> because I never traverse. On eviction, I drop the tail and remove its key from the map.
>
> It has to be doubly linked so I can unlink a node in O(1) without knowing its predecessor.

**The tells:** stating the two requirements *before* choosing, recognising that neither
structure alone suffices, and explaining specifically why *doubly* linked.

**Follow-up you should survive:** *"Make it thread-safe."* A single lock around the whole
structure, because every `get` mutates the shared list head — so per-entry locks do not help.
Then, if pushed: shard by key hash into N independent caches to reduce contention, accepting
that each shard now evicts independently, which changes the semantics slightly. Naming that
trade-off is a strong signal.

You will have built this in
[the cache project](../../../projects/in-memory-cache/README.md), which means you can talk
about the race you actually caused rather than the one you imagine.

---

## Discussion 5 — "Your code is fast in testing and times out in production. Where do you look?"

A judgment question disguised as a debugging question.

**A competent answer** enumerates before guessing:

> Most likely something that is fine at test scale and quadratic at production scale. The usual
> suspects: a membership check against a list instead of a set inside a loop; a lookup that
> scans a collection instead of using a prebuilt map; string concatenation in a loop; or sorting
> inside a loop.
>
> The way to find out rather than guess: profile it at production-like data volume. If I cannot
> profile production, I would reproduce the data *shape* — not just the size but the
> distribution, because skew changes behaviour.
>
> The other possibility is that the structure is fine and the data no longer fits in memory, in
> which case it is swapping and the answer is a different architecture, not a different
> structure.

**The tells:** naming specific plausible causes, insisting on measurement, and considering that
the answer might be outside the structure entirely.

---

## Discussion 6 — "Why is your implementation slower than the standard library's?"

Rarely asked directly. Enormously valuable when you volunteer it, because it demonstrates you
have measured something.

**A competent answer:**

> Same complexity, different constants. Three main reasons in my case: the built-in is compiled
> C rather than interpreted; it stores values contiguously rather than as pointers to boxed
> objects, so it gets far better cache locality; and it has a specialised fast path for common
> key types that skips generic dispatch.
>
> The general lesson I took from it is that complexity analysis narrows the candidates and
> measurement decides. I've had cases where a linear scan over a small contiguous array beat a
> hash table, purely because of locality.

**The tell:** naming mechanisms rather than saying "it's optimised", and drawing the general
conclusion. This is the answer that most reliably distinguishes someone who did the
[project](projects.md) from someone who read about it.

---

## Shallow-answer tells, generally

In roughly increasing severity:

**Reciting complexities with no context.** "Insertion is O(1) amortised" without being able to
say what happens on the non-amortised operation, or when that matters.

**No worst cases.** Claiming O(1) for hash tables with no mention of collisions or load factor.
It signals memorisation from a table.

**Choosing the structure before understanding the problem.** Naming a structure in the first
sentence, before asking about access patterns or scale.

**No magnitudes.** "Sets are faster than lists" is not a model. "About 100× at 100,000 items,
because the list version is quadratic" is.

**Never questioning the requirement.** The strongest candidates ask "does it need to be exact?"
and "how many items, realistically?" before designing.

**Treating Big-O as the whole answer.** The tell here is being *unable* to explain why two
same-complexity implementations differ by 10×. Most candidates cannot, so being able to is
disproportionately valuable.

---

## On grinding problem sets

A direct position, since this is the topic where the temptation is strongest.

Competitive programming sites are **useful later, for `algorithms`, and not now.** They train
retrieval of solutions on a fixed problem set, which collapses under perturbation — and the
interview is the perturbation. They also correlate poorly with the actual job, where the
structure choice matters and the clever trick almost never does.

What to do instead, in order of value:

1. **Do [the project](projects.md).** It gives you the measurement stories that make you
   credible, and nobody else has them.
2. **Practise the choosing skill.** Exercise 1 in [exercises.md](exercises.md) is eight
   requirements needing eight different answers with justifications. That is the actual
   interview skill.
3. **Practise the `design` gate**: "top 10 trending from 100,000 events per second." Out loud.
   To a person.
4. **Then**, if you want problem-set practice, do 20–30 problems slowly, deriving each one, and
   for each write down which structure you chose and why. Twenty derived beats two hundred
   memorised.

The `explain` gates in [`topic.yml`](topic.yml) are the highest-value preparation available,
because they force articulation, and articulation is what an interview measures.
