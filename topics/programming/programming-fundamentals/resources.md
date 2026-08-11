# Programming fundamentals — resources

Nine resources. Read three or four of them properly rather than skimming all nine.

Choosing what to read is a hard problem you are not yet equipped to solve, so it has been
solved for you. Selection rules:
[resource-tiers.md](../../../docs/resource-tiers.md).

[← Programming fundamentals](README.md) · [Fundamentals](fundamentals.md) ·
[Advanced](advanced.md)

---

## Tier 1 — Primary sources

### [The Python Tutorial (official)](https://docs.python.org/3/tutorial/)

If you chose Python, this is the primary source, and it is unusually readable for official
documentation — it was written to teach.

**Sections 3 through 6 cover this entire topic.** Section 4 is control flow and functions;
section 5 is data structures; section 9 is classes, which you can skip for now
(`object-oriented-programming` at Level 2).

Listed at Tier 1 rather than as a tutorial because reading official documentation is a
habit most engineers acquire far too late, and there is no reason to wait. When you have a
question about how a built-in behaves, the answer is in the Library Reference, it is
correct, and it is faster than searching.

### [MDN JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)

If you chose JavaScript, this is the reference maintained closest to the standard, and it
is the reason you never need a low-quality tutorial site.

Use the **Guide** for learning and the **Reference** for lookup. Treating them as the same
thing is why people end up reading content farms — the Guide teaches, the Reference tells
you exactly what `Array.prototype.splice` does to its arguments.

### [What Every Computer Scientist Should Know About Floating-Point Arithmetic — Goldberg](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html)

**Read only sections 1 and 2, now**, at the moment `0.1 + 0.2` first surprises you. The
rest is for a much later day and is genuinely hard.

Included because floating point is the first place a beginner meets a *machine limitation*
rather than a mistake of their own, and understanding it early prevents a specific
expensive class of bug — money handled in floats. It is also a good first experience of
reading a technical paper and taking only what you need.

---

## Tier 2 — High-quality learning material

### [Think Python — Allen Downey](https://greenteapress.com/wp/think-python-3rd-edition/)

**The best single linear path through this topic if you want one.** Free.

It teaches problem decomposition rather than giving a syntax tour, and the exercises are
hard enough to be worth doing. Crucially, it treats debugging as a first-class subject
with its own sections, which most introductions do not.

**How to use it:** do the exercises. All of them, in order. Reading it without the
exercises produces the recognition-without-capability state this repository exists to
prevent.

### [Eloquent JavaScript — Marijn Haverbeke](https://eloquentjavascript.net/)

The JavaScript equivalent, and equally good. Free online, with runnable examples.

Chapters 1–6 map onto this topic. It teaches programming *using* JavaScript rather than
listing JavaScript features in order, which is what separates it from almost everything
else available for this language.

### [Structure and Interpretation of Computer Programs (SICP)](https://mitpress.mit.edu/sites/default/files/sicp/full-text/book/book.html)

**Hard. Not a first resource.** The best available treatment of what programming *is*
rather than how one language spells it.

Read chapters 1 and 2, slowly, doing the exercises, **after your first project**. It uses
Scheme, which will feel alien for two days and then stop mattering — that alienation is
part of the value, because it strips away the syntax you had started mistaking for
concepts.

It will reorganise what you already know rather than teach you new facts. That is why the
ordering matters: read it too early and it is impenetrable; read it after a project and it
is clarifying.

Budget 30+ hours for two chapters. Worth it, and skippable — nothing later in this
repository depends on it.

### [Debugging — David Agans](https://debuggingrules.com/)

Nine rules, none language-specific, all applicable for the rest of your career. Short
enough to read in an evening.

Read it once now, and again after your first genuinely hard bug — the second reading is
when the rules stop being obvious and start being useful. "Quit thinking and look" and
"change one thing at a time" are the two that will save you the most time in the next
year.

---

## Tier 3 — Practical

### [Exercism](https://exercism.org/)

Small exercises with human mentorship, in 70 languages. Free.

Listed instead of a competitive-programming site deliberately: the feedback is about
**clarity and idiom**, which is what you need now. Competitive programming optimises for
speed and clever tricks, which is a different skill that will not help you at this level
and can actively teach habits you must later unlearn.

Do the first 15–20 exercises in your language, and **request mentorship on at least
three**. Having someone review your code and tell you it is unclear is worth more than ten
exercises done alone.

### [Python Tutor — visualise execution](https://pythontutor.com/)

Steps through code line by line, showing variables, references, and the call stack as
diagrams. Supports several languages despite the name.

**The fastest way to fix a wrong mental model** of
[variables and binding](concepts.md#variables-and-binding) or aliasing. Paste in the
ten-line example that confuses you and watch the arrows.

Use it for ten confusing lines, not for whole programs. It is a diagnostic instrument, not
a development environment.

---

## What is deliberately not here

The reasons are more useful than more links.

**Video courses.** They produce a strong feeling of comprehension that does not survive a
blank file, which is the definition of
[tutorial hell](../../../docs/philosophy.md#tutorial-hell). If you use one, use it for
orientation only, and cap it: one hour of video per three hours of writing code.

**Bootcamp-style "learn X in Y days" material.** This topic takes 8–16 weeks of real work.
Anything promising less is redefining "learn", and the framing trains an expectation that
makes the actual timeline feel like failure.

**Competitive programming sites** (LeetCode, Codeforces) — genuinely useful later for
`algorithms`, actively unhelpful now. They train pattern retrieval on a fixed problem set,
which is the opposite of what Level 1 needs, and they will make you feel incapable for
reasons unrelated to your actual progress.

**Framework tutorials.** Django, React, Express. Not yet. See
[advanced.md](advanced.md#what-not-to-do-next).

**"Top 10 tricks" articles.** Language tricks are worth nothing until the fundamentals are
solid, and they crowd out the material that matters.

**Anything requiring a subscription** as the only route through a concept — see the
[paywall rule](../../../docs/resource-tiers.md#rules). Everything you need for this topic
is free.

---

## A working plan

If you want a concrete schedule, this is a defensible one. Adjust the pace, not the order.

**Weeks 1–3 — mechanics.** Work through Think Python or Eloquent JavaScript, chapters 1–6,
doing every exercise. In parallel, do [exercises.md](exercises.md) 1–20. Keep the REPL open
constantly.

**Weeks 4–6 — first project.** Build the
[calculator](../../../projects/cli-calculator/README.md). Expect to be stuck, repeatedly;
that is the work, not a sign of a problem. Read Agans when you hit your first bug that
takes more than an hour.

**Weeks 7–9 — the rest of the drills.** Finish [exercises.md](exercises.md), including all
the Break-it and Explain items. Do the benchmark gate.

**Weeks 10–13 — second project.** Build the
[file organiser](../../../projects/file-organizer/README.md), including undo.

**Weeks 14–16 — consolidate.** Work the remaining gates. Read SICP chapters 1–2 if you want
depth. Then rewrite the calculator from memory — see
[advanced.md](advanced.md#rewrite-your-calculator-from-memory).

Sixteen weeks is normal. Eight is fast. Twenty-four while working full time is entirely
reasonable and is not behind schedule, because there is no schedule.
