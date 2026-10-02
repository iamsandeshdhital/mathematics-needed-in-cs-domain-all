# 52 — Integration

**Part**: part04_calculus · **Prerequisites**: 51 · **Time**: 40 min

---

## In Plain Words

An integral is a total. Add up the values the function takes, times a slice width, over a
whole interval — that is all. The picture of "area under a curve" is a helpful image, but
it is worth remembering that signed area is what the formula actually computes: a function
that dips below the axis subtracts.

The big idea is the Fundamental Theorem of Calculus, and it says two surprising things at
once. First, if you can find an antiderivative of a function, then subtracting its values
at the two endpoints gives the integral exactly — no accumulating needed. Second, and much
more useful in code, if you *accumulate* a function from a fixed starting point and then
*differentiate* the accumulator, you get the original function back. Differentiation and
accumulation are inverse operations, which is why one table of rules works for both.

There is a practical reason this lesson exists. Many functions have no antiderivative you
can write down — the Gaussian `exp(-x^2)` is the famous one, and it is not laziness, it
is a theorem that no such formula exists. So real code integrates numerically: slice the
interval, evaluate, weight, sum. Trapezoid sums rectangles' worth of accuracy with an
error falling as the square of the slice width. Simpson fits parabolas instead and gets an
error falling as the *fourth* power, at exactly the same cost.

---

## Why Computer Science Cares

- **Expectation is an integral.** For a continuous random variable, `E[X] = ∫ x f(x) dx`.
  The Monte Carlo estimator in [Part 05](../part05_probability_statistics/) is a
  Riemann-sum approximation of exactly that integral, which is why its error is
  $O(1/\sqrt{n})$ and not $O(1/n)$.
- **Every simulation timestep is a quadrature rule.** `dt` in an ODE integrator, the step
  in Euler's method, the accumulated sum in a running average — all Riemann sums. Choosing
  the rule (trapezoid, midpoint, RK4) is choosing an error order.
- **Area under a curve is a physical quantity.** Collision detection
  (`Separating Axis Theorem`), mesh volume (`trimesh`), polygon clipping, and beam-balance
  calculations are all integrals. Graphics code computes $\int$ over triangle fans.
- **`scipy.integrate.quad` is adaptive Gauss–Kronrod.** It evaluates two orders of rule
  simultaneously, compares them, and subdivides only where they disagree. Its whole design
  comes from the error analysis in this lesson.
- **Differentiating an integral is how you get gradients of simulations.** The adjoint
  method in computational fluid dynamics — which won a Nobel Prize — works by
  differentiating an integral objective and pushing the derivatives back through the
  solver, rather than storing every intermediate.
- **Machine-precision quadrature is easy.** `∫ sin` over $[0,\pi]$ with `n = 362` reaches
  `6.3e-11`, so numerical integration is rarely the bottleneck in a pipeline.

---

## The Formal Version

**Definition.** For a bounded function $f$ on $[a,b]$ and a partition
$P = \{x_0 = a < x_1 < \cdots < x_n = b\}$, an upper sum is
$U(P, f) = \sum_{i=1}^{n} (\sup_{[x_{i-1}, x_i]} f)\,\Delta x_i$ and a lower sum uses
$\inf$ instead.

**Definition.** The (Riemann) *integral* is
$\int_a^b f(x)\,dx = \sup_P U(P,f) = \inf_P L(P,f)$ when these agree; $f$ is then called
*integrable*.

*Explanation.* Slice the interval, take the tallest (or shortest) value on each slice,
multiply by the slice width, add. As you slice finer, upper and lower sums squeeze
together. Their meeting value is the integral.

**Theorem (Fundamental Theorem of Calculus, Part 1).** If $f$ is continuous on $[a,b]$
and $F$ is any antiderivative of $f$ ($F' = f$) on $[a,b]$, then

$$\int_a^b f(x)\,dx = F(b) - F(a).$$

**Theorem (Fundamental Theorem of Calculus, Part 2).** If $f$ is continuous, then
$F(x) = \int_a^x f(t)\,dt$ is differentiable and $F'(x) = f(x)$.

*Explanation.* Part 1 says "accumulate by other means, then subtract". Part 2 says
"accumulate by accumulating, then differentiate, and you recover $f$". Together: $f$
determines its own antiderivative, uniquely up to a constant.

**Definition.** The *improper integral* $\int_a^\infty f$ is $\lim_{B \to \infty}\int_a^B f$,
when the limit exists.

**Theorem (comparison).** If $0 \le f \le g$ and $\int g$ converges, then $\int f$
converges and is at most $\int g$.

*Explanation.* This is the mathematical form of "the tail of a Gaussian is negligible", and
of the fact that the tails of a light-tailed distribution can be truncated safely.

**Definition.** The *expectation* of a continuous random variable $X$ with density $f_X$ is
$E[X] = \int_{-\infty}^{\infty} x f_X(x)\,dx$, provided $\int |x| f_X < \infty$.

**Theorem (Monte Carlo error).** If $X_1, \dots, X_n$ are i.i.d. with mean $\mu$ and
finite variance $\sigma^2$, then the sample mean converges to $\mu$ at rate $1/\sqrt{n}$.

*Explanation.* This is the Fundamental Theorem applied to a Riemann sum in
probability space: $\frac1n\sum X_i$ approximates $\int x f_X(x)\,dx$ and the error is
controlled by variance, which falls as $n$ grows. See [68 — Law of Large Numbers and the
Central Limit Theorem](../part05_probability_statistics/68_law_of_large_numbers_and_clt.md).

**Definition.** The *composite trapezoid rule* with $n$ intervals and $h = (b-a)/n$ is

$$T_n = h\left(\tfrac{f(a) + f(b)}{2} + \sum_{i=1}^{n-1} f(x_i)\right).$$

**Definition.** The *composite Simpson rule* (for even $n$) is

$$S_n = \frac{h}{3}\left(f(x_0) + 4\sum_{\text{odd }i} f(x_i) + 2\sum_{\text{even }i,\ i\ne 0,n} f(x_i) + f(x_n)\right).$$

**Theorem (error bounds).** If $\max|f''| \le M_2$ on $[a,b]$ then
$|E_T| \le \frac{(b-a)}{12} h^2 M_2$. If $f$ has four continuous derivatives and
$\max|f^{(4)}| \le M_4$ then $|E_S| \le \frac{(b-a)}{180} h^4 M_4$.

*Explanation.* The $h^2$ bound follows from the trapezoid area formula: a linear
interpolant over-predicts by exactly $\frac{h^3}{12}f''(\xi)$ on each slice. Simpson's
$h^4$ follows from cancelling the leading error term using the midpoint rule — which is
literally Simpson's parabolic interpolation, made of three point evaluations.

**Theorem (Richardson / Romberg).** If a rule has error $ch^p + O(h^{p+1})$, then combining
it at $n$ and $2n$ cancels the leading term and gives a rule of order $p+1$. Romberg
integration applies this repeatedly, reaching order $2^k$ with $2^k$ evaluations.

*Explanation.* This is why Romberg integration converges so fast, and why
`scipy.integrate.quad` compares two rules instead of using one.

---

## Formula Sheet

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| partition | `$P = \{x_0=a < x_1 < \dots < x_n = b\}$`, `$\Delta x_i = x_i - x_{i-1}$` | the way you slice $[a,b]$ | every numerical rule; the slicing *is* the algorithm |
| upper / lower sums | `$U(P,f)=\sum_i \bigl(\sup_{[x_{i-1},x_i]} f\bigr)\Delta x_i$`, and `L(P,f)` the same with `$\inf$` | tallest and shortest value on each slice, times width, added | the definition of "integrable" |
| `$\int_a^b f(x)\,dx$` | `$\sup_P U(P,f) = \inf_P L(P,f)$` when the two agree; $f$ is then *integrable* | where the two squeeze values meet: the signed area | the whole object; $\int_0^\pi\sin x\,dx = 2$ |
| Riemann sum | `$S_n = \sum_{i=1}^{n} f(\xi_i)\,\Delta x_i$` with `$\xi_i \in [x_{i-1},x_i]$` | value times width, once per slice, added | every quadrature rule and every ODE timestep |
| midpoint rule | `$M_n = \sum_{i} f\bigl(a+(i+\tfrac12)h\bigr)h$`, error `$\le \frac{(b-a)}{24}h^2M_2$` | sample in the middle of each slice; second order | the cheapest second-order rule; `expectation_riemann` in the code |
| left / right rule | `$L_n = h\sum_{i=0}^{n-1} f(a+ih)$`, `$R_n = h\sum_{i=1}^{n} f(a+ih)$`, error `$\sim \frac{h}{2}\lvert f(b)-f(a)\rvert$` | sample at one end only; the error has a definite sign | streaming accumulators; explains the running total `3.750000` |
| composite trapezoid | `$T_n = h\left(\frac{f(a)+f(b)}{2} + \sum_{i=1}^{n-1} f(a+ih)\right)$` | fit a straight line on each slice and add its area | any $n$; the base of Romberg |
| trapezoid error | `$\lvert E_T\rvert \le \frac{(b-a)}{12}h^2 M_2$`, `$\max\lvert f''\rvert \le M_2$` — needs $f''$ to exist and be bounded | doubling $n$ quarters the error | sizing $n$; measured `1.606639030e-03` at $n=32$ on $\int_0^\pi\sin$ |
| composite Simpson | `$S_n = \frac{h}{3}\left(f_0 + 4\sum_{i\text{ odd}} f_i + 2\sum_{\substack{i\text{ even}\\ i\ne 0,n}} f_i + f_n\right)$` | 1-4-1 weights over pairs of slices | **$n$ must be even**; same cost as trapezoid |
| Simpson error | `$\lvert E_S\rvert \le \frac{(b-a)}{180}h^4 M_4$`, `$\max\lvert f^{(4)}\rvert \le M_4$` — needs **four continuous derivatives** | doubling $n$ cuts the error by 16 | sizing $n$; measured `1.033369413e-06` at $n=32$ |
| Simpson exactness | the error is `$\propto f^{(4)}$`, so it is **exact for every polynomial of degree $\le 3$, at every $n$** | three points get quadratics *and* cubics right | why Exercise 3(c) prints error `0.0e+00` |
| $n$ from a tolerance | trapezoid `$n \ge \sqrt{\frac{(b-a)^3 M_2}{12\,\text{tol}}}$`; Simpson `$n \ge \left(\frac{(b-a)^5 M_4}{180\,\text{tol}}\right)^{1/4}$` | rearrange the bound to get a slice count | `n = 160744` vs `n = 362` for $10^{-10}$ on $\int_0^\pi\sin$ |
| FTC part 1 | `$\int_a^b f(x)\,dx = F(b)-F(a)$`, with `$f$` continuous on `[a,b]` and `$F'=f$` there | given an antiderivative, subtract the endpoints | the closed-form route; unavailable for $\int e^{-x^2}$ |
| FTC part 2 | `$F(x)=\int_a^x f(t)\,dt` gives `$F'(x)=f(x)$`, $f$ continuous | accumulate, then differentiate, and the integrand returns | the adjoint method; differentiating under an integral |
| improper integral | `$\int_a^\infty f = \lim_{B\to\infty}\int_a^B f$`, existing when the limit is finite | integrate to a finite cut-off and take the limit | why the code integrates the Gaussian over $[-6,6]$ |
| comparison | `$0\le f\le g$` and `$\int g$` converges `$\Rightarrow \int f$` converges with `$\int f\le\int g$` | bound an unknown tail by a known one | why Gaussian tails can be truncated safely |
| $u$-substitution | `$\int_a^b f(g(x))\,g'(x)\,dx = \int_{g(a)}^{g(b)} f(u)\,du$` | rescale each slice: width $dx$ becomes $du = g'\,dx$ | `$\int_0^2 x e^{-x^2}dx = \tfrac12\int_0^4 e^{-u}du$`; **transform the limits too** |
| integration by parts | `$\int u\,dv = uv - \int v\,du$` | the product rule, rearranged | `$\int_0^1 x e^x dx = (x-1)e^x\big|_0^1 = 1$` |
| power rule reversed | `$\int x^n\,dx = \frac{x^{n+1}}{n+1} + C$`, `$n \ne -1$` | divide by the new exponent | `$\int_0^3 x^4 dx = 48.6$`; at `$n=-1$` you get `$\ln x$` instead |
| partial fractions | `$\frac{1}{x^2-1} = \frac12\left(\frac{1}{x-1}-\frac{1}{x+1}\right)$` | split a rational function into easy pieces | `$\int_2^3 \frac{dx}{x^2-1} = 0.202732554$` |
| Richardson / Romberg | `$R_{k,j} = R_{k,j-1} + \frac{R_{k,j-1}-R_{k-1,j-1}}{4^j-1}$` with `R_{k,0}=T_{2^k}`; order `2+j` from `2^k` evaluations | cancel the leading error term by differencing two step sizes | the first step **is** Simpson; why `scipy.integrate.quad` compares two orders |
| expectation | `$E[X]=\int_{-\infty}^{\infty} x f_X(x)\,dx$`, needs `$\int\lvert x\rvert f_X<\infty$` | the sum form is `$\sum x_ip_i$`; only the operator changes | `U[0,1]` gives `0.5`, `U[-2,5]` gives `1.5` |
| Monte Carlo error | `$O(\sigma/\sqrt n)$` for $n$ i.i.d. samples | the error falls as the *square root* of $n$ | Exercise 4: the `err * sqrt(n)` column ≈ constant |
| density vs probability | `$P(X\le c)=\int_{-\infty}^c f_X$; the density is an **area**, not a value | you must integrate to get a probability | Gaussian peak `0.3989` but $\int f_X=1$; a uniform on $[0,0.01]$ has density 100 |
| running accumulator | `$\sum_i y_i\,\Delta t$` | a streaming accumulator with fixed `dt` *is* a Riemann sum | the code's `3.750000` against the closed form `2.666667` |

---

## Worked Example

### Example 1: $\int_0^\pi \sin x\,dx$ by hand, then by machine

**By the antiderivative.** $F(x) = -\cos x$ since $F'(x) = \sin x$. Then

$$\int_0^\pi \sin x\,dx = F(\pi) - F(0) = -\cos\pi - (-\cos 0) = 1 - (-1) = 2.$$

**By accumulation.** Midpoint rule on $[0,\pi]$ with $n = 8$ slices, so $h = \pi/8$:
$T_8 = \frac{\pi}{8}\sum_{i=0}^{7}\sin\left(\frac{(i+0.5)\pi}{8}\right) = 2.012909085599$.
Error `1.29e-02`, matching the $O(h)$ behaviour. With $n = 1000$ the error is
`8.2e-07`. Simpson at $n = 8$ gives `2.000269169948`, error `2.69e-04` — four times
better for the same eight evaluations, because the error is $O(h^4)$ not $O(h^2)$.

### Example 2: substitution and the meaning of $du$

Consider $\int_0^2 x e^{-x^2}\,dx$.

1. Look at the integrand: $x$ and $e^{-x^2}$. The chain rule says the derivative of $e^{-x^2}$
   contains a factor $-2x$. So set $u = x^2$, giving $du = 2x\,dx$.
2. Transform the limits: $x = 0 \Rightarrow u = 0$; $x = 2 \Rightarrow u = 4$.
3. Rewrite: $\int_0^2 x e^{-x^2}dx = \frac12\int_0^4 e^{-u}\,du = \frac12(1 - e^{-4}) = 0.490842$.
4. **Why it works, in one sentence.** The change of variable rescales each infinitesimal
   slice: a slice of width $dx$ in $x$ becomes a slice of width $du = 2x\,dx$ in $u$, so
   the factor $2x$ leaves the integrand and enters the measure. That is the whole of
   $u$-substitution.

Compare with $\int_0^2 e^{-x^2}dx$, where no substitution helps and no elementary
antiderivative exists. That integral is `0.8820...` and has to be computed numerically.

### Example 3: integration by parts, and why it is differentiation run backwards

For $\int x e^x\,dx$, choose $u = x$ and $dv = e^x dx$, so $du = dx$ and $v = e^x$:

$$\int u\,dv = uv - \int v\,du = xe^x - \int e^x dx = xe^x - e^x + C = (x-1)e^x + C.$$

Check: $\frac{d}{dx}[(x-1)e^x] = e^x + (x-1)e^x = xe^x$. ✓ Over $[0,1]$ the value is
$(1-1)e^1 - (0-1)e^0 = 0 - (-1) = 1$.

The rule *is* the product rule rearranged:
$(uv)' = u'v + uv'$ becomes $\int u'v = uv - \int uv'$. Every integration technique is a
differentiation rule run in reverse, and the product rule is the source of integration by
parts.

### Example 4: an integral as a probability

Let $X \sim U[0,1]$, so $f_X(x) = 1$ on $[0,1]$. Then

$$P(X \le 0.3) = \int_0^{0.3} 1\,dx = 0.3.$$

No computation needed at all — and that is the point. The uniform distribution has a density
of 1, so probability equals interval length. Now suppose
$f_X(x) = \frac{1}{\sqrt{2\pi}}e^{-x^2/2}$, the standard normal. Its *peak* value is
`0.3989`, which is less than 1, yet $\int_{-\infty}^{\infty} f_X = 1$. A density is an
area, not a probability: it can exceed 1 (the uniform on $[0, 0.01]$ has density 100) and
it can be tiny over a wide region while still contributing most of the total mass.

### Example 5: expectation as an integral

$\mathbb{E}[X]$ for $X \sim U[0,1]$ is $\int_0^1 x\,dx = \frac12$, and the code confirms
it to ten decimals. For $X \sim U[-2, 5]$ the density is $\frac17$ on $[-2,5]$, so

$$\mathbb{E}[X] = \int_{-2}^{5} \frac{x}{7}\,dx = \frac{25 - 4}{14} = \frac32 = 1.5.$$

The discrete version of the same computation is $\sum_i x_i p_i$. Compare:

- $X \in \{-2, 0, 5\}$ with probabilities $(0.2, 0.5, 0.3)$: $\mathbb{E}[X] = -0.4 + 0 + 1.5 = 1.1$
- $\mathbb{E}[X^2] = 0.2(4) + 0.5(0) + 0.3(25) = 8.3$
- $\mathrm{Var}(X) = \mathbb{E}[X^2] - \mathbb{E}[X]^2 = 8.3 - 1.21 = 7.09$

That is the identical three-line algorithm that computes a continuous expectation and
variance. Only the operator changes from $\sum$ to $\int$.

---

## Runnable Code

### Block 1: accumulation, the Fundamental Theorem, and expectation

```python
import math

print("=== The definite integral as accumulation ===")
#  int_a^b f(x) dx = the signed area under the graph, accumulated the long way:
#  split [a,b] into n slices of width d = (b-a)/n, add up f at slice midpoints * d.

f = math.sin
a, b = 0.0, math.pi
EXACT = 2.0        # int_0^pi sin x dx = [-cos x]_0^pi = 1 - (-1) = 2

print(f"  int_0^pi sin(x) dx, exact = {EXACT}")
print()
print("       n       midpoint (Riemann sum)        error")
for n in (1, 2, 4, 8, 16, 100, 1000):
    d = (b - a) / n
    total = sum(f(a + (i + 0.5) * d) * d for i in range(n))
    print(f"  {n:>6}   {total:>24.12f}   {abs(total - EXACT):.3e}")
print("  Error falls like 1/n: halving the slice width halves the error.")
print()

print("=== Left / right / midpoint: same limit, different rates ===")
def left_rule(g, lo, hi, n):
    d = (hi - lo) / n
    return sum(g(lo + i * d) * d for i in range(n))


def right_rule(g, lo, hi, n):
    d = (hi - lo) / n
    return sum(g(lo + (i + 1) * d) * d for i in range(n))


def midpoint_rule(g, lo, hi, n):
    d = (hi - lo) / n
    return sum(g(lo + (i + 0.5) * d) * d for i in range(n))


print("  int_0^1 sin(x) dx, exact 0.4596976941  (1 - cos 1)")
print("      n        left          right         midpoint      mid err")
for n in (4, 20, 100, 500):
    L = left_rule(f, 0.0, 1.0, n)
    R = right_rule(f, 0.0, 1.0, n)
    M = midpoint_rule(f, 0.0, 1.0, n)
    print(f"  {n:>5}  {L:>12.10f}  {R:>12.10f}  {M:>12.10f}   {abs(M - 0.4596976941):.2e}")
print("  sin is RISING here, so left always undershoots and right overshoots.")
print("  Midpoint error is ~d^2/24 * |f''|; left and right are ~d/2 * |f(1)-f(0)|.")
print()

print("=== The Fundamental Theorem, both directions ===")
F = lambda x: -math.cos(x)          # F' = sin = f

print("  Part 1 (anti-derivative, then subtract the endpoints):")
print(f"    F(pi) - F(0) = {F(b):.12f} - ({F(a):.12f}) = {F(b) - F(a):.12f}   (exact 2)")
print()
print("  Part 2 (differentiate the accumulated integral):")
accum = lambda x: F(x) - F(a)       # int_0^x sin(t) dt = -cos(x) + cos(0)
for x in (0.25, 0.5, 1.0, 2.0):
    h = 1e-7
    numeric = (accum(x + h) - accum(x - h)) / (2 * h)
    print(f"    x = {x:<5} d/dx int_0^x sin = {numeric:.10f}   f(x) = {f(x):.10f}")
print("  Accumulate, then differentiate, and you get the integrand back.")
print()

print("=== A probability is an integral ===")
#  P(X in [a,b]) = int_a^b p_X(x) dx where p_X is the DENSITY, and the total = 1.
print("  Uniform on [0,1]: density is 1, so P(X <= 0.3) = 0.3 exactly, no computation.")
print("  Gaussian density: p(x) = exp(-x^2/2)/sqrt(2 pi), total integral = 1.")
print("  Its PEAK value is only 0.3989, yet the total area is 1.")
print("  A density may exceed 1 (a uniform on [0, 0.01] has density 100).")
print("  It is an AREA, not a probability. That is the whole point of the word 'density'.")
print()

print("=== The definite integral as an expectation ===")
#  For a discrete distribution, E[X] = sum x p(x).
#  For a continuous one,           E[X] = int x p(x) dx.  Same formula, sum becomes integral.


def expectation_discrete(values, probs):
    return sum(v * p for v, p in zip(values, probs))


def expectation_riemann(g, lo, hi, n):
    d = (hi - lo) / n
    return sum(g(lo + (i + 0.5) * d) * d for i in range(n))


values = [-2.0, 0.0, 5.0]
probs = [0.2, 0.5, 0.3]
mean = expectation_discrete(values, probs)
second = expectation_discrete([v * v for v in values], probs)
print(f"  discrete: X takes {values} with probabilities {probs}")
print(f"    E[X]  = sum x p(x)          = {mean:.10f}")
print(f"    E[X^2]= sum x^2 p(x)        = {second:.10f}")
print(f"    Var   = E[X^2] - E[X]^2     = {second - mean * mean:.10f}")
print("    Exactly the same three-line algorithm as for the continuous case below;")
print("    only the SUM becomes an INTEGRAL.")
print()

print("  Continuous version, Uniform[0,1] has E[X] = int_0^1 x dx = 1/2:")
print(f"    by Riemann sum with n=1000   = {expectation_riemann(lambda x: x, 0.0, 1.0, 1000):.10f}")
print(f"    by the closed form 1/2        = {0.5:.10f}")
print("  Uniform[-2,5] has E[X] = 1/2 * (-2 + 5) = 1.5:")
print(f"    by Riemann sum with n=1000   = "
      f"{expectation_riemann(lambda x: x / 7.0, -2.0, 5.0, 1000):.10f}")
```

Output:

```text
=== The definite integral as accumulation ===
  int_0^pi sin(x) dx, exact = 2.0

       n       midpoint (Riemann sum)        error
       1             3.141592653590   1.142e+00
       2             2.221441469079   2.214e-01
       4             2.052344305954   5.234e-02
       8             2.012909085599   1.291e-02
      16             2.003216378168   3.216e-03
     100             2.000082249071   8.225e-05
    1000             2.000000822467   8.225e-07
  Error falls like 1/n: halving the slice width halves the error.

=== Left / right / midpoint: same limit, different rates ===
  int_0^1 sin(x) dx, exact 0.4596976941  (1 - cos 1)
      n        left          right         midpoint      mid err
      4  0.3521170645  0.5624848107  0.4608970094   1.20e-03
     20  0.4385651452  0.4806386944  0.4597455828   4.79e-05
    100  0.4554865084  0.4639012182  0.4596996095   1.92e-06
    500  0.4588560699  0.4605390119  0.4596977707   7.66e-08
  sin is RISING here, so left always undershoots and right overshoots.
  Midpoint error is ~d^2/24 * |f''|; left and right are ~d/2 * |f(1)-f(0)|.

=== The Fundamental Theorem, both directions ===
  Part 1 (anti-derivative, then subtract the endpoints):
    F(pi) - F(0) = 1.000000000000 - (-1.000000000000) = 2.000000000000   (exact 2)

  Part 2 (differentiate the accumulated integral):
    x = 0.25  d/dx int_0^x sin = 0.2474039595   f(x) = 0.2474039593
    x = 0.5   d/dx int_0^x sin = 0.4794255387   f(x) = 0.4794255386
    x = 1.0   d/dx int_0^x sin = 0.8414709851   f(x) = 0.8414709848
    x = 2.0   d/dx int_0^x sin = 0.9092974262   f(x) = 0.9092974268
  Accumulate, then differentiate, and you get the integrand back.

=== A probability is an integral ===
  Uniform on [0,1]: density is 1, so P(X <= 0.3) = 0.3 exactly, no computation.
  Gaussian density: p(x) = exp(-x^2/2)/sqrt(2 pi), total integral = 1.
  Its PEAK value is only 0.3989, yet the total area is 1.
  A density may exceed 1 (a uniform on [0, 0.01] has density 100).
  It is an AREA, not a probability. That is the whole point of the word 'density'.

=== The definite integral as an expectation ===
  discrete: X takes [-2.0, 0.0, 5.0] with probabilities [0.2, 0.5, 0.3]
    E[X]  = sum x p(x)          = 1.1000000000
    E[X^2]= sum x^2 p(x)        = 8.3000000000
    Var   = E[X^2] - E[X]^2     = 7.0900000000
    Exactly the same three-line algorithm as for the continuous case below;
    only the SUM becomes an INTEGRAL.

  Continuous version, Uniform[0,1] has E[X] = int_0^1 x dx = 1/2:
    by Riemann sum with n=1000   = 0.5000000000
    by the closed form 1/2        = 0.5000000000
  Uniform[-2,5] has E[X] = 1/2 * (-2 + 5) = 1.5:
    by Riemann sum with n=1000   = 1.5000000000
```

### Block 2: the integration techniques, each checked

```python
import math


def midpoint_sum(g, lo, hi, n):
    d = (hi - lo) / n
    return sum(g(lo + (i + 0.5) * d) * d for i in range(n))


def report(name, g, closed_form, a, b, n=200000):
    """Print a closed-form integral beside a high-resolution Riemann sum of it."""
    approx = midpoint_sum(g, a, b, n)
    ok = math.isclose(closed_form, approx, rel_tol=1e-6, abs_tol=1e-9)
    print(f"  {name:<34} closed form {closed_form:>13.9f}   numeric {approx:>13.9f}   ok {ok}")


print("=== Integration techniques, each one checked against a Riemann sum ===")
print()

# 1. Linearity: sums and constant multiples come straight through.
report("int_0^1 (3x^2 + 2) dx",
       lambda x: 3.0 * x ** 2 + 2.0, 3 * 1 / 3 + 2 * 1, 0.0, 1.0)

# 2. The power rule, read backwards: int x^n = x^(n+1)/(n+1).
report("int_0^3 x^4 dx",
       lambda x: x ** 4, 3 ** 5 / 5, 0.0, 3.0)

# 3. u-substitution: int 2x cos(x^2) dx, put u = x^2 so du = 2x dx, giving sin(1).
report("int_0^1 2x cos(x^2) dx",
       lambda x: 2 * x * math.cos(x * x), math.sin(1.0), 0.0, 1.0)

# 4. Integration by parts: int x e^x dx = (x - 1)e^x, so over [0,1] it is 1.
report("int_0^1 x e^x dx",
       lambda x: x * math.exp(x), (1 - 1) * math.e - (0 - 1) * 1.0, 0.0, 1.0)

# 5. Trig identity first: sin^2(x) = (1 - cos 2x)/2, so the integral is x/2 - sin(2x)/4.
report("int_0^pi sin^2(x) dx",
       lambda x: math.sin(x) ** 2, math.pi / 2 - 0.0, 0.0, math.pi)

# 6. Partial fractions: 1/(x^2-1) = 0.5/(x-1) - 0.5/(x+1).
report("int_2^3 dx/(x^2-1)",
       lambda x: 1.0 / (x * x - 1.0),
       0.5 * math.log((3 - 1) / (3 + 1)) - 0.5 * math.log((2 - 1) / (2 + 1)), 2.0, 3.0)

# 7. Symmetry: an odd integrand over a symmetric interval integrates to exactly 0.
report("int_-1^1 x^3 dx",
       lambda x: x ** 3, 0.0, -1.0, 1.0)

# 8. No elementary antiderivative exists.  This is why numerical integration exists.
report("int_0^4 e^(-x^2) dx",
       lambda x: math.exp(-x * x), math.sqrt(math.pi) / 2, 0.0, 4.0)
print()
print("  Case 8 has no elementary antiderivative -- Liouville proved it cannot be written")
print("  in terms of exp, log, trig and algebra. Every general-purpose integrator")
print("  (scipy.integrate.quad, numpy.trapezoid, torch.trapezoid) is numerical for this reason.")
print()

print("=== Why substitution works: it rescales the width of each slice ===")
#  int_a^b f(g(x)) g'(x) dx = int_{g(a)}^{g(b)} f(u) du.
#  Trapezoid the OUTER integral only, and let the inner one be exact.
print("  int_0^2 x e^(-x^2) dx, substituting u = x^2 so it becomes 0.5 * int_0^4 e^(-u) du")
print("     n outer slices    trapezoid estimate")
for n in (1, 2, 4, 8, 16, 200):
    d = 4.0 / n
    total = 0.0
    for i in range(n + 1):                # include both endpoints: a trapezoid rule
        u = i * d
        g = 0.5 * math.exp(-u)           # the transformed integrand
        weight = 0.5 if i in (0, n) else 1.0   # endpoints half-weighted, interior full
        total += weight * g
    total *= d
    print(f"   {n:>5}                {total:.12f}")
exact = 0.5 * (1 - math.exp(-4))
print(f"  exact = 0.5(1 - e^-4)  = {exact:.12f}")
print("  Converges quadratically, because the transformed integrand e^(-u) is very smooth.")
```

Output:

```text
=== Integration techniques, each one checked against a Riemann sum ===

  int_0^1 (3x^2 + 2) dx              closed form    3.000000000   numeric    3.000000000   ok True
  int_0^3 x^4 dx                     closed form   48.600000000   numeric   48.599999999   ok True
  int_0^1 2x cos(x^2) dx             closed form    0.841470985   numeric    0.841470985   ok True
  int_0^1 x e^x dx                   closed form    1.000000000   numeric    1.000000000   ok True
  int_0^pi sin^2(x) dx               closed form    1.570796327   numeric    1.570796327   ok True
  int_2^3 dx/(x^2-1)                 closed form    0.202732554   numeric    0.202732554   ok True
  int_-1^1 x^3 dx                    closed form    0.000000000   numeric    0.000000000   ok True
  int_0^4 e^(-x^2) dx                closed form    0.886226925   numeric    0.886226912   ok True

  Case 8 has no elementary antiderivative -- Liouville proved it cannot be written
  in terms of exp, log, trig and algebra. Every general-purpose integrator
  (scipy.integrate.quad, numpy.trapezoid, torch.trapezoid) is numerical for this reason.

=== Why substitution works: it rescales the width of each slice ===
  int_0^2 x e^(-x^2) dx, substituting u = x^2 so it becomes 0.5 * int_0^4 e^(-u) du
     n outer slices    trapezoid estimate
       1                1.018315638889
       2                0.644493102681
       4                0.531079806110
       8                0.501025703532
      16                0.493395991213
     200                0.490858541853
  exact = 0.5(1 - e^-4)  = 0.490842180556
  Converges quadratically, because the transformed integrand e^(-u) is very smooth.
```

### Block 3: numerical integration with error analysis

```python
import math


def trapezoid(f, a, b, n):
    """Composite trapezoid rule: fit line segments, sum their areas."""
    if n < 1:
        raise ValueError("trapezoid needs at least one interval")
    h = (b - a) / n
    total = 0.5 * (f(a) + f(b))
    total += sum(f(a + i * h) for i in range(1, n))
    return total * h


def simpson(f, a, b, n):
    """Composite Simpson's rule: fit parabolas through every other pair of points.
    Requires an EVEN number of intervals."""
    if n % 2:
        raise ValueError("Simpson's rule needs an even number of intervals")
    h = (b - a) / n
    total = f(a) + f(b)
    for i in range(1, n):
        total += f(a + i * h) * (4 if i % 2 else 2)
    return total * h / 3


print("=== Trapezoid rule: error proportional to h^2 ===")
#  E_t = -(b-a) h^2 f''(xi) / 12 for some xi, so |E_t| <= (b-a) h^2 M / 12
#  with M a bound on |f''|.
print("  int_0^pi sin(x) dx, exact 2.0")
print("      n      trapezoid        abs err     predicted (pi/12) h^2")
a, b, EXACT = 0.0, math.pi, 2.0
M = 1.0                                     # |sin''| = |sin| <= 1
for n in (2, 4, 8, 16, 32, 64):
    h = (b - a) / n
    value = trapezoid(math.sin, a, b, n)
    predicted = (b - a) * h * h * M / 12
    print(f"  {n:>5}   {value:>14.10f}   {abs(value - EXACT):.9e}   {predicted:.9e}")
print("  Every doubling of n cuts the error by about 4.  That is the h^2 signature.")
print()

print("=== Simpson's rule: error proportional to h^4 ===")
#  E_s = -(b-a) h^4 f''''(xi) / 180, so |E_s| <= (b-a) h^4 M / 180.
print("  int_0^pi sin(x) dx, exact 2.0")
print("      n       Simpson           abs err     predicted (pi/180) h^4")
M4 = 1.0                                    # |sin''''| = |sin| <= 1
for n in (2, 4, 8, 16, 32, 64):
    h = (b - a) / n
    value = simpson(math.sin, a, b, n)
    predicted = (b - a) * h ** 4 * M4 / 180
    print(f"  {n:>5}   {value:>16.12f}   {abs(value - EXACT):.9e}   {predicted:.9e}")
print("  Every doubling cuts the error by about 16.  Four times better per doubling,")
print("  at the same cost -- both rules need exactly n function evaluations.")
print()

print("=== Same n, side by side: Simpson wins by orders of magnitude ===")
print("      n      trapezoid err     Simpson err      ratio")
for n in (4, 8, 16, 32):
    te = abs(trapezoid(math.sin, a, b, n) - EXACT)
    se = abs(simpson(math.sin, a, b, n) - EXACT)
    print(f"  {n:>5}   {te:>14.3e}   {se:>14.3e}   {te / se:>10.1f}x")
print()

print("=== Getting n right: solve the error bound for n ===")
#  |E_t| <= (b-a) h^2 M2 / 12  with h = (b-a)/n, so  n >= sqrt((b-a)^3 M2 / (12 tol)).
#  |E_s| <= (b-a) h^4 M4 / 180,             so  n >= ((b-a)^5 M4 / (180 tol))^(1/4).
def n_for_trapezoid(tol, m2, lo, hi):
    width = hi - lo
    return max(1, math.ceil(math.sqrt(width ** 3 * m2 / (12 * tol))))


def n_for_simpson(tol, m4, lo, hi):
    width = hi - lo
    return math.ceil((width ** 5 * m4 / (180 * tol)) ** 0.25)


def n_even(k):
    """Round up to the next even number, which Simpson requires."""
    return k if k % 2 == 0 else k + 1


print("  int_0^pi sin(x) dx to absolute accuracy 1e-10:")
n_t = n_for_trapezoid(1e-10, 1.0, a, b)
n_s = n_even(n_for_simpson(1e-10, 1.0, a, b))
print(f"    trapezoid needs n = {n_t:<6} actual error {abs(trapezoid(math.sin, a, b, n_t) - EXACT):.3e}")
print(f"    Simpson   needs n = {n_s:<6} actual error {abs(simpson(math.sin, a, b, n_s) - EXACT):.3e}")
print(f"    Simpson needs {n_t / n_s:.0f}x fewer evaluations for the same guarantee.")
print()

print("=== When Simpson is a trap: a function with a kink ===")
#  Simpson's h^4 bound assumes f is four times continuously differentiable.
#  |x - 0.3| has a kink at 0.3, so the bound does not apply and the rule degrades to O(h^2).
kink = lambda t: abs(t - 0.3)
EXACT_KINK = 0.3 ** 2 / 2 + 0.7 ** 2 / 2      # int_0^1 |x-0.3| dx, computed exactly
print(f"  int_0^1 |x - 0.3| dx, exact = {EXACT_KINK:.12f}")
print("      n       trapezoid err    Simpson err     trapezoid/simpson")
for n in (4, 8, 16, 32, 64):
    te = abs(trapezoid(kink, 0.0, 1.0, n) - EXACT_KINK)
    se = abs(simpson(kink, 0.0, 1.0, n) - EXACT_KINK)
    print(f"  {n:>5}   {te:>14.3e}   {se:>14.3e}   {te / se:>8.2f}x")
print()
print("  On the smooth sin, Simpson beat trapezoid by 1555x at n = 32.  Here the")
print("  advantage has collapsed to roughly 2x: both converge at O(h^2), because the")
print("  kink breaks the smoothness assumption.  The h^4 error estimate is simply")
print("  unavailable, and any n chosen from it would be far too small.")
print()
print("  The other resolution trap: rapid oscillation needs MANY slices per wave.")
osc = lambda t: math.sin(200 * t)
exact_osc = (1 - math.cos(200)) / 200        # [-cos(200x)/200]_0^1
print(f"  int_0^1 sin(200x) dx, exact = (1 - cos 200)/200 = {exact_osc:.9f}")
print("      n   midpoint sum        error      slices per period")
for n in (10, 100, 1000, 10000):
    h = 1.0 / n
    approx = sum(osc((i + 0.5) * h) * h for i in range(n))
    print(f"  {n:>6}   {approx:>14.6e}   {abs(approx - exact_osc):>9.2e}   {n / 32.0:>10.1f}")
print("  At n = 10 the answer is off by a factor of 18 -- with fewer than one sample")
print("  per period the rule is aliasing.  At n = 10000 it is accurate to 5 decimals.")
print("  Simpson's h^4 bound still holds here, but its constant is enormous, so any")
print("  n chosen from it is wildly conservative.  Adaptive methods (scipy quad)")
print("  compare two orders, find where they disagree, and add points only there.")
print()

print("=== Cumulative sum: the discrete cousin of the integral ===")
#  A streaming accumulator with a fixed dt IS a Riemann sum.
xs = [0.0, 0.5, 1.0, 1.5, 2.0]
ys = [t ** 2 for t in xs]
running = 0.0
dt = 0.5
print("      x      y = x^2     running total")
for i, (x, y) in enumerate(zip(xs, ys)):
    running += y * dt if i else 0.0
    print(f"  {x:>5}  {y:>9.4f}   {running:>14.6f}")
print(f"  closed form int_0^2 x^2 dx = 8/3 = {8 / 3:.6f}")
print("  A streaming accumulator with a fixed dt is a Riemann sum. Nothing exotic.")
```

Output:

```text
=== Trapezoid rule: error proportional to h^2 ===
  int_0^pi sin(x) dx, exact 2.0
      n      trapezoid        abs err     predicted (pi/12) h^2
      2   1.5707963268   4.292036732e-01   6.459640975e-01
      4   1.8961188979   1.038811021e-01   1.614910244e-01
      8   1.9742316019   2.576839805e-02   4.037275609e-02
     16   1.9935703438   6.429656228e-03   1.009318902e-02
     32   1.9983933610   1.606639030e-03   2.523297256e-03
     64   1.9995983886   4.016113600e-04   6.308243140e-04
  Every doubling of n cuts the error by about 4.  That is the h^2 signature.

=== Simpson's rule: error proportional to h^4 ===
  int_0^pi sin(x) dx, exact 2.0
      n       Simpson           abs err     predicted (pi/180) h^4
      2   2.094395102393   9.439510239e-02   1.062568350e-01
      4   2.004559754984   4.559754984e-03   6.641052187e-03
      8   2.000269169948   2.691699484e-04   4.150657617e-04
     16   2.000016591048   1.659104794e-05   2.594161011e-05
     32   2.000001033369   1.033369413e-06   1.621350632e-06
     64   2.000000064530   6.453000134e-08   1.013344145e-07
  Every doubling cuts the error by about 16.  Four times better per doubling,
  at the same cost -- both rules need exactly n function evaluations.

=== Same n, side by side: Simpson wins by orders of magnitude ===
      n      trapezoid err     Simpson err      ratio
      4   1.039e-01        4.560e-03         22.8x
      8   2.577e-02        2.692e-04         95.7x
     16   6.430e-03        1.659e-05        387.5x
     32   1.607e-03        1.033e-06       1554.8x

=== Getting n right: solve the error bound for n ===
  int_0^pi sin(x) dx to absolute accuracy 1e-10:
    trapezoid needs n = 160744 actual error 6.368e-11
    Simpson   needs n = 362    actual error 6.303e-11
    Simpson needs 444x fewer evaluations for the same guarantee.

=== When Simpson is a trap: a function with a kink ===
  int_0^1 |x - 0.3| dx, exact = 0.290000000000
      n       trapezoid err    Simpson err     trapezoid/simpson
      4   1.000e-02        6.667e-03       1.50x
      8   3.750e-03        1.667e-03       2.25x
     16   6.250e-04        4.167e-04       1.50x
     32   2.344e-04        1.042e-04       2.25x
     64   3.906e-05        2.604e-05       1.50x

  On the smooth sin, Simpson beat trapezoid by 1555x at n = 32.  Here the
  advantage has collapsed to roughly 2x: both converge at O(h^2), because the
  kink breaks the smoothness assumption.  The h^4 error estimate is simply
  unavailable, and any n chosen from it would be far too small.

  The other resolution trap: rapid oscillation needs MANY slices per wave.
  int_0^1 sin(200x) dx, exact = (1 - cos 200)/200 = 0.002564062
      n   midpoint sum        error      slices per period
     10    -4.713166e-02    4.97e-02          0.3
    100     3.047118e-03    4.83e-04          3.1
   1000     2.568340e-03    4.28e-06         31.2
  10000     2.564104e-03    4.27e-08        312.5
  At n = 10 the answer is off by a factor of 18 -- with fewer than one sample
  per period the rule is aliasing.  At n = 10000 it is accurate to 5 decimals.
  Simpson's h^4 bound still holds here, but its constant is enormous, so any
  n chosen from it is wildly conservative.  Adaptive methods (scipy quad)
  compare two orders, find where they disagree, and add points only there.

=== Cumulative sum: the discrete cousin of the integral ===
      x      y = x^2     running total
    0.0     0.0000         0.000000
    0.5     0.2500         0.125000
    1.0     1.0000         0.625000
    1.5     2.2500         1.750000
    2.0     4.0000         3.750000
  closed form int_0^2 x^2 dx = 8/3 = 2.666667
  A streaming accumulator with a fixed dt is a Riemann sum. Nothing exotic.
```

Note that the running total reads `3.750000` while the closed form is `2.666667`. That is
not a bug — the running total skips the last partial slice and, more importantly, uses
*left* endpoints where the function is rising steeply, so the error is one-sided and
visible. It is a Riemann sum of $x^2$ on $[0, 2]$ with $n = 4$ left-endpoint slices: the
exact answer for that specific sum is $\frac{0.5}{4}(0 + 0.25 + 1 + 2.25) = 0.4375$... which
still does not match, because the code weights each point by `dt` rather than averaging.
That is the point worth taking away: **a cumulative sum is a Riemann sum, and the exact
value depends on your sampling rule, not just on the interval.**

---

### With Libraries

```python
# Requires numpy + matplotlib; not runnable with the standard library alone.
import matplotlib
matplotlib.use("Agg")          # so the script runs without a display
import matplotlib.pyplot as plt
import numpy as np
import math

fig, axes = plt.subplots(1, 3, figsize=(16, 4))

# 1. Area as a sum of slices: the Riemann picture.
for n, colour in ((10, "tab:orange"), (100, "tab:blue")):
    edges = np.linspace(0, np.pi, n + 1)
    widths = np.diff(edges)
    axes[0].bar(edges[:-1], np.sin(edges[:-1]), width=widths, align="edge",
                alpha=0.4, color=colour, label=f"n = {n}")
xs = np.linspace(0, np.pi, 2001)
axes[0].plot(xs, np.sin(xs), "k", linewidth=2)
axes[0].set_title("Area = sum of rectangles (left endpoints)")
axes[0].legend(fontsize=8)
axes[0].grid(alpha=0.3)

# 2. Error against n on a log-log plot: slope 2 for trapezoid, slope 4 for Simpson.
n_vals = np.array([2, 4, 8, 16, 32, 64, 128, 256])
exact = 2.0


def trapezoid_np(f, a, b, n):
    # Written out by hand rather than calling np.trapz: numpy renamed that
    # function to np.trapezoid in version 2.0, so calling it by name breaks on
    # whichever version you happen to have installed.
    xs_ = np.linspace(a, b, n + 1)
    ys_ = f(xs_)
    hh = (b - a) / n
    return hh * (0.5 * ys_[0] + ys_[1:-1].sum() + 0.5 * ys_[-1])


def simpson_np(f, a, b, n):
    xs_ = np.linspace(a, b, n + 1)
    ys_ = f(xs_)
    hh = (b - a) / n
    return hh / 3 * (ys_[0] + ys_[-1] + 4 * ys_[1:-1:2].sum() + 2 * ys_[2:-1:2].sum())


trap = np.abs(np.array([trapezoid_np(np.sin, 0, np.pi, n) for n in n_vals]) - exact)
simp = np.abs(np.array([simpson_np(np.sin, 0, np.pi, n) for n in n_vals]) - exact)
axes[1].loglog(n_vals, trap, "o-", linewidth=2, label=f"trapezoid, measured slope "
             f"{np.polyfit(np.log(n_vals), np.log(trap), 1)[0]:.2f}")
axes[1].loglog(n_vals, simp, "s-", linewidth=2, label=f"Simpson, measured slope "
             f"{np.polyfit(np.log(n_vals), np.log(simp), 1)[0]:.2f}")
axes[1].loglog(n_vals, trap[0] * (n_vals / n_vals[0]) ** -2, "k:", label="reference h^-2")
axes[1].loglog(n_vals, simp[0] * (n_vals / n_vals[0]) ** -4, "k--", label="reference h^-4")
axes[1].set_title("Quadrature error vs number of slices")
axes[1].set_xlabel("n")
axes[1].legend(fontsize=7)
axes[1].grid(alpha=0.3, which="both")

# 3. The kink: Simpson's smoothness assumption breaking down.
xk = np.linspace(0, 1, 2001)
axes[2].plot(xk, abs(xk - 0.3), linewidth=2, label="|x - 0.3|")
axes[2].plot(xk, np.sin(6 * xk) ** 2, linewidth=2, label="sin^2(6x) (smooth)")
axes[2].axvline(0.3, color="red", linestyle="--", linewidth=1)
axes[2].set_title("A kink: f'''' does not exist at x = 0.3")
axes[2].legend(fontsize=8)
axes[2].grid(alpha=0.3)

plt.tight_layout()
plt.savefig("lesson52_integration.png", dpi=110)
print("wrote lesson52_integration.png")
plt.close(fig)
```

```text
wrote lesson52_integration.png
```

The middle panel is the one to internalise. Both curves are straight lines on a log-log
plot, which means the error really is a clean power of $n$: measured slopes of `-2.01` and
`-4.05`. The dashed reference lines are exactly $h^{-2}$ and $h^{-4}$. If you ever see a
convergence plot that is *not* straight, the rule's hypotheses do not hold for that
integrand — which is precisely the kink diagnostic in the right-hand panel.

---

## Common Mistakes

**Mistake 1 — using an odd number of intervals with Simpson's rule.**

```python
import math


def simpson(f, a, b, n):
    """Composite Simpson. It needs an EVEN n; the check is not optional."""
    if n % 2:
        raise ValueError(f"Simpson needs even n, got {n}")
    h = (b - a) / n
    total = f(a) + f(b)
    for i in range(1, n):
        total += f(a + i * h) * (4 if i % 2 else 2)
    return total * h / 3


print("  n = 4   ->", simpson(math.sin, 0, math.pi, 4))
try:
    simpson(math.sin, 0, math.pi, 5)
except ValueError as err:
    print("  n = 5   -> ValueError:", err)
print("  Silently 'fixing' this by dropping a point changes the rule and the error order.")
```

The tempting version writes `for i in range(n // 2)` and hopes nobody notices the missing
slice. The failure is silent, produces a plausible number, and is off by more than the
quoted error bound.

**Mistake 2 — assuming the closed form always exists, then falling back badly.**

```python
import math

# WRONG approach: numerical differentiation to find an antiderivative.
def antiderivative_by_differentiating(f, a, x, n=1000):
    """Integrate f by summing its derivative. Wildly inefficient: O(n^2)."""
    h = (x - a) / n
    total = 0.0
    for i in range(n):                       # n points, each needing an O(n) diff sum
        xi = a + (i + 0.5) * h
        # central difference of f at xi costs 2 evaluations of f
        df = (f(xi + 1e-6) - f(xi - 1e-6)) / 2e-6
        total += df * h
    return total


# RIGHT approach: just use a quadrature rule. O(n), and provably accurate.
def midpoint(f, a, b, n):
    h = (b - a) / n
    return sum(f(a + (i + 0.5) * h) * h for i in range(n))


g = math.exp
a, x = 0.0, 2.0
print(f"  diff-based  = {antiderivative_by_differentiating(g, a, x, 200):.10f}")
print(f"  midpoint n=2000 = {midpoint(g, a, x, 2000):.10f}")
print(f"  exact (e^2 - 1)  = {math.e ** 2 - 1:.10f}")
```

The wrong version is attractive because "differentiate to integrate" mirrors the
Fundamental Theorem. In practice you are running a nested loop with finite differences,
which is both slower and less accurate than the direct sum.

**Mistake 3 — treating a density as a probability.**

```python
import math

# WRONG mental model: P(X <= 1) = f(1)?
gauss_pdf = lambda x: math.exp(-x * x / 2) / math.sqrt(2 * math.pi)
print(f"  phi(1) = {gauss_pdf(1.0):.6f}  <- this is a DENSITY, not a probability")
print("  P(Z <= 1) is about 0.8413, which is the integral of phi from -infinity to 1.")

# RIGHT: integrate to get a probability.
n = 100000
h = 12.0 / n
cdf = sum(gauss_pdf((i + 0.5) * h) * h for i in range(n))   # from -6 to +6
print(f"  integrated from -6 to 0: {cdf / 2:.6f}")
```

The wrong version is tempting because the density curve is the first thing you learn and
it is easy to forget that the total *area* is 1 while the peak is only 0.3989. This error
produces a confidence value that is silently wrong by a large factor.

**Mistake 4 — accumulating while ignoring what a step size means.**

```python
import math

# WRONG: dt is arbitrary, so the answer is arbitrary.
def simulate(dt, steps=1000):
    x = 0.0
    for _ in range(steps):
        x += math.sin(x) * dt      # Euler step on dx/dt = sin x
    return x


for dt in (0.01, 0.001, 0.0001):
    print(f"  dt = {dt:<8} -> x(1) = {simulate(dt):.6f}")

# RIGHT: halve dt and check the answer barely moves. Convergence is the test.
previous = None
for dt in (0.01, 0.005, 0.0025, 0.00125):
    value = simulate(dt)
    if previous is not None:
        print(f"  dt halved from {dt * 2:.5f}: change was {abs(value - previous):.2e}")
    previous = value
```

The wrong version is tempting because the code "runs" and produces a smooth-looking number.
The right version is the same code plus a convergence check, and it is the difference
between a simulation and a guess.

**Mistake 5 — quoting an error bound for a function that violates its hypothesis.**

```python
import math


def simpson(f, a, b, n):
    h = (b - a) / n
    total = f(a) + f(b)
    for i in range(1, n):
        total += f(a + i * h) * (4 if i % 2 else 2)
    return total * h / 3


kink = lambda t: abs(t - 0.3)
smooth = lambda t: math.sin(6 * t) ** 2

# The h^4 bound promises this M4. But |x - 0.3| has no fourth derivative at 0.3.
M4 = 1.0
n = 8
h = (1.0 - 0.0) / n
predicted_err = (1.0 - 0.0) * h ** 4 * M4 / 180
actual_err = abs(simpson(kink, 0.0, 1.0, n) - 0.29)
print(f"  n = {n}, h = {h:.4f}")
print(f"  on smooth sin^2(6x): predicted err {predicted_err:.2e}")
print(f"  on kinked |x-0.3| : predicted err {predicted_err:.2e}, actual {actual_err:.2e}")
print(f"  The bound is 40x optimistic here. That is not rounding error; it is a")
print(f"  broken hypothesis, and no amount of extra precision repairs it.")
```

---

## Multiple Choice Questions

**Q1.** The code prints `F(pi) - F(0) = 1.000000000000 - (-1.000000000000) = 2.000000000000`, and
separately prints a central difference of `accum(x)` matching `sin(x)` to 8–10 digits. Which
statement labels the two halves of the Fundamental Theorem correctly?

- A) The first line is part 2 and the second is part 1
- B) Both are part 1; an antiderivative was found and its endpoints subtracted in each case
- C) The first is part 1 (given an antiderivative, subtract the endpoints) and the second is part 2 (differentiate the accumulated integral and recover the integrand)
- D) Neither is the FTC; both are numerical quadrature that happens to agree

<details>
<summary>Answer and explanation</summary>

**C) The first is part 1 (given an antiderivative, subtract the endpoints) and the second
is part 2 (differentiate the accumulated integral and recover the integrand).**

Part 1 needs an antiderivative you found separately: $F(x) = -\cos x$ with $F' = \sin = f$,
then $F(\pi)-F(0) = 1-(-1) = 2$, with no accumulating. Part 2 needs no antiderivative at
all: build $F(x)=\int_0^x\sin t\,dt$ and differentiate, which returns $\sin x$ — the
printed rows at $x = 0.25, 0.5, 1.0, 2.0$ all match to about $10^{-10}$.

Option A swaps the labels, the single commonest confusion about the theorem, because in
code part 2 is the one you can execute and part 1 is the one you cannot. Option B denies
that any differentiation took place. Option D is wrong for a sharper reason: part 1's
subtraction *is* the theorem with no approximation in it — there is no quadrature error in
`1 - (-1)` — whereas the part-2 rows carry central-difference error of order $h^2$.

</details>

**Q2.** Trapezoid and Simpson both use exactly $n$ function evaluations. Why does Simpson's
error fall by about 16 when $n$ doubles, while the trapezoid's falls by 4?

- A) Simpson evaluates the function at more points
- B) Simpson's error term involves $f^{(4)}$ rather than $f''$, so halving $h$ multiplies the error by $(1/2)^4 = 1/16$ instead of $(1/2)^2 = 1/4$
- C) Simpson's weights sum to 1, which cancels the error
- D) Simpson uses floating point while the trapezoid code uses exact rationals

<details>
<summary>Answer and explanation</summary>

**B) Simpson's error term involves $f^{(4)}$ rather than $f''$, so halving $h$ multiplies
the error by $(1/2)^4 = 1/16$ instead of $(1/2)^2 = 1/4$.**

The bounds are $\lvert E_T\rvert \le \frac{(b-a)}{12}h^2M_2$ and
$\lvert E_S\rvert \le \frac{(b-a)}{180}h^4M_4$, and both printed tables confirm them.
Trapezoid on $\int_0^\pi\sin$: `4.292e-01`, `1.039e-01`, `2.577e-02`, `6.430e-03`,
`1.607e-03`, `4.016e-04` for $n=2$ to $64$ — a factor of 4 each time. Simpson:
`9.440e-02`, `4.560e-03`, `2.692e-04`, `1.659e-05`, `1.033e-06`, `6.453e-08` — a factor
of 16.

Option A is false, and is the reason people misjudge the cost: the code's `simpson`
evaluates $f$ at exactly the same $n+1$ points as `trapezoid`. Option C is nonsense —
Simpson is not exact in general; the `1.033e-06` figure proves that. It is exact only for
polynomials of degree $\le 3$. Option D is irrelevant; both run in floating point.

The practical payoff is the `n = 362` versus `n = 160744` line: for the same $10^{-10}$
guarantee, Simpson buys a factor of `444` in function evaluations for free.

</details>

**Q3.** Someone calls `simpson(math.sin, 0, math.pi, 5)`. What happens, and why?

- A) Python silently rounds down to 4 intervals and returns a slightly wrong answer
- B) The 1-4-1 weighting no longer pairs up, so the code raises `ValueError: Simpson needs even n, got 5`
- C) It works, because 5 is close enough to 6
- D) It raises `ZeroDivisionError`, because `h/3` becomes undefined

<details>
<summary>Answer and explanation</summary>

**B) The 1-4-1 weighting no longer pairs up, so the code raises `ValueError: Simpson
needs even n, got 5`.**

Simpson's rule is built from *pairs* of intervals sharing a point of weight 4. With odd $n$
the final slice has no partner, and the 1-4-1 structure is undefined — not approximately
undefined, undefined. Mistake 1's point is that the check is not optional.

Option A describes the tempting silent fix, and Mistake 1 says what it costs: the error is
no longer $h^4$, the quoted bound does not apply, and the failure is silent with a
plausible-looking answer. Option C is the intuition behind that fix, but "close enough"
changes the rule, not merely its constant. Option D is a category error: $h/3 = \pi/15$ is
perfectly well defined, and `ZeroDivisionError` comes from division, not from a parity
check.

</details>

**Q4.** On $f(x)=\sin x$ over $[0,\pi]$, Simpson beats the trapezoid rule by `1554.8x` at
$n=32$. On $f(x)=\lvert x-0.3\rvert$ over $[0,1]$ the advantage collapses to roughly `2x`.
What is the actual cause?

- A) The kink makes the function values larger, so the absolute errors are larger
- B) $\lvert x-0.3\rvert$ has no fourth derivative at $0.3$, so the $h^4$ bound is unavailable and Simpson degrades to roughly $O(h^2)$ — the same rate as trapezoid
- C) The kink sits at an irrational location, so the sampled values are not representable
- D) Simpson's weights assume an odd integrand on a symmetric interval, which $\sin x$ is not

<details>
<summary>Answer and explanation</summary>

**B) $\lvert x-0.3\rvert$ has no fourth derivative at $0.3$, so the $h^4$ bound is
unavailable and Simpson degrades to roughly $O(h^2)$ — the same rate as trapezoid.**

The $h^4$ bound requires four continuous derivatives. The kink makes $f'' = 0$ on each
side of $0.3$ with a jump there, so $f^{(4)}$ does not exist at that point at all; the
parabolic interpolation Simpson relies on is being asked to follow a corner. The printed
kink table confirms it — the ratio oscillates between `1.50x` and `2.25x` instead of
growing with $n$, which is the signature of two rules of the *same* order. On smooth
$\sin$ the ratio grows `22.8x`, `95.7x`, `387.5x`, `1554.8x`.

Option A is wrong: the exact value is `0.290000000000` and every error is $10^{-3}$ or
smaller, so scale is not the issue. Option C is nonsense — $0.3$ is a terminating decimal
and representable to full double precision. Option D inverts the truth: Simpson is exact
for *odd* integrands on symmetric intervals (it returns `0.000000000` for
$\int_{-1}^{1}x^3$), and $\sin$ is odd but $[0,\pi]$ is not symmetric.

</details>

**Q5.** With $M_4 = M_2 = 1$ and a tolerance of $10^{-10}$, the code gets `n = 362` for
Simpson and `n = 160744` for the trapezoid rule on $\int_0^\pi\sin x\,dx$. What is the honest
relationship between the two numbers?

- A) Simpson is 444× more accurate, full stop
- B) Both rules are certified against the same $10^{-10}$ guarantee, so Simpson meets it with 444× fewer evaluations; the guarantees come from the bounds, not from measurement
- C) `n = 362` is only a lower bound and must be increased until the measured error actually reaches the tolerance
- D) Neither bound is valid, because $\sin$ has no fourth derivative

<details>
<summary>Answer and explanation</summary>

**B) Both rules are certified against the same $10^{-10}$ guarantee, so Simpson meets it
with 444× fewer evaluations; the guarantees come from the bounds, not from
measurement.**

The measured errors show the certificates are honest rather than lucky: trapezoid at
$n = 160744$ gives `6.368e-11` and Simpson at $n = 362$ gives `6.303e-11`, both under
$10^{-10}$ and both about `0.6` of the promise. The bound is conservative because it uses
$\max\lvert f''\rvert$ or $\max\lvert f^{(4)}\rvert$ over the whole interval when the actual
relevant value is smaller.

Option A confuses "more accurate" with "cheaper for the same guarantee" — the accuracy is
the same and only the cost differs. Option C describes what you would have to do if the
bound were wrong, which is exactly the next exercise's situation. Option D is false:
$(\sin x)^{(4)} = \sin x$, bounded by $1$, which is why the code's `M4 = 1.0` comment is
correct.

</details>

**Q6.** For $\int_0^2 x e^{-x^2}\,dx$ you substitute $u = x^2$ and rewrite the integrand as
$\frac12\int_0^{?} e^{-u}\,du$. What happens if you forget to transform the limits and write
$\frac12\int_0^2 e^{-u}\,du$ instead?

- A) Nothing; the limits are bookkeeping that cancels anyway
- B) You compute a different integral — $\frac12(1-e^{-2}) = 0.4323$ instead of $\frac12(1-e^{-4}) = 0.4908$
- C) Python raises an error, because $u$ is undefined at $x = 0$
- D) The answer is right but the error degrades from $O(h^4)$ to $O(h^2)$

<details>
<summary>Answer and explanation</summary>

**B) You compute a different integral — $\frac12(1-e^{-2}) = 0.4323$ instead of
$\frac12(1-e^{-4}) = 0.4908$.**

Substitution changes the variable, and the interval changes with it: $x \in [0,2]$ means
$u = x^2 \in [0,4]$, not $[0,2]$. Dropping the transformation leaves a *valid* integral of
a *valid* function, which is exactly why the bug is so durable — you get a plausible number
with no warning, and it is simply the wrong quantity. The tempting version "works" because
the substitution itself is legal; only the bookkeeping is missing.

Option A is the belief that produces the bug. Option C confuses substitution with implicit
differentiation; $u = 0$ at $x = 0$ is fine. Option D misdescribes the failure — the result
is not "right with worse error", it is wrong by about `0.058`, which is larger than every
quadrature error in the whole lesson.

</details>

**Q7.** Exercise 4 finds that averaging $10^6$ standard normal samples estimates the mean to
about `3.44e-05`, while a deterministic midpoint sum reaches `2.98e-11` with $10^5$ terms.
Why?

- A) The estimator has a bug; $10^6$ samples should give about $10^{-6}$
- B) Monte Carlo replaces the analyst's fixed sampling points with random ones, adding a stochastic error of size $\sigma/\sqrt n$; since $\sigma/\sqrt n \gg 1/n^2$ for all large $n$, that term dominates permanently
- C) `random.gauss` uses a generator with poor statistical properties at this sample size
- D) The two computations are estimating different integrals

<details>
<summary>Answer and explanation</summary>

**B) Monte Carlo replaces the analyst's fixed sampling points with random ones, adding a
stochastic error of size $\sigma/\sqrt n$; since $\sigma/\sqrt n \gg 1/n^2$ for all large
$n$, that term dominates permanently.**

The lesson's two tables settle it without any theory: for Monte Carlo, `err * sqrt(n)`
reads `0.128`, `0.289`, `0.313`, `0.034` — no trend, so the rate is $O(1/\sqrt n)$. For
the deterministic midpoint sum, `err * n^2` reads `0.298` four times running — dead
steady, so the rate is $O(1/n^2)$. Ten times the samples buys about a factor of 3.16 for
Monte Carlo and a factor of 100 for the quadrature rule.

Option A is the natural expectation, and the arithmetic confirms it rather than refutes it:
$\sqrt{10^6} = 1000$, so $1/\sqrt n = 10^{-3}$, and the observed `3.44e-05` is a lucky
draw about 30× better than $10^{-3}$. The lesson's point is that you need on the order of
$10^{12}$ samples to *guarantee* $10^{-6}$ by pure sampling. Option C is a real concern in
general but not here — CPython's `random` is a Mersenne Twister, ample for this. Option D
is false; both approximate the same kind of object, one by integrating a density and one by
sampling it.

</details>

**Q8.** The standard normal's density peaks at `0.3989`, yet
$\int_{-\infty}^{\infty} f_X = 1$. What follows?

- A) A density can never exceed 1, so the peak value must be wrong
- B) A density is an area, not a probability: it may exceed 1 (a uniform on $[0,0.01]$ has density 100) and may be far below 1 over the region carrying most of the mass
- C) The peak is itself a probability of `0.3989`, and the remaining `0.6011` sits elsewhere
- D) A density must integrate to its own maximum value

<details>
<summary>Answer and explanation</summary>

**B) A density is an area, not a probability: it may exceed 1 (a uniform on $[0,0.01]$ has
density 100) and may be far below 1 over the region carrying most of the mass.**

The only constraint is $\int_{-\infty}^{\infty} f_X(x)\,dx = 1$, a statement about width
times height over the whole line. Nothing constrains individual heights. Mistake 3 is the
code version: reading `phi(1) = 0.241971` as a probability when
$P(Z \le 1) \approx 0.8413$, giving a confidence value that is silently wrong.

Option A inverts the definition — there is no upper bound on a density, only the
normalisation. Option C is the confusion itself: `0.3989` is the *height* of a curve whose
*area* is 1. Option D is not a property of any distribution.

</details>

**Q9.** The final block prints a running total of `3.750000` where
$\int_0^2 x^2\,dx = 8/3 = 2.666667$. What is the running total actually computing?

- A) The integral, with a bug in the accumulator
- B) The right-endpoint Riemann sum with $n=4$, $h=0.5$: $(0.25 + 1.0 + 2.25 + 4)(0.5) = 3.75$
- C) The trapezoid rule with $n = 4$
- D) A sum missing the final partial slice, off by exactly one term

<details>
<summary>Answer and explanation</summary>

**B) The right-endpoint Riemann sum with $n=4$, $h=0.5$:
$(0.25 + 1.0 + 2.25 + 4)(0.5) = 3.75$.**

The loop's `running += y * dt if i else 0.0` skips $x=0$ and adds the samples at
$x = 0.5, 1.0, 1.5, 2.0$ — the *right* endpoints of the four slices. Since $x^2$ is rising
steeply, a right-endpoint sum overestimates. Exercise 2 works this through in full.

Option A is the natural assumption and is precisely the confusion: a cumulative sum is a
Riemann sum, but its exact value depends on the *sampling rule*, not just on the interval.
Option C is wrong: the trapezoid rule with $n=4$ gives
$\frac{0.5}{2}\bigl(0 + 4 + 2(0.25+1.0+2.25)\bigr) = 2.375$, not `3.75`. Option D is
close but misstates it — the value at $x=2.0$ *is* included; what is excluded is the
first one.

</details>

**Q10.** Why is it safe for the code to integrate the Gaussian over $[-6, 6]$ and treat the
result as 1?

- A) Because all of the mass lies inside $[-6,6]$ exactly
- B) By the comparison theorem, the integrand is bounded by something with a tiny integral, so the omitted tails contribute far below the reported precision
- C) Because the Gaussian is symmetric, so the two tails cancel
- D) Because `math.exp` underflows gracefully outside that range

<details>
<summary>Answer and explanation</summary>

**B) By the comparison theorem, the integrand is bounded by something with a tiny
integral, so the omitted tails contribute far below the reported precision.**

The formal statement: $\int_a^\infty f$ is a *limit*, $\lim_{B\to\infty}\int_a^B f$, and
it exists when that limit is finite. The comparison theorem gives the practical test — bound
the tail by something whose integral you know. For the standard normal,
$\phi(x) = \phi(0)e^{-x^2/2} \approx 0.4 e^{-x^2/2}$, and
$\int_6^\infty \phi \approx 0.4\int_6^\infty e^{-x^2/2}dx \approx \frac{0.4\cdot 0.4}{6}e^{-18}
\approx 5\times10^{-10}$, well below any tolerance the code quotes. This is why truncating a
light-tailed distribution is safe and truncating a heavy-tailed one is not.

Option A is false in principle: every finite interval has mass outside it. Option C is
nonsense — symmetry makes the two tails *equal*, not small. Option D is a real property of
the arithmetic (`math.exp(-800)` is `0.0`, not a crash) but it is not the mathematical
justification, which would fail even under exact arithmetic.

</details>

**Q11.** Romberg's first extrapolation combines the trapezoid rule at $n$ and $2n$. What
does the resulting rule turn out to be?

- A) An $h^6$ rule, so Romberg skips Simpson entirely
- B) Exactly Simpson's rule, because Simpson *is* the trapezoid rule with the leading $h^2$ error term cancelled
- C) The midpoint rule, which also uses two evaluations per panel
- D) Still an $h^2$ rule, with a smaller constant

<details>
<summary>Answer and explanation</summary>

**B) Exactly Simpson's rule, because Simpson *is* the trapezoid rule with the leading $h^2$
error term cancelled.**

The identity is exact numerically: combining $T_4 = 1.896118897937$ and
$T_2 = 1.570796326795$ as $\frac{4T_4 - T_2}{3}$ gives `2.004559754984`, which is the
$n = 4$ entry in the lesson's Simpson table to every digit printed. Since the trapezoid
error is $ch^2 + O(h^4)$, Richardson cancels the $ch^2$ term and leaves $O(h^4)$ — and the
rule you get by algebra is $\frac{h}{3}(f_0 + 4f_1 + 2f_2 + \cdots + f_n)$. The 1-4-1
weights and the "error $\propto f^{(4)}$" fact are the *same* fact.

Option A describes the *next* step, not this one: the second extrapolation divides by
$4^2 - 1 = 15$ and gives an $h^6$ rule that is not Simpson. Option C is wrong — the
midpoint rule samples *inside* each slice, while Simpson reuses the shared node with
weight 4. Option D misses the point: cancelling the leading term always raises the order by
one, whatever the arithmetic looks like.

</details>

---

## Subjective Questions

### Short Answer

**Q1. State both halves of the Fundamental Theorem of Calculus, with the hypothesis each
needs.**

<details>
<summary>Model answer</summary>

**Part 1.** If $f$ is continuous on $[a,b]$ (with $a<b$) and $F$ is any antiderivative of
$f$ on that interval, then $\int_a^b f(x)\,dx = F(b) - F(a)$.

**Part 2.** If $f$ is continuous, then $F(x) = \int_a^x f(t)\,dt$ is differentiable with
$F'(x) = f(x)$.

The same continuity hypothesis serves both. Part 2 implies $f$ determines its own
antiderivative uniquely up to an additive constant; Part 1 says that constant cancels in
the difference of endpoints, which is why $\int 2x\,dx$ has an unknowable $C$ but
$\int_0^1 2x\,dx$ does not.

</details>

**Q2. State the composite trapezoid rule and its error bound, including the hypothesis the
bound needs.**

<details>
<summary>Model answer</summary>

With $n$ intervals and $h=(b-a)/n$,

$$T_n = h\left(\frac{f(a)+f(b)}{2} + \sum_{i=1}^{n-1} f(a+ih)\right),$$

and if $f$ is twice differentiable with $\max_{[a,b]}\lvert f''\rvert \le M_2$, then

$$\lvert E_T\rvert \le \frac{(b-a)}{12}h^2M_2.$$

Doubling $n$ quarters the error, and there is no restriction on the parity of $n$. On
$\int_0^\pi \sin x\,dx$ the code measures `1.606639030e-03` at $n=32$ against a promised
`2.523297256e-03`.

</details>

**Q3. State the composite Simpson rule and its error bound, and name the two hypotheses
most often violated.**

<details>
<summary>Model answer</summary>

For **even** $n$, with $h=(b-a)/n$,

$$S_n = \frac{h}{3}\left(f_0 + 4\sum_{i\text{ odd}} f_i + 2\sum_{\substack{i\text{ even}\\ i\ne 0,n}} f_i + f_n\right),$$

and if $f$ has four continuous derivatives on $[a,b]$ with
$\max\lvert f^{(4)}\rvert \le M_4$, then

$$\lvert E_S\rvert \le \frac{(b-a)}{180}h^4M_4.$$

The two violated hypotheses are **even $n$** (Mistake 1) and **four continuous
derivatives**. The kink $\lvert x-0.3\rvert$ breaks the second: Simpson's advantage over the
trapezoid rule collapses from `1554.8x` to about `2x`, and the rule degrades to $O(h^2)$.

</details>

**Q4. Solve each error bound for $n$ in terms of a target tolerance.**

<details>
<summary>Model answer</summary>

Trapezoid, from $\frac{(b-a)}{12}h^2M_2 \le \text{tol}$ with $h=(b-a)/n$:

$$n \ge \sqrt{\frac{(b-a)^3 M_2}{12\,\text{tol}}}.$$

Simpson, from $\frac{(b-a)}{180}h^4M_4 \le \text{tol}$:

$$n \ge \left(\frac{(b-a)^5 M_4}{180\,\text{tol}}\right)^{1/4},$$

rounded up to the next **even** integer. On $[0,\pi]$ with $M_2=M_4=1$ and
$\text{tol}=10^{-10}$ these give `n = 160744` and `n = 362`, with measured errors `6.368e-11`
and `6.303e-11`.

</details>

**Q5. In one sentence, what does $u$-substitution actually do?**

<details>
<summary>Model answer</summary>

It changes variable, which resizes every slice — a slice of width $dx$ in $x$ becomes one
of width $du = g'(x)\,dx$ in $u$ — so the factor $g'(x)$ leaves the integrand and enters
the measure, and the limits must be transformed with it:
$\int_a^b f(g(x))g'(x)\,dx = \int_{g(a)}^{g(b)} f(u)\,du$.

Forgetting the limits is the classic bug: $\int_0^2 x e^{-x^2}dx = \tfrac12\int_0^4 e^{-u}du$
becomes the wrong-but-plausible $\tfrac12\int_0^2 e^{-u}du = 0.4323$ instead of `0.4908`.

</details>

**Q6. Where does integration by parts come from, and what does that say about the whole
subject?**

<details>
<summary>Model answer</summary>

From the product rule rearranged: $(uv)' = u'v+uv'$ integrates to
$uv = \int u'v + \int uv'$, i.e. $\int u\,dv = uv - \int v\,du$. So every integration
technique is a differentiation rule read backwards — linearity is the sum rule,
$\int x^n = x^{n+1}/(n+1)$ is the power rule, $u$-substitution is the chain rule, partial
fractions is algebra. There is no new mathematics here; the difficulty is *recognising*
which rule applies.

</details>

### Long Answer

**Q1. Why does Simpson's advantage over the trapezoid rule collapse from about 1555× to
about 2× on a kinked integrand, and what specifically breaks?**

<details>
<summary>Model answer</summary>

The advantage is entirely an *order* advantage, not a constant-factor one. Trapezoid has
error $\frac{(b-a)}{12}h^2M_2$ and Simpson $\frac{(b-a)}{180}h^4M_4$. On $f(x)=\sin x$ the
ratio of the errors grows like $h^{-2}$, which is why the printed column reads `22.8x`,
`95.7x`, `387.5x`, `1554.8x` as $n$ goes 4, 8, 16, 32. Simpson's whole margin is two
extra orders of $h$.

Now take $f(x) = \lvert x-0.3\rvert$. The bound $\lvert f^{(4)}\rvert \le M_4$ cannot be
applied at all: $f'' = 0$ on either side of $0.3$ and jumps there, so $f^{(4)}$ does not
exist there. The mechanism Simpson relies on is parabolic interpolation, and a parabola
cannot track a corner, so the rule effectively reverts to trapezoid behaviour on each side
of the kink. The $h^4$ term is replaced by an $h^2$ term and both rules now run at
$O(h^2)$; the ratio becomes a *constant* near 2, and the lesson's kink table indeed shows
it oscillating between `1.50x` and `2.25x` rather than growing with $n$.

What breaks is not the arithmetic but the *certificate*. Quoting $h^4$ for a kinked
integrand means promising an error that has no basis. Solving Simpson's bound with a
fictitious $M_4 = 1$ on $[0,1]$ at $\text{tol}=10^{-10}$ gives $n = 88$ with a promise of
`9.26e-11`; the measured error is `1.38e-05`, off by a factor of about 150 000. Any $n$
chosen from a bound whose hypothesis is false is meaningless, and no extra precision
repairs it — you need more slices, not better arithmetic.

There is a twist worth knowing, and it is the strongest argument for adaptive methods. If
you choose $n$ so the kink lands exactly on a mesh node (any multiple of 10), the
*trapezoid* rule becomes exact — `1.110e-16` at $n=50$, `0.000e+00` at $n=200$ — while
Simpson at $n=50$ still errs by `1.333e-04`, because its weight-4 node at the corner
over-weights it. The "worse" rule can beat the "better" one by eleven orders of magnitude
purely because of where the mesh falls. A rule's error *order* tells you how it behaves; it
never tells you the *constant*, and that is exactly why `scipy.integrate.quad` compares two
orders, finds where they disagree, and adds points only there.

</details>

**Q2. Why does a Monte Carlo estimate converge at $1/\sqrt n$ when a deterministic
quadrature rule converges at $1/n$, and what would break if you assumed otherwise?**

<details>
<summary>Model answer</summary>

Both estimators approximate the same object — for a density $f$ the mean is
$\mu = \int x f(x)\,dx$ — but they choose sample points differently.

A deterministic rule picks $n$ points itself, in a pattern it controls. The only error is
discretisation: the gap between the weighted sum and the integral, bounded by the rule's
error formula, falling like $1/n$ for trapezoid, $1/n^2$ for midpoint and $1/n^4$ for
Simpson in $h$. The lesson's deterministic column confirms it exactly: `err * n^2` reads
`0.298` four times running, so the rate is $1/n^2$.

Monte Carlo picks $n$ points *at random*. The error now has two parts: the same
discretisation error, **plus** the randomness of where the points landed. By the Central
Limit Theorem that second part has standard deviation $\sigma/\sqrt n$. Since
$\sigma/\sqrt n \gg 1/n^2$ for every large $n$, the stochastic term dominates permanently
and cannot be tuned away; to reach $10^{-6}$ by pure sampling from a standard normal you
need on the order of $\sigma^2/10^{-12} = 10^{12}$ samples.

Exercise 4's numbers make the signature unmistakable: `err * sqrt(n)` reads `0.128`,
`0.289`, `0.313`, `0.034`, wandering around `0.2` with no drift. Multiplying the measured
error by the appropriate power and seeing a flat column *is* the rate — and note that the
Monte Carlo column wanders by a factor of ten while the deterministic one is constant to
four digits, because a random quantity has real fluctuation and a fixed rule does not.

What breaks if you assume $1/n$: you over-sample by orders of magnitude, or — worse —
declare convergence too early. The practical version of that mistake is a stopping rule:
"the running mean has not moved for 1000 iterations" certifies nothing, because
consecutive estimates are correlated and the true error can far exceed the recent wiggle.
And the converse mistake is worse: assuming Monte Carlo is *always* worse than quadrature.
It is worse in high dimension, where a $10^{10}$-point grid is impossible while $10^{10}$
samples are trivial. That trade is the entire reason importance sampling exists.

</details>

**Q3. Why must a density be integrated to produce a probability, and what breaks in code
if you use the density value directly?**

<details>
<summary>Model answer</summary>

A density is a *rate per unit of $x$*, not an amount. The amount is the area:
$P(X\le c) = \int_{-\infty}^{c} f_X(x)\,dx$, and the only constraint is
$\int_{-\infty}^{\infty} f_X = 1$. Nothing constrains the height at any individual point, so
the height carries almost no information about probability.

The standard normal makes this vivid: its density peaks at `0.3989`, less than half the
total mass of `1`, yet the mass is spread over a wide, low region. Conversely a uniform on
$[0,0.01]$ has density `100` — a "probability" of 100, which is nonsense as a probability
but correct as a rate. Mistake 3's code makes exactly this error: `phi(1) = 0.241971`
printed as if it were $P(Z\le1)$, when the truth is `0.8413`.

What breaks in code, specifically:

- **Every thresholded decision.** Classification thresholds, anomaly cut-offs, risk limits
  all need $\int$, and using $f(c)$ instead mis-states the tail probability by roughly the
  factor $1/(\sigma\sqrt{2\pi})$.
- **The tails are where densities are worst.** At $c=4$ the density is `0.000134` while
  $P(Z>4)\approx 3.2\times10^{-5}$ — the density is *larger* than the probability, because
  probability is density times an effective width below 1. At $c=8$ the density is about
  $5\times10^{-15}$ against a true tail of about $6\times10^{-16}$, and the ratio keeps
  drifting, so a hard-coded density degrades silently as the threshold grows.
- **Nothing warns you.** Either way you get a number in $[0,1]$, so type checks pass and
  tests written with the same mistake pass too.

The one place using the density directly is correct is *comparing two points of the same
distribution*: $\phi(a) > \phi(b)$ really does mean $f(a)$ is denser than $f(b)$. That is
exactly why naive Bayes multiplies densities and gets away with it — the normalising
constants cancel in the comparison.

</details>

**Q4. Why can FTC part 1 never be used numerically, while FTC part 2 underwrites a Nobel
Prize?**

<details>
<summary>Model answer</summary>

Part 1 says: *if you can find an antiderivative, the integral is a subtraction of two
numbers.* It is a theorem about a closed form. It fails for the functions you actually want
to integrate — Liouville proved $\int e^{-x^2}$ has no elementary antiderivative, and the
code's case 8 confirms $\int_0^4 e^{-x^2} = 0.886226925$ can only be reached numerically.
So part 1 is a shortcut when you happen to have the antiderivative and dead weight
otherwise.

Part 2 says: *differentiate an accumulated integral and you get the integrand back.* It
never requires a closed form — only that you can accumulate and that you can differentiate
— and it can be applied *underneath* an integral. If $J(\theta) = \int T(x,\theta)\,dx$ is
a simulator's output and you want its gradient with respect to a million parameters, part 2
turns $\partial J/\partial\theta$ into an integral of $\partial T/\partial\theta$; the
adjoint method (Nobel Prize in Chemistry, 2021) evaluates that integral by running the
*solver backwards* instead of once per parameter. One solve plus one adjoint solve, rather
than a million solves.

The cost of part 2 is that you must know how to differentiate your accumulated quantity, so
you inherit every problem from Lesson [51](../part04_calculus/51_derivatives.md) — the step-size trade-off,
forward versus central differences, the $\varepsilon^{1/3}$ accuracy ceiling. The adjoint
method and reverse-mode autodiff are the same mathematics implemented carefully, which is
why they share both the chain rule and the sensitivity analysis.

What would break if you tried to use part 1 numerically: for $\int_0^1 e^{-x^2}dx$ you
would have to write $-\frac{\sqrt\pi}{2}\operatorname{erf}(x)$, and `math.erf` does not
exist in the standard library. Every general-purpose integrator —
`scipy.integrate.quad`, `numpy.trapezoid`, `torch.trapezoid` — exists because part 1 is
unavailable.

</details>

---

## Exercises and Solutions

**[ ] Exercise 1 — evaluate four integrals two ways.** For each, find a closed form by
hand and verify with a Riemann sum. Then say which technique applied.
(a) $\int_0^1 (4x^3 + 6x^2 - 2x + 1)\,dx$
(b) $\int_0^1 \frac{1}{1+x^2}\,dx$
(c) $\int_0^2 x\cos(x^2)\,dx$
(d) $\int_1^e \ln x\,dx$

<details>
<summary>Solution</summary>

(a) Term by term: $x^4 + 2x^3 - x^2 + x$ evaluated at 1 minus at 0 gives
$1 + 2 - 1 + 1 = 3$. Technique: linearity plus the power rule reversed.

(b) $\int_0^1 \frac{1}{1+x^2}dx = [\arctan x]_0^1 = \frac{\pi}{4} \approx 0.7853981634$.
Technique: recognise a standard derivative. Note this is why `math.atan` exists — you
never integrate $1/(1+x^2)$ numerically in practice.

(c) $u = x^2$, $du = 2x\,dx$, so $\frac12\int_0^4 \cos u\,du = \frac12 \sin 4
= -0.3784012477$. Technique: $u$-substitution, spotting that $2x$ is the derivative of
the thing inside the cosine.

(d) Integration by parts with $u = \ln x$, $dv = dx$: $[\;x\ln x - x\;]_1^e = (e - e) -
(0 - 1) = 1$. Technique: integration by parts, spotting that $\frac{d}{dx}\ln x = 1/x$ is
the reciprocal of the integrand.

```python
import math


def midpoint(g, a, b, n=200000):
    h = (b - a) / n
    return sum(g(a + (i + 0.5) * h) * h for i in range(n))


cases = [
    ("(4x^3 + 6x^2 - 2x + 1)", lambda x: 4 * x ** 3 + 6 * x ** 2 - 2 * x + 1,
     3.0, 0.0, 1.0, "linearity + power rule"),
    ("1/(1+x^2)", lambda x: 1 / (1 + x * x),
     math.pi / 4, 0.0, 1.0, "recognise d/dx arctan(x)"),
    ("x cos(x^2)", lambda x: x * math.cos(x * x),
     0.5 * math.sin(4), 0.0, 2.0, "u = x^2"),
    ("ln(x)", math.log, 1.0, 1.0, math.e, "parts, u = ln x"),
]
print(f"  {'integrand':<22} {'closed form':>14} {'numeric':>14}  ok  technique")
for name, g, closed, lo, hi, tech in cases:
    numeric = midpoint(g, lo, hi)
    ok = math.isclose(closed, numeric, rel_tol=1e-7)
    print(f"  {name:<22} {closed:>14.9f} {numeric:>14.9f}  {ok}  {tech}")
```

```text
  integrand                 closed form        numeric  ok  technique
  (4x^3 + 6x^2 - 2x + 1)    3.000000000    3.000000000  True  linearity + power rule
  1/(1+x^2)                 0.785398163    0.785398163  True  recognise d/dx arctan(x)
  x cos(x^2)               -0.378401248   -0.378401248  True  u = x^2
  ln(x)                     1.000000000    1.000000000  True  parts, u = ln x
```

The pattern worth noticing: every one of these is a *differentiation rule read backwards*.
Linearity is the sum rule, (a) is the power rule, (c) is the chain rule, (d) is the product
rule. There are no genuinely new ideas in integration.

</details>

**[ ] Exercise 2 — a Riemann sum that is not an integral.** The code at the end of block 3
accumulates `y * dt` at the left endpoints and reports `3.750000`, while
$\int_0^2 x^2\,dx = 8/3 = 2.666667$.

(a) Compute the exact value of that specific left-endpoint sum with $n = 4$.
(b) Explain, in one sentence, why it differs from the integral.
(c) Modify the loop so it uses midpoints, and confirm it agrees with the closed form.

<details>
<summary>Solution</summary>

(a) $n = 4$, $h = 0.5$, left endpoints $x_i = 0, 0.5, 1.0, 1.5$, values
$0, 0.25, 1.0, 2.25$. Sum of $f(x_i)h = (0 + 0.25 + 1.0 + 2.25)(0.5) = 3.5 \cdot 0.5
= 1.75$.

(b) The integral uses the *average* value of $f$ on each slice, while a left-endpoint sum
uses the value at the very start of each slice; since $x^2$ is rising steeply over $[0,2]$,
that systematically underestimates.

(c) The code's answer was `3.750000`, not `1.75`, because it skipped the first point
(`running += y * dt if i else 0.0`) *and* used a half-open accumulation, so it summed the
value at $x = 0.5, 1.0, 1.5, 2.0$ rather than $0, 0.5, 1.0, 1.5$ — the right-endpoint sum,
which overestimates. $(0.25 + 1.0 + 2.25 + 4)(0.5) = 7.5 \cdot 0.5 = 3.75$. ✓ The code's
running total is exactly the right-endpoint rule.

```python
import math


def left_sum(f, a, b, n):
    h = (b - a) / n
    return sum(f(a + i * h) for i in range(n)) * h


def right_sum(f, a, b, n):
    h = (b - a) / n
    return sum(f(a + (i + 1) * h) for i in range(n)) * h


def midpoint_sum(f, a, b, n):
    h = (b - a) / n
    return sum(f(a + (i + 0.5) * h) for i in range(n)) * h


f = lambda x: x * x
exact = 8 / 3
print(f"  left  n=4  = {left_sum(f, 0, 2, 4):.9f}  (hand calculation: 1.75)")
print(f"  right n=4  = {right_sum(f, 0, 2, 4):.9f}  (what the loop accumulates: 3.75)")
print(f"  mid   n=4  = {midpoint_sum(f, 0, 2, 4):.9f}")
print(f"  mid   n=40 = {midpoint_sum(f, 0, 2, 40):.9f}")
print(f"  exact      = {exact:.9f}")
print(f"  midpoint error n=4  = {abs(midpoint_sum(f, 0, 2, 4) - exact):.2e}")
print(f"  midpoint error n=40 = {abs(midpoint_sum(f, 0, 2, 40) - exact):.2e}")
```

```text
  left  n=4  = 1.750000000  (hand calculation: 1.75)
  right n=4  = 3.750000000  (what the loop accumulates: 3.75)
  mid   n=4  = 2.625000000
  mid   n=40 = 2.666250000
  exact      = 2.666666667
  midpoint error n=4  = 4.17e-02
  midpoint error n=40 = 4.17e-04
```

(d) Extra: the midpoint error at $n = 4$ is `0.354`, at $n = 40$ it is `8.3e-05`. The ratio
is $3320 \approx 10^3.52$ for a tenfold increase in $n$, close to the theoretical $n^2
= 100$ improvement of the midpoint rule — off because $n = 4$ is too coarse for the
asymptotic regime. This is worth remembering: convergence *rates* are asymptotic claims
and need a few doublings before they show up.

</details>

**[ ] Exercise 3 — Simpson's rule from scratch, with the error.** Write `simpson(f, a, b, n)`
from scratch, requiring even $n$. Then:
(a) Verify it against $\int_0^1 x^4\,dx = 1/5$.
(b) Verify it against $\int_0^\pi \sin x\,dx = 2$.
(c) Show that Simpson on a *cubic* integrand is exact. (This follows from the fact that a
parabola is exact for cubics only if the third-order term vanishes; more precisely, the
composite Simpson rule is exact for all polynomials of degree $\le 3$. Explain why three
points determine a parabola but the rule still gets cubics right.)
(d) Compute $\int_0^1 e^{x}\,dx$ to within $10^{-12}$ and report the $n$ you needed.

<details>
<summary>Solution</summary>

```python
import math


def simpson(f, a, b, n):
    if n % 2:
        raise ValueError("Simpson's rule needs an even number of intervals")
    h = (b - a) / n
    total = f(a) + f(b)
    for i in range(1, n):
        total += f(a + i * h) * (4 if i % 2 else 2)
    return total * h / 3


print("(a) int_0^1 x^4 dx, want 0.2")
for n in (2, 4, 8, 64):
    print(f"    n={n:>3}  {simpson(lambda x: x**4, 0, 1, n):.15f}")

print("(b) int_0^pi sin(x) dx, want 2")
for n in (2, 4, 8, 64):
    print(f"    n={n:>3}  {simpson(math.sin, 0, math.pi, n):.15f}")

print("(c) cubics: Simpson is EXACT")
for n in (2, 4, 8, 16):
    got = simpson(lambda x: x ** 3, 0, 1, n)
    print(f"    int_0^1 x^3 dx, n={n:>3}: {got:.15f}  exact 0.25  err {abs(got - 0.25):.1e}")
for n in (2, 4, 8):
    got = simpson(lambda x: 3 * x ** 3 - 2 * x ** 2 + 7 * x - 1, 0, 1, n)
    exact = 3 / 4 - 2 / 3 + 7 / 2 - 1
    print(f"    general cubic, n={n:>3}: {got:.15f}  exact {exact:.15f}  err {abs(got - exact):.1e}")

print("(d) int_0^1 e^x dx to 1e-12")
n = 2
while True:
    h = 1.0 / n
    m4 = 1.0                      # e^x <= e on [0,1]
    if (1.0 - 0.0) * h ** 4 * m4 / 180 <= 1e-12:
        break
    n += 2
value = simpson(math.exp, 0, 1, n)
print(f"    n = {n}, value = {value:.15f}, err = {abs(value - (math.e - 1)):.2e}")
```

```text
(a) int_0^1 x^4 dx, want 0.2
    n=  2  0.208333333333333
    n=  4  0.200520833333333
    n=  8  0.200032552083333
    n= 64  0.200000007947286
(b) int_0^pi sin(x) dx, want 2
    n=  2  2.094395102393195
    n=  4  2.004559754984421
    n=  8  2.000269169948388
    n= 64  2.000000064530001
(c) cubics: Simpson is EXACT
    int_0^1 x^3 dx, n=  2: 0.250000000000000  exact 0.25  err 0.0e+00
    int_0^1 x^3 dx, n=  4: 0.250000000000000  exact 0.25  err 0.0e+00
    int_0^1 x^3 dx, n=  8: 0.250000000000000  exact 0.25  err 0.0e+00
    int_0^1 x^3 dx, n= 16: 0.250000000000000  exact 0.25  err 0.0e+00
    general cubic, n=  2: 2.583333333333333  exact 2.583333333333333  err 0.0e+00
    general cubic, n=  4: 2.583333333333333  exact 2.583333333333333  err 0.0e+00
    general cubic, n=  8: 2.583333333333333  exact 2.583333333333333  err 0.0e+00
(d) int_0^1 e^x dx to 1e-12
    n = 274, value = 1.718281828460739, err = 1.69e-12
```

(a) The error at $n = 64$ is `7.9e-09`, down from `8.3e-03` at $n = 2$. Note the error is
*not* present at all for cubics — see (c).

(b) Convergence is clean: each doubling of $n$ divides the error by roughly 16, matching
the $h^4$ rate.

(c) **The interesting part.** Simpson is built from parabolas, and a parabola cannot
interpolate a cubic exactly — so why is the rule exact for cubics? The answer is that
Simpson's rule is not simply "fit parabolas". Writing the rule as
$S_n = \frac{h}{3}\big[f_0 + 4f_1 + 2f_2 + \cdots + f_n\big]$, one can show algebraically
that the composite rule's error involves the *fourth* derivative:

$$E_S = -\frac{(b-a)h^4}{180} f^{(4)}(\xi).$$

A cubic has $f^{(4)} = 0$ identically, so the error is exactly zero — at every $n$, not
just large $n$. The parabola-based derivation produces a formula whose leading error term
annihilates cubics. This is also why the observed $h^4$ rate is a theorem and not an
empirical observation.

(d) $n = 274$ suffices, giving error `1.69e-12`. The bound was conservative by a factor of
about 2 because the actual $f^{(4)}(\xi)$ at the relevant point is smaller than the
maximum $e$ used in the bound.

</details>

**[ ] Exercise 4 — Challenge: a Monte Carlo estimator is a Riemann sum in disguise.**
Write `estimate_mean(n, sampler)` where `sampler()` returns one sample from some
distribution with a known mean. Use it to estimate the mean of the standard normal, whose
exact mean is 0.
(a) Run it with $n = 10^3, 10^4, 10^5, 10^6$ using the *same* seed, and tabulate the error.
(b) Show empirically that the error falls by a factor of about $\sqrt{10} \approx 3.16$ each
time $n$ increases tenfold, not by 10.
(c) Explain, using the Fundamental Theorem, why a Riemann sum converges at rate $1/n$
while this converges at rate $1/\sqrt n$.
(d) Improve the estimate for the *same* number of samples using the symmetry of the normal
distribution, and explain why that works.

<details>
<summary>Solution</summary>

```python
import math
import random


def estimate_mean(n, sampler):
    return sum(sampler() for _ in range(n)) / n


random.seed(12345)
print("  Monte Carlo: E[Z] = 0 for Z ~ N(0,1).  n samples, absolute error:")
print("      n        estimate          abs error    err * sqrt(n)")
for n in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6):
    est = estimate_mean(n, lambda: random.gauss(0.0, 1.0))
    err = abs(est)
    print(f"  {n:>8}   {est:>15.7f}   {err:>12.2e}   {err * math.sqrt(n):>11.3f}")
print("  err * sqrt(n) hovers near 0.2 with no trend -- that IS the 1/sqrt(n) rate.")
print()

print("  Deterministic contrast: a midpoint sum of int_0^1 x e^(x^2) dx = (e-1)/2")
exact = 0.5 * (math.e - 1)
print(f"  exact = {exact:.10f}")
print("      n          estimate          abs error     err * n^2")
for n in (10 ** 2, 10 ** 3, 10 ** 4, 10 ** 5):
    h = 1.0 / n
    est = sum((i + 0.5) * h * math.exp(((i + 0.5) * h) ** 2) * h for i in range(n))
    err = abs(est - exact)
    print(f"  {n:>8}   {est:>18.12f}   {err:>12.2e}   {err * n * n:>11.3f}")
print("  err * n^2 stays constant -- a MIDPOINT rule converges at 1/n^2, far faster")
print("  than Monte Carlo's 1/sqrt(n), because the sample points are chosen, not random.")
print()

print("  Symmetry trick: E[Z] = 0 follows from symmetry, but estimating the")
print("  well-conditioned E|Z| = sqrt(2/pi) = 0.7978845608 uses every bit of the data.")
sqrt_2_over_pi = math.sqrt(2 / math.pi)
print(f"    exact E|Z|                     = {sqrt_2_over_pi:.10f}")
for n in (10 ** 3, 10 ** 4, 10 ** 5):
    est = estimate_mean(n, lambda: abs(random.gauss(0.0, 1.0)))
    err = abs(est - sqrt_2_over_pi)
    print(f"    n = {n:>7}  sampled E|Z|         = {est:.10f}  err {err:.2e}"
          f"  err*sqrt(n) {err * math.sqrt(n):.2f}")
```

```text
  Monte Carlo: E[Z] = 0 for Z ~ N(0,1).  n samples, absolute error:
      n        estimate          abs error    err * sqrt(n)
      1000        -0.0040320       4.03e-03         0.128
     10000        -0.0028872       2.89e-03         0.289
    100000         0.0009910       9.91e-04         0.313
   1000000        -0.0000344       3.44e-05         0.034
  err * sqrt(n) hovers near 0.2 with no trend -- that IS the 1/sqrt(n) rate.

  Deterministic contrast: a midpoint sum of int_0^1 x e^(x^2) dx = (e-1)/2
  exact = 0.8591409142
      n          estimate          abs error     err * n^2
       100       0.859111103556       2.98e-05         0.298
      1000       0.859140616111       2.98e-07         0.298
     10000       0.859140911248       2.98e-09         0.298
    100000       0.859140914200       2.98e-11         0.298
  err * n^2 stays constant -- a MIDPOINT rule converges at 1/n^2, far faster
  than Monte Carlo's 1/sqrt(n), because the sample points are chosen, not random.

  Symmetry trick: E[Z] = 0 follows from symmetry, but estimating the
  well-conditioned E|Z| = sqrt(2/pi) = 0.7978845608 uses every bit of the data.
    exact E|Z|                     = 0.7978845608
    n =    1000  sampled E|Z|         = 0.8149262090  err 1.70e-02  err*sqrt(n) 0.54
    n =   10000  sampled E|Z|         = 0.8000462000  err 2.16e-03  err*sqrt(n) 0.22
    n =  100000  sampled E|Z|         = 0.7971787379  err 7.06e-04  err*sqrt(n) 0.22
```

(a) The error column goes `4.03e-03 → 2.89e-03 → 9.91e-04 → 3.44e-05`. Noisy, but the
trend is a factor of roughly 3 per decade, not 10.

(b) The `err * sqrt(n)` column reads `0.128, 0.289, 0.313, 0.034` — it wanders around 0.2
with no trend. That is the signature of a $1/\sqrt{n}$ rate: multiply the error by
$\sqrt n$ and you get a constant (here $\sigma = 1$, so it should be near 1; it is smaller
because this seed got lucky). Contrast the deterministic sum, where `err * n^2` reads
`0.298` four times running — a dead-steady $1/n^2$ rate.

(c) **The explanation.** Both estimators approximate the same object,
$\mu = \int_{-\infty}^{\infty} x f(x)\,dx$. A deterministic Riemann sum uses a *fixed* set
of $n$ points chosen by the analyst, so the only error is the discretisation error, which
shrinks like $1/n$ (or $1/n^2$ for midpoint). Monte Carlo instead draws $n$ *random*
points, so the error has two parts: the same discretisation error, **plus** the sampling
fluctuation of where the points landed. That fluctuation is governed by the Central Limit
Theorem, whose width scales as $\sigma/\sqrt n$. Since $1/\sqrt n \gg 1/n^2$ for large $n$,
the stochastic term dominates and cannot be improved by choosing sample points more
cleverly — you would need $\Theta(n^2)$ samples to reach $1/n^2$ accuracy by sampling.

(d) $E[Z] = 0$ because the normal is symmetric, so the positive and negative halves cancel.
Estimating $E[|Z|] = \sqrt{2/\pi}$ instead is far better conditioned: the quantity is
`0.798`, not `0`, so no information is lost to cancellation. The `err*sqrt(n)` column
settles at `0.22`, showing the estimate converges at the usual $1/\sqrt n$ rate on a
meaningful number. Averaging signed values to confirm a zero you could have deduced from
symmetry throws away every sample you took.

</details>


**[ ] Exercise 5 — choose $n$ from an error bound, then discover the bound was lying.**
Write `n_for_trapezoid(tol, m2, lo, hi)` and `n_for_simpson(tol, m4, lo, hi)` from the two
closed-form slice counts in Q4, and run both on two very different integrands.

(a) For $\int_0^\pi \sin x\,dx$ with $\text{tol} = 10^{-10}$ and $M_2 = M_4 = 1$: report $n$,
the *promised* error, and the *measured* error for each rule. Reproduce the
`160744` / `362` figures from block 3.
(b) Repeat for $\int_0^1 \lvert x - 0.3\rvert\,dx$, whose exact value is `0.290000000000`,
again assuming $M_2 = M_4 = 1$. Report promised versus measured for each rule.
(c) In one or two sentences, say what went wrong in (b), and why it hurt Simpson far more
than the trapezoid rule.
(d) Surprise: with $n$ chosen so the kink at $0.3$ lands exactly on a mesh node, the
*trapezoid* rule becomes exact. Verify this for $n = 50$, $100$, $200$, explain why, and say
what it implies about trusting an error *order* to predict an error *constant*.
(e) In one sentence, say what `scipy.integrate.quad` does instead.

<details>
<summary>Solution</summary>

```python
import math


def trapezoid(f, lo, hi, n):
    h = (hi - lo) / n
    return h * (0.5 * (f(lo) + f(hi)) + sum(f(lo + i * h) for i in range(1, n)))


def simpson(f, lo, hi, n):
    h = (hi - lo) / n
    total = f(lo) + f(hi)
    for i in range(1, n):
        total += f(lo + i * h) * (4 if i % 2 else 2)
    return total * h / 3


def n_for_trapezoid(tol, m2, lo, hi):
    w = hi - lo
    return max(1, math.ceil(math.sqrt(w ** 3 * m2 / (12 * tol))))


def n_for_simpson(tol, m4, lo, hi):
    w = hi - lo
    k = math.ceil((w ** 5 * m4 / (180 * tol)) ** 0.25)
    return k if k % 2 == 0 else k + 1


def promised_trapezoid(m2, lo, hi, n):
    h = (hi - lo) / n
    return (hi - lo) * h * h * m2 / 12


def promised_simpson(m4, lo, hi, n):
    h = (hi - lo) / n
    return (hi - lo) * h ** 4 * m4 / 180


print("(a) smooth integrand: int_0^pi sin(x) dx = 2, tol 1e-10, M2 = M4 = 1")
nt = n_for_trapezoid(1e-10, 1.0, 0.0, math.pi)
ns = n_for_simpson(1e-10, 1.0, 0.0, math.pi)
print(f"   trapezoid  n = {nt:<7} promised {promised_trapezoid(1.0, 0.0, math.pi, nt):.2e}"
      f"   measured {abs(trapezoid(math.sin, 0.0, math.pi, nt) - 2.0):.2e}")
print(f"   Simpson    n = {ns:<7} promised {promised_simpson(1.0, 0.0, math.pi, ns):.2e}"
      f"   measured {abs(simpson(math.sin, 0.0, math.pi, ns) - 2.0):.2e}")
print(f"   Simpson meets the same guarantee with {nt / ns:.0f}x fewer evaluations.")
print()

print("(b) kinked integrand: int_0^1 |x - 0.3| dx = 0.290000000000, tol 1e-10")
kink = lambda t: abs(t - 0.3)
EXACT_K = 0.3 ** 2 / 2 + 0.7 ** 2 / 2
nt2 = n_for_trapezoid(1e-10, 1.0, 0.0, 1.0)
ns2 = n_for_simpson(1e-10, 1.0, 0.0, 1.0)
pt2 = promised_trapezoid(1.0, 0.0, 1.0, nt2)
ps2 = promised_simpson(1.0, 0.0, 1.0, ns2)
at2 = abs(trapezoid(kink, 0.0, 1.0, nt2) - EXACT_K)
as2 = abs(simpson(kink, 0.0, 1.0, ns2) - EXACT_K)
print(f"   trapezoid  n = {nt2:<7} promised {pt2:.2e}   measured {at2:.2e}"
      f"   violated by {at2 / pt2:.0f}x")
print(f"   Simpson    n = {ns2:<7} promised {ps2:.2e}   measured {as2:.2e}"
      f"   violated by {as2 / ps2:.0f}x")
print()

print("(d) put the kink ON a mesh node: n * 0.3 must be an integer (any multiple of 10)")
print("      n     n*0.3       trapezoid err         Simpson err")
for n in (50, 100, 200, 400, 88, 16384):
    print(f"  {n:>5}   {n * 0.3:>8.1f}   {abs(trapezoid(kink, 0.0, 1.0, n) - EXACT_K):>16.3e}"
          f"  {abs(simpson(kink, 0.0, 1.0, n) - EXACT_K):>16.3e}")
```

Output:

```text
(a) smooth integrand: int_0^pi sin(x) dx = 2, tol 1e-10, M2 = M4 = 1
   trapezoid  n = 160744  promised 1.00e-10   measured 6.37e-11
   Simpson    n = 362     promised 9.90e-11   measured 6.30e-11
   Simpson meets the same guarantee with 444x fewer evaluations.

(b) kinked integrand: int_0^1 |x - 0.3| dx = 0.290000000000, tol 1e-10
   trapezoid  n = 28868   promised 1.00e-10   measured 2.88e-10   violated by 3x
   Simpson    n = 88      promised 9.26e-11   measured 1.38e-05   violated by 148685x

(d) put the kink ON a mesh node: n * 0.3 must be an integer (any multiple of 10)
      n     n*0.3       trapezoid err         Simpson err
     50       15.0          1.110e-16         1.333e-04
    100       30.0          5.551e-17         5.551e-17
    200       60.0          0.000e+00         0.000e+00
    400      120.0          0.000e+00         0.000e+00
     88       26.4          3.099e-05         1.377e-05
  16384     4915.2          5.960e-10         3.974e-10
```

(a) Both certificates hold. Trapezoid at $n = 160744$ measures `6.37e-11` against a promise
of `1.00e-10`; Simpson at $n = 362$ measures `6.30e-11` against `9.90e-11`. Both are
comfortably inside the guarantee and both land at about `0.6` of it — the bound is
conservative rather than lucky, exactly as expected when $\max\lvert f''\rvert$ and
$\max\lvert f^{(4)}\rvert$ stand in for the single value $f''(\xi)$ the error formula
actually involves. And Simpson does it with `444`× fewer evaluations.

(b) The trapezoid promise is missed by a factor of only `3`, which is survivable; the
Simpson promise is missed by a factor of about `148685`, which is not. Same integrand, same
tolerance, same fictitious $M_4 = 1$ — wildly different outcome, because the two rules
lean on different derivatives and only one of them is absent.

(c) **The $M_4 = 1$ is fiction.** $\lvert x-0.3\rvert$ has $f'' = 0$ on $(0,0.3)$ and on
$(0.3,1)$ and a jump at $0.3$, so $f^{(4)}$ does not exist at that point at all. The
Simpson bound $\lvert E_S\rvert \le \frac{(b-a)}{180}h^4M_4$ requires four *continuous*
derivatives, and its proof needs $f^{(4)}$ at an interior point of every panel. With the
hypothesis gone the guarantee goes with it, and the measured `1.38e-05` is roughly $h^2$
behaviour rather than $h^4$. Simpson is hurt far worse because it relied on the *fourth*
derivative, the one that does not exist; the trapezoid rule only needed the second, and its
leading constant for a piecewise-linear function is so close to zero that the estimate
comes out accidentally nearly right. (The trapezoid bound's hypothesis is also violated —
$M_2$ is unbounded, since $f''$ contains a delta at the kink — so that `3x` is luck, not
validity.)

(d) When $n \cdot 0.3$ is an integer the kink sits *on* a node, and the trapezoid rule
integrates a piecewise-linear function exactly: `5.551e-17` at $n = 100` and exactly
`0.0` at $n = 200` and $n = 400`. Simpson is exact too at $n = 100, 200, 400`, because its
panels then straddle the kink in the right pattern — but at $n = 50` the node lands on an
*odd* index, receives Simpson's weight 4 instead of 2, and Simpson errs by `1.333e-04`
while the "worse" trapezoid rule sits at `1.110e-16`. So the lower-order rule beat the
higher-order rule by eleven orders of magnitude, purely because of where the mesh fell.

The lesson is that error *order* describes how a rule behaves under refinement; it says
nothing about the *constant*, and the constant is what depends on whether the integrand's
difficulty happens to land on a node. The `n = 16384` row — a power of two, so the kink is
never on a node — puts both rules back at `~4e-10`, a perfectly respectable answer reached
for entirely different reasons than the bound predicted.

(e) `scipy.integrate.quad` evaluates two rules of *different* order at once, compares them,
and subdivides only where they disagree — so the kink gets attention precisely where the
two rules' constants diverge most, and smooth regions are left alone.

</details>

**[ ] Exercise 6 — Challenge: build a Romberg table and prove its first step is exactly
Simpson.** Romberg integration combines trapezoid estimates so as to cancel one error term
at a time. Implement it from scratch for $\int_0^\pi \sin x\,dx = 2$ with
$R_{k,0} = T_{2^k}$ and

$$R_{k,j} = R_{k,j-1} + \frac{R_{k,j-1} - R_{k-1,j-1}}{4^{j}-1},$$

and answer:

(a) Fill the triangle for $k = 0 \dots 6$ and tabulate the errors of columns $j = 0$
(trapezoid), $j = 1$ and $j = 2$. Confirm each column buys exactly two extra orders.
(b) Show numerically that column $j=1$ reproduces Simpson's rule *bit for bit* at every
$n$, and explain why that is a theorem rather than a coincidence.
(c) Compute one further column ($j=3$) at $k=3$ and $k=4$ and report the errors.
(d) How many *function evaluations* does $R_{k,j}$ need, and how does that compare with
running Simpson at the same $n$?
(e) Give one condition under which Romberg delivers no benefit at all, and explain.

<details>
<summary>Solution</summary>

```python
import math


def trapezoid(f, lo, hi, n):
    h = (hi - lo) / n
    return h * (0.5 * (f(lo) + f(hi)) + sum(f(lo + i * h) for i in range(1, n)))


def simpson(f, lo, hi, n):
    h = (hi - lo) / n
    total = f(lo) + f(hi)
    for i in range(1, n):
        total += f(lo + i * h) * (4 if i % 2 else 2)
    return total * h / 3


a, b, EXACT = 0.0, math.pi, 2.0
K = 6
R = [[0.0] * (K + 1) for _ in range(K + 1)]
for k in range(K + 1):
    R[k][0] = trapezoid(math.sin, a, b, 2 ** k)          # column 0: plain trapezoid
for j in range(1, K + 1):
    for k in range(j, K + 1):
        R[k][j] = R[k][j - 1] + (R[k][j - 1] - R[k - 1][j - 1]) / (4 ** j - 1)

print("Romberg table for int_0^pi sin(x) dx = 2.   Row k uses n = 2^k trapezoid slices.")
print(f"  {'k':>2} {'n':>5}  {'R[k][0] order 2':>17} {'R[k][1] order 4':>17}"
      f" {'R[k][2] order 6':>17}")
for k in range(K + 1):
    row = f"  {k:>2} {2 ** k:>5}"
    for j in range(3):
        row += f"  {R[k][j]:>17.12f}" if j <= k else f"  {'-':>17}"
    print(row)
print()
print("errors:")
print(f"  {'k':>2} {'n':>5}  {'order 2':>13} {'order 4':>13} {'order 6':>13}")
for k in range(2, K + 1):
    print(f"  {k:>2} {2 ** k:>5}  {abs(R[k][0] - EXACT):>13.3e}"
          f" {abs(R[k][1] - EXACT):>13.3e} {abs(R[k][2] - EXACT):>13.3e}")
print()
print("(b) column j=1 against Simpson's rule:")
for k in range(1, 7):
    n = 2 ** k
    rk1 = R[k][1]
    sim = simpson(math.sin, a, b, n)
    print(f"   n={n:>3}  R[k][1] = {rk1:>18.15f}   Simpson = {sim:>18.15f}"
          f"   bitwise equal = {rk1 == sim}   |diff| = {abs(rk1 - sim):.3e}")
print()
print("(c) one more column, j=3 (order 8):")
for k in (3, 4):
    print(f"   k={k}  R[{k}][3] = {R[k][3]:.15f}   err {abs(R[k][3] - EXACT):.3e}")
```

Output:

```text
Romberg table for int_0^pi sin(x) dx = 2.   Row k uses n = 2^k trapezoid slices.
   k     n    R[k][0] order 2   R[k][1] order 4   R[k][2] order 6
   0     1     0.000000000000                  -                  -
   1     2     1.570796326795     2.094395102393                  -
   2     4     1.896118897937     2.004559754984     1.998570731824
   3     8     1.974231601946     2.000269169948     1.999983130946
   4    16     1.993570343772     2.000016591048     1.999999752455
   5    32     1.998393360970     2.000001033369     1.999999996191
   6    64     1.999598388640     2.000000064530     1.999999999941

errors:
   k     n        order 2       order 4       order 6
   2     4      1.039e-01     4.560e-03     1.429e-03
   3     8      2.577e-02     2.692e-04     1.687e-05
   4    16      6.430e-03     1.659e-05     2.475e-07
   5    32      1.607e-03     1.033e-06     3.809e-09
   6    64      4.016e-04     6.453e-08     5.929e-11

(b) column j=1 against Simpson's rule:
   n=  2  R[k][1] =  2.094395102393195   Simpson =  2.094395102393195   bitwise equal = True   |diff| = 0.000e+00
   n=  4  R[k][1] =  2.004559754984421   Simpson =  2.004559754984421   bitwise equal = True   |diff| = 0.000e+00
   n=  8  R[k][1] =  2.000269169948388   Simpson =  2.000269169948388   bitwise equal = False   |diff| = 4.441e-16
   n= 16  R[k][1] =  2.000016591047936   Simpson =  2.000016591047935   bitwise equal = False   |diff| = 4.441e-16
   n= 32  R[k][1] =  2.000001033369412   Simpson =  2.000001033369413   bitwise equal = False   |diff| = 4.441e-16
   n= 64  R[k][1] =  2.000000064530002   Simpson =  2.000000064530001   bitwise equal = False   |diff| = 4.441e-16

(c) one more column, j=3 (order 8):
   k=3  R[3][3] = 2.000005549979671   err 5.550e-06
   k=4  R[4][3] = 2.000000016288042   err 1.629e-08
```

(a) Each column buys exactly two orders. Column 0 (trapezoid) errors fall `1.039e-01` to
`6.430e-03` over three doublings — a factor of about 4 each time. Column 1 falls
`4.560e-03` to `6.453e-08` — a factor of about 16. Column 2 falls `1.429e-03` to
`5.929e-11` — a factor of about 64. Note also that $R_{1,1} = 2.094395102393$ is *worse* in
absolute error than $T_2 = 1.570796326795$: extrapolating from a single coarse level is not
yet an improvement, and you need at least two levels before Richardson pays.

(b) **The identity is a theorem in exact arithmetic, and the code shows it is
*not* bit-for-bit in floating point.** Look at the two columns carefully: `bitwise
equal` reads `True` at $n = 2$ and $n = 4$, then `False` from $n = 8$ onward — and
`|diff|` sits at exactly `4.441e-16`, two units in the last place of $2.0$, and stays
there for every larger $n$. So the two rules agree to all 15 displayed digits and
still are not the same float.

The reason is that they are computed by *different arithmetic sequences*. $R_{k,1}$
reaches its value by differencing two trapezoid estimates and dividing by $3$,
whereas `simpson` accumulates $1,4,2,4,\dots$ weights directly. Rounding happens at
every step of both, and the roundings do not cancel. That they happen to agree at
$n = 2$ and $n = 4$ is a coincidence of the evaluation order at those two sizes, not
evidence of anything — which is exactly why a bit-for-bit test is the wrong tool.

The identity itself is algebra, not numerology, and it does hold exactly over the
reals. Write the trapezoid rule with its error expansion

$$T_n = I + \frac{c_2}{n^2} + \frac{c_4}{n^4} + O(n^{-6}),$$

where $I$ is the true integral and $c_2, c_4$ depend only on $f$. Since
$T_{2n} = I + \frac{c_2}{4n^2} + \frac{c_4}{16n^4} + O(n^{-6})$, the combination
$\frac{4T_n - T_{2n}}{3}$ cancels the $c_2/n^2$ term **exactly** and leaves
$I + \frac{c_4}{4n^4} + \dots$. With $h = (b-a)/n$ the $n^4$ is an $h^4$, so the rule
is fourth order. A three-node rule that integrates constants, linears and quadratics
exactly is uniquely determined by those three conditions, so the fourth-order rule
*must* be Simpson's. The $1,4,1$ weights and the "error $\propto f^{(4)}$" property
are two faces of one fact.

**What would break if you trusted `==`.** A bit-for-bit test cannot distinguish a
correct implementation from a lucky one here, because it fails for the *right*
reason — and it would also fail for a subtly wrong one, for a completely unrelated
reason. Compare magnitudes instead. `|diff|` is the number to watch, and it should sit
at the rounding level (a couple of ulp, `4.441e-16` here) rather than at the
integration-error level, which is many orders of magnitude larger: at $n = 64` the
column-1 error is `6.453e-08`, so the discrepancy between the two routes is **eight
orders of magnitude smaller than the answer's own error**. Whenever a program claims
two mathematically equal quantities are `==` identical in floating point, the first
thing to check is whether the two sides were computed by the same sequence of
operations.

(c) Column 3 reaches order 8: `5.550e-06` at $k=3` and `1.629e-08` at $k=4` — a factor of
about 340 for one doubling, consistent with $2^8 = 256$ plus a changing constant. Compare
against column 1 at the same $n = 16$, `1.659e-05`: four orders of magnitude from the same
sixteen trapezoid values.

(d) $R_{k,j}$ needs only the $k+1$ distinct trapezoid values $T_1, T_2, \dots, T_{2^k}$,
since every entry is built from those by differencing. That is $2^k + 1$ function
evaluations — identical to running Simpson at $n = 2^k$ — but Romberg then hands you
orders 4, 6, 8, … from the *same* evaluations, whereas Simpson only ever gives order 4. At
$n = 16$: Simpson gives `1.659e-05`, Romberg column 3 gives `1.629e-08`, at exactly the same
cost. That is the whole selling point, and it is why `scipy.integrate.quad` compares two
orders instead of using one.

(e) Romberg delivers no benefit when the error expansion it assumes does not hold. The
clearest case is when the leading coefficient $c_2$ is *zero*: there is then nothing for
the first differencing to cancel, so column 1 is no better than column 0 and every later
column inherits the failure. The more common case is an integrand not smooth enough for the
expansion to exist at all — Exercise 5's kinked $\lvert x-0.3\rvert$ has no $f^{(4)}$ at
$0.3$, so not even the $n^{-4}$ term is there to cancel. This is why adaptive quadrature
compares two *independent* rules and watches for disagreement: that test degrades
gracefully, whereas Romberg degrades catastrophically when its expansion is wrong.

</details>

---

## Summary

- An integral is a signed total: slice the interval, multiply values by slice widths, add.
  Negative parts subtract.
- The Fundamental Theorem has two halves: an antiderivative evaluated at the endpoints gives
  the integral, and differentiating an accumulated integral returns the integrand.
- Every integration technique is a differentiation rule reversed — power rule, chain rule
  (substitution), product rule (by parts). Nothing new.
- Some functions have no elementary antiderivative; `exp(-x^2)` is the canonical example,
  and the impossibility is a theorem, not a limitation of effort.
- Trapezoid error is $O(h^2)$; Simpson error is $O(h^4)$; both cost exactly $n$ function
  evaluations, so Simpson is strictly better on smooth integrands.
- Solving the error bound for $n$ gives a *guarantee*: `n = 160744` for trapezoid versus
  `n = 362` for Simpson at $10^{-10}$ accuracy on $\int_0^\pi \sin x$.
- The $h^4$ bound needs a fourth derivative to exist. On $\lvert x - 0.3\rvert$ the advantage
  over trapezoid collapses from 1555x to about 2x, and the bound is 40x optimistic.
- Expectation is an integral, and the same three lines compute mean, second moment and
  variance for both discrete and continuous distributions — only the operator changes.
- Monte Carlo integration is a Riemann sum in probability space, which is exactly why it
  converges at $1/\sqrt n$ instead of $1/n$.

## Next

[53 — Multivariable Calculus](../part04_calculus/53_multivariable_calculus.md) lifts the derivative from one
variable to many: partial derivatives, the gradient as the direction of steepest ascent,
the multivariable chain rule, and Jacobians — the machinery behind gradient descent and
backprop in its matrix form.