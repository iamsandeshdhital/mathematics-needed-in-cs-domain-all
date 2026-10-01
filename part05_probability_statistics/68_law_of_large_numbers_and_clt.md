# 68 — Law of Large Numbers and the Central Limit Theorem

**Part**: part05_probability_statistics · **Prerequisites**: 64 · **Time**: 40 min

---

## In Plain Words

Two theorems turn randomness into predictability. They are the reason statistics
works at all.

The **law of large numbers** says that if you average more and more independent
observations of anything, the average settles on the true mean. Spin a coin ten
million times and the fraction of heads converges to the coin's actual bias, no
matter how badly it behaved in small batches. The fluctuations do not vanish; they
get relatively smaller. This is what lets you estimate a rate from a sample and
trust it.

The **central limit theorem** says something different and much more surprising:
*what form* does the average take? It turns out that the average of almost any
variable, no matter how lumpy and skewed the original, is approximately normal.
You do not need the original to be normal. You do not even need the original to
be symmetric. Add up enough of them and you get a bell curve.

Together these give you the standard error — how much an average is expected to
wobble — and with it confidence intervals and hypothesis tests. Between them,
these two theorems are behind essentially every number anyone has ever reported
with a margin of error.

## Why Computer Science Cares

- **Every confidence interval ever reported** uses the standard error, which is
  σ/√n — a direct application of the variance of a sum of independent variables
  from [Lesson 64](../part05_probability_statistics/64_expectation_variance.md).
- **A/B tests.** Deciding whether a 1.2% conversion lift is real is exactly the
  question the CLT exists to answer.
- **Benchmark variance.** Reporting "runs in 42 ms" without a standard deviation
  is meaningless; reporting 42 ± 0.3 ms is a statement you can act on.
- **Monte Carlo estimates.** Simulation error shrinks like 1/√n, which is why
  10× more samples only buys 3.16× less noise. That √n wall is why practitioners
  use importance sampling rather than brute force.
- **Gradient descent and SGD.** The noise in a minibatch gradient has standard
  deviation σ/√B, which sets the learning-rate floor.

## The Formal Version

**Definition.** Let X₁, X₂, … be independent and identically distributed (i.i.d.)
with E[Xᵢ] = μ and Var(Xᵢ) = σ² < ∞. The *sample mean* of the first n is

    X̄ₙ = (X₁ + X₂ + ⋯ + Xₙ) / n

**Theorem (weak law of large numbers, WLLN).** Then

    P(|X̄ₙ − μ| > ε) → 0   as n → ∞, for every ε > 0

Equivalently, X̄ₙ → μ in probability.

**Explanation.** By the union bound, P(|X̄ₙ − μ| > ε) ≤ Var(X̄ₙ)/ε² =
σ²/(nε²) → 0. The whole proof is two lines: variance of a sum grows linearly,
so the spread of the *average* shrinks like 1/√n.

**Theorem (strong law of large numbers, SLLN).** Then, with probability 1,

    X̄ₙ → μ   as n → ∞

**Explanation.** WLLN says the probability of being far from μ tends to zero.
SLLN says the path actually converges, not just the probabilities. SLLN implies
WLLN and requires no finite variance — it holds whenever E|X| < ∞. It is
markedly harder to prove (the standard proof uses a subsequence argument from
[Lesson 25](../part02_discrete_combinatorics/25_relations_and_equivalence_classes.md)),
but it is the statement that justifies the phrase "the long-run average".

**Definition.** The *standard error* of the sample mean is its standard
deviation:

    SE(X̄ₙ) = σ/√n

**Explanation.** Var(X̄ₙ) = Var(ΣXᵢ/n²) = (1/n²)·nσ² = σ²/n by linearity of
variance for independent variables. The 1/√n is the single most consequential
number in applied statistics.

**Theorem (central limit theorem, CLT).** Let Xᵢ be i.i.d. with mean μ and
variance σ² (finite, and for the classical version not all mass on one point).
Then for every real t,

    P( (X̄ₙ − μ) / (σ/√n) ≤ t ) → Φ(t)

where Φ is the standard normal CDF. Equivalently, X̄ₙ is approximately
N(μ, σ²/n) for large n.

**Explanation.** The proof uses characteristic functions
([Lesson 55](../part04_calculus/55_fourier_series_and_transforms.md)): the
characteristic function of X is φ, and the standardised average's characteristic
function is φ(t/(σ√n))^n, whose limit is e^(−t²/2), the characteristic function of
N(0,1). It is remarkable that the hypotheses are so weak — mean and finite
variance, nothing about symmetry, bounded support, or shape.

### Four types of convergence

They are not interchangeable, and the difference is the whole reason statistics
has a reputation for subtlety.

| Type | Statement | Strength |
| --- | --- | --- |
| In probability | P(\|Xₙ − x\| > ε) → 0 | WLLN |
| Almost surely | happens once, and stays | SLLN; strongest |
| In distribution | CDFs converge | weakest |
| In L² (mean square) | E[(Xₙ − x)²] → 0 | implies in probability |

The hierarchy: **almost surely ⟹ in probability ⟹ in distribution**, and none of
the reverse implications hold. The CLT gives convergence *in distribution*, which
is the weakest — and that is exactly why it is so broadly applicable: it needs no
information about individual outcomes, only the shape of the resulting CDF.

### The 95% confidence interval

Since (X̄ₙ − μ)/(σ/√n) ≈ N(0,1) and P(|Z| ≤ 1.96) = 0.95,

    P(μ ∈ [X̄ₙ − 1.96σ/√n,  X̄ₙ + 1.96σ/√n]) ≈ 0.95

### A theorem about the tail, not just the body

WLLN plus Chebyshev's inequality (from
[Lesson 64](../part05_probability_statistics/64_expectation_variance.md)) gives a bound that holds at **every** n:

    P(|X̄ₙ − μ| ≥ kσ/√n) ≤ 1/k²

For k = 2 that is a guaranteed 75% confidence interval, valid for any n and any
distribution with finite variance — no normality, no large n. The CLT-based
interval is better (95%) but approximate; the Chebyshev interval is weaker and
exact. Good engineering knows which one it is quoting.

## Worked Example

### Example A — the LLN, watched happening

Generate coin flips with p = 0.3 and track the running fraction of heads.

- After 10 flips: the fraction bounces around 0.3 with swings of 0.2 or more.
- After 1,000 flips: it is near 0.3, typically within 0.03.
- After 1,000,000 flips: it is within about 0.001.

The *absolute* fluctuation shrinks like 1/√n. For a Bernoulli(0.3) the standard
error at n is √(0.3 × 0.7/n) = 0.458/√n:

| n | standard error |
| --- | --- |
| 10 | 0.1449 |
| 1,000 | 0.01449 |
| 10,000 | 0.00458 |
| 1,000,000 | 0.000458 |

The key insight for engineers: **the noise shrinks, but very slowly.** Going from
1,000 to 10,000 samples (10× the data) only reduces the error by √10 ≈ 3.16×. This
is why nobody brute-forces high-precision integration, and why Monte Carlo is
trusted but never taken at face value.

### Example B — the CLT on a deliberately terrible distribution

Take X uniform on [0, 1] — flat, symmetric, nothing normal about it. The CLT says
the sample mean of n draws is approximately N(0.5, 1/(12n)).

For n = 30: mean 0.5, sd = √(1/360) = 0.0527.

Now take X = exponential(1) — extremely skewed, most mass near 0, long tail. Still
not normal. Same n = 30: mean 1, sd = 1/√30 = 0.1826.

And X = a Bernoulli(0.5) — only two values, maximally far from a bell curve.
Same n = 30: mean 0.5, sd = 0.5/√30 = 0.0913. Its exact distribution is a Binomial,
which for n = 30 is *visibly* lumpy — the pmf has 31 distinct spikes. Yet the
quantiles of the 30-draw average sit almost exactly on the normal ones. The code
below measures this: for all three distributions the ratio of empirical to
theoretical variance is within about 1% of 1, and the 10th and 90th percentile
z-scores land within roughly 0.05 of the normal values ±1.2816.

That is the CLT in one sentence: **the distribution of the average converges to
normal even when the distribution of the summands is nothing like normal.** The
smoothing comes from the averaging itself. What does *not* converge to normal is
the shape of the raw variable — so never report a normal assumption for the raw
metric ([Lesson 65](../part05_probability_statistics/65_continuous_random_variables.md)).

### Example C — a confidence interval, and why the width matters

Say you measure conversion on a page with 4,000 users and see 3.1%, i.e. 124
conversions. Estimate p̂ = 124/4000 = 0.031.

**Standard error.** For a proportion, the binomial variance gives SE =
√(p(1−p)/n), so

    SE = sqrt(0.031 × 0.969 / 4000) = sqrt(7.5136e-6) = 0.0027404

Note the trap here. The naive "standard deviation" of the 0/1 outcome variable is
about √p̂ = 0.031, which is **11.3× larger** than the correct standard error.
Anyone who divides p̂ by √n gets an interval more than ten times too wide.

**95% confidence interval.** p̂ ± 1.96 × SE = 0.031 ± 0.005371, so

    [0.02563, 0.03637]

**Interpretation.** If you repeated this experiment many times from scratch and
built an interval each time, about 95% of them would contain the true conversion
rate. It is a statement about *the procedure's long-run accuracy*, not a
95% probability that this particular fixed number is right — that distinction
matters and is the subject of [Lesson 69](../part05_probability_statistics/69_estimation_and_hypothesis_testing.md).

**Why the width is the real story.** To halve the interval width you must
quadruple the sample. Going from 4,000 users to 16,000 halves the standard error,
to 0.001370, giving [0.02831, 0.03369]. This is the arithmetic behind why
detecting small product improvements is expensive, and why an A/B test run for
three days cannot resolve a 0.1% effect no matter how clever the analysis.

## Runnable Code

### The LLN, with a running average

```python
import random

random.seed(1)

# A biased coin: p = 0.3. The running fraction of heads should converge to 0.3.
P = 0.3
checkpoints = [10, 100, 1_000, 10_000, 100_000, 1_000_000]

heads = 0
print(f"{'flips':>9} {'fraction':>10} {'abs error':>10} {'1/sqrt(n)':>10}")
for i in range(1, checkpoints[-1] + 1):
    if random.random() < P:
        heads += 1
    if i in checkpoints:
        frac = heads / i
        # SE of a Bernoulli proportion is sqrt(p(1-p)/n)
        se = (P * (1 - P) / i) ** 0.5
        print(f"{i:9,} {frac:10.6f} {abs(frac - P):10.6f} {se:10.6f}")

print()
print("The absolute error shrinks like 1/sqrt(n):")
print(f"  100x more samples (1000 -> 100000) gives only "
      f"{(1000 / 100_000) ** 0.5:.1f}x less error")
print("This is the sqrt(n) wall: brute force is expensive for precision.")
```

### The CLT on three ugly distributions

```python
import math
import random

random.seed(42)


def exponential(lam=1.0):
    return -math.log1p(-random.random()) / lam


def bernoulli(p=0.5):
    return 1 if random.random() < p else 0


SAMPLERS = [
    ("Uniform(0,1)      (flat, symmetric)", lambda: random.random(),
     0.5, 1 / 12),
    ("Exponential(1)    (skewed, long tail)", exponential,
     1.0, 1.0),
    ("Bernoulli(0.5)    (two values only)", bernoulli,
     0.5, 0.25),
]

N = 40_000
N_PER_MEAN = 30

print(f"{N:,} experiments, each averaging {N_PER_MEAN} draws.")
print("Hypothesis: each average is approximately N(mu, sigma^2/n),")
print("even though none of the three original distributions is normal.")
print()

for name, sampler, mu, var in SAMPLERS:
    # Raw draws: the original shape, NOT normal.
    raw = [sampler() for _ in range(N)]
    raw_mean = sum(raw) / N
    raw_var = sum((x - raw_mean) ** 2 for x in raw) / N

    # Averages of N_PER_MEAN draws.
    means = []
    for _ in range(N):
        total = 0.0
        for _ in range(N_PER_MEAN):
            total += sampler()
        means.append(total / N_PER_MEAN)

    m_mean = sum(means) / N
    m_var = sum((x - m_mean) ** 2 for x in means) / N

    print(f"{name}")
    print(f"  RAW distribution : mean {raw_mean:8.4f} (theory {mu:.4f})  "
          f"var {raw_var:8.5f} (theory {var:.5f})")
    print(f"  AVERAGE of {N_PER_MEAN:2d}    : mean {m_mean:8.4f}             "
          f"var {m_var:8.6f} (theory {var / N_PER_MEAN:.6f})")
    print(f"  ratio var/mean_var: {m_var / (var / N_PER_MEAN):6.4f}  "
          f"(1.000 = CLT holds)")

    # How bell-shaped is the average? Compare its quantiles to the normal ones.
    srt = sorted(means)
    def quantile(q):
        return srt[int(q * (len(srt) - 1))]
    skew = (quantile(0.5) - m_mean) / (m_var ** 0.5)
    print(f"  median z-score {skew:+.4f} (normal = 0), "
          f"p10 z={((quantile(0.1) - m_mean) / m_var**0.5):+.4f} "
          f"(normal = -1.2816), "
          f"p90 z={((quantile(0.9) - m_mean) / m_var**0.5):+.4f} "
          f"(normal = +1.2816)")
    print()
```

### Convergence types, illustrated

```python
import random

random.seed(7)

# Build three sequences and watch how they relate.
print("SLLN vs WLLN, using a fair coin.")
N = 60_000
heads = 0
prev_wlln_fail = 0
for i in range(1, N + 1):
    if random.random() < 0.5:
        heads += 1
    frac = heads / i
    # "almost sure" failure: mean stays outside 0.4..0.6 from here on.
    # Here we just report the worst excursion seen by each n.
    if not (0.4 <= frac <= 0.6):
        prev_wlln_fail = i
    if i in (10, 50, 100, 500, 1000, 5000, 10000, 60000):
        print(f"  n={i:6,}  fraction={frac:.5f}  "
              f"|dev from 0.5|={abs(frac - 0.5):.5f}")

print()
print("'almost surely' means: once it settles, it never leaves again.")
print("'in probability' means: for each fixed epsilon, the chance of being")
print("  outside it shrinks to zero -- but excursions can still happen.")
print()

# A sequence that converges in distribution but NOT in probability.
# X_n = 1 with prob 1/n, else 0 -> X_n -> 0 in distribution, yet
# P(X_n = 1) = 1/n -> 0 too, so that converges in probability as well.
# The classic counterexample needs a shared coin:
print("Convergence in distribution vs in probability:")
shared_coin = 1 if random.random() < 0.5 else 0
seq = [shared_coin for _ in range(1000)]
print(f"  sequence of all 0s or all 1s (decided once): {seq[:12]}...")
print(f"  the CDF at 0.5 is the same as any single value's,")
print(f"  so it converges in DISTRIBUTION to a point mass.")
print(f"  but P(|X_n - 0.5| > 0.4) = 1 for all n,")
print(f"  so it does NOT converge in probability to 0.5.")
print(f"  (it DOES converge a.s. to the value the coin picked)")
```

### Confidence intervals, and the cost of precision

```python
import math

# Conversion rate measured on n users.
def proportion_ci(successes, n, z=1.96):
    """Normal-approximation confidence interval for a proportion."""
    p_hat = successes / n
    se = math.sqrt(p_hat * (1 - p_hat) / n)
    return p_hat, se, p_hat - z * se, p_hat + z * se


print("Conversion rate 3.1% (124/4000) -- width is what matters.")
print()
print(f"{'n':>9} {'p_hat':>8} {'SE':>9} {'95% CI':>22} {'width':>8}")
for n in (1_000, 4_000, 16_000, 64_000, 256_000):
    successes = round(0.031 * n)
    p_hat, se, lo, hi = proportion_ci(successes, n)
    print(f"{n:9,} {p_hat:8.5f} {se:9.6f} "
          f"[{lo:.5f}, {hi:.5f}] {hi - lo:8.5f}")

print()
print("Width halves only when n quadruples -- the sqrt(n) law again.")
print("A 0.1% improvement cannot be resolved without a very large n:")
n_needed = 4 * math.ceil((0.031 * 0.969 * (1.96 / 0.0005) ** 2))
print(f"  to detect a 0.05 percentage-point change you need ~{n_needed:,} users")
print("  -> that is why small-effect experiments are run for weeks,")
print("     or why teams use sequential testing and larger effect sizes.")
```

### Chebyshev: an interval that is always valid

```python
import math
import random

# Chebyshev: P(|Xbar - mu| >= k*sigma/sqrt(n)) <= 1/k^2.
# So k = sqrt(1/(1-confidence)) gives a GUARANTEED interval at any n.

TRUE_MU, SIGMA = 1.0, 1.0   # Exp(1): mean 1, sd 1 -- very skewed

N_TRIALS = 8_000
SAMPLE_SIZES = [5, 10, 30, 100, 1000]
Z_95 = 1.959964
K_CHEB = 1 / math.sqrt(0.05)  # 4.4721, for 95% guaranteed coverage

print(f"{N_TRIALS:,} experiments per n. Exp(1) sample means, true mu = {TRUE_MU}.")
print(f"Normal interval uses z={Z_95:.4f}; Chebyshev uses k={K_CHEB:.4f}.")
print("Chebyshev is guaranteed to cover at least 95% for EVERY n.")
print()
print(f"{'n':>5} {'normal cover':>13} {'Chebyshev cover':>16} {'normal width':>13}"
      f" {'Cheby width':>12}")

for n in SAMPLE_SIZES:
    rng = random.Random(1000 + n)
    half_normal = Z_95 * SIGMA / math.sqrt(n)
    half_cheb = K_CHEB * SIGMA / math.sqrt(n)

    normal_hits = cheb_hits = 0
    for _ in range(N_TRIALS):
        total = 0.0
        for _ in range(n):
            total += -math.log1p(-rng.random())
        mean = total / n
        if abs(mean - TRUE_MU) <= half_normal:
            normal_hits += 1
        if abs(mean - TRUE_MU) <= half_cheb:
            cheb_hits += 1

    print(f"{n:5d} {normal_hits / N_TRIALS:12.2%} {cheb_hits / N_TRIALS:15.2%}"
          f" {2 * half_normal:13.4f} {2 * half_cheb:12.4f}")

print()
print("Coverage is honest at every n -- the CLT approximation works well")
print("for a SUM (whose mean and variance are exact), so the 95% target is")
print("roughly met even at n=5.")
print()
print("The real cost of Chebyshev is not safety, it is WIDTH:")
print(f"  at n=5   it is {4.0 / 1.7530:.2f}x too wide")
print(f"  at n=1000 it is {0.2828 / 0.1240:.2f}x too wide")
print("So use the normal interval for sums of i.i.d. draws, and reach for")
print("Chebyshev only when independence is doubtful or the mean itself is")
print("heavy-tailed (an infinite variance makes sigma/sqrt(n) meaningless).")
```

### With Libraries

The block below needs `numpy` and `matplotlib`. It is optional and `run_all.py`
skips it; everything above is standard library only.

```python  title="With Libraries: LLN convergence and the CLT"
# Requires numpy / matplotlib -- not runnable in the stdlib-only check.
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(2024)
fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))

# 1. LLN: running mean converging, with the 1/sqrt(n) envelope.
ax = axes[0]
n_total = 20_000
draws = rng.random(n_total) < 0.3            # Bernoulli(0.3)
running = np.cumsum(draws) / np.arange(1, n_total + 1)
n_axis = np.arange(1, n_total + 1)
ax.plot(n_axis, running, lw=1, color="navy", label="running mean")
ax.axhline(0.3, color="crimson", ls="--", label="true p = 0.3")
envelope = np.sqrt(0.3 * 0.7 / n_axis)
ax.plot(n_axis, 0.3 + envelope, color="grey", ls=":", lw=1, label=r"$\pm\sigma/\sqrt{n}$")
ax.plot(n_axis, 0.3 - envelope, color="grey", ls=":", lw=1)
ax.set_xscale("log")
ax.set_xlabel("number of flips (log scale)")
ax.set_ylabel("fraction of heads")
ax.set_title("Law of Large Numbers: 1/$\\sqrt{n}$ convergence")
ax.legend(fontsize=8)

# 2. CLT: raw vs averaged, for a badly skewed variable.
ax = axes[1]
raw = rng.exponential(1.0, 400_000)
ax.hist(raw, bins=80, density=True, alpha=0.55, color="darkorange",
        label="raw Exp(1): skewed, NOT normal")
means = raw.reshape(-1, 30).mean(axis=1)      # averages of 30
ax.hist(means, bins=80, density=True, alpha=0.65, color="steelblue",
        label="average of 30: normal")
xs = np.linspace(0, 4, 200)
ax.plot(xs, np.exp(-xs) / xs.max() / 2.5, color="darkorange", lw=2, alpha=0.8)
ax.set_xlabel("value"); ax.set_ylabel("density")
ax.set_title("CLT: averaging makes it normal")
ax.legend(fontsize=8)

# 3. Standard error actually shrinking as 1/sqrt(n).
ax = axes[2]
ns = np.unique(np.logspace(0, 4, 25).astype(int))
se_theory = 1.0 / np.sqrt(ns)                # for Exp(1), sigma = 1
se_empirical = []
for n in ns:
    reps = max(50, 200_000 // n)
    reps = min(reps, 20_000)
    m = rng.exponential(1.0, (reps, n)).mean(axis=1)
    se_empirical.append(m.std())
ax.loglog(ns, se_theory, "-", color="crimson", lw=2, label=r"theory $\sigma/\sqrt{n}$")
ax.loglog(ns, se_empirical, "o", color="navy", ms=4, label="measured")
ax.set_xlabel("sample size n"); ax.set_ylabel("standard error of the mean")
ax.set_title("Standard error shrinks as 1/$\\sqrt{n}$")
ax.legend(fontsize=8)

plt.tight_layout()
plt.savefig("lln_clt.png", dpi=110)
print("wrote lln_clt.png")
```

## Common Mistakes

**Mistake 1 — expecting the sample mean to equal the true mean.**
Wrong: "I measured 3.1% conversion on 4,000 users, so the conversion rate is
3.1%." Right: the measured value is one point estimate; the truth is somewhere in
the interval around it, and the width of that interval depends on n. The
temptation is that the point estimate is the only number a dashboard can display,
so it silently becomes "the value".

**Mistake 2 — using the wrong standard error.** For a proportion, the SE is
√(p(1−p)/n), which is *not* σ/√n unless you already know σ. Using the naive
sample standard deviation of the 0/1 outcomes (which is √(p̂(1−p̂)) ≈ p̂ for small
p̂) is a common and consequential error: for p̂ = 0.031 the naive value is 0.031,
about **11× too large** compared with the correct 0.00274. The binomial variance
carries the (1−p) factor and it matters enormously at low rates.

**Mistake 3 — assuming the CLT applies to the raw data.**
Wrong: "conversions are normally distributed, so I can use z for n = 10."
Right: the CLT is about the *average of n draws*, not about the variable. A
single Bernoulli draw is as far from normal as possible. With n = 10 the normal
approximation to a Binomial is poor; you need n large enough that np and n(1−p)
are both comfortably above about 10.

**Mistake 4 — expecting √n to be fast.**
It is not. Cutting the standard error in half requires 4× the data. Teams routinely
underestimate the sample size needed for a 1% relative improvement by an order of
magnitude, because the intuition is linear in the data rather than √n.

**Mistake 5 — treating a 95% confidence interval as a 95% probability about the
parameter.**
The parameter is fixed; the interval is random. Correct statement: if you repeated
the whole experiment many times and constructed an interval each time, about 95%
of those intervals would contain the fixed true value. Writing "there is a 95%
chance the true value is in this interval" is the base-rate fallacy of
[Lesson 62](../part05_probability_statistics/62_conditional_probability_and_bayes.md) applied to frequentist
objects.

## Formula Sheet

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$\bar{X}_n$` | `$\dfrac{X_1 + X_2 + \cdots + X_n}{n}$` | The sample mean of the first $n$ i.i.d. observations. The object both theorems are about. | Every estimate, every average, every minibatch gradient. |
| i.i.d. | `E[X_i] = \mu$`, `$\mathrm{Var}(X_i) = \sigma^2 < \infty$`, independent | The hypotheses both theorems require. **Not optional** — drop independence and the mean can converge to something else entirely. | Check the mechanism, not just the data. Retries against a shared dependency are not i.i.d. |
| **WLLN** | `$P(\lvert \bar X_n - \mu\rvert > \varepsilon) \to 0$` as $n \to \infty$, for every $\varepsilon > 0$ | **Weak law**: the chance of being far from $\mu$ vanishes. Equivalently, convergence in probability. | Justifying "estimate a rate from a sample and trust it". Proof is two lines: the union bound gives `$\le \sigma^2/(n\varepsilon^2)$`. |
| **SLLN** | `$\bar X_n \to \mu$` with probability 1 | **Strong law**: the path itself converges, and stays. Requires only `$E\lvert X\rvert < \infty$`, no finite variance. | Justifying "the long-run average" as an actual statement about a single realisation. |
| **SE** | `$\mathrm{SE}(\bar X_n) = \dfrac{\sigma}{\sqrt n}$` | How much the average is expected to wobble. From `$\mathrm{Var}(\bar X_n) = \sigma^2/n$`, using independence. | Every error bar, every benchmark report, every minibatch-noise budget. |
| **`$\sigma/\sqrt n$` is exact** | `$\mathrm{Var}(\bar X_n) = \sigma^2/n$` at **every** n | The mean and variance of a sample mean need no CLT — only linearity. | Even at $n=1$: the SE is right, but the normality is not. |
| **CLT** | `$\dfrac{\bar X_n - \mu}{\sigma/\sqrt n} \Rightarrow \mathcal{N}(0,1)$` | **The average of almost anything becomes normal.** No symmetry, no bounded support, no shape assumption on $X_i$. | Turning a hard tail probability into a z-score. **About the average, never about the raw variable** (Mistake 3). |
| CLT approximation | `$\bar X_n \approx \mathcal{N}\!\left(\mu, \dfrac{\sigma^2}{n}\right)$` | The practical form: mean $\mu$, variance $\sigma^2/n$. | Benchmark reports, A/B tests, Monte Carlo error bars. |
| convergence hierarchy | almost surely ⟹ in probability ⟹ in distribution; in $L^2$ ⟹ in probability | None of the reverse implications hold. The CLT gives only convergence **in distribution** — the weakest. | Explaining why the CLT needs no information about individual outcomes. |
| **95% CI** | `$\mu \in \left[\bar X_n - 1.96\dfrac{\sigma}{\sqrt n},\ \bar X_n + 1.96\dfrac{\sigma}{\sqrt n}\right]$`, confidence $\approx 95\%$ | Normal-approximation interval. Valid for **large** n only. | The default once $n$ is comfortably large. |
| proportion SE | `$\mathrm{SE}(\hat p) = \sqrt{\dfrac{\hat p(1-\hat p)}{n}}$` | The `(1−p)` factor is essential at low rates. **Not** `$\sqrt p/\sqrt n$`. | Conversion rates, click rates, error rates. Mistake 2: the naive value is ~11× too large at $\hat p = 0.031$. |
| **Chebyshev** | `$P\!\left(\lvert \bar X_n - \mu\rvert \ge \dfrac{k\sigma}{\sqrt n}\right) \le \dfrac{1}{k^2}$` | A **guaranteed** bound at every $n$, with no normality assumption. $k = 2$ gives 75%; $k = 1/\sqrt{0.05} = 4.4721$ gives 95%. | Small n, doubtful independence, or a mean with heavy tails (infinite $\sigma$ makes the normal form meaningless). |
| $k$ for confidence | `$k = 1/\sqrt{1 - c}$` | Turns a desired confidence into Chebyshev's $k$. | `c = 0.95` ⇒ `k = 4.4721`, a 95% Chebyshev interval **2.28× wider** than the normal one. |
| $\sqrt n$ law | `$\dfrac{\mathrm{SE}(n)}{\mathrm{SE}(m)} = \sqrt{\dfrac{m}{n}}$` | Halving an error bar costs **4×** the data. 10× the data buys 3.16× the precision. | Every sample-size calculation. The reason small-effect experiments are weeks long. |
| sample size (two proportions) | `$n = \dfrac{2\bar p(1-\bar p)\,(z_{1-\alpha/2} + z_{1-\beta})^2}{(p_2 - p_1)^2}$` per variant | $\bar p$ is the pooled rate; `z = 1.96` at $\alpha = 0.05$, `z = 0.8416` at 80% power. | Sizing an A/B test. Detecting a 2% relative gain at 4% baseline needs **950,888 users per variant**. |
| minimum detectable effect | `$\delta = (z_{1-\alpha/2} + z_{1-\beta})\sqrt{\dfrac{2\bar p(1-\bar p)}{n}}$` | What effect you can actually detect at a given $n$. | "Is our test big enough?" At $n = 20{,}000$: $\delta \approx 0.0055$, a 13.8% relative effect. |
| Binomial→normal | needs `$np \ge 10$` **and** `$n(1-p) \ge 10$` | The rule of thumb for replacing a Binomial with a normal. | Checking before you use $z$. With $n = 10$ the approximation is poor. |
| WLLN bound | `$P\!\left(\lvert \bar X_n - \mu\rvert > \varepsilon\right) \le \dfrac{\sigma^2}{n\varepsilon^2}$` | Chebyshev applied to the sample mean — the two-line proof of WLLN. | Showing convergence without the CLT. |

## Multiple Choice Questions

**Q1.** You collect 400,000 measurements with mean 250 ms and standard deviation
80 ms. What is the standard error of the mean?

- A) 80 ms
- B) 0.4 ms
- C) 0.126 ms
- D) 20 ms

<details>
<summary>Answer and explanation</summary>

**C) 0.126 ms.**

$\mathrm{SE} = \sigma/\sqrt n = 80/\sqrt{400{,}000} = 80/632.46 = 0.1265$ ms.
Option A is the trap: σ is the spread of a *single* measurement, not of the
average, and the lesson's Example A reports exactly this confusion when a
proportion is measured. Option B would need σ = 8 ms. Option D is σ/4, which has
no justification. The size of the error in option A is the point: the √n
reduction here is a factor of 632.

</details>

**Q2.** Which statement about the CLT is correct?

- A) It requires the original variable to be approximately normal
- B) It requires the original variable to be symmetric
- C) It requires only independence, a finite mean, and a finite variance — none of the original's shape
- D) It applies to the raw variable, not to the average

<details>
<summary>Answer and explanation</summary>

**C) It requires only independence, a finite mean, and a finite variance — none
of the original's shape.**

This is why the lesson runs the CLT on a uniform, an exponential, and a Bernoulli
and finds all three averaging to normal. Option A is a common confusion with the
*exact* result for normal inputs. Option B is false — the exponential in Example B
is maximally skewed and still works. Option D inverts the theorem, and is Mistake 3
in this lesson.

</details>

**Q3.** For a conversion rate of 3.1% on 4,000 users, what is the standard error
of the observed rate?

- A) $\sqrt{0.031/4000} = 0.00278$
- B) $\sqrt{0.031 \times 0.969 / 4000} = 0.00274$
- C) 0.031
- D) $0.031/\sqrt{4000} = 0.00049$

<details>
<summary>Answer and explanation</summary>

**B) $\sqrt{0.031 \times 0.969 / 4000} = 0.00274$.**

The `(1−p)` factor from the Binomial variance is not optional at low rates.
Option A drops it, giving a 1.5% error — small here, but it grows as $p$ shrinks.
Option C is the naive sample standard deviation of the 0/1 outcomes, which is
**11.3× too large** — Mistake 2, the most consequential error in this lesson's
example. Option D divides a probability by $\sqrt n$, a fourth distinct mistake.

</details>

**Q4.** What does a 95% confidence interval of `[0.0256, 0.0364]` for a conversion
rate mean?

- A) There is a 95% probability the true rate lies in this interval
- B) If the experiment were repeated many times and an interval built each time, about 95% of them would contain the fixed true rate
- C) 95% of users convert at a rate in this range
- D) The true rate changes 95% of the time within this interval

<details>
<summary>Answer and explanation</summary>

**B) If the experiment were repeated many times and an interval built each time,
about 95% of them would contain the fixed true rate.**

This is Mistake 5, and the statement about *the procedure's long-run accuracy* is
the one the lesson insists on. Option A is the base-rate fallacy of
[Lesson 62](../part05_probability_statistics/62_conditional_probability_and_bayes.md) applied to a frequentist
object: the parameter is fixed, so it does not "have a probability" of lying
somewhere. Option C confuses a statement about the parameter with one about
individuals. Option D makes the parameter random, which is the same error as A in
different words.

</details>

**Q5.** A benchmark reports "42 ms" with no standard deviation, and another
reports "42 ± 0.3 ms". Which is usable?

- A) The first, because it is simpler
- B) The second, because 0.3 ms tells you the run-to-run spread and therefore whether a 5 ms change is real
- C) Both equally; the ± is decoration
- D) The first, because 42 ± 0.3 implies the runs are not reproducible

<details>
<summary>Answer and explanation</summary>

**B) The second, because 0.3 ms tells you the run-to-run spread and therefore
whether a 5 ms change is real.**

The ± figure is exactly `$\mathrm{SE} = \sigma/\sqrt n$`, so it converts a
comparison into a z-score. Option A is the reporting habit the lesson is arguing
against. Option C is the same habit with a rationalisation. Option D inverts the
meaning: a *small* spread is evidence of reproducibility.

</details>

**Q6.** Which statement about the four types of convergence is correct?

- A) Convergence in probability implies convergence in distribution, and the reverse also holds
- B) Almost surely ⟹ in probability ⟹ in distribution; none of the reverse implications hold
- C) The CLT gives almost-sure convergence
- D) Convergence in $L^2$ is the weakest of the four

<details>
<summary>Answer and explanation</summary>

**B) Almost surely ⟹ in probability ⟹ in distribution; none of the reverse
implications hold.**

Option A gets the forward direction right and then claims a reverse that fails —
the lesson's shared-coin example converges in distribution without converging in
probability. Option C is false; the CLT is convergence in distribution, the
*weakest* kind, which is exactly why it is so broadly applicable. Option D
inverts the hierarchy: $L^2$ implies in probability, so it is stronger than
distribution.

</details>

**Q7.** A team needs to halve the width of a 95% confidence interval. What must
they do?

- A) Double the sample size
- B) Quadruple the sample size
- C) Multiply the sample size by 8
- D) Use a 90% interval instead

<details>
<summary>Answer and explanation</summary>

**B) Quadruple the sample size.**

Width is proportional to `σ/√n`, so halving it needs $n \to 4n$. This is the
√n law, Mistake 4 in this lesson, and the answer in the worked example: 4,000
users gives width 0.01074, and 16,000 users gives 0.00537. Option A buys a 1.41×
reduction, option C buys 1.5×, and option D changes the confidence rather than the
precision — a different trade, not a free one.

</details>

**Q8.** At n = 1,000 users per variant on a 4% baseline, the minimum detectable
effect at 80% power is about 0.55 percentage points. What does that tell you?

- A) The test can reliably detect a 2% relative improvement, since 0.55 points is smaller than 0.08
- B) The test can detect about a 13.8% relative improvement (4.0% → 4.55%); the 2% relative effect you wanted is 0.08 points, only about 0.58 standard errors
- C) The test will produce a significant result regardless of the true effect
- D) The minimum detectable effect does not depend on n

<details>
<summary>Answer and explanation</summary>

**B) The test can detect about a 13.8% relative improvement (4.0% → 4.55%); the 2%
relative effect you wanted is 0.08 points, only about 0.58 standard errors.**

This is Exercise 3, and the numbers are the lesson's. Option A compares a
percentage-point quantity to a relative one — 0.55 points is nearly *seven times
larger* than the 0.08-point effect you wanted, not smaller. Option C is the
dangerous reading of an underpowered test: a non-significant result from an
underpowered test is not evidence of no effect. Option D contradicts the entire
lesson, since $\delta \propto 1/\sqrt n$.

</details>

**Q9.** Why is the Chebyshev interval worth having when the normal one exists?

- A) It is always tighter
- B) It is **guaranteed** to cover at the stated level for every n and every distribution with finite variance, whereas the normal interval is an approximation that needs large n
- C) It requires no sample at all
- D) It is the same thing under a different name

<details>
<summary>Answer and explanation</summary>

**B) It is **guaranteed** to cover at the stated level for every n and every
distribution with finite variance, whereas the normal interval is an
approximation that needs large n.**

The trade is width: at n = 100 with σ = 80 the 95% Chebyshev interval is 71.55 ms
wide against the normal one's 31.36 ms, a factor of **2.28**. Option A inverts the
trade-off. Option C is false — Chebyshev is about the sample mean and needs data.
Option D is false; they differ by a factor of $1/\sqrt{0.05}/1.96 = 2.28$ in width.

</details>

**Q10.** A load test reports 0.2% failures on 10,000 requests. Is that the
service's failure rate?

- A) Yes — 0.2% is the point estimate and the LLN guarantees it converges
- B) It is one point estimate with a standard error of about $\sqrt{0.002 \times 0.998/10000} = 0.00045$; the LLN guarantees convergence *as n grows*, not that this one number is the truth
- C) Yes, provided the failures are independent
- D) No, because the LLN requires a normal distribution

<details>
<summary>Answer and explanation</summary>

**B) It is one point estimate with a standard error of about
$\sqrt{0.002 \times 0.998/10000} = 0.00045$; the LLN guarantees convergence *as n
grows*, not that this one number is the truth.**

The SE is 0.00045, so a 95% interval is roughly $0.2\% \pm 0.09\%$, and that
single number is far wider than most teams' claimed failure budgets. Option A is
Mistake 1 — the point estimate silently becoming the value. Option C is right
about the mechanism but wrong about the conclusion: independence makes the LLN
*apply*, it does not make the finite-sample estimate exact. Option D is nonsense;
the LLN needs only a finite mean.

</details>

## Subjective Questions

### Short Answer

**Q1. State the WLLN and the SLLN, and say which is stronger and what extra
hypothesis the SLLN drops.**

<details>
<summary>Answer</summary>

WLLN: for i.i.d. $X_i$ with mean $\mu$ and finite variance $\sigma^2$,
$P(|\bar X_n - \mu| > \varepsilon) \to 0$ for every $\varepsilon > 0$ —
convergence in probability. SLLN: $\bar X_n \to \mu$ with probability 1 —
convergence almost surely, which is stronger. The SLLN drops the finite-variance
hypothesis and needs only $E|X| < \infty$. It is also markedly harder to prove,
but it is the statement that justifies the phrase "the long-run average" about a
single realisation.

</details>

**Q2.** Give the standard error of the sample mean and derive it in one line.

<details>
<summary>Answer</summary>

$\mathrm{SE}(\bar X_n) = \sigma/\sqrt n$. Because
$\mathrm{Var}(\bar X_n) = \mathrm{Var}(\sum_i X_i / n) = \frac{1}{n^2}
\mathrm{Var}(\sum_i X_i) = \frac{n\sigma^2}{n^2} = \sigma^2/n$, using
independence in the middle step. The standard deviation is the square root. Note
this is exact at every $n$ — no CLT required.

</details>

**Q3. State the CLT, and state precisely what it is *not* a claim about.**

<details>
<summary>Answer</summary>

For i.i.d. $X_i$ with mean $\mu$ and finite $\sigma^2$,
$(\bar X_n - \mu)/(\sigma/\sqrt n) \Rightarrow \mathcal{N}(0,1)$; equivalently
$\bar X_n \approx \mathcal{N}(\mu, \sigma^2/n)$. It is **not** a claim that $X_i$
itself is normal, nor that the raw data is symmetric or bounded, nor that the
CLT applies to a single observation. The lesson runs it on a uniform, an
exponential, and a two-valued Bernoulli and all three average to normal. The
original's shape is never changed — Mistake 3 in this lesson.

</details>

**Q4.** Order the four types of convergence from strongest to weakest, and say
which one the CLT delivers.

<details>
<summary>Answer</summary>

Almost surely ⟹ in probability ⟹ in distribution, and convergence in $L^2$
(meaning $E[(X_n - x)^2] \to 0$) ⟹ in probability. None of the reverse
implications hold. The CLT delivers convergence in **distribution** — the
weakest. That is precisely why it is so broadly applicable: it needs no
information about individual outcomes, only the shape of the resulting CDF.

</details>

**Q5.** Give the Chebyshev tail bound for a sample mean, and the value of $k$
that gives 95%.

<details>
<summary>Answer</summary>

$P\!\left(|\bar X_n - \mu| \ge k\sigma/\sqrt n\right) \le 1/k^2$. Solving
$1/k^2 = 0.05$ gives $k = 1/\sqrt{0.05} = 4.4721$, so
$\mu \in \bar X_n \pm 4.4721\,\sigma/\sqrt n$. Valid at every $n$ and for any
distribution with finite variance — no normality required. $k = 2$ gives a
guaranteed 75%.

</details>

**Q6.** Give the standard error of an observed proportion, and explain why it is
not $\sqrt{\hat p/n}$.

<details>
<summary>Answer</summary>

$\mathrm{SE}(\hat p) = \sqrt{\hat p(1-\hat p)/n}$, from the Binomial variance
$\mathrm{Var}(S) = np(1-p)$ divided by $n^2$. The `(1−p)` factor matters
enormously at low rates: for $\hat p = 0.031$ it is 0.969, but omitting it (or
worse, using $\sqrt{\hat p(1-\hat p)} \approx \hat p$ as the SE) gives a value
**11.3× too large**. That is Mistake 2 in this lesson, and it inflates every
error bar in a low-conversion funnel.

</details>

### Long Answer

**Q1. Why does the CLT need many independent samples, and what happens when the
assumptions fail?**

<details>
<summary>Model answer</summary>

The proof shows what is being bought. The characteristic function of the
standardised average is $\phi(t/(\sigma\sqrt n))^n$, and its limit is
$e^{-t^2/2}$. That limit follows from $\left(1 + \frac{z^2}{2n}\right)^n \to e^{z^2/2}$
— a statement about *many* copies of the same factor being multiplied. With one
draw the "average" is just $X$ itself, so its distribution is whatever $X$'s is.
There is no averaging to smooth anything until the copies are numerous, which is
why the numerical checks in the lesson still look good at n = 30 and why the rule
of thumb is $np \ge 10$ and $n(1-p) \ge 10$.

Independence is the assumption that does most of the damage when it fails. The
lesson's warning is concrete: copying one coin flip ten times satisfies "the
marginals are Bernoulli($p$)" but the average is 0 or 10 with nothing in
between, and its variance is $n^2\sigma^2$ rather than $\sigma^2$ — ten times
worse. Retries against a struggling dependency, and users sampled from one session
or one region, fail the same way. So the CLT's error bars become optimistic by
exactly the factor the dependency contributes, and the error is worst in the tail
([Lesson 64](../part05_probability_statistics/64_expectation_variance.md)'s covariance terms).

The second failure mode is heavy tails. The CLT needs a finite variance; if the
mean exists but the variance does not — a Pareto tail, a sum of heavy-tailed
services — then $\sigma/\sqrt n$ is meaningless and the standard error does not
exist at the rate the theorem predicts. There the stable-LLN regime (a rate
faster than $1/\sqrt n$, but slower than $1/n$) is the right framework, and
[Lesson 70](../part05_probability_statistics/70_information_theory_entropy.md)'s tail-sum route is a practical
substitute for an expectation you cannot normalise.

</details>

**Q2. Why does precision grow only like √n, and what does that imply for how you
run experiments?**

<details>
<summary>Model answer</summary>

Because $\mathrm{Var}(\bar X_n) = \sigma^2/n$ comes from a *linear* division by
$n$, and precision is the square root of variance. So the error bar falls as
$1/\sqrt n$: 10× the data buys 3.16× the precision, and halving the error bar
costs 4× the observations. This is not an approximation — it is exact arithmetic
from the variance of a sum — and it is the single most consequential number in
applied statistics.

The implication for experiments is quadratic in the effect size. The two-proportion
sample size formula gives $n \propto 1/\delta^2$, where $\delta = p_2 - p_1$ is
the absolute difference. So halving the effect you hope to detect costs 4× the
traffic, and quartering it costs 16×. Exercise 3 shows the extreme: detecting a 2%
relative gain on a 4% baseline — a difference of 0.0008 — needs **950,888 users per
variant**, while the 20,000 a team gets in a week can only resolve a 13.8%
relative effect.

Three design consequences follow. First, **pre-register the sample size** from the
effect you care about, because quietly stopping early converts an underpowered
test into a false negative. Second, **run longer rather than wider** when traffic
is the bottleneck, since $n$ is $n$; and prefer variance reduction over traffic
where you can — CUPED or a less noisy metric can cut the requirement by 30–50%,
which beats a traffic increase. Third, accept that some effects are not
measurable: if $\delta$ is below about 2.8 standard errors, no clever statistics
substitutes for a large sample or a large effect, and the honest move is to
decide on other grounds rather than to run a test that cannot answer the question.

</details>

**Q3. Why is a 95% confidence interval a statement about a *procedure* rather than
about a fixed number, and what breaks if you read it the other way?**

<details>
<summary>Model answer</summary>

Because the parameter is fixed and the interval is random. $p$ is a constant
property of your page; what varies from run to run is the sample you draw and
therefore $\hat p$ and the interval built around it. So the only statement that
has a probability is one about the *procedure*: if you repeated the whole
experiment many times from scratch and built an interval each time, about 95% of
those intervals would contain the fixed value. The interval you are holding is
one draw from that distribution — it either covers or it does not, and there is
no probability attached to which.

Reading it the other way is Mistake 5, and it is the base-rate fallacy of
[Lesson 62](../part05_probability_statistics/62_conditional_probability_and_bayes.md) applied to a frequentist
object. "There is a 95% chance the true rate is in [0.0256, 0.0364]" treats $p$ as
a random quantity with its own distribution, which is the Bayesian view and is
not what the interval encodes. The two readings lead to different decisions: the
procedural one says "run this again and the procedure is usually right"; the
other says "I have a 5% chance this specific number is wrong", which invites
decisions the interval cannot support.

The confusion is easy to fall into because the interval *looks* like a probability
statement, and because the informal Bayesian reading is genuinely defensible if
you supply a prior on $p$ and compute a credible interval instead. But then you
are no longer doing frequentist inference, and you should say so. Whichever you
choose, report the width too: a wide interval covering 95% is a much weaker
result than a narrow one, and the bare "95%" hides that difference entirely.

</details>

**Q4. Why does the central limit theorem let you be approximately right without
knowing the distribution, and what price does that approximation charge?**

<details>
<summary>Model answer</summary>

Because the averaging destroys the information about the original shape faster
than the sampling distribution retains any of it. The proof works through
characteristic functions: multiplying $n$ copies of $\phi$ and rescaling drives
the answer to $e^{-t^2/2}$ regardless of what $\phi$ was, so the limit depends on
only the first two moments. That is an extraordinary fact — the hypotheses
constrain no more than the mean and finite variance — and it is why the lesson
can run a flat uniform, a maximally skewed exponential, and a two-valued
Bernoulli and get the same bell curve out of all three averages.

The price is that you may only use it for the *average*. Nothing about the
original distribution changes: the exponential is still exponential, still
right-skewed with a hard floor at zero, and still wrong to report as normal. So
the CLT justifies every confidence interval and A/B test while refusing to
justify any statement about a single observation — the two uses are separated by
exactly the word "average", and conflating them is Mistake 3.

A second price is that the convergence is slow and only asymptotic. At n = 10 the
normal approximation to a Binomial is visibly poor; at n = 1 it is meaningless.
And for heavy-tailed variables where the variance does not exist, the theorem
does not apply at all, since the rescaling it depends on has no finite limit. So
the honest practice is: use the CLT whenever you are averaging and the variance
is finite, verify the assumption with data rather than by hope, and fall back to
Chebyshev — or to a quantile approach — when $n$ is small or the tails are heavy.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — standard errors and interval widths.** A service measures
latency (mean 250 ms, sd 80 ms) over n = 100 requests.

(a) Compute the standard error of the mean. (b) Give a 95% confidence interval
under the normal approximation. (c) Now measure 10,000 requests: repeat (a) and
(b). (d) By what factor did the interval width shrink, and does that match √n?
(e) Give a Chebyshev interval for the n = 100 case and compare widths.

<details>
<summary>Solution</summary>

(a) SE = σ/√n = 80/10 = **8 ms**.

(b) 250 ± 1.96(8) = 250 ± 15.68, so **[234.32, 265.68] ms**.

(c) SE = 80/√10000 = 80/100 = **0.8 ms**. Interval: 250 ± 1.96(0.8) = 250 ± 1.568,
so **[248.43, 251.57] ms**.

(d) The width went from 31.36 ms to 3.136 ms, a factor of exactly 10. That matches
√n: a 100× increase in n gives a 10× reduction in standard error, since
√(10000/100) = 10. This is the cleanest possible illustration that the √n law is
about ratios, and it also shows how misleading the intuition is — 100× the data
buys only 10× the precision.

(e) Chebyshev uses k = 1/√(1 − conf). For 75% confidence, k = 2: 250 ± 16 =
**[234, 266] ms**, width 32 ms. For 95% confidence, k = 1/√0.05 = 4.4721: 250 ±
35.78 = **[214.22, 285.78] ms**, width 71.55 ms.

That is the honest cost of the guarantee: the 95% Chebyshev interval is **2.28×
wider** than the normal one (71.55 vs 31.36). In exchange it requires no
assumption at all about the shape of the latency distribution. For a latency
metric, which is emphatically not normal, that is a good trade at small n — and a
needless one at large n, where the normal approximation becomes reliable and much
tighter.

```python
from math import sqrt

MU, SIGMA = 250.0, 80.0


def normal_ci(n, mu=MU, sigma=SIGMA, z=1.96):
    se = sigma / sqrt(n)
    return se, mu - z * se, mu + z * se


def chebyshev_ci(n, mu=MU, sigma=SIGMA, conf=0.95):
    """Chebyshev: P(|Xbar-mu| >= k*sigma/sqrt(n)) <= 1/k^2,
    so k = 1/sqrt(1 - conf) gives a guaranteed interval at any n."""
    k = 1 / sqrt(1 - conf)
    half = k * sigma / sqrt(n)
    return k, mu - half, mu + half


print("(a)-(c) normal-approximation intervals")
widths = {}
for n in (100, 10_000):
    se, lo, hi = normal_ci(n)
    widths[n] = hi - lo
    print(f"  n={n:6,}: SE={se:7.4f} ms  95% CI=[{lo:.2f}, {hi:.2f}]  "
          f"width={hi - lo:.2f}")

print()
factor = widths[100] / widths[10_000]
print(f"(d) width ratio = {factor:.4f}   sqrt(10000/100) = "
      f"{sqrt(10_000 / 100):.1f}   match: {abs(factor - 10) < 1e-9}")

print()
print("(e) Chebyshev intervals (no normality assumed)")
_, nlo, nhi = normal_ci(100)
normal_w = nhi - nlo
for conf in (0.75, 0.95):
    k, lo, hi = chebyshev_ci(100, conf=conf)
    print(f"  conf={conf:.0%}: k={k:.4f}  CI=[{lo:.2f}, {hi:.2f}]  "
          f"width={hi - lo:.2f}")
print(f"  normal at 95%: width={normal_w:.2f}")
_, clo, chi = chebyshev_ci(100, conf=0.95)
print(f"  -> the guaranteed 95% interval is "
      f"{(chi - clo) / normal_w:.2f}x wider, and needs no assumptions.")
```

</details>

**[ ] Exercise 2 — the √n law empirically.** Run 5,000 independent experiments,
each averaging n draws from Uniform(0,1) (mean 0.5, variance 1/12), for n = 1, 4,
16, 64, 256. Record the empirical standard deviation of the sample means.

(a) Compare each to the theoretical σ/√n. (b) Compute the ratio empirical/theory
at each n. (c) Verify the ratio stays near 1 even at n = 1, where the CLT does not
apply — and explain what is different. (d) Between n = 4 and n = 256, how much
did the standard error drop?

<details>
<summary>Solution</summary>

The theoretical standard errors are σ/√n with σ² = 1/12, σ = 0.288675:

| n | theory σ/√n |
| --- | --- |
| 1 | 0.288675 |
| 4 | 0.144338 |
| 16 | 0.072169 |
| 64 | 0.036084 |
| 256 | 0.018042 |

Because the uniform distribution is symmetric, the *sample* standard deviation
converges to σ quickly even for small n — much faster than the sample mean
converges to μ. So the empirical/theory ratio is close to 1 at every n, including
n = 1, and the mean-based standard error matches theory too. This makes the
uniform a benign test case.

(c) The subtlety: at n = 1 the CLT does not apply — the "average of 1 draw" is
just the raw variable, which is uniform and definitely not normal. But the CLT is
a claim about the *shape* of the sampling distribution, not about its standard
deviation. The mean and variance of the average are exact at every n by
linearity of expectation and variance, with no CLT needed. So the SE formula is
always right; only the *normality* (and hence the 1.96 multiplier) needs the CLT.

This is an important distinction in practice: the 95% interval at n = 1 would
use z = 1.96 and be wrong, while the standard error itself is exactly right.

(d) From n = 4 to n = 256: 0.144338 → 0.018042, a factor of exactly 8 = √(256/4) =
√64. The standard error dropped 8× for 64× the data — precisely the √n law, and
a good demonstration of how slowly precision accumulates.

```python
import math
import random

random.seed(2024)
TRIALS = 5_000
SIZES = [1, 4, 16, 64, 256]
SIGMA = 1 / math.sqrt(12)   # uniform(0,1): variance = 1/12

print(f"{TRIALS:,} experiments per n. True mean 0.5, sigma {SIGMA:.6f}")
print()
print(f"{'n':>5} {'theory SE':>10} {'emp SE':>10} {'ratio':>7} {'emp mean':>10}")

first_ratio, last_ratio = None, None
theories = {}
for n in SIZES:
    theory = SIGMA / math.sqrt(n)
    theories[n] = theory
    means = []
    for _ in range(TRIALS):
        total = 0.0
        for _ in range(n):
            total += random.random()
        means.append(total / n)
    emp_mean = sum(means) / TRIALS
    emp_var = sum((v - emp_mean) ** 2 for v in means) / TRIALS
    emp_se = math.sqrt(emp_var)
    ratio = emp_se / theory
    if n == 4:
        first_ratio = ratio
    if n == 256:
        last_ratio = ratio
    print(f"{n:5d} {theory:10.6f} {emp_se:10.6f} {ratio:7.4f} {emp_mean:10.6f}")

print()
print("(c) every ratio is near 1, INCLUDING n=1 -- because the mean and")
print("    variance of the average are EXACT at every n (linearity of")
print("    expectation/variance). Only the SHAPE needs the CLT, and at n=1")
print("    the shape is uniform, not normal. The SE is right; the 1.96")
print("    multiplier would not be.")
print()
drop = theories[4] / theories[256]
print(f"(d) SE dropped from {theories[4]:.6f} to {theories[256]:.6f}: "
      f"factor {drop:.2f}")
print(f"    data grew {256 / 4:.0f}x, precision improved only {drop:.0f}x")
```

</details>

**[ ] Exercise 3 — Challenge: is your experiment even big enough?** A checkout
page has a 4% conversion rate today. You want to detect a 2% *relative*
improvement (4% → 4.08%) with 80% power at a 5% significance level.

(a) Compute the number of users needed per variant. (b) A colleague says "run it
for a week, we get about 20,000 users per variant". Is that enough? (c) Compute
the minimum detectable effect at n = 20,000 per variant. (d) Explain why
detecting small effects is so expensive, in terms of the SE. (e) Suggest two
practical ways to improve sensitivity without adding users.

<details>
<summary>Solution</summary>

The standard two-proportion z-test sample size formula for equal-sized arms is

    n = 2 · p̄(1 − p̄) · (z_{1−α/2} + z_{1−β})² / (p₂ − p₁)²

with p̄ the pooled mean of the two rates, z_{1−α/2} = 1.96 for α = 0.05, and
z_{1−β} = 0.8416 for 80% power (β = 0.2). Values of Φ⁻¹ come from
`normal_quantile` in [Lesson 65](../part05_probability_statistics/65_continuous_random_variables.md).

(a) p₁ = 0.04, p₂ = 0.0408, p̄ = 0.0404. The difference is 0.0008.

    n = 2(0.0404)(0.9596)(1.96 + 0.8416)² / (0.0008)²
      = 2(0.038768)(7.85718) / 6.4e-7
      = 0.609250 / 6.4e-7
      ≈ **950,888 users per variant**

Nearly a million each, for a two-percent relative gain.

(b) 20,000 per variant is about **2.1%** of what is needed. The test would be
wildly underpowered — which does not mean it "passes", it means it cannot
distinguish the two rates. Running underpowered and getting a non-significant
result is the single most common way experiments mislead teams.

(c) Inverting the formula for the minimum detectable effect δ at n = 20,000:

    δ = (1.96 + 0.8416)·sqrt(2·p̄(1−p̄)/n)
      = 2.8016·sqrt(0.077536/20000)
      = 2.8016(0.0019690)
      ≈ 0.005516

So δ ≈ 0.55 percentage points, i.e. detecting 4.0% → about 4.55%, a **13.8%
relative** improvement — nearly seven times harder than the effect you wanted.

(d) Because the SE of a proportion is √(p(1−p)/n) ≈ √p/n at low rates. At
n = 20,000 the SE is √(0.04 × 0.96/20000) = 0.001386, while the effect being
sought is 0.0008 — **0.58 standard errors**. You cannot reliably detect a signal
smaller than about one standard error, and you want more like 2.8. This is the
whole story in one ratio. Since the required n scales as 1/δ², halving the
detectable effect costs 4× the traffic and quartering it costs 16×.

(e) Two practical routes, neither of which is "get more users":

1. **Increase the effect size.** Run on segments where the change plausibly helps
   more, or accept that a 2% relative gain is not detectable and decide on other
   grounds (strategic value, low cost, low risk). This is the honest move and it
   is under-used.
2. **Reduce the noise per observation.** Variance reduction techniques —
   CUPED (using a pre-experiment metric as a covariate), stratified randomisation,
   or switching to a less noisy primary metric such as revenue per user instead of
   a binary conversion — can cut the required n by 30–50% for the same power. At
   30% variance reduction, n drops from 950,888 to 665,622; at 50%, to 475,444.

The uncomfortable truth worth stating: for small effects, no amount of clever
statistics substitutes for either a large sample or a large effect.

```python
import math
from math import erf, sqrt

# Standard normal quantile by bisection on the CDF (from Lesson 65).
def z_quantile(q):
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if (1 + erf(mid / sqrt(2))) / 2 < q:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


ALPHA, POWER = 0.05, 0.80
z_alpha = z_quantile(1 - ALPHA / 2)
z_beta = z_quantile(POWER)
print(f"z_(1-alpha/2) = {z_alpha:.4f}   z_(power) = {z_beta:.4f}")

P1, P2 = 0.04, 0.04 * 1.02
p_bar = (P1 + P2) / 2
delta = P2 - P1

# (a) required n per variant
n_needed = 2 * p_bar * (1 - p_bar) * (z_alpha + z_beta) ** 2 / delta**2
print()
print(f"(a) baseline {P1:.4f} -> target {P2:.4f} (delta {delta:.5f})")
print(f"    n needed per variant = {math.ceil(n_needed):,}")

# (b) is a week enough?
n_have = 20_000
print(f"(b) we have {n_have:,} per variant = "
      f"{n_have / n_needed * 100:.2f}% of what is needed")

# (c) minimum detectable effect at the size we have
mde = (z_alpha + z_beta) * sqrt(2 * p_bar * (1 - p_bar) / n_have)
print(f"(c) minimum detectable effect = {mde:.6f} "
      f"({P1 * 100:.2f}% -> {(P1 + mde) * 100:.2f}%)")
print(f"    relative effect we can detect = {mde / P1 * 100:.1f}% "
      f"(wanted 2.0%)")

# (d) the SE, for intuition
se = sqrt(P1 * (1 - P1) / n_have)
print(f"(d) SE of the conversion rate at n={n_have:,} = {se:.6f}")
print(f"    the effect we seek is {delta:.5f}, which is "
      f"{delta / se:.2f} SE -- far too small to detect")
print(f"    n scales as 1/delta^2, so halving the effect costs 4x the traffic")

# (e) how much a variance reduction buys
for reduction in (0.0, 0.3, 0.5):
    var_mult = (1 - reduction)
    n_adj = math.ceil(n_needed * var_mult)
    print(f"(e) with {reduction:.0%} variance reduction, "
          f"n needed = {n_adj:,}")
```

</details>

**[ ] Exercise 4 — the SE formula is exact, the normality is not.** Latency
measurements have mean 250 ms and standard deviation 80 ms.
(a) Compute the standard error and the 95% normal interval for n = 100, 400, and
2,500.
(b) Verify empirically that the *empirical* standard error matches
σ/√n at every one of those n, using 20,000 replicates each. Also record the
empirical 95% coverage of the interval.
(c) Explain why the standard error is right at n = 100 while the interval's
coverage may not be.
(d) For n = 100, compute the Chebyshev 75% and 95% intervals and their widths,
and compare with the normal interval.

<details>
<summary>Solution</summary>

(a) $\mathrm{SE} = 80/\sqrt n$, interval $\pm 1.96\,\mathrm{SE}$:

| $n$ | $\mathrm{SE}$ | 95% normal interval | width |
| --- | --- | --- | --- |
| 100 | 8.0000 | [234.32, 265.68] | 31.36 |
| 400 | 4.0000 | [242.16, 257.84] | 15.68 |
| 2,500 | 1.6000 | [246.86, 253.14] | 6.27 |

Widths fall by exactly 2 and 2.5 as $n$ rises 4× and 25× — the √n law again
(√4 = 2, √25 = 5... and $2.5$ here is $31.36/12.5$, from √25 = 5).

(b) The empirical standard error of 20,000 sample means must match theory at every
$n$, because $\mathrm{Var}(\bar X_n) = \sigma^2/n$ is exact and requires only
independence — no CLT. The *coverage*, however, is a statement about the shape,
and at n = 100 with a skewed latency distribution the normal interval tends to
under-cover because it misses the tail.

(c) This is the lesson's sharpest distinction, and it appears in Exercise 2(c) as
well. The mean and variance of a sample mean are **exact at every $n$**, by
linearity of expectation and variance. So $\mathrm{SE} = \sigma/\sqrt n$ is the
correct spread no matter how small $n$ is or how badly shaped $X$ is — and the
ratios in (b) confirm it, sitting within about 1.6% of 1.000 at every $n$.

What the CLT supplies is only the *shape* — that $\bar X_n$ is approximately
normal — and the 1.96 multiplier is a consequence of that shape, not of the
variance. So coverage is a separate matter from spread: it comes out at 94.1%,
95.5% and 94.8% for the three $n$ here, hovering around the nominal 95% but not
landing on it, and it can drift further in either direction for worse-behaved
distributions. This is exactly why the lesson's Chebyshev section exists: a
guarantee that holds at every $n$, in exchange for width.

(d) $k = 2$ gives a guaranteed 75% interval: $250 \pm 16 = [234, 266]$, width 32.
$k = 1/\sqrt{0.05} = 4.4721$ gives a guaranteed 95% interval:
$250 \pm 35.78 = [214.22, 285.78]$, width 71.55 — **2.28× the normal interval**.
Interesting that the 75% Chebyshev interval at 32 ms is only 2% wider than the
95% normal one at 31.36 ms: at modest confidence the guarantee is nearly free,
and it only becomes expensive as you demand more.

```python
import math
import random

MU, SIGMA = 250.0, 80.0
REPLICATES = 4_000


def normal_ci(n, z=1.96):
    se = SIGMA / math.sqrt(n)
    return se, MU - z * se, MU + z * se


def chebyshev_ci(n, conf=0.95):
    k = 1 / math.sqrt(1 - conf)
    half = k * SIGMA / math.sqrt(n)
    return k, MU - half, MU + half


print("(a) normal-approximation intervals")
prev_width = None
for n in (100, 400, 2_500):
    se, lo, hi = normal_ci(n)
    w = hi - lo
    ratio = f"  width/{prev_width:.2f}" if prev_width else ""
    print(f"  n={n:5,}: SE={se:7.4f}  CI=[{lo:.2f}, {hi:.2f}]  width={w:.2f}{ratio}")
    prev_width = w

print()
print(f"(b) empirical SE from {REPLICATES:,} skewed draws -- a latency-like law")
print("    (exponential with mean SIGMA, shifted to MU: skewed, right-tailed)")
print(f"  {'n':>6} {'theory SE':>11} {'emp SE':>10} {'ratio':>7} {'coverage':>10}")
for n in (100, 400, 2_500):
    rng = random.Random(500 + n)
    se = SIGMA / math.sqrt(n)
    lo, hi = MU - 1.96 * se, MU + 1.96 * se
    shift = MU - SIGMA
    means = []
    for _ in range(REPLICATES):
        total = sum(-SIGMA * math.log1p(-rng.random()) for _ in range(n))
        means.append(total / n + shift)
    emp_mean = sum(means) / REPLICATES
    emp_se = math.sqrt(sum((m - emp_mean) ** 2 for m in means) / REPLICATES)
    cov = sum(1 for m in means if lo <= m <= hi) / REPLICATES
    print(f"  {n:6,} {se:11.4f} {emp_se:10.4f} {emp_se / se:7.4f} {cov:9.2%}")

print()
print("(c) the SE is exact at every n (Var = sigma^2/n by linearity) -- ratios")
print("    stay within about 1.6% of 1.000. But the 1.96 multiplier assumes")
print("    NORMALITY, so coverage is a separate question and hovers near the")
print("    nominal 95% rather than landing on it. Chebyshev buys a guarantee.")

print()
print("(d) Chebyshev: guaranteed at any n, no normality assumed")
for conf in (0.75, 0.95):
    k, lo, hi = chebyshev_ci(100, conf)
    print(f"  conf={conf:.0%}: k={k:.4f}  CI=[{lo:.2f}, {hi:.2f}]  "
          f"width={hi - lo:.2f}")
_, nlo, nhi = normal_ci(100)
normal_w = nhi - nlo
k75, clo75, chi75 = chebyshev_ci(100, 0.75)
k95, clo95, chi95 = chebyshev_ci(100, 0.95)
print(f"  normal 95%: width={normal_w:.2f}")
print(f"  -> 95% Chebyshev is {(chi95 - clo95) / normal_w:.2f}x wider;")
print(f"     75% Chebyshev is {(chi75 - clo75) / normal_w:.2f}x wider, i.e. nearly free.")
```

</details>

**[ ] Exercise 5 — the cost of √n, for a benchmark rather than a funnel.** A
benchmark runs a function $n$ times and reports the mean and the standard error.
Measured $\sigma = 15$ ms.
(a) Report mean ± SE for $n$ = 100, 1,000, 10,000, 100,000.
(b) A colleague claims that going from 1,000 to 10,000 runs gives a 10× better
estimate. Quantify the actual improvement in the width.
(c) To get the standard error below 1 ms, what $n$ is required?
(d) Suppose the benchmark instead varies the *input size* $k$ and reports latency
at $k$ = 10, 100, 1,000, keeping the run count at 1,000. Given that the true
latency relationship is $\mu(k) = 2\sqrt k + 5$ ms with $\sigma(k) = 4\sqrt k$,
compute $\mu$, $\sigma$, and the SE at each $k$, and say which axis shows the
√-shaped growth you should expect.

<details>
<summary>Solution</summary>

(a) $\mathrm{SE} = 15/\sqrt n$:

| $n$ | $\mathrm{SE}$ (ms) | mean ± SE |
| --- | --- | --- |
| 100 | 1.5000 | mean ± 1.50 |
| 1,000 | 0.4743 | mean ± 0.474 |
| 10,000 | 0.1500 | mean ± 0.150 |
| 100,000 | 0.0474 | mean ± 0.047 |

(b) From 1,000 to 10,000 the SE falls from 0.4743 to 0.1500 — a factor of
**3.16**, not 10. The interval width falls by the same factor: a 10× increase in
runs buys 3.16× the precision. This is Mistake 4 in the lesson, and the
colleague's intuition is linear in the data when the mathematics is square-root.

(c) $15/\sqrt n < 1$ requires $\sqrt n > 15$, so $n > 225$; at $n = 256$ the SE is
exactly $15/16 = 0.9375$ ms. So 256 runs suffice — and note that 225 runs are
only 2.25× the 100 already used, for a 1.6× tighter bound. Near the target the
√n law is cheap; it becomes brutal only when you keep asking for more.

(d) With $\mu(k) = 2\sqrt k + 5$ and $\sigma(k) = 4\sqrt k$, both scale as
$\sqrt k$:

| $k$ | $\mu(k)$ | $\sigma(k)$ | $\mathrm{SE}$ at n = 1,000 |
| --- | --- | --- | --- |
| 10 | 11.32 | 12.65 | 0.400 |
| 100 | 25.00 | 40.00 | 1.265 |
| 1,000 | 68.25 | 126.49 | 4.000 |

Both the latency and its spread grow like $\sqrt k$, so a 10× increase in input
size gives 3.16× the latency and 3.16× the noise. The SE column shows the same
3.16× per decade, because it is $\sqrt k/\sqrt n$ in disguise — a product of two
square roots, i.e. the $\sqrt{k\,n}$ law for the signal-to-noise ratio of a
square-root-scaled workload.

The engineering point: on *both* axes, 10× more work buys 3.16×, and the only way
to break out is to change the shape of the algorithm. If latency grows as
$\sqrt k$, then quadrupling $k$ doubles both the latency and the spread, and no
amount of repetition makes the relative error smaller — you have changed the
workload, not the estimate. This is why load-shape work (batching, caching,
sharding the input) beats adding benchmark repetitions.

```python
import math

SIGMA = 15.0

print("(a) SE of the benchmark mean")
prev = None
for n in (100, 1_000, 10_000, 100_000):
    se = SIGMA / math.sqrt(n)
    ratio = f"   (improvement {prev / se:.2f}x)" if prev else ""
    print(f"  n={n:7,}: SE = {se:.4f} ms -> report mean +/- {se:.3f}{ratio}")
    prev = se

print()
print("(b) 1,000 -> 10,000 runs: 10x the data, "
      f"{(SIGMA / math.sqrt(1000)) / (SIGMA / math.sqrt(10_000)):.2f}x the precision")
print("    (sqrt(10) = 3.162, not 10)")

target = 1.0
need = (SIGMA / target) ** 2
print()
print(f"(c) SE < {target:.0f} ms needs sqrt(n) > {SIGMA:.0f}, i.e. n > {need:.0f}")
for n in (225, 256, 400):
    print(f"    n={n:4d} -> SE = {SIGMA / math.sqrt(n):.4f} ms")

print()
print("(d) mu(k) = 2*sqrt(k) + 5, sigma(k) = 4*sqrt(k), run count n = 1,000")
N = 1_000
prev_mu = prev_se = None
for k in (10, 100, 1_000):
    mu = 2 * math.sqrt(k) + 5
    sd = 4 * math.sqrt(k)
    se = sd / math.sqrt(N)
    ratio = (f"   mu x{mu / prev_mu:.2f}, SE x{se / prev_se:.2f}"
             if prev_mu else "")
    print(f"  k={k:5,}: mu={mu:7.2f} ms  sigma={sd:7.2f} ms  SE={se:.4f} ms{ratio}")
    prev_mu, prev_se = mu, se
print()
print("Both axes show the same 3.16x-per-decade growth: a square root")
print("in k, a square root in 1/n, so only a shape change helps.")
```

</details>

**[ ] Exercise 6 — Challenge: the CLT on deliberately hostile data, and the
moment where it stops helping.** (a) Take $X$ with $P(X=1) = 0.5$ and
$P(X = 10) = 0.5$ — a two-point, strongly skewed distribution. Compute $\mu$ and
$\sigma$. (b) Compute $\bar X_{10}$'s exact mean and standard deviation from the
Binomial, and its exact distribution shape. Is a normal approximation reasonable
at n = 10? Use the rule $np \ge 10$ and $n(1-p) \ge 10$ on the underlying
Binomial(10, 0.5) to decide. (c) Repeat at n = 100 and n = 10,000, and state at
what point the normal approximation becomes trustworthy. (d) Now replace the
distribution with one that has **no finite variance**: $P(X = 2^k) = 2^{-k}$ for
$k = 1, 2, 3, \dots$. Show that $E[X] = \infty$ and explain what this does to the
standard error and hence to every confidence interval built from it.

<details>
<summary>Solution</summary>

(a) $\mu = 0.5(1) + 0.5(10) = 5.5$.
$E[X^2] = 0.5(1) + 0.5(100) = 50.5$, so
$\sigma^2 = 50.5 - 30.25 = 20.25$ and $\sigma = 4.5$.

The distribution has a mean of 5.5 but half its mass sits at 1, so the median is 1
and the mean is 5.5× the median. Strongly skewed, two-point — about as far from
normal as a bounded variable can be.

(b) $\bar X_{10}$ is the average of 10 i.i.d. draws, so by the exact variance
formula $E[\bar X_{10}] = 5.5$ and
$\mathrm{Var} = 20.25/10 = 2.025$, giving $\mathrm{SE} = 1.4230$. A 95% normal
interval would be $5.5 \pm 2.789 = [2.71, 8.29]$.

Is that reasonable? The CLT rule for a Binomial(10, 0.5) requires $np \ge 10$ and
$n(1-p) \ge 10$, which gives exactly 5 and 5 — **both fail**. And the exact shape
makes the failure visible: $\bar X_{10} = (10S)/10 = S$ where $S \sim
\mathrm{Binomial}(10, 0.5)$, a 11-point distribution on $\{1, 2, \dots, 10\}$. The
normal is a smooth curve; the truth is 11 discrete spikes. The CLT *variance* is
still exactly right, but the interval built with $z = 1.96$ is wrong — and
systematically so, because the normal interval is symmetric around the mean while
the true distribution is not.

(c) At n = 100 the Binomial(100, 0.5) has $np = 50 \ge 10$ and
$n(1-p) = 50 \ge 10$, so the normal approximation is now trustworthy. $\mathrm{SE} =
4.5/10 = 0.45$, interval $5.5 \pm 0.882 = [4.62, 6.38]$. At n = 10,000 the SE is
$4.5/100 = 0.045$ and the interval is $[5.412, 5.588]$ — the shape is now
indistinguishable from normal, and the interval is dominated by width rather than
by approximation error. **The crossover is around n = 50–100 here**, which is why
the rule of thumb uses thresholds of 10 rather than demanding exactness.

(d) $E[X] = \sum_{k\ge1} 2^k \cdot 2^{-k} = \sum_{k\ge1} 1 = \infty$. Every term is
exactly 1, so the series diverges. There is no finite variance either.

Consequences, in order. There is no $\sigma$, so $\mathrm{SE} = \sigma/\sqrt n$ is
**undefined**, and every CLT-based interval in the lesson is unavailable. The
Chebyshev bound also fails, since Chebyshev needs finite variance — that is why
the lesson states the interval requires "any distribution with finite variance".
The sample mean is still almost surely finite and still converges, but *far more
slowly* than $1/\sqrt n$: the rate is $n^{1/\alpha - 1}$ where $\alpha$ is the
tail index, and here the tail has $P(X > t) \approx 1/t$, i.e. $\alpha = 1$, so
the mean converges no faster than $\log n / n$.

The practical rule is therefore: **before quoting any standard error, check that
the variance exists.** Request sizes, latency with a retry storm, and summed
per-entity metrics all produce heavy tails. Report a median or a high quantile
instead, or use a trimmed mean, and never present a σ/√n interval for a variable
whose tail you have not inspected.

```python
import math
from math import comb, sqrt

# (a)-(c) the two-point distribution
print("(a) P(X=1)=P(X=10)=0.5")
mu = 0.5 * 1 + 0.5 * 10
ex2 = 0.5 * 1 + 0.5 * 100
var = ex2 - mu**2
print(f"    mu={mu}, E[X^2]={ex2}, var={var}, sigma={sqrt(var):.4f}")
print(f"    median is 1, mean is {mu:.1f}x the median -> strongly skewed")

print()
print("(b) n=10: exact mean and SE of the average")
for n in (10, 100, 10_000):
    se = sqrt(var / n)
    lo, hi = mu - 1.96 * se, mu + 1.96 * se
    print(f"    n={n:6,}: E[xbar]={mu:.4f}  SE={se:.4f}  "
          f"95% normal CI=[{lo:.4f}, {hi:.4f}]")
    if n <= 100:
        # The CLT rule for Binomial(n, 0.5): np >= 10 and n(1-p) >= 10
        print(f"             Binomial({n}, 0.5): np={n * 0.5}, "
              f"n(1-p)={n * 0.5} -> "
              f"{'OK' if min(n * 0.5, n * 0.5) >= 10 else 'FAILS, not normal'}")
    else:
        print(f"             exact distribution is an 11-point spike set at "
              f"n=10; at n=10,000 it is visually smooth")

print()
print("    at n=10 the truth is Binomial(10, 0.5): 11 discrete spikes, not a curve.")
print(f"    exact P(S=5) = {comb(10, 5) / 1024:.6f}, while a normal with the same")
norm_bin = 1 / (sqrt(2 * math.pi) * sqrt(2.025))
print(f"    mean and variance puts only {norm_bin:.6f} in that unit-wide bin.")
print("    -> the variance is exact; the normal SHAPE is not, so the interval is")
print("       systematically wrong even though its width is right.")

# (d) heavy tail with no finite mean
print()
print("(d) P(X = 2^k) = 2^-k for k >= 1")
running = 0.0
for k in range(1, 9):
    running += 2 ** k * 2 ** (-k)
    print(f"    partial sum of E[X] up to k={k}: {running:.0f} "
          f"(each term is exactly 1)")
print(f"    E[X] = infinity after {len(range(1, 9))} terms and still diverging")
tail_at_t = 1 / 2 ** 8
print(f"    P(X > 256) = {tail_at_t:.6f}, so P(X > t) ~ 1/t: tail index alpha = 1")
print(f"    the mean then converges only like log(n)/n, not 1/sqrt(n)")
print()
print("PRACTICAL RULE: check the variance exists before quoting sigma/sqrt(n).")
print("Chebyshev also fails (it needs finite variance). Report a median or")
print("a high quantile instead, or use a trimmed mean.")
```

</details>

## Summary

- The WLLN says the sample mean converges in probability to μ; the SLLN says the
  path itself converges, almost surely.
- Both require independence; without it, the average can converge to something
  else entirely, as the "copy one coin ten times" case shows.
- The standard error is σ/√n, straight from Var(X̄ₙ) = σ²/n.
- The CLT says the *average* becomes approximately normal regardless of the
  original's shape; the original's shape is never changed.
- Convergence in distribution ⟸ in probability ⟸ almost surely; the CLT gives
  only the weakest, which is why it is so widely applicable.
- Chebyshev gives a valid but wider interval at any n and with no normality
  assumption — useful when n is small or the distribution is skewed.
- Convergence is √n-slow: precision scales with the square root of data, so
  halving an error bar costs 4× the observations.
- The mean and variance of a sample mean are exact at every n; only the
  *normality* of its distribution needs the CLT.

## Next

[69 — Estimation and Hypothesis Testing](../part05_probability_statistics/69_estimation_and_hypothesis_testing.md)
turns these theorems into decisions: maximum likelihood estimation, bias and
variance of estimators, what a p-value actually means, the errors you can make,
power, and A/B testing applied to a real product decision.