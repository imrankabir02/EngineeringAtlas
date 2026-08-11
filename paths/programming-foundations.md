# Programming foundations

**Level 1 → Level 2** · roughly 5–9 months part-time · assumes you can write a small program

Machine-readable steps: [`programming-foundations.yml`](programming-foundations.yml)
Prerequisite path: [absolute-beginner](absolute-beginner.md)

---

## Who this is for

You can write and debug a few hundred lines of code. You want the foundation that every later
specialisation assumes — and that most self-taught engineers have gaps in, because it is the
material that no tutorial project forces you to learn.

The path ends here:

> You have designed, built, tested and deployed an application designed by you — not scaffolded
> from a tutorial — with tests you actually rely on when refactoring, and you can review a peer's
> pull request with comments about design rather than style.

That is Level 2, and it is the transition from *programmer* to *software engineer*: the concerns
shift from "does it run" to "is it correct, readable, testable, and changeable."

---

## Why this path exists separately

Everything here is **language-agnostic and permanent.** Object-oriented and functional concepts,
type systems, testing, review, and design principles do not expire when a framework generation
turns over.

That matters because it is the material people skip. It has no visible output — nobody's portfolio
says "understands cohesion and coupling" — so it loses every competition against building
something. Then at Level 3 the bill arrives: a codebase that cannot be changed safely, tests
nobody trusts, and abstractions that made things harder.

The second reason: **this is where you learn to evaluate rather than only produce.** `code-review`
is a step in this path, and reviewing code you did not write is a different skill from writing it.
It is also the one that turns into judgment, which is what Levels 3 and 4 run on.

---

## Phase 1 — consolidate what you have

**Steps 1–4 · roughly 6–10 weeks**

| Step | Why it is here |
|---|---|
| [`programming-fundamentals`](../topics/programming/programming-fundamentals/README.md) | Revisit it against the depth markings, not for coverage |
| `debugging-fundamentals` | The highest-leverage topic at this level |
| `error-handling` | Failure as design, not as an afterthought |
| `version-control-git` | The object model, so the commands make sense |

Starting with a topic you have "done" is deliberate. Go to
[`concepts.md`](../topics/programming/programming-fundamentals/concepts.md) and check yourself
against the six `deep` concepts. Specifically, try the two explain gates: variables versus values
using an aliasing example, and why `0.1 + 0.2 != 0.3` and what to do about money.

Most people cannot do both on the first attempt, and the binding model in particular is worth
fixing now — a wrong model there causes bugs at Level 3 that are extremely hard to find, because
the code that breaks is not the code that caused it.

`debugging-fundamentals` is the step that most changes your pace for the next two years. Doing it
deliberately — hypothesis before change, bisection, an actual debugger — rather than by accumulated
habit is worth its two weeks several times over.

**Milestone.** You can write, debug, and version a few hundred lines without fear. When something
breaks you diagnose it from evidence rather than by changing things.

---

## Phase 2 — how software is built by more than one person

**Steps 5–14 · roughly 4–7 months**

This is the substance of the path. Ten topics, in three loose groups.

### Ways of organising code

`object-oriented-programming`, `functional-programming`, `type-systems`.

Learn all three, and learn them as **complementary rather than competing**. The
industry argument between OO and functional is much less interesting than the fact that both
answer the same question — how do you keep a change in one place from breaking another — and that
good code uses ideas from both.

The transferable pieces: from OO, that you should depend on behaviour rather than on a concrete
type, and that deep inheritance hierarchies reliably fail. From functional, that a pure function
is trivially testable, and that immutability removes whole categories of bug. From type systems,
what a checker can and cannot prove, and therefore what tests are still for.

If your language is dynamic, add optional typing to an existing project of yours and count the
real bugs it finds. That number is more persuasive than any argument about static versus dynamic.

### Practices

`clean-code`, `testing-fundamentals`, `package-management`, `git-workflows`, `code-review`.

`testing-fundamentals` is where the most common misconception lives. The value of a test is not
that it proves correctness — it is that **you can change the code without re-checking everything by
hand.** Once you feel that, testing stops being a chore and becomes the thing that lets you move
fast. Until you feel it, no amount of advocacy helps.

Note also what the topic says about coverage: it is a weak proxy that becomes actively harmful the
moment it becomes a target, because you get tests written to touch lines rather than to catch
regressions.

`code-review` deserves more attention than it usually gets. Review is the cheapest place to learn
design, because you see many people's decisions rather than only your own. Practise on real
open-source pull requests: read the diff, write your comments, *then* read the maintainers'
discussion. What they saw that you did not is the most direct measurement of judgment available to
a self-learner.

### Design

`software-design-principles`.

Last, deliberately. Design principles are answers to problems you have to have experienced. SOLID
read before you have maintained anything produces cargo-culted abstractions; read after you have
had to change your own six-month-old code, it lands.

The important skill in this topic is not applying the principles. It is **recognising when an
abstraction is premature** — which is the more common error by a wide margin, and the one the
principles are most often misused to justify.

**Milestone.** You have built and deployed an application designed by you, with tests you rely on
when refactoring, and you can review a peer's pull request for design rather than style. **You are
Level 2.**

---

## Where people stall

**Skipping testing because it feels slow.** It is slower for the first two weeks and faster
forever after. The way through is not discipline; it is to refactor something moderately large
*without* tests, notice how carefully and slowly you had to move, and then do it again with them.

**Learning OO as syntax.** Classes, inheritance, and the keyword list are not the topic.
Encapsulation and dependency direction are. If your notes are about `super()` and not about which
module is allowed to know about which, you have learned the language feature and not the idea.

**Over-applying design principles.** The characteristic Level 2 failure: an interface per class,
a factory for everything, four layers of indirection to change a string. This comes from reading
the principles without the experience they respond to. The corrective is
[refactoring](../topics/programming/programming-fundamentals/advanced.md) and the honest question
*what did this abstraction save me?*

**No project to hang it on.** The topics in phase 2 are hard to learn in the abstract. Have one
real application you are building throughout, and apply each topic to it. The
[project ladder](../projects/ladder.md) at Level 2 lists suitable ones — a REST API with a
database, an authentication system, a blog platform.

---

## Honest effort estimate

| Group | Focused hours | Calendar, at ~8 h/week |
|---|---|---|
| Phase 1 (4 topics) | ~70 | 9 weeks |
| Ways of organising code (3 topics) | ~90 | 11 weeks |
| Practices (5 topics) | ~130 | 16 weeks |
| Design (1 topic) | ~40 | 5 weeks |
| **Total** | **~330** | **~41 weeks (9–10 months)** |

Five months is achievable at 16 hours a week. This path is genuinely long, and the reason is that
most of it is skill rather than knowledge — it requires doing things repeatedly, which cannot be
compressed by reading faster.

---

## What comes next

| Next | Choose it if |
|---|---|
| [Computer science foundations](computer-science-foundations.md) | You want the theory that predicts behaviour before building bigger systems |
| [Software engineering core](software-engineering-core.md), phase 4 | You want to continue straight into production concerns — concurrency, databases, caching, operations |
| [Python backend](stacks/python-backend.md), phase 2 onward | You want a stack-specific route to production services |
| [`data-structures`](../topics/computer-science/data-structures/README.md) | The single highest-value individual topic from here |

**The honest recommendation:** do
[`data-structures`](../topics/computer-science/data-structures/README.md) next regardless of which
path you pick. It is the topic that turns "it works" into "it works at scale", and it is a hard
prerequisite for indexing, caching, and most of Level 3. Everything downstream is easier with it
and confusing without it.
