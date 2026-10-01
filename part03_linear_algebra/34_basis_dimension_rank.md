# 34 — Basis, Dimension, and Rank

**Part**: part03_linear_algebra · **Prerequisites**: 33 · **Time**: 40 min

---

## In Plain Words

Lesson 30 introduced the span: the set of everything you can build by scaling
and adding a given list of vectors. The span is a set, and sets are awkward to
store — you cannot write them down. A *basis* is the shortest list that generates
the same set, and the *dimension* is how long that list is. Two things can have
the same span and different bases; that is normal and expected, and the span is
the thing that matters.

*Rank* is that dimension, applied to a matrix. It answers: how many independent
directions are in here? A dataset with a hundred columns and rank 3 has three
independent factors, not a hundred, and everything downstream — feature
selection, PCA, the cost of a solver — is driven by that number.

The theorem that makes rank usable is this: the number of independent rows always
equals the number of independent columns. Row spaces and column spaces are
different sets living in different ambient spaces, and the fact that they always
have the same dimension is what lets one algorithm — row reduction — answer
questions about both.

## Why Computer Science Cares

- **Feature selection.** A column of your dataset that is a linear combination of
  the others carries no new information. Rank finds these columns, and dropping
  them is free. Keeping them costs storage, slows every solver, and makes
  regularisation arbitrary.
- **PCA** ([lesson 40](40_svd_and_pca.md)) keeps exactly `rank` components. If
  rank is 3 out of 50 columns, PCA compresses 50 to 3 with no information loss.
- **Image compression.** An `n × n` image with rank `r` is exactly representable
  by `r` singular values. A rank-20 photograph of a 1000×1000 image needs 20,000
  numbers instead of a million.
- **Degrees of freedom.** An `m × n` system of rank `r` has `n − r` free unknowns.
  That count is how many parameters your data cannot pin down, and it is why a
  linear model with more coefficients than independent features is
  under-determined.
- **Condition numbers.** The rank reveals near-dependence. A rank drop under a
  small perturbation means the matrix is nearly singular, which is the signal
  that a solver's answer will be garbage.
- **Interview questions.** "What is the rank of this matrix?", "why does removing
  a redundant column not change the model?", and "what does it mean that a
  least-squares fit is under-determined?" are all rank questions.

## The Formal Version

Symbols follow [SYMBOLS.md](../../SYMBOLS.md).

**Definition.** A list of vectors `B = (v₁, …, v_k)` is a **basis** for a set of
vectors `S` if `span(B) = S` and `B` is linearly independent.

**Explanation.** Two requirements: it reaches everything, and nothing in it is
redundant. Drop any one vector from a basis and the span shrinks; add a redundant
vector and the span does not grow.

**Definition.** The **dimension** of `S` is the number of vectors in any basis of
`S`, written `dim(S)`.

**Theorem.** Every basis of a set has the same number of vectors.

**Explanation.** Suppose `B₁` has `k` vectors and `B₂` has `m > k`. Since
`span(B₁) = span(B₂)`, every `v ∈ B₂` is a combination of `B₁`, so `B₂` is
dependent. But `B₂` is a basis, hence independent — a contradiction.

**Definition.** For an `m × n` matrix `A`:

- the **row space** is the span of the rows, a subspace of `ℝⁿ`;
- the **column space** is the span of the columns, a subspace of `ℝ^m`;
- the **null space** is `{x ∈ ℝⁿ : A x = 0}`, also a subspace of `ℝⁿ`;
- the **left null space** is `{y ∈ ℝ^m : Aᵀ y = 0}`, a subspace of `ℝ^m`.

**Definition.** The **rank** of `A` is `dim(row space) = dim(column space)`,
where the equality is the theorem below. The **nullity** is
`dim(null space)`, and the **left nullity** is `dim(left null space)`.

**Theorem (Row rank = column rank).** For every matrix `A`,
`dim(row space of A) = dim(column space of A)`, and both equal the number of
pivots in any row echelon form of `A`.

**Explanation.** Row reduction preserves the row space, so the nonzero rows of the
RREF form a basis for it — call the count `r`. For the column space: the pivot
columns of the *original* `A` are linearly independent (each has a leading 1 in
a row where no other pivot column has one), and every other column of `A` is a
linear combination of them (non-pivot columns correspond to free variables). So
there are exactly `r` pivot columns and they form a basis. Both counts are the
pivot count. Note the subtlety: the basis for the row space comes from the
*reduced* matrix, and the basis for the column space comes from the *original*
matrix. Mixing those up is the standard error.

**Theorem (Rank-nullity).** For every `n × n` matrix `A`, `rank(A) + nullity(A) = n`.
More generally, for an `m × n` matrix, `rank(A) + nullity(A) = n`, and
`rank(A) + left nullity(A) = m`.

**Explanation.** In the RREF, each pivot variable is determined by the free
variables, so a solution of `A x = b` is `x = x_p + Σ c_j v_j` with one free
parameter per non-pivot column. The count of non-pivot columns is `n − r`. The
left version is the same statement applied to `Aᵀ`, whose number of columns is
`m`.

**Theorem (Four fundamental subspaces).** For an `m × n` matrix `A` of rank `r`:

| Space | Ambient | Dimension | Where the basis comes from |
| --- | --- | --- | --- |
| column space `im(A)` | `ℝ^m` | `r` | pivot columns of `A` |
| row space `im(Aᵀ)` | `ℝ^n` | `r` | nonzero rows of `rref(A)` |
| null space `ker(A)` | `ℝ^n` | `n − r` | free columns of `rref(A)` |
| left null space `ker(Aᵀ)` | `ℝ^m` | `m − r` | free columns of `rref(Aᵀ)` |

**Explanation.** The total is `r + r + (n − r) + (m − r)`, and every basis is
found by one row reduction. This table is the organisation of the whole subject:
given a matrix, four spaces, two numbers (`r` and the shape), one algorithm.

**Theorem (Rank and linear systems).** For `A x = b` with `A` of rank `r` and
`n` columns:

- the system is consistent iff `b` is in the column space of `A`;
- when consistent, the solution set is `x_p + ker(A)`, an affine subspace of
  dimension `n − r`;
- so a unique solution requires `r = n`, which for a square matrix is exactly
  `det(A) ≠ 0`.

**Explanation.** The homogeneous system has solutions `ker(A)`, and if `x_p` is
one particular solution of the inhomogeneous system then `x_p + v` solves it for
every `v ∈ ker(A)`.

**Theorem (Basis exchange).** If `B` is a basis for `V` and `v ∉ V`, then
`B ∪ {v}` has a dependent subset containing `v` and exactly one vector of `B`.
Replacing that vector gives another basis of a space strictly containing `V`.

**Explanation.** Express `v` in terms of `B`: `v = Σ c_j b_j`. Some `c_j ≠ 0`, so
`b_j = (v − Σ_{i≠j} c_i b_i) / c_j` lies in the span of `B ∪ {v}`, and swapping it
for `v` preserves the span while adding one dimension. This is the mechanism
behind every greedy basis algorithm.

## Worked Example

A small dataset. Three students, three features: hours studied, hours slept,
exam score.

    A = | 3  7  71 |
        | 5  6  79 |
        | 4  8  75 |

**Step 1: row reduce.** Pivot on row 0, column 0, value 3. Eliminate:

    R1 ← R1 − (5/3)R0:   5 − 5 = 0,  6 − 35/3 = −17/3,  79 − 355/3 = −118/3
    R2 ← R2 − (4/3)R0:   4 − 4 = 0,  8 − 28/3 = −4/3,  75 − 284/3 = −59/3

    | 3    7       71 |
    | 0  −17/3  −118/3 |
    | 0   −4/3    −59/3 |

Scale R1 and R2 to make the pivots 1:

    | 3    7    71 |
    | 0    1    118/17 |
    | 0    1     59/4 |

Eliminate column 1 from R2. Multiplier is `1`, so `R2 ← R2 − R1`:

    1 − 1 = 0
    59/4 − 118/17 = (59·17 − 118·4) / 68 = (1003 − 472)/68 = 531/68

Eliminate column 1 from R0. Multiplier is 7, so `R0 ← R0 − 7R1`:

    3 − 7 = −4
    71 − 7(118/17) = (1207 − 826)/17 = 381/17

Scale R0 by `−1/4`:

    | 1   0    −381/68 |
    | 0   1     118/17 |
    | 0   0      531/68 |

**Step 2: count the pivots.** Three pivots, in columns 0, 1, 2. So

    rank(A) = 3

**Step 3: read off all four spaces.**

*Column space*: pivot columns of the **original** `A` are columns 0, 1, 2 — all
three. A basis for the column space is the whole of `ℝ³`:

    col0 = (3, 5, 4),  col1 = (7, 6, 8),  col2 = (71, 79, 75)

Dimension 3.

*Row space*: the nonzero rows of the RREF, all three of them. Dimension 3.

*Null space*: `n − r = 3 − 3 = 0`. No free variables. There is no nonzero `x` with
`A x = 0`. Check the third row: `x₂ = 0`, then the first gives `x₀ = 0`, the second
gives `x₁ = 0`.

*Left null space*: `m − r = 3 − 3 = 0`. No relations among the rows.

**Step 4: what this means.** All three features are independent. No student
column is a combination of the others, so you cannot drop one without losing
information. A linear model on these three features has all three coefficients
determined by the data.

**Step 5: a case with rank 2.** Add a fourth feature: exam score plus 10, which
is a copy of the third.

    A' = | 3  7  71  81 |
         | 5  6  79  89 |
         | 4  8  75  85 |

Column 3 is column 2 plus the all-ones column, so it is certainly a combination,
and `rank(A') ≤ 3`. Row reduction confirms `rank(A') = 3`, so the new column
carries no new *direction* — it is new information about position but not a new
factor. The null space now has dimension `4 − 3 = 1`. Find it: since
`col3 − col2 = (10, 10, 10)`, the vector `(0, 0, 1, −1)` satisfies `A' x = 0`:

    Row 0:  0 + 0 + 71 − 81 = −10

That is not zero. Recheck: `A' x` with `x = (0, 0, 1, −1)` is
`(71 − 81, 79 − 89, 75 − 85) = (−10, −10, −10)`, not zero. So `(0, 0, 1, −1)` is
**not** in the null space — I need the *same* coefficients in every row for the
relation to vanish, and a difference of constants does not do that.

The right relation comes from the fact that col3 = col2 + `10·(1,1,1)`. So
`A' x = 0` requires

    3x₀ + 7x₁ + 71x₂ + 81x₃ = 0
    5x₀ + 6x₁ + 79x₂ + 89x₃ = 0
    4x₀ + 8x₁ + 75x₂ + 85x₃ = 0

Subtracting the first equation from the second:

    2x₀ − x₁ + 8x₂ + 8x₃ = 0

and the third minus the first:

    x₀ + x₁ + 4x₂ + 4x₃ = 0

Adding these: `3x₀ + 12x₂ + 12x₃ = 0`, so `x₀ = −4x₂ − 4x₃`. Then from the third
equation above, `x₁ = −x₀ − 4x₂ − 4x₃ = 0`. Substitute into the first:

    3(−4x₂ − 4x₃) + 71x₂ + 81x₃ = −12x₂ − 12x₃ + 71x₂ + 81x₃ = 59x₂ + 69x₃ = 0

So `x₂ = −69/59 · x₃`, one free variable, dimension 1 as predicted. With
`x₃ = 59`:

    x = ( −4(−69) − 4(59),  0,  −69,  59 ) = ( 276 − 236,  0,  −69,  59 )
       = ( 40,  0,  −69,  59 )

Check: `3(40) + 7(0) + 71(−69) + 81(59) = 120 + 0 − 4899 + 4779 = 0` ✓
And `5(40) + 79(−69) + 89(59) = 200 − 5451 + 5251 = 0` ✓
And `4(40) + 8(0) + 75(−69) + 85(59) = 160 − 5175 + 5015 = 0` ✓

The null space has dimension 1, and rank-nullity says `3 + 1 = 4`, the column
count. The lesson: a new column that is *nearly* a copy of an old one still
raises nothing, but you must row reduce to find out, and you must do it exactly —
the "obvious" relation `(0,0,1,−1)` was wrong, and only checking caught it.

## Runnable Code

### Rank, bases, and the null space

Row reduction gives every answer in this lesson. One implementation, four
outputs.

```python
TOL = 1e-9


# ---------------------------------------------------------------- helpers
def shape(M):
    return len(M), len(M[0])


def zeros(rows, cols):
    return [[0.0] * cols for _ in range(rows)]


def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def transpose(M):
    rows, cols = shape(M)
    return [[M[i][j] for i in range(rows)] for j in range(cols)]


def rref(A, tol=TOL):
    """Reduced row echelon form of A, plus the pivot column indices."""
    M = [list(row) for row in A]
    rows, cols = len(M), len(M[0])
    pivot_row = 0
    pivots = []
    for col in range(cols):
        best = None
        for r in range(pivot_row, rows):
            if abs(M[r][col]) > tol:
                best = r
                break
        if best is None:
            continue
        M[pivot_row], M[best] = M[best], M[pivot_row]
        p = M[pivot_row][col]
        M[pivot_row] = [v / p for v in M[pivot_row]]
        for r in range(rows):
            if r != pivot_row and M[r][col] != 0.0:
                f = M[r][col]
                M[r] = [M[r][c] - f * M[pivot_row][c] for c in range(cols)]
        pivots.append(col)
        pivot_row += 1
    # Adding 0.0 turns -0.0 into 0.0 so the printed matrix has no signed zeros.
    M = [[v + 0.0 for v in row] for row in M]
    return M, pivots


def rank(A, tol=TOL):
    """The rank is the number of pivots in row echelon form."""
    _, pivots = rref(A, tol)
    return len(pivots)


def row_space_basis(A, tol=TOL):
    """The nonzero rows of the RREF form a basis for the row space."""
    M, _ = rref(A, tol)
    return [list(row) for row in M if any(abs(v) > tol for v in row)]


def column_space_basis(A, tol=TOL):
    """The original columns of A that had pivots form a basis for the column space."""
    _, pivots = rref(A, tol)
    return [[A[i][c] for i in range(len(A))] for c in pivots]


def null_space(A, tol=TOL):
    """Basis of {x : A x = 0}. Free variables get 1 in turn."""
    M, pivots = rref(A, tol)
    cols = shape(A)[1]
    free = [c for c in range(cols) if c not in pivots]
    basis = []
    for fc in free:
        v = [0.0] * cols
        v[fc] = 1.0
        for i, pc in enumerate(pivots):
            v[pc] = -M[i][fc]
        basis.append(v)
    return basis


def matvec(M, v):
    rows, cols = shape(M)
    return [sum(M[i][k] * v[k] for k in range(cols)) for i in range(rows)]


def print_matrix(label, M, width=8):
    rows, cols = shape(M)
    print(f"{label}  ({rows}x{cols})")
    for row in M:
        print("  | " + " ".join(f"{x:{width}.3f}" for x in row) + " |")


def print_vectors(label, vs):
    print(label)
    for v in vs:
        print(f"  {v}")


# ---------------------------------------------------------------- span vs basis
print("=== Span is a set; a basis is a list ===")
v1 = [1.0, 2.0, 3.0]
v2 = [0.0, 1.0, 1.0]
v3 = [1.0, 3.0, 4.0]      # = v1 + v2, so redundant
print(f"generators: {[v1, v2, v3]}")
print("span(v1, v2, v3) = span(v1, v2): the third adds nothing")
print(f"  v3 - (v1 + v2) = {[v3[i] - v1[i] - v2[i] for i in range(3)]}")
print()
A = [[v1[0], v2[0], v3[0]],
     [v1[1], v2[1], v3[1]],
     [v1[2], v2[2], v3[2]]]
print("the same three vectors as the COLUMNS of A:")
print_matrix("A", A)
print(f"rank(A) = {rank(A)}")
print("Three generators, two independent directions. The span is the same set")
print("either way; the basis is the shortest list that generates it.")

# ---------------------------------------------------------------- RREF
print()
print("=== Row reduction, and what the pivots mean ===")
print_matrix("A", A)
M, pivots = rref(A)
print_matrix("rref(A)", M)
print(f"pivot columns: {pivots}")
print(f"rank = {len(pivots)}")
print("The nonzero rows of the RREF are a basis for the ROW space. They are not")
print("the original rows, but they span the same set.")

print()
print("=== Row space versus column space: the theorem ===")
rb = row_space_basis(A)
cb = column_space_basis(A)
print_vectors("row space basis (nonzero RREF rows):", rb)
print_vectors("column space basis (pivot columns of A):", cb)
print(f"row rank   = {len(rb)}")
print(f"column rank = {len(cb)}")
print(f"they agree: {len(rb) == len(cb)}")
print("Row rank = column rank is THE theorem of this lesson. They look like")
print("completely different objects: the row space lives in a different space")
print("from the column space whenever A is not square. That they always have")
print("the same dimension is the surprising, useful, slightly mystical part.")

# Show that the row space really is spanned by the original rows.
print()
print("=== Check that the RREF rows span the original rows ===")


def express(target, gens):
    """Return coefficients c with target = sum(c_j * gens[j]), or None."""
    # Build the matrix whose columns are the generators, solve for c.
    G = [[gens[j][i] for j in range(len(gens))] for i in range(len(target))]
    rows, cols = len(G), len(G[0])
    Mx = [list(G[i]) + [target[i]] for i in range(rows)]
    pivot_cols = []
    r = 0
    for c in range(cols):
        best = None
        for i in range(r, rows):
            if abs(Mx[i][c]) > TOL:
                best = i
                break
        if best is None:
            continue
        Mx[r], Mx[best] = Mx[best], Mx[r]
        for i in range(rows):
            if i != r:
                f = Mx[i][c] / Mx[r][c]
                for j in range(c, cols + 1):
                    Mx[i][j] -= f * Mx[r][j]
        pivot_cols.append(c)
        r += 1
    for i in range(len(pivot_cols), rows):
        if abs(Mx[i][cols]) > TOL:
            return None
    x = [0.0] * cols
    for i, c in enumerate(pivot_cols):
        x[c] = Mx[i][cols] / Mx[i][c]
    return x


print("each original row as a combination of the RREF rows:")
for i, row in enumerate(A):
    coeffs = express(row, rb)
    print(f"  row {i} {row} = {coeffs} * rref_rows")
print("each RREF row as a combination of the original rows:")
for i, row in enumerate(rb):
    coeffs = express(row, A)
    print(f"  rref row {i} {row} = {coeffs} * A_rows")
print("Two sets spanning each other are the same set. That is what 'row reduction")
print("preserves the row space' means.")

# ---------------------------------------------------------------- null space
print()
print("=== The null space: directions that vanish ===")
print("The null space is the set of x with A x = 0. It is the space of")
print("'invisible directions': the components of a vector that this matrix")
print("throws away.")
ns = null_space(A)
print_vectors(f"null space basis (dim {len(ns)}):", ns)
for v in ns:
    print(f"  A v = {matvec(A, v)}")
print(f"dim(null space) = {len(ns)} = columns - rank = {shape(A)[1]} - {rank(A)}")

print()
print("=== rank + nullity = number of columns ===")
A2 = [[1.0, 2.0, 3.0],      # row 2 = 2 * row 0, row 3 = row 0 + row 1
      [4.0, 5.0, 6.0],
      [2.0, 4.0, 6.0],
      [5.0, 7.0, 9.0]]
print_matrix("A2 (4x3, row 2 = 2*row 0, row 3 = row 0 + row 1)", A2)
r2 = rank(A2)
n2 = len(null_space(A2))
print(f"columns = {shape(A2)[1]}, rank = {r2}, nullity = {n2}")
print(f"rank + nullity = {r2} + {n2} = {r2 + n2}, which equals the column count")
print(f"The null space is generated by "
      f"{[[round(x, 4) for x in v] for v in null_space(A2)]}")
print("Every column of A2 is a data point, and the null space says there is")
print(f"{n2} direction the data cannot distinguish. This is rank-nullity, and")
print("it is the counting principle behind PCA and behind 'how many degrees of")
print("freedom does this system have'.")

print()
print("=== Rank is the same whether you reduce rows or columns ===")
# Reduce the transpose and count pivots: this is the column rank, computed by
# the same algorithm but on A^T. The theorem says the counts match.


def rank_of_transpose(A, tol=TOL):
    return rank(transpose(A), tol)


for label, M in [("A  (3x3)", A), ("A2 (4x3)", A2)]:
    rr = rank(M)
    cr = rank_of_transpose(M)
    print(f"  {label:12s} row rank = {rr}, column rank = {cr}, equal: {rr == cr}")
print("Computing the two ranks by two different routes always gives the same")
print("number. That is the theorem, and it is why 'the rank of a matrix' needs")
print("no qualifier: there is only one rank.")

print()
print("=== Rank as degrees of freedom in a system ===")
print("For A2 x = b, the number of free unknowns is n - r = "
      f"{shape(A2)[1]} - {rank(A2)} = {shape(A2)[1] - rank(A2)}")
print("For a full-rank square system, r = n, so there are 0 free unknowns and")
print("the solution, if it exists, is unique. That is lesson 32's uniqueness")
print("theorem, now expressed as a rank statement.")

print()
print("=== Dimension of the span equals the number of independent vectors ===")
test_cases = {
    "3 independent vectors in R^3": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
    "2 independent + 1 redundant": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]],
    "3 vectors all in a plane": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]],
    "4 vectors in R^3": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 1.0, 1.0]],
}
for label, vecs in test_cases.items():
    Mx = [[v[i] for v in vecs] for i in range(len(vecs[0]))]
    r = rank(Mx)
    basis = column_space_basis(Mx)
    print(f"  {label:32s} {len(vecs)} vectors -> rank {r}")
    print(f"  {'':32s} a basis has {len(basis)} vectors, so dim(span) = {len(basis)}")
print("The dimension of the span is the number of vectors in ANY basis of it,")
print("and it is always at most the ambient dimension. Four vectors in three")
print("dimensions can never give rank 4.")
```

### The fundamental theorem, the four spaces, and basis exchange

```python
TOL = 1e-9


# ---------------------------------------------------------------- helpers
def shape(M):
    return len(M), len(M[0])


def zeros(rows, cols):
    return [[0.0] * cols for _ in range(rows)]


def transpose(M):
    rows, cols = shape(M)
    return [[M[i][j] for i in range(rows)] for j in range(cols)]


def rref(A, tol=TOL):
    M = [list(row) for row in A]
    rows, cols = len(M), len(M[0])
    pivot_row = 0
    pivots = []
    for col in range(cols):
        best = None
        for r in range(pivot_row, rows):
            if abs(M[r][col]) > tol:
                best = r
                break
        if best is None:
            continue
        M[pivot_row], M[best] = M[best], M[pivot_row]
        p = M[pivot_row][col]
        M[pivot_row] = [v / p for v in M[pivot_row]]
        for r in range(rows):
            if r != pivot_row and M[r][col] != 0.0:
                f = M[r][col]
                M[r] = [M[r][c] - f * M[pivot_row][c] for c in range(cols)]
        pivots.append(col)
        pivot_row += 1
    M = [[v + 0.0 for v in row] for row in M]
    return M, pivots


def rank(A, tol=TOL):
    _, pivots = rref(A, tol)
    return len(pivots)


def row_space_basis(A, tol=TOL):
    M, _ = rref(A, tol)
    return [list(row) for row in M if any(abs(v) > tol for v in row)]


def column_space_basis(A, tol=TOL):
    _, pivots = rref(A, tol)
    return [[A[i][c] for i in range(len(A))] for c in pivots]


def null_space(A, tol=TOL):
    M, pivots = rref(A, tol)
    cols = shape(A)[1]
    free = [c for c in range(cols) if c not in pivots]
    basis = []
    for fc in free:
        v = [0.0] * cols
        v[fc] = 1.0
        for i, pc in enumerate(pivots):
            v[pc] = -M[i][fc]
        basis.append(v)
    return basis


def left_null_space(A, tol=TOL):
    """{y : A^T y = 0}, i.e. the vectors orthogonal to the column space.

    The left null space of A is the null space of A^T, and its basis vectors
    are exactly the linear relations among the rows of A.
    """
    return null_space(transpose(A), tol)


def matvec(M, v):
    rows, cols = shape(M)
    return [sum(M[i][k] * v[k] for k in range(cols)) for i in range(rows)]


def matmul(A, B):
    rows_a, cols_a = shape(A)
    rows_b, cols_b = shape(B)
    if cols_a != rows_b:
        raise ValueError(f"cannot multiply {rows_a}x{cols_a} by {rows_b}x{cols_b}")
    C = zeros(rows_a, cols_b)
    for i in range(rows_a):
        for j in range(cols_b):
            C[i][j] = sum(A[i][k] * B[k][j] for k in range(cols_a))
    return C


def print_matrix(label, M, width=7):
    rows, cols = shape(M)
    print(f"{label}  ({rows}x{cols})")
    for row in M:
        print("  | " + " ".join(f"{x:{width}.3f}" for x in row) + " |")


def show_basis(label, vs):
    print(label)
    for v in vs:
        print(f"  {v}")


# ------------------------------------------------- the fundamental theorem
print("=== The fundamental theorem of linear algebra, in one example ===")
# A dataset: five students, three features (study hours, attendance, score).
# The score is built as 10*hours + 20*attendance, so it carries no new
# information: three columns, only two independent components.
data = [[3.0, 0.90, 48.0],
        [5.0, 0.80, 66.0],
        [2.0, 0.60, 32.0],
        [4.0, 0.95, 59.0],
        [6.0, 0.85, 77.0]]
print_matrix("data (5 students x 3 features)", data)
for row in data:
    print(f"    check: 10*{row[0]} + 20*{row[1]} = {10 * row[0] + 20 * row[1]:6.2f}"
          f"   vs score {row[2]:6.2f}")
r = rank(data)
print(f"rank = {r}, so three feature columns carry only {r} independent components")
print()
show_basis("column space basis (pivot columns of data):", column_space_basis(data))
show_basis("row space basis (nonzero RREF rows):", row_space_basis(data))
print(f"row rank {len(row_space_basis(data))} == column rank "
      f"{len(column_space_basis(data))}")
print()
show_basis("null space basis (ker(data)):", null_space(data))
show_basis("left null space basis (ker(data^T), dim = rows - r):",
           left_null_space(data))
print()
print("Every basis above has exactly r vectors, except the null space, which has")
print(f"cols - r = 3 - {r} = {3 - r}, and the left null space, which has")
print(f"rows - r = {len(data)} - {r} = {len(data) - r}. That is rank-nullity, and")
print("the four spaces are the whole of linear algebra for a rectangular matrix.")
print()
print("Reading it for machine learning: r = 2 here, so the score column is a")
print("combination of the other two and carries no new information. PCA would")
print(f"keep {r} components instead of 3 with no loss at all, and a linear model")
print("fitted on all three columns has one coefficient that is not identified.")
print("The null space vector [-10, -20, 1] says exactly that: moving 10 hours and")
print("20 attendance units in opposite directions changes nothing in the output.")

# ------------------------------------------------- left null space = relations
print()
print("=== The left null space records relations among the rows ===")
A = [[1.0, 2.0, 3.0],
     [4.0, 5.0, 6.0],
     [7.0, 8.0, 10.0],
     [5.0, 7.0, 9.0]]      # row 3 = row 0 + row 1
print_matrix("A (4x3)", A)
print(f"rank = {rank(A)}")
lns = left_null_space(A)
show_basis("left null space of A (relations among the 4 rows):", lns)
print()
for y in lns:
    # Coefficients of exactly 0 are dropped from the printed relation: they are
    # part of the vector but carry no information.
    parts = " ".join(f"{y[i]:+.0f}*row{i}" for i in range(len(A)) if abs(y[i]) > 1e-12)
    terms = parts
    print(f"  relation: {terms} = 0")
    print(f"    check: A^T y = {[round(t, 9) for t in matvec(transpose(A), y)]}")
    total = [0.0] * 3
    for i, row in enumerate(A):
        for j in range(3):
            total[j] += y[i] * row[j]
    print(f"    weighted sum of rows = {total}")
print("A y-transpose = 0 means y1*row0 + y2*row1 + ... = 0, which is exactly a")
print("linear dependence written with the coefficients collected up front. The")
print("left null space is the complete list of such relations.")

# ------------------------------------------------- rank as degrees of freedom
print()
print("=== Degrees of freedom in a system, counted by rank ===")
# Four unknowns, three equations, one redundancy: 2 - ... let's build it.
# Three unknowns, four equations with one redundancy: rank 3, so unique.
def solve_consistent(A, b, tol=TOL):
    rows, cols = len(A), len(A[0])
    M = [list(A[i]) + [b[i]] for i in range(rows)]
    pivot_row = 0
    pivots = []
    for col in range(cols):
        best = None
        for r in range(pivot_row, rows):
            if abs(M[r][col]) > tol:
                best = r
                break
        if best is None:
            continue
        M[pivot_row], M[best] = M[best], M[pivot_row]
        p = M[pivot_row][col]
        M[pivot_row] = [v / p for v in M[pivot_row]]
        for r in range(rows):
            if r != pivot_row and M[r][col] != 0.0:
                f = M[r][col]
                M[r] = [M[r][c] - f * M[pivot_row][c] for c in range(cols + 1)]
        pivots.append(col)
        pivot_row += 1
    for i in range(pivot_row, rows):
        if any(abs(M[i][j]) > tol for j in range(cols)) or abs(M[i][cols]) > tol:
            return "no solution", M, pivots
    if len(pivots) < cols:
        return "infinitely many", M, pivots
    x = [0.0] * cols
    for i, pc in enumerate(pivots):
        x[pc] = M[i][cols]
    return "unique", M, pivots


print("An m-equation, n-unknown system of rank r:")
print("  consistent  -> n - r free unknowns, so n - r free parameters in x")
print("  inconsistent -> no solution at all, and rank does not tell you which")
print("  (you have to look at the augmented matrix, as in lesson 32)")
print()
A_sys = [[1.0, 2.0, 3.0],
         [4.0, 5.0, 6.0],
         [7.0, 8.0, 10.0],
         [5.0, 7.0, 9.0]]     # 4 equations, 3 unknowns, rank 3
b_sys = [10.0, 20.0, 31.0, 30.0]
kind, M, pivots = solve_consistent(A_sys, b_sys)
print(f"A_sys is {len(A_sys)}x{len(A_sys[0])}, rank {rank(A_sys)}, "
      f"b = {b_sys}")
print(f"  outcome: {kind}, {len(pivots)} pivots, "
      f"{len(A_sys[0]) - len(pivots)} free unknowns")
x = [M[i][len(A_sys[0])] for i in range(len(pivots))]
print(f"  x = {[round(v, 6) for v in x]}")
resid = [round(sum(A_sys[i][j] * x[j] for j in range(3)) - b_sys[i], 9)
         for i in range(len(A_sys))]
print(f"  residuals {resid}")
print("Four equations but only three unknowns, so one equation is redundant.")
print("It contributes nothing, which is why the system still has a unique")
print("solution: over-determined is fine, over-determined and inconsistent is not.")

# A rank-deficient consistent system: 2 equations, 3 unknowns, rank 2.
A_under = [[1.0, 2.0, 3.0], [2.0, 1.0, 0.0]]
b_under = [6.0, 2.0]
kind2, M2, pivots2 = solve_consistent(A_under, b_under)
print()
print(f"A_under is {len(A_under)}x{len(A_under[0])}, rank {rank(A_under)}, "
      f"b = {b_under}")
print(f"  outcome: {kind2}, {len(pivots2)} pivots, "
      f"{len(A_under[0]) - len(pivots2)} free unknowns")
show_basis("  solution family is x_p + t*v:", null_space(A_under))
print("  one free unknown means one free parameter, and the solution set is a")
print("  line. Two free unknowns would give a plane.")

# ------------------------------------------------- basis by exchange
print()
print("=== Getting a basis by removing redundant generators ===")
# Start with a set, drop anything that is a combination of what is left.
def greedy_basis(vectors, tol=TOL):
    """Keep a vector only if it increases the rank when added.

    The test builds the matrix whose columns are the kept vectors plus the
    candidate, and checks whether the rank goes up. That is the pivot column
    rule, applied one column at a time.
    """
    kept = []
    for v in vectors:
        n = len(v)
        # rows i = 0..len(kept): the kept columns, then the candidate column
        candidate = [[kept[j][i] for j in range(len(kept))] + [v[i]]
                     for i in range(n)]
        if rank(candidate, tol) > len(kept):
            kept = kept + [list(v)]
    return kept


col_vectors = [[data[i][j] for i in range(len(data))] for j in range(len(data[0]))]
show_basis("three columns of the dataset:", col_vectors)
basis = greedy_basis(col_vectors)
print()
show_basis("greedy basis in the original order:", basis)
print(f"kept {len(basis)} of {len(col_vectors)} columns; the span is unchanged.")

reordered = [col_vectors[2], col_vectors[0], col_vectors[1]]
print()
show_basis("same columns, score first:", reordered)
basis2 = greedy_basis(reordered)
show_basis("greedy basis in that order:", basis2)
print(f"kept {len(basis2)} columns: a different basis, same span.")
print()
print("Two different bases of the same space. That is the whole point: a basis")
print("is not unique, the span is. The greedy rule is the pivot column rule run")
print("one column at a time, and its answer depends on the order you try things")
print("in. This is exactly why greedy feature selection can pick a worse subset")
print("than the one PCA finds, and why picking features by correlation alone is")
print("a shortcut that ignores the linear structure.")
```

### With Libraries

```python
# A dataset: four observations, three features. One feature is engineered as a
# combination of the other two, so the matrix has rank 2 and not 3.

import numpy as np

data = np.array([
    [3.0, 0.90, 48.0],
    [5.0, 0.80, 66.0],
    [2.0, 0.60, 32.0],
    [4.0, 0.95, 59.0],
])

print("=== data ===")
print(data)
print(f"shape {data.shape}")

print()
print("=== rank: one call ===")
print(f"np.linalg.matrix_rank(data)     = {np.linalg.matrix_rank(data)}")
print(f"np.linalg.matrix_rank(data.T)   = {np.linalg.matrix_rank(data.T)}")
print("The transpose gives the same number. That is row rank = column rank, and")
print("the library does not care which you meant.")

print()
print("=== singular values: the graded version of rank ===")
sv = np.linalg.svd(data, compute_uv=False)
print(f"singular values = {sv}")
print(f"there are {len(sv)} of them, but only "
      f"{np.sum(sv > 1e-10 * sv[0])} are nonzero to working precision")
print("Rank is a thresholded question: how many are 'big enough'. Singular values")
print("are the unthresholded answer, and the ratio between the smallest and")
print("largest tells you how ill-conditioned the problem is.")
print(f"cond = {np.linalg.cond(data):.4e}  (largest / smallest nonzero)")

print()
print("=== The four fundamental subspaces, from numpy ===")
u, s, vt = np.linalg.svd(data, full_matrices=True)
r = int(np.sum(s > 1e-10 * s[0]))
print(f"rank r = {r}, data is {data.shape[0]}x{data.shape[1]}")
print()
print(f"column space = span of the first r columns of U  (in R^{data.shape[0]})")
print(np.round(u[:, :r], 6))
print()
print(f"null space of data = span of the last {data.shape[1] - r} rows of V^T")
print(np.round(vt[r:, :], 6))
print()
print(f"row space = span of the first r rows of V^T      (in R^{data.shape[1]})")
print(np.round(vt[:r, :], 6))
print()
print(f"left null space = span of the last {data.shape[0] - r} columns of U")
print(np.round(u[:, r:], 6))
print()
print("Four spaces, four dimensions: r + (cols - r) + r + (rows - r). Each basis")
print("has the length rank-nullity predicts. SVD just hands you all of them,")
print("which is why lesson 40 builds PCA out of it.")

print()
print("=== Verifying the null space vector by hand ===")
# The score column is 10*hours + 20*attendance, so [10, 20, -1] is the relation
# between the COLUMNS: 10*col0 + 20*col1 - col2 = 0.
relation = np.array([10.0, 20.0, -1.0])
print(f"10*col0 + 20*col1 - 1*col2 = {data @ relation}")
print("All zeros, so the relation vector is in the null space of data. Moving 10")
print("hours and 20 attendance units against each other changes nothing, which")
print("is precisely why the score column is not independent information.")

print()
print("=== rank and invertibility ===")
print("For a square matrix, rank = n is the same statement as det != 0, which")
print("is the same statement as 'solvable for every b'. Three ways to ask:")
full_rank = np.array([[1.0, 2.0], [3.0, 4.0]])
rank_deficient = np.array([[1.0, 2.0], [2.0, 4.0]])
for label, M in (("full rank", full_rank), ("rank deficient", rank_deficient)):
    print()
    print(f"  {label}: {M.tolist()}")
    print(f"    matrix_rank  = {np.linalg.matrix_rank(M)}")
    print(f"    det          = {np.linalg.det(M)}")
    try:
        x = np.linalg.solve(M, np.array([1.0, 2.0]))
        print(f"    solve works  = {np.round(x, 6)}")
    except np.linalg.LinAlgError as err:
        print(f"    solve raises = {err}")
print()
print("All three agree, because they are three faces of one fact. Use whichever is")
print("most convenient: matrix_rank works on rectangular matrices, det is")
print("square-only, and solve actually computes something.")

print()
print("=== Rank as degrees of freedom, numerically ===")
# A 4x3 system with a redundant equation: 4 equations, 3 unknowns, rank 3.
A_sys = np.array([[1.0, 2.0, 3.0],
                  [4.0, 5.0, 6.0],
                  [7.0, 8.0, 10.0],
                  [5.0, 7.0, 9.0]])       # row 3 = row 0 + row 1
b_sys = np.array([10.0, 20.0, 31.0, 30.0])
r_sys = int(np.linalg.matrix_rank(A_sys))
print(f"A_sys is {A_sys.shape}, rank {r_sys}")
print(f"unknowns - rank = {A_sys.shape[1]} - {r_sys} = {A_sys.shape[1] - r_sys} free unknowns")
# A_sys is not square, so solve() refuses. lstsq handles it: when the system is
# consistent and full rank, least squares gives the unique solution anyway.
x, residuals, rank_sys, _ = np.linalg.lstsq(A_sys, b_sys, rcond=None)
print(f"lstsq solution x = {np.round(x, 6)}")
print(f"residuals       = {np.round(A_sys @ x - b_sys, 12)}")
print("(np.linalg.solve refuses a non-square matrix; lstsq is the right tool and")
print(" gives the same answer whenever the system is consistent.)")
print("One of the four equations is redundant, so it adds no constraint and the")
print("solution is still unique. Over-determined is fine; over-determined and")
print("inconsistent is not, and that distinction is about b, not about A.")

# An underdetermined system: 2 equations, 3 unknowns, rank 2.
A_under = np.array([[1.0, 2.0, 3.0], [2.0, 1.0, 0.0]])
b_under = np.array([6.0, 2.0])
print()
print(f"A_under is {A_under.shape}, rank {int(np.linalg.matrix_rank(A_under))}")
x_ls, residuals, rank_ls, _ = np.linalg.lstsq(A_under, b_under, rcond=None)
print(f"lstsq gives the minimum-norm solution {np.round(x_ls, 6)}")
print(f"  residuals = {np.round(A_under @ x_ls - b_under, 12)}")
print(f"  that is one of infinitely many solutions; check by adding the null vector:")
u2, s2, vt2 = np.linalg.svd(A_under)
null_dir = vt2[2:, :][0]
print(f"  null direction = {np.round(null_dir, 6)}")
other = x_ls + 5.0 * null_dir
print(f"  x_ls + 5*null = {np.round(other, 6)}")
print(f"  residuals of that too = {np.round(A_under @ other - b_under, 12)}")
print("One free unknown, so the solution set is a line, and lstsq returns the")
print("point of that line nearest the origin. That is a free choice, not a fact")
print("about the system.")

print()
print("=== Feature selection by rank ===")
# Adding a column that is a combination of existing ones must not change rank.
extra = 2.0 * data[:, 0] - 3.0 * data[:, 1]
grown = np.column_stack([data, extra])
print(f"data shape {data.shape}, rank {np.linalg.matrix_rank(data)}")
print("added a column equal to 2*col0 - 3*col1")
print(f"grown shape {grown.shape}, rank {np.linalg.matrix_rank(grown)}")
print("Same rank, one more column to store. That is the arithmetic behind every")
print("warning about redundant features, and behind why dropping one is free.")

print()
print("=== Numerical rank versus exact rank ===")
# Exactly rank 1, plus a perturbation far below the default tolerance.
exactly_rank_one = np.array([[1.0, 2.0, 3.0],
                             [1e-17, 2e-17, 3e-17]])
print(f"matrix =\n{exactly_rank_one}")
print("row 1 is exactly 1e-17 * row 0, so the exact rank is 1 and so is the")
print(f"computed rank: {np.linalg.matrix_rank(exactly_rank_one)}")

# Now break the exact proportionality by an amount smaller than the default
# tolerance but larger than zero. The exact rank becomes 2.
perturbed = np.array([[1.0, 2.0, 3.0],
                      [1e-17, 2e-17, 3.1e-17]])
print()
print(f"matrix =\n{perturbed}")
print("row 1 is no longer a multiple of row 0 (note the 3.1), so the EXACT rank")
print("is 2. But the second direction is 1e-17, far below the default tolerance:")
print(f"  matrix_rank, default tolerance = {np.linalg.matrix_rank(perturbed)}")
print(f"  matrix_rank, tol = 1e-30        = {np.linalg.matrix_rank(perturbed, tol=1e-30)}")
print(f"  singular values = {np.linalg.svd(perturbed, compute_uv=False)}")
print("Rank is always computed against a tolerance, and the tolerance is a")
print("judgement call. SVD makes it a first-class parameter for exactly this")
print("reason. A 'rank 1' answer on noisy data means the second direction is")
print("below your noise floor, not that it does not exist.")
```

## Common Mistakes

**Mistake 1: taking the row space basis from the original matrix.** The wrong
version: "the basis for the row space is the nonzero rows of `A`." The right
version: the basis for the **row** space is the nonzero rows of the *reduced*
matrix, and the basis for the **column** space is the pivot columns of the
*original* matrix. Both counts equal the rank, so the mistake is invisible if you
only want the number — and produces a wrong set when you want the vectors.

**Mistake 2: expecting `m ≠ n` to mean the ranks differ.** The wrong version: "a
`3 × 50` matrix has row rank 3 and column rank 50." The right version: the row
rank is at most 3, the column rank at most 50, and they are **equal**. A `3 × 50`
matrix can have rank at most 3, and if it does, its null space has dimension 47.
This is why a dataset with 3 rows has nothing worth calling a basis for 50 columns.

**Mistake 3: thinking a redundant column changes the rank.** The wrong version:
"adding a column always raises the rank by one." The right version: it raises the
rank only if the new column is outside the current span. A column that is any
combination of existing ones is free to add, and equally free to drop. This is
the whole basis for feature selection, and the reason correlation-based filtering
picks worse subsets than PCA.

**Mistake 4: saying "rank 3" about noisy data without a tolerance.** The wrong
version: "the matrix has rank 2". The right version: rank is always
"rank *at some threshold*". A perturbation of `1e-17` makes the exact rank jump
while the computed rank does not move. When the answer depends on the threshold,
say so, or report singular values instead.

**Mistake 5: confusing rank with dimension of the ambient space.** The wrong
version: "a `4 × 7` matrix has dimension 4". The right version: the matrix has
rank at most 4; its column space is a subspace of `ℝ⁴`; its row space is a
subspace of `ℝ⁷`. `4` and `7` are the ambient dimensions, not the rank, and the
rank is whatever the pivots say.

---

## Formula Sheet

`A` is `m × n`; `a_ij` is row `i`, column `j`; `r = rank(A)`; `B` is a list of
vectors; `x ∈ ℝⁿ`; `y ∈ ℝ^m`; `S` is a set of vectors; `dim` is dimension;
`piv` is the list of pivot columns of the RREF; `TOL` is the threshold below
which an entry counts as zero.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `span(B)` | `$\{\sum_j c_j b_j : c_j \in \mathbb{R}\}$` | Everything buildable by scaling and adding the generators. | Defining what a space *is* |
| **basis** | `B` with `span(B) = S` **and** `B` independent | Reaches everything, nothing redundant. Two requirements, not one. | Any statement about a space's size |
| `dim(S)` | number of vectors in **any** basis of `S` | The length of every basis, not just a convenient one. | "How many real factors are here?" |
| Rank theorem | `dim(row space) = dim(col space) = \# piv` | Both equal the pivot count. There is only **one** rank. | Never qualify "the rank of `A`" |
| `rank(A)` | `= \#\{j : \text{column } j \text{ is a pivot column}\}` | Count pivots in the RREF. Works for any `m × n`. | Every rank computation |
| `rank(A) \le \min(m, n)` | — | An upper bound, not a default. `m \ne n` does **not** mean the ranks differ. | Mistake 2's correction |
| `nullity(A)` | `= n - r` | Free unknowns in `Ax = b`. | Degrees of freedom |
| Left nullity | `= m - r` | Relations among the **rows**. Apply rank-nullity to `Aᵀ`. | Redundant equations |
| Rank-nullity | `rank(A) + nullity(A) = n`; `rank(A) + leftnull(A) = m` | Independent count plus free count equals column count. | Counting parameters |
| Row space | `span` of the rows, a subspace of `ℝⁿ` | What the matrix *says*. | Linear regression models |
| Column space `im(A)` | `{Ax : x ∈ ℝⁿ}`, a subspace of `ℝ^m` | What the matrix *can produce*. Reachability of `b`. | Consistency tests |
| `ker(A)` | `\{x \in \mathbb{R}^n : Ax = 0\}`, dim `n − r` | Invisible directions: the parts of a vector the matrix discards. | Model non-identifiability |
| `ker(Aᵀ)` | `\{y \in \mathbb{R}^m : Aᵀy = 0\}`, dim `m − r` | `y₁row₁ + … + y_m row_m = 0`, i.e. all row relations. | Which equations are redundant |
| Row-space basis | nonzero rows of `rref(A)` — from the **reduced** matrix | Simplified, but spans the same set. | Mistake 1's correction |
| Column-space basis | pivot columns of the **original** `A` | Taken from `A` itself, not from the RREF. | The most-mixed-up step in the subject |
| Null-space basis | one vector per free column: set it to `1`, read pivot entries off the RREF as `−M[i][free]` | | Finding `ker(A)` |
| Four subspaces | dims `r, r, n − r, m − r` for col, row, ker, ker-transpose | Four spaces, two numbers, one row reduction. | The organisation of the subject |
| Consistency | `Ax = b` solvable `iff b \in col(A)` `iff rank(A) = rank([A\|b])` | `b` must be reachable. Depends on `b`, so not a rank-of-`A` question. | Lesson 32's diagnosis |
| Solution set | `x = x_p + \sum c_j v_j`, `c_j \in \mathbb{R}` | A point plus a span: an **affine** subspace of dim `n − r`. | "Infinitely many, here's the family" |
| Unique solution | needs `r = n`; for square `A` that is `det(A) \ne 0` | Full column rank. | Links to lessons 32 and 33 |
| Redundant column | `col_j \in span(others) \Rightarrow` rank unchanged, `span` unchanged | Free to add, free to drop. | Feature selection |
| Basis exchange | `v \notin V` ⟹ swap one `b_j` out of `B \cup \{v\}` for `v` | Grow a basis one dimension at a time. | Greedy selection algorithms |
| Greedy basis | keep `v` only if `rank(kept ∪ {v}) > rank(kept)` | The pivot rule, one column at a time. **Order-dependent.** | Why correlation filtering underperforms PCA |
| Exact rank vs computed | `rank_tol(A) = \#\{j : \|U_{jj}\| > tol \cdot \|A\|` | Always "rank at some threshold". | Mistake 4; noisy data |
| Singularity signal | a rank drop under a small perturbation | The matrix is nearly singular; solver answers are unreliable. | `cond` from lesson 32 |

## Multiple Choice Questions

**Q1.** For an `m × n` matrix `A` of rank `r`, what is the dimension of the null
space?

- A) `r`
- B) `m − r`
- C) `n − r`
- D) `m + n − r`

<details>
<summary>Answer and explanation</summary>

**C) `n − r`.**

Rank-nullity says `rank(A) + nullity(A) = n`, and `nullity(A) = dim ker(A)`, so
`dim ker(A) = n − r`. The `n` is the number of **columns**, because a null-space
vector is an input and inputs have one entry per column. The worked example
confirms it: the four-column matrix `A'` has rank 3, so the null space has
dimension `4 − 3 = 1`, and the found vector `(40, 0, −69, 59)` spans it. The
`3 × 3` full-rank case gives `3 − 3 = 0`, an empty null space, as stated.

- A) is the nullity of `Aᵀ` confused with `A`, and it uses the wrong ambient
  dimension. `Aᵀ` is `n × m`, so *its* nullity is `m − r`.
- B) is the **left** nullity, the dimension of `ker(Aᵀ)`. It is a real quantity
  and the lesson's four-space table has it, but it lives in `ℝ^m` and counts row
  relations, not input directions.
- D) double-counts. `m + n − r` is the total dimension of all four spaces summed
  with multiplicity (`r + r + (n−r) + (m−r)` is `m + n`, with no `r` at all), and
  no single space has that dimension.

</details>

**Q2.** You compute the RREF of `A` and find pivot columns 0, 1, and 2. Which
statement about the column space of `A` is correct?

- A) Columns 0, 1, 2 of the **RREF** form a basis for the column space of `A`
- B) Columns 0, 1, 2 of the **original** `A` form a basis for the column space of
  `A`
- C) The nonzero rows of the RREF form a basis for the column space
- D) The pivot columns of the RREF span a different space, because row operations
  change the column space

<details>
<summary>Answer and explanation</summary>

**B) Columns 0, 1, 2 of the **original** `A` form a basis for the column space of
`A`.**

Two facts make this work and both are stated in the lesson's explanation of the
theorem. First, the pivot columns of the *original* `A` are linearly independent:
in the RREF each has a leading `1` in a row where no other pivot column has one,
and row operations are invertible, so that independence survives. Second, every
non-pivot column of `A` is a combination of them, because non-pivot columns
correspond to free variables. So the `r` pivot columns of the original matrix span
`col(A)` and are independent — a basis.

- A) is Mistake 1, and it is the single most common error in this subject. The RREF
  is in a different coordinate system; its pivot columns are `(1,0,…,0)^T`,
  `(0,1,0,…,0)^T`, and so on, which span all of `ℝ^n` when the rank is `n` and so
  say nothing about `col(A)`.
- C) is the same mistake with rows and columns swapped. The nonzero RREF rows are
  a basis for the **row** space, which is a subspace of `ℝ^n`, not the column space
  of `ℝ^m`. For a non-square matrix these are different sets in different spaces.
- D) is false, and the distinction is the point: row operations preserve the row
  space exactly, and they do *not* preserve the column space — which is precisely
  why you must go back to the original matrix for the column-space basis.

</details>

**Q3.** `A` is `3 × 50`. What can you say about its row rank and column rank?

- A) Row rank is at most 3, column rank is at most 50, and they are equal
- B) Row rank is 3 and column rank is 50, because there are 3 rows and 50 columns
- C) Row rank equals column rank only when `m = n`
- D) Column rank is at most 3, row rank is at most 50

<details>
<summary>Answer and explanation</summary>

**A) Row rank is at most 3, column rank is at most 50, and they are equal.**

Both are bounded by `min(3, 50) = 3` — the row rank by the number of rows, the
column rank by the number of rows again, since the column space is a subspace of
`ℝ³` — and the theorem says they agree. The lesson's own correction of Mistake 2
is precisely this: "the row rank is at most 3, the column rank at most 50, and
they are **equal**."

- B) is Mistake 2 verbatim, and it is wrong twice. It reads the rank off the shape
  instead of counting pivots, and it assigns different values to the two ranks. A
  matrix with three rows has at most three independent rows no matter how many
  columns it has.
- C) is false; the row-rank-equals-column-rank theorem is stated for *every*
  matrix, and rectangular cases are where it earns its keep. It is what lets one
  algorithm — row reduction — answer questions about two spaces living in
  different ambient dimensions.
- D) has the roles of `m` and `n` swapped. The column space is a subspace of `ℝ^m`,
  so it is bounded by `m = 3`; the row space is a subspace of `ℝ^n`, so it is
  bounded by `n = 50`. A subspace of a 3-dimensional space has dimension at most 3
  no matter how many vectors span it.

</details>

**Q4.** A dataset has 3 columns, and you add a fourth column that happens to be
`2 ×` the third. What happens to the rank?

- A) It rises from 3 to 4, because a new column is new data
- B) It rises from 3 to 4 unless the coefficients are exact integers
- C) It is unchanged, because the new column lies in the existing span
- D) It falls, because the matrix is no longer square

<details>
<summary>Answer and explanation</summary>

**C) It is unchanged, because the new column lies in the existing span.**

`2 × col3` is a linear combination of the existing columns — a combination with a
single nonzero coefficient — so it adds no new direction. `span` is unchanged,
rank is unchanged, and the null space grows by one dimension. The lesson's
`A'` is exactly this case: column 3 is column 2 plus ten times the all-ones
column, `rank(A') = 3` for a four-column matrix, and the null space has
dimension `4 − 3 = 1`. The code's dataset is the same shape, with `score = 10 ×
hours + 20 × attendance`, so `rank = 2` out of three columns.

- A) is Mistake 3. "New data" and "new direction" are different: you can add a
  column that changes every predicted value while carrying no information, because
  it is determined by columns you already had.
- B) is not a thing. Scalars are real; `2` is as legitimate a coefficient as
  `0.5`. What matters is whether the column is in the span, and the coefficients
  involved in a genuine dependency are usually ugly fractions, as the worked
  example's `x = (40, 0, −69, 59)` shows.
- D) confuses rank with the shape. A `3 × 4` matrix is perfectly ordinary, and
  its rank is still bounded by 3. The lesson's four-space table is written for
  rectangular matrices precisely because they are the interesting case.

</details>

**Q5.** A greedy routine picks a basis by keeping a vector only if it raises the
rank of the set so far. It tries columns in the order `c₀, c₁, c₂` and then again
in the order `c₂, c₀, c₁`. Both runs produce a 2-element basis of the same 2-D
space. Is that a bug?

- A) Yes — a basis is unique, so two different answers mean one is wrong
- B) Yes — a greedy routine must be order-independent to be correct
- C) No — a basis is not unique; only the span is. The lesson's code shows exactly
  this, keeping different columns in different orders
- D) No, but only because the dimension happened to be 2

<details>
<summary>Answer and explanation</summary>

**C) No — a basis is not unique; only the span is. The lesson's code shows exactly
this, keeping different columns in different orders.**

The lesson's dataset has `rank = 2` with three columns, where the score column is
`10 × hours + 20 × attendance`. Trying the columns in the original order the greedy
routine keeps the hours and attendance columns; trying them score-first it keeps
the score and attendance columns. Different lists, same span, same dimension. The
text says so directly: "Two different bases of the same space. That is the whole
point: a basis is not unique, the span is."

- A) confuses the space with one description of it. Uniqueness of basis *size* is
  the theorem the lesson proves — every basis has the same number of vectors — but
  that is about *how long*, never about *which vectors*.
- B) is a real concern about greedy methods, and the lesson raises it, but it is not
  an error in the mathematics. Order-dependence is a property of the *algorithm*,
  not of the basis, and it is exactly why greedy feature selection picks worse
  subsets than PCA: the code's closing lines make this argument.
- D) is a non-reason. Non-uniqueness holds at every dimension, and the theorem
  that *does* constrain dimension (`dim` is basis-independent) is satisfied in
  both runs. The two bases have the same length, which is what the theorem
  guarantees.

</details>

**Q6.** Row reduction gives `rref(A) = I₃` for a `3 × 3` matrix `A`. What does that
tell you about `ker(A)`?

- A) `ker(A) = {0}`, dimension 0
- B) `ker(A) = ℝ³`, because the RREF is the identity
- C) `ker(A)` has dimension 1, since `A` must have a kernel
- D) `ker(A) = {0}` but the row space is also `{0}`

<details>
<summary>Answer and explanation</summary>

**A) `ker(A) = {0}`, dimension 0.**

`I₃` has three pivots in three columns, so `rank = 3` and
`dim ker(A) = n − r = 3 − 3 = 0`. A zero-dimensional subspace contains exactly one
vector, and it must be the zero vector. Equivalently, `Ax = 0` has only the
trivial solution, which the worked example confirms directly from the RREF:
"the third row gives `x₂ = 0`, then the first gives `x₀ = 0`, the second gives
`x₁ = 0`."

- B) is a real confusion — the RREF *is* the identity, so the RREF's own null space
  is `{0}` — and the error is attributing the reduced matrix's kernel to `A`.
  Row operations change the null space unless you track the transform. In this
  case they happen to agree, but for a rank-deficient matrix they do not, and
  reading the kernel off the RREF directly is a mistake waiting to happen. The
  correct procedure is in the formula sheet: set each free variable to `1` and
  read the pivot entries off the RREF.
- C) is false because nothing forces a square matrix to have a kernel. `A = I₃`
  itself is a `3 × 3` with trivial kernel. A `3 × 3` matrix has a nontrivial
  kernel only when its determinant is zero, which is lesson 33.
- D) mixes up the spaces. The row space of a full-rank `3 × 3` is all of `ℝ³`,
  dimension 3, not `{0}`. `{0}` is the kernel, and the null space is the only one
  of the four spaces that can be `{0}` for a full-rank square matrix.

</details>

**Q7.** `A` is `4 × 3` with `rank = 3`. The left null space `ker(Aᵀ)` has
dimension 1. What does a basis vector of that space represent?

- A) A direction the matrix cannot see, i.e. an element of `ker(A)`
- B) A linear relation among the four **rows**: `y₁row₁ + … + y₄row₄ = 0`
- C) A combination of the three columns that produces `0`
- D) The right-hand side that makes the system inconsistent

<details>
<summary>Answer and explanation</summary>

**B) A linear relation among the four **rows**: `y₁row₁ + … + y₄row₄ = 0`.**

`Aᵀy = 0` says exactly `Σ_i y_i row_i = 0` with the coefficients collected up
front, and the lesson's code prints precisely that: a 4×3 matrix whose row 3 is
`row 0 + row 1` has left null space `[-1, -1, 0, 1]`, and the code renders it as
`+0*row0 +0*row1 -1*row2 +1*row3 = 0`, then verifies the weighted sum of rows is
`(0, 0, 0)`. The dimension is `m − r = 4 − 3 = 1`, so there is exactly one
independent way for the rows to be dependent.

- A) is the null space of `A`, not `Aᵀ`, and it lives in `ℝⁿ = ℝ³` while
  `ker(Aᵀ)` lives in `ℝ^m = ℝ⁴`. Here `dim ker(A) = n − r = 3 − 3 = 0`, so the two
  are very different — one is `{0}`, the other is a line.
- C) is `ker(A)` again, phrased as a column combination. It is the right idea
  (a dependence) attached to the wrong space.
- D) confuses a relation among the rows with a statement about `b`. The lesson is
  careful: consistency of `Ax = b` depends on `rank(A)` versus `rank([A|b])`, and
  the left null space says nothing about whether a given `b` is reachable.

</details>

**Q8.** The data matrix in the lesson's code has 3 columns and `rank = 2`, with
null space basis `[-10, -20, 1]`. You fit a linear model with all three
coefficients. What does that null vector tell you?

- A) The model has three coefficients and is fully determined by the data
- B) The coefficient on the score column is not identified: any value works if the
  other two adjust, because the null direction changes nothing in the output
- C) The model is over-parameterised in a way that makes the fit numerically
  unstable
- D) One of the three coefficients must be exactly zero

<details>
<summary>Answer and explanation</summary>

**B) The coefficient on the score column is not identified: any value works if the
other two adjust, because the null direction changes nothing in the output.**

`[-10, -20, 1]` is a vector with `A v = 0`, so moving the coefficients by any
multiple of it leaves every fitted value unchanged. The lesson's code spells out
the reading: "moving 10 hours and 20 attendance units in opposite directions
changes nothing in the output." Concretely, `c` and `c + t·[-10, -20, 1]` fit
equally well for every `t`, so the individual coefficients are not determined by
the data — only `r = 2` combinations of them are.

- A) is the count without the constraint. Three coefficients and rank 2 means two
  determined combinations and one undetermined direction; you cannot have three
  identified coefficients out of two independent features.
- C) is a different and non-sequitur claim. Rank deficiency is about
  *identification*, not numerical stability, and the lesson's lesson 32 and 33
  material covers conditioning separately. A rank-2 design matrix can be perfectly
  well-conditioned; the issue is that the answer is not unique, not that it is
  inaccurate.
- D) confuses "not identified" with "zero". No coefficient is forced to be zero;
  rather, a whole line of coefficient vectors fits identically, and no software
  will tell you which point on it to trust. Dropping a column is the practical fix,
  and the lesson's feature-selection discussion is why.

</details>

## Subjective Questions

### Short Answer

**Q1. Define a basis, and state why both halves of the definition are needed.**

<details>
<summary>Model answer</summary>

A list of vectors `B = (v₁, …, v_k)` is a **basis** for a set of vectors `S` if

1. `span(B) = S` — it generates everything in `S`; and
2. `B` is linearly independent — nothing in it is a combination of the others.

Both halves are needed. Drop (2) and you have a generating set, which may be
arbitrarily long: `{v₁, v₂, v₁ + v₂}` spans the same space as `{v₁, v₂}` but is
longer and less useful. Drop (1) and you have an independent list that reaches
some larger space, so it says nothing about `S` itself. The lesson's greedy routine
implements exactly this: keep a vector only if the rank goes up, which is (1) and
(2) in one test.

</details>

**Q2. State the row-rank-equals-column-rank theorem, and explain where the two
counts come from.**

<details>
<summary>Model answer</summary>

For every matrix `A`, `dim(row space) = dim(col space)`, and both equal the number
of pivots in any row echelon form of `A`.

The row-space count is easy: row operations preserve the row space, so the `r`
nonzero rows of the RREF span it and are independent (each has a leading `1` in a
row where no other has one). For the column space: the pivot columns of the
**original** `A` are linearly independent, by the same leading-`1` argument
transferred back through the invertible row operations; and every non-pivot column
of `A` is a combination of them, because non-pivot columns correspond to free
variables. So there are exactly `r` of them and they span. Both counts are the
pivot count.

The subtlety worth remembering: the row-space basis comes from the *reduced*
matrix, the column-space basis from the *original*. Mixing them up is Mistake 1,
and it is invisible if you only want the number.

</details>

**Q3. State rank-nullity in both its forms, and say which ambient dimension
appears in each.**

<details>
<summary>Model answer</summary>

For an `m × n` matrix `A`:

    rank(A) + nullity(A) = n
    rank(A) + left nullity(A) = m

The first form pairs the column space (dimension `r`) with the null space
(dimension `n − r`), and both spaces live in `ℝⁿ`, which is where the `n` comes
from. The second is the same statement applied to `Aᵀ`, which is `n × m`, so the
column count is `m`.

The reason is the free-variable count. In the RREF, each pivot variable is
determined by the free variables, so a solution is `x = x_p + Σ c_j v_j` with one
parameter per non-pivot column, and there are `n − r` non-pivot columns. For a
square `A` the first form is `rank + nullity = n`, so a trivial null space is
exactly `rank = n`, which is exactly `det(A) ≠ 0`.

</details>

**Q4. State the four fundamental subspaces with their ambient spaces and
dimensions, and say where each basis comes from.**

<details>
<summary>Model answer</summary>

For an `m × n` matrix `A` of rank `r`:

| Space | Ambient | Dimension | Basis from |
| --- | --- | --- | --- |
| column space `im(A)` | `ℝ^m` | `r` | pivot columns of the **original** `A` |
| row space `im(Aᵀ)` | `ℝ^n` | `r` | nonzero rows of `rref(A)` |
| null space `ker(A)` | `ℝ^n` | `n − r` | free columns of `rref(A)` |
| left null space `ker(Aᵀ)` | `ℝ^m` | `m − r` | free columns of `rref(Aᵀ)` |

The dimensions sum to `r + r + (n − r) + (m − r)`, and the two in `ℝ^n` give `n`
while the two in `ℝ^m` give `m` — rank-nullity, twice. Note that only the column
space and the left null space live in `ℝ^m`; mixing the two ambient spaces is
Mistake 5's territory. And note the column-space basis is the only one taken from
the original matrix.

</details>

**Q5. A column of your dataset is a linear combination of the others. What can you
delete, what can you not conclude, and what is the practical fix?**

<details>
<summary>Model answer</summary>

You can delete that column, or any one member of the dependent set, and the span
of the data is unchanged. Nothing inside the span is lost; the *description* gets
shorter. This is the whole basis of feature selection, and it is why a dataset with
100 columns and rank 3 stores three numbers' worth of information per row.

What you must **not** conclude: that the data "has 99 features" (it has 100
columns and 3 degrees of freedom), that the column is noise (it is an exact
combination, and dropping it loses nothing), or that dropping a *different* column
would be equally safe in a later fit (any member of the dependent set works for the
span, but the choice changes the coefficients you get).

The practical fix is to find a basis first and fit on that. Use `np.linalg.svd` or
the greedy pivot-column rule: keep a column only when the rank goes up. And be
explicit about the tolerance, because a column that is *nearly* a combination is a
judgement call — that is Mistake 4, and the honest diagnostic is to look at
singular values rather than declare a rank.

</details>

**Q6. Give an example where the greedy basis routine returns a different basis
depending on the order it tries columns, and say why that matters in practice.**

<details>
<summary>Model answer</summary>

The lesson's own dataset is the example: three columns, `score = 10 × hours + 20 ×
attendance`, so `rank = 2` and any two of the three columns form a basis. Trying
them in the original order, the greedy routine keeps hours and attendance;
reordered score-first, it keeps score and attendance. The lesson prints both.

It matters because the choice of subset is not random noise but a real modelling
decision with consequences. A greedy rule that keeps `height_in_cm` and drops
`height_in_m` produces a model whose coefficients are numerically terrible,
because the two kept columns are nearly parallel. A rule that keeps a physically
meaningful column and drops an alias is better. PCA avoids the problem by not
choosing a subset at all — it takes `rank` linear combinations, which is why the
lesson says greedy selection "can pick a worse subset than the one PCA finds", and
why correlation-based filtering is called out as a shortcut that ignores the
linear structure.

</details>

### Long Answer

**Q1. Why does row rank equal column rank? What breaks if this theorem were
false?**

<details>
<summary>Model answer</summary>

**The argument.** Row operations are invertible — each of the three permitted
operations is a step of Gaussian elimination with a matrix inverse — so they
preserve linear independence relations *among the columns*. Now reduce `A` to its
echelon form `E` and count `r` pivots.

*Row space.* `E` and `A` have the same row space, because row operations only
recombine the rows. The `r` nonzero rows of `E` span it, and they are independent
(each has a leading `1` in a row where no other has one). So `dim row space = r`.

*Column space.* The `r` pivot columns of `E` are independent by the same
leading-`1` argument. Since `E = E' A` for some invertible `E'`, and invertible
maps preserve independence, the corresponding `r` pivot columns of `A` are also
independent. For the other direction, every non-pivot column of `E` is zero, and
`E = E' A` says those columns of `A` are `E'⁻¹` applied to a zero vector, hence
`E'⁻¹ · 0 = 0`… more carefully: the non-pivot column of `E` is a combination of
the pivot columns of `E`, and pulling back through `E'⁻¹` shows the non-pivot
column of `A` is the same combination of the pivot columns of `A`. So the `r` pivot
columns of `A` span `col(A)`. Hence `dim col space = r`.

Both counts are the same `r`. That is the theorem, and its proof is short because
both halves reuse the same observation: **pivot columns are the independent ones,
in both spaces simultaneously.**

**What breaks if it were false.** Almost everything the subject is organised
around.

- *Rank would not be a well-defined concept.* You could not say "the rank of `A`"
  without qualifying which space you meant, and every downstream claim would need
  two versions. The lesson's correction of Mistake 2 is exactly this: `m ≠ n` does
  not mean the two ranks differ, because there is only one number.
- *One algorithm could not answer both questions.* Row reduction is the only
  practical way to find either space, and it is the *same* computation. If the two
  counts could differ, you would have no reason to expect one pass to serve both,
  and the four-space table would not be computable from a single RREF.
- *Rank-nullity would have no consistent ambient.* The identity pairs `rank` with
  `nullity` to give `n` and with `left nullity` to give `m`. That works precisely
  because `rank` is a single number sitting in both `ℝ^n` and `ℝ^m` at once.
- *The determinant would lose its meaning as a rank test.* `det(A) = 0` is
  "the rows are dependent". Lesson 33 equates that with "the columns are
  dependent" — which is this theorem, applied to a square matrix.
- *Nearly every real algorithm would need two passes.* Compressed sensing, matrix
  completion, and low-rank approximation are all built on "the number of
  independent columns is small", and they use row reduction once. A matrix of rank
  `r` in the row sense but rank `s > r` in the column sense would not be a coherent
  object.

The deeper reason the theorem feels slightly mystical is that the row space and
column space are genuinely different sets, often living in different ambient
spaces, and yet the theorem says they have equal dimension. It is a fact about
matrices, not about vectors, and it is the hinge on which the whole subject turns.

</details>

**Q2. Why must you take the column-space basis from the original matrix and the
row-space basis from the RREF? What goes wrong if you do it the other way round?**

<details>
<summary>Model answer</summary>

**Why they differ.** Row operations are left multiplication: `A → E'A` for
invertible `E'`. This recombine the rows, so the row space is preserved and the
column space generally is not. Concretely, in `rref(A)` every pivot column is a
unit vector `(1, 0, …, 0)^T`. Those span all of `ℝ^n` when the rank is `n`, which
tells you nothing whatsoever about the column space of `A` — the actual set of
vectors `Ax` can produce.

So the column-space basis must come from `A`: the pivot *columns* of the original
matrix, which the theorem shows are independent and spanning. The row-space basis
may come from either, but is usually taken from the RREF because the reduced rows
are simpler — the nonzero rows of `rref(A)`.

**What goes wrong in each direction.**

Taking the RREF's pivot columns as the column-space basis gives you `(1,0,…,0)^T`
and friends, which span `ℝ^n` and have the right *number* of vectors, so any check
on the dimension passes. The failure is in the *vectors*: the set you report is
not a subset of `col(A)` and generates a different space entirely. If you used it
to decide whether some `b` is reachable, every `b` would look reachable. If you
used it to find a least-squares fit, you would be projecting onto the wrong
subspace.

Taking the original rows as the row-space basis is subtler. They *do* span the row
space — that is what Mistake 1's wrong version says, and it is true as a claim
about the span. It fails in the "nothing redundant" half: after a non-pivot column
is present, the original rows can be dependent. In the lesson's `4 × 3` example
with `row 3 = row 0 + row 1`, the original four rows are dependent, so they are
not a basis. Take the RREF's nonzero rows and you are guaranteed independence.

**Why the error survives casual testing.** Both mistakes give the right *count*.
`dim` is basis-independent, so any routine that only reports a number — `rank`, a
`min`-bound, a cost estimate — is unaffected. The bug only appears when you use
the vectors: a null space basis, a projection, a reachability test, a
feature-selection output. That is why the lesson's code prints the actual vectors
and the actual products rather than just the dimensions, and why its checks are of
the form "does this vector satisfy `Ax = 0`?" rather than "is the length right?".

**The habit that prevents it.** Treat the RREF as a description of the *system*
(solutions, free variables) and the original `A` as the description of the
*matrix* (its columns, its reachable set). Every time you cross from one to the
other, ask which object you are reading.

</details>

**Q3. A dataset has 5000 rows and 3 columns, and the rank of the centred data
matrix is 2. What does that mean, what can you do about it, and what must you not
conclude?**

<details>
<summary>Model answer</summary>

**What it means.** The 5000 rows, viewed as vectors in `ℝ³` after centring, occupy
a 2-dimensional subspace. Equivalently the three columns satisfy one non-trivial
linear relation, so one is a combination of the other two and the data has exactly
two independent factors. The row count is irrelevant to this number — rank 2 is
rank 2 whether there are 5 rows or 5 million. Nullity is `n − r = 3 − 2 = 1`, so
there is one direction in `ℝ³` the data never moves in, and `dim ker(A) = 1` names
it.

**What you can do.** Drop one member of the dependent set and store the rest. The
span is unchanged, so nothing inside the data space is lost; the description is
shorter. Equivalently, keep all three columns and fit with one fewer independent
coefficient. Concretely, PCA keeps `r = 2` components and compresses 3 columns to 2
with zero information loss. The lesson's dataset is this exact case: `score = 10 ×
hours + 20 × attendance`, rank 2, null space `[-10, -20, 1]`.

**What you must not conclude.**

1. *Not* "the data has three features". It has three columns and two degrees of
   freedom. Any model with three coefficients on these columns has one
   unidentifiable direction, and software will silently pick a point on that line
   for you. The null vector tells you which direction: any multiple of it changes
   the coefficients without changing a single fitted value.
2. *Not* that this is a numerical accident to be ignored. A rank drop is the
   signal that a matrix is nearly singular; `cond` from lesson 32 will be large, and
   solver answers will be unreliable. Rank 2 and rank 3 in a *nearly* dependent
   matrix are the same phenomenon at different thresholds, which is Mistake 4.
3. *Not* that the third column is noise. It is an exact combination, and if you
   delete it you lose nothing — but you also gain nothing you did not already
   have. A column that is 99.9% predictable is a different decision, and the
   honest diagnostic is the singular value spectrum, not a binary rank.
4. *Not* that the row count helps. 5000 rows do not rescue a rank-2 design matrix;
   rank depends only on the columns' linear structure. This is the standard
   confusion behind "we have plenty of data, so overfitting is impossible" — with
   rank 2, adding rows never identifies the third coefficient.

**The practical rule.** Find the relation first (`A v = 0` gives `v`), so you know
*which* column to drop rather than guessing; then fit on a basis. And report the
singular values rather than a bare rank whenever the answer will be used for
something consequential.

</details>

**Q4. Why does rank not have a single answer, and what would break if we treated
it as if it did?**

<details>
<summary>Model answer</summary>

**Why.** Because the rank a routine reports is a function of a threshold, and
there is no threshold-free notion of "zero" in floating point. The formal
definition — the number of pivots, equivalently the largest `r` for which some
`r × r` minor is nonzero — is exact and unambiguous over a field. In practice
the routine applies `TOL`, and `rank_tol(A)` is a step function of `TOL`. A
perturbation of `1e-17` changes the exact rank while leaving the computed rank
fixed at any reasonable tolerance; a perturbation of `1e-9` may or may not, depending
on where `TOL` sits. The lesson's Mistake 4 says this directly: "rank is always
'rank *at some threshold*'."

**The two things that break.**

First, *reproducibility of decisions*. If a pipeline thresholds on rank — "drop
columns until the rank stops dropping", "reject the model if rank < 5" — then the
result depends on a parameter nobody wrote down. Two engineers running the same
code on the same data can legitimately report different ranks, and the disagreement
is not a bug to be filed but a consequence of a choice that was never stated.

Second, *the conflation of exact and near dependence*. A matrix that is exactly
singular and one whose smallest singular value is `1e-14` are different objects
with opposite practical consequences: the first has no inverse, the second has an
inverse that is garbage. If "rank" collapses these, you either throw away solvable
problems or trust unsolvable ones. This is why the lesson's formula sheet offers
the singular-value-based statement as the honest one.

**What to do instead.** Report the singular values, and state the threshold
alongside any rank you quote. `np.linalg.matrix_rank(A, tol=...)` and
`np.linalg.cond(A)` both make the dependence explicit, and the SVD in
[lesson 40](40_svd_and_pca.md) is the tool that turns "is it dependent" into "how
badly", which is a continuous question with a numerical answer. For a dataset,
this is the difference between "the score column is a duplicate of hours and
attendance" and "the score column is 0.999 correlated with something", which are
decisions you would not want to make by accident.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — rank and a basis for each.** For each matrix, report the rank,
verify row rank equals column rank, and give a basis for the column space:

1. the zero 3×3
2. the identity 3×3
3. the all-ones 3×3
4. `[[1,2,3],[4,5,6],[7,8,9]]`
5. `[[1,2],[3,4],[4,6]]`
6. a 4×3 whose last row is zero
7. `[[1,2,0,1],[0,1,1,0],[1,3,1,1]]`

<details>
<summary>Solution</summary>

```python
TOL = 1e-9


# ---------------------------------------------------------------- helpers
def shape(M):
    return len(M), len(M[0])


def zeros(rows, cols):
    return [[0.0] * cols for _ in range(rows)]


def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def transpose(M):
    rows, cols = shape(M)
    return [[M[i][j] for i in range(rows)] for j in range(cols)]


def rref(A, tol=TOL):
    M = [list(row) for row in A]
    rows, cols = len(M), len(M[0])
    pivot_row = 0
    pivots = []
    for col in range(cols):
        best = None
        for r in range(pivot_row, rows):
            if abs(M[r][col]) > tol:
                best = r
                break
        if best is None:
            continue
        M[pivot_row], M[best] = M[best], M[pivot_row]
        p = M[pivot_row][col]
        M[pivot_row] = [v / p for v in M[pivot_row]]
        for r in range(rows):
            if r != pivot_row and M[r][col] != 0.0:
                f = M[r][col]
                M[r] = [M[r][c] - f * M[pivot_row][c] for c in range(cols)]
        pivots.append(col)
        pivot_row += 1
    M = [[v + 0.0 for v in row] for row in M]
    return M, pivots


def rank(A, tol=TOL):
    _, pivots = rref(A, tol)
    return len(pivots)


def row_space_basis(A, tol=TOL):
    M, _ = rref(A, tol)
    return [list(row) for row in M if any(abs(v) > tol for v in row)]


def column_space_basis(A, tol=TOL):
    _, pivots = rref(A, tol)
    return [[A[i][c] for i in range(len(A))] for c in pivots]


def null_space(A, tol=TOL):
    M, pivots = rref(A, tol)
    cols = shape(A)[1]
    free = [c for c in range(cols) if c not in pivots]
    basis = []
    for fc in free:
        v = [0.0] * cols
        v[fc] = 1.0
        for i, pc in enumerate(pivots):
            v[pc] = -M[i][fc]
        basis.append(v)
    return basis


matrices = {
    "zero 3x3": zeros(3, 3),
    "identity 3x3": identity(3),
    "all ones 3x3": [[1.0] * 3 for _ in range(3)],
    "1 2 3 / 4 5 6 / 7 8 9": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]],
    "rank 2, row3 = row1+row2": [[1.0, 2.0], [3.0, 4.0], [4.0, 6.0]],
    "4x3 with a zero row": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0],
                            [7.0, 8.0, 10.0], [0.0, 0.0, 0.0]],
    "3x4 tall": [[1.0, 2.0, 0.0, 1.0],
                 [0.0, 1.0, 1.0, 0.0],
                 [1.0, 3.0, 1.0, 1.0]],
}
for label, M in matrices.items():
    r = rank(M)
    Mrr, pivots = rref(M)
    row_b = row_space_basis(M)
    col_b = column_space_basis(M)
    print(f"--- {label}  ({shape(M)[0]}x{shape(M)[1]}) ---")
    print(f"  rank {r}, pivot columns {pivots}")
    print(f"  row rank {len(row_b)}, column rank {len(col_b)}, equal: "
          f"{len(row_b) == len(col_b)}")
    print("  a basis for the column space:")
    for v in col_b:
        print(f"    {v}")
    print(f"  nullity = {shape(M)[1]} - {r} = {shape(M)[1] - r}")
    print()

print("'1 2 3 / 4 5 6 / 7 8 9' has rank 2, not 3, because row 0 + row 2 = 2*row 1.")
print("The 4x3 with a zero row has rank 3: a zero row is a trivial dependence,")
print("so it costs nothing, but the other three rows are independent.")
print()
print("The 3x4 tall matrix has rank 2 in R^3 for its column space and in R^4 for")
print("its row space, and a null space of dimension 4 - 2 = 2: two of its four")
print("columns carry no new direction.")
```

Output:

```
--- zero 3x3  (3x3) ---
  rank 0, pivot columns []
  row rank 0, column rank 0, equal: True
  a basis for the column space:
  nullity = 3 - 0 = 3

--- identity 3x3  (3x3) ---
  rank 3, pivot columns [0, 1, 2]
  row rank 3, column rank 3, equal: True
  a basis for the column space:
    [1.0, 0.0, 0.0]
    [0.0, 1.0, 0.0]
    [0.0, 0.0, 1.0]
  nullity = 3 - 3 = 0

--- all ones 3x3  (3x3) ---
  rank 1, pivot columns [0]
  row rank 1, column rank 1, equal: True
  a basis for the column space:
    [1.0, 1.0, 1.0]
  nullity = 3 - 1 = 2

--- 1 2 3 / 4 5 6 / 7 8 9  (3x3) ---
  rank 2, pivot columns [0, 1]
  row rank 2, column rank 2, equal: True
  a basis for the column space:
    [1.0, 4.0, 7.0]
    [2.0, 5.0, 8.0]
  nullity = 3 - 2 = 1

--- rank 2, row3 = row1+row2  (3x2) ---
  rank 2, pivot columns [0, 1]
  row rank 2, column rank 2, equal: True
  a basis for the column space:
    [1.0, 3.0, 4.0]
    [2.0, 4.0, 6.0]
  nullity = 2 - 2 = 0

--- 4x3 with a zero row  (4x3) ---
  rank 3, pivot columns [0, 1, 2]
  row rank 3, column rank 3, equal: True
  a basis for the column space:
    [1.0, 4.0, 7.0, 0.0]
    [2.0, 5.0, 8.0, 0.0]
    [3.0, 6.0, 10.0, 0.0]
  nullity = 3 - 3 = 0

--- 3x4 tall  (3x4) ---
  rank 2, pivot columns [0, 1]
  row rank 2, column rank 2, equal: True
  a basis for the column space:
    [1.0, 0.0, 1.0]
    [2.0, 1.0, 3.0]
  nullity = 4 - 2 = 2
```

</details>

**[ ] Exercise 2 — prove row rank = column rank.** Write out the argument that
both counts equal the number of pivots, and verify the key claim numerically: for
a matrix of rank `r`, every column of `A` is a linear combination of the pivot
columns of `A`. Use `A` below, where column 2 is column 0 plus column 1.

    A = | 1  2   3 |
        | 4  5   9 |
        | 7  8  15 |
        | 5  7  12 |

<details>
<summary>Solution</summary>

```python
TOL = 1e-9


# ---------------------------------------------------------------- helpers
def shape(M):
    return len(M), len(M[0])


def zeros(rows, cols):
    return [[0.0] * cols for _ in range(rows)]


def transpose(M):
    rows, cols = shape(M)
    return [[M[i][j] for i in range(rows)] for j in range(cols)]


def rref(A, tol=TOL):
    M = [list(row) for row in A]
    rows, cols = len(M), len(M[0])
    pivot_row = 0
    pivots = []
    for col in range(cols):
        best = None
        for r in range(pivot_row, rows):
            if abs(M[r][col]) > tol:
                best = r
                break
        if best is None:
            continue
        M[pivot_row], M[best] = M[best], M[pivot_row]
        p = M[pivot_row][col]
        M[pivot_row] = [v / p for v in M[pivot_row]]
        for r in range(rows):
            if r != pivot_row and M[r][col] != 0.0:
                f = M[r][col]
                M[r] = [M[r][c] - f * M[pivot_row][c] for c in range(cols)]
        pivots.append(col)
        pivot_row += 1
    M = [[v + 0.0 for v in row] for row in M]
    return M, pivots


def rank(A, tol=TOL):
    _, pivots = rref(A, tol)
    return len(pivots)


def row_space_basis(A, tol=TOL):
    M, _ = rref(A, tol)
    return [list(row) for row in M if any(abs(v) > tol for v in row)]


def column_space_basis(A, tol=TOL):
    _, pivots = rref(A, tol)
    return [[A[i][c] for i in range(len(A))] for c in pivots]


def express(target, gens, tol=TOL):
    """Coefficients c with target = sum(c_j * gens[j]), or None if impossible."""
    n = len(target)
    k = len(gens)
    if k == 0:
        return [0.0] if all(abs(v) <= tol for v in target) else None
    G = [[gens[j][i] for j in range(k)] for i in range(n)]
    Mx = [list(G[i]) + [target[i]] for i in range(n)]
    pivot_cols = []
    r = 0
    for c in range(k):
        best = None
        for i in range(r, n):
            if abs(Mx[i][c]) > tol:
                best = i
                break
        if best is None:
            continue
        Mx[r], Mx[best] = Mx[best], Mx[r]
        for i in range(n):
            if i != r:
                f = Mx[i][c] / Mx[r][c]
                for j in range(c, k + 1):
                    Mx[i][j] -= f * Mx[r][j]
        pivot_cols.append(c)
        r += 1
    for i in range(len(pivot_cols), n):
        if abs(Mx[i][k]) > tol:
            return None
    x = [0.0] * k
    for i, c in enumerate(pivot_cols):
        x[c] = Mx[i][k] / Mx[i][c]
    return x


def print_matrix(label, M, width=8):
    rows, cols = shape(M)
    print(f"{label}  ({rows}x{cols})")
    for row in M:
        print("  | " + " ".join(f"{x:{width}.3f}" for x in row) + " |")


A = [[1.0, 2.0, 3.0],
     [4.0, 5.0, 9.0],
     [7.0, 8.0, 15.0],
     [5.0, 7.0, 12.0]]       # column 2 = column 0 + column 1
print_matrix("A", A)
print(f"rank {rank(A)}, so of the {shape(A)[1]} columns, "
      f"{len(column_space_basis(A))} are pivots and there is a non-pivot column "
      f"to express.")
print()
piv_cols = column_space_basis(A)
_, piv_indices = rref(A)
print(f"pivot column indices {piv_indices}")
print(f"pivot columns of A: {piv_cols}")
non_pivot = [j for j in range(shape(A)[1]) if j not in piv_indices]
print(f"non-pivot column indices {non_pivot}")
print()
print("Each column of A, expressed in terms of the pivot columns:")
for j in range(shape(A)[1]):
    col_j = [A[i][j] for i in range(len(A))]
    coeffs = express(col_j, piv_cols)
    check = [sum(coeffs[k] * piv_cols[k][i] for k in range(len(piv_cols)))
             for i in range(len(A))]
    print(f"  column {j} {col_j} = {coeffs} * pivot_columns")
    print(f"    check: {check}  matches: "
          f"{all(abs(check[i] - col_j[i]) < 1e-9 for i in range(len(A)))}")
print()
print("Column 2 is exactly pivot 0 + pivot 1, which is the redundancy the rank")
print("is measuring.")
print()
print("So the pivots span the column space. They are also independent: suppose")
print("sum c_j * pivot_j = 0, and look at the row where pivot_0 has its leading")
print("1. Only c_0 appears there, so c_0 = 0. Then look at pivot_1's leading row,")
print("and so on. Hence all c_j = 0, so the pivots are a basis and the column")
print("rank equals the number of pivots.")
print()
print("Combined with the row-space argument, both ranks are the pivot count, so")
print(f"they are equal: row rank {len(row_space_basis(A))} = column rank "
      f"{len(piv_cols)}.")
```

Output:

```
A  (4x3)
  |    1.000    2.000    3.000 |
  |    4.000    5.000    9.000 |
  |    7.000    8.000   15.000 |
  |    5.000    7.000   12.000 |
rank 2, so of the 3 columns, 2 are pivots and there is a non-pivot column to express.

pivot column indices [0, 1]
pivot columns of A: [[1.0, 4.0, 7.0, 5.0], [2.0, 5.0, 8.0, 7.0]]
non-pivot column indices [2]

Each column of A, expressed in terms of the pivot columns:
  column 0 [1.0, 4.0, 7.0, 5.0] = [1.0, -0.0] * pivot_columns
    check: [1.0, 4.0, 7.0, 5.0]  matches: True
  column 1 [2.0, 5.0, 8.0, 7.0] = [0.0, 1.0] * pivot_columns
    check: [2.0, 5.0, 8.0, 7.0]  matches: True
  column 2 [3.0, 9.0, 15.0, 12.0] = [1.0, 1.0] * pivot_columns
    check: [3.0, 9.0, 15.0, 12.0]  matches: True
```

The three-step argument in full:

1. Row reduction preserves the row space, so the nonzero rows of the RREF form a
   basis for it. Row rank = number of nonzero RREF rows.
2. The pivot columns of the original `A` are independent and span the column
   space, as the computation above confirms. Column rank = number of pivots.
3. Both counts are the pivot count of the same RREF. Therefore they are equal.

The subtlety that makes this worth proving rather than asserting: the row space
basis comes from the **reduced** matrix and the column space basis comes from the
**original** one. They are different sets in different ambient spaces, which is
why the equality of their dimensions is a theorem and not an identity.

</details>

**[ ] Exercise 3 — rank as degrees of freedom.** For each system, report the rank,
the number of free unknowns, and whether the solution is unique. Then explain in
one sentence why the last case is not unique even though the matrix is square.

1. 3 equations, 3 unknowns, rank 3
2. 4 equations, 3 unknowns, one redundant
3. 2 equations, 3 unknowns, rank 2
4. 3 equations, 3 unknowns, rank 2

**Challenge.** A dataset has 3 columns and rank 2. A linear model
`score = w₁·hours + w₂·sleep + w₃·score` is fitted by least squares. Explain, using
the null space, why the fitted coefficients are not unique, and what that means
for the prediction.

<details>
<summary>Solution</summary>

```python
TOL = 1e-9


# ---------------------------------------------------------------- helpers
def shape(M):
    return len(M), len(M[0])


def zeros(rows, cols):
    return [[0.0] * cols for _ in range(rows)]


def rref(A, tol=TOL):
    """Reduced row echelon form of A, plus the pivot column indices."""
    M = [list(row) for row in A]
    rows, cols = len(M), len(M[0])
    pivot_row = 0
    pivots = []
    for col in range(cols):
        best = None
        for r in range(pivot_row, rows):
            if abs(M[r][col]) > tol:
                best = r
                break
        if best is None:
            continue
        M[pivot_row], M[best] = M[best], M[pivot_row]
        p = M[pivot_row][col]
        M[pivot_row] = [v / p for v in M[pivot_row]]
        for r in range(rows):
            if r != pivot_row and M[r][col] != 0.0:
                f = M[r][col]
                M[r] = [M[r][c] - f * M[pivot_row][c] for c in range(cols)]
        pivots.append(col)
        pivot_row += 1
    M = [[v + 0.0 for v in row] for row in M]
    return M, pivots


def rank(A, tol=TOL):
    _, pivots = rref(A, tol)
    return len(pivots)


def solve_consistent(A, b, tol=TOL):
    """Reduce [A | b] and classify the system as in lesson 32."""
    rows, cols = len(A), len(A[0])
    M = [list(A[i]) + [b[i]] for i in range(rows)]
    pivot_row = 0
    pivots = []
    for col in range(cols):
        best = None
        for r in range(pivot_row, rows):
            if abs(M[r][col]) > tol:
                best = r
                break
        if best is None:
            continue
        M[pivot_row], M[best] = M[best], M[pivot_row]
        p = M[pivot_row][col]
        M[pivot_row] = [v / p for v in M[pivot_row]]
        for r in range(rows):
            if r != pivot_row and M[r][col] != 0.0:
                f = M[r][col]
                M[r] = [M[r][c] - f * M[pivot_row][c] for c in range(cols + 1)]
        pivots.append(col)
        pivot_row += 1
    for i in range(pivot_row, rows):
        if any(abs(M[i][j]) > tol for j in range(cols)) or abs(M[i][cols]) > tol:
            return "no solution", M, pivots
    if len(pivots) < cols:
        return "infinitely many", M, pivots
    x = [0.0] * cols
    for i, pc in enumerate(pivots):
        x[pc] = M[i][cols]
    return "unique", M, pivots


def null_space(A, tol=TOL):
    M, pivots = rref(A, tol)
    cols = shape(A)[1]
    free = [c for c in range(cols) if c not in pivots]
    basis = []
    for fc in free:
        v = [0.0] * cols
        v[fc] = 1.0
        for i, pc in enumerate(pivots):
            v[pc] = -M[i][fc]
        basis.append(v)
    return basis


cases = [
    ("3 eq, 3 unknowns, full rank",
     [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 10.0]], [10.0, 20.0, 31.0]),
    ("4 eq, 3 unknowns, one redundant",
     [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 10.0], [5.0, 7.0, 9.0]],
     [10.0, 20.0, 31.0, 30.0]),
    ("2 eq, 3 unknowns, rank 2",
     [[1.0, 2.0, 3.0], [2.0, 1.0, 0.0]], [6.0, 2.0]),
    ("3 eq, 3 unknowns, rank 2",
     [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [5.0, 7.0, 9.0]], [1.0, 2.0, 3.0]),
]

print(f"  {'system':38s} {'rank':>4} {'free':>4}  outcome")
for label, A, b in cases:
    r = rank(A)
    kind, M, pivots = solve_consistent(A, b)
    free = len(A[0]) - len(pivots)
    print(f"  {label:38s} {r:>4} {free:>4}  {kind}")
print()
print("Read the 'free' column: it is unknowns minus rank in every case, and it")
print("is the number of free parameters in the solution set. Zero means a single")
print("point; one means a line; two means a plane.")
print()
print("The last case has 3 equations and rank 2, so there is one free unknown")
print("even though the system looks square. A square matrix is not the same as a")
print("full-rank matrix, and rank is what tells them apart.")
print()
print("The second case is worth dwelling on: four equations, three unknowns, and")
print("still a unique solution. One equation is redundant, so it constrains")
print("nothing new. Over-determined is fine; over-determined and inconsistent is")
print("not, and that distinction lives in b, not in A.")

print()
print("=== Challenge: why the coefficients are not unique ===")
# score = 10*hours + 20*attendance, so the design matrix has rank 2 in 3 columns.
hours = [3.0, 5.0, 2.0, 4.0, 6.0]
attendance = [0.90, 0.80, 0.60, 0.95, 0.85]
score = [10.0 * h + 20.0 * a for h, a in zip(hours, attendance)]
X = [[h, a, s] for h, a, s in zip(hours, attendance, score)]
print("design matrix, rows are observations, columns are the three features:")
for row in X:
    print(f"  {row}")
print(f"rank = {rank(X)} of 3 columns")
ns = null_space(X)
print(f"null space basis = {ns}")
v = ns[0]
print()
print(f"The vector v = {v} satisfies X v = 0, meaning")
for i, row in enumerate(X):
    lhs = sum(row[j] * v[j] for j in range(3))
    print(f"  row {i}: {row[0]}*{v[0]} + {row[1]}*{v[1]} + {row[2]}*{v[2]} = {lhs}")
print()
print("So if w is any coefficient vector that fits the data, then w + t*v fits")
print("it too, for any t. The predictions are identical, because")
print("(X (w + t*v))[i] = (X w)[i] + t*(X v)[i] = (X w)[i].")
print()
print("That is the practical meaning: rank deficiency makes the coefficients")
print("meaningless in isolation while leaving the predictions perfectly fine.")
print("Any regulariser, or any choice of pivot columns, picks one point of the")
print("line, and different choices give different-looking models with identical")
print("behaviour on any data whose score obeys the same relation.")
```

Output:

```
  system                                 rank free  outcome
  3 eq, 3 unknowns, full rank               3    0  unique
  4 eq, 3 unknowns, one redundant           3    0  unique
  2 eq, 3 unknowns, rank 2                  2    1  infinitely many
  3 eq, 3 unknowns, rank 2                  2    1  infinitely many

=== Challenge: why the coefficients are not unique ===
design matrix, rows are observations, columns are the three features:
  [3.0, 0.9, 48.0]
  [5.0, 0.8, 66.0]
  [2.0, 0.6, 32.0]
  [4.0, 0.95, 59.0]
  [6.0, 0.85, 77.0]
rank = 2 of 3 columns
null space basis = [[-10.0, -20.0, 1.0]]
```

The vector `v = [-10, -20, 1]` says that raising the hours coefficient by `−10`
and the attendance coefficient by `−20` while raising the score coefficient by
`1` leaves every prediction unchanged, because the score column is exactly
`10·hours + 20·attendance`. This is the reason L2 regularisation ([lesson
100](../part08_optimization/100_convexity.md)) always produces a *unique*
answer to an under-determined fit: it adds a term that is strictly convex in
`w`, and a strictly convex objective has a unique minimiser. The data does not
pick a point on the line; the penalty does.

</details>

## Summary

- A **basis** is a list that spans a set and is independent. The **dimension** is
  the number of vectors in any basis, and every basis of the same set has the same
  length.
- The **span** is the set; the basis is one description of it. Bases are not
  unique, and the rank of a matrix is the dimension of the span of its rows or
  columns.
- **Row rank = column rank** is the theorem that makes rank well defined. Both
  equal the pivot count of any row echelon form. The row space basis comes from
  the *reduced* matrix; the column space basis comes from the *original* one.
- **Rank-nullity**: `rank(A) + dim ker(A) = n`. With `m` rows,
  `rank(A) + dim ker(Aᵀ) = m`. One number, `r`, fixes all four dimensions.
- The **four fundamental subspaces** are found by one row reduction: column space
  (pivot columns of `A`), row space (nonzero RREF rows), null space (free
  columns), left null space (free columns of `rref(Aᵀ)`).
- A system of rank `r` with `n` unknowns has `n − r` free parameters. For a square
  system, `r = n` is the unique-solution condition, which is lesson 33's `det ≠ 0`.
- Rank counts independent directions, so adding a redundant column is free and
  dropping it is free. That is the arithmetic behind feature selection and PCA.
- Rank is always "at some tolerance". On noisy data, report singular values rather
  than a bare rank, and say what threshold you used.

## Next

[35 — Linear Transformations and Kernels](35_linear_transformations_and_kernels.md)
puts a name on the machinery: a matrix applied to a vector *is* a linear
transformation. That lesson makes the four subspaces concrete, defines kernel and
image, and proves rank-nullity in its full geometric form, which is the
conceptual core of the whole part.
