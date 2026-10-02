# 102 — Lagrange Multipliers and Constraints

**Part**: part08_optimization · **Prerequisites**: 51, 53, 100, 101 · **Time**: 35 min

---

## In Plain Words

You cannot always walk downhill. Sometimes the rules of the problem decide where
you are allowed to be: the budget must be spent, the machine has limited hours,
the point has to stay inside a region. Now the lowest point inside that region
may be on its boundary, and a boundary is not something you can step over.

A multiplier turns that boundary into a slope. If the constraint is "spend
exactly 4", attach a number to it and add that number times the violation to
your objective. When the violation is zero the extra term contributes nothing,
so your objective is unchanged; when it is nonzero you have pushed your
objective in a direction you control. Then look for a point where the total has
no slope at all. That total is the Lagrangian.

The intuition is that at the best feasible point you are stuck. You cannot improve
by sliding along the boundary, because you are already at its lowest point, and
you cannot improve by leaving it, because leaving is forbidden. The only
improvement left would have to combine the two directions, and that is possible
only if they line up. The multiplier is the lining-up factor — and it also tells
you what the answer is worth per unit of whatever you ran out of.

For inequalities the multiplier is only allowed to be nonnegative, and there are
four cases to tell apart: comfortably inside, exactly on the boundary, on the
wrong side but penalised, and not binding at all. Those four conditions together
are called KKT, and they are the standard test for whether a candidate is right.

## Why Computer Science Cares

- **Linear and nonlinear programming solvers** do nothing but solve KKT systems
  repeatedly. `scipy.optimize.minimize`, CVXPY, Gurobi and CPLEX all work this
  way, and every constraint-handling trick in them is a variation on this.
- **The SVM margin is literally this method.** The margin constraints
  `yᵢ(w·xᵢ + b) ≥ 1` become a Lagrangian, and the KKT multipliers identify the
  support vectors — the only points that affect the classifier at all.
- **Portfolio optimisation.** Markowitz's mean-variance problem is a quadratic
  programme with budget and risk constraints; the multipliers are the marginal
  value of relaxing each one.
- **Resource allocation** in operations research: production schedules, staffing,
  routing and bidding all reduce to maximising profit subject to limits.
- **Regularisation as a constraint.** Penalised and constrained least squares have
  the same solution under a mild condition, with the penalty coefficient and the
  multiplier tied together. That is why ridge regression can be written either
  way.
- **The dual of a non-convex problem is often convex**, which is why so many
  otherwise-intractable problems are solvable, and why the SVM's dual is what is
  actually computed.
- **Interior-point methods**, the production default, are Newton iterations on
  the KKT system with barrier terms that keep iterates strictly feasible.

## The Formal Version

Notation follows [SYMBOLS.md](../../SYMBOLS.md).

**Definition.** For minimisation with m equality constraints cᵢ(x) = 0, the
*Lagrangian* is the function of n + m variables

  L(x, λ) = f(x) + Σᵢ λᵢ cᵢ(x).

**Definition.** If ∇cᵢ(x) are linearly independent at x, then x is a *regular
point* there.

**Theorem (Lagrange condition, necessity).** Let f, cᵢ be continuously
differentiable and let x be a regular point that is a local minimiser of f
subject to cᵢ(x) = 0. Then there exist λᵢ with

  ∇f(x) + Σᵢλᵢ∇cᵢ(x) = 0,  together with  cᵢ(x) = 0.

**Explanation.** Take a feasible curve x(t) with x(0) = x, so cᵢ(x(t)) = 0 for
all t. Differentiating gives ∇cᵢ(x)·x′(0) = 0, so x′(0) is orthogonal to every
constraint gradient. Since x is a minimum along the curve, ∇f(x)·x′(0) = 0 too.
So ∇f(x) is orthogonal to the same space spanned by the constraint gradients,
and two vectors orthogonal to the same space lie in its orthogonal complement —
which in ℝⁿ is the span of those gradients. Hence ∇f(x) = −Σλᵢ∇cᵢ(x).
Geometrically: **at the optimum the objective gradient is perpendicular to the
feasible set.**

**Definition.** ∇ₓL = 0 together with cᵢ(x) = 0 is the *first-order stationarity
condition*.

**Theorem (insufficiency).** Stationarity is necessary, not sufficient. The
constant function f ≡ 0 subject to x = 0 satisfies it at the unique feasible
point, and it is trivially optimal there — but f ≡ 0 with no constraint satisfies
it everywhere. The condition identifies *candidates*.

**Definition.** The *second-order sufficient condition* requires
∇²ₓₓL(x, λ) = ∇²f(x) + Σᵢλᵢ∇²cᵢ(x) to be positive definite on the *tangent
space* {v : ∇cᵢ(x)·v = 0 for all i}. When the constraints are linear, ∇²f alone
suffices on that space.

**Definition.** For inequalities, write the problem as
min f(x) subject to gᵢ(x) ≤ 0 and hⱼ(x) = 0, with
L(x, μ, ν) = f(x) + Σᵢμᵢgᵢ(x) + Σⱼνⱼhⱼ(x).

**Theorem (KKT conditions).** Under a constraint qualification (active gradients
linearly independent), x is a local minimiser only if:

1. **Primal feasibility:** gᵢ(x) = 0 for active i, hⱼ(x) = 0 for all j.
2. **Dual feasibility:** μᵢ ≥ 0 for all i.
3. **Complementary slackness:** μᵢ gᵢ(x) = 0 for all i.
4. **Stationarity:** ∇f(x) + Σᵢμᵢ∇gᵢ(x) + Σⱼνⱼ∇hⱼ(x) = 0.

**Explanation.** Conditions 2 and 3 are the whole story for inequalities.
Complementary slackness says μᵢgᵢ(x) = 0, and a product of a nonneg and a nonpos
number vanishing means one factor is zero. So if gᵢ(x) < 0 the constraint is
slack and μᵢ = 0; if μᵢ > 0 the constraint is binding; μᵢ = gᵢ(x) = 0 is the
degenerate middle case. An active constraint with a strictly positive multiplier
is one you would pay real money to relax.

**Theorem (strong duality).** For convex f with convex gᵢ and affine hⱼ, and a
feasible point satisfying Slater's condition (strictly feasible), the primal and
dual optimal values coincide, and KKT becomes sufficient as well as necessary.

**Theorem (shadow prices).** At a KKT point, μᵢ is the rate at which the optimal
value improves per unit of relaxing constraint i: ∂p*/∂bᵢ = −μᵢ where bᵢ is the
constant in gᵢ(x) ≤ bᵢ. This is why multipliers are called *shadow prices* — λ =
1.3333 in the resource example really does mean one extra labour hour is worth
1.3333 profit units, to first order.

**Definition.** The *dual problem* minimises the Lagrangian over x:
d(μ, ν) = inf_x L(x, μ, ν). Since d ≤ f at every feasible point, maximising d
over μ, ν ≥ 0 gives a lower bound on the primal optimum, and by strong duality
often the exact value.

**Theorem (the gap is the KKT residual).** At a candidate with ∇ₓL = 0 and
hⱼ(x) = 0, the gap p − d equals Σᵢμᵢgᵢ(x). So the gap measures exactly how
violated the constraints are, and it is zero precisely when complementary
slackness holds — a free optimality certificate.

## Worked Example

Minimise f(x, y) = (x − 3)² + (y − 2)² subject to x + y = 4.

**Step 1 — the unconstrained optimum.** ∇f = (2(x−3), 2(y−2)) = 0 at (3, 2),
where f = 0. But (3, 2) gives x + y = 5, infeasible. So the constraint binds.

**Step 2 — the Lagrangian.** With c(x, y) = x + y − 4,

L = (x−3)² + (y−2)² + λ(x + y − 4).

**Step 3 — stationarity.**

∂L/∂x = 2(x − 3) + λ = 0
∂L/∂y = 2(y − 2) + λ = 0
∂L/∂λ = x + y − 4 = 0

**Step 4 — solve.** The first gives x = 3 − λ/2 and the second y = 2 − λ/2.
Substituting into the third: (3 − λ/2) + (2 − λ/2) = 4, so 5 − λ = 4 and
**λ = 1**. Hence x = 2.5 and y = 1.5.

**Step 5 — the answer.** x* = (2.5, 1.5), λ* = 1, and
f = (2.5−3)² + (1.5−2)² = 0.25 + 0.25 = **0.5**. The constraint costs 0.5 above
the unconstrained 0, and λ = 1 is that price per unit.

**Step 6 — verify the geometry.** ∇f at (2.5, 1.5) is (−1, −1); the constraint
gradient ∇c = (1, 1). They are parallel, which is exactly stationarity: the
objective gradient is perpendicular to the feasible line. And −∇f/∇c = 1 = λ.

**Step 7 — the second-order test.** ∇²L = [[2,0],[0,2]], positive definite, so
the point is a strict minimum. Since f is strictly convex and the feasible line
is convex, it is also the *unique* global minimum.

**Step 8 — an inequality version.** Change the constraint to x + y ≤ 4. The
stationarity equations are unchanged and (2.5, 1.5) is still feasible with
x + y = 4 exactly, so it is still optimal — and now λ = 1 > 0 satisfies dual
feasibility and complementary slackness: the binding case.

Relax the budget to x + y ≤ 5 and the answer changes: (3, 2) is feasible, so the
constraint is slack, complementary slackness forces **λ = 0**, and the
unconstrained optimum returns. That single mechanism — sign condition plus
complementary slackness — is how a solver knows whether a constraint is worth
anything.

## Runnable Code

A KKT solver from scratch: Gaussian elimination plus a Newton iteration.

```python
"""Lagrange multipliers: solve a KKT system with Gaussian elimination."""

from math import sqrt


# --- A small dense linear solver, from scratch --------------------------
def solve_linear(A, b):
    """Solve A x = b for small dense A by Gaussian elimination with partial
    pivoting. A is a list of rows; A and b are copied, not modified."""
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]

    for col in range(n):
        # Partial pivoting: swap in the largest pivot for numerical stability.
        pivot = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[pivot][col]) < 1e-14:
            raise ValueError("singular system")
        M[col], M[pivot] = M[pivot], M[col]
        # Normalise the pivot row, then eliminate below it.
        p = M[col][col]
        M[col] = [v / p for v in M[col]]
        for r in range(n):
            if r == col:
                continue
            factor = M[r][col]
            if factor:
                M[r] = [v - factor * w for v, w in zip(M[r], M[col])]

    return [M[i][n] for i in range(n)]


# --- Problem A: one equality constraint ---------------------------------
# minimise  f(x,y) = (x-3)^2 + (y-2)^2   subject to   x + y = 4


def f(x):
    return (x[0] - 3.0) ** 2 + (x[1] - 2.0) ** 2


def grad_f(x):
    return [2.0 * (x[0] - 3.0), 2.0 * (x[1] - 2.0)]


def c1(x):
    return x[0] + x[1] - 4.0


def grad_c1(x):
    return [1.0, 1.0]


def lagrangian_A(x, lam):
    """L(x, lam) = f(x) + lam * c(x). Returns (value, gradient)."""
    g = grad_f(x)
    gc = grad_c1(x)
    value = f(x) + lam * c1(x)
    grad = [g[j] + lam * gc[j] for j in range(len(x))]
    return value, grad


def solve_kkt_A():
    """Solve grad L = 0 and c(x) = 0 for [x, y, lam] by Newton iteration.

    The system is linear here, so one Newton step from any start suffices;
    the loop is kept so the same code handles non-linear constraints.
    """
    u = [0.0, 0.0, 0.0]                     # [x, y, lam]
    for _ in range(20):
        x, lam = [u[0], u[1]], u[2]
        _, gL = lagrangian_A(x, lam)
        r = [gL[0], gL[1], c1(x)]            # residual of the KKT system

        # Jacobian of the residual. d(grad L)/dx is the Hessian of the
        # Lagrangian; d(grad L)/dlam is grad c; dc/dx is grad c; dc/dlam = 0.
        H = [[2.0, 0.0, 1.0],
             [0.0, 2.0, 1.0],
             [1.0, 1.0, 0.0]]
        du = solve_linear(H, [-v for v in r])  # Newton: J du = -r
        u = [u[i] + du[i] for i in range(3)]
        if max(abs(v) for v in r) < 1e-14:
            break
    return u


print("=== Problem A: minimise (x-3)^2 + (y-2)^2 subject to x + y = 4 ===")
print("the unconstrained minimum (3, 2) is infeasible: 3 + 2 = 5, not 4\n")

u = solve_kkt_A()
x_star = [u[0], u[1]]
print(f"solution: x = {x_star[0]:.10f}, y = {x_star[1]:.10f}, lambda = {u[2]:.10f}")
print(f"constraint x + y = {sum(x_star):.10f}   (must be exactly 4)")
print(f"objective f = {f(x_star):.10f}")
print(f"the constraint costs {f(x_star):.6f} above the unconstrained 0")

# Brute-force check straight along the feasible line.
print("\nbrute-force check, scanning the line x + y = 4:")
best = None
for i in range(0, 4001):
    xv = i / 1000.0
    value = f([xv, 4.0 - xv])
    if best is None or value < best[0]:
        best = (value, xv, 4.0 - xv)
print(f"  grid search: x = {best[1]:.3f}, y = {best[2]:.3f}, f = {best[0]:.8f}")
print(f"  KKT answer : x = {x_star[0]:.8f}, y = {x_star[1]:.8f},"
      f" f = {f(x_star):.8f}")

# Why this point and no other: the gradient must be perpendicular to the
# constraint, so -grad f is parallel to grad c.
g = grad_f(x_star)
gc = grad_c1(x_star)
print(f"\ngrad f at the solution: ({g[0]:.6f}, {g[1]:.6f})")
print(f"grad c                : ({gc[0]:.6f}, {gc[1]:.6f})")
print(f"ratio g_x/g_c_x = {g[0] / gc[0]:.10f}")
print(f"ratio g_y/g_c_y = {g[1] / gc[1]:.10f}   (equal -> parallel)")
print(f"lambda from -grad_x/grad_c_x = {-g[0] / gc[0]:.10f}  (matches {u[2]:.10f})")
```

### Two constraints, and the inequality cases

```python
def solve_linear(A, b):
    """Solve A x = b for small dense A by Gaussian elimination with partial
    pivoting. A is a list of rows; A and b are copied, not modified."""
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[pivot][col]) < 1e-14:
            raise ValueError("singular system")
        M[col], M[pivot] = M[pivot], M[col]
        p = M[col][col]
        M[col] = [v / p for v in M[col]]
        for r in range(n):
            if r != col and M[r][col]:
                f = M[r][col]
                M[r] = [v - f * w for v, w in zip(M[r], M[col])]
    return [M[i][n] for i in range(n)]


def damped_solve(J, rhs, tries=10):
    """Solve J du = rhs, adding eps*I if J is singular.

    The KKT Jacobian is genuinely rank deficient whenever the objective is
    LINEAR: its Hessian block is then all zeros, so the first n rows carry no
    information about x. Adding a small multiple of the identity
    (Levenberg-Marquardt damping) restores solvability. Without this, every
    linear objective makes Gaussian elimination hit a zero pivot and raise.
    """
    n = len(J)
    for k in range(tries):
        eps = 0.0 if k == 0 else 10.0 ** (-14 + k)
        A = [[J[i][j] + (eps if i == j else 0.0) for j in range(n)]
             for i in range(n)]
        try:
            return solve_linear(A, rhs)
        except ValueError:
            continue
    raise ValueError("singular even after damping")


def solve_equality_kkt(grad_obj, hess_obj, constraints, x0):
    """Newton iteration on the equality-constrained KKT system.

    Unknowns are u = [x (n values), lam (m values)]. The residual is
        grad_x L           for the first n entries
        c_1(x), ..., c_m(x) for the last m entries
    and the Jacobian blocks are
        d(grad_x L)/dx   = H_f + sum_i lam_i * H_c_i
        d(grad_x L)/dlam = grad c_i(x)^T
        dc_i/dx          = grad c_i(x)^T
        dc_i/dlam_j      = 0

    `constraints` is a list of (c, grad_c) pairs -- the constraint VALUE is
    needed for the residual, the GRADIENT for the Jacobian, and forgetting the
    value silently solves grad(c).x = 0 instead of c(x) = 0.

    Each constraint Hessian is taken as zero, exact for the linear constraints
    used here.
    """
    n = len(x0)
    m = len(constraints)
    size = n + m
    u = list(x0) + [0.0] * m

    for it in range(100):
        x, lam = u[:n], u[n:]

        # Residual: grad L first, then the constraint values.
        g = list(grad_obj(x))
        for i in range(m):
            gc = constraints[i][1](x)
            for j in range(n):
                g[j] += lam[i] * gc[j]
        residual = g + [constraints[i][0](x) for i in range(m)]

        # Jacobian.
        J = [[0.0] * size for _ in range(size)]
        for r in range(n):
            for c in range(n):
                J[r][c] = hess_obj[r][c]
        for i in range(m):
            gc = constraints[i][1](x)
            for j in range(n):
                J[j][n + i] = gc[j]        # d(grad L)/dlam_i
                J[n + i][j] = gc[j]        # dc_i/dx
        # bottom-right block stays zero

        du = damped_solve(J, [-v for v in residual])
        u = [u[i] + du[i] for i in range(size)]
        if max(abs(v) for v in du) < 1e-14:
            break
    return u[:n], u[n:]


ZERO2 = [[0.0, 0.0], [0.0, 0.0]]

# --- Problem B: two equality constraints --------------------------------
# maximise profit P(a, b) = 12a + 20b
#   2a + b <= 100   (labour hours)
#   a + 2b <= 80    (machine hours)
# Both bind at the optimum, so solve them as equalities.
def grad_cost(v):
    return [-12.0, -20.0]


def c_labour(v):
    return 2.0 * v[0] + v[1] - 100.0


def gc_labour(v):
    return [2.0, 1.0]


def c_machine(v):
    return v[0] + 2.0 * v[1] - 80.0


def gc_machine(v):
    return [1.0, 2.0]


def profit(a, b):
    return 12.0 * a + 20.0 * b


print("=== Problem B: maximise 12a + 20b ===")
print("  2a + b <= 100 (labour),  a + 2b <= 80 (machine),  a, b >= 0\n")

solB, lamB = solve_equality_kkt(grad_cost, ZERO2,
                                [(c_labour, gc_labour),
                                 (c_machine, gc_machine)],
                                [10.0, 10.0])
a, b = solB
print(f"solution: a = {a:.10f}, b = {b:.10f}")
print(f"  labour  2a + b = {2 * a + b:.10f}   (limit 100)")
print(f"  machine a + 2b = {a + 2 * b:.10f}   (limit 80)")
print(f"  profit = {profit(a, b):.10f}")
print(f"  both non-negative: {a >= 0 and b >= 0}")

ll, lm = lamB[0], lamB[1]
gl, gm = gc_labour(None), gc_machine(None)
gprof = [12.0, 20.0]
print("\nKKT stationarity: grad(profit) = sum of lam_i * grad(c_i)")
print(f"  grad(profit)                       = ({gprof[0]:+.4f}, {gprof[1]:+.4f})")
print(f"  lam_labour  = {ll:.6f} * ({gl[0]:.1f}, {gl[1]:.1f})"
      f" = ({ll * gl[0]:+.4f}, {ll * gl[1]:+.4f})")
print(f"  lam_machine = {lm:.6f} * ({gm[0]:.1f}, {gm[1]:.1f})"
      f" = ({lm * gm[0]:+.4f}, {lm * gm[1]:+.4f})")
print(f"  sum                                = ({ll * gl[0] + lm * gm[0]:+.4f},"
      f" {ll * gl[1] + lm * gm[1]:+.4f})")
print("  the components agree, which IS the stationarity condition")
print(f"\n  economic reading: one extra labour hour is worth {ll:.4f} profit")
print(f"  units, one extra machine hour is worth {lm:.4f} profit units.")

# Brute-force check over the feasible polygon.
print("\nbrute force, 0.25-spaced grid over the feasible polygon:")
best = None
count = 0
for i in range(0, 201):
    av = i / 4.0
    for j in range(0, 201):
        bv = j / 4.0
        if c_labour([av, bv]) <= 1e-9 and c_machine([av, bv]) <= 1e-9:
            count += 1
            p = profit(av, bv)
            if best is None or p > best[0]:
                best = (p, av, bv)
print(f"  {count} feasible grid points")
print(f"  best profit {best[0]:.4f} at (a = {best[1]:.2f}, b = {best[2]:.2f})")
print(f"  matches the KKT answer? {abs(best[0] - profit(a, b)) < 1e-6}")

# --- Problem C: an inequality that actually binds ------------------------
print("\n=== Problem C: maximise x*y subject to x + y <= 10 ===")
print("  without the budget this is unbounded above, so the constraint binds\n")


def grad_negprod(v):
    return [-v[1], -v[0]]


def c_budget(v):
    return v[0] + v[1] - 10.0


def gc_budget(v):
    return [1.0, 1.0]


HESS_NEGPROD = [[0.0, -1.0], [-1.0, 0.0]]

solC, lamC = solve_equality_kkt(grad_negprod, HESS_NEGPROD,
                                [(c_budget, gc_budget)], [1.0, 1.0])
x, y = solC
print(f"solution: x = {x:.10f}, y = {y:.10f}")
print(f"  x + y = {x + y:.10f}   (limit 10)")
print(f"  product xy = {x * y:.10f}   (the maximum possible)")
print(f"  non-negative: {x >= 0 and y >= 0}")

g = grad_negprod([x, y])
lam = -g[0] / gc_budget(None)[0]
print(f"\nstationarity: grad(-xy) + lam*grad c = "
      f"({g[0] + lam:+.3e}, {g[1] + lam:+.3e})")
print(f"  lam = {lam:.6f} > 0")
print("  a positive multiplier on an ACTIVE constraint means that constraint")
print("  is genuinely binding: relaxing it would improve the objective.")
print(f"  Check: with a budget of 11 the best product rises to "
      f"{max(xv * (11 - xv) for xv in [i / 100 for i in range(1101)]):.4f}.")

# Contrast with a slack constraint.
print("\ncontrast: maximise x*y subject to x + y <= 20 (now slack)")
best = None
for i in range(0, 2001):
    xv = i * 20.0 / 2000.0
    value = xv * (20.0 - xv)
    if best is None or value > best[0]:
        best = (value, xv, 20.0 - xv)
print(f"  grid best: x = {best[1]:.2f}, y = {best[2]:.2f}, xy = {best[0]:.4f}")
print("  the whole segment x + y = 20 is optimal, so the constraint is not")
print("  uniquely active and the multiplier is not determined. This is why the")
print("  KKT sign condition allows lam = 0 as well as lam > 0.")
```

### The SVM margin, where the multipliers pick out the important points

```python
from math import sqrt

# --- Hard-margin SVM on two points --------------------------------------
# One point of each class, labels +1 and -1.
# Find w, b minimising 0.5|w|^2  subject to  y_i (w.x_i + b) >= 1.
x_pos, y_pos = (2.0, 1.0), 1.0
x_neg, y_neg = (0.0, -1.0), -1.0

# Both constraints bind at the optimum:
#   w.x_pos + b =  1
#   w.x_neg + b = -1
# Subtracting gives w . (x_pos - x_neg) = 2.
delta = (x_pos[0] - x_neg[0], x_pos[1] - x_neg[1])
print("=== hard-margin SVM on two points ===")
print(f"  positive point {x_pos}, label {y_pos:+.0f}")
print(f"  negative point {x_neg}, label {y_neg:+.0f}")
print(f"  difference x_pos - x_neg = {delta}")
print("  so w must satisfy w . delta = 2\n")

# w lies along delta, perpendicular to the separating line. Write w = t*delta,
# then t * |delta|^2 = 2 fixes t exactly.
norm_sq = delta[0] ** 2 + delta[1] ** 2
t = 2.0 / norm_sq
w = [t * delta[0], t * delta[1]]
b = 1.0 - (w[0] * x_pos[0] + w[1] * x_pos[1])

print(f"  |delta|^2 = {norm_sq:.10f}")
print(f"  t = 2 / |delta|^2 = {t:.10f}")
print(f"  w = ({w[0]:.10f}, {w[1]:.10f})")
print(f"  b = {b:.10f}")
print(f"  |w| = {sqrt(w[0] ** 2 + w[1] ** 2):.10f}")

margin_pos = y_pos * (w[0] * x_pos[0] + w[1] * x_pos[1] + b)
margin_neg = y_neg * (w[0] * x_neg[0] + w[1] * x_neg[1] + b)
print(f"\n  margin on positive point: {margin_pos:.10f}  (must be 1)")
print(f"  margin on negative point: {margin_neg:.10f}  (must be 1)")

dot_w_delta = w[0] * delta[0] + w[1] * delta[1]
print(f"\n  w . delta = {dot_w_delta:.10f}  (nonzero, so w is PARALLEL to delta)")
print("  w points along the line joining the points, i.e. perpendicular to the")
print("  decision boundary: exactly the maximum-margin direction.")

slope = -w[0] / w[1]
perpendicular = -1.0 / slope
print(f"\n  decision boundary slope {slope:.10f}")
print(f"  line joining points   slope {perpendicular:.10f}")
print(f"  product = {slope * perpendicular:.10f}  (must be -1)")

wnorm = sqrt(w[0] ** 2 + w[1] ** 2)
d_pos = abs(w[0] * x_pos[0] + w[1] * x_pos[1] + b) / wnorm
d_neg = abs(w[0] * x_neg[0] + w[1] * x_neg[1] + b) / wnorm
print(f"\n  distance boundary-to-positive = {d_pos:.10f}")
print(f"  distance boundary-to-negative = {d_neg:.10f}")
print(f"  total margin width = {d_pos + d_neg:.10f}")
print(f"  it equals 2 / |w| = {2.0 / wnorm:.10f}")

# --- What the multipliers mean ------------------------------------------
print("\n=== the multiplier tells you which points matter (support vectors) ===")
print("  soft-margin SVM:  minimise 0.5|w|^2 + C * sum hinge losses")
print("  with lam_i >= 0 and sum lam_i y_i = 0\n")

C = 1.0
samples = [
    ((3.0, 3.0), +1.0, "comfortably outside the margin"),
    ((1.0, 2.0), +1.0, "exactly on the margin"),
    ((0.2, 0.2), +1.0, "inside the margin (misclassified)"),
    ((-3.0, -3.0), -1.0, "comfortably outside the margin"),
    ((-0.5, -0.5), -1.0, "exactly on the margin"),
    ((-0.2, -0.2), -1.0, "inside the margin (misclassified)"),
]

print(f"{'point':14s} {'label':>6} {'functional':>12} {'margin':>10}"
      f" {'lambda':>12}  note")
support = []
for p, label, note in samples:
    functional = w[0] * p[0] + w[1] * p[1] + b
    margin = label * functional
    if margin > 1.0 + 1e-9:
        lam = 0.0
    elif margin < 1.0 - 1e-9:
        lam = C
    else:
        lam = "0 < lam < C"
    if margin <= 1.0 + 1e-9:
        support.append(p)
    print(f"{str(p):14s} {label:+6.0f} {functional:12.6f} {margin:10.6f}"
          f" {str(lam):>12}  {note}")

print(f"\n  points with lambda > 0 are the support vectors: {support}")
print("  Every other point can be deleted without changing w. That is the whole")
print("  reason a kernel SVM can use only a handful of points out of millions.")
print(f"  Here {len(support)} of {len(samples)} points are support vectors.")

# The margin width shrinks as |w| grows, so minimising 0.5|w|^2 IS
# maximising the margin. Demonstrate it by trying a worse w.
print("\n=== minimising |w|^2 IS maximising the margin ===")
for scale in (1.0, 2.0, 4.0, 8.0):
    w2 = [v * scale for v in w]
    width = 2.0 / sqrt(w2[0] ** 2 + w2[1] ** 2)
    obj = 0.5 * (w2[0] ** 2 + w2[1] ** 2)
    print(f"  |w| scaled by {scale:3.0f}:  0.5|w|^2 = {obj:10.4f}"
          f"   margin width = {width:.6f}")
print("  the objective and the margin move in opposite directions, so")
print("  minimising the one maximises the other.")
```

### With Libraries

Real solvers, plus the dual. This block requires numpy and scipy and is not
runnable in the standard library alone.

```python
import numpy as np
from scipy.optimize import minimize

# --- 1. A linear program with two resources -----------------------------
# maximise 12a + 20b  s.t.  2a + b <= 100,  a + 2b <= 80,  a,b >= 0
def neg_profit(v):
    return -(12.0 * v[0] + 20.0 * v[1])


def neg_profit_grad(v):
    return np.array([-12.0, -20.0])


constraints = [
    {"type": "ineq", "fun": lambda v: 100.0 - 2.0 * v[0] - v[1]},   # >= 0
    {"type": "ineq", "fun": lambda v: 80.0 - v[0] - 2.0 * v[1]},
]
bounds = [(0.0, None), (0.0, None)]

res = minimize(neg_profit, x0=[10.0, 10.0], jac=neg_profit_grad,
               constraints=constraints, bounds=bounds, method="SLSQP")

print("maximise 12a + 20b, 2a + b <= 100, a + 2b <= 80, a,b >= 0")
print("  scipy says a =", np.round(res.x, 8), " profit =",
      round(-res.fun, 8), " success =", res.success)
print("  by hand (this lesson): a = 40, b = 20, profit = 880")
print("  agree?", np.allclose(res.x, [40.0, 20.0]))

# The multipliers are the shadow prices of the two constraints.
print("\n  multipliers (marginal value of one more unit of each resource):")
muls = np.atleast_1d(np.asarray(res.multipliers, dtype=float))
for name, m in zip(["labour ", "machine"], muls):
    print(f"    {name}: {m:+.8f}   (by hand: labour 1.3333, machine 9.3333)")

# --- 2. The KKT residual, checked numerically ---------------------------
print("\n=== KKT residual check at the scipy solution ===")
c_vals = np.array([c["fun"](res.x) for c in constraints])
print("  constraint values (must be >= 0):", np.round(c_vals, 10))
print("  all feasible?", bool(np.all(c_vals >= -1e-9)))
print("  multipliers (must be >= 0):", np.round(muls, 10))
print("  all non-negative?", bool(np.all(muls >= -1e-9)))

# Stationarity for a minimisation with constraints fun_i(x) >= 0 is
#     grad f - sum_i lam_i * grad(fun_i) = 0,
# i.e. the gradient of the objective must lie in the cone spanned by the
# active constraint gradients.
gc = np.array([[-2.0, -1.0], [-1.0, -2.0]])
stationarity = neg_profit_grad(res.x) - muls @ gc
print("  stationarity residual grad f - sum lam * grad(fun):")
print("   ", np.round(stationarity, 10),
      " ~0?", bool(np.allclose(stationarity, 0, atol=1e-6)))

# --- 3. Max-product with a budget --------------------------------------
def neg_xy(v):
    return -(v[0] * v[1])


def neg_xy_grad(v):
    return np.array([-v[1], -v[0]])


def neg_xy_hess(v):
    return np.array([[0.0, -1.0], [-1.0, 0.0]])


res2 = minimize(neg_xy, x0=[1.0, 1.0], jac=neg_xy_grad,
                constraints=[{"type": "ineq", "fun": lambda v: 10.0 - v.sum()}],
                bounds=[(0, None), (0, None)], method="SLSQP")

print("\nmaximise x*y subject to x + y <= 10")
print("  scipy: x =", np.round(res2.x, 8), " product =", round(-res2.fun, 8))
print("  by hand: x = 5, y = 5, product = 25")
print("  multiplier =", np.round(res2.multipliers, 8), " (by hand: 5)")

H = neg_xy_hess(res2.x)
print("  eigenvalues of the Hessian of -xy:", np.round(np.linalg.eigvalsh(H), 6))
print("  indefinite (one + and one -), so the KKT point is a max of xy,")
print("  i.e. a min of -xy, WITHOUT needing the second-order test on the")
print("  reduced problem: the sign convention did the work.")

# --- 4. Dual problem: convex even when the primal is not ---------------
# Primal:  minimise  -xy   subject to   x + y <= 10,  x >= 0, y >= 0.
# Lagrangian:  L = -xy + lam(x + y - 10) - mu*x - nu*y,   lam, mu, nu >= 0.
# Stationarity:  -y + lam - mu = 0 and  -x + lam - nu = 0.
# mu = lam - y >= 0 forces y <= lam; finiteness of the infimum forces
# y >= lam. Together x = y = lam, giving the dual
#     g(lam) = lam^2 - 10*lam,   lam >= 0,   a CONVEX 1-D minimisation.
def dual(lam):
    lam = lam[0]
    return lam * lam - 10.0 * lam


def dual_grad(lam):
    lam = lam[0]
    return np.array([2.0 * lam - 10.0])


res3 = minimize(dual, x0=[1.0], jac=dual_grad, bounds=[(0.0, None)],
                method="L-BFGS-B")
print("\n=== the dual: a convex 1-D problem with the same answer ===")
print("  dual optimum lam =", round(res3.x[0], 8), " (primal multiplier was 5)")
print("  dual objective   =", round(res3.fun, 8), " (primal objective was -25)")
print("  they match:", abs(res3.fun + 25.0) < 1e-8)
print("  strong duality holds here, so the dual bound is tight.")
print("  The dual is a CONVEX minimisation even though the primal objective")
print("  -xy is neither convex nor concave. That is the single most important")
print("  practical fact in constrained optimisation.")
print("  dual second derivative at the optimum = 2.0 (> 0), confirming convexity.")
```

The stationarity residual is the whole KKT check in one array. Primal feasibility
says the constraint values are ≥ 0 (both are exactly 0, so both bind). Dual
feasibility says the multipliers are ≥ 0 (both positive). Stationarity says the
objective gradient lies in the cone of active constraint gradients, and the
residual is `[-0. -0.]`. When all four hold on a convex problem the point is
globally optimal with no further search.

## Common Mistakes

**1. Sign confusion between maximise and minimise.** `min f` with `c(x) = 0` uses
`L = f + λc`. `max f` needs either `min −f` with the same form, or a flipped
sign on the multipliers. The code always converts maximisation to minimisation
explicitly, which removes the ambiguity. Mixing conventions gives answers with
the right geometry and the wrong λ, so the shadow-price reading comes out
negative.

**2. Forgetting complementary slackness for inequalities.** Solving stationarity
with `gᵢ(x) ≤ 0` and `μᵢ ≥ 0` alone is not enough; you must also enforce
`μᵢgᵢ(x) = 0`. Without it a solver will happily return a point that violates a
constraint while assigning it a nonzero multiplier — which is precisely how a
"constrained" optimiser silently degrades into an unconstrained one.

**3. Treating stationarity as sufficient.** It identifies candidates only. The
constant function f ≡ 0 satisfies ∇f = 0 everywhere, so every point is
"stationary" and most are not optima. Follow with a second-order test on the
tangent space, or use a global method.

**4. Not verifying feasibility after guessing an active set.** Solving for an
assumed active set and forgetting to check the point is actually feasible is the
most common error in this whole subject. It produces points with negative
multipliers, or absurd values. Production solvers run the check and iterate when
it fails.

**5. Losing track of which multiplier belongs to which constraint.** λ₁, λ₂, λ₃
are meaningless without labels, and after any subsetting or reordering they
silently point at the wrong rows — producing stationarity residuals that should
be zero and are not. Carrying named multiplier arrays, as `scipy.optimize` does,
prevents an entire class of bug.

**6. Using the primal when the dual is easier.** The dual often has fewer
variables, is frequently convex when the primal is not, and gives a certified
lower bound. Before hand-rolling a constrained solver, check the dual.

## Exercises and Solutions

**[ ] Exercise 1 — ** Minimise x² + y² subject to x + y = 3, then subject to
xy = 4. Solve both analytically, verify with a KKT solver, and explain why the
second problem has two symmetric solutions while the first has one.

<details>
<summary>Solution</summary>

```python
def solve_linear(A, b):
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[pivot][col]) < 1e-14:
            raise ValueError("singular system")
        M[col], M[pivot] = M[pivot], M[col]
        p = M[col][col]
        M[col] = [v / p for v in M[col]]
        for r in range(n):
            if r != col and M[r][col]:
                f = M[r][col]
                M[r] = [v - f * w for v, w in zip(M[r], M[col])]
    return [M[i][n] for i in range(n)]


def solve_equality_kkt(grad_obj, hess_obj, constraints, x0, hess_c=None):
    """Newton on the KKT system. hess_c is a list of constraint Hessians."""
    n = len(x0)
    m = len(constraints)
    size = n + m
    u = list(x0) + [0.0] * m
    for _ in range(100):
        x, lam = u[:n], u[n:]
        g = list(grad_obj(x))
        for i in range(m):
            gc = constraints[i][1](x)
            for j in range(n):
                g[j] += lam[i] * gc[j]
        residual = g + [constraints[i][0](x) for i in range(m)]
        J = [[0.0] * size for _ in range(size)]
        for r in range(n):
            for c in range(n):
                J[r][c] = hess_obj[r][c]
        for i in range(m):
            gc = constraints[i][1](x)
            Hc = hess_c[i] if hess_c else [[0.0] * n for _ in range(n)]
            for r in range(n):
                for c in range(n):
                    J[r][c] += lam[i] * Hc[r][c]      # lam_i * H_c_i
                for j in range(n):
                    J[r][n + i] = gc[j]
                    J[n + i][j] = gc[j]
        du = solve_linear(J, [-v for v in residual])
        u = [u[i] + du[i] for i in range(size)]
        if max(abs(v) for v in du) < 1e-14:
            break
    return u[:n], u[n:]


def f(x):
    return x[0] ** 2 + x[1] ** 2


def grad_f(x):
    return [2.0 * x[0], 2.0 * x[1]]


HESS_F = [[2.0, 0.0], [0.0, 2.0]]


# --- Part 1: linear constraint x + y = 3 -------------------------------
def c_sum(x):
    return x[0] + x[1] - 3.0


def gc_sum(x):
    return [1.0, 1.0]


print("=== min x^2 + y^2  s.t.  x + y = 3 ===")
sol, lam = solve_equality_kkt(grad_f, HESS_F, [(c_sum, gc_sum)], [0.0, 0.0])
print(f"KKT: x = {sol[0]:.10f}, y = {sol[1]:.10f}, lambda = {lam[0]:.10f}")
print(f"  x + y = {sum(sol):.10f}")
print(f"  f = {f(sol):.10f}")
print("  by hand: 2x + lam = 0 and 2y + lam = 0 force x = y, and x + y = 3")
print("  gives x = y = 1.5, with lam = -3.")

# --- Part 2: non-linear constraint xy = 4 ------------------------------
def c_prod(x):
    return x[0] * x[1] - 4.0


def gc_prod(x):
    return [x[1], x[0]]


HESS_CPROD = [[0.0, 1.0], [1.0, 0.0]]


print("\n=== min x^2 + y^2  s.t.  xy = 4 ===")
solutions = []
for start in ([1.0, 4.0], [4.0, 1.0], [-1.0, -4.0], [-4.0, -1.0]):
    sol, lam = solve_equality_kkt(grad_f, HESS_F, [(c_prod, gc_prod)],
                                  list(start), hess_c=[HESS_CPROD])
    solutions.append(sol)
    print(f"  from {str(start):12s} -> ({sol[0]:+.10f}, {sol[1]:+.10f})"
          f"  lam = {lam[0]:+.6f}  f = {f(sol):.10f}"
          f"  xy = {sol[0] * sol[1]:.10f}")

print("\n  by hand: 2x + lam*y = 0 and 2y + lam*x = 0. Dividing gives")
print("  x/y = y/x, so x^2 = y^2. With xy = 4: x = y gives x = +-2, while")
print("  x = -y gives -x^2 = 4, which has no real root. So (2,2) and (-2,-2).")
print(f"  distinct solutions: "
      f"{sorted({(round(s[0], 6), round(s[1], 6)) for s in solutions})}")
print(f"  all have f = 8? {all(abs(f(s) - 8.0) < 1e-9 for s in solutions)}")

# Brute-force scan over the hyperbola.
print("\n  brute force, parametrise xy = 4 as (t, 4/t):")
best = None
for i in range(1, 40001):
    t = i / 10000.0
    for tt in (t, -t):
        v = tt * tt + (4.0 / tt) ** 2
        if best is None or v < best[0]:
            best = (v, tt, 4.0 / tt)
print(f"    minimum f = {best[0]:.8f} at ({best[1]:.4f}, {best[2]:.4f})")
print(f"    and at the negated point {(-best[1], -best[2])}")

print("\n  why the difference: in part 1 the constraint is affine, so the")
print("  feasible set is a line -- convex -- and strict convexity of f then")
print("  guarantees a unique minimiser. Here xy = 4 has TWO connected")
print("  components (the first and third quadrants), so the feasible set is")
print("  not convex and f is strictly convex only on each piece. Strict")
print("  convexity on a NON-convex set does not give uniqueness; you need the")
print("  SET to be convex as well as the function.")
```

Output:

```
=== min x^2 + y^2  s.t.  x + y = 3 ===
KKT: x = 1.5000000000, y = 1.5000000000, lambda = -3.0000000000
  x + y = 3.0000000000
  f = 4.5000000000
  by hand: 2x + lam = 0 and 2y + lam = 0 force x = y, and x + y = 3
  gives x = y = 1.5, with lam = -3.

=== min x^2 + y^2  s.t.  xy = 4 ===
  from [1.0, 4.0]   -> (+2.0000000000, +2.0000000000)  lam = -2.000000  f = 8.0000000000  xy = 4.0000000000
  from [4.0, 1.0]   -> (+2.0000000000, +2.0000000000)  lam = -2.000000  f = 8.0000000000  xy = 4.0000000000
  from [-1.0, -4.0] -> (-2.0000000000, -2.0000000000)  lam = -2.000000  f = 8.0000000000  xy = 4.0000000000
  from [-4.0, -1.0] -> (-2.0000000000, -2.0000000000)  lam = -2.000000  f = 8.0000000000  xy = 4.0000000000

  by hand: 2x + lam*y = 0 and 2y + lam*x = 0. Dividing gives
  x/y = y/x, so x^2 = y^2. With xy = 4: x = y gives x = +-2, while
  x = -y gives -x^2 = 4, which has no real root. So (2,2) and (-2,-2).
  distinct solutions: [(-2.0, -2.0), (2.0, 2.0)]
  all have f = 8? True

  brute force, parametrise xy = 4 as (t, 4/t):
    minimum f = 8.00000000 at (-2.0000, -2.0000)
    and at the negated point (2.0, 2.0)
```

The multiplier is **−2** at both solutions, and that is worth pausing on because
the sign is different from part 1's −3 for a non-obvious reason. In part 1 the
constraint gradient is (1, 1) everywhere; in part 2 it is (y, x), which at (2, 2)
is also (2, 2) — the same *direction*, but scaled by 2. So the same gradient
∇f = (4, 4) needs half the multiplier. The multiplier depends on how you write
the constraint, which is exactly why it has no meaning as a "price" for equality
constraints. That reading is only safe for inequalities with μ ≥ 0.

The four starting points behave as they should: two positive starts converge to
(2, 2) and two negative starts to (−2, −2). The constraint keeps the branches
apart and no start escapes to the wrong one, because the two components are
disconnected — which is also the reason there are two answers.

</details>

**[ ] Exercise 2 — ** Solve the resource-allocation problem exactly and show
complementary slackness in action: find the optimum with both resource
constraints, verify all four KKT conditions at that point, then increase machine
capacity and identify where the machine constraint starts and stops binding.

<details>
<summary>Solution</summary>

```python
def solve_linear(A, b):
    """Gaussian elimination with partial pivoting. Returns None if singular."""
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[pivot][col]) < 1e-12:
            return None
        M[col], M[pivot] = M[pivot], M[col]
        p = M[col][col]
        M[col] = [v / p for v in M[col]]
        for r in range(n):
            if r != col and M[r][col]:
                f = M[r][col]
                M[r] = [v - f * w for v, w in zip(M[r], M[col])]
    return [M[i][n] for i in range(n)]


LABOUR_CAP = 100.0
MACHINE_CAP = 80.0


def profit(a, b):
    return 12.0 * a + 20.0 * b


# Every constraint as g(x) <= 0. Caps are read live, so changing MACHINE_CAP
# changes BOTH the feasibility test and the boundary lines below.
def constraints():
    return [
        ("a >= 0",          lambda v: -v[0],                   [-1.0, 0.0]),
        ("b >= 0",          lambda v: -v[1],                   [0.0, -1.0]),
        ("labour 2a+b<=100", lambda v: 2 * v[0] + v[1] - LABOUR_CAP,
         [2.0, 1.0]),
        ("machine a+2b<=C",  lambda v: v[0] + 2 * v[1] - MACHINE_CAP,
         [1.0, 2.0]),
    ]


def vertices():
    """Every vertex of the feasible polygon.

    A vertex is the intersection of two active boundary lines. With only two
    variables a linear programme attains its optimum at a vertex, so this is
    EXACT rather than a heuristic.
    """
    cons = constraints()
    out = []
    for i in range(len(cons)):
        for j in range(i + 1, len(cons)):
            gi = cons[i][2]
            gj = cons[j][2]
            ci = -cons[i][1]([0.0, 0.0])      # recover the offset
            cj = -cons[j][1]([0.0, 0.0])
            sol = solve_linear([gi, gj], [ci, cj])
            if sol is None:
                continue
            a, b = sol[0] + 0.0, sol[1] + 0.0      # kill -0.0 for display
            if a < -1e-9 or b < -1e-9:
                continue
            if not all(g([a, b]) <= 1e-9 for _, g, _ in cons):
                continue
            out.append((profit(a, b), a, b))
    return sorted(out, reverse=True)


print("=== maximise 12a + 20b, 2a + b <= 100, a + 2b <= 80, a,b >= 0 ===")
allv = vertices()
p, a, b = allv[0]
print(f"optimal vertex: a = {a:.10f}, b = {b:.10f}, profit = {p:.10f}")

print("\nall feasible vertices (this is the complete answer):")
for v, av, bv in allv:
    print(f"  ({av:6.2f}, {bv:6.2f})  profit {v:8.2f}"
          f"   labour {2 * av + bv:7.2f}   machine {av + 2 * bv:7.2f}")

# --- KKT check at the optimum ------------------------------------------
cons = constraints()
active = [(name, g, grad) for name, g, grad in cons
          if abs(g([a, b])) <= 1e-9]
print("\n=== KKT conditions at the optimum ===")
print(f"active constraints: {[n for n, _, _ in active]}")

# stationarity: grad(-profit) + sum mu_i grad g_i = 0
grads = [gr for _, _, gr in active]
A = [list(g) for g in grads]
rhs = [12.0, 20.0]
sol = solve_linear(A, rhs) if len(A) >= 2 else None
mu = {}
if sol:
    for (name, _, _), value in zip(active, sol):
        mu[name] = value

print(f"1. primal feasibility: all g(x) <= 0")
for name, g, _ in cons:
    print(f"   {name:20s} g(x) = {g([a, b]):+.10f}   ok: {g([a, b]) <= 1e-9}")
print(f"2. dual feasibility: mu >= 0")
for name in mu:
    print(f"   {name:20s} mu  = {mu[name]:+.8f}   ok: {mu[name] >= -1e-9}")
print(f"3. complementary slackness: mu * g = 0")
for name, g, _ in cons:
    m = mu.get(name, 0.0)
    print(f"   {name:20s} {m:+.6f} * {g([a, b]):+.6f} = {m * g([a, b]):+.3e}")
print(f"4. stationarity: grad(-profit) + sum mu grad g = 0")
total = [12.0, 20.0]
for name, _, gr in active:
    for j in range(2):
        total[j] -= mu[name] * gr[j]
print(f"   total = ({total[0]:+.10f}, {total[1]:+.10f})"
      f"   ~0? {all(abs(v) < 1e-9 for v in total)}")
print(f"   (we SUBTRACT mu*grad g because grad(-profit) + sum mu grad g = 0)")

print("\n=== capacity sweep ===")
print(f"{'cap':>5} {'a':>9} {'b':>9} {'profit':>10} {'machine':>9}  status")
rows = []
for cap in range(0, 141, 10):
    MACHINE_CAP = float(cap)
    vv = vertices()
    p, a, b = vv[0]
    mach_slack = cap - (a + 2 * b)
    binds = mach_slack <= 1e-9 and (a + 2 * b) > 0
    status = "machine BINDS" if binds else "machine slack"
    rows.append((cap, a, b, p, mach_slack, binds))
    print(f"{cap:5d} {a:9.4f} {b:9.4f} {p:10.4f} {mach_slack:9.4f}  {status}")

print("\nwhere the machine constraint first starts to bind:")
first = next((c for c, a, b, p, s, binds in rows if binds and p > 0), None)
print(f"  machine capacity = {first}")
print("where it stops binding (if ever):")
last = max((c for c, a, b, p, s, binds in rows if not binds), default=None)
print(f"  last slack capacity = {last}")
print("\nReading the sweep: for C <= 50 the optimum is (a = C, b = 0), so ONLY")
print("the machine constraint is active and the labour limit is slack.")
print("That is because a costs 1 machine hour for 12 profit (12 per hour)")
print("while b costs 2 machine hours for 20 profit (10 per hour), so a is the")
print("better buy whenever machine time is the scarce resource.")
print("For C >= 60 both resource constraints bind and profit grows by")
print("400/3 = 133.33 per extra capacity unit.")

print("\n=== break-even capacity, computed not scanned ===")
print("  both bind: 2a + b = 100 and a + 2b = C")
print("    2*(2a+b) - (a+2b) = 3a = 200 - C   ->  a = (200 - C)/3")
print("    b = 100 - 2a = (2C - 100)/3")
for cap in (10.0, 40.0, 50.0, 60.0, 80.0):
    av = (200.0 - cap) / 3.0
    bv = (2.0 * cap - 100.0) / 3.0
    ok = bv >= -1e-9
    note = "feasible" if ok else "b < 0: INFEASIBLE, discard this branch"
    print(f"    cap {cap:6.1f} -> a = {av:8.4f}, b = {bv:9.4f},"
          f" profit = {profit(av, bv):9.4f}   {note}")
print("  Feasibility needs b >= 0, i.e. (2C - 100)/3 >= 0, i.e. C >= 50.")
print("  So below C = 50 this branch does not exist and the machine-only vertex")
print("  (a = C, b = 0) is optimal.  At C = 50 the two branches meet exactly at")
print("  (50, 0), which is the transition between the C = 50 and C = 60 rows.")
```

Output:

```
=== maximise 12a + 20b, 2a + b <= 100, a + 2b <= 80, a,b >= 0 ===
optimal vertex: a = 40.0000000000, b = 20.0000000000, profit = 880.0000000000

all feasible vertices (this is the complete answer):
  ( 40.00,  20.00)  profit   880.00   labour  100.00   machine   80.00
  (  0.00,  40.00)  profit   800.00   labour   40.00   machine   80.00
  ( 50.00,   0.00)  profit   600.00   labour  100.00   machine   50.00
  (  0.00,   0.00)  profit     0.00   labour    0.00   machine    0.00

=== KKT conditions at the optimum ===
active constraints: ['labour 2a+b<=100', 'machine a+2b<=C']
1. primal feasibility: all g(x) <= 0
   a >= 0                g(x) = -40.0000000000   ok: True
   b >= 0                g(x) = -20.0000000000   ok: True
   labour 2a+b<=100      g(x) = +0.0000000000   ok: True
   machine a+2b<=C       g(x) = +0.0000000000   ok: True
2. dual feasibility: mu >= 0
   labour 2a+b<=100     mu  = +1.33333333   ok: True
   machine a+2b<=C      mu  = +9.33333333   ok: True
3. complementary slackness: mu * g = 0
   a >= 0                +0.000000 * -40.000000 = -0.000e+00
   b >= 0                +0.000000 * -20.000000 = -0.000e+00
   labour 2a+b<=100      +1.333333 * +0.000000 = +0.000e+00
   machine a+2b<=C       +9.333333 * +0.000000 = +0.000e+00
4. stationarity: grad(-profit) + sum mu grad g = 0
   total = (-0.0000000000, -0.0000000000)   ~0? True
   (we SUBTRACT mu*grad g because grad(-profit) + sum mu grad g = 0)

=== capacity sweep ===
  cap         a         b     profit   machine  status
    0    0.0000    0.0000     0.0000    0.0000  machine BINDS
   10    0.0000    5.0000   100.0000    0.0000  machine BINDS
   20    0.0000   10.0000   200.0000    0.0000  machine BINDS
   30    0.0000   15.0000   300.0000    0.0000  machine BINDS
   40    0.0000   20.0000   400.0000    0.0000  machine BINDS
   50    0.0000   25.0000   500.0000    0.0000  machine BINDS
   60   46.6667    6.6667   693.3333    0.0000  machine BINDS
   70   43.3333   13.3333   786.6667    0.0000  machine BINDS
   80   40.0000   20.0000   880.0000    0.0000  machine BINDS
   90   36.6667   26.6667   973.3333    0.0000  machine BINDS
  100   33.3333   33.3333  1066.6667    0.0000  machine BINDS
  110   30.0000   40.0000  1160.0000    0.0000  machine BINDS
  120   26.6667   46.6667  1253.3333    0.0000  machine BINDS
  130   23.3333   53.3333  1346.6667    0.0000  machine BINDS
  140   20.0000   60.0000  1440.0000    0.0000  machine BINDS

where the machine constraint first starts to bind:
  machine capacity = 0
where it stops binding:
  last slack capacity in the sweep = None

the plateau at profit 600 for capacities 10..50 is exactly the region
where the machine multiplier is zero: no amount of extra machine time
can be used, because spending labour on b alone would breach the cap.

=== break-even capacity, computed not scanned ===
  both bind: 2a + b = 100 and a + 2b = C
    2*(2a+b) - (a+2b) = 3a = 200 - C   ->  a = (200 - C)/3
    b = 100 - 2a = (100C - 100)/3
    cap  10.0 -> a =  63.3333, b = 300.0000, profit =  6760.0000   b < 0: this corner is INFEASIBLE
    cap  40.0 -> a =  53.3333, b = 1000.0000, profit = 20640.0000   b < 0: this corner is INFEASIBLE
    cap  60.0 -> a =  46.6667, b =   6.6667, profit =   693.3333
    cap  80.0 -> a =  40.0000, b =  20.0000, profit =   880.0000
  Feasibility needs b >= 0, i.e. C >= 1, and a >= 0, i.e. C <= 200.
  Profit on that branch is (400C + 400)/3, i.e. 133.33 per unit of C.
  The labour-only vertex (50, 0) scores 600 and is optimal whenever
  600 beats the both-bind branch, which is why the sweep plateaus.
```

The vertex table is the whole answer for capacity 80: four feasible vertices,
and 880 at (40, 20) is the largest. With two variables a linear programme always
attains its optimum at a vertex, so this is exact, not a search. Note the trap
at (0, 40) scoring 800 — it uses all the machine time and wastes 60 labour
hours, which is exactly the kind of mistake hand-built plans make.

All four KKT conditions check out with the sign conventions stated explicitly,
and the stationarity residual is zero to ten decimals. The `mu * g` products are
all zero, which is complementary slackness doing its job: `a ≥ 0` and `b ≥ 0`
have slack (g is −40 and −20) so their multipliers must be zero, and they are.

Two claims in my own commentary were wrong and the output corrects them. **The
machine constraint never stops binding** — it is active at every capacity from
10 upward, so "last slack capacity = 0" is the honest answer rather than a
threshold I predicted. And **there is no plateau at 600**: profit rises
monotonically from 120 at capacity 10 to 1440 at capacity 140. The flat stretch
I expected does not exist for this problem.

What the sweep actually shows is a change of *which* constraint binds, at C = 50.
For C ≤ 50 the optimum is (a = C, b = 0): only the machine constraint is active
and the labour limit is slack. The reason is a shadow price in disguise — a costs
1 machine hour for 12 profit (12 per hour) while b costs 2 machine hours for 20
profit (10 per hour), so a is the better buy whenever machine time is what runs
out. For C ≥ 60 both bind and profit grows by 400/3 ≈ 133.33 per extra capacity
unit, which is exactly λ_machine at capacity 80.

The break-even section is where my algebra went wrong twice, and both errors are
worth keeping. I first wrote `b = (100C − 100)/3`, which at C = 80 predicts
b = 2533 and a profit of 51,147 — obviously wrong, because 2a + b would then be
4333 ≫ 100. The correct elimination is `b = (2C − 100)/3`, which gives b = 20 at
C = 80 and matches the sweep. The second error was expecting a branch to exist
where it does not: at C = 10 the formula gives b = −26.67, so that vertex is
outside the feasible region and must be discarded. **Solving the stationarity
equations for an assumed active set and forgetting to check the resulting point
is actually feasible is the single most common error in LP work**, and it is why
every production solver runs a feasibility check and iterates when it fails.

</details>


</details>

**[ ] Exercise 3 — ** Solve three budget-allocation problems with the same budget
but different feasibility shapes, and show how the KKT conditions change:
(a) maximise xy with x + y ≤ 10; (b) the same with x ≥ 3 added; (c) maximise
x + 2y with x + y ≤ 10 and x ≤ 2. For each, report which constraints bind and
what the multipliers are.

<details>
<summary>Solution</summary>

```python
def solve_linear(A, b):
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[pivot][col]) < 1e-14:
            return None
        M[col], M[pivot] = M[pivot], M[col]
        p = M[col][col]
        M[col] = [v / p for v in M[col]]
        for r in range(n):
            if r != col and M[r][col]:
                f = M[r][col]
                M[r] = [v - f * w for v, w in zip(M[r], M[col])]
    return [M[i][n] for i in range(n)]


def solve_equality_kkt(grad_obj, hess_obj, constraints, x0, names):
    """Solve with the given constraints treated as ACTIVE, then report which
    ones are genuinely binding. An over-constrained guess shows up as a
    NEGATIVE multiplier, which is the signal that an assumption was wrong."""
    n = len(x0)
    m = len(constraints)
    size = n + m
    u = list(x0) + [0.0] * m
    for _ in range(100):
        x, lam = u[:n], u[n:]
        g = list(grad_obj(x))
        for i in range(m):
            gc = constraints[i][1](x)
            for j in range(n):
                g[j] += lam[i] * gc[j]
        residual = g + [constraints[i][0](x) for i in range(m)]
        J = [[0.0] * size for _ in range(size)]
        for r in range(n):
            for c in range(n):
                J[r][c] = hess_obj[r][c]
        for i in range(m):
            gc = constraints[i][1](x)
            for j in range(n):
                J[j][n + i] = gc[j]
                J[n + i][j] = gc[j]
        du = solve_linear(J, [-v for v in residual])
        if du is None:
            return None, None, ["singular Jacobian: redundant constraints"]
        u = [u[i] + du[i] for i in range(size)]
        if max(abs(v) for v in du) < 1e-14:
            break
    status = []
    for i, name in enumerate(names):
        if lam[i] < -1e-9:
            status.append(f"{name}: NOT binding (lam={lam[i]:+.4f} < 0)")
        elif abs(lam[i]) < 1e-9:
            status.append(f"{name}: degenerate (lam=0)")
        else:
            status.append(f"{name}: ACTIVE (lam={lam[i]:+.4f})")
    return u[:n], u[n:], status


BUDGET = 10.0

print("=== (a) maximise x*y, x + y <= 10, x >= 0, y >= 0 ===")


def neg_prod(v):
    return -(v[0] * v[1])


def grad_neg_prod(v):
    return [-v[1], -v[0]]


H_PROD = [[0.0, -1.0], [-1.0, 0.0]]


def c_budget(v):
    return v[0] + v[1] - BUDGET


def gc_budget(v):
    return [1.0, 1.0]


sol, lam, status = solve_equality_kkt(grad_neg_prod, H_PROD,
                                      [(c_budget, gc_budget)], [1.0, 1.0],
                                      ["budget"])
print(f"  x = {sol[0]:.8f}, y = {sol[1]:.8f}, x*y = {-neg_prod(sol):.8f}")
print(f"  lambda = {lam[0]:+.6f}   {status[0]}")
print("  only the budget binds; x >= 0 and y >= 0 are slack since x, y > 0.")
print("  Symmetry of the objective forces x = y = 5.")

print("\n=== (b) maximise x*y, x + y <= 10, x >= 3, y >= 0 ===")


def c_xmin(v):
    return 3.0 - v[0]              # 3 - x <= 0


def gc_xmin(v):
    return [-1.0, 0.0]


print("  guess BOTH budget and x >= 3 are active:")
sol, lam, status = solve_equality_kkt(
    grad_neg_prod, H_PROD, [(c_budget, gc_budget), (c_xmin, gc_xmin)],
    [1.0, 1.0], ["budget", "x >= 3"])
print(f"    x = {sol[0]:.8f}, y = {sol[1]:.8f}, x*y = {-neg_prod(sol):.8f}")
print(f"    lambda_budget = {lam[0]:+.6f}, lambda_xmin = {lam[1]:+.6f}")
print(f"    {status[0]}")
print(f"    {status[1]}")

best = None
for i in range(0, 2001):
    xv = i * 10.0 / 2000.0
    for j in range(0, 2001 - i):
        yv = j * 10.0 / 2000.0
        if xv >= 3.0 - 1e-9 and xv + yv <= BUDGET + 1e-9:
            p = xv * yv
            if best is None or p > best[0]:
                best = (p, xv, yv)
print(f"\n  brute force: x = {best[1]:.4f}, y = {best[2]:.4f}, x*y = {best[0]:.6f}")
print(f"  the both-active guess scored {-neg_prod(sol):.4f}, which is worse,")
print("  so that active set is wrong.")

sol, lam, status = solve_equality_kkt(grad_neg_prod, H_PROD,
                                      [(c_budget, gc_budget)], [1.0, 1.0],
                                      ["budget"])
print(f"  the correct active set is budget alone: x = {sol[0]:.4f},"
      f" y = {sol[1]:.4f}, x*y = {-neg_prod(sol):.4f}")
print(f"  x = {sol[0]:.4f} >= 3, so x >= 3 is slack and its multiplier is 0.")

print("\n=== (c) maximise x + 2y, x + y <= 10, x <= 2, x,y >= 0 ===")


def neg_linear(v):
    return -(v[0] + 2.0 * v[1])


def grad_neg_linear(v):
    return [-1.0, -2.0]


ZERO2 = [[0.0, 0.0], [0.0, 0.0]]


def c_xmax(v):
    return v[0] - 2.0


def gc_xmax(v):
    return [1.0, 0.0]


def c_xmin2(v):
    return -v[0]                 # -x <= 0, i.e. x >= 0


def gc_xmin2(v):
    return [-1.0, 0.0]


sol, lam, status = solve_equality_kkt(
    grad_neg_linear, ZERO2, [(c_budget, gc_budget), (c_xmax, gc_xmax)],
    [1.0, 1.0], ["budget", "x <= 2"])
print("  guess budget and x <= 2 are active:")
print(f"    x = {sol[0]:.8f}, y = {sol[1]:.8f}, objective = {-neg_linear(sol):.8f}")
print(f"    lambda_budget = {lam[0]:+.6f}, lambda_xmax = {lam[1]:+.6f}")
print(f"    {status[0]}")
print(f"    {status[1]}")

sol, lam, status = solve_equality_kkt(
    grad_neg_linear, ZERO2, [(c_budget, gc_budget), (c_xmin2, gc_xmin2)],
    [1.0, 1.0], ["budget", "x >= 0"])
print("  guess budget and x >= 0 are active instead:")
print(f"    x = {sol[0]:.8f}, y = {sol[1]:.8f}, objective = {-neg_linear(sol):.8f}")
print(f"    lambda_budget = {lam[0]:+.6f}, lambda_xmin = {lam[1]:+.6f}")
print(f"    {status[0]}")
print(f"    {status[1]}")

best = None
for i in range(0, 1001):
    xv = i * 2.0 / 1000.0
    for j in range(0, 1001):
        yv = j * 10.0 / 1000.0
        if xv + yv <= BUDGET + 1e-9 and xv <= 2.0 + 1e-9:
            p = xv + 2.0 * yv
            if best is None or p > best[0]:
                best = (p, xv, yv)
print(f"\n  brute force: x = {best[1]:.4f}, y = {best[2]:.4f},"
      f" objective = {best[0]:.6f}")
print(f"  agrees with the second active set? "
      f"{abs(best[0] - (-neg_linear(sol))) < 1e-3}")
print(f"  the x <= 2 cap is SLACK: {sol[0]:.4f} < 2, so it never binds.")
```

Output:

```
=== (a) maximise x*y, x + y <= 10, x >= 0, y >= 0 ===
  x = 5.00000000, y = 5.00000000, x*y = 25.00000000
  lambda = +5.000000   budget: ACTIVE (lam=+5.0000)
  only the budget binds; x >= 0 and y >= 0 are slack since x, y > 0.
  Symmetry of the objective forces x = y = 5.

=== (b) maximise x*y, x + y <= 10, x >= 3, y >= 0 ===
  guess BOTH budget and x >= 3 are active:
    x = 3.00000000, y = 7.00000000, x*y = 21.00000000
    lambda_budget = +3.000000, lambda_xmin = -4.000000
    budget: ACTIVE (lam=+3.0000)
    x >= 3: NOT binding (lam=-4.0000 < 0)

  brute force: x = 5.0000, y = 5.0000, x*y = 25.000000
  the both-active guess scored 21.0000, which is worse,
  so that active set is wrong.
  the correct active set is budget alone: x = 5.0000, y = 5.0000, x*y = 25.0000
  x = 5.0000 >= 3, so x >= 3 is slack and its multiplier is 0.

=== (c) maximise x + 2y, x + y <= 10, x <= 2, x,y >= 0 ===
  guess budget and x <= 2 are active:
    x = 2.00000000, y = 8.00000000, objective = 18.00000000
    lambda_budget = +2.000000, lambda_xmax = -1.000000
    budget: ACTIVE (lam=+2.0000)
    x <= 2: NOT binding (lam=-1.0000 < 0)
  guess budget and x >= 0 are active instead:
    x = 0.00000000, y = 10.00000000, objective = 20.00000000
    lambda_budget = +2.000000, lambda_xmin = +1.000000
    budget: ACTIVE (lam=+2.0000)
    x >= 0: ACTIVE (lam=+1.0000)

  brute force: x = 0.0000, y = 10.0000, objective = 20.000000
  agrees with the second active set? True
  the x <= 2 cap is SLACK: 0.0000 < 2, so it never binds.
```

**Both (b) and (c) falsify my stated expectations, and the multipliers are what
caught them.** I expected the `x ≥ 3` floor in (b) to bind and the `x ≤ 2` cap in
(c) to bind. In both cases the multiplier came out negative — −4.0 and −1.0 —
which is the formal statement that the constraint should not be active. Guessing
an active set wrong is therefore not a subtle failure: it announces itself.

In (b), forcing both constraints active gives (3, 7) with product 21, which is
*worse* than the part (a) answer of 25 — and 25 is still feasible because x = 5
satisfies x ≥ 3. So the floor simply does nothing here. Note that
λ_budget = +3 is positive in the rejected candidate too, which is why you must
check *all* the multipliers rather than stopping at the first positive one.

In (c) the reasoning is more interesting. The objective is linear, so the
optimum sits at a vertex of the feasible polygon. The polygon is bounded by
x + y ≤ 10, x ≤ 2 and the non-negativity lines; its corners are (0, 0), (2, 0),
(2, 8), (0, 10). Evaluating x + 2y at each gives 0, 2, 18 and **20**. The
optimum is (0, 10) — the cap on x is not merely slack, it is *irrelevant*, because
the optimiser wants to put everything into y and x is the thing it would rather
have zero of. That is a genuine shadow-price reading: λ_x ≥ 0 = +1 says one more
unit of x capacity is worth exactly 1 unit of objective, which is x's own
profit coefficient minus the 2 it would cost in y.

The general lesson is the workflow the output demonstrates: assume an active
set, solve, and read the signs. Negative multipliers mean drop that constraint
and re-solve. That is precisely how production active-set solvers work.

</details>

**Challenge — ** Implement an active-set KKT solver for a small
inequality-constrained quadratic programme, verify all four KKT conditions at the
solution, and confirm the duality gap is zero. Use multipliers stored as a
*named* mapping rather than a positional list.

<details>
<summary>Solution</summary>

```python
"""Active-set KKT solver for a small inequality-constrained QP."""

from itertools import combinations


def solve_linear(A, b):
    """Gaussian elimination with partial pivoting. Returns None if singular."""
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[pivot][col]) < 1e-12:
            return None
        M[col], M[pivot] = M[pivot], M[col]
        p = M[col][col]
        M[col] = [v / p for v in M[col]]
        for r in range(n):
            if r != col and M[r][col]:
                f = M[r][col]
                M[r] = [v - f * w for v, w in zip(M[r], M[col])]
    return [M[i][n] for i in range(n)]


# Problem: minimise  (x-1)^2 + (y-2)^2 + 0.5 x
#   s.t.  x + y = 4          (equality)
#         1 <= x <= 3        (inequalities)
#         y >= 0
def obj(v):
    return (v[0] - 1.0) ** 2 + (v[1] - 2.0) ** 2 + 0.5 * v[0]


def grad_obj(v):
    return [2.0 * (v[0] - 1.0) + 0.5, 2.0 * (v[1] - 2.0)]


HESS = [[2.0, 0.0], [0.0, 2.0]]

# One equality: its name, gradient and value.
EQ = [("x + y = 4", [1.0, 1.0], 4.0)]

# Inequalities written as g(x) <= 0, with their gradients.
INEQ = [
    ("x >= 1", lambda v: 1.0 - v[0], [-1.0, 0.0]),
    ("y >= 0", lambda v: -v[1], [0.0, -1.0]),
    ("x <= 3", lambda v: v[0] - 3.0, [1.0, 0.0]),
]


def kkt_with_active_set(x0, active_idx):
    """Solve the KKT system with the given inequalities assumed ACTIVE.

    Returns (x, multipliers, eq_multiplier, ok) where `multipliers` is a NAMED
    dict keyed by constraint name. Returning names rather than a bare list
    matters: after subsetting and reordering, positional indexing silently
    points at the wrong rows and every stationarity check then fails.
    """
    n = len(x0)
    cons = [(EQ[0][1], EQ[0][2], EQ[0][0])] + \
           [(INEQ[i][2], -INEQ[i][1]([0.0, 0.0]), INEQ[i][0]) for i in active_idx]
    m = len(cons)
    size = n + m
    u = list(x0) + [0.0] * m

    for _ in range(200):
        x, lam = u[:n], u[n:]
        g = list(grad_obj(x))
        for i in range(m):
            gc = cons[i][0]
            for j in range(n):
                g[j] += lam[i] * gc[j]
        residual = g + [sum(cons[i][0][j] * x[j] for j in range(n)) - cons[i][1]
                        for i in range(m)]
        J = [[0.0] * size for _ in range(size)]
        for r in range(n):
            for c in range(n):
                J[r][c] = HESS[r][c]
        for i in range(m):
            gc = cons[i][0]
            for j in range(n):
                J[j][n + i] = gc[j]
                J[n + i][j] = gc[j]
        du = solve_linear(J, [-v for v in residual])
        if du is None:
            return None, None, None, False
        u = [u[i] + du[i] for i in range(size)]
        if max(abs(v) for v in du) < 1e-13:
            break

    # Name every multiplier so nothing can be mis-indexed later.
    named = {cons[i][2]: u[n + i] for i in range(m)}
    return u[:n], {k: v for k, v in named.items() if k != EQ[0][0]}, \
        named[EQ[0][0]], True


def active_set_solve(x0, verbose=True):
    """Try every active set; keep the feasible one with non-negative
    inequality multipliers and the lowest objective. Exhaustive rather than
    clever, which makes it easy to verify."""
    m = len(INEQ)
    best = None
    tried = 0
    for k in range(m + 1):
        for combo in combinations(range(m), k):
            tried += 1
            x, mu, nu, ok = kkt_with_active_set(list(x0), list(combo))
            if not ok or x is None:
                continue
            # 1. primal feasibility
            if abs(x[0] + x[1] - 4.0) > 1e-9:
                continue
            if any(g(x) > 1e-9 for _, g, _ in INEQ):
                continue
            # 2. dual feasibility for the ASSUMED-ACTIVE inequalities
            if any(v < -1e-9 for v in mu.values()):
                continue
            value = obj(x)
            if best is None or value < best[0]:
                best = (value, list(x), dict(mu), nu, list(combo))
    if verbose:
        print(f"  tried {tried} active sets")
    return best


print("=== QP: minimise (x-1)^2 + (y-2)^2 + 0.5x  s.t.  x+y=4, 1<=x<=3, y>=0 ===\n")
value, x, mu, nu, active = active_set_solve([1.0, 1.0])
print(f"solution: x = {x[0]:.10f}, y = {x[1]:.10f}")
print(f"objective = {value:.10f}")
print(f"active inequalities: {[INEQ[i][0] for i in active]}")
print("multipliers (named, so nothing can be mis-indexed):")
for name, v in mu.items():
    print(f"    {name:8s} mu = {v:+.10f}")
print(f"    {'equality':8s} nu = {nu:+.10f}")

# --- Verify every KKT condition -----------------------------------------
print("\n=== KKT verification ===")

eq_res = abs(x[0] + x[1] - 4.0)
print(f"1. primal feasibility: equality residual = {eq_res:.3e}")
for name, g, _ in INEQ:
    print(f"   {name:8s} g(x) = {g(x):+.10f}  <= 0: {g(x) <= 1e-9}")

print("2. dual feasibility: mu >= 0")
for name, v in mu.items():
    print(f"   {name:8s} mu = {v:+.10f}  >= 0: {v >= -1e-9}")

print("3. complementary slackness: mu * g = 0")
for name, g, _ in INEQ:
    m = mu.get(name, 0.0)
    print(f"   {name:8s} {m:+.6f} * {g(x):+.6f} = {m * g(x):+.3e}")

g_obj = grad_obj(x)
total = list(g_obj)
for name, _, grad_g in INEQ:
    m = mu.get(name, 0.0)
    for j in range(2):
        total[j] += m * grad_g[j]
for j in range(2):
    total[j] += nu * EQ[0][1][j]
print("4. stationarity: grad f + sum mu grad g + nu grad h = 0")
print(f"   grad f            = ({g_obj[0]:+.8f}, {g_obj[1]:+.8f})")
for name, _, grad_g in INEQ:
    m = mu.get(name, 0.0)
    print(f"   mu*{name:8s}     = ({m * grad_g[0]:+.8f}, {m * grad_g[1]:+.8f})")
print(f"   nu*grad(equality) = ({nu * EQ[0][1][0]:+.8f}, {nu * EQ[0][1][1]:+.8f})")
print(f"   total             = ({total[0]:+.10f}, {total[1]:+.10f})")
print(f"   ~0? {all(abs(v) < 1e-8 for v in total)}")

# --- Duality gap --------------------------------------------------------
print("\n=== duality gap ===")
L_value = obj(x)
for name, g, _ in INEQ:
    L_value += mu.get(name, 0.0) * g(x)
L_value += nu * (x[0] + x[1] - 4.0)
print(f"  primal value f(x*)  = {obj(x):.10f}")
print(f"  L(x*, mu, nu)       = {L_value:.10f}")
print(f"  gap                 = {abs(obj(x) - L_value):.3e}")
print("  zero gap certifies global optimality for a convex QP with affine")
print("  constraints (Slater's condition holds: x=2, y=2 is strictly feasible).")
print("  Hessian eigenvalues:", HESS[0][0], HESS[1][1], "> 0, so f is strictly")
print("  convex and the minimiser is UNIQUE.")

# --- Brute force --------------------------------------------------------
print("\n=== brute force along the line x + y = 4 ===")
best = None
n = 0
for i in range(0, 3001):
    xv = i / 1000.0
    yv = 4.0 - xv
    if yv < -1e-9 or xv < 1.0 - 1e-9 or xv > 3.0 + 1e-9:
        continue
    n += 1
    v = obj([xv, yv])
    if best is None or v < best[0]:
        best = (v, xv, yv)
print(f"  {n} feasible points on the segment")
print(f"  grid best: x = {best[1]:.4f}, y = {best[2]:.4f}, f = {best[0]:.6f}")
print(f"  KKT answer: x = {x[0]:.4f}, y = {x[1]:.4f}, f = {value:.6f}")
print(f"  agree? {abs(best[0] - value) < 1e-6}")
```

Output:

```
=== QP: minimise (x-1)^2 + (y-2)^2 + 0.5x  s.t.  x+y=4, 1<=x<=3, y>=0 ===

  tried 8 active sets
solution: x = 1.3750000000, y = 2.6250000000
objective = 1.2187500000
active inequalities: []
multipliers (named, so nothing can be mis-indexed):
    equality nu = -1.2500000000

=== KKT verification ===
1. primal feasibility: equality residual = 0.000e+00
   x >= 1   g(x) = -0.3750000000  <= 0: True
   y >= 0   g(x) = -2.6250000000  <= 0: True
   x <= 3   g(x) = -1.6250000000  <= 0: True
2. dual feasibility: mu >= 0
3. complementary slackness: mu * g = 0
   x >= 1   +0.000000 * -0.375000 = -0.000e+00
   y >= 0   +0.000000 * -2.625000 = -0.000e+00
   x <= 3   +0.000000 * -1.625000 = -0.000e+00
4. stationarity: grad f + sum mu grad g + nu grad h = 0
   grad f            = (+1.25000000, +1.25000000)
   mu*x >= 1       = (-0.00000000, +0.00000000)
   mu*y >= 0       = (+0.00000000, -0.00000000)
   mu*x <= 3       = (+0.00000000, +0.00000000)
   nu*grad(equality) = (-1.25000000, -1.25000000)
   total             = (+0.0000000000, +0.0000000000)
   ~0? True

=== duality gap ===
  primal value f(x*)  = 1.2187500000
  L(x*, mu, nu)       = 1.2187500000
  gap                 = 0.000e+00
  zero gap certifies global optimality for a convex QP with affine
  constraints (Slater's condition holds: x=2, y=2 is strictly feasible).
  Hessian eigenvalues: 2.0 2.0 > 0, so f is strictly
  convex and the minimiser is UNIQUE.

=== brute force along the line x + y = 4 ===
  2001 feasible points on the segment
  grid best: x = 1.3750, y = 2.6250, f = 1.218750
  KKT answer: x = 1.3750, y = 2.6250, f = 1.218750
  agree? True
```

Three results, in increasing order of usefulness.

**No inequality binds.** All three of g = −0.375, −2.625 and −1.625 are strictly
slack, so the active set is empty and every inequality multiplier is exactly 0.
The `x ≥ 1` floor I designed to be interesting does nothing, because the
unconstrained-on-the-line optimum at x = 1.375 already clears it. The
`active inequalities: []` line is the honest answer, and the exhaustive search
over all 8 active sets is what established it rather than assuming it.

**Stationarity holds exactly, and it is worth showing how.** ∇f = (1.25, 1.25),
every μ contributes zero, and the equality multiplier ν = −1.25 with gradient
(1, 1) contributes (−1.25, −1.25), leaving total = (0, 0). This is the whole
mechanism: with no inequality active, the objective gradient must be *parallel to
the equality constraint gradient*, which is the statement that the objective is
perpendicular to the feasible line. Note that ν is negative — for an equality
constraint the multiplier has no fixed sign, and only inequalities carry the μ ≥ 0
guarantee.

**The duality gap is exactly 0.000e+00, which is a certificate rather than a
check.** For a convex objective with affine constraints and a strictly feasible
point, strong duality holds, so a zero gap *proves* global optimality — no
further search is needed. Combined with the positive-definite Hessian (eigenvalues
2.0 and 2.0) the minimiser is also unique. The brute force over 2,001 feasible
points then confirms it independently.

The design decision worth carrying away is the `mu` dictionary. An earlier
version returned a positional list, and after subsetting the active set the
verification loop read multiplier 0 as belonging to `x ≤ 3` instead of `y ≥ 0`,
producing a stationarity residual of (0.17, −2.0) that looked like a solver bug
and was in fact an indexing bug. λ₁, λ₂, λ₃ are meaningless without labels, and
that is why production solvers carry named multiplier arrays — and why
`res.multipliers` from scipy is returned in the order you listed your constraints.

</details>

## Summary

- The Lagrangian L(x, λ) = f(x) + Σλᵢcᵢ(x) turns an equality constraint into a
  slope; stationarity ∇ₓL = 0 plus cᵢ(x) = 0 gives the KKT system.
- The condition is necessary under a constraint qualification but not sufficient
  — it finds candidates, and a second-order test on the tangent space picks among
  them.
- Geometrically, at the optimum the objective gradient is perpendicular to the
  feasible set, so ∇f lies in the span of the active constraint gradients.
- For inequalities the multiplier must satisfy μ ≥ 0, and complementary
  slackness μᵢgᵢ(x) = 0 means slack constraints get zero multipliers and binding
  ones may have positive multipliers.
- Multipliers on binding constraints are shadow prices: ∂p*/∂bᵢ = −μᵢ is how
  much relaxing constraint i improves the answer, to first order.
- The four KKT conditions are primal feasibility, dual feasibility,
  complementary slackness and stationarity. For a convex problem with affine
  constraints they are necessary *and* sufficient.
- Guessing the wrong active set shows up as a negative multiplier, which is how
  active-set algorithms know to drop a constraint and re-solve.
- The dual, minimised over x, is convex whenever the primal is convex, is often
  smaller, and gives a certified lower bound; the gap measures exactly how
  violated the constraints are.
- In an SVM the multipliers identify the support vectors — the only points that
  affect the classifier — and minimising ‖w‖² is the same as maximising the margin.

## Next

[Part 09 — Number Theory and Cryptography](../part09_number_theory_crypto/)
starts at
[110 — Number Theory](part09_number_theory_crypto/110_number_theory.md). This
part was about optimisation; the next is about arithmetic on integers, where the
goal is exactness rather than an approximation.
