# Tools

## `validate_graph.py`

The enforcement mechanism for the architecture. Architecture that is not enforced is a suggestion.

```bash
pip install pyyaml

python3 tools/validate_graph.py              # validate everything
python3 tools/validate_graph.py --stats      # also print graph statistics
python3 tools/validate_graph.py --no-links   # skip markdown link checking (faster)
python3 tools/validate_graph.py --quiet      # errors only
```

Exit code 0 means valid. Runs on every push and pull request via
[`.github/workflows/validate.yml`](../.github/workflows/validate.yml).

**No network access.** Relative links within the repository are checked; external URLs are not, so a
temporarily unreachable site can never block a pull request. External link checking belongs in a
scheduled job — see [ROADMAP.md](../ROADMAP.md).

---

## What it checks

| Area | Rules |
|---|---|
| **Registry** | Unique IDs, known domain matching the filename, valid level and status, non-empty summary |
| **Directory invariant** | `published`/`drafting` nodes have a directory containing `topic.yml`, at the canonical path; `planned` nodes have **no** directory |
| **Single source of truth** | `published` registry entries must not duplicate `prerequisites` — those live in `topic.yml` |
| **Schema** | Required fields present, unknown keys rejected, types correct, `last_reviewed` not in the future |
| **References** | Every prerequisite, `next`, project, path-step, and concept reference resolves |
| **Acyclicity** | No cycles in the hard-prerequisite graph. Soft edges may cycle — two topics can genuinely illuminate each other |
| **Level monotonicity** | A hard prerequisite may not be at a higher level than the topic requiring it |
| **Nine files** | Published topics have all nine, none under 400 characters, none containing a placeholder marker, each starting with a single `#` heading, and no unexpected files |
| **Depth honesty** | Rejects a topic where every concept is marked `deep` — that is a failure to answer "how deeply?" |
| **Gates** | `build` and `explain` mandatory; every gate a non-empty list of strings |
| **Resources** | Tier 1 and Tier 2 non-empty, Tier 3 capped at five, every entry has a `why`, no duplicate URLs, absolute URLs |
| **Path ordering** | Every step's hard prerequisites appear earlier in the path, in a prerequisite path, or below `entry_level`; at least one milestone; no duplicate topics |
| **Links** | Relative Markdown links resolve to real files; heading anchors checked as warnings |
| **YAML subset** | No tabs, no anchors or aliases, and prose accidentally parsed as a mapping is caught with a specific error |

The last one deserves a note. A YAML scalar containing `": "` silently becomes a single-key mapping:

```yaml
- A written analysis explains each gap: constant factors and memory layout
```

That is a mapping, not a string, and the resulting downstream error ("must be a list of strings")
does not point at the cause. The validator detects mapping keys that look like prose and reports it
directly: *"looks like prose that YAML parsed as a mapping, because it contains ': '. Quote the whole
value."*

It is the single most common authoring mistake in this schema, and a clear error message for it saves
more contributor time than any other check.

---

## Design notes

**Errors versus warnings.** Errors fail CI; warnings do not. Only broken heading anchors are warnings,
because anchor generation varies between renderers and a wrong anchor degrades gracefully — the link
still opens the right file.

**Anchor slugs approximate GitHub's algorithm.** Lowercase, drop characters that are not
alphanumeric, space, or hyphen, then map each remaining space to a single hyphen — *individually*, not
collapsing runs, because GitHub does the same. `"A → B"` becomes `a--b`, not `a-b`. Getting this wrong
produces a stream of false positives on any heading containing an arrow or an em dash.

**Fenced code blocks are stripped before link checking.** Example links inside code samples are
documentation, not references, and treating them as real links makes the style guide unlintable.

**Cycle reporting gives one representative cycle per strongly connected component**, not every cycle.
A dependency cycle usually has one cause, and printing hundreds of paths through it obscures it.

**Unknown keys are errors, not warnings.** A typo in a field name would otherwise silently disable a
check. The cost is that adding a field requires touching this file and
[graph-schema.md](../docs/graph-schema.md) in the same pull request, which is the intended discipline
— the schema document and the validator must not diverge.

---

## Extending it

If a rule can be checked mechanically, it belongs here. If it cannot, it belongs in the pull request
checklist in [CONTRIBUTING.md](../CONTRIBUTING.md) — not in both, and not nowhere.

To add a rule:

1. Document it in [`docs/graph-schema.md`](../docs/graph-schema.md) first. The schema is normative;
   the validator implements it.
2. Add the check, and add the new key to the relevant `*_KEYS` set if it is a new field.
3. Make the error message say **what to do**, not only what is wrong. Compare *"invalid gate"* with
   *"gate 'build' must be a non-empty list of strings"* — the second one is actionable, and
   contributors will read it far more often than they read the schema.
4. Verify it catches the mistake by making that mistake on purpose. A check you have not seen fail is
   a check you have not tested.

The script deliberately has one dependency (PyYAML) and lives in one file. It is meant to be readable
by a contributor who wants to know why their pull request failed, which rules out any framework.
