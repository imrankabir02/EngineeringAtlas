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

### Changed — the dependency map is now generated, and renders on mobile

The diagrams in `graph/dependency-map.md` were hand-written Mermaid. Two problems, one reported and
one found while investigating it:

- **GitHub does not render Mermaid in its mobile apps** — only on the web — so the whole file
  degraded to raw source on a phone. This is a documented limitation that GitHub has said is not on
  their roadmap.
- The diagrams were the **only hand-maintained duplication in the repository**: the graph could say
  one thing and the picture another, with nothing to catch the drift.

Both are now fixed by deriving the diagrams from the graph and shipping them as images plus text.

- **Added `tools/generate_diagrams.py`** — derives each view's Mermaid source, a theme-aware
  `<picture>` block, and a **collapsible table of every hard prerequisite** from
  `graph/registry/` and the new `graph/diagrams.yml`. Manages a delimited region of
  `dependency-map.md`; `--check` verifies the committed output is current and runs in CI.
- **Added `tools/render_diagrams.sh`** — renders light and dark SVGs, reusing a preinstalled
  Chromium where one exists.
- **Added `graph/diagrams.yml`** — view definitions plus the authored prose (titles, captions, and
  the commentary under each diagram). Structure comes from the registry; judgment stays here.
- **Added `graph/diagrams/`** — generated `.mmd` sources and 14 SVGs.

Notable details:

- **Every diagram now ships twice.** The image is the overview; the table is what actually works
  under ctrl-F, in a screen reader, and on a phone, where a 2,600-pixel-wide graph is tappable but
  not readable. Both derive from one source, so they cannot disagree. Where coverage differs the
  table is complete.
- **CI needs no browser.** Stage 1 records a checksum per `.mmd`; stage 2 stamps it into the SVG it
  produced. The Python-only `--check` compares both links in that chain, catching all three
  staleness modes — graph changed, `.mmd` not regenerated, SVG not re-rendered.
- **The generated Mermaid is more robust than the hand-written version was.** Every label is quoted,
  and emphasis uses `classDef` rather than `<b>`, which was verified to disappear silently when
  Mermaid's `htmlLabels` are disabled. No colours are hard-coded, so one source renders correctly in
  both themes.
- **Images draw only cross-area prerequisites shared by two or more topics in a view.** Drawing every
  one-off dependency laid one view out at a 6:1 aspect ratio, illegible at any size. The table carries
  the rest.
- **Split the operations diagram** into "Operations and cloud" and "Security" — a layout fix and the
  more honest grouping, since security depends on other areas rather than on other security topics.

### Added

- `validate_graph.py` now checks **image references** too — Markdown images plus `<img src>` and
  `<source srcset>` — so a theme-aware `<picture>` block cannot rot silently.
- `docs/style-guide.md` gains two rules: do not hand-write Mermaid for a graph derived from the
  registry, and anything conveyed only by a picture must also exist as text with an `alt`.

See [ROADMAP.md](ROADMAP.md) for what is planned next — this work was brought forward from Phase 5.

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
