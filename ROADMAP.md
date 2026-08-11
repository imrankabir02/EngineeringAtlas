# Roadmap

The plan is deliberately **architecture first, breadth last**. A repository of this scope fails by
accumulating inconsistent content faster than it can be navigated, so every phase below adds
structure or depth before it adds volume.

Nothing here is dated. Phases complete when their exit criteria are met.

---

## Phase 1 — Architecture and exemplars · **complete**

Establish a structure that can hold a thousand topics, and prove it with a small number of fully
developed ones.

| Delivered | |
|---|---|
| Information architecture, with rejected alternatives documented | [docs/architecture.md](docs/architecture.md) |
| Learning philosophy, the ten questions, the anti-patterns | [docs/philosophy.md](docs/philosophy.md) |
| Six-level competency model and the four axes | [docs/levels.md](docs/levels.md) |
| Competency gates, progress states, evidence standards | [docs/competency-gates.md](docs/competency-gates.md), [docs/progress-tracking.md](docs/progress-tracking.md) |
| Machine-readable schema, normative | [docs/graph-schema.md](docs/graph-schema.md) |
| Technology-selection rubric, Redis worked in full | [docs/technology-selection.md](docs/technology-selection.md) |
| Resource tiers, version awareness, style guide | [docs/](docs/) |
| **129-node learning graph**, validated: acyclic, level-monotone, all references resolve | [graph/](graph/) |
| Rendered dependency map with first-principles chains | [graph/dependency-map.md](graph/dependency-map.md) |
| **Four written topics** at Levels 0, 1, 2, 3 — nine files each | [topics/](topics/) |
| **Six specified projects**, Levels 0–3 | [projects/](projects/) |
| **Five paths**, including the beginner→advanced spine and the reference stack path | [paths/](paths/) |
| Full template set, kept in sync with the schema | [templates/](templates/) |
| Graph validator running in CI | [tools/validate_graph.py](tools/validate_graph.py) |
| Contribution guide, issue and PR templates, code of conduct | — |

**Exit criteria, all met:** the validator passes; a contributor can add a topic from the template
without reading anything else; the four written topics demonstrate the standard at four different
levels; the graph is complete enough to answer "what am I missing?" for the software-engineering
spine.

---

## Phase 2 — Depth on the spine

**Goal: make the [software-engineering-core](paths/software-engineering-core.md) path fully walkable
through Level 2.** A learner should be able to go from zero to Level 2 without leaving the repository
for structure — only for resources.

Roughly 25 topics, in dependency order:

**Level 0 (6)** — `operating-system-basics`, `files-and-directories`, `command-line-basics`,
`internet-basics`, `what-programming-is`, `problem-solving-basics`.

Cheap and high-value: they are short, they have no prerequisites, and they are the entry point for
every beginner.

**Level 1 (6)** — `debugging-fundamentals`, `error-handling`, `version-control-git`,
`linux-fundamentals`, `networking-fundamentals`, `databases-introduction`.

`debugging-fundamentals` is the highest-priority single topic in this phase. It is the skill that most
determines a learner's pace for two levels, and it is almost never taught deliberately.

**Level 2 (13)** — `object-oriented-programming`, `functional-programming`, `complexity-analysis`,
`algorithms`, `sql`, `relational-modeling`, `http`, `rest-apis`,
`authentication-and-authorization`, `testing-fundamentals`, `clean-code`, `code-review`,
`software-design-principles`.

`http` and `sql` are the two that unlock the most downstream topics.

**Also in this phase:**

- Projects for Levels 1–2 from [the ladder](projects/ladder.md): REST API with a database,
  authentication system, blog platform, test suite for someone else's code.
- The **frontend** path, because it is the most requested and the most structurally different from
  the backend spine.
- Expand [gate-library.md](validation/gate-library.md) — it is currently the thinnest part of the
  repository relative to its importance.

**Exit criteria:** a learner can complete Levels 0–2 of the spine using only this repository for
structure; every Level 0 and Level 1 topic in the graph is written; the ladder has specified projects
at every level from 0 to 2.

---

## Phase 3 — Depth at Level 3

**Goal: the level where most professional engineers work.** This is where the repository becomes
useful to people who already have jobs, and it is where the content is hardest to write well, because
it requires production experience rather than reading.

Roughly 20 topics: `operating-systems-fundamentals`, `concurrency-and-parallelism`,
`async-programming`, `memory-management`, `processes-and-scheduling`, `tcp-ip-internals`,
`transactions-and-isolation`, `indexing-and-query-optimization`, `nosql-data-models`,
`containers-and-docker`, `ci-cd`, `observability`, `cloud-fundamentals`,
`distributed-systems-fundamentals`, `message-queues-and-streaming`, `application-security`,
`api-design`, `software-architecture`, `system-design-fundamentals`, `performance-engineering`.

**Also:** the Level 3–4 projects — distributed task queue, real-time chat, search engine, monitoring
system — and the DevOps and full-stack paths.

**Exit criteria:** the spine is walkable through Level 3; `distributed-systems-fundamentals` and
`operating-systems-fundamentals` are written to the standard of [caching](topics/backend/caching/),
since everything above them depends on their quality.

---

## Phase 4 — Breadth

**Only after the spine is deep.** Adding domains before the core is solid produces a repository that
is wide and useless, which is the failure mode this ordering exists to avoid.

- **Stack paths:** PHP/Laravel, JavaScript/TypeScript, Go, Java, Rust. Cheap once the shared topics
  exist — a stack path is mostly emphasis notes, which is
  [the point](docs/architecture.md#5-languages-and-stacks-are-paths-not-topics).
- **Domains:** data engineering, AI/ML, cybersecurity, mobile, embedded, game development.
- **Role paths:** cloud, data, ML, security, architect, research engineer.
- **Level 4 topics:** the distributed-systems and reliability material.

**Exit criteria:** at least three stack paths complete; at least two non-backend domains walkable to
Level 3.

---

## Phase 5 — Level 4–5 and maintenance as a practice

**Level 4–5 content is different in kind**, and the roadmap should say so rather than treating it as
more topics.

Level 5 competencies — designing abstractions, deciding under uncertainty, mentoring, research — cannot
be conveyed by exposition. What the repository can provide is **structured practice**: design
challenges with traps, failure simulations with prediction scoring, paper-reading exercises, and
review exercises against real pull requests. That means Phase 5 is mostly
[gate-library.md](validation/gate-library.md) growing, not `topics/` growing.

**Also in this phase, and ongoing from now:**

- **Rot review.** A scheduled job surfacing topics whose `last_reviewed` exceeds their
  `version_sensitivity` cadence (6 months for `high`, annually for `medium`, 2 years for `low`), plus
  external link checking. See [version-awareness.md](docs/version-awareness.md).
- ~~**Graph rendering.** Generated diagrams from the YAML, so `dependency-map.md` stops being
  hand-maintained.~~ **Done, brought forward from this phase.** `tools/generate_diagrams.py`
  derives every diagram and its accompanying prerequisite table from the registry;
  `tools/render_diagrams.sh` renders light and dark SVGs; CI verifies freshness without needing
  a browser. This removes the last hand-maintained duplication in the repository.
- **Translation.** Only once the English content is stable — translating a moving target wastes
  contributors' effort.

---

## Standing priorities, at every phase

**Correctness over volume.** A wrong claim costs a reader more than a missing topic. Fixing an error
outranks writing anything new.

**Depth markings before prose.** A topic that does not say how deeply to learn each concept has not
answered the question that most distinguishes this project.

**Every technology answers "when NOT to use this."** Enforced in review.

**Gates must be actions with observable outcomes.** "Understand X" fails review.

**No empty files, ever.** A `planned` node with no directory is honest; a stub is not.

---

## Deliberately not planned

Stated so they are not repeatedly proposed. Full reasoning:
[architecture.md §11](docs/architecture.md#11-deliberate-non-goals).

| Not doing | Why |
|---|---|
| A web application | The repository must stay fully usable in the GitHub UI and a text editor. Tooling may add views; it may never become the only way to read |
| A progress database or accounts | The project stores no user state. Progress lives in your fork |
| Video content | Text is diffable, reviewable, searchable, translatable. Videos may be resources, never curriculum |
| Certificates or gamified scoring | The artifacts you build are the credential |
| Exhaustive link collections | Curation is the value. Prefer fewer excellent resources |
| A topic per language for shared concepts | "Python OOP" and "PHP OOP" are 85% the same idea. Languages are paths |
| An interview question bank | It trains recall, which is the failure mode this project opposes. `interview.md` covers discussion shapes instead |
| Ranking technologies by popularity | Popularity is evidence about hiring markets, not fitness for a problem |

---

## How to help

The bottleneck is **written topics at Levels 1–3**, and the highest-value contributions right now are
smaller than that:

1. **Add graph nodes.** Ten minutes each, and they make gaps visible.
2. **Report errors.** You do not need to fix them.
3. **Add gate challenges.** [gate-library.md](validation/gate-library.md) is thin.
4. **Write a Level 0 or Level 1 topic.** Short, no prerequisites, high leverage for beginners.
5. **Improve resource `why` fields.** Turns a link into curation.

[CONTRIBUTING.md](CONTRIBUTING.md) has the bar for each.
