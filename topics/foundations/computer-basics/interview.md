# How computers work — interview

What competent discussion of this topic sounds like, and what a shallow answer reveals.

**This is not a question bank.** Memorised answers fail immediately under a follow-up
question, and the follow-up is where the assessment actually happens. What follows are
*discussion shapes*: the topics, what a good answer contains, and the tells that separate
understanding from recall.

[← How computers work](README.md) · [Concepts](concepts.md) ·
[Advanced](advanced.md)

---

## Where this topic actually comes up

Almost never as a direct question, and constantly as an assumption.

Nobody interviewing for a software role asks "what is RAM?". But when you are asked why
a service is slow, or whether to add a cache, or what happens if the process crashes
mid-write, your answer is built entirely out of this topic. Interviewers hear the
difference immediately, without asking about hardware once.

The signal they are reading: **do you reason about mechanisms, or do you pattern-match on
vocabulary?**

---

## Discussion 1 — "Why is reading from a database slower than reading from a variable?"

**A shallow answer:** "Because databases are slower." (Restates the question.)

**A competent answer** names a mechanism and a magnitude:

> A variable is in the process's memory, roughly 100 nanoseconds away. A database read
> usually leaves the process — a network round trip, maybe half a millisecond in the same
> datacentre — and on a cache miss the database itself reads from storage, another
> ~100 microseconds. So we are comparing nanoseconds to hundreds of microseconds or
> milliseconds: three to four orders of magnitude. It buys durability and sharing, which a
> variable cannot give you.

**The tell:** competent answers include a *number or a ratio*, and name what the slowness
buys. "It's a network call" is halfway there; "it's a network call, so we've gone from
nanoseconds to milliseconds, in exchange for the data surviving a restart" is the whole
answer.

**Follow-up you should survive:** *"When would reading from a variable be wrong?"*
When the value must survive a crash, or when several processes must agree on it. That is
the real trade-off, and noticing it unprompted is the difference between Level 0 knowledge
and Level 1 judgment.

---

## Discussion 2 — "What happens when a program crashes before saving?"

**A shallow answer:** "The data is lost."

**A competent answer** explains where it was:

> The data was in the process's memory, which the operating system reclaims when the
> process ends. Nothing wrote it to storage, so nothing persisted. What is subtler is that
> "wrote it to storage" is not binary — the write may have gone to the OS page cache and
> be waiting to be flushed, in which case the program was told it succeeded and the data
> can still be lost in a power failure. That gap is why `fsync` exists and why databases
> keep write-ahead logs.

**The tell:** mentioning the gap between "the write returned" and "the bytes are durable".
Most people at this level do not know that gap exists, and knowing it signals that you
have thought about durability rather than assumed it.

You do not need to know how `fsync` works. Knowing the problem it solves is the whole
signal.

---

## Discussion 3 — "Your machine has 16 GB of RAM and `free` shows 500 MB free. Is that a problem?"

This is a small trap, and it is a good one.

**A shallow answer:** "Yes, it's nearly out of memory."

**A competent answer:**

> Probably not. Most of that RAM is likely holding cached file contents, which the OS
> reclaims instantly when a program needs memory. The number to look at is `available`,
> not `free`. Unused RAM is wasted RAM, so a healthy long-running system has very little
> `free`. What *would* worry me is heavy swap usage, because that means memory pressure is
> real and pages are going to disk — a thousand times slower — which is why a swapping
> machine feels broken even though nothing has failed.

**The tell:** distinguishing `free` from `available`, and knowing that swap activity, not
low `free`, is the alarming signal.

---

## Discussion 4 — "How would you find out why a machine got slow?"

Level 0 cannot be expected to debug production. It *can* be expected to enumerate
resources.

**A competent answer** names the exhaustible resources and how to check each:

| Resource | Symptom | Check |
|---|---|---|
| CPU | Everything slow, load average high | `top`, `uptime` |
| Memory | Slow with heavy disk activity | `free -h`, swap columns |
| Disk space | Writes fail, programs will not start | `df -h` |
| Disk throughput | Slow I/O, high wait time | `iostat`, `top`'s `wa` figure |
| Network | Slow only for remote things | `ping`, `ss` |

**The tell:** enumerating *before* guessing. The weak version picks one cause and pursues
it; the strong version lists candidates and then narrows with evidence. That habit is the
whole of debugging, and it is visible from the first sentence.

---

## Discussion 5 — "Why does the same file open faster the second time?"

**A competent answer** names the page cache, explains it was not requested, and draws the
general conclusion:

> The OS kept the file's contents in RAM after the first read, because RAM was free and
> the file might be needed again. The second read never touches storage. Nobody asked for
> this — it is automatic. It is also the same idea as every cache in every system:
> keep what you needed recently closer, because reaching further away costs orders of
> magnitude more.

**The tell:** generalising from the observation to caching as a principle. That connection
is what makes this topic worth learning, and stating it unprompted signals you learned the
idea rather than the fact.

---

## Discussion 6 — "Is `photo.jpg` an image?"

**A competent answer:** "Not necessarily. A file is bytes plus a name; the extension is a
convention that helps programs guess. `file` and any careful program read the leading
bytes — the magic number — instead of trusting the name. Which is also a security matter:
anything that trusts an uploaded filename to decide how to handle content has a
vulnerability."

**The tell:** the security observation. It is unprompted, correct, and shows you thought
about consequences rather than reciting a definition.

---

## Shallow-answer tells, generally

What interviewers register as weak signals, in roughly increasing severity:

**Vocabulary without mechanism.** "It's an I/O bottleneck" with no account of what is
waiting for what. Naming a category is not a diagnosis.

**No magnitudes.** "Memory is faster than disk" is true and nearly content-free. "About a
thousand times faster" shows you have a model that can make predictions.

**Certainty where there should be a question.** "I'd add a cache" before asking about the
read/write ratio or the access distribution. Strong candidates ask what the workload looks
like.

**Confusing "it worked" with "it is correct".** Particularly around durability. The write
returned; that is not the same as the data being safe.

**Never saying "I don't know, here's how I'd find out."** This is the single most
underrated answer at every level. "I don't know the exact figure, but I'd measure it with
`dd` and compare cold to warm" is a *strong* answer. Guessing confidently is a weak one.

---

## Practising this properly

The `explain` gates in [`topic.yml`](topic.yml) are the real preparation, and they are
harder than they look:

- Explain to a non-technical person why unsaved work vanishes in a power cut — without
  using "memory" as though the word explains itself.
- Explain why a large file opens faster the second time, in two paragraphs.

Do these **out loud, to an actual person**, or written down. Rehearsing in your head skips
the step where you discover which parts you cannot articulate, which is the only part that
matters.

Then, per [philosophy.md](../../../docs/philosophy.md#anti-patterns): do not grind question
banks. Derive from mechanisms. Someone who can reason from the memory hierarchy answers
questions they have never seen, and that is what is being tested.
