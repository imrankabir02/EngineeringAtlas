# Topics

Written topics. One directory per topic, addressed by its stable ID.

**Most of the map is not here.** 129 topics are declared in
[`graph/registry/`](../graph/registry/); four are written. Unwritten topics have `status: planned` and
**no directory** — the map is complete, the gaps are visible, and the repository contains zero
placeholder files. See
[architecture.md §4](../docs/architecture.md#4-the-registry-and-the-no-empty-files-rule).

---

## Written

| Level | Topic | Domain | What it demonstrates |
|---|---|---|---|
| 0 | [How computers work](foundations/computer-basics/README.md) | foundations | Measuring instead of assuming; an honestly short `advanced.md` |
| 1 | [Programming fundamentals](programming/programming-fundamentals/README.md) | programming | Depth markings doing real work: 6 deep, 6 working, 3 capped at aware |
| 2 | [Data structures](computer-science/data-structures/README.md) | computer-science | Where theory and measurement openly disagree |
| 3 | [Caching](backend/caching/README.md) | backend | The full first-principles chain; failure as curriculum |

Four topics at four levels, deliberately. Between them they show what the standard looks like at each
level, including the ways a Level 0 topic legitimately differs from a Level 3 one.

---

## Layout

```text
topics/<domain>/<topic-id>/
├── topic.yml         machine-readable definition — the source of truth
├── README.md         orientation, prerequisites, how deep to go, reading order
├── fundamentals.md   the concept from first principles — the problem before the solution
├── concepts.md       the inventory, with a required depth per concept
├── practical.md      doing it for real: tools, selection rubric, failure modes, operation
├── exercises.md      small, graded, verifiable drills
├── projects.md       which projects validate this topic, and why those ones
├── interview.md      what competent discussion sounds like; shallow-answer tells
├── advanced.md       where the topic goes at L4-L5; where the depth lives
└── resources.md      tiered resources, each with a stated reason for existing
```

**Nine files, always the same names, always in that order.** This is not bureaucracy — it is why
navigation survives a thousand topics. A learner who has read one topic knows exactly where to find
things in every other, and that predictability is worth more than the flexibility it costs.

The names are fixed. Adding a file to a topic directory requires changing
[architecture.md §9](../docs/architecture.md#9-standard-topic-directory) in the same pull request, and
the validator rejects unexpected files.

---

## Files may be short. Files may not be placeholders.

The validator rejects any of the nine under 400 characters or containing `TODO`, `TBD`, `WIP`, or
similar.

Some topics genuinely have little to say under some headings. A Level 0 orientation topic has no
advanced dimension of its own — so
[computer-basics/advanced.md](foundations/computer-basics/advanced.md) says that in a sentence,
explains why padding it would be a disservice, and spends the file mapping where the depth actually
lives.

That is real content, and it is more useful than two thousand words assembled from restated basics.
**One honest sentence is content; `TODO` is not.**

---

## Domains are shelves, not meaning

`topics/backend/`, `topics/databases/`, `topics/systems/` exist so that a human browsing the tree is
not looking at a thousand sibling directories. That is their only job.

Consequences worth knowing:

- **A topic's domain is not its definition.** `caching` is legitimately part of backend, databases,
  distributed systems, performance engineering, and system design. It lives in one place and is
  referenced by ID from everywhere.
- **Do not nest.** One level only: `topics/<domain>/<topic-id>/`. Depth is where navigation dies.
- **Moving a topic between domains is cheap and non-breaking**, because nothing references it by path.
- **If you cannot decide which domain, the choice does not matter.** Pick one and move on. The
  architecture removed the stakes from an unanswerable question, which is a feature.

---

## Reading a topic

Suggested order, and it is repeated in every topic's README:

1. `README.md` — is this your gap? What are the prerequisites? How deep should you go?
2. `fundamentals.md` — the derivation. The most important file in most topics.
3. `concepts.md` — use this to **budget your attention**. Each concept is marked `aware`, `working`,
   or `deep`, and the markings are the answer to "how deeply should I learn this?"
4. `practical.md` — tools, commands, the selection rubric, and how it fails in production.
5. `exercises.md` — before the project, so the project's difficulty is design rather than syntax.
6. `projects.md` → build it.
7. `topic.yml` → work the gates. This is the step people skip and the one that produces judgment.

**Trust the depth markings.** Going deep on an `aware` concept is the most common way to spend a month
on a topic and finish no better prepared. The `aware` markings name the topic and level where each
subject is properly treated — that pointer is the useful part.

---

## Adding a topic

```bash
cp -r templates/topic topics/<domain>/<topic-id>
```

Then follow [CONTRIBUTING.md](../CONTRIBUTING.md#writing-a-topic). In summary: fill in `topic.yml`
first, update the registry entry (`planned` → `published`, add `dir`, **move** `prerequisites` into
`topic.yml` with a `why` on each), write the prose, delete the template's `AUTHOR:` comments, and run
`python3 tools/validate_graph.py`.

The bar is the eight quality questions in [style-guide.md](../docs/style-guide.md). The one most
commonly failed is **Evolution**: if every tool named in your `fundamentals.md` were replaced next
year, how much would still be true? If the answer is "not much", the durable material is missing.
