# Software engineering, beginner to advanced

**Level 0 → Level 4** · roughly 2–4 years part-time · nothing assumed

Machine-readable steps: [`software-engineering-core.yml`](software-engineering-core.yml)

**This is the spine of the repository.** It assumes no background and ends at the point where you
can be accountable for a production system. Every other path is either a slice of this one or a
specialisation branching off it.

---

## Who this is for

Anyone going from no technical background to being trusted with a real system. Also anyone already
partway who wants to find their gaps — take the level tests in
[levels.md](../docs/levels.md) and start at the phase that matches.

The path ends here:

> You have designed a system others built that survived a failure you predicted, led or materially
> contributed to an incident response that produced real changes, and can state the money,
> complexity, and operational cost of your architectural choices.

That is Level 4. Beyond it, see [the guru definition](../docs/levels.md#level-5--guru) — it is
deliberately not another list of topics, because guru is not reached by studying guru material.

---

## Read this before starting

**Two to four years is the honest range**, part-time. Nine to eighteen months full-time. If that
number is discouraging, note that it is the range in which people become genuinely, durably good at
this — and that every shorter claim you have seen is either about a narrower goal or is not true.

**The middle is the longest part.** Phase 4 (Level 3) is the largest phase and the slowest, because
progress there is measured in systems shipped and failures survived rather than topics read. That is
not a plateau; it is what the level consists of.

**You will not follow this exactly, and that is fine.** Skip topics when you have reason to — and
**write down what you skipped**. Every hard prerequisite here exists because its absence causes a
specific later failure, and knowing which one you deferred turns three days of confusion into ten
minutes.

**Milestones are the load-bearing part of the structure.** Sixty topics listed in order would tell
you nothing about readiness. The five milestones are stated as capabilities with evidence. When you
reach one, verify it honestly; if you cannot pass it, the phase is not finished regardless of what
you have read.

---

## Phase 1 — the machine stops being magic

**Level 0 · 7 topics · ~40 hours · 5–6 weeks**

`computer-basics` → `operating-system-basics` → `files-and-directories` →
`command-line-basics` → `internet-basics` → `what-programming-is` → `problem-solving-basics`

No code. Four to six weeks before you write a line, and skipping it is the most common reason
people stall three months later.

The carrying step is [`computer-basics`](../topics/foundations/computer-basics/README.md) and its
[project](../projects/machine-anatomy/README.md), where you measure your own machine and **write
every prediction down before measuring.** That habit is the real deliverable, and it reappears
unchanged at Level 5 as experiment design.

**Milestone.** You can operate a computer deliberately rather than by memorised clicks, and explain
the memory-versus-disk difference using numbers you measured.

---

## Phase 2 — you can make a computer do something

**Level 1 · 7 topics · ~230 hours · 7–8 months**

`programming-fundamentals` → `debugging-fundamentals` → `error-handling` →
`version-control-git` → `linux-fundamentals` → `networking-fundamentals` →
`databases-introduction`

[`programming-fundamentals`](../topics/programming/programming-fundamentals/README.md) is 120 of
those hours and the longest single topic in the repository. One language. Both projects, from a
blank file.

The four topics after it are chosen to remove permanent sources of mystery rather than to add
capability:

- `debugging-fundamentals` — the topic that most determines your pace for the next two years.
- `linux-fundamentals` — almost all servers run Linux. Without this, the environment stays magic.
- `networking-fundamentals` — what "connection refused" versus "timeout" tells you about *where*
  the failure is. You will use this weekly for the rest of your career.
- `databases-introduction` — why a file is not enough, before any query language.

**Milestone.** You can write and debug a 300-line program unaided, use Git without fear, navigate a
Linux server over SSH, and explain why a network request failed. **Level 1.**

---

## Phase 3 — you can build a correct application

**Level 2 · 20 topics · ~600 hours · 12–18 months**

This is where "programmer" becomes "software engineer". The concerns change from *does it run* to
*is it correct, readable, testable, and changeable*.

Four groups, roughly in order:

**Cost and structure** — `object-oriented-programming`, `functional-programming`,
[`data-structures`](../topics/computer-science/data-structures/README.md), `complexity-analysis`,
`algorithms`.

The data-structures project is where theory and measurement first openly disagree — identical
complexity, 20× different speed. That discovery is the beginning of engineering judgment.

**Data** — `sql`, `relational-modeling`.

Learn the relational model *as a model*, not as syntax. Write SQL by hand before using an ORM: if
you cannot read the query the ORM generated, you cannot debug it, and you will need to.

**The web** — `http`, `rest-apis`, `tls-and-cryptography-basics`,
`authentication-and-authorization`, `backend-development`.

`http` before any framework. Read the RFC sections rather than a tutorial — every framework is a
thin layer over these semantics, and knowing the semantics is what transfers.
`authentication-and-authorization` is two different problems in one topic, and every mistake in it
is a real vulnerability, which is why the advice is to use the framework's implementation.

**Working with other people** — `testing-fundamentals`, `package-management`, `clean-code`,
`git-workflows`, `code-review`, `software-design-principles`, plus `linux-administration` and
`security-fundamentals`.

`code-review` deserves emphasis: reviewing code you did not write is a different skill from writing
it, and it is the one that becomes judgment. Practise on real open-source pull requests — read the
diff, write your comments, *then* read the maintainers' discussion.

**Milestone.** You have designed, built, tested and deployed an application with a database, an API
and authentication. You can review a peer's pull request for design, and explain what happens
between typing a URL and rendering a response through your own stack. **Level 2.**

---

## Phase 4 — your system survives reality

**Level 3 · 23 topics · ~900 hours · 12–24 months**

The largest phase, the slowest, and the one that changes how you think. The defining shift: **you
begin reasoning about what happens when things go wrong**, not only about the happy path.

**Underneath your program** — `operating-systems-fundamentals`, `processes-and-scheduling`,
`memory-management`.

`operating-systems-fundamentals` explains most surprising performance. Learn to read `top`,
`strace`, and `/proc` as evidence rather than noise.

**More than one thing at a time** — `concurrency-and-parallelism`, `async-programming`.

Produce a race condition **on purpose** before trusting any concurrent code you write. Reading
about races does not prepare you; causing one does.

**Data under pressure** — `transactions-and-isolation`, `indexing-and-query-optimization`.

Check what your database's default isolation level actually is. It is rarely what you assumed, and
the anomalies each level permits are the difference between correct and nearly-correct.

**Making it fast, and the cost of doing so** — [`caching`](../topics/backend/caching/README.md).

The cheapest place to learn that **adding a component adds a failure mode.** Cause a stampede and
a stale read yourself. Every topic after this one has the same shape.

**Shipping and running it** — `containers-and-docker`, `ci-cd`, `observability`,
`cloud-fundamentals`, `infrastructure-as-code`.

`observability` is how you debug a system you cannot attach a debugger to. Alert on symptoms, not
causes.

**More than one machine** — `distributed-systems-fundamentals`, `background-jobs-and-queues`,
`message-queues-and-streaming`.

`distributed-systems-fundamentals` reframes everything before it. Partial failure, and the
impossibility of distinguishing slow from dead, are not edge cases — they are the environment.

**Keeping it changeable** — `refactoring`, `test-strategy`, `application-security`, `api-design`,
`software-architecture`, `system-design-fundamentals`.

The phase ends with `system-design-fundamentals`: draw a diagram where you can justify every box.
If you cannot, you have copied an architecture rather than designed one.

**Milestone.** You have run something in production or an honest simulation of it, diagnosed a
performance problem with a profiler rather than a guess, and deliberately broken your own system and
fixed what that exposed. **Level 3 — this is where most professional engineers work, and it is a
good place to be.**

---

## Phase 5 — you can be accountable for a system

**Level 4 · 13 topics · ~700 hours · 12–24 months, mostly on the job**

The work is now as much about constraints, organisations, and economics as about code.

`performance-engineering` → `fault-tolerance` → `replication-and-consistency` →
`partitioning-and-sharding` → `sre-and-reliability` → `incident-response` →
`capacity-planning` → `cost-optimization` → `large-scale-system-design` → `microservices` →
`kubernetes` → `reading-source-code` → `open-source-engineering`

Four notes on this phase specifically:

**`performance-engineering` first**, because everything else in the phase is measured. Percentiles,
coordinated omission, Little's Law. Predict every number before you measure it.

**`sre-and-reliability` has an uncomfortable implication**: change is the dominant cause of
outages. Sitting with that honestly affects how you ship, and most teams avoid the conclusion.

**`microservices` is here so you can say when it is wrong.** Most systems should remain a modular
monolith. Learning the technique in order to decline it is a legitimate and underrated reason to
learn something.

**`reading-source-code` and `open-source-engineering` are the bridge to Level 5.** They are where
you stop depending on documentation existing, which is the precondition for working where no
guidance exists.

**Milestone.** You have designed a system others built that survived a failure you predicted, led or
materially contributed to an incident response that produced real changes, and can state the money,
complexity, and operational cost of your architectural choices. **Level 4.**

---

## Honest effort estimate

| Phase | Topics | Focused hours | Calendar at ~10 h/week |
|---|---|---|---|
| 1 — machine (L0) | 7 | ~40 | 1 month |
| 2 — programs (L1) | 7 | ~230 | 6 months |
| 3 — applications (L2) | 20 | ~600 | 14 months |
| 4 — systems (L3) | 23 | ~900 | 21 months |
| 5 — accountability (L4) | 13 | ~700 | 16 months |
| **Total** | **70** | **~2,470** | **~4.7 years** |

At 20 hours a week that is roughly 2.4 years. Full-time and immersed, with a job that provides
phases 4 and 5 as work rather than study, 18 months to two years is realistic.

**Phases 4 and 5 substantially overlap with employment.** You cannot learn incident response
without incidents, or capacity planning without capacity to plan. Getting a job at Level 2 and
learning phases 4–5 on it is the normal and correct route, and it changes the calendar considerably.

---

## Where people stall, by phase

**Phase 1:** impatience — it does not feel like real programming. Do the project; it is concrete.

**Phase 2:** the week-three wall in `programming-fundamentals`, where tutorials stop being enough.
Nearly universal. Do the exercises before the projects so mechanics are automatic.

**Phase 3:** the largest attrition point, for two reasons. First, this phase has 20 topics and no
single dramatic capability jump, so progress feels slow. Second, it is where people are tempted to
jump to a framework and skip the foundations — which works until it does not, and then it is
unrecoverable. Keep one real application throughout and apply each topic to it.

**Phase 4:** trying to learn operations without operating anything. There is a limit to how far
reading gets you here. Deploy something real, even something small, and break it deliberately. A
single VM you are responsible for teaches more than a year of reading about Kubernetes.

**Phase 5:** waiting for permission. Accountability is usually taken rather than granted. Volunteer
for the on-call rotation, write the design doc nobody asked for, run the post-mortem.

---

## Related paths

| Path | Relationship |
|---|---|
| [Absolute beginner](absolute-beginner.md) | Phases 1–2 of this path, on its own |
| [Programming foundations](programming-foundations.md) | The engineering-practice subset of phase 3, in more depth |
| [Computer science foundations](computer-science-foundations.md) | The theory subset of phase 3, extended to Level 4 |
| [Python backend](stacks/python-backend.md) | This path with Python-specific emphasis, and a narrower scope |

Roughly 80% of a stack path's steps are topics from this path. That is not a coincidence and it is
the intended lesson: what transfers between stacks is most of it.
