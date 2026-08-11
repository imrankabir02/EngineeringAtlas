<!-- Thank you for contributing. Delete the sections that do not apply. -->

## What this changes

<!-- One or two sentences. If it adds a topic, project, or path, name it. -->

## Type

- [ ] Graph node added or corrected (`graph/registry/`)
- [ ] New written topic
- [ ] New project specification
- [ ] New path
- [ ] Correction to existing content
- [ ] Documentation or tooling
- [ ] Gate challenge added to `validation/gate-library.md`

## Checks

- [ ] `python3 tools/validate_graph.py` passes locally
- [ ] Prose wrapped at 80 characters (tables, code, and URLs exempt)
- [ ] All `AUTHOR:` template comments deleted
- [ ] Relative links only — no `github.com` URLs between files
- [ ] One topic per pull request

---

## For a new topic

<!-- Delete this section if not adding a topic. -->

**Topic:** `topic-id` · **Level:** N · **Domain:** `domain`

### The eight quality questions

<!-- From docs/style-guide.md. Answer each in a sentence rather than ticking it - the answers
     are what the review discusses. -->

| Test | Your answer |
|---|---|
| **Completeness** — essential concepts present, nothing important silently omitted? | |
| **Dependency** — prerequisites correct, minimal, correctly ordered? | |
| **Depth** — goes past what a good tutorial would cover? | |
| **Practicality** — does the learner build something real? | |
| **Understanding** — explains *why* it works, not only how to use it? | |
| **Validation** — can the learner prove competency, with declared gates? | |
| **Production** — addresses real operation, not just the happy path? | |
| **Evolution** — still correct after the current tooling generation is replaced? | |

**Evolution is the most commonly failed.** If every tool named in `fundamentals.md` and
`concepts.md` were replaced next year, how much would still be true?

### Schema specifics

- [ ] Registry entry updated: `status` → `published`, `dir` added, `prerequisites` **moved** into
      `topic.yml` with a `why` on each
- [ ] Concept depths make a real judgment call — not everything marked `deep`
- [ ] `aware` concepts name the topic that properly treats each one
- [ ] Every gate is an **action with an observable outcome** (not "understand X")
- [ ] `first_principles_chain` steps are *problems*, each answered by the next step
- [ ] At least one Tier 1 and one Tier 2 resource; every `why` explains the **selection**, not the
      resource
- [ ] Tier 3 has at most five entries
- [ ] `effort` is a range with stated assumptions
- [ ] Version-specific claims are marked and confined to `practical.md`
- [ ] All nine files present; none is a placeholder (short is fine, `TODO` is not)

---

## For a new project

<!-- Delete if not adding a project. -->

- [ ] `validates` states **competencies**, not features ("Can design an idempotent write endpoint and
      demonstrate that a duplicated request causes no double charge" — not "builds a REST API")
- [ ] At least one constraint prevents shortcutting the lesson, with the reason stated
- [ ] `break_it` contains failures the learner must cause deliberately
- [ ] Finishable by a learner at that level in one to three weeks part-time
- [ ] Specifies *what* and *why*, leaving *how* to the learner — **not a walkthrough**

**The test for the last one:** could a reader follow this to a working system without making a
decision? If yes, it is a tutorial.

---

## For a new path

<!-- Delete if not adding a path. -->

- [ ] Audience is a specific person with a goal stated as a **capability**
- [ ] Differs from every existing path by more than a few steps
- [ ] Steps carry `emphasis` notes saying what matters *here* — not a bare topic list
- [ ] At least one milestone, stated as a capability with evidence
- [ ] Narrative includes an honest effort estimate in ranges, with assumptions
- [ ] Validator's step-ordering check passes

---

## Anything you are unsure about

<!-- Genuinely useful to state. A design decision you were torn on, a claim you would like checked,
     a level you were unsure of. Reviewers can help with a named uncertainty and cannot with an
     unnamed one. -->
