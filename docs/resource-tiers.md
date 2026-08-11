# Resource Tiers

Every resource in this repository is tiered and carries a `why`. A link without a
reason for existing is not curation; it is a bookmark you inflicted on someone.

**The rule that matters most: prefer fewer excellent resources.** A topic with
five well-chosen resources is more useful than one with fifty, because the second
one silently transfers the hardest problem — deciding what to read — back to a
learner who is not yet equipped to solve it.

---

## Tier 1 — Primary sources

The thing itself, written by the people who made it or who define it.

- Official documentation and specifications
- RFCs and standards (IETF, W3C, POSIX, ECMA, ISO)
- Academic papers, especially the original paper for an idea
- Source code of the implementation
- Release notes, design documents, and architecture decision records

**When to use:** when you need to be *right*. Every non-trivial question is
eventually answered here and nowhere else.

**Why it goes first:** primary sources are more accurate, more stable, and
usually more concise than the material written about them. They are also where
you learn that documentation *can* be read directly — a skill many engineers
never acquire, and a hard prerequisite for Level 4.

**Cost:** written for practitioners, not learners. They assume the model you are
trying to build. This is exactly why Tier 2 exists.

**Every topic must have at least one Tier 1 resource.** If a topic has none, it
is either not a real technical topic or the author has never consulted the
primary source — both are grounds for rejecting the pull request.

---

## Tier 2 — High-quality learning material

Material built to *teach* the concept, by someone with authority, with enough
depth to still be useful in two years.

- Books, especially ones that survived a decade
- University courses with published materials (MIT OCW, Berkeley CS, CMU DB)
- Conference talks by people describing systems they built
- Long-form technical writing that explains mechanisms rather than usage

**When to use:** to build the mental model before or alongside the primary
source. This tier does the work of ordering ideas and choosing what to omit,
which is most of what teaching is.

**Selection test:** would this still be worth reading if the current version of
every tool it mentions were replaced? If yes, Tier 2. If no, it is Tier 3.

---

## Tier 3 — Practical material

Concrete, current, task-oriented, and expected to age.

- Tutorials and how-to guides
- Engineering blog posts describing a specific production system
- Videos and screencasts
- Example repositories and reference implementations

**When to use:** to get moving, to see a real configuration, or to learn how a
company solved a problem at a scale you have not seen.

**Cost:** Tier 3 is where tutorial hell lives. It is the most comfortable
material and the least durable. It is included because seeing one concrete
working example is often the fastest way past a blocker — but the *concept*
should come from Tier 1 or 2.

**Cap:** at most five Tier 3 resources per topic. If a sixth seems necessary, one
of the existing five is not pulling its weight.

---

## Writing the `why`

The `why` field is not a description. It answers: *why is this here instead of
the twenty alternatives?*

Bad — describes the resource:

```yaml
- title: The Linux Programming Interface
  url: https://man7.org/tlpi/
  why: A book about Linux system programming.
```

Good — explains the selection:

```yaml
- title: The Linux Programming Interface
  url: https://man7.org/tlpi/
  why: >
    The most complete treatment of the syscall interface, and the reason it is
    here rather than a tutorial: it explains what each call guarantees, which is
    what you need when a call behaves unexpectedly. Use it as a reference, not
    front to back.
```

The second version tells the learner *how to use it*, which is often the missing
piece. It also implicitly warns them not to try reading a 1,500-page book
linearly.

---

## Rules

1. **No affiliate links, no referral codes, no self-promotion without
   disclosure.** A maintainer or contributor linking their own material must say
   so in the `why`.
2. **No paywalled resource as the only option** for a concept. Paid material may
   be listed — some books are simply the best available — but a learner without a
   budget must have a viable route through every topic.
3. **No link aggregators.** Do not link to another list. Link to the thing.
4. **No videos in Tier 1 or 2** unless it is a recorded lecture series with
   published materials, or a talk by the system's author. Video is hard to
   search, hard to skim, and impossible to diff.
5. **Date-sensitive resources must say so** in the `why` — "accurate as of
   Kubernetes 1.29" — and the topic's `version_sensitivity` must reflect it.
6. **Dead links are bugs.** A scheduled job checks external URLs; a broken link
   is fixed or removed, not left as an artifact.
7. **Prefer the stable URL.** Canonical documentation URLs over versioned ones,
   DOIs over PDF mirrors, `man7.org` over a random man-page mirror.

---

## What to do when a resource genuinely does not exist

Sometimes the good material for a topic is not public: it is tribal knowledge,
or it is spread across mailing-list threads and source comments.

Say so, and provide a route:

```yaml
tier1:
  - title: The source (kernel networking stack, net/ipv4)
    url: https://github.com/torvalds/linux/tree/master/net/ipv4
    why: >
      There is no good secondary treatment of this at the level of detail
      required. Read tcp_input.c alongside RFC 9293. Start at
      tcp_v4_rcv() and follow the path; expect this to take days, not hours.
```

That is more honest and more useful than padding the list with three mediocre
blog posts, and it teaches the learner something true about where knowledge lives
at Level 4.
