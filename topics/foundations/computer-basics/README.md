# How computers work

**Level 0** · Foundations · ~12 focused hours · no prerequisites

What a computer physically is, and what "running a program" actually means.

[Fundamentals](fundamentals.md) · [Concepts](concepts.md) ·
[Practical](practical.md) · [Exercises](exercises.md) · [Projects](projects.md) ·
[Interview](interview.md) · [Advanced](advanced.md) · [Resources](resources.md)

---

## What this is

A computer follows instructions on data, very fast and very literally. This topic
covers the parts that make that possible — processor, memory, storage — and, crucially,
**how far apart they are in time.**

You will finish able to draw your own machine, state roughly how long each part takes
to reach, and explain what survives a power loss.

## Why it matters

Two reasons, both load-bearing for everything after this.

**Performance is a question of location.** Nearly every slow system you will
encounter is slow because data is further from the processor than it needs to be —
on disk instead of in memory, across a network instead of on the machine, in a
database instead of in a cache. Without a physical model, "the API is slow" has no
possible explanation except magic, and every fix is a guess.

**Correctness is a question of what survives.** The difference between memory and
disk is the difference between "the program knows it" and "the program will still
know it after a crash." Databases, transactions, and durability all exist because of
that one distinction.

There is a third reason, less obvious and more important: this is where you learn to
**measure instead of assume**. You will predict how long something takes, then find
out. Being wrong repeatedly and cheaply, now, builds the instinct that separates
engineers who keep improving from those who plateau.

## Prerequisites

None. This is the entry point to the entire map.

If you can open a terminal and type a command, you have what you need. If you cannot
yet, that is fine — the [practical](practical.md) file starts there.

## How deeply to learn this

Full depth guidance is in [concepts.md](concepts.md), which marks every concept
`aware`, `working`, or `deep`. The short version:

**Deep** — the memory hierarchy and the volatile/persistent distinction. These two
ideas you should be able to explain to someone else, from memory, with rough numbers.

**Working** — what running a program means, files as bytes, binary and encoding,
hardware versus software, rough latency numbers.

**Aware** — what an operating system does, processes, how CPU caches work internally.
You need to know these exist. The mechanisms come later, in
`operating-system-basics` and much later in `operating-systems-fundamentals`. Do not
go down those rabbit holes now; you will come back with the right prerequisites.

The most common way to waste time here is to start reading about cache-line sizes and
branch prediction. That material is genuinely interesting and genuinely useless to you
today.

## Reading order

1. [fundamentals.md](fundamentals.md) — the machine from first principles. Start here.
2. [concepts.md](concepts.md) — the inventory, with depth per concept.
3. [practical.md](practical.md) — the commands to inspect your own machine.
4. [exercises.md](exercises.md) — small drills, each verifiable.
5. [projects.md](projects.md) — the machine-anatomy investigation.
6. [interview.md](interview.md) — what a competent answer sounds like.
7. [resources.md](resources.md) — fewer, better.
8. [advanced.md](advanced.md) — short, and honest about why.

## How you know you have it

The gates are in [`topic.yml`](topic.yml). In summary, you can:

- **Explain** to a non-technical person why unsaved work disappears in a power cut.
- **Explain** why the second time you open a large file it opens faster.
- **Benchmark** disk-cold, disk-warm, and memory reads on your own machine, having
  predicted the numbers first.
- **Break** things deliberately: fill a disk, exhaust memory, lie about a file type.
- **Build** the [machine-anatomy](../../../projects/machine-anatomy/README.md) report.

## What comes next

| Next | Why |
|---|---|
| `what-programming-is` | You know what a machine does; next is how you tell it what to do |
| `operating-system-basics` | You saw that many programs run at once, isolated. The OS is how |
| `internet-basics` | The same distance argument, extended between machines |
