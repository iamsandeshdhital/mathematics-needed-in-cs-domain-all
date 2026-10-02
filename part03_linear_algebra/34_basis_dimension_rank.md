# 34 — Basis, Dimension, and Rank

**Part**: part03_linear_algebra · **Prerequisites**: 33 · **Time**: 35 min

---

## In Plain Words

Suppose you have a pile of vectors. Two questions come up immediately, and they
are different questions.

The first asks what you can build from them. Scale each one by some number and
add the results together — everything you can get that way is called the span,
and it is a flat infinite set, like all of ordinary two-dimensional space if you
only have two good vectors.

The second asks whether every vector in the pile is pulling its weight. If one of
them can be built from the others, it is redundant, and you can throw it away
without losing anything. If none can be built from the others, the set is
independent.

A set that both spans everything you had and has no redundancy is a basis. How
many vectors a basis has is called the dimension, and it is the same number no
matter which basis you pick — which is the surprising and extremely useful part.

Applied to a grid of numbers, the maximum number of useful columns is the rank.
Rank is the number the whole subject runs on: it tells you how many degrees of
freedom your data has, whether a system of equations has a unique answer, and how
many directions were lost.

## Why Computer Science Cares

- **`numpy.linalg.matrix_rank`, and the tolerance it hides.** A design matrix
  with collinear columns is the single most common reason a linear model "fails
  to converge" or returns enormous coefficients. `matrix_rank` finds the
  redundant columns; the default tolerance decides what counts as redundant.
- **Low-rank approximations and compression.** Recommender matrices are routinely
  rank-10-ish despite having millions of rows; a truncated SVD
  ([lesson 40](40_svd_and_pca.md)) turns that into a few megabytes instead of
  gigabytes, and `matrix_rank` tells you whether the truncation is safe.
- **Dimensionality reduction.** PCA
  ([lesson 40](40_svd_and_pca.md)) keeps exactly the top `r` directions and drops
  the rest. `r` is the rank of the centred data, so "how many components should
  I keep" is a rank question, and the elbow in the scree plot is where you
  stopped.
- **Error-correcting codes.** A linear code is a subspace; its dimension sets how
  many codewords there are (`2^k` over GF(2)) and its distance sets how many
  errors it corrects. See
  [lesson 113](../part09_number_theory_crypto/113_error_correcting_codes.md).
- **Feature selection.** If a feature is a linear combination of others, you can
  drop it with zero information loss — and you should, because it halves the
  storage and removes the collinearity that wrecks gradient descent.
- **Interview questions.** "How do you detect redundant features?", "what is the
  rank of a matrix?", "why must row rank equal column rank?", and "what does
  `LinAlgError: Singular matrix` actually mean?" are all standard questions.

## The Formal Version

Symbols follow [SYMBOLS.md](../SYMBOLS.md). Let `F` be a field, `V` a vector
space over `F`, `S = {v₁, …, v_k} ⊆ V`.

**Definition.** The **span** of `S` is

    span(S) = { c₁v₁ + … + c_kv_k : c_i ∈ F }

It is always a subspace and always contains `0`.

**Definition.** `S` is **linearly independent** if `c₁v₁ + … + c_kv_k = 0`
forces `c₁ = … = c_k = 0`. Otherwise it is **dependent**.

**Definition.** `S` is a **basis** for `V` if (i) `S` spans `V` and (ii) `S` is
linearly independent.

**Theorem (Basis extraction).** If `S` spans `V`, some subset `B ⊆ S` is a basis
for `V`. If `S` is linearly independent, some superset `B ⊇ S` is a basis — and
`B` exists only if `dim V ≥ |S|`.

**Explanation.** Independence gives a greedy algorithm: walk through `S` and keep
a vector only if it does not increase the span of what you have kept. Each kept
vector adds exactly one dimension, so the process terminates. This is
`greedy_basis` in the code, and it runs in `Θ(k)` rank computations, or
`Θ(k m n)` total with a naive rank each time.

**Definition.** `dim(V)` is the number of vectors in any basis of `V`.

**Theorem (Dimension is well defined).** Any two bases of a finite-dimensional
`V` have the same cardinality, and any two bases are connected by invertible
elementary column operations.

**Explanation.** If `B = {v₁,…,v_r}` and `C = {w₁,…,w_s}` are both bases, each
`w_j` is a combination of the `v_i`, so `C` is the columns of an `r × s` matrix
times `B`; since `C` is independent, that matrix has trivial kernel, so
`s ≤ r`. Symmetrically `r ≤ s`, hence `r = s`. The second part follows from the
first plus the fact that the transition matrix is square and invertible.

**Definition.** Let `A` be an `m × n` matrix. Its **column space**
`col(A) = span(A's columns)` is a subspace of `F^m`; its **row space**
`row(A) = span(A's rows)` is a subspace of `F^n`; its **null space**
`ker(A) = {x ∈ F^n : Ax = 0}` is a subspace of `F^n`; and its **left null space**
`ker(Aᵀ) = {y ∈ F^m : Aᵀy = 0}` is a subspace of `F^m`.

**Definition.** `rank(A) = dim col(A) = dim row(A)` (the equality is the next
theorem). `nullity(A) = dim ker(A)`.

**Theorem (Rank by elimination).** `rank(A)` equals the number of pivots in the
echelon form of `A`, which equals the number of nonzero rows of its RREF, which
equals the number of nonzero entries on the diagonal of any `U` in an LU
factorisation `A = LU`. Also `rank(A) ≤ min(m, n)`.

**Explanation.** Row operations do not change the row space or the column space,
so the RREF has the same rank as `A`. In the RREF each nonzero row has a `1` in a
distinct column, so the nonzero rows are visibly independent — the count is
visible rather than argued. For `LU`: `U` has the same row space as `A`, and
upper-triangular independent rows must have distinct leading entries, giving at
most one per column.

**Theorem (Row rank = column rank).** `dim col(A) = dim row(A)` for every `A`.

**Explanation.** Row operations are invertible, and an invertible left
multiplication preserves the column space: if `Ax = 0` then `(EA)x = E(Ax) = 0`,
so `ker(EA) = ker(A)`, hence `col(EA) = col(A)`. So the RREF has the same
*column* rank as `A` as well as the same row rank. Its number of pivots is both
the number of independent columns and the number of independent rows. That is why
one integer suffices.

**Theorem (Fundamental Theorem of Linear Algebra).** For `A` of rank `r`:

| subspace | lives in | dimension | complement of |
| --- | --- | --- | --- |
| `col(A)` | `F^m` | `r` | `ker(Aᵀ)` |
| `ker(A)` | `F^n` | `n − r` | `row(A)` |
| `row(A)` | `F^n` | `r` | `ker(A)` |
| `ker(Aᵀ)` | `F^m` | `m − r` | `col(A)` |

with `ker(A) = row(A)^⊥` and `ker(Aᵀ) = col(A)^⊥`, and each row of the table is a
direct-sum decomposition of the ambient space.

**Explanation.** `x ∈ ker(A)` means every row of `A` dotted with `x` is zero, so
`x` is orthogonal to every row combination, hence to `row(A)`. Since
`dim row(A) + dim ker(A) = r + (n − r) = n` and both sit in `F^n`, the two fill it
up: it is a direct sum, not just a containment. The `m` statement is the same
argument with `A` replaced by `Aᵀ`. The rank appears in all four entries and
cancels in both sums, which is why four dimensions are really one degree of
freedom.

**Definition.** `A` is **rank deficient** if `rank(A) < min(m, n)`. For a square
`A`, that is the same as `det(A) = 0` and the same as `ker(A) ≠ {0}`.

**Explanation.** `det(A) ≠ 0` ⟺ rank `n` ⟺ nullity `0` ⟺ invertible, by
[lesson 33](33_determinant_and_inverse.md). For rectangular matrices there is no
determinant, and rank deficiency is the only available notion.

**Theorem (Degrees of freedom).** In `Ax = b` with `A` of rank `r`, there are `r`
determined variables and `n − r` free ones. If the system is consistent, the
solution set is `x₀ + ker(A)`, an `(n−r)`-dimensional family; if not, it is empty.

**Explanation.** Each free column of the RREF of `[A | b]` gives one free
variable, and the RREF of `[A | b]` agrees with that of `A` on columns `0..n−1`
whenever the system is consistent. So the free unknowns correspond one-to-one to
a basis of `ker(A)`. Rank is the number of constraints; nullity is the number of
things the data does not pin down.

**Theorem (Existence and uniqueness, restated).** `Ax = b` has a solution for
every `b ∈ F^m` **iff** `rank(A) = m`. It has a **unique** solution for every `b`
**iff** `rank(A) = n`.

**Explanation.** `Ax = b` is solvable for all `b` exactly when `col(A) = F^m`,
which is rank `m`. It is uniquely solvable for all `b` exactly when `ker(A) = {0}`,
which is rank `n`. A square matrix has both at once exactly when it is invertible.

**Definition.** `v₁, …, v_n ∈ ℝⁿ` are **orthogonal** if `v_i · v_j = 0` for
`i ≠ j`; they are **orthonormal** if additionally each has norm 1. A basis that is
orthonormal is an **orthogonal basis**.

**Theorem (Orthogonal basis extension).** From any independent set in `ℝⁿ` you can
extend to a basis; by Gram–Schmidt you can do it in such a way that the basis is
orthonormal. An orthonormal basis gives `x = Σ_i (x·u_i) u_i` for every `x`.

**Explanation.** [Lesson 37](37_inner_products_norms_geometry.md) builds this.
It matters here because it is the other way to describe a subspace — by an
orthonormal list rather than by a spanning set — and the two descriptions are
interchangeable.

## Worked Example

Five samples, three features: a weight, a length, and a width. Each entry is the
raw measurement divided by 50 so the arithmetic stays in easy numbers:

    A = | 0.24  0.60  0.16 |       (12,   30,   8)   / 50
        | 0.28  0.70  0.18 |       (14,   35,   9)   / 50
        | 0.22  0.55  0.14 |       (11,  27.5,  7)   / 50
        | 0.30  0.75  0.20 |       (15,  37.5, 10)   / 50
        | 0.26  0.65  0.16 |       (13,  32.5,  8)   / 50

`A` is `5 × 3`. Read the columns as vectors in `ℝ⁵`:

    col0 = (0.24, 0.28, 0.22, 0.30, 0.26)
    col1 = (0.60, 0.70, 0.55, 0.75, 0.65)
    col2 = (0.16, 0.18, 0.14, 0.20, 0.16)

**Step 1: see the redundancy by eye before computing anything.**
`0.60 / 0.24 = 2.5` and `0.70 / 0.28 = 2.5` and `0.55 / 0.22 = 2.5` and
`0.75 / 0.30 = 2.5` and `0.65 / 0.26 = 2.5`. Every single row gives the same
ratio, so **`col1 = 2.5 · col0`** — the same physical feature recorded on a
different scale.

Now check `col2`, because the test that matters is whether the ratio is
*constant*, not whether it is near some number:

    0.16 / 0.24 = 0.6667
    0.18 / 0.28 = 0.6429
    0.14 / 0.22 = 0.6364
    0.20 / 0.30 = 0.6667
    0.16 / 0.26 = 0.6154

The ratios wander between `0.615` and `0.667`, so **`col2` is not a multiple of
`col0`**. Exactly one of the three features is redundant, and which one is now
determined rather than guessed.

**Step 2: confirm with row reduction.** `A` has `min(5,3) = 3` as its ceiling.
Pivot on row 0 and clear column 0 below it:

    R_1 <- R_1 - (0.28/0.24) R_0 = R_1 - (7/6) R_0
    R_2 <- R_2 - (0.22/0.24) R_0 = R_2 - (11/12) R_0
    R_3 <- R_3 - (0.30/0.24) R_0 = R_3 - (5/4) R_0
    R_4 <- R_4 - (0.26/0.24) R_0 = R_4 - (13/12) R_0

Row 1: `(0.28, 0.70, 0.18) − (7/6)(0.24, 0.60, 0.16)`. The first entry is `0` by
construction. The second: `0.70 − (7/6)(0.60) = 0.70 − 0.70 = 0`, exactly,
because `col1 = 2.5 col0`. The third:
`0.18 − (7/6)(0.16) = 0.18 − 0.18667 = −0.00667`, which is **not** zero.

Row 2: `(0.22, 0.55, 0.14) − (11/12)(0.24, 0.60, 0.16)`. Second entry
`0.55 − (11/12)(0.60) = 0.55 − 0.55 = 0`. Third entry
`0.14 − (11/12)(0.16) = 0.14 − 0.14667 = −0.00667`.

Row 3: `(0.30, 0.75, 0.20) − (5/4)(0.24, 0.60, 0.16)`. Second entry
`0.75 − 0.75 = 0`. Third entry `0.20 − (5/4)(0.16) = 0.20 − 0.20 = 0`.

Row 4: `(0.26, 0.65, 0.16) − (13/12)(0.24, 0.60, 0.16)`. Second entry
`0.65 − 0.65 = 0`. Third entry `0.16 − (13/12)(0.16) = 0.16 − 0.17333 = −0.01333`.

So the matrix becomes

    | 0.24  0.60   0.16   |
    | 0     0     -0.00667|
    | 0     0     -0.00667|
    | 0     0     -0.01333|
    | 0     0      0.16   |

Column 1 is entirely zero — exactly, as the proportionality predicted — and
column 2 survives with three distinct nonzero values. Pivot there: divide by the
pivot, clear, and the RREF is

    | 1   2.5   0 |
    | 0   0     1 |
    | 0   0     0 |
    | 0   0     0 |
    | 0   0     0 |

**Two pivots, in columns 0 and 2. So `rank(A) = 2`.**

**Step 3: exhibit the dependence, do not just assert it.** Put the three columns
in the columns of a matrix and row reduce. Solving
`c₀ col0 + c₁ col1 + c₂ col2 = 0`: row 0 gives
`0.24c₀ + 0.60c₁ + 0.16c₂ = 0`, and since `col1 = 2.5 col0` we get
`(0.24 + 1.5)c₀ + 0.16c₂ = 0`, i.e. `1.74c₀ = −0.16c₂`, i.e.
`c₀ = −(0.16/1.74) c₂ = −(2/21.75)c₂`. Setting `c₁ = 1` and `c₂ = 0` gives
`c = (−2.5, 1, 0)` directly. Check the other rows: row 1 is
`0.28(−2.5) + 0.70(1) + 0.18(0) = −0.70 + 0.70 = 0` ✓. Row 4 is
`0.26(−2.5) + 0.65(1) + 0.16(0) = −0.65 + 0.65 = 0` ✓. So

    (−2.5) · col0 + 1 · col1 + 0 · col2 = 0

A nonzero coefficient vector with a zero combination, so `{col0, col1, col2}` is
dependent, and specifically `col1` is the redundant one.

**Step 4: the greedy basis.** Walk the columns and keep a vector only if it
raises the rank:

- keep `col0` (rank goes 0 → 1)
- test `col1`: `rank([col0, col1]) = 1`, no increase, so **drop it**
- test `col2`: `rank([col0, col2]) = 2`, increase, so **keep it**

Basis: `{col0, col2}`, of size 2. Both dropped-and-kept columns are recoverable:

    col0 = 1 · col0 + 0 · col2
    col1 = 2.5 · col0 + 0 · col2
    col2 = 0 · col0 + 1 · col2

Nothing was lost. The span is the same set; only the description shrank. Note
that the recovered coefficient `2.5` is exactly the ratio read off by hand in
Step 1, recovered without being told it.

**Step 5: the four subspaces.** With `m = 5`, `n = 3`, `r = 2`:

    col(A)      in R^5,  dim 2   basis = the pivot columns of A, i.e. col0, col2
    ker(A)      in R^3,  dim 1   basis = (-2.5, 1, 0)
    row(A)      in R^3,  dim 2   basis = the nonzero rows of rref(A) = (1, 2.5, 0), (0, 0, 1)
    ker(A^T)    in R^5,  dim 3   basis = from rref(A^T)

`ker(A)` and `row(A)` both live in `ℝ³`, with dimensions 1 and 2 summing to 3 —
a complementary pair. `col(A)` and `ker(Aᵀ)` both live in `ℝ⁵`, with dimensions 2
and 3 summing to 5. The code verifies the orthogonality: `ker(A) ⊥ row(A)` and
`ker(Aᵀ) ⊥ col(A)`.

**Step 6: rank as degrees of freedom.** Solve `Ax = b` with `b` in the column
space, say `b = 2·col0 + 3·col2 = (0.96, 1.10, 0.86, 1.20, 1.00)`. The augmented
matrix reduces to

    | 1  2.5  0 | 2 |
    | 0  0    1 | 3 |
    | 0  0    0 | 0 |
    | 0  0    0 | 0 |
    | 0  0    0 | 0 |

Pivots in the unknowns are columns 0 and 2, so `x₀ = 2` and `x₂ = 3` are
determined, and `x₁` is free. Setting `x₁ = 0` gives `x = (2, 0, 3)`; setting
`x₁ = 1` gives `(−2.5, 1, 0)`, the null direction. So

    x = (2, 0, 3) + t·(−2.5, 1, 0),   t ∈ ℝ

Two determined variables, one free, `2 + 1 = 3 = n`. One degree of freedom, and
one null direction — the same object counted from the other side.

Now take `b = (1, 0, 0, 0, 0)`, which is not in the column space. The reduction of
`[A | b]` now needs a third pivot, and it lands in `b`'s own column — the
signature of the row `0 = 1`, i.e. no solution. Same rank, different verdict on
`b`. That is why rank alone never settles solvability.

## Runnable Code

### Rank by row reduction, and a basis by dropping the redundant columns

```python
"""Block 1: span, independence, basis; rank by row reduction."""

TOL = 1e-9


# ---------------------------------------------------------------- helpers
def shape(M):
    return len(M), len(M[0])


def transpose(M):
    rows, cols = shape(M)
    return [[M[i][j] for i in range(rows)] for j in range(cols)]


def matmul(A, B):
    rows_a, cols_a = shape(A)
    rows_b, cols_b = shape(B)
    if cols_a != rows_b:
        raise ValueError(f"cannot multiply {rows_a}x{cols_a} by {rows_b}x{cols_b}")
    return [[sum(A[i][k] * B[k][j] for k in range(cols_a)) for j in range(cols_b)]
            for i in range(rows_a)]


def matvec(M, v):
    return [sum(row[j] * v[j] for j in range(len(v))) for row in M]


def as_columns(vectors):
    """A matrix whose COLUMNS are the given vectors, so A c = target."""
    dim = len(vectors[0])
    return [[v[j] for v in vectors] for j in range(dim)]


def print_matrix(label, M, width=9, prec=3):
    print(label)
    for row in M:
        print("    " + " ".join(f"{x:{width}.{prec}f}" for x in row))
    print()


# ---------------------------------------------------------------- the machinery
def rref(M, tol=TOL):
    """Full row reduction. Returns (reduced matrix, pivot column indices)."""
    M = [list(row) for row in M]
    rows, cols = len(M), len(M[0])
    pivot_cols = []
    r = 0
    for c in range(cols):
        best = None
        for i in range(r, rows):
            if abs(M[i][c]) > tol:
                best = i
                break
        if best is None:
            continue                       # this column is free
        M[r], M[best] = M[best], M[r]
        p = M[r][c]
        M[r] = [x / p for x in M[r]]       # scale the pivot to 1
        for i in range(rows):
            if i != r and M[i][c] != 0.0:
                f = M[i][c]
                M[i] = [M[i][k] - f * M[r][k] for k in range(cols)]
        pivot_cols.append(c)
        r += 1
        if r == rows:
            break
    return M, pivot_cols


def rank(M, tol=TOL):
    """Rank = number of pivots in the RREF."""
    _, pivots = rref(M, tol)
    return len(pivots)


def is_independent(vectors, tol=TOL):
    """k vectors are independent iff A (columns = vectors) has k pivots."""
    _, pivots = rref(as_columns(vectors), tol)
    return len(pivots) == len(vectors)


def dependence_relation(vectors, tol=TOL):
    """If dependent, return coefficients c != 0 with sum c_i v_i = 0, else None."""
    M, pivots = rref(as_columns(vectors), tol)
    cols = len(vectors)
    if len(pivots) == cols:
        return None
    free = [c for c in range(cols) if c not in pivots][0]
    c_vec = [0.0] * cols
    c_vec[free] = 1.0
    for row_index, pc in enumerate(pivots):
        c_vec[pc] = -M[row_index][free]
    return c_vec


def greedy_basis(vectors, tol=TOL):
    """Keep a vector only if it adds a new pivot: drop the redundant ones."""
    kept = []
    for v in vectors:
        if not kept or rank(as_columns(kept + [v]), tol) > len(kept):
            kept.append(v)
    return kept


def express_in_basis(basis, target, tol=TOL):
    """Coefficients c with sum c_k basis_k = target, or None if out of the span.

    Solves basis_matrix c = target by RREF on the augmented system, setting the
    free variables (if any) to zero.
    """
    k = len(basis)
    B = as_columns(basis)
    m = len(target)
    M = [[B[i][j] for j in range(k)] + [target[i]] for i in range(m)]
    R, pivots = rref(M, tol)
    for i in range(len(pivots), len(R)):
        if abs(R[i][k]) > tol:
            return None                       # a row [0 ... 0 | nonzero]
    c = [0.0] * k
    for row_index, pc in enumerate(pivots):
        c[pc] = R[row_index][k]
    return c


# ================================================================ the example
# Five samples, three features: a weight, a length, and a width. Every entry is
# divided by 50 so the numbers stay small.
raw = [[12.0, 30.0, 8.0],
       [14.0, 35.0, 9.0],
       [11.0, 27.5, 7.0],
       [15.0, 37.5, 10.0],
       [13.0, 32.5, 8.0]]
A = [[x / 50.0 for x in row] for row in raw]
print("=== Data as a matrix: 5 samples, 3 features ===")
print_matrix("A = (every entry divided by 50)", A, prec=3)
print(f"shape: {len(A)} rows, {len(A[0])} columns")

print()
print("Look at the columns before doing anything to them:")
cols = transpose(A)
for j, c in enumerate(cols):
    print(f"  col{j} = {[round(x, 4) for x in c]}")
ratios1 = [cols[1][i] / cols[0][i] for i in range(5)]
ratios2 = [cols[2][i] / cols[0][i] for i in range(5)]
print(f"col1[i] / col0[i] = {[round(r, 6) for r in ratios1]}")
print(f"col2[i] / col0[i] = {[round(r, 6) for r in ratios2]}")
print("col1 is exactly 2.5 * col0 in every row - the same feature recorded on a")
print("different scale. col2 is NOT: the ratios wander between "
      f"{min(ratios2):.3f} and {max(ratios2):.3f}.")
print("So exactly one of the three features is redundant.")

print()
print("=== Rank = number of pivots in the RREF ===")
R, pivots = rref(A)
print_matrix("rref(A)", R, prec=4)
print(f"pivot columns (0-indexed): {pivots}")
print(f"rank(A) = {rank(A)}")
print(f"With {len(A)} rows and {len(A[0])} columns, at most "
      f"{min(len(A), len(A[0]))} was possible.")

print()
print("=== The dependence, exhibited numerically ===")
rel = dependence_relation(cols)
print("three vectors given, so three coefficients")
print(f"relation c = {[round(x, 6) for x in rel]}")
combined = [sum(rel[j] * cols[j][i] for j in range(len(cols))) for i in range(len(A))]
print(f"sum of c_j * col_j, per row = {[round(x, 10) for x in combined]}")
print("(-2.5)*col0 + 1*col1 + 0*col2 = 0, which is col1 = 2.5*col0.")
print("The algorithm found the relation without being told about it.")

print()
print("=== Independent? Ask the same question with a subset ===")
for name, sub in [
    ("{col0, col1}", cols[:2]),
    ("{col0, col1, col2}", cols[:3]),
    ("{col0, col2}", [cols[0], cols[2]]),
]:
    print(f"{name:20s} independent: {str(is_independent(sub)):5s} rank: "
          f"{rank(as_columns(sub))}")

print()
print("=== A greedy basis: drop the redundant vectors ===")
basis = greedy_basis(cols)
print(f"started with {len(cols)} vectors, kept {len(basis)}")
for k, v in enumerate(basis):
    print(f"  basis[{k}] = {[round(x, 4) for x in v]}")
print(f"their rank is {rank(as_columns(basis))}, equal to their count: "
      f"{rank(as_columns(basis)) == len(basis)}")
print("Now check that the kept vectors still span everything the originals did.")
for j, orig in enumerate(cols):
    c = express_in_basis(basis, orig)
    rebuilt = [sum(c[k] * basis[k][i] for k in range(len(basis))) for i in range(5)]
    print(f"  col{j} = {[round(x, 4) for x in c]} * basis  -> "
          f"{[round(x, 4) for x in rebuilt]}  "
          f"matches: {all(abs(rebuilt[i] - orig[i]) < 1e-9 for i in range(5))}")
print()
print("Note the coefficient on col0 for col1: 2.5, exactly the ratio we read off")
print("by hand. And col2's coefficients are (0, 1) because col2 survived.")

print()
print("=== rank = min(rows, cols) is a ceiling, not an answer ===")
cases = [
    ([[1.0, 2.0], [2.0, 4.0], [3.0, 6.0]], "3x2, all columns proportional"),
    ([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]], "3x3, row0+row2=2*row1"),
    ([[1.0, 0.0], [0.0, 1.0]], "2x2 identity"),
    ([[1.0, 2.0, 3.0, 4.0], [1.0, 1.0, 1.0, 1.0]], "2x4, rank 2 (all rows present)"),
]
for M, label in cases:
    r, c = len(M), len(M[0])
    print(f"{label:38s} {r}x{c}, rank {rank(M)}")
print("The 2x4 case is the interesting one: min(2,4) = 2 and the rank really is 2.")
print("But the 3x3 case has min(3,3) = 3 and rank 2, so counting columns tells")
print("you the maximum and nothing more.")

print()
print("=== Row rank equals column rank ===")
for M, label in [(A, "A (5x3, the data matrix)"),
                 ([[1.0, 2.0], [2.0, 4.0], [3.0, 6.0]], "3x2, rank 1"),
                 ([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]], "3x3, rank 2"),
                 ([[1.0, 2.0, 3.0, 4.0], [1.0, 1.0, 1.0, 1.0]], "2x4, rank 2")]:
    rr = rank(M)
    cr = rank(transpose(M))
    print(f"{label:26s} row rank {rr}, column rank {cr}, agree: {rr == cr}")
print()
print("Not a coincidence and not a numerical fluke: row operations preserve the")
print("column space as well as the row space, so the pivot count is simultaneously")
print("the number of independent rows and the number of independent columns.")
print("Without that fact, 'the rank' would be two different numbers.")
```

### The four fundamental subspaces, and rank as degrees of freedom

```python
"""Block 2: the four fundamental subspaces, and rank as degrees of freedom."""

TOL = 1e-9


# ---------------------------------------------------------------- helpers
def shape(M):
    return len(M), len(M[0])


def transpose(M):
    rows, cols = shape(M)
    return [[M[i][j] for i in range(rows)] for j in range(cols)]


def matmul(A, B):
    rows_a, cols_a = shape(A)
    rows_b, cols_b = shape(B)
    if cols_a != rows_b:
        raise ValueError(f"cannot multiply {rows_a}x{cols_a} by {rows_b}x{cols_b}")
    return [[sum(A[i][k] * B[k][j] for k in range(cols_a)) for j in range(cols_b)]
            for i in range(rows_a)]


def matvec(M, v):
    return [sum(row[j] * v[j] for j in range(len(v))) for row in M]


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def as_columns(vectors):
    dim = len(vectors[0])
    return [[v[j] for v in vectors] for j in range(dim)]


def print_matrix(label, M, width=10, prec=3):
    print(label)
    for row in M:
        print("    " + " ".join(f"{x:{width}.{prec}f}" for x in row))
    print()


def rref(M, tol=TOL):
    M = [list(row) for row in M]
    rows, cols = len(M), len(M[0])
    pivot_cols = []
    r = 0
    for c in range(cols):
        best = None
        for i in range(r, rows):
            if abs(M[i][c]) > tol:
                best = i
                break
        if best is None:
            continue
        M[r], M[best] = M[best], M[r]
        p = M[r][c]
        M[r] = [x / p for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] != 0.0:
                f = M[i][c]
                M[i] = [M[i][k] - f * M[r][k] for k in range(cols)]
        pivot_cols.append(c)
        r += 1
        if r == rows:
            break
    return M, pivot_cols


def rank(M, tol=TOL):
    _, pivots = rref(M, tol)
    return len(pivots)


def nullspace(M, tol=TOL):
    """A basis of ker(M): one vector per free column of rref(M)."""
    R, pivots = rref(M, tol)
    cols = len(M[0])
    free = [c for c in range(cols) if c not in pivots]
    out = []
    for fc in free:
        v = [0.0] * cols
        v[fc] = 1.0
        for row_index, pc in enumerate(pivots):
            v[pc] = -R[row_index][fc]
        out.append(v)
    return out


def rowspace_basis(M, tol=TOL):
    """The nonzero rows of rref(M) are a basis of the row space."""
    R, _ = rref(M, tol)
    return [row[:] for row in R if any(abs(x) > tol for x in row)]


def columnspace_basis(M, tol=TOL):
    """The pivot columns of M, not of rref(M), span the column space."""
    _, pivots = rref(M, tol)
    return [[M[i][pc] for i in range(len(M))] for pc in pivots]


def orthogonality_defect(M, tol=1e-9):
    """Max |v . w| over a basis v of ker(M) and a basis w of rowspace(A).

    For the correct M this is 0: the null space is orthogonal to the row space.
    """
    ns = nullspace(M, tol)
    rb = rowspace_basis(M, tol)
    if not ns or not rb:
        return 0.0
    return max(abs(dot(v, w)) for v in ns for w in rb)


# ================================================================ the example
# A small, deliberately rank-deficient matrix: 5 rows, 3 columns, rank 2.
A = [[0.24, 0.60, 0.16],
     [0.28, 0.70, 0.18],
     [0.22, 0.55, 0.14],
     [0.30, 0.75, 0.20],
     [0.26, 0.65, 0.16]]

m, n = len(A), len(A[0])
r = rank(A)
print(f"A is {m} x {n}, rank {r}.")
print("The Four Fundamental Subspaces. Every one of the four lives in the space its")
print("name implies, and the two that share a space are orthogonal complements.")

print()
print("--- 1. the column space, a subspace of R^m -------------------------")
col_basis = columnspace_basis(A)
print(f"basis (the pivot columns of A itself, {len(col_basis)} of them):")
for k, c in enumerate(col_basis):
    print(f"  c{k} = {[round(x, 4) for x in c]}")
print(f"dimension = {len(col_basis)} = rank = {r}")
print(f"it lives in R^{m}, and every vector in it is a combination of A's columns.")

print()
print("--- 2. the null space of A, a subspace of R^n -----------------------")
ns = nullspace(A)
print(f"basis ({len(ns)} vectors, one per free column):")
for k, v in enumerate(ns):
    print(f"  v{k} = {[round(x, 4) for x in v]}")
print(f"dimension = {len(ns)} = n - rank = {n} - {r} = {n - r}")
print(f"it lives in R^{n}. Every member maps to the zero vector of R^{m}:")
for k, v in enumerate(ns):
    print(f"  A v{k} = {[round(x, 10) for x in matvec(A, v)]}")

print()
print("--- 3. the row space, a subspace of R^n -----------------------------")
row_basis = rowspace_basis(A)
print(f"basis (the nonzero rows of rref(A), {len(row_basis)} of them):")
for k, w in enumerate(row_basis):
    print(f"  w{k} = {[round(x, 4) for x in w]}")
print(f"dimension = {len(row_basis)} = rank = {r}")
print(f"it lives in R^{n}, the SAME space as the null space.")

print()
print("--- 4. the null space of A^T, a subspace of R^m ---------------------")
nsT = nullspace(transpose(A))
print(f"basis ({len(nsT)} vectors):")
for k, w in enumerate(nsT):
    print(f"  z{k} = {[round(x, 4) for x in w]}")
print(f"dimension = {len(nsT)} = m - rank = {m} - {r} = {m - r}")
print(f"it lives in R^{m}, the SAME space as the column space.")
print("Equivalently it is the orthogonal complement of the column space, so it is")
print("the set of vectors orthogonal to every column of A.")

print()
print("--- the orthogonality that ties them together -----------------------")
defect = orthogonality_defect(A)
print(f"max |v . w| over v in a ker(A) basis and w in a rowspace basis: {defect:.3e}")
print("Zero, as it must be: if A v = 0 then each row of A dotted with v is 0, so")
print("v is orthogonal to every row combination, i.e. to the entire row space.")
print("ker(A) = rowspace(A)^perp, and both live in R^n, so they are")
print("complements: the n dimensions of R^n split into r + (n - r).")

print()
print("--- the same orthogonality the other way ---------------------------")
cb = columnspace_basis(A)
zt = nsT
print("max |z . c| over z in a ker(A^T) basis and c in a col(A) basis: "
      f"{max(abs(dot(z, c)) for z in zt for c in cb):.3e}")
print("Same argument with the roles swapped: ker(A^T) = col(A)^perp in R^m.")

print()
print("=== Degrees of freedom: what rank means for a linear system ===")
# Choose a target that is genuinely in the column space: 2*col0 + 3*col2.
b_good = [2.0 * A[i][0] + 3.0 * A[i][2] for i in range(m)]
print(f"b chosen as 2*col0 + 3*col2, so it IS in the column space:")
print(f"  b = {[round(x, 4) for x in b_good]}")
Aug = [A[i] + [b_good[i]] for i in range(m)]
R, pivots = rref(Aug)
print_matrix("rref([A | b])", R, prec=4)
free = [c for c in range(n) if c not in pivots]      # unknowns only, not b
print(f"pivot columns among the {n} unknowns: {pivots}")
print(f"free unknowns: {free}   -> {len(free)} free variable(s)")
print(f"nullity = n - rank = {n} - {r} = {n - r}, and {len(free)} = {n - r} "
      f"{'agree' if len(free) == n - r else 'DISAGREE'}")
x = [0.0] * n
for row_index, pc in enumerate(pivots):
    x[pc] = R[row_index][n]
print(f"setting the free variable x_{free[0]} to 0 gives x = {[round(v, 6) for v in x]}")
d = [0.0] * n
d[free[0]] = 1.0
for row_index, pc in enumerate(pivots):
    d[pc] = -R[row_index][free[0]]
print(f"setting it to 1 gives the null direction {[round(v, 4) for v in d]}")
print("Every solution is that particular point plus t times that direction, for")
print("any real t. So one degree of freedom, exactly one null direction.")

print()
print("Now the same system with a target outside the column space.")
b_bad = [1.0, 0.0, 0.0, 0.0, 0.0]
print(f"b = {b_bad}")
R2, pivots2 = rref([A[i] + [b_bad[i]] for i in range(m)])
print_matrix("rref([A | b])", R2, prec=4)
print(f"pivot columns among the {n} unknowns: {pivots2}")
print(f"b's own column (index {n}) now has a pivot, because the reduction needed a")
print("row that says 0 = 1. Detecting that is the 'no solution' case of lesson 32.")
print()
print("n unknowns, r pivot variables, n - r free variables, and the free variables")
print("are exactly a basis of ker(A). Degrees of freedom consumed = nullity.")

print()
print("=== The size table, in one place ===")
rows = [
    ("column space  col(A)", f"R^{m}", len(col_basis), "rank", r),
    ("null space    ker(A)", f"R^{n}", len(ns), "n - rank", n - r),
    ("row space     row(A)", f"R^{n}", len(row_basis), "rank", r),
    ("left null     ker(A^T)", f"R^{m}", len(nsT), "m - rank", m - r),
]
print(f"{'subspace':22s} {'ambient':>9s} {'dimension':>10s}  {'rule':>10s}  value")
for name, ambient, dim, rule, val in rows:
    print(f"{name:22s} {ambient:>9s} {dim:>10d}  {rule:>10s}  {val}")
print()
print("Check the two dimension sums: rank + (n - rank) = n and")
print(f"rank + (m - rank) = m, i.e. {r} + {n - r} = {n} and {r} + {m - r} = {m}.")
print("The rank appears in all four entries and cancels in both sums, which is")
print("why the four numbers are not four independent pieces of information.")

print()
print("=== A full-rank square matrix: rank = n, nullity = 0, invertibility ===")
P = [[2.0, 1.0], [1.0, 3.0]]
print_matrix("P", P, prec=1)
print(f"rank(P) = {rank(P)}, n = {len(P[0])}, so nullity = {len(P[0]) - rank(P)}")
print(f"basis of ker(P): {nullspace(P)}   <- the empty list means only v = 0")
print("A square matrix has full rank exactly when its null space is {0}, exactly")
print("when it is invertible, exactly when det(P) != 0. See lesson 33.")
```

### With Libraries

Everything above was plain Python nested lists. numpy replaces the whole
RREF with one call — and, importantly, computes rank by a completely
different route, which is worth seeing.

```python
"""Block 3 (With Libraries): rank, SVD rank, and numpy's conventions."""

import numpy as np

A = np.array([[0.24, 0.60, 0.16],
              [0.28, 0.70, 0.18],
              [0.22, 0.55, 0.14],
              [0.30, 0.75, 0.20],
              [0.26, 0.65, 0.16]])

print("=== One call replaces the whole hand-written rref ===")
print(f"np.linalg.matrix_rank(A) = {np.linalg.matrix_rank(A)}")
print()
print("Under the hood that is an SVD, not row reduction: it takes the singular")
print("values and counts how many exceed tol = max(M,N) * eps * sigma_max.")
u, s, vt = np.linalg.svd(A, full_matrices=False)
print(f"singular values = {s}")
tol = max(A.shape) * np.finfo(float).eps * s[0]
print(f"tol = max(shape) * eps * s[0] = {tol:.3e}")
print(f"count of singular values above tol = {int((s > tol).sum())}")
print()
print("Rank by counting nonzero singular values, rank by counting pivots, rank")
print("by counting zero eigenvalues of A^T A: three routes, same integer. The")
print("lesson's rref route is what you write when the matrix is explicit and")
print("small; matrix_rank is what you call when someone hands you a sparse thing")
print("you did not build.")

print()
print("=== The SVD tells you the rank AND the shape of the degeneracy ===")
for i, val in enumerate(s):
    tag = "   <- numerical zero" if val <= tol else ""
    print(f"  sigma_{i} = {val:.6e}{tag}")
print()
print(f"sigma_2 is about {s[2]:.1e}, not exactly 0. The redundant column was built")
print("by multiplying 0.24 by 2.5 in binary floating point, which is not the same")
print("arithmetic as multiplying by 2 and adding 0.6, so the entries do not cancel")
print("bit for bit. The exact rank is 2 and the numerical rank is also 2, because")
print(f"the tolerance has room to absorb a {s[2]:.0e} residue.")
print()
print("That gap between exact rank and numerical rank is the entire reason")
print("matrix_rank takes a tolerance argument. Set the tolerance too high and you")
print("undercount; too low and you start counting noise.")

print()
print("=== Row rank = column rank, checked through numpy ===")
for M, label in [(A, "the 5x3 data matrix"),
                 (np.array([[1.0, 2.0], [2.0, 4.0], [3.0, 6.0]]), "3x2, rank 1"),
                 (np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]),
                  "3x3, rank 2")]:
    print(f"{label:22s} rank(A) = {np.linalg.matrix_rank(M)}, "
          f"rank(A.T) = {np.linalg.matrix_rank(M.T)}")
print()
print("Always the same integer. Not a floating-point accident: it is the")
print("row-rank-equals-column-rank theorem, and it is why the phrase 'the rank'")
print("needs no adjective.")

print()
print("=== numpy.linalg.matrix_rank defaults, and why they bite ===")
M = np.array([[1.0, 0.0],
              [0.0, 1e-18]])
print("M =")
print(M)
print(f"matrix_rank(M)             = {np.linalg.matrix_rank(M)}")
print(f"matrix_rank(M, tol=1e-12)  = {np.linalg.matrix_rank(M, tol=1e-12)}")
print(f"matrix_rank(M, tol=1e-20)  = {np.linalg.matrix_rank(M, tol=1e-20)}")
print()
print("The default tol is max(M,N) * eps * s_max = 2 * 2.2e-16 * 1 = 4.4e-16,")
print("which swallows the 1e-18 direction. numpy says rank 1, and for most")
print("purposes it is right to: that direction is numerical noise and inverting")
print("along it would be meaningless. But if you genuinely need it you must say")
print("so. 'What is the rank' always had a hidden parameter.")

print()
print("=== Rank of a sparse matrix: the sparse tools ===")
try:
    import scipy.sparse as sp
    import scipy.sparse.linalg as spla

    # The adjacency matrix of the path graph 1-2-3-4.
    Adj = sp.csr_matrix(np.array([[0, 1, 0, 0],
                                  [1, 0, 1, 0],
                                  [0, 1, 0, 1],
                                  [0, 0, 1, 0]], dtype=float))
    print(f"adjacency of the path graph 1-2-3-4: shape {Adj.shape}, nnz {Adj.nnz}")
    s_full = np.linalg.svd(Adj.toarray(), compute_uv=False)
    print(f"dense SVD singular values = {np.sort(s_full)[::-1]}")
    print(f"all four are nonzero, so the adjacency matrix has rank 4: det(A) = 1.")
    print("The adjacency matrix of a bipartite graph is singular only when one")
    print("side is empty, because it permutes into a block form [[0, B], [B^T, 0]]")
    print("whose determinant is det(B)^2 up to sign.")
    print()
    us, ss, vts = spla.svds(Adj, k=2)
    print(f"scipy.sparse.linalg.svds(k=2) gives singular values "
          f"{np.sort(ss)[::-1]}")
    print("Same top two, at a fraction of the cost: svds computes a partial SVD")
    print("from a Lanczos-style iteration, so it never forms the full thing.")
    print("Full SVD of a big sparse matrix is hopeless; svds with small k is how")
    print("you get a low-rank approximation cheaply.")
    print()
    # The star graph on 4 nodes: 1 in the middle, 3 leaves. Its adjacency matrix
    # really is singular, because every leaf has degree 1.
    Star = sp.csr_matrix(np.array([[0, 1, 1, 1],
                                   [1, 0, 0, 0],
                                   [1, 0, 0, 0],
                                   [1, 0, 0, 0]], dtype=float))
    print("The star graph K(1,3) instead: hub 1, leaves 2, 3, 4.")
    print("adjacency =\n" + str(Star.toarray()))
    print(f"singular values = {np.sort(np.linalg.svd(Star.toarray(), compute_uv=False))[::-1]}")
    print(f"matrix_rank = {np.linalg.matrix_rank(Star.toarray())}")
    print("The three leaves have identical rows, so two of the four singular values")
    print("are zero and the rank drops to 2. This is a structural dependency in")
    print("the graph itself, not a numerical artifact - no tolerance would fix it")
    print("or need to.")
    print()
    L = sp.csr_matrix(sp.diags(np.array([1.0, 2.0, 2.0, 1.0])) - Adj)
    print("The Laplacian L = D - A of the path graph 1-2-3-4:")
    print(L.toarray())
    ls = np.sort(np.linalg.eigvalsh(L.toarray()))[::-1]
    print(f"eigenvalues = {ls}")
    print("Exactly one is 0 - well, 5.0e-17, machine zero - and the Laplacian of a")
    print("graph has one zero eigenvalue per connected component. That eigenvector")
    print("is the all-ones vector, the constant function on the graph. Lesson 41")
    print("turns this observation into a clustering algorithm.")
except ImportError:
    print("scipy is not installed, so the sparse section is skipped in this run.")
    print("The standard library version of the same idea is in the plain-Python")
    print("blocks above: reduce, count pivots, done.")

print()
print("=== QR: find an independent SUBSET, not just a count ===")
rng = np.random.default_rng(3)
X = rng.normal(size=(6, 3))
X[:, 2] = X[:, 0]                       # exact copy: column 2 IS column 0
print("X has 6 rows and 3 columns, with column 2 copied from column 0.")
Q, R = np.linalg.qr(X, mode="reduced")
print("R =")
print(R)
print(f"|diag(R)| = {np.abs(np.diag(R))}")
print(f"matrix_rank(X) = {np.linalg.matrix_rank(X)}")
print()
print(f"The third diagonal entry of R is {np.abs(np.diag(R))[2]:.1e} rather than")
print("exactly 0 - a zero there would be the exact algebraic statement that this")
print("column is a combination of the previous ones, and floating point cannot")
print("produce the exact 0 because the subtraction accumulates differently on")
print("each row. QR with column pivoting (scipy.linalg.qr with pivoting=True) is")
print("how you find WHICH columns are redundant rather than merely how many.")

print()
print("=== rank + nullity = n, checked numerically ===")
B = np.array([[1.0, 2.0],
              [2.0, 4.0],
              [3.0, 6.0],
              [4.0, 8.0]])
r = np.linalg.matrix_rank(B)
n = B.shape[1]
print("B =\n" + str(B))
print(f"rank = {r}, n = {n}, so nullity should be {n - r}")
vals, vecs = np.linalg.eig(B.T @ B)
order = np.argsort(np.abs(vals))
print(f"eigenvalues of B^T B (ascending by magnitude) = {np.abs(vals[order])}")
for j in order:
    v = vecs[:, j]
    if np.linalg.norm(B @ v) < 1e-8:
        print(f"  eigenvector {np.round(v, 6)} gives B v = {np.round(B @ v, 12)}")
print()
print("One zero eigenvalue, one eigenvector, nullity 1, and rank 1 + 1 = 2 = n.")
print("This is the numerical shadow of the rank-nullity theorem that lesson 35")
print("proves. Worth having both: the theorem for correctness, this check for")
print("the case where your matrix came out of a pipeline and you no longer")
print("entirely trust it.")
```

## Common Mistakes

**Mistake 1: using `min(m, n)` as the rank.**
The wrong version: "this is a `5 × 3` matrix, so its rank is 3." The right version:
`3` is the *ceiling*; the rank is the number of pivots, which here is `2`. The
code's `3 × 3` case makes the point: `[[1,2,3],[4,5,6],[7,8,9]]` has
`row0 + row2 = 2 · row1`, so rank `2`, not `3`. Counting dimensions tells you the
maximum, and only a reduction tells you the actual value. It is tempting because
for a generic matrix with entries drawn independently at random, the rank *is*
`min(m, n)` — so the shortcut works on every random test you write and fails on
every real dataset.

**Mistake 2: reading the pivot columns off the RREF instead of off `A`.**
The wrong version: "the columns of `rref(A)` with a `1` in them are a basis of
`col(A)`." The right version: row operations preserve the row space but they
*change* the column space, so the pivot columns to extract are the columns of the
**original** `A` at the pivot indices. This is why the code has two functions,
`rowspace_basis` and `columnspace_basis`, and only the second one reaches back
into `A`. It is tempting because for a square matrix RREF is
`[I | c]`, and the nonzero columns there look like a perfectly good basis — of
the wrong space. The lesson's worked example makes it concrete: `rref(A)`'s
nonzero columns are `(1, 0, 0, 0, 0)` and `(0, 0, 1, 0, 0)`, which have nothing to
do with the actual column space of a matrix about weights and lengths.

**Mistake 3: extracting the row-space basis from `rref(A)` and using it for
least squares.**
The wrong version: "the row space is the span of `rref`'s nonzero rows, so project
onto those." The right version: the row space is the *right* object to project
onto — that part is Mistake 2's mirror image and it is correct — but the *basis*
you use must be one you can take inner products with correctly. The rows of
`rref(A)` span the right set, so the projection `W x` is right; the mistake is
assuming the basis is unique. It is not: `rref`'s rows are `A`'s rows run through
`E⁻¹`, and if you then compute `x = W⁻¹W W x` you have wasted a triangular solve.
Orthonormalise first, which is what [lesson 38](38_orthogonality_and_least_squares.md)
does with Gram–Schmidt.

**Mistake 4: saying "rank 3, so the system has three solutions."**
The wrong version: reading `r = 3` off a `5 × 3` matrix's shape. The right version:
`r` is the number of *determined* variables, and the number of solutions is
governed by the nullity. A consistent `Ax = b` has either one solution (nullity
`0`) or infinitely many (nullity `> 0`) — never "three solutions", and never a
finite number greater than one, for a linear system. Rank and nullity are
complementary: `r + (n − r) = n`. The code's degrees-of-freedom section shows the
## Formula Sheet

`A` is `m × n` over a field `F`; `a_ij` is row `i`, column `j`; `V, W` are vector
spaces; `S = {v₁,…,v_k} ⊆ V`; `x ∈ Fⁿ`; `y ∈ F^m`; `c ∈ F`; `r` is the rank; `I` is
the identity; `‖·‖` and `·` are the Euclidean norm and dot product from
[lesson 37](37_inner_products_norms_geometry.md).

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$\operatorname{span}(S)$` | `$\{\sum_{i=1}^{k} c_i v_i : c_i \in F\}$` | Everything you can build by scaling and adding members of `S`. Always contains `0`. | "What can this data represent?" |
| independent | `$\sum_i c_i v_i = 0 \Rightarrow c_1 = \dots = c_k = 0$` | No nonzero weighting cancels to zero. Equivalently: no vector is a combination of the others. | "Is this vector needed?" |
| dependent | `$\exists\, (c_1,\dots,c_k) \ne 0$ with `$\sum_i c_i v_i = 0$` | They cancel each other out; at least one is redundant. | Reported as a witness, not just a verdict |
| basis `B` of `V` | `$\operatorname{span}(B) = V$` **and** `B` independent | Spans everything **and** has no redundancy. Both halves are required. | The canonical representative of a subspace |
| `$\dim(V)$` | `$\dim(V) = \lvert B\rvert$` for any basis `B` | How many independent directions. Basis-independent, so any two answers agree. | "How many real factors are in this data?" |
| basis exists | `$\dim V = n \Rightarrow$ a basis of `n` vectors exists | `n` vectors, no redundancy, spans all of `Fⁿ`. | Certifying a matrix as invertible |
| `$\dim V = n \Rightarrow$ `$\dim(\operatorname{span} S) \le \lvert S\rvert$` | More vectors than dimensions is never independent | A free argument needing no computation. Valid for `$\lvert S\rvert > n$` only. | Quick impossibility check |
| extension | independent `S`, `$\dim V = n \Rightarrow$ basis `B` with `S \subseteq B` | You can always add more vectors until you span. | Building a basis from a partial list |
| **rank** | `$\operatorname{rank}(A) = \dim\operatorname{col}(A) = \dim\operatorname{row}(A)$` | Number of independent directions. `A` is `m × n`. | The master diagnostic for any matrix |
| rank bound | `$\operatorname{rank}(A) \le \min(m,n)$` | A ceiling only. **Never** an answer on its own. | The mistake in MCQ Q6 |
| rank by elimination | `$\operatorname{rank}(A) = $` # pivots in the RREF | Count, don't argue. Costs `Θ(mn min(m,n))`. | Every rank computation you write |
| rank by LU | `$\operatorname{rank}(A) = $` # nonzero entries of `U`'s diagonal | Free once you have the factors. | Repeated solves, `scipy.linalg.lu` |
| rank by SVD | `$\operatorname{rank}(A) = \#\{i : \sigma_i > \text{tol}\}$`, `$\text{tol} = \max(m,n)\,\varepsilon\,\sigma_0$` | Counts numerically significant singular values. `A` is `m × n`, so `min(m,n)` singular values. | What `numpy.linalg.matrix_rank` actually does |
| **nullity** | `$\operatorname{nullity}(A) = \dim\ker(A) = n - \operatorname{rank}(A)$` | Degrees of freedom the system leaves open. Requires `A` `m × n`. | "How many solutions are there?" |
| rank–nullity | `$\operatorname{rank}(A) + \operatorname{nullity}(A) = n$` | Constraints plus freedoms equal unknowns. | Every solvability question; proved in [35](35_linear_transformations_and_kernels.md) |
| `$\operatorname{col}(A)$ | `$\operatorname{span}\{$columns of `A`$\}$`, in `F^m` | Every vector `Ax` can produce. | "Which targets are reachable?" |
| `$\operatorname{row}(A)$ | `$\operatorname{span}\{$rows of `A`$\}$`, in `F^n` | Every vector that is orthogonal to `ker(A)`. | Least-sgeometry; normal equations |
| `$\ker(A)$ | `$\{x : Ax = 0\}$`, in `F^n` | Inputs that vanish. One basis vector per free column. | The general solution of `Ax = b` |
| `$\ker(A^{\mathsf T})$ | `$\{y : A^{\mathsf T}y = 0\}$`, in `F^m` | Constraints `Ax = b` must satisfy. | Detecting inconsistency |
| **Fundamental Theorem** | `$\operatorname{col}(A) \oplus \ker(A^{\mathsf T}) = F^m$` and `$\operatorname{row}(A) \oplus \ker(A) = F^n$` | Two complementary pairs, splitting each ambient space by rank `r` and the rest. | Projections, least squares, Gram–Schmidt |
| orthogonality pair | `$\ker(A) = \operatorname{row}(A)^{\perp}$` | An input vanishes exactly when it is orthogonal to every row. | Why the residual of a least-squares fit lies in `ker(A)` |
| orthogonality pair | `$\ker(A^{\mathsf T}) = \operatorname{col}(A)^{\perp}$` | A target is reachable exactly when it is orthogonal to every vector in `ker(Aᵀ)`. | Deciding whether `b` is in `col(A)` |
| dimension table | `col` and `row` have dim `r`; `ker` has dim `n−r`; `ker(Aᵀ)` has dim `m−r` | One rank determines all four. | The whole of lesson 33's failure to localise |
| rank deficient | `$\operatorname{rank}(A) < \min(m,n)$` | Some direction was lost. | Detecting collinear features |
| square equivalence | `$\det(A) \ne 0 \iff \operatorname{rank}(A) = n \iff \ker(A) = \{0\} \iff A$ invertible | Four ways to say one thing. | Ties lesson 33 to this one |
| always solvable | `$\forall b: Ax = b$ solvable $\iff \operatorname{rank}(A) = m$` | Surjective onto the whole codomain. | A map `F^n → F^m` that never fails |
| always unique | `$\forall b: Ax = b$ unique $\iff \operatorname{rank}(A) = n$` | Injective, so no free variables. | A map that never has to choose |
| degrees of freedom | `r` determined, `n − r` free unknowns | Rank is the number of constraints; nullity the number of choices left. | Reading a solution off an RREF |
| general solution | `$x = x_0 + \sum_{i} t_i v_i$`, `v_i` a `ker(A)` basis | A particular point plus a span of directions. | Complete answer for a singular system |
| consistent `iff` | `$Ax = b$ consistent $\iff b \in \operatorname{col}(A) \iff b \perp \ker(A^{\mathsf T})$` | The target must be reachable. | Before you solve, decide whether to bother |
| orthonormal basis | `$x = \sum_i (x\cdot u_i)\,u_i$` with `u_i · u_j = δ_ij` | Coordinates are dot products, no solving. | Numerical stability; see [37](37_inner_products_norms_geometry.md) |
| subspace coordinates | `$x = c_1 v_1 + \dots + c_r v_r$` in a basis `{v_i}` of `W` | The `r` numbers `c_i` identify `x ∈ W` uniquely. | Parametrising a solution set |
| greedy basis cost | `Θ(k)` rank calls, `Θ(k·m·n·min(m,n))` naive | Keep a vector only if it raises the rank. | Feature pruning |

one-and-only-one-mechanism: one free variable means a one-parameter family
`x₀ + t·v`, which is uncountably many solutions.

**Mistake 5: treating `ker(A)` as living in the same space as `col(A)`.**
The wrong version: "the null space is the complement of the column space." The
right version: `ker(A)` is a subspace of `Fⁿ` and `col(A)` is a subspace of
`F^m`; they are not even in the same space unless `m = n`. The complementary pair
is `ker(A)` with `row(A)`, both in `Fⁿ`, and `ker(Aᵀ)` with `col(A)`, both in
`F^m`. It is tempting because the phrase "null space of the column space" is easy
to say and the diagram of four boxes in `Fⁿ` and `F^m` is easy to remember
backwards. Getting it wrong makes `dim ker(A) = m − r`, which can exceed `n` and
is instantly nonsensical — the worked example's `m − r = 5 − 2 = 3` would then
claim a 3-dimensional null space inside `ℝ³` with rank 2, i.e. nullity 3 ≠ `n − r = 1`.

---

## Multiple Choice Questions

**Q1.** Let `S = {v₁, …, v_k} ⊆ ℝⁿ` with `k ≤ n`. Which statement is always
true?

- A) `S` is a basis of `ℝⁿ`
- B) `S` is linearly dependent
- C) `S` spans a space of dimension at most `k`, and is independent exactly when that dimension is `k`
- D) `S` is linearly independent

<details>
<summary>Answer and explanation</summary>

**C) `S` spans a space of dimension at most `k`, and is independent exactly when
that dimension is `k`.**

That is the definition of dimension composed with the definition of independence.
The span is built from `k` generators, so it can have at most `k` dimensions; and
by the lesson's own statement of the theorem, a set of `k` vectors is independent
if and only if its span has dimension `k`. It is also true that every such `S`
extends to a basis of `ℝⁿ` — that is the extension theorem.

- A) is the counting mistake from Mistake 1, in its pure form. `k ≤ n` gives you
  the *permission* to be a basis, not the fact that you are one. The lesson's
  worked example is the counterexample: three vectors in `ℝ⁵` with
  `col1 = 2.5·col0`, so the three span only a 2-dimensional space.
- B) is the same mistake with the sign flipped. `k ≤ n` says nothing at all about
  dependence; the `k > n` theorem only fires in the other direction. Three vectors
  in `ℝ³` can be either independent (the standard basis) or dependent (any set
  containing a scalar multiple), and nothing about the count distinguishes them.
- D) is the mirror of A and equally unjustified. The code's test table shows all
  four combinations occurring at `k ≤ n`: `{col0, col1}` dependent, `{col0, col2}`
  independent, `{col0, col1, col2}` dependent, `I₂` independent.

</details>

**Q2.** The columns of a `5 × 3` matrix satisfy `col1 = 2.5 · col0`, and the
elementwise ratios `col2[i] / col0[i]` are `0.6667, 0.6429, 0.6364, 0.6667,
0.6154`. What is the rank?

- A) 3, because `min(5, 3) = 3`
- B) 2, because `col1` is redundant but `col0` and `col2` are independent
- C) 1, because every column is a multiple of `col0`
- D) It cannot be determined without seeing all the entries

<details>
<summary>Answer and explanation</summary>

**B) 2, because `col1` is redundant but `col0` and `col2` are independent.**

`col1 = 2.5·col0` gives one dependence, so at most 2 columns are independent. The
ratios for `col2` are *not constant* — they wander between `0.615` and `0.667` —
so no single scalar `c` has `col2 = c·col0`, so `col0` and `col2` are
independent. Together: rank exactly 2. The code confirms it, printing
`rank(A) = 2` with pivots in columns 0 and 2.

The test that matters here is **constancy of the ratio**, not its magnitude. Any
value in that range would look like "`about` two-thirds of `col0`" to the eye; the
third decimal place moving from `0.615` to `0.667` across rows is the whole
evidence.

- A) is Mistake 1. `min(m, n)` is a ceiling that a generic random matrix
  happens to attain. Real datasets essentially never do, which is why you have to
  reduce.
- C) is the right instinct taken one step too far. "Every column is a multiple of
  `col0`" requires a *constant* ratio, and the ratios are not constant. Rank
  counts the generators that survive, and `col2` survives. The greedy algorithm
  in the code makes exactly this distinction step by step: keep `col0`, drop
  `col1`, keep `col2`.
- D) is false, and the phrasing of the question shows why: the ratios *were*
  given, and they determine the answer without further computation. A single
  elimination pass settles the same thing in `Θ(mnk)` if you have the full matrix.

</details>

**Q3.** `A` is `4 × 7` with `rank(A) = 3`. Which statement must be true?

- A) `ker(A)` has dimension 3 and `ker(Aᵀ)` has dimension 4
- B) `ker(A)` has dimension 4 and `ker(Aᵀ)` has dimension 1
- C) `ker(A)` has dimension 1 and `ker(Aᵀ)` has dimension 4
- D) `ker(A)` has dimension 3 and `ker(Aᵀ)` has dimension 3

<details>
<summary>Answer and explanation</summary>

**B) `ker(A)` has dimension 4 and `ker(Aᵀ)` has dimension 1.**

    dim ker(A)   = n - rank = 7 - 3 = 4
    dim ker(A^T) = m - rank = 4 - 3 = 1

The formula that matters is *which* of `m` and `n` goes with *which* space.
`ker(A)` is a set of **inputs**, so it lives in `Fⁿ` and its dimension is
`n − rank`. `ker(Aᵀ)` is a set of **outputs**, so it lives in `F^m` and its
dimension is `m − rank`. Getting these two backwards is Mistake 5.

A free sanity check catches every version of this. `ker(A) ⊆ Fⁿ`, so its
dimension can never exceed `n = 7`; and `ker(Aᵀ) ⊆ F⁴`, so *its* dimension can
never exceed `m = 4`. Neither bound is binding here, but both dimensions must
close up: `4 + 3 = 7` and `3 + 1 = 4`. Whenever a pair of dimensions does not sum
to the ambient dimension, one of the formulas has been applied to the wrong space.

- A) puts `rank = 3` itself into the null space, forgetting the subtraction, *and*
  claims `dim ker(Aᵀ) = 4`. A 4-dimensional subspace of `F⁴` is all of `F⁴`,
  which would force `rank = 0`, not 3.
- C) swaps which of `m` and `n` goes with which space. `7 − 3 = 4`, not `4 − 3 = 1`.
  This is the single most common arithmetic error in the four-subspace table, and
  it is invisible on square matrices because there `m = n`.
- D) uses `rank = 3` for the null space and `m − rank = 1` is nowhere in sight,
  so the numbers do not close: `3 + 3 = 6 ≠ 7`.

</details>

**Q4.** Let `A` be a `5 × 5` matrix. `rank(A) = 5` is equivalent to which of the
following?

- A) `det(A) = 0`
- B) `ker(A) = {0}`, and `Ax = b` has a unique solution for every `b`
- C) `ker(A)` is a two-dimensional subspace
- D) `col(A)` is a proper subspace of `ℝ⁵`

<details>
<summary>Answer and explanation</summary>

**B) `ker(A) = {0}`, and `Ax = b` has a unique solution for every `b`.**

`rank(A) = 5 = n`, so by rank–nullity the nullity is `n − 5 = 0`, so `ker(A)` has
dimension 0 and therefore contains only the zero vector. And rank `= n` is
exactly the "always unique" criterion: the map `x ↦ Ax` is injective, so if a
solution exists it is the only one, and with full rank a solution always exists.
For a square matrix this is also `det(A) ≠ 0` and also invertibility — all five
statements in the lesson's chain — but only B appears here correctly.

- A) is exactly backwards. `det(A) = 0` is rank `< 5`. The lesson's equivalence
  chain reads `det(A) ≠ 0 ⟺ rank = n ⟺ ker(A) = {0} ⟺ invertible`, and dropping
  the negation is the trap.
- C) is a rank-3 matrix. If `dim ker(A) = 2` then `rank = 5 − 2 = 3`.
- D) is a rank-`< 5` matrix. `col(A)` has dimension `rank(A) = 5`, and a
  5-dimensional subspace of `ℝ⁵` is `ℝ⁵` itself, so it is not proper.

</details>

**Q5.** Why is `dim ker(A) = n − rank(A)` for an `m × n` matrix?

- A) Because `ker(A) ⊕ row(A) = ℝⁿ`, with `dim row(A) = rank(A)`
- B) Because `ker(A) ⊕ col(A) = ℝⁿ`, with `dim col(A) = rank(A)`
- C) Because the RREF has `m` rows and `m − rank(A)` of them are zero
- D) Because `dim ker(A) = m − rank(A)`, and `m = n` for this purpose

<details>
<summary>Answer and explanation</summary>

**A) Because `ker(A) ⊕ row(A) = ℝⁿ`, with `dim row(A) = rank(A)`.**

The proof is two sentences. `x ∈ ker(A)` means `Ax = 0`, which means every row of
`A` dotted with `x` is zero, which means `x` is orthogonal to every row
combination — so `x ⊥ row(A)` and `ker(A) ⊆ row(A)^⊥`. By the fundamental theorem
`dim row(A)^⊥ = n − dim row(A) = n − rank(A)`. Equivalently, the RREF has
`n − r` free columns and one null basis vector per free column.

The code checks the orthogonality numerically: for the worked example the largest
`|v·w|` over a `ker(A)` basis and a row-space basis is `0.000e+00`.

- B) is Mistake 5, and the most attractive wrong answer on the list because
  `dim col(A) = rank(A)` really is true. But `col(A)` lives in `ℝ^m`, so
  `col(A) ⊕ ker(A)` is not even a sum of subspaces of the same space when
  `m ≠ n` — it is a category error dressed as an identity. The subspace that
  actually pairs with `ker(A)` inside `ℝⁿ` is the **row** space.
- C) confuses rows with columns, and gets the arithmetic backwards besides. The
  RREF of an `m × n` matrix has `m` rows, of which `r` are nonzero — so `m − r`
  is the number of zero *rows*, which says nothing about the null space. The
  number that matters is the number of free *columns*, `n − r`.
- D) is the swapped-`m`-and-`n` error. The formula is `n − r` for `ker(A)` and
  `m − r` for `ker(Aᵀ)`. Applying `m − r` to `ker(A)` gives the right answer only
  when `m = n`, which is precisely why the mistake survives on every square
  matrix you test it on.

</details>

**Q6.** Which of these is *always* a basis of `col(A)`?

- A) The nonzero rows of `rref(A)`
- B) The pivot columns of `rref(A)`
- C) The pivot columns of `A` itself
- D) Any maximal independent subset of the columns

<details>
<summary>Answer and explanation</summary>

**C) The pivot columns of `A` itself.**

Row operations preserve the row space and change the column space, so the columns
to pull out are the original ones at the pivot indices. (D) is also true —
"any maximal independent subset" is the definition of a basis for `col(A)` — but
if you read the question as "which do you compute by row reduction", C is the
one, and C is the option that is *always* the right procedure.)

- A) is Mistake 2's mirror image and also wrong as an answer to "basis of
  `col(A)`": the nonzero rows of `rref(A)` are a basis of the **row** space, which
  lives in `ℝⁿ`, whereas `col(A)` lives in `ℝⁿ`... in the square case these are
  different sets of vectors. For the lesson's `5 × 3` example, `rref(A)`'s
  nonzero columns are `(1,0,0,0,0)` and `(0,0,1,0,0)`, and the true column space
  of a matrix of weights and lengths is nothing like the set of vectors with one
  nonzero entry.
- B) is Mistake 2 itself, and the most seductive option on the list because it is
  only *slightly* wrong. `rref(A)`'s nonzero columns are always independent and
  always the right *number* of them, so any dimension check passes. They span the
  row space reinterpreted as columns, not `col(A)`.
- C) is right because a pivot column of `A` cannot be built from the columns
  before it — if it could, it would not have a pivot — and every non-pivot column
  *can* be built from the pivot ones, as the greedy `express_in_basis` check in
  the code verifies numerically for all three original columns.

</details>

**Q7.** You fit a linear model with 50 features to 3 observations. The design
matrix `X` is `3 × 50`. Which must be true?

- A) `X` has rank 50, so the fit is over-determined and unique
- B) `rank(X) ≤ 3`, so at least 47 features are linear combinations of the others
- C) `rank(X) = 50`, because the features were chosen independently
- D) `rank(X) = 47`

<details>
<summary>Answer and explanation</summary>

**B) `rank(X) ≤ 3`, so at least 47 features are linear combinations of the
others.**

`rank(X) ≤ min(3, 50) = 3`. With 50 columns and at most rank 3, at most 3 columns
can be independent, so at least `50 − 3 = 47` are linear combinations of the rest.
This is why the normal equations `XᵀX w = Xᵀy` in
[lesson 38](38_orthogonality_and_least_squares.md) are unsolvable here:
`XᵀX` is `50 × 50` of rank at most 3, so `det(XᵀX) = 0` by lesson 33's product
rule, and it has no inverse. `numpy.linalg.lstsq` or the pseudoinverse is the
answer, not `solve`.

- A) and C) both claim rank 50, which exceeds `min(3, 50) = 3`. A rank-50 matrix
  needs 50 rows; with 3 rows there are only 3 pivots to be had. This is Mistake 1
  applied in the direction where the ceiling actually bites.
- D) picks `50 − 3 = 47` but attaches it to the rank rather than to the number of
  redundant features. The rank is at most 3, not 47 — `47` is the number of
  columns that are *not* needed, which is a different quantity in a different
  unit.

</details>

**Q8.** `numpy.linalg.matrix_rank` is called on `diag(1, 1e-18)`. What does it
report, and why?

- A) 2, because both diagonal entries are nonzero
- B) 1, because the default tolerance `max(m,n)·ε·σ_max = 4.4e-16` is larger than `1e-18`
- C) 0, because the matrix is nearly the zero matrix
- D) It raises an error, because the matrix is singular

<details>
<summary>Answer and explanation</summary>

**B) 1, because the default tolerance `max(m,n)·ε·σ_max = 4.4e-16` is larger
than `1e-18`.**

The code prints all three: the default gives `1`, `tol=1e-12` gives `1`, and
`tol=1e-20` gives `2`. So the answer is well defined once you fix the tolerance,
which is exactly the lesson's point: `matrix_rank` is not computing rank, it is
computing numerical rank, and the two differ by precisely the tolerance you
choose.

- A) is the exact-arithmetic answer and the trap. `1e-18` is a perfectly ordinary
  double; it is not zero; and in exact arithmetic the matrix is invertible. This
  is the same `det != 0` versus "usable inverse" gap as
  [lesson 33](33_determinant_and_inverse.md)'s underflow example — one scale up.
- C) confuses "below tolerance" with "zero". `σ_max = 1` is far above the
  tolerance, so one singular value counts.
- D) confuses rank deficiency with singularity. `diag(1, 1e-18)` is
  mathematically nonsingular, and `numpy` reports no error — it returns `1`,
  which is a rank estimate, not a diagnosis.

</details>

**Q9.** Let `W ⊆ ℝ³` be a subspace and `v₁, v₂, v₃ ∈ ℝ³`. Which must be true if
`W = span(v₁, v₂, v₃)`?

- A) `dim W = 3`
- B) `v₁, v₂, v₃` are linearly independent
- C) `dim W = 3` if and only if `v₁, v₂, v₃` are linearly independent; otherwise `dim W < 3`
- D) `v₁, v₂, v₃` form a basis of `ℝ³`

<details>
<summary>Answer and explanation</summary>

**C) `dim W = 3` if and only if `v₁, v₂, v₃` are linearly independent; otherwise
`dim W < 3`.**

This is the composition of two facts in the lesson: `W` is spanned by three
vectors, so `dim W ≤ 3`, and a set of three vectors is independent exactly when
its span has dimension 3. Since `W ⊆ ℝ³`, `dim W = 3` would mean `W = ℝ³`.

- A) is the counting mistake again, and it is worse here because `W` is only
  *given* to be a subspace of `ℝ³`, not stated to be all of it. Three vectors can
  span a 1-dimensional line.
- B) is the same error read as independence. Three vectors in `ℝ³` can be
  dependent, and the code's `{col0, col1, col2}` case is exactly that:
  `col1 = 2.5·col0`, so the triple spans a 2-dimensional space.
- D) is A plus an unwarranted promotion. Even if `dim W = 3`, the *basis* is the
  independent subset, and since `W ⊆ ℝ³` a 3-dimensional `W` would mean
  `W = ℝ³` — which is the conclusion, not a hypothesis. In the worked example
  `dim W = 2`, so `{v₁,v₂,v₃}` spans `W` but is not a basis of it.

</details>

**Q10.** The RREF of the worked example's matrix `A` is

    | 1  2.5  0 |
    | 0  0    1 |
    | 0  0    0 |
    | 0  0    0 |
    | 0  0    0 |

A student extracts the basis of `col(A)` as "the nonzero columns of the RREF",
namely `(1,0,0,0,0)` and `(0,0,1,0,0)`. What is wrong, and what is the correct
basis?

- A) Nothing is wrong; those are independent and there are two of them, and
  `rank(A) = 2`
- B) Row operations preserve the row space but not the column space, so the basis
  must be the pivot columns of the **original** `A`: `col0` and `col2`
- C) The RREF's nonzero rows `(1, 2.5, 0)` and `(0, 0, 1)` are the right basis for
  `col(A)`
- D) Both work, because the column space and the row space of a matrix always
  have the same basis vectors

<details>
<summary>Answer and explanation</summary>

**B) Row operations preserve the row space but not the column space, so the basis
must be the pivot columns of the **original** `A`: `col0` and `col2`.**

The student's two vectors are independent and there are exactly two of them, so
every *dimension* check passes — which is why this bug survives casual testing.
They are simply the wrong vectors. `col(A)` is the plane of combinations of
`col0 = (0.24, 0.28, 0.22, 0.30, 0.26)` and
`col2 = (0.16, 0.18, 0.14, 0.20, 0.16)`, vectors with all five components nonzero
and ratios between entries that vary row to row. The student's vectors have
exactly one nonzero component each and span a completely different 2-dimensional
subspace.

The reason is that a row operation `E` is invertible, so `Ax = 0 ⟺ EAx = 0`,
hence `ker(EA) = ker(A)` — the row space is preserved. But the columns themselves
are *rewritten*: `EA`'s column `j` is the combination `Σ_i E_ij (row i of A)`, not
`A`'s column `j`. So the columns change and the column space generally does not
survive.

This is Mistake 2, and it is the most dangerous one in the lesson because it is
the only bug that passes every cheap check.

- A) is the diagnosis itself restated as a defence. "Independent" and "the right
  count" are necessary but not sufficient: a basis of the *wrong* subspace also
  has those properties. Compare the sets directly — they share no vector.
- C) names the RREF's nonzero **rows**, `(1, 2.5, 0)` and `(0, 0, 1)`. Those are
  a correct basis of the **row** space, which lives in `ℝ³`. `col(A)` lives in
  `ℝ⁵`. Using them is a second, independent error stacked on the first.
- D) is false whenever `m ≠ n`, which is exactly this case: `col(A) ⊆ ℝ⁵` and
  `row(A) ⊆ ℝ³` are subspaces of different ambient spaces and cannot share basis
  vectors at all. They even have different dimensions in general — here both are
  2, which is the row-rank-equals-column-rank theorem, not an accident.

</details>

## Subjective Questions

### Short Answer

**Q1. State the basis extraction theorem in both directions, and give the
algorithmic content.**

<details>
<summary>Model answer</summary>

If `S` spans `V`, some subset `B ⊆ S` is a basis for `V`. If `S` is linearly
independent, some superset `B ⊇ S` is a basis for `V` — and such a `B` exists
exactly when `dim V ≥ |S|`.

Both directions are constructive and share one algorithm. Walk through `S` in
order, maintaining a list of kept vectors. For each `v`, test whether `v` is in
the span of what you have kept; if it is not, keep it. Because the kept set is
independent, "not in the span" is equivalent to "adding `v` raises the rank", so
the test is one rank computation. If `S` was spanning, at the end you have an
independent spanning set — a basis. If `S` was independent, you never drop
anything and you have an independent set you can keep extending until it spans.

The implementation is `greedy_basis` in the code: `Θ(k)` rank computations, or
`Θ(k·m·n·min(m,n))` with a naive rank each time.

</details>

**Q2. What is the rank of a matrix, and give three equivalent ways to compute it
that do not involve division.**

<details>
<summary>Model answer</summary>

`rank(A) = dim col(A) = dim row(A)` for an `m × n` matrix `A`. Three equivalent
computations, all division-free:

1. **Count pivots in the RREF** of `A` — `Θ(mnk)` for `k = min(m, n)`. This is
   `rank()` in the code.
2. **Count nonzero entries on the diagonal of `U`** in an LU factorisation
   `A = LU` with partial pivoting. Free once the factors exist, `Θ(n³)` for the
   whole thing, and the routine a solver needs anyway.
3. **Count singular values above a tolerance** in the SVD. This is what
   `numpy.linalg.matrix_rank` does: `tol = max(m, n)·ε·σ_max`, then count.
   `Θ(mn·min(m, n))`.

A fourth, for symmetric matrices: count the nonzero eigenvalues of `A`. All four
return the same integer in exact arithmetic; they differ only in how they behave
in floating point, which is why the choice is a numerical decision rather than a
mathematical one.

</details>

**Q3. Explain why row rank equals column rank, and what would go wrong if it did
not.**

<details>
<summary>Model answer</summary>

Row operations are invertible: `A ↦ EA` with `E` invertible. Since `E` is
invertible, `Ax = 0 ⟺ E(Ax) = 0`, so `ker(EA) = ker(A)`, hence
`col(EA) = col(A)`. So the column space is preserved as well as the row space.
The RREF therefore has the same column rank *and* the same row rank as `A`. In
the RREF the nonzero rows are visibly independent (each has a `1` in a distinct
column), and their number equals the number of pivots — which is simultaneously
the number of independent columns. That is the equality.

If it failed, "the rank" would be two different numbers, and the four-subspace
table would not close up. `col(A)` has `r_col` dimensions and `ker(Aᵀ)` has
`m − r_col`; `ker(A)` has `n − r_row` dimensions and `row(A)` has `r_row`. For
`ℝⁿ` to split into `row(A) ⊕ ker(A)` at all you need `r_row + dim ker(A) = n`,
and the complement argument gives `dim ker(A) = n − r_row`, which is consistent.
The whole apparatus — orthogonal complements, projections, least squares — is
built on the two ranks being one number. In practice the theorem also means you
never have to decide which one to compute: `np.linalg.matrix_rank` returns one
integer and it is both.

</details>

**Q4. Given an `m × n` matrix of rank `r`, state the dimensions of the column
space, the row space, the null space, and the left null space, and say which
spaces each lives in.**

<details>
<summary>Model answer</summary>

    subspace        ambient space   dimension
    col(A)          F^m            r
    row(A)          F^n            r
    ker(A)          F^n            n - r
    ker(A^T)        F^m            m - r

Note the two pairs. `col(A)` and `ker(Aᵀ)` both live in `F^m` and their
dimensions sum to `m`. `row(A)` and `ker(A)` both live in `F^n` and sum to `n`.
The row rank and column rank both equal `r` by the row-rank-equals-column-rank
theorem, so a single number determines all four.

The complementarity is orthogonal, not merely set-theoretic:
`row(A) ⊕ ker(A) = F^n` with `ker(A) = row(A)^⊥`, and
`col(A) ⊕ ker(Aᵀ) = F^m` with `ker(Aᵀ) = col(A)^⊥`. The code verifies both
numerically: the largest `|v·w|` over a `ker(A)` basis and a rowspace basis is
`0.000e+00` for the lesson's example.

</details>

**Q5. Explain why a feature that is a linear combination of other features is
safe to delete, and why a feature that is *nearly* such a combination is not.**

<details>
<summary>Model answer</summary>

A feature column that is a linear combination of the others adds nothing to the
span of the data: `col(A)` is unchanged by deleting it. Any linear functional
computed from the features — a prediction, a projection, a Gram matrix entry — is
unaffected. The rank is unchanged, the nullity is unchanged, and the fitted
coefficients simply redistribute among the surviving features.

"Nearly" is where it goes wrong. If `col₂ = 0.999·col₀`, deleting it still loses
nothing *exactly*, and the rank is still correct. But in floating point the two
columns are numerically indistinguishable at the scale the solver works at, so
an algorithm that keys on a tolerance may already be treating them as one — and a
solver that does not will produce enormous coefficients split between them, with
the individual values meaningless and only their sum stable. This is exactly what
`np.linalg.matrix_rank` is deciding: `diag(1, 1e-18)` returns rank 1, so the
`1e-18` direction is discarded, and if your model actually depends on it, that is
a silent, wrong answer.

The practical rule: delete exactly-redundant columns freely, and delete
nearly-redundant ones only after inspecting the condition number and the
coefficient magnitudes. "Nearly" is a decision, not a computation.

</details>

**Q6. A system `Ax = b` has `rank(A) = 2` and `n = 5`. What can you say about
the number of solutions, and what do you need `b` for?**

<details>
<summary>Model answer</summary>

`nullity = n − rank = 5 − 2 = 3`, so if the system is consistent the solution set
is a 3-parameter family `x = x₀ + t₁v₁ + t₂v₂ + t₃v₃`, with `v₁, v₂, v₃` a basis of
`ker(A)`. Infinitely many solutions, never a finite number greater than one.

What you need `b` for is the one bit: whether the system is consistent at all.
`Ax = b` is solvable iff `b ∈ col(A)`, and rank tells you nothing about `b` —
this is lesson 33's "not exactly one" in another guise. If `b ∉ col(A)` there
are no solutions despite the rank being 2.

The two cases are distinguished by row-reducing the **augmented** matrix: a row
`[0 … 0 | c]` with `c ≠ 0` means inconsistent; the absence of such a row with
three free columns means the 3-parameter family above. Equivalently, by the
fundamental theorem, `b ∈ col(A) ⟺ b ⊥ ker(Aᵀ)`.

</details>

### Long Answer

**Q1. `rank(A) = 3` for a `5 × 7` matrix. Why does this tell you almost nothing
about the data, and what would you need to know to make it useful?**

<details>
<summary>Model answer</summary>

Rank `3` on a `5 × 7` matrix is one integer. What it does tell you is precise and
useful: three columns are independent, and four are linear combinations of them.
The column space is 3-dimensional inside `ℝ⁵`; the null space is 4-dimensional
inside `ℝ⁷`; the row space is 3-dimensional inside `ℝ⁷`; the left null space is
2-dimensional inside `ℝ⁵`.

What it does not tell you is *which* columns are redundant, and that is the part
that matters in practice. `A` could have its first three columns independent and
the last four redundant, or the columns could be interleaved so that dropping any
*prefix* of three fails. The greedy `greedy_basis` code resolves this by keeping
vectors left to right, and it produced `col0` and `col2` for the lesson's
example — dropping `col1` and keeping `col2`, not dropping `col2` and keeping
`col1`. Both bases span `col(A)`, but they are different subsets of your data,
and the choice of which feature to delete is a modelling decision that rank does
not make for you.

Nor does rank say *why* the four are redundant. The lesson's example has an
innocent explanation (col1 and col2 are rescalings of col0 — one physical feature
recorded three times). A rank-3 matrix could equally arise from three genuinely
distinct features with one weird outlier row, in which case deleting a column is
the wrong repair entirely and you should be looking at the row. Rank is a
statement about linear structure; it is silent about cause.

Nor does it say how *well conditioned* the three retained directions are. Rank
counts dimensions; the singular values carry the scale. `diag(1, 1e-18)` has
rank 2 with a second direction that is real but numerically invisible, and the
tolerance in `matrix_rank` decides whether you see it. A rank of 3 is compatible
with singular values `1, 1e-3, 1e-15`, where the third direction is barely worth
keeping, and with `1, 1, 1`, where all three are solid. Same integer, completely
different numerical situation. This is why PCA
([lesson 40](40_svd_and_pca.md)) reports the whole spectrum alongside the rank.

To make rank `3` useful on a `5 × 7` matrix you would want, at minimum: the pivot
column indices, to know *which* columns to keep; the singular values, to know
whether all three directions are worth keeping; and the pivoting/conditioning
information from the factorisation, to know whether a downstream `solve` will be
stable. Concretely that means `scipy.linalg.qr` with column pivoting, or the
`piv` output of `scipy.linalg.lu`, plus `np.linalg.cond`.

The general lesson: rank is the right thing to know first and the wrong thing to
stop at. It is a single integer summarising a genuinely high-dimensional object,
and every interesting question about a deficient matrix — which columns, which
rows, how badly, why — is a question rank cannot answer.

</details>

**Q2. Why is the null space a subspace of `Fⁿ` while the column space is a
subspace of `F^m`, and what goes wrong — concretely, in the code of this lesson —
if you forget?**

<details>
<summary>Model answer</summary>

`x ↦ Ax` maps `Fⁿ → F^m`: the input has `n` components (one per column) and the
output has `m` (one per row). `ker(A) = {x ∈ Fⁿ : Ax = 0}` is a set of **inputs**,
so it sits in `Fⁿ`. `col(A) = {Ax : x ∈ Fⁿ}` is a set of **outputs**, so it sits
in `F^m`. The dimension formulas follow: `dim ker(A) = n − r` because the null
space is a subspace of an `n`-dimensional space; `dim col(A) = r`.

Forgetting this produces two specific, opposite errors, and the lesson's own
worked example is set up to expose both.

**Error one: using `m − r` for the null space.** For the `5 × 3` matrix,
`m − r = 5 − 2 = 3`, so `dim ker(A) = 3` — inside `ℝ³`, which would force
`ker(A) = ℝ³` and `rank = 0`, contradicting `rank = 2`. The internal
inconsistency is the tell: a null space can never have dimension exceeding `n`,
because `ker(A) ⊆ Fⁿ`. That is a free check available before you compute
anything.

**Error two: taking `rref`'s nonzero columns as a basis of `col(A)`.** Row
operations preserve the row space but *change* the column space, so
`rref(A)`'s nonzero columns are the wrong vectors even though there are the right
number of them. In the lesson's example, `rref(A)`'s nonzero columns are
`(1,0,0,0,0)` and `(0,0,1,0,0)` — vectors with a single nonzero entry in
coordinates 0 and 2 — while `col(A)` is the plane of combinations of
`col0 = (0.24,0.28,0.22,0.30,0.26)` and `col2 = (0.16,0.18,0.15,0.19,0.17)`. These
sets have nothing in common, and a dimension check cannot tell you that, which is
why the bug survives casual testing. The code keeps `rowspace_basis` and
`columnspace_basis` as separate functions for exactly this reason: only the
second reaches back into the original `A`.

The fourth row of the fundamental-theorem table is where the confusion usually
comes from: `ker(Aᵀ)` is the orthogonal complement of `col(A)`, and both live in
`F^m`, so they do pair up. `ker(A)` and `row(A)` are the pair inside `Fⁿ`. Getting
the pairing right is what makes the table close up into
`r + (n−r) = n` and `r + (m−r) = m`; getting it wrong gives dimensions that do
not sum to the ambient dimension, and that arithmetic failure is always visible
if you check.

The general principle: in any statement about `Ax`, count `n` things on the input
side and `m` things on the output side, and be suspicious of any formula that
mixes them without saying which side it is on.

</details>

**Q3. A colleague says "rank 47 out of 50, so the model is fine." Give the
strongest case that this is misleading, and explain what you would check
instead.**

<details>
<summary>Model answer</summary>

Rank `47` out of `50` sounds like a nearly-successful fit and is in fact a
statement about the *wrong* thing in two ways.

**First, rank is not goodness of fit.** It measures linear structure in the
design matrix, not how well predictions match. A design matrix of rank 47 can fit
terribly and one of rank 3 can fit perfectly, because rank says how many
independent directions the features span, not how much signal there is. The
quantity that speaks to fit is the residual norm from
[lesson 38](38_orthogonality_and_least_squares.md).

**Second, three of the 50 features are redundant and you do not know which
three.** That is a real cost, not a rounding detail. It means:

- Three of your parameters are not identifiable: the fitted coefficients are
  determined only up to how they redistribute among the redundant group, so
  individual coefficients are meaningless even though predictions are fine.
- The collinearity inflates the variance of the estimates. The variance inflation
  factor for a redundant feature is unbounded — in the limit of exact
  collinearity, `XᵀX` is singular and the normal equations have no solution at
  all, so `np.linalg.solve` raises `LinAlgError`.
- Gradient descent will converge slowly and unstably along the redundant
  direction, because the loss surface is flat there. This is the classic
  "training loss goes down and down but the test loss goes up" story.

**What to check instead, in order:**

1. `np.linalg.matrix_rank(X)` — confirm `47` rather than taking it on trust, and
   note that the number depends on the tolerance.
2. `np.linalg.cond(X)` or `np.linalg.cond(XᵀX)`. This is the real diagnostic.
   The condition number, not the rank, tells you how much the inversion will
   amplify rounding. A rank-47 matrix can have `cond = 1e3` (harmless) or
   `cond = 1e17` (hopeless), and the rank cannot distinguish those.
3. Which columns: pivoted QR (`scipy.linalg.qr(X, pivoting=True)`) or the `piv`
   output of `scipy.linalg.lu`, to find *which* three are redundant. Then look
   at them — collinear features usually have an innocent explanation (one
   measurement recorded twice, a feature that is a linear combination of two
   others) and an innocent repair.
4. The variance inflation factors of the fitted coefficients. A VIF in the
   hundreds localises the problem to specific columns.
5. Standardise the features first. Rank is invariant to column scaling, so
   unscaled data can look fine while the solver drowns; `sklearn`'s
   `StandardScaler` and `Ridge` regressor's internal solver exist because of
   this.

The general point: rank tells you *whether* a matrix is deficient, and the
condition number tells you whether you should care. Confusing the two is how a
model ships with silently unstable coefficients.

</details>

**Q4. Explain the greedy basis algorithm, prove it works, and say when the order
of the input vectors changes the answer.**

<details>
<summary>Model answer</summary>

**The algorithm.** Maintain a list `kept`, initially empty. For each `v` in the
input order, if `kept` is empty or adding `v` strictly increases
`rank(kept ∪ {v})`, append `v` to `kept`. Return `kept`. That is
`greedy_basis` in the code; for the lesson's example it keeps `col0`, drops
`col1`, keeps `col2`.

**Why the test is the right one.** After `k` steps, `kept` has `k` elements and
they are linearly independent. Proof by induction: it is vacuous at `k = 0`; if
`kept` is independent and we add `v` exactly when `rank` increases, then `rank`
goes from `k` to `k + 1` and `kept ∪ {v}` has `k + 1` independent vectors. The
independence of `kept ∪ {v}` is precisely what the rank increase certifies — a set
of `k+1` vectors in a space of dimension `k+1` is a basis, hence independent.

**Why it spans.** If the input `S` spans, then every `v ∈ S` is in
`span(S) = span(kept ∪ rejected)`. Any rejected `v` was in `span(kept)` *at the
time*, and `kept` only grows, so `v ∈ span(kept_final)`. Hence `span(kept_final)`
contains every member of `S`, and therefore all of `span(S) = S`. So `kept_final`
is an independent spanning set: a basis. Termination is automatic because each
step either grows `kept` or discards, and `kept` can grow at most `dim V` times.

Cost: `k` rank computations, `Θ(k·m·n·min(m,n))` with a naive rank each, or
`Θ(mnk)` if you carry the elimination forward incrementally instead of
restarting — which is what a real implementation does.

**When the order matters — and it does.** The output depends on the input order,
and the lesson's example shows it. In the order `col0, col1, col2` the algorithm
keeps `col0`, rejects `col1` (since `col1 = 2.5·col0`), and keeps `col2`. In the
order `col0, col2, col1` it keeps `col0`, keeps `col2` (its ratios to `col0` are
not constant, so it is independent of `col0`), and rejects `col1` — same answer
here. But in the order `col1, col0, col2` it keeps `col1`, keeps `col0`
(`col0 = 0.4·col1` is independent of `col1`), and rejects `col2`, giving basis
`{col1, col0}` rather than `{col0, col2}`. Both are valid bases of `col(A)`;
neither is canonical. Exercise 3 works this through with four vectors in `ℝ³`.

**Why that matters, and what fixes it.** Different bases are genuinely different
*descriptions*, so which features you keep can differ — and which features you
keep is a modelling decision, not a mathematical output. In the feature-selection
setting, keeping `col0, col2` versus `col1, col0` may mean keeping a physically
meaningful feature versus a duplicate of one.

Two standard repairs. **Pivoted QR** (`scipy.linalg.qr(M, pivoting=True)`)
repeatedly picks the column with the largest remaining norm, which tends to pick
the best-conditioned representatives and is what LAPACK does internally.
**Column-pivoted LU** gives the permutation `piv` directly, listing the pivot
columns in order. Both still depend on the choice of norm and on numerical
details; neither is canonical in the way the RREF is. The honest summary is that
a basis of a subspace is never unique, only its *size* is, and any algorithm that
hands you specific vectors is making a choice you should be willing to explain.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — rank of a design matrix, and which feature is redundant.** For

    A = | 1  2  3  6 |
        | 2  1  4  8 |
        | 0  3  1  7 |
        | 5  4  2 15 |
        | 1  0  2  3 |

(a) Find `rank(A)` by counting pivots, showing the reduction. (b) Find a basis of
`col(A)`. (c) Compute `dim ker(A)` and `dim ker(Aᵀ)`.

<details>
<summary>Solution</summary>

**(a)** Pivot on row 0 and clear column 0:

    R_1 <- R_1 - 2 R_0 :  (2,1,4,8) - 2(1,2,3,6) = (0, -3, -2, -4)
    R_2                  (0, 3, 1, 7)                    (already 0)
    R_3 <- R_3 - 5 R_0 :  (5,4,2,15) - 5(1,2,3,6) = (0, -6, -13, -15)
    R_4 <- R_4 - R_0    :  (1,0,2,3) - (1,2,3,6)    = (0, -2, -1, -3)

    | 1   2   3    6 |
    | 0  -3  -2   -4 |
    | 0   3   1    7 |
    | 0  -6 -13  -15 |
    | 0  -2  -1   -3 |

Pivot on `−3` in column 1 and clear:

    R_2 <- R_2 + R_1      :  (0, 3, 1, 7) + (0,-3,-2,-4) = (0, 0, -1, 3)
    R_3 <- R_3 - 2 R_1     :  (0,-6,-13,-15) - 2(0,-3,-2,-4) = (0, 0, -9, -7)
    R_4 <- R_4 - (2/3) R_1 :  (0,-2,-1,-3) - (2/3)(0,-3,-2,-4) = (0, 0, 1/3, -1/3)

    | 1   2   3    6 |
    | 0  -3  -2   -4 |
    | 0   0  -1    3 |
    | 0   0  -9   -7 |
    | 0   0   1/3 -1/3|

Pivot on `−1` in column 2 and clear:

    R_3 <- R_3 - 9 R_2      :  (0,0,-9,-7) - 9(0,0,-1,3) = (0, 0, 0, -34)
    R_4 <- R_4 + (1/3) R_2   :  (0,0,1/3,-1/3) + (1/3)(0,0,-1,3) = (0, 0, 0, 2/3)

Column 3 now holds `6`, `−4`, `3`, `−34`, `2/3`; the last two rows are nonzero, so
column 3 pivots too.

**Four pivots, in columns 0, 1, 2, 3. So `rank(A) = 4`**, and
`min(5, 4) = 4` — full column rank, so every column is needed.

**(b)** The pivot columns of `A` itself are columns 0, 1, 2, 3, i.e. all of them:

    col0 = (1, 2, 0, 5, 1)
    col1 = (2, 1, 3, 4, 0)
    col2 = (3, 4, 1, 2, 2)
    col3 = (6, 8, 7, 15, 3)

so `col(A) = ℝ⁵`... no: `col(A) ⊆ ℝ⁵` has dimension 4, so it is a hyperplane in
`ℝ⁵`, and the four columns above are its basis.

There is **no redundant column**, which is worth stating plainly: a rank-4 result
on a `5 × 4` matrix means full column rank, so no feature can be deleted. (Had
the problem intended a redundant column, the last row or the last column would
have needed to be a combination of the others — the elimination would then have
produced a zero row here.)

**(c)** `A` is `m × n` with `m = 5`, `n = 4`, `r = 4`:

    dim ker(A)   = n - r = 4 - 4 = 0
    dim ker(A^T) = m - r = 5 - 4 = 1

Read off the reduction: `ker(A)` is trivial because there is no free column in
the RREF, and `dim ker(Aᵀ) = 1` because one of the five rows must be a
combination of the other four. The reduction is consistent with both: four
independent rows plus a fifth that row-reduces to zero.

Note the shape of the answer. This matrix has **full column rank**, which means
`Ax = b` has a solution for every `b ∈ ℝ⁴` and either none or infinitely many —
never exactly one, because `dim ker(A) = 0` means a unique solution exists but
only if one exists. What it *does* guarantee is that the map `ℝ⁴ → ℝ⁵` is
injective, so distinct inputs give distinct outputs.

</details>

**Challenge — Exercise 2 — a matrix with one genuine redundancy, all four
subspaces computed.** Let

    A = | 1  2  0  3 |
        | 2  4  1  7 |
        | 3  6  2 12 |
        | 0  0  3  9 |

Note first that `col1 = 2 · col0` exactly. (a) Find `rank(A)`. (b) Give a basis of
`col(A)`. (c) Give a basis of `row(A)`. (d) Give a basis of `ker(A)`. (e) Give a
basis of `ker(Aᵀ)`. (f) Verify both orthogonal-complement claims numerically and
check both dimension sums.

<details>
<summary>Solution</summary>

**(a)** Pivot on row 0 and clear column 0:

    R_1 <- R_1 - 2 R_0 :  (2,4,1,7) - 2(1,2,0,3) = (0, 0, 1, 1)
    R_2 <- R_2 - 3 R_0 :  (3,6,2,12) - 3(1,2,0,3) = (0, 0, 2, 3)
    R_3                  (0, 0, 3, 9)                    (already 0)

    | 1  2  0  3 |
    | 0  0  1  1 |
    | 0  0  2  3 |
    | 0  0  3  9 |

Clear column 2 using row 1:

    R_2 <- R_2 - 2 R_1 :  (0,0,2,3) - 2(0,0,1,1) = (0, 0, 0, 1)
    R_3 <- R_3 - 3 R_1 :  (0,0,3,9) - 3(0,0,1,1) = (0, 0, 0, 6)

    | 1  2  0  3 |
    | 0  0  1  1 |
    | 0  0  0  1 |
    | 0  0  0  6 |

Column 3 has `3`, `1`, `1`, `6`, all nonzero below the first two pivots, so it
pivots. **`rank(A) = 3`**, pivots in columns 0, 2, 3, with **column 1 free** —
which is the computational signature of `col1 = 2·col0`.

The RREF, for later use, is

    | 1  2  0  0 |
    | 0  0  1  0 |
    | 0  0  0  1 |
    | 0  0  0  0 |

**(b)** `dim col(A) = 3` and `col(A) ⊆ ℝ⁴`. The pivot columns of **`A` itself**
are columns 0, 2, 3:

    col0 = (1, 2, 3, 0)
    col2 = (0, 1, 2, 3)
    col3 = (3, 7, 12, 9)

Note this is *not* `col1`, even though column 1 is where the redundancy sits:
the pivot columns are what survives, and `col1` did not.

**(c)** `dim row(A) = 3` and `row(A) ⊆ ℝ⁴`. A basis is the nonzero rows of the
RREF:

    (1, 2, 0, 0),  (0, 0, 1, 0),  (0, 0, 0, 1)

And here is Mistake 2 in numbers: the nonzero **columns** of that same RREF are
`(1,0,0,0)`, `(0,0,1,0)`, `(0,0,0,1)` — three vectors that are independent and
the right *number*, but a different set from the column space of a matrix about
rows of measurements. Any dimension check passes; the vectors are wrong.

**(d)** `dim ker(A) = n − rank = 4 − 3 = 1`, and column 1 is the free one. From
the RREF: `x₁` is free, `x₀ + 2x₁ = 0`, `x₂ = 0`, `x₃ = 0`. Set `x₁ = 1`:

    ker(A) = span{ (-2, 1, 0, 0) }

Verify: `A(-2, 1, 0, 0) = (-2 + 2, -4 + 4, -6 + 6, 0 + 0) = (0, 0, 0, 0)` ✓

**(e)** `dim ker(Aᵀ) = m − rank = 4 − 3 = 1`, so one vector. Solve `Aᵀy = 0`, i.e.
dot `y` with each column. The columns are `(1,2,3,0)`, `(2,4,6,0)`, `(0,1,2,3)`,
`(3,7,12,9)`. The first two give the *same* equation, `y₀ + 2y₁ + 3y₂ = 0`,
because `col1 = 2 col0`.

From `y₀ = −2y₁ − 3y₂` and `y₁ = −2y₂ − 3y₃` (from the third column) and the
fourth, the system reduces to `6y₃ = 0`, so `y₃ = 0`, `y₁ = −2y₂`, `y₀ = y₂`.
Take `y₂ = 1`:

    ker(A^T) = span{ (1, -2, 1, 0) }

Verify against all four columns:
- col0 `(1,2,3,0)`: `1 − 4 + 3 + 0 = 0` ✓
- col1 `(2,4,6,0)`: `2 − 8 + 6 + 0 = 0` ✓
- col2 `(0,1,2,3)`: `0 − 2 + 2 + 0 = 0` ✓
- col3 `(3,7,12,9)`: `3 − 14 + 12 + 0 = 1` ✗

Off by 1 on col3, which means either the vector or the column is misread. Read
col3 off the matrix again: row 0 gives `3`, row 1 gives `7`, row 2 gives `12`,
row 3 gives `9`. And `3·1 + 7·(−2) + 12·1 + 9·0 = 3 − 14 + 12 = 1`.

So `(1, −2, 1, 0)` is **not** in `ker(Aᵀ)`. Yet `dim ker(Aᵀ) = m − rank = 1`, so
a nonzero vector must exist. The error is in my solving: I used `y₁ = −2y₂ − 3y₃`
from the third column, but the third column `(0,1,2,3)` gives
`y₁ + 2y₂ + 3y₃ = 0` — and with `y₃ = 0` that reads `y₁ = −2y₂`. That much is
right. The failing equation is the fourth, so let me redo the algebra including
it from the start rather than assuming the reduction.

Equations, with `y = (y₀, y₁, y₂, y₃)`:

    (i)   y₀ + 2y₁ + 3y₂ = 0
    (ii)  2y₀ + 4y₁ + 6y₂ = 0      <- same as (i)
    (iii) y₁ + 2y₂ + 3y₃ = 0
    (iv)  3y₀ + 7y₁ + 12y₂ + 9y₃ = 0

From (i): `y₀ = −2y₁ − 3y₂`. Into (iv):
`3(−2y₁ − 3y₂) + 7y₁ + 12y₂ + 9y₃ = 0`
`−6y₁ − 9y₂ + 7y₁ + 12y₂ + 9y₃ = 0`
`y₁ + 3y₂ + 9y₃ = 0`        ... (v)

From (iii): `y₁ = −2y₂ − 3y₃`. Into (v):
`(−2y₂ − 3y₃) + 3y₂ + 9y₃ = 6y₃ = 0`, so `y₃ = 0`.

Then `y₁ = −2y₂` and `y₀ = −2(−2y₂) − 3y₂ = 4y₂ − 3y₂ = y₂`. That gives
`y = y₂·(1, −2, 1, 0)`, which fails (iv). Since the derivation used (iv), the
only escape is that `y₃ = 0` is wrong, i.e. `6y₃ = 0` is wrong, i.e. one of the
coefficients above is wrong.

Recheck the substitution into (v). (v) came from (iv) with `y₀` replaced. `3·(−2y₁)
= −6y₁` ✓; `3·(−3y₂) = −9y₂` ✓; plus `7y₁` gives `y₁` ✓; `−9y₂ + 12y₂ = 3y₂` ✓;
plus `9y₃` ✓. So (v) is right.

Recheck (iii): `y·(0,1,2,3) = y₁ + 2y₂ + 3y₃` ✓.

So `−2y₂ − 3y₃ + 3y₂ + 9y₃ = y₂ + 6y₃`, **not** `6y₃`. I dropped the `y₂`.
Then `y₂ = −6y₃`, `y₁ = −2(−6y₃) − 3y₃ = 12y₃ − 3y₃ = 9y₃`, and
`y₀ = −2(9y₃) − 3(−6y₃) = −18y₃ + 18y₃ = 0`.

Take `y₃ = 1`: `y = (0, 9, −6, 1)`.

Verify against all four columns:
- col0 `(1,2,3,0)`: `0 + 18 − 18 + 0 = 0` ✓
- col1 `(2,4,6,0)`: `0 + 36 − 36 + 0 = 0` ✓
- col2 `(0,1,2,3)`: `0 + 9 − 12 + 3 = 0` ✓
- col3 `(3,7,12,9)`: `0 + 63 − 72 + 9 = 0` ✓

**All four zero.** So `ker(Aᵀ) = span{ (0, 9, −6, 1) }`, of dimension 1 ✓

**(f)** First the orthogonality `ker(A) ⊥ row(A)`. Dot `(−2, 1, 0, 0)` with each
row-space basis vector:

    (-2,1,0,0) . (1,2,0,0) = -2 + 2 = 0   ✓
    (-2,1,0,0) . (0,0,1,0) = 0           ✓
    (-2,1,0,0) . (0,0,0,1) = 0           ✓

All zero, as the theorem requires.

Then `ker(Aᵀ) ⊥ col(A)`. Dot `(0, 9, −6, 1)` with each column-space basis vector:

    (0,9,-6,1) . (1,2,3,0)    =  0 + 18 - 18 + 0  = 0   ✓
    (0,9,-6,1) . (0,1,2,3)    =  0 +  9 - 12 + 3  = 0   ✓
    (0,9,-6,1) . (3,7,12,9)   =  0 + 63 - 72 + 9  = 0   ✓

All zero.

And the dimension sums:

    dim ker(A) + dim row(A)    = 1 + 3 = 4 = n   ✓
    dim ker(A^T) + dim col(A)  = 1 + 3 = 4 = m   ✓

Both close up, and the `1 + 3` is the same `r + (n − r)` = `r + (m − r)` = `3 + 1`
wearing different labels — because here `m = n = 4`. For a matrix with `m ≠ n`
the two sums are different, which is precisely the confusion MCQ Q3 tests.

**A note on the arithmetic above.** Twice in this solution I asserted a rank
conclusion from an elimination whose arithmetic was wrong, and each time the
verification step caught it — first the rank-4 claim that the free column
contradicted, then the `y = (1,−2,1,0)` that failed col3. In both cases the
detector was a *substitution into the original matrix*, not a re-derivation.
That is the habit worth keeping: after any hand elimination, plug the claimed
null vectors back into `A` and dot the claimed bases. It takes four dot products
and it catches everything.

</details>

**[ ] Exercise 3 — greedy basis, and why the answer depends on input order.** Take

    v1 = (1, 0, 1)     v2 = (0, 1, 1)     v3 = (1, 1, 2)     v4 = (1, 2, 3)

(a) Notice the relations among these four by hand. (b) Apply the greedy algorithm
in the order `v1, v2, v3, v4` and report what it keeps. (c) Apply it in the
order `v4, v3, v2, v1` and report what it keeps. (d) Show both answers span the
same space and both are independent. (e) Give the two independent null vectors of
the matrix whose columns are `v1, v2, v3, v4`.

<details>
<summary>Solution</summary>

**(a)** Compare components.

`v3 = v1 + v2`: `(1,0,1) + (0,1,1) = (1,1,2)` ✓

`v4 = v1 + 2v2`: `(1,0,1) + 2(0,1,1) = (1,2,3)` ✓

So all four lie in `span(v1, v2)`, and two relations exist:

    -1*v1 - 1*v2 + 1*v3 +  0*v4 = 0
    -1*v1 - 2*v2 + 0*v3 +  1*v4 = 0

The span of all four is therefore `span(v1, v2)`, and since `v1, v2` are clearly
independent (`a v1 + b v2 = 0` forces `a = 0` from coordinate 0 and `b = 0` from
coordinate 1), `dim = 2`.

**(b)** Order `v1, v2, v3, v4`:
- `v1`: keep (rank 0 → 1)
- `v2`: `rank({v1,v2}) = 2`, increase, **keep**
- `v3`: `v3 = v1 + v2`, so rank stays 2, **drop**
- `v4`: `v4 = v1 + 2v2`, so rank stays 2, **drop**

Keeps `{v1, v2}`, size 2.

**(c)** Order `v4, v3, v2, v1`:
- `v4`: keep (rank 0 → 1)
- `v3`: is `v3` in `span(v4)`? No — `v4 = (1,2,3)` and `v3 = (1,1,2)` are not
  multiples (ratios `1, 0.5, 0.667`). So rank 2, **keep**
- `v2`: is `v2` in `span(v4, v3)`? `v4 − v3 = (0,1,1) = v2`. Yes, so rank stays
  2, **drop**
- `v1`: is `v1` in `span(v4, v3)`? `v3 − v2` would give it, but `v2` was not
  kept. Directly: `a v4 + b v3 = (a+b, 2a+b, 3a+2b) = (1,0,1)`. From
  `2a + b = 0` and `a + b = 1`: subtracting gives `a = −1`, then `b = 2`, and the
  third coordinate is `3(−1) + 2(2) = 1` ✓. So `v1 = −v4 + 2v3`, rank stays 2,
  **drop**

Keeps `{v4, v3}`, size 2.

**Different vectors, same count.** The greedy algorithm's output depends on the
order of the input. That is not a bug — dimension is basis-independent, but the
*particular* basis is not.

**(d)** Both span the same space.

From (b): `span(v1, v2)` contains `v3` and `v4` because `v3 = v1 + v2` and
`v4 = v1 + 2v2`. So `span(v1,v2,v3,v4) = span(v1,v2)`.

From (c): `span(v4, v3)` contains `v2 = v4 − v3` and `v1 = 2v3 − v4`. So
`span(v4,v3,v1,v2) = span(v4,v3)`.

Are `span(v1,v2)` and `span(v4,v3)` the same? `v3 = v1 + v2` and `v4 = v1 + 2v2`
are in `span(v1,v2)`, so `span(v4,v3) ⊆ span(v1,v2)`. Conversely `v1 = 2v3 − v4`
and `v2 = v4 − v3` are in `span(v4,v3)`, so `span(v1,v2) ⊆ span(v4,v3)`. Equal ✓

Independence. `{v1, v2}`: `a(1,0,1) + b(0,1,1) = 0` gives `a = 0` and `b = 0` ✓
`{v4, v3}`: `a(1,2,3) + b(1,1,2) = 0` gives `a + b = 0` and `2a + b = 0` from
coordinates 0 and 1, hence `a = 0`, `b = 0` ✓

So both are bases of the same 2-dimensional subspace.

**(e)** The matrix with these columns is `3 × 4` of rank 2, so
`dim ker = 4 − 2 = 2`, one basis vector per free column. Solve
`a v1 + b v2 + c v3 + d v4 = 0`:

    coord 0:  a + c + d = 0
    coord 1:  b + c + 2d = 0
    coord 2:  a + b + 2c + 3d = 0

Set `c = 1, d = 0`: `a = −1`, `b = −1`, and coord 2 gives `−1 − 1 + 2 + 0 = 0` ✓.
So one null vector is `(-1, -1, 1, 0)` — which is exactly the relation from (a).

Set `c = 0, d = 1`: `a = −1`, `b = −2`, and coord 2 gives
`−1 − 2 + 0 + 3 = 0` ✓. So the second is `(-1, -2, 0, 1)`.

    ker = span{ (-1, -1, 1, 0),  (-1, -2, 0, 1) }

Both match the relations found by hand in (a). The two are independent: the third
coordinate of the first forces the first coefficient to 0, and the fourth
coordinate of the second forces the second to 0.

**(f) — the lesson.** A basis of a subspace is *not unique*, only its size is.
Two different greedy passes gave `{v1, v2}` and `{v4, v3}` for the same space.
In a feature-selection setting that is not a formality — which features you keep
can differ, and if they are physically meaningful measurements the choice is a
modelling decision. Pivoted QR (`scipy.linalg.qr(M, pivoting=True)`) is the
standard repair; it still depends on a norm and on numerical details, so the
honest summary is that any algorithm handing you specific vectors is making a
choice you should be ready to explain.

</details>

**[ ] Exercise 4 — the degrees-of-freedom reading of rank.** Let `A` be the `5 × 3`
matrix from the worked example, so `col1 = 2.5·col0` and `rank(A) = 2`, and let

    b = 2·col0 + 3·col2 = (0.96, 1.10, 0.86, 1.20, 1.00)

(a) Solve `Ax = b`. (b) Give three more solutions. (c) Find a `b'` for which
`Ax = b'` has no solution. (d) Explain, purely in terms of rank and nullity, why
(a) and (b) cannot be the only solutions and why (c) exists.

<details>
<summary>Solution</summary>

**(a)** Row-reduce `[A | b]`. Since `col1 = 2.5·col0` and `col0, col2` are
independent, any solution has the form `x = (x₀, x₁, x₂)` with
`Ax = x₀col0 + x₁(2.5col0) + x₂col2 = (x₀ + 2.5x₁)col0 + x₂col2`. Matching
against `b = 2·col0 + 3·col2` and using the independence of `col0, col2`:

    x₂ = 3            and    x₀ + 2.5x₁ = 2

so `x₀ = 2 − 2.5x₁` and

    x = (2 - 2.5 t,  t,  3),    t ∈ ℝ

At `t = 0`: `x = (2, 0, 3)`. Check directly:
`2·col0 + 3·col2 = (0.48+0.48, 0.56+0.54, 0.44+0.42, 0.60+0.60, 0.52+0.48)
= (0.96, 1.10, 0.86, 1.20, 1.00) = b` ✓

**(b)** Three more, from `t = 1, 2, 3`:

    t = 1 :  x = (-0.5, 1, 3)     A x = -0.5 col0 + 2.5 col0 + 3 col2 = 2 col0 + 3 col2 = b ✓
    t = 2 :  x = (-3.0, 2, 3)     A x = -3 col0 + 2(2.5 col0) + 3 col2
                                    = -3 col0 + 5 col0 + 3 col2 = 2 col0 + 3 col2 = b ✓
    t = 3 :  x = (-5.5, 3, 3)     A x = -5.5 col0 + 7.5 col0 + 3 col2 = 2 col0 + 3 col2 = b ✓

**(c)** Take `b' = (1, 0, 0, 0, 0)`. Is it in `col(A)`? Any vector in `col(A)` is
`s·col0 + t·col2`. Its first two coordinates are `(0.24s + 0.16t, 0.28s + 0.18t)`.
Setting these equal to `b'`'s `(1, 0)`:

    0.24s + 0.16t = 1
    0.28s + 0.18t = 0

The determinant is `0.24·0.18 − 0.16·0.28 = 0.0432 − 0.0448 = −0.0016 ≠ 0`, so
`s, t` are uniquely determined: `s = 0.18·1/−0.0016 = −112.5` and
`t = (0.24·0 − 0.28·1)/(−0.0016) = −0.28/(−0.0016) = 175`. The third coordinate
would then be `−112.5·0.22 + 175·0.14 = −24.75 + 24.5 = −0.25`, but `b'₃ = 0`.

Mismatch, so `b' ∉ col(A)` and **`Ax = b'` has no solution**.

Confirming structurally: the RREF of `[A | b']` needs a third pivot, and it lands
in `b'`'s own column (index 3) — the signature of the row `0 = 1`. The code prints
exactly that.

**(d)** `rank(A) = 2` and `n = 3`, so `nullity = n − rank = 1`. That means
`ker(A) = span{ (−2.5, 1, 0) }` is a one-dimensional subspace. If `x₀` is any
solution then so is `x₀ + t·(−2.5, 1, 0)` for every real `t`, because

    A(x₀ + t v) = A x₀ + t (A v) = b + t·0 = b

So a linear system over `ℝ` has either one solution or infinitely many — never a
finite number greater than one. One degree of freedom *is* an infinite
one-parameter family. And the `t = 0, 1, 2, 3` solutions in (a) and (b) are just
four of them; nothing distinguishes them, which is why picking `t = 0` is a choice
rather than a fact.

For (c): `Ax = b'` is solvable exactly when `b' ∈ col(A)`. Now
`dim col(A) = rank(A) = 2` inside a 5-dimensional `ℝ⁵`, so `col(A)` is a proper
subspace and most targets miss it. The complement `ker(Aᵀ)` has dimension
`m − rank = 5 − 2 = 3`, so the set of unreachable targets is itself 3-dimensional —
a whole hyperplane's worth of `b` that will fail. The code finds that complement
explicitly.

So one number, `r = 2`, does all of the work: it says there are 2 determined
variables and 1 free one (parts a, b), and it says the reachable set is
2-dimensional inside `ℝ⁵` (part c). `rank + nullity = n` is the whole of it.

</details>

**[ ] Exercise 5 — proving row rank equals column rank for one specific matrix,
two ways.** Let

    B = | 1  2  0 |
        | 2  4  1 |
        | 3  6  2 |
        | 0  0  3 |

(a) Compute the row rank by counting pivots in `rref(B)`. (b) Compute the column
rank by row-reducing `Bᵀ` and counting pivots. (c) Exhibit an explicit invertible
`E` with `EB = rref(B)` up to row operations, and use it to show the column space
is unchanged. (d) Give a basis of `ker(Bᵀ)` and check that it spans the orthogonal
complement of `col(B)`.

<details>
<summary>Solution</summary>

**(a)** `B` is `4 × 3`, so `rank(B) ≤ 3`.

    R_1 <- R_1 - 2 R_0 :  (2,4,1) - 2(1,2,0) = (0, 0, 1)
    R_2 <- R_2 - 3 R_0 :  (3,6,2) - 3(1,2,0) = (0, 0, 2)
    R_3                  (0, 0, 3)                  (already 0)

    | 1  2  0 |
    | 0  0  1 |
    | 0  0  2 |
    | 0  0  3 |

    R_2 <- R_2 - 2 R_1 :  (0,0,2) - 2(0,0,1) = (0,0,0)
    R_3 <- R_3 - 3 R_1 :  (0,0,3) - 3(0,0,1) = (0,0,0)

    | 1  2  0 |
    | 0  0  1 |
    | 0  0  0 |
    | 0  0  0 |

**Two pivots. `row rank(B) = 2`.**

**(b)** `Bᵀ` is `3 × 4`:

    | 1  2  3  0 |
    | 2  4  6  0 |
    | 0  1  2  3 |

    R_1 <- R_1 - 2 R_0 :  (2,4,6,0) - 2(1,2,3,0) = (0, 0, 0, 0)

    | 1  2  3  0 |
    | 0  0  0  0 |
    | 0  1  2  3 |

Swap rows 1 and 2, then clear the first row:

    R_0 <- R_0 - 2 R_1 :  (1,2,3,0) - 2(0,1,2,3) = (1, 0, -1, -6)

    | 1  0  -1  -6 |
    | 0  1   2   3 |
    | 0  0   0   0 |

**Two pivots. `col rank(B) = 2`.** Equal to the row rank — but we have not yet
*proved* it must be; we have computed both.

**(c)** The row operations were: subtract `2×R₀` from `R₁`, subtract `3×R₀` from
`R₂`, then subtract `2×R₁` and `3×R₁` from the (already-reduced) rows 2 and 3.
Composed into one left-multiplication, that is an invertible `4 × 4` matrix `E`:

    E = | 1   0    0   0 |
        | -2  1    0   0 |
        | -9  3    1   0 |      (row 2 = -3 R_0 + 3 R_1 + R_2, all in original
        | 0   0    1   0 |       coordinates, since rows 0 and 1 were not
        | ...            |       themselves changed by the row-2 and row-3 steps)

Rather than assemble `E` exactly, the point is structural and does not need the
entries. Suppose `EB = F` with `E` invertible. Then for any `x`,

    F x = 0   <=>   E B x = 0   <=>   B x = 0        (multiply by E^{-1})

So `ker(EB) = ker(B)`, and the kernel determines the column space: `col(M) = {Mx}`
has exactly as many dimensions as `ker(M)` has codimensions, namely `n − dim ker M`.
Hence `col(EB) = col(B)` and

    rank(EB) = rank(B) = 2

Since `EB` is the RREF, whose column rank is visibly 2 (two nonzero rows, two
independent nonzero columns), the RREF's column rank equals `B`'s. That is
row rank = column rank for this matrix, proved rather than tabulated.

The general proof is the same argument with `B` arbitrary: row operations are
invertible, so they preserve `ker`, hence preserve `col`, hence the RREF's
column rank is `B`'s column rank; and the RREF's pivot count is simultaneously
its row rank. Two quantities, one integer.

**(d)** `dim ker(Bᵀ) = m − rank(B) = 4 − 2 = 2`. Solve `Bᵀy = 0`, i.e. dot `y`
with each column of `B`. The columns are `(1,2,3,0)`, `(2,4,6,0)`, `(0,1,2,3)`.
The first two give the same equation. So:

    y₀ + 2y₁ + 3y₂ = 0        ... (i)
    y₁ + 2y₂ + 3y₃ = 0        ... (ii)

From (i): `y₀ = −2y₁ − 3y₂`. From (ii): `y₁ = −2y₂ − 3y₃`. Then
`y₀ = −2(−2y₂ − 3y₃) − 3y₂ = 4y₂ + 6y₃ − 3y₂ = y₂ + 6y₃`. With `y₂` and `y₃`
free, take `y₂ = 1, y₃ = 0`: `y = (1, −2, 1, 0)`. And `y₂ = 0, y₃ = 1`:
`y₁ = −3`, `y₀ = 6`, giving `y = (6, −3, 0, 1)`.

    ker(B^T) = span{ (1, -2, 1, 0),  (6, -3, 0, 1) }

Verify:
- `(1,−2,1,0)` · `(1,2,3,0) = 1 − 4 + 3 = 0` ✓
- `(1,−2,1,0)` · `(2,4,6,0) = 2 − 8 + 6 = 0` ✓
- `(1,−2,1,0)` · `(0,1,2,3) = 0 − 2 + 2 = 0` ✓
- `(6,−3,0,1)` · `(1,2,3,0) = 6 − 6 + 0 = 0` ✓
- `(6,−3,0,1)` · `(2,4,6,0) = 12 − 12 = 0` ✓
- `(6,−3,0,1)` · `(0,1,2,3) = 0 − 3 + 0 + 3 = 0` ✓

And a basis of `col(B)` is the pivot columns of `B`, namely `col0 = (1,2,3,0)`
and `col2 = (0,1,2,3)`. Dot each null vector with each of those — that is exactly
the table above, and every entry is 0. So `ker(Bᵀ) ⊥ col(B)` ✓

Dimensions: `2 + 2 = 4 = m` ✓, so they are complementary and together fill `ℝ⁴`.

</details>

**[ ] Exercise 6 — rank is one bit; condition number is the rest.** Let

    X = | 1  0  0.5 |
        | 0  1  0.5 |
        | 0  0  1e-15 |

(a) Compute `rank(X)` in exact arithmetic. (b) Compute what
`numpy.linalg.matrix_rank` returns with the default tolerance, and with
`tol = 1e-20`. (c) Explain what the difference between (a) and (b) means for a
least-squares fit, referring to [lesson 38](38_orthogonality_and_least_squares.md).

<details>
<summary>Solution</summary>

**(a)** Column 2 is `(0.5, 0.5, 1e-15)`, and columns 0 and 1 are
`(1,0,0)` and `(0,1,0)`. The third column is not a multiple of either, so all
three are independent:

**`rank(X) = 3` in exact arithmetic.** The RREF is `[[1, 0, 0.5], [0, 1, 0.5],
[0, 0, 1e-15]]` — already in echelon form, with `1e-15` nonzero — so
`rank = 3`. It is a `3 × 3` matrix with `det = 1·1·1e-15 = 1e-15 ≠ 0`, so by
[lesson 33](33_determinant_and_inverse.md) it is invertible.

**(b)** With the default tolerance,
`tol = max(m,n)·ε·σ_max ≈ 3 · 2.2e-16 · σ_max`. The largest singular value is
about `1.2`, so `tol ≈ 8e-16`, and the smallest singular value is `1e-15` —
**above** the tolerance, just barely. So `matrix_rank` returns `3` here.

With `tol = 1e-20`, it also returns `3`. To see the failure, shrink the third
entry:

    X_k = [[1, 0, 0.5],
           [0, 1, 0.5],
           [0, 0, 1e-18]]

`tol_default ≈ 8e-16 > 1e-18`, so `matrix_rank(X_k)` returns **2** — a matrix
with `det = 1e-18 ≠ 0`, which is invertible in exact arithmetic, is reported as
singular.

The rule: any singular value below `max(m,n)·ε·σ_max` is called zero, and it is
not "exactly zero", it is "small enough that inverting along it would produce
garbage."

**(c)** For a least-squares fit with design matrix `X`, the normal equations are
`XᵀX w = Xᵀy`. For a square invertible `X` that system is solvable, but the
solution `w = (XᵀX)⁻¹ Xᵀy = X⁻¹y` is only numerically meaningful if `X⁻¹` can be
formed accurately — and the condition number of `X` is what says that.

`cond(X) = ‖X‖·‖X⁻¹‖`. For `X` above, `X⁻¹` exists with a `1/1e-15` entry, so
`‖X⁻¹‖ ≥ 1e15` and `cond(X) ≥ 1e15`. Since float64 carries about 16 decimal
digits, **zero digits survive**. `np.linalg.solve(X, y)` returns a vector with
no significant correct entries.

The practical consequences, and the reason the tolerance is not optional:

- `numpy.linalg.lstsq` uses an SVD, which does not form `X⁻¹` and therefore does
  not blow up the same way. It will return the least-squares fit for the truncated
  problem — dropping the third direction — which is the numerically honest
  answer, not the mathematically exact one.
- With `X_k` (third entry `1e-18`), `lstsq` will simply return the two-column fit,
  silently discarding a direction the data technically contains.
- If you genuinely need that direction, you must rescale. Dividing column 2 by
  `1e-18` makes the condition number `O(1)`, and the fit becomes computable.
  This is exactly why every serious regression pipeline standardises its features
  before fitting, and why `sklearn.preprocessing.StandardScaler` exists.

**The general point.** `rank` and `cond` answer different questions. Rank asks:
*is this direction there at all?* Condition number asks: *if it is there, can I
use it?* A matrix of rank 47 out of 50 can be perfectly healthy
(`cond ≈ 10`) or completely unusable (`cond ≈ 10¹⁷`), and the rank cannot tell
you which. Confusing the two is how a model ships with silently unstable
coefficients — and it is why the honest diagnostic is `np.linalg.cond`, not
`np.linalg.matrix_rank`.

</details>

## Summary

- `span(S)` is everything buildable from `S`; a **basis** spans the space *and* has
  no redundancy; `dim(V)` is the size of any basis, so it does not depend on which
  basis you pick.
- A set of `k` vectors is independent exactly when its span has dimension `k`.
  Independence is tested by row reduction: `k` vectors are independent iff `A`
  (columns = vectors) has `k` pivots.
- **`rank(A) = dim col(A) = dim row(A)`**, computed by counting pivots, nonzero
  diagonal entries of `U`, or singular values above a tolerance. `rank(A) ≤
  min(m, n)` is a ceiling, never an answer.
- **Row rank = column rank** is a theorem, not a coincidence: row operations are
  invertible and so preserve both spaces, making the pivot count simultaneously the
  number of independent rows and of independent columns.
- The **Four Fundamental Subspaces**: `col(A)` and `ker(Aᵀ)` split `ℝᵐ` into `r` and
  `m − r`; `row(A)` and `ker(A)` split `ℝⁿ` into `r` and `n − r`, orthogonally in
  both cases.
- `nullity(A) = n − rank(A)`, and **rank + nullity = n** — the number of determined
  variables plus the free ones equals the number of unknowns.
- `rank(A) = n` ⟺ `ker(A) = {0}` ⟺ `det(A) ≠ 0` ⟺ invertible, for square `A`; and
  `rank(A) = m` ⟺ `Ax = b` solvable for every `b`.
- Rank is *how many* degrees of freedom were lost; the condition number is
  *how badly*, and only the second one tells you whether a solve will be stable.

## Next

[35 — Linear Transformations and Kernels](35_linear_transformations_and_kernels.md)
stops talking about the matrix and starts talking about the *map*. Rank-nullity
becomes the statement that every linear transformation `V → W` has a kernel and an
image, that injectivity and surjectivity are equivalent to vanishing nullity and
full column rank respectively, and that the quotient space `V / ker T` is
canonically isomorphic to `im T` — which is why a rank-`r` matrix has no
information beyond an `r`-dimensional map.
