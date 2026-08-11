# How computers work — fundamentals

The machine from first principles: what it does, why it is built in layers, and what
that costs you.

[← How computers work](README.md) · [Concepts](concepts.md) ·
[Practical](practical.md)

---

## A computer does one thing

It follows instructions on data. Very fast, and very literally.

That is the whole job. Everything else — operating systems, the internet, databases,
machine learning — is built on a machine that repeats this loop billions of times per
second:

```text
1. Fetch the next instruction
2. Work out what it says
3. Do it
4. Repeat
```

The instructions are extremely simple. Add two numbers. Copy a value from here to
there. If this number is zero, jump to a different instruction. There is no
instruction for "load the web page" or "check spelling" — those are millions of the
simple ones, arranged carefully.

Two consequences worth sitting with:

**The computer has no judgment.** It does what the instructions say, including when
they are wrong. Every bug you will ever write is the machine doing exactly what you
said. This is genuinely good news: it means every bug has a cause you can find.

**A program is data.** The instructions are numbers stored in memory, no different in
kind from the numbers they operate on. That is why you can copy a program, email it,
version it, and — importantly — why a program can generate another program. Compilers
do exactly that.

---

## The parts

Three things you cannot avoid knowing about.

### The processor (CPU)

The part that does the fetch-decode-execute loop. Fast — billions of steps per second
— and it holds almost nothing. It has a handful of tiny slots called **registers**
(typically 16 to 32 of them, each holding a single number). That is the CPU's entire
working space.

A modern CPU has several **cores**, each running its own loop. Four cores means four
instructions genuinely happening at the same moment. This is where "doing two things
at once" becomes physically real rather than an illusion, and it is why concurrency
becomes a topic later.

### Memory (RAM)

Where the program and the data it is working on live while it runs. Much larger than
the registers — billions of slots rather than dozens — and much slower to reach.

**RAM forgets everything when power is removed.** Remember this; half of this topic
follows from it.

### Storage (disk, SSD)

Where things persist. Much larger than memory, much slower, and it **keeps its
contents without power**.

That is the entire difference that matters right now: memory is fast and forgetful,
storage is slow and remembers.

---

## Why the machine is built in layers

Here is the constraint that shapes everything.

Fast storage is expensive and physically small. Slow storage is cheap and large. There
is no technology that is simultaneously fast, large, and cheap — not as an engineering
oversight, but because speed comes from being physically close to the processor and
simple, and there is a limited amount of "close".

So machines are built as a **hierarchy**: a small amount of very fast storage, backed
by a larger amount of slower storage, backed by a larger amount of slower storage
still.

```text
                     size            time to reach       ratio vs registers
  registers          ~1 KB           <1 ns               1×
  CPU cache          ~1-64 MB        ~1-40 ns            ~10×
  RAM                ~8-128 GB       ~100 ns             ~100×
  SSD                ~0.5-4 TB       ~100,000 ns         ~100,000×
  network (same DC)  effectively ∞   ~500,000 ns         ~500,000×
  network (global)   effectively ∞   ~150,000,000 ns     ~150,000,000×
```

Do not memorise the digits. **Memorise the shape**, and one anchor: RAM is roughly a
hundred nanoseconds, an SSD is roughly a hundred microseconds — a thousand times
slower — and a network round trip across the world is milliseconds, another thousand
times slower again.

To make the ratios feel real, scale them up so one CPU cycle is one second:

| Real | If a cycle were 1 second |
|---|---|
| Read from a register | 1 second |
| Read from CPU cache | ~10 seconds |
| Read from RAM | ~2 minutes |
| Read from SSD | ~1.5 days |
| Round trip to a server across the world | ~5 years |

This table is the single most useful thing in the topic. When someone says "just fetch
it from the database," you now know they said "wait a day and a half instead of two
minutes."

You will measure these ratios yourself in the
[machine-anatomy project](../../../projects/machine-anatomy/README.md). Your numbers
will differ from the table. Yours are the ones that matter.

---

## The consequence: caching is unavoidable

If reaching down a layer is a hundred times slower, then anything you had to reach for
once and might need again is worth keeping closer.

That is **caching**, and it is not a technique somebody invented. It is the only
possible response to the hierarchy, which is why it appears independently at every
level of every system:

- The CPU keeps recently used memory in its cache.
- The operating system keeps recently read file contents in RAM — the **page cache**.
- Your browser keeps downloaded images on disk.
- A web application keeps database results in memory.

You can observe the page cache with no special tools. Read a large file, time it. Read
it again, time it. The second read is dramatically faster because the operating system
kept a copy in RAM, unasked, because RAM was free and you might want it again.

Nothing in your program changed. The data just moved closer.

Caching also creates the problem it always creates: **you now have two copies, and one
of them can be wrong.** That is a Level 3 topic and you will spend real time on it. For
now, notice only that the problem exists and that it was created by the solution.

---

## The consequence: saving is slow, and that is the point

Memory forgets. Storage remembers. Storage is slower.

Therefore *making something survive is slower than changing it* — necessarily, not
incidentally. The bytes have to reach a physical medium that holds its state without
power, and that takes a thousand times longer than changing a value in RAM.

This is why:

- A program can lose unsaved work. The work was only ever in RAM.
- Databases are slower than variables. They are guaranteeing survival.
- "Did it save?" is a real engineering question with a precise meaning — did the bytes
  reach persistent storage, or are they still in a fast, forgetful layer that intends
  to write them later?

That last case is a genuine and common source of data loss. Storage devices and
operating systems both buffer writes in RAM to make them appear fast, then write for
real slightly later. If power is lost in that window, the data is gone even though your
program was told the write succeeded. Every serious storage system has machinery for
this problem, and you will meet it again in `filesystems-and-storage` and
`transactions-and-isolation`.

---

## Many programs at once

Your machine is running hundreds of programs right now. It has a handful of cores. Both
statements are true.

The processor switches between programs thousands of times per second, giving each a
slice. Each switch is fast enough that everything appears to run continuously. Programs
that genuinely need to run at the same instant use different cores.

A running program is called a **process**, and each process has its own region of
memory that other processes cannot read. That isolation is why one crashing program
does not take the machine with it, and why a bug in your text editor cannot read your
banking password out of your browser.

Who does the switching and enforces the isolation? A program whose job is managing all
the other programs: the **operating system**. It decides who runs, hands out memory,
owns access to the disk and the network, and stops programs interfering with each
other.

That is as much as you need today. `operating-system-basics` takes it further, and
`operating-systems-fundamentals` at Level 3 does it properly.

---

## Everything is numbers

At the bottom, the machine stores only numbers, in the simplest possible form: each
slot is either on or off. One such slot is a **bit**. Eight of them are a **byte**,
which can therefore hold 2⁸ = 256 different values.

That is why 256 appears everywhere in computing, and why a byte is the standard unit of
"a small amount of data."

Text is numbers by agreement. Somebody decided that 72 means `H` and 105 means `i`, and
everybody agreed. That agreement is a **character encoding**. ASCII covered English in
one byte per character; Unicode covers essentially every writing system, and UTF-8 is
the encoding that represents it — using one byte for ASCII characters and up to four for
others.

The practical consequence, which you will meet within weeks: **a file has no inherent
type.** A file is a sequence of bytes. `photo.jpg` and `notes.txt` are the same kind of
thing; the extension is a hint to programs about how to interpret the bytes, and it can
be wrong. Renaming a text file to `.png` does not make it an image. It makes it a text
file with a misleading name, and the image viewer will read the bytes, find they make
no sense as an image, and complain.

You will verify this yourself in [exercises.md](exercises.md).

---

## Putting it together

```text
     A program is instructions and data.
                    ↓
     Instructions and data must be somewhere the CPU can reach.
                    ↓
     Reaching further away takes longer, by large factors.
                    ↓
     Fast storage is small and expensive; large storage is slow.
                    ↓
     So the machine is a hierarchy: registers → cache → RAM → disk → network.
                    ↓
     Keep what you need close.                    → caching, everywhere
     Only the slow layers survive power loss.     → persistence is slow
     Many programs share one hierarchy safely.    → the operating system
```

Every claim in the rest of this repository about why something is fast, slow, durable,
or lost traces back to this diagram. When you are confused about performance three
years from now, come back and ask: *where is the data, and how far does it have to
travel?*

---

## Next

[concepts.md](concepts.md) for the inventory and how deeply to learn each part, then
[practical.md](practical.md) to look at your own machine.
