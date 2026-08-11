# Programming fundamentals — exercises

Thirty drills, grouped by concept and roughly ordered by difficulty. Each is small
enough to finish in one sitting.

**Rules that make these worth doing:**

- **Predict the output before running.** Every time. The gap is the lesson.
- **Write assertions**, not print statements you inspect by eye.
- **Do them before the projects.** Exercises make mechanics automatic so the projects can
  be about design.
- If a group is trivially easy, skip ahead. If none is easy, you may be missing a
  prerequisite.

[← Programming fundamentals](README.md) · [Concepts](concepts.md) ·
[Practical](practical.md) · [Projects](projects.md)

---

## Values and types

**1.** Predict, then check: what do `7 / 2`, `7 // 2`, `-7 // 2`, and `7 % -2` give in
your language? The negative cases are the interesting ones — different languages
genuinely disagree, and knowing yours prevents a real bug class in index arithmetic.

**2.** Show that `0.1 + 0.2 != 0.3`. Then write `almost_equal(a, b, tolerance)` and use
it to compare them correctly.

**3.** Write a function that adds a list of prices given as strings like `"19.99"` and
returns the exact total in cents as an integer. No floats anywhere in the computation.
This is how money is actually handled.

**4.** Find your language's largest integer, or demonstrate it has none. Then find what
happens when you exceed the largest float. Both answers are worth knowing before they
surprise you.

**5.** Write a function that takes a value and returns a description of its type and
whether it is "empty" by your language's truthiness rules. Test it with `0`, `""`, `[]`,
`{}`, `None`, `" "`, and `"0"`. Two of these commonly surprise people.

---

## Variables, binding, and aliasing

**6.** Predict the output, then run:

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a, b)

c = [1, 2, 3]
d = c
d = [9]
print(c, d)
```

Explain the difference between the two halves in one sentence each.

**7.** Write a function that takes a list and returns a sorted version **without
modifying the caller's list.** Then write one that sorts in place. Demonstrate the
difference with an assertion on the caller's list.

**8.** Demonstrate the default-mutable-argument trap in your language, or demonstrate
that your language prevents it. Then write the correct version.

**9.** Take a nested structure — a list of lists — and make a copy such that modifying
the inner lists of the copy does not affect the original. Then make one where it does.
Name both behaviours.

**10.** Using [Python Tutor](https://pythontutor.com/) or your debugger, step through
exercise 6 and watch the arrows. Write two sentences on what you saw that the code did
not make obvious.

---

## Control flow

**11.** Predict the number of times `body()` runs, on paper, before running it:

```python
for i in range(1, 10, 2):
    for j in range(i):
        body()
```

**12.** Write a function that returns the FizzBuzz string for one number. Then a
function that produces the sequence for 1 to n. Note that you separated computing from
producing — that separation is the point of the exercise, not the fizzing.

**13.** Write a loop that finds the first item in a list matching a condition, returning
a sentinel if none matches. Then write it again using your language's built-in for this.
Compare readability.

**14.** Write a linear search over a list and state its loop invariant explicitly in a
comment: what is true at the start of every iteration?

**15.** Write a condition that safely checks a possibly-absent nested value — for example
`user["address"]["city"] == "Dhaka"` when `user` may lack an address. Do it using
short-circuit evaluation, and demonstrate that reordering the conditions breaks it.

---

## Functions

**16.** Take this function and split it into parts that each do one nameable thing:

```python
def process(filename):
    lines = open(filename).read().split("\n")
    total = 0
    for line in lines:
        if line and not line.startswith("#"):
            total += float(line.split(",")[2])
    print(f"Total: {total:.2f}")
    return total
```

List what each new function can now be tested or reused for that the original could not.
There are at least four separable concerns.

**17.** Write a function that takes another function as an argument and applies it to
every item in a list. Then use your language's built-in equivalent.

**18.** Write a pure function (no I/O, no globals, no mutation of arguments) that
computes a non-trivial result. Write three assertions for it. Notice how easy the test
was to write; that ease is a property of the function's design, not of the test.

**19.** Write a function with a mistake in its scope handling — reading a global it should
have taken as a parameter — then fix it. Explain in one sentence why the fixed version is
easier to test.

**20.** Write a function that validates its input and raises a specific error with a
useful message. Test both the success and failure paths.

---

## Collections

**21.** Given a text file, count occurrences of each word and print the ten most common.
Choose your collection deliberately and write one sentence justifying the choice.

**22.** Write two functions that find duplicates in a list: one using only list
operations, one using a set. Assert that they agree.

**23. [benchmark]** Time both functions from exercise 22 on 1,000 and 100,000 items.
**Predict the ratio first.** Then explain the shape of the difference. This is a gate in
[`topic.yml`](topic.yml).

**24.** Invert a dictionary — swap keys and values. Then handle the case where two keys
share a value. What does the result type have to become, and why?

**25.** Given a list of records (dicts), group them by one field. Then sort each group by
another field. Do it without a library beyond your language's sort.

---

## Text, files, and errors

**26.** Read a file and print its lines with numbers, handling: the file not existing, it
being a directory, and it being empty. Each case gets its own message.

**27.** Determine the length of a string containing one emoji, in bytes and in whatever
your language calls characters. Try a family emoji (👨‍👩‍👧). Explain the difference.

**28.** Write a function that builds a long string in a loop using `+=`, and one using
your language's join or builder. Time both at 10,000 iterations. Explain why one is
quadratic.

**29.** Write a program that takes a filename as a command-line argument, reads it,
writes a transformed version to a new file, and exits with a non-zero status on any
failure. Verify the exit code from your shell with `echo $?`.

**30.** Write a recursive function that walks a directory tree and reports total size.
Handle: permission denied on a subdirectory, and a symlink pointing at a parent
directory. Predict what happens with the symlink before you test it.

---

## Break it

Not optional. These are `break` gates in [`topic.yml`](topic.yml).

**B1.** Write a recursive function with no base case. Run it. Read the error carefully
and explain what resource ran out. Then add a depth limit and a clear message.

**B2.** Write a function that mutates a list it was passed. Call it from code that did
not expect mutation and assert on the surprising result. Then fix it two ways: by copying
inside the function, and by returning a new list instead. Say which you prefer and why.

**B3.** Deliberately catch `Exception` broadly around a block containing a typo. Observe
that your own bug is now hidden behind a generic message. Then narrow the catch and watch
the real error appear. This is the most instructive five minutes in the group.

**B4.** Create a file with a name containing a space, a quote, and a leading dash. Write
a program that opens each by name. Anything that builds paths by string concatenation
will break on at least one.

**B5.** Write a loop that never terminates because the condition depends on a variable
you forgot to update. Find it with a debugger rather than by reading.

---

## Explain

Write these down. Writing is where you find out which parts you were pattern-matching.
These are `explain` gates.

**E1.** Explain the difference between a variable and a value to someone at Level 0,
using an example where two names refer to the same list.

**E2.** Explain why `0.1 + 0.2 != 0.3`, and what to do instead when handling money. Two
paragraphs.

**E3.** Explain why a function that both computes a result and prints it is harder to
test than one that only computes. Show both versions.

**E4.** Explain, to someone who has only written scripts, why version control matters
even when working alone.

**E5.** A colleague's function is 80 lines long and works. Explain what you would change
and why, without saying "it's too long".

---

## Answers to check yourself

<details>
<summary>Expand after attempting</summary>

**1.** `-7 // 2` is `-4` in Python (floor division rounds toward negative infinity) and
`-3` in C, Java, and Go (truncation toward zero). `%` follows correspondingly, so the
sign of a modulo result differs between languages. This bites when computing wrapped
indices with possibly-negative inputs.

**5.** `" "` (a space) is truthy — it is a non-empty string. `"0"` is truthy for the same
reason, which surprises people coming from languages or shells where it is not.

**6.** First half prints `[1, 2, 3, 4] [1, 2, 3, 4]` — `append` **mutates** the one
shared list. Second half prints `[1, 2, 3] [9]` — assignment **rebinds** `d` to a
different list, leaving `c` alone.

**11.** `i` takes 1, 3, 5, 7, 9. Inner loop runs `i` times each. Total 1+3+5+7+9 = 25.

**16.** At least four separable concerns: reading the file, filtering comment and blank
lines, extracting and summing the third field, and formatting for display. Splitting them
means you can test the parsing on a string instead of a file, reuse the summing on data
from anywhere, and call the computation from code that has no console.

**23.** The list version is O(n²) — for each item it scans the list. The set version is
O(n). At 1,000 items the difference is small; at 100,000 it is roughly a hundredfold, and
the list version may take minutes. The *shape* is what matters: 100× the input made the
list version 10,000× slower and the set version 100× slower.

**24.** If two keys share a value, the inverted mapping must map each value to a
*collection* of keys. The return type has to change, which is the real lesson: the
inverse of a function is not necessarily a function.

**27.** A family emoji is a sequence of several emoji joined by zero-width joiners. It is
one user-perceived character, several code points, and often 25+ bytes in UTF-8. Most
languages report the code-point count, which matches neither what a user sees nor what is
stored.

**28.** Strings are immutable, so `s += x` allocates a new string and copies the old
contents each time. Total work is 1+2+3+...+n, which is O(n²). `join` computes the final
size once and copies each piece once, O(n).

**30.** A symlink pointing at a parent directory creates a cycle, and a naive recursive
walk follows it forever until the stack or your patience runs out. Real tools track
visited inodes or refuse to follow symlinks. This is the same class of bug as the
symlink case in the [file-organizer project](../../../projects/file-organizer/README.md).

**B1.** The call stack ran out — each call needs a frame holding its local variables and
return address, and the space for frames is finite and much smaller than your heap.

</details>

---

## Next

[projects.md](projects.md) — the two core projects. Do the exercises first; the projects
assume the mechanics are automatic.
