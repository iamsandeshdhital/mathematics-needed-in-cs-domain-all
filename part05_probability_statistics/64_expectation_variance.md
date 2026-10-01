# 64 — Expectation, Variance, and Laws

**Part**: part05_probability_statistics · **Prerequisites**: 63 · **Time**: 35 min

---

## In Plain Words

Given a random variable, the two questions worth asking are: what does it average
to, and how much does it wander? The first is the expectation, sometimes called
the mean, and it is a probability-weighted average of the possible values. The
second is the variance, the average squared distance from the mean, and its
square root is the standard deviation — the spread in the original units.

Expectation turns out to have one remarkable property that makes it the most
useful tool in statistics: the expectation of a sum is the sum of the
expectations, **whether or not the parts are independent**. No assumption at all.
That is why you can compute the average number of database calls for a million
requests by doing one small calculation, without ever building the distribution.

There is also one notorious trap. The square of a mean is not the mean of the
squares, and the gap between them is not a rounding detail — it is the variance.
Every time you average squared quantities, the squaring and the averaging do not
commute, and the reason is that squaring over-weights large values. This lesson
shows exactly how much they differ, and that the difference is precisely Var.

## Why Computer Science Cares

- **Every standard error in [Lesson 68](../part05_probability_statistics/68_law_of_large_numbers_and_clt.md) and
  [Lesson 69](../part05_probability_statistics/69_estimation_and_hypothesis_testing.md) is a variance divided by
  n.** The confidence interval formula and the p-value formula are both this.
- **Algorithmic runtime analysis for randomised algorithms.** Expected cost is
  E[cost]; Quicksort's expected depth is 2 ln n, and the variance is what tells
  you how concentrated that expectation is.
- **Hashing and load balancing.** The variance of the number of collisions, or of
  the number of keys landing in a bucket, governs worst-case latency under
  hashing.
- **Queueing theory.** Average wait time is an expectation; the tail is a variance
  or a higher moment. SLOs are about tails
  ([Lesson 65](../part05_probability_statistics/65_continuous_random_variables.md)).
- **Risk and optimisation.** Minimising expected loss is the entire framing of
  decision-making under uncertainty, and a portfolio's risk is its variance.

## The Formal Version

**Definition.** The *expectation* of a discrete random variable X with PMF p_X is

    E[X] = Σ_x x · p_X(x)

More generally, for any function g, the expectation of g(X) is E[g(X)] = Σ_x
g(x) p_X(x). Expectation is a linear functional: it takes a random variable and
returns a number, and it respects weighted sums of numbers.

**Theorem (Jensen's inequality, simplest case).** For any convex function g and
any random variable X,

    E[g(X)] ≥ g(E[X])

Concretely, for the square function g(x) = x²: **E[X²] ≥ (E[X])²**, with equality
exactly when X is constant.

**Proof (for the square).** Write μ = E[X]. Then

    E[X²] − μ² = E[X² − 2μX + μ²] = E[(X − μ)²] ≥ 0

where the middle step used linearity of expectation and E[μ] = μ.  ∎

The left side is by definition the variance, so this single theorem is what makes
variance non-negative. Everything about "spread" follows from it.

**Definition.** The *variance* is

    Var(X) = E[(X − E[X])²] = E[X²] − (E[X])²

and the *standard deviation* is σ = √Var(X). Both have the same units as X.

**Definition.** The *k-th moment* is E[Xᵏ]. The mean is the first moment about the
origin; the variance is the second moment about the mean. The distinction is not
cosmetic: moments about the origin are translation-sensitive, moments about the
mean are not. Adding a constant to X shifts every value but leaves the spread
unchanged — which is exactly why variance is defined around E[X] rather than
around zero.

### The core theorem: linearity of expectation

**Theorem.** For random variables X₁, …, Xₙ and constants aᵢ,

    E[Σᵢ aᵢXᵢ] = Σᵢ aᵢE[Xᵢ]

**No independence assumption. None.**

**Proof.** Let g(x₁,…,xₙ) = Σᵢ aᵢxᵢ. Then E[g] = Σ_{x} g(x)·P(x) =
Σ_{x}(Σᵢ aᵢxᵢ)P(x) = Σᵢ aᵢ Σ_{x} xᵢ P(x). The inner sum is E[Xᵢ], since the
marginal probability of xᵢ is Σ over all other coordinates.  ∎

**Explanation.** Linearity is a property of the *sum*, not of the joint
distribution. It says the average of a total is the total of the averages, which
is a statement about how we organised the arithmetic. If it required
independence it would be a much weaker theorem, and it would not be the workhorse
it is.

Two corollaries worth internalising:

- E[X + c] = E[X] + c, so adding a constant shifts the mean by that constant.
- E[I·g(X)] = E[I]·E[g(X)] whenever I is an indicator, *provided* I is
  independent of X. This is the "conditional expectation" trick used constantly
  in algorithm analysis: multiply an indicator by a cost, and the expectation
  factors.

### Variance of a sum

**Theorem.** Var(Σᵢ Xᵢ) = Σᵢ Var(Xᵢ) + 2Σ_{i<j} Cov(Xᵢ, Xⱼ), where

    Cov(X, Y) = E[XY] − E[X]E[Y]

and in particular, if the Xᵢ are pairwise independent then

    Var(Σᵢ Xᵢ) = Σᵢ Var(Xᵢ)

**Explanation.** Expand (ΣXᵢ)², apply linearity, and note that E[Xᵢ²] =
Var(Xᵢ) + E[Xᵢ]². The cross terms E[XᵢXⱼ] are not E[Xᵢ]E[Xⱼ] unless Xᵢ and Xⱼ
are independent — which is exactly what the covariance term records, and why
variance behaves so differently from expectation here.

**The contrast to memorise:**

| | Requires independence? |
| --- | --- |
| E[ΣXᵢ] = ΣE[Xᵢ] | **No** |
| Var(ΣXᵢ) = ΣVar(Xᵢ) | **Yes** |

This asymmetry is the practical lesson of the lesson: means are robust to
dependencies, spread is not.

### Law of total variance

**Theorem.** If Y takes values y₁, …, yₘ and X is a random variable, then

    Var(X) = E[Var(X | Y)] + Var(E[X | Y])

**Explanation.** Decompose X as (its conditional mean given Y) plus (the
remaining noise). The two pieces are uncorrelated by construction, so their
variances add: the first term is the average within-group spread, the second is
the spread of the group means. This is the formal statement of "total risk =
systematic risk + idiosyncratic risk", and it is what lets you decompose a
variance into components you can actually attack.

### Variance of common functions

For constants a, b:

| | Mean | Variance |
| --- | --- | --- |
| aX + b | aE[X] + b | a²Var(X) |
| X² | E[X²] | Var(X²) = Var(X)(Var(X) + 2(E[X])²) |

The second row is worth pausing on: squaring *inflates* the mean by a term
proportional to the square of the original mean. If a latency has mean 100 ms
and standard deviation 10 ms, then E[latency²] is not 100² = 10,000 but
Var + μ² = 100 + 10,000 = 10,100. The mean dominates, and this is the algebraic
form of "squares over-weight large values".

## Worked Example

### Example A — a small hand-built distribution

Let X be the number of heads in two fair coin flips, so p(0) = 1/4, p(1) = 1/2,
p(2) = 1/4 (from [Lesson 63](../part05_probability_statistics/63_discrete_random_variables.md)).

**Expectation:**

    E[X] = 0·(1/4) + 1·(1/2) + 2·(1/4) = 0 + 0.5 + 0.5 = 1

**E[X²]:**

    E[X²] = 0²·(1/4) + 1²·(1/2) + 2²·(1/4) = 0 + 0.5 + 1.0 = 1.5

**Variance, both routes:**

    direct:  E[(X−1)²] = (0−1)²·(1/4) + (1−1)²·(1/2) + (2−1)²·(1/4)
                       = 0.25 + 0 + 0.25 = 0.5
    formula: E[X²] − (E[X])² = 1.5 − 1 = 0.5   ✓

**Standard deviation:** √0.5 ≈ 0.7071.

**The gap that matters.** (E[X])² = 1 but E[X²] = 1.5. The difference is exactly
Var = 0.5. Now imagine averaging 20 such variables: E[ΣXᵢ] = 20 regardless of any
dependency between them, but Var(ΣXᵢ) = ΣVar + 2ΣCov is entirely dependent on the
covariances. If the 20 coin pairs all came from one shuffled deck and were
strongly correlated, the sum's variance could be close to 20 × 0.5 = 10, or much
larger.

### Example B — linearity of expectation with a mechanism that is obviously not independent

A system processes 3 requests. Request 1 is a "large" job with probability 0.5.
If request 1 was large, the cache is cold, so request 2 is also large with
probability 0.6. And request 3 is large with probability 0.5 regardless.

Let Lᵢ be the indicator that request i is large. Cost of request i is
1 + Lᵢ (one base unit, plus one if large). Total cost C = Σᵢ (1 + Lᵢ) = 3 + L₁ + L₂ + L₃.

**By linearity, no independence needed:**

    E[C] = 3 + E[L₁] + E[L₂] + E[L₃] = 3 + 0.5 + 0.6 + 0.5 = 4.6

Note we never used that L₁ and L₂ are dependent. We did not need the joint
probability P(L₁ = 1, L₂ = 1) = 0.3 at all.

**Now the variance, where dependence bites:**

    Var(C) = Var(L₁) + Var(L₂) + Var(L₃) + 2Cov(L₁,L₂) + 2Cov(L₁,L₃) + 2Cov(L₂,L₃)

Each Lᵢ is Bernoulli, so Var(Lᵢ) = p(1−p):

    Var(L₁) = 0.5·0.5 = 0.25
    Var(L₂) = 0.6·0.4 = 0.24
    Var(L₃) = 0.25

Independence of L₁ and L₂ is broken, so we need the covariance. For Bernoullis:

    Cov(L₁, L₂) = P(L₁=1, L₂=1) − P(L₁=1)P(L₂=1) = 0.3 − 0.5·0.6 = 0.3 − 0.3 = 0

So here the dependence is *not* reflected in the covariance — because 0.5 × 0.6
= 0.3 happens to equal the joint probability exactly, which by the chain rule
means L₁ and L₂ are actually independent. Let me change the model so the effect
is real: suppose P(L₁=1, L₂=1) = 0.45. Then P(L₂=1|L₁=1) = 0.9, so:

    Cov(L₁, L₂) = 0.45 − 0.3 = 0.15

and

    Var(C) = 0.25 + 0.24 + 0.25 + 2(0.15) = 0.74 + 0.30 = 1.04

If you had wrongly assumed independence you would report Var(C) = 0.74, understating
the spread by about 29%. Meanwhile the **mean was 4.6 either way**. That is the
lesson in one line: linearity of expectation is assumption-free, and variance
silently inherits every dependency you failed to model.

### Example C — E[X²] ≠ E[X]² with a dramatic gap

Let X be uniform on {1, 2, 3}.

    E[X]  = (1 + 2 + 3)/3 = 2
    (E[X])² = 4
    E[X²] = (1 + 4 + 9)/3 = 14/3 ≈ 4.6667

So E[X²] − (E[X])² = 4.6667 − 4 = 0.6667 = Var(X), and

    Var(X) = (1² + 2² + 3²)/3 − 2² = 14/3 − 4 = 2/3

The relative gap is (4.6667 − 4)/4 = 16.7%. Now scale up: let Y = 100X. Then

    E[Y] = 200,  (E[Y])² = 40,000
    E[Y²] = 100² · 14/3 = 46,666.7
    Var(Y) = 100² · (2/3) = 6,666.7

The gap between E[Y²] and (E[Y])² is 6,666.7 out of 40,000, or 16.7% — the same
relative gap. This is worth noting: **the relative gap is invariant under
rescaling**, so the discrepancy never washes out by working in different units.

Where this bites hardest is when averaging quantities with large dynamic range. If
you average squared errors across a model where typical values are 1 but a few are
1000, the average of the squares is dominated by the few huge values, and the
number you report tells you almost nothing about typical behaviour. This is the
mathematical reason error metrics are reported as **root mean squared error**
rather than mean square error: taking the square root at the end makes the units
right and stops large outliers from dominating the *reported* figure.

## Runnable Code

### Expectation and variance, computed three ways

```python
from math import sqrt
from itertools import product

# Two fair coin flips; X = number of heads.
outcomes = list(product([0, 1], repeat=2))
pmf = {0: 0.25, 1: 0.50, 2: 0.25}

support = sorted(pmf)

# (1) Direct from the definition.
mean = sum(x * pmf[x] for x in support)
second_moment = sum(x**2 * pmf[x] for x in support)
var_about_mean = sum((x - mean) ** 2 * pmf[x] for x in support)

print("x | P(X=x) | x*P(X=x) | x^2*P(X=x) | (x-mean)^2*P(X=x)")
for x in support:
    print(f"{x} | {pmf[x]:.6f} | {x * pmf[x]:9.6f} | "
          f"{x**2 * pmf[x]:10.6f} | {(x - mean) ** 2 * pmf[x]:14.6f}")
print()
print(f"E[X]              = {mean:.6f}")
print(f"E[X^2]            = {second_moment:.6f}")
print(f"E[(X-E[X])^2]     = {var_about_mean:.6f}   (direct definition)")
print(f"E[X^2]-(E[X])^2   = {second_moment - mean**2:.6f}   (the formula)")
print(f"agree: {abs(var_about_mean - (second_moment - mean**2)) < 1e-12}")
print(f"sd(X)             = {sqrt(var_about_mean):.6f}")
print()
print(f"KEY: (E[X])^2 = {mean**2:.6f} but E[X^2] = {second_moment:.6f}")
print(f"the gap is exactly Var(X) = {second_moment - mean**2:.6f}")
```

### Linearity of expectation, without any independence

```python
import random

# Linearity of expectation needs NO independence. To make that vivid, build
# two worlds with the same marginals and wildly different dependence.
#
# Each trial: draw TEN Bernoulli(0.3) variables and record their sum.
rng = random.Random(11)
TRIALS = 200_000
N = 10
P = 0.3

# World A: fully INDEPENDENT. Ten separate coins.
sums_indep = []
for _ in range(TRIALS):
    s = sum(1 for _ in range(N) if rng.random() < P)
    sums_indep.append(s)

# World B: perfectly CORRELATED. Draw ONE hidden coin, copy it ten times.
# Every variable still has marginal P(X=1) = 0.3, so E is unchanged --
# but the sum is 0 or 10 and nothing in between.
sums_correl = []
for _ in range(TRIALS):
    hidden = 1 if rng.random() < P else 0
    sums_correl.append(hidden * N)

mean_indep = sum(sums_indep) / TRIALS
mean_correl = sum(sums_correl) / TRIALS
var_indep = sum(s * s for s in sums_indep) / TRIALS - mean_indep**2
var_correl = sum(s * s for s in sums_correl) / TRIALS - mean_correl**2

print(f"{N} variables, each Bernoulli({P}), {TRIALS:,} trials each")
print(f"predicted mean of the sum = {N} * {P} = {N * P}")
print()
print("mean of the SUM (linearity says both worlds must match):")
print(f"  independent : {mean_indep:.6f}")
print(f"  correlated  : {mean_correl:.6f}")
print(f"  match the prediction: "
      f"{abs(mean_indep - N * P) < 0.05 and abs(mean_correl - N * P) < 0.05}")
print()
print("variance of the SUM (dependence changes this completely):")
print(f"  independent : {var_indep:10.4f}   sd = {var_indep ** 0.5:.4f}")
print(f"                 theory N*p*(1-p) = {N * P * (1 - P):.4f}")
print(f"  correlated  : {var_correl:10.4f}   sd = {var_correl ** 0.5:.4f}")
print(f"                 theory N^2*p*(1-p) = {N**2 * P * (1 - P):.4f}")
print()
print(f"-> the CORRELATED world has {var_correl / var_indep:.2f}x MORE spread,")
print("   yet the means match to three decimals. Same marginals, same mean,")
print("   wildly different risk. That is why variance needs an independence")
print("   assumption and expectation does not.")
print()
print("Direction matters: POSITIVE dependence (all-or-nothing, as here) creates")
print("fatter tails. NEGATIVE dependence -- a load balancer spreading work so")
print("no node gets two slow requests -- would push the variance DOWN, below")
print("n*p*(1-p), which is why coordinated schedulers outperform naive ones.")
```

### A worked dependency example: same mean, different variance

```python
import random
from math import sqrt

# The Example B model, where the second job's cost depends on the first.
# Each variable has a FIXED marginal; only the JOINT probability changes,
# and that is what shifts the covariance.

P_L1, P_L2, P_L3 = 0.5, 0.6, 0.5
TRIALS = 400_000


def stats(p_joint):
    """Simulate C = 3 + L1 + L2 + L3 with FIXED marginals.

    P(L1 = 1, L2 = 1) is achieved by changing the conditional probabilities,
    which is exactly how real dependent variables are constructed. Both
    marginals stay at P_L1 and P_L2 regardless of the joint value.
    """
    rng = random.Random(3)
    # Given L1 = 1, L2 happens this often...
    p_l2_if_l1 = p_joint / P_L1
    # ...and given L1 = 0, this often, chosen so P(L2=1) = P_L2 exactly.
    p_l2_if_not_l1 = (P_L2 - P_L1 * p_l2_if_l1) / (1 - P_L1)
    assert 0 <= p_l2_if_l1 <= 1 and 0 <= p_l2_if_not_l1 <= 1
    total = 0.0
    total_sq = 0.0
    for _ in range(TRIALS):
        l1 = 1 if rng.random() < P_L1 else 0
        cond = p_l2_if_l1 if l1 else p_l2_if_not_l1
        l2 = 1 if rng.random() < cond else 0
        l3 = 1 if rng.random() < P_L3 else 0
        c = 3 + l1 + l2 + l3
        total += c
        total_sq += c * c
    mean = total / TRIALS
    return mean, total_sq / TRIALS - mean**2


print(f"P(L1)= {P_L1}  P(L2)= {P_L2}  P(L3)= {P_L3}   (marginals held FIXED)")
print(f"linearity predicts E[C] = 3 + {P_L1} + {P_L2} + {P_L3} "
      f"= {3 + P_L1 + P_L2 + P_L3}")
print()
for joint in (0.30, 0.45):
    mean, var = stats(joint)
    cov = joint - P_L1 * P_L2
    # Analytic variance: sum of individual variances + 2*covariance
    var_parts = (P_L1 * (1 - P_L1) + P_L2 * (1 - P_L2) + P_L3 * (1 - P_L3))
    var_analytic = var_parts + 2 * cov
    label = "independent" if abs(cov) < 1e-12 else "dependent"
    print(f"P(L1 and L2) = {joint:.2f}  ({label}, cov = {cov:+.4f})")
    print(f"   E[C]   sim {mean:.4f}   analytic {3 + P_L1 + P_L2 + P_L3:.4f}")
    print(f"   Var(C) sim {var:.4f}   analytic {var_analytic:.4f}   "
          f"sd = {sqrt(var):.4f}")
    print(f"   1 sd range: [{mean - sqrt(var):.2f}, {mean + sqrt(var):.2f}]")
    print()

print("The MEAN is identical in both worlds -- linearity of expectation")
print("required no assumption at all about L1 and L2.")
print("The VARIANCE is not: the 2*Cov term adds 0.30 in the dependent case")
print("and nothing in the independent one. Ignoring it understates spread.")
```

### Why root mean squared error is the right metric

```python
from math import sqrt

# Four measurements. Three are close to 10 ms, one is catastrophically off.
observations = [10.0, 10.5, 9.8, 400.0]
true_value = 10.0

errors = [o - true_value for o in observations]
mean_error = sum(errors) / len(errors)

mean_abs = sum(abs(e) for e in errors) / len(errors)
mean_square = sum(e**2 for e in errors) / len(errors)
rmse = sqrt(mean_square)

# The metric difference, shown side by side on two comparable data sets.
# Same outliers, wildly different magnitudes -- RMSE punishes the big ones.
mild = [10.0, 10.5, 9.8, 13.0]        # one 3 ms error
mild_errors = [o - true_value for o in mild]
mild_mae = sum(abs(e) for e in mild_errors) / len(mild)
mild_rmse = sqrt(sum(e**2 for e in mild_errors) / len(mild))

print(f"errors                 : {[f'{e:+.2f}' for e in errors]}")
print(f"mean error             = {mean_error:+.4f}")
print(f"mean absolute error    = {mean_abs:.4f} ms")
print(f"mean square error      = {mean_square:.2f} ms^2")
print(f"root mean square error = {rmse:.4f} ms")
print()
print(f"RMSE is {rmse / mean_abs:.2f}x the mean absolute error,")
print(f"entirely because of the single {errors[-1]:+.0f} ms outlier.")
outlier_share = errors[-1] ** 2 / sum(e**2 for e in errors)
print(f"That one value contributes {outlier_share * 100:.1f}% of the")
print("total squared error, but only "
      f"{abs(errors[-1]) / sum(abs(e) for e in errors) * 100:.1f}% of the")
print("total absolute error. Squaring re-weights the large values.")
print()
print("Contrast with the same dataset but a MILD outlier:")
print(f"  errors              : {[f'{e:+.2f}' for e in mild_errors]}")
print(f"  mean absolute error = {mild_mae:.4f} ms")
print(f"  RMSE                = {mild_rmse:.4f} ms")
print(f"  RMSE/MAE ratio      = {mild_rmse / mild_mae:.2f}  vs {rmse / mean_abs:.2f} above")
print()
print("So the ratio grows with the size of the outlier: the penalty is")
print("superlinear in the error, which is exactly the point.")
print()
print("Algebraic source. Writing the error as E, the identity is")
print("  E[E^2] = Var(E) + (E[E])^2")
print("The variance ADDS to the squared mean; it never replaces it.")
print()
print("Practical rule: RMSE when large errors are catastrophic (dose limits,")
print("load forecasts). MAE when they are not (search ranking, survey scales),")
print("because MAE is robust to outliers.")
```

## Common Mistakes

**Mistake 1 — writing Var(X) = E[X]² − (E[X])².**
Wrong sign order. The formula is Var(X) = **E[X²] − (E[X])²**, with the square
inside the second bracket only. The tempting version looks symmetric and
plausible, and it can even return a negative "variance" for some inputs, which at
least announces itself — but it is wrong.

**Mistake 2 — dividing E[X²] by n twice, or averaging variances.**
Wrong: "the variance of the average of n samples is Var(X)." It is Var(X)/n.
Division by n is the entire reason sampling helps, and omitting it inflates your
error bars by a factor of √n. For 100 samples that is a factor of 10.

**Mistake 3 — assuming Var(ΣXᵢ) = ΣVar(Xᵢ) for independent *enough* things.**
Consecutive HTTP requests to a rate-limited service are not independent; they are
positively correlated when the service is stressed. The covariance terms are
exactly the correction for that, and dropping them understates tail risk — the
errors you most want to predict.

**Mistake 4 — thinking the mean is a likely value.**
Wrong: "the mean latency is 50 ms, so a typical request takes 50 ms." For a
right-skewed latency distribution the mean is dragged up by the tail and *most*
requests are faster than the mean. This is why percentiles, not means, belong in
a latency dashboard, and why the median is usually the number to report to
non-technical stakeholders.

**Mistake 5 — ignoring the variance when comparing options.**
Wrong: "Option A has expected value 10 and option B has expected value 10, so
they are equally good." They may have variances of 1 and 100, in which case A is
better for almost any risk-adjusted criterion. Any decision made on expectation
alone is incomplete.

## Formula Sheet

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$E[X]$` | `$\mu = \sum_x x\,p_X(x)$` | **Expectation**: the probability-weighted average. Always in the units of X, and often not an achievable value. | Every "what does it average to" question. Long-run balance point, never a prediction for one run. |
| `$E[g(X)]$` | `$= \sum_x g(x)\,p_X(x)$` | Apply the function first, then average. | Squared errors, $X^2$, $\log X$, anything derived from a sample. |
| Jensen | `$E[g(X)] \ge g(E[X])$` for convex g | Averaging first is never worse for a convex function. | The single fact behind `E[X²] ≥ (E[X])²`, and behind "squares over-weight large values". |
| `$E[X^2]$` | `$\ge (E[X])^2$` | **The trap.** The mean of squares is not the square of the mean, and the gap is not rounding. | Averaging squared quantities — loss functions, moments, energy. |
| `$E[X^k]$` | `$k$-th moment about the origin | The mean is the first; the variance is the second *about the mean*. | Comparing moments. About the origin is translation-sensitive; about the mean is not. |
| `$E[X+c]$` | `$= E[X] + c$` | Adding a constant shifts the mean by exactly that constant. | Converting units, offsets, fixed costs. |
| `$\mathrm{Var}(X)$` | `$= E[(X-E[X])^2] = E[X^2] - (E[X])^2$` | **Variance**: mean squared distance from the mean. Nonnegative, by Jensen. Square goes *inside* the brackets only. | Every spread question. Watch the sign order — Mistake 1 in this lesson. |
| `$\sigma$` | `$\sigma = \sqrt{\mathrm{Var}(X)}$` | Standard deviation, in the units of X. | Error bars, "±", RMSE, comparing spreads across differently-scaled quantities. |
| `$\mu$ | `$E[X]$` | The mean. | Centring data, SLOs, expected cost. |
| `E[\sum_i a_iX_i]` | `$= \sum_i a_i E[X_i]$` | **Linearity of expectation. No independence assumption — none.** | The workhorse. Computing expected cost of a million requests from one small calculation. |
| `$E[Ig(X)]$` | `$= E[I]\cdot E[g(X)]$`, needs I independent of X | The conditional-expectation trick: multiply an indicator by a cost and factor. | Algorithm analysis, "expected work if the cache misses". |
| `$aX + b$` | mean `$aE[X]+b$`; variance `$a^2\mathrm{Var}(X)$` | Scaling multiplies spread by $\lvert a\rvert$; adding a constant leaves spread unchanged. | Unit conversion, normalisation. **Variance ignores $b$ entirely.** |
| `$X^2$` | `$E[X^2]$`; `$\mathrm{Var}(X^2) = \mathrm{Var}(X)\big(\mathrm{Var}(X) + 2(E[X])^2\big)$` | Squaring *inflates* the mean by a term proportional to the square of the original mean. | Mean latency 100 ms, sd 10 ms ⇒ $E[L^2] = 10{,}100$, not 10,000. |
| `$\mathrm{Cov}(X,Y)$` | `$= E[XY] - E[X]E[Y]$` | Do they move together? Signed, and in squared units. | The correction term for dependence. For Bernoullis, `$\mathrm{Cov} = P(\text{both}) - p_1p_2$`. |
| `$\mathrm{Var}(\sum_i X_i)$` | `$= \sum_i \mathrm{Var}(X_i) + 2\sum_{i<j}\mathrm{Cov}(X_i,X_j)$` | **Requires independence** to drop the covariance terms. Positive covariance *increases* spread. | Any risk estimate over a batch. Getting this wrong understates the tail. |
| independent | `$\mathrm{Var}(\sum_i X_i) = \sum_i \mathrm{Var}(X_i)$` | The shortcut, valid only when every covariance vanishes. | Binomial sums, coin flips, trials argued independent. |
| `$\bar{X}$` (sample mean of n) | `$E[\bar{X}] = \mu$`, `$\mathrm{Var}(\bar{X}) = \sigma^2/n$` | Averaging n samples divides the *variance* by n, so the standard error falls as $1/\sqrt{n}$. | Every standard error. Omitting the `/n` inflates error bars by $\sqrt{n}$ — a factor of 10 for n = 100. |
| `$\mathrm{Var}(X\mid Y)$` | `$\mathrm{Var}(X) = E[\mathrm{Var}(X\mid Y)] + \mathrm{Var}(E[X\mid Y])$` | **Law of total variance**: spread = average within-group spread + spread of group means. | Decomposing risk into attackable pieces; the formal "systematic + idiosyncratic". |
| `$E[X\mid Y=y_j]$` | `$\mu_j$` with weights $P(Y=y_j)$ | Group means; `$\mathrm{Var}(E[X\mid Y])$` is their weighted spread. | Between-segment variance. Segments at 200 ms and 50 ms give 5400 here. |
| `$\bar X - \mu$` | `$= O(\sigma/\sqrt{n})$` | How far a sample mean typically sits from the true mean. | Sizing a test or a load run; the basis of [Lesson 68](../part05_probability_statistics/68_law_of_large_numbers_and_clt.md). |
| RMSE vs MAE | `$\mathrm{RMSE} = \sqrt{E[E^2]}`, `$\mathrm{MAE} = E\lvert E\rvert` | RMSE is dominated by outliers; MAE is robust to them. | In the lesson's code RMSE = 195.0 ms against MAE = 97.7 ms — a factor of 2.00, entirely because of the single 390 ms error. |

## Multiple Choice Questions

**Q1.** For the uniform variable on {1, 2, 3}, what are `E[X²]` and `(E[X])²`?

- A) Both are 4, because averaging commutes with squaring
- B) `E[X²] = 14/3 ≈ 4.667` and `(E[X])² = 4`; the gap of 2/3 is the variance
- C) Both are 14/3, because the variance is included in both
- D) `E[X²] = 4` and `(E[X])² = 14/3`, because squaring moves mass toward the mean

<details>
<summary>Answer and explanation</summary>

**B) `E[X²] = 14/3 ≈ 4.667` and `(E[X])² = 4`; the gap of 2/3 is the variance.**

Example C works this out exactly. Option A is the misconception the whole lesson
exists to correct. Option C misassigns which expression carries the variance —
it is the *difference* between them, not a component of each. Option D reverses
the inequality, which is impossible by Jensen's inequality:
$E[X^2] \ge (E[X])^2$ always, with equality only for a constant variable.

</details>

**Q2.** Ten Bernoulli(0.3) variables are summed. What is the variance of the sum
if they are perfectly correlated (one hidden coin copied ten times)?

- A) 2.1, the same as the independent case, because the marginals are identical
- B) 21.0, ten times larger, because the covariance terms add up
- C) 0, because a perfectly correlated sum has no randomness beyond one coin
- D) 210, a hundred times larger

<details>
<summary>Answer and explanation</summary>

**B) 21.0, ten times larger, because the covariance terms add up.**

The sum is 0 or 10 with probability 0.7/0.3, so
$\mathrm{Var} = 10^2 \cdot 0.3 \cdot 0.7 = 21$, against $10 \cdot 0.3 \cdot 0.7 =
2.1$ in the independent case. This is the `theory N^2*p*(1-p)` line in the
lesson's second code block, and it is exactly the `var_correl / var_indep = 10.00x`
ratio it prints. Option A is the trap: identical marginals guarantee an identical
*mean*, never an identical variance. Option C is wrong because the hidden coin
still carries randomness, which is now concentrated entirely in one variable.
Option D miscounts the scaling.

</details>

**Q3.** Why does `Var(X₁ + X₂ + X₃) = Σ Var(Xᵢ)` need an independence assumption
while `E[X₁ + X₂ + X₃] = Σ E[Xᵢ]` does not?

- A) Linearity needs independence only when the variables are non-identically distributed
- B) Linearity is a property of the sum, but the variance expansion contains cross terms $E[X_iX_j]$ that factorise only under independence
- C) Neither needs independence; the covariance terms vanish automatically
- D) Expectation needs independence, variance does not — the lesson's table is backwards

<details>
<summary>Answer and explanation</summary>

**B) Linearity is a property of the sum, but the variance expansion contains cross
terms $E[X_iX_j]$ that factorise only under independence.**

This is the asymmetry the lesson is built around. Option A is false —
linearity works for any collection, identically distributed or not. Option C is
false precisely when the point: the covariance terms vanish only for independent
variables, and Example B shows $\mathrm{Cov} = 0.15$ changing the answer by 29%.
Option D inverts the lesson's own table.

</details>

**Q4.** A latency distribution has mean 100 ms and standard deviation 10 ms. What
is `E[latency²]`?

- A) 10,000
- B) 10,100
- C) 200
- D) It cannot be computed without the full PMF

<details>
<summary>Answer and explanation</summary>

**B) 10,100.**

$E[X^2] = \mathrm{Var}(X) + (E[X])^2 = 100 + 10{,}000 = 10{,}100$. Option A drops
the variance term. Option C is $E[L^2]$ confused with something else entirely.
Option D is false — the second moment is determined by the mean and the variance,
which is the whole point of writing variance as $E[X^2] - (E[X])^2$.

</details>

**Q5.** Ten independent requests each cost 1 unit plus 1 if the cache misses,
with miss probability 0.2. What is the expected total cost, and does answering
require the joint distribution?

- A) 12, and yes — you need $P(\text{two specific requests both miss})$
- B) 12, and no — linearity of expectation needs only the marginals
- C) 10, because the base cost dominates
- D) It cannot be computed without knowing whether the misses are correlated

<details>
<summary>Answer and explanation</summary>

**B) 12, and no — linearity of expectation needs only the marginals.**

$E[C] = 10 + \sum_{i=1}^{10} E[L_i] = 10 + 10 \times 0.2 = 12$. Option A is the
over-correction: the joint distribution is needed for the *variance*, never the
mean. Option C forgets the retry cost entirely. Option D describes the
variance problem, not the expectation, and the answer is well defined either way.

</details>

**Q6.** Customers split into 40% "power" at mean 200 ms and 60% "casual" at mean
50 ms, with standard deviation 20 ms inside each segment. What fraction of the
total variance is between-segment?

- A) 6.9%
- B) 93.1%
- C) 50%
- D) It depends on the sample size

<details>
<summary>Answer and explanation</summary>

**B) 93.1%.**

Between-segment variance is $0.4(200-110)^2 + 0.6(50-110)^2 = 3240 + 2160 =
5400$; within-segment is $20^2 = 400$; total $5800$; share $5400/5800 \approx
93.1\%$, exactly as Exercise 3 computes. Option A is the *within*-segment share,
which is the part that is hard to attack. Option C is a guess. Option D is
irrelevant: this is a property of the population, not of how much you sampled.

</details>

**Q7.** Which measurement is most robust to a single catastrophic outlier, and
why?

- A) RMSE, because taking the square root at the end undoes the squaring
- B) MAE, because it uses absolute values, which grow linearly rather than quadratically with the error
- C) RMSE, because it is computed from more of the data
- D) The mean of the raw observations, because outliers cancel

<details>
<summary>Answer and explanation</summary>

**B) MAE, because it uses absolute values, which grow linearly rather than
quadratically with the error.**

In the lesson's worked code, one 390 ms error supplies 100.0% of the total squared
error (rounded) but only 99.8% of the total absolute error. Option A is a real property of
RMSE — the square root restores the units — but it does not reduce an outlier's
*share* of the total, since taking the root of a sum preserves the ordering of
contributions. Option C is false; both metrics use the same four numbers. Option
D is wrong because a single outlier does not cancel against anything — it shifts
the mean by a quarter of its own size.

</details>

**Q8.** What happens to the variance when you convert a variable from milliseconds
to seconds by dividing by 1000?

- A) It divides by 1000
- B) It divides by $10^6$, because the transformation squares
- C) It is unchanged
- D) It is not defined once the units change

<details>
<summary>Answer and explanation</summary>

**B) It divides by $10^6$, because the transformation squares.**

$\mathrm{Var}(aX) = a^2\mathrm{Var}(X)$ with $a = 1/1000$, so variance is
multiplied by $10^{-6}$ while the standard deviation is divided by 1000 — the
distinction between variance and standard deviation in one line. Option A
confuses the two, and it is the single most common unit-conversion bug in error
bars. Option C is true only for *adding* a constant, which is why Mistake-style
conversions that shift rather than scale are harmless. Option D is nonsense; a
variance is a variance.

</details>

**Q9.** Why does a mean latency of 50 ms make a poor SLO target?

- A) Because the mean is too hard to compute
- B) Because latency is right-skewed, so the mean is dragged up by the tail and most requests are faster than the mean
- C) Because variance, not mean, is the correct measure of latency
- D) Because the mean of a distribution is always its largest value

<details>
<summary>Answer and explanation</summary>

**B) Because latency is right-skewed, so the mean is dragged up by the tail and
most requests are faster than the mean.**

This is Mistake 4 in this lesson, and it is why percentiles appear in latency
dashboards. Option A is a practical objection, not a mathematical one. Option C
replaces rather than supplements: you want both, and the tail is a quantile
question ([Lesson 65](../part05_probability_statistics/65_continuous_random_variables.md)). Option D is false for
any distribution with more than one value.

</details>

**Q10.** Why is RMSE the right metric when a large error is catastrophic, and
MAE the right one when it is not?

- A) RMSE is always preferred, because it is more sensitive to outliers
- B) RMSE's quadratic weighting makes large errors dominate, which matches a cost that blows up; MAE's linear weighting means a moderate error is as bad as a slightly larger one
- C) MAE is easier to compute
- D) They are interchangeable once you rescale the units

<details>
<summary>Answer and explanation</summary>

**B) RMSE's quadratic weighting makes large errors dominate, which matches a cost
that blows up; MAE's linear weighting means a moderate error is as bad as a
slightly larger one.**

This is the lesson's practical rule, and it follows from the algebra: $E[E^2]$
adds a variance term on top of the squared mean, so large errors get
super-linear weight. Option A states the property without the criterion, which
makes RMSE unconditionally preferable — the opposite of the lesson's advice.
Option C is a computation fact, not a modelling one. Option D is false:
rescaling multiplies both metrics by the same factor, so their *ranking* of
outlier sensitivity never changes.

</details>

## Subjective Questions

### Short Answer

**Q1. State the definition of variance in both forms, and say what the two forms
buy you.**

<details>
<summary>Answer</summary>

$\mathrm{Var}(X) = E[(X-E[X])^2] = E[X^2] - (E[X])^2$. The first form is
conceptually clean — average squared distance from the mean — and is what makes
variance nonnegative by Jensen's inequality. The second is computationally useful
because it avoids computing the mean twice, and it is what lets you get a
variance from data you only summarised. Crucially the square belongs *inside* the
second bracket only: $E[X]^2$ is a different quantity, and writing it that way is
Mistake 1 in this lesson.

</details>

**Q2. Why is $E[X^2] \ge (E[X])^2$, and when does equality hold?**

<details>
<summary>Answer</summary>

Write $\mu = E[X]$. Then $E[X^2] - \mu^2 = E[X^2 - 2\mu X + \mu^2] = E[(X-\mu)^2]
\ge 0$, using linearity of expectation and $E[\mu] = \mu$. The left side is
$\mathrm{Var}(X)$, so the statement is really "variance is nonnegative". Equality
holds exactly when $X$ is constant — $(X-\mu)^2 = 0$ almost surely — because any
nonzero spread makes the squared deviations positive.

</details>

**Q3. State linearity of expectation and name the assumption it does *not*
make.**

<details>
<summary>Answer</summary>

$E[\sum_i a_i X_i] = \sum_i a_i E[X_i]$. It makes **no independence assumption**
at all, for any collection of random variables and any constants $a_i$. This is a
property of the sum, not of the joint distribution: the average of a total is the
total of the averages. Contrast $\mathrm{Var}(\sum_i X_i) = \sum_i
\mathrm{Var}(X_i) + 2\sum_{i<j}\mathrm{Cov}(X_i,X_j)$, which needs pairwise
independence to drop the covariance terms.

</details>

**Q4. Give the two variance formulas for `aX + b` and explain why `b` appears in
one and not the other.**

<details>
<summary>Answer</summary>

Mean: $E[aX+b] = aE[X] + b$. Variance: $\mathrm{Var}(aX+b) = a^2\mathrm{Var}(X)$.
The constant $b$ shifts every value by the same amount, and variance is measured
*from the mean*, which shifts by $b$ too — so the distances are unchanged. The
scale factor $a$ multiplies every distance, and squaring doubles the exponent,
hence $a^2$. This is why "add an offset" leaves error bars untouched while "change
units" divides them by the square of the factor.

</details>

**Q5.** For $S \sim \mathrm{Binomial}(n, p)$, give $\mathrm{Var}(S/n)$.

<details>
<summary>Answer</summary>

$\mathrm{Var}(S) = np(1-p)$, so by $\mathrm{Var}(aX) = a^2\mathrm{Var}(X)$,

$$\mathrm{Var}(S/n) = \frac{np(1-p)}{n^2} = \frac{p(1-p)}{n}.$$

The standard deviation is $\sqrt{p(1-p)/n}$, which falls as $1/\sqrt{n}$ — not
$1/n$. For $p = 0.1$, $n = 10{,}000$: variance $0.0000089$, standard error
$0.003$. This is Mistake 2 in this lesson: reporting $\mathrm{Var}(S)$ instead
would inflate error bars by a factor of $\sqrt{n} = 100$.

</details>

**Q6.** State the law of total variance and name its two terms.

<details>
<summary>Answer</summary>

$\mathrm{Var}(X) = E[\mathrm{Var}(X\mid Y)] + \mathrm{Var}(E[X\mid Y])$. The first
term is the average *within*-group spread; the second is the spread of the group
*means*. The two are uncorrelated by construction, which is why their variances
add rather than interfere. It is the formal statement of "total risk = systematic
+ idiosyncratic risk", and it is what tells you which component is worth
attacking.

</details>

### Long Answer

**Q1. Two systems have the same mean latency. Why can you not conclude they are
equivalent, and what do you need besides the mean?**

<details>
<summary>Model answer</summary>

Because the mean is one number and the behaviour is a distribution. Two systems
can agree on $E[L]$ while differing in everything you actually care about, because
the mean is the *balance point* and is indifferent to how the mass is arranged
around it.

The first thing you need is the variance, or better the standard deviation, since
it is in the units of latency and interpretable. A system with mean 110 ms and sd
20 ms and one with mean 110 ms and sd 76 ms are not interchangeable: the second
has a tail reaching well past 300 ms, and tail latency is what users feel and what
SLOs are written about. Mistake 5 in this lesson makes the decision-theoretic
version of this point — expected value alone is an incomplete decision criterion.

The second thing you need is to know whether the distribution is unimodal at all.
Exercise 3 builds the trap explicitly: 40% of requests at 200 ms ± 20 and 60% at
50 ms ± 20 give a single mean of 110 ms and a single sd of 76 ms, and *nothing in
that summary resembles any real request*. The 110 ms figure sits in the empty gap
between the humps. An engineer optimising "the average toward 110" would be
chasing a value no user ever experiences. The law of total variance diagnoses
this — 93.1% of the variance is between-segment, so the fix is to split traffic by
user type or report per-segment SLOs, not to micro-tune individual requests.

So: mean, then variance, then check for mixtures. Only then is a comparison
meaningful, and only then do percentiles
([Lesson 65](../part05_probability_statistics/65_continuous_random_variables.md)) become the right vocabulary.

</details>

**Q2. Why does linearity of expectation not need independence, and what would
break if you assumed otherwise?**

<details>
<summary>Model answer</summary>

The proof never mentions a joint distribution. Expanding $E[g]$ with
$g(x_1,\dots,x_n) = \sum_i a_i x_i$ and pushing the sum inside gives
$\sum_i a_i \sum_x x_i P(x)$, and the inner sum is the marginal $E[X_i]$ — the
other coordinates simply marginalise out. Nothing in that computation needs
$P(x_1, x_2) = P(x_1)P(x_2)$; it would work identically if the variables were
deterministically identical.

The payoff is computational. Expected cost for a million requests, or the
expected depth of Quicksort, or the expected number of collisions, all reduce to
summing per-item contributions. Exercise 2 of this lesson shows the sharpest
version: with $D_2 = D_1$ (perfect dependence) the mean of the sum is still 7,
computed from marginals alone. What breaks if you assume otherwise is your
ability to decompose problems at all — you'd be forced to construct the joint
distribution of every variable in the system, which is exponential in the number
of variables and completely infeasible.

The trap is that this generosity does *not* extend to the variance. Because
$\mathrm{Var}$ involves $E[X_iX_j]$ cross terms, $\mathrm{Var}(\sum_i X_i) =
\sum_i \mathrm{Var}(X_i) + 2\sum_{i<j}\mathrm{Cov}(X_i,X_j)$, and dropping the
covariance terms requires pairwise independence. Example B shows the cost: with
$\mathrm{Cov}(L_1,L_2) = 0.15$, the correct variance is 1.04 while the
independence answer 0.74 understates the spread by 29%. The mean is safe;
everything else you compute from it is not.

</details>

**Q3. Why does squaring over-weight large values, and what does that mean for
error metrics?**

<details>
<summary>Model answer</summary>

Because $(x + \delta)^2 - x^2 = 2x\delta + \delta^2$, so a perturbation $\delta$ to a
value $x$ has an effect growing *linearly in $x$*. Two equal-sized errors at
different levels are not penalised equally: doubling every observation multiplies
the mean of the squares by 4. In the algebra, this is exactly what
$E[X^2] = \mathrm{Var}(X) + (E[X])^2$ states — squaring adds the variance on top of
the squared mean, and the squared mean dominates when the mean is large relative
to the spread. A latency of 100 ms with sd 10 ms gives $E[L^2] = 10{,}100$, not
10,000.

The practical consequence is that mean square error is dominated by whatever is
worst. In the lesson's worked code, three errors near 10 ms and one at 390 ms
give an MSE of 38,025 where the single outlier is essentially 100% of the total
squared error — yet also 99.8% of the total absolute error, so the *reported*
figures diverge sharply: RMSE = 195.0 ms against MAE = 97.7 ms, a factor of
exactly 2.00. So MSE answers the question
"how badly did the worst thing go?", while MAE answers "how wrong am I typically?".

Neither is universally right, and the choice is about the cost function rather
than the mathematics. When a large error is catastrophic — a dose limit, a load
forecast, a safety margin — the cost really does grow faster than linearly, and
RMSE matches it, with the pleasant side effect that the square root restores the
units. When it is not — search ranking, survey scales, latency SLOs where 400 ms
is bad but not catastrophic — a large error should not outweigh several moderate
ones, so MAE is the right choice. The mathematical statement is invariance: the
*relative* gap between $E[X^2]$ and $(E[X])^2$ is scale-invariant, so switching
units never rescues you from a metric whose weighting is wrong for your problem.

</details>

**Q4. Why does negative dependence *reduce* variance below the independent
prediction, and why might a load balancer rely on that?**

<details>
<summary>Model answer</summary>

The general formula is $\mathrm{Var}(\sum_i X_i) = \sum_i \mathrm{Var}(X_i) + 2\sum_{i<j}\mathrm{Cov}(X_i,X_j)$, so the sign of the pairwise covariance decides the direction. Independence is
covariance zero, and that is the *midpoint*, not the ceiling. Positive dependence —
all-or-nothing failures, as in the lesson's correlated world — gives positive
covariances and inflates the variance (21 against 2.1, a factor of 10). Negative
dependence pushes covariances below zero and deflates it.

The mechanism in a load balancer is that the scheduler coordinates: it knows which
nodes are already handling slow work and routes the next request away from them.
That is not independence — the routes are *jointly determined* — but it is
deliberately anti-correlated, and the total latency is better behaved than
independent routing would give.

This is why "randomly" is not always the best routing policy, and it is the
practical reading of Mistake 3 in this lesson. The trade-off is real, though:
negative dependence can be achieved only by coordinating, which costs
bookkeeping and can fail under load — and when the coordinator's information is
stale you get the worst of both worlds, correlations you did not intend in the
busy regime. So the design goal is not to maximise negative correlation
everywhere but to identify which shared resource actually causes the positive
correlation and remove that, rather than trying to cancel spread downstream.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — hand-compute for a custom PMF.** Let X take values 0, 1, 2,
3 with probabilities 0.1, 0.2, 0.3, 0.4. (a) Verify the PMF is valid. (b) Compute
E[X], E[X²], and Var(X) by the direct definition and by the formula, showing they
agree. (c) Compute the standard deviation and the coefficient of variation. (d)
Compute Y = 3X + 5 and give its mean, variance, and standard deviation.

<details>
<summary>Solution</summary>

(a) All values non-negative and 0.1 + 0.2 + 0.3 + 0.4 = 1.0 ✓

(b) Direct:
    E[X] = 0(0.1) + 1(0.2) + 2(0.3) + 3(0.4) = 0 + 0.2 + 0.6 + 1.2 = 2.0
    E[X²] = 0(0.1) + 1(0.2) + 4(0.3) + 9(0.4) = 0 + 0.2 + 1.2 + 3.6 = 5.0
    Var = Σ(x − 2)²p(x) = 4(0.1) + 1(0.2) + 0(0.3) + 1(0.4) = 0.4 + 0.2 + 0 + 0.4 = 1.0

Formula:
    Var = E[X²] − (E[X])² = 5.0 − 4.0 = 1.0 ✓

Both routes give 1.0, and the gap between E[X²] = 5 and (E[X])² = 4 is exactly
the variance.

(c) σ = √1.0 = 1.0. The coefficient of variation is σ/μ = 1.0/2.0 = 0.5, or 50%
relative spread.

(d) Mean: 3(2.0) + 5 = 11. Variance: 3² × 1.0 = 9, so σ = 3. Note the mean
adds the constant but the variance ignores it entirely — shifting a variable
moves it without changing its spread.

```python
from math import sqrt

pmf = {0: 0.1, 1: 0.2, 2: 0.3, 3: 0.4}
support = sorted(pmf)

print(f"(a) all non-negative: {all(p >= 0 for p in pmf.values())}, "
      f"sums to 1: {sum(pmf.values()) == 1.0}")

mean = sum(x * pmf[x] for x in support)
second = sum(x**2 * pmf[x] for x in support)
var_direct = sum((x - mean) ** 2 * pmf[x] for x in support)
var_formula = second - mean**2

print(f"(b) E[X]   = {mean:.6f}")
print(f"    E[X^2] = {second:.6f}   (E[X])^2 = {mean**2:.6f}")
print(f"    Var direct = {var_direct:.6f}, Var formula = {var_formula:.6f}, "
      f"agree: {abs(var_direct - var_formula) < 1e-12}")
print(f"(c) sd = {sqrt(var_formula):.6f}, "
      f"coefficient of variation = {sqrt(var_formula) / mean:.6f}")

a, b = 3, 5
print(f"(d) Y = {a}X + {b}: mean = {a * mean + b:.6f}, "
      f"var = {a**2 * var_formula:.6f}, sd = {sqrt(a**2 * var_formula):.6f}")
```

The constant b contributes 0 to the variance. That is not a quirk, it is the
definition: spread is measured *from the mean*, so translating the distribution
cannot change it.

</details>

**[ ] Exercise 2 — linearity without independence, done exactly.** Two dice are
rolled. Let D₁ and D₂ be the two face values, and S = D₁ + D₂.

(a) Compute E[D₁], E[D₂] and hence E[S] using only the marginal distributions,
without ever computing P(D₁ = a, D₂ = b) for a ≠ b.

(b) Now compute E[S²] from the marginals alone and show it does **not** equal
(E[S])². Then compute Var(S) two ways.

(c) Finally, make the dice fully dependent: let D₂ = D₁ (the same die read
twice). Recompute E[S] and Var(S), and comment on what changed.

<details>
<summary>Solution</summary>

(a) Each die is uniform on {1,…,6}, so E[Dᵢ] = (1+2+3+4+5+6)/6 = 3.5. By
linearity, E[S] = E[D₁] + E[D₂] = 7. **No joint distribution was used** — we
never needed to know whether the dice are independent, loaded, or correlated.

(b) E[S²] = E[(D₁+D₂)²] = E[D₁²] + 2E[D₁D₂] + E[D₂²]. The first and last terms
come from the marginals: E[Dᵢ²] = (1+4+9+16+25+36)/6 = 91/6 ≈ 15.1667. The middle
term E[D₁D₂] is a **joint** moment, so it cannot be obtained from marginals alone:
for independent dice it is 3.5 × 3.5 = 12.25, and for identical dice it is
E[D²] = 91/6 ≈ 15.1667.

With independent dice:
    E[S²] = 15.1667 + 24.5 + 15.1667 = 54.8333
    (E[S])² = 49
    Var(S) = 54.8333 − 49 = 5.8333  = 2 × Var(D) = 2 × (35/12) ✓

(c) With D₂ = D₁, S = 2D₁, so:
    E[S] = 2 × 3.5 = 7            <- unchanged, by linearity
    Var(S) = 4 × Var(D) = 4 × 2.9167 = 11.6667   <- nearly DOUBLE

The mean is untouched at 7 in both worlds. The variance rose from 5.83 to 11.67,
almost exactly doubled, because the correlation between the dice contributes the
covariance term 2Cov(D₁,D₂). For identical dice Cov = Var(D) = 2.9167.

This is the cleanest possible demonstration of the asymmetry: **the expectation
genuinely does not care about dependence, and the variance genuinely does.**

```python
from math import sqrt

faces = [1, 2, 3, 4, 5, 6]
n = len(faces)
mean_d = sum(faces) / n
second_d = sum(x**2 for x in faces) / n
var_d = second_d - mean_d**2

print(f"E[D] = {mean_d:.6f}   E[D^2] = {second_d:.6f}   Var(D) = {var_d:.6f}")

# (a) linearity, marginals only
print(f"(a) E[S] = E[D1] + E[D2] = {mean_d + mean_d:.6f}  "
      f"(no joint distribution needed)")

# (b) independent dice
cov_independent = 0.0
mean_s = 2 * mean_d
second_s = 2 * second_d + 2 * (mean_d * mean_d + cov_independent)
var_s_indep = second_s - mean_s**2
print(f"(b) independent: E[S^2] = {second_s:.6f}, (E[S])^2 = {mean_s**2:.6f}")
print(f"    Var(S) = {var_s_indep:.6f}  (check 2*Var(D) = {2 * var_d:.6f})")

# (c) identical dice: D2 = D1
cov_identical = var_d
second_s_dep = 2 * second_d + 2 * (mean_d * mean_d + cov_identical)
var_s_dep = second_s_dep - mean_s**2
print(f"(c) identical:   Cov(D1,D2) = {cov_identical:.6f}")
print(f"    Var(S) = {var_s_dep:.6f}  sd = {sqrt(var_s_dep):.6f}")
print(f"    vs independent Var(S) = {var_s_indep:.6f}  "
      f"sd = {sqrt(var_s_indep):.6f}")
print()
print(f"E[S] identical: {mean_s:.6f}  <- unchanged")
print(f"variance ratio: {var_s_dep / var_s_indep:.4f}x")
```

</details>

**[ ] Exercise 3 — Challenge: total variance decomposition.** Suppose customers
are split into two segments, "power users" (40%, mean latency 200 ms) and "casual
users" (60%, mean latency 50 ms). Within each segment, latency has standard
deviation 20 ms.

(a) Compute E[latency]. (b) Compute Var(latency) using the total variance
formula. (c) Compute the between-segment variance Var(E[L | segment]) and the
within-segment average E[Var(L | segment)]. (d) What fraction of the total
variance is between-segment, and what does that imply for where you would invest
in optimisation effort? (e) If you merged the two segments into one report and
reported only the overall standard deviation, what misleading impression would
you create?

<details>
<summary>Solution</summary>

(a) E[L] = 0.4(200) + 0.6(50) = 80 + 30 = 110 ms.

(b) Total variance: Var(L) = E[Var(L|seg)] + Var(E[L|seg]).
Within-segment variance is 20² = 400 for both, so E[Var(L|seg)] = 400.
The segment means are 200 and 50 with weights 0.4 and 0.6, so

    Var(E[L|seg]) = 0.4(200 − 110)² + 0.6(50 − 110)²
                 = 0.4(8100) + 0.6(3600)
                 = 3240 + 2160 = 5400

Var(L) = 400 + 5400 = 5800, so σ = √5800 ≈ 76.16 ms.

(c) Between-segment = 5400, within-segment = 400. Total 5800. ✓

(d) Between-segment share = 5400/5800 ≈ 93.1%. Almost all the variance is
*structural* — it comes from who the customers are, not from noise in
measurement. The practical implication is sharp: tuning the within-segment
system (where variance is 400, sd 20 ms) can at best shrink total variance from
5800 to 5400, a 7% improvement in σ. Splitting traffic by user type, or
per-segment SLOs, attacks the 93%. This decomposition is the formal basis of
"variance decomposition" in A/B test analysis and in Simpson's paradox.

(e) A single overall sd of 76 ms implies the whole population is spread over
roughly 110 ± 76, which suggests that *every* request has a latency somewhere in
the 34 to 186 ms band with comparable likelihood. The truth is a mixture of two
populations at 200 and 50 with tight spreads. Reporting one sd hides the fact that
the distribution is bimodal: the 50 ms requests are extremely reliable and the
200 ms requests are also reasonably reliable, and nothing happens near 110 ms.
An engineer who "fixed" the average toward 110 ms would have been working on a
number that no user actually experiences.

```python
from math import sqrt, exp

SEGMENTS = {
    "power":  {"p": 0.4, "mean": 200.0, "sd": 20.0},
    "casual": {"p": 0.6, "mean": 50.0,  "sd": 20.0},
}

# (a) overall mean
mean_l = sum(s["p"] * s["mean"] for s in SEGMENTS.values())
print(f"(a) E[L] = 0.4*200 + 0.6*50 = {mean_l:.2f} ms")

# (c) between-segment variance of the conditional means, and within-segment
between = sum(s["p"] * (s["mean"] - mean_l) ** 2 for s in SEGMENTS.values())
within = sum(s["p"] * s["sd"] ** 2 for s in SEGMENTS.values())
total = between + within

# (b) total variance
print(f"(b) Var(E[L|seg]) = 0.4*(200-110)^2 + 0.6*(50-110)^2 = {between:.2f}")
print(f"    E[Var(L|seg)] = {within:.2f}  (sd 20 in BOTH segments)")
print(f"    Var(L)        = {between:.2f} + {within:.2f} = {total:.2f}   "
      f"sd = {sqrt(total):.2f} ms")

# (d) how much of the spread is structural?
floor_sd = sqrt(between)
print(f"(d) between-segment share = {between / total * 100:.1f}%")
print(f"    within-segment share  = {within / total * 100:.1f}%")
print(f"    if within-segment noise were removed entirely, sd would fall")
print(f"    from {sqrt(total):.2f} ms to {floor_sd:.2f} ms -- a "
      f"{(1 - floor_sd / sqrt(total)) * 100:.1f}% improvement.")
print("    So per-request tuning is nearly pointless here; splitting traffic")
print("    by segment (or reporting per-segment SLOs) attacks the other 93%.")

# (e) where the probability mass actually is -- two tight humps, nothing between
print()
print("(e) Approximate density of the mixture:")
lo, hi = 0.0, 260.0
buckets = 26
width = (hi - lo) / buckets
grid = [0.0] * buckets
for name, s in SEGMENTS.items():
    sd = s["sd"]
    for i in range(buckets):
        centre = lo + (i + 0.5) * width
        z = (centre - s["mean"]) / sd
        # normal density factor 1/(sd*sqrt(2*pi)), precomputed as 2.5066
        grid[i] += s["p"] * exp(-0.5 * z * z) / (sd * 2.5066282746310002)

for i, v in enumerate(grid):
    if v > 0.0005:
        bar = "#" * int(round(v * 600))
        print(f"  {lo + i * width:5.0f}-{lo + (i + 1) * width:5.0f} ms "
              f"{int(round(v * 600)):3d} {bar}")

print()
print(f"The mean {mean_l:.0f} ms sits in the EMPTY gap between the humps,")
print("so it describes almost no real request. One sd of "
      f"{sqrt(total):.0f} ms")
print("implies a spread that the data does not contain -- the distribution")
print("is bimodal, and reporting a single mean and sd hides that.")
```
The takeaway generalises past latency: whenever you have a mixture of populations,
always report the segments as well as the aggregate, and use the variance
decomposition to find out which of the two numbers is worth attacking.

</details>

**[ ] Exercise 4 — `E[X²]` versus `(E[X])²`, and the units trap.** A system
measures the latency of three requests: 10 ms, 10.5 ms, and 400 ms.
(a) Compute the mean latency and the mean of the squares.
(b) Compute `(E[L])²` and the variance, and show that the gap between the two
quantities in (a) is exactly the variance.
(c) Report the RMSE and the MAE, and say which one describes a "typical" request.
(d) Convert the same measurements to seconds, and verify that the variance is
divided by `10⁶` while the standard deviation is divided by 1000.

<details>
<summary>Solution</summary>

(a) Mean latency: $E[L] = (10 + 10.5 + 400)/3 = 420.5/3 = 140.1667$ ms.
Mean of the squares: $E[L^2] = (100 + 110.25 + 160000)/3 = 160210.25/3 =
53403.4167$ ms².

(b) $(E[L])^2 = 140.1667^2 = 19646.6944$ ms², so

$$\mathrm{Var}(L) = E[L^2] - (E[L])^2 = 53403.4167 - 19646.6944 = 33756.7222\ \text{ms}^2,$$

which is exactly the gap between the two numbers in (a). Now the instructive part:
the third measurement contributes $160000/3 = 53333.33$ out of the total second
moment of $53403.42$, a share of **99.87%**. Essentially all of the mean of
squares comes from one request. That is the whole lesson in a single number —
squaring re-weights large values, so the mean of squares is a report on the worst
case rather than on typical behaviour.

(c) Three distinct numbers, and it is worth keeping them apart:

- standard deviation of $L$ itself: $\sigma = \sqrt{33756.7222} = 183.73$ ms
- RMSE against the true value of 10 ms: $\sqrt{(0^2 + 0.5^2 + 390^2)/3} =
\sqrt{50700.0833} = 225.17$ ms
- MAE against the same true value: $(0 + 0.5 + 390)/3 = 130.17$ ms

Neither error metric describes a "typical" request well, but MAE at least keeps
the two fast requests visible, whereas RMSE has all but forgotten them: RMSE is
1.73× MAE, and RMSE − MAE $= 95$ ms is almost entirely the outlier's penalty. For
"typical" you want percentiles
([Lesson 65](../part05_probability_statistics/65_continuous_random_variables.md)); RMSE is justified only when a
large error is catastrophic.

(d) In seconds the measurements are 0.010, 0.0105, 0.400. The variance becomes
$33756.7222 / 10^6 = 0.0337567$ s² and the standard deviation becomes
$\sqrt{0.0337567} = 0.18373$ s $= 183.73$ ms. So the variance is divided by
$10^6$ — because $\mathrm{Var}(aX) = a^2\mathrm{Var}(X)$ with $a = 1/1000$ — while
the standard deviation is merely divided by 1000. Dividing the variance by 1000
instead would overstate the spread by a factor of 1000, which is the practical
form of Mistake 1: variance is in squared units and transforms quadratically.

```python
from math import sqrt

observations = [10.0, 10.5, 400.0]
true_value = 10.0

mean_l = sum(observations) / len(observations)
second = sum(o**2 for o in observations) / len(observations)
squared_mean = mean_l ** 2
var_l = second - squared_mean

errors = [o - true_value for o in observations]
mae = sum(abs(e) for e in errors) / len(errors)
rmse = sqrt(sum(e**2 for e in errors) / len(errors))

print(f"(a) E[L]    = {mean_l:.4f} ms")
print(f"    E[L^2]  = {second:.4f} ms^2")
print()
print(f"(b) (E[L])^2 = {squared_mean:.4f} ms^2")
print(f"    Var(L)   = {second:.4f} - {squared_mean:.4f} = {var_l:.4f} ms^2")
print(f"    the gap in (a) IS the variance: {abs((second - squared_mean) - var_l) < 1e-6}")
worst_share = (observations[-1] ** 2 / len(observations)) / second
print(f"    the single {observations[-1]:.0f} ms request supplies "
      f"{worst_share * 100:.2f}% of E[L^2]")

print()
print(f"(c) sd(L) = {sqrt(var_l):.4f} ms")
print(f"    RMSE (vs true {true_value} ms) = {rmse:.4f} ms")
print(f"    MAE  (vs true {true_value} ms) = {mae:.4f} ms")
print(f"    RMSE/MAE = {rmse / mae:.2f}")

in_seconds = [o / 1000 for o in observations]
mean_s = sum(in_seconds) / len(in_seconds)
second_s = sum(o**2 for o in in_seconds) / len(in_seconds)
var_s = second_s - mean_s ** 2
print()
print(f"(d) mean {mean_l:.4f} ms -> {mean_s:.6f} s   (divided by "
      f"{mean_l / mean_s:.0f})")
print(f"    var  {var_l:.4f} ms^2 -> {var_s:.6f} s^2   (divided by "
      f"{var_l / var_s:.0f})")
print(f"    sd   {sqrt(var_l):.4f} ms -> {sqrt(var_s):.6f} s   (divided by "
      f"{sqrt(var_l) / sqrt(var_s):.0f})")
print(f"    check Var/10^6 = {var_l / 1e6:.6f}, matches: {abs(var_s - var_l / 1e6) < 1e-9}")
```

</details>

**[ ] Exercise 5 — variance of a sum with a known dependency.** A pipeline makes
4 database calls. Each call costs 1 unit, plus 1 extra unit if the cache is cold.
Call 1 has a 0.5 chance of being cold; if call 1 was cold then call 2 has a 0.9
chance of being cold; if call 1 was warm then call 2 has a 0.1 chance of being
cold; calls 3 and 4 are cold with probability 0.5 independently of everything. Let
$C$ be the total cost and $I_1,\dots,I_4$ the cold indicators.
(a) Confirm every indicator has marginal 0.5, then compute $E[C]$ by linearity
without ever computing a joint probability.
(b) Compute $\mathrm{Var}(I_i)$ for each $i$.
(c) Compute $\mathrm{Cov}(I_1,I_2)$ from $P(I_1=1,I_2=1) = 0.5 \times 0.9 = 0.45$,
and explain why every other covariance is zero.
(d) Compute $\mathrm{Var}(C)$ and compare with the answer you would get by wrongly
assuming independence.

<details>
<summary>Solution</summary>

(a) **Check the marginal of $I_2$:**
$P(I_2 = 1) = P(I_1=1)P(I_2=1\mid I_1=1) + P(I_1=0)P(I_2=1\mid I_1=0) =
0.5(0.9) + 0.5(0.1) = 0.45 + 0.05 = 0.50$. ✓ So all four marginals are 0.5.

By linearity,
$E[C] = 4 + E[I_1] + E[I_2] + E[I_3] + E[I_4] = 4 + 4(0.5) = 6$.
We never used $P(I_1=1,I_2=1) = 0.45$. That number is *not needed for the mean* —
it is exactly the point of linearity of expectation, and it is why Example B's mean
was 4.6 in both the dependent and independent worlds.

(b) Each $I_i$ is Bernoulli(0.5), so $\mathrm{Var}(I_i) = 0.5 \times 0.5 = 0.25$
for all four. Sum of variances $= 1.00$.

(c) $\mathrm{Cov}(I_1,I_2) = P(I_1=1,I_2=1) - P(I_1=1)P(I_2=1) = 0.45 - 0.25 =
+0.20$. Every other covariance is zero because those indicators are independent
*by construction*: $I_3$ and $I_4$ were generated with fresh randomness that knows
nothing about the first two, so knowing $I_1$ gives no information about them.

(d) $\mathrm{Var}(C) = \sum \mathrm{Var}(I_i) + 2\sum_{i<j}\mathrm{Cov} = 1.00 +
2(0.20) = 1.40$, so $\sigma = \sqrt{1.40} = 1.1832$.

Assuming independence would give $\mathrm{Var}(C) = 1.00$ and $\sigma = 1.0000$,
understating the standard deviation by 15.5%. The covariance term contributes
$0.40/1.40 = 28.6\%$ of the true variance. Meanwhile the mean is 6 in both worlds.
The 2σ band under the correct model is $[3.63,\ 8.37]$ rather than $[4.00, 8.00]$,
so the independence model promises a tighter range than the mechanism can deliver
— which is precisely the failure mode of Mistake 3 in this lesson.

```python
from math import sqrt

P = [0.5, 0.5, 0.5, 0.5]          # marginal cold probabilities
joint_12 = 0.5 * 0.9              # P(I1 = 1 and I2 = 1)

# (a) verify the marginal of I2 by the law of total probability
cond_warm = 0.1                  # P(I2 = 1 | I1 = 0), chosen so the marginal is 0.5
marginal_2 = P[0] * 0.9 + (1 - P[0]) * cond_warm
print(f"(a) marginal of I2 = {P[0]}*0.9 + {1 - P[0]}*{cond_warm} "
      f"= {marginal_2:.4f}  (intended 0.5)")
mean_c = len(P) + sum(P)
print(f"    E[C] = {len(P)} + sum of marginals = {mean_c:.4f}")
print("    -> the joint probability 0.45 was never needed")

# (b)
var_parts = sum(p * (1 - p) for p in P)
print()
print(f"(b) Var(I_i) = {[round(p * (1 - p), 4) for p in P]}, sum = {var_parts:.4f}")

# (c)
cov_12 = joint_12 - P[0] * P[1]
print()
print(f"(c) Cov(I1,I2) = {joint_12} - {P[0]}*{P[1]} = {cov_12:+.4f}")
print("    all other covariances are 0 (independent by construction)")

# (d)
var_correct = var_parts + 2 * cov_12
var_naive = var_parts
sd_correct, sd_naive = sqrt(var_correct), sqrt(var_naive)
print()
print(f"(d) Var(C) correct = {var_correct:.4f}, sd = {sd_correct:.4f}")
print(f"    Var(C) assuming independence = {var_naive:.4f}, sd = {sd_naive:.4f}")
print(f"    sd understated by {(1 - sd_naive / sd_correct) * 100:.1f}%")
print(f"    the covariance term is {2 * cov_12 / var_correct * 100:.1f}% of the true variance")
print(f"    E[C] = {mean_c:.4f} either way -- linearity needs no assumption")
print(f"    2 sd band: correct [{mean_c - 2 * sd_correct:.2f}, "
      f"{mean_c + 2 * sd_correct:.2f}] vs "
      f"naive [{mean_c - 2 * sd_naive:.2f}, {mean_c + 2 * sd_naive:.2f}]")
```

</details>

**[ ] Exercise 6 — Challenge: the standard error falls as 1/√n, which is why A/B
tests are expensive.** An A/B test has $n$ users per arm, each converting
independently with probability $p = 0.08$.
(a) Compute $\mathrm{Var}(\hat p) = \mathrm{Var}(S/n)$ and the standard error for
$n = 100$, $1{,}000$, and $10{,}000$.
(b) Find the sample size per arm needed for the standard error to reach 0.005 and
0.0025, and comment on the ratio.
(c) The two arms differ by 1 percentage point (0.08 versus 0.09). Express that gap
in units of the standard error of the *difference* between two independent arms,
for each $n$ in (a), and find the smallest $n$ at which the gap is at least 2
standard errors.
(d) Use the $1/\sqrt{n}$ law to show why a 0.5 percentage point improvement is out
of reach for a reasonable experiment.

<details>
<summary>Solution</summary>

(a) $S \sim \mathrm{Binomial}(n,p)$, so by $\mathrm{Var}(aX) = a^2\mathrm{Var}(X)$,
$\mathrm{Var}(\hat p) = \mathrm{Var}(S/n) = \frac{np(1-p)}{n^2} =
\frac{p(1-p)}{n}$, and $\sigma_{\hat p} = \sqrt{\frac{p(1-p)}{n}}$. With
$p(1-p) = 0.08 \times 0.92 = 0.0736$:

| $n$ | $\mathrm{Var}(\hat p)$ | $\sigma_{\hat p}$ |
| --- | --- | --- |
| 100 | 0.000736 | 0.02713 |
| 1,000 | 0.0000736 | 0.00858 |
| 10,000 | 0.00000736 | 0.00271 |

Note the variance falls by exactly 10× when $n$ rises 10×, and the standard error
by only $\sqrt{10} \approx 3.16×$.

(b) Solve $n = \frac{p(1-p)}{\sigma'^2}$:
for $\sigma' = 0.005$, $n = 0.0736/0.000025 = 2{,}944$ per arm;
for $\sigma' = 0.0025$, $n = 0.0736/0.00000625 = 11{,}776$ per arm.
The ratio is exactly 4: **halving the standard error costs four times the
users**, because the standard error falls like $1/\sqrt{n}$.

(c) For two independent arms, $\mathrm{Var}(\hat p_1 - \hat p_2) =
\mathrm{Var}(\hat p_1) + \mathrm{Var}(\hat p_2) = \frac{2p(1-p)}{n}$, so
$\sigma_{\text{diff}} = \sqrt{2}\,\sigma_{\hat p}$. The observed gap is 0.01:

| $n$ | $\sigma_{\text{diff}}$ | gap / $\sigma_{\text{diff}}$ |
| --- | --- | --- |
| 100 | 0.03837 | 0.26 |
| 1,000 | 0.01213 | 0.82 |
| 10,000 | 0.00384 | 2.61 |

For a 2-standard-error threshold, $n \ge \frac{2p(1-p) \cdot 4}{0.01^2} =
\frac{8 \times 0.0736}{0.0001} = 5{,}888$ per arm. At $n = 10{,}000$ the gap is
2.61 standard errors and the effect is detectable; at $n = 1{,}000$ it is 0.82
standard errors, which is unremarkable day-to-day noise.

(d) Detecting a gap $\delta$ requires $n \ge 2p(1-p)(z/\delta)^2$ per arm, so
$n \propto 1/\delta^2$:

- $\delta = 0.01$: $n \ge 2(0.0736)(2/0.01)^2 = 5{,}888$ per arm
- $\delta = 0.005$: $n \ge 2(0.0736)(2/0.005)^2 = 23{,}552$ per arm (47,104 total)
- $\delta = 0.0025$: $n \ge 94{,}208$ per arm (188,416 total)

Each halving of the effect costs 4× the traffic, so a 0.5 percentage point win is
not merely hard to detect — it is quadratic-expensive. A tenfold increase in
traffic only buys a 3.16× reduction in the standard error, which is nowhere near
enough. This is why teams pre-register large-effect experiments, report
underpowered results as inconclusive rather than negative, and are tempted by
sequential designs that peek and stop early — a temptation worth resisting,
because each peek inflates the false-positive rate ([Lesson
69](../part05_probability_statistics/69_estimation_and_hypothesis_testing.md)).

```python
from math import sqrt

p = 0.08
print(f"p(1-p) = {p * (1 - p):.4f}")
print()
print("(a)")
print(f"{'n':>8} | Var(S/n) | sd(S/n)")
for n in (100, 1_000, 10_000):
    var = p * (1 - p) / n
    print(f"{n:8,} | {var:.8f} | {sqrt(var):.5f}")

print()
print("(b)")
for target in (0.005, 0.0025):
    print(f"  target sd {target:.4f} -> n = {p * (1 - p) / target ** 2:.0f} per arm")

print()
print("(c) gap = 0.01 between two independent arms; sd_diff = sqrt(2) * sd(S/n)")
GAP = 0.01
for n in (100, 1_000, 10_000):
    sd_diff = sqrt(2 * p * (1 - p) / n)
    print(f"  n = {n:6,}  sd_diff = {sd_diff:.5f}   gap/sd = {GAP / sd_diff:.2f}")
n_needed = 2 * p * (1 - p) * (2 / GAP) ** 2
print(f"  n for gap >= 2 sd: {n_needed:.0f} per arm ({2 * n_needed:.0f} total)")

print()
print("(d) sample size per arm scales as 1/delta^2")
for delta in (0.01, 0.005, 0.0025):
    n_arm = 2 * p * (1 - p) * (2 / delta) ** 2
    print(f"  delta = {delta:.4f} -> {n_arm:,.0f} per arm, {2 * n_arm:,.0f} total")
```

</details>

## Summary

- E[X] = Σ x·p_X(x) is a probability-weighted average, and E[g(X)] applies a
  function then averages.
- E[X²] ≥ (E[X])² always, with equality only for a constant variable; the gap is
  exactly Var(X) by definition.
- Var(X) = E[X²] − (E[X])², σ = √Var, both in the units of X.
- Linearity of expectation, E[ΣaᵢXᵢ] = ΣaᵢE[Xᵢ], requires **no independence** and
  is the most-used theorem in the subject.
- Var(ΣXᵢ) = ΣVar(Xᵢ) + 2ΣCov(Xᵢ,Xⱼ) does require independence; the covariance
  terms are what dependencies add.
- The asymmetry between those two is the practical lesson: means are robust to
  unmodelled dependencies, spread is not.
- Total variance splits spread into within-group and between-group components,
  which tells you which one is worth attacking.
- Scaling by a constant multiplies σ by |a|; adding a constant leaves σ
  unchanged, which is why variance is defined around the mean.

## Next

[65 — Continuous Random Variables](../part05_probability_statistics/65_continuous_random_variables.md) replaces
the PMF with a density, explains why a density can exceed 1, and introduces the
uniform, exponential (with its memoryless property), and normal distributions
including the 68-95-99.7 rule.