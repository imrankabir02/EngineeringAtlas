# How computers work — resources

Six resources. Not sixty. Choosing what to read is a hard problem you are not yet equipped
to solve, so it has been solved for you — see
[resource-tiers.md](../../../docs/resource-tiers.md) for the selection rules.

`topic.yml` holds the machine-readable version of this list.

[← How computers work](README.md) · [Fundamentals](fundamentals.md) ·
[Advanced](advanced.md)

---

## Tier 1 — Primary sources

The thing itself, written by the people who define it.

### [Intel 64 and IA-32 Architectures Software Developer Manual, Volume 1, chapter 3](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html)

**Do not read this cover to cover.** It is thousands of pages of reference material for
people writing compilers and operating systems.

Open Volume 1, find chapter 3, and look at the register diagrams for ten minutes. Come
away knowing one thing: **registers are real, there are very few of them, and they have
names.** That single observation removes a surprising amount of later mystery about what
"the CPU is working on" means.

The second reason it is listed: you should see, once, early, that this kind of document
exists and is readable by humans. Being unafraid of primary sources is a Level 4 habit and
it starts by opening one.

### [`man 5 proc` — the Linux /proc filesystem](https://man7.org/linux/man-pages/man5/proc.5.html)

The authoritative description of where Linux publishes facts about your machine.

Use it as a lookup while doing the [project](../../../projects/machine-anatomy/README.md):
find `/proc/cpuinfo`, `/proc/meminfo`, `/proc/loadavg`. It teaches something `lscpu` hides
— that these numbers come from a specific place, and that convenience commands are just
readers of files you can read yourself.

Read it in your terminal (`man 5 proc`) rather than in a browser. Learning to navigate a
man page — `/` to search, space to page, `q` to quit — is worth the five minutes.

---

## Tier 2 — High-quality learning material

Built to teach, by people with authority, still useful in five years.

### [*Code: The Hidden Language of Computer Hardware and Software* — Charles Petzold](https://www.charlespetzold.com/code/)

**The single best resource for this topic.** If you read one thing, read this.

Petzold builds a working computer from switches and relays, one step at a time, starting
from two people sending signals along a wire. Nothing is assumed and nothing is taken on
faith. By the end you have constructed — on paper, but genuinely — a machine that executes
instructions, and the entire stack above it stops feeling like magic.

Roughly 15 hours. The best return on reading time available at Level 0, and it stays
correct forever because it is about mechanisms, not products. Get the second edition if you
have the choice.

**How to use it:** read it linearly, and do not skip the chapters that feel slow. The
relay-logic chapters in the middle are where the payoff is built.

### [Crash Course Computer Science](https://www.youtube.com/playlist?list=PL8dPuuaLjXtNlUrzyH5r6jN9ulIgZBpdo)

A recorded lecture series with a coherent curriculum, which is why it qualifies at this
tier rather than Tier 3 — see the
[video rule](../../../docs/resource-tiers.md#rules).

Use it for **orientation and breadth**: 40 short episodes covering the whole field, which
gives you a map of what exists before you go deep on anything. Then read Petzold for depth.

**How to use it without wasting the time:** watch at most two episodes per session, and
write down what you did not understand. Video creates a strong feeling of comprehension
that does not survive a blank page — it is the most common on-ramp to tutorial hell.
Writing down your confusions is what converts watching into learning.

### [Latency Numbers Every Programmer Should Know (interactive)](https://colin-scott.github.io/personal_website/research/interactive_latency.html)

The memory hierarchy as numbers you can see, compare, and watch change across hardware
generations.

**Look at this after taking your own measurements in the project**, not before. If you read
the table first you will memorise it; if you measure first and then compare, you calibrate
against your own data, which is what actually sticks. The ratios are what matter — the
absolute figures drift with hardware.

---

## Tier 3 — Practical

Concrete, current, and expected to age.

### [Ben Eater — 8-bit computer on breadboards](https://eater.net/8bit)

A CPU built by hand from discrete logic chips, on video, over many episodes.

Watch the first few if the fetch-decode-execute loop still feels abstract after Petzold —
seeing a clock signal physically step a real machine through instructions makes it
concrete in a way text cannot.

**Optional, and a genuine rabbit hole.** The full series is dozens of hours and goes far
past anything you need. The project does not require it. Listed because for some people
this is the thing that makes it click, and for those people it is worth every hour.

---

## What is deliberately not here

Some notable absences, with reasons — the reasons are more useful than more links.

**"Learn X in Y days" material.** Nothing about how computers work can be usefully
compressed to a week, and the framing trains the wrong expectation.

**Operating systems textbooks.** *Operating Systems: Three Easy Pieces* is excellent and
free, and it belongs to `operating-systems-fundamentals` at Level 3. Reading it now means
reading about page tables with no mental model to attach them to.

**Computer architecture textbooks.** Hennessy and Patterson is the standard reference and
is aimed at people designing processors. Not your problem for several years.

**Blog posts explaining "how a computer works".** There are thousands. Almost all of them
are a worse version of Petzold's first five chapters, and the effort of finding the good
ones exceeds the effort of just reading Petzold.

**Tutorials.** This topic has nothing to build in code, so there is nothing for a tutorial
to walk you through. The [project](../../../projects/machine-anatomy/README.md) is the
practical work.

---

## If you only have three hours

1. Watch two episodes of Crash Course (hardware and CPU). — 25 minutes
2. Do the memory hierarchy measurement in
   [practical.md](practical.md#watch-the-memory-hierarchy-happen), predicting first.
   — 30 minutes
3. Do exercises 1–10 in [exercises.md](exercises.md). — 60 minutes
4. Write the answer to exercise 25 — explaining a power cut to a non-technical person.
   — 30 minutes

That leaves you with a working model, measured numbers, and one thing you can explain. It
is not the full topic, but it is honest progress, and it is far better than three hours of
reading.
