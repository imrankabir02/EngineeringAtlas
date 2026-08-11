# Learning paths

A path is a **curated ordering of topics for a goal.** It owns no content — every step is a
reference to a topic that lives once in [`topics/`](../topics/). That is what lets a topic
appear in ten paths without being written ten times, and it is the central architectural
decision of this repository ([architecture.md §1](../docs/architecture.md#1-the-three-entity-types)).

Each path has two files:

- `<id>.md` — the teaching narrative: phases, what to expect, where people stall.
- `<id>.yml` — the machine-readable step list, validated in CI.

The `.yml` is authoritative for ordering. The `.md` explains it.

---

## Available paths

| Path | Entry → Exit | For |
|---|---|---|
| [Absolute beginner](absolute-beginner.md) | L0 → L1 | Never studied technology. Ends when you can write and debug a real program unaided |
| [Programming foundations](programming-foundations.md) | L1 → L2 | The language-agnostic programming and engineering foundation everything else needs |
| [Computer science foundations](computer-science-foundations.md) | L2 → L4 | The theory that predicts behaviour: structures, complexity, algorithms, papers |
| [Software engineering, beginner to advanced](software-engineering-core.md) | L0 → L4 | **The spine.** No background assumed, ends at production accountability |
| [Python backend engineer](stacks/python-backend.md) | L1 → L4 | The reference stack path: Python from fundamentals to production |

**If you are unsure, start with [software-engineering-core](software-engineering-core.md).**
It is the longest path and it subsumes most of the others; the shorter paths are slices of it
for people who already have parts.

---

## Choosing one

Pick **one**. Two paths at once is
[technology hopping](../docs/philosophy.md#technology-hopping) with extra structure.

The choice is driven by a goal stated as a capability, not a job title:

| Weak goal | Usable goal | Path |
|---|---|---|
| "Learn to code" | "Write and debug a 300-line program I designed" | [absolute-beginner](absolute-beginner.md) |
| "Learn backend" | "Build and operate an API that survives its dependencies failing" | [software-engineering-core](software-engineering-core.md) |
| "Learn Python" | "Build and operate a production Python service" | [python-backend](stacks/python-backend.md) |
| "Get better at algorithms" | "Reason about cost before writing code, and read a paper" | [computer-science-foundations](computer-science-foundations.md) |
| "Become a senior engineer" | "Be accountable for a system: its scale, cost, and incidents" | [software-engineering-core](software-engineering-core.md), phases 4–5 |

Then find your current level with the "you are here when" tests in
[levels.md](../docs/levels.md) — **not** by reading the level descriptions and picking the one
that sounds like you. Everyone overestimates that, in a well-documented direction.

---

## How to read a path

**Steps** are topics, in dependency order, sometimes with an `emphasis` note saying what
specifically matters *in this context*. The emphasis is where stack-specific and role-specific
guidance lives — the same `object-oriented-programming` topic gets different emphasis in a Python
path than it would in a Java one, without the content being duplicated.

**Milestones** are checkpoints stated as capabilities. They are the point of the path's
structure: a path that listed 60 topics in a row would tell you nothing about whether you were
ready to continue. When you reach a milestone, stop and verify it honestly. If you cannot pass
it, the topics behind it are not finished, regardless of how much you have read.

**Projects** attached to a step are the ones that validate it. Do the `core` ones.

**Planned topics.** Most topics in the map are `planned` — declared in the graph, not yet
written. A path step pointing at a planned topic still tells you what to learn and in what
order; you use external resources for the content. This is deliberate: a complete map with
honest gaps is more useful than an incomplete map that hides them. See
[architecture.md §4](../docs/architecture.md#4-the-registry-and-the-no-empty-files-rule).

---

## Paths do not have to be followed exactly

You may skip a topic. Sometimes it is correct — a deadline decides, or you already have it, or it
is genuinely not relevant to your goal.

**Write down what you skipped.** The bill arrives later as a bug you cannot explain, and knowing
what you skipped turns three days of confusion into ten minutes. Every hard prerequisite in this
repository is there because its absence causes a specific, predictable failure later.

What you should not do is reorder freely. The orderings are validated: CI checks that every
step's hard prerequisites appear earlier in the path, in a prerequisite path, or below the
path's entry level. That check is the mechanical version of "no framework before fundamentals",
and it is the reason a path here can be trusted in a way an arbitrary curriculum cannot.

---

## Planned paths

These are declared design briefs, not placeholders. Each states its audience and its
distinguishing content, which is what a contributor would work from. See
[ROADMAP.md](../ROADMAP.md) for sequencing.

| Path | Entry → Exit | What distinguishes it |
|---|---|---|
| **Frontend engineer** | L1 → L4 | Browser internals before frameworks; rendering strategy; accessibility as a requirement; performance measured on hardware users own |
| **Full-stack engineer** | L1 → L4 | The frontend and backend paths interleaved, with the boundary itself — API contracts, auth across the boundary, and where state lives — as first-class content |
| **DevOps engineer** | L1 → L4 | Linux and networking depth first, then containers, IaC, pipelines, and the SRE material. Explicitly includes when *not* to adopt Kubernetes |
| **Cloud engineer** | L2 → L4 | Provider primitives, identity as the real perimeter, cost as a design constraint, and multi-region trade-offs |
| **Data engineer** | L2 → L4 | SQL depth, pipeline idempotency and replay, warehousing, batch and stream processing, and data quality as a testable property |
| **AI/ML engineer** | L2 → L4 | Statistics and evaluation before models; MLOps; and honest treatment of when the answer is not machine learning |
| **Cybersecurity engineer** | L2 → L4 | Networking and OS depth first, then application security, cryptography in practice, offensive techniques within authorised scope, and detection |
| **System architect** | L3 → L5 | Distributed systems depth, trade-off documentation, capacity and cost, and the L5 material on abstractions and decisions under uncertainty |
| **Research engineer** | L3 → L5 | Reading source code and papers, experiment design, benchmarking that others can reproduce, and building what does not exist |
| **PHP / Laravel** | L1 → L4 | Modern PHP, Composer, Laravel, queues, and the same shared topics with PHP-specific emphasis |
| **JavaScript / TypeScript full-stack** | L1 → L4 | Browser fundamentals, TypeScript, Node, and the shared backend topics with Node-specific emphasis |
| **Go backend** | L1 → L4 | Explicit errors, goroutines and channels, and a standard-library-first culture as a contrast to Python's |

**A note on stack paths.** The Python path is the reference implementation, and reading it shows
why the others are cheap to add: roughly 80% of its steps are language-neutral topics with a
paragraph of Python-specific emphasis. A new stack path is mostly a matter of writing those
paragraphs, not writing a curriculum. It is also, deliberately, the honest lesson for the
learner — most of what you learn transfers.

---

## Adding a path

Copy [`templates/path/`](../templates/path/) and read [CONTRIBUTING.md](../CONTRIBUTING.md).

The bar:

| Test | Question |
|---|---|
| **Audience** | Is there a specific person with a specific goal, stated as a capability? |
| **Distinct** | Does it differ from an existing path by more than a few steps? If not, add emphasis to that path instead |
| **Ordered** | Does the validator pass? Every hard prerequisite reachable before its step |
| **Milestones** | At least one, stated as a capability with evidence — not "finished the section" |
| **Emphasis** | Do the steps say what matters *here*, or is it a bare topic list? A bare list adds nothing over the graph |
| **Honest about scale** | Does the narrative state realistic effort, in ranges, with assumptions? |

The most common rejected proposal is a path that duplicates an existing one with a different
name. Two paths differing in three steps should be one path with a note.
