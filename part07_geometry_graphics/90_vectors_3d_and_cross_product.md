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
