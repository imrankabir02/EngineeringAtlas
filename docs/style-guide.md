# Style Guide

Consistency is a navigation feature. A learner who has read one topic should know
exactly where to look in every other topic.

---

## Voice

**Direct.** Say the thing. No preamble, no "in this section we will explore".

**Second person for instruction, third for explanation.**
"You will need a running Postgres instance." / "Postgres acquires a row-level
lock."

**Concrete over abstract.** Numbers, mechanisms, and named failure modes beat
adjectives. "Fast" is not information; "roughly 100 ns from L1, 100 µs from a
local NVMe read, 500 µs–2 ms for a network round trip inside a datacentre" is.

**Honest about difficulty.** If something is hard, say so, and say why. Learners
who are told a hard thing is easy conclude they are the problem and stop.

**No hedging as a substitute for knowing.** "It depends" is only acceptable when
followed by *what it depends on*.

### Do not write

- Motivational filler: "you've got this", "let's dive in", "exciting"
- Hype: "blazing fast", "game-changing", "revolutionary", "industry-standard"
- Timeline claims: "learn X in 7 days", "master Y in a weekend"
- Empty transitions: "Now that we've covered X, let's move on to Y."
- SEO padding: keyword repetition, "In this article we will discuss..."
- Rhetorical questions used as headings
- Emoji in content (a single one is acceptable in a navigation table if it
  carries information; decorative emoji are not)
- Condescension. "Simply", "just", and "obviously" mean "you should already know
  this" to a reader who does not. Delete them.

---

## Explaining a hard concept

Simple language first, then depth. Not simplified *content* — simplified
*language*, then the precision added back.

Three passes:

1. **What problem does this solve?** Plain words, no jargon, one paragraph.
2. **How does it work?** Introduce the mechanism and the correct terminology,
   defining each term at first use.
3. **What are the edge cases and costs?** Where the simple model is wrong, and
   why the simplification was still worth making.

Worked example:

> **Pass 1.** A database index is a second, sorted copy of one column, kept
> alongside the table, so the database can find rows without reading all of them.
>
> **Pass 2.** Concretely, most relational indexes are B+ trees: a balanced tree
> whose interior nodes hold key ranges and whose leaves hold keys with pointers
> to rows. Depth stays low — three or four levels for millions of rows — so a
> lookup costs a handful of page reads instead of a full scan.
>
> **Pass 3.** The costs: every write must also update every index, so an
> over-indexed table has slow inserts. The index consumes storage and memory. The
> planner may ignore it if it estimates that too many rows match, because at that
> point a sequential scan is genuinely faster — random I/O per row is more
> expensive than streaming pages. And "sorted copy" was a simplification: for a
> composite index the sort order is lexicographic across columns, which is why
> `(a, b)` can serve a query filtering on `a` but not one filtering only on `b`.

Pass 3 is what makes the content useful to an experienced engineer while pass 1
keeps it accessible to a beginner. Both audiences are served by the same file
because the depth increases monotonically.

---

## Markdown conventions

- **One `#` per file**, matching the topic or document title.
- **Sentence case headings.** "Cache invalidation", not "Cache Invalidation".
- **Wrap prose at 80 characters.** Diffs become reviewable line by line rather
  than as whole-paragraph replacements. Do not wrap tables, code, or long URLs.
- **Fenced code blocks with a language tag.** Use `text` for output, `console`
  for shell sessions with prompts, `bash` for scripts.
- **Tables for comparisons.** Prose comparisons of more than two options are
  hard to scan and hard to keep symmetric.
- **Relative links** between files, always. `../../databases/sql/README.md`, never
  a `github.com` URL. CI checks that they resolve.
- **ASCII diagrams for chains and flows** (they render everywhere and diff
  cleanly); Mermaid for graphs with more than about six nodes — but see below.
- **Do not hand-write a Mermaid block for a dependency graph.** GitHub renders Mermaid on the web
  and *not* in its mobile apps, where the fence degrades to raw source. Graphs derived from the
  learning graph are generated as light/dark SVGs plus a text table by
  `tools/generate_diagrams.py`; add a view to [`graph/diagrams.yml`](../graph/diagrams.yml) instead
  of drawing one. Mermaid remains fine for a small illustrative diagram that is not derived from
  the graph.
- **Anything conveyed only by a picture must also exist as text.** A diagram is an overview; a
  table, list, or ASCII chain is what works under ctrl-F, in a screen reader, and on a phone.
  Always give an `alt` attribute that says what the image shows.
- **No HTML** except `<details>` for genuinely optional long content.
- **No badges** except build status and licence on the root README. Badge walls
  are visual noise that pushes the actual content below the fold.
- **Blockquotes** for definitions and version-dated claims, not for emphasis.
- **Bold** for the load-bearing sentence in a long section. *Italic* for terms at
  first use. Never all-caps for emphasis.

---

## Structure conventions

Every topic file starts with a one-line statement of what the file covers, then a
navigation line back to the topic README:

```markdown
# Cache invalidation

When a cached copy is wrong, how you find out, and what it costs to prevent.

[← Caching](README.md) · [Concepts](concepts.md) · [Practical](practical.md)
```

Lists of things a learner must *do* are numbered. Lists of things a learner must
*know* are bulleted.

Every claim about performance, scale, or behaviour that a reader might act on
should carry either a number, a mechanism, or a pointer to a primary source. If
none of the three is available, say that it is your experience rather than
stating it as fact.

---

## Naming

- **Topic and project IDs:** lowercase-hyphenated, name the concept not the
  product. `caching` not `redis`; `containers-and-docker` is acceptable because
  Docker is load-bearing history.
- **Titles:** sentence case, expand acronyms on first use in prose. "REST APIs",
  "Transactions and isolation", "CI/CD" (universally known, no expansion needed).
- **File names:** the nine standard topic files have fixed names. Do not add
  files to a topic directory without changing
  [architecture.md](architecture.md#9-standard-topic-directory) in the same pull
  request.

---

## Length

There is no minimum. There is a quality floor.

A three-paragraph `advanced.md` that honestly says "this topic has no meaningful
advanced dimension in isolation; the depth lives in `distributed-systems` and
`operating-systems`, here is what to read" is **good content**. A 2,000-word
`advanced.md` assembled from restated basics is not.

Guidance, not rules:

| File | Typical |
|---|---|
| `README.md` | 200–500 words. It is a signpost. |
| `fundamentals.md` | 800–2,500 words. The first-principles chain, fully worked. |
| `concepts.md` | Mostly a table. Depth marking per concept is the payload. |
| `practical.md` | 1,000–3,000 words. Usually the longest file. |
| `exercises.md` | 8–20 exercises, each 1–5 sentences. |
| `projects.md` | 200–600 words. Points to `projects/`, does not restate specs. |
| `interview.md` | 400–1,200 words. Discussion shapes, not question banks. |
| `advanced.md` | Highly variable. May legitimately be short. |
| `resources.md` | 5–15 resources total. Fewer, better. |

If a file exceeds these substantially, the topic is probably two topics.

---

## Reviewing content

The quality bar, as eight questions. A pull request adding a topic must pass all
eight:

| Test | Question |
|---|---|
| **Completeness** | Are the essential concepts present, and is anything important silently omitted? |
| **Dependency** | Are prerequisites correct, minimal, and correctly ordered? |
| **Depth** | Does it go past what a good tutorial would cover? |
| **Practicality** | Does the learner build something real? |
| **Understanding** | Does it explain *why* the technology works, not only how to use it? |
| **Validation** | Can the learner prove competency, with declared gates? |
| **Production** | Does it eventually address real-world operation, not just the happy path? |
| **Evolution** | Will it still be correct after the current tooling generation is replaced? |

The last one is the most commonly failed. Ask it explicitly: *if every tool named
here were replaced next year, how much of this file would still be true?* If the
answer is "not much", the durable material is missing and needs to be written.
