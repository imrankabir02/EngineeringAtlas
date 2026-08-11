# Programming fundamentals — interview

What competent discussion of these concepts sounds like, and what a shallow answer
reveals.

**This is not a question bank.** Memorised answers collapse under the first follow-up, and
the follow-up is where the assessment happens. What follows are discussion shapes: the
topic, what a good answer contains, and the tells that separate understanding from recall.

[← Programming fundamentals](README.md) · [Concepts](concepts.md) ·
[Advanced](advanced.md)

---

## What is being assessed at this level

Not whether you can recite definitions. Three things:

1. **Do you have a correct mental model?** Most visible in questions about variables,
   mutability, and scope, because a wrong model gives confidently wrong predictions.
2. **Can you decompose a problem?** Visible in how you approach any "write a function
   that..." task — where you start says more than whether you finish.
3. **Can you debug?** Visible in what you do when something does not work, which
   interviewers will engineer an opportunity to observe.

You will not be asked "what is a for loop". You will be handed a small problem and
watched.

---

## Discussion 1 — "What does this print?"

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)
```

**A shallow answer:** "`[1, 2, 3]` — `b` is a copy."

Wrong, and it reveals the box model. This exact question, in various forms, is asked
constantly at this level precisely because it discriminates so cleanly.

**A competent answer:**

> `[1, 2, 3, 4]`. `b = a` binds a second name to the same list; it does not copy. So
> `b.append(4)` mutates the one list, and both names see the change. If I wanted a copy I
> would write `b = a[:]` or `list(a)` — and if the list contained nested lists, even that
> would be shallow, so the inner lists would still be shared.

**The tell:** distinguishing **rebinding** from **mutation**, unprompted. The strong
answer also mentions shallow versus deep copy without being asked, because someone who
has actually been bitten by this knows there are two layers to it.

**Follow-up you should survive:** *"How would you write a function that sorts a list
without affecting the caller's copy?"* Return `sorted(items)` rather than calling
`items.sort()`. And be able to say why that is a better default: functions that mutate
their arguments surprise callers, and the surprise arrives far from the cause.

---

## Discussion 2 — "Why doesn't `0.1 + 0.2` equal `0.3`?"

**A shallow answer:** "Floating point is imprecise."

True, and it does not answer the question. Everyone has heard this sentence.

**A competent answer:**

> Floats are stored in binary, and `0.1` is a repeating fraction in binary the way `1/3`
> is in decimal. It gets truncated to the available bits, so the stored value is slightly
> off, and adding two slightly-off values makes the error visible. The practical
> consequences: never compare floats with `==`, compare with a tolerance; and never use
> floats for money — use integer cents or a decimal type. I would also mention that
> addition is not associative for floats, so `(a+b)+c` can differ from `a+(b+c)`, which
> matters when summing many values.

**The tell:** naming the *mechanism* (binary representation of a decimal fraction) and
then the *action* (integer cents for money). Knowing what to do about it is what makes
the knowledge useful.

---

## Discussion 3 — "Walk me through how you'd approach this problem"

You are given something like: *count word frequencies in a file and return the ten most
common.*

**A weak approach** starts typing immediately.

**A competent approach** talks first, and the talking is what is being assessed:

> First, clarifying: what counts as a word — split on whitespace, or strip punctuation?
> Case-sensitive? How large is the file — does it fit in memory? What should happen on a
> tie for tenth place?
>
> Assuming reasonable answers: read the file line by line rather than all at once so it
> works on large files, normalise each line to lowercase, split into words, and count in a
> dictionary — because I need lookup by key and a list would be a linear scan per word.
> Then take the top ten. I'd sort by count, though a heap of size ten would be better if
> the vocabulary were huge, since sorting everything to keep ten is wasteful.
>
> I'd separate counting from selecting from printing, so the counting function is testable
> on a string without touching a file.

**The tells:** clarifying questions before code, choosing a collection with a stated
reason, mentioning the memory consideration, separating computation from I/O, and noting a
better algorithm while explaining why the simpler one is fine here. Every one of those is
a signal about judgment rather than knowledge.

**A tell that costs you:** silence. Interviewers cannot assess reasoning they cannot hear.
Thinking out loud is a skill and it is worth practising deliberately.

---

## Discussion 4 — "Your code doesn't work. What do you do?"

This is often observed rather than asked, because interviewers will give you a problem
where something goes wrong.

**A weak response:** change things semi-randomly, re-run, and hope. Or freeze.

**A competent response, out loud:**

> The error says `NoneType has no attribute append`, at line 12, so something I expected
> to be a list is `None`. Line 12 uses `result`, which comes from `build_result` — so
> either that function returned nothing on some path, or it was never called. Let me look
> at its return statements... there is a branch with no `return`, so on that path it
> returns `None` implicitly. Let me confirm by checking which branch this input takes.

**The tells:** reading the error properly, forming a specific hypothesis, and then seeking
evidence rather than making changes. Also: narrating. An interviewer who can hear your
reasoning can assess it; one who watches silent typing cannot.

**The strongest single thing you can say when stuck:** "I don't know — here's how I'd find
out." Followed by a concrete method. This is a *good* answer at every level, and
confidently guessing is a bad one.

---

## Discussion 5 — "When would you use a dictionary instead of a list?"

**A shallow answer:** "Dictionaries are faster."

Faster at what? This answer signals memorised advice.

**A competent answer:**

> It depends on the access pattern. A dictionary gives lookup by key in roughly constant
> time, so if I am looking things up by an ID or a name repeatedly, that is the right
> structure. A list is right when order matters, when I will iterate over everything
> anyway, or when there are few enough items that a scan is irrelevant — a few dozen items
> is not worth optimising.
>
> The place it really matters is a lookup inside a loop: scanning a list inside a loop over
> the same data is quadratic, and at a hundred thousand items that is the difference
> between instant and unusable. I've measured that — the list version got about ten
> thousand times slower when the input grew a hundredfold, and the set version a hundred
> times.

**The tell:** "it depends on the access pattern", plus a magnitude, plus — best of all —
having measured it. The
[benchmark gate](exercises.md#collections) exists to give you that sentence honestly.

---

## Discussion 6 — "What makes code good?"

Open-ended, and the answer reveals a lot.

**A weak answer** lists rules: comments, short functions, DRY.

**A competent answer** names a *goal* and derives properties from it:

> Mostly: how easily can the next person change it correctly? That includes me in three
> months. So — names that say what things are, functions that do one nameable thing,
> computation separated from I/O so it can be tested, and errors that fail loudly with
> enough information to act on.
>
> I'd be careful with rules like DRY. Removing duplication between two things that happen
> to look alike but change for different reasons makes the code harder to change, not
> easier. Comments are similar: a comment explaining *why* is valuable, and one restating
> *what* the code does becomes a lie the first time someone edits the line above it.

**The tell:** treating principles as heuristics with failure cases rather than as rules.
That distinction is the entry point to `software-design-principles` and it is the
difference between someone who has read about clean code and someone who has maintained
something.

---

## Shallow-answer tells, generally

In roughly increasing severity:

**Vocabulary without mechanism.** "It's pass by reference" with no account of what is
actually passed. Naming a category is not an explanation — and in most languages that
phrase is imprecise anyway.

**No magnitudes.** "Sets are faster" tells nobody anything. "About a hundredfold at a
hundred thousand items, because the list version is quadratic" is a model.

**The box model of variables.** Confidently predicting `[1, 2, 3]` in discussion 1. This
is the single clearest signal at this level, and it is why the question keeps being asked.

**Changing code without a hypothesis.** Observable in any live exercise, and it reads as
"has never systematically debugged anything".

**Silence.** Not thinking out loud. Costs you credit for reasoning you actually did.

**Certainty about things that depend.** "Always use X" for anything. Someone with real
experience knows the case where X is wrong, because they hit it.

---

## Practising this properly

The `explain` gates in [`topic.yml`](topic.yml) *are* the interview preparation:

- Explain variables versus values to someone at Level 0, using aliasing.
- Explain `0.1 + 0.2` and what to do about money.
- Explain why a function that computes and prints is harder to test.

Do them **out loud, to an actual person**, or written down in full sentences. Rehearsing
in your head skips the step where you find out which parts you cannot articulate, which is
the only part that matters.

Then, per
[philosophy.md](../../../docs/philosophy.md#interview-question-memorisation): do not grind
question banks. They train retrieval, which collapses under perturbation, and the
perturbation is the interview. Derive from mechanisms instead. Someone who understands
binding answers every aliasing question ever invented, including the ones nobody has
posted online.

The most reliable interview preparation available to you at this level is
[the two projects](projects.md), done properly, with a written account of what you decided
and what broke. That gives you concrete things to talk about, and concrete beats fluent
every time.
