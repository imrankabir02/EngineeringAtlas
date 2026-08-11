# How to Use This Repository

The repository is a map, not a course. It does not have a beginning; it has a
*your* beginning, which depends on what you can already do.

The loop:

```
Start Here → Choose Your Goal → Find Your Current Level → Follow Prerequisites
   → Learn → Practice → Build → Validate → Advance ──┐
   ▲                                                 │
   └─────────────────────────────────────────────────┘
```

Ten to fifteen minutes of setup here saves months of directionless study. Do it
properly.

---

## Step 1 — Start here

Read, in order:

1. [philosophy.md](philosophy.md) — why this repository is shaped the way it is,
   and the ten questions every topic answers. **Do not skip this one.** If you
   skip it you will use the repository as a link collection and get link-collection
   results.
2. [levels.md](levels.md) — the competency model, and the four axes that levels do
   not capture.
3. This document.

---

## Step 2 — Choose your goal

A goal is a capability, not a job title, and not a technology.

| Weak goal | Usable goal |
|---|---|
| "Learn backend" | "Build and operate an API that serves real users and survives its dependencies failing" |
| "Learn Kubernetes" | "Deploy and debug a multi-service application on a cluster I did not set up" |
| "Get a job" | "Be able to pass a system design interview and a take-home for a mid-level backend role" |
| "Learn AI" | "Train, evaluate, and deploy a model, and know when the answer is not machine learning" |

Then pick the matching path from [paths/README.md](../paths/README.md). Pick
**one**. Two paths at once is technology hopping with extra structure.

If no path matches, choose the closest and treat its differences as your own
research problem. That is a Level 4 skill and starting it early is fine.

---

## Step 3 — Find your current level

Do **not** self-assess by reading the level descriptions and picking the one that
sounds like you. Everyone overestimates this, in a well-documented direction.

Instead, take the **"you are here when"** test in [levels.md](levels.md) for each
level, starting at Level 1. Your level is the highest one whose test you can pass
*right now, unaided, without looking anything up*.

Two specific tests worth taking seriously, because they are the ones people
usually fail after assuming they would pass:

- **Level 1 → 2:** open a blank file and write a 300-line program that solves a
  problem you chose, with no tutorial. Not a tutorial project. Not something you
  have written before.
- **Level 2 → 3:** take something you built and make it fail in a way you did not
  plan for, then diagnose it from evidence.

If a test is uncomfortable to attempt, that discomfort is the answer.

Compute your level **per domain**. Being L3 in backend and L0 in embedded is
normal and permanent.

---

## Step 4 — Follow prerequisites

Open your path's first unmet topic. Read its `README.md` and check the
prerequisites.

Two kinds:

- **Hard** — the topic will not make sense without them. The concepts will feel
  arbitrary and you will resort to memorisation.
- **Soft** — helpful, and they make the topic feel concrete rather than abstract.
  Skipping soft prerequisites is a reasonable trade-off.

**If you are missing a hard prerequisite, go there instead.** This is the
single highest-value behaviour the repository can teach you. Almost every "I
just don't get X" is a missing prerequisite one or two levels down, not a
deficiency in you and not a bad explanation of X.

You *may* skip a hard prerequisite deliberately — sometimes a deadline decides
for you. If you do, write down what you skipped. The bill arrives later as a bug
you cannot explain, and knowing what you skipped turns three days of confusion
into ten minutes.

---

## Step 5 — Learn

Inside a topic, read in this order:

| Read | For |
|---|---|
| `README.md` | Orientation, prerequisites, how deep to go, reading order |
| `fundamentals.md` | The concept from first principles — the problem before the solution |
| `concepts.md` | The inventory, with a required depth for each item |
| `practical.md` | Doing it for real: tools, commands, failure modes, selection rubric |

Use `concepts.md` to budget your attention. Each concept is marked `aware`,
`working`, or `deep`. **Trust the markings.** They are the answer to "how deeply
should I learn this?", and going deep on an `aware` concept is a common and
expensive way to feel productive while making no progress.

Resources are in `resources.md`, tiered. Start with Tier 2 if you are new to the
topic, Tier 1 if you need to be certain. Do not read all of them; three good
resources fully worked through beat twelve skimmed.

---

## Step 6 — Practice

`exercises.md`. Small, bounded, verifiable drills.

Do them **before** the project, not after. Practice exists to make the mechanics
automatic so that the project's difficulty is design, not syntax.

If every exercise is easy, skip ahead — you already have this. If none is, you
are missing a prerequisite.

---

## Step 7 — Build

`projects.md` points to the projects that validate this topic. Do the `core` one.

Non-negotiable rules:

- **Start from a blank directory.** Not a template, not a clone, not a tutorial
  repository.
- **You make the decisions.** Structure, libraries, schema, error handling. Being
  wrong is part of it; the wrong decision you made and then had to live with is
  worth more than the right one you copied.
- **Read the `constraints` in `project.yml`.** They are what make the project
  educational rather than assembly. "No third-party cache library" is not
  arbitrary difficulty; the eviction logic *is* the lesson.
- **Finish it.** A finished small project teaches more than three abandoned
  ambitious ones, because everything hard is at the end.

---

## Step 8 — Validate

This is the step that distinguishes this repository from a reading list, and it is
the step people skip.

Open the topic's `gates` in `topic.yml`. Work through them:

- **Build** — you did this in step 7.
- **Break** — make it fail on purpose. Kill the database mid-write. Fill the
  disk. Add 500 ms of latency. Send garbage.
- **Debug** — diagnose what you broke, from evidence, to root cause.
- **Explain** — write it down for someone one level below you. Writing is where
  you discover which parts you were pattern-matching.
- **Benchmark** — predict a number, then measure it. The gap is the lesson.
- **Review** — critique code you did not write.

Details and method: [competency-gates.md](competency-gates.md).

A gate you cannot pass tells you exactly where to go back to. That is the
information you came for.

---

## Step 9 — Advance

Record your state and evidence — see
[progress-tracking.md](progress-tracking.md). Then read the topic's `next`, which
names candidate topics *and why each follows*.

Then repeat from step 4.

---

## Common ways to use this badly

| Behaviour | Result | Instead |
|---|---|---|
| Reading many topic READMEs to "get an overview" | A map of things you cannot do | Read one topic properly, all the way through the gates |
| Starting at a topic that sounds interesting, ignoring prerequisites | Memorisation, then a wall | Take the level test; start where it says |
| Doing the reading, skipping the project | High Knowledge, zero Skill — tutorial hell with better structure | The project is the point |
| Doing the project, skipping Break/Benchmark | Confidently wrong under load | These two stages produce judgment; nothing else does |
| Following three paths at once | Three abandoned paths | One path to a deployed, benchmarked system |
| Marking everything `mastered` | A tracker that measures optimism | Evidence, per [progress-tracking.md](progress-tracking.md) |

---

## If you are already an experienced engineer

Use the repository as a gap-finder rather than a curriculum:

1. Take the "you are here when" tests for Levels 3 and 4. Most working engineers
   fail one or two items and are surprised by which.
2. Read [dependency-map.md](../graph/dependency-map.md) and look for topics you
   use daily but have never studied deliberately. Almost everyone has several —
   TLS, TCP internals, transaction isolation, and the memory hierarchy are the
   usual ones.
3. Go straight to `advanced.md` and the Tier 1 resources for those topics.
4. Use the gates, especially **Break** and **Benchmark**. Experience produces
   Skill efficiently and Judgment slowly; deliberate failure injection is the
   fastest way to close that gap.

The most common finding is not a missing technology. It is a layer — usually one
below where you normally work — that you have been treating as a black box for
years.
