# 100 — Convexity

**Part**: part08_optimization · **Prerequisites**: 51, 53, 54 · **Time**: 35 min

---

## In Plain Words

A set is convex if it has no dents. Draw any two points inside it, draw the
straight line between them, and the whole line stays inside. That is the entire
definition, and it sounds almost too weak to matter. It matters enormously.

A function is convex if its graph is shaped like a bowl — the middle always sits
below the straight line joining any two points on it. Concave is the mirror
image, like a dome. Most of the functions you optimise in machine learning are
either exactly convex or very nearly so, and that near-convexity is what makes
training tractable.

The payoff is a guarantee that changes how you write optimisers. For a convex
function there is exactly one bottom of the bowl. Get anywhere on the slope and
keep walking downhill and you cannot help but end up at it. For a function with
dents, walking downhill can strand you in a ditch that is not the bottom at all,
with no local signal telling you that you are stuck. Convexity is the property
that lets you treat "keep going downhill" as a correct algorithm rather than a
hope.

## Why Computer Science Cares

- **Every loss function in linear regression** is convex in the weights, which
  is why `scikit-learn`'s `LinearRegression` can use ordinary least squares and
  converge without tuning.
- **L2 regularisation** (ridge regression, weight decay) adds a convex term to a
  convex objective and keeps it convex. **L1 does not** — and the resulting
  non-convexity is exactly why L1 produces sparse solutions and needs
  subgradients, coordinate descent, or proximal methods instead of plain gradient
  descent.
- **Logistic regression** is convex in the weights even though the model is a
  sigmoid, because the log-likelihood curvature is positive. This surprises
  people and is worth memorising.
- **Convex programs are solvable in polynomial time** (interior-point and
  subgradient methods), and the [linear programming](../part02_discrete_combinotics/)
  and [quadratic programming](../part03_linear_algebra/) problems inside them are
  handled by mature solvers. Non-convex equivalents are NP-hard in general.
- **The Lagrangian dual** of a non-convex problem is often a convex problem, which
  is the entire reason [dual methods work](102_lagrange_multipliers_and_knt.md).
- **The perceptron's convergence proof** requires separability and relies on
  convexity of the margin, which is why adding a bias term to the perceptron
  breaks its convergence guarantee.

## The Formal Version

Notation follows [SYMBOLS.md](../SYMBOLS.md).

**Definition.** A set S ⊆ ℝⁿ is *convex* if for every x, y ∈ S and every
t ∈ [0, 1], the point (1 − t)x + ty is in S. Such a point is a *convex
combination* of x and y.

**Definition.** The *convex hull* conv(S) is the intersection of all convex sets
containing S — equivalently, the set of all convex combinations of points of S.
This is the object computed by
[Lesson 92](../part07_geometry_graphics/92_geometric_algorithms.md).

**Theorem.** conv(S) = conv(H) where H ⊆ S is the set of extreme points of S.
*Convexity is preserved when interior points are deleted.*

**Explanation.** A convex combination of points of S can be rewritten as a
convex combination of the extreme points of conv(S), so the two sets contain each
other. This is why hull algorithms discard so aggressively, and why the hull is a
valid collision proxy.

**Definition.** A function f : C → ℝ on a convex domain C is *convex* if
f((1 − t)x + ty) ≤ (1 − t)f(x) + t f(y) for all x, y ∈ C, t ∈ [0, 1].

**Theorem (Jensen's inequality).** If f is convex and wᵢ ≥ 0 with Σᵢ wᵢ = 1, then

  f(Σᵢ wᵢxᵢ) ≤ Σᵢ wᵢ f(xᵢ)

for any points xᵢ. This is the definition above applied repeatedly.

**Explanation.** Induction. Combining two points with the two-point inequality
gives the case of two weights; combining that result with the next point gives
three, and so on. The statement is the single most useful inequality in
optimisation — it is what lets you replace a hard average-of-functions bound with
an easy one.

**Definition.** f is *strictly convex* if the inequality above is strict whenever
x ≠ y and 0 < t < 1.

**Definition.** f is *affine* if equality always holds: f((1−t)x + ty) =
(1−t)f(x) + t f(y). Affine functions are convex but not strictly convex, unless
the domain is a single point.

**Theorem.** If f is convex on an open set then f is continuous there. If f is
convex on a convex set C and t ∈ [0,1), then the one-sided slope is monotone:

  (f(y) − f(x))/(y − x) ≤ (f(z) − f(y))/(z − y)  whenever x < y < z.

**Explanation.** The slope inequality is the discrete form of "the derivative
never decreases". It is the reason a convex function has at most one minimum,
and the reason the curve has no flat-then-steepened-then-flat shape.

**Theorem (local implies global for convex f).** If f is convex and x* is a local
minimum, then x* is a global minimum. If f is *strictly* convex, x* is the
*unique* global minimum.

**Explanation.** Assume there is a y with f(y) < f(x*). Since f is convex, the
slope into x* from the left must be at most the slope out of x* to the right.
With f(y) < f(x*) on one side, the right-hand slope must be positive, so moving
slightly right from x* decreases f — contradicting local minimality. Strict
convexity then forces the set of minimisers to be a single point.

**Definition.** The *Hessian* of f : ℝⁿ → ℝ is the n×n matrix of second partial
derivatives, Hᵢⱼ = ∂²f/∂xᵢ∂xⱼ. It is always symmetric when the mixed partials
exist.

**Theorem (second-order test).** Let f be twice continuously differentiable and
suppose x* is a stationary point (∇f(x*) = 0).

- H(x*) positive definite ⟹ x* is a **strict** local minimum.
- H(x*) negative definite ⟹ x* is a strict local maximum.
- H(x*) indefinite (some positive and some negative eigenvalue) ⟹ x* is a
  saddle point.
- H(x*) singular ⟹ the test is **inconclusive**.

**Definition.** A symmetric matrix H is *positive definite* if xᵀHx > 0 for all
x ≠ 0. It is *negative definite* if xᵀHx < 0 for all x ≠ 0. It is *positive
semidefinite* if xᵀHx ≥ 0.

**Theorem (equivalences).** H is positive definite ⟺ all eigenvalues of H are
positive ⟺ all leading principal minors are positive (Sylvester's criterion).

**Explanation.** The eigenvalue version follows by writing x in an orthonormal
eigenbasis, where xᵀHx = Σᵢ λᵢcᵢ², a positive combination of eigenvalues. This
is why `np.linalg.eigvalsh` is the numerically preferred check.

**Theorem (quadratic case).** For f(x) = ½xᵀHx + bᵀx, convexity of f is exactly
positive semidefiniteness of H, and strict convexity is exactly positive
definiteness. So a quadratic is convex ⟺ its Hessian is PSD ⟺ all eigenvalues
are ≥ 0.

**Theorem (composition rules).** These are the rules you use to prove a function
convex without expanding anything:

1. A non-negative affine combination of convex functions is convex:
   αf + βg is convex if α, β ≥ 0.
2. The maximum of convex functions is convex: max(f, g) is convex.
3. The minimum is **not**: min(f, g) is generally concave-ish.
4. A convex non-decreasing function composed with a convex function is convex.
5. An affine function composed with a convex function is convex.

**Explanation.** Rule 2 is the surprising one. Take the max of two convex
functions: the max is the larger of two bowls, and the larger bowl is still a
bowl. Taking the min carves a valley between them, which is exactly how you
produce a non-convex objective. **This is why softplus-style relaxations use max
and L1's exact min-over-slopes structure destroys convexity.**

**Theorem (strictly convex ⟹ unique minimiser).** If f is strictly convex on a
convex set and attains its minimum at x*, then x* is the unique minimiser.
Convex but not strictly convex may have a whole flat region of minimisers.

## Worked Example

Take the two-variable function f(x, y) = x² + 3xy + 5y².

**Step 1 — the Hessian.** Differentiate twice.

fₓ = 2x + 3y, so fₓₓ = 2 and fₓᵧ = 3.
f_y = 3x + 10y, so f_yy = 10 and f_yx = 3.

H = [[2, 3], [3, 10]]. It is symmetric, as it must be.

**Step 2 — Sylvester's criterion.** Leading principal minors:

D₁ = 2 > 0.
D₂ = det(H) = 2·10 − 3·3 = 20 − 9 = 11 > 0.

Both positive, so H is positive definite, so f is **strictly convex**.

**Step 3 — verify with eigenvalues.** The characteristic equation is
λ² − 12λ + 11 = 0, so λ = (12 ± √(144 − 44))/2 = (12 ± 10)/2, giving
λ₁ = 1 and λ₂ = 11. Both positive, which agrees with Sylvester. Trace = 12 = 1 + 11
and det = 11 = 1 · 11, both consistent.

**Step 4 — verify convexity directly, from the definition.** Take x = (1, 0) and
y = (0, 1).

f(1,0) = 1, f(0,1) = 5.
At t = 0.5 the midpoint is (0.5, 0.5):
f(0.5, 0.5) = 0.25 + 3(0.25) + 5(0.25) = 0.25 + 0.75 + 1.25 = 2.25.

The average of the endpoints is (1 + 5)/2 = 3. Since 2.25 ≤ 3, Jensen holds for
this pair. The gap is 0.75.

**Step 5 — the same gap has a closed form.** For a quadratic with positive
definite Hessian, the Jensen gap is

  (1−t)f(x) + tf(y) − f((1−t)x + ty) = ½(1−t)t · (x − y)ᵀ H (x − y)

With t = 0.5, x − y = (1, −1):
(x−y)ᵀH(x−y) = [1, −1]·[[2,3],[3,10]]·[1,−1]ᵀ = [1,−1]·[2−3, 3−10]ᵀ = [1,−1]·[−1,−7]ᵀ
= −1 + 7 = 6.

Gap = ½ · 0.5 · 0.5 · 6 = ½ · 0.25 · 6 = 0.75. Matches exactly.

This closed form is worth memorising because it says the gap is a positive
multiple of a positive-definite quadratic form. It is positive whenever x ≠ y,
which is precisely strict convexity, proved without a single derivative
argument.

**Step 6 — a concave-looking sibling.** Now take g(x, y) = x² + 3xy + **1**·y².
The Hessian is [[2, 3], [3, 1]], with det = 2 − 9 = −7 < 0. Not positive
definite, so g is not convex — it is a saddle. Check the same midpoint: g(0.5,0.5)
= 0.25 + 0.75 + 0.25 = 1.25, while (g(1,0) + g(0,1))/2 = (1 + 1)/2 = 1. Since
1.25 > 1, Jensen **fails**. One computation, exactly as predicted.

## Runnable Code

Convexity of sets, convex combinations, and Jensen's inequality — plain Python.

```python
from math import exp, log


# --- 1. Convexity of a set, by finding a witness -----------------------
def segment_points(a, b, n=6):
    """n+1 points spread along the segment from a to b."""
    return [(a[0] + (b[0] - a[0]) * t / n, a[1] + (b[1] - a[1]) * t / n)
            for t in range(n + 1)]


def in_unit_disc(p):
    return p[0] ** 2 + p[1] ** 2 <= 1.0


def in_square(p):
    return -1.0 <= p[0] <= 1.0 and -1.0 <= p[1] <= 1.0


# A set containing two points but not the segment between them is not convex.
# This "dumbbell" is the top and bottom caps of the unit disc.
def in_dumbbell(p):
    return p[0] ** 2 + p[1] ** 2 <= 1.0 and abs(p[1]) >= 0.5


def sample_in(inside, n=200, seed=4):
    """Random points known to be inside the set, by rejection sampling."""
    import random
    random.seed(seed)
    found = []
    tries = 0
    while len(found) < n and tries < 200000:
        tries += 1
        p = (random.uniform(-2, 2), random.uniform(-2, 2))
        if inside(p):
            found.append(p)
    return found


def find_convexity_violation(inside, n=200, seed=4):
    """Return a point outside the set lying on a segment between two points
    inside it -- a certificate that the set is NOT convex. None means convex.
    """
    pts = sample_in(inside, n, seed)
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            for p in segment_points(pts[i], pts[j], 5):
                if not inside(p):
                    return (pts[i], pts[j], p)
    return None


print("unit disc convex? ", find_convexity_violation(in_unit_disc) is None)
print("square convex?    ", find_convexity_violation(in_square) is None)
violation = find_convexity_violation(in_dumbbell)
print("dumbbell convex?  ", violation is None)
print("  witness segment from", tuple(round(v, 3) for v in violation[0]),
      "to", tuple(round(v, 3) for v in violation[1]))
print("  contains a point outside the set:",
      tuple(round(v, 3) for v in violation[2]))
print("  is that witness outside the dumbbell?", not in_dumbbell(violation[2]))


# --- 2. Convex combinations ---------------------------------------------
def convex_combination(a, b, t):
    return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))


def weighted_combination(points, weights):
    total = sum(weights)
    xs = sum(p[0] * w for p, w in zip(points, weights)) / total
    ys = sum(p[1] * w for p, w in zip(points, weights)) / total
    return (xs, ys)


triangle = [(0.0, 0.0), (4.0, 0.0), (0.0, 3.0)]
print("\nconvex combination of (0,0) and (4,0) at t=0.25:",
      tuple(round(v, 6) for v in convex_combination((0, 0), (4, 0), 0.25)))
print("weighted mean of the triangle's vertices:",
      tuple(round(v, 6) for v in weighted_combination(triangle, [1, 1, 1])))
print("a weighted mean with a negative weight:",
      tuple(round(v, 6) for v in weighted_combination(triangle, [-1, 2, 2])))
print("  -> negative weights fall outside the definition, and the result")
print("     (2.667, 2.0) leaves the triangle, which is the whole point")


# --- 3. Convex functions and Jensen's inequality ------------------------
def f1(x):
    return x * x


def f2(x):
    return exp(x)


def f3(x):
    return -x * x                      # concave, not convex


def f4(x):
    return abs(x)                      # convex, but not strictly convex


def worst_jensen_gap(f, lo=-4.0, hi=4.0, n=200):
    """Smallest Jensen gap over all sampled pairs.

    Jensen's inequality for a convex f says
        f((a+b)/2) <= (f(a) + f(b))/2
    so the gap (average of f) - f(midpoint) must be >= 0. Convexity is exactly
    the statement that this holds for every pair, so the MINIMUM gap over all
    pairs is >= 0 if and only if the function is convex.
    """
    smallest = float("inf")
    for i in range(n + 1):
        a = lo + (hi - lo) * i / n
        for j in range(i + 1, n + 1):
            b = lo + (hi - lo) * j / n
            gap = (f(a) + f(b)) / 2.0 - f((a + b) / 2.0)
            smallest = min(smallest, gap)
    return smallest


print("\nsmallest Jensen gap over all sampled pairs (>= 0 means convex):")
for name, f in [("x^2", f1), ("exp(x)", f2), ("-x^2", f3), ("|x|", f4)]:
    print(f"  f(x) = {name:8s} -> {worst_jensen_gap(f):.12f}")


# Jensen with three points: the general statement.
def check_jensen(f, points, weights):
    """Sum of w_i f(x_i) minus f of the weighted mean. >= 0 means convex."""
    total = sum(weights)
    mean = sum(x * w for x, w in zip(points, weights)) / total
    lhs = sum(w * f(x) for x, w in zip(points, weights)) / total
    return lhs - f(mean)


xs = [0.0, 1.0, 3.0]
ws = [1.0, 2.0, 1.0]
print("\nJensen, 3 points at", xs, "weights", ws)
print(f"  f(x) = x^2    gap = {check_jensen(f1, xs, ws):.12f}  (>= 0: convex)")
print(f"  f(x) = -x^2   gap = {check_jensen(f3, xs, ws):.12f}  (< 0: fails)")


# Equality: Jensen is an equality for affine functions on the segment.
def f5(x):
    return 3.0 * x + 2.0


print(f"  f(x) = 3x+2   gap = {check_jensen(f5, xs, ws):.12f}  (== 0: affine)")
```

```
unit disc convex?  True
square convex?     True
dumbbell convex?   False
  witness segment from (0.147, -0.893) to (-0.761, 0.508)
  contains a point outside the set: (-0.216, -0.333)
  is that witness outside the dumbbell? True

convex combination of (0,0) and (4,0) at t=0.25: (1.0, 0.0)
weighted mean of the triangle's vertices: (1.333333, 1.0)
a weighted mean with a negative weight: (2.666667, 2.0)
  -> negative weights fall outside the definition, and the result
     (2.667, 2.0) leaves the triangle, which is the whole point

smallest Jensen gap over all sampled pairs (>= 0 means convex):
  f(x) = x^2      -> 0.000400000000
  f(x) = exp(x)   -> 0.000003737252
  f(x) = -x^2     -> -16.000000000000
  f(x) = |x|      -> 0.000000000000

Jensen, 3 points at [0.0, 1.0, 3.0] weights [1.0, 2.0, 1.0]
  f(x) = x^2    gap = 1.187500000000  (>= 0: convex)
  f(x) = -x^2   gap = -1.187500000000  (< 0: fails)
  f(x) = 3x+2   gap = 0.000000000000  (== 0: affine)
```

The `x^2` and `exp(x)` gaps are tiny but positive, not exactly zero — they are
small because the sampled grid happens to contain adjacent points whose chord is
short. The `|x|` gap is exactly 0 because the flat right half of `|x|` gives a
perfectly straight segment. `-x^2` is −16, decisively negative.

### Strict versus non-strict convexity

```python
from math import exp, sin, cos, sqrt


def jensen_gap(f, a, b, t):
    """How much f sits below the chord from a to b.

    gap = (1-t) f(a) + t f(b) - f((1-t)a + t b)

    For a convex f this is >= 0. It is exactly 0 along a flat region, which is
    how non-strict (linear) stretches show up.
    """
    return (1.0 - t) * f(a) + t * f(b) - f((1.0 - t) * a + t * b)


def f_quad(x):
    return x * x


def f_abs(x):
    return abs(x)                  # convex, but flat on (-inf, 0] and [0, inf)


def f_relu(x):
    return max(0.0, x)            # convex, flat on (-inf, 0]


def f_hinge(x):
    """max(0, |x| - 1): convex, and flat outside [-1, 1].

    Note this is NOT clamp(x, -1, 1) = min(1, max(-1, x)). That one has slopes
    0, then 1, then 0 -- the slope decreases at the top, so it is NOT convex.
    """
    return max(0.0, abs(x) - 1.0)


def f_quartic(x):
    return (x * x) ** 2            # convex AND strictly convex


print("Jensen gap at t = 0.5 (0 means the function is flat on that segment)")
for name, f in [("x^2", f_quad), ("|x|", f_abs), ("relu(x)", f_relu),
                ("max(0,|x|-1)", f_hinge), ("x^4", f_quartic)]:
    gaps = [jensen_gap(f, a, b, 0.5) for a, b in
            [(-3.0, 2.0), (0.0, 4.0), (-1.0, 0.0), (1.0, 3.0)]]
    print(f"  f(x) = {name:16s} gaps {['%.6f' % g for g in gaps]}")

print("\n  f_abs and f_relu have gaps of exactly 0 -- convex but NOT strictly convex.")
print("  f_quad and f_quartic have all gaps > 0 -- strictly convex.")
print("  f_hinge has some 0 gaps -- flat outside [-1, 1].")
print("  min(1, max(-1, x)) would give a gap of -0.5 and is NOT convex:")
print("    slopes go 0, then 1, then 0 -- and convex slopes never decrease.")

# A strictly convex function has at most one minimiser.
xs = [i / 100 for i in range(-500, 501)]
best = min(xs, key=f_quad)
print("\nx^2 on [-5, 5]: argmin =", best, " value =", f_quad(best))
print("number of grid points attaining the minimum:",
      sum(1 for x in xs if f_quad(x) == f_quad(best)))
```

```
Jensen gap at t = 0.5 (0 means the function is flat on that segment)
  f(x) = x^2              gaps ['6.250000', '4.000000', '0.250000', '1.000000']
  f(x) = |x|              gaps ['2.000000', '0.000000', '0.000000', '0.000000']
  f(x) = relu(x)          gaps ['1.000000', '0.000000', '0.000000', '0.000000']
  f(x) = max(0,|x|-1)     gaps ['1.500000', '0.500000', '0.000000', '0.000000']
  f(x) = x^4              gaps ['48.437500', '112.000000', '0.437500', '25.000000']

  f_abs and f_relu have gaps of exactly 0 -- convex but NOT strictly convex.
  f_quad and f_quartic have all gaps > 0 -- strictly convex.
  f_hinge has some 0 gaps -- flat outside [-1, 1].
  min(1, max(-1, x)) would give a gap of -0.5 and is NOT convex:
    slopes go 0, then 1, then 0 -- and convex slopes never decrease.

x^2 on [-5, 5]: argmin = 0.0  value = 0.0
number of grid points attaining the minimum: 1
```

`relu` and `max(0, |x| − 1)` matter for machine learning specifically: ReLU
networks, Huber loss, and the softplus relaxation are all convex but not
strictly convex, which is why the minimiser of a convex model is often not
unique — there are many equally good weight vectors, and which one you get
depends on your initialisation and regularisation.

### Why local implies global

The single most useful consequence of convexity, demonstrated on a function
where it fails.

```python
from math import cos, exp, log


def f_quadratic(x, y):
    return x * x + 2.0 * y * y


def f_rastrigin(x, y):
    """Non-convex: a bowl with many ripples on top."""
    return 20.0 + x * x + y * y - 10.0 * (cos(2.0 * 3.141592653589793 * x)
                                         + cos(2.0 * 3.141592653589793 * y))


def local_minima_on_grid(f, lo, hi, step):
    """Grid search for points that beat all eight neighbours."""
    pts = []
    n = int((hi - lo) / step)
    grid = {(i, j): f(lo + i * step, lo + j * step)
            for i in range(n + 1) for j in range(n + 1)}
    for i in range(1, n):
        for j in range(1, n):
            v = grid[(i, j)]
            neighbours = [grid[(i + di, j + dj)]
                          for di in (-1, 0, 1) for dj in (-1, 0, 1)
                          if (di, dj) != (0, 0)]
            if all(v < nb for nb in neighbours):
                pts.append((round(lo + i * step, 4), round(lo + j * step, 4),
                            round(v, 6)))
    return pts


print("=== convex function: quadratic ===")
mins_q = local_minima_on_grid(f_quadratic, -3.0, 3.0, 0.5)
print("grid on [-3, 3] step 0.5 -> local minima:", mins_q)
print("count:", len(mins_q), "(every hit is the same point)")

print("\n=== non-convex function: Rastrigin ===")
# Offset the grid so that (0, 0) is NOT a grid point. Otherwise the grid search
# lands exactly on the global minimum and hides the whole point of the example.
mins_r = local_minima_on_grid(f_rastrigin, -2.6, 2.6, 0.4)
print("grid on [-2.6, 2.6] step 0.4 -> local minima:", len(mins_r), "of them")
for p in mins_r[:5]:
    print("   ", p)
best = min(mins_r, key=lambda t: t[2])
print("lowest of the local minima:", best)
print("true global minimum is (0, 0) with value",
      round(f_rastrigin(0.0, 0.0), 6))
print("gap from the best local minimum found by grid search:",
      round(best[2] - f_rastrigin(0.0, 0.0), 6))
print("(a gradient method starting anywhere will typically stop near the")
print(" worst of these, not at (0, 0) -- that is why convexity matters)")


# --- composition rules ---------------------------------------------------
def is_convex_on_grid(f, lo=-3.0, hi=3.0, n=120, tol=1e-9):
    """1D convexity by finite differences: slopes must never decrease."""
    prev_slope = None
    xs = [lo + (hi - lo) * i / n for i in range(n + 1)]
    for i in range(n):
        slope = (f(xs[i + 1]) - f(xs[i])) / (xs[i + 1] - xs[i])
        if prev_slope is not None and slope < prev_slope - tol:
            return False
        prev_slope = slope
    return True


print("\n=== composition rules ===")
print("f(x)=x^2 convex?", is_convex_on_grid(lambda x: x * x))
print("exp(x^2) = exp o square, convex?",
      is_convex_on_grid(lambda x: exp(x * x)))
print("log(exp(x)) = x, convex?", is_convex_on_grid(lambda x: log(exp(x))))
print("max(x^2, 1) = max of two convex, convex?",
      is_convex_on_grid(lambda x: max(x * x, 1.0)))
print("min(x^2, 1) = min of two convex, convex?",
      is_convex_on_grid(lambda x: min(x * x, 1.0)))
print("sum of convex: x^2 + exp(x), convex?",
      is_convex_on_grid(lambda x: x * x + exp(x)))
print("NON-negative scaling: 5x^2, convex?", is_convex_on_grid(lambda x: 5 * x * x))
print("NEGATIVE scaling: -x^2, convex?", is_convex_on_grid(lambda x: -x * x))
print("nonlinear f(x^2) with f = -x^2, convex?",
      is_convex_on_grid(lambda x: -(x * x) * (x * x)))
print("  -> the outer function must be convex AND nondecreasing on the range")
```

```
=== convex function: quadratic ===
grid on [-3, 3] step 0.5 -> local minima: [(0.0, 0.0, 0.0)]
count: 1 (every hit is the same point)

=== non-convex function: Rastrigin ===
grid on [-2.6, 2.6] step 0.4 -> local minima: 25 of them
    (-1.8, -1.8, 20.29966)
    (-1.8, -1.0, 11.14983)
    (-1.8, -0.2, 17.09966)
    (-1.8, 1.0, 11.14983)
    (-1.8, 1.8, 20.29966)
lowest of the local minima: (-1.0, -1.0, 2.0)
true global minimum is (0, 0) with value 0.0
gap from the best local minimum found by grid search: 2.0
(a gradient method starting anywhere will typically stop near the)
( worst of these, not at (0, 0) -- that is why convexity matters)

=== composition rules ===
f(x)=x^2 convex? True
exp(x^2) = exp o square, convex? True
log(exp(x)) = x, convex? True
max(x^2, 1) = max of two convex, convex? True
min(x^2, 1) = min of two convex, convex? False
sum of convex: x^2 + exp(x), convex? True
NON-negative scaling: 5x^2, convex? True
NEGATIVE scaling: -x^2, convex? False
nonlinear f(x^2) with f = -x^2, convex? False
  -> the outer function must be convex AND nondecreasing on the range
```

Twenty-five local minima for Rastrigin, and the grid never lands on the true
answer. That is the practical meaning of convexity: the number of places a
solver can get stuck.

Note the `min(x², 1)` line. `min` of two convex functions is **not** convex,
and that is exactly the structural reason L1 regularisation ruins convexity. L1
is the minimum over candidate directions of a family of affine functions — and
min of affine is concave. L2 is `max(0, ...)`, a max of convex terms, which is
why it preserves convexity.

### Hessian computation in pure Python

Analytic second derivatives, then the same thing by finite differences.

```python
"""Hessian computation in pure Python: by definition, and by finite differences."""

from math import exp, sqrt


# --- 1. The definition: second partial derivatives, taken analytically ----
# f(x, y) = (1-x)^2 + 100 (y - x^2)^2  (Rosenbrock's function)
def f_rosenbrock(x, y):
    return (1.0 - x) ** 2 + 100.0 * (y - x * x) ** 2


def grad_rosenbrock(x, y):
    return (400.0 * x * (x * x - y) + 2.0 * (x - 1.0),
            200.0 * (y - x * x))


def hess_rosenbrock(x, y):
    """Rosenbrock's Hessian, written out by hand.

    f    = (1-x)^2 + 100(y - x^2)^2
    f_x  = 400x(x^2 - y) + 2(x - 1)
    f_y  = 200(y - x^2)

    f_xx = 400(3x^2 - y) + 2
    f_xy = -400x
    f_yy = 200
    """
    return [[400.0 * (3.0 * x * x - y) + 2.0, -400.0 * x],
            [-400.0 * x, 200.0]]


# --- 2. Numerical Hessian, by central differences -----------------------
def numeric_gradient(f, point, h=1e-6):
    """Central-difference partial derivatives: (f(x+h) - f(x-h)) / 2h."""
    g = []
    for i in range(len(point)):
        up = list(point)
        down = list(point)
        up[i] += h
        down[i] -= h
        g.append((f(*up) - f(*down)) / (2.0 * h))
    return g


def numeric_hessian(f, point, h=1e-5):
    """Second partials by central differences.

    Diagonal entries use a symmetric second difference of f. The mixed partial
    is taken as d/dy of the ANALYTIC f_x, because f_x is exact and avoids a
    second layer of rounding error.
    """
    x, y = point
    eps = h

    dxx = (f(x + eps, y) - 2.0 * f(x, y) + f(x - eps, y)) / (eps * eps)
    dyy = (f(x, y + eps) - 2.0 * f(x, y) + f(x, y - eps)) / (eps * eps)

    gx_up = grad_rosenbrock(x, y + eps)[0]
    gx_down = grad_rosenbrock(x, y - eps)[0]
    dxy = (gx_up - gx_down) / (2.0 * eps)

    return [[dxx, dxy], [dxy, dyy]]


# --- 3. Positive definiteness, by Sylvester's criterion ------------------
def is_positive_definite_2x2(h):
    """For a symmetric 2x2: H00 > 0 and det(H) > 0."""
    h00, h01 = h[0][0], h[0][1]
    h10, h11 = h[1][0], h[1][1]
    symmetric = abs(h01 - h10) < 1e-12
    det = h00 * h11 - h01 * h10
    return {
        "symmetric": symmetric,
        "H00": h00,
        "det": det,
        "positive definite": symmetric and h00 > 0 and det > 0,
    }


print("=== Rosenbrock's function ===")
print("f(1, 1) =", f_rosenbrock(1.0, 1.0), "(the global minimum)")
print("f(0, 0) =", f_rosenbrock(0.0, 0.0))
print("f(-1.2, 1.0) =", round(f_rosenbrock(-1.2, 1.0), 6))

print("\n--- analytic vs numerical gradient ---")
for point in [(1.0, 1.0), (0.0, 0.0), (2.0, 3.0), (-1.2, 1.0)]:
    ga = grad_rosenbrock(*point)
    gn = numeric_gradient(f_rosenbrock, point)
    print(f"  at {str(point):14s} analytic {tuple(round(v, 6) for v in ga)}"
          f"  numeric {tuple(round(v, 6) for v in gn)}")

print("\n--- analytic vs numerical Hessian ---")
for point in [(1.0, 1.0), (0.0, 0.0), (2.0, 3.0)]:
    ha = hess_rosenbrock(*point)
    hn = numeric_hessian(f_rosenbrock, point)
    err = max(abs(ha[i][j] - hn[i][j]) for i in range(2) for j in range(2))
    print(f"  at {str(point)}")
    print("    analytic :", [[round(v, 6) for v in r] for r in ha])
    print("    numeric  :", [[round(v, 4) for v in r] for r in hn])
    print("    max error:", round(err, 4))

print("\n--- positive definiteness at several points ---")
for point in [(1.0, 1.0), (0.0, 0.0), (2.0, 3.0), (-1.2, 1.0)]:
    h = hess_rosenbrock(*point)
    info = is_positive_definite_2x2(h)
    print(f"  at {str(point):14s} H00={info['H00']:10.4f}"
          f"  det={info['det']:12.4f}"
          f"  PD={info['positive definite']}")
```

```
=== Rosenbrock's function ===
f(1, 1) = 0.0 (the global minimum)
f(0, 0) = 1.0
f(-1.2, 1.0) = 24.2

--- analytic vs numerical gradient ---
  at (1.0, 1.0)     analytic (0.0, 0.0)  numeric (0.0, -0.0)
  at (0.0, 0.0)     analytic (-2.0, 0.0)  numeric (-2.0, 0.0)
  at (2.0, 3.0)     analytic (802.0, -200.0)  numeric (802.0, -200.0)
  at (-1.2, 1.0)    analytic (-215.6, -88.0)  numeric (-215.6, -88.0)

--- analytic vs numerical Hessian ---
  at (1.0, 1.0)
    analytic : [[802.0, -400.0], [-400.0, 200.0]]
    numeric  : [[802.0, -400.0], [-400.0, 200.0]]
    max error: 0.0
  at (0.0, 0.0)
    analytic : [[2.0, -0.0], [-0.0, 200.0]]
    numeric  : [[2.0, 0.0], [0.0, 200.0]]
    max error: 0.0
  at (2.0, 3.0)
    analytic : [[3602.0, -800.0], [-800.0, 200.0]]
    numeric  : [[3601.9999, -800.0], [-800.0, 200.0]]
    max error: 0.0001

--- positive definiteness at several points ---
  at (1.0, 1.0)     H00=  802.0000  det=    400.0000  PD=True
  at (0.0, 0.0)     H00=    2.0000  det=    400.0000  PD=True
  at (2.0, 3.0)     H00= 3602.0000  det=  80400.0000  PD=True
  at (-1.2, 1.0)    H00= 1330.0000  det=  35600.0000  PD=True
```

The analytic and numerical Hessians agree to four decimal places. The mixed
partial is the fragile one — computing it as a second difference of `f` rather
than a first difference of the exact gradient costs several digits of precision,
which is exactly why the code differentiates the gradient.

### With Libraries

The same ideas with numpy, which is how you would actually do this in
autodiff-free code. This block requires numpy and is not runnable in the standard
library alone.

```python
import numpy as np

print("numpy version:", np.__version__)

# --- Hessian as the Jacobian of the gradient ----------------------------
def f_rosenbrock(v):
    x, y = v
    return (1.0 - x) ** 2 + 100.0 * (y - x * x) ** 2


def grad_rosenbrock(v):
    x, y = v
    return np.array([400.0 * x * (x * x - y) + 2.0 * (x - 1.0),
                     200.0 * (y - x * x)])


def hess_rosenbrock(v):
    """Rosenbrock's Hessian, written out by hand."""
    x, y = v
    return np.array([[400.0 * (3.0 * x * x - y) + 2.0, -400.0 * x],
                     [-400.0 * x, 200.0]])


def hess_via_jac(v, step=1e-5):
    """Hessian = Jacobian of the gradient. Central differences of grad."""
    out = np.zeros((len(v), len(v)))
    for i in range(len(v)):
        e = np.zeros(len(v))
        e[i] = step
        out[:, i] = (grad_rosenbrock(v + e) - grad_rosenbrock(v - e)) / (2 * step)
    return out


v = np.array([2.0, 3.0])
print("analytic Hessian:\n", np.round(hess_rosenbrock(v), 6))
print("numerical Hessian:\n", np.round(hess_via_jac(v), 4))
print("max abs error:",
      float(np.max(np.abs(hess_rosenbrock(v) - hess_via_jac(v)))))

# --- Eigenvalues decide positive definiteness ---------------------------
print("\npositive definiteness via eigenvalues (eigvalsh for symmetric input):")
for point in [(1.0, 1.0), (0.0, 0.0), (2.0, 3.0), (-1.2, 1.0), (0.0, 3.0)]:
    H = hess_rosenbrock(np.array(point))
    eig = np.linalg.eigvalsh(H)
    print(f"  at {str(point):14s} eigenvalues {np.round(eig, 4).tolist()}"
          f"  PD={bool(eig[0] > 0)}")

# A positive determinant is NOT enough: this matrix is a saddle.
H_bad = np.array([[1.0, 2.0], [2.0, 1.0]])
print("\nsaddle Hessian [[1,2],[2,1]]:")
print("  eigenvalues:", np.round(np.linalg.eigvalsh(H_bad), 6).tolist(),
      " PD =", bool(np.linalg.eigvalsh(H_bad)[0] > 0))
print("  det =", round(float(np.linalg.det(H_bad)), 6),
      "-- a negative det rules PD out, but a positive det does not confirm it")

# --- Rosenbrock is NOT convex everywhere --------------------------------
xs = np.linspace(-3, 3, 121)
X, Y = np.meshgrid(xs, xs)

Hxx = 1200.0 * X * X - 400.0 * Y + 2.0
Hxy = -400.0 * X
Hyy = np.full_like(X, 200.0)
tr = Hxx + Hyy
det = Hxx * Hyy - Hxy * Hxy
disc = np.sqrt(np.maximum(tr * tr / 4.0 - det, 0.0))
lam_min = tr / 2.0 - disc

print("\nRosenbrock over a 121x121 grid on [-3, 3]^2:")
print("  smallest eigenvalue found:", round(float(lam_min.min()), 4))
print("  convex at every grid point?", bool(np.all(lam_min > 0)))
print("  fraction of the grid that is convex:",
      round(float(np.mean(lam_min > 0)), 4))

# The convex region is exactly the valley below the curve y = x^2.
# det(H) = 80000(x^2 - y) + 400, so PD requires y < x^2 + 0.005.
y_line = X * X
convex_mask = Y < y_line + 0.005
print("\n  fraction matching the analytic rule y < x^2 + 0.005:",
      round(float(np.mean(convex_mask)), 4))
print("  agreement between the two tests:",
      round(float(np.mean((lam_min > 0) == convex_mask)), 4))

print("\n  => Rosenbrock is convex only in its narrow valley. That is why it is")
print("     the standard NON-convex benchmark for gradient-based optimisers.")


# Compare with the same function at a smaller coefficient.
def lam_min_general(X, Y, a):
    hxx = 2.0 * a * (3.0 * X * X - Y) + 2.0
    hxy = -4.0 * a * X
    hyy = np.full_like(X, 2.0 * a)
    t = hxx + hyy
    d = hxx * hyy - hxy * hxy
    return t / 2.0 - np.sqrt(np.maximum(t * t / 4.0 - d, 0.0))


lm100 = lam_min_general(X, Y, 100.0)
lm1 = lam_min_general(X, Y, 1.0)
print("\n  same function with a = 1 instead of 100:")
print("    smallest eigenvalue over the grid:", round(float(lm1.min()), 4))
print("    convex everywhere?", bool(np.all(lm1 > 0)))
print("    (still no -- shrinking the ripples narrows the convex set but does")
print("     not remove it; only a quadratic is convex everywhere)")

# --- Jensen, vectorised over many random weightings ----------------------
rng = np.random.default_rng(0)
pts = rng.normal(size=(5, 2000))
w = rng.random(5)
w = w / w.sum()                        # non-negative, summing to 1

lhs = (w[:, None] * pts ** 2).sum(axis=0)      # sum_i w_i f(x_i)
mean = w @ pts                                 # weighted mean of the points
gap = lhs - mean ** 2                          # minus f(weighted mean)

print("\nJensen for f(x)=x^2 over 2000 random weightings of 5 points:")
print("  smallest gap:", round(float(gap.min()), 9))
print("  all gaps >= 0:", bool(np.all(gap >= 0)))

# The gap has a closed form: sum_{i<j} w_i w_j (x_i - x_j)^2.
closed_form = np.zeros(2000)
for i in range(5):
    for j in range(i + 1, 5):
        closed_form += w[i] * w[j] * (pts[i] - pts[j]) ** 2
print("  matches closed form sum_{i<j} w_i w_j (x_i-x_j)^2:",
      bool(np.allclose(gap, closed_form)))
```

```
numpy version: 2.4.6
analytic Hessian:
 [[3602. -800.]
  [-800.  200.]]
numerical Hessian:
 [[3602. -800.]
  [-800.  200.]]
max abs error: 5.761421562056057e-08

positive definiteness via eigenvalues (eigvalsh for symmetric input):
  at (1.0, 1.0)     eigenvalues [0.3994, 1001.6006]  PD=True
  at (0.0, 0.0)     eigenvalues [2.0, 200.0]  PD=True
  at (2.0, 3.0)     eigenvalues [21.2657, 3780.7343]  PD=True
  at (-1.2, 1.0)    eigenvalues [23.633, 1506.367]  PD=True
  at (0.0, 3.0)     eigenvalues [-1198.0, 200.0]  PD=False

saddle Hessian [[1,2],[2,1]]:
  eigenvalues: [-1.0, 3.0]  PD = False
  det = -3.0 -- a negative det rules PD out, but a positive det does not confirm it

Rosenbrock over a 121x121 grid on [-3, 3]^2:
  smallest eigenvalue found: -1198.0
  convex at every grid point? False
  fraction of the grid that is convex: 0.8092

  fraction matching the analytic rule y < x^2 + 0.005: 0.8092
  agreement between the two tests: 1.0

  => Rosenbrock is convex only in its narrow valley. That is why it is
     the standard NON-convex benchmark for gradient-based optimisers.

  same function with a = 1 instead of 100:
    smallest eigenvalue over the grid: -4.0
    convex everywhere? False
    (still no -- shrinking the ripples narrows the convex set but does
     not remove it; only a quadratic is convex everywhere)

Jensen for f(x)=x^2 over 2000 random weightings of 5 points:
  smallest gap: 0.01931111
  all gaps >= 0: True
  matches closed form sum_{i<j} w_i w_j (x_i-x_j)^2: True
```

Two results worth pausing on. First, at (0, 3) the Hessian has a **negative**
eigenvalue of −1198, so Rosenbrock is not convex there — and the eigenvalue test
agrees with the analytic rule `y < x² + 0.005` at **100%** of the 14,641 grid
points, which is a strong check that both are right. Second, the closed form for
the Jensen gap of a quadratic,
`Σ_{i<j} wᵢwⱼ(xᵢ − xⱼ)²`, is a sum of non-negative terms, which is a proof of
convexity of `x²` that uses no calculus at all.

## Common Mistakes

**1. Using `min` of convex functions and expecting convexity.** `min(x², 1)` is
not convex, and the code above catches it with a −0.5 Jensen gap. This is not a
contrived example: L1 regularisation is structurally a minimum over affine
functions, which is why it breaks convexity and requires subgradient or
proximal methods. If your loss has an L1 penalty, plain gradient descent on the
smooth part alone is not solving the problem you think it is.

**2. Treating a positive determinant as sufficient.** For a symmetric 2×2
matrix, `det > 0` happens both when both eigenvalues are positive and when one
is positive and one negative. The matrix [[1,2],[2,1]] has det = −3, but
[[−1,0],[0,−1]] has det = +1 and is negative definite. Check the sign of the
first diagonal entry too, or just check eigenvalues.

**3. Forgetting that the second-order test needs a stationary point.** A positive
definite Hessian at a point where the gradient is *not* zero tells you nothing
about minimisation — it only says the curvature is upward there. At (2, 3),
Rosenbrock's Hessian is positive definite, but (2, 3) is not a minimum because
the gradient is (802, −200). Always solve ∇f = 0 first, or run an optimiser.

**4. Assuming convexity is all-or-nothing.** It is not. Many real objectives
(every neural network with more than one hidden layer, for instance) are
neither convex nor wildly non-convex — they are "convex in the region near the
answer". Optimisers work anyway, and that near-convexity is worth more than
global convexity would be. Treat convexity as a strong guarantee when you have
it and a weak heuristic when you nearly have it.

**5. Claiming a Hessian-based test decided something it did not.** When the
Hessian is singular the test is inconclusive, and the code must say so. Silently
rounding a tiny eigenvalue to zero and reporting "not positive definite" turns
an inconclusive result into a wrong one — often for a function that genuinely is
convex but badly scaled.

## Exercises and Solutions

**[ ] Exercise 1 — ** Prove that the maximum of two convex functions is convex,
and that the minimum of two convex functions is not. Work in one dimension with
f(x) = x² and g(x) = x² − 4x + 4 = (x − 2)², evaluating both max(f, g) and
min(f, g) on a grid and reporting the smallest Jensen gap of each.

<details>
<summary>Solution</summary>

```python
def f(x):
    return x * x


def g(x):
    return (x - 2.0) ** 2


def jensen_gap(h, a, b, t):
    """(1-t) h(a) + t h(b) - h((1-t)a + t b). >= 0 for all pairs means convex."""
    return (1.0 - t) * h(a) + t * h(b) - h((1.0 - t) * a + t * b)


def smallest_gap(h, lo=-3.0, hi=5.0, n=120):
    worst = float("inf")
    at = None
    for i in range(n + 1):
        a = lo + (hi - lo) * i / n
        for j in range(n + 1):
            b = lo + (hi - lo) * j / n
            gap = jensen_gap(h, a, b, 0.5)
            if gap < worst:
                worst = gap
                at = (a, b)
    return worst, at


def h_max(x):
    return max(f(x), g(x))


def h_min(x):
    return min(f(x), g(x))


for name, h in [("f(x) = x^2", f), ("g(x) = (x-2)^2", g),
                ("max(f, g)", h_max), ("min(f, g)", h_min)]:
    worst, at = smallest_gap(h)
    verdict = "convex" if worst >= -1e-9 else "NOT convex"
    print(f"{name:18s} smallest gap = {worst:+.9f}  {verdict}")
    if worst < -1e-9:
        print(f"{'':18s}   worst pair a={at[0]:.4f} b={at[1]:.4f}")

# Show why: max(f,g) is f except on one side, and there it is g. Both pieces
# are convex and they meet at a single point, so the join is still convex.
print("\nwhere do f and g cross?")
for x in (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0):
    print(f"  x={x:.1f}  f={f(x):6.3f}  g={g(x):6.3f}"
          f"  max={h_max(x):6.3f}  min={h_min(x):6.3f}")

# The min of two convex functions has a V-shape notch at the crossing: a
# downward kink, which is exactly what breaks convexity.
c = 1.0
print(f"\nslopes near the crossing x = {c}:")
for x0, x1 in [(0.5, 1.0), (1.0, 1.5)]:
    print(f"  max slope over [{x0}, {x1}]: "
          f"{(h_max(x1) - h_max(x0)) / (x1 - x0):+.6f}")
    print(f"  min slope over [{x0}, {x1}]: "
          f"{(h_min(x1) - h_min(x0)) / (x1 - x0):+.6f}")
```

Output:

```
f(x) = x^2         smallest gap = +0.000000000  convex
g(x) = (x-2)^2     smallest gap = +0.000000000  convex
max(f, g)          smallest gap = +0.000000000  convex
min(f, g)          smallest gap = -1.000000000  NOT convex
                     worst pair a=0.0000 b=2.0000

where do f and g cross?
  x=0.0  f= 0.000  g= 4.000  max= 4.000  min= 0.000
  x=0.5  f= 0.250  g= 2.250  max= 2.250  min= 0.250
  x=1.0  f= 1.000  g= 1.000  max= 1.000  min= 1.000
  x=1.5  f= 2.250  g= 0.250  max= 2.250  min= 0.250
  x=2.0  f= 4.000  g= 0.000  max= 4.000  min= 0.000
  x=2.5  f= 6.250  g= 0.250  max= 6.250  min= 0.250
  x=3.0  f= 9.000  g= 1.000  max= 9.000  min= 1.000

slopes near the crossing x = 1.0:
  max slope over [0.5, 1.0]: -2.500000
  min slope over [0.5, 1.0]: +1.500000
  max slope over [1.0, 1.5]: +2.500000
  min slope over [1.0, 1.5]: -1.500000
```

The mechanism is clearest in the slopes, and it is the opposite of what you might
guess. `max(f, g)` has slope −2.5 *before* the crossing and +2.5 *after*: the
slope **increases**, from −2.5 to +2.5, and that upward jump at x = 1 is a
convex kink. `min(f, g)` has slope +1.5 before and −1.5 after: the slope
**decreases**, which is the definition of a concave kink.

So the V-shape is the convex one. Take the max of two curves and you get a
V-shaped valley; take the min and you get a Λ-shaped peak. That is worth
internalising because it explains the L1/L2 asymmetry directly — L1's
`max(0, ·)`-style structure introduces the *convext* kink and is fine, while
anything built from a min introduces a non-convex one.

The worst pair is (0, 2), where both endpoints have value 0 but the midpoint
(1, 1) has value 1. Gap = (0 + 0)/2 − 1 = −1.

</details>

</details>

**[ ] Exercise 2 — ** For the quadratic f(x, y) = x² + 3xy + 5y², verify all three
convexity tests and the closed-form Jensen gap: Sylvester's criterion,
eigenvalues, direct midpoint evaluation, and the formula
`½(1−t)t(x−y)ᵀH(x−y)`. Then repeat for g(x, y) = x² + 3xy + y² and show the tests
disagree in the way you would predict.

<details>
<summary>Solution</summary>

```python
from math import sqrt


def hess_f(x, y):
    return [[2.0, 3.0], [3.0, 10.0]]


def hess_g(x, y):
    """d2/dy2 of y^2 is 2, not 1 -- the Hessian is [[2,3],[3,2]]."""
    return [[2.0, 3.0], [3.0, 2.0]]


def det2(h):
    return h[0][0] * h[1][1] - h[0][1] * h[1][0]


def sylvester(h):
    """Symmetric matrix: PD iff H00 > 0 and det > 0."""
    return h[0][0] > 0 and det2(h) > 0


def eigenvalues_2x2(h):
    """Roots of lambda^2 - tr lambda + det = 0."""
    tr = h[0][0] + h[1][1]
    d = det2(h)
    disc = tr * tr - 4.0 * d
    if disc < 0:
        return None                      # complex: matrix is not symmetric
    root = sqrt(disc)
    return ((tr - root) / 2.0, (tr + root) / 2.0)


def f(x, y):
    return x * x + 3.0 * x * y + 5.0 * y * y


def g(x, y):
    return x * x + 3.0 * x * y + y * y


def midpoint_gap(fn, a, b, t=0.5):
    m = ((1 - t) * a[0] + t * b[0], (1 - t) * a[1] + t * b[1])
    return (1 - t) * fn(*a) + t * fn(*b) - fn(*m)


def closed_form_gap(h, a, b, t=0.5):
    """For a quadratic with Hessian H the gap is 0.5 (1-t) t (a-b)' H (a-b)."""
    d = [a[i] - b[i] for i in range(2)]
    quad = sum(d[i] * h[i][j] * d[j] for i in range(2) for j in range(2))
    return 0.5 * (1 - t) * t * quad


a, b = (1.0, 0.0), (0.0, 1.0)

for name, fn, h in [("f(x,y) = x^2 + 3xy + 5y^2", f, hess_f(0, 0)),
                    ("g(x,y) = x^2 + 3xy + 1y^2", g, hess_g(0, 0))]:
    print(f"=== {name} ===")
    print("  Hessian        :", h)
    print("  symmetric      :", h[0][1] == h[1][0])
    print("  H00            :", h[0][0])
    print("  det            :", det2(h))
    print("  Sylvester PD   :", sylvester(h))
    eig = eigenvalues_2x2(h)
    print("  eigenvalues    :", tuple(round(e, 6) for e in eig))
    print("  all eig > 0    :", eig is not None and all(e > 0 for e in eig))
    print("  trace check    :", abs(sum(eig) - (h[0][0] + h[1][1])) < 1e-12)
    print("  det check      :", abs(eig[0] * eig[1] - det2(h)) < 1e-12)

    direct = midpoint_gap(fn, a, b)
    closed = closed_form_gap(h, a, b)
    print(f"  midpoint gap (a=(1,0), b=(0,1), t=0.5): {direct:+.9f}")
    print(f"  closed-form gap, 0.5(1-t)t (a-b)'H(a-b) : {closed:+.9f}")
    print("  the two agree  :", abs(direct - closed) < 1e-9)
    print(f"  convex?        : {direct >= 0 and sylvester(h)}\n")
```

Output:

```
=== f(x,y) = x^2 + 3xy + 5y^2 ===
  Hessian        : [[2.0, 3.0], [3.0, 10.0]]
  symmetric      : True
  H00            : 2.0
  det            : 11.0
  Sylvester PD   : True
  eigenvalues    : (1.0, 11.0)
  all eig > 0    : True
  trace check    : True
  det check      : True
  midpoint gap (a=(1,0), b=(0,1), t=0.5): +0.750000000
  closed-form gap, 0.5(1-t)t (a-b)'H(a-b) : +0.750000000
  the two agree  : True
  convex?        : True

=== g(x,y) = x^2 + 3xy + 1y^2 ===
  Hessian        : [[2.0, 3.0], [3.0, 2.0]]
  symmetric      : True
  H00            : 2.0
  det            : -5.0
  Sylvester PD   : False
  eigenvalues    : (-1.541381, 4.541381)
  all eig > 0    : False
  trace check    : True
  det check      : True
  midpoint gap (a=(1,0), b=(0,1), t=0.5): -0.250000000
  closed-form gap, 0.5(1-t)t (a-b)'H(a-b) : -0.250000000
  the two agree  : True
  convex?        : False
```

All four tests agree in both cases, and they agree for the right reason: for a
quadratic, the closed-form gap `½(1−t)t(x−y)ᵀH(x−y)` is a positive multiple of
the quadratic form `xᵀHx`, which is positive for every x ≠ 0 exactly when H is
positive definite. So the gap test and the Sylvester test are not independent
here — they are the same fact seen twice. That agreement is the real check: if
you had written the Hessian wrong, the two gap columns would disagree.

For f the eigenvalues are exactly 1 and 11 (integers, since det = 11 and trace =
12 give λ² − 12λ + 11 = 0). For g, det = −5 < 0 forces one eigenvalue negative,
so g is a saddle: convex in some directions, concave in others. Note the
eigenvalues are irrational, ±√5 − 1 and ±√5 + 1, and their product is exactly
−5.

Note that the closed-form gap generalises to any points a, b and any t, not just
midpoints — it is an exact identity for quadratics, which makes it a
particularly clean way to check a symbolic derivation against code.

</details>

**[ ] Exercise 3 — ** Take f(x, y) = x² + y² and a linear constraint x + y = 1.
Minimise f subject to the constraint two ways: (a) substitute y = 1 − x and
minimise the resulting single-variable function by hand; (b) search a grid along
the constrained line. Confirm the results agree, and then show what happens
without the constraint. This sets up
[Lesson 102](102_lagrange_multipliers_and_knt.md).

<details>
<summary>Solution</summary>

```python
from math import sqrt


def f(x, y):
    return x * x + y * y


# --- (a) substitution: y = 1 - x, minimise g(x) = x^2 + (1-x)^2 ----------
def g(x):
    return x * x + (1.0 - x) ** 2


print("g(x) = x^2 + (1-x)^2")
print("  g'(x) = 2x + 2(x-1) = 4x - 2")
print("  set to zero: x = 0.5, so y = 0.5")

# Verify with a grid, and check the second derivative is positive.
xs = [i / 10000 for i in range(0, 10001)]
best_x = min(xs, key=g)
print(f"  grid argmin      : x = {best_x:.5f}, y = {1 - best_x:.5f}")
print(f"  grid min value   : {g(best_x):.10f}")
print(f"  g(0.5)           : {g(0.5):.10f}")
print("  g''(x) = 4 > 0, so it is a minimum")
print("  analytic value   :", f(0.5, 0.5))


# --- (b) constrained grid search, sampling the whole feasible line -------
def constrained_search(step=0.01):
    """Walk along x + y = 1 and keep the best point seen."""
    best = None
    n = int(round(2.0 / step))
    for i in range(n + 1):
        x = -1.0 + i * step
        y = 1.0 - x
        value = f(x, y)
        if best is None or value < best[0]:
            best = (value, x, y)
    return best


value, x, y = constrained_search()
print(f"\nconstrained grid search: value = {value:.10f} at ({x:.4f}, {y:.4f})")
print("  satisfies x + y = 1?", abs(x + y - 1.0) < 1e-12)
print("  agrees with the analytic answer?", abs(value - f(0.5, 0.5)) < 1e-9)


# --- unconstrained: the answer changes ---------------------------------
print("\nwithout the constraint, minimise f(x,y) = x^2 + y^2:")
print("  grad f = (2x, 2y) = 0 at (0, 0)")
print("  f(0, 0) =", f(0.0, 0.0))
print("  f(0.5, 0.5) =", f(0.5, 0.5))
print("  -> the constraint moved the answer from (0,0) to (0.5,0.5)")
print("  -> but both are unique global minima, because f is strictly convex")


# --- why convexity makes this easy --------------------------------------
def on_line(p, c=1.0):
    return abs(p[0] + p[1] - c) < 1e-9


pts = [(-1.0, 2.0), (-0.5, 1.5), (0.0, 1.0), (0.5, 0.5), (1.0, 0.0),
       (1.5, -0.5), (2.0, -1.0)]
print("\nvalues along the constraint line x + y = 1:")
for p in pts:
    print(f"  {str(p):12s} f = {f(*p):.4f}  on the line: {on_line(p)}")

# Take any feasible point and any other: their midpoint is feasible too, and
# its value is no worse. That is convexity doing the work.
worst_midpoint_gap = float("-inf")
for i in range(len(pts)):
    for j in range(i + 1, len(pts)):
        a, b = pts[i], pts[j]
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        gap = (f(*a) + f(*b)) / 2 - f(*m)
        worst_midpoint_gap = max(worst_midpoint_gap, gap)
print("\nmax Jensen gap along the feasible line:", round(worst_midpoint_gap, 10))
print("positive means the feasible set itself is convex, so there is one answer")
```

Output:

```
g(x) = x^2 + (1-x)^2
  g'(x) = 2x + 2(x-1) = 4x - 2
  set to zero: x = 0.5, so y = 0.5
  grid argmin      : x = 0.50000, y = 0.50000
  grid min value   : 0.5000000000
  g(0.5)           : 0.5000000000
  g''(x) = 4 > 0, so it is a minimum
  analytic value   : 0.5

constrained grid search: value = 0.5000000000 at (0.5000, 0.5000)
  satisfies x + y = 1? True
  agrees with the analytic answer? True

without the constraint, minimise f(x,y) = x^2 + y^2:
  grad f = (2x, 2y) = 0 at (0, 0)
  f(0, 0) = 0.0
  f(0.5, 0.5) = 0.5
  -> the constraint moved the answer from (0,0) to (0.5,0.5)
  -> but both are unique global minima, because f is strictly convex

values along the constraint line x + y = 1:
  (-1.0, 2.0)   f = 5.0000  on the line: True
  (-0.5, 1.5)   f = 2.5000  on the line: True
  (0.0, 1.0)    f = 1.0000  on the line: True
  (0.5, 0.5)    f = 0.5000  on the line: True
  (1.0, 0.0)    f = 1.0000  on the line: True
  (1.5, -0.5)   f = 2.5000  on the line: True
  (2.0, -1.0)   f = 5.0000  on the line: True

max Jensen gap along the feasible line: 4.5
```

Three observations that matter.

**The unconstrained answer and the constrained answer both exist and both are
unique.** Unconstrained the minimum is (0, 0) with value 0; constrained it is
(0.5, 0.5) with value 0.5. Convexity guarantees both are *the* answers, not
merely local ones — no amount of searching can find something better.

**The maximum Jensen gap along the feasible line is 4.5, comfortably positive.**
It comes from the two extreme feasible points (−1, 2) and (2, −1), both with
value 5, whose midpoint is (0.5, 0.5) with value 0.5: gap = (5 + 5)/2 − 0.5 = 4.5.
A positive gap means the midpoint of any two feasible points is both feasible
*and* no worse, which is the conjunction of the feasible set being convex and
the objective being convex. Non-convex constraints break the first half, which is
why non-convex feasible regions are so much harder.

**Substitution works here because the constraint is an equality you can solve
for one variable.** For inequalities like `x + y ≤ 1`, or several constraints at
once, you cannot eliminate variables this way — which is exactly why
[Lesson 102](102_lagrange_multipliers_and_knt.md) introduces multipliers.

</details>

**Challenge — ** Write a routine that decides whether a two-variable quadratic
`f(x, y) = ax² + bxy + cy² + dx + ey + g` is convex, non-strictly convex,
indefinite, or concave, using only the Hessian — no search over points. Test it
on at least six quadratics including two that sit on the boundary between
categories, and explain why a positive determinant alone cannot classify them.

<details>
<summary>Solution</summary>

```python
from math import sqrt


def classify_quadratic(a, b, c):
    """Classify f = ax^2 + bxy + cy^2 + dx + ey + g by its Hessian alone.

    The linear and constant terms shift the optimum but never change curvature,
    so they are irrelevant to the classification.

    The Hessian is [[2a, b], [b, 2c]] because d2/dx2 of ax^2 is 2a and
    d2/dxdy of bxy is b.
    """
    h00, h01, h11 = 2.0 * a, b, 2.0 * c
    det = h00 * h11 - h01 * h01

    if det > 0 and h00 > 0:
        return "strictly convex"
    if det > 0 and h00 < 0:
        return "strictly concave"
    if det < 0:
        return "indefinite (saddle)"
    # det == 0: one eigenvalue is zero, so the test is inconclusive
    if h00 == 0 and h01 == 0 and h11 == 0:
        return "degenerate (affine only, no curvature)"
    return "positive or negative semidefinite: not strictly convex"


def eigenvalues(h00, h01, h11):
    tr = h00 + h11
    d = h00 * h11 - h01 * h01
    disc = tr * tr - 4.0 * d
    if disc < 0:
        return None
    r = sqrt(disc)
    return ((tr - r) / 2.0, (tr + r) / 2.0)


cases = [
    ("x^2 + y^2", 1, 0, 1),
    ("x^2 + y^2 + 10x + 10y", 1, 0, 1),        # linear terms are irrelevant
    ("-x^2 - y^2", -1, 0, -1),
    ("x^2 + 3xy + 5y^2", 1, 3, 5),
    ("x^2 + 3xy + 1y^2", 1, 3, 1),
    ("x^2 + 4y^2  (det = 0)", 1, 0, 0),
    ("x^2 - 4y^2  (det < 0)", 1, 0, -1),
    ("x^2 + 2xy + y^2 = (x+y)^2", 1, 2, 1),   # rank 1, semidefinite
    ("x^2 + 2xy - y^2", 1, 2, -1),
    ("-x^2 + 2xy - y^2 = -(x+y)^2", -1, 2, -1),
    ("flat: 0", 0, 0, 0),
]

print(f"{'quadratic':32s} {'H':18s} {'det':>8s} {'eigenvalues':>22s}  verdict")
for name, a, b, c in cases:
    h00, h01, h11 = 2.0 * a, b, 2.0 * c
    det = h00 * h11 - h01 * h01
    eig = eigenvalues(h00, h01, h11)
    eig_s = f"({eig[0]:.4f}, {eig[1]:.4f})" if eig else "complex"
    h_s = f"[[{h00:g}, {h01:g}], [{h01:g}, {h11:g}]]"
    print(f"{name:32s} {h_s:18s} {det:8.2f} {eig_s:>22s}  "
          f"{classify_quadratic(a, b, c)}")

# Why det alone cannot classify.
print("\nwhy det alone cannot classify:")
for name, h in [("[[1,2],[2,1]]", (1.0, 2.0, 1.0)),
                ("[[-1,0],[0,-1]]", (-1.0, 0.0, -1.0)),
                ("[[1,2],[2,5]]", (1.0, 2.0, 5.0))]:
    h00, h01, h11 = h
    det = h00 * h11 - h01 * h01
    eig = eigenvalues(h00, h01, h11)
    if eig[0] > 0 and eig[1] > 0:
        signs = "both positive (convex)"
    elif eig[0] < 0 and eig[1] < 0:
        signs = "both negative (concave)"
    else:
        signs = "mixed (saddle)"
    print(f"  {name:14s} det={det:+.1f}  trace={h00 + h11:+.1f}"
          f"  eig=({eig[0]:+.3f}, {eig[1]:+.3f})  {signs}")

# Confirm the boundary cases really are not strictly convex, by finding two
# distinct points with the same value on the flat direction.
def f_semi(x, y):
    return x * x + 2.0 * x * y + y * y      # (x + y)^2


print("\nverifying (x+y)^2 is convex but NOT strictly convex:")
for t in (1.0, 2.0, 3.0, 4.0, 5.0):
    print(f"  f({t:.1f}, {-t:.1f}) = {f_semi(t, -t):.4f}   <- constant on x + y = 0")
print("  five distinct points, all the same value -> not strictly convex")

# Strict convexity test: the Hessian quadratic form is positive for every
# nonzero direction.
print("\ndirections v = (vx, vy) and v'Hv for (x+y)^2, whose Hessian is [[2,2],[2,2]]:")
H = [[2.0, 2.0], [2.0, 2.0]]
for v in [(1.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, -1.0), (2.0, -2.0)]:
    q = sum(v[i] * H[i][j] * v[j] for i in range(2) for j in range(2))
    note = "   <- zero: flat direction" if abs(q) < 1e-12 else ""
    print(f"  v={str(v):12s} v'Hv = {q:.4f}{note}")
```

Output:

```
quadratic                         H                  det   eigenvalues  verdict
Output:

```
quadratic                        H                       det            eigenvalues  verdict
x^2 + y^2                        [[2, 0], [0, 2]]       4.00       (2.0000, 2.0000)  strictly convex
x^2 + y^2 + 10x + 10y            [[2, 0], [0, 2]]       4.00       (2.0000, 2.0000)  strictly convex
-x^2 - y^2                       [[-2, 0], [0, -2]]     4.00     (-2.0000, -2.0000)  strictly concave
x^2 + 3xy + 5y^2                 [[2, 3], [3, 10]]     11.00      (1.0000, 11.0000)  strictly convex
x^2 + 3xy + 1y^2                 [[2, 3], [3, 2]]      -5.00     (-1.0000, 5.0000)  indefinite (saddle)
x^2 + 4y^2  (det = 0)            [[2, 0], [0, 0]]       0.00      (0.0000, 2.0000)  positive or negative semidefinite: not strictly convex
x^2 - 4y^2  (det < 0)            [[2, 0], [0, -2]]     -4.00     (-2.0000, 2.0000)  indefinite (saddle)
x^2 + 2xy + y^2 = (x+y)^2        [[2, 2], [2, 2]]       0.00      (0.0000, 4.0000)  positive or negative semidefinite: not strictly convex
x^2 + 2xy - y^2                  [[2, 2], [2, -2]]     -8.00     (-2.8284, 2.8284)  indefinite (saddle)
-x^2 + 2xy - y^2 = -(x+y)^2      [[-2, 2], [2, -2]]     0.00     (-4.0000, 0.0000)  positive or negative semidefinite: not strictly convex
flat: 0                          [[0, 0], [0, 0]]       0.00      (0.0000, 0.0000)  degenerate (affine only, no curvature)

why det alone cannot classify:
  [[1,2],[2,1]]  det=-3.0  trace=+2.0  eig=(-1.000, +3.000)  mixed (saddle)
  [[-1,0],[0,-1]] det=+1.0  trace=-2.0  eig=(-1.000, -1.000)  both negative (concave)
  [[1,2],[2,5]]  det=+1.0  trace=+6.0  eig=(+0.172, +5.828)  both positive (convex)

verifying (x+y)^2 is convex but NOT strictly convex:
  f(1.0, -1.0) = 0.0000   <- constant on x + y = 0
  f(2.0, -2.0) = 0.0000   <- constant on x + y = 0
  f(3.0, -3.0) = 0.0000   <- constant on x + y = 0
  f(4.0, -4.0) = 0.0000   <- constant on x + y = 0
  f(5.0, -5.0) = 0.0000   <- constant on x + y = 0
  five distinct points, all the same value -> not strictly convex

directions v = (vx, vy) and v'Hv for (x+y)^2, whose Hessian is [[2,2],[2,2]]:
  v=(1.0, 0.0)   v'Hv = 2.0000
  v=(0.0, 1.0)   v'Hv = 2.0000
  v=(1.0, 1.0)   v'Hv = 8.0000
  v=(1.0, -1.0)  v'Hv = 0.0000   <- zero: flat direction
  v=(2.0, -2.0)  v'Hv = 0.0000   <- zero: flat direction
```

The `det` column shows the trap. Rows 2 and 3 both have det = +4 yet are one
convex and one concave; rows 6, 8 and 10 all have det = 0 yet are positive
semidefinite, positive semidefinite, and negative semidefinite respectively.

The "why det alone" block makes the precise point, and it is subtler than "a
positive det is ambiguous between convex and saddle". For a symmetric 2×2
matrix, `det > 0` already **rules out** a saddle — the eigenvalues must have the
same sign. What `det > 0` cannot tell you is *which* sign: [[−1,0],[0,−1]] and
[[1,2],[2,5]] both have det = +1, yet the first is negative definite and the
second positive definite. You need the trace (or equivalently H₀₀) to break the
tie. So the correct statement is: `det > 0` means "definite, sign unknown", and
Sylvester's criterion is the `det > 0` test *plus* the `H₀₀ > 0` test.

The boundary cases are the valuable ones. `x² + 4y²` has a zero eigenvalue, so it
is convex but has no unique minimiser — the whole line y = 0 minimises it.
`(x + y)²` is worse: rank 1, so it is constant along an entire line, and the five
test points all give 0. And `−(x + y)²` is the mirror image, negative
semidefinite, giving a whole line of *maximisers* and no minimum at all.

The `v'Hv` computation closes the loop: strict convexity is exactly the statement
that `v'Hv > 0` for every nonzero v, and the flat direction v = (1, −1) is where
it fails. Note it fails *exactly* — scaling v to (2, −2) leaves v'Hv at 0 rather
than quadrupling it, which is the signature of a rank-deficient form.
</details>

## Summary

- A set is convex when it contains every segment between its own points; the
  convex hull is the smallest such set, and it is unchanged by deleting interior
  points.
- Jensen's inequality says a convex function at a weighted mean is at most the
  weighted mean of its values; this single statement is the workhorse of convex
  analysis.
- Convex functions have non-decreasing slopes, which is why they have at most
  one minimum.
- Convexity but not strict convexity means a whole flat region of minimisers —
  the normal situation for ReLU networks and L2 penalties.
- For a convex function, local implies global; strict convexity makes the
  minimiser unique. This is the guarantee that makes descent-based optimisers
  correct rather than hopeful.
- The Hessian is the matrix of second partials; positive definite ⟹ strict local
  minimum at a stationary point, and also ⟹ strict convexity.
- Positive definiteness is equivalent to all eigenvalues being positive, or all
  leading principal minors being positive; a positive determinant alone is not
  enough.
- Max of convex functions is convex, min is not — which is exactly why L2
  preserves convexity and L1 destroys it.
- Quadratic functions are the easy case: convexity is a property of the Hessian
  alone, and the Jensen gap has the closed form `½(1−t)t(x−y)ᵀH(x−y)`.

## Next

[101 — Gradient Descent](101_gradient_descent.md) turns the existence and
uniqueness guarantees from this lesson into an actual algorithm, with the update
rule, learning rates, momentum, and worked descent paths on convex and
non-convex test functions.
