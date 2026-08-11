# Information Architecture

This document explains how the repository is structured and, more importantly,
**why**. Read it before adding anything. Most contribution mistakes are
architectural, not editorial.

The design goal is stated once, plainly:

> The repository must be able to hold ~1,000 topics without losing navigability,
> consistency, or learning quality.

Everything below follows from that constraint.

---

## 1. The three entity types

There are exactly three kinds of first-class content. If something you want to
add is not one of these, it does not belong in the content tree.

| Entity | Lives in | Identity | Answers |
|---|---|---|---|
| **Topic** | `topics/<domain>/<id>/` | stable `id` | "What is this, why does it matter, how deeply do I learn it?" |
| **Project** | `projects/<id>/` | stable `id` | "What do I build, and what competency does it prove?" |
| **Path** | `paths/<id>.{yml,md}` | stable `id` | "In what order, for which goal?" |

The critical property: **topics and projects own content; paths own only
ordering.** A path is a list of references. This is what makes the many-to-many
problem tractable.

### Why this matters

`caching` is legitimately part of backend engineering, database engineering,
distributed systems, performance engineering, and system design. In a
directory-as-taxonomy design you must either pick one parent (arbitrary, and
wrong for four of the five audiences) or copy the content (guaranteed drift).

Here, `topics/backend/caching/` is written once. The backend path, the
distributed-systems path, the SRE path, and the Python stack path all reference
`caching` by ID. Improving the topic improves every path simultaneously.

---

## 2. Domains are shelves, not meaning

`topics/backend/`, `topics/databases/`, `topics/systems/` exist so that a human
browsing the file tree is not staring at 1,000 sibling directories. That is
their **only** job.

Consequences you must internalise:

- A topic's domain is **not** its definition. `graph/domains.yml` is a flat,
  deliberately boring list.
- Do **not** nest domains (`topics/backend/apis/rest/`). Depth is where
  navigation dies. One level: `topics/<domain>/<topic-id>/`.
- Moving a topic between domains is a cheap, non-breaking operation, because
  nothing references it by path — everything references it by ID.
- If you cannot decide which domain a topic goes in, **the choice does not
  matter**. Pick one and move on. This is a feature: the architecture removed
  the stakes from an unanswerable question.

The set of domains here differs from the obvious first draft because the obvious
first draft has overlapping shelves. Specific merges, with reasons:

| Rejected | Chosen | Reason |
|---|---|---|
| `web-development/` alongside `backend/` + `frontend/` | `backend/`, `frontend/` | Three shelves for two things; every web topic had two homes. |
| `computer-science/` containing OS + networking | `computer-science/` (theory: data structures, algorithms, complexity), `systems/`, `networking/` | "CS" as a catch-all absorbs everything and stops discriminating. |
| `programming/` + `languages/` | `programming/` (language-agnostic concepts), `stacks/` under `paths/` (language-specific *orderings*) | A language is not a topic; it is a path through topics. See §5. |
| `data/` + `ai-ml/` | `data/`, `ai-ml/` (kept separate) | These genuinely diverge: pipelines/warehousing vs. modelling/training. Kept because the split is real, not cosmetic. |
| `interview-preparation/` | `validation/` | See §7. |
| `resources/` as a top-level content area | `resources` block inside each `topic.yml` | A resource with no topic attached is a link dump. Resources are always *about* something. |

---

## 3. The graph is data. Markdown is prose.

Every published topic directory contains a `topic.yml`. That file is the
**single source of truth** for:

- `id`, `title`, `domain`, `level`, `status`
- `prerequisites` (hard and soft)
- `concepts` and the required depth of each
- `projects` that validate it
- `gates` (how competency is proven)
- `resources`, tiered
- `next`

The Markdown files in the same directory teach. They must not *define* structure
that contradicts `topic.yml`. If `topic.yml` says the hard prerequisites are
`sql` and `networking-fundamentals`, `README.md` may explain *why* those are the
prerequisites, but must not introduce a third one.

**Rationale.** Prose-only prerequisite claims are unenforceable and therefore
always rot. Once the graph is data:

- cycles are detectable (`tools/validate_graph.py`)
- a prerequisite pointing at a nonexistent topic is a CI failure, not a
  discovered-in-6-months embarrassment
- "I know X, what next?" becomes a query, not a reading exercise
- future automation (rendered graphs, personalised paths, progress tooling) has
  something to consume

Schema is specified in [graph-schema.md](graph-schema.md).

### Why YAML, and why a restricted subset

YAML is diff-friendly and readable by non-programmers, who are a large share of
likely contributors. In exchange, the schema restricts itself to maps, lists,
scalars, and block scalars. No anchors, no aliases, no multi-document files, no
flow-style nesting beyond one level. This keeps the files reviewable in a GitHub
diff and keeps the validator simple.

---

## 4. The registry, and the "no empty files" rule

A learning map is only useful if it is **complete enough to show you what you
don't know**. But §5 of the design brief is right that mass-generating empty
files destroys the repository: hundreds of one-line stubs make the project look
finished while teaching nothing, and they make real gaps invisible.

Both requirements are satisfied by separating **node declaration** from
**node content**:

```
graph/registry/<domain>.yml   →  every topic that exists in the map
topics/<domain>/<id>/         →  only topics that have been written
```

Every node in the registry has a `status`:

| Status | Meaning | Directory exists? |
|---|---|---|
| `published` | Written to the quality standard, reviewed | **Yes**, with `topic.yml` |
| `drafting` | Actively being written; content may be incomplete | Yes |
| `planned` | Declared in the map, not yet written | **No** |

So the dependency graph can be complete and navigable from day one, paths can
reference future topics (rendered as "planned — not written yet"), and the
repository contains **zero empty files**. A gap is visibly a gap.

The validator enforces the invariant in both directions: a `published` node
without a directory fails, and a `planned` node *with* a directory fails.

### Where prerequisites live for planned nodes

A `planned` node has no `topic.yml`, so its provisional prerequisites are
declared in the registry entry itself. A `published` node must **not** repeat
prerequisites in the registry — they live in `topic.yml` and only there. The
validator enforces this asymmetry rather than allowing two sources of truth to
coexist and disagree.

When a topic is promoted from `planned` to `published`, its registry
`prerequisites` are moved into the new `topic.yml`. That is a deliberate,
reviewable step in the promotion checklist.

### Why the registry is split per domain

One 100+ node file becomes a permanent merge-conflict bottleneck: every
contributor touches it. Per-domain files (`graph/registry/backend.yml`) mean two
people adding topics in different domains never conflict. The validator
concatenates them, so there is still exactly one logical registry.

---

## 5. Languages and stacks are paths, not topics

Tempting: `topics/languages/python/`. Rejected.

A language is a *lens over shared concepts*. "Python OOP" and "PHP OOP" are 85%
the same idea. If both are topics, you write object-oriented programming twice,
then five more times, and the seventh copy is the only one that is any good.

Instead:

- The concept lives once: `topics/programming/object-oriented-programming/`.
- The language-specific ordering, idioms, ecosystem, and gotchas live in a
  path: `paths/stacks/python-backend.md`.
- Language-specific *practice* lives in the path's steps and in projects.

A stack path therefore reads: "step 4 — `object-oriented-programming`, and here
is what specifically matters about it in Python: dunder methods, descriptors,
`dataclasses`, and why deep inheritance hierarchies are rarer here than in Java."

This is also how the repository stays honest about transferability. A learner
who finishes the Python path can see that eight of its twelve steps were
language-neutral, which is the actual lesson.

---

## 6. Levels are properties, not locations

`level: 3` is a field on the topic. It is never a directory.

A single domain spans the whole range — `databases` runs from
`databases-introduction` (L1) to `distributed-databases` (L4) — so level-based
folders would either fragment domains or duplicate them. Level-as-field also
lets the validator enforce a real invariant:

> A hard prerequisite may not have a higher level than the topic that requires
> it.

That single rule catches a large class of ordering mistakes automatically.

Levels are defined in [levels.md](levels.md); the registry of level IDs is
`graph/levels.yml`.

---

## 7. `validation/` replaces `interview-preparation/`

An `interview-preparation/` directory reliably becomes a question bank, and a
question bank trains recall, which is the failure mode the project exists to
oppose (see [philosophy.md](philosophy.md)).

The replacement inverts the framing. `validation/` holds the machinery for
**proving competency**: gate types, evidence standards, and a reusable library
of design/debugging/benchmark/review challenges.

Interview material still exists — every topic has an `interview.md` — but it is
scoped as *"what a competent engineer should be able to discuss about this
topic, and what a shallow answer looks like"*, not as a list of questions with
answers to memorise.

---

## 8. Full tree

```
.
├── README.md                     Navigation entry point. Optimised for "where do I start?"
├── ROADMAP.md                    Expansion plan, phases, what is deliberately not done yet
├── CONTRIBUTING.md               How to add a topic/project/path without breaking the graph
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
├── LICENSE
│
├── docs/                         How the system works. Not learning content.
│   ├── architecture.md           (this file)
│   ├── philosophy.md             Learning model; tutorial-hell countermeasures
│   ├── levels.md                 L0–L5 competency model + the four competency axes
│   ├── competency-gates.md       Learn → … → Advance, and the gate types
│   ├── progress-tracking.md      Progress states and required evidence
│   ├── resource-tiers.md         Tier 1/2/3 definitions and selection rules
│   ├── technology-selection.md   The trade-off rubric every technology must pass
│   ├── version-awareness.md      Separating concept / implementation / version
│   ├── graph-schema.md           Normative schema for topic.yml, project.yml, path.yml
│   ├── how-to-use.md             The Start Here → Advance loop, in detail
│   └── style-guide.md            Writing and Markdown conventions
│
├── graph/
│   ├── README.md                 How to query and extend the graph
│   ├── domains.yml               Flat list of storage shelves
│   ├── levels.yml                Level registry
│   ├── dependency-map.md         Human-readable core map (rendered diagrams)
│   └── registry/<domain>.yml     Node manifest, one file per domain
│
├── topics/<domain>/<topic-id>/   Written topics only. 9-file standard structure.
│
├── paths/
│   ├── README.md                 How to choose a path; what a path is and is not
│   ├── <path-id>.md              Teaching narrative for humans
│   ├── <path-id>.yml             Ordered step list for machines
│   └── stacks/                   Language/ecosystem-specific paths
│
├── projects/
│   ├── README.md
│   ├── ladder.md                 The full project ladder, L0 → L5
│   └── <project-id>/             project.yml + README.md (the specification)
│
├── validation/
│   ├── README.md                 Evidence standards
│   └── gate-library.md           Reusable design/debug/perf/review/failure challenges
│
├── templates/                    Copy-paste starting points. Kept in sync with the schema.
│   ├── topic/                    All 9 files + topic.yml
│   ├── project/                  project.yml + README.md
│   ├── path/                     path.yml + path.md
│   └── resource-list.md
│
├── tools/
│   ├── README.md
│   └── validate_graph.py         Graph + link + schema validator. Runs in CI.
│
└── .github/                      Issue templates, PR template, CI workflow
```

---

## 9. Standard topic directory

Nine files, always the same names, always in this order of intended reading:

| File | Contains | Must answer |
|---|---|---|
| `topic.yml` | machine-readable definition | — |
| `README.md` | orientation, prerequisites, how deep to go, how to navigate the rest | Q1, Q2, Q3, Q4, Q6, Q10 |
| `fundamentals.md` | the concept from first principles, no tooling | Q1, Q5 |
| `concepts.md` | the concept inventory with required depth per concept | Q5, Q6 |
| `practical.md` | doing it for real: tools, commands, code, failure modes | Q5, Q7 |
| `exercises.md` | small, graded, verifiable drills | Q7 |
| `projects.md` | which projects validate this topic and why | Q8 |
| `interview.md` | what competent discussion sounds like; shallow-answer tells | Q9 |
| `advanced.md` | where the topic goes at L4–L5; open problems; papers | Q6, Q10 |
| `resources.md` | tiered resources with a note on *why* each is listed | Q5 |

("Q1–Q10" are the ten questions in [philosophy.md](philosophy.md#the-ten-questions).)

The nine-file structure is mandatory for `published` topics and is the reason
navigation stays predictable across a thousand topics: a learner who has read
one topic knows exactly where to find things in every other topic.

**A file may be short. A file may not be empty or a placeholder.** If a topic
genuinely has nothing to say under a heading — some L0 topics have no meaningful
`advanced.md` — say that in one sentence and point to where the depth lives
instead. One honest sentence is content; `TODO` is not.

---

## 10. Enforcement

Architecture that is not enforced is a suggestion. `tools/validate_graph.py`
runs on every pull request and checks:

1. Registry: unique IDs, valid `level`, valid `status`, known `domain`.
2. `published`/`drafting` nodes have a directory containing `topic.yml`;
   `planned` nodes do not.
3. `topic.yml` agrees with its registry entry on `id`, `title`, `domain`,
   `level`.
4. `published` registry entries do not duplicate `prerequisites`.
5. All prerequisite / `next` / project / path-step references resolve.
6. The hard-prerequisite graph is acyclic.
7. Hard prerequisites never exceed the level of the topic requiring them.
8. All nine standard files exist for `published` topics, and none is a
   placeholder.
9. Relative Markdown links resolve to real files.
10. Resource entries are well-formed and non-duplicated within a topic.

If a rule here cannot be checked mechanically, it belongs in the PR checklist in
[CONTRIBUTING.md](../CONTRIBUTING.md), not in this list.

---

## 11. Deliberate non-goals

Stated so they are not repeatedly re-proposed:

- **No web application.** The repository must be fully usable in the GitHub UI
  and in a text editor. Tooling may render *additional* views; it may never
  become the only way to read the content.
- **No progress database.** Progress is tracked in the learner's own fork or a
  local file (see [progress-tracking.md](progress-tracking.md)). The project
  stores no user state.
- **No exhaustive link collections.** Curation is the value. See
  [resource-tiers.md](resource-tiers.md).
- **No video-first content.** Text is diffable, reviewable, searchable, and
  translatable. Videos may be *resources*, never the curriculum.
- **No per-language duplication of shared concepts.** See §5.
- **No completion certificates or gamified scoring.** The project's position is
  that the artifacts you build are the credential.
