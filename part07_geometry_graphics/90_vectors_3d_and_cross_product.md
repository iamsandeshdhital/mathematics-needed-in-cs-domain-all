# 90 — Vectors in 3D and the Cross Product

**Part**: part07_geometry_graphics · **Prerequisites**: 31, 37 · **Time**: 30 min

---

## In Plain Words

A 3D vector is three numbers. That is the whole idea. Point `(2, 1, 5)` is a
vector, and so is the direction "one step right, one step up, five steps
forward". Adding two vectors component by component gives the vector that
represents doing both movements in turn. Taking the square root of the sum of
the squared components gives its length.

The dot product of two vectors tells you how much one points in the direction of
the other: large and positive when they agree, negative when they oppose, zero
when they are at right angles. It is the tool for measuring angles and for
finding how far a point sits from a wall.

The cross product is the tool for orientation. Given two vectors it returns a
third vector standing at right angles to both of them, with a direction decided
by your right hand. Its length is not arbitrary — it equals the area of the flat
parallelogram you get by sticking the two vectors out from the same corner. This
single operation gives you plane normals, face orientations in a mesh, the
direction a surface is facing, and the volume of a box built from three vectors.
Almost every graphics and physics engine leans on it thousands of times per
frame.

## Why Computer Science Cares

- **Triangle winding and back-face culling.** OpenGL and Direct3D decide whether
  you are looking at the front or back of a triangle from the sign of the cross
  product of two of its edges. Get the vertex order wrong and the whole model
  renders inside out.
- **Physics engines.** Collision response between a box and a plane, contact
  normals for a character controller, and torque as a cross product
  `r × F` all reduce to this operation.
- **Robotics.** The denominator of a Jacobian in a 6-DOF robot arm is the
  scalar triple product. When it is near zero the arm is at a singularity —
  in software this is a division by a tiny number and an arm that suddenly
  moves at infinite speed.
- **Computer vision.** Estimating a plane from a point cloud usually starts with
  a covariance matrix from the [PCA lesson](../part03_linear_algebra/40_svd_and_pca.md);
  the plane normal is its smallest eigenvector.
- **Terrain and level design.** Slope of a heightmap cell is computed from the
  cross product of the two edge vectors of the cell.
- **Interview staple.** "Given two 3D line segments, find the closest points on
  them" is a standard hard question, and it is a cross-product and linear-system
  exercise.

## The Formal Version

Notation follows [SYMBOLS.md](../../SYMBOLS.md).

**Definition.** A *vector* in ℝ³ is a triple **v** = (v₁, v₂, v₃) ∈ ℝ³. Vector
addition is componentwise: (**u** + **v**)ᵢ = uᵢ + vᵢ. Scalar multiplication is
(λ**v**)ᵢ = λvᵢ. The zero vector **0** = (0, 0, 0) is the additive identity and
has **u** + **0** = **u**.

**Definition.** The *dot product* (inner product) is

**u** · **v** = u₁v₁ + u₂v₂ + u₃v₃.

**Definition.** The *norm* is ‖**v**‖ = √(**v** · **v**) = √(v₁² + v₂² + v₃²).
A vector with ‖**v**‖ = 1 is a *unit vector*.

**Theorem (Cauchy–Schwarz).** For all **u**, **v** ∈ ℝ³, |**u** · **v**| ≤ ‖**u**‖ ‖**v**‖,
with equality exactly when **u** and **v** are parallel.

**Why this matters.** Divide the inequality by the two norms to get
**u** · **v** = ‖**u**‖ ‖**v**‖ cos θ, the familiar formula. The theorem is the
formal reason the dot product *can* be read as an angle. If you ever implement
something like `dot(u, v) / (norm(u) * norm(v))` and get a value outside [−1, 1],
the inequality says your arithmetic is wrong, not that the maths is broken.

**Definition.** The *cross product* is

**u** × **v** = (u₂v₃ − u₃v₂,  u₃v₁ − u₁v₃,  u₁v₂ − u₂v₁).

**Theorem (properties of the cross product).**

1. **Orthogonality.** (**u** × **v**) · **u** = 0 and (**u** × **v**) · **v** = 0.
2. **Antisymmetry.** **v** × **u** = −(**u** × **v**).
3. **Magnitude.** ‖**u** × **v**‖ = ‖**u**‖ ‖**v**‖ sin θ = 2·area of the triangle
   with sides **u**, **v**.
4. **Parallel inputs.** If **u** × **v** = **0** then **u** and **v** are
   parallel (including the degenerate case where one is **0**).
5. **Distributivity.** **u** × (**v** + **w**) = **u** × **v** + **u** × **w**.

**Explanation.** Property 1 falls straight out of the expansion. Expand
(**u** × **v**) · **u** and the two u₁ terms cancel, and so do the two u₂ and u₃
terms. Property 2 is visible term by term: swapping the inputs swaps the two
subtracted terms in each component. Property 4 matters computationally — the
zero cross product is your test for "these two things point the same way", which
is how you detect parallel segments and degenerate triangles.

**Definition.** The *scalar triple product* of **u**, **v**, **w** ∈ ℝ³ is
(**u** × **v**) · **w**.

**Theorem (volume).** |(**u** × **v**) · **w**| is the volume of the
parallelepiped with edges **u**, **v**, **w**. Divided by 6, it is the volume of
the tetrahedron (four-sided pyramid) spanned by **0**, **u**, **v**, **w**.

**Explanation.** (**u** × **v**) is perpendicular to the base spanned by **u**
and **v**, with length equal to that base's area. So it is a valid height vector
for the parallelepiped, and volume = base area × height = ‖**u** × **v**‖ ·
|(**u** × **v**) · **w**| / ‖**u** × **v**‖ = |(**u** × **v**) · **w**|. The sign
records handedness, and swapping two arguments flips it.

**Definition.** A *plane* in ℝ³ is the set **P** = {**x** ∈ ℝ³ : **n** · **x** = d}
for a nonzero **n** (the *normal*) and scalar d.

**Theorem.** Three non-collinear points **p**₀, **p**₁, **p**₂ determine exactly
one plane, whose normal is **n** = (**p**₁ − **p**₀) × (**p**₂ − **p**₀) and whose
offset is d = **n** · **p**₀.

**Theorem (distance).** If ‖**n**‖ = 1 then the signed distance from a point
**q** to the plane is **n** · **q** − d; the absolute value is the distance. If
‖**n**‖ ≠ 1 the correct formula is (**n** · **q** − d) / ‖**n**‖.

**Theorem (reflection).** Mirroring a point **q** across the plane
**n** · **x** = d with **n** a unit vector gives
**q**′ = **q** − 2(**n** · **q** − d)**n**.

## Worked Example

Take three points in the scene: a triangle with corners

A = (0, 0, 0),  B = (4, 0, 0),  C = (0, 3, 0).

**Step 1 — two vectors inside the triangle.** Pull both edges to the same origin:

**u** = B − A = (4 − 0, 0 − 0, 0 − 0) = (4, 0, 0)
**v** = C − A = (0 − 0, 3 − 0, 0 − 0) = (0, 3, 0)

**Step 2 — the normal.** Cross them:

- first component: u₂v₃ − u₃v₂ = (0)(0) − (0)(3) = 0
- second component: u₃v₁ − u₁v₃ = (0)(0) − (4)(0) = 0
- third component: u₁v₂ − u₂v₁ = (4)(3) − (0)(0) = 12

**n** = (0, 0, 12). The face points straight up, which is what you expect of a
triangle lying flat on the ground.

**Step 3 — the offset.** d = **n** · A = (0)(0) + (0)(0) + (12)(0) = 0. So the
plane is (0, 0, 12) · (x, y, z) = 0, i.e. z = 0.

**Step 4 — normalise, because distances need a unit normal.** ‖**n**‖ = 12, so

**n̂** = (0, 0, 1),  d̂ = 0.

**Step 5 — distance of a point above the floor.** Let P = (1, 1, 5).

**n̂** · P − d̂ = 0 + 0 + 5 − 0 = 5.

So the point is 5 units above the floor. Positive means on the side the normal
points to.

**Step 6 — the triangle's area, straight from the cross product.**
‖**u** × **v**‖ = 12, and area = 12 / 2 = 6. Check by hand: a right triangle
with legs 4 and 3 has area (4·3)/2 = 6. The cross product never needed to know
that the triangle was right-angled.

**Step 7 — volume of a tetrahedron.** Add a fourth vertex D = (4, 3, 6) and use
**w** = D − A = (4, 3, 6):

(**u** × **v**) · **w** = (0, 0, 12) · (4, 3, 6) = 0 + 0 + 72 = 72.
Volume = 72 / 6 = 12.

**Step 8 — mirror a bouncing ball.** Reflect (1, 1, 5) off the floor:
P′ = (1, 1, 5) − 2(5)(0, 0, 1) = (1, 1, −5). Only the z component changed,
which is exactly right: a ball hitting a flat floor bounces straight back up.

## Runnable Code

Vector arithmetic and the cross product, in plain Python. Nothing here needs a
package.

```python
from math import sqrt

# A vector in 3D is just three numbers.
a = (1.0, 0.0, 0.0)
b = (1.0, 1.0, 0.0)


def add(u, v):
    return (u[0] + v[0], u[1] + v[1], u[2] + v[2])


def sub(u, v):
    return (u[0] - v[0], u[1] - v[1], u[2] - v[2])


def scale(u, s):
    return (u[0] * s, u[1] * s, u[2] * s)


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def norm(u):
    return sqrt(dot(u, u))


def cross(u, v):
    """The cross product: a vector perpendicular to both u and v."""
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


x_axis = (1.0, 0.0, 0.0)
y_axis = (0.0, 1.0, 0.0)
z_axis = (0.0, 0.0, 1.0)

print("a =", a, " b =", b)
print("a + b =", add(a, b))
print("b - a =", sub(b, a))
print("3 * a =", scale(a, 3))
print("dot(a, b) =", dot(a, b))
print("norm(a) =", norm(a), " norm(b) =", round(norm(b), 6))

# Right-hand rule: fingers curl from the first vector to the second,
# and the thumb points along the cross product.
c = cross(x_axis, y_axis)
print("cross(x_axis, y_axis) =", c)
print("cross(y_axis, x_axis) =", cross(y_axis, x_axis))

d = cross(b, z_axis)
print("b =", b, " z =", z_axis)
print("cross(b, z) =", d, " norm =", round(norm(d), 6))

# The cross product is orthogonal to both inputs, and its length is the
# area of the parallelogram spanned by them.
cp = cross(b, z_axis)
print("dot(cp, b) =", dot(cp, b))
print("dot(cp, z_axis) =", dot(cp, z_axis))
print("area of parallelogram =", norm(cp))
print("|b| * |z| * sin(90 deg) =", norm(b) * norm(z_axis))
```

```
a = (1.0, 0.0, 0.0)  b = (1.0, 1.0, 0.0)
a + b = (2.0, 1.0, 0.0)
b - a = (0.0, 1.0, 0.0)
3 * a = (3.0, 0.0, 0.0)
dot(a, b) = 1.0
norm(a) = 1.0  norm(b) = 1.414214
cross(x_axis, y_axis) = (0.0, 0.0, 1.0)
cross(y_axis, x_axis) = (0.0, 0.0, -1.0)
b = (1.0, 1.0, 0.0)  z = (0.0, 0.0, 1.0)
cross(b, z) = (1.0, -1.0, 0.0)  norm = 1.414214
dot(cp, b) = 0.0
dot(cp, z_axis) = 0.0
area of parallelogram = 1.4142135623730951
|b| * |z| * sin(90 deg) = 1.4142135623730951
```

Note `dot(cp, b) = 0.0` and `dot(cp, z_axis) = 0.0` — that is property 1
verified numerically, not assumed.

### Volumes, planes, and distances

```python
from math import sqrt


def sub(u, v):
    return (u[0] - v[0], u[1] - v[1], u[2] - v[2])


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def cross(u, v):
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


def scalar_triple(u, v, w):
    """(u x v) . w -- the signed volume of the box spanned by u, v, w."""
    return dot(cross(u, v), w)


# Two points, and the displacement vectors from the origin to each.
o = (0.0, 0.0, 0.0)
p = (1.0, 1.0, 0.0)
q = (1.0, 0.0, 1.0)

u = sub(p, o)
v = sub(q, o)
w = (1.0, 1.0, 1.0)

print("u =", u, " v =", v, " w =", w)
print("u x v =", cross(u, v))
triple = scalar_triple(u, v, w)
print("scalar triple product =", triple)
print("parallelepiped volume =", abs(triple))
print("tetrahedron volume   =", abs(triple) / 6.0)

# Swapping two vectors flips the sign: orientation matters.
print("scalar triple(v, u, w) =", scalar_triple(v, u, w))

# --- Planes -------------------------------------------------------------
# Three non-collinear points determine a unique plane. Build two in-plane
# vectors, cross them for a normal, then solve for the offset.


def plane_from_points(p0, p1, p2):
    n = cross(sub(p1, p0), sub(p2, p0))
    d = dot(n, p0)  # plane is {x : n . x = d}
    return n, d


def plane_normalise(n, d):
    """Scale n and d together so that |n| = 1. Distance is then n.x - d."""
    length = sqrt(dot(n, n))
    return tuple(c / length for c in n), d / length


a = (0.0, 0.0, 0.0)
b = (1.0, 0.0, 0.0)
c = (0.0, 1.0, 0.0)

n, d = plane_from_points(a, b, c)
print()
print("p0 =", a, "p1 =", b, "p2 =", c)
print("normal =", n, " offset d =", d)
nn, dd = plane_normalise(n, d)
print("unit normal =", nn, " unit offset =", dd)

# Signed distance of an arbitrary point from the plane.
q = (0.0, 0.0, 5.0)
print("point q =", q)
print("signed distance q->plane =", dot(nn, q) - dd)


def reflect(v, n):
    """Mirror v across a plane with unit normal n."""
    return tuple(v[i] - 2.0 * dot(n, v) * n[i] for i in range(3))


print("reflect(q) across z=0 =", reflect(q, nn))
```

```
u = (1.0, 1.0, 0.0)  v = (1.0, 0.0, 1.0)  w = (1.0, 1.0, 1.0)
u x v = (1.0, -1.0, -1.0)
scalar triple product = -1.0
parallelepiped volume = 1.0
tetrahedron volume   = 0.16666666666666666
scalar triple(v, u, w) = 1.0

p0 = (0.0, 0.0, 0.0) p1 = (1.0, 0.0, 0.0) p2 = (0.0, 1.0, 0.0)
normal = (0.0, 0.0, 1.0)  offset d = 0.0
unit normal = (0.0, 0.0, 1.0)  unit offset = 0.0
point q = (0.0, 0.0, 5.0)
signed distance q->plane = 5.0
reflect(q) across z=0 = (0.0, 0.0, -5.0)
```

The negative triple product is not a bug. **u**, **v**, **w** here form a
left-handed basis, and the sign is recording exactly that.

### Line–segment distance

The most useful piece of geometry in a physics engine: how close are these two
segments, and where? Both closest points must lie *on* the segments, so both
parameters get clamped into [0, 1] and then alternately re-solved until they
agree.

```python
from math import sqrt

EPS = 1e-12


def sub(u, v):
    return (u[0] - v[0], u[1] - v[1], u[2] - v[2])


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def cross(u, v):
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


def segment_intersect(p, p2, q, q2, eps=1e-9):
    """Closest approach of two 3D segments.

    Returns (point_on_pq, point_on_qr, distance). If the segments cross,
    the two points coincide and the distance is 0.
    """
    d1 = sub(p2, p)  # direction of the first segment
    d2 = sub(q2, q)  # direction of the second segment
    r = sub(p, q)

    a = dot(d1, d1)
    e = dot(d2, d2)
    f = dot(d2, r)

    # Both segments are genuine (non-degenerate) here, so a > 0 and e > 0.
    if a <= eps or e <= eps:
        raise ValueError("degenerate segment")

    b = dot(d1, d2)
    c = dot(d1, r)

    denom = a * e - b * b
    if abs(denom) < eps:  # parallel: use s = 0 for the first segment
        s = 0.0
        t = f / e
    else:
        s = (b * f - c * e) / denom
        t = (a * f - b * c) / denom

    # Clamp both parameters into [0, 1] so we stay on the segments.
    s = min(1.0, max(0.0, s))
    t = min(1.0, max(0.0, t))
    # Clamping s can invalidate t; recompute t as the best point on qr.
    t = (b * s + f) / e
    t = min(1.0, max(0.0, t))
    # ...and re-clamp s given the new t.
    s = (b * t - c) / a
    s = min(1.0, max(0.0, s))

    closest_p = tuple(p[i] + s * d1[i] for i in range(3))
    closest_q = tuple(q[i] + t * d2[i] for i in range(3))
    dist = sqrt(sum((closest_p[i] - closest_q[i]) ** 2 for i in range(3)))
    return closest_p, closest_q, dist


# Two crossing segments in the z = 0 plane.
p, p2 = (-1.0, 0.0, 0.0), (1.0, 0.0, 0.0)  # along x, through the origin
q, q2 = (0.0, -1.0, 0.0), (0.0, 1.0, 0.0)  # along y, through the origin

cp, cq, dist = segment_intersect(p, p2, q, q2)
print("segment 1:", p, "->", p2)
print("segment 2:", q, "->", q2)
print("closest point on segment 1 =", tuple(round(v, 6) for v in cp))
print("closest point on segment 2 =", tuple(round(v, 6) for v in cq))
print("distance =", round(dist, 9))

# Two parallel segments at z = 0 and z = 3.
r, r2 = (-1.0, 0.0, 3.0), (1.0, 0.0, 3.0)
cp, cq, dist = segment_intersect(p, p2, r, r2)
print()
print("parallel case: distance =", round(dist, 9))

# Two skew segments: closest points are interior, distance is not zero.
s, s2 = (0.0, 1.0, -1.0), (0.0, 1.0, 2.0)  # along z at x=0, y=1
t, t2 = (0.0, 0.0, 0.5), (3.0, 0.0, 0.5)  # along x at z = 0.5
cp, cq, dist = segment_intersect(s, s2, t, t2)
print()
print("skew case:")
print("  closest on first  =", tuple(round(v, 6) for v in cp))
print("  closest on second =", tuple(round(v, 6) for v in cq))
print("  distance =", round(dist, 6))
```

```
segment 1: (-1.0, 0.0, 0.0) -> (1.0, 0.0, 0.0)
segment 2: (0.0, -1.0, 0.0) -> (0.0, 1.0, 0.0)
closest point on segment 1 = (0.0, 0.0, 0.0)
closest point on segment 2 = (0.0, 0.0, 0.0)
distance = 0.0

parallel case: distance = 3.0

skew case:
  closest on first  = (0.0, 1.0, 0.5)
  closest on second = (0.0, 0.0, 0.5)
  distance = 1.0
```

Read the skew case carefully. The first segment runs along z at x = 0, y = 1.
The second runs along x at z = 0.5, y = 0. They never touch. The closest point
on the first is the one directly above the closest point on the second, and the
gap is exactly 1 in y. If a physical object were dropped along that first
segment it would land on the second, and 1 is the penetration depth you would
use to resolve the collision.

### With Libraries

The same three operations, using `numpy`. Cross products and dot products become
one short expression, and the signed-distance computation vectorises across a
whole array of points, which is what a renderer or a broadphase actually needs.
This block requires numpy and is not runnable in the standard library alone.

```python
import numpy as np

a = np.array([1.0, 0.0, 0.0])
b = np.array([1.0, 1.0, 0.0])

print("np.cross(a, b) =", np.cross(a, b))
print("np.linalg.norm(a) =", np.linalg.norm(a))
print("a @ b =", a @ b)

# Stack vectors as rows of a 2x3 array; cross() applies to each pair.
pairs = np.array([[1.0, 0.0, 0.0], [1.0, 1.0, 0.0]])
print("row cross products:\n", np.cross(pairs, pairs[:, ::-1]))

# Matrices make the triple product a one-liner and are faster in bulk.
U = np.array([[1.0, 1.0, 0.0], [0.0, 1.0, 1.0], [1.0, 0.0, 1.0]])
print("det(U) =", np.linalg.det(U))
print("abs(det(U)) = 2.0  <- volume scale factor")

# Plane from three points, via SVD for a robust normal.
p0 = np.array([0.0, 0.0, 0.0])
p1 = np.array([1.0, 0.0, 0.0])
p2 = np.array([0.0, 1.0, 1.0])
n = np.cross(p1 - p0, p2 - p0)
n = n / np.linalg.norm(n)
print("unit normal =", n)

q = np.array([0.0, 0.0, 5.0])
signed = float(n @ (q - p0))
print("signed distance =", round(signed, 9))

# Vectorised signed distance for many points at once -- the shape a
# renderer or a collision broadphase actually wants.
pts = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 5.0], [0.0, 0.0, -2.0]])
print("signed distances =\n", np.round((pts - p0) @ n, 6))
```

```
np.cross(a, b) = [ 0.  0.  1.]
np.linalg.norm(a) = 1.0
a @ b = 1.0
row cross products:
 [[ 0. -1.  0.]
  [ 1. -1.  1.]]
det(U) = 2.0
abs(det(U)) = 2.0  <- volume scale factor
unit normal = [ 0.         -0.70710678  0.70710678]
signed distance = 3.535533906
signed distances =
 [ 0.        3.535534 -1.414214]
```

`det(U) = 2.0` deserves a second look. The determinant of a 3×3 matrix whose
*columns* are three edge vectors is exactly the signed volume they span — the
matrix form of the scalar triple product, which is why
`det([u v w]) == (u x v) . w`. That identity is how a physics engine computes
collision volume without ever writing out a cross product.

## Common Mistakes

**1. Forgetting the order of the operands.**

```python
cross = lambda u, v: (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
```

Wrong: `cross(a, b)` where the winding rule says the normal should point at
the camera. Right: `cross(b, a)` to flip it, since **v** × **u** = −(**u** × **v**).

Tempting because both "look like a normal of the same triangle", and the
difference is invisible until you look at the sign. **Never rely on memory for
the sign — compute both and pick the one that faces the viewer.**

**2. Using `cross(a, b)` to measure an angle.** The cross product does not
encode the angle between two vectors directly; it throws the angle away and
gives you a perpendicular. Angles come from the dot product:
`cos θ = (a · b) / (‖a‖ ‖b‖)`. This is tempting because "3D vector maths" feels
like one tool, but dot and cross answer different questions.

**3. Taking the distance to a plane with an unnormalised normal.** If you build
the normal from a triangle with big edges, ‖**n**‖ can be large, and
**n** · **q** − d will be huge and meaningless. Divide by ‖**n**‖, or normalise
**n** and d together once at setup. Tempting because the wrong version returns
a plausible-looking number instead of crashing.

**4. Clamping the segment parameters only once.** Solving for the closest pair
on two *infinite* lines is two independent formulas and you can clamp them once.
For *segments*, clamping s can push the best t outside [0, 1], so you must
re-solve and re-clamp alternately. Doing it once gives a wrong answer that still
looks plausible. Iterate the two lines a few times, or use the exact
two-variable box-constrained solve.

**5. Treating a zero cross product as an error.** `cross(a, b) == (0,0,0)` is a
valid, useful answer meaning *parallel*. Collinear input points, a
zero-area triangle, and two parallel segments all produce it. Check for it
explicitly and branch, rather than dividing by the norm and producing `nan`.

## Formula Sheet

Bold **u**, **v**, **w** are vectors in ℝ³; bold **p**, **q**, **p**₀, **p**₁,
**p**₂, **q**₂ are points; **n** is a plane normal; $\lambda$ and $d$ are
scalars; $s, t \in [0, 1]$ are parameters along a segment; $\theta$ is the
angle between two vectors.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| $\mathbf{0} = (0,0,0)$ | $\mathbf{u} + \mathbf{0} = \mathbf{u}$ | the vector that changes nothing when added | identity checks, initialising accumulators |
| $\mathbf{u} + \mathbf{v}$ | $(u_1+v_1,\; u_2+v_2,\; u_3+v_3)$ | add each pair of coordinates; walking along both displacements in turn | displacements, positions, centroids of a mesh |
| $\lambda\mathbf{u}$ | $(\lambda u_1,\; \lambda u_2,\; \lambda u_3)$ | scale a vector, or flip it if $\lambda < 0$ | normals, velocities, area scaling |
| $\mathbf{u} \cdot \mathbf{v}$ | $u_1v_1 + u_2v_2 + u_3v_3$ | multiply and add; how much $\mathbf{u}$ points along $\mathbf{v}$ | angles, projection lengths, signed plane distance |
| $\|\mathbf{u}\|$ | $\sqrt{\mathbf{u} \cdot \mathbf{u}} = \sqrt{u_1^2+u_2^2+u_3^2}$ | the length of $\mathbf{u}$ | lengths, areas, comparing magnitudes |
| $\hat{\mathbf{n}} = \mathbf{n} / \|\mathbf{n}\|$ | divide every component by the length | a normal of length exactly 1 | required before any distance formula; **requires $\mathbf{n} \ne \mathbf{0}$** |
| $\cos\theta$ | $\dfrac{\mathbf{u}\cdot\mathbf{v}}{\|\mathbf{u}\|\,\|\mathbf{v}\|}$ | the cosine of the angle between $\mathbf{u}$ and $\mathbf{v}$ | measuring angles; **requires both vectors nonzero**; result is in $[-1,1]$ |
| $\theta$ in radians | $\theta = \arccos\!\big(\mathbf{u}\cdot\mathbf{v} / (\|\mathbf{u}\|\|\mathbf{v}\|)\big)$ | turn that cosine back into an angle | converting to degrees, setting a camera's field of view |
| Cauchy–Schwarz | $\|\mathbf{u}\cdot\mathbf{v}\| \le \|\mathbf{u}\|\,\|\mathbf{v}\|$ | the dot product can never be bigger than the product of the lengths | a self-check: $\cos\theta$ outside $[-1,1]$ means the arithmetic is wrong |
| **$\mathbf{u} \times \mathbf{v}$** | $(u_2v_3 - u_3v_2,\; u_3v_1 - u_1v_3,\; u_1v_2 - u_2v_1)$ | the vector at right angles to both inputs, oriented by the right hand | face normals, surface direction, torque, triangle area; **only defined in ℝ³** |
| Orthogonality | $(\mathbf{u}\times\mathbf{v})\cdot\mathbf{u} = (\mathbf{u}\times\mathbf{v})\cdot\mathbf{v} = 0$ | the result is at right angles to both inputs | verifying a normal numerically |
| Antisymmetry | $\mathbf{v}\times\mathbf{u} = -(\mathbf{u}\times\mathbf{v})$ | swap the inputs and the result flips sign | correcting a winding-order mistake; the whole back-face-culling convention |
| Cross magnitude | $\|\mathbf{u}\times\mathbf{v}\| = \|\mathbf{u}\|\,\|\mathbf{v}\|\sin\theta$ | its length is the two lengths times the sine of the angle between them | area of a parallelogram, twice the area of a triangle |
| Triangle area | $A = \tfrac12\|\mathbf{u}\times\mathbf{v}\|$ | half the parallelogram area | mesh surface area, cross-section areas |
| Parallel test | $\mathbf{u}\times\mathbf{v} = \mathbf{0} \iff$ $\mathbf{u} \parallel \mathbf{v}$ | the cross product vanishes exactly when the vectors point the same or opposite way | detecting collinear points, degenerate triangles, parallel segments; compare $\|\mathbf{u}\times\mathbf{v}\|^2 \le \text{tol}^2$, never `== 0.0` |
| Distributivity | $\mathbf{u}\times(\mathbf{v}+\mathbf{w}) = \mathbf{u}\times\mathbf{v} + \mathbf{u}\times\mathbf{w}$ | the cross product distributes over addition | simplifying expressions; the reason the Laplacian distributes |
| Scalar triple product | $(\mathbf{u}\times\mathbf{v})\cdot\mathbf{w}$ | signed volume of the box on edges $\mathbf{u},\mathbf{v},\mathbf{w}$; negative = left-handed | orientation tests, volume, Jacobian determinants |
| Parallelepiped volume | $V = \|(\mathbf{u}\times\mathbf{v})\cdot\mathbf{w}\|$ | absolute value of the triple product | collision volumes, polyhedron volume |
| Tetrahedron volume | $V = \tfrac16\|(\mathbf{u}\times\mathbf{v})\cdot\mathbf{w}\|$ | one sixth of the box | volume of a pyramid or mesh simplex |
| Determinant identity | $\det[\mathbf{u}\ \mathbf{v}\ \mathbf{w}] = (\mathbf{u}\times\mathbf{v})\cdot\mathbf{w}$ | the determinant of the matrix whose *columns* are the three vectors | computing volume with matrix libraries, no cross product needed |
| Plane | $\mathbf{P} = \{\mathbf{x}\in\mathbb{R}^3 : \mathbf{n}\cdot\mathbf{x} = d\}$ | all points whose dot product with the normal is the constant $d$ | every plane in a scene; **requires $\mathbf{n} \ne \mathbf{0}$** |
| Normal from 3 points | $\mathbf{n} = (\mathbf{p}_1-\mathbf{p}_0)\times(\mathbf{p}_2-\mathbf{p}_0)$, $\; d = \mathbf{n}\cdot\mathbf{p}_0$ | cross two edges of the triangle to get the normal, dot it with any vertex for the offset | **requires three non-collinear points**; collinear input gives $\mathbf{n}=\mathbf{0}$ and a useless plane |
| Signed distance, unit normal | $\delta = \hat{\mathbf{n}}\cdot\mathbf{q} - \hat{d}$ | how far $\mathbf{q}$ sits from the plane, positive on the normal's side | penetration depth, back-face tests |
| Signed distance, any normal | $\delta = \dfrac{\mathbf{n}\cdot\mathbf{q} - d}{\|\mathbf{n}\|}$ | the same thing with the normal's length divided out; **requires $\mathbf{n} \ne \mathbf{0}$** | when you did not pre-normalise — forgetting the division is a silent, plausible-looking bug |
| Reflection | $\mathbf{q}' = \mathbf{q} - 2\,(\hat{\mathbf{n}}\cdot\mathbf{q}-\hat{d})\,\hat{\mathbf{n}}$ | push $\mathbf{q}$ twice its signed distance along the normal | bouncing balls, mirrors; **requires $\hat{\mathbf{n}}$ to be a unit vector** |
| Segment parameterisation | $\mathbf{p}(s) = \mathbf{p} + s\,\mathbf{d}_1$, $\;\mathbf{q}(t) = \mathbf{q} + t\,\mathbf{d}_2$ | walk along each segment by a fraction $s$ or $t$ | closest-pair search; $s,t \in [0,1]$ keeps you *on* the segments |
| Segment dot-product shorthand | $\mathbf{d}_1 = \mathbf{p}_2-\mathbf{p}$, $\mathbf{d}_2 = \mathbf{q}_2-\mathbf{q}$, $\mathbf{r} = \mathbf{p}-\mathbf{q}$; $a=\mathbf{d}_1\!\cdot\!\mathbf{d}_1$, $b=\mathbf{d}_1\!\cdot\!\mathbf{d}_2$, $c=\mathbf{d}_1\!\cdot\!\mathbf{r}$, $e=\mathbf{d}_2\!\cdot\!\mathbf{d}_2$, $f=\mathbf{d}_2\!\cdot\!\mathbf{r}$ | every dot product the solver needs, computed once | the inner loop of the routine above |
| Unconstrained parameters | $s = \dfrac{bf-ce}{ae-b^2}, \;\; t = \dfrac{af-bc}{ae-b^2}$ | where the closest points sit on the two *infinite* lines | first pass of the routine; **requires $ae-b^2 \ne 0$** |
| Parallel-segment branch | $ae - b^2 = 0 \iff \mathbf{d}_1 \parallel \mathbf{d}_2$ (Cauchy–Schwarz) | the denominator vanishes exactly when the segments are parallel; then set $s=0$, $t = f/e$ | branching instead of dividing by zero; $a>0$ and $e>0$ are also required (non-degenerate segments) |
| Clamp | $x \mapsto \min(1,\max(0,x))$ | force a parameter into $[0,1]$ | keeping the answer on the segments |
| Re-solve after clamping | $t \leftarrow (bs+f)/e$, then $s \leftarrow (bt-c)/a$, repeat | clamp one, fix the other, clamp the other | **must be iterated** — clamping $s$ can push the best $t$ out of range and vice versa |
| Closest-pair distance | $d = \|\mathbf{p}(s) - \mathbf{q}(t)\|$ | the gap at the converged $(s,t)$ | compare against a radius to answer "did they collide?" |
| Collision test | $d \le \text{radius}$ | the gap is within the tolerance | broadphase and narrowphase hit tests |
| Back-face test | $((\mathbf{p}_1-\mathbf{p}_0)\times(\mathbf{p}_2-\mathbf{p}_0)) \cdot (\mathbf{c}-\mathbf{p}_0) > 0$ | the triangle's right-hand normal points from the face toward the camera $\mathbf{c}$ | culling back faces; the sign depends on winding order |
| Outward normal | $\mathbf{n} \leftarrow -\mathbf{n}$ **iff** $\mathbf{n}\cdot(\mathbf{p}_{\text{inside}}-\mathbf{p}_0) > 0$ | flip the normal exactly when it leans toward a known interior point | winding-order-proof mesh normals; makes the result independent of vertex order |

## Multiple Choice Questions

**Q1.** Let **u** = (1, 2, 3) and **v** = (4, 5, 6). What is **u** × **v**?

- A) (−3, 6, −3)
- B) (3, −6, 3)
- C) (−8, −6, −4)
- D) (0, 0, 0)

<details>
<summary>Answer and explanation</summary>

**A) (−3, 6, −3).**

Expand component by component: first component $u_2v_3 - u_3v_2 = 2\cdot6 - 3\cdot5 = 12 - 15 = -3$; second $u_3v_1 - u_1v_3 = 3\cdot4 - 1\cdot6 = 12 - 6 = 6$; third $u_1v_2 - u_2v_1 = 1\cdot5 - 2\cdot4 = 5 - 8 = -3$. So (−3, 6, −3), which is what Exercise 1 prints.

B) (3, −6, 3) is **v** × **u** — the operands swapped. Antisymmetry says the two differ by a sign, so B is the same formula with the order reversed, and order is exactly the thing this question is testing.

C) (−8, −6, −4) comes from multiplying *matching* indices, $2\cdot5 - 3\cdot6$, $3\cdot4-1\cdot6$, $1\cdot5-2\cdot4$. That is the dot product's pattern of "same index, multiply, add" wrongly rewritten as a difference. The cross product deliberately pairs index 2 of **u** with index 3 of **v**, and index 3 of **v**'s partner with index 1 of **u**.

D) (0, 0, 0) is the answer you would get from believing the two vectors are parallel. **u** × **v** = **0** holds exactly when the inputs are parallel, and (1,2,3) and (4,5,6) are not: no single scalar makes them equal. "The components all increase together" is not a proportionality test.

</details>

**Q2.** A triangle's vertices arrive as `p0, p1, p2`. You compute `n = cross(p1 - p0, p2 - p0)` and find that **n** points *away* from the camera, so back-face culling discards a triangle that should be visible. What fixes it?

- A) Divide **n** by ‖**n**‖ to make it a unit vector
- B) Divide **n** by ‖**n**‖² to remove the triangle's area scale
- C) Compute `cross(p2 - p0, p1 - p0)` instead
- D) Rotate **n** by 180° about the **x** axis

<details>
<summary>Answer and explanation</summary>

**C) Compute `cross(p2 - p0, p1 - p0)` instead.**

Swapping the two operands negates the result, by antisymmetry: $\mathbf{v}\times\mathbf{u} = -(\mathbf{u}\times\mathbf{v})$. That is the whole fix, and it costs one transposition.

A) is wrong because scaling a vector by a positive number never changes its direction. Dividing by the length makes it a unit vector, which is what the *distance* formula needs, but the direction — the only thing that is wrong here — is untouched.

B) is wrong for the same reason, only with a different positive factor. Length does not encode which way a normal points; it encodes the triangle's area.

D) is wrong because a 180° rotation about **x** maps $(n_1, n_2, n_3)$ to $(n_1, -n_2, -n_3)$. That leaves the **x** component unchanged, so it does not in general produce $-\mathbf{n}$. It also destroys orthogonality to the triangle's plane whenever $n_1 \ne 0$. Rotations are not available here anyway — all you have is the three vertices.

</details>

**Q3.** With A = (0, 0, 0), B = (4, 0, 0), C = (0, 3, 0), set **u** = B − A and **v** = C − A. What number is $\|\mathbf{u}\times\mathbf{v}\|$, and what does that number represent?

- A) 12, the area of the triangle
- B) 24, the area of the triangle
- C) 12, the area of the parallelogram spanned by **u** and **v**
- D) 6, the area of the triangle

<details>
<summary>Answer and explanation</summary>

**C) 12, the area of the parallelogram spanned by **u** and **v**.**

**u** = (4, 0, 0), **v** = (0, 3, 0), so **u** × **v** = (0·0 − 0·3, 0·0 − 4·0, 4·3 − 0·0) = (0, 0, 12) and the magnitude is 12. Stick **u** and **v** out from a common corner and you get a 4 × 3 rectangle of area 12. By $\sin 90° = 1$ the magnitude formula also gives $\|\mathbf{u}\|\|\mathbf{v}\| = 4 \cdot 3 = 12$.

A) is the classic halving error: the triangle's area really is 6, but the cross product returns the *parallelogram* area, which is twice as big. B) is the mirror-image mistake — halve instead of doubling, or read $\|\mathbf{u}\times\mathbf{v}\|$ as the triangle area and double it by mistake, landing on 24. D) reports the right number for the right geometric quantity but the wrong answer to this question: 6 is $\tfrac12\|\mathbf{u}\times\mathbf{v}\|$, not the magnitude itself.

</details>

**Q4.** In Exercise 2 the plane normal is **n** = (35, −21, −2) with $d = 33$, so ‖**n**‖ ≈ 40.865633. You evaluate **n** · **q** − *d* at **q** = (0, 0, 0) and get −33. What have you actually computed?

- A) The true signed distance from **q** to the plane, −0.807524
- B) The signed distance multiplied by ‖**n**‖, so 40.8656 times too large in magnitude
- C) The true distance, but with the sign flipped because you subtracted in the wrong order
- D) The component of **q** along the un-normalised normal, which happens to equal the distance here

<details>
<summary>Answer and explanation</summary>

**B) The signed distance multiplied by ‖**n**‖, so 40.8656 times too large in magnitude.**

Since **n** · **q** − *d* is linear in **n** and in *d*, scaling the normal by a factor $k$ scales this quantity by $k$. The true signed distance is $(\mathbf{n}\cdot\mathbf{q} - d)/\|\mathbf{n}\| = -33/40.865633 \approx -0.807524$, exactly the value the lesson's code prints after normalising. The raw quantity is $40.865633$ times that.

A) is what you get *after* dividing by ‖**n**‖, so it is the right number attached to the wrong computation.

C) is wrong because there is no sign error in the arithmetic. The sign of −33 and the sign of −0.807524 agree; they are both negative, meaning the origin is on the far side of the plane from where the normal points.

D) confuses an un-normalised projection with a distance. "The component along the normal" is only a distance when the normal has length 1; with length 40.87 the projection is stretched by exactly that factor.

</details>

**Q5.** The lesson's code computes `scalar_triple(u, v, w) = -1.0` for **u** = (1, 1, 0), **v** = (1, 0, 1), **w** = (1, 1, 1). What does the minus sign mean?

- A) The three vectors are linearly dependent, so no box can be built from them
- B) The floating-point subtraction inside the cross product lost precision
- C) The three vectors span a left-handed basis, so the sign is recording orientation
- D) The tetrahedron volume is negative and must be wrapped in `abs()` before the sign can be interpreted

<details>
<summary>Answer and explanation</summary>

**C) The three vectors span a left-handed basis, so the sign is recording orientation.**

The magnitude 1.0 is nonzero, so the vectors are independent and the box is perfectly well defined. What is negative is the *signed* volume: det[**u** **v** **w**] = −1 < 0 means the ordered triple (**u**, **v**, **w**) has the opposite handedness to (**x**-axis, **y**-axis, **z**-axis). Swap any two of the three and the lesson's code prints `scalar triple(v, u, w) = 1.0`.

A) would require the value to be 0. Linear dependence is the zero case; the sign of a nonzero number never indicates dependence.

B) is wrong because nothing here is inexact: **u** × **v** = (1, −1, −1) and (1, −1, −1) · (1, 1, 1) = 1 − 1 − 1 = −1, which is exact in binary floating point. Floating-point error produces a wrong *magnitude*, not a clean sign flip.

D) has the right instinct — volume is $\lvert(\mathbf{u}\times\mathbf{v})\cdot\mathbf{w}\rvert$ — but wrong framing. Taking `abs()` is how you *discard* the orientation information, not how you unlock it. The tetrahedron's volume is 0.1667, and the sign is the extra payload that a bare `abs()` throws away.

</details>

**Q6.** Your code computes `cos_theta = dot(u, v) / (norm(u) * norm(v))` and gets **1.02**. What does that tell you?

- A) θ is a small angle, about 2.9°, since cos θ is close to 1
- B) θ is undefined, because the argument of `acos` exceeded 1
- C) At least one of the inputs, or the arithmetic producing them, is wrong: Cauchy–Schwarz forbids a dot-product ratio outside [−1, 1]
- D) `acos` needs its argument clamped into [0, 1], so clamp it and continue

<details>
<summary>Answer and explanation</summary>

**C) At least one of the inputs, or the arithmetic producing them, is wrong: Cauchy–Schwarz forbids a dot-product ratio outside [−1, 1].**

Dividing $\|\mathbf{u}\cdot\mathbf{v}\| \le \|\mathbf{u}\|\,\|\mathbf{v}\|$ by the two lengths gives $\lvert\cos\theta\rvert \le 1$ as a theorem, not an empirical observation. A value of 1.02 therefore cannot happen for exact inputs; it means a length was computed wrong, a component was read wrong, or one of the vectors is zero (in which case the denominator is 0 and the ratio is `nan` or `inf`, not 1.02). The inequality is your built-in assertion.

A) is the tempting reading of "cos is near 1". But 1.02 is not near 1, it is outside the range; and if the value really were 0.98 you would get $\arccos(0.98) \approx 11.5°$, so the "small angle" conclusion was never justified by the number you have.

B) treats the symptom as the diagnosis. `acos` does raise a domain error there, but that exception is the *bug detector*, not the bug. Chasing the exception instead of the inequality hides the real fault.

D) is what people reach for because clamping silences the error. Clamping turns a loud failure into a wrong answer that still looks like a plausible angle. Fix the inputs; never clamp a value that a theorem says must be in $[-1,1]$.

</details>

**Q7.** Why must the closest-point routine solve for $t$ again after clamping $s$?

- A) Because matrix multiplication is not associative, so the first $t$ is computed under a different parenthesisation
- B) Because clamping $s$ moves the first point to an endpoint, which can push the best $t$ outside $[0,1]$, and clamping *that* can push $s$ outside $[0,1]$ again
- C) Because the dot products $a, b, c, e, f$ were built from the unclamped $s$ and must be rebuilt from the clamped one
- D) Because $s$ and $t$ are direction vectors whose lengths change under clamping

<details>
<summary>Answer and explanation</summary>

**B) Because clamping $s$ moves the first point to an endpoint, which can push the best $t$ outside $[0,1]$, and clamping *that* can push $s$ outside $[0,1]$ again.**

On two *infinite* lines $s$ and $t$ are independent: solve once, done. Segments are different, because the pair $(s, t)$ must satisfy four inequalities at once, $0\le s\le 1$ and $0\le t\le 1$, and each clamp can violate the other variable's pair. Re-solve with $t = (bs+f)/e$, clamp, re-solve with $s = (bt-c)/a$, clamp, and iterate to a fixed point. Take the segment from (0,0,0) to (0,0,1) and the segment from (0,0,3) to (0,1,0): the unclamped solution is $s = 3.0$, $t = 0.0$; one clamp pass gives distance 2.0, while the converged answer is $s = 1.0$, $t = 0.6$ with distance 0.632455532. A single pass over-reports the gap by more than 3×.

A) is wrong because there is no matrix product here — the routine is six scalar dot products and four divisions. Associativity does not enter.

C) is wrong because $a, b, c, e, f$ depend only on the segment endpoints, which clamping never changes. They are correctly computed once and reused; the lesson's code computes them before the clamping loop for exactly this reason.

D) is wrong because $s$ and $t$ are scalars in $[0,1]$, not vectors. Clamping a parameter picks a *position* along a segment; the direction vectors $\mathbf{d}_1, \mathbf{d}_2$ are untouched.

</details>

**Q8.** Let **a** = (2, −1, 3), **b** = (0, 4, −2), **c** = (−1, 0.5, 2), and form the 3×3 matrix whose *columns* are **a**, **b**, **c**. What is its determinant, and how does it relate to the triple product?

- A) 28, and it equals (**a** × **b**) · **c**
- B) 28, and it equals ‖**a** × **b**‖, the parallelogram area
- C) 0, because no two of the three vectors are parallel
- D) −28, and it equals (**b** × **c**) · **a**

<details>
<summary>Answer and explanation</summary>

**A) 28, and it equals (**a** × **b**) · **c**.**

Both computations give 28.0. By hand, **a** × **b** = ((−1)(−2) − (3)(4), (3)(0) − (2)(−2), (2)(4) − (−1)(0)) = (2 − 12, 0 + 4, 8) = (−10, 4, 8), and (−10, 4, 8) · (−1, 0.5, 2) = 10 + 2 + 16 = 28. The determinant form is the same number because the determinant of a 3×3 matrix *is* its signed column volume, and this is the matrix statement of the triple product.

B) confuses volume with area. ‖**a** × **b**‖ = √(100 + 16 + 64) = √180 ≈ 13.416, and even that ignores **c** entirely — a volume that depends on only two of the three vectors cannot be right.

C) confuses "no two are parallel" with "the determinant is zero". A zero determinant means *linear dependence* — some **nontrivial** combination of the three vectors vanishes — which does not require any *pair* to be parallel. Three pairwise-nonparallel vectors in ℝ³ can still be coplanar through the origin. Here the determinant is a healthy 28.

D) gets the right idea (both expressions are the triple product) and the wrong sign. Permuting **three** vectors cyclically, (a,b,c) → (b,c,a), is an even permutation and leaves the value unchanged, so (**b** × **c**) · **a** = 28, not −28. Only a *swap of two* flips the sign.

</details>

**Q9.** Which of these is something the cross product computes that nothing else in the lesson does?

- A) The angle between two vectors
- B) A unit vector along the sum of two vectors
- C) A vector perpendicular to two non-parallel vectors
- D) The length of a vector

<details>
<summary>Answer and explanation</summary>

**C) A vector perpendicular to two non-parallel vectors.**

The cross product is the unique operation in this lesson that *constructs a new direction* rather than measuring one. Given two non-parallel inputs it returns the one direction that is orthogonal to both, with a length and a sign fixed by the right-hand rule. Everything else in the lesson takes existing vectors as input and returns a scalar.

A) is the dot product: $\cos\theta = (\mathbf{u}\cdot\mathbf{v})/(\|\mathbf{u}\|\|\mathbf{v}\|)$. The cross product throws the angle away entirely and returns a perpendicular instead, which is Common Mistake 2.

B) is two dot products and a square root. The unit vector along **u** + **v** is $(\mathbf{u}+\mathbf{v})/\|\mathbf{u}+\mathbf{v}\|$. No cross product appears, and the cross product cannot produce this result because its output is perpendicular to both inputs, not along their sum.

D) is $\sqrt{\mathbf{u}\cdot\mathbf{u}}$, which is Common Mistake 2's other half. Note the distinction is not academic: the *magnitude* of the cross product is an area, which is why it can exceed both input lengths.

</details>

**Q10.** `is_parallel(u, v)` is implemented as `dot(cross(u, v), cross(u, v)) <= tol * tol`. It reports `True` for **u** = (0, 0, 0) and **v** = (1, 2, 3). Is that a bug?

- A) Yes, because the zero vector is parallel to nothing
- B) No: **0** × **v** = **0** for every **v**, so the test is mathematically consistent. Filter zero-length inputs separately if that case matters for your application
- C) Yes, because the tolerance should have been compared against `tol`, not `tol * tol`
- D) No, but only because in IEEE 754 the cross product of exactly parallel vectors is guaranteed to come out as exactly `0.0`

<details>
<summary>Answer and explanation</summary>

**B) No: **0** × **v** = **0** for every **v**, so the test is mathematically consistent.**

The lesson states the equivalence plainly: **u** × **v** = **0** iff **u** and **v** are parallel, "including the degenerate case where one is **0**". Every component of **0** × **v** is a difference of zeros, so the result is exactly (0,0,0) and the test returns `True` for every input. Whether that is *desirable* is an application question, not a correctness question — and Exercise 3 says so directly, recommending a separate norm check for the zero vector.

A) is the informal reading of "parallel" as "goes the same way". The zero vector has no direction at all, so it neither agrees nor disagrees; the algebra settles it, and the algebra says the cross product is zero.

C) is wrong twice over. Comparing a squared magnitude against $\text{tol}^2$ is the standard, dimensionally consistent choice: $\lVert\mathbf{u}\times\mathbf{v}\rVert \le \text{tol}$ is equivalent to $\lVert\mathbf{u}\times\mathbf{v}\rVert^2 \le \text{tol}^2$ because both sides are nonnegative. And `tol * tol` is exactly the default parameter value `tol = 1e-12` used in the exercise, so nothing is out of step.

D) is a tempting and thoroughly wrong belief. Floating-point multiplication and subtraction of exactly equal values *does* give exact zero here, but that is irrelevant to why the answer is `True`: it would be `True` in exact arithmetic too, for every **v**. And the guarantee does not extend to merely *nearly* parallel inputs — which is the entire reason a tolerance exists, since $\lVert\mathbf{u}\times\mathbf{v}\rVert = \lVert\mathbf{u}\rVert\lVert\mathbf{v}\rVert\sin\theta$ is a product of rounding-prone quantities and rarely lands on exactly zero.

</details>

**Q11.** A renderer culls back faces. With **c** the camera position and a triangle (p₀, p₁, p₂), which expression is the correct front-facing test?

- A) `dot(cross(p1 - p0, p2 - p0), p0 - c) > 0`
- B) `dot(cross(p1 - p0, p2 - p0), c - p0) > 0`
- C) `dot(p1 - p0, p2 - p0) > 0`
- D) `dot(cross(c - p0, p0 - p1), p2 - p0) > 0`

<details>
<summary>Answer and explanation</summary>

**B) `dot(cross(p1 - p0, p2 - p0), c - p0) > 0`.**

The cross product gives the triangle's right-hand normal **n**, which by definition stands at right angles to the face. The dot product of **n** with `c - p0` is positive exactly when **n** leans toward the camera, i.e. the face is turned toward us. Negate it and you get the back-face case, which is what the rasteriser throws away. (The exact `>` versus `>=` convention is a pipeline choice; what matters is that all three operands are as written.)

A) uses `p0 - c` instead of `c - p0` — the vector from the camera to the triangle instead of the triangle to the camera. That is exactly the negated expression, so it classifies precisely the wrong set of triangles. This is the most common version of the bug, because both vectors connect the same two points and both look like "the direction between them".

C) drops the cross product entirely. `dot(p1 - p0, p2 - p0)` measures whether the triangle is acute or obtuse at **p**₀, a shape property that has nothing to do with where the viewer is. Put the camera at the origin, then far away along **z**, then inside the cube, and this expression never changes — which is exactly the failure.

D) is the clever trap. By the cyclic identity $(a\times b)\cdot c = (b\times c)\cdot a = (c\times a)\cdot b$, the vector part satisfies $(\mathbf{c}-\mathbf{p}_0)\times(\mathbf{p}_0-\mathbf{p}_1) = -(\mathbf{c}-\mathbf{p}_0)\times(\mathbf{p}_1-\mathbf{p}_0)$, and dotting with $(\mathbf{p}_2-\mathbf{p}_0)$ then gives precisely $-(\mathbf{n}\cdot(\mathbf{c}-\mathbf{p}_0))$. It looks like a harmless rearrangement; it is the exact negation.

</details>

## Subjective Questions

### Short Answer

**Q1. State the magnitude formula for the cross product, and say in words what the magnitude measures.**

<details>
<summary>Answer</summary>

$\|\mathbf{u}\times\mathbf{v}\| = \|\mathbf{u}\|\,\|\mathbf{v}\|\sin\theta$, where $\theta$ is the angle between the two vectors.

Geometrically it is the area of the parallelogram you get by placing **u** and **v** tail to tail. Because a triangle with sides **u** and **v** is exactly half of that parallelogram, the triangle's area is $\tfrac12\|\mathbf{u}\times\mathbf{v}\|$.

</details>

**Q2. Two of your inputs are parallel. What does the cross product return, and how should your code react?**

<details>
<summary>Answer</summary>

It returns (0, 0, 0). Antisymmetry and the orthogonality property together give: **u** × **v** = **0** iff **u** and **v** are parallel (or one of them is the zero vector).

In code, branch on it explicitly rather than carrying on. Normalising a zero normal divides by zero and produces `nan`; the lesson's `is_parallel` test compares $\|\mathbf{u}\times\mathbf{v}\|^2$ against `tol * tol` instead of testing `== 0.0`, because floating-point round-off rarely lands a near-parallel pair on exactly zero. A zero cross product also flags a degenerate triangle (three collinear vertices) and two parallel segments, so it is a signal to handle a special case, not an error to raise.

</details>

**Q3. Give the plane through three non-collinear points **p**₀, **p**₁, **p**₂, together with its offset.**

<details>
<summary>Answer</summary>

$\mathbf{n} = (\mathbf{p}_1 - \mathbf{p}_0) \times (\mathbf{p}_2 - \mathbf{p}_0)$, then $d = \mathbf{n} \cdot \mathbf{p}_0$.

The plane is the set of all **x** with $\mathbf{n}\cdot\mathbf{x} = d$. The cross product is orthogonal to both edges of the triangle, and therefore to the plane the triangle lies in; dotting with any vertex pins down which plane out of the family of parallel planes through the origin.

The non-collinearity condition matters: collinear points give $\mathbf{n} = \mathbf{0}$, and the "plane" $\mathbf{0}\cdot\mathbf{x} = 0$ is all of ℝ³ or empty, never a surface.

</details>

**Q4. A plane is stored as **n** · **x** = *d* with ‖**n**‖ = 1. How do you find the distance from a point **q** to it, and how do you flip it to the other side?**

<details>
<summary>Answer</summary>

Signed distance: $\delta = \mathbf{n}\cdot\mathbf{q} - d$. Positive means **q** is on the side the normal points to; negative means the other side; the unsigned distance is $\lvert\delta\rvert$.

Reflection: $\mathbf{q}' = \mathbf{q} - 2\delta\,\mathbf{n}$. The factor 2 comes from walking $\mathbf{q}$ to the plane (a displacement of $\delta\mathbf{n}$) and then the same distance past it. In the lesson's Step 8, $\mathbf{q} = (1,1,5)$ and $\delta = 5$ against the floor, giving $(1,1,-5)$.

If ‖**n**‖ ≠ 1 you must divide by it: $\delta = (\mathbf{n}\cdot\mathbf{q} - d)/\|\mathbf{n}\|$.

</details>

**Q5. Write the two unconstrained closest-point parameters for two segments, and say when the formula is invalid.**

<details>
<summary>Answer</summary>

With $\mathbf{d}_1 = \mathbf{p}_2 - \mathbf{p}$, $\mathbf{d}_2 = \mathbf{q}_2 - \mathbf{q}$, $\mathbf{r} = \mathbf{p} - \mathbf{q}$ and $a = \mathbf{d}_1\cdot\mathbf{d}_1$, $b = \mathbf{d}_1\cdot\mathbf{d}_2$, $c = \mathbf{d}_1\cdot\mathbf{r}$, $e = \mathbf{d}_2\cdot\mathbf{d}_2$, $f = \mathbf{d}_2\cdot\mathbf{r}$:

$s = \dfrac{bf-ce}{ae-b^2}, \qquad t = \dfrac{af-bc}{ae-b^2}$.

Invalid when $ae - b^2 = 0$, which by Cauchy–Schwarz happens exactly when the segments are parallel. Then take $s = 0$ and $t = f/e$. Also invalid when $a = 0$ or $e = 0$, i.e. a segment whose endpoints coincide.

And even when the formula is valid, $s$ and $t$ can fall outside $[0,1]$: the solution is for infinite *lines*, so the parameters must then be clamped and re-solved alternately.

</details>

### Long Answer

**Q1. Why does the order of the operands decide which way a normal points, and what actually breaks in a renderer if the winding order of a mesh is wrong? How would you find out?**

<details>
<summary>Model answer</summary>

The cross product is antisymmetric: $\mathbf{v}\times\mathbf{u} = -(\mathbf{u}\times\mathbf{v})$. Look at the first component, $u_2v_3 - u_3v_2$: swapping the inputs swaps the two subtracted terms, which negates the whole expression. The same happens in the other two components, so the entire result is negated. Geometrically the operation encodes an *ordering* — the right-hand rule curls your fingers from the first operand to the second, and reversing the order curls them the other way round the circle. So (**a**, **b**) and (**b**, **a**) are not two ways of computing the same normal; they are two opposite normals, and only one of them can be the outward one.

A renderer turns this into a sign test. With **n** = (**p**₁ − **p**₀) × (**p**₂ − **p**₀), the triangle is front-facing exactly when $\mathbf{n}\cdot(\mathbf{c} - \mathbf{p}_0) > 0$ for camera position **c**. The cross product is perpendicular to the face, so that dot product is positive precisely when the face leans toward the camera.

If the winding order is reversed, every normal in the mesh points inward. Then $\mathbf{n}\cdot(\mathbf{c}-\mathbf{p}_0) > 0$ holds for exactly the faces on the *far* side of the object, and the culler discards the ones you are looking at. The visible symptom is a model that looks inside out: you see its interior walls, lighting is computed against inward normals so shading is inverted, and with back-face culling on, back-face culling is now front-face culling — the near surfaces vanish and you see straight through the model to its far side.

Detecting it is usually easy. Render with culling disabled and compare: a correctly wound model looks solid, an inverted one looks transparent and see-through. The numerical tell is a count like the one in Exercise 6: for a closed convex mesh, a camera outside the object sees about half the faces. Get a number wildly different from half — 10 of 12 where 2 is right — and the winding is inverted. If you already store normals per face, compare each normal against the vector from the face's centre to your reference interior point: `dot(n, inside - p0)` should be negative for every outward normal. It is worth adding that as an assertion, because it is exactly the invariance the lesson's Challenge exercises: `outward_normal` flips the normal when needed, so reversing the vertex order can no longer change the answer.

</details>

**Q2. Why must $s$ and $t$ be clamped and re-solved alternately in the closest-point routine rather than clamped once? Show a case where one pass gives the wrong answer.**

<details>
<summary>Model answer</summary>

On two infinite *lines*, $s$ and $t$ are independent unknowns and each has a unique value; solve once and you are done. Segments add four coupled constraints, $0 \le s \le 1$ and $0 \le t \le 1$, and they are not independent of each other: each is "the parameter of the point on segment 2 nearest the point currently chosen on segment 1". Clamping $s$ to an endpoint *moves* that point, which can move the nearest point on segment 2 outside the segment, so $t$ must be clamped too — and clamping $t$ moves the first point again. You are solving a two-variable problem with a box constraint, and the box constraint bites one coordinate at a time. The fix is to alternate until the pair stops moving: $t \leftarrow (bs+f)/e$ clamped, then $s \leftarrow (bt-c)/a$ clamped, repeatedly.

A concrete case from the lesson's own routine. Take segment 1 from (0, 0, 0) to (0, 0, 1) — one unit along **z** — and segment 2 from (0, 0, 3) to (0, 1, 0).

- Unclamped solution: $s = 3.0$, $t = 0.0$. The two *lines* meet at (0, 0, 3), which is two units beyond the end of segment 1.
- One clamp pass: $s \mapsto 1$, $t = 0$ stays. Closest points (0, 0, 1) and (0, 0, 3), distance **2.0**.
- Converged: $s = 1$, then $t = (bs+f)/e$ gives $t = 0.6$. Closest points (0, 0, 1) and (0, 0.6, 1.2), distance **0.632455532**.

The one-pass answer over-reports the gap by a factor of 3.16. This is exactly Common Mistake 4: the wrong answer is *plausible*, not obviously broken, because a distance of 2.0 between those segments looks entirely reasonable on paper.

Why the two-pass version is right can be checked by hand. With $s = 1$ the first point is pinned at (0, 0, 1). Segment 2 is (0, *t*, 3 − 3*t*), so the squared distance is $t^2 + (2-3t)^2 = 10t^2 - 12t + 4$. Differentiating gives $20t - 12 = 0$, so $t = 0.6$, which is inside $[0,1]$ and therefore a legal point on the segment. Squared distance $0.4$, distance $0.6325$ — matching the iterated routine. And once $t = 0.6$ is plugged back in, $s = (bt-c)/a$ returns $s = 1$ again, so the pair has reached its fixed point and further iteration changes nothing.

Two more details worth knowing. First, in a physics engine this value is the penetration depth, the distance an object is pushed to resolve a contact, so an error here is a visible bug: things float apart or snap through each other. Second, the alternating form is a coordinate-descent method; it converges in a handful of iterations for non-degenerate segments but is not guaranteed to terminate if the segments are nearly parallel, which is why production code usually special-cases the parallel branch explicitly rather than relying on the loop.

</details>

**Q3. Why does the distance-to-a-plane formula need a unit normal, and what happens in collision detection if you forget?**

<details>
<summary>Model answer</summary>

The signed distance is $\delta = (\mathbf{n}\cdot\mathbf{q} - d)/\|\mathbf{n}\|$, and the division by ‖**n**‖ is not optional. A plane is unchanged if you rescale it: $\lambda\mathbf{n}\cdot\mathbf{x} = \lambda d$ defines the same set as $\mathbf{n}\cdot\mathbf{x} = d$ for any nonzero $\lambda$. A quantity that gives the same answer for every valid description of one and the same plane must therefore also be invariant under that rescaling — and $\mathbf{n}\cdot\mathbf{q} - d$ is not. Rescale by $\lambda$ and it multiplies by $\lambda$.

The fix is to divide by the length, because $\mathbf{n}\cdot\mathbf{q} - d$ grows in proportion to ‖**n**‖ while the distance does not. Working through the geometry: let $h$ be the true perpendicular distance and $\hat{\mathbf{n}}$ the unit normal, so $\mathbf{n} = \|\mathbf{n}\|\hat{\mathbf{n}}$ and $d = \|\mathbf{n}\|(\hat{\mathbf{n}}\cdot\mathbf{p}_0)$ for any **p**₀ on the plane. Then $\mathbf{n}\cdot\mathbf{q} - d = \|\mathbf{n}\|(\hat{\mathbf{n}}\cdot(\mathbf{q} - \mathbf{p}_0)) = \|\mathbf{n}\|h$ with the sign carried by $h$. Dividing by ‖**n**‖ recovers $h$ exactly, for every choice of $\mathbf{n}$.

The dimension argument says the same thing more bluntly. $\mathbf{n}$ has the units of area if it came from a cross product of two edges, $d$ has units of length cubed, and $\mathbf{n}\cdot\mathbf{q} - d$ is then a mix of cubic units — it cannot be a length at all until you divide. The lesson's Exercise 2 shows the error concretely: the raw normal (35, −21, −2) has length 40.865633, so the raw $\mathbf{n}\cdot\mathbf{q} - d = -33$ at the origin, while the true signed distance is $-33/40.865633 \approx -0.807524$. Both numbers are finite and both are "signed distances" by the sloppy definition; they differ by a factor of 40.87.

Why this matters in collision detection. That number is the penetration depth — how far a shape is inside a wall, and therefore how far to push it out. Get it wrong and the magnitude of the correction is wrong by a factor of ‖**n**‖, which depends on the size of the triangle or quad the normal was built from. Two failure modes follow. With a large scale factor, shapes are flung out of contact and appear to stick to walls at a distance. With a small one — a normal from a small triangle, or one that has been normalised *twice* — the correction is too small, so a shape sinks further in each frame and eventually tunnels through the wall. Both are non-obvious: nothing raises, nothing returns `nan` unless the normal is exactly zero, and the error scales with the size of the geometry, so it looks correct on a unit cube and fails on a large level.

The practical rule: normalise **n** and *d* together once, at setup, as the lesson's `plane_normalise` does, and store only the unit pair. Never normalise one without the other — dividing **n** by its length while leaving *d* alone silently changes the plane to a different one, and you have lost the original offset with nothing to recover it from.

</details>

**Q4. The scalar triple product is negative for the lesson's **u**, **v**, **w**. What exactly does the sign record, why can you not simply take the absolute value, and where does the sign get used?**

<details>
<summary>Model answer</summary>

The sign records *orientation* — which handedness the ordered triple (**u**, **v**, **w**) has relative to a fixed right-handed frame. For the lesson's values **u** = (1,1,0), **v** = (1,0,1), **w** = (1,1,1), the code prints `scalar triple product = -1.0`, and swapping two inputs prints `+1.0`. Same three vectors, same box, same magnitude — opposite sign. The sign is a property of the *labelling*, not of the geometry.

The mathematics is that the sign is det[**u** **v** **w**], the determinant of the matrix with those vectors as columns. A determinant is positive on an even permutation and negative on an odd one, so a cyclic shift of the three vectors leaves it alone while any pairwise swap negates it. And the sign is not decoration: it is the entire content of $\mathbf{u}\times\mathbf{v} = \mathbf{0} \iff \mathbf{u} \parallel \mathbf{v}$'s companion fact that the cross product *direction* is fixed by the right-hand rule. In ℝ³ the two surfaces $\hat{\mathbf{n}}$ and $-\hat{\mathbf{n}}$ are geometrically identical as normals — a plane has no preferred side — but as a *facing direction* they mean opposite things.

So you cannot take the absolute value and expect to have kept the information. $\lvert(\mathbf{u}\times\mathbf{v})\cdot\mathbf{w}\rvert$ is the volume, and the volume genuinely cannot tell you anything about orientation. Take `abs()` and you have destroyed the one bit the signed version gave you for free. The lesson's own output makes this concrete: `parallelepiped volume = 1.0` and `tetrahedron volume = 0.16666666666666666` are both correct *and* both consistent with a left-handed basis; the sign is only visible in the line above them, `scalar triple product = -1.0`. The paragraph that follows that output says the negative value is not a bug — **u**, **v**, **w** form a left-handed basis and the sign is recording exactly that.

Where the sign is actually used. The clearest case is back-face culling: $\mathbf{n}\cdot(\mathbf{c}-\mathbf{p}_0) > 0$ versus $< 0$ *is* the front/back decision, and if it always came out positive the renderer would cull the wrong half of every model — the exercise showing 10 of 12 triangles front-facing where 2 is correct. A second case is the winding-order convention for a triangle mesh, where the sign of the face normal relative to the surface interior decides whether the face is treated as front- or back-facing; the same ternary test decides whether a ray hits the near or far side of a closed solid. A third is orientation in meshes that carry a consistent outward direction, where a negative scalar product against a known interior point is the test that a face has been wound the wrong way round. A fourth is the determinant of a Jacobian: its sign tells you whether a coordinate map has preserved or flipped handedness, and a sign flip means a mirror image — which is how you detect a degenerate triangle or a flipped texture in a UV mapping, and how you detect that an implicit surface's normal points inward instead of outward.

The rule of thumb: use the magnitude when you want a length, a volume, or an area, and use the sign deliberately whenever you want to know *which way*. Never reach for `abs()` reflexively — ask first whether you are about to discard the orientation.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — ** Given **u** = (1, 2, 3) and **v** = (4, 5, 6), compute the
dot product, the norms, the angle between them in degrees, and **u** × **v**.
Then verify numerically that the cross product is perpendicular to both inputs.

<details>
<summary>Solution</summary>

```python
from math import acos, degrees, sqrt


def sub(u, v):
    return (u[0] - v[0], u[1] - v[1], u[2] - v[2])


def add(u, v):
    return (u[0] + v[0], u[1] + v[1], u[2] + v[2])


def scale(u, s):
    return (u[0] * s, u[1] * s, u[2] * s)


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def norm(u):
    return sqrt(dot(u, u))


def cross(u, v):
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


u = (1.0, 2.0, 3.0)
v = (4.0, 5.0, 6.0)

d = dot(u, v)
print("dot(u, v) =", d)          # 4 + 10 + 18 = 32
print("norm(u) =", round(norm(u), 6))   # sqrt(14)
print("norm(v) =", round(norm(v), 6))   # sqrt(77)

cos_theta = d / (norm(u) * norm(v))
print("cos(theta) =", round(cos_theta, 9))
print("theta in degrees =", round(degrees(acos(cos_theta)), 4))

c = cross(u, v)
print("u x v =", c)
print("dot(u x v, u) =", dot(c, u))
print("dot(u x v, v) =", dot(c, v))
print("norm(u x v) =", round(norm(c), 6))
```

Output:

```
dot(u, v) = 32.0
norm(u) = 3.741657
norm(v) = 8.774964
cos(theta) = 0.974631846
theta in degrees = 12.9332
u x v = (-3.0, 6.0, -3.0)
dot(u x v, u) = 0.0
dot(u x v, v) = 0.0
norm(u x v) = 7.348469
```

Both dot products with the result are exactly `0.0`, confirming orthogonality.
By hand, the cross product is (2·6 − 3·5, 3·4 − 1·6, 1·5 − 2·4) = (−3, 6, −3),
and ‖**u** × **v**‖ = √(9 + 36 + 9) = √54 ≈ 7.3485.

</details>

**[ ] Exercise 2 — ** Three points form a triangle:
P = (1, 0, 1), Q = (4, 5, 1), R = (2, 1, 8). Find the plane through them. Give
the raw normal, the unit normal, the plane's offset d, and the signed distance
of the point S = (0, 0, 0) from that plane. Is S in front of the triangle
(same side as the normal points) or behind it?

<details>
<summary>Solution</summary>

```python
from math import sqrt


def sub(u, v):
    return (u[0] - v[0], u[1] - v[1], u[2] - v[2])


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def cross(u, v):
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


P = (1.0, 0.0, 1.0)
Q = (4.0, 5.0, 1.0)
R = (2.0, 1.0, 8.0)

u = sub(Q, P)  # (3, 5, 0)
v = sub(R, P)  # (1, 1, 7)

n = cross(u, v)
print("u =", u, " v =", v)
print("raw normal =", n)

d = dot(n, P)
print("d = n . P =", d)

length = sqrt(dot(n, n))
print("length of normal =", round(length, 6))

nn = tuple(round(c / length, 9) for c in n)
dd = d / length
print("unit normal =", nn)
print("unit offset =", round(dd, 6))

S = (0.0, 0.0, 0.0)
signed = dot(nn, S) - dd
print("signed distance of S =", round(signed, 6))
print("S is", "in front of" if signed > 0 else "behind", "the triangle")
```

Output:

```
u = (3.0, 5.0, 0.0) v = (1.0, 1.0, 7.0)
raw normal = (35.0, -21.0, -2.0)
d = n . P = 33.0
length of normal = 40.865633
unit normal = (0.856465372, -0.513879223, -0.048940878)
unit offset = 0.807524
signed distance of S = -0.807524
S is behind the triangle
```

The raw normal is (5·7 − 0·1, 0·1 − 3·7, 3·1 − 5·1) = (35, −21, −2). Its length
is √(1225 + 441 + 4) = √1670 ≈ 40.8656. The signed distance is negative, so
the origin lies on the far side of the plane from where the normal points.

</details>

**[ ] Exercise 3 — ** Write a function `is_parallel(u, v, tol)` that returns
`True` when two vectors point in the same direction. Test it on parallel,
anti-parallel, perpendicular, and identical vectors, and confirm that parallel
vectors produce a zero cross product.

<details>
<summary>Solution</summary>

The cross product is zero exactly for parallel vectors, and so is the cross
product's length compared against a tolerance.

```python
def sub(u, v):
    return (u[0] - v[0], u[1] - v[1], u[2] - v[2])


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def cross(u, v):
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


def is_parallel(u, v, tol=1e-12):
    return dot(cross(u, v), cross(u, v)) <= tol * tol


cases = [
    ("identical", (1.0, 2.0, 3.0), (1.0, 2.0, 3.0)),
    ("parallel, different length", (1.0, 2.0, 3.0), (2.0, 4.0, 6.0)),
    ("anti-parallel", (1.0, 0.0, 0.0), (-3.0, 0.0, 0.0)),
    ("perpendicular", (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)),
    ("skew", (1.0, 1.0, 0.0), (0.0, 1.0, 1.0)),
    ("zero vector", (0.0, 0.0, 0.0), (1.0, 2.0, 3.0)),
]

for label, u, v in cases:
    cp = cross(u, v)
    print(f"{label:28s} cross = {cp}  parallel = {is_parallel(u, v)}")
```

Output:

```
identical                    cross = (0.0, 0.0, 0.0)   parallel = True
parallel, different length   cross = (0.0, 0.0, 0.0)   parallel = True
anti-parallel                cross = (0.0, -0.0, 0.0)  parallel = True
perpendicular                cross = (0.0, 0.0, 1.0)   parallel = False
skew                         cross = (1.0, -1.0, 1.0)  parallel = False
zero vector                  cross = (0.0, 0.0, 0.0)   parallel = True
```

The zero vector reports `True`, which is mathematically consistent — the zero
vector is parallel to everything — but if that is not what you want in your
application, test for the zero vector separately with a norm check.

</details>

**[ ] Exercise 4 — ** Extend the segment code to report *both* an unsigned
distance and a boolean `hit` that is `True` when that distance is at most
`radius`. Use it to answer: do segments (0,0,0)–(10,0,0) and (5,−5,0)–(5,5,0)
come within 1 unit of each other, given `radius = 1`? What if the second
segment is moved to z = 3?

<details>
<summary>Solution</summary>

Reuse the clamping routine and wrap the result.

```python
from math import sqrt

EPS = 1e-9


def sub(u, v):
    return (u[0] - v[0], u[1] - v[1], u[2] - v[2])


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def segment_closest(p, p2, q, q2, eps=EPS):
    d1 = sub(p2, p)
    d2 = sub(q2, q)
    r = sub(p, q)
    a, e, f = dot(d1, d1), dot(d2, d2), dot(d2, r)
    if a <= eps or e <= eps:
        raise ValueError("degenerate segment")
    b = dot(d1, d2)
    c = dot(d1, r)
    denom = a * e - b * b
    if abs(denom) < eps:
        s, t = 0.0, f / e
    else:
        s = (b * f - c * e) / denom
        t = (a * f - b * c) / denom
    s = min(1.0, max(0.0, s))
    t = (b * s + f) / e
    t = min(1.0, max(0.0, t))
    s = (b * t - c) / a
    s = min(1.0, max(0.0, s))
    cp = tuple(p[i] + s * d1[i] for i in range(3))
    cq = tuple(q[i] + t * d2[i] for i in range(3))
    dist = sqrt(sum((cp[i] - cq[i]) ** 2 for i in range(3)))
    return cp, cq, dist


def within(p, p2, q, q2, radius):
    cp, cq, dist = segment_closest(p, p2, q, q2)
    return dist, dist <= radius, cp, cq


radius = 1.0
a1, a2 = (0.0, 0.0, 0.0), (10.0, 0.0, 0.0)
b1, b2 = (5.0, -5.0, 0.0), (5.0, 5.0, 0.0)

dist, hit, cp, cq = within(a1, a2, b1, b2, radius)
print("coplanar case:")
print("  distance =", round(dist, 9))
print("  hit within radius =", hit)
print("  closest points =", cp, cq)

c1, c2 = (5.0, -5.0, 3.0), (5.0, 5.0, 3.0)  # the same segment, lifted to z = 3
dist, hit, cp, cq = within(a1, a2, c1, c2, radius)
print("lifted to z=3:")
print("  distance =", round(dist, 9))
print("  hit within radius =", hit)
print("  closest points =", cp, cq)
```

Output:

```
coplanar case:
  distance = 0.0
  hit within radius = True
  closest points = (5.0, 0.0, 0.0) (5.0, 0.0, 0.0)
lifted to z=3:
  distance = 3.0
  hit within radius = False
  closest points = (5.0, 0.0, 0.0) (5.0, 0.0, 3.0)
```

In the first case the segments cross at (5, 0, 0), so the distance is exactly
zero and the answer is obviously `True`. Lifting one segment by 3 units raises
the gap to 3, which exceeds the radius, so the answer flips to `False` without
any change to the algorithm. That is the whole collision test: compute a
distance, compare against a threshold.

</details>

**Challenge — ** A triangle mesh stores face normals precomputed as
`cross(p1 - p0, p2 - p0)`. Write a function `outward_normal(p0, p1, p2, inside_point)`
that returns the normal guaranteed to point away from a reference point (such as
the centre of a bounding box). Show that it returns the negated normal when the
winding order of the vertices is reversed.

<details>
<summary>Solution</summary>

```python
def sub(u, v):
    return (u[0] - v[0], u[1] - v[1], u[2] - v[2])


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def cross(u, v):
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


def outward_normal(p0, p1, p2, inside_point):
    """Return the face normal oriented away from inside_point."""
    n = cross(sub(p1, p0), sub(p2, p0))
    # n . (inside - p0) is negative exactly when inside is on the side the
    # normal points away from, so flip when it is not negative.
    if dot(n, sub(inside_point, p0)) > 0:
        n = tuple(-c for c in n)
    return n


# A face on the +x side of a unit cube centred at the origin.
p0 = (1.0, -1.0, -1.0)
p1 = (1.0, 1.0, -1.0)
p2 = (1.0, 1.0, 1.0)
centre = (0.0, 0.0, 0.0)

n1 = outward_normal(p0, p1, p2, centre)
print("winding p0,p1,p2 ->", n1)

n2 = outward_normal(p0, p2, p1, centre)  # reversed winding
print("winding p0,p2,p1 ->", n2)

print("identical? ", n1 == n2)
print("both point along +x:", n1[0] > 0 and n2[0] > 0)
```

Output:

```
winding p0,p1,p2 -> (4.0, 0.0, 0.0)
winding p0,p2,p1 -> (4.0, -0.0, -0.0)
identical?  True
both point along +x: True
```

Reversing the winding does produce the negated raw cross product, so the raw
normals are (4, 0, 0) and (−4, 0, 0). The orientation test then flips the
second one back, so the function returns the same outward normal either way.
The `-0.0` in the second line is the negation surviving as a signed zero, which
compares equal to `0.0` — that is why `identical?` prints `True`. This is the
invariance we want: the mesh author cannot accidentally invert a face by getting
the vertex order wrong.

</details>

**[ ] Exercise 5 — ** Verify the identity the numpy section asserted, that
`det([u v w])` equals `(u x v) . w` when the columns of the matrix are the
three vectors. Use the lesson's `u = (1, 1, 0)`, `v = (1, 0, 1)`,
`w = (1, 1, 1)`, which the code above reports as a triple product of −1.0, and
confirm with a second, less symmetric triple. Show what happens to both
quantities when two vectors are swapped.

<details>
<summary>Solution</summary>

The 3×3 determinant by cofactor expansion along the first row, where
`cols = [u, v, w]` and each is a *column*.

```python
def sub(u, v):
    return (u[0] - v[0], u[1] - v[1], u[2] - v[2])


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def cross(u, v):
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


def det3(cols):
    """3x3 determinant by cofactor expansion. cols is [u, v, w] as COLUMNS."""
    # m[i][j] = component i of column j, i.e. the usual matrix layout.
    m = [[cols[j][i] for j in range(3)] for i in range(3)]
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


u = (1.0, 1.0, 0.0)
v = (1.0, 0.0, 1.0)
w = (1.0, 1.0, 1.0)
print("u =", u, " v =", v, " w =", w)
print("det3([u v w])      =", det3([u, v, w]))
print("(u x v) . w        =", dot(cross(u, v), w))
print("det3([v u w])      =", det3([v, u, w]))
print("equal?", det3([u, v, w]) == dot(cross(u, v), w))

# A second triple with no special symmetry, to be sure it is not a coincidence.
a = (2.0, -1.0, 3.0)
b = (0.0, 4.0, -2.0)
c = (-1.0, 0.5, 2.0)
print()
print("det3([a b c])      =", det3([a, b, c]))
print("(a x b) . c        =", dot(cross(a, b), c))
print("parallelepiped vol =", abs(dot(cross(a, b), c)))
print("tetrahedron vol    =", abs(dot(cross(a, b), c)) / 6.0)
```

Output:

```
u = (1.0, 1.0, 0.0)  v = (1.0, 0.0, 1.0)  w = (1.0, 1.0, 1.0)
det3([u v w])      = -1.0
(u x v) . w        = -1.0
det3([v u w])      = 1.0
equal? True

det3([a b c])      = 28.0
(a x b) . c        = 28.0
parallelepiped vol = 28.0
tetrahedron vol    = 4.666666666666667
```

The identity holds to the last bit, and it holds for the asymmetric triple too.
Swapping **u** and **v** flips *both* quantities: `det3([v u w])` is 1.0 where
the triple product was −1.0. That is the antisymmetry of the cross product
showing up in matrix language — swapping two columns is one transposition, and a
determinant changes sign under an odd permutation.

Two hand checks. For the second triple, **a** × **b** = ((−1)(−2) − (3)(4),
(3)(0) − (2)(−2), (2)(4) − (−1)(0)) = (−10, 4, 8), and (−10, 4, 8) · (−1, 0.5, 2)
= 10 + 2 + 16 = 28. For the first, **u** × **v** = (1·1 − 0·0, 0·1 − 1·1, 1·0 − 1·1)
= (1, −1, −1) and (1, −1, −1) · (1, 1, 1) = 1 − 1 − 1 = −1, matching the output
of the lesson's own `scalar_triple` call.

Why this is worth knowing: it means a matrix library can compute collision
volume without anyone writing a cross product. Build a 3×3 with your three edge
vectors as columns and call `numpy.linalg.det` — which is exactly what the
numpy block's `det(U) = 2.0` line was doing.

</details>

**[ ] Exercise 6 — ** A renderer culls back faces with the test
`dot(cross(p1 - p0, p2 - p0), camera - p0) > 0`. Build a closed cube as six
quads (twelve triangles), fix each quad's winding so its normal points out of
the cube, and then count the front-facing triangles for a camera far along
**x**, far along **y**, at a distant corner, and at the centre of the cube.
Finally, reverse every winding and repeat. Explain each number.

<details>
<summary>Solution</summary>

The winding is fixed once, using the same inside/outside test as the earlier
Challenge, so the mesh starts out correct and the second half of the exercise
measures the damage from flipping it.

```python
def sub(u, v):
    return (u[0] - v[0], u[1] - v[1], u[2] - v[2])


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def cross(u, v):
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


def facing(p0, p1, p2, camera):
    """True when the triangle's right-hand normal points at the camera."""
    n = cross(sub(p1, p0), sub(p2, p0))
    return dot(n, sub(camera, p0)) > 0.0


# A unit cube centred at the origin: 6 faces, each given as 4 corners.
# The winding below is deliberately not trusted -- it is fixed afterwards.
RAW = [
    [(1, -1, -1), (1, 1, -1), (1, 1, 1), (1, -1, 1)],
    [(-1, -1, -1), (-1, 1, -1), (-1, 1, 1), (-1, -1, 1)],
    [(-1, -1, -1), (1, -1, -1), (1, -1, 1), (-1, -1, 1)],
    [(-1, 1, -1), (1, 1, -1), (1, 1, 1), (-1, 1, 1)],
    [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)],
    [(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1)],
]
CENTRE = (0.0, 0.0, 0.0)
faces = []
for quad in RAW:
    q = [tuple(float(c) for c in p) for p in quad]
    # Orient outward: the raw normal must point AWAY from the centre, so
    # n . (centre - p0) must be negative. If it is positive, reverse.
    if dot(cross(sub(q[1], q[0]), sub(q[2], q[0])), sub(CENTRE, q[0])) > 0:
        q = list(reversed(q))
    faces.append(q)


def count_visible(faces, camera):
    """Count front-facing triangles; each quad is split into two triangles."""
    seen = 0
    for quad in faces:
        for tri in ((0, 1, 2), (0, 2, 3)):
            if facing(quad[tri[0]], quad[tri[1]], quad[tri[2]], camera):
                seen += 1
    return seen


cams = [(10.0, 0.0, 0.0), (0.0, 10.0, 0.0), (0.0, 0.0, 10.0),
        (10.0, 10.0, 10.0), CENTRE]
for cam in cams:
    print(f"camera {str(cam):22s} {count_visible(faces, cam):2d} of 12 front-facing")

rev = [list(reversed(f)) for f in faces]
print()
for cam in cams[:4]:
    print(f"camera {str(cam):22s} {count_visible(rev, cam):2d} of 12 front-facing (reversed)")
```

Output:

```
camera (10.0, 0.0, 0.0)        2 of 12 front-facing
camera (0.0, 10.0, 0.0)        2 of 12 front-facing
camera (0.0, 0.0, 10.0)        2 of 12 front-facing
camera (10.0, 10.0, 10.0)      6 of 12 front-facing
camera (0.0, 0.0, 0.0)         0 of 12 front-facing

camera (10.0, 0.0, 0.0)       10 of 12 front-facing (reversed)
camera (0.0, 10.0, 0.0)       10 of 12 front-facing (reversed)
camera (0.0, 0.0, 10.0)       10 of 12 front-facing (reversed)
camera (10.0, 10.0, 10.0)      6 of 12 front-facing (reversed)
```

Every number has a geometric reading.

- **Camera far along one axis: 2 of 12.** From (10, 0, 0) you see exactly one
  face of the cube, the +**x** face, and each quad is two triangles. The other
  ten triangles are back-facing and get culled. The same count appears for
  **y** and **z**, which is the first sign the winding was fixed correctly: the
  three counts must agree, and they do.
- **Camera at a distant corner: 6 of 12.** From (10, 10, 10) three faces are
  turned toward the viewer — +**x**, +**y**, +**z** — so three quads, six
  triangles.
- **Camera at the centre: 0 of 12.** Every normal points *out* of the cube, and
  the centre is on the inside of every face, so no normal leans toward it. Zero
  is the correct answer and a useful assertion: a camera inside a closed mesh
  should see nothing through the front-face test.

Now the damage. Reversing every winding turns 2 into 10 along an axis: the
culler now keeps the five *far* faces and throws away the one face you were
looking straight at. The corner case is the deceptive one — 6 of 12 before, 6 of
12 after — so a naive "count the visible triangles" sanity check passes at that
camera position while the model renders inside out everywhere else. That is
exactly why the fix belongs in the assertion from the earlier Challenge: check
each face's normal against a known interior point at load time, not against the
camera.

</details>

**Challenge 2 — ** Write `closest_point_on_triangle(p, a, b, c)` returning the
nearest point on a triangle (including its interior) to **p**, the distance, and
a flag saying whether the nearest point lies in the interior of the face rather
than on one of its three edges. Use it to explain why a point sitting directly
above a triangle's *vertex* is reported as "interior", and what a physics engine
must do differently when it wants an edge or vertex contact instead.

<details>
<summary>Solution</summary>

The routine is: project **p** onto the plane of the triangle, test whether the
projection is inside by barycentric coordinates, and if it is not, fall back to
the closest point on each of the three edges.

```python
from math import sqrt


def sub(u, v):
    return (u[0] - v[0], u[1] - v[1], u[2] - v[2])


def add(u, v):
    return (u[0] + v[0], u[1] + v[1], u[2] + v[2])


def scale(u, s):
    return (u[0] * s, u[1] * s, u[2] * s)


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def cross(u, v):
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


def norm(u):
    return sqrt(dot(u, u))


def point_segment(p, a, b):
    """Nearest point on segment a-b, with its parameter clamped to [0, 1]."""
    ab = sub(b, a)
    denom = dot(ab, ab)
    if denom == 0.0:
        return a, norm(sub(p, a))
    s = max(0.0, min(1.0, dot(sub(p, a), ab) / denom))
    c = add(a, scale(ab, s))
    return c, norm(sub(p, c))


def closest_point_on_triangle(p, a, b, c):
    """(nearest point, distance, is_it_in_the_face_interior)."""
    n = cross(sub(b, a), sub(c, a))
    nn = dot(n, n)
    if nn == 0.0:
        raise ValueError("degenerate triangle: the three vertices are collinear")

    # 1. Orthogonal projection of p onto the plane, walking along n.
    h = dot(sub(p, a), n) / nn
    proj = sub(p, scale(n, h))

    # 2. Barycentric coordinates of the projection relative to (a, b, c).
    v0 = sub(b, a)
    v1 = sub(c, a)
    v2 = sub(proj, a)
    d00, d01, d11 = dot(v0, v0), dot(v0, v1), dot(v1, v1)
    d20, d21 = dot(v2, v0), dot(v2, v1)
    denom = d00 * d11 - d01 * d01
    s = (d11 * d20 - d01 * d21) / denom
    t = (d00 * d21 - d01 * d20) / denom
    inside = s >= 0.0 and t >= 0.0 and (s + t) <= 1.0

    if inside:
        return proj, norm(sub(p, proj)), True

    # 3. Outside the face: the nearest point is on one of the three edges.
    best = None
    for e0, e1 in ((a, b), (b, c), (c, a)):
        cp, d = point_segment(p, e0, e1)
        if best is None or d < best[1]:
            best = (cp, d)
    return best[0], best[1], False


A = (0.0, 0.0, 0.0)
B = (4.0, 0.0, 0.0)
C = (0.0, 3.0, 0.0)
print("triangle A", A, "B", B, "C", C)
for label, p in [
    ("above the interior", (1.0, 1.0, 5.0)),
    ("above vertex A", (0.0, 0.0, 5.0)),
    ("far off to the side", (10.0, 1.0, 0.0)),
    ("past edge BC", (3.0, 3.0, 0.0)),
    ("in the plane, inside", (1.0, 1.0, 0.0)),
]:
    cp, d, inside = closest_point_on_triangle(p, A, B, C)
    shown = tuple(round(x, 6) for x in cp)
    print(f"{label:22s} closest={str(shown):26s} dist={round(d, 6)} interior={inside}")
```

Output:

```
triangle A (0.0, 0.0, 0.0) B (4.0, 0.0, 0.0) C (0.0, 3.0, 0.0)
above the interior     closest=(1.0, 1.0, 0.0)            dist=5.0 interior=True
above vertex A         closest=(0.0, 0.0, 0.0)            dist=5.0 interior=True
far off to the side    closest=(4.0, 0.0, 0.0)            dist=6.082763 interior=False
past edge BC           closest=(1.92, 1.56, 0.0)          dist=1.8 interior=False
in the plane, inside   closest=(1.0, 1.0, 0.0)            dist=0.0 interior=True
```

Reading the rows.

- *Above the interior*: the projection is (1, 1, 0), which is inside, so the
  answer is the perpendicular foot and the distance is 5 — the point is exactly
  5 above the plane.
- *Above vertex A*: the projection is (0, 0, 0), the vertex itself, and the
  barycentric coordinates come out as $s = 0$, $t = 0$. The test
  `s >= 0 and t >= 0 and s + t <= 1` uses `>=`, so boundary points count as
  interior, and the routine reports `interior=True` with distance 5.
- *Far off to the side*: the projection is outside, so all three edges are tried
  and the winner is the whole edge AB, nearest point (4, 0, 0) — the **nearer
  endpoint** of AB, which is why the flag is `False`. Distance
  $\sqrt{6^2 + 1^2} = \sqrt{37} \approx 6.0828$.
- *Past edge BC*: the projection of (3, 3, 0) is (3, 3, 0) itself (it is already
  in the plane) and lies beyond BC, so the nearest point is interior to edge BC.
  BC runs from (4, 0, 0) with direction (−4, 3, 0), and the parameter is
  $s = \frac{(p-B)\cdot d}{\lVert d\rVert^2} = \frac{(-1)(-4) + (3)(3)}{16+9} = \frac{13}{25} = 0.52$,
  giving the point $(4 - 0.52\cdot 4,\; 0.52\cdot 3,\; 0) = (1.92, 1.56, 0)$.
  The distance is $\sqrt{1.08^2 + 1.44^2} = \sqrt{3.24} = 1.8$, matching the
  printed value.
- *In the plane, inside*: distance 0, as it must be.

Why a physics engine cares about the flag. The barycentric test treats the
boundary as interior, which is the right call for a collision *query* — you want
the smallest distance and the point of contact, and (0,0,0) genuinely is the
nearest point of the triangle to (0, 0, 5). But a contact needs more than a
position: it needs a *classification*, because the contact normal differs
between the three regions. Over the interior, the normal is **n** = (**b** − **a**)
× (**c** − **a**), and that is the number to push against. Over an edge, the
object is sliding off a corner, so the normal is the component of **n**
perpendicular to that edge, and only that component is a real contact — the
other axis is a separate feature of the mesh and needs its own contact. At a
vertex, the object has hit a corner and the true constraint set is an intersection
of half-spaces, so the engine typically solves it with a cone constraint or
falls back to a bounding volume around the vertex.

This is why the flag, not just the distance, is the return value worth having.
An engine that reads only `closest` and pushes along **n** at every contact will
push sideways incorrectly for edge and vertex contacts, and the object will
slide along the wrong face. A cheap extra line — recomputing $s$ and $t$ and
testing $s > 0$, $t > 0$, $s + t < 1$ separately — separates the three cases and
turns a subtly wrong solver into three correct ones.

</details>

## Summary

- A 3D vector is three numbers; addition is componentwise and the norm is the
  square root of the sum of squares.
- The dot product measures agreement between directions and encodes the angle
  via `cos θ = (u · v) / (‖u‖ ‖v‖)`.
- The cross product returns the unique vector perpendicular to both inputs,
  oriented by the right-hand rule, with magnitude equal to the parallelogram
  area.
- The cross product is zero exactly when the inputs are parallel, which makes it
  a cheap parallelism test.
- The scalar triple product `(u × v) · w` is the signed volume of a box; divide
  by 6 for a tetrahedron, and `det([u v w])` computes the same thing.
- Three non-collinear points fix a plane; its normal is the cross product of two
  in-plane edges and its offset is `n · p₀`.
- Distance to a plane needs a unit normal: `n̂ · q − d̂`, and reflection across
  it is `q − 2(n̂ · q − d̂)n̂`.
- Segment distance needs the two parameters clamped into `[0, 1]` and
  re-solved alternately; the result is what a collision test compares to a
  radius.

## Next

[91 — Transformations for Computer Graphics](91_transformations_graphics.md)
takes the cross product and turns it into a matrix: 4×4 homogeneous transforms,
the order of composition, and a complete transform–project–clip pipeline built
from scratch.
