# Resource list conventions

The tiering rules and the `why` convention, worked out with real examples. Read this before
writing a topic's `resources.md` or the `resources` block of a `topic.yml`.

Normative rules: [resource-tiers.md](../docs/resource-tiers.md).

---

## The rule that matters most

**Prefer fewer excellent resources.**

Five well-chosen resources are more useful than fifty, because a long list silently transfers the
hardest problem — deciding what to read — back to a learner who is not yet equipped to solve it. That
is the problem curation exists to solve, and a link dump does not solve it.

Targets: 5–15 resources per topic. At least one Tier 1 and one Tier 2. At most five Tier 3.

---

## The `why` field

`why` answers **"why this instead of the twenty alternatives?"** It is not a description.

This is the single most common thing to get wrong, so here it is three times.

### Bad — describes the resource

```yaml
- title: The Linux Programming Interface
  url: https://man7.org/tlpi/
  why: A book about Linux system programming.
```

The reader learns nothing they could not get from the title.

### Better — explains the selection

```yaml
- title: The Linux Programming Interface
  url: https://man7.org/tlpi/
  why: >
    The most complete treatment of the syscall interface, and the reason it is here rather
    than a tutorial: it explains what each call guarantees, which is what you need when a
    call behaves unexpectedly.
```

### Best — also says how to use it

```yaml
- title: The Linux Programming Interface
  url: https://man7.org/tlpi/
  why: >
    The most complete treatment of the syscall interface, and the reason it is here rather
    than a tutorial: it explains what each call guarantees, which is what you need when a
    call behaves unexpectedly. Use it as a reference, not front to back - it is 1,500 pages
    and reading it linearly is a known way to stall.
```

That last sentence prevents a specific, common, expensive mistake. **How to use a resource is
frequently the missing piece**, especially for Tier 1 material written for practitioners rather than
learners.

---

## Tier 1 — primary sources

The thing itself: specifications, RFCs, official documentation, original papers, source code,
release notes, design documents.

**At least one is required per topic.** A topic with no primary source is either not a real
technical topic, or the author never consulted one — both are grounds for rejecting the pull
request.

**Say which sections.** "Read RFC 9111" is unhelpful; "read sections 4 and 5" is usable.
Navigation guidance is most of the value you add at this tier.

Worked examples from written topics:

```yaml
- title: "RFC 9111 - HTTP Caching"
  url: https://www.rfc-editor.org/rfc/rfc9111.html
  why: >
    The specification for the cache you get for free. Read sections 4 and 5 - constructing
    responses from caches, and the header field definitions. It is the clearest existing
    statement of what freshness, validation and staleness mean, and every application-level
    cache reinvents these ideas badly.
```

```yaml
- title: "CPython source - Objects/dictobject.c"
  url: https://github.com/python/cpython/blob/main/Objects/dictobject.c
  why: >
    A production hash table with its reasoning in the comments. Read the header comment on
    the design of compact dicts, not the whole file. Seeing real engineering trade-offs
    annotated by the people who made them is worth more than another explanation of chaining.
```

Note that both say what to read and what to skip. That is the pattern.

---

## Tier 2 — high-quality learning material

Books, university courses with published materials, conference talks by people describing systems
they built, long-form writing that explains mechanisms rather than usage.

**At least one required.**

**The selection test:** would this still be worth reading if every tool it mentions were replaced?
If yes, Tier 2. If no, Tier 3.

**Mark the single best one** if there is one. "If you read one thing, read this" is genuinely
helpful and readers use it.

```yaml
- title: "Code: The Hidden Language of Computer Hardware and Software - Charles Petzold"
  url: https://www.charlespetzold.com/code/
  why: >
    Builds a working computer from switches and relays, one step at a time, with no
    prerequisites. The best available answer to "but how does it actually work" and it never
    requires you to take anything on faith. Roughly 15 hours, and it stays correct forever
    because it is about mechanisms rather than products.
```

**Videos are Tier 2 only** if they are a recorded lecture series with published materials, or a talk
by the system's author. Otherwise Tier 3. Video is hard to search, hard to skim, and impossible to
diff.

---

## Tier 3 — practical

Tutorials, engineering blog posts, videos, reference implementations, interactive tools.

**Cap of five.** If a sixth seems necessary, one of the existing five is not pulling its weight.

Tier 3 is where tutorial hell lives — the most comfortable material and the least durable. It is
included because one concrete working example is often the fastest way past a blocker. But the
*concept* comes from Tier 1 or 2.

```yaml
- title: "A Gallery of Processor Cache Effects - Igor Ostrovsky"
  url: https://igoro.com/archive/gallery-of-processor-cache-effects/
  why: >
    Run these, do not just read them. Seven small experiments where the only change is the
    memory access pattern and the runtime changes by an order of magnitude. The most
    convincing demonstration available that complexity analysis is not the whole story.
    Predict each result before running; you will be wrong on at least three.
```

---

## Rules that get pull requests rejected

1. **No affiliate links, referral codes, or undisclosed self-promotion.** Linking your own material
   is fine; say so in the `why`.
2. **No paywalled resource as the only route** through a concept. Paid material may be listed —
   some books are simply the best available — but a learner without a budget must have a viable path.
3. **No link aggregators.** Do not link to another list. Link to the thing.
4. **Date-sensitive resources must say so** in the `why`, and the topic's `version_sensitivity`
   must reflect it.
5. **Prefer stable URLs.** Canonical documentation over versioned, DOIs over PDF mirrors.
6. **No duplicate URLs** within a topic. The validator checks this.

---

## The "deliberately not here" section

Every topic's `resources.md` should end with the notable absences **and their reasons**. This is
frequently more useful than the list itself, because it saves the reader from the obvious wrong
choices.

Standard candidates, with the shape of a good reason:

> **CLRS (*Introduction to Algorithms*).** The standard reference, and genuinely excellent — as a
> *reference*. It is written for a rigorous course with mathematical maturity assumed, and reading it
> front to back at Level 2 is a common way to stall. Get it when you reach `algorithms` and use it
> to look things up.

> **LeetCode and similar.** Useful later for `algorithms`, unhelpful now. They train retrieval of
> solutions on a fixed problem set, which is not the skill this topic builds, and they will make you
> feel incapable for reasons unrelated to your progress.

> **Framework tutorials.** Not yet. See the framework-first anti-pattern.

Reasons, not just names. A bare "not included: CLRS" tells the reader nothing.

---

## When good material genuinely does not exist

Sometimes the knowledge is tribal, or spread across mailing-list threads and source comments.

Say so, and provide a route:

```yaml
tier1:
  - title: The source (kernel networking stack, net/ipv4)
    url: https://github.com/torvalds/linux/tree/master/net/ipv4
    why: >
      There is no good secondary treatment of this at the level of detail required. Read
      tcp_input.c alongside RFC 9293. Start at tcp_v4_rcv() and follow the path; expect this
      to take days, not hours.
```

That is more honest and more useful than padding the list with three mediocre blog posts, and it
teaches the learner something true about where knowledge lives at Level 4.
