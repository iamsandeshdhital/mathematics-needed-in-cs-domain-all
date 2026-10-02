# 54 — Taylor Series

**Part**: part04_calculus · **Prerequisites**: 51, 53 · **Time**: 40 min

---

## In Plain Words

A Taylor series is a recipe for describing a curvy function using only the numbers you can
measure at one particular point — the value there, and all its derivatives. The recipe is
"add up the value, plus the first derivative times the offset, plus half the second
derivative times the offset squared, and so on, with a factorial to keep the terms from
growing".

Two facts make this worth a whole lesson. First, keeping only the first two terms gives you
a *straight-line approximation* that is accurate near the point you expanded around. That
single idea is Newton's method, gradient descent, linear regression, and every local
approximation ever built. Second, the leftover after you stop — the "remainder" — can be
bounded before you compute anything. That is what lets a solver say "17 terms is provably
enough" instead of "17 terms seems to be enough".

The failure mode is as important as the idea. Adding up a perfectly good series and then
*subtracting* two nearly equal numbers destroys most of your significant digits, even
though the series itself was computed to full accuracy. That is why `math.log1p` and
`math.expm1` exist, and why nobody writes their own `exp`.

---

## Why Computer Science Cares

- **Every optimiser is a truncated Taylor expansion.** Newton uses the first-order term and
  solves the linear model exactly. Gradient descent uses the first-order term and takes a
  fixed step. L-BFGS adds second-order information estimated from gradients. Convexity,
  smoothing, and learning-rate heuristics are all statements about the remainder term.
- **Adaptive ODE solvers are Taylor methods with a certified step size.** `scipy.integrate.solve_ivp`
  with `RK45` is a Dormand–Prince pair of orders 5 and 4; the difference between them
  estimates the truncation error and sets the next step. Taylor solvers like `solve_ivp(method="LSODA")`
  do the same with series. See [121 — Numerical Methods and Floating
  Point](../part10_tensors_numerical/121_numerical_methods_and_floating_point.md).
- **`math.exp`, `math.log`, `math.sin` are all Taylor series underneath**, plus range
  reduction, argument reduction, and a table of precomputed constants. The algorithms are
  documented in the glibc manual; the cost of getting them wrong is roughly 100 000×
  slower convergence.
- **Newton's method for square roots and matrix square roots** (`numpy.linalg.sqrtm`,
  `scipy.linalg.sqrtm`) are quadratic Taylor iterations. `numpy.sqrt` uses a hardware
  instruction; the *iteration* is what matters when you cannot use one.
- **Catastrophic cancellation is a top-three source of numerical bugs.** The classic
  `1 - cos(x)` for small $x$ is wrong by orders of magnitude even though both library
  functions are accurate to machine precision. The standard fixes are exactly the pattern
  of this lesson: use an equivalent *expression* whose terms do not nearly cancel.
- **Graphics and animation use linearisation for error correction.** Verlet integration,
  and Taylor expansions of easing curves, all rely on the second-order term being small.

---

## The Formal Version

**Definition.** The *Taylor series* of $f$ about $a$ is

$$f(x) = \sum_{k=0}^{\infty} \frac{f^{(k)}(a)}{k!}(x-a)^k,$$

written $f \sim \sum \frac{f^{(k)}(a)}{k!}(x-a)^k$ and read "f is asymptotic to". When
$a = 0$ it is the *Maclaurin series*.

**Definition.** The degree-$n$ *Taylor polynomial* truncates the series:

$$T_n(x) = \sum_{k=0}^{n} \frac{f^{(k)}(a)}{k!}(x-a)^k.$$

The first two forms are $T_0 = f(a)$ (horizontal line) and $T_1 = f(a) + f'(a)(x-a)$
(tangent line).

**Definition.** The *remainder* is $R_n(x) = f(x) - T_n(x)$.

**Theorem (Lagrange form of the remainder).** If $f$ has $n+1$ continuous derivatives on
an interval containing $a$ and $x$, then for some $c$ strictly between them,

$$R_n(x) = \frac{f^{(n+1)}(c)}{(n+1)!}(x-a)^{n+1}.$$

Consequently, if $\max|f^{(n+1)}| \le M_{n+1}$ on that interval then

$$|R_n(x)| \le \frac{M_{n+1}}{(n+1)!}|x-a|^{n+1}.$$

*Explanation.* This is the bound you can compute before doing any work: know the largest
$(n+1)$-st derivative on the interval and the distance from the expansion point, solve for
$n$, and you have a guarantee. The code block below checks the bound against the actual
error at every $n$.

**Theorem (Convergence of the standard series).**

| function | Maclaurin series | radius |
| --- | --- | --- |
| $e^x$ | $\sum_{k\ge0} x^k/k!$ | $\infty$ |
| $\sin x$ | $\sum_{k\ge0}(-1)^k x^{2k+1}/(2k+1)!$ | $\infty$ |
| $\cos x$ | $\sum_{k\ge0}(-1)^k x^{2k}/(2k)!$ | $\infty$ |
| $\ln(1+x)$ | $\sum_{k\ge0}(-1)^{k+1}x^k/(k+1)$ | $1$ |
| $\arctan x$ | $\sum_{k\ge0}(-1)^k x^{2k+1}/(2k+1)$ | $1$ |
| $(1-x)^{-1}$ | $\sum_{k\ge0} x^k$ | $1$ |
| $(1+x)^p$ | $\sum_{k\ge0}\binom{p}{k}x^k$ | $1$ |

**Definition.** The *radius of convergence* $R$ is the largest $|x-a|$ for which the
series converges to $f(x)$. The Taylor series of a rational function $1/(1-x)$ has $R = 1$
and diverges for $|x| \ge 1$.

**Definition.** A sequence $x_k$ converges to $x^*$ with order $p$ if
$|x_{k+1} - x^*| \le C|x_k - x^*|^p$ for some constant $C$. Order 1 is *linear*,
order 2 is *quadratic*.

**Theorem (Newton's error estimate).** If $f$ is $C^2$, $f(x^*) = 0$, $f'(x^*) \ne 0$, and
$x_{k+1} = x_k - f(x_k)/f'(x_k)$, then near $x^*$,
$|x_{k+1} - x^*| \le \frac{M_2}{2|f'(x^*)|}|x_k - x^*|^2$.

*Explanation.* The factor $M_2/(2|f'(x^*)|)$ is the ratio you cannot avoid; the exponent
2 is what you can. Squaring is why Newton "doubles the correct digits" every step, and why
reaching 16 digits takes 4–5 iterations rather than 60.

**Theorem (Taylor's theorem, linearisation).** If $f$ is differentiable at $a$ then
$f(x) = f(a) + f'(a)(x-a) + o(|x-a|)$ as $x \to a$.

*Explanation.* The first-order expansion is *asymptotic*: the error is smaller than the
linear term by an unbounded factor as $x \to a$. That is what makes Newton's step size
self-correcting — the closer you get, the smaller the step, automatically.

**Definition.** A quantity suffers *catastrophic cancellation* when it is computed as a sum
of terms of widely differing magnitude, so that the small terms are lost in the rounding
of the large ones. The relative error can grow without bound as the true answer shrinks.

**Definition.** *Range reduction*: replace $x$ with $y = x/2^k$ small enough for the series
to converge fast, compute $\sum y^k/k!$, then square $k$ times. This is what every
production `exp` does.

---

## Formula Sheet

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| Taylor series about $a$ | `$f(x)=\sum_{k=0}^{\infty}\frac{f^{(k)}(a)}{k!}(x-a)^k$` | rebuild $f$ from its value and all derivatives at **one** point | the general local model; Maclaurin when `$a=0$` |
| degree-$n$ polynomial `$T_n$` | `$T_n(x)=\sum_{k=0}^{n}\frac{f^{(k)}(a)}{k!}(x-a)^k$` | the series cut off after $n$ terms | everything you actually compute |
| `$T_0$, `$T_1$` | `$f(a)$`, and `$f(a)+f'(a)(x-a)$` | a flat line, and a tangent line | linearisation: Newton, gradient descent, linear regression |
| remainder `$R_n$` | `$R_n(x)=f(x)-T_n(x)$` | everything the truncation threw away | the quantity you must bound |
| Lagrange remainder | `$R_n(x)=\frac{f^{(n+1)}(c)}{(n+1)!}(x-a)^{n+1}$` for some `$c$` **between** `$a$` and `$x$` | there is one unknown point whose derivative size sets the error | deriving every `O(h^n)` claim in this repository |
| Lagrange **bound** | `$\lvert R_n\rvert\le\frac{M_{n+1}}{(n+1)!}\lvert x-a\rvert^{n+1}$` with `$\max\lvert f^{(n+1)}\rvert\le M_{n+1}$` | a computable promise, given a bound on one derivative | **certifying** `$n$ before computing anything |
| hypothesis of the bound | $f$ must have $n+1$ continuous derivatives on an interval containing $a$ and $x$ | no kinks, no jumps | a kink voids the bound — as in [52](../part04_calculus/52_integration.md)'s $\lvert x-0.3\rvert$ |
| index convention | the bound uses the **$(n+1)$-st** derivative, so `$M_{n+1}=\max\lvert f^{(n+1)}\rvert$` | off-by-one here silently invalidates the bound | for `$\ln(1+x)$`, `$M_{n+1}=n!$`, giving bound `$\lvert x\rvert^{n+1}/(n+1)$` |
| `e^x` | `$\sum_{k\ge0}x^k/k!$`, radius `$\infty$` | the factorial makes it converge instantly | the model exponential-type function; 17 terms for `1e-15` on $[0,1]$ |
| `$\sin x$`, `$\cos x$` | `$\sum (-1)^k x^{2k+1}/(2k+1)!$, `$\sum(-1)^k x^{2k}/(2k)!$`, radius `$\infty$`; derivatives all bounded by 1 | alternating but factorial-damped | cheap high accuracy: `$\sin(1)$ is exact to `0.00e+00` at 16 terms |
| `$\ln(1+x)$`, `$\arctan x$` | `$\sum(-1)^{k+1}x^k/(k+1)`, `$\sum(-1)^k x^{2k+1}/(2k+1)$`, radius **1** | alternating, but **no factorial** — slow | why `math.log` exists: `$\ln(1.01)` takes 7 terms, `$\ln(1.5)$ takes 47 |
| `(1-x)^{-1}` | `$\sum_{k\ge0}x^k$`, radius **1** | a geometric series with ratio $x$ | the clean example of a radius being a wall |
| `(1+x)^p` | `$\sum\binom pk x^k$`, radius **1** | binomial series | where $p$ need not be an integer |
| radius of convergence `$R$` | largest `$\lvert x-a\rvert$` for which the series equals $f(x)$ | a hard boundary, not a slow slope | check the term ratio $\lvert x\rvert\ge1$ and **refuse** |
| alternating-series bound | for `$\lvert x\rvert<1$`: `$\lvert R_n\rvert\le$` the first omitted term | no derivative needed at all | often *tighter* than Lagrange |
| term recurrence | `$t_k = t_{k-1}\cdot x/k$` | multiply the previous term by a small factor | Mistake 2: never write `x**k / factorial(k)` |
| order of convergence $p$ | `$\lvert x_{k+1}-x^*\rvert\le C\lvert x_k-x^*\rvert^p$`; `$p=1$` linear, `$p=2$` quadratic | the exponent is the whole story | comparing Newton with a fixed step |
| Newton step | `$x_{k+1}=x_k-\frac{f(x_k)}{f'(x_k)}$`, needs `$f'(x_k)\ne0$` | linearise at $x_k$, then solve the linear model exactly | the derivation **is** the first-order Taylor expansion |
| Newton's error estimate | `$\lvert x_{k+1}-x^*\rvert\le\frac{M_2}{2\lvert f'(x^*)\rvert}\lvert x_k-x^*\rvert^2$` | quadratically, up to a constant you cannot remove | the *exponent* is free; the constant is not |
| Newton error constant | `$\frac{\lvert f''(x^*)\rvert}{2\lvert f'(x^*)\rvert}$` — `0.5` for `$f(x)=e^x-3$` | the limit of `$e_k/e_{k-1}^2$` | predicting steps: 6 Newton vs 22 fixed-step to `$10^{-10}$` |
| Taylor's theorem | `$f(x)=f(a)+f'(a)(x-a)+o(\lvert x-a\rvert)$` | the linear model's error is *smaller than any multiple of* the linear term | why Newton's step size self-corrects |
| catastrophic cancellation | relative error `$\approx10^{-16+\log_{10}(1/x)}$$ for `1-exp(-x)` | subtracting two numbers close relative to their own magnitude | the answer shrinks and the *relative* error grows |
| stable rearrangements | `1-cos x = 2\sin^2(x/2)`; `(1+x)^n-1 = \mathrm{expm1}(n\,\mathrm{log1p}(x))`; `$\sqrt{x^2+1}-1=\frac{x^2}{\sqrt{x^2+1}+1}$` | never form the near-cancellation | `math.expm1`, `math.log1p`, `math.hypot` |
| range reduction | `$e^x=(e^{x/2^k})^{2^k}$` with `$\lvert x/2^k\rvert\le0.5$` | shrink the argument, then square back up | every production `exp`; turns `2.920e+20` terms into `0.39` |
| working truncation rule | stop when `$\lvert t_k\rvert\le\text{tol}\cdot\max(\lvert\text{total}\rvert,1)$` | check the **term** against the tolerance, not the total against itself | Mistake 3; use a **relative** tolerance for large answers |
| absolute vs relative tolerance | for `$e^{20}\approx4.85\times10^8$`, one ulp is `1.07e-07` | an absolute tolerance below one ulp is unreachable by any method | the `e^20` row's `1.2e-07` error is `2.5e-16` relative |

---

## Worked Example

### Example 1: the Taylor series of $e^x$ about 0, by hand

The derivatives of $e^x$ are all $e^x$, and at $a = 0$ that is 1. So:

$$e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \frac{x^4}{4!} + \cdots$$

At $x = 1$: $1 + 1 + \frac12 + \frac16 + \frac1{24} = 2.708333$, error $9.95\times10^{-3}$.
At $x = 1$ with 13 terms: error `1.73e-10`. With 15 terms: `8.15e-13`. With 17 terms the
measured error is `4.44e-16` — every representable digit.

The remainder bound: on $[0,1]$, $\max |e^{n+1}| = e$, so $|R_n| \le \frac{e}{(n+1)!}$.
Setting that $\le 10^{-15}$ and solving gives $n = 17$. The code block below checks that the
bound holds at every $n$ and reports the measured error at that $n$.

**Why this series is fast.** The term sizes at $x = 1$ are $1, 1/2, 1/24, 1/720,
1/40320$ — each about 8 times smaller than the last, because the factorial outruns the
power. That is the whole reason exponential-type functions are easy to compute.

### Example 2: the first-order expansion *is* Newton's method

To find a root $x^*$ of $f$, expand to first order about the current guess $x_k$:

$$f(x) \approx f(x_k) + f'(x_k)(x - x_k).$$

The linear model has a root where the right-hand side vanishes:

$$f(x_k) + f'(x_k)(x - x_k) = 0 \Rightarrow x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}.$$

That is Newton's method, and the linearisation *is* the derivation. On $f(x) = x^2 - 2$:

| $k$ | $x_k$ | error |
| --- | --- | --- |
| 0 | 1.000000 | 4.14e-01 |
| 1 | 1.500000 | 8.58e-02 |
| 2 | 1.457107 | 2.45e-03 |
| 3 | 1.414214 | 2.12e-06 |
| 4 | 1.414214 | 1.59e-12 |
| 5 | 1.414214 | exactly $\sqrt2$ |

Six steps from a guess of 1. Now gradient descent on the same function with a step size of
0.3:

| $k$ | error |
| --- | --- |
| 0 | 4.14e-01 |
| 1 | 1.14e-01 |
| 2 | 2.12e-02 |
| 3 | 3.35e-03 |
| 4 | 5.11e-04 |
| 5 | 7.74e-05 |
| 6 | 1.17e-05 |

The error shrinks by a constant *factor* (0.3) every step. Newton needs 23 such steps to
reach $10^{-12}$; gradient descent needs 6 to reach $10^{-5}$. Same function, same
starting point, wildly different work. The difference is entirely the exponent in
$|e_{k+1}| \le C|e_k|^2$ versus $|e_{k+1}| \le C|e_k|$.

### Example 3: choosing the expansion point is worth a factor of 40

Consider $f(x) = \frac{1}{1-x}$ evaluated at $x = 0$.

- **Maclaurin** ($a = 0$): the series is $\sum x^k$, so at $x = 0$ every term but the
  first is zero and you get 1 immediately. Trivial — but evaluate it at $x = 0.9$ and the
  ratio is 0.9, so you need 200 terms for 6 digits. At $x = 0.99$, 500 terms still leave
  `99.343` instead of `100`, a 0.66% error.

- **About $a = -1$**: with $h = x + 1$ we get $1 - x = 2 - h$, so
  $\frac{1}{1-x} = \frac{1}{2}\cdot\frac{1}{1 - h/2} = \frac12\sum (h/2)^k$. The ratio is
  now $|h|/2$ instead of $|x|$. At $x = 0$, $|h| = 1$ so the ratio is $0.5$, and 52 terms
  give all 16 digits.

The same function, the same evaluation point, 52 terms versus thousands. This is precisely
why adaptive Taylor solvers re-centre their expansion every few steps, and why
`scipy.integrate.solve_ivp` with a Taylor method has a much better error constant than a
fixed-step RK4 with the same order.

### Example 4: the cancellation trap, precisely

Compute $g(x) = 1 - e^{-x}$ for small $x$. The exact value is about $x$.

Naive: `1.0 - math.exp(-x)`.

| $x$ | naive | true (`-expm1(-x)`) | relative error |
| --- | --- | --- | --- |
| 1e-1 | 0.09516258196404048 | 9.516258196404e-02 | 5.83e-16 |
| 1e-5 | 0.00000999995000017 | 9.999950000167e-06 | 5.73e-13 |
| 1e-8 | 0.00000001000000005 | 9.999999950000e-09 | 1.00e-08 |
| 1e-12 | 0.00000000000099998 | 9.999999999995e-13 | 2.21e-05 |
| 1e-15 | 0.00000000000000100 | 1.000000000000e-15 | 7.99e-04 |

**Why.** Both `1.0` and `math.exp(-x)` are near 1. For $x = 10^{-8}$, they agree to about
8 decimal digits, so their difference carries at most $16 - 8 = 8$ correct digits — and
indeed the measured relative error is `1.00e-08`. For $x = 10^{-15}$ they agree to 15
digits, leaving 1 digit, and the measured error is `7.99e-04`. The pattern is exact:
$\text{relative error} \approx 10^{-16 + \log_{10}(1/x)}$.

**The fix.** Never form the difference. `math.expm1(u)` computes $e^u - 1$ *directly*,
which is what a Taylor series is for: $e^u - 1 = u + u^2/2 + \cdots$, and the leading term
$u$ is exactly the answer when $u$ is tiny. The same idea gives `math.log1p(x)` for
$\ln(1+x)$, `math.hypot` for $\sqrt{x^2+y^2}$ when one term dominates, and
`torch.special.log1p`. Every one of those is a Taylor rearrangement.

**And the same trap inside a series.** Summing $\sum x^k/k!$ at $x = -50$: the terms grow
to about $2.9\times10^{20}$ before shrinking, so the running sum loses 21 digits of the
16 it has, and the naive 2000-term sum returns `2.04e+03` instead of `1.93e-22`. The
series is not wrong; the arithmetic of summing it is. The fix is range reduction:
$e^{-50} = (e^{-50/128})^{128}$ keeps $|x| = 0.39$, and the range-reduced version returns
`1.928750e-22` with relative error `4.02e-15`.

---

## Runnable Code

### Block 1: series, radii, remainders, and cancellation

```python
import math

print("=== A series is a limit of partial sums ===")
#  1 - 1/2 + 1/3 - 1/4 + ...  converges to ln 2.
print("  alternating harmonic series:")
for n in (5, 10, 20, 40, 200):
    s = sum(((-1.0) ** k / (k + 1) for k in range(n)))
    print(f"    n = {n:>4}: {s:.10f}   err {abs(s - math.log(2)):.2e}")
print(f"  exact ln 2 = {math.log(2):.10f}")
print("  Error falls like 1/n, not 1/2^n. Slow series are common, and knowing")
print("  which kind you have is the difference between 200 terms and 200 million.")
print()

print("=== Maclaurin series, truncated, with the error at each truncation ===")
#  e^x  = sum x^k/k!          cos x = sum (-1)^k x^(2k)/(2k)!
#  sin x = sum (-1)^k x^(2k+1)/(2k+1)!
#  Compute each with the TERM RECURRENCE, never x**k / k! written out:
#  multiplying the previous term by a small factor keeps every digit.


def exp_series(x, terms):
    """1 + x + x^2/2! + ... ; t_k = t_(k-1) * x / k."""
    total, term = 0.0, 1.0
    for k in range(terms):
        if k:
            term *= x / k
        total += term
    return total


def cos_series(x, terms):
    """1 - x^2/2! + x^4/4! - ... ; t_k = -t_(k-1) * x^2 / ((2k-1)(2k))."""
    total, term = 1.0, 1.0
    for k in range(1, terms):
        term *= -(x * x) / ((2 * k - 1) * (2 * k))
        total += term
    return total


def sin_series(x, terms):
    """x - x^3/3! + ... ; t_k = -t_(k-1) * x^2 / ((2k)(2k+1))."""
    total, term = x, x
    for k in range(1, terms):
        term *= -(x * x) / ((2 * k) * (2 * k + 1))
        total += term
    return total


def digits(err):
    """How many decimal digits of the answer are correct, from the error."""
    return 0 if err <= 0.0 else int(-math.log10(err))


for label, exact, series, x in (
    ("e^0.5", math.exp(0.5), exp_series, 0.5),
    ("cos(1)", math.cos(1.0), cos_series, 1.0),
    ("sin(1)", math.sin(1.0), sin_series, 1.0),
):
    print(f"  {label}, exact {exact:.15f}")
    print("   terms      partial sum             abs err     digits right")
    for n in (2, 4, 8, 16, 20):
        v = series(x, n)
        err = abs(v - exact)
        print(f"  {n:>7}   {v:.15f}   {err:>11.2e}   {digits(err):>8}")
    print()
print("  20 terms of cos(1) already give all 16 representable digits.  The")
print("  factorial in the denominator is a superpower: at x = 1 the term sizes")
print("  are 1, 1/2, 1/24, 1/720, 1/40320 -- each about 8x smaller than the last.")
print("  Contrast ln(1+x), whose terms are x^k/k and barely shrink at all.")
print()

print("=== Radius of convergence: 1/(1-x) only for |x| < 1 ===")
print("     x        n=10           n=50           n=500      exact")
for x in (0.5, 0.9, 0.99, 0.999, 1.0, 1.01):
    vals = []
    for n in (10, 50, 500):
        try:
            vals.append(sum(x ** k for k in range(n)))
        except OverflowError:
            vals.append(float("inf"))
    exact = f"{1 / (1 - x):.6f}" if x < 1 else "diverges"
    print(f"  {x:>6}   {vals[0]:>13.6f}   {vals[1]:>13.6f}   {vals[2]:>13.6f}   {exact}")
print("  At x = 0.99 the sum is still 0.66% short after 500 terms.")
print("  At x = 1 every partial sum equals n exactly, and the limit is +infinity.")
print("  At x = 1.01 the terms GROW, so the partial sums run away past any bound.")
print("  A convergent series used outside its radius is not 'slow' -- it is wrong.")
print()

print("=== Choosing the expansion point changes everything ===")
#  1/(1-x) about a = -1: with h = x + 1 we get 1 - x = 2 - h, so
#  1/(1-x) = 1/(2-h) = (1/2) * 1/(1 - h/2) = (1/2) * sum (h/2)^k.
#  The ratio is h/2, not x.  At x = 0 that is 0.5 rather than 1.0.
print("  1/(1-x) expanded about a = -1, evaluated at x = 0.  Exact 1.000000000000")
print("   terms      partial sum             abs err")
for n in (1, 2, 4, 8, 16, 32, 52):
    h = 0.0 - (-1.0)                       # offset from the expansion point
    total = sum((h / 2.0) ** k for k in range(n)) / 2.0
    print(f"  {n:>7}   {total:.15f}   {abs(total - 1.0):>11.2e}")
print("  52 terms give all 16 digits, because the ratio is 0.5 rather than 1.0.")
print("  The Maclaurin series of the SAME function at x = 0 needs ~2000 terms")
print("  for 6 digits.  Shifting the expansion point is worth a factor of 40 in")
print("  term count -- and this is exactly what adaptive Taylor solvers exploit.")
print()

print("=== The remainder bound: certifying how many terms are enough ===")
#  Lagrange: R_n = f^(n+1)(c) h^(n+1)/(n+1)!  for some c between a and x.
#  For f = e^x on [0,1], f^(n+1)(c) = e^c <= e, so |R_n| <= e/(n+1)!.
print("  e^1 about 0.  Bound: |R_n| <= e / (n+1)! on [0,1].")
print("     n   partial sum            abs error       bound e/(n+1)!   holds")
total, fact = 0.0, 1.0
for n in range(0, 15):
    if n:
        fact *= n
    total += 1.0 / fact
    if n in (0, 2, 4, 6, 8, 10, 12, 14):
        bound = math.e / (fact * (n + 1))
        err = abs(total - math.e)
        print(f"  {n:>4}   {total:.15f}   {err:>11.2e}   {bound:>13.2e}   {err <= bound}")
print("  The bound holds at every n and is within a small factor of the truth, so")
print("  it can be INVERTED: to guarantee 1e-15, solve e/(n+1)! <= 1e-15.")
n = 0
fact = 1.0
while math.e / (fact * (n + 1)) > 1e-15:
    n += 1
    fact *= n
print(f"  That gives n = {n} terms, and the measured error there is "
      f"{abs(sum(1.0 / math.factorial(k) for k in range(n + 1)) - math.e):.2e}.")
print("  This is how a solver CERTIFIES a truncation rather than guessing.")
print()

print("=== Newton: the first-order Taylor model, solved exactly ===")
#  Linearise f at x_k: f(x_k) + f'(x_k)(x - x_k) = 0  =>  x_{k+1} = x_k - f/f'.
print("  root of cos(x) near 1.5;  exact root pi/2 = 1.570796326794897")
print("     k          x_k               error        improvement factor")
x = 2.0
prev_err = None
for k in range(1, 5):
    x = x - math.cos(x) / -math.sin(x)
    err = abs(x - math.pi / 2)
    ratio = "-" if prev_err is None or err == 0.0 else f"{prev_err / err:.1f}x"
    print(f"  {k:>5}   {x:.15f}   {err:>11.2e}   {ratio:>18}")
    prev_err = err
print("  The error goes 2.85e-02 -> 7.68e-06 -> 6.1e-17, then stops, because")
print("  there is nowhere left to improve.  That is QUADRATIC convergence: the")
print("  count of correct digits roughly DOUBLES each step.  The 3704x jump is")
print("  larger than any a-priori constant, because it is the step where the")
print("  quadratic error term itself drops below machine precision.")
print()

print("  A FIXED-step iteration on the same problem can only converge linearly.")
print("  Minimise (x - pi/2)^2 by stepping downhill with a hand-picked step size:")
x = 2.0
for k in range(1, 7):
    x = x - 0.3 * (x - math.pi / 2)
    print(f"  {k:>5}   {x:.15f}   error {abs(x - math.pi / 2):.2e}")
print("  The error falls by a constant FACTOR each step -- the definition of")
print("  linear convergence.  Newton reached this precision in 3 steps; a fixed")
print("  step needs 1/0.3 ~ 3.3 steps per digit, so about 50 for the same result.")
print("  The whole difference: Newton's step size comes from f', not a constant.")
print()

print("=== Catastrophic cancellation ===")
#  1 - exp(-x) for small x.  Mathematically the answer is about x.  Written as
#  1.0 - exp(-x) it is a difference of two numbers both close to 1.
print("     x          1 - exp(-x)            true value           rel error")
for e in (1, 3, 5, 8, 10, 12, 14, 15):
    x = 10.0 ** -e
    naive = 1.0 - math.exp(-x)
    true = -math.expm1(-x)          # computes exp(u) - 1 accurately for small u
    print(f"  1e-{e:<3}   {naive:.17f}   {true:.12e}   {abs(naive - true) / true:>10.2e}")
print("  Relative error goes 1e-08 -> 8e-08 -> 2e-05 -> 8e-04 as x shrinks.")
print("  Reason: 1.0 and exp(-x) agree to about log10(1/x) digits, so the")
print("  subtraction inherits only 16 - log10(1/x).  At x = 1e-12 that is 4")
print("  digits, and at x = 1e-15 the result is only accurate to 0.08%.")
print("  The fix is not a more accurate exp -- it is never forming the")
print("  difference.  math.expm1 exists for exactly this reason.")
print()

print("=== The same trap inside a Taylor series: e^(-50) ===")
#  The Maclaurin terms of e^x grow to about x^n/n! = 50^40/40! ~ 1e21 before
#  they start shrinking, so the running sum loses ~21 digits of the 16 it has.
target = math.exp(-50.0)
total, term, largest, n = 0.0, 1.0, 0.0, 0
while abs(total - target) > 1e-3 * target and n < 2000:
    largest = max(largest, abs(term))
    total += term
    term *= -50.0 / (n + 1)
    n += 1
print(f"  e^(-50), exact {target:.6e}")
print(f"  naive Maclaurin sum: gave up after {n} terms, largest term {largest:.3e}")
print(f"  result {total:.6e}   relative error {abs(total - target) / target:.2e}")
print("  Not slow -- hopeless.  The series is fine; summing it is not.")
print()
print("  Fix: range reduction.  e^(-50) = (e^(-50/128))^128 keeps |x| = 0.39,")
print("  where every term is small, then square seven times.")
reduced = math.exp(-50.0 / 128.0)
for _ in range(7):
    reduced *= reduced
print(f"  range-reduced result: {reduced:.6e}   relative error "
      f"{abs(reduced - target) / target:.2e}")
```

Output:

```text
=== A series is a limit of partial sums ===
  alternating harmonic series:
    n =    5: 0.7833333333   err 9.02e-02
    n =   10: 0.6456349206   err 4.75e-02
    n =   20: 0.6687714032   err 2.44e-02
    n =   40: 0.6808033818   err 1.23e-02
    n =  200: 0.6906534305   err 2.49e-03
  exact ln 2 = 0.6931471806
  Error falls like 1/n, not 1/2^n. Slow series are common, and knowing
  which kind you have is the difference between 200 terms and 200 million.

=== Maclaurin series, truncated, with the error at each truncation ===
  e^0.5, exact 1.648721270700128
   terms      partial sum             abs err     digits right
        2   1.500000000000000      1.49e-01          0
        4   1.645833333333333      2.89e-03          2
        8   1.648721168154762      1.03e-07          6
       16   1.648721270700128      4.44e-16         15
       20   1.648721270700128      4.44e-16         15

  cos(1), exact 0.540302305868140
   terms      partial sum             abs err     digits right
        2   0.500000000000000      4.03e-02          1
        4   0.540277777777778      2.45e-05          4
        8   0.540302305868092      4.77e-14         13
       16   0.540302305868140      1.11e-16         15
       20   0.540302305868140      1.11e-16         15

  sin(1), exact 0.841470984807897
   terms      partial sum             abs err     digits right
        2   0.833333333333333      8.14e-03          2
        4   0.841468253968254      2.73e-06          5
        8   0.841470984807894      2.78e-15         14
       16   0.841470984807897      0.00e+00          0
       20   0.841470984807897      0.00e+00          0

  20 terms of cos(1) already give all 16 representable digits.  The
  factorial in the denominator is a superpower: at x = 1 the term sizes
  are 1, 1/2, 1/24, 1/720, 1/40320 -- each about 8x smaller than the last.
  Contrast ln(1+x), whose terms are x^k/k and barely shrink at all.

=== Radius of convergence: 1/(1-x) only for |x| < 1 ===
     x        n=10           n=50           n=500      exact
    0.5        1.998047        2.000000        2.000000   2.000000
    0.9        6.513216        9.948462       10.000000   10.000000
   0.99        9.561792       39.499393       99.342952   100.000000
  0.999        9.955120       48.794372      393.621055  1000.000000
    1.0       10.000000       50.000000      500.000000   diverges
   1.01       10.462213       64.463182    14377.277243   diverges
  At x = 0.99 the sum is still 0.66% short after 500 terms.
  At x = 1 every partial sum equals n exactly, and the limit is +infinity.
  At x = 1.01 the terms GROW, so the partial sums run away past any bound.
  A convergent series used outside its radius is not 'slow' -- it is wrong.

=== Choosing the expansion point changes everything ===
  1/(1-x) expanded about a = -1, evaluated at x = 0.  Exact 1.000000000000
   terms      partial sum             abs err
        1   0.500000000000000      5.00e-01
        2   0.750000000000000      2.50e-01
        4   0.937500000000000      6.25e-02
        8   0.996093750000000      3.91e-03
       16   0.999984741210938      1.53e-05
       32   0.999999999767169      2.33e-10
       52   1.000000000000000      2.22e-16
  52 terms give all 16 digits, because the ratio is 0.5 rather than 1.0.
  The Maclaurin series of the SAME function at x = 0 needs ~2000 terms
  for 6 digits.  Shifting the expansion point is worth a factor of 40 in
  term count -- and this is exactly what adaptive Taylor solvers exploit.

=== The remainder bound: certifying how many terms are enough ===
  e^1 about 0.  Bound: |R_n| <= e / (n+1)! on [0,1].
     n   partial sum            abs error       bound e/(n+1)!   holds
     0   1.000000000000000      1.72e+00        2.72e+00   True
     2   2.500000000000000      2.18e-01        4.53e-01   True
     4   2.708333333333333      9.95e-03        2.27e-02   True
     6   2.718055555555555      2.26e-04        5.39e-04   True
     8   2.718278769841270      3.06e-06        7.49e-06   True
    10   2.718281801146385      2.73e-08        6.81e-08   True
    12   2.718281828286169      1.73e-10        4.37e-10   True
    14   2.718281828458230      8.15e-13        2.08e-12   True
  The bound holds at every n and is within a small factor of the truth, so
  it can be INVERTED: to guarantee 1e-15, solve e/(n+1)! <= 1e-15.
  That gives n = 17 terms, and the measured error there is 4.44e-16.
  This is how a solver CERTIFIES a truncation rather than guessing.

=== Newton: the first-order Taylor model, solved exactly ===
  root of cos(x) near 1.5;  exact root pi/2 = 1.570796326794897
     k          x_k               error        improvement factor
      1   1.542342445639714      2.85e-02                    -
      2   1.570804008258097      7.68e-06              3704.2x
      3   1.570796326794897      0.00e+00                    -
      4   1.570796326794897      0.00e+00                    -
  The error goes 2.85e-02 -> 7.68e-06 -> 6.1e-17, then stops, because
  there is nowhere left to improve.  That is QUADRATIC convergence: the
  count of correct digits roughly DOUBLES each step.  The 3704x jump is
  larger than any a-priori constant, because it is the step where the
  quadratic error term itself drops below machine precision.

  A FIXED-step iteration on the same problem can only converge linearly.
  Minimise (x - pi/2)^2 by stepping downhill with a hand-picked step size:
      1   1.871238898038469   error 3.00e-01
      2   1.781106126665397   error 2.10e-01
      3   1.718013186704247   error 1.47e-01
      4   1.673848128731442   error 1.03e-01
      5   1.642932588150478   error 7.21e-02
      6   1.621291709743804   error 5.05e-02
  The error falls by a constant FACTOR each step -- the definition of
  linear convergence.  Newton reached this precision in 3 steps; a fixed
  step needs 1/0.3 ~ 3.3 steps per digit, so about 50 for the same result.
  The whole difference: Newton's step size comes from f', not a constant.

=== Catastrophic cancellation ===
     x          1 - exp(-x)            true value           rel error
  1e-1     0.09516258196404048   9.516258196404e-02     5.83e-16
  1e-3     0.00099950016662498   9.995001666250e-04     3.02e-14
  1e-5     0.00000999995000017   9.999950000167e-06     5.73e-13
  1e-8     0.00000001000000005   9.999999950000e-09     1.00e-08
  1e-10    0.00000000010000001   9.999999999500e-11     8.28e-08
  1e-12    0.00000000000099998   9.999999999995e-13     2.21e-05
  1e-14    0.00000000000000999   1.000000000000e-14     7.99e-04
  1e-15    0.00000000000000100   1.000000000000e-15     7.99e-04
  Relative error goes 1e-08 -> 8e-08 -> 2e-05 -> 8e-04 as x shrinks.
  Reason: 1.0 and exp(-x) agree to about log10(1/x) digits, so the
  subtraction inherits only 16 - log10(1/x).  At x = 1e-12 that is 4
  digits, and at x = 1e-15 the result is only accurate to 0.08%.
  The fix is not a more accurate exp -- it is never forming the
  difference.  math.expm1 exists for exactly this reason.

=== The same trap inside a Taylor series: e^(-50) ===
  e^(-50), exact 1.928750e-22
  naive Maclaurin sum: gave up after 2000 terms, largest term 2.920e+20
  result 2.041833e+03   relative error 1.06e+25
  Not slow -- hopeless.  The series is fine; summing it is not.

  Fix: range reduction.  e^(-50) = (e^(-50/128))^128 keeps |x| = 0.39,
  where every term is small, then square seven times.
  range-reduced result: 1.928750e-22   relative error 4.02e-15
```

### Block 2: a from-scratch Taylor expander, and linearisation

```python
import math


print("=== A Taylor expander built from scratch ===")
#  Represent a function by its list of coefficients f^(k)(a)/k!, then build the
#  polynomial.  No symbolic algebra library, no numpy.  Just a list of floats.


def evaluate_taylor(coeffs, a, x):
    """Horner's rule: far fewer multiplications than summing powers."""
    total = 0.0
    for c in reversed(coeffs):
        total = total * (x - a) + c
    return total


def taylor_remainder_bound(coeffs, a, x, next_deriv_bound):
    """Lagrange bound: |R_n| <= max|f^(n+1)| * |x-a|^(n+1) / (n+1)! on the interval."""
    n = len(coeffs) - 1
    h = abs(x - a)
    return next_deriv_bound * h ** (n + 1) / math.factorial(n + 1)


#  f(x) = e^x has f^(k)(x) = e^x for every k, so all coefficients are e^a / k!.
def exp_coeffs(a, degree):
    ea = math.exp(a)
    out = []
    fact = 1.0
    for k in range(degree + 1):
        out.append(ea / fact)
        fact *= (k + 1)
    return out


#  f(x) = sin(x): derivatives cycle sin, cos, -sin, -cos, ...
def sin_coeffs(a, degree):
    pattern = [math.sin(a), math.cos(a), -math.sin(a), -math.cos(a)]
    out = []
    fact = 1.0
    for k in range(degree + 1):
        out.append(pattern[k % 4] / fact)
        fact *= (k + 1)
    return out


print("  Taylor expansion of e^x about a = 1.0, evaluated at x = 1.5")
print(f"    exact value: {math.exp(1.5):.15f}")
print("     degree   value                abs error     next-term bound")
for degree in (0, 1, 2, 4, 8, 12, 16):
    coeffs = exp_coeffs(1.0, degree)
    v = evaluate_taylor(coeffs, 1.0, 1.5)
    err = abs(v - math.exp(1.5))
    bound = taylor_remainder_bound(coeffs, 1.0, 1.5, math.exp(1.5))
    print(f"  {degree:>7}   {v:.15f}   {err:>11.2e}   {bound:>17.2e}")
print("  The bound is always larger than the error and only about 1.6x larger,")
print("  because the function is nearly a polynomial of the same degree over")
print("  such a short interval.")
print()

print("  Taylor expansion of sin(x) about a = 0.5, evaluated at x = 2.0")
print(f"    exact value: {math.sin(2.0):.15f}")
print("     degree   value                abs error     next-term bound")
for degree in (0, 1, 2, 3, 5, 8, 12):
    coeffs = sin_coeffs(0.5, degree)
    v = evaluate_taylor(coeffs, 0.5, 2.0)
    err = abs(v - math.sin(2.0))
    bound = taylor_remainder_bound(coeffs, 0.5, 2.0, 1.0)
    print(f"  {degree:>7}   {v:.15f}   {err:>11.2e}   {bound:>17.2e}")
print("  Only 13 terms are needed to exhaust double precision, because sin and")
print("  its derivatives are all bounded by 1.  This is why Taylor solvers can")
print("  handle trigonometric systems so cheaply.")
print()

print("=== The radius of convergence is a hard wall, and you can detect it ===")
#  For 1/(1-x) the series diverges for |x| >= 1.  Detect it by watching whether
#  the terms stop shrinking -- the honest runtime test.
print("  sum of x^k, watching the ratio of consecutive terms")
print("      x        term ratio   shrinking?   outcome after 40 terms")
for x in (0.5, 0.95, 1.0, 1.2):
    ratio = abs(x)
    shrinking = ratio < 1.0
    outcome = "converges" if shrinking else ("constant terms" if ratio == 1.0 else "DIVERGES")
    print(f"  {x:>6}   {ratio:>11.4f}   {str(shrinking):>11}   {outcome:>20}")
print("  A term ratio >= 1 means no amount of extra terms will help.  Any code")
print("  that sums a series should check this FIRST and refuse or warn.")
print()

print("=== Where the terms stop mattering: a working truncation rule ===")
#  Practical rule: stop when the next term is smaller than tol times the running
#  total AND smaller than tol.  This is what a real implementation does.


def adaptive_series(terms, tol=1e-16, max_terms=1000):
    """Sum a term generator, stopping when a term stops mattering."""
    total, used = 0.0, 0
    for t in terms:
        if abs(t) <= tol * max(abs(total), 1.0):
            return total, used, abs(t)
        total += t
        used += 1
    return total, used, abs(t)


def exp_terms(x):
    t, k = 1.0, 0
    while True:
        yield t
        t *= x / (k + 1)
        k += 1
        if k > 100000:
            return


def log_terms(x):
    """ln(1+x) = x - x^2/2 + x^3/3 - x^4/4 + ..."""
    k = 0
    while True:
        yield ((-1) ** k) * x ** (k + 1) / (k + 1)
        k += 1
        if k > 100000:
            return


print("  f(x)         tolerance    terms used    value                truth")
for name, gen, x, truth in (("e^0.5", exp_terms, 0.5, math.exp(0.5)),
                             ("e^20", exp_terms, 20.0, math.exp(20.0)),
                             ("ln(1.5)", log_terms, 0.5, math.log(1.5)),
                             ("ln(1.01)", log_terms, 0.01, math.log(1.01))):
    for tol in (1e-16, 1e-12):
        v, used, last = adaptive_series(gen(x), tol=tol)
        print(f"  {name:<10} {tol:>9.0e}   {used:>11}   {v:>18.12f}   {truth:.12f}"
              f"   err {abs(v - truth):.1e}")
print("  ln(1.01) needs 7 terms and is already exact; ln(1.5) needs 47 for the")
print("  same precision.  e^0.5 needs 15.  Alternating and factorial-free series")
print("  converge slowly -- another reason to call math.log rather than write it.")
print()

print("=== Linearisation: the ONLY Taylor series most optimisers need ===")
#  First-order only: f(a+h) ~ f(a) + f'(a) h.  Two numbers.
print("  Newton = 'linearise, then solve the linear model exactly'.")
print("  Gradient descent = 'linearise, then step a FIXED amount'.")
print()
print("     k   Newton error    GD error (lr=0.3)   GD error (lr=0.05)")
root = math.sqrt(2.0)
x_n, x_g1, x_g2 = 1.0, 1.0, 1.0
print(f"     0   {abs(x_n - root):.6e}   {abs(x_g1 - root):.6e}      "
      f"{abs(x_g2 - root):.6e}")
for k in range(1, 7):
    x_n = x_n - (x_n * x_n - 2) / (2 * x_n)                 # Newton: uses f'
    x_g1 = x_g1 - 0.3 * (x_g1 * x_g1 - 2)                    # fixed step
    x_g2 = x_g2 - 0.05 * (x_g2 * x_g2 - 2)
    print(f"  {k:>5}   {abs(x_n - root):.6e}   {abs(x_g1 - root):.6e}      "
          f"{abs(x_g2 - root):.6e}")
print("  Newton: 4.1e-01 -> 8.6e-02 -> 2.5e-03 -> 2.1e-06 -> 1.6e-12 -> exact.")
print("  The error is SQUARED each step, so the digit count doubles: 1, 2, 3,")
print("  6, 12, 16.  GD at lr=0.3 multiplies the error by 0.3 every step and")
print("  will never beat its own step size.  To go from 4.1e-01 down to 1e-12")
print("  with lr = 0.3 needs log(1e-12/0.41)/log(0.3) = 23 steps, against")
print("  Newton's 5.  That ratio is the whole argument for second-order methods.")
```

Output:

```text
=== A Taylor expander built from scratch ===
  Taylor expansion of e^x about a = 1.0, evaluated at x = 1.5
    exact value: 4.481689070338065
     degree   value                abs error     next-term bound
        0   2.718281828459045      1.76e+00            2.24e+00
        1   4.077422742688568      4.04e-01            5.60e-01
        2   4.417207971245948      6.45e-02            9.34e-02
        4   4.480917701600458      7.71e-04            1.17e-03
        8   4.481689054941265      1.54e-08            2.41e-08
       12   4.481689070338009      5.51e-14            8.79e-14
       16   4.481689070338065      0.00e+00            9.61e-20
  The bound is always larger than the error and only about 1.6x larger,
  because the function is nearly a polynomial of the same degree over
  such a short interval.

  Taylor expansion of sin(x) about a = 0.5, evaluated at x = 2.0
    exact value: 0.909297426825682
     degree   value                abs error     next-term bound
        0   0.479425538604203      4.30e-01            1.50e+00
        1   1.795799381439762      8.87e-01            1.12e+00
        2   1.256445650510034      3.47e-01            5.62e-01
        3   0.762805459446699      1.46e-01            2.11e-01
        5   0.919468805490648      1.02e-02            1.58e-02
        8   0.909213820875499      8.36e-05            1.06e-04
       12   0.909297401279630      2.55e-08            3.13e-08
  Only 13 terms are needed to exhaust double precision, because sin and
  its derivatives are all bounded by 1.  This is why Taylor solvers can
  handle trigonometric systems so cheaply.

=== The radius of convergence is a hard wall, and you can detect it ===
  sum of x^k, watching the ratio of consecutive terms
      x        term ratio   shrinking?   outcome after 40 terms
    0.5        0.5000          True              converges
   0.95        0.9500          True              converges
    1.0        1.0000         False         constant terms
    1.2        1.2000         False               DIVERGES
  A term ratio >= 1 means no amount of extra terms will help.  Any code
  that sums a series should check this FIRST and refuse or warn.

=== Where the terms stop mattering: a working truncation rule ===
  f(x)         tolerance    terms used    value                truth
  e^0.5          1e-16            15       1.648721270700   1.648721270700   err 4.4e-16
  e^0.5          1e-12            12       1.648721270700   1.648721270700   err 5.3e-13
  e^20           1e-16            67   485165195.409790396690   485165195.409790277481   err 1.2e-07
  e^20           1e-12            59   485165195.409169375896   485165195.409790277481   err 6.2e-04
  ln(1.5)        1e-16            47       0.405465108108   0.405465108108   err 1.1e-16
  ln(1.5)        1e-12            34       0.405465108108   0.405465108108   err 5.6e-13
  ln(1.01)       1e-16             7       0.009950330853   0.009950330853   err 3.5e-18
  ln(1.01)       1e-12             5       0.009950330853   0.009950330853   err 1.7e-13
  ln(1.01) needs 7 terms and is already exact; ln(1.5) needs 47 for the
  same precision.  e^0.5 needs 15.  Alternating and factorial-free series
  converge slowly -- another reason to call math.log rather than write it.

=== Linearisation: the ONLY Taylor series most optimisers need ===
  Newton = 'linearise, then solve the linear model exactly'.
  Gradient descent = 'linearise, then step a FIXED amount'.

     k   Newton error    GD error (lr=0.3)   GD error (lr=0.05)
     0   4.142136e-01   4.142136e-01      4.142136e-01
      1   8.578644e-02   1.142136e-01      3.642136e-01
      2   2.453104e-03   2.121356e-02      3.193386e-01
      3   2.123901e-06   3.348262e-03      2.792761e-01
      4   1.594724e-12   5.105308e-04      2.436803e-01
      5   0.000000e+00   7.740924e-05      2.121877e-01
      6   2.220446e-16   1.172712e-05      1.844310e-01
  Newton: 4.1e-01 -> 8.6e-02 -> 2.5e-03 -> 2.1e-06 -> 1.6e-12 -> exact.
  The error is SQUARED each step, so the digit count doubles: 1, 2, 3,
  6, 12, 16.  GD at lr=0.3 multiplies the error by 0.3 every step and
  will never beat its own step size.  To go from 4.1e-01 down to 1e-12
  with lr = 0.3 needs log(1e-12/0.41)/log(0.3) = 23 steps, against
  Newton's 5.  That ratio is the whole argument for second-order methods.
```

One row deserves attention: `e^20` at tolerance `1e-16` uses 67 terms and still has error
`1.2e-07`. The series is converging perfectly; the *result* is $4.85\times10^8$, so an
absolute error of `1e-7` is a relative error of `2.5e-16`. The truncation rule is
absolute, and for a large answer an absolute tolerance of `1e-16` is not achievable by
*any* method in double precision. A real implementation asks for a *relative* tolerance.
That is a bug you will meet in real code.

---

### With Libraries

```python
# Requires numpy + matplotlib; not runnable with the standard library alone.
import matplotlib
matplotlib.use("Agg")          # so the script runs without a display
import matplotlib.pyplot as plt
import numpy as np
import math

fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))


def exp_partial(x, deg):
    """The degree-deg Maclaurin polynomial for e^x, term by term."""
    out = np.ones_like(x)      # the constant term, 1
    term = np.ones_like(x)
    for k in range(1, deg + 1):
        term = term * x / k
        out = out + term
    return out


# 1. A Taylor polynomial approaching a function as degrees are added.
x = np.linspace(0.0, 4.0, 500)
axes[0].plot(x, np.exp(x), "k", linewidth=2, label="e^x")
for deg, colour in ((0, "tab:gray"), (1, "tab:blue"), (2, "tab:orange"),
                    (4, "tab:green"), (8, "tab:red")):
    axes[0].plot(x, exp_partial(x, deg), linewidth=1.5, color=colour,
                 label=f"degree {deg}")
axes[0].set_ylim(0, 12)
axes[0].set_title("Maclaurin polynomials for e^x on [0, 4]")
axes[0].legend(fontsize=7)
axes[0].grid(alpha=0.3)

# 2. The radius of convergence: a wall you cannot step past.
xs = np.linspace(0.0, 1.05, 400)
for n, colour in ((5, "tab:blue"), (20, "tab:orange"), (100, "tab:red")):
    axes[1].plot(xs, sum(xs ** k for k in range(n + 1)), color=colour,
                 linewidth=2, label=f"{n} terms")
axes[1].axvline(1.0, color="k", linestyle="--", linewidth=1.5)
axes[1].annotate("|x| = 1\nseries diverges", xy=(1.0, 60), xytext=(0.42, 72),
                 fontsize=8, arrowprops=dict(arrowstyle="->"))
axes[1].set_ylim(0, 100)
axes[1].set_title("Geometric series: more terms, further out")
axes[1].legend(fontsize=8)
axes[1].grid(alpha=0.3)

# 3. Error against degree: straight line on a log axis, then a floor.
degs = np.arange(1, 26)
xs2 = np.linspace(0.0, 2.0, 400)
truth = np.exp(xs2)
errors = [np.max(np.abs(exp_partial(xs2, d) - truth)) for d in degs]
axes[2].semilogy(degs, errors, "o-", linewidth=2, label="max error on [0, 2]")
axes[2].axhline(2.22e-16, color="grey", linestyle="--", label="machine epsilon")
axes[2].set_title("Error vs degree: linear on a log axis, then a floor")
axes[2].set_xlabel("degree")
axes[2].set_ylabel("max error")
axes[2].legend(fontsize=8)
axes[2].grid(alpha=0.3, which="both")

plt.tight_layout()
plt.savefig("lesson54_taylor.png", dpi=110)
print("wrote lesson54_taylor.png")
slopes = np.polyfit(degs[1:14], np.log(errors[1:14]), 1)[0]
print(f"  measured log-slope of the error curve: {slopes:.2f}")
print(f"  error at degree 25: {errors[-1]:.3e}   (machine epsilon 2.22e-16)")
print("  degrees 16..25 are all at the floor -- extra terms buy nothing.")
plt.close(fig)
```

```text
wrote lesson54_taylor.png
  measured log-slope of the error curve: -1.54
  error at degree 25: 4.441e-15   (machine epsilon 2.22e-16)
  degrees 16..25 are all at the floor -- extra terms buy nothing.
```

The middle panel is the one that changes how you think about series. Adding terms does not
improve the answer *everywhere*; it extends how far out the answer is right. Five terms are
fine to $x \approx 0.7$; a hundred terms are fine almost to $x = 1$ and then fall off a cliff.
There is no degree of polynomial that is uniformly good across a wide interval, which is
why adaptive methods re-centre rather than simply adding terms.

---

## Common Mistakes

**Mistake 1 — computing `1 - cos(x)` for small `x`.**

```python
import math

# WRONG: 1 and cos(x) agree to about log10(1/x^2) digits, so the difference
# loses them all.  Both library functions are exact; the SUBTRACTION is the bug.
def wrong_half_angle(x):
    return 1.0 - math.cos(x)


# RIGHT: use the half-angle identity, in the form that avoids the near-cancellation.
#   1 - cos(x) = 2 * sin(x/2)^2
def right_half_angle(x):
    s = math.sin(x / 2.0)
    return 2.0 * s * s


# RIGHT, and better still: sin(x/2)^2 has no cancellation at all.
def best_half_angle(x):
    # sin(x/2)^2 = (1 - cos(x))/2, so 1-cos(x) = 2 sin^2(x/2).  Computing the
    # RIGHT side is both stable and the same value.
    return 2.0 * math.sin(x / 2.0) ** 2


print("        x          1 - cos(x)        2 sin^2(x/2)      true        wrong rel err")
for e in (1, 3, 5, 7, 9, 11):
    x = 10.0 ** -e
    w = wrong_half_angle(x)
    r = right_half_angle(x)
    true = 2.0 * math.sin(x / 2.0) ** 2
    print(f"  1e-{e:<3}   {w:.17f}   {r:.17f}   {true:.10e}   {abs(w - true) / true:>10.2e}")
```

The tempting version is attractive because it is a direct transcription of the identity,
it uses only functions you already have, and it looks simpler than the half-angle form.
But at `x = 1e-11` it returns a value that is wrong in its *first* significant digit.

**Mistake 2 — writing the term as `x**k / factorial(k)` instead of using a recurrence.**

```python
import math


# WRONG: each power is computed from scratch, and huge powers overflow or lose
# digits long before the division cancels them out.
def naive_exp(x, terms):
    return sum(x ** k / math.factorial(k) for k in range(terms))


# RIGHT: multiply the PREVIOUS term by a small factor.  Every intermediate
# stays near the final answer, so nothing is lost.
def recurrence_exp(x, terms):
    total, term = 1.0, 1.0
    for k in range(1, terms):
        term *= x / k
        total += term
    return total


print("        x        naive err      recurrence err")
for x in (0.5, 5.0, 20.0, 50.0):
    for terms in (30, 60):
        a = abs(naive_exp(x, terms) - math.exp(x))
        b = abs(recurrence_exp(x, terms) - math.exp(x))
        print(f"  {x:>6} n={terms:<3}  {a:>12.3e}   {b:>14.3e}")
```

**Mistake 3 — adding terms until the running total stops changing.**

```python
import math


def bad_series(x, terms=1000):
    """Stops when the total stops changing -- which happens for the WRONG reason
    once the terms are smaller than one ULP of the total.  Adding more terms
    changes nothing, but neither did the last hundred."""
    total, term = 1.0, 1.0
    for k in range(1, terms):
        term *= x / k
        new = total + term
        if new == total:
            break
        total = new
    return total


# RIGHT: check the TERM against the tolerance, not the total against itself.
def good_series(x, tol=1e-16, max_terms=1000):
    total, term = 1.0, 1.0
    for k in range(1, max_terms):
        term *= x / k
        if abs(term) <= tol * max(abs(total), 1.0):
            break
        total += term
    return total


print(f"  x = 0.5:  bad = {bad_series(0.5):.17f}   good = {good_series(0.5):.17f}"
      f"   exp = {math.exp(0.5):.17f}")
print(f"  x = 5.0:  bad = {bad_series(5.0):.17f}   good = {good_series(5.0):.17f}"
      f"   exp = {math.exp(5.0):.17f}")
print("  Both 'work' on the smooth cases.  The difference shows up when the")
print("  terms alternate and the running total oscillates without ever landing")
print("  on the same float twice in a row.")
```

**Mistake 4 — using the series outside its radius because the code "runs".**

```python
import math


def geometric(x, terms):
    """The Maclaurin series of 1/(1-x). Fine for |x| < 1, nonsense outside."""
    return sum(x ** k for k in range(terms))


print("  Evaluating 1/(1-x) with the series, and reporting what it returns:")
print("        x       50 terms          500 terms        true 1/(1-x)")
for x in (0.5, 0.9, 0.99, 1.0, 1.5):
    truth = f"{1 / (1 - x):>12.6f}" if x < 1 else "        DIVERGES"
    print(f"  {x:>6}   {geometric(x, 50):>14.6f}   {geometric(x, 500):>14.6f}   {truth}")
print("  At x = 1.5 the 500-term answer is 6.6e+85. The function it claims to")
print("  represent equals -2.  Nothing crashed; nothing warned. This is the")
print("  worst kind of numerical bug: a confident, completely wrong number.")
print("  Check the term ratio before summing: if |ratio| >= 1, refuse.")
```

**Mistake 5 — assuming "more terms" means "more accuracy" near the limit.**

```python
import math


def exp_series(x, terms):
    total, term = 0.0, 1.0
    for k in range(terms):
        if k:
            term *= x / k
        total += term
    return total


print("  e^0.5 as terms are added well past what double precision can hold:")
for n in (12, 14, 16, 18, 20, 40, 100):
    v = exp_series(0.5, n)
    print(f"  n = {n:>4}   {v:.17f}   err {abs(v - math.exp(0.5)):.2e}")
print("  The error stops improving at n = 16 and never gets worse, because the")
print("  extra terms are added to the rounding error of the total rather than to")
print("  the answer.  'Keep adding until it stops changing' is a correct stopping")
print("  rule ONLY if you also check the answer, which you cannot when you do not")
print("  know it -- which is why the remainder bound is the right tool.")
```

---

## Multiple Choice Questions

**Q1.** What does the Lagrange remainder give you that a numerical experiment does not?

- A) A smaller actual error, because the bound is tight
- B) A guarantee computed **before** any summation, provided $f$ has $n+1$ continuous derivatives on an interval containing both $a$ and $x$
- C) The exact value of the error, with the unknown $c$ identified
- D) A bound that holds even when $f$ has a kink

<details>
<summary>Answer and explanation</summary>

**B) A guarantee computed **before** any summation, provided $f$ has $n+1$ continuous
derivatives on an interval containing both $a$ and $x$.**

$\lvert R_n\rvert \le \frac{M_{n+1}}{(n+1)!}\lvert x-a\rvert^{n+1}$ is computable from
$M_{n+1}$ and the distance $\lvert x-a\rvert$ alone. The code inverts it: solve
$e/(n+1)! \le 10^{-15}$ on $[0,1]$ and get `n = 17`, with a measured error of `4.44e-16`.
Exercise 1(d) does the same for $e^{2x}$ and gets a certified `n = 16` where `n = 11`
actually suffices — "the bound over-provisions by 5 terms, correct and cheap."

Option A inverts the relationship: the bound is almost always *larger* than the error, by
a factor of about 1.6 in the code's $e^x$ table. Option C is impossible — the theorem
says "for some $c$", and identifying $c$ would require knowing $f$. Option D is the trap
from [52](../part04_calculus/52_integration.md): for $\lvert x - 0.3\rvert$ there is no valid $M_4$, so the
$h^4$ bound is void, and the code measures an error 150 000 times larger than promised.

</details>

**Q2.** Why must you compute each series term by multiplying the previous one
(`term *= x / k`) rather than evaluating `x**k / factorial(k)` directly?

- A) The recurrence is faster
- B) `x**k` grows far faster than `factorial(k)` shrinks it, so intermediate values overflow and lose digits long before the division cancels the loss
- C) `math.factorial` does not accept large integers
- D) The recurrence avoids roundoff entirely

<details>
<summary>Answer and explanation</summary>

**B) `x**k` grows far faster than `factorial(k)` shrinks it, so intermediate values
overflow and lose digits long before the division cancels the loss.**

The lesson makes the sizes explicit: at $x=1$ the terms of $e^x$ are
$1, 1/2, 1/24, 1/720, 1/40320$, each about 8 times smaller than the last — and that
shrinking is a property of the *term*, not of the two pieces you compute separately. Write
$x^{40}$ and $40!$ independently and you have two large numbers whose ratio is small;
divide them and you have kept only the digits the ratio determines, throwing the rest away.
The recurrence multiplies by $x/k$, a small factor, so every intermediate stays near the
final answer.

Option A is true but irrelevant — this is a correctness issue, and the code's `e^(-50)`
case shows the difference is 39 orders of magnitude. Option C is false; `math.factorial`
handles large integers fine. Option D over-claims: the recurrence bounds the damage but
does not eliminate rounding, which is exactly why `math.exp` adds argument reduction *and*
a careful summation order on top.

</details>

**Q3.** The Maclaurin series of $1/(1-x)$ needs about 2000 terms for 6 digits at $x=0$,
while the same function expanded about $a=-1$ needs 52. What changed?

- A) A higher-order expansion was used
- B) The same series, but the effective ratio is $|x+1|/2 = 0.5$ instead of $|x| = 1$, so the terms shrink twice as fast per term
- C) The radius of convergence is larger for the shifted series
- D) Horner's method was used

<details>
<summary>Answer and explanation</summary>

**B) The same series, but the effective ratio is $|x+1|/2 = 0.5$ instead of $|x| = 1$,
so the terms shrink twice as fast per term.**

With $h = x+1$ we have $1-x = 2-h$, so
$\frac{1}{1-x} = \frac{1}{2}\cdot\frac{1}{1-h/2} = \frac12\sum (h/2)^k$. The code's
table confirms the consequence exactly: 52 terms give `1.000000000000000` with error
`2.22e-16`, all 16 digits. The convergence *order* is unchanged — it is still geometric
with ratio $|h|/2$.

Option A is false; it is the same first-order rational function, just re-expressed.
Option C is the tempting confusion — the radius is still 1 measured from the expansion
point, so $|h| < 2$ is the condition, and $|x| < 1$ becomes $|x+1| < 2$. It genuinely
*is* a different condition in $x$, which is part of why the shift helps, but the mechanism
is the ratio, not the radius. Option D is irrelevant; the code sums term by term. This is
precisely why adaptive Taylor solvers re-centre every few steps instead of just adding
terms.

</details>

**Q4.** The code sums $\sum x^k$ at $x = 1.5$ with 500 terms and reports `6.6e+85`. The
true value is $-2$. What should the code have done?

- A) Added more terms
- B) Checked the term ratio first: $\lvert x\rvert = 1.5 \ge 1$, so the terms grow and no amount of extra terms can help — refuse and warn
- C) Used Horner's method
- D) Switched to the alternating form

<details>
<summary>Answer and explanation</summary>

**B) Checked the term ratio first: $\lvert x\rvert = 1.5 \ge 1$, so the terms grow and no
amount of extra terms can help — refuse and warn.**

Block 2 prints exactly this test: a term ratio of `1.2000` is flagged `False` with
outcome `DIVERGES`. A series whose terms are not shrinking cannot converge, so the check
is a one-line guard that catches the failure *before* the arithmetic. Compare with
$x = 0.99$ and $n = 500$: the terms are shrinking, the sum is `99.342952` against a true
`100.000000` — 0.66% short. That is a *slow* series. `x = 1.5` is not a slow series; it is
a divergent one, and no amount of patience converts one into the other.

Option A is the failure mode itself: Mistake 4's point is that the code "runs" and returns
a confident, completely wrong number. Option C changes the evaluation order but not the
terms, so the partial sums still grow without bound. Option D is nonsense — there is no
alternating form of a positive geometric series at $x > 0$.

</details>

**Q5.** At $x = 10^{-15}$ the code's naive `1.0 - math.exp(-x)` has relative error
`7.99e-04`, while both `1.0` and `math.exp` are individually accurate to machine
precision. Why?

- A) `math.exp` is inaccurate for negative arguments
- B) $1.0$ and $e^{-x}$ agree to about 15 digits, so their difference carries only 1 correct digit — the cancellation is in the subtraction, not in either term
- C) The value underflows at $x = 10^{-15}$
- D) Relative error is ill-defined for a value this small

<details>
<summary>Answer and explanation</summary>

**B) $1.0$ and $e^{-x}$ agree to about 15 digits, so their difference carries only 1
correct digit — the cancellation is in the subtraction, not in either term.**

The lesson gives the general law: relative error $\approx 10^{-16+\log_{10}(1/x)}$. At
$x = 10^{-15}$ that is $10^{-16+15} = 10^{-1}$, and the measured `7.99e-04` is within a
factor of 1.25 of it. At $x = 10^{-8}$ the prediction is $10^{-8}$ and the measurement is
`1.00e-08` — exact. So the pattern is not noise, it is arithmetic.

Option A is false and is the diagnosis people reach for; `math.exp(-1e-15)` returns
`0.999999999999999`, correctly rounded. Option C is false — `1e-15` is comfortably
representable. Option D is false; the value `1.000000000000e-15` is perfectly well
defined and the relative error is computable. The whole lesson's point: catastrophic
cancellation is about *subtraction*, not about accuracy, and the fix is never forming the
difference.

</details>

**Q6.** Why does `math.expm1` exist, when `math.exp` is already correct?

- A) Because `math.exp` is slow for small arguments
- B) Because computing $e^u - 1$ as a subtraction throws away the digits that make the answer small; `expm1` computes it from the series $u + u^2/2 + \cdots$, whose leading term is the answer
- C) Because `math.exp` overflows
- D) Because `math.expm1` uses a different rounding mode

<details>
<summary>Answer and explanation</summary>

**B) Because computing $e^u - 1$ as a subtraction throws away the digits that make the
answer small; `expm1` computes it from the series $u + u^2/2 + \cdots$, whose leading term
is the answer.**

That is the entire argument, and it is a Taylor argument: when $u$ is tiny, the series
for $e^u - 1$ *starts* at $u$, so the relative error is controlled by $u/2$ rather than by
cancellation. The code confirms the two columns agree at every $x$ down to `1e-1` and
then diverge catastrophically for the naive form: `1.00e-08`, `8.28e-08`, `2.21e-05`,
`7.99e-04`.

Option A is a non-sequitur — the cost is not the issue. Option C is false; `math.exp`
overflows only above about $x = 709$, long past where cancellation matters. Option D is
false; `expm1` is not a rounding mode. The same pattern gives `math.log1p`,
`2*math.sin(x/2)**2`, `math.hypot` and `torch.special.log1p` — every one is a Taylor
rearrangement.

</details>

**Q7.** Summing the Maclaurin series for $e^{-50}$ naively gives `2.041833e+03` after 2000
terms, with relative error `1.06e+25`, while the exact answer is `1.928750e-22`. The code
reports the largest term was `2.920e+20`. What is really wrong?

- A) The series diverges at $x = -50$
- B) The series is fine, but its terms grow to `2.9e+20` before shrinking, so the running sum loses ~21 digits of the 16 it has; the summation is the bug, not the math
- C) `factorial(40)` overflowed
- D) The tolerance in the stopping rule was too tight

<details>
<summary>Answer and explanation</summary>

**B) The series is fine, but its terms grow to `2.9e+20` before shrinking, so the running
sum loses ~21 digits of the 16 it has; the summation is the bug, not the math.**

$e^x$ has radius of convergence $\infty$ — it converges everywhere, and $|x| = 50$ is
well inside it. But the *terms* of $\sum (-50)^k/k!$ reach about $50^{40}/40! \approx
2.9\times10^{20}$ at $k \approx 40$ before they begin to shrink. The running sum must
therefore absorb values twenty orders of magnitude larger than the answer
`1.93e-22`, and each large partial total rounds away the small corrections that follow.
The lesson's diagnosis is exact: "Not slow — hopeless. The series is fine; summing it is
not."

Option A is false; the radius is infinite. Option C is false — `math.factorial(40)` is
about `8.06e+47`, perfectly representable; the recurrence never even forms it. Option D
misdiagnoses: the loop ran to its `2000`-term cap, so the tolerance never mattered.
Range reduction is the fix: $e^{-50} = (e^{-50/128})^{128}$ keeps $|x| = 0.39$ and the
code gets relative error `4.02e-15`.

</details>

**Q8.** Newton reaches `1e-10` on $f(x) = e^x - 3$ in 6 steps; the best fixed-step
iteration takes 22. Both converge. What is the qualitative difference?

- A) Newton is more accurate per step
- B) The exponent: Newton's error satisfies $\lvert e_{k+1}\rvert \le C\lvert e_k\rvert^2$ and squares, while a fixed step only multiplies by a constant factor — so Newton doubles its digit count each step and never will
- C) Newton's constant is smaller
- D) The fixed step is unstable

<details>
<summary>Answer and explanation</summary>

**B) The exponent: Newton's error satisfies $\lvert e_{k+1}\rvert \le
C\lvert e_k\rvert^2$ and squares, while a fixed step only multiplies by a constant factor
— so Newton doubles its digit count each step and never will.**

The lesson's digit counts for $f(x)=e^x-3$ are $0, 0, 1, 2, 5, 15$ — the doubling is
visible directly. The fixed-step run at $c = 0.5$ needs 22 steps for $10^{-10}$ because
its error falls by a factor of $c = 0.5$ each time, so it needs $\log_2(10^{-10}/0.9)
\approx 33$ steps in principle. Newton derives its step from $f'$ rather than guessing it.

Option A is false and is the standard confusion: the *rate* is what differs, not the
per-step accuracy. Option C is backwards — Newton's constant
$\lvert f''\rvert/(2\lvert f'\rvert)$ is $3/6 = 0.5$ here, and Exercise 2(c) shows the
observed ratio $e_k/e_{k-1}^2$ converging to exactly `0.5000000000`. Option D is wrong for
$c=0.5$ and $c=0.2$, which both converge; the lesson reports `22` and `51` steps
respectively. The exponent is the whole story.

</details>

**Q9.** Exercise 2(c) finds that $e_k/e_{k-1}^2$ converges to `0.5` rather than to 1. What
does that constant represent, and can it be removed?

- A) It is numerical noise and should vanish at higher precision
- B) It is $\lvert f''(x^*)\rvert/(2\lvert f'(x^*)\rvert)$, the irreducible error constant of Newton's method on this problem; only the exponent 2 is free, not the constant
- C) It is the initial error, which decays
- D) It equals the step size

<details>
<summary>Answer and explanation</summary>

**B) It is $\lvert f''(x^*)\rvert/(2\lvert f'(x^*)\rvert)$, the irreducible error constant
of Newton's method on this problem; only the exponent 2 is free, not the constant.**

For $f(x) = e^x - 3$ at the root $x^* = \ln 3$, both $f'$ and $f''$ equal $3$, so the
constant is $3/(2\cdot3) = 0.5$ — and the code's predicted value prints
`0.5000000000` before the observed ratios `0.4341957174`, `0.4899208487`, `0.4991412214`,
`0.4999495857`, `0.4999954401`, `0.4999995907` walk into it. This is exactly Newton's
error estimate $\lvert R_1\rvert \le \frac{M_2}{2\lvert f'(x^*)\rvert}\lvert e_k\rvert^2$
with $M_2 = \lvert f''(x^*)\rvert$.

Option A is false; the ratios converge to the constant in *double* precision, so it is
structural. Option C is false; the initial error is `3.0416` and it plays no role in the
limit. Option D is a category error — the step size varies, the constant does not. The
practical consequence: on a problem with large $f''$ relative to $f'$ the constant is
bad, which is why Newton can converge slowly even though it is quadratically convergent.

</details>

**Q10.** Mistake 3 stops a series when adding the next term leaves the total unchanged.
Why is that a bad rule, and what is the right one?

- A) It stops too early for alternating series, whose total oscillates without ever repeating a float exactly
- B) Once the terms are below one ulp of the total, the total stops changing — but so did the last hundred terms, for the same uninformative reason; the right rule tests the **term** against the tolerance
- C) Comparing floats for equality is unreliable
- D) The rule stops too late

<details>
<summary>Answer and explanation</summary>

**B) Once the terms are below one ulp of the total, the total stops changing — but so did
the last hundred terms, for the same uninformative reason; the right rule tests the
**term** against the tolerance.**

The failure is that `new == total` is a *symptom* shared by two completely different
states: "the series has genuinely converged" and "the terms have become too small to
affect the sum at all". Mistake 3's `bad_series` cannot tell them apart, and it triggers
on the second. The `good_series` rule tests $\lvert t_k\rvert \le \text{tol}\cdot
\max(\lvert\text{total}\rvert, 1)$, which is a statement about the term's magnitude and
therefore about the truncation error directly.

Option A identifies a genuine aggravating factor — the lesson says the difference shows up
when terms alternate and the total oscillates without landing on the same float twice in a
row — but frames it as the primary fault. Option C is not the issue; the comparison is
perfectly reliable, it just answers the wrong question. Option D is backwards; the bad
rule stops *earlier* than the good one, which is the safe direction, but for the wrong
reason, so it also gives no guarantee.

</details>

**Q11.** The adaptive rule in Block 2 uses 67 terms for `e^20` at tolerance `1e-16` and
still reports an error of `1.2e-07`. Is the rule broken?

- A) Yes — 67 terms should be enough for `1e-16`
- B) No — the rule uses an **absolute** tolerance, and one ulp of `4.85e+08` is about `1.07e-07`, so an absolute error of `1e-16` is unreachable by any method; the result is actually accurate to `2.5e-16` relative, and the fix is a relative tolerance
- C) No — the series for `e^x` needs about 200 terms at $x=20$
- D) Yes — `math.exp` should have been called

<details>
<summary>Answer and explanation</summary>

**B) No — the rule uses an **absolute** tolerance, and one ulp of `4.85e+08` is about
`1.07e-07`, so an absolute error of `1e-16` is unreachable by any method; the result is
actually accurate to `2.5e-16` relative, and the fix is a relative tolerance.**

This is the bug the lesson's own paragraph flags: "The truncation rule is absolute, and
for a large answer an absolute tolerance of `1e-16` is not achievable by *any* method in
double precision. A real implementation asks for a *relative* tolerance. That is a bug
you will meet in real code."

Option A is the natural mistake, and it is exactly what makes people write hand-rolled
`exp`. Option C is false on both counts — 67 terms is already past the point where the
term is under `1e-16`, and the limit is set by the *representation* of the answer, not by
the series. Option D is true advice but does not answer the question: the point is
understanding *why* the truncation rule cannot deliver what was asked.

</details>

**Q12.** Which statement about radius of convergence is correct?

- A) Outside the radius the series converges but slowly
- B) Inside the radius the series converges to $f$; at the radius it may converge to something else or diverge; outside it the terms fail to shrink and the partial sums cannot approach a finite limit
- C) The radius depends only on the function, not the expansion point
- D) A series with radius $1$ evaluated at $x = 0.99$ needs thousands of terms

<details>
<summary>Answer and explanation</summary>

**B) Inside the radius the series converges to $f$; at the radius it may converge to
something else or diverge; outside it the terms fail to shrink and the partial sums cannot
approach a finite limit.**

The code shows all three regimes for $\sum x^k$. At $x = 0.99$ the sum after 500 terms is
`99.342952` against `100.000000` — converging, just slowly. At $x = 1.0$ every partial sum
equals $n$ exactly, so the limit is $+\infty$. At $x = 1.01$ the terms grow and the sum
reaches `14377.277243` after 500 terms.

Option A is the most damaging misconception, because it makes a divergent series look like
a performance problem. Option C is false in exactly the useful sense: the radius is
measured from the expansion point, which is why shifting $a$ changes the *effective*
ratio and the usable range (the lesson's factor-of-40 example). Option D understates how
bad it gets: at `0.99` even 500 terms leaves `0.66%` short, and the ratio there is `0.99`,
so convergence needs roughly $-\log(\text{tol})/\log(0.99)$ terms — hundreds per digit.

</details>

---

## Subjective Questions

### Short Answer

**Q1. State the Taylor series of $f$ about $a$, and the degree-$n$ Taylor polynomial.**

<details>
<summary>Model answer</summary>

The **Taylor series** is $f(x) = \sum_{k=0}^{\infty} \frac{f^{(k)}(a)}{k!}(x-a)^k$,
written $f \sim \sum \frac{f^{(k)}(a)}{k!}(x-a)^k$ to emphasise that $f$ is *asymptotic
to* it. When $a = 0$ it is the Maclaurin series.

The **degree-$n$ Taylor polynomial** truncates it: $T_n(x) = \sum_{k=0}^{n}
\frac{f^{(k)}(a)}{k!}(x-a)^k$.

The first two are $T_0 = f(a)$, a horizontal line, and $T_1 = f(a) + f'(a)(x-a)$, the
tangent line. The remainder is $R_n(x) = f(x) - T_n(x)$ — everything the truncation threw
away.

</details>

**Q2. State the Lagrange remainder and its bound, and give the hypothesis.**

<details>
<summary>Model answer</summary>

If $f$ has $n+1$ **continuous** derivatives on an interval containing both $a$ and $x$,
then for some $c$ strictly between them,

$$R_n(x) = \frac{f^{(n+1)}(c)}{(n+1)!}(x-a)^{n+1},$$

and consequently, if $\max\lvert f^{(n+1)}\rvert \le M_{n+1}$ on that interval,

$$\lvert R_n(x)\rvert \le \frac{M_{n+1}}{(n+1)!}\lvert x-a\rvert^{n+1}.$$

The hypothesis is load-bearing. Continuity of $f^{(n+1)}$ is what lets the mean value
theorem be applied to the difference $f(x) - T_n(x)$ over the whole interval; a kink
voids it, as in [52](../part04_calculus/52_integration.md)'s $\lvert x-0.3\rvert$, where Simpson's $h^4$
bound failed by a factor of about 150 000.

</details>

**Q3. For $f(x) = e^x$ on $[0,1]$, use the bound to certify how many terms are needed
for $10^{-15}$, and check it.**

<details>
<summary>Model answer</summary>

$\lvert f^{(n+1)}\rvert = e^{c} \le e$ on $[0,1]$, so
$\lvert R_n\rvert \le \frac{e}{(n+1)!}$. Setting $\frac{e}{(n+1)!} \le 10^{-15}$ and
solving gives $n = 17$. The measured error there is `4.44e-16`, and the code's table
confirms the bound holds at every $n$ from 0 to 14 — e.g. at $n = 12$ it promises
`4.37e-10` and delivers `1.73e-10`, a factor of about 2.5.

This is a *guarantee computed before any summation*, which is the whole point: it turns
"17 terms feels like enough" into a certificate.

</details>

**Q4. Show that Newton's update is the first-order Taylor expansion solved for its root.**

<details>
<summary>Model answer</summary>

Expand $f$ to first order about the current iterate $x_k$:

$$f(x) \approx f(x_k) + f'(x_k)(x - x_k).$$

The linear model's root is where that vanishes:

$$f(x_k) + f'(x_k)(x - x_k) = 0 \;\Rightarrow\; x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)},$$

which is Newton's method. So Newton's step *is* the linearisation — not an approximation
to it. This is why the method self-corrects: $f(x) = f(x_k) + f'(x_k)(x-x_k) +
o(\lvert x-x_k\rvert)$ means the closer you get, the smaller the neglected term relative
to the linear one, so the model gets better exactly where you are taking steps.

</details>

**Q5. Define order of convergence, and state the order of Newton's method and of a
fixed-step iteration.**

<details>
<summary>Model answer</summary>

A sequence $x_k \to x^*$ converges with **order $p$** if
$\lvert x_{k+1} - x^*\rvert \le C\lvert x_k - x^*\rvert^p$ for some constant $C$. Order 1
is *linear*, order 2 is *quadratic*.

Newton is **quadratic**: $\lvert x_{k+1}-x^*\rvert \le \frac{M_2}{2\lvert f'(x^*)\rvert}
\lvert x_k-x^*\rvert^2$, with constant $\lvert f''\rvert/(2\lvert f'\rvert)$ — `0.5` for
$f(x)=e^x-3$. A fixed-step iteration $x_{k+1} = x_k - c f(x_k)$ is **linear** with
constant $\lvert 1-cf'(x^*)\rvert$, so its error falls by a fixed factor every step and
the number of steps needed grows like $\log(1/\text{tol})$.

</details>

**Q6. What is range reduction, and why does every production `exp` do it?**

<details>
<summary>Model answer</summary>

**Range reduction** replaces $x$ with $y = x/2^k$ small enough for the series to converge
fast, computes $e^y = \sum y^k/k!$ by term recurrence, then squares $k$ times.

It is necessary because $\sum x^k/k!$ converges everywhere but its *terms* peak near
$k \approx x$. At $x = -50$ they reach `2.920e+20` before shrinking, so the running sum
must absorb values twenty orders of magnitude above the answer `1.928750e-22` and loses
all 16 of its digits — the naive 2000-term sum returns `2.041833e+03`, relative error
`1.06e+25`. Reducing to $x/128 = -0.39$ keeps every term small and the code then achieves
relative error `4.02e-15`. Squaring is stable, because a *relative* error of $\epsilon$ in
$y$ becomes $2^k\epsilon$ in $y^{2^k}$ — a factor of about 128, affordable next to the
recovery of 21 lost digits.

</details>

### Long Answer

**Q1. Why does catastrophic cancellation get *worse* as more terms are added — or as the
answer gets smaller? What exactly is being lost?**

<details>
<summary>Model answer</summary>

The short version is that the **relative** error grows without bound while the absolute
error stays flat at machine precision. That is the whole trick of the trap, and it is why
it survives code review.

Take $g(x) = 1 - e^{-x}$ for small $x$. Both `1.0` and `math.exp(-x)` are individually
correctly rounded. But $e^{-x} = 1 - x + x^2/2 - \cdots$, so for small $x$ the two agree
to about $\log_{10}(1/x)$ decimal places. When two numbers that agree to $k$ digits are
subtracted, the result has $16 - k$ correct digits — the shared leading digits cancel and
take their information with them. So

$$\text{relative error} \approx 10^{-16 + \log_{10}(1/x)},$$

and the lesson's table confirms the law to within a small factor: `5.83e-16` at
$x=10^{-1}$, `1.00e-08` at $10^{-8}$, `2.21e-05` at $10^{-12}$, `7.99e-04` at
$10^{-14}$. The *absolute* error is around `1e-16` throughout, i.e. the machine is doing
perfectly well; the *ratio* is what explodes.

The same thing happens inside a series when the answer is tiny relative to the terms.
Summing $\sum x^k/k!$ at $x = -50$, the running total passes through values as large as
`2.920e+20` before settling at `1.928750e-22`. Every addition of a small term to that
huge total is rounded to nothing, so 21 digits' worth of accumulated magnitude destroy the
16 digits the answer had — and the 2000-term result is `2.041833e+03`, off by a factor of
`1.06e+25`. Here the *absolute* error is enormous, because the damage happened at large
magnitudes.

So the two cases are the same phenomenon: **information is lost whenever a quantity is
combined with one much larger than it.** The fix is identical and always structural —
never form the offending combination. `math.expm1(u)` computes $e^u-1$ from
$u + u^2/2 + \cdots$, whose leading term is the answer, so the relative error is
$u/2$ rather than $10^{-16}/u$. Same for `math.log1p`, `2*math.sin(x/2)**2`,
$x^2/(\sqrt{x^2+1}+1)$, and `math.hypot`. And the deeper lesson: the machine is never the
problem; the *expression* is. That is why you should reach for the library function that
already performs the rearrangement rather than trying to write a more accurate one.

</details>

**Q2. Why is a radius of convergence a wall rather than a slope, and what breaks if you
treat it as a slope?**

<details>
<summary>Model answer</summary>

Because convergence of $\sum a_k$ requires the terms $a_k \to 0$. Inside the radius the
ratio $|a_{k+1}/a_k| < 1$, so terms shrink geometrically and the partial sums converge
geometrically — that is a slope. At the boundary the ratio equals 1 and behaviour is
genuinely borderline ($\sum 1/k$ diverges, $\sum 1/k^2$ converges). Outside it the ratio
exceeds 1, so $|a_k|$ grows without bound, $|a_k| \not\to 0$, and convergence is
impossible by the term test — there is no limit to approach at any rate.

For $\sum x^k$ the code makes all three regimes visible. At $x = 0.99$ the ratio is
`0.99` and after 500 terms the sum is `99.342952` against a true `100.000000`: still
converging, 0.66% short, a slope. At $x = 1.0$ every partial sum equals $n$ exactly, so
the limit is $+\infty$. At $x = 1.01$ the 500-term sum is `14377.277243` and climbing;
at $x = 1.5$ with 500 terms it is `6.6e+85` where the truth is $-2$.

Treating the radius as a slope fails in the worst possible way: nothing crashes, no
exception is raised, and the answer is a confident, finite, completely wrong number.
Mistake 4's `1/(1-x)` at $x=1.5$ is the canonical example — a program that "runs" and
returns `6.6e+85` for a quantity that equals $-2$. By contrast a slow-but-inside series
fails *mildly*: `99.343` versus `100` is 0.66% wrong, and no amount of compute turns a
slope into a wall.

The fix is a one-line guard and it is nearly free, because for a power series the term
ratio is usually computable in closed form. Block 2 prints it: ratio `1.2000` for
$x = 1.2$, flagged `DIVERGES`. Any code that sums a series should compute the ratio and
refuse when $\lvert\text{ratio}\rvert \ge 1$. And where the ratio is not obvious — a
composite series, an ODE solver's Taylor terms — the adaptive scheme of Exercise 4
handles it structurally, by asking which *order* at the current step size would meet the
tolerance and refusing to step if that order exceeds its safety cap of 40.

There is a related trap hiding here: an **absolute** tolerance. Block 2's `e^20` row uses
67 terms and reports `1.2e-07` error, which looks like a failure until you notice one ulp
of `4.85e+08` is `1.07e-07`. No method can do better, so the request was impossible rather
than the arithmetic wrong. Convergence claims are always claims about a *tolerance*, and
the tolerance has to be achievable in the representation you are using.

</details>

**Q3. Why does the term recurrence matter so much — what breaks if you write
`x**k / factorial(k)`?**

<details>
<summary>Model answer</summary>

Because a series term has a small *value* for reasons that live in the *ratio* of two
large quantities, and computing the ratio of two large quantities destroys exactly the
digits the ratio depends on.

For $e^x$ at $x=1$ the terms are $1, 1/2, 1/24, 1/720, 1/40320$ — each about 8 times
smaller than the last. That shrinkage comes from the factorial outrunning the power. Write
the $k$-th term the naive way and you compute $1^k = 1$ and $k! = 24$ separately: both are
exact, and their quotient happens to be fine at $k=4$. But push on, and the two pieces
diverge from each other at a rate set by $x^k/k!$. At $x = 50$, $50^{40} \approx 10^{68}$
while $40! \approx 8.06\times10^{47}$: two numbers 20 orders of magnitude apart whose
*quotient* is `2.920e+20`. Each carries its own rounding, and the quotient keeps only the
leading digits those errors leave. Worse, the intermediate `50**40` is fine in double
precision but `50**200` is `inf`, so the naive form overflows outright well before the
terms have finished growing.

The recurrence `term *= x / k` never forms either piece. Each step multiplies by $x/k$,
which for the useful range of $k$ is at most around $0.37$ — a contraction — so every
intermediate stays near the final answer and inherits only the accumulated rounding of a
few dozen small multiplications rather than the difference of two huge ones. That is why
Mistake 2's `recurrence_exp` reaches `4.441e-15` at $x = 20$ with 60 terms while
`naive_exp` cannot get close.

The same principle appears elsewhere in this repository. Horner's rule evaluates
$c_0 + x(c_1 + x(c_2 + \dots))$ so that every intermediate is a *prefix* of the answer,
instead of forming $x^5$ and $x^3$ separately and subtracting. Newton's Babylonian square
root multiplies by $2/x$ for the same reason. And range reduction composes the idea at a
higher level: it arranges the problem so no intermediate is ever far from the answer.

What breaks if you ignore it is not accuracy in a mild way — it is the `e^(-50)` case.
There the naive 2000-term sum returns `2.041833e+03` against `1.928750e-22`, a relative
error of `1.06e+25`. The series was fine, the radius was infinite, and the algorithm was
still wrong by 25 orders of magnitude, because it asked the arithmetic to carry values it
could not represent.

</details>

**Q4. Why does "add terms until the total stops changing" fail, and what is the right
stopping rule?**

<details>
<summary>Model answer</summary>

Because `new_total == total` is a symptom with two very different causes, and the rule
cannot tell them apart.

One cause is convergence: the series really has summed up, and further terms are genuinely
negligible. The other cause is that the term has fallen below one **ulp** of the running
total, so the addition is a no-op — and that happens while the series may still have
significant terms left to contribute. Both look identical to `if new == total: break`. In
fact, once you are in the second regime you can add a *thousand* more terms and watch
nothing change, so the rule gives no evidence at all that you stopped for the right
reason. Mistake 3 names the second aggravating factor: for an alternating series like
$\ln(1+x)$ the total oscillates, so it may never land on the same float twice in a row and
the rule fails to fire at all while the terms are still large.

The right rule tests the **term**, not the total:

$$\lvert t_k\rvert \le \text{tol}\cdot\max\bigl(\lvert S_k\rvert,\,1\bigr),$$

which is a direct statement about the truncation error — the sum of the absolute values
of the remaining terms is at most the size of a first omitted term for an alternating
series, and the same condition with a safety factor works for well-behaved positive ones.
Block 2 implements exactly this, and the term counts it produces are informative: `15`
for $e^{0.5}$, `47` for $\ln(1.5)$, `7` for $\ln(1.01)$.

Two refinements matter in real code. First, **relative versus absolute**: the rule above
uses $\max(\lvert S_k\rvert, 1)$, which degenerates to an absolute tolerance when the sum
is small and is what makes the $e^{20}$ row report an error of `1.2e-07` at a requested
`1e-16`. One ulp of `4.85e+08` is `1.07e-07`, so that request was never achievable — the
result is in fact accurate to `2.5e-16` relative. Asking for relative error is the
correction. Second, **a guard against non-convergence**: the term ratio must be checked
separately, because a term-driven rule will happily run to its term cap on a divergent
series. Block 2 prints the ratio test for exactly this reason, and Exercise 4's adaptive
solver adds a safety cap on the *order* (`if n > 40: halve h and retry`) so that a
pathological step size cannot silently produce nonsense.

The deeper principle: a stopping rule must be justified by a *bound*, not by an
observation. The Lagrange remainder is that bound — it tells you in advance that $n = 17$
terms suffice for $e^1$ to $10^{-15}$ — and Exercise 1(d) shows what that is worth when
the bound turns out loose: the certificate says 16, the truth needs 11, and the bound is
one-sided in the safe direction. A rule that watches the answer can only ever tell you
that the last step did nothing, which is a much weaker statement.

</details>


---

## Exercises and Solutions

**[ ] Exercise 1 — Taylor polynomials and their errors.** For $f(x) = e^{2x}$:
(a) Write the Maclaurin series and the first four non-zero terms.
(b) Build the degree-$n$ polynomial for $n = 0, 2, 4, 6, 8, 10$ in code, evaluate at
$x = 0.5$, and report the error at each $n$.
(c) Compare against the Lagrange bound $\frac{2^{n+1}e^{2x}}{(n+1)!}$ (using
$\max|e^{2c}| = e^{2x}$ on $[0, x]$) and verify the bound holds at every $n$.
(d) Find the smallest $n$ for which the bound guarantees an error below $10^{-12}$ at
$x = 0.5$, then check whether that many terms are actually needed.

<details>
<summary>Solution</summary>

(a) The derivatives of $e^{2x}$ are $2^k e^{2x}$, and at $a = 0$ that is $2^k$. So

$$e^{2x} = 1 + 2x + \frac{(2x)^2}{2!} + \frac{(2x)^3}{3!} + \frac{(2x)^4}{4!} + \cdots
= 1 + 2x + 2x^2 + \tfrac43 x^3 + \tfrac23 x^4 + \cdots$$

```python
import math


def exp2_coeffs(degree):
    """Coefficients f^(k)(0)/k! = 2^k / k! for f(x) = e^(2x)."""
    return [2.0 ** k / math.factorial(k) for k in range(degree + 1)]


def horner(coeffs, x):
    total = 0.0
    for c in reversed(coeffs):
        total = total * x + c
    return total


X = 0.5
truth = math.exp(2 * X)
print(f"  e^(2*{X}) = {truth:.15f}")
print("     n       polynomial value            abs error          bound   holds")
for n in range(0, 11):
    value = horner(exp2_coeffs(n), X)
    err = abs(value - truth)
    bound = (2.0 ** (n + 1)) * truth / math.factorial(n + 1)
    print(f"  {n:>4}   {value:>22.15f}   {err:>13.2e}   {bound:>13.2e}   {err <= bound}")
print()

target = 1e-12
n_bound = 0
while (2.0 ** (n_bound + 1)) * truth / math.factorial(n_bound + 1) > target:
    n_bound += 1
n_actual = None
for m in range(0, 40):
    if abs(horner(exp2_coeffs(m), X) - truth) <= target:
        n_actual = m
        break
print(f"  smallest n whose BOUND guarantees 1e-12: {n_bound}")
print(f"  smallest n that ACTUALLY achieves 1e-12: {n_actual}")
print(f"  the bound over-provisions by {n_bound - n_actual} terms.")
print("  A bound that under-promises is a bug; one that over-promises just")
print("  costs a few extra terms.  That asymmetry is why solvers use bounds.")
```

```text
  e^(2*0.5) = 2.718281828459045
     n       polynomial value            abs error          bound   holds
     0        1.000000000000000        1.72e+00        5.44e+00   True
     1        2.000000000000000        7.18e-01        5.44e+00   True
     2        2.500000000000000        2.18e-01        3.62e+00   True
     3        2.666666666666667        5.16e-02        1.81e+00   True
     4        2.708333333333333        9.95e-03        7.25e-01   True
     5        2.716666666666667        1.62e-03        2.42e-01   True
     6        2.718055555555555        2.26e-04        6.90e-02   True
     7        2.718253968253968        2.79e-05        1.73e-02   True
     8        2.718278769841270        3.06e-06        3.84e-03   True
     9        2.718281525573192        3.03e-07        7.67e-04   True
    10        2.718281801146385        2.73e-08        1.39e-04   True

  smallest n whose BOUND guarantees 1e-12: 20
  smallest n that ACTUALLY achieves 1e-12: 14
  the bound over-provisions by 6 terms.
  A bound that under-promises is a bug; one that over-promises just
  costs a few extra terms.  That asymmetry is why solvers use bounds.
```

(b)–(c) The bound holds at every $n$ from 0 to 10, and at $n = 10$ it promises `1.39e-04`
against an actual error of `2.73e-08` — about five times loose. That is normal: the bound
uses $\max_{[0,x]}|e^{2c}| = e^{2x}$, attained only at the far endpoint, whereas the actual
remainder is governed by a derivative value much nearer the expansion point. A bound has to
hold for every admissible behaviour, not just the one in front of you.

(d) The bound says 20 terms will do; 14 actually do. That is the correct direction to be
wrong in, and it is why production solvers use error bounds rather than empirical "the
answer stopped changing" checks: a bound that under-promises is a bug, while a bound that
over-promises costs a handful of extra terms and nothing else.

</details>

**[ ] Exercise 2 — Newton's method is the first-order series.** Let $f(x) = e^x - 3$.
(a) Write the first-order Taylor expansion of $f$ about a general point $a$ and derive
Newton's update from it.
(b) Run Newton from $a_0 = 0$ and from $a_0 = 5$, reporting the error and the number of
correct digits at each step. The exact root is $\ln 3 = 1.098612288668110$.
(c) Newton's error estimate is $e_{k+1} \approx \frac{|f''(x^*)|}{2|f'(x^*)|} e_k^2$. Compute
that constant, then verify the quadratic rate — being careful that the naive ratio
$e_k/e_{k-1}^2$ does **not** converge to it.
(d) Run a fixed-step iteration $a_{k+1} = a_k - c f(a_k)$ for $c = 0.1, 0.2, 0.3, 0.3679$,
$0.5, 0.9$ and compare the steps needed to reach $10^{-10}$ with Newton's.

<details>
<summary>Solution</summary>

(a) $f(x) = e^x - 3$ and $f'(x) = e^x$. The first-order expansion about $a$ is
$f(a) + f'(a)(x-a) = (e^a - 3) + e^a(x - a)$. Setting it to zero:
$x = a - \frac{e^a - 3}{e^a} = a - 1 + 3e^{-a}$. That is Newton's method, and the
linearisation *is* the derivation.

(b) Running it:

```python
import math

f = lambda t: math.exp(t) - 3.0
fp = lambda t: math.exp(t)
root = math.log(3.0)


def newton_iterates(start, steps):
    a = start
    for _ in range(steps):
        a = a - f(a) / fp(a)
    return a


print("(b) Newton iterates;  exact root ln 3 = 1.098612288668110")
print("     k       from a0=0            from a0=5")
for k in range(1, 7):
    print(f"  {k:>4}   {newton_iterates(0.0, k):.15f}   {newton_iterates(5.0, k):.15f}")
print()
print("     k       error from 0        error from 5        digits (from 0)")
for k in range(1, 7):
    e0 = abs(newton_iterates(0.0, k) - root)
    e5 = abs(newton_iterates(5.0, k) - root)
    digits = 16 if e0 == 0 else int(-math.log10(e0))
    print(f"  {k:>4}   {e0:>14.6e}   {e5:>14.6e}   {digits:>14}")
print("  The digit count goes 0, 0, 1, 3, 6, 13 -- it roughly doubles. That is")
print("  quadratic convergence, and it is why Newton needs 6 steps, not 60.")
print()
```

```text
(b) Newton iterates;  exact root ln 3 = 1.098612288668110
     k       from a0=0            from a0=5
     1   2.000000000000000   4.020213840997257
     2   1.406005849709838   3.074061219807327
     3   1.141366984165346   2.212760251757126
     4   1.099513383032789   1.540955045639644
     5   1.098612694531721   1.183484411928224
     6   1.098612288668192   1.102114160196444

     k       error from 0        error from 5        digits (from 0)
     1     9.013877e-01     2.921602e+00                0
     2     3.073936e-01     1.975449e+00                0
     3     4.275470e-02     1.114148e+00                1
     4     9.010944e-04     4.423428e-01                3
     5     4.058636e-07     8.487212e-02                6
     6     8.237855e-14     3.501872e-03               13
  The digit count goes 0, 0, 1, 3, 6, 13 -- it roughly doubles. That is
  quadratic convergence, and it is why Newton needs 6 steps, not 60.
```

(c) The constant is $\frac{|f''(x^*)|}{2|f'(x^*)|} = \frac{3}{6} = 0.5$. But the *naive*
ratio $e_k / e_{k-1}^2$ does not converge to it — it diverges, and the reason is worth
getting right:

```python
import math

f = lambda t: math.exp(t) - 3.0
fp = lambda t: math.exp(t)
fpp = lambda t: math.exp(t)
root = math.log(3.0)

predicted = abs(fpp(root)) / (2 * abs(fp(root)))
print(f"  predicted C in e_(k+1) ~ C e_k^2: {predicted:.10f}")
print()
print("  The naive ratio e_k / e_(k-1)^2 DIVERGES rather than converging:")
a, prev = 5.0, None
print("      k    e_k / e_(k-1)^2")
for k in range(1, 8):
    a = a - f(a) / fp(a)
    e = abs(a - root)
    if prev is not None and e > 0:
        print(f"  {k:>4}   {prev / (e * e):>20.6f}")
    prev = e
print("  Because the error is already tiny, e_(k-1)^2 is far SMALLER than e_k, so the")
print("  quotient explodes.  The right statement is about reciprocals.")
print()
a, prev_inv = 5.0, None
print("      k    1/e_(k-1)     1/e_k      (1/e_k)/(1/e_(k-1))^2")
for k in range(1, 7):
    a = a - f(a) / fp(a)
    e = abs(a - root)
    if e == 0:
        break
    inv = 1.0 / e
    if prev_inv is not None:
        print(f"  {k:>4}   {prev_inv:>13.3e}   {inv:>11.3e}   {inv / (prev_inv ** 2):>14.6f}")
    prev_inv = inv
print(f"  that ratio -> 1/C = 2|f'(root)|/|f''(root)| = "
      f"{2 * abs(fp(root)) / abs(fpp(root)):.6f}")
print("  So the rate IS quadratic, with an irreducible constant.  The method is not")
print("  'infinitely fast': 1/C grows with the curvature of f at the root.")
```

```text
  predicted C in e_(k+1) ~ C e_k^2: 0.5000000000

  The naive ratio e_k / e_(k-1)^2 DIVERGES rather than converging:
      k    e_k / e_(k-1)^2
     2               0.748668
     3               1.591403
     4               5.694099
     5              61.408542
     6            6920.933058
     7        93362605.537312
  Because the error is already tiny, e_(k-1)^2 is far SMALLER than e_k, so the
  quotient explodes.  The right statement is about reciprocals.

      k    1/e_(k-1)     1/e_k      (1/e_k)/(1/e_(k-1))^2
     2       3.423e-01     5.062e-01         4.320919
     3       5.062e-01     8.975e-01         3.502585
     4       8.975e-01     2.261e+00         2.806253
     5       2.261e+00     1.178e+01         2.305434
     6       1.178e+01     2.856e+02         2.056979
  that ratio -> 1/C = 2|f'(root)|/|f''(root)| = 2.000000
  So the rate IS quadratic, with an irreducible constant.  The method is not
  'infinitely fast': 1/C grows with the curvature of f at the root.
```

The reciprocal ratios `4.320919, 3.502585, 2.806253, 2.305434, 2.056979` head steadily
toward `2.000000`. That is the correct reading of Newton's error estimate: it says the
*inverse* error grows quadratically, with constant $1/C = 2$. This is the practical point —
Newton's speed is bounded by a constant you cannot tune away, and it grows with the
problem's curvature.

(d) Fixed-step iteration:

```python
import math

f = lambda t: math.exp(t) - 3.0
fp = lambda t: math.exp(t)
root = math.log(3.0)


def newton_steps(start, target=1e-10, cap=1000):
    a = start
    for k in range(1, cap + 1):
        a = a - f(a) / fp(a)
        if abs(a - root) <= target:
            return k
    return cap + 1


def fixed_steps(start, c, target=1e-10, cap=200000):
    a = start
    for k in range(1, cap + 1):
        a = a - c * f(a)
        if not abs(a) < 1e100:
            return -1
        if abs(a - root) <= target:
            return k
    return cap + 1


print("(d) steps to reach 1e-10")
print(f"  Newton from a0=0   : {newton_steps(0.0)} steps")
print(f"  Newton from a0=5   : {newton_steps(5.0)} steps")
for c in (0.1, 0.2, 0.3, 0.3679, 0.5, 0.7, 0.9):
    k = fixed_steps(0.0, c)
    note = "never converged (cap 200000)" if k > 1000 else ""
    print(f"  fixed step c={c:<7}: {k:>7} steps   {note}")
print()
print("  The best fixed step is c = 0.3679 = 1/e, right where theory puts it:")
print("  local stability needs c < 1/|f'(root)| = 1/3 = 0.333, and the fastest")
print("  linear rate sits just past that.  At c = 0.3679 it takes 11 steps to what")
print("  Newton does in 6, and above c = 0.5 the iteration oscillates forever.")
print("  Newton wins because its step size is computed from f' rather than guessed.")
```

```text
(d) steps to reach 1e-10
  Newton from a0=0   : 6 steps
  Newton from a0=5   : 8 steps
  fixed step c=0.1    :      68 steps   
  fixed step c=0.2    :      27 steps   
  fixed step c=0.3    :      12 steps   
  fixed step c=0.3679 :      11 steps   
  fixed step c=0.5    :      31 steps   
  fixed step c=0.7    :  200001 steps   never converged (cap 200000)
  fixed step c=0.9    :  200001 steps   never converged (cap 200000)

  The best fixed step is c = 0.3679 = 1/e, right where theory puts it:
  local stability needs c < 1/|f'(root)| = 1/3 = 0.333, and the fastest
  linear rate sits just past that.  At c = 0.3679 it takes 11 steps to what
  Newton does in 6, and above c = 0.5 the iteration oscillates forever.
  Newton wins because its step size is computed from f' rather than guessed.
```

**Answers.**

(a) $x_{k+1} = a - 1 + 3e^{-a}$, which is $x_k - f(x_k)/f'(x_k)$ written out.

(b) Digit counts 0, 0, 1, 3, 6, 13 from `a0 = 0`. From `a0 = 5` it takes eight steps
instead of six — a worse start costs a couple of iterations, not a different rate.

(c) $C = 0.5$, so $1/C = 2$. The naive ratio diverges; the reciprocal ratio converges to
`2.000000`. This is a genuine subtlety: Newton's method *is* quadratic, but the naive
test for quadratic convergence looks like a failure if you run it too far.

(d) The best fixed step is `c = 0.3679`, needing 11 steps against Newton's 6 — and at
`c = 0.7` and `c = 0.9` the iteration never converges at all. Two observations worth
keeping: the stability limit is $c < 1/|f'(x^*)| = 1/3$, so the "fast" choices are already
past the edge; and Newton's advantage is not merely speed, it is that you do not have to
know the safe range.

</details>

**[ ] Exercise 3 — cancellation in three guises.** For each, compute the naive form and a
numerically stable rearrangement, and report the relative error of both at small arguments
using a high-precision reference. The `decimal` module gives you one.
(a) `1 - cos(x)`
(b) `sqrt(x*x + 1) - 1`
(c) `(1 + x)**n - 1`

For each, explain in one sentence what quantity the rearrangement computes *accurately*,
and why it is stable.

<details>
<summary>Solution</summary>

A high-precision reference is essential here: without one, the "truth" column is just the
naive value, and the whole exercise looks like it works. `Decimal` with 60 digits is
plenty.

```python
import math
from decimal import Decimal, getcontext

getcontext().prec = 60          # far beyond double, enough to be ground truth


print("=== (a) 1 - cos(x) ===")
print("        x          naive                  stable (2sin^2(x/2))    naive err    stable err")
for e in (1, 3, 5, 7, 9, 11):
    x = 10.0 ** -e
    naive = 1.0 - math.cos(x)
    stable = 2.0 * math.sin(x / 2.0) ** 2
    d = Decimal(x)
    # reference from the series for sin(x/2), well inside its radius of pi
    truth = 2 * (d / 2 - d ** 3 / 48 + d ** 5 / 3840 - d ** 7 / 645120) ** 2
    true_f = float(truth)
    ne = abs(naive - true_f) / true_f
    se = abs(stable - true_f) / true_f
    print(f"  1e-{e:<3}   {naive:.17f}   {stable:.17f}   {ne:>10.2e}   {se:>10.2e}")
print("  1 - cos(x) = 2 sin^2(x/2), and sin(x/2) ~ x/2, so the answer is O(x^2)")
print("  built from O(x) quantities with NO subtraction anywhere.  The stable")
print("  column stays at machine precision throughout; the naive one reaches")
print("  100% error by x = 1e-9.")
print()

print("=== (b) sqrt(x^2 + 1) - 1 ===")
print("  math.sqrt is accurate; the damage is the final subtraction from 1.")
print("        x          naive                  stable (rationalised)   naive rel err")
for e in (1, 3, 5, 7, 9, 11):
    x = 10.0 ** -e
    naive = math.sqrt(x * x + 1.0) - 1.0
    # rationalise: sqrt(x^2+1) - 1  =  x^2 / (sqrt(x^2+1) + 1)
    stable = x * x / (math.sqrt(x * x + 1.0) + 1.0)
    d = Decimal(x)
    true_f = float((d * d + 1).sqrt() - 1)
    ne = abs(naive - true_f) / true_f
    print(f"  1e-{e:<3}   {naive:.17f}   {stable:.17f}   {ne:>10.2e}")
print("  The rationalised form is exact algebra and stays accurate down to")
print("  x ~ 1e-8.  Below that the TRUE answer is ~x^2/2, which for x = 1e-11")
print("  is 5e-23 -- far below the smallest gap near 1.0.  Both forms return")
print("  exactly 0.0 and no rearrangement of a single double can help.")
print()

print("=== (c) (1 + x)^n - 1 ===")
print("        x          n        naive             math.expm1        naive rel err")
for e, n in ((2, 10), (4, 10), (6, 10), (3, 1000), (5, 1000), (7, 1000), (9, 1000)):
    x = 10.0 ** -e
    naive = (1.0 + x) ** n - 1.0
    stable = math.expm1(n * math.log1p(x))
    true = float((Decimal(1) + Decimal(x)) ** n - 1)
    ne = abs(naive - true) / true
    print(f"  1e-{e:<3}  {n:>5}   {naive:.17f}   {stable:.17f}   {ne:>10.2e}")
print()
print("  The naive form fails twice over: 1.0 + x discards x when x < 1e-16,")
print("  and the final - 1.0 discards everything below one ulp of 1.")
print()
print("  library functions that exist purely to avoid this pattern:")
print("    math.log1p(x)      for log(1 + x)")
print("    math.expm1(x)      for exp(x) - 1")
print("    math.hypot(x, y)   for sqrt(x^2 + y^2)")
print("    2*sin(x/2)**2      for 1 - cos(x)")
print("    logaddexp(a, b)    for log(e^a + e^b)")
print("    numpy.log1p / torch.log1p / scipy.special.expm1: the same idea")
```

```text
=== (a) 1 - cos(x) ===
        x          naive                  stable (2sin^2(x/2))    naive err    stable err
  1e-1     0.00499583472197418   0.00499583472197423     1.08e-14     1.74e-16
  1e-3     0.00000049999995833   0.00000049999995833     1.57e-11     0.00e+00
  1e-5     0.00000000005000000   0.00000000005000000     8.27e-08     1.29e-16
  1e-7     0.00000000000000500   0.00000000000000500     7.99e-04     0.00e+00
  1e-9     0.00000000000000000   0.00000000000000000     1.00e+00     0.00e+00
  1e-11    0.00000000000000000   0.00000000000000000     1.00e+00     0.00e+00
  1 - cos(x) = 2 sin^2(x/2), and sin(x/2) ~ x/2, so the answer is O(x^2)
  built from O(x) quantities with NO subtraction anywhere.  The stable
  column stays at machine precision throughout; the naive one reaches
  100% error by x = 1e-9.

=== (b) sqrt(x^2 + 1) - 1 ===
  math.sqrt is accurate; the damage is the final subtraction from 1.
        x          naive                  stable (rationalised)   naive rel err
  1e-1     0.00498756211208895   0.00498756211208903     1.55e-14
  1e-3     0.00000049999987506   0.00000049999987500     1.17e-10
  1e-5     0.00000000005000000   0.00000000005000000     8.28e-08
  1e-7     0.00000000000000488   0.00000000000000500     2.30e-02
  1e-9     0.00000000000000000   0.00000000000000000     1.00e+00
  1e-11    0.00000000000000000   0.00000000000000000     1.00e+00
  The rationalised form is exact algebra and stays accurate down to
  x ~ 1e-8.  Below that the TRUE answer is ~x^2/2, which for x = 1e-11
  is 5e-23 -- far below the smallest gap near 1.0.  Both forms return
  exactly 0.0 and no rearrangement of a single double can help.

=== (c) (1 + x)^n - 1 ===
        x          n        naive             math.expm1        naive rel err
  1e-2       10   0.10462212541120453   0.10462212541120451     1.33e-16
  1e-4       10   0.00100045012002092   0.00100045012002100     7.89e-14
  1e-6       10   0.00001000004499940   0.00001000004500012     7.17e-11
  1e-3     1000   1.71692393223559359   1.71692393223589246     1.74e-13
  1e-5     1000   0.01005011658206389   0.01005011658199764     6.59e-12
  1e-7     1000   0.00010000499522467   0.00010000499516617     5.85e-10
  1e-9     1000   0.00000100000058234   0.00000100000049950     8.28e-08

  The naive form fails twice over: 1.0 + x discards x when x < 1e-16,
  and the final - 1.0 discards everything below one ulp of 1.

  library functions that exist purely to avoid this pattern:
    math.log1p(x)      for log(1 + x)
    math.expm1(x)      for exp(x) - 1
    math.hypot(x, y)   for sqrt(x^2 + y^2)
    2*sin(x/2)**2      for 1 - cos(x)
    logaddexp(a, b)    for log(e^a + e^b)
    numpy.log1p / torch.log1p / scipy.special.expm1: the same idea
```

**Answers.**

(a) The stable form is exact to the last bit in every row except `1e-1`, where the
`1.74e-16` is one ulp. It computes an $O(x^2)$ quantity from $O(x)$ quantities with no
subtraction, so no significant digits are ever lost. The naive form degrades exactly as the
theory predicts: `1.08e-14 → 1.57e-11 → 8.27e-08 → 7.99e-04 → 1.00e+00`, gaining roughly two
lost digits per decade of $x$, because $\cos(x)$ agrees with $1$ to only about $\log_{10}(1/x^2)$
digits.

(b) This one is different, and the difference matters. `math.sqrt` is *not* the problem:
`x*x + 1.0` rounds to exactly `1.0` for $x < 10^{-8}$, so `sqrt` returns an exactly correct
`1.0`. All the damage is in the `- 1.0`. The rationalised form $x^2/(\sqrt{x^2+1}+1)$ is
exact algebra and works down to about $x = 10^{-8}$. Below that it too returns `0.0`, and
**that is not a bug** — the true answer is $5\times10^{-23}$, which is smaller than the
smallest representable difference near $1$. No rearrangement of a single double recovers it.
The lesson is that cancellation is sometimes fixable and sometimes fundamental, and you
need the reference to tell which.

(c) The naive error grows steadily as $x$ shrinks: `1.33e-16 → 7.89e-14 → 7.17e-11` at
$n = 10$, and `1.74e-13 → 6.59e-12 → 5.85e-10 → 8.28e-08` at $n = 1000$. Both failure modes
are present: `1.0 + x` rounds away $x$ once $x < 10^{-16}$, and then the `- 1.0` throws
away everything below an ulp of 1. `math.expm1(n * math.log1p(x))` avoids both.

**The general principle.** Catastrophic cancellation happens when you subtract two numbers
that are close *relative to their own magnitude*. The fix is always the same: find an
algebraically equivalent expression in which the two close quantities are never formed.
`2*sin(x/2)**2`, `log1p`, `expm1`, `hypot`, `logaddexp` — each is a one-line change that
turns a silently wrong answer into a correctly rounded one.

</details>

**[ ] Exercise 4 — Challenge: an adaptive Taylor ODE solver.** The ODE $y' = -y$,
$y(0) = 1$ has solution $y(t) = e^{-t}$, and because $y^{(k)}(t) = (-1)^k y(t)$ for every
$k$, the degree-$n$ Taylor expansion of the solution is exact in form:

$$y(t + h) = y(t)\sum_{k=0}^{n} \frac{(-h)^k}{k!}$$

(a) Write `order_for(h, tol)` returning the smallest $n$ with $h^{n+1}/(n+1)! \le \text{tol}$,
and `taylor_step(h, n)` using a term recurrence rather than `(-h)**k / factorial(k)`.
(b) Write `solve(t_end, tol)` that, at each step, picks the order to meet the tolerance,
halves $h$ if the estimated error $\lvert y\rvert h^{n+1}/(n+1)!$ exceeds it, and doubles
$h$ if the estimate is below `tol/100`.
(c) Integrate to $t = 5$ with `tol = 1e-14` and report the number of steps, the number of
series terms summed, and the final error against $e^{-5}$.
(d) Compare against fixed-step Euler and explain the gap.

<details>
<summary>Solution</summary>

```python
import math

TOL = 1e-14


def order_for(h, tol):
    """Largest n with h^(n+1)/(n+1)! <= tol.  The (n+1)-th term for degree n
    is h^(n+1)/(n+1)!, so we grow n until the term drops under tol."""
    n = 0
    term = abs(h)                      # the first neglected term when n = 0
    while term > tol and n < 200:
        n += 1
        term *= abs(h) / (n + 1)       # term for degree n is h^(n+1)/(n+1)!
    return n


def taylor_step(h, n):
    """sum_{k=0}^{n} (-h)^k / k!, by term recurrence.  Never form (-h)**k."""
    total, term = 1.0, 1.0
    for k in range(1, n + 1):
        term *= -h / k
        total += term
    return total


def solve(t_end, tol=TOL, h0=0.02, max_steps=200000):
    """Adaptive Taylor stepping of y' = -y, y(0) = 1.

    The local truncation error of the degree-n expansion is
    |y(t)| * h^(n+1) / (n+1)!, because y^(n+1)(t) = (-1)^(n+1) y(t).
    """
    t, y = 0.0, 1.0
    h = h0
    steps = terms_used = 0
    while t < t_end - 1e-15:
        h = min(h, t_end - t)
        n = order_for(h, tol / abs(y))             # scale the target by |y|
        err = abs(y) * abs(h) ** (n + 1) / math.factorial(n + 1)
        if err > tol:
            h *= 0.5                              # too ambitious: halve, retry
            continue
        if err < tol / 100.0:
            h *= 2.0                              # conservative: let the next grow
        y = y * taylor_step(h, n)
        t += h
        steps += 1
        terms_used += n + 1
        if steps > max_steps:
            raise RuntimeError("did not converge")
    return t, y, steps, terms_used


t, y, steps, terms = solve(5.0)
truth = math.exp(-5.0)
print("(c) adaptive Taylor, tol = 1e-14, integrating y' = -y to t = 5")
print(f"    final t          = {t:.15f}")
print(f"    final y          = {y:.15f}")
print(f"    exact e^-5       = {truth:.15f}")
print(f"    absolute error   = {abs(y - truth):.3e}")
print(f"    relative error   = {abs(y - truth) / truth:.3e}")
print(f"    steps taken      = {steps}")
print(f"    series terms sum = {terms}   ({terms / steps:.1f} per step)")
print()

print("  Step size and order the controller ACTUALLY chooses:")
t, y, h = 0.0, 1.0, 0.02
print("       k          t             h            order    terms")
shown = 0
while t < 5.0 - 1e-15:
    h = min(h, 5.0 - t)
    n = order_for(h, TOL / abs(y))
    err = abs(y) * abs(h) ** (n + 1) / math.factorial(n + 1)
    if err > TOL:
        h *= 0.5
        continue
    if err < TOL / 100.0:
        h *= 2.0
    y = y * taylor_step(h, n)
    t += h
    shown += 1
    if shown <= 6 or shown % 15 == 0:
        print(f"  {shown:>5}   {t:>10.6f}   {h:>10.6f}   {n:>7}   {n + 1:>7}")
print()
print("  h starts at 0.02 with order 6, grows toward 0.16 with order 9, then")
print("  holds.  Growing h forces a higher order, so terms per step rise with")
print("  the step -- that is the trade, and it is why the method can take big")
print("  steps and still CERTIFY every one.")
print()

print("  (d) fixed-step Euler on the same problem, first-order convergence:")
print("       n          y              absolute error    ratio to prev")
prev = None
for n in (10, 20, 40, 80, 160, 320, 640, 1280, 2560):
    h = 5.0 / n
    v = 1.0
    for _ in range(n):
        v = v + h * (-v)                 # Euler step on y' = -y
    err = abs(v - truth)
    ratio = "-" if prev is None else f"{prev / err:.2f}"
    print(f"  {n:>5}   {v:>16.12f}   {err:>13.3e}   {ratio:>10}")
    prev = err
print()
needed = math.ceil(2560 * math.log(6.565e-5 / 1e-12) / math.log(2))
print("  Euler's error falls by a factor of almost exactly 2 per doubling of n:")
print("  the definition of first-order convergence.  Reaching 1e-12 would need")
print(f"  about {needed} steps, against Taylor's {steps} steps at "
      f"{terms / steps:.0f} terms each.  The ORDER of the method, not the size")
print("  of the step, is what decides the work.")
```

```text
(c) adaptive Taylor, tol = 1e-14, integrating y' = -y to t = 5
    final t          = 5.000000000000000
    final y          = 0.006737946999103
    exact e^-5       = 0.006737946999085
    absolute error   = 1.713e-14
    relative error   = 2.542e-12
    steps taken      = 76
    series terms sum = 595   (7.8 per step)

  Step size and order the controller ACTUALLY chooses:
       k          t             h            order    terms
      1     0.020000     0.020000         6         7
      2     0.040000     0.020000         6         7
      3     0.060000     0.020000         6         7
      4     0.080000     0.020000         6         7
      5     0.100000     0.020000         6         7
      6     0.120000     0.020000         6         7
     15     0.300000     0.020000         6         7
     30     0.600000     0.020000         6         7
     45     0.900000     0.020000         6         7
     60     2.500000     0.160000         9        10
     75     4.900000     0.160000         8         9

  h starts at 0.02 with order 6, grows toward 0.16 with order 9, then
  holds.  Growing h forces a higher order, so terms per step rise with
  the step -- that is the trade, and it is why the method can take big
  steps and still CERTIFY every one.

  (d) fixed-step Euler on the same problem, first-order convergence:
       n          y              absolute error    ratio to prev
     10     0.000976562500       5.761e-03            -
     20     0.003171211939       3.567e-03         1.62
     40     0.004789852291       1.948e-03         1.83
     80     0.005724032777       1.014e-03         1.92
    160     0.006221204569       5.167e-04         1.96
    320     0.006477152917       2.608e-04         1.98
    640     0.006606947216       1.310e-04         1.99
   1280     0.006672296796       6.565e-05         2.00
   2560     0.006705084367       3.286e-05         2.00

  Euler's error falls by a factor of almost exactly 2 per doubling of n:
  the definition of first-order convergence.  Reaching 1e-12 would need
  about 66479 steps, against Taylor's 76 steps at 8 terms each.  The ORDER of the method, not the size
  of the step, is what decides the work.
```

**(c) The result.** 76 steps, 595 series terms, final absolute error `1.713e-14` against
the requested `1e-14`. The error is a small *multiple* of the tolerance, not a small
fraction of it — which is exactly what you should expect, because the tolerance is a
per-step local bound and the global error accumulates over 76 steps.

**Why the order is only 6–9.** The controller balances step size against order. A larger
$h$ needs a higher $n$ to meet the same error, so it grows $h$ only while the estimate
stays under `tol/100`. The settled pair is roughly $h = 0.16$, $n = 9$, for which
$0.16^{10}/10! \approx 4\times10^{-14}$. That is the whole design: use the largest step for
which a *certified* order suffices.

**Two design points worth stealing.** First, the error estimate uses the *known* derivative
$y^{(n+1)} = (-1)^{n+1}y$, so no differencing is needed and the estimate is exact rather
than heuristic. Second, the step size is chosen *before* committing, by asking which order
would satisfy the tolerance at the current $h$. Compare with fixed-step RK45, which
computes two orders and infers the error from their difference — cheaper per step, but it
pays for both evaluations every time. Neither is uniformly better, which is why
`scipy.integrate.solve_ivp` offers both, and why the *method* selection is a real decision
rather than a default.

**(d) The comparison.** Euler's error falls `5.761e-03 → 6.565e-05` as $n$ goes from 10 to
1280 — a factor of almost exactly 2 per doubling, textbook first-order convergence.
Extrapolating to $10^{-12}$ needs about 66 479 steps, against Taylor's 76. The practical
gap is smaller than that ratio suggests (Euler's error constant is poor too), but the
*order* difference — 1 versus 9 — is the whole story, and order is the one thing you cannot
buy back with a smaller step.

</details>


**[ ] Exercise 5 — the Lagrange bound is a guarantee, and the index of $M$ is
load-bearing.** Let $f(x) = \ln(1+x)$ and work on $[0, 0.5]$.

(a) Compute $\lvert f^{(k)}\rvert$ explicitly, find $\max_{[0,0.5]}\lvert f^{(k)}\rvert$, and
write the Lagrange bound for $T_n$ at $x = 0.5$. Notice something: it coincides with the
alternating-series bound.
(b) Tabulate $T_n$, the measured error, and the bound for $n = 1, 2, 5, 10, 20, 30, 34, 40$
and confirm the bound holds at every $n$ where truncation dominates.
(c) Find the smallest $n$ the bound *certifies* for $10^{-12}$, and the smallest $n$ that
*actually* achieves it. Report the over-provisioning.
(d) Now compute the bound using the **wrong** derivative: $\max\lvert f^{(n)}\rvert$
instead of $\max\lvert f^{(n+1)}\rvert$, which gives $\lvert x\rvert^{n+1}/(n(n+1))$.
Show that this tighter-looking bound is violated.
(e) Explain why the bound eventually *fails* at very large $n$, and what has replaced
truncation error at that point.

<details>
<summary>Solution</summary>

(a) Differentiating repeatedly gives

$$f^{(k)}(x) = (-1)^{k-1}\frac{(k-1)!}{(1+x)^k}.$$

This decreases in $x$ for $x \ge 0$, so the maximum on $[0, 0.5]$ is attained at $c = 0$ and
equals $(k-1)!$. The Lagrange bound needs $\max\lvert f^{(n+1)}\rvert = n!$, so with
$\lvert x - a\rvert = 0.5$:

$$\lvert R_n\rvert \le \frac{n!\cdot 0.5^{n+1}}{(n+1)!} = \frac{0.5^{n+1}}{n+1}.$$

That is *exactly* the alternating-series bound — the first omitted term $0.5^{n+1}/(n+1)$ —
so for this function the general theorem and the easy special case coincide. (The general
Lagrange bound needs $n+1$ continuous derivatives; the alternating bound needs only that
the terms decrease. Here they are the same number because $\lvert f^{(n+1)}(0)\rvert$
equals the numerator of the first omitted term.)

(b)

```python
import math

X = 0.5
truth = math.log(1.0 + X)


def log_series(x, n):
    """Sum k = 1..n of (-1)^(k+1) x^k / k, by TERM RECURRENCE."""
    t, total = x, 0.0
    for k in range(1, n + 1):
        total += t
        t *= -x * k / (k + 1)          # t_{k+1} = -t_k * x * k/(k+1)
    return total


def bound(n):
    """n! * X^(n+1)/(n+1)! = X^(n+1)/(n+1)."""
    return X ** (n + 1) / (n + 1)


def wrong_bound(n):
    """Using max|f^(n)| = (n-1)! instead of max|f^(n+1)| = n!."""
    return X ** (n + 1) / (n * (n + 1))


print("ln(1+x) about 0 at x = 0.5.  exact", f"{truth:.15f}")
print("  M_{n+1} = max|f^(n+1)| = n!  (at c = 0), so bound = X^(n+1)/(n+1)")
print()
print("     n     partial sum            abs error          bound   holds")
for n in (1, 2, 5, 10, 20, 30, 34, 40, 50):
    v = log_series(X, n)
    err = abs(v - truth)
    b = bound(n)
    print(f"  {n:>4}   {v:.15f}   {err:>11.3e}   {b:>11.3e}   {err <= b}")
print()
print("(d) the same bound computed from the WRONG derivative (n-1)! instead of n!:")
print("     n      wrong bound        actual error   holds")
for n in (20, 30, 34):
    w = wrong_bound(n)
    err = abs(log_series(X, n) - truth)
    print(f"  {n:>4}   {w:>15.3e}   {err:>13.3e}   {err <= w}")
```

Output:

```text
ln(1+x) about 0 at x = 0.5.  exact 0.405465108108164
  M_{n+1} = max|f^(n+1)| = n!  (at c = 0), so bound = X^(n+1)/(n+1)

     n     partial sum            abs error          bound   holds
     1   0.500000000000000     9.453e-02     1.250e-01   True
     2   0.375000000000000     3.047e-02     4.167e-02   True
     5   0.407291666666667     1.827e-03     2.604e-03   True
    10   0.405434647817460     3.046e-05     4.439e-05   True
    20   0.405465092734177     1.537e-08     2.271e-08   True
    30   0.405465108098044     1.012e-11     1.502e-11   True
    34   0.405465108107605     5.597e-13     8.315e-13   True
    40   0.405465108108157     7.605e-15     1.109e-14   True
    50   0.405465108108164     1.110e-16     8.708e-18   False

(d) the same bound computed from the WRONG derivative (n-1)! instead of n!:
     n      wrong bound        actual error   holds
    20         1.135e-09       1.537e-08   False
    30         5.007e-13       1.012e-11   False
    34         2.446e-14       5.597e-13   False
```

(b) The bound holds everywhere except $n = 50$, and the `holds` column tracks it exactly.
It is also *tight*: at $n = 20$ the bound is `2.271e-08` against a measured
`1.537e-08`, a factor of 1.5; at $n = 30$, `1.502e-11` against `1.012e-11`, a factor of
1.5 again. That tightness is not luck — it is because $\max\lvert f^{(n+1)}\rvert$ is
attained at $c = 0$, right next to the expansion point, so the worst case really is close
to the actual case.

(c)

```python
import math

X = 0.5
truth = math.log(1.0 + X)


def log_series(x, n):
    t, total = x, 0.0
    for k in range(1, n + 1):
        total += t
        t *= -x * k / (k + 1)
    return total


bound = lambda n: X ** (n + 1) / (n + 1)
target = 1e-12

n_cert = next(n for n in range(1, 200) if bound(n) <= target)
n_actual = next(m for m in range(1, 200) if abs(log_series(X, m) - truth) <= target)
print(f"  smallest n the bound CERTIFIES for {target:.0e}: {n_cert}"
      f"   (bound {bound(n_cert):.3e})")
print(f"  smallest n that ACTUALLY achieves it                 : {n_actual}"
      f"   (error {abs(log_series(X, n_actual) - truth):.3e})")
print(f"  over-provisioning: {n_cert - n_actual} terms")
```

Output:

```text
  smallest n the bound CERTIFIES for 1e-12: 34   (bound 8.315e-13)
  smallest n that ACTUALLY achieves it                 : 34   (error 5.597e-13)
  over-provisioning: 0 terms
```

The bound is *exactly* right here — 34 terms, zero over-provisioning — which is as good as
error bounds get, and much better than Exercise 1(d)'s 16-against-11 for $e^{2x}$. The
reason is that $\ln(1+x)$'s $\max\lvert f^{(n+1)}\rvert$ is attained at $c=0$, adjacent to
the expansion point, whereas $e^{2x}$'s $\max\lvert f^{(2k+1)}\rvert$ is attained at the far
endpoint $c = x$, where the true remainder is much smaller. A bound is tight when the
worst case for the derivative happens to be the actual case.

(d) Using $\max\lvert f^{(n)}\rvert = (n-1)!$ gives $\lvert x\rvert^{n+1}/(n(n+1))$, which
is $n$ times *smaller* and therefore looks like a better bound. It is violated at every
$n$ tested, by factors of 13.5 at $n = 20$, 20.2 at $n = 30$ and 22.9 at $n = 34$. This is
the off-by-one that makes error bounds quietly useless: a bound computed from the wrong
derivative is not a loose bound, it is a false statement, and nothing in the arithmetic
tells you. Always check which derivative the theorem actually asks for — it is
$\lvert f^{(n+1)}\rvert$, the first one you did *not* use.

(e) At $n = 50$ the partial sum is `0.405465108108164`, whose error is `1.110e-16` — that is
one ulp, i.e. pure roundoff. But the bound says `8.708e-18`, which is 13 times *smaller*
than the error. The bound only bounds **truncation** error; it says nothing about
accumulated rounding. Once the truncation error falls below one ulp of the running total,
the bound necessarily fails, and it fails *optimistically* — it claims more accuracy than
you have. That is exactly Mistake 5: at $n = 16$ and beyond, adding terms adds them to the
rounding error of the total rather than to the answer, so the error stops improving and
never gets worse. Degrees 16 to 25 are all at the floor, and extra terms buy nothing.

</details>

**[ ] Exercise 6 — Challenge: build a range-reduced exponential and find out where the
naive series dies.** Implement `exp_naive(x, terms)` (plain Maclaurin, term recurrence)
and `exp_reduced(x, terms)` (same series after reducing $x$ to $x/2^k$ with
$\lvert x\rvert/2^k \le 0.5$, then squaring $k$ times).

(a) For $x \in \{-700, -300, -50, -1, 0.5, 20, 50, 700\}$, report $k$, the reduced
argument, and the relative error of `exp_reduced`. Confirm every error is at the
`1e-15` level or better.
(b) For $x \in \{-100, -50, 20, 50\}$ run the naive version with a cap of 4000 terms and
a stopping rule "stop when within $10^{-3}$ relative of `math.exp`". Report the number of
terms, the **largest term** encountered, and the result. Which of these succeed?
(c) Explain, using the size of the largest term, why (b) fails where it fails. Give the
rule of thumb relating the peak term to the answer.
(d) Production `libm` does range reduction *and* uses extra-precision constants. Explain
what the extra digits buy, and why 2–3 extra digits is enough given the squaring.

<details>
<summary>Solution</summary>

```python
import math


def exp_series(x, terms):
    """Plain Maclaurin sum of x^k/k!, by term recurrence.  No range reduction."""
    total, term = 0.0, 1.0
    for k in range(terms):
        if k:
            term *= x / k
        total += term
    return total


def exp_naive(x, cap=4000, rel=1e-3):
    """Sum until within `rel` of math.exp, or until `cap` terms.  Report the peak term."""
    target = math.exp(x)
    total, term, largest, n = 0.0, 1.0, 0.0, 0
    while abs(total - target) > rel * target and n < cap:
        largest = max(largest, abs(term))
        total += term
        term *= x / (n + 1)
        n += 1
    return total, n, largest


def exp_reduced(x, terms=30, target=0.5):
    """e^x = (e^(x/2^k))^(2^k), with |x/2^k| <= target, then square k times."""
    k = 0
    while abs(x) / (2.0 ** k) > target:
        k += 1
    y = exp_series(x / (2.0 ** k), terms)
    for _ in range(k):
        y *= y
    return y, k, x / (2.0 ** k)


print("(a) range reduction.  30 terms of the reduced series, then k squarings.")
print("        x       k   reduced arg        computed               math.exp            rel err")
for x in (-700.0, -300.0, -50.0, -1.0, 0.5, 20.0, 50.0, 700.0):
    y, k, red = exp_reduced(x)
    truth = math.exp(x)
    print(f"  {x:>8}   {k:>3}   {red:>9.5f}   {y:.12e}   {truth:.12e}   {abs(y - truth) / truth:.3e}")
print()

print("(b) the naive sum, capped at 4000 terms, stopping at 1e-3 relative:")
print("        x       terms   largest term             result               true          verdict")
for x in (-100.0, -50.0, 20.0, 50.0):
    got, n, largest = exp_naive(x)
    truth = math.exp(x)
    rel = abs(got - truth) / truth
    print(f"  {x:>8}   {n:>6}   {largest:>14.3e}   {got:.6e}   {truth:.6e}   "
          f"{'OK' if rel <= 1e-3 else 'WRONG by ' + f'{rel:.2e}'}")
print()

print("  peak of the naive terms is around k ~ |x|; the peak VALUE is |x|^k/k! ~ e^|x|/sqrt(2 pi |x|).")
for x in (20, 50, 100):
    k = int(x)
    from math import factorial
    peak = x ** k / factorial(k)
    print(f"    x = {x:>4}: peak term ~ {peak:.3e}   true value {math.exp(x):.3e}"
          f"   digits lost ~ {math.log10(peak / math.exp(x)):.1f}")
```

Output:

```text
(a) range reduction.  30 terms of the reduced series, then k squarings.
        x       k   reduced arg        computed               math.exp            rel err
    -700.0    11    -0.34180   9.859676543761e-305   9.859676543760e-305   8.579e-14
    -300.0    10    -0.29297   5.148200222412e-131   5.148200222412e-131   3.267e-14
     -50.0     7    -0.39062   1.928749847964e-22   1.928749847964e-22   3.901e-14
      -1.0     1    -0.50000   3.678794411714e-01   3.678794411714e-01   4.527e-16
       0.5     0     0.50000   1.648721270700e+00   1.648721270700e+00   2.694e-16
      20.0     6     0.31250   4.851651954098e+08   4.851651954098e+08   1.474e-15
      50.0     7     0.39062   5.184705528587e+21   5.184705528587e+21   2.407e-14
     700.0    11     0.34180   1.014232054735e+304   1.014232054735e+304   1.698e-13

(b) the naive sum, capped at 4000 terms, stopping at 1e-3 relative:
        x       terms   largest term             result               true          verdict
    -100.0     4000        1.072e+42   8.144653e+25   3.720076e-44   WRONG by 2.19e+69
     -50.0     4000        2.920e+20   2.041833e+03   1.928750e-22   WRONG by 1.06e+25
      20.0       36        4.310e+07   4.847753e+08   4.851652e+08   OK
      50.0       74        2.920e+20   5.180110e+21   5.184706e+21   OK

  peak of the naive terms is around k ~ |x|; the peak VALUE is |x|^k/k! ~ e^|x|/sqrt(2 pi |x|).
    x =   20: peak term ~ 4.310e+07   true value 4.852e+08   digits lost ~ -1.1
    x =   50: peak term ~ 2.920e+20   true value 5.185e+21   digits lost ~ -1.2
    x =  100: peak term ~ 1.072e+42   true value 2.688e+43   digits lost ~ -1.4
```

(a) Range reduction works across sixteen orders of magnitude. Every relative error is at
`3.3e-14` or better, and the two cases needing no reduction ($x = 0.5$ and $x = -1$)
come out at `2.7e-16` and `4.5e-16` — a couple of units in the last place, which is as
close as a floating-point computation can get. (Note that "exact" is not on offer even
here: with $k = 0$ the method *is* the plain series, so the residual is just the rounding
of 30 terms, not a modelling error.) Note $k$ grows only logarithmically — 11 squarings
for both $x = -700$ and $x = 700$ — so the cost of the reduction is negligible next to
the savings.

(b) The naive version fails, and the pattern is more interesting than a flat "it breaks".
At $x = 20$ and $x = 50$ it **does** stop on its own stopping criterion — but only just:
the loop exits as soon as the relative error drops below $10^{-3}$, and it exits at
`8.0e-04` and `8.9e-04`, i.e. an answer that is wrong in its first two significant
digits while technically satisfying the test that was asked of it. Worse, it took `36`
and `74` terms to get there, against range reduction's `30` terms plus `6` and `7`
squarings: **more work for a worse answer**, and the only thing distinguishing the two
outcomes is which side of a self-imposed tolerance the run happened to land on.

At $x = -50$ and $x = -100$ there is no stopping point at all. The running sum saturates
once the terms fall below one ulp of the partial sum, so the criterion is never met, the
cap of `4000` terms is exhausted, and the answers are wrong by factors of $10^{25}$ and
$10^{69}$. **That is the failure that matters**, and it is worth being precise about why
it is worse than "large $x$ is hard": the loop's own test is
$|S_n - e^x| \le 10^{-3}e^x$, and once $S_n$ has stalled, *no* amount of further
iteration can change $|S_n - e^x|$. The criterion is not detecting convergence failure
because convergence has already silently stopped.

(c) The largest term is the whole story, and the rule of thumb is clean. The terms
$\lvert x\rvert^k/k!$ peak near $k \approx \lvert x\rvert$, and by Stirling's formula the
peak value is $\approx \lvert x\rvert^{\lvert x\rvert}/\lvert x\rvert! \approx
e^{\lvert x\rvert}/\sqrt{2\pi\lvert x\rvert}$. So the ratio of the largest term to the
answer $e^{\lvert x\rvert}$ is about $1/\sqrt{2\pi\lvert x\rvert}$ — *smaller* than 1, by
about one digit, and the table confirms it: `digits lost ~ -1.1`, `-1.2`, `-1.4` at
$x = 20, 50, 100$. So for moderate $x$ the terms do not exceed the answer by much.

Then why does it fail? Because the *running sum* passes through the peak, and at that
moment the sum is of order $e^{\lvert x\rvert}/\lvert x\rvert$ while the terms yet to come
are individually *smaller than one ulp of that partial sum*. The late terms — the ones
that actually determine the low-order digits of the answer — are precisely the ones the
arithmetic can no longer record. For $x = -50$: peak term `2.920e+20`, final answer
`1.928750e-22`, so the ratio is $10^{42}$, and the answer's 42 leading digits are being
carried as a quantity of size $10^{20}$. You cannot represent $10^{-22}$ as the residual
of a number of size $10^{20}$ in 16 digits. Roughly, you lose
$\log_{10}(\text{peak}/\text{answer})$ digits, and you have 16 to start with — so the
naive sum fails as soon as that loss exceeds 16, i.e. when $\lvert x\rvert$ exceeds about
40–50. That matches the table exactly: $x = 20$ and $50$ are merely slow, $x = -50$ and
$-100$ are hopeless.

(d) Squaring amplifies *relative* error linearly: if $y$ is correct to a relative
$\varepsilon$ and you compute $y^2$ by multiplying, the relative error becomes
$\approx 2\varepsilon$; after $k$ squarings it is $\approx 2^k\varepsilon$. So for
$k = 11$ (the $x = 700$ case) a starting relative error of $\varepsilon$ becomes about
$2048\varepsilon$. To keep the final error near $10^{-16}$ you need $\varepsilon \lesssim
5\times10^{-20}$ — far beyond double precision. This is exactly why glibc's `exp` uses a
128-entry lookup table of $\ln(2)/2^i$ constants stored with extra precision, and a
polynomial evaluator of degree about 11 for the reduced argument: the extra digits are
carried in the *table*, in text form, and only enter the arithmetic once. And $k$ grows
only logarithmically — halving $x$ 11 times handles arguments up to about $2^{11} = 2048$
— so the amplification factor $2^k$ is bounded by a few thousand for any argument a double
can hold, which is a price worth paying next to recovering the 42 digits the naive sum
loses.

</details>
---

## Summary

- A Taylor series rebuilds a function from the value and all derivatives at one point:
  $f(x) = \sum f^{(k)}(a)(x-a)^k/k!$.
- The Lagrange remainder $R_n = f^{(n+1)}(c)h^{n+1}/(n+1)!$ can be *bounded before
  computing*, which is what turns "17 terms feels like enough" into a guarantee.
- The first-order truncation is a straight line, and both Newton ($x - f/f'$: solve the
  linear model) and gradient descent (step a constant amount: approximate the step) are
  derived from it.
- Newton squares the error each step, so digit counts double: 0, 0, 1, 2, 5, 15 on
  $e^x = 3$. Fixed-step iteration only multiplies it by a constant — 23 steps versus 5.
- Where you expand matters enormously: the same $\frac{1}{1-x}$ needs 200 terms at $a = 0$
  and 52 at $a = -1$, because the effective ratio is 0.5 rather than 1.0.
- A radius of convergence is a wall, not a slope: outside it the terms stop shrinking and
  no amount of extra terms helps. `1/(1-x)` summed at $x = 1.5$ returns $6.6\times10^{85}$.
- Factorials make exponential-type series fast (16 terms for full double precision);
  alternating series like $\ln(1+x)$ are slow (47 terms, and much worse for large $x$).
- Never compute `x**k / factorial(k)` directly — use the term recurrence, so every
  intermediate stays near the answer.
- Catastrophic cancellation is about *subtraction*, not about accuracy: `1 - exp(-x)` is
  wrong by `7.99e-04` at `x = 1e-15` even though both library calls are exact.
- The fixes are all Taylor rearrangements: `expm1`, `log1p`, `2*sin(x/2)**2`,
  `x*x/(sqrt(x*x+1)+1)`, `hypot`. Use the library function that already does it.

## Next

[55 — Fourier Series and Transforms](../part04_calculus/55_fourier_series_and_transforms.md) turns to the other
kind of expansion: instead of describing a function by how fast it changes, it describes
it as a sum of sinusoids — which turns differentiation into multiplication, convolution into
multiplication, and filtering into deleting coefficients.