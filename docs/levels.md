# Competency Levels

Six levels, `0` through `5`. Each is defined by **what you can do unaided**, not
by what you have been exposed to.

Two rules govern how they are used:

1. **A level is not a stage of life.** You will be L4 in one domain and L1 in
   another, permanently. A staff backend engineer can be L0 in embedded systems.
   That is normal and the map is built to support it.
2. **Levels are claimed with evidence, not felt.** Each level below has an
   explicit "you are here when" test. If you cannot do the test, you are not
   there yet, regardless of years of experience or job title.

| Level | Name | One-line test | Typical topic count |
|---|---|---|---|
| 0 | Absolute Beginner | Can operate a computer deliberately rather than by memorised clicks | 5–8 |
| 1 | Foundation | Can write a small program that solves a problem nobody handed you a template for | 10–15 |
| 2 | Intermediate | Can build and test a correct multi-component application | 20–30 |
| 3 | Advanced | Can build a system that survives real traffic, real failures, and real data | 30–50 |
| 4 | Expert | Can be accountable for a system: its scale, cost, reliability, and incidents | 30–50 |
| 5 | Guru | Can work correctly where no guidance exists, and raise the capability of others | open-ended |

---

## The four axes

Level answers "how far along". It does not answer "along what". Four axes, from
[philosophy.md](philosophy.md#knowledge--skill--judgment--mastery), progress
semi-independently:

| Axis | Question | Evidence |
|---|---|---|
| **Knowledge** | Can you state it correctly? | You can explain it to a peer without notes |
| **Skill** | Can you do it reliably? | You have done it repeatedly, including on unfamiliar code |
| **Judgment** | Can you decide well under uncertainty? | You have made the call, been wrong, and know why |
| **Mastery** | Can you extend the field? | You produced something that did not exist: an abstraction, a diagnosis nobody else had, a paper, a mentored engineer |

The common failure is an axis imbalance: high Knowledge, low Skill (tutorial
hell); high Skill, low Judgment (builds everything, chooses badly); high
Judgment, low Knowledge (opinionated, wrong about mechanisms).

Levels 0–2 are mostly Knowledge and Skill. Level 3 is where Judgment starts
mattering more than either. Levels 4–5 are dominated by Judgment and Mastery —
which is why "learn more technologies" stops working as a strategy around L3.

---

## Level 0 — Absolute Beginner

**Goal: the computer stops being magic.**

You are here when you have never seriously studied technology. You may use
computers daily; that is not the same thing.

### What you learn

- **How a computer works** — CPU, memory, storage, I/O; what "running a program"
  physically means; why memory is fast and disks are slow.
- **Hardware vs software** — what is physical, what is instructions, and why the
  distinction matters.
- **Operating systems** — what an OS does for you: processes, memory, files,
  devices; why programs cannot see each other's memory.
- **Files and directories** — paths, absolute vs relative, extensions as a
  convention rather than a fact, text vs binary.
- **The command line** — navigating, running programs, arguments, input/output,
  redirection. The point is not speed; it is that the CLI shows you what is
  actually happening.
- **Internet basics** — client/server, what a URL is, roughly what happens when
  you open a page.
- **What programming is** — instructions, sequence, state; a program as a
  precise description of a process.
- **Programming languages** — why more than one exists; compiled vs interpreted;
  what a language chooses to make easy.
- **Basic problem solving** — decomposition, following a procedure exactly,
  noticing your assumptions. Practise this away from a keyboard too.

### You are here (and ready to leave) when

- You can navigate a filesystem, create/move/delete files, and run a program
  from a terminal without a GUI.
- You can explain, to someone else, the difference between RAM and disk and why
  it matters.
- Given a task like "rename 200 files consistently", you know it is automatable,
  even if you cannot yet automate it.
- You can read an error message and identify *which part* is the message, the
  location, and the noise.

### Anti-goal

Do not start a framework. Do not start "web development". You will succeed at
copying and learn nothing.

---

## Level 1 — Foundation

**Goal: you can make a computer do something you decided.**

### What you learn

- **Programming fundamentals** — values and types, variables and binding,
  expressions vs statements, conditions, loops, functions, scope, collections,
  mutability, modules.
- **Error handling** — errors as expected outcomes; exceptions vs return values;
  failing loudly vs silently.
- **Debugging** — reading stack traces, forming a hypothesis, bisecting,
  printing vs stepping in a debugger. This is a *skill*, and it is the one that
  most determines your pace for the next two levels.
- **Git basics** — commit, branch, merge, remote; what a commit actually is.
- **Basic Linux** — the filesystem hierarchy, permissions, processes, pipes,
  package managers, editing files over SSH.
- **Basic networking** — IP, ports, DNS, what "localhost:8000" means, why a
  request fails.
- **Basic databases** — persistence, tables, rows, why a file is not enough.

### Language choice

Learn **one** language properly first. Which one matters much less than
finishing. The three defensible starting points:

| Language | Why it exists | Best first if | Cost of starting here |
|---|---|---|---|
| **Python** | Readability and breadth; batteries included | You want the shortest path from idea to working program; you are aimed at backend, data, or ML | Hides memory, types, and concurrency — you must learn them later, deliberately |
| **JavaScript** | The browser needed a scripting language; then it escaped | You are aimed at frontend or full-stack, and want your work visible immediately | Historical inconsistencies and a large, churning toolchain add noise while you are learning to think |
| **C** | A portable abstraction over the machine | You want to understand the machine, or are aimed at systems/embedded | Slowest to a working program; you will spend real time on memory before writing anything interesting |

Recommendation for most people: **Python** first, then a second language chosen
to be *different* (C for the machine, JavaScript for the browser, Go for
concurrency, a Lisp or Haskell for a genuinely different model). The second
language is where you learn what was the language and what was programming.

### You are here (and ready to leave) when

- You can write a 200–500 line program from a blank file that solves a real
  problem you have, without following a tutorial.
- When it breaks, you diagnose it yourself, and you can describe the bug's cause
  in one sentence.
- You can use Git for your own work without fear, and explain what a branch is.
- You can read a small program written by someone else and predict its output.

### Anti-goal

Do not learn three languages at 20%. Do not start a web framework until you can
write and debug programs unaided.

---

## Level 2 — Intermediate

**Goal: you can build a correct application with more than one moving part.**

This is where "programmer" becomes "software engineer": the concerns shift from
*does it run* to *is it correct, readable, testable, and changeable*.

### What you learn

- **Object-oriented programming** — encapsulation, composition over inheritance,
  interfaces, why deep hierarchies fail.
- **Functional programming concepts** — purity, immutability, higher-order
  functions, why these make code testable. You do not need a functional
  language; you need the ideas.
- **Data structures** — arrays, linked lists, hash tables, trees, heaps, graphs:
  the memory layout, the trade-offs, and when each is the wrong choice.
- **Algorithms and complexity** — sorting, searching, traversal, recursion; Big-O
  as a tool for prediction, and its limits (constants and cache behaviour are
  real).
- **SQL and relational modelling** — joins, aggregation, normalisation,
  constraints, keys; the relational model as a *model*, not as syntax.
- **HTTP** — methods, status codes, headers, statelessness, caching semantics.
- **REST APIs** — resources, representations, idempotency, versioning, errors.
- **Authentication and authorisation** — sessions vs tokens, password storage,
  OAuth's shape, and the difference between the two words.
- **Testing** — unit/integration/end-to-end, what makes a test valuable, test
  doubles, and why chasing coverage percentages misleads.
- **Git workflows** — rebase vs merge, pull requests, code review, resolving
  conflicts without panic.
- **Package management** — dependencies, version constraints, lockfiles, and
  supply-chain risk.
- **Clean code and design principles** — naming, cohesion, coupling,
  SOLID-as-heuristics, when to abstract and when abstraction is premature.
- **Basic architecture** — layering, boundaries, dependency direction.

### You are here (and ready to leave) when

- You have built and deployed an application with a database, an API, and
  authentication — designed by you, not scaffolded from a tutorial.
- It has tests you actually rely on when refactoring.
- You can write a SQL query with multiple joins and aggregation, and explain
  what it does to someone else.
- You can review a peer's pull request and produce comments about design, not
  only style.
- You can explain what happens between typing a URL and rendering a response,
  through your own stack.

### Anti-goal

Do not skip data structures because your language provides them. Do not skip
testing because it feels slow. Both bills come due at L3, with interest.

---

## Level 3 — Advanced

**Goal: your system survives contact with reality — concurrent users, real data
volumes, partial failures, and time.**

The defining shift: **you begin reasoning about what happens when things go
wrong**, not only about the happy path. Judgment becomes the dominant axis.

### What you learn

- **Concurrency and parallelism** — threads, processes, async/event loops; race
  conditions, deadlock, locks, atomicity; why "just add threads" is not a plan.
- **Async programming** — non-blocking I/O, what an event loop actually does,
  backpressure, and why blocking calls poison async code.
- **Operating systems in earnest** — scheduling, virtual memory, page cache,
  syscalls, file descriptors, signals; how to read `top`, `strace`, and `/proc`.
- **Networking internals** — TCP handshake, congestion control, MTU, latency vs
  bandwidth, TLS handshakes, connection pooling, keep-alive.
- **Advanced database concepts** — transactions and isolation levels, MVCC,
  locking, B-trees, indexing strategy, execution plans, query optimisation,
  connection limits, migrations without downtime.
- **NoSQL data models** — document/key-value/wide-column/graph; what you gain
  and precisely what you gave up.
- **Caching** — the whole chain: locality, invalidation, eviction, stampedes,
  cache-aside vs write-through, distributed caching.
- **Message queues and streaming** — at-least-once vs at-most-once vs
  exactly-once-as-marketing, ordering, idempotent consumers, dead-letter queues.
- **Event-driven architecture** — events vs commands, choreography vs
  orchestration, eventual consistency as a product decision.
- **Distributed systems fundamentals** — partial failure, timeouts and retries
  (and retry storms), idempotency, clocks, CAP as a starting point rather than a
  conclusion.
- **Containers** — namespaces, cgroups, images and layers, what Docker actually
  automates.
- **CI/CD** — pipelines, artifacts, environments, deployment strategies,
  rollback.
- **Cloud infrastructure** — compute/storage/network primitives, IAM, managed
  services and their lock-in.
- **Infrastructure as code** — declarative infrastructure, state, drift.
- **Security** — the OWASP classes and their mechanisms, secrets management,
  input trust boundaries, dependency risk.
- **Observability** — logs, metrics, traces; SLIs; how to debug a system you
  cannot attach a debugger to.
- **Performance engineering** — profiling, flame graphs, latency percentiles and
  why the mean lies, Little's Law, queueing basics, load testing.
- **Advanced algorithms** — graphs, dynamic programming, string algorithms,
  probabilistic structures (Bloom filters, HyperLogLog), and *why they show up in
  infrastructure*.

### You are here (and ready to leave) when

- You have run something in production, or an honest simulation of it, and
  handled a failure you did not anticipate.
- You have diagnosed a performance problem with a profiler, and the numbers, not
  a guess, told you where the time went.
- You can reason about a request's full path — client, DNS, TLS, load balancer,
  app, cache, database, disk — and say where the latency is.
- You can explain why a specific piece of your system is *not* consistent, and
  what the product consequence is.
- You have deliberately broken your own system (killed nodes, filled disks,
  injected latency) and fixed what that exposed.

### Anti-goal

Do not adopt microservices, Kubernetes, or event sourcing to learn them and then
leave them in a system that did not need them. Learn them on purpose, in a
sandbox, and be able to say when they are wrong.

---

## Level 4 — Expert

**Goal: you can be accountable for a system.**

Accountable means: its scale, its cost, its reliability, its failure modes, and
what happens at 3 a.m. The work is now as much about constraints, organisations,
and economics as about code.

### What you learn

- **Large-scale system design** — decomposition, boundaries, data flow, sizing
  from first principles (requests/sec → bytes → machines → dollars).
- **Distributed databases** — replication topologies, quorums, leader election,
  partitioning, rebalancing, cross-shard queries, distributed transactions and
  their real cost.
- **Consensus** — Paxos, Raft, ZAB: what they guarantee, what they cost, and why
  you should almost always use an existing implementation.
- **Fault tolerance** — failure domains, redundancy, bulkheads, circuit
  breakers, graceful degradation, blast-radius reduction.
- **High availability** — failover, split-brain, health checking that does not
  lie, multi-AZ and multi-region trade-offs.
- **Scalability** — vertical vs horizontal, statelessness, sharding strategy,
  hot partitions, backpressure end-to-end.
- **Reliability engineering** — SLIs/SLOs/error budgets, toil reduction, change
  as the dominant cause of outages.
- **Incident response** — command structure, mitigation before diagnosis,
  communication, blameless post-mortems that produce real changes.
- **Capacity planning** — headroom, growth modelling, load testing that
  resembles production, saturation points.
- **Cost optimisation** — unit economics, the cost of a request, egress,
  storage tiers, when engineering time is more expensive than the bill.
- **Advanced security** — threat modelling, defence in depth, blast-radius
  thinking, key management, supply chain, detection.
- **Infrastructure and cloud architecture** — multi-account/tenant boundaries,
  networking at scale, disaster recovery with tested RPO/RTO.
- **Advanced performance optimisation** — cache hierarchy, memory layout,
  syscall and allocation cost, tail latency, coordinated omission.
- **Architecture trade-offs** — writing decisions down (ADRs), defending them,
  and revisiting them when the constraints change.
- **Production engineering** — migrations at scale, backwards/forwards
  compatibility, feature flags, dual writes, backfills, rollback plans.

### You are here when

- You have designed a system that others built, and it worked — including under a
  failure you predicted.
- You have led or materially contributed to an incident response, and the
  post-mortem produced changes that prevented recurrence.
- You can size a system on paper and be within an order of magnitude, and
  explain your assumptions.
- You routinely say "we should not build that" and are right.
- You can state the cost — money, complexity, operational load — of your
  architectural choices.

### Anti-goal

Do not confuse "has opinions about architecture" with L4. The distinguishing
evidence is accountability for outcomes, not fluency in vocabulary.

---

## Level 5 — Guru

**Guru is not "knows more technologies." Someone who has used 40 databases and
understands none deeply is not here.**

Guru means: **you work correctly where no guidance exists, and you raise the
capability of everyone near you.**

### The capabilities

**First principles.** You can derive a system's behaviour from mechanisms rather
than from documentation, and you can work in a system nobody has written about.

**Design at scale and complexity.** Not just large traffic — large
*uncertainty*: multi-team systems, decade-long lifespans, requirements that will
change in ways nobody can name yet.

**Trade-off reasoning.** You can hold several incompatible goods in mind
(latency, consistency, cost, operability, delivery speed, team capability) and
choose, explicitly, what you are sacrificing.

**Diagnosing the unknown.** Given a symptom nobody has seen, with no runbook,
you can build a diagnosis from evidence — narrowing, bisecting, instrumenting,
and disproving your own hypotheses.

**Reading source code.** You can answer questions about a 500k-line codebase you
saw this morning by reading it, because the documentation does not cover your
case, or is wrong.

**Reading research papers.** You can read a systems or algorithms paper,
identify its actual contribution, find the assumption that makes it work, and
judge whether it applies to you.

**Designing experiments.** You can turn "is this faster?" into a measurement
that will not lie: a hypothesis, a controlled setup, an isolated variable, and
enough statistical care to distinguish signal from noise.

**Benchmarking.** You know how benchmarks mislead — warm-up, coordinated
omission, unrepresentative data, GC pauses, cache warmth, measuring the wrong
percentile — and you produce numbers others can trust and reproduce.

**Contributing to open source.** Not typo fixes: real changes in unfamiliar
codebases, with maintainers, under review, to a standard you did not set.

**Designing abstractions.** You can create an interface that makes a class of
problems easier — and you know that most abstractions are net negative, so you
design few and delete some.

**Explaining clearly.** You can make a hard idea land for an audience at a
different level, without falsifying it. This is a hard technical skill, and it
is the bottleneck on your influence.

**Deciding under uncertainty.** You commit to architectural decisions with
incomplete information, write down what would change your mind, and revisit
without ego.

**Knowing the limits of existing technology.** You know where the tools you use
stop working, and can tell "this needs different tooling" from "we are using it
wrong."

**Research and development.** When nothing available solves the problem, you can
build something that does, and evaluate it honestly against what exists.

**Mentoring.** You can raise other engineers' capability deliberately — which
requires diagnosing *their* gaps, not restating your own knowledge.

**Systems that survive.** Your systems keep working through traffic growth,
hardware failure, staff turnover, dependency deprecation, and requirements
churn. This is the ultimate test, and it is only measurable in years.

### You are here when

Others' work is measurably better because of you: engineers you mentored, an
abstraction people rely on, a diagnosis that saved a system, a design that held
up for five years, a contribution in a codebase you do not own.

Guru is the only level with no exit criteria, because there is no next level —
there is only the next problem.

### Warning

Level 5 is not reached by studying Level 5 material. It is reached by doing
Level 3 and Level 4 work for a long time, with unusual attention to *why*, and
by teaching. Reading a consensus paper does not make you L5; being the person
your team escalates to when the consensus layer misbehaves does.

---

## Using levels honestly

- Compute your level **per domain**, from the "you are here when" tests.
- Do not skip levels. You *can* skip topics — sometimes correctly — but a missing
  prerequisite does not disappear; it resurfaces as a bug you cannot explain.
- If you are stuck on a topic, the cause is usually a missing prerequisite one or
  two levels down. Go down, not sideways.
- Levels 3 and 4 are wide and slow. Progress there is measured in systems shipped
  and failures survived, not topics read. This is normal, not a plateau.
