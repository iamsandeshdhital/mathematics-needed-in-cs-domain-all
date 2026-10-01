# 65 — Continuous Random Variables

**Part**: part05_probability_statistics · **Prerequisites**: 64 · **Time**: 40 min

---

## In Plain Words

A discrete random variable can only take a limited list of values: 3 retries, 7
failures. A continuous one takes any value at all: 12.7 milliseconds, 3.14159
requests per second. Because you can split any interval into infinitely many
pieces, asking "what is the probability X equals exactly 12.7?" becomes a strange
question — you can always split it further. The probability is always zero.

So probability gets redefined as an *area*. A continuous variable is described by
a density curve, and the probability of an event is the area under the curve
over the relevant range. This immediately explains something that trips up
everyone: a density value can be larger than 1. A density is not a probability,
it is a probability *per unit of x*. Two densities can both exceed 1 because they
sit at different x values and the total area is what must equal 1.

This lesson develops the three distributions you will actually meet. The uniform
is flat and simple. The exponential models waiting times and has a startling
property — it forgets. The normal is the bell curve, and because it shows up
whenever you average a lot of things, it becomes the workhorse of the entire
second half of this part.

## Why Computer Science Cares

- **Latency and every "how long until" quantity.** Time to first byte, time to
  a failure, inter-arrival gaps. The exponential is the default model for
  arrival times, and the normal approximation explains why percentile-based SLOs
  behave the way they do.
- **Load testing.** Generating a realistic request stream means sampling
  inter-arrival times from an exponential distribution, and this is one line of
  code.
- **Monte Carlo integration.** Uniform sampling turns a multi-dimensional volume
  into an average, which is how numerical integration is done without a formula
  ([Lesson 70](70_information_theory_entropy.md) uses this idea).
- **Averaging many small things.** Gradient descent updates, shuffled SGD
  minibatch means, and averaged sensor readings are all approximately normal by
  the central limit theorem ([Lesson 68](68_law_of_large_numbers_and_clt.md)),
  which is why normal-based confidence intervals work at all.
- **`numpy.random` and friends.** `np.random.normal`, `np.random.exponential`,
  `np.random.uniform` are exactly these three, and their `scale`/`loc` arguments
  are the parameters below.

## The Formal Version

**Definition.** X is a *continuous* random variable if the probability of every
single point is zero: P(X = a) = 0 for every real a.

This is not a technicality. It follows from countable additivity: if
P(X = a) = 0, then the point has zero width, so its area under any curve is
zero. The consequence is that intervals get positive probability even though
each point in them does not — the same way a line has length but no area.

**Definition.** X has a *probability density function* (PDF) f_X(x) if

    P(a ≤ X ≤ b) = ∫ₐᵇ f_X(x) dx

for all a, b, where f_X(x) ≥ 0 and ∫_{−∞}^{∞} f_X(x)dx = 1.

**Density is not probability.** Three consequences, all of which surprise people:

1. **f_X(x) can exceed 1.** A density is probability per unit width. A normal with
   σ = 0.5 has a peak of about 0.798, and shrinking σ to 0.1 pushes the peak to
   about 3.99 — perfectly legal, because the *area* is still 1.
2. **f_X(x) is not P(X = x)**, and there is no value of x for which it is that.
3. **Density comparisons are width-dependent.** Two densities can agree about
   "which is bigger at this point" and disagree about which region is more
   likely, because one region may be wider. Comparing PDFs at a point tells you
   nothing about which is more likely overall.

**Theorem (the CDF is the safest tool).** For continuous X,

    P(a ≤ X ≤ b) = F_X(b) − F_X(a)

where F_X(x) = P(X ≤ x) = ∫_{−∞}^x f_X(t)dt. Note that ≤ and < are
interchangeable for continuous variables, since the boundary points have
probability zero. That is why "P(X ≤ x)" and "P(X < x)" are the same number for
continuous X and *different* numbers for discrete X — the single most common
source of off-by-one errors when switching between worlds.

**Definition.** X is *uniform* on [a, b], written X ~ Uniform(a, b), when

    f_X(x) = 1/(b − a) for a ≤ x ≤ b, and 0 otherwise

with E[X] = (a+b)/2 and Var(X) = (b−a)²/12.

**Definition.** X is *exponential* with rate λ > 0, written X ~ Exp(λ), when

    f_X(x) = λe^(−λx) for x ≥ 0,   F_X(x) = 1 − e^(−λx)

with E[X] = 1/λ and Var(X) = 1/λ². The parameter λ is a *rate*, so **larger λ
means faster**. The mean is 1/λ, so λ = 1/mean. This trips people up constantly:
λ is not the mean, and setting "λ = 100" does not give a mean of 100.

**Theorem (memorylessness).** If X ~ Exp(λ) and s, t ≥ 0, then

    P(X > s + t | X > s) = P(X > t)

**Proof.** Using the survival function:

    P(X > s+t | X > s) = P(X > s+t)/P(X > s) = e^(−λ(s+t))/e^(−λs) = e^(−λt)

which equals P(X > t). ∎

**Explanation.** Conditional on having already survived s, the residual waiting
time is a fresh Exp(λ). The process carries no memory of how long you have
waited. This is a statement about the distribution, not about the mechanism — it
holds exactly for the exponential and approximately for real systems that are
roughly stationary.

**Definition.** X is *normal* (Gaussian) with mean μ and variance σ², written
X ~ N(μ, σ²), when

    f_X(x) = (1 / (σ√(2π))) · e^(−(x−μ)²/(2σ²))

with E[X] = μ and Var(X) = σ². The CDF has no closed form in elementary
functions, but Python's `math.erf` gives it exactly:

    F_X(x) = (1 + erf((x − μ)/(σ√2))) / 2

The bell curve's most useful property is the **68-95-99.7 rule**: about 68% of
the mass lies within one standard deviation of the mean, 95% within two, 99.7%
within three.

## Worked Example

### Example A — the normal distribution, computed from scratch

Let X ~ N(100, 5²): a measurement centred at 100 with standard deviation 5.

**Step 1 — the density function.** f(x) = (1/(5√(2π)))·e^(−(x−100)²/50).
The prefactor is 1/(5 × 2.506628) = 0.079788. The exponent term is
e^(−(x−100)²/(2·25)) = e^(−(x−100)²/50).

At x = 100 the density is 0.079788 per unit. At x = 105 it is
0.079788·e^(−0.5) = 0.048394. At x = 110 it is 0.079788·e^(−2) = 0.010790.

**Step 2 — the CDF.** F(x) = (1 + erf((x−100)/(5√2)))/2.

    F(100) = 0.5                    by symmetry
    F(105) = 0.8413447              the classic 84.13th percentile
    F(110) = 0.9772499
    F(95)  = 0.1586553
    F(90)  = 0.0227501

Note F(90) = 1 − F(110) = 0.0227501. That symmetry identity is worth
remembering: F(μ + a) = 1 − F(μ − a).

**Step 3 — the 68-95-99.7 rule, verified.** Compute the probability of lying
within k standard deviations of the mean:

    k=1: F(105) − F(95) = 0.8413447 − 0.1586553 = 0.682689
    k=2: F(110) − F(90) = 0.9772499 − 0.0227501 = 0.954500
    k=3: F(115) − F(85) = 0.9986501 − 0.0013499 = 0.997300

So 68.27%, 95.45%, and 99.73%. Those are the real numbers, not the rounded
"68/95/99.7" of the rule of thumb. The rule is memorable precisely because the
true values are so close to those round figures.

**Step 4 — a real question.** "What fraction of measurements exceed 112?"

    P(X > 112) = 1 − F(112) = 1 − 0.9918018 = 0.0081982

About 0.82%, or roughly 1 in 122 requests. If a threshold is set at 112 ms then
about 1 in 122 requests will exceed it — which is the arithmetic behind an SLO.

**Step 5 — invert it, which is what monitoring actually needs.** "What value do I
set so that only 1% of requests exceed it?" This is the quantile function, and
it requires inverting F, which for the normal means searching numerically:

    find x with 1 − F(x) = 0.01  ->  x = 100 + 2.3263479 × 5 = 111.6317

So the 99th percentile is about 111.63 ms. The code below gets this by binary
search on F, which is exactly how a quantile function works, and it reproduces
the other standard figures too: the 90th percentile is 106.41 ms and the 95th is
108.22 ms.

### Example B — the exponential distribution and memorylessness

Let T ~ Exp(λ) with λ = 0.5, so the mean waiting time is 1/0.5 = 2 seconds.

**Step 1 — the survival function.** P(T > t) = e^(−λt) = e^(−0.5t).

    t=0:   1.000000
    t=1:   0.606531
    t=2:   0.367879
    t=3:   0.223130
    t=4:   0.135335
    t=6:   0.049787

**Step 2 — the median.** Set P(T > m) = 0.5: e^(−0.5m) = 0.5, so
−0.5m = ln(0.5) = −0.693147, giving m = ln(2)/0.5 = 1.386294 seconds. The
median (1.386) is
well below the mean (2.0) because the distribution is right-skewed — the long tail
pulls the mean up. This is the concrete demonstration of the mistake in
[Lesson 63](63_discrete_random_variables.md): for a skewed distribution, the
mean is not a typical value.

**Step 3 — memorylessness, computed.** Using the numbers above:

    P(T > 5 | T > 2) = P(T > 5)/P(T > 2) = e^(−0.5·5)/e^(−0.5·2)
                    = e^(−2.5)/e^(−1.0)
                    = 0.0820850/0.367879
                    = 0.223130

And P(T > 3) = e^(−1.5) = 0.223130. **Identical.** Having already waited 2
seconds, the chance of waiting more than 3 *further* seconds is exactly the same
as the chance of waiting more than 3 seconds from the start. The distribution
genuinely has no memory.

**Step 4 — why this matters.** If you have already waited 5 seconds for a
callback, the exponential model says the expected *remaining* wait is still
1/λ. This is why exponential distributions appear in queues, in retry logic, and
in timeouts. It is also why "wait 3 seconds, then give up" and "wait until the
total is 3 seconds" behave identically under this model — a fact you can exploit
but should be suspicious of in a real system, since real systems drift.

### Example C — integrating a density numerically

Real distributions rarely have a closed-form integral. Here is a probability
computed by two different numerical methods and cross-checked against the exact
value.

For X ~ Uniform(1, 5), find P(2 ≤ X ≤ 4).

**Exactly:** the density is 1/4 on [1,5], so the area from 2 to 4 is
(4 − 2)/4 = 0.5.

**By numerical integration**, applying Simpson's rule on a fine grid: the density
is constant, so the approximation is exact to floating point — it returns
0.5000000000.

**By Monte Carlo**, the trick from [Lesson 60](60_probability_foundations.md):
sample uniformly from a wide window and count the fraction landing in the region
of interest. Sampling over [0, 6] and asking what fraction falls in [2, 4] gives
roughly 0.333, which is the area ratio 2/6 — exactly what we want, since we want
the probability of [2,4] *relative to the whole window*, and the density is
constant. The value wanders a little from run to run, which is the point: Monte
Carlo is approximate and its error shrinks like 1/√n, whereas numerical quadrature
of a smooth known integrand is far more accurate. Use Monte Carlo when you cannot
integrate analytically, not when you can.

## Runnable Code

### Density is not probability

```python
from math import exp, sqrt, pi, erf

# A normal density with a TINY standard deviation has a peak far above 1.
# This is legal: the AREA is 1, not the height.
sigma = 0.1
mu = 0.0
peak = 1 / (sigma * sqrt(2 * pi))
print(f"N(0, {sigma}^2) peak density = {peak:.6f}")
print("A density is probability PER UNIT WIDTH, so it may exceed 1.")
print()

# Show the area is 1 anyway, by integrating numerically.
def normal_pdf(x, mu, sigma):
    return 1 / (sigma * sqrt(2 * pi)) * exp(-((x - mu) ** 2) / (2 * sigma**2))


def simpson(f, lo, hi, n=200000):
    """Simpson's rule. For this smooth integrand it is accurate to ~1e-15."""
    h = (hi - lo) / n
    total = f(lo) + f(hi)
    for i in range(1, n):
        total += f(lo + i * h) * (4 if i % 2 else 2)
    return total * h / 3


area = simpson(lambda x: normal_pdf(x, 0.0, sigma), -1.0, 1.0)
print(f"integrating the PDF over [-1, 1]: {area:.10f}   <- still 1.0")
print()
print(f"peak density when sigma=5.0:  {1 / (5 * sqrt(2 * pi)):.6f}")
print(f"peak density when sigma=0.1:  {1 / (0.1 * sqrt(2 * pi)):.6f}")
print(f"peak density when sigma=0.01: {1 / (0.01 * sqrt(2 * pi)):.6f}")
print("-> no upper bound on a density, as long as the total area is 1.")
```

### The normal CDF, quantiles, and the 68-95-99.7 rule

```python
from math import erf, sqrt, exp, pi

MU, SIGMA = 100.0, 5.0


def normal_cdf(x, mu=MU, sigma=SIGMA):
    """P(X <= x) using math.erf -- the exact closed form."""
    return (1.0 + erf((x - mu) / (sigma * sqrt(2.0)))) / 2.0


def pdf(x, mu=MU, sigma=SIGMA):
    """The normal density function."""
    return 1 / (sigma * sqrt(2 * pi)) * exp(-((x - mu) ** 2) / (2 * sigma**2))


print(f"N({MU}, {SIGMA}^2) -- density and CDF at several points")
print("  x   | density   | F(x)      | P(X > x)")
for x in (85, 90, 95, 100, 105, 110, 115):
    print(f"{x:4d} | {pdf(x):.6f}  | {normal_cdf(x):.6f}  | {1 - normal_cdf(x):.6f}")

print()
print("symmetry check F(90) + F(110) =",
      f"{normal_cdf(90) + normal_cdf(110):.10f}")

print()
print("the 68-95-99.7 rule, computed exactly:")
for k in (1, 2, 3):
    lo, hi = MU - k * SIGMA, MU + k * SIGMA
    p = normal_cdf(hi) - normal_cdf(lo)
    print(f"  within {k} sd [{lo:.0f}, {hi:.0f}]: {p * 100:.4f}%")

print()
print("a real question: P(X > 112) =", f"{1 - normal_cdf(112):.6f}")
print(f"  about 1 in {1 / (1 - normal_cdf(112)):.0f} requests")

print()
# Inverting the CDF by bisection -- this is what a quantile function does.
def normal_quantile(q, mu=MU, sigma=SIGMA):
    """Smallest x with normal_cdf(x) >= q."""
    lo, hi = mu - 40 * sigma, mu + 40 * sigma
    for _ in range(200):
        mid = (lo + hi) / 2
        if normal_cdf(mid, mu, sigma) < q:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


for q in (0.5, 0.9, 0.95, 0.99, 0.999):
    x = normal_quantile(q)
    print(f"  {q * 100:6.3f}th percentile = {x:7.3f}   "
          f"(verified F = {normal_cdf(x):.6f})")
```

### Uniform and exponential, and the memoryless property

```python
from math import exp, log, sqrt

# --- Uniform(1, 5) ---
A, B = 1.0, 5.0


def uniform_pdf(x, a=A, b=B):
    return 1 / (b - a) if a <= x <= b else 0.0


def uniform_cdf(x, a=A, b=B):
    return 0.0 if x < a else (1.0 if x >= b else (x - a) / (b - a))


print(f"Uniform({A}, {B}):")
print(f"  E[X]   = {(A + B) / 2:.6f}   (the midpoint)")
print(f"  Var(X) = {(B - A) ** 2 / 12:.6f}   sd = {sqrt((B - A) ** 2 / 12):.6f}")
print(f"  P(2 <= X <= 4) exactly = {uniform_cdf(4) - uniform_cdf(2):.6f}")
print("  P(2 <= X <= 4) = (4 - 2)/(5 - 1) -- the width ratio")
print()

# --- Exponential(rate) ---
LAMBDA = 0.5


def exp_surv(t, lam=LAMBDA):
    """P(T > t) = e^(-lambda t). Simpler and safer than the CDF."""
    return exp(-lam * t)


def exp_mean(lam=LAMBDA):
    return 1 / lam


print(f"Exponential(rate={LAMBDA}):")
print(f"  E[T]   = 1/lambda = {exp_mean():.6f}   Var = {1 / LAMBDA ** 2:.6f}")
print(f"  NOTE: lambda = {LAMBDA} is a RATE, not a mean.")
print(f"  lambda=0.5 -> mean {exp_mean(0.5):.2f},  lambda=2.0 -> mean {exp_mean(2.0):.2f}")
print()
print("  t   | P(T > t)  | P(T <= t)")
for t in (0, 1, 2, 3, 4, 6):
    print(f"{t:5d} | {exp_surv(t):.6f}  | {1 - exp_surv(t):.6f}")

print()
median = -log(0.5) / LAMBDA
print(f"  median = ln(2)/lambda = {median:.6f}  (well BELOW the mean "
      f"{exp_mean():.2f})")
print("  -> right-skewed: the long tail drags the mean up. Report the median.")
print()

# --- memorylessness, demonstrated numerically ---
S, T = 2.0, 3.0
conditional = exp_surv(S + T) / exp_surv(S)
marginal = exp_surv(T)
print("memorylessness: P(T > s+t | T > s) == P(T > t)")
print(f"  P(T > {S + T} | T > {S}) = {exp_surv(S + T):.6f} / {exp_surv(S):.6f} "
      f"= {conditional:.6f}")
print(f"  P(T > {T})                        = {marginal:.6f}")
print(f"  identical: {abs(conditional - marginal) < 1e-12}")
print()
print("  Check several (s, t) pairs:")
for s in (0.5, 1.0, 4.0):
    for t in (0.5, 2.0, 7.0):
        lhs = exp_surv(s + t) / exp_surv(s)
        rhs = exp_surv(t)
        if abs(lhs - rhs) > 1e-12:
            print("    MISMATCH", s, t, lhs, rhs)
print("    all match to machine precision")
```

### Numerical integration and Monte Carlo, cross-checked

```python
import random
from math import exp, sqrt, pi, erf

rng = random.Random(2024)


def simpson(f, lo, hi, n=100000):
    """Simpson's rule: (h/3) * (f0 + 4*f1 + 2*f2 + ... + fn)."""
    h = (hi - lo) / n
    total = f(lo) + f(hi)
    for i in range(1, n):
        total += f(lo + i * h) * (4 if i % 2 else 2)
    return total * h / 3


def midpoint(f, lo, hi, n=100000):
    """The simplest possible rule: sample the middle of each slab."""
    h = (hi - lo) / n
    return sum(f(lo + (i + 0.5) * h) for i in range(n)) * h


# P(2 <= X <= 4) for Uniform(1, 5): exactly 0.5 by hand.
uniform = lambda x: 1 / 4 if 1 <= x <= 5 else 0.0
exact = 0.5
print(f"exact                       : {exact:.10f}")
print(f"Simpson's rule              : {simpson(uniform, 2, 4):.10f}")
print(f"midpoint rule               : {midpoint(uniform, 2, 4):.10f}")

# Monte Carlo: the probability is the AREA ratio. Sample uniformly over a
# wide window [0, 6] and count what fraction lands in [2, 4].
n = 400_000
hits = sum(1 for _ in range(n) if 2.0 <= rng.uniform(0.0, 6.0) <= 4.0)
mc = hits / n
print(f"Monte Carlo ({n:,} samples over [0,6], fraction in [2,4]): {mc:.6f}")
print("  -> the Monte Carlo estimate of an AREA is the fraction of samples")
print("     inside the region times the window width, or equivalently here")
print("     the fraction, because we only want the ratio.")
print()

# A case with a curved integrand and no trivial hand answer: the upper tail
# of a normal, integrated numerically and checked against the erf formula.
def normal_pdf(x, mu, sigma):
    return 1 / (sigma * sqrt(2 * pi)) * exp(-((x - mu) ** 2) / (2 * sigma**2))


lo, hi = 112.0, 200.0
num = simpson(lambda x: normal_pdf(x, 100.0, 5.0), lo, hi)
ana = 1 - (1 + erf((112 - 100) / (5 * sqrt(2)))) / 2
print("P(X > 112) for N(100, 5^2)")
print(f"  by numerical integration : {num:.8f}")
print(f"  by the erf formula       : {ana:.8f}")
print(f"  agreement within 1e-6    : {abs(num - ana) < 1e-6}")
print()
print("Note the integration ran to +infinity in principle; 200 is 20 sd")
print("above the mean, so the tail beyond it is about 1e-88 and irrelevant.")
```

## Common Mistakes

**Mistake 1 — reading a PDF value as a probability.**
Wrong: "the normal density at 100 is 0.0798, so there's a 7.98% chance the value
is 100." Right: P(X = 100) = 0 exactly, for every continuous variable. The number
0.0798 is probability *per millisecond near 100*. The correct reading is that
roughly 7.98% of the mass lies within one millisecond of 100. The temptation is
strong because for discrete variables p_X(x) *is* P(X = x), and the notation is
nearly identical.

**Mistake 2 — integrating the density over the wrong interval.**
Wrong: "P(X ≤ 100) = ∫_{−∞}^{100} f." Right: that integral *is* P(X ≤ 100), so
this one is right, but the common error is using F(a) − F(b) instead of F(b) −
F(a), or forgetting that you want the *area*, not the height. Also, "P(X > x) =
F(x)" is wrong; it is 1 − F(x).

**Mistake 3 — using ≤ and < interchangeably.**
For discrete X, P(X ≤ 3) and P(X < 3) differ by p(3), which is often large. For
continuous X they are equal. Code that mixes the two silently shifts results when
you move between integer counts and real-valued measurements. This is a genuine
source of off-by-one bugs in quantile computations.

**Mistake 4 — treating λ as the mean of an exponential.**
Wrong: "Exponential(100) has a mean of 100." Right: mean = 1/λ, so
Exponential(100) has mean 0.01. The parameter is a rate because the density is
λe^(−λx) — it describes how fast the survival function decays. This is the single
most common parameterisation bug, and it is invisible until the numbers come out
100× off.

**Mistake 5 — believing a normal distribution because data looks normal.**
Normal data has no sharp cutoffs and a symmetric tail. Latency data, file sizes,
and request counts are right-skewed with hard floors at zero. Fitting a normal to
them produces sensible-looking means and badly wrong percentiles — which is
precisely what an SLO depends on. If the tail matters, model the tail: log-normal,
gamma, or a mixture.

## Formula Sheet

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$P(X = a)$` | `$= 0$` for every real a | **The defining fact of continuity.** A single point has zero width, so it has zero area and zero probability. | Anything where "the exact value" is asked. Intervals get positive probability; points never do. |
| `$f_X(x)$` | `$P(a \le X \le b) = \int_a^b f_X(x)\,dx$` | **PDF**: probability *per unit width* over a range. | Only via integration. Never read as a probability at a point. |
| PDF conditions | `$f_X(x) \ge 0$` and `$\int_{-\infty}^{\infty} f_X(x)\,dx = 1$` | Nonnegative, total area 1. These two conditions define the distribution completely, exactly as a PMF does. | Validation. If a proposed density integrates to 1.2, it is not a density. |
| `$f_X(x)$` | can be `> 1` | **A density is not a probability.** `N(0, 0.1²)` peaks at 3.989; `N(0, 0.01²)` peaks at 39.894. Legal, because only the *area* is constrained. | Any time you wonder whether a number above 1 is a bug. It usually is not. |
| `$F_X(x)$` | `$= P(X \le x) = \int_{-\infty}^{x} f_X(t)\,dt$` | **CDF**, the safe tool. Answers interval questions with no integration. | Every threshold and SLO question. |
| `$P(a \le X \le b)$` | `$= F_X(b) - F_X(a)$` | Subtract CDF values, larger first. | The main computational move in this lesson. |
| `$F_X(b)$ vs `$F_X(a)$` | `$P(X > x) = 1 - F_X(x)$ | **never** `$F_X(x)$` | Upper tails. The most common sign error with densities. |
| `$P(X \le x) = P(X < x)$` | for continuous X only | Boundary points have probability zero, so the distinction vanishes. | Switching between discrete and continuous code — a genuine off-by-one source (Mistake 3). |
| `$X \sim \mathrm{Uniform}(a,b)$` | `$f_X(x) = \dfrac{1}{b-a}$` on $[a,b]$, needs $a < b$ | Flat density; probability is a **width ratio**. | Monte Carlo integration, random jitter, sampling inside an interval. |
| `Uniform` moments | `$E[X] = \dfrac{a+b}{2}$`, `$\mathrm{Var}(X) = \dfrac{(b-a)^2}{12}$` | Midpoint mean; variance from the width alone. | `Uniform(1,5)`: mean 3, variance 16/12 = 1.3333, sd 1.1547. |
| `$X \sim \mathrm{Exp}(\lambda)$` | `$f_X(x) = \lambda e^{-\lambda x}$` for `x \ge 0` | **Waiting time** to an event happening at constant rate. | Arrival gaps, time to first failure, retry timing, queueing. |
| `\lambda` | `> 0`, a **rate** | Larger λ means *faster*. It is the reciprocal of the mean, **not** the mean. | The single most common parameterisation bug: `Exp(100)` has mean 0.01. |
| `$E[X]$`, `$\mathrm{Var}(X)$` for Exp | `$1/\lambda$`, `$1/\lambda^2$` | Mean is the reciprocal of the rate; sd equals the mean. | Converting between "one event every 4 s" and λ. |
| survival function | `$P(T > t) = 1 - F_T(t) = e^{-\lambda t}$` | **Simpler than the CDF** for the exponential — one `exp`, no branching. | Tail probabilities, timeouts, retry budgets. `Exp(0.5)`: 0.367879 at t = 2. |
| **memorylessness** | `$P(X > s+t \mid X > s) = P(X > t)$` | Having already waited s, the residual wait is a fresh draw. | Why timeout-and-retry ladders behave as they do. Holds *exactly* for Exp, only approximately for real systems. |
| median of Exp | `$\ln 2 / \lambda$ | **Median $\ln 2/\lambda = 1.3863$ against mean 2** at λ = 0.5. | The right-skew demonstration: the mean is not a typical value. |
| `$X \sim \mathcal{N}(\mu,\sigma^2)$` | `$f_X(x) = \dfrac{1}{\sigma\sqrt{2\pi}} e^{-\dfrac{(x-\mu)^2}{2\sigma^2}}$` | The bell curve, parameterised by mean and variance. | Averaging many things ([Lesson 68](68_law_of_large_numbers_and_clt.md)), measurement error, and anything approximately normal. |
| normal CDF | `$F_X(x) = \dfrac{1 + \mathrm{erf}\!\left(\dfrac{x-\mu}{\sigma\sqrt{2}}\right)}{2}$` | Exact closed form via `math.erf`. No elementary formula otherwise. | Any normal probability. `N(100,5²)`: F(105) = 0.8413447, F(112) = 0.9918025. |
| quantile | `$F^{-1}(q)$ | "What value do I set so only $(1-q)$ exceed it?" | SLO thresholds. By **bisection**, since no elementary inverse exists. `N(100,5²)`: 99th percentile = 111.632. |
| `$Z = \dfrac{X-\mu}{\sigma}$` | `$\sim \mathcal{N}(0,1)$` | Standardisation: absorbs μ and σ entirely, leaving a parameter-free law. | Every z-score, every two-sided comparison. F_Z(1.96) = 0.9750. |
| 68-95-99.7 rule | `$k=1: 0.6827`, `$k=2: 0.9545`, `$k=3: 0.9973$ | The mass within k standard deviations of the mean. | Sanity checks and back-of-envelope SLOs — accurate to about 0.2%. |
| Simpson's rule | `$\dfrac{h}{3}\big(f_0 + 4f_1 + 2f_2 + \cdots + f_n\big)$` | Numerical integration of a smooth density. | No closed form. Accurate to ~1e-15 for these integrands. |
| Monte Carlo area | `$\dfrac{\text{fraction of samples in the region}}{\text{fraction in the window}}$` | Probability as an area *ratio*, estimated by sampling. | When you cannot integrate. Error shrinks like $1/\sqrt{n}$ — much worse than quadrature. |
| "mean ± 2 sd as an SLO" | — | **Not valid for bimodal or hard-bounded data.** For the 1 ms / 50 ms mixture it gives [−23.5, 35.3] while 10% of requests take 50 ms. | A warning. Decompose modes before fitting (Exercise 3). |

## Multiple Choice Questions

**Q1.** A measurement $X \sim \mathcal{N}(0, 0.1^2)$ has density 3.989 at $x = 0$.
What is the correct reading of that number?

- A) A 398.9% chance that $X = 0$
- B) Probability per unit width near 0; the mass within roughly 0.05 of 0 is about 0.2
- C) The probability that $X$ exceeds 0
- D) An error, since a probability cannot exceed 1

<details>
<summary>Answer and explanation</summary>

**B) Probability per unit width near 0; the mass within roughly 0.05 of 0 is about
0.2.**

This is the lesson's central point and Mistake 1. Option A is the reading the
notation invites and the answer to every one of them is wrong: $P(X = 0) = 0$
exactly. Option C is not what a density at a point means in any case. Option D
confuses the density with a probability; the constraint is on the *integral*,
which is 1, and the code block integrates the density over [−1, 1] and gets
1.0000000000.

</details>

**Q2.** For continuous $X$, why is $P(X \le 3)$ equal to $P(X < 3)$?

- A) Because $P(X = 3) = 0$ and the two events differ by exactly that point
- B) Because continuous variables are symmetric
- C) Because $F(3) = 0.5$ for every continuous distribution
- D) Because integration ignores endpoints

<details>
<summary>Answer and explanation</summary>

**A) Because $P(X = 3) = 0$ and the two events differ by exactly that point.**

$\{X \le 3\} = \{X < 3\} \cup \{X = 3\}$ is a disjoint union, so additivity gives
$F(3) = P(X<3) + 0$. Option B is a property of *normal* distributions, not of
continuity. Option C is false for every continuous distribution except the
symmetric-about-3 ones, and even then only at that one point. Option D is a
statement about the *mechanism* (Riemann and Lebesgue integration agree on
endpoints) rather than the reason the probabilities are equal — the reason is
that the point has zero probability.

</details>

**Q3.** $X \sim \mathrm{Exp}(\lambda)$ has mean 4 seconds. What is $\lambda$, and
what is the 90th percentile?

- A) $\lambda = 4$ and the 90th percentile is 4 seconds
- B) $\lambda = 0.25$ and the 90th percentile is $\ln 10 / 0.25 = 9.2103$ seconds
- C) $\lambda = 0.25$ and the 90th percentile is $4 / 0.9 = 4.44$ seconds
- D) $\lambda = 2.5$ and the 90th percentile is 9.2103 seconds

<details>
<summary>Answer and explanation</summary>

**B) $\lambda = 0.25$ and the 90th percentile is $\ln 10 / 0.25 = 9.2103$
seconds.**

This is Exercise 2 in this lesson. Option A is Mistake 4: the parameter is a
rate, so $\lambda = 1/\text{mean}$. Option C tries to scale the mean linearly,
which is what a symmetric distribution would allow — the exponential has no such
symmetry, its median is $\ln 2/\lambda = 2.77$ and its mean is 4. Option D has
the rate inverted ($1/0.4$), which would give a mean of 0.4 s.

</details>

**Q4.** Why does the exponential distribution satisfy
$P(T > s + t \mid T > s) = P(T > t)$?

- A) Because the mean and variance of an exponential are equal
- B) Because the survival function factorises: $e^{-\lambda(s+t)}/e^{-\lambda s} = e^{-\lambda t}$, with the s cancelling
- C) Because conditional probabilities always ignore earlier events
- D) Because exponentials are normal

<details>
<summary>Answer and explanation</summary>

**B) Because the survival function factorises:
$e^{-\lambda(s+t)}/e^{-\lambda s} = e^{-\lambda t}$, with the s cancelling.**

This is the whole proof, and the lesson's Example B verifies it numerically at
s = 2, t = 3. Option A is a numerical curiosity ($E[X] = \sigma$ for Exp) with no
bearing on memorylessness. Option C is false in general — conditioning on an
event usually changes the answer; it happens not to here for a structural reason.
Option D is nonsense; the exponential is right-skewed and the normal is not.

</details>

**Q5.** Which of these is a valid density for $X \sim \mathrm{Uniform}(1,5)$?

- A) $f(x) = 1/4$ for $1 \le x \le 5$, 0 otherwise
- B) $f(x) = 1/5$ for $1 \le x \le 5$, 0 otherwise
- C) $f(x) = 4$ for $1 \le x \le 5$, 0 otherwise
- D) $f(x) = 1/4$ for all real x

<details>
<summary>Answer and explanation</summary>

**A) $f(x) = 1/4$ for $1 \le x \le 5$, 0 otherwise.**

The area must be 1, and a rectangle of width 4 needs height 1/4. Option B has
total area $4 \times 0.2 = 0.8$, so it under-counts — every probability from it
would be 20% low. Option C has area 16. Option D has infinite area, so it is not
normalisable at all. This is the cheapest density check there is: multiply height
by width.

</details>

**Q6.** $X \sim \mathcal{N}(100, 5^2)$. What is $P(X > 112)$?

- A) $1 - F(112) \approx 0.0082$, so about 1 in 122 requests
- B) $F(112) \approx 0.9918$, so about 99% of requests exceed 112
- C) $0.0082 \times 5 = 0.041$, scaling by the standard deviation
- D) $0.0082 / 100 = 0.000082$, scaling by the mean

<details>
<summary>Answer and explanation</summary>

**A) $1 - F(112) \approx 0.0082$, so about 1 in 122 requests.**

$F(112) = 0.9918025$, so the upper tail is $0.0081975$. Option B is the
sign error in Mistake 2: $F$ is a *lower*-tail probability. Options C and D
multiply or divide by parameters that have nothing to do with it. Note the
standardisation: $(112-100)/5 = 2.4$, so this is a 2.4-sigma upper tail.

</details>

**Q7.** Why is `mean ± 2 sd` a poor SLO rule for latency data?

- A) Because the 68-95-99.7 rule applies only to normals, and latency is not normal
- B) Because it can produce physically impossible bounds and contradict the actual mass: for the 1 ms / 50 ms mixture it gives [−23.5, 35.3] while 10% of requests take 50 ms
- C) Because 2 sd is too wide; 1 sd is correct
- D) Because sd must be added, not multiplied

<details>
<summary>Answer and explanation</summary>

**B) Because it can produce physically impossible bounds and contradict the actual
mass: for the 1 ms / 50 ms mixture it gives [−23.5, 35.3] while 10% of requests
take 50 ms.**

Exercise 3 works this through. Option A is related but weaker — the problem is not
merely non-normality, it is that a symmetric interval cannot describe a bimodal
distribution with an atom at 50. Option C makes it worse, since 1 sd would claim
68% within a window that excludes 10% of the mass entirely. Option D is a units
error; you always multiply by sd.

</details>

**Q8.** Why is Monte Carlo integration a poor choice when you have a smooth
density and no closed-form CDF?

- A) Monte Carlo cannot integrate at all
- B) Its error shrinks like $1/\sqrt{n}$, so you need roughly a million samples to match numerical quadrature's accuracy on a $10^{-15}$ target
- C) Monte Carlo requires the integrand to be non-negative
- D) Monte Carlo is exact only for polynomials

<details>
<summary>Answer and explanation</summary>

**B) Its error shrinks like $1/\sqrt{n}$, so you need roughly a million samples
to match numerical quadrature's accuracy on a $10^{-15}$ target.**

The lesson's code makes the comparison: Simpson's rule returns 0.5000000000 for
the uniform case, while 400,000 Monte Carlo samples give something like 0.333
with visible run-to-run wobble. Option A is false; it is precisely how
Monte Carlo integration works ([Lesson 70](70_information_theory_entropy.md)
uses it). Option C is wrong; non-negativity is a requirement of the *density*,
not a limitation of the method. Option D is not a real property.

</details>

**Q9.** Which real-world process is the exponential distribution the natural model
for?

- A) The number of successes in 100 independent requests
- B) The time until the next event in a stream where events arrive independently at a constant rate
- C) A measurement with bell-shaped error
- D) The number of retries until a first success

<details>
<summary>Answer and explanation</summary>

**B) The time until the next event in a stream where events arrive independently
at a constant rate.**

Inter-arrival gaps in Poisson traffic, time to first failure on a component, and
gap between retries all satisfy this, which is why the exponential appears in
queues and timeout logic. Option A is Binomial
([Lesson 63](63_discrete_random_variables.md)). Option C is normal. Option D is
Geometric, the *discrete* memoryless distribution — the right shape, but counted
in trials rather than measured in time, and introduced in
[Lesson 66](66_common_distributions.md).

</details>

**Q10.** A normal is fitted to latency data that has a hard floor at zero and a
long right tail. What goes wrong, and in which direction?

- A) Nothing much — the mean and sd still fit well
- B) The fitted percentiles are badly wrong precisely in the tail that SLOs depend on, because a normal places unbounded mass at negative latencies and smooths away the tail structure
- C) The fit fails to converge
- D) A normal cannot be fitted to any data with a point mass

<details>
<summary>Answer and explanation</summary>

**B) The fitted percentiles are badly wrong precisely in the tail that SLOs
depend on, because a normal places unbounded mass at negative latencies and
smooths away the tail structure.**

This is Mistake 5 in the lesson, and Exercise 3 shows the inversion: the fitted
normal puts 39.0% beyond 10 ms where the truth is 10.0%. Option A is the
dangerous belief — the mean and sd *are* matched exactly, which is precisely why
the error hides. Option C is false; the fit converges fine to the wrong
conclusion. Option D is false; Exercise 3's own distribution has atoms and is
still mis-fitted by a normal, not un-fittable.

</details>

## Subjective Questions

### Short Answer

**Q1. Define a continuous random variable, and say what forces the definition.**

<details>
<summary>Answer</summary>

$X$ is continuous if $P(X = a) = 0$ for every real $a$. What forces it is
countable additivity combined with the fact that a point has zero width: a point
contributes zero area under any curve, so its probability must be 0. The
consequence that matters in practice is that intervals get positive probability
even though no point inside them does — the same way a line has length but no
area.

</details>

**Q2. State the two conditions that make a function a valid PDF.**

<details>
<summary>Answer</summary>

$f_X(x) \ge 0$ for all $x$, and $\int_{-\infty}^{\infty} f_X(x)\,dx = 1$. These
play exactly the role the two PMF conditions play in
[Lesson 63](63_discrete_random_variables.md): they determine the distribution
completely, and nothing else does. Note what is *not* required — $f_X(x) \le 1$
nowhere appears, and that omission is what makes Q1's surprise possible.

</details>

**Q3. Why can a density exceed 1? Explain in one sentence.**

<details>
<summary>Answer</summary>

Because a density is probability *per unit width*, not probability: the value
$\int_{a}^{b} f_X(x)\,dx$ is the probability, and it is the integral that equals
1. A tall narrow density is exactly how you represent a distribution concentrated
in a small interval — $\mathrm{N}(0, 0.01^2)$ peaks at 39.894 and still integrates
to 1.

</details>

**Q4.** A system has mean latency 100 ms and sd 5 ms, both taken from a normal
fit. What is the fitted 99th percentile, and what does the code's bisection
approach have to do with it?

<details>
<summary>Answer</summary>

$F^{-1}(0.99)$ for $\mathrm{N}(100, 5^2)$ is $100 + 2.3263479 \times 5 =
111.632$ ms. The bisection matters because the normal CDF has no elementary
inverse: you bracket, test the midpoint, and halve. The lesson's
`normal_quantile` does this in 200 iterations over a range of $\pm 40\sigma$,
which is more than enough since 40 sigma is past floating-point resolution.

</details>

**Q5.** Give the mean, median, and standard deviation of $X \sim \mathrm{Exp}(0.5)$.

<details>
<summary>Answer</summary>

Mean $= 1/\lambda = 2$ seconds. Median $= \ln 2 / \lambda = 1.3863$ seconds.
Standard deviation $= 1/\lambda = 2$ seconds — for the exponential the standard
deviation always equals the mean. The median sitting 31% below the mean is the
concrete demonstration that the mean is not a typical value for a right-skewed
distribution.

</details>

**Q6.** For $X \sim \mathrm{Uniform}(a,b)$, state the probability of any interval
$[c,d] \subseteq [a,b]$, the mean, and the variance.

<details>
<summary>Answer</summary>

$P(c \le X \le d) = (d-c)/(b-a)$ — a **width ratio**, since the density is the
constant $1/(b-a)$. Mean $=(a+b)/2$, the midpoint. Variance $=(b-a)^2/12$, so
sd $= (b-a)/\sqrt{12}$. Note the variance depends on the width alone and not on
where the interval sits.

</details>

### Long Answer

**Q1. Why can a density value not be a probability, and what would break if you
treated it as one?**

<details>
<summary>Model answer</summary>

Because they measure different things. $p_X(x) = P(X = x)$ is the mass on a
single value, and for continuous $X$ that mass is 0. $f_X(x)$ is a *rate*: how much
probability sits in a neighbourhood of width $dx$ around $x$. The conversion is
$\int_a^b f_X(x)\,dx$, an integral, not a lookup. There is no value of $x$ at which
the two coincide, because the left side is 0 everywhere for a continuous variable.

Reading the density as a probability fails in a specific and dangerous way: it
always *underestimates* heavily-tailed behaviour, because the omitted factor is
the width of the region you actually care about. For the 1 ms / 50 ms mixture,
the mass beyond 10 ms is 0.1, while the density at 10 ms is 0 — so a
density-driven reading reports *no* tail at all, not merely a wrong one.

It also breaks in the other direction on narrow distributions, where the peak can
be far above 1. $\mathrm{N}(0, 0.01^2)$ has a peak of 39.894. If any downstream
code validates `probability <= 1`, it rejects a perfectly correct model. The
defence is to check the *integral*, not the height: integrate the density and
confirm you get 1, exactly as the lesson's first code block does over [−1, 1].

The general habit this installs: for a continuous quantity, every question should
be phrased as an interval and answered with the CDF. `f` is for integration and
plotting; `F` is for decisions.

</details>

**Q2. Why does memorylessness hold exactly for the exponential but only
approximately for real systems — and what breaks if you trust it?**

<details>
<summary>Model answer</summary>

Mathematically it is a direct consequence of the exponential survival function's
factorisation: $P(T>s+t \mid T>s) = e^{-\lambda(s+t)}/e^{-\lambda s} =
e^{-\lambda t}$. The $s$ cancels *exactly*, not approximately, because the
exponential's hazard rate $f/F$ is constant. Every distribution with a constant
hazard rate has this form, so "memoryless" and "constant rate" are the same fact
seen twice.

Real systems are not constant-rate. A service's arrival rate rises during a
traffic spike, its latency distribution shifts after a deploy, and a dependency
degrading makes both the rate and the shape drift. Under such drift, having
waited 30 seconds tells you something real about the remaining wait — the
conditional distribution is genuinely shifted — and memorylessness is
approximately true only over short horizons relative to the drift timescale.

What breaks is the retry-ladder intuition that "each retry is a fresh draw, so
more retries help just as much". The lesson's Example B notes this directly. If
you keep a 6-second timeout and retry three times under a *drifting* process, the
third retry is not equivalent to one 6-second window, and if the cause of the
slowness is persistent (a cold cache that has not warmed, a lock held by the
first request) then each retry is *positively correlated* with the last. The
symptom in production is a retry ladder that succeeds early and never late —
consistent with the "fixed window per attempt" model and wrong about the process.

So memorylessness is best read as a design hint about which model to fit first:
if the hazard looks roughly constant, the exponential is a reasonable starting
point and its algebra will be simple. Confirm it by comparing the empirical
conditional survival at several values of s — if
$P(T > s+t \mid T > s)$ drifts with s, you need a different distribution
([Lesson 66](66_common_distributions.md)) or a segmented model.

</details>

**Q3. Why does fitting a normal to bimodal latency data invert your conclusion
about the tail?**

<details>
<summary>Model answer</summary>

Because the fit matches the two numbers you can compute and mismatches the shape
you care about. Fitting $\mathrm{N}(5.9, 216.09)$ to the 1 ms / 50 ms mixture gets
the mean exactly right by construction, and the variance exactly right too, since
both are determined by the data. That agreement is precisely what makes the fit
plausible — and precisely why the error hides.

Then the percentiles are wrong in a *direction*, not just a size. The true
$P(X > 10) = 0.1$ because 10% of responses take exactly 50 ms. The fitted normal
gives 0.3902, overestimating the tail nearly four-fold. A normal cannot represent
an atom at 50 ms, so it must smear that 10% across a continuous range, putting
most of it below 50 and leaving a spurious tail above. The result is that a
threshold chosen from the fitted percentile is set far too tight, so the SLO
fires constantly; or, if set from the mean ± 2 sd, it claims 99.7% under 35.3 ms
while 10% of requests take 50 ms — a direct contradiction, plus a physically
impossible lower bound of −23.5 ms.

The structural diagnosis is what saves you: the distribution is bimodal because
the service has two *modes of operation* (fast path versus slow path), not one
mode with a fat tail. Mistake 5 in this lesson generalises this to latency, file
sizes and request counts, all of which have hard floors and structural modes. The
fix is to decompose first — split by cached/uncached, hot/cold, small/large
tenant — and then model each mode, which is the continuous-world version of the
variance decomposition in
[Lesson 64](64_expectation_variance.md).

</details>

**Q4. Why is Monte Carlo integration worse than numerical quadrature when you
have a smooth density, and when is it nevertheless the right choice?**

<details>
<summary>Model answer</summary>

Because the two use their evaluations completely differently. Quadrature takes a
*deterministic* grid: with $n$ points on a smooth integrand, Simpson's rule gains
four digits of accuracy every time you double $n$, so error falls like
$h^4$. Monte Carlo uses $n$ *random* points, and by the central limit theorem its
error falls like $1/\sqrt{n}$. To halve a Monte Carlo error you quadruple the
samples; to halve a quadrature error you double them. The lesson's comparison is
stark: Simpson's rule returns 0.5000000000 for the uniform case, while 400,000
samples give something near 0.333 with visible run-to-run wobble. That is about
three correct digits against fifteen.

Randomness also carries a failure mode quadrature does not have: the answer
*changes between runs*. A load test whose Monte Carlo integration gives 0.333 one
day and 0.336 the next is reporting noise, not signal, and for a fixed seed you
have merely hidden the noise rather than removed it.

Monte Carlo is still the right tool when quadrature is unavailable or
impractical: the integrand has no closed form *and* no smooth structure, the
dimension is high (numerical quadrature suffers a curse of dimensionality that
Monte Carlo does not — 100 dimensions costs 100× the samples, not
$2^{100}$), the integrand is a complicated expression better evaluated
statistically, or the quantity is itself random. That is why it underpins
Monte Carlo integration in graphics and rare-event simulation, and why
[Lesson 70](70_information_theory_entropy.md) uses the area-ratio idea to turn
averages into probabilities. The rule of thumb the lesson states is right: use
Monte Carlo when you cannot integrate, not when you could.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — normal distribution, several computations.** Let X ~ N(50,
10²). (a) Compute P(X ≤ 60) and P(X ≥ 40) and confirm they are equal. (b) Compute
P(45 ≤ X ≤ 55). (c) Find x such that P(X ≤ x) = 0.025. (d) Convert to a
standard normal Z = (X − 50)/10 and confirm Z ~ N(0,1).

<details>
<summary>Solution</summary>

(a) P(X ≤ 60) = (1 + erf((60−50)/(10√2)))/2 = (1 + erf(0.7071068))/2 ≈ 0.8413447.
By symmetry P(X ≥ 40) = 1 − F(40) = 1 − 0.1586553 = 0.8413447. Equal ✓ — the
symmetry identity F(μ+a) = 1 − F(μ−a) is exact for the normal.

(b) P(45 ≤ X ≤ 55) = F(55) − F(45) = 0.6914625 − 0.3085375 = 0.3829250. This is
inside one standard deviation (±5 is only ±0.5 sd here), and 0.3829 is indeed
less than 0.6827.

(c) We need the z with Φ(z) = 0.025, which is z = −1.959964. Since 0.025 is
close to the lower tail, x = 50 + (−1.959964)(10) = 30.40. So about 2.5% of
values are below 30.40.

(d) The substitution Z = (X−50)/10 is exactly the standardisation. Check:
F_Z(0) should be 0.5, F_Z(1) should be Φ(1) = 0.8413447, and F_Z(−1.96) should be
0.025. The reason it works is that the change of variables absorbs μ and σ
entirely, so the resulting law has no parameters — which is why "the z-score"
is a universal yardstick.

```python
from math import erf, sqrt

MU, SIGMA = 50.0, 10.0


def normal_cdf(x, mu=MU, sigma=SIGMA):
    return (1.0 + erf((x - mu) / (sigma * sqrt(2.0)))) / 2.0


def normal_quantile(q, mu=MU, sigma=SIGMA):
    lo, hi = mu - 40 * sigma, mu + 40 * sigma
    for _ in range(200):
        mid = (lo + hi) / 2
        if normal_cdf(mid, mu, sigma) < q:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


a1 = normal_cdf(60)
a2 = 1 - normal_cdf(40)
print(f"(a) P(X <= 60) = {a1:.7f}")
print(f"    P(X >= 40) = {a2:.7f}")
print(f"    equal by symmetry: {abs(a1 - a2) < 1e-12}")

b = normal_cdf(55) - normal_cdf(45)
print(f"(b) P(45 <= X <= 55) = {b:.7f}   (vs 0.6827 for a full sd)")

x = normal_quantile(0.025)
z = (x - MU) / SIGMA
print(f"(c) x with P(X <= x) = 0.025: {x:.4f}")
print(f"    standardised z = {z:.6f}  (known value: -1.959964)")

print("(d) standardising:")
for raw, target in ((50.0, 0.5), (60.0, 0.8413447), (30.4, 0.025)):
    zz = (raw - MU) / SIGMA
    print(f"    X={raw:6.1f} -> Z={zz:+.4f}, F_Z = {normal_cdf(zz, 0.0, 1.0):.7f}"
          f"   expected {target:.7f}")
```

Note (c): the quantile function was found by bisection, not from a table. That is
exactly how `numpy` computes quantiles for arbitrary distributions, and it means
you never need a printed z-table to do real work.

</details>

**[ ] Exercise 2 — exponential, including the rate/mean confusion.** Let T be
exponentially distributed with mean 4 seconds.

(a) Find λ. (b) Compute P(T > 10). (c) Compute the 90th percentile. (d) Verify
memorylessness for s = 3, t = 4. (e) A server is configured to time out after
6 seconds and retry. Under the exponential model, what fraction of retries
succeed if the underlying service time is T ~ Exp with mean 4?

<details>
<summary>Solution</summary>

(a) λ = 1/mean = 1/4 = 0.25 per second. This is the step where people slip: the
parameter is a rate, so it is the *reciprocal* of the mean.

(b) P(T > t) = e^(−λt) = e^(−0.25 × 10) = e^(−2.5) ≈ 0.0820850. About 8.2%.

(c) The 90th percentile solves P(T ≤ x) = 0.9, i.e. e^(−0.25x) = 0.1, giving
x = ln(10)/0.25 = 9.210340. Note that 9.21 > 4: the 90th percentile sits well
above the mean for a right-skewed distribution.

(d) P(T > 7 | T > 3) = e^(−0.25×7)/e^(−0.25×3) = e^(−1.75)/e^(−0.75)
= 0.1737739/0.4723666 = 0.3678794. And P(T > 4) = e^(−1) = 0.3678794. Equal ✓

(e) Under this model a retry "succeeds" if it would complete within the 6-second
window, i.e. P(T ≤ 6) = 1 − e^(−0.25×6) = 1 − e^(−1.5) = 1 − 0.2231302 =
0.7768698. So about 77.7% succeed.

The memoryless result gives a nice alternative reading: because of memorylessness,
P(T ≤ 6) = P(T ≤ 3) + P(T ≤ 6 | T > 3)·P(T > 3) — the first 3 seconds plus a
fresh 3-second chance. This is exactly why timeout-and-retry ladders work as
intended under an exponential model: each retry is a genuinely independent fresh
draw, not a shorter slice of the original wait.

```python
from math import exp, log

MEAN = 4.0
LAMBDA = 1 / MEAN          # rate = reciprocal of the mean


def surv(t, lam=LAMBDA):
    """P(T > t) = e^(-lambda t)."""
    return exp(-lam * t)


print(f"(a) mean = {MEAN} s  ->  lambda = {LAMBDA} per second")
print(f"    (not {MEAN}! the exponential parameter is a RATE)")

b = surv(10)
print(f"(b) P(T > 10) = e^(-0.25*10) = e^-2.5 = {b:.7f}")

c = -log(0.10) / LAMBDA
print(f"(c) 90th percentile = ln(10)/lambda = {c:.7f} s   (mean is only {MEAN})")

s, t = 3.0, 4.0
lhs = surv(s + t) / surv(s)
rhs = surv(t)
print(f"(d) P(T > {s+t} | T > {s}) = {lhs:.7f}")
print(f"    P(T > {t})             = {rhs:.7f}")
print(f"    memoryless: {abs(lhs - rhs) < 1e-12}")

e = 1 - surv(6)
print(f"(e) P(success within 6 s) = 1 - e^(-1.5) = {e:.7f}")

# The retry-ladder reading of memorylessness.
first3 = 1 - surv(3)
retry3 = (1 - surv(3)) * surv(3)
print(f"    first 3 s: {first3:.7f}  +  retry after {surv(3):.7f}: {retry3:.7f}")
print(f"    total {first3 + retry3:.7f} -- equals the direct answer: "
      f"{abs(first3 + retry3 - e) < 1e-12}")
```

That last line is a genuine identity, not an approximation: memorylessness means a
3-second retry is statistically a fresh 3-second wait, so a ladder of timeouts is
exactly equivalent to one long window.

</details>

**[ ] Exercise 3 — Challenge: build a two-point mixture and see why normal is
wrong.** A service responds in 1 ms with probability 0.9 and in 50 ms with
probability 0.1. (a) Compute the mean and variance. (b) Compute the probability
that a response takes more than 10 ms. (c) A normal fitted to (a) would put
essentially zero probability beyond 10 ms. Compare. (d) For an SLO of "99% of
requests under 10 ms", does this service pass? (e) What does this tell you about
using mean ± 2 sd as a latency SLO?

<details>
<summary>Solution</summary>

(a) E[X] = 0.9(1) + 0.1(50) = 0.9 + 5 = 5.9 ms.
Var(X) = E[X²] − (E[X])² = (0.9·1 + 0.1·2500) − 5.9² = (0.9 + 250) − 34.81 =
250.9 − 34.81 = 216.09, so σ ≈ 14.70 ms.

(b) P(X > 10) = 0.1 exactly — a 50 ms response is slow, a 1 ms one is not, and
there are no values in between.

(c) Normal(N(5.9, 216.09)): P(X > 10) = 1 − Φ((10−5.9)/14.70) = 1 − Φ(0.2789) ≈
0.3902. So the true answer is 0.1000 and the normal says 0.3902 — the normal
**overestimates** the tail here. Worse, it assigns P(X > 50) ≈ 0.0032 to a value
that is *atom*, and P(X > 100) ≈ 4 × 10⁻⁶ to something with probability zero. A
well-chosen normal never has 1% probability sitting at exactly one point.

(d) The SLO "99% under 10 ms" **fails badly**: only 90% of requests are under
10 ms, so 10% violate it — ten times the allowed error budget. A fitted normal
would have said 39% violate, i.e. the SLO fails obviously; the honest mixture
reveals it fails, and it also reveals *why*: the slow path is a distinct mode,
not a tail.

(e) mean ± 2σ = 5.9 ± 29.4 = [−23.5, 35.3]. This is worse than useless for
three reasons. First, the lower bound is negative, which is physically impossible.
Second, it says 99.7% of requests finish within 35 ms, but 10% take 50 ms — a
direct contradiction. Third, it identifies the wrong problem: the distribution is
bimodal, so there is no single "normal-ish" behaviour to tighten. The fix is to
separate the modes (fast path vs slow path) and set a per-mode SLO, or to fit a
mixture, or to model the slow path with a log-normal. This is exactly the
bimodality from
[Lesson 64](64_expectation_variance.md)'s variance-decomposition exercise,
wearing a latency costume.

```python
from math import erf, sqrt

P_FAST, T_FAST, T_SLOW = 0.9, 1.0, 50.0
mean = P_FAST * T_FAST + (1 - P_FAST) * T_SLOW
second = P_FAST * T_FAST**2 + (1 - P_FAST) * T_SLOW**2
var = second - mean**2
sigma = var**0.5

def normal_cdf(x, mu, sd):
    return (1.0 + erf((x - mu) / (sd * sqrt(2.0)))) / 2.0


def mixture_cdf(x):
    """Exact CDF of the two-point mixture."""
    if x < T_FAST:
        return 0.0
    if x < T_SLOW:
        return P_FAST
    return 1.0


print(f"(a) E[X] = {mean:.4f} ms")
print(f"    E[X^2] = {second:.4f}   Var = {var:.4f}   sd = {sigma:.4f}")

true_tail = 1 - mixture_cdf(10)
fit_tail = 1 - normal_cdf(10, mean, sigma)
print(f"(b) true P(X > 10)          = {true_tail:.4f}")
print(f"(c) normal-fit P(X > 10)     = {fit_tail:.4f}   "
      f"({fit_tail / true_tail:.1f}x too high)")

print(f"    normal P(X > 50) = {1 - normal_cdf(50, mean, sigma):.6f} "
      f"(but 50 is an ATOM with probability 0.1)")
print(f"    normal P(X > 100)= {1 - normal_cdf(100, mean, sigma):.3e} "
      f"(probability is exactly 0)")

violation = true_tail
budget = 0.01
print(f"(d) SLO '99% under 10 ms': violation rate {violation:.2%}, "
      f"budget {budget:.2%}")
print(f"    passes: {violation <= budget}  "
      f"({violation / budget:.1f}x over budget)")

print(f"(e) mean +/- 2sd = [{mean - 2 * sigma:.2f}, {mean + 2 * sigma:.2f}]")
print(f"    lower bound negative: {mean - 2 * sigma < 0}")
print(f"    claims 99.7% within {mean + 2 * sigma:.1f} ms, but "
      f"{violation:.0%} take 50 ms")
```

The general lesson: fitting a normal to a bimodal distribution does not merely
add error, it *inverts* the conclusion about the tail. Whenever a metric has hard
structural modes — cached versus uncached, small tenants versus large ones, hot
versus cold path — decompose before you fit.

</details>

**[ ] Exercise 4 — density versus probability, made concrete.** (a) For
$X \sim \mathcal{N}(0, 0.1^2)$, compute the peak density and verify numerically
that the total area is 1 despite the peak exceeding 1. (b) For
$X \sim \mathrm{Uniform}(1,5)$, compute $P(X = 3)$ and
$P(2.9 \le X \le 3.1)$, and explain the ratio between them. (c) Give the
probability of the interval $[0.05, 0.15]$ under the same normal, and compare it
with the density at 0. (d) State which of your three answers would be wrong if
reported as "the probability that $X = 3$".

<details>
<summary>Solution</summary>

(a) The peak of a normal is at the mean, with value
$\frac{1}{\sigma\sqrt{2\pi}} = \frac{1}{0.1 \times 2.5066283} = 3.989423$. That is
nearly 4× a probability, and it is perfectly legal. Numerically integrating the
density over [−1, 1] with Simpson's rule gives 1.0000000000 — the ±1 window is
10 standard deviations each way, so it captures essentially all the mass. The
lesson's own code block makes exactly this check.

(b) $P(X = 3) = 0$ exactly, because $X$ is continuous. But the density is a
constant $1/4$, so

$$P(2.9 \le X \le 3.1) = \int_{2.9}^{3.1}\tfrac14\,dx = \tfrac{0.2}{4} = 0.05.$$

The ratio between them is infinite, and that is the point: the point probability
is 0 no matter how small the interval around it, while the interval probability is
a width ratio. The density $0.25$ sits between them, meaning "5% of the mass lies
in any window of width 0.2 centred here".

(c) $P(0.05 \le X \le 0.15)$ is the region from $0.5\sigma$ to $1.5\sigma$, so
$F(1.5) - F(0.5) = 0.9332 - 0.6915 = 0.2417$. The density at 0 is 3.989423, so the
density is about **16.5 times larger** than the probability of that whole
0.1-wide interval. That ratio is the width: the density is per unit, and the
interval has width 0.1.

(d) All of the "probability that $X = x$" readings are wrong: $P(X=3) = 0$ for
(a)'s normal as well, and the density 3.989 is not a probability of anything.
Reporting "3.99 chance" is Mistake 1 twice over — once for treating a density as
a probability, and once for treating a continuous variable as if it could equal a
point.

```python
from math import erf, exp, sqrt, pi

SIGMA = 0.1

def normal_pdf(x, mu=0.0, sigma=SIGMA):
    return 1 / (sigma * sqrt(2 * pi)) * exp(-((x - mu) ** 2) / (2 * sigma**2))


def normal_cdf(x, mu=0.0, sigma=SIGMA):
    return (1.0 + erf((x - mu) / (sigma * sqrt(2.0)))) / 2.0


def simpson(f, lo, hi, n=200000):
    h = (hi - lo) / n
    total = f(lo) + f(hi)
    for i in range(1, n):
        total += f(lo + i * h) * (4 if i % 2 else 2)
    return total * h / 3


A, B = 1.0, 5.0
uniform_pdf = lambda x: 1 / (B - A) if A <= x <= B else 0.0

peak = normal_pdf(0.0)
area = simpson(normal_pdf, -1.0, 1.0)
print("(a) peak density = {peak:.6f}   (a probability cannot exceed 1)")
print(f"    total area over [-1, 1] = {area:.10f}")
print(f"    legal: {abs(area - 1.0) < 1e-9}")

point = 0.0                        # P(X = 3) for a continuous variable
window = uniform_pdf(3.0) * (3.1 - 2.9)
print()
print(f"(b) P(X = 3)          = {point:.6f}")
print(f"    density at 3      = {uniform_pdf(3.0):.6f}")
print(f"    P(2.9 <= X <= 3.1)= {window:.6f}  = width 0.2 x density 0.25")

interval = normal_cdf(0.15, 0.0, SIGMA) - normal_cdf(0.05, 0.0, SIGMA)
print()
print(f"(c) P(0.05 <= X <= 0.15) = {interval:.6f}")
print(f"    density at 0          = {peak:.6f}")
print(f"    density / interval    = {peak / interval:.1f}x  (the window is 0.1 wide)")
print(f"    (d) every 'P(X = x)' reading here is 0 -- the correct answer is 0.")
```

</details>

**[ ] Exercise 5 — uniform, exponential, and an SLO threshold.** (a) Requests
arrive at a Poisson rate of 4 per second, so the inter-arrival gap $T$ is
$\mathrm{Exp}(\lambda = 4)$. Compute the mean gap, the 95th percentile, and
$P(T > 0.5)$.
(b) Service time is $X \sim \mathrm{Uniform}(0.2, 0.8)$ seconds. Compute
$E[X]$, $\mathrm{Var}(X)$, and $P(X > 0.5)$.
(c) Suppose you want an end-to-end timeout of 1.0 second and you assume arrival
and service are independent. What is $P(\text{arrival gap} + \text{service} >
1.0)$?
(d) Explain why the answer to (c) is not just "the 95th percentile of each",
and state the assumption that would break.

<details>
<summary>Solution</summary>

(a) $\lambda = 4$ gives $E[T] = 1/\lambda = 0.25$ s. The 95th percentile solves
$e^{-4t} = 0.05$, so $t = \ln 20 / 4 = 2.9957/4 = 0.7489$ s. And
$P(T > 0.5) = e^{-4 \times 0.5} = e^{-2} = 0.1353$. Note the mean gap is 0.25 s
while the 95th percentile is 0.75 s — a factor of 3 — because the exponential is
right-skewed.

(b) $E[X] = (0.2+0.8)/2 = 0.5$ s. $\mathrm{Var}(X) = (0.8-0.2)^2/12 =
0.36/12 = 0.03$ s², so $\sigma = 0.1732$ s. And $P(X > 0.5) = (0.8-0.5)/(0.8-0.2)
= 0.3/0.6 = 0.5$ — exactly half, because the distribution is symmetric about 0.5.
The uniform *is* one distribution where mean and median coincide, which is why
Mistake 2 of Lesson 63 does not bite here.

(c) The sum $T + S$ exceeds 1.0 exactly when $S > 1.0 - T$. Integrate over $T$:

$$P(T+S>1) = \int_0^{0.2}\!\!1\,f_S(s)\,ds + \int_{0.2}^{0.8}\!\!\bigl(1 - F_T(1-s)\bigr)f_S(s)\,ds$$

with $f_S = 1/0.6$ and $F_T(t) = 1 - e^{-4t}$ on the support. Substituting and
evaluating gives the CDF of the sum directly: since $F_{T+S}(x) = P(T \le x-S)$,
integrating the inner tail,

$$P(T + S > 1) = \int_{0.2}^{0.8} e^{-4(1-s)} \cdot \frac{1}{0.6}\,ds 
= \frac{e^{-4}}{0.6}\int_{0.2}^{0.8}e^{4s}\,ds = \frac{e^{-4}(e^{3.2} - e^{0.8})}{0.6 \times 4}.$$

Numerically: $e^{-4} = 0.018316$, $e^{3.2} = 24.5325$, $e^{0.8} = 2.2255$, so
$P = 0.018316 \times 22.3070 / 2.4 = 0.4086 / 2.4 = 0.1702$.

So about **17.0%** of requests exceed the 1-second budget.

(d) It is not the 95th percentile of either, because the *sum* of two
independent variables is not either variable. Each marginal is right-skewed
(exponential) or symmetric (uniform); the sum is a different distribution with
mean $0.75$ and its own tail. Adding the two 95th percentiles ($0.7489 +
0.77 = 1.52$ s) overstates the budget by 52%, because that treats the two events
as perfectly positively correlated — both at their worst simultaneously — which
is the wrong model in the opposite direction.

The assumption that would break the calculation is **independence**. If the queue
is busy when a request arrives (it usually is, since an arrival and a long
service time both mean load), the gap and the service time are negatively
correlated, and the sum's tail is *fatter* than 0.1702. Under a shared-bottleneck
model the correct tool is a queueing model, not independent convolution.

```python
from math import erf, exp, log, sqrt

LAMBDA = 4.0
A_S, B_S = 0.2, 0.8

def exp_surv(t, lam=LAMBDA):
    return exp(-lam * t)


def uniform_pdf(x, a=A_S, b=B_S):
    return 1 / (b - a) if a <= x <= b else 0.0


def uniform_cdf(x, a=A_S, b=B_S):
    return 0.0 if x < a else (1.0 if x >= b else (x - a) / (b - a))


print("(a) Exp(rate=4): mean 1/lambda = {:.4f} s".format(1 / LAMBDA))
print("    95th percentile = ln(20)/4 = {:.4f} s".format(log(20) / LAMBDA))
print("    P(T > 0.5) = e^-2 = {:.4f}".format(exp_surv(0.5)))

mean_s = (A_S + B_S) / 2
var_s = (B_S - A_S) ** 2 / 12
print()
print(f"(b) Uniform({A_S}, {B_S}): E[X] = {mean_s:.4f} s")
print(f"    Var(X) = {var_s:.4f} s^2, sd = {sqrt(var_s):.4f} s")
print(f"    P(X > 0.5) = {1 - uniform_cdf(0.5):.4f}  (symmetric about the mean)")

# (c) exact: P(T + S > x) = integral over s of exp(-lam*(x-s)) * f_S(s) ds
def tail_of_sum(x, lam=LAMBDA, a=A_S, b=B_S):
    """P(T + S > x) with T ~ Exp(lam), S ~ Uniform(a, b), independent."""
    total = 0.0
    n = 200_000
    h = (b - a) / n
    for i in range(n):
        s = a + (i + 0.5) * h
        total += exp_surv(x - s, lam) * (1 / (b - a)) if s < x else 0.0
    return total * h


tail = tail_of_sum(1.0)
q95_arrival = log(20) / LAMBDA
q95_service = A_S + 0.95 * (B_S - A_S)
print()
print(f"(c) P(arrival + service > 1.0 s) = {tail:.4f}")
print(f"    sum of the two 95th percentiles = {q95_arrival:.4f} + "
      f"{q95_service:.4f} = {q95_arrival + q95_service:.4f} s -- "
      f"{((q95_arrival + q95_service) / 1.0 - 1) * 100:.0f}% over the real budget")
print("    adding marginal quantiles assumes perfect POSITIVE correlation;")
print(f"    independence gives {tail:.4f}, and negative correlation")
print("    (busy queue) would be worse still.")
```

</details>

**[ ] Exercise 6 — Challenge: choose an SLO threshold by inverting the CDF, and
show what a normal fit would have cost you.** A request path consists of two
stages, each independently $\mathrm{Exp}(4)$ seconds per second — so each stage
has mean 0.25 s — and the total is their sum.
(a) Compute $E[T_{\text{total}}]$ and $\mathrm{Var}(T_{\text{total}})$ by linearity
and by the sum-of-variance formula, confirming agreement.
(b) Find the threshold $x$ such that only 1% of totals exceed it.
(c) Suppose instead someone fits a $\mathrm{N}(0.5, \sigma^2)$ to this total.
Compute the sd they would fit, the threshold they would derive, and how far off it
is from the answer in (b).
(d) Explain which is the more dangerous error for an SLO: over- or
under-estimating the tail, and what operational symptom each produces.

<details>
<summary>Solution</summary>

(a) By linearity, $E[T_{\text{total}}] = 0.25 + 0.25 = 0.5$ s. For the variance,
$\mathrm{Var}(T_1 + T_2) = \mathrm{Var}(T_1) + \mathrm{Var}(T_2) = 2(1/16) =
0.125$ s² because the stages are independent. Check against the direct route:
$1/\lambda^2 = 1/16 = 0.0625$, so $2 \times 0.0625 = 0.125$. ✓ Same answer.

(b) The sum of two independent exponentials with the *same* rate is
$\mathrm{Gamma}(2, \text{rate } 4)$, with CDF $1 - e^{-4x}(1 + 4x)$. Set
$e^{-4x}(1+4x) = 0.01$ and solve numerically:

- $x = 0.9$: $e^{-3.6}(4.6) = 0.0273 \times 4.6 = 0.1256$
- $x = 1.2$: $e^{-4.8}(5.8) = 0.00823 \times 5.8 = 0.0477$
- $x = 1.5$: $e^{-6}(7) = 0.00248 \times 7 = 0.01735$
- $x = 1.65$: $e^{-6.6}(7.6) = 0.00136 \times 7.6 = 0.01035$
- $x = 1.70$: $e^{-6.8}(7.8) = 0.00111 \times 7.8 = 0.00867$

The tail probability decreases in $x$, so the crossing lies between 1.65 and
1.70, and bisection on the CDF gives **$x = 1.6596$ s**. The 99th percentile of
the true total is **1.66 seconds**, more than three times the mean of 0.5 s.

(c) The fitted normal would use $\mu = 0.5$ and $\sigma = \sqrt{0.125} = 0.3536$.
Its 99th percentile is $0.5 + 2.3263479 \times 0.3536 = 0.5 + 0.8226 = 1.3226$
s. So the normal suggests a threshold of **1.32 s**, which is 0.337 s too tight —
**25% below** the truth.

The tail figures show how badly. The true $P(T > 1.3225) = e^{-5.29}(1 + 5.29) =
0.00505 \times 6.29 = 0.0317$, so a threshold of 1.32 s actually lets through
**3.2%** of requests when you promised 1%. Conversely the fitted normal
$P(T > 1.6596) = 1 - \Phi((1.6596-0.5)/0.3536) = 1 - \Phi(3.279) = 0.00052$, so
the model thinks the true threshold is almost never exceeded — it badly
*understates* the risk at large $x$, which is exactly where SLOs live.

(d) The fitted normal *understates* the far tail, and that is the more dangerous
error of the two directions. If a model says the risk at your threshold is lower
than it really is, the dashboard looks safe right up until the day it is not, and
the breach arrives with no warning — the SLO was never going to catch it. The
opposite error, overestimating the tail, produces the milder symptom of constant
near-misses and a threshold set too loose, which costs headroom but is *visible*.

Here the two effects combine into something worse than either: the normal-derived
threshold of 1.32 s is 25% too tight, so it produces near-misses continuously, and
the model simultaneously claims the risk there is only 3.2% when it is really
about 32% — a factor of 10. The team learns to ignore a metric that is wrong by an
order of magnitude, and the real tail at 1.66 s never gets examined.

The fix is not to widen the threshold blindly but to model the right distribution:
the sum of independent stages has a Gamma CDF, whose 99th percentile is exactly
computable, and [Lesson 68](68_law_of_large_numbers_and_clt.md) explains *why*
the normal approximation degrades here — two stages is nowhere near enough
averaging for the CLT to apply.

```python
from math import erf, exp, log, sqrt

LAMBDA = 4.0
N_STAGES = 2

def stage_var():
    return 1 / LAMBDA ** 2


def gamma2_cdf(x, lam=LAMBDA, shape=N_STAGES):
    """CDF of the sum of `shape` independent Exp(lam): 1 - e^(-lam x) sum_{i<shape} (lam x)^i / i!"""
    if x <= 0:
        return 0.0
    total = 0.0
    term = 1.0
    for i in range(shape):
        if i > 0:
            term *= (lam * x) / i
        total += term
    return 1.0 - exp(-lam * x) * total


def gamma2_quantile(q, lo=0.0, hi=20.0):
    """Bisection on the CDF -- the quantile function by search."""
    for _ in range(200):
        mid = (lo + hi) / 2
        if gamma2_cdf(mid) < q:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def normal_cdf(x, mu, sigma):
    return (1.0 + erf((x - mu) / (sigma * sqrt(2.0)))) / 2.0


def normal_quantile(q, mu, sigma):
    lo, hi = mu - 40 * sigma, mu + 40 * sigma
    for _ in range(200):
        mid = (lo + hi) / 2
        if normal_cdf(mid, mu, sigma) < q:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


mean_t = N_STAGES / LAMBDA
var_t = N_STAGES * stage_var()
print(f"(a) E[total] = {N_STAGES} x 1/lambda = {mean_t:.4f} s")
print(f"    Var(1 stage) = {stage_var():.6f}, sum = {var_t:.6f} s^2, "
      f"sd = {sqrt(var_t):.4f} s")
print(f"    Var(additive form 2 x (1/4^2) = {2 * (1 / 4 ** 2):.6f}, agree: "
      f"{abs(var_t - 2 / 16) < 1e-12}")

q99_true = gamma2_quantile(0.99)
print()
print(f"(b) true 99th percentile (Gamma shape 2, rate {LAMBDA}) = {q99_true:.4f} s")
print(f"    CDF check: {gamma2_cdf(q99_true):.6f}")
print(f"    note it is {q99_true / mean_t:.1f}x the mean of {mean_t} s")

q99_fit = normal_quantile(0.99, mean_t, sqrt(var_t))
print()
print(f"(c) normal fit N({mean_t}, {var_t:.4f}) -> 99th percentile = {q99_fit:.4f} s")
print(f"    too tight by {q99_true - q99_fit:.4f} s "
      f"({(q99_true / q99_fit - 1) * 100:.0f}% off)")
print(f"    actual P(total > {q99_fit:.2f}) with the TRUE law = "
      f"{1 - gamma2_cdf(q99_fit):.4f}  (you promised 0.01)")
print(f"    the normal thinks P(total > {q99_true:.2f}) = "
      f"{1 - normal_cdf(q99_true, mean_t, sqrt(var_t)):.6f}  (truth: 0.01)")
print("    -> the normal understates the far tail, where SLOs live.")
```

</details>

## Summary

- For a continuous variable P(X = a) = 0, so probability is redefined as an
  **area** under a density, not a value at a point.
- A density is probability per unit width, so f(x) may exceed 1; only the total
  area is constrained to equal 1.
- The CDF is the reliable tool: P(a ≤ X ≤ b) = F(b) − F(a), and for continuous X,
  P(X ≤ x) = P(X < x).
- Uniform(a, b) has mean (a+b)/2 and variance (b−a)²/12; probability is a width
  ratio.
- Exponential(λ) has mean 1/λ — the parameter is a **rate**, not a mean — and it
  is memoryless: P(T > s+t | T > s) = P(T > t).
- The normal CDF is (1 + erf(z/√2))/2, so `math.erf` gives it exactly; the CDF
  has no elementary inverse, so quantiles come from bisection.
- The 68-95-99.7 rule is exact to 0.2%: 0.6827, 0.9545, and 0.9973.
- Never fit a normal to bimodal or hard-bounded data; it can invert your
  conclusion about the tail, which is the number SLOs depend on.

## Next

[66 — Common Distributions](66_common_distributions.md) collects Bernoulli,
Binomial, Poisson, Geometric, Uniform, Exponential, and Normal into one reference
table, with a from-scratch pure-Python sampler for each and a matplotlib section
that plots them all together.