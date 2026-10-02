# Part 06 — Mathematics for Algorithms

Every algorithm has two numbers attached to it: how much work it does, and how you
know that is the answer. This part is about both, and about the third thing that
decides whether a program is any good — whether the work it does is *worth* the space
and time it costs.

The part has one running idea, which is that **complexity analysis is not about
finding the fastest algorithm but about making claims that survive scrutiny**. It is
easy to write "my algorithm is `O(n^2)`"; it is much harder to write "my algorithm is
`O(n^2)` and here is an input for which nothing smaller is possible". The three
lessons build up exactly that discipline in three layers.

Lesson 80 is about measuring. It defines the vocabulary — `O`, `Θ`, `o`, and the cost
model that every claim has to name — and then shows, with numbers the code actually
prints, how the cost model changes the answer: `x == y` is `O(1)` for a machine word
and `Θ(k)` for a `k`-bit integer, and under schoolbook multiplication the `Θ(log n)`
fast-doubling Fibonacci *loses* to the `Θ(n)` loop.

Lesson 81 is about the bound you get when no single operation is representative. A
dynamic array's `append` costs 1, usually, and `n/2`, occasionally; quoting either
number alone is useless. Amortised analysis adds up a whole sequence and divides, and
the lesson proves the bound three ways — an exact ledger, an accounting scheme with a
never-overdrawn reserve, and a potential function whose sum telescopes — then shows
where the method fails completely, on structures where every operation is expensive
and there is no bank to pay from.

Lesson 82 is about the other direction: how do you *find* an algorithm, and how do you
know it is right? Loop invariants for correctness, exchange arguments for greedy rules,
recurrences and the Master Theorem for divide and conquer, and the overlap test that
decides between dynamic programming and recursion. It ends by building a data structure
from scratch with its invariant machine-checked on every operation.

## What is in it

| # | Lesson | What you get out of it |
| --- | --- | --- |
| 80 | [Big-O and Complexity Analysis](80_big_o_and_complexity.md) | The vocabulary (`O`, `Θ`, `o`, cost models), counting instead of timing, four ways to solve a recurrence, the decision-tree lower bound for comparison sorts, and why the *cost model* is part of the claim |
| 81 | [Amortised Analysis](81_amortized_analysis.md) | Aggregate bounds, the accounting and potential methods, geometric growth proved necessary, why tombstones break a hash table without an adversary, and union-find's `α(n)` — plus where amortisation cannot help at all |
| 82 | [Tools for Algorithm Design](82_tools_for_algorithm_design.md) | Loop invariants and variant functions as executable code, the exchange argument and when it does not exist, the Master Theorem including its boundary case, dynamic programming versus divide and conquer, and designing a structure whose invariant is machine-checked |

## What this part assumes

- **Part 02** at the level of [Lesson 24 — Recurrence Relations](../part02_discrete_combinatorics/24_recurrence_relations.md),
  because lesson 80's four solution methods are all methods for solving recurrences, and
  lesson 82's Master Theorem section assumes you can expand one into a tree. The
  pigeonhole principle from
  [Lesson 23](../part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md)
  is the reason a hash table's expected `O(1)` cannot also be a guarantee.
- **Part 03** for the asymptotic notation itself and for reading the matrix products in
  the cost-model discussion.
- **Part 05** only for the word "expected", which lesson 81 uses in its precise sense
  (an average over a distribution you must name) as distinct from both worst case and
  amortised.
- Basic Python: arithmetic, functions, loops, lists, dicts, `f`-strings, recursion.
  Nothing else.

## What it does not assume

No prior algorithms course. No discrete maths beyond recurrences and the pigeonhole
principle. No numpy, no scipy. Every plain-Python block in this part runs with the
standard library alone and is checked automatically by `python run_all.py`; the
sections marked **With Libraries** use matplotlib for the pictures and can be skipped
without losing anything, because every number they plot was printed by an earlier block.

## The one-sentence version of each lesson

- **80.** A complexity claim is only as good as the cost model it names and the lower
  bound it survives, and the difference between counting iterations and counting work
  is where most wrong answers come from.
- **81.** When one operation is rare and enormous and the rest are trivial, the
  meaningful number is the average over a whole sequence — but only when the rare
  operation can pay for itself out of what the cheap ones saved.
- **82.** A correct algorithm needs an invariant and a termination argument, a greedy
  rule needs an exchange, and a recurrence needs its subproblems classified as
  overlapping or not before you can say anything about it.

## Where to go next

**[Part 07 — Geometry for Graphics](../part07_geometry_graphics/)**. This part argued
about the *cost* of an algorithm without ever mentioning what it computes. Part 07 puts
the techniques here onto real numbers: the convex-hull algorithms of lesson 92 are
divide-and-conquer and greedy, and the spatial partitioning there is an amortised-cost
argument about cache behaviour, exactly like lesson 81's hash tables.

**Back to [Part 02 — Discrete Mathematics and Combinatorics](../part02_discrete_combinatorics/)**.
Lesson 80 assumed you can solve a recurrence and read a summatory function; the
generating-function methods in lessons 22 and 28 are the tool for the cases lesson 82's
Master Theorem cannot reach, and the recurrence-solving toolkit there is what makes
lessons 80 and 82's derivations feel routine rather than clever.

## A note on the code

Every numeric value printed in these lessons was produced by running the code shown.
Where a printed number appears in the prose it is the number the program actually
emitted — including the ones that came out badly, such as the sliding-window section in
lesson 81 where the amortised ledger and the naive rebuild disagree by a factor that
grows with the window size, and lesson 82's frequency-counter measurement where the
speed-up ratio grows from `137×` to `1,390×` while the normalised ratio stays flat at
`0.138`. Where a measurement would not reproduce — anything involving a wall clock — it
is either counted instead or explicitly not tabulated, and the block says so in as many
words. The check is automated, and it re-runs each block and diffs its real stdout
against the `Output:` block printed beneath it:

```bash
python run_all.py 06        # every plain-Python block in this part
python run_all.py 06 --show # and print each block's output
```