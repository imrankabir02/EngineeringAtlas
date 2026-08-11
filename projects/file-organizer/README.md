# File organiser

**Level 1** · validates
[`programming-fundamentals`](../../topics/programming/programming-fundamentals/README.md)
· any language

A tool that reorganises a messy directory according to rules you define:

```console
$ organize ~/Downloads
DRY RUN - no changes made
  invoice.pdf          -> documents/invoice.pdf
  holiday.jpg          -> images/holiday.jpg
  archive.tar.gz       -> archives/archive.tar.gz
  weird thing          -> (no rule matched, left in place)
3 moves planned, 1 file unmatched. Re-run with --apply to execute.
```

---

## Why this project exists

[`cli-calculator`](../cli-calculator/README.md) taught you structure. This project
teaches something the calculator could not: **the outside world is hostile and your
mistakes are permanent.**

A calculator with a bug prints a wrong number. This program with a bug deletes
someone's files. That difference changes how you write code, and experiencing the
change is the point.

Three specific lessons, none of which can be learned from a tutorial:

1. **Separate deciding from doing.** If the code that chooses a destination is the
   same code that performs the move, a faithful dry-run is impossible. You will
   discover this the moment you try to add `--dry-run` to a program that mixes them,
   which is why the project makes you build the plan first.
2. **Enumerate failure before writing.** Filenames with spaces, quotes, newlines,
   and emoji all exist on real machines. So do permission errors, collisions, and
   symlinks pointing somewhere surprising.
3. **Design for reversibility.** Any operation that destroys information should be
   undoable, and the way you achieve that is by writing down what you did *as* you
   do it. This is the same idea as a database write-ahead log, three levels early.

---

## Stage 1 — Plan

Build the list of intended moves. Touch nothing.

Two requirements that are easy to get wrong:

**The plan is data, not text.** Return a list of (source, destination, reason)
records. Printing is a separate step. If your "plan" is a series of `print`
statements, you cannot test it, and `--apply` will end up re-deciding everything,
at which point dry-run and apply can disagree — the exact bug this design prevents.

**Rules are data, not code.** Start here:

```text
rules = {
  documents: [pdf, docx, txt, md]
  images:    [jpg, jpeg, png, gif, webp]
  archives:  [zip, tar, gz, bz2, 7z]
  code:      [py, js, ts, go, rs, c, h]
}
```

A chain of `if extension == ...` works for four categories and collapses at twenty.
More importantly, rules-as-data means you can load them from a file later without
restructuring the program.

**Unmatched files are reported, not skipped.** Silence is the enemy. A file the tool
does not understand is information for the user.

Path handling, before you write a line: use your language's path API
(`pathlib`/`path.join`/`filepath.Join`), never string concatenation. `"~/Downloads"
+ "/" + name` breaks on names with spaces, breaks differently on Windows, and breaks
catastrophically on a name containing `..`. Note that `.tar.gz` has two
extensions — decide what "the extension" means and write the decision down.

---

## Stage 2 — Execute

Only with `--apply`. Dry-run is the default, permanently.

### Collisions

`documents/invoice.pdf` already exists. You have four options, and you must pick
one and document it:

| Policy | Consequence |
|---|---|
| Skip, and report | Safest. Nothing lost, user decides. |
| Rename with a suffix (`invoice-1.pdf`) | Nothing lost, directory gets cluttered. |
| Overwrite if identical (compare a hash), else skip | Correct but slower; requires reading both files. |
| Overwrite | **Never.** This is data loss with extra steps. |

The right default is skip-and-report. The instructive option is the hash
comparison, because it forces the question *what does "the same file" mean?* Same
bytes? Same name and size? Same modification time? You will meet this question again
in caching, in deduplication, and in every sync system ever written.

### The log

Append one line per completed action, **before** starting the next:

```text
2026-08-11T10:32:01Z MOVE /home/u/Downloads/invoice.pdf -> /home/u/Downloads/documents/invoice.pdf
2026-08-11T10:32:01Z SKIP /home/u/Downloads/holiday.jpg (collision, destination exists)
```

Write it as you go, not at the end. If the process is killed halfway, the log must
describe exactly what happened — nothing more, nothing less. That property is what
makes stage 3 possible, and getting it right requires flushing rather than trusting
a buffer to be written.

---

## Stage 3 — Reverse

`--undo <logfile>` puts everything back, using only the log.

Two rules:

- **Undo is dry-run by default too.** It is a destructive operation like any other.
- **Undo verifies before acting.** If a file has been modified or removed since the
  original run, refuse and report it. Do not guess. An undo that silently overwrites
  a file the user edited afterwards is worse than no undo at all.

Reverse the log in order — last action first. Explain, in your README, why order
matters. (Consider a run that moved `a` to `b` and later `c` to `a`.)

---

## Break it

Predict each outcome before running it.

**1. Hostile filenames.** Create these in a scratch directory:

```console
$ mkdir -p ~/scratch && cd ~/scratch
$ touch "a b.txt" "-rf.txt" "quote'.txt" "back\\slash.txt" "emoji-🙂.txt"
$ touch "$(printf 'new\nline.txt')"
```

Every one of these breaks a naive implementation. `-rf.txt` breaks anything that
passes filenames to a shell. The newline breaks anything that parses `ls` output.
The space breaks string concatenation. These are not contrived; they occur on real
machines, and each is a bug class you now recognise.

**2. Permission denied.** Remove write permission from a subdirectory and run
`--apply`. The tool must name the file that failed and stop cleanly. Half a run
with no report is the worst possible outcome.

**3. Same-name collision.** Two files in different subdirectories, same name, same
destination. Your policy should handle it; confirm it does.

**4. Kill it mid-run.** Generate 10,000 files, start `--apply`, and interrupt it.
Then run `--undo`. If the result is not exactly the starting state, your log is
being written after the fact or buffered — fix the ordering.

**5. A symlink out of the tree.** Create `ln -s ~ ~/scratch/escape`. If your
directory walk follows symlinks, you are now about to reorganise your home
directory. Confirm it does not, and write down how you confirmed it.

---

## Done when

- [ ] Dry-run is the default and `--apply` is required to change anything.
- [ ] Every filename in "Break it" step 1 is handled without error.
- [ ] Interrupting a run and running `--undo` restores the exact starting state.
- [ ] Collision policy is documented in your README and matches the code.
- [ ] Unmatched files are reported, not silently ignored.
- [ ] The tool does not follow symlinks out of the target directory.

---

## Anti-patterns

**Applying by default.** A destructive default is a bug no amount of careful code
compensates for. Users run tools before reading them.

**String-concatenated paths.** The source of the space-in-filename bug, and of the
`..` traversal bug, in every language.

**Deciding and acting in one loop.** Makes dry-run a lie: the plan you printed and
the actions you took were computed twice and can differ.

**Per-file `try: ... except: pass`.** The run half-succeeds and reports success.
Collect failures, report them at the end, and exit with a non-zero status.

---

## Stretch

- **Content-based rules.** Read the first bytes and identify the type from its magic
  number rather than its extension. Then find a file whose extension lies.
- **Duplicate detection** by content hash. Then measure: hashing every file versus
  comparing sizes first and hashing only same-size candidates. Report the numbers —
  this is your first optimisation justified by measurement rather than intuition.
- **Resumability.** Interrupt a run over 100,000 files and continue from the log
  rather than restarting.

---

## Next

Return to
[`programming-fundamentals`](../../topics/programming/programming-fundamentals/README.md)
for the gates. When you can build both projects unaided, you are Level 1 and ready
for [`data-structures`](../../topics/computer-science/data-structures/README.md).
