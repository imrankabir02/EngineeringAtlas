# Templates

Copy-paste starting points. Each is kept in sync with the normative schema in
[graph-schema.md](../docs/graph-schema.md) — if you change a template's structure, change the schema
and the validator in the same pull request.

| Template | Copy to | For |
|---|---|---|
| [`topic/`](topic/) | `topics/<domain>/<topic-id>/` | A new written topic. All nine files plus `topic.yml` |
| [`project/`](project/) | `projects/<project-id>/` | A new project specification |
| [`path/`](path/) | `paths/<path-id>.{yml,md}` | A new learning path |
| [`resource-list.md`](resource-list.md) | into a topic's `resources.md` | The tiering and `why` conventions, with worked examples |
| [`progress.yml`](progress.yml) | your own fork or private repo | Tracking your own progress with evidence |

---

## Using the topic template

```bash
cp -r templates/topic topics/backend/message-queues-and-streaming
```

Then:

1. Fill in `topic.yml` first. It is the source of truth, and writing it forces the decisions the
   prose will have to be consistent with — especially the concept depths and the gates.
2. Update the registry entry: `status: planned` → `published`, add `dir`, and **move**
   `prerequisites` out of the registry into `topic.yml`, adding a `why` to each.
3. Write the nine Markdown files. Suggested order: `fundamentals.md`, `concepts.md`, `practical.md`,
   then `README.md` last — the README is a signpost, and it is much easier to write once you know
   what it points at.
4. Delete every instruction comment from the template. They are marked
   `<!-- AUTHOR: ... -->` in Markdown and `# AUTHOR:` in YAML.
5. Run `python3 tools/validate_graph.py`.

The validator will reject a published topic that is missing any of the nine files, or where any file
is under 400 characters or contains a placeholder marker such as `TODO` or `TBD`. **A file may be
short; it may not be a placeholder.** If a topic genuinely has nothing to say under a heading, say so
in a sentence and point to where the depth lives — see
[computer-basics/advanced.md](../topics/foundations/computer-basics/advanced.md) for an example of
doing this honestly.

---

## A note on links inside templates

Relative links in `topic/`, `project/`, and `path/` are written for the **destination** depth, not for
where the template lives. A link in `templates/topic/resources.md` reads
`../../../docs/resource-tiers.md`, which is correct once the file sits at
`topics/<domain>/<topic-id>/` and is broken where it currently is.

That is deliberate: it means you do not have to fix link depths after copying. The validator skips
these three directories for link resolution and says why. `templates/README.md` and
`templates/resource-list.md` are not copied anywhere, so their links are checked normally.

---

## The hardest fields to get right

From reviewing what goes wrong most often.

**`concepts[].depth`** — most concepts in most topics should be `working`. A topic with everything
marked `deep` has not made a judgment call and will be rejected: telling a learner what they can
safely skim is as valuable as telling them what to master. The `aware` markings are usually the most
useful ones in the file.

**`gates`** — every gate must be an *action with an observable outcome*. "Understand caching" is not a
gate. "Send 500 concurrent requests for the same cold key and measure how many reach the origin" is.
If you cannot tell whether someone passed it, it is not a gate.

**`prerequisites[].why`** — writing this down usually reveals that one of your prerequisites was not
actually required, or that one was missing. Do not skip it; it is the field that keeps the graph
honest.

**`first_principles_chain`** — each step must be a *problem* that the next step answers. If your chain
reads as a list of subtopics, it is a table of contents rather than a derivation. Compare
[caching's chain](../topics/backend/caching/topic.yml).

**`resources[].why`** — answers *why this instead of the twenty alternatives*, not what the resource
is. See [resource-list.md](resource-list.md) for the difference, worked.

**`effort`** — give a range with stated assumptions. A single number implies a precision that does not
exist; individual variation at Level 1 is a factor of five.

---

## Style

Read [style-guide.md](../docs/style-guide.md) before writing prose. The conventions that matter most:

- Wrap prose at 80 characters so diffs are reviewable line by line.
- Sentence case headings.
- Relative links only, and they are checked in CI.
- No motivational filler, no hype, no timeline promises.
- Explain hard concepts in three passes: the problem in plain words, then the mechanism with correct
  terminology, then the edge cases and costs.

The last one is the single most useful writing technique in this repository, because it serves a
beginner and an experienced engineer with the same file.
