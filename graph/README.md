# The learning graph

This directory is the machine-readable map: which topics exist, how they depend on each other, and
what level each sits at.

**The graph is data. The Markdown is prose.** That separation is the central architectural decision
of the repository — prose-only prerequisite claims are unenforceable and therefore always rot, while
a graph in YAML can be validated in CI. See
[architecture.md §3](../docs/architecture.md#3-the-graph-is-data-markdown-is-prose).

---

## Files

| File | Contains |
|---|---|
| [`domains.yml`](domains.yml) | The storage shelves. A flat, deliberately boring list |
| [`levels.yml`](levels.yml) | The six levels, with the "you are here when" test for each |
| [`registry/<domain>.yml`](registry/) | The node manifest: every topic in the map, one file per domain |
| [`dependency-map.md`](dependency-map.md) | The graph rendered for humans, with the first-principles chains |

Prerequisites for **written** topics live in their own `topics/<domain>/<id>/topic.yml`, not here.
The registry carries provisional prerequisites only for `planned` nodes, which have no `topic.yml`
to hold them. That asymmetry is deliberate and enforced — a written topic has exactly one source of
truth. See
[architecture.md §4](../docs/architecture.md#where-prerequisites-live-for-planned-nodes).

---

## Node statuses

| Status | Meaning | Directory exists? |
|---|---|---|
| `published` | Written to the quality standard, reviewed | **Yes**, with all nine files |
| `drafting` | Actively being written; content may be incomplete | Yes |
| `planned` | Declared in the map, not yet written | **No** |

This is how the map is complete while the repository contains **zero empty files**. A `planned`
node tells you the topic exists, its level, and where it sits in the dependency order — which is most
of what a map is for — without pretending to teach it.

The validator enforces the invariant in both directions: a `published` node without a directory
fails, and a `planned` node *with* a directory fails.

Most nodes are `planned`. That is the honest state of a project of this scope, and it is visible
rather than hidden behind stubs.

---

## Querying it

```bash
python3 tools/validate_graph.py --stats
```

Reports node counts by level, status and domain; total hard edges; entry points (topics with no
prerequisites); and the topics with the deepest transitive prerequisite trees.

For anything more specific, the files are small enough to read and regular enough to parse:

```python
import yaml, pathlib

nodes = {}
for f in pathlib.Path("graph/registry").glob("*.yml"):
    data = yaml.safe_load(f.read_text())
    for t in data["topics"]:
        nodes[t["id"]] = {**t, "domain": data["domain"]}

# every Level 3 topic that is written
print([n for n in nodes.values() if n["level"] == 3 and n["status"] == "published"])
```

---

## Adding a topic to the map

Adding a *node* is much cheaper than writing a topic, and it is a genuinely useful contribution on
its own — it makes a gap visible and gives the map somewhere to point.

1. Pick the domain whose file it belongs in. If you cannot decide, **the choice does not matter** —
   domains are storage, not meaning, and moving a topic later is a non-breaking operation.
2. Add an entry with `id`, `title`, `level`, `status: planned`, `summary`, and provisional
   `prerequisites`.
3. Choose the level from the "you are here when" tests in [`levels.yml`](levels.yml), not by how
   hard the topic feels.
4. Run `python3 tools/validate_graph.py`.

The validator will reject: a duplicate ID, an unknown domain, a prerequisite that does not exist, a
cycle, and a hard prerequisite at a higher level than the topic requiring it. That last check catches
a large class of ordering mistakes automatically, and it is worth reading the error carefully rather
than working around it — a level inversion usually means either the level or the dependency is wrong.

### Choosing an ID

IDs are permanent. Renaming one breaks every reference, so choose for the long term:

- **Name the concept, not the product.** `caching`, not `redis`. `containers-and-docker` is
  acceptable because Docker is load-bearing history.
- **Do not encode level or domain.** Both are fields, and both can change.
- **No version numbers.** `kubernetes`, never `kubernetes-1-29`.

### Writing the summary

One to three sentences saying what it is *and why it matters*. This is what a learner reads when
deciding whether the topic is their gap, so it has to discriminate.

Weak: *"Covers the fundamentals of message queues."*

Strong: *"Decoupling producers from consumers durably: brokers versus logs, ordering guarantees,
at-least-once delivery and why exactly-once is mostly marketing, dead-letter queues, and replay."*

The second one tells a reader whether it answers their question. The first does not.

---

## Promoting a topic to written

When you write a topic, its registry entry changes:

```diff
   - id: message-queues-and-streaming
     level: 3
-    status: planned
+    status: published
+    dir: topics/backend/message-queues-and-streaming
     summary: >
       ...
-    prerequisites:
-      hard: [background-jobs-and-queues, distributed-systems-fundamentals]
```

The `prerequisites` block **moves into** the new `topic.yml`, gaining a `why` for each entry. That
is a deliberate, reviewable step: writing down *why* a prerequisite is required usually reveals that
one of them was not, or that another was missing.

Then create the directory with all nine standard files and `topic.yml`. Full checklist:
[CONTRIBUTING.md](../CONTRIBUTING.md).

---

## What the graph deliberately cannot express

Worth stating, because people try.

**Experience.** Level 4 and 5 competencies require having been accountable for something, having
survived an incident, having been wrong and lived with it. No edge encodes that, which is why
`technical-leadership` has only two prerequisites despite being the hardest topic in the map.

**Time.** Effort estimates live in `topic.yml` as `focused_hours` with stated assumptions, not as
edge weights. Individual variation is large enough that a weighted graph would imply a precision
that does not exist.

**Partial prerequisites.** "You need the first third of `sql`" is not representable, and adding
partial-dependency semantics would make the graph unreadable for a marginal gain. Where it matters,
the dependent topic's prerequisite `why` says which part.

**Alternative routes.** There is often more than one order that works. The graph encodes the
constraint (A before B) rather than a route; [`paths/`](../paths/) encode routes, and several paths
can traverse the same subgraph differently.
