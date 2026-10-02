# 33 — Determinant and Inverse

**Part**: part03_linear_algebra · **Prerequisites**: 32 · **Time**: 35 min

---

## In Plain Words

Every square grid of numbers has one extra number attached to it, computed from
all its entries, and that single number decides whether the grid can be undone.
If the number is not zero, there is exactly one grid that undoes it. If the
number is zero, no grid undoes it — the information has been lost, and it is
lost in a structural, identifiable way rather than a numerical accident.

The number also means something geometric, and that meaning is why it is worth
learning. Apply the grid to a shape, and the shape comes out stretched or
squashed by a definite factor, and possibly turned over like a glove. The
absolute value of the number is how much the size changed. The sign records
whether the shape ended up the same way round or reversed.

The reason programmers meet this constant is efficiency and honesty. One number
tells you whether a system has an answer, and computing it by row reduction costs
the same cubic time as solving the system itself — so it is a diagnostic, not a
speedup. The famous closed-form formulas for the inverse are beautiful and
almost never what you should run.

## Why Computer Science Cares

- **Singularity detection, everywhere.** `numpy.linalg.solve` raises
  `LinAlgError: Singular matrix` when LU elimination cannot find a pivot. That
  is `det(A) = 0` discovered computationally rather than symbolically. Every
  time a regression design matrix turns out to be rank-deficient — collinear
  features, a duplicated column, more features than rows — this is the fact that
  fires.
- **`numpy.linalg.slogdet`.** Underflow in `det` gives false zeros on large
  sparse matrices, which is common in graph and probabilistic work. `slogdet`
  returns `(sign, log|det|)` and is the correct routine whenever the determinant
  enters multiplicatively.
- **Collinearity checks in regression.** If two features are exact linear
  combinations of the others, `XᵀX` is singular and the normal equations in
  [lesson 38](38_orthogonality_and_least_squares.md)
  cannot be inverted. The residual sum of squares has a flat direction.
- **Graphics.** An affine transform matrix with determinant 0 collapses
  geometry onto a lower-dimensional subspace — a projection matrix has
  `det = 0` by design, and no inverse transform exists, which is exactly why
  you cannot un-project. See
  [lesson 91](../part07_geometry_graphics/91_transformations_graphics.md).
- **Interview questions.** "How do you check if a matrix is invertible?",
  "compute the inverse of a 3×3 without a library", "what does a negative
  determinant mean?", and "why is Cramer's rule not used in practice?" are all
  standard, and this lesson answers every one.

## The Formal Version

Symbols follow [SYMBOLS.md](../SYMBOLS.md). Let `A` be an `n × n` matrix over a
field `F`, written `A = (a_ij)`.

**Definition.** The **determinant** of a `1 × 1` matrix is `det([a]) = a`.

**Definition.** For `n ≥ 2`, `M_ij` is the **minor** of entry `(i, j)`: the
`(n−1) × (n−1)` matrix obtained by deleting row `i` and column `j`. The
**cofactor** is

    C_ij = (-1)^(i+j) · det(M_ij)

The sign pattern `(-1)^(i+j)` is the checkerboard

    + - + - ...        (i+j even  →  +)
    - + - + ...
    + - + - ...

**Theorem (Cofactor expansion).** `det(A) = Σ_{j=1..n} a_1j · C_1j` — expansion
along **any** row, and equally along any column. `C_1j = det(M_1j)` for
`n = 2`, giving the familiar `ad − bc`.

**Explanation.** Expanding along row `1` and along row `k` are two routes to the
same number. This is the one place where the definition is agreed by everyone and
each recursive call shrinks the problem, so it is safe to write down and
unpleasant to compute.

**Definition (Leibniz formula).** The equivalent non-recursive definition, with divisible
`det(A) = Σ_{σ ∈ S_n} sgn(σ) · Π_{i=1..n} a_{i,σ(i)}`, where `S_n` is the set of all
permutations of `{1, …, n}` and `sgn(σ) = (-1)^{#inversions}` counts how many
pairs `i < j` have `σ(i) > σ(j)`.

**Explanation.** This is the definition that makes the *meaning* obvious. Take
the unit square in `ℝ²` with corners `(0,0), (1,0), (1,1), (0,1)`. `A` sends each
corner `v` to `Av`. The signed area of the resulting parallelogram is exactly the
sum above: the two positive permutations are the counterclockwise orders and the
two negative ones the clockwise orders. Each product `a_1σ(1) · a_2σ(2)` is twice
the signed area of one of the two triangles the origin and the images cut out, and
`n!` of them tile the whole solid. For `n = 3`, the volume of the parallelepiped
spanned by the columns of `A` is `|det(A)|`.

**Theorem (Geometric meaning).** For `A ∈ ℝ^{n×n}` and any measurable `S ⊆ ℝⁿ`:

    volume(A S) = |det(A)| · volume(S)

`det(A) > 0` means `A` preserves orientation; `det(A) < 0` means it reverses it;
`det(A) = 0` means `AS` has volume zero — `A` collapses space onto a proper
subspace.

**Explanation.** `det(A) > 0` means the images of the standard basis vectors,
taken in their natural order, still wind the same way around as the basis
itself; `det(A) < 0` means one transposition is needed to restore the winding.
`det(A) = 0` means one column is a combination of the others, so the parallelepiped
is flat.

**Theorem (Row and column properties).** For `A`, `B` square of the same size and
`c ∈ F`:

1. `det(cA) = cⁿ det(A)`
2. `det(A + B)` is **not** `det(A) + det(B)` — the determinant is not linear
3. `det(AB) = det(A) det(B)`
4. `det(Aᵀ) = det(A)`
5. `det(A⁻¹) = 1/det(A)` (when `A` is invertible)
6. swapping two rows of `A` negates `det(A)`; adding a multiple of one row to
   another leaves it unchanged; multiplying one row by `c ≠ 0` multiplies it by `c`
7. `det(U) = Π_i u_ii` for upper-triangular `U`, and likewise for lower-triangular

**Explanation.** (1) holds because scaling a row scales the volume, and `n` rows
get scaled. (2) fails because cross terms appear; `det(A + B) = det(A) + det(B)`
holds only when the rows of `A` and `B` are disjointly supported, which almost
never happens. (3) is composition of volume scalings: the scale factor of `AB` is
the product. (4) comes from the Leibniz formula, since transposing swaps `a_i_j`
for `a_j_i`, which maps even permutations to even and odd to odd, preserving
every sign. (6) is the definition: a transposition is exactly one sign flip in
the Leibniz sum, and a row addition is `A → A + c · (stuff)` whose extra
contribution is a determinant with two equal rows, hence zero. (7) is (6) applied
repeatedly: the off-diagonal cofactors of a triangular matrix vanish by induction.

**Theorem (Invertibility criterion).** `A` is invertible if and only if
`det(A) ≠ 0`.

**Explanation.** If `A` is invertible, `A⁻¹A = I` and `det(A⁻¹)det(A) = det(I) = 1`,
so `det(A) ≠ 0`. Conversely, if `det(A) ≠ 0`, the adjugate identity below gives
`A⁻¹` explicitly. In elimination terms, `det(A) ≠ 0` means the elimination never
runs out of pivots, and then the solution is unique by
[lesson 32](32_linear_systems_gaussian_elimination.md).

**Definition.** The **cofactor matrix** is `C = (C_ij)`. The **adjugate**
(classical adjoint) is `adj(A) = Cᵀ`. Note these are *different matrices* — the
transpose is not optional.

**Theorem (Adjugate identity).** `A · adj(A) = adj(A) · A = det(A) · I_n`, for
**every** square `A`, including singular ones.

**Explanation.** Expand `(A adj(A))_ij = Σ_k a_ik adj(A)_kj = Σ_k a_ik C_jk`
along row `j` of the "matrix" whose `jk` entry is `a_ik`. For `i = j` this is
cofactor expansion of row `i` of `A`, giving `det(A)`. For `i ≠ j` it is
cofactor expansion of row `j` of `A` with row `i` moved to the top, which costs
`(-1)^{i+j}`, cancelling the `(-1)^{i+j}` in the cofactor, and the matrix has
two equal rows so the determinant is zero.

**Theorem (Inverse formula).** If `det(A) ≠ 0` then

    A⁻¹ = adj(A) / det(A)

and conversely. **The precondition `det(A) ≠ 0` is not decorative** — it is
division by `det(A)`, and `adj(A)` is still perfectly well defined when
`det(A) = 0`.

**Explanation.** Divide the adjugate identity by `det(A)`. The identity itself
does not need `det(A) ≠ 0`, but the *conclusion* does: when `det(A) = 0` it reads
`A adj(A) = 0`, which is a true statement about nothing. In fact for `n ≥ 2`,
`det(A) = 0` forces every row of `adj(A)` to be zero, so `adj(A)` is singular too.

**Theorem (Cramer's rule).** If `det(A) ≠ 0` and `Ax = b`, then `x_i = det(A_i)/det(A)`,
where `A_i` is `A` with column `i` replaced by `b`.

**Explanation.** `A_i` is the matrix you'd get from the adjugate identity with `A`
replaced by the augmented matrix, and it is what makes the formula work. It needs
`n + 1` determinants, so it is a device for pencil-and-paper work on 2×2 and 3×3
systems and nothing else.

**Theorem (Cost).** Cofactor expansion is `Θ(n!)` — it forks into `n` problems of
size `n−1`, so `T(n) = n·T(n−1) + Θ(n²)`. Computing the determinant by LU
elimination is `Θ(n³)`. Forming `adj(A)` directly is `Θ(n⁴)` (one `O(n³)`
cofactor per entry), so even the closed form is not the fast route.

**Explanation.** `n!` vs `n³` at `n = 10` is `3,628,800` vs `1,000`. And an LU
factorisation already gives you the determinant for free as the pivot product, so
a library hands you the factors and never a determinant.

**Corollary (What `det(A) = 0` does *not* say).** `det(A) = 0` means "not
exactly one solution". It does **not** mean "no solution", and it does not mean
"infinitely many" — both occur, and telling them apart requires looking at `b`,
which the determinant knows nothing about.

**Explanation.** For a singular `A` the system `Ax = b` is consistent exactly when
`b ∈ col(A)`, and then has infinitely many solutions (since `ker(A) ≠ {0}`);
otherwise it has none. `b` appears in no determinant formula.

## Worked Example

One matrix, carried all the way:

    A = | 2  1  3 |
        | 1  4  1 |
        | 0  2  1 |

**Step 1: determinant by cofactor expansion along row 0.** The signs down the first
row are `+ − +`, from `(-1)^{0+j}`:

    det(A) = +2·det|4 1| + (-1)·1·det|1 1| + (+1)·3·det|1 4|
                  |2 1|            |0 1|            |0 2|

Compute each `2 × 2` by the `ad − bc` rule:

- first minor: `4·1 − 1·2 = 4 − 2 = 2`, so the term is `(+1)·2·2 = +4`
- second minor: `1·1 − 1·0 = 1 − 0 = 1`, so the term is `(−1)·1·1 = −1`
- third minor: `1·2 − 4·0 = 2 − 0 = 2`, so the term is `(+1)·3·2 = +6`

Total: `+4 − 1 + 6 = 9`. So `det(A) = 9`, and by the theorem `A` is invertible.

**Step 2: confirm with elimination**, since that is the route you would actually
take. Column 0 holds `[2, 1, 0]`; the largest magnitude is `2`, already at the
top, so no swap and the sign stays positive.

    R_1 <- R_1 - (1/2) R_0   gives  [1, 4, 1] - [1, 0.5, 1.5] = [0, 3.5, -0.5]
    R_2 <- R_2 - (0/2) R_0   gives  [0, 2, 1] - [0, 0, 0]     = [0, 2, 1]

    now  | 2   1    3  |
         | 0   3.5 -0.5|
         | 0   2    1  |

Clear column 1 using row 1: factor `2/3.5 = 0.5714`:

    R_2 <- R_2 - 0.5714 R_1   gives  [0, 2, 1] - [0, 2, -0.2857] = [0, 0, 1.2857]

Now `U` is upper triangular, so `det(A) = 2 · 3.5 · 1.2857 = 9`, and the sign
factor is `(-1)^0 = +1` because no row was swapped. Same answer. The exact value
of the last pivot is `9/7 ≈ 1.2857`, so the product is exactly `2 · 7/2 · 9/7 = 9`.

**Step 3: the cofactor matrix.** Nine `2 × 2` determinants, one per entry:

    C[0][0] = +det[[4,1],[2,1]] = 4 - 2 = 2
    C[0][1] = -det[[1,1],[0,1]] = -(1) = -1
    C[0][2] = +det[[1,4],[0,2]] = 2      = 2
    C[1][0] = -det[[1,3],[2,1]] = -(1-6) = 5
    C[1][1] = +det[[2,3],[0,1]] = 2      = 2
    C[1][2] = -det[[2,1],[0,2]] = -(4)   = -4
    C[2][0] = +det[[1,3],[4,1]] = 1-12   = -11
    C[2][1] = -det[[2,3],[1,1]] = -(2-3) = 1
    C[2][2] = +det[[2,1],[1,4]] = 8-1    = 7

So

    C = |  2  -1   2 |      and      adj(A) = Cᵀ = |  2   5  -11 |
        |  5   2  -4 |                        | -1   2    1 |
        | -11  1   7 |                        |  2  -4    7 |

Sanity check against Step 1: the first row of `C` times `A`'s first row gives
`2·2 + (−1)·1 + 2·3 = 4 − 1 + 6 = 9` ✓ — that is `det(A)` again, which is what
cofactor expansion means.

**Step 4: the inverse.** Divide every entry of `adj(A)` by `9`:

    A⁻¹ = |  2/9    5/9  -11/9 |  =  |  0.222222  0.555556 -1.222222 |
          | -1/9    2/9    1/9 |     | -0.111111  0.222222  0.111111 |
          |  2/9   -4/9    7/9 |     |  0.222222 -0.444444  0.777778 |

**Step 5: verify.** `A · A⁻¹` should be `I`. Row 0 of the product:

    2·(2/9) + 1·(-1/9) + 3·(2/9)  = (4 - 1 + 6)/9  = 9/9  = 1     ✓
    2·(5/9) + 1·(2/9)  + 3·(-4/9) = (10 + 2 - 12)/9 = 0/9  = 0     ✓
    2·(-11/9) + 1·(1/9) + 3·(7/9) = (-22 + 1 + 21)/9 = 0/9 = 0     ✓

The remaining six entries work out the same way. The code below prints all nine.

**Step 6: use it.** Solve `Ax = b` with `b = (5, 7, 4)`:

    x = A⁻¹ b = (2/9·5 + 5/9·7 - 11/9·4,
                 -1/9·5 + 2/9·7 + 1/9·4,
                  2/9·5 - 4/9·7 + 7/9·4)
      = ((10 + 35 - 44)/9, (-5 + 14 + 4)/9, (10 - 28 + 28)/9)
      = (1/9, 13/9, 10/9)
      ≈ (0.111111, 1.444444, 1.111111)

Cramer's rule gives the same three numbers from three separate determinants, and
substituting back gives a residual of exactly `(0, 0, 0)`.

**Step 7: the negative case, so the sign is not mysterious.** Take
`G = [[1, 2], [2, 1]]`. Then `det(G) = 1·1 − 2·2 = −3`. The unit square has area
`1`; the images of its corners are `(0,0), (1,2), (3,3), (2,1)`, and the shoelace
formula gives signed area `−3`. Absolute value `3` — the area tripled. Sign `−` —
the corners came out clockwise where they started counterclockwise, so the map
turned the square over. That is the entire content of the sign.

## Runnable Code

### Two definitions, and why only one of them is usable

```python
from itertools import permutations
from math import factorial


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


def matmul(A, B):
    rows_a, cols_a = shape(A)
    rows_b, cols_b = shape(B)
    if cols_a != rows_b:
        raise ValueError(f"cannot multiply {rows_a}x{cols_a} by {rows_b}x{cols_b}")
    return [[sum(A[i][k] * B[k][j] for k in range(cols_a)) for j in range(cols_b)]
            for i in range(rows_a)]


def matvec(M, v):
    return [sum(row[j] * v[j] for j in range(len(v))) for row in M]


def print_matrix(label, M, width=9, prec=3):
    print(label)
    for row in M:
        print("    " + " ".join(f"{x:{width}.{prec}f}" for x in row))
    print()


# ---------------------------------------------------------------- definitions
def permutation_sign(perm):
    """+1 for an even permutation, -1 for an odd one.

    Count inversions: pairs i < j with perm[i] > perm[j]. A single inversion
    means the permutation is one transposition, which flips orientation; an even
    number of them cancels out.
    """
    inversions = sum(
        1
        for i in range(len(perm))
        for j in range(i + 1, len(perm))
        if perm[i] > perm[j]
    )
    return -1 if inversions % 2 else 1


def det_leibniz(A):
    """The defining formula: one signed term for every permutation of the columns."""
    n = len(A)
    total = 0.0
    for perm in permutations(range(n)):
        product = 1.0
        for i in range(n):
            product *= A[i][perm[i]]
        total += permutation_sign(perm) * product
    return total


def minor(M, i, j):
    """The (n-1) x (n-1) matrix left after deleting row i and column j."""
    return [[M[r][c] for c in range(len(M[0])) if c != j]
            for r in range(len(M)) if r != i]


def det_cofactor(A):
    """Expand along the first row: det(A) = sum_j (-1)^j a_0j det(minor_0j).

    Base cases: a 1x1 determinant is its single entry, and the 2x2 rule
    ad - bc is the one place the recursion stops.
    """
    n = len(A)
    if n == 1:
        return A[0][0]
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    total = 0.0
    for j in range(n):
        total += (-1) ** j * A[0][j] * det_cofactor(minor(A, 0, j))
    return total


# ---------------------------------------------------------------- the example
A = [[2.0, 1.0, 3.0],
     [1.0, 4.0, 1.0],
     [0.0, 2.0, 1.0]]

print("=== One 3x3 matrix, two definitions, one answer ===")
print_matrix("A =", A)
cof = det_cofactor(A)
leib = det_leibniz(A)
print(f"det by cofactor expansion along row 0 : {cof:g}")
print(f"det by the Leibniz permutation sum   : {leib:g}")
print(f"they agree: {abs(cof - leib) < 1e-12}")

print()
print("=== The cofactor expansion, term by term ===")
# The signs down the first row of a 3x3 are + - +, from the checkerboard (-1)^(0+j).
signs = [(-1) ** j for j in range(3)]
print(f"signs for row 0 of a 3x3: {signs}")
terms = []
for j in range(3):
    m = minor(A, 0, j)
    d = det_cofactor(m)
    term = signs[j] * A[0][j] * d
    terms.append(term)
    print(f"  j={j}: a_0j = {A[0][j]:g}, minor = {m}, "
          f"det(minor) = {d:g}, term = ({signs[j]:+d})*{A[0][j]:g}*{d:g} = {term:g}")
print(f"  det(A) = {' '.join(f'{t:+g}' for t in terms)} = {sum(terms):g}")

print()
print("=== The Leibniz sum, all 3! = 6 permutations ===")
print(f"{'perm':>10} {'sign':>5} {'product':>10} {'signed term':>12}")
total = 0.0
for perm in permutations(range(3)):
    product = 1.0
    for i in range(3):
        product *= A[i][perm[i]]
    s = permutation_sign(perm)
    total += s * product
    print(f"{str(perm):>10} {s:>+5d} {product:>10.1f} {s * product:>12.1f}")
print(f"sum of the six signed terms = {total:g}")

print()
print("=== Why nobody computes determinants with the Leibniz formula ===")
# n! terms. Elimination is O(n^3). The gap opens immediately and then explodes.
print(f"{'n':>4} {'n! terms (Leibniz)':>22} {'n^3 ops (elimination)':>22}")
for n in (3, 5, 8, 10, 20):
    print(f"{n:>4} {factorial(n):>22,} {n ** 3:>22,}")

print()
print("=== Small cases, checked against the rules ===")
two = [[1.0, 2.0], [3.0, 4.0]]
print(f"det([[1, 2], [3, 4]]) Leibniz   = {det_leibniz(two):g}")
print(f"det([[1, 2], [3, 4]]) cofactor  = {det_cofactor(two):g}")
print("  by the 2x2 rule ad - bc = 1*4 - 2*3 = 4 - 6 = -2")
print(f"det of the 1x1 [[7.5]]          = {det_cofactor([[7.5]]):g}")
print(f"det of the 4x4 identity         = {det_cofactor(identity(4)):g}  (1, all diagonal 1s)")
```

### Determinant by elimination, the properties, and the geometry

```python
# ---------------------------------------------------------------- helpers
def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def transpose(M):
    rows, cols = len(M), len(M[0])
    return [[M[i][j] for i in range(rows)] for j in range(cols)]


def matmul(A, B):
    rows_a, cols_a = len(A), len(A[0])
    rows_b, cols_b = len(B), len(B[0])
    if cols_a != rows_b:
        raise ValueError(f"cannot multiply {rows_a}x{cols_a} by {rows_b}x{cols_b}")
    return [[sum(A[i][k] * B[k][j] for k in range(cols_a)) for j in range(cols_b)]
            for i in range(rows_a)]


def matvec(M, v):
    return [sum(row[j] * v[j] for j in range(len(v))) for row in M]


def print_matrix(label, M, width=9, prec=3):
    print(label)
    for row in M:
        print("    " + " ".join(f"{x:{width}.{prec}f}" for x in row))
    print()


def det_cofactor(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    total = 0.0
    for j in range(n):
        m = [[A[r][c] for c in range(n) if c != j] for r in range(1, n)]
        total += (-1) ** j * A[0][j] * det_cofactor(m)
    return total


def determinant_lu(A, tol=1e-12):
    """det(A) from Gaussian elimination with partial pivoting.

    Three row facts, all inherited from the determinant definition:
      adding a multiple of one row to another leaves the determinant unchanged;
      multiplying a row by c multiplies the determinant by c;
      swapping two rows negates the determinant.

    Elimination never uses the second of those, so when it finishes
    det(A) = (-1)^(number of swaps) * product of the pivots.
    """
    M = [list(row) for row in A]
    n = len(M)
    det = 1.0
    swaps = 0

    for col in range(n):
        best = max(range(col, n), key=lambda r: abs(M[r][col]))   # partial pivoting
        if abs(M[best][col]) <= tol:
            return 0.0                       # no pivot available: det = 0
        if best != col:
            M[col], M[best] = M[best], M[col]
            swaps += 1

        det *= M[col][col]                   # the pivot, now the only nonzero in its column
        for r in range(col + 1, n):
            factor = M[r][col] / M[col][col]
            if factor:
                M[r] = [M[r][c] - factor * M[col][c] for c in range(n)]

    return -det if swaps % 2 else det


# ================================================================ worked example
A = [[2.0, 1.0, 3.0],
     [1.0, 4.0, 1.0],
     [0.0, 2.0, 1.0]]

print("=== Determinant by elimination, step by step ===")
print("Column 0 holds [2, 1, 0]; the largest magnitude is 2, already at the top,")
print("so no swap is needed and the sign is untouched.")
print()
print_matrix("start", A)

M = [list(row) for row in A]
f1 = M[1][0] / M[0][0]
f2 = M[2][0] / M[0][0]
M[1] = [M[1][c] - f1 * M[0][c] for c in range(3)]
M[2] = [M[2][c] - f2 * M[0][c] for c in range(3)]
print(f"R_1 <- R_1 - {f1:g} R_0      R_2 <- R_2 - {f2:g} R_0")
print("Both are rule (i): adding a multiple of one row to another. det unchanged.")
print_matrix("after clearing column 0", M)

f3 = M[2][1] / M[1][1]
M[2] = [M[2][c] - f3 * M[1][c] for c in range(3)]
print(f"R_2 <- R_2 - {f3:.4f} R_1")
print_matrix("upper triangular", M)

p = [M[0][0], M[1][1], M[2][2]]
sign = (-1) ** 0
print(f"pivots        = {[round(x, 4) for x in p]}")
print(f"product       = {p[0]:g} * {p[1]:g} * {p[2]:.4f} = {p[0] * p[1] * p[2]:g}")
print("sign          = (-1)^0 = +1, because no row was swapped")
print(f"det(A)        = {sign:+d} * {p[0] * p[1] * p[2]:g} = "
      f"{sign * p[0] * p[1] * p[2]:g}")
print()
print(f"determinant_lu(A)       = {determinant_lu(A):g}")
print(f"determinant_cofactor(A) = {det_cofactor(A):g}")
print("Both say 9. The elimination version is O(n^3); the cofactor version is")
print("O(n!) because each expansion forks into n subproblems of size n-1.")

print()
print("=== The three row properties, one example each ===")
B = [list(row) for row in A]
B[0], B[1] = B[1], B[0]
print(f"(iii) swap R_0 and R_1:  det = {determinant_lu(B):g}  "
      f"(was {determinant_lu(A):g}, so the sign flipped and only the sign flipped)")
C = [[3.0 * x for x in row] for row in A]
print(f"(ii)  multiply every entry by 3 (scale every row by 3): "
      f"det = {determinant_lu(C):g}")
print(f"      and 3^3 * det(A) = {3 ** 3} * {determinant_lu(A):g} = "
      f"{3 ** 3 * determinant_lu(A):g}   <- n row scalings give a factor of c^n")

print()
print("=== A singular matrix: no pivot, det = 0 ===")
S = [[1.0, 2.0],
     [2.0, 4.0]]
print_matrix("S =", S, prec=1)
print(f"determinant_lu(S)       = {determinant_lu(S):g}")
print(f"determinant_cofactor(S) = {det_cofactor(S):g}")
print("Elimination clears column 0, then finds column 1 already zero below the")
print("pivot position, so there is no pivot left to multiply. That failure IS the")
print("statement det(S) = 0. Row 1 of S is [2, 4], which is exactly 2 * [1, 2],")
print("so the two rows depend on each other - and row dependence is what")
print("det = 0 says for a 2x2.")

print()
print("=== det(AB) = det(A) det(B) ===")
P = [[1.0, 2.0],
     [3.0, 4.0]]                 # det = 1*4 - 2*3 = -2
Q = [[5.0, 6.0],
     [7.0, 8.0]]                 # det = 5*8 - 6*7 = -2
PQ = matmul(P, Q)
print(f"det(P) = {determinant_lu(P):g},  det(Q) = {determinant_lu(Q):g},  "
      f"product = {determinant_lu(P) * determinant_lu(Q):g}")
print(f"P Q = {PQ}")
print(f"det(P Q) = {determinant_lu(PQ):g}")
print(f"identity holds: {abs(determinant_lu(PQ) - determinant_lu(P) * determinant_lu(Q)) < 1e-9}")
print("Note that det(P) det(Q) = (+4) even though both factors are negative.")
print("Multiplicativity is what makes the determinant a genuine scale factor:")
print("scaling by det(A) and then by det(B) scales by the product, as it must.")

print()
print("=== det(A^T) = det(A) ===")
PT = transpose(P)
print(f"P^T = {PT}")
print(f"det(P^T) = {determinant_lu(PT):g},  det(P) = {determinant_lu(P):g}")
print("The Leibniz formula for A^T permutes the same indices in the same order,")
print("only reading the product off a different matrix, and a_i_j -> a_j_i pairs")
print("even permutations with even and odd with odd, so every sign survives.")

print()
print("=== Triangular determinants are the diagonal product ===")
U = [[2.0, 3.0, 4.0],
     [0.0, 5.0, 6.0],
     [0.0, 0.0, 7.0]]
L = [[1.0, 0.0, 0.0],
     [8.0, 2.0, 0.0],
     [9.0, 9.0, 3.0]]
print_matrix("U (upper triangular)", U, prec=1)
print(f"det(U) by elimination   = {determinant_lu(U):g}")
print(f"det(U) as 2*5*7         = {2 * 5 * 7:g}")
print_matrix("L (lower triangular)", L, prec=1)
print(f"det(L) by elimination   = {determinant_lu(L):g}")
print(f"det(L) as 1*2*3         = {1 * 2 * 3:g}")
print("Every cofactor off the diagonal of a triangular matrix is the determinant")
print("of a smaller triangular matrix with a zero row, so the recursion stops at")
print("once. This is why an LU solver can never be asked for a determinant.")

print()
print("=== What the number means: a 2x2 that scales and flips the unit square ===")
# The unit square has corners (0,0), (1,0), (1,1), (0,1) and area 1. Apply a 2x2
# matrix to each corner and measure the resulting quadrilateral with the shoelace
# formula. The answer is |det| for the area and det itself for the orientation.
def shoelace_area(points):
    """Signed area of a polygon given its vertices in order. Counterclockwise is positive."""
    total = 0.0
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        total += x1 * y2 - x2 * y1
    return total / 2.0


corners = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
print(f"unit square corners {corners}, signed area {shoelace_area(corners):g}")

for name, G in [
    ("G1 = [[2, 0], [0, 3]]  (stretch x2, y3)", [[2.0, 0.0], [0.0, 3.0]]),
    ("G2 = [[1, 2], [2, 1]]  (det = -3)",     [[1.0, 2.0], [2.0, 1.0]]),
    ("G3 = [[1, 1], [1, 1]]  (det = 0)",      [[1.0, 1.0], [1.0, 1.0]]),
]:
    images = [(G[0][0] * x + G[0][1] * y, G[1][0] * x + G[1][1] * y)
              for x, y in corners]
    area = shoelace_area(images)
    d = determinant_lu(G)
    print()
    print(name)
    print(f"  images of the corners: {[(round(x, 3), round(y, 3)) for x, y in images]}")
    print(f"  shoelace signed area = {area:g}")
    print(f"  det(G)              = {d:g}")
    print(f"  |area| = |det|      : {abs(abs(area) - abs(d)) < 1e-9}")
    if d > 0:
        print("  det > 0: the corner order came out counterclockwise, so the")
        print("          orientation is preserved.")
    elif d < 0:
        print("  det < 0: the corner order came out clockwise - the map turned the")
        print("          square over. |det| is the area; the sign records the flip.")
    else:
        print("  det = 0: the four images are collinear, the square collapsed onto a")
        print("          line segment, and there is no area left at all.")
```

### The adjugate, the inverse, and why `det = 0` kills uniqueness

```python
# ---------------------------------------------------------------- helpers
def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def transpose(M):
    rows, cols = len(M), len(M[0])
    return [[M[i][j] for i in range(rows)] for j in range(cols)]


def matmul(A, B):
    rows_a, cols_a = len(A), len(A[0])
    rows_b, cols_b = len(B), len(B[0])
    if cols_a != rows_b:
        raise ValueError(f"cannot multiply {rows_a}x{cols_a} by {rows_b}x{cols_b}")
    return [[sum(A[i][k] * B[k][j] for k in range(cols_a)) for j in range(cols_b)]
            for i in range(rows_a)]


def matvec(M, v):
    return [sum(row[j] * v[j] for j in range(len(v))) for row in M]


def print_matrix(label, M, width=9, prec=3):
    print(label)
    for row in M:
        print("    " + " ".join(f"{x:{width}.{prec}f}" for x in row))
    print()


def det_cofactor(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    total = 0.0
    for j in range(n):
        m = [[A[r][c] for c in range(n) if c != j] for r in range(1, n)]
        total += (-1) ** j * A[0][j] * det_cofactor(m)
    return total


def cofactor_matrix(A):
    """C_ij = (-1)^(i+j) det(minor_ij). NOT the adjugate - that is the transpose."""
    n = len(A)
    C = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            m = [[A[r][c] for c in range(n) if c != j]
                 for r in range(n) if r != i]
            C[i][j] = (-1) ** (i + j) * det_cofactor(m)
    return C


def adjugate(A):
    """adj(A) = C^T, the cofactor matrix with rows and columns exchanged."""
    return transpose(cofactor_matrix(A))


def inverse_by_adjugate(A, tol=1e-12):
    """A^{-1} = adj(A) / det(A). Requires det(A) != 0."""
    d = det_cofactor(A)
    if abs(d) <= tol:
        raise ValueError("singular: det(A) = 0, so adj(A)/det(A) is undefined")
    adj = adjugate(A)
    n = len(A)
    return [[adj[i][j] / d for j in range(n)] for i in range(n)]


def solve_by_determinants(A, b, tol=1e-12):
    """Cramer's rule: x_i = det(A_i) / det(A), with column i replaced by b."""
    d = det_cofactor(A)
    if abs(d) <= tol:
        return None
    n = len(A)
    x = []
    for i in range(n):
        Ai = [[b[r] if c == i else A[r][c] for c in range(n)] for r in range(n)]
        x.append(det_cofactor(Ai) / d)
    return x


# ================================================================ the example
A = [[2.0, 1.0, 3.0],
     [1.0, 4.0, 1.0],
     [0.0, 2.0, 1.0]]

print("=== The cofactor matrix and the adjugate are different objects ===")
C = cofactor_matrix(A)
print_matrix("cofactor matrix C", C, prec=1)
print("Entry C[0][1]: delete row 0 and column 1, leaving [[1, 1], [0, 1]], whose")
print("determinant is 1*1 - 1*0 = 1, and the sign is (-1)^(0+1) = -1, so C[0][1] = -1.")
print()
adj = adjugate(A)
print_matrix("adj(A) = C^T", adj, prec=1)
print("The transpose really does swap things: C[0][1] = -1 but adj[0][1] = "
      f"{adj[0][1]:g}, because adj[0][1] = C[1][0].")
print("Getting this backwards is the single most common error in hand-written")
print("cofactor code, and it produces a matrix that looks plausible and is wrong.")

print()
print("=== adj(A) A = det(A) I, checked entry by entry ===")
d = det_cofactor(A)
adjA = matmul(adj, A)
print_matrix("adj(A) A", adjA, prec=1)
print(f"det(A) = {d:g}, so det(A) I is {d:g} down the diagonal and 0 elsewhere.")
print(f"adj(A) A == det(A) I : "
      f"{all(abs(adjA[i][j] - (d if i == j else 0.0)) < 1e-9 for i in range(3) for j in range(3))}")
print("Divide both sides by det(A) and you have A^{-1} = adj(A) / det(A).")

print()
print("=== The inverse, built from the adjugate ===")
Ainv = inverse_by_adjugate(A)
print_matrix("A^{-1} = adj(A)/9", Ainv, prec=6)
print()
print("Entry (0,0) by hand: adj(A)[0][0] = C[0][0] = det([[4,1],[2,1]]) = 4*1 - 1*2 = 2,")
print(f"so A^{{-1}}[0][0] = 2/9 = {2 / 9:.6f}")
print()
print("Entry (0,2) by hand, and this one exercises the transpose: adj(A)[0][2] is")
print("C[2][0], the cofactor of the ENTRY in row 2, column 0 - not row 0, column 2.")
print("Deleting row 2 and column 0 leaves [[1, 3], [4, 1]], determinant 1*1 - 3*4 = -11,")
print("sign (-1)^(2+0) = +1, so C[2][0] = -11 and")
print(f"A^{{-1}}[0][2] = -11/9 = {-11 / 9:.6f}")
print("Reading row 0 and column 2 instead would delete row 0 and column 2, leaving")
print("[[1, 4], [0, 2]], determinant 2, sign (-1)^(0+2) = +1, giving 2/9 - a")
print("plausible-looking number that is in the wrong place.")

print_matrix("check A A^{-1}", matmul(A, Ainv), prec=6)
print_matrix("check A^{-1} A", matmul(Ainv, A), prec=6)
print("Both are the identity to 6 decimals. The rounding error is the only thing")
print("distinguishing them from an exact 0 and 1.")

print()
print("=== Cramer's rule gets the same answer from determinants alone ===")
b = [5.0, 7.0, 4.0]
x = solve_by_determinants(A, b)
print(f"A = {A},  b = {b}")
print(f"x_i = det(A_i)/det(A) gives x = {[round(v, 6) for v in x]}")
residual = [matvec(A, x)[i] - b[i] for i in range(3)]
print(f"residual A x - b = {[round(v, 12) for v in residual]}")
print("Cramer's rule needs n+1 determinants, each O(n!) by cofactor expansion, so")
print("it is purely a hand-calculation device. Gaussian elimination is what you")
print("actually run; this is here because the formula explains why det != 0")
print("is precisely the condition for a unique answer.")

print()
print("=== det = 0 means no unique solution, and it means two different things ===")
print()
print("Case 1: b is in the span of the columns, so there are infinitely many x.")
S = [[1.0, 2.0],
     [2.0, 4.0]]               # row 1 = 2 * row 0
print_matrix("S =", S, prec=1)
print(f"det(S) = {det_cofactor(S):g}")
b1 = [3.0, 6.0]                # b1 = 3 * (first column), so x = (3, 0) works
print(f"b = {b1}:  S x = b has x = (3, 0)")
print(f"   S (3, 0) = {matvec(S, [3.0, 0.0])}, which is b, so a solution exists.")
print("   But S (3, 0) = S (-1, 2), so x = (-1, 2) is another solution:")
print(f"   S (-1, 2) = {matvec(S, [-1.0, 2.0])}")
print("   Infinitely many: x = (3 - 2t, t) for any t.")
b2 = [3.0, 7.0]                # inconsistent: the left sides always satisfy x2 = 2 x1
print(f"b = {b2}:  any S x has second entry twice its first ({b2[1]:g} != 2*{b2[0]:g}),")
print("   so no x exists at all.")
print()
print("So det(A) = 0 does NOT mean 'no solution'. It means 'not exactly one'.")
print("The distinction between the two cases above needs the row reduction of")
print("lesson 32; the determinant alone cannot tell you which one you are in.")

print()
print("=== The adjugate of a singular matrix is not a back door ===")
S3 = [[1.0, 2.0, 3.0],
      [2.0, 4.0, 6.0],
      [1.0, 1.0, 1.0]]
print_matrix("S3 =", S3, prec=1)
print(f"det(S3) = {det_cofactor(S3):g}   (row 1 is 2 * row 0)")
print_matrix("adj(S3)", adjugate(S3), prec=1)
print_matrix("S3 adj(S3)", matmul(S3, adjugate(S3)), prec=1)
print("The adjugate is still perfectly well defined - it is a cofactor")
print("computation, not a division - but the identity adj(S3) S3 = det(S3) I now")
print("reads 0 = 0 and tells you nothing. Dividing by det(S3) = 0 is what fails.")
print()
print("The general shape of the fact, for n >= 2: when det(A) = 0 the rows of")
print("adj(A) are all zero, so adj(A) is itself singular and gives no inverse.")

print()
print("=== det(A) != 0 is exactly invertibility, in one line ===")
for M, name in [(A, "the worked example"),
                ([[3.0, 1.0], [2.0, 4.0]], "invertible 2x2"),
                (S, "singular 2x2"),
                (S3, "singular 3x3")]:
    dd = det_cofactor(M)
    try:
        inverse_by_adjugate(M)
        got = "an inverse"
    except ValueError:
        got = "no inverse"
    print(f"det = {dd:>4g}   {name:22s} -> {got}")
print("Exactly one of the two things is true in every row: a nonzero determinant")
print("gives an inverse, a zero determinant does not. There is no in-between and")
print("no near-miss, because 'nonzero' is exactly the condition Cramer's rule,")
print("the adjugate formula, and Gaussian elimination all share.")
```

### With Libraries

Everything above was plain Python nested lists. numpy runs the same arithmetic in
compiled code and hands you the determinant, the inverse, and the solve in one
line each. None of it is magic — but the fourth block shows where the shortcut
stops being safe.

```python
# Everything above was plain Python nested lists. numpy does the same
# mathematics in compiled code, through LU factorisation with partial
# pivoting rather than cofactors. Nothing here is magic - except slogdet,
# which is the one routine on this page that the hand-written version cannot
# imitate, and that is exactly why you should reach for it.

import numpy as np

A = np.array([[2.0, 1.0, 3.0],
              [1.0, 4.0, 1.0],
              [0.0, 2.0, 1.0]])
b = np.array([5.0, 7.0, 4.0])

print("=== The whole lesson, four lines ===")
print(f"np.linalg.det(A)      = {np.linalg.det(A):g}")
print("np.linalg.inv(A)      =")
print(np.linalg.inv(A))
print("A @ inv(A)            =")
print(A @ np.linalg.inv(A))
print(f"np.linalg.solve(A, b) = {np.linalg.solve(A, b)}")
print()
print("Everything above is the hand-written det_cofactor, adjugate, and Cramer's")
print("rule from the previous blocks. numpy does the same mathematics in compiled")
print("code, but through LU factorisation with partial pivoting, never cofactors.")

print()
print("=== slogdet: the numerically sane way to ask about singularity ===")
# np.linalg.det underflows to 0.0 once the determinant drops below about 1e-308,
# so a nonzero determinant can read as zero. slogdet returns the sign and the log
# of the absolute value separately and never underflows.
hilbert3 = np.array([[1.0 / (i + j + 1) for j in range(3)] for i in range(3)])
hilbert6 = np.array([[1.0 / (i + j + 1) for j in range(6)] for i in range(6)])
cases = [
    ("A (the worked example)", A),
    ("A * 1e-30", A * 1e-30),
    ("A * 1e-100", A * 1e-100),
    ("A * 1e-110", A * 1e-110),
    ("3x3 Hilbert", hilbert3),
    ("6x6 Hilbert", hilbert6),
]
print(f"{'matrix':26s} {'det':>12} {'slogdet sign':>13} {'slogdet log|det|':>18}")
for name, M in cases:
    sign, logabs = np.linalg.slogdet(M)
    print(f"{name:26s} {np.linalg.det(M):>12.4g} {sign:>+13.0f} {logabs:>18.4f}")
print()
print("Look at the fourth row of that table.")
print("A * 1e-110 is exactly A scaled down by a constant. Every entry is a perfectly")
print("ordinary double. Its determinant is 9 * 1e-330, a nonzero real number, and")
print("yet np.linalg.det reports 0.0 while slogdet still reports sign +1 and a log")
print("of -757.6559. The value fell below the smallest positive normal float64,")
print("about 2.2e-308, and no double-precision routine can hand it back.")
print()
print("That is the practical meaning of the adjugate formula's precondition.")
print("'det(A) != 0' is a claim about exact arithmetic. The question you actually")
print("want to ask a computer is 'is A invertible to within the precision I have',")
print("which is what an LU pivot tolerance, a condition number, or slogdet's sign")
print("answers - never det == 0.")
print()
print("The Hilbert rows are the classic worst case. A Hilbert matrix has ones on")
print("the diagonal and 1/(i+j+1) off it, and its determinant is nonzero and tiny")
print("from the very first size:")
for name, M in [("3x3 Hilbert", hilbert3), ("6x6 Hilbert", hilbert6)]:
    print(f"  {name}: det = {np.linalg.det(M):.4g}, cond = {np.linalg.cond(M):.4g}, "
          f"digits lost ~ {np.log10(np.linalg.cond(M)):.0f}")
print()
print("Every one of those determinants is nonzero, so by the theorem every one of")
print("those matrices has an exact inverse. Their condition numbers say how many")
print("of the 16 digits of float64 survive the trip through A^-1 b.")

print()
print("=== det(AB) = det(A) det(B) in floating point ===")
rng = np.random.default_rng(11)
worst = 0.0
for _ in range(2000):
    M = rng.normal(size=(4, 4))
    N = rng.normal(size=(4, 4))
    lhs = np.linalg.det(M @ N)
    rhs = np.linalg.det(M) * np.linalg.det(N)
    worst = max(worst, abs(lhs - rhs) / abs(rhs))
print(f"2000 random 4x4 pairs: worst relative error in det(MN) - det(M)det(N) "
      f"was {worst:.2e}")
print("That is rounding, not a broken identity: a 4x4 determinant of Gaussian")
print("entries is itself the difference of products of 24 numbers, so it has")
print("already lost several digits before you multiply anything.")
print()
print("Underflow is the real reason nobody computes det(A)det(B) in code. For a")
print("large sparse matrix, work with the log:")
sign_a, log_a = np.linalg.slogdet(A)
sign_b, log_b = np.linalg.slogdet(A)
print(f"slogdet(A) + slogdet(A) = ({sign_a * sign_b:+.0f}, {log_a + log_b:.4f})")
print(f"slogdet(A @ A)           = ({np.linalg.slogdet(A @ A)[0]:+.0f}, "
      f"{np.linalg.slogdet(A @ A)[1]:.4f})")
print("Same numbers, no underflow, no overflow. A random-walk probability")
print("computation that needs det(P)^k should use k * log det(P).")

print()
print("=== det != 0 is not the same as well-conditioned ===")
print("A matrix can be invertible and still so badly scaled that inverting it in")
print("floating point destroys most of its digits.")
for c in (1.0, 1e-6, 1e-10, 1e-14):
    M = np.array([[1.0, 0.0], [0.0, c]])
    k = np.linalg.cond(M)
    print(f"  diag(1, {c:.0e}): det = {np.linalg.det(M):.1e} (nonzero), "
          f"cond = {k:.1e}, digits lost ~ {np.log10(k):.0f}")
print()
print("Every one of those determinants is nonzero, so by the theorem every one of")
print("those matrices has an exact inverse. Three of them have an inverse that is")
print("useless numerically. This is why a solver tests the pivot against a")
print("tolerance and never tests det == 0.")

print()
print("=== Solving with many right-hand sides ===")
B = np.array([[1.0, 0.0, 2.0],
              [0.0, 1.0, 3.0],
              [1.0, 1.0, 1.0]])
X = np.linalg.solve(A, B)
print("A =")
print(A)
print("B =")
print(B)
print("B has three columns, so solve returns all three solutions at once:")
print(X)
print("each column of X satisfies A @ X = B:")
print(A @ X)
print()
print("This is the concrete reason to prefer solve over inv. With k right-hand")
print("sides, one factorisation plus k triangular solves costs O(n^3 + k n^2).")
print("Forming inv(A) first costs the same O(n^3) factorisation, then a full")
print("O(n^3) matrix multiply, and then throws away k*n - k of the n^2 entries")
print("it just computed.")

Y = np.linalg.inv(A) @ B
print()
print("inv(A) @ B reaches the same answer the long way:")
print(Y)
print(f"max entrywise difference: {np.max(np.abs(Y - X)):.3e}")
print("Tiny here because A is well conditioned. On the diag(1, 1e-14) matrix the")
print("same two routes differ in the sixth digit of the answer.")
```

## Common Mistakes

**Mistake 1: forgetting the transpose in `adj(A)`.**
The wrong version: `C[i][j] = cofactor of entry (j, i)` and calling the result
`A⁻¹`. The right version: the *cofactor matrix* is `C_ij = (-1)^{i+j}det(M_ij)`,
the *adjugate* is `Cᵀ`, and the inverse is `adj(A)/det(A)`. In the worked
example `C[0][1] = -1` but `adj[0][1] = 5`, so mixing them up gives a matrix whose
entries are all plausible and none of them right. It is tempting because for a
**symmetric** matrix `C` is symmetric, so the transpose is a no-op and the bug
never fires on your first test case. Test on a nonsymmetric matrix.

**Mistake 2: `det(cA) = c·det(A)`.**
The wrong version: thinking that scaling a matrix scales its determinant by the
same factor. The right version: `det(cA) = cⁿ det(A)`. Scaling **one** row by `c`
gives `c·det(A)`; scaling all `n` rows gives `cⁿ`. The code prints both: a `3×3`
scaled by 3 has determinant `27 × 9 = 243`, not `3 × 9 = 27`. It is tempting
because determinants behave additively on sums, so linearity feels natural — but
the determinant is emphatically *not* linear, see Mistake 3.

**Mistake 3: assuming `det(A + B) = det(A) + det(B)`.**
The wrong version: using the determinant as though it were linear, the way the
trace is. The right version: the determinant is a polynomial in the entries of
degree `n`, so `A + B` brings cross terms. Only `tr(A + B) = tr(A) + tr(B)` and
`det(cA) = cⁿdet(A)` are clean, and they are clean for different reasons. It is
tempting because `tr` really is linear and the two functions get used side by side
in the same diagonalisation code.

**Mistake 4: reading `det(A) = 0` as "no solution".**
The wrong version: catching `LinAlgError: Singular matrix` and reporting that the
system has no solution. The right version: `det(A) = 0` means the system has **not
exactly one** solution. It may have none, or it may have infinitely many, and the
determinant cannot tell you which because it never sees `b`. The code demonstrates
both with the same singular matrix `S`: `b = (3, 6)` gives infinitely many
solutions, `b = (3, 7)` gives none. Only row reduction on the augmented matrix
distinguishes them.

**Mistake 5: testing `det(A) == 0` to decide whether to invert.**
## Formula Sheet

`A` is `n × n` over a field `F`; `a_ij` is row `i`, column `j`; `M_ij` is the minor
of `(i, j)`; `C_ij` is the cofactor; `σ ∈ S_n` is a permutation of `{1, …, n}`;
`sgn(σ)` is its sign; `|S_n| = n!`; `b ∈ Fⁿ`; `I_n` is the identity; `c ∈ F`.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$\det(A)$`, `1×1` | `$\det([a]) = a$` | The lone entry. | Base case of every recursive scheme |
| minor `$M_{ij}$` | `A` with row `i` and column `j` deleted | The square matrix left over once you commit to entry `(i,j)`. | One cofactor computation |
| cofactor `$C_{ij}$` | `$C_{ij} = (-1)^{i+j}\det(M_{ij})$` | Minor's determinant with a checkerboard sign: `+` when `i+j` is even, `−` when odd. | Cofactor expansion |
| cofactor expansion | `$\det(A) = \sum_{j=1}^{n} a_{1j}C_{1j}$` | Expand along any row `i` or column `j`: one term per entry, each entry times its cofactor. | By hand, `n ≤ 3` |
| `2 × 2` rule | `$\det\begin{pmatrix} a & b\\ c & d\end{pmatrix} = ad - bc$` | Diagonal products, minus off-diagonal. The recursion's base case. | Every hand calculation |
| Leibniz formula | `$\det(A) = \sum_{\sigma \in S_n}\operatorname{sgn}(\sigma)\prod_{i=1}^{n} a_{i,\sigma(i)}$` | One signed term per way of picking one entry from each row and each column. `n!` terms. | Proving the properties; never computing |
| `$\operatorname{sgn}(\sigma)$` | `$(-1)^{\#\{i<j : \sigma(i)>\sigma(j)\}}$` | `+1` for an even permutation, `−1` for an odd one. | Sign in the Leibniz sum |
| geometric meaning | `$\operatorname{vol}(AS) = \lvert\det(A)\rvert\operatorname{vol}(S)$` | `A` multiplies every `n`-dimensional volume by `\|det(A)\|`. Requires `A ∈ ℝ^{n×n}`. | Interpreting a determinant |
| sign of the determinant | `$\det(A) > 0$` preserves orientation, `$\det(A) < 0$` reverses it, `$\det(A) = 0$` collapses space | The sign says whether the map turned space inside out. | Interpreting a determinant; picking a winding convention |
| `$\det(cA)$ | `$\det(cA) = c^{n}\det(A)$` | Scaling every row by `c` scales the determinant by `c` **to the power `n`** — the trap in Mistake 2. | Sanity-checking a scaling argument |
| `$\det(AB)$ | `$\det(AB) = \det(A)\det(B)$` | Applying `B` then `A` scales volumes by the product of the two scale factors. `A, B` both `n × n`. | Checking; **never** how you should compute a big determinant — use `slogdet` |
| `$\det(A^{\mathsf T})$ | `$\det(A^{\mathsf T}) = \det(A)$` | Flipping rows and columns changes nothing. | Debugging a transpose bug |
| `$\det(A^{-1})$ | `$\det(A^{-1}) = 1/\det(A)$` | Undoing multiplies by the reciprocal. Needs `$\det(A) \ne 0$`. | Volume factor of an inverse map |
| row swap | `$\det(\text{A with } R_i,R_j \text{ exchanged}) = -\det(A)$` | One transposition, one sign flip. | Explaining the pivot sign in `determinant_lu` |
| row add | `$\det(R_i + cR_j) = \det(A)$` | Adding a multiple of one row to another changes nothing. | **Why elimination computes determinants** |
| row scale | `$\det(cR_i) = c\det(A)$` | Scaling one row by `c` scales the determinant by `c`. | The `cⁿ` rule, applied row by row |
| triangular | `$\det(U) = \prod_{i=1}^{n} u_{ii}` | For triangular `U`, multiply the diagonal. No expansion needed. | Reading a determinant off an LU factorisation |
| cofactor matrix `C` | `$C_{ij} = (-1)^{i+j}\det(M_{ij})$` | Entry-by-entry. **Not** the adjugate. | Building the adjugate |
| adjugate | `$\operatorname{adj}(A) = C^{\mathsf T}$` | The cofactor matrix with rows and columns exchanged. | The inverse formula |
| adjugate identity | `$A\operatorname{adj}(A) = \operatorname{adj}(A)A = \det(A)I_n$` | Holds for **every** square `A`, singular or not. | Proving the inverse exists |
| inverse formula | `$A^{-1} = \operatorname{adj}(A)/\det(A)$` | Cofactors, transposed, divided by the determinant. **Requires `det(A) ≠ 0`** — it divides. | Hand computation for `n ≤ 3`; proofs |
| adjugate of a singular matrix | `$\det(A)=0,\ n\ge 2 \Rightarrow \operatorname{adj}(A) = 0$` | Every row of the adjugate is zero, so it is singular too. | Why the adjugate is not a back door to an inverse |
| Cramer's rule | `$x_i = \det(A_i)/\det(A)$` | `A_i` is `A` with column `i` replaced by `b`. Requires `$\det(A) \ne 0$`. | Pencil-and-paper on tiny systems |
| `$\det(A) = 0` means | "not exactly one solution" — could be none, could be infinitely many | The determinant never sees `b`, so it cannot say which. | Explaining a `LinAlgError` without claiming "no solution" |
| `cond(A)` | `$\lVert A\rVert\lVert A^{-1}\rVert$; digits lost `≈ log₁₀ cond` | `det(A) ≠ 0` is exact arithmetic; conditioning is floating point. | Before trusting `inv` or `solve` |
| cofactor cost | `$\Theta(n!)` | Forking recursion: `T(n) = n T(n-1)`. | Explains why nobody uses it |
| elimination cost | `$\Theta(n^{3})$`, and `det(A) = (-1)^{\text{swaps}}\prod_i u_{ii}$` | Row reduction gives the determinant for free. | The practical route, and all of `numpy.linalg.det` |
| adjugate cost | `$\Theta(n^{4})$ | `n²` cofactors, each an `O(n³)` determinant. | Even the closed form loses to LU |

The wrong version: `if np.linalg.det(A) != 0: x = np.linalg.inv(A) @ b`. The right
version: call `np.linalg.solve(A, b)` and let it raise if it must; if you must
test, test the LU pivot against a tolerance or test `slogdet`'s sign. The code
shows `A * 1e-110` whose true determinant is `9 × 10⁻³³⁰` — nonzero — reported by
`np.linalg.det` as exactly `0.0`. A zero determinant computed in floating point is
a statement about your precision, not about the matrix. And `inv(A) @ b` is
strictly more work and strictly less accurate than `solve(A, b)`, as
[lesson 32](32_linear_systems_gaussian_elimination.md) already warned.

---

## Multiple Choice Questions

**Q1.** `A` is a 3×3 matrix and `det(A) = 0`. What must be true?

- A) The system `Ax = b` has no solution, for every `b`
- B) The system `Ax = b` has infinitely many solutions, for every `b`
- C) The system `Ax = b` has either no solution or infinitely many, depending on `b`
- D) `A` has at least one row that is entirely zero

<details>
<summary>Answer and explanation</summary>

**C) The system `Ax = b` has either no solution or infinitely many, depending on
`b`.**

`det(A) = 0` means the elimination of [lesson 32](32_linear_systems_gaussian_elimination.md)
runs out of pivots, which means the map `x ↦ Ax` is not one-to-one, which means
"not exactly one solution". The two remaining possibilities are both real, and
the code demonstrates both with the same matrix `S = [[1,2],[2,4]]`: with
`b = (3,6)` the solution set is the whole line `x = (3−2t, t)`, and with `b = (3,7)`
there is no solution at all because `7 ≠ 2·3`.

- A) confuses "not unique" with "none". The determinant is a property of `A`
  alone; it contains no information about `b`. Claiming "no solution for every
  `b`" would require `col(A) = {0}`, i.e. `A = 0`, which is a far stronger
  statement than `det(A) = 0`.
- B) is the other half of the same confusion. Infinite solutions need
  `b ∈ col(A)`, which is a condition on `b` and on the specific `A`. Here
  `col(A)` is the line of vectors `(t, 2t)`, so `b = (3,6)` is in it and `b = (3,7)`
  is not.
- D) confuses singularity with a specific cause. Singular means *some* linear
  dependence among the rows; `S`'s rows are `[1,2]` and `[2,4]`, and neither is
  zero. A zero row would force `det = 0`, but the converse is false, and Mistake
  4's point is precisely that the determinant cannot diagnose *which* dependence
  you have.

</details>

**Q2.** Which statement about `adj(A)` is correct?

- A) `adj(A) A = det(A) I` holds only when `det(A) ≠ 0`
- B) `adj(A) A = det(A) I` holds for every square `A`, and `A⁻¹ = adj(A)/det(A)` needs `det(A) ≠ 0`
- C) `adj(A)` is the cofactor matrix `C` itself, with no transpose involved
- D) `adj(A) = det(A) · A⁻¹` is a definition that also works when `det(A) = 0`

<details>
<summary>Answer and explanation</summary>

**B) `adj(A) A = det(A) I` holds for every square `A`, and `A⁻¹ = adj(A)/det(A)`
needs `det(A) ≠ 0`.**

The adjugate identity is a polynomial identity in the entries of `A`, established
by cofactor expansion, and it makes no assumption about the determinant. What
requires `det(A) ≠ 0` is the *next step*: dividing both sides by `det(A)`. The
code separates the two statements explicitly — `adjugate(S3)` and
`matmul(S3, adjugate(S3))` both work fine on the singular matrix `S3`, and the
product is the zero matrix because `det(S3) I = 0 I = 0`.

- A) is the classic over-restriction. If you need `det(A) ≠ 0` to state the
  identity, you cannot use the identity to *prove* `det(A) ≠ 0` implies
  invertibility, since the theorem would then be circular.
- C) is Mistake 1. In the worked example, `C[0][1] = -1` while `adj[0][1] = 5`.
  The transpose is not a formality; on a symmetric matrix the two agree, which is
  why the bug survives casual testing.
- D) is circular in the wrong direction — it uses `A⁻¹` to define `adj(A)` and then
  claims to recover `A⁻¹`. It also fails where it matters: when `det(A) = 0` the
  expression `det(A) · A⁻¹` has nothing to multiply, and the code confirms the
  adjugate of a singular `n × n` matrix (for `n ≥ 2`) is the **zero** matrix, so
  it certainly is not hiding an inverse.

</details>

**Q3.** `det(cA)` for a 3×3 matrix `A` and scalar `c` is:

- A) `c · det(A)`, because the determinant is linear
- B) `c² · det(A)`, because the determinant is quadratic in the entries
- C) `c³ · det(A)`, because scaling all three rows multiplies the determinant by `c` three times
- D) `c^det(A) · det(A)`

<details>
<summary>Answer and explanation</summary>

**C) `c³ · det(A)`, because scaling all three rows multiplies the determinant by
`c` three times.**

Scaling **one** row by `c` multiplies the determinant by `c`. `cA` scales all
three, so the factor is `c³`. The code checks it numerically: `A` has
`det(A) = 9`, `3A` has `det = 243`, and `3³ · 9 = 243`. In general `det(cA) =
cⁿ det(A)` for an `n × n` matrix, so a `20 × 20` matrix scaled by 2 has its
determinant multiplied by about a million.

- A) is Mistake 2. It is the answer you get if you remember the single-row rule
  and forget to apply it three times. The temptation is real: the trace *is*
  linear, so `tr(cA) = c tr(A)`, and the two functions appear together in
  diagonalisation code.
- B) is a real confusion but the wrong degree. The determinant is degree `n` in
  the entries — every term in the Leibniz formula is a product of exactly `n`
  entries. For a 3×3 that happens to be degree 3, not 2; someone reasoning
  "it's the volume, and volume is quadratic" is thinking of a 2×2 case, where
  `det(cA) = c² det(A)` is indeed correct.
- D) has no mathematical content. `c^det(A)` is not a determinant rule under any
  hypothesis, and it gives nonsense immediately: `det(2I₃) = 8`, while
  `2^det(I₃) · det(I₃) = 2 · 1 = 2`.

</details>

**Q4.** Which is the *only* correct statement about the determinant?

- A) `det(A) = 0` implies the columns of `A` are all zero
- B) `det(A + B) = det(A) + det(B)`
- C) `det(A) = det(Aᵀ)`, and `det(A) det(B) = det(AB)`
- D) `det(AB) = det(A) + det(B)`

<details>
<summary>Answer and explanation</summary>

**C) `det(A) = det(Aᵀ)`, and `det(A) det(B) = det(AB)`.**

Both are on the properties list and both hold for square matrices of a common
size. The transposed-determinant identity holds because transposing swaps `a_ij`
for `a_ji`, which maps even permutations to even and odd to odd, so every sign in
the Leibniz sum survives — the code prints `det(P) = det(Pᵀ) = -2`.
Multiplicativity is the volume-scaling property: apply `B` then `A`, and volumes
scale by `det(B)` then by `det(A)`, hence by the product. The code checks
`det(PQ) = 4 = (-2)(-2)` for `P = [[1,2],[3,4]]` and `Q = [[5,6],[7,8]]`.

- A) is far too strong. `[[1,2],[2,4]]` has `det = 0` and not one zero entry. The
  determinant is zero exactly when the columns are *linearly dependent*, which
  means one is a combination of the others, not that any of them vanish.
- B) is Mistake 3, and the single most quoted false statement in linear algebra.
  It fails on the smallest possible example: `A = B = I₂` gives
  `det(2I₂) = 4` on the left and `1 + 1 = 2` on the right.
- D) mixes two different rules. It looks like `tr(AB) = tr(BA)` from
  [lesson 31](31_matrices_and_matrix_algebra.md) — where a similar-looking
  identity really is true — with the multiplicative determinant rule. Note the
  trap: `tr(AB) = tr(BA)` *is* true even though `AB ≠ BA`, but there is no
  additive analogue of it for the determinant at all.

</details>

**Q5.** The Leibniz formula gives the "true" definition of the determinant. Why
is it never used to compute one?

- A) It is only defined for matrices with integer entries
- B) It requires `n!` terms, which is `3,628,800` for `n = 10` and `Θ(n!)` overall, against `Θ(n³)` for row reduction
- C) It gives the determinant only up to sign, and recovering the sign needs a separate computation
- D) It requires a choice of pivot order, which makes it numerically unstable

<details>
<summary>Answer and explanation</summary>

**B) It requires `n!` terms, which is `3,628,800` for `n = 10` and `Θ(n!)`
overall, against `Θ(n³)` for row reduction.**

The code prints the comparison table: at `n = 8` the Leibniz sum has `40,320`
terms against `512` multiply-adds for elimination, and at `n = 20` it has about
`2.4 × 10¹⁸` terms against `8,000`. Leibniz is not just slower — it is in a
different complexity class, `Θ(n!)` rather than `Θ(n³)`, so no engineering
improvement closes the gap.

- A) is false: the Leibniz formula is perfectly well defined over any field,
  including `ℝ`, and the code computes `det(A) = 9` for a matrix of floats.
  Sums of products of real numbers are real numbers.
- C) is false and the sign is fully determined by the formula — `sgn(σ)` is
  right there in the summand. The code prints all six signed terms for the 3×3
  case and the running total is exactly `9`.
- D) is false for two reasons. Leibniz has no pivots at all — it is a direct
  combinatorial sum. And the numerical-instability argument, while true of
  everything, is not the reason: this formula is *exact*, not unstable, it is
  merely combinatorially absurd. The instability lives in the row-reduction
  route, and partial pivoting is what fixes it there.

</details>

**Q6.** A 2×2 matrix `A` has `det(A) = -5`. Which geometric statement follows?

- A) `A` maps area-1 shapes to area-5 shapes
- B) `A` maps area-1 shapes to area-5 shapes and reverses orientation
- C) `A` is not invertible, because a negative determinant is not positive
- D) `A` rotates by 180° and scales by 5

<details>
<summary>Answer and explanation</summary>

**B) `A` maps area-1 shapes to area-5 shapes and reverses orientation.**

`|det(A)| = 5` is the area scale factor, and `det(A) < 0` is the orientation
reversal. The code's `G2 = [[1,2],[2,1]]` case is exactly this: the unit square's
images come out as `(0,0), (1,2), (3,3), (2,1)` with shoelace signed area `-3`, so
the area tripled and the corner order went from counterclockwise to clockwise.
Compare `G1 = [[2,0],[0,3]]`, `det = +6`, where the area is still `|det| = 6` but
the order stays counterclockwise.

- A) is right about the magnitude and wrong about the sign's significance. It is
  the answer you get if you treat `det` as `|det|` throughout, which is
  tempting because volume is unsigned. But the sign is not noise: it is the
  orientation data, and it is the reason `det` rather than `|det|` is the
  multiplicative function — `|det(AB)| = |det A||det B|` is true but throws away
  the information that `A` and `B` compose to two orientation-reversing maps.
- C) is the misunderstanding that a determinant is a volume. A negative volume is
  not a contradiction; it is a signed volume. Invertibility is about `≠ 0`, and
  `-5 ≠ 0` as surely as `5 ≠ 0`. The lesson's own test table shows a matrix with
  `det = -2` and an inverse, `P = [[1,2],[3,4]]`.
- D) confuses a determinant with an eigenvalue. A 180° rotation by scale 5 is
  `-5I₂`, whose determinant is `(-5)² = 25`, positive — because a 180° rotation
  in the plane preserves orientation, being a product of two reflections. The
  determinant of a planar map tells you about reflections and area, not about
  rotation angle; recovering the rotation needs the eigenvalues or the polar
  decomposition from
  [lesson 39](39_diagonalization_and_spectral.md).

</details>

**Q7.** You need `x` for ten different right-hand sides `b_1, …, b_10` with the
same matrix `A`. Which is the right call?

- A) `det(A)`, then `inv(A) @ b_i` for each `i`, so you can check invertibility once
- B) `np.linalg.solve(A, b_i)` for each `i`, letting the library factorise each time
- C) `np.linalg.inv(A)` once, then `inv(A) @ b_i` for each `i`
- D) `np.linalg.solve(A, B)` once with `B` the 10-column matrix of right-hand sides

<details>
<summary>Answer and explanation</summary>

**D) `np.linalg.solve(A, B)` once with `B` the 10-column matrix of right-hand
sides.**

`solve` factorises `A` once and then does ten triangular solves, each `O(n²)`,
for `O(n³ + 10n²)`. The code shows the mechanism with three columns: `B` has
three columns, `np.linalg.solve(A, B)` returns a 3-column `X`, and `A @ X = B` up
to rounding at `10⁻¹⁶`.

- A) pays for an `O(n³)` determinant *and* an `O(n³)` inverse formation, then
  discards all `n²` entries except the row you needed, ten times. And
  `det(A) != 0` is the wrong test anyway — the code shows `A * 1e-110`, whose true
  determinant is `9 × 10⁻³³⁰`, reported by `np.linalg.det` as exactly `0.0`.
- B) gets the right answer with the right routine and pays for the `O(n³)`
  factorisation ten times over. It is the correct code, just wasteful; if you
  genuinely need one-off solves with the same `A`, this is what you write.
- C) is the standard textbook error. It forms `n²` numbers to use `n` of them per
  solve, does a full `O(n³)` matrix multiply instead of a triangular solve, and
  loses accuracy at every step. The code shows `inv(A) @ B` agreeing with `solve`
  to `4.441e-16` here — but that is only because this `A` is well conditioned.
  On `diag(1, 1e-14)` the same two routes disagree in the sixth digit.

</details>

**Q8.** Which matrix's determinant tells you nothing about whether it is
invertible in floating-point arithmetic?

- A) `[[1, 0], [0, 0]]`, whose determinant computes to exactly 0
- B) `[[1, 2], [2, 4]]`, whose determinant computes to exactly 0
- C) `A · 10⁻¹¹⁰` for an invertible `A`, whose determinant computes to 0 by underflow
- D) `[[0, 0], [0, 0]]`, whose determinant computes to exactly 0

<details>
<summary>Answer and explanation</summary>

**C) `A · 10⁻¹¹⁰` for an invertible `A`, whose determinant computes to 0 by
underflow.**

The code's `slogdet` table shows `A * 1e-110` with `det = 0` from
`np.linalg.det` but `sign = +1` and `log|det| = -757.6559` from
`np.linalg.slogdet`. The true determinant is `9 × 10⁻³³⁰`, comfortably nonzero in
real arithmetic; it has simply fallen below the smallest positive normal float64
of about `2.2 × 10⁻³⁰⁸`. Every entry of the matrix itself is an ordinary double.

- A), B) and D) all give a determinant of exactly zero for the right reason: the
  matrix really is singular. In each case the rows genuinely depend — `[[1,0],[0,0]]`
  has a zero row, `[[1,2],[2,4]]` has row 1 twice row 0, `[[0,0],[0,0]]` has all
  zeros. The computed zero agrees with the mathematics, so it carries information.
- The distinction matters because the two situations look identical to the code
  that branches on them. `if np.linalg.det(A) == 0` takes the singular branch for
  a matrix that has an exact inverse and loses about 757 digits' worth of scale to
  underflow. The lesson's `determinant_lu` avoids this by comparing the *pivot*
  against a tolerance `tol = 1e-12` rather than testing for an exact zero, which
  is why every LU-based solver on the planet works that way.

</details>

**Q9.** Why does `det(AB) = det(A)det(B)` make the determinant a *useful*
invariant rather than an arbitrary one?

- A) Because it lets you compute `det(A)` from `A` without factoring it
- B) Because it says that a determinant can be factorised into primes, so it detects integer matrices
- C) Because it says the volume change of "apply `B`, then apply `A`" is the product of the two individual volume changes
- D) Because it means `det(A)` is determined by `tr(A)` and `AB ≠ BA`

<details>
<summary>Answer and explanation</summary>

**C) Because it says the volume change of "apply `B`, then apply `A`" is the
product of the two individual volume changes.**

That is exactly `vol(A(BS)) = |det A| · |det B| · vol(S)`, which is what any scale
factor must do: the composition of two scalings scales by the product. The code
checks `det(PQ) = 4` with `det(P) = det(Q) = -2`, and both factors are negative,
so the composition of two orientation-reversing maps preserves orientation — a
fact you could not read off either determinant alone.

- A) inverts the direction of usefulness. `det(AB)` does not help you compute
  `det(A)`; it helps you verify one determinant against another, which is a
  consistency check on your code, not a computational shortcut. In practice you
  compute `det(A)` by elimination and never by factorisation.
- B) confuses the determinant of a matrix with the determinant of an integer, a
  different notion (`det(A)` for integer `A` *is* an integer, but multiplicativity
  here is about composition of linear maps, and `det` on matrices is not the
  number-theoretic determinant used for factoring). It also gives the wrong
  answer to the question asked: `det(A) ≠ 0` says nothing about whether `A` has
  prime factors in any useful sense.
- D) is confused on three counts. `det` and `tr` are different invariants —
  the code's `P` has `tr(P) = 5` and `det(P) = -2` — and neither determines the
  other. And `AB ≠ BA` is precisely why `det(AB) = det(BA)` is *interesting*: two
  different matrices with the same determinant. Multiplicativity is not a
  commutativity claim.

</details>

**Q10.** You compute `A · adj(A)` for a singular 3×3 matrix `A` and get the zero
matrix. What have you learned?

- A) That `adj(A)` contains `A⁻¹` and you can divide by `det(A) = 0` to get it
- B) That the adjugate identity is false for singular matrices and was never proved
- C) That `adj(A) = 0`, so the adjugate is singular too and gives no inverse — the identity `A adj(A) = det(A) I` now reads `0 = 0`
- D) That `A` has three zero rows

<details>
<summary>Answer and explanation</summary>

**C) That `adj(A) = 0`, so the adjugate is singular too and gives no inverse —
the identity `A adj(A) = det(A) I` now reads `0 = 0`.**

The code computes exactly this for `S3 = [[1,2,3],[2,4,6],[1,1,1]]`: `det(S3) = 0`,
`adj(S3)` prints as the zero matrix, and `S3 adj(S3)` is the zero matrix. The
identity is not false — it is *uninformative*. `A adj(A) = det(A) I` with
`det(A) = 0` is the statement `A adj(A) = 0`, which is true of many pairs and
tells you nothing about how to invert `A`.

- A) inverts the direction of the identity. `A adj(A) = det(A) I` means
  `A⁻¹ = adj(A)/det(A)` **when you can divide**; it never says `adj(A)` is an
  inverse on its own. Dividing by `det(A) = 0` is `0/0`, and the code's
  `inverse_by_adjugate` raises `ValueError` there by design.
- B) misreads a true identity as a false one. The adjugate identity holds for
  every square matrix — it is proved by cofactor expansion with no hypothesis
  about the determinant. The lesson separates the identity from the inverse
  formula for exactly this reason.
- D) is a non-sequitur. `S3`'s rows are `[1,2,3]`, `[2,4,6]` and `[1,1,1]`; none
  is zero. What makes it singular is that row 1 is twice row 0. The determinant
  detects a *dependence*, and a dependent row need not be a zero row — this is
  the same trap as MCQ Q1 option D.

</details>

## Subjective Questions

### Short Answer

**Q1. State the cofactor expansion formula, and explain what the exponent
`i + j` in the cofactor is doing.**

<details>
<summary>Model answer</summary>

For an `n × n` matrix `A`, let `M_ij` be the `(n−1) × (n−1)` matrix obtained by
deleting row `i` and column `j`. The cofactor of entry `(i,j)` is
`C_ij = (−1)^{i+j} · det(M_ij)`, and cofactor expansion says
`det(A) = Σ_{j=1..n} a_1j · C_1j`, valid along **any** row or column.

The exponent `i+j` produces the checkerboard of signs: `+` where `i+j` is even,
`−` where it is odd. It is the sign acquired by moving row `i` to the top of the
matrix by `i−1` adjacent transpositions and column `j` to the left by `j−1`
adjacent transpositions, a total of `(i−1)+(j−1) = i+j−2` swaps, each contributing
a factor of `−1`. Since `−1` raised to `i+j−2` equals `−1` raised to `i+j`, the
sign is `(−1)^{i+j}`. That is why expanding along row 2 of a 3×3 gives signs
`−, +, −` while row 1 gives `+, −, +`.

</details>

**Q2. Give the Leibniz formula and say how it makes the geometric meaning of the
determinant visible.**

<details>
<summary>Model answer</summary>

`det(A) = Σ_{σ ∈ S_n} sgn(σ) · Π_{i=1..n} a_{i,σ(i)}`, where `S_n` is the set of
all `n!` permutations of `{1,…,n}` and `sgn(σ) = (−1)^{#inversions}` counts pairs
`i < j` with `σ(i) > σ(j)`.

Each product `a_{1σ(1)} · a_{2σ(2)} · … · a_{nσ(n)}` is the determinant of the
matrix whose `i`-th row is the original row `i` with its entries permuted, and
hence is twice the signed volume of the simplex spanned by the origin and those
permuted rows — this is the rule of false position. The `n!` simplices indexed by
the permutations tile the parallelepiped spanned by the columns of `A` exactly
once, the even permutations filling the positive-orientation half and the odd ones
the negative half. Summing signed gives `|det(A)|` times the orientation sign,
i.e. the determinant. For `n = 2` the formula is `a₁₁a₂₂ − a₁₂a₂₁`: the two
triangles of the parallelogram.

</details>

**Q3. Why is `det(cA) = cⁿ det(A)` rather than `c · det(A)`? State the
one-row version too.**

<details>
<summary>Model answer</summary>

The one-row version: if only row `i` of `A` is multiplied by `c`, the determinant
is multiplied by `c`. This follows from cofactor expansion along row `i`: the
entry `a_ij` appears in the single term `a_ij · C_ij`, and the cofactor `C_ij`
depends only on the *other* rows, so scaling the entry scales the term and hence
the whole sum by `c`.

`cA` scales **all** `n` rows. Applying the one-row rule `n` times gives
`det(cA) = c · c · … · c · det(A) = cⁿ det(A)`.

Equivalently, from the Leibniz formula each term is a product of exactly `n`
entries, and each entry picks up a factor of `c`, so every one of the `n!` terms
picks up `cⁿ`. The code checks it: `det(A) = 9`, `det(3A) = 243 = 27 · 9`.

</details>

**Q4. Explain why the determinant is *not* a linear function of a matrix, and give
the smallest counterexample.**

<details>
<summary>Model answer</summary>

Linearity would require `det(A + B) = det(A) + det(B)` and
`det(cA) = c det(A)`. Neither holds in general.

`det(cA) = cⁿ det(A)`, which equals `c det(A)` only when `c^{n−1} = 1` — for real
scalars, only when `c = 0`, `c = 1`, or `n = 1`.

The additive failure: take `A = B = I₂`. Then `det(A + B) = det(2I₂) = 4` while
`det(A) + det(B) = 1 + 1 = 2`. Cross terms appear because the determinant is a
polynomial of degree `n` in the entries; the Leibniz formula has `n!` monomials,
and expanding the products in `det(A+B)` produces mixed terms that neither
`det(A)` nor `det(B)` contains.

The trace *is* linear, which is exactly the confusion: `tr(A + B) = tr(A) + tr(B)`
is true, and the two functions are used side by side.

</details>

**Q5. State Cramer's rule and say why it is not used in numerical work.**

<details>
<summary>Model answer</summary>

If `A` is `n × n` with `det(A) ≠ 0` and `Ax = b`, then `x_i = det(A_i) / det(A)`,
where `A_i` is `A` with column `i` replaced by `b`.

It is not used numerically for two compounding reasons. First, cost: it needs
`n + 1` determinant evaluations, and by cofactor expansion each is `Θ(n!)`. Second
and worse, conditioning: computing a solution as a ratio of two numbers that are
both nearly zero loses digits catastrophically. If `det(A)` is small — which is
exactly the near-singular case where a careful numerical answer matters most — the
numerator `det(A_i)` is small too, and the quotient amplifies the relative error of
both by `1/|det(A)|`.

Gaussian elimination computes all `n` components in one `Θ(n³)` pass with no such
division, which is why `np.linalg.solve` is the routine you call.

</details>

**Q6. What does `det(A) = 0` tell you, and what does it fail to tell you?**

<details>
<summary>Model answer</summary>

It tells you the system `Ax = b` does **not** have exactly one solution, for any
`b`; equivalently, `A` is singular and has no inverse, and the map `x ↦ Ax` is not
injective.

It fails to tell you which of the two remaining cases you are in. If
`b ∈ col(A)` there are infinitely many solutions (all `x₀ + ker(A)`); if
`b ∉ col(A)` there are no solutions. The determinant contains no information about
`b` at all — `det` is a function of `A` alone. The code shows both cases for the
same singular `S = [[1,2],[2,4]]`: `b = (3,6)` gives the line `x = (3−2t, t)`,
while `b = (3,7)` gives nothing, because every `Sx` has second entry twice its
first.

Distinguishing them requires the augmented-matrix reduction of
[lesson 32](32_linear_systems_gaussian_elimination.md): a row `[0 … 0 | c]` with
`c ≠ 0` means no solution, a free column means infinitely many.

</details>

### Long Answer

**Q1. Why does `det(A) ≠ 0` fail to be a usable test for invertibility in
floating-point arithmetic, and what should you test instead?**

<details>
<summary>Model answer</summary>

`det(A) ≠ 0` is a theorem about exact arithmetic over a field. It is a statement
about whether there *exists* a matrix `B` with `BA = AB = I`, and it is perfectly
sharp: either exactly one such `B` exists, or none does. There is no in-between,
and that sharpness is what makes it such a clean criterion on paper.

In floating point the arithmetic is finite, and the criterion stops being sharp in
three separate ways.

**Underflow.** The determinant is a polynomial in the `n²` entries involving
products of `n` of them and a sum of `n!` terms, so it is very easy for its true
value to fall outside the representable range even when every entry is
comfortably ordinary. The code's `slogdet` table makes this concrete: `A` has
`det = 9`, and `A · 10⁻¹¹⁰` — a matrix with perfectly ordinary entries — has true
determinant `9 × 10⁻³³⁰`. `np.linalg.det` reports `0.0`. It is not singular; the
number is below the smallest positive normal float64, about `2.2 × 10⁻³⁰⁸`. A
branch on `det == 0` therefore rejects a matrix that has an exact inverse. The
`6 × 6` Hilbert matrix is the standard next example: `det ≈ 5.367 × 10⁻¹⁸`,
`cond ≈ 1.5 × 10⁷`, so seven of your sixteen digits are already gone and the
`12 × 12` version is past saving.

**Overflow.** The mirror-image failure: entries around `10^100` give a determinant
around `10^100⁰⁰⁰`, which overflows to `inf`. `inf != 0`, so the test passes and
you proceed to invert a matrix whose factorisation is already meaningless.

**The deeper problem: nonzero is not the same as well-conditioned.** Even when
`det(A)` is representable and nonzero, its magnitude carries no information about
*how hard* the inversion is, because it conflates the size of the matrix with how
close it is to singular. `diag(1, 10⁻¹⁴)` has `det = 10⁻¹⁴ ≠ 0` and an exact
inverse — and roughly 14 of your 16 digits destroyed by the round trip. The
detected failure mode is therefore not just "wrong verdict about invertibility" but
the worse one: a *right* verdict followed by a *wrong* answer.

**What to test instead.** Three options, in increasing order of usefulness:

- A pivot tolerance inside the factorisation. `determinant_lu` here compares
  `abs(pivot) > tol` with `tol = 1e-12` and returns `0.0` otherwise. This is
  scale-relative — the pivot is compared against the matrix's own scale — and it
  is what every production LU solver does internally.
- `np.linalg.slogdet(A)`, which returns `(sign, log|det|)`. The log never
  underflows or overflows, so it is the right way to ask the determinant question
  on a large sparse matrix. The code uses it to recover the sign `+1` and
  `log|det| = −757.6559` for the matrix `det` calls zero.
- `np.linalg.cond(A) = ‖A‖·‖A⁻¹‖`, which is the quantity that actually predicts
  how many digits you keep. This is the honest diagnostic and the one to reach for
  when the answer will be used in a subsequent calculation rather than merely
  displayed.

The underlying lesson generalises: in exact arithmetic a theorem tells you
*whether* a thing exists, and the dichotomy is clean. In floating point, existence
is not the question that matters — *usefulness* is, and that is a continuous,
scale-dependent quantity.

</details>

**Q2. The adjugate identity `A·adj(A) = det(A)·I` holds for every square matrix.
Why is it not circular as a proof that `A` is invertible when `det(A) ≠ 0`?**

<details>
<summary>Model answer</summary>

The apparent circularity would be real if the identity had a hypothesis. It does
not. `A·adj(A) = det(A)·I` is a *polynomial* identity: both sides are polynomials
in the entries of `A`, and they are equal as polynomials, so they agree on every
substitution over any commutative field. There is no assumption about `det(A)`
anywhere in its statement or proof.

The proof is pure cofactor expansion and does not divide. Expand
`(A adj(A))_ij = Σ_k a_ik · adj(A)_kj`. Since `adj(A)_kj = C_jk`, this is
`Σ_k a_ik C_jk`. When `i = j` this is cofactor expansion of row `i` of `A`,
giving `det(A)`. When `i ≠ j`, it is cofactor expansion of `A` along row `j`
after row `i` has been moved to the top; that move costs `(i−j)` transpositions,
each a sign flip, contributing `(+1)^{i−j}`, while the cofactor contributes
`(−1)^{j+k}`… combining the two gives a matrix with a zero row and hence a
determinant of `0`. So the off-diagonal entries vanish and the diagonal is
`det(A)`.

**What *would* be circular** is stating the identity with `det(A) ≠ 0` as a
hypothesis, because then to prove "invertibility follows from `det(A) ≠ 0`" you
would need the identity on matrices you have not yet established to be
nonsingular. Stating it unconditionally is what lets the proof go through, and the
code separates the two: it computes `adjugate(S3)` and `matmul(S3, adjugate(S3))`
for the *singular* matrix `S3` without complaint, obtaining the zero matrix,
which is `det(S3) I = 0 I`.

The division happens exactly once, afterwards, and only there does the hypothesis
`det(A) ≠ 0` appear. So the structure of the argument is: unconditional identity →
conditional division → conditional existence of the inverse. Each step uses only
what the previous step established. The general pattern — state the algebraic
identity without assumptions, and put the division at the end — is worth copying;
it is why `adj(A)` is defined for singular matrices rather than only for
invertible ones.

</details>

**Q3. A student claims that `det` is "the volume of the parallelepiped formed by
the rows of `A`". Give the full correction, including why the sign matters and
what happens in the degenerate case.**

<details>
<summary>Model answer</summary>

The statement is right up to the sign and the shape of the argument. Precisely:

- The parallelepiped is spanned by the **columns** of `A` as vectors from the
  origin — though this equals the one spanned by the rows, because `det(Aᵀ) =
  det(A)`, so the student's choice is harmless.
- Its `n`-dimensional **volume** is `|det(A)|`, not `det(A)`. Volume is a
  nonnegative number; the determinant may be negative.
- `det(A)` is the **signed** volume: positive when the ordered basis
  `(col_1, …, col_n)` has the same orientation as the standard basis, negative
  when it has the opposite.

The sign is not a technicality, and the Leibniz formula is what shows why. Expand
the unit cube's images: each of the `n!` permutations indexes one simplex, and
`sgn(σ) = +1` for the permutations preserving orientation, `−1` for those
reversing it. The even and odd simplices tile the parallelepiped in two
half-volume sets, so the signed sum is exactly the volume with a `+` or `−`
attached. The code demonstrates the geometry directly: `G1 = [[2,0],[0,3]]` sends
the unit square's corners to `(0,0), (2,0), (2,3), (0,3)`, shoelace signed area
`6 = det(G1)`, counterclockwise preserved. `G2 = [[1,2],[2,1]]` sends them to
`(0,0), (1,2), (3,3), (2,1)`, shoelace signed area `−3 = det(G2)` — the same
order of points, now walked clockwise, so the map turned the square over like a
glove.

The degenerate case is where the claim needs the most care. When `det(A) = 0` the
parallelepiped has **zero** `n`-dimensional volume — it is flat. It is not empty,
and it is not zero-dimensional: `G3 = [[1,1],[1,1]]` sends the unit square's
corners to `(0,0), (1,1), (2,2), (1,1)`, four collinear points lying on the line
`y = x`. The image is a line segment, which has `1`-dimensional volume 1 and
`2`-dimensional volume 0. So "volume zero" is a statement about the *wrong*
dimension, and `A` is not the zero matrix: it still moves points, just not
independently in every direction.

That is exactly why `det(A) = 0` is the invertibility criterion. The transformation
`A` is invertible on `ℝⁿ` if and only if it is a bijection of `ℝⁿ`, and a linear
map is a bijection exactly when its columns stay independent — exactly when the
flat object they span has full dimension — exactly when `det(A) ≠ 0`.

</details>

**Q4. Why is `det(AB) = det(A) det(B)` the property that makes the determinant
worth computing, and what breaks if you try to use it as a computational shortcut
on a large sparse matrix?**

<details>
<summary>Model answer</summary>

**Why it earns its keep.** It makes the determinant the *scale factor* of a
transformation rather than an arbitrary function of a grid. Volume satisfies
`vol(A(BS)) = |det A| · |det B| · vol(S)` because applying `B` then `A` scales
volume twice, and composition of scalings multiplies. So any candidate for "the
determinant" must satisfy multiplicativity, and it is the volume argument that
identifies it uniquely (up to the sign convention) — Leibniz's formula is the
proof that the `n!` signed simplices tile exactly once.

The sign also composes correctly, which the code checks: `P = [[1,2],[3,4]]` and
`Q = [[5,6],[7,8]]` both have `det = −2`, so `det(PQ) = (+4) > 0`. Two
orientation-reversing maps compose to an orientation-preserving one. You cannot
see that from either determinant alone, and it is a genuine fact about geometry
rather than bookkeeping.

**What breaks.** Two things, and the second is fatal.

First, cost and conditioning. `det(A) det(B)` requires forming both determinants
numerically and then dividing — two `O(n³)` factorisations plus a quotient of two
possibly-tiny numbers, which amplifies both relative errors by `1/|det|`. If
`A` is nearly singular (exactly when you care most) the quotient is garbage.
Computing `det(AB)` directly is `O((n+m)^{2.1})` to `(n+m)³` and involves no
division at all.

Second, and decisively for sparse matrices, range. A large sparse matrix, say a
`10⁵ × 10⁵` web-graph matrix, has a determinant whose magnitude is astronomically
far outside double precision — anywhere from underflow to `0.0` to overflow to
`inf`. The code's `slogdet` table shows the underflow case with a mere `3 × 3`:
`A * 1e-110` reports `det = 0.0` from `np.linalg.det` while `np.linalg.slogdet`
reports sign `+1` and `log|det| = −757.6559`. Scale a matrix down by a constant
and you can force underflow with no change in its structure whatsoever.

The fix is to keep the determinant in log form. Since `log(det(AB)) = log(det A) +
log(det B)`, a computation needing `det(P)^k` — a random walk, a Markov chain
normalisation, a PageRank damping constant — should use `k · slogdet(P)[1]`, which
is a single `O(n³)` factorisation reused `k` times. The code verifies the identity
holds there: `slogdet(A) + slogdet(A)` and `slogdet(A @ A)` both give
`(+1, 4.3944)`.

So multiplicativity is what makes the determinant conceptually central and
simultaneously what makes computing it by factorisation the wrong instinct. Use
the identity in your head; use LU, `slogdet`, and `cond` in your code.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — cofactor expansion of a 4×4, twice.** For

    A = | 2  1  1  0 |
        | 1  3  0  1 |
        | 0  1  4  1 |
        | 1  0  1  5 |

(a) compute `det(A)` by expanding along row 0; (b) compute `det(A)` by expanding
along column 3; (c) confirm your two answers with a third method — Gaussian
elimination, reading the determinant off the pivots — and say in one sentence why
the three must agree.

<details>
<summary>Solution</summary>

**(a) Along row 0.** The signs are `+ − + −`. Each minor is `3 × 3`, so expand
each one along its own first row.

`M₀₀` (delete row 0, column 0):

    | 3  0  1 |
    | 1  4  1 |
    | 0  1  5 |

`= 3·(4·5 − 1·1) − 0·(1·5 − 1·0) + 1·(1·1 − 4·0) = 3·19 − 0 + 1 = 58`.
Sign `(+1)`, so `C₀₀ = 58` and the term is `2 · 58 = 116`.

`M₀₁` (delete row 0, column 1):

    | 1  0  1 |
    | 0  4  1 |
    | 1  1  5 |

`= 1·(4·5 − 1·1) − 0·(0·5 − 1·1) + 1·(0·1 − 4·1) = 19 − 0 + (0 − 4) = 15`.
Sign `(−1)`, so `C₀₁ = −15` and the term is `1 · (−15) = −15`.

`M₀₂` (delete row 0, column 2):

    | 1  3  1 |
    | 0  1  1 |
    | 1  0  5 |

`= 1·(1·5 − 1·0) − 3·(0·5 − 1·1) + 1·(0·0 − 1·1) = 5 − 3·(−1) + (−1) = 7`.
Sign `(+1)`, so `C₀₂ = 7` and the term is `1 · 7 = 7`.

`M₀₃` (delete row 0, column 3):

    | 1  3  0 |
    | 0  1  4 |
    | 1  0  1 |

`= 1·(1·1 − 4·0) − 3·(0·1 − 4·1) + 0·(0·0 − 1·1) = 1 − 3·(−4) + 0 = 13`.
Sign `(−1)`, so `C₀₃ = −13`. The entry `a₀₃ = 0`, so the term is `0 · (−13) = 0`.

Total: `116 − 15 + 7 + 0 = 108`. So **`det(A) = 108`**.

**(b) Along column 3.** The entries are `0, 1, 1, 5` at rows 0 to 3, with signs
`(−1)^{i+3}` for `i = 0,1,2,3` giving `−, +, −, +`. Two of the four minors were
already computed in (a).

`i = 0`: minor `M₀₃` has `det = 13`, sign `−`, so `C₀₃ = −13`. Entry `a₀₃ = 0`,
term `0`.

`i = 1`: delete row 1 and column 3, leaving

    | 2  1  1 |
    | 0  1  4 |
    | 1  0  1 |

`= 2·(1·1 − 4·0) − 1·(0·1 − 4·1) + 1·(0·0 − 1·1) = 2·1 − (−4) + (−1) = 5`.
Sign `(+1)`, so `C₁₃ = 5` and the term is `1 · 5 = 5`.

`i = 2`: delete row 2 and column 3, leaving

    | 2  1  1 |
    | 1  3  0 |
    | 1  0  1 |

`= 2·(3·1 − 0·0) − 1·(1·1 − 0·1) + 1·(1·0 − 3·1) = 6 − 1 + (−3) = 2`.
Sign `(−1)`, so `C₂₃ = −2` and the term is `1 · (−2) = −2`.

`i = 3`: delete row 3 and column 3, leaving

    | 2  1  1 |
    | 1  3  0 |
    | 0  1  4 |

`= 2·(3·4 − 0·1) − 1·(1·4 − 0·0) + 1·(1·1 − 3·0) = 24 − 4 + 1 = 21`.
Sign `(+1)`, so `C₃₃ = 21` and the term is `5 · 21 = 105`.

Total: `0 + 5 − 2 + 105 = 108`. Same as (a). ✓

**(c) By elimination.** Start from `A`, and never scale a row, so the determinant
is the product of the pivots times `(−1)^{swaps}`.

Clear column 0:

    R_1 <- R_1 - (1/2) R_0   ->  [0, 5/2, -1/2, 1]
    R_3 <- R_3 - (1/2) R_0   ->  [0, -1/2, 1/2, 5]

giving

    | 2    1    1    0 |
    | 0   5/2 -1/2   1 |
    | 0    1    4    1 |
    | 0  -1/2  1/2   5 |

Clear column 1 (pivot `5/2` is already the largest magnitude in that column below
row 1, so no swap):

    R_2 <- R_2 - (2/5) R_1   ->  [0, 0, 4 + 1/5,  1 - 2/5]  =  [0, 0, 21/5,  3/5]
    R_3 <- R_3 + (1/5) R_1   ->  [0, 0, 1/2 - 1/10, 5 + 1/5] =  [0, 0,  2/5, 26/5]

Clear column 2 (pivot `21/5` already largest, no swap):

    R_3 <- R_3 - (2/21) R_2   ->  last entry  26/5 - (2/21)(3/5) = 26/5 - 2/35 = 180/35 = 36/7

So `U` is upper triangular with **zero row swaps** and pivots
`2, 5/2, 21/5, 36/7`. The determinant is the diagonal product:

    det(A) = 2 · (5/2) · (21/5) · (36/7)
           = (2 · 5 · 21 · 36) / (2 · 5 · 7)
           = 2 · 3 · 36
           = 216 / 2
           = 108   ✓

**(c) continued — why all three agree.** They must, because all three are
computations of the *same* function: cofactor expansion along row 0, along
column 3, and the pivot product from LU are three routes to `det(A)`, and the
elimination route agrees with cofactor expansion because each of its three
operations is a determinant-preserving row operation. Any disagreement means an
arithmetic error, which is exactly why doing it twice is worth doing.

</details>

**[ ] Exercise 2 — the adjugate of a 2×2, and why the transpose is not optional.**
For `A = [[a, b], [c, d]]`, write down `adj(A)` in closed form, then evaluate it
for `A = [[4, 7], [2, 6]]` and check `A·adj(A) = det(A)·I`.

<details>
<summary>Solution</summary>

**(a) Closed form.** The cofactor matrix is

    C = | C₀₀ C₀₁ |  =  |  d   −c |
        | C₁₀ C₁₁ |     | −b    a |

because `C₀₀ = det[[d]] = d`, `C₀₁ = −det[[c]] = −c`, `C₁₀ = −det[[b]] = −b`,
`C₁₁ = det[[a]] = a`. Transposing gives

    adj(A) = |  d  −b |      and      det(A) = ad − bc
             | −c   a |

so

    A⁻¹ = 1/(ad − bc) · |  d  −b |
                           | −c   a |

which is the familiar 2×2 inverse with the diagonal entries swapped and the
off-diagonal entries negated.

**(b) Evaluate.** For `A = [[4, 7], [2, 6]]`, `det(A) = 4·6 − 7·2 = 24 − 14 = 10`.

    adj(A) = | 6  −7 |     and     A⁻¹ = | 0.6  −0.7 |
             | −2   4 |              | −0.2  0.4 |

**(c) Verify.** `A · adj(A)`:

- `(0,0)`: `4·6 + 7·(−2) = 24 − 14 = 10` ✓
- `(0,1)`: `4·(−7) + 7·4 = −28 + 28 = 0` ✓
- `(1,0)`: `2·6 + 6·(−2) = 12 − 12 = 0` ✓
- `(1,1)`: `2·(−7) + 6·4 = −14 + 24 = 10` ✓

So `A adj(A) = 10 I = det(A) I`.

Note the transpose mattered: the cofactor matrix of `A` is `[[6, −2], [−7, 4]]`,
which is a *different* matrix from `adj(A) = [[6, −7], [−2, 4]]`. Using the
cofactor matrix directly would give a wrong "inverse" that still multiplies out to
`10 I` in only two of the four positions.

</details>

**[ ] Exercise 3 — what `det(A) = 0` does and does not determine.** Let

    A = | 1  2  0 |
        | 2  4  0 |
        | 0  0  5 |

(a) Compute `det(A)`. (b) Characterise all `b` for which `Ax = b` has a solution,
and give the general solution for such a `b`. (c) Give an explicit `b` with no
solution. (d) Compute `adj(A)` and show that `adj(A)` does not rescue the
situation.

<details>
<summary>Solution</summary>

**(a)** Expand along row 0, signs `+ − +`:

`det(A) = 1·det[[4,0],[0,5]] − 2·det[[2,0],[0,5]] + 0·det[[2,4],[0,0]]`
`= 1·(4·5 − 0·0) − 2·(2·5 − 0·0) + 0`
`= 20 − 20 + 0 = 0`.

**(b)** `Ax = b` with `A` block-diagonal `diag(M, 5)` where `M = [[1,2],[2,4]]`:

- rows 2 and 3 of the system are `0 = b₂` and `5x₃ = b₃`, so `b₂ = 0` is required
  and `x₃ = b₃/5`.
- rows 0 and 1 are `x₁ + 2x₂ = b₀` and `2x₁ + 4x₂ = b₁`. The second left-hand side
  is twice the first, so consistency needs `b₁ = 2b₀`. When it holds, `x₁ = b₀ −
  2x₂` and `x₂` is free.

So: solutions exist **iff** `b₁ = 2b₀` **and** `b₂ = 0`. The general solution is

    x = (b₀ − 2t, t, b₃/5),   t ∈ ℝ

a one-parameter family, i.e. infinitely many. (Compare
[lesson 32](32_linear_systems_gaussian_elimination.md), where the free variable is
read off the pivot pattern.)

**(c)** `b = (1, 2, 5)` works, but `b = (1, 0, 5)` does not: `b₁ = 0 ≠ 2·1 = 2b₀`,
so the equations `x₁ + 2x₂ = 1` and `2x₁ + 4x₂ = 0` contradict — the second demands
`2(x₁ + 2x₂) = 0`, i.e. `x₁ + 2x₂ = 0`. Equally, `b = (1, 2, 1)` fails on `b₂ = 0`.
Two independent reasons for failure in the same matrix, which is a useful thing
to see.

**(d)** The cofactors:

- `C₀₀ = det[[4,0],[0,5]] = 20`
- `C₀₁ = −det[[2,0],[0,5]] = −10`
- `C₀₂ = +det[[2,4],[0,0]] = 0`
- `C₁₀ = −det[[2,0],[0,5]] = −10`
- `C₁₁ = +det[[1,0],[0,5]] = 5`
- `C₁₂ = −det[[1,2],[0,0]] = 0`
- `C₂₀ = +det[[2,0],[4,0]] = 0`
- `C₂₁ = −det[[1,0],[2,0]] = 0`
- `C₂₂ = +det[[1,2],[2,4]] = 4 − 4 = 0`

    C = | 20  −10   0 |      adj(A) = Cᵀ = | 20  −10   0 |
        | −10   5   0 |                    | −10   5   0 |
        |  0    0   0 |                    |  0    0   0 |

`A · adj(A)`: row 0 of `A` is `[1, 2, 0]` and row 0 of `adj(A)` is `[20, −10, 0]`, so
row 0 of the product is `[20 − 20, −10 + 10, 0] = [0, 0, 0]`. Row 1 of `A` is twice
row 0, so its product row is also `[0, 0, 0]`. Row 2 is `[0, 0, 5]` times a zero
row, also zero. Hence

    A adj(A) = 0 = det(A) I

exactly as the adjugate identity predicts. The identity holds — but it is now a
statement about nothing, since the left-hand side is the zero matrix whatever
`adj(A)` had been. Dividing by `det(A) = 0` is what fails, and `A` has no inverse.

Note the shape of `adj(A)` here: rank 1, with every row but one proportional to
`(2, −1, 0)`. This is the general shape of the adjugate of a singular matrix —
it encodes the dependence relation rather than an inverse, and for `n ≥ 2` its
rank is exactly `n − 1` if the rank of `A` is `n − 1`, and `0` otherwise.

</details>

**[ ] Exercise 4 — determinant as a volume scale factor, checked by hand.** Let
`G = [[3, 1], [0, 2]]`. (a) Apply `G` to the unit square and find the area of the
image by the shoelace formula. (b) Compare with `det(G)` and explain the
disagreement, if any. (c) Now let `H = [[3, 1], [0, −2]]` and repeat, explaining
what the sign change does to the picture.

<details>
<summary>Solution</summary>

**(a)** The unit square's corners in counterclockwise order are
`(0,0), (1,0), (1,1), (0,1)`. Their images:

- `(0,0) → (3·0 + 1·0, 0·0 + 2·0) = (0, 0)`
- `(1,0) → (3, 0)`
- `(1,1) → (4, 2)`
- `(0,1) → (1, 2)`

Shoelace over `(0,0), (3,0), (4,2), (1,2)`:
`Σ (x_i y_{i+1} − x_{i+1} y_i) = (0·0 − 3·0) + (3·2 − 4·0) + (4·2 − 1·2) + (1·0 − 0·2)`
`= 0 + 6 + 6 + 0 = 12`, so signed area `12/2 = 6`.

**(b)** `det(G) = 3·2 − 1·0 = 6`. **They agree exactly**, and the signed area is
positive because the images still run counterclockwise. Geometrically: `G`
stretches horizontally by 3 and vertically by 2, so areas scale by `3 · 2 = 6`.
The code's `G1 = [[2,0],[0,3]]` case is the same phenomenon with the factors
swapped, giving shoelace area `6` and `det = 6`.

**(c)** `H` differs from `G` only in the sign of the bottom-right entry.

- `(0,0) → (0,0)`
- `(1,0) → (3, 0)`
- `(1,1) → (4, −2)`
- `(0,1) → (1, −2)`

Shoelace over `(0,0), (3,0), (4,−2), (1,−2)`:
`(0·0 − 3·0) + (3·(−2) − 4·0) + (4·(−2) − 1·(−2)) + (1·0 − 0·(−2))`
`= 0 + (−6) + (−8 + 2) + 0 = 0 − 6 − 6 + 0 = −12`, signed area `−6`.

`det(H) = 3·(−2) − 1·0 = −6`. Agreement again, but now negative. The unsigned area
is still `6` — stretching by 3 and by 2 — while the sign records that the corner
order came out **clockwise**. Visually, `H` reflects the plane across the
horizontal axis (stretch ×3, flip, stretch ×2), and a reflection reverses
orientation. This is precisely the code's `G2 = [[1,2],[2,1]]` case, where
`det = −3` and the shoelace area is `−3`: same area, opposite winding.

So the pattern across all three examples is one rule: `|det|` is the area scale
factor, and the sign is the orientation, and the shoelace formula measures both at
once because it is itself a signed area.

</details>

**[ ] Exercise 5 — `det(AB) = det(A)det(B)` on a case where `AB ≠ BA`.** Let

    A = | 1  2 |      B = | 0  1 |
        | 0  1 |          | 1  0 |

(a) Compute `AB` and `BA`. (b) Compute `det(A)`, `det(B)`, `det(AB)` and
`det(BA)`. (c) Verify multiplicativity in both orders and comment on what this
says about the relationship between the determinant and non-commutativity.

<details>
<summary>Solution</summary>

**(a)** `A` is upper triangular and `B` is the transposition matrix.

`AB = |1·0 + 2·1, 1·1 + 2·0; 0·0 + 1·1, 0·1 + 1·0| = |2  1; 1  0|`.

`BA = |0·1 + 1·0, 0·2 + 1·1; 1·1 + 0·0, 1·2 + 0·1| = |0  1; 1  2|`.

So `AB ≠ BA`, as expected: `AB` is upper triangular while `BA` is lower.

**(b)** `det(A) = 1·1 − 2·0 = 1`. `det(B) = 0·0 − 1·1 = −1`.
`det(AB) = 2·0 − 1·1 = −1`. `det(BA) = 0·2 − 1·1 = −1`.

**(c)** `det(A)det(B) = 1·(−1) = −1 = det(AB)` ✓
and `det(B)det(A) = (−1)·1 = −1 = det(BA)` ✓.

Both hold. Now the interesting part: `AB ≠ BA`, yet `det(AB) = det(BA)`. The
determinant is not sensitive to order at all, because it is a *scale factor* and
scale factors multiply commutatively. What the determinant cannot tell you, and
what `AB ≠ BA` shows, is that the two products are different maps: `AB` sends
`(1,0)` to `(2,1)` while `BA` sends it to `(0,1)`. They scale area identically
(so `det` agrees) while pointing in different directions (so `AB ≠ BA`).

This is the honest limit of what the determinant knows. It is a complete invariant
for the *magnitude* of a transformation's effect on volume, and no information at
all about the rotation or shear part. To recover that you need eigenvalues,
singular values, or the polar decomposition —
[lesson 39](39_diagonalization_and_spectral.md) and
[lesson 40](40_svd_and_pca.md).

</details>

**[ ] Exercise 6 — a rank story told by determinants.** Let

    A = | 1  2  3  4 |
        | 2  4  6  8 |      (row 1 = 2 · row 0)
        | 1  1  1  1 |
        | 0  1  2  3 |

(a) Find `det(A)`. (b) Find a nonzero `v` with `Av = 0`. (c) Find all solutions
of `Av = 0`. (d) Explain why the determinant alone cannot distinguish `A` from the
zero matrix, and what does.

<details>
<summary>Solution</summary>

**(a)** Row 1 is twice row 0, so eliminate it: `R₁ ← R₁ − 2R₀` produces a zero row.
That operation leaves the determinant unchanged, and a matrix with a zero row has
determinant `0` — expand along that row and every term is `0 · (cofactor)`. So
`det(A) = 0`.

The same fact seen through cofactors: every cofactor `C₁ⱼ` is the determinant of a
`3 × 3` minor obtained by deleting row 1 and column `j`, and every such minor
still contains row 0 intact plus one of rows 2 and 3. Those rows are not
proportional in general, so this argument alone does not force the minors to
vanish. The cofactors `C₂ⱼ` and `C₃ⱼ` do vanish, though: their minors contain both
rows 0 and 1, which are proportional, so each is `0`. Either way the expansion
along row 1 gives `det(A) = 0`.

**(b)** Reduce `A` by elimination, which is determinant-preserving at every step.
The rows are `r₀ = (1,2,3,4)`, `r₁ = (2,4,6,8) = 2r₀`, `r₂ = (1,1,1,1)`,
`r₃ = (0,1,2,3)`.

    R_1 <- R_1 - 2 R_0      ->   0  0  0  0
    R_2 <- R_2 - R_0        ->   0 -1 -2 -3
    R_3                     ->   0  1  2  3      (first entry already 0)

Swap rows 1 and 2, then add, and the two remaining rows cancel:

    R_1 <-> R_2             ->   | 1  2  3  4 |
                                 | 0  1  2  3 |
                                 | 0  0  0  0 |
                                 | 0 -1 -2 -3 |
    R_3 <- R_3 + R_1        ->   | 1  2  3  4 |
                                 | 0  1  2  3 |
                                 | 0  0  0  0 |
                                 | 0  0  0  0 |

Finally `R_0 ← R_0 − 2R_1`, and the RREF is

    | 1  0  -1  -2 |
    | 0  1   2   3 |
    | 0  0   0   0 |
    | 0  0   0   0 |

Read off the equations. The first row says `x₀ − x₂ − 2x₃ = 0`, so
`x₀ = x₂ + 2x₃`. The second says `x₁ + 2x₂ + 3x₃ = 0`, so `x₁ = −2x₂ − 3x₃`.
Columns 2 and 3 have no pivot, so both are free.

Set `x₂ = 0`, `x₃ = 1`: **`v = (2, −3, 0, 1)`**.

Verify by direct multiplication, row by row:

- row 0: `1·2 + 2·(−3) + 3·0 + 4·1 = 2 − 6 + 0 + 4 = 0` ✓
- row 1: `2·2 + 4·(−3) + 6·0 + 8·1 = 4 − 12 + 0 + 8 = 0` ✓
- row 2: `1·2 + 1·(−3) + 1·0 + 1·1 = 2 − 3 + 0 + 1 = 0` ✓
- row 3: `0·2 + 1·(−3) + 2·0 + 3·1 = 0 − 3 + 0 + 3 = 0` ✓

**(c)** `x₂` and `x₃` are both free, so

    ker(A) = { (s + 2t, −2s − 3t, s, t) : s, t ∈ ℝ }
           = span{ (1, −2, 1, 0),  (2, −3, 0, 1) }

Check the first basis vector: `A(1,−2,1,0) = (1−4+3+0, 2−8+6+0, 1−2+1+0,
0−2+2+0) = (0, 0, 0, 0)` ✓, and the second was just verified. They are
independent: the third coordinate of the first forces `s = 0`, and the fourth of
the second forces `t = 0`.

Two free variables means `dim ker(A) = 2`, and since `A` is `4 × 4` the rank is
`4 − 2 = 2` — matching the two pivots found in (b). Note that **two**
dependencies are at work, not one: row 1 being twice row 0 is the obvious
redundancy, but row 3 is *also* redundant, being `−(r₂ − r₀)` up to sign. That is
exactly the kind of detail the determinant cannot report and the pivot count can;
see (d). [Lesson 34](34_basis_dimension_rank.md) makes this bookkeeping
systematic, and [lesson 35](35_linear_transformations_and_kernels.md) proves
`rank + nullity = n` as a theorem rather than a coincidence.

**(d)** The determinant cannot distinguish `A` from the zero matrix, because both
have `det = 0`. It cannot distinguish rank 3 from rank 1, nor rank 1 from rank 0.
It is one number standing in for an `n²`-dimensional object, so almost all of the
information is necessarily thrown away.

What distinguishes them is the **rank**: the number of pivots after row reduction,
equivalently `n − dim ker(A)`, equivalently `dim im(A)`. The lesson's
`determinant_lu` is blunt here — it returns `0.0` the instant it fails to find a
pivot, and `0.0` is compatible with rank `0, 1, …, n−1` alike. For this `A`,
`det = 0` narrows things only to "rank < 4", while the pivot count pins it down to
"rank = 2".

The two invariants measure genuinely different things, and neither determines the
other. Rank counts directions retained, so `I₄` and `diag(1,1,1,10⁻⁹)` both have
rank 4 while their determinants are `1` and `10⁻⁹` — a nine-order-of-magnitude
spread invisible to the rank. The determinant is the total volume scale, so it is
sensitive to every direction at once, which is exactly why it collapses to a single
uninformative `0` the moment *any* direction is lost. The lesson's cofactor matrix
shows the third case: for the singular `S3` of the third code block, `det = 0` and
`adj(S3) = 0`, so not one digit of the dependence structure survives in the
determinant, while the pivot count recovers it exactly.

**Challenge.** Let

    A  = | 2  1  0 |     S2 = | 1  2  3 |     S1 = | 1  2  3 |
         | 1  2  1 |          | 2  4  6 |          | 2  4  6 |
         | 0  1  2 |          | 1  1  1 |          | 3  6  9 |

(a) For `A`: compute `det(A)` and `adj(A)`, then form `A⁻¹` **twice** — as
`adj(A)/det(A)` and by Gaussian elimination on `[A | I]` — and confirm the two
agree and that `A A⁻¹ = I`. Then verify `A adj(A) = det(A) I` directly and say in
one sentence what that identity is doing for you.

(b) For `S2`: compute `det(S2)`, `adj(S2)`, and `S2 adj(S2)`. Show that
`adj(S2)` is **not** the zero matrix even though `S2` is singular, relate its
columns to `ker(S2)`, and confirm that `S2 adj(S2) = det(S2) I` still holds.
Explain in one sentence what that identity is worth once `det = 0`.

(c) For `S1`: show that `adj(S1)` is exactly the zero matrix and explain why
`rank(S1) = 1` forces that. Then tabulate all three matrices by `det`, rank, and
the number of nonzero entries in `adj`.

(d) Run Cramer's rule on `A x = (1, 0, 1)` and check the result against `A x = b`.
Then run the same move on `S2 x = (1, 0, 1)`, and explain in one paragraph what
breaks — being precise about `k/0` versus `0/0` — and name the one piece of
information the determinant has thrown away that you now need.

**(a)** Expanding along row 0: `2(2·2 − 1·1) − 1(1·2 − 1·0) + 0 = 2·3 − 2 = 4`. So
`det(A) = 4 ≠ 0` and the matrix is invertible. The cofactor matrix is

    |  3  -2   1 |
    | -2   4  -2 |
    |  1  -2   3 |

and the adjugate is its **transpose**. Here the cofactor matrix happens to be
symmetric, so the transpose is invisible — which is exactly why Exercise 2 had to
reach for a `2 × 2`, where it is not. Dividing by `4` and eliminating on
`[A | I]` give the same matrix to the last digit,

    | 0.75  -0.50   0.25 |
    |-0.50   1.00  -0.50 |
    | 0.25  -0.50   0.75 |

and multiplying `A` by it returns the identity exactly.

What the identity `A adj(A) = det(A) I` is doing for you: it is the algebraic
license to divide. Without it, `adj(A)` is just a matrix of cofactors with no
claim to invert anything. With it, both `A adj(A)` and `adj(A) A` are *known* to
be the same scalar multiple of `I`, so dividing both by `det(A)` hands you a
**two-sided** inverse for free — you never have to check the second product
separately. That is the entire content of the inverse formula.

**(b)** `rank(S2) = 2`, so `det(S2) = 0`, yet

    adj(S2) = | -2   1   0 |
              |  4  -2   0 |
              | -2   1   0 |

is emphatically not zero. The reason is worth knowing: the null vector of `S2`
is `(1, −2, 1)`, and **every column of `adj(S2)` is a multiple of it** — columns
`−2·(1,−2,1)`, `1·(1,−2,1)` and `0`. For a matrix of rank exactly `n − 1` the
adjugate has rank `1` and points along the single direction that was lost. So
the dependence information is not destroyed by `det = 0`; it has simply moved
somewhere the inverse formula cannot reach it.

And `S2 adj(S2)` is the zero matrix, so the identity `S2 adj(S2) = det(S2) I`
still holds. That is the whole story: when `det = 0` the identity degenerates to
`0 = 0`. It constrains nothing, divides into nothing, and the "inverse" you
computed is a matrix whose entire image is a single direction. Gaussian
elimination says the same thing more bluntly — it refuses to run, reporting no
pivot in the second column.

**(c)** `adj(S1)` is the zero matrix, entry by entry. The reason is dimensional
rather than accidental: a `3 × 3` adjugate is built from `2 × 2` minors, and
`S1` has rank `1 ≤ 3 − 2`, so every `2 × 2` minor vanishes and so does the whole
adjugate. One more row of dependence and the last trace of structure is gone.

The three cases together:

| matrix | `det` | rank | nonzero entries in `adj` | invertible |
|---|---|---|---|---|
| `A` | `4` | 3 | 9 | yes |
| `S2` | `0` | 2 | 6 | no |
| `S1` | `0` | 1 | 0 | no |

`det` distinguishes the first row from the other two and says **nothing** about
the difference between the second and third. It is one bit, and `S2` and `S1` are
on the same side of it. `rank` is the quantity that separates them.

**(d)** Cramer's rule on `A`: the three replaced-column determinants come out
`4, −4, 4`, so dividing by `det(A) = 4` gives `x = (1, −1, 1)`, and
`A(1, −1, 1) = (1, 0, 1)` — correct.

On `S2` the denominators are all `0`, and the numerators are `−2, 4, −2`, none of
them zero. So each expression is `k/0` with `k ≠ 0`: **undefined, not zero**. The
distinction matters. `0/0` is indeterminate, and one might hope the system has a
consistent family of answers hiding in it; `k/0` with `k ≠ 0` rules that out
immediately, because replacing a column with `b` and getting a nonzero determinant
means `b` left the column space. What is lost is precisely the *consistency*
information: whether `S2 x = b` is solvable at all, or solvable with infinitely
many solutions. `det` reports "singular" for both cases and cannot separate them.

So the division is not a detail to be tidied away. Cancelling a factor of `det`,
or "simplifying" `adj/det` into a single expression, is legal only when you have
already established `det ≠ 0` — and establishing that is the entire job. The step
that looks like algebra is the step that silently throws away the distinction
between *no solution* and *infinitely many*.

```python
TOL = 1e-9


# ---------------------------------------------------------------- helpers
def shape(M):
    return len(M), len(M[0])


def matmul(A, B):
    ra, ca = shape(A)
    rb, cb = shape(B)
    if ca != rb:
        raise ValueError(f"cannot multiply {ra}x{ca} by {rb}x{cb}")
    return [[sum(A[i][k] * B[k][j] for k in range(ca)) for j in range(cb)]
            for i in range(ra)]


def matvec(M, v):
    return [sum(M[i][k] * v[k] for k in range(len(v))) for i in range(len(M))]


def det(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]
    total = 0.0
    for j in range(n):
        minor = [[M[i][c] for c in range(n) if c != j] for i in range(1, n)]
        sign = 1.0 if j % 2 == 0 else -1.0
        total += sign * M[0][j] * det(minor)
    return total


def cofactor(M, i, j):
    n = len(M)
    minor = [[M[r][c] for c in range(n) if c != j] for r in range(n) if r != i]
    sign = 1.0 if (i + j) % 2 == 0 else -1.0
    return sign * det(minor)


def adjugate(M):
    """The TRANSPOSE of the cofactor matrix -- the transpose is the whole point."""
    n = len(M)
    # + 0.0 normalises -0.0 to 0.0 so the printout does not show "-0.00".
    return [[cofactor(M, j, i) + 0.0 for j in range(n)] for i in range(n)]


def rref(A, tol=TOL):
    M = [list(row) for row in A]
    rows, cols = len(M), len(M[0])
    pr, pivots = 0, []
    for col in range(cols):
        if pr == rows:
            break
        best = max(range(pr, rows), key=lambda r: abs(M[r][col]))
        if abs(M[best][col]) <= tol:
            continue
        M[pr], M[best] = M[best], M[pr]
        p = M[pr][col]
        M[pr] = [v / p for v in M[pr]]
        for r in range(rows):
            if r != pr and M[r][col] != 0.0:
                f = M[r][col]
                M[r] = [M[r][c] - f * M[pr][c] for c in range(cols)]
        pivots.append(col)
        pr += 1
    return [[v + 0.0 for v in row] for row in M], pivots


def rank(A, tol=TOL):
    return len(rref(A, tol)[1])


def null_space(A, tol=TOL):
    M, pivots = rref(A, tol)
    cols = len(A[0])
    basis = []
    for fc in [c for c in range(cols) if c not in pivots]:
        v = [0.0] * cols
        v[fc] = 1.0
        for i, pc in enumerate(pivots):
            v[pc] = -M[i][fc]
        basis.append(v)
    return basis


def eye(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def inverse_by_elimination(M, tol=TOL):
    n = len(M)
    aug = [list(M[i]) + [1.0 if i == j else 0.0 for j in range(n)]
           for i in range(n)]
    for col in range(n):
        best = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[best][col]) <= tol:
            raise ValueError("matrix is singular: no pivot in this column")
        aug[col], aug[best] = aug[best], aug[col]
        p = aug[col][col]
        aug[col] = [v / p for v in aug[col]]
        for r in range(n):
            if r != col and aug[r][col] != 0.0:
                f = aug[r][col]
                aug[r] = [aug[r][c] - f * aug[col][c] for c in range(2 * n)]
    return [row[n:] for row in aug]


def print_matrix(label, M, width=6):
    rows, cols = shape(M)
    print(f"  {label}  ({rows}x{cols})")
    for row in M:
        print("    | " + " ".join(f"{x:{width}.2f}" for x in row) + " |")


def show(label, v, width=6):
    print(f"  {label} = [" + ", ".join(f"{x:{width}.4f}" for x in v) + "]")


A = [[2.0, 1.0, 0.0],
     [1.0, 2.0, 1.0],
     [0.0, 1.0, 2.0]]

print("=== (a) A: invertible, three routes to A^-1 must agree ===")
print_matrix("A", A)
dA = det(A)
adjA = adjugate(A)
print(f"  det(A) = {dA:g}   (row expansion: 2*3 - 1*2 + 0*1 = {2 * 3 - 1 * 2})")
print_matrix("adj(A)", adjA)
inv_formula = [[adjA[i][j] / dA for j in range(3)] for i in range(3)]
inv_elim = inverse_by_elimination(A)
print_matrix("adj(A)/det(A)", inv_formula)
print_matrix("by elimination", inv_elim)
print(f"  the two agree: {all(abs(inv_formula[i][j] - inv_elim[i][j]) <= TOL for i in range(3) for j in range(3))}")
prod = matmul(A, inv_formula)
print_matrix("A (adj(A)/det(A))", prod)
print(f"  that is the identity: {all(abs(prod[i][j] - eye(3)[i][j]) <= TOL for i in range(3) for j in range(3))}")
print()
print("  The identity A adj(A) = det(A) I is the whole reason dividing by det")
print("  works. Verify it directly:")
lhs = matmul(A, adjA)
print_matrix("A adj(A)", lhs)
print_matrix("det(A) I", [[dA if i == j else 0.0 for j in range(3)] for i in range(3)])
print(f"  equal: {all(abs(lhs[i][j] - (dA if i == j else 0.0)) <= TOL for i in range(3) for j in range(3))}")
print(f"  Both sides equal {dA:g} I, so dividing by det(A) = {dA:g} -- legal --")
print("  and the two-sided inverse falls out for free.")

S2 = [[1.0, 2.0, 3.0],
      [2.0, 4.0, 6.0],
      [1.0, 1.0, 1.0]]

print()
print("=== (b) S2: singular, but the adjugate is NOT zero ===")
print_matrix("S2", S2)
dS = det(S2)
adjS = adjugate(S2)
print(f"  rank(S2) = {rank(S2)} of 3, so det(S2) = {dS:g}")
print_matrix("adj(S2)", adjS)
print(f"  adj(S2) is all zero? {all(abs(adjS[i][j]) <= TOL for i in range(3) for j in range(3))}")
print("  Not zero, and the reason is instructive. The null vector of S2 is")
ns = null_space(S2)[0]
show("null vector of S2", ns)
print("  and every COLUMN of adj(S2) is a multiple of it:")
for j in range(3):
    col = [adjS[i][j] for i in range(3)]
    scale = next((col[i] / ns[i] for i in range(3) if abs(ns[i]) > TOL), None)
    print(f"    column {j} = {str([round(t, 4) for t in col]):<22} = "
          f"{scale:g} * null vector")
print("  So for a rank n-1 matrix the adjugate still carries the direction that")
print("  was lost -- it just cannot act as an inverse, since it only spans that")
print("  one direction.")
lhs2 = matmul(S2, adjS)
print_matrix("S2 adj(S2)", lhs2)
print(f"  equal to det(S2) I = the ZERO matrix: "
      f"{all(abs(lhs2[i][j]) <= TOL for i in range(3) for j in range(3))}")
print("  So the identity still holds -- and it now reads 0 = 0, which says")
print("  nothing at all. No division is available and no inverse exists.")
try:
    inverse_by_elimination(S2)
    print("  elimination unexpectedly succeeded")
except ValueError as exc:
    print(f"  elimination on S2 refuses: {exc}")

print()
print("=== (c) S1: also singular, and here adj is exactly zero ===")
S1 = [[1.0, 2.0, 3.0],
      [2.0, 4.0, 6.0],
      [3.0, 6.0, 9.0]]
print_matrix("S1", S1)
dS1 = det(S1)
adjS1 = adjugate(S1)
print(f"  rank(S1) = {rank(S1)} of 3, so det(S1) = {dS1:g}")
print_matrix("adj(S1)", adjS1)
print(f"  adj(S1) is all zero? {all(abs(adjS1[i][j]) <= TOL for i in range(3) for j in range(3))}")
print("  Every 2x2 minor of a rank-1 matrix is 0, and a 3x3 adjugate is made of")
print("  2x2 minors, so adj is the zero matrix outright. Three cases, one det:")
for label, M in (("A  (rank 3)", A), ("S2 (rank 2)", S2), ("S1 (rank 1)", S1)):
    d = det(M)
    a = adjugate(M)
    nz = sum(1 for i in range(3) for j in range(3) if abs(a[i][j]) > TOL)
    print(f"    {label}: det = {d:5g}   nonzero entries of adj = {nz}   "
          f"invertible = {d != 0.0}")

print()
print("=== (d) what breaks if you divide anyway ===")
print("  Cramer's rule for A x = b, with b = (1, 0, 1):")
b = [1.0, 0.0, 1.0]
for i in range(3):
    Mc = [list(row) for row in A]
    for r in range(3):
        Mc[r][i] = b[r]
    print(f"    det(A with column {i} replaced by b) / det(A) = {det(Mc):g} / {dA:g} = {det(Mc) / dA:g}")
x_cramers = [det([[b[r] if c == i else A[r][c] for c in range(3)] for r in range(3)]) / dA
             for i in range(3)]
show("x from Cramer's rule", x_cramers)
print(f"  A x = {matvec(A, x_cramers)}   matches b: "
      f"{all(abs(t) <= TOL for t in [matvec(A, x_cramers)[i] - b[i] for i in range(3)])}")
print()
print("  Now the same Cramer move on S2, whose det is 0. Every numerator comes out")
print("  NONZERO, so each fraction is k/0 with k != 0 -- undefined, not zero:")
for i in range(3):
    Mc = [[b[r] if c == i else S2[r][c] for c in range(3)] for r in range(3)]
    num = det(Mc)
    print(f"    det(S2 with column {i} replaced by b) = {num:g}")
print("  A 0 denominator is not an answer of 0. It means the system is either")
print("  unsolvable or infinitely solvable, and the determinant alone cannot")
print("  say which -- that needs the rank. Never cancel, divide, or 'simplify'")
print("  a factor of det away when det may be 0: the division is the step that")
print("  silently discards the consistency information.")
```

Output:

```
=== (a) A: invertible, three routes to A^-1 must agree ===
  A  (3x3)
    |   2.00   1.00   0.00 |
    |   1.00   2.00   1.00 |
    |   0.00   1.00   2.00 |
  det(A) = 4   (row expansion: 2*3 - 1*2 + 0*1 = 4)
  adj(A)  (3x3)
    |   3.00  -2.00   1.00 |
    |  -2.00   4.00  -2.00 |
    |   1.00  -2.00   3.00 |
  adj(A)/det(A)  (3x3)
    |   0.75  -0.50   0.25 |
    |  -0.50   1.00  -0.50 |
    |   0.25  -0.50   0.75 |
  by elimination  (3x3)
    |   0.75  -0.50   0.25 |
    |  -0.50   1.00  -0.50 |
    |   0.25  -0.50   0.75 |
  the two agree: True
  A (adj(A)/det(A))  (3x3)
    |   1.00   0.00   0.00 |
    |   0.00   1.00   0.00 |
    |   0.00   0.00   1.00 |
  that is the identity: True

  The identity A adj(A) = det(A) I is the whole reason dividing by det
  works. Verify it directly:
  A adj(A)  (3x3)
    |   4.00   0.00   0.00 |
    |   0.00   4.00   0.00 |
    |   0.00   0.00   4.00 |
  det(A) I  (3x3)
    |   4.00   0.00   0.00 |
    |   0.00   4.00   0.00 |
    |   0.00   0.00   4.00 |
  equal: True
  Both sides equal 4 I, so dividing by det(A) = 4 -- legal --
  and the two-sided inverse falls out for free.

=== (b) S2: singular, but the adjugate is NOT zero ===
  S2  (3x3)
    |   1.00   2.00   3.00 |
    |   2.00   4.00   6.00 |
    |   1.00   1.00   1.00 |
  rank(S2) = 2 of 3, so det(S2) = 0
  adj(S2)  (3x3)
    |  -2.00   1.00   0.00 |
    |   4.00  -2.00   0.00 |
    |  -2.00   1.00   0.00 |
  adj(S2) is all zero? False
  Not zero, and the reason is instructive. The null vector of S2 is
  null vector of S2 = [1.0000, -2.0000, 1.0000]
  and every COLUMN of adj(S2) is a multiple of it:
    column 0 = [-2.0, 4.0, -2.0]      = -2 * null vector
    column 1 = [1.0, -2.0, 1.0]       = 1 * null vector
    column 2 = [0.0, 0.0, 0.0]        = 0 * null vector
  So for a rank n-1 matrix the adjugate still carries the direction that
  was lost -- it just cannot act as an inverse, since it only spans that
  one direction.
  S2 adj(S2)  (3x3)
    |   0.00   0.00   0.00 |
    |   0.00   0.00   0.00 |
    |   0.00   0.00   0.00 |
  equal to det(S2) I = the ZERO matrix: True
  So the identity still holds -- and it now reads 0 = 0, which says
  nothing at all. No division is available and no inverse exists.
  elimination on S2 refuses: matrix is singular: no pivot in this column

=== (c) S1: also singular, and here adj is exactly zero ===
  S1  (3x3)
    |   1.00   2.00   3.00 |
    |   2.00   4.00   6.00 |
    |   3.00   6.00   9.00 |
  rank(S1) = 1 of 3, so det(S1) = 0
  adj(S1)  (3x3)
    |   0.00   0.00   0.00 |
    |   0.00   0.00   0.00 |
    |   0.00   0.00   0.00 |
  adj(S1) is all zero? True
  Every 2x2 minor of a rank-1 matrix is 0, and a 3x3 adjugate is made of
  2x2 minors, so adj is the zero matrix outright. Three cases, one det:
    A  (rank 3): det =     4   nonzero entries of adj = 9   invertible = True
    S2 (rank 2): det =     0   nonzero entries of adj = 6   invertible = False
    S1 (rank 1): det =     0   nonzero entries of adj = 0   invertible = False

=== (d) what breaks if you divide anyway ===
  Cramer's rule for A x = b, with b = (1, 0, 1):
    det(A with column 0 replaced by b) / det(A) = 4 / 4 = 1
    det(A with column 1 replaced by b) / det(A) = -4 / 4 = -1
    det(A with column 2 replaced by b) / det(A) = 4 / 4 = 1
  x from Cramer's rule = [1.0000, -1.0000, 1.0000]
  A x = [1.0, 0.0, 1.0]   matches b: True

  Now the same Cramer move on S2, whose det is 0. Every numerator comes out
  NONZERO, so each fraction is k/0 with k != 0 -- undefined, not zero:
    det(S2 with column 0 replaced by b) = -2
    det(S2 with column 1 replaced by b) = 4
    det(S2 with column 2 replaced by b) = -2
  A 0 denominator is not an answer of 0. It means the system is either
  unsolvable or infinitely solvable, and the determinant alone cannot
  say which -- that needs the rank. Never cancel, divide, or 'simplify'
  a factor of det away when det may be 0: the division is the step that
  silently discards the consistency information.
```

</details>

## Summary

- `det(A)` is a single number attached to a square matrix, defined by cofactor
  expansion (`Θ(n!)`) or equivalently by the Leibniz formula over `n!` signed
  permutation terms.
- Geometrically `|det(A)|` is the factor by which `A` multiplies every
  `n`-dimensional volume; the sign records orientation, and `det = 0` means the
  image collapses to a lower-dimensional subspace.
- Three row facts carry the whole practical theory: row addition leaves `det`
  alone, row scaling by `c` multiplies it by `c`, and a row swap negates it — so
  elimination gives `det(A) = (−1)^{swaps} · Π u_ii` in `Θ(n³)`.
- `det(AB) = det(A)det(B)` and `det(Aᵀ) = det(A)` make it the scale factor of the
  transformation; `det(A + B) = det(A) + det(B)` is **false**.
- `det(A) ≠ 0` **iff** `A` is invertible; `det(A) = 0` means "not exactly one
  solution", which may be none or infinitely many — the determinant never sees `b`.
- `adj(A) = Cᵀ` satisfies `A·adj(A) = det(A)·I` for **every** square `A`;
  dividing to get `A⁻¹ = adj(A)/det(A)` is the step that needs `det(A) ≠ 0`.
- Triangular matrices give `det(U) = Π u_ii`, so an LU factorisation hands you the
  determinant for free and no library ever asks for one separately.
- In floating point `det == 0` is not a test: use `solve`, `slogdet`, or
  `np.linalg.cond`, because underflow reports `0.0` for matrices that are
  invertible.

## Next

[34 — Basis, Dimension, and Rank](34_basis_dimension_rank.md) asks the question
the determinant cannot answer. `det(A) = 0` says *that* a matrix is deficient, but
not *how* — and how deficient is the whole content of rank, nullity, and the four
fundamental subspaces that make linear algebra cohere.
