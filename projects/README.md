# Projects

A project is the difference between knowing a topic and being able to do it. Reading
produces Knowledge; building produces Skill; breaking what you built produces
Judgment. There is no shortcut between those.

Every project here answers three questions:

1. **What competency does it validate?** (`validates` in `project.yml` — competency
   statements, not features)
2. **What constraints make it educational?** (`constraints` — the rules that stop it
   becoming assembly work)
3. **How will you break it?** (`break_it` — the stage everyone skips and the one that
   produces judgment)

---

## Specified projects

These have full specifications. See [ladder.md](ladder.md) for the complete planned
ladder across all levels.

| Level | Project | Validates | Core skill |
|---|---|---|---|
| 0 | [Anatomy of your own machine](machine-anatomy/README.md) | `computer-basics` | Measuring instead of assuming |
| 1 | [Expression calculator](cli-calculator/README.md) | `programming-fundamentals` | Decomposition, recursion, error design |
| 1 | [File organiser](file-organizer/README.md) | `programming-fundamentals` | A hostile external world; reversibility |
| 2 | [Data structures from scratch](ds-from-scratch/README.md) | `data-structures` | Invariants, and measurement vs. asymptotics |
| 3 | [In-memory cache](in-memory-cache/README.md) | `caching` | Eviction, concurrency, benchmarking |
| 3 | [URL shortener](url-shortener/README.md) | `caching`, `backend-development` | Read-heavy system design under load |

---

## Rules that apply to every project

**Start from a blank directory.** Not a template, not a clone, not a tutorial
repository. The decisions are the learning; if someone else made them, you got typing
practice.

**Read the constraints first.** They are not arbitrary difficulty. "No `eval`" in the
calculator, "no third-party cache library" in the cache, "no built-in dict" in the
data structures project — in each case the forbidden thing *is* the assignment.

**Predict before you measure.** Write the number down first, unedited. The gap between
prediction and result is the most valuable output of any project on this list.

**Finish it.** A finished small project teaches more than three abandoned ambitious
ones, because everything hard is in the last 20%.

**Do the `break_it` section.** It is not optional polish. It is where the topic stops
being theory. A project you have not broken is a project you do not understand.

**Write it up.** A README explaining what you built, what you chose, what you
measured, and what surprised you. This is the `explain` gate, and it is what makes
the project worth anything to anyone else — including a future employer, who can read
a design write-up far faster than they can read your code.

---

## How projects relate to topics

A topic's `topic.yml` lists projects with a `role`:

- **`core`** — do this one. It validates the topic's central competency.
- **`stretch`** — do it if you want depth, or if the core project felt easy.

A project can validate several topics, and a topic can have several projects. The
`validates` field in `project.yml` is the authoritative statement of what completing
it proves.

---

## Adding a project

Copy [`templates/project/`](../templates/project/) and read
[CONTRIBUTING.md](../CONTRIBUTING.md).

The bar for a new project:

| Test | Question |
|---|---|
| **Competency** | Does `validates` state capabilities, not features? "Builds a REST API" fails; "can design an idempotent write endpoint and demonstrate that a duplicated request causes no double charge" passes |
| **Constraint** | Is there at least one constraint that prevents shortcutting the lesson? |
| **Failure** | Does `break_it` contain failures the learner must cause deliberately? |
| **Finishable** | Can a learner at that level finish the core stages in one to three weeks of part-time work? |
| **Not a tutorial** | Does it specify *what* and *why*, and leave *how* to the learner? |

The last one is the most commonly failed. A project specification is a requirements
document, not a walkthrough. If a reader could follow it to a working system without
making a decision, it is a tutorial and it belongs somewhere else.
