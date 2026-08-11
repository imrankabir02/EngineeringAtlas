# Learning Philosophy

The project's position, stated once:

> Competence is the ability to produce a correct outcome in an unfamiliar
> situation. Nothing else counts as knowing something.

Course completion, certificates, tutorial hours, and the number of technologies
you can name are all *proxies*. Proxies are useful until they are optimised for,
at which point they become worse than nothing, because they produce confident
people who cannot do the work.

Everything in this repository is organised to make the real thing — capability —
easier to reach than the proxy.

---

## The ten questions

Every topic must answer all ten. If a topic cannot answer them, it is not ready
to be published.

| # | Question | Where it is answered |
|---|---|---|
| 1 | What is this? | `README.md`, `fundamentals.md` |
| 2 | Why does it matter? | `README.md` — including what breaks without it |
| 3 | What prerequisite knowledge is required? | `topic.yml` → `prerequisites.hard` |
| 4 | What should I learn before this? | `topic.yml` → `prerequisites` + reading order in `README.md` |
| 5 | What exactly should I learn? | `concepts.md`, `practical.md` |
| 6 | How deeply should I learn it? | `concepts.md` — a required depth per concept |
| 7 | What should I practice? | `exercises.md` |
| 8 | What should I build? | `projects.md` |
| 9 | How do I know I actually understand it? | `topic.yml` → `gates`, plus `interview.md` |
| 10 | What should I learn next? | `topic.yml` → `next` |

Question 6 is the one most curricula omit, and its absence is expensive. "Learn
Kubernetes" is not actionable. "Be able to explain what a controller loop is and
debug a pod stuck in `CrashLoopBackOff`; you do **not** need to know how the
scheduler's scoring plugins work unless you are operating a cluster" is
actionable, and it also tells you when to stop and move on.

---

## Knowledge → Skill → Judgment → Mastery

These are four different things. Conflating them is the single most common
reason engineers plateau.

### Knowledge — "I can state it correctly"

You can explain what a database index is, why it speeds up reads, and why it
slows down writes.

Acquired by: reading, lectures, documentation.
Cheap to acquire. Cheap to fake. Decays fast without use.

### Skill — "I can do it reliably"

You can look at a slow query, read its execution plan, add the right index,
and verify the improvement — repeatedly, on code you did not write.

Acquired by: deliberate practice with feedback. Requires doing the thing and
finding out you were wrong.

Knowledge without skill is the tutorial-hell state: you recognise every concept
in a video and can build nothing.

### Engineering judgment — "I can decide well under uncertainty"

You can decide *whether to add the index at all*, given that this table takes
40k writes/second, the query runs twice a day on an internal dashboard, and the
index would add 12 GB. You choose not to, and you can defend it.

Acquired by: making decisions, living with the consequences, and — critically —
studying decisions others made and *why* they made them (post-mortems, design
docs, RFC discussions, papers).

This is the level most job descriptions actually want and most curricula never
address, because judgment cannot be taught by exposition. It requires
consequences. The gate system (see below) is the closest simulation available:
break your own systems, then decide.

### Mastery — "I can extend the field"

You understand the mechanism deeply enough to work correctly where no guidance
exists: novel problems, new failure modes, missing abstractions. You can read
the source, read the paper, design the experiment, and be the person others
escalate to.

Acquired by: sustained first-principles work, reading primary sources,
building things that are hard, and teaching — teaching is where you discover
which parts you only *thought* you understood.

**The progression is not automatic.** More knowledge does not become skill, and
more skill does not become judgment. Each transition requires a different
activity. The repository's level model (see [levels.md](levels.md)) tracks
capability across all four axes rather than counting topics covered.

---

## The competency loop

No topic is complete at "I read it." The loop:

```
Learn → Practice → Build → Break → Debug → Explain → Benchmark → Review → Advance
```

Each stage produces something the previous stage could not:

| Stage | Produces | What it exposes |
|---|---|---|
| **Learn** | vocabulary, mental model | — |
| **Practice** | fluency on small, bounded problems | gaps in the mental model |
| **Build** | a working artifact | everything the tutorial silently handled for you |
| **Break** | a reproducible failure you caused deliberately | your assumptions about what is load-bearing |
| **Debug** | a diagnosis, from symptom to root cause | whether you understand the mechanism or just the API |
| **Explain** | a written or spoken account someone else can act on | the parts you were pattern-matching |
| **Benchmark** | numbers | the difference between what you believe and what is true |
| **Review** | critique of code you did not write | whether you can evaluate, not just produce |
| **Advance** | a decision to move on, with evidence | — |

**Break and Benchmark are the stages everyone skips, and they are where
judgment comes from.**

You do not understand a system until you have made it fail on purpose. Kill the
database mid-transaction. Fill the disk. Add 300 ms of latency. Drop the cache.
Send malformed input. Run it with one CPU. Each of these teaches something no
amount of reading will.

You do not know whether something is fast until you measured it. Engineers are
consistently wrong about where time goes — including experienced ones. This is
not a character flaw; it is why profilers exist.

Full specification: [competency-gates.md](competency-gates.md).

---

## First principles

Teach the problem before the solution. Always.

A technology is an *answer*. Presented without its question, it is arbitrary
trivia — memorable at best, and useless the moment the ecosystem moves.

Bad:

> Learn Redis. It's an in-memory key-value store. Here are the commands.

What the learner ends up with: a command reference and no ability to decide
whether Redis belongs in their system.

Good:

```
Why is this request slow?
    ↓
Where does the time go? (measure)
    ↓
Memory is ~100,000× faster than a network round trip to disk-backed storage
    ↓
Some data is read far more often than it changes  (locality)
    ↓
So: keep a copy of hot data closer to the reader        ← this is caching
    ↓
Now you own a second copy of the truth  →  when is it wrong?  (invalidation)
    ↓
The copy is smaller than the truth      →  what do you evict?  (LRU/LFU/TTL)
    ↓
One machine's memory is not enough      →  distributed caching, hashing, hot keys
    ↓
Redis, Memcached, and your CDN are implementations of the above
```

A learner who follows the second version can evaluate a cache they have never
seen, because they know what problem it must solve and what problems it creates.
They can also recognise when the correct answer is "no cache — fix the query."

Same treatment for everything:

```
What problem does HTTP solve?
  → two programs on different machines need to exchange documents
  → client/server, request/response, statelessness and what it costs
  → it needs an ordered reliable byte stream → TCP
  → the bytes are readable by anyone on the path → TLS
  → one request per connection is slow → keep-alive, pipelining, HTTP/1.1
  → head-of-line blocking within a connection → multiplexing, HTTP/2
  → head-of-line blocking *below* TCP → QUIC, HTTP/3
```

Every step is a *problem* that the next step answers. That is the shape all
content in this repository should take. Each topic's `fundamentals.md` carries
this chain explicitly, and `topic.yml` records it as
`first_principles_chain` so it can be reviewed for gaps.

---

## Anti-patterns

Named because naming them makes them easier to notice in yourself.

### Tutorial hell

Watching or reading continuously without building. It feels productive because
comprehension feels like capability. It is not — recognition and recall are
different from production.

**Symptom:** you follow along fine, and freeze in front of an empty file.
**Fix:** ratio discipline. For every hour consuming, spend at least two hours
producing, on a problem the tutorial did not solve. Change the requirements.
Delete the code and rewrite it from memory. Build the thing again, differently.

### Certificate collecting

Optimising for credentials rather than capability. Certificates are weak signals
of *exposure* and near-zero signals of skill; the people who evaluate you know
this.
**Fix:** ship artifacts. A repository with a real system, a written design doc
explaining the trade-offs, and benchmarks outperforms any certificate.

### Framework-first learning

Learning Django before HTTP, React before the DOM, Kubernetes before processes
and networking. It works — until something breaks one layer below where you
looked, and then it is unrecoverable, because you have no model of what is
underneath.
**Fix:** the prerequisite graph. It exists exactly to stop this. When a
framework confuses you, the confusion is almost always in a prerequisite.

### Technology hopping

Restarting at the shallow end of a new stack whenever difficulty arrives. Ten
technologies at 10% is not one technology at 100%; it is not even close, because
everything hard is in the last 30%.
**Fix:** finish one path to a working, deployed, benchmarked system before
starting another. Depth transfers between stacks; breadth does not.

### Copy-paste projects

Following a build-along and adding it to your portfolio. You did the typing,
not the engineering — no decisions were yours, so no judgment was formed.
**Fix:** if you follow a tutorial project, immediately rebuild it from a blank
directory with a changed requirement (different storage engine, add auth,
support 100× the data). The rebuild is the learning; the tutorial was the
lecture.

### Interview-question memorisation

Grinding question banks. It produces recall of solutions, which collapses under
any perturbation, and it produces no capability at all for the actual job.
**Fix:** solve problems you have not seen, out loud, on the whiteboard, and
practise *deriving* rather than *retrieving*. See
[validation/README.md](../validation/README.md).

### Tool worship

Knowing a tool's flags without knowing what it does. Being able to run
`kubectl` while unable to explain what a container is.
**Fix:** for every tool, be able to state the problem it solves, the mechanism
it uses, and one alternative. See
[technology-selection.md](technology-selection.md).

### Résumé-driven architecture

Choosing technology for what it does for your career rather than for the system.
The costs land on your colleagues and your on-call rotation.
**Fix:** the technology-selection rubric — you must be able to state when *not*
to use it, and what the simpler alternative would cost.

---

## What this repository will not do

- **Promise timelines.** "Learn X in 30 days" is either a lie or a redefinition
  of "learn". Time-to-competence varies by a factor of five between individuals
  and the honest answer is a range with assumptions attached. Where a topic
  gives estimates, they are focused hours with the assumptions stated.
- **Rank technologies by popularity.** Popularity is evidence about hiring
  markets, not about fitness for your problem.
- **Motivate you.** There is no fluff, no "you've got this", no gamification.
  The content assumes you brought your own reasons.
- **Pretend the order is arbitrary.** Prerequisites are real. Skipping them is
  allowed and sometimes correct — but the repository will tell you what you are
  skipping and what it will cost.
- **Confuse a checked box with mastery.** See
  [progress-tracking.md](progress-tracking.md). Every status beyond "learning"
  requires evidence that exists outside this repository.
