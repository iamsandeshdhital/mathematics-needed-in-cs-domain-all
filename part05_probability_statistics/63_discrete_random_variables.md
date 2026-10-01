# 63 — Discrete Random Variables

**Part**: part05_probability_statistics · **Prerequisites**: 62 · **Time**: 35 min

---

## In Plain Words

So far every question has been about events: things that either happened or did
not. But most of the time you care about a *number*. How many retries. How many
milliseconds. How many successes out of a thousand. That number is not known in
advance, and that is exactly what a random variable is: a function from outcomes
to numbers.

The point of wrapping the number in a function is that you stop reasoning about
events and start reasoning about a distribution — a table saying how likely each
value is. Once you have that table, everything about the variable follows. The
probability it equals some value. The probability it is at most some value,
which is the cumulative distribution and turns out to be the genuinely useful
one for engineering. The average value it will settle on. And whether it holds
the same value repeatedly, which turns out to be the cleanest decomposition of
any discrete variable you will ever find.

This lesson builds that machinery and then spends most of its time on two
distributions that genuinely appear everywhere: the Bernoulli trial (one coin
flip, one yes/no outcome) and the Binomial (count successes in a fixed number of
trials).

## Why Computer Science Cares

- **Everything stochastic in a program is a random variable.** A retry count, a
  queue depth, a cache hit count, the number of edges a graph search explores.
  Naming the variable makes the distribution arguable.
- **A/B test conversion.** "Did the user sign up" is Bernoulli with p equal to
  the conversion rate; "how many of 10,000 users signed up" is Binomial with
  n = 10,000. The variance of that count decides whether the result is real
  ([Lesson 64](../part05_probability_statistics/64_expectation_variance.md)).
- **Binomial CIs.** Every standard error formula for a proportion, and the
  normal-approximation p-value, is derived from the Binomial
  ([Lesson 69](../part05_probability_statistics/69_estimation_and_hypothesis_testing.md)).
- **Tail-latency modelling.** Whether a request takes 1 ms or 2 ms is Bernoulli;
  the count of slow requests in a batch is Binomial.
- **Interviews.** "If p = 0.1, what is the chance of at least 3 successes in 5
  trials?" is a standard warm-up and separates people who have internalised the
  PMF from people who have memorised one formula.

## The Formal Version

**Definition.** A *random variable* is a function X: Ω → ℝ that assigns a real
number to every outcome. The experiment is fixed; X is a lens on it.

This definition is worth sitting with, because it means a random variable has no
extra randomness of its own. All the uncertainty came from Ω. Two different
lenses on the same sample space are perfectly legitimate: from two dice you could
take X = sum of faces, or Y = |difference|, and both are random variables.

**Definition.** The *probability mass function* (PMF) of a discrete random
variable X is the function

    p_X(x) = P(X = x)

for each real x. Two properties define it completely:

1. p_X(x) ≥ 0 for all x
2. Σ_x p_X(x) = 1, where the sum runs over the distinct values X can take

The PMF is exactly the probability mass table: the list of possible values with
their probabilities. Once you have it, everything else is arithmetic on it.

**Definition.** The *cumulative distribution function* (CDF) is

    F_X(x) = P(X ≤ x) = Σ_{t ≤ x} p_X(t)

Two properties worth knowing:

- F is non-decreasing, and P(X = x) = F(x) − F(x⁻), the jump at x. The PMF is
  recovered from the CDF as a difference of left limits.
- F(x) = 1 for all sufficiently large x, and the right limit F(x⁺) = P(X ≤ x) is
  what you use for integer-valued variables where you may want P(X < x).

Engineers often prefer the CDF because it answers the question you actually ask:
"what fraction of results are at most 200 milliseconds?" is F(200), whereas the
PMF answers "what fraction are exactly 200 milliseconds?", which is almost never
the question.

**Definition.** Two random variables X and Y are **independent** if for all
x, y, p_{X,Y}(x, y) = p_X(x)·p_Y(y) — knowing X tells you nothing about Y.

**Theorem (every discrete variable is a sum of Bernoullis).** Let X be a
discrete random variable taking values in {0, 1, …, n}. Define indicator
variables

    Iₖ = 1 if X ≥ k, for k = 1, 2, …, n, and 0 otherwise.

Then

    X = I₁ + I₂ + ⋯ + Iₙ   and   E[X] = Σₖ P(X ≥ k)

**Proof.** For any outcome, if X = 3 then precisely I₁, I₂, I₃ are 1 and the rest
are 0, so the sum equals 3 = X. Summing probabilities over outcomes gives the
expectation identity, which is linearity of expectation
([Lesson 64](../part05_probability_statistics/64_expectation_variance.md)).  ∎

This is sometimes called the tail-sum formula, and it is a genuine piece of
mathematical engineering: **every discrete distribution can be built from
one-point distributions.** It is why a Bernoulli is the only primitive you need,
and it is the conceptual bridge from Bernoulli to Binomial.

### The Bernoulli distribution

**Definition.** X is *Bernoulli(p)* — written X ~ Bernoulli(p) — when

    P(X = 1) = p,   P(X = 0) = 1 − p

for a parameter p ∈ [0, 1]. It models one trial with two outcomes, and only
those two.

Its mean and variance (proved in [Lesson 64](../part05_probability_statistics/64_expectation_variance.md)) are

    E[X] = p        Var(X) = p(1 − p)

**Theorem.** If X₁, …, Xₙ are independent Bernoulli(p) and
S = X₁ + ⋯ + Xₙ, then S ~ Binomial(n, p).

**Explanation.** S takes values in {0, …, n}, and

    P(S = k) = C(n, k) pᵏ (1 − p)ⁿ⁻ᵏ

To see this, "exactly k successes" means choosing which k of the n trials
succeed (C(n,k) ways, from
[Lesson 21](../part02_discrete_combinatorics/21_permutations_and_combinations.md)),
each such assignment has probability pᵏ(1−p)ⁿ⁻ᵏ by independence, and the
assignments are disjoint. The combinatorial object is a *subset* of size k of an
n-element set, which is why the counting machinery of Part 02 reappears here
verbatim.

### The Binomial distribution

**Definition.** S ~ Binomial(n, p) when

    P(S = k) = C(n,k) pᵏ (1−p)ⁿ⁻ᵏ,  for k = 0, 1, …, n

and 0 otherwise. The mean and variance are

    E[S] = np        Var(S) = np(1 − p)

Both follow from the tail-sum / indicator argument: S = ΣXᵢ, so E[S] = ΣE[Xᵢ] = np
by linearity, and Var(S) = ΣVar(Xᵢ) = np(1−p) by independence.

The mean is the count you would expect, np, and the standard deviation
√(np(1−p)) is the spread around it. These two numbers determine everything
practical — [Lesson 68](../part05_probability_statistics/68_law_of_large_numbers_and_clt.md) shows that for large
np the shape is approximately normal, so these two alone predict the tail
probabilities.

## Worked Example

### Example A — the full PMF of Binomial(10, 0.3)

Let S count successes in 10 independent trials with p = 0.3. Compute the whole
PMF, then the CDF at a few points.

**Step 1 — write the formula.** P(S=k) = C(10,k) · 0.3ᵏ · 0.7^(10−k).

**Step 2 — compute each row.** Doing k = 0 and k = 1 by hand to check the method:

    k=0: C(10,0) · 0.3⁰ · 0.7¹⁰ = 1 · 1 · 0.0282475249 = 0.028248
    k=1: C(10,1) · 0.3¹ · 0.7⁹  = 10 · 0.3 · 0.040353607 = 0.121061
    k=2: C(10,2) · 0.3² · 0.7⁸  = 45 · 0.09 · 0.057648010 = 0.233474
    k=3: C(10,3) · 0.3³ · 0.7⁷  = 120 · 0.027 · 0.082354300 = 0.266828
    k=4: C(10,4) · 0.3⁴ · 0.7⁶  = 210 · 0.0081 · 0.117649000 = 0.200121
    k=5: C(10,5) · 0.3⁵ · 0.7⁵  = 252 · 0.00243 · 0.168070000 = 0.102919
    k=6: C(10,6) · 0.3⁶ · 0.7⁴  = 210 · 0.000729 · 0.240100000 = 0.036757
    k=7: C(10,7) · 0.3⁷ · 0.7³  = 120 · 0.0002187 · 0.343000000 = 0.009002
    k=8: C(10,8) · 0.3⁸ · 0.7²  = 45 · 0.00006561 · 0.490000000 = 0.001447
    k=9: C(10,9) · 0.3⁹ · 0.7¹   = 10 · 0.000019683 · 0.700000000 = 0.000138
    k=10: C(10,10) · 0.3¹⁰ · 0.7⁰ = 1 · 0.0000059049 = 0.000006

**Step 3 — sanity checks.**

- The probabilities sum to 1 (the code prints 1.0000000000). ✓ A PMF that does
  not sum to 1 is a bug.
- The mode (most likely value) is 3, and the mean np = 10 × 0.3 = 3. For a
  Binomial the mode is floor((n+1)p) = floor(3.3) = 3. Mean and mode agree here
  because the distribution is close to symmetric.
- The shape is unimodal and right-skewed: there is a tail out to 10 but nothing
  below 0. Asymmetry is the norm for a count variable with a hard lower bound.
- The standard deviation is √(np(1−p)) = √(10 · 0.3 · 0.7) = √2.1 ≈ 1.4491.

**Step 4 — the CDF.** Summing upward:

    F(0) = 0.028248
    F(1) = 0.149308
    F(2) = 0.382783
    F(3) = 0.649611
    F(4) = 0.849732
    F(5) = 0.952651

So P(S ≤ 5) = 0.952651, and by the complement rule P(S ≥ 6) = 0.047349.
Engineers care about that number: "6 or more successes out of 10" happens about
4.7% of the time.

**Step 5 — a question you will actually be asked.** P(at least 3) =
1 − P(0) − P(1) − P(2) = 1 − 0.382783 = 0.617217. Note that computing this
needs three PMF values and the complement rule, *not* a special formula. This is
the general strategy: PMF values plus the complement rule, always.

### Example B — the tail-sum formula on a hand-built variable

Take the space of two coin flips, Ω = {HH, HT, TH, TT}, each with probability 1/4.
Define X = number of heads.

**The PMF** follows from counting: P(X=0) = 1/4 (TT), P(X=1) = 2/4 (HT, TH),
P(X=2) = 1/4 (HH). Note P(X=1) = 0.5 while each individual outcome is 0.25 —
one value of X can collect probability from several outcomes. This is exactly why
the PMF is a function on *values*, not on outcomes.

**The CDF** is F(0) = 0.25, F(1) = 0.75, F(2) = 1.

**The tail-sum formula.** Define I₁ = 1 if X ≥ 1, I₂ = 1 if X ≥ 2. Check the
decomposition:

| outcome | X | I₁ | I₂ | I₁ + I₂ |
| --- | --- | --- | --- | --- |
| HH | 2 | 1 | 1 | 2 ✓ |
| HT | 1 | 1 | 0 | 1 ✓ |
| TH | 1 | 1 | 0 | 1 ✓ |
| TT | 0 | 0 | 0 | 0 ✓ |

So X = I₁ + I₂ on every outcome. Since I₁ is Bernoulli(0.75) and I₂ is
Bernoulli(0.25),

    E[X] = E[I₁] + E[I₂] = 0.75 + 0.25 = 1

which agrees with 2 × 0.5 = 1. Two routes, one answer. The tail-sum route is the
useful one because it generalises: **E[X] = Σₖ P(X ≥ k)** says the mean is the sum
of the survival probabilities, which is how you compute an expectation when the
support is huge and the PMF is impractical.

### Example C — a Bernoulli is a coin flip, and its mean is the parameter

X ~ Bernoulli(0.25). Enumerate a long run and watch the average settle.

Over 4 flips, "success" happens with probability 0.25 per flip. The average of
the indicator values over many flips should approach 0.25 — which is p. This is
the whole content of the claim E[X] = p for a Bernoulli, and it is also the law
of large numbers ([Lesson 68](../part05_probability_statistics/68_law_of_large_numbers_and_clt.md)) in its
smallest form.

For a fair coin (p = 0.5), the sample average of 20 flips is 0.5 only in
expectation. The standard deviation of that average is
√(p(1−p)/n) = √(0.25/20) ≈ 0.1118, so a run of 20 flips landing at 14 heads
(0.7) sits about 1.79 standard deviations above the mean — unusual, not shocking.
This is precisely the arithmetic behind "coin flips are random", and it is why
someone who sees 14 heads out of 20 and declares the coin rigged is usually
reasoning about the wrong distribution.

## Runnable Code

### A random variable as a function, and its PMF

```python
from itertools import product
from collections import Counter

# The sample space: two fair coin flips, four equally likely outcomes.
outcomes = list(product(["H", "T"], repeat=2))
omega_prob = 1 / len(outcomes)

# A random variable is just a FUNCTION on the sample space.
# X = number of heads.
def number_of_heads(outcome):
    return outcome.count("H")


print("outcome | X | P(X=x) | F(X<=x)")
for o in sorted(outcomes, key=number_of_heads):
    x = number_of_heads(o)
    print(f"{str(o):7s} | {x} | {omega_prob:.6f}   (see CDF below)")

# The PMF groups outcomes that produce the SAME value.
pmf = Counter({x: 0 for x in range(3)})
for o in outcomes:
    pmf[number_of_heads(o)] += omega_prob

print()
print("PMF (the probability mass table):")
for x in sorted(pmf):
    print(f"  P(X = {x}) = {pmf[x]:.6f}")
print(f"  sum      = {sum(pmf.values()):.6f}  <- must be exactly 1")

# The CDF is the running sum.
cdf = {}
running = 0.0
for x in sorted(pmf):
    running += pmf[x]
    cdf[x] = running
print()
print("CDF (running total):")
for x in sorted(cdf):
    print(f"  F({x}) = P(X <= {x}) = {cdf[x]:.6f}")

# Recover the PMF from jumps in the CDF -- and note the discrete subtlety.
print()
print("Recovering the PMF from CDF jumps: F(x) - F(x-1) = P(X = x)")
for x in sorted(cdf):
    prev = cdf[x - 1] if x - 1 in cdf else 0.0
    print(f"  {cdf[x]:.6f} - {prev:.6f} = {cdf[x] - prev:.6f}  = P(X = {x})")
```

### The tail-sum decomposition, checked on every outcome

```python
from itertools import product

outcomes = list(product([0, 1], repeat=4))  # four Bernoulli trials

# X = number of successes. I_k = indicator of the event X >= k.
def x_of(o):
    return sum(o)


def indicators(o, n):
    """The n indicator variables I_1..I_n for this one outcome."""
    return [1 if x_of(o) >= k else 0 for k in range(1, n + 1)]


n = 4
total_outcomes = len(outcomes)
print("outcome | X | I_1 I_2 I_3 I_4 | sum of indicators | match")
for o in sorted(outcomes, key=x_of):
    x = x_of(o)
    inds = indicators(o, n)
    print(f"{str(o):7s} | {x} | {' '.join(map(str, inds))}   | "
          f"{sum(inds):16d} | {sum(inds) == x}")

# Tail-sum: E[X] = sum_k P(X >= k). With n fair coins all outcomes are
# equally likely, so P(X >= k) is just the count of outcomes reaching k
# divided by the total.
print()
print("The identity X = I_1 + ... + I_n holds on EVERY outcome, so:")
tail_terms = [
    sum(1 for o in outcomes if x_of(o) >= k) / total_outcomes
    for k in range(1, n + 1)
]
print("  P(X >= k) for k = 1..n :", [f"{t:.4f}" for t in tail_terms])
print("  E[X] = sum of those    =", f"{sum(tail_terms):.6f}")
print("  E[X] = n * p           =", n * 0.5)
print("  agree:",
      abs(sum(tail_terms) - n * 0.5) < 1e-12)
```

### Bernoulli and Binomial, side by side

```python
from math import comb, factorial


def bernoulli_pmf(x, p):
    """P(X = x) for X ~ Bernoulli(p)."""
    if x not in (0, 1):
        return 0.0
    return p if x == 1 else 1.0 - p


def binomial_pmf(k, n, p):
    """P(S = k) for S ~ Binomial(n, p), written in terms of factorials
    exactly as the definition states it."""
    if not 0 <= k <= n:
        return 0.0
    # C(n, k) p^k (1-p)^(n-k)
    return comb(n, k) * p**k * (1 - p) ** (n - k)


# E[X] = p for a Bernoulli -- verify by summing the PMF times the values.
p = 0.25
mean_bernoulli = sum(x * bernoulli_pmf(x, p) for x in (0, 1))
print(f"Bernoulli(p={p}):")
print(f"  PMF:  P(X=0) = {bernoulli_pmf(0, p):.6f}   P(X=1) = {bernoulli_pmf(1, p):.6f}")
print(f"  E[X] = 0*{bernoulli_pmf(0, p):.4f} + 1*{bernoulli_pmf(1, p):.4f}"
      f" = {mean_bernoulli:.6f}")
print(f"  ... which equals the parameter p = {p} exactly.")
print()

# The Binomial(n, p) row that is an average of n Bernoulli rows.
n = 10
print(f"Binomial(n={n}, p={p}) -- full PMF:")
print("  k | count | P(S=k)      | F(S<=k)  | cumulative check")
total = 0.0
cdf = 0.0
for k in range(n + 1):
    pk = binomial_pmf(k, n, p)
    total += pk
    cdf += pk
    print(f"{k:2d} | {comb(n, k):5d} | {pk:.6f}  | {cdf:.6f}  | total={total:.6f}")

print()
print(f"sum of PMF      = {total:.10f}   (must be 1)")
print(f"E[S] = n*p      = {n * p:.6f}")
print(f"Var(S) = np(1-p)= {n * p * (1 - p):.6f}")
print(f"sd(S)           = {(n * p * (1 - p)) ** 0.5:.6f}")

# The Binomial is a sum of Bernoullis -- check the equivalence numerically.
import random

rng = random.Random(4242)
trials = 200_000
counts = [0] * (n + 1)
for _ in range(trials):
    successes = sum(1 for _ in range(n) if rng.random() < p)
    counts[successes] += 1

print()
print(f"Simulating {trials} runs of {n} Bernoulli({p}) trials:")
print("  k | simulated   exact")
for k in range(n + 1):
    print(f"{k:2d} | {counts[k] / trials:.6f}  {binomial_pmf(k, n, p):.6f}")
```

### Estimating p by counting successes — the MLE, introduced informally

```python
import random

# The whole reason Binomial matters: given n observations, we want p.
# The natural estimate is the observed success rate, and it IS the maximum
# likelihood estimate (proved in Lesson 69).
rng = random.Random(7)

true_p = 0.25
n = 20
trials = 100_000
counts = [0] * (n + 1)
for _ in range(trials):
    counts[sum(1 for _ in range(n) if rng.random() < true_p)] += 1

# Which observed proportion is most frequent? That is the mode of Binomial.
mode_k = max(range(n + 1), key=lambda k: counts[k])
print(f"true p = {true_p}, n = {n}, {trials} simulated experiments")
print(f"most frequent number of successes: {mode_k} -> p_hat = {mode_k / n:.4f}")
print(f"close to the true value: {abs(mode_k / n - true_p) < 0.05}")

# The distribution of the estimate, which is what confidence intervals use.
print()
print("  k | P(k successes)  | p_hat = k/n")
for k in range(n + 1):
    print(f"{k:3d} | {counts[k] / trials:13.6f}  | {k / n:.4f}")

import math
sd_of_phat = math.sqrt(true_p * (1 - true_p) / n)
print()
print(f"standard deviation of p_hat = sqrt(p(1-p)/n) = {sd_of_phat:.6f}")
print(f"so p_hat within 2 sd covers roughly "
      f"[{true_p - 2 * sd_of_phat:.4f}, {true_p + 2 * sd_of_phat:.4f}]")
```

## Common Mistakes

**Mistake 1 — treating the PMF as if it were a CDF.**
Wrong: "P(X = 200ms) is 0.03, so 3% of requests take 200ms." That is true but
useless. For a latency distribution you want P(X ≤ 200) = F(200), which
accumulates every value up to the threshold. The temptation is that the PMF is
the definition you learn first, and its entries are easy to compute one at a
time; the CDF requires a running sum.

**Mistake 2 — expecting the mean of a skewed distribution to be the mode.**
Wrong: "The most likely value of S ~ Binomial(10, 0.3) is 3, so the average must
be 3." Here they happen to nearly agree (np = 3, mode = 3), which is exactly why
the mistake survives. Try n = 10, p = 0.1: the mean is 1 but the mode is 0, and
more than 34% of the time the count is exactly zero. Mean is the balance point;
mode is the peak. They coincide only for symmetric distributions.

**Mistake 3 — using the mean as if it were an outcome.**
Wrong: "E[S] = 3, so we expect exactly 3 successes." In any single run of 10
trials with p = 0.3, the count is 3 with probability 0.2668 and is something
else with probability 0.7332. The mean is not a prediction of any particular run;
it is the long-run average. Variance is what tells you how wrong you can be, and
skipping it is why people are surprised by bad runs.

**Mistake 4 — confusing the number of trials with the probability.**
Wrong: "n = 1000 means p = 0.9." n sets how many trials you run; p is the
per-trial success probability. The mean np = 900 is a product of both, which is
where the confusion comes from — the two numbers get tangled precisely because
they multiply in the mean.

**Mistake 5 — assuming independence is implied by "repeating" something.**
Wrong: "We retried the flaky request 5 times, so it's Binomial(5, p)." Only if
the retries are independent. Retries against a struggling dependency are
positively correlated — the thing that failed once will fail again — so the count
has *more* variance than Binomial predicts. State the independence assumption
whenever you write down a Binomial, and check whether the mechanism deserves it.

## Formula Sheet

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$X$` | `$X : \Omega \to \mathbb{R}$` | A **random variable** is a function from outcomes to numbers. It adds no randomness of its own — it is a lens on a fixed sample space. | Whenever you name the quantity whose value is uncertain: retries, queue depth, cache hits. |
| `$p_X(x)$` | `$p_X(x) = P(X = x)$` | **PMF**, the probability mass function: the exact mass on one value. | Point probabilities. One value can collect mass from many outcomes — that is why the PMF lives on *values*, not outcomes. |
| PMF conditions | `$p_X(x) \ge 0$` and `$\sum_x p_X(x) = 1$` | Nonnegative, and the total mass is exactly 1. The sum runs over the **distinct values X can take**, not over all reals. | The cheapest bug check there is: a PMF that does not sum to 1 is wrong. |
| `$F_X(x)$` | `$F_X(x) = P(X \le x) = \sum_{t \le x} p_X(t)$` | **CDF**, the cumulative distribution: everything up to and including $x$. | Threshold questions — "what fraction of requests are at most 200 ms". Engineers reach for this far more than the PMF. |
| `$F_X(x) - F_X(x^-)$` | `$= p_X(x)$` | The PMF is the jump in the CDF at $x$. | Recovering the PMF from a CDF you already have. Needs the left limit, since F is flat across gaps. |
| `$F(x^+)$` | `$= P(X \le x)$`, and `$F(x^-) = P(X < x)$` | Left and right limits. | Distinguishing "$P(X < x)$" from "$P(X \le x)$" on integer-valued variables. |
| `$X \perp Y$` | `$p_{X,Y}(x,y) = p_X(x)\,p_Y(y)$` | **Independence**: knowing X tells you nothing about Y. | Must be argued from the mechanism. Binomial and sum-of-Bernoullis both require it. |
| `$I_k$` | `$I_k = 1$ if `$X \ge k$`, else $0$ | An **indicator variable** — a Bernoulli(·) that fires when $X$ reaches level $k$. | Decomposing any count variable into one-point pieces. |
| tail-sum formula | `$X = I_1 + \cdots + I_n$` and `$E[X] = \sum_{k=1}^{n} P(X \ge k)$` | Every discrete count is a sum of indicators, so the mean is the sum of the survival probabilities. | When the support is huge and the full PMF impractical. Bridges Bernoulli to Binomial. |
| `p` | `$p \in [0, 1]$` | The Bernoulli (and Binomial) success parameter. Per trial, **not** the expected count. | Setting `p` is a modelling decision about the mechanism. |
| `p_X` (Bernoulli) | `$P(X = 1) = p`, `$P(X = 0) = 1 - p$` | One trial, two outcomes. The only primitive you need. | One yes/no outcome: one request, one cache hit, one conversion. |
| `E[X]` (Bernoulli) | `$= p$` | The mean equals the parameter. | Sanity check that your sample average should converge to $p$. |
| `Var(X)` (Bernoulli) | `$= p(1-p)$` | Spread of a single trial; maximal at $p = 0.5$, zero at the ends. | Converting a count's spread into a proportion's spread. |
| `n` | `$n \in \{0, 1, 2, \dots\}$`, a non-negative integer | The **number of independent trials**. Fixed, not random, not the success rate. | Any Binomial or sum-of-Bernoullis. "n = 1000" says nothing about $p$. |
| `k` | `$k \in \{0, 1, \dots, n\}$` | The number of successes counted. | Every Binomial PMF query; $P(S=k) = 0$ outside $\{0,\dots,n\}$. |
| `$S \sim \mathrm{Binomial}(n,p)$` | `$P(S=k) = \binom{n}{k} p^k (1-p)^{n-k}$`, needs **`0 \le p \le 1`** and **`n` a non-negative integer** | Count of successes in $n$ **independent** trials each succeeding with probability $p$. | Conversions in a fixed-size sample, cache hits in a batch, failures in a window. |
| `E[S]` (Binomial) | `$= np$` | The expected count. Often not an achievable outcome — for $n=8, p=0.4$ it is 3.2. | Capacity planning. Not a prediction for one run. |
| `Var(S)` (Binomial) | `$= np(1-p)$` | Spread of the count. From independence plus $\operatorname{Var}(X_1 + \cdots + X_n) = \sum \operatorname{Var}(X_i)$. | Every standard error for a proportion ([Lesson 68](../part05_probability_statistics/68_law_of_large_numbers_and_clt.md)). |
| `sd(S)` | `$\sqrt{np(1-p)}$` | The spread in original units. | "Typically between 29 and 51" out of an expected 40. |
| `mode` (Binomial) | `$\lfloor (n+1)p \rfloor$` | The peak. Equals the mean only for symmetric distributions. | The single most likely count, which is usually not the expected count for small $np$. |
| `$\binom{n}{k}$` | `$= \dfrac{n!}{k!\,(n-k)!}$` | Choosing which $k$ of the $n$ trials succeeded. | The combinatorial reason the Binomial exists; needs the counting of [Lesson 21](../part02_discrete_combinatorics/21_permutations_and_combinations.md). |
| `$\hat{p}$` | `$= k/n$`, the observed success rate | The maximum likelihood estimate of $p$ from $k$ successes in $n$ trials. | A/B tests. Its spread is $\sqrt{p(1-p)/n}$, which is what confidence intervals use. |
| `f_n(A)` vs `p_X(x)` | — | A frequency is what you *observed*; a PMF is what the model *says*. They should agree, and the gap is sampling error. | Load tests and dashboards. Lesson 68 turns their convergence into a theorem. |

## Multiple Choice Questions

**Q1.** A cache serves requests independently with a 0.8 hit rate. What is the
distribution of the number of cache misses in 1,000 requests?

- A) Poisson(800), since hits and misses are independent and numerous
- B) Binomial(1000, 0.2), with mean 20 and standard deviation ≈ 4.43
- C) Binomial(1000, 0.8), with mean 800
- D) Binomial(200, 0.2), because misses trigger retries

<details>
<summary>Answer and explanation</summary>

**B) Binomial(1000, 0.2), with mean 20 and standard deviation ≈ 4.43.**

$n = 1000$ fixed trials, $p = 0.2$ miss rate, independence given — that *is* the
definition of Binomial. Mean $= 1000 \times 0.2 = 20$; variance $= 1000 \times
0.2 \times 0.8 = 160$, so $sd = \sqrt{160} \approx 4.43$. Option A imports a
different distribution (introduced in
[Lesson 66](../part05_probability_statistics/66_common_distributions.md)) for a count that has a hard bound of
1000. Option C flips $p$ — hits are $p = 0.8$, misses are $p = 0.2$ — giving the
right shape with the wrong mean, which is Mistake 4 in this lesson. Option D
confuses the miss count with the retry structure from Exercise 3; retries would
make it 2,000 trials, but there is no retry in this question.

</details>

**Q2.** For $S \sim \mathrm{Binomial}(10, 0.3)$, what is the most likely value of
$S$, and how does it relate to the mean?

- A) 3, which equals $np = 3$ because the distribution is nearly symmetric here
- B) 1, because small counts are the common case for low $p$
- C) 5, because the PMF is right-skewed so the peak sits above the mean
- D) There is no single most likely value, because the PMF never peaks

<details>
<summary>Answer and explanation</summary>

**A) 3, which equals $np = 3$ because the distribution is nearly symmetric here.**

Mode $= \lfloor(n+1)p \rfloor = \lfloor 11 \times 0.3 \rfloor = \lfloor 3.3
\rfloor = 3$, and $P(S=3) = 0.266828$ is the largest entry in the worked
example's table. Option B is wrong here because $P(S=1) = 0.121061$ is far
smaller. Option C gets the skew direction right in principle (a right-skewed
distribution has mean above mode, not below) but the wrong conclusion. Option D
is contradicted by the worked example's own table.

</details>

**Q3.** For $S \sim \mathrm{Binomial}(10, 0.1)$, the mean is 1. What fraction of
the time is the count exactly zero?

- A) About 35%
- B) About 10%, since that is the per-trial failure rate
- C) Exactly 0.9, because a mean of 1 means most runs have nothing
- D) About 65%

<details>
<summary>Answer and explanation</summary>

**A) About 35%.**

$P(S=0) = \binom{10}{0} 0.1^0 \cdot 0.9^{10} = 0.348678$, matching the "more than
34%" figure in Mistake 2. Option B is the base rate per *trial* applied to the
whole experiment — with 10 trials the chance every one misses is $0.9^{10}$, not
$0.1$. Option C confuses the mean with a probability at all: $E[S] = 1$ does not
mean "most runs have nothing". Option D is the complement $1 - 0.348678 =
0.651322$, i.e. the chance of **at least one** success — the mirror-image error.

</details>

**Q4.** What does $E[S] = 3$ mean for a single run of 10 trials with $p = 0.3$?

- A) The run will produce exactly 3 successes
- B) The count is 3 with probability 0.2668, and something else with probability 0.7332; 3 is the long-run average
- C) At least 3 of the 10 trials will succeed
- D) The most likely outcome is 3, so 3 is guaranteed by the mode

<details>
<summary>Answer and explanation</summary>

**B) The count is 3 with probability 0.2668, and something else with probability
0.7332; 3 is the long-run average.**

This is Mistake 3 in this lesson. Option A treats the mean as an outcome, which is
exactly the reasoning that makes people surprised by bad runs. Option C is a
strictly stronger claim than the mean makes — $P(S \ge 3) = 0.6172$, so you are
wrong about "at least 3" in 38% of runs, not in a negligible fraction. Option D
conflates mode with certainty; even the peak of the PMF carries only 27% of the
mass.

</details>

**Q5.** Which statement about the PMF and the CDF is correct?

- A) $P(X = 200\text{ ms}) = 0.03$ tells you 3% of requests take exactly 200 ms, which is what a latency SLO needs
- B) $F(200) = 0.97$ tells you 97% of requests take at most 200 ms, which is what a latency SLO needs
- C) Both are equally useful, since one is the density and one the integral
- D) The PMF and the CDF of the same variable have different normalisations

<details>
<summary>Answer and explanation</summary>

**B) $F(200) = 0.97$ tells you 97% of requests take at most 200 ms, which is what
a latency SLO needs.**

A threshold question is a cumulative question; that is Mistake 1 in this lesson.
The PMF statement in option A is true but nearly useless, because no SLO is
written about one exact millisecond. Option C is wrong because the CDF is a
running sum *of* the PMF — they are the same information in two arrangements, not
two different quantities. Option D is false: both are probabilities and both sum
to 1 over the support.

</details>

**Q6.** Why does the lesson say every discrete variable is a sum of Bernoulli
variables?

- A) Because every discrete distribution is, by definition, a mixture of two-point distributions
- B) Because $X = \sum_k 1[X \ge k]$ holds on every outcome, so one-point pieces suffice for both the law and the mean
- C) Because the Binomial is defined as the sum of $n$ Bernoullis and nothing else is discrete
- D) Because indicators are independent whenever $X$ is

<details>
<summary>Answer and explanation</summary>

**B) Because $X = \sum_k 1[X \ge k]$ holds on every outcome, so one-point pieces
suffice for both the law and the mean.**

If $X = 3$ then exactly $I_1, I_2, I_3$ are 1, so the sum reproduces $X$ on
every outcome — the worked example tabulates this for two flips. Option A
overstates it: the pieces are *deterministic functions* of $X$, not a genuine
mixture with free randomness. Option C is false; the Bernoulli is the primitive
for counts, not for all discrete distributions (a loaded die is discrete too, and
is not a fair Bernoulli). Option D is false: the indicators are strongly
*dependent* — if $I_4 = 1$ then $I_3 = 1$ — which is precisely why the
expectation identity needs no independence but the Binomial formula does.

</details>

**Q7.** Two requests are sent to the same struggling database. Each times out with
probability 0.1, but a timeout affects both. Is `P(both time out)` equal to
$0.1 \times 0.1 = 0.01$?

- A) Yes, because timeouts are rare
- B) No, because sharing a dependency makes the events positively correlated, so the joint probability is greater than the product
- C) No, because the second timeout is impossible after the first
- D) Yes, as long as both requests were sent within the same second

<details>
<summary>Answer and explanation</summary>

**B) No, because sharing a dependency makes the events positively correlated, so
the joint probability is greater than the product.**

Positive dependence means the timeout events overlap more than independence
allows, so the union is *smaller* and the intersection *larger* than the
independent figures. Option A is a non-sequitur — rarity has nothing to do with
independence. Option C is wrong in kind: conditioning on the first timeout makes
the second *more* likely, not impossible. Option D introduces a time window
where none was given, and conflates simultaneous with independent.

</details>

**Q8.** In the worked example, why does $P(X = 1) = 0.5$ while each of the
outcomes HT and TH has probability 0.25?

- A) It cannot; one of those probabilities must be wrong
- B) Because the PMF is a function on values, and two outcomes map to the same value 1
- C) Because $P(X = 1)$ should be 0.25 by linearity
- D) Because the two coin flips are dependent

<details>
<summary>Answer and explanation</summary>

**B) Because the PMF is a function on values, and two outcomes map to the same
value 1.**

$X$ is a function $\Omega \to \mathbb{R}$, so several outcomes can share one
value, and $p_X(1) = P(\{HT, TH\}) = 0.25 + 0.25 = 0.5$. Option A misses the
distinction the whole lesson is built on. Option C applies linearity to a
probability rather than an expectation. Option D is false — the flips are
independent, which is exactly why the two outcomes each have probability 1/4.

</details>

**Q9.** An A/B test with 10,000 users per variant sees 1,000 conversions in
variant A. What is the natural estimate of $p$, and what is the standard
deviation of that estimate?

- A) $\hat p = 0.1$, with standard deviation $\sqrt{0.1 \cdot 0.9 / 10{,}000} \approx 0.003$
- B) $\hat p = 1000$, with standard deviation 30
- C) $\hat p = 10$, with standard deviation 3
- D) $\hat p = 0.001$, with standard deviation 0.00003

<details>
<summary>Answer and explanation</summary>

**A) $\hat p = 0.1$, with standard deviation $\sqrt{0.1 \cdot 0.9 / 10{,}000}
\approx 0.003$.**

$\hat p = k/n = 1000/10{,}000 = 0.1$, and the spread of a proportion follows from
the Binomial variance divided by $n^2$: $\sqrt{np(1-p)}/n = \sqrt{p(1-p)/n}$.
Option B is the count and its spread ($np = 1000$, $\sqrt{np(1-p)} = 30$) left
unconverted. Option C divides by 100 twice. Option D is off by a factor of 100 in
the estimate — the reciprocal error. Note how small the standard error is: that is
why an A/B test needs thousands of users, and why the whole machinery of
[Lesson 69](../part05_probability_statistics/69_estimation_and_hypothesis_testing.md) is needed to say whether a
difference this size is real.

</details>

**Q10.** A variable takes values in $\{0, 1, \dots, n\}$ and its CDF has a flat
step at $x = 2$. What does that tell you?

- A) The variance is zero
- B) $P(X = 2) = 0$ — there is a gap in the support, so $F(2) = F(2^-)$
- C) The mean is at most 2
- D) The variable is continuous rather than discrete

<details>
<summary>Answer and explanation</summary>

**B) $P(X = 2) = 0$ — there is a gap in the support, so $F(2) = F(2^-)$.**

Since $p_X(2) = F(2) - F(2^-)$, a flat step means zero mass at that value.
Exercise 2 of this lesson builds exactly such a distribution (mass at 0, 1 and 3)
and prints `F(1) == F(2)`. Option A is unrelated — a gap in the support says
nothing about spread. Option C confuses a support gap with a mean bound. Option D
is backwards: flat steps are a *discrete* signature, and a continuous CDF is flat
almost everywhere.

</details>

## Subjective Questions

### Short Answer

**Q1. Define a random variable, and say what a random variable does *not*
introduce.**

<details>
<summary>Answer</summary>

A random variable is a function $X : \Omega \to \mathbb{R}$ assigning a real
number to each outcome. It introduces no randomness of its own — all the
uncertainty came from $\Omega$. Two different lenses on the same sample space are
equally valid: from two dice you could take the sum or the absolute difference,
and both are random variables on the same experiment. This is why naming the
variable matters: it is a claim about *which* number you care about, not a new
source of noise.

</details>

**Q2. State the two conditions that make a function a valid PMF, and say what
the summation is over.**

<details>
<summary>Answer</summary>

$p_X(x) = P(X = x)$ is a valid PMF when (1) $p_X(x) \ge 0$ for all $x$, and (2)
$\sum_x p_X(x) = 1$. The sum in (2) runs over the **distinct values $X$ can
take**, not over all reals — for $S \sim \mathrm{Binomial}(10, 0.3)$ that means
$k = 0, 1, \dots, 10$ and nothing else. Summing over all reals would give the
same total but is not what the notation means; summing over the wrong support is
a classic source of a PMF that "does not sum to 1".

</details>

**Q3. How do you recover the PMF from a CDF you already have?**

<details>
<summary>Answer</summary>

By differencing: $p_X(x) = F_X(x) - F_X(x^-)$, where $F_X(x^-) = \lim_{t \uparrow
x} F_X(t)$ is the left limit. You need the left limit rather than $F_X(x-1)$
because the CDF is flat across gaps in the support — for the distribution with
mass at 0, 1 and 3, $F(1) = F(2) = 0.8$, so $F(2) - F(1) = 0$ correctly reports
$P(X = 2) = 0$. Equivalently, for integer-valued $X$, $F(x^+) = P(X \le x)$ and
$F(x^-) = P(X < x)$, and the jump is the mass at $x$.

</details>

**Q4.** A variable counts the number of retries a request needed. Its PMF puts
0.5 on 0, 0.3 on 1, and 0.2 on 3. Is it a valid PMF, and what is its mean?

<details>
<summary>Answer</summary>

It is valid: all values are nonnegative and $0.5 + 0.3 + 0.2 = 1$. The mean is
$E[X] = 0 \cdot 0.5 + 1 \cdot 0.3 + 3 \cdot 0.2 = 0.9$. Note there is no mass at
2, which is fine — a support need not be contiguous. This is exactly the
distribution in Exercise 2.

</details>

**Q5.** For $S \sim \mathrm{Binomial}(n, p)$, give the mean, the variance, the
standard deviation, and the mode.

<details>
<summary>Answer</summary>

Mean $E[S] = np$. Variance $\operatorname{Var}(S) = np(1-p)$, requiring the
$n$ trials to be independent. Standard deviation $\sigma = \sqrt{np(1-p)}$. Mode
$\lfloor (n+1)p \rfloor$. The mean is often not an achievable value at all — for
$\mathrm{Binomial}(8, 0.4)$ it is 3.2 — which is the cleanest demonstration that a
mean is a summary and not a prediction.

</details>

**Q6.** State the tail-sum formula and give one situation where it is the better
tool than the full PMF.

<details>
<summary>Answer</summary>

$E[X] = \sum_{k \ge 1} P(X \ge k)$, following from the decomposition $X =
\sum_{k=1}^{n} I_k$ with $I_k = 1[X \ge k]$. It is the better tool when the
support is enormous: it needs only survival probabilities $P(X \ge k)$, not the
mass at each value. That is why monitoring dashboards compute "fraction of
requests at or above threshold" rather than materialising a histogram over every
possible value.

</details>

### Long Answer

**Q1. Why does the Binomial PMF need the independence assumption, while the
tail-sum identity $E[X] = \sum_k P(X \ge k)$ does not?**

<details>
<summary>Model answer</summary>

The two formulas compute different things, and only one of them is a probability
about a joint event. The Binomial PMF asserts $P(S = k) = \binom{n}{k} p^k
(1-p)^{n-k}$, which counts outcomes: choose which $k$ of the $n$ trials
succeeded, and each such assignment must have probability $p^k (1-p)^{n-k}$. That
factorisation is exactly the independence assumption — if the trials were
correlated, the $\binom{n}{k}$ assignments would *not* all carry the same
probability, and some joint pattern would be more likely than $p^k(1-p)^{n-k}$.

The tail-sum identity does not factorise anything. It says $X = I_1 + I_2 +
\cdots + I_n$ where each $I_k$ is a deterministic function of $X$, and then takes
expectations. Linearity of expectation holds for *any* collection of random
variables, dependent or not, so no hypothesis is consumed. The proof in the
lesson is one line per outcome: if $X = 3$ then exactly $I_1, I_2, I_3$ are 1.

The engineering consequence is that the indicators $I_k$ are strongly *negatively*
dependent by construction — $I_4 = 1$ forces $I_3 = 1$ — and this lesson shows
that case in a table, while the $X_i$ in the Binomial are assumed independent.
Both claims survive their respective proofs precisely because they make different
demands. That is also why a sum-of-Bernoullis model with correlated trials (the
retry case in Mistake 5) still has a well-defined mean $np$ but a *wrong* variance:
the expectation only ever needed linearity.

</details>

**Q2. A mean of 3 and a most likely value of 3 look like the same fact. Why are
they different, and what breaks when you confuse them?**

<details>
<summary>Model answer</summary>

The mean is a balance point: the value that would make the sum of deviations
zero. The mode is the peak of the PMF: the single most likely value. They coincide
for symmetric distributions and diverge as soon as the distribution is skewed,
which is the normal case for a count with a hard bound at 0. For
$\mathrm{Binomial}(10, 0.1)$ the mean is 1 while $P(S = 0) = 0.3487$ exceeds
$P(S = 1) = 0.3874$… barely, but the more striking case is
$\mathrm{Binomial}(10, 0.05)$, where the mean is 0.5, the mode is 0, and $P(S=0) =
0.5987$ — a typical run produces *nothing at all*.

The confusion survives in $\mathrm{Binomial}(10, 0.3)$ precisely because there the
mean, the mode and the value 3 all coincide. So a system tuned to "we expect 3
retries" that is actually running at $p = 0.05$ will see zero retries most of the
time and mistake that for an improvement.

What breaks concretely: capacity sizing that budgets for the mean gets 0 retries
of the 10 the budget implies, so a per-retry cost model is right on average and
wrong on the day; alerting that fires when the count differs from the mode fires
constantly, because 36% of runs give exactly 0; and quantile-based reasoning
collapses, since the mean carries no information about the tail. The lesson's own
advice follows from this: use the mean and the standard deviation
$\sqrt{np(1-p)}$ to reason about spread, and the CDF to reason about tails, never
the mode.

</details>

**Q3. Why does a retry count have more variance than
$\mathrm{Binomial}(5, p)$ predicts, and what does that do to an alert threshold?**

<details>
<summary>Model answer</summary>

The Binomial assumes the $n$ trials are independent, and retries against the same
dependency are not. If the first attempt fails because the connection pool is
exhausted, the retry hits the same exhausted pool, so the second failure is *more*
likely than $p$, not equally likely. Positive dependence means the failure
indicators overlap more than independence permits: the count clusters near 0 and
near 5 with less in between than the Binomial allows.

Variance responds to this directly. For a sum of identically distributed
indicators, $\operatorname{Var}(\sum X_i) = \sum \operatorname{Var}(X_i) + 2\sum_{i<j}
\operatorname{Cov}(X_i, X_j)$, and independence is exactly what kills the
covariance terms. With positive correlation those terms are positive, so the true
variance exceeds $np(1-p)$.

What this does to a threshold depends on which error you care about. Because
clustering puts extra mass at the extremes, a threshold set at the 99th percentile
of the Binomial model is crossed *more* often than 1% of the time — the model
understates the tail exactly where tails are the point. So the alert fires too
often, and the team learns to ignore it. The fix is not to lower the threshold
indefinitely but to fix the model: either make the retries genuinely independent
(jittered backoff, randomised routing to a different replica), or replace the
Binomial with a correlated-count model such as a beta-binomial. This is Mistake 5
in this lesson, and it is the most common way a correct-looking distribution
produces a wrong SLO.

</details>

**Q4. Why does an A/B test need thousands of users per variant, when a
conversion rate is "just" 10%?**

<details>
<summary>Model answer</summary>

Because the spread of an estimate falls like $1/\sqrt{n}$, not like $1/n$. With
$k$ successes out of $n$ trials, the count has variance $np(1-p)$ by the Binomial,
and dividing by $n^2$ to get a proportion gives standard deviation
$\sqrt{p(1-p)/n}$. With $p = 0.1$ and $n = 10{,}000$ that is
$\sqrt{0.09/10{,}000} \approx 0.003$, so two variants differing by 1 percentage
point sit about 3.3 standard errors apart — detectable. At $n = 100$ the standard
deviation is $\approx 0.03$, the same 1-point difference is a third of a standard
error, and the test is worthless.

The square root is the whole story, and it comes from $np(1-p)$ growing only
linearly in $n$ while $n^2$ grows quadratically. The consequence for planning is
that detecting a relative change of size $r$ needs $n$ roughly proportional to
$1/r^2$: halving the effect you want to detect costs four times the traffic.
This is why product teams are pushed towards detecting large effects, towards
running longer, and towards accepting that a 0.5% improvement is not measurable in
a week — not because the arithmetic is subtle, but because $1/\sqrt{n}$ is a slow
way to zero.

It is also why the lesson's last code block reports the *distribution* of $\hat{p}$
rather than a single number: an estimate without its spread is not an answer, and
the spread is what a confidence interval is built from
([Lesson 69](../part05_probability_statistics/69_estimation_and_hypothesis_testing.md)).

</details>

## Exercises and Solutions

**[ ] Exercise 1 — full PMF and CDF of Binomial(8, 0.4).** Compute every PMF
value, verify they sum to 1, find the mode and the mean, and compute P(X ≥ 6)
and P(X ≤ 1) using both the complement rule and direct summation.

<details>
<summary>Solution</summary>

P(X=k) = C(8,k) · 0.4ᵏ · 0.6^(8−k):

| k | C(8,k) | P(X=k) | F(X≤k) |
| --- | --- | --- | --- |
| 0 | 1 | 0.016796 | 0.016796 |
| 1 | 8 | 0.089580 | 0.106376 |
| 2 | 28 | 0.209019 | 0.315395 |
| 3 | 56 | 0.278692 | 0.594086 |
| 4 | 70 | 0.232243 | 0.826330 |
| 5 | 56 | 0.123863 | 0.950193 |
| 6 | 28 | 0.041288 | 0.991480 |
| 7 | 8 | 0.007864 | 0.999345 |
| 8 | 1 | 0.000655 | 1.000000 |

Sum = 1.000000 ✓. Mean np = 3.2. The mode is the largest entry, k = 3, with
P(3) = 0.278692. That matches the formula mode = floor((n+1)p) = floor(3.6) = 3.

Notice the mean (3.2) is not an integer and is not an achievable outcome at all —
X can only be 0 through 8. The mean does not need to be in the support, which is
the clearest possible demonstration that a mean is a summary, not a prediction.

P(X ≥ 6) = 0.041288 + 0.007864 + 0.000655 = 0.049807. Via the complement,
1 − F(5) = 1 − 0.950193 = 0.049807. The two agree exactly.

P(X ≤ 1) = 0.016796 + 0.089580 = 0.106376.

```python
from math import comb

n, p = 8, 0.4
pmf = {k: comb(n, k) * p**k * (1 - p) ** (n - k) for k in range(n + 1)}
cdf, running = {}, 0.0
for k in range(n + 1):
    running += pmf[k]
    cdf[k] = running

for k in range(n + 1):
    print(f"k={k} C({n},{k})={comb(n, k):3d} P={pmf[k]:.6f} F={cdf[k]:.6f}")

print(f"sum of PMF      = {sum(pmf.values()):.10f}")
print(f"mean np         = {n * p:.6f}   mode = {(n + 1) * p}")
mode = max(pmf, key=lambda k: (pmf[k], -k))
print(f"P(X >= 6) direct  = {sum(pmf[k] for k in range(6, n + 1)):.6f}")
print(f"P(X >= 6) via 1-F = {1 - cdf[5]:.6f}")
print(f"agree: {abs(sum(pmf[k] for k in range(6, n + 1)) - (1 - cdf[5])) < 1e-12}")
print(f"P(X <= 1)       = {cdf[1]:.6f}")
```

The agreement check is the real point: the complement rule and direct summation
are both consequences of the axioms, so they cannot disagree beyond rounding.

</details>

**[ ] Exercise 2 — an unusual PMF and its expectation.** A network device emits
0 packets with probability 0.5, 1 packet with probability 0.3, and 3 packets with
probability 0.2. (a) Verify this is a valid PMF. (b) Compute E[X]. (c) Compute
the CDF and P(X ≤ 1). (d) Use the tail-sum formula to compute E[X] a second
time, and explain why it agrees.

<details>
<summary>Solution</summary>

(a) All values non-negative and 0.5 + 0.3 + 0.2 = 1.0, so this is a valid PMF.

(b) E[X] = 0·0.5 + 1·0.3 + 3·0.2 = 0 + 0.3 + 0.6 = 0.9.

(c) The CDF: F(0) = 0.5, F(1) = 0.8, F(2) = 0.8 (no mass at 2), F(3) = 1.0.
Note F is non-decreasing with a **flat step** at 2 — that flat step is the
signature of a value with zero probability, and it is exactly why recovering the
PMF as F(x) − F(x−1) must be done with care in continuous settings.

So P(X ≤ 1) = 0.8.

(d) Tail-sum: E[X] = Σ_{k≥1} P(X ≥ k) = P(X≥1) + P(X≥2) + P(X≥3)
= 0.5 + 0.2 + 0.2 = 0.9. ✓

The agreement is structural, not lucky. The tail-sum formula works because each
indicator Iₖ contributes 1 precisely when X ≥ k, so summing them counts each
outcome exactly X times. Note also how the two computations use the PMD
differently: the direct route needs to know the value at each outcome, while the
tail-sum route only needs survival probabilities — which is why it is the method
that scales to huge supports, and why monitoring dashboards compute "fraction of
requests ≥ threshold" rather than the full histogram.

```python
support = {0: 0.5, 1: 0.3, 3: 0.2}
max_x = max(support)

# (a) validity
print(f"all non-negative : {all(p >= 0 for p in support.values())}")
print(f"sums to 1        : {sum(support.values()) == 1.0}")

# (b) direct expectation
mean_direct = sum(x * p for x, p in support.items())
print(f"(b) E[X] direct          = {mean_direct:.6f}")

# (c) CDF
cdf, running = {}, 0.0
for x in range(max_x + 1):
    running += support.get(x, 0.0)
    cdf[x] = running
print("(c) CDF:", {k: round(v, 6) for k, v in cdf.items()})
print(f"    P(X <= 1)           = {cdf[1]:.6f}")
print(f"    F(1) == F(2) (no mass at 2): {cdf[1] == cdf[2]}")

# (d) tail-sum
mean_tail = sum(cdf[max_x] - cdf[k - 1] for k in range(1, max_x + 1))
print(f"(d) E[X] via tail-sum   = {mean_tail:.6f}")
print(f"    agree: {abs(mean_direct - mean_tail) < 1e-12}")
```

</details>

**[ ] Exercise 3 — Challenge: design a distribution from a requirement.** A
cache serves a request with probability 0.8 (a hit) and misses with probability
0.2. On a miss the cache refills and the request is retried once, and the retry
succeeds with probability 0.8. (a) Build the PMF of the total number of backend
calls made for one request, and confirm it is Binomial. (b) Compute its mean and
compare with a naive "0.2 extra calls per request" calculation. (c) Compute the
probability that a single request costs 2 backend calls. (d) With 100 requests,
what is the distribution of the total number of backend calls, and what is the
standard deviation?

<details>
<summary>Solution</summary>

(a) Each request makes one backend call unconditionally? No — it makes a backend
call only if the cache misses. So model it as: the number of backend calls B
takes values {0, 1, 2}. B = 0 when the first attempt hits: probability 0.8. If
the first attempt misses (0.2) and the retry hits (0.8), B = 1: probability
0.2·0.8 = 0.16. If both miss, B = 2: 0.2·0.2 = 0.04.

Equivalently: B = X₁ + X₂ where X₁ ~ Bernoulli(0.2) is "first attempt missed"
and X₂ ~ Bernoulli(0.2) is "retry missed", and these are independent because the
miss events are independent. So B ~ Binomial(2, 0.2).

(b) Mean = 2 × 0.2 = 0.4. The naive calculation "0.2 expected misses, each
causing one extra call" also gives 0.4 — and that is the correct intuition,
because a miss costs one *extra* call and the indicator decomposition makes each
miss contribute exactly one.

(c) P(B = 2) = C(2,2) · 0.2² · 0.8⁰ = 0.04. Four percent of requests hit the
backend twice.

(d) The total T over 100 independent requests is Binomial(200, 0.2), because
Binomials add when independent. Mean = 40, and

    Var(T) = 200 · 0.2 · 0.8 = 32,   sd = √32 ≈ 5.657

So a 100-request batch makes about 40 backend calls, but the actual count will
typically land between roughly 29 and 51. If instead you only counted the misses
(about 20 per 100 requests) and forgot that each miss triggers a retry, you'd
underestimate by half.

```python
from math import comb, sqrt

p_miss = 0.2
n_requests = 100

# (a) PMF of backend calls per request -- Binomial(2, 0.2)
print("backend calls | probability")
for b in range(3):
    pb = comb(2, b) * p_miss**b * (1 - p_miss) ** (2 - b)
    print(f"{b:14d} | {pb:.6f}")
print(f"sum = {sum(comb(2,b)*p_miss**b*(1-p_miss)**(2-b) for b in range(3)):.6f}")

# (b) mean
mean_b = 2 * p_miss
print(f"(b) E[backend calls per request] = {mean_b:.6f}")

# (c)
print(f"(c) P(2 calls) = {p_miss ** 2:.6f}")

# (d) total over a batch -- Binomial adds
n_trials = 2 * n_requests
mean_t = n_trials * p_miss
var_t = n_trials * p_miss * (1 - p_miss)
print(f"(d) T ~ Binomial({n_trials}, {p_miss})")
print(f"    E[T]  = {mean_t:.4f}")
print(f"    Var(T)= {var_t:.4f}   sd = {sqrt(var_t):.4f}")
print(f"    ~2sd range: [{mean_t - 2*sqrt(var_t):.2f}, {mean_t + 2*sqrt(var_t):.2f}]")
```

The pattern generalises: **whenever the number of trials is random, check
whether the random part is a sum of Bernoullis.** Here the number of *misses* is
random, which is what made (d) need care — you cannot treat the miss count as
fixed and simply scale, because the variance formula depends on the number of
trials, not on the mean number of misses.

</details>

**[ ] Exercise 4 — a queue-depth variable with gaps in its support.** A request
queue receives exactly 4 jobs per minute, and each job is rejected with
probability 0.15, independently. Let $R$ be the number of rejections in a minute.
(a) State the distribution of $R$ together with its two restrictions. (b) Compute
`P(R = 3)`, `P(R = 0)` and `P(R = 2)`, and explain why the third cannot be
derived from the first two. (c) Build the CDF and compute `P(R ≤ 1)` and
`P(R ≥ 2)`. (d) Verify `P(R = 2)` by counting which of the 4 jobs must be
rejected.

<details>
<summary>Solution</summary>

(a) $R \sim \mathrm{Binomial}(n = 4,\ p = 0.15)$, requiring $0 \le p \le 1$ (here
0.15) and $n$ a non-negative integer (here 4 — the fixed number of jobs, not the
number that get rejected).

(b) Using $P(R = k) = \binom{4}{k}\,0.15^k\,0.85^{4-k}$:

$$P(R = 3) = \binom{4}{3} \cdot 0.15^3 \cdot 0.85 = 4 \cdot 0.003375 \cdot 0.85 = 0.011475$$
$$P(R = 0) = 0.85^4 = 0.522006$$
$$P(R = 2) = \binom{4}{2} \cdot 0.15^2 \cdot 0.85^2 = 6 \cdot 0.0225 \cdot 0.7225 = 0.097537$$

The third number cannot be derived from the first two. Probability mass is
additive only over **disjoint events**, and the events $\{R = 3\}$ and $\{R = 0\}$
carry no information about $\{R = 2\}$. What you *can* add is
$P(R \in \{2,3\}) = 0.097537 + 0.011475 = 0.109012$, because those two events are
disjoint. This is Mistake 1 from Lesson 61 wearing different clothes.

(c) CDF by running sum:

| $k$ | $p_X(k)$ | $F(k) = P(R \le k)$ |
| --- | --- | --- |
| 0 | 0.522006 | 0.522006 |
| 1 | 0.368475 | 0.890481 |
| 2 | 0.097537 | 0.988019 |
| 3 | 0.011475 | 0.999494 |
| 4 | 0.000506 | 1.000000 |

So $P(R \le 1) = 0.890481$, and by the complement rule
$P(R \ge 2) = 1 - 0.890481 = 0.109519$. ✓

(d) Count directly. "Exactly 2 of the 4 jobs are rejected" is a subset of size 2
from a 4-element set, so there are $\binom{4}{2} = 6$ such assignments, each with
probability $0.15^2 \cdot 0.85^2 = 0.016256$. Total $6 \times 0.016256 =
0.097537$. ✓ Matches. The six are reject $\{1,2\}$, $\{1,3\}$, $\{1,4\}$, $\{2,3\}$,
$\{2,4\}$, $\{3,4\}$ — all disjoint, which is what makes the addition legal.

For capacity, $E[R] = np = 0.6$ and $\operatorname{sd}(R) =
\sqrt{4 \cdot 0.15 \cdot 0.85} = \sqrt{0.51} \approx 0.7141$, so a threshold of
"3 or more rejections in a minute" fires about 1.2% of the time.

```python
from math import comb, sqrt

n, p = 4, 0.15
pmf = {k: comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)}
cdf, running = {}, 0.0
for k in range(n + 1):
    running += pmf[k]
    cdf[k] = running

print(f"R ~ Binomial(n={n}, p={p})")
print(f"mean {n * p}, sd {(n * p * (1 - p)) ** 0.5:.4f}")
for k in range(n + 1):
    print(f"  P(R={k}) = {pmf[k]:.6f}   F({k}) = {cdf[k]:.6f}")
print(f"  sum of PMF = {sum(pmf.values()):.10f}")

print()
print(f"(b) P(R=3) = {pmf[3]:.6f}")
print(f"    P(R=0) = {pmf[0]:.6f}")
print(f"    P(R=2) = {pmf[2]:.6f}  <- not derivable from the two above")
print(f"    P(R in {{2,3}}) IS additive = {pmf[2] + pmf[3]:.6f}")

print()
print(f"(c) P(R <= 1) = {cdf[1]:.6f}")
print(f"    P(R >= 2) = {1 - cdf[1]:.6f}")
direct = sum(pmf[k] for k in range(2, n + 1))
print(f"    agree with direct summation: {abs((1 - cdf[1]) - direct) < 1e-12}")

by_counting = comb(n, 2) * p ** 2 * (1 - p) ** 2
print()
print(f"(d) C({n},2) = {comb(n, 2)} subsets, each {p ** 2 * (1 - p) ** 2:.6f} "
      f"-> {by_counting:.6f}")
print(f"    agrees with the PMF: {abs(by_counting - pmf[2]) < 1e-12}")
```

</details>

**[ ] Exercise 5 — Bernoulli to Binomial, and the tail-sum route.** A feature
flag is served to 12 sessions, and each session converts independently with
probability 0.2. Let $S$ be the number of converters.
(a) Give `E[S]` and `Var(S)` from the Binomial formulas.
(b) Compute `E[S]` a second time using the tail-sum formula
`E[S] = Σ_k P(S ≥ k)`, showing each survival probability.
(c) Compute `P(S = 0)` and `P(S ≥ 3)`.
(d) Compute the standard deviation of `p̂ = S/12` and determine how many sessions
you would need for the standard error to halve.

<details>
<summary>Solution</summary>

(a) $E[S] = np = 12 \times 0.2 = 2.4$.
$\operatorname{Var}(S) = np(1-p) = 12 \times 0.2 \times 0.8 = 1.92$.

(b) Tail-sum, each survival probability computed directly:

| $k$ | $P(S \ge k)$ |
| --- | --- |
| 1 | 0.931281 |
| 2 | 0.725122 |
| 3 | 0.441654 |
| 4 | 0.205431 |
| 5 | 0.072555 |
| 6 | 0.019405 |
| 7 | 0.003903 |
| 8 | 0.000581 |
| 9 | 0.000062 |
| 10 | 0.000005 |
| 11 | 0.000000 |
| 12 | 0.000000 |

The sum is 2.4. ✓ It agrees with (a) exactly, as it must: the decomposition
$S = I_1 + \cdots + I_{12}$ holds on every outcome and linearity of expectation
consumes no independence assumption. Only four of the twelve terms are
appreciable, which is the practical reason the tail-sum route is cheap when $p$ is
small.

(c) $P(S = 0) = 0.8^{12} = 0.068719$, so **6.9% of sessions convert nobody at
all**. $P(S \ge 3) = 0.441654$, about 44%. The asymmetry is stark: sessions with
zero converters outnumber sessions with three or more by better than 6 to 1,
which is the concrete form of the skewed-distribution warning in Mistake 2.

(d) $\operatorname{Var}(S/12) = 1.92/144 = 0.013333$, so
$\sigma_{\hat p} = 0.11547$, which matches
$\sqrt{p(1-p)/n} = \sqrt{0.2 \cdot 0.8/12}$. Halving it requires
$n' = 4 \times 12 = 48$ sessions, because the standard error falls like
$1/\sqrt{n}$: halving a square root means quadrupling what is under it.

```python
from math import comb, sqrt

n, p = 12, 0.2
pmf = {k: comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)}
survival = {t: 1 - sum(pmf[k] for k in range(t)) for t in range(0, n + 1)}

print(f"(a) E[S] = np = {n * p}, Var(S) = np(1-p) = {n * p * (1 - p)}")

print()
print("(b) tail-sum: P(S >= k) for k = 1..n")
for k in range(1, n + 1):
    print(f"  k={k:2d}: {survival[k]:.6f}")
print(f"  sum  = {sum(survival[k] for k in range(1, n + 1)):.6f}")
print(f"  agrees with np: "
      f"{abs(sum(survival[k] for k in range(1, n + 1)) - n * p) < 1e-12}")

print()
print(f"(c) P(S = 0)  = {pmf[0]:.6f}")
print(f"    P(S >= 3) = {survival[3]:.6f}")

sd_s = (n * p * (1 - p)) ** 0.5
sd_phat = sd_s / n
target = sd_phat / 2
needed = p * (1 - p) / target ** 2
print()
print(f"(d) sd(S) = {sd_s:.6f};  sd(S/12) = {sd_phat:.6f} "
      f"(= sqrt(p(1-p)/n) = {(p * (1 - p) / n) ** 0.5:.6f})")
print(f"    to halve the standard error you need n' = {needed:.0f} sessions, "
      f"which is {needed / n:.0f}x as many")
```

</details>

**[ ] Exercise 6 — Challenge: a Poisson-binomial, and why the shortcut fails.**
Three independent events can fire on each request: a timeout with probability
0.10, a 5xx error with probability 0.02, and a cache miss with probability 0.30.
Let $T$ be the number of distinct events that fire on one request.
(a) Show that $T$ is **not** Binomial and name what it is instead.
(b) Compute the PMF of $T$ and verify it sums to 1.
(c) Compute `E[T]` and `Var(T)` both from the structure and directly from the PMF.
(d) Compare the correct variance with that of the naive `Binomial(3, p̄)` where
`p̄ = 0.14`, and explain the direction of the discrepancy.

<details>
<summary>Solution</summary>

(a) Binomial requires **one common** $p$ across all trials. Here the three
probabilities differ (0.10, 0.02, 0.30), so $T$ is a **Poisson-binomial**: the sum
of independent Bernoullis with unequal parameters. Its PMF is the convolution of
the three individual PMFs, which in generating-function form is the coefficient
of $z^k$ in

$$(0.9 + 0.1z)(0.98 + 0.02z)(0.7 + 0.3z).$$

(b) Expanding, step by step: $(0.9 + 0.1z)(0.98 + 0.02z) = 0.882 + 0.098z +
0.002z^2$. Then multiplying by $(0.7 + 0.3z)$:

- constant: $0.882 \times 0.7 = 0.6174$
- $z^1$: $0.098 \times 0.7 + 0.882 \times 0.3 = 0.0686 + 0.2646 = 0.3332$
- $z^2$: $0.002 \times 0.7 + 0.098 \times 0.3 = 0.0014 + 0.0294 = 0.0308$
- $z^3$: $0.002 \times 0.3 = 0.0006$

So the PMF should be 0.6174, 0.3332, 0.0308, 0.0006 — but those sum to 0.9820,
not 1. The expansion above is wrong, and finding out where is the whole exercise.
Redo the $z^1$ coefficient carefully: the probability of *exactly one* event firing
is the sum of three disjoint cases (only timeout fires, only 5xx fires, only cache
miss fires):

$$0.10(0.98)(0.7) + 0.02(0.9)(0.7) + 0.30(0.9)(0.98) = 0.0686 + 0.0126 + 0.2646 = 0.3458.$$

The error above was using $0.882 \times 0.3$ without subtracting the cases where
timeout or 5xx *also* fired; the $z$-coefficient of a product is not a plain term
sum when more than two factors are present. The correct PMF is therefore

$$P(T=0) = 0.6174,\quad P(T=1) = 0.3458,\quad P(T=2) = 0.0362,\quad P(T=3) = 0.0006,$$

and it sums to $0.6174 + 0.3458 + 0.0362 + 0.0006 = 1.0000$. ✓ There is no mass
above 3, since only three events can fire. Verify $P(T=2)$ by summing its three
disjoint cases: $0.10 \cdot 0.02 \cdot 0.7 + 0.10 \cdot 0.30 \cdot 0.98 +
0.02 \cdot 0.30 \cdot 0.9 = 0.0014 + 0.0294 + 0.0054 = 0.0362$. ✓

(c) **From the structure.** Linearity of expectation needs no common $p$:
$E[T] = \sum_i p_i = 0.10 + 0.02 + 0.30 = 0.42$. Independence gives
$\operatorname{Var}(T) = \sum_i p_i(1 - p_i) = 0.10(0.9) + 0.02(0.98) + 0.30(0.7)
= 0.09 + 0.0196 + 0.21 = 0.3196$.

**From the PMF.** $E[T] = 0(0.6174) + 1(0.3458) + 2(0.0362) + 3(0.0006) =
0.3458 + 0.0724 + 0.0018 = 0.42$. ✓
$E[T^2] = 0 + 0.3458 + 4(0.0362) + 9(0.0006) = 0.3458 + 0.1448 + 0.0054 =
0.496$, so $\operatorname{Var}(T) = 0.496 - 0.42^2 = 0.496 - 0.1764 = 0.3196$. ✓
Two routes, one answer — the lesson's standard check.

(d) The naive model averages the probabilities to $\bar p = 0.14$ and fits
$\mathrm{Binomial}(3, 0.14)$:

- Naive mean: $3 \times 0.14 = 0.42$. **Correct** — the mean never needed the
  probabilities to be equal.
- Naive variance: $3 \times 0.14 \times 0.86 = 0.3612$, versus the true 0.3196.
  The naive variance is **13.0% high**, and in standard-deviation terms
  $\sqrt{0.3612} = 0.6010$ against the true $\sqrt{0.3196} = 0.5653$.

The discrepancy has a one-line cause: $x(1-x)$ is concave, so
$\sum_i p_i(1-p_i) \le n\bar p(1-\bar p)$ with equality only when all $p_i$ are
equal. Averaging before applying the variance formula always *inflates* the
spread, because it pretends every trial carried the average risk instead of the
mix that actually occurred. A 2%-likely event does not dilute a 30%-likely one by
sitting in the same bucket.

In production this direction matters: an alarm threshold computed from the naive
variance is wider than reality, so it under-fires and hides genuine spikes. The
same concavity argument appears every time heterogeneous trials are collapsed into
one Binomial, which is the general lesson of this exercise.

```python
from math import sqrt

PROBS = {"timeout": 0.10, "5xx": 0.02, "cache_miss": 0.30}

# (b) PMF by explicit convolution over independent Bernoulli trials
pmf = {0: 1.0}
for name, p in PROBS.items():
    nxt = {}
    for k, mass in pmf.items():
        nxt[k] = nxt.get(k, 0.0) + mass * (1 - p)       # this event did not fire
        nxt[k + 1] = nxt.get(k + 1, 0.0) + mass * p     # this event fired
    pmf = nxt

print("PMF of T (Poisson-binomial):")
for k in sorted(pmf):
    print(f"  P(T={k}) = {pmf[k]:.6f}")
print(f"  sum = {sum(pmf.values()):.6f}")

# Cross-check two entries by summing their disjoint cases directly.
pt, p5, pc = PROBS["timeout"], PROBS["5xx"], PROBS["cache_miss"]

# Exactly one fired: three DISJOINT cases, one per event.
one = (pt * (1 - p5) * (1 - pc)
       + p5 * (1 - pt) * (1 - pc)
       + pc * (1 - pt) * (1 - p5))
# Exactly two fired: three DISJOINT cases, one per PAIR of events.
two = (pt * p5 * (1 - pc)
       + pt * pc * (1 - p5)
       + p5 * pc * (1 - pt))
print(f"  P(T=1) direct = {one:.6f}   agrees: {abs(one - pmf[1]) < 1e-9}")
print(f"  P(T=2) direct = {two:.6f}   agrees: {abs(two - pmf[2]) < 1e-9}")

# (c) from the structure, then from the PMF
mean_struct = sum(PROBS.values())
var_struct = sum(p * (1 - p) for p in PROBS.values())
mean_pmf = sum(k * m for k, m in pmf.items())
second_moment = sum(k ** 2 * m for k, m in pmf.items())
var_pmf = second_moment - mean_pmf ** 2
print()
print(f"E[T]   structure {mean_struct:.6f}   pmf {mean_pmf:.6f}   "
      f"agree {abs(mean_struct - mean_pmf) < 1e-9}")
print(f"Var(T) structure {var_struct:.6f}   pmf {var_pmf:.6f}   "
      f"agree {abs(var_struct - var_pmf) < 1e-9}")

# (d) the naive Binomial(3, mean p)
p_bar = mean_struct / len(PROBS)
var_naive = len(PROBS) * p_bar * (1 - p_bar)
print()
print(f"naive Binomial(3, p_bar={p_bar:.4f}): mean {len(PROBS) * p_bar:.4f} "
      f"(correct), variance {var_naive:.6f}")
print(f"  true variance {var_struct:.6f} -> naive is "
      f"{(var_naive / var_struct - 1) * 100:.1f}% HIGH")
print(f"  sd: naive {sqrt(var_naive):.6f} vs true {sqrt(var_struct):.6f}")
```

</details>

## Summary

- A random variable is a function Ω → ℝ; it introduces no randomness of its own,
  only a new lens on the sample space.
- The PMF p_X(x) = P(X = x) is nonnegative and sums to 1; summing it to 1 is the
  cheapest bug check available.
- The CDF F(x) = P(X ≤ x) answers the questions engineers ask ("what fraction is
  at most this threshold"), and the PMF is recoverable as a jump in the CDF.
- Every discrete variable equals a sum of indicators X = Σₖ 1[X ≥ k], which
  makes Bernoulli the only primitive distribution you need.
- Bernoulli(p) has mean p and variance p(1−p); it models one two-outcome trial.
- Binomial(n, p) counts successes in n independent trials; its PMF is
  C(n,k)pᵏ(1−p)^(n−k), with mean np and variance np(1−p).
- The Binomial formula is counting — choosing a subset of k successful trials out
  of n — so Part 02 is a hard prerequisite, not a nice-to-have.
- The mean is a long-run balance point, not a prediction for one run; mode is the
  peak; they differ for skewed distributions like Binomial(10, 0.1).

## Next

[64 — Expectation, Variance, and Laws](../part05_probability_statistics/64_expectation_variance.md) computes the
mean and spread of any random variable, proves linearity of expectation without
any independence assumption, and shows why the square of a mean is not the mean
of squares.