# Gate library

Reusable challenges for the gate types that need more than a one-line instruction. Topics reference
these patterns; this file is where the method and the examples live.

[← Validation](README.md) · [Competency gates](../docs/competency-gates.md)

---

## Design challenges

A problem statement with constraints and no solution. Produce an architecture, then defend it.

**What makes a good one: the obvious answer is wrong, for a reason stated in the constraints.** The
trap is the teaching. Without it, a design challenge is an invitation to recite a standard
architecture.

### Rate limiter (L3–L4)

> Design a rate limiter for an API served by 2,000 nodes. Limits must be accurate to within 1%.
> Nodes may not share a database on the request path.

The obvious answer — a shared counter — violates the last constraint. Working around it teaches
distributed counting: local buckets with periodic reconciliation, or a sliding window in a shared
cache with the accuracy budget spent deliberately.

**Probe with:** *what happens during a network partition between a node and the counter store?*

### Feed with a celebrity problem (L4)

> Design a social feed. Most users have under 500 followers. A few have 50 million.

The obvious answer — fan-out on write — is correct for most users and catastrophic for the celebrity,
because one post produces 50 million writes. The lesson is that **a single strategy is wrong**, and
the answer is a hybrid: fan-out on write for normal accounts, fan-out on read for large ones, with a
threshold you have to justify.

**Probe with:** *where is the threshold, and what happens to a user who crosses it?*

### Scheduled jobs at scale (L3)

> Users schedule reminders at arbitrary future times. Millions of pending reminders. Each must fire
> within 5 seconds of its time, exactly once.

The obvious answer — poll a table every second for due rows — fails at scale on the index and on
contention. The lesson is time-bucketing, and *exactly once* forces the honest answer: at-least-once
delivery plus idempotent handling, because exactly-once firing is not achievable.

**Probe with:** *what happens if a worker dies after sending and before marking the row done?*

### Stock levels and caching (L3)

> A product page shows a description, a price, and a live stock level. Traffic is 20,000 requests
> per second. Stock changes constantly.

The obvious answer — cache the page — oversells. The lesson is that **staleness tolerance differs per
field**, so the page must be decomposed: description cached for hours, price for minutes, stock not
at all or for two seconds with the business cost stated explicitly.

**Probe with:** *what is the business cost of 60-second-stale stock, and who decided it was
acceptable?*

### Migration with no downtime (L4)

> Change the primary key type of a table with 4 billion rows, in a system with no maintenance
> window.

There is no obvious answer, which is the point. Expected shape: add the new column, dual-write,
backfill in batches with monitoring, verify equivalence, switch reads, switch writes, drop the old
column — with a rollback plan at every step.

**Probe with:** *at which step is rollback no longer possible, and how do you know the backfill is
correct?*

---

## Debugging challenges

A symptom, a system, no runbook. Sometimes a red herring.

**Run them out loud.** The value is in the narration — hypothesis, cheapest disproving observation,
narrowing — not in reaching the answer.

### The 14:00 latency tripling (L3)

> p99 latency tripled at 14:00 and has stayed there. Deploys were frozen. CPU, memory, and request
> volume are flat.

Plausible causes: a dependency's own p99 degraded; a bulk cache expiry (many entries written at
13:00 with a one-hour TTL); a scheduled job saturating disk I/O; connection pool exhaustion; a
routing or DNS change; a table crossing a size threshold that changed the query plan.

The flat request volume is the interesting clue — it rules out load and points at something whose
*cost per request* changed.

### The slow deploy that is not slow (L3)

> A new version is 30% slower in production. Identical in staging. Same container image.

Plausible causes: different data volume or shape; cold caches after restart; a config difference;
noisy neighbours; a connection pool sized for staging; a feature flag; a query whose plan differs
because production statistics differ.

The lesson is that **"same image" is not "same system"** — the environment is part of the program.

### Intermittent wrong values (L3)

> One user in a thousand sees another user's data. Not reproducible.

Plausible causes: a cache key omitting the user; a shared mutable object across requests; a
connection returned to the pool with state; a race in request-scoped storage; a CDN caching a
personalised response without `Vary`.

The one-in-a-thousand rate is the clue: it points at a race or a cache hit rather than a logic error,
because logic errors are deterministic.

### The disappearing message (L3–L4)

> A queue consumer processes 99.9% of messages. The rest vanish with no error logged.

Plausible causes: an exception swallowed by a catch-all; a visibility timeout expiring mid-processing
so the message is redelivered and then dead-lettered; messages exceeding a size limit; a poison
message killing the worker before it logs; acknowledgement before processing rather than after.

**The generalisable lesson:** *no error logged* is itself evidence — it points at a path where errors
are discarded, not at a path with no errors.

---

## Performance challenges

"Make this 10× faster" with a fixed workload and a required correctness test.

**The structure that makes them work:** you must predict where the time goes before profiling. The
lesson is almost always that you were wrong, and the value is in that specific wrongness.

Good targets, in increasing difficulty:

- **An endpoint with an N+1 query.** The fix is small; the lesson is that the profile pointed at the
  database and the cause was in the ORM.
- **A batch job that is I/O-bound and looks CPU-bound.** Teaches reading a profile correctly.
- **A hot loop over a scattered data structure.** Teaches that layout beats complexity.
- **A JSON API serialising more than it needs to.** Teaches that the work you do not do is the
  cheapest optimisation.
- **A service whose p99 is 40× its p50.** Teaches that tail latency has different causes from
  median latency — queueing, GC, cache misses, retries.

**Rules:** correctness test passes throughout; one change at a time; record the number after each
change. If a change made no difference, that is a finding and it goes in the writeup.

---

## Failure simulations

The cheapest judgment-building exercise that exists.

**The method:** pick a component. **Write down what you predict happens if it fails.** Then fail it.
Score your prediction.

That is the whole exercise, and its value is entirely in the written prediction — without it, you are
just breaking things.

| Failure to inject | What it usually reveals |
|---|---|
| Kill a dependency mid-operation | What state you left behind; whether you are idempotent |
| Fill the disk | Whether your error paths have ever executed |
| Add 500 ms latency to every outbound call | Which timeouts are wrong; whether retries stampede |
| Drop the cache entirely | Whether the system can serve real load at all |
| Send malformed and hostile input | Where your trust boundaries actually are |
| Clamp to one CPU, or halve memory | What your concurrency model silently assumed |
| Run two instances concurrently | Every race and every piece of unshared state |
| Set the clock forward, then backward | Every assumption that time is monotonic |
| Deliver a message twice | Whether at-least-once was handled or hoped about |
| Return an error from every write for 30 seconds | Whether the system recovers or requires a restart |

**Scoring your prediction:** exact match, right direction wrong magnitude, wrong mechanism, or
completely surprised. Track the distribution over time — it is the most direct measurement of your
own model quality available, and watching it improve is unusually motivating.

---

## Code review exercises

**The method:** find a real merged pull request in an open-source project. Read the diff. Write your
review comments. **Then** read the maintainers' discussion.

What they saw that you did not is the most direct measurement of judgment available to a
self-learner. Do it ten times and the gap is a curriculum.

Choose pull requests that:

- **changed behaviour**, not formatting or dependencies
- had **real discussion** — three or more substantive comments
- are in a codebase you can understand in an hour
- were **eventually revised**, so you can see what the review caught

Progression, roughly:

1. **Style and clarity** — what you can see without understanding the change.
2. **Correctness** — edge cases, error paths, off-by-ones.
3. **Design** — is this the right place for this logic; what does it couple.
4. **Failure modes** — what happens under concurrency, load, or partial failure.
5. **What is missing** — the test that was not written, the case not considered, the migration path.

Level 5 stops here. Level 2 reviews stop at 1.

---

## Research exercises

Read a paper. Answer four questions **in writing**:

1. **What is the contribution?** One sentence. Not the abstract, which is written to sell.
2. **What assumption makes it work?** Every result rests on one. Finding it is the skill.
3. **What does it cost?** Latency, complexity, memory, operational burden. Good papers say; most
   understate.
4. **Does it apply to a system you have built?** Why, or why not, specifically.

Good first papers, in order of accessibility:

| Paper | Why it is a good first one |
|---|---|
| *Scaling Memcache at Facebook* (NSDI 2013) | Every problem in it is one you caused in the caching project |
| *The Google File System* (2003) | Assumptions stated plainly; you can see the design following from them |
| *Dynamo* (2007) | The clearest exposition of choosing availability over consistency, and what it costs |
| *The Tail at Scale* (2013) | Short, and it changes how you think about latency permanently |
| *Raft: In Search of an Understandable Consensus Algorithm* (2014) | Written to be understood, and it says so |

Read the introduction, then the evaluation section, then the design. Skipping to the design is how
people get lost — the introduction says what problem exists, and without that the design is arbitrary.

---

## Using this library

**Do not work through it.** These are patterns to draw from when a topic's gates need substance, or
when you want to practise a specific kind of thinking.

**One good failure simulation is worth ten skimmed design challenges.** The prediction, the failure,
and the scored result are where judgment comes from; reading the scenarios is not.

**Adding to this library** is a valuable, low-barrier contribution. A design challenge needs a trap
and a probing follow-up; a debugging scenario needs at least four plausible causes and a clue that
narrows them. See [CONTRIBUTING.md](../CONTRIBUTING.md).
