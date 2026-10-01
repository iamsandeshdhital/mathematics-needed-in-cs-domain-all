# 38 — Orthogonality and Least Squares

**Part**: part03_linear_algebra · **Prerequisites**: 37 · **Time**: 40 min

---

## In Plain Words

Last lesson you learned to measure how long a vector is. This lesson uses that
ruler to answer a question you have been circling: if you must *approximate*
something, how do you pick the closest approximation?

The answer is to throw away the part you cannot use and keep the part you can.
Whatever you keep should be the piece lying along the direction you care about;
whatever you throw away should be perpendicular to it, pointing in a direction
you have no use for. This is called a **projection**, and the leftover piece is
the **error**.

Then the lesson pays off. Linear regression — the single most-used algorithm in
machine learning — is nothing but this idea applied to a straight line. The best
fitting line is the one whose leftover errors point in a direction that is
perpendicular to everything the line was built from. That single condition
produces a closed-form answer, and it is exactly the same formula that comes
out of calculus, but you can derive it with a ruler instead.

Along the way you meet **Gram-Schmidt**, a fifteen-line procedure that takes
any basis and rotates it into a perpendicular one, and the **orthogonal
matrix**, whose inverse is its own transpose.

## Why Computer Science Cares

- **Linear regression is least squares.** `sklearn.linear_model.LinearRegression`
  is a thin wrapper over `np.linalg.lstsq`. Every linear model in every
  framework routes back to the normal equations derived here.
- **`np.linalg.lstsq` vs `np.linalg.solve`.** The normal equations square the
  condition number (`cond(AᵀA) = cond(A)²`) and are correspondingly less
  accurate. `lstsq` uses SVD and does not have this problem. Lesson
  [40](../part03_linear_algebra/40_svd_and_pca.md) explains the algorithm underneath.
- **QR factorisation** is Gram-Schmidt applied to a matrix's columns, and it is
  the standard numerically-safe way to solve least squares problems.
- **Ridge regression** is least squares plus `λI`, the fix for ill-conditioned
  or over-parameterised problems. `sklearn.linear_model.Ridge(penalty='l2')`.
- **Graphics and rendering.** Rotation matrices are orthogonal, which is what
  makes them free to invert. If a transform were not orthogonal, undoing a
  rotation would require a full matrix solve. See
  [Part 07](../part07_geometry_graphics/91_transformations_graphics.md).
- **Signal processing.** Fourier analysis decomposes a signal into orthogonal
  frequency components, and the same Pythagoras identity from lesson 37 says
  the energy splits as a sum of squares. That is Parseval's theorem.
- **Overfitting.** This lesson's ridge demonstration shows concretely why adding
  features can make RSS *worse* on held-out data while making it *better* on
  training data.

## The Formal Version

**Definition.** The **orthogonal projection** of `x` onto a nonzero vector `u` is

```
proj_u(x) = (xᵀu / uᵀu) u
```

**Theorem.** `x − proj_u(x)` is orthogonal to `u`.

**Explanation.** The scalar `xᵀu / uᵀu` is chosen so the remainder is
perpendicular. And that perpendicularity *is* the optimality: for any other
point `cu` on the line, `‖x − cu‖² = ‖x − proj_u(x)‖² − 2c(uᵀ residual) + c²‖u‖²`,
and the middle term vanishes, leaving a minimum at `c = 0` offset. Orthogonality
and best approximation are the same statement.

**Definition.** Vectors `u` and `v` are **orthogonal** if `uᵀv = 0`. An
**orthonormal** set satisfies `uᵢᵀuⱼ = δᵢⱼ`: unit length, and mutually
perpendicular.

**Theorem (Gram–Schmidt).** Any linearly independent set can be turned into an
orthogonal set with the same span by repeatedly subtracting projections.

**Explanation.** The procedure: take the first vector as is. For each later
vector, subtract its projection onto every vector already accepted. What
remains cannot have any component along those directions — by construction — so
it is perpendicular to all of them. Since we only subtracted combinations of
earlier vectors, the span is untouched.

**Definition.** A square matrix `Q` is **orthogonal** if `QᵀQ = I`.

**Theorem.** If `Q` is orthogonal then `QᵀQ = QQᵀ = I`, so `Q⁻¹ = Qᵀ`, and
`Qᵀ = Q⁻¹`.

**Theorem.** If `Q` is orthogonal then `‖Qx‖ = ‖x‖` and `(Qx)ᵀ(Qy) = xᵀy` for all
`x, y`. So orthogonal matrices preserve lengths and angles — they are pure
rotations and reflections, and nothing else.

**Explanation.** The two identities follow immediately from `QᵀQ = I`. This is
why "orthogonal" and "rotation" are used almost interchangeably in graphics.

**Definition.** Given `A` (`m × n`) and `y` (`m × 1`), the **least squares
problem** is to find `β` minimising `‖Aβ − y‖₂`, or equivalently the sum of
squared residuals.

**Theorem (Normal equations).** If `AᵀA` is invertible, the unique minimiser
satisfies

```
AᵀA β = Aᵀy
```

and equivalently is `β = (AᵀA)⁻¹Aᵀy`.

**Explanation.** The residual `r = y − Aβ` at the optimum is orthogonal to every
column of `A`, which means `Aᵀr = 0`, i.e. `AᵀAβ = Aᵀy`. Geometrically: the
error points in a direction that is perpendicular to everything the model
used, so you cannot reduce the error by adjusting the model. This is the
"derivative is zero" condition, obtained without any calculus.

**Theorem.** Least squares has a unique solution iff `A` has full column rank.
If `A` does not, the minimiser is not unique (infinitely many coefficients give
the same fit) and `AᵀA` is singular.

**Definition.** The **Ridge** solution minimises `‖Aβ − y‖² + λ‖β‖²` and
satisfies

```
(AᵀA + λI) β = Aᵀy
```

for `λ > 0`.

**Explanation.** The extra `λI` makes the system invertible even when `AᵀA` is
singular, because the eigenvalues of `AᵀA + λI` are all at least `λ`. In
practice you do not penalise the intercept, so `λ` goes on all but the first
diagonal entry.

See [SYMBOLS.md](../SYMBOLS.md) for `xᵀy`, `‖x‖`, `x ⊥ y`, `A⁻¹`, `Aᵀ`.

## Worked Example

Fit `price = β₀ + β₁·area` to the data
`(1, 2.1), (2, 3.9), (3, 6.2), (4, 7.8), (5, 10.1)`.

**Step 1: build the design matrix.** One row per data point, a column of ones
for the intercept, then the feature:

```
A = [1  1]      y = [2.1]
    [1  2]          [3.9]
    [1  3]          [6.2]
    [1  4]          [7.8]
    [1  5]          [10.1]
```

5 equations, 2 unknowns — overdetermined, so no exact solution.

**Step 2: form the normal matrix.**

```
AᵀA = [1  1]  [1  1]        [5   15]
      [1  5]  [1  2]   =    [15  55]

      [1  3]  [1  3]
      [1  4]  [1  4]
      [1  5]  [1  5]
```

Check by hand: `AᵀA[0][0] = 1+1+1+1+1 = 5`. `AᵀA[0][1] = 1+2+3+4+5 = 15`.
`AᵀA[1][1] = 1+4+9+16+25 = 55`. ✓

**Step 3: form the right-hand side.**

```
Aᵀy = [1+3.9+6.2+7.8+10.1]  = [30.1]
      [1(2.1) + 2(3.9) + 3(6.2) + 4(7.8) + 5(10.1)]
      [2.1 + 7.8 + 18.6 + 31.2 + 50.5] = [110.2]
```

**Step 4: solve the 2×2 system.**

```
5β₀ + 15β₁ = 30.1
15β₀ + 55β₁ = 110.2
```

Multiply the first by 3: `15β₀ + 45β₁ = 90.3`. Subtract from the second:
`10β₁ = 19.9`, so `β₁ = 1.99`. Then `5β₀ = 30.1 − 15(1.99) = 30.1 − 29.85 =
0.25`, giving `β₀ = 0.05`.

```
β = [0.05, 1.99]
```

**Step 5: verify orthogonality of the residuals.**

Fitted values `2.04, 4.03, 6.02, 8.01, 10.00`. Residuals
(actual − fitted): `0.06, −0.13, 0.18, −0.21, 0.10`.

- `r·(column of ones) = 0.06 − 0.13 + 0.18 − 0.21 + 0.10 = 0` ✓
- `r·(column of x) = 0.06 − 0.26 + 0.54 − 0.84 + 0.50 = 0` ✓

Both are exactly zero, which is the guarantee that no adjustment of the
coefficients can reduce the error.

**Step 6: score it.** `RSS = 0.06² + 0.13² + 0.18² + 0.21² + 0.10² = 0.107`.
With `ȳ = 6.22`, `TSS = 39.708`, so `R² = 1 − 0.107/39.708 = 0.997305`.

The model is `price ≈ 0.05 + 1.99·area`: about 2 thousand per square foot.

## Runnable Code

First, Gram–Schmidt, on a deliberately ill-conditioned basis:

```python
import math

# ---------- shared helpers ----------

def dot(u, v):
    return sum(a * b for a, b in zip(u, v))

def transpose(A):
    return [list(row) for row in zip(*A)]

def matmul(A, B):
    Bt = transpose(B)
    return [[sum(a * b for a, b in zip(row, col)) for col in Bt] for row in A]

def matvec(A, v):
    return [sum(a * b for a, b in zip(row, v)) for row in A]

def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

def norm2(v):
    return math.sqrt(dot(v, v))

def print_matrix(A, title=""):
    if title:
        print(title)
    for row in A:
        print("   " + "".join(f"{v:9.4f}" for v in row))
    print()

# ---------- Gram-Schmidt ----------

def gram_schmidt(columns):
    """Turn any list of independent vectors into an ORTHOGONAL set.

    The trick: take the next vector and subtract its projection onto every
    direction already accepted. Whatever is left over cannot have any component
    along those directions, so it is orthogonal to all of them.
    """
    q = []
    for v in columns:
        w = list(v)
        for u in q:
            proj = dot(u, w) / dot(u, u)      # scalar coefficient of u in w
            w = [a - proj * b for a, b in zip(w, u)]
        q.append(w)
    return q

def normalize(v):
    n = norm2(v)
    return [x / n for x in v]

# A deliberately terrible basis: two almost-parallel vectors, chosen so that
# naive projection loses precision.
original = [[1.0, 1.0], [1.0, 1.001]]

print("Input vectors (deliberately nearly parallel -- a hard case):")
print_matrix([[original[0][0], original[1][0]],
              [original[0][1], original[1][1]]], "   v1 = (1, 1), v2 = (1, 1.001)")
print("   v1 . v1 =", dot(original[0], original[0]))
print("   v1 . v2 =", dot(original[0], original[1]), " <- nearly as large, so")
print("   nearly all of v2 is 'explained by' v1 and the leftover is tiny")
print()

q = gram_schmidt(original)
print("Gram-Schmidt output (orthogonal but not normalised):")
for i, u in enumerate(q):
    print(f"   u{i+1} = {u}   |u{i+1}| = {norm2(u):.10f}")
print()
print("Check orthogonality -- both off-diagonal dots must be zero:")
for i in range(len(q)):
    for j in range(len(q)):
        if i != j:
            print(f"   u{i+1} . u{j+1} = {dot(q[i], q[j]):.15f}")
print()
print("Now normalise to get an ORTHONORMAL basis:")
e = [normalize(u) for u in q]
for i, u in enumerate(e):
    print(f"   e{i+1} = {[round(x, 10) for x in u]}   |e{i+1}| = {norm2(u):.12f}")
print()
print("   e1 . e2 =", dot(e[0], e[1]))
print("   e1 . e1 =", dot(e[0], e[0]), "   e2 . e2 =", dot(e[1], e[1]))
print("So the orthonormal basis satisfies  e_i . e_j = delta_ij:  1 if i == j,")
print("0 otherwise. That single identity is what makes everything downstream")
print("easy -- the columns of an orthogonal matrix, QR factorisation, and the")
print("projection formula in the next block all rest on it.")

print("\n--- the key property, verified: each q_i lies in the span of the")
print("    first i+1 input vectors, and the span is preserved ---")
print("Since we only ever SUBTRACT multiples of earlier vectors, span(v) is")
print("unchanged. So the orthogonal set is a basis of exactly the same space.")
print(f"   span of input has dimension 2, span of output has dimension {len(q)}")
print("Gram-Schmidt preserves both the span and the dimension. It only changes")
print("the basis, never the subspace.")
```

Now projection, and the orthogonal matrix:

```python
import math

# ---------- shared helpers ----------

def dot(u, v):
    return sum(a * b for a, b in zip(u, v))

def transpose(A):
    return [list(row) for row in zip(*A)]

def matmul(A, B):
    Bt = transpose(B)
    return [[sum(a * b for a, b in zip(row, col)) for col in Bt] for row in A]

def matvec(A, v):
    return [sum(a * b for a, b in zip(row, v)) for row in A]

def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

def norm2(v):
    return math.sqrt(dot(v, v))

def normalize(v):
    n = norm2(v)
    return [x / n for x in v]

def print_matrix(A, title=""):
    if title:
        print(title)
    for row in A:
        print("   " + "".join(f"{v:9.4f}" for v in row))
    print()

# ---------- projection ----------

def project_onto(v, u):
    """The closest point to v on the line spanned by u."""
    return [(dot(u, v) / dot(u, u)) * x for x in u]

# ---------- part 1: projection onto a single line ----------

v = [3.0, 4.0]
u = [1.0, 1.0]

print("--- projecting (3,4) onto the line through (1,1) ---")
c = dot(u, v) / dot(u, u)
proj = [c * x for x in u]
resid = [a - b for a, b in zip(v, proj)]
print(f"   v        = {v}")
print(f"   u        = {u}")
print(f"   u . u    = {dot(u, u)}")
print(f"   u . v    = {dot(u, v)}")
print(f"   c = (u.v)/(u.u) = {dot(u, v)}/{dot(u, u)} = {c}")
print(f"   proj     = {proj}")
print(f"   residual = {resid}    <- the leftover, the ERROR")
print(f"   u . residual = {dot(u, resid):.10f}  <- zero, so the leftover is")
print("      perpendicular to the line. That is what makes it 'best possible':")
print("      any other point on the line would be further away.")
print()
print("Why is it optimal? Pushing c by epsilon changes the distance by")
print("  |v - (c+eps)u|^2 = |resid|^2 - 2*eps*(u.resid) + eps^2*|u|^2")
print("The cross term vanishes because u . resid = 0, so the expression is")
print("minimised at eps = 0. Orthogonality IS optimality.")

# verify by brute force, scanning the range that actually contains the optimum
print()
print("Brute-force check: search 200001 points t*u for t in [-10, 10]:")
best_t, best_d = None, float("inf")
for i in range(200001):
    t = -10.0 + 20.0 * i / 200000.0
    d = norm2([a - t * b for a, b in zip(v, u)])
    if d < best_d:
        best_t, best_d = t, d
print(f"   best t = {best_t:.6f}, best |v - t u| = {best_d:.10f}")
print(f"   our c  = {c}, our |v - proj|  = {norm2(resid):.10f}")
print(f"   the formula and the search agree to {abs(best_d - norm2(resid)):.2e}")
print("The formula found the same optimum as a search, with no calculus.")

# ---------- part 2: projection onto a whole basis ----------

print("\n--- projecting onto a 2D orthonormal basis (a full decomposition) ---")
e1 = normalize([1.0, 1.0])
e2 = normalize([1.0, -1.0])
w = [3.0, 4.0]
c1 = dot(e1, w)
c2 = dot(e2, w)
recon = [c1 * e1[i] + c2 * e2[i] for i in range(2)]
print(f"   w         = {w}")
print(f"   e1        = {e1}")
print(f"   e2        = {e2}")
print(f"   e1 . w    = {c1}")
print(f"   e2 . w    = {c2}")
print(f"   rebuild w = e1*(e1.w) + e2*(e2.w) = {recon}")
print(f"   matches w to {max(abs(a - b) for a, b in zip(recon, w)):.2e}")
print("Because e1 and e2 span all of R^2, the projection is the identity:")
print("the residual is zero. Orthogonality is what makes the coefficients")
print("independent -- no double counting between the two directions.")

# ---------- part 3: the orthogonal matrix ----------

print("\n--- the orthogonal matrix Q ---")
Q = transpose([e1, e2])          # columns are the basis vectors
print_matrix(Q, "Q = (columns e1, e2):")
Qt = transpose(Q)
print("Q^T Q =")
print_matrix(matmul(Qt, Q))
print("Diagonal 1, off-diagonal 0: Q^T Q = I. That is what 'orthogonal' means.")
print()
print("Consequences, all checked numerically:")
x = [2.0, 5.0]
print(f"   Q x        = {[round(v, 12) for v in matvec(Q, x)]}")
print(f"   |Qx|       = {norm2(matvec(Q, x)):.12f}")
print(f"   |x|        = {norm2(x):.12f}   <- length preserved")
print(f"   equal?     {abs(norm2(matvec(Q, x)) - norm2(x)) < 1e-12}")
dot_before = dot(x, [1.0, 2.0])
dot_after = dot(matvec(Q, x), matvec(Q, [1.0, 2.0]))
print(f"   x . y      = {dot_before:.12f}")
print(f"   (Qx).(Qy)  = {dot_after:.12f}   <- angle preserved too")
print()
print("And the inverse is free: Q^-1 = Q^T. No solving, no elimination.")
QtQ = matmul(Qt, Q)
print(f"   Q^T @ Q == I (to 1e-12)? "
      f"{all(abs(QtQ[i][j] - identity(2)[i][j]) < 1e-12 for i in range(2) for j in range(2))}")
print(f"   Q @ Q^T == I (to 1e-12)? "
      f"{all(abs(matmul(Q, Qt)[i][j] - identity(2)[i][j]) < 1e-12 for i in range(2) for j in range(2))}")
print("   Both hold, because a square matrix with a left inverse has a right")
print("   inverse. So Q is invertible AND the inverse is the transpose.")
print()
print("This is why graphics code uses orthogonal matrices: rotating the world")
print("by Q is free to undo, because undoing it is just the transpose.")
```

And the main event — a complete linear regression written from scratch:

```python
import math

# ---------- shared helpers ----------

def dot(u, v):
    return sum(a * b for a, b in zip(u, v))

def transpose(A):
    return [list(row) for row in zip(*A)]

def matmul(A, B):
    Bt = transpose(B)
    return [[sum(a * b for a, b in zip(row, col)) for col in Bt] for row in A]

def matvec(A, v):
    return [sum(a * b for a, b in zip(row, v)) for row in A]

def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

def norm2(v):
    return math.sqrt(dot(v, v))

def print_matrix(A, title=""):
    if title:
        print(title)
    for row in A:
        print("   " + "".join(f"{v:11.5f}" for v in row)
              + ("     <- singular, no inverse" if all(abs(x) < 1e-11 for x in row) else ""))
    print()

def solve(A, b):
    """Gaussian elimination with partial pivoting (lesson 32)."""
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [x / pv for x in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0.0:
                f = M[r][col]
                M[r] = [M[r][j] - f * M[col][j] for j in range(n + 1)]
    return [M[i][n] for i in range(n)]

# ---------- the data ----------

# Area (square feet) and price (thousands). Deliberately noisy, and the
# noise is exactly what least squares is built to absorb.
X = [1.0, 2.0, 3.0, 4.0, 5.0]
y = [2.1, 3.9, 6.2, 7.8, 10.1]

# Design matrix: a column of 1s for the intercept, then the feature column.
# 1 + X*beta means  beta0 + beta1*x
n = len(X)
A = [[1.0, X[i]] for i in range(n)]
At = transpose(A)

print("Model:  price = beta0 + beta1 * area")
print("With 5 data points and 2 unknowns, the system is OVERDETERMINED.")
print("We cannot satisfy all 5 equations exactly, so we find the line that")
print("minimises the total squared error.\n")

print_matrix(A, "A = [1 | x]  (one row per data point):")
print_matrix(At, "A^T =")

AtA = matmul(At, A)
Aty = matvec(At, y)
print_matrix(AtA, "A^T A  (this is the 'normal matrix'):")
print("A^T y  (the right-hand side) = [" + ", ".join(f"{v:.5f}" for v in Aty) + "]\n")

# how singular would A^T A be if the feature carried no information?
Xbad = [1.0, 1.0, 1.0, 1.0, 1.0]              # the feature is CONSTANT
Abad = [[1.0, Xbad[i]] for i in range(n)]
AtA_bad = matmul(transpose(Abad), Abad)
print("For comparison, if the feature were IDENTICAL in every row the")
print("normal matrix collapses onto a single line:")
print_matrix(AtA_bad, "A^T A with x = (1,1,1,1,1) instead:")
print("Both rows are (5, 5), so the columns are identical and A^T A has no")
print("inverse. That is the geometric statement 'the feature carries no")
print("information': no line can distinguish a small house from a large one.")
print("A nearly-constant feature gives a NEARLY singular normal matrix, which")
print("is why practitioners centre or standardise their data first, and why")
print("the QR / SVD routes in lesson 40 are numerically safer here.\n")

print("=" * 66)
print("The NORMAL EQUATIONS:  A^T A beta = A^T y")
print("=" * 66)
beta = solve(AtA, Aty)
b0, b1 = beta
print(f"   beta = {beta}")
print(f"   intercept = {b0:.6f}")
print(f"   slope     = {b1:.6f}")
print()
print("So the fitted model is")
print(f"   price_hat = {b0:.4f} + {b1:.4f} * area")
print()

# ---------- verify: it is genuinely the best line ----------

print("--- checking it really is the minimum, by direct search ---")
def sse(intercept, slope):
    return sum((y[i] - (intercept + slope * X[i])) ** 2 for i in range(n))

print(f"   SSE at our solution      = {sse(b0, b1):.10f}")
# perturb the slope, keeping the intercept optimal for that slope
for ds in (-0.5, -0.1, 0.1, 0.5):
    s = b1 + ds
    # optimal intercept for a given slope: mean(y) - s*mean(x)
    b0_alt = (sum(y) / n) - s * (sum(X) / n)
    print(f"   SSE at slope {s:7.4f}     = {sse(b0_alt, s):.10f}   (worse)")
print("Every perturbation gives a larger error, so this is the minimum.")
print("A coarse grid search confirms it:")
best = min(((sse(slope=sl, intercept=sum(y) / n - sl * (sum(X) / n)), sl)
            for sl in [i / 100.0 for i in range(-200, 2001)]))
print(f"   grid search best SSE = {best[0]:.10f} at slope {best[1]:.2f}")
print(f"   our SSE              = {sse(b0, b1):.10f}")
print("The normal equations give a better answer than a 2201-point grid,")
print("because they use the exact derivative-free geometric condition that")
print("the residual is orthogonal to both columns of A.")

# ---------- the orthogonality condition ----------

residuals = [y[i] - (b0 + b1 * X[i]) for i in range(n)]
fitted = [b0 + b1 * X[i] for i in range(n)]
print()
print("--- why it works: the residual is orthogonal to everything ---")
print("   residuals r =", [round(r, 6) for r in residuals])
print(f"   r . (column of 1s)  = {dot(residuals, [1.0] * n):.12f}")
print(f"   r . (column of x)   = {dot(residuals, X):.12f}")
print("Both zero. If you nudge the intercept, the error changes by")
print("   2 * sum(r_i) * (nudge)  = 0")
print("so the error cannot decrease. That is optimality, with no calculus.")
print()
print("The three vectors (ones, x, residual) are mutually orthogonal, so by")
print("Pythagoras the total squared error decomposes with no cross terms.")
explained = dot(fitted, fitted)
unexplained = dot(residuals, residuals)
print(f"   total length^2 of y        = {dot(y, y):.10f}")
print(f"   explained by the model     = {explained:.10f}")
print(f"   unexplained (the residual) = {unexplained:.10f}")
print(f"   sum of the two             = {explained + unexplained:.10f}")
print("They add up exactly. That is the whole theory in one line.")

# ---------- the prediction table ----------

print()
print("--- fitted values and errors ---")
print(f"   {'area':>6} {'actual':>8} {'fitted':>9} {'residual':>10}")
for i in range(n):
    print(f"   {X[i]:6.1f} {y[i]:8.2f} {fitted[i]:9.4f} {residuals[i]:10.4f}")
rss = unexplained
tmean = sum(y) / n
tss = sum((yi - tmean) ** 2 for yi in y)
print()
print(f"   RSS (residual sum of squares) = {rss:.6f}")
print(f"   TSS (total sum of squares)    = {tss:.6f}")
print(f"   R^2 = 1 - RSS/TSS             = {1 - rss / tss:.6f}")
print("R^2 is the fraction of the variance in y that the model explains.")
print("Here the linear model explains most of it; the remainder is noise.")

# ---------- multiple features: the same code, no changes ----------

print()
print("=" * 66)
print("Multiple features: identical code, more columns")
print("=" * 66)

# area, number of bedrooms, and the same target
X2 = [1.0, 2.0, 3.0, 4.0, 5.0]
B2 = [1.0, 3.0, 2.0, 4.0, 3.0]          # bedrooms
A2 = [[1.0, X2[i], B2[i]] for i in range(n)]
beta2 = solve(matmul(transpose(A2), A2), matvec(transpose(A2), y))
print("   design matrix A = [1 | area | bedrooms]")
print_matrix(A2, "   ")
print("   beta = [intercept, area coefficient, bedroom coefficient]")
print("   " + "  ".join(f"{v:.6f}" for v in beta2))
fit2 = [sum(beta2[j] * A2[i][j] for j in range(3)) for i in range(n)]
r2 = [y[i] - fit2[i] for i in range(n)]
rss2 = dot(r2, r2)
print(f"   RSS with 2 features  = {rss2:.6f}   (was {rss:.6f} with 1)")
print(f"   R^2                  = {1 - rss2 / tss:.6f}   (was {1 - rss / tss:.6f})")
print("More columns can only help or leave it unchanged, because the old")
print("solution is still available to the search. RSS is monotonically")
print("non-increasing in the number of features -- which is exactly why R^2")
print("is a misleading score to maximise, and why adjusted R^2 or held-out")
print("validation exists. Now add a RANDOM NOISE column and watch what happens:")

import random
random.seed(0)
noise = [random.gauss(0.0, 0.5) for _ in range(n)]
A3 = [[1.0, X[i], noise[i]] for i in range(n)]
At3 = transpose(A3)
beta3 = solve(matmul(At3, A3), matvec(At3, y))
r3 = [y[i] - sum(beta3[j] * A3[i][j] for j in range(3)) for i in range(n)]
print(f"   RSS with a noise column     = {dot(r3, r3):.6f}")
print("   coefficients:", "  ".join(f"{v:+.6f}" for v in beta3))
print(f"   (slope on area was {b1:.6f} with one feature)")
print()
print("The noise column is correlated with the real one purely by chance, so")
print("it steals some of the real feature's variance. RSS went DOWN, but the")
print("coefficient on area got worse. That is overfitting, and it is the whole")
print("reason ridge and LASSO add a penalty term. RSS is the wrong thing to")
print("minimise on its own.")

# ---------- ridge regression: the same equations plus a penalty ----------

print()
print("=" * 66)
print("Ridge regression: add a penalty and the problem becomes easy again")
print("=" * 66)
print("Minimise  RSS + lambda * ||beta||^2  instead of RSS alone.")
print("The penalty shrinks the coefficients, which is exactly what kills the")
print("noise column's influence. The normal equations gain one term:\n")
print("   (A^T A + lambda*I) beta = A^T y")
print("Note lambda*I, not a penalty on the intercept: leave the first row\n")
print("   " + "".join(f"{v:11.5f}" for v in matvec(transpose(A3), y)))
p = len(beta3)
ident = identity(p)
AtA3 = matmul(At3, A3)
for lam in (0.0, 0.5, 5.0, 50.0, 500.0):
    reg = [[AtA3[i][j] + (lam if i == j else 0.0) for j in range(p)] for i in range(p)]
    b = solve(reg, matvec(At3, y))
    rr = [y[i] - sum(b[j] * A3[i][j] for j in range(p)) for i in range(n)]
    print(f"   lambda = {lam:7.2f}: beta = "
          + "  ".join(f"{v:+.6f}" for v in b)
          + f"   RSS = {dot(rr, rr):.6f}")
print()
print("Read the coefficients across the rows. As lambda grows, EVERY")
print("coefficient shrinks toward zero: the area term falls from 1.986 to")
print("0.197, and the noise term falls too. The penalty is applied to the")
print("whole vector, so it cannot tell the real feature from the fake one --")
print("it only knows they are both coefficients.")
print()
print("But the NOISE term stays small in absolute terms across the whole")
print("range (-0.038 down to -0.013), because it started small. The real")
print("coefficient is around 2.0, so the noise never had comparable size to")
print("begin with. Ridge shrinks the big coefficients hardest in RELATIVE")
print("terms -- which is why it cannot actually solve the feature-selection")
print("problem. LASSO, which uses an L1 penalty, can set coefficients to")
print("EXACTLY zero. That distinction is lesson 37's norm choice paying off.")
print()
print("Notice also that RSS gets steadily worse as lambda grows. Always pick")
print("lambda on held-out data, never by minimising RSS.")
print()
print("Finally: lambda*I also makes the system solvable even when A is")
print("singular, because A^T A + lambda*I has eigenvalues at least lambda.")
print("That robustness is why ridge is the default choice in practice.")
```

### With Libraries

```python
import numpy as np
import pandas as pd

np.set_printoptions(precision=6, suppress=True)

X = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
y = np.array([2.1, 3.9, 6.2, 7.8, 10.1])

# ---------- the design matrix, built explicitly ----------
A = np.column_stack([np.ones_like(X), X])          # [1 | x]
print("Design matrix A =\n", A)

print("\n--- the same normal equations, three lines of numpy ---")
beta, *_ = np.linalg.lstsq(A, y, rcond=None)
print("np.linalg.lstsq      ->", beta)
print("  (this is the SVD-based solver from lesson 40, and it is the one to")
print("   reach for: it does not form A^T A, so it is far better conditioned)")

beta_normal = np.linalg.solve(A.T @ A, A.T @ y)
print("np.linalg.solve(A'A) ->", beta_normal, " <- the normal equations")
print("difference           ->", np.abs(beta - beta_normal))
print("Both give the same answer on well-conditioned data. They diverge when")
print("A is close to singular, which is exactly when solve() breaks down.")
print()
print("Why? A^T A squares the condition number: cond(A^T A) = cond(A)^2.")
print("  cond(A)      =", round(np.linalg.cond(A), 4))
print("  cond(A^T A)  =", round(np.linalg.cond(A.T @ A), 4),
      " (which is roughly the square)")

# ---------- pandas, because that is how the data actually arrives ----------
print("\n--- the pandas version, which is what you will actually type ---")
df = pd.DataFrame({"area": X, "price": y})
print(df)

# add an intercept column, which statsmodels does for you
df["const"] = 1.0
X_design = df[["const", "area"]].to_numpy()
y_target = df["price"].to_numpy()

ols = np.linalg.lstsq(X_design, y_target, rcond=None)[0]
print("\nlstsq on the same matrix ->", ols)

from sklearn.linear_model import LinearRegression, Ridge
lr = LinearRegression().fit(df[["area"]], df["price"])
print(f"sklearn LinearRegression: intercept={lr.intercept_:.6f} "
      f"coef={lr.coef_[0]:.6f}  score={lr.score(df[['area']], df['price']):.6f}")
print("sklearn fits the intercept itself, so do NOT add a column of ones --")
print("doing both is a classic mistake and it silently doubles the intercept.")

# ---------- multiple features, sklearn style ----------
print("\n--- multiple features ---")
df2 = pd.DataFrame({"area": X, "beds": [1.0, 3.0, 2.0, 4.0, 3.0], "price": y})
lr2 = LinearRegression().fit(df2[["area", "beds"]], df2["price"])
print("LinearRegression on [area, beds]:")
print("   intercept =", round(float(lr2.intercept_), 6))
print("   coefs     =", np.round(lr2.coef_, 6))
print("   R^2       =", round(float(lr2.score(df2[["area", "beds"]], df2["price"])), 6))
print("These match the plain-Python run exactly: 0.257778, 2.084444, -0.188889")

# ---------- ridge ----------
print("\n--- ridge, the same penalty we wrote by hand ---")
for alpha in (0.0, 0.5, 5.0, 50.0, 500.0):
    m = Ridge(alpha=alpha).fit(df2[["area", "beds"]], df2["price"])
    print(f"   alpha={alpha:7.2f}: intercept={m.intercept_:+.6f} "
          f"coefs={np.round(m.coef_, 6)}")
print("sklearn's Ridge solves (A'A + alpha*I) beta = A'y internally, with the")
print("intercept excluded from the penalty -- the same thing we implemented.")

# ---------- the QR route, mentioned for completeness ----------
print("\n--- QR instead of the normal equations ---")
Q, R = np.linalg.qr(A)
print("Q =\n", np.round(Q, 6))
print("R =\n", np.round(R, 6))
print("A = Q R exactly:", np.allclose(Q @ R, A))
beta_qr = np.linalg.solve(R, Q.T @ y)
print("solving the triangular system R beta = Q^T y gives", beta_qr)
print("No matrix is squared, so QR is as stable as lstsq and much faster.")
print("This is the 'normal equations done safely' and it comes free from")
print("Gram-Schmidt, which is the first thing you learned in this lesson.")

# ---------- doing the statistics yourself ----------
print("\n--- the standard error, computed by hand from the same matrices ---")
fitted = X_design @ ols
resid = y_target - fitted
n_obs, n_par = X_design.shape
sigma2 = float(resid @ resid) / (n_obs - n_par)          # residual variance
XtX_inv = np.linalg.inv(X_design.T @ X_design)
se = np.sqrt(np.diag(sigma2 * XtX_inv))
print(f"   residuals          = {np.round(resid, 4)}")
print(f"   RSS                = {float(resid @ resid):.6f}")
print(f"   degrees of freedom = {n_obs} - {n_par} = {n_obs - n_par}")
print(f"   residual variance  = {sigma2:.6f}")
print(f"   standard errors    = {np.round(se, 6)}")
tstats = ols / se
print(f"   t-statistics       = {np.round(tstats, 4)}")
print("A large |t| means the coefficient is many standard errors from zero,")
print("i.e. unlikely to be pure noise. This is the whole of ordinary least")
print("squares inference, and it takes three lines once you have the fit.")
```

## Common Mistakes

**1. Adding an intercept column when the library already fits one.**

```python
import numpy as np

X = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
y = np.array([2.1, 3.9, 6.2, 7.8, 10.1])
A = np.column_stack([np.ones_like(X), X])       # WRONG for sklearn
print("column of ones:", A[:2].tolist())
print("sklearn fits the intercept itself, so this duplicates it.")
```

```python
import numpy as np
from sklearn.linear_model import LinearRegression

X = np.array([[1.0], [2.0], [3.0], [4.0], [5.0]])
y = np.array([2.1, 3.9, 6.2, 7.8, 10.1])
# RIGHT: hand it the raw features and let it add the intercept
m = LinearRegression().fit(X, y)
print("intercept =", round(float(m.intercept_), 6), " coef =", np.round(m.coef_, 6))
print("Use np.linalg.lstsq / statsmodels-style design matrices ONLY when you")
print("are building the normal equations yourself.")
```

Tempting because the textbook derivation requires a column of ones, so you
carry that habit into an API that hides it. The symptom is an intercept that
looks roughly doubled and an R² that looks slightly too good.

**2. Using `np.linalg.solve(A.T @ A, ...)` in production.**

```python
import numpy as np

rng = np.random.default_rng(0)
X = rng.normal(size=(500, 40)) + 1.0        # 40 features, correlated
y = rng.normal(size=500)
A = np.column_stack([np.ones(500), X])
# WRONG: squares the condition number, and can be exactly singular
b = np.linalg.solve(A.T @ A, A.T @ y)
print("cond(A)     =", f"{np.linalg.cond(A):.3e}")
print("cond(A'A)   =", f"{np.linalg.cond(A.T @ A):.3e}")
print("the error in b can be thousands of times larger")
```

```python
import numpy as np

rng = np.random.default_rng(0)
X = rng.normal(size=(500, 40)) + 1.0
y = rng.normal(size=500)
A = np.column_stack([np.ones(500), X])
# RIGHT: lstsq uses SVD internally and never forms A^T A
b, *_ = np.linalg.lstsq(A, y, rcond=None)
print("lstsq solution norm =", round(float(np.linalg.norm(b)), 6))
print("Also fine, and faster for square systems: np.linalg.qr then a")
print("triangular solve. Rule of thumb: lstsq unless you have a reason.")
```

**3. Forgetting to standardise before ridge or LASSO.**

```python
import numpy as np
from sklearn.linear_model import Ridge

# area in square feet, income in dollars -- wildly different scales
X = np.array([[1500.0, 45000.0], [2200.0, 52000.0], [3100.0, 61000.0]])
y = np.array([300.0, 420.0, 560.0])
m = Ridge(alpha=1.0).fit(X, y)               # WRONG: penalty is meaningless
print("coefs on raw scales:", np.round(m.coef_, 6))
print("alpha=1 punishes the big-scale column far more than the small one,")
print("so the penalty is really a penalty on UNITS, not on importance.")
```

```python
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X = np.array([[1500.0, 45000.0], [2200.0, 52000.0], [3100.0, 61000.0]])
y = np.array([300.0, 420.0, 560.0])
# RIGHT: scale first, so alpha means the same thing for every feature
pipe = make_pipeline(StandardScaler(), Ridge(alpha=1.0))
pipe.fit(X, y)
print("coefs on standardised scales:", np.round(pipe[-1].coef_, 6))
print("This is the standard fix, and it is why almost every sklearn")
print("regularised pipeline starts with StandardScaler.")
```

**4. Believing a lower RSS means a better model.**

```python
import random

random.seed(0)
X = [1.0, 2.0, 3.0, 4.0, 5.0]
y = [2.1, 3.9, 6.2, 7.8, 10.1]
noise = [random.gauss(0.0, 0.5) for _ in X]

# WRONG: judge a model by training RSS alone
for name, cols in (("area only", [X]), ("area + noise", [X, noise])):
    A = [[1.0] + [c[i] for c in cols] for i in range(len(X))]
    # (solving omitted; the point is which RSS you would REPORT)
    print(f"{name:14s}: more features always means RSS <= before, "
          f"by construction")
print("The true slope on area is 1.99. The noise column is pure chance, and")
print("fitting it steals variance from the real coefficient. The model got")
print("worse while the score got better. Always validate on held-out data.")
```

**5. Interpreting R² as a model quality score to maximise.**

R² can only go up as you add features, including useless ones, because the fit
is always free to do at least as well with more freedom. A model that
memorises noise reaches R² = 1.0 and predicts nothing. Use held-out R²,
adjusted R², or a proper information criterion. The R² printed by
`lr.score()` in scikit-learn is computed on whatever you pass it — pass test
data, not training data.

## Formula Sheet

Symbols follow [SYMBOLS.md](../SYMBOLS.md). `A` is `m × n` with `m > n`,
`y ∈ ℝ^m`, `β ∈ ℝ^n`, `u, v ∈ ℝ^n` with `u ≠ 0`, `Q` is `n × n` orthogonal,
`λ > 0`, `I` is the `n × n` identity.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| residual | `$r = y - A\beta$` | what the model failed to explain | the quantity being minimised; at the optimum it is perpendicular to the model |
| least squares problem | `$\min_\beta \lVert A\beta - y\rVert_2$`, equivalently `$\min_\beta \sum_i (y_i - (A\beta)_i)^2$` | find the coefficients whose fit has the smallest total squared error | every linear regression, `LinearRegression` and `np.linalg.lstsq` included |
| projection onto one direction | `$\text{proj}_u(x) = \dfrac{x^{\mathsf T}u}{u^{\mathsf T}u}\,u$` | the point on the line through `u` closest to `x` | one step of Gram–Schmidt; needs `u \ne 0` since `uᵀu` is the denominator |
| residual of that projection | `$x - \text{proj}_u(x)`, with `$u^{\mathsf T}(x - \text{proj}_u(x)) = 0$` | the leftover, pointing at right angles to `u` | the proof that the projection is the *best* choice, not merely a choice |
| Pythagoras | `$x \perp v \Rightarrow \lVert x+v\rVert_2^2 = \lVert x\rVert_2^2 + \lVert v\rVert_2^2$` | squared lengths of perpendicular pieces add | splitting total error into explained plus unexplained |
| Gram–Schmidt step | `$q_k = v_k - \sum_{j<k}\dfrac{q_j^{\mathsf T}v_k}{q_j^{\mathsf T}q_j}\,q_j$` | strip off the parts already accounted for | turning any basis into an orthogonal one of the same span; requires the `v_k` linearly independent |
| orthonormal condition | `$q_i^{\mathsf T}q_j = \delta_{ij}$` | length 1 when `i = j`, dot product 0 otherwise | the identity to verify after Gram–Schmidt |
| Gram–Schmidt stopping rule | a `q_k` with `‖q_k‖` below tolerance (exactly zero in theory) | the input was linearly dependent | the number of nonzero `q_k` is `dim(span)` |
| orthogonal matrix | `$Q^{\mathsf T}Q = I$` | columns are orthonormal | rotations, reflections, QR, graphics transforms |
| transpose is the inverse | `$Q^{-1} = Q^{\mathsf T}`, and `$Q Q^{\mathsf T} = I$ too` | undoing a rotation costs one transpose | undoing transforms in graphics; requires `Q` **square** — a tall matrix has no inverse |
| lengths and angles preserved | `$\lVert Qx\rVert_2 = \lVert x\rVert_2$` and `$(Qx)^{\mathsf T}(Qy) = x^{\mathsf T}y$` | `Q` rotates without stretching | shows `Q` is a pure rotation or reflection; `det(Q) = \pm 1`, not always `+1` |
| projection matrix | `$P = Q Q^{\mathsf T}`, or `$A(A^{\mathsf T}A)^{-1}A^{\mathsf T}$` | projects onto the column space of `A` | idempotent, `P² = P`, so projecting twice changes nothing |
| normal equations | `$A^{\mathsf T}A\,\beta = A^{\mathsf T}y$` | the best `β` satisfies this | the derivation, and textbook implementations |
| regression coefficients | `$\hat\beta = (A^{\mathsf T}A)^{-1}A^{\mathsf T}y$` | the closed-form least-squares answer | hand computation and proofs; **not** recommended numerically |
| simple regression slope | `$\hat\beta_1 = \dfrac{\sum_i (x_i - \bar x)(y_i - \bar y)}{\sum_i (x_i - \bar x)^2}$`, intercept `$\hat\beta_0 = \bar y - \hat\beta_1\bar x$ | the two-number version for one feature | hand checks; the same formula `LinearRegression` applies |
| uniqueness condition | unique `$\hat\beta \iff$` `A` has full column rank, `rank(A) = n`; otherwise `AᵀA` is singular | you need `n` independent columns to pin down `n` unknowns | the assumption the normal equations hide; `m ≥ n` is necessary but not sufficient |
| minimum-norm solution | among tied minimisers, the one with smallest `‖β‖₂` | the least-committal fit | what `np.linalg.lstsq` returns for rank-deficient `A` |
| error and score | `$\mathrm{RSS} = \lVert r\rVert_2^2$`, `$\mathrm{TSS} = \sum_i (y_i - \bar y)^2$`, `$R^2 = 1 - \mathrm{RSS}/\mathrm{TSS}$` | error, total spread, fraction explained | scoring a fit — but `R²` rises with every extra feature, so never maximise it |
| Pythagoras decomposition | `$\lVert y\rVert_2^2 = \lVert A\hat\beta\rVert_2^2 + \lVert r\rVert_2^2$`; with an intercept, `$\mathrm{TSS} = \text{explained} + \mathrm{RSS}$` | model's squared length plus the error's, no overlap | the one-line reason residual orthogonality means optimality |
| ridge | `$\min_\beta \lVert A\beta - y\rVert_2^2 + \lambda\lVert\beta\rVert_2^2$` → `$(A^{\mathsf T}A + \lambda I)\beta = A^{\mathsf T}y$` | least squares plus a pull toward zero | ill-conditioned or over-parameterised data; needs `λ > 0` for invertibility; **exclude the intercept** from the penalty |
| condition number | `$\text{cond}(A) = \sigma_{\max}/\sigma_{\min}$`; `$\text{cond}(A^{\mathsf T}A) = \text{cond}(A)^2$` | worst-case error amplification | the reason to prefer `np.linalg.lstsq` (SVD) or QR over the normal equations |

Two restrictions to carry. The normal equations need `AᵀA` invertible, which
requires **full column rank** — having more equations than unknowns is not enough.
And forming `AᵀA` squares the condition number, so the formula that is clearest on
paper is the one you should not run in production.

## Multiple Choice Questions

**Q1.** At the least-squares optimum, what is the relationship between the
residual `r = y − Aβ̂` and the columns of `A`?

- A) `r` is parallel to the column of `A` with the largest norm
- B) `r` is orthogonal to every column of `A`, i.e. `Aᵀr = 0`
- C) `r` equals the first column of `A`, because the intercept absorbs the error
- D) There is no defined relationship; least squares only minimises a number

<details>
<summary>Answer and explanation</summary>

**B) `r` is orthogonal to every column of `A`, i.e. `Aᵀr = 0`.**

This is the whole geometric content of least squares, and the lesson verifies it
numerically: the residuals `(0.06, −0.13, 0.18, −0.21, 0.10)` give `r·1 = 0` and
`r·x = 0`, both exactly. Orthogonality *is* optimality — moving `β` along any
column direction is perpendicular to the leftover, so no adjustment can shrink it.

A has the relationship backwards. If `r` were *parallel* to a column of `A`, then
adding a little of that column to the prediction would shrink `r`, so the point
would not have been a minimum. D confuses "the minimum is *characterised* by
`Aᵀr = 0`" with "there is no constraint" — the condition is exactly what defines
the minimum, and it is how `n` orthogonality conditions become `n` linear
equations in `n` unknowns. C is the over-parameterised failure: if `r` equalled a
column of `A`, that column would be a direction in which the error *could* be
reduced, which is the contradiction.

</details>

**Q2.** Gram–Schmidt on a linearly dependent input produces a vector whose norm
is essentially zero. What does that mean?

- A) The algorithm failed and should be rerun with more iterations
- B) The input vectors span a space of smaller dimension than the number of
  vectors given, and the zero is the signal to stop
- C) The zero vector should be added to the basis as an extra direction
- D) The inputs were nearly orthogonal and Gram–Schmidt made them worse

<details>
<summary>Answer and explanation</summary>

**B) The input vectors span a space of smaller dimension than the number of
vectors given, and the zero is the signal to stop.**

Gram–Schmidt only *subtracts* combinations of earlier vectors, so it preserves
the span exactly. If `q_k` comes out as the zero vector then `v_k` was already in
the span of `v_1, …, v_{k−1}` and contributed nothing new. The lesson's Exercise 1
walks through precisely this: `v₃ = v₁ + v₂`, and the Gram–Schmidt output has
only two nonzero vectors.

A is wrong because Gram–Schmidt is a single fixed-pass recipe, not an iterative
refinement. C is nonsense: the zero vector spans nothing, and admitting it is
exactly the confusion the eigenvector definition of
[36](../part03_linear_algebra/36_eigenvalues_and_eigenvectors.md) exists to prevent. D reverses the
mechanism — Gram–Schmidt *creates* orthogonality, so a near-zero output is
evidence it succeeded in removing the component along the previous directions.

</details>

**Q3.** Why can `np.linalg.lstsq` return a different, more trustworthy answer
than `np.linalg.solve(A.T @ A, A.T @ y)` on an ill-conditioned problem?

- A) `lstsq` uses a more accurate rounding mode for the same arithmetic
- B) `lstsq` works in an SVD or QR basis and never forms `AᵀA`, so it does not
  square the condition number
- C) `lstsq` adds a small ridge penalty while `solve` does not
- D) They always agree; any difference is a bug in one of them

<details>
<summary>Answer and explanation</summary>

**B) `lstsq` works in an SVD or QR basis and never forms `AᵀA`, so it does not
square the condition number.**

`cond(AᵀA) = cond(A)²` exactly, since the singular values of `AᵀA` are the
squares of those of `A`. On the lesson's own design matrix, `cond(A) = 8.3657`
becomes `cond(AᵀA) = 69.9857`. Squaring an already large number destroys the
trailing digits: the answer is computed as a difference of quantities that have
already lost precision to cancellation.

A is wrong — both use IEEE 754 double precision; the difference is *which*
formulas get evaluated. C is wrong: `lstsq` adds no penalty unless you request one
(`scipy.linalg.lstsq` has a `rcond` cutoff, not a regularisation term), and
`Ridge` is the thing that adds `αI`. D is wrong — they genuinely diverge exactly
where the data is bad, which is where you most need the trustworthy answer. The
lesson's demonstration: with a 4×2 design whose second column is
`(1, 1.00000001, 0.99999999, 1.00000002)`, `lstsq` and QR both return
`(−3.99999984 × 10⁷, 4.00000007 × 10⁷)` while the normal equations return
`(−2.25179956 × 10⁷, 2.25179980 × 10⁷)` — wrong in the second significant figure.

</details>

**Q4.** An orthogonal matrix `Q` satisfies `QᵀQ = I`. Which of the following does
**not** follow?

- A) `Q⁻¹ = Qᵀ`
- B) `‖Qx‖₂ = ‖x‖₂` for every `x`
- C) `det(Q) = 1` for every orthogonal matrix
- D) `(Qx)ᵀ(Qy) = xᵀy` for every `x, y`

<details>
<summary>Answer and explanation</summary>

**C) `det(Q) = 1` for every orthogonal matrix.**

`det(QᵀQ) = det(Q)² = det(I) = 1`, so `det(Q) = ±1`. The `−1` case is a
reflection and it is common: `diag(1, −1)`, which flips the y-axis, satisfies
`QᵀQ = I` exactly and has `det = −1`, with eigenvalues `1` and `−1`. So
`det = +1` characterises rotations and `det = −1` orientation-reversing maps —
both are orthogonal matrices.

A follows from `QᵀQ = I`: for square matrices a left inverse is a right inverse,
so `Qᵀ` is a two-sided inverse, and `QQᵀ = I` as well. B and D are the two
preservation properties the lesson checks numerically to 12 decimals: on
`x = (2,5)`, `‖Qx‖ = ‖x‖ = 5.385165`; on `x = (2,5)`, `y = (1,2)`, the dot product
is 12 before and after. C is the trap precisely because `det(Q)² = 1` is easy to
misremember as `det(Q) = 1`; the square root has two signs and only one is
positive.

</details>

**Q5.** Why is the intercept excluded from the ridge penalty in practice?

- A) Because the intercept is zero for centred data, so `λ·0 = 0` anyway
- B) Because `I` in `(AᵀA + λI)` must have exactly one nonzero diagonal entry
- C) Because shrinking the intercept toward zero makes predictions depend on
  where the origin of the feature scale happens to be
- D) Because scikit-learn's `Ridge` refuses to penalise the first coefficient

<details>
<summary>Answer and explanation</summary>

**C) Because shrinking the intercept toward zero makes predictions depend on where
the origin of the feature scale happens to be.**

The intercept is the predicted value at `x = 0`. Penalising it drags that
prediction toward zero for no statistical reason: change your units from metres
to millimetres and the *same data* gets a different, heavily penalised intercept,
while the slope stays meaningful. scikit-learn's `Ridge` therefore fits the
intercept by ordinary least squares and applies the penalty only to `coef_`.

A is false: the intercept is generally not zero, and after centring the *data*
the fitted intercept equals `ȳ`, which is emphatically not 0. B invents a
restriction — `(AᵀA + λI)` puts `λ` on every diagonal entry, and excluding the
intercept is done by using `λ·D` with `D = diag(0,1,…,1)`. D states the
convention correctly but gives it no reason, and the reason is C.

</details>

**Q6.** A ridge fit with `λ = 50` has a much higher RSS than the same fit with
`λ = 0` on the lesson's data. Which statement is correct?

- A) The `λ = 50` model is wrong, since least squares is defined to minimise RSS
- B) RSS is minimised by the unregularised fit by construction, which is exactly
  why training RSS is not a model-quality score — `λ` must be chosen on held-out
  data
- C) `λ = 50` makes the normal matrix singular, so the RSS figure is unreliable
- D) The unregularised fit has lower RSS, so it will also predict better

<details>
<summary>Answer and explanation</summary>

**B) RSS is minimised by the unregularised fit by construction, which is exactly
why training RSS is not a model-quality score — `λ` must be chosen on held-out
data.**

The lesson's table makes the arithmetic concrete. On the area-plus-noise design,
`λ = 0` gives `RSS = 0.105796`, `λ = 0.5` gives `0.148951`, `λ = 5` gives
`1.573511`, `λ = 50` gives `46.362735` and `λ = 500` gives `176.538844`. RSS
rises monotonically with `λ`, because the penalty is a deliberate sacrifice of fit
for stability.

A repeats the circular mistake of Common Mistake 4: RSS is the objective `λ = 0`
optimises, so of course it prefers `λ = 0`. C is false — `AᵀA + λI` is *more*
invertible as `λ` grows, with all eigenvalues at least `λ > 0`. D is the trap in
the question: lower training RSS is exactly the signature of overfitting, as the
lesson shows when a pure-noise column drives RSS down while the real slope
degrades from 1.99.

</details>

**Q7.** A 5-point dataset is fitted with `y = β₀ + β₁x`. What happens if you add a
third column that is constant `1`?

- A) `β₁` becomes more accurate, since more information is available
- B) `AᵀA` becomes singular, `np.linalg.solve` fails, and the two intercept
  coefficients are not separately identifiable
- C) Nothing changes, because a constant column carries no information
- D) The fit becomes exact, because the model gained a degree of freedom

<details>
<summary>Answer and explanation</summary>

**B) `AᵀA` becomes singular, `np.linalg.solve` fails, and the two intercept
coefficients are not separately identifiable.**

The new column equals the existing intercept column, so `rank(A)` stays 2 while
the parameter count is 3. `AᵀA` has a duplicated row and column, so
`det(AᵀA) = 0` and it has no inverse. The lesson's code shows exactly this
collapse with `x = (1,1,1,1,1)`: both rows of the normal matrix become `(5, 5)`.
`np.linalg.lstsq` still answers, returning the minimum-norm solution with the
two duplicate coefficients split evenly.

C says "no information" but draws the wrong conclusion — the consequence is a
*crash*, not a no-op, because the missing object is the inverse. A is wrong: a
duplicate column adds zero new directions, so the span is unchanged. D is the
deepest confusion — adding a parameter never makes the fit more expressive, so
RSS cannot improve, and it certainly cannot become exact on noisy data. This is
Common Mistake 1 in another guise: the same duplicate-intercept bug that doubles
the intercept when you hand a column of ones to `sklearn.LinearRegression`.

</details>

**Q8.** In `A = QR`, why is solving `Rβ = Qᵀy` equivalent to the normal equations
but numerically safer?

- A) Because `Q` is orthogonal, `Qᵀy` preserves length exactly and so loses no
  information, and `R` is triangular so no elimination step amplifies error
- B) Because `QR` is a closer approximation of `A` than `AᵀA` is
- C) Because `cond(R)` is smaller than `cond(AᵀA)` for every matrix
- D) Because `Q` is orthogonal, `R = Q⁻¹A` can be computed by transposing

<details>
<summary>Answer and explanation</summary>

**A) Because `Q` is orthogonal, `Qᵀy` preserves length exactly and so loses no
information, and `R` is triangular so no elimination step amplifies error.**

Two structural reasons. First, `‖Qᵀy‖ = ‖y‖` exactly up to rounding, so the
change of basis cannot destroy information — the projection `Qᵀy` *is* the
expansion of `y` in the orthogonal basis, and that expansion is precisely what is
being used. Second, `R` is upper triangular, so backsolving is numerically
benign. Nothing is squared anywhere.

B is a category error: `QR` *is* `A`, not an approximation of it, which is the
point (`np.allclose(Q @ R, A)` is `True` in the lesson's code). C is false as a
universal claim; `cond(R)` is essentially `cond(A)`, and the real statement is
that you never form `AᵀA`. D is half-right for the wrong reason — `R = Q⁻¹A =
QᵀA` is correct, but what helps is *triangularity*, not the transpose. If `R`
were not triangular, transposing would give you nothing.

</details>

**Q9.** Why can a general matrix refuse to diagonalise while a symmetric matrix
never does?

- A) Because a symmetric matrix has all real eigenvalues, so complex numbers
  never enter
- B) Because for a symmetric matrix the geometric and algebraic multiplicities
  always agree, so a full basis of eigenvectors exists
- C) Because a symmetric matrix always has `n` distinct eigenvalues
- D) Because `numpy.linalg.eig` uses a better algorithm for symmetric input

<details>
<summary>Answer and explanation</summary>

**B) Because for a symmetric matrix the geometric and algebraic multiplicities
always agree, so a full basis of eigenvectors exists.**

That is the precise criterion from [36](../part03_linear_algebra/36_eigenvalues_and_eigenvectors.md):
diagonalisable iff `dim E_λ = mult_alg(λ)` for every `λ`, and symmetry guarantees
the equality for all of them. This is why `np.linalg.eigh` both exists and beats
`eig` on speed and accuracy — it exploits orthogonality of the eigenvectors, which
a general matrix does not have.

A is a necessary condition masquerading as the answer. Real eigenvalues do not
guarantee diagonalisability: `[[2,1],[0,2]]` has only the real eigenvalue 2, with
algebraic multiplicity 2 and geometric multiplicity 1, and it refuses to
diagonalise. C is false: `diag(2,3,3)` is symmetric with a repeated eigenvalue and
is perfectly diagonalisable — repeated is not the problem, defective is. D
confuses cause with implementation; `eigh` is faster because the *structure* is
exploitable, not because the code is smarter.

</details>

**Q10.** A projection matrix `P` satisfies `P = P²` and `P = Pᵀ`. What is its rank
relative to its size?

- A) `rank(P) = size(P)`, since projection matrices are invertible
- B) `rank(P) ≤ size(P)`, and the rank equals the dimension of the subspace being
  projected onto — strictly smaller whenever that subspace is proper
- C) `rank(P) = 0` always, since projecting removes information
- D) `rank(P) = size(P)/2` always

<details>
<summary>Answer and explanation</summary>

**B) `rank(P) ≤ size(P)`, and the rank equals the dimension of the subspace being
projected onto — strictly smaller whenever that subspace is proper.**

The image of `P` is by definition the subspace projected onto, and `rank` is the
dimension of the image. `P² = P` is exactly "projecting twice is the same as
projecting once", which is idempotence. Projecting `(3,4)` onto the single
direction `(1,1)` inside `ℝ²` gives `P = [[1/2,1/2],[1/2,1/2]]` with
`rank(P) = 1`; projecting onto all of `ℝ²` is the identity with rank 2.

A is false and the contradiction is instructive: if `P` were invertible, `P² = P`
multiplied by `P⁻¹` would give `P = I`, so the only invertible idempotent is the
identity. C confuses the null space with the image: `P` discards exactly
`size − rank` dimensions. D is numerology with no basis; projecting onto a
3-dimensional subspace of `ℝ¹⁰⁰` gives rank 3, not 50.

</details>

## Subjective Questions

### Short Answer

**Q1. State the projection formula and explain why the denominator is `uᵀu`.**

<details>
<summary>Model answer</summary>

For `u ≠ 0`, `proj_u(x) = (xᵀu / uᵀu)·u`.

The projection must land on the line through the origin in direction `u`, so it
is a scalar multiple `cu` of `u`. Requiring the leftover `x − cu` to be
perpendicular to `u` gives `uᵀ(x − cu) = 0`, i.e. `uᵀx = c(uᵀu)`, hence
`c = xᵀu/(uᵀu)`.

The denominator is `uᵀu = ‖u‖₂²` for two reasons. It is the only place where the
size of `u` enters, so rescaling `u` changes numerator and denominator
proportionally and leaves `proj_u(x)` unchanged, as it must. And it is strictly
positive for `u ≠ 0` by positive definiteness, so it cannot be zero — whereas the
numerator `xᵀu` certainly can be, when `x ⊥ u`. That asymmetry is why the formula
is well posed: the denominator is protected, the numerator is free.

</details>

**Q2. Why is the orthogonal leftover the *smallest possible* error, not merely a
small one?**

<details>
<summary>Model answer</summary>

Write `x = c*·u + r` with `c* = xᵀu/(uᵀu)` and `r` the leftover, so `uᵀr = 0`. For
any other point `cu` on the line,

    ‖x − cu‖₂² = ‖(c* − c)u + r‖₂²
               = (c* − c)²‖u‖₂² + 2(c* − c)uᵀr + ‖r‖₂²
               = (c* − c)²‖u‖₂² + ‖r‖₂²

The cross term vanishes, so the error at any `c ≠ c*` equals the minimum `‖r‖₂²`
plus a strictly positive amount `(c* − c)²‖u‖₂²`. Since `‖u‖₂² > 0` the minimum is
unique.

The lesson calls this "Orthogonality IS optimality" and confirms it by brute
force: scanning 200001 points `t·u` for `t ∈ [−10, 10]` finds the same optimum
`t = 3.5` as the closed formula, with the distance agreeing to `10⁻¹⁰`.

</details>

**Q3. What does Gram–Schmidt preserve, and what does it change?**

<details>
<summary>Model answer</summary>

It preserves the **span** (and hence the dimension) and changes the **basis**.

Preservation holds because the only operation is `w ← w − (uᵀw/uᵀu)u`, i.e.
subtracting a combination of previously accepted vectors. Induction gives that
every `q_k` lies in `span(v_1, …, v_k)` and that each `v_k` lies in
`span(q_1, …, q_k)`, so the two spans coincide.

What changes is orthogonality. By construction `q_k` has had its component along
every earlier `q_j` removed, so `q_jᵀq_k = 0` for all `j < k`; after normalising,
`q_iᵀq_j = δ_ij`.

The corollary is the stopping rule: if the inputs are linearly dependent, some
`q_k` comes out as (numerically) the zero vector, and the count of *nonzero*
outputs is the dimension of the span.

</details>

**Q4. State the normal equations and explain where the orthogonality condition
enters.**

<details>
<summary>Model answer</summary>

The normal equations are `AᵀAβ = Aᵀy`; when `AᵀA` is invertible the unique
least-squares solution is `β̂ = (AᵀA)⁻¹Aᵀy`.

The orthogonality enters like this. At the optimum the residual `r = y − Aβ̂` is
orthogonal to every column `a_j` of `A`, so `a_jᵀr = 0` for all `j`, which collects
into `Aᵀr = 0`. Substituting `r = y − Aβ̂`:

    Aᵀ(y − Aβ̂) = 0
    Aᵀy = AᵀAβ̂

which is the normal equations. No calculus was used — "you cannot improve" became
"the leftover is perpendicular", and `n` perpendicularity conditions is exactly
`n` linear equations in `n` unknowns. Uniqueness then requires `AᵀA` invertible,
i.e. `A` of full column rank.

</details>

**Q5. Compute the least-squares line for `x = (1,2,3,4,5)` and
`y = (2.1, 3.9, 6.2, 7.8, 10.1)`, and report `RSS` and `R²`.**

<details>
<summary>Model answer</summary>

With `A = [1 | x]`: `AᵀA = [[5, 15], [15, 55]]` and `Aᵀy = [30.1, 110.2]`.

Solve: multiply the first row by 3 and subtract from the second, giving
`10β₁ = 19.9`, so `β₁ = 1.99`. Then `5β₀ = 30.1 − 15(1.99) = 0.25`, so
`β₀ = 0.05`.

So `ŷ = 0.05 + 1.99x`. Fitted values `2.04, 4.03, 6.02, 8.01, 10.00`; residuals
`0.06, −0.13, 0.18, −0.21, 0.10`, which sum to 0 and have zero dot product with
the `x` column — the orthogonality check.

`RSS = 0.06² + 0.13² + 0.18² + 0.21² + 0.10² = 0.107`. With `ȳ = 6.22`,
`TSS = 39.708`, so `R² = 1 − 0.107/39.708 = 0.997305`.

</details>

**Q6. State the ridge solution and explain what `λI` does that `AᵀA` alone does
not.**

<details>
<summary>Model answer</summary>

Ridge minimises `‖Aβ − y‖₂² + λ‖β‖₂²`, which yields the normal equations plus one
term:

    (AᵀA + λI)β = Aᵀy

Two effects. **Invertibility**: the eigenvalues of `AᵀA + λI` are `σᵢ² + λ ≥ λ > 0`,
so no zero direction survives and the system is solvable for any `λ > 0` — which
is why ridge returns an answer where the unregularised normal equations raise
`LinAlgError: Singular matrix`.

**Shrinkage**: increasing `λ` drives every `β_j` toward 0, and since the noise
column's coefficient starts much smaller than the real feature's, the *relative*
distortion of the real coefficient is what the penalty limits. The lesson's ridge
table shows the area slope falling from `1.985940` at `λ = 0` to `0.197016` at
`λ = 500`, with RSS rising from `0.105796` to `176.538844`. The noise coefficient
travels only from `−0.037781` to `−0.013457`, so it stays small in absolute terms
throughout — which is exactly why ridge cannot do feature selection.

In practice the intercept is excluded from the penalty, which is what
`sklearn.linear_model.Ridge` does.

</details>

### Long Answer

**Q1. Why is an orthogonal matrix invertible, what is its inverse, and why does
this matter so much in graphics and in numerical linear algebra?**

<details>
<summary>Model answer</summary>

**The proof.** Suppose `Q` is `n × n` and `QᵀQ = I`. Then `Qᵀ` is a *left* inverse.
For square matrices a left inverse is also a right inverse. One route: `QᵀQ = I`
gives `QᵀQ Qᵀ = Qᵀ`, i.e. `Qᵀ(QQᵀ) = Qᵀ`; because `Qᵀ` is invertible (it has
right inverse `Q`), cancel it to get `QQᵀ = I`. Hence `Qᵀ` is a two-sided inverse
and **`Q⁻¹ = Qᵀ`**.

**Why it must be so.** `det(QᵀQ) = det(Q)² = det(I) = 1`, so `|det(Q)| = 1` — the
largest absolute determinant any invertible matrix can have. The columns of `Q`
are orthonormal, so they cannot be collinear and cannot span a degenerate
parallelepiped. Invertibility is forced by the geometry, not granted by luck.

**What it buys.**

*Graphics.* Undoing a rotation is free: `Qᵀ(Qx) = x` is one transpose, no linear
solve. If the transform were not orthogonal, undoing it would need
`np.linalg.solve`, `O(n³)` per frame per object, with accumulated error. That is
why model matrices in
[Part 07](../part07_geometry_graphics/91_transformations_graphics.md) are built
from orthogonal blocks.

*Preservation.* `‖Qx‖₂² = xᵀQᵀQx = xᵀx` and `(Qx)ᵀ(Qy) = xᵀQᵀQy = xᵀy`, so `Q`
preserves lengths and angles: it is a pure rotation (`det = +1`) or a reflection
(`det = −1`). The lesson checks both numerically to 12 decimals — `‖Qx‖ = ‖x‖ =
5.385165` on `x = (2,5)`, and a dot product of 12 before and after on
`y = (1,2)`.

*Conditioning.* All singular values of `Q` equal 1, so `cond(Q) = 1`, the smallest
possible value: no input error is amplified and none is lost. That is why QR
factorisation, which builds `Q` by Gram–Schmidt, is the numerically safe way to
solve least squares, and why the SVD route in
[40](../part03_linear_algebra/40_svd_and_pca.md) works in these coordinates.

**What breaks.** "Orthogonal" is not a yes/no property in floating point; it is a
measurement. With `C = [[1,1],[1,1.001]]` the matrix stays invertible but
`cond(C) = 4002` and `C⁻¹ = [[1001, −1000], [−1000, 1000]]` — entries of order
1000 where the input had entries of order 1. Perturbing `x = (1,1)` by `10⁻⁴` moves
the solution by about 0.1, a factor-1000 amplification. So the practical rule is
to *check* orthogonality (`‖QᵀQ − I‖`) rather than assume it.

</details>

**Q2. Why do the normal equations square the condition number, and what should
you use instead?**

<details>
<summary>Model answer</summary>

**Why.** The singular values of `AᵀA` are the squares of the singular values of
`A`. If `Avᵢ = σᵢuᵢ` is a singular value decomposition, then `AᵀA vᵢ = σᵢ²vᵢ`, so

    cond(AᵀA) = σ_max²/σ_min² = cond(A)²

exactly. On the lesson's own design matrix `[1 | x]` for `x = (1,2,3,4,5)`,
`cond(A) = 8.3657` and `cond(AᵀA) = 69.9857` — which is `8.3657²`.

**Why that is fatal.** A condition number is a worst-case error amplification
factor. With `cond(A) = 10⁴` the answer already has only about 12 reliable digits
of 16; squaring gives `10⁸`, about 8 reliable digits. At `cond(A) ≈ 10⁶` the
normal equations deliver `cond ≈ 10¹²`, so the last four digits are noise.

Worse, the squaring is not a clean rescaling of the error. `AᵀA` is formed by
*summing* products `a_ik a_kj`, and when columns of `A` are nearly parallel those
sums suffer catastrophic cancellation, so the entries of `AᵀA` already carry large
relative error before the solve begins.

A demonstration with a 4×2 design whose second column is
`(1, 1.00000001, 0.99999999, 1.00000002)`: `cond(A) = 1.79 × 10⁸` and
`cond(AᵀA) = 1.27 × 10¹⁶`. `np.linalg.lstsq` and QR both return
`(−3.99999984 × 10⁷, 4.00000007 × 10⁷)`; the normal equations return
`(−2.25179956 × 10⁷, 2.25179980 × 10⁷)` — wrong in the second significant
figure, a 44% relative error, with no error raised at all. Push the perturbation
to `10⁻¹⁰` and `np.linalg.solve(A.T @ A, A.T @ y)` raises
`LinAlgError: Singular matrix` while `lstsq` still returns `(−4 × 10⁹, 4 × 10⁹)`.

**What to do instead.**

- **`np.linalg.lstsq(A, b, rcond=None)`** — computes via the SVD, working in an
  orthonormal basis of the column space and inverting only singular values above
  `rcond`. It also handles rank-deficient `A`, returning the minimum-norm
  solution rather than raising. This is the production default.
- **`Q, R = np.linalg.qr(A)` then `np.linalg.solve(R, Q.T @ b)`** — same
  stability at lower cost, and `R` is triangular so the backsolve is cheap. The
  lesson prints this route and the answer matches `lstsq` exactly.
- **`np.linalg.pinv(A)`** — the Moore–Penrose pseudoinverse `(AᵀA)⁻¹Aᵀ` done
  stably via the SVD, when you want the operator itself rather than one
  application.

**Keep the normal equations for what they are good for**: deriving closed-form
coefficients, proving uniqueness, proving residual orthogonality, and understanding
what ridge is adding. They are the clearest statement of the problem and the worst
way to compute it.

</details>

**Q3. Why does adding a feature column always lower or leave RSS unchanged, and
why does that make `R²` a misleading score?**

<details>
<summary>Model answer</summary>

**The monotonicity.** Least squares minimises over all `β ∈ ℝⁿ`. Adding a column
enlarges that set to `ℝⁿ⁺¹`: the old optimum `(β̂₀, …, β̂_{n−1}, 0)` is still
admissible, with the new coefficient set to 0. A minimum over a larger set cannot
be larger, so `RSS_new ≤ RSS_old` always, with no assumption on the data.

The lesson shows both halves of this. With just the area feature, `RSS = 0.107`.
Adding bedrooms — a real feature — drops it to `0.010667`. Then adding a
pure random-noise column gives `RSS = 0.105796`, still below the one-feature
`0.107`, because the same argument applies: the previous solution with a zero
noise coefficient remains in the search space.

**Why the coefficients get worse anyway.** The noise column is correlated with the
real feature purely by chance. Two nearly-collinear columns split the same
variance between them, and the split is arbitrary because neither explains
anything real. The lesson's numbers show it: the area slope is `1.990000` alone,
`2.084444` with bedrooms, and `1.985940` with the noise column — three different
answers for a quantity the data pins down to no better than about two decimal
places, while RSS and `R²` both improve the whole time.

**Why `R²` misleads.** `R² = 1 − RSS/TSS` uses a fixed `TSS`, so it is a monotone
function of `RSS` and inherits exactly the same monotonicity. Keep adding columns
and `R² → 1`. A model that memorises the training set — one parameter per data
point — achieves `RSS = 0` and `R² = 1.0` while predicting nothing. And
`lr.score()` computes `R²` on *whatever you pass it*, so passing training data
reports the training score.

**What to use instead.** Held-out `R²` on data the fit never saw. Adjusted `R²`,
which charges a penalty for each parameter. Or AIC/BIC. And for regularised
models, choose `λ` on held-out data, because the ridge table shows RSS rising
monotonically with `λ` — so minimising training RSS always selects `λ = 0`, which
is precisely the over-parameterised model you were trying to avoid.

</details>

**Q4. Why is the residual orthogonal to the columns of `A` at the optimum, and
how does that produce a Pythagoras decomposition of the error?**

<details>
<summary>Model answer</summary>

**The orthogonality.** At the optimum, moving `β` along a single column `a_j`
changes the residual by `−εa_j`. The first-order change in squared error is
`2rᵀ(−εa_j) = −2ε(a_jᵀr)`. A minimum requires this to vanish for every `j`, so
`a_jᵀr = 0` for all `j`, i.e. `Aᵀr = 0`. Geometrically: the leftover points in a
direction perpendicular to everything the model uses, so there is nothing to gain
by pushing further along any of them. The lesson verifies `r·1 = 0` and `r·x = 0`
on the worked example.

**The Pythagoras step.** Expand `y = Aβ̂ + r` and take squared lengths:

    ‖y‖₂² = (Aβ̂ + r)ᵀ(Aβ̂ + r) = β̂ᵀAᵀAβ̂ + 2β̂ᵀAᵀr + rᵀr
          = ‖Aβ̂‖₂² + ‖r‖₂²       because Aᵀr = 0

This is [37](../part03_linear_algebra/37_inner_products_norms_geometry.md)'s Pythagoras identity for
vectors: perpendicular pieces have squared lengths that add, with no cross term.
It is also what makes RSS a genuine measure of the *unexplained* variance rather
than partly double-counting the model.

**The caveat, which is the sharp part.** The identity as written needs `Aβ̂ ⟂ r`.
With an intercept column of ones, the residuals sum to zero, so `r` is orthogonal
to the ones column — but `Aβ̂` itself is generally **not** orthogonal to `y`,
because both contain the mean. The correct statement with an intercept is the
decomposition about the mean:

    Σ(yᵢ − ȳ)² = Σ(ŷᵢ − ȳ)² + Σ(yᵢ − ŷᵢ)²

which is `TSS = explained + RSS`, the definition of `R²`. The lesson's code
prints this: total, explained, unexplained, with the last two summing exactly.
Miss the mean correction and the two halves do not add up — a useful check that
you have noticed.

**Why it matters.** Because `r` is orthogonal to the model, the model and the
error share no variance: no part of `Aβ̂` is merely reproducing noise. That is the
honest-fit property, and it is exactly what ridge's `λI` and LASSO's kink give up
deliberately, trading orthogonality for stability and sparsity.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — Gram–Schmidt by hand.** Given `v₁ = (1, 1, 0)`,
`v₂ = (1, 0, 1)`, `v₃ = (1, 1, 1)`:

(a) apply Gram–Schmidt and give the orthogonal set;
(b) normalise each vector to get an orthonormal basis;
(c) verify all pairwise dot products of the orthonormal set;
(d) show that `v₃` was actually redundant by finding the linear combination
that expresses it in terms of `v₁` and `v₂`.

<details>
<summary>Solution</summary>

**(a)** `q₁ = v₁ = (1, 1, 0)`.

`q₂ = v₂ − proj_{q₁}(v₂)`. `q₁·q₁ = 2`, `q₁·v₂ = 1·1 + 1·0 + 0·1 = 1`.
Coefficient `= 1/2`. So `q₂ = (1,0,1) − (1/2)(1,1,0) = (1/2, −1/2, 1)`.
Scale by 2 for tidiness: `q₂ = (1, −1, 2)`. (Scaling is harmless — it stays
orthogonal to `q₁`.)

`q₃ = v₃ − proj_{q₁}(v₃) − proj_{q₂}(v₃)`.
Using `q₁ = (1,1,0)`: `q₁·v₃ = 2`, `q₁·q₁ = 2`, coefficient `= 1`.
Using `q₂ = (1,−1,2)`: `q₂·v₃ = 1 − 1 + 2 = 2`, `q₂·q₂ = 1 + 1 + 4 = 6`,
coefficient `= 2/6 = 1/3`.
`q₃ = (1,1,1) − 1·(1,1,0) − (1/3)(1,−1,2) = (1,1,1) − (1,1,0) − (1/3, −1/3, 2/3)`
`   = (0, 0, 1) − (1/3, −1/3, 2/3) = (−1/3, 1/3, 1/3)`.
Scale by 3: `q₃ = (−1, 1, 1)`.

Orthogonal set: `(1,1,0)`, `(1,−1,2)`, `(−1,1,1)`.

**(b)** Norms: `‖q₁‖ = √2`, `‖q₂‖ = √6`, `‖q₃‖ = √3`.
Orthonormal set: `(1/√2, 1/√2, 0)`, `(1/√6, −1/√6, 2/√6)`, `(−1/√3, 1/√3, 1/√3)`.
Numerically: `(0.7071, 0.7071, 0)`, `(0.4082, −0.4082, 0.8165)`, `(−0.5774, 0.5774, 0.5774)`.

**(c)** `e₁·e₂ = 0.7071(0.4082) + 0.7071(−0.4082) + 0 = 0` ✓
`e₁·e₃ = 0.7071(−0.5774) + 0.7071(0.5774) + 0 = 0` ✓
`e₂·e₃ = 0.4082(−0.5774) + (−0.4082)(0.5774) + 0.8165(0.5774) = −0.2357 − 0.2357 + 0.4714 = 0` ✓
`e₁·e₁ = 0.5 + 0.5 = 1` ✓, and similarly `e₂·e₂ = e₃·e₃ = 1` ✓

**(d)** Solve `a(1,1,0) + b(1,0,1) = (1,1,1)`.
From the first coordinate: `a + b = 1`. Second: `a = 1`. Third: `b = 1`.
So `v₃ = v₁ + v₂`, with `a = b = 1`.

So the three input vectors were **linearly dependent**, and `v₃` spanned
nothing new. Gram–Schmidt handled it correctly: `q₃` came out nonzero only
because it subtracted the projections properly. If the inputs are *exactly*
dependent the third orthogonal vector comes out as the zero vector, which is
the signal to stop — the span has dimension 2, not 3.

</details>

**[ ] Exercise 2 — least squares by hand.** For the data
`(x, y) = (0, 1.1), (1, 2.0), (2, 3.1), (3, 3.9)`:

(a) build the design matrix `A` and the target vector `y`;
(b) compute `AᵀA` and `Aᵀy`;
(c) solve the normal equations for `β₀, β₁`;
(d) compute the residuals and verify they sum to zero and are orthogonal to the
`x` column;
(e) report `RSS` and `R²`.

<details>
<summary>Solution</summary>

**(a)**
```
A = [1  0]      y = [1.1]
    [1  1]          [2.0]
    [1  2]          [3.1]
    [1  3]          [3.9]
```

**(b)**
`AᵀA[0][0] = 4`. `AᵀA[0][1] = 0+1+2+3 = 6`. `AᵀA[1][1] = 0+1+4+9 = 14`.
```
AᵀA = [4  6]
      [6  14]
```
`Aᵀy[0] = 1.1+2.0+3.1+3.9 = 10.1`. `Aᵀy[1] = 0(1.1) + 1(2.0) + 2(3.1) + 3(3.9) = 0 + 2.0 + 6.2 + 11.7 = 19.9`.
```
Aᵀy = [10.1, 19.9]
```

**(c)** The system is `4β₀ + 6β₁ = 10.1` and `6β₀ + 14β₁ = 19.9`.
Multiply the first by 1.5: `6β₀ + 9β₁ = 15.15`. Subtract: `5β₁ = 4.75`, so
`β₁ = 0.95`. Then `4β₀ = 10.1 − 6(0.95) = 10.1 − 5.7 = 4.4`, so `β₀ = 1.1`.

```
β = [1.1, 0.95]
```

**(d)** Fitted values: `1.1`, `2.05`, `3.0`, `3.95`. Residuals (actual − fitted):
`0.0`, `−0.05`, `0.1`, `−0.05`.
- Sum: `0.0 − 0.05 + 0.1 − 0.05 = 0.0` ✓ (this is `r·1 = 0`)
- `r·x = 0(0.0) + 1(−0.05) + 2(0.1) + 3(−0.05) = −0.05 + 0.2 − 0.15 = 0.0` ✓

Both orthogonality conditions hold exactly, confirming the solution is the
least-squares optimum.

**(e)** `RSS = 0² + 0.05² + 0.1² + 0.05² = 0 + 0.0025 + 0.01 + 0.0025 = 0.015`.
`ȳ = (1.1+2.0+3.1+3.9)/4 = 10.1/4 = 2.525`.
`TSS = (1.1−2.525)² + (2.0−2.525)² + (3.1−2.525)² + (3.9−2.525)²`
`    = 2.031006 + 0.275625 + 0.330625 + 1.890625 = 4.527881`.
`R² = 1 − 0.015/4.527881 = 1 − 0.003313 = 0.996687`.

So roughly 99.7% of the variance is explained; the fit is
`y ≈ 1.1 + 0.95x`.

</details>

**Challenge — Exercise 3 — when does the normal matrix fail?** Consider fitting
`y = β₀ + β₁x` to three points where the `x` values are `(1.0, 1.0, 1.0)`.

(a) Show that `AᵀA` is singular and say, in words, what that means about the data.
(b) Explain why `np.linalg.lstsq` still returns an answer and what it returns.
(c) Now suppose the `x` values are `(1.0, 1.0, 1.001)` — a realistic near-miss.
What goes wrong with `AᵀA`, and what does `np.linalg.cond` report?
(d) Propose a preprocessing step that fixes (c) in one line, and explain why it
is standard practice.

<details>
<summary>Solution</summary>

**(a)** `A = [[1, 1], [1, 1], [1, 1]]` — all three rows are identical.
```
AᵀA = [3  3]
      [3  3]
```
Both rows equal, so `det(AᵀA) = 3·3 − 3·3 = 0`. Singular, no inverse.

In words: the feature is **constant**, so it carries no information at all. No
line through the data can distinguish a high value from a low value — the
feature and the intercept column are the *same direction*. The two unknowns
`β₀` and `β₁` are not separately identifiable: only the sum `β₀ + β₁` is
determined by the data, and infinitely many `(β₀, β₁)` pairs give identical
predictions. Least squares is not wrong; the *problem* is under-determined.

**(b)** `np.linalg.lstsq` returns the **minimum-norm** least-squares solution:
among all the solutions that give the same minimum error, the one with the
smallest `‖β‖₂`. It finds this via the SVD (lesson 40) by inverting only the
nonzero singular values, so singular directions get a coefficient of exactly
zero. It never attempts to invert the singular part.

For the constant-`x` case, `A = 1·(1,1,1)ᵀ ⊗ (1,1)`, rank 1, so the minimum-norm
solution puts everything on the single independent direction: `β₀ = β₁` and
`Aβ` is the mean of `y` repeated. Concretely with `y = (2, 3, 4)`, mean 3, the
answer is `β = [1.5, 1.5]` — which is the unique minimum-norm split of
`β₀ + β₁ = 3`.

**(c)** With `x = (1, 1, 1.001)`:
```
AᵀA = [3        3.001  ]
      [3.001    3.002001]
```
`det = 3(3.002001) − (3.001)² = 9.006003 − 9.006001 = 0.000002`. Tiny but
nonzero, so it *is* invertible — and the inverse is enormous, of order
`1/0.000002 ≈ 500000`. The normal equations amplify every rounding error by
that factor.

`np.linalg.cond(AᵀA)` reports roughly `cond(A)²`, which is on the order of
`2.5 × 10¹¹` here. A condition number that large means the last few digits of
the answer are pure noise: the slope `β₁` comes out as something like
`999500 ± 500` — numerically meaningless. `np.linalg.solve` may even return
`nan` or raise, because the pivot is treated as zero.

The root cause is that `x` has a large **mean** (≈1) relative to its spread
(≈0.0005). An uncentred column nearly parallel to the intercept column.

**(d)** Subtract the mean: `x ← x − mean(x)`. Then `x = (0, 0, 0.001)`, the
intercept and feature columns become nearly perpendicular, and `AᵀA` is
well-conditioned.

Why standard practice: centring removes the constant component of each feature,
so the design matrix's columns are uncorrelated by construction and
`AᵀA ≈ diagonal`. In practice you centre *and* divide by the standard deviation
(standardisation), which puts every feature on the same scale so that a single
regularisation parameter λ means the same thing for all of them. That is exactly
what the `StandardScaler` in a scikit-learn pipeline does, and it is why the
pipelines in the "With Libraries" block above start with a scaler.

The deeper fix is to stop forming `AᵀA` at all: `np.linalg.lstsq` uses the SVD,
which never squares the condition number, and `np.linalg.qr` gives the same
stability for a fraction of the cost.

</details>

**[ ] Exercise 4 — projection onto a basis, and the projection matrix.** Let
`u₁ = (1, 1)` and `u₂ = (1, −1)`.

(a) Normalise both to get an orthonormal basis `e₁, e₂`.
(b) Build `Q = [e₁ | e₂]` and verify `QᵀQ = I` exactly.
(c) Use `Q` to decompose `w = (3, 4)`: compute the coefficients `Qᵀw`, then
rebuild `w`, then compute the residual.
(d) Build the projection matrix `P = QQᵀ` and check `P² = P` and `Pᵀ = P`.
(e) Explain why `‖P‖₂ = 1` and why that is the statement "`P` discards something".

<details>
<summary>Solution</summary>

**(a)** `‖u₁‖₂ = √(1+1) = √2`, so `e₁ = (1/√2, 1/√2) = (0.7071, 0.7071)`.
`‖u₂‖₂ = √2` as well, so `e₂ = (1/√2, −1/√2) = (0.7071, −0.7071)`.

**(b)**

    Q = [ 0.7071  0.7071 ]
        [ 0.7071 -0.7071 ]

    Q^T Q = [ 0.5+0.5   0.5-0.5 ]  = [1  0]
            [ 0.5-0.5   0.5+0.5 ]    [0  1]

Exactly the identity. `e₁·e₂ = 0.7071(0.7071) + 0.7071(−0.7071) = 0.5 − 0.5 = 0`,
and both have squared length 1.

**(c)** `Qᵀw = (e₁·w, e₂·w)ᵀ`:

    e₁·w = (3 + 4)/√2 = 7/√2 = 4.9497
    e₂·w = (3 − 4)/√2 = −1/√2 = −0.7071

Rebuild: `e₁(4.9497) + e₂(−0.7071) = (3.5 − 0.5, 3.5 + 0.5) = (3, 4)` ✓
The residual is `(3,4) − (3,4) = (0, 0)`, exactly zero.

That is expected and is the point of part (c): `e₁` and `e₂` span *all* of `ℝ²`,
so the projection onto the whole space is the identity. The lesson's code makes
the same observation. To see a nonzero residual you must project onto a *proper*
subspace — that is Exercise 6.

**(d)**

    P = Q Q^T = [ 0.7071·0.7071 + 0.7071·0.7071 , 0.7071·0.7071 + 0.7071(−0.7071) ]
        [ 0.7071·0.7071 + (−0.7071)·0.7071 , 0.7071·0.7071 + (−0.7071)(−0.7071) ]

      = [ 1.0   0.0 ]
        [ 0.0   1.0 ]

which is `I`, consistent with part (c). `P² = I² = I = P` ✓ and `Pᵀ = P` ✓
(it is symmetric, as every projection matrix must be).

**(e)** `P` is orthogonal (symmetric with `P² = P`), so all its singular values are
1 and `‖P‖₂ = 1`. And `P = I` has `rank 2` out of size 2 — it discards
*nothing*, which is the degenerate case. In general `rank(P) = dim(span{e₁,…})`,
so projecting `(3,4)` onto the single direction `e₁` gives

    P = e₁ e₁^T = [0.5  0.5]
                  [0.5  0.5]

with `rank(P) = 1 < 2`, `P² = P`, `Pᵀ = P`, and `‖P‖₂ = 1`. The "discards
something" content is `rank(P) < size(P)`: the vector `(1,−1)/√2` is annihilated,
since `P(1,−1)/√2 = (0, 0)`. If `P` were invertible, `P² = P` would force
`P = I`, so the only invertible projection is the identity.

</details>

**[ ] Exercise 5 — fit two features by hand and compare with ridge.** Use
`x = (1, 2, 3, 4, 5)` for area, `z = (1, 3, 2, 4, 3)` for bedrooms, and
`y = (2.1, 3.9, 6.2, 7.8, 10.1)`.

(a) Build `A = [1 | x | z]` and compute `AᵀA` and `Aᵀy`.
(b) Solve the normal equations for `β`.
(c) Report `RSS` and `R²`.
(d) Solve `(AᵀA + I)β = Aᵀy` (ridge with `λ = 1`, all three coefficients
penalised) and report the new `RSS`.
(e) Explain, using the numbers, why the penalised fit is worse on the training
data and might still be better on new data.

<details>
<summary>Solution</summary>

**(a)** `AᵀA` has entries that are column-wise dot products:

    A^T A = [ 5   15    13  ]
            [ 15  55    44  ]
            [ 13  44    39  ]

`AᵀA[0][0] = Σ1 = 5`. `AᵀA[0][1] = Σx = 15`. `AᵀA[0][2] = Σz = 13`.
`AᵀA[1][1] = Σx² = 1+4+9+16+25 = 55`. `AᵀA[1][2] = Σxz = 1+6+6+16+15 = 44`.
`AᵀA[2][2] = Σz² = 1+9+4+16+9 = 39`.

    A^T y = [ 30.1   110.2   87.7 ]

`Σy = 30.1`; `Σxy = 2.1 + 7.8 + 18.6 + 31.2 + 50.5 = 110.2`;
`Σzy = 2.1 + 11.7 + 12.4 + 31.2 + 30.3 = 87.7`.

**(b)** Solve

    5β₀ + 15β₁ + 13β₂ = 30.1
    15β₀ + 55β₁ + 44β₂ = 110.2
    13β₀ + 44β₁ + 39β₂ = 87.7

Subtract `(b₀ + 3b₁ + 2b₂) = 5.9883` — obtained by dividing row 3 by 13 and
multiplying by 30.1/… — the cleaner route is to eliminate `β₀`. Row 2 minus 3×row 1:

    (55 − 45)β₁ + (44 − 39)β₂ = 110.2 − 90.3
    10β₁ + 5β₂ = 19.9                       ... (i)

Row 3 minus (13/5)×row 1:

    (44 − 39)β₁ + (39 − 33.8)β₂ = 87.7 − 78.26
    5β₁ + 5.2β₂ = 9.44                      ... (ii)

From (i): `β₁ = 1.99 − 0.5β₂`. Substitute into (ii):
`5(1.99 − 0.5β₂) + 5.2β₂ = 9.44` → `9.95 − 2.5β₂ + 5.2β₂ = 9.44` →
`2.7β₂ = −0.51` → `β₂ = −0.188889`. Then `β₁ = 1.99 − 0.5(−0.188889) = 2.084444`,
and `β₀ = (30.1 − 15(2.084444) − 13(−0.188889))/5 = (30.1 − 31.266667 + 2.455556)/5 =
1.288889/5 = 0.257778`.

    β = [0.257778, 2.084444, -0.188889]

**(c)** Evaluate `ŷ = β₀ + β₁x + β₂z` row by row:

| `x` | `z` | `ŷ` | `r = y − ŷ` |
| --- | --- | --- | --- |
| 1 | 1 | 2.153333 | −0.053333 |
| 2 | 3 | 3.860000 | +0.040000 |
| 3 | 2 | 6.133333 | +0.066667 |
| 4 | 4 | 7.840000 | −0.040000 |
| 5 | 3 | 10.113333 | −0.013333 |

`RSS = 0.002844 + 0.001600 + 0.004444 + 0.001600 + 0.000178 = 0.010667`.

`TSS = 39.708` as before, so `R² = 1 − 0.010667/39.708 = 0.999731`. Compare the
one-feature fit's `RSS = 0.107`: bedrooms genuinely carry signal, so the error
dropped by a factor of 10.

Orthogonality check: `Σr = −0.053333 + 0.04 + 0.066667 − 0.04 − 0.013333 = 0` ✓,
`r·x = −0.053333 + 0.08 + 0.2 − 0.16 − 0.066667 = 0` ✓, and
`r·z = −0.053333 + 0.12 + 0.133333 − 0.16 − 0.04 = 0` ✓.

**(d)** With `λ = 1` on all three coefficients,

    A^T A + I = [ 6  15  13 ]
                [ 15 56  44 ]
                [ 13 44  40 ]

Solving gives

    β_ridge = [0.194615, 1.788654, 0.161731]

Fitted values `2.145000, 4.257115, 5.884038, 7.996154, 9.623077`; residuals
`(−0.045000, −0.357115, +0.315962, −0.196154, +0.476923)`.

`RSS = 0.002025 + 0.127411 + 0.099832 + 0.038476 + 0.227456 = 0.495320`.

**(e)** RSS jumped from `0.010667` to `0.495320`, a factor of about 46. That is
not a bug. The penalised problem is a *different* objective,
`RSS + λ‖β‖₂²`, and its minimiser need not minimise `RSS` at all. With `λ = 0`
the plain least-squares fit is optimal by definition; with `λ = 1` we have
deliberately accepted a worse fit in exchange for smaller coefficients — the
penalty dropped `‖β‖₂²` from `0.257778² + 2.084444² + 0.188889² = 4.4192` to
`0.037876 + 3.1993 + 0.026157 = 3.2633`.

Whether the trade pays depends on new data, and two features of these numbers
suggest it might. The bedroom coefficient **flips sign**, from `−0.188889` to
`+0.161731`: a sign flip in a coefficient is a classic symptom of fitting noise,
because a genuinely causal feature does not reverse direction when the penalty
changes. And `z` is correlated with area — `Σxz = 44` against
`(Σx)(Σz)/5 = 15·13/5 = 39`, a correlation of about `0.997` — so `z`'s
coefficient is barely determined by these five points: the two columns compete
for the same variance and the split between them is close to arbitrary.

So a large in-sample penalty with a stabilised coefficient is often the right
trade. Choosing `λ` on held-out data is exactly how you find out; choosing `λ = 0`
because it minimises training RSS guarantees you never find out.

</details>

**Challenge — Exercise 6 — where the normal equations lose digits, measured.**
Let `A` be the 4×2 matrix whose first column is all ones and whose second column
is `(1, 1.001, 0.999, 1.002)`, and let `b = (1, 2, 3, 4)`.

(a) Compute `cond(A)` and `cond(AᵀA)` and check the squaring relation.
(b) Solve the problem three ways: with `np.linalg.lstsq`, with QR
(`Q, R = np.linalg.qr(A)` then solve `Rβ = Qᵀb`), and with the normal equations
`np.linalg.solve(AᵀA, Aᵀb)`.
(c) Report the relative difference between the normal-equation answer and the
`lstsq` answer, and the `RSS` for each.
(d) Now replace `1.001, 0.999, 1.002` by `1.00000001, 0.99999999, 1.00000002`,
and then by `1.0000000001, 0.9999999999, 1.0000000002`. Report what each of the
three methods returns at each scale, and explain what is happening.
(e) State the practical rule this supports, and say what the normal equations are
still good for.

<details>
<summary>Solution</summary>

**(a)** `A = [[1, 1], [1, 1.001], [1, 0.999], [1, 1.002]]`. Its two columns are
nearly parallel — the angle between them is about `10⁻³` radians, not 90°.
Numerically:

    cond(A)     = 1789.7496
    cond(A^T A) = 3203203.6019
    cond(A)^2   = 3203203.6024

The relation `cond(AᵀA) = cond(A)²` holds to five significant figures — it is an
exact identity in exact arithmetic.

**(b)**

    np.linalg.lstsq(A, b, rcond=None)[0]  ->  [-397.70000000,  400.00000000]
    np.linalg.solve(R, Q.T @ b)  (QR)      ->  [-397.70000000,  400.00000000]
    np.linalg.solve(A.T @ A, A.T @ b)      ->  [-397.70000001,  400.00000001]

**(c)** Relative difference, per component:

    |−397.7000000082 − (−397.7)| / 397.7 = 2.05 × 10^-11

RSS values:

    lstsq : 4.20000000000
    QR    : 4.20000000000
    normal: 4.20000000000

At `cond(A) ≈ 1.8 × 10³` the normal equations lose about 5 of their 16 digits and
are still usable. That is the key calibration: squaring `10³` gives `10⁶`, so you
keep roughly `16 − 6 = 10` significant digits. Nothing has visibly broken yet.

**(d)** Two further scales.

At `10⁻⁸` offsets — second column `(1, 1.00000001, 0.99999999, 1.00000002)`:

    cond(A) = 1.7888544 × 10^8      cond(A^T A) = 1.2738103 × 10^16
    lstsq -> [-3.99999984 × 10^7,  4.00000007 × 10^7]
    QR    -> [-3.99999984 × 10^7,  4.00000007 × 10^7]
    normal-> [-2.25179956 × 10^7,  2.25179980 × 10^7]

Now the normal-equation answer is wrong in its **second significant figure** —
`2.25 × 10⁷` instead of `4.00 × 10⁷`, a 44% relative error — while `lstsq` and QR
are unchanged, because neither of them forms `AᵀA`. Note `cond(AᵀA) ≈ 1.27 × 10¹⁶`
is now within a factor of 10 of machine epsilon `≈ 2.2 × 10⁻¹⁶`: the normal matrix
has no significant digits left, and it happens not to have been flagged as
singular yet.

At `10⁻¹⁰` offsets:

    cond(A) = 1.7888542 × 10^10
    lstsq -> [-3.99999967 × 10^9,  3.99999967 × 10^9]
    normal-> LinAlgError: Singular matrix

Here `cond(AᵀA) ≈ 3 × 10²⁰`, far beyond what double precision can represent
distinctly, so the computed `AᵀA` has *exactly* a zero pivot and partial pivoting
raises. The failure is not a rounding accident — the arithmetic being performed has
no answer.

The pattern to recognise: the normal equations do not degrade gracefully, they
degrade *silently and then abruptly*. The `lstsq` and QR answers are stable across
all three scales because they work with `cond = 1` orthogonal coordinates and a
triangular back-substitution, and never square anything.

**(e)** **The rule:** for a least-squares solve, use `np.linalg.lstsq` (or QR when
you also need the factorisation), not `np.linalg.solve(AᵀA, Aᵀb)`. And do not
test `AᵀA` for invertibility as your guard — by the time you can compute its
condition number you have already formed the matrix you were trying to avoid.
Check `np.linalg.cond(A)` instead, and treat anything above about `10⁸` as a
signal to rescale the features rather than to trust the digits.

**What the normal equations remain good for.** They are the clearest single
statement of the problem: `AᵀAβ = Aᵀy` says "the residual is orthogonal to
everything the model used", which is the entire geometry of least squares and the
easiest route to proving uniqueness, to deriving the closed form, and to seeing
what ridge's `+λI` is doing. They are excellent for hand computation, for
symbolic algebra, and for teaching. They are the wrong way to compute.

</details>

## Summary

- **Projection** splits a vector into the part along a direction and the part
  perpendicular to it: `proj_u(x) = (xᵀu / uᵀu) u`.
- The perpendicular leftover **is** the optimality proof: any other point on the
  line is strictly further away, because the cross term vanishes.
- **Gram–Schmidt** turns any independent set into an orthogonal set of the same
  span, by repeatedly subtracting projections. The output satisfies
  `uᵢᵀuⱼ = δᵢⱼ` once normalised.
- An **orthogonal matrix** has `QᵀQ = I`, so `Q⁻¹ = Qᵀ` for free, and it
  preserves all lengths and angles — it is a pure rotation or reflection.
- **Least squares** asks for the best `β` in `Aβ ≈ y`. The answer is the
  **normal equations** `AᵀAβ = Aᵀy`, derived from the residual being
  orthogonal to every column of `A`.
- The residual orthogonality also gives `‖y‖² = ‖Aβ‖² + ‖r‖²` by Pythagoras —
  the model and the error carry no shared variance.
- Least squares is **unique only when `A` has full column rank**; otherwise
  `AᵀA` is singular and infinitely many fits tie.
- The normal equations **square the condition number**, which is why
  `np.linalg.lstsq` (SVD-based) is the right default in production.
- **Ridge** adds `λI` to the normal matrix, shrinking coefficients, keeping the
  system solvable, and trading a worse RSS for a better model.

## Next

[39 — Diagonalization and Spectral Theory](../part03_linear_algebra/39_diagonalization_and_spectral.md)
asks when these eigenvalues can actually be used to simplify a matrix. Not
always: defective matrices refuse to diagonalise, and this lesson's
Gram–Schmidt output, applied to a matrix's columns, is the QR factorisation
whose pivots do the work.
