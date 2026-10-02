# 69 — Estimation and Hypothesis Testing

**Part**: part05_probability_statistics · **Prerequisites**: 68 · **Time**: 45 min

---

## In Plain Words

Two theorems let you average a lot of noise. This lesson turns them into
decisions.

First, **estimation**: you do not know the true conversion rate, so you pick a
number. The best such number is the *maximum likelihood estimate* — the value
that makes the data you actually observed as unsurprising as possible. For a
success rate it is just the observed fraction, and the calculus proving that is
three lines.

Second, **hypothesis testing**: you have a hunch, and you want to know whether the
data argues against it. You state the hunch formally, compute how surprising the
data would be if the hunch were true, and call that probability a *p-value*.

Here is the part everyone gets wrong, so we will say it plainly. **A p-value is
not the probability that the null hypothesis is true.** It is the probability of
data at least this extreme, *assuming* the null is true. It is a statement about
the data, not about the hypothesis. The smaller it is, the more the data
contradicts your hunch — but it never tells you the probability your hunch is
wrong, and it certainly does not tell you the probability the alternative is true.

Alongside p-values come the two ways to be wrong. You can reject a true hypothesis
(a false alarm), or fail to reject a false one (you missed a real effect). **You
can never avoid both at once** — trade one for the other with the significance
level. And *power* is the probability of detecting a real effect when it exists.
An experiment with no power teaches you nothing regardless of its p-value.

## Why Computer Science Cares

- **A/B testing**, which is the highest-volume application of this material in
  industry, and where misreading p-values causes real money to be lost.
- **Model evaluation.** "Is this model's accuracy better than that one?" is a
  hypothesis test on paired data, and the paired test is much more powerful than
  comparing two independent samples.
- **Alert thresholds and anomaly detection.** Deciding when a metric has moved
  enough to page someone is a significance test, and choosing the threshold is
  choosing α and the power.
- **Benchmark comparisons.** Reporting "42.1 ms vs 42.3 ms, not significant" is a
  correct use of hypothesis testing, and often the most valuable sentence in a
  performance report.
- **Interviews.** "How many samples do you need?" and "what is a p-value?" are
  standard questions, and the second one has a famously correct answer.

## The Formal Version

**Definition.** An *estimator* is a statistic T(X₁, …, Xₙ) used as a guess for a
parameter θ. It is *unbiased* if E[T] = θ for every θ.

**Definition.** The *bias* of T is Bias(T) = E[T] − θ. The *mean squared error*
is MSE(T) = E[(T − θ)²] = Var(T) + Bias(T)².

**Explanation.** MSE is what you actually care about, and it decomposes into the
two things you can trade off: the estimator's variance (its noise) and the square
of its bias (its systematic error). So MSE(T) = Var(T) + Bias² is the single
formula that organises estimator comparison, and it is the "bias–variance
trade-off" in one line.

**Definition.** The *maximum likelihood estimate* (MLE) θ̂ is the value of θ
maximising the likelihood L(θ) = P(data | θ).

**Theorem.** For i.i.d. Bernoulli(p) data with k successes in n trials, the MLE is
p̂ = k/n.

**Proof.** L(p) = p^k(1−p)^(n−k). Take logs:
ℓ(p) = k ln p + (n−k) ln(1−p). Differentiate: k/p − (n−k)/(1−p) = 0, which gives
k(1−p) = p(n−k), so k = pn, hence p̂ = k/n. The second derivative is
−k/p² − (n−k)/(1−p)² < 0, so this is a maximum, unique when 0 < k < n. ∎

**Definition.** For two proportions p̂₁ and p̂₂ from samples of sizes n₁, n₂, the
*pooled estimate* is p̄ = (k₁ + k₂)/(n₁ + n₂), and the test statistic for
H₀: p₁ = p₂ is

    z = (p̂₁ − p̂₂) / sqrt(p̄(1 − p̄)(1/n₁ + 1/n₂))

**Explanation.** The denominator is the standard error of the difference under the
null. The numerator is the observed difference. z measures how many standard
errors apart the two rates are, and by the CLT that quantity is approximately
standard normal when the null holds — which is exactly what the p-value needs.

**Definition.** The *p-value* for a test statistic z is

    p-value = P(|Z| ≥ |z_obs|)   under the null

**Theorem (the two errors).** Rejecting H₀ when H₀ is true is a **Type I** error,
with probability α (the significance level). Failing to reject when H₀ is false
is a **Type II** error, with probability β. **Power** is 1 − β.

**Explanation.** α is chosen *before* seeing data, precisely so that the false
alarm rate is controlled. Power depends on the effect size, n, and α — and it is
always a property you should check *before* running anything.

**Definition.** The *confidence interval* for a parameter at level 1 − α is the set
of θ values not rejected by the corresponding test at level α. For a mean,

    p̂ ± z_{1−α/2} · SE

This definition is the reason the "95%" has the interpretation it does. If the
procedure were repeated many times, 95% of the intervals constructed would
contain the fixed true value.

**Definition.** A *false discovery rate* context: if you run m independent tests at
level α, the expected number of false positives is mα. This is why α = 0.05 with
50 comparisons yields about 2.5 spurious "discoveries" — the reason for
Benjamini–Hochberg correction in large-scale inference.

## Worked Example

### Example A — MLE for a Bernoulli rate, derived properly

Suppose 400 users visit a checkout page and 31 convert. Estimate the conversion
rate.

**The likelihood.** Each user independently converts with probability p, so

    L(p) = p³¹(1 − p)³⁶⁹

**Log-likelihood** (log makes products into sums and is maximised at the same
point):

    ℓ(p) = 31 ln p + 369 ln(1 − p)

**Differentiate and solve:**

    ℓ'(p) = 31/p − 369/(1 − p) = 0
    → 31(1 − p) = 369p
    → 31 = 400p
    → p̂ = 31/400 = 0.0775

So the estimate is **7.75%**. The general identity: for Bernoulli data the MLE is
always the observed fraction. The calculus exists to prove that the obvious answer
is the right one, which is not always true for other models.

**Standard error.** SE = √(p̂(1 − p̂)/n) = √(0.0775 × 0.9225/400) = √(1.787e-4) =
0.013368.

**95% confidence interval:** 0.0775 ± 1.96(0.013368) = 0.0775 ± 0.026201, giving

    [0.05130, 0.10370]

**The honest reading.** If you ran this measurement afresh many times, about 95%
of intervals built this way would capture the true rate. This particular number,
0.0775, is a fixed point estimate and the true rate is a fixed number — the 95%
belongs to the *procedure*, not to this measurement. Writing "there is a 95%
chance the true rate is between 5.1% and 10.4%" is the base-rate fallacy from
[Lesson 62](../part05_probability_statistics/62_conditional_probability_and_bayes.md) applied to a frequentist
object, and it is the single most common statistical misstatement in product work.

### Example B — a two-sided test, worked by hand

The old checkout page converts 7% of users. A redesign is live and 22 of 300 users
have converted. Is the redesign working?

**Step 1 — state the hypotheses.** H₀: p = 0.07 (no change) versus H₁: p ≠ 0.07.
Note this is *two-sided*: we would also be interested if the redesign made things
worse.

**Step 2 — compute the observed rates.** p̂₁ = 22/300 = 0.07333. The difference is
0.07333 − 0.07 = 0.00333.

**Step 3 — pool under the null.** For a two-proportion test, pool:
p̄ = (22 + 21)/(300 + 300) = 43/600 = 0.071667. Here 21 = 0.07 × 300.

**Step 4 — standard error of the difference.**

    SE = sqrt(0.071667 × 0.928333 × (1/300 + 1/300))
       = sqrt(0.066531 × 0.0066667)
       = sqrt(4.4354e-4)
       = 0.021060

**Step 5 — the test statistic.** z = 0.00333/0.021060 = 0.1584.

**Step 6 — the p-value.** P(|Z| ≥ 0.1584) = 2(1 − Φ(0.1584)) = 2(0.4371) = **0.8742**.

**Step 7 — the decision.** 0.8742 ≫ 0.05, so we **fail to reject** H₀.

**Step 8 — what that does not mean.** It does *not* mean the redesign has no
effect. It means the data is entirely consistent with no effect — we would see
exactly this result 87% of the time if there were truly no change. The observed
difference (0.33 percentage points) is 0.16 standard errors, which is far too
small to distinguish from noise.

**Step 9 — power.** For this sample size, what effect *would* we have detected?
The minimum detectable effect at 80% power is roughly
(1.96 + 0.8416) × SE = 2.8016 × 0.021060 = 0.059, i.e. 5.9 percentage points. A
redesign improving conversion by less than ~6 points is invisible at n = 300 per
arm. That is the honest summary of the experiment: *we ran an experiment too small
to answer the question.*

### Example C — what a p-value is not, concretely

The following is the canonical demonstration.

**Setup.** A drug is tested against a placebo. Let H₀ be "the drug has no effect"
and suppose that is in fact true. Look at many independent studies. Studies
produce p-values below 0.05 about **5% of the time** — that is what α = 0.05
*means*.

Now, given that a study reported p < 0.05, what is the probability the drug
really works?

Let W = "drug works", P(W) = 0.001 (a genuinely effective but rare treatment),
P(Wᶜ) = 0.999. Let the study have 80% power when the drug works and 5% false
alarm rate when it does not.

Then:

    P(p < 0.05) = 0.80(0.001) + 0.05(0.999) = 0.0008 + 0.04995 = 0.05075
    P(W | p < 0.05) = 0.0008 / 0.05075 ≈ **0.0158**

So even given a "significant" result, the probability the drug works is about
**1.6%**, not 95%. The base rate dominates: a false alarm from a huge pool of
ineffective treatments swamps the true positives from a small pool of effective
ones.

**Note what this is.** This is exactly the base-rate fallacy of
[Lesson 62](../part05_probability_statistics/62_conditional_probability_and_bayes.md), now applied to
frequentist output. "Significant" ≠ "probably true". The correct conclusion from
"p < 0.05" is narrow: *if the null were true, data this extreme would be
unusual.* Nothing more.

## Runnable Code

### MLE for a Bernoulli rate, derived and verified

```python
from math import log, sqrt


def bernoulli_log_likelihood(p, k, n):
    """log L(p) = k*ln(p) + (n-k)*ln(1-p)."""
    if p <= 0 or p >= 1:
        return float("-inf")
    return k * log(p) + (n - k) * log(1 - p)


def mle_by_grid(k, n, steps=200001):
    """Brute-force the likelihood, just to see the maximum."""
    best_p, best_ll = 0.0, float("-inf")
    for i in range(1, steps):
        p = i / (steps - 1)
        ll = bernoulli_log_likelihood(p, k, n)
        if ll > best_ll:
            best_ll, best_p = ll, p
    return best_p, best_ll


K, N = 31, 400

print(f"{K} successes out of {N} trials")
print(f"analytic MLE  = k/n = {K / N:.6f}")
p_grid, ll_grid = mle_by_grid(K, N)
print(f"grid search   = {p_grid:.6f}   (agrees to 6dp: "
      f"{abs(p_grid - K / N) < 1e-6})")
print()
print("the likelihood curve, sampled:")
for p in (0.03, 0.05, K / N, 0.10, 0.15, 0.20):
    print(f"  p={p:.4f}  logL = {bernoulli_log_likelihood(p, K, N):10.4f}")
print(f"  p={K/N:.4f}  logL = {ll_grid:10.4f}   <- the maximum")
print()

# Why the observed fraction is the answer: the derivative is zero there.
def derivative(p, k, n):
    """d(logL)/dp = k/p - (n-k)/(1-p), zero exactly at p = k/n."""
    return k / p - (n - k) / (1 - p)


print(f"d(logL)/dp at p = k/n = {derivative(K / N, K, N):.2e}  (zero)")
print()
print("as k changes with n fixed, the MLE moves to match -- that is what")
print("'the estimate is the observed fraction' means:")
for k in (20, 31, 50):
    print(f"  k={k:3d} -> p_hat = {k / N:.4f}")
```

### Bias and variance of estimators

```python
import random

random.seed(31415)


def simulate(estimator, true_p, n, trials=20_000):
    """Run `trials` experiments of size n; return (mean, variance)."""
    rng = random.Random(1234 + n)
    values = [estimator(true_p, n, rng) for _ in range(trials)]
    mean = sum(values) / trials
    var = sum((v - mean) ** 2 for v in values) / trials
    return mean, var


def binom(rng, n, p):
    """A draw of the SUCCESS COUNT k ~ Binomial(n, p_true).

    The three estimators below differ only in how they post-process k, so the
    binomial draw is factored out and shared -- and for large n it is taken
    from the normal approximation (Lesson 68) rather than by summing n
    Bernoulli trials, which would be far too slow for 20,000 experiments.
    """
    if n <= 200:
        return sum(1 for _ in range(n) if rng.random() < p)
    mean = n * p
    sd = (n * p * (1 - p)) ** 0.5
    return min(n, max(0, int(round(rng.gauss(mean, sd)))))


def mle(p_true, n, rng):
    """The MLE: the observed fraction."""
    return binom(rng, n, p_true) / n


def estimator_two(p_true, n, rng):
    """A biased estimator: forget the 10% of traffic we cannot observe."""
    return binom(rng, n, p_true) / (0.9 * n)


def estimator_shrink(p_true, n, rng):
    """Bias-variance trade-off: shrink the MLE toward 0.5 a little."""
    return 0.95 * (binom(rng, n, p_true) / n) + 0.05 * 0.5


TRUE_P = 0.2
print(f"true p = {TRUE_P}\n")
print(f"{'n':>6} {'estimator':>12} {'mean':>9} {'bias':>9} "
      f"{'variance':>10} {'MSE':>10}")
for n in (50, 500, 5000):
    for name, est in (("MLE (k/n)", mle),
                      ("biased /0.9", estimator_two),
                      ("shrunk 0.95", estimator_shrink)):
        m, v = simulate(est, TRUE_P, n)
        bias = m - TRUE_P
        mse = v + bias**2
        print(f"{n:6d} {name:>12} {m:9.5f} {bias:+9.5f} {v:10.6f} {mse:10.6f}")
    print()

print("Read three things off this table:")
print(" 1. The MLE's bias shrinks with n (like 1/n): it is consistent.")
print(" 2. The biased estimator's bias does NOT shrink -- it is forever.")
print(" 3. The shrunk estimator trades a little bias for a lot less variance")
print("    at small n, and converges to the MLE as n grows.")
print("    This is the bias-variance trade-off, in one table.")
```

### A complete two-proportion z-test

```python
from math import erf, sqrt


def normal_cdf(x):
    return 0.5 * (1 + erf(x / sqrt(2)))


def two_proportion_z_test(k1, n1, k2, n2):
    """Compare two proportions. Returns a dict of every intermediate."""
    p1, p2 = k1 / n1, k2 / n2
    p_pool = (k1 + k2) / (n1 + n2)          # pooled under H0
    se = sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    diff = p1 - p2
    z = diff / se
    p_two = 2 * (1 - normal_cdf(abs(z)))
    p_one_greater = 1 - normal_cdf(z)
    return {
        "p1": p1, "p2": p2, "pooled": p_pool, "se": se, "diff": diff,
        "z": z, "p_two_sided": p_two, "p_one_sided_greater": p_one_greater,
        "ci_lo": diff - 1.96 * se, "ci_hi": diff + 1.96 * se,
    }


r = two_proportion_z_test(k1=22, n1=300, k2=21, n2=300)
print("Does the redesign beat the old checkout page?")
print(f"  variant  : {r['p1'] * 100:.2f}%  ({22}/300)")
print(f"  control  : {r['p2'] * 100:.2f}%  ({21}/300)")
print(f"  pooled   : {r['pooled']:.6f}")
print(f"  SE of difference : {r['se']:.6f}")
print(f"  difference       : {r['diff']:+.6f}")
print(f"  z                : {r['z']:+.4f}")
print(f"  p-value (2-sided): {r['p_two_sided']:.4f}")
print(f"  p-value (1-sided): {r['p_one_sided_greater']:.4f}")
print(f"  95% CI on the difference: "
      f"[{r['ci_lo'] * 100:+.2f}, {r['ci_hi'] * 100:+.2f}] percentage points")
print()
print(f"alpha = 0.05 -> {'REJECT' if r['p_two_sided'] < 0.05 else 'FAIL TO REJECT'} H0")
print("The CI contains 0, which is exactly the same conclusion -- that is")
print("not a coincidence; a CI is the set of hypotheses the test rejects.")

print()
print("The same comparison at a realistic sample size:")
for n_per_arm in (300, 3_000, 30_000, 300_000):
    r2 = two_proportion_z_test(k1=round(0.0733 * n_per_arm), n1=n_per_arm,
                               k2=round(0.07 * n_per_arm), n2=n_per_arm)
    print(f"  n={n_per_arm:7,} per arm: diff {r2['diff'] * 100:+.4f} pp, "
          f"z = {r2['z']:+.2f}, p = {r2['p_two_sided']:.4f}")
print()
print("The same 0.33-point effect becomes significant only at large n.")
print("That is the entire power story in one table.")
```

### The p-value misinterpretation, computed

```python
# The base rate problem: what does p < 0.05 actually tell you?
#
# Setup: a treatment has a 0.1% prior chance of being genuinely effective.
# A study has 80% power when it works, and 5% false alarm when it does not.

PRIOR = 0.001          # P(works) -- the base rate
POWER = 0.80           # P(significant | works)
ALPHA = 0.05           # P(significant | does not work)


def posterior_given_significant(prior, power, alpha):
    """P(works | significant), by Bayes' rule."""
    true_positive = power * prior
    false_positive = alpha * (1 - prior)
    return true_positive / (true_positive + false_positive)


print(f"prior P(works)          = {PRIOR:.4f}")
print(f"power P(sig | works)    = {POWER:.2f}")
print(f"alpha  P(sig | not work) = {ALPHA:.2f}")
print()
tp = POWER * PRIOR
fp = ALPHA * (1 - PRIOR)
print(f"  true positives  = 0.80 * 0.001 = {tp:.5f}")
print(f"  false positives = 0.05 * 0.999 = {fp:.5f}")
print(f"  P(significant)  = {tp + fp:.5f}")
print()
post = posterior_given_significant(PRIOR, POWER, ALPHA)
print(f"P(works | significant) = {tp:.5f} / {tp + fp:.5f} = {post:.4f}")
print(f"  -> only {post * 100:.2f}% even though p < 0.05!")
print()
print("The false positives come from a population 999x larger than the")
print("true positives, so they dominate completely. Increasing power helps:")
for pw in (0.8, 0.9, 0.95, 0.99):
    print(f"  power={pw:.2f} -> P(works | significant) = "
          f"{posterior_given_significant(PRIOR, pw, ALPHA):.4f}")
print()
print("but the only way to fix a LOW PRIOR is a low alpha, or a prior study:")
for pr in (0.001, 0.01, 0.05, 0.2):
    print(f"  prior={pr:.3f} -> P(works | significant) = "
          f"{posterior_given_significant(pr, 0.8, 0.05):.4f}")
```

### Type I and Type II errors, demonstrated

```python
import random
from math import erf, sqrt

random.seed(5)


def normal_cdf(z):
    return 0.5 * (1 + erf(z / sqrt(2)))


def two_prop_p(k1, n1, k2, n2):
    """Two-sided p-value for a difference in proportions."""
    p_pool = (k1 + k2) / (n1 + n2)
    se = (p_pool * (1 - p_pool) * (1 / n1 + 1 / n2)) ** 0.5
    z = (k1 / n1 - k2 / n2) / se
    return 2 * (1 - normal_cdf(abs(z)))


def binom(rng, n, p):
    """Binomial(n, p) by direct simulation -- only used for SMALL n here."""
    return sum(1 for _ in range(n) if rng.random() < p)


CONTROL_P = 0.07
ALPHA = 0.05

print("Demonstrating Type I and Type II errors with a REALISTIC effect.")
print("We do not know whether the effect is present, so we test both worlds")
print("many times and count the four possible outcomes.")
print()

# Effect is large enough that 2000/arm can detect it.
for true_effect, n_arm, trials in ((0.02, 2_000, 3_000),):
    rng = random.Random(99)
    type1 = type2 = correct_reject = correct_keep = 0
    for _ in range(trials):
        has_effect = rng.random() < 0.5      # the hidden truth, chosen first
        p_variant = CONTROL_P + (true_effect if has_effect else 0.0)
        k_a = binom(rng, n_arm, CONTROL_P)
        k_b = binom(rng, n_arm, p_variant)
        reject = two_prop_p(k_b, n_arm, k_a, n_arm) < ALPHA

        if reject and not has_effect:
            type1 += 1
        elif reject and has_effect:
            correct_reject += 1
        elif not reject and has_effect:
            type2 += 1
        else:
            correct_keep += 1

    print(f"effect = +{true_effect * 100:.1f} pp, n = {n_arm:,}/arm, "
          f"{trials:,} trials")
    print(f"  Type I  (rejected a true H0)      : {type1 / trials:.4f}   "
          f"[target alpha = {ALPHA}]")
    print(f"  Type II (missed a real effect)    : {type2 / trials:.4f}")
    print(f"  power = 1 - beta                  : {correct_reject / trials:.4f}")
    print(f"  correctly kept H0                 : {correct_keep / trials:.4f}")
    print()

# Now a small effect, with n large enough to detect it.
print("Now a SMALL effect (+0.5 pp), and watch power fall as n grows:")
print(f"{'n per arm':>10} {'alpha realised':>15} {'beta':>8} {'power':>8}")
for n_arm in (2_000, 20_000, 200_000):
    rng = random.Random(4242 + n_arm)
    trials = 3_000
    type1 = type2 = 0
    for _ in range(trials):
        has_effect = rng.random() < 0.5
        p_variant = CONTROL_P + (0.005 if has_effect else 0.0)
        # Sample Binomial(n, p) as Binomial via sum of Bernoulli in BLOCKS:
        # for large n use the normal approximation instead of n draws.
        mean = n_arm * p_variant
        sd = (n_arm * p_variant * (1 - p_variant)) ** 0.5
        k_b = max(0, min(n_arm, int(round(rng.gauss(mean, sd)))))
        mean_a = n_arm * CONTROL_P
        sd_a = (n_arm * CONTROL_P * (1 - CONTROL_P)) ** 0.5
        k_a = max(0, min(n_arm, int(round(rng.gauss(mean_a, sd_a)))))
        reject = two_prop_p(k_b, n_arm, k_a, n_arm) < ALPHA
        if reject and not has_effect:
            type1 += 1
        elif not reject and has_effect:
            type2 += 1

    print(f"{n_arm:10,} {type1 / trials:14.4f} {type2 / trials:8.4f} "
          f"{1 - type2 / trials:8.4f}")

print()
print("Type I stays pinned at alpha regardless of n -- that is the whole")
print("point of fixing alpha in advance. Power, however, climbs toward 1")
print("as n grows, and it climbs much faster for larger effects.")
```

This demonstration keeps alpha fixed at 0.05 in every case, and power varies as
expected.

### A full A/B test with a decision

```python
from math import erf, sqrt


def cdf(z):
    return 0.5 * (1 + erf(z / sqrt(2)))


def ab_test(conv_a, n_a, conv_b, n_b, alpha=0.05):
    p_a, p_b = conv_a / n_a, conv_b / n_b
    p_pool = (conv_a + conv_b) / (n_a + n_b)
    se = sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))
    diff = p_b - p_a
    z = diff / se
    p_value = 2 * (1 - cdf(abs(z)))
    lo, hi = diff - 1.96 * se, diff + 1.96 * se
    return {
        "rate_a": p_a, "rate_b": p_b, "lift": diff / p_a,
        "diff": diff, "se": se, "z": z, "p_value": p_value,
        "ci": (lo, hi), "significant": p_value < alpha,
    }


CASES = [
    ("clear winner",        1200, 20000, 1320, 20000),
    ("small but real",       1200, 20000, 1240, 20000),
    ("noise",                1200, 20000, 1210, 20000),
    ("directionally worse",  1200, 20000, 1160, 20000),
    ("tiny sample",           120,   2000,  132,   2000),
]

print(f"{'case':20} {'A':>8} {'B':>8} {'lift':>8} {'p-value':>9} "
      f"{'95% CI of diff':>22} {'decision':>16}")
for name, ca, na, cb, nb in CASES:
    r = ab_test(ca, na, cb, nb)
    ci = f"[{r['ci'][0]*100:+.2f}, {r['ci'][1]*100:+.2f}]pp"
    if r["significant"] and r["diff"] > 0:
        decision = "SHIP B"
    elif r["significant"] and r["diff"] < 0:
        decision = "KEEP A"
    elif r["ci"][0] > 0:
        decision = "ship B"
    elif r["ci"][1] < 0:
        decision = "keep A"
    else:
        decision = "no decision"
    print(f"{name:20} {r['rate_a']*100:7.2f}% {r['rate_b']*100:7.2f}% "
          f"{r['lift']*100:+7.2f}% {r['p_value']:9.4f} {ci:>22} {decision:>16}")

print()
print("Note the 'noise' row: p is large, so we learned nothing -- but that is")
print("not evidence of no effect. The CI is wide and straddles zero, so the")
print("honest answer is 'underpowered', not 'no difference'.")
print()
print("Note the 'tiny sample' row: the SAME relative lift as 'small but real',")
print("but at 1/10 the sample size it cannot be detected. Sample size, not")
print("effect size, is what failed there.")
```

### With Libraries

The block below needs `numpy` and `matplotlib`. It is optional and `run_all.py`
skips it; everything above is standard library only.

```python  title="With Libraries: power curves and the significance threshold"
# Requires numpy / matplotlib -- not runnable in the stdlib-only check.
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))

# 1. Power as a function of sample size, for several effect sizes.
ax = axes[0]
p0 = 0.07
ns = np.logspace(2, 6, 60)
for delta in (0.02, 0.005, 0.002, 0.001):
    power = []
    for n in ns:
        se = np.sqrt(p0 * (1 - p0) * 2 / n)
        z = delta / se
        # Power for a two-sided test at alpha = 0.05.
        power.append(stats.norm.cdf(z - stats.norm.ppf(0.975))
                     + stats.norm.cdf(-z - stats.norm.ppf(0.975)))
    ax.semilogx(ns, power, lw=2, label=f"$\\Delta$ = {delta*100:.1f} pp")
ax.axhline(0.8, ls="--", color="grey", label="80% power target")
ax.set_xlabel("users per variant (log scale)")
ax.set_ylabel("power = 1 - $\\beta$")
ax.set_title("Power vs sample size, 7% baseline, $\\alpha$ = 0.05")
ax.legend(fontsize=8)
ax.set_ylim(0, 1.02)

# 2. Where the p-value threshold cuts, and what it costs.
ax = axes[1]
mu, se = 0.0, 1.0
xs = np.linspace(-4, 4, 500)
null_pdf = stats.norm.pdf(xs, mu, se)
alt_pdf = stats.norm.pdf(xs, mu + 1.5, se)
alpha_area = stats.norm.sf(stats.norm.ppf(0.975)) * 2
beta_area = stats.norm.cdf(stats.norm.ppf(0.975) - 1.5, loc=1.5)

ax.plot(xs, null_pdf, color="navy", lw=2, label="H0 is true: N(0, 1)")
ax.plot(xs, alt_pdf, color="crimson", lw=2, label="H0 false: N(1.5, 1)")
cut = stats.norm.ppf(0.975)
ax.axvspan(-cut, cut, color="gold", alpha=0.35,
           label=f"reject region ($\\alpha$ = {alpha_area:.3f})")
ax.fill_between([-cut, cut], alt_pdf[xs <= cut], alt_pdf[xs >= -cut][::-1],
                color="crimson", alpha=0.15)
ax.text(-3.4, 0.14, f"Type I\n$\\alpha$ = {alpha_area:.3f}",
        fontsize=9, color="darkgoldenrod")
ax.text(0.5, 0.20, f"Type II\n$\\beta$ = {beta_area:.3f}\npower = {1-beta_area:.3f}",
        fontsize=9, color="crimson")
ax.set_xlabel("test statistic z")
ax.set_ylabel("density")
ax.set_title("One threshold, two error types")
ax.legend(fontsize=8, loc="upper left")

plt.tight_layout()
plt.savefig("power_and_errors.png", dpi=110)
print("wrote power_and_errors.png")
```

## Common Mistakes

**Mistake 1 — reading a p-value as P(null is true).**
Wrong: "the p-value is 0.03, so there is a 3% chance the null hypothesis is
true." Right: the p-value is P(data this extreme | null true). To get
P(null | data) you must go through Bayes' rule and use a prior, and the answer
will usually be very different — in the drug example, 1.6% rather than 95%. This
is the most consequential error in applied statistics.

**Mistake 2 — p-hacking.** Running twenty metrics and reporting the one that
crossed 0.05 gives you a 64% chance of a false positive, not 5%
(1 − 0.95²⁰ = 0.642). Pre-register your primary metric, or correct for multiple
comparisons.

**Mistake 3 — treating "not significant" as "no effect".**
Wrong: "p = 0.4, so the redesign does nothing." Right: the experiment failed to
detect an effect. The confidence interval is the honest summary: if it is wide,
the experiment was underpowered and you should report "we could not resolve
anything above X points", which is actionable and true.

**Mistake 4 — peeking at the data and stopping when p < 0.05.**
This inflates your false positive rate dramatically, because you are choosing the
luckiest moment out of many. If you must monitor continuously, use a sequential
test with alpha spending or an always-valid confidence sequence. Fixed-horizon
rules exist precisely because peeking is so common and so harmful.

**Mistake 5 — using the wrong variance in the SE of a difference.**
For two independent proportions you need the *pooled* variance under the null, not
the average of the two separate variances and certainly not a variance computed
from post-hoc-selected data. Getting this wrong changes the test statistic and
therefore the p-value, usually making effects look more significant than they are.

## Formula Sheet

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$T = T(X_1,\dots,X_n)$` | estimator | A statistic used as a guess for a parameter θ. | Any point estimate. |
| `$\mathrm{Bias}(T)$ | $= E[T] - \theta$` | Systematic error: where the estimator sits on average, away from the truth. | Comparing estimators. Bias that **does not** shrink with $n$ is fatal. |
| `$E[T] = \theta$` | unbiased for **every** θ | No systematic error. | The MLE is unbiased here. |
| `$\mathrm{MSE}(T)$ | `$= E[(T-\theta)^2] = \mathrm{Var}(T) + \mathrm{Bias}(T)^2$ | Mean squared error: noise plus systematic error. | The organising formula for estimator comparison. Minimise this, not variance alone. |
| likelihood `$L(\theta)$ | `$= P(\text{data}\mid\theta)$` | How likely the observed data is, given θ. **Never** $P(\theta\mid\text{data})$. | The object the MLE maximises. Getting this direction wrong is Mistake 1. |
| log-likelihood `$\ell(\theta)$ | `$\ell = \ln L$` | Same maximiser, products become sums. | Every MLE derivation. |
| `$\hat\theta_{\text{MLE}}$ | `$= \arg\max_\theta L(\theta)$` | The parameter value making the observed data least surprising. | Default estimator for Bernoulli/Binomial/Poisson data. |
| Bernoulli MLE | `$\hat p = k/n$` | The observed fraction. | Conversion, CTR, error rates. `87/1500 = 0.058`. |
| MLE derivative | `$\ell'(p) = k/p - (n-k)/(1-p) = 0 \Rightarrow p = k/n$`; `$\ell'' < 0$` | Three lines of calculus proving the obvious answer is right. | Any time someone says "the MLE is just the average" and needs justifying. |
| pooled estimate | `$\bar p = \dfrac{k_1 + k_2}{n_1 + n_2}$` | The common rate assumed under `H₀: p_1 = p_2`. | **Pooling is required** under the null. Using the unpooled SE is Mistake 5. |
| SE of the difference | `$\mathrm{SE} = \sqrt{\bar p(1-\bar p)\left(\frac{1}{n_1}+\frac{1}{n_2}\right)}$` | How far apart two rates are expected to be if they were equal. | Every two-proportion test. `600/300 vs 600/300`: SE $= 0.0023933$. |
| test statistic | `$z = \dfrac{\hat p_1 - \hat p_2}{\mathrm{SE}} \approx \mathcal{N}(0,1)$` | Observed difference in units of standard errors. | A two-proportion z-test. `z = 0.8357` in Exercise 3. |
| **p-value** | `$P(\lvert Z\rvert \ge \lvert z_{\text{obs}}\rvert)$` **under $H_0$** | Probability of data **at least this extreme**, *assuming the null is true*. A statement about the data, never about the hypothesis. | Every decision. It is **not** $P(H_0 \mid \text{data})$. |
| Type I error | `$\alpha = P(\text{reject } H_0 \mid H_0 \text{ true})$` | False alarm. Fixed **in advance**, which is the whole point. | Choosing the significance level. |
| Type II error | `$\beta = P(\text{fail to reject } H_0 \mid H_0 \text{ false})$` | Missed real effect. | Reporting an inconclusive result honestly. |
| **power** | `$1 - \beta$ | $P(\text{detect the effect} \mid \text{effect is real})$` | Check it **before** running anything. A p-value from a powerless test teaches nothing. |
| power (two-sided, α = 0.05) | `$\approx \Phi\!\left(\dfrac{\delta}{\mathrm{SE}} - 1.96\right)$` | Effect size in standard errors, shifted by the threshold. | At δ = 0.2 pp and SE = 0.0024: power = **0.1304**, about 1 in 8. |
| sample size (two proportions) | `$n = \dfrac{2\bar p(1-\bar p)(z_{1-\alpha/2} + z_{1-\beta})^2}{\delta^2}$` per arm | Solves the power equation for $n$. $z = 1.96$ at α = 0.05, $z = 0.8416$ at 80% power. | Designing an experiment. A 1 pp effect at 6% baseline needs **8,991 per arm**. |
| confidence interval | `$\hat\theta \pm z_{1-\alpha/2}\,\mathrm{SE}$` | The set of θ values the test at level α does **not** reject. | Reporting results. "Not significant" ⇔ "CI contains 0" — the same statement. |
| correct CI reading | if repeated $m$ times, about `$(1-\alpha)m$` intervals contain the fixed θ | About the **procedure**, not the interval. | Every write-up. `95%` is not a probability the parameter is in this range. |
| `$P(W\mid \text{sig})$ | `$= \dfrac{\text{power}\cdot P(W)}{\text{power}\cdot P(W) + \alpha\,(1-P(W))}$` | The number you actually want, and it needs a prior. | After a significant result. With prior 0.001 and power 0.80: **0.0158**, not 0.95. |
| multiple comparisons | `$m$ independent tests ⇒ $m\alpha$ expected false positives | 20 tests at α = 0.05 give `1 - 0.95^20 = 0.642`. | Pre-register a primary metric, or apply Benjamini–Hochberg. |
| peeking | inflates the false positive rate | Stopping at the first p < 0.05 selects the luckiest moment of many. | Use a fixed horizon, or α-spending / always-valid sequences. |

## Multiple Choice Questions

**Q1.** A study reports p = 0.03 against the null hypothesis "the treatment has no
effect". What does that number mean?

- A) There is a 3% chance the null hypothesis is true
- B) If the null were true, data at least this extreme would occur 3% of the time
- C) There is a 97% chance the treatment works
- D) The treatment is 3% effective

<details>
<summary>Answer and explanation</summary>

**B) If the null were true, data at least this extreme would occur 3% of the time.**

This is the definition, and Mistake 1 in this lesson is exactly option A. Option C
is the complement read as a posterior, which needs a prior: with prior 0.001 and
80% power the true figure is **1.58%**, as Example C computes. Option D conflates
a p-value with an effect size, which are entirely different quantities.

</details>

**Q2.** In the drug example, 0.1% of candidate treatments work, a study has 80%
power and a 5% false alarm rate, and it reports p < 0.05. What is the
probability the treatment actually works?

- A) 95%, because the result was significant at α = 0.05
- B) About 1.6%, because the false positives come from a population 999× larger
- C) About 50%, since power is 80%
- D) About 0.1%, since that is the prior

<details>
<summary>Answer and explanation</summary>

**B) About 1.6%, because the false positives come from a population 999× larger.**

Bayes: `P(W | sig) = 0.80 × 0.001 / (0.80 × 0.001 + 0.05 × 0.999) =
0.0008/0.05075 = 0.0158`. Option A is the p-value read as a posterior.
Option C averages the two rates, which is not what Bayes does. Option D is the
prior itself — the right magnitude by coincidence, but the posterior is 16×
larger than the prior here, so the answer would change with the prior.

</details>

**Q3.** A redesign test gives p = 0.4. What is the honest conclusion?

- A) The redesign has no effect
- B) The experiment failed to detect an effect; report the confidence interval, and if it is wide, say the test was underpowered
- C) The redesign made things worse
- D) Run it again with α = 0.5 and re-check

<details>
<summary>Answer and explanation</summary>

**B) The experiment failed to detect an effect; report the confidence interval, and
if it is wide, say the test was underpowered.**

Mistake 3 in this lesson. Example B shows a p of 0.8742 with a 0.33-point
observed difference — 0.16 standard errors, and a minimum detectable effect of 5.9
points. Option A is the error; p = 0.4 is compatible with a range of effects
including zero and including harmful ones. Option C over-reads in the other
direction. Option D is p-hacking by another name — lowering α after seeing data
guarantees significance without evidence.

</details>

**Q4.** Why must the standard error of a two-proportion difference use the
*pooled* rate?

- A) Because the pooled rate is a better estimate of the true rate
- B) Because the SE must be computed **under the null hypothesis** the test assumes, and the null says the two rates are equal
- C) Because pooling always reduces variance
- D) It does not matter which rate is used

<details>
<summary>Answer and explanation</summary>

**B) Because the SE must be computed **under the null hypothesis** the test assumes,
and the null says the two rates are equal.**

The denominator of a z-statistic is the standard error of the test statistic
*under the null*, so the correct variance is the null's. Option A is a
statement about estimation, which is a different problem. Option C is false:
pooling often *raises* the estimated variance when the two arms differ, which is
precisely why Mistake 5 says using the wrong variance "usually makes effects look
more significant". Option D is false; the two give different z and different
p-values.

</details>

**Q5.** You run 20 metrics and report the one with the smallest p-value. What is
your effective false positive rate?

- A) 0.05, because each test was run at α = 0.05
- B) `1 − 0.95²⁰ ≈ 0.642`, about 64%
- C) 0.0025, the multiple-comparison correction
- D) 1.0, because at least one will be significant

<details>
<summary>Answer and explanation</summary>

**B) `1 − 0.95²⁰ ≈ 0.642`, about 64%.**

Mistake 2 in this lesson. Under the global null all 20 p-values are independent
uniforms, so the probability that at least one falls below 0.05 is exactly that.
Option A is the belief the error depends on. Option C is roughly $m\alpha^2$,
which is not the right correction — Bonferroni uses $\alpha/m$, i.e. 0.0025 here
— and it does not apply to "pick the smallest". Option D is the limiting case, and
it is a reminder that with enough comparisons significance is guaranteed.

</details>

**Q6.** Two estimators of the same parameter have MSE 0.010 (unbiased) and 0.029
(biased). Which should you use, and why?

- A) The biased one, because its variance is smaller
- B) The unbiased one, because MSE = Var + Bias² is what you actually care about and it is lower
- C) It depends on which has the smaller variance
- D) Neither — you must use the MLE by definition

<details>
<summary>Answer and explanation</summary>

**B) The unbiased one, because MSE = Var + Bias² is what you actually care about
and it is lower.**

Exercise 2 works these numbers out: at $n = 20$, $\hat p_1$ has variance 0.0105
and zero bias, while $\hat p_2 = k/(n-5)$ has variance 0.0187 and bias $+0.1$,
so its MSE is 0.0287 — nearly three times worse. Option A is exactly the
one-sided view of the trade-off: variance alone ignores systematic error.
Option C can pick the wrong estimator — the biased one here has *higher* variance
as well, but the general principle stands. Option D is false; the MLE is a
default, not an obligation, and it can lose on MSE.

</details>

**Q7.** What is the power of the Exercise 3 experiment against the 0.2-point
effect it observed?

- A) About 13%, so it had roughly a 1-in-8 chance of detecting what it saw
- B) 50%, since it is halfway between 0 and 1
- C) 95%, since that is the confidence level
- D) About 98.7%, which is the power against a 1-point effect

<details>
<summary>Answer and explanation</summary>

**A) About 13%, so it had roughly a 1-in-8 chance of detecting what it saw.**

`power ≈ Φ(0.002/0.0023933 − 1.96) = Φ(−1.1243) = 0.1304`. Option B is a guess.
Option C confuses the confidence level with power, which measure different things:
confidence is about the interval procedure, power about detection. Option D is the
power against a *different* effect, quoted out of context — against a 1-point
effect the power really is 0.9867, which is what makes the design's mis-sizing so
clear.

</details>

**Q8.** A p-value is 0.04. Which of these is a legitimate reading?

- A) The null hypothesis is 4% likely to be true
- B) The data would be this extreme or more 4% of the time if the null were true
- C) There is a 96% chance the alternative is true
- D) The effect size is 4%

<details>
<summary>Answer and explanation</summary>

**B) The data would be this extreme or more 4% of the time if the null were true.**

Options A and C are the two directional errors — treating the p-value as
$P(H_0 \mid \text{data})$ or as $P(H_1 \mid \text{data})$, neither of which it is.
Option D confuses the p-value with an effect size; the two are unrelated, and a
significant result can have a negligible effect while a large effect can be
non-significant in a small sample.

</details>

**Q9.** A 95% confidence interval of [3.1%, 4.9%] for a conversion rate. Which
statement is correct?

- A) There is a 95% probability the true rate is in this range
- B) Repeated many times, about 95% of intervals built this way would contain the fixed true rate; this particular interval either covers or it does not
- C) 95% of users convert at a rate in this range
- D) The true rate is most likely 4%

<details>
<summary>Answer and explanation</summary>

**B) Repeated many times, about 95% of intervals built this way would contain the
fixed true rate; this particular interval either covers or it does not.**

Mistake 5 in this lesson, and the base-rate fallacy of
[Lesson 62](../part05_probability_statistics/62_conditional_probability_and_bayes.md) applied to a frequentist
object: the parameter is fixed, so it does not "have a probability" of lying
somewhere. Option C confuses the parameter with individuals. Option D is a
frequentist non-sequitur; without a prior, no value inside the interval is more
likely than another.

</details>

**Q10.** You stop an A/B test the first day the p-value dips below 0.05. What
have you done?

- A) Saved time with no cost
- B) Inflated your false positive rate, because you selected the luckiest of many looks at the data
- C) Made the test more rigorous
- D) Reduced the Type II error

<details>
<summary>Answer and explanation</summary>

**B) Inflated your false positive rate, because you selected the luckiest of many
looks at the data.**

This is Mistake 4 in this lesson. The mechanism is selection: each daily look is a
fresh test, and stopping at the first success means you condition on the minimum of
many p-values, which is biased small. Option A is the intuition behind the mistake
— stopping early *does* save time, but it is not free. Option C inverts the effect
entirely. Option D is wrong in direction: peeking does not reduce the missed-effect
rate for the data you already have, it just makes the reported result optimistic.

</details>

## Subjective Questions

### Short Answer

**Q1. Define the MLE and state the formula for Bernoulli data.**

<details>
<summary>Answer</summary>

$\hat\theta_{\text{MLE}} = \arg\max_\theta L(\theta)$ where
$L(\theta) = P(\text{data} \mid \theta)$ — the parameter value that makes the
observed data least surprising. For $k$ successes in $n$ Bernoulli trials,
$L(p) = p^k(1-p)^{n-k}$, so
$\ell'(p) = k/p - (n-k)/(1-p) = 0$ gives $k(1-p) = p(n-k)$, hence
$p = k/n$. The second derivative is negative, so it is a unique maximum when
$0 < k < n$. Note $L$ is $P(\text{data} \mid \theta)$, never
$P(\theta \mid \text{data})$.

</details>

**Q2.** State the bias–variance decomposition for an estimator's mean squared
error, and say what each term is.

<details>
<summary>Answer</summary>

$\mathrm{MSE}(T) = E[(T-\theta)^2] = \mathrm{Var}(T) + \mathrm{Bias}(T)^2$ with
$\mathrm{Bias}(T) = E[T] - \theta$. The first term is the estimator's noise — how
much it wobbles across repeated samples of the same size. The second is its
systematic error — where it sits on average, away from the truth, no matter how
much data you have. You minimise MSE, not variance alone, so it is legitimate to
accept a little bias for a lot less variance.

</details>

**Q3.** Give the two-proportion z-statistic and say what the denominator is.

<details>
<summary>Answer</summary>

$z = (\hat p_1 - \hat p_2)/\mathrm{SE}$ with
$\bar p = (k_1+k_2)/(n_1+n_2)$ and
$\mathrm{SE} = \sqrt{\bar p(1-\bar p)(1/n_1 + 1/n_2)}$. The denominator is the
standard error of the difference **under the null** $H_0: p_1 = p_2$, which is
why the rate is *pooled*: the null says the two rates are equal, so the variance
must be evaluated at that common value. Under the null, $z$ is approximately
standard normal, which is what makes the p-value computable.

</details>

**Q4.** Define Type I error, Type II error, and power, and state which one you
choose before running an experiment.

<details>
<summary>Answer</summary>

Type I: rejecting $H_0$ when it is true, with probability $\alpha$ — the false
alarm rate. Type II: failing to reject when $H_0$ is false, with probability
$\beta$ — the missed-effect rate. Power is $1-\beta$, the probability of detecting
an effect that is really there. **α** is the one you fix in advance, precisely so
that the false alarm rate is controlled; power is what you then check, because it
depends on the effect size, $n$, and α.

</details>

**Q5.** Give the sample-size formula for a two-sided two-proportion test, and the
values of the two z's at α = 0.05 and 80% power.

<details>
<summary>Answer</summary>

$n = 2\bar p(1-\bar p)(z_{1-\alpha/2} + z_{1-\beta})^2/\delta^2$ per arm, where
$\delta = p_2 - p_1$ and $\bar p$ is the pooled baseline. At α = 0.05,
$z_{1-\alpha/2} = 1.959964$; at 80% power, $z_{1-\beta} = 0.841621$. So the
constant is $(1.96 + 0.8416)^2 = 7.8572$. For a 6% baseline and a 1-point effect
this gives 8,991 users per arm.

</details>

**Q6.** State the p-value definition, and state precisely what it is *not*.

<details>
<summary>Answer</summary>

$p = P(\lvert Z\rvert \ge \lvert z_{\text{obs}}\rvert)$, evaluated **under the null
hypothesis**. It is not $P(H_0 \mid \text{data})$, not
$P(H_1 \mid \text{data})$, and not an effect size. It is a statement about the
data: how surprising this outcome would be *if the null were true*. The
conclusion it licenses is narrow — *if the null were true, data this extreme would
be unusual* — and nothing more without a prior.

</details>

### Long Answer

**Q1. Why does a p-value of 0.05 not mean there is a 5% chance the null hypothesis
is true?**

<details>
<summary>Model answer</summary>

Because a p-value and the probability of a hypothesis are computed from
*different conditionals*. The p-value is $P(\text{data} \mid H_0)$ — the
probability of the data, given the hypothesis. The thing people want is
$P(H_0 \mid \text{data})$ — the probability of the hypothesis, given the data.
Bayes' theorem relates them, and the two are equal only when the marginals happen
to coincide, which they generally do not:

$$P(H_0 \mid \text{data}) = \frac{P(\text{data}\mid H_0)P(H_0)}{P(\text{data})} = \frac{\text{p-value} \cdot \pi}{\pi + (1-\pi)\cdot r}$$

with $\pi$ the prior and $r$ the probability of this data under the alternative.
The p-value is the *numerator* of that fraction. Reporting it as the answer drops
the prior and the alternative likelihood entirely.

Example C puts numbers on the damage. Take $\pi = 0.001$, 80% power, and
$\alpha = 0.05$. Then $P(\text{works} \mid \text{sig}) = 0.0008/0.05075 =
0.0158$ — about 1.6%, not 95%. The reason is a base-rate effect straight out of
[Lesson 62](../part05_probability_statistics/62_conditional_probability_and_bayes.md): the pool of ineffective
treatments is 999× larger, so even a 5% false alarm rate produces 999 false
positives for every 80 true ones.

Note also that the error runs one way only in practice. A p-value of 0.05 is at
least *evidence against* the null, so treating it as "5% chance the null is true"
understates the evidence. Treating it as "95% chance the alternative is true"
overstates it, and that is the direction that actually causes harm — teams shipping
changes that the experiment could never have resolved.

The fix is procedural: report the p-value as a p-value, and if a posterior is what
you need, do the Bayes computation explicitly with a stated prior. Do not convert
one into the other by arithmetic identity.

</details>

**Q2. Why must α be fixed before the experiment, and what goes wrong when it is
not?**

<details>
<summary>Model answer</summary>

Because α is a statement about the *procedure's* long-run false alarm rate, and
that claim only holds if the rule was committed to in advance. Once you have seen
the data, the number you compute is conditional on those data, and the guarantee
is gone. This is the same structure as the confidence interval: the parameter is
fixed and the statistic is random, so the only claim available is about
repeated applications of the procedure.

Three failure modes follow, and the lesson covers each. **Threshold shopping:** a
PM who tests CTR against 5%, then 5.5%, then 6%, is guaranteed to find one that
rejects — Exercise 1(d) shows all six candidates and an effective false positive
rate of about 26%. **Multiple comparisons:** running 20 metrics and reporting the
best gives `1 − 0.95²⁰ = 0.642`, a 64% false positive rate, not 5%.
**Peeking:** stopping the first day p dips below 0.05 selects the minimum of many
p-values, which is biased small. All three are the same error — choosing the
hypothesis or the stopping time after looking — and all three make the reported
p-value optimistic by an amount you cannot easily compute.

The remedies are all about moving the decision before the data. Pre-register the
primary metric, the null, the sample size, and the horizon. If you need multiple
comparisons, correct for them (Benjamini–Hochberg for discovery, Bonferroni for
family-wise control). If you need to monitor continuously, use a sequential test
with α-spending or an always-valid confidence sequence, which accounts for the
number of looks rather than pretending there was one.

</details>

**Q3. Why does a non-significant result tell you nothing, and what is the honest
way to report it?**

<details>
<summary>Model answer</summary>

Because "not significant" is a statement about your ability to detect an effect,
not about the effect's existence. Failing to reject H₀ happens for two very
different reasons: there is no effect, or there is an effect your sample was too
small to resolve. The test's output does not distinguish them, and Example B makes
the point concretely — a p-value of 0.8742 with a minimum detectable effect of 5.9
percentage points, on a redesign that might well have helped by 2.

The honest report is the **confidence interval**, because it says how much you
*could* have resolved. In Exercise 3 the interval on the difference is
[−0.27, +0.67] percentage points, which is far more informative than "p = 0.40":
it says the redesign may be slightly harmful, is probably slightly helpful, and
neither end is excluded. The gap between 0 and the effect you care about is the
part of the space your experiment failed to explore.

This matters because "not significant" invites a false dichotomy: teams read it
as "no difference", ship the redesign on that basis, and never learn that they
could not have detected a regression either. The same run reports power of 13%
against the effect actually observed — a 1-in-8 chance of detecting it — so the
experiment was never capable of answering the question being asked of it.

Two practical habits follow. **Report power and the minimum detectable effect
alongside the p-value**, so a non-significant result is read as underpowered rather
than as null. And pre-compute the required sample size before running, since
n scales as $1/\delta^2$: the 0.2-point effect in Exercise 3 would need 224,787
users per arm, and finding that out beforehand is much cheaper than finding it out
afterwards.

</details>

**Q4. Why does the base rate dominate every p-value-based conclusion, and how
much can good methodology fix it?**

<details>
<summary>Model answer</summary>

Because the p-value conditions on the null, so it discards the one number that
matters most for a posterior — how common the hypothesis is. When the base rate
is small, the pool of null cases is enormous, and a fixed false alarm rate
generates more false positives than a high power generates true positives. In the
drug example, 80% power against 0.1% prevalence yields 0.0008 true positives per
trial while 5% false alarm against 99.9% yields 0.04995 false positives: a ratio
of 62 to 1, which caps the posterior at 1.6% no matter how good the science.

Two levers move it. **Raise power**, which helps but is bounded: at power 0.99
the posterior only reaches about 3.9%, because the false-positive pool is
unaffected. **Lower α**, which is much stronger but has a cost — you reject fewer
true effects. And the decisive lever is **the prior**, which no amount of
methodology supplies: for the same 80% power and α = 0.05, a prior of 0.2 gives a
posterior of 0.79 rather than 0.016.

This is why serious work in medicine and platform engineering runs *sequential*
analyses with pre-declared stopping rules, or requires independent replication,
rather than reading a single p-value. A pre-declared rule accumulates evidence in
one direction, so the base rate is faced once with a large posterior rather than
repeatedly with small ones — and a replication is a second prior-scale
observation rather than another coin flip.

The practical takeaway is that the p-value answers "is this data surprising under
the null?", which is a real question worth asking, and nothing more. The decision
question — should I ship, should I treat — is a posterior question, and it needs a
prior you state out loud.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — compute an MLE and its confidence interval.** A search returns
results for 1,500 queries. 87 of them produce a click (a successful search).

(a) Compute the MLE of the click-through rate. (b) Compute its standard error and
a 95% confidence interval. (c) A PM asks "is our CTR above 5%?" Write the
hypothesis test and compute the p-value, given that the null is CTR = 0.05.
(d) What would the p-value be if you tested against 5% *after* seeing that the MLE
is 5.8%, and why is that a problem?

<details>
<summary>Solution</summary>

(a) MLE = k/n = 87/1500 = **0.058**, i.e. 5.8%.

(b) SE = √(p̂(1−p̂)/n) = √(0.058 × 0.942 / 1500) = √(3.6432e-5) = 0.0060360.
95% CI: 0.058 ± 1.96(0.0060360) = 0.058 ± 0.011831, so
**[0.04617, 0.06983]**.

(c) H₀: p = 0.05 versus H₁: p > 0.05, one-sided.
z = (0.058 − 0.05)/0.0060360 = 0.008/0.0060360 = **1.3254**.
p-value (one-sided) = P(Z ≥ 1.3254) = 1 − Φ(1.3254) = **0.0925**.

So at α = 0.05 we fail to reject: 0.0925 > 0.05. A PM wanting to claim "we beat
5%" cannot from this data alone — the point estimate is higher, but not
significantly so. Note the temptation to switch to the two-sided test, which
would give p ≈ 0.185 and make it worse; the test was specified correctly.

(d) If the null is chosen *after* seeing the MLE, the threshold is
guaranteed to be beaten and the p-value is meaningless — you have fitted the
hypothesis to the data. It is the "researcher degrees of freedom" problem: if you
try CTR = 5%, 5.5%, 6%, 7%, 9%, and 12% until one gives p < 0.05, your effective
false positive rate is roughly 5% per try, so across six tries it is about 26%.

The correct discipline: fix the null from domain knowledge *before* collecting
data, and if you genuinely need to explore, split the data into an exploratory
set and a confirmatory set.

```python
from math import erf, sqrt


def cdf(z):
    return 0.5 * (1 + erf(z / sqrt(2)))


K, N = 87, 1500
p_hat = K / N
se = (p_hat * (1 - p_hat) / N) ** 0.5

print(f"(a) MLE = k/n = {K}/{N} = {p_hat:.6f}  ({p_hat*100:.2f}%)")
print(f"(b) SE  = {se:.7f}")
print(f"    95% CI = [{p_hat - 1.96*se:.5f}, {p_hat + 1.96*se:.5f}]")
print(f"    width  = {2 * 1.96 * se:.5f}")

p0 = 0.05
z = (p_hat - p0) / se
p_one = 1 - cdf(z)
p_two = 2 * (1 - cdf(abs(z)))
print()
print(f"(c) H0: CTR = {p0}, z = {z:.4f}")
print(f"    p-value one-sided (>)   = {p_one:.4f}")
print(f"    p-value two-sided       = {p_two:.4f}")
print(f"    reject at 0.05? {p_one < 0.05}")

print()
print("(d) searching for a null that gives p < 0.05:")
trials = []
for cand in (0.05, 0.055, 0.06, 0.07, 0.09, 0.12):
    zz = (p_hat - cand) / se
    ppp = 1 - cdf(zz)
    trials.append(ppp < 0.05)
    print(f"    test vs {cand:.3f}: p = {ppp:.4f}  {'<- would declare success' if ppp < 0.05 else ''}")
from math import prod
any_success = 1 - prod(1 - 0.05 for _ in trials)
print(f"    probability of at least one false positive across 6 tries: "
      f"{any_success:.4f}")
```

</details>

**[ ] Exercise 2 — MLE versus a biased estimator, measured.** Suppose you observe
k successes in n trials, with true p = 0.3. Consider two estimators:

- p̂₁ = k/n (the MLE)
- p̂₂ = k/(n − 5), which ignores the first 5 observations

(a) For n = 20 and n = 200, compute the expected value and variance of each
analytically. (b) Which is unbiased? (c) Simulate both at n = 20 and report the
empirical bias and variance. (d) Which estimator would you use, and why does the
answer change with n?

<details>
<summary>Solution</summary>

(a) Analytically. Write k ~ Binomial(n, p), E[k] = np, Var(k) = np(1−p).

For p̂₁ = k/n: E[p̂₁] = np/n = p = 0.3 ✓ unbiased.
Var(p̂₁) = np(1−p)/n² = p(1−p)/n = 0.21/n.
  - n = 20: Var = 0.0105
  - n = 200: Var = 0.00105

For p̂₂ = k/(n−5): E[p̂₂] = np/(n−5) = p·n/(n−5), which exceeds p whenever n/(n−5)
> 1. The bias is p·5/(n−5).
  - n = 20: E = 0.3(20/15) = 0.4, so bias = **+0.1**
  - n = 200: E = 0.3(200/195) = 0.30769, so bias = **+0.00769**

Var(p̂₂) = np(1−p)/(n−5)² = 0.21n/(n−5)².
  - n = 20: 0.21(20)/225 = 0.018667
  - n = 200: 0.21(200)/38025 = 0.0011046

(b) Only p̂₁ is unbiased. p̂₂ is biased upward because dividing by a smaller
number inflates the estimate: throwing away five observations makes the rate
*larger*, not smaller, whenever the true rate is being estimated as k/n. This is
a genuinely counter-intuitive direction and worth remembering — discarding data
here inflates the estimate.

(c) Simulation at n = 20 should give bias ≈ 0 for p̂₁ and ≈ +0.1 for p̂₂, with the
variances matching the analytic values above.

(d) At n = 20, MSE(p̂₁) = 0.0105 + 0 = 0.0105, while
MSE(p̂₂) = 0.018667 + 0.01 = 0.028667. The MLE wins decisively — its bias is zero
and its variance is lower too.

At n = 200: MSE(p̂₁) = 0.00105, MSE(p̂₂) = 0.0011046 + 0.0000591 = 0.0011637.
The MLE still wins, but the gap has narrowed to about 11%.

The general lesson: **bias that shrinks with n is harmless; bias that does not
shrink is fatal.** At n = 200, p̂₂'s bias of 0.0077 is comparable to its standard
error of 0.0332, so it is not even detectable — but it is still there, and it
would persist at n = 10,000 with a bias of 0.00015 that is still real. The MLE
never has this problem.

```python
import random

P_TRUE = 0.3


def analytic(k_div, n):
    """Mean, bias and variance of k/(n - k_div) for k ~ Binomial(n, p)."""
    denom = n - k_div
    mean = P_TRUE * n / denom
    bias = mean - P_TRUE
    var = P_TRUE * (1 - P_TRUE) * n / denom**2
    mse = var + bias**2
    return mean, bias, var, mse


print("(a) analytic")
print(f"{'n':>6} {'estimator':>10} {'mean':>9} {'bias':>9} "
      f"{'variance':>10} {'MSE':>10}")
for n in (20, 200):
    for label, div in (("p1 = k/n", 0), ("p2 = k/(n-5)", 5)):
        mean, bias, var, mse = analytic(div, n)
        print(f"{n:6d} {label:>13} {mean:9.5f} {bias:+9.5f} "
              f"{var:10.6f} {mse:10.6f}")

print()
print("(b) p1 is unbiased; p2 has bias = p*5/(n-5) > 0 always.")
print("    NOTE the direction: DISCARDING data inflates the rate, because")
print("    you divide a numerator by a smaller denominator.")

print()
print("(c) simulation, 20,000 replications per n")
TRIALS = 20_000
rng = random.Random(777)
for n in (20, 200):
    s1 = s1sq = s2 = s2sq = 0.0
    for _ in range(TRIALS):
        # k ~ Binomial(n, P_TRUE). Small n is drawn exactly; large n uses the
        # normal approximation, which at n = 200 is accurate to well under a
        # count and makes 20,000 replications instantaneous.
        if n <= 200:
            k = sum(1 for _ in range(n) if rng.random() < P_TRUE)
        else:
            k = int(round(rng.gauss(n * P_TRUE,
                                    (n * P_TRUE * (1 - P_TRUE)) ** 0.5)))
            k = min(n, max(0, k))
        p1 = k / n
        p2 = k / (n - 5)
        s1 += p1; s1sq += p1 * p1
        s2 += p2; s2sq += p2 * p2
    e1, e2 = s1 / TRIALS, s2 / TRIALS
    v1 = s1sq / TRIALS - e1**2
    v2 = s2sq / TRIALS - e2**2
    print(f"  n={n:3d}  p1: mean {e1:.5f} bias {e1-P_TRUE:+.5f} var {v1:.6f}")
    print(f"        p2: mean {e2:.5f} bias {e2-P_TRUE:+.5f} var {v2:.6f}")

print()
print("(d) MSE comparison (analytic):")
for n in (20, 200):
    _, _, _, mse1 = analytic(0, n)
    _, _, _, mse2 = analytic(5, n)
    winner = "MLE" if mse1 < mse2 else "biased"
    print(f"  n={n:3d}: MLE {mse1:.6f} vs p2 {mse2:.6f}  -> {winner} "
          f"by {mse2/mse1:.2f}x")
print()
print("The MLE wins at both sizes, but note the bias of p2 shrinks as")
print("5p/(n-5) -> 0 while never vanishing. MSE = Var + Bias^2 is the")
print("organising formula for this whole comparison.")
```

</details>

**[ ] Exercise 3 — Challenge: run an A/B test properly, and design the next
one.** Control: 1,200 conversions from 20,000 users (6.0%). Variant: 1,240 from
20,000 (6.2%).

(a) Run the two-proportion z-test. Report the p-value, the confidence interval on
the difference, and the decision. (b) A colleague says "ship it, we saw a lift".
Give the strongest honest objection. (c) Compute the power of this experiment to
detect the observed 0.2 percentage-point effect, and to detect 1 point. (d) Using
the formula from [Lesson 68](../part05_probability_statistics/68_law_of_large_numbers_and_clt.md), compute how many
users per arm would be needed to detect 1 percentage point at 80% power and 5%
significance. (e) Give one recommendation about the *next* experiment that is not
"get more users".

<details>
<summary>Solution</summary>

(a) p̂_A = 0.060, p̂_B = 0.062, difference = +0.002.
Pooled p̄ = (1200 + 1240)/40000 = 2440/40000 = 0.061.
SE = √(0.061 × 0.939 × (2/20000)) = √(0.057279 × 1e-4) = 0.0023933.
z = 0.002/0.0023933 = **0.8357**.
p-value (two-sided) = 2(1 − Φ(0.8357)) = **0.4033**.
95% CI on the difference: 0.002 ± 1.96(0.0023933) = 0.002 ± 0.004691, so
**[−0.00269, +0.00669]**, i.e. −0.27 to +0.67 percentage points.

Decision: fail to reject H₀. The CI contains 0, the same conclusion, as it must.

(b) The strongest objection is that **the experiment cannot distinguish the
observed effect from zero, and it certainly cannot rule out a meaningful harm.**
The interval extends to −0.27 points, so a 0.27-point *degradation* is fully
consistent with this data. Shipping on a non-significant result is not "a small
win"; it is a coin flip that happened to land positive. The honest summary is "no
evidence of an effect, with a range that includes mild harm."

(c) Power calculations. For a two-sided test at α = 0.05 (z_{α/2} = 1.96), power
against effect δ with standard error SE is

    power = P(Z > 1.96 − δ/SE) + P(Z < −1.96 − δ/SE) ≈ Φ(δ/SE − 1.96)

- δ = 0.002: δ/SE = 0.002/0.0023933 = 0.8357. Φ(0.8357 − 1.96) = Φ(−1.1243) =
  0.1305. Power ≈ **13.1%**.
- δ = 0.010: δ/SE = 0.010/0.0023933 = 4.178. Φ(4.178 − 1.96) = Φ(2.218) =
  0.9867. Power ≈ **98.7%**.

So this experiment had about a 1-in-8 chance of detecting the effect it actually
observed, and would easily have detected a full point. The design was aimed at
the wrong effect size.

(d) With p̄ = 0.061 and δ = 0.01,

    n = 2 × 0.061 × 0.939 × (1.96 + 0.8416)² / 0.01²
      = 2(0.057279)(7.85718) / 0.0001
      = 0.900206 / 0.0001
      = **8,991 users per arm**

That is *fewer* than the 20,000 already run — so the current experiment was
already adequately powered for a 1-point effect. It was simply aimed at detecting
0.2 points, which needs (0.01/0.002)² = 25× more data: **224,787 per arm**.

(e) Three options that do not involve simply adding users:

1. **Aggregate over longer time or more surface area.** Run the same comparison on
   a longer window or across several similar pages. Traffic is the binding
   constraint, and the same conversion logic can be validated in places with more
   volume.
2. **Reduce noise per observation with CUPED.** Using a pre-experiment metric
   (previous session's conversion, or historical revenue) as a covariate removes
   variance shared between arms. In practice this routinely cuts required n by
   30–50%, which at these numbers is worth more than doubling the sample.
3. **Change the primary metric to a higher-signal one.** Binary conversion is a
   noisy metric: at a 6% baseline, 20,000 users yields only about 1,200 events.
   Revenue per user or a compound metric carries far more signal per observation,
   so the same traffic resolves smaller effects. This also changes what you are
   optimising, so it must be a deliberate decision, not a statistical trick.

The honest overarching recommendation: decide the smallest effect that would
actually change your decision, size the experiment for it, and run it before
launching — not after.

```python
from math import erf, sqrt


def cdf(z):
    return 0.5 * (1 + erf(z / sqrt(2)))


def zq(q):
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if cdf(mid) < q:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def ab(ca, na, cb, nb, alpha=0.05):
    pa, pb = ca / na, cb / nb
    pool = (ca + cb) / (na + nb)
    se = (pool * (1 - pool) * (1 / na + 1 / nb)) ** 0.5
    diff = pb - pa
    z = diff / se
    margin = zq(1 - alpha / 2) * se
    return {
        "pa": pa, "pb": pb, "diff": diff, "se": se, "z": z,
        "p": 2 * (1 - cdf(abs(z))),
        "ci": (diff - margin, diff + margin),
    }


CA, NA, CB, NB = 1200, 20000, 1240, 20000
r = ab(CA, NA, CB, NB)

print(f"(a) control {r['pa']*100:.2f}%  variant {r['pb']*100:.2f}%  "
      f"diff {r['diff']*100:+.3f} pp")
print(f"    SE = {r['se']:.7f}   z = {r['z']:.4f}   p = {r['p']:.4f}")
print(f"    95% CI = [{r['ci'][0]*100:+.3f}, {r['ci'][1]*100:+.3f}] pp")
print(f"    decision: {'REJECT' if r['p'] < 0.05 else 'FAIL TO REJECT'} H0")

print()
print("(b) the CI reaches "
      f"{r['ci'][0]*100:+.3f} pp, so a real degradation is not excluded.")

print()
print("(c) power of THIS design")
for delta in (0.002, 0.005, 0.010):
    power = cdf(delta / r["se"] - zq(0.975))
    print(f"    delta = {delta*100:5.2f} pp:  delta/SE = {delta/r['se']:.3f}"
          f"   power = {power:.4f}")

print()
print("(d) n per arm for a 1 pp effect at 80% power, alpha = 0.05")
z_a, z_b = zq(0.975), zq(0.80)
pool = (CA + CB) / (NA + NB)
delta = 0.01
n_needed = int(2 * pool * (1 - pool) * (z_a + z_b) ** 2 / delta**2)
n_small = int(2 * pool * (1 - pool) * (z_a + z_b) ** 2 / 0.002**2)
print(f"    n = {n_needed:,} users per arm   (we already had {NA:,})")
print(f"    n for the 0.2 pp effect actually seen: {n_small:,} per arm")
print()
print("(e) the answer is not more users: aggregate over more surface,")
print("    apply CUPED-style variance reduction, or switch to a")
print("    higher-signal primary metric such as revenue per user.")
```

Note the last computation: detecting a 0.2-point effect needs about **224,787 per
arm**, which is 11× the traffic already spent. That is the number that should
stop a team from shipping on a non-significant result — the experiment that was
run could not have answered the question it was implicitly being asked.

</details>

**[ ] Exercise 4 — interpreting a p-value and a confidence interval correctly.**
An experiment tests a checkout redesign. Control: 480 conversions from 8,000
users. Variant: 522 from 8,000. The reported p-value is **0.048** and the
headline reads "redesign improves conversion".

(a) Compute the two rates, their difference, and the pooled estimate.
(b) Compute the standard error, the z statistic, and the p-value yourself, and
confirm the CI on the difference.
(c) Interpret the p-value correctly in one sentence, and state three things it
does **not** say.
(d) Interpret the confidence interval correctly in one sentence, and say whether
the interval excludes a *harmful* effect.
(e) A second analyst writes "there is a 4.8% chance the redesign does not work".
Correct them, and compute what the probability actually is under a stated prior.

<details>
<summary>Solution</summary>

(a) $\hat p_A = 480/8000 = 0.0600$, $\hat p_B = 522/8000 = 0.06525$. Difference
$= +0.00525$, i.e. **+0.525 percentage points**. Pooled under the null:
$\bar p = (480+522)/16000 = 1002/16000 = 0.062625$.

(b) $\mathrm{SE} = \sqrt{0.062625 \times 0.937375 \times (2/8000)}
= \sqrt{0.0586964 \times 2.5\times10^{-4}} = \sqrt{1.46741\times10^{-5}}
= 0.0038309$.

$z = 0.00525/0.0038309 = 1.3704$.
$p = 2(1-\Phi(1.3704)) = 2 \times 0.0853 = \mathbf{0.1706}$.

Note this is **not** 0.048 — the reported figure does not reproduce. The CI on the
difference is $0.00525 \pm 1.96 \times 0.0038309 = 0.00525 \pm 0.007508$, so
**[−0.00226, +0.01276]**, i.e. −0.23 to +1.28 percentage points. That interval
contains 0, which agrees with the p-value I computed and contradicts the
headline.

(c) **Correct interpretation:** if the redesign had no effect, data at least this
far from equal conversion would occur about 17% of the time. Three things it does
**not** say: that there is a 17% chance the null is true; that there is an 83%
chance the redesign works; and anything about the size of the effect.

(d) **Correct interpretation:** if this whole procedure were repeated many times,
about 95% of intervals built this way would contain the fixed true difference;
this particular interval either covers the truth or it does not. And note the
lower end: at −0.23 points the interval does **not** exclude a mild harmful
effect, so "improves conversion" is not something this data supports even at a
conventional level.

(e) The analyst's sentence is Mistake 1 in this lesson: it reports
$P(\text{data} \mid H_0)$ as if it were $P(H_0 \mid \text{data})$. To get the
posterior you need a prior. Take the (generous, favourable) prior that the
redesign is a 50/50 coin flip: the power at the observed 0.525-point effect is
only $0.2777$, and with $\alpha = 0.05$,

$$P(\text{works} \mid \text{sig}) = \frac{0.2777 \times 0.5}{0.2777 \times 0.5 + 0.05 \times 0.5} = \frac{0.13885}{0.16385} = 0.8474.$$

So with an even-handed prior the probability is about **85%**, not 4.8%. If the
prior were 0.1 instead: $0.02777/(0.02777 + 0.045) = 0.382$. The lesson's point
is that the posterior is a function of the prior *and* the data, and quoting
either alone is misleading — which is why the correct sentence reports the
p-value as a p-value.

```python
from math import erf, sqrt


def cdf(z):
    return 0.5 * (1 + erf(z / sqrt(2)))


KA, NA, KB, NB = 480, 8_000, 522, 8_000
ALPHA = 0.05

p_a, p_b = KA / NA, KB / NB
diff = p_b - p_a
pool = (KA + KB) / (NA + NB)
se = (pool * (1 - pool) * (1 / NA + 1 / NB)) ** 0.5
z = diff / se
p_value = 2 * (1 - cdf(abs(z)))
margin = 1.96 * se

print(f"(a) control {p_a * 100:.3f}%  variant {p_b * 100:.3f}%  "
      f"diff {diff * 100:+.3f} pp")
print(f"    pooled p = {pool:.6f}")
print()
print(f"(b) SE = {se:.7f}, z = {z:.4f}, p-value = {p_value:.4f}")
print(f"    REPORTED p-value was 0.0480 -- does not reproduce: "
      f"{p_value:.4f}")
print(f"    95% CI on the difference = "
      f"[{(diff - margin) * 100:+.3f}, {(diff + margin) * 100:+.3f}] pp")
print(f"    contains 0: {diff - margin < 0 < diff + margin}")
print()
print("(c) correct: under H0, data this extreme occurs ~"
      f"{p_value * 100:.1f}% of the time.")
print("    NOT: P(H0|data)=17%; NOT P(H1|data)=83%; NOT an effect size.")
print()
print(f"(d) correct: the interval is one draw from a procedure covering 95%")
print(f"    of repeats. Lower end {(diff - margin) * 100:+.3f} pp does NOT")
print("    exclude a mild harmful effect, so 'improves conversion' is not")
print("    supported.")
print()

# Power at the observed effect, for the posterior computation in (e).
power = cdf(abs(z) - 1.96)
print(f"    power at the observed {diff * 100:.3f} pp effect = {power:.4f}")


def posterior_given_significant(prior, power, alpha=ALPHA):
    return (power * prior) / (power * prior + alpha * (1 - prior))


print()
print("(e) correcting '4.8% chance the redesign does not work':")
for prior in (0.5, 0.1, 0.02):
    print(f"    prior P(works) = {prior:.2f} -> "
          f"P(works | sig) = {posterior_given_significant(prior, power):.4f}")
print("    The posterior depends on BOTH the prior and the data; a p-value")
print("    supplies only the likelihood-side information.")
```

</details>

**[ ] Exercise 5 — the p-value is a property of the null, demonstrated by
simulation.** Set up: baseline conversion 6%, $n = 4{,}000$ per arm, two-sided
$\alpha = 0.05$. (a) Simulate 20,000 experiments in which the null **is true**
($p_A = p_B = 0.06$) and record the fraction with p < 0.05. (b) Repeat with a real
effect of +2 percentage points, and record both the rejection rate in the effect
worlds (power) and the Type I rate in the null worlds. (c) With a prior that the
effect is real 50% of the time, compute $P(\text{real} \mid p < 0.05)$ from the
simulated rates, and repeat with priors 0.1 and 0.01. (d) Explain why the answer
differs so much from 95%, and compare the two levers that move it — raising power
versus lowering α.

<details>
<summary>Solution</summary>

(a) Under the true null, $\alpha = 0.05$ **by definition**, so the rejection rate
should be 0.05 — up to Monte Carlo error of about $\sqrt{0.05 \times 0.95/20000}
= 0.0015$. This is the check that validates the whole apparatus: if the false alarm
rate were 14% when α = 0.05, nothing else could be trusted either.

(b) With a real +2-point effect,
$\delta/\mathrm{SE} = 0.02/\sqrt{2 \times 0.07 \times 0.93/4000} =
0.02/0.005705 = 3.505$, giving power $\Phi(3.505 - 1.96) = \Phi(1.545) =
0.9389$ — the simulation should land near that. Crucially the Type I rate in the
null worlds stays at 0.05: the two are independent, because the false alarm rate
is a property of the threshold while power is a property of the effect size and
$n$.

(c) With simulated power $\approx 0.94$, $\alpha = 0.05$, and prior 0.5:
$$P(\text{real} \mid p<0.05) = \frac{0.94 \times 0.5}{0.94\times 0.5 + 0.05 \times 0.5} = \frac{0.470}{0.495} = 0.949.$$

With a 50/50 prior you get back roughly the power, which is the sanity check that
the arithmetic is right. Push the prior to 0.1 and it falls to
$0.094/(0.094+0.045) = 0.677$; to 0.01 and it collapses to
$0.0094/(0.0094+0.0495) = 0.160$ — a **16% posterior** from a p-value below
0.05, because the null pool is 99× larger.

(d) The answer differs from 95% because a p-value conditions on the null and
discards the prior. The "null pool" is $(1-\pi)$ times as large as the real pool,
and the false positives from it scale with $\alpha$ while the true positives
scale with power × $\pi$. Whenever $\alpha(1-\pi) \gg \text{power}\cdot\pi$, the
posterior collapses — and that condition is just a restatement of the base-rate
problem from [Lesson 62](62_conditional_probability_and_bayes.md).

Two levers, with very different reach. **Raise power**: at 0.99 instead of 0.94
the posterior with prior 0.01 goes only from 0.160 to 0.167, because power
multiplies a pool that is already negligible. **Lower α**: at $\alpha = 0.01$ the
posterior with prior 0.01 rises to $0.0094/(0.0094+0.0099) = 0.487$, which is a
far larger move — because the false-positive pool was the thing that was too
big. Lowering α costs you power and requires much more evidence to declare a win;
raising power costs you time and traffic. The prior is the third input and the
strongest of the three — which is why it has to be stated rather than assumed.

```python
import random
from math import erf, sqrt

random.seed(2024)
TRIALS = 20_000
N_ARM = 4_000
P_BASE = 0.06
EFFECT = 0.02
ALPHA = 0.05


def cdf(z):
    return 0.5 * (1 + erf(z / sqrt(2)))


def two_sided_p(k1, n1, k2, n2):
    pool = (k1 + k2) / (n1 + n2)
    se = (pool * (1 - pool) * (1 / n1 + 1 / n2)) ** 0.5
    return 2 * (1 - cdf(abs((k1 / n1 - k2 / n2) / se)))


def binom(rng, n, p):
    """A draw from Binomial(n, p).

    Drawing n Bernoulli trials one at a time is exact but costs O(n) per
    sample, which is prohibitive for 20,000 experiments of size 4,000.
    Since n*p and n*(1-p) are both in the hundreds here, the normal
    approximation from Lesson 68 is accurate to a few counts and is
    effectively instant. Small n is still drawn exactly.
    """
    if n <= 200:
        return sum(1 for _ in range(n) if rng.random() < p)
    mean = n * p
    sd = (n * p * (1 - p)) ** 0.5
    # Clip to the feasible integer range so impossible counts never occur.
    return min(n, max(0, int(round(rng.gauss(mean, sd)))))


rng = random.Random(7)

# (a) the null is TRUE in every trial: the rejection rate should be alpha.
reject_null = 0
for _ in range(TRIALS):
    ka = binom(rng, N_ARM, P_BASE)
    kb = binom(rng, N_ARM, P_BASE)
    if two_sided_p(ka, N_ARM, kb, N_ARM) < ALPHA:
        reject_null += 1
alpha_hat = reject_null / TRIALS
print(f"(a) null always true: rejection rate = {alpha_hat:.4f} "
      f"(target {ALPHA}, Monte Carlo error ~{sqrt(ALPHA * (1 - ALPHA) / TRIALS):.4f})")

# (b) half the worlds have a real +2 point effect.
reject_real = reject_fake = n_real = n_fake = 0
for _ in range(TRIALS):
    has_effect = rng.random() < 0.5
    ka = binom(rng, N_ARM, P_BASE)
    kb = binom(rng, N_ARM, P_BASE + (EFFECT if has_effect else 0.0))
    if has_effect:
        n_real += 1
    else:
        n_fake += 1
    if two_sided_p(ka, N_ARM, kb, N_ARM) < ALPHA:
        if has_effect:
            reject_real += 1
        else:
            reject_fake += 1

power = reject_real / n_real
type1 = reject_fake / n_fake
pool_theory = P_BASE + EFFECT / 2
power_theory = cdf(EFFECT / (2 * pool_theory * (1 - pool_theory) / N_ARM) ** 0.5 - 1.96)
print()
print(f"(b) n={N_ARM:,}/arm, effect +{EFFECT * 100:.1f} pp")
print(f"    power (real effect detected) = {power:.4f}  "
      f"(theory {power_theory:.4f})")
print(f"    Type I (false alarm)         = {type1:.4f}   "
      f"-> pinned at alpha regardless of the effect: "
      f"{abs(type1 - ALPHA) < 0.01}")


def posterior_given_significant(prior, power, alpha=ALPHA):
    return (power * prior) / (power * prior + alpha * (1 - prior))


print()
print("(c) P(real | p < 0.05) by Bayes, using the simulated power")
for prior in (0.5, 0.1, 0.01):
    print(f"    prior {prior:.2f} -> {posterior_given_significant(prior, power):.4f}")

print()
print("(d) levers, at prior = 0.01:")
print(f"    power 0.94 -> 0.99, prior 0.01: "
      f"{posterior_given_significant(0.01, 0.99):.4f} "
      f"(vs {posterior_given_significant(0.01, 0.94):.4f} at 0.94)")
print(f"    alpha 0.05 -> 0.01, prior 0.01: "
      f"{posterior_given_significant(0.01, 0.94, 0.01):.4f}")
print("    -> lowering alpha moves the posterior far more than raising power,")
print("       because the false-positive pool is the one that is too large.")
```

</details>

**[ ] Exercise 6 — Challenge: design the experiment before running it, and
explain why the order matters.** A recommendation engine's click-through rate is
2.0%. You want to test whether a change lifts it, and you have budget for **50,000
users per arm**.
(a) Compute the minimum detectable effect at $n = 50{,}000$ per arm, at 80% power
and two-sided α = 0.05.
(b) Compute the relative effect that corresponds to (a), and say whether it is a
plausible business target.
(c) Compute the sample size needed for a **50% relative** lift (2.0% → 3.0%) at the
same power, and compare with your budget.
(d) Compute the sample size for a **15% relative** lift, and check whether that
one fits.
(e) Explain what you would report if the experiment runs at $n = 50{,}000$ per arm
and returns a non-significant result, and why reporting the p-value alone would be
misleading.

<details>
<summary>Solution</summary>

(a) With $\bar p = 0.02$ and $n = 50{,}000$ per arm,
$\mathrm{SE}(\bar p_1 - \bar p_2) = \sqrt{2\bar p(1-\bar p)/n}
= \sqrt{2 \times 0.02 \times 0.98/50{,}000} = \sqrt{7.84\times10^{-7}}
= 0.0008854$.

$$\delta_{\min} = (1.959964 + 0.841621)\times 0.0008854 = 2.801585 \times 0.0008854 = \mathbf{0.002481},$$

i.e. **0.248 percentage points**.

(b) That is $0.248/2.0 = 12.4\%$ **relative**. Whether it is a plausible business
target depends on the product, but for a recommendation surface at a 2% baseline
it is a large ask — most tested changes move CTR by single-digit relative amounts.
So the budget, as stated, is aimed at roughly the smallest effect anyone should
care about.

(c) A 50% relative lift is $2.0\% \to 3.0\%$, so $\delta = 0.01$:

$$n = \frac{2 \times 0.02 \times 0.98 \times (2.801585)^2}{0.01^2} = \frac{0.0392 \times 7.849}{0.0001} = 3{,}076\ \text{per arm}.$$

That *fits* comfortably inside 50,000 — 16× more budget than needed. So if a 50%
lift were the real target, this budget is wildly over-provisioned.

(d) A 15% relative lift is $2.0\% \to 2.3\%$, so $\delta = 0.003$:
$n = 0.307687/0.000009 = \mathbf{34{,}186}$ per arm. That also fits inside 50,000.
Note the quadratic: 50% relative needed 3,076 and 15% relative needed 34,186 —
the smaller effect costs **11.1×** more traffic, because $(0.01/0.003)^2 = 11.11$.

So 50,000 per arm resolves anything down to about 12.4% relative. If the team
wanted to detect a 5% relative lift ($2.0\% \to 2.1\%$, $\delta = 0.001$), it would
need $0.307687/0.000001 = 307{,}676$ per arm — over 6× the budget. That is the
number to establish **before** running, because it determines whether the question
is answerable at all.

(e) Report three things, not one. **The estimate and its interval**: $\hat\Delta$
with a 95% CI, which tells the reader the range of effects consistent with the
data, including any that would harm. **The minimum detectable effect**, computed
from (a), so the reader knows the bound of the experiment's resolution. **The
power** against the effect actually observed.

Why the p-value alone misleads: $p = 0.2$ is compatible with a real 0.2-point
lift and with a real 0.5-point lift, and readers take it as evidence of "no
effect" when it is really evidence of "could not resolve". Worse, the failure is
silent — the report looks identical to a clean null result, so nothing prompts
anyone to ask whether the experiment was capable of answering the question. This
is Mistake 3 in the lesson, and the ordering matters because all three of these
numbers are computable *in advance*. Reporting them afterwards is a description;
reporting them beforehand is a design.

```python
from math import erf, sqrt


def cdf(z):
    return 0.5 * (1 + erf(z / sqrt(2)))


def zq(q):
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if cdf(mid) < q:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


Z_A, Z_B = zq(0.975), zq(0.80)
P_BASE = 0.02
N_ARM = 50_000
BUDGET = 50_000


def se_of_difference(n_arm, p=P_BASE):
    """Pooled-null standard error of p1 - p2 for equal arms."""
    return sqrt(2 * p * (1 - p) / n_arm)


def mde(n_arm, p=P_BASE):
    """Minimum detectable effect at 80% power, two-sided alpha = 0.05."""
    return (Z_A + Z_B) * se_of_difference(n_arm, p)


def n_for(delta, p=P_BASE):
    """Required users per arm for a given absolute effect."""
    return 2 * p * (1 - p) * (Z_A + Z_B) ** 2 / delta**2


se = se_of_difference(N_ARM)
d_min = mde(N_ARM)
print(f"(a) SE of difference at n={N_ARM:,}/arm = {se:.7f}")
print(f"    minimum detectable effect = {d_min:.6f} = "
      f"{d_min * 100:.3f} percentage points")
print()
print(f"(b) relative effect = {d_min / P_BASE * 100:.1f}%  "
      f"(baseline {P_BASE * 100:.1f}%)")
print()
for rel in (0.50, 0.15, 0.05):
    target = P_BASE * (1 + rel)
    delta = target - P_BASE
    need = int(n_for(delta))
    verdict = "FITS" if need <= BUDGET else "DOES NOT FIT"
    print(f"(c/d) {rel * 100:4.0f}% relative -> {P_BASE * 100:.1f}% -> "
          f"{target * 100:.2f}%  (delta {delta:.4f})")
    print(f"        n = {need:,} per arm  ({verdict} in the "
          f"{BUDGET:,} budget)")
print()
print("(e) what a non-significant result would need to report:")
print(f"    1. the estimate and its 95% CI (width tied to the SE above)")
print(f"    2. the minimum detectable effect: {d_min * 100:.3f} pp")
print(f"    3. the power at whatever effect was observed")
print("    A p-value alone reads identically to a clean null, so nothing")
print("    prompts the reader to ask whether the test could answer the question.")
```

</details>

## Summary

- An estimator is a statistic used to guess a parameter; the MLE maximises
  P(data | θ), and for Bernoulli data it is always the observed fraction k/n.
- MSE(T) = Var(T) + Bias(T)² is the organising formula: it trades estimator noise
  against estimator error, and minimising it is the goal.
- Bias that shrinks with n is harmless; bias that does not shrink is fatal, since
  it persists at any sample size.
- The two-proportion z statistic divides the observed difference by the
  **pooled** standard error under the null, and is approximately standard normal
  when the null holds.
- A p-value is P(data at least this extreme | null true) — a statement about the
  data, never about the probability the hypothesis is true.
- A p-value of 0.05 with a rare true effect can mean under 2% probability the
  effect is real, because the base rate dominates.
- Type I (false alarm, rate α) and Type II (missed effect, rate β) trade against
  each other; power is 1 − β and must be checked before running an experiment.
- A confidence interval is the set of hypotheses a test would reject, so "not
  significant" and "the CI contains 0" are the same statement.
- Pre-specify the null, the primary metric, and the sample size. Searching after
  seeing data inflates the false positive rate without limit.

## Next

[70 — Information Theory and Entropy](../part05_probability_statistics/70_information_theory_entropy.md) measures
how surprising an outcome is in bits, and shows that cross-entropy — the loss
every neural network minimises — is just entropy computed against the wrong
distribution.