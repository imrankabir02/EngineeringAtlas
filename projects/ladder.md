# The project ladder

Every project on the ladder exists for a reason, stated here. Projects with links have
full specifications; the rest are planned, and their entries here are the design brief
a contributor would work from.

The ladder is not a checklist to complete. Pick the projects that validate the topics
you are actually learning. Four finished projects across four levels beat twenty
started.

---

## Level 0 — the machine stops being magic

| Project | Validates | Why it exists |
|---|---|---|
| [Anatomy of your own machine](machine-anatomy/README.md) | `computer-basics` | Produces first-hand numbers for the memory/disk gap. Every later performance claim rests on these |
| Manual data organiser | `files-and-directories` | Reorganise 200 files by hand, time it, then estimate the same for 20,000. The felt need for automation is the prerequisite for wanting to program |
| Trace a page load | `internet-basics` | Follow one request from URL to rendered page using browser devtools. Establishes that the web is machines sending messages |

---

## Level 1 — you can make a computer do something you decided

| Project | Validates | Why it exists |
|---|---|---|
| [Expression calculator](cli-calculator/README.md) | `programming-fundamentals` | Precedence forces representing structure, not scanning text. Recursion becomes necessary rather than decorative |
| [File organiser](file-organizer/README.md) | `programming-fundamentals`, `error-handling` | First contact with a hostile external world where mistakes are permanent. Teaches plan-then-act and reversibility |
| Notes application (CLI) | `programming-fundamentals`, `files-and-directories` | Persistence without a database: serialisation formats, concurrent edits from two terminals, and what "saved" means |
| Log summariser | `programming-fundamentals` | Parse a real messy log file. Every line that does not match your assumption is a lesson about real data |
| Personal Git archaeology | `version-control-git` | Take an existing repository and answer questions about it using `log`, `blame`, and `bisect`. Git becomes an investigative tool rather than a save button |

---

## Level 2 — you can build a correct application with more than one moving part

| Project | Validates | Why it exists |
|---|---|---|
| [Data structures from scratch](ds-from-scratch/README.md) | `data-structures`, `complexity-analysis` | Invariants, and the gap between asymptotic prediction and measured speed |
| REST API with a database | `rest-apis`, `backend-development`, `sql` | The first system with layers. Where "it works on my machine" becomes insufficient |
| Authentication system | `authentication-and-authorization` | Password storage, sessions vs tokens, and the difference between the two words. Every mistake here is a real vulnerability |
| Blog platform | `backend-development`, `relational-modeling` | Schema design with real relationships: users, posts, comments, tags. Migrations on data you care about |
| Test suite for someone else's code | `testing-fundamentals`, `reading-source-code` | Write tests for an unfamiliar open-source project. Teaches reading code and what makes code testable |
| E-commerce backend | `backend-development`, `transactions-and-isolation` | Money makes correctness non-negotiable: inventory under concurrency, idempotent payments, and the first place a transaction is genuinely required |

---

## Level 3 — your system survives contact with reality

| Project | Validates | Why it exists |
|---|---|---|
| [In-memory cache](in-memory-cache/README.md) | `caching`, `concurrency-and-parallelism` | O(1) eviction, a race you can exhibit, and a stampede you caused |
| [URL shortener](url-shortener/README.md) | `caching`, `system-design-fundamentals` | Small enough to finish, and contains every problem of a read-heavy service including its saturation point |
| Distributed task queue | `background-jobs-and-queues`, `distributed-systems-fundamentals` | What happens to a job when a worker dies mid-execution. Forces idempotency, retries, backoff, and visibility timeouts |
| Real-time chat | `async-programming`, `event-driven-architecture` | Long-lived connections break every request/response assumption: presence, fan-out, ordering, and reconnection with missed messages |
| Search engine | `advanced-algorithms`, `indexing-and-query-optimization` | Build an inverted index and rank results. Tokenisation, stemming, and why exact matching is not what users want |
| Monitoring system | `observability` | Collect, store, and alert on metrics. Time-series storage, cardinality as a real cost, and alerts that fire on symptoms |
| Containerise and deploy something | `containers-and-docker`, `ci-cd` | Take a project you built and get it running reproducibly, deployed by a pipeline, with a tested rollback |

---

## Level 4 — you can be accountable for a system

Each of these reimplements infrastructure you normally consume. That is the point:
you cannot fully reason about a component you have never built a version of.

| Project | Validates | Why it exists |
|---|---|---|
| Distributed cache | `partitioning-and-sharding`, `caching` | Consistent hashing, node membership, and measuring key churn when a node leaves |
| Message broker | `message-queues-and-streaming`, `fault-tolerance` | Durable append-only storage, consumer offsets, and discovering why exactly-once delivery is not a thing you can simply implement |
| Mini database | `database-internals`, `transactions-and-isolation` | A storage engine with a B-tree or LSM tree, a write-ahead log, and crash recovery you test by actually killing the process |
| Load balancer | `network-performance`, `fault-tolerance` | Connection handling, balancing algorithms, health checks that do not lie, and behaviour when every backend is unhealthy |
| Distributed storage | `replication-and-consistency`, `consensus` | Replication with quorums, and reading the consistency guarantee off your own implementation rather than off a marketing page |
| Raft implementation | `consensus` | Leader election and log replication from the paper. The definitive way to stop treating consensus as magic |
| Production migration | `distributed-databases`, `sre-and-reliability` | Change a schema on a large table with no downtime: dual writes, backfill, verification, cutover, and a rollback plan |

---

## Level 5 — you work where no guidance exists

At Level 5 the project is not a *thing to build* from a list. The list would defeat the
purpose, because the defining property of guru-level work is that nobody handed you the
requirements.

A Level 5 project is characterised by properties rather than by subject:

**Architecture.** The design decisions are yours, they conflict, and you must document
what you sacrificed and what would change your mind.

**Scale.** Some dimension — traffic, data, connections, teams, years — is large enough
that the obvious approach fails.

**Failure handling.** You enumerated failure modes before building, and the system
degrades rather than collapsing.

**Performance.** You have a latency and throughput budget derived from requirements,
and measurements proving you meet it.

**Observability.** Someone else could debug it at 3 a.m. from its telemetry alone.

**Security.** There is a written threat model and the design reflects it.

**Benchmarking.** You produced numbers a sceptic could reproduce, with the setup
published.

**Real constraints.** Cost, deadlines, an existing system you cannot replace, a team
with mixed experience, or a compatibility requirement you cannot break.

Concrete shapes that usually satisfy these:

- **Contribute a substantial feature to a widely used open-source project.** Real
  reviewers, real standards, a codebase you did not design, and constraints you must
  discover rather than choose.
- **Reproduce a paper, then find its assumption.** Implement a published system,
  benchmark it honestly, and find the workload where its claims do not hold.
- **Design and lead a system others build.** The evidence is that it worked, including
  under a failure you predicted in advance.
- **Build the tool that does not exist.** Something you needed, could not find, and
  can evaluate honestly against the alternatives — including "do nothing".
- **Write the definitive analysis of a hard problem** in your domain: the trade-off
  space, the measurements, and the recommendation. Then be publicly wrong about part
  of it and correct it.

---

## Adding a project to the ladder

An entry here is a design brief, not a placeholder. Every planned project above states
what it validates and why it exists — if you cannot write that sentence, the project is
not ready to be on the ladder.

To promote a planned project to specified, copy
[`templates/project/`](../templates/project/) and follow
[CONTRIBUTING.md](../CONTRIBUTING.md). The bar is in
[projects/README.md](README.md#adding-a-project).
