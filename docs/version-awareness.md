# Version Awareness

Technology changes; the problems it solves change far more slowly. A curriculum
that mixes the two ages badly and then misleads people, which is worse than being
merely out of date.

The countermeasure is structural: **separate the three layers, and keep them in
different files.**

---

## The three layers

```
Fundamental concept          Lifespan: decades.       Where: fundamentals.md, concepts.md
        ↓
Current implementation       Lifespan: years.         Where: practical.md
        ↓
Version-specific knowledge   Lifespan: months.        Where: practical.md, clearly marked
```

### Layer 1 — Fundamental concept

The problem, why it is hard, and the shape of any solution to it.

> A cache is a second copy of data placed closer to its reader. It trades memory
> and the risk of staleness for latency. Every cache must answer: what to keep,
> when to discard it, and what to do when it is wrong.

This is true of CPU caches, page caches, HTTP caches, ORM identity maps, DNS
resolvers, and Redis. It was true in 1965 and will be true in 2065. It is the
layer that transfers.

### Layer 2 — Current implementation

How a specific well-established technology embodies the concept. Stable over a
few years; occasionally invalidated by a major release.

> Redis is single-threaded for command execution, which makes individual commands
> atomic. It supports several eviction policies selected by `maxmemory-policy`.
> Persistence is via periodic snapshots (RDB), an append-only command log (AOF),
> or both.

### Layer 3 — Version-specific knowledge

Flags, defaults, API signatures, deprecations, minimum versions. Correct today,
possibly wrong next quarter.

> As of Redis 7, `maxmemory-policy` defaults to `noeviction`, and functions
> (`FUNCTION LOAD`) supersede the older `EVAL` script-caching workflow for
> persistent server-side logic.

Layer 3 content must be **marked with the version it was verified against**.

---

## Rules for authors

1. **Never state a version-specific fact in `fundamentals.md` or `concepts.md`.**
   Those files must remain correct if every tool named in the topic were replaced.

2. **Mark version-specific claims inline:**

   > *Verified against Redis 7.2 (2026-08).* The default `maxmemory-policy` is
   > `noeviction`, which means writes fail rather than evicting once the limit is
   > reached.

   A reader in two years then knows exactly how much to trust the sentence.

3. **Prefer canonical documentation URLs** over versioned ones, so links follow
   the current release rather than freezing.

4. **Do not paste command output or code that will drift.** Describe what to look
   for. `docker ps` output format is not curriculum; "confirm the container is in
   the running state and note the port mapping" is.

5. **Set `version_sensitivity` in `topic.yml`:**

   | Value | Meaning | Review cadence | Examples |
   |---|---|---|---|
   | `low` | Concepts dominate; implementations named illustratively | Every 2 years | `data-structures`, `caching`, `transactions-and-isolation` |
   | `medium` | Specific tools named, with commands and configuration | Annually | `containers-and-docker`, `ci-cd`, `sql` |
   | `high` | Fast-moving ecosystem; concrete guidance dates quickly | Every 6 months | `kubernetes`, `frontend-frameworks`, `llm-engineering`, `cloud-fundamentals` |

6. **Update `last_reviewed` when you verify content,** even if nothing changed.
   "Checked, still correct" is valuable information; a stale date is a warning.

---

## Applying it to a fast-moving topic

Frontend frameworks are the hard case: high churn, strong opinions, and a large
audience of beginners who will be told the ecosystem's current preference is a
permanent truth.

The topic should be organised so that ~80% of it survives the next framework:

**Layer 1 — durable** (`fundamentals.md`)

- Why manual DOM manipulation does not scale: state and view drift apart, and
  nothing forces them back into agreement.
- The core idea: describe the UI as a function of state; let something else
  compute the change.
- The costs that idea creates: reconciliation work, identity of list items, and
  the question of where state lives.
- Client-side vs server-side rendering as a trade between time-to-first-byte,
  interactivity, SEO, and infrastructure complexity — a trade that predates
  every current framework and will outlive them.

**Layer 2 — multi-year** (`practical.md`)

- React's model: components, one-way data flow, hooks, and the reason a
  dependency array exists.
- What the alternatives chose differently: Svelte compiles away the runtime; Vue
  uses fine-grained reactivity; Solid uses signals without a virtual DOM. Each
  is a different answer to the same reconciliation cost.

**Layer 3 — dated and quarantined** (`practical.md`, marked)

- *Verified against React 19 (2026-08).* Specific API guidance, current
  recommended router, current build tooling.

A learner who reads only Layer 1 can pick up any framework. A learner who reads
only Layer 3 must relearn everything on the next major release. Ordering the file
this way makes the durable material unavoidable and the disposable material
clearly labelled.

---

## Reviewing for rot

The scheduled maintenance job (see [ROADMAP.md](../ROADMAP.md)) surfaces:

- topics whose `last_reviewed` exceeds their review cadence
- external URLs returning errors or redirects
- topics with `version_sensitivity: high` and no dated markers, which is almost
  always an authoring error

Rot is normal and expected. A repository that claims never to need review is
either brand new or unmaintained.
