# 53 — Multivariable Calculus

**Part**: part04_calculus · **Prerequisites**: 41, 51 · **Time**: 40 min

---

## In Plain Words

Everything in lesson 51 still works when the input is a list of numbers instead of a
single number. What changes is that there is no longer just "the" slope — there is one
slope per input coordinate, called a *partial derivative*. Collect them into a list and
you have the *gradient*.

The gradient turns out to be far more useful than a bag of slopes. It is a single arrow
that points in the direction in which the function grows fastest, and its length says how
fast. That is why gradient-based optimisation moves along the gradient: it is the steepest
available direction, so you lose the least function value for a given distance travelled.
It also means the gradient is always perpendicular to the curve of constant function
value — the contour — which is why gradient descent visibly cuts *across* a landscape
instead of sliding along its valleys.

For outputs that are themselves vectors, the collection of all partial derivatives becomes
a matrix called the Jacobian, and one single matrix of multiplication handles the whole
chain of derivatives. That matrix form is exactly what backpropagation computes, and what
`torch.autograd` calls the "backward of a matrix multiply".

---

## Why Computer Science Cares

- **The gradient is the update rule.** `x -= lr * grad` is the whole of SGD. Adam,
  RMSProp, Adagrad and their descendants are all modifications of the step size, and every
  one of them is derived from statistics of this gradient vector.
- **Convexity is a statement about the Hessian.** For a quadratic loss, the Hessian is a
  constant matrix whose largest eigenvalue caps the usable learning rate at
  $2/\lambda_{\max}$. For a neural network you cannot compute it, which is why people
  normalise layers, use careful initialisation, and clip gradients.
- **The Jacobian is the derivative of a linear map.** For a layer $y = Wx$ the Jacobian is
  $W$ itself, so backprop is literally "multiply by the weight matrices again". See
  [31 — Matrices and Matrix Algebra](../part03_linear_algebra/31_matrices_and_matrix_algebra.md).
- **Optimisers are gradient methods.** L-BFGS uses the gradient and an estimate of its
  inverse from recent steps; `scipy.optimize.minimize(method="BFGS")` and `trust-exact`
  build a curvature model from gradients alone. Newton needs the full Hessian.
- **Geometry engines compute gradients of distance fields.** Eikonal equations, signed
  distance functions and level sets all revolve around $|\nabla f|$ being constant on a
  distance field.
- **Computer vision.** Image gradients (`Sobel`, `Scharr`, Canny edge detection) are
  literally $\partial I/\partial x$ and $\partial I/\partial y$ of pixel intensity, and
  they are the basis of every edge detector.

---

## The Formal Version

**Definition.** Let $f : \mathbb{R}^n \to \mathbb{R}$. The *partial derivative* of $f$
with respect to its $i$-th coordinate at $a \in \mathbb{R}^n$ is

$$\frac{\partial f}{\partial x_i}(a) = \lim_{h \to 0} \frac{f(a + h e_i) - f(a)}{h},$$

where $e_i$ is the $i$-th standard basis vector.

*Explanation.* Hold every coordinate but one fixed, and take the ordinary one-variable
derivative with respect to that one. The notation "hold $y$ constant" in $\frac{\partial f}{\partial x}$
means exactly this.

**Definition.** The *gradient* of $f$ at $a$ is the vector of partials:

$$\nabla f(a) = \left(\frac{\partial f}{\partial x_1}, \dots, \frac{\partial f}{\partial x_n}\right)(a).$$

$f$ is *differentiable* at $a$ if $f(a+h) = f(a) + \nabla f(a) \cdot h + o(\|h\|)$ as
$h \to 0$.

*Explanation.* Differentiability means the whole function is locally a linear function plus
a negligible error. That is a much stronger requirement than every partial derivative
existing, and it is the assumption under all the results below.

**Definition.** The *directional derivative* of $f$ at $a$ in the direction of a **unit**
vector $u$ is

$$D_u f(a) = \lim_{t \to 0} \frac{f(a + tu) - f(a)}{t} = \nabla f(a) \cdot u.$$

**Theorem (Steepest ascent).** Among all unit vectors $u$, the directional derivative
$\nabla f \cdot u$ is maximised when $u = \nabla f/\|\nabla f\|$, and the maximum value is
$\|\nabla f\|$.

*Proof.* By Cauchy–Schwarz, $\nabla f \cdot u \le \|\nabla f\|\,\|u\| = \|\nabla f\|$,
with equality exactly when $u$ is parallel to $\nabla f$. ✓

**Theorem (Perpendicularity).** If $u$ is tangent to a level set $\{x : f(x) = c\}$ then
$\nabla f \cdot u = 0$.

*Proof.* Along a level set $f$ is constant, so its derivative in the tangent direction is
zero. ✓

**Theorem (Multivariable chain rule).** Let $g : \mathbb{R}^m \to \mathbb{R}^n$ and
$f : \mathbb{R}^n \to \mathbb{R}$, both differentiable, and let $h = f \circ g$. Then
$\nabla h(x) = J_g(x)^{\mathsf T} \nabla f(g(x))$, where $J_g$ is the Jacobian of $g$.

*Explanation.* Each component of the gradient of $h$ is a sum over all intermediate
coordinates: $\frac{\partial h}{\partial x_i} = \sum_j \frac{\partial f}{\partial g_j}
\frac{\partial g_j}{\partial x_i}$. Written as a matrix this is $J^{\mathsf T}\nabla f$,
and in scalar form it is the ordinary chain rule repeated.

**Definition.** For $g : \mathbb{R}^m \to \mathbb{R}^n$, the *Jacobian* is the $n \times m$
matrix

$$J_g(x) = \left[\frac{\partial g_i}{\partial x_j}(x)\right]_{i,j}.$$

When $n = 1$ the Jacobian is the gradient written as a row vector; that is why the two
notions are the same object.

**Definition.** For a vector field $F : \mathbb{R}^3 \to \mathbb{R}^3$,

$$\text{div}\, F = \frac{\partial F_1}{\partial x} + \frac{\partial F_2}{\partial y} + \frac{\partial F_3}{\partial z},
\qquad
\text{curl}\, F = \left(\frac{\partial F_3}{\partial y} - \frac{\partial F_2}{\partial z},\; \frac{\partial F_1}{\partial z} - \frac{\partial F_3}{\partial x},\; \frac{\partial F_2}{\partial x} - \frac{\partial F_1}{\partial y}\right).$$

*Explanation.* Divergence is net outflow per unit volume. Curl is local rotation. Positive
divergence means fluid expands out of a small ball; non-zero curl means it swirls.

**Theorem (curl of a gradient).** $\text{curl}(\nabla f) = 0$ wherever $f$ is twice
continuously differentiable.

*Explanation.* Mixed partials commute: $\frac{\partial^2 f}{\partial y \partial x} =
\frac{\partial^2 f}{\partial x \partial y}$, so the terms cancel in pairs. The condition is
not cosmetic — it fails for fields with a "memory" of path, which is what makes
non-conservative force fields (magnetic fields, friction) different from gradients.

**Definition.** $f$ is *Lipschitz* with constant $L$ on a convex set if
$\|\nabla f(x) - \nabla f(y)\| \le L\|x-y\|$. For a quadratic $f$ the Lipschitz constant of
$\nabla f$ is the largest absolute eigenvalue of the Hessian.

**Theorem (Gradient descent stability).** For $f$ with $L$-Lipschitz gradient, the
iteration $x_{k+1} = x_k - \eta\nabla f(x_k)$ converges when $\eta < 2/L$ and diverges in
general when $\eta > 2/L$.

*Explanation.* This is the single most important number in deep learning. On
$f = (x-3)^2 + 4(y+1)^2$ the largest curvature is $8$, so $L = 8$ and the stability
threshold is $\eta = 0.25$. The code below finds exactly that boundary.

---

## Worked Example

### Example 1: partial derivatives of $f(x,y) = x^2 + 3xy + y^2$

**With respect to $x$**, treat $y$ as a constant:

$$\frac{\partial f}{\partial x} = 2x + 3y \quad (y^2 \text{ is constant; } 3xy \to 3y)$$

**With respect to $y$**, treat $x$ as a constant:

$$\frac{\partial f}{\partial y} = 3x + 2y$$

At $(1, 2)$: $\nabla f = (2 + 6,\; 3 + 4) = (8, 7)$, with
$\|\nabla f\| = \sqrt{64 + 49} = \sqrt{113} = 10.6301$. The steepest-ascent unit direction is
$(8, 7)/10.6301 = (0.7526, 0.6585)$.

### Example 2: the gradient really is the steepest direction

At $(1, 2)$, measure $f$ a distance `0.01` along several unit directions:

| direction | $\nabla f \cdot u$ | measured $(f(x + 0.01u) - f(x))/0.01$ |
| --- | --- | --- |
| $(1, 0)$ | 8.000000 | 8.010000 |
| $(0.9397, 0.3420)$ | 9.911682 | 9.931324 |
| $(0.6000, 0.8000)$ | **10.400000** | 10.424400 |
| $(0.7660, 0.6428)$ | **10.627869** | 10.652641 |
| $(0, 1)$ | 7.000000 | 7.010000 |

The direction $(0.7526, 0.6585)$ — the unit gradient — gives the largest value,
$\|\nabla f\| = 10.6301$, and every other direction gives less. That is Cauchy–Schwarz in
action, and the table confirms it numerically.

### Example 3: why gradient descent cuts across contours

The level set through $(1,2)$ is $f = 11$. Take a tangent direction by rotating the
gradient: $t = (-7, 8)/\sqrt{113} = (-0.6585, 0.7526)$. Then

$$\nabla f \cdot t = 8(-0.6585) + 7(0.7526) = -5.268 + 5.268 = 0.$$

Moving along $t$ leaves $f$ unchanged to seven digits: $f$ goes from `11.000000000` to
`10.999999513`. Moving along the gradient by `0.001` instead gives $f = 11.008$. So the
gradient is precisely *perpendicular* to the level curve, and descending it means crossing
contours head-on rather than sliding along them. This is why gradient descent zigzags on
an elongated valley: it goes straight down the steep wall and barely moves along the floor.

### Example 4: the chain rule, with two links

Let $u = 3x - 2y$ and $L = u^2$. At $(x,y) = (1.5, 0.5)$:

1. $u = 3(1.5) - 2(0.5) = 4.5 - 1 = 3.5$, so $L = 12.25$.
2. $\frac{\partial L}{\partial u} = 2u = 7$.
3. $\frac{\partial u}{\partial x} = 3$, $\frac{\partial u}{\partial y} = -2$.
4. Multiply: $\frac{\partial L}{\partial x} = 7 \cdot 3 = 21$ and
   $\frac{\partial L}{\partial y} = 7 \cdot (-2) = -14$.

Numerical central differences give `20.999999997` and `-14.000000000`. In code, `L` is
computed as a single expression of `x` and `y`; the two partials come from differentiating
one layer at a time. That is the whole multivariable chain rule — the same object as the
one-dimensional version, just with more links.

### Example 5: curl of a gradient is zero

Take $F = (x, 2y)$.

- $\text{div} F = \frac{\partial x}{\partial x} + \frac{\partial 2y}{\partial y} = 1 + 2 = 3$.
  Positive: a small ball around $(1,2)$ has more field leaving it than entering, so the
  "fluid" expands.
- $\text{curl} F = (\frac{\partial F_3}{\partial y} - \frac{\partial F_2}{\partial z},\; \frac{\partial F_1}{\partial z} - \frac{\partial F_3}{\partial x},\; \frac{\partial F_2}{\partial x} - \frac{\partial F_1}{\partial y}) = (0 - 0,\; 0 - 0,\; 0 - 1) = (0,0,-1)$.
  Non-zero: the field rotates clockwise about the $z$-axis.
- But $F = \nabla(x^2/2 + y^2)$, and $\text{curl}(\nabla f) = 0$ for any twice-differentiable
  $f$. Computing directly: $\frac{\partial}{\partial y}(2x+3y) - \frac{\partial}{\partial x}(3x+2y)
  = 3 - 3 = 0$. ✓

This is not trivia. "The gradient of a loss has zero curl" is the condition that lets you
exchange a backpropagation pass with an adjoint pass and get the same answer, which is the
entire basis of adjoint methods.

---

## Runnable Code

### Block 1: partials, the gradient, Jacobians, divergence and curl

```python
import math


def vec_sub(u, v):
    return [a - b for a, b in zip(u, v)]


def vec_add(u, v):
    return [a + b for a, b in zip(u, v)]


def vec_scale(c, u):
    return [c * a for a in u]


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def norm(u):
    return math.sqrt(dot(u, u))


print("=== Partial derivatives: a slope that depends on where you look ===")
#  f(x, y) = x^2 + 3xy + y^2.  df/dx = 2x + 3y,  df/dy = 3x + 2y.
f = lambda x, y: x * x + 3 * x * y + y * y
H = 1e-6


def central_partial(g, x, y, axis, h=H):
    """One partial derivative, by central difference along one axis only."""
    if axis == 0:
        return (g(x + h, y) - g(x - h, y)) / (2 * h)
    return (g(x, y + h) - g(x, y - h)) / (2 * h)


print("  f(x,y) = x^2 + 3xy + y^2,   df/dx = 2x + 3y,   df/dy = 3x + 2y")
print("      x      y       df/dx num      df/dx exact    df/dy num      df/dy exact")
for x, y in ((1.0, 2.0), (3.0, -1.0), (-2.0, 0.5)):
    print(f"  {x:>5}  {y:>6}  {central_partial(f, x, y, 0):>13.9f}  {2 * x + 3 * y:>12.6f}"
          f"  {central_partial(f, x, y, 1):>13.9f}  {3 * x + 2 * y:>12.6f}")
print("  Holding the other coordinate fixed is what makes it a PARTIAL derivative.")
print()

print("=== The gradient, and why it points uphill ===")
#  grad f = (df/dx, df/dy).  The directional derivative along a UNIT vector u is
#  D_u f = grad f . u, maximised when u = grad f / ||grad f||.
x0, y0 = 1.0, 2.0
grad = (2 * x0 + 3 * y0, 3 * x0 + 2 * y0)
g_norm = norm(grad)
unit = [g / g_norm for g in grad]
print(f"  at ({x0}, {y0}): grad f = ({grad[0]:.1f}, {grad[1]:.1f}),  ||grad f|| = {g_norm:.6f}")
print(f"  unit steepest-ascent direction = ({unit[0]:.6f}, {unit[1]:.6f})")
print()
print("  Directional derivative along a unit vector u:   df/du = grad f . u")
print("      u (angle)             dot product     f(x+0.01u) - f(x)")
for angle_deg in (0, 20, 40, 53.130102, 70, 90, 126.869898):
    a = math.radians(angle_deg)
    u = [math.cos(a), math.sin(a)]
    d_dot = dot(grad, u)
    step = f(x0 + 0.01 * u[0], y0 + 0.01 * u[1]) - f(x0, y0)
    mark = "  <- steepest" if abs(angle_deg - 53.130102) < 1e-3 else ""
    print(f"  ({u[0]:>7.4f},{u[1]:>7.4f}) {d_dot:>13.6f}   {step / 0.01:>18.6f}{mark}")
print("  The dot product is largest exactly where u equals the unit gradient,")
print("  Cauchy-Schwarz guarantees that: grad.u <= ||grad|| ||u|| = ||grad||.")
print()

print("=== Perpendicularity: a level set has the gradient as its normal ===")
#  Moving ALONG the level set f = c leaves f unchanged, so the gradient is perpendicular.
print(f"  level set through ({x0}, {y0}): x^2 + 3xy + y^2 = {f(x0, y0):.1f}")
tangent = [-unit[1], unit[0]]      # rotate the gradient direction by 90 degrees
print(f"  gradient (normal)  = ({grad[0]:.4f}, {grad[1]:.4f})")
print(f"  along the tangent  = ({tangent[0]:.4f}, {tangent[1]:.4f})")
print(f"  their dot product  = {dot(grad, tangent):.2e}   (exactly zero)")
before = f(x0, y0)
after = f(x0 + 0.001 * tangent[0], y0 + 0.001 * tangent[1])
print(f"  f before = {before:.9f}   f after moving along it = {after:.9f}")
print("  This is why gradient descent walks across contours and never along one.")
print()

print("=== The multivariable chain rule is still just the chain rule ===")
#  u = a*x + b*y ;  L = u^2.   dL/dx = 2u * a,  dL/dy = 2u * b.
a, b = 3.0, -2.0
x, y = 1.5, 0.5
u = a * x + b * y
L = u * u
print(f"  u = {a}x + {b}y,  L = u^2,  at (x,y) = ({x}, {y})")
print(f"  u = {u:.6f},  L = {L:.6f}")
print(f"  dL/dx = 2u * a = 2 * {u:.4f} * {a} = {2 * u * a:.6f}")
print(f"  dL/dy = 2u * b = 2 * {u:.4f} * {b} = {2 * u * b:.6f}")
L_of = lambda px, py: (a * px + b * py) ** 2
print(f"  numeric dL/dx = {central_partial(L_of, x, y, 0):.9f}")
print(f"  numeric dL/dy = {central_partial(L_of, x, y, 1):.9f}")
print()

print("=== Jacobians: the gradient is the Jacobian when the output is scalar ===")
#  For a vector output, the Jacobian is a matrix of all partials.
#  Rotation by theta: J = [[cos, -sin], [sin, cos]], and J^T J = I.
theta = math.radians(30.0)
J = [[math.cos(theta), -math.sin(theta)],
     [math.sin(theta), math.cos(theta)]]


def matvec(m, v):
    return [row[0] * v[0] + row[1] * v[1] for row in m]


def matmul(a_, b_):
    return [[sum(a_[i][k] * b_[k][j] for k in range(2)) for j in range(2)]
            for i in range(2)]


def transpose(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]


v = [1.0, 0.0]
print(f"  rotation by {math.degrees(theta):.0f} degrees")
print(f"    J = [[{J[0][0]:>8.5f}, {J[0][1]:>8.5f}], [{J[1][0]:>8.5f}, {J[1][1]:>8.5f}]]")
rotated = matvec(J, v)
print(f"    J @ (1, 0) = ({rotated[0]:.6f}, {rotated[1]:.6f})  "
      f"(length {norm(rotated):.6f}, unchanged)")
JtJ = matmul(transpose(J), J)
print(f"    J^T J = [[{JtJ[0][0]:.6f}, {JtJ[0][1]:.6f}], "
      f"[{JtJ[1][0]:.6f}, {JtJ[1][1]:.6f}]]  -- the identity, so rotations preserve length")
print()

print("=== Divergence and curl, briefly ===")
#  For a vector FIELD F, divergence measures net outflow, curl measures local spin.
#  For a scalar potential f with F = grad f, the curl is identically zero.
F = [x0 * 1.0, y0 * 2.0]     # F = (x, 2y) at our point
div = 1.0 + 2.0              # dF1/dx + dF2/dy = 1 + 2
curl = 0.0 - 1.0             # dF2/dx - dF1/dy = 0 - 1
print(f"  F = (x, 2y);  at ({x0}, {y0}): F = ({F[0]:.1f}, {F[1]:.1f})")
print(f"    div F = dF1/dx + dF2/dy = 1 + 2 = {div}")
print("      positive -> more fluid leaves a small ball than enters it")
print(f"    curl F = dF2/dx - dF1/dy = 0 - 1 = {curl}")
print("      negative -> the field circulates clockwise around the z axis")
curl_of_grad = 3.0 - 3.0     # d/dy (2x+3y) - d/dx (3x+2y) = 3 - 3
print(f"    curl(grad f) = {curl_of_grad}  -- gradients have zero curl. Always.")
print("    This is the condition a neural network's backward pass relies on.")
```

Output:

```text
=== Partial derivatives: a slope that depends on where you look ===
  f(x,y) = x^2 + 3xy + y^2,   df/dx = 2x + 3y,   df/dy = 3x + 2y
      x      y       df/dx num      df/dx exact    df/dy num      df/dy exact
    1.0     2.0    7.999999999      8.000000    7.000000000      7.000000
    3.0    -1.0    3.000000001      3.000000    6.999999999      7.000000
   -2.0     0.5   -2.500000000     -2.500000   -5.000000000     -5.000000
  Holding the other coordinate fixed is what makes it a PARTIAL derivative.

=== The gradient, and why it points uphill ===
  at (1.0, 2.0): grad f = (8.0, 7.0),  ||grad f|| = 10.630146
  unit steepest-ascent direction = (0.752577, 0.658505)

  Directional derivative along a unit vector u:   df/du = grad f . u
      u (angle)             dot product     f(x+0.01u) - f(x)
  ( 1.0000, 0.0000)      8.000000             8.010000
  ( 0.9397, 0.3420)      9.911682             9.931324
  ( 0.7660, 0.6428)     10.627869            10.652641
  ( 0.6000, 0.8000)     10.400000            10.424400  <- steepest
  ( 0.3420, 0.9397)      9.314009             9.333651
  ( 0.0000, 1.0000)      7.000000             7.010000
  (-0.6000, 0.8000)      0.800000             0.795600
  The dot product is largest exactly where u equals the unit gradient,
  Cauchy-Schwarz guarantees that: grad.u <= ||grad|| ||u|| = ||grad||.

=== Perpendicularity: a level set has the gradient as its normal ===
  level set through (1.0, 2.0): x^2 + 3xy + y^2 = 11.0
  gradient (normal)  = (8.0000, 7.0000)
  along the tangent  = (-0.6585, 0.7526)
  their dot product  = 0.00e+00   (exactly zero)
  f before = 11.000000000   f after moving along it = 10.999999513
  This is why gradient descent walks across contours and never along one.

=== The multivariable chain rule is still just the chain rule ===
  u = 3.0x + -2.0y,  L = u^2,  at (x,y) = (1.5, 0.5)
  u = 3.500000,  L = 12.250000
  dL/dx = 2u * a = 2 * 3.5000 * 3.0 = 21.000000
  dL/dy = 2u * b = 2 * 3.5000 * -2.0 = -14.000000
  numeric dL/dx = 20.999999997
  numeric dL/dy = -14.000000000

=== Jacobians: the gradient is the Jacobian when the output is scalar ===
  rotation by 30 degrees
    J = [[ 0.86603, -0.50000], [ 0.50000,  0.86603]]
    J @ (1, 0) = (0.866025, 0.500000)  (length 1.000000, unchanged)
    J^T J = [[1.000000, 0.000000], [0.000000, 1.000000]]  -- the identity, so rotations preserve length

=== Divergence and curl, briefly ===
  F = (x, 2y);  at (1.0, 2.0): F = (1.0, 4.0)
    div F = dF1/dx + dF2/dy = 1 + 2 = 3.0
      positive -> more fluid leaves a small ball than enters it
    curl F = dF2/dx - dF1/dy = 0 - 1 = -1.0
      negative -> the field circulates clockwise around the z axis
    curl(grad f) = 0.0  -- gradients have zero curl. Always.
    This is the condition a neural network's backward pass relies on.
```

### Block 2: gradient descent, step sizes, and direction search

```python
import math

print("=== 1. Gradient descent on a convex quadratic: it works ===")
#  f(x,y) = (x-3)^2 + 4(y+1)^2.  Convex, so descent converges to (3, -1).
#  Deliberately anisotropic: curvature 1 along x, curvature 4 along y.  Real
#  problems have this property too, and it is why one learning rate is awkward.


def f(x, y):
    return (x - 3.0) ** 2 + 4.0 * (y + 1.0) ** 2


def grad(x, y):
    return (2 * (x - 3.0), 8.0 * (y + 1.0))


def norm(u):
    return math.hypot(u[0], u[1])


def gradient_descent(f, grad, start, step_size, steps=200, tol=1e-12, limit=1e100):
    """The canonical loop. Every line of it is the lesson 51 chain rule.

    `limit` is a divergence guard. Real code needs one too: without it, an
    exploding gradient quietly produces inf, then nan, then nonsense."""
    x, y = start
    for _ in range(steps):
        gx, gy = grad(x, y)
        if norm((gx, gy)) < tol:            # stopping criterion: gradient is small
            break
        x = x - step_size * gx                # move DOWNHILL: subtract the gradient
        y = y - step_size * gy
        if not math.isfinite(x) or abs(f(x, y)) > limit:
            return float("inf"), float("inf")
    return x, y


def run_and_count(lr, start=(0.0, 5.0), steps=200, tol=1e-12, limit=1e100):
    """Same loop, but also report how many steps it actually took."""
    x, y = start
    for k in range(steps):
        gx, gy = grad(x, y)
        if norm((gx, gy)) < tol:
            return x, y, k
        x, y = x - lr * gx, y - lr * gy
        if not math.isfinite(x) or abs(f(x, y)) > limit:
            return float("inf"), float("inf"), steps
    return x, y, steps


print("  f(x,y) = (x-3)^2 + 4(y+1)^2,  grad f = (2(x-3), 8(y+1)),  minimum at (3, -1)")
print()
print("   step size          final (x, y)            f        ||grad||   steps")
for lr in (0.05, 0.1, 0.2, 0.24, 0.25, 0.26, 0.5, 1.0):
    x, y, count = run_and_count(lr)
    if math.isinf(x):
        print(f"  {lr:>10}   {'diverged to infinity':>34}")
    else:
        print(f"  {lr:>10}   ({x:>10.6f}, {y:>10.6f})   {f(x, y):>10.2e}   "
              f"{norm(grad(x, y)):.2e}  {count:>5}")
print("  Stable below lr = 0.25, because the largest curvature is 8 and the")
print("  condition is lr < 2/8.  Above it the iteration oscillates or diverges,")
print("  which is exactly what an untuned learning rate does in real training.")
print()

print("  Watch the iteration approach, step by step, at lr = 0.2:")
px, py = 0.0, 5.0
print("        k          x            y            f")
for k in range(1, 26):
    gx, gy = grad(px, py)
    px, py = px - 0.2 * gx, py - 0.2 * gy
    if k <= 6 or k % 5 == 0:
        print(f"  {k:>5}  {px:>11.7f}  {py:>11.7f}  {f(px, py):>12.3e}")
print("  Each coordinate shrinks by a different factor: x by (1 - 0.2*2) = 0.6,")
print("  y by (1 - 0.2*8) = -0.6.  The SLOW coordinate (x) sets the overall rate,")
print("  which is why elongated valleys slow gradient descent down so much.")
print()

print("=== 2. A non-convex function: descent can run away ===")
#  f(x,y) = x^2 + 3xy + y^2 has Hessian eigenvalues 5 and -1.  It is unbounded
#  below, so descending eventually means heading for infinity.


def f2(x, y):
    return x * x + 3 * x * y + y * y


def grad2(x, y):
    return (2 * x + 3 * y, 3 * x + 2 * y)


def run2(step_size, steps, limit=1e12):
    x, y = 1.0, 2.0
    for _ in range(steps):
        gx, gy = grad2(x, y)
        x, y = x - step_size * gx, y - step_size * gy
        if not math.isfinite(f2(x, y)) or abs(f2(x, y)) > limit:
            return float("inf"), float("inf")
    return x, y


print("  f(x,y) = x^2 + 3xy + y^2,  grad f = (2x + 3y, 3x + 2y).  Eigenvalues 5 and -1.")
print("   step size   after 200 steps                f            verdict")
for lr in (0.001, 0.01, 0.1, 0.3):
    x, y = run2(lr, 200)
    if math.isinf(x):
        print(f"  {lr:>10}   {'escaped past |f| > 1e12':>38}  DIVERGED")
    else:
        note = "at the saddle (0,0)" if abs(f2(x, y)) < 10 else "RUNNING AWAY"
        print(f"  {lr:>10}   ({x:>9.4f}, {y:>9.4f})   {f2(x, y):>13.4f}   {note}")
print("  The origin is only a SADDLE.  Head along y = -x and f = -x^2 falls")
print("  without limit, so 'keep lowering f' has no floor to hit.")
print("  Nothing goes wrong at lr = 0.001; everything is fine until it is not.")
print()

print("=== 3. One learning rate cannot fit a whole loss landscape ===")
print("  The gradient's MAGNITUDE varies by orders of magnitude, so a single")
print("  step size either crawls in flat regions or explodes in steep ones.")
print()
print("     f(x)          f'(0.1)      lr that moves 0.01 in one step")
for name, d in (("x^4", 4 * 0.1 ** 3),
                ("exp(3x)", 3 * math.exp(0.3)),
                ("sin(10x)", 10 * math.cos(1.0)),
                ("log(1+x^2) at 0.1", 0.2 / 1.01)):
    needed = 0.01 / abs(d)
    print(f"  {name:<18} {d:>10.6f}      {needed:>12.4f}")
print("  The required step spans three orders of magnitude.  Adam, Adagrad and")
print("  RMSProp all exist to fix this by dividing by a running RMS of the gradient.")
print()

print("=== 4. Direction search: steer toward a target by following a gradient ===")
#  The gradient of (x - tx)^2 + (y - ty)^2 is 2*(x - tx, y - ty): it points
#  straight at the target.  This is the loop behind ray marching and PID control.
target = (0.7, -0.3)
x, y = 1.0, 2.0
step = 0.1
path = [(x, y)]
for _ in range(200):
    gx = 2.0 * (x - target[0])
    gy = 2.0 * (y - target[1])
    if math.hypot(gx, gy) < 1e-14:
        break
    x, y = x - step * gx, y - step * gy
    path.append((x, y))
print(f"  aiming at {target}, started at (1.0, 2.0), step 0.1")
print("   step          x             y        distance to target")
for k in (1, 5, 10, 20, 40, 60, len(path) - 1):
    if k < len(path):
        px, py = path[k]
        print(f"  {k:>5}  {px:>11.7f}  {py:>11.7f}   {math.hypot(px - target[0], py - target[1]):.3e}")
start_dist = math.hypot(1.0 - target[0], 2.0 - target[1])
end_dist = math.hypot(path[-1][0] - target[0], path[-1][1] - target[1])
print(f"  Distance fell from {start_dist:.3f} to {end_dist:.3e} in {len(path) - 1} steps,")
print("  a factor of exactly 0.8 each step -- which is why linear convergence is")
print("  slow and why Newton's method (lesson 54) is worth the extra arithmetic.")
```

Output:

```text
=== 1. Gradient descent on a convex quadratic: it works ===
  f(x,y) = (x-3)^2 + 4(y+1)^2,  grad f = (2(x-3), 8(y+1)),  minimum at (3, -1)

   step size          final (x, y)            f        ||grad||   steps
        0.05   (  3.000000,  -1.000000)     4.48e-18   4.23e-09    200
         0.1   (  3.000000,  -1.000000)     2.34e-25   9.68e-13    132
         0.2   (  3.000000,  -1.000000)     4.73e-26   8.50e-13     62
        0.24   (  3.000000,  -1.000000)     4.72e-13   2.75e-06    200
        0.25   (  3.000000,   5.000000)     1.44e+02   4.80e+01    200
        0.26   (  3.000000, 29033696.509402)     3.37e+15   2.32e+08    200
         0.5                 diverged to infinity
         1.0                 diverged to infinity
  Stable below lr = 0.25, because the largest curvature is 8 and the
  condition is lr < 2/8.  Above it the iteration oscillates or diverges,
  which is exactly what an untuned learning rate does in real training.

  Watch the iteration approach, step by step, at lr = 0.2:
        k          x            y            f
      1    1.2000000   -4.6000000     5.508e+01
      2    1.9200000    1.1600000     1.983e+01
      3    2.3520000   -2.2960000     7.138e+00
      4    2.6112000   -0.2224000     2.570e+00
      5    2.7667200   -1.4665600     9.251e-01
      6    2.8600320   -0.7200640     3.330e-01
     10    2.9818601   -0.9637203     5.594e-03
     15    2.9985894   -1.0028211     3.382e-05
     20    2.9998903   -0.9997806     2.045e-07
     25    2.9999915   -1.0000171     1.237e-09
  Each coordinate shrinks by a different factor: x by (1 - 0.2*2) = 0.6,
  y by (1 - 0.2*8) = -0.6.  The SLOW coordinate (x) sets the overall rate,
  which is why elongated valleys slow gradient descent down so much.

=== 2. A non-convex function: descent can run away ===
  f(x,y) = x^2 + 3xy + y^2,  grad f = (2x + 3y, 3x + 2y).  Eigenvalues 5 and -1.
   step size   after 200 steps                f            verdict
       0.001   (  -0.0602,    1.1611)          1.1420   at the saddle (0,0)
        0.01   (  -3.6580,    3.6581)        -13.3810   RUNNING AWAY
         0.1                  escaped past |f| > 1e12  DIVERGED
         0.3                  escaped past |f| > 1e12  DIVERGED
  The origin is only a SADDLE.  Head along y = -x and f = -x^2 falls
  without limit, so 'keep lowering f' has no floor to hit.
  Nothing goes wrong at lr = 0.001; everything is fine until it is not.

=== 3. One learning rate cannot fit a whole loss landscape ===
  The gradient's MAGNITUDE varies by orders of magnitude, so a single
  step size either crawls in flat regions or explodes in steep ones.

     f(x)          f'(0.1)      lr that moves 0.01 in one step
  x^4                  0.004000            2.5000
  exp(3x)              4.049576            0.0025
  sin(10x)             5.403023            0.0019
  log(1+x^2) at 0.1    0.198020            0.0505
  The required step spans three orders of magnitude.  Adam, Adagrad and
  RMSProp all exist to fix this by dividing by a running RMS of the gradient.

=== 4. Direction search: steer toward a target by following a gradient ===
  aiming at (0.7, -0.3), started at (1.0, 2.0), step 0.1
   step          x             y        distance to target
      1    0.9400000    1.5400000   1.856e+00
      5    0.7983040    0.4536640   7.600e-01
     10    0.7322123   -0.0530394   2.491e-01
     20    0.7034588   -0.2734828   2.674e-02
     40    0.7000399   -0.2996943   3.083e-04
     60    0.7000005   -0.2999965   3.555e-06
    152    0.7000000   -0.3000000   4.310e-15
  Distance fell from 2.319 to 4.310e-15 in 152 steps,
  a factor of exactly 0.8 each step -- which is why linear convergence is
  slow and why Newton's method (lesson 54) is worth the extra arithmetic.
```

The `lr = 0.25` row is worth staring at. The $x$ coordinate converges perfectly
(`3.000000`) while the $y$ coordinate oscillates between `-1` and `5` forever, because
$1 - 0.25 \cdot 8 = -1$ exactly — a marginal case with no damping at all. Real code must
handle that case explicitly, which is why every practical optimiser includes either a
clip, a backtracking line search, or an adaptive rule.

---

### With Libraries

The picture worth having in your head is a contour plot with the gradient field drawn on
it. Everything above becomes obvious when you see it.

```python
# Requires numpy + matplotlib; not runnable with the standard library alone.
import matplotlib
matplotlib.use("Agg")          # so the script runs without a display
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))

# 1. Contour plot with the gradient field: arrows perpendicular to the contours.
X, Y = np.meshgrid(np.linspace(-2, 6, 31), np.linspace(-4, 2, 31))
F = (X - 3) ** 2 + 4 * (Y + 1) ** 2
U, V = 2 * (X - 3), 8 * (Y + 1)
axes[0].contour(X, Y, F, levels=np.logspace(0, 3, 12), colors="grey", linewidths=0.6)
axes[0].quiver(X, Y, U, V, color="tab:blue", scale=250)
axes[0].plot(3, -1, "r*", markersize=14)
axes[0].set_title("Contours of f; gradient arrows cross them at right angles")
axes[0].set_xlabel("gradient arrows all point at (3, -1)")

# 2. What a step size does.  Same problem, different learning rates.
def descend(lr, steps=60):
    p = np.array([0.0, 5.0])
    path = [p.copy()]
    for _ in range(steps):
        g = np.array([2 * (p[0] - 3), 8 * (p[1] + 1)])
        if np.linalg.norm(g) < 1e-12:
            break
        p = p - lr * g
        if not np.isfinite(p).all() or np.linalg.norm(p) > 1e6:
            break
        path.append(p.copy())
    return np.array(path)


for lr, colour in ((0.05, "tab:green"), (0.2, "tab:orange"), (0.24, "tab:purple"),
                   (0.26, "tab:red")):
    path = descend(lr)
    axes[1].plot(path[:, 0], path[:, 1], "-o", markersize=2, color=colour,
                 label=f"lr = {lr}")
axes[1].plot(3, -1, "k*", markersize=14)
axes[1].set_title("Same start, different step size")
axes[1].legend(fontsize=7)
axes[1].set_xlim(-4, 6)
axes[1].set_ylim(-6, 6)

# 3. Steepest descent vs Newton's method on the same quadratic.
def newton(x, y, steps=6):
    p = np.array([x, y])
    path = [p.copy()]
    for _ in range(steps):
        g = np.array([2 * (p[0] - 3), 8 * (p[1] + 1)])
        H = np.diag([2.0, 8.0])              # the Hessian of this quadratic
        step = np.linalg.solve(H, g)
        p = p - step
        path.append(p.copy())
    return np.array(path)


sd = descend(0.2, 60)
nt = newton(0.0, 5.0)
axes[2].plot(sd[:, 0], sd[:, 1], "-", color="tab:orange", label="gradient descent (60 steps)")
axes[2].plot(nt[:, 0], nt[:, 1], "o-", color="tab:green", label="Newton (6 steps)")
axes[2].plot(3, -1, "k*", markersize=14)
axes[2].set_title("Quadratic: Newton lands exactly, descent creeps")
axes[2].legend(fontsize=7)

plt.tight_layout()
plt.savefig("lesson53_multivariable.png", dpi=110)
print("wrote lesson53_multivariable.png")

# How many gradient-descent steps to reach the same accuracy Newton gets in 6?
target = np.array([3.0, -1.0])
p = np.array([0.0, 5.0])
needed = None
for k in range(1, 100000):
    p = p - 0.2 * np.array([2 * (p[0] - 3), 8 * (p[1] + 1)])
    if np.linalg.norm(p - target) < 1e-10:
        needed = k
        break
nt_err = np.linalg.norm(newton(0.0, 5.0)[-1] - target)
print(f"  gradient descent at lr=0.2 needs {needed} steps to reach distance 1e-10")
print(f"  Newton needs 6 steps and lands at distance {nt_err:.1e}")
print("  On a quadratic the Newton step is exact in one shot per coordinate, which")
print("  is why Newton-type methods dominate for least squares and root finding.")
plt.close(fig)
```

```text
wrote lesson53_multivariable.png
  gradient descent at lr=0.2 needs 49 steps to reach distance 1e-10
  Newton needs 6 steps and lands at distance 0.0e+00
  On a quadratic the Newton step is exact in one shot per coordinate, which
  is why Newton-type methods dominate for least squares and root finding.
```

Look at the left panel: the arrows are long where the contours are close together and
short where they are far apart. That length is exactly $\|\nabla f\|$, the rate of change.
Look at the middle panel: `lr = 0.26` (red) is already off the edge of the plot after
sixty steps, while `lr = 0.2` (orange) arrives comfortably. One order-of-magnitude
difference in a number you probably set by guessing.

---

## Common Mistakes

**Mistake 1 — forgetting the cross term when taking a partial derivative.**

```python
import math

# WRONG: treats y as a constant while differentiating with respect to x, but then
# also assumes df/dy has no x in it. One of the two is always wrong.
f = lambda x, y: x * x + 3 * x * y + y * y
dfdx_WRONG = lambda x, y: 2 * x          # forgot the 3y from d/dx (3xy)
dfdx_RIGHT = lambda x, y: 2 * x + 3 * y
print(f"  df/dx wrong = {dfdx_WRONG(1.0, 2.0):.4f},  right = {dfdx_RIGHT(1.0, 2.0):.4f}")
```

The tempting version is attractive because the cross term does not depend on `x` *as a
function of x alone* — but it does depend on the parameter `y`, and `y` is a coordinate,
not a constant. Any `+ c*x*y` term must appear in both partials.

**Mistake 2 — assuming the gradient points at the minimum.**

```python
import math

# A saddle is a critical point where the function falls in one direction
# and rises in another.  The gradient is zero there too, so "grad is zero"
# does NOT mean "we found the answer".
f = lambda x, y: x * x + 3 * x * y + y * y
print(f"  grad f(0,0) = ({0.0}, {0.0})  -- zero gradient")
print(f"  f(0.01, 0)   = {f(0.01, 0.0):+.6f}  -> going right, we go UP")
print(f"  f(0, -0.01)  = {f(0.0, -0.01):+.6f} -> going down, we go DOWN")
print(f"  f(-0.01, 0.01) = {f(-0.01, 0.01):+.6f} -> falling the other way too")
print("  Zero gradient, no minimum. This is why optimisers need a convexity")
print("  assumption, restarts, or both.")
```

The wrong mental model — "gradient descent descends, so it must be finding a minimum" — is
the source of nearly every "my training diverged" mystery.

**Mistake 3 — normalising the gradient and then using a large step size.**

```python
import math


def f(x, y):
    return (x - 3.0) ** 2 + 4.0 * (y + 1.0) ** 2


def grad(x, y):
    return (2 * (x - 3.0), 8.0 * (y + 1.0))


# WRONG: normalising divides by ||grad||, which is huge in steep regions and
# tiny in flat ones, so a fixed step size becomes wildly non-uniform.
def descent_wrong(start, step_size, steps=40):
    x, y = start
    for _ in range(steps):
        gx, gy = grad(x, y)
        n = math.hypot(gx, gy) or 1.0
        x, y = x - step_size * gx / n, y - step_size * gy / n
    return x, y


# RIGHT: clip the NORM instead of dividing by it.  The direction is preserved
# exactly where the gradient is large, and the step is capped everywhere.
def descent_right(start, step_size, clip=1.0, steps=40):
    x, y = start
    for _ in range(steps):
        gx, gy = grad(x, y)
        n = math.hypot(gx, gy)
        scale = step_size if n <= clip else clip / n
        x, y = x - scale * gx, y - scale * gy
    return x, y


for name, fn in (("normalise", descent_wrong), ("clip", descent_right)):
    x, y = fn((0.0, 5.0), 0.1)
    print(f"  {name:<10} (x,y) = ({x:>10.5f}, {y:>10.5f})   f = {f(x, y):.3e}")
```

Gradient clipping is in `torch.nn.utils.clip_grad_norm_` and it is the standard fix for
loss spikes. Normalising by the norm — the tempting fix — discards exactly the information
that tells you a region is steep.

**Mistake 4 — confusing the Jacobian with the transpose.**

```python
import math


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)]
            for i in range(2)]


def transpose(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]


a = [[1.0, 2.0], [3.0, 4.0]]
print(f"  A     = {a}")
print(f"  A^T   = {transpose(a)}")
print(f"  A A^T = {matmul(a, transpose(a))}")
print("  These are all different. Backprop multiplies by J^T on the way back,")
print("  which is the transpose -- getting this wrong gives wrong shapes or")
print("  silently transposed gradients, and never a shape error in plain lists.")
```

**Mistake 5 — writing a descent loop with no stopping criterion and no cap.**

```python
import math


def f(x, y):
    return (x - 3.0) ** 2 + 4.0 * (y + 1.0) ** 2


def grad(x, y):
    return (2 * (x - 3.0), 8.0 * (y + 1.0))


# WRONG: no cap, no tolerance, no check for divergence.
x, y = 0.0, 5.0
for _ in range(50):
    gx, gy = grad(x, y)
    x, y = x - 0.26 * gx, y - 0.26 * gy
print(f"  50 steps at lr=0.26 from (0,5):  x = {x:.4e},  f = {f(x, y):.4e}")

# RIGHT: cap the steps, stop when the gradient is small, and refuse to return
# a value that has blown up.  Every production optimiser has all three.
x, y = 0.0, 5.0
for k in range(50):
    gx, gy = grad(x, y)
    if math.hypot(gx, gy) < 1e-12:
        break
    x, y = x - 0.2 * gx, y - 0.2 * gy
    if not math.isfinite(f(x, y)):
        break
print(f"  same problem at lr=0.2:          x = {x:.10f},  f = {f(x, y):.3e}")
print("  One number changed from 0.26 to 0.2 and the result went from infinity")
print("  to exact. Always say what your step size is and why.")
```

---

## Formula Sheet

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$\partial f/\partial x_i(a)$` | `$\lim_{h\to0}\frac{f(a+he_i)-f(a)}{h}$`; $f$ must be defined on a neighbourhood | hold every coordinate but one fixed, take the ordinary one-variable derivative | the entrywise building block of everything below |
| `$\nabla f(a)$` | `$\left(\frac{\partial f}{\partial x_1},\dots,\frac{\partial f}{\partial x_n}\right)(a)$` | all the partials as one vector | the object SGD moves along |
| differentiability | `$f(a+h)=f(a)+\nabla f(a)\cdot h+o(\lVert h\rVert)$` as `$h\to0$` | the function is locally linear plus negligible error | the hypothesis under all the theorems; **stronger** than every partial existing |
| `$\lVert\cdot\rVert$`, `$\cdot$` | dot product and Euclidean norm | multiply-and-add, and square-root-of-sum-of-squares | comparing a gradient with a direction |
| directional derivative | `$D_u f(a)=\lim_{t\to0}\frac{f(a+tu)-f(a)}{t}=\nabla f(a)\cdot u$` — **requires $\lVert u\rVert = 1$** | how fast $f$ grows moving a unit step along $u$ | any "which way is steepest?" question |
| steepest ascent / descent | `$\max_{\lVert u\rVert=1}\nabla f\cdot u=\lVert\nabla f\rVert$` at `$u=\nabla f/\lVert\nabla f\rVert$; the minimum is `$-(\lVert\nabla f\rVert)$` at `$u=-\nabla f/\lVert\nabla f\rVert$` | the single best direction, and the single worst | why gradient descent moves along `$\nabla f$` at all (Cauchy–Schwarz) |
| perpendicularity | `$u$ tangent to `$\{x:f(x)=c\}$` `$\Rightarrow \nabla f\cdot u = 0$` | the gradient is the contour's normal vector | explains zigzagging; gradient descent crosses contours, never follows them |
| Jacobian `$\left[\frac{\partial g_i}{\partial x_j}\right]$` | `$n\times m$ matrix for `$g:\mathbb{R}^m\to\mathbb{R}^n$`; for `$n=1$` it **is** the gradient as a row | the derivative of a vector-valued function | `torch.autograd` backward of a linear layer |
| multivariable chain rule | `$\nabla(f\circ g)(x)=J_g(x)^{\mathsf T}\nabla f(g(x))$` | the transpose of the inner Jacobian times the outer gradient | backprop: one transpose-times-vector per layer |
| scalar form of the chain rule | `$\frac{\partial h}{\partial x_i}=\sum_j\frac{\partial f}{\partial g_j}\frac{\partial g_j}{\partial x_i}$` | sum over every intermediate coordinate | deriving $\nabla(u^2)=2u\,\nabla u$ by hand |
| Jacobian of a linear layer | `$J_{Wx+b}=W$` (the weight matrix itself) | for `y = Wx`, the derivative *is* `$W$` | why backprop is literally a `GEMM` |
| adjoint of a linear layer | `$J^{\mathsf T}\bar{y}$`, one matrix-vector product | the transposed multiply on the way back | Exercise 3(d): `dL/dx = [3.7375, 6.7]` |
| `$\bar{r} = \partial L/\partial r$` for `L=\tfrac12\lVert r\rVert^2` | `$\bar r = r$`; then `$\partial L/\partial W_2 = r\,h^{\mathsf T}$`, `$\partial L/\partial h = W_2^{\mathsf T}r$` | seed the backward pass with the residual | the opening move of every autodiff implementation |
| total differential / first-order expansion | `$f(a+h)=f(a)+\nabla f(a)\cdot h+O(\lVert h\rVert^2)$` | linear prediction, with the remainder written down | any local model; the reason linearisation is *only* local |
| second-order term | `$\tfrac12 h^{\mathsf T}Hh$` with `$H=\nabla^2 f$` | the leading thing you threw away | for the quadratic `$x^2+3xy+y^2$, `err = \tfrac12 d^2\cdot 4.97345` exactly |
| Hessian `$\nabla^2 f$` | for `$x^3+2xy^2-5y$`: `$\begin{pmatrix}6x & 4y\\ 4y & 4x\end{pmatrix}$`, `$\det = 24x^2-16y^2$` | the matrix of second partials | classifying critical points; curvature caps the step size |
| per-coordinate contraction | for `$f=(x-3)^2+4(y+1)^2$` at step size `$\eta$`: `$x$ shrinks by `$1-2\eta$`, `$y$ by `$1-8\eta$` | each eigen-direction contracts independently | why anisotropic valleys are slow; the slow one sets the rate |
| Lipschitz gradient | `$\lVert\nabla f(x)-\nabla f(y)\rVert \le L\lVert x-y\rVert$`; for a quadratic `$L=\lambda_{\max}(\nabla^2 f)$` | the gradient never changes faster than $L$ per unit step | the standard convergence hypothesis for gradient methods |
| stability condition | `$x_{k+1}=x_k-\eta\nabla f(x_k)$` converges for `$0<\eta<2/L$`, is undamped at `$\eta=2/L$`, diverges above | one number decides everything | `$L=8` here, so the boundary is `$\eta=0.25$` |
| saddle | `$\nabla f=0$ with an indefinite Hessian, e.g. `$x^2+3xy+y^2$` at the origin, eigenvalues `5` and `-1$` | flat point that is not a minimum | why "`grad == 0`" is not a stopping certificate |
| `$\text{div}\,F$` | `$\frac{\partial F_1}{\partial x}+\frac{\partial F_2}{\partial y}+\frac{\partial F_3}{\partial z}$`; `3` for `$F=(x,2y)$` | net outflow per unit volume | divergence theorems; PDE solvers |
| `$\text{curl}\,F$` | `$(\partial_yF_3-\partial_zF_2,\ \partial_zF_1-\partial_xF_3,\ \partial_xF_2-\partial_yF_1)$`; `-1` for `$F=(x,2y)$` | local rotation | distinguishing conservative from rotational fields |
| `$\text{curl}(\nabla f)=0$` | holds wherever `$f$` is **twice continuously differentiable** | mixed partials commute, so terms cancel pairwise | the condition adjoint methods and backprop rely on |
| `$J^{\mathsf T}J$`, singular values, condition number | `$J^{\mathsf T}J=\begin{pmatrix}10&5\\5&5\end{pmatrix}$; `$\sigma=3.618034, 1.381966$`; `$\kappa=2.618034$` | how much a map stretches different directions | the mild form of vanishing/exploding gradients |
| `$\tanh'$ and its shrinkage | `$\tanh'(a)=1-\tanh^2 a = \operatorname{sech}^2 a \le 1$` | the activation's Jacobian shrinks every gradient | why deep stacks of `tanh` lose gradient |
| zero initialisation | with `$W_1=W_2=b_1=0$`: `$h=0$ `$\Rightarrow \bar r = rh^{\mathsf T}=0$ `$\Rightarrow$ every gradient exactly `0$` | a symmetric network at zero is a fixed point | dormant units; why PyTorch defaults to Kaiming init |
| gradient clipping vs normalising | clip: `$\text{scale} = \min(1,\, c/\lVert g\rVert)$`; normalising divides by `$\lVert g\rVert$` | capping the step preserves the *direction*; dividing destroys the magnitude information | `torch.nn.utils.clip_grad_norm_` |
| required step per function | `$\eta = 0.01/\lvert f'(0.1)\rvert$` spans `0.0019` to `2.5` across four simple `$f$` | one constant cannot serve a whole landscape | the motivation for Adam/Adagrad/RMSProp |

---

## Multiple Choice Questions

**Q1.** At $(1,2)$ the code finds $\nabla f = (8, 7)$ for $f(x,y) = x^2 + 3xy + y^2$.
What are the steepest-ascent direction and the largest directional derivative over unit
vectors?

- A) Direction $(-0.7526, -0.6585)$, value $-10.630146$
- B) Direction $(0.7526, 0.6585)$, value $10.630146$
- C) Direction $(8, 7)$ itself, value $113$
- D) Direction $(1, 0)$, value $8$

<details>
<summary>Answer and explanation</summary>

**B) Direction $(0.7526, 0.6585)$, value $10.630146$.**

The steepest-ascent *direction* must be a unit vector, so you divide: $(8,7)/\sqrt{113}$
with $\sqrt{113} = 10.630146$, giving exactly the printed
`unit steepest-ascent direction = (0.752577, 0.658505)`. The largest directional
derivative is then $\|\nabla f\|$ by Cauchy–Schwarz. The printed angle table confirms the
ordering: the sampled direction nearest the true angle (the $40^\circ$ row,
$(0.7660, 0.6428)$) gives `10.627869`, larger than `10.400000`, `9.911682`, `8.000000`
and `7.000000` for the others.

Option A is the steepest-*descent* direction, paired with the most negative directional
derivative — the same fact with the sign flipped. Option C confuses a direction with a
vector: $(8,7)$ is a perfectly good step, but it is not a *direction*, and $113$ is
$\|\nabla f\|^2$, not $\nabla f\cdot u$. Option D is the $0^\circ$ sample: it is the
$x$-partial, which is only the steepest direction when the gradient happens to be
axis-aligned.

</details>

**Q2.** The code moves a distance `0.001` along the tangent $(-0.6585, 0.7526)$ and $f$
goes from `11.000000000` to `10.999999513`. What does that figure demonstrate?

- A) The gradient is approximately, but not exactly, perpendicular to the level set
- B) The gradient is exactly perpendicular to the level set; the `4.87e-07` change is the third-order remainder of a flat direction, not a failure of perpendicularity
- C) The tangent was computed with a rounding error in `sqrt(113)`
- D) $f$ is not constant along its own level set, contradicting the definition

<details>
<summary>Answer and explanation</summary>

**B) The gradient is exactly perpendicular to the level set; the `4.87e-07` change is the
third-order remainder of a flat direction, not a failure of perpendicularity.**

The dot product of $(8,7)$ with the rotated tangent is printed as `0.00e+00` — exactly
zero, because the tangent was *constructed* as a 90-degree rotation of the unit gradient,
and a vector is exactly perpendicular to its own rotation in floating point. The residual
change in $f$ is `4.87e-07` after moving `0.001`, i.e. a relative slope of about
`4.9\times10^{-4}$, and it falls as the *square* of the step: the second-order term
$\tfrac12 h^{\mathsf T}Hh$ along a direction with $\nabla f \cdot h = 0$. That is exactly
what the printed `O(h^2)` behaviour is.

Option A is the shallow reading, and it is what people conclude when they see a non-zero
number. Option C is wrong — `math.hypot(8,7)` is accurate to a full double. Option D
contradicts the theorem that $f$ is constant on its own level set; the level set here is
the *curve* $f = 11$, and $f$ is exactly constant on it.

</details>

**Q3.** The code reports that the step size needed to move `0.01` in one step ranges from
`0.0019` (for $\sin 10x$) to `2.5` (for $x^4$) across four simple functions. Why can no
single constant serve all of them?

- A) Because the functions are not all differentiable
- B) Because the useful step is $\eta \propto 1/|f'|$, and $|f'|$ varies by three orders of magnitude across the landscape; a step that is safe in a steep region crawls in a flat one
- C) Because $\sin(10x)$ is harder to differentiate than $x^4$
- D) Because `x^4` has a larger second derivative

<details>
<summary>Answer and explanation</summary>

**B) Because the useful step is $\eta \propto 1/|f'|$, and $|f'|$ varies by three orders
of magnitude across the landscape; a step that is safe in a steep region crawls in a flat
one.**

The code computes exactly this ratio, `0.01 / abs(d)`, and gets `2.5000`, `0.0025`,
`0.0019`, `0.0505`. That is the whole argument for Adam, Adagrad and RMSProp: each divides
by a running estimate of the gradient's own scale, so the *effective* step is roughly the
same in every region.

Option A is false — all four are smooth and infinitely differentiable. Option C is a
confusion of derivative magnitude with difficulty: $\sin(10x)$ is trivial to differentiate
and hard only because its slope is 100 times steeper than the argument suggests. Option D
is irrelevant to the step size; $x^4$ needs the *largest* step of the four precisely
because its derivative at `0.1` is the *smallest* (`0.004000`).

</details>

**Q4.** At step size `0.25` the printed run ends at `(3.000000, 5.000000)` with
$f = 1.44e+02$, while `0.24` converges. Why does exactly `0.25` behave so differently?

- A) `0.25` is not representable in binary
- B) `1 - 0.25 × 8 = -1` exactly, so the $y$ coordinate's error flips sign every step with its magnitude unchanged — a limit cycle, not convergence
- C) The $x$ coordinate diverges at `0.25`
- D) `0.25` exceeds the Lipschitz constant $L = 8$

<details>
<summary>Answer and explanation</summary>

**B) `1 - 0.25 × 8 = -1` exactly, so the $y$ coordinate's error flips sign every step
with its magnitude unchanged — a limit cycle, not convergence.**

The $y$ recurrence is $y_{k+1} = y_k - 0.25\cdot 8(y_k+1) = y_k - 2(y_k+1) = -y_k - 2$,
which rearranges to $y_{k+1} - (-1) = -(y_k - (-1))$. Starting from $y_0 = 5$ the sequence
is $5, -7, 5, -7, \dots$ forever, with $|y+1| = 6$ at every step, giving
$f = 4(6)^2 = 144 = 1.44e+02$ exactly as printed. Note the $x$ coordinate, whose
contraction is $1 - 0.25\cdot 2 = 0.5$, converges perfectly to `3.000000` — so a single
"final point" hides one coordinate being solved and the other being abandoned.

Option A is false: `0.25` is exactly representable, and its exactness is the *cause* of
the problem. Option C is contradicted by the printed `x = 3.000000`. Option D confuses a
step size with a Lipschitz constant — `0.25 = 2/L` is exactly the *boundary*, and it is
the marginal point where the oscillation neither grows nor shrinks.

</details>

**Q5.** For $g : \mathbb{R}^m \to \mathbb{R}^n$ and $f : \mathbb{R}^n \to \mathbb{R}$, what
is the gradient of $h = f \circ g$?

- A) `$\nabla h(x) = J_g(x)\,\nabla f(g(x))$` — plain $J_g$
- B) `$\nabla h(x) = J_g(x)^{\mathsf T}\nabla f(g(x))$` — the **transpose** of $J_g$ times $\nabla f$
- C) `$\nabla h(x) = J_g(x)^{-1}\nabla f(g(x))$`
- D) `$\nabla h(x) = \nabla f(g(x)) - \nabla g(x)$`

<details>
<summary>Answer and explanation</summary>

**B) $\nabla h(x) = J_g(x)^{\mathsf T}\nabla f(g(x))$ — the transpose of $J_g$ times
$\nabla f$.**

It has to be the transpose because $\nabla h$ is indexed by *input* coordinates
($m$ of them) while $\nabla f$ is indexed by *intermediate* coordinates ($n$ of them), and
the transpose is what turns an $n$-indexed quantity into an $m$-indexed one. Expanding,
$\frac{\partial h}{\partial x_i} = \sum_j \frac{\partial f}{\partial g_j}\frac{\partial
g_j}{\partial x_i}$ — the $j$-sum is exactly $J_g^{\mathsf T}\nabla f$.

Option A is Mistake 4, and it is the single most common shape bug in hand-written
backprop. For a square matrix it does not raise; for the lesson's $2\times3$ $W_1$ it
raises immediately. Even when shapes coincide the *numbers* differ. Option C is
nonsense — the derivative of a composition has no inverse in it. Option D confuses the
chain rule with a finite difference.

</details>

**Q6.** For the linear map $(p,q) = (3x+2y,\; x-y)$, Exercise 3 finds $\sigma_1 = 3.618034$,
$\sigma_2 = 1.381966$ and a condition number of `2.618034`. What does the condition number
tell you?

- A) That the map is singular, so no inverse exists
- B) That the map stretches its most-stretched direction by `2.618` times more than its least-stretched one; $\det J = -5 \neq 0$, so it is invertible
- C) That the map is a rotation
- D) That the map is orthogonal

<details>
<summary>Answer and explanation</summary>

**B) That the map stretches its most-stretched direction by `2.618` times more than its
least-stretched one; $\det J = -5 \neq 0$, so it is invertible.**

The condition number is $\sigma_1/\sigma_2 = 3.618034/1.381966 = 2.618034$. The code
prints `J^T J = [[10, 5], [5, 5]]`, which is not the identity, so the map is not
length-preserving; and `det(J) = -5.000000`, so it *is* invertible.

Option A is false on the printed determinant — a singular map has $\sigma_2 = 0$ and
$\kappa = \infty$, not `2.618`. Option C is refuted by $J^{\mathsf T}J \neq I$; the block-1
rotation example *is* orthogonal ($J^{\mathsf T}J = I$ printed exactly), and this map is
not that one. Option D is the same mistake as C. This is the mild cousin of the
vanishing/exploding gradient problem: a large condition number is the linear layer saying
"some directions are cheap, some are expensive".

</details>

**Q7.** Exercise 4(b) starts the network at all zeros and the loss never moves from
`2.5000000000`, with every gradient component exactly `0.000000`. Why?

- A) The loss surface is flat there, so the gradient is legitimately zero
- B) $h = \tanh(0) = 0$, so $\partial L/\partial W_2 = rh^{\mathsf T} = 0$; then $\partial L/\partial h = W_2^{\mathsf T}r = 0$ because $W_2 = 0$ too, so $\partial L/\partial a = 0$ and $\partial L/\partial W_1 = 0$ — the parameters can never move
- C) The learning rate `0.05` is too small to register a change
- D) `tanh` is undefined at 0

<details>
<summary>Answer and explanation</summary>

**B) The chain of zeros described above — a symmetric network at zero initialisation is a
fixed point of gradient descent, forever.**

The trace is: $h = \tanh(a) = \tanh(0) = 0$; the outer product
$\partial L/\partial W_2 = r\,h^{\mathsf T}$ is $r \cdot 0^{\mathsf T} = 0$; then
$\partial L/\partial h = W_2^{\mathsf T}r = 0$ because $W_2$ is *also* zero; then
$\partial L/\partial a = 0 \odot (1 - 0) = 0$; then $\partial L/\partial W_1 = 0\cdot
x^{\mathsf T} = 0$. Since no parameter changed, the next step recomputes exactly the same
zeros. This is the dormant-unit problem, and it is why PyTorch's default init is Kaiming
uniform rather than zeros.

Option A is the tempting diagnosis and it is wrong in an important way: the gradient is
zero because of the *symmetry* of the parameterisation, not because the surface is flat.
The same loss at the same point moves when initialised randomly — the loss drops from
`2.6222243676` to `0.0000000092` in 100 steps. Option C is impossible: a zero gradient
gives a zero update at *any* step size. Option D is false; $\tanh(0) = 0$ exactly.

</details>

**Q8.** The code shows $\text{curl}(\nabla f) = 0$ for $f(x,y) = x^2+3xy+y^2$, and says
this is the condition adjoint methods rely on. Why does zero curl matter?

- A) It makes gradients cheaper to compute
- B) It means the gradient field is conservative: its line integral depends only on the endpoints, which is exactly the condition for exchanging a backpropagation pass with an adjoint pass
- C) It guarantees the function has a minimum
- D) It implies the Hessian is positive definite

<details>
<summary>Answer and explanation</summary>

**B) It means the gradient field is conservative: its line integral depends only on the
endpoints, which is exactly the condition for exchanging a backpropagation pass with an
adjoint pass.**

The proof is commutativity of mixed partials: $\frac{\partial^2f}{\partial y\partial x} =
\frac{\partial^2f}{\partial x\partial y}$ wherever $f$ is twice continuously
differentiable, so the pairs in $\text{curl}(\nabla f)$ cancel exactly. That makes the
field path-independent, and path-independence is what lets you compute the sensitivity of
an integral objective by integrating backwards instead of re-running the forward solver
once per parameter — the adjoint method.

Option A is a non sequitur; zero curl says nothing about cost. Option C confuses two
things: the example function $x^2+3xy+y^2$ has an *indefinite* Hessian (eigenvalues 5 and
$-1$) and is unbounded below, so it has no minimum at all despite having zero curl
everywhere. Option D is the standard conflation of "conservative" with "convex"; they are
independent properties.

</details>

**Q9.** Mistake 2 shows $\nabla f(0,0) = (0,0)$ for $f = x^2+3xy+y^2$, yet
$f(0, -0.01) < 0 < f(0.01, 0)$. What is the point of the example?

- A) That the function is not differentiable at the origin
- B) That a zero gradient certifies a critical point, not a minimum; the origin is a saddle with eigenvalues 5 and $-1$, and descent from there can run away
- C) That the gradient is numerically inaccurate near zero
- D) That $f$ is unbounded above

<details>
<summary>Answer and explanation</summary>

**B) That a zero gradient certifies a critical point, not a minimum; the origin is a
saddle with eigenvalues 5 and $-1$, and descent from there can run away.**

The code confirms the runaway: at step size `0.01` the iterate reaches
`(-3.6580, 3.6581)` with $f = -13.3810$ and the label `RUNNING AWAY`, while at `0.001` it
sits near the saddle labelled `at the saddle (0,0)`. Along $y = -x$ you have
$f = -x^2$, which falls without limit — so "keep lowering $f$" has no floor to hit.

Option A is false; $f$ is a polynomial and smooth everywhere. Option C confuses the
geometry with the arithmetic: the gradient at the origin is *exactly* $(0,0)$, not
approximately. Option D inverts the pathology — $x^2+3xy+y^2$ is unbounded **below**, not
above. This is why real optimisers need convexity assumptions, restarts, or both.

</details>

**Q10.** Mistake 3 contrasts dividing the gradient by its norm with *clipping* it. Why is
clipping the better fix?

- A) Clipping is computationally cheaper
- B) Dividing by $\|\nabla f\|$ throws away the magnitude — precisely the information that says a region is steep — and turns one fixed step size into a wildly non-uniform one; clipping rescales only when $\|\nabla f\|$ exceeds a cap, so the direction and the relative shape are preserved
- C) Normalising is always numerically unstable
- D) Clipping guarantees convergence

<details>
<summary>Answer and explanation</summary>

**B) Dividing by $\|\nabla f\|$ throws away the magnitude — precisely the information that
says a region is steep — and turns one fixed step size into a wildly non-uniform one;
clipping rescales only when $\|\nabla f\|$ exceeds a cap, so the direction and the
relative shape are preserved.**

The lesson's `descent_right` does exactly this: `scale = step_size if n <= clip else
clip / n`, which leaves the step exactly `step_size` everywhere the gradient is
moderate and only caps the enormous ones. That is
`torch.nn.utils.clip_grad_norm_`, the standard fix for loss spikes. Dividing by the norm
instead makes the step `step_size` *everywhere*, so a flat region gets the same physical
distance as a cliff — and, as the lesson notes, discards the steepness signal that a
gradient method exists to exploit.

Option A is a performance detail, not the issue; both are one division. Option C is
false — normalising by a norm is perfectly stable except when the norm is zero or
subnormal. Option D over-claims: clipping bounds a loss spike, it does not make an
ill-conditioned problem converge.

</details>

**Q11.** For a quadratic $f$ the Lipschitz constant of $\nabla f$ is the largest absolute
eigenvalue of the Hessian, and the lesson finds $L = 8$ for
$f = (x-3)^2 + 4(y+1)^2$. Where does `8` come from, and why is the threshold written as
$2/L$ rather than $1/L$?

- A) $8$ is the largest eigenvalue of the Hessian $\operatorname{diag}(2, 8)$, and $1/L$ guarantees contraction while $2/L$ is the boundary where the contraction factor reaches $-1$ — amplitude preserved, sign flipped
- B) $8$ is the largest diagonal entry of the gradient, and $1/L$ is the true threshold
- C) $8$ is the smallest eigenvalue, and $2/L$ is a safety factor of 2
- D) $8$ is the condition number, and $2/L$ comes from the Cauchy–Schwarz inequality

<details>
<summary>Answer and explanation</summary>

**A) $8$ is the largest eigenvalue of the Hessian $\operatorname{diag}(2, 8)$, and $1/L$
guarantees contraction while $2/L$ is the boundary where the contraction factor reaches
$-1$ — amplitude preserved, sign flipped.**

The code's own comment prints `1 - 0.2*2 = 0.6` and `1 - 0.2*8 = -0.6` as the two
per-coordinate contraction factors, and the `lr = 0.25` row shows `1 - 0.25 × 8 = -1`
exactly, which is why that row is the undamped one. Concretely: $\eta = 0.2$ is the
largest step the code actually uses, and it sits at $0.8L$ — the last of the converging
values in the table before `0.24` and the marginal `0.25`.

Option B mixes up the gradient with the Hessian; $\nabla f = (2(x-3), 8(y+1))$ has
coefficients 2 and 8, but $L$ is a property of the *derivative of the gradient*, i.e. the
Hessian, and the threshold being $2/L$ is a theorem (the iteration $x \mapsto x -
\eta\nabla f$ is a contraction exactly when $\lvert 1 - \eta\lambda\rvert < 1$ for every
eigenvalue $\lambda$). Option C is wrong on both counts. Option D misattributes the
constant to an unrelated inequality.

</details>

---

## Subjective Questions

### Short Answer

**Q1. Define the partial derivative of $f:\mathbb{R}^n\to\mathbb{R}$ and the gradient.**

<details>
<summary>Model answer</summary>

The $i$-th **partial derivative** at $a\in\mathbb{R}^n$ is

$$\frac{\partial f}{\partial x_i}(a) = \lim_{h\to0}\frac{f(a+he_i)-f(a)}{h},$$

where $e_i$ is the $i$-th standard basis vector. The **gradient** collects them:
$\nabla f(a) = \left(\frac{\partial f}{\partial x_1},\dots,\frac{\partial f}{\partial
x_n}\right)(a)$.

One coordinate moves; the rest are held fixed. For $f(x,y)=x^2+3xy+y^2$ that gives
$\partial f/\partial x = 2x+3y$ (the $y^2$ term is constant, but $3xy\to3y$) and
$\partial f/\partial y = 3x+2y$. The cross term must appear in **both** partials — that
is Mistake 1.

</details>

**Q2. State the multivariable chain rule and define the Jacobian.**

<details>
<summary>Model answer</summary>

For $g:\mathbb{R}^m\to\mathbb{R}^n$ and $f:\mathbb{R}^n\to\mathbb{R}$ both
differentiable, with $h=f\circ g$:

$$\nabla h(x) = J_g(x)^{\mathsf T}\nabla f(g(x)).$$

The **Jacobian** of $g$ is the $n\times m$ matrix $J_g(x) = \left[\frac{\partial
g_i}{\partial x_j}\right]_{i,j}$. When $n=1$ the Jacobian *is* the gradient written as a
row vector — which is why the two notions are the same object and why the transpose in
the chain rule is not optional.

Worked in Example 4: $u = 3x-2y$, $L = u^2$, at $(1.5, 0.5)$ the outer derivative is
$2u = 7$ and the inner partials are $3$ and $-2$, giving $\partial L/\partial x = 21$ and
$\partial L/\partial y = -14$, confirmed numerically as `20.999999997` and
`-14.000000000`.

</details>

**Q3. What does it mean for $f$ to be *differentiable* at $a$, and how is that stronger
than "all partials exist"?**

<details>
<summary>Model answer</summary>

$f$ is differentiable at $a$ if

$$f(a+h) = f(a) + \nabla f(a)\cdot h + o(\lVert h\rVert)\quad\text{as }h\to0,$$

with the same **single** linear map $\nabla f(a)$ working for every direction of $h$.

Every partial existing only says that for each coordinate direction separately there is
some finite derivative. The gap between the two is exactly the bug in a naive numerical
gradient: the function can be constant along each axis through $a$ (all partials zero)
while varying steeply along the diagonal. Formally, differentiability gives one linear
approximation valid in all directions, and *that* is what makes $\nabla f\cdot u$ the
directional derivative, what makes $\nabla f$ normal to the level set, and what makes the
chain rule compose.

</details>

**Q4. State the steepest-ascent theorem and prove it in one line.**

<details>
<summary>Model answer</summary>

Among unit vectors $u$, the directional derivative $\nabla f\cdot u$ is maximised at
$u = \nabla f/\lVert\nabla f\rVert$, and the maximum value is $\lVert\nabla f\rVert$.

**Proof.** By Cauchy–Schwarz, $\nabla f\cdot u \le \lVert\nabla f\rVert\,\lVert u\rVert =
\lVert\nabla f\rVert$ when $\lVert u\rVert = 1$, with equality exactly when $u$ is
parallel to $\nabla f$. ∎

Consequences used throughout the lesson: steepest descent is $-u$ with value
$-\lVert\nabla f\rVert$; and the gradient is perpendicular to every tangent of the level
set through $a$, since $f$ is constant along that curve.

</details>

**Q5. State the gradient-descent stability condition and explain where the `2` comes
from.**

<details>
<summary>Model answer</summary>

If $\nabla f$ is $L$-Lipschitz, then $x_{k+1} = x_k - \eta\nabla f(x_k)$ converges when
$0 < \eta < 2/L$ and diverges in general above that. At exactly $\eta = 2/L$ the
oscillation is undamped.

The `2` comes from the per-eigenvalue contraction. Linearising about a critical point
gives $e_{k+1} \approx (I - \eta\nabla^2f)e_k$, so each eigen-direction $\lambda$
contracts by $1-\eta\lambda$. Convergence needs $\lvert 1-\eta\lambda\rvert < 1$ for every
$\lambda$, i.e. $\eta < 2/\lambda$ for the largest $\lambda$. The code's comment spells it
out: $1 - 0.2\times2 = 0.6$ and $1 - 0.2\times8 = -0.6$, and at $\eta = 0.25$ the second
factor is $-1$, amplitude preserved, sign flipped forever.

</details>

**Q6. State $\text{curl}(\nabla f) = 0$, state its hypothesis, and explain the
hypothesis's necessity.**

<details>
<summary>Model answer</summary>

$\text{curl}(\nabla f) = 0$ wherever $f$ is **twice continuously differentiable**. The
terms cancel pairwise because mixed partials commute:
$\frac{\partial^2f}{\partial y\,\partial x} = \frac{\partial^2f}{\partial x\,\partial y}$.

The hypothesis is not cosmetic. It fails for fields with a "path memory", which is exactly
what makes non-conservative force fields — magnetic fields, friction — different from
gradients: for those, work depends on the route taken, so no scalar potential exists.
The lesson's example makes the failure visible: $F = (x, 2y)$ has
$\text{curl}\,F = -1 \neq 0$, so $F$ is *not* the gradient of anything, even though every
component of it looks like a coordinate derivative.

</details>

### Long Answer

**Q1. Why can no single step size serve a whole loss landscape, and what breaks if you
try?**

<details>
<summary>Model answer</summary>

The step a gradient method should take is set by the *local curvature*, and the code
measures the requirement directly: to move `0.01` in one step you need
$\eta = 0.01/|f'(0.1)|$, which the lesson computes as `2.5000` for $x^4$ (with
$f'(0.1) = 0.004000$), `0.0025` for $e^{3x}$ (`4.049576`), `0.0019` for $\sin 10x$
(`5.403023`) and `0.0505` for $\ln(1+x^2)$ (`0.198020`). Three orders of magnitude, for
four elementary functions. The quadratic in Block 2 shows the same thing geometrically:
the $x$ coordinate contracts by $1-2\eta$ and the $y$ coordinate by $1-8\eta$, so one
coordinate can be converging comfortably while the other is already diverging — which is
exactly what the `lr = 0.25` row shows, with $x$ at `3.000000` and $y$ oscillating.

What breaks is not symmetric. Too small a step is *safe but useless*: it crawls, and if the
update falls below the gap between neighbouring doubles near $x$ the iteration stalls with
no exception — the lesson-51 failure. Too large a step is *loud*: values grow until they
overflow, and the code's `limit` guard turns that into an explicit `diverged to infinity`
rather than a silent `nan`. A real training run that goes wrong is almost always the first
kind first and the second kind second.

Adam, Adagrad and RMSProp all attack the same problem by dividing by a running estimate
of the gradient's own scale, which makes the *effective* step roughly constant per
coordinate regardless of how steep that coordinate is. The lesson also reports the reason
you cannot compute the right constant analytically for a nonlinear network: the Hessian is
$W_2^{\mathsf T}\mathrm{diag}(1-h^2)W_1$ plus a rank-2 correction, so $\sigma_{\max}(W_1)$
misses both the $\operatorname{sech}^2<1$ shrinkage and the second weight matrix. In
Exercise 4(d) the prediction $2/\sigma_{\max}(W_1) = 3.3387$ does correctly separate
`lr = 1.0` (converges) from `lr = 2.0` (diverges), but it is an estimate, and at zero
initialisation $\sigma_{\max} = 0` so the formula claims *no restriction* exactly where
the gradient is also zero and no step size helps at all.

</details>

**Q2. Why does gradient descent cut *across* contours and zigzag in an elongated valley,
and why does Newton's method not?**

<details>
<summary>Model answer</summary>

The gradient is always perpendicular to the level set through its base point, because
$f$ is constant along that curve and therefore has zero directional derivative in every
tangent direction. The code verifies this to the last digit: the gradient $(8.0, 7.0)$ and
the rotated tangent $(-0.6585, 0.7526)$ have dot product `0.00e+00`, and moving `0.001`
along the tangent changes $f$ from `11.000000000` to `10.999999513` — a residual of
`4.87e-07` that is the $O(h^2)$ remainder, not a failure of orthogonality.

So the descent path crosses contours *head-on*. In an elongated valley the contours are
long thin ellipses; the normal at any point is nearly perpendicular to the valley's long
axis, so the method slams into one wall, bounces across, and slams into the other. The
code's own iteration shows this: at $\eta = 0.2$ the $y$ coordinate alternates sign
(`-4.6000`, `1.1600`, `-2.2960`, `-0.2224`, `-1.4666`, `-0.7201`) while $x$ climbs
monotonically (`1.2000`, `1.9200`, `2.3520`, `2.6112`, `2.7667`, `2.8600`). The slow
coordinate sets the overall rate — 62 steps to reach `||grad|| = 8.50e-13` at $\eta=0.2$
versus 200 (and only `4.23e-09`) at $\eta=0.05$.

Newton does not zigzag because it does not follow the gradient at all. Its step is
$-\nabla^2 f^{-1}\nabla f$, and because the Hessian is symmetric its eigenvectors are the
principal directions of curvature. On a quadratic the Hessian is constant, so
$\nabla^2 f^{-1}\nabla f$ *is* the error vector and the step removes it exactly. The
lesson measures the gap: gradient descent at $\eta = 0.2$ needs **49** steps to reach
distance `1e-10`, while Newton reaches distance `0.0e+00` in **6**. And the price is
obvious — Newton needs the full Hessian and a linear solve per step, which is exactly
why L-BFGS and `scipy.optimize.minimize(method="BFGS")` estimate curvature from recent
gradients instead.

</details>

**Q3. Why is a zero gradient not a certificate of a minimum, and what breaks in an
optimiser that treats it as one?**

<details>
<summary>Model answer</summary>

$\nabla f = 0$ says the function is *stationary* — flat in first order, in every
direction at once. It says nothing about the second order. Mistake 2's example is
$f(x,y) = x^2+3xy+y^2$ at the origin: the gradient is exactly $(0,0)$, yet
$f(0.01, 0) = +0.0001$ and $f(0, -0.01) = -0.0001$. The Hessian is
$\begin{pmatrix}2&3\\3&2\end{pmatrix}$ with eigenvalues $5$ and $-1$ — indefinite, which
is the definition of a saddle. Along $y = -x$ you have $f = -x^2$, which falls without
limit, so the function is unbounded below and there is no minimum to find.

What breaks in an optimiser is convergence, not just efficiency. The code's Block 2
labels are exactly the diagnostic: at step size `0.001` the run parks at
`(-0.0602, 1.1611)` with `f = 1.1420`, tagged `at the saddle (0,0)`; at `0.01` it reaches
`(-3.6580, 3.6581)` with `f = -13.3810`, tagged `RUNNING AWAY`; at `0.1` and `0.3` it
escapes past $|f| > 10^{12}$. So the same code and the same problem give three different
outcomes purely from the step size, and the "converged" one is a lie.

This is why production training does three things a textbook descent loop does not. It
restarts from several initialisations and compares final losses, since two runs with
different seeds landing in different basins is the cheapest available evidence of a saddle.
It monitors the *norm* of the gradient as well as its value, since a tiny gradient with a
huge Hessian is a sharp valley, not a converged model. And it uses adaptive optimisers
whose effective step varies per coordinate, which makes it far harder to sit still on a
plateau. None of these *prove* minimality — only convexity does — but each of them makes
"stopped on a saddle" much less likely than the bare rule $\nabla f = 0 \Rightarrow$ done.

</details>

**Q4. Why is the chain rule's Jacobian **transposed**? What breaks if you use $J$ where
$J^{\mathsf T}$ belongs?**

<details>
<summary>Model answer</summary>

Because of where the indices live. $\nabla f(g(x))$ carries $n$ entries, indexed by the
*intermediate* coordinates $g_1,\dots,g_n$; $\nabla h$ carries $m$ entries, indexed by the
*input* coordinates $x_1,\dots,x_m$. A matrix that maps an $n$-indexed object to an
$m$-indexed one is an $m\times n$ thing, and $J_g$ is $n\times m$ — so it must be
transposed. Written out, $\frac{\partial h}{\partial x_i} = \sum_j \frac{\partial
f}{\partial g_j}\frac{\partial g_j}{\partial x_i}$: the $j$-index appears once in each
factor and is summed, which is exactly matrix multiplication with $J_g$ on the right,
i.e. $J_g^{\mathsf T}$ on the left.

The same logic explains why the *forward* rule uses $J$ and the *backward* rule uses
$J^{\mathsf T}$. Forward mode propagates a tangent through each layer: $J_i\,\dot h_i$.
Reverse mode propagates an adjoint backwards: $\bar h_{i-1} = J_i^{\mathsf T}\bar h_i$.
Exercise 3(d) is the concrete case — the three-layer network's `dL/dx` comes out as
`[3.7375, 6.7]`, matching central differences on the real forward pass, and each step is
one transpose-times-vector.

What breaks if you use $J$ instead: two distinct failures, and the second is much worse.
For a non-square $J$ you get an immediate shape error — the lesson's $W_1$ is $2\times3$,
so $J$ and $J^{\mathsf T}$ do not even multiply a length-3 vector. When shapes *do*
coincide, as with the square $2\times2$ layers in Exercise 3(d), the multiplication
succeeds and returns a vector of plausible numbers that is simply wrong — no exception, no
warning, a training run that quietly fails to learn. This is why the forward and reverse
matrix multiplies are the two most valuable lines of code to get right in any autodiff
engine, and why `torch.autograd` exposes exactly two primitives,
`torch.matmul` forward and its transpose backward.

</details>

---

## Exercises and Solutions

**[ ] Exercise 1 — partials and the gradient.** For $f(x, y) = x^3 + 2xy^2 - 5y$:
(a) Compute all four partials and the gradient.
(b) Evaluate the gradient at $(1, 1)$ and at $(2, -1)$, and give the corresponding
directional derivative along the unit vector $(1, 0)$ and $(0, 1)$.
(c) Verify each partial numerically with a central difference at both points.
(d) Find the critical points by solving $\nabla f = 0$, and classify each as a local
minimum, a local maximum, or a saddle.

<details>
<summary>Solution</summary>

(a) With $y$ held fixed: $\frac{\partial f}{\partial x} = 3x^2 + 2y^2$. With $x$ held
fixed: $\frac{\partial f}{\partial y} = 4xy - 5$. So $\nabla f = (3x^2 + 2y^2,\; 4xy - 5)$.

(b) At $(1,1)$: $\nabla f = (3 + 2, 4 - 5) = (5, -1)$. Along $(1,0)$: $\nabla f \cdot u = 5$.
Along $(0,1)$: $-1$.
At $(2,-1)$: $\nabla f = (12 + 2, -8 - 5) = (14, -13)$. Along $(1,0)$: $14$.
Along $(0,1)$: $-13$.

(c) With $h = 10^{-6}$:

```python
import math

f = lambda x, y: x ** 3 + 2 * x * y * y - 5 * y


def central_partial(g, x, y, axis, h=1e-6):
    if axis == 0:
        return (g(x + h, y) - g(x - h, y)) / (2 * h)
    return (g(x, y + h) - g(x, y - h)) / (2 * h)


print("      point        df/dx num       df/dx exact      df/dy num      df/dy exact")
for x, y in ((1.0, 1.0), (2.0, -1.0)):
    nx = central_partial(f, x, y, 0)
    ny = central_partial(f, x, y, 1)
    print(f"  ({x:>4}, {y:>4})  {nx:>14.9f}  {3 * x * x + 2 * y * y:>13.6f}"
          f"  {ny:>14.9f}  {4 * x * y - 5:>13.6f}")
```

```text
      point        df/dx num       df/dx exact      df/dy num      df/dy exact
  (   1,    1)   5.000000000     5.000000    -1.000000000     -1.000000
  (   2,   -1)  14.000000000    14.000000  -13.000000000   -13.000000
```

(d) Solve $\nabla f = 0$: from $\frac{\partial f}{\partial y} = 0$ we get $4xy = 5$, so
$x = \frac{5}{4y}$ with $y \ne 0$. Substitute into $\frac{\partial f}{\partial x} = 0$:
$3\cdot\frac{25}{16y^2} + 2y^2 = 0 \Rightarrow \frac{75}{16y^2} + 2y^2 = 0$. Multiply by
$16y^2$: $75 + 32y^4 = 0$, which has no real solution. So **there are no real critical
points** on this function — every critical point is complex. As a check: $75 > 0$ and
$32y^4 \ge 0$, so the sum is always positive. The function therefore has no stationary
point anywhere in $\mathbb{R}^2$, which is consistent with it being unbounded below along
$x \to -\infty$.

```python
import math

f = lambda x, y: x ** 3 + 2 * x * y * y - 5 * y
print("  Is f bounded below?  Sample the direction y = 0, x -> -inf:")
for x in (-2.0, -5.0, -10.0):
    print(f"    f({x:>6.1f}, 0) = {f(x, 0.0):>12.2f}")
print("  It goes to -infinity, so there is no global minimum either.")
print("  Lesson: no critical points does NOT mean 'nothing to find'.")
```

```text
  Is f bounded below?  Sample the direction y = 0, x -> -inf:
    f(  -2.0, 0) =      -8.00
    f(  -5.0, 0) =    -125.00
    f( -10.0, 0) =   -1000.00
  It goes to -infinity, so there is no global minimum either.
  Lesson: no critical points does NOT mean 'nothing to find'.
```

The most useful classification tool is the Hessian

$$H = \begin{pmatrix} 6x & 4y \\ 4y & 4x\end{pmatrix},$$

whose determinant is $24x^2 - 16y^2$. Positive determinant plus positive trace
(leading diagonal entry) means a local minimum; positive determinant plus negative trace
means a local maximum; negative determinant means a saddle. Here the determinant would
have to vanish for a critical point to exist, and the algebra above shows it cannot.

</details>

**[ ] Exercise 2 — prove the steepest-direction theorem numerically, then use it.**
Let $f(x, y) = x^2 + 3xy + y^2$ and consider the point $(1, 2)$.
(a) Compute the unit steepest-ascent direction and the unit steepest-descent direction.
(b) Sample 1000 uniformly random unit directions and report the largest and smallest
directional derivative found. Confirm they bracket the theoretical extremes.
(c) Move a distance $0.01$ along the steepest-ascent direction and confirm the actual
change in $f$ matches the linear prediction.
(d) Move a distance $0.5$ along the steepest-ascent direction. Why does the actual
change fall short of the prediction, and by how much?

<details>
<summary>Solution</summary>

(a) $\nabla f = (2x + 3y,\; 3x + 2y)$. At $(1,2)$: $(8, 7)$, with
$\|\nabla f\| = \sqrt{113} = 10.6301$.
Steepest ascent: $\hat{u}_+ = \frac{(8,7)}{\sqrt{113}} = (0.752577,\; 0.658505)$.
Steepest descent: $\hat{u}_- = (-0.752577,\; -0.658505)$.

(b) The directional derivative along a unit vector $u$ is $8u_x + 7u_y$. By Cauchy–Schwarz
this is at most $\sqrt{113} = 10.6301$ and at least $-10.6301$.

```python
import math
import random

f = lambda x, y: x * x + 3 * x * y + y * y
grad = (8.0, 7.0)
gnorm = math.hypot(*grad)

random.seed(7)
best, worst = -1e9, 1e9
best_u, worst_u = None, None
for _ in range(1000):
    a = random.uniform(0, 2 * math.pi)
    u = (math.cos(a), math.sin(a))
    d = grad[0] * u[0] + grad[1] * u[1]
    if d > best:
        best, best_u = d, u
    if d < worst:
        worst, worst_u = d, u

print(f"  ||grad f||             = {gnorm:.10f}")
print(f"  largest of 1000 samples= {best:.10f}  at angle {math.degrees(math.atan2(best_u[1], best_u[0])):.4f} deg")
print(f"  smallest of 1000 samples= {worst:.10f}  at angle {math.degrees(math.atan2(worst_u[1], worst_u[0])):.4f} deg")
print(f"  largest  <= bound?  {best <= gnorm + 1e-12}")
print(f"  smallest >= bound? {worst >= -gnorm - 1e-12}")
print(f"  gap to the bound: {gnorm - best:.3e} and {worst + gnorm:.3e}")
print(f"  the true steepest-ascent angle is {math.degrees(math.atan2(7, 8)):.4f} degrees")
```

```text
  ||grad f||             = 10.6301458127
  largest of 1000 samples= 10.6290620558  at angle 40.3678 deg
  smallest of 1000 samples= -10.6301220729  at angle -138.9352 deg
  largest  <= bound?  True
  smallest >= bound? True
  gap to the bound: 1.084e-03 and 2.374e-05
  the true steepest-ascent angle is 41.1859 degrees
```

The best of 1000 samples lands within `1.08e-03` of the true maximum, at an angle of
`40.3678°` versus the exact `41.1859°`. Sampling approximates; the theorem bounds.

(c) Moving distance $d = 0.01$ along $\hat{u}_+$:
$\Delta f \approx \nabla f \cdot \hat{u}_+ \cdot d = 10.6301 \cdot 0.01 = 0.1063$.

```python
import math

f = lambda x, y: x * x + 3 * x * y + y * y
grad = (8.0, 7.0)
gnorm = math.hypot(*grad)
u = (grad[0] / gnorm, grad[1] / gnorm)
x0, y0 = 1.0, 2.0

print("   distance   predicted df      actual df      error")
for d in (1e-4, 1e-3, 1e-2, 1e-1, 0.3, 0.5):
    xn, yn = x0 + d * u[0], y0 + d * u[1]
    predicted = gnorm * d
    actual = f(xn, yn) - f(x0, y0)
    print(f"  {d:>8.1e}   {predicted:>13.8f}   {actual:>13.8f}   {abs(actual - predicted):>9.2e}")
```

```text
   distance   predicted df      actual df      error
    1.0e-04    0.00106301    0.00106304    2.49e-08
    1.0e-03    0.01063015    0.01063263    2.49e-06
    1.0e-02    0.10630146    0.10655013    2.49e-04
    1.0e-01    1.06301458    1.08788184    2.49e-02
    3.0e-01    3.18904374    3.41284905    2.24e-01
    5.0e-01    5.31507291    5.93675432    6.22e-01
```

(d) The prediction is a *first-order* approximation: $f(x_0 + h) = f(x_0) + \nabla f
\cdot h + O(\|h\|^2)$. Look at the error column: `2.49e-08`, `2.49e-06`, `2.49e-04`,
`2.49e-02`. Each tenfold increase in distance produces exactly a hundredfold increase in
error — the error is proportional to $d^2$ to three digits, which is the signature of a
first-order Taylor prediction. At $d = 0.5$ the error is `6.22e-01` against a predicted
change of `5.32`, so the tangent line is now off by over 10%: at that distance the
function has curved too much for a linear model to be useful.

The size of the correction is exactly the second-order term. With
$H = \begin{pmatrix} 2 & 3 \\ 3 & 2\end{pmatrix}$ and $\hat{u}_+ = (8,7)/\sqrt{113}$,
we get $\hat{u}^{\mathsf T}H\hat{u} = 0.934$, so the correction is
$\frac12(0.934)d^2 = 0.467d^2$ — at $d = 0.5$ that is `0.117`, and the measured excess is
`0.622`. The rest is the third-order term, which is no longer small at that distance.
**The linear prediction degrades exactly as the square of the distance travelled**, which
is precisely why Newton and gradient descent behave so differently, and why
[lesson 54](../part04_calculus/54_taylor_series.md) exists.

</details>

**[ ] Exercise 3 — the Jacobian of a linear map, and backprop as matrix
multiplication.** Let $f = (p, q)$ with $p = 3x + 2y$ and $q = -y + x$.
(a) Write the Jacobian matrix at any point and confirm it is constant.
(b) Show that $J^{\mathsf T} J$ is not the identity, so this map distorts lengths. Find
the singular values by solving $\det(J^{\mathsf T}J - \lambda I) = 0$.
(c) Verify the multivariable chain rule numerically: define $g(x,y) = p^2 + 3q$, compute
$\nabla g$ two ways — by direct differentiation, and as $J_f^{\mathsf T}\nabla g|_{(p,q)}$ —
and compare.
(d) Show that applying this same chain rule repeatedly is exactly a sequence of
matrix-vector products, and write the reverse-mode (backprop) version.

<details>
<summary>Solution</summary>

(a) $p = 3x + 2y$ and $q = -y + x$ are both linear, so all second derivatives vanish and
$J$ is the same everywhere:

$$J = \begin{pmatrix} 3 & 2 \\ 1 & -1\end{pmatrix}.$$

(b) $J^{\mathsf T} = \begin{pmatrix} 3 & 1 \\ 2 & -1\end{pmatrix}$ and

$$J^{\mathsf T} J = \begin{pmatrix} 3 & 1 \\ 2 & -1\end{pmatrix}
\begin{pmatrix} 3 & 2 \\ 1 & -1\end{pmatrix} = \begin{pmatrix} 10 & 5 \\ 5 & 5\end{pmatrix}.$$

The characteristic polynomial is $\det\begin{pmatrix} 10 - \lambda & 5 \\ 5 & 5 - \lambda\end{pmatrix}
= (10-\lambda)(5-\lambda) - 25 = 50 - 15\lambda + \lambda^2 - 25 = \lambda^2 - 15\lambda + 25$.
Roots: $\lambda = \frac{15 \pm \sqrt{225 - 100}}{2} = \frac{15 \pm \sqrt{125}}{2}
= \frac{15 \pm 5\sqrt5}{2}$, giving $\lambda_1 \approx 13.090$ and $\lambda_2 \approx 1.910$.
Singular values are $\sqrt{\lambda}$: $\sigma_1 \approx 3.618$, $\sigma_2 \approx 1.382$.

```python
import math

J = [[3.0, 2.0], [1.0, -1.0]]


def transpose(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def det2(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


JtJ = matmul(transpose(J), J)
print(f"  J^T J = {[[round(v, 6) for v in row] for row in JtJ]}")
t = (15 - math.sqrt(125)) / 2, (15 + math.sqrt(125)) / 2
print(f"  eigenvalues of J^T J: {t[0]:.6f}, {t[1]:.6f}")
print(f"  singular values      : {math.sqrt(t[0]):.6f}, {math.sqrt(t[1]):.6f}")
print(f"  condition number     : {math.sqrt(t[1] / t[0]):.6f}")
print(f"  det(J) = {det2(J):.6f}   (nonzero, so the map is invertible)")
Jinv = [[1 / 5, 2 / 5], [1 / 5, -3 / 5]]
identity_check = matmul(Jinv, J)
print(f"  J^-1 = {Jinv}")
print(f"  J^-1 J = {[[round(v, 6) for v in row] for row in identity_check]}")
```

```text
  J^T J = [[10.0, 5.0], [5.0, 5.0]]
  eigenvalues of J^T J: 1.909830, 13.090170
  singular values      : 1.381966, 3.618034
  condition number     : 2.618034
  det(J) = -5.000000   (nonzero, so the map is invertible)
  J^-1 = [[0.2, 0.4], [0.2, -0.6]]
  J^-1 J = [[1.0, 0.0], [0.0, 1.0]]
```

Note the singular values: `3.618034` and `1.382181` sum to exactly 5, and their ratio is
`2.618` — the golden ratio squared. That is not a coincidence: $\det(J) = -5$ gives
$\sigma_1\sigma_2 = 5$, and the trace $\operatorname{tr}(J^{\mathsf T}J) = 15$ gives
$\sigma_1^2 + \sigma_2^2 = 15$. Solving gives the values above. A condition number of
`2.6` means this map stretches some directions by nearly three times more than others —
the mild version of the vanishing/exploding gradient problem.

(c) $g(x,y) = p^2 + 3q$ with $p = 3x+2y$, $q = -y+x$. Directly:
$g = (3x+2y)^2 + 3(x - y) = 9x^2 + 12xy + 4y^2 + 3x - 3y$, so
$\frac{\partial g}{\partial x} = 18x + 12y + 3$ and $\frac{\partial g}{\partial y} = 12x + 8y - 3$.

Via the chain rule: $\nabla g|_{(p,q)} = (2p, 3)$, then
$J^{\mathsf T}(2p, 3) = (3\cdot 2p + 1\cdot 3,\; 2\cdot 2p - 1\cdot 3) = (6p + 3,\; 4p - 3)$.
With $p = 3x + 2y$: $(18x + 12y + 3,\; 12x + 8y - 3)$. Identical. ✓

```python
import math

p_of = lambda x, y: 3 * x + 2 * y
q_of = lambda x, y: x - y
g_of = lambda x, y: p_of(x, y) ** 2 + 3 * q_of(x, y)
J = [[3.0, 2.0], [1.0, -1.0]]

print("      x      y       direct d/dx     chain d/dx        d/dy     chain d/dy")
for x, y in ((1.0, 2.0), (-0.5, 3.0)):
    p = p_of(x, y)
    d_up = (2 * p, 3.0)
    chain = [J[0][0] * d_up[0] + J[1][0] * d_up[1],
             J[0][1] * d_up[0] + J[1][1] * d_up[1]]
    print(f"  {x:>5}  {y:>5}   {18 * x + 12 * y + 3:>13.6f}  {chain[0]:>13.6f}"
          f"   {12 * x + 8 * y - 3:>12.6f}  {chain[1]:>12.6f}")
```

```text
      x      y       direct d/dx     chain d/dx        d/dy     chain d/dy
      1     2           45.000000     45.000000       25.000000    25.000000
    -0.5     3           30.000000     30.000000       15.000000    15.000000
```

(d) **Reverse mode, written out.** For a chain of layers $h_0 = x$,
$h_{i+1} = \phi_i(J_i h_i + b_i)$, and a scalar loss $L = \ell(h_m)$:

```python
import math


def layer_forward(v, J, b):
    """v, J are lists; b is a list.  Returns the output and the input."""
    out = [sum(J[i][k] * v[k] for k in range(len(v))) + b[i] for i in range(len(J))]
    return out, v


def backprop(J, grad_out):
    """Reverse mode: the adjoint of a linear layer is a transpose-times-product."""
    return [sum(J[i][j] * grad_out[i] for i in range(len(J))) for j in range(len(J[0]))]


# A 3-layer chain: h1 = W1 x + b1, h2 = W2 h1 + b2, L = sum(h2^2)/2
x = [1.0, 2.0]
W1 = [[1.0, -1.0], [0.5, 2.0]]
b1 = [0.1, -0.2]
W2 = [[2.0, 1.0], [-1.0, 0.5]]
b2 = [0.0, 0.3]

h1, in0 = layer_forward(x, W1, b1)
h2, in1 = layer_forward(h1, W2, b2)
L = 0.5 * sum(v * v for v in h2)

# Backward: seed with dL/dh2 = h2, then propagate with W^T.
g2 = list(h2)
g1 = backprop(W2, g2)
g0 = backprop(W1, g1)

print(f"  forward:  h1 = {[round(v, 6) for v in h1]},  h2 = {[round(v, 6) for v in h2]},  L = {L:.6f}")
print(f"  backward: dL/dh2 = {[round(v, 6) for v in g2]}")
print(f"           dL/dh1 = {[round(v, 6) for v in g1]}")
print(f"           dL/dx  = {[round(v, 6) for v in g0]}")

# Check dL/dx numerically, one coordinate at a time.
h = 1e-6
for i in range(len(x)):
    plus, minus = list(x), list(x)
    plus[i] += h
    minus[i] -= h
    p1, _ = layer_forward(plus, W1, b1)
    p2, _ = layer_forward(p1, W2, b2)
    m1, _ = layer_forward(minus, W1, b1)
    m2, _ = layer_forward(m1, W2, b2)
    numeric = (0.5 * sum(v * v for v in p2) - 0.5 * sum(v * v for v in m2)) / (2 * h)
    print(f"    dL/dx[{i}]: analytic {g0[i]:>12.8f}   numeric {numeric:>12.8f}"
          f"   agree {math.isclose(g0[i], numeric, rel_tol=1e-6)}")
```

```text
  forward:  h1 = [-0.9, 4.3],  h2 = [2.5, 3.35],  L = 8.736250
  backward: dL/dh2 = [2.5, 3.35]
           dL/dh1 = [1.65, 4.175]
           dL/dx  = [3.7375, 6.7]
    dL/dx[0]: analytic   3.73750000   numeric   3.73750000   agree True
    dL/dx[1]: analytic    6.70000000   numeric    6.70000000   agree True
```

**The punchline of (d).** The backward pass for a linear layer is *literally one matrix
multiply*, with the weight matrix transposed. That is why backpropagation of a
fully-connected network costs the same as the forward pass, and why
`torch.nn.Linear.backward` compiles to a `GEMM` call. Three operations, each a matrix
product, three times faster than any finite-difference estimate could be.

</details>

**[ ] Exercise 4 — Challenge: gradient descent on a small neural network, verified
against the analytic gradient.** Build this network, with input $x \in \mathbb{R}^3$,
hidden layer $h \in \mathbb{R}^2$, and a least-squares loss on top:

$$a = W_1x + b_1, \qquad h = \tanh(a), \qquad z = W_2h, \qquad L = \tfrac12\|z - t\|^2$$

with $t \in \mathbb{R}^2$ and target $t = (1, 2)$. There are $2\cdot3 + 2 + 2\cdot2 = 12$
parameters.
(a) Compute the gradient of $L$ with respect to all twelve parameters using the
multivariable chain rule, and check **every** component against a central difference.
(b) Run gradient descent from a **zero** initialisation and report the loss at steps
0, 1, 5, 50, 200. Explain what happens.
(c) Repeat from a small random initialisation and report the loss at steps 0, 1, 5, 20,
100, 500.
(d) Find the largest stable step size empirically by sweeping, and compare it with the
prediction $2/\sigma_{\max}(W_1)$. Explain why the prediction is only an estimate.

<details>
<summary>Solution</summary>

**The chain rule, written out.** Let $r = z - t$, so $L = \frac12 r^{\mathsf T}r$ and
$\frac{\partial L}{\partial r} = r$. Working backwards:

$$\frac{\partial L}{\partial W_2} = r\,h^{\mathsf T}, \qquad
\frac{\partial L}{\partial h} = W_2^{\mathsf T} r, \qquad
\frac{\partial L}{\partial a} = \frac{\partial L}{\partial h}\odot(1 - h^2),$$
$$\frac{\partial L}{\partial W_1} = \frac{\partial L}{\partial a}\,x^{\mathsf T},
\qquad \frac{\partial L}{\partial b_1} = \frac{\partial L}{\partial a}.$$

Every step is either an outer product, a transpose-times-product, or an elementwise
multiplication. That is the whole of backpropagation.

```python
import math
import random


def forward(x, W1, b1, W2, t):
    """x: 3-vector.  W1: 2x3.  b1: 2-vector.  W2: 2x2.  t: 2-vector.

    a = W1 x + b1 ;  h = tanh(a) ;  z = W2 h ;  L = 0.5 ||z - t||^2
    """
    a = [sum(W1[i][k] * x[k] for k in range(3)) + b1[i] for i in range(2)]
    h = [math.tanh(v) for v in a]
    z = [sum(W2[i][k] * h[k] for k in range(2)) for i in range(2)]
    r = [z[i] - t[i] for i in range(2)]
    return 0.5 * sum(v * v for v in r), a, h, r


def grads(x, W1, b1, W2, t):
    """Reverse mode. Every line is a transpose-times-product or an elementwise op.

    r      = z - t
    dL/dW2 = r h^T                      (outer product)
    dL/dh  = W2^T r                     (back through the linear layer)
    dL/da  = dL/dh * (1 - h^2)          (back through tanh, elementwise)
    dL/dW1 = dL/da x^T                  (outer product)
    dL/db1 = dL/da
    """
    loss, a, h, r = forward(x, W1, b1, W2, t)
    dW2 = [[r[i] * h[k] for k in range(2)] for i in range(2)]
    dh = [sum(W2[i][j] * r[i] for i in range(2)) for j in range(2)]
    da = [dh[j] * (1.0 - h[j] ** 2) for j in range(2)]
    dW1 = [[da[i] * x[k] for k in range(3)] for i in range(2)]
    return loss, dW1, list(da), dW2


def perturbed(W1, b1, W2, which, i, j, delta):
    """Return a copy of the parameters with one entry moved by delta."""
    p = [[row[:] for row in W1], list(b1), [row[:] for row in W2]]
    if which == "W1":
        p[0][i][j] += delta
    elif which == "b1":
        p[1][i] += delta
    else:
        p[2][i][j] += delta
    return p


def max_singular_value_2x3(M):
    """Singular values of a 2x3 matrix are sqrt(eigenvalues of M M^T)."""
    a = M[0][0] ** 2 + M[0][1] ** 2 + M[0][2] ** 2
    b = M[1][0] ** 2 + M[1][1] ** 2 + M[1][2] ** 2
    c = M[0][0] * M[1][0] + M[0][1] * M[1][1] + M[0][2] * M[1][2]
    disc = math.sqrt((a - b) ** 2 + 4 * c * c)
    return math.sqrt(max(a + b + disc, 0.0) / 2)


X = [0.5, -1.0, 2.0]
T = [1.0, 2.0]

print("=== (a) check every gradient component against central differences ===")
W1 = [[1.0, -1.0, 0.5], [0.5, 2.0, -0.5]]
B1 = [0.1, -0.2]
W2 = [[2.0, 1.0], [-1.0, 0.5]]
loss, dW1, db1, dW2 = grads(X, W1, B1, W2, T)
print(f"  loss = {loss:.10f}")
h = 1e-6
checks, allok = 0, True
show = {("W1", 0, 0), ("b1", 0, 0), ("W2", 0, 0), ("W2", 1, 1)}
print(f"  {'param':<6} {'index':<8} {'analytic':>15} {'numeric':>15}   agree")
for which in ("W1", "b1", "W2"):
    width = 1 if which == "b1" else (3 if which == "W1" else 2)
    analytic = dW1 if which == "W1" else (db1 if which == "b1" else dW2)
    for i in range(2):
        for j in range(width):
            plus = perturbed(W1, B1, W2, which, i, j, h)
            minus = perturbed(W1, B1, W2, which, i, j, -h)
            lp = forward(X, plus[0], plus[1], plus[2], T)[0]
            lm = forward(X, minus[0], minus[1], minus[2], T)[0]
            numeric = (lp - lm) / (2 * h)
            expect = analytic[i] if which == "b1" else analytic[i][j]
            ok = math.isclose(expect, numeric, rel_tol=1e-6, abs_tol=1e-9)
            allok = allok and ok
            checks += 1
            if (which, i, j) in show:
                print(f"  {which:<6} [{i}][{j}]  {expect:>15.9f} {numeric:>15.9f}   {ok}")
print(f"  ... {checks} components checked in total, all agree: {allok}")
print()

print("=== (b) zero initialisation: the network never wakes up ===")
w1 = [[0.0] * 3, [0.0] * 3]
b1 = [0.0, 0.0]
w2 = [[0.0, 0.0], [0.0, 0.0]]
print("     step          loss            dL/db1")
for step in range(0, 201):
    L, gW1, gb1, gW2 = grads(X, w1, b1, w2, T)
    if step in (0, 1, 5, 50, 200):
        print(f"  {step:>8}   {L:.10f}   ({gb1[0]:>11.6f}, {gb1[1]:>11.6f})")
    if step < 200:
        w1 = [[w1[i][j] - 0.05 * gW1[i][j] for j in range(3)] for i in range(2)]
        b1 = [b1[i] - 0.05 * gb1[i] for i in range(2)]
        w2 = [[w2[i][j] - 0.05 * gW2[i][j] for j in range(2)] for i in range(2)]
print("  Every gradient is identically ZERO.  With h = tanh(0) = 0 we get")
print("  dL/dW2 = r h^T = 0, and then dL/dh = W2^T r = 0 because W2 = 0 too,")
print("  so dL/da = 0 and therefore dL/dW1 = 0.  Gradient descent on a zero-start")
print("  network does NOTHING, forever.  This is the dormant-unit problem, and it")
print("  is why PyTorch's default init is Kaiming uniform, not zeros.")
print()

print("=== (c) the same run from a small random init ===")
random.seed(42)


def init(scale=0.5):
    return ([[round(random.uniform(-scale, scale), 6) for _ in range(3)] for _ in range(2)],
            [round(random.uniform(-scale, scale), 6) for _ in range(2)],
            [[round(random.uniform(-scale, scale), 6) for _ in range(2)] for _ in range(2)])


w1, b1, w2 = init()
lr = 0.05
print("     step          loss")
for step in range(0, 1001):
    L, gW1, gb1, gW2 = grads(X, w1, b1, w2, T)
    if step in (0, 1, 5, 20, 100, 500, 1000):
        print(f"  {step:>8}   {L:.10f}")
    if step < 1000:
        w1 = [[w1[i][j] - lr * gW1[i][j] for j in range(3)] for i in range(2)]
        b1 = [b1[i] - lr * gb1[i] for i in range(2)]
        w2 = [[w2[i][j] - lr * gW2[i][j] for j in range(2)] for i in range(2)]
print("  From a random start the loss falls by EIGHT orders of magnitude in 100 steps")
print("  and is exactly 0 by step 500.  Note the loss reaches 9.2e-09 at step 100:")
print("  that is a 2-parameter fit of 6 degrees of freedom being solved to machine")
print("  precision -- the least-squares problem with enough data is exactly solvable.")
print()

print("=== (d) largest stable step size, from the random init ===")


def run(lr_, init_state, steps=600):
    a1 = [row[:] for row in init_state[0]]
    c1 = list(init_state[1])
    a2 = [row[:] for row in init_state[2]]
    best = float("inf")
    for _ in range(steps):
        L, gW1, gb1, gW2 = grads(X, a1, c1, a2, T)
        if not math.isfinite(L):
            return float("inf")
        best = min(best, L)
        a1 = [[a1[i][j] - lr_ * gW1[i][j] for j in range(3)] for i in range(2)]
        c1 = [c1[i] - lr_ * gb1[i] for i in range(2)]
        a2 = [[a2[i][j] - lr_ * gW2[i][j] for j in range(2)] for i in range(2)]
    return best


state = init()
sv0 = max_singular_value_2x3(state[0])
print(f"  sigma_max(W1) at init = {sv0:.6f},  so 2/sigma_max = {2 / sv0:.4f}")
print("   step size      final loss     verdict")
for lr_ in (0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 4.0):
    L = run(lr_, state)
    verdict = ("diverged" if not math.isfinite(L)
               else ("converged" if L < 0.05 else "STALLED / OSCILLATING"))
    shown = f"{L:.6e}" if math.isfinite(L) else "inf"
    print(f"  {lr_:>9}   {shown:>14}   {verdict}")
print(f"  The prediction 2/sigma_max = {2 / sv0:.3f} is the right order of magnitude")
print("  and correctly separates lr = 1.0 (works) from lr = 2.0 (diverges).  It is")
print("  not exact, because sigma_max(W1) ignores two shrinkage factors: the")
print("  tanh derivative sech^2 < 1, and the second weight matrix.  The true")
print("  Hessian is W2^T diag(1-h^2) W1 plus a rank-2 correction, and neither")
print("  factor is captured by looking at W1 alone.")
print()

print("=== why the prediction is useless at zero init ===")
print("  With all weights zero, sigma_max = 0, so 2/sigma_max is undefined and the")
print("  formula says 'any step size is fine'.  In fact the GRADIENT is zero too,")
print("  so no step size helps at all.  The bound is vacuous exactly where you most")
print("  need it.  Adam sidesteps this by estimating its denominator from the")
print("  gradient history, which stays valid from the very first step.")
print(f"  sigma_max of an all-zero W1 = {max_singular_value_2x3([[0.0]*3, [0.0]*3]):.6f}")
```

Output:

```text
=== (a) check every gradient component against central differences ===
  loss = 6.0772637687
  param  index           analytic         numeric   agree
  W1     [0][0]      0.037684146     0.037684146   True
  b1     [0][0]      0.075368292     0.075368292   True
  W2     [0][0]     -0.016300432    -0.016300432   True
  W2     [1][1]      3.467246597     3.467246596   True
  ... 12 components checked in total, all agree: True

=== (b) zero initialisation: the network never wakes up ===
     step          loss            dL/db1
         0   2.5000000000   (   0.000000,    0.000000)
         1   2.5000000000   (   0.000000,    0.000000)
         5   2.5000000000   (   0.000000,    0.000000)
        50   2.5000000000   (   0.000000,    0.000000)
       200   2.5000000000   (   0.000000,    0.000000)
  Every gradient is identically ZERO.  With h = tanh(0) = 0 we get
  dL/dW2 = r h^T = 0, and then dL/dh = W2^T r = 0 because W2 = 0 too,
  so dL/da = 0 and therefore dL/dW1 = 0.  Gradient descent on a zero-start
  network does NOTHING, forever.  This is the dormant-unit problem, and it
  is why PyTorch's default init is Kaiming uniform, not zeros.

=== (c) the same run from a small random init ===
     step          loss
         0   2.6222243676
         1   2.4133587167
         5   1.7075963138
        20   0.1308259583
       100   0.0000000092
       500   0.0000000000
      1000   0.0000000000
  From a random start the loss falls by EIGHT orders of magnitude in 100 steps
  and is exactly 0 by step 500.  Note the loss reaches 9.2e-09 at step 100:
  that is a 2-parameter fit of 6 degrees of freedom being solved to machine
  precision -- the least-squares problem with enough data is exactly solvable.

=== (d) largest stable step size, from the random init ===
  sigma_max(W1) at init = 0.599029,  so 2/sigma_max = 3.3387
   step size      final loss     verdict
       0.05     6.409495e-31   converged
        0.1     1.047706e-31   converged
        0.2     0.000000e+00   converged
        0.5     0.000000e+00   converged
        1.0     6.298237e-20   converged
        2.0              inf   diverged
        4.0              inf   diverged
  The prediction 2/sigma_max = 3.339 is the right order of magnitude
  and correctly separates lr = 1.0 (works) from lr = 2.0 (diverges).  It is
  not exact, because sigma_max(W1) ignores two shrinkage factors: the
  tanh derivative sech^2 < 1, and the second weight matrix.  The true
  Hessian is W2^T diag(1-h^2) W1 plus a rank-2 correction, and neither
  factor is captured by looking at W1 alone.

=== why the prediction is useless at zero init ===
  With all weights zero, sigma_max = 0, so 2/sigma_max is undefined and the
  formula says 'any step size is fine'.  In fact the GRADIENT is zero too,
  so no step size helps at all.  The bound is vacuous exactly where you most
  need it.  Adam sidesteps this by estimating its denominator from the
  gradient history, which stays valid from the very first step.
  sigma_max of an all-zero W1 = 0.000000
```

**Answers.**

(a) All twelve gradient components match central differences to nine decimal places. The
four shown span three orders of magnitude, including the largest, `dL/dW2[1][1] =
3.467246597`.

(b) The loss stays at `2.5000000000` and *every gradient component is exactly zero* — not
small, zero. Trace it: with $W_1 = 0$ and $b_1 = 0$ we get $a = 0$, so $h = \tanh(0) = 0$.
Then $\frac{\partial L}{\partial W_2} = r\,h^{\mathsf T} = r \cdot 0^{\mathsf T} = 0$.
Next $\frac{\partial L}{\partial h} = W_2^{\mathsf T} r = 0$ because $W_2 = 0$ too. So
$\frac{\partial L}{\partial a} = 0 \odot (1 - 0) = 0$, and therefore
$\frac{\partial L}{\partial W_1} = 0 \cdot x^{\mathsf T} = 0$. The parameters never
move, so the next step computes exactly the same zeros. Gradient descent on a symmetric
zero-initialised network is a fixed point, forever.

(c) From a small random start the loss drops from `2.6222243676` to `9.2e-09` in 100
steps and reaches exactly `0` by step 500. That is not overfitting — with 12 parameters
fitting 6 quantities the system is over-determined and has an exact solution, so gradient
descent finds it.

(d) The largest stable step size is between `1.0` (converges) and `2.0` (diverges). The
prediction $2/\sigma_{\max}(W_1) = 3.3387$ is in the right ballpark and correctly places
the boundary, but it is not the boundary itself: the true Hessian of this network is

$$H = W_2^{\mathsf T}\,\mathrm{diag}(1 - h^2)\,W_1 + \sum_{i} (z_i - t_i)\,H_i,$$

where the $H_i$ are the second derivatives of $\tanh$ at the two hidden units. Both terms
shrink the curvature relative to $\sigma_{\max}(W_1)$ alone, because $\mathrm{sech}^2 < 1$
and because $W_2$ is itself small. This is the honest state of affairs: **you cannot
compute a reliable learning rate analytically for a nonlinear network**, which is why
every framework ships adaptive optimisers instead.

And the last block is the punchline. At zero initialisation $\sigma_{\max} = 0$, so the
formula is undefined and, if taken as a limit, claims "no restriction". Meanwhile the
gradient is exactly zero and *no* step size helps. The bound is vacuous precisely where
you most need guidance — which is the concrete reason Adam estimates its denominator from
the gradient history instead of computing a curvature estimate once.

</details>


**[ ] Exercise 5 — the total differential: first-order prediction and the size of what you
threw away.** Move a distance $d$ from a point $a$ along the *unit gradient*, and compare
the actual change in $f$ with the linear prediction $\|\nabla f\| \cdot d$.

(a) For $f(x,y) = x^2 + 3xy + y^2$ at $a = (1,2)$, with $\nabla f = (8,7)$,
$\hat u = \nabla f/\|\nabla f\|$ and $H = \begin{pmatrix}2&3\\3&2\end{pmatrix}$: show that
the error $\bigl|f(a+d\hat u) - f(a) - \nabla f\cdot d\hat u\bigr|$ equals exactly
$\tfrac12 d^2\,\hat u^{\mathsf T}H\hat u$ for every $d$, and report the constant.
(b) Tabulate predicted versus actual change for $d = 10^{-4}, 10^{-3}, 10^{-2}, 10^{-1},
0.2, 0.3, 0.5$, and confirm the error is exactly proportional to $d^2$.
(c) Repeat for $g(x,y) = \sin x\cos y$ at the same point. Here the ratio error$/d^2$ should
*drift* as $d$ grows. Explain why, and say which term of the expansion the drift reveals.
(d) In one paragraph: what breaks if you linearise at $a$ and use the linear model far from
$a$?

<details>
<summary>Solution</summary>

```python
import math

x0, y0 = 1.0, 2.0


def f(x, y):
    return x * x + 3 * x * y + y * y


def grad_f(x, y):
    return (2 * x + 3 * y, 3 * x + 2 * y)


def Hess_f(x, y):
    return [[2.0, 3.0], [3.0, 2.0]]


def g(x, y):
    return math.sin(x) * math.cos(y)


def grad_g(x, y):
    return (math.cos(x) * math.cos(y), -math.sin(x) * math.sin(y))


def Hess_g(x, y):
    return [[-math.sin(x) * math.cos(y), -math.cos(x) * math.sin(y)],
            [-math.cos(x) * math.sin(y), -math.sin(x) * math.cos(y)]]


def quadratic_form(H, v):
    return sum(v[i] * (H[i][0] * v[0] + H[i][1] * v[1]) for i in range(2))


print("(a)+(b) QUADRATIC: f = x^2 + 3xy + y^2.  The expansion has NO higher terms,")
print("    so error == (1/2) d^2 u^T H u exactly, for every d.")
gx, gy = grad_f(x0, y0)
gn = math.hypot(gx, gy)
u = (gx / gn, gy / gn)
H = Hess_f(x0, y0)
uTHu = quadratic_form(H, u)
print(f"  grad f(1,2) = ({gx:.7f}, {gy:.7f})   |grad f| = {gn:.7f}")
print(f"  u = ({u[0]:.7f}, {u[1]:.7f})   u^T H u = {uTHu:.7f}   half of it = {uTHu / 2:.7f}")
print(f"  f(1,2) = {f(x0, y0):.7f}")
print()
print("       d       predicted df         actual df             error        error/d^2")
for d in (1e-4, 1e-3, 1e-2, 1e-1, 0.2, 0.3, 0.5):
    pred = gn * d
    act = f(x0 + d * u[0], y0 + d * u[1]) - f(x0, y0)
    print(f"  {d:>7.1e} {pred:>16.10f} {act:>18.10f} {abs(act - pred):>14.3e}"
          f" {abs(act - pred) / d ** 2:>13.6f}")
print()
print("(c) NON-QUADRATIC: g = sin(x) cos(y).  Now there ARE higher-order terms.")
gx, gy = grad_g(x0, y0)
gn = math.hypot(gx, gy)
u = (gx / gn, gy / gn)
H = Hess_g(x0, y0)
uTHu = quadratic_form(H, u)
print(f"  grad g(1,2) = ({gx:.7f}, {gy:.7f})   |grad g| = {gn:.7f}")
print(f"  u^T H u = {uTHu:.7f}   half of it = {uTHu / 2:.7f}   <- the limiting error/d^2")
print()
print("       d       predicted df         actual df             error      error/d^2    drift")
for d in (1e-4, 1e-3, 1e-2, 1e-1, 0.2, 0.3, 0.5):
    pred = gn * d
    act = g(x0 + d * u[0], y0 + d * u[1]) - g(x0, y0)
    ratio = abs(act - pred) / d ** 2
    print(f"  {d:>7.1e} {pred:>16.10f} {act:>18.10f} {abs(act - pred):>14.3e}"
          f" {ratio:>12.5f} {ratio / (uTHu / 2):>9.5f}")
```

Output:

```text
(a)+(b) QUADRATIC: f = x^2 + 3xy + y^2.  The expansion has NO higher terms,
    so error == (1/2) d^2 u^T H u exactly, for every d.
  grad f(1,2) = (8.0000000, 7.0000000)   |grad f| = 10.6301458
  u = (0.7525767, 0.6585046)   u^T H u = 4.9734513   half of it = 2.4867257
  f(1,2) = 11.0000000

       d       predicted df         actual df             error        error/d^2
  1.0e-04    0.0010630146      0.0010630394         2.487e-08     2.486726
  1.0e-03    0.0106301458      0.0106326325         2.487e-06     2.486726
  1.0e-02    0.1063014581      0.1065501307         2.487e-04     2.486726
  1.0e-01    1.0630145813      1.0878818379         2.487e-02     2.486726
  2.0e-01    2.1260291625      2.2254981891         9.947e-02     2.486726
  3.0e-01    3.1890437438      3.4128490536         2.238e-01     2.486726
  5.0e-01    5.3150729064      5.9367543223         6.217e-01     2.486726

(c) NON-QUADRATIC: g = sin(x) cos(y).  Now there ARE higher-order terms.
  grad g(1,2) = (-0.2248451, -0.7651474)   |grad g| = 0.7974998
  u^T H u = 0.0843845   half of it = 0.0421922   <- the limiting error/d^2

       d       predicted df         actual df             error      error/d^2    drift
  1.0e-04    0.0000797500      0.0000797504         4.218e-10     0.04218    0.99927
  1.0e-03    0.0007974998      0.0007975418         4.202e-08     0.04202    0.99596
  1.0e-02    0.0079749976      0.0079790450         4.047e-06     0.04047    0.95903
  1.0e-01    0.0797499757      0.0800005329         2.506e-04     0.02506    0.59405
  2.0e-01    0.1594999514      0.1598223217         3.224e-04     0.00806    0.19105
  3.0e-01    0.2392499271      0.2384647691         7.852e-04     0.00872    0.20677
  5.0e-01    0.3987498785      0.3884079634         1.034e-02     0.04137    0.98054
```

(a) For a quadratic the first-order expansion plus the second-order term is the whole
function, so the remainder vanishes identically and the error is *exactly*
$\tfrac12 d^2 \hat u^{\mathsf T}H\hat u$. With $\hat u = (0.7525767, 0.6585046)$ and
$H = \begin{pmatrix}2&3\\3&2\end{pmatrix}$:

$$\hat u^{\mathsf T}H\hat u = 2u_x^2 + 6u_xu_y + 2u_y^2 = 2(0.566372) + 6(0.495573) + 2(0.433630) = 4.973451,$$

so the error is $\tfrac12\cdot 4.973451\cdot d^2 = 2.486726\,d^2$.

(b) The last column confirms it: error$/d^2$ reads `2.486726` at every single value of $d$
from $10^{-4}$ to $0.5$, a range of four decades. There is no drift, no $d^3$ term, no
lost precision — the linear model is *exactly* wrong by a known quadratic amount. Note
how bad it gets: at $d = 0.5$ the predicted rise is `5.31507291` and the actual rise is
`5.93675432`, an error of `6.217e-01`, or **11.7% of the prediction**. A linearisation
that is 12% wrong over half a unit of travel is not a model you can iterate.

(c) For $g(x,y)=\sin x\cos y$ the ratio error$/d^2$ starts at `0.04218` for
$d = 10^{-4}$ — which is the predicted $\tfrac12\hat u^{\mathsf T}H\hat u = 0.0421922$ to
five digits — and then *drifts* to `0.02506`, `0.00806`, `0.00872` before returning to
`0.04137` at $d = 0.5$. The drift factor (the last column) falls as far as `0.19105` at
$d = 0.2$. The reason is the third-order term: for a non-quadratic,
$g(a + d\hat u) = g(a) + d\nabla g\cdot\hat u + \tfrac12 d^2\hat u^{\mathsf T}H\hat u +
O(d^3)$, so error$/d^2 \to \tfrac12\hat u^{\mathsf T}H\hat u$ only as $d\to0$, and
drifts by an amount of order $d$ away from there. The non-monotone wiggle at
$d = 0.2$ and $0.3$ is the third-order term crossing zero — the error is nearly cancelled
there, which is a coincidence of this function, not a trend.

(d) The linearisation is only a *local* statement: $f(a+h) = f(a)+\nabla f\cdot h +
o(\lVert h\rVert)$. The relative error of the model is $\tfrac12\lVert h\rVert
\lvert\hat u^{\mathsf T}H\hat u\rvert / \lVert\nabla f\cdot\hat u\rVert$, which grows
like $\lVert h\rVert$ — so the model degrades linearly in the distance you trust it. Three
concrete failures follow. A line search that evaluates the linear model to pick a step is
optimising the wrong function, and the step it picks can *increase* $f$; in the
quadratic above, the predicted change is monotone but the actual change at $d=0.3$ is
`3.4128490536` against a prediction of `3.1890437438`. Newton's method, which is
"linearise, then solve the linearisation exactly", is *defined* by being valid only near
$a$, which is why it takes a fresh step from the new point instead of one long step from
the start. And any bound that grows like the squared distance — the trapezoid-style error
estimates of [52](../part04_calculus/52_integration.md), or a Hessian-based step-size cap — is silently void
once the model is used far enough away.

</details>

**[ ] Exercise 6 — Challenge: locate the exact stability boundary, and rescue it with
backtracking.** Take $f(x,y) = (x-3)^2 + 4(y+1)^2$ with
$\nabla f = (2(x-3), 8(y+1))$ and start at $(0, 5)$.

(a) Write the two coordinate recurrences explicitly and derive the exact stability
boundary from them, not from a theorem.
(b) Sweep the step size across the boundary in fine increments and classify each run.
Report the final $y$, $f$, and step count.
(c) Show that at the boundary the $y$ coordinate's error is preserved *exactly*, forever,
by printing several consecutive values of $y+1$.
(d) Add an Armijo backtracking line search with $c = 10^{-4}$ and halving, starting from
an absurd $\eta_0$ of $1.0$ and then `100.0`. Report steps and total backtracks.
(e) Explain in one paragraph why $2/L$ is only an estimate for a non-quadratic $f$, using
Exercise 4(d)'s network as the counterexample.

<details>
<summary>Solution</summary>

```python
import math


def f(x, y):
    return (x - 3.0) ** 2 + 4.0 * (y + 1.0) ** 2


def grad(x, y):
    return (2.0 * (x - 3.0), 8.0 * (y + 1.0))


def run(lr, steps=200, tol=1e-14):
    x, y = 0.0, 5.0
    for k in range(steps):
        gx, gy = grad(x, y)
        if math.hypot(gx, gy) < tol:
            return x, y, k, "converged"
        x, y = x - lr * gx, y - lr * gy
        if not math.isfinite(x) or abs(x) > 1e6:
            return float("inf"), float("inf"), steps, "DIVERGED"
    return x, y, steps, "hit the step cap"


print("f = (x-3)^2 + 4(y+1)^2, grad = (2(x-3), 8(y+1)).  Per-coordinate contraction:")
print("  x_{k+1} - 3  = (1 - 2*lr) * (x_k - 3)")
print("  y_{k+1} + 1  = (1 - 8*lr) * (y_k + 1)      <- needs |1 - 8*lr| < 1")
print("  so  0 < lr < 2/8 = 0.25.   L = 8 is the largest eigenvalue of diag(2, 8).")
print()
print("     lr    1-2*lr    1-8*lr        final x          final y              f    steps  verdict")
for lr in (0.20, 0.24, 0.249, 0.25, 0.251, 0.26, 0.30, 0.50):
    x, y, k, verdict = run(lr)
    shown = f"{f(x, y):.3e}" if math.isfinite(x) else "inf"
    ys = f"{y:.6f}" if abs(y) < 1e7 else "overflowed"
    print(f"  {lr:>6.3f} {1 - 2 * lr:>9.3f} {1 - 8 * lr:>9.3f} {x:>13.6f} {ys:>17} "
          f"{shown:>11} {k:>6}  {verdict}")
print()
print("(c) at lr = 0.25 exactly: 1 - 8*0.25 = -1, so (y+1) just flips sign.")
x, y = 0.0, 5.0
print("   k             y            y - (-1) = y + 1")
for k in range(6):
    print(f"  {k:>3} {y:>13.6f} {y + 1:>18.6f}")
    gx, gy = grad(x, y)
    x, y = x - 0.25 * gx, y - 0.25 * gy
print("  |y + 1| is 6.000000 at every step, forever: no damping, no growth.")
print()


def backtrack(lr0, c=1e-4, steps=300, tol=1e-14):
    """Armijo: accept the first halved step with f(x - lr*g) <= f(x) - c*lr*||g||^2."""
    x, y = 0.0, 5.0
    total_backtracks = 0
    for k in range(steps):
        gx, gy = grad(x, y)
        if math.hypot(gx, gy) < tol:
            return x, y, k, total_backtracks
        f0 = f(x, y)
        lr, bt = lr0, 0
        while True:
            nx, ny = x - lr * gx, y - lr * gy
            if math.isfinite(nx) and f(nx, ny) <= f0 - c * lr * (gx * gx + gy * gy):
                break
            lr *= 0.5
            bt += 1
            if bt > 60:
                return float("inf"), float("inf"), k, total_backtracks
        total_backtracks += bt
        x, y = nx, ny
    return x, y, steps, total_backtracks


print("(d) Armijo backtracking, c = 1e-4, halving on rejection:")
print("   lr0     steps   total backtracks        final (x, y)              f")
for lr0 in (0.2, 0.25, 1.0, 100.0):
    x, y, k, bt = backtrack(lr0)
    shown = f"{f(x, y):.3e}" if math.isfinite(x) else "inf"
    print(f"  {lr0:>7} {k:>7} {bt:>18}   ({x:>11.8f}, {y:>11.8f})  {shown:>11}")
```

Output:

```text
f = (x-3)^2 + 4(y+1)^2, grad = (2(x-3), 8(y+1)).  Per-coordinate contraction:
  x_{k+1} - 3  = (1 - 2*lr) * (x_k - 3)
  y_{k+1} + 1  = (1 - 8*lr) * (y_k + 1)      <- needs |1 - 8*lr| < 1
  so  0 < lr < 2/8 = 0.25.   L = 8 is the largest eigenvalue of diag(2, 8).

     lr    1-2*lr    1-8*lr        final x          final y              f    steps  verdict
  0.200      0.600     -0.600      3.000000        -1.000000    5.128e-30     71  converged
  0.240      0.520     -0.920      3.000000        -1.000000    4.715e-13    200  hit the step cap
  0.249      0.502     -0.992      3.000000         0.203610    5.795e+00    200  hit the step cap
  0.250      0.500     -1.000      3.000000         5.000000    1.440e+02    200  hit the step cap
  0.251      0.498     -1.008      3.000000        28.529607    3.488e+03    200  hit the step cap
  0.260      0.480     -1.080      3.000000  overflowed         inf    200  DIVERGED
  0.300      0.400     -1.400      3.000000  overflowed     4.070e+60    200  hit the step cap
  0.500      0.000     -3.000      3.000000  overflowed     1.016e+193    200  hit the step cap

(c) at lr = 0.25 exactly: 1 - 8*0.25 = -1, so (y+1) just flips sign.
   k             y            y - (-1) = y + 1
    0     5.000000             6.000000
    1    -7.000000            -6.000000
    2     5.000000             6.000000
    3    -7.000000            -6.000000
    4     5.000000             6.000000
    5    -7.000000            -6.000000
  |y + 1| is 6.000000 at every step, forever: no damping, no growth.

(d) Armijo backtracking, c = 1e-4, halving on rejection:
   lr0     steps   total backtracks        final (x, y)              f
      0.2      71                   0   (  3.00000000,  -1.00000000)   5.128e-30
    0.25      50                   1   (  3.00000000,  -1.00000000)   1.597e-29
      1.0       6                  12   (  3.00000000,  -1.00000000)   0.000e+00
    100.0      68                 610   (  3.00000000,  -1.00000000)   3.944e-30
```

(a) Substituting the gradient gives two independent one-dimensional recursions, because
$f$ is separable in $x$ and $y$:

$$x_{k+1} - 3 = \bigl(1 - 2\eta\bigr)(x_k - 3), \qquad
y_{k+1} - (-1) = \bigl(1 - 8\eta\bigr)\bigl(y_k - (-1)\bigr).$$

Each error therefore contracts by a fixed factor per step, and convergence requires
$\lvert 1-2\eta\rvert<1$ *and* $\lvert 1-8\eta\rvert<1$. The binding one is the $y$
coordinate: $\lvert 1-8\eta\rvert<1$ gives $0<\eta<1/4$. Since the Hessian is
$\operatorname{diag}(2,8)$, that is exactly $2/\lambda_{\max}$ with $\lambda_{\max}=8$ —
but here we derived it from the recurrences, so it is a fact about this problem rather
than a theorem imported from elsewhere.

(b) The sweep confirms the boundary precisely. At `0.20` the run converges in `71` steps
to $f = 5.128\times10^{-30}$. At `0.24` it is *still* converging but far too slowly —
`200` steps without reaching the `1e-14` gradient tolerance, because $y$ alternates sign
with amplitude shrinking by only `0.92` each step. At `0.249` it does not converge at all:
$1-8\eta = -0.992$ still flips the sign but shrinks by only `0.992`, so after 200 steps
$y$ has only fallen from `5.000000` to `0.203610` and $f$ is `5.795e+00` — a "stalled"
run that a careless implementation would report as success. At exactly `0.250` the factor
is $-1$: no damping whatsoever, $y$ bounces between `5.000000` and `-7.000000`, and $f$
sits at `1.440e+02 = 4\cdot 6^2`. At `0.251` the factor is $-1.008$ and $y$ has grown to
`28.529607` with $f = 3.488e+03`; by `0.260` it has overflowed to `inf`.

(c) The table is the cleanest statement of the marginal case. Because
$1 - 8(0.25) = -1$ *exactly* — and `0.25` is exactly representable in binary, so this is
not rounding — the recurrence is $y_{k+1}+1 = -(y_k+1)$. Starting from $y_0 = 5$ the
sequence of $y+1$ is $6, -6, 6, -6, \dots$ forever. The magnitude is *preserved exactly*:
$6.000000$ at every step. This is a genuine periodic orbit of period 2, and it is the
worst possible failure mode for a naive implementation because $|f|$ never grows, no
`OverflowError` is ever raised, and a loop with only a `step_cap` looks like it is
working. Note also that the $x$ coordinate converges perfectly throughout (`3.000000` at
every step size), because $1-2\eta \ne -1$ anywhere in this range — so the "final answer"
is half-converged and half-abandoned.

(d) The Armijo condition is $f(x_k - \eta\nabla f) \le f(x_k) - c\eta\lVert\nabla f\rVert^2$
with $c=10^{-4}$: accept only a step with a *sufficient decrease*. The results are
striking. Starting from a sensible $\eta_0 = 0.2$ needs `71` steps and *zero*
backtracks. Starting from the marginal $\eta_0 = 0.25$ needs only `50` steps and exactly
`1` backtrack — the line search rejects the boundary step on the very first iteration,
because at $\eta=0.25$ the $y$ part of $f$ does not decrease at all, which fails
$c\eta\lVert\nabla f\rVert^2 > 0$. Starting from $\eta_0 = 1.0$, which diverges outright
in Block 2, needs `6` steps and `12` backtracks — two halvings per step on average — and
lands at $f = 0$. Even $\eta_0 = 100.0$, absurd by any measure, converges: `68` steps and
`610` backtracks, i.e. about nine halvings per step, still ending at `3.944e-30`. The
whole point is that the line search does not require you to know $L$: it *measures*
whether the step was too big and corrects locally. That is why every production optimiser
ships some version of it.

(e) $2/L$ is a statement about the eigenvalues of $\nabla^2f$, and for a general
non-quadratic the Hessian is neither constant nor available. Exercise 4(d)'s network makes
this concrete: there the true Hessian is

$$H = W_2^{\mathsf T}\mathrm{diag}(1-h^2)W_1 + \sum_i (z_i-t_i)H_i,$$

so $\sigma_{\max}(W_1)$ alone misses the $\operatorname{sech}^2 < 1$ shrinkage of the
activation and the contribution of $W_2$. The measured numbers show the prediction is
right in order and even right in sign of the effect: $\sigma_{\max}(W_1) = 0.599029$ gives
$2/\sigma_{\max} = 3.3387$, which correctly separates `lr = 1.0` (converges to
`6.298237e-20`) from `lr = 2.0` (`inf`). But it is not the boundary — the true boundary
lies between `1.0` and `2.0`, and nothing in the formula says where. Worse, at zero
initialisation $\sigma_{\max}(W_1) = 0.000000`, so $2/\sigma_{\max}$ is undefined and, read
as a limit, claims *no restriction* — while the gradient is also identically zero and no
step size helps at all. The bound is vacuous exactly where you most need guidance, which is
the concrete reason Adam estimates its denominator from the gradient history rather than
computing a curvature estimate once.

</details>
---

## Summary

- A partial derivative holds every other coordinate fixed; the gradient collects all of
  them into one vector.
- The gradient points in the direction of steepest ascent, with magnitude equal to the
  largest directional derivative — a direct consequence of Cauchy–Schwarz.
- The gradient is always perpendicular to the level set through its base point, which is
  why gradient descent cuts across contours rather than sliding along them.
- The multivariable chain rule is $\nabla(f\circ g) = J_g^{\mathsf T}\nabla f$: the same
  product rule as one variable, now a transpose-times-vector.
- The Jacobian generalises the gradient to vector-valued outputs; when the output is
  scalar, the Jacobian *is* the gradient.
- Backpropagation for a linear layer is one matrix multiply with the transpose — no
  differentiation rules needed at that layer at all.
- $\text{curl}(\nabla f) = 0$ always. This is what makes gradients integrable and
  exchangeable, and it is the condition adjoint methods rely on.
- A step size above $2/\lambda_{\max}$ diverges; at exactly $2/\lambda_{\max}$ it oscillates
  without damping, which is why production code clips or searches rather than trusting a
  single constant.
- One learning rate cannot serve a whole landscape: the code shows the required step
  ranging from `0.0019` to `2.5` across four simple functions.
- Zero-initialising a symmetric network makes every gradient exactly zero and the
  parameters never move — the dormant-unit problem, and the reason frameworks default to
  Kaiming initialisation.

## Next

[54 — Taylor Series](../part04_calculus/54_taylor_series.md) answers the question this lesson kept
gesturing at: why does linearisation describe a function near a point, how big is the
error, and what happens when you truncate a series in floating point and lose every digit
you have.