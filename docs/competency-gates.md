# Competency Gates

A gate is a **specific action with an observable outcome** that you either did or
did not do. Gates replace self-assessment, which is unreliable in a predictable
direction: people who have only read about something consistently overestimate
how well they could do it.

Every topic's `topic.yml` declares gates. `build` and `explain` are mandatory;
the rest are used where they discriminate.

---

## The loop

```
Learn ──► Practice ──► Build ──► Break ──► Debug ──► Explain ──► Benchmark ──► Review ──► Advance
   ▲                                                                                        │
   └────────────────────────── failed a gate? go back to the stage that would fix it ───────┘
```

The loop is not decorative. Each stage produces evidence the previous stage
cannot, and the ordering matters: you cannot debug a failure you have not
caused, and you cannot explain a mechanism you have not observed failing.

---

## The nine stages

### 1. Learn

Build the mental model. Read the primary source, not a summary of a summary.

**Output:** you can restate the idea in your own words, including what problem it
solves.
**Trap:** stopping here. Learning feels like the whole activity because it is the
only stage with obvious progress.

### 2. Practice

Small, bounded, repeated problems with fast feedback. Fifteen small exercises
beat one large one at this stage, because the feedback loop is where the learning
happens.

**Output:** fluency — you stop thinking about syntax and mechanics.
**Trap:** practising only what you can already do. Practice should fail
sometimes; if it never does, it is too easy to be useful.

### 3. Build

Make something whole, from a blank directory, that you decided the requirements
for.

**Output:** an artifact, and a list of everything the tutorials silently handled
for you.
**Trap:** following a build-along. If someone else made the decisions, you got
typing practice.

### 4. Break

Deliberately cause failure. This is the stage that separates people who know a
system from people who have used one.

Standard breakages, applicable to almost anything:

| Break | Reveals |
|---|---|
| Kill a dependency mid-operation | What state you left behind; whether you are idempotent |
| Fill the disk | Whether your error paths were ever executed |
| Add 500 ms latency to every call | Which timeouts are wrong; whether retries stampede |
| Drop the cache entirely | Whether the system was ever able to serve real load |
| Send malformed and hostile input | Where your trust boundaries actually are |
| Restrict to one CPU / clamp memory | What your concurrency model assumed |
| Run two instances concurrently | Every race you did not know you had |
| Set the clock forward, or backward | Every assumption about time being monotonic |
| Duplicate a message | Whether "at least once" was handled or hoped about |

**Output:** a reproducible failure, and a written explanation of the mechanism.
**Trap:** breaking it and moving on without diagnosing. The break is only worth
the time if stage 5 follows.

### 5. Debug

Take the failure from symptom to root cause using evidence.

The method:

1. Reproduce it reliably. An intermittent bug you cannot trigger is not yet
   being debugged.
2. Write down what you believe is happening — before you look.
3. Find the cheapest observation that would *disprove* it.
4. Bisect. In space (which component?), in time (which change?), in data (which
   input?).
5. Continue until you can predict the failure, then fix it.
6. Explain why it went unnoticed, and what would have caught it earlier.

**Output:** a root-cause statement specific enough that someone else could
reproduce and fix it.
**Trap:** stopping at the first change that makes the symptom disappear. That is
not a diagnosis; that is a coincidence you have shipped.

### 6. Explain

Write it down for someone one level below you. Writing is where you find the
parts you were pattern-matching rather than understanding — this is not a
metaphor, it is the reliable experience of everyone who tries it.

**Output:** a short document — a design note, a post-mortem, a README section —
that another person can act on.
**Trap:** explaining *what you did* instead of *why it works and what it costs*.

### 7. Benchmark

Measure. Then compare against what you predicted.

Rules that make a benchmark worth anything:

- **Predict first.** Write the number you expect down before measuring. The gap
  is the entire lesson.
- **Warm up, and exclude the warm-up.** JIT, page cache, connection pools, and
  CPU frequency scaling all make the first run a lie.
- **Report percentiles, not means.** p50, p95, p99, max. The mean hides exactly
  the behaviour users notice.
- **Beware coordinated omission.** A load generator that waits for a response
  before sending the next request will not record the latency of the requests it
  failed to send. This makes overloaded systems look fast.
- **Change one variable.** Otherwise you have an anecdote.
- **Record the setup.** Hardware, data shape and size, concurrency, versions.
  A benchmark that cannot be reproduced is a claim, not a measurement.
- **Measure the realistic distribution.** Real keys are skewed, real payloads
  vary, real caches are partially warm. Uniform-random inputs flatter everything.

**Output:** numbers, a stated setup, and the reason your prediction was wrong.
**Trap:** benchmarking to confirm a decision already made.

### 8. Review

Critique code and designs you did not write. Producing and evaluating are
different skills, and evaluation is the one that transfers into judgment.

**Output:** review comments about design, correctness, and failure modes — not
formatting.
**Trap:** reviewing only for style, because style is the only thing you can see
without understanding the change.

### 9. Advance

Move on, deliberately, having recorded what evidence you have and what you
skipped.

---

## Gate types for advanced topics

At Level 3 and above, "did you build it" stops discriminating. These gate types
target judgment.

### Design challenges

A problem statement with constraints, no solution. Produce an architecture, then
defend it.

Good design challenges have a trap: the obvious answer is wrong for a reason
stated in the constraints. Example — *"Design a rate limiter for an API with
2,000 nodes; limits must be accurate to within 1%; nodes may not share a
database on the request path."* The obvious answer (a shared counter) violates
the last constraint; the trap teaches distributed counting.

### Debugging challenges

A symptom, a system, and no runbook. Sometimes with a red herring.

Example — *"p99 latency tripled at 14:00. Deploys were frozen. CPU, memory, and
request volume are flat. Find the cause."* (Plausible answers: a dependency's own
p99, a cache expiring in bulk, a cron job saturating I/O, connection pool
exhaustion, a routing change, a table crossing a size threshold that changed the
query plan.)

### Performance challenges

"Make this 10× faster" with a fixed workload and a required correctness test.
The lesson is almost always that the bottleneck is elsewhere than expected.

### Architecture exercises

Take a real system's public design (a paper, an engineering blog post) and:

- state what constraint forced each decision
- name a decision you would make differently, and what it would cost you
- identify what would break at 100× the scale

### Failure simulations

Choose a component. Write down what you predict happens if it fails. Then fail
it. Score your prediction. This is the cheapest judgment-building exercise that
exists.

### Code review exercises

Review a real open-source pull request before reading the discussion, then
compare your comments to the maintainers'. What did they see that you did not?
That gap is the most direct measurement of judgment available to a self-learner.

### Research exercises

Read a paper. Answer, in writing:

- What is the contribution? (One sentence. Not the abstract.)
- What assumption makes it work?
- What does it cost?
- Does it apply to a system you have built? Why or why not?

---

## Failing a gate

Failing a gate is information, not a verdict. It tells you which stage to return
to:

| Symptom | Return to |
|---|---|
| Cannot start the build | Learn — the mental model has a hole |
| Build works but you cannot say why | Explain, then Learn what you could not write |
| Cannot cause a failure on purpose | Learn — you do not know what is load-bearing |
| Broke it, cannot diagnose it | Learn the layer below |
| Benchmark contradicts your prediction | Learn — this is the most valuable failure available |
| Review comments are all about style | Practice reading unfamiliar code |

The gate you fail most is the topic you understand least, regardless of how much
of it you have read.
