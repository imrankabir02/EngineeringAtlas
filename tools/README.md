# Tools

| Tool | Does | Needs |
|---|---|---|
| [`validate_graph.py`](#validate_graphpy) | Enforces the architecture. Runs in CI | PyYAML |
| [`generate_diagrams.py`](#generate_diagramspy) | Derives the dependency-map diagrams and tables from the graph. Freshness check runs in CI | PyYAML |
| [`render_diagrams.sh`](#render_diagramssh) | Renders the diagram sources to light/dark SVGs | Node + Chromium |

---

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
| **Images** | Markdown images and the HTML forms — `<img src>`, `<source srcset>` — resolve, so a theme-aware `<picture>` block cannot rot silently |
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

---

## `generate_diagrams.py`

Derives the diagrams in [`graph/dependency-map.md`](../graph/dependency-map.md) from
[`graph/registry/`](../graph/registry/) and the view definitions in
[`graph/diagrams.yml`](../graph/diagrams.yml).

```bash
python3 tools/generate_diagrams.py           # write .mmd, the manifest, and the map's diagram region
python3 tools/generate_diagrams.py --check   # verify committed output is current (runs in CI)
```

Per view it emits a Mermaid source, and into `dependency-map.md`: a theme-aware `<picture>` block, a
legend, and a **collapsible table of every hard prerequisite**.

Three decisions worth knowing:

**Why images at all, when GitHub renders Mermaid.** It renders Mermaid on the *web* and not in its
mobile apps, where a ` ```mermaid ` fence degrades to raw source. Committed SVGs render everywhere.

**Why a table as well as an image.** The largest diagram is 2,600 pixels wide. Scaled to a phone that
is tappable but not readable, and it is invisible to a screen reader and to ctrl-F. The table is the
same data in a form that always works, and because both come from one source they cannot disagree.
Where coverage differs the **table is complete**: the images draw only cross-area prerequisites that
two or more topics in the view share, because drawing every one-off dependency laid one view out at a
6:1 aspect ratio that was illegible at any size.

**Why the generated Mermaid avoids `<b>` and quotes every label.** The hand-written version used
`<b>` for emphasis, which works only while Mermaid's `htmlLabels` are enabled — verified by rendering
with them off, where the emphasis silently disappears. `classDef` carries the distinction instead, and
no colours are hard-coded, so one source renders correctly in both themes. `<br/>` is safe either way
because Mermaid converts it to `tspan`s regardless of that setting.

---

## `render_diagrams.sh`

Stage 2: renders each `.mmd` to a light and a dark SVG.

```bash
tools/render_diagrams.sh          # all views
tools/render_diagrams.sh spine    # one view, by id
```

Reuses a preinstalled Chromium when it finds one (`PUPPETEER_EXECUTABLE_PATH`, `/opt/pw-browsers`,
or a `chromium`/`google-chrome` on `PATH`) rather than downloading another.

### How the freshness check works without a browser

Node and Chromium are too heavy a dependency to add to CI for a repository whose tooling story is
otherwise "one file, one dependency". So the two stages are linked by a checksum instead:

```text
generate_diagrams.py  →  writes .mmd, records sha256(.mmd) in diagrams/manifest.yml
render_diagrams.sh    →  stamps that same sha into the SVG as an XML comment
--check               →  regenerates .mmd in memory, compares to the committed .mmd,
                         and compares each SVG's stamp to the current sha
```

That catches all three ways a diagram can go stale — graph changed, `.mmd` not regenerated, SVG not
re-rendered — using only Python. The error message names the command that fixes it.

