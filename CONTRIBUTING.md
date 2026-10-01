---

## Lesson Template

Copy this file, rename it to `NN_topic_name.md`, and fill in every section.
Do not delete a section. If a section genuinely does not apply, write one line
saying why instead of removing the heading.

````markdown
# NN — Lesson Title

**Part**: partXX_name · **Prerequisites**: lesson numbers · **Time**: 25 min

---

## In Plain Words

Three to five sentences. No symbols. Explain the idea as if to someone who is
smart but has never seen this topic. This is the section people read first, so
it must be genuinely understandable on its own.

## Why Computer Science Cares

Two to four concrete places this appears: an algorithm, a data structure, a
system design decision, a paper, an interview question. Be specific. Name real
libraries, real classes, real functions where possible.

## The Formal Version

Precise definitions. Use the symbols from [SYMBOLS.md](../../SYMBOLS.md).

**Definition.** A *term* is …

**Theorem.** If … then …

Keep the statement and the explanation separate. The statement is what you can
look up; the explanation is what you actually understand.

## Formula Sheet

Every formula this lesson introduces, in one table. Use LaTeX in `$…$` for
inline and `$$…$$` for display. Add a plain-English column so the formula is
readable without knowing the notation.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$\det(A)$` | `$\sum_{\sigma \in S_n} \operatorname{sgn}(\sigma)\prod_i a_{i,\sigma(i)}$` | signed volume scale factor | checking invertibility |

Rules for this section:
- Every formula used anywhere in the lesson MUST appear here.
- No formula appears here that is not explained in the body.
- Always say what each symbol in the formula means, right there in the table.
- If a formula has conditions ("valid only for $n > 0$"), put them in the
  "When you use it" or a note column. Omitting a domain restriction is how
  people get answers wrong.

## Worked Example

Solve something slowly. Show every step. Explain why you chose that step.
Use a small enough example to hold in your head. Show intermediate values.

## Runnable Code

Python 3. Every snippet runs as written, with no edits.

```python
# imports
# the computation
# print with the actual values
```

Print explanatory labels. The output should be readable by someone who has not
seen the lesson.

## Common Mistakes

Three to five real errors, each with the wrong version, the right version, and
why the wrong one is tempting.

---

## Multiple Choice Questions

At least 8 questions per lesson. Four options each. Cover both the definitions
and the applications, and include at least two questions where a plausible
misconception makes a wrong option tempting.

Format each one exactly like this. The answer and the reasoning go inside the
`<details>` block so the reader can try first:

**Q1.** What does the symbol `$\sum_{i=1}^{n} i$` represent?

- A) The product of all integers from 1 to n
- B) The sum of all integers from 1 to n
- C) The average of all integers from 1 to n
- D) The largest integer less than or equal to n

<details>
<summary>Answer and explanation</summary>

**B) The sum of all integers from 1 to n.**

`$\sum$` is the summation sign and `$i$` runs from 1 up to $n$, so the terms
being added are $1, 2, 3, \dots, n$. Option A describes `$\prod$`, which is the
product sign. Option C is $\frac{n(n+1)}{2n}$, a different quantity. Option D is
the floor function.

</details>

Rules for MCQs:
- Four options, exactly one correct. Never "all of the above" or "none of the
  above" as the correct answer.
- Distractors must be real confusions, not joke answers. Explain in the solution
  block why each wrong option is wrong.
- No question may be answerable from the `## Summary` alone. The summary
  restates; the questions test.
- Vary difficulty. Roughly two thirds recall/comprehension, one third application.
- State the answer letter and the full option text, then explain.

## Subjective Questions

Short answer and long answer, each with a model answer.

### Short Answer

**Q1. Define a *subspace* of $\mathbb{R}^n$.**

<details>
<summary>Answer</summary>

A subset $W \subseteq \mathbb{R}^n$ is a subspace if it contains the zero
vector and is closed under vector addition and scalar multiplication. Closure
means: if $u, v \in W$ then $u + v \in W$, and if $u \in W$ and $c \in \mathbb{R}$
then $cu \in W$.

</details>

### Long Answer

**Q1. Why is a hash table lookup expected $O(1)$ rather than guaranteed $O(1)$?**

<details>
<summary>Model answer</summary>

A good hash function spreads keys nearly uniformly over the $m$ buckets, so the
expected number of keys in any bucket is $n/m$, which is constant when the load
factor $n/m$ is bounded. A lookup therefore examines a constant number of
entries on average, giving expected $O(1)$.

It is not guaranteed, because two distinct keys can collide into the same
bucket. With $n$ keys and $m$ buckets, by the pigeonhole principle at least one
bucket must contain $\lceil n/m \rceil$ or more keys, so the worst case for that
bucket is linear. An adversary who knows the hash function can construct all
$n$ keys to collide, forcing $O(n)$ per lookup — this is why production hash
tables randomise the seed (Python's `PYTHONHASHSEED`, SipHash in Rust's
`HashMap`).

The bound is therefore an expectation over the random seed or over the choice of
keys, not a guarantee for a fixed key set.

</details>

Rules for subjective questions:
- 4 to 6 short-answer questions, each answerable in under ten lines.
- 3 to 5 long-answer questions requiring a real explanation, not a definition.
- Model answers must be complete. A model answer that only names the concept
  does not model a good answer.
- At least one long-answer question per lesson must ask "why" or "what would
  break this", not "what is this".
- Answers must agree with the code and formulas in the lesson. If the lesson says
  the values are 0.1 and 0.2, a question answer cannot use different numbers.

---

## Exercises and Solutions

**[ ] Exercise 1 — question.** Enough detail that it is solvable without hints.

<details>
<summary>Solution</summary>

Full working answer, not just a number.

</details>

**[ ] Exercise 2** — and a **Challenge** for readers who found it easy.

## Summary

- Bullet points, five to eight of them, each one line.
- No new material in the summary.
- Do not repeat the formula sheet; link to it instead.

## Next

Link to the next lesson and say in one line what it assumes from this one.
````

---

## Rules for Writing Lessons

**Plain language means plain language.** The `In Plain Words` section must contain
no LaTeX and no undeclared symbols. If you catch yourself writing "here $V$ is a
subspace", stop and say it in words instead.

**Show your reasoning, not just your answer.** A worked example where the reader
sees every intermediate value teaches far more than one where only the final
number appears. Prefer a smaller example computed completely over a larger one
computed partially.

**Every code block must run.** Test it. Do not use a variable before defining it.
Do not require files that are not in the repository. Do not require network
access. Keep imports minimal and at the top of the block.

**Use only the standard library in the main examples.** Numpy, matplotlib, scipy
and sympy are encouraged in "With Libraries" subsections because they make the
mathematics visible, but the plain-Python version must appear first so the
lesson works with nothing installed.

**Real numbers in the output.** If the text says the answer is 0.6660, the code
must print something consistent with that. Never write an output block you did
not run.

**Exercises need complete solutions.** `[ ]` for the question, `<details>` for
the answer. Solutions are in the same file, directly after their exercise — this
is deliberate so the repository is usable offline.

**Questions need real reasoning.** An MCQ whose solution block only restates the
answer teaches nothing. Every MCQ solution explains why each wrong option is
wrong, because the wrong options are the actual lesson.

**Questions must be answerable from the lesson.** Do not test something the
lesson never covered, and do not test something stated only in the summary.

**Link generously.** Link to the prerequisite lesson, to related lessons, and to
the notation table. Use relative paths that work from GitHub and from a local
clone.

**Respect the reader's time.** If a topic genuinely needs 3000 words, say so in
the header rather than padding 800 words. Cut exposition that repeats the code.

---

## What every lesson must contain

This is the checklist. A lesson missing any row is incomplete.

| Section | Minimum size |
| --- | --- |
| Header with part, prerequisites, time | one line |
| `## In Plain Words` | 3–5 sentences, no symbols |
| `## Why Computer Science Cares` | 2–4 concrete examples |
| `## The Formal Version` | definitions and statements |
| `## Formula Sheet` | a table covering every formula in the lesson |
| `## Worked Example` | one problem solved completely, every step shown |
| `## Runnable Code` | standard library only, verified to run |
| `## Common Mistakes` | 3–5 real errors |
| `## Multiple Choice Questions` | 8+ questions, 4 options each, answers and reasoning in `<details>` |
| `## Subjective Questions` | 4–6 short answer, 3–5 long answer, all with model answers |
| `## Exercises and Solutions` | 6+ problems with full solutions |
| `## Summary` | 5–8 one-line bullets |
| `## Next` | link forward |

---

## Adding New Lessons

1. Check `README.md` and the relevant `partXX_*/README.md` — if the topic is
   already listed but has no file, you found your slot.
2. Pick the next unused number in the part. Numbers are stable once used; do not
   renumber existing lessons, because every cross-link depends on them.
3. Follow the template above exactly.
4. Add the row to `README.md` and to the part's `README.md`.
5. Run `python run_all.py` and make sure your lesson's code still passes.
6. Open a pull request.

## Adding a New Part

A new part needs: a `partXX_name/` directory, a `README.md` inside it that
explains what the part covers and what it assumes, at least three lessons, a
section in the root `README.md`, and a `TIME.md` estimate if you can give a
reasonable one.

## Code Style for Examples

- Python 3, standard library first, third-party libraries in a clearly marked
  subsection.
- Prefer small numbers so results can be checked by hand.
- Use `f-strings` for output.
- Add a comment above any non-obvious line explaining the mathematics being
  implemented, not the mechanics of the Python.
- If a snippet is long, put it in a real `.py` file under the part directory and
  link to it instead of inlining everything in the markdown.

## Tone

Write like a good textbook and a good senior colleague at the same time.
Confident, not condescending. Direct, not padded. Assume the reader is capable
of hard things but has not done this particular thing before.