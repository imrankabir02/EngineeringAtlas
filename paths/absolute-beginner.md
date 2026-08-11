# Absolute beginner

**Level 0 → Level 1** · roughly 4–8 months part-time · no prior knowledge assumed

Machine-readable steps: [`absolute-beginner.yml`](absolute-beginner.yml)

---

## Who this is for

You have never seriously studied technology. You may use computers every day; that is a
different thing.

The path ends at a specific, testable capability:

> You can open a blank file and write a 300-line program that solves a problem you chose, with
> no tutorial, and diagnose it yourself when it breaks.

That is Level 1. It is a real threshold and it is further away than most introductory material
implies.

---

## What this path deliberately does not do

**It does not start with a programming language.** The first seven steps are about the machine,
the filesystem, the terminal, and what a program *is*. That is about four to six weeks before you
write a line of code, and skipping it is the most common reason people stall three months later.

The reason is concrete rather than philosophical: if you do not know that memory is fast and
volatile while disks are slow and persistent, then "why did my program lose the data" has no
possible answer except magic. If you cannot read a file path, half of every error message is
noise. If you have never run a program from a terminal, you are dependent on an IDE button whose
behaviour you cannot inspect.

**It does not promise a timeline.** Four to eight months is the honest range for part-time study,
and individual variation is larger than any curriculum can account for. Eight months is not
behind schedule, because there is no schedule.

**It does not lead to a framework.** Web development is not the next step after this path. See
[what comes next](#what-comes-next).

---

## Phase 1 — the machine stops being magic

**Steps 1–7 · roughly 4–6 weeks**

| Step | What you get |
|---|---|
| [`computer-basics`](../topics/foundations/computer-basics/README.md) | A physical model of the machine, and numbers you measured yourself |
| `operating-system-basics` | The OS as a program that manages the others |
| `files-and-directories` | Paths, and that an extension is a convention rather than a fact |
| `command-line-basics` | The ability to see what is actually happening |
| `internet-basics` | Client and server; what a URL names |
| `what-programming-is` | A program as a precise description of a process |
| `problem-solving-basics` | Decomposition, and noticing your own assumptions |

The one that carries the phase is `computer-basics`, and specifically its project —
[Anatomy of your own machine](../projects/machine-anatomy/README.md). It has no code. You
investigate your own computer, and for every measurement you **write your prediction down
first**.

That prediction habit is the real deliverable of this phase. You will guess how long a 1 GB disk
read takes and be wrong, probably by a factor of ten. Being wrong cheaply — now, with a scratch
file and no consequences — installs the instinct that everything from Level 3 upward depends on.
It reappears at Level 5 as
[experiment design](../docs/competency-gates.md#7-benchmark), unchanged in nature.

**Milestone.** You can navigate a filesystem and run programs from a terminal without a GUI, you
can explain the memory-versus-disk difference using numbers you measured, and you can read an
error message and separate the message from the location from the noise.

---

## Phase 2 — you can make a computer do something

**Steps 8–9 · roughly 3–7 months**

This phase is one enormous step and one small one.

### [`programming-fundamentals`](../topics/programming/programming-fundamentals/README.md)

Budget 8 to 16 weeks. This is the single longest topic in the entire repository and the one most
commonly learned badly.

**Pick one language and finish it.** Which one matters far less than that. For most people,
Python — the reasoning, including what it costs you, is in the
[topic README](../topics/programming/programming-fundamentals/README.md#which-language).

Two projects, both from a blank file:

- [Expression calculator](../projects/cli-calculator/README.md) — no `eval`. Precedence forces
  you to represent structure rather than scan text, which is where recursion becomes necessary
  rather than decorative.
- [File organiser](../projects/file-organizer/README.md) — dry-run by default. Your first
  program where a bug destroys data, which changes how you write code in a way nobody becomes
  careful by being told.

### `version-control-git`

Small step, and put it here rather than earlier for a reason: you now have code worth not losing,
so the tool has an obvious purpose.

Learn what a commit actually *is* — a snapshot plus parents — before learning the commands. Git's
interface only makes sense once its object model does, which is why people who learn the commands
first stay afraid of it for years.

The discipline at this stage is one line: **commit whenever something works.** That is enough,
and it immediately makes you a bolder editor, because you can always get back.

**Milestone.** You can write a 300-line program from a blank file solving a problem you chose,
with no tutorial, and diagnose it yourself when it breaks. **You are Level 1.**

---

## Where people stall, and what to do

**Stalling in phase 1 because it feels like it is not "real" programming.** It is not, and it is
load-bearing. Four weeks here saves months later. If you are impatient, do the project — it is
concrete and it produces numbers.

**Stalling in `programming-fundamentals` at around week three.** Almost universal. This is the
point where tutorials stop being enough and you have to write something nobody showed you. It
feels like a wall and it is the actual work starting.

What helps, in order: do the [exercises](../topics/programming/programming-fundamentals/exercises.md)
before the projects, so mechanics are automatic and the project's difficulty is design rather
than syntax. Trace confusing code on paper. Reduce a bug to five lines before trying to fix it.

**Frozen in front of a blank file, but able to read code fine.** This is the diagnostic symptom of
[tutorial hell](../docs/philosophy.md#tutorial-hell): recognition without production. The fix is
not more reading. Start something small and badly. A working 50-line program you wrote is worth
more than a 500-line one you followed.

**Switching languages when it gets hard.** It feels identical from the inside to making a good
choice. The test: are you switching *before* or *after* the difficulty? Finish both projects in
one language.

**Comparing yourself to people who started earlier.** Their week 3 also looked like yours. Nobody
posts about being stuck.

---

## Honest effort estimate

| Phase | Focused hours | Calendar, at ~8 h/week |
|---|---|---|
| Phase 1 (7 topics + project) | ~40 | 5–6 weeks |
| Phase 2 (`programming-fundamentals`) | ~120 | 15 weeks |
| Phase 2 (`version-control-git`) | ~15 | 2 weeks |
| **Total** | **~175** | **~22 weeks (5–6 months)** |

At 4 hours a week that is closer to eleven months. At 20 hours a week — a full-time change of
career — it is about nine weeks. All three are normal.

The variance between individuals at this level is larger than at any later level, which is worth
knowing so you do not read your own pace as a verdict.

---

## What comes next

You are Level 1. Four honest options:

| Next | Choose it if |
|---|---|
| [Programming foundations](programming-foundations.md) | You want the general engineering foundation before specialising. **The default recommendation** |
| [Software engineering core](software-engineering-core.md) | You want the whole spine to Level 4 in one path. Continues exactly where this one stops |
| [Python backend](stacks/python-backend.md) | You learned Python and want to build services. Starts here |
| [`data-structures`](../topics/computer-science/data-structures/README.md) | You want depth in what your language has been doing for you |

**Do not go to a web framework.** Django, Rails, React, and Express all work fine until something
breaks one layer below where you are looking, at which point it is unrecoverable, because you have
no model of what is underneath. The prerequisite graph exists to prevent exactly this — see
[framework-first learning](../docs/philosophy.md#framework-first-learning). Go through `http`,
`sql`, and `data-structures` first. It is not much longer and it is the difference between using
a framework and being trapped in one.
