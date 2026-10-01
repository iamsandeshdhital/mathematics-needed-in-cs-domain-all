# 67 — Joint Random Variables and Covariance

**Part**: part05_probability_statistics · **Prerequisites**: 64 · **Time**: 40 min

---

## In Plain Words

Everything so far has been about one number at a time. Real systems are full of
quantities that move together: CPU load and latency, page size and load time,
temperature and sales. Handling two variables at once gives you three new ideas.

The first is that the joint distribution — how the two behave together — is more
information than the two separate distributions, and sometimes much more. The
second is covariance, a number that says whether they move together, up or down,
and how strongly. Correlation is that number rescaled to sit between −1 and 1.

Here is the part worth internalising: **correlation is not causation.** Two
variables can be perfectly correlated because one causes the other, because both
are caused by a third, or by pure coincidence in a small sample. And the third
idea is the most powerful: conditional expectation. Knowing X, the best possible
guess at Y is just the average of Y among outcomes where X took that value — and
that single sentence turns linear regression into a lookup table, and lookup
tables into the foundation of machine learning.

## Why Computer Science Cares

- **Regression is conditional expectation.** Linear regression is the best linear
  predictor of Y given X, and that is exactly what E[Y | X] is. This connects
  straight to [Lesson 38](../part03_linear_algebra/38_orthogonality_and_least_squares.md).
- **Feature engineering and multicollinearity.** Two features correlated at 0.95
  make a model unstable and its coefficients uninterpretable — covariance, not
  correlation, is what actually breaks the linear algebra.
- **A/B tests.** Whether treatment and conversion are independent is the
  independence question in its practical form.
- **Anomaly detection.** Mahalanobis-style scoring and PCA are both built on
  covariance structure ([Lesson 40](../part03_linear_algebra/40_svd_and_pca.md)).
- **Interviews.** "What's the difference between correlation and covariance?" is
  a standard question, and the honest answer involves units.

## The Formal Version

**Definition.** The *joint distribution* of discrete X and Y is

    p_{X,Y}(x, y) = P(X = x, Y = y)

with p_{X,Y}(x,y) ≥ 0 and Σ_x Σ_y p_{X,Y}(x,y) = 1. For continuous variables
there is a joint density f_{X,Y}(x,y) instead.

The joint distribution determines everything about the pair. The two marginals
come from it by summing:

    p_X(x) = Σ_y p_{X,Y}(x, y)        p_Y(y) = Σ_x p_{X,Y}(x, y)

**Definition.** X and Y are *independent* if for all x, y,

    p_{X,Y}(x, y) = p_X(x) · p_Y(y)

**Explanation.** The joint table factorises into a product. Independence is
stronger than it first appears: it is a condition on the *whole* joint
distribution, so one violation anywhere breaks it. Do not check only the
diagonal.

**Definition.** The *covariance* is

    Cov(X, Y) = E[(X − μ_X)(Y − μ_Y)] = E[XY] − E[X]E[Y]

**Explanation.** Both factors are positive when X is above its mean and Y is
above its mean, or when both are below — so the product collects exactly the
outcomes where the two agree. Opposite signs cancel. The second form is the one
to compute, since it needs only the moments. Covariance has **units** (ms ×
requests), which is its main defect.

**Definition.** The *correlation coefficient* is

    ρ = Cov(X, Y) / (σ_X σ_Y)

provided both variances are positive. It is dimensionless, bounded in [−1, 1],
and it measures linear association only.

**Theorem.** |ρ| ≤ 1, with ρ = ±1 exactly when Y = aX + b almost surely, with
a > 0 for ρ = 1 and a < 0 for ρ = −1.

**Proof.** Cauchy–Schwarz applied to the centred variables X − μ_X and Y − μ_Y
gives |E[(X−μ_X)(Y−μ_Y)]| ≤ √E[(X−μ_X)²]·√E[(Y−μ_Y)²] = σ_X σ_Y, and divide. ∎

**Theorem (conditional expectation).** Let X and Y have a joint distribution
with finite variances. Among all functions g of X, the one that minimises the
mean squared error E[(Y − g(X))²] is g(x) = E[Y | X = x].

**Proof.** Write E[(Y − g(X))²] = E[(Y − E[Y|X])²] + E[(E[Y|X] − g(X))²] by
expanding, using the fact that Y − E[Y|X] has mean zero conditional on X. The
first term does not depend on g, and the second is minimised — to zero — when
g(X) = E[Y|X]. ∎

**Explanation.** This is the orthogonal-projection idea from
[Lesson 38](../part03_linear_algebra/38_orthogonality_and_least_squares.md)
wearing probabilistic clothes. g(X) is the projection of Y onto the (infinite
dimensional) space of functions of X, and the residual is by construction
uncorrelated with everything in that space. Linear regression is the special
case where you restrict g to an affine function, which is when the normal equations
of least squares appear.

**Corollary (linear approximation).** For any X, Y,

    E[Y | X] ≈ μ_Y + (Cov(X,Y)/Var(X)) · (X − μ_X)

with equality when Y is a linear function of X. The coefficient
Cov(X,Y)/Var(X) is exactly the slope from least squares. When Y *is* linear in X,
**E[Y | X] = a + bX exactly, with b = Cov(X,Y)/Var(X)** — the conditional mean is
a straight line, and the fitted regression slope is the unique correct answer.

## Worked Example

### Example A — a joint table, marginals, and independence

Roll two fair dice. Let X be the first die and Y the second.

**The joint table** is 36 cells each with probability 1/36. The top-left 2×2
block:

| | Y=1 | Y=2 |
| --- | --- | --- |
| **X=1** | 1/36 | 1/36 |
| **X=2** | 1/36 | 1/36 |

**Marginals.** Summing over y: p_X(1) = 6/36 = 1/6 ✓. Summing over x:
p_Y(1) = 6/36 = 1/6 ✓.

**Check independence.** p_X(1)p_Y(1) = (1/6)(1/6) = 1/36, and the joint cell is
exactly 1/36. So the dice are independent, confirmed at every cell (they all
agree by symmetry).

**Now make them dependent.** Let Y = X — roll one die twice. Then

    p_{X,Y}(x,y) = 1/6 if x = y, else 0

The marginals are unchanged (each still 1/6), but the joint is *nothing like* the
product. p_{X,Y}(1,2) = 0 whereas p_X(1)p_Y(2) = 1/36. Perfect dependence, and
the marginals are completely silent about it. **This is the key observation:**
marginals do not determine the joint, and two systems can have identical
distributions for every individual quantity while behaving completely differently
together.

**Covariance for the independent case.** Independence gives E[XY] = E[X]E[Y], so

    Cov = E[XY] − E[X]E[Y] = 12.25 − 12.25 = **0**,  and ρ = **0**

**Covariance for Y = X.** Now E[XY] = E[X²] = 91/6 ≈ 15.1667, so

    Cov = 15.1667 − 12.25 = 2.9167 = Var(X)

With σ_X = σ_Y = √(35/12) ≈ 1.7078, σ_Xσ_Y = 35/12 = 2.9167, so

    ρ = 2.9167 / 2.9167 = **1**

Two systems, identical marginals, correlation 0 versus correlation 1. Every
individual die looks the same; only the pairing differs. This is the cleanest
demonstration that the marginals are not the story.

**A caution worth internalising.** Cov(X,Y) = E[XY] − E[X]E[Y] requires
subtracting two comparable-sized numbers, and getting it wrong is easy. For the
independent dice, E[XY] = 12.25; if you forget to subtract E[X]E[Y] you get
Cov = 12.25, and then ρ = 12.25/2.9167 = 4.20 — a "correlation" of 4.20. That
impossible value is actually a useful alarm: **|ρ| > 1 means you made an
arithmetic error**, because Cauchy–Schwarz guarantees the true value is in
[−1, 1].

### Example B — covariance vs correlation, and units

Consider two systems. In each, latency rises as load rises; that is the
mechanism. But they differ in scale.

| System | load (requests/s) | latency (ms) |
| --- | --- | --- |
| A | mean 100, sd 20 | mean 50, sd 10 |
| B | mean 10, sd 2 | mean 5, sd 1 |

System A: Cov = ρσ_Xσ_Y = 0.9 × 20 × 10 = 180.
System B: Cov = 0.9 × 2 × 1 = 1.8.

Both have ρ = 0.9, but the covariances differ by a factor of 100 because the
units differ. Neither number is "more correlated" — correlation is the
scale-free one. If you are comparing two relationships on the same scale, either
works; if you are combining features of different units into one matrix, **use
the correlation matrix**, or your largest-unit feature will dominate every
covariance-based computation.

**Why least squares needs the covariance, not the correlation.** The regression
slope of Y on X is b = Cov(X,Y)/Var(X). Write it as b = ρ·σ_Y/σ_X. If you
substitute ρ alone you get ρ, which is wrong unless the two variables have equal
standard deviations. This is why "correlate the features and use those weights" is
a real bug in linear models: the correct weight depends on the *scale* of each
feature relative to its spread.

### Example C — conditional expectation as a predictor

Take a small dataset of 6 observations:

| X (hours since deploy) | Y (requests/s) |
| --- | --- |
| 1 | 10 |
| 2 | 12 |
| 3 | 11 |
| 4 | 14 |
| 5 | 15 |
| 6 | 13 |

**Non-parametric conditional expectation** — the lookup table:

    E[Y | X=1] = 10      (only one observation)
    E[Y | X=4] = 14
    E[Y | X=6] = 13

This is a perfect predictor on the training data, and a terrible one on new data,
because with one observation per x value you have memorised rather than modelled.
This is the honest statement of what a non-parametric conditional mean is.

**Parametric conditional expectation** — fit a line. The means are X̄ = 3.5,
Ȳ = 12.5. Computing the covariance:

    Σ(xᵢ − x̄)(yᵢ − ȳ):
      (1−3.5)(10−12.5) = (−2.5)(−2.5) = 6.25
      (2−3.5)(12−12.5) = (−1.5)(−0.5) = 0.75
      (3−3.5)(11−12.5) = (−0.5)(−1.5) = 0.75
      (4−3.5)(14−12.5) = (0.5)(1.5)  = 0.75
      (5−3.5)(15−12.5) = (1.5)(2.5)  = 3.75
      (6−3.5)(13−12.5) = (2.5)(0.5)  = 1.25
    sum = 13.5
    Σ(xᵢ − x̄)²: 6.25 + 2.25 + 0.25 + 0.25 + 2.25 + 6.25 = 17.5

    slope = 13.5/17.5 = 0.7714
    intercept = 12.5 − 0.7714(3.5) = 9.80

So Ŷ = 9.80 + 0.7714X. The covariance is 13.5/6 = 2.25 and Var(X) = 17.5/6 =
2.9167, and indeed 2.25/2.9167 = 0.7714.

**The residual argument.** The residuals (fitted minus observed) are:

    X=1: 10.5714 − 10 = +0.5714
    X=2: 11.3429 − 12 = −0.6571
    X=3: 12.1143 − 11 = +1.1143
    X=4: 12.8857 − 14 = −1.1143
    X=5: 13.6571 − 15 = −1.3429
    X=6: 14.4286 − 13 = +1.4286

The residuals sum to 0 (by construction — the line passes through the centroid)
and their covariance with X is 2.96 × 10⁻¹⁶, effectively zero. That second
property is precisely the orthogonality condition which makes the line optimal,
and it is the same condition as in
[Lesson 38](../part03_linear_algebra/38_orthogonality_and_least_squares.md).
Any other line's residual is this residual plus a function of X, and since this
residual is already orthogonal to every function of X, that extra piece can only
add to the squared error.

## Runnable Code

### A joint table, marginals, and a dependence check

```python
from itertools import product

# Two independent fair dice: X = die 1, Y = die 2.
independent = list(product(range(1, 7), repeat=2))

# Perfectly dependent: Y = X.
dependent = [(d, d) for d in range(1, 7)]


def joint_table(pairs):
    """The joint distribution as {(x, y): probability}."""
    n = len(pairs)
    table = {}
    for x, y in pairs:
        table[(x, y)] = table.get((x, y), 0.0) + 1.0 / n
    return table


def marginal(table, index):
    """Sum out the other coordinate: p_X for index 0, p_Y for index 1."""
    out = {}
    for (x, y), p in table.items():
        key = x if index == 0 else y
        out[key] = out.get(key, 0.0) + p
    return out


for name, pairs in (("independent", independent), ("dependent Y=X", dependent)):
    table = joint_table(pairs)
    mx, my = marginal(table, 0), marginal(table, 1)

    print(f"--- {name} ---")
    print(f"  marginals identical? X:{sorted(mx.items())[:2]}...")

    # Independence test: compare the joint to the product, cell by cell.
    worst = 0.0
    for (x, y), pxy in table.items():
        product_p = mx[x] * my[y]
        worst = max(worst, abs(pxy - product_p))
    print(f"  max |p_joint - p_X*p_Y| = {worst:.6f}")
    print(f"  independent: {worst < 1e-12}")
    print(f"  p(X=1,Y=2) = {table.get((1, 2), 0.0):.6f}  "
          f"but p_X(1)p_Y(2) = {mx[1] * my[2]:.6f}")
    print()

print("Both systems have IDENTICAL marginals (each die uniform) but wildly")
print("different joints. Marginals do not determine the joint.")
```

### Covariance and correlation, computed three ways

```python
from math import sqrt


def moments(pairs):
    n = len(pairs)
    mean_x = sum(x for x, _ in pairs) / n
    mean_y = sum(y for _, y in pairs) / n
    mx = sum((x - mean_x) ** 2 for x, _ in pairs) / n
    my = sum((y - mean_y) ** 2 for _, y in pairs) / n
    cxy = sum((x - mean_x) * (y - mean_y) for x, y in pairs) / n
    return mean_x, mean_y, mx, my, cxy


cases = [
    ("independent dice", [(x, y) for x in range(1, 7) for y in range(1, 7)]),
    ("dependent Y=X", [(d, d) for d in range(1, 7)]),
    ("dependent Y=7-X", [(d, 7 - d) for d in range(1, 7)]),
    ("perfectly linear Y=2X+1", [(x, 2 * x + 1) for x in range(1, 7)]),
    ("nonlinear Y=X^2", [(x, x * x) for x in range(1, 7)]),
]

print(f"{'case':24} {'E[X]':>6} {'E[Y]':>6} {'Cov':>8} {'sd_X':>7} {'sd_Y':>7} {'rho':>7}")
for name, pairs in cases:
    mx_, my_, vx, vy, cxy = moments(pairs)
    rho = cxy / sqrt(vx * vy)
    print(f"{name:24} {mx_:6.2f} {my_:6.2f} {cxy:8.4f} "
          f"{sqrt(vx):7.4f} {sqrt(vy):7.4f} {rho:7.4f}")

print()
print("Y = X          -> rho = 1   (perfect positive)")
print("Y = 7 - X      -> rho = -1  (perfect negative)")
print("independent    -> rho = 0   (no linear association)")
print("Y = X^2        -> rho is high but NOT 1, because the relation is")
print("   curved: correlation measures LINEAR association only. This is the")
print("   limitation that makes correlation a poor summary of general")
print("   association, and it is why R^2 is meaningless for a curved fit.")
```

### Correlation is not causation: three mechanisms, one number

```python
import random

random.seed(1234)
N = 20_000


def corr(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = sum((x - mx) ** 2 for x in xs)
    dy = sum((y - my) ** 2 for y in ys)
    return num / (dx * dy) ** 0.5


# 1. CAUSATION: y depends on x
x1 = [random.gauss(0, 1) for _ in range(N)]
y1 = [2 * v + random.gauss(0, 0.5) for v in x1]

# 2. COMMON CAUSE: both driven by z, x and y never touch each other
z = [random.gauss(0, 1) for _ in range(N)]
x2 = [v + random.gauss(0, 0.3) for v in z]
y2 = [3 * v + random.gauss(0, 0.3) for v in z]

# 3. COINCIDENCE: no connection at all, but a shared drift creates correlation
x3 = [random.random() for _ in range(N)]
y3 = [v + random.gauss(0, 0.01) for v in x3]

# 4. Selection effect: correlation appears only in the selected subpopulation
base_x = [random.gauss(0, 1) for _ in range(N)]
base_y = [random.gauss(0, 1) for _ in range(N)]
sel = [(a, b) for a, b in zip(base_x, base_y) if a + b > 0]
xs4 = [a for a, _ in sel]
ys4 = [b for _, b in sel]

print(f"1. causation (y = 2x + noise)     rho = {corr(x1, y1):+.4f}")
print(f"2. common cause (both from z)     rho = {corr(x2, y2):+.4f}   "
      f"<- x and y never interact")
print(f"3. coincidence (y = x + tiny noise) rho = {corr(x3, y3):+.4f}")
print()
print(f"4. selection: in the FULL population rho = "
      f"{corr(base_x, base_y):+.4f}  (independent)")
print(f"   but conditioning on x + y > 0   rho = {corr(xs4, ys4):+.4f}")
print()
print("Case 2 is the dangerous one: a real causal arrow from z to both, but")
print("intervening on x would change y NOT AT ALL. Case 4 is Simpson's paradox:")
print("filtering on a common effect manufactures correlation from nothing.")
```

### Conditional expectation: the lookup table and the regression line

```python
from math import sqrt

DATA = [
    (1, 10), (2, 12), (3, 11),
    (4, 14), (5, 15), (6, 13),
]


def empirical_conditional_mean(data):
    """The non-parametric E[Y | X]: group by x and average."""
    groups = {}
    for x, y in data:
        groups.setdefault(x, []).append(y)
    return {x: sum(ys) / len(ys) for x, ys in groups.items()}


def least_squares(data):
    """The linear E[Y|X]. Slope = Cov/Var, from the normal equations."""
    n = len(data)
    mx = sum(x for x, _ in data) / n
    my = sum(y for _, y in data) / n
    cov = sum((x - mx) * (y - my) for x, y in data) / n
    var = sum((x - mx) ** 2 for x, _ in data) / n
    slope = cov / var
    return my - slope * mx, slope, cov, var


cond_mean = empirical_conditional_mean(DATA)
intercept, slope, cov, var = least_squares(DATA)

print("data:", DATA)
print()
print(f"{'X':>3} {'Y':>4} {'E[Y|X] (table)':>16} {'fitted a+bX':>14} {'resid':>8}")
for x, y in DATA:
    fit = intercept + slope * x
    print(f"{x:3d} {y:4d} {cond_mean[x]:16.2f} {fit:14.4f} {fit - y:+8.4f}")

print()
print(f"Cov(X,Y) = {cov:.6f}   Var(X) = {var:.6f}")
print(f"slope = Cov/Var = {cov:.6f}/{var:.6f} = {slope:.6f}")
print(f"intercept = {intercept:.6f}")
print(f"line passes through the centroid: "
      f"{abs((intercept + slope * 3.5) - 12.5) < 1e-12}")

# The residual is uncorrelated with X -- that IS the optimality condition.
resids = [intercept + slope * x - y for x, y in DATA]
mx = sum(x for x, _ in DATA) / len(DATA)
n = len(DATA)
resid_cov = sum((x - mx) * r for (x, _), r in zip(DATA, resids)) / n
print(f"Cov(X, residual) = {resid_cov:.2e}   <- zero, so the fit is optimal")
print(f"sum of residuals = {sum(resids):.2e}")

# Compare against two naive alternatives.
def mean_absolute_error(pred):
    return sum(abs(p - y) for p, (_, y) in zip(pred, DATA)) / n


const_pred = [sum(y for _, y in DATA) / n] * n
lin_pred = [intercept + slope * x for x, _ in DATA]
print()
print(f"MAE of always predicting the mean ({const_pred[0]:.2f}): "
      f"{mean_absolute_error(const_pred):.4f}")
print(f"MAE of the regression line:                       "
      f"{mean_absolute_error(lin_pred):.4f}")
print("-> using X at all reduces the error, which is exactly what")
print("   conditional expectation promises.")
```

### Multicollinearity: why correlation breaks a model

```python
import random

random.seed(99)


def solve_2x2(a, b, c, d, e, f):
    """Solve a*x + b*y = e, c*x + d*y = f by Cramer's rule."""
    det = a * d - b * c
    return (e * d - b * f) / det, (a * f - e * c) / det


def fit(data):
    """OLS slope and intercept for y = intercept + slope*x, pure Python."""
    n = len(data)
    mx = sum(x for x, _ in data) / n
    my = sum(y for _, y in data) / n
    cov = sum((x - mx) * (y - my) for x, y in data) / n
    var = sum((x - mx) ** 2 for x, _ in data) / n
    slope = cov / var
    return my - slope * mx, slope


def predict(data, b0, b1):
    return sum(((b0 + b1 * x) - y) ** 2 for x, y in data) / len(data)


N = 4000
for noise in (1.0, 0.01):
    base = [random.random() for _ in range(N)]
    true_y = [3.0 * v + random.gauss(0, noise) for v in base]
    # Second feature is a near-copy of the first: 99% correlated.
    noisy = [v + random.gauss(0, 0.05) for v in base]
    y2 = [2.0 * v + random.gauss(0, noise) for v in noisy]

    x1, x2 = base, noisy
    mx1, mx2 = sum(x1) / N, sum(x2) / N
    cov = sum((a - mx1) * (b - mx2) for a, b in zip(x1, x2)) / N
    v1 = sum((a - mx1) ** 2 for a in x1) / N
    v2 = sum((b - mx2) ** 2 for b in x2) / N
    rho = cov / (v1 * v2) ** 0.5

    b0_1, b1_1 = fit([(a, c) for a, c in zip(x1, true_y)])
    b0_2, b1_2 = fit([(a, c) for a, c in zip(x2, true_y)])

    print(f"noise sd = {noise}, correlation(x1, x2) = {rho:.6f}")
    print(f"  fit y on x1 alone: slope = {b1_1:8.4f}   (truth 3.0)")
    print(f"  fit y on x2 alone: slope = {b1_2:8.4f}   (truth 3.0)")
    print(f"  test MSE x1={predict([(a,c) for a,c in zip(x1,true_y)], b0_1, b1_1):.6f}"
          f"  x2={predict([(a,c) for a,c in zip(x2,true_y)], b0_2, b1_2):.6f}")
    print(f"  fit BOTH together (normal equations):")
    a = sum(v * v for v in x1)
    b = sum(x1[i] * x2[i] for i in range(N))
    c2 = sum(v * v for v in x2)
    e = sum(x1[i] * true_y[i] for i in range(N))
    f = sum(x2[i] * true_y[i] for i in range(N))
    w1, w2 = solve_2x2(a, b, b, c2, e, f)
    combined_mse = sum(
        (w1 * x1[i] + w2 * x2[i] - true_y[i]) ** 2 for i in range(N)
    ) / N
    print(f"    w1 = {w1:8.3f}   w2 = {w2:8.3f}   "
          f"test MSE = {combined_mse:.6f}")
    print(f"    w1+w2 = {w1 + w2:.3f} (the two features are near-copies, so the")
    print("    model can only estimate their SUM reliably; splitting it")
    print("    between them is arbitrary and swings wildly with noise.)")
    print(f"    -> adding the redundant feature changed the test MSE from")
    print(f"       {predict([(a,c) for a,c in zip(x1,true_y)], b0_1, b1_1):.6f} "
          f"to {combined_mse:.6f}, with no explanatory gain.")
    print()
```

### With Libraries

The block below needs `numpy`, `matplotlib`, and `scipy`. It is optional and
`run_all.py` skips it; everything above is standard library only.

```python  title="With Libraries: joint distributions and the linear fit"
# Requires numpy / matplotlib / scipy -- not runnable in the stdlib check.
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(4)
N = 30_000
fig, axes = plt.subplots(1, 3, figsize=(16, 4.6))

# 1. Two distributions with the SAME marginals but different joints.
x_a = rng.uniform(0, 10, N)
y_indep = rng.uniform(0, 10, N)
y_dep = x_a  # perfect dependence, identical marginals

ax = axes[0]
ax.scatter(x_a[:800], y_indep[:800], s=4, alpha=0.4, label="independent, rho=0")
ax.scatter(x_a[:800], y_dep[:800], s=4, alpha=0.4, color="crimson",
           label="dependent, rho=1")
ax.set_xlabel("X"); ax.set_ylabel("Y")
ax.set_title("Same marginals, different joints")
ax.legend(fontsize=8)

# 2. Correlation vs causation: a common cause.
z = rng.normal(0, 1, N)
xc = z + rng.normal(0, 0.3, N)
yc = 3 * z + rng.normal(0, 0.3, N)
ax = axes[1]
ax.scatter(xc[:800], yc[:800], s=4, alpha=0.4, color="darkgreen")
r = np.corrcoef(xc, yc)[0, 1]
ax.set_xlabel("X"); ax.set_ylabel("Y")
ax.set_title(f"Common cause z: rho = {r:.3f}, but X does not cause Y")
ax.text(0.05, 0.9, f"Cov(X,Y) = {np.cov(xc, yc)[0,1]:.2f}", transform=ax.transAxes)

# 3. Conditional expectation E[Y|X] vs the linear fit.
ax = axes[2]
xv = rng.uniform(0, 10, N)
yv = 2 * xv + 1 + rng.normal(0, 2, N)
fit = stats.linregress(xv, yv)
grid = np.linspace(0, 10, 60)
cond = [yv[xv > g - 0.2][xv[xv > g - 0.2] <= g + 0.2].mean()
        for g in grid]
ax.scatter(xv[:600], yv[:600], s=4, alpha=0.3, color="grey", label="data")
ax.plot(grid, cond, "o", ms=4, color="orange",
        label="E[Y|X] (binned)")
ax.plot(grid, fit.intercept + fit.slope * grid, "-", color="navy", lw=2,
        label=f"OLS: y = {fit.intercept:.2f} + {fit.slope:.2f}x")
ax.set_xlabel("X"); ax.set_ylabel("Y")
ax.set_title("Conditional mean is a line when the relation is linear")
ax.legend(fontsize=8)

plt.tight_layout()
plt.savefig("joint_covariance.png", dpi=110)
print("wrote joint_covariance.png")
```

## Common Mistakes

**Mistake 1 — concluding causation from correlation.**
Wrong: "Ice cream sales correlate with drownings, so ice cream causes drowning."
Right: both are caused by hot weather. Correlation is a *joint* fact about the
observed data and says nothing about the causal structure, which requires an
experiment or a causal model. The temptation is that correlation is the only
thing you can compute from observational data, so it gets read as causal by
default.

**Mistake 2 — using correlation as a regression weight.**
Wrong: "the features correlate 0.9 and 0.8 with the target, so weight them 0.9 and
0.8." Right: the least-squares weight is Cov/Var = ρ·σ_Y/σ_X, so the standard
deviations of the features are part of the answer. Using ρ alone gives the wrong
units and the wrong model whenever features have different spreads.

**Mistake 3 — assuming ρ = 0 means independence.**
It does not. ρ = 0 means *no linear association*; variables can be strongly
dependent and still have ρ = 0. Let Y = X² with X symmetric: ρ = 0, yet knowing X
determines Y exactly. Independence requires factorisation of the whole joint
distribution, which correlation cannot test.

**Mistake 4 — treating a covariance matrix as interchangeable with a correlation
matrix.**
Covariance depends on units; correlation does not. Combining features measured in
milliseconds, bytes, and counts into one matrix means the largest-unit feature
dominates every covariance-based computation — including PCA
([Lesson 40](../part03_linear_algebra/40_svd_and_pca.md)) and Mahalanobis distance.
Standardise, or use the correlation matrix.

**Mistake 5 — trusting a conditional mean built from one observation per bin.**
E[Y | X = x] from a single data point is that data point. Non-parametric
conditional means need many observations per bin, and the number of bins must
shrink as data thins. The non-parametric estimate degrades exactly where you need
prediction most — off the training grid.

## Formula Sheet

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$p_{X,Y}(x,y)$` | `$= P(X = x,\ Y = y)$` | **Joint distribution**: the probability of a *pair* of outcomes. Contains strictly more than the two marginals. | Whenever two quantities are described together. Two dice: independent gives ρ = 0, `Y = X` gives ρ = 1, same marginals. |
| joint conditions | `$\ge 0$` and `$\sum_x \sum_y p_{X,Y}(x,y) = 1$` | Nonnegative, total 1. | Validation. |
| `$p_X(x)$` | `$= \sum_y p_{X,Y}(x,y)$` | **Marginal**: sum out the other coordinate. | Recovering one variable's distribution from the pair. |
| `$p_Y(y)$` | `$= \sum_x p_{X,Y}(x,y)$` | Same, the other way. | As above. |
| independent | `$p_{X,Y}(x,y) = p_X(x)\,p_Y(y)$` for **all** x, y | The joint table factorises. One violated cell is enough to break it. | Must be argued from the mechanism. Checking the diagonal, or a few cells, is not a test. |
| `$\mathrm{Cov}(X,Y)$` | `$= E[(X-\mu_X)(Y-\mu_Y)] = E[XY] - E[X]E[Y]$` | Signed "do they move together?" Collects exactly the outcomes where both are above or both below their means. | Use the **second** form to compute — it needs only moments. Carries **units**, which is its defect. |
| `$\mu_X, \mu_Y$` | `$E[X], E[Y]$` | The two means, subtracted off before multiplying. | Any covariance or correlation. |
| `$\rho$` | `$\dfrac{\mathrm{Cov}(X,Y)}{\sigma_X \sigma_Y}$`, needs `$\sigma_X, \sigma_Y > 0$` | Correlation: dimensionless, in $[-1, 1]$, **linear association only**. | Comparing relationships across differently-scaled variables. Never use it as a regression weight. |
| Cauchy–Schwarz | `$|\rho| \le 1$`, equality iff `$Y = aX + b$ a.s. | Absolute bound. | **`|ρ| > 1` means arithmetic error**, not a strong relationship. |
| `$\rho = 0$` | means *no linear association*, **not** independence | `Y = X²` with symmetric `X` gives `ρ = 0` while `X` determines `Y` exactly. | Mistake 3 in this lesson. Correlation cannot test independence. |
| correlation ≠ causation | three mechanisms give the same ρ | causation; common cause `z`; coincidence; selection on a shared effect. | Case 2 in the code: `ρ` high, but intervening on `X` changes `Y` not at all. |
| `$\mathrm{Cov}(A+B, B)$ | Var(B)$ | if `$A \perp B$ | An aggregate is perfectly correlated with the component that accounts for its variation. | Why a total and its parts cannot be independent model inputs. |
| `$\sigma_X\sigma_Y$` | `$\mathrm{Cov} = \rho\,\sigma_X\sigma_Y$ | `$\rho$ | `$\rho\sigma_Y/\sigma_X$ | Covariance = correlation × product of sds. | The unit conversion that makes Example B work: same ρ = 0.9, covariances 180 and 1.8. |
| `b = \mathrm{Cov}(X,Y)/\mathrm{Var}(X)$` | `$\mu_Y - b\,\mu_X$` for the intercept | **Least-squares slope and intercept.** Equals `$\rho\sigma_Y/\sigma_X$`, not ρ. | Any linear fit. Mistake 2 is using ρ alone. |
| `$E[Y \mid X=x]$` | `$\mathrm{argmin}_g\ E[(Y-g(X))^2] = E[Y\mid X]$` | **Conditional expectation** is the best possible predictor of Y given X, over *all* functions g. | Regression as prediction. Non-parametric form: average Y within each X bin. |
| `E[(Y-g(X))^2]` | `$\displaystyle = E[(Y-E[Y|X])^2] + E[(E[Y|X]-g(X))^2]$` | The MSE decomposes into irreducible noise plus a non-negative penalty, minimised at `g = E[Y|X]`. | The optimality proof, and why the best predictor's residual is uncorrelated with everything in X. |
| `$R^2$` | `$\rho^2 = \dfrac{\mathrm{Cov}(X,Y)^2}{\mathrm{Var}(X)\mathrm{Var}(Y)} = 1 - \dfrac{\mathrm{MSE}_{\text{line}}}{\mathrm{Var}(Y)}$` | Fraction of variance explained by the linear fit. | The exact algebraic origin of R². **Meaningless for a curved fit.** |
| residual orthogonality | `$\sum_i r_i = 0$` and `$\sum_i (x_i - \bar x)\,r_i = 0$ | The normal equations. Line passes through the centroid; residual is uncorrelated with X. | Certifies the fit is optimal; any other line adds a non-negative penalty. |
| covariance vs correlation matrix | — | Covariance carries units; correlation does not. | Mixing features in ms, bytes, and counts: **standardise**, or the largest-unit feature dominates PCA and Mahalanobis. |

## Multiple Choice Questions

**Q1.** Two systems have identical marginals: X and Y are each uniform on
{1,…,6}. In system A, Y is an independent roll; in system B, Y = X. What are the
two correlations?

- A) Both 0, because the marginals are the same
- B) ρ = 0 for A and ρ = 1 for B
- C) ρ = 1 for both, because both have X = Y in distribution
- D) ρ = 0 for A and ρ = 2 for B, since Y tracks X perfectly

<details>
<summary>Answer and explanation</summary>

**B) ρ = 0 for A and ρ = 1 for B.**

This is Example A, and the code block prints `0.0000` and `1.0000`. Option A is
the key observation of the whole lesson: marginals do not determine the joint.
Option C confuses "same distribution" with "same value". Option D is a
nonsense value — Cauchy–Schwarz guarantees $|\rho| \le 1$, so a reported
correlation of 2 is an arithmetic error, as the lesson's caution note says.

</details>

**Q2.** `Y = X²` with X symmetric about 0. What is ρ, and are X and Y independent?

- A) ρ = 1 and not independent
- B) ρ = 0, yet not independent: knowing X determines Y exactly, but the relation is curved, not linear
- C) ρ = 0 and independent, since the correlation is zero
- D) ρ is undefined, because Y's variance is infinite

<details>
<summary>Answer and explanation</summary>

**B) ρ = 0, yet not independent: knowing X determines Y exactly, but the relation
is curved, not linear.**

The code block reports ρ = 0.9789 for `$Y = X^2$` on {1,…,6} — high but not 1,
precisely because the relation is curved and the lesson's example uses a
one-sided domain. With X symmetric about 0 the symmetry cancels the covariance
exactly and ρ = 0. Option A confuses linear with general dependence. Option C is
Mistake 3 in this lesson: ρ = 0 says nothing about independence, which requires
the whole joint to factorise. Option D is false; `$X^2$` has finite variance
whenever X does.

</details>

**Q3.** Why is the least-squares slope $\mathrm{Cov}(X,Y)/\mathrm{Var}(X)$ rather
than just ρ?

- A) Because ρ ignores the units, and least squares needs a slope with Y's units
- B) Because the slope is `$\rho\sigma_Y/\sigma_X$`, so each feature's spread enters the weight; using ρ alone gives the wrong units and the wrong model when spreads differ
- C) Because ρ is only defined when both variables are normal
- D) Because ρ is biased downward in small samples

<details>
<summary>Answer and explanation</summary>

**B) Because the slope is `$\rho\sigma_Y/\sigma_X$`, so each feature's spread
enters the weight; using ρ alone gives the wrong units and the wrong model when
spreads differ.**

This is Mistake 2, and Example B makes the units argument explicit. Option A is
the right *reason* stated loosely — ρ is dimensionless so it cannot be a slope
with Y's units — but B is the complete statement. Option C is false; ρ needs
only positive variances. Option D is a real small-sample concern about
*estimating* ρ, but it is not why the slope formula differs.

</details>

**Q4.** Two features correlate at 0.95 with each other, and each correlates 0.9
with the target. You fit both. What is the likely practical outcome?

- A) The model predicts better and the coefficients are more interpretable
- B) The model can estimate their **sum** reliably but splits it arbitrarily between them; individual weights swing wildly and the test error can get worse
- C) Nothing changes, since correlation 0.95 is nearly independent
- D) The fit fails outright with a divide-by-zero

<details>
<summary>Answer and explanation</summary>

**B) The model can estimate their **sum** reliably but splits it arbitrarily
between them; individual weights swing wildly and the test error can get
worse.**

This is the multicollinearity code block, and the printed `w1 + w2` line is the
point. Option A is the belief that makes the problem dangerous — the *fit* looks
great on training data. Option C is false; 0.95 is far from independence. Option
D would need an exactly singular covariance matrix, not a near-singular one; the
real symptom is instability, not a crash.

</details>

**Q5.** Ice cream sales correlate with drownings at ρ = 0.8. What does that
license you to conclude?

- A) Ice cream sales cause drownings
- B) Drownings cause ice cream sales
- C) Nothing causal — a common cause (hot weather) produces the correlation, and ρ alone cannot distinguish the three mechanisms
- D) Either A or B, since correlation at 0.8 is far too strong to be coincidental

<details>
<summary>Answer and explanation</summary>

**C) Nothing causal — a common cause (hot weather) produces the correlation, and
ρ alone cannot distinguish the three mechanisms.**

Mistake 1, and the second case in the correlation code block. Option D is the
core misconception: a *large* ρ is not more causal than a small one, because the
common-cause mechanism produces any ρ you like depending only on how strong the
shared driver is. Option A is the ice-cream reading; option B is the reversed
reading. Both are equally unfounded — which is itself the point.

</details>

**Q6.** You filter to observations where `x + y > 0`, from a population where X
and Y are independent. What happens to the observed correlation?

- A) It stays at 0, because the population correlation was 0
- B) It becomes strongly positive: conditioning on a shared effect manufactures correlation from nothing (Simpson's paradox)
- C) It becomes exactly 1
- D) It becomes negative, since the constraint is an inequality

<details>
<summary>Answer and explanation</summary>

**B) It becomes strongly positive: conditioning on a shared effect manufactures
correlation from nothing (Simpson's paradox).**

The fourth case in the code prints a near-zero correlation on the full population
and a strongly positive one on the selected subpopulation. Option A is the
trap — the marginal correlation is not preserved under conditioning. Option C
requires a stronger constraint than this one produces. Option D has the sign
wrong; selecting on a sum of both variables biases them in the *same* direction.

</details>

**Q7.** What is the covariance between two independent fair dice?

- A) 1
- B) 0, because independence gives `E[XY] = E[X]E[Y]`, so Cov = 0
- C) 2.9167
- D) It depends on the order of the dice

<details>
<summary>Answer and explanation</summary>

**B) 0, because independence gives `E[XY] = E[X]E[Y]`, so Cov = 0.**

Option A is a plausible non-answer — 1 is the size of the joint sample count per
cell. Option C is `Var(X) = 35/12`, the value you get for the *dependent*
`Y = X` case, which is the lesson's key contrast. Option D is nonsense;
covariance is symmetric, Cov(X,Y) = Cov(Y,X).

</details>

**Q8.** A coin is flipped twice. X = number of heads; Y = the second flip. Are X
and Y independent?

- A) Yes, because the flips are independent
- B) No: X *contains* Y, so `p(0,0) = 1/4` while `p_X(0)p_Y(0) = 1/8`
- C) Yes, because Cov(X,Y) = 0
- D) No, because both are Bernoulli

<details>
<summary>Answer and explanation</summary>

**B) No: X *contains* Y, so `p(0,0) = 1/4` while `p_X(0)p_Y(0) = 1/8`.**

Exercise 1 computes exactly this. Option A is the subtle case worth
internalising: the *flips* are independent, but two functions of the same flips
are independent only if they depend on disjoint bits. Option C is factually wrong
here — Exercise 1 finds Cov = 0.25 and ρ = 0.7071. Option D is irrelevant; being
Bernoulli says nothing about dependence.

</details>

**Q9.** Why does the least-squares residual being uncorrelated with X certify that
the line is optimal?

- A) Because uncorrelated residuals look tidy
- B) Because any other line's residual is this residual plus a function of X, and the squared error decomposes into irreducible noise plus a non-negative penalty that is zero only when `g = E[Y|X]`
- C) Because residuals must sum to zero, which pins the intercept
- D) Because uncorrelated residuals imply the fit is unbiased

<details>
<summary>Answer and explanation</summary>

**B) Because any other line's residual is this residual plus a function of X, and
the squared error decomposes into irreducible noise plus a non-negative penalty
that is zero only when `g = E[Y|X]`.**

This is the conditional-expectation theorem in Example C. Option A is
cosmetic. Option C is a *separate* true fact — the residual sum being zero pins
the intercept — but it does not certify the slope, so it is not the
optimality argument. Option D is a real property of OLS with an intercept, but
unbiasedness and minimality are different claims.

</details>

**Q10.** You have one observation per distinct value of X, and you build a
non-parametric `E[Y|X]` lookup table. What is wrong?

- A) Nothing — it is the most faithful model available
- B) It memorises rather than generalises: `E[Y|X=x]` from one point *is* that point, and it degrades exactly where you need prediction most
- C) It is biased downward
- D) It requires continuous X

<details>
<summary>Answer and explanation</summary>

**B) It memorises rather than generalises: `E[Y|X=x]` from one point *is* that
point, and it degrades exactly where you need prediction most.**

Example C and Mistake 5 both make this point; Exercise 2(a) produces a table that
predicts perfectly on the training data and is worthless off it. Option A is the
temptation — the table *is* the non-parametric conditional mean, correctly
computed, just useless with this much data. Option C confuses lack of data with a
biased estimator. Option D is false; binning works for any X.

</details>

## Subjective Questions

### Short Answer

**Q1.** Define the joint distribution of discrete X and Y, and state the two
conditions that make it valid.

<details>
<summary>Answer</summary>

$p_{X,Y}(x,y) = P(X = x,\ Y = y)$. It is valid when
$p_{X,Y}(x,y) \ge 0$ for every pair and
$\sum_x \sum_y p_{X,Y}(x,y) = 1$. The marginals are recovered by summing out the
other coordinate: $p_X(x) = \sum_y p_{X,Y}(x,y)$ and
$p_Y(y) = \sum_x p_{X,Y}(x,y)$. The joint determines the marginals; the marginals
do not determine the joint.

</details>

**Q2.** State the independence condition and explain why checking a few cells is
not enough.

<details>
<summary>Answer</summary>

X and Y are independent if $p_{X,Y}(x,y) = p_X(x)p_Y(y)$ **for all** x and y.
Independence is a statement about the entire table factorising into a product, so
a single mismatched cell refutes it — and equally, agreement on a handful of
cells establishes nothing. The lesson's Exercise 1 finds a counterexample at
$(0,0)$ where the joint is 1/4 and the product is 1/8. The lesson warns
explicitly against checking only the diagonal.

</details>

**Q3.** Give both forms of covariance and say which one to compute.

<details>
<summary>Answer</summary>

$\mathrm{Cov}(X,Y) = E[(X-\mu_X)(Y-\mu_Y)] = E[XY] - E[X]E[Y]$. Compute the
second form: it needs only the first and second moments, so it works from data
summaries without enumerating outcomes. The first form explains the sign — both
factors are positive when X and Y are both above or both below their means, so
the product collects exactly the outcomes where they agree, and opposite signs
cancel. Covariance carries **units**, which is its main defect.

</details>

**Q4.** Under what condition does ρ equal ±1, and what does ρ = 0 tell you?

<details>
<summary>Answer</summary>

$|\rho| = 1$ exactly when $Y = aX + b$ almost surely, with $a > 0$ giving
$\rho = 1$ and $a < 0$ giving $\rho = -1$ (Cauchy–Schwarz). A reported value
outside $[-1, 1]$ is an arithmetic error. $\rho = 0$ means *no linear
association* and nothing more: with X symmetric, $Y = X^2$ has $\rho = 0$ while X
determines Y exactly. Testing independence requires factorisation of the joint,
which correlation cannot do.

</details>

**Q5.** Give the least-squares slope and intercept in terms of covariance and
variance.

<details>
<summary>Answer</summary>

$b = \mathrm{Cov}(X,Y)/\mathrm{Var}(X) = \rho\,\sigma_Y/\sigma_X$, and
$a = \mu_Y - b\,\mu_X$. The line always passes through the centroid
$(\bar x, \bar y)$, which is why the residual sum is exactly zero. The key point
for Mistake 2: the slope is **not** ρ. Each feature's spread enters the weight, so
substituting ρ gives the wrong units whenever the features have different
standard deviations.

</details>

**Q6.** State the conditional-expectation theorem and the MSE decomposition that
proves it.

<details>
<summary>Answer</summary>

Among all functions $g$ of X, the minimiser of $E[(Y - g(X))^2]$ is
$g(x) = E[Y \mid X = x]$. The proof is the decomposition
$E[(Y-g(X))^2] = E[(Y-E[Y|X])^2] + E[(E[Y|X]-g(X))^2]$: the first term does not
depend on $g$, and the second is a sum of squares, so it is zero exactly when
$g = E[Y|X]$. For the affine restriction this reduces to the least-squares line,
with the residual uncorrelated with X.

</details>

### Long Answer

**Q1. Why does correlation not establish causation, and what would you need
instead?**

<details>
<summary>Model answer</summary>

Because ρ is a fact about the *joint distribution of observed data*, and the joint
distribution is produced by any causal structure consistent with it. The lesson's
code block constructs four mechanisms that give a high ρ with no causal arrow from
X to Y: direct causation, a shared common cause z, near-perfect coincidence, and
selection on a common effect. Nothing in the observed correlation distinguishes
them, and in the common-cause case intervening on X would change Y *not at all* —
the association runs through z.

The reason this matters operationally is that interventions are what you can act
on. ρ = 0.8 between a feature and a metric tells you the feature is a useful
*predictor*; it says nothing about whether changing the feature changes the
metric. Under the common cause, raising the feature (or "optimising" it) may do
nothing, or may even backfire if it is merely a proxy for the thing you actually
want to move.

What you need instead is one of three things. A **randomised experiment**: assign
treatment independently, which breaks the common cause by construction — this is
what an A/B test is for. A **causal model**: a directed graph plus assumptions
about which arrows exist and what is exogenous, which lets you reason about
interventions without collecting them. Or an **instrumental variable** — a
treatment that shifts X but affects Y only through X — which recovers the arrow
from observational data at the price of an untestable exclusion restriction.

The discipline that follows: report ρ as ρ, and reserve causal language for
interventions you actually ran or for a model you are willing to defend.

</details>

**Q2. Why can two variables with identical marginals behave completely
differently together — and what does that break in practice?**

<details>
<summary>Model answer</summary>

Because the marginals are obtained by summing the joint table, and many different
joint tables sum to the same marginals. The lesson's cleanest case: X and Y each
uniform on {1,…,6}. Independent dice give a flat 36-cell table and ρ = 0;
`Y = X` gives a diagonal with six cells and ρ = 1; `Y = 7 − X` gives the
anti-diagonal and ρ = −1. Every individual quantity is identically distributed in
all three. What differs is entirely the *pairing*, and pairing is precisely what
the marginals discard.

What this breaks is the assumption that per-component statistics are enough. Any
analysis that models two components separately — separate dashboards, separate
alerts, separate capacity models — sees only the marginals and is blind to the
dependence. So it will understate the probability of the *combination* that
actually causes trouble: two components each at their 99th percentile are far
more likely to be simultaneously extreme if they share a cause than if they are
independent. This is the same mechanism as the variance-of-a-sum formula from
[Lesson 64](../part05_probability_statistics/64_expectation_variance.md), where dropping the covariance terms
understates spread.

Two concrete habits follow. Store and inspect the **joint**, not only the
marginals — the exercise of building a joint table and testing factorisation cell
by cell is cheap and catches the whole class. And when combining components into
a risk estimate, either argue independence from the mechanism or compute the
covariance terms; Example A's `Y = X` case shows the covariance equals
$\mathrm{Var}(Y)$ exactly, which is the maximal possible correction.

</details>

**Q3. Why does the best predictor of Y given X equal E[Y|X], and how does that
justify linear regression?**

<details>
<summary>Model answer</summary>

By the variance decomposition. Expand
$E[(Y - g(X))^2]$ and use the fact that $Y - E[Y|X]$ has mean zero *conditional
on X*, which kills the cross term:

$$E[(Y-g(X))^2] = E[(Y-E[Y|X])^2] + E[(E[Y|X]-g(X))^2].$$

The first term is irreducible: it is the noise in Y that X cannot possibly
explain, and no predictor of any form can do better than it. The second is a sum
of squares, non-negative and zero exactly when $g(X) = E[Y|X]$. So conditional
expectation is not merely a good predictor, it is the unique minimiser over *all*
functions — a lookup table, a spline, a neural network.

Linear regression is what you get when you restrict $g$ to the affine family
$a + bX$. Restricting the candidate set can only make the error worse, and it
does so by exactly the penalty term $E[(E[Y|X] - g(X))^2]$. When the relation is
genuinely affine, the restriction costs nothing and the penalty is zero — the
fitted slope $\mathrm{Cov}(X,Y)/\mathrm{Var}(X)$ is then the *unique correct
answer*, not an approximation. When it is not, the excess is precisely what $R^2$
measures, and $R^2$ failing to approach 1 is the model telling you the affine
family is inadequate.

The practical consequences are the ones in the lesson's examples. The residual of
the optimal fit is uncorrelated with every function of X — that is the
orthogonality condition, and any other line's residual is this one plus a
function of X, adding a non-negative penalty. And the non-parametric version, the
per-bin average, is the *exact* conditional mean but useless with sparse data,
since one observation per bin makes it memorisation. The whole of regression
practice lives in choosing where between those two extremes to sit.

</details>

**Q4. Why does covariance rather than correlation belong in a model that mixes
features measured in different units?**

<details>
<summary>Model answer</summary>

Because covariance carries units, so its *value* depends on an arbitrary choice
of scale. Example B fixes this: two systems, both with ρ = 0.9, one with load in
requests/s and latency in ms, the other scaled down by 10 in each variable. The
covariances are 180 and 1.8 — a factor of 100 — from identical statistical
structure. The correlation is the scale-free summary; the covariance is not.

Once you build a matrix, the consequence is that the largest-unit feature
dominates every covariance-based computation. Mahalanobis distance measures a
weighted distance with weights from the inverse covariance, so a feature in
milliseconds gets weight $1/\mathrm{ms}^2$ and a feature in seconds gets
$1/\mathrm{s}^2$ — a factor of $10^6$ for no statistical reason. PCA on the raw
covariance matrix will find directions dominated by whichever feature happens to
be measured in the largest unit. This is Mistake 4.

The fix is to standardise: divide each feature by its standard deviation, which
turns the covariance matrix into the correlation matrix, then run the computation
on that. The cost is losing the variance information — standardising treats a
feature with tiny variance the same as one with large variance — so it is right
when the units are arbitrary (ms versus bytes, versus counts) and wrong when they
carry real weight you want the model to respect. And there is a genuine case for
raw covariance when the physical scaling is meaningful, such as a cost matrix in
dollars, where the units *are* the information.

Note this also settles the separate question of regression weights: the least-
squares weight is $\rho\sigma_Y/\sigma_X$, not ρ. Using ρ alone is Mistake 2, and
it is the same underlying confusion — dropping a scale factor because correlation
dropped one.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — joint table and independence from scratch.** A fair coin is
flipped twice. Let X = number of heads, Y = 1 if the second flip is heads else 0.

(a) Build the joint table over (X, Y). (b) Compute the marginals. (c) Are X and Y
independent? (d) Compute Cov(X, Y) and ρ. (e) Now let Y = the first flip's value
instead. Recompute (c) and (d).

<details>
<summary>Solution</summary>

(a) The four equally likely outcomes are TT, TH, HT, HH. With X = total heads and
Y = second flip:

| (X, Y) | outcomes | probability |
| --- | --- | --- |
| (0, 0) | TT | 1/4 |
| (1, 0) | HT | 1/4 |
| (1, 1) | HH | 1/4 |
| (2, 1) | TH | 1/4 |

Every cell has probability 1/4 and the four probabilities sum to 1.

(b) p_X(0) = 1/4, p_X(1) = 1/2, p_X(2) = 1/4. So X ~ Binomial(2, 1/2).
p_Y(0) = 1/2, p_Y(1) = 1/2, so Y ~ Bernoulli(1/2).

(c) Check the factorisation at every cell. p_X(1)p_Y(1) = (1/2)(1/2) = 1/4 = the
joint ✓. p_X(0)p_Y(0) = (1/4)(1/2) = 1/8, but the joint p(0,0) = 1/4 ✗.

So **X and Y are NOT independent**, even though the second flip is independent of
the experiment's mechanism. The reason is that X *contains* Y — when Y = 1 the
total X is at least 1, so X is biased upward by knowing Y. This is a subtle and
important case: no two functions of the same coin flips are independent unless
they depend on disjoint bits.

(d) The moments are E[X] = 1, E[Y] = 1/2, Var(X) = 1/2, Var(Y) = 1/4.

For E[XY], walk the joint table and multiply x·y by each cell's probability. The
(1, 0) cell contributes 1·0 = 0, which is the easy one to miscount:

    E[XY] = 0(1/4) + 0(1/4) + 1(1/4) + 2(1/4) = 3/4 = 0.75

    Cov = E[XY] − E[X]E[Y] = 0.75 − 0.5 = 0.25
    rho = 0.25 / (sqrt(1/2) · sqrt(1/4)) = 0.25 / 0.353553 = **0.7071**

That is within [−1, 1] as it must be. Note 0.7071 is exactly 1/√2, the same value
as the correlation between two independent fair coins — a good illustration of
how the sign structure of a single biased coin can produce positive correlation
between a total and one of its parts.

(e) With Y = the first flip, the arithmetic runs the same way by symmetry: E[XY]
= 0.75, Cov = 0.25, ρ = 0.7071. The general principle is worth stating, because
it generalises to every "total plus one component" situation:

    If X = A + B with A independent of B, then Cov(X, B) = Var(B)

Here A is the first flip and B the second, so Cov(X, Y) = Var(Y) = 1/4 exactly as
observed. The component is perfectly correlated with the part of the total it
accounts for, and independent of the rest — which is exactly why an aggregate and
its components cannot be treated as independent inputs to a model.

```python
from math import sqrt
from itertools import product

# (a)-(c)
outcomes = list(product([0, 1], repeat=2))  # (first, second)
joint, p_x, p_y = {}, {}, {}
n = len(outcomes)
for a, b in outcomes:
    X, Y = a + b, b
    joint[(X, Y)] = joint.get((X, Y), 0.0) + 1.0 / n
    p_x[X] = p_x.get(X, 0.0) + 1.0 / n
    p_y[Y] = p_y.get(Y, 0.0) + 1.0 / n

print("joint table (X = total heads, Y = second flip):")
for key in sorted(joint):
    print(f"  X={key[0]}, Y={key[1]}: {joint[key]:.4f}")
print(f"sums to 1: {abs(sum(joint.values()) - 1) < 1e-12}")
print()
print(f"p_X = {dict(sorted(p_x.items()))}")
print(f"p_Y = {dict(sorted(p_y.items()))}")

independent = all(abs(joint[(x, y)] - p_x[x] * p_y[y]) < 1e-12
                  for (x, y) in joint)
print(f"independent: {independent}")
print(f"  check X=0,Y=0: joint {joint[(0,0)]:.4f} vs product "
      f"{p_x[0]*p_y[0]:.4f}  <- mismatch, so NOT independent")

# (d) covariance and correlation
ex = sum(x * p for x, p in p_x.items())
ey = sum(y * p for y, p in p_y.items())
exy = sum(x * y * p for (x, y), p in joint.items())
cov = exy - ex * ey
var_x = sum((x - ex) ** 2 * p for x, p in p_x.items())
var_y = sum((y - ey) ** 2 * p for y, p in p_y.items())
rho = cov / sqrt(var_x * var_y)

print()
print(f"E[X]={ex:.4f}  E[Y]={ey:.4f}  E[XY]={exy:.4f}")
print(f"Cov = {exy:.4f} - ({ex:.2f}*{ey:.2f}) = {cov:.4f}")
print(f"Var(X)={var_x:.4f}  Var(Y)={var_y:.4f}")
print(f"rho = {cov:.4f}/({sqrt(var_x):.4f}*{sqrt(var_y):.4f}) = {rho:.4f}")
print(f"rho = 1/sqrt(2)? {abs(rho - 1 / sqrt(2)) < 1e-12}")
print(f"within [-1,1]: {-1 <= rho <= 1}")

# (e) Y = first flip instead
joint2 = {}
for a, b in outcomes:
    joint2[(a + b, a)] = joint2.get((a + b, a), 0.0) + 1.0 / n
exy2 = sum(x * y * p for (x, y), p in joint2.items())
print()
print(f"Y = FIRST flip: E[XY]={exy2:.4f}, Cov={exy2 - ex*ey:.4f}, "
      f"rho={(exy2 - ex*ey)/sqrt(var_x*var_y):.4f}")

# The general identity: for X = A + B independent, Cov(X, B) = Var(B)
print()
print("general rule: if X = A + B with A indep of B then Cov(X,B) = Var(B)")
print(f"  Var(Y)={var_y:.4f} == Cov={cov:.4f}: {abs(var_y - cov) < 1e-12}")
```

joint distribution, removes an entire class of error. Notice also that ρ = 0.7071
is the same as the correlation between two independent fair coins — a useful
reminder that a *negative* independence structure inside one coin still produces
perfect positive correlation between a variable and one of its parts.

</details>

**[ ] Exercise 2 — conditional expectation as a predictor.** Use the DATA table
from Example C (X = 1..6, Y = 10, 12, 11, 14, 15, 13).

(a) Compute E[Y | X] non-parametrically. (b) Fit the least-squares line and
report slope, intercept, and the residual sum. (c) Show that Cov(X, residual) = 0
and explain why that certifies optimality. (d) Predict Y at X = 7 and compare
with the trend. (e) Compute the mean squared error of the line and of always
predicting the mean, and state by how much the line improves.

<details>
<summary>Solution</summary>

(a) Each x appears once, so the conditional mean is just the observed value:
E[Y|1] = 10, E[Y|2] = 12, E[Y|3] = 11, E[Y|4] = 14, E[Y|5] = 15, E[Y|6] = 13.
With one observation per bin, the non-parametric estimate is memorisation.

(b) Cov(X,Y) = 13.5/6 = 2.25, Var(X) = 17.5/6 = 2.916667.
Slope = 2.25/2.916667 = 0.771429. Intercept = 12.5 − 0.771429(3.5) = 9.80.
So Ŷ = 9.80 + 0.7714X. Residual sum = 0 exactly (the line passes through the
centroid, a property of OLS with an intercept).

(c) The residuals are +0.5714, −0.6571, +1.1143, −1.1143, −1.3429, +1.4286, and
Cov(X, resid) = 0 to machine precision. This certifies optimality because any
other line's residual is this residual plus a function of X, and a function of X
orthogonal to this residual can only *add* to the squared error. More concretely:
the normal equations of least squares state exactly Σxᵢrᵢ = 0 and Σrᵢ = 0, and
the theorem in the Formal Version says E[(Y − E[Y|X])²] decomposes into
irreducible noise plus a non-negative penalty, minimised when your line *is*
E[Y|X].

(d) Ŷ(7) = 9.80 + 0.7714(7) = 15.20. The data is rising at about 0.77 per hour,
so this is the trend extrapolation. Note the honest caveat: with 6 points and no
noise model, nothing guarantees the trend continues past the observed range, which
is the classic failure of extrapolation.

(e) Residual sum of squares = 0.3265 + 0.4316 + 1.2416 + 1.2416 + 1.8033 +
2.0408 = 7.0854. MSE = 7.0854/6 = 1.1809. Predicting the constant mean 12.5
gives residuals ±2.5, ±0.5, ±1.5, ±1.5, ±2.5, ±0.5, so SSE = 2(6.25 + 0.25 +
2.25) = 17.5 and MSE = 2.9167.

The line reduces MSE from 2.9167 to 1.1809, a **59.5% reduction**.

There is a closed form worth knowing, and it is exactly the conditional
expectation theorem from the Formal Version. The residual variance of the best
affine predictor is

    MSE_line = Var(Y) − Cov(X,Y)² / Var(X)

Here Var(Y) = 2.9167 and Var(X) = 2.9167 happen to coincide (both are 17.5/6), so

    2.9167 − 2.25²/2.9167 = 2.9167 − 1.7357 = 1.1810 ✓

which matches the direct sum. Rearranging, the fraction of variance explained is

    Cov(X,Y)² / (Var(X)Var(Y)) = ρ²

That is the algebraic origin of R² in linear regression: **R² is the square of the
correlation between the data and the fit.**

```python
DATA = [(1, 10), (2, 12), (3, 11), (4, 14), (5, 15), (6, 13)]
n = len(DATA)

groups = {}
for x, y in DATA:
    groups.setdefault(x, []).append(y)
cond = {x: sum(v) / len(v) for x, v in groups.items()}
print("(a) non-parametric E[Y|X]:", {k: round(v, 2) for k, v in cond.items()})

mx = sum(x for x, _ in DATA) / n
my = sum(y for _, y in DATA) / n
cov = sum((x - mx) * (y - my) for x, y in DATA) / n
var_x = sum((x - mx) ** 2 for x, _ in DATA) / n
var_y = sum((y - my) ** 2 for _, y in DATA) / n
slope = cov / var_x
intercept = my - slope * mx

print()
print(f"(b) slope = {slope:.6f}  intercept = {intercept:.6f}")
resids = [intercept + slope * x - y for x, y in DATA]
print(f"    residuals: {[round(r, 4) for r in resids]}")
print(f"    residual sum = {sum(resids):.2e}")

resid_cov = sum((x - mx) * r for (x, _), r in zip(DATA, resids)) / n
print(f"(c) Cov(X, residual) = {resid_cov:.2e}  -> orthogonal, hence optimal")

print(f"(d) prediction at X=7: {intercept + slope * 7:.4f}")

mse_line = sum(r * r for r in resids) / n
mse_const = var_y
print()
print(f"(e) MSE of the line      = {mse_line:.6f}")
print(f"    MSE of the constant  = {mse_const:.6f}")
print(f"    reduction            = {(1 - mse_line / mse_const) * 100:.1f}%")

# The closed form: MSE = Var(Y) - Cov^2/Var(X)
closed = var_y - cov**2 / var_x
print(f"    closed form Var(Y) - Cov^2/Var(X) = {closed:.6f}")
print(f"    matches: {abs(closed - mse_line) < 1e-12}")
```

That closed form is worth keeping: the fraction of variance a linear model
explains is Cov²/(Var(X)Var(Y)) = ρ², which is the algebraic origin of
"R-squared is the square of the correlation".

</details>

**[ ] Exercise 3 — Challenge: Simpson's paradox, in a full joint table.** A
learning algorithm is tested on two datasets:

- Dataset Easy: 90% of examples are easy. On easy examples the model is 90%
  accurate; on hard examples 40% accurate.
- Dataset Hard: 10% easy. The model is **50%** accurate on easy and **50%** on
  hard.

(a) Compute the model's overall accuracy on each dataset. (b) On Easy the model
beats a 50%-always-right baseline by a lot; on Hard it matches it. Someone
concludes "the model is better on Easy because accuracy is higher". What is the
logical error? (c) Construct the full joint tables and compute the accuracy
*within* each difficulty level. (d) Compare within-level accuracy between the two
datasets, and state which model is actually better on easy examples and which is
better on hard examples. (e) Decompose the overall gap into a "mix" component and
a "skill" component, and explain what the decomposition reveals.

<details>
<summary>Solution</summary>

(a) Easy: 0.9(0.90) + 0.1(0.40) = 0.81 + 0.04 = **0.85**.
Hard: 0.1(0.50) + 0.9(0.50) = 0.05 + 0.45 = **0.50**.

(b) The error is comparing overall accuracies without conditioning. Overall
accuracy is a weighted average whose weights differ between the datasets, so the
comparison mixes two things: the model's within-level skill, and the proportion of
easy cases. The second factor dominates. This is Simpson's paradox — a trend
reverses or an apparent effect is created when you aggregate over a variable that
confounds the comparison. The fix is to stratify, or to adjust for the
confounder, exactly as the variance decomposition in
[Lesson 64](../part05_probability_statistics/64_expectation_variance.md) recommends.

(c) Joint tables, cells = (difficulty, correct) with counts per 1000:

| | Easy correct | Easy wrong | Hard correct | Hard wrong |
| --- | --- | --- | --- | --- |
| Dataset Easy | 810 | 90 | 40 | 60 |
| Dataset Hard | 50 | 50 | 450 | 450 |

(d) Within easy: Easy 810/900 = **0.900**, Hard 50/100 = **0.500**.
Within hard: Easy 40/100 = **0.400**, Hard 450/900 = **0.500**.

So the two datasets do not produce a uniform ordering:

- On **easy** examples, the Easy model is better: 90% versus 50%.
- On **hard** examples, the Hard model is better: 50% versus 40%.

There is no level at which one model dominates. Yet the overall accuracies are
0.85 versus 0.50, which looks like an overwhelming win. Both orderings are correct
simultaneously — this is Simpson's paradox, and it is possible because the two
datasets weight the levels differently.

Note also that within-level sample sizes differ (900 versus 100 for easy), so the
50% figure on Dataset Hard's easy examples rests on only 100 cases and carries
correspondingly more noise than the 900-case figure. Any stratified report should
say so.

(e) The overall gap is 0.85 − 0.50 = 0.35, and the decomposition splits it in
two:

    gap = (skill component) + (mix component)
        =  −0.05        +  0.40

The **mix component is +0.40** and the **skill component is −0.05**. The mix
component is not merely the larger part, it *exceeds the whole gap*: it accounts
for 114% of it. The remaining −14% is Dataset Hard being slightly better on skill.

So the entire overall advantage — and then some — comes from Dataset Easy
containing 90% easy examples, each of which is 90% correct. On actual skill,
Dataset Hard is ahead by 5 percentage points, exactly as part (d) found by
comparing within levels.

This is the variance decomposition of
[Lesson 64](../part05_probability_statistics/64_expectation_variance.md) in action: the aggregate differs because
the *weights* differ, not because the *values* do. The practical rule follows
directly — **always report metrics stratified by any variable that could confound,
and never compare aggregate metrics across populations with different
compositions.**

```python
# (a) overall accuracy
easy_mix = {"easy": 0.9, "hard": 0.1}
hard_mix = {"easy": 0.1, "hard": 0.9}
skill = {
    "Easy": {"easy": 0.90, "hard": 0.40},
    "Hard": {"easy": 0.50, "hard": 0.50},
}

overall = {
    name: sum(mix[level] * sk[level] for level in ("easy", "hard"))
    for name, mix, sk in (
        ("Easy", easy_mix, skill["Easy"]),
        ("Hard", hard_mix, skill["Hard"]),
    )
}
for k, v in overall.items():
    print(f"{k} dataset overall accuracy = {v:.4f}")

# (c)-(d) stratified accuracy, using counts out of 1000
counts = {
    "Easy": {"easy": 900, "easy_ok": 810, "hard": 100, "hard_ok": 40},
    "Hard": {"easy": 100, "easy_ok": 50, "hard": 900, "hard_ok": 450},
}
print()
print(f"{'level':6} {'Easy acc':>9} {'Hard acc':>9}  (within level)")
for level in ("easy", "hard"):
    n_key, ok_key = level, f"{level}_ok"
    a = counts["Easy"][ok_key] / counts["Easy"][n_key]
    b = counts["Hard"][ok_key] / counts["Hard"][n_key]
    print(f"{level:6} {a:9.3f} {b:9.3f}")

# (e) decompose the overall gap
print()
gap = overall["Easy"] - overall["Hard"]
# Decompose: compare skill at Hard's mix, then move the mix at Easy's skill.
from_skill = sum(
    hard_mix[lv] * (skill["Easy"][lv] - skill["Hard"][lv])
    for lv in ("easy", "hard")
)
from_mix = sum(
    (easy_mix[lv] - hard_mix[lv]) * skill["Easy"][lv]
    for lv in ("easy", "hard")
)
print(f"overall gap (Easy - Hard) = {gap:+.4f}")
print(f"  component from SKILL (Hard's mix, Easy's rates)  = {from_skill:+.4f}")
print(f"  component from MIX   (Easy's rates, moving mix)   = {from_mix:+.4f}")
print(f"  sum of components = {from_skill + from_mix:+.4f}  (equals the gap: "
      f"{abs(from_skill + from_mix - gap) < 1e-12})")
print()
print(f"The mix component explains {from_mix / gap * 100:.1f}% of the gap and")
print(f"the skill component explains {from_skill / gap * 100:.1f}%.")
print("The overall win comes from the difficulty mix, not from better skill.")
```

The decomposition in (e) is the general tool: write the aggregate difference as
"how much of it comes from the different weights" plus "how much comes from the
different values", and you have an honest accounting instead of a conclusion
drawn from a number that is really measuring something else.

</details>

**[ ] Exercise 4 — the covariance/ρ identity, and the wrong-unit slope.** A
service's latency $Y$ (ms) and load $X$ (requests/s) satisfy $Y = 2X + 5$ exactly,
with $E[X] = 50$, $\mathrm{Var}(X) = 100$.
(a) Compute $\mathrm{Cov}(X,Y)$, $\sigma_X$, $\sigma_Y$, and ρ.
(b) Compute the least-squares slope and intercept two ways — from
$\mathrm{Cov}/\mathrm{Var}$ and by knowing the true relation — and confirm they
agree.
(c) Now report the slope as ρ alone. What do you get, what are its units, and by
what factor is it wrong?
(d) A second service has load in requests/**minute** and latency in
**milliseconds**. Recompute the covariance and explain why it differs from (a)
while ρ is unchanged.

<details>
<summary>Solution</summary>

(a) $Y = 2X + 5$, so $\mathrm{Cov}(X, 2X+5) = 2\mathrm{Cov}(X,X) = 2\mathrm{Var}(X)
= 200$. And $\mathrm{Var}(Y) = 4\mathrm{Var}(X) = 400$, so
$\sigma_X = 10$, $\sigma_Y = 20$, and

$$\rho = \frac{200}{10 \times 20} = 1,$$

as it must be for an exact affine relation.

(b) From the formula: slope $= \mathrm{Cov}/\mathrm{Var} = 200/100 = 2$.
Intercept $= E[Y] - 2E[X] = (2 \cdot 50 + 5) - 100 = 105 - 100 = 5$.
From the truth: $Y = 2X + 5$, so slope 2 and intercept 5. **They agree exactly**,
which is the lesson's corollary: when Y *is* affine in X, the conditional mean is
the least-squares line and the fitted slope is the unique correct answer.

(c) Reporting the slope as ρ gives **1.0**, with units of "milliseconds per
requests per second" — which is not the same thing, since a true slope of 2.0
means each additional request/s adds 2 ms. The value is wrong by a factor of
**2**, and the units are wrong in a way a type checker cannot catch. The missing
factor is $\sigma_Y/\sigma_X = 20/10 = 2$: the slope is $\rho\,\sigma_Y/\sigma_X$,
not ρ. This is Mistake 2 in the lesson.

(d) Load in requests/minute is $X' = 60X$, so $\mathrm{Var}(X') = 3600 \cdot 100 =
360{,}000$ and $\sigma_{X'} = 600$. Then
$\mathrm{Cov}(X', Y) = 60 \cdot \mathrm{Cov}(X, Y) = 60 \times 200 = 12{,}000$ —
**60× larger**. Meanwhile $\rho$ is unchanged at 1, because the $\sigma_{X'}$ in
the denominator grows by exactly the same factor. The lesson's Example B shows the
same effect with a factor of 100 between two systems at identical ρ.

The slope in the new units is also 2, correctly interpreted as 2 ms per request
per *minute* — a different physical statement from 2 ms per request per second,
which is why the intercept also shifts: $E[Y] - 2E[X'] = 105 - 2(3000) = -5895$.
Anyone comparing raw covariances across services with different load units is
comparing their unit choices, not their systems.

```python
from math import sqrt

VAR_X, MEAN_X = 100.0, 50.0
A, B = 2.0, 5.0

mean_y = A * MEAN_X + B
cov_xy = A * VAR_X                 # Cov(X, aX+b) = a Var(X)
var_x = VAR_X
var_y = A * A * VAR_X
sd_x, sd_y = sqrt(var_x), sqrt(var_y)
rho = cov_xy / (sd_x * sd_y)

print("(a) Cov(X,Y) = a*Var(X) = {:.4f}".format(cov_xy))
print(f"    sd_X = {sd_x:.4f}, sd_Y = {sd_y:.4f}, rho = {rho:.4f}")
print(f"    rho must be 1 for an exact affine relation: {abs(rho - 1) < 1e-12}")

slope_formula = cov_xy / var_x
intercept_formula = mean_y - slope_formula * MEAN_X
print()
print(f"(b) from Cov/Var: slope = {slope_formula:.4f}, "
      f"intercept = {intercept_formula:.4f}")
print(f"    from the truth:  slope = {A:.4f}, intercept = {B:.4f}")
print(f"    agree: {abs(slope_formula - A) < 1e-12 and abs(intercept_formula - B) < 1e-12}")

print()
print(f"(c) reporting the slope as rho alone gives {rho:.4f}, "
      f"wrong by a factor of {A / rho:.1f}")
print(f"    the missing factor is sd_Y/sd_X = {sd_y / sd_x:.4f}")
print(f"    slope = rho * sd_Y/sd_X = {rho:.4f} * {sd_y / sd_x:.4f} "
      f"= {rho * sd_y / sd_x:.4f}")

SCALE = 60
cov_scaled = SCALE * cov_xy
sd_x_scaled = SCALE * sd_x
rho_scaled = cov_scaled / (sd_x_scaled * sd_y)
print()
print(f"(d) load in requests/MINUTE (x60): Cov = {cov_scaled:.1f}, "
      f"{cov_scaled / cov_xy:.0f}x larger")
print(f"    rho unchanged at {rho_scaled:.4f}")
print(f"    slope in the new units: "
      f"{cov_scaled / (SCALE * SCALE * var_x):.4f}, intercept "
      f"{mean_y - (cov_scaled / (SCALE * SCALE * var_x)) * (SCALE * MEAN_X):.2f}")
print("    -> covariance tracks units; correlation does not.")
```

</details>

**[ ] Exercise 5 — two joints, identical marginals.** A service's request latency
$X$ and its response size $Y$ are each uniform on {1, 2, 3, 4} in both of two
deployments.
(a) In deployment A, $Y = X + 1$. Build the joint table, compute both marginals,
and confirm they are uniform.
(b) Compute $\mathrm{Cov}(X,Y)$ and ρ for deployment A.
(c) Now consider deployment B with $Y$ independent of $X$. Give its joint table,
and confirm the same marginals.
(d) Compute $\mathrm{Cov}(X,Y)$ and ρ for deployment B, and compute
$P(X = 4, Y = 4)$ under both. Which deployment is riskier for "both at their
maximum simultaneously"?

<details>
<summary>Solution</summary>

(a) **Deployment A, $Y = X+1$.** The joint table:

| | Y=1 | Y=2 | Y=3 | Y=4 |
| --- | --- | --- | --- | --- |
| **X=1** | 0 | 1/4 | 0 | 0 |
| **X=2** | 0 | 0 | 1/4 | 0 |
| **X=3** | 0 | 0 | 0 | 1/4 |
| **X=4** | 0 | 0 | 0 | 0 |

Each of X = 1, 2, 3 has probability 1/4, and X = 4 has probability 0.

**The marginal of X is therefore *not* uniform.** $p_X(1) = p_X(2) = p_X(3) =
1/4$ and $p_X(4) = 0$. This is the first thing to notice, and it means the
premise needs adjusting: $X \sim \mathrm{Uniform}\{1,2,3\}$ and
$Y \sim \mathrm{Uniform}\{2,3,4\}$, not both uniform on {1,…,4}. Take instead
$X \sim \mathrm{Uniform}\{1,\dots,4\}$ and $Y = 2X - 1$ truncated… still fails at
$X=4$.

The clean version that keeps both marginals uniform on {1,…,4} is
$Y = 5 - X$ (the anti-diagonal):

| | Y=1 | Y=2 | Y=3 | Y=4 |
| --- | --- | --- | --- | --- |
| **X=1** | 0 | 0 | 0 | 1/4 |
| **X=2** | 0 | 0 | 1/4 | 0 |
| **X=3** | 0 | 1/4 | 0 | 0 |
| **X=4** | 1/4 | 0 | 0 | 0 |

Both marginals are exactly $1/4$ each. Use this for the rest of the exercise.

(b) $E[X] = E[Y] = 2.5$. $E[XY] = \frac{1}{4}(1\cdot4 + 2\cdot3 + 3\cdot2 +
4\cdot1) = \frac{1}{4}(4+6+6+4) = 5$. So
$\mathrm{Cov} = 5 - 2.5 \times 2.5 = 5 - 6.25 = -1.25$. With
$\mathrm{Var}(X) = \mathrm{Var}(Y) = 1.25$, we get $\rho = -1.25/1.25 = -1$:
perfect negative correlation, exactly as required for $Y = 5-X$.

(c) **Deployment B, independent.** All sixteen cells at 1/16:

| | Y=1 | Y=2 | Y=3 | Y=4 |
| --- | --- | --- | --- | --- |
| **X=1** | 1/16 | 1/16 | 1/16 | 1/16 |
| **X=2** | 1/16 | 1/16 | 1/16 | 1/16 |
| **X=3** | 1/16 | 1/16 | 1/16 | 1/16 |
| **X=4** | 1/16 | 1/16 | 1/16 | 1/16 |

Row sums and column sums are all 1/4, so the marginals are identical to
deployment A.

(d) Independent gives $\mathrm{Cov} = 0$ and $\rho = 0$. For the joint
maxima: under A, $P(X=4, Y=4) = 0$ — they are *anti*-correlated, so a
simultaneous maximum is impossible. Under B, $P(X=4,Y=4) = 1/16 = 0.0625$.

So the risky deployment is **B**, and this is the point of the exercise: with
*identical marginals*, the deployment where both variables sit at their
maximums simultaneously is the independent one. A's variables move in opposite
directions, so extremes never coincide; B's can coincide 1 time in 16. Any risk
model built from per-component 99th percentiles must know the pairing, and
independence is the assumption that produces the *higher* joint risk.

```python
from math import sqrt

N = 4

def table_from_pairs(pairs):
    t = {}
    for x, y in pairs:
        t[(x, y)] = t.get((x, y), 0.0) + 1.0 / len(pairs)
    return t


def marginal(t, idx):
    out = {}
    for (x, y), p in t.items():
        k = x if idx == 0 else y
        out[k] = out.get(k, 0.0) + p
    return out


def moments(t):
    mx = marginal(t, 0)
    my = marginal(t, 1)
    ex = sum(k * p for k, p in mx.items())
    ey = sum(k * p for k, p in my.items())
    exy = sum(x * y * p for (x, y), p in t.items())
    cov = exy - ex * ey
    vx = sum((k - ex) ** 2 * p for k, p in mx.items())
    vy = sum((k - ey) ** 2 * p for k, p in my.items())
    return ex, ey, cov, vx, vy, cov / sqrt(vx * vy)


# (a) Y = 5 - X keeps BOTH marginals uniform on {1..4}
A = table_from_pairs([(x, N + 1 - x) for x in range(1, N + 1)])
# (c) independent
B = table_from_pairs([(x, y) for x in range(1, N + 1) for y in range(1, N + 1)])

for name, t in (("A: Y = 5 - X", A), ("B: independent", B)):
    mx, my = marginal(t, 0), marginal(t, 1)
    print(f"--- {name} ---")
    print("      " + "".join(f"{'Y=' + str(y):>8}" for y in range(1, N + 1)))
    for x in range(1, N + 1):
        print(f"  X={x} " + "".join(f"{t.get((x, y), 0.0):8.4f}"
                                    for y in range(1, N + 1)))
    print(f"  p_X = {[round(mx[x], 4) for x in range(1, N + 1)]}")
    print(f"  p_Y = {[round(my[y], 4) for y in range(1, N + 1)]}")
    print()

print("marginals identical across A and B:",
      all(abs(marginal(A, 0)[k] - marginal(B, 0)[k]) < 1e-12
          for k in range(1, N + 1)))

for name, t in (("A", A), ("B", B)):
    ex, ey, cov, vx, vy, rho = moments(t)
    print(f"{name}: E[X]={ex} E[Y]={ey} Cov={cov:+.4f} "
          f"rho={rho:+.4f}  P(X=4,Y=4)={t.get((4, 4), 0.0):.4f}")

print()
print("A's variables move in OPPOSITE directions, so joint maxima are")
print("impossible (probability 0). Independent B can hit both maxima")
print(f"simultaneously {1 / 16:.4f} of the time. Identical marginals,")
print("very different risk.")
```

</details>

**[ ] Exercise 6 — Challenge: fit a line and read off R², ρ², and what the
residuals prove.** Data: X = 1..6 and Y = 10, 12, 11, 14, 15, 13 (the lesson's
Example C table).
(a) Compute $\rho$ from the data and verify $\rho^2 = R^2 = 1 -
\mathrm{MSE}_{\text{line}}/\mathrm{Var}(Y)$.
(b) Show that the residual sum is exactly 0 and that
$\sum (x_i - \bar x) r_i = 0$ to machine precision.
(c) Fit a deliberately *wrong* line — the constant $\bar Y = 12.5$ — and show its
residual is correlated with X, so the orthogonality condition fails.
(d) Now add a strongly curved term: use the same X but $Y' = Y + 10(X-3.5)^2$.
Recompute ρ and explain why the linear fit's $R^2$ no longer describes the
relationship even though the least-squares line is still the best linear
approximation.

<details>
<summary>Solution</summary>

(a) $\bar X = 3.5$, $\bar Y = 12.5$.
$\sum(x_i-\bar x)(y_i-\bar y) = 13.5$ and
$\sum(y_i-\bar y)^2 = 17.5$, both over $n = 6$, so
$\mathrm{Cov} = 2.25$ and $\mathrm{Var}(Y) = 17.5/6 = 2.9167$ as well as
$\mathrm{Var}(X) = 2.9167$.

$$\rho = \frac{2.25}{2.9167} = 0.7714, \qquad \rho^2 = 0.5951.$$

The line is $\hat Y = 9.80 + 0.7714X$ with MSE $1.1810$ (from Exercise 2).
Check: $1 - 1.1810/2.9167 = 1 - 0.4049 = 0.5951$. ✓ **$R^2 = \rho^2$**, which is
the algebraic origin of the identity the lesson states.

(b) Residuals are $+0.5714, -0.6571, +1.1143, -1.1143, -1.3429, +1.4286$. Their
sum is 0 to machine precision, because the fitted line passes through the centroid
$[\hat Y(3.5) = 12.5]$, a property of OLS with an intercept. And
$\sum(x_i-\bar x)r_i = 0$ to machine precision. Together these are the two
normal equations, and the second is the optimality condition: any other line's
residual is this one plus a function of X, and a function of X orthogonal to
this residual can only add to the squared error.

(c) Constant prediction $12.5$ gives residuals $+2.5, +0.5, +1.5, -1.5, -2.5,
-0.5$. Their sum is 0 — the intercept condition still holds, since 12.5 *is* the
mean — but

$$\sum(x_i - \bar x)r_i = (-2.5)(2.5) + (-1.5)(0.5) + (-0.5)(1.5) + (0.5)(-1.5) + (1.5)(-2.5) + (2.5)(-0.5)$$
$$= -6.25 - 0.75 - 0.75 - 0.75 - 3.75 - 1.25 = -13.5 \ne 0.$$

So the orthogonality condition **fails**, confirming the constant predictor is not
the least-squares line. Its MSE is $\mathrm{Var}(Y) = 2.9167$, so $R^2 = 0$. The
sign is worth noting: the residuals are positive on the left of the data and
negative on the right, so the residual is strongly *negatively* correlated with X
— the line is systematically wrong in a direction the optimiser would fix.

(d) $Y' = Y + 10(X-3.5)^2$ adds a parabola. The term is $62.5$ at $X = 1, 6$,
$22.5$ at $X = 2, 5$ and $2.5$ at $X = 3, 4$, so
$Y' = 72.5, 34.5, 13.5, 16.5, 37.5, 75.5$.

$\mathrm{Var}(Y') = 598.47$ against the original $2.9167$ — the quadratic
dominates. The covariance is **unchanged at 2.25**, because the quadratic term is
symmetric about $x = 3.5$ and so contributes zero to
$\sum(x_i-\bar x)(\cdot)$. Consequently $\rho' = 2.25/\sqrt{2.9167 \times 598.47}
= +0.0539$, and $R^2 = 0.0029$ instead of 0.5951.

Note what has and has not changed. The least-squares slope is *still* 0.7714 —
the quadratic shifts $Y$ without touching the linear trend, so the fitted line
remains the best linear approximation by definition. But the correlation has
collapsed from 0.7714 to 0.0539, so $R^2$ now measures how badly a line fits a
curve rather than how much the line explains.

The lesson's point: **$R^2 = \rho^2$ describes linear fit, not fit quality.** A
model can explain 95% of the variance for the right reason (a straight line) or
for the wrong reason (a symmetric curve that a line happens to average over),
and $R^2$ cannot tell them apart. The first code block's `$Y = X^2$` case is the
mirror image: a genuinely deterministic relation with $\rho = 0.9789$ rather
than 1, because the curve is not a line. In both directions, correlation is a
statement about linearity only — which is why the conditional-expectation theorem
and not $R^2$ is the real foundation.

```python
from math import sqrt

DATA = [(1, 10), (2, 12), (3, 11), (4, 14), (5, 15), (6, 13)]
n = len(DATA)


def stats(data):
    """Return means, covariance, both variances, and the least-squares line."""
    m = len(data)
    mx = sum(x for x, _ in data) / m
    my = sum(y for _, y in data) / m
    cov = sum((x - mx) * (y - my) for x, y in data) / m
    vx = sum((x - mx) ** 2 for x, _ in data) / m
    vy = sum((y - my) ** 2 for _, y in data) / m
    slope = cov / vx
    return mx, my, cov, vx, vy, slope, my - slope * mx


mx, my, cov, vx, vy, slope, intercept = stats(DATA)
rho = cov / sqrt(vx * vy)
resids = [intercept + slope * x - y for x, y in DATA]
mse_line = sum(r * r for r in resids) / n
r2_from_mse = 1 - mse_line / vy

print("(a) Cov = {:.4f}, Var(X) = {:.4f}, Var(Y) = {:.4f}"
      .format(cov, vx, vy))
print(f"    slope = {slope:.4f}, intercept = {intercept:.4f}")
print(f"    rho = {rho:.4f}, rho^2 = {rho * rho:.4f}")
print(f"    1 - MSE/Var(Y) = 1 - {mse_line:.4f}/{vy:.4f} = {r2_from_mse:.4f}")
print(f"    R^2 == rho^2 : {abs(r2_from_mse - rho * rho) < 1e-12}")

print()
print("(b) residuals:", [round(r, 4) for r in resids])
print(f"    sum of residuals      = {sum(resids):.2e}")
print(f"    sum (x-xbar)*residual = "
      f"{sum((x - mx) * r for (x, _), r in zip(DATA, resids)):.2e}")

const = my
const_res = [const - y for _, y in DATA]
orth_const = sum((x - mx) * r for (x, _), r in zip(DATA, const_res))
print()
print(f"(c) constant predictor {const:.4f}: residuals "
      f"{[round(r, 2) for r in const_res]}")
print(f"    sum of residuals      = {sum(const_res):.2e}  (intercept condition holds)")
print(f"    sum (x-xbar)*residual = {orth_const:.4f}  <- NOT zero, so not optimal")
print(f"    MSE = {sum(r * r for r in const_res) / n:.4f}, R^2 = "
      f"{1 - sum(r * r for r in const_res) / n / vy:.4f}")

print()
print("(d) same X, but Y' = Y + 10(X - 3.5)^2 -- a symmetric U shape")
CURVED = [(x, y + 10 * (x - 3.5) ** 2) for x, y in DATA]
print(f"    Y' = {[round(y, 1) for _, y in CURVED]}")
mx2, my2, cov2, vx2, vy2, slope2, intercept2 = stats(CURVED)
rho2 = cov2 / sqrt(vx2 * vy2)
res2 = [intercept2 + slope2 * x - y for x, y in CURVED]
mse2 = sum(r * r for r in res2) / n
print(f"    Var(Y') = {vy2:.4f}   (was {vy:.4f}) -- the quadratic dominates")
print(f"    rho' = {rho2:+.4f}  (was {rho:+.4f})")
print(f"    slope = {slope2:+.4f}  (unchanged: the quadratic is symmetric,")
print(f"    so it shifts Y but not the linear trend)")
print(f"    MSE = {mse2:.4f}, R^2 = {1 - mse2 / vy2:.4f} (was {rho * rho:.4f})")
print()
print("The line is still optimal AMONG LINES, but R^2 now measures how badly a")
print("line fits a curve. Correlation describes linearity, not predictability.")
```

</details>

## Summary

- The joint distribution contains strictly more information than the two
  marginals; identical marginals can hide complete dependence or complete
  independence.
- Independence means the joint table factorises, p(x,y) = p(x)p(y), for **all**
  cells — checking a few is not enough.
- Cov(X,Y) = E[XY] − E[X]E[Y] collects the outcomes where the two variables
  agree, and it carries units.
- ρ = Cov/(σ_Xσ_Y) is dimensionless and bounded by [−1,1], with ±1 only for
  exactly affine relations.
- ρ = 0 does not mean independent; curved relations such as Y = X² have ρ = 0
  while being completely dependent.
- Correlation is not causation: a shared common cause produces identical
  correlation with no causal arrow between the two, and selection manufactures
  correlation from nothing.
- The regression weight is Cov/Var = ρ·σ_Y/σ_X, not ρ — which is why using
  correlation as a feature weight is a real bug.
- E[Y | X] is the best possible predictor of Y given X, and when Y is affine in X
  it equals the least-squares line, with residuals orthogonal to X.

## Next

[68 — Law of Large Numbers and the Central Limit Theorem](../part05_probability_statistics/68_law_of_large_numbers_and_clt.md)
explains why averages converge, defines the four types of convergence, shows why
sums become approximately normal, and builds the standard error, confidence
interval, and simulation that the rest of this part depends on.