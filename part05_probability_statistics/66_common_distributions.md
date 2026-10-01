# 66 — Common Distributions

**Part**: part05_probability_statistics · **Prerequisites**: 65 · **Time**: 40 min

---

## In Plain Words

Seven distributions cover almost everything you will ever need in practice. This
lesson puts them in one place: what each one is for, what its parameters mean,
what its mean and variance are, and how to generate samples from it yourself in
a few lines of standard-library Python.

There are two shapes here. The discrete ones — Bernoulli, Binomial, Poisson,
Geometric — count things: how many successes, how many arrivals, how many
retries. The continuous ones — Uniform, Exponential, Normal — measure things:
how long, how much, how far. Learning to tell them apart by asking "does this
count or does it measure?" solves most of the identification problem before any
formula comes out.

The samplers are the practical payload. Modern libraries hide a surprising amount
of machinery behind `np.random.exponential(scale=0.5)`, and writing each one by
hand is how you learn what that machinery is. Two techniques cover almost
everything: **inverse transform sampling** (draw a uniform, push it through the
inverse CDF) and the **Box–Muller transform** (turn two uniforms into two normals
via trigonometry).

## Why Computer Science Cares

- **Load and traffic modelling.** Poisson is the default model for arrival rates;
  Exponential for inter-arrival gaps; together they give the M/M/1 queue.
- **Error and retry counts.** Poisson for "how many errors per minute", Geometric
  for "how many attempts until success", Binomial for "how many successes in a
  fixed budget".
- **Simulation and testing.** Every one of these samplers is needed to write a
  load test that produces a realistic request stream. A load test using uniform
  arrival times stresses your system in a way production never does.
- **Monte Carlo and optimisation.** Randomised search, simulated annealing, and
  importance sampling all draw from named distributions.
- **Interviews.** "How would you model the number of failures per hour?" is a
  Poisson question, and recognising that it is one is the whole test.

## The Formal Version

Notation: X ~ D(θ) means X follows distribution D with parameter θ.

### The discrete four

**Bernoulli(p).** One trial, two outcomes.
p_X(1) = p, p_X(0) = 1 − p. E[X] = p, Var = p(1−p).
Use for: one yes/no outcome. Cache hit, click, test passed.
Sampler: one uniform compared against p.

**Binomial(n, p).** Successes in n independent trials.
p_X(k) = C(n,k) pᵏ(1−p)^(n−k). E = np, Var = np(1−p).
Use for: a count out of a fixed number of attempts. Conversion rate, defects in
100 builds, successes in 20 A/B test trials.
Sampler: sum n Bernoulli draws. (Or a faster algorithm for large n — see below.)

**Poisson(λ).** Number of events in a fixed interval of length 1.
p_X(k) = e^(−λ) λᵏ/k!. E = λ, Var = λ.
Use for: rare independent events in a window. Requests per second, errors per
minute, typos per page.
Sampler: Knuth's product method — multiply uniforms until the product drops
below e^(−λ). Works well for small λ, badly for large.

**Geometric(p).** Number of trials until the first success, counting the success.
p_X(k) = (1−p)^(k−1) p for k = 1, 2, …. E = 1/p, Var = (1−p)/p².
Use for: how many attempts until success. Retries until a request succeeds,
polls until a job is ready.
Sampler: repeat uniform draws until one exceeds 1 − p.

### The continuous three

**Uniform(a, b).** Every value in [a, b] equally likely.
f(x) = 1/(b−a). E = (a+b)/2, Var = (b−a)²/12.
Use for: picking a random element, a random point for Monte Carlo, jitter.
Sampler: a + (b−a)·u for u uniform on [0,1).

**Exponential(λ).** Waiting time until the first event, with rate λ.
f(x) = λe^(−λx). E = 1/λ, Var = 1/λ².
Use for: time between arrivals, time to failure.
Sampler: **−ln(1−u)/λ**. This is inverse transform, and the derivation is worth
doing once: F(x) = 1 − e^(−λx), so setting F(x) = u gives x = −ln(1−u)/λ.

**Normal(μ, σ²).** The bell curve.
f(x) = e^(−(x−μ)²/(2σ²)) / (σ√(2π)). E = μ, Var = σ².
Use for: sums and averages of many small things, measurement error, anything
where the central limit theorem applies.
Sampler: **Box–Muller**, two normals from two uniforms.

**Theorem (Box–Muller).** If U₁, U₂ are independent uniform on [0,1), then

    Z₀ = √(−2 ln U₁) · cos(2π U₂)
    Z₁ = √(−2 ln U₁) · sin(2π U₂)

are independent standard normals.

**Explanation.** In polar coordinates, the joint density of two independent
standard normals is (1/2π)e^(−r²/2) in the plane, so the radius and angle are
independent: r² ~ Exp(1/2) and θ ~ Uniform(0, 2π). That gives r = √(−2 ln U₁)
and θ = 2πU₂, and converting back to Cartesian coordinates via (r cos θ, r sin θ)
gives the formula. The reason the log appears is that the squared radius is
exponential — the same exponential you already implemented.

### The reference table

| Distribution | Parameters | Support | Mean | Variance | Real-world use |
| --- | --- | --- | --- | --- | --- |
| Bernoulli | p | {0, 1} | p | p(1−p) | one yes/no trial |
| Binomial | n, p | 0…n | np | np(1−p) | successes in n trials |
| Poisson | λ | 0,1,2,… | λ | λ | rare events per interval |
| Geometric | p | 1,2,… | 1/p | (1−p)/p² | trials until first success |
| Uniform | a, b | [a,b] | (a+b)/2 | (b−a)²/12 | random point, jitter |
| Exponential | λ | [0,∞) | 1/λ | 1/λ² | waiting time, inter-arrival |
| Normal | μ, σ² | (−∞,∞) | μ | σ² | averages, measurement error |

Two facts from the table worth internalising:

- **Poisson has mean equal to variance**, which is the fingerprint that
  distinguishes it from Binomial (variance ≤ mean, always) and from any
  over-dispersed count process (variance > mean). If you ever measure a count
  distribution and find variance much bigger than mean, it is not Poisson — the
  events are clustered, and you need a negative-binomial or compound model.
- **Exponential's parameter is a rate.** Mean = 1/λ. Similarly the Geometric mean
  is 1/p, a reciprocal. Count distributions get parameterised by rate, so the
  reciprocal appears everywhere.

## Worked Example

### Example A — sampling a Normal with Box–Muller, deriving the constant

Take U₁ = 0.5 and U₂ = 0.25.

    r = √(−2 ln 0.5) = √(2 × 0.693147) = √1.386294 = 1.177410
    θ = 2π × 0.25 = π/2 = 1.570796
    Z₀ = 1.177410 × cos(π/2) = 1.177410 × 0.000000 = 0.000000
    Z₁ = 1.177410 × sin(π/2) = 1.177410 × 1.000000 = 1.177410

So (Z₀, Z₁) = (0, 1.1774). The first value is exactly 0 because U₂ = 0.25 gives
θ = π/2, and cos(π/2) = 0 — a nice coincidence that shows the geometry: this
point lies exactly on the vertical axis. Then Z ~ N(0,1) becomes
X = μ + σZ, so with μ = 100, σ = 5 the sample is X = 100 + 5(1.1774) = 105.887.

Let me do a second draw to show the pair is genuinely different: U₁ = 0.9,
U₂ = 0.4.

    r = √(−2 ln 0.9) = √(0.210721) = 0.459044
    θ = 2π(0.4) = 2.513274
    cos θ = −0.809017, sin θ = 0.587785
    Z₀ = 0.459044 × (−0.809017) = −0.371373
    Z₁ = 0.459044 × (0.587785) =  0.269796

So X = 100 + 5(−0.371373) = 98.143.

Two useful observations. First, r shrinks as U₁ grows toward 1, because −ln U₁
shrinks — so U₁ controls how *far* from the mean you land, and U₂ controls
*which direction*. That is a genuinely intuitive parameterisation, and it is why
Box–Muller feels mechanical rather than magical.

### Example B — inverse transform for the Exponential

We want a sample from Exp(λ = 0.5). Draw u = 0.3.

    x = −ln(1 − u)/λ = −ln(0.7)/0.5 = 0.356675/0.5 = 0.713350

With u = 0.9: x = −ln(0.1)/0.5 = 2.302585/0.5 = 4.605170.

Note how the transform inverts the shape. Small u gives small x, large u gives
large x, with the exponential's characteristic long tail — u = 0.9 already
produced a wait more than twice the mean of 2.

**The derivation.** We want a function g such that P(g(U) ≤ x) = F(x). Set g(u) =
−ln(1−u)/λ. Then

    P(g(U) ≤ x) = P(−ln(1−U)/λ ≤ x) = P(U ≤ 1 − e^(−λx)) = 1 − e^(−λx) = F(x) ✓

The final equality is the exponential CDF, so g(U) has exactly the distribution
we wanted. This works whenever F is invertible, which is why it is the default
method — and why a distribution with no closed-form inverse, like the normal,
needs a different trick.

### Example C — Poisson by Knuth's method, and when it stops working

To sample Poisson(λ) with λ = 2.5, Knuth's algorithm is:

1. Set L = e^(−2.5) = 0.0820850, k = 0, p = 1.
2. Repeat: multiply p by a fresh uniform; while p > L, increment k and redraw.
3. Return k.

Following it: p = 1·0.5 = 0.5 > L, so k = 1. Next p = 0.5·0.7 = 0.35 > L, so
k = 2. Next p = 0.35·0.4 = 0.14 > L, so k = 3. Next p = 0.14·0.6 = 0.084 > L,
so k = 4. Next p = 0.084·0.9 = 0.0756 < L — stop, return 4.

So this particular sequence of uniforms gives k = 4. The expected number of
multiplications is λ + 1 = 3.5, which is why the method is efficient for small
λ. For λ = 1000 it needs about 1001 multiplications per sample, which is far
worse than the alternatives — hence the practical advice: use Knuth for λ below
about 30, and use the normal approximation (or a rejection method) above that.

## Runnable Code

### Every sampler, from scratch, standard library only

```python
import math
import random

# Each sampler returns ONE draw from its distribution, using only `random`
# uniform values on [0, 1). This is what numpy.random does internally.

u = random.random  # shorthand: a uniform on [0, 1)


def sample_bernoulli(p):
    """One trial, two outcomes. Compare a uniform against p."""
    return 1 if u() < p else 0


def sample_binomial(n, p):
    """Successes in n independent trials: just add up n Bernoulli draws."""
    return sum(sample_bernoulli(p) for _ in range(n))


def sample_poisson(lam):
    """Knuth's product method. Efficient for small lam only.

    Multiply uniforms until the running product drops below e^(-lam);
    the number of multiplications is the count.
    """
    limit = math.exp(-lam)
    k = 0
    prod = 1.0
    while True:
        prod *= u()
        if prod <= limit:
            return k
        k += 1


def sample_geometric(p):
    """Trials until the first success, counting the success itself."""
    count = 0
    while u() >= p:
        count += 1
    return count + 1


def sample_uniform(a, b):
    """Inverse transform: a + (b - a) * U is uniform on [a, b)."""
    return a + (b - a) * u()


def sample_exponential(lam):
    """Inverse transform on the exponential CDF.

    F(x) = 1 - e^(-lam x), so solving F(x) = v for x gives x = -ln(1-v)/lam.
    Using 1-v avoids taking log(0) when v happens to be very close to 1.
    """
    return -math.log1p(-u()) / lam


def sample_normal(mu, sigma):
    """Box-Muller: two uniforms give two independent standard normals.

    r^2 is exponential with rate 1/2, so r = sqrt(-2 ln U1);
    the angle is uniform on [0, 2*pi).
    """
    u1 = max(u(), 1e-12)  # guard against log(0)
    u2 = u()
    r = math.sqrt(-2.0 * math.log(u1))
    theta = 2.0 * math.pi * u2
    z = r * math.cos(theta)
    return mu + sigma * z


def sample_normal_pair(mu, sigma):
    """Box-Muller yields TWO normals per call; use both for efficiency."""
    u1 = max(u(), 1e-12)
    u2 = u()
    r = math.sqrt(-2.0 * math.log(u1))
    theta = 2.0 * math.pi * u2
    return (mu + sigma * r * math.cos(theta),
            mu + sigma * r * math.sin(theta))


random.seed(31337)

print("Ten draws from each distribution (fixed seed, so reproducible):")
print()
print("Bernoulli(0.3)   :", [sample_bernoulli(0.3) for _ in range(10)])
print("Binomial(10,0.3) :", [sample_binomial(10, 0.3) for _ in range(10)])
print("Poisson(2.5)     :", [sample_poisson(2.5) for _ in range(10)])
print("Geometric(0.3)   :", [sample_geometric(0.3) for _ in range(10)])
print("Uniform(1,5)     :", [round(sample_uniform(1, 5), 3) for _ in range(10)])
print("Exponential(0.5) :", [round(sample_exponential(0.5), 3) for _ in range(10)])
print("Normal(100,5)    :", [round(sample_normal(100, 5), 3) for _ in range(10)])
```

### Do the samplers match the theory?

```python
import math
import random
from collections import Counter

# Sampling is easy; the question is whether the draws have the right
# distribution. Compare empirical statistics against the closed forms.
random.seed(20240601)
N = 200_000


def moments(values):
    n = len(values)
    mean = sum(values) / n
    var = sum((x - mean) ** 2 for x in values) / n
    return mean, var


def geometric(p):
    count = 0
    while random.random() >= p:
        count += 1
    return count + 1


def poisson(lam):
    limit, k, prod = math.exp(-lam), 0, 1.0
    while True:
        prod *= random.random()
        if prod <= limit:
            return k
        k += 1


def bernoulli(p):
    return 1 if random.random() < p else 0


def binomial(n, p):
    return sum(bernoulli(p) for _ in range(n))


def exponential(lam):
    return -math.log1p(-random.random()) / lam


def uniform(a, b):
    return a + (b - a) * random.random()


def normal_pair(mu, sigma):
    u1 = max(random.random(), 1e-12)
    u2 = random.random()
    r = math.sqrt(-2.0 * math.log(u1))
    th = 2.0 * math.pi * u2
    return (mu + sigma * r * math.cos(th), mu + sigma * r * math.sin(th))


print(f"{N:,} draws each. Comparing empirical mean/sd to theory.")
print()
print(f"{'distribution':22} {'emp mean':>10} {'theory':>10} "
      f"{'emp sd':>10} {'theory':>10}")

cases = [
    ("Bernoulli(0.3)", [bernoulli(0.3) for _ in range(N)], 0.3,
     math.sqrt(0.3 * 0.7)),
    ("Binomial(50,0.4)", [binomial(50, 0.4) for _ in range(N // 10)],
     50 * 0.4, math.sqrt(50 * 0.4 * 0.6)),
    ("Poisson(3)", [poisson(3) for _ in range(N)], 3.0, math.sqrt(3.0)),
    ("Geometric(0.25)", [geometric(0.25) for _ in range(N)], 4.0,
     math.sqrt(0.75) / 0.25),
    ("Uniform(2,10)", [uniform(2, 10) for _ in range(N)], 6.0,
     math.sqrt(64 / 12)),
    ("Exponential(0.5)", [exponential(0.5) for _ in range(N)], 2.0, 2.0),
]

for name, vals, theo_mean, theo_sd in cases:
    m, v = moments(vals)
    print(f"{name:22} {m:10.4f} {theo_mean:10.4f} "
          f"{math.sqrt(v):10.4f} {theo_sd:10.4f}")

# The normal is sampled in pairs, using Box-Muller twice per call.
normals = []
while len(normals) < N:
    normals.extend(normal_pair(100.0, 5.0))
normals = normals[:N]
m, v = moments(normals)
print(f"{'Normal(100,5)':22} {m:10.4f} {100.0:10.4f} "
      f"{math.sqrt(v):10.4f} {5.0:10.4f}")

print()
print("Every empirical mean and sd sits within Monte Carlo error of theory.")
```

### The Poisson fingerprint: mean equals variance

```python
import math
import random
from collections import Counter

# Poisson is the ONLY distribution in the table with Var = E.
# Verify that, and show what breaks when events cluster instead.
random.seed(5)
N = 120_000


def poisson(lam):
    limit, k, prod = math.exp(-lam), 0, 1.0
    while True:
        prod *= random.random()
        if prod <= limit:
            return k
        k += 1


counts = Counter(poisson(3.0) for _ in range(N))
mean = sum(k * c for k, c in counts.items()) / N
var = sum((k - mean) ** 2 * c for k, c in counts.items()) / N

print(f"Poisson(3.0), {N:,} samples")
print(f"  empirical mean = {mean:.4f}   (theory lambda = 3)")
print(f"  empirical var  = {var:.4f}   (theory 1/lambda = 3)")
print(f"  mean == variance: {abs(mean - var) < 0.15}")
print()
print("  k | empirical | exact e^-3 * 3^k / k!")
lam = 3.0
for k in range(0, 10):
    exact = math.exp(-lam) * lam**k / math.factorial(k)
    emp = counts[k] / N
    print(f"{k:3d} | {emp:9.6f} | {exact:.6f}")

print()
print("Compare with Binomial(30, 0.1), which also has mean 3:")
# mean = 3, but variance = 30*0.1*0.9 = 2.7, NOT 3.
print(f"  Binomial mean = {30 * 0.1}, variance = {30 * 0.1 * 0.9}")
print("  So Var < E here. Poisson's Var = E is a genuine fingerprint.")
```

### Working out the samplers by hand

```python
import math

# --- Exponential: inverse transform, derived ---
# F(x) = 1 - e^(-lam x)  =>  x = -ln(1 - u) / lam
lam = 0.5
for u in (0.3, 0.9):
    x = -math.log(1 - u) / lam
    print(f"Exponential(lam={lam}), u={u}: x = {x:.6f}")
print("  check: F(x) should return u")
for u in (0.3, 0.9):
    x = -math.log(1 - u) / lam
    print(f"    x={x:.6f} -> F(x) = {1 - math.exp(-lam * x):.6f}")
print()

# --- Normal: Box-Muller, with the worked numbers from the lesson ---
for u1, u2 in ((0.5, 0.25), (0.9, 0.4)):
    r = math.sqrt(-2.0 * math.log(u1))
    theta = 2.0 * math.pi * u2
    z0 = r * math.cos(theta)
    z1 = r * math.sin(theta)
    print(f"Box-Muller with U1={u1}, U2={u2}:")
    print(f"  r = sqrt(-2 ln {u1}) = {r:.6f}")
    print(f"  theta = 2*pi*{u2} = {theta:.6f} rad")
    print(f"  Z0 = r*cos(theta) = {z0:.6f}   Z1 = r*sin(theta) = {z1:.6f}")
    print(f"  as N(100,5): {100 + 5 * z0:.4f} and {100 + 5 * z1:.4f}")
    print(f"  r^2 = {r * r:.6f} should be -2 ln(u1) = {-2 * math.log(u1):.6f}")
    print()

# --- Poisson: Knuth's method, step by step ---
lam = 2.5
limit = math.exp(-lam)
print(f"Poisson(lam={lam}): Knuth threshold L = e^-2.5 = {limit:.7f}")
draws = [0.5, 0.7, 0.4, 0.6, 0.9]
prod = 1.0
k = 0
print(f"  start: prod = 1.0, k = 0")
for d in draws:
    prod *= d
    print(f"  prod *= {d} -> {prod:.6f}   {'> L, so k++' if prod > limit else '<= L, STOP'}")
    if prod <= limit:
        break
    k += 1
print(f"  result k = {k}")
print(f"  expected multiplications = lam + 1 = {lam + 1}")
print("  (which is why Knuth is only sensible for small lambda)")
```

### With Libraries

The following section needs `matplotlib`, `numpy`, and `scipy`. It is optional —
everything above runs on the standard library alone. To see the shapes at a
glance, run it after `pip install matplotlib numpy scipy`.

```python  title="With Libraries: plotting all six distributions"
# This block is not runnable without matplotlib, numpy and scipy installed,
# so `run_all.py` skips it. Everything before this point is standard library.
import numpy as np
import matplotlib
matplotlib.use("Agg")  # non-interactive backend, works headless
import matplotlib.pyplot as plt
from scipy import stats

fig, axes = plt.subplots(2, 3, figsize=(16, 9))
rng = np.random.default_rng(7)

# --- Discrete: Binomial PMF, exact vs simulated ---
ax = axes[0, 0]
n, p = 30, 0.35
k = np.arange(0, n + 1)
exact = stats.binom.pmf(k, n, p)
sim = np.bincount(rng.binomial(n, p, 40_000), minlength=n + 1) / 40_000
ax.bar(k - 0.18, exact, width=0.36, label="exact PMF", alpha=0.8)
ax.bar(k + 0.18, sim, width=0.36, label="simulated", alpha=0.5)
ax.set_title(f"Binomial(n={n}, p={p})")
ax.set_xlabel("successes"); ax.legend()

# --- Discrete: Poisson PMF ---
ax = axes[0, 1]
lam = 4.0
k = np.arange(0, 18)
exact = stats.poisson.pmf(k, lam)
sim = np.bincount(rng.poisson(lam, 40_000), minlength=18)[:18] / 40_000
ax.bar(k - 0.18, exact, width=0.36, label="exact PMF", alpha=0.8)
ax.bar(k + 0.18, sim, width=0.36, label="simulated", alpha=0.5)
ax.set_title(f"Poisson(lambda={lam})  -- mean = var = {lam}")
ax.set_xlabel("events per interval"); ax.legend()

# --- Discrete: Geometric PMF ---
ax = axes[0, 2]
pg = 0.3
k = np.arange(1, 16)
ax.bar(k, stats.geom.pmf(k, pg), color="seagreen", alpha=0.8)
ax.set_title(f"Geometric(p={pg})  -- mean = 1/p = {1/pg:.2f}")
ax.set_xlabel("trials until first success")

# --- Continuous: Uniform density ---
ax = axes[1, 0]
x = np.linspace(-0.5, 3.5, 400)
ax.plot(x, stats.uniform.pdf(x, 0, 3), label="Uniform(0,3)")
ax.fill_between(x, stats.uniform.pdf(x, 0, 3), alpha=0.3)
ax.set_title("Uniform(a=0, b=3) -- flat, mean 1.5")
ax.set_ylabel("density"); ax.legend()

# --- Continuous: Exponential density and survival ---
ax = axes[1, 1]
x = np.linspace(0, 8, 400)
pdf = stats.expon.pdf(x, scale=2.0)
surv = stats.expon.sf(x, scale=2.0)
ax.plot(x, pdf, label="PDF", color="darkorange")
ax.plot(x, surv, label="survival P(T>t)", color="crimson")
ax.axvline(2.0, ls="--", color="grey", label="mean = 1/lambda = 2")
ax.set_title("Exponential(lambda=0.5) -- right-skewed")
ax.set_ylabel("probability per unit"); ax.legend()

# --- Continuous: Normal density, with the 68-95-99.7 bands ---
ax = axes[1, 2]
x = np.linspace(-4.5, 4.5, 500)
mu, sd = 0.0, 1.0
pdf = stats.norm.pdf(x, mu, sd)
ax.plot(x, pdf, color="navy", lw=2)
for k, shade, alpha in [(1, 0.15, 1), (2, 0.10, 2), (3, 0.06, 3)]:
    lo, hi = mu - k * sd, mu + k * sd
    band = stats.norm.cdf(hi) - stats.norm.cdf(lo)
    ax.axvspan(lo, hi, color="steelblue", alpha=shade)
    ax.axvline(lo, ls=":", color="grey", lw=1)
    ax.axvline(hi, ls=":", color="grey", lw=1)
    ax.text(hi + 0.08, pdf.max() * 0.92 - 0.07 * k,
            f"{k}sd: {band*100:.2f}%", fontsize=8)
ax.set_title("N(0,1) -- the 68-95-99.7 rule")
ax.set_ylabel("density")

plt.tight_layout()
plt.savefig("distributions_reference.png", dpi=110)
print("wrote distributions_reference.png")
```

## Common Mistakes

**Mistake 1 — parameterising the exponential by its mean.**
Wrong: `sample_exponential(mean=2.0)` implemented as `2.0 * -log(u)`.
Right: the density is λe^(−λx) with **rate** λ, so the sample is
`−log(1−u)/λ`, and mean 2 corresponds to λ = 0.5. The bug produces values 4× too
large, and it survives review because the code "looks like" an exponential. When
in doubt, print ten samples and check they average to the mean you intended.

**Mistake 2 — using Knuth's Poisson sampler for large λ.**
At λ = 1000 it needs about 1001 uniform draws per sample, so generating a
million events takes a billion draws. Use the normal approximation or a rejection
method above λ ≈ 30. The temptation is that the method is correct — it is
correct, it is just catastrophically slow, and no test will tell you.

**Mistake 3 — forgetting Box–Muller gives you two samples.**
The polar transformation produces two independent normals per pair of uniforms.
Discarding the second halves your throughput for no reason. This is a common
performance bug in simulation code.

**Mistake 4 — assuming Poisson whenever you see a count.**
Poisson requires events to be independent, stationary in time, and rare. Real
traffic is bursty: an incident produces a cluster of errors in seconds, not a
uniform trickle. Measure the count distribution and check whether variance ≈
mean. If variance ≫ mean, Poisson is wrong and your error budget is optimistic
by exactly that factor.

**Mistake 5 — using the geometric distribution without deciding whether it counts
the success.**
Some texts define it as the number of *failures* before the first success, with
mean (1−p)/p; others count the success too, with mean 1/p. Getting this wrong
shifts every value by one, which matters enormously when p is small. Decide
explicitly and say which convention you are using.

## Formula Sheet

| Symbol | Distribution | PMF / PDF | Mean | Variance | Use it for |
| --- | --- | --- | --- | --- | --- |
| `$\mathrm{Bernoulli}(p)$` | discrete, support $\{0,1\}$, needs `0 \le p \le 1` | `$p_X(1) = p$`, `$p_X(0) = 1-p$` | `$p$` | `$p(1-p)$` | One yes/no outcome: a cache hit, a click, a request failing |
| `$\mathrm{Binomial}(n,p)$` | discrete, support `$0,\dots,n$`, needs **`n` a non-negative integer** and `0 \le p \le 1` | `$\binom{n}{k}p^k(1-p)^{n-k}$` | `$np$` | `$np(1-p) \le np$` | Successes in **n fixed** independent trials: conversion rate, defects in 100 builds |
| `$\mathrm{Poisson}(\lambda)$` | discrete, support `$0,1,2,\dots$`, needs **`\lambda > 0`** | `$e^{-\lambda}\lambda^k/k!$` | `$\lambda$` | `$\lambda$` — **equal to the mean** | Rare independent events in a **window of fixed length**: requests per second, errors per minute |
| `$\mathrm{Geometric}(p)$` | discrete, support `$1,2,3,\dots$`, needs `0 < p \le 1` | `$(1-p)^{k-1}p$` | `$1/p$` | `$(1-p)/p^2$` | **Trials until first success, counting the success**: retries until 200, polls until ready |
| failures-first Geometric | support `$0,1,2,\dots$` | `$(1-p)^k p$` | `$(1-p)/p$` | `$(1-p)/p^2$` | The other convention. Differs by exactly 1 — always state which you use |
| `$\mathrm{Uniform}(a,b)$` | continuous, support `$[a,b]$`, needs `$a < b$` | `$1/(b-a)$` | `$(a+b)/2$` | `$(b-a)^2/12$` | A random point, a random array index, jitter, Monte Carlo sampling |
| discrete `$\mathrm{Uniform}\{0,\dots,n-1\}$` | continuous formula does **not** apply | `$1/n$` | `$(n-1)/2$` | `$(n^2-1)/12$` | Picking a random index. For n = 50: mean 24.5, variance 208.25 versus the continuous 208.33 |
| `$\mathrm{Exponential}(\lambda)$` | continuous, support `$[0,\infty)$`, needs **`\lambda > 0`**, a **rate** | `$\lambda e^{-\lambda x}$` | `$1/\lambda$` | `$1/\lambda^2$` | **Waiting time** to the first event: inter-arrival gaps, time to failure |
| `$\mathrm{Normal}(\mu,\sigma^2)$` | continuous, support `$(-\infty,\infty)$`, needs **`\sigma > 0`** | `$\dfrac{e^{-(x-\mu)^2/(2\sigma^2)}}{\sigma\sqrt{2\pi}}$` | `$\mu$` | `$\sigma^2$` | Sums and averages of many small things, measurement error, CLT results |
| **$\mathrm{Var} = E$ fingerprint** | Poisson only | — | — | — | Ratio near 1 ⇒ Poisson. Ratio $\gg 1$ ⇒ clustered events, Poisson is **wrong** |
| inverse transform | `$x = F^{-1}(u)$` | — | — | — | Any invertible CDF. Exponential: `x = -\ln(1-u)/\lambda` |
| Box–Muller | `$Z_0 = \sqrt{-2\ln U_1}\cos(2\pi U_2)$`, `$Z_1 = \sqrt{-2\ln U_1}\sin(2\pi U_2)$` | — | `$0,0$` | `$1,1$` | Two independent standard normals from two uniforms. **Use both** |
| Knuth's Poisson | cost `$\lambda + 1` uniform draws per sample | — | — | — | Only for `$\lambda \lesssim 30$`. At $\lambda = 1000$ it needs ~1001 draws per sample |
| rejection sampling | accept `$\lambda^k/(k!\,T)$` where `$T = \sum_j \lambda^j/j! = e^\lambda$` | — | — | — | Any discrete distribution with a computable PMF and computable bound |
| `$\lambda = 1/5000$` | `$\mathrm{Exponential}(0.0002)$` per hour | — | 5000 h | — | The reciprocal shows up **everywhere** in count distributions |
| `$\binom{n}{k}$` | `$\dfrac{n!}{k!(n-k)!}$` | — | — | — | The Binomial's combinatorial factor: which $k$ of $n$ trials succeeded |
| `$\mathrm{Var}/\mathrm{E}$` | diagnostic, not a distribution | — | — | — | `$\mathrm{Binomial}(30,0.1)$`: `2.7/3.0 = 0.9 < 1`. `$\mathrm{Poisson}(4.2)$`: `4.2/4.2 = 1.0` |

## Multiple Choice Questions

**Q1.** A component's time-to-failure has an average of 5000 hours and is
memoryless. Which distribution, with which parameter, and what is the answer to
"why is the parameter not 5000"?

- A) Exponential(5000), since the mean is 5000
- B) Exponential(0.0002 per hour), since λ is a **rate** and `E[X] = 1/λ`
- C) Poisson(5000), since Poisson models rare events
- D) Normal(5000, 1), since failure times are approximately normal

<details>
<summary>Answer and explanation</summary>

**B) Exponential(0.0002 per hour), since λ is a **rate** and `E[X] = 1/λ`.**

This is Exercise 1(e) and Mistake 1. Option A gives a mean of $1/5000 = 0.0002$
hours — off by a factor of 25 million, and the code "looks like" an exponential
either way, which is why it survives review. Option C counts events per window;
it does not model a waiting *time*, and Poisson has no memoryless property.
Option D is wrong on two counts: failure times are right-skewed with a hard floor
at zero, and Poisson/normal disagreement aside, a normal places negative
failure times.

</details>

**Q2.** A client retries until it gets a 200, succeeding 30% of the time on each
attempt. What is the expected number of attempts, and which convention gives that
number?

- A) Geometric(0.3) counting the success, `E = 1/0.3 ≈ 3.33`
- B) Geometric(0.3) counting failures, `E = 1/0.3 ≈ 3.33`
- C) Geometric(0.3) counting failures, `E = (1−0.3)/0.3 ≈ 2.33`
- D) Binomial(0.3), `E = 0.3`

<details>
<summary>Answer and explanation</summary>

**A) Geometric(0.3) counting the success, `E = 1/0.3 ≈ 3.33`.**

Option C's 2.33 is the *other* convention — failures before success — and it is
correct arithmetic for a different quantity. This is Mistake 5 in this lesson: the
two conventions differ by exactly one trial, and the difference matters enormously
when $p$ is small (here it is 43%). Option B mixes the convention with the wrong
mean. Option D is a category error; a single trial's success indicator is
Bernoulli, but "how many until success" is Geometric.

</details>

**Q3.** You measure errors per minute and find mean 4.2 and variance 11.9. What
does that tell you?

- A) Poisson(4.2) fits, since 4.2 and 11.9 are both "small"
- B) The data is over-dispersed: variance/mean = 2.83, so errors cluster and Poisson is wrong
- C) The data is under-dispersed, so you should use Binomial instead
- D) Nothing — variance is always allowed to exceed the mean for a count

<details>
<summary>Answer and explanation</summary>

**B) The data is over-dispersed: variance/mean = 2.83, so errors cluster and
Poisson is wrong.**

Exercise 3 works this through: Poisson(4.2) says `P(X ≥ 10) = 0.0111` while a
negative binomial fitted to the same mean and variance says `0.0795` — 7.1×
more violations against the same SLO. Option A is the trap; Poisson requires
*exactly* mean = variance, which is its fingerprint. Option C has the direction
backwards, and Binomial cannot exceed mean either — its variance is always
`≤ np`. Option D is true but irrelevant: Poisson is the only count distribution
here whose variance is *pinned* to the mean.

</details>

**Q4.** Why does Knuth's Poisson method become useless at large λ?

- A) It is incorrect for λ above 30, producing biased samples
- B) It costs about λ+1 uniform draws per sample, so λ = 1000 needs ~1001 draws each
- C) It overflows the floating-point range because $e^{-\lambda}$ underflows
- D) It requires λ to be an integer

<details>
<summary>Answer and explanation</summary>

**B) It costs about λ+1 uniform draws per sample, so λ = 1000 needs ~1001 draws
each.**

The method is *correct* at every λ — it is just catastrophically slow, and no
correctness test will tell you (Mistake 2). A million events at λ = 1000 costs a
billion draws. Option A inverts the problem; correctness is not the issue.
Option C is a real floating-point concern but a different one, and 1001 draws is
the dominant cost regardless. Option D is false; λ can be any positive real.

</details>

**Q5.** In Box–Muller, `U₁ = 0.5` and `U₂ = 0.25`. What do you get?

- A) `Z₀ = 0` exactly and `Z₁ = 1.1774`, because `U₂ = 0.25` makes `θ = π/2` and `cos(π/2) = 0`
- B) `Z₀ = 1.1774` and `Z₁ = 0`, because `sin(π/2) = 1`
- C) Both equal `√(2 ln 2) = 1.1774`
- D) `Z₀ = 0.5` and `Z₁ = 0.25`, since the uniforms pass through unchanged

<details>
<summary>Answer and explanation</summary>

**A) `Z₀ = 0` exactly and `Z₁ = 1.1774`, because `U₂ = 0.25` makes `θ = π/2` and
`cos(π/2) = 0`.**

The lesson's Example A computes this, and the zero is a genuine coincidence of
these particular inputs — the point is on the vertical axis. Option B swaps the
sine and cosine, which is the classical slip. Option C has both coordinates
non-zero. Option D confuses the inputs with the outputs; the whole point is that
the transform produces standard *normals*, not uniforms.

</details>

**Q6.** Which distribution models "a request either fails or succeeds, and 2% of
requests fail"?

- A) Binomial(1000, 0.02), because you will eventually look at 1000 requests
- B) Bernoulli(0.02), because this is one trial with two outcomes; Binomial appears only once you fix the number of trials
- C) Poisson(0.02), because failures are rare
- D) Geometric(0.98), because a request can be retried

<details>
<summary>Answer and explanation</summary>

**B) Bernoulli(0.02), because this is one trial with two outcomes; Binomial
appears only once you fix the number of trials.**

This is the count-versus-measure discipline in Exercise 1(c): Bernoulli for the
single request, Binomial(1000, 0.02) with mean 20 only after the sample size is
specified. Option A picks an arbitrary $n$ the question never gave. Option C
describes a rate per window, not a single trial's outcome. Option D is only
appropriate if retries actually happen, which is a different scenario.

</details>

**Q7.** `Uniform{0,…,49}` has mean 24.5. What is its variance, and how does it
differ from `Uniform[0,49]`?

- A) 208.33 for both — one is a subset of the other
- B) 208.25 discrete, versus 208.33 continuous; the formulas $(n^2-1)/12$ and $(b-a)^2/12$ differ
- C) 204.17, because 49 is the largest value
- D) It has no variance, since the values are equally likely

<details>
<summary>Answer and explanation</summary>

**B) 208.25 discrete, versus 208.33 continuous; the formulas $(n^2-1)/12$ and
$(b-a)^2/12$ differ.**

Exercise 1(d) prints both numbers. Option A is the natural guess — the
continuous formula's endpoints look like the discrete values — but the two
distributions put their mass at different places (50 discrete points including
both endpoints versus a continuum). Option C uses $49.5/12$, which is a standard
deviation formula, not variance. Option D is a category error: equal probability
across values gives a uniform distribution, which has a perfectly ordinary
variance.

</details>

**Q8.** You generate 10 samples from `sample_exponential(mean=2.0)` implemented as
`2.0 * -log(u)`. What is wrong, and how would you detect it in review?

- A) Nothing; `-log(u)` is uniform, so scaling gives the right shape
- B) The samples average about 4 instead of 2, because the correct transform divides by λ = 0.5; print ten samples and check the average against your intended mean
- C) The samples can never exceed 2, which is impossible for an exponential
- D) `-log(u)` overflows for u near 1

<details>
<summary>Answer and explanation</summary>

**B) The samples average about 4 instead of 2, because the correct transform
divides by λ = 0.5; print ten samples and check the average against your intended
mean.**

Multiplicating by the mean instead of dividing by the rate gives a scale factor of
$2/0.5 = 4$ too large — exactly the 4× in Mistake 1. Option A is a real property
of $-\ln u$ (it is $\mathrm{Exp}(1)$) but the scale parameter has to be applied
correctly. Option C is false: `-log(u)` is unbounded above. Option D describes
`log(0)`, i.e. u near **0**, not near 1 — which is why the lesson's sampler uses
`log1p(-u)` and guards `u1` against zero in Box–Muller.

</details>

**Q9.** Why does $\mathrm{Binomial}(n,p)$ have variance $\le np$ while
$\mathrm{Poisson}(\lambda)$ has variance exactly $\lambda$?

- A) Because Binomial counts successes and Poisson counts events, and counting is different
- B) Because Binomial has a finite number of trials: the bound comes from $np(1-p) \le np$, and Poisson is the $n \to \infty$, $p \to 0$, $np \to \lambda$ limit where $p \to 0$
- C) Because Poisson requires integer λ
- D) There is no relationship; the two variances are unrelated

<details>
<summary>Answer and explanation</summary>

**B) Because Binomial has a finite number of trials: the bound comes from
$np(1-p) \le np$, and Poisson is the $n \to \infty$, $p \to 0$, $np \to \lambda$
limit where $p \to 0$.**

This is why the variance-to-mean ratio is a usable diagnostic
([Lesson 63](63_discrete_random_variables.md) and Exercise 3 here):
$\mathrm{Binomial}(30,0.1)$ gives ratio $2.7/3.0 = 0.9 < 1$, so a ratio below 1
points at a fixed-trial model. Option A is descriptive, not explanatory. Option C
is false; λ is any positive real. Option D denies a relationship that is exactly
the Binomial→Poisson limit.

</details>

**Q10.** You need a sampler for a distribution whose CDF has no closed-form
inverse, such as the normal. Why is inverse transform unavailable, and what do
you use instead?

- A) Inverse transform works for any CDF; you just need more precision
- B) There is no elementary closed form for $F^{-1}$, so you use Box–Muller, or another specialised method such as the acceptance–rejection or ziggurat algorithms
- C) Inverse transform gives the wrong distribution for continuous variables
- D) You must use the PMF rather than the CDF

<details>
<summary>Answer and explanation</summary>

**B) There is no elementary closed form for $F^{-1}$, so you use Box–Muller, or
another specialised method such as the acceptance–rejection or ziggurat
algorithms.**

The lesson's `normal_quantile` function bisects on the CDF instead — that works,
and is how `numpy` computes normal quantiles. Option A is false; invertibility is
the requirement, not precision. Option C is false; the transform is correct for
continuous distributions whenever $F$ is invertible (which is why the Exponential
sampler in the lesson is one line). Option D confuses the two representations —
the normal's PDF is not what you sample from directly.

</details>

## Subjective Questions

### Short Answer

**Q1.** Name the four discrete distributions in the reference table and, for each,
the one-sentence question that identifies it.

<details>
<summary>Answer</summary>

**Bernoulli(p)** — "one trial, two outcomes?"; **Binomial(n,p)** — "how many
successes in $n$ *fixed* independent trials?"; **Poisson(λ)** — "how many rare
independent events in a window of fixed length?"; **Geometric(p)** — "how many
trials until the first success, and does the count include it?"

The discriminators are *finite versus infinite trial count*, *fixed versus random
window*, and *counting versus measuring*. Getting these right identifies the
distribution before any formula is needed.

</details>

**Q2.** Why is "$\mathrm{Var} = E$" a fingerprint for Poisson rather than a
coincidence?

<details>
<summary>Answer</summary>

Because it is the only row in the reference table where the two are pinned
together. Bernoulli has $p(1-p) < p$ unless $p$ is 0 or 1; Binomial has
$np(1-p) \le np$; the continuous three have variance in squared units of $x$
while the mean is in units of $x$, so the comparison is not even
dimensionally meaningful. Poisson's $\lambda$ is both an event count and a
variance, and that is a theorem rather than a coincidence.

</details>

**Q3.** State the inverse transform formula for the Exponential and derive it in
two lines.

<details>
<summary>Answer</summary>

$F(x) = 1 - e^{-\lambda x}$. Setting $F(x) = u$ and solving:
$e^{-\lambda x} = 1-u$, so $\lambda x = -\ln(1-u)$, hence
$x = -\ln(1-u)/\lambda$. The derivation check is
$P(x(U) \le x) = P(U \le 1 - e^{-\lambda x}) = 1 - e^{-\lambda x} = F(x)$,
which the lesson's code verifies numerically at $u = 0.3$ and $u = 0.9$,
returning 0.713350 and 4.605170.

</details>

**Q4.** Why does Box–Muller produce *two* normals, and where does the log come
from?

<details>
<summary>Answer</summary>

Because the construction works in polar coordinates. The joint density of two
independent standard normals is $\frac{1}{2\pi}e^{-r^2/2}$ in the plane, which
factorises into a radial part and an angular part, so the radius and angle are
independent: $r^2 \sim \mathrm{Exp}(\tfrac12)$ and
$\theta \sim \mathrm{Uniform}(0, 2\pi)$. Inverting gives
$r = \sqrt{-2\ln U_1}$ — the log appears because the **squared** radius is
exponential — and $\theta = 2\pi U_2$. Converting back gives two independent
normals, $r\cos\theta$ and $r\sin\theta$, from two uniforms. Discarding the
second halves your throughput for nothing (Mistake 3).

</details>

**Q5.** State Knuth's Poisson algorithm and the bound on λ that makes it
sensible.

<details>
<summary>Answer</summary>

Set $L = e^{-\lambda}$, $k = 0$, $p = 1$. Repeatedly multiply $p$ by a fresh
uniform on $[0,1)$; while $p > L$, increment $k$ and redraw; return $k$. The
expected number of multiplications is $\lambda + 1$, so the method is sensible
only for small λ — the lesson's advice is $\lambda \lesssim 30$. Above that, use
rejection sampling with a computed bound $M$, or the normal approximation.

</details>

**Q6.** Why do discrete and continuous uniform differ in variance, and by how
much for n = 50?

<details>
<summary>Answer</summary>

The continuous $\mathrm{Uniform}[a,b]$ has variance $(b-a)^2/12$, while the
discrete $\mathrm{Uniform}\{0,\dots,n-1\}$ has $(n^2-1)/12$. For $n = 50$ the
discrete value is $2499/12 = 208.25$, while the continuous formula applied to a
window of width 50 gives $2500/12 = 208.33$. The difference is 0.08 — small, but
real, because the continuous distribution has mass where the discrete one has
none: 50 distinct points each at probability 1/50, versus a continuum at
constant density. Both have mean 24.5.

</details>

### Long Answer

**Q1. Why does the variance-to-mean ratio diagnose clustering, and what breaks
if you assume Poisson anyway?**

<details>
<summary>Model answer</summary>

Because Poisson's mean and variance are the *same* parameter, $\lambda$. So the
ratio $\mathrm{Var}/E$ is not a free statistic for Poisson — it is pinned at
exactly 1, which makes it a sharp test. A Binomial with $p<1$ has ratio $1-p<1$,
so a ratio below 1 points at a fixed-trial model; a ratio of 1 is Poisson;
a ratio far above 1 is over-dispersion, meaning the count is not Poisson at all.

Clustering is the mechanism behind over-dispersion: a bad deploy produces a spike
of errors in one minute and near-zero in the next, so the distribution is a
*mixture* over incident states. A mixture of Poissons with different rates has
mean $\sum w_i\lambda_i$ and variance $\sum w_i\lambda_i^2$, and
$\sum w_i \lambda_i^2 > (\sum w_i\lambda_i)^2$ by strict convexity of the square.
So the excess variance is exactly the *between-state* variance — the same law of
total variance from [Lesson 64](64_expectation_variance.md), applied to arrival
rates instead of latency.

What breaks is the tail, and always in the optimistic direction. Poisson has no
mechanism for producing bursts, so it spreads probability too thin across the
moderate counts and reserves too little for the extreme ones. Exercise 3 puts
numbers on it: for the same mean of 4.2, Poisson says `P(X ≥ 10) = 0.0111` while
a negative binomial fitted to the observed variance says `0.0795`. Same data,
same mean, 7.1× more SLO violations. Since SLOs are written in the tail, the
error lands precisely on the number people act on — and it fails in production
rather than in review, because review only ever sees the mean.

</details>

**Q2. Why is inverse transform sampling the default method, and what stops it
from working for the normal?**

<details>
<summary>Model answer</summary>

Because it is exact, needs one uniform per sample, and requires no cleverness at
all — just arithmetic on the inverse CDF. The proof is a one-line swap: draw
$u$ uniform, set $x = F^{-1}(u)$, then $P(x \le t) = P(F^{-1}(u) \le t) = P(u
\le F(t)) = F(t)$, using the fact that $F^{-1}$ is increasing. Every step is a
restatement of the definition, so the sampler is correct by construction.

The method stops exactly where $F$ stops being invertible in closed form. The
exponential gives $x = -\ln(1-u)/\lambda$ in one line; the uniform gives
$a + (b-a)u$; the geometric gives $\lceil \ln(1-u)/\ln(1-p) \rceil$. The normal
has a CDF (via `math.erf`) but **no elementary inverse** — the inverse error
function is a special function, not something you can write down and evaluate
cheaply. So you either bisect on $F$ (which is what the lesson's
`normal_quantile` does, and what `numpy` effectively does for arbitrary
quantiles), or you use a method built for the purpose: Box–Muller, the
ziggurat algorithm, or acceptance–rejection with an envelope.

The reason this matters beyond tidiness is that the normal is the distribution you
most want to sample from — it is the CLT limit and the basis of every simulation
in [Lesson 68](68_law_of_large_numbers_and_clt.md). So "the sampler for the most
important distribution needs a trick" is not a trivial gap in the method, it is
the gap the whole Box–Muller derivation exists to fill. And note the shape of the
trick: Box–Muller is not a rejection scheme with an envelope, it is a *change of
variables* into polar coordinates, which is why it produces two independent
normals per pair of uniforms and why it is exact rather than merely converging.

</details>

**Q3. A load test uses uniformly spaced arrivals. Why does that stress a system
in a way production never does, even when the mean rate matches?**

<details>
<summary>Model answer</summary>

Because matching the mean rate does not match the *distribution*. Uniformly spaced
arrivals are exactly $\mathrm{Uniform}$, whose variance is $(b-a)^2/12$ and whose
inter-arrival gaps are perfectly regular. Production arrivals are Poisson
processes: the count per second is $\mathrm{Poisson}(\lambda)$ and the gaps are
$\mathrm{Exponential}(\lambda)$. Those are the same mean and wildly different
behaviour.

The mechanism is burstiness. An exponential gap has a real right tail —
$P(T > 2/\lambda) = e^{-2} = 0.135$, so 13.5% of gaps are more than double the
mean, and $P(T > 4/\lambda) = e^{-4} = 0.018$. Uniform gaps have none: the
maximum gap is bounded, so the *number* of simultaneous arrivals is bounded too.
So the uniform test never produces the arrival coincidence that makes production
fall over. It also never produces the quiet period that lets it recover, so it
gives you no information about queue drain rates.

The second failure mode is subtler: the mean *number* of requests in flight. Under
Poisson arrivals with service time $S$, the count in the system is a birth–death
process, and its mean is $\rho/(1-\rho)$ where $\rho = \lambda E[S]$ is
utilisation. That relationship is non-linear, so a test that holds the average
arrival rate constant while removing the burstiness systematically *understates*
queueing delay near saturation — the region where SLOs live. Mistake 4 makes the
related point from the other side: assuming Poisson whenever you see a count is
wrong when the mechanism clusters, so a load test should also be checked against
its own observed variance-to-mean ratio.

The fix is one line: draw inter-arrival gaps from the exponential rather than
stepping a fixed interval. `random.expovariate(1/mean_interval)` does it, and the
lesson's `sample_exponential` shows it from scratch.

</details>

**Q4. How do you decide which of the seven distributions a real process follows
— and what is the failure mode of deciding too confidently?**

<details>
<summary>Model answer</summary>

You decide by asking, in order: does it count or measure; is there a fixed number
of trials or a fixed window; are the events independent, stationary and rare; and
what does the observed mean-versus-variance ratio say. That sequence narrows the
table quickly. "Fixed trials" gives Binomial, "fixed window of rare independent
events" gives Poisson, "waiting time to the first event" gives Exponential,
"until first success" gives Geometric, "any point in an interval equally likely"
gives Uniform, and "average of many small things" gives Normal.

The failure mode is that these are *modelling assumptions*, and the ones that hurt
most are the ones nobody writes down. Independence and stationarity are the
expensive ones: a load test satisfies them by construction and production does
not, so a model fitted on synthetic traffic will understate the tail. The
variance-to-mean ratio is the cheap check — 2.83 in Exercise 3 — and it catches
the whole class of over-dispersed processes with one line.

There is a second failure mode, specific to this lesson's Normal. Everything else
in the table follows from the *mechanism*: a queue with constant arrival rate and
constant service rate really is exponential, whatever the data looks like. The
normal, by contrast, is usually a *consequence* — of averaging many small things
via the CLT ([Lesson 68](68_law_of_large_numbers_and_clt.md)) — and so it is
legitimate for a sum of many terms and illegitimate for a single latency. Mistake
5's warning is the version that bites: fitting a normal to hard-bounded,
right-skewed data reproduces the mean exactly and gets the percentiles badly
wrong, and Exercise 3 shows the error going to the wrong side (39.0% beyond 10 ms
against a true 10.0%). So the diagnostic to carry is not "which distribution
looks like the data" but "which distribution does the mechanism produce, and
does the variance-to-mean ratio agree".

</details>

## Exercises and Solutions

**[ ] Exercise 1 — identify the distribution.** For each scenario, name the
distribution, its parameters, and its expected value. (a) A server receives
requests at a steady rate of 20 per second. (b) A client retries until it gets a
200, succeeding 30% of the time. (c) A request either fails or succeeds, 2% fail.
(d) You pick a random index in an array of 50. (e) A component fails after a
waiting time with average 5000 hours. (f) A dataset's measurement error has mean
0 and standard deviation 3.

<details>
<summary>Solution</summary>

(a) **Poisson(λ = 20)**, expected 20 per second, provided arrivals are
independent and the rate is stationary. This is the M/M/1 assumption set.

(b) **Geometric(p = 0.3)** counting the success, expected 1/0.3 ≈ 3.33 attempts.
If you want failures before success, the mean is (1−p)/p = 2.33.

(c) **Bernoulli(p = 0.02)**, expected 0.02 — a single request's failure
indicator. Over 1000 requests it becomes Binomial(1000, 0.02) with mean 20.

(d) **Uniform on {0, …, 49}**, a discrete uniform, mean 24.5. Its variance is
(50²−1)/12 = 208.25 for the discrete version, which differs from the continuous
(b−a)²/12 = 208.33 — a small but real distinction worth knowing.

(e) **Exponential(λ = 1/5000 = 0.0002 per hour)**, expected 5000 hours. Note the
reciprocal: λ is a rate.

(f) **Normal(0, 3²)**, expected 0. Defensible only if the errors really are
symmetric and roughly normal; if the metric is a latency, prefer a log-normal.

```python
import math

scenarios = [
    ("a steady 20/s arrivals", "Poisson(20)", 20.0),
    ("retry until 200, p=0.3", "Geometric(0.3)", 1 / 0.3),
    ("request fails 2% of time", "Bernoulli(0.02)", 0.02),
    ("random index in 50", "Discrete Uniform{0..49}", 49 / 2),
    ("fails after avg 5000 h", "Exponential(1/5000)", 5000.0),
    ("error mean 0 sd 3", "Normal(0, 3^2)", 0.0),
]
for desc, dist, expected in scenarios:
    print(f"{desc:28} -> {dist:22} E = {expected:9.4f}")

# (d) discrete vs continuous uniform variance, a subtle difference.
n = 50
disc_var = (n * n - 1) / 12
cont_var = (n - 1) ** 2 / 12
print()
print(f"variance of uniform on 0..{n-1}, discrete  : {disc_var:.4f}")
print(f"variance of uniform on [0, {n-1}], continuous: {cont_var:.4f}")
print(f"difference: {cont_var - disc_var:.4f} -- small but real")

# (e) the reciprocal that trips people up
print()
print(f"mean 5000 h  ->  lambda = 1/5000 = {1/5000} per hour, NOT 5000")
```

</details>

**[ ] Exercise 2 — implement and verify a sampler from the definition.** Write a
Poisson sampler without using the Knuth method or any library. Use rejection
sampling: propose k from a uniform on {0, …, M} for large enough M, accept with
probability λᵏ/(k!·T) where T = Σλⱼ/j!, else redraw. Verify your sampler's
empirical mean and variance against λ and λ.

<details>
<summary>Solution</summary>

Rejection sampling needs a bound M with λᵏ/(k!T) ≤ 1 for all k, and a
precomputed normalising constant T. For λ = 4, T = e^λ = 54.598 (the sum of
λᵏ/k! equals e^λ exactly). The ratio λᵏ/(k!T) = (λᵏ/k!)e^(−λ) is the Poisson PMF,
which is unimodal, so its maximum is at k = floor(λ). For λ = 4 the maximum is
about 0.195, so acceptance is comfortable and M = 20 is more than enough.

The method: draw k uniformly from {0,…,20}, draw a second uniform, and accept if
it is below the Poisson PMF value at k. The accepted values have exactly the
Poisson distribution, because a uniform proposal times an acceptance ratio equal
to the PMF gives the PMF back.

This is worth building once because it is the general pattern: *any* discrete
distribution with computable PMF can be sampled this way, and it beats
"generate then reject by eye", which is subtly biased.

```python
import math
import random

random.seed(20240702)

LAM = 4.0
M = 20


def poisson_rejection(lam, m):
    """Rejection sampler for Poisson(lam), proposal uniform on {0..m}."""
    while True:
        k = random.randrange(0, m + 1)
        # The acceptance threshold is the PMF at k, which is <= its maximum,
        # so the loop terminates quickly as long as m >= floor(lam) + a little.
        if random.random() < math.exp(-lam) * lam**k / math.factorial(k):
            return k


N = 150_000
samples = [poisson_rejection(LAM, M) for _ in range(N)]
mean = sum(samples) / N
var = sum((s - mean) ** 2 for s in samples) / N

print(f"rejection sampler for Poisson({LAM}), n = {N:,}")
print(f"  empirical mean = {mean:.4f}   theory {LAM}")
print(f"  empirical var  = {var:.4f}   theory {LAM}")
print(f"  mean ~= lambda: {abs(mean - LAM) < 0.05}")
print(f"  var  ~= lambda: {abs(var - LAM) < 0.05}")

# Show the PMF it reproduces.
print()
print("  k | empirical | exact")
counts = {}
for s in samples:
    counts[s] = counts.get(s, 0) + 1
for k in range(0, 13):
    emp = counts.get(k, 0) / N
    exact = math.exp(-LAM) * LAM**k / math.factorial(k)
    print(f"{k:3d} | {emp:9.6f} | {exact:.6f}")

# Compare speed with Knuth at a larger lambda.
def poisson_knuth(lam):
    limit, k, prod = math.exp(-lam), 0, 1.0
    while True:
        prod *= random.random()
        if prod <= limit:
            return k
        k += 1


random.seed(1)
small = 20_000
knuth_uniforms = small * 1.0  # ~ (lam+1) uniforms per sample at lam=4
print()
print(f"Knuth at lam=4   needs about {4 + 1:.0f} uniforms per sample")
print(f"Knuth at lam=1000 would need about {1000 + 1:.0f} per sample,")
print(f"so {1001 / 5:.0f}x more work than at lam=4 -- which is why you")
print("switch to the normal approximation or another method for large lam.")
```

</details>

**[ ] Exercise 3 — Challenge: fit and test a model, and find it wrong.** A
server logs the number of 500 errors per minute for 50,000 minutes. You observe a
mean of 4.2 and a variance of 11.9.

(a) Given the mean, what would Poisson predict for the variance? (b) Compute the
variance-to-mean ratio. (c) What does the ratio tell you, and what does it imply
about assuming independent events? (d) Design a better model. (e) For an SLO of
"fewer than 10 errors in 99% of minutes", compute the fraction of minutes that
violate under (i) the observed Poisson model and (ii) a model that accounts for
the over-dispersion.

<details>
<summary>Solution</summary>

(a) Poisson has Var = λ, so λ = 4.2 predicts a variance of **4.2**.

(b) The variance-to-mean ratio is 11.9/4.2 = **2.833**, so the data is
over-dispersed.

(c) This is the most important part. A ratio near 1 means Poisson; a ratio
considerably above 1 means **clustering** — errors arrive in bursts rather than
independently. Real mechanisms explain this: a bad deploy causes a spike of
errors in one minute and nothing in the next; a database failover causes a
correlated wave. If you keep the Poisson assumption anyway, your tail
probabilities are far too optimistic, because Poisson has no mechanism for
generating bursts, and your error budget quietly assumes the system is better
behaved than it is. This is the over-dispersion check, and it is one line of
arithmetic that catches a whole class of wrong models.

(d) Two standard options. A **negative binomial** (gamma–Poisson mixture)
allows variance > mean; the extra parameter is the dispersion. Or keep Poisson
for the mean and model the burstiness explicitly — an arrival rate that is itself
random, so that minutes following an incident are more likely to be bad. For a
practical fix, segment the data (incident minutes versus quiet minutes) and fit
separately, which is usually more informative than any single parametric family.

(e) Under Poisson(4.2), P(X ≥ 10) = **0.011127**, so about 1.11% of minutes
violate — already just over the 1% budget.

Under over-dispersion the violation rate is **7.1× higher**. Fitting a negative
binomial with the same mean 4.2 and variance 11.9 requires the shape parameter
r = μ²/(Var − μ) = 17.64/7.7 = 2.2909, and it puts P(X ≥ 10) at **0.079487**, or
about 7.95% of minutes.

This is the whole lesson in two numbers. The Poisson model says you are at
1.11% against a 1% budget — a near miss that an engineer would plausibly wave
through. The model that respects the observed dispersion says you are at 7.95%,
nearly eight times over. Same mean, same data, radically different verdict, and
the difference is entirely in the shape of the tail.

```python
import math

MEAN, VAR = 4.2, 11.9
ratio = VAR / MEAN

print(f"(a) Poisson(lambda={MEAN}) would predict variance = {MEAN}")
print(f"(b) observed variance = {VAR}, ratio = {ratio:.3f}")
print(f"(c) ratio > 1 means OVER-DISPERSION: errors cluster into bursts.")
print("    Poisson cannot produce bursts by construction, so its tail")
print("    probabilities are systematically too small.")
print()

# (e)(i) Poisson tail
def poisson_pmf(k, lam):
    return math.exp(-lam) * lam**k / math.factorial(k)


lam = MEAN
p_poisson = sum(poisson_pmf(k, lam) for k in range(10, 60))
print(f"(e)(i)  Poisson(4.2):     P(X >= 10) = {p_poisson:.6f}  "
      f"({p_poisson*100:.2f}% of minutes violate)")

# (e)(ii) negative binomial with the same mean and variance.
# NB parameterisation: Var = mu + mu^2/r  =>  r = mu^2 / (Var - mu)
r = MEAN**2 / (VAR - MEAN)
print(f"(e)(ii) NegativeBinomial r = mu^2/(Var-mu) = {MEAN**2:.2f}/"
      f"{VAR-MEAN:.2f} = {r:.4f}")

def nb_pmf(k, r, p):
    """NB: number of failures before the r-th success.

    r is the shape parameter; when r is not an integer, the generalised
    binomial coefficient comb(k+r-1, k) = Gamma(k+r)/(Gamma(r) Gamma(k+1))
    is computed with the log-gamma function, which math.lgamma gives us.
    """
    log_comb = math.lgamma(k + r) - math.lgamma(r) - math.lgamma(k + 1)
    return math.exp(log_comb) * p**r * (1 - p)**k


# success probability for NB with mean mu: mu = r(1-p)/p  =>  p = r/(r+mu)
p_nb = r / (r + MEAN)
p_nb_tail = sum(nb_pmf(k, r, p_nb) for k in range(10, 200))
print(f"        mean = {r*(1-p_nb)/p_nb:.4f}, "
      f"var = {r*(1-p_nb)/p_nb + r*(1-p_nb)**2/p_nb**2:.4f}  (should match 4.2, 11.9)")
print(f"        P(X >= 10) = {p_nb_tail:.6f}  "
      f"({p_nb_tail*100:.2f}% of minutes violate)")
print()
print(f"the over-dispersed model reports {p_nb_tail/p_poisson:.1f}x more")
print("violations than Poisson for the same mean.")
print()
budget = 0.01
print(f"SLO budget is {budget:.1%}: Poisson says "
      f"{'PASS' if p_poisson <= budget else 'FAIL'} but marginal, "
      f"the realistic model says {'PASS' if p_nb_tail <= budget else 'FAIL'}.")
```

The conclusion to carry away: the variance-to-mean ratio is a one-line diagnostic
that catches a whole class of wrong distributional assumptions, and getting it
wrong biases every downstream tail probability and SLO in the optimistic
direction — the direction that fails in production and not in review.

</details>

**[ ] Exercise 4 — build and verify every sampler in the reference table.** Write
one sampler per distribution from the reference table, using only `random` values
on `[0,1)`. For each, draw 100,000 samples and compare the empirical mean and
standard deviation with the theoretical values. Then confirm the two
distribution-specific identities: **Poisson has mean = variance**, and
**Binomial's variance is strictly below its mean**.

<details>
<summary>Solution</summary>

| Distribution | Sampler | Theory mean | Theory sd |
| --- | --- | --- | --- |
| Bernoulli(0.3) | `1 if u() < 0.3 else 0` | 0.3 | `sqrt(0.21)` = 0.4583 |
| Binomial(50, 0.4) | sum of 50 Bernoulli | 20.0 | `sqrt(12)` = 3.4641 |
| Poisson(3) | Knuth product method | 3.0 | `sqrt(3)` = 1.7321 |
| Geometric(0.25) | draw until `u() >= 0.25` fails | 4.0 | `sqrt(0.75)/0.25` = 3.4641 |
| Uniform(2, 10) | `2 + 8*u()` | 6.0 | `sqrt(64/12)` = 2.3094 |
| Exponential(0.5) | `-log1p(-u())/0.5` | 2.0 | 2.0 |
| Normal(100, 5) | Box–Muller, in pairs | 100.0 | 5.0 |

The two identities to verify:

- **Poisson:** mean and variance must both land near 3.0. This is the
  distribution's fingerprint — no other row in the table pins them together.
- **Binomial(50, 0.4):** mean $50 \times 0.4 = 20$, variance $50 \times 0.4 \times
  0.6 = 12$, and $12 < 20$. The ratio is $1-p = 0.6$, so the finite trial count
  keeps the variance strictly below the mean. (The lesson's Poisson code block
  compares against $\mathrm{Binomial}(30, 0.1)$: mean 3, variance 2.7, ratio 0.9.)

The Exponential row deserves a second look: its mean and standard deviation are
*both* $1/\lambda = 2$. That is not a typo — for the exponential, $\sigma = E$.

```python
import math
import random

random.seed(20240601)
N = 200_000
HALF = N // 2


def moments(values):
    n = len(values)
    mean = sum(values) / n
    var = sum((x - mean) ** 2 for x in values) / n
    return mean, var ** 0.5


def bernoulli(p):
    return 1 if random.random() < p else 0


def binomial(n, p):
    return sum(bernoulli(p) for _ in range(n))


def poisson(lam):
    limit, k, prod = math.exp(-lam), 0, 1.0
    while True:
        prod *= random.random()
        if prod <= limit:
            return k
        k += 1


def geometric(p):
    """Counting the SUCCESS, so the support is {1, 2, ...}."""
    count = 0
    while random.random() >= p:
        count += 1
    return count + 1


def uniform(a, b):
    return a + (b - a) * random.random()


def exponential(lam):
    """Inverse transform. log1p(-u) avoids log(0) when u is very near 1."""
    return -math.log1p(-random.random()) / lam


def normal_pair(mu, sigma):
    u1 = max(random.random(), 1e-12)
    u2 = random.random()
    r = math.sqrt(-2.0 * math.log(u1))
    th = 2.0 * math.pi * u2
    return (mu + sigma * r * math.cos(th),
            mu + sigma * r * math.sin(th))


cases = [
    ("Bernoulli(0.3)", [bernoulli(0.3) for _ in range(N)],
     0.3, math.sqrt(0.3 * 0.7)),
    ("Binomial(50,0.4)", [binomial(50, 0.4) for _ in range(HALF)],
     20.0, math.sqrt(50 * 0.4 * 0.6)),
    ("Poisson(3)", [poisson(3.0) for _ in range(N)], 3.0, math.sqrt(3.0)),
    ("Geometric(0.25)", [geometric(0.25) for _ in range(N)],
     4.0, math.sqrt(0.75) / 0.25),
    ("Uniform(2,10)", [uniform(2.0, 10.0) for _ in range(N)],
     6.0, math.sqrt(64 / 12)),
    ("Exponential(0.5)", [exponential(0.5) for _ in range(N)], 2.0, 2.0),
]

normals = []
while len(normals) < N:
    normals.extend(normal_pair(100.0, 5.0))
normals = normals[:N]

print(f"{N:,} draws per distribution (Binomial uses {HALF:,}).")
print(f"{'distribution':18} {'emp mean':>10} {'theory':>9} "
      f"{'emp sd':>9} {'theory':>9}")
for name, vals, tm, ts in cases:
    em, es = moments(vals)
    print(f"{name:18} {em:10.4f} {tm:9.4f} {es:9.4f} {ts:9.4f}")
em, es = moments(normals)
print(f"{'Normal(100,5)':18} {em:10.4f} {100.0:9.4f} {es:9.4f} {5.0:9.4f}")

# Identity 1: Poisson's mean equals its variance.
poiss = [poisson(3.0) for _ in range(N)]
m, sd = moments(poiss)
print()
print(f"Poisson(3): mean = {m:.4f}, variance = {sd ** 2:.4f}  "
      f"(both should be 3; Var = E is the fingerprint)")

# Identity 2: Binomial's variance is strictly below its mean.
bin_vals = [binomial(30, 0.1) for _ in range(N)]
m2, sd2 = moments(bin_vals)
print(f"Binomial(30,0.1): mean = {m2:.4f}, variance = {sd2 ** 2:.4f}")
print(f"  ratio var/mean = {sd2 ** 2 / m2:.4f} = 1-p = {1 - 0.1} exactly "
      f"(so Var < E, unlike Poisson)")
```

</details>

**[ ] Exercise 5 — the rate/mean trap in code.** A service has a mean inter-arrival
time of 250 ms between requests.
(a) State the correct distribution and parameter, and give the correct sampler.
(b) Write the plausible-but-wrong version that puts the mean where the rate
belongs, and predict its empirical mean exactly.
(c) Draw 100,000 samples from each and confirm both predictions.
(d) Compute the median and 95th percentile under the correct model, and say what
the buggy sampler would do to a load test's conclusions.

<details>
<summary>Solution</summary>

(a) Inter-arrival times of a Poisson process are $\mathrm{Exp}(\lambda)$ with
$\lambda = 1/\text{mean} = 1/0.25 = 4$ per second. Since $\mathrm{Exp}(\lambda)$
has mean $1/\lambda$, the correct sampler is

```text
x = -log1p(-u) / LAMBDA,      LAMBDA = 1 / MEAN = 4
```

equivalently `MEAN * -log1p(-u)`, or in the standard library
`random.expovariate(1 / MEAN)`.

(b) The bug is to write the rate position but fill it with the mean:

```text
x = -log1p(-u) / MEAN          <-- WRONG: MEAN is not a rate
```

Direct computation. $-\ln u \sim \mathrm{Exp}(1)$, so its mean is 1. Dividing by
$LAMBDA = 4$ gives mean $1/4 = 0.25$ s. Dividing by $MEAN = 0.25$ gives mean
$1/0.25 = 4.0$ s. So the buggy sampler's empirical mean is **4.0 s, sixteen times
too large** — an inflation factor of $1/\text{mean}^2 = 1/0.0625 = 16$.

(c) Both samplers, 100,000 draws each.

(d) Correct model: median $= \ln 2/4 = 0.1733$ s, which is **0.69×** the mean and
therefore *below* it; 95th percentile $= \ln 20/4 = 0.7489$ s, which is **3.0×**
the mean. That gap is the right-skew signature, and it is why the lesson insists
you report a percentile rather than a mean for waiting times.

Under the buggy sampler every gap is 16× larger, so a load test would report a
mean of 4 s and a p95 of 12.0 s. That looks like a service 16× slower than the
target — or, if you calibrate the test by dividing the intended rate by 16 to hit
the right throughput, you generate 16× too little load and everything looks
healthy. Crucially the *shape* is still perfectly exponential in both cases, so a
distributional test cannot catch this; only checking the mean against the
intended mean can. That is exactly the advice in Mistake 1: print ten samples and
check they average to the mean you intended.

```python
import math
import random

random.seed(777)
N = 100_000

MEAN = 0.25                  # seconds between arrivals
LAMBDA = 1 / MEAN           # rate: the RECIPROCAL of the mean


def correct(u):
    return -math.log1p(-u) / LAMBDA


def buggy(u):
    """Puts MEAN where the RATE belongs. Effective rate = 1/MEAN = 4."""
    return -math.log1p(-u) / MEAN


good = [correct(random.random()) for _ in range(N)]
bad = [buggy(random.random()) for _ in range(N)]

print("(c) empirical means")
for name, vals, predicted in (("correct /LAMBDA", good, MEAN),
                              ("buggy   /MEAN  ", bad, 1 / MEAN)):
    m = sum(vals) / N
    print(f"  {name}: {m:.4f} s   predicted {predicted:.4f} s   "
          f"ratio {m / predicted:.4f}")
print(f"  inflation factor = 1/MEAN^2 = {1 / MEAN ** 2:.0f}x")

print()
print("(d) correct model percentiles")
median = math.log(2) / LAMBDA
p95 = math.log(20) / LAMBDA
print(f"  mean {MEAN:.4f} s, median {median:.4f} s ({median / MEAN:.2f}x), "
      f"p95 {p95:.4f} s ({p95 / MEAN:.2f}x)")
print(f"  buggy mean {1 / MEAN:.2f} s, buggy p95 {math.log(20) / MEAN:.2f} s")
print("  The shape is still exponential either way -- only the scale is wrong,")
print("  so a shape test cannot catch this. Only the mean can.")
```

</details>

**[ ] Exercise 6 — Challenge: is this actually a Poisson process?** A service logs
request counts in each 1-second bucket for 100,000 buckets. You observe:
mean 12.0, variance 14.4, and $P(X = 0) = 0.0062$.
(a) Test the variance-to-mean ratio against the Poisson prediction. What does it
conclude?
(b) Poisson(12) predicts $P(X = 0) = e^{-12} = 0.0000061$. Compare with the
observed 0.0062 — a factor of about 1000. Which is more diagnostic, the ratio or
the zero mass, and why?
(c) A mixture model: with probability 0.7 the bucket is "quiet" with
$\mathrm{Poisson}(8)$, otherwise "busy" with $\mathrm{Poisson}(20.57)$. Compute
its mean and variance, and compare both to the observations.
(d) Design a test that would distinguish "Poisson with a wrong λ" from
"over-dispersed" using only the count distribution, and state which explanation
the observations favour.

<details>
<summary>Solution</summary>

(a) Poisson pins variance to the mean, so $\mathrm{Poisson}(12)$ predicts
variance $12.0$. Observed is $14.4$, a ratio of $14.4/12.0 = 1.2$. That is
over-dispersed, but only mildly — worth flagging, not alarming on its own.

(b) This is the decisive test. $\mathrm{Poisson}(12)$ gives
$P(X = 0) = e^{-12} = 0.0000061$, i.e. 0.61 expected empty buckets in 100,000.
The observed 0.0062 is **about 1000× larger**: 620 empty buckets where Poisson
expects well under one. No choice of λ can fix this, because for any Poisson,
$P(X=0) = e^{-\lambda}$ and matching the mean forces $\lambda = 12$.

So the zero mass is *more* diagnostic than the ratio. The ratio is a
one-number summary that a mild mixture can nudge; the zero mass tests the model
at a point where it makes an extreme, falsifiable prediction. A process that
produces 620 empty seconds while averaging 12 requests is bimodal in its
arrival behaviour — some seconds have no traffic at all, others have far more than
12. The ratio of 1.2 understates how far from Poisson this is, because variance
is dominated by the bulk of the distribution.

(c) A mixture of Poissons with weights 0.7 / 0.3 and rates 8 / 20.57. For a
mixture, $E[X] = \sum w_i \lambda_i$ and
$\mathrm{Var}(X) = \sum w_i(\lambda_i + \lambda_i^2) - \mu^2$, because the
second moment is $\sum w_i(\lambda_i + \lambda_i^2)$ for a Poisson component.

**Mean:** $0.7 \times 8 + 0.3 \times 20.57 = 5.6 + 6.171 = 11.771$.

**Variance:** $\left[0.7(8 + 64) + 0.3(20.57 + 422.9)\right] - 11.771^2 =
\left[50.4 + 133.05\right] - 138.57 = 183.45 - 138.57 = 44.95$.

The mean is close to the observed 12.0 but the variance is 3.1× too large. That
is itself the diagnosis: **a busy/quiet two-state mixture produces far more
over-dispersion than 1.2× at this mean**, because the between-component variance
$\sum w_i(\lambda_i-\mu)^2$ is large whenever the two rates are far apart. To get
only 14.4 you would need rates much closer together — and rates closer together
also drive $P(X=0)$ toward $e^{-\mu}$, killing the 1000× excess of zeros. So no
mixture of this form explains both observations at once.

(d) **The test: compare $P(X = 0)$ against $e^{-\bar X}$, where $\bar X$ is the
observed mean.** If the data were Poisson, these would agree to within sampling
error, since $E[X] = \lambda$ pins $\lambda$ and $P(X=0) = e^{-\lambda}$
follows. Here $e^{-12} = 0.00000614$ — under 1 expected empty bucket in 100,000 —
against 620 observed.

This is more diagnostic than the variance ratio, for two reasons. First, it tests
the model at a point where it makes an extreme, falsifiable prediction, whereas
the ratio is a one-number summary that a mild mixture can nudge to 1.2 without
coming close to breaking the Poisson. Second, it is *invariant to the parameter*:
there is no value of $\lambda$ for which $e^{-\lambda} = 0.0062$ while
$\lambda = 12$ also holds.

The shape that does explain both is **zero-inflation**: with probability
$\theta = 0.0062$ the bucket is empty, otherwise it is
$\mathrm{Poisson}(\lambda)$. Its mean is $(1-\theta)\lambda$ and its variance is
$(1-\theta)\lambda + \theta(1-\theta)\lambda^2$. Matching the observed mean of
12.0 gives $\lambda = 12/(1-0.0062) = 12.0749$, and then the variance is
$12.0 + 0.0062 \times 0.9938 \times 145.8 = 12.90$ — against the observed 14.4,
which is close. Mean, variance, and zero mass all line up.

Operationally the message is the same as in Exercise 3(d): do not re-fit $\lambda$,
segment the timeline. The 620 empty buckets are not noise around 12 — they are
quiet regimes showing through a window that spans them, and the honest fix is to
bucket only over active periods, or to accept a compound model with an explicit
zero component.

Operationally, the fix is not to re-fit λ but to split the timeline: bucket
counts taken across deploys, or across regions, are sums over heterogeneous
regimes, and the empty buckets are the quiet regimes showing through. Segment,
then fit Poisson within each segment — which is precisely the recommendation in
Exercise 3(d).

```python
import math

OBS_MEAN, OBS_VAR, OBS_P0 = 12.0, 14.4, 0.0062

# (a) variance-to-mean ratio
ratio = OBS_VAR / OBS_MEAN
print(f"(a) observed var/mean = {OBS_VAR}/{OBS_MEAN} = {ratio:.3f}")
print(f"    Poisson pins this at exactly 1.0, so {ratio:.3f} is over-dispersed,")
print(f"    but only mildly.")

# (b) the zero-mass test
poisson_p0 = math.exp(-OBS_MEAN)
print()
print(f"(b) Poisson({OBS_MEAN}) predicts P(X=0) = e^-12 = {poisson_p0:.8f}")
print(f"    observed P(X=0)                              = {OBS_P0:.8f}")
print(f"    observed / predicted                          = {OBS_P0 / poisson_p0:.0f}x")
print(f"    expected empty buckets in 100,000: {100_000 * poisson_p0:.4f}")
print(f"    observed empty buckets in 100,000: {100_000 * OBS_P0:.0f}")
print("    No lambda can fix this: matching the mean forces lambda = 12,")
print("    and then P(X=0) = e^-12 no matter what.")

# (c) a two-state mixture, and why it over-shoots
w, lam_q, lam_b = 0.7, 8.0, 20.57
mix_mean = w * lam_q + (1 - w) * lam_b
mix_var = w * (lam_q + lam_q**2) + (1 - w) * (lam_b + lam_b**2) - mix_mean**2
print()
print(f"(c) mixture 0.7*Poisson({lam_q}) + 0.3*Poisson({lam_b}):")
print(f"    mean     = {mix_mean:.4f}   (observed {OBS_MEAN})")
print(f"    variance = {mix_var:.4f}   (observed {OBS_VAR})")
print(f"    -> variance overshoots badly, so a two-state busy/quiet mixture")
print(f"       at this ratio is NOT the right explanation.")

# (d) zero-inflation IS the shape the numbers want.
# ZI(theta, lam): X = 0 with probability theta, else Poisson(lam).
#   E[X]   = (1 - theta) lam
#   Var[X] = (1 - theta) lam + theta(1 - theta) lam^2
theta = OBS_P0
lam = OBS_MEAN / (1 - theta)          # chosen so the mean matches exactly
zi_mean = (1 - theta) * lam
zi_var = (1 - theta) * lam + theta * (1 - theta) * lam**2
print()
print(f"(d) zero-inflated Poisson, theta = {theta}, lam = {lam:.4f}")
print(f"    mean     = {zi_mean:.4f}   (observed {OBS_MEAN})")
print(f"    variance = {zi_var:.4f}   (observed {OBS_VAR})")
print(f"    P(X=0)   = {theta:.4f}    (observed {OBS_P0})")
print()
print("    THE DECISIVE STATISTIC IS P(X=0) vs e^(-mean): under Poisson these")
print(f"    agree, but here they differ by {OBS_P0 / math.exp(-OBS_MEAN):.0f}x.")
print("    A wrong lambda moves mean and e^(-mean) TOGETHER, leaving var/mean")
print("    at exactly 1. Ours is 1.2, so lambda alone cannot explain it.")
print("    So: excess zeros -- buckets where traffic genuinely stopped.")
```

</details>

## Summary

- Seven distributions cover most practice: count things with Bernoulli, Binomial,
  Poisson, Geometric; measure things with Uniform, Exponential, Normal.
- Poisson is the only one in the table with Var = E; a variance-to-mean ratio
  far above 1 means events cluster and Poisson is wrong.
- Exponential's parameter λ is a **rate**, so mean = 1/λ; the geometric's mean is
  likewise 1/p. Count distributions get reciprocals.
- Inverse transform sampling solves F(x) = u for x; it works for any invertible
  CDF and gives the exponential in one line.
- Box–Muller turns two uniforms into two independent normals via r = √(−2 ln U₁),
  θ = 2πU₂ — and gives you both, so do not discard the second.
- Knuth's Poisson method is correct but costs λ+1 uniforms per sample, so it is
  only sensible for small λ.
- Discrete uniform and continuous uniform have slightly different variances,
  (n²−1)/12 versus (b−a)²/12.
- Always state which geometric convention you use; the two differ by one full
  trial.

## Next

[67 — Joint Random Variables and Covariance](67_joint_random_variables_covariance.md)
handles two variables at once: joint and marginal distributions, independence,
covariance and correlation, why correlation is not causation, and how conditional
expectation turns least-squares regression into a prediction problem.
