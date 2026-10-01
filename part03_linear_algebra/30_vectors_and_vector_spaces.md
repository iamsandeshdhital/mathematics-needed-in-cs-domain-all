# 30 — Vectors and Vector Spaces

**Part**: part03_linear_algebra · **Prerequisites**: 24 · **Time**: 40 min

---

## In Plain Words

A vector is just a list of numbers. Three measurements about a person, the
pixels of an image, the coefficients of a polynomial — each one is a list of
numbers, and once you see that a lot of code stops looking arbitrary. What
makes lists of numbers special is that you can add them together and you can
multiply them by a plain number, and both operations keep you inside the world
of lists of numbers. Everything else in this part is a consequence of that fact.

Once you can add and scale, you can ask the two questions that the whole part
is about. First: starting from some given lists, which other lists can I build?
That set is called the *span*, and it is the set of things your data can reach.
Second: are any of the lists you were given unnecessary, because they can be
rebuilt from the others? If so you are wasting memory, and the fix is to keep
only the ones you cannot rebuild, which is what a *basis* is.

A vector space is nothing more exotic than a collection of lists of numbers that
is closed under addition and scaling. Real numbers, complex numbers, and even
bits satisfy the same rules, which is why the same mathematics handles geometry,
data, and error-correcting codes.

## Why Computer Science Cares

- **Machine learning data.** A training set is a list of vectors. Cosine
  similarity between two embeddings, Euclidean distance between two images, and
  the projection step in PCA are all vector operations from this lesson.
- **Search and ranking.** TF-IDF represents each document as a (sparse) vector.
  A query is a vector. Ranking documents is ranking the dot products between the
  query vector and each document vector.
- **Recommendation.** A user-item rating matrix is a table of vectors. Predicting
  a missing rating is fitting a linear combination of a few known vectors, which
  is a linear system, and the "dimension" of the span of your vectors is the
  number of independent factors in your data.
- **Computer graphics.** A 3-D point, a colour, a surface normal, and a 4×4
  transform are all vectors. Every vertex shader in [lesson 91](../part07_geometry_graphics/91_transformations_graphics.md)
  is arithmetic of this kind.
- **Error-correcting codes and hashes.** Treat a bit string as a vector over the
  field of two elements. A linear code is a subspace, and "the parity bits are
  determined by the data bits" is a linear constraint. See
  [lesson 113](../part09_number_theory_crypto/113_error_correcting_codes.md).
- **Interview questions.** "Given a matrix of data, which columns are
  redundant?", "Why does gradient descent need the features to be on comparable
  scales?", and "what does it mean if two eigenvectors have the same value?" are
  all questions about span and independence.

## The Formal Version

Symbols follow [SYMBOLS.md](../SYMBOLS.md).

**Definition.** Let `F` be a *field* of scalars — a set of numbers where
addition, subtraction, multiplication, and division by nonzero elements all
behave as you expect. `ℝ`, `ℂ` and GF(2) (arithmetic mod 2) are the three you
will meet here.

**Definition.** A **vector space** over `F` is a set `V` of objects together
with two operations, vector addition and scalar multiplication, such that:

1. `u + v` is in `V` whenever `u, v` are in `V` (closure under addition).
2. `c·u` is in `V` whenever `c ∈ F` and `u` is in `V` (closure under scaling).
3. `u + (v + w) = (u + v) + w` (associativity).
4. `u + 0 = u`, and for every `u` there is `-u` with `u + (-u) = 0` (additive
   identity and inverses).
5. `c·(d·u) = (c·d)·u` and `c·(u+v) = c·u + c·v` (compatibility).
6. `1·u = u` (scalar identity).

**Explanation.** Rule 1 and rule 2 are the whole content of "closed under".
Rules 3 to 6 are bookkeeping that says the arithmetic behaves the way ordinary
arithmetic does. The standard example is `ℝⁿ`: all lists of `n` real numbers.

**Definition.** A **linear combination** of vectors `v₁, …, v_k` is
`c₁v₁ + c₂v₂ + … + c_kv_k` for scalars `c₁, …, c_k`.

**Definition.** The **span** of a set `S` is the set of all linear combinations of
its elements:

    span(S) = { c₁v₁ + … + c_kv_k : v_i ∈ S, c_i ∈ F }

**Explanation.** The span is the set of points reachable from the origin by
adding scaled copies of the generators. Adding a redundant generator never
changes the span, which is why span is the right notion of "what this data can
represent" and not the number of columns you happen to have.

**Definition.** A set `S = {v₁, …, v_k}` is **linearly independent** (or *linearly
free*) if the only choice of scalars making

    c₁v₁ + … + c_kv_k = 0

is `c₁ = … = c_k = 0`. If some other choice exists, `S` is **linearly dependent**.

**Explanation.** A dependence relation `c₁v₁ + … + c_kv_k = 0` with at least one
nonzero `c_j` says "these vectors cancel each other out". Divide by `c_j` and you
have expressed `v_j` in terms of the others. So independence is exactly the
statement that no generator is redundant.

**Theorem.** If `S` has `m` vectors in `ℝⁿ` and `m > n`, then `S` is linearly
dependent.

**Explanation.** Consider the system `Ac = 0` where `A` has the vectors of `S` as
its columns. `A` has `n` rows and `m > n` columns, so it has more unknowns than
equations, and any homogeneous system with more unknowns than equations has a
nontrivial solution. The full algorithm is in
[lesson 34](../part03_linear_algebra/34_basis_dimension_rank.md).

**Definition.** A **subspace** `W ⊆ V` is a subset that is itself a vector space
under the same operations.

**Theorem (Subspace test).** A nonempty subset `W ⊆ V` is a subspace if and only
if:

1. `0 ∈ W`;
2. `c·u ∈ W` for every `c ∈ F` and `u ∈ W`;
3. `u + v ∈ W` for all `u, v ∈ W`.

**Explanation.** Condition 1 gives the additive identity, condition 2 with `c = 0`
gives `0·u = 0 ∈ W`, condition 2 with `c = -1` gives additive inverses, and the
rest of the axioms follow from the ambient ones. Nothing else needs checking.
This is the single most-used test in applied linear algebra.

**Definition.** `dim(V)`, the **dimension** of a vector space, is the number of
vectors in any basis of `V`. For `ℝⁿ` it is `n`.

**Theorem.** A set of `k` vectors in `ℝⁿ` is independent if and only if its span
has dimension `k`.

**Explanation.** This is why "independent" and "a basis of its span" mean the
same thing from two directions. See
[lesson 34](../part03_linear_algebra/34_basis_dimension_rank.md).

## Worked Example

Three features describe a house: floor area in square metres, number of rooms,
and age in years. Three houses:

    H1 = (80,  3, 10)
    H2 = (120, 4, 25)
    H3 = (200, 7, 35)

Note the third: it is the first two added together, component by component.
`80 + 120 = 200`, `3 + 4 = 7`, `10 + 25 = 35`.

**Question 1: is `H3` in the span of `H1` and `H2`?**

Yes, with `a = 1`, `b = 1`:

    1·(80, 3, 10) + 1·(120, 4, 25)
      = (80 + 120, 3 + 4, 10 + 25)
      = (200, 7, 35)
      = H3  ✓

So `{H1, H2, H3}` is linearly dependent. Here is the relation:

    -1·H1 + -1·H2 + 1·H3 = 0

Verify by hand, component by component:
- area: `-80 - 120 + 200 = 0` ✓
- rooms: `-3 - 4 + 7 = 0` ✓
- age: `-10 - 25 + 35 = 0` ✓

**Question 2: what is `span(H1, H2)`?**

Every point of the form `a·H1 + b·H2`. Since `H3` is already in there, this is
also `span(H1, H2, H3)` — the third vector bought nothing. There are two free
numbers, `a` and `b`, and only two independent directions.

To describe the set without naming `H1` and `H2`, find a nonzero vector `p`
perpendicular to both. Solve

    80p₁ +  3p₂ + 10p₃ = 0     (p·H1 = 0)
    120p₁ + 4p₂ + 25p₃ = 0     (p·H2 = 0)

Multiply the first equation by 4 and the second by 3, then subtract:

    320p₁ + 12p₂ + 40p₃ = 0
    360p₁ + 12p₂ + 75p₃ = 0
    --------------------
    -40p₁      - 35p₃ = 0      →  40p₁ = -35p₃  →  p₁ = -7p₃/8

Set `p₃ = 8`, so `p₁ = -7`. Then `80(-7) + 3p₂ + 10(8) = 0` gives
`-560 + 3p₂ + 80 = 0`, so `3p₂ = 480`, so `p₂ = 160`.

Therefore `p = (-7, 160, 8)`.

Check it against all three houses:
- `p·H1 = -7(80) + 160(3) + 8(10) = -560 + 480 + 80 = 0` ✓
- `p·H2 = -7(120) + 160(4) + 8(25) = -840 + 640 + 200 = 0` ✓
- `p·H3 = -7(200) + 160(7) + 8(35) = -1400 + 1120 + 280 = 0` ✓

Every linear combination of the houses is perpendicular to `p`, because
`p·(a·H1 + b·H2) = a(p·H1) + b(p·H2) = 0`. So the span is contained in the
flat set

    -7x + 160y + 8z = 0

and since `H1`, `H2` are independent, that containment is equality. The span is
the plane through the origin whose normal is `(-7, 160, 8)`. A subspace, as the
subspace test demands: it contains the origin, and scaling and adding preserve
the equation, because `c(-7x + 160y + 8z) = 0` whenever the bracket is `0`.

**Question 3: which points are reachable, and which are not?**

Reachable: `H1 + 2·H2 = (80 + 240, 3 + 8, 10 + 50) = (320, 11, 60)`.
Check the plane equation: `-7(320) + 160(11) + 8(60) = -2240 + 1760 + 480 = 0` ✓

Not reachable: `(0, 0, 1)`. Check the plane equation:
`-7(0) + 160(0) + 8(1) = 8 ≠ 0`. No coefficients `a`, `b` give it, and the
reason is not a computational failure but a structural fact: the data does not
contain that direction.

**Question 4: how many houses would you need for an independent set?**

Two. `H1` and `H2` are independent because neither is a multiple of the other —
the ratio of areas is `80/120 = 2/3`, and the ratio of rooms is `3/4`, and those
differ, so no single scalar turns `H1` into `H2`. Add a third house that is not a
combination and you would have three independent vectors in three dimensions,
spanning all of `ℝ³`.

This is the whole practical content of the lesson: three feature columns of a
dataset may carry two independent factors, not three, and knowing which and why
is what [lesson 34](../part03_linear_algebra/34_basis_dimension_rank.md) is for.

## Runnable Code

### Vector arithmetic on plain lists

A vector is a Python list of numbers. Everything in this lesson is a function
over lists, so there is nothing to import beyond `math`.

```python
from math import sqrt


# ---------------------------------------------------------------- the toolbox
# A vector is a Python list of numbers. Nothing else. Everything below is a
# function over those lists.
def vadd(u, v):
    """Add two vectors componentwise."""
    return [a + b for a, b in zip(u, v)]


def vsub(u, v):
    """Subtract two vectors componentwise."""
    return [a - b for a, b in zip(u, v)]


def vscale(c, u):
    """Multiply every component of u by the scalar c."""
    return [c * a for a in u]


def dot(u, v):
    """Dot product: multiply matching components, then add them up."""
    return sum(a * b for a, b in zip(u, v))


def norm(u):
    """Euclidean length: square root of the sum of squared components."""
    return sqrt(dot(u, u))


def print_vector(label, v):
    print(f"{label} = {v}")


# ---------------------------------------------------------------- the example
# Three data points, each a vector of three numbers.
# Read them as (height in cm, weight in kg, age in years).
bob = [170.0, 70.0, 30.0]
sue = [160.0, 55.0, 28.0]
max_point = [185.0, 90.0, 45.0]

print("=== Basic vector arithmetic ===")
print_vector("bob", bob)
print_vector("sue", sue)

# Adding two data points means adding each feature separately.
sum_point = vadd(bob, sue)
print_vector("bob + sue", sum_point)

# Scaling by 2 doubles every feature.
print_vector("2 * max", vscale(2.0, max_point))

# Subtracting two points gives a difference vector. In gradient descent this is
# the direction of steepest increase of the loss.
grad = vsub(sue, bob)
print_vector("sue - bob (a gradient, roughly)", grad)

print()
print("=== The dot product and the norm ===")
# The dot product is how much two vectors point the same way.
print(f"dot(bob, sue)   = {dot(bob, sue)}")
print(f"norm(bob)       = {norm(bob):.4f}")
print(f"norm(sue)       = {norm(sue):.4f}")
print(f"norm(sue - bob) = {norm(grad):.4f}")

# Dot product divided by the two lengths is the cosine of the angle between
# them, between -1 and 1. This is the core of every search engine's text search.
cosine = dot(bob, sue) / (norm(bob) * norm(sue))
print(f"cosine similarity(bob, sue) = {cosine:.4f}")

# A right-angle check: if two vectors are perpendicular their dot product is 0.
right_a = [1.0, 0.0]
right_b = [0.0, 5.0]
print(f"dot([1,0], [0,5]) = {dot(right_a, right_b)}  (perpendicular)")
```

### Linear combinations and the span

The span is the set of everything reachable by scaling and adding generators.
To ask whether a target is reachable, we form a linear system and solve it. The
solver here is a preview; [lesson 32](../part03_linear_algebra/32_linear_systems_gaussian_elimination.md)
builds the real one and explains why partial pivoting matters.

```python
from math import sqrt


# ---------------------------------------------------------------- helpers
# A vector is a Python list of numbers. A list of vectors is a matrix:
# a list of rows.
def vadd(u, v):
    return [a + b for a, b in zip(u, v)]


def vsub(u, v):
    return [a - b for a, b in zip(u, v)]


def vscale(c, u):
    return [c * a for a in u]


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def norm(u):
    return sqrt(sum(a * a for a in u))


def columns_to_matrix(generators):
    """Turn a list of generators (the columns) into a matrix (a list of rows)."""
    return [
        [generators[j][i] for j in range(len(generators))]
        for i in range(len(generators[0]))
    ]


def solve_consistent(A, b, tol=1e-9):
    """Try to solve A c = b.

    Returns one coefficient vector if the system is consistent, else None.
    Free variables are set to zero, which is a choice, not a fact. Lesson 32
    does this properly with full row reduction and case analysis.
    """
    rows, cols = len(A), len(A[0])
    M = [list(A[i]) + [b[i]] for i in range(rows)]

    pivot_cols = []
    r = 0
    for c in range(cols):
        # Find a row at or below r that has a nonzero entry in column c.
        pivot = None
        for i in range(r, rows):
            if abs(M[i][c]) > tol:
                pivot = i
                break
        if pivot is None:
            continue
        M[r], M[pivot] = M[pivot], M[r]
        for i in range(rows):
            if i != r:
                factor = M[i][c] / M[r][c]
                for j in range(c, cols + 1):
                    M[i][j] -= factor * M[r][j]
        pivot_cols.append(c)
        r += 1
        if r == rows:
            break

    # A row of the form [0 0 0 | nonzero] means no solution exists.
    for i in range(len(pivot_cols), rows):
        if abs(M[i][cols]) > tol:
            return None

    x = [0.0] * cols
    for i, c in enumerate(pivot_cols):
        x[c] = M[i][cols] / M[i][c]
    return x


def print_vector(label, v):
    print(f"{label} = {[round(x, 4) for x in v]}")


# ---------------------------------------------------------------- the basics
# The three standard basis vectors of R^3. Each one points along a single axis.
e1 = [1.0, 0.0, 0.0]
e2 = [0.0, 1.0, 0.0]
e3 = [0.0, 0.0, 1.0]

print("=== A linear combination is a weighted sum ===")
# 2*e1 + 3*e2 + 5*e3 means "2 units along axis 1, 3 along axis 2, 5 along axis 3".
combo = vadd(vadd(vscale(2.0, e1), vscale(3.0, e2)), vscale(5.0, e3))
print_vector("2*e1 + 3*e2 + 5*e3", combo)

# By hand: 2*[1,0,0] = [2,0,0], 3*[0,1,0] = [0,3,0], 5*[0,0,1] = [0,0,5].
# Sum componentwise: [2+0+0, 0+3+0, 0+0+5] = [2, 3, 5]. Nothing clever here,
# because the basis vectors do not overlap. That is exactly what a basis buys you.
print(f"matches the hand calculation [2.0, 3.0, 5.0]: {combo == [2.0, 3.0, 5.0]}")

print()
print("=== Now with overlapping vectors, where the arithmetic matters ===")
u = [1.0, 2.0, 3.0]
w = [0.0, 1.0, 4.0]
mixed = vadd(vscale(4.0, u), vscale(-1.0, w))
print_vector("u", u)
print_vector("w", w)
print_vector("4*u", vscale(4.0, u))
print_vector("-1*w", vscale(-1.0, w))
print_vector("4*u - w", mixed)
print(f"by hand 4*[1,2,3] - [0,1,4] = [4-0, 8-1, 12-4] = [4, 7, 8]: {mixed == [4.0, 7.0, 8.0]}")

print()
print("=== Redundancy: a vector built from others adds no new direction ===")
# v3 = e1 + e2, so having e1, e2 and v3 gives no more reach than e1 and e2.
v3 = vadd(e1, e2)
print_vector("v3 = e1 + e2", v3)
leftover = vsub(v3, vadd(e1, e2))
print(f"v3 - (e1 + e2) = {leftover}   (all zeros means v3 carried no new direction)")
print(f"norm(v3) = {norm(v3):.4f}, and sqrt(1+1) = {sqrt(2):.4f} by hand")

print()
print("=== Span: everything reachable as a linear combination ===")
generators = [e1, e2, v3]      # three vectors, but only two real directions
A = columns_to_matrix(generators)
print("generators used as COLUMNS of A:")
for j, g in enumerate(generators):
    print(f"  column {j} = {g}")
print(f"A = {A}")

# This target lives in the span: its third component is zero.
reachable = [4.0, -1.0, 0.0]
print(f"target (third component 0) = {reachable}")
print(f"one solution c = {solve_consistent(A, reachable)}")

# This target does not. Every combination of e1, e2 and v3 has third component
# zero, so there is no way to reach a point whose third component is 2.
unreachable = [4.0, -1.0, 2.0]
print(f"target (third component 2) = {unreachable}")
print(f"one solution c = {solve_consistent(A, unreachable)}  <- None means no solution")

print()
print("=== Four standard basis vectors reach every point of R^4 ===")
R4_basis = [
    [1.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 1.0],
]
any_point = [3.5, -2.0, 0.0, 7.25]
recovered = [
    sum(any_point[j] * R4_basis[j][i] for j in range(4)) for i in range(4)
]
print_vector("3.5*e1 - 2*e2 + 0*e3 + 7.25*e4", recovered)
print(f"equals the original point: {recovered == any_point}")
```

### Testing linear independence

Independence is the question "is `Ac = 0` solvable with `c ≠ 0`?", which is the
same row reduction we will build properly in lesson 32.

```python
import random

# Linear independence: can any vector in the list be built from the others?
# The test is always the same question asked in the language of row reduction:
# does the homogeneous system  A c = 0  have a solution other than all zeros?
#
# Careful with orientation. A c = 0 puts the vectors in the COLUMNS of A, and c
# has one entry per vector. That is the version that produces the relation we
# want, so we build A that way.

TOL = 1e-9


def as_columns(vectors):
    """Build a matrix whose columns are the given vectors."""
    dim = len(vectors[0])
    return [[v[j] for v in vectors] for j in range(dim)]


def _rref(M, tol=TOL):
    """Full row reduction, in place-ish. Returns (reduced matrix, pivot columns)."""
    M = [list(row) for row in M]
    rows, cols = len(M), len(M[0])
    r = 0
    pivot_cols = []
    for c in range(cols):
        pivot = None
        for i in range(r, rows):
            if abs(M[i][c]) > tol:
                pivot = i
                break
        if pivot is None:
            continue
        M[r], M[pivot] = M[pivot], M[r]
        # Scale the pivot row to 1 so back substitution is trivial.
        p = M[r][c]
        for j in range(c, cols):
            M[r][j] /= p
        for i in range(rows):
            if i != r:
                factor = M[i][c]
                for j in range(c, cols):
                    M[i][j] -= factor * M[r][j]
        pivot_cols.append(c)
        r += 1
        if r == rows:
            break
    return M, pivot_cols


def is_independent(vectors):
    """True if no vector in the list is a linear combination of the others."""
    _, pivot_cols = _rref(as_columns(vectors))
    # Every vector got its own pivot column, so every vector is needed.
    return len(pivot_cols) == len(vectors)


def dependent_relation(vectors):
    """If the vectors are dependent, exhibit a nonzero c with A c = 0.

    Returns None if the vectors are independent. Otherwise returns coefficients
    such that  c1*v1 + c2*v2 + ... = the zero vector.
    """
    M, pivot_cols = _rref(as_columns(vectors))
    cols = len(vectors)
    if len(pivot_cols) == cols:
        return None
    # A non-pivot column is a free variable. Set the first one to 1, then read
    # the pivot variables straight off the reduced rows.
    free = [c for c in range(cols) if c not in pivot_cols][0]
    c_vec = [0.0] * cols
    c_vec[free] = 1.0
    for row_index, pc in enumerate(pivot_cols):
        c_vec[pc] = -M[row_index][free]
    return c_vec


e1 = [1.0, 0.0, 0.0]
e2 = [0.0, 1.0, 0.0]
e3 = [0.0, 0.0, 1.0]

print("=== Independent sets ===")
print(f"{{e1, e2, e3}}                   independent: {is_independent([e1, e2, e3])}")
print(f"{{e1, e2}}                       independent: {is_independent([e1, e2])}")
print(f"{{e1, 2*e1}}  (collinear)        independent: "
      f"{is_independent([e1, [2.0, 0.0, 0.0]])}")
print(f"{{[1,0],[2,3]}}                  independent: "
      f"{is_independent([[1.0, 0.0], [2.0, 3.0]])}")

print()
print("=== Dependent sets, with the cancelling relation exhibited ===")
cases = [
    ("{[1,0], [0,1], [1,1]}", [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]),
    ("{[1,0], [0,1], [3,-2]}", [[1.0, 0.0], [0.0, 1.0], [3.0, -2.0]]),
    ("{[1,2], [2,4]}", [[1.0, 2.0], [2.0, 4.0]]),
    ("{[1,2], [2,3]}", [[1.0, 2.0], [2.0, 3.0]]),
    ("{[1,0,0],[0,1,0],[1,1,0]}", [e1, e2, [1.0, 1.0, 0.0]]),
    ("{[1,1],[1,2],[2,3]}", [[1.0, 1.0], [1.0, 2.0], [2.0, 3.0]]),
]
for name, vecs in cases:
    rel = dependent_relation(vecs)
    rel_text = "none (independent)" if rel is None else str([round(x, 4) for x in rel])
    print(f"{name:26s} independent: {is_independent(vecs)!s:5s} relation c = {rel_text}")

print()
print("Reading a relation. Take {[1,0], [0,1], [1,1]}: the coefficients are")
print("[-1, -1, 1], meaning -1*[1,0] - 1*[0,1] + 1*[1,1] = [0, 0]. Verify:")
vecs = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
rel = dependent_relation(vecs)
total = [sum(rel[j] * vecs[j][i] for j in range(len(vecs))) for i in range(2)]
print(f"  c = {[round(x, 4) for x in rel]}")
print(f"  c1*v1 = {round(rel[0], 4)} * [1, 0] = {[round(rel[0] * 1.0, 4), 0.0]}")
print(f"  c2*v2 = {round(rel[1], 4)} * [0, 1] = [0.0, {round(rel[1] * 1.0, 4)}]")
print(f"  c3*v3 = {round(rel[2], 4)} * [1, 1] = {[round(rel[2] * 1.0, 4), round(rel[2] * 1.0, 4)]}")
print(f"  sum   = {total}")

print()
print("=== More vectors than dimensions can never be independent ===")
four_in_r4 = [
    [float(((i * 7 + j * 3) % 5) - 2) for j in range(4)] for i in range(4)
]
print(f"4 vectors in R^4: {[[round(x, 1) for x in v] for v in four_in_r4]}")
print(f"independent: {is_independent(four_in_r4)}")
five = four_in_r4 + [[1.0, -1.0, 1.0, -1.0]]
print(f"independent after adding a 5th: {is_independent(five)}  (never possible)")

print()

random.seed(7)
dependent_trials = 0
trials = 500
for _ in range(trials):
    vs = [[float(random.randint(-3, 3)) for _ in range(3)] for _ in range(4)]
    if not is_independent(vs):
        dependent_trials += 1
print(f"Random 4 vectors in R^3, {trials} trials: {dependent_trials} dependent.")
print("Four vectors cannot be independent in three dimensions, so this must be")
print(f"{trials}. If it is not, the routine is wrong.")
```

### Subspaces and the subspace test

A subspace is a set of vectors that cannot be left by adding and scaling. Three
checks, and nothing else.

```python
# Subspaces: collections of vectors closed under the two allowed operations.
# The subspace test is only three checks:
#   1. the zero vector is in the set
#   2. u in the set and scalar c  =>  c*u in the set
#   3. u, v in the set             =>  u + v in the set
# Failing any one of them means the set is not a subspace.

TOL = 1e-9


def vadd(u, v):
    return [a + b for a, b in zip(u, v)]


def vscale(c, u):
    return [c * a for a in u]


# Each candidate set is written as a predicate: "is this vector in the set?"
# That is exactly how you would implement it in code, and it describes the whole
# infinite set, not just the samples we test.
def subspace_test(name, predicate, samples):
    """Check the three closure conditions using a finite list of probe vectors."""
    dim = len(samples[0])
    has_zero = predicate([0.0] * dim)

    members = [u for u in samples if predicate(u)]

    scalar_ok = True
    for u in members:
        for c in (2.0, -1.0, 0.5):
            if not predicate(vscale(c, u)):
                scalar_ok = False

    add_ok = True
    for u in members:
        for v in members:
            if not predicate(vadd(u, v)):
                add_ok = False

    ok = has_zero and scalar_ok and add_ok
    print(f"{name:36s} zero={str(has_zero):5s} scalar={str(scalar_ok):5s} "
          f"add={str(add_ok):5s} -> {'SUBSPACE' if ok else 'not a subspace'}")
    return ok


# Probe vectors. A finite sample can never prove a subspace exists, but it can
# catch a set that definitely is not one.
samples = [
    [1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [2.0, -2.0],
    [-3.0, 3.0], [0.5, -0.5], [0.0, 0.0],
]

print("=== Candidate subsets of R^2 ===")
subspace_test("x + y == 0 (line through origin)",
              lambda v: abs(v[0] + v[1]) < TOL, samples)
subspace_test("x + y == 1 (line not through origin)",
              lambda v: abs(v[0] + v[1] - 1.0) < TOL, samples)
subspace_test("x * y == 0 (the two axes together)",
              lambda v: abs(v[0] * v[1]) < TOL, samples)
subspace_test("x == 0 (the y-axis)",
              lambda v: abs(v[0]) < TOL, samples)
subspace_test("x^2 + y^2 == 1 (unit circle)",
              lambda v: abs(v[0] ** 2 + v[1] ** 2 - 1.0) < TOL, samples)
subspace_test("x == 0 or y == 0 (axes)",
              lambda v: abs(v[0]) < TOL or abs(v[1]) < TOL, samples)

print()
print("Why the failures fail, in plain words:")
print("  x + y == 1: the zero vector [0, 0] does not satisfy it, so the set")
print("    cannot contain zero. A set with no zero can never be a subspace.")
print("  x * y == 0: [1, 0] and [0, 1] are both in it, but their sum [1, 1] is")
print("    not, because 1 * 1 = 1. Two lines crossing make a cross, not a plane.")

print()
print("=== The same three rules over GF(2), where the scalars are 0 and 1 ===")
# GF(2) is arithmetic mod 2: addition is XOR and negative numbers do not exist.
# Bit strings are vectors over GF(2), which is the setting of every error
# correcting code and every hash checksum.


def gf2_add(u, v):
    return [a ^ b for a, b in zip(u, v)]  # XOR is addition mod 2


def gf2_subspace_test(name, predicate, probes):
    has_zero = predicate([0] * len(probes[0]))
    members = [p for p in probes if predicate(p)]
    scalar_ok = all(predicate(vscale(c, m)) for m in members for c in (0, 1))
    add_ok = all(predicate(gf2_add(u, v)) for u in members for v in members)
    ok = has_zero and scalar_ok and add_ok
    print(f"{name:36s} zero={str(has_zero):5s} scalar={str(scalar_ok):5s} "
          f"add={str(add_ok):5s} -> {'SUBSPACE' if ok else 'not a subspace'}")
    return ok


bit_probes = [
    [0, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [1, 1, 0, 0],
    [0, 0, 1, 0], [1, 1, 1, 1], [1, 0, 1, 0], [0, 1, 1, 1],
]
gf2_subspace_test("even number of 1 bits (weight)",
                  lambda v: sum(v) % 2 == 0, bit_probes)
gf2_subspace_test("first two bits are equal",
                  lambda v: v[0] == v[1], bit_probes)
gf2_subspace_test("all bits equal",
                  lambda v: all(b == v[0] for b in v), bit_probes)
gf2_subspace_test("first bit is 1",
                  lambda v: v[0] == 1, bit_probes)

print()
print("The even-weight set is the smallest useful linear code: a subspace of")
print("GF(2)^4 with 3 degrees of freedom, so it holds 2^3 = 8 codewords out of")
print("2^4 = 16 possible 4-bit words. Printed from the 3 free bits plus a parity bit:")
for c0 in (0, 1):
    for c1 in (0, 1):
        for c2 in (0, 1):
            parity = (c0 + c1 + c2) % 2
            word = [c0, c1, c2, parity]
            check = f"{sum(word) % 2 == 0}"
            print(f"  {''.join(map(str, word))}   even weight: {check}")
```

### With Libraries

Everything above was plain Python lists. numpy runs the same arithmetic in
compiled code and ships the vector-space routines we hand-rolled. None of it is
magic; it is the same mathematics with a faster implementation.

```python
# Everything above was plain Python lists. numpy does the same arithmetic in
# compiled code, and adds the vector-space routines (dot, norm, rank, solve,
# least squares) that we hand-rolled. Nothing here is magic; it is the maths
# from the previous sections with a faster implementation.

import numpy as np

e1 = np.array([1.0, 0.0, 0.0])
e2 = np.array([0.0, 1.0, 0.0])
e3 = np.array([0.0, 0.0, 1.0])

print("=== The same arithmetic, one line each ===")
u = np.array([1.0, 2.0, 3.0])
w = np.array([0.0, 1.0, 4.0])
print(f"4*u - w           = {4.0 * u - w}")
print(f"np.dot(u, w)      = {np.dot(u, w)}")
print(f"u @ w             = {u @ w}   (@ is matrix multiply, dot for 1-D arrays)")
print(f"np.linalg.norm(u) = {np.linalg.norm(u):.4f}")
cosine = np.dot(u, w) / (np.linalg.norm(u) * np.linalg.norm(w))
print(f"cosine(u, w)      = {cosine:.4f}")

print()
print("=== Rank as a dependence test ===")
# np.linalg.matrix_rank runs the same row reduction we wrote by hand above.
independent = np.array([e1, e2, e3])
dependent = np.array([e1, e2, e1 + e2])
print(f"rank([e1, e2, e3])     = {np.linalg.matrix_rank(independent)}")
print(f"rank([e1, e2, e1 + e2]) = {np.linalg.matrix_rank(dependent)}")

print()
print("=== Coefficients of a linear combination ===")
# Generators go in as COLUMNS, so A c = target.
A = np.array([e1, e2, e3]).T
target = np.array([4.0, -1.0, 2.0])
coeffs = np.linalg.solve(A, target)
print(f"A (columns = generators) =\n{A}")
print(f"target   = {target}")
print(f"coeffs c = {coeffs}")
print(f"rebuilt  = {A @ coeffs}")
print(f"matches: {np.allclose(A @ coeffs, target)}")

print()
print("=== Least squares when the target is outside the span ===")
flat_A = np.array([e1, e2, e1 + e2]).T
unreachable = np.array([4.0, -1.0, 5.0])
c_ls, _, rank, _ = np.linalg.lstsq(flat_A, unreachable, rcond=None)
fit = flat_A @ c_ls
print(f"flat_A (columns) =\n{flat_A}")
print(f"target   = {unreachable}")
print(f"rank     = {rank}  (only two independent directions)")
print(f"coeffs   = {c_ls}")
print(f"fit      = {fit}   (third component forced to 0)")
residual = unreachable - fit
print(f"residual = {residual}")
print(f"sum of squared residuals = {float(np.sum(residual ** 2)):.4f}")

print()
print("=== Why a data point is a vector ===")
# Each row is one observation, each column one feature. Row operations on this
# table are exactly the vector operations of the previous sections, applied to
# every row at once.
data = np.array([
    [170.0, 70.0, 30.0],
    [160.0, 55.0, 28.0],
    [185.0, 90.0, 45.0],
    [150.0, 60.0, 22.0],
])
means = data.mean(axis=0)
centered = data - means
print(f"data =\n{data}")
print(f"column means       = {means}")
print(f"centered =\n{centered}")
print(f"new column means   = {centered.mean(axis=0)}")
print("Centring is one scalar multiplication and one addition applied to every")
print("row, using the fixed vector of column means:")
print(f"  row + (-1) * mean_vector, applied to all rows: {np.allclose(centered, data - means)}")

# Standardisation rescales each column too: divide by the standard deviation,
# which is another per-column scalar. Both steps are vector-space operations.
stds = data.std(axis=0)
standardized = centered / stds
print()
print(f"column std devs    = {stds}")
print(f"standardized =\n{standardized}")
print(f"new column means   = {standardized.mean(axis=0)}")
print(f"new column stds    = {standardized.std(axis=0)}")

# The distance between two rows is one norm. Nearest-neighbour search is
# "compute many norms, take the smallest".
d_bob_sue = np.linalg.norm(data[0] - data[1])
d_bob_max = np.linalg.norm(data[0] - data[2])
print()
print(f"distance bob to sue (rows 0,1) = {d_bob_sue:.4f}")
print(f"distance bob to max (rows 0,2) = {d_bob_max:.4f}")
print("a row scaled to unit length by dividing by its norm:")
print(f"  bob / ||bob|| = {data[0] / np.linalg.norm(data[0])}")
```

## Common Mistakes

**Mistake 1: treating vectors as points and forgetting they can be subtracted.**
The wrong version: `bob - sue` is "the house that is neither bob nor sue". The
right version: `bob - sue` is a *direction*, the displacement from sue to bob,
and it is a legitimate vector independent of where either one lives. Gradient
descent moves along `bob - sue`, not toward either point.

**Mistake 2: assuming `m` vectors in `ℝⁿ` are independent when `m ≤ n`.**
The wrong version: "three vectors in three dimensions, so they must be a basis."
The right version: counting only rules out dependence when `m > n`. Three vectors
in `ℝ³` can be dependent — the worked example above has exactly that, with a
cancelling combination. You must actually row reduce.

**Mistake 3: calling the circle or a line not through the origin a subspace.**
The wrong version: "a subspace is any set defined by an equation." The right
version: a subspace must contain the zero vector and must be flat. `x² + y² = 1`
and `x + y = 1` both fail the zero-vector check. Any subspace passes through the
origin — if your set does not, it is an *affine* subspace, useful in regression
but not a vector space.

**Mistake 4: putting generators in rows when you meant columns.**
The wrong version: "span works the same either way." The right version: the
coefficients `c` must multiply the *columns* of `A` to give the target, because
`A c` is a sum of scaled columns. If you build `A` with the generators as rows,
you are solving the wrong system. The set you get is the row space, which for a
square matrix happens to match, which is exactly why this bug survives testing.

**Mistake 5: comparing vectors of different scales by dot product alone.**
The wrong version: ranking documents by raw dot product when one document is ten
times longer than another, so it wins every query. The right version: cosine
similarity, `dot(a, b) / (norm(a) * norm(b))`, divides out the length and leaves
only the direction. This is why every retrieval system normalises first.

---

## Formula Sheet

Every symbol and formula this lesson introduces, in one place. `F` is the field of
scalars (here `ℝ`, `ℂ`, or `GF(2)`); `u, v, w ∈ Fⁿ` are `n`-component vectors;
`a_{ij}` is the entry in row `i`, column `j` of a matrix whose **columns** are the
listed vectors, so `A` is `n × k`.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `u + v` | `$(u+v)_i = u_i + v_i$` | Add matching components. Requires `u, v` to have the same length. | Combining two measurements, or the add step of one optimiser step |
| `c \cdot u` | `$(cu)_i = c\,u_i$` | Multiply every component by the one number `c ∈ F`. | Rescaling; `c = -1` reverses a direction |
| `-u` | `$-u = (-1) \cdot u$` | Point the opposite way, same length. | Turning two data points into a displacement |
| `0` | `$\mathbf{0} = (0, \dots, 0)$ | The zero vector: the additive identity, at the origin. | Any subspace must contain it; any dependence relation sums to it |
| `u \cdot v` | `u \cdot v = \sum_{i=1}^{n} u_i v_i$` | Multiply matching components and add. Zero means the two point at right angles. | Perpendicularity test, projection, ranking documents |
| `\|u\|` | `$\|u\| = \sqrt{u \cdot u}$` | The Euclidean length of `u`. Always `≥ 0`, and `= 0` only for `u = 0`. | Distances, normalising a vector to unit length |
| `$\cos\theta$` | `$\cos\theta = \dfrac{u \cdot v}{\|u\|\,v\|} \in [-1, 1]}$` | How closely two vectors point the same way, ignoring length. | Cosine similarity; comparing text of different lengths |
| Linear combination | `$\sum_{i=1}^{k} c_i v_i$`, `c_i ∈ F` | A weighted sum: scale each vector, then add. | The only way this lesson builds new vectors |
| `$\operatorname{span}(S)$` | `$\operatorname{span}(S) = \left\{ \sum_{i=1}^{k} c_i v_i : v_i \in S,\ c_i \in F \right\}$` | Everything reachable from the origin by scaling and adding members of `S`. Always contains `0` and is always a subspace. | "What can this data represent?" |
| `$\operatorname{span}(\emptyset)$` | `$\{\mathbf{0}\}$` | The empty set spans only the origin — the one zero-dimensional space. | Edge case in "drop all dependent vectors" |
| Independence test | `$\sum_{i=1}^{k} c_i v_i = \mathbf{0} \ \Rightarrow\ c_1 = \dots = c_k = 0$` | No nonzero choice of weights cancels to zero. Equivalently: no vector is a combination of the others. | Deciding what to keep and what to delete |
| Dependence | `$\exists\ (c_1,\dots,c_k) \ne 0$ with `$\sum_i c_i v_i = \mathbf{0}$` | The vectors cancel each other out; at least one is redundant. | Reported by `dependent_relation` as a witness |
| Dimension counting | `k > n \Rightarrow \{v_1,\dots,v_k\} \subseteq F^n$ is dependent` | More vectors than dimensions *always* means redundancy. Valid for `k > n` only. | A free argument that never needs a computation |
| `$\dim(V)$` | `$\dim(\mathbb{R}^n) = n$; generally `$\dim(V) = $` size of any basis of `V` | How many independent directions the space has. Basis-independent, so any two bases agree. | "How many real factors are in this data?" |
| Independent ⇔ spanning dimension | `$\{v_1,\dots,v_k\}$ independent $\iff \dim(\operatorname{span}\{v_1,\dots,v_k\}) = k$` | A set is independent exactly when it is already a basis of its own span. | Deciding whether a basis needs extending |
| Subspace test | `W` nonempty, and `$\mathbf{0} \in W$`, `c \in F, u \in W \Rightarrow cu \in W$`, `u, v \in W \Rightarrow u+v \in W$` | Three checks, nothing else. `W ⊆ V` is a subspace iff all three hold. | The most-used test in applied linear algebra |
| Homogeneous description | `$W = \{x \in \mathbb{R}^n : p_1 x_1 + \dots + p_n x_n = 0\}` | Any set cut out by *homogeneous* linear equations (no constant term). | The quickest way to recognise a subspace |
| Affine set | `$\{x \in \mathbb{R}^n : p_1x_1 + \dots + p_nx_n = b\},\ b \ne 0$` | Parallel to a subspace but shifted off the origin; **not** a subspace. | Regression without an intercept |
| `A c = 0` (null space test) | `$A \in \mathbb{R}^{n \times k}$, `$\sum_{i=1}^{n} c_i v_i = 0 \iff A c = \mathbf{0}$` | Put the vectors in the **columns** of `A`; a nonzero null vector *is* the cancelling relation. | The mechanical independence test |
| RREF pivot count | `$\{v_i\}$ independent $\iff$ ` `$\operatorname{rref}(A)$` has a pivot in every one of its `k` columns | Each pivot column is one vector that cannot be built from the others. | What `is_independent` counts |
| Least squares | `$\hat c = \arg\min_c \|A c - t\|^2$`, `$\hat y = A\hat c$` | The reachable point closest to the target. Not unique when `A` has dependent columns. | Fitting a model whose columns are collinear |
| Orthogonality of the residual | `$(t - A\hat c) \cdot v_i = 0$ for every `i` | The leftover error points in a direction no generator reaches. | Why least squares works; why the residual is diagnostic |
| GF(2) addition | `$u \oplus v$`, componentwise, `a + b \bmod 2` | XOR. There is no subtraction, and `-1 = 1`. | Parity bits, checksums, error-correcting codes |
| `$\|W\|$` for a GF(2) subspace | `$\|W\| = 2^{\dim W}$` | A `k`-dimensional space over two scalars has `2^k` points — one per free bit. | Sizing a linear code without enumerating it |
| Centred data | `$x - \mu$`, `$\mu$` the column mean | Subtract the mean vector from every row: scaling by `-1` then adding. | PCA, correlation, before any rank analysis |
| Standardised data | `$(x - \mu)/\sigma$`, `$\sigma$` the column std. dev. | Centre, then rescale each column to unit spread. | Comparing features with different units |

## Multiple Choice Questions

**Q1.** Which of these subsets of `ℝ³` is a subspace?

- A) `{(x, y, z) : x + y + z = 1}`
- B) `{(x, y, z) : x·y·z = 0}`
- C) `{(x, y, z) : x = y}`
- D) `{(x, y, z) : x² + y² + z² = 1}`

<details>
<summary>Answer and explanation</summary>

**C) `{(x, y, z) : x = y}`.**

This is a *homogeneous* linear equation — no constant term — so scaling preserves
it and adding two such triples gives another such triple; `(0,0,0)` satisfies it.

- A) fails the zero-vector check immediately: `0 + 0 + 0 = 0 ≠ 1`. A set with no
  zero vector can never be a subspace, however well it behaves under addition.
- B) *does* contain `(0,0,0)` and *is* closed under scaling, which is why it looks
  right. It fails addition: `(1,2,0)` and `(0,0,7)` are both in it, but their sum
  is `(1,2,7)`, and `1·2·7 = 14 ≠ 0`. It is the union of three coordinate planes,
  and a union of flats is not a flat.
- D) fails twice over: `(0,0,0)` is not on the unit sphere, and `(1,0,0)` plus
  `(0,1,0)` gives `(1,1,0)`, which is also not on it.

</details>

**Q2.** In the worked example, `H3 = H1 + H2`. Which statement about
`{H1, H2, H3}` is guaranteed?

- A) It is a basis of `ℝ³`, because it has exactly three vectors
- B) It is linearly dependent, and its span has dimension 2
- C) It is linearly independent, because `H3` is a combination of the other two
- D) Its span is the line through `H1` and `H2`

<details>
<summary>Answer and explanation</summary>

**B) It is linearly dependent, and its span has dimension 2.**

The relation `-1·H1 - 1·H2 + 1·H3 = 0` has a nonzero coefficient, so the set is
dependent — the worked example checks it component by component
(`-80 - 120 + 200 = 0`, `-3 - 4 + 7 = 0`, `-10 - 25 + 35 = 0`).

The span is `span(H1, H2)`, which is `span(H1, H2, H3)` since `H3` adds nothing.
`H1` and `H2` are independent — the ratio of areas is `80/120 = 2/3` but the
ratio of rooms is `3/4`, so no single scalar turns one into the other — hence the
span has dimension 2, the plane `-7x + 160y + 8z = 0`.

- A) and C) are the two halves of the classic mistake in Mistake 2. Having `n`
  vectors in `n` dimensions guarantees *at most* that they span; it says nothing
  about independence, and the counterexample is sitting in the lesson.
- C) is also internally backwards: a vector being a combination of the others is
  the *definition* of redundancy, not evidence of independence.
- D) is wrong because a span of two independent vectors is a plane, not a line.
  A line is what a *single* generator produces.

</details>

**Q3.** `is_independent` is run on 500 random sets of four vectors in `ℝ³`, and
reports dependent 500 times. Is the routine broken?

- A) Yes — four vectors in three dimensions should be independent at least some of
  the time, so a 100% failure rate is suspicious
- B) Yes — the routine should have reported exactly 250 dependent and 250
  independent, since independence and dependence are equally likely
- C) No — four vectors in `ℝ³` can never be independent, so 500 out of 500 is the
  only outcome a correct routine can produce
- D) No — but only because 500 is a round number and the seed is fixed, so the
  agreement proves nothing

<details>
<summary>Answer and explanation</summary>

**C) No — four vectors in `ℝ³` can never be independent, so 500 out of 500 is the
only outcome a correct routine can produce.**

This is the `k > n` theorem from the Formal Version, applied to the code: the
lesson states it as a *specification* — "Four vectors cannot be independent in
three dimensions, so this must be 500. If it is not, the routine is wrong." A
routine that ever reported `True` here would be the thing under suspicion.

- A) and B) both assume the two outcomes are equiprobable, which they are not.
  Dependence here is not a coin flip; it is a certainty. Random sampling is the
  wrong tool for testing a counting argument.
- B) invents a `250/250` split that no mathematics supports.
- D) confuses "the answer is right" with "the check is informative". The fixed
  seed and round number are irrelevant; the 500/500 agreement is a genuine
  confirmation because the prediction `500` was forced in advance.

</details>

**Q4.** The lesson finds `span(H1, H2) = { -7x + 160y + 8z = 0 }`. Why is
`(0, 0, 1)` not in that span?

- A) Its coordinates are not integers, so no integer combination of `H1` and `H2`
  can produce it
- B) It fails the plane equation — it evaluates to `8 ≠ 0` — and every linear
  combination of `H1` and `H2` satisfies that equation exactly
- C) Two generators in `ℝ³` can only reach two points, and `(0,0,1)` is not one of
  the generators
- D) It is not a scalar multiple of the normal vector `(-7, 160, 8)`, and nothing
  in the span needs to be

<details>
<summary>Answer and explanation</summary>

**B) It fails the plane equation — it evaluates to `8 ≠ 0` — and every linear
combination of `H1` and `H2` satisfies that equation exactly.**

The normal `p = (-7, 160, 8)` was constructed with `p·H1 = p·H2 = 0`, and the dot
product is bilinear, so `p·(a·H1 + b·H2) = a(p·H1) + b(p·H2) = 0` for all `a, b`.
For `t = (0,0,1)`, `p·t = -7(0) + 160(0) + 8(1) = 8`. Contradiction, so no `a, b`
exist. The lesson is explicit that this is "a structural fact, not a
computational failure".

- A) is wrong because the coefficients are in `F = ℝ`, not `ℤ`. `H1` and `H2` are
  already integer vectors, and the question is whether some *real* pair works.
  This is exactly the "why a field, not the integers" issue.
- C) is nonsense numerically: a single generator reaches an infinite line, so two
  independent generators reach an infinite plane. Reaching "two points" is what a
  set with *one* independent vector cannot do.
- D) is true but irrelevant. Reachability is about being a combination of the
  generators, not about being related to the normal; the normal is a certificate
  of exclusion, not a target.

</details>

**Q5.** The subspace test is stated for a **nonempty** `W ⊆ V`. Why must
nonemptiness be part of the statement rather than a side remark?

- A) Because the empty set is not closed under scaling, since there is nothing to
  scale
- B) Because "contains the zero vector" already implies nonemptiness, so adding
  the hypothesis would be redundant
- C) Because closure under addition of the empty set is undefined, and a theorem
  with an undefined case can be neither proved nor used
- D) Because every vector space must be finite

<details>
<summary>Answer and explanation</summary>

**C) Because closure under addition of the empty set is undefined, and a theorem
with an undefined case can be neither proved nor used.**

The statement is a biconditional: "`W` is a subspace **if and only if** these
three conditions hold." The reverse direction is the delicate one — it must show
that the three conditions *imply* the eight vector-space axioms. That proof picks
`u, v ∈ W` and reasons about `u + v`, which is only meaningful if such `u, v`
exist. Without the nonemptiness hypothesis, `∅` vacuously satisfies the closure
sentences and would have to be declared a subspace.

- A) is not a real objection. "Closed under addition" means *if* `u, v ∈ W` *then*
  `u + v ∈ W`; over an empty `W` that sentence is vacuously true, which is
  precisely the problem.
- B) would be right if the theorem did not also need `u, v` for the addition
  closure, but condition 1 guarantees nonemptiness *for the reader's benefit*,
  not for the statement's — the statement has to be well formed before any
  condition is used.
- D) is false as mathematics: `ℝⁿ` and any GF(2) space of any size are all
  vector spaces, finite and infinite.

</details>

**Q6.** To test whether the target `t` lies in `span(g1, g2, g3)`, which matrix
should you hand to the solver?

- A) The matrix whose **rows** are `g1, g2, g3`
- B) The matrix whose **columns** are `g1, g2, g3`
- C) Either one, because the set of reachable points is the same either way
- D) The `3 × 3` identity, since the coefficients are all that is being solved for

<details>
<summary>Answer and explanation</summary>

**B) The matrix whose **columns** are `g1, g2, g3`.**

`A c` *is* the sum of scaled columns: `A c = c1·g1 + c2·g2 + c3·g3`. So the
coefficients multiply the columns, and the generators must be the columns. The
lesson's `as_columns` helper does precisely this transpose-by-hand.

- A) with the generators as rows solves for coefficients in the *row space*, a
  different set. This is Mistake 4 in the Common Mistakes section.
- C) is the trap that makes the bug survive testing: for a **square** matrix the
  row space and column space happen to be the same set, so the bug is invisible
  on small square examples and appears the moment the generators are not
  `n × n` or not the same length.
- D) solves `c = 0` (well, `c =` the target read as a vector) and has nothing to
  do with `g1, g2, g3`. If you find yourself building an identity you have lost
  the generators.

</details>

**Q7.** The vectors `bob = (170, 70, 30)` and `sue = (160, 55, 28)` give
`bob · sue = 31890` and `cos(bob, sue) = 0.9983`. A third vector `long_doc` has
exactly the same direction as `bob` but is scaled by 10. Which quantity changes?

- A) The cosine similarity, because the longer vector has more components to
  contribute to the dot product
- B) The cosine similarity, because any change to one of the vectors changes the
  angle between them
- C) Neither the dot product nor the cosine changes
- D) Only the norm changes; the dot product and the cosine are both unchanged

<details>
<summary>Answer and explanation</summary>

**D) Only the norm changes; the dot product and the cosine are both unchanged.**

Scaling one vector by a constant `c` multiplies its norm by `|c|` and its dot
product with anything by `c`, so

`$\cos(10u, v) = \dfrac{(10u)\cdot v}{\|10u\|\,\|v\|} = \dfrac{10(u\cdot v)}{10\|u\|\,\|v\|} = \cos(u, v)$`.

The angle between two directions does not depend on how long the arrows are, so
the cosine stays `0.9983` and the dot product becomes `318900`.

- A) confuses the dot product (which does scale, by 10) with the cosine (which
  divides that scale straight back out).
- B) is the misconception: it treats a vector as a point. Scaling is a *length*
  change, not a *direction* change, and an angle is purely a direction quantity.
  This is why the whole retrieval pipeline normalises documents before ranking.
- C) is wrong about the dot product, which is bilinear and therefore does scale:
  `31890 → 318900`. Only the cosine is scale-invariant.

</details>

**Q8.** The set of 4-bit strings with an even number of 1s is a subspace of
`GF(2)⁴` with 3 degrees of freedom. How many elements does it contain?

- A) 2, because a subspace must contain the zero vector and at least one other
  point
- B) 4, because even weight forces the last bit to be determined by the first
  three
- C) 8, because each of the 3 free bits can independently be 0 or 1
- D) 16, because every 4-bit string has an even number of 1s somewhere in it

<details>
<summary>Answer and explanation</summary>

**C) 8, because each of the 3 free bits can independently be 0 or 1.**

The rule "the weight is even" fixes the **parity bit** from the other three, so
three bits are free and one is determined: `2³ = 8`. The code prints exactly the
eight words `0000, 0011, 0101, 0110, 1001, 1010, 1100, 1111`, and the general
rule is `|W| = 2^dim(W)` for any subspace of a space over two scalars.

- A) and B) undercount. `2` is the count for a 1-dimensional subspace and `4` for
  a 2-dimensional one; the dimension here is 3, and the lesson's own brute-force
  loop `for c0 in (0,1): for c1 in (0,1): for c2 in (0,1)` makes the `2³` structure
  explicit.
- B) is a subtle and instructive error: the parity rule pins the *fourth* bit from
  the first three, not the last from the first. Fixing one bit from three others
  always leaves three free.
- D) is simply false — `0001` has weight 1, and the loop's own printed output
  never lists it.

</details>

**Q9.** `is_independent` puts the vectors in the columns of `A`, row reduces, and
returns `True` exactly when there is a pivot in every column. Why is *pivot per
column* the right criterion?

- A) Because row reduction preserves the row space but is allowed to change the
  column space, so the columns must be checked some other way
- B) Because row operations preserve linear dependence relations among the columns,
  and a column with no pivot is precisely a vector buildable from the ones with
  pivots
- C) Because Python stores lists of numbers column-major, so the routine has to
  match
- D) Because the null space is a subspace of the row space, so it can only be read
  off the pivots of the rows

<details>
<summary>Answer and explanation</summary>

**B) Because row operations preserve linear dependence relations among the
columns, and a column with no pivot is precisely a vector buildable from the ones
with pivots.**

Row operations are invertible, so if `A c = 0` has a nonzero solution then
`rref(A) c = 0` has one too, and a free variable in `rref(A)` reads the relation
straight off the reduced rows — that is exactly what `dependent_relation` does
when it sets `c_vec[free] = 1` and copies `-M[row_index][free]` into the pivot
entries. If all `k` columns get pivots, there is no free variable, so `c = 0` is
the only solution.

- A) reverses the truth. Row reduction **does** preserve linear dependence among
  the columns, which is the whole reason the algorithm is valid. (It preserves
  the column *space* as well.)
- C) is a plausible-sounding non-reason; the orientation is forced by the
  mathematics, not by the storage layout. Getting it "wrong by accident" is
  exactly Mistake 4.
- D) is backwards on two counts: the null space is a subspace of `F^k`, indexed by
  *columns* not rows, and `ker(A)` is emphatically not the row space.

</details>

**Q10.** With generators `e1, e2, e1+e2` and target `(4, -1, 5)`, what does
`np.linalg.lstsq` return, and what is the residual?

- A) `None`, because no exact solution exists, and a residual of 0
- B) Coefficients of a best fit and a nonzero residual, whose third component is
  5, because no combination of the generators can produce a nonzero third
  component
- C) Coefficients of a best fit and a zero residual, because least squares always
  fits the target exactly
- D) A pseudoinverse of `A` and a residual of 0, because a least-squares solution
  is by definition a solution

<details>
<summary>Answer and explanation</summary>

**B) Coefficients of a best fit and a nonzero residual, whose third component is
5, because no combination of the generators can produce a nonzero third
component.**

All three generators have third component 0, so the fitted point is
`(4, -1, 0)` and the residual is `(0, 0, 5)` with squared length 25. The
residual is perpendicular to every generator, which is the certificate that no
better fit exists.

- A) mixes up two different functions. `None` is what the lesson's own
  `solve_consistent` returns for the exact solve; `lstsq` is specifically the
  routine that answers the question you asked when the exact answer is
  unavailable. Reporting 0 as the residual alongside `None` is also
  self-contradictory.
- C) describes the opposite of what least squares does. It returns the *closest
  reachable* point, and a nonzero residual is the honest report that the target
  has a component the model cannot express.
- D) is the deepest confusion: "least-squares solution" refers to minimising
  `‖A c − t‖²`, not to being an exact solution of `A c = t`. `lstsq` does use
  a least-squares/pseudoinverse route internally, but it returns a `fit` and a
  `residual` precisely so you can see how far off it is.

</details>

**Q11.** Two different sets both span the same subspace `W` of `ℝ⁴`: one has two
vectors, the other has three. What must be true?

- A) The three-vector set must contain a vector outside `W`, since it is larger
- B) The two-vector set is independent, the three-vector set is dependent, and
  both spans have dimension 2
- C) The three-vector set must be independent, because three vectors in four
  dimensions cannot be dependent
- D) The two spans have different dimensions, differing by the one extra vector

<details>
<summary>Answer and explanation</summary>

**B) The two-vector set is independent, the three-vector set is dependent, and
both spans have dimension 2.**

If the two-vector set were dependent, its span would be one-dimensional, and a
one-dimensional space cannot be spanned by three independent vectors — so it must
be independent and `dim(W) = 2`. A third spanning vector is then redundant by
definition, and `|W| = 2` is basis-independent: `dim` is one of the few
quantities that genuinely does not depend on which spanning set you picked.

- A) is impossible: `span` is closed under taking linear combinations, so any
  combination of vectors in `W` is in `W`. Adding a generator can never escape
  the set, which is why it can never extend the span either.
- C) applies the `k > n` theorem with the numbers the wrong way round. `3 ≤ 4`
  means counting is *silent* — the theorem only fires when `k > n`. Whether three
  vectors in `ℝ⁴` are dependent is decided by the actual numbers, not the
  count.
- D) is the misconception the whole part exists to kill. Dimension is a property
  of the *set*, not of the description. `span(H1, H2) = span(H1, H2, H3)` in the
  worked example, and both have dimension 2.

</details>

**Q12.** Why must the scalars come from a *field* such as `ℝ`, `ℂ`, or `GF(2)`,
rather than from the integers `ℤ`?

- A) Because `ℤ` is infinite, and vector spaces are required to be finite
- B) Because `ℤ` has no multiplicative identity, and a space needs an element `1`
  acting as `1·u = u`
- C) Because over `ℤ` you cannot always divide by a nonzero integer, so
  normalising coefficients is impossible — `ℤ²` has no basis containing
  `(1,0)` and `(0,1/2)`
- D) Because `ℤ` is not closed under addition, so vectors in `ℤⁿ` could sum to
  something outside `ℤⁿ`

<details>
<summary>Answer and explanation</summary>

**C) Because over `ℤ` you cannot always divide by a nonzero integer, so
normalising coefficients is impossible — `ℤ²` has no basis containing
`(1,0)` and `(0,1/2)`.**

The lesson defines `F` as "a set of numbers where addition, subtraction,
multiplication, **and division by nonzero elements** all behave as you expect."
The division clause is the one that rules out `ℤ`. Over `ℤ` the lattice
`ℤ·(1,0) + ℤ·(0,2)` is a proper sublattice of `ℤ²` that cannot be repaired by
any integer rescaling, so rank and independence stop agreeing with the linear
algebra developed in this part. The lesson's worked example leans on exactly
this: `H1`, `H2`, `H3` and the coefficients `-1, -1, 1` are all integers, but the
*plane* they span is a real object, and the point `(0,0,1)` is excluded by real
arithmetic, not integer arithmetic.

- A) is false: `ℝⁿ` is an infinite vector space over an infinite field, and
  nothing in the axioms limits either.
- B) is false: `1 ∈ ℤ` and `1·u = u` holds perfectly well. Identity elements are
  not the problem.
- D) is false: `ℤ` is closed under addition and subtraction, so `ℤⁿ` *is* closed
  under the two operations. The gap is division, and that gap is subtle enough
  to be the real reason `ℤ` is not a field.

</details>

## Subjective Questions

### Short Answer

**Q1. State the subspace test, and say what the "nonempty" hypothesis is doing
there.**

<details>
<summary>Model answer</summary>

A nonempty subset `W ⊆ V` is a subspace if and only if all three hold: (1) the zero
vector is in `W`; (2) for every scalar `c ∈ F` and every `u ∈ W`, the vector
`cu` is in `W`; (3) for every `u, v ∈ W`, the vector `u + v` is in `W`.

The nonemptiness hypothesis is needed so that condition 3 is a statement about an
actual pair of vectors. Without it, `∅` satisfies conditions 2 and 3
*vacuously* — there are no `u, v` to check — and the biconditional would force
the empty set to be declared a subspace, which it is not. Equivalently: the
reverse direction of the theorem has to derive the eight vector-space axioms,
and it cannot do that if there is no `u` to derive them from.

</details>

**Q2. Give the definition of linear independence, and give the one-sentence
operational test for it.**

<details>
<summary>Model answer</summary>

A set `S = {v₁, …, v_k}` is **linearly independent** over `F` if the only choice
of scalars making `c₁v₁ + … + c_kv_k = 0` is `c₁ = … = c_k = 0`. If some other
choice exists, `S` is **linearly dependent**.

The operational test: build the matrix `A` whose columns are the `v_i` and row
reduce it. `S` is independent exactly when `rref(A)` has a pivot in every one of
its `k` columns — equivalently when the homogeneous system `A c = 0` has only
the zero solution. A nonzero solution *is* a cancelling relation, so the solver
can hand it to you as a certificate of which vectors are redundant.

</details>

**Q3. State the `k > n` counting result, and give an example of `k ≤ n` that is
still dependent.**

<details>
<summary>Model answer</summary>

If `S` has `k` vectors in `ℝⁿ` and `k > n`, then `S` is linearly dependent.
Put the vectors in the columns of an `n × k` matrix `A`; the homogeneous system
`A c = 0` then has `k` unknowns and `n` equations with `k > n`, and any
homogeneous system with more unknowns than equations has a nontrivial solution,
which is a dependence relation.

The converse is false, and the lesson's own worked example is the counterexample:
`H1 = (80,3,10)`, `H2 = (120,4,25)`, `H3 = (200,7,35)` are three vectors in `ℝ³`,
so `k = n = 3` and counting says nothing — yet `-H1 - H2 + H3 = 0`, so they are
dependent. A smaller case is `{[1,2], [2,4]}` in `ℝ²`, where the relation
`-2·[1,2] + 1·[2,4] = 0` is detected in Exercise 5.

</details>

**Q4. What is the difference between a subspace and an affine subspace, and why
does the distinction matter when you fit a model?**

<details>
<summary>Model answer</summary>

A **subspace** is a subset that is closed under addition and scalar multiplication
and therefore contains the zero vector: it always passes through the origin. An
**affine subspace** is a translate of one — a set cut out by non-homogeneous
linear equations, `p·x = b` with `b ≠ 0` — which is a flat sitting off the
origin. It is closed under *differences* of its members but not under addition of
them, and it is not a vector space: `(0,0,0)` is not in it.

It matters because a subspace-flavoured constraint always permits the trivial
solution `c = 0` and a prediction of zero. In regression, forcing the fit through
the origin — a subspace constraint — is a real modelling decision: it says
"no offset", it removes one degree of freedom, and it can be badly wrong when
there is a genuine baseline. The lesson's `S2 = {x + y + z = 1}` versus
`S1 = {x + y + z = 0}` is the minimal illustration: identical equations, and
only one of them is a vector space.

</details>

**Q5. In `dependent_relation`, why are the free variable set to `1` rather than
`0`?**

<details>
<summary>Model answer</summary>

Because setting it to `0` recovers the trivial solution. The procedure is: if
there are fewer pivots than columns then at least one column is a non-pivot, and
its coefficient is a free variable of `A c = 0`. Setting the free coefficient to
`0` forces every pivot coefficient to `0` as well, because the reduced rows read
`c_pivot = -M[row][free] · c_free`. That gives `c = 0`, which every homogeneous
system has, and it certifies nothing.

Setting the free coefficient to `1` — any nonzero value would do — forces a
genuinely nonzero vector, and the pivot entries then become the actual
coefficients of the cancelling relation. For `{[1,0], [0,1], [1,1]}` this yields
`c = [-1, -1, 1]`, which the lesson verifies by hand as `-1·[1,0] - 1·[0,1] +
1·[1,1] = [0,0]`. Any nonzero scalar multiple of this vector is an equally valid
relation; the `1` is a choice that makes the output readable, not a fact.

</details>

**Q6. Why does a `k`-dimensional subspace of `GF(2)ⁿ` contain exactly `2^k`
elements, and how is that different from the real case?**

<details>
<summary>Model answer</summary>

Pick a basis of `k` vectors. Every element of the subspace is a *unique* linear
combination of them — unique because the basis is independent. Over `GF(2)` there
are exactly two scalars, `0` and `1`, so each basis vector is either in or out,
giving `2 · 2 · … · 2 = 2^k` combinations, hence `2^k` elements.

Over `ℝ` the same argument gives an *infinite* set, because each coefficient can
be any real number: the count `2^k` is replaced by "continuum", and the
`k`-bit-style information content is lost. This is the reason GF(2) is the
right setting for error-correcting codes — a `k`-dimensional code over two
symbols stores exactly `k` bits of information in an `n`-bit word, and the
lesson's even-weight subspace has `dim = 3`, hence 8 codewords out of 16 possible
4-bit words. The same count appears in Exercise 5's challenge, where two
independent conditions on 4 bits leave 2 free bits and `2² = 4` codewords.

</details>

### Long Answer

**Q1. Why does every subspace pass through the origin, and what would break in a
fitted model if you forced the fit through the origin?**

<details>
<summary>Model answer</summary>

The origin is forced by the axioms, not chosen. Condition 1 of the subspace test
requires `0 ∈ W` outright. Even without that condition, closure under scaling
alone forces it: pick any `u ∈ W`, and take `c = 0`. Then `0·u = 0 ∈ W`. So
"nonempty and closed under scaling" is already enough to place the origin inside
the set. You can see the same thing in the plane description from the worked
example: `span(H1, H2) = { -7x + 160y + 8z = 0 }` is homogeneous, and the
homogeneous part is not decoration — it *is* the origin constraint. A non-zero
right-hand side `b` moves the whole flat off the origin, and the resulting affine
set is no longer closed under addition: two points on the line `x + y = 1` sum to
something with `x + y = 2`.

What breaks in a fitted model is concrete. If you constrain `y = c₁x₁ + c₂x₂`
(a subspace constraint, since the coefficient vector must lie in a subspace of
`ℝ²`) you have removed the intercept, and you have asserted that zero features
predicts zero output. Exercise 4 shows the cost: fitting `price = 3000·area +
50000` from the first two houses gives `slope = 3000.0, intercept = 50000.0`,
which reproduces the 200 m² house as `650000` against an actual `690000` — a
`40000` residual. If instead the true relationship had a genuine baseline (a
house is worth something even with zero floor area, or a sensor reads a nonzero
value at zero input), the origin-constrained fit is not merely less accurate, it
is biased, and no amount of data fixes it. The practical rule: the subspace
constraint is correct exactly when the physics says the zero response is zero,
and that is an assumption to state, not one to inherit by accident. Machine
learning practice encodes it as a choice — scikit-learn's `LinearRegression`
includes an intercept by default and `fit_intercept=False` removes it.

</details>

**Q2. A dataset has 5000 rows and 3 feature columns, and the rank of the centred
data matrix is 2. What does that tell you, what can you safely delete, and what
must you *not* conclude?**

<details>
<summary>Model answer</summary>

Rank 2 means the 5000 rows, viewed as vectors in `ℝ³` after centring, occupy a
2-dimensional subspace. Equivalently, the three feature columns satisfy one
non-trivial linear relation, so one of them is a combination of the other two.
This is a statement about the *columns* surviving row reduction, and the row
count is irrelevant to it — a rank of 2 is the same whether there are 5 rows or
5 million. It also means the data has exactly 2 independent factors, not 3.

What you can safely delete: one of the three columns — after solving `A c = 0` to
find *which* relation, so you delete a member of the dependent set rather than
guessing. You keep the other two, and every row of the dataset is still
represented exactly: `span` is unchanged, which the lesson demonstrates in
Exercise 2 by showing that `[5, -3, 0]` is reachable both with and without the
redundant generator `[1, 1, 0]`, and `[5, -3, 7]` is unreachable in both cases.
Equivalently, drop all dependent columns and the remainder is a basis for
precisely the same set, in strictly less storage. Since centring subtracts the
column means, a *constant* column is the rank-1 case of this: it disappears under
centring, which is why the lesson's numpy section centres before analysing.

What you must **not** conclude:
1. Not that the data "has three features". It has three columns and two degrees
   of freedom; the third column is a derived quantity and may be numerically
   fragile. A column like `height_in_cm` and `height_in_m` is exactly this trap.
2. Not that the two kept columns are "independent in general". Independence is a
   property of the *realised matrix*, not of the schema. Correlated columns can
   produce an exact rank-2 relation in a finite sample by accident, and the
   dependency can disappear the moment new data arrives.
3. Not that rank 2 is "nearly rank 3 and therefore fine". Exact rank 2 is exact:
   there is a whole plane of targets the model provably cannot hit. Any target
   with a component normal to the span gets a residual — Exercise 6 measures one
   of squared length 25.
4. Not that you have lost information by deleting. You have not, for anything
   inside the span; what you lost is the *description* of a redundancy, which is
   precisely the thing you wanted to know.

</details>

**Q3. Why does counting arguments settle dependence but never independence? What
does that tell you about how you should test a real dataset?**

<details>
<summary>Model answer</summary>

Because the counting argument is one-directional. The proof goes: build `A` with
the `k` vectors as columns, write the independence question as `A c = 0`, and
observe that the system has `k` unknowns and `n` equations. If `k > n` then the
system is under-determined, a free variable exists, and `c ≠ 0` is guaranteed.
Every step of that argument is an implication *from* the inequality to dependence.
There is no step that runs backwards: `k ≤ n` leaves you with a square-ish,
possibly full-rank system, and the inequality simply carries no information. That
is why `{[1,0], [0,1], [1,1]}` and `{[1,0], [0,1], [1,2]}` — both three vectors in
`ℝ²` — behave differently while every count agrees, and why the worked example
can have three vectors in `ℝ³` that cancel.

The asymmetry is structural, not a gap waiting to be filled. A counting
argument can only ever produce a *certificate of redundancy*; independence is the
absence of any such relation, and "absence" cannot be established by counting
how many things could exist. You have to check the actual numbers. This is
precisely Mistake 2 in the lesson's Common Mistakes: the wrong version says
"three vectors in three dimensions, so they must be a basis", and the right
version is "counting only rules out dependence when `m > n`; you must actually
row reduce."

The practical consequence is a two-stage policy. Use counting as a free
screen — it is O(1) and it catches the most common and most embarrassing case,
a feature matrix with more columns than rows-plus-one, which is the standard
symptom of an over-parameterised model. Then, for everything the screen does not
decide, run the actual algorithm: `np.linalg.matrix_rank` in numpy, `is_independent`
in the lesson, or the RREF pivot count. And when you want more than a yes/no,
ask for the *witness*, not the verdict. `dependent_relation` does this: it
returns the coefficients `c` with `A c = 0`, so the report is "-1·H1 - 1·H2 +
1·H3 = 0" rather than "dependent". A boolean cannot be acted on; a relation tells
you exactly which column to drop, or which pair to re-collect.

</details>

**Q4. Why does the least-squares residual always come out perpendicular to every
generator, and what would break if you minimised something other than the
distance?**

<details>
<summary>Model answer</summary>

Because the perpendicularity *is* the optimality condition, and it falls out of
one line of algebra. We want to minimise `f(c) = ‖A c − t‖²` over `c`. For
convenience write `c* = c − h` for an arbitrary displacement `h`. Then

`f(c* − h) − f(c*) = ‖A c* − t − A h‖² − ‖A c* − t‖² = −2(A c* − t)·(A h)`

because `‖A h‖²` appears on both sides and cancels. If `r = A c* − t` is the
residual and `r·A h = 0` for all `h`, then `f` is unchanged along every direction
in the space of `c` — which is exactly "at a minimum". Taking `h = e_i` (the
`i`-th standard basis vector of `F^k`) gives `r·a_i = 0`, i.e. the residual is
perpendicular to the `i`-th **column** of `A`, which is the `i`-th generator.
The lesson's Exercise 6 checks this numerically: with generators `e1, e2, e1+e2`
and target `(4, -1, 5)`, the fit is `(4, -1, 0)`, the residual is `(0, 0, 5)`, and
the dot product with all three generators is `0.0000`.

Two things break if you optimise something else. First, if you minimise the
*squared* residual componentwise with a weight that is not constant — a weighted
or regularised objective — the residual is no longer perpendicular to the
generators; it is perpendicular to the *weighted* generators, and the plain
orthogonality check fails even though the solve is correct. This is why the
leverage and residual plots in `statsmodels` OLS are the standard diagnostics
rather than raw residuals. Second, and more seriously, if you minimise the
absolute error `‖A c − t‖` instead of its square, the normal equations do not
hold and there is no `A`-based closed form: you must fall back on an iterative
method (linear programming, or iteratively reweighted least squares). The square
is not an arbitrary convenience; it is the choice that makes the problem smooth
and solvable by row reduction, and it is what `np.linalg.lstsq` and every
`XᵀX` normal-equation solver actually compute.

A final wrinkle worth knowing: the residual is unique, but the *coefficients* are
not, when the generators are dependent. In Exercise 6, `c = (4, -1, 0)` and
`c = (3, -2, 1)` and `c = (6.5, 1.5, -2.5)` all give the identical fit and the
identical residual of squared length 25, because the third generator is a
combination of the first two. So "the least-squares solution" is ambiguous
exactly when the model is redundant — which is a reason to find a basis first
and only then fit.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — express a vector as a combination.** Let `u = [1, 2, 3]`,
`v = [2, -1, 0]` and `w = [5, 0, 3]`. Find scalars `a` and `b` with
`a·u + b·v = w`, verify the answer by hand, and confirm with code.

<details>
<summary>Solution</summary>

By hand, try small integer weights. `1·u + 2·v = [1 + 4, 2 - 2, 3 + 0] = [5, 0, 3]`,
which is `w`. So `a = 1`, `b = 2`.

The code confirms it, using a general solver rather than a guess.

```python
TOL = 1e-9


def solve_consistent(A, b, tol=TOL):
    """Return one solution of A c = b, or None when no solution exists."""
    rows, cols = len(A), len(A[0])
    M = [list(A[i]) + [b[i]] for i in range(rows)]
    pivot_cols = []
    r = 0
    for c in range(cols):
        pivot = None
        for i in range(r, rows):
            if abs(M[i][c]) > tol:
                pivot = i
                break
        if pivot is None:
            continue
        M[r], M[pivot] = M[pivot], M[r]
        for i in range(rows):
            if i != r:
                factor = M[i][c] / M[r][c]
                for j in range(c, cols + 1):
                    M[i][j] -= factor * M[r][j]
        pivot_cols.append(c)
        r += 1
        if r == rows:
            break
    for i in range(len(pivot_cols), rows):
        if abs(M[i][cols]) > tol:
            return None
    x = [0.0] * cols
    for i, c in enumerate(pivot_cols):
        x[c] = M[i][cols] / M[i][c]
    return x


def as_columns(vectors):
    dim = len(vectors[0])
    return [[v[j] for v in vectors] for j in range(dim)]


u = [1.0, 2.0, 3.0]
v = [2.0, -1.0, 0.0]
w = [5.0, 0.0, 3.0]

print(f"u = {u}, v = {v}, w = {w}")
print(f"1*u + 2*v = {[round(u[i] + 2 * v[i], 6) for i in range(3)]}")
print(f"2*u + 1*v = {[round(2 * u[i] + v[i], 6) for i in range(3)]}")

sol = solve_consistent(as_columns([u, v]), w)
print(f"solve a*u + b*v = w gives [a, b] = {sol}")
rebuilt = [round(sol[0] * u[i] + sol[1] * v[i], 6) for i in range(3)]
print(f"a*u + b*v       = {rebuilt}")
print(f"equal to w: {rebuilt == w}")
```

Output:

```
u = [1.0, 2.0, 3.0], v = [2.0, -1.0, 0.0], w = [5.0, 0.0, 3.0]
1*u + 2*v = [5.0, 0.0, 3.0]
2*u + 1*v = [4.0, 3.0, 6.0]
solve a*u + b*v = w gives [a, b] = [1.0, 2.0]
a*u + b*v       = [5.0, 0.0, 3.0]
equal to w: True
```

</details>

**[ ] Exercise 2 — span membership.** Write an `in_span(target, generators)`
function returning `True` or `False`. Test it on: (a) the single generator
`[1, 1]` in `ℝ²` with targets `[5, 5]`, `[30, 3]`, `[-2, -2]`; (b) the
generators `[1, 0]` and `[0, 1]`; (c) the generators `[1, 0, 0]` and
`[0, 1, 0]` in `ℝ³` with the extra target `[4, -1, 2]`. For each case, say in one
sentence why the answer is what it is.

<details>
<summary>Solution</summary>

The test is "does `A c = target` have a solution?", with the generators as the
columns of `A`.

```python
TOL = 1e-9


def solve_consistent(A, b, tol=TOL):
    """Return one solution of A c = b, or None when no solution exists."""
    rows, cols = len(A), len(A[0])
    M = [list(A[i]) + [b[i]] for i in range(rows)]
    pivot_cols = []
    r = 0
    for c in range(cols):
        pivot = None
        for i in range(r, rows):
            if abs(M[i][c]) > tol:
                pivot = i
                break
        if pivot is None:
            continue
        M[r], M[pivot] = M[pivot], M[r]
        for i in range(rows):
            if i != r:
                factor = M[i][c] / M[r][c]
                for j in range(c, cols + 1):
                    M[i][j] -= factor * M[r][j]
        pivot_cols.append(c)
        r += 1
        if r == rows:
            break
    for i in range(len(pivot_cols), rows):
        if abs(M[i][cols]) > tol:
            return None
    x = [0.0] * cols
    for i, c in enumerate(pivot_cols):
        x[c] = M[i][cols] / M[i][c]
    return x


def as_columns(vectors):
    dim = len(vectors[0])
    return [[v[j] for v in vectors] for j in range(dim)]


def in_span(target, generators):
    return solve_consistent(as_columns(generators), target) is not None


print("=== Part 1: a single generator reaches only a line ===")
g = [[1.0, 1.0]]
for probe in ([30.0, 3.0], [5.0, 5.0], [-2.0, -2.0], [1.0, 2.0]):
    print(f"  target {probe} in span of {[1.0, 1.0]}? {in_span(probe, g)}")
print("Reachable points are exactly the multiples of [1, 1], which is the line y = x.")

print()
print("=== Part 2: two independent generators reach the whole of R^2 ===")
g = [[1.0, 0.0], [0.0, 1.0]]
for probe in ([30.0, 3.0], [-7.5, 2.25], [0.0, 0.0]):
    print(f"  target {probe} in span? {in_span(probe, g)}")

print()
print("=== Part 3: two generators that span only a plane in R^3 ===")
g = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]  # both have third component 0
for probe in ([4.0, -1.0, 0.0], [4.0, -1.0, 2.0], [0.0, 0.0, 0.0]):
    print(f"  target {probe} in span? {in_span(probe, g)}")
print("Unreachable means no coefficients c1, c2 give c1*[1,0,0] + c2*[0,1,0] = target,")
print("because the left side always has third component 0.")

print()
print("=== Part 4: the span is unchanged if we add a redundant generator ===")
base = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
with_extra = base + [[1.0, 1.0, 0.0]]  # the third generator is base[0] + base[1]
print(f"base          = {base}")
print(f"with_extra    = {with_extra}")
print(f"both reach [5, -3, 0]: "
      f"{in_span([5.0, -3.0, 0.0], base) and in_span([5.0, -3.0, 0.0], with_extra)}")
print(f"both fail on [5, -3, 7]: "
      f"{in_span([5.0, -3.0, 7.0], base) and in_span([5.0, -3.0, 7.0], with_extra)}")
print("A redundant generator costs storage and buys nothing. This is why real")
print("systems find a basis first: it is the smallest description of the same set.")
```

Output:

```
=== Part 1: a single generator reaches only a line ===
  target [30.0, 3.0] in span of [1.0, 1.0]? False
  target [5.0, 5.0] in span of [1.0, 1.0]? True
  target [-2.0, -2.0] in span of [1.0, 1.0]? True
  target [1.0, 2.0] in span of [1.0, 1.0]? False
Reachable points are exactly the multiples of [1, 1], which is the line y = x.

=== Part 2: two independent generators reach the whole of R^2 ===
  target [30.0, 3.0] in span? True
  target [-7.5, 2.25] in span? True
  target [0.0, 0.0] in span? True

=== Part 3: two generators that span only a plane in R^3 ===
  target [4.0, -1.0, 0.0] in span? True
  target [4.0, -1.0, 2.0] in span? False
  target [0.0, 0.0, 0.0] in span? True
Unreachable means no coefficients c1, c2 give c1*[1,0,0] + c2*[0,1,0] = target,
because the left side always has third component 0.

=== Part 4: the span is unchanged if we add a redundant generator ===
base          = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
with_extra    = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]]
both reach [5, -3, 0]: True
both fail on [5, -3, 7]: False
A redundant generator costs storage and buys nothing. This is why real
systems find a basis first: it is the smallest description of the same set.
```

In words: (a) one generator reaches a line, and only points on it. (b) Two
perpendicular generators reach every point of the plane. (c) Two generators
whose third component is zero can never produce a nonzero third component.

</details>

**[ ] Exercise 3 — subspace or not?** Decide whether each of these subsets of
`ℝ³` is a subspace, and give a one-line reason for each.

1. `{(x, y, z) : x + y + z = 0}`
2. `{(x, y, z) : x + y + z = 1}`
3. `{(x, y, z) : x·y·z = 0}`
4. `{(x, y, z) : x = y}`

<details>
<summary>Solution</summary>

1. Subspace. `0 + 0 + 0 = 0`; scaling gives `c(x+y+z) = 0`; adding two triples
   whose sums are zero gives a triple whose sum is zero.
2. Not a subspace. It does not contain the zero vector.
3. Not a subspace. `[1, 2, 0]` and `[0, 0, 7]` are both in it, but their sum
   `[1, 2, 7]` is not, since `1·2·7 = 14 ≠ 0`.
4. Subspace. `0 = 0`; scaling preserves the equality; adding two points with
   equal first and second components gives another such point.

```python
TOL = 1e-9


def is_zero(v, tol=TOL):
    return all(abs(x) <= tol for x in v)


def vadd(u, v):
    return [a + b for a, b in zip(u, v)]


def vscale(c, u):
    return [c * a for a in u]


# A candidate set, described by the rule that decides membership.
def subspace_test(predicate, probes):
    dim = len(probes[0])
    has_zero = predicate([0.0] * dim)
    members = [p for p in probes if predicate(p)]

    add_ok = all(
        predicate(vadd(u, v)) for u in members for v in members
    )
    scale_ok = all(
        predicate(vscale(c, u)) for u in members for c in (2.0, -1.0, 0.5)
    )
    return has_zero, add_ok, scale_ok, members


candidates = {
    "S1 = {(x,y,z) : x + y + z = 0}": lambda v: abs(v[0] + v[1] + v[2]) < TOL,
    "S2 = {(x,y,z) : x + y + z = 1}": lambda v: abs(v[0] + v[1] + v[2] - 1.0) < TOL,
    "S3 = {(x,y,z) : x*y*z = 0}": lambda v: abs(v[0] * v[1] * v[2]) < TOL,
    "S4 = {(x,y,z) : x = y}": lambda v: abs(v[0] - v[1]) < TOL,
}

# Probes chosen so that each candidate set has at least two interesting members.
probes = [
    [1.0, 2.0, 0.0],    # x*y*z = 0
    [1.0, 1.0, -2.0],   # x+y+z = 0
    [0.0, 0.0, 0.0],    # the zero vector
    [2.0, 0.0, 2.0],    # x*y*z = 0
    [0.0, 0.0, 7.0],    # x = y and x*y*z = 0
    [-1.0, 5.0, -4.0],  # x+y+z = 0
    [3.0, 3.0, 3.0],    # x = y
]

for name, pred in candidates.items():
    zero_ok, add_ok, scale_ok, members = subspace_test(pred, probes)
    ok = zero_ok and add_ok and scale_ok
    print(f"{name}")
    print(f"    zero={str(zero_ok):5s} closed under addition={str(add_ok):5s} "
          f"closed under scaling={str(scale_ok):5s} -> "
          f"{'SUBSPACE' if ok else 'not a subspace'}")

print()
print("Explicit witness for the failure of S3: [1,2,0] and [0,0,7] are both in")
print("S3, but their sum is [1,2,7], and 1*2*7 = 14, not 0.")
a, b = [1.0, 2.0, 0.0], [0.0, 0.0, 7.0]
print(f"  in S3? {[a, b]} -> "
      f"{[a[0]*a[1]*a[2] == 0, b[0]*b[1]*b[2] == 0]}")
print(f"  sum = {vadd(a, b)}, product = {vadd(a, b)[0]*vadd(a, b)[1]*vadd(a, b)[2]}")

print()
print("Proof sketch for S1 = {(x,y,z) : x + y + z = 0}: write a point as")
print("(x, y, z) = x*(1,0,0) + y*(0,1,0) + z*(0,0,1) with the condition")
print("x + y + z = 0. Adding two such points gives a new triple whose sum is")
print("still 0, and scaling by any number c gives c(x+y+z) = 0. Done.")
```

Output:

```
S1 = {(x,y,z) : x + y + z = 0}
    zero=True  closed under addition=True  closed under scaling=True  -> SUBSPACE
S2 = {(x,y,z) : x + y + z = 1}
    zero=False closed under addition=True  closed under scaling=True  -> not a subspace
S3 = {(x,y,z) : x*y*z = 0}
    zero=True  closed under addition=False closed under scaling=True  -> not a subspace
S4 = {(x,y,z) : x = y}
    zero=True  closed under addition=True  closed under scaling=True  -> SUBSPACE
```

Note that finite probing can only *refute* a subspace claim, never prove one.
The proof of S1 and S4 above is the argument you would write on paper; the code
is a check, not a proof.

</details>

**[ ] Exercise 4 — a linear model of house prices.** Four houses have floor
areas `80, 120, 150, 200` square metres and asking prices
`290000, 410000, 500000, 690000` dollars.

1. Fit the single rule `price = 3000·area + 50000` and report the residual for
   each house.
2. Now fit `price_i = c_i · area_i` with one coefficient per house. Report the
   coefficients and say why this model, despite fitting perfectly, is useless.
3. Fit a slope and intercept from the first two houses only, then check it
   against all four.

<details>
<summary>Solution</summary>

```python
area = [80.0, 120.0, 150.0, 200.0]
price = [290_000.0, 410_000.0, 500_000.0, 690_000.0]

print("=== Model 1: one global rule, price = 3000 * area + 50000 ===")
predicted = [3000.0 * a + 50_000.0 for a in area]
residuals = [p - q for p, q in zip(price, predicted)]
for a, p, q, r in zip(area, price, predicted, residuals):
    print(f"  {a:5.0f} sqm: actual {p:9.0f}  predicted {q:9.0f}  residual {r:9.0f}")
print(f"  max |residual| = {max(abs(r) for r in residuals):.0f}")

print()
print("=== Model 2: one coefficient per house, price_i = c_i * area_i ===")
# This always fits perfectly, and it is useless: a model with as many free
# parameters as data points memorises the data and predicts nothing.
coeffs = [p / a for p, a in zip(price, area)]
print(f"  implied price per square metre per house: {[round(c, 1) for c in coeffs]}")
for a, p, c in zip(area, price, coeffs):
    print(f"  {a:5.0f} sqm -> {c:7.1f}/sqm, rebuilds {c * a:9.1f} (actual {p:9.1f})")
print(f"  spread of coefficients: {max(coeffs) - min(coeffs):.1f} per sqm")
print("The variation is the model's error, hidden inside the parameters.")

print()
print("=== Why the two-parameter version is the useful one ===")
# Solve for [slope, intercept] from two houses, then check the other two.
i, j = 0, 1
slope = (price[j] - price[i]) / (area[j] - area[i])
intercept = price[i] - slope * area[i]
print(f"  fitted from houses {i} and {j} only: slope={slope:.1f}, intercept={intercept:.1f}")
for k, (a, p) in enumerate(zip(area, price)):
    fit = slope * a + intercept
    flag = "exact" if abs(fit - p) < 1e-6 else f"off by {fit - p:+.0f}"
    print(f"  house {k}: {a:5.0f} sqm -> fit {fit:9.1f}, actual {p:9.1f}  ({flag})")
print()
print("Two houses with different areas pin down both numbers exactly. That is")
print("the whole content of 'solving a linear system', and lesson 32 is the")
print("algorithm for doing it when you have many houses.")
```

Output:

```
=== Model 1: one global rule, price = 3000 * area + 50000 ===
     80 sqm: actual    290000  predicted    290000  residual         0
    120 sqm: actual    410000  predicted    410000  residual         0
    150 sqm: actual    500000  predicted    500000  residual         0
    200 sqm: actual    690000  predicted    650000  residual     40000
  max |residual| = 40000

=== Model 2: one coefficient per house, price_i = c_i * area_i ===
  implied price per square metre per house: [3625.0, 3416.7, 3333.3, 3450.0]
     80 sqm ->  3625.0/sqm, rebuilds  290000.0 (actual  290000.0)
    120 sqm ->  3416.7/sqm, rebuilds  410000.0 (actual  410000.0)
    150 sqm ->  3333.3/sqm, rebuilds  500000.0 (actual  500000.0)
    200 sqm ->  3450.0/sqm, rebuilds  690000.0 (actual  690000.0)
  spread of coefficients: 291.7 per sqm
The variation is the model's error, hidden inside the parameters.

=== Why the two-parameter version is the useful one ===
  fitted from houses 0 and 1 only: slope=3000.0, intercept=50000.0
    house 0:    80 sqm -> fit  290000.0, actual  290000.0  (exact)
    house 1:   120 sqm -> fit  410000.0, actual  410000.0  (exact)
    house 2:   150 sqm -> fit  500000.0, actual  500000.0  (exact)
    house 3:   200 sqm -> fit  650000.0, actual  690000.0  (off by -40000)
```

For part 2, the spread of 291.7 per square metre *is* the disagreement between
houses, and the model has no way to say which coefficient is right for a fifth
house. Model 1 has two free numbers total, so it makes a prediction it can be
wrong about. Prefer the model with fewer parameters that still fits, which is the
idea behind regularisation in [lesson 100](../part08_optimization/100_convexity.md).

</details>

**[ ] Exercise 5 — independence, and a code count.** Write `is_independent` and
`dependent_relation` for a list of vectors, then decide independence for:
`{[1,0], [0,1], [1,1]}`, `{[1,0], [0,1], [1,2]}`, `{[1,2], [2,4]}`, and
`{[1,2], [2,3]}`. Verify one relation by hand. Then explain why the four vectors
`e1, e2, e3, [1,1,1]` in `ℝ³` are dependent.

**Challenge.** The bit strings of length 4 satisfying "the number of 1 bits is
even" and "bit 0 equals bit 3" form a subspace over GF(2). Enumerate its
codewords by brute force, and then count them without enumerating. Explain why
your count matches.

<details>
<summary>Solution</summary>

```python
import itertools

TOL = 1e-9


def vadd(u, v):
    return [a + b for a, b in zip(u, v)]


def vscale(c, u):
    return [c * a for a in u]


def dependent_relation(vectors, tol=TOL):
    """Return coefficients c with sum(c_j * v_j) = 0, or None if independent.

    The vectors go in as COLUMNS of a matrix, and we row reduce to find the
    null space. A nonzero null vector IS the cancelling relation.
    """
    dim = len(vectors[0])
    A = [[v[j] for v in vectors] for j in range(dim)]
    rows, cols = len(A), len(A[0])
    M = [list(A[i]) for i in range(rows)]
    pivot_cols = []
    r = 0
    for c in range(cols):
        pivot = None
        for i in range(r, rows):
            if abs(M[i][c]) > tol:
                pivot = i
                break
        if pivot is None:
            continue
        M[r], M[pivot] = M[pivot], M[r]
        p = M[r][c]
        for j in range(c, cols):
            M[r][j] /= p
        for i in range(rows):
            if i != r:
                factor = M[i][c]
                for j in range(c, cols):
                    M[i][j] -= factor * M[r][j]
        pivot_cols.append(c)
        r += 1
        if r == rows:
            break
    if len(pivot_cols) == cols:
        return None
    free = [c for c in range(cols) if c not in pivot_cols][0]
    c_vec = [0.0] * cols
    c_vec[free] = 1.0
    for i, pc in enumerate(pivot_cols):
        c_vec[pc] = -M[i][free]
    return c_vec


def is_independent(vectors, tol=TOL):
    return dependent_relation(vectors, tol) is None


e1 = [1.0, 0.0, 0.0]
e2 = [0.0, 1.0, 0.0]

print("=== Are the three vectors independent? ===")
sets = [
    ("{e1, e2, e1+e2}", [e1, e2, [1.0, 1.0, 0.0]]),
    ("{e1, e2, e1+2e2}", [e1, e2, [1.0, 2.0, 0.0]]),
    ("{e1, e2}", [e1, e2]),
    ("{[1,2],[2,4]}", [[1.0, 2.0], [2.0, 4.0]]),
    ("{[1,2],[2,3]}", [[1.0, 2.0], [2.0, 3.0]]),
]
for name, vecs in sets:
    rel = dependent_relation(vecs)
    text = "none (independent)" if rel is None else str([round(x, 4) for x in rel])
    print(f"  {name:18s} independent={str(is_independent(vecs)):5s} relation={text}")

print()
print("Check by hand for {e1, e2, e1+e2}: relation [-1, -1, 1] means")
vecs = [e1, e2, [1.0, 1.0, 0.0]]
rel = dependent_relation(vecs)
total = [round(sum(rel[j] * vecs[j][i] for j in range(3)), 6) for i in range(3)]
print(f"  -1*[1,0,0] + -1*[0,1,0] + 1*[1,1,0] = {total}")

print()
print("More vectors than the dimension: never independent.")
four = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 1.0, 1.0]]
print(f"  4 vectors in R^3: independent = {is_independent(four)}")
print(f"  relation          = {[round(x, 4) for x in dependent_relation(four)]}")
print("Read it as: v1 + v2 + v3 - v4 = 0, which is obviously true.")

print()
print("=== Challenge: count the codewords of a GF(2) subspace by brute force ===")
code = [w for w in itertools.product((0, 1), repeat=4)
        if (w[0] + w[1] + w[2]) % 2 == 0 and w[0] == w[3]]
print(f"  conditions: w0 + w1 + w2 is even, and w0 == w3")
for w in code:
    print(f"    {''.join(map(str, w))}")
print(f"  total {len(code)} codewords")
print("  Count them structurally instead, so it scales past n = 4. The rule")
print("  w3 = w0 fixes the last bit from the first. Then the parity rule is a")
print("  single equation in the remaining bits, so it fixes exactly one of them")
print("  and leaves two free. Two free bits means 2^2 = 4 codewords. Matches.")
print("  The same logic is why every linear code has exactly 2^k codewords.")

print()
print("Verify closure with the same three subspace conditions, using XOR as add.")
words = [list(w) for w in code]


def gf2_in(w):
    return (w[0] + w[1] + w[2]) % 2 == 0 and w[0] == w[3]


closed_add = all(gf2_in(vadd(u, v)) for u in words for v in words)
closed_scale = all(gf2_in(vscale(c, u)) for u in words for c in (0, 1))
has_zero = gf2_in([0, 0, 0, 0])
print(f"  contains zero: {has_zero}, closed under XOR: {closed_add}, "
      f"closed under scaling by 0 and 1: {closed_scale}")
print("  all three hold, so it really is a subspace, and a code by definition.")
```

Output:

```
=== Are the three vectors independent? ===
  {e1, e2, e1+e2}    independent=False relation=[-1.0, -1.0, 1.0]
  {e1, e2, e1+2e2}   independent=False relation=[-1.0, -2.0, 1.0]
  {e1, e2}           independent=True  relation=none (independent)
  {[1,2],[2,4]}      independent=False relation=[-2.0, 1.0]
  {[1,2],[2,3]}      independent=True  relation=none (independent)

Check by hand for {e1, e2, e1+e2}: relation [-1, -1, 1] means
  -1*[1,0,0] + -1*[0,1,0] + 1*[1,1,0] = [0.0, 0.0, 0.0]

More vectors than the dimension: never independent.
  4 vectors in R^3: independent = False
  relation          = [-1.0, -1.0, -1.0, 1.0]
Read it as: v1 + v2 + v3 - v4 = 0, which is obviously true.

=== Challenge: count the codewords of a GF(2) subspace by brute force ===
  conditions: w0 + w1 + w2 is even, and w0 == w3
    0000
    0110
    1011
    1101
  total 4 codewords
  Count them structurally instead, so it scales past n = 4. The rule
  w3 = w0 fixes the last bit from the first. Then the parity rule is a
  single equation in the remaining bits, so it fixes exactly one of them
  and leaves two free. Two free bits means 2^2 = 4 codewords. Matches.
  The same logic is why every linear code has exactly 2^k codewords.

Verify closure with the same three subspace conditions, using XOR as add.
  contains zero: True, closed under XOR: True, closed under scaling by 0 and 1: True
  all three hold, so it really is a subspace, and a code by definition.
```

The hand check: `-1·[1,0,0] + -1·[0,1,0] + 1·[1,1,0] = [-1,0,0] + [0,-1,0] + [1,1,0] = [0,0,0]`,
which is the zero vector, so the set is dependent.

</details>

**[ ] Exercise 6 — the least-squares residual is perpendicular to the span.**
Take the three generators `g₀ = [1,0,0]`, `g₁ = [0,1,0]`, `g₂ = [1,1,0]` in `ℝ³`
and the target `t = [4, -1, 5]`.

1. Show that `A c = t` has no solution, and say in one sentence why.
2. Find the coefficients of the best fit and the residual. Report the squared
   length of the residual.
3. Show that the residual is perpendicular to all three generators, including
   the dependent one `g₂`.
4. Find a second, different set of coefficients giving exactly the same fit.
   Explain what that tells you about the word "the" in "the least-squares
   solution".

**Challenge.** Prove in general that when `c` minimises `‖A c − t‖²` over `c`,
the residual `t − A c` is perpendicular to every column of `A`. Then use the
result to explain why the minimum is unique in the *fitted point* but never
unique in the *coefficients* when the columns of `A` are linearly dependent —
and say what one should do about that in a real model.

<details>
<summary>Solution</summary>

Parts 1 to 4 by hand first. Write the product out with the generators as columns:

    A c = c₀·[1,0,0] + c₁·[0,1,0] + c₂·[1,1,0] = (c₀ + c₂,  c₁ + c₂,  0)

**Part 1.** The third component of `A c` is `0` for every choice of coefficients,
but the third component of `t = (4, -1, 5)` is `5`. No `A c` can equal `t`, so
`A c = t` has no solution. The generators simply do not contain the third
direction.

**Part 2.** Drop the unreachable part of the target, so we ask for
`A c = (4, -1, 0)`. Taking `c₂ = 0` gives `c₀ = 4`, `c₁ = -1`, hence

    c = (4, -1, 0),   fit = A c = (4, -1, 0),   residual = t - fit = (0, 0, 5)

Squared length of the residual: `0² + 0² + 5² = 25`. Length `5`.

**Part 3.** Perpendicularity, by hand:

    (0,0,5) · (1,0,0) = 0
    (0,0,5) · (0,1,0) = 0
    (0,0,5) · (1,1,0) = 0 + 0 + 0 = 0

All three are zero, so the residual is perpendicular to all three generators. It
points along the third axis, which is exactly the direction the generators
cannot reach.

**Part 4.** Take `c₂ = 1`. Then `c₀ + 1 = 4` and `c₁ + 1 = -1`, so
`c = (3, -2, 1)`, and

    3·[1,0,0] + (-2)·[0,1,0] + 1·[1,1,0] = (3,0,0) + (0,-2,0) + (1,1,0) = (4,-1,0)

The same fit, the same residual, the same squared distance `25`. Generally
`c = (4 - t, -1 - t, t)` for any `t`, because the first two components are
`c₀ + c₂` and `c₁ + c₂` and only those sums are pinned down. So the fitted point
is unique and the coefficients are not: "the least-squares solution" should be
"a least-squares solution". Any statement of the form "the coefficient on `g₂`
is 0" is meaningless — it is arbitrary, and a different pivot choice returns a
different number.

```python
import itertools
from math import sqrt


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def vadd(u, v):
    return [a + b for a, b in zip(u, v)]


def vsub(u, v):
    return [a - b for a, b in zip(u, v)]


def vscale(c, u):
    return [c * a for a in u]


def norm(u):
    return sqrt(dot(u, u))


def as_columns(vectors):
    dim = len(vectors[0])
    return [[v[j] for v in vectors] for j in range(dim)]


def solve_consistent(A, b, tol=1e-9):
    """Return one solution of A c = b, or None when no solution exists."""
    rows, cols = len(A), len(A[0])
    M = [list(A[i]) + [b[i]] for i in range(rows)]
    pivot_cols = []
    r = 0
    for c in range(cols):
        pivot = None
        for i in range(r, rows):
            if abs(M[i][c]) > tol:
                pivot = i
                break
        if pivot is None:
            continue
        M[r], M[pivot] = M[pivot], M[r]
        for i in range(rows):
            if i != r:
                factor = M[i][c] / M[r][c]
                for j in range(c, cols + 1):
                    M[i][j] -= factor * M[r][j]
        pivot_cols.append(c)
        r += 1
        if r == rows:
            break
    for i in range(len(pivot_cols), rows):
        if abs(M[i][cols]) > tol:
            return None
    x = [0.0] * cols
    for i, c in enumerate(pivot_cols):
        x[c] = M[i][cols] / M[i][c]
    return x


generators = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]]
target = [4.0, -1.0, 5.0]
A = as_columns(generators)

print("=== Part 1: the exact problem has no solution ===")
print(f"generators (columns of A) = {A}")
print(f"target t = {target}")
print(f"solve A c = t exactly  -> {solve_consistent(A, target)}   <- None means unreachable")
print("A c = (c0 + c2, c1 + c2, 0): the third component can only ever be 0.")

print()
print("=== Part 2: the best fit and its residual ===")
reachable_part = [4.0, -1.0, 0.0]
c = solve_consistent(A, reachable_part)
fit = [round(sum(c[j] * generators[j][i] for j in range(3)), 6) for i in range(3)]
residual = vsub(target, fit)
print(f"t with the unreachable part dropped = {reachable_part}")
print(f"coefficients c = {c}")
print(f"fit      = {fit}")
print(f"residual = t - fit = {residual}")
print(f"length of residual = {norm(residual):.4f}, squared = {dot(residual, residual):.4f}")

print()
print("=== Part 3: the residual is perpendicular to every generator, dependent one included ===")
for j, g in enumerate(generators):
    print(f"  residual . g{j} = {dot(residual, g):.4f}")
print("All zero, so the leftover error is in a direction no generator reaches.")

print()
print("=== Part 4: the coefficients are NOT unique, but the fit and residual are ===")
for c2 in (0.0, 1.0, -2.5):
    cand = [4.0 - c2, -1.0 - c2, c2]
    rebuild = [round(sum(cand[j] * generators[j][i] for j in range(3)), 6) for i in range(3)]
    res = vsub(target, rebuild)
    print(f"  c2 = {c2:5.1f} -> c = {cand}, fit = {rebuild}, "
          f"squared distance = {dot(res, res):.4f}")

print()
print("=== Brute-force check that nothing is better ===")
best = None
grid = [k / 2 for k in range(-4, 9)]
for c0, c1, c2 in itertools.product(grid, repeat=3):
    rebuild = [c0 * generators[0][i] + c1 * generators[1][i] + c2 * generators[2][i]
               for i in range(3)]
    res = vsub(target, rebuild)
    d = dot(res, res)
    if best is None or d < best:
        best = d
print(f"smallest squared distance on a {len(grid)}^3 grid = {best:.4f}")
print(f"our residual gives {dot(residual, residual):.4f}. Nothing beats it.")
```

Output:

```
=== Part 1: the exact problem has no solution ===
generators (columns of A) = [[1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [0.0, 0.0, 0.0]]
target t = [4.0, -1.0, 5.0]
solve A c = t exactly  -> None   <- None means unreachable
A c = (c0 + c2, c1 + c2, 0): the third component can only ever be 0.

=== Part 2: the best fit and its residual ===
t with the unreachable part dropped = [4.0, -1.0, 0.0]
coefficients c = [4.0, -1.0, 0.0]
fit      = [4.0, -1.0, 0.0]
residual = t - fit = [0.0, 0.0, 5.0]
length of residual = 5.0000, squared = 25.0000

=== Part 3: the residual is perpendicular to every generator, dependent one included ===
  residual . g0 = 0.0000
  residual . g1 = 0.0000
  residual . g2 = 0.0000
All zero, so the leftover error is in a direction no generator reaches.

=== Part 4: the coefficients are NOT unique, but the fit and residual are ===
  c2 =   0.0 -> c = [4.0, -1.0, 0.0], fit = [4.0, -1.0, 0.0], squared distance = 25.0000
  c2 =   1.0 -> c = [3.0, -2.0, 1.0], fit = [4.0, -1.0, 0.0], squared distance = 25.0000
  c2 =  -2.5 -> c = [6.5, 1.5, -2.5], fit = [4.0, -1.0, 0.0], squared distance = 25.0000

=== Brute-force check that nothing is better ===
smallest squared distance on a 13^3 grid = 25.0000
our residual gives 25.0000. Nothing beats it.
```

**Challenge, by hand.** Let `c*` be any minimiser of `f(c) = ‖A c − t‖²` and let
`h` be an arbitrary displacement. With `r = A c* − t`:

    f(c* + h) − f(c*)
      = ‖r + A h‖² − ‖r‖²
      = (‖r‖² + 2 r·(A h) + ‖A h‖²) − ‖r‖²
      = 2 r·(A h) + ‖A h‖²

If `r` is perpendicular to every column of `A`, then `r·(A h) = 0` for every `h`,
and `f(c* + h) − f(c*) = ‖A h‖² ≥ 0`, so `c*` is a global minimum. Conversely, if
`r·(A h) ≠ 0` for some `h` then for `h` and `−h` the two differences are
`2 r·(A h) + ‖A h‖²` and `−2 r·(A h) + ‖A h‖²`, whose minimum is
`‖A h‖² − 2|r·(A h)|`; if `r·(A h)` is nonzero enough to outweigh `‖A h‖²/2` that
is negative and `c*` was not a minimum. Smallest positive values of `h` give
exactly the normal equations, so the two conditions are equivalent. Hence

    `r = A c* − t` ⟂ every column of `A`, i.e. `Aᵀ(A c* − t) = 0`, i.e.
    `(Aᵀ A) c* = Aᵀ t` — the normal equations.

That is why every least-squares routine in existence multiplies by `Aᵀ` first.

Now the uniqueness question. The fitted point is unique because the fitted point
*is* the closest point of the span, and a subspace is closed: if `p` and `q` are
both closest to `t` then every point `s p + (1−s) q` of the segment joining them
lies in the span and is at least as close, and the distance is a strictly convex
function along that segment unless `p = q`. The coefficients are different: if the
columns of `A` are dependent there is a nonzero `d` with `A d = 0`, so
`A(c* + d) = A c*` for every `c*` already found. An entire line `c* + ℝ d` of
coefficient vectors produces the identical fit, which is precisely what parts 3
and 4 exhibit: `d = (-1, -1, 1)` is the relation among the three generators, and
`c = (4, -1, 0) + t·(-1, -1, 1)` runs along it.

What to do about it: a non-unique coefficient is not a numerical curiosity, it is
a report that your model is over-parameterised. Two coefficients that are
mathematically interchangeable can behave very differently in practice — with any
regularisation term, or any finite precision, the solver will pick one of them
essentially arbitrarily, and the one it picks can change when you reorder your
columns, change the data order, or upgrade numpy. The fix is to make the model
minimal before fitting: drop the dependent column and keep `g₀, g₁`, at which
point the coefficients become unique and equal to `(4, -1)`. This is the same
redundancy argument as Exercise 2's fourth part and the same reason
`np.linalg.lstsq` reports a `rank` field alongside the coefficients — it is
telling you which of those two situations you are in.

</details>



## Summary

- A vector is a list of numbers, and a vector space is a collection of lists
  closed under addition and scalar multiplication.
- A linear combination is a weighted sum of vectors; the span is the set of all
  such sums, i.e. everything reachable from the origin.
- A set is linearly dependent when some nonzero combination of its vectors
  equals the zero vector, which is the same as one vector being rebuildable from
  the others.
- More vectors than the dimension guarantees dependence, but the converse is
  false: you must row reduce to know.
- The subspace test is three checks — contains zero, closed under scaling,
  closed under addition — and no others.
- Any subspace passes through the origin. A set that does not (a circle, a line
  offset from the origin) is an affine subspace, not a vector space.
- Span and independence are about redundancy: drop every dependent vector and
  what remains is a basis for exactly the same set, in strictly less space.
- The same rules hold over any field, including GF(2), which is why linear codes
  and bitwise logic are this same mathematics.

## Next

[31 — Matrices and Matrix Algebra](../part03_linear_algebra/31_matrices_and_matrix_algebra.md) takes the
list of vectors from this lesson and puts them in a grid, then makes the grid do
arithmetic: multiplication, transpose, powers, and the special shapes that
structured problems rely on.
