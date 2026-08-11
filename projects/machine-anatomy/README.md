# Anatomy of your own machine

**Level 0** · validates [`computer-basics`](../../topics/foundations/computer-basics/README.md)
· no programming required

You are going to investigate the computer in front of you until you can draw it
from memory and defend every number you write down.

This produces a report, not code. That is deliberate: at Level 0 the bottleneck is
not typing, it is that the machine is still a black box. Every performance claim
you meet for the next five levels rests on the facts you are about to measure
yourself.

---

## Why this project exists

You will spend years being told that "memory is fast and disks are slow," that
"a network call is expensive," that "your program is one of many processes." Those
are all true, and repeating them is worth almost nothing.

Measuring them once, on your own machine, with your own hands, is worth a great
deal — because from then on the numbers are yours. When someone later claims a
cache saves 200 ms, you will have a felt sense of what 200 ms buys.

The second reason: **you will predict before you measure.** The gap between your
prediction and reality is the most useful information this project produces, and
it is the habit that Levels 3 through 5 are built on.

---

## Setup

You need a terminal and a text editor. Nothing else.

Create a working directory and a report file:

```console
$ mkdir ~/machine-anatomy && cd ~/machine-anatomy
$ touch report.md
```

Everything you record goes in `report.md`. Every number gets the command that
produced it, so a reader — including you in six months — can reproduce it.

**Before each measurement, write your prediction in the report first.** Do not go
back and edit predictions after seeing the result. Being wrong is the point.

---

## Stage 1 — Inventory

Find out what is actually in your machine.

What you are looking for:

| Component | What you want | Why it matters later |
|---|---|---|
| CPU | Model, number of cores | Determines how many things truly run at once |
| RAM | Total capacity, how much is free | Where running programs and cached files live |
| Storage | Type (SSD/NVMe/HDD), capacity, free space | Where data survives a power loss |
| OS | Name and version | Decides what the syscall interface looks like |

Useful starting points — you may need to search for the equivalent on your system:

```console
$ uname -a                      # OS and kernel
$ lscpu                         # CPU details (Linux)
$ free -h                       # memory in human-readable units (Linux)
$ df -h                         # filesystem usage
$ lsblk -o NAME,SIZE,ROTA,TYPE  # block devices; ROTA=1 means spinning disk
```

On macOS: `sysctl -n machdep.cpu.brand_string`, `vm_stat`, `diskutil list`.

Finding the right command is part of the exercise. You will spend your career
looking things up; start now.

**Record in your report:**

1. Each component, its value, and the command you used.
2. One sentence per component: what it does, and what running out of it would mean.
3. Which components lose their contents when power is removed, and which do not.
   Be specific about *why* — this distinction is the foundation of everything about
   persistence, databases, and durability.

---

## Stage 2 — Measure the hierarchy

This is the stage that matters most.

### Predict first

Write in your report, before running anything:

- How long do you think it takes to read 1 GB from RAM?
- How long from your disk?
- What ratio between them do you expect?

Commit to numbers. "I don't know" is not a prediction; guess anyway.

### Then measure

Create a 1 GB file:

```console
$ dd if=/dev/zero of=testfile bs=1M count=1024
```

Read it from disk, with caches cleared as far as you are able:

```console
$ sync
$ dd if=testfile of=/dev/null bs=1M
```

Read it again, immediately:

```console
$ dd if=testfile of=/dev/null bs=1M
```

Note the throughput `dd` reports each time.

**The second read is dramatically faster. Explain why.** The answer is that the
operating system kept a copy of the file's contents in RAM after the first read,
because RAM was free and the file might be needed again. That copy is called the
**page cache**, and you have just observed caching happening without anyone asking
for it. You will meet this idea again in almost every topic on the map.

Now measure memory speed directly. On Linux:

```console
$ dd if=/dev/zero of=/dev/null bs=1M count=1024
```

This never touches storage at all — it is roughly a memory-bandwidth measurement.

**Record:** your predictions, the three measured throughputs, the commands, and
the ratio between memory and cold-disk reads. State how wrong your prediction was
and in which direction.

Typical results, for calibration only — **yours are the ones that matter**: a
modern NVMe drive reads in the low single-digit GB/s, a spinning disk closer to
100–200 MB/s, and memory bandwidth is often 10–20 GB/s. The gap between cold disk
and memory is commonly 10× to 100×; between memory and a *random* disk read, it is
far larger still.

Clean up when done:

```console
$ rm testfile
```

---

## Stage 3 — What is running

Your machine is running hundreds of programs. Look at them.

```console
$ ps aux | head -20     # snapshot of processes
$ top                   # live view; press q to quit
```

**Record:**

1. Five processes, with a sentence each on what you believe it does. Include at
   least one you did not start — those belong to the operating system and to
   background services.
2. Which process uses the most memory. Which uses the most CPU. Are they the same?
3. Start a program (for example `sleep 300 &`), find it in the process list by its
   process ID, then stop it deliberately with `kill <pid>`.

The concept you are building: a **process** is a running program with its own
memory that other processes cannot read. That isolation is provided by the
operating system, and it is the reason one crashing program does not take the
machine with it.

---

## Stage 4 — Where the bytes are

Files feel like documents. They are sequences of bytes.

```console
$ echo -n "hello" > small.txt
$ ls -l small.txt          # size in bytes
$ wc -c small.txt          # byte count
$ xxd small.txt            # raw bytes in hexadecimal, with characters alongside
```

**Record:**

1. The exact size in bytes, and why it is that number and not another. (What would
   `echo` without `-n` have added, and how many bytes is it?)
2. The hexadecimal value of at least one byte, matched to the character you typed.
   `h` is `68`. That mapping is a table someone agreed on — you are looking at a
   character encoding.
3. Copy the file to `small.png`, then try to open it in an image viewer. Record the
   error. Explain it in terms of the difference between a filename convention and
   the actual content of the file.

---

## Break it

Three deliberate failures. Predict each outcome in writing first.

**1. Run out of disk.** In a scratch directory, create files until the filesystem
is nearly full, then try to save something. Record the exact error. Then delete
them.

```console
$ mkdir ~/scratch && cd ~/scratch
$ dd if=/dev/zero of=filler bs=1M count=... # increase carefully
```

Stop well before the system becomes unusable, and delete `filler` immediately
after. On a machine you rely on, leave several gigabytes of headroom. A full disk
can prevent programs — including your editor and the system itself — from starting.

**2. Run out of memory.** Watch `free -h` or `top` while a program allocates memory
steadily. Note what the system does *before* it fails: it starts writing memory to
disk (swapping), everything gets slow, and eventually the OS kills something. That
sequence — degradation, then failure — is how most resource exhaustion behaves, and
recognising it is a Level 3 debugging skill you are getting an early look at.

**3. Lie about a file type.** Covered in stage 4. The lesson is that the system
mostly does not check, and the ones that do check are reading the bytes, not the
name.

---

## Done when

- [ ] `report.md` covers all four stages, with a command behind every number.
- [ ] Predictions are recorded *before* their measurements, unedited.
- [ ] You can explain why the second read of a file is faster than the first.
- [ ] You can draw the machine from memory — CPU, RAM, disk, and the paths between
      them — and place your measured speeds on the drawing.
- [ ] You can state which of your components forget everything when power is
      removed.

---

## Anti-patterns

**Copying specifications from a website.** The manufacturer's stated read speed is
not what your machine does under your filesystem with your caches. Measure.

**Measuring without predicting.** You lose the only calibration signal available,
and you learn a number instead of a habit.

**Treating this as trivia.** Nobody will ask you your RAM bandwidth. They will ask
you why the API is slow, and your answer will rest on the model you build here.

---

## Stretch

- Time reading the same file three times in a row and explain the pattern using
  the phrase "page cache".
- Find out how much of your RAM is currently holding cached file contents rather
  than program data. On Linux, compare the `free` and `available` columns of
  `free -h` and explain the difference.
- Draw the machine from memory, then check it against your report. What did you
  leave out? What you forget is what you have not yet internalised.

---

## Next

Return to [`computer-basics`](../../topics/foundations/computer-basics/README.md)
and work the gates, then continue to `what-programming-is`.
