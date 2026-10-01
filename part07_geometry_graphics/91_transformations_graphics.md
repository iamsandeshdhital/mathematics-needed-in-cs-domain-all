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

Build the transform for a point P = (1, 0, 0): scale by 2 in x, rotate 90° about
z, then translate by (0, 5, 0).

**Step 1 — the matrices.** For θ = 90°, c = 0 and s = 1:

```
S  = ⎡2 0 0 0; 0 1 0 0; 0 0 1 0; 0 0 0 1⎦
Rz = ⎡0 −1 0 0; 1 0 0 0; 0 0 1 0; 0 0 0 1⎦
T  = ⎡1 0 0 0; 0 1 0 5; 0 0 1 0; 0 0 0 1⎦
```

**Step 2 — apply them in order.** With column vectors, `M = T · Rz · S`.

S·P = (2, 0, 0, 1)ᵀ. The point stretched along x.

Rz·(2, 0, 0, 1)ᵀ = (0·2 + (−1)·0 + 0, 1·2 + 0·0 + 0, 0, 1)ᵀ = (0, 2, 0, 1)ᵀ.

T·(0, 2, 0, 1)ᵀ = (0, 2 + 5, 0, 1)ᵀ = (0, 7, 0, 1)ᵀ.

The point ends at **(0, 7, 0)**. As a story: a unit point on the x axis stretched
to x = 2, swept a quarter turn onto the y axis at height 2, then lifted 5 more.
That is "scale, then rotate, then translate".

**Step 3 — why the order matters.** Compose the single matrix M = T·Rz·S.
First Rz·S scales the rows: ⎡0 −1 0 0; 2 0 0 0; 0 0 1 0; 0 0 0 1⎦. Then T
combines row 1 as `row 1 + 5·row 3` = (2, 0, 0, 5), leaving the others alone:

```
M = ⎡0 −1 0 0; 2 0 0 5; 0 0 1 0; 0 0 0 1⎦
```

Check: M·P = (0, 2 + 5, 0, 1)ᵀ = (0, 7, 0, 1)ᵀ. Matches.

Now the *other* order, S·Rz·T, on the same point:
T·P = (1, 5, 0, 1)ᵀ → Rz·(1, 5, 0, 1)ᵀ = (−5, 1, 0, 1)ᵀ → S·(−5, 1, 0, 1)ᵀ =
(−10, 1, 0, 1)ᵀ.

Completely different point: **(−10, 1, 0)**. Worse, the translation itself got
rotated and scaled, which is never what you want. That is why the convention
exists and why `R · S · T` is the mnemonic worth memorising.

**Step 4 — the arbitrary-axis formula as a self-check.** Take **u** = (0, 0, 1),
θ = 90°, so c = 0 and s = 1. Substituting:

- R₀₀ = c + u₁²(1−c) = 0
- R₀₁ = u₁u₂(1−c) − u₃s = 0 − 1 = −1
- R₁₀ = u₂u₁(1−c) + u₃s = 0 + 1 = 1
- R₁₁ = c + u₂²(1−c) = 0
- R₂₂ = c + u₃²(1−c) = 0 + 1 = 1

which is exactly Rz. The general formula is a unification of the three special
cases, not separate mathematics.

**Step 5 — perspective projection.** Take θ = 90°, aspect = 1, n = 1, f = 10,
and P = (1, 1, −3) — one unit right, one unit up, three units in front. Since
tan(45°) = 1, the matrix is

```
P = ⎡1 0 0 0; 0 1 0 0; 0 0 −11/9 −20/9; 0 0 −1 0⎦
```

w = −z = 3, so x_ndc = 1/3 and y_ndc = 1/3. For depth:
z_clip = (−11/9)(−3) + (−20/9)(1) = 33/9 − 20/9 = 13/9 ≈ 1.4444, and
z_ndc = (13/9)/3 = 13/27 ≈ 0.4815.

The point lands at (0.3333, 0.3333, 0.4815). On an 800×600 screen that is pixel
((1 + 0.3333)/2 · 800, (1 − 0.3333)/2 · 600) = (533.3, 200.0) — shifted right
and up from the centre, as expected for a point up and to the right.

Compare (1, 1, −6), twice as far away. Now w = 6, so x_ndc = 1/6 = 0.1667 and
the pixel is (466.7, 250.0). Half the offset for double the depth, and that came
from the division by w alone. **That is perspective.**

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

A complete from-scratch 3D pipeline: model matrix, view matrix, projection,
Sutherland–Hodgman clipping, NDC-to-pixel mapping. Two triangles go through it —
one comfortably inside the frustum, and one with a vertex *behind* the camera,
which is the case that forces the w-planes to exist.

```python
from math import cos, sin, sqrt, tan

EPS = 1e-9


def identity():
    return [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]


def matmul(a, b):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)]
            for i in range(n)]


def apply(m, v):
    return [sum(m[i][k] * v[k] for k in range(4)) for i in range(4)]


def rotate_y(theta):
    c, s = cos(theta), sin(theta)
    return [[c, 0.0, s, 0.0], [0.0, 1.0, 0.0, 0.0], [-s, 0.0, c, 0.0], [0.0, 0.0, 0.0, 1.0]]


def rotate_z(theta):
    c, s = cos(theta), sin(theta)
    return [[c, -s, 0.0, 0.0], [s, c, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]


def look_at(eye, target, up):
    """Camera transform: build an orthonormal basis, then invert it.

    Inverting a rotation is transposing it, so the camera basis vectors become
    the rows of the matrix, and the translation part is -R * eye. The result
    puts the camera at the origin of the new space, looking down -z.
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
    forward = tuple(c / sqrt(dot3(forward, forward)) for c in forward)
    # The camera looks down -z, so its own z axis points back along the view.
    zaxis = tuple(-c for c in forward)
    xaxis_raw = cross3(up, zaxis)
    xlen = sqrt(dot3(xaxis_raw, xaxis_raw))
    if xlen < EPS:
        raise ValueError("up vector is parallel to the view direction")
    xaxis = tuple(c / xlen for c in xaxis_raw)
    yaxis = cross3(zaxis, xaxis)

    V = [[xaxis[0], xaxis[1], xaxis[2], 0.0],
         [yaxis[0], yaxis[1], yaxis[2], 0.0],
         [zaxis[0], zaxis[1], zaxis[2], 0.0],
         [0.0, 0.0, 0.0, 1.0]]
    t = [-sum(V[i][j] * eye[j] for j in range(3)) for i in range(3)]
    V[0][3], V[1][3], V[2][3] = t
    return V


def perspective(fov_y, aspect, near, far):
    """Maps eye space to clip space. Row 3 is (0, 0, -1, 0), so
    w_clip = -z_eye: exactly the depth you want to divide by."""
    t = 1.0 / tan(fov_y / 2.0)
    return [[t / aspect, 0.0, 0.0, 0.0],
            [0.0, t, 0.0, 0.0],
            [0.0, 0.0, -(far + near) / (far - near), -2.0 * far * near / (far - near)],
            [0.0, 0.0, -1.0, 0.0]]


# The six clip planes, each as a function of a homogeneous vertex (x,y,z,w)
# returning a non-negative value inside. These are the planes of the cube
# -w <= x, y, z <= w, written so that "inside" always means ">= 0".
# The w <= ... tests are what stop the perspective divide from flipping the
# geometry inside out for vertices behind the camera.
PLANE_NAMES = ["x >= -w", "x <= w", "y >= -w", "y <= w", "z >= -w", "z <= w", "w >= 0"]
PLANE_DISTANCE = [
    lambda v: v[0] + v[3], lambda v: v[3] - v[0],
    lambda v: v[1] + v[3], lambda v: v[3] - v[1],
    lambda v: v[2] + v[3], lambda v: v[3] - v[2],
    lambda v: v[3],
]


def clip_poly(poly):
    """Sutherland-Hodgman: clip a polygon against each plane in turn.

    Vertices are kept or discarded by the sign of the plane distance, and
    crossings are found by linear interpolation between two vertices with
    opposite signs. Working in homogeneous space means no division by w is
    needed until the very last step.
    """
    for plane, name in zip(PLANE_DISTANCE, PLANE_NAMES):
        if not poly:
            return []
        out = []
        for i in range(len(poly)):
            cur, nxt = poly[i], poly[(i + 1) % len(poly)]
            dc, dn = plane(cur), plane(nxt)
            if dc >= 0.0:
                out.append(cur)
            if (dc >= 0.0) != (dn >= 0.0):
                # One endpoint is in and one is out: find the crossing point.
                denom = dc - dn
                t = dc / denom if abs(denom) > EPS else 0.0
                out.append([cur[k] + t * (nxt[k] - cur[k]) for k in range(4)])
        poly = out
    return poly


def to_screen(clip, width, height):
    """Clip -> NDC -> pixels. Image row 0 is at the top, hence 1 - y."""
    x, y, z, w = clip
    xn, yn, zn = x / w, y / w, z / w
    return ((xn + 1.0) / 2.0 * width, (1.0 - yn) / 2.0 * height, zn)


WIDTH, HEIGHT, NEAR, FAR = 800, 600, 1.0, 100.0
V = look_at((0.0, 0.0, 10.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0))
P = perspective(1.0471975511965976, WIDTH / HEIGHT, NEAR, FAR)  # 60 degree fov

# Two objects, so two model matrices. A spins in place at the origin; B is
# static and pokes through the camera.
MODEL_A = matmul(rotate_z(0.3490658503988659), rotate_y(0.5235987755982988))
MODEL_B = identity()

TRI_A = [(1.0, 0.5, 0.0), (-1.0, 0.5, 0.0), (0.0, 0.5, -1.5)]
TRI_B = [(0.0, 0.0, 11.0), (1.5, 1.0, 8.0), (-1.5, 1.0, 8.0)]


def pipeline(label, tri, model):
    print(f"===== {label} =====")
    # Stage 1: model -> eye space. Model matrix first, then view matrix.
    eye_pts = [apply(V, apply(model, list(v) + [1.0])) for v in tri]
    print("eye space (camera at origin, looking down -z):")
    for v in eye_pts:
        print(f"    ({v[0]:+8.4f}, {v[1]:+8.4f}, {v[2]:+8.4f})  w = {v[3]:.1f}")

    # Stage 2: eye -> clip space. After this, w should equal -z_eye.
    clip_pts = [apply(P, v) for v in eye_pts]
    print("clip space (w == -z_eye):")
    for v in clip_pts:
        print(f"    ({v[0]:+8.4f}, {v[1]:+8.4f}, {v[2]:+8.4f})  w = {v[3]:8.4f}")

    # Stage 3: clip. Must happen before any division by w.
    clipped = clip_poly(clip_pts)
    print(f"after clipping: {len(clipped)} vertices (input had {len(clip_pts)})")
    for v in clipped:
        xn, yn, zn = v[0] / v[3], v[1] / v[3], v[2] / v[3]
        sx, sy, _ = to_screen(v, WIDTH, HEIGHT)
        print(f"    ndc = ({xn:+.6f}, {yn:+.6f}, {zn:+.6f})"
              f"  pixel = ({sx:7.1f}, {sy:7.1f})")
    print()
    return clipped


print("Camera at (0,0,10) looking down -z, 60 deg fov, near 1, far 100.\n")
a = pipeline("Triangle A, fully inside", TRI_A, MODEL_A)
b = pipeline("Triangle B, straddles the near plane", TRI_B, MODEL_B)

# Post-conditions that must hold for any correct pipeline.
print("all A z inside [-1, 1]?", all(-1.0 <= c[2] / c[3] <= 1.0 for c in a))
print("all B z inside [-1, 1]?", all(-1.0 <= c[2] / c[3] <= 1.0 for c in b))
print("B gained vertices from clipping?", len(b) > 3)
```

```
Camera at (0,0,10) looking down -z, 60 deg fov, near 1, far 100.

===== Triangle A, fully inside =====
eye space (camera at origin, looking down -z):
    ( +0.6428,  +0.7660, -10.5000)  w = 1.0
    ( -0.9848,  +0.1736,  -9.5000)  w = 1.0
    ( -0.8758,  +0.2133, -11.2990)  w = 1.0
clip space (w == -z_eye):
    ( +0.8350,  +1.3268,  +8.6919)  w =  10.5000
    ( -1.2793,  +0.3008,  +7.6717)  w =   9.5000
    ( -1.1377,  +0.3695,  +9.5071)  w =  11.2990
after clipping: 3 vertices (input had 3)
    ndc = (+0.079524, +0.126365, +0.827802)  pixel = (  431.8,   262.1)
    ndc = (-0.134663, +0.031660, +0.807549)  pixel = (  346.1,   290.5)
    ndc = (-0.100687, +0.032702, +0.841408)  pixel = (  359.7,   290.2)

===== Triangle B, straddles the near plane =====
eye space (camera at origin, looking down -z):
    ( +0.0000,  +0.0000,  +1.0000)  w = 1.0
    ( +1.5000,  +1.0000,  -2.0000)  w = 1.0
    ( -1.5000,  +1.0000,  -2.0000)  w = 1.0
clip space (w == -z_eye):
    ( +0.0000,  +0.0000,  -3.0404)  w =  -1.0000
    ( +1.9486,  +1.7321,  +0.0202)  w =   2.0000
    ( -1.9486,  +1.7321,  +0.0202)  w =   2.0000
after clipping: 6 vertices (input had 3)
    ndc = (+1.000000, +0.888889, -0.069900)  pixel = (  800.0,    33.3)
    ndc = (+0.974279, +0.866025, +0.010101)  pixel = (  789.7,    40.2)
    ndc = (-0.974279, +0.866025, +0.010101)  pixel = (   10.3,    40.2)
    ndc = (-1.000000, +0.888889, -0.069900)  pixel = (    0.0,    33.3)
    ndc = (-1.000000, +1.000000, -0.458689)  pixel = (    0.0,     0.0)
    ndc = (+1.000000, +1.000000, -0.458689)  pixel = (  800.0,    -0.0)

all A z inside [-1, 1]? True
all B z inside [-1, 1]? True
B gained vertices from clipping? True
```

Triangle B is the interesting one. Its first vertex sits at eye-space z = +1,
which is *behind* the camera, so w = −z_eye = −1: a negative divisor. Dividing
by that would throw the vertex to infinity and flip the triangle through the
screen. Instead the clipper keeps two vertices, discards one, and inserts four
new ones where edges cross the planes — the 3-gon becomes a 6-gon. Every
surviving vertex has ndc x and y inside [−1, 1] and pixels on or near the
viewport edges, which is exactly what "clipped against the side walls" looks
like.

Note also that `w == -z_eye` holds for every vertex in both triangles, and that
triangle A gained no vertices because nothing needed clipping. A's depths
(0.8075, 0.8278, 0.8414) spread across a real range because it is 10–11 units
from a camera whose far plane is at 100.

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


V = look_at([0, 0, 10], [0, 0, 0], [0, 1, 0])

# Model A: spin 30 deg about y, then tilt 20 deg about z. Same order as above.
ty = np.radians(30.0)
tz = np.radians(20.0)
Ry = np.array([[np.cos(ty), 0, np.sin(ty), 0],
               [0, 1, 0, 0],
               [-np.sin(ty), 0, np.cos(ty), 0],
               [0, 0, 0, 1.0]])
Rz = np.array([[np.cos(tz), -np.sin(tz), 0, 0],
               [np.sin(tz), np.cos(tz), 0, 0],
               [0, 0, 1, 0],
               [0, 0, 0, 1.0]])
M = Rz @ Ry

P = perspective(np.radians(60.0), 800 / 600, 1.0, 100.0)

# Column vectors: VP = P @ V @ M, and the rightmost factor acts first.
VP = P @ V @ M
print("VP =\n", np.round(VP, 6))

pts = np.array([[1.0, 0.5, 0.0, 1.0],
                [-1.0, 0.5, 0.0, 1.0],
                [0.0, 0.5, -1.5, 1.0]])

# One expression transforms every vertex: the @ applies to each row.
clip = (VP @ pts.T).T
print("\nclip space (one row per vertex):\n", np.round(clip, 6))

ndc = clip[:, :3] / clip[:, 3:]
print("\nndc:\n", np.round(ndc, 6))

screen = np.column_stack([
    (ndc[:, 0] + 1) / 2 * 800,
    (1 - ndc[:, 1]) / 2 * 600,
    ndc[:, 2],
])
print("\nscreen (x, y, depth):\n", np.round(screen, 4))

# Row-vector users write pts @ VP.T instead -- same numbers, opposite look.
print("\nrow-vector form matches:", np.allclose(pts @ VP.T, clip))

# Inverting the view-projection recovers world space: the basis of
# screen-to-world picking.
inv = np.linalg.inv(VP)
v = np.array([1.0, 2.0, 3.0, 1.0])
back = inv @ (VP @ v)
print("\nround trip of (1, 2, 3):", np.round(back, 9))

# A rigid transform must have orthonormal rows and determinant +1.
R = V[:3, :3]
print("\nV rotation orthogonal?", np.allclose(R @ R.T, np.eye(3)))
print("det of rotation part =", round(float(np.linalg.det(R)), 9))

# Scaling, rotation and translation are single @ products away.
S = np.diag([2.0, 1.0, 1.0, 1.0])
p = np.array([1.0, 0.0, 0.0, 1.0])
print("\nS @ p =", S @ p)
print("(S @ R) @ p =", (S @ Rz) @ p, " -- scale applied after rotation")
```

```
VP =
 [[ 1.057154 -0.444297  0.610348  0.      ]
  [ 0.51303   1.627595  0.296198  0.      ]
  [ 0.510101  0.       -0.883521  8.181818]
  [ 0.5       0.       -0.866025 10.      ]]

clip space (one row per vertex):
 [[ 0.835006  1.326828  8.691919 10.5     ]
  [-1.279303  0.300767  7.671717  9.5     ]
  [-1.137671  0.3695    9.507099 11.299038]]

ndc:
 [[ 0.079524  0.126365  0.827802]
  [-0.134663  0.03166   0.807549]
  [-0.100687  0.032702  0.841408]]

screen (x, y, depth):
 [[431.8097 262.0906   0.8278]
  [346.1346 290.5021   0.8075]
  [359.725  290.1894   0.8414]]

row-vector form matches: True

round trip of (1, 2, 3): [1. 2. 3. 1.]

V rotation orthogonal? True
det of rotation part = 1.0
```

The clip space rows here are identical to the ones the plain-Python pipeline
printed for triangle A — the numpy `look_at` reproduces the hand-built matrix
exactly. `row-vector form matches: True` is the one-liner that proves the two
conventions are interchangeable. `det(R) = 1.0` confirms the camera matrix is a
pure rotation, and the round trip returns the original point to nine decimal
places, which is the practical reason `np.linalg.inv` is safe to call on a
view-projection matrix in picking code.

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

## Formula Sheet

**M** is a 4×4 homogeneous transform; **p** = (x, y, z, 1)ᵀ is a point in homogeneous
coordinates; **t** = (tx, ty, tz) is a translation; $\mathbf{L}$ is the top-left 3×3
block; $\theta$ is a rotation angle; **u** is a unit axis; $\mathbf{w}$ and
$\mathbf{e}$ are the plane's normal and offset; $n$ and $f$ are the near and far
distances; $c = \cos\theta$, $s = \sin\theta$.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| Homogeneous lift | $(x,y,z) \mapsto (x,y,z,1)$ | add a fourth coordinate fixed at 1 so a 4×4 matrix can act on a 3D point | every time you feed a 3D point to a 4×4 matrix |
| Transform | $\mathbf{p}' = \mathbf{M}\mathbf{p}$ | the new position is the matrix times the old one, column style | the one line that runs the whole pipeline |
| Block form | $\mathbf{M} = \begin{pmatrix}\mathbf{L} & \mathbf{t} \\ \mathbf{0}^{T} & 1\end{pmatrix}$ | a 3×3 that rotates/scales, plus a 3-vector that moves | reading any composed matrix; translation must be top-right for column vectors |
| $\mathbf{I}_4$ | $\mathbf{I}\mathbf{M} = \mathbf{M}\mathbf{I} = \mathbf{M}$ | the do-nothing matrix | starting point for building T, S, R; the neutral element in a product |
| Translation $\mathbf{T}(\mathbf{t})$ | $\begin{pmatrix}1&0&0&t_x\\0&1&0&t_y\\0&0&1&t_z\\0&0&0&1\end{pmatrix}$ | 1s on the diagonal, the offset in the last column | moving an object or the camera |
| Scale $\mathbf{S}$ | $\mathrm{diag}(s_x,s_y,s_z,1)$ | multiply each coordinate by its own factor | resizing; **requires $s_i \ne 0$** for the matrix to be invertible |
| $\mathbf{R}_x(\theta)$ | $\begin{pmatrix}1&0&0\\0&c&-s\\0&s&c\end{pmatrix}$ | spin about the **x** axis; y and z mix | rolling a model |
| $\mathbf{R}_y(\theta)$ | $\begin{pmatrix}c&0&s\\0&1&0\\-s&0&c\end{pmatrix}$ | spin about **y**; x and z mix | the most common turn in a game |
| $\mathbf{R}_z(\theta)$ | $\begin{pmatrix}c&-s&0\\s&c&0\\0&0&1\end{pmatrix}$ | spin about **z**; x and y mix — this is the 2D rotation matrix | screen-space and sprite rotation |
| Rodrigues $\mathbf{R}(\mathbf{u},\theta)$ | $c\mathbf{I} + (1-c)\mathbf{u}\mathbf{u}^{T} + s[\mathbf{u}]_{\times}$, expanded in the lesson | rotate by $\theta$ about **any** axis, right-hand rule | physics joints, arcball cameras; **requires $\|\mathbf{u}\|=1$** — normalise first |
| Self-check for Rodrigues | $\mathbf{u}=(0,0,1),\ \theta=90° \Rightarrow \mathbf{R}_z$ | the general formula reduces to the special cases | catching a sign or transpose error |
| **Composition order** | $\mathbf{M}=\mathbf{A}\cdot\mathbf{B} \Rightarrow$ **B** first, then **A** | read the product right to left | every multi-transform; the #1 source of graphics bugs |
| Standard object transform | $\mathbf{M} = \mathbf{T}\cdot\mathbf{R}\cdot\mathbf{S}$ | scale, then rotate, then place in the world | a scene node's local-to-parent matrix |
| Translation column of a product | $(\mathbf{T}\cdot\mathbf{R}\cdot\mathbf{S})$'s column 3 $= \mathbf{R}\mathbf{S}\mathbf{t}$ | anything left of T also acts on the offset | diagnosing a wrong order: compare column 3 against $\mathbf{t}$ |
| Scene graph | $\mathbf{M}_{\text{world}} = \mathbf{M}_{\text{parent}}\cdot\mathbf{M}_{\text{child}}$, so $\mathbf{p}_{\text{world}} = \mathbf{P}(\mathbf{C}\mathbf{p_{\text{local}})$ | the child's transform happens first, entirely in its own frame | hierarchy traversal; generally $\mathbf{P}\cdot\mathbf{C} \ne \mathbf{C}\cdot\mathbf{P}$ |
| `look_at` basis | $\mathbf{f}=\frac{\text{target}-\text{eye}}{\lVert\text{target}-\text{eye}\rVert}$, $\mathbf{z}=-\mathbf{f}$, $\mathbf{x}=\frac{\mathbf{up}\times\mathbf{z}}{\lVert\cdot\rVert}$, $\mathbf{y}=\mathbf{z}\times\mathbf{x}$ | build a right-handed camera basis looking down −z | building the view matrix |
| View matrix | rows are $\mathbf{x},\mathbf{y},\mathbf{z}$; translation $=-(\mathbf{R}\,\text{eye})$ | transpose to invert a rotation, then negate the camera's position | placing the world relative to a camera; **requires `up` not parallel to the view direction** |
| Projection $\mathbf{P}(\theta,a,n,f)$ | $\begin{pmatrix}\frac{1}{a\tan(\theta/2)}&0&0&0\\0&\frac{1}{\tan(\theta/2)}&0&0\\0&0&-\frac{f+n}{f-n}&-\frac{2fn}{f-n}\\0&0&-1&0\end{pmatrix}$ | the matrix that turns 3D eye coordinates into a 2D image with depth | the projection stage; **requires $0<n<f$** and $\theta>0$ |
| Aspect ratio | $a = \dfrac{\text{width}}{\text{height}}$ | widen the horizontal field to match the image | choosing the top-left entry; **must** match the viewport or the image stretches |
| Depth from division | $w_{\text{clip}} = -z_{\text{eye}}$ | the fourth coordinate *is* the distance in front of the camera | why dividing by w produces perspective for free; $w>0$ exactly for points in front |
| Near/far mapping | $z_{\text{eye}}=-n \Rightarrow z_{\text{ndc}}=-1$; $\quad z_{\text{eye}}=-f \Rightarrow z_{\text{ndc}}=+1$ | the two depth planes land on the two ends of [−1, 1] | sanity-checking the matrix; **depth increases with distance**, so the depth test is `LESS` |
| NDC | $(x,y,z)_{\text{ndc}} = (x,y,z)_{\text{clip}} / w$ | divide by the distance — the perspective step | converting to anything screen-shaped |
| Clip volume | $-w \le x,y,z \le w$, $\quad w \ge 0$ | the seven-sided box of visible homogeneous coordinates | the clipping stage; **must be enforced before dividing** |
| Plane distance (homogeneous) | $d(v) = a\,v_x + b\,v_y + c\,v_z + d\,v_w$ | how far a vertex is from a clip plane; ≥ 0 means inside | Sutherland–Hodgman, without ever dividing by $w$ |
| Edge–plane intersection | $t = \dfrac{d_{\text{cur}}}{d_{\text{cur}}-d_{\text{nxt}}}$, point $= \mathbf{v}_{\text{cur}} + t(\mathbf{v}_{\text{nxt}}-\mathbf{v}_{\text{cur}})$ | slide along the edge to where it crosses | generating the new vertices clipping adds |
| Screen mapping | $x_{\text{screen}}=\frac{x_{\text{ndc}}+1}{2}\cdot\text{width}$, $\; y_{\text{screen}}=\frac{1-y_{\text{ndc}}}{2}\cdot\text{height}$ | NDC → pixels; the y flip is because image row 0 is the top | the viewport transform; getting y backwards flips the scene vertically |
| Normal transform | $\mathbf{n}' = (\mathbf{M}^{-1})^{T}\mathbf{n}$ | transform normals by the *inverse transpose* of the linear block | lighting under non-uniform scale; **requires $\mathbf{M}$ invertible**, i.e. no zero scale factor |
| Rigid-transform test | $\mathbf{R}\mathbf{R}^{T} = \mathbf{I}$ and $\det(\mathbf{R}) = +1$ | orthonormal rows and positive orientation — no scaling, no mirroring | a cheap assertion on every model and view matrix |
| Pure-rotation shortcut | $(\mathbf{R}^{-1})^{T} = \mathbf{R}^{T}$ | for a rotation, the inverse transpose is just the transpose | skipping the inverse when the matrix is known to be rigid |
| Frustum plane test | $\text{dist} = \dfrac{\mathbf{e}\cdot\mathbf{c} + d}{\lVert\mathbf{e}\rVert}$; outside iff $\text{dist} < -r$ | signed distance from a bounding sphere's centre to a clip plane | frustum culling; rows with $\lVert\mathbf{e}\rVert=0$ are skipped as degenerate |
| Pick ray | $\mathbf{p}_{\text{near}}=(\mathbf{VP})^{-1}(x_{\text{ndc}},y_{\text{ndc}},-1,1)$, $\mathbf{p}_{\text{far}}=(\mathbf{VP})^{-1}(x_{\text{ndc}},y_{\text{ndc}},+1,1)$ | undo the pipeline at the two depth extremes to get the click ray | click-to-select; **requires the view-projection to be invertible** |
| Pixel → NDC | $x_{\text{ndc}}=\frac{2x_{\text{screen}}}{\text{width}}-1$, $\; y_{\text{ndc}}=1-\frac{2y_{\text{screen}}}{\text{height}}$ | inverts the viewport transform exactly | picking code; the y form must match the y flip above |

## Multiple Choice Questions

**Q1.** With column vectors, you compute `M = A · B` and then apply it to a point.
Which of A and B acts on the point first?

- A) A, because matrix multiplication is left-to-right
- B) B, because the rightmost factor in a product of matrices acting on a vector is applied first
- C) A, but only when A is a rotation and B is a translation
- D) Neither — both act simultaneously, which is why the order cannot matter

<details>
<summary>Answer and explanation</summary>

**B) B, because the rightmost factor in a product of matrices acting on a vector is applied first.**

$(AB)\mathbf{p} = A(B\mathbf{p})$ by associativity of matrix multiplication: B's product is formed first and its output is fed to A. The lesson's worked example applies this directly — with `M = T · Rz · S` and P = (1, 0, 0), the printed stages are `[2.0, 0.0, 0.0]` then `[0.0, 2.0, 0.0]` then `[0.0, 7.0, 0.0]`, i.e. scale, then rotate, then translate.

A) is the row-vector reading. Under the row convention `p_row M` the leftmost factor acts first, which is why numpy code is often confusing to people coming from OpenGL: numpy's `pts @ M` is the row form, and the lesson's `row-vector form matches: True` line shows the two conventions are the same computation written backwards.

C) is false and dangerous, because it is the kind of half-truth that survives code review. Nothing about the algebra depends on the *types* of the factors — the order is determined purely by the position of the factor in the product. What is true is that the *consequences* differ by type: putting T to the left of R rotates the translation, which is the bug people actually hit.

D) is false because the two orders produce different numbers on the same point. The lesson computes both: `M = T · Rz · S` sends P to (0, 7, 0) while `S · Rz · T` sends it to (−10, 1, 0). Matrix multiplication is not commutative except in special cases.

</details>

**Q2.** In the worked example, `T · Rz · S` sends (1, 0, 0) to (0, 7, 0) but `S · Rz · T` sends the same point to (−10, 1, 0). What specifically went wrong in the second case?

- A) The scale was applied to the wrong coordinates
- B) The translation happened first, so it was then rotated and scaled along with the point
- C) The rotation direction was reversed
- D) The 3×3 blocks should have been transposed before multiplying

<details>
<summary>Answer and explanation</summary>

**B) The translation happened first, so it was then rotated and scaled along with the point.**

Trace it: T·P = (1, 5, 0, 1); then Rz turns that into (−5, 1, 0, 1); then S doubles the x component to give (−10, 1, 0, 1). The offset (0, 5, 0) that T contributed was rotated into (−5, 0, 0) and then scaled to (−10, 0, 0). You can see the same thing in the translation column of the composed matrix: for `T · Rz · S` it is (0, 5, 0), the offset untouched, while for `S · Rz · T` it becomes (−10, 0, 0). Whatever transform sits to the left of the translation also acts on the translation.

A) is wrong because the scale was applied to all three coordinates correctly. (5, 5, 0) is not what happened; (1, 5, 0) went in and only its x component got doubled at the end.

C) is wrong because Rz appears in the same position in both products and its internal sign pattern is untouched. A reversed rotation would give a different error — the point would land in the fourth quadrant instead of the second. Compare the printed values: −10 is the *translation's* contribution doubled, not a mis-rotated point.

D) is wrong because transposing would make the matrices orthogonal (preserving lengths and angles), which is the opposite of what you want from a scale. `S · Rz · T` is already a perfectly valid matrix product; it just describes a different transformation.

</details>

**Q3.** For the composition `M = T · R · S`, the translation column of `M` is `R S t`, not `t`. Why must that be?

- A) It is an approximation that happens to be good enough for small rotations
- B) Because `(A · T)` applies A's linear block to t, so anything left of T also transforms the offset
- C) Because matrix multiplication always changes the last column
- D) Because the last column of a 4×4 matrix is always its normal vector

<details>
<summary>Answer and explanation</summary>

**B) Because `(A · T)` applies A's linear block to t, so anything left of T also transforms the offset.**

Write `T` as the block matrix `[[I, t], [0, 1]]`. Then for any 4×4 `A = [[L, u], [0, 1]]`, the product `A · T` is `[[L, L t + u], [0, 1]]`. The offset column becomes `L t + u` — A's linear block applied to t, plus A's own offset. With `A = R · S` the linear block is `R S`, so the column is `R S t`. It is exact algebra, not an approximation.

A) is wrong because the error is not small. In the worked example the raw offset (0, 5, 0) becomes a completely different vector once rotated; in the un-rotated case Exercise 1's forward composition turns the offset (3, 0, 1) into (6, 0, 2), a doubling, not a rounding error.

C) is wrong because multiplication leaves a column alone whenever the *right* factor has a zero there. S and R both have a zero column 3, so the offset in `T · R · S` comes entirely from T's own column 3 and is then transformed by the two factors to T's left. The column is not universally changed; it is changed by exactly the factors to the left of the translation, which is option B restated.

D) is wrong because there is no such relationship in a 4×4. In a *3×3* rotation matrix the last column happens to be a normal direction, and that is how the lesson's Rodrigues check works — but a 4×4's last column is the translation, and it is not required to be perpendicular to anything.

</details>

**Q4.** In a scene graph a parent node has transform `P` and a child node has transform `C`. What is the correct world matrix, and is it equal to `C · P`?

- A) `C · P` — apply the child first, then the parent
- B) `P · C` — the child's local-to-parent transform happens first, then the parent's
- C) `P · C`, because matrix multiplication is commutative
- D) `Pᵀ · Cᵀ` — because transforms are stored transposed for column vectors

<details>
<summary>Answer and explanation</summary>

**B) `P · C` — the child's local-to-parent transform happens first, then the parent's.**

`C` maps the child's own coordinates into its parent's coordinate system; `P` then maps parent coordinates into world coordinates. Chaining them gives `p_world = P(C(p_local)) = (P·C) p_local`. The verified numbers in the composition exercise show this: with `P = T(10,0,0)·Rz(30°)` and `C = Ry(45°)·S(1,2,1)`, the local point (1, 0, 0) becomes (0.707107, 0, −0.707107) after `C` and (10.612372, 0.353553, −0.707107) after `P`, and `(P·C)·q` returns that same value while `(C·P)·q` returns the unrelated (7.68344, 1.0, −7.68344).

A) is the single most common scene-graph bug, and it is silent: no error, just a hierarchy that behaves strangely, with children apparently ignoring their parents' rotations.

C) is false in general. `P · C == C · P` printed `False` for those matrices, and the printed translation columns differ too — (10, 0, 0, 1) versus (7.071068, 0, −7.071068, 1). Commutativity holds only for commuting pairs such as two rotations about the *same* axis, which is not something you can rely on in a general hierarchy.

D) is wrong because `Pᵀ·Cᵀ` is `(C·P)ᵀ`, i.e. the same product in the wrong order again. Transposing does not fix an ordering error; it converts one into a different one. (Transposing *everything* and switching to row vectors does preserve the meaning — that is the `row-vector form matches: True` line — but changing one matrix is not a fix.)

</details>

**Q5.** Which entry of the perspective matrix is responsible for making perspective happen, and what would break without it?

- A) The `(0,0)` entry $1/(a\tan(\theta/2))$ — without it there is no field of view
- B) The `(3,2)` entry, −1 — it makes `w_clip = −z_eye`, so the later division by w shrinks distant points
- C) The `(2,3)` entry, `−2fn/(f−n)` — without it the near and far planes stop mapping to ±1
- D) The `(2,2)` entry, `−(f+n)/(f−n)` — without it the depth range collapses

<details>
<summary>Answer and explanation</summary>

**B) The `(3,2)` entry, −1 — it makes `w_clip = −z_eye`, so the later division by w shrinks distant points.**

The last row of `P` is `(0, 0, −1, 0)`, so `w_clip = −z_eye`. Every perspective effect in the pipeline — a distant point occupying fewer pixels, parallel lines converging, the horizon — is that single division `x_ndc = x_clip / w` with `w` growing with distance. Set that entry to 0 and `w_clip` is 0 for every vertex, the NDC is a division by zero, and you get `inf`/`nan` rather than a projection. The pipeline's clip-space output makes it plain: `w = 10.5000` for the nearest vertex and `w = 11.2990` for the farthest of triangle A.

A) is real but it is the *field of view*, not perspective. With `(0,0)` = 0 you would get x_ndc = 0 for every point, i.e. everything collapses onto the vertical centre line — a valid orthographic-style degenerate, not a broken projection.

C) and D) are both necessary for correct *depth*, and you would notice their absence as a depth-buffer bug rather than a geometry bug. Without `(2,3)` the near and far planes would both map to depth 0, so nothing would occlude anything. Without `(2,2)` the same thing happens in a different way. But geometry would still be correct, because x and y never read those entries — which is exactly the signature of a depth bug: right shape, wrong overlap.

</details>

**Q6.** After projection, `w_clip = −z_eye`. What does that tell you about which points are in front of the camera?

- A) Nothing useful; w is an arbitrary scaling factor
- B) `w > 0` exactly when the point is in front of the camera, and it equals the distance along the view axis
- C) `w > 0` exactly when the point is *behind* the camera
- D) `w` is always 1 for points on the near plane and always −1 on the far plane

<details>
<summary>Answer and explanation</summary>

**B) `w > 0` exactly when the point is in front of the camera, and it equals the distance along the view axis.**

The camera looks down −z, so a point in front has `z_eye < 0`, and `w = −z_eye > 0`. The printed clip-space rows confirm the sign and the size together: triangle A's vertices have `w = 10.5000, 9.5000, 11.2990` — all positive, all equal to the negated eye-space z printed immediately above them (10.5, 9.5, 11.299). Triangle B's first vertex has eye-space z = +1.0 and `w = -1.0000`, negative, because it sits behind the camera.

A) is wrong because w is not free. It is fixed by the last row of `P`, so it carries real information — it is exactly the depth you would want to sort by.

C) inverts the sign. The lesson's pipeline makes the cost of getting this backwards vivid: dividing by that `w = -1.0000` throws the vertex to infinity and flips the triangle through the screen, which is the reason the seven `w >= 0` clip planes exist.

D) confuses w with normalised depth. The near plane has `w = n = 1` here, but the far plane has `w = f = 100`, not −1. The ±1 values are what z *becomes after* dividing by w — that is, NDC depth, a different quantity from w.

</details>

**Q7.** The near plane maps to NDC z = −1 and the far plane to NDC z = +1. What does that imply about the depth buffer test?

- A) Use `GREATER`, because larger depth means closer
- B) Use `LESS`, because depth increases with distance and the fragment drawn earlier should be the nearer one
- C) Use `EQUAL`, since each pixel has exactly one correct depth
- D) The mapping is irrelevant; the depth test only cares that values stay in [−1, 1]

<details>
<summary>Answer and explanation</summary>

**B) Use `LESS`, because depth increases with distance and the fragment drawn earlier should be the nearer one.**

With the near plane at −1 and the far plane at +1, a point further from the camera has a *larger* depth. So the fragment you want to keep — the nearer one — has the smaller value, and you keep it when the incoming depth is `LESS` than the stored one. This is why the default comparison in nearly every graphics API is `GL_LESS` / `D3D11_COMPARISON_LESS`, and why the lesson's triangle A shows depths spread across a real range (0.8075, 0.8278, 0.8414) rather than all equal.

A) is the trap: `GREATER` looks like the natural choice if you think of NDC z as a "closeness" score where bigger means nearer. It is exactly backwards here, and it produces inverted occlusion — near objects hidden behind far ones — which is easy to misdiagnose as a geometry bug.

C) is wrong because a single pixel is covered by many fragments along the view ray, and the whole point of a depth buffer is to resolve that. `EQUAL` would keep only exact ties, which almost never occur, and would leave z-fighting everywhere. (The classic related mistake is `LEQUAL` or a reversed winding producing *exactly* this symptom: shimmering, speckled surfaces where two nearly-coplanar triangles fight.)

D) understates the requirement. Staying in [−1, 1] is what makes the value storable in a normalised fixed-point buffer, but the *ordering* is what the comparison function is for, and the mapping to ±1 is precisely what fixes that ordering as "increasing with distance".

</details>

**Q8.** Why must clipping happen in homogeneous space *before* dividing by w?

- A) Because division is slow, and clipping after dividing is an optimisation
- B) Because dividing by a negative or zero w throws vertices to infinity and mirrors the geometry, so the seven planes −w ≤ x, y, z ≤ w and w ≥ 0 must remove them first
- C) Because clipped vertices would otherwise have undefined normals
- D) Because the NDC range is [0, 1] rather than [−1, 1]

<details>
<summary>Answer and explanation</summary>

**B) Because dividing by a negative or zero w throws vertices to infinity and mirrors the geometry, so the seven planes −w ≤ x, y, z ≤ w and w ≥ 0 must remove them first.**

The frustum's side walls are planes *through the origin* in homogeneous coordinates, of the form `x = w` and `x = −w`. Those are not representable after dividing by w, where they collapse to `x = ±1` and the geometry has already been mirrored by any vertex with `w < 0`. Triangle B is the demonstration: its first vertex has `w = -1.0000`, and clipping it produces six output vertices from three inputs — `after clipping: 6 vertices (input had 3)` — with every survivor's ndc x and y inside [−1, 1] and pixels on the viewport edges.

A) is wrong on the numbers: division by w happens exactly once per vertex per coordinate in the whole pipeline, which is not a bottleneck. And the ordering is a correctness requirement, not a performance choice.

C) is wrong because clipping happens on positions, before any shading, and the vertex shader does not compute lighting normals at all. Sutherland–Hodgman interpolates positions and the barycentric weight; normals come afterwards.

D) is wrong twice over. NDC is [−1, 1] in **both** x and y; [0, 1] is the *pixel* range and the Vulkan-style clip-volume convention, not what this pipeline uses. And in either convention, clipping still has to precede the divide for the same reason.

</details>

**Q9.** In the numpy section, `VP @ p` transforms a column point. Which of these is the identical computation written the other way?

- A) `p @ VP`
- B) `p @ VP.T`
- C) `VP.T @ p`
- D) `transpose(VP) @ transpose(p)`

<details>
<summary>Answer and explanation</summary>

**B) `p @ VP.T`.**

For column vectors `VP @ p` computes $\mathbf{VP}\,\mathbf{p}$. Taking transposes of both sides gives $\mathbf{p}^{T}\mathbf{VP}^{T}$, which is exactly `p @ VP.T`. The lesson verifies it: `row-vector form matches: True` comes from `np.allclose(pts @ VP.T, clip)`.

A) is wrong because `p @ VP` computes $\mathbf{p}^{T}\mathbf{VP}$, which is the product with the factors in the opposite order — the same class of bug as Q1 and Q4. Nothing crashes; you get a silently different (in general non-sensical) transform.

C) is wrong for the same reason: transposing only one of the two operands gives $\mathbf{VP}^{T}\mathbf{p}$, which reverses which factor acts first.

D) is wrong because transposing both a matrix and a vector on the left-hand side does not recover the original. $\mathbf{VP}^{T}\mathbf{p}^{T}$ has mismatched orientation and is not even a well-formed product of the two; the rule that works is transposing both sides of an equation, which here means putting the transposes in *reversed* order.

</details>

**Q10.** Why do normals transform by the inverse transpose rather than by the model matrix?

- A) Because normals are stored as rows rather than columns
- B) Because a non-uniform scale does not preserve perpendicularity; the inverse transpose is the unique linear map that keeps normals orthogonal to transformed tangents
- C) Because the model matrix may contain rounding error and the inverse corrects it
- D) Because normals must be unit length and only the inverse transpose guarantees that

<details>
<summary>Answer and explanation</summary>

**B) Because a non-uniform scale does not preserve perpendicularity; the inverse transpose is the unique linear map that keeps normals orthogonal to transformed tangents.**

If **t** and **n** are perpendicular then $\mathbf{t}^{T}\mathbf{n}=0$, and under a linear map $\mathbf{L}$ we want $(\mathbf{L}\mathbf{t})^{T}\mathbf{n}' = 0$. Writing $\mathbf{n}' = \mathbf{A}\mathbf{n}$ and expanding gives $\mathbf{t}^{T}\mathbf{L}^{T}\mathbf{A}\mathbf{n} = 0$ whenever $\mathbf{t}\perp\mathbf{n}$, which holds for **all** such **t** exactly when $\mathbf{L}^{T}\mathbf{A} = \mathbf{I}$, i.e. $\mathbf{A} = \mathbf{L}^{-T}$. The exercise demonstrates the failure numerically: with `scale(2, 3, 4)` and the oblique normal (1,1,1)/√3, the point-transformed normal gives `t'.wrong = -2.041241` where the inverse transpose gives `t'.right = 0.0`.

A) is wrong because normals are columns everywhere in this pipeline, exactly like positions. The distinction is which *matrix* is applied, not which orientation the vector is stored in.

C) is wrong because the inverse transpose is not a numerical correction — it is exact, and it is *worse* than the model matrix numerically, since it requires an inversion. Rounding is a separate concern; the lesson keeps the exercise's `abs(norm(right) - closed_form) < 1e-12` check purely as a verification.

D) is wrong because neither transform guarantees unit length. The exercise prints `|wrong| = 3.109126` and `|right| = 0.375771` for a unit input normal — neither is 1. What the inverse transpose guarantees is perpendicularity; unit length comes from normalising afterwards, which is exactly why shaders do it and why normalising hides the length half of the bug while never hiding the direction half.

</details>

**Q11.** You call a rotation helper with axis `(1, 1, 0)` and θ = 90°. The result has determinant 4.0 and moves the point (1, 0, 0) to (1, 1, −1). What did you forget?

- A) To negate the angle, so the rotation goes the other way
- B) To normalise the axis; Rodrigues' formula assumes ‖u‖ = 1, and without it the matrix is a rotation *plus* a uniform scaling
- C) To transpose the matrix, because column vectors need it
- D) To use the 4×4 form rather than the 3×3 form

<details>
<summary>Answer and explanation</summary>

**B) To normalise the axis; Rodrigues' formula assumes ‖u‖ = 1, and without it the matrix is a rotation *plus* a uniform scaling.**

‖(1, 1, 0)‖ = √2, and the resulting matrix is 2× the intended rotation, so `det = 2³ = 4.0` and the point (1, 0, 0) lands at (1, 1, −1) with length √3 instead of staying at length 1. That is not a rotation any more: `max |RᵀR − I| = 2.0`. The lesson's `rotation_about_axis` calls `normalise(axis)` first and prints `(0.7071067811865476, 0.7071067811865476, 0.0)` alongside the raw input, and the correct result has determinant 1.0 with the point at length exactly 1.0.

A) is wrong because negating θ gives the transposed rotation — still determinant +1 and still length-preserving. A determinant of 4 is a scaling fingerprint, and a mirrored rotation would give −1.

C) is wrong because transposing an *orthogonal* matrix inverts it, which has determinant 1 too. The 3×3-versus-4×4 distinction is a shape issue, not a magnitude issue.

D) is wrong because the lesson's helper already returns a 4×4 with a unit bottom row, and the 3×3 helper form has the same problem. The bug is the magnitude of the axis, not the size of the matrix.

</details>

**Q12.** A point at eye-space (0, +2, −10) maps to pixel y = 196.077 on a 600-pixel-tall image. Why is the mapping `y_screen = (1 − y_ndc)/2 · height` rather than `(y_ndc + 1)/2 · height`?

- A) Because y_ndc has the opposite sign convention to x_ndc
- B) Because image row 0 is the top of the picture while +y in graphics space points up
- C) Because a scale factor of 1/2 is needed on y but not on x
- D) Because the aspect ratio has to be divided out of the y coordinate

<details>
<summary>Answer and explanation</summary>

**B) Because image row 0 is the top of the picture while +y in graphics space points up.**

Pixel coordinates increase *downward*; world/eye coordinates increase upward. So a point above the centre, with `y_ndc = +0.346410162`, must land in the *upper* half of the buffer, which is small row numbers. `(1 − y_ndc)/2 · 600` gives 196.077, and the symmetric point (0, −2, −10) gives 403.923 — the two are exact reflections about the image centre row 300, which is the behaviour you want. `(y_ndc + 1)/2 · 600` would put the point above the axis at row 403.9, i.e. below the centre, rendering the whole scene vertically mirrored.

A) is wrong because x and y use the *same* sign convention in NDC; both run from −1 to +1 over the viewport. Only the mapping out of NDC differs between the axes.

C) is wrong because the 1/2 and the +1 appear symmetrically in both axes; there is no asymmetry in the normalisation. The only asymmetry is the `1 −` instead of `+`.

D) is wrong because the aspect ratio has already been baked into the projection matrix's `(0,0)` entry as $1/(a\tan(\theta/2))$. Dividing it out again at the viewport stage would undo the horizontal stretch and give the wrong picture.

</details>

## Subjective Questions

### Short Answer

**Q1. State the composition-order rule for column vectors, and write the standard object transform in terms of scale, rotation and translation.**

<details>
<summary>Answer</summary>

With column vectors, `M = A · B` applies **B** first and then **A** — read the product right to left.

So "scale, then rotate, then place in the world" is

$$\mathbf{M} = \mathbf{T}\cdot\mathbf{R}\cdot\mathbf{S}$$

with the scale innermost (rightmost) and the translation outermost (leftmost). The reversal `S · R · T` means scale first, then rotate, then move, which scales and rotates the translation too.

</details>

**Q2. Write the perspective projection matrix and name what each of its four non-zero rows does.**

<details>
<summary>Answer</summary>

$$
\mathbf{P} = \begin{pmatrix}
\frac{1}{a\tan(\theta/2)} & 0 & 0 & 0\\
0 & \frac{1}{\tan(\theta/2)} & 0 & 0\\
0 & 0 & -\frac{f+n}{f-n} & -\frac{2fn}{f-n}\\
0 & 0 & -1 & 0
\end{pmatrix}
$$

- Row 0: horizontal scale $1/(a\tan(\theta/2))$ — maps the horizontal half-extent onto $x_{\text{clip}}$.
- Row 1: vertical scale $1/\tan(\theta/2)$ — maps the vertical half-extent onto $y_{\text{clip}}$.
- Row 2: the depth map, taking $z_{\text{eye}} = -n$ to −1 and $z_{\text{eye}} = -f$ to +1.
- Row 3: `w_clip = −z_eye`, the entry that makes the divide by w produce perspective.

Restrictions: $0 < n < f$ and $\theta > 0$.

</details>

**Q3. What does `look_at` do, and what two inputs must its caller get right?**

<details>
<summary>Answer</summary>

It builds the transform that maps world coordinates into camera space, leaving the camera at the origin looking down the −z axis. It normalises `target − eye` into the forward vector, negates it to get the camera's own z axis, crosses that with `up` to get x, crosses again for y, puts x, y, z in the *rows* (transposing inverts the rotation), and sets the translation column to $-(R\,\text{eye})$.

Two caller obligations:

- `up` must not be parallel to the view direction, or `up × z` is zero and normalising it divides by zero. The lesson's `look_at` raises `ValueError` in that case.
- `eye` and `target` must differ, for the same reason: a zero-length forward vector cannot be normalised.

</details>

**Q4. Give the two cheap numerical tests that certify a model or view matrix is a rigid transform, and explain what each rules out.**

<details>
<summary>Answer</summary>

$\mathbf{R}\mathbf{R}^{T} = \mathbf{I}$ to within rounding, and $\det(\mathbf{R}) = +1$.

The first rules out scaling, shearing and any non-orthogonal distortion: orthonormal rows preserve lengths and angles exactly. The second rules out mirroring — a reflection is orthogonal but has determinant −1, so it satisfies the first test and fails the second.

Together they say "rotated, not resized, not flipped", which for a model or view matrix is exactly the contract. A single `det(R) = 1.0` assertion is the cheap version most engines keep in debug builds.

</details>

**Q5. What is the normal transform, when is it needed, and what does it simplify to for a rigid transform?**

<details>
<summary>Answer</summary>

$\mathbf{n}' = (\mathbf{M}^{-1})^{T}\mathbf{n}$, using the 3×3 linear block of **M**.

It is needed whenever the transform is not a rigid motion — that is, under non-uniform scale, and also under shear. Under uniform scale and pure rotation, transforming a normal like a point happens to be correct up to a constant factor, which normalisation hides. That hiding is exactly why the bug survives in engines that normalise.

For a pure rotation $\mathbf{R}$ with $\mathbf{R}^{-1} = \mathbf{R}^{T}$, so $(\mathbf{R}^{-1})^{T} = \mathbf{R}^{T}$: the inverse transpose is just the transpose, and no inversion is needed. Requiring $\mathbf{M}$ invertible means no zero scale factor.

</details>

### Long Answer

**Q1. Why does the order of matrix factors matter so much, and how do you actually remember the right one?**

<details>
<summary>Model answer</summary>

Matrix multiplication is not commutative, and the pipeline depends on that. With column vectors, `M = A · B` applies B first and then A, because $(AB)\mathbf{p} = A(B\mathbf{p})$. The order is therefore not a detail of notation — it selects a genuinely different transformation out of the same ingredients. The lesson's worked example makes the stakes concrete: `T · Rz · S` sends (1, 0, 0) to (0, 7, 0), while `S · Rz · T` sends the *same* point to (−10, 1, 0). Different point, and no exception, no warning, no crash.

Why it bites is that both orders are *plausible*. `S · Rz · T` is not nonsense; it is a coherent description of a different scene, where the object is scaled in its own frame, then rotated in its own frame, and only then placed. It renders. It just renders the wrong thing. And the error is largest exactly where it is easiest to miss: the translation column. For `T · R · S` the column is `R S t`; for `S · R · T` it is `t` run through the other two transforms. In the worked example the offset (0, 5, 0) becomes (−10, 0, 0) — the object is not where you asked, and there is no number in the output that says so.

**How to remember it.** There are three devices, and the reliable one is the third.

*Read right to left.* The rightmost factor is closest to the point, so it happens first. This is not a mnemonic to memorise but a consequence of associativity, and it generalises: in `VP = P · V · M` the model transform is rightmost and therefore first, which is exactly the order a vertex goes through — object, camera, lens.

*The story test.* Ask what the sentence "scale, then rotate, then translate" would have to look like as a product. The rightmost factor is the first thing the point meets, so scale goes rightmost, and the phrase comes out in order as you read left to right: `T · R · S`. If the order is wrong, the sentence comes out backwards — which is a much more noticeable symptom than a wrong number.

*The translation test, which is the one to actually use in review.* Whatever sits to the **left** of the translation also transforms the translation. So read off column 3 of your composed matrix and compare it with the offset you intended. In Exercise 1's forward composition the offset (3, 0, 1) becomes (6, 0, 2) — scaled, because the scale is to the left of the translation, which is correct and expected: world units are absolute, so a world offset should not be scaled. In the reverse composition the same offset becomes (1, 0, −3): merely rotated into the object's frame, no longer a world position, which is the tell. One comparison catches the whole class of bug, works when the rotation is not axis-aligned, and needs no mental arithmetic.

Two corollaries worth internalising. First, the rule is about *position* in the product, not about the *type* of the factor — "put translation on the left" is a statement about multiplication order, not about matrices, and the derivation `(A·T)` has offset column $A_{3\times3}\mathbf{t} + A_{\text{offset}}$ makes that explicit. Second, the convention is arbitrary and you may switch it, but you must switch it *everywhere*. `p_row @ M` and `M @ p_col` describe the same computation only if you also transpose one of them; a codebase that mixes `M @ p` with `p @ M` in different files produces a scene that is subtly, placidly wrong. Pick the column convention the API uses and write a one-line wrapper that takes a matrix, so the order never appears in calling code at all.

</details>

**Q2. Why does the pipeline divide by w at all — what does the fourth coordinate buy that a 3×3 matrix could not — and what would break if you skipped it?**

<details>
<summary>Model answer</summary>

The divide is what makes distant objects smaller, and the fourth coordinate is what makes the divide possible as a *matrix* rather than a separate pass.

Start from the problem. A pinhole camera's projection is genuinely non-linear: the image of a world point depends on its distance. You can see this in the exercise's own numbers — a point one unit to the right at eye-space z = −10 has `x_ndc = +0.129903811`, and the same one unit at z = −5 has `x_ndc = +0.259807621`. Exactly twice the distance, exactly half the image offset. A 3×3 linear map cannot produce that: linearity forces `f(λx) = λf(x)`, and the halving is not a scaling.

The trick is to smuggle the reciprocal distance through as a *coordinate*. Set the fourth coordinate to the distance, $w = -z_{\text{eye}}$, and let the matrix compute an ordinary linear map into clip space. The perspective is then recovered by a single division of all four coordinates by the fourth. So the division is not an optional flourish — it is the nonlinear step, and it has been moved from "impossible in a matrix" to "one divide at the end of the pipeline".

What the slack coordinate buys beyond that is the ability to compose. Because the fourth coordinate is carried along, a translation can be written as a matrix and multiplied in. Under the projection matrix the bottom row is `(0, 0, −1, 0)`, so clip-space w is a genuine function of z and every transform upstream leaves it at 1; the perspective divide then happens once, after everything. A pipeline without a fourth coordinate needs a separate `position = R·position + t` step at every stage, which is precisely what makes naive implementations slow and what the homogeneous form removes.

Now, what breaks if you skip the divide. Geometry: `x_clip` and `y_clip` are then raw eye coordinates with no image projection at all, and you get an isometric wireframe rather than a picture. Sanity check with the lesson's triangle A — without the divide, `x_clip` values are 0.8350, −1.2793, −1.1377 against `w` values of 10.5, 9.5, 11.2990. Dividing gives x_ndc 0.079524, −0.134663, −0.100687, i.e. a triangle clustered around the centre of the screen. Not dividing leaves x values of order 1 *because w happens to be of order 10*, so the "image" would be an accidental narrow sliver whose shape depends on how far away the object is. Depth breaks too: z_ndc would be the raw `z_clip = 8.6919, 7.6717, 9.5071`, which are all > 1, entirely outside the [−1, 1] clip volume, so the depth buffer would read garbage.

The subtler failure is the one that bites hardest. Dividing by a **negative** w does not fail loudly — it mirrors. Triangle B's first vertex sits behind the camera at eye-space z = +1.0, giving `w = -1.0000`. Dividing by −1 flips that vertex's x and y through the origin, so the triangle appears to wrap around and behind the camera, producing enormous stretched geometry across the whole viewport. That is why the pipeline clips first against seven planes, −w ≤ x, y, z ≤ w together with w ≥ 0: the side walls are equations of the form x = w, which are representable in homogeneous coordinates but collapse to x = ±1 after the divide, so they must be enforced while w is still around. The clipper turning 3 vertices into 6 for triangle B, all inside [−1, 1], is that stage doing its job.

A useful way to hold all this together: w is the *only* place in the pipeline where non-linearity lives. Everything upstream of the divide is an affine map, which is why matrices compose so cleanly and why a whole hierarchy of transforms collapses into one 4×4 `VP` that can be inverted in a single call for picking. Break the divide and you lose perspective, depth, and the ability to clip correctly — in that order of visibility.

</details>

**Q3. Why is `w_clip = −z_eye` such a useful property, and how does it interact with clipping, the depth test and ray picking all at once?**

<details>
<summary>Model answer</summary>

Because it makes the fourth coordinate *mean* something. In most matrix pipelines w is an opaque by-product that you divide by and forget. Here it is exactly the distance in front of the camera, measured along the view axis, and that single identity ties three separate parts of the pipeline together.

**It produces perspective for free.** Every entry of the projection matrix is linear; the only nonlinearity in the whole transform is `x_ndc = x_clip / (−z_eye)`. So an object twice as far away comes out with half the image offset, with no special case in the matrix. The pipeline's own output shows it: triangle A's three vertices sit at depths 0.8075, 0.8278 and 0.8414 — a 0.034 spread for an object about 10 units from a camera whose far plane is 100. That is the whole of perspective, and it came from one row of numbers.

**It tells you which vertices are in front.** Since `w > 0` exactly when `z_eye < 0`, the sign of w is a free behind-the-camera test. Triangle B's first vertex has eye-space z = +1.0 and `w = -1.0000`; that single sign is what the clipper's `w >= 0` plane keys on, and it is why you do not need a separate "is this behind the camera" branch. It is also why the depth comparison must be `LESS` rather than `GREATER`: depth increases with distance because w does.

**It gives you the pick ray for free.** To turn a pixel into a world ray you unproject at the two depth extremes, `z_ndc = −1` and `z_ndc = +1`, and divide the resulting homogeneous point by w to get real coordinates. Those two points are the endpoints of the click ray. And because w equals distance, they are *exactly* the points at distance n and f along the ray — nothing is approximate and nothing needs a separate camera-space construction. In the picking exercise the near point comes back at z = 9.125 for a camera at z = 10 (distance 0.875, inside the near plane because the camera is tilted down) and the far point at z = −77.49, and the floor intersection of that ray lands at (2.047891, 0, 5.345154), which re-projects to pixel (600.0000, 450.0000) exactly.

The consequences of *not* having this property are worth knowing too, because they explain the design. Suppose instead that w came out as `z_eye` with the wrong sign, or as a constant 1. With w = 1 you lose perspective and are left with an orthographic projection — which is a legitimate choice for CAD, and is why some pipelines genuinely do normalise w away, but it is not perspective. With the wrong sign, every vertex in front of the camera would have negative w, the near-plane clipping test would invert, and half the scene would be culled.

One practical caveat that the identity creates: because the near-plane maps to NDC z = −1 and the far plane to +1, depth precision is not uniform. The mapping is $z_{ndc} = \frac{(f+n)z_{eye} + 2fn}{(f-n)(-z_{eye})}$, which changes fastest near the near plane, so with near = 1 and far = 100 the depth buffer's resolution is concentrated in the first few units. This is Common Mistake 5's point: keep near and far close to the actual scene, because a huge ratio is where depth fighting and "every fragment reads depth 1.0" come from. The identity `w = −z_eye` does not cause that, but it is the reason the ratio is the knob that matters.

</details>

**Q4. A model looks correctly shaped but its lighting is subtly wrong — flat faces look evenly lit and curved faces look banded. What is the most likely cause, why is the symptom so deceptive, and how would you confirm it in one line of code?**

<details>
<summary>Model answer</summary>

The most likely cause is that normals are being transformed with the model matrix instead of its inverse transpose, which is wrong the moment the transform is not a rigid motion — in practice, as soon as there is any non-uniform scale.

The reason is geometric. A normal is not a position; it is a direction constrained to be perpendicular to the surface. Under a uniform scale, scaling a normal by the same factor as a position keeps the perpendicular relationship, which is why uniform scale and pure rotation hide the bug completely. Under non-uniform scale, the surface is stretched by different amounts in different directions, and the true new normal tilts *further* from the stretched axis, not closer — it is divided by the scale factor, not multiplied. The exercise shows exactly this: for `scale(2, 3, 4)` and the oblique normal (1, 1, 1)/√3, the correct transform gives components n/2, n/3, n/4 and a length of 0.375771, matching the closed form √(1/4 + 1/9 + 1/16)/√3 to twelve places, while transforming the normal like a point gives a length of 3.109126 in roughly the wrong direction.

The symptom is deceptive for two separate reasons, and each one has cost somebody a day.

First, the *direction* is wrong, not just the length, and direction is what lighting uses. Blinn–Phong and Lambert both compute a dot product between the normal and a light direction; feeding in a normal pointing the wrong way does not produce an obviously broken image, it produces one that is merely dull in the wrong places. Banding on curved surfaces is the signature: a sphere under non-uniform scale has a smoothly varying true normal, and a wrongly-transformed normal varies smoothly too, so the terminator lands in the wrong place and quantises into visible rings.

Second, and worse, many engines normalise normals in the fragment shader. That repairs the length, so the remaining error is only a direction error — and a direction error is invisible to any test that checks `length(normal) == 1`. Which is why the lesson's first attempt at this demonstration, with an axis-aligned normal, hides the bug: `(0, 1, 0)` under any diagonal scale comes out unchanged, so both transforms look identical. The difference only appears once the normal is oblique.

**The one-line confirmation.** Transform a normal and a tangent that are perpendicular to each other, then check that they are *still* perpendicular afterwards:

```
t' = L · t          # tangent, transformed as a point -- this is correct
n' = (L⁻¹)ᵀ · n     # normal, inverse transpose -- this is correct
dot(t', n')         # 0.0 exactly
```

Run it with the model matrix for `n'` instead and you get the exercise's `t'.wrong = -2.041241` where the correct version prints `0.0`. A nonzero value is proof, not a hint.

The fix, once confirmed: build the normal matrix as `transpose(inverse(M[:3, :3]))` once per frame per object rather than per vertex, and cache it — the inverse is the expensive part and it is the same for every vertex of an object. If you know the object is rigid (rotation and translation only, no scale), skip the inverse entirely and use `M[:3, :3].T`, since $(\mathbf{R}^{-1})^{T} = \mathbf{R}^{T}$ for a rotation. And if you apply scale on the CPU before uploading, apply the *same* scale to the normals there and you never need the normal matrix at all — which is why a lot of asset pipelines work correctly and a lot of runtime-scaled hierarchies do not.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — ** Compose a transform that rotates a point 90° about the
y axis, translates it by (3, 0, 1), then scales it by 2 uniformly. Apply it to
P = (1, 0, 0) stage by stage. Then compose the reverse order and use the
translation column of each composed matrix to explain exactly how they differ.

<details>
<summary>Solution</summary>

With column vectors, "rotate, then translate, then scale" is `M = S · T · R`,
because the rightmost factor acts first.

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
R, T, S = rotate_y(HALF_PI), translate(3.0, 0.0, 1.0), scale(2.0, 2.0, 2.0)

p = [1.0, 0.0, 0.0, 1.0]
print("start          =", p[:3])
r = apply(R, p)
print("after rotate   =", [round(v, 6) for v in r[:3]])
t = apply(T, r)
print("after translate=", [round(v, 6) for v in t[:3]])
s = apply(S, t)
print("after scale    =", [round(v, 6) for v in s[:3]])

M = matmul(S, matmul(T, R))
print("one-shot matches stages:", all(abs(a - b) < 1e-12 for a, b in zip(apply(M, p), s)))

W = matmul(R, matmul(T, S))   # reverse: scale, then translate, then rotate
print("\nforward S*T*R  ->", [round(v, 6) for v in apply(M, p)[:3]])
print("reverse R*T*S  ->", [round(v, 6) for v in apply(W, p)[:3]])
print("\ntranslation column, forward =", [round(v, 6) for v in (M[0][3], M[1][3], M[2][3])])
print("translation column, reverse =", [round(v, 6) for v in (W[0][3], W[1][3], W[2][3])])
```

Output:

```
start          = [1.0, 0.0, 0.0]
after rotate   = [0.0, 0.0, -1.0]
after translate= [3.0, 0.0, 0.0]
after scale    = [6.0, 0.0, 0.0]
one-shot matches stages: True

forward S*T*R  -> [6.0, 0.0, 0.0]
reverse R*T*S  -> [1.0, 0.0, -5.0]

translation column, forward = [6.0, 0.0, 2.0]
translation column, reverse = [1.0, 0.0, -3.0]
```

Forward, as a story: the point starts on the x axis, rotating 90° about y sweeps
it onto the −z axis at (0, 0, −1), translating adds (3, 0, 1) giving (3, 0, 0),
and scaling by 2 gives **(6, 0, 0)**. In reverse the scale happens first, so the
point doubles to (2, 0, 0), translates to (5, 0, 1), and rotates to **(1, 0, −5)**.

The translation columns say why without touching the point at all. The object's
own offset is (3, 0, 1). Forward, the translation is applied last, so the scale
also acts on it: (6, 0, 2). Reverse, the translation comes before the scale, so
it is merely rotated into the object's frame: (1, 0, −3).

**The rule: whatever sits to the left of the translation gets applied to the
translation too.** Put the translation innermost when you mean "move this object
to this world position".

</details>

**[ ] Exercise 2 — ** Show numerically that the inverse transpose, not the model
matrix, is the correct normal transform. Use a non-uniform scale of (2, 3, 4),
an oblique unit normal, and a tangent perpendicular to it. Show that
transforming the normal like a point breaks perpendicularity while the inverse
transpose preserves it, and check the correct normal's length against a closed
form.

<details>
<summary>Solution</summary>

```python
from math import sqrt

def scale(sx, sy, sz):
    return [[sx, 0.0, 0.0, 0.0], [0.0, sy, 0.0, 0.0],
            [0.0, 0.0, sz, 0.0], [0.0, 0.0, 0.0, 1.0]]

def transpose(a):
    return [list(r) for r in zip(*a)]

def invert_3x3(m):
    """Inverse of a 3x3 block via the adjugate and one determinant."""
    a, b, c = m[0][0], m[0][1], m[0][2]
    d, e, f = m[1][0], m[1][1], m[1][2]
    g, h, i = m[2][0], m[2][1], m[2][2]
    det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    return [[(e * i - f * h) / det, (c * h - b * i) / det, (b * f - c * e) / det],
            [(f * g - d * i) / det, (a * i - c * g) / det, (c * d - a * f) / det],
            [(d * h - e * g) / det, (b * g - a * h) / det, (a * e - b * d) / det]]

def mv(m, v):
    return [sum(m[i][k] * v[k] for k in range(3)) for i in range(3)]

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def norm(v):
    return sqrt(dot(v, v))

S = scale(2.0, 3.0, 4.0)
L = [row[:3] for row in S[:3]]       # the linear 3x3 part
inv_T = transpose(invert_3x3(L))    # (L^-1)^T, the correct normal matrix

# Oblique normal and a perpendicular tangent -- axis-aligned ones hide the bug.
n = [0.5773502691896258] * 3          # (1,1,1)/sqrt(3)
t = [0.7071067811865476, -0.7071067811865476, 0.0]

print("before scaling: t.n =", round(dot(t, n), 12))
t1 = mv(L, t)
wrong = mv(L, n)      # normal transformed like a point: WRONG
right = mv(inv_T, n)  # normal transformed by inverse transpose: RIGHT

print("\ntangent after scale =", t1, "length =", round(norm(t1), 6))
print("wrong normal        =", wrong, "length =", round(norm(wrong), 6))
print("right normal        =", right, "length =", round(norm(right), 6))

print("\nperpendicularity (both should be 0):")
print("  t'.wrong =", round(dot(t1, wrong), 6))
print("  t'.right =", round(dot(t1, right), 6))

closed_form = sqrt(1 / 4 + 1 / 9 + 1 / 16) / sqrt(3)
print("\n|right| =", round(norm(right), 6),
      " closed form =", round(closed_form, 6),
      " match?", abs(norm(right) - closed_form) < 1e-12)
```

Output:

```
before scaling: t.n = 0.0

tangent after scale = [1.4142135623730951, -2.121320343559643, 0.0] length = 2.54951
wrong normal        = [1.1547005383792517, 1.7320508075688776, 2.3094010767585034] length = 3.109126
right normal        = [0.2886751345948129, 0.19245008972987526, 0.14433756729740646] length = 0.375771

perpendicularity (both should be 0):
  t'.wrong = -2.041241
  t'.right = 0.0

|right| = 0.375771  closed form = 0.375771  match? True
```

`t'.wrong = -2.041241` is the bug stated numerically: the scaled tangent and the
"wrong" normal are no longer perpendicular, so every lighting term derived from
that normal is wrong. The inverse transpose gives exactly `0.0`.

The length result explains *why* the inverse transpose is right. The correct
normal's components are n/2, n/3, n/4 — a **division** by the scale factors,
not a multiplication — so its length is √(1/4 + 1/9 + 1/16)/√3 ≈ 0.3758, which
the code confirms. Physically: a surface stretched 4× along z has its normal
tilted 4× further from the z axis. This is also why engines normalise normals in
the shader — that hides the length error but never the direction error.

</details>

**[ ] Exercise 3 — ** A point sits at world P = (0, 0, −5). The camera is at
(0, 0, 10) looking at the origin, up = (0, 1, 0), fov 60°, aspect 4/3, near 1,
far 100. Find the eye-space coordinates, clip coordinates, NDC, and pixel on an
800×600 screen. Verify `w = −z_eye` after projection and check the pixel against
the image centre.

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
        return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2],
                a[0] * b[1] - a[1] * b[0])

    f = sub(target, eye)
    f = tuple(c / sqrt(dot3(f, f)) for c in f)
    z = tuple(-c for c in f)
    x = cross3(up, z)
    x = tuple(c / sqrt(dot3(x, x)) for c in x)
    y = cross3(z, x)
    V = [[x[0], x[1], x[2], 0.0], [y[0], y[1], y[2], 0.0],
         [z[0], z[1], z[2], 0.0], [0.0, 0.0, 0.0, 1.0]]
    t = [-sum(V[i][j] * eye[j] for j in range(3)) for i in range(3)]
    V[0][3], V[1][3], V[2][3] = t
    return V

def perspective(fov_y, aspect, near, far):
    t = 1.0 / tan(fov_y / 2.0)
    return [[t / aspect, 0.0, 0.0, 0.0], [0.0, t, 0.0, 0.0],
            [0.0, 0.0, -(far + near) / (far - near), -2.0 * far * near / (far - near)],
            [0.0, 0.0, -1.0, 0.0]]

def apply(m, v):
    return [sum(m[i][k] * v[k] for k in range(4)) for i in range(4)]

V = look_at((0.0, 0.0, 10.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0))
Pm = perspective(1.0471975511965976, WIDTH / HEIGHT, 1.0, 100.0)

eye = apply(V, [0.0, 0.0, -5.0, 1.0])
print("eye space  =", [round(v, 9) for v in eye[:3]], " w =", eye[3])

# In eye space w is still 1; w = -z_eye only appears after the projection,
# whose last row is (0, 0, -1, 0).
clip = apply(Pm, eye)
print("clip space =", [round(v, 9) for v in clip])
print("check clip w == -z_eye:", abs(clip[3] + eye[2]) < 1e-12)

w = clip[3]
ndc = [c / w for c in clip[:3]]
print("\nndc   =", [round(v, 9) for v in ndc])
px = (ndc[0] + 1) / 2 * WIDTH
py = (1 - ndc[1]) / 2 * HEIGHT
print("pixel =", (round(px, 4), round(py, 4)), " image centre =",
      (WIDTH / 2, HEIGHT / 2))
print("depth =", round(ndc[2], 9), " inside [-1, 1]?", -1.0 <= ndc[2] <= 1.0)
```

Output:

```
eye space  = [0.0, 0.0, -15.0]  w = 1.0
clip space = [0.0, 0.0, 13.282828283, 15.0]
check clip w == -z_eye: True

ndc   = [0.0, 0.0, 0.885521886]
pixel = (400.0, 300.0)  image centre = (400.0, 300.0)
depth = 0.885521886  inside [-1, 1]? True
```

The camera at z = +10 looking towards the origin puts a point at z = −5 fifteen
units in front of it, hence eye-space z = −15 and w = 15.

Check the depth by hand. tan(30°) = 0.57735, so P₀₀ = P₁₁ = 1.73205;
P₂₂ = −101/99 = −1.02020; P₂₃ = −200/99 = −2.02020. Then
z_clip = (−1.02020)(−15) + (−2.02020)(1) = 15.3030 − 2.0202 = 13.2828,
matching the printed value. Divide by 15: 0.88552.

Depth 0.886 rather than something near 0 is correct: the point is 15 units into a
frustum running from 1 to 100, so most of the depth range lies further away. The
pixel lands at exactly (400, 300) because x and y are both zero — a free check
that `look_at` produced a sane basis.

</details>

**Challenge — ** Write frustum culling. Given a world-space bounding sphere
(centre c, radius r) and a view-projection matrix, classify it `inside`,
`outside`, or `intersecting`. Extract the six frustum planes with the
Gribb–Hartmann method, and confirm the near and far planes land where the camera
parameters say they should.

<details>
<summary>Solution</summary>

```python
from math import sqrt, tan

EPS = 1e-12

def matmul(a, b):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)]
            for i in range(n)]

def look_at(eye, target, up):
    def sub(a, b):
        return tuple(x - y for x, y in zip(a, b))
    def dot3(a, b):
        return sum(x * y for x, y in zip(a, b))
    def cross3(a, b):
        return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2],
                a[0] * b[1] - a[1] * b[0])

    f = sub(target, eye)
    f = tuple(c / sqrt(dot3(f, f)) for c in f)
    z = tuple(-c for c in f)
    x = cross3(up, z)
    x = tuple(c / sqrt(dot3(x, x)) for c in x)
    y = cross3(z, x)
    V = [[x[0], x[1], x[2], 0.0], [y[0], y[1], y[2], 0.0],
         [z[0], z[1], z[2], 0.0], [0.0, 0.0, 0.0, 1.0]]
    t = [-sum(V[i][j] * eye[j] for j in range(3)) for i in range(3)]
    V[0][3], V[1][3], V[2][3] = t
    return V

def perspective(fov_y, aspect, near, far):
    t = 1.0 / tan(fov_y / 2.0)
    return [[t / aspect, 0.0, 0.0, 0.0], [0.0, t, 0.0, 0.0],
            [0.0, 0.0, -(far + near) / (far - near), -2.0 * far * near / (far - near)],
            [0.0, 0.0, -1.0, 0.0]]

def build_vp(eye, target=(0.0, 0.0, 0.0)):
    return matmul(perspective(1.0471975511965976, 4.0 / 3.0, 1.0, 100.0),
                  look_at(eye, target, (0.0, 1.0, 0.0)))

def extract_world_planes(vp):
    """Gribb-Hartmann extraction: frustum planes in WORLD space.

    The clip volumes are -w <= x, y, z <= w, which as inequalities in clip
    coordinates c are x+w >= 0, w-x >= 0, and so on -- each is q . c >= 0 for
    a fixed coefficient vector q. Since c = VP . x, substituting gives
    (VP^T . q) . x >= 0, so multiplying each q by VP^T lands the plane in
    world space. No matrix inverse is needed.
    """
    vp_T = [list(r) for r in zip(*vp)]
    names = ["left", "right", "bottom", "top", "near", "far"]
    coefficients = [(1, 0, 0, 1), (-1, 0, 0, 1), (0, 1, 0, 1),
                    (0, -1, 0, 1), (0, 0, 1, 1), (0, 0, -1, 1)]
    planes = []
    for name, q in zip(names, coefficients):
        wp = [sum(vp_T[i][j] * q[j] for j in range(4)) for i in range(4)]
        a, b, c, d = wp
        length = sqrt(a * a + b * b + c * c)
        if length < EPS:
            continue
        planes.append((name, (a / length, b / length, c / length, d / length)))
    return planes

def classify(centre, radius, planes):
    """'inside', 'outside' or 'intersecting' for a world-space sphere.

    With a unit normal, a*x + b*y + c*z + d is a true distance in world units.
    The sphere is wholly outside a plane when that is below -radius.
    """
    outside = 0
    for name, (a, b, c, d) in planes:
        distance = a * centre[0] + b * centre[1] + c * centre[2] + d
        if distance < -radius:
            outside += 1
        elif distance < radius:
            return "intersecting"
    return "outside" if outside else "inside"

planes = extract_world_planes(build_vp((0.0, 0.0, 10.0)))

print("frustum planes in WORLD space (unit normals):")
for name, (a, b, c, d) in planes:
    print(f"  {name:7s} n = ({a:+.4f}, {b:+.4f}, {c:+.4f})  d = {d:+.4f}")

# The near plane should be 1 unit in front of a camera at z = 10, and the far
# plane 100 units in front -- i.e. the planes z = 9 and z = -90.
print("\nnear plane at z =", round(-planes[4][1][3] / planes[4][1][2], 4),
      " far plane at z =", round(-planes[5][1][3] / planes[5][1][2], 4))

print("\nclassifying world-space bounding spheres:")
spheres = [
    ("small ball at the origin", (0.0, 0.0, 0.0), 1.0),
    ("tiny ball at the target", (0.0, 0.0, 0.0), 0.5),
    ("ball behind the camera", (0.0, 0.0, 30.0), 1.0),
    ("ball past the far plane", (0.0, 0.0, -500.0), 1.0),
    ("ball far off to the side", (400.0, 0.0, 0.0), 1.0),
    ("ball straddling near plane", (0.0, 0.0, 9.0), 1.5),
    ("ball just inside near plane", (0.0, 0.0, 8.4), 0.5),
    ("huge ball covering all", (0.0, 0.0, 0.0), 500.0),
]
for label, centre, radius in spheres:
    print(f"  {label:28s} -> {classify(centre, radius, planes)}")

# Turn the camera and confirm the planes follow.
planes2 = extract_world_planes(build_vp((0.0, 0.0, 10.0), (10.0, 0.0, 0.0)))
print("\nafter turning the camera 30 degrees right:")
for (n1, p1), (n2, p2) in zip(planes, planes2):
    print(f"  {n1:7s} n was ({p1[0]:+.4f}, {p1[1]:+.4f}, {p1[2]:+.4f})"
          f"  now ({p2[0]:+.4f}, {p2[1]:+.4f}, {p2[2]:+.4f})")
print("\n  origin now reads:", classify((0.0, 0.0, 0.0), 0.5, planes2))
print("  new centre reads:", classify((10.0, 0.0, 0.0), 0.5, planes2))
```

Output:

```
frustum planes in WORLD space (unit normals):
  left    n = (+0.7924, +0.0000, -0.6100)  d = +6.0999
  right   n = (-0.7924, +0.0000, -0.6100)  d = +6.0999
  bottom  n = (+0.0000, +0.8660, -0.5000)  d = +5.0000
  top     n = (+0.0000, -0.8660, -0.5000)  d = +5.0000
  near    n = (+0.0000, +0.0000, -1.0000)  d = +9.0000
  far     n = (+0.0000, +0.0000, +1.0000)  d = +90.0000

near plane at z = 9.0  far plane at z = -90.0

classifying world-space bounding spheres:
  small ball at the origin     -> inside
  tiny ball at the target      -> inside
  ball behind the camera       -> outside
  ball past the far plane      -> outside
  ball far off to the side     -> outside
  ball straddling near plane   -> intersecting
  ball just inside near plane  -> inside
  huge ball covering all       -> intersecting

after turning the camera 30 degrees right:
  left    n was (+0.7924, +0.0000, -0.6100)  now (+0.9916, +0.0000, +0.1290)
  right   n was (-0.7924, +0.0000, -0.6100)  now (-0.1290, +0.0000, -0.9916)
  bottom  n was (+0.0000, +0.8660, -0.5000)  now (+0.3536, +0.8660, -0.3536)
  top     n was (+0.0000, -0.8660, -0.5000)  now (+0.3536, -0.8660, -0.3536)
  near    n was (+0.0000, +0.0000, -1.0000)  now (+0.7071, +0.0000, -0.7071)
  far     n was (+0.0000, +0.0000, +1.0000)  now (-0.7071, +0.0000, +0.7071)

  origin now reads: outside
  new centre reads: inside
```

The near and far planes come out as `n = (0, 0, −1)` through z = 9 and
`n = (0, 0, +1)` through z = −90 — exactly right for a camera at z = 10 with
near = 1 and far = 100, and a strong check that the extraction is correct.

The side planes are *tilted*, which is not a bug: a perspective frustum has
slanted sides and an orthographic one would not. Only near and far come out
axis-aligned.

The classification is deliberately conservative. `intersecting` means "possibly
visible, draw it", and only `outside` permits rejection, so a sphere touching a
plane is drawn rather than dropped and nothing pops at the frustum edge. This is
the shape of `Frustum.intersectsSphere` in a typical engine.

</details>

**[ ] Exercise 4 — ** The worked example composes three transforms for a single
object. Real hierarchies nest them: a parent node carries `P` and a child node
carries `C`, and you must decide what `P · C` versus `C · P` means before you can
place anything. With `P = T(10,0,0) · Rz(30°)` and `C = Ry(45°) · S(1,2,1)`, take
the child's local point (1, 0, 0). Compute `C · q` and then `P · (C · q)`, verify
that `(P · C) · q` equals that, and then compute `(C · P) · q` and explain in
words why it is wrong and where in a scene graph the mistake would appear.

<details>
<summary>Solution</summary>

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


def col(m, j):
    return [m[i][j] for i in range(4)]


def translate(tx, ty, tz):
    m = identity(); m[0][3], m[1][3], m[2][3] = tx, ty, tz; return m


def scale(sx, sy, sz):
    m = identity(); m[0][0], m[1][1], m[2][2] = sx, sy, sz; return m


def rot_y(t):
    c, s = cos(t), sin(t)
    return [[c, 0.0, s, 0.0], [0.0, 1.0, 0.0, 0.0], [-s, 0.0, c, 0.0], [0.0, 0.0, 0.0, 1.0]]

def rot_z(t):
    c, s = cos(t), sin(t)
    return [[c, -s, 0.0, 0.0], [s, c, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]


P = matmul(translate(10.0, 0.0, 0.0), rot_z(0.5235987755982988))   # Rz(30 deg)
C = matmul(rot_y(0.7853981633974483), scale(1.0, 2.0, 1.0))       # Ry(45) then scale

q = [1.0, 0.0, 0.0, 1.0]

# The child's own transform first, entirely in the child's frame.
local_to_parent = apply(C, q)
print("child local q        =", q[:3])
print("C * q  (local->parent) =", [round(v, 6) for v in local_to_parent[:3]])

# Then the parent's transform maps parent space into world space.
world_pt = apply(P, local_to_parent)
print("P * (C * q)          =", [round(v, 6) for v in world_pt[:3]])

# The composed world matrix must give the identical answer in one multiply.
print("(P*C) * q            =", [round(v, 6) for v in apply(matmul(P, C), q)[:3]])
print("match?", all(abs(a - b) < 1e-12 for a, b in zip(apply(matmul(P, C), q), world_pt)))

# The wrong order.
print("\n(C*P) * q            =", [round(v, 6) for v in apply(matmul(C, P), q)[:3]])
print("P*C == C*P ?", matmul(P, C) == matmul(C, P))

print("\n(P*C) translation column =", [round(v, 6) for v in col(matmul(P, C), 3)])
print("(C*P) translation column =", [round(v, 6) for v in col(matmul(C, P), 3)])
```

Output:

```
child local q        = [1.0, 0.0, 0.0]
C * q  (local->parent) = [0.707107, 0.0, -0.707107]
P * (C * q)          = [10.612372, 0.353553, -0.707107]
(P*C) * q            = [10.612372, 0.353553, -0.707107]
match? True

(C*P) * q            = [7.68344, 1.0, -7.68344]
P*C == C*P ? False

(P*C) translation column = [10.0, 0.0, 0.0, 1.0]
(C*P) translation column = [7.071068, 0.0, -7.071068, 1.0]
```

Reading the correct chain. The scale (1, 2, 1) stretches the point's y, but y was 0, so nothing happens; the `Ry(45°)` then swings the unit x-axis point onto the line x = −z, giving (0.707107, 0, −0.707107). The parent's `Rz(30°)` rotates that about z — x and y mix, and y was 0, so the point rotates onto (0.866025, 0.353553, −0.707107) — and then the parent's translation adds (10, 0, 0), landing at **(10.612372, 0.353553, −0.707107)**. The composed matrix reproduces that exactly, which is the point of composing: one multiply per vertex instead of two per vertex per level.

Where the wrong order goes wrong. `C · P · q` first moves the point by the parent's translation while it is still in *local* coordinates — so the child is shoved 10 units along its own x axis before the parent's rotation is applied. Then it is scaled by (1, 2, 1), which doubles the y coordinate that the parent's own translation... did not produce, and finally rotated by the *child's* 45° about y, which the parent never asked for. The net result, (7.68344, 1.0, −7.68344), is a point roughly 2.9 units away from the correct one, in a direction that has nothing to do with either node's intent.

Read the translation columns for the diagnosis. `P · C` has translation column (10, 0, 0, 1) — exactly the parent's offset, untouched, because C sits to its *right* and so acts first and cannot rotate it away. `C · P` has translation column (7.071068, 0, −7.071068, 1): the offset has been run through the child's `Ry(45°)` and `S(1,2,1)`, so it is no longer a world position. An offset that should be in world units has been dragged into an object's frame, and that is always the bug.

In a scene graph this shows up as children that visibly ignore their parent's rotation — a turret that stays facing north while its hull turns, a wheel that slides sideways off a turning chassis. Nothing crashes; the hierarchy simply misbehaves in a way that is easy to mistake for a physics or interpolation problem. The rule that prevents it: **`world = parent · child`, and traverse the hierarchy from the root down, multiplying on the right.** Compose a fixed transform on the left of an object's transform, because that is how you say "do this to the finished object"; compose a hierarchy on the right, because that is how you say "in this frame".

</details>

**[ ] Exercise 5 — ** A `look_at` matrix is built by hand in the lesson's pipeline.
Write a routine that certifies any 4×4 matrix as a rigid transform: check that
the 3×3 block is orthonormal, that its determinant is +1, that lengths and dot
products are preserved, and that the matrix is invertible. Then run it on
`M = T(1,2,3) · Ry(0.7) · Rz(0.3)`, on `scale(2,3,4)`, and on a mirrored
transform, and explain what each failure rules out.

<details>
<summary>Solution</summary>

```python
from math import cos, sin


def identity():
    return [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]


def matmul(a, b):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)]
            for i in range(n)]


def transpose(a):
    return [list(r) for r in zip(*a)]


def det3(m):
    a, b, c = m[0][0], m[0][1], m[0][2]
    d, e, f = m[1][0], m[1][1], m[1][2]
    g, h, i = m[2][0], m[2][1], m[2][2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def translate(tx, ty, tz):
    m = identity(); m[0][3], m[1][3], m[2][3] = tx, ty, tz; return m

def scale(sx, sy, sz):
    m = identity(); m[0][0], m[1][1], m[2][2] = sx, sy, sz; return m

def rot_y(t):
    c, s = cos(t), sin(t)
    return [[c, 0.0, s, 0.0], [0.0, 1.0, 0.0, 0.0], [-s, 0.0, c, 0.0], [0.0, 0.0, 0.0, 1.0]]

def rot_z(t):
    c, s = cos(t), sin(t)
    return [[c, -s, 0.0, 0.0], [s, c, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]

def apply(m, v):
    return [sum(m[i][k] * v[k] for k in range(4)) for i in range(4)]

def tl3(m):
    return [row[:3] for row in m[:3]]

def mv3(m, v):
    return [sum(m[i][k] * v[k] for k in range(3)) for i in range(3)]

def dot3(a, b):
    return sum(a[i] * b[i] for i in range(3))

def norm3(a):
    return dot3(a, a) ** 0.5

def orthonormal3(m, tol=1e-12):
    RtR = matmul(transpose(m), m)
    return all(abs(RtR[i][k] - (1.0 if i == k else 0.0)) < tol
               for i in range(3) for k in range(3))

def invert4(m):
    """Gauss-Jordan with a partial pivot per column."""
    a = [list(m[i]) + [1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
    for col in range(4):
        piv = max(range(col, 4), key=lambda r: abs(a[r][col]))
        a[col], a[piv] = a[piv], a[col]
        d = a[col][col]
        a[col] = [x / d for x in a[col]]
        for r in range(4):
            if r != col and a[r][col] != 0.0:
                f = a[r][col]
                a[r] = [a[r][k] - f * a[col][k] for k in range(8)]
    return [row[4:] for row in a]

def is_rigid(m, label):
    R = tl3(m)
    ok_orth = orthonormal3(R)
    d = det3(R)
    u, v = [1.0, 2.0, 3.0], [0.0, 1.0, 0.0]
    ok_len = abs(norm3(mv3(R, u)) - norm3(u)) < 1e-12
    ok_dot = abs(dot3(mv3(R, u), mv3(R, v)) - dot3(u, v)) < 1e-12
    inv = invert4(m)
    ok_inv = all(abs(sum(m[i][k] * inv[k][j] for k in range(4))
                     - (1.0 if i == j else 0.0)) < 1e-12
                 for i in range(4) for j in range(4))
    print(f"{label:34s} orthonormal={ok_orth!s:5s} det={d:+9.4f} "
          f"len={ok_len!s:5s} dot={ok_dot!s:5s} invertible={ok_inv}")
    return ok_orth and abs(d - 1.0) < 1e-12 and ok_len and ok_dot and ok_inv


print("candidate                          checks")
R = matmul(rot_y(0.7), rot_z(0.3))
is_rigid(matmul(translate(1.0, 2.0, 3.0), R), "T(1,2,3) * Ry(0.7) * Rz(0.3)")
is_rigid(scale(2.0, 3.0, 4.0), "scale(2, 3, 4)")
mirror = matmul(translate(1.0, 2.0, 3.0), scale(1.0, 1.0, -1.0))
is_rigid(mirror, "translate * scale(1,1,-1)  [mirror]")

# Round trip and the inverse-transpose shortcut.
M = matmul(translate(1.0, 2.0, 3.0), R)
Minv = invert4(M)
w = [5.0, -1.0, 2.5, 1.0]
print("\nM^-1 * M * (5,-1,2.5) =", [round(x, 9) for x in apply(Minv, apply(M, w))])

R3 = tl3(R)
inv_R3 = tl3(invert4(R))
print("inv(R) == R^T ?",
      all(abs(transpose(R3)[i][k] - inv_R3[i][k]) < 1e-12 for i in range(3) for k in range(3)))
print("=> for a rigid transform, (M^-1)^T normal matrix is just M's 3x3 transpose")

n = [0.0, 1.0, 0.0]
print("\nnormal (0,1,0) transformed by the rigid M:")
print("  (M^-1)^T n =", [round(x, 9) for x in mv3(tl3(transpose(Minv)), n)])
print("  length preserved?", abs(norm3(mv3(tl3(transpose(Minv)), n)) - 1.0) < 1e-12)
```

Output:

```
candidate                          checks
T(1,2,3) * Ry(0.7) * Rz(0.3)       orthonormal=True  det=  +1.0000 len=True  dot=True  invertible=True
scale(2, 3, 4)                     orthonormal=False det= +24.0000 len=False dot=False invertible=True
translate * scale(1,1,-1)  [mirror] orthonormal=True  det=  -1.0000 len=True  dot=True  invertible=True

M^-1 * M * (5,-1,2.5) = [5.0, -1.0, 2.5, 1.0]
inv(R) == R^T ? True
=> for a rigid transform, (M^-1)^T normal matrix is just M's 3x3 transpose

normal (0,1,0) transformed by the rigid M:
  (M^-1)^T n = [-0.226026321, 0.955336489, 0.190379344]
  length preserved? True
```

The three candidates fail in three different ways, and that is the point of testing three things.

The rigid matrix passes everything. Its rows are orthonormal, its determinant is exactly +1, and the direct consequences hold: (1, 2, 3) of length √14 = 3.741657387 comes out at length 3.741657387, and the dot product of 2.0 between (1, 2, 3) and (0, 1, 0) comes out at 2.0. The round trip returns (5, −1, 2.5) to nine decimal places. Note that `det(M)` equals `det(R)` = 1: a translation matrix has determinant 1, so composing one changes nothing — the determinant of the 3×3 block depends on the *linear* part alone.

The scale fails the orthonormality check and the two derived checks, but is still invertible. That combination is informative. `det = 24` is the volume factor: three independent stretches of 2, 3 and 4 multiply to 24. Length preservation fails because the stretch is not uniform, and the dot-product check fails because stretching two vectors by different amounts destroys the angle between them. So `invertible = True` alone tells you almost nothing — every non-degenerate matrix in this lesson except a zero scale factor is invertible, including ones that are obviously wrong.

The mirror is the interesting one. It **passes** the orthonormality check and it **passes** both length and dot preservation, because a reflection through the z axis is a genuine isometry: it preserves lengths and angles exactly. The only thing it fails is `det = -1.0000`. That is precisely why the determinant test is not redundant. An orthonormal 3×3 block has determinant ±1 and nothing more; `+1` says rotation, `−1` says the orientation is reversed, and a mirrored scene renders inside out in a way that no length or angle test will ever reveal. A triangle whose vertex winding was reversed in modelling software, or a negative-determinant node scale on one axis, is the everyday source. Note the contrast with the uniform scale above: the scale fails almost everything, the mirror fails exactly one thing, and only the determinant catches the mirror.

Two facts worth taking away. First, for a pure rotation the inverse is the transpose, so `(M⁻¹)ᵀ` reduces to transposing the 3×3 block — `inv(R) == R^T ? True` — and you can skip the inversion entirely. That is a real optimisation: the 3×3 inverse is the expensive part of building a normal matrix, and for rigid objects it is free. Second, the last block shows why the rigid case is easy: transforming the unit normal (0, 1, 0) through the full `(M⁻¹)ᵀ` gives (−0.226026321, 0.955336489, 0.190379344), a different direction from the original — as it must be, since the matrix contains a rotation — but with `length preserved? True`. Rigid transforms keep normals unit length automatically, so they need no normalisation step and no normal matrix. That is exactly why scaling an object, and only scaling, is what breaks normal handling.

</details>

**[ ] Exercise 6 — ** Without a camera, none of this is checkable. Build a
perspective projection with near = 1, far = 100, vertical field of view 60° and
aspect 4/3, and check four properties numerically: that the near and far planes
map to NDC depth −1 and +1, that depth increases monotonically with distance,
that a point above the camera axis maps to the *upper* half of a 600-pixel-tall
image, and that halving the distance exactly doubles the image offset.

<details>
<summary>Solution</summary>

```python
from math import tan


def perspective(fov_y, aspect, near, far):
    t = 1.0 / tan(fov_y / 2.0)
    return [[t / aspect, 0.0, 0.0, 0.0],
            [0.0, t, 0.0, 0.0],
            [0.0, 0.0, -(far + near) / (far - near), -2.0 * far * near / (far - near)],
            [0.0, 0.0, -1.0, 0.0]]

def apply(m, v):
    return [sum(m[i][k] * v[k] for k in range(4)) for i in range(4)]


WIDTH, HEIGHT = 800, 600
NEAR, FAR = 1.0, 100.0
FOV = 1.0471975511965976  # 60 degrees in radians
P = perspective(FOV, WIDTH / HEIGHT, NEAR, FAR)


def to_ndc(v):
    c = apply(P, list(v) + [1.0])
    return [k / c[3] for k in c[:3]]


# 1. The near and far planes must land on the ends of [-1, 1].
print("near plane, z_eye = -1   -> z_ndc =", round(to_ndc((0, 0, -NEAR))[2], 9))
print("far plane,  z_eye = -100 -> z_ndc =", round(to_ndc((0, 0, -FAR))[2], 9))

# 2. Depth must increase with distance.
print("\ndepth versus distance:")
prev = None
monotone = True
for z in (-1.0, -1.5, -2.0, -5.0, -10.0, -25.0, -50.0, -100.0):
    d = to_ndc((0, 0, z))[2]
    print(f"  distance {-z:7.2f}   z_ndc = {d:+.9f}")
    if prev is not None and d <= prev:
        monotone = False
    prev = d
print("monotonically increasing?", monotone)

# 3. A point above the axis must land in the TOP half of the image (small rows).
print("\nvertical mapping, z_eye = -10:")
for y in (2.0, 1.0, 0.0, -1.0, -2.0):
    ndc = to_ndc((0.0, y, -10.0))
    py = (1 - ndc[1]) / 2 * HEIGHT
    print(f"  y_eye = {y:+5.1f}  y_ndc = {ndc[1]:+.9f}  pixel_y = {py:8.3f}"
          f"  ({'upper' if py < HEIGHT / 2 else 'lower'} half)")

# 4. Half the distance must double the image offset -- that is perspective.
print("\nforeshortening: a 2-unit-wide object at two distances")
for z in (-5.0, -10.0, -20.0):
    left = to_ndc((-1.0, 0.0, z))[0]
    right = to_ndc((1.0, 0.0, z))[0]
    print(f"  distance {-z:5.1f}   width in ndc = {right - left:.9f}"
          f"   pixel width = {(right - left) / 2 * WIDTH:7.3f}")
```

Output:

```
near plane, z_eye = -1   -> z_ndc = -1.0
far plane,  z_eye = -100 -> z_ndc = 1.0

depth versus distance:
  distance    1.00   z_ndc = -1.000000000
  distance    1.50   z_ndc = -0.326599327
  distance    2.00   z_ndc = +0.010101010
  distance    5.00   z_ndc = +0.616161616
  distance   10.00   z_ndc = +0.818181818
  distance   25.00   z_ndc = +0.939393939
  distance   50.00   z_ndc = +0.979797980
  distance  100.00   z_ndc = +1.000000000
monotonically increasing? True

vertical mapping, z_eye = -10:
  y_eye =  +2.0  y_ndc = +0.346410162  pixel_y =  196.077  (upper half)
  y_eye =  +1.0  y_ndc = +0.173205081  pixel_y =  248.038  (upper half)
  y_eye =  +0.0  y_ndc = +0.000000000  pixel_y =  300.000  (lower half)
  y_eye =  -1.0  y_ndc = -0.173205081  pixel_y =  351.962  (lower half)
  y_eye =  -2.0  y_ndc = -0.346410162  pixel_y =  403.923  (lower half)

foreshortening: a 2-unit-wide object at two distances
  distance   5.0   width in ndc = 0.519615242   pixel width = 207.846
  distance  10.0   width in ndc = 0.259807621   pixel width = 103.923
  distance  20.0   width in ndc = 0.129903811   pixel width =  51.962
```

(The `y_eye = +0.0` row reports "lower half" only because the label uses
`py < HEIGHT / 2`, and row 300 is not strictly less than 300. The point is
exactly on the centre line either way.)

**Property 1** holds exactly: −1.0 at the near plane and 1.0 at the far. This is the pair of equations that pins down the third row of the matrix. Setting `z_eye = −n` gives `z_ndc = −1` and `z_eye = −f` gives `z_ndc = +1` determines both `−(f+n)/(f−n)` and `−2fn/(f−n)`, and you can recover them: with `a = −(f+n)/(f−n)` and `b = −2fn/(f−n)`, the equations are `−an + b = −n` and `−af + b = f`, whose difference is `a(f−n) = f+n` — one equation, one unknown, then substitute back.

**Property 2** shows *why* the depth test is `LESS` and not something cleverer. Depth is not linear in distance: doubling from 1 to 2 units moves depth from −1.000000000 to +0.010101010, a change of 1.0101, while doubling from 50 to 100 moves it from 0.979797980 to 1.0, a change of 0.0202. Fifty times the distance, fifty times less depth resolution. The precision is concentrated near the camera. That is the arithmetic behind Common Mistake 5: an extreme near/far ratio leaves the depth buffer with almost no information about distant geometry, and the symptom is z-fighting on far surfaces or every fragment reading depth 1.0. A "reversed-Z" pipeline exploits the same fact by storing 1 − z_ndc so that precision lands at the far end instead.

**Property 3** is the y-flip check, and the pixel rows are what matter: a point 2 units *above* the axis lands at row 196, in the upper half, and one 2 units below lands at row 404, in the lower half. Rows 196 and 404 are exact reflections about row 300, the image centre, which is the symmetry you want. If you had written `y_screen = (y_ndc + 1)/2 * height` these two would swap, and the whole scene renders vertically mirrored — a bug that survives review because the image still looks like a scene.

**Property 4** is perspective itself, and the numbers are exact halvings: 0.519615, 0.259808, 0.129904 as the distance doubles, and in pixels 207.846, 103.923, 51.962. The object is the same size in the world and shrinks exactly inversely with distance. No entry in the projection matrix produces this — every entry is a constant. It comes entirely from dividing by `w = −z_eye`, which is why that division is the one non-linear step in the pipeline, and why a 3×3 matrix could not have done it.

</details>

**Challenge 2 — ** Click-to-select needs the opposite of the whole pipeline: given a
pixel, find the world-space ray the camera sent through it. Using the lesson's
`look_at` and `perspective`, invert the composed view-projection, unproject two
pixels at `z_ndc = −1` and `z_ndc = +1`, intersect the resulting ray with the
floor plane `y = 0`, and confirm the hit re-projects to the pixel you started
from. Camera at (0, 3, 10) looking at the origin, 60° vertical field of view,
4/3 aspect, near = 1, far = 100, on an 800×600 image.

<details>
<summary>Solution</summary>

The trick is that the near and far planes are the two ends of the view frustum,
so unprojecting at `z_ndc = −1` and `+1` gives exactly the two endpoints of the
click ray — no camera-space reconstruction needed.

```python
from math import sqrt, tan


def identity():
    return [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]

def matmul(a, b):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

def apply(m, v):
    return [sum(m[i][k] * v[k] for k in range(4)) for i in range(4)]

def invert4(m):
    """Gauss-Jordan inverse of a 4x4, partial pivot per column."""
    a = [list(m[i]) + [1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
    for col in range(4):
        piv = max(range(col, 4), key=lambda r: abs(a[r][col]))
        a[col], a[piv] = a[piv], a[col]
        d = a[col][col]
        a[col] = [x / d for x in a[col]]
        for r in range(4):
            if r != col and a[r][col] != 0.0:
                f = a[r][col]
                a[r] = [a[r][k] - f * a[col][k] for k in range(8)]
    return [row[4:] for row in a]

def sub3(a, b): return [a[i] - b[i] for i in range(3)]
def add3(a, b): return [a[i] + b[i] for i in range(3)]
def dot3(a, b): return sum(a[i] * b[i] for i in range(3))
def cross3(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def norm3(a): return sqrt(dot3(a, a))

def look_at(eye, target, up):
    f = sub3(target, eye)
    f = [c / norm3(f) for c in f]
    z = [-c for c in f]                 # camera looks down -z
    x = list(cross3(up, z))
    x = [c / norm3(x) for c in x]
    y = list(cross3(z, x))
    V = [[x[0], x[1], x[2], 0.0], [y[0], y[1], y[2], 0.0],
         [z[0], z[1], z[2], 0.0], [0.0, 0.0, 0.0, 1.0]]
    t = [-sum(V[i][j] * eye[j] for j in range(3)) for i in range(3)]
    V[0][3], V[1][3], V[2][3] = t
    return V

def perspective(fov_y, aspect, near, far):
    t = 1.0 / tan(fov_y / 2.0)
    return [[t / aspect, 0.0, 0.0, 0.0],
            [0.0, t, 0.0, 0.0],
            [0.0, 0.0, -(far + near) / (far - near), -2.0 * far * near / (far - near)],
            [0.0, 0.0, -1.0, 0.0]]

WIDTH, HEIGHT = 800, 600
NEAR, FAR = 1.0, 100.0
VP = matmul(perspective(1.0471975511965976, WIDTH / HEIGHT, NEAR, FAR),
            look_at((0.0, 3.0, 10.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)))
INV_VP = invert4(VP)


def unproject(px, py, z_ndc):
    """Pixel -> world point at the given NDC depth."""
    x_ndc = (2.0 * px / WIDTH) - 1.0
    y_ndc = 1.0 - (2.0 * py / HEIGHT)   # same y flip as the viewport transform
    p = apply(INV_VP, [x_ndc, y_ndc, z_ndc, 1.0])
    return [k / p[3] for k in p[:3]]    # the final divide: back to real coords


def ray_plane(origin, direction, normal, offset):
    """Intersect with the plane normal.x = offset. Returns (t, point)."""
    denom = dot3(direction, normal)
    if abs(denom) < 1e-12:
        return None                     # parallel: no hit or infinitely many
    t = (offset - dot3(origin, normal)) / denom
    return t, add3(origin, [t * k for k in direction])


FLOOR_N, FLOOR_D = (0.0, 1.0, 0.0), 0.0

for px, py in [(400, 300), (400, 450), (600, 450), (200, 550), (400, 100)]:
    near_p = unproject(px, py, -1.0)
    far_p = unproject(px, py, 1.0)
    direction = sub3(far_p, near_p)
    hit = ray_plane(near_p, direction, FLOOR_N, FLOOR_D)
    print(f"pixel ({px:3d},{py:3d})  near={[round(v, 6) for v in near_p]}")
    if hit is None or hit[0] < 0.0:
        print("    ray points above the horizon: no hit on the floor")
        continue
    t, point = hit
    print(f"    far={[round(v, 4) for v in far_p]}   t = {t:.6f}")
    print(f"    floor hit = ({point[0]:+.6f}, {point[1]:+.6f}, {point[2]:+.6f})")
    # Push the hit back through the forward pipeline: it must return the pixel.
    clip = apply(VP, list(point) + [1.0])
    sx = (clip[0] / clip[3] + 1) / 2 * WIDTH
    sy = (1 - clip[1] / clip[3]) / 2 * HEIGHT
    print(f"    re-projected pixel = ({sx:.4f}, {sy:.4f})")
```

Output:

```
pixel (400,300)  near=[0.0, 2.712652, 9.042174]
    far=[0.0, -25.7348, -85.7826]   t = 0.095357
    floor hit = (+0.000000, +0.000000, +0.000000)
    re-projected pixel = (400.0000, 300.0000)
pixel (400,450)  near=[0.0, 2.436151, 9.125124]
    far=[0.0, -53.3849, -77.4876]   t = 0.043642
    floor hit = (+0.000000, +0.000000, +5.345154)
    re-projected pixel = (400.0000, 450.0000)
pixel (600,450)  near=[0.3849, 2.436151, 9.125124]
    far=[38.49, -53.3849, -77.4876]   t = 0.043642
    floor hit = (+2.047891, +0.000000, +5.345154)
    re-projected pixel = (600.0000, 450.0000)
pixel (200,550)  near=[-0.3849, 2.251818, 9.180424]
    far=[-38.49, -71.8182, -71.9576]   t = 0.030401
    floor hit = (-1.543341, +0.000000, +6.713731)
    re-projected pixel = (200.0000, 550.0000)
pixel (400,100)  near=[0.0, 3.08132, 8.931573]
    ray points above the horizon: no hit on the floor
```

Every hit re-projects to four decimal places of the pixel it started from, which
is the round-trip property the whole thing rests on: `VP · VP⁻¹ = I`. Getting the
pixel back exactly means the y flip was written consistently in both directions,
the aspect ratio is right, and the depth planes are where the matrix put them.
In a real engine this loop is the regression test for the camera code.

Four results deserve comment.

The centre pixel (400, 300) hits the origin. That is a consequence of the camera
being aimed at (0, 0, 0): the pixel at the exact centre of the image is the point
the view direction hits, and it hits the look-at target. A useful sanity check to
keep — if your centre pixel does not land on the target, `look_at` or the viewport
transform has the y flip wrong.

Moving down the screen brings the hit *closer*: pixel (400, 450) lands at
z = +5.345154, well in front of the origin. Moving further down and right,
(600, 450), keeps the same z = +5.345154 but adds x = +2.047891. That the z is
identical is not a coincidence — it is the symmetry of the frustum about its
central vertical plane, and the horizontal offset is the perspective divide at
work. Compare it with pixel (200, 550): the hit is at (−1.543341, 0, +6.713731),
both further left and further away, because that pixel is both off-axis and lower
in the frame. Those three rows together are the ground plane rendered correctly.

Pixel (400, 100) produces no hit, and that is correct rather than a failure. It is
100 pixels *above* the centre, which places it above the horizon: the camera at
height 3 is tilted downward, so the top of the image looks at the sky. The ray's
y component points away from the floor, so `t` is negative and the intersection
lies behind the camera. Real picking code must handle this — it is why a
raycaster in a game returns "miss" when you click above the skyline rather than
hitting an infinitely distant floor.

Two implementation notes. First, the final divide by `p[3]` in `unproject` is
not optional: `INV_VP` returns homogeneous coordinates, and skipping the divide
gives you a point on the line through the origin, not a point in the world.
Second, the inverse is computed once per camera change, not per click — the
lesson's numpy section does exactly this with `inv = np.linalg.inv(VP)` and
verifies the round trip on a test point. What makes it safe is that a
view-projection matrix is well conditioned for any sane near/far ratio; if you
push the far plane to a million while the near plane is 0.001, the same inversion
loses most of its significant digits and picking develops a bias toward the near
plane. Bounding the frustum is what keeps this routine honest.

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
