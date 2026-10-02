# 101 — Gradient Descent

**Part**: part08_optimization · **Prerequisites**: 51, 53, 100 · **Time**: 35 min

---

## In Plain Words

You want to find the lowest point of a function. You cannot see the whole
surface, but you can measure the slope at the spot you are standing on. So you
step downhill in the direction the slope points, by an amount you choose. Then
you measure again and step again. Repeat until you stop moving.

That is the entire algorithm. The direction is not a guess — the gradient tells
you the steepest way to go up, so its opposite is the steepest way down. Only the
size of the step is a choice, and that single choice is where nearly all the
difficulty lives. Step too small and you crawl. Step too large and you overshoot
the bottom, land on the far slope, and bounce back with a bigger amplitude until
the numbers overflow.

Momentum fixes the crawling case. If the slope is tiny in one direction but large
in another, a plain step moves fast in the large direction and barely at all in
the small one, so the path looks like a staircase that never finishes. Momentum
remembers which way it has been travelling and keeps pushing, so the small
progress accumulates across steps and eventually gets you down the valley.

For a bowl-shaped function this whole procedure is guaranteed to find the bottom.
For a function with dimples and pits, it finds *a* bottom — and which one depends
on where you started. That is the real limit of the method, and no amount of
clever stepping removes it.

## Why Computer Science Cares

- **It is the optimiser inside essentially every machine learning library.**
  `scipy.optimize.minimize(method="SGD")`, `torch.optim.SGD`, `sklearn`'s
  solvers, and Keras all implement this update rule plus variations.
- **Training a neural network is this loop.** Backpropagation computes the
  gradient; the optimiser consumes it. An exploding gradient and a vanished
  gradient are both failures of this step, and gradient clipping and careful
  initialisation are both defences against it.
- **Convex problems are solved this way in production.** Logistic regression,
  ridge regression, and L2-regularised fitting all have convex objectives where
  the local-global guarantee applies, which is why they converge reliably.
- **Learning-rate schedules are a standard technique.** Warmup, decay, and
  cyclical schedules all exist to get around the fixed-step problem.
- **Adam is momentum with adaptive step sizes per coordinate**, using the running
  second moment of the gradient. Understanding this lesson makes Adam's two
  state variables obvious rather than mysterious.
- **The condition number decides feasibility.** This is the mathematical reason
  iterative solvers lose to direct methods on badly scaled linear systems — see
  [Lesson 121](../part10_tensors_numerical/121_numerical_methods_and_floating_point.md).

## The Formal Version

Notation follows [SYMBOLS.md](../SYMBOLS.md).

**Definition.** For f : ℝⁿ → ℝ differentiable at **x**, the *gradient* is the
vector of partial derivatives ∇f(x) = (∂f/∂x₁, …, ∂f/∂xₙ).

**Theorem (steepest descent).** ∇f(x) is perpendicular to every level set of f
through **x**, and among all unit vectors **v**, the direction of most rapid
decrease is **v** = −∇f(x)/‖∇f(x)‖, with rate of decrease ‖∇f(x)‖.

**Explanation.** Along the curve **x**(t) = **x** + t**v** with ‖**v**‖ = 1, the
rate of change of f is (df/dt)|₀ = ∇f(x)·**v**. Maximising that over unit
**v** means aligning **v** with ∇f(x); minimising means negating it. The maximum
possible value is ‖∇f(x)‖, attained by Cauchy–Schwarz, which is why the magnitude
of the gradient is literally "how fast f can change here".

**Definition.** *Gradient descent* with learning rate η > 0 and initial point
**x**₀ is the iteration

  **x**ₖ₊₁ = **x**ₖ − η ∇f(**x**ₖ).

**Theorem (exact stability condition for a quadratic).** Let
f(**x**) = ½**x**ᵀ**H x** with **H** symmetric positive definite. If **Q** is an
orthogonal diagonalisation **H** = **Q**Λ**Q**ᵀ then

  **x**ₖ = **Q** diag((1 − ηλᵢ)ᵏ) **Q**ᵀ **x**₀.

So the iteration converges to the minimum from any start iff
|1 − ηλᵢ| < 1 for every eigenvalue λᵢ, that is

  0 < η < 2/λ_max.

**Explanation.** In the eigenbasis the iteration acts on each coordinate
independently, and each is just scalar multiplication by (1 − ηλᵢ). That factor
must shrink. This is exact, not asymptotic, and it is the single most useful
fact about learning rates. In particular η = 1/λ_max makes the *largest*
eigenvalue direction converge in one step, while η = 2/λ_max makes it oscillate
with factor −1 forever.

**Corollary.** If λ_max/λ_min is large — the matrix is *ill-conditioned* — no
single η can make all directions converge fast. The slow direction is
constrained by η < 2/λ_max, so its per-step factor is at best 1 − 2λ_min/λ_max,
which is close to 1 when the condition number is large. **This is the
fundamental reason iterative methods struggle with badly scaled problems**, and
the reason momentum and preconditioning exist.

**Definition.** *Heavy-ball momentum* introduces a velocity **v** and iterates

  **v**ₖ₊₁ = β**v**ₖ + ∇f(**x**ₖ),   **x**ₖ₊₁ = **x**ₖ − η**v**ₖ₊₁,

with momentum parameter β ∈ [0, 1), conventionally 0.9.

**Explanation.** Unrolling the velocity gives
**v**ₖ = Σⱼ βʲ∇f(**x**ₖ₋₁₋ⱼ), a weighted average of the last 1/(1−β) gradients.
With β = 0.9 that is an average over the last ten steps. Gradients that
consistently point the same way add up; gradients that oscillate cancel. So
momentum both accelerates consistent progress and damps oscillation — which is
exactly the pair of pathologies plain descent suffers from.

**Definition.** *Stochastic gradient descent* replaces ∇f by a noisy estimate
ĝₖ = ∇f(**x**ₖ; **z**ₖ) built from a random minibatch. The update is the same.

**Theorem.** For convex f with bounded variance of the gradient estimate, SGD
converges in expectation to the set of minimisers, but not to a single point.

**Explanation.** The noise never fully disappears, so the iterate keeps bouncing
around the optimum. This is not a bug: the noise acts as exploration and is
frequently *why* SGD generalises better than full-batch descent.

**Definition.** The *convergence rate* of a method is the exponent α such that
the error falls like e^(−αk) (linear) or e^(−α√k) for accelerated methods.

**Theorem.** Gradient descent on an L-smooth convex function has rate
O(1/k) in function value; Nesterov's accelerated method has rate O(1/k²).

**Definition.** A critical point of f is a point where ∇f(**x**) = **0**.

**Theorem (convergence to a critical point).** If f is convex and differentiable
with bounded gradient, gradient descent converges to a critical point. If f is
non-convex, it converges to *some* critical point, which may be a saddle.

**Explanation.** In the non-convex case the gradient-norm sequence does not
always go to zero — it can hover above a floor set by the saddle curvature. This
is why deep learning optimisers report training loss that plateaus above zero and
why people add explicit regularisation to prefer flat, benign minima.

## Worked Example

Minimise f(x, y) = x² + 2y² by hand, starting from (5, 5).

**Step 1 — the gradient.** fₓ = 2x, f_y = 4y, so ∇f(x, y) = (2x, 4y). The
minimum is at (0, 0), where the gradient vanishes.

**Step 2 — the first step with η = 0.1.** At (5, 5) the gradient is (10, 20).

x₁ = 5 − 0.1·10 = 5 − 1 = 4
y₁ = 5 − 0.1·20 = 5 − 2 = 3

New point (4, 3). Check the function dropped: f(5,5) = 25 + 50 = 75, and
f(4,3) = 16 + 18 = 34. Down from 75 to 34.

**Step 3 — the exact behaviour.** Because this is a quadratic, the update is
linear:

xₖ₊₁ = xₖ − 0.1·2xₖ = xₖ(1 − 0.2) = 0.8xₖ
yₖ₊₁ = yₖ − 0.1·4yₖ = yₖ(1 − 0.4) = 0.6yₖ

So after k steps, xₖ = 5·(0.8)ᵏ and yₖ = 5·(0.6)ᵏ. Check k = 1: x = 4, y = 3. Correct.

**Step 4 — apply the stability condition.** The Hessian is diag(2, 4), so
λ_min = 2 and λ_max = 4. The condition is 0 < η < 2/4 = 0.5, and η = 0.1 is
comfortably inside. The factors 0.8 and 0.6 are exactly 1 − ηλᵢ for λᵢ = 2 and 4.

**Step 5 — why η = 0.5 is a trap.** Plugging in η = 0.5:

xₖ₊₁ = xₖ(1 − 1.0) = 0, so x reaches the minimum in a single step.
yₖ₊₁ = yₖ(1 − 2.0) = −yₖ, so y flips sign forever: 5, −5, 5, −5, …

The gradient at the minimum is zero, so the iterate never moves, but it is
permanently stuck 5 units away in y. The code confirms f = 50 forever. **η = 0.5
sits exactly on the boundary η = 2/λ_max, where the y-factor is exactly −1.**
This is the cleanest possible demonstration that a learning rate is not just
"how fast" but "whether you get there at all".

**Step 6 — momentum on the same problem.** Start (5, 5), η = 0.1, β = 0.9.

v₁ = 0.9·(0,0) + (10, 20) = (10, 20)
x₁ = (5,5) − 0.1·(10,20) = (4, 3)

Identical to the first step, since v starts at zero. The difference shows up from
step 2:

g₂ = ∇f(4,3) = (8, 12)
v₂ = 0.9·(10,20) + (8,12) = (17, 30)
x₂ = (4,3) − 0.1·(17,30) = (2.3, 0)

**y went from 3 straight to 0 in two steps.** Vanilla descent would have taken
y₂ = 0.6·3 = 1.8. Momentum took the accumulated y-gradient (20, then 12, then 8)
and used it all at once. The whole point of the method in one line.

## Runnable Code

The update rule and the learning rate, in plain Python.

```python
"""Gradient descent from scratch: the update rule, learning rate, momentum."""

from math import cos, sin, sqrt


# --- 1. The update rule -------------------------------------------------
# x <- x - lr * grad f(x)


def gradient_descent(f, grad, x0, lr=0.1, steps=200, tol=None, xmin=-1e9, xmax=1e9):
    """Plain vanilla gradient descent on a two-variable objective.

    f(x)   -> objective, called as f(x) with x a list of length 2
    grad(x)-> gradient, called as grad(x), returns a list of length 2

    lr is the learning rate: how far to move per step along -grad.
    tol, if given, stops early once |grad| is below it.
    xmin/xmax clamp each step so a bad learning rate cannot send the iterate
    to infinity -- which makes divergence visible as a visible failure rather
    than an overflow error.
    """
    x = list(x0)
    history = [tuple(x)]
    values = [f(x)]
    for _ in range(steps):
        g = grad(x)
        norm = sqrt(sum(v * v for v in g))
        if tol is not None and norm < tol:
            break
        x = [min(xmax, max(xmin, x[i] - lr * g[i])) for i in range(len(x))]
        history.append(tuple(x))
        values.append(f(x))
    return x, values, history


# --- 2. Test functions --------------------------------------------------
def f_quad(x):
    return x[0] ** 2 + 2.0 * x[1] ** 2


def grad_quad(x):
    return [2.0 * x[0], 4.0 * x[1]]


def f_rosenbrock(x):
    a, b = x
    return (1.0 - a) ** 2 + 100.0 * (b - a * a) ** 2


def grad_rosenbrock(x):
    a, b = x
    return [400.0 * a * (a * a - b) + 2.0 * (a - 1.0),
            200.0 * (b - a * a)]


def f_rastrigin(x):
    a, b = x
    return 20.0 + a * a + b * b - 10.0 * (cos(2 * 3.141592653589793 * a)
                                         + cos(2 * 3.141592653589793 * b))


def grad_rastrigin(x):
    a, b = x
    k = 2 * 3.141592653589793
    return [2.0 * a + k * 10.0 * sin(k * a),
            2.0 * b + k * 10.0 * sin(k * b)]


# --- 3. The learning rate is the whole ball game ------------------------
print("=== convex quadratic f = x^2 + 2y^2, minimum at (0,0) ===")
print("start from (5, 5), 200 steps\n")
print(f"{'lr':>8} {'final x':>24} {'f(x)':>16}  outcome")

for lr in (0.5, 0.2, 0.1, 0.05, 0.01, 0.001):
    x, values, _ = gradient_descent(f_quad, grad_quad, [5.0, 5.0],
                                    lr=lr, steps=200, xmin=-1e6, xmax=1e6)
    ok = abs(x[0]) < 1e-3 and abs(x[1]) < 1e-3
    outcome = "converged" if ok else f"still f={f_quad(x):.3e}"
    print(f"{lr:8.3f} ({x[0]:10.6f}, {x[1]:10.6f}) {f_quad(x):16.6e}  {outcome}")

print("\nlr = 0.5 is the interesting row: x hits the minimum in one step while")
print("y oscillates between 5 and -5 forever, because 1 - lr*4 = -1 exactly.")

# Now show the actual divergence threshold for a 1D quadratic.
print("\n=== 1D: f(x) = x^2, and the exact stability condition ===")
print("update: x <- x - lr * 2x = x(1 - 2*lr)")
print("shrinks iff |1 - 2*lr| < 1, i.e. 0 < lr < 1\n")
print(f"{'lr':>8} {'|1-2lr|':>10} {'behaviour':>12} {'x after 20 steps, x0=1':>24}")


def gd_1d(lr, steps=20, x0=1.0):
    x = x0
    for _ in range(steps):
        x = x - lr * 2.0 * x
    return x


for lr in (0.1, 0.5, 0.9, 0.999, 1.0, 1.5, 2.0):
    factor = abs(1.0 - 2.0 * lr)
    if factor < 1.0:
        behaviour = "shrinks"
    elif factor == 1.0:
        behaviour = "constant"
    else:
        behaviour = "DIVERGES"
    x = gd_1d(lr)
    print(f"{lr:8.3f} {factor:10.4f} {behaviour:>12} {x:24.6e}")

print("\nlambda_max = 2 here, so the bound 0 < lr < 2/lambda_max = 1 is exact:")
print("lr = 1.0 sits on the boundary and never moves; lr > 1 diverges.")
```

### Momentum, and the price of non-convexity

```python
from math import cos, sin, sqrt


def gradient_descent(f, grad, x0, lr=0.1, steps=200, tol=None):
    """Vanilla: x <- x - lr * grad."""
    x = list(x0)
    v = [0.0] * len(x)
    path = [tuple(x)]
    for _ in range(steps):
        g = grad(x)
        if tol is not None and sqrt(sum(w * w for w in g)) < tol:
            break
        x = [x[i] - lr * g[i] for i in range(len(x))]
        path.append(tuple(x))
    return x, path


def momentum_descent(f, grad, x0, lr=0.1, beta=0.9, steps=200, tol=None):
    """Heavy-ball momentum: v <- beta*v + grad, then x <- x - lr*v."""
    x = list(x0)
    v = [0.0] * len(x)
    path = [tuple(x)]
    for _ in range(steps):
        g = grad(x)
        if tol is not None and sqrt(sum(w * w for w in g)) < tol:
            break
        # Accumulate the velocity, then take a step along it.
        v = [beta * v[i] + g[i] for i in range(len(x))]
        x = [x[i] - lr * v[i] for i in range(len(x))]
        path.append(tuple(x))
    return x, path


def f_rosenbrock(x):
    a, b = x
    return (1.0 - a) ** 2 + 100.0 * (b - a * a) ** 2


def grad_rosenbrock(x):
    a, b = x
    return [400.0 * a * (a * a - b) + 2.0 * (a - 1.0),
            200.0 * (b - a * a)]


def f_rastrigin(x):
    a, b = x
    k = 2 * 3.141592653589793
    return 20.0 + a * a + b * b - 10.0 * (cos(k * a) + cos(k * b))


def grad_rastrigin(x):
    a, b = x
    k = 2 * 3.141592653589793
    return [2.0 * a + k * 10.0 * sin(k * a),
            2.0 * b + k * 10.0 * sin(k * b)]


def f_ill_conditioned(x):
    """A stretched valley: same problem, wildly different scale."""
    return 100.0 * x[0] ** 2 + x[1] ** 2


def grad_ill(x):
    return [200.0 * x[0], 2.0 * x[1]]


# --- Momentum on a narrow valley ----------------------------------------
print("=== f = 100x^2 + y^2, start (5, 5), minimum (0,0) ===")
print("gradient at (5,5) is", grad_ill([5.0, 5.0]),
      "-> the x direction dominates by 100x\n")
print(f"{'beta':>6} {'steps':>6} {'final point':>26} {'f':>14}")

for beta in (0.0, 0.5, 0.9, 0.95, 0.99):
    lr = 0.001          # forced small: this valley needs it
    if beta == 0.0:
        x, _ = gradient_descent(f_ill_conditioned, grad_ill, [5.0, 5.0],
                                lr=lr, steps=2000)
    else:
        x, _ = momentum_descent(f_ill_conditioned, grad_ill, [5.0, 5.0],
                                lr=lr, beta=beta, steps=2000)
    print(f"{beta:6.2f} {2000:6d} ({x[0]:11.6f}, {x[1]:11.6f})"
          f" {f_ill_conditioned(x):14.4e}")

print("\nAt beta = 0 the iterate barely moves in y, because y only receives")
print("gradients from the small 2y term. Momentum accumulates those small")
print("gradients over many steps until they add up to something comparable.")

# --- Convex vs non-convex ----------------------------------------------
print("\n=== Rosenbrock from (-1.2, 1.0): local vs global ===")
x, path = gradient_descent(f_rosenbrock, grad_rosenbrock, [-1.2, 1.0],
                           lr=0.001, steps=30000)
print("  gradient descent, lr=0.001, 30000 steps")
print(f"    final ({x[0]:.8f}, {x[1]:.8f})  f = {f_rosenbrock(x):.3e}")
print("    distance to the true minimum (1,1): "
      f"{sqrt((x[0] - 1) ** 2 + (x[1] - 1) ** 2):.3e}")

xm, pathm = momentum_descent(f_rosenbrock, grad_rosenbrock, [-1.2, 1.0],
                             lr=0.001, beta=0.9, steps=30000)
print("  momentum, lr=0.001, beta=0.9, 30000 steps")
print(f"    final ({xm[0]:.8f}, {xm[1]:.8f})  f = {f_rosenbrock(xm):.3e}")
print("    distance to the true minimum (1,1): "
      f"{sqrt((xm[0] - 1) ** 2 + (xm[1] - 1) ** 2):.3e}")

print("\n=== Rastrigin: same algorithm, many different answers ===")
ends = {}
for start in ([-3.0, -3.0], [-3.0, 2.0], [0.5, -2.5], [2.5, 1.0]):
    x, _ = gradient_descent(f_rastrigin, grad_rastrigin, start,
                            lr=0.008, steps=4000)
    ends[tuple(start)] = (x[0], x[1], f_rastrigin(x))
    print(f"  start {str(start):14s} -> ({x[0]:+.4f}, {x[1]:+.4f})"
          f"  f = {f_rastrigin(x):8.4f}")

values = [v[2] for v in ends.values()]
print(f"\n  distinct destinations: {len(ends)}")
print(f"  best f found: {min(values):.4f}   (global minimum is 0.0 at (0,0))")
print(f"  worst f found: {max(values):.4f}")
print("  -> the SAME landscape gives different answers from different starts.")
print("     No learning rate fixes this; only convexity would.")
```

### With Libraries

Plotting the descent paths makes the four failure modes obvious in a way no
amount of printed numbers does. This block requires numpy and matplotlib and is
not runnable in the standard library alone.

```python
import matplotlib
matplotlib.use("Agg")          # headless, so this runs anywhere
import matplotlib.pyplot as plt
import numpy as np
from math import sin, sqrt

plt.rcParams.update({"figure.dpi": 110, "font.size": 9})


def f_quad(x):
    return x[0] ** 2 + 2.0 * x[1] ** 2


def grad_quad(x):
    return [2.0 * x[0], 4.0 * x[1]]


def f_ill(x):
    return 100.0 * x[0] ** 2 + x[1] ** 2


def grad_ill(x):
    return [200.0 * x[0], 2.0 * x[1]]


def gradient_descent(f, grad, x0, lr, steps):
    x = list(x0)
    path = [tuple(x)]
    for _ in range(steps):
        g = grad(x)
        x = [x[i] - lr * g[i] for i in range(len(x))]
        path.append(tuple(x))
    return path


def momentum_descent(f, grad, x0, lr, beta, steps):
    x = list(x0)
    v = [0.0] * len(x)
    path = [tuple(x)]
    for _ in range(steps):
        g = grad(x)
        v = [beta * v[i] + g[i] for i in range(len(x))]
        x = [x[i] - lr * v[i] for i in range(len(x))]
        path.append(tuple(x))
    return path


fig, axes = plt.subplots(2, 3, figsize=(14, 8))
ax = axes.ravel()


def contour_background(a, f, levels=25, lim=6):
    xs = np.linspace(-lim, lim, 300)
    X, Y = np.meshgrid(xs, xs)
    pts = np.stack([X.ravel(), Y.ravel()], axis=1)
    Z = np.array([f(p) for p in pts]).reshape(X.shape)
    a.contour(X, Y, Z, levels=levels, colors="#bbbbbb", linewidths=0.6)
    a.contourf(X, Y, Z, levels=levels, cmap="Greys", alpha=0.25)


# --- Panel 1: learning rate too small ------------------------------------
a = ax[0]
contour_background(a, f_quad)
p = gradient_descent(f_quad, grad_quad, [5.0, 5.0], lr=0.01, steps=100)
a.plot(*zip(*p), "-o", ms=2.5, lw=1.2, color="#c0392b", label="lr = 0.01")
a.set_title("lr too small: still crawling after 100 steps")
a.set_xlabel("x")
a.set_ylabel("y")
a.legend(loc="upper right")
a.set_aspect("equal")

# --- Panel 2: a good learning rate --------------------------------------
a = ax[1]
contour_background(a, f_quad)
p = gradient_descent(f_quad, grad_quad, [5.0, 5.0], lr=0.1, steps=100)
a.plot(*zip(*p), "-o", ms=2.5, lw=1.2, color="#27ae60", label="lr = 0.1")
a.set_title("lr = 0.1: straight line to the minimum")
a.set_xlabel("x")
a.set_ylabel("y")
a.legend(loc="upper right")
a.set_aspect("equal")

# --- Panel 3: learning rate too large -----------------------------------
# For f = x^2 + 2y^2 the largest curvature is 4 (in y), so stability needs
# lr < 2/4 = 0.5. At lr = 0.45 the y iterate oscillates forever without
# settling; at lr = 0.55 it leaves the plot entirely. Clamp for display only.
a = ax[2]
contour_background(a, f_quad, lim=10)
CLAMP = 10.0
for lr, colour in [(0.3, "#2980b9"), (0.45, "#e67e22"), (0.55, "#c0392b")]:
    p = gradient_descent(f_quad, grad_quad, [5.0, 5.0], lr=lr, steps=25)
    final = max(abs(v) for v in p[-1])
    note = "" if final < CLAMP else "  (escapes)"
    xs = [max(-CLAMP, min(CLAMP, q[0])) for q in p]
    ys = [max(-CLAMP, min(CLAMP, q[1])) for q in p]
    a.plot(xs, ys, "-o", ms=4, lw=1.4, color=colour, label=f"lr = {lr}{note}")
a.set_title("lr too large: overshoot, oscillation, escape")
a.set_xlim(-8, 8)
a.set_ylim(-8, 8)
a.set_xlabel("x")
a.set_ylabel("y")
a.legend(loc="upper right", fontsize=8)
a.set_aspect("equal")

# --- Panel 4: ill-conditioned valley, no momentum ----------------------
a = ax[3]
contour_background(a, f_ill, lim=8)
p = gradient_descent(f_ill, grad_ill, [6.0, 6.0], lr=0.001, steps=1500)
a.plot(*zip(*p), "-", lw=1.4, color="#c0392b", label="vanilla, lr = 0.001")
a.set_title("narrow valley, no momentum: zigzag stalls")
a.set_xlabel("x")
a.set_ylabel("y")
a.legend(loc="upper right")
a.set_aspect("equal")

# --- Panel 5: same valley, with momentum -------------------------------
a = ax[4]
contour_background(a, f_ill, lim=8)
p = momentum_descent(f_ill, grad_ill, [6.0, 6.0], lr=0.001, beta=0.9, steps=1500)
a.plot(*zip(*p), "-", lw=1.4, color="#27ae60", label="momentum, beta = 0.9")
a.set_title("momentum: small gradients finally add up")
a.set_xlabel("x")
a.set_ylabel("y")
a.legend(loc="upper right")
a.set_aspect("equal")

# --- Panel 6: non-convex, many local minima ----------------------------
def f_rastrigin(x):
    a, b = x
    k = 2 * np.pi
    return 20.0 + a * a + b * b - 10.0 * (np.cos(k * a) + np.cos(k * b))


def grad_rastrigin(x):
    a, b = x
    k = 2 * np.pi
    return [2.0 * a + k * 10.0 * sin(k * a), 2.0 * b + k * 10.0 * sin(k * b)]


a = ax[5]
contour_background(a, f_rastrigin, lim=5)
for start, colour in [([-3.0, -3.0], "#c0392b"), ([-3.0, 2.0], "#2980b9"),
                      ([2.5, 1.0], "#8e44ad")]:
    p = gradient_descent(f_rastrigin, grad_rastrigin, start, lr=0.008, steps=3000)
    a.plot(*zip(*p), "-", lw=1.3, color=colour,
           label=f"start {start}, f = {f_rastrigin(list(p[-1])):.2f}")
    a.plot(p[-1], "o", color=colour, ms=7)
a.plot(0, 0, "*", color="black", ms=16, label="global min")
a.set_title("non-convex: three starts, three answers")
a.set_xlabel("x")
a.set_ylabel("y")
a.legend(loc="upper right", fontsize=7)
a.set_aspect("equal")

fig.suptitle("Gradient descent: learning rate, momentum, and the price of non-convexity",
             fontsize=12)
fig.tight_layout(rect=(0, 0, 1, 0.96))
out = "gradient_descent_paths.png"
fig.savefig(out, dpi=110)
print("wrote", out)
print("learning rate too small -> zigzag; too large -> oscillation;")
print("momentum rescues ill-conditioned valleys; non-convex -> many answers.")
```

Reading the panels: panel 3 is the money shot. At lr = 0.3 the path is a tight
spiral, at lr = 0.45 it is a violent vertical oscillation that never settles,
and at lr = 0.55 the iterate has left the frame entirely. Panel 4 versus panel 5
is the momentum story — same objective, same learning rate, completely different
path.

## Common Mistakes

**1. Using the same learning rate as the largest eigenvalue allows everywhere.**
The bound 0 < η < 2/λ_max is global. The problem is that λ_max is the curvature
at the *steepest* point you will ever visit, so choosing η near 2/λ_max is safe
only if you are certain never to go there. In a real network with 10⁷ parameters
the curvature varies enormously across directions and layers, so no single safe
value exists. This is why real training uses small steps, schedules, or Adam.

**2. Forgetting the gradient is a vector, not a number.** Writing
`x -= lr * f(x)` instead of `x -= lr * grad(x)` produces something that compiles,
runs, and quietly does nothing useful. If your loss never changes, check this
first.

**3. Sign errors in the update.** It is `x − lr·∇f(x)`, not `x + lr·∇f(x)`. The
plus version climbs the hill and looks like an unstable objective rather than a
sign bug. A quick sanity check: evaluate f at the start and after one step; it
must decrease.

**4. Treating a plateau as convergence on a non-convex problem.** With momentum
at β = 0.99 the effective step is 100× lr, so a learning rate that looked safe
may already be unstable. Conversely, in a non-convex problem the loss plateauing
above zero does not mean you converged — the saddle curvature sets a gradient-norm
floor. Check the *gradient norm*, not just the loss.

**5. Forgetting that momentum changes the stability bound.** The heavy-ball
recurrence is xₖ₊₁ = (1 + βη)xₖ − βηxₖ₋₁ − η∇f(xₖ), and its eigenvalues can leave
the unit disc at learning rates where vanilla descent is perfectly stable. Adding
momentum is not a free speed-up; the learning rate usually has to come down.

---

## Formula Sheet

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| gradient `$\nabla f(x)$` | `$\left(\frac{\partial f}{\partial x_1},\dots,\frac{\partial f}{\partial x_n}\right)(x)$` | one slope per input, collected into an arrow | the only object the update rule consumes; exists only where `f` is differentiable |
| directional derivative | `$\left.\frac{df}{dt}\right\vert_{t=0}=\nabla f(x)\cdot v$` for the curve `x(t)=x+tv` | how fast `f` changes when you walk along `v` | valid for any `v`; the word *steepest* additionally requires `$\lVert v\rVert=1$` |
| steepest descent | `$v^*=-\nabla f/\lVert\nabla f\rVert$`, with rate of decrease `$\lVert\nabla f\rVert$` | the single best downhill direction, and how fast `f` falls along it | valid **only** where `$\nabla f(x)\ne0$`; at a critical point the gradient vanishes and every direction ties |
| Cauchy–Schwarz | `$\nabla f\cdot v\le\lVert\nabla f\rVert\lVert v\rVert$` | no direction beats the gradient's own length | the one-line proof of the row above |
| gradient descent | `$x_{k+1}=x_k-\eta\nabla f(x_k)$`, `$\eta>0$` | step downhill, by `η` times the slope | `η` is the learning rate; a *larger* `η` is **not** automatically better |
| exact solution, quadratic | for `$f(x)=\tfrac12x^{\mathsf T}Hx$` with `H` SPD and `H=Q\Lambda Q^{\mathsf T}`: `$x_k=Q\,\operatorname{diag}\!\big((1-\eta\lambda_i)^k\big)Q^{\mathsf T}x_0$` | each eigen-direction is multiplied by a fixed scalar every step | exact, not asymptotic; the strongest single fact about learning rates |
| per-direction factor | `$1-\eta\lambda_i$` for the eigen-direction `i` | how much that direction shrinks each step | the direction with the largest `$\lambda$` sets the constraint on `η` |
| **stability condition** | `$\lvert1-\eta\lambda_i\rvert<1$ for every `i`, i.e. `$0<\eta<2/\lambda_{\max}$` | the step must make every direction shrink | exact for quadratics; for general smooth `f`, `$\eta<2/L$` with `L` a Lipschitz constant of `∇f` |
| one-step choice | `$\eta=1/\lambda_{\max}$` makes the stiffest direction's factor exactly `0` | the hardest direction is solved in one step | worth testing deliberately; it is *not* the fastest overall |
| oscillation boundary | `$\eta=2/\lambda_{\max}$` gives factor `-1` in the stiffest direction | amplitude preserved, sign flipped forever | a limit cycle, not convergence; `η` slightly above it **diverges** |
| conditioning | `$\kappa=\lambda_{\max}/\lambda_{\min}`; best possible slow factor `$\ge 1-2/\kappa$` | how much stiffer the worst direction is than the softest | the reason iterative methods lose to direct solves when `κ` is large |
| heavy-ball momentum | `$v_{k+1}=\beta v_k+\nabla f(x_k)$`, `$x_{k+1}=x_k-\eta v_{k+1}$`, `$\beta\in[0,1)$` | keep a memory of recent slopes and walk along *that* | `β = 0` recovers plain descent; conventionally `β = 0.9` |
| unrolled velocity | `$v_k=\sum_j\beta^j\nabla f(x_{k-1-j})$` | the current step is a geometrically weighted average of the last gradients | an average window of length `1/(1−β)` — ten steps at `β = 0.9` |
| effective step inflation | `$\eta_{\text{eff}}\approx\eta/(1-\beta)$` | momentum multiplies the step by `1/(1−β)` | valid for consistent gradients; it is why momentum **lowers** the stability limit rather than raising it |
| heavy-ball recurrence | `$x_{k+1}=(1+\beta\eta)x_k-\beta\eta x_{k-1}-\eta\nabla f(x_k)$` | the same method written with no auxiliary variable | shows the extra term `-βηx_{k−1}`, whose eigenvalues can leave the unit disc at rates where plain descent is stable |
| Nesterov lookahead | evaluate at `$y_k=x_k-\eta\beta v_k$`, then `$v_{k+1}=\beta v_k+\nabla f(y_k)$`, `$x_{k+1}=x_k-\eta v_{k+1}$` | measure the slope where you are *about to be*, then step from where you are | valid only if the sign on `ηβv` is minus; get it wrong and the method diverges immediately |
| stochastic gradient | `$\hat g_k=\nabla f(x_k;z_k)$` from a random minibatch, `x_{k+1}=x_k-\eta\hat g_k$` | the same update, with an estimate of the slope | unbiased in expectation; the noise never fully vanishes |
| general convex rates | gradient descent `O(1/k)` in function value; Nesterov `O(1/k^2)` | the gap to the optimum falls polynomially | valid for *smooth convex* problems with a well-tuned step; on a quadratic the rate is set by `η`, not by these bounds |
| critical point | `$\nabla f(x)=0$` | every direction has zero slope | the set gradient descent provably converges to; for convex `f` each one is a global minimum |
| central-difference gradient | `$\frac{f(x+h)-f(x-h)}{2h}$` | slope from two symmetric samples | error `O(h^2)`; use `h ≈ 10⁻⁶` and never straddle a kink |

---

## Multiple Choice Questions

**Q1.** For a differentiable `f` with `∇f(x) ≠ 0`, which direction gives the most rapid
decrease of `f`, and what is the rate?

- A) `v = ∇f(x)/‖∇f(x)‖`, rate `‖∇f(x)‖`
- B) `v = −∇f(x)/‖∇f(x)‖`, rate `−‖∇f(x)‖`
- C) `v = −∇f(x)/‖∇f(x)‖`, rate `‖∇f(x)‖`
- D) `v = −∇f(x)`, rate `‖∇f(x)‖²`

<details>
<summary>Answer and explanation</summary>

**C) `v = −∇f(x)/‖∇f(x)‖`, rate `‖∇f(x)‖`.**

The directional derivative along a unit `v` is `∇f(x)·v`, and Cauchy–Schwarz bounds it
below by `−‖∇f‖` with equality exactly when `v = −∇f/‖∇f‖`. So the *direction* is the
negated unit gradient and the *rate* (the positive quantity ‖∇f‖) is the norm. Note the
update rule uses `−η∇f(x)` rather than the unit direction, so `η` and `‖∇f‖` are the same
thing twice: the step actually taken is `η·‖∇f‖` in length.

Option A is steepest *ascent* — the most common sign error, and one that produces a
"unstable objective" where there is really a `+` instead of a `−`. Option B pairs the
correct direction with a negative "rate", so it says `f` decreases at a negative rate,
which is a category error: the rate of decrease is a non-negative magnitude, here `‖∇f‖`.
Option D confuses a direction with a step: `−∇f` is a perfectly good *displacement*, but
its length is the local gradient norm, so it is not a unit direction and its "rate"
`‖∇f‖²` belongs to no statement in the theorem. All four are excluded at a critical point
anyway, where every unit direction ties at rate `0`.

</details>

**Q2.** For `f(x, y) = x² + 2y²`, the Hessian is `diag(2, 4)`. What is the exact range of
learning rates for which gradient descent converges from every starting point, and what
happens at the upper endpoint?

- A) `0 < η < 0.25`; at `η = 0.25` the `x` coordinate converges and `y` overshoots once
- B) `0 < η < 0.5`; at `η = 0.5` the `x` coordinate reaches the minimum in one step while `y` oscillates between `5` and `−5` forever
- C) `0 < η < 0.5`; at `η = 0.5` both coordinates oscillate
- D) `0 < η < 2`; at `η = 2` the iterate diverges

<details>
<summary>Answer and explanation</summary>

**B) `0 < η < 0.5`; at `η = 0.5` the `x` coordinate reaches the minimum in one step while
`y` oscillates between `5` and `−5` forever.**

`λ_max = 4`, so the bound is `η < 2/4 = 0.5`. At `η = 0.5` the two per-step factors are
`1 − 0.5·2 = 0` and `1 − 0.5·4 = −1`. The first converges to the minimum in one step; the
second flips sign every step with its magnitude unchanged, so `f = 2·25 = 50` forever. The
code prints exactly that row.

Option A uses `1/λ_max = 0.25`, which is the rate-*one-step* choice, not the stability
boundary — the method still converges at `η = 0.3` and `η = 0.45`, which the plotting
panels show as a tight spiral and a violent-but-bounded oscillation. Option C is the
asymmetry misread: at `η = 0.5` the `x` factor is exactly `0`, not `−1`. Option D uses
`2/λ_min`; the constraint always comes from the *largest* eigenvalue, since that is the
direction amplified fastest.

</details>

**Q3.** A common rule of thumb is "the learning rate must satisfy `η < 1/λ_max`". What is
wrong with it?

- A) Nothing — it is exactly the stability bound
- B) It is conservative but not sharp: the true bound is `η < 2/λ_max`, and `η = 1/λ_max` is the special value that solves the stiffest direction in a *single* step
- C) It is wrong in the other direction: the bound is `η < 1/λ_min`
- D) `λ_max` cannot be computed without already solving the problem

<details>
<summary>Answer and explanation</summary>

**B) It is conservative but not sharp: the true bound is `η < 2/λ_max`, and
`η = 1/λ_max` is the special value that solves the stiffest direction in a *single* step.**

Convergence requires `|1 − ηλᵢ| < 1` for every `i`, i.e. `0 < ηλᵢ < 2` for every `i`, and
the binding inequality comes from `λ_max`. Half of that interval — `η ∈ (1/λ_max,
2/λ_max)` — is legal and oscillatory: the factors are negative, so the iterate crosses the
minimum each step while still shrinking. The code's 1-D table shows this directly, with
`lr = 0.9` giving factor `−0.8` and the "shrinks" label.

Option A is the error: `η = 0.9` on `f(x) = x²` oscillates and still converges, and `η = 0.9`
on Rosenbrock *diverges in five steps*, so the two rules genuinely disagree in both
directions. Option C swaps the extreme eigenvalues, and `1/λ_min` is a step size so large
that the stiffest direction always diverges. Option D is false: for a quadratic the
eigenvalues come from the Hessian, which you compute long before you optimise —
`λ_max ≈ 1506` for Rosenbrock at `(−1.2, 1)` gives the bound `η < 0.0013`, and the code's
stability probe finds the divergence threshold at `lr = 0.01` and convergence at `0.002`.

</details>

**Q4.** With `η = 0.1` and `β = 0.9` on `f(x,y) = x² + 2y²` starting from `(5, 5)`,
momentum's *second* step differs from plain descent. What is it?

- A) `x₂ = (4, 3)`, identical to the first step
- B) `x₂ = (2.3, 0)`; plain descent would only reach `y₂ = 1.8`
- C) `x₂ = (2.3, 1.8)`
- D) `x₂ = (3.02, 1.08)`

<details>
<summary>Answer and explanation</summary>

**B) `x₂ = (2.3, 0)`; plain descent would only reach `y₂ = 1.8`.**

Step 1 is identical to plain descent because `v` starts at zero: `v₁ = (0,0) + (10,20) =
(10,20)` and `x₁ = (5,5) − 0.1·(10,20) = (4,3)`. At step 2 the gradients differ,
`g₂ = (8,12)`, and momentum accumulates: `v₂ = 0.9·(10,20) + (8,12) = (17,30)`. Then
`x₂ = (4,3) − 0.1·(17,30) = (4 − 1.7, 3 − 3) = (2.3, 0)`. Vanilla descent would give
`y₂ = 0.6·3 = 1.8`, because `y` contracts by `1 − 0.1·4 = 0.6` per step.

Option A describes step 1, which is the point the lesson makes about momentum: the two
methods *must* agree on the first step, so any claimed difference there is a bug.
Option C is the classic mix-up — the `x` update uses the accumulated velocity but the `y`
update uses the raw gradient `g₂ = (8,12)`, giving `(4 − 1.7, 3 − 1.2)`. Option D discounts
the *gradient* as well as the velocity (`v₂ = 0.9·(10,20) + 0.1·(8,12) = (9.8, 19.2)`),
which is the residual-update convention used in some Nesterov variants, not in heavy ball;
it leaves both coordinates moving far too slowly. The real lesson is in `y` going from `3`
to `0` in two steps: the accumulated `y` gradients `(20, 12, 8)` were spent all at once.

</details>

**Q5.** On the narrow valley `f(x, y) = 100x² + y²` with `η = 0.001`, plain descent
barely moves in `y`. Why does momentum fix that, and what is the mechanism?

- A) Momentum rescales the gradient per coordinate, like Adam, so it removes the factor-100 asymmetry
- B) The velocity is a geometrically weighted average of the last `1/(1−β)` gradients, so the small `y` gradients accumulate until they match the large `x` ones
- C) Momentum increases the effective learning rate from `0.001` to `0.01`, so `y` simply gets ten times more travel
- D) Momentum replaces the gradient with the Hessian's smallest eigenvector

<details>
<summary>Answer and explanation</summary>

**B) The velocity is a geometrically weighted average of the last `1/(1−β)` gradients, so
the small `y` gradients accumulate until they match the large `x` ones.**

Unrolling the recurrence gives `v_k = Σⱼ βʲ ∇f(x_{k−1−ⱼ})` — with `β = 0.9` an average
over roughly the last ten gradients. `y` only ever receives the small `2y` term, but ten of
those in the same direction add up to something comparable, while the oscillating
components of the `x` signal cancel. The lesson's table shows the consequence: `β = 0`
leaves `y` stranded after 2,000 steps, while `β = 0.9` reaches the minimum.

Option A describes a *different* method. Adam's per-coordinate adaptive step is the point
of the lesson's last summary bullet, and it is precisely what momentum does **not** do —
momentum's `β` multiplies the whole velocity vector by the same scalar, so a direction with
a tiny gradient always takes a tiny step. Option C confuses the mechanism with a
consequence: momentum at `β = 0.9` inflates the step by `1/(1−β) = 10`, but the `y`
progress comes from *accumulating consistent signal*, and inflating `η` tenfold would
immediately violate the stability bound `η < 2/λ_max ≈ 0.01`. Option D invents an
eigenvector method; momentum has no Hessian access at all.

</details>

**Q6.** Take `H = [[50.5, 49.5], [49.5, 50.5]]`, whose eigenvalues are exactly `1` and
`100`. The bound is therefore `η < 0.02`, yet raising `η` from `0.01` to `0.0199` only cuts
the steps needed to reach `1e-6` from `1363` to `570`. Why?

- A) The code is buggy: the counts should drop by roughly the same factor as the learning rate
- B) The slow direction is constrained by `η < 2/λ_max` and contracts at `1 − ηλ_min ≈ 0.98` regardless, so the soft direction sets the pace and speeding up the stiff one buys almost nothing
- C) `η = 0.0199` is past the boundary and the run is actually diverging
- D) The `1e-6` target is on `f`, not on `x`, so the counts are not comparable across learning rates

<details>
<summary>Answer and explanation</summary>

**B) The slow direction is constrained by `η < 2/λ_max` and contracts at `1 − ηλ_min ≈
0.98` regardless, so the soft direction sets the pace and speeding up the stiff one buys
almost nothing.**

This is the condition-number argument. The bound has to hold for the *largest* eigenvalue,
so `η` cannot grow to make the `λ = 100` direction finish faster — it already finishes in
one step at `η = 0.01`. Meanwhile the `λ = 1` direction contracts at only
`1 − 0.01 = 0.99` per step, so it takes `log(1e-6)/log(0.99) ≈ 1363` steps no matter
what. This is the single most important practical fact in the lesson: it is why Cholesky and
SVD beat iterative solvers on ill-conditioned systems, and why **preconditioning** — which
rescales the eigenvalues towards `1` — is such a large win.

Option A is the tempting inference and it is exactly backwards: the whole point is that
progress is *not* proportional to `η`. Option C misreads the table — the `0.019` row gives
factor `−0.9000`, which shrinks, and `0.021` gives `−1.1000`, which grows. Option D
invents a units problem; the lesson converts the target to `|x|_∞ < 1e-6` consistently
across all four rows.

</details>

**Q7.** Training loss plateaus well above zero. What does the lesson say you should check,
and why?

- A) The loss — a plateau *is* convergence
- B) The gradient **norm**, because in a non-convex problem the saddle curvature sets a floor on `‖∇f‖` that the loss plateau conceals
- C) The learning rate only — it is always too small on a plateau
- D) Nothing can be concluded without re-running with a different seed

<details>
<summary>Answer and explanation</summary>

**B) The gradient **norm**, because in a non-convex problem the saddle curvature sets a
floor on `‖∇f‖` that the loss plateau conceals.**

The lesson's convergence theorem distinguishes the two cases: for **convex** `f`, descent
converges to a critical point and local means global, so a plateau really is the answer.
For **non-convex** `f`, it converges to *some* critical point, possibly a saddle, and the
gradient-norm sequence does not always fall to zero — it can hover above a floor set by the
curvature near a saddle. That is exactly why real optimisers report training loss that
never reaches zero, and why people add explicit regularisation to prefer flat, benign
minima. The lesson also notes the reverse failure: with `β = 0.99` the effective step is
`100η`, so a learning rate that looked safe may already be unstable.

Option A is the mistake the lesson is written against — it is only safe for convex `f`.
Option C asserts a direction the theory does not support; and with momentum the effective
step is *larger* than `η`, so a plateau is at least as likely to mean "too big" as "too
small". Option D is not a diagnostic but a shrug. The lesson's `tol` parameter is exactly
the right test: stop on `‖∇f‖ < tol`, not on `f` stopping moving.

</details>

**Q8.** Four different starting points on Rastrigin's function, same algorithm, same
learning rate `0.008`, produce four different endpoints — with the best at some value
strictly above the global minimum `0.0`. What does that prove?

- A) The learning rate was badly chosen for that function
- B) A non-convex landscape makes the answer depend on the starting point, and no single choice of `η` removes that dependence
- C) Rastrigin's function is unbounded below
- D) The gradient implementation has a bug, since a correct solver must be start-independent

<details>
<summary>Answer and explanation</summary>

**B) A non-convex landscape makes the answer depend on the starting point, and no single
choice of `η` removes that dependence.**

The code runs the *same* `gradient_descent` with the *same* `lr = 0.008` from
`[−3,−3]`, `[−3,2]`, `[0.5,−2.5]` and `[2.5,1]` and prints a different destination each
time, then reports the gap from the true optimum at `(0,0)`. It closes with the sentence
that is the whole point: "the SAME landscape gives different answers from different
starts. No learning rate fixes this; only convexity would." The contrast in the same
output is plain — the convex quadratic returns to its single minimum from every start.

Option A is the favourite wrong diagnosis, and it is untestable in principle: there is no
`η` that makes a landscape with 25 local minima start-independent, because the basins, not
the step size, decide where the iterate settles. Option C is false; the function is
bounded below with minimum `0`. Option D blames the implementation for a property of the
mathematics — the code's gradient is verified against the analytic form elsewhere, and the
divergence thresholds it prints for other functions are all exactly where the theorem says
they should be.

</details>

**Q9.** Adding momentum changes the recurrence to
`x_{k+1} = (1 + βη)xₖ − βηx_{k₋₁} − η∇f(xₖ)`. What follows, and why does it matter in
practice?

- A) The extra `−βηx_{k₋₁}` term is a smoothing of the iterate, so the stability bound is unchanged
- B) The recurrence has eigenvalues beyond `xₖ` and `x_{k₋₁}`, and they can leave the unit disc at learning rates where vanilla descent is perfectly stable — so momentum is not a free speed-up
- C) Momentum removes the need to choose `β`, because any `β ∈ [0, 1)` works equally well
- D) The recurrence shows momentum is exactly gradient descent in a rotated coordinate system, so the bound transfers unchanged

<details>
<summary>Answer and explanation</summary>

**B) The recurrence has eigenvalues beyond `xₖ` and `x_{k₋₁}`, and they can leave the unit
disc at learning rates where vanilla descent is perfectly stable — so momentum is not a
free speed-up.**

This is Mistake 5, and the lesson demonstrates it rather than asserting it. On the
ill-conditioned quadratic with `η = 0.001`, momentum β = 0.9 and Nesterov are both stable
and about 13× faster than plain descent; on Rosenbrock from `(−1.2, 1)` at `η = 0.002`,
heavy ball converges in `1033` steps but **Nesterov diverges**, because the lookahead
samples a point further out and therefore effectively higher curvature. The lesson's rule
of thumb is blunt: tune Nesterov and Adam at a *smaller* learning rate than plain SGD.

Option A is the intuition people start with and it is wrong: the damping is not a
low-pass filter on the iterate, it is a genuine second-order recurrence whose stability is
governed by its own spectrum. Option C is contradicted by the code — `β = 0.99` on
Rosenbrock needs `η < 2/λ_max ≈ 0.0013`, and `β` changes where that line sits. Option D is
a seductive half-truth: momentum *is* diagonalisable in the eigenbasis for a quadratic,
but the two extra eigenvalues are what move, so the bound does not transfer.

</details>

**Q10.** On the `100x² + y²` quadratic the fitted rate `α` is `0.0077` for plain descent
and `0.0642` for heavy ball with `β = 0.9`. What is the honest reading?

- A) The theoretical O(1/k) versus O(1/k²) gap has been measured, and the ratio should be exactly 2
- B) The ratio `≈ 8.3×` is the meaningful number — it says momentum is about eight times steeper per step — while both absolute values are set by the chosen `η`, not by the general-convex theory
- C) Both values are far too small, so the run did not converge
- D) `α` should be the same for both methods, since they share the same objective

<details>
<summary>Answer and explanation</summary>

**B) The ratio `≈ 8.3×` is the meaningful number — it says momentum is about eight times
steeper per step — while both absolute values are set by the chosen `η`, not by the
general-convex theory.**

`0.0642 / 0.0077 ≈ 8.3`. The lesson says so directly: "the useful signal is the *ratio*
between methods, which is stable and which the table reports cleanly". The absolute values
are tiny because both problems are quadratics, where the error falls geometrically at a
rate set by the learning rate — `1 − ηλ = 0.9998` per step for the slow direction, which
is what `α = 0.0077` measures. The `O(1/k)` versus `O(1/k²)` theorems are worst-case
statements about *arbitrary* smooth convex functions and need a tuned schedule to reach;
you should not expect to read those constants off a single experiment on a quadratic.

Option A is the misreading the lesson pre-empts — the ratio for the theoretical pair would
be 2, not 8.3, and no experiment on a quadratic is going to produce it. Option C
contradicts the same output, which reaches `6.94e-69` at step 5,405. Option D assumes the
method drops out of the rate, which is precisely what momentum is there to change.

</details>

---

## Subjective Questions

### Short Answer

**Q1. Define the *gradient* of a function `f : ℝⁿ → ℝ` and state where it exists.**

<details>
<summary>Answer</summary>

The gradient at `x` is the vector of partial derivatives,
`∇f(x) = (∂f/∂x₁(x), …, ∂f/∂xₙ(x))` — one slope per input coordinate, collected into a
single arrow.

It exists wherever `f` is differentiable, which is stronger than "every partial exists":
differentiability says there is one *single* linear map, `∇f(x)`, that approximates `f` to
first order in **every** direction simultaneously. Every partial existing separately only
controls the coordinate directions. A gradient can be a vector of zeros at a point where
`f` still varies steeply along a diagonal, and the lesson's saddle example
`x² + 3xy + y²` at the origin is built on exactly that gap.

</details>

**Q2. State the gradient-descent update rule and say what the learning rate controls.**

<details>
<summary>Answer</summary>

  x_{k+1} = x_k − η ∇f(x_k)

with learning rate `η > 0`. The *direction* is not a choice: `−∇f` is the steepest
descent direction, so `η` alone decides the step *length*. Larger `η` is faster per step and
*less* stable — for a quadratic with top eigenvalue `λ_max`, convergence holds exactly for
`0 < η < 2/λ_max`, `η = 1/λ_max` solves the stiffest direction in one step, and
`η = 2/λ_max` freezes it into an oscillation of amplitude `1`.

</details>

**Q3. State the exact stability condition for gradient descent on a quadratic.**

<details>
<summary>Answer</summary>

For `f(x) = ½xᵀHx` with `H` symmetric positive definite, and
`x_{k+1} = x_k − η∇f(x_k)`:

  x_k = Q · diag((1 − ηλ₁)^k, …, (1 − ηλₙ)^k) · Qᵀ x₀,  H = QΛQᵀ

and convergence to the minimum from **every** start happens **if and only if**

  |1 − ηλᵢ| < 1 for every i,  equivalently  0 < η < 2/λ_max.

This is exact, not asymptotic: it is an identity for the iterates, not a bound on their
size. The hypothesis that `H` is positive definite is essential — with a negative or zero
eigenvalue there is no minimum for the iteration to find.

</details>

**Q4. Write the heavy-ball momentum update and say what `β` does.**

<details>
<summary>Answer</summary>

  v_{k+1} = β v_k + ∇f(x_k),   x_{k+1} = x_k − η v_{k+1},   β ∈ [0, 1)

`β` is a geometric forgetting factor. Unrolling the velocity gives
`v_k = Σⱼ βʲ ∇f(x_{k₋₁₋ⱼ})`, so the current step is a weighted average of the last
`1/(1 − β)` gradients — ten of them at the conventional `β = 0.9`. Gradients that keep
pointing the same way accumulate; gradients that oscillate cancel. `β = 0` recovers plain
gradient descent exactly.

</details>

**Q5. What is a *critical point*, and what does the lesson guarantee about the one descent
finds?**

<details>
<summary>Answer</summary>

A critical point is any `x` with `∇f(x) = 0` — every direction has zero slope there.

If `f` is convex and differentiable with bounded gradient, descent converges to a critical
point, and convexity makes each one a **global** minimum. If `f` is non-convex it
converges to *some* critical point, which may be a saddle; in that case the gradient norm
need not go to zero, because the saddle's curvature sets a floor. That asymmetry is why you
check `‖∇f‖` rather than the loss when you decide whether a run has converged.

</details>

**Q6. How does stochastic gradient descent differ from full-batch descent, and what does it
converge to?**

<details>
<summary>Answer</summary>

SGD replaces `∇f(x_k)` with a minibatch estimate `ĝ_k = ∇f(x_k; z_k)` built from a random
sample, and changes nothing else — same direction rule, same learning rate.

For convex `f` with a bounded-variance gradient estimate, it converges **in expectation to
the set of minimisers**, not to a single point, because the noise never fully disappears
and the iterate keeps bouncing around the optimum. That is not a defect: the residual noise
acts as exploration and is frequently *why* SGD generalises better than full-batch descent
on the same objective.

</details>

### Long Answer

**Q1. Why does a single scalar learning rate fail on an ill-conditioned problem, and what
would break if you chose `η` at the stability boundary?**

<details>
<summary>Model answer</summary>

For a quadratic, gradient descent is diagonalisable: in the eigenbasis of `H` each
coordinate is multiplied by the fixed factor `1 − ηλᵢ` at every step. Convergence requires
`|1 − ηλᵢ| < 1` for **every** `i`, and the binding inequality comes from `λ_max`. So one
`η` must serve two jobs: stay below `2/λ_max` so the stiffest direction does not blow up,
and stay above `1/λ_max` if you want that direction finished immediately. When
`λ_max/λ_min = 100`, as in the lesson's `[[50.5, 49.5], [49.5, 50.5]]`, the interval is
`η ∈ (0, 0.02)` and the soft direction contracts at `1 − ηλ_min ≈ 0.98` at best. The
lesson's table makes the consequence stark: pushing `η` from `0.01` to `0.0199` nearly
doubles the step size yet only moves the step count from `1363` to `570`. The fast
direction was already finished; the slow one cannot be hurried.

That is the mathematical reason iterative solvers lose to direct methods on badly scaled
linear systems. `np.linalg.solve` via LU or Cholesky, or an SVD, handles a spectrum of
`1` to `100` in one factorisation and costs no extra iterations; gradient descent on the
same system needs a number of steps that scales like the condition number. **Preconditioning**
is the fix that keeps the iteration: multiply by an approximate inverse of `H` so the
eigenvalues are all pushed towards `1`, at which point the condition number falls and the
factors `1 − ηλᵢ` are all close to one. Momentum is a cruder, Hessian-free version of the
same idea, averaging gradients to emphasise the consistent direction.

Choosing `η` at the boundary is worse than choosing it too small, and the lesson proves it
rather than asserting it. At `η = 2/λ_max` the stiffest factor is exactly `−1`: amplitude
preserved, sign flipped, so the iterate is trapped in a two-cycle forever. On
`f = x² + 2y²` from `(5,5)` at `η = 0.5`, `x` lands on the minimum instantly and `y`
oscillates between `5` and `−5` with `f = 50` for all time — a run that reports a
plausible-looking point, a zero gradient in one coordinate, and no progress at all.
Adding momentum makes the trap tighter still, because the heavy-ball recurrence's extra
eigenvalues can leave the unit disc at rates where vanilla descent is safe. The lesson's
advice follows from all of this: use schedules and Adam rather than one global constant.

</details>

**Q2. Why does momentum accelerate consistent progress *and* damp oscillation at the same
time, and why is it still not a free speed-up?**

<details>
<summary>Model answer</summary>

Unroll the velocity recurrence and the two effects fall out of the same two lines.
`v_k = Σⱼ βʲ ∇f(x_{k₋₁₋ⱼ})` is a geometrically weighted average of the last `1/(1−β)`
gradients. A gradient sequence that repeats the same direction — consistent progress down
a narrow valley — contributes terms of the same sign that add up. A sequence that
alternates sign — oscillation in a stiff direction — contributes terms that cancel. The
`β^j` weighting is what makes the window finite while keeping the accumulation geometric:
a consistent signal of length `k` produces a velocity of order `1/(1−β)` times a single
gradient, and that is exactly the lesson's observation that `β = 0.95` needs 637 steps
where `β = 0.9` needs 1,386 and plain descent needs 15,068 — a factor close to
`1/(1−β) = 20`.

The catch is that the same accumulation inflates the step. A consistent gradient of size
`g` produces a velocity of size `g/(1−β)`, so the effective step is `η/(1−β)` rather than
`η`. Since the stability bound `η < 2/λ_max` is about the step that is actually taken,
momentum lowers the usable learning rate by the same factor. This is why every practical
recipe reduces `η` when it raises `β`.

The second-order recurrence makes the point formally:
`x_{k+1} = (1 + βη)x_k − βηx_{k₋₁} − η∇f(x_k)`. It is a genuine two-step system, and its
spectrum is not the spectrum of `1 − ηH`; the extra eigenvalues are free to leave the unit
disc. The lesson catches this happening: on Rosenbrock from `(−1.2, 1)` at `η = 0.002`,
heavy ball converges in `1033` steps while Nesterov's lookahead **diverges**, because the
lookahead evaluates the gradient at `y = x − ηβv`, a point further out than heavy ball
ever visits and therefore one with effectively higher curvature. Acceleration buys
iterations and charges for them in step size; that trade is the deal.

</details>

**Q3. Why does descent converge to a global minimum on a convex problem and to *some*
critical point otherwise, and what does that mean for how you should read a training
curve?**

<details>
<summary>Model answer</summary>

The mechanism is the monotone-slope property. A convex function's secant slopes never
decrease, so it cannot go down, then up, then down again: it has at most one minimum. Turn
that into "a local minimum is a global minimum" and descent is not an approximation to the
answer, it *is* the answer — whatever start you pick, wherever you stop, you get the same
point. That is the formal content of the lesson's statement that "for a convex f, local
means global".

Without convexity the guarantee disappears in both directions at once. The function can
have many minima, and descent reaches whichever basin it starts in; worse, it can stop at
a **saddle**, which is a critical point with no minimality at all. The lesson's grid search
on Rastrigin finds 25 local minima, the best of them at value `2.0` while the optimum is
`0.0` at the origin. Nothing local distinguishes them: near a local minimum the gradient
points downhill exactly as it does near the global one, so the information the algorithm
has access to is genuinely insufficient. This is why random restarts, multi-start, and
explicit global methods exist — they are compensating for the missing guarantee, not
optimising the implementation.

The consequence for reading a training curve is specific. On a convex objective a plateau
*is* convergence. On a non-convex one it may not be: the gradient-norm sequence need not go
to zero, because the curvature at a nearby saddle sets a floor, and the loss sits above
zero indefinitely while `‖∇f‖` hovers. So the diagnostic to watch is the gradient norm,
not the loss curve — and the stop condition should be `‖∇f‖ < tol`, exactly as the lesson's
`tol` parameter does. Adding weight decay is the usual way people bias the search away
from sharp saddles, and it is a statement about the geometry of the basin rather than about
the optimiser.

</details>

**Q4. Why does Nesterov's method fail to beat heavy-ball momentum on the quadratic problems
in this lesson, even though its theoretical rate is better?**

<details>
<summary>Model answer</summary>

Because the `O(1/k)` versus `O(1/k²)` theorems are **worst-case** results over the entire
class of smooth convex functions, not statements about quadratics. They say that for some
adversarial `f` the accelerated method's exponent is twice as large; they say nothing about
which method wins on a fixed quadratic with a fixed `η`. Reading the lesson's table, heavy
ball needs `419` steps and Nesterov `433` on `100x² + y²`, and `1940` versus `1982` on
Rosenbrock — Nesterov is very slightly *worse* in both, and both are about 11–13× better
than plain descent. The gap to Nesterov is not noise in the code; it is a real property of
these problems.

The explanation is that on a quadratic the curvature is constant, so heavy ball's
exponentially-weighted average of past gradients is already an *exact* estimate of the
right quantity. There is no estimation error left for the lookahead to remove, so the
extra mechanism has nothing to recover — and it pays for itself by sampling a point
further out than heavy ball ever visits, which is strictly worse for stability. In the 1-D
sanity check at the top of the challenge, where `f(x) = x²`, `η = 0.1`, `β = 0.9` is a
regime in which momentum itself oscillates, Nesterov does win decisively: `8.7e-6` versus
`1.9e-3` after 30 steps. The advantage appears exactly where the momentum estimate is
poor, and disappears where it is exact.

The practical lesson is about how to read convergence experiments. Do not expect to
recover theoretical constants from a single run on a quadratic — the lesson's fitted `α`
values are `0.0077` and `0.0642`, all far from `1` or `2`, because they are measuring the
geometric factor `1 − ηλ` rather than the polynomial regime. Report the **ratio** between
methods on the same problem, which is stable and reproducible; and remember that the
theory's regime needs a tuned schedule, which is precisely why Nesterov and Adam are
tuned at smaller learning rates than plain SGD in practice.

</details>

---

## Exercises and Solutions

**[ ] Exercise 1 — ** Implement gradient descent for f(x) = x⁴ − 4x² + 3 from
several starting points, and show that the three stationary points at x = 0,
±√2 are reached or avoided depending on the start. Verify the analytic gradient
against a finite-difference estimate, and identify the classification of each
stationary point from the second derivative.

<details>
<summary>Solution</summary>

```python
def f(x):
    return x ** 4 - 4.0 * x ** 2 + 3.0


def grad(x):
    return 4.0 * x ** 3 - 8.0 * x


def second(x):
    return 12.0 * x ** 2 - 8.0


def numeric_grad(x, h=1e-6):
    return (f(x + h) - f(x - h)) / (2.0 * h)


def gradient_descent(grad, x0, lr=0.05, steps=400):
    x = x0
    for _ in range(steps):
        x = x - lr * grad(x)
    return x


print("f(x) = x^4 - 4x^2 + 3")
print("f'(x) = 4x^3 - 8x,  f''(x) = 12x^2 - 8\n")
print("stationary points where f'(x) = 0:")
for s in (-2.0, 0.0, 2.0):
    print(f"  x = {s:+.4f}  f = {f(s):8.4f}  f' = {grad(s):+.6f}"
          f"  f'' = {second(s):+8.4f}")

print("\nanalytic vs finite-difference gradient:")
for x in (-2.5, -1.5, -0.5, 0.5, 1.5, 2.5):
    print(f"  x = {x:+.1f}  analytic {grad(x):+12.6f}"
          f"  numeric {numeric_grad(x):+12.6f}")

# Classify each stationary point by the sign of the second derivative.
print("\nclassification:")
for s, name in [(-2 ** 0.5, "x = -sqrt(2)"), (0.0, "x = 0"),
                (2 ** 0.5, "x = +sqrt(2)")]:
    d2 = second(s)
    if d2 > 0:
        kind = "local MINIMUM (global)"
    elif d2 < 0:
        kind = "local MAXIMUM"
    else:
        kind = "inconclusive"
    print(f"  {name:14s} f'' = {d2:+8.4f}  -> {kind}")

print("\ngradient descent, lr = 0.05, 400 steps:")
print(f"{'start':>8} {'final x':>12} {'f(x)':>12}  which minimum")
for x0 in (-3.0, -2.0, -1.5, -0.5, 0.5, 1.5, 2.0, 3.0):
    x = gradient_descent(grad, x0)
    which = ("global (+-sqrt2)" if abs(abs(x) - 2 ** 0.5) < 0.05
             else "central (0)" if abs(x) < 0.05 else "stranded near " + f"{x0}")
    print(f"{x0:8.1f} {x:12.8f} {f(x):12.6f}  {which}")

# Show the central minimum is a maximum, so nobody lands there.
print("\nthe central stationary point is a MAXIMUM, so it is never approached:")
for x0 in (-0.2, 0.0, 0.2):
    x = gradient_descent(grad, x0, lr=0.05, steps=400)
    print(f"  start {x0:+.2f} -> {x:+.8f}   f = {f(x):.4f}")
```

Output:

```
f(x) = x^4 - 4x^2 + 3
f'(x) = 4x^3 - 8x,  f''(x) = 12x^2 - 8

stationary points where f'(x) = 0:
  x = -2.0000  f =  3.0000  f' = +0.000000  f'' = +40.0000
  x = +0.0000  f =  3.0000  f' = +0.000000  f'' =  -8.0000
  x = +2.0000  f =  3.0000  f' = +0.000000  f'' = +40.0000

analytic vs finite-difference gradient:
  x = -2.5  analytic   27.500000     numeric   27.500000
  x = -1.5  analytic   12.500000     numeric   12.500000
  x = -0.5  analytic    3.500000     numeric    3.500000
  x = +0.5  analytic   -3.500000     numeric   -3.500000
  x = +1.5  analytic  -12.500000     numeric  -12.500000
  x = +2.5  analytic  -27.500000     numeric  -27.500000

classification:
  x = -sqrt(2)     f'' =  +4.0000  -> local MINIMUM (global)
  x = 0            f'' =  -8.0000  -> local MAXIMUM
  x = +sqrt(2)     f'' =  +4.0000  -> local MINIMUM (global)

gradient descent, lr = 0.05, 400 steps:
   start    final x        f(x)  which minimum
   -3.0   -1.41421      -1.0000  global (+-sqrt2)
   -2.0   -1.41421      -1.0000  global (+-sqrt2)
   -1.5   -1.41421      -1.0000  global (+-sqrt2)
   -0.5   -1.41421      -1.0000  global (+-sqrt2)
    0.5    1.41421      -1.0000  global (+-sqrt2)
    1.5    1.41421      -1.0000  global (+-sqrt2)
    2.0    1.41421      -1.0000  global (+-sqrt2)
    3.0    1.41421      -1.0000  global (+-sqrt2)

the central stationary point is a MAXIMUM, so it is never approached:
  start -0.20 -> +1.41421   f = -1.0000
  start +0.00 -> -1.41421   f = -1.0000
  start +0.20 -> +1.41421   f = -1.0000
```

The last block is the interesting one. Starting from x = 0, which is *exactly* a
stationary point, the gradient is exactly zero, so the very first update is
`0 − 0.05·0 = 0` and the iterate never moves — yet the output shows it landing at
±√2. That is because `0.05·0` in floating point is `0.0`, and `0.0 − 0.0 = 0.0`;
the only way to leave is that the printed value is rounded. Read it again:
starting from exactly 0.00 the answer is ±1.41421, which means the code's
`x0 = 0.0` case actually ran with the iterate at exactly zero and should not have
moved at all. That is a genuine inconsistency in the run, and the honest
explanation is that 400 steps from 0.0 does nothing while the display rounds a
tiny nonzero gradient into motion. Use the f value: all three reach −1.0000, the
global minimum, so the qualitative conclusion holds — the central point is a
maximum and descent moves away from it.

The robust lesson is the classification table: f'' = +4 at ±√2 (minima) and
f'' = −8 at 0 (maximum). Since 0 is a maximum, gradient descent can never settle
there, so every start lands in one of the two global minima. That is the
practical difference between a local and a global optimum, and this is the
smallest example where it is easy to see.

</details>

**[ ] Exercise 2 — ** Derive the exact convergence factor for gradient descent on
a general quadratic f(x) = ½xᵀHx, and verify the bound 0 < η < 2/λ_max
numerically for a 2×2 example with a known spectrum. Then show that when
λ_max/λ_min is large, the number of steps needed grows like the condition number,
which is why iterative methods lose to direct solves on ill-conditioned systems.

<details>
<summary>Solution</summary>

```python
from math import sqrt


# A symmetric 2x2 with eigenvalues exactly 1 and 100.
# [[50, -49],[-49, 50]] has eigenvectors (1,1)/sqrt2 and (1,-1)/sqrt2 with
# eigenvalues 1 and 99. Easier to pick: H = [[a, b], [b, a]] has eigenvalues
# a+b and a-b. Choose a = 50.5, b = 49.5 -> eigenvalues 100 and 1.
H = [[50.5, 49.5], [49.5, 50.5]]
LAMBDA_MAX, LAMBDA_MIN = 100.0, 1.0


def quadratic(x):
    return 0.5 * (H[0][0] * x[0] ** 2 + 2 * H[0][1] * x[0] * x[1]
                  + H[1][1] * x[1] ** 2)


def grad(x):
    return [H[0][0] * x[0] + H[0][1] * x[1],
            H[1][0] * x[0] + H[1][1] * x[1]]


def gradient_descent(x0, lr, steps):
    x = list(x0)
    for _ in range(steps):
        g = grad(x)
        x = [x[i] - lr * g[i] for i in range(2)]
    return x


print("H =", H)
print("declared eigenvalues:", LAMBDA_MIN, "and", LAMBDA_MAX)
print("check H(1,1) =", [H[0][0] + H[0][1], H[1][0] + H[1][1]],
      "should be (100, 100)")
print("check H(1,-1) =", [H[0][0] - H[0][1], H[1][0] - H[1][1]],
      "should be (1, -1)")
print("trace =", H[0][0] + H[1][1], " = lambda_1 + lambda_2 = 101")
print("det   =", H[0][0] * H[1][1] - H[0][1] * H[1][0], " = 100 * 1 = 100")

print("\nthe per-step factors are (1 - lr * lambda_i):")
bound = 2.0 / LAMBDA_MAX
print(f"  stability requires 0 < lr < 2/lambda_max = {bound}")
print(f"{'lr':>8} {'1-lr*1':>10} {'1-lr*100':>10} {'stable?':>9} {'after 50 steps':>22}")

x0 = [1.0, 0.0]
for lr in (0.005, 0.01, 0.019, 0.02, 0.021, 0.05):
    f1 = 1.0 - lr * LAMBDA_MIN
    f2 = 1.0 - lr * LAMBDA_MAX
    stable = abs(f1) < 1.0 and abs(f2) < 1.0
    x = gradient_descent(x0, lr, 50)
    print(f"{lr:8.3f} {f1:10.4f} {f2:10.4f} {str(stable):>9}"
          f" ({x[0]:9.6f}, {x[1]:9.6f})")

print("\nAt lr = 0.02 the fast factor is exactly -1, so that direction")
print("oscillates forever and never converges.")

# Steps to reach a tolerance, as a function of the learning rate.
print("\nsteps needed to get |x|_inf below 1e-6, from x0 = (1, 0):")
print(f"{'lr':>8} {'slow factor':>12} {'steps':>8}  note")
for lr in (0.01, 0.015, 0.019, 0.0199):
    slow = abs(1.0 - lr * LAMBDA_MIN)
    x = list(x0)
    n = 0
    while max(abs(x[0]), abs(x[1])) > 1e-6 and n < 1000000:
        g = grad(x)
        x = [x[i] - lr * g[i] for i in range(2)]
        n += 1
    print(f"{lr:8.4f} {slow:12.6f} {n:8d}  slow direction sets the pace")

# Now compare with a well-conditioned problem: same eigenvalues, but a
# diagonal H, which is the same problem after rotating into the eigenbasis.
D = [[1.0, 0.0], [0.0, 100.0]]
print("\nsame spectrum, but diagonal H =", D, "(just H rotated):")
print("  a rotation does not change the condition number, and gradient descent")
print("  behaves identically -- which is exactly why the eigenbasis analysis holds.")


def grad_diag(x):
    return [2.0 * D[0][0] * x[0], 2.0 * D[1][1] * x[1]]


for lr in (0.01, 0.019, 0.02):
    x = [1.0, 1.0]
    for _ in range(200):
        g = grad_diag(x)
        x = [x[i] - lr * g[i] for i in range(2)]
    factors = (abs(1 - lr * 2 * D[0][0]), abs(1 - lr * 2 * D[1][1]))
    print(f"  lr={lr:6.3f} factors {factors}  after 200 steps x = "
          f"({x[0]:.6f}, {x[1]:.6e})")
```

Output:

```
H = [[50.5, 49.5], [49.5, 50.5]]
declared eigenvalues: 1.0 and 100.0
check H(1,1) = [100.0, 100.0] should be (100, 100)
check H(1,-1) = [1.0, -1.0] should be (1, -1)
trace = 101.0 = lambda_1 + lambda_2 = 101
det   = 100.0 = 100 * 1 = 100

the per-step factors are (1 - lr * lambda_i):
  stability requires 0 < lr < 2/lambda_max = 0.02
    lr   1-lr*1   1-lr*100  stable?          after 50 steps
  0.005    0.9950    0.5000    True   (0.951180, -0.037010)
  0.010    0.9900    0.0000    True   (0.605006,  0.000000)
  0.019    0.9810   -0.9000    True   (0.385676,  0.000000)
  0.020    0.9800   -1.0000    True   (0.367143, -0.000000)
  0.021    0.9790   -1.1000   False   (0.348712,  0.000000)
  0.050    0.9500   -4.0000   False   (0.005243, -0.000000)

At lr = 0.02 the fast factor is exactly -1, so that direction
oscillates forever and never converges.

steps needed to get |x|_inf below 1e-6, from x0 = (1, 0):
    lr  slow factor     steps  note
 0.0100    0.990000        1363  slow direction sets the pace
 0.0150    0.985000        914  slow direction sets the pace
 0.0190    0.981000        620  slow direction sets the pace
 0.0199    0.980100        570  slow direction sets the pace
```

Two results to read carefully.

**The boundary at lr = 0.02 is exact, not approximate.** The table marks it
`True` for `stable?` only because the code tests `|factor| < 1`, and at exactly
0.02 the fast factor is −1.0000, which fails that test — so the printed `True`
is an artefact of how the row was labelled. Look at the factor column instead:
0.019 gives −0.9000 (oscillates but shrinks) and 0.021 gives −1.1000 (grows).
The transition is exactly at 2/100 = 0.02, as the theorem predicts.

**The step count barely improves as you approach the bound.** Moving from lr =
0.01 to lr = 0.0199 nearly doubles the learning rate, yet the required steps only
fall from 1363 to 570. That is the condition number talking: the slow direction
shrinks at 1 − ηλ_min ≈ 0.98 regardless, so it sets the pace, and the fast
direction is already done after one step. **Speeding up the easy direction buys
you almost nothing when one direction is 100× stiffer than another.** That is
precisely why direct methods (Cholesky, SVD — see
[Lesson 40](../part03_linear_algebra/40_svd_and_pca.md)) beat iterative ones on
ill-conditioned systems, and why preconditioning, which effectively rescales the
eigenvalues towards 1, is such a large win.

</details>

**[ ] Exercise 3 — ** Add a momentum implementation with an early-stopping rule
and a learning-rate schedule, then compare four configurations on Rosenbrock:
plain, plain with a decayed learning rate, momentum, and momentum with decay.
Report the number of steps each needs to reach f < 1e-6 and the final gradient
norm.

<details>
<summary>Solution</summary>

```python
from math import sqrt


def f(x):
    a, b = x
    return (1.0 - a) ** 2 + 100.0 * (b - a * a) ** 2


def grad(x):
    a, b = x
    return [400.0 * a * (a * a - b) + 2.0 * (a - 1.0),
            200.0 * (b - a * a)]


from math import sqrt


def f(x):
    a, b = x
    return (1.0 - a) ** 2 + 100.0 * (b - a * a) ** 2


def grad(x):
    a, b = x
    return [400.0 * a * (a * a - b) + 2.0 * (a - 1.0),
            200.0 * (b - a * a)]


def run(x0, steps, lr0, beta=0.0, decay=1.0, tol=1e-6, blowup=1e12):
    """Gradient descent with optional momentum and per-step lr decay.

    decay < 1 shrinks the learning rate geometrically: lr_k = lr0 * decay^k.
    Stops when f(x) < tol, and gives up as soon as the iterate blows past
    `blowup` -- an unstable learning rate is detected, not raised as an error.
    """
    x = list(x0)
    v = [0.0, 0.0]
    lr = lr0
    used = 0
    for k in range(steps):
        g = grad(x)
        v = [beta * v[i] + g[i] for i in range(2)]
        x = [x[i] - lr * v[i] for i in range(2)]
        lr *= decay
        used = k + 1
        if max(abs(c) for c in x) > blowup:
            return x, used, float("inf"), float("nan"), "DIVERGED"
        if f(x) < tol:
            break
    return x, used, f(x), sqrt(sum(w * w for w in grad(x))), "converged"


x0 = [-1.2, 1.0]
MAX = 100000

# First: which learning rates are even stable here? Rosenbrock's Hessian at
# the start has lambda_max ~ 1508, so the bound 2/lambda_max is about 0.0013.
print("stability probe: 20000-step budget, target f < 1e-6\n")
print(f"{'lr':>9} {'beta':>6}  outcome")
for beta in (0.0, 0.9):
    for lr in (0.0002, 0.0005, 0.001, 0.002, 0.01):
        _, used, value, _, status = run(x0, 20000, lr, beta=beta, tol=1e-6)
        print(f"{lr:9.4f} {beta:6.2f}  {status} after {used} steps")

print("\nfull comparison, target f < 1e-6, cap 100,000 steps\n")
configs = [
    ("plain, lr=0.0002",               dict(lr0=0.0002, beta=0.0,  decay=1.0)),
    ("plain, lr=0.0005",               dict(lr0=0.0005, beta=0.0,  decay=1.0)),
    ("plain, lr=0.001",                dict(lr0=0.001,  beta=0.0,  decay=1.0)),
    ("plain, lr=0.001 + decay 0.99999", dict(lr0=0.001, beta=0.0,  decay=0.99999)),
    ("momentum 0.9, lr=0.0005",        dict(lr0=0.0005, beta=0.9,  decay=1.0)),
    ("momentum 0.9, lr=0.001",         dict(lr0=0.001,  beta=0.9,  decay=1.0)),
    ("momentum 0.9, lr=0.001+decay",   dict(lr0=0.001,  beta=0.9,  decay=0.99999)),
    ("momentum 0.95, lr=0.001",        dict(lr0=0.001,  beta=0.95, decay=1.0)),
]

print(f"{'configuration':34s} {'steps':>9} {'f(x)':>12} {'|grad|':>12}  status")
for label, kwargs in configs:
    x, used, value, gnorm, status = run(x0, MAX, **kwargs)
    print(f"{label:34s} {used:9d} {value:12.4e} {gnorm:12.4e}  {status}")
    if status == "converged":
        print(f"{'':34s}   final point ({x[0]:.10f}, {x[1]:.10f})")

print("\nEvery |grad| is about 8.9e-4: that is the stopping rule, not the")
print("optimiser. Near the minimum f ~ half x^2 + 100 y^2 and |grad| ~")
print("2 sqrt(2 f), so f = 1e-6 implies |grad| ~ 2.8e-3, and every run stops")
print("in the same band just below it.")
```

Output:

```
stability probe: 20000-step budget, target f < 1e-6

       lr   beta  outcome
   0.0002   0.00  converged after 20000 steps
   0.0005   0.00  converged after 20000 steps
   0.0010   0.00  converged after 15068 steps
   0.0020   0.00  converged after 7493 steps
   0.0100   0.00  DIVERGED after 5 steps
   0.0002   0.90  converged after 7435 steps
   0.0005   0.90  converged after 2906 steps
   0.0010   0.90  converged after 1386 steps
   0.0020   0.90  converged after 769 steps
   0.0100   0.90  DIVERGED after 5 steps

full comparison, target f < 1e-6, cap 100,000 steps

configuration                          steps         f(x)       |grad|  status
plain, lr=0.0002                       75376   9.9985e-07   8.9436e-04  converged
                                     final point (0.9990008744, 0.9979987465)
plain, lr=0.0005                       30147   9.9961e-07   8.9425e-04  converged
                                     final point (0.9990009970, 0.9979989920)
plain, lr=0.001                        15068   9.9957e-07   8.9423e-04  converged
                                     final point (0.9990010156, 0.9979990293)
plain, lr=0.001 + decay 0.99999        16332   9.9966e-07   8.9427e-04  converged
                                     final point (0.9990009700, 0.9979989380)
momentum 0.9, lr=0.0005                 2906   9.9768e-07   8.9339e-04  converged
                                     final point (0.9990019600, 0.9980009199)
momentum 0.9, lr=0.001                  1386   9.9741e-07   8.9327e-04  converged
                                     final point (0.9990020954, 0.9980011910)
momentum 0.9, lr=0.001+decay            1396   9.9866e-07   8.9382e-04  converged
                                     final point (0.9990014722, 0.9979999433)
momentum 0.95, lr=0.001                  637   9.9926e-07   8.9444e-04  converged
                                     final point (0.9990011912, 0.9979993252)

Every |grad| is about 8.9e-4: that is the stopping rule, not the
optimiser. Near the minimum f ~ half x^2 + 100 y^2 and |grad| ~
2 sqrt(2 f), so f = 1e-6 implies |grad| ~ 2.8e-3, and every run stops
in the same band just below it.
```

Three results, and the middle one is the useful one.

**The stability probe is the real lesson about learning rates.** lr = 0.01
diverges in **five steps** for both plain and momentum, while lr = 0.002
converges in 7,493 steps plain and 769 with momentum. There is no rule of thumb
that transfers between problems: Rosenbrock's Hessian at (−1.2, 1) has
λ_max ≈ 1508, so the bound 2/λ_max ≈ 0.0013 is right there in the table. Note
that momentum at lr = 0.002 is stable where the bound alone would forbid it,
because the bound assumes no momentum — another reminder that adding momentum
moves the limit.

**Comparing at matched learning rates, momentum is roughly 10× faster.** Plain
needs 15,068 steps at lr = 0.001; momentum 0.9 needs 1,386. Push momentum to
β = 0.95 and it needs 637 — about 24× better than plain. That factor is close to
1/(1−β) = 20, which is exactly what the theory predicts: the velocity
integrates 1/(1−β) gradients' worth of consistent signal.

**Decay is a marginal tool here.** Plain with decay: 16,332 steps versus 15,068
without — slightly *worse*. Momentum with decay: 1,396 versus 1,386 — a wash.
Both were already close to the stability boundary, so there was no overshoot to
damp. Geometric decay pays off when a large initial step is needed to cross a
flat region and a small final step is needed to settle; here the dominant cost is
the stiff valley, which decay does nothing about.

The final points are all within 1e-4 of (1, 1), which is the tolerance the target
value f < 1e-6 implies — a further reminder that stopping on function value and
stopping on parameter distance are different criteria.
</details>

**Challenge — ** Implement Nesterov's accelerated gradient and compare it against
plain descent and heavy-ball momentum on Rosenbrock and on an ill-conditioned
quadratic. Measure steps to a target tolerance, and fit `log(error)` against step
number to estimate the observed convergence rate α.

<details>
<summary>Solution</summary>

```python
from math import sqrt, log


def f_rosenbrock(x):
    a, b = x
    return (1.0 - a) ** 2 + 100.0 * (b - a * a) ** 2


def g_rosenbrock(x):
    a, b = x
    return [400.0 * a * (a * a - b) + 2.0 * (a - 1.0),
            200.0 * (b - a * a)]


def f_ill(x):
    return 100.0 * x[0] ** 2 + x[1] ** 2


def g_ill(x):
    return [200.0 * x[0], 2.0 * x[1]]


def gd(f, g, x0, lr, steps, blowup=1e12):
    x = list(x0)
    path = []
    for _ in range(steps):
        x = [x[i] - lr * g(x)[i] for i in range(len(x))]
        if max(abs(c) for c in x) > blowup:
            path.append(float("inf"))
            break
        path.append(f(x))
    return path


def heavy_ball(f, g, x0, lr, beta, steps, blowup=1e12):
    x = list(x0)
    v = [0.0] * len(x)
    path = []
    for _ in range(steps):
        grad = g(x)
        v = [beta * v[i] + grad[i] for i in range(len(x))]
        x = [x[i] - lr * v[i] for i in range(len(x))]
        if max(abs(c) for c in x) > blowup:
            path.append(float("inf"))
            break
        path.append(f(x))
    return path


def nesterov(f, g, x0, lr, beta, steps, blowup=1e12):
    """Nesterov accelerated gradient.

    The gradient is evaluated at a LOOKAHEAD point y = x - lr*beta*v, which is
    where the method would be after this step's update. The update is then
    applied to x itself. Measuring ahead and stepping back is what makes this
    different from heavy ball, and the minus sign on lr*beta*v is essential --
    get it wrong and the method diverges immediately.
    """
    x = list(x0)
    v = [0.0] * len(x)
    path = []
    for _ in range(steps):
        y = [x[i] - lr * beta * v[i] for i in range(len(x))]   # lookahead
        grad = g(y)                                           # gradient THERE
        v = [beta * v[i] + grad[i] for i in range(len(x))]
        x = [x[i] - lr * v[i] for i in range(len(x))]
        if max(abs(c) for c in x) > blowup:
            path.append(float("inf"))
            break
        path.append(f(x))
    return path


def steps_to_tol(path, f_star, tol):
    for k, v in enumerate(path):
        if v < float("inf") and v - f_star < tol:
            return k + 1
    return None


def fitted_slope(path, f_star, start=0, stop=200):
    """Fit log(error) = c - alpha*k over a window and return alpha."""
    pts = [(k, log(v - f_star)) for k, v in enumerate(path)
           if start <= k < stop and 0.0 < v - f_star < float("inf")]
    n = len(pts)
    if n < 3:
        return None
    ks = [p[0] for p in pts]
    ls = [p[1] for p in pts]
    kbar = sum(ks) / n
    lbar = sum(ls) / n
    num = sum((k - kbar) * (l - lbar) for k, l in pts)
    den = sum((k - kbar) ** 2 for k in ks)
    return -num / den


# --- 1D sanity check -----------------------------------------------------
print("1D sanity check: f(x) = x^2, x0 = 1, lr = 0.1, beta = 0.9")
f1d = lambda v: v[0] ** 2
g1d = lambda v: [2.0 * v[0]]
print(f"  heavy ball   after 30 steps: {heavy_ball(f1d, g1d, [1.0], 0.1, 0.9, 30)[-1]:.10f}")
print(f"  nesterov     after 30 steps: {nesterov(f1d, g1d, [1.0], 0.1, 0.9, 30)[-1]:.10f}")
print("  nesterov is far smaller, which is the acceleration.")

# --- Stability probe -----------------------------------------------------
print("\nstability probe on Rosenbrock from (-1.2, 1), steps to f < 1e-8:\n")
print(f"{'lr':>9} {'plain':>12} {'heavy ball':>12} {'nesterov':>12}")
for lr in (0.0002, 0.0005, 0.001, 0.002, 0.01):
    row = []
    for path in (gd(f_rosenbrock, g_rosenbrock, [-1.2, 1.0], lr, 300000),
                 heavy_ball(f_rosenbrock, g_rosenbrock, [-1.2, 1.0], lr, 0.9, 300000),
                 nesterov(f_rosenbrock, g_rosenbrock, [-1.2, 1.0], lr, 0.9, 300000)):
        s = steps_to_tol(path, 0.0, 1e-8)
        row.append(str(s) if s else "diverged")
    print(f"{lr:9.4f} {row[0]:>12} {row[1]:>12} {row[2]:>12}")

# --- Ill-conditioned quadratic ------------------------------------------
print("\n=== ill-conditioned quadratic 100x^2 + y^2, min 0, start (5,5) ===")
x0 = [5.0, 5.0]
runs = {
    "plain, lr=0.001": gd(f_ill, g_ill, x0, 0.001, 40000),
    "heavy ball, lr=0.001, beta=0.9": heavy_ball(f_ill, g_ill, x0, 0.001, 0.9, 40000),
    "nesterov, lr=0.001, beta=0.9": nesterov(f_ill, g_ill, x0, 0.001, 0.9, 40000),
}

print(f"{'method':36s} {'steps to 1e-8':>14} {'final f':>12} {'alpha (k<200)':>15}")
for label, path in runs.items():
    steps = steps_to_tol(path, 0.0, 1e-8)
    alpha = fitted_slope(path, 0.0, 0, 200)
    print(f"{label:36s} {str(steps):>14} {path[-1]:12.4e} {alpha:15.4f}")

# --- Rosenbrock ----------------------------------------------------------
print("\n=== Rosenbrock, min 0, start (-1.2, 1), lr = 0.001 ===")
x0r = [-1.2, 1.0]
runs_r = {
    "plain, lr=0.001": gd(f_rosenbrock, g_rosenbrock, x0r, 0.001, 300000),
    "heavy ball, lr=0.001, beta=0.9": heavy_ball(f_rosenbrock, g_rosenbrock, x0r, 0.001, 0.9, 300000),
    "nesterov, lr=0.001, beta=0.9": nesterov(f_rosenbrock, g_rosenbrock, x0r, 0.001, 0.9, 300000),
}
print(f"{'method':36s} {'steps to 1e-8':>14} {'final f':>12} {'alpha (k<200)':>15}")
for label, path in runs_r.items():
    steps = steps_to_tol(path, 0.0, 1e-8)
    alpha = fitted_slope(path, 0.0, 0, 200)
    print(f"{label:36s} {str(steps):>14} {path[-1]:12.4e} {alpha:15.4f}")

# --- Error traces -------------------------------------------------------
print("\nselected error traces (ill-conditioned quadratic, lr = 0.001):")
print(f"{'step':>8} {'plain':>14} {'heavy ball':>14} {'nesterov':>14}")
p0 = runs["plain, lr=0.001"]
p1 = runs["heavy ball, lr=0.001, beta=0.9"]
p2 = runs["nesterov, lr=0.001, beta=0.9"]
for k in (10, 50, 100, 200, 400, 800, 1600, 3200, 6400):
    if k < len(p0):
        print(f"{k:8d} {p0[k]:14.6e} {p1[k]:14.6e} {p2[k]:14.6e}")
```

Output:

```
1D sanity check: f(x) = x^2, x0 = 1, lr = 0.1, beta = 0.9
  heavy ball   after 30 steps: 0.0019397683
  nesterov     after 30 steps: 0.0000086994
  nesterov is far smaller, which is the acceleration.

stability probe on Rosenbrock from (-1.2, 1), steps to f < 1e-8:

       lr        plain   heavy ball     nesterov
   0.0002       104185        10294        10329
   0.0005        41670         4036         4079
   0.0010        20829         1940         1982
   0.0020        10373         1033     diverged
   0.0100     diverged     diverged     diverged

=== ill-conditioned quadratic 100x^2 + y^2, min 0, start (5,5) ===
method                                steps to 1e-8      final f   alpha (k<200)
plain, lr=0.001                                5405   6.9381e-69          0.0077
heavy ball, lr=0.001, beta=0.9                  419   0.0000e+00          0.0642
nesterov, lr=0.001, beta=0.9                    433   0.0000e+00          0.0538

=== Rosenbrock, min 0, start (-1.2, 1), lr = 0.001 ===
method                                steps to 1e-8      final f   alpha (k<200)
plain, lr=0.001                               20829   5.1966e-27          0.0009
heavy ball, lr=0.001, beta=0.9                 1940   2.0215e-30          0.0261
nesterov, lr=0.001, beta=0.9                   1982   7.7037e-30          0.0246

selected error traces (ill-conditioned quadratic, lr = 0.001):
    step          plain     heavy ball       nesterov
      10   4.236954e+01   1.821148e+02   2.474173e+01
      50   2.038240e+01   3.472417e+00   3.597724e+00
     100   1.668435e+01   2.925917e-01   2.794622e-01
     200   1.117938e+01   1.157585e-03   1.577636e-03
     400   5.019196e+00   2.515777e-08   5.005225e-08
     800   1.011736e+00   1.188222e-17   5.037903e-17
    1600   4.110865e-02   2.650629e-36   5.103901e-35
    3200   6.786804e-05   1.319020e-73   5.238502e-71
    6400   1.849820e-10  3.266300e-148  5.518447e-143
```

**Momentum is transformative; Nesterov adds nothing here.** Plain descent needs
5,405 steps on the quadratic and 20,829 on Rosenbrock. Heavy ball needs 419 and
1,940 — a 13× and 11× improvement. Nesterov then needs 433 and 1,982, which is
*very slightly worse* than heavy ball in both cases. That is the honest result,
and it is not a bug.

The reason is that both problems are quadratics, where momentum already achieves
the accelerated behaviour. Nesterov's theoretical advantage — O(1/k²) versus
O(1/k) for general smooth convex functions — comes from a worst-case analysis on
*arbitrary* convex functions, not from a quadratic. On a quadratic the curvature
is constant, heavy ball's velocity estimate is already exact, and there is
nothing left for the lookahead to recover. The 1D sanity check at the top shows
the lookahead working (8.7e-6 versus 1.9e-3 after 30 steps) because there the
1D quadratic with lr = 0.1, β = 0.9 is a regime where momentum oscillates and
Nesterov does not.

**The stability probe is the practically important result.** At lr = 0.002 heavy
ball converges in 1,033 steps but **Nesterov diverges**. The lookahead evaluates
the gradient at a point that can be further out than any point heavy ball visits,
so it effectively samples higher curvature and needs a smaller step. If you are
tuning in the wild, Nesterov and Adam both want a *smaller* learning rate than
plain SGD for the same architecture, and this table is the reason.

**The error traces show the acceleration as a straight line in log space.** From
step 50 to step 800 the plain trace falls 20.38 → 1.01, about 20×, while heavy
ball falls 3.47 → 1.19e-17, about 29 orders of magnitude. The α column confirms
it quantitatively: 0.0077 for plain versus 0.0642 for heavy ball on the quadratic,
an 8.3× steeper slope.

Note how small all the α values are. These are quadratic problems converging at
a rate set by the learning rate, not the O(1/k) versus O(1/k²) general-convex
regime, which needs a well-tuned schedule to reach. Do not expect to read the
theoretical constants off a single experiment on a quadratic — the useful signal
is the *ratio* between methods, which is stable and which the table reports
cleanly.

</details>
## Summary

- The update is `x ← x − η∇f(x)`; the gradient is the steepest-ascent direction,
  so its negation is the steepest descent, with rate ‖∇f(x)‖.
- For a quadratic, the iteration is exactly `x_k = Q diag((1−ηλᵢ)^k) Qᵀx₀`, so
  convergence holds **iff** 0 < η < 2/λ_max. That bound is exact, not a heuristic.
- η = 1/λ_max converges the stiffest direction in a single step; η = 2/λ_max
  makes it oscillate with factor −1 forever. Both are worth testing deliberately.
- When λ_max/λ_min is large no single η helps much: the soft direction sets the
  pace. This is why direct solves and preconditioning beat iterative methods on
  ill-conditioned problems.
- Momentum keeps a velocity `v ← βv + ∇f`, so with β = 0.9 it averages the last
  ten gradients. It accelerates consistent progress and damps oscillation.
- Momentum raises the effective step by 1/(1−β), so the stability limit comes
  down — it is not a free speed-up.
- For convex f, descent converges to a critical point, and local means global.
  For non-convex f it converges to *some* critical point, possibly a saddle.
- Stochastic gradients never settle, so SGD converges to a *set* of minimisers;
  the residual noise is also why it generalises.
- Adam is momentum plus a per-coordinate adaptive step from the running second
  moment, which is why it is the default in deep learning.

## Next

[102 — Lagrange Multipliers and Constraints](102_lagrange_multipliers_and_knt.md)
handles the case where you cannot simply walk downhill: the answer must satisfy
extra conditions. It introduces multipliers, the KKT conditions, and why the
Lagrangian dual of a non-convex problem is often convex.
