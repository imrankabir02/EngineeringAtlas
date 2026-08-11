# Topic title — practical

<!-- AUTHOR: usually the longest file. Target 1,000-3,000 words. Doing it for real: tools,
     commands, the selection rubric, failure modes, and operation.
     Delete every AUTHOR comment before committing. -->

<!-- AUTHOR: one line on what this file covers. -->

[← Topic title](README.md) · [Fundamentals](fundamentals.md) ·
[Concepts](concepts.md) · [Exercises](exercises.md)

---

## Before you start

<!-- AUTHOR: for topics involving a decision - adding a component, adopting a tool - open with
     the questions the reader must be able to answer first. Three or four, each with a note on
     what a non-answer looks like.

     This section prevents the most common misuse of most topics: applying the technique
     without establishing that it is the right one. -->

---

## Setup

<!-- AUTHOR: minimal. What is genuinely needed, and an explicit list of what is NOT needed yet.
     Elaborate tooling is a way to feel productive without doing the work, and each tool is
     something that can break while the reader is trying to learn something else. -->

---

## Selection

<!-- AUTHOR: REQUIRED for any topic that names a technology. The eight questions from
     ../../../docs/technology-selection.md:

       1. What problem does it solve? (stated as a problem someone had before it existed)
       2. When should you use it? (concrete conditions, with thresholds where they exist)
       3. When should you NOT use it? (the most important, and the one marketing never answers)
       4. What are the alternatives? (always including "do nothing" and "the boring option")
       5. What are the trade-offs? (stated as losses, not "considerations")
       6. What complexity does it add? (operationally - the cost everyone omits)
       7. What is the ecosystem like?
       8. What does production look like?

     A technology that cannot answer question 3 with something specific is being sold rather
     than explained, and does not belong in the repository. -->

| Option | Choose when |
|---|---|
| <!-- AUTHOR: including the simplest option, first --> | |

**When not to use <the main option>:**

- <!-- AUTHOR: specific, and each one a real case rather than a hedge -->

---

## Doing it

<!-- AUTHOR: real code or real commands. Then annotate what is load-bearing and, just as
     usefully, what is deliberately missing so the reader can see the gap.

     Mark version-specific claims:
       > *Verified against <tool> <version> (<YYYY-MM>).* <the claim>

     Do not paste output that will drift. Describe what to look for instead. -->

---

## Operating it

<!-- AUTHOR: for anything that runs in production:
       - the metrics needed from day one, and what each one being wrong indicates
       - configuration that is not optional, and the bad default it protects against
       - what breaks on deploy
       - the security default that is wrong out of the box -->

---

## Debugging

<!-- AUTHOR: a decision procedure, not a list of tips. An ASCII decision tree works well:

       Is it X or Y?
         X ──► look here
         Y ──► look there

     Then name the one or two causes that catch everyone out. Those are the highest-value
     lines in the file, because they are what a colleague would tell you and no
     documentation does. -->

---

## Measuring

<!-- AUTHOR: what to measure and how not to fool yourself. The general rules are in
     ../../../docs/competency-gates.md - state only what is SPECIFIC to this topic.

     Almost always worth saying: predict first; exclude warm-up; report percentiles rather
     than means; use a realistic input distribution. -->

---

## Anti-patterns

<!-- AUTHOR: the mistakes that actually appear in real code, each with its symptom.
     The symptom is what makes the entry useful - it is how a reader recognises the mistake
     in their own work.

       **The mistake.** Why it is wrong. **Symptom:** how you notice. **Fix:** what to do. -->

---

## Next

[exercises.md](exercises.md), then [projects.md](projects.md).
