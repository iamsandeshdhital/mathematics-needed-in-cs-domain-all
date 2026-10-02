# Part 10 — Tensors and Numerical Methods

The practical bridge: how the mathematics actually meets the machine.

Two lessons, and they are the last in the repository because they are the
point the other ten parts were building towards. Everything before this was
about *what* is true. These two are about what a computer can actually hold and
how much of the truth survives the holding.

## What this part covers

| # | Lesson | What it gives you |
| --- | --- | --- |
| 120 | [Tensors and Broadcasting](120_tensors_and_broadcasting.md) | Tensors as functions from a product of index sets; shapes, size and rank; the broadcasting rules implemented from scratch; why a 1D array aligns with the **last** axis and what that silently breaks; `einsum` built by hand, including the rule that a letter is summed only if it is absent from the output; strides as memory layout; why transposing is free and reshaping is not; broadcasting-as-a-view |
| 121 | [Numerical Methods and Floating Point](121_numerical_methods_and_floating_point.md) | IEEE 754 and what a `float64` actually stores; `ulp`, unit roundoff and why `1e16 + 1 == 1e16`; catastrophic cancellation and the five standard rewrites; forward versus backward error; condition numbers as a property of the problem; bisection, Newton, secant and Brent with their measured orders of convergence; stopping criteria; finite differences and their √u floor; Richardson extrapolation, trapezoid, Simpson and Romberg |

## The one idea running through both

**How the numbers are laid out and how the arithmetic is ordered decides
how much of the answer survives.** That is one sentence, and it covers both
lessons.

Lesson 120 says it about memory: a tensor is a flat buffer plus a shape plus
a set of strides, and two operations that produce the same *shape* can
produce different *numbers* (`reshape(3,2)` versus `transpose`), while two
operations that look different can be the same buffer walked two ways.

Lesson 121 says it about time: float addition is not associative, so the
*order* in which a sum is accumulated decides its value — `[1e16, 1.0,
-1e16, 1.0]` folds to `1.0` in a loop and `2.0` in `math.fsum`, from
identical inputs.

Same fact, two levels. numpy's pairwise summation and its C-contiguous
default are both the same decision made in different code.

## The one-sentence version of each lesson

- **120.** A tensor is a shape and a rule for getting to an entry; broadcasting is
  that rule applied without copying; `einsum` is the notation that makes any
  contraction readable; and the whole thing is a buffer plus metadata, which is
  why transposing costs nothing and reshaping sometimes does.
- **121.** A float is a rounded binary fraction, subtraction of near-equals
  throws away significant digits, no algorithm can beat an ill-conditioned
  problem, and the numerical methods worth trusting are the ones whose
  convergence order you can *measure* rather than assume.

## What this part assumes

- **Lesson 31 (Matrices and Matrix Algebra)** — a 2D tensor is a matrix, and
  every rule in 120 generalises one lesson's arithmetic to an arbitrary number
  of axes. Nothing else about matrices is needed.
- **Lesson 41 (Matrices, Graphs, and Applications)** — adjacency matrices and
  the idea of an operation that maps a whole collection of vectors at once,
  which is exactly what broadcasting automates.
- **Lesson 51 (Derivatives)** and **Lesson 52 (Integration)** — Newton's method
  needs a derivative and Simpson's rule needs an integral; 121 states every
  error bound rather than assuming the calculus.
- **Lesson 54 (Taylor Series)** — the real prerequisite for 121's error
  analysis. Every truncation constant in that lesson is a Taylor coefficient
  (`h·f″/2`, `h²·f‴/6`, `−h²/12·(g′(b) − g′(a))`), and Richardson extrapolation
  is nothing more than repeatedly cancelling the leading term of a Taylor
  expansion. If Taylor expansions are unfamiliar, read 54 first — otherwise
  the formulas will be correct and unexplained.
- Basic Python: nested lists, loops, `f`-strings, and one class in 120's
  stride example. Every plain-Python block runs with the standard library alone.

You do **not** need any framework experience, and you do not need to have
written floating-point code before. The `### With Libraries` subsections use
numpy, scipy, matplotlib and `decimal`, and can be skipped entirely — though
121's is where `math.fsum` and `scipy.optimize.brentq` stop being names and
become measurable.

## A suggested route

Read them in order. The dependency is short and real:

```
31, 41  (matrices as collections of vectors)
   |
   v
120 (tensors, broadcasting, einsum, strides)
   |
   v
121 (IEEE 754, cancellation, conditioning, root-finding)
```

About **75 minutes** for a first pass at reading plus running the code, and
roughly double that again for the exercises, which have full worked solutions
in the same files.

**If you work with tensors today** — PyTorch, JAX, a dataframe library — read
120's *Strides and memory layout* section first and skip the rest. The
`reshape`-is-not-`transpose` distinction and the fact that a broadcast axis
which gets *summed* costs `M` times the output are the two things that explain
most "why is this slow" and "why is this number wrong" questions about real
code. Then go straight to 121.

**If you have never thought about precision** — 121 is the one to read, and it
is written to be read start to finish without 120 at all. It is the most
self-contained lesson in the repository after
[Lesson 13 — Proof Techniques](../part01_logic_proof/13_proof_techniques.md).

**If you are preparing for numerical-methods coursework**, read both in order
and do every exercise. 121's Exercise 4 is a complete experiment: it sweeps a
step size over twenty decades, fits the convergence order of four rules, and
compares the measured optimum against the theoretical `h*`. Nothing in that
lesson is asserted without being measured first.

## Exercises

Each lesson ends with four worked exercises and a challenge, with full
solutions in the same file, so the part is usable offline. Several are
deliberately measurable rather than proveable: you are asked to print the
number and then explain why it is that number.

Two of them are worth doing even if you do nothing else.

**Exercise 3 of lesson 121** sets up two rows that pull in opposite
directions. `[1e16] + 10⁴ ones` has condition number 1 — perfectly
conditioned — and still loses a relative 1e-12, because conditioning is a
*worst-case bound* and not a prediction. `[1e16, 1, -1e16, 1]` has condition
number 1e16 and no summation order can save it. Between them they establish
that you must measure the error and separately reason about the problem, and
that the two are different jobs.

**The Challenge of lesson 121** builds a Romberg table and then runs it on
`|x − 0.5|`, where the plain trapezoid rule is *exact* because the corner
lands on a node. Extrapolation turns that exact answer into a wrong one and
keeps it wrong. That single table is the strongest available argument that
Richardson extrapolation is a bet on smoothness rather than an improvement.

## A note on the code

Every numeric value printed in these lessons was produced by running the code
shown. Where a printed number appears in the prose, it is the number the
program actually emitted — including the ones that come out badly, which is
why lesson 121 quotes `0.0` where `1.49e-13` belongs and calls it a result
rather than a typo.

```bash
python run_all.py 10          # every plain-Python block in this part
python run_all.py 10 --show   # and print each block's output
```

Lesson 121's `### With Libraries` block additionally writes
`numerical_error.png` — two log-log panels showing finite-difference error
against step size (truncation up, roundoff down, crossing at the √u floor)
and quadrature error against panel count (slopes 2, 2 and 4).

## Where to go next

There is no Part 11. This is the end of the repository, and the two lessons
are the right place to stop because they are the point at which the other ten
parts become checkable.

**Back to [Part 08 — Optimisation](../part08_optimization/)** if you want the
numerical content in its algorithm form.
[Lesson 101 — Gradient Descent](../part08_optimization/101_gradient_descent.md)
is where the condition number first appears, as a *speed* question — it decides
whether an iterative method is usable at all. Lesson 121 is the same number as
an *accuracy* question: it decides whether a direct solve is worth reaching for
instead. Reading them together is the single most useful pairing in the
repository.

**Back to [Part 04 — Calculus](../part04_calculus/)** if the error constants in
121 were correct but unexplained. Every one of them is a Taylor coefficient,
and
[Lesson 54 — Taylor Series](../part04_calculus/54_taylor_series.md) is where
they come from.

**And keep the habit the part is really about**: when a number comes out wrong,
check the condition number before you read the code. Most of the time the code
is fine and the problem cannot be solved to the precision you asked for.

For the notation, see [SYMBOLS.md](../SYMBOLS.md). The symbols used here that are
not in the general table — a stride, an ulp, the order of convergence — are
defined where they appear. Verify the whole part at any time with
`python run_all.py part10_tensors_numerical`.
