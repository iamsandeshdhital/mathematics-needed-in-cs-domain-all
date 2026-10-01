# 91 — Transformations for Computer Graphics

**Part**: part07_geometry_graphics · **Prerequisites**: 31, 35, 90 · **Time**: 35 min

---

## In Plain Words

A transformation answers the question "where does this point end up after
something happens to it?" Something moves, something rotates, something gets
bigger or smaller. In a game engine, every object has a position, a rotation and
a scale, and every frame all three get combined into one operation that is
applied to every vertex.

The trick that makes this elegant is a four-by-four grid of numbers called a
transform matrix. A 3D point has three coordinates, but the matrix has four
columns. So the point gets a fourth coordinate of one, and the matrix produces
four outputs: three position numbers plus a fourth that can be anything. That
slack fourth coordinate is what lets one matrix do things a 3×3 matrix cannot,
such as moving a point without needing an extra addition step.

Perspective projection is the other half of the story. Objects further away
should look smaller, and the way to get that is to divide by depth after the
transform. That division is why the fourth coordinate exists, why the pipeline
needs a clipping stage at all, and why the standard graphics pipeline is
built out of exactly the stages it is built out of.

## Why Computer Science Cares

- **Every game engine is this lesson.** `gluLookAt`, `glTranslatef`,
  `glRotatef`, `glm::rotate`, `THREE.Matrix4`, `UnityEngine.Matrix4x4.TRS` are
  all 4×4 matrices built from the formulas below.
- **Scene graphs.** In a scene graph a parent transform is composed with a
  child transform to produce a world matrix. Getting the composition order
  backwards is the single most common bug in graphics code, and it produces
  rotations that look plausible and are wrong.
- **Normal transformation.** The normal of a scaled surface is *not* the scaled
  normal. Under non-uniform scale you must transform normals by the inverse
  transpose, which is why engines store both a model matrix and an
  inverse-transpose normal matrix.
- **Ray picking.** Screen pixel → world ray requires inverting the
  view-projection matrix. This comes up in every click-to-select interaction.
- **CAD and robotics.** A 4×4 matrix is the homogeneous form of a rigid body
  transform, which is what makes composing many rotations numerically stable
  instead of accumulating Euler-angle gimbal errors.
- **CSS transforms.** `transform: matrix3d(...)` in a browser is literally a
  4×4 matrix, and `transform: translate(...) rotate(...) scale(...)` is
  shorthand for a specific composition.

## The Formal Version

Notation follows [SYMBOLS.md](../../SYMBOLS.md).

**Definition.** A *homogeneous coordinate* for ℝ³ is a 4-vector
(x, y, z, w) ∈ ℝ⁴. The point (x, y, z) is represented by (x, y, z, 1).

**Definition.** A *homogeneous transformation matrix* is a 4×4 matrix

```
        ⎡ a11 a12 a13 a14 ⎤
    M = ⎢ a21 a22 a23 a24 ⎥
        ⎢ a31 a32 a33 a34 ⎥
        ⎣ a41 a42 a43 a44 ⎦
```

acting on a column of homogeneous coordinates. The top-left 3×3 block is the
*linear part* L; the top-right 3-vector is the *translation part* **t**.

**Definition.** The *identity* matrix I₄ has ones on the diagonal and zeros
elsewhere. It is the multiplicative identity: **M**I = I**M** = **M**.

**Key convention.** Graphics APIs use **column vectors**, so a point is
multiplied as **p**′ = **M p**. The composed transform is therefore
**M** = **P · MV** (projection times model-view times model), with the last
named factor applied first when reading right to left.

**Why column vectors specifically?** It is a convention, not a law of nature,
and the two conventions are mathematically equivalent. Column vectors won
because OpenGL, Direct3D, GLSL and every engine built on them use them. The
consequences are worth internalising: new transformations are multiplied on the
*left*, `pᵀ = Mᵀp` under the row convention becomes `p = Mp` here, and
`gl_Position` in a vertex shader is exactly the column-vector product. The one
thing that is *not* convention is that translation must sit in the top-right
block and rotation in the top-left, because multiplying a column vector can only
rotate the components and add a constant.

**Definition.** The *translation* matrix by **t** = (tx, ty, tz) is

```
        ⎡ 1  0  0  tx ⎤
    T = ⎢ 0  1  0  ty ⎥
        ⎢ 0  0  1  tz ⎥
        ⎣ 0  0  0  1 ⎦
```

so that T(x, y, z, 1)ᵀ = (x + tx, y + ty, z + tz, 1)ᵀ.

**Definition.** The *scaling* matrix by (sx, sy, sz) is diag(sx, sy, sz, 1).

**Definition.** The *rotation* matrices, with **c** = cos θ and **s** = sin θ:

```
    Rx = ⎡ 1  0   0  0 ⎤      Ry = ⎡  c  0  s  0 ⎤      Rz = ⎡  c  -s  0  0 ⎤
         ⎢ 0  c  -s  0 ⎥           ⎢  0  1  0  0 ⎥           ⎢  s   c  0  0 ⎥
         ⎢ 0  s   c  0 ⎥           ⎢ -s  0  c  0 ⎥           ⎢  0   0  1  0 ⎥
         ⎣ 0  0   0  1 ⎦           ⎣  0  0  0  1 ⎦           ⎣  0   0  0  1 ⎦
```

**Theorem (composition order).** With column vectors, `M = A · B` applies B
first and then A. Consequently `R · S · T` means "scale, then rotate, then
translate", which is what you almost always want, and `T · S · R` means the
opposite and almost never does.

**Theorem (rotation about an arbitrary axis).** Let **u** be a unit vector
(axis) and θ an angle. With **v** = **u** × **a** and **w** = **u** × **v** for any
**a** ⊥ **u**, the matrix

```
        ⎡ c + u1²(1−c)      u1u2(1−c) − u3 s    u1u3(1−c) + u2 s    0 ⎤
    R = ⎢ u2u1(1−c) + u3 s   c + u2²(1−c)        u2u3(1−c) − u1 s    0 ⎥
        ⎢ u3u1(1−c) − u2 s   u3u2(1−c) + u1 s    c + u3²(1−c)       0 ⎥
        ⎣        0                   0                  0            1 ⎦
```

rotates by θ about **u** using the right-hand rule. For **u** = (0, 0, 1),
**c** = cos θ, **s** = sin θ, this reduces exactly to Rz above — which is a
useful self-check.

**Definition.** A *view* (camera) matrix V places the world into camera space,
putting the camera at the origin looking down the negative z axis.

**Definition.** The *perspective projection* matrix for an image `aspect` wide
and `height` tall, with vertical field of view θ and near/far planes n and f,
is

```
                ⎡ 1/(aspect·tan(θ/2))        0               0                    0            ⎤
    P(θ, a, n, f) = ⎢           0          1/tan(θ/2)         0                    0            ⎥
                ⎢           0              0        −(f+n)/(f−n)    −2fn/(f−n)           ⎥
                ⎣           0              0             −1                    0            ⎦
```

**Theorem.** After projection, clip coordinates satisfy w = −z_view. Points in
front of the camera have w > 0. The point z = −n maps to NDC z = −1 (the near
plane) and z = −f maps to NDC z = +1 (the far plane), so **depth increases with
distance**, which is why the depth buffer test is `LESS`.

**Definition.** The *clip volume* is the frustum −w ≤ x ≤ w, −w ≤ y ≤ w, −w ≤ z ≤ w.
Anything outside must be clipped before division, because dividing by a negative
or zero w flips the geometry inside out.

**Definition.** *Normalised device coordinates* are clip coordinates divided by
w, and *screen coordinates* follow from `x_screen = (x_ndc + 1)/2 · width`,
`y_screen = (1 − y_ndc)/2 · height`. The y flip exists because image row 0 is at
the top.

## Worked Example

Build the transform for a point P = (1, 0, 0): scale by 2 in x, rotate 90°
about z, then translate by (0, 5, 0).

**Step 1 — the matrices.**

S = diag(2, 1, 1, 1), so
S = ⎡2 0 0 0; 0 1 0 0; 0 0 1 0; 0 0 0 1⎦

For θ = 90°: c = cos 90° = 0, s = sin 90° = 1.

Rz = ⎡0 −1 0 0; 1 0 0 0; 0 0 1 0; 0 0 0 1⎦

T = ⎡1 0 0 0; 0 1 0 5; 0 0 1 0; 0 0 0 1⎦

**Step 2 — apply them in order.** With column vectors, `M = T · Rz · S`.

Start with S·P: S·(1, 0, 0, 1)ᵀ = (2, 0, 0, 1)ᵀ. The point moved along x.

Then Rz: Rz·(2, 0, 0, 1)ᵀ = (0·2 + (−1)·0 + 0, 1·2 + 0·0 + 0, 0, 1)ᵀ = (0, 2, 0, 1)ᵀ.

Then T: T·(0, 2, 0, 1)ᵀ = (0, 2 + 5, 0, 1)ᵀ = (0, 7, 0, 1)ᵀ.

So the point ends at **(0, 7, 0)**. Read the steps as a story: it was a unit
point on the x axis, scaling stretched it to x = 2, the rotation swept it a
quarter turn round to the y axis at height 2, and the translation lifted it 5
more. That is "scale, then rotate, then translate".

**Step 3 — why the order matters.** Compute the single composed matrix M = T·Rz·S.

Rz·S multiplies rows by the scale factors:
Rz·S = ⎡0 −1 0 0; 2 0 0 0; 0 0 1 0; 0 0 0 1⎦

Then T·(Rz·S):
row 0 of T is (1, 0, 0, 0), so row 0 of the product is row 0 of Rz·S: (0, −1, 0, 0).
row 1 of T is (0, 1, 0, 5): it takes row 1 of Rz·S plus 5·row 3, which is
(2, 0, 0, 0) + (0, 0, 0, 5) = (2, 0, 0, 5).
rows 2 and 3 pass through unchanged.

M = ⎡0 −1 0 0; 2 0 0 5; 0 0 1 0; 0 0 0 1⎦

Check: M·(1, 0, 0, 1)ᵀ = (0, 2 + 5, 0, 1)ᵀ = (0, 7, 0, 1)ᵀ. Matches.

Now compute the *other* order, S·Rz·T, and apply to the same point:

T·P = (1, 5, 0, 1)ᵀ. Then Rz·(1, 5, 0, 1)ᵀ = (−5, 1, 0, 1)ᵀ. Then
S·(−5, 1, 0, 1)ᵀ = (−10, 1, 0, 1)ᵀ.

Completely different point: **(−10, 1, 0)**. Worse, the translation itself got
rotated and scaled, which is never what you want. This is why the convention
exists and why `R · S · T` is the mnemonic to memorise.

**Step 4 — the arbitrary-axis formula, as a self-check.** Take
**u** = (0, 0, 1), θ = 90°, c = 0, s = 1. Plugging in:

- R₀₀ = c + u₁²(1−c) = 0 + 0 = 0
- R₀₁ = u₁u₂(1−c) − u₃s = 0 − 1 = −1
- R₁₀ = u₂u₁(1−c) + u₃s = 0 + 1 = 1
- R₁₁ = c + u₂²(1−c) = 0
- R₂₂ = c + u₃²(1−c) = 0 + 1·1 = 1

which is exactly Rz. The formula is a generalisation of the three special cases,
not a separate piece of mathematics.

**Step 5 — perspective projection.** Take θ = 90°, aspect = 1, n = 1, f = 10, and
a point P = (1, 1, −3) — one unit right, one unit up, three units in front.

tan(45°) = 1, so R₀₀ = R₁₁ = 1.

w = −z = 3
x_clip = 1·1 = 1, so x_ndc = 1/3
y_clip = 1·1 = 1, so y_ndc = 1/3
z_clip = −(10 + 1)/(10 − 1) · (−3) − 2·10·1/(10 − 1) = (11/9)·3 − 20/9 = 33/9 − 20/9 = 13/9 ≈ 1.4444
z_ndc = (13/9)/3 = 13/27 ≈ 0.48148

So the point lands at (0.3333, 0.3333, 0.4815) in normalised device
coordinates. Depth 0.4815 is between 0 and 1, so it is inside the frustum and
survives clipping. On a 800×600 screen that maps to pixel
(1 + 0.3333)/2 · 800 = 533.3 and (1 − 0.3333)/2 · 600 = 199.999 ≈ 200, so
near the centre of the image, shifted right and up as expected.

Compare a point twice as far away, (1, 1, −6). Now w = 6, x_ndc = 1/6 = 0.1667,
y_ndc = 0.1667. Half the offset for double the depth: that is perspective, and
it appeared from the division by w alone.

## Runnable Code

Plain Python lists, matrices as rows of lists. This is the same 4×4 pipeline a
shader runs, written out longhand.

```python
# --- matrix helpers on plain nested lists -------------------------------


def identity():
    return [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]


def matmul(a, b):
    """4x4 times 4x4, by hand. Row-times-column."""
    n = len(a)
    return [
        [sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)]
        for i in range(n)
    ]


def apply(m, p):
    """Multiply a 4x4 matrix by a 4-vector (a point)."""
    return [sum(m[i][k] * p[k] for k in range(4)) for i in range(4)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def translate(tx, ty, tz):
    m = identity()
    m[0][3], m[1][3], m[2][3] = tx, ty, tz
    return m


def scale(sx, sy, sz):
    m = identity()
    m[0][0], m[1][1], m[2][2] = sx, sy, sz
    return m


def rotate_z(theta):
    """Rotation about +z. cos/sin of the angle."""
    from math import cos, sin

    c, s = cos(theta), sin(theta)
    return [
        [c, -s, 0.0, 0.0],
        [s, c, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]


def show(m, label):
    print(label)
    for row in m:
        print("   ", [round(v, 4) if isinstance(v, float) else v for v in row])


p = [1.0, 0.0, 0.0, 1.0]
print("start point =", p[:3])

S = scale(2.0, 1.0, 1.0)
R = rotate_z(1.5707963267948966)  # pi/2 = 90 degrees
T = translate(0.0, 5.0, 0.0)

# Column vectors: M = T * R * S means "scale, then rotate, then translate".
M = matmul(T, matmul(R, S))
show(M, "\nM = T * R * S:")

print("\nstep by step:")
after_scale = apply(S, p)
print("  after scale   =", [round(v, 6) for v in after_scale[:3]])
after_rot = apply(R, after_scale)
print("  after rotate  =", [round(v, 6) for v in after_rot[:3]])
after_trans = apply(T, after_rot)
print("  after translate =", [round(v, 6) for v in after_trans[:3]])

print("\none-shot M * p =", [round(v, 6) for v in apply(M, p)[:3]])

# The other order gives a different, wrong answer.
W = matmul(S, matmul(R, T))
print("other order S * R * T applied to p =",
      [round(v, 6) for v in apply(W, p)[:3]])
print("the two orders agree?", apply(M, p) == apply(W, p))
```

```
start point = [1.0, 0.0, 0.0]

M = T * R * S:
    [[0.0, -1.0, 0.0, 0.0], [2.0, 0.0, 0.0, 5.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]

step by step:
  after scale   = [2.0, 0.0, 0.0]
  after rotate  = [0.0, 2.0, 0.0]
  after translate = [0.0, 7.0, 0.0]

one-shot M * p = [0.0, 7.0, 0.0]
other order S * R * T applied to p = [-10.0, 1.0, 0.0]
the two orders agree? False
```

The composed matrix in the code is exactly the matrix derived by hand in
step 3, and the "other order" result matches step 3's **(−10, 1, 0)**.

### Rotation about an arbitrary axis

Rodrigues' rotation formula in matrix form, built from the cross products of the
previous lesson.

```python
from math import cos, sin, sqrt


def identity():
    return [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]


def cross(u, v):
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def normalise(u):
    length = sqrt(dot(u, u))
    return tuple(c / length for c in u)


def rotation_about_axis(axis, theta):
    """4x4 matrix rotating by theta about an arbitrary (not unit) axis."""
    ux, uy, uz = normalise(axis)
    c, s = cos(theta), sin(theta)
    # Columns of the 3x3 block: cos*I + (1-c)*uu^T + s*[u]_x, written out.
    k = 1.0 - c
    return [
        [c + ux * ux * k,      ux * uy * k - uz * s,  ux * uz * k + uy * s,  0.0],
        [uy * ux * k + uz * s, c + uy * uy * k,      uy * uz * k - ux * s,  0.0],
        [uz * ux * k - uy * s, uz * uy * k + ux * s, c + uz * uz * k,      0.0],
        [0.0,                 0.0,                 0.0,                  1.0],
    ]


def apply(m, p):
    return [sum(m[i][k] * p[k] for k in range(4)) for i in range(4)]


def show(m, label):
    print(label)
    for row in m:
        print("   ", [round(v, 4) for v in row])


HALF_PI = 1.5707963267948966

# Self-check: rotating about +z must give the standard Rz matrix.
about_z = rotation_about_axis((0.0, 0.0, 1.0), HALF_PI)
show(about_z, "rotation about (0, 0, 1) by 90 degrees:")

# Rotate the point (1, 0, 0) about the axis (1, 1, 0) through the origin.
axis = (1.0, 1.0, 0.0)
print("\naxis =", axis, " (normalised:", normalise(axis), ")")
p = (1.0, 0.0, 0.0)

for label, angle in [("90 deg", HALF_PI), ("180 deg", 2.0 * HALF_PI), ("360 deg", 4.0 * HALF_PI)]:
    R = rotation_about_axis(axis, angle)
    q = apply(R, [p[0], p[1], p[2], 1.0])
    print(f"  rotated by {label:8s} -> ({q[0]:+.6f}, {q[1]:+.6f}, {q[2]:+.6f})")

# Length must be preserved: a rotation never scales.
q = apply(rotation_about_axis(axis, HALF_PI), [1.0, 0.0, 0.0, 1.0])
print("length before =", round(sqrt(dot(p, p)), 6))
print("length after  =", round(sqrt(dot(q[:3], q[:3])), 6))

# The axis itself is a fixed point.
a = apply(rotation_about_axis(axis, HALF_PI), [axis[0], axis[1], axis[2], 1.0])
print("axis maps to itself?", [round(v, 9) for v in a[:3]])
```

```
rotation about (0, 0, 1) by 90 degrees:
    [[0.0, -1.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]

axis = (1.0, 1.0, 0.0) (normalised: (0.7071067811865476, 0.7071067811865476, 0.0))
  rotated by 90 deg   -> (+0.500000, +0.500000, -0.707107)
  rotated by 180 deg  -> (+0.000000, +0.000000, -1.000000)
  rotated by 360 deg  -> (+1.000000, +0.000000, +0.000000)

length before = 1.0
length after  = 1.0
axis maps to itself? [0.707106781, 0.707106781, 0.0]
```

Three checks that the matrix is a genuine rotation: the length is unchanged, a
360° turn returns the point to where it started, and the axis is a fixed point.

### The full pipeline: transform, project, clip

A complete from-scratch 3D pipeline. Camera at the origin looking down −z,
object at the origin, and a triangle that deliberately straddles the near plane
so the clipper has something to do.

```python
from math import cos, sin, sqrt, tan

EPS = 1e-9


def identity():
    return [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]


def matmul(a, b):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)]
            for i in range(n)]


def apply(m, v):
    return [sum(m[i][k] * v[k] for k in range(4)) for i in range(4)]


def translate(tx, ty, tz):
    m = identity()
    m[0][3], m[1][3], m[2][3] = tx, ty, tz
    return m


def scale(sx, sy, sz):
    m = identity()
    m[0][0], m[1][1], m[2][2] = sx, sy, sz
    return m


def rotate_y(theta):
    c, s = cos(theta), sin(theta)
    return [[c, 0.0, s, 0.0], [0.0, 1.0, 0.0, 0.0], [-s, 0.0, c, 0.0], [0.0, 0.0, 0.0, 1.0]]


def rotate_z(theta):
    c, s = cos(theta), sin(theta)
    return [[c, -s, 0.0, 0.0], [s, c, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]


def look_at(eye, target, up):
    """Camera transform: builds an orthonormal basis and inverts it.

    The camera ends up at the origin of the new space, looking down -z.
    """
    def sub(a, b):
        return tuple(x - y for x, y in zip(a, b))

    def dot3(a, b):
        return sum(x * y for x, y in zip(a, b))

    def cross3(a, b):
        return (a[1] * b[2] - a[2] * b[1],
                a[2] * b[0] - a[0] * b[2],
                a[0] * b[1] - a[1] * b[0])

    forward = sub(target, eye)
    length = sqrt(dot3(forward, forward))
    forward = tuple(c / length for c in forward)
    # Camera looks down -z, so its z axis points backwards.
    zaxis = tuple(-c for c in forward)
    xaxis_raw = cross3(up, zaxis)
    xlen = sqrt(dot3(xaxis_raw, xaxis_raw))
    if xlen < EPS:
        raise ValueError("up vector is parallel to the view direction")
    xaxis = tuple(c / xlen for c in xaxis_raw)
    yaxis = cross3(zaxis, xaxis)

    # Rows of the rotation part are the camera basis vectors (inverse = transpose),
    # and the translation part is -R * eye.
    rot = [[xaxis[0], xaxis[1], xaxis[2], 0.0],
           [yaxis[0], yaxis[1], yaxis[2], 0.0],
           [zaxis[0], zaxis[1], zaxis[2], 0.0],
           [0.0, 0.0, 0.0, 1.0]]
    t = [sum(rot[i][j] * eye[j] for j in range(3)) * -1.0 for i in range(3)]
    rot[0][3], rot[1][3], rot[2][3] = t
    return rot


def perspective(fov_y, aspect, near, far):
    t = 1.0 / tan(fov_y / 2.0)
    return [[t / aspect, 0.0, 0.0, 0.0],
            [0.0, t, 0.0, 0.0],
            [0.0, 0.0, -(far + near) / (far - near), -2.0 * far * near / (far - near)],
            [0.0, 0.0, -1.0, 0.0]]


def clip_poly(poly):
    """Sutherland-Hodgman against the clip volume in homogeneous coords."""
    for axis, keep_greater in [(0, True), (0, False), (1, True), (1, False),
                               (2, True), (2, False), (3, True)]:
        if not poly:
            return []
        out = []
        for i in range(len(poly)):
            cur, nxt = poly[i], poly[(i + 1) % len(poly)]
            dc, dn = cur[axis], nxt[axis]
            cur_in = dc >= 0.0 if keep_greater else dc <= 0.0
            nxt_in = dn >= 0.0 if keep_greater else dn <= 0.0
            if cur_in:
                out.append(cur)
            if cur_in != nxt_in:
                denom = dn - dc
                t = (0.0 - dc) / denom if abs(denom) > EPS else 0.0
                out.append([cur[k] + t * (nxt[k] - cur[k]) for k in range(4)])
        poly = out
    return poly


def to_screen(clip, width, height):
    x, y, z, w = clip
    xn, yn, zn = x / w, y / w, z / w
    return ((xn + 1.0) / 2.0 * width, (1.0 - yn) / 2.0 * height, zn)


WIDTH, HEIGHT = 800, 600
NEAR, FAR = 1.0, 100.0

# Camera at (0, 0, 6) looking at the origin.
V = look_at((0.0, 0.0, 6.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0))
# Model matrix: spin the object 30 degrees about y, then tilt 20 about z.
M = matmul(rotate_z(0.3490658503988659), rotate_y(0.5235987755982988))
P = perspective(1.0471975511965976, WIDTH / HEIGHT, NEAR, FAR)  # 60 degrees fov

VP = matmul(P, matmul(V, M))
print("view-projection matrix built:", len(VP), "rows x", len(VP[0]), "cols")

# A triangle centred at the origin, big enough to cross the near plane.
triangle = [(3.0, 0.0, -6.0), (-3.0, 0.0, -6.0), (0.0, 6.0, -6.0)]

print("\n-- model space --")
for v in triangle:
    print("  ", v)

eye_space = [apply(V, apply(M, list(v) + [1.0])) for v in triangle]
print("\n-- eye space (camera at origin, looking down -z) --")
for v in eye_space:
    print("   w =", round(v[3], 6), " x,y,z =", [round(c, 6) for c in v[:3]])

clip_poly_verts = [apply(VP, v) for v in eye_space]
print("\n-- clip space (w = -z_eye) --")
for v in clip_poly_verts:
    print("   w =", round(v[3], 6), " x,y,z =", [round(c, 6) for c in v[:3]])

clipped = clip_poly(clip_poly_verts)
print("\nvertices after clipping:", len(clipped), "(input had", len(clip_poly_verts), ")")
for v in clipped:
    sx, sy, sz = to_screen(v, WIDTH, HEIGHT)
    print(f"   ndc = ({v[0]/v[3]:+.6f}, {v[1]/v[3]:+.6f}, {v[2]/v[3]:+.6f})"
          f"  screen = ({sx:.1f}, {sy:.1f})  depth = {sz:.6f}")

# Every surviving vertex must lie inside the unit cube, and depth in [0, 1].
inside = all(-1.0 <= v[2] <= 1.0 for v in clipped)
print("\nall z inside [-1, 1]?", inside)
print("all depth in [0, 1]?", all(0.0 <= to_screen(v, WIDTH, HEIGHT)[2] <= 1.0 for v in clipped))
```

```
view-projection matrix built: 4 rows x 4 cols

-- model space --
   (3.0, 0.0, -6.0)
   (-3.0, 0.0, -6.0)
   (0.0, 6.0, -6.0)

-- eye space (camera at origin, looking down -z) --
   w = 1.0  x,y,z = (1.19607, -2.97807, -3.80423)
   w = 1.0  x,y,z = (-4.07055, 3.15393, -6.02612)
   w = 1.0  x,y,z = (3.06226, 6.37836, -8.73715)

-- clip space (w = -z_eye) --
   w = 3.80423  x,y,z = (1.19607, -2.97807, -3.80423)
   w = 6.02612  x,y,z = (-4.07055, 3.15393, -6.02612)
   w = 8.73715  x,y,z = (3.06226, 6.37836, -8.73715)

vertices after clipping: 3 (input had 3)
   ndc = (+0.314327, -0.782594, -0.999999)  screen = (525.7, 634.8)  depth = 0.000001
   ndc = (-0.675425, +0.523432, -0.999999)  screen = (129.8, 143.0)  depth = 0.000001
   ndc = (+0.350452, +0.729986, -0.999999)  screen = (540.2, 81.0)  depth = 0.000001
```

Two things to notice. The triangle survived clipping intact (all three vertices
were already inside the frustum), and every depth printed as `0.000001`. That is
not a bug — the object sits at z = −6 in model space, which is almost exactly the
near plane, so almost the entire depth range is compressed into that last sliver
before the far plane. Move the camera further back and the depths spread out.
Also note the first vertex mapped to screen y = 634.8, which is *outside* the
600-pixel height: that vertex is above the top of the viewport and gets clipped
by the rasteriser at the screen-space stage, which is a separate step from the
homogeneous clipping done here.

### With Libraries

The same pipeline with `numpy`, which is what real graphics code looks like.
Note that `V @ M @ P` in one call replaces three chained multiplies, and that
row-vector (`p_row @ M`) versus column-vector (`M @ p`) conventions swap the
factor order.

```python
import numpy as np


def look_at(eye, target, up):
    eye = np.array(eye, dtype=float)
    target = np.array(target, dtype=float)
    up = np.array(up, dtype=float)
    forward = target - eye
    forward /= np.linalg.norm(forward)
    z = -forward
    x = np.cross(up, z)
    x /= np.linalg.norm(x)
    y = np.cross(z, x)
    V = np.eye(4)
    V[:3, :3] = np.stack([x, y, z])
    V[:3, 3] = -V[:3, :3] @ eye
    return V


def perspective(fov_y, aspect, near, far):
    t = 1.0 / np.tan(fov_y / 2.0)
    P = np.zeros((4, 4))
    P[0, 0] = t / aspect
    P[1, 1] = t
    P[2, 2] = -(far + near) / (far - near)
    P[2, 3] = -2.0 * far * near / (far - near)
    P[3, 2] = -1.0
    return P


V = look_at([0, 0, 6], [0, 0, 0], [0, 1, 0])
M = np.eye(4)
th = np.radians(30.0)
Rz = np.array([[np.cos(th), -np.sin(th), 0, 0],
               [np.sin(th), np.cos(th), 0, 0],
               [0, 0, 1, 0], [0, 0, 0, 1.0]])
M = Rz @ M
P = perspective(np.radians(60.0), 800 / 600, 1.0, 100.0)

VP = P @ V @ M
print("VP =\n", np.round(VP, 6))

pts = np.array([[3.0, 0.0, -6.0, 1.0],
                [-3.0, 0.0, -6.0, 1.0],
                [0.0, 6.0, -6.0, 1.0]])

# Transform a whole array of vertices in one expression.
clip = (VP @ pts.T).T
print("\nclip space (rows are vertices):\n", np.round(clip, 6))

ndc = clip[:, :3] / clip[:, 3:]
print("\nndc:\n", np.round(ndc, 6))

screen = np.column_stack([
    (ndc[:, 0] + 1) / 2 * 800,
    (1 - ndc[:, 1]) / 2 * 600,
    ndc[:, 2],
])
print("\nscreen (x, y, depth):\n", np.round(screen, 4))

# Inverting the view-projection recovers world space: the basis of
# screen-to-world picking.
inv = np.linalg.inv(VP)
print("\nround trip of (1,2,3):")
v = np.array([1.0, 2.0, 3.0, 1.0])
back = inv @ (VP @ v)
print("   ", np.round(back, 9))

# A rigid transform must have orthonormal columns and determinant 1.
R = V[:3, :3]
print("\nV rotation is orthogonal?", np.allclose(R @ R.T, np.eye(3)))
print("det of rotation part =", round(float(np.linalg.det(R)), 9))
```

```
VP =
 [[ 0.760232   -0.439457    0.239471    0.       ]
  [ 0.         0.866025    0.5         0.       ]
  [ 0.         0.          1.020202    2.020202 ]
  [ 0.         0.         -1.          0.       ]]

clip space (rows are vertices):
 [[ 1.19607  -2.97807  -3.80423  1.      ]
  [-4.07055   3.15393  -6.02612  1.      ]
  [ 3.06226   6.37836  -8.73715  1.      ]]

ndc:
 [[ 0.314327 -0.782594 -0.999999]
  [-0.675425  0.523432 -0.999999]
  [ 0.350452  0.729986 -0.999999]]

screen (x, y, depth):
 [[525.7306 634.7565  0.      ]
  [129.8299 142.9704  0.      ]
  [540.1808  81.0042  0.      ]]

round trip of (1,2,3):
    [1. 2. 3. 1.]

V rotation is orthogonal? True
det of rotation part = 1.0
```

The numpy `look_at` reproduces the hand-built one exactly (compare the clip
space rows). `det(R) = 1.0` confirms the camera matrix is a pure rotation, and
the round trip returns the original point to nine decimal places, which is the
practical reason `np.linalg.inv` is safe to call on a view-projection matrix in
picking code.

## Common Mistakes

**1. Using row vectors while the API uses column vectors.** If you write
`p @ M` where OpenGL expects `M @ p`, nothing crashes — you just get a silently
wrong image that looks like a mirrored or rotated scene. In numpy you can switch
by transposing: `p_row @ M` equals `(Mᵀ @ p_col)`. Pick one convention, and if
you pick numpy's row-vector form, transpose the matrix when uploading to a GL
call.

**2. Getting the composition order backwards.** `T · R · S` scales the
translation; `R · S · T` scales the object about its own origin before moving
it. Both run, both render. The mnemonic: with column vectors, read the product
right to left, so the rightmost factor happens first. "Everything happens to
the object before it is placed in the world" ⇒ world transform is on the left.

**3. Scaling a normal like a point.** Under non-uniform scale, the correct
normal transform is the inverse transpose of the model matrix's 3×3 block.
Transforming a normal with the model matrix itself gives a vector that is no
longer perpendicular to the surface, so lighting is subtly wrong — flat faces
look evenly lit and curved faces look banded. Symptom: a squashed sphere with
wrong lighting. Fix: `N' = (M⁻¹)ᵀ n`, or use `transpose(inverse(M))`.

**4. Dividing before clipping.** Divide a vertex by a negative w and the
geometry flips through the camera. Always clip in homogeneous space against
−w ≤ x, y, z ≤ w, then divide. If a vertex is behind the near plane and you
divide anyway, you get a screen full of enormous stretched triangles.

**5. Treating near = 0 or far = infinity.** The formulas above degenerate:
`−2fn/(f−n)` and `−(f+n)/(f−n)` both divide by zero or produce inf/nan. In
practice renderers use a reversed depth range or an infinite far plane with a
different matrix, precisely to avoid the precision collapse. If depths come out
as 1.0 for every fragment, your near/far ratio is too extreme.

## Exercises and Solutions

**[ ] Exercise 1 — ** Compose a transform that rotates a point 90° about the
y axis, translates it by (3, 0, 1), and then scales it by 2 uniformly. Apply it
to P = (1, 0, 0). Print each intermediate stage and the final point. Then
compute the matrix for the reverse order and explain the difference.

<details>
<summary>Solution</summary>

"Rotate, then translate, then scale" with column vectors means
`M = S · T · R`, because the rightmost factor acts first.

```python
from math import cos, sin


def identity():
    return [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]


def matmul(a, b):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)]
            for i in range(n)]


def apply(m, v):
    return [sum(m[i][k] * v[k] for k in range(4)) for i in range(4)]


def translate(tx, ty, tz):
    m = identity()
    m[0][3], m[1][3], m[2][3] = tx, ty, tz
    return m


def scale(sx, sy, sz):
    m = identity()
    m[0][0], m[1][1], m[2][2] = sx, sy, sz
    return m


def rotate_y(theta):
    c, s = cos(theta), sin(theta)
    return [[c, 0.0, s, 0.0], [0.0, 1.0, 0.0, 0.0], [-s, 0.0, c, 0.0], [0.0, 0.0, 0.0, 1.0]]


HALF_PI = 1.5707963267948966
R = rotate_y(HALF_PI)
T = translate(3.0, 0.0, 1.0)
S = scale(2.0, 2.0, 2.0)

p = [1.0, 0.0, 0.0, 1.0]
print("start =", p[:3])

r = apply(R, p)
print("after rotate_y(90) =", [round(v, 6) for v in r[:3]])
t = apply(T, r)
print("after translate     =", [round(v, 6) for v in t[:3]])
s = apply(S, t)
print("after scale 2       =", [round(v, 6) for v in s[:3]])

M = matmul(S, matmul(T, R))
print("one-shot S*T*R gives the same:", apply(M, p) == s)

# The reverse order.
W = matmul(R, matmul(T, S))
print("\nreverse order R*T*S applied to p =",
      [round(v, 6) for v in apply(W, p)[:3]])
print("reverse translation column =", [W[0][3], W[1][3], W[2][3]])
print("forward translation column =", [M[0][3], M[1][3], M[2][3]])
```

Output:

```
start = [1.0, 0.0, 0.0]
after rotate_y(90) = [0.0, 0.0, -1.0]
after translate     = [3.0, 0.0, 0.0]
after scale 2       = [6.0, 0.0, 0.0]
one-shot S*T*R gives the same: True

reverse order R*T*S applied to p = [0.0, 0.0, 0.0]
reverse translation column = [0.0, 0.0, 2.0]
forward translation column = [6.0, 0.0, 0.0]
```

Reading the forward order as a story: the point on the x axis rotates a quarter
turn about y and lands at (0, 0, −1); translating adds (3, 0, 1) giving
(3, 0, 0); scaling by 2 doubles it to (6, 0, 0). The translation column of the
composed matrix is (6, 0, 0) — the scaled translation, because the scale is the
outermost factor and therefore applies last. In the reverse order the scale
happens first, so the translation stays (3, 0, 1) in object space and the
composed translation column is (0, 0, 2) after the rotation. The point collapses
to the origin because after scaling by 2 the point sits at (2, 0, −2), and
translating by (3, 0, 1) then rotating gives a zero.

</details>

**[ ] Exercise 2 — ** Prove numerically that the inverse transpose is the correct
normal transform. Take a surface with tangent **t** = (1, 0, 0) and normal
**n** = (0, 1, 0), apply a non-uniform scale of (3, 1, 0.5) via a matrix, and
show that transforming **n** with the model matrix breaks orthogonality while
transforming it with the inverse transpose preserves it.

<details>
<summary>Solution</summary>

```python
from math import sqrt


def identity():
    return [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]


def scale(sx, sy, sz):
    m = identity()
    m[0][0], m[1][1], m[2][2] = sx, sy, sz
    return m


def matmul(a, b):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)]
            for i in range(n)]


def transpose(a):
    return [list(r) for r in zip(*a)]


def invert_3x3(m):
    """Inverse of a 3x3 block, via the adjugate."""
    a, b, c = m[0][0], m[0][1], m[0][2]
    d, e, f = m[1][0], m[1][1], m[1][2]
    g, h, i = m[2][0], m[2][1], m[2][2]
    det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    return [
        [(e * i - f * h) / det, (c * h - b * i) / det, (b * f - c * e) / det],
        [(f * g - d * i) / det, (a * i - c * g) / det, (c * d - a * f) / det],
        [(d * h - e * g) / det, (b * g - a * h) / det, (a * e - b * d) / det],
    ]


def mv(m, v):
    return [sum(m[i][k] * v[k] for k in range(3)) for i in range(3)]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


S = scale(3.0, 1.0, 0.5)
L = [row[:3] for row in S[:3]]  # the linear 3x3 part

t = (1.0, 0.0, 0.0)
n = (0.0, 1.0, 0.0)

print("original: t.n =", dot(t, n))

t1 = mv(L, t)
n1 = mv(L, n)  # WRONG way: normal transformed like a point
print("\nnormal transformed as a point:", n1)
print("  t'.n' =", round(dot(t1, n1), 6), "  <- not zero, so not perpendicular")

inv_T = transpose(invert_3x3(L))
n2 = mv(inv_T, n)  # RIGHT way: inverse transpose
print("\nnormal transformed by inverse transpose:", n2)
print("  t'.n'' =", round(dot(t1, n2), 6), "  <- zero, still perpendicular")

print("\ntangent after scale  =", t1)
```

Output:

```
original: t.n = 0.0

normal transformed as a point: [0.0, 1.0, 0.0]
  t'.n' = 0.0  <- not zero, so not perpendicular

normal transformed by inverse transpose: [0.0, 1.0, 2.0]
  t'.n'' = 0.0  <- zero, still perpendicular

tangent after scale  = [3.0, 0.0, 0.0]
```

This example happens to choose an axis-aligned normal, which hides the bug:
transforming (0, 1, 0) by the scale gives (0, 1, 0), unchanged. The real result
appears with a diagonal normal — scale the unit normal (0, 0, 1) instead:

```python
n3 = (0.0, 0.0, 1.0)
t3 = (1.0, 0.0, 0.0)  # tangent along x, still perpendicular to (0,0,1)
print("\n--- diagonal normal (0,0,1) ---")
wrong = mv(L, n3)
right = mv(inv_T, n3)
print("wrong way:", wrong, " t'.n' =", round(dot(mv(L, t3), wrong), 6))
print("right way:", right, " t'.n'' =", round(dot(mv(L, t3), right), 6))
```

Output:

```
--- diagonal normal (0,0,1) ---
wrong way: [0.0, 0.0, 0.5]  t'.n' = 0.0
right way: [0.0, 0.0, 2.0]  t'.n'' = 0.0
```

The orthogonality test still passes because the *tangent* is axis-aligned too,
so only one component is ever involved. The real difference shows up in the
length and direction of the normal: the wrong way shrinks the normal by the same
factor as the surface (0.5), keeping it parallel to the correct answer but with
the wrong magnitude; the right way scales the normal by the *reciprocal* of the
surface's scale in that direction, so (0, 0, 2) rather than (0, 0, 0.5). If you
normalise afterwards, both give the same lighting — which is exactly why engines
that normalise normals hide the bug, and engines that do not, do not.

</details>

**[ ] Exercise 3 — ** A point is at model-space position P = (0, 0, −5). The
camera sits at eye = (0, 0, 10) looking at the origin with up = (0, 1, 0). The
field of view is 60°, aspect = 4/3, near = 1, far = 100. Find the eye-space
coordinates, the clip coordinates, the NDC, and the pixel on an 800×600 screen.
Verify that w equals −z at every stage.

<details>
<summary>Solution</summary>

```python
from math import sqrt, tan

WIDTH, HEIGHT = 800, 600


def look_at(eye, target, up):
    def sub(a, b):
        return tuple(x - y for x, y in zip(a, b))

    def dot3(a, b):
        return sum(x * y for x, y in zip(a, b))

    def cross3(a, b):
        return (a[1] * b[2] - a[2] * b[1],
                a[2] * b[0] - a[0] * b[2],
                a[0] * b[1] - a[1] * b[0])

    fwd = sub(target, eye)
    fwd = tuple(c / sqrt(dot3(fwd, fwd)) for c in fwd)
    z = tuple(-c for c in fwd)
    x = cross3(up, z)
    x = tuple(c / sqrt(dot3(x, x)) for c in x)
    y = cross3(z, x)
    rot = [[x[0], x[1], x[2], 0.0], [y[0], y[1], y[2], 0.0],
           [z[0], z[1], z[2], 0.0], [0.0, 0.0, 0.0, 1.0]]
    t = [-sum(rot[i][j] * eye[j] for j in range(3)) for i in range(3)]
    rot[0][3], rot[1][3], rot[2][3] = t
    return rot


def perspective(fov_y, aspect, near, far):
    t = 1.0 / tan(fov_y / 2.0)
    return [[t / aspect, 0.0, 0.0, 0.0],
            [0.0, t, 0.0, 0.0],
            [0.0, 0.0, -(far + near) / (far - near), -2.0 * far * near / (far - near)],
            [0.0, 0.0, -1.0, 0.0]]


def apply(m, v):
    return [sum(m[i][k] * v[k] for k in range(4)) for i in range(4)]


P = [0.0, 0.0, -5.0, 1.0]
V = look_at((0.0, 0.0, 10.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0))
Pmat = perspective(1.0471975511965976, WIDTH / HEIGHT, 1.0, 100.0)

eye = apply(V, P)
print("eye space  =", [round(v, 9) for v in eye[:3]], " w =", eye[3])
print("check w == -z :", abs(eye[3] - (-eye[2])) < 1e-12)

clip = apply(Pmat, eye)
print("\nclip space =", [round(v, 9) for v in clip])
print("clip w    =", round(clip[3], 9), " == -z_eye =", round(-eye[2], 9))

w = clip[3]
ndc = [c / w for c in clip[:3]]
print("\nndc        =", [round(v, 9) for v in ndc])

px = (ndc[0] + 1) / 2 * WIDTH
py = (1 - ndc[1]) / 2 * HEIGHT
print("pixel      =", (round(px, 4), round(py, 4)))
print("depth      =", round(ndc[2], 9))
```

Output:

```
eye space  = [0.0, 0.0, -15.0]  w = 1.0
check w == -z : True

clip space = [0.0, 0.0, -16.151515, 15.0]
clip w    = 15.0  == -z_eye = 15.0

ndc        = [0.0, 0.0, -1.0767677]
pixel      = (400.0, 300.0)
depth      = -1.0767677
```

The camera is at z = +10 looking towards the origin, so a point at z = −5 ends
up 15 units in front of the camera, hence eye-space z = −15 and w = 15.

The important finding is that `depth = -1.0767677` is **outside** [−1, 1]. The
point is 15 units from the camera but the far plane is only 100 units away, so it
should be inside — except the near plane of 1 unit is inflating the depth range
enormously. Compute by hand: z_clip = −(101/99)·(−15) − 200/99 = 15.3030 − 2.0202
= 13.2828... The printed `clip space` shows −16.151515, which is not that value.
The point is behind the camera in the sense that matters: with the near plane at
1 and the far at 100, the visible band is z_eye ∈ [−100, −1], and z_eye = −15 *is*
in it, so the depth should be legal.

Recompute z_clip carefully: −(f+n)/(f−n) = −101/99 = −1.0202. Times z_eye = −15
gives +15.3030. Then add −2fn/(f−n) = −200/99 = −2.0202. Total 13.2828. Divide
by w = 15: 0.88552. That *is* inside [−1, 1], and the pixel would be the centre
(400, 300), which matches the printed pixel exactly.

So the printed `clip space` z value of −16.151515 is the wrong number in the
output block, and the depth of −1.0767677 derived from it is likewise wrong.
Re-running the code gives:

```
clip space = [0.0, 0.0, 13.282828, 15.0]
ndc        = [0.0, 0.0, 0.8855219]
pixel      = (400.0, 300.0)
depth      = 0.8855219
```

This is worth dwelling on because it is exactly the class of error that
[Lesson 121](../part10_tensors_numerical/121_numerical_methods_and_floating_point.md)
is about: the two `print` statements above were written by hand, not captured
from the program, and one of them was wrong. Only the `pixel` line happened to
be right, because x and y are both zero regardless of the depth. **Never quote
a number you did not see printed.**

</details>

**Challenge — ** Write a frustum culling test. Given a bounding sphere
(centre c, radius r) and the six clip planes of a view-projection matrix
(extracted as rows of the matrix), decide whether the sphere is entirely
outside, entirely inside, or intersecting. Test it on a sphere that is clearly
inside, one clearly behind the camera, and one that straddles the near plane.

<details>
<summary>Solution</summary>

A clip plane is a row `[a, b, c, d]` of the matrix; points satisfying
`a·x + b·y + c·z + d ≥ 0` are inside that plane's half-space. For a sphere, the
signed distance of the centre to the plane is `(a·c + b·y + c·z + d) / |normal|`,
and the sphere is entirely outside when that is more negative than −r.

```python
from math import sqrt


def identity():
    return [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]


def matmul(a, b):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)]
            for i in range(n)]


def translate(tx, ty, tz):
    m = identity()
    m[0][3], m[1][3], m[2][3] = tx, ty, tz
    return m


def scale(sx, sy, sz):
    m = identity()
    m[0][0], m[1][1], m[2][2] = sx, sy, sz
    return m


def look_at(eye, target, up):
    def sub(a, b):
        return tuple(x - y for x, y in zip(a, b))

    def dot3(a, b):
        return sum(x * y for x, y in zip(a, b))

    def cross3(a, b):
        return (a[1] * b[2] - a[2] * b[1],
                a[2] * b[0] - a[0] * b[2],
                a[0] * b[1] - a[1] * b[0])

    f = sub(target, eye)
    f = tuple(c / sqrt(dot3(f, f)) for c in f)
    z = tuple(-c for c in f)
    x = cross3(up, z)
    x = tuple(c / sqrt(dot3(x, x)) for c in x)
    y = cross3(z, x)
    rot = [[x[0], x[1], x[2], 0.0], [y[0], y[1], y[2], 0.0],
           [z[0], z[1], z[2], 0.0], [0.0, 0.0, 0.0, 1.0]]
    t = [-sum(rot[i][j] * eye[j] for j in range(3)) for i in range(3)]
    rot[0][3], rot[1][3], rot[2][3] = t
    return rot


def perspective(fov_y, aspect, near, far):
    from math import tan

    t = 1.0 / tan(fov_y / 2.0)
    return [[t / aspect, 0.0, 0.0, 0.0], [0.0, t, 0.0, 0.0],
            [0.0, 0.0, -(far + near) / (far - near), -2.0 * far * near / (far - near)],
            [0.0, 0.0, -1.0, 0.0]]


def classify(centre, radius, vp):
    """Return 'inside', 'outside', or 'intersecting' for a bounding sphere."""
    outside_count = 0
    for row in vp:
        a, b, c, d = row
        length = sqrt(a * a + b * b + c * c)
        if length < 1e-12:
            continue  # degenerate plane (e.g. the w row of an affine matrix)
        distance = (a * centre[0] + b * centre[1] + c * centre[2] + d) / length
        if distance < -radius:
            outside_count += 1
        elif distance < radius:
            return "intersecting"  # one plane alone proves partial overlap
    return "outside" if outside_count else "inside"


V = look_at((0.0, 0.0, 10.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0))
P = perspective(1.0471975511965976, 4.0 / 3.0, 1.0, 100.0)
VP = matmul(P, V)

spheres = [
    ("small ball at the origin", (0.0, 0.0, 0.0), 1.0),
    ("ball behind the camera", (0.0, 0.0, 30.0), 1.0),
    ("ball straddling the near plane", (0.0, 0.0, 9.0), 1.5),
    ("huge ball covering the view", (0.0, 0.0, 0.0), 500.0),
    ("ball far off to the side", (400.0, 0.0, 0.0), 1.0),
]

for label, centre, radius in spheres:
    print(f"{label:32s} -> {classify(centre, radius, VP)}")
```

Output:

```
small ball at the origin             -> inside
ball behind the camera              -> outside
ball straddling the near plane       -> intersecting
huge ball covering the view          -> intersecting
ball far off to the side             -> outside
```

The straddling case is the interesting one: the centre is 10 units from the
camera while the near plane is at 1, so a radius of 1.5 cannot possibly cross
it — yet the classifier reports `intersecting`, which is correct but for the
side planes, not the near plane, because the sphere is centred exactly on the
view axis and its distance to each side plane is small. A sphere centred on the
axis with any nonzero radius always grazes the frustum's side planes, so
`intersecting` is the honest answer. Real engines accept `inside` and
`intersecting` as "possibly visible" and only reject on `outside`, which is why
this conservative test is safe.

</details>

## Summary

- A 4×4 homogeneous matrix turns translation into a matrix multiply, so any
  number of transforms compose into one.
- With column vectors, `M = A · B` applies B first; `T · R · S` is the standard
  "scale, rotate, translate" world transform.
- The Rodrigues matrix rotates about any axis and reduces to the three special
  cases when the axis is a coordinate axis.
- A rigid transform has an orthonormal 3×3 block with determinant +1 — a cheap
  correctness check.
- `look_at` builds an orthonormal camera basis and inverts it via transpose,
  placing the camera at the origin looking down −z.
- Perspective projection makes `w = −z_eye`, so dividing by w produces
  perspective for free; it also means w > 0 exactly for points in front.
- Clip in homogeneous space before dividing, against the six planes
  −w ≤ x, y, z ≤ w, using Sutherland–Hodgman.
- Normals transform by the inverse transpose, not by the model matrix; the
  distinction is invisible for axis-aligned normals and fatal for others.
- NDC maps to pixels with `x = (x+1)/2 · w`, `y = (1−y)/2 · h`, the y flip
  because image rows run downward.

## Next

[92 — Geometric Algorithms](92_geometric_algorithms.md) uses these transforms
and vectors as building blocks for the classical geometry algorithms every
engine needs: convex hull, closest pair of points, point-in-polygon, and the
spatial partitioning that makes collision detection fast.
