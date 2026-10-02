# Part 10 — Tensors and Numerical Methods

The practical bridge between the mathematics and the code that runs it.

## What this part covers

Two lessons that take the mathematics of Parts 01 through 09 and put it into
the two types you actually write every day: the array, and the floating point
number. They are the last lesson in the repository because they are the point
at which every earlier idea meets the machine.

| # | Lesson | What it gives you |
| --- | --- | --- |
| 120 | [Tensors and Broadcasting](120_tensors_and_broadcasting.md) | Tensors as n-dimensional arrays, the rank/shape/axis/dtype vocabulary, the exact broadcasting rules and why they are shaped that way, three silent shape bugs that raise no exception, einsum notation and how to read it, reshape versus transpose, strides, C order versus Fortran order, view versus copy, and how all of it maps onto the tensor operations in PyTorch and JAX |
| 121 | [Numerical Methods and Floating Point](121_numerical_methods_and_floating_point.md) | IEEE 754 and machine epsilon, why `0.1 + 0.2 != 0.3` with the binary expansions shown, catastrophic cancellation with runnable demonstrations, absolute versus relative error, conditioning and the condition number, bisection with its error bound, Newton-Raphson with full code and a worked example, finite-difference truncation error and step-size choice, and how to pick tolerances you can actually meet |

## The two ideas that connect them

**The shape of a computation is part of the mathematics, and Python will not
check it for you.** Broadcasting will happily align a `(3, 1)` array against a
`(1, 5)` one and hand you a 3x5 result you did not intend, or quietly scale
the columns of a matrix when you meant to contract them. Every one of those
failures returns the right *type* with the wrong *contents*, and none of them
raises. Lesson 120 is about learning to see shapes before you operate on them,
and about `einsum`, which makes the shape a readable consequence of the
notation rather than something you have to remember.

**The number you get back is not the number you computed.** Lesson 120's
strides explain why `reshape` sometimes copies and sometimes does not. Lesson
121 explains why the copy that *does* happen matters: a float64 holds about 16
significant digits, most real numbers are not representable at all, and the
gap between representable numbers grows with magnitude. From that one fact
follows cancellation, conditioning, and the finite optimum step size for
numerical differentiation. The theme connecting the two lessons is that
floating point is not a slightly-approximate version of the arithmetic in
Parts 01 to 09. It is a different arithmetic, with different laws, and code
written for the first is often wrong in the second.

## What this part assumes

- [Lesson 30 — Vectors and Vector Spaces](../part03_linear_algebra/30_vectors_and_vector_spaces.md)
  and [Lesson 31 — Matrices and Matrix Algebra](../part03_linear_algebra/31_matrices_and_matrix_algebra.md)
  — the linear algebra that `einsum` notation makes explicit.
- [Lesson 40 — SVD and PCA](../part03_linear_algebra/40_svd_and_pca.md) — for the
  condition number as a ratio of singular values, and for the least-squares path
  when a system is ill conditioned.
- [Lesson 50 — Functions, Limits, and Continuity](../part04_calculus/50_functions_limits_continuity.md)
  — for the bisection precondition, and for what "converges" means.
- [Lesson 51 — Derivatives](../part04_calculus/51_derivatives.md) and
  [Lesson 54 — Taylor Series](../part04_calculus/54_taylor_series.md) — for the
  truncation error of a finite difference, which is a Taylor remainder.
- [Lesson 101 — Gradient Descent](../part08_optimization/101_gradient_descent.md)
  — for why regularisation is the answer to an ill-conditioned problem, since
  ridge regression minimises exactly that objective.
- [Lesson 111 — Modular Arithmetic and Public-Key Crypto](../part09_number_theory_crypto/111_modular_arithmetic_and_crypto.md)
  — for the contrast: modular arithmetic is exact and associative, and that is
  what Lesson 121 is measured against.
- [Lesson 113 — Error-Correcting Codes](../part09_number_theory_crypto/113_error_correcting_codes.md)
  — the prerequisite for the two lessons here, and the last exact-arithmetic
  lesson in the repository.
- For the notation, see [SYMBOLS.md](../SYMBOLS.md). The symbols used here that
  are not in the general table — a stride, an ulp, the order of convergence —
  are defined where they appear.

Nothing else. No prior numerical-analysis course is needed, and no library
beyond the Python standard library is required for any code that runs. Every
example builds its own broadcasting checker, its own `einsum`, its own bisection
and Newton solvers, and its own finite differences, so the mechanics are visible
before they are delegated.

## A suggested route

```
113 (exact arithmetic, the contrast)
  -> 120 (how arrays hold and align numbers)
       -> 121 (how those numbers are represented, and what that costs)
```

Read 120 first even though it is the "easier" topic. Almost every question in
121 becomes concrete once you have seen that a `float64` is a flat buffer of
about sixteen digits per element, because the same storage decision that makes
`reshape` free in one case and a copy in another is what makes an answer
eleven digits accurate instead of sixteen.

**Suggested study time.** Lesson 120 is 35 minutes of reading, Lesson 121 is 45,
so a first pass through the part is about **80 minutes** with the code open.
Add roughly **90 minutes** for the twelve exercises, which are the part's real
work — the questions in both lessons are measurable rather than proveable, and
you are asked to print the number and then explain why it is that number. The
`### With Libraries` subsections in 121 need numpy, scipy, matplotlib and
mpmath; they are optional, and nothing in the argument depends on them.

Verify the whole part at any time with:

```bash
python run_all.py part10_tensors_numerical
```

## Exercises

Every lesson ends with worked exercises and full solutions in the same file, so
the repository is usable offline. Several exercises are deliberately
measurable rather than proveable: you are asked to print the number and then
explain why it is that number.

The two most satisfying exercises in the part are Exercise 3 of Lesson 120,
where the identical bug is silent on square data and a loud error the moment
the data stops being square, and Exercise 3 of Lesson 121, which finds a
formula that returns exactly `0.0` for a root of size `1e-9`, repairs it two
ways that both land on `-1e-09`, and then shows that running the *broken*
version at 60 digits of `decimal` also gets the right answer — which is exactly
why more precision is not the fix.

## Where to go next

This is the last part, and that is deliberate — the repository ends where the
mathematics meets the machine. Four directions out from here, with the
prerequisites each one assumes:

- **Numerical linear algebra**, for the algorithms behind `np.linalg`. Go back
  to [Lesson 38 — Orthogonality and Least Squares](../part03_linear_algebra/38_orthogonality_and_least_squares.md)
  for why the normal equations square the condition number, and
  [Lesson 33 — Determinant and Inverse](../part03_linear_algebra/33_determinant_and_inverse.md)
  for the determinant as both an invertibility test and a condition-number
  approximation.
- **Numerical analysis**, for the convergence theory behind Lesson 121. The
  rigorous source of every truncation constant in it is
  [Lesson 54 — Taylor Series](../part04_calculus/54_taylor_series.md), and the
  integrals behind the quadrature rules are
  [Lesson 52 — Integration](../part04_calculus/52_integration.md).
- **Optimisation**, for the algorithmic face of conditioning:
  [Lesson 101 — Gradient Descent](../part08_optimization/101_gradient_descent.md)
  is where the condition number first appears as a *speed* question, and the
  stability bound `2/λ_max` is the same arithmetic as a stability bound.
- **Back to the [course index](../README.md)** to pick another part, or write a
  few of the exercise solutions yourself rather than reading them. The habit
  this part is really about is to check the condition number before reading the
  code: most of the time the code is fine and the problem cannot be solved to
  the precision you asked for.