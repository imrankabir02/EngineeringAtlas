# Progress Tracking

Seven states per topic. Each transition beyond `learning` requires **evidence
that exists outside this repository** — a commit, a document, a benchmark, a
review.

This is the whole point. A checkbox records intent; evidence records capability.

---

## The states

| State | Meaning | Evidence required |
|---|---|---|
| `not-started` | Not begun | — |
| `started` | Read the topic README; prerequisites verified | — |
| `learning` | Working through `fundamentals.md` / `concepts.md` | — |
| `practicing` | Doing `exercises.md`; the drills sometimes fail | Your exercise solutions exist somewhere you can point to |
| `built` | Completed a `core` project for this topic | A repository, from a blank directory, that you designed |
| `validated` | Passed the topic's declared gates | Break/debug notes, a written explanation, benchmark numbers with a stated setup |
| `mastered` | Others rely on your judgment here | See below |

### On `mastered`

You do not set this yourself from having done the gates. `mastered` means at
least one of:

- You taught the topic to someone who then did it unaided.
- You debugged a novel failure in it that others could not.
- You made a non-trivial contribution to a tool or codebase implementing it.
- You made an architectural decision involving it, lived with the consequences,
  and can explain both what you got right and what you got wrong.

If none of those is true, you are `validated`. `validated` is a genuinely strong
position — most working engineers are `validated` on most of what they use daily,
and that is fine. Inflating it to `mastered` costs you the ability to tell the
difference, which is the only thing the tracker is for.

---

## What the repository stores: nothing

There is no account, no database, and no server. Progress is yours.

Three workable approaches:

### 1. A tracker file (recommended)

Copy `templates/progress.yml` into your own fork or a private repository:

```yaml
# my-progress.yml
learner: your-handle
updated: 2026-08-11

topics:
  programming-fundamentals:
    state: validated
    evidence:
      - "github.com/me/file-organizer — built from scratch, 340 lines"
      - "Wrote up why my first recursion approach blew the stack"
    started: 2026-01-08
    updated: 2026-03-02

  data-structures:
    state: built
    evidence:
      - "github.com/me/ds-from-scratch — hash table with open addressing"
    note: >
      Benchmark gate not done yet. I still cannot explain why my hash table
      degrades at 0.8 load factor.
    started: 2026-03-05
    updated: 2026-04-11

  caching:
    state: learning
    started: 2026-04-20
    updated: 2026-04-28
```

The `note` field is the most valuable one. Write down what you know you do not
understand. That list is your actual curriculum.

### 2. GitHub issues in your own fork

One issue per topic, labelled with the state. Works well if you like a board
view, and the issue thread becomes a log of what you tried.

### 3. An engineering journal

A dated Markdown file per week: what you built, what broke, what you measured,
what surprised you. This is the lowest-friction option and it has a property the
others do not — rereading it six months later shows you your own growth in
judgment, which is otherwise invisible.

---

## Reviewing your own progress

Every month or two, ask:

**Is my level balanced across the four axes?**
(See [levels.md](levels.md#the-four-axes).) Many `learning` states and few
`built` states means high Knowledge and low Skill: you are in tutorial hell.
Many `built` and no `validated` means you build but never verify — you will be
confidently wrong under load.

**Am I collecting `started` states?**
More than three or four topics in `started`/`learning` at once is technology
hopping. Finish something.

**What is the oldest unfinished topic?**
Either finish it or drop it explicitly. Ambient guilt about a half-read topic
costs more than the topic.

**What is in my `note` fields?**
Those are real gaps and they are usually one prerequisite level down. That is
where your next two weeks should go.

---

## Anti-pattern: the completed checklist

A fully checked list of 200 topics proves you can maintain a list.

If your tracker has more `mastered` entries than you have systems in production,
the tracker is measuring optimism. Recalibrate against the "you are here when"
tests in [levels.md](levels.md); they are written to be hard to pass by
self-assessment alone.
