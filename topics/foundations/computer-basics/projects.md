# How computers work — projects

[← How computers work](README.md) · [Exercises](exercises.md) ·
[Interview](interview.md)

---

## Core project

### [Anatomy of your own machine](../../../projects/machine-anatomy/README.md)

**Level 0** · a written investigation, no programming

Investigate the computer in front of you until you can draw it from memory and defend
every number you write down. Four stages: inventory the hardware, measure the memory
hierarchy, look at what is running, and connect files to bytes.

**Validates:** `memory-hierarchy`, `volatile-vs-persistent`, `latency-numbers`,
`process`

**Why it is the right project for this topic**

There is nothing to build at Level 0, because you cannot program yet. But there is
something to *do*, and it is not reading.

The project's value is in one rule: **predict every measurement before taking it.** You
will guess how long a 1 GB disk read takes, then find out. Most people are wrong by an
order of magnitude in one direction or the other, and being wrong cheaply — now, with a
scratch file, no consequences — is what installs the habit that Levels 3 through 5 depend
on entirely.

The secondary value is that the numbers become *yours*. When someone later claims a cache
saves 200 ms, you will have a felt sense of what 200 ms buys, because you measured
something comparable with your own hands on your own hardware. A table you read has none
of that weight.

**What it deliberately does not include**

No code. Adding "write a script to collect this" would seem like an upgrade and would
wreck the project — you would spend the time fighting syntax instead of building a model
of the machine. Programming starts in `what-programming-is`, with the right prerequisite
in place.

---

## Also on the ladder at this level

Two more Level 0 projects, listed in [projects/ladder.md](../../../projects/ladder.md).
Neither is required for this topic; both are cheap and worth doing if the core project
felt easy.

**Manual data organiser** — validates `files-and-directories`. Reorganise 200 files by
hand, time it, then estimate the same task for 20,000. The felt need for automation is
the actual prerequisite for wanting to program, and it is more persuasive than being
told.

**Trace a page load** — validates `internet-basics`. Follow a single request from URL to
rendered page using browser developer tools. Establishes that the web is machines sending
messages to other machines, which makes `internet-basics` land properly.

---

## How to know the project is done

The full checklist is in the
[project README](../../../projects/machine-anatomy/README.md#done-when). The three items
that matter most:

1. **Every number has the command that produced it.** A number you cannot reproduce is a
   number you copied.
2. **Predictions are recorded before their measurements, unedited.** If you edited a
   prediction after seeing the result, you removed the only calibration the project
   offers. Nobody will check; you will know.
3. **You can draw the machine from memory** — CPU, RAM, disk, and the paths data takes
   between them — with your measured speeds on the drawing. What you leave out of the
   drawing is what you have not yet internalised, which makes this the most useful of the
   three tests.

---

## After the project

Return to [`topic.yml`](topic.yml) and work through the remaining gates — the `break`,
`debug`, `explain`, and `review` items. The `explain` gates especially: explaining a power
cut to a non-technical person is genuinely harder than it sounds, and failing it tells you
exactly which part of your model is still vague.

Then continue to `what-programming-is`.
