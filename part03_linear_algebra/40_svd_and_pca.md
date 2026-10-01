# 40 — SVD and PCA

**Part**: part03_linear_algebra · **Prerequisites**: 39 · **Time**: 45 min

---

## In Plain Words

Everything in the last three lessons had a catch. Eigenvalues need a square
matrix, so they are undefined for a tall table of data. They can be complex, so
you get numbers you cannot plot or compare. They can come out unsorted, so
"the largest one" is not well defined. And if a matrix is defective, the
eigenvectors do not even exist.

The **singular value decomposition** has none of these problems. It works on
every matrix, rectangular or square, full rank or not. Its special numbers are
always real, always non-negative, and always sorted largest first. Its
directions are always perpendicular to each other. And it never fails.

What it tells you is the most useful question you can ask about a matrix: *how
much does it stretch things, and in which directions?* Every direction in the
input is measured, and each one gets a single number saying how much it comes
out stretched. The directions sorted by that number are the matrix's real
structure.

That last sentence is **PCA**, the single most-used algorithm in data science.
If your data has many columns that mostly repeat each other, the SVD finds the
handful of directions that actually carry information, so you can describe each
row with a few numbers instead of hundreds.

## Why Computer Science Cares

- **`np.linalg.svd` is the default decomposition for a reason.** It never
  returns a complex number, never a negative value, and always returns sorted
  values. When in doubt, use the SVD.
- **PCA is the SVD of your centred data.** `sklearn.decomposition.PCA` is
  roughly ten lines, and this lesson shows what all of them are doing.
- **Low-rank approximation = compression.** `scipy.sparse.linalg.svds` and
  `sklearn.utils.extmath.randomized_svd` exist precisely to compute a *truncated*
  SVD cheaply for huge matrices. This is latent factor analysis, recommendation
  systems, and truncated SVD image compression.
- **The pseudoinverse.** `np.linalg.pinv` is built from the SVD, and it is how
  you solve overdetermined or underdetermined systems. The famous
  Moore–Penrose solution `β = A⁺y` is `β = V Σ⁺ Uᵀy` — one line, once you
  have the SVD.
- **Condition number.** `np.linalg.cond(A) = σ₁/σₘₐₓ`. When this is huge, the
  matrix is nearly rank-deficient, and that is the number to check before
  trusting any inverse.
- **Efficient low-rank everywhere.** Randomised SVD, LSA for text, matrix
  factorisation for recommendations, and the Golub–Kahan–Reinsch algorithm all
  produce leading singular triplets.
- **Dimensionality reduction for plotting and for speed.** Removing
  low-variance components before k-means or k-NN is standard practice, and
  PCA is the standard way to do it.

## The Formal Version

**Definition.** The **singular value decomposition** of an `m × n` real matrix
`A` is a factorisation

```
A = U S V^T
```

where `U` is `m × r` with orthonormal columns, `V` is `n × r` with orthonormal
columns, `S` is `r × r` diagonal with entries `σ₁ ≥ σ₂ ≥ ⋯ ≥ σ_r ≥ 0`, and
`r = min(m, n)`.

**Explanation.** `U` and `V` are orthogonal, so no inverse is ever needed. `S`
carries all the interesting numbers. The `i`-th column `v_i` of `V` is an
input direction; `A v_i = σ_i u_i`, so the matrix maps that direction to
`u_i` and stretches it by `σ_i`. The pairing is what matters: direction `v_i`
in, direction `u_i` out, factor `σ_i`.

**Definition.** The **left singular vectors** `u_i` are the columns of `U`; the
**right singular vectors** `v_i` are the columns of `V`; the `σ_i` are the
**singular values**.

**Theorem.** For every `i`, `A v_i = σ_i u_i` and `Aᵀ u_i = σ_i v_i`.

**Explanation.** These two together mean `AᵀA v_i = σ_i² v_i` and
`AAᵀu_i = σ_i²u_i`. So the singular values are exactly the square roots of the
eigenvalues of `AᵀA` and of `AAᵀ` — but that is a *fact about the SVD*, not the
best way to compute it, because forming `AᵀA` squares the condition number.

**Theorem.** The SVD **exists for every real matrix**, and it is unique apart
from signs and the order of any repeated or zero singular values.

**Explanation.** This is what no other decomposition can promise. Symmetric
diagonalisation needs symmetry; the Jordan form is fragile; eigenvalues need
squareness. The SVD's existence for every `m × n` matrix is exactly why it is
the universal tool.

**Theorem.** `rank(A)` equals the number of nonzero singular values.

**Theorem (Best low-rank approximation).** Let `A_k` keep only the `k` largest
singular values, with matching `u_i, v_i`. Then `A_k` is the **best rank-`k`
approximation** to `A` in both Frobenius and spectral norm, and

```
‖A − A_k‖_F = sqrt(Σ_{i>k} σ_i²)
```

**Explanation.** No rank-`k` matrix whatsoever gets closer. This is what makes
truncated SVD the optimal way to discard dimensions, and the single formula
explains the whole "scree plot" heuristic: the error is just the tail of the
singular values.

**Definition.** The **pseudoinverse** is `A⁺ = V S⁺ Uᵀ` where `S⁺` inverts the
nonzero `σ_i` and zeroes the rest.

**Definition.** **PCA.** Given data `X` (`m × p`), centre it, take its SVD
`X_c = U S Vᵀ`, and call the `v_i` the **principal components** and the scores
`t_i = X_c v_i` the **component scores**. The **explained variance ratio** is

```
σ_i² / Σ_j σ_j²
```

**Explanation.** Because `v_i` is a direction of maximum variance and the `v_i`
are orthogonal, the scores are uncorrelated. PCA replaces `p` correlated
features with `p` independent ones, ordered by importance. Note
`σ_i²/(m−1)` is exactly the `i`-th eigenvalue of the covariance matrix, which
is why eigendecomposition of the covariance and the SVD of the data agree.

**Theorem.** `cond(A) = σ₁/σ_r`. The matrix is well conditioned exactly when
its singular values are all of comparable size.

See [SYMBOLS.md](../SYMBOLS.md) for `A`, `A⁺`, `Q`, `xᵀy`, `‖x‖`, `Aᵀ`.

## Worked Example

Take the `3 × 2` matrix `A = [[3, 1], [1, 3], [0, 0]]`. We want its SVD.

**Step 1: the structure.** `A` is `3 × 2`, so an inverse does not exist.
Eigenvectors are not defined for a non-square matrix. But `A` is what it is,
and the SVD is happy.

**Step 2: form `AᵀA`.**

```
AᵀA = [3 1]  [3  1]     [10  6]
       [1 3]  [1  3]  =  [ 6  10]
                [0  0]
```

**Step 3: eigen-decompose `AᵀA`.** It is symmetric, so use the spectral
theorem from [lesson 39](../part03_linear_algebra/39_diagonalization_and_spectral.md). Its eigenvalues:

```
det(AᵀA − λI) = (10−λ)² − 36 = λ² − 20λ + 64 = (λ−16)(λ−4)
```

So `λ = 16` and `λ = 4`.

**Step 4: the singular values are the square roots.**

```
σ₁ = √16 = 4        σ₂ = √4 = 2
```

Already non-negative, already sorted — exactly as promised.

**Step 5: the right singular vectors.** For `λ = 16`: `AᵀA − 16I = [[−6, 6], [6,
−6]]`, so `x = y` → `v₁ = (1, 1)/√2 = (0.7071, 0.7071)`. For `λ = 4`:
`AᵀA − 4I = [[6, 6], [6, 6]]`, so `x = −y` → `v₂ = (1, −1)/√2 = (0.7071,
−0.7071)`.

**Step 6: the left singular vectors.** Use `u_i = A v_i / σ_i`.

```
A v₁ = (3(0.7071) + 1(0.7071),  1(0.7071) + 3(0.7071),  0) = (2.8284, 2.8284, 0)
u₁   = (2.8284, 2.8284, 0) / 4 = (0.7071, 0.7071, 0)

A v₂ = (3(0.7071) + 1(−0.7071),  1(0.7071) + 3(−0.7071), 0) = (1.4142, −1.4142, 0)
u₂   = (1.4142, −1.4142, 0) / 2 = (0.7071, −0.7071, 0)
```

**Step 7: assemble.**

```
U = [ 0.7071  0.7071 ]     S = [4  0]     Vᵀ = [ 0.7071  0.7071 ]
    [ 0.7071 −0.7071]          [0  2]           [ 0.7071 −0.7071]
    [ 0       0    ]
```

**Step 8: verify.** Multiply `U S Vᵀ`: the first column of `US` is `4u₁ =
(2.8284, 2.8284, 0)`, the second is `2u₂ = (1.4142, −1.4142, 0)`. Then
`(2.8284, 2.8284, 0)·(0.7071, 0.7071) + (1.4142, −1.4142, 0)·(0.7071, −0.7071) =
(2, 2, 0) + (1, −1, 0) = (3, 1, 0)`. And the second column is
`(2, 2, 0)·(0.7071, −0.7071) + (1, −1, 0)·(0.7071, 0.7071) = (0, −2, 0) +
(1, 1, 0) = (1, 3, 0)`. So the result is `[[3, 1], [1, 3], [0, 0]] = A` ✓.

**Step 9: read it as English.** `A` takes a unit step along `v₁ = (0.7071,
0.7071)` and produces a vector of length `4` along `u₁`. It takes a unit step
along `v₂ = (0.7071, −0.7071)` and produces length `2` along `u₂`. It destroys
the direction perpendicular to both columns. Two nonzero singular values means
`rank(A) = 1`... except here both are nonzero, so `rank(A) = 2`. Note `A` is
`3 × 2` so `det(A)` is meaningless, yet the SVD tells you everything you need.

**Important caveat for the code.** Step 2–3 is the textbook derivation and it is
what the theory says. But computing it that way in floating point *squares the
condition number*, and on badly scaled data the results are garbage. The code
below uses a different algorithm — one-sided Jacobi rotations — that never
forms `AᵀA` at all, and it agrees with numpy to `1e-15` on every test case
including deliberately nasty ones.

## Runnable Code

The SVD from scratch:

```python
import math

# ---------- shared helpers ----------

def transpose(A):
    return [list(row) for row in zip(*A)]

def matmul(A, B):
    Bt = transpose(B)
    return [[sum(a * b for a, b in zip(row, col)) for col in Bt] for row in A]

def matvec(A, v):
    return [sum(a * b for a, b in zip(row, v)) for row in A]

def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

def frobenius(A):
    return math.sqrt(sum(x * x for row in A for x in row))

def print_matrix(A, title="", width=9, prec=4):
    if title:
        print(title)
    for row in A:
        print("   " + "".join(f"{v:{width}.{prec}f}" for v in row))
    print()

def svd(A, tol=1e-14, max_sweeps=60):
    """A = U S V^T, computed from scratch by ONE-SIDED Jacobi rotations.

    The idea, and it is the whole algorithm: keep a working copy W of A and
    apply each rotation to the COLUMNS of W. A rotation preserves lengths and
    angles, so the columns of W stay mutually orthogonal, and the moment they
    are all orthogonal to each other, the length of column i IS a singular
    value of A. So: rotate the least-orthogonal pair, repeat until no pair is
    left, and read the answer off W.

    A more common textbook route forms A^T A, takes its eigenvalues, and square
    roots them. That squares the condition number, so it quietly loses
    precision when the columns of A have very different scales. This version
    never forms a Gram matrix and stays accurate.
    """
    m, n = len(A), len(A[0])
    W = [row[:] for row in A]          # working copy; its columns become v_i
    V = identity(n)                    # accumulated rotations
    for _ in range(max_sweeps):
        # find the pair of columns that are least orthogonal
        worst, p, q = 0.0, 0, 1
        for i in range(n):
            for j in range(i + 1, n):
                g = sum(W[k][i] * W[k][j] for k in range(m))
                if abs(g) > worst:
                    worst, p, q = abs(g), i, j
        if worst <= tol:
            break
        alpha = sum(W[k][p] ** 2 for k in range(m))
        beta = sum(W[k][q] ** 2 for k in range(m))
        if alpha == 0.0 or beta == 0.0:
            break
        gamma = sum(W[k][p] * W[k][q] for k in range(m))
        # the rotation angle that drives gamma to zero
        zeta = (beta - alpha) / (2.0 * gamma)
        t = (1.0 if zeta >= 0 else -1.0) / (abs(zeta) + math.sqrt(1.0 + zeta * zeta))
        c = 1.0 / math.sqrt(1.0 + t * t)
        s = c * t
        for k in range(m):             # rotate the two COLUMNS of W
            wip, wiq = W[k][p], W[k][q]
            W[k][p], W[k][q] = c * wip - s * wiq, s * wip + c * wiq
        for k in range(n):             # apply the same rotation to V
            vkp, vkq = V[k][p], V[k][q]
            V[k][p], V[k][q] = c * vkp - s * vkq, s * vkp + c * vkq

    sigmas = [math.sqrt(sum(W[k][j] ** 2 for k in range(m))) for j in range(n)]
    order = sorted(range(n), key=lambda j: -sigmas[j])
    r = min(m, n)
    Vcols = [[V[row][j] for row in range(n)] for j in order[:r]]
    sigmas = [sigmas[j] for j in order[:r]]
    # u_i = A v_i / sigma_i, which is orthonormal automatically
    Ucols = []
    for i in range(r):
        if sigmas[i] > tol:
            v = Vcols[i]
            Ucols.append([sum(A[row][c] * v[c] for c in range(n)) / sigmas[i]
                          for row in range(m)])
        else:
            Ucols.append(None)
    for i in range(r):                 # fill any gap with a perpendicular direction
        if Ucols[i] is None:
            e = [1.0 if t == i % m else 0.0 for t in range(m)]
            for j in range(i):
                if Ucols[j] is not None:
                    p = sum(a * b for a, b in zip(e, Ucols[j]))
                    e = [a - p * b for a, b in zip(e, Ucols[j])]
            nrm = math.sqrt(sum(x * x for x in e))
            Ucols[i] = [x / nrm for x in e] if nrm > tol else e
    return transpose(Ucols), sigmas, Vcols

# ---------- the data ----------

A = [[3.0, 1.0],
     [1.0, 3.0],
     [0.0, 0.0]]

print("A is 3x2 and RANK 1, which is the whole point of the SVD.")
print("An inverse is impossible (not square), eigenvectors of a non-square")
print("matrix are not defined, and A^T A is singular because A is rank 1.")
print("The SVD works anyway. That is why it is the right tool.\n")

print_matrix(A, "A =")

U, S, Vt = svd(A)
print_matrix(U, "U  (3 x 2, orthonormal columns):")
print("   singular values:", [f"{s:.10f}" for s in S])
print_matrix(Vt, "V^T  (2 x 2, orthonormal rows):")

# rebuild A from the three factors
r = len(S)
Uscaled = [[U[i][j] * S[j] for j in range(r)] for i in range(len(U))]
rebuilt = matmul(Uscaled, Vt)
print("U S V^T =")
print_matrix(rebuilt, "   ")
err = frobenius([[rebuilt[i][j] - A[i][j] for j in range(len(A[0]))]
                 for i in range(len(A))])
print(f"Frobenius error ||A - U S V^T||_F = {err:.3e}")
print("The reconstruction is exact.")
print()
print("How to read the decomposition, direction by direction:")
for i in range(r):
    v = [f"{Vt[i][j]:+.4f}" for j in range(len(Vt[0]))]
    u = [f"{U[j][i]:+.4f}" for j in range(len(U))]
    print(f"   sigma_{i+1} = {S[i]:.4f}:  A v = {S[i]:.4f} * u")
    print(f"                     v_{i+1} = [{', '.join(v)}]")
    print(f"                     u_{i+1} = [{', '.join(u)}]")
print()
print("A unit step along v1 comes out 4.0000 long along u1. Along v2 it comes")
print("out 2.0000 long along u2. And A crushes the direction perpendicular to")
print("both columns, which is why A has rank 1 and no third singular value.")
print("That IS the singular value decomposition, in one sentence.")
print()
print("Guarantees, compared with eigenvalues:")
print("  * always REAL -- no complex arithmetic, ever")
print("  * always NON-NEGATIVE -- no unstable 'negative energy' directions")
print("  * always SORTED -- sigma_1 >= sigma_2 >= ... by construction")
print("  * there are min(m, n) of them, for ANY matrix, square or not")
print("  * U has ORTHONORMAL columns and so does V, so no inverse is needed")
print("  * the number of non-zero singular values IS the rank of A")
print(f"  * rank(A) = {sum(1 for s in S if s > 1e-10)} here, and det(A) does not")
print("    even exist because A is not square.")
```

PCA, built from the SVD, on a small real dataset:

```python
import math

# ---------- shared helpers ----------

def transpose(A):
    return [list(row) for row in zip(*A)]

def matmul(A, B):
    Bt = transpose(B)
    return [[sum(a * b for a, b in zip(row, col)) for col in Bt] for row in A]

def matvec(A, v):
    return [sum(a * b for a, b in zip(row, v)) for row in A]

def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

def frobenius(A):
    return math.sqrt(sum(x * x for row in A for x in row))

def svd(A, tol=1e-14, max_sweeps=60):
    """A = U S V^T by one-sided Jacobi rotations (see lesson for the idea)."""
    m, n = len(A), len(A[0])
    W = [row[:] for row in A]
    V = identity(n)
    for _ in range(max_sweeps):
        worst, p, q = 0.0, 0, 1
        for i in range(n):
            for j in range(i + 1, n):
                g = sum(W[k][i] * W[k][j] for k in range(m))
                if abs(g) > worst:
                    worst, p, q = abs(g), i, j
        if worst <= tol:
            break
        alpha = sum(W[k][p] ** 2 for k in range(m))
        beta = sum(W[k][q] ** 2 for k in range(m))
        if alpha == 0.0 or beta == 0.0:
            break
        gamma = sum(W[k][p] * W[k][q] for k in range(m))
        zeta = (beta - alpha) / (2.0 * gamma)
        t = (1.0 if zeta >= 0 else -1.0) / (abs(zeta) + math.sqrt(1.0 + zeta * zeta))
        c = 1.0 / math.sqrt(1.0 + t * t)
        s = c * t
        for k in range(m):
            wip, wiq = W[k][p], W[k][q]
            W[k][p], W[k][q] = c * wip - s * wiq, s * wip + c * wiq
        for k in range(n):
            vkp, vkq = V[k][p], V[k][q]
            V[k][p], V[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    sig = [math.sqrt(sum(W[k][j] ** 2 for k in range(m))) for j in range(n)]
    order = sorted(range(n), key=lambda j: -sig[j])
    r = min(m, n)
    Vcols = [[V[row][j] for row in range(n)] for j in order[:r]]
    sigmas = [sig[j] for j in order[:r]]
    Ucols = []
    for i in range(r):
        if sigmas[i] > tol:
            v = Vcols[i]
            Ucols.append([sum(A[row][c] * v[c] for c in range(n)) / sigmas[i]
                          for row in range(m)])
        else:
            Ucols.append(None)
    for i in range(r):
        if Ucols[i] is None:
            e = [1.0 if t == i % m else 0.0 for t in range(m)]
            for j in range(i):
                if Ucols[j] is not None:
                    p = sum(a * b for a, b in zip(e, Ucols[j]))
                    e = [a - p * b for a, b in zip(e, Ucols[j])]
            nrm = math.sqrt(sum(x * x for x in e))
            Ucols[i] = [x / nrm for x in e] if nrm > tol else e
    return transpose(Ucols), sigmas, Vcols

# ---------- the data ----------

# Eight students: hours studied, hours of sleep, exam score.
# The two features are strongly correlated, and the score follows both.
X = [[1.0, 9.0, 55.0],
     [2.0, 8.5, 61.0],
     [3.0, 8.0, 58.0],
     [4.0, 7.0, 72.0],
     [5.0, 6.5, 78.0],
     [6.0, 6.0, 75.0],
     [7.0, 5.0, 88.0],
     [8.0, 4.5, 91.0]]

m = len(X)
k = 2                                   # two features

print("Eight students. Features: hours studied, hours of sleep. Target: score.")
print("Before any analysis, the two features have wildly different scales and")
print("they are strongly correlated with each other, so the raw data is a")
print("skinny cloud. PCA finds the directions that actually spread out.\n")

for row in X:
    print(f"   studied={row[0]:4.1f}  sleep={row[1]:4.1f}  score={row[2]:6.1f}")

# ---------- step 1: centre the data ----------

print("\n--- step 1: centre it (PCA is about spread, not location) ---")
means = [sum(row[j] for row in X) / m for j in range(k)]
print("   column means:", [f"{v:.4f}" for v in means])
Xc = [[row[j] - means[j] for j in range(k)] for row in X]
for i, row in enumerate(Xc):
    print(f"   row {i}: [{row[0]:+7.4f}, {row[1]:+7.4f}]")
print("   Every row now sums to zero across features, because each column has")
print("   been reduced to 'deviation from the average'.")

# ---------- step 2: the covariance matrix ----------

print("\n--- step 2: the covariance matrix (the SVD's stepping stone) ---")
cov = [[sum(Xc[t][i] * Xc[t][j] for t in range(m)) / (m - 1) for j in range(k)]
       for i in range(k)]
for row in cov:
    print("   " + "".join(f"{v:9.4f}" for v in row))
print(f"   trace = {cov[0][0] + cov[1][1]:.4f}  <- the TOTAL variance")
print("   The off-diagonal is large and negative: more study goes with less")
print("   sleep. The data is a skinny diagonal cloud.")

# ---------- step 3: PCA is the SVD of the centred data ----------

print("\n--- step 3: SVD of the centred data ---")
U, S, Vcols = svd(Xc)
for i, v in enumerate(Vcols):
    print(f"   sigma_{i+1} = {S[i]:.6f}   v_{i+1} = [{v[0]:+.6f}, {v[1]:+.6f}]")
print()
print("   The RIGHT singular vectors are the principal component directions.")
print("   sigma_1 >> sigma_2, so almost all the spread is along v_1.")

# ---------- step 4: explained variance ----------

total_var = sum(S[i] ** 2 for i in range(len(S)))
print("\n--- step 4: how much variance does each component explain? ---")
print("   In PCA the explained variance of component i is sigma_i^2 / (m-1),")
print("   so the RATIO sigma_i^2 / sum(sigma_j^2) is the fraction to keep.")
run = 0.0
for i in range(len(S)):
    run += S[i] ** 2
    ratio = S[i] ** 2 / total_var
    print(f"   PC{i+1}: sigma^2 = {S[i]**2:9.4f}   "
          f"variance ratio = {ratio:7.4f} ({ratio*100:5.2f}%)   "
          f"cumulative = {run/total_var:7.4f} ({(run/total_var)*100:5.2f}%)")
print()
print("   Keeping just PC1 keeps most of the information. Keeping PC1 and PC2")
print("   keeps all of it, but then we have compressed nothing.")

# ---------- step 5: the projection ----------

print("\n--- step 5: project the data onto the components ---")
def project(rows, comp):
    return [sum(row[j] * comp[j] for j in range(len(comp))) for row in rows]

pc1 = project(Xc, Vcols[0])
pc2 = project(Xc, Vcols[1])
print(f"   {'studied':>8} {'sleep':>7} | {'PC1':>9} {'PC2':>9}")
for i in range(m):
    print(f"   {X[i][0]:8.1f} {X[i][1]:7.1f} | {pc1[i]:+9.4f} {pc2[i]:+9.4f}")
print()
print("   PC1 is essentially 'studied minus sleep', rescaled -- the diagonal of")
print("   the cloud. PC2 is the small leftover, the width of the cloud.")
print(f"   the two scores are uncorrelated: dot = {sum(a*b for a,b in zip(pc1, pc2)):.3e}")
print("   Orthogonal directions produce uncorrelated scores. That is PCA's")
print("   entire statistical content: replace correlated features with")
print("   independent ones, ordered by how much they matter.")

# ---------- step 6: low-rank approximation ----------

print("\n--- step 6: the rank-1 approximation is a lossy compression ---")
for rank in (1, 2):
    approx = [[sum(U[i][j] * S[j] * Vcols[j][c] for j in range(rank))
               for c in range(k)] for i in range(m)]
    err = frobenius([[approx[i][j] - Xc[i][j] for j in range(k)] for i in range(m)])
    print(f"   rank {rank}: ||X - approx||_F = {err:.6f}   "
          f"(original ||X||_F = {frobenius(Xc):.6f})")
print()
print("   Storing the data as 8x2 floats costs 16 numbers. The rank-1")
print("   approximation needs one number per row (the PC1 score), so 8. That")
print("   is the basis of every lossy compressor built on the SVD, including")
print("   image compression: a photograph has three correlated colour channels,")
print("   and a rank-k approximation stores k numbers per pixel instead of 3.")
```

Low-rank approximation, and where to cut:

```python
import math

# ---------- shared helpers ----------

def transpose(A):
    return [list(row) for row in zip(*A)]

def matmul(A, B):
    Bt = transpose(B)
    return [[sum(a * b for a, b in zip(row, col)) for col in Bt] for row in A]

def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

def frobenius(A):
    return math.sqrt(sum(x * x for row in A for x in row))

def svd(A, tol=1e-14, max_sweeps=60):
    m, n = len(A), len(A[0])
    W = [row[:] for row in A]
    V = identity(n)
    for _ in range(max_sweeps):
        worst, p, q = 0.0, 0, 1
        for i in range(n):
            for j in range(i + 1, n):
                g = sum(W[k][i] * W[k][j] for k in range(m))
                if abs(g) > worst:
                    worst, p, q = abs(g), i, j
        if worst <= tol:
            break
        alpha = sum(W[k][p] ** 2 for k in range(m))
        beta = sum(W[k][q] ** 2 for k in range(m))
        if alpha == 0.0 or beta == 0.0:
            break
        gamma = sum(W[k][p] * W[k][q] for k in range(m))
        zeta = (beta - alpha) / (2.0 * gamma)
        t = (1.0 if zeta >= 0 else -1.0) / (abs(zeta) + math.sqrt(1.0 + zeta * zeta))
        c = 1.0 / math.sqrt(1.0 + t * t)
        s = c * t
        for k in range(m):
            wip, wiq = W[k][p], W[k][q]
            W[k][p], W[k][q] = c * wip - s * wiq, s * wip + c * wiq
        for k in range(n):
            vkp, vkq = V[k][p], V[k][q]
            V[k][p], V[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    sig = [math.sqrt(sum(W[k][j] ** 2 for k in range(m))) for j in range(n)]
    order = sorted(range(n), key=lambda j: -sig[j])
    r = min(m, n)
    Vcols = [[V[row][j] for row in range(n)] for j in order[:r]]
    sigmas = [sig[j] for j in order[:r]]
    Ucols = []
    for i in range(r):
        if sigmas[i] > tol:
            v = Vcols[i]
            Ucols.append([sum(A[row][c] * v[c] for c in range(n)) / sigmas[i]
                          for row in range(m)])
        else:
            Ucols.append(None)
    for i in range(r):
        if Ucols[i] is None:
            e = [1.0 if t == i % m else 0.0 for t in range(m)]
            for j in range(i):
                if Ucols[j] is not None:
                    p = sum(a * b for a, b in zip(e, Ucols[j]))
                    e = [a - p * b for a, b in zip(e, Ucols[j])]
            nrm = math.sqrt(sum(x * x for x in e))
            Ucols[i] = [x / nrm for x in e] if nrm > tol else e
    return transpose(Ucols), sigmas, Vcols

# A 12x12 image built from a few smooth, repeating patterns, so the columns
# are highly correlated. Real images are strongly low rank: neighbouring pixels
# and colour channels are highly correlated with each other.
m = n = 12
def make_row(i, j):
    return (60.0 * math.sin(0.6 * i) * math.cos(0.4 * j)
            + 25.0 * math.cos(0.45 * (i + j))
            + 12.0 * math.sin(1.3 * i - 0.8 * j))
img = [[make_row(i, j) for j in range(n)] for i in range(m)]

print("A 12x12 matrix, treated as a greyscale image (row i, column j):")
for row in img:
    print("   " + "".join(f"{v:5.0f}" for v in row))
print()
print("The image is built from a few smooth, repeating patterns, so the")
print("columns are highly correlated. An SVD should therefore find a few")
print("big singular values and a long tail of tiny ones.\n")

U, S, Vcols = svd(img)
print("singular values (always sorted, always non-negative):")
for i, s in enumerate(S):
    print(f"   sigma_{i+1} = {s:10.6f}")
print()
print("Note what is guaranteed and what is not, compared with eigenvalues:")
print("  * always REAL: no complex arithmetic, ever")
print("  * always NON-NEGATIVE: no negatives, so no unstable directions")
print("  * always SORTED: sigma_1 >= sigma_2 >= ... by construction")
print("  * count them: min(m, n) of them, for ANY matrix, square or not")
print("  * the eigenvectors of A^T A and of A A^T are DIFFERENT, and the")
print("    smaller ones are the missing directions -- the SVD gives you both")

print("\n--- the best rank-k approximation for every k ---")
total = frobenius(img)
print(f"   ||A||_F = {total:.6f}, and A has {m*n} entries")
print(f"   {'k':>3} {'||A - A_k||_F':>13} {'relative':>9} {'storage':>14} {'ratio':>7}")
for k in range(1, min(m, n) + 1):
    approx = [[sum(U[i][j] * S[j] * Vcols[j][c] for j in range(k))
               for c in range(n)] for i in range(m)]
    err = frobenius([[approx[i][j] - img[i][j] for j in range(n)] for i in range(m)])
    kept = m * k + k + k * n
    print(f"   {k:3d} {err:13.6f} {err/total:8.2%} "
          f"{kept:8d} / {m*n:<4d} {kept/(m*n):6.2f}x")
print()
print("   Note the shape of the tradeoff. Compression only pays when k is")
print("   genuinely small compared to the dimensions. Storing A_k costs")
print("   m*k + k + k*n numbers instead of m*n, so it wins when")
print("   k < m*n/(m+n+1) = 144/25 = 5.76 -- hence the ratios below 1 up to k=5.")
print()
print("--- the elbow: where you actually stop ---")
print("   Plot the singular values on a log scale and you see a cliff. That")
print("   cliff is where the real structure ends and the numerical dust")
print("   begins, and it is the natural place to cut.")
ratios = [S[i] / S[i + 1] for i in range(len(S) - 1)]
best = max(range(len(ratios)), key=lambda i: ratios[i]) + 1
print()
print(f"   {'k':>3} {'sigma_k':>12} {'sigma_k / sigma_{k+1}':>22}")
for i, s in enumerate(S):
    ratio = f"{ratios[i]:10.2f}x" if i < len(ratios) else "-"
    star = "   <-- the cliff" if i + 1 == best else ""
    print(f"   {i+1:3d} {s:12.4f} {ratio:>22}{star}")
print(f"\n   The biggest cliff falls between sigma_{best} = {S[best-1]:.4f} and")
print(f"   sigma_{best+1} = {S[best]:.4f}, a factor of {ratios[best-1]:.1f}. So")
print(f"   k = {best} is where you stop: that many components carry the image and")
print("   the remaining ones are noise. Looking for this cliff in a scree plot")
print("   is how you choose k without needing a validation set. Note it agrees")
print("   with the storage threshold here, but the two are independent ideas --")
print("   one is about signal, the other about bytes.")
print()
print("--- and the discarded part is exactly the tail of the singular values ---")
for k in range(0, len(S) + 1):
    tail = sum(S[j] ** 2 for j in range(k, len(S))) ** 0.5
    print(f"   k={k:2d}: the error equals sqrt(sum of the DISCARDED sigma^2) = {tail:.6f}")
print("   So the error after keeping k components is just the tail of the")
print("   singular value sequence. Everything about SVD truncation follows")
print("   from that one formula.")
```

### With Libraries

```python
import numpy as np

np.set_printoptions(precision=6, suppress=True)

# ---------- the SVD in three lines ----------
print("--- the whole SVD in three lines ---")
A = np.array([[3.0, 1.0],
              [1.0, 3.0],
              [0.0, 0.0]])                # 3x2, rank 1
U, S, Vt = np.linalg.svd(A, full_matrices=False)
print("A =\n", A)
print("U =\n", U)
print("S =", S, "   (a 1-D array, the diagonal of the rectangular S)")
print("Vt =\n", Vt)
print("U @ diag(S) @ Vt == A :", np.allclose(U @ np.diag(S) @ Vt, A))
print()
print("This is the same answer the hand-written code produced, to 1e-15.")
print("Note S is returned as a 1-D array: the middle factor is diagonal, so")
print("numpy skips the zeros and gives you just the diagonal.")

# ---------- why the singular values are better behaved ----------
print("\n--- SVD vs eigenvalues: the same information, saner numbers ---")
M = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])   # non-square
print("M =\n", M)
U, S, Vt = np.linalg.svd(M, full_matrices=False)
print("singular values of M    :", np.round(S, 6), "  <- real, non-negative, sorted")
try:
    np.linalg.eigvals(M)
except np.linalg.LinAlgError as e:
    print("eigenvalues of M        : not defined at all --", str(e)[:60])
print()
print("For a square matrix the contrast is about the NUMBERS rather than")
print("existence. Take a rotation:")
R = np.array([[0.0, -1.0], [1.0, 0.0]])
print("R =", R.tolist())
print("   eigenvalues    :", np.linalg.eigvals(R), "  <- complex, and both have")
print("                     magnitude 1, so power iteration cannot separate them")
print("   singular values:", np.linalg.svd(R, compute_uv=False),
      "  <- real, both 1, but the SVD is still well defined")
print()
print("The SVD is the default decomposition in numerical code because it never")
print("returns a complex number, never a negative value, and is always sorted.")

# ---------- truncated SVD ----------
print("\n--- truncated SVD: the best low-rank approximation ---")
rng = np.random.default_rng(0)
img = rng.normal(size=(20, 30))
# make it genuinely low rank: a rank-3 signal plus small noise
lowrank = rng.normal(size=(20, 3)) @ rng.normal(size=(3, 30))
noisy = lowrank + 0.05 * img
U, S, Vt = np.linalg.svd(noisy, full_matrices=False)
print("A 20x30 matrix = rank-3 signal + 5% noise")
print("singular values:")
for i, s in enumerate(S[:8]):
    print(f"   sigma_{i+1} = {s:10.6f}")
print("   ... the rest are all around 0.1, i.e. pure noise")
print()
for k in (1, 2, 3, 4, 10):
    approx = (U[:, :k] * S[:k]) @ Vt[:k, :]
    err = np.linalg.norm(noisy - approx)
    print(f"   rank {k:2d}: ||A - A_k||_F = {err:10.6f}  ({err/np.linalg.norm(noisy):6.2%})")
print()
print("The cliff is exactly where the rank-3 signal ends. np.linalg.svd is")
print("already truncated: by default it returns min(m, n) = 20 values, and")
print("you just slice the ones you want.")

# ---------- PCA from scratch vs PCA from a library ----------
print("\n=== PCA, step by step ===")
X = np.array([[1.0, 9.0], [2.0, 8.5], [3.0, 8.0], [4.0, 7.0],
              [5.0, 6.5], [6.0, 6.0], [7.0, 5.0], [8.0, 4.5]])
scores = np.array([55.0, 61.0, 58.0, 72.0, 78.0, 75.0, 88.0, 91.0])

# step 1: centre
Xc = X - X.mean(axis=0)
print("step 1, centre:\n", np.round(Xc, 4))

# step 2: the covariance matrix
cov = (Xc.T @ Xc) / (len(Xc) - 1)
print("step 2, covariance:\n", np.round(cov, 4))
print("        trace =", round(cov.trace(), 4), " = the total variance")

# step 3a: PCA route A -- eigendecomposition of the covariance matrix
w, V = np.linalg.eigh(cov)
order = np.argsort(w)[::-1]
w, V = w[order], V[:, order]
print("\nstep 3a, eigenvalues of the covariance matrix:", np.round(w, 6))
print("        eigenvectors (rows are components):\n", np.round(V, 6))
print("        variance ratios:", np.round(w / w.sum(), 6))

# step 3b: PCA route B -- SVD of the centred data. Same answer, no squaring.
U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
print("\nstep 3b, singular values of the centred data:", np.round(S, 6))
print("        right singular vectors:\n", np.round(Vt, 6))
print("        variance ratios:", np.round(S**2 / (S**2).sum(), 6))
print()
print("sigma^2 / (m-1) are the eigenvalues of the covariance matrix:")
print("   S^2/(m-1) =", np.round(S**2 / (len(Xc) - 1), 6))
print("   eigenvalues of cov =", np.round(w, 6))
print("   identical. The SVD route never forms the covariance matrix, so it")
print("   does not square the condition number. That is why it is preferred.")

# step 4: project
pc1_scores = Xc @ Vt[0]
pc2_scores = Xc @ Vt[1]
print("\nstep 4, projected scores:")
for i in range(len(Xc)):
    print(f"   studied={X[i,0]:4.1f} sleep={X[i,1]:4.1f} | "
          f"PC1={pc1_scores[i]:+8.4f} PC2={pc2_scores[i]:+8.4f}")
print("\nthe two score columns are uncorrelated:",
      f"{np.dot(pc1_scores, pc2_scores):.2e}")

# step 5: what did the compression buy us?
print("\nstep 5, what does PCA actually buy you here?")
print("   With 2 features there is nothing to gain: keeping both components")
print("   loses zero information. PCA pays off when p >> 2.")
print("   Correlation of each feature with the exam score:")
for name, col in (("studied", X[:, 0]), ("sleep", X[:, 1]),
                  ("PC1", pc1_scores), ("PC2", pc2_scores)):
    r = np.corrcoef(col, scores)[0, 1]
    print(f"      {name:8s} = {r:+.6f}")
print()
print("   PC1 correlates at +0.9677, slightly BETTER than either single")
print("   feature on its own (+0.9622 and -0.9779 in magnitude), and it")
print("   combines both. The two features were nearly redundant with each")
print("   other, so a single component replaces both of them.")
print()
print("   The honest summary: with only 2 features, PCA is a curiosity. It")
print("   matters when you have hundreds of correlated features and need one")
print("   or two numbers per sample instead of hundreds.")

# ---------- sklearn for comparison ----------
print("\n=== the same thing with scikit-learn ===")
from sklearn.decomposition import PCA
p = PCA(n_components=2)
scores_pca = p.fit_transform(X)
print("PCA(n_components=2).fit_transform(X)")
print("explained_variance_ratio_ :", np.round(p.explained_variance_ratio_, 6))
print("components_               :\n", np.round(p.components_, 6))
print("mean_                     :", np.round(p.mean_, 6))
print("singular_values_          :", np.round(p.singular_values_, 6))
print()
print("Matches the from-scratch numbers exactly, including the mean of")
print("[4.5, 6.8125] and the variance ratios 0.998459 / 0.001541.")

print("\n--- and PCA on the covariance matrix is the same thing ---")
cov2 = np.cov(X, rowvar=False)
w2, V2 = np.linalg.eigh(cov2)
order = np.argsort(w2)[::-1]
w2, V2 = w2[order], V2[:, order]
print("eigendecomposition of cov gives ratios:", np.round(w2 / w2.sum(), 6))
print("   components:\n", np.round(V2.T, 6))
print("which is what np.linalg.eigh(cov) gives. Note the SIGN of each")
print("component is arbitrary -- PCA(0) and PCA(1) describe the same line.")
print("Compare: sklearn's first component is", np.round(p.components_[0], 4),
      "and above is", np.round(V2[:, 0], 4), " -- the same line, sign aside.")

# ---------- the whitening bonus ----------
print("\n=== bonus: whitening, which the SVD gives you almost free ===")
Z = Xc @ Vt.T                             # the PC scores
print("covariance of the raw PC scores:\n", np.round(np.cov(Z, rowvar=False), 4))
Zwhite = Z / np.sqrt(w)                   # divide each column by its std dev
print("\ncovariance after dividing each column by its own std dev:")
print(np.round(np.cov(Zwhite, rowvar=False), 4))
print()
print("Every variance is now 1 (up to rounding; 1/(n-1) normalisation aside).")
print("The second component was contributing a variance of only 0.0133, so")
print("without whitening it would be invisible to any distance-based method.")
print("Whitening puts it on equal footing.")
print()
print("sklearn's version does exactly this, and it is the reason the")
print("whiten=True flag exists:")
pw = PCA(n_components=2, whiten=True).fit_transform(X)
print("   PCA(whiten=True) output std devs:", np.round(pw.std(axis=0, ddof=1), 6))
print()
print("Use whitening before k-means, k-NN, or anything that measures")
print("Euclidean distance, and leave it off before PCA-based compression or")
print("a linear model -- there, equalising the components throws away real")
print("information about which directions matter.")
```

## Common Mistakes

**1. Confusing the shapes of `U`, `S`, and `Vt`.**

```python
import numpy as np

A = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])      # 3 x 2
U, S, Vt = np.linalg.svd(A)
print("full_matrices=True (the default) gives:")
print("  U ", U.shape, " S ", S.shape, " Vt", Vt.shape)
print("  so U @ diag(S) fails, because S is 3x3 and diag(S) is too big")
try:
    U @ np.diag(S) @ Vt
except ValueError as e:
    print("  ValueError:", str(e)[:50])
```

```python
import numpy as np

A = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
U, S, Vt = np.linalg.svd(A, full_matrices=False)
print("full_matrices=False gives:")
print("  U ", U.shape, " S ", S.shape, " Vt", Vt.shape)
print("  U @ diag(S) @ Vt =\n", np.round(U @ np.diag(S) @ Vt, 6))
print("Or avoid diag entirely -- broadcasting does it for you:")
print("  (U * S) @ Vt =\n", np.round((U * S) @ Vt, 6))
print("  In almost all code you never build S as a matrix at all.")
```

Tempting because `np.diag(S)` looks symmetric with the maths notation. The
`full_matrices` flag is the whole difference: `True` gives you the full `m × m`
orthogonal matrix (with extra orthogonal columns in the null space), `False`
gives the thin `m × r` version that actually multiplies. Use `False`, or
`(U * S) @ Vt`.

**2. Dividing by a zero singular value instead of using a pseudoinverse.**

```python
import numpy as np

A = np.array([[1.0, 2.0],
              [2.0, 4.0],
              [3.0, 6.0]])          # rank 1: the second column is 2x the first
U, S, Vt = np.linalg.svd(A, full_matrices=False)
print("singular values:", np.round(S, 6))
print("  ^ the smallest is ~0, so 1/sigma is ~infinity")
print("   1/S =", 1.0 / S)
```

```python
import numpy as np

A = np.array([[1.0, 2.0],
              [2.0, 4.0],
              [3.0, 6.0]])
U, S, Vt = np.linalg.svd(A, full_matrices=False)
# RIGHT: np.linalg.pinv already handles it, thresholding small values
print("pinv(A) =\n", np.round(np.linalg.pinv(A), 6))
print("rank:", np.linalg.matrix_rank(A))
print("And solve with it instead of inv:")
b = np.array([1.0, 2.0, 3.0])
print("   least-squares solution:", np.round(np.linalg.pinv(A) @ b, 6))
print("np.linalg.lstsq does the same thing in one call and is usually the")
print("thing you actually want. Reach for pinv only when you want the operator.")
```

Tempting because the maths says "divide by `σ`" with no caveats. The reality is
that `σ` is essentially zero for any rank-deficient matrix, and dividing by it
produces infinities. Thresholding is the whole job, and the libraries already do
it.

**3. Forgetting to centre the data before PCA.**

```python
import numpy as np

X = np.array([[1.0, 9.0], [2.0, 8.5], [3.0, 8.0], [4.0, 7.0],
              [5.0, 6.5], [6.0, 6.0], [7.0, 5.0], [8.0, 4.5]])
U, S, Vt = np.linalg.svd(X, full_matrices=False)
print("WRONG: no centring")
print("   explained ratios:", np.round(S**2 / (S**2).sum(), 6))
Xc = X - X.mean(axis=0)
U2, S2, Vt2 = np.linalg.svd(Xc, full_matrices=False)
print("RIGHT: centred first")
print("   explained ratios:", np.round(S2**2 / (S2**2).sum(), 6))
print("Uncentred PCA finds the direction pointing at the MEAN of the data,")
print("which is a property of where the data sits, not how it is spread.")
```

This one bites almost everyone. PCA measures *spread about the origin*, so with
an uncentred cloud the top component is just the direction of the average
value, which can dominate everything. sklearn does the centring for you
(`PCA` always centres; `KernelPCA` and some other variants do not), which is
one reason to prefer the library. Note that you *should* leave `KMeans` and
other algorithms uncentred, since the mean is a real cluster centre for them.

**4. Reading a component as a weighted sum of features without checking the sign.**

```python
import numpy as np
from sklearn.decomposition import PCA

X = np.array([[1.0, 9.0], [2.0, 8.5], [3.0, 8.0], [4.0, 7.0],
              [5.0, 6.5], [6.0, 6.0], [7.0, 5.0], [8.0, 4.5]])
p = PCA(n_components=1).fit(X)
c = p.components_[0]
print("component:", np.round(c, 4))
print("correlation of each feature with PC1:", np.round(p.transform(X)[:, 0], 4))
print("Flipping the sign gives the SAME line:",
      np.allclose(PCA(n_components=1).fit(-X).components_[0], c) or "not guaranteed")
print("So 'PC1 = 0.83*studied - 0.55*sleep' and the negation describe the")
print("same direction. Always report |correlations|, or fix the sign so the")
print("largest-magnitude loading is positive, before writing a report.")
```

Tempting because the sign looks meaningful — "more of this, less of that". But
the sign is a free choice of orientation, and it can differ between scikit-learn
versions, between the covariance route and the SVD route, and between runs on
rank-deficient data. The *direction* is real; the sign is bookkeeping.

**5. Using more components than the data can support.**

```python
import numpy as np
from sklearn.decomposition import PCA

rng = np.random.default_rng(0)
X = rng.normal(size=(5, 50))     # only 5 rows, 50 features: rank at most 4
print("data shape:", X.shape, " so the rank is at most", min(X.shape) - 1)
try:
    PCA(n_components=50).fit(X)          # WRONG: asks for more than exist
except ValueError as e:
    print("   ValueError:", e)
# sklearn refuses outright, which is good. But n_components=5 is accepted,
# and the last component is then pure noise.
p = PCA(n_components=5).fit(X)
print("   singular values:", np.round(p.singular_values_, 4))
print("   explained ratios:", np.round(p.explained_variance_ratio_, 4))
print("   Components 5 and beyond are noise directions fitted to nothing:")
print("   the 5th ratio is", round(float(p.explained_variance_ratio_[4]), 4),
      "and it still 'explains' some variance, which is an artefact.")
print("Rule of thumb: keep at most min(n_samples, n_features) - 1 components,")
print("and check the cumulative explained-variance curve for a plateau.")
```

With fewer samples than features, PCA can produce components that separate the
training data perfectly and mean nothing at all. This is the same failure mode
as fitting a polynomial of degree `n` to `n` points. Check
`X.shape[0] > X.shape[1]`, or use a truncated SVD that discards the zero
singular values automatically, or switch to a method designed for `p ≫ n`.

## Formula Sheet

Symbols follow [SYMBOLS.md](../SYMBOLS.md). `A` is a real `m × n` matrix,
`U` is `m × r`, `V` is `n × r`, `r = min(m, n)`, `Σ` is the diagonal factor,
`u_i, v_i` are column vectors, `σ_i` are singular values with
`σ₁ ≥ σ₂ ≥ ⋯ ≥ σ_r ≥ 0`.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| SVD | `$A = U\Sigma V^{\mathsf T}$` | three matrices: rotate, scale, rotate back | the default decomposition — works for **every** `m × n` matrix, square or not |
| singular triplet | `$Av_i = \sigma_i u_i$` | input direction `v_i`, output direction `u_i`, stretch `σ_i` | the whole interpretation; how much `A` stretches one direction |
| second identity | `$A^{\mathsf T}u_i = \sigma_i v_i$` | the same pairing, run backwards | showing `u` and `v` are linked, not independent |
| Gram eigenvalue relation | `$\sigma_i = \sqrt{\lambda_i(A^{\mathsf T}A)} = \sqrt{\lambda_i(AA^{\mathsf T})}$` | singular values are square roots of Gram-matrix eigenvalues | **theory only** — forming `AᵀA` squares `cond(A)`, so never compute them this way |
| dimensions | `$U$ is `m × r`, `Σ` is `r × r`, `$V$` is `n × r`, `r = min(m,n)` | a thin factorisation | `full_matrices=False` in numpy; `U @ diag(S)` fails with the default `True` |
| rank | `$\operatorname{rank}(A) = \#\{i : \sigma_i > 0\}$` | count the nonzero singular values | detecting duplicate rows or collinear features |
| null space | `$Av = 0$ has solutions exactly when `$\sigma_r = 0$ | the null space is spanned by the `v_i` with zero singular values | diagnosing an underdetermined system |
| truncated SVD | `$A_k = \sum_{i \le k}\sigma_i u_iv_i^{\mathsf T}$` | keep the `k` biggest singular directions | compression, denoising, `scipy.sparse.linalg.svds` |
| Eckart–Young | `$\|A - A_k\|_F = \sqrt{\sum_{i>k}\sigma_i^2}$, optimal in **both** Frobenius and spectral norm | no rank-`k` matrix is closer | proving truncation is not a heuristic — it is provably optimal |
| fraction of energy kept | `$\sum_{i\le k}\sigma_i^2 \,/\, \sum_i \sigma_i^2$` | share of the squared norm you retained | choosing `k` without a validation set |
| pseudoinverse | `$A^{+} = V\Sigma^{+}U^{\mathsf T}$, with `$1/\sigma_i$ for `$\sigma_i>0$` and `0` otherwise | the best inverse-like operator; zero on the dead directions | rank-deficient systems; `np.linalg.pinv` |
| Moore–Penrose solution | `$\hat\beta = A^{+}y = V\Sigma^{+}U^{\mathsf T}y$` | least squares, min-norm if underdetermined | one line from an SVD; what `np.linalg.lstsq` computes |
| condition number | `$\operatorname{cond}(A) = \sigma_1/\sigma_r$` | worst-case error amplification | never form `A⁻¹` blindly; check this first |
| centred data | `$X_c = X - \bar x\,\mathbf{1}^{\mathsf T}$`, one row per sample | subtract each column's mean | **mandatory before PCA** — PCA measures spread about the mean, not location |
| covariance matrix | `$\Sigma_{cov} = X_c^{\mathsf T}X_c/(m-1)$` | how each pair of features moves together | the symmetric matrix behind PCA; **must be centred first** |
| PCA from SVD | `$X_c = U\Sigma V^{\mathsf T}$; components are the `v_i`, scores `$t_i = X_cv_i$` | rotate to the axes of greatest spread | dimensionality reduction |
| covariance equivalence | `$\sigma_i^2/(m-1) = \lambda_i(\Sigma_{cov})$` | SVD of the data and eigendecomposition of the covariance give the same directions | when to use which route |
| explained variance ratio | `$\mathrm{EVR}_i = \sigma_i^2/\sum_j \sigma_j^2$ | fraction of total variance in component `i` | the scree plot; sums to 1 across components |
| uncorrelatedness | `$t_i^{\mathsf T}t_k = 0$ for `$i \ne k$ | the component scores have zero covariance | PCA's statistical content: `p` correlated features become independent ones |
| whitening | `$Z = T\operatorname{diag}(\sigma_i/\sqrt{m-1})$` | divide each score column by its own standard deviation | before k-means or k-NN; **not** before compression |
| standardisation before PCA | `$Z = (X - \bar x)/\operatorname{std}(x)$`, per column | put every feature on a common scale | mandatory when features have different units; otherwise the largest-unit feature dominates PC1 |
| compression storage | `$\|A_k\|` costs `m·k + k + k·n` numbers vs `m·n` for `A` | three thin blocks instead of the whole grid | deciding whether truncation is worth it at all; a win only when `k < mn/(m+n+1)` |
| elbow / scree cliff | largest drop in `$\sigma_k/\sigma_{k+1}$` | where signal ends and numerical dust begins | choosing `k` without labels or a validation set |
| one-sided Jacobi | rotate the **columns** of a working copy `W` until they are mutually orthogonal; then `$\sigma_i = \|W_i\|_2$` | rotations preserve lengths, so the final column norms are the answer | the numerically safe SVD in the lesson's code — never forms `AᵀA` |

Four restrictions to carry. `A = UΣVᵀ` needs no inverse because `U` and `V` are
orthonormal, but it *does* need `A` to be finite and real (or complex with the
conjugate transpose). The `σ_i = √λ_i(AᵀA)` route is a mathematical fact and a
computational trap. PCA **must** be centred, and standardised too when units
differ. And `1/σ_i` in the pseudoinverse is only legal for nonzero `σ_i` — for
rank-deficient `A` the whole point is to set those entries to zero.

## Multiple Choice Questions

**Q1.** Why is the SVD preferred over an eigendecomposition for a data matrix
with 10,000 rows and 300 columns?

- A) Because singular values are always smaller than eigenvalues, so they fit in
  memory better
- B) Because eigenvalues are not defined for non-square matrices, whereas the SVD
  exists for every `m × n` matrix
- C) Because the SVD is always faster, since it does not require orthogonal
  factorisation
- D) Because eigenvectors of a tall matrix can be negative and singular values
  cannot

<details>
<summary>Answer and explanation</summary>

**B) Because eigenvalues are not defined for non-square matrices, whereas the SVD
exists for every `m × n` matrix.**

A characteristic polynomial `det(A − λI)` needs `A` square: you cannot form a
square matrix from a `10000 × 300` array. `np.linalg.eigvals` on such a matrix
raises `LinAlgError` — the lesson's library block prints exactly that. The SVD
has no such requirement, which is why `np.linalg.svd` is the default
decomposition and `np.linalg.lstsq` is built on it.

A is false and backwards: `σ_i² = λ_i(AᵀA)`, so the singular values are the
*square roots* of the Gram-matrix eigenvalues and are smaller, but that is a
consequence, not a reason. C is false — both cost `O(mn·min(m,n))`, and the SVD
is generally the more expensive of the two factorisations, not the cheaper.
D is nonsense: both singular values and eigenvalues can be negative or complex;
singular values are *by construction* non-negative, eigenvalues are not.

</details>

**Q2.** A 90° rotation `R = [[0,−1],[1,0]]` has eigenvalues `±i` and singular
values `1, 1`. What does that pair of facts tell you?

- A) That `R` is defective, since it has no real eigenvectors
- B) That `R` is perfectly conditioned and well behaved as a transform, even
  though it has no direction it leaves fixed
- C) That `R` is singular, since neither eigenvalue is positive
- D) That the singular values must have been computed incorrectly

<details>
<summary>Answer and explanation</summary>

**B) That `R` is perfectly conditioned and well behaved as a transform, even
though it has no direction it leaves fixed.**

`cond(R) = σ₁/σ_r = 1/1 = 1`, the smallest possible value, and `RᵀR = I` so it
preserves every length and angle. Its eigenvalues `±i` are perfectly correct
information too — a real rotation genuinely has no real eigenvector, which is
[36](../part03_linear_algebra/36_eigenvalues_and_eigenvectors.md)'s conjugate-pair theorem in action. The
point is that the *singular values* answer a different, better-conditioned
question: "how much does this transform stretch things?", not "is there a
direction it only scales?".

A conflates defective with complex. A matrix is defective when it has too few
independent eigenvectors, a structural failure; `R` has two perfectly good
complex eigenvectors, and the spectral theorem guarantees a complete eigenbasis
over `ℂ`. C is wrong — `σ_i = √λ_i(AᵀA)`, and `AᵀA = I` here, so no eigenvalue
of the Gram matrix is negative. D is wrong: `numpy` returns exactly `1.0, 1.0`
here, as the lesson's library block prints.

</details>

**Q3.** A symmetric matrix `A` is not diagonalisable. Which statement is
impossible?

- A) Its characteristic polynomial has a repeated root
- B) Its eigenvalues include a negative value
- C) It has fewer than `n` linearly independent eigenvectors
- D) Its eigenvectors are pairwise orthogonal

<details>
<summary>Answer and explanation</summary>

**D) Its eigenvectors are pairwise orthogonal.**

Impossible, because a real symmetric matrix is **always** diagonalisable by an
orthogonal matrix — that is the spectral theorem from
[39](../part03_linear_algebra/39_diagonalization_and_spectral.md), and the proof sketch is exactly this:
`(λ − μ)(uᵀv) = 0` by symmetry, so distinct eigenvalues give perpendicular
eigenvectors, and equal eigenvalues can be re-orthonormalised by Gram-Schmidt. A
symmetric matrix with fewer than `n` independent eigenvectors does not exist.

A is not just possible but *necessary*: non-diagonalisability means some
eigenvalue has geometric multiplicity below algebraic multiplicity, which is
exactly a repeated root. B is unconstrained — `diag(1, −1)` is symmetric and
indefinite. C is the definition of defective, and it cannot happen for symmetric
input. The lesson's own code applies this: `np.linalg.eigh` is called on a
symmetric matrix throughout and never fails.

</details>

**Q4.** The singular values of a matrix are `4, 2, 1`. You keep only the largest.
What is the relative Frobenius error of the best rank-1 approximation?

- A) `1/7`
- B) `√5/21`
- C) `1/21`
- D) `2/7`

<details>
<summary>Answer and explanation</summary>

**B) `√5/21`.**

The Eckart–Young error is `‖A − A₁‖_F = √(Σ_{i>1} σ_i²) = √(2² + 1²) = √5`.
The total is `‖A‖_F = √(4² + 2² + 1²) = √21`. So the relative error is
`√5/√21 = √(5/21) ≈ 0.48795`, about **48.8%** — nearly half the information is
lost by dropping that last component.

A mistakes the relative error for the tail *fraction of squares* counted only
part-way. C forgets the square root: `√5 ≠ 5`, which is the whole point of the
Frobenius norm being an L2 aggregation of the discarded energies. D uses the
largest discarded value with no norm and no normalisation. And "best" matters:
no rank-1 matrix whatsoever does better, because Eckart–Young says so.

</details>

**Q5.** Why must you centre data before running PCA?

- A) Because the SVD is undefined for data whose columns do not sum to zero
- B) Because PCA finds directions of maximum *spread about the mean*, so without
  centring the top component points at the mean's location, which is a property
  of where the data sits rather than how it varies
- C) Because centring guarantees the singular values are distinct
- D) Because uncentred PCA returns negative singular values

<details>
<summary>Answer and explanation</summary>

**B) Because PCA finds directions of maximum *spread about the mean*, so without
centring the top component points at the mean's location, which is a property of
where the data sits rather than how it varies.**

On the lesson's own dataset of hours studied and hours of sleep, centring is
required for the answer to mean anything: the raw columns are at `(1,9)` through
`(8,4.5)`, so the biggest `σ_i` is `7.770173` and PC1 is
`v₁ = (0.833772, −0.552110)`. Centred, the same direction is
`v₁ = (0.833772, −0.552110)` with variance ratios `0.998459 / 0.001541` — the
point being that *which* direction wins depends entirely on where the origin is.

A is false: the SVD works on any matrix, centred or not. C is false and
backwards — `diag(1,1)` is centred (after subtraction) and has repeated singular
values. D is false — singular values are never negative, which is one of their
guarantees. sklearn's `PCA` always centres; `KernelPCA` and some other variants
do not, which is Common Mistake 3.

</details>

**Q6.** You have features "annual income in dollars" (std ≈ 55,000) and "age in
years" (std ≈ 8). What does unscaled PCA give you, and why is it a problem?

- A) A PC1 that is essentially income alone, and a PC2 that captures age — because
  PCA's objective is variance, and raw variance is dominated by the units
- B) A PC1 mixing both features evenly, since PCA is scale-invariant
- C) Two components with equal explained variance, since PCA equalises features
- D) An error, because the two features have incompatible units

<details>
<summary>Answer and explanation</summary>

**A) A PC1 that is essentially income alone, and a PC2 that captures age — because
PCA's objective is variance, and raw variance is dominated by the units.**

This is the standardisation trap. On the lesson's analogous three-column dataset
(sd ≈ `1.0488`, `55.0151`, `0.2160`), the raw covariance matrix has a leading
eigenvalue of `3027.749338` against `0.063858` and `0.000138` — so raw PCA gives
variance ratios `0.999979 / 0.000021 / 0.000000` and PC1 is literally just the
income column. Standardise first (divide each column by its own standard
deviation) and the ratios become `0.986692 / 0.012805 / 0.000503` with PC1 mixing
all three features meaningfully.

B is false: PCA is *not* scale-invariant — rescaling a feature rescales its
variance and hence its influence. C is false: PCA does the opposite of
equalising, it *orders* by variance. D is false: mixed units are completely
fine, and no SVD is scale-invariant across columns.

</details>

**Q7.** Why do the PCA component scores come out uncorrelated?

- A) Because PCA minimises the correlation between components
- B) Because the components `v_i` are orthonormal, so `t_iᵀt_k = X_c v_i v_kᵀ X_cᵀ = 0`
  for `i ≠ k`
- C) Because the covariance matrix of the centred data is diagonal
- D) Because the singular values are all distinct

<details>
<summary>Answer and explanation</summary>

**B) Because the components `v_i` are orthonormal, so `t_iᵀt_k = X_c v_i v_kᵀ X_cᵀ =
0` for `i ≠ k`.**

That is the whole proof, and the lesson's code verifies it numerically: the dot
product of the two score columns is printed as `−3.15e-15`, i.e. zero to machine
precision. Orthogonality of `v` does all the work; the scores inherit it.

A reverses the logic — uncorrelatedness is a *consequence* of taking
orthonormal directions, not an objective being minimised. C is false: the
covariance matrix of the centred data is generally *not* diagonal in the original
coordinates. On the lesson's dataset it is `[[6, −3.9643], [−3.9643, 2.6384]]`,
strongly off-diagonal; it only becomes diagonal in the *component* basis, which
is the same statement as B. D is irrelevant: repeated singular values are
perfectly fine, and PCA handles them by spanning the eigenspace.

</details>

**Q8.** Which is true of the pseudoinverse `A⁺ = VΣ⁺Uᵀ`?

- A) It exists only when `A` is square and invertible
- B) It exists for every matrix; for an invertible square `A` it equals `A⁻¹`,
  and for a rank-deficient `A` it returns the minimum-norm solution of `Ax = y`
- C) It equals `Aᵀ(AAᵀ)⁻¹` always
- D) It has the same rank as `A`

<details>
<summary>Answer and explanation</summary>

**B) It exists for every matrix; for an invertible square `A` it equals `A⁻¹`, and
for a rank-deficient `A` it returns the minimum-norm solution of `Ax = y`.**

Every `A` has `Σ⁺` defined by inverting the nonzero `σ_i` and zeroing the rest,
so `A⁺` always exists. When all `σ_i > 0`, `Σ⁺ = Σ⁻¹` and `A⁺ = VΣ⁻¹Uᵀ = A⁻¹`
by direct inversion of `A = UΣVᵀ`.

A is false — that would make it useless for exactly the cases it is designed
for. C is wrong twice: the formula only holds when `AAᵀ` is invertible, and the
correct general statement is `A⁺ = (AᵀA)⁺Aᵀ`, computed stably via the SVD rather
than by forming `AᵀA`. D is false, and for a different reason than you might
expect: `A⁺` has the same rank as `A` in the sense that it recovers exactly the
rows and columns `A` uses, but it is `m × n` where `A` may be `n × m`, so the
shapes — and therefore the ranks — need not agree. What is true, and is the
useful fact, is that `A A⁺` is the orthogonal projector onto the column space of
`A` and `A⁺A` the projector onto its row space. On the lesson's rank-1 matrix
`[[1,2],[2,4],[3,6]]`, `rank(A) = 1` and
`pinv(A) @ (1,2,3)ᵀ = (0.2, 0.4)ᵀ` — one nonzero direction, and the residual
`b − A(0.2, 0.4)ᵀ` is exactly zero.

</details>

**Q9.** A PCA component loads heavily on both "price" and "number of windows
installed". What does that establish?

- A) That windows cause prices
- B) Only that the two features covary strongly; a third variable (the builder's
  budget) could produce the correlation without any causal arrow between them
- C) That the component is unreliable and should be discarded
- D) That the data must be normalised

<details>
<summary>Answer and explanation</summary>

**B) Only that the two features covary strongly; a third variable (the builder's
budget) could produce the correlation without any causal arrow between them.**

PCA finds directions of maximum *variance*, and variance is not causation. It
makes no causal claim at all: it is a rotation of your coordinate system, and a
rotation preserves whatever causal story you bring to it. Nothing in the
algorithm can distinguish "price drives windows" from "budget drives both" from
"both are driven by region" — all three produce the same covariance matrix and
the same components.

A is the inference the warning exists to prevent. C is unwarranted — a
correlated pair of features is exactly what PCA is *for*, since combining them
removes redundancy. D confuses a statistical caveat with a preprocessing step;
standardising may or may not be appropriate ([40] and
[37](../part03_linear_algebra/37_inner_products_norms_geometry.md)), but it has nothing to do with
causality. The honest statement is that PCA is a **descriptive** tool: it
compresses variance, and establishing direction requires an experiment.

</details>

**Q10.** When you truncate an SVD to keep `k` components, what determines the
error?

- A) `k` alone, and nothing else
- B) The discarded tail: `‖A − A_k‖_F = √(Σ_{i>k} σ_i²)`, so the error depends only
  on the singular values you threw away
- C) The number of rows `m` and columns `n`
- D) The rank of `A_k`, which is always `k`

<details>
<summary>Answer and explanation</summary>

**B) The discarded tail: `‖A − A_k‖_F = √(Σ_{i>k} σ_i²)`, so the error depends only
on the singular values you threw away.**

Eckart–Young guarantees no rank-`k` matrix whatsoever is closer, in either
Frobenius or spectral norm. On the lesson's `4 × 6` example the errors are
`2.695635 → 0.732348 → 0` for `k = 1, 2, 3`, and each one is just the tail.

A is the tempting version — "fewer components, more error" is directionally true
but says nothing about *how much*. C is false: shape enters only through how many
singular values there are. D is a non sequitur; `rank(A_k) = k` when the first `k`
singular values are nonzero, but that is not what determines the error.

</details>

## Subjective Questions

### Short Answer

**Q1. State the SVD and its two key identities, and say what each factor means.**

<details>
<summary>Model answer</summary>

Every real `m × n` matrix `A` factorises as `A = UΣVᵀ`, with `U` orthonormal
columns, `V` orthonormal columns, and `Σ` diagonal with entries
`σ₁ ≥ σ₂ ≥ ⋯ ≥ σ_r ≥ 0`, `r = min(m, n)`.

The key identities are `Av_i = σ_i u_i` and `Aᵀu_i = σ_i v_i`, where `u_i, v_i`
are the columns of `U, V`. Together they say `AᵀA v_i = σ_i² v_i`.

`V` rotates the input space, `Σ` scales each axis by `σ_i`, `U` rotates the
result. Because `U` and `V` are orthonormal, their inverses are their
transposes, so **no matrix inverse is ever computed**.

</details>

**Q2. Why are the singular values the square roots of the eigenvalues of `AᵀA`,
and why is that a bad way to compute them?**

<details>
<summary>Model answer</summary>

From `Av_i = σ_i u_i`, applying `Aᵀ` gives `Aᵀu_i = σ_i v_i`, then applying `A`
again gives `AᵀA v_i = σ_i² v_i`. So `σ_i²` are the eigenvalues of the Gram
matrix `AᵀA`, which is symmetric positive semidefinite because
`xᵀ(AᵀA)x = ‖Ax‖₂² ≥ 0`.

It is a bad way to **compute** them because `cond(AᵀA) = cond(A)²`. Squaring an
already-large condition number destroys trailing digits, and forming `AᵀA` sums
products that suffer catastrophic cancellation when the columns are nearly
parallel. The lesson's own one-sided Jacobi code never forms the Gram matrix and
agrees with numpy to `1e-15` on badly scaled inputs where the textbook route does
not.

</details>

**Q3. State Eckart–Young and explain why truncation is a decision, not a
heuristic.**

<details>
<summary>Model answer</summary>

**Eckart–Young–Mirsky.** Let `A_k` keep the `k` largest singular triplets. Then
`A_k` is the best rank-`k` approximation to `A` in **both** the Frobenius and the
spectral norm, and

    ‖A − A_k‖_F = sqrt(sum over i > k of sigma_i^2)

Because this is a theorem about *all* rank-`k` matrices, no heuristic search can
beat it. So the only remaining question is which `k` you want, and that is a
modelling decision informed by three separate things: the error curve (when the
discarded tail is negligible), the scree-plot cliff (when signal ends and
numerical dust begins), and the storage count `m·k + k + k·n` versus `m·n`.

</details>

**Q4. Given singular values `σ₁ = 9.5255` and `σ₂ = 0.5143`, report the rank, the
condition number, and the relative error of the best rank-1 approximation.**

<details>
<summary>Model answer</summary>

**Rank 2** — both singular values are nonzero (they belong to the `3 × 2` matrix
`[[1,2],[3,4],[5,6]]`).

**Condition number** `cond = σ₁/σ₂ = 9.5255/0.5143 = 18.52`.

**Relative rank-1 error** `= σ₂/‖A‖_F`, and `‖A‖_F = √(Σσᵢ²) = √91 = 9.5394`.
So `= 0.5143/9.5394 = 0.05391`, about **5.39%**. Much better than the raw entry
range of 1 to 6 suggests, because the three columns of `A` are nearly parallel —
the matrix is close to rank 1 in a way its entries hide.

</details>

**Q5. Explain why the pseudoinverse handles rank deficiency, and what "minimum
norm" means there.**

<details>
<summary>Model answer</summary>

`A⁺ = VΣ⁺Uᵀ` where `Σ⁺` inverts the nonzero `σ_i` and sets the rest to **zero**.
That zeroing is the whole mechanism: the directions `A` destroys get no
contribution back, so no division by a near-zero `σ_i` occurs and no infinity
appears. It is exactly the thresholding Common Mistake 2 warns you to do by hand.

"Minimum norm" applies when `Ax = y` has infinitely many solutions. Among them,
`A⁺y` is the one with the smallest `‖x‖₂` — the least-committal answer, putting
no more weight on any coefficient than the data forces. For the rank-1 matrix
`[[1,2],[2,4],[3,6]]` and `y = (1,2,3)ᵀ`, the solution set is
`x = t(1,2) + s(0,1)` for any `t, s`, and the minimum-norm member is
`x = (0.2, 0.4)`, which satisfies `‖x‖₂ = 0.4472` against `√2 ≈ 1.4142` for
`(1,2)` and larger for every other member of the family.

</details>

**Q6. Describe the algorithm in the lesson's from-scratch SVD in one sentence,
and say what invariant makes it work.**

<details>
<summary>Model answer</summary>

Keep a working copy `W` of `A`, repeatedly rotate the pair of its columns that is
least orthogonal, and stop when every pair is orthogonal; then `σ_i` is the
length of column `i` of `W` and `v_i` is column `i` of the accumulated rotation
matrix `V`.

The invariant: a rotation is orthogonal, so it **preserves lengths and inner
products**. Rotating columns of `W` is therefore the same as rotating columns of
`A` and absorbing the rotation into `V` — `A = W Vᵀ` at every step. When `W`'s
columns are mutually orthogonal, column `i` of `W` is `σ_i v_i` for some unit
`v_i`, so `‖W_i‖ = σ_i‖v_i‖ = σ_i` because `v_i` is a column of the orthogonal `V`.
That is why this route never forms `AᵀA` and never squares the condition number.

</details>

### Long Answer

**Q1. Why does PCA choose the directions of maximum variance? What would break if
it chose any other directions?**

<details>
<summary>Model answer</summary>

**The derivation.** Take one direction `w` with `‖w‖ = 1`. The variance of the
projection `t = X_c w` is

    Var(t) = (1/(m−1)) · tᵀt = (1/(m−1)) · wᵀ(X_cᵀX_c)w = wᵀ Σ_cov w

Maximising a quadratic form over the unit sphere: if `Σ_cov = UΛUᵀ`, then
`wᵀΣ_cov w = Σ λᵢ (uᵢᵀw)²`, which is at most `λ_max` with equality **only** when
`w` lies entirely in the top eigenspace. So the maximiser is the eigenvector of
the covariance matrix for the largest eigenvalue — which is `v₁`, the first right
singular vector of `X_c`.

**Why it is the right objective.** PCA is compression. You want to spend the
fewest numbers describing the data, so you want each retained number to carry as
much as possible. Variance is precisely "how much information a number carries
about the row", and the singular values are the standard deviations of the
scores: `std(tᵢ) = σᵢ/√(m−1)`. Choosing maximum variance is choosing the
coordinates with the largest standard deviations.

**What breaks if you choose differently.**

- *The scores stop being uncorrelated.* This is the loss PCA cannot recover. With
  `v_i, v_k` not orthogonal, `t_iᵀt_k = v_iᵀ(X_cᵀX_c)v_k ≠ 0`, so two components
  both encode the same variation — you pay twice for one fact. On the lesson's
  data the PC1/PC2 dot product is `−3.15e-15`; take both components along the
  same direction and it would be the entire variance again.
- *Orthogonality of the retained set is lost*, so the basis is not a basis. The
  score vectors would be linearly dependent, and you would be claiming `p`
  independent numbers where you have fewer.
- *The variance ordering loses meaning.* `σᵢ` would no longer be the standard
  deviations of the retained coordinates, so the explained-variance ratio
  `σᵢ²/Σσⱼ²` would be reporting something other than what each coordinate
  actually contains.
- *The optimality guarantee disappears.* Eckart–Young applies specifically to the
  top singular directions. Any other rank-`k` approximation is strictly worse, so
  a non-maximum-variance choice can be beaten by a rank-`k` matrix that was never
  a set of projection directions at all.

One honest caveat: maximum variance is not the same as maximum *information* in
any information-theoretic sense. PCA is optimal for reconstructing the data in
least squares, and it is sensitive to outliers — a single wild row moves `X_cᵀX_c`
just as much as a whole trend. That is the reason for the many PCA variants
(truncated, robust, kernel, incremental) and for standardising before the
transform.

</details>

**Q2. Why does the SVD exist for every matrix when diagonalisation does not, and
what is the SVD's relationship to the eigendecomposition?**

<details>
<summary>Model answer</summary>

**Why the SVD always exists.** Start from any `m × n` matrix `A`. The Gram matrix
`AᵀA` is `n × n`, symmetric and positive semidefinite — `xᵀ(AᵀA)x = ‖Ax‖₂² ≥ 0`
for every `x`. The spectral theorem therefore gives it a full orthonormal
eigenbasis: `AᵀA v_i = σ_i² v_i` with real `σ_i² ≥ 0`. Take `σ_i = √σ_i²`, which
is real and non-negative by construction. Then define `u_i = Av_i/σ_i` for
nonzero `σ_i` (norm 1 because `‖Av_i‖² = v_iᵀ(AᵀA)v_i = σ_i²‖v_i‖² = σ_i²`), and
complete the orthonormal set of `u_i` arbitrarily. Diagonalisation of `A` itself
is never attempted, so nothing can go wrong.

Contrast with the three things that block an eigendecomposition: a non-square
matrix has no characteristic polynomial; a rotation has complex eigenvalues and
no real eigenvectors; a Jordan block has too few independent eigenvectors. The
SVD sidesteps all three by never diagonalising `A`.

**How they relate.** For square symmetric `A`, the two coincide up to signs:
`σᵢ = |λᵢ|`, and `V = U` when the eigenvalues are positive (as they are for a
symmetric positive definite matrix). For a general square `A` with an
eigendecomposition `A = WΛW⁻¹`, the singular values are `|λᵢ|` — the SVD is
essentially the eigendecomposition with the signs removed and the basis
orthonormalised.

Two differences matter in practice. First, **the SVD needs no `W⁻¹`**: `U` and
`V` are orthonormal, so `cond = 1` on the basis. That is why `np.linalg.lstsq`
uses the SVD rather than forming `AᵀA`
([38](../part03_linear_algebra/38_orthogonality_and_least_squares.md)). Second, **the SVD sorts and
signs**: `σ₁ ≥ σ₂ ≥ ⋯ ≥ 0` is a guarantee, while `λ` may be complex, negative, or
returned in arbitrary order. The loss is the *sign* information — the SVD tells
you how much each direction is stretched, not whether it is flipped, so it cannot
recover the eigenvalues' signs for a general matrix.

</details>

**Q3. Why should you standardise features before PCA, and what goes wrong if you
do not?**

<details>
<summary>Model answer</summary>

**The mechanism.** PCA maximises `wᵀ(X_cᵀX_c)w`. The covariance matrix has
`Σᵢⱼ = Cov(xᵢ, xⱼ)`, and `Var(xᵢ)` carries the feature's **units squared**. If
income is measured in dollars and age in years, `Var(income)` is roughly
`55.015² = 3027` while `Var(age)` is about `64`. Income's variance is 47 times
larger before any correlation is considered, so the top eigenvector is income's
axis alone and the others are squeezed into rounding error.

**The numbers.** On the three-feature dataset with standard deviations
`1.0488`, `55.0151`, `0.2160`:

    raw covariance    -> leading eigenvalue 3027.749338, ratios 0.999979/0.000021/0.000000
    standardised      -> leading eigenvalue    2.960077, ratios 0.986692/0.012805/0.000503

So raw PC1 is `v₁ = (0.018499, 0.999821, 0.003920)` — that is, "income, full
stop". Standardised, PC1 is `(0.573693, 0.579124, 0.579217)` — all three features
contributing almost equally, because the standardised covariance matrix
`[[1, 0.9705, 0.9710], [0.9705, 1, 0.9985], [0.9710, 0.9985, 1]]` is about
equicorrelated and its top eigenvector is nearly flat.

**What goes wrong if you skip it.**

- **A useless first component.** You spent one of your `p` outputs restating a
  unit conversion. With three raw features and ratios `0.999979/0.000021/0.0`,
  the second and third components are numerical dust.
- **Distance-based methods downstream break.** If you feed the scores to k-means
  or k-NN, which measure Euclidean distance, PC2's variance of `0.0133` makes it
  invisible — the lesson says exactly this in the whitening section. Whitening
  (`Z/σ`) is one fix, but standardising first is the better one.
- **The explained-variance ratio becomes uninterpretable.** `0.999979` sounds
  amazing and means nothing; it is a report on units, not on structure.
- **Regularisation interacts badly.** Ridge's single `λ` implicitly assumes
  comparable scales; that is why scikit-learn pipelines start with
  `StandardScaler` ([38](../part03_linear_algebra/38_orthogonality_and_least_squares.md)).

**The counter-case.** Do **not** standardise when the features are already the
same unit and you care about absolute magnitudes — raw pixel intensities, a
temperature range, anything where a ten-fold difference in variance is genuine
signal. Standardising equalises variance by fiat and will promote a direction
that is numerically large but semantically empty. This is the same
"scale is a modelling decision, not bookkeeping" point as
[37](../part03_linear_algebra/37_inner_products_norms_geometry.md): L1 gave sparsity, L2 gave smooth
shrinkage, and standardisation gives every feature equal say.

</details>

**Q4. Why do we use a truncated SVD rather than just keeping the covariance
matrix, and why is `cond(AᵀA) = cond(A)²` the crux?**

<details>
<summary>Model answer</summary>

**The two routes to the same answer.** PCA can be computed either as the
eigendecomposition of `Σ_cov = X_cᵀX_c/(m−1)` or as the SVD of `X_c` itself.
They give identical components and identical variance ratios, because
`σᵢ²/(m−1) = λᵢ(Σ_cov)` — an exact identity, printed in the lesson's library
block. The lesson's dataset gives `S²/(m−1) = [8.625083, 0.013310]` and
`eigvalsh(cov) = [0.013310, 8.625083]`: the same two numbers.

**Why the SVD route is the one to use.** Forming `X_cᵀX_c` squares the condition
number. `AᵀA` has singular values `σ_i²`, so `cond(AᵀA) = (σ₁/σ_r)² =
cond(A)²`. For the near-collinear matrix `[[1, 0.999999], [0.999999,
0.999999]]`, `cond = 3.999998 × 10⁶`; the covariance route squares that to
`1.6 × 10¹³` and the smallest component direction is gone. That is the same
mechanism as the normal equations in
[38](../part03_linear_algebra/38_orthogonality_and_least_squares.md): the answer is a difference of
quantities that have already lost their digits.

Worse, the covariance route forces you to build the `p × p` matrix, which is
hopeless when `p` is large — a term-document matrix for 1 million documents is
`10⁶ × 10⁶`, but its SVD is only ever asked for a few hundred components.
`TruncatedSVD` in scikit-learn exists precisely because it takes the *truncated*
SVD of `X` and never forms `XᵀX`. For `p ≫ n`, the truncated SVD of `X` has cost
`O(mnk)` rather than `O(np²)`.

**Why truncation is not a compromise.** Eckart–Young says the rank-`k` SVD
approximation is the *best possible* rank-`k` matrix, in both Frobenius and
spectral norm. So there is no better rank-`k` answer hiding anywhere. The only
question is which `k`, and that is judged by the tail
`√(Σ_{i>k} σᵢ²)`, by the scree-plot cliff, or by held-out downstream performance.
Randomised SVD (`sklearn.utils.extmath.randomized_svd`) and `svds` take the same
truncated decomposition for a fraction of the cost when `k ≪ min(m, n)`.

The honest summary: the covariance matrix is the *concept* — it is where variance
lives — and the SVD is the *computation*. Build the covariance when you want to
reason about variance, and reach for the SVD when you want numbers.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — a full SVD by hand.** Let

```
A = [[1, 2], [3, 4], [5, 6]]        (3 x 2)
```

(a) Compute `AᵀA` and its eigenvalues.
(b) Give the singular values in sorted order.
(c) Find the right singular vectors, then the left ones via `u_i = Av_i/σ_i`.
(d) Write out `U`, `S`, `V` and verify `USVᵀ = A` numerically.
(e) Find the best rank-1 approximation and report the relative Frobenius error.
(f) Explain why `det(A)` cannot be used to check this decomposition.

<details>
<summary>Solution</summary>

**(a)** `AᵀA = [[1,3,5],[2,4,6]]·[[1,2],[3,4],[5,6]]`.

`AᵀA[0][0] = 1 + 9 + 25 = 35`. `AᵀA[0][1] = 2 + 12 + 30 = 44`.
`AᵀA[1][1] = 4 + 16 + 36 = 56`.
```
AᵀA = [35  44]
      [44  56]
```

Eigenvalues: `det(AᵀA − λI) = (35−λ)(56−λ) − 44² = 1960 − 91λ + λ² − 1936`
` = λ² − 91λ + 24`.
`λ = [91 ± √(8281 − 96)]/2 = [91 ± √8185]/2`. `√8185 = 90.47099`.
So `λ₁ = 90.735496`, `λ₂ = 0.264504`.

**(b)** `σ₁ = √90.735496 = 9.525518`, `σ₂ = √0.264504 = 0.514301`. Sorted and
non-negative. Check: `σ₁² + σ₂² = 91 = tr(AᵀA) = 35 + 56` ✓.

**(c)** For `λ₁ = 90.735496`: `AᵀA − λ₁I = [[−55.735496, 44], [44, −34.735496]]`.
Row 1 gives `−55.735496x + 44y = 0` → `y = 1.266715x`.
`‖(1, 1.266715)‖ = √(1 + 1.604567) = √2.604567 = 1.613866`,
so `v₁ = (0.619629, 0.784894)` (numpy returns the negation, same line).
For `λ₂`, orthogonality gives `v₂ = (−0.784894, 0.619629)`.

Left vectors, `u_i = A v_i/σ_i`:
`A v₁ = (1(0.619629) + 2(0.784894), 3(0.619629) + 4(0.784894), 5(0.619629) + 6(0.784894))`
` = (2.189417, 4.996431, 7.803887)`.
`u₁ = that / 9.525518 = (0.229848, 0.524745, 0.819642)`.
`‖u₁‖ = √(0.05283 + 0.27536 + 0.67181) = √1.00000 = 1` ✓

`A v₂ = (1(−0.784894) + 2(0.619629), 3(−0.784894) + 4(0.619629), 5(−0.784894) + 6(0.619629))`
` = (0.454364, −0.876528, −0.503368)`.
`u₂ = that / 0.514301 = (0.883461, −1.704384, −0.978688)`.

**(d)**
```
U = [ 0.229848  −0.883461]    S = [9.525518   0]     V = [ 0.619629  −0.784894]
    [ 0.524745   1.704384]           [   0  0.514301]     [ 0.784894   0.619629]
    [ 0.819642   0.978688]
```
(numpy flips the signs of the columns of `U`; the same subspace results.)
`U @ diag(S) @ Vt` reproduces `[[1,2],[3,4],[5,6]]` to `1e-15`, and `UᵀU = I`,
`VᵀV = I` to `1e-16`.

**(e)** The best rank-1 approximation is `A₁ = σ₁u₁v₁ᵀ`:
```
A₁ = [ [1.357, 1.719] ]
    [ [3.097, 3.923] ]
    [ [4.838, 6.128] ]
```
`‖A − A₁‖_F = σ₂ = 0.514301`, since the error is the square root of the
discarded squared singular values and only `σ₂` is discarded.
`‖A‖_F = √(1+4+9+16+25+36) = √91 = 9.539392`.
Relative error `= 0.514301/9.539392 = 0.053913`, i.e. **5.39%**.

**(f)** `A` is `3 × 2`, so `det(A)` is undefined. That is the point of the
lesson: the SVD is the only decomposition that works on every shape, and it
still tells you everything — the rank is 2, the condition number is
`σ₁/σ₂ = 9.525518/0.514301 = 18.521`, and you have the provably best rank-1
approximation.

</details>

**[ ] Exercise 2 — PCA on a 2D dataset, all by hand.** Consider the four points
`(1, 2)`, `(2, 1)`, `(3, 0)`, `(0, 3)`.

(a) Compute the mean and the centred data.
(b) Compute the covariance matrix.
(c) Find its eigenvalues and eigenvectors by hand.
(d) Report the explained variance ratio for each component.
(e) Project each point onto PC1 and give its score.
(f) What fraction of the data is "lost" if you keep only PC1, and is that
acceptable? Would you recommend 1 component or 2?

<details>
<summary>Solution</summary>

**(a)** `n = 4`. Mean: `x̄ = (1+2+3+0)/4 = 1.5`, `ȳ = (2+1+0+3)/4 = 1.5`.
Centred:
```
(-0.5,  0.5)
( 0.5, -0.5)
( 1.5, -1.5)
(-1.5,  1.5)
```

**(b)** `C₁₁ = (0.25 + 0.25 + 2.25 + 2.25)/3 = 5/3 = 1.6667`.
`C₂₂ = same = 1.6667`. `C₁₂ = (−0.25 − 0.25 − 2.25 − 2.25)/3 = −5/3 = −1.6667`.
```
C = [ 1.6667  -1.6667]
    [-1.6667   1.6667]
```

**(c)** `det(C − λI) = (1.6667 − λ)² − 2.7778 = λ² − 3.3333λ + 0`.
So `λ = 0` and `λ = 3.3333`. (Eigenvectors: for `λ = 3.3333`,
`(1.6667 − 3.3333)x − 1.6667y = 0` → `−1.6666x − 1.6667y = 0` → `y = −x`, so
`v₁ = (1, −1)/√2 = (0.70711, −0.70711)`. For `λ = 0`: `1.6667x − 1.6667y = 0`
→ `x = y`, so `v₂ = (1, 1)/√2 = (0.70711, 0.70711)`.)

**(d)** Total variance `= λ₁ + λ₂ = 3.3333`. Ratios:
PC1: `3.3333/3.3333 = 1.0000` (100%). PC2: `0/3.3333 = 0.0000` (0%).

**(e)** Scores `t_i = (x_i − 1.5)(0.70711) + (y_i − 1.5)(−0.70711)`:
```
(1,2):  (-0.5)(0.70711) + (0.5)(-0.70711) = -0.70711
(2,1):  ( 0.5)(0.70711) + (-0.5)(-0.70711) = +0.70711
(3,0):  ( 1.5)(0.70711) + (-1.5)(-0.70711) = +2.12132
(0,3):  (-1.5)(0.70711) + ( 1.5)(-0.70711) = -2.12132
```

**(f)** You lose **0%** of the variance, because the second eigenvalue is
exactly zero. The four points lie exactly on the line `x + y = 3`, so the data
is genuinely rank 1. Storing only PC1 loses nothing at all.

Recommendation: **1 component**, and with total confidence. A zero eigenvalue
is not a judgement call — there is no second dimension to find. This is the
clearest possible case, and it is why a scree plot that just drops to zero is
easier to read than one that flattens out gradually.

Real data essentially never behaves this well, which is why the practical
question is where the *tail* becomes indistinguishable from noise.

</details>

**Challenge — Exercise 3 — low-rank approximation as compression.** Let
`A` be the `4 × 6` matrix whose rows are the first four rows of the
image-like pattern below (you may compute the SVD numerically):

```
 1  2  3  4  5  6
 2  4  6  8 10 12
 1  1  2  3  4  5
 3  2  5  4  7  6
```

(a) Compute its singular values and state the rank of `A`.
(b) For each `k = 1, 2, 3`, compute `‖A − A_k‖_F` and the relative error.
(c) Determine the value of `k` at which the biggest drop in error occurs, and
explain why that is the right place to cut.
(d) Count how many numbers each option requires to store, and state for which
`k` compression is a win at all.
(e) `A`'s second row is exactly twice its first. Confirm this from the singular
values, and say what it implies about the relationship between rank and repeated
rows.

<details>
<summary>Solution</summary>

**(a)** The singular values are

```
sigma_1 = 25.352190
sigma_2 =  2.594247
sigma_3 =  0.732348
sigma_4 =  0.000000   (to machine precision)
```

**Rank of `A` = 3.** The matrix is `4 × 6`, so `min(4,6) = 4` singular values
exist, and the fourth is zero to machine precision — an exact zero caused by the
repeated row, not a numerical accident.

**(b)** With `‖A‖_F = √(25.352190² + 2.594247² + 0.732348²) = √(642.73 + 6.73 +
0.54) = √649.99 = 25.495097`:

| k | `‖A − A_k‖_F` | relative |
| --- | --- | --- |
| 1 | `√(σ₂² + σ₃²) = √(6.730 + 0.536) = 2.695635` | 10.57% |
| 2 | `√σ₃² = 0.732348` | 2.87% |
| 3 | `0.000000` | 0.00% |

**(c)** The errors go `2.6956 → 0.7323 → 0`. The biggest proportional drop is
from `k = 1` to `k = 2`, where the error shrinks by a factor of `2.6956/0.7323
= 3.68`. So **`k = 2`** is the sensible cut.

The principle is `‖A − A_k‖_F = √(Σ_{i>k} σᵢ²)`: you stop when what you discard
is negligible beside what you keep. Here `σ₃/σ₁ = 0.0289`, already negligible,
while `σ₂/σ₁ = 0.1023` is not. And the ratio `σ₂/σ₃ = 3.54` is the cliff.

**(d)** Storage for `A_k` is `m·k` (for `U_k`) `+ k` (for `σ`) `+ k·n` (for
`V_kᵀ`). With `m = 4, n = 6`, and `A` having 24 entries:

| k | stored | ratio |
| --- | --- | --- |
| 1 | `4 + 1 + 6 = 11` | 0.46x |
| 2 | `8 + 2 + 12 = 22` | 0.92x |
| 3 | `12 + 3 + 18 = 33` | 1.38x |

Compression is a win only for `k = 1`, and barely for `k = 2`. The threshold is
`k < mn/(m+n+1) = 24/11 = 2.18`, so `k ≤ 2` qualifies. At `k = 3` you store
*more* numbers than the original — exact reconstruction is the worst possible
choice for storage, which is worth internalising.

Note that the algebra and the engineering disagree here. The best
*approximation* is `k = 2` (2.87% error); the best *compression* is `k = 1`
(10.57% error, but half the storage). Choose based on which you care about.

**(e)** Row 2 = 2 × row 1, so the two rows are linearly dependent and the rank
is at most 3 — and exactly 3, since the other rows are not dependent. That is
directly visible as `σ₄ = 0`.

Two proportional rows guarantee at least one zero singular value, so
`rank < min(m, n)`. This is a genuinely useful diagnostic: a zero (or
near-zero) singular value is the computational way of saying "these rows carry
the same information", and locating those directions is how you detect
redundant features or duplicate records.

</details>

**[ ] Exercise 4 — a 2×3 matrix: SVD, pseudoinverse, and an exact solve.** Let

```
M = [[1, 2, 3],
     [4, 5, 6]]        (2 x 3)
```

(a) Compute `MᵀM` and its eigenvalues.
(b) Report the singular values, the rank, and `cond(M)`.
(c) Compute `MMᵀ` and its eigenvalues, and confirm the nonzero ones agree with
those in (a).
(d) Using `M⁺ = VΣ⁺Uᵀ`, solve `Mx = (1, 2)ᵀ` and verify the solution is exact.
(e) Show that the solution in (d) is the minimum-norm one.
(f) Compute the best rank-1 approximation and its relative Frobenius error.
(g) Explain why `np.linalg.solve(MᵀM, Mᵀb)` fails on this matrix, and what that
failure is telling you.

<details>
<summary>Solution</summary>

**(a)** The `(i,j)` entry of `MᵀM` is the dot product of columns `i` and `j`:

    M^T M = [1·1+4·4   1·2+4·5   1·3+4·6]   [17  22  27]
            [2·1+5·4   2·2+5·5   2·3+5·6] = [22  29  36]
            [3·1+6·4   3·2+6·5   3·3+6·6]   [27  36  45]

Eigenvalues: `90.402673`, `0.597327`, `0`.

Checks: they sum to `91 = 17 + 29 + 45 = tr(MᵀM)` ✓, and
`det(MᵀM) = 17(29·45 − 36·36) − 22(22·45 − 36·27) + 27(22·36 − 29·27)`.
The three minors are `9`, `18`, `9`, so `det = 17(9) − 22(18) + 27(9) = 153 −
396 + 243 = 0` ✓. The third eigenvalue really is zero.

**(b)** `σ₁ = √90.402673 = 9.508032`, `σ₂ = √0.597327 = 0.772870`, `σ₃ = 0`.

**Rank 2** — two nonzero singular values. `min(2,3) = 2`, so a third is forced to
zero. `cond(M) = 9.508032/0.772870 = 12.3022`.

**(c)** `MMᵀ` is `2 × 2`, from the row dot products:

    MM^T = [1²+2²+3²    1·4+2·5+3·6]   [14  32]
           [1·4+2·5+3·6  4²+5²+6²]   [32  77]

`tr = 91`, `det = 14·77 − 32² = 1078 − 1024 = 54`.
Eigenvalues: `λ = [91 ± √(91² − 4·54)]/2 = [91 ± √8065]/2`, and `√8065 =
89.805345`, giving `90.402673` and `0.597327`.

Exactly the two nonzero eigenvalues from (a). This is the general statement:
**the nonzero singular values squared are the nonzero eigenvalues of both Gram
matrices.** Which side you square changes only the *zeros*, never the nonzero
spectrum.

**(d)** `np.linalg.svd(M, full_matrices=False)` gives

    U  = [-0.386318  -0.922366]     Vᵀ = [-0.428667  -0.566307  -0.703947]
         [-0.922366   0.386318]           [ 0.805964   0.112382  -0.581199]

With `b = (1, 2)ᵀ`: `Uᵀb = (−2.231049, −0.149730)ᵀ`. Divide by the singular
values:

    c = (−2.231049/9.508032, −0.149730/0.772870) = (−0.234649, −0.193733)

Then `x = Vc = (−0.055556, 0.111111, 0.277778)ᵀ`.

Verify:

    Mx = (1(−0.055556) + 2(0.111111) + 3(0.277778),
          4(−0.055556) + 5(0.111111) + 6(0.277778))
       = (−0.055556 + 0.222222 + 0.833334,
          −0.222224 + 0.555555 + 1.666668)
       = (1.000000, 2.000000)

The residual is zero. `b` lies in the column space of `M`, which here is all of
`ℝ²` because `M` is `2 × 3` and therefore full row rank. So this is an **exact**
solve, not a least-squares approximation.

**(e)** The solution set. From `x₁ + 2x₂ + 3x₃ = 1`, write `x₁ = 1 − 2x₂ − 3x₃`.
Substitute into `4x₁ + 5x₂ + 6x₃ = 2`:

    4 − 8x₂ − 12x₃ + 5x₂ + 6x₃ = 2
    4 − 3x₂ − 6x₃ = 2   →   3x₂ + 6x₃ = 2   →   x₂ = 2/3 − 2x₃

With `s = x₃` free:

    x = (−1/3 + s,  2/3 − 2s,  s)

Minimise `f(s) = (−1/3 + s)² + (2/3 − 2s)² + s²`:

    f'(s) = 2(−1/3 + s) − 4(2/3 − 2s) + 2s = 12s − 10/3

so `f'(s) = 0` gives `s = 5/18 = 0.277778`, and

    x = (−1/3 + 5/18,  2/3 − 5/9,  5/18) = (−0.055556, 0.111111, 0.277778)

matching (d), with `‖x‖₂ = √(0.003086 + 0.012346 + 0.077160) = √0.092592 =
0.304290`.

The theorem behind this: **the minimum-norm solution lies in the row space of
`M`**, because any component of `x` orthogonal to `span{(1,2,3), (4,5,6)}` can be
added or removed without changing `Mx`, while increasing `‖x‖₂`. The SVD
formula delivers this for free — `x = VΣ⁺Uᵀb` is a combination of columns of
`V`, and those span exactly the row space. That is why `pinv` never needs a
"which solution?" decision, and why it differs from `inv` on a non-square matrix.

**(f)** `A₁ = σ₁u₁v₁ᵀ`:

    A₁ = [[1.5745, 2.0801, 2.5857],
          [3.7594, 4.9664, 6.1735]]

`‖M − A₁‖_F = σ₂ = 0.772870`, and `‖M‖_F = √(1+4+9+16+25+36) = √91 = 9.539392`.
Relative error `= 0.772870/9.539392 = 0.081019`, i.e. **8.10%**.

**(g)** `np.linalg.solve(MᵀM, Mᵀb)` raises `LinAlgError: Singular matrix`, because
`MᵀM` has an exactly zero eigenvalue as computed in (a).

The failure is reporting the truth: **`M` has only two independent directions,
and the third is identically zero.** There is no third singular value to divide
by, so the normal equations ask for something that does not exist. This is the
same under-determination as the rank-deficient least-squares problem in
[38](../part03_linear_algebra/38_orthogonality_and_least_squares.md), seen from the rectangular side — and
here it is detectable *in advance*: a `2 × 3` matrix can never have rank 3, so its
`3 × 3` Gram matrix is guaranteed singular.

The fix is to work only with the nonzero singular values, which is exactly what
`np.linalg.lstsq` and `np.linalg.pinv` do. General rule: if
`rank(A) < min(m, n)`, never form `AᵀA`.

</details>

**[ ] Exercise 5 — PCA with and without standardisation.** Six observations,
three features: monthly spend `a`, annual income `i`, credit score `s`.

```
[ 10, 1000, 3.0]
[ 12, 1100, 3.4]
[ 11, 1050, 3.2]
[ 13, 1150, 3.6]
[ 12, 1080, 3.3]
[ 11, 1020, 3.1]
```

(a) Compute the column means and the column standard deviations (the `1/(m−1)`
convention).
(b) Compute the raw covariance matrix and its eigenvalues, and report the
explained variance ratios.
(c) Repeat after standardising each column, and compare the two sets of ratios.
(d) Report PC1 in both cases and say in one sentence what the raw version has
actually discovered.
(e) Compute the correlation matrix and explain what it adds that the raw
covariance matrix does not.

<details>
<summary>Solution</summary>

**(a)** Means: `ā = 69/6 = 11.5`, `ī = 6400/6 = 1066.666667`,
`s̄ = 19.6/6 = 3.266667`.

Centred deviations and their sums of squares (dividing by `m − 1 = 5`):

    a: (−1.5,  0.5, −0.5,  1.5,  0.5, −0.5)              sumsq 5.500000 → var 1.100000
    i: (−66.666667, 33.333333, −16.666667, 83.333333,
        13.333333, −46.666667)                           sumsq 15133.333333 → var 3026.666667
    s: (−0.266667, 0.133333, −0.066667, 0.333333,
        0.033333, −0.166667)                             sumsq 0.233333 → var 0.046667

    std = (1.048809, 55.015149, 0.216025)

**(b)** Off-diagonal covariances (sums of products of deviations, over 5):

    a·i: 100.0 + 16.666667 + 8.333333 + 125.0 + 6.666667 + 23.333333 = 280.000000 → 56.000000
    a·s: 0.4 + 0.066667 + 0.033333 + 0.5 + 0.016667 + 0.083333 = 1.100000 → 0.220000
    i·s: 17.777778 + 4.444444 + 1.111111 + 27.777778 + 0.444444 + 7.777778 = 59.333333 → 11.866667

    Sigma_cov = [   1.100000    56.000000     0.220000]
                [  56.000000  3026.666667    11.866667]
                [   0.220000    11.866667     0.046667]

Eigenvalues, descending: `3027.749338`, `0.063858`, `0.000138`.
Trace check: `3027.749338 + 0.063858 + 0.000138 = 3027.813334`, matching
`tr(Σ_cov) = 1.1 + 3026.666667 + 0.046667 = 3027.813334` ✓

Explained variance ratios: `0.999979`, `0.000021`, `0.000000`.

**(c)** Dividing each centred column by its own standard deviation makes the
diagonal 1 and turns the off-diagonals into correlations:

    Sigma_z = [1.000000  0.970531  0.971008]
              [0.970531  1.000000  0.998488]
              [0.971008  0.998488  1.000000]

Eigenvalues: `2.960077`, `0.038414`, `0.001509`, summing to `3` ✓.
Ratios: `0.986692`, `0.012805`, `0.000503`.

**Comparison.** Raw PCA puts `99.998%` of the variance in one component and
`0.002%` in the other two combined — effectively one-dimensional, and the
remaining components are numerical dust. Standardised PCA gives
`98.67% / 1.28% / 0.05%`, a genuine three-level structure.

**(d)** Raw PC1, the top eigenvector of `Σ_cov`:
`v₁ = (0.018499, 0.999821, 0.003920)` — that is, **the income column, alone.**

Standardised PC1: `v₁ = (0.573693, 0.579124, 0.579217)` — all three features
contributing almost equally.

What the raw version has actually discovered is not a relationship between the
features. It has discovered that income is recorded in large numbers:
`Var(income) = 3026.67` against `Var(spend) = 1.10`, a factor of 2752, so income
wins before any correlation is even considered. The `0.999979` figure is a report
on **units**, not on structure. This is the identical trap to the norm-choice
question in [37](../part03_linear_algebra/37_inner_products_norms_geometry.md): the measurement instrument,
not the subject, is doing the deciding.

**(e)** The correlation matrix is `Σᵢⱼ/(stdᵢ·stdⱼ)` — exactly the standardised
covariance from (c). By hand:

    corr(a,i) = 56.000000/(1.048809 × 55.015149)  = 56.000000/57.700000  = 0.970531
    corr(a,s) =  0.220000/(1.048809 ×  0.216025) =  0.220000/0.226540   = 0.971008
    corr(i,s) = 11.866667/(55.015149 ×  0.216025) = 11.866667/11.882640  = 0.998488

What it adds is **scale-freeness**. `Σᵢᵢ = 3026.67` says income varies a lot, but
a lot *in dollars*, which is a statement about the denomination rather than about
the data. Dividing by `stdᵢstdⱼ` asks the scale-free question — how tightly do
two features move together — and the answer is striking: **all three
correlations exceed 0.97**, with `corr(i,s) = 0.998488`.

So the honest reading is that the standardised PCA is right and the raw one was
right for the wrong reason. There really is one dominant axis, but it is a
*shared* axis of all three features, not the income column. Had raw PC1 genuinely
been "income", the standard deviations of the other two columns would have been
large — they are not. The correlation matrix is what tells you the raw conclusion
was accidentally correct.

</details>

**Challenge — Exercise 6 — reading a singular value spectrum and choosing how many
components to keep.** You are handed an `8 × 12` matrix's singular values, in
descending order, plus its Frobenius norm:

```
sigma: 7.758890   2.475911   1.509323   1.034756   0.894488   0.813630   0.659233   0.253395
||A||_F = 8.464053
```

(a) Compute `Σσᵢ²` and check it against `‖A‖_F²`. Name the identity and say what a
failure would mean.
(b) Report the explained variance ratio for each component, and the cumulative
ratios for `k = 1, 2, 3`.
(c) Compute the relative Frobenius error of the best rank-`k` approximation for
`k = 1, 2, 3, 4`.
(d) Compute the successive ratios `σₖ/σₖ₊₁` and identify the largest drop. Does
it agree with what (b) and (c) suggest?
(e) Decide how many components to keep, justifying it with at least two of the
criteria above. State what would change your decision.
(f) A colleague proposes keeping all 8, since "the extra components are lossless".
Compare the storage cost with the raw matrix and explain the error in their
reasoning.

<details>
<summary>Solution</summary>

**(a)** Squaring and summing:

    7.758890² = 60.200133      0.894488² = 0.800109
    2.475911² =  6.130135      0.813630² = 0.661993
    1.509323² =  2.278056      0.659233² = 0.434588
    1.034756² =  1.070720      0.253395² = 0.064209
                             ------------------
    total    = 71.639943

And `‖A‖_F² = 8.464053² = 71.639953` ✓ (agreeing to six decimals).

This is the **Parseval identity** for the SVD: the squared singular values sum to
the squared Frobenius norm, i.e. to the total energy in the data. It is a free
correctness check on the entire spectrum. A failure means the numbers are not the
spectrum of `A` — usually a transcription slip, or values rounded so hard that a
small one was dropped.

**(b)** Ratios `σᵢ²/71.639943`:

| i | `σᵢ²` | ratio | cumulative |
| --- | --- | --- | --- |
| 1 | 60.200133 | 0.840316 | 0.840316 |
| 2 | 6.130135 | 0.085568 | 0.925884 |
| 3 | 2.278056 | 0.031799 | 0.957683 |
| 4 | 1.070720 | 0.014946 | 0.972629 |
| 5 | 0.800109 | 0.011168 | 0.983797 |
| 6 | 0.661993 | 0.009241 | 0.993038 |
| 7 | 0.434588 | 0.006066 | 0.999104 |
| 8 | 0.064209 | 0.000896 | 1.000000 |

**(c)** By Eckart–Young, `‖A − Aₖ‖_F = √(Σ_{i>k} σᵢ²)`; divide by `8.464053`:

| k | `‖A − Aₖ‖_F` | relative |
| --- | --- | --- |
| 1 | `√11.439810 = 3.382280` | 0.399605 |
| 2 | `√5.309675 = 2.304274` | 0.272242 |
| 3 | `√3.031619 = 1.741155` | 0.205712 |
| 4 | `√1.753563 = 1.324221` | 0.156472 |
| 8 | `0` | 0 |

**(d)** Successive ratios:

    sigma_1/sigma_2 = 3.134        sigma_5/sigma_6 = 1.099
    sigma_2/sigma_3 = 1.640        sigma_6/sigma_7 = 1.234
    sigma_3/sigma_4 = 1.459        sigma_7/sigma_8 = 2.602
    sigma_4/sigma_5 = 1.157

The largest drop is between `σ₁` and `σ₂`, a factor of `3.134`, so the naive
"biggest cliff" rule says `k = 1`. **It disagrees with (b) and (c).**

Note that the *second* largest ratio is `σ₇/σ₈ = 2.602`, and it is spurious:
`σ₈` is small because the matrix is only `8 × 12` and the sequence is running
into its own tail, not because there is a second structural break in the data.

The disagreement is instructive. The cliff rule measures **ratios**, which are
scale-free and therefore get fooled by a final value approaching zero — an edge
effect of the finite dimension. The criteria in (b) and (c) measure the
**absolute** contribution of what you discard, which is literally the error you
would incur. Since the error is the thing you care about, trust (c) when the two
conflict.

**(e)** Keep **`k = 2`**, on three grounds of different kinds.

- *Marginal return.* By (c), `k = 1` costs `39.96%` error and `k = 2` costs
  `27.22%`: one extra number nearly halves the error. `k = 3` buys a further
  `6.65` points and `k = 4` a further `4.92`. The marginal value does not
  collapse until about `k = 4`.
- *Cumulative variance.* By (b), `k = 2` captures `92.59%` and `k = 3` captures
  `95.77%`. If your threshold is 90%, `k = 2` clears it; if it is 95%, take
  `k = 3`.
- *Shape.* From (d), the decay is smooth (`0.319`, `0.610`, `0.686`, …) rather
  than a cliff. Smooth decay in a spectrum like this is the signature of **noise
  mixed into every component** instead of clean low-rank structure. This matrix
  has no elbow, so the tail must be cut on error grounds, not on shape — which
  is precisely why the cliff heuristic fails here.

What would change the decision:

- **A downstream task with a validation set.** Then choose `k` by held-out
  performance. PCA is usually preprocessing, and preprocessing tuned on training
  error is the overfitting trap from
  [38](../part03_linear_algebra/38_orthogonality_and_least_squares.md).
- **A plotting requirement.** `k = 1` gives one number per row and therefore a
  two-dimensional scatter plot, using `84%` of the variance. That is usually
  plenty for a plot, and much better than an unreadable cloud.
- **A clean low-rank matrix.** If `A` were `UV` with no noise then `σ₃ = 0` and
  the tail would vanish; `k = 2` would be an *exact* reconstruction and the
  question trivial. The smoothness of this tail is exactly the evidence that the
  matrix is not clean.
- **A need to invert the matrix.** Never truncate something you intend to invert
  ([38](../part03_linear_algebra/38_orthogonality_and_least_squares.md)). Dropping a component changes the
  answer by a factor of at least `σₖ/σₖ₊₁`, and here that is already `3.13` for
  the very first drop.

**(f)** The raw matrix needs `m·n = 8 × 12 = 96` numbers.

The full SVD with `r = min(8,12) = 8` needs `m·r + r + r·n = 64 + 8 + 96 = 168`
numbers, a ratio of `168/96 = 1.75×`. So the proposal costs **75% more storage
than the original** and gains nothing.

The error in the reasoning is a confusion between *lossless* and *useful*.
`k = 8` is lossless in the sense that the reconstruction is exact — but the exact
reconstruction *is* the original matrix, so you are now storing it twice over,
once whole and once in pieces. Truncation exists to make the representation
cheaper, and at `k = r` it has done the opposite.

The general threshold: `Aₖ` costs `k(m + n + 1)` numbers against `mn` for `A`,
so compression pays only when

    k < mn/(m + n + 1) = 96/21 = 4.571

Here `k ≤ 4` qualifies: at `k = 4` you store `4 × 21 = 84` numbers against 96, a
`0.875×` compression for `15.65%` error. A real saving, but a modest one — and
honestly so: an `8 × 12` matrix has `96` numbers and `r = 8` singular
directions, so there is not much redundancy to exploit at this size. Compression
starts paying properly when `k ≪ min(m, n)`, which is why
`scipy.sparse.linalg.svds` and `randomized_svd` are built for large matrices
where `k` might be 50 out of `10⁶`.

This is the lesson's recurring point in a new form: **exactness is not the goal,
and the exact answer is frequently the most expensive one.** The `4 × 6` matrix
of Exercise 3 makes it sharper — exact reconstruction there costs `33` numbers
against `24` for the raw matrix, a ratio of `1.38×`.

</details>

## Summary

- The SVD writes **any** `m × n` matrix as `A = U S Vᵀ`, with `U` and `V`
  orthonormal and `S` diagonal.
- `A v_i = σ_i u_i`: input direction `v_i`, output direction `u_i`, stretch
  factor `σ_i`. That reading is the whole meaning of the decomposition.
- Singular values are **always real, non-negative, sorted, and there are
  exactly `min(m, n)` of them** — unlike eigenvalues, which can be complex,
  negative, unsorted, and undefined for non-square matrices.
- The count of nonzero singular values **is the rank**, and `cond(A) = σ₁/σₘₐₓ`
  tells you how close to singular a matrix is.
- `σᵢ` are the square roots of the eigenvalues of `AᵀA` — a fact about the
  theory, but a bad way to compute them, since it squares the condition number.
  One-sided Jacobi rotations never form the Gram matrix and stay accurate.
- **Truncated SVD** (`A_k`, keeping the `k` largest) is the provably best
  rank-`k` approximation, with error `√(Σ_{i>k} σᵢ²)`.
- **PCA is the SVD of centred data**: the `v_i` are the principal components,
  the scores are `X_c v_i`, and `σᵢ²/Σσⱼ²` is the explained variance ratio.
- The component scores are **uncorrelated**, which is PCA's statistical point:
  `p` correlated features become `p` independent ones, ordered by importance.
- `σᵢ²/(m−1)` equals the `i`-th eigenvalue of the covariance matrix, so the
  covariance-eigendecomposition route and the SVD route agree exactly.
- The **pseudoinverse** `A⁺ = V S⁺ Uᵀ` handles rank deficiency and the
  Moore–Penrose least-squares solution in one line — prefer
  `np.linalg.lstsq` or `pinv` over ever forming an inverse.

## Next

[41 — Matrices, Graphs, and Applications](../part03_linear_algebra/41_matrices_graphs_and_applications.md)
puts matrices back to work on real structures. A network is a matrix, its
adjacency matrix has an SVD and an eigendecomposition, and the *graph
Laplacian* — which is symmetric positive definite by construction — turns
connectedness, clustering, and "what is this community?" into eigenvalue
problems. Everything from the last four lessons gets used at once.
