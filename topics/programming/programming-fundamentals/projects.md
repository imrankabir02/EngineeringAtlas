# Programming fundamentals — projects

Two core projects. Both are required to pass this topic's `build` gate, and they are
chosen because they teach different things.

[← Programming fundamentals](README.md) · [Exercises](exercises.md) ·
[Interview](interview.md)

---

## Core project 1

### [Expression calculator](../../../projects/cli-calculator/README.md)

**Level 1** · validates `functions`, `control-flow`, `recursion`,
`errors-and-exceptions`, `debugging`

A command-line program that evaluates arithmetic expressions with correct operator
precedence and parentheses. **No `eval`, no parser library.**

**Why this project and not another**

`2 + 3 * 4` must produce `14`, not `20`. That single requirement is what makes the
project work, because getting it right forces you to represent the *structure* of the
expression rather than scanning it left to right. You cannot pattern-match your way to a
correct answer.

What it forces, all at once and for real:

- **Decomposition** — a string becomes tokens, tokens become structure, structure becomes
  a number. Three stages with clean interfaces, and you will discover why they need to be
  separate when a precedence bug appears and you have to work out which stage is wrong.
- **Recursion where it is genuinely the right tool** — parentheses nest arbitrarily, and a
  recursive-descent parser handles that naturally while a loop-based approach becomes a
  mess. This is much more convincing than a factorial example.
- **Error handling as design** — most input a user types is invalid. Errors are the main
  path, and "never crash, always report a position" is a real requirement rather than
  polish.
- **Testing that catches something** — precedence bugs are invisible until you write the
  case. `10 - 2 - 3` catches associativity bugs that `2 + 3 * 4` does not.

There is a bonus you should notice: you have written the front half of an interpreter.
That connection makes `compilers-and-interpreters` at Level 4 feel like a continuation
rather than a new subject.

**The constraint that matters:** no `eval`. With it, the program works in one line and
teaches nothing. The parser *is* the assignment.

---

## Core project 2

### [File organiser](../../../projects/file-organizer/README.md)

**Level 1** · validates `io-and-files`, `errors-and-exceptions`, `collections`,
`strings-and-encoding`

A tool that reorganises a messy directory according to rules you define, with dry-run as
the default, collision handling, and a log good enough to undo the run.

**Why a second project, and why this one**

The calculator only ever touches strings it was given. This project touches the outside
world, and that changes everything.

Three lessons that the calculator structurally cannot teach:

1. **Your mistakes are permanent.** A calculator bug prints a wrong number. This program
   with a bug deletes someone's files. Working under that constraint changes how you write
   code, and experiencing the change is the point — nobody becomes careful by being told
   to be careful.

2. **The world is hostile.** Filenames contain spaces, quotes, newlines, and emoji.
   Directories are unwritable. Two files want the same destination. Symlinks point
   somewhere surprising. None of this is contrived; all of it exists on real machines, and
   each case is a bug class you will now recognise for the rest of your career.

3. **Design for reversibility.** Any destructive operation should be undoable, and the way
   you achieve that is by writing down what you did *as* you do it. That is a
   write-ahead log, three levels before you meet the term in
   `transactions-and-isolation` — and meeting the idea first, in a context where you
   needed it, is why it will make sense later.

**The constraint that matters:** dry-run is the default. Forever. A destructive default
is a bug no amount of careful code compensates for, because users run tools before
reading them.

---

## Do them in order

The calculator first. It is self-contained — no filesystem, no external state, no
platform differences — so when something is wrong, it is wrong in your logic and nowhere
else. That makes it the better first experience of debugging your own design.

The file organiser second, because it adds the outside world on top of skills you now
have. Doing it first means fighting two unfamiliar things at once and being unable to
tell which is causing the problem.

---

## What "done" means

Not "it runs." The checklists are in each project README. The three that matter most,
across both:

**You started from a blank file.** No tutorial, no template, no clone. If someone else
made the decisions, you got typing practice — see
[copy-paste projects](../../../docs/philosophy.md#copy-paste-projects).

**You did the `break_it` section.** Five thousand nested parentheses. Filenames with
newlines. A killed process mid-run. A project you have not broken is a project you do not
understand, and this is the stage that separates Level 1 from "has completed a tutorial".

**You wrote it up.** A README saying what you built, what you decided, what broke, and
what surprised you. This is the `explain` gate, and it is what makes the work legible to
anyone else — including a future employer, who can read a design write-up far faster than
they can read your code.

---

## Also on the ladder at this level

Optional, in [projects/ladder.md](../../../projects/ladder.md). Worth doing if the core
projects felt easy.

**Notes application (CLI)** — persistence without a database. Serialisation formats,
concurrent edits from two terminals, and what "saved" actually means. A good bridge to
`databases-introduction`.

**Log summariser** — parse a real, messy log file. Every line that does not match your
assumption is a lesson about real data, and there will be many.

**Personal Git archaeology** — answer questions about an existing repository using `log`,
`blame`, and `bisect`. Turns Git from a save button into an investigative tool, and it is
the natural bridge to `version-control-git`.

---

## After the projects

Return to [`topic.yml`](topic.yml) and work the remaining gates — `debug`, `explain`,
`benchmark`, `review`.

The `benchmark` gate is the one to take seriously: two versions of a duplicate-finder,
one scanning a list and one using a set, measured at 1,000 and 100,000 items, with your
prediction recorded first. It is your first measurement-driven conclusion about
performance, and it makes `complexity-analysis` at Level 2 land on something real rather
than on notation.

The `review` gate — reading 200 lines of someone else's code and naming three specific
improvements — is the one people skip and the one that most directly builds judgment.
Evaluating code is a different skill from writing it, and it is the one that transfers.
