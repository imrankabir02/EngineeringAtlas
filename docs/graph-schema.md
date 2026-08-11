# Graph Schema (normative)

This is the contract. `tools/validate_graph.py` enforces it, and CI runs the
validator on every pull request.

Four file kinds:

| File | Schema tag | Purpose |
|---|---|---|
| `graph/registry/<domain>.yml` | `registry/v1` | Declares which topics exist in the map |
| `topics/<domain>/<id>/topic.yml` | `topic/v1` | Authoritative definition of a written topic |
| `projects/<id>/project.yml` | `project/v1` | Project specification |
| `paths/<id>.yml`, `paths/stacks/<id>.yml` | `path/v1` | Ordered learning path |

Supporting registries: `graph/domains.yml`, `graph/levels.yml`.

---

## Conventions

**IDs** — lowercase, `a–z`, `0–9`, hyphens. No underscores, no slashes, no
version numbers. Regex: `^[a-z][a-z0-9]*(-[a-z0-9]+)*$`

IDs are permanent. Renaming one breaks every reference to it, so choose for the
long term:

- Name the *concept*, not the product: `caching`, not `redis`.
- Name the *stable* thing: `containers-and-docker` is acceptable because Docker
  is load-bearing history; `kubernetes-1-29` is not.
- Do not encode level or domain into the ID. Both are fields, and both can
  change.

**YAML subset** — maps, lists, scalars, and `>`/`|` block scalars only. No
anchors, aliases, merge keys, multi-document files, or flow-style collections
nested more than one deep. This keeps diffs readable and the validator small.

**Dates** — `YYYY-MM-DD`.

**Unknown keys are errors,** not silently ignored. If you need a new field,
change this document and the validator in the same pull request.

---

## `registry/v1`

One file per domain, at `graph/registry/<domain>.yml`. The filename must equal
the domain ID.

```yaml
schema: registry/v1
domain: backend

topics:
  - id: rest-apis
    title: REST APIs
    level: 2
    status: published
    dir: topics/backend/rest-apis
    summary: >
      Resource-oriented HTTP APIs: modelling resources, choosing methods and
      status codes, idempotency, versioning, and error design.

  - id: api-gateways
    title: API Gateways
    level: 4
    status: planned
    summary: >
      Edge routing, authentication offload, rate limiting, and the cost of
      putting a single component in front of everything.
    prerequisites:
      hard: [rest-apis, caching]
      soft: [kubernetes]
```

### Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `schema` | string | yes | `registry/v1` |
| `domain` | id | yes | must exist in `graph/domains.yml` and match the filename |
| `topics` | list | yes | may be empty for a reserved domain |

Each entry in `topics`:

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | id | yes | globally unique across **all** registry files |
| `title` | string | yes | human title; sentence case except proper nouns |
| `level` | int 0–5 | yes | must exist in `graph/levels.yml` |
| `status` | enum | yes | `published` \| `drafting` \| `planned` |
| `summary` | string | yes | 1–3 sentences. What it is and why it matters. |
| `dir` | path | conditional | **required** for `published`/`drafting`, **forbidden** for `planned` |
| `prerequisites` | map | conditional | **forbidden** for `published`/`drafting` (they live in `topic.yml`), optional for `planned` |

The `prerequisites` asymmetry is deliberate and enforced: a written topic has
exactly one source of truth for its prerequisites. See
[architecture.md §4](architecture.md#where-prerequisites-live-for-planned-nodes).

---

## `topic/v1`

At `topics/<domain>/<id>/topic.yml`. Required for `published` and `drafting`
nodes.

```yaml
schema: topic/v1
id: caching
title: Caching
domain: backend
level: 3
status: published

summary: >
  Keeping a copy of data closer to its reader to trade memory and correctness
  risk for latency. Covers locality, invalidation, eviction, stampedes, and
  distributed caches.

why_it_matters: >
  Caching is the most common way to make a system fast and the most common
  source of "impossible" bugs. Every layer of a real system caches, usually
  without being asked.

effort:
  focused_hours: 40
  calendar_weeks: "3-5"
  assumes: >
    Prerequisites met, roughly 8 focused hours per week, including the project.

prerequisites:
  hard:
    - id: networking-fundamentals
      why: You cannot reason about latency savings without knowing what a round trip costs.
    - id: sql
      why: The canonical cache sits in front of a database; you must know what it is protecting.
  soft:
    - id: operating-systems-fundamentals
      why: Page cache and memory hierarchy make eviction policy concrete rather than abstract.

first_principles_chain:
  - Why is this request slow? Measure before assuming.
  - Memory is orders of magnitude faster than disk or network.
  - Some data is read far more often than it changes.
  - Therefore keep a copy closer to the reader.
  - A second copy of the truth can be wrong -> invalidation.
  - The copy is smaller than the truth -> eviction.
  - One machine's memory is not enough -> distributed caching.
  - Redis, Memcached, and CDNs are implementations of the above.

concepts:
  - id: locality
    name: Locality of reference
    depth: deep
    note: Temporal and spatial locality; why caching works at all.
  - id: eviction
    name: Eviction policies
    depth: working
    note: LRU, LFU, TTL, ARC. Know LRU deeply, the rest by shape.
  - id: cache-coherence-hardware
    name: Hardware cache coherence
    depth: aware
    note: Know it exists and that it constrains multi-core performance.

gates:
  build:
    - Implement an LRU cache with O(1) get and put, in front of a real datastore.
  break:
    - Force a cache stampede with concurrent misses on a hot key; observe origin load.
    - Serve deliberately stale data and trace the resulting user-visible bug.
  debug:
    - Given a wrong-value bug, determine which cache layer served it.
  explain:
    - Explain cache-aside vs write-through and when each is wrong, in writing.
  benchmark:
    - Measure p50/p95/p99 with the cache cold, warm, and disabled; report hit ratio.
  review:
    - Review a peer's caching layer and identify one invalidation hazard.

projects:
  - id: in-memory-cache
    role: core
    validates: [locality, eviction]
  - id: url-shortener
    role: stretch

resources:
  tier1:
    - title: Redis documentation — key eviction
      url: https://redis.io/docs/latest/develop/reference/eviction/
      why: The authoritative description of a real eviction implementation.
  tier2:
    - title: "Designing Data-Intensive Applications, ch. 1-3"
      url: https://dataintensive.net/
      why: Places caching inside the broader storage and latency picture.
  tier3:
    - title: Caching at Netflix — EVCache
      url: https://netflixtechblog.com/announcing-evcache-distributed-in-memory-datastore-for-cloud-c42d99f8ab5f
      why: A production distributed cache with its constraints stated.

next:
  - id: message-queues-and-streaming
    why: The next tool for decoupling load from the origin.
  - id: distributed-systems-fundamentals
    why: Two copies of the truth is the entry point to consistency.

version_sensitivity: low
last_reviewed: 2026-08-11
maintainers: []
```

### Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `schema` | string | yes | `topic/v1` |
| `id`, `title`, `domain`, `level`, `status` | — | yes | must match the registry entry exactly |
| `summary` | string | yes | 1–3 sentences |
| `why_it_matters` | string | yes | Concretely: what breaks or costs more without this |
| `effort` | map | yes | `focused_hours` (int), `calendar_weeks` (string range), `assumes` (string) |
| `prerequisites` | map | yes | `hard` and/or `soft`, each a list of `{id, why}` |
| `first_principles_chain` | list of strings | yes | Problem → answer steps, in order. Min 3. |
| `concepts` | list | yes | `{id, name, depth, note}`. `depth` ∈ `aware`\|`working`\|`deep`. |
| `gates` | map | yes | Keys from the gate vocabulary; each a list of strings. `build` and `explain` are mandatory. |
| `projects` | list | no | `{id, role, validates?}`. `role` ∈ `core`\|`stretch`. |
| `resources` | map | yes | `tier1`/`tier2`/`tier3`, each a list of `{title, url, why}` |
| `next` | list | yes | `{id, why}` |
| `version_sensitivity` | enum | yes | `low`\|`medium`\|`high` — see [version-awareness.md](version-awareness.md) |
| `last_reviewed` | date | yes | |
| `maintainers` | list of strings | yes | GitHub handles; may be empty |

### Rules the validator enforces

1. `prerequisites.hard[].id` and `.soft[].id` resolve to registry IDs.
2. No cycles in the **hard** prerequisite graph. (Soft edges may cycle: two
   topics can genuinely illuminate each other.)
3. For every hard prerequisite `p`: `level(p) <= level(topic)`.
4. `projects[].id` resolves to a `projects/<id>/project.yml`.
5. `next[].id` resolves to a registry ID, and is not a hard prerequisite of this
   topic.
6. Every `concepts[].depth` is in the vocabulary; every concept has a `note`.
7. `gates` contains at least `build` and `explain`. Every gate item is a
   sentence describing an action with an observable outcome.
8. `resources`: `tier1` and `tier2` each have ≥1 entry; every entry has a
   non-empty `why`; no duplicate URLs within the topic.
9. `last_reviewed` is not in the future.
10. For `published` topics, all nine standard Markdown files exist and none is a
    placeholder (see [architecture.md §9](architecture.md#9-standard-topic-directory)).

### Depth vocabulary

Answering "how deeply should I learn it?" — schema question 6.

| `depth` | Means | Test |
|---|---|---|
| `aware` | You know it exists, roughly what it does, and when to go read about it. | You would not be surprised by the term in a design review, and you know it is relevant. |
| `working` | You can use it correctly and explain the trade-off without notes. | You can apply it to a new problem and defend the choice. |
| `deep` | You understand the mechanism well enough to debug it and predict its failure modes. | You can explain *how* it works, implement a simplified version, and say where it breaks. |

Most concepts in most topics should be `working`. A topic with everything marked
`deep` has not made a judgment call and will be rejected in review: telling the
learner what they can safely skim is as valuable as telling them what to master.

---

## `project/v1`

At `projects/<id>/project.yml`, with a sibling `README.md` holding the full
specification.

```yaml
schema: project/v1
id: in-memory-cache
title: In-memory cache with eviction
level: 3

summary: >
  A cache library with pluggable eviction, TTLs, metrics, and a benchmark
  harness, placed in front of a real datastore.

validates:
  - Can implement an O(1) LRU and prove the complexity claim by measurement.
  - Can reason about invalidation as a correctness problem, not a detail.
  - Can produce a benchmark whose numbers a reviewer would trust.

topics: [caching, data-structures, concurrency-and-parallelism]

constraints:
  - No third-party cache library. Standard library only.
  - Must be thread-safe, and you must demonstrate the race it prevents.
  - Must expose hit ratio, eviction count, and latency percentiles.

stages:
  - name: Correct
    goal: A working cache with a fixed capacity and one eviction policy.
    done_when:
      - Unit tests cover eviction order, TTL expiry, and capacity edge cases.
  - name: Concurrent
    goal: Safe under parallel readers and writers.
    done_when:
      - A test fails reliably without the lock and passes with it.
  - name: Measured
    goal: Numbers you can defend.
    done_when:
      - Benchmark reports p50/p95/p99 for hit and miss paths, with warm-up excluded.
      - You can explain the shape of the latency distribution.

break_it:
  - Set capacity to 1 and drive a workload with 2 hot keys. Explain the result.
  - Trigger a stampede: 500 concurrent misses on the same cold key.

anti_patterns:
  - Wrapping a dictionary and calling it done. The eviction is the project.
  - Benchmarking with a uniform random key distribution only; real traffic is skewed.

stretch:
  - Add a second eviction policy and compare hit ratios on a Zipfian workload.
  - Make it distributed across two processes with consistent hashing.
```

| Field | Type | Required |
|---|---|---|
| `schema`, `id`, `title`, `level`, `summary` | — | yes |
| `validates` | list of strings | yes — competency statements, not features |
| `topics` | list of ids | yes — must resolve to registry IDs |
| `constraints` | list of strings | yes — what makes it educational rather than assembly |
| `stages` | list of `{name, goal, done_when[]}` | yes — min 2 |
| `break_it` | list of strings | yes — see [philosophy.md](philosophy.md#the-competency-loop) |
| `anti_patterns` | list of strings | yes |
| `stretch` | list of strings | no |

`validates` is the field that justifies the project's existence. "Builds a REST
API" is not a competency statement. "Can design an idempotent write endpoint and
demonstrate that a duplicated request causes no double charge" is.

---

## `path/v1`

At `paths/<id>.yml` (or `paths/stacks/<id>.yml`), with a sibling `.md` carrying
the teaching narrative.

```yaml
schema: path/v1
id: python-backend
title: Python backend engineer
audience: >
  Someone who can already write small programs and wants to build and operate
  production Python services.
entry_level: 1
exit_level: 4
prerequisite_paths: [programming-fundamentals]

steps:
  - topic: object-oriented-programming
    emphasis: >
      Dataclasses, protocols, and composition. Skip deep inheritance
      hierarchies; Python's duck typing makes them rarer than in Java.
    projects: [notes-cli]
  - topic: testing-fundamentals
    emphasis: pytest fixtures, parametrisation, and what not to mock.
  - milestone: >
      You can build a tested Python package with a CLI and publish it.
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `schema`, `id`, `title`, `audience` | — | yes | |
| `entry_level`, `exit_level` | int 0–5 | yes | `exit_level` > `entry_level` |
| `prerequisite_paths` | list of path ids | no | |
| `steps` | list | yes | each item is **either** a step or a milestone |

A **step** has `topic` (required, resolves to a registry ID), optional
`emphasis` (what specifically matters *here* — this is where stack-specific
guidance lives), and optional `projects` (list of project IDs).

A **milestone** has only `milestone`: a capability statement marking a
checkpoint. Milestones are how a path says "stop and prove something" rather
than listing 40 topics in a row.

### Rules

1. Every `steps[].topic` resolves to a registry ID.
2. Every `steps[].projects[]` resolves to a project ID.
3. A step's hard prerequisites must appear **earlier** in the same path, or in a
   `prerequisite_paths` path, or be strictly below `entry_level`. This is the
   check that makes paths trustworthy — it mechanically prevents the
   "framework before fundamentals" ordering error.
4. No duplicate `topic` values within a path.
5. `steps` contains at least one milestone.

---

## `graph/domains.yml` and `graph/levels.yml`

```yaml
schema: domains/v1
domains:
  - id: backend
    title: Backend
    description: Server-side application engineering.
```

```yaml
schema: levels/v1
levels:
  - id: 0
    name: Absolute Beginner
    test: Can operate a computer deliberately rather than by memorised clicks.
```

Both are small, stable, and changed rarely. Adding a domain requires a
justification in the pull request: a new shelf is only warranted when an
existing shelf would hold more than roughly 25 topics.

---

## Running the validator

```bash
python3 tools/validate_graph.py           # validate everything
python3 tools/validate_graph.py --stats   # also print graph statistics
python3 tools/validate_graph.py --no-links  # skip Markdown link checking
```

Exit code 0 means valid. No network access is performed — link checking is
limited to relative links within the repository. External URLs are checked by a
separate scheduled job so that a temporarily unreachable site cannot block a
pull request.
