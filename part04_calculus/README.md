# Part 04 — Calculus

Calculus is the mathematics of change and accumulation. It is not required to write
programs, but almost every interesting program eventually needs one of its three ideas:
a *slope* (how fast something changes), a *total* (how much of something there is), or
an *expansion* (an approximation to a hard function that is good near a point).

This part is the one where "all mathematics needed for computer science" earns its keep.
Optimisation, machine learning, numerical error analysis, signal processing, and graphics
are all calculus wearing different clothes. If you read only one part of this repository
for the practical benefit, read this one.

## What is in it

| # | Lesson | What you get out of it |
| --- | --- | --- |
| 50 | [Functions, Limits, and Continuity](50_functions_limits_continuity.md) | Functions as mappings, composition and inverses, epsilon-delta limits, continuity, and why bisection search needs a continuous function |
| 51 | [Derivatives](51_derivatives.md) | The limit definition, the rule table, the chain rule, implicit differentiation, numerical differentiation and its error, and **backpropagation as the chain rule applied to a network** |
| 52 | [Integration](52_integration.md) | Accumulation, the Fundamental Theorem, integration techniques, expectation as an integral, trapezoid and Simpson rules with error bounds, and why Monte Carlo converges at `1/sqrt(n)` |
| 53 | [Multivariable Calculus](53_multivariable_calculus.md) | Partial derivatives, the gradient as the direction of steepest ascent, Jacobians, divergence and curl, and gradient descent including the zero-initialisation trap |
| 54 | [Taylor Series](54_taylor_series.md) | Series, expansion points and convergence radii, the Lagrange remainder as a *guarantee*, Newton as first-order linearisation, and **catastrophic cancellation** |
| 55 | [Fourier Series and Transforms](55_fourier_series_and_transforms.md) | Sinusoids as a basis, the DFT written from scratch, a real radix-2 FFT, the convolution theorem, Gibbs' phenomenon, and frequency-domain filtering |

## What this part assumes

- **Part 01** (Logic and Proof) for the quantifiers and the word "for all". Limits are
  quantifier-heavy and cannot be read without them.
- **Part 03** (Linear Algebra) for vectors and matrices. Lesson 53 needs the Jacobian and
  the Hessian, and lesson 51's backpropagation section is much clearer if you are comfortable
  with matrix products.
- **Part 02** at the level of the binomial theorem, used implicitly in the Taylor
  expansions of $(1+x)^p$.
- Basic Python: arithmetic, functions, loops, `f`-strings. Nothing else.

## What it does not assume

No prior calculus. No probability. No numpy. Every plain-Python code block in this part
runs with the standard library alone and is checked automatically by
`python run_all.py`. Sections marked **With Libraries** use matplotlib or numpy for the
pictures and can be skipped entirely.

## The one-sentence version of each lesson

- **50.** A function is a machine; a limit is what it does as the input approaches a point it
  may never reach; continuity means those two agree.
- **51.** A derivative is a slope, measured as a limit you cannot take, so every code
  implementation is a compromise; and the chain rule is exactly what backpropagation runs.
- **52.** An integral is a signed total; the Fundamental Theorem says accumulate-then-
  differentiate gets you back where you started; and quadrature error is a power law.
- **53.** With many inputs there is one slope per input, and together they form an arrow
  that points uphill and crosses contour lines at right angles.
- **54.** A function can be rebuilt from its derivatives at one point; the first two terms
  are a straight line, which is all that Newton and gradient descent ever use; and
  truncating a series in floating point can destroy every digit you had.
- **55.** Any finite signal is exactly a sum of sinusoids; the FFT finds them in
  `N log N` instead of `N^2`; and in that basis, filtering means deleting coefficients.

## Where to go next

**[Part 05 — Probability and Statistics](../part05_probability_statistics/)**. This part
assumed clean signals and exact arithmetic. Real inputs are noisy and finite-precision, and
Part 05 is about how to say how much you trust a number. The two connect directly: lesson
52's expectation-as-integral is the continuous case of the sums in lesson 64, and the
`1/sqrt(n)` Monte Carlo rate from lesson 52 is the Central Limit Theorem of lesson 68.

**[Part 06 — Mathematics for Algorithms](../part06_algorithms_math/)**. If this part was
about *what* to compute, Part 06 is about *how fast*. The two share a boundary: the
`O(N^2)` versus `O(N log N)` gap that made the FFT worth writing appears in
[80 — Big-O and Complexity Analysis](../part06_algorithms_math/80_big_o_and_complexity.md),
and the cost of arithmetic on large integers there is the same floating-point caveat as
lesson 54, one layer down.

## A note on the code

Every numeric value printed in these lessons was produced by running the code shown.
Where a printed number appears in the prose it is the number the program actually emitted.
The check is automated:

```bash
python run_all.py 04        # every plain-Python block in this part
python run_all.py 04 --show # and print each block's output
```