# Changelog

All notable changes to this repository. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

Versioning here describes the **curriculum**, not software:

- **Major** — a change to the information architecture or the graph schema that requires existing
  content to be migrated.
- **Minor** — new topics, projects, paths, or documents.
- **Patch** — corrections, clarifications, resource updates, `last_reviewed` refreshes.

---

## [Unreleased]

Nothing yet. See [ROADMAP.md](ROADMAP.md) for what is planned next.

---

## [0.1.0] — 2026-08-11

Phase 1: architecture and exemplars. The structure, the graph, and enough written content to
demonstrate the standard at four different levels.

### Added — architecture and documentation

- `docs/architecture.md` — the information architecture, with the rejected alternatives and their
  reasons. The key decisions: domains are storage rather than taxonomy; the graph is data and the
  Markdown is prose; languages and stacks are paths rather than topics; `planned` nodes have no
  directory, so the map is complete without any empty files.
- `docs/philosophy.md` — the ten questions every topic must answer; the
  knowledge → skill → judgment → mastery distinction; the nine-stage competency loop; eight named
  anti-patterns.
- `docs/levels.md` — six levels defined by what a learner can do unaided, each with a "you are here
  when" test, plus the four competency axes that levels do not capture.
- `docs/competency-gates.md` — the nine stages in method detail, and the gate types for advanced
  topics: design, debugging, performance, failure simulation, review, research.
- `docs/graph-schema.md` — normative schema for `registry/v1`, `topic/v1`, `project/v1`, `path/v1`.
- `docs/technology-selection.md` — the eight-question rubric, with Redis worked out in full including
  when not to use it.
- `docs/resource-tiers.md` — Tier 1/2/3 definitions, the selection rules, and what makes a `why`
  field useful.
- `docs/version-awareness.md` — separating fundamental concept from current implementation from
  version-specific detail, with review cadences per `version_sensitivity`.
- `docs/progress-tracking.md` — seven progress states, each with the evidence it requires.
- `docs/how-to-use.md` — the Start Here → Advance loop in detail, including how to use the repository
  badly.
- `docs/style-guide.md` — voice, Markdown conventions, the three-pass method for hard concepts, and
  the eight-question quality bar.

### Added — the graph

- 18 domains, six levels, and a **129-topic registry** split per domain to avoid merge-conflict
  bottlenecks.
- `graph/dependency-map.md` — the graph rendered as Mermaid diagrams by area, plus the
  first-principles chains for caching, HTTP, data structures, and containers.
- Every node carries a level, a status, and a discriminating summary. Every hard prerequisite edge is
  validated: acyclic, level-monotone, and fully resolving.

### Added — written topics

Four topics, nine files each, at four different levels:

- `computer-basics` (L0) — the memory hierarchy and the volatile/persistent distinction, with an
  honestly short `advanced.md` that maps where the depth lives instead of padding.
- `programming-fundamentals` (L1) — the depth markings doing real work: 6 `deep`, 6 `working`, and 3
  deliberately capped at `aware`.
- `data-structures` (L2) — built around the place where theory and measurement openly disagree.
- `caching` (L3) — the full first-principles chain from "why is this slow" to Redis, with failure as
  curriculum.

### Added — projects

Six specifications, Levels 0–3: `machine-anatomy`, `cli-calculator`, `file-organizer`,
`ds-from-scratch`, `in-memory-cache`, `url-shortener`. Each states the competency it validates, the
constraint that stops it becoming assembly work, and how the learner will break it.

`projects/ladder.md` carries the full ladder to Level 5, with a design brief for every planned
project.

### Added — paths

Five paths with validated step ordering: `absolute-beginner`, `programming-foundations`,
`computer-science-foundations`, `software-engineering-core` (the L0→L4 spine, 70 steps), and
`stacks/python-backend` (the reference stack path).

Twelve further paths declared as design briefs in `paths/README.md`.

### Added — validation and tooling

- `validation/` — evidence standards and a gate library of reusable design challenges, debugging
  scenarios, failure simulations, review exercises, and research exercises.
- `tools/validate_graph.py` — checks registry consistency, the `published`/`planned` directory
  invariant in both directions, schema conformance, reference resolution, prerequisite acyclicity,
  level monotonicity, the nine-file requirement with placeholder detection, path step ordering,
  resource well-formedness, and relative Markdown links including heading anchors. No network access.
- `templates/` — the full set, with authoring guidance inline, kept in sync with the schema.
- GitHub Actions workflow, four issue templates, and a pull request template.

### Notes

- Most of the 129 topics are `status: planned` — declared in the map with no directory. This is
  deliberate: a complete map with visible gaps is more useful than an incomplete map that hides them
  behind stubs, and the repository contains zero placeholder files.
- The validator rejects any published topic file under 400 characters or containing a placeholder
  marker, which is how the "no empty files" rule is enforced rather than merely stated.

[Unreleased]: https://github.com/imrankabir02/EngineeringAtlas/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/imrankabir02/EngineeringAtlas/releases/tag/v0.1.0
