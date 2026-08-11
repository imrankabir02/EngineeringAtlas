# How computers work — practical

Look at your own machine. Every concept in this topic is observable with commands you
already have.

[← How computers work](README.md) · [Fundamentals](fundamentals.md) ·
[Concepts](concepts.md) · [Exercises](exercises.md)

---

## Getting a terminal

You need a text interface to your machine. Not because it is faster (though it is), but
because it **shows you what is happening** — a graphical file manager hides the
filesystem behind pictures, and right now you want to see the filesystem.

| System | How |
|---|---|
| Linux | Your desktop has a Terminal application. `Ctrl`+`Alt`+`T` often works |
| macOS | Terminal.app, in Applications → Utilities. Or `Cmd`+Space, type "terminal" |
| Windows | Install WSL (Windows Subsystem for Linux) and use that. Everything below assumes a Unix-like system, and WSL gives you a real Linux |

Windows users: WSL is worth the fifteen minutes. Almost all servers run Linux, so every
command you learn there transfers to real work. PowerShell is a fine shell but a
different world, and learning both at once is unnecessary friction.

You will see a **prompt** — usually ending in `$` — waiting for a command. Type, press
Enter, read the output. That is the entire interaction model.

In the examples below, `$` marks the prompt. Do not type it.

---

## What is in this machine

### Everything at once

```console
$ uname -a
Linux thinkpad 6.8.0-45-generic #45-Ubuntu SMP x86_64 GNU/Linux
```

Kernel, version, architecture, hostname. `x86_64` means a 64-bit Intel/AMD processor;
`aarch64` or `arm64` means ARM, which is what Apple Silicon and most phones use.

### The processor

```console
$ lscpu | head -20
```

Look for:

| Field | Means |
|---|---|
| `Model name` | Which processor, and its base clock speed |
| `CPU(s)` | Total logical processors the OS can schedule on |
| `Core(s) per socket` | Physical cores — the number that genuinely run at once |
| `Thread(s) per core` | 2 means hyper-threading: each core presents as two logical CPUs |
| `L1d/L1i/L2/L3 cache` | The cache layers from [fundamentals.md](fundamentals.md). Notice how small L1 is |

The `L1d` figure is worth a pause. It is often 32 KB *per core* — a few thousand times
smaller than your RAM, and the fastest storage in the machine. That size constraint is
why access patterns matter.

On macOS:

```console
$ sysctl -n machdep.cpu.brand_string
$ sysctl -n hw.physicalcpu hw.logicalcpu
```

### Memory

```console
$ free -h
               total        used        free      shared  buff/cache   available
Mem:            15Gi       4.2Gi       1.1Gi       0.5Gi        10Gi        11Gi
Swap:          2.0Gi          0B       2.0Gi
```

The interesting column is **`buff/cache`**. In this example, 10 GB of RAM holds cached
file contents — the page cache from [fundamentals.md](fundamentals.md#the-consequence-caching-is-unavoidable).

This surprises people: "only 1.1 GB free" looks alarming and is not. That memory is
being used for something useful (caching files) and will be handed to a program the
instant one asks. **`available` is the number that matters**, not `free`. Unused RAM is
wasted RAM, so a healthy system's `free` figure is small.

`Swap` is disk space used as overflow when RAM runs out. Because disk is ~1000× slower,
a system that is swapping heavily feels broken even though nothing has failed. You will
observe this in [exercises.md](exercises.md).

macOS: `vm_stat`, plus Activity Monitor for a readable view.

### Storage

```console
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1p2  468G  213G  232G  48% /

$ lsblk -o NAME,SIZE,ROTA,TYPE,MODEL
NAME        SIZE ROTA TYPE MODEL
nvme0n1     476G    0 disk Samsung SSD 980
```

`ROTA` is the useful column: `1` means a rotating disk, `0` means solid state. A device
named `nvme` is an SSD on a fast interface. The distinction matters because a spinning
disk pays a ~10 ms mechanical seek for random access, while an SSD does not — a 100×
difference for scattered reads, and the reason database performance advice from 2008
reads strangely today.

---

## Watch the memory hierarchy happen

This is the most valuable ten minutes in the topic.

Create a 1 GB file:

```console
$ cd /tmp
$ dd if=/dev/zero of=testfile bs=1M count=1024
1073741824 bytes (1.1 GB, 1.0 GiB) copied, 0.8 s, 1.3 GB/s
```

`dd` copies bytes. `if` is input file, `of` is output file, `bs` is block size, `count`
is how many blocks. `/dev/zero` is a special file that produces endless zero bytes.

**Predict now, in writing:** how long to read that file back? And a second time?

```console
$ sync                                    # flush pending writes
$ dd if=testfile of=/dev/null bs=1M       # read #1
1073741824 bytes (1.1 GB) copied, 0.42 s, 2.6 GB/s

$ dd if=testfile of=/dev/null bs=1M       # read #2, immediately
1073741824 bytes (1.1 GB) copied, 0.09 s, 12 GB/s
```

The second read is several times faster. **Nothing about the file, the command, or the
disk changed.** The operating system kept the file's contents in RAM after the first
read, so the second read never touched storage.

That is the page cache, and you just measured the RAM-versus-disk gap on your own
hardware without writing a line of code.

`/dev/null` discards everything written to it, so you are measuring read speed and not
write speed.

Clean up:

```console
$ rm /tmp/testfile
```

**Note on honesty:** on Linux, `echo 3 > /proc/sys/vm/drop_caches` (as root) clears the
page cache for a properly cold measurement. Without it, your "read #1" may be partly
warm already because `dd` wrote the file moments ago. If you can drop caches, your
numbers will be cleaner — and noticing that your measurement setup affects your result
is itself a Level 3 skill arriving early.

---

## What is running

```console
$ ps aux | head
USER   PID %CPU %MEM    VSZ   RSS COMMAND
root     1  0.0  0.1 168404 12608 /sbin/init
root   412  0.0  0.2  92140 18432 /lib/systemd/systemd-journald
alice 2891 12.3  4.8 3892104 782336 /usr/lib/firefox/firefox
```

| Column | Means |
|---|---|
| `PID` | Process ID — the number that identifies this running program |
| `%CPU` | Share of processor time recently |
| `RSS` | Resident Set Size — actual RAM this process is using, in KB. **The useful memory column** |
| `VSZ` | Virtual size — address space reserved, usually much larger than RSS and rarely what you want |

The `VSZ` versus `RSS` distinction confuses everyone at first. A process can reserve
huge amounts of address space without using it; `RSS` is what is really occupying RAM.
Full explanation waits for `operating-systems-fundamentals` — for now, read `RSS`.

Live view:

```console
$ top          # press q to quit, M to sort by memory, P by CPU
$ htop         # nicer, if installed
```

Try it yourself:

```console
$ sleep 300 &            # start a program in the background
[1] 4823
$ ps aux | grep sleep    # find it
$ kill 4823              # stop it deliberately
```

You have just started a process, observed it, and terminated it. That is the entire
process lifecycle from outside.

---

## Files are bytes

```console
$ cd /tmp
$ echo -n "hello" > small.txt
$ ls -l small.txt
-rw-r--r-- 1 alice alice 5 Aug 11 10:32 small.txt
```

Five bytes for five characters. `echo -n` suppresses the trailing newline; without
`-n` you would see 6, because the newline is a real byte (value 10).

Look at the actual bytes:

```console
$ xxd small.txt
00000000: 6865 6c6c 6f                             hello
```

`68` is hexadecimal for 104, which is `h` in ASCII. `65` is 101, `e`. You are looking
at the encoding agreement from [concepts.md](concepts.md#binary-and-character-encoding).

Now prove that extensions are conventions:

```console
$ cp small.txt small.png
$ file small.png
small.png: ASCII text, with no line terminators
```

`file` ignores the name and reads the bytes. It correctly reports text. Try opening
`small.png` in an image viewer: it will fail, because the viewer reads the bytes too,
looks for the PNG magic number (`89 50 4E 47`), and does not find it.

```console
$ rm /tmp/small.txt /tmp/small.png
```

---

## Where these numbers come from

On Linux, the kernel publishes facts about the machine as readable files:

```console
$ cat /proc/cpuinfo | head -20      # what lscpu formats
$ cat /proc/meminfo | head -10      # what free formats
$ cat /proc/loadavg                 # load average
```

`lscpu` and `free` are just readers of these files. Knowing that means you are never
stuck when a convenience command is missing, and it is the beginning of the mental habit
of asking *where does this tool get its information?* — which is how you debug tools
that lie.

The authoritative reference is
[`man 5 proc`](https://man7.org/linux/man-pages/man5/proc.5.html). Reading a man page
is a skill; start now:

```console
$ man 5 proc          # q to quit, / to search, space to page down
```

---

## A safety note on breaking things

The gates ask you to fill a disk and exhaust memory. Do both **in `/tmp` or a scratch
directory**, and clean up immediately.

A genuinely full disk can prevent programs — including your editor, your shell, and
parts of the operating system — from starting, because many need to write temporary
files. Leave several gigabytes of headroom, and delete your filler file as soon as you
have recorded the error message. Deletes still work when writes fail, so recovery is
always available.

This caution is itself the lesson: you are learning to break things in an environment
where breaking them is cheap. That is what a scratch directory, a test environment, and
a staging cluster are all for.

---

## Command reference

Everything used in this topic:

| Command | Does |
|---|---|
| `uname -a` | OS, kernel, architecture |
| `lscpu` | Processor details including cache sizes |
| `free -h` | Memory, including the page cache |
| `df -h` | Filesystem space |
| `lsblk` | Block devices; `ROTA` distinguishes SSD from spinning disk |
| `ps aux` | Process snapshot |
| `top` / `htop` | Live process view |
| `kill <pid>` | Stop a process |
| `dd` | Copy bytes; useful for crude throughput measurement |
| `ls -l` | File listing with sizes |
| `xxd` / `hexdump -C` | Raw bytes of a file |
| `file` | Guess a file's type from its content, not its name |
| `cat /proc/...` | Read kernel-published facts directly (Linux) |
| `man <n> <name>` | Read the manual |

---

## Next

[exercises.md](exercises.md) — drills that verify each concept, then the
[machine-anatomy project](projects.md).
