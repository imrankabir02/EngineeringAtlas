# Technical Learning Guru Map

[![validate](https://github.com/imrankabir02/EngineeringAtlas/actions/workflows/validate.yml/badge.svg)](https://github.com/imrankabir02/EngineeringAtlas/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**A map of technical knowledge and engineering competency — not a list of technologies to learn.**

This repository answers six questions that reading lists do not:

| Question | Where |
|---|---|
| I know X. What should I learn next? | [The dependency map](graph/dependency-map.md) |
| Why should I learn it? | Every topic's `why_it_matters` — what breaks without it |
| What prerequisite am I missing? | [The dependency map](graph/dependency-map.md) — and it is checked in CI |
| How deeply should I learn it? | Every topic's `concepts.md` — a required depth per concept |
| What should I build? | [The project ladder](projects/ladder.md) |
| How do I know I am ready? | [Competency gates](docs/competency-gates.md) — evidence, not checkboxes |

The last two are the point. **Competency, not course completion.**

---

## Start here

Fifteen minutes of setup saves months of directionless study. Do it properly.

### 1 · Read the philosophy

[**docs/philosophy.md**](docs/philosophy.md) — 10 minutes. Do not skip it. If you skip it you will
use this repository as a link collection and get link-collection results.

It covers the ten questions every topic answers, the difference between
**knowledge → skill → judgment → mastery**, and the anti-patterns this project is built to oppose.

### 2 · Choose your goal

A goal is a capability, not a job title and not a technology.

| Weak goal | Usable goal |
|---|---|
| "Learn backend" | "Build and operate an API that survives its dependencies failing" |
| "Learn Kubernetes" | "Deploy and debug a multi-service app on a cluster I did not set up" |
| "Learn AI" | "Train, evaluate and deploy a model, and know when the answer is not ML" |

### 3 · Find your current level

Six levels, defined by **what you can do unaided** — not by exposure.
[**docs/levels.md**](docs/levels.md)

| Level | Name | The test |
|---|---|---|
| 0 | Absolute Beginner | Can operate a computer deliberately rather than by memorised clicks |
| 1 | Foundation | Can write a 300-line program solving a problem nobody gave you a template for |
| 2 | Intermediate | Can build, test and deploy a correct multi-component application |
| 3 | Advanced | Can build a system that survives real traffic, real failures and real data |
| 4 | Expert | Can be accountable for a system: its scale, cost, reliability and incidents |
| 5 | Guru | Can work correctly where no guidance exists, and raise others' capability |

**Do not self-assess by reading these and picking one.** Take the "you are here when" test for each
level in [levels.md](docs/levels.md). Everyone overestimates this in the same direction.

Compute your level **per domain**. Being Level 3 in backend and Level 0 in embedded is normal and
permanent.

### 4 · Pick a path

| Path | Entry → Exit | For |
|---|---|---|
| [Absolute beginner](paths/absolute-beginner.md) | L0 → L1 | Never studied technology |
| [Programming foundations](paths/programming-foundations.md) | L1 → L2 | The foundation everything else assumes |
| [Computer science foundations](paths/computer-science-foundations.md) | L2 → L4 | Theory that predicts behaviour |
| [**Software engineering, beginner to advanced**](paths/software-engineering-core.md) | L0 → L4 | **The spine.** Nothing assumed, ends at production accountability |
| [Python backend engineer](paths/stacks/python-backend.md) | L1 → L4 | The reference stack path |

Pick **one**. Two at once is [technology hopping](docs/philosophy.md#technology-hopping) with extra
structure. Twelve more paths are planned — see [paths/README.md](paths/README.md).

### 5 · Then: learn → practise → build → validate → advance

The loop, in detail: [**docs/how-to-use.md**](docs/how-to-use.md).

```text
Learn ──► Practise ──► Build ──► Break ──► Debug ──► Explain ──► Benchmark ──► Review ──► Advance
   ▲                                                                                        │
   └──────────────────────── failed a gate? go back to the stage that fixes it ─────────────┘
```

**Break and Benchmark are the stages everyone skips, and they are where judgment comes from.** You
do not understand a system until you have made it fail on purpose. You do not know whether something
is fast until you measured it.

---

## Written topics

Most of the map is declared and not yet written — see
[why that is deliberate](docs/architecture.md#4-the-registry-and-the-no-empty-files-rule). These four
are complete, and they demonstrate the standard at four different levels:

| Level | Topic | Shows |
|---|---|---|
| 0 | [How computers work](topics/foundations/computer-basics/README.md) | Measuring instead of assuming; an honestly short `advanced.md` |
| 1 | [Programming fundamentals](topics/programming/programming-fundamentals/README.md) | Depth markings doing real work: 6 deep, 6 working, 3 capped at aware |
| 2 | [Data structures](topics/computer-science/data-structures/README.md) | Where theory and measurement openly disagree |
| 3 | [Caching](topics/backend/caching/README.md) | The full first-principles chain, and failure as curriculum |

Each has nine files in the same order, always: `README`, `fundamentals`, `concepts`, `practical`,
`exercises`, `projects`, `interview`, `advanced`, `resources`. A learner who has read one topic knows
where to find things in every other.

---

## Projects

Six specified, from Level 0 to Level 3. The full ladder to Level 5:
[projects/ladder.md](projects/ladder.md).

| Level | Project | Core lesson |
|---|---|---|
| 0 | [Anatomy of your own machine](projects/machine-anatomy/README.md) | Measure instead of assuming |
| 1 | [Expression calculator](projects/cli-calculator/README.md) | Decomposition and recursion, with no `eval` |
| 1 | [File organiser](projects/file-organizer/README.md) | A hostile world; reversibility |
| 2 | [Data structures from scratch](projects/ds-from-scratch/README.md) | Invariants, and measurement versus asymptotics |
| 3 | [In-memory cache](projects/in-memory-cache/README.md) | Eviction, a demonstrated race, a stampede you caused |
| 3 | [URL shortener](projects/url-shortener/README.md) | A read-heavy system, to its saturation point |

Every project states **what competency it validates**, the **constraint** that stops it becoming
assembly work, and **how you will break it**.

---

## What makes this different

**The graph is data, and it is enforced.** 129 topics, their levels, and their prerequisites live in
[`graph/registry/`](graph/registry/). CI checks that the prerequisite graph is acyclic, that no
prerequisite is at a higher level than the topic requiring it, that every reference resolves, and
that every path's step ordering is satisfiable. Prose prerequisites drift; a validated graph does
not.

**Every topic says how deeply to learn each concept.** `aware`, `working`, or `deep`, per concept.
Telling you what to skim is as valuable as telling you what to master, and it is the question most
curricula never answer.

**Problems before solutions, always.** Not "learn Redis" but: *why is this slow → memory is a
thousand times closer → some data is read more than it changes → keep a copy closer → now two copies
can disagree → what do you evict → what happens when everyone misses at once → Redis is one answer to
these.* A learner who follows that can evaluate a cache they have never seen.

**Technologies must answer "when NOT to use this."** Anything that cannot is being sold rather than
explained. [docs/technology-selection.md](docs/technology-selection.md).

**Fewer, better resources.** Tiered, each with a stated reason for existing. A topic with fifty links
transfers the hardest problem — deciding what to read — back to someone not equipped to solve it.

**No empty files.** Unwritten topics are declared in the graph with `status: planned` and **no
directory**. The map is complete; the gaps are visible.

**Nothing is stored about you.** No accounts, no progress database. Track your own in a fork:
[templates/progress.yml](templates/progress.yml).

---

## Repository layout

```text
docs/         How the system works: philosophy, levels, gates, schema, style
graph/        The map: domains, levels, and the 129-node registry
topics/       Written topics. Nine files each, always the same names
paths/        Curated orderings. Reference topics; own no content
projects/     Project specifications, and the full ladder
validation/   Evidence standards and the gate library
templates/    Copy-paste starting points, kept in sync with the schema
tools/        The graph validator that runs in CI
```

Why it is shaped this way, and the alternatives rejected:
[**docs/architecture.md**](docs/architecture.md).

---

## Documentation

| Read | For |
|---|---|
| [philosophy.md](docs/philosophy.md) | The learning model, and the anti-patterns |
| [levels.md](docs/levels.md) | L0–L5, the four competency axes, and the level tests |
| [how-to-use.md](docs/how-to-use.md) | The Start Here → Advance loop, in detail |
| [competency-gates.md](docs/competency-gates.md) | How competency is proven |
| [architecture.md](docs/architecture.md) | Information architecture and its rationale |
| [graph-schema.md](docs/graph-schema.md) | Normative schema for the YAML |
| [technology-selection.md](docs/technology-selection.md) | The eight-question rubric, with Redis worked |
| [resource-tiers.md](docs/resource-tiers.md) | How resources are chosen |
| [version-awareness.md](docs/version-awareness.md) | Separating concept from implementation from version |
| [progress-tracking.md](docs/progress-tracking.md) | Seven states, and the evidence each requires |
| [style-guide.md](docs/style-guide.md) | Writing conventions and the eight-question quality bar |

---

## Status and contributing

**Phase 1 complete.** The architecture, the validated graph, four written topics across four levels,
six projects, five paths, and the full template set. [ROADMAP.md](ROADMAP.md) has what comes next and
what is deliberately not done yet.

Contributions welcome, and the highest-value ones are smaller than you might expect:

- **Add a node to the graph** — declare a topic that should exist, with its level and prerequisites.
  Ten minutes, and it makes a gap visible.
- **Write a topic** — the nine-file structure, from [templates/topic/](templates/topic/). The bar is
  in [CONTRIBUTING.md](CONTRIBUTING.md).
- **Add a design or debugging challenge** to [the gate library](validation/gate-library.md).
- **Specify a project** from [the ladder](projects/ladder.md).
- **Fix something wrong.** Technical errors matter more than typos, and a topic that overstates its
  own certainty is a real bug.

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/architecture.md](docs/architecture.md) first — most
contribution mistakes here are architectural rather than editorial. Run
`python3 tools/validate_graph.py` before opening a pull request.

[Code of Conduct](CODE_OF_CONDUCT.md) · [Changelog](CHANGELOG.md) · [License](LICENSE) (MIT)

---

## What this repository will not do

- **Promise timelines.** "Learn X in 30 days" is a lie or a redefinition of "learn". Estimates here
  are focused hours in ranges, with assumptions stated.
- **Rank technologies by popularity.** Popularity is evidence about hiring markets, not about fitness
  for your problem.
- **Motivate you.** No fluff, no gamification, no certificates. The artifacts you build are the
  credential.
- **Pretend the order is arbitrary.** Prerequisites are real. You may skip them — and the repository
  will tell you what you are skipping and what it will cost.
- **Confuse a checked box with mastery.** Every state beyond "learning" requires evidence that exists
  outside this repository.
