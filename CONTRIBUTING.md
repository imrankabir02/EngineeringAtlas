# Contributing

**Read [docs/architecture.md](docs/architecture.md) first.** Most contribution mistakes here are
architectural rather than editorial: a topic filed as a path, content duplicated instead of
referenced, a prerequisite asserted in prose instead of in the graph. Those are expensive to unpick
later, which is why the architecture is enforced in CI.

Then run the validator before opening a pull request:

```bash
pip install pyyaml
python3 tools/validate_graph.py
```

---

## Ways to contribute, easiest first

| Contribution | Effort | Value |
|---|---|---|
| **Add a node to the graph** | 10 minutes | High — makes a gap visible and gives paths somewhere to point |
| **Fix a technical error** | Varies | Highest — a wrong claim is worse than a missing one |
| **Add a gate challenge** | 30 minutes | High — [gate-library.md](validation/gate-library.md) is the thinnest part of the repository |
| **Improve a `why` on a resource** | 15 minutes | Underrated — turns a link into curation |
| **Specify a project** | Several hours | High — [the ladder](projects/ladder.md) has design briefs waiting |
| **Write a topic** | 10–40 hours | Highest, and the highest bar |
| **Add a path** | 4–10 hours | High if genuinely distinct |

**The most useful small contribution is adding graph nodes.** A topic declared with a level and
prerequisites is immediately useful — it appears in the dependency map, paths can reference it, and the
gap is visible. It requires no prose.

**The second most useful is correcting errors.** A confident wrong claim costs a reader more than a
missing topic does. If you find one, say so plainly in an issue or a pull request; you do not need to
fix it to report it.

---

## Adding a node to the graph

1. Pick a domain file in [`graph/registry/`](graph/registry/). If you cannot decide which,
   **the choice does not matter** — domains are storage, not meaning, and moving a topic later is a
   non-breaking operation.
2. Add an entry:

```yaml
  - id: message-queues-and-streaming
    title: Message queues and streaming
    level: 3
    status: planned
    summary: >
      Decoupling producers from consumers durably: brokers versus logs, ordering guarantees,
      at-least-once delivery and why exactly-once is mostly marketing, dead-letter queues, and
      replay.
    prerequisites:
      hard: [background-jobs-and-queues, distributed-systems-fundamentals]
```

3. `python3 tools/validate_graph.py`

**Choosing an ID.** Permanent — renaming breaks every reference. Name the *concept*, not the product
(`caching`, not `redis`). No level, no domain, no version number in the ID.

**Choosing a level.** From the "you are here when" tests in [`graph/levels.yml`](graph/levels.yml),
not from how hard the topic feels to you. The validator will reject a hard prerequisite at a higher
level than the topic requiring it, and that error usually means either the level or the dependency is
wrong — work out which rather than routing around it.

**Writing the summary.** One to three sentences saying what it is *and why it matters*. This is what a
learner reads when deciding whether the topic is their gap, so it has to discriminate. "Covers the
fundamentals of message queues" does not.

---

## Writing a topic

The highest bar in the repository. Budget 10–40 hours for a real topic.

```bash
cp -r templates/topic topics/backend/message-queues-and-streaming
```

### Order of work

1. **`topic.yml` first.** It is the source of truth, and writing it forces the decisions the prose
   must be consistent with — especially the concept depths and the gates.
2. **Update the registry:** `status: planned` → `published`, add `dir`, and **move** `prerequisites`
   into `topic.yml`, adding a `why` to each.
3. **`fundamentals.md`, `concepts.md`, `practical.md`.**
4. **`exercises.md`, `projects.md`, `interview.md`, `advanced.md`, `resources.md`.**
5. **`README.md` last.** It is a signpost, and far easier to write once you know what it points at.
6. **Delete every `AUTHOR:` comment** from the template.
7. **Run the validator.**

### The quality bar

Eight questions, from [style-guide.md](docs/style-guide.md). A topic must pass all eight.

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

**Evolution is the most commonly failed.** Ask it explicitly: *if every tool named here were replaced
next year, how much of this file would still be true?* If the answer is "not much", the durable
material is missing.

### The fields most often wrong

**`concepts[].depth`** — most concepts should be `working`. Everything marked `deep` means you have not
made a judgment call, and the validator rejects it. **The `aware` markings usually save the reader the
most time**; be generous with them, and name the topic that properly treats each one.

**`gates`** — every gate is an *action with an observable outcome*. "Understand caching" is not a gate;
"send 500 concurrent requests for the same cold key and measure how many reach the origin" is. If you
cannot tell whether someone passed, rewrite it.

**`prerequisites[].why`** — writing this usually reveals a prerequisite you did not need or one you
missed. It is the field that keeps the graph honest.

**`first_principles_chain`** — each step must be a *problem* the next step answers. If it reads as a
list of subtopics, it is a table of contents rather than a derivation. Compare
[caching's](topics/backend/caching/topic.yml).

**`resources[].why`** — answers *why this instead of the alternatives*, not what it is. Worked examples:
[templates/resource-list.md](templates/resource-list.md).

**`effort`** — a range with stated assumptions. A single number implies precision that does not exist.

### Files may be short. Files may not be placeholders.

The validator rejects any of the nine files under 400 characters or containing `TODO`, `TBD`, `WIP`, or
similar.

If a topic genuinely has nothing to say under a heading — some Level 0 topics have no meaningful
`advanced.md` — say that in a sentence, explain why, and point to where the depth lives. See
[computer-basics/advanced.md](topics/foundations/computer-basics/advanced.md) for an example of doing
this honestly. One honest sentence is content; `TODO` is not.

---

## Specifying a project

```bash
cp -r templates/project projects/distributed-task-queue
```

The bar:

| Test | Question |
|---|---|
| **Competency** | Does `validates` state capabilities, not features? |
| **Constraint** | Is there at least one constraint that prevents shortcutting the lesson? |
| **Failure** | Does `break_it` contain failures the learner must cause deliberately? |
| **Finishable** | Can a learner at that level finish the core stages in one to three weeks part-time? |
| **Not a tutorial** | Does it specify *what* and *why*, leaving *how* to the learner? |

**"Not a tutorial" is the most commonly failed.** A project specification is a requirements document.
If a reader could follow it to a working system without making a decision, it is a walkthrough and the
learner will get typing practice instead of judgment.

`validates` is the field that justifies the project's existence. "Builds a REST API" is not a
competency statement. "Can design an idempotent write endpoint and demonstrate that a duplicated
request causes no double charge" is.

[The ladder](projects/ladder.md) has design briefs for planned projects — each already states what it
validates and why it exists, so promoting one is a matter of writing the specification rather than
inventing the project.

---

## Adding a path

```bash
cp templates/path/path.yml paths/frontend-engineer.yml
cp templates/path/path.md  paths/frontend-engineer.md
```

The bar:

| Test | Question |
|---|---|
| **Audience** | A specific person with a specific goal, stated as a capability? |
| **Distinct** | Does it differ from an existing path by more than a few steps? |
| **Ordered** | Does the validator pass? |
| **Milestones** | At least one, stated as a capability with evidence |
| **Emphasis** | Do the steps say what matters *here*, or is it a bare topic list? |
| **Honest about scale** | Realistic effort, in ranges, with assumptions? |

**The most common rejected proposal is a path that duplicates an existing one with a different name.**
Two paths differing in three steps should be one path with an emphasis note.

**A path with no `emphasis` notes adds nothing over the graph** and will be rejected. The emphasis is
where all stack-specific and role-specific guidance lives — see
[python-backend.yml](paths/stacks/python-backend.yml) for the reference implementation.

The validator enforces step ordering: every step's hard prerequisites must appear earlier in the path,
in a `prerequisite_paths` path, or below the path's `entry_level`. That check is the mechanical version
of "no framework before fundamentals". If it fails, add the missing topic earlier rather than lowering
`entry_level`.

---

## Style

Full conventions: [docs/style-guide.md](docs/style-guide.md). The ones that matter most:

- **Wrap prose at 80 characters.** Diffs become reviewable line by line rather than as whole-paragraph
  replacements. Do not wrap tables, code, or long URLs.
- **Sentence case headings.**
- **Relative links only.** Checked in CI.
- **Three passes for a hard concept:** the problem in plain words, then the mechanism with correct
  terminology, then the edge cases and costs. This is what lets one file serve a beginner and an
  experienced engineer.
- **No** motivational filler, hype, timeline promises, SEO padding, rhetorical-question headings, or
  decorative emoji.
- **Delete "simply", "just", and "obviously".** To a reader who does not already know, they mean "you
  should have".

### Numbers and claims

Any claim about performance, scale, or behaviour that a reader might act on needs a number, a
mechanism, or a pointer to a primary source. If you have none of the three, say it is your experience
rather than stating it as fact.

Mark version-specific claims:

> *Verified against Redis 7.2 (2026-08).* The default `maxmemory-policy` is `noeviction`.

And keep them out of `fundamentals.md` and `concepts.md` entirely — those files must stay correct if
every tool they name is replaced. See [version-awareness.md](docs/version-awareness.md).

---

## Pull requests

Use the [template](.github/PULL_REQUEST_TEMPLATE.md). Before opening:

- [ ] `python3 tools/validate_graph.py` passes
- [ ] Prose wrapped at 80 characters
- [ ] All `AUTHOR:` template comments deleted
- [ ] Every resource has a `why` that explains the *selection*
- [ ] Every gate is an action with an observable outcome
- [ ] Version-specific claims are marked and confined to `practical.md`
- [ ] `last_reviewed` updated on any `topic.yml` you touched

**One topic per pull request.** A pull request adding three topics cannot be reviewed properly, and
topic review is where the quality bar is actually applied.

### Review

Reviews are about the eight quality questions, not about tone. Expect substantive comments on depth
markings, gate wording, and whether prerequisites are minimal — those are the parts that determine
whether the topic works, and they are usually the parts that need a second pass.

If you disagree with a review comment, say so with your reasoning. Being right matters more than
being agreeable, and the reviewer may be wrong.

---

## Licensing

By contributing you agree that your contribution is licensed under the [MIT License](LICENSE), the
same as the rest of the repository. This covers prose as well as code, deliberately, so that reuse of
the curriculum has no ambiguity.

Do not contribute text you do not have the right to license. Quoting a short passage with attribution
is fine; pasting a chapter is not. Summarising a resource in your own words is what the `why` field is
for.

---

## Non-goals

Stated so they are not repeatedly re-proposed. Full list:
[architecture.md §11](docs/architecture.md#11-deliberate-non-goals).

- No web application. The repository must stay fully usable in the GitHub UI and a text editor.
- No progress database. The project stores no user state.
- No exhaustive link collections. Curation is the value.
- No video-first content. Text is diffable, reviewable, searchable, and translatable.
- No per-language duplication of shared concepts. Languages are paths, not topics.
- No completion certificates or gamified scoring.
