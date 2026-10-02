# Part 07 — Geometry for Graphics

Matrices in 3D, used by every rendering engine and game engine — plus the
algorithms that answer spatial questions about the things those matrices move.

## What this part covers

Three lessons on the geometry that runs under every renderer, every physics
engine, and every spatial database. The part has one running idea: **a point is
a vector, a change of frame is a matrix, and everything else follows from knowing
which matrix to use and when**.

That gives the shape of the part. Lesson 90 builds the vocabulary — length,
angle, perpendicularity, and the cross product that produces a normal. Lesson 91
turns the vocabulary into a pipeline: the 4×4 matrices that translate, rotate and
project, and the order they must be composed in. Lesson 92 drops the matrices and
asks the questions an engine actually asks: what is the outline of this mesh,
which two of these ten thousand dots are nearest, is this point inside this
shape, and which pairs of objects need an exact test.

The through-line from 91 to 92 is the transform's shadow. A model matrix tells
you where a vertex goes; a collision test tells you whether two vertices are the
same point. Lesson 92 is the discrete, decision-making version of the same
geometry, and it is where the O(n log n) claims start being about objects rather
than about numbers.

## The lessons

| # | Lesson | What it gives you |
| --- | --- | --- |
| 90 | [Vectors in 3D and the Cross Product](../part07_geometry_graphics/90_vectors_3d_and_cross_product.md) | Vectors as points and directions; dot product for length and angle; orthogonality; the cross product as a perpendicular direction and a signed area; normals; left-handed versus right-handed conventions and why the choice is visible in the output |
| 91 | [Transformations for Computer Graphics](../part07_geometry_graphics/91_transformations_graphics.md) | Translation, scale and rotation matrices; homogeneous coordinates; composition order read right to left; the scene graph and parent-child transforms; `look_at`; perspective projection and the divide by w; near/far depth and precision; clipping; the viewport transform; the inverse transpose for normals |
| 92 | [Geometric Algorithms](../part07_geometry_graphics/92_geometric_algorithms.md) | Convexity and hull vertices; Andrew's monotone chain and Graham scan; the shoelace formula; closest pair by divide and conquer; point-in-polygon by crossing number; line–circle intersection via the discriminant; broad phase versus narrow phase; uniform grids, BVHs and kd-trees |

## What this part assumes

- Lesson 31 (matrices and matrix algebra) — matrix multiplication and block
  structure. Everything in 91 is a 4×4 matrix, and the composition-order rule is
  just associativity.
- Lesson 35 (linear transformations and kernels) — a linear map as something
  that takes a vector in and produces a vector out. 91 calls a transform exactly
  that and nothing more.
- Lesson 37 (inner products, norms, and geometry) — dot products give lengths and
  angles, and orthogonality is what makes a normal a normal. This is the lesson
  that turns the matrices of 31 into something you can picture.
- Lesson 80 (big-O and complexity analysis) — only for the `$O(n \log n)$`
  claims in 92. Without it those are just assertions.
- Basic Python: lists of tuples, loops, functions, and a class in Lesson 92's
  spatial hash. Every main example runs with the standard library alone.

You do **not** need calculus, and you do not need any graphics experience. Lesson
92 needs no linear algebra beyond a sign test — if you can decide whether a
triple of points turns left or right, you can do all of it.

## A suggested route

The dependencies are real and short:

```
90 (vectors, cross product, normals)
  └─> 91 (4×4 transforms, projection, the pipeline)
        └─> 92 (hull, closest pair, point-in-polygon, broad/narrow phase)
```

Roughly 100 minutes for all three at the stated pace, and the exercises —
which have full worked solutions in the same files — roughly double that.

Read them in order. If you already write shader code and know why
`gl_Position = MVP * vec4(pos, 1.0)`, read 90 for the notation, skim 91, and
start at 92 — that lesson is almost entirely self-contained and is the one with
the most transferable algorithms in the part.

If you want the other direction, 90 and 91 together are the minimum for reading
engine source: the `btDbvtBroadphase` and `SqPrBroadPhase` classes named in 92
are full of exactly the matrices 91 derives.

## What you should be able to do afterwards

- Compose a transform and say, without running it, which factor acts first.
- Explain why a normal needs the inverse transpose and when the transpose alone
  is enough.
- Compute a convex hull, its area, and whether a point is inside it — and explain
  which of those answers are conservative rather than exact.
- Take a nearest-neighbour question and choose between brute force, a grid, a
  BVH and a kd-tree, and say what each costs.
- Look at a collision-detection module and identify which part is broad phase
  and which is narrow phase, and argue whether the broad phase is conservative.

## Where to go next

[Part 08 — Optimisation](../part08_optimization/) picks up the one idea from
this part it needs. Convexity appears in Lesson 92 as the property that makes the
hull a valid collision proxy and the centroid safe;
[Lesson 100 — Convexity](../part08_optimization/100_convexity.md) develops it as
the property that makes optimisation tractable.

[Part 03 — Linear Algebra](../part03_linear_algebra/) is the prerequisite and
stays useful: SVD is how you compress a transform matrix, and
[Lesson 40 — SVD and PCA](../part03_linear_algebra/40_svd_and_pca.md) is where
the eigen-decomposition a graphics researcher actually wants is proved.

For the notation, see [SYMBOLS.md](../SYMBOLS.md). The symbols used here that
are not in the general table — `conv`, the cross product determinant, the
crossing number — are defined where they appear. Verify the whole part at any
time with `python run_all.py part07_geometry_graphics`.