# Part 08 — Optimisation

How a machine finds the best answer when there are too many to check.

Every other part of this repository hands you answers. This part is the one that
produces them. A least-squares fit over ten million parameters, a route through a
traffic network, a protein fold, a hyperparameter sweep, a portfolio: in each case
nobody enumerated the answers, and something had to *search*. That something is an
optimiser, and this part is the mathematics that decides whether it works.

The part has one running idea. An optimiser is a search, and the only question that
matters is **how many places can the search get stuck**. Convexity is the property that
makes that number exactly one. Everything else here is either the machinery that turns
"there is one answer" into "here it is" (gradient descent) or the machinery that handles
the case where the rules of the problem forbid most of the space (Lagrange multipliers).

## What this part covers

Three lessons. The first states the guarantee, the second spends it, the third extends
it to problems where you are not allowed to walk wherever you like.

| # | Lesson | What it gives you |
| --- | --- | --- |
| 100 | [Convexity](100_convexity.md) | Convex sets and the convex hull; convex, strictly convex and affine functions; Jensen's inequality; the second-order test; positive definiteness via eigenvalues and Sylvester's criterion; the composition rules that make L2 safe and L1 dangerous; why local implies global, and why Rosenbrock's function is not convex |
| 101 | [Gradient Descent](101_gradient_descent.md) | The gradient as the steepest-descent direction; the update rule `x ← x − η∇f(x)`; the exact stability bound `0 < η < 2/λ_max` and where the `2` comes from; the condition number and why iterative methods lose to direct solves; heavy-ball momentum and why it is not a free speed-up; Nesterov acceleration; stochastic gradients and why they converge to a *set* of minimisers |
| 102 | [Lagrange Multipliers and Constraints](102_lagrange_multipliers_and_knt.md) | The Lagrangian; stationarity and why it is necessary but not sufficient; the second-order test on the tangent space; the four KKT conditions and complementary slackness; shadow prices; strong duality and Slater's condition; the dual problem and why it is often convex when the primal is not; the SVM margin, where the multipliers pick out the support vectors |

## What this part assumes

- **Lesson 51 (Derivatives)** — partial derivatives and the chain rule. The gradient *is*
  the vector of partials, and every result here is proved by differentiating something.
- **Lesson 53 (Multivariable Calculus)** — the gradient as the direction of steepest
  ascent, Jacobians, and gradient descent itself. Lesson 101 in particular treats 53's
  first descent example as already understood; read it if the terms `∇f`, `η` and
  "learning rate" are not yet ordinary words.
- **Lesson 54 (Taylor Series)** — only for first-order and second-order expansions.
  Lesson 100's quadratic case is a Taylor argument, and `½hᵀHh` is the term Taylor
  throws away.
- **Lessons 32–40 (Linear Algebra)** — matrices, symmetric matrices, eigenvalues and
  positive definiteness. This is the real prerequisite for lessons 100 and 101: the
  Hessian is a matrix, the stability bound is a statement about its eigenvalues, and the
  condition number is `λ_max/λ_min`. Without
  [Lesson 36 — Eigenvalues and Eigenvectors](../part03_linear_algebra/36_eigenvalues_and_eigenvectors.md)
  and [Lesson 39 — Diagonalization and Spectral Theory](../part03_linear_algebra/39_diagonalization_and_spectral.md)
  these lessons will be much harder than they need to be.
- **Lesson 80 (Big-O)** — so that `O(1/k)` and `O(1/k²)` mean something when the
  convergence rates come up.
- Basic Python: functions, tuples, loops, `f`-strings. Every plain-Python block runs on
  the standard library alone.

You do **not** need numerical analysis, and you do not need to have seen an optimiser
before. The `### With Libraries` subsections use numpy, scipy and matplotlib and can be
skipped entirely.

## A suggested route

Read them in order. Each one consumes the guarantee the previous one established:

```
100 (convexity: there is one answer)
  -> 101 (gradient descent: here it is, and how big a step is safe)
       -> 102 (Lagrange multipliers: and what if you may not walk freely?)
```

If you are coming from machine learning and want the fastest useful route, **100 then
101** is the whole part for almost every practical purpose; lesson 102 matters when you
hit a solver's `constraints=` argument and want to know why the answer has a number
attached to it. If you are coming from operations research or from a course in
nonlinear optimisation, go straight to 102 — it is written to stand on its own, and it
is the only lesson here with a real theory of *certificates*.

If you only have half an hour, read `## In Plain Words` and `## Why Computer Science
Cares` in lesson 100 and then the **Common Mistakes** of all three. That combination is
most of the practical content: what convexity buys you, which sign goes where, and the
five ways people silently get the wrong answer.

## Suggested study time

The headers of the three lessons say **35 min** each, so budget about **1 h 45 min** for a
first pass at reading plus running the code. Realistically:

| Stage | Time | What to do |
| --- | --- | --- |
| Read 100 | 35 min | Read prose and the worked example; run the blocks and check the printed output against the prose |
| Read 101 | 35 min | Read prose and the worked example; plot the six panels from `### With Libraries` if you can |
| Read 102 | 35 min | Read prose and the worked example; run the KKT solver and read the four-condition verification carefully |
| Exercises | 60–90 min | Six-plus exercises per lesson, each with a full solution in the same file |

Double the figure if you intend to actually *use* this: lesson 100's Composition Rules
and lesson 102's four KKT conditions are the two things you will look up repeatedly, and
they are not learnable by skimming.

## The one-sentence version of each lesson

- **100.** A convex function is a bowl: no dents, slopes that never decrease, and
  therefore a single bottom — which is what turns "keep walking downhill" from a hope into
  an algorithm.
- **101.** Measure the slope, step against it, and the only real decision is how far; for
  a quadratic that decision has an exact answer, `0 < η < 2/λ_max`, and everything harder
  about optimisation follows from that bound being tight.
- **102.** When the rules of the problem decide where you may stand, attach a price to
  each rule and look for a point where the total has no slope — then read the sign of the
  prices to find out which rules were actually doing any work.

## Common threads worth noticing

**The eigenvalue is the unit of account.** `λ_max` sets the safe step size in lesson 101
and the largest eigenvalue of the Hessian decides convexity in lesson 100. Learning to
compute and interpret a spectrum is therefore not optional background — it is the common
machinery underneath both lessons.

**Everything is a Hessian test.** Convexity of a quadratic (lesson 100), the stability
bound (lesson 101), and the second-order sufficient condition on the tangent space
(lesson 102) are all the same question asked about a different matrix. Learn it once.

**The boundary cases are the informative ones.** `η = 2/λ_max` freezes the stiffest
direction forever; a singular Hessian makes the second-order test *inconclusive*; a zero
multiplier on an equality constraint is fine while a negative one on an inequality means
your active set is wrong. Each lesson devotes real attention to what happens exactly at
the edge of a condition rather than comfortably inside it.

## Exercises

Every lesson ends with six or more worked exercises and full solutions in the same file,
so the repository is usable offline. Several are deliberately measurable rather than
proveable: you are asked to print the number and then explain why it is that number.

The most instructive exercise in the part is the Challenge of lesson 100, which writes a
routine that classifies a two-variable quadratic from its Hessian alone — and then shows,
from the printed `det` column alone, why a positive determinant cannot do the job. The
most satisfying is Exercise 2 of lesson 101, where the step count barely improves as the
learning rate nearly doubles, and the explanation is the condition number.

## A note on the code

Every numeric value printed in these lessons was produced by running the code shown.
Where a printed number appears in the prose it is the number the program actually emitted.
The check is automated, and it takes a few minutes for this part because lesson 101 runs
300,000-step descent trajectories on purpose:

```bash
python run_all.py 08        # every plain-Python block in this part
python run_all.py 08 --show # and print each block's output
```

## Where to go next

**[Part 09 — Number Theory and Cryptography](../part09_number_theory_crypto/)** starts
at [110 — Number Theory](../part09_number_theory_crypto/110_number_theory.md). This part
was about approximation and search; the next one is about arithmetic that is *exact*, so
it never rounds, never converges and never stalls.

**[Part 10 — Tensors and Numerical Methods](../part10_tensors_numerical/)** is the
practical bridge: it takes the iterations from lesson 101 and asks what floating-point
rounding does to them, which is why the condition number shows up there as a feasibility
question rather than a speed question. Lesson 121 of that part is the one that makes the
connection explicit — the same `λ_max/λ_min` that decides whether a descent method is
usable at all also decides whether a direct solve is worth reaching for.

For the notation, see [SYMBOLS.md](../SYMBOLS.md). The symbols used here that are not in
the general table — `∇`, the Hessian, a KKT multiplier — are defined where they appear.