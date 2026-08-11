# Validation

How you prove competency, and what counts as evidence.

This directory replaces the `interview-preparation/` folder a repository like this would normally
have. The reason is structural: an interview-preparation directory reliably becomes a question bank,
and a question bank trains recall — which is the failure mode the project exists to oppose. See
[architecture.md §7](../docs/architecture.md#7-validation-replaces-interview-preparation).

Interview material still exists. It is `interview.md` in each topic, scoped as *what competent
discussion of this topic sounds like and what a shallow answer reveals* — not questions with answers
to memorise.

---

## The problem this solves

Self-assessment does not work, and it fails in a predictable direction: people who have only read
about something consistently overestimate how well they could do it. This is not a character flaw,
it is how recognition and recall differ from production — following an explanation *feels* like
capability, and there is no internal signal distinguishing the two.

So the repository does not ask you how well you know something. It asks what you did.

---

## Evidence standards

A [progress state](../docs/progress-tracking.md) beyond `learning` requires evidence that exists
**outside this repository**.

| State | Evidence that counts | Evidence that does not |
|---|---|---|
| `practicing` | Your exercise solutions exist somewhere you can point to | "I did most of them" |
| `built` | A repository, started from a blank directory, that you designed | A tutorial project; a clone with your name on it |
| `validated` | Break/debug notes, a written explanation, benchmark numbers with a stated setup | A passing test suite alone; "it works" |
| `mastered` | Someone you taught can do it unaided; a novel diagnosis; a merged contribution; a decision you lived with | Years of use; a job title; confidence |

The distinction that does most of the work: **`built` is about producing, `validated` is about
understanding.** You can build something that works without understanding why, which is why the
`break`, `benchmark`, and `explain` gates exist between them.

---

## The gate types

Each topic's `topic.yml` declares gates drawn from this vocabulary. `build` and `explain` are
mandatory; the others appear where they discriminate.

| Gate | Asks | Produces |
|---|---|---|
| `build` | Can you make it? | An artifact you designed |
| `break` | Do you know what is load-bearing? | A reproducible failure you caused deliberately |
| `debug` | Do you understand the mechanism? | A root-cause statement from evidence |
| `explain` | Do you understand it, or recognise it? | Writing another person can act on |
| `benchmark` | Is it true, or do you believe it? | Numbers, and a prediction you got wrong |
| `review` | Can you evaluate, not just produce? | Critique of code you did not write |
| `design` | Can you decide under constraints? | An architecture, and a defence of it |
| `research` | Can you use primary sources? | A paper's contribution, assumption, and cost, in your words |

Full method for each: [competency-gates.md](../docs/competency-gates.md).

A library of reusable challenges — design problems with traps, debugging scenarios, failure
simulations, and review exercises: [gate-library.md](gate-library.md).

---

## Which gates matter most, and when

**Levels 0–2:** `build` and `explain` carry almost all the weight. At these levels the question is
whether you can produce a correct thing and say why it works. `break` starts appearing at Level 2
and is where the transition to Level 3 begins.

**Level 3:** `break`, `debug`, and `benchmark` become the discriminating gates. "Did you build it"
stops separating people, because everyone at Level 3 can build things. What separates them is
whether they have made their own systems fail and measured the result.

**Level 4:** `design` and `review` dominate. The work is judgment, and judgment is only visible in
decisions made under constraints and in critique of others' decisions.

**Level 5:** `research`, plus the gates that cannot be written down — did someone you mentored become
capable, did your design survive five years, did your diagnosis save a system.

---

## Interviews

A note, because it is the reason many people arrive here.

The gates in this repository are better interview preparation than any question bank, for a reason
that is worth understanding rather than taking on faith: **interviews test derivation under
perturbation.** The interviewer changes a constraint and watches what you do. Memorised answers have
nothing to change; derived answers do.

Concretely, what the gates give you that grinding does not:

- **Measurements you took.** "I caused 500 origin calls on a cold key, added single-flight, and got
  1" is a sentence nobody else in the queue has. Interviewers can tell the difference between
  measured and read immediately.
- **Failures you caused.** "I corrupted a linked list with two threads and here is the interleaving"
  demonstrates a mental model. Reciting that locks prevent races does not.
- **Practice articulating.** The `explain` gates require writing or speaking to a specific audience.
  That is the actual skill being assessed in an interview, and it is nearly impossible to do well
  unrehearsed.

What to avoid: grinding problem sets before you can choose a data structure from an access pattern.
See [interview.md](../topics/computer-science/data-structures/interview.md#on-grinding-problem-sets)
for the direct argument.

---

## Running a gate honestly

Nobody is checking. That makes two habits load-bearing:

**Write the prediction before the measurement, and do not edit it.** The gap between prediction and
result is the whole value of a benchmark gate. Editing the prediction afterwards leaves you with a
number instead of a calibration.

**Distinguish "I could do that" from "I did that".** The first is the feeling this whole directory
exists to distrust. If you find yourself reading a gate and thinking *obviously I could* — that is
precisely the moment to do it, because that feeling has a poor track record.

The honest failure mode is not cheating. It is doing four of a topic's six gates, recording the
topic as validated, and forgetting which two you skipped. Write down what you skipped; the list is
more useful than the checkmarks.
