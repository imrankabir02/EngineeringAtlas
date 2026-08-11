# How computers work — exercises

Small, verifiable drills. Each has a checkable answer, and each takes minutes rather
than hours.

**Predict before you run.** Write your prediction down for every exercise marked
**[predict]**. Comparing the prediction with the result is where the learning is; skipping
it turns the exercise into typing.

[← How computers work](README.md) · [Practical](practical.md) ·
[Projects](projects.md)

---

## Inventory

**1.** Find your CPU model, physical core count, and logical processor count. Are the
last two the same? If not, explain the difference in one sentence.

**2.** Find the size of your L1 data cache and your total RAM. Compute the ratio. Write
it down — you now know how much of your RAM fits in the fastest layer.

**3.** Determine whether your main storage device is solid state or rotating, and state
the command that told you.

**4.** List which components in your machine lose their contents when power is removed,
and which do not. For each, say why in one clause.

**5.** Run `free -h` and identify how much RAM is currently holding cached file
contents. Explain why `free` being small is not a problem.

---

## The hierarchy

**6. [predict]** How long to read 1 GB from your disk when it is not cached? Write a
number, then measure with `dd`. Record how wrong you were and in which direction.

**7. [predict]** Read the same 1 GB file a second time immediately. Predict the
throughput first. Then explain the result using the phrase "page cache".

**8. [predict]** Estimate how long a 40 KB web page takes to arrive from a server
150 ms away, ignoring bandwidth entirely. Then compare that to the time to read 40 KB
from your SSD. What is the ratio, and what does it imply about where data should live?

**9.** Using only the latency table in
[concepts.md](concepts.md#rough-latency-numbers), decide which is faster and by roughly
how much: reading 1 MB sequentially from RAM, or reading 1 MB sequentially from an SSD.
Then verify with `dd` (write to `/dev/null` for the SSD case, read from `/dev/zero` for
the memory case).

**10.** Take the "if a cycle were one second" table from
[fundamentals.md](fundamentals.md#why-the-machine-is-built-in-layers) and add one row:
an intercontinental network round trip. Work out the scaled figure yourself.

---

## Processes

**11.** List your running processes. Find one you did not start and work out what it is
for. Search for its name if needed.

**12.** Identify the process using the most RAM. Use the `RSS` column, not `VSZ`, and
state why.

**13.** Start `sleep 300` in the background, find its PID, and stop it with `kill`.
Confirm it is gone.

**14.** Run `top` and watch for thirty seconds. Note one process whose CPU usage
changes and one that stays at zero. What does a process at 0% CPU for thirty seconds
tell you about what it is doing?

**15.** Start two `sleep 300` processes. Confirm both appear with different PIDs. Kill
only one and verify the other survives — you have just demonstrated process isolation.

---

## Files and bytes

**16.** Create a file containing exactly the text `hello` with no trailing newline.
Confirm its size is 5 bytes. Then create one *with* a newline and confirm it is 6.
Which byte value is the newline?

**17.** View the raw bytes of your 5-byte file. Match at least two bytes to the
characters you typed, using ASCII values.

**18.** Copy a text file to a name ending in `.png`. Run `file` on it. Explain in one
sentence why `file` gives the right answer while the name lies.

**19. [predict]** Create a file containing a single non-ASCII character — an accented
letter or an emoji. Predict its size in bytes, then check. Explain any surprise using
UTF-8.

**20.** Find a real image or PDF on your machine and look at its first 8 bytes with
`xxd`. Search for what those bytes signify. You have found a magic number.

---

## Break it

Each of these fails on purpose. **Predict the outcome in writing first.** Use `/tmp` or
a scratch directory, and clean up immediately.

**21. Fill the disk.** In a scratch directory, create a large file until the filesystem
is nearly full, then try to save something else. Record the **exact** error message.
Then delete the filler.

```console
$ mkdir -p /tmp/scratch && cd /tmp/scratch
$ df -h .                      # check headroom FIRST
$ dd if=/dev/zero of=filler bs=1M count=<leave several GB free>
$ echo hi > another.txt        # record what happens
$ rm filler                    # clean up immediately
```

Leave several gigabytes free. A genuinely full disk can stop your editor and parts of
the system from working.

**22. Exhaust memory.** Watch `free -h` in one terminal while a program allocates
memory steadily in another. Note the **order** of events: memory fills, swap starts,
everything slows, and eventually something is killed. That sequence — degradation, then
failure — is how most resource exhaustion behaves, and recognising it early is a real
debugging skill.

**23. Lie about a file type.** Covered in exercise 18. Now try the reverse: rename a
real PNG to `.txt` and open it in a text editor. Explain what you see in terms of bytes
being interpreted under the wrong assumption.

**24. Kill something important-ish.** Start a text editor, find its PID, kill it, and
observe that unsaved work is gone. Then explain, in one sentence, where that work was
and why it did not survive.

---

## Explain

These are the hardest exercises here, and the most valuable. Write the answers down —
writing is where you find out which parts you were only pattern-matching.

**25.** Explain to someone with no technical background why a computer loses unsaved
work in a power cut. You may not use "memory" as though the word explains itself.

**26.** Explain why opening a large file is faster the second time. Two paragraphs
maximum.

**27.** Someone says "my computer is slow." Name three different resources that could
be exhausted, and for each, one command that would check it.

**28.** Explain why making data survive is necessarily slower than changing it, rather
than being slower because of an implementation shortcoming.

**29.** A colleague proposes storing session data on disk instead of in memory "because
it is safer." Using the latency ratios, state what that costs per request and what it
buys. Do not conclude that they are wrong — state the trade-off.

---

## Answers to check yourself

<details>
<summary>Expand after attempting</summary>

**1.** Logical processors exceed physical cores when hyper-threading (SMT) is enabled —
each core presents as two logical CPUs, sharing execution resources. Two logical CPUs on
one core do not deliver twice the throughput.

**5.** Cached file contents are instantly reclaimable. The OS hands that memory to a
program the moment one asks. Unused RAM does nothing useful, so a healthy system's
`free` is small; `available` is the meaningful figure.

**8.** A 150 ms round trip versus roughly 100 µs from an SSD is a factor of about 1,500.
Implication: a network fetch you could have avoided costs more than a thousand local
reads, which is why caching at the edge exists at all.

**12.** `VSZ` counts reserved address space, much of which is never backed by physical
memory. `RSS` counts pages actually resident in RAM.

**14.** A process at 0% CPU is blocked — waiting for input, a timer, a network packet, or
a disk read. Most processes on a machine are waiting almost all the time, which is why a
machine with 300 processes and 4 cores works fine.

**16.** Newline is byte value 10 (`0a` in hex), historically "line feed".

**19.** An accented Latin character is 2 bytes in UTF-8; most emoji are 4. The file may
also be 3 or 5 bytes with a trailing newline. If you predicted 1, you have found the
reason "length" is ambiguous for text: bytes, code points, and user-perceived characters
are three different counts, and confusing them is a durable source of bugs.

**24.** The work was in RAM, held by the process. Killing the process destroys its
memory, and nothing wrote the data to storage, so nothing persisted.

**28.** Survival requires the bytes to reach a medium that holds state without power.
Such media are physically slower than RAM — that is why they retain data at all. The
gap is a property of the physics, not of the software.

</details>

---

## Next

[projects.md](projects.md) — the [machine-anatomy](../../../projects/machine-anatomy/README.md)
investigation, which is the `build` gate for this topic.
