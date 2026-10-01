# 39 — Diagonalization and Spectral Theory

**Part**: part03_linear_algebra · **Prerequisites**: 38 · **Time**: 40 min

---

## In Plain Words

[Lesson 36](../part03_linear_algebra/36_eigenvalues_and_eigenvectors.md) found the special directions a
matrix stretches or squashes. This lesson asks the obvious follow-up: can you
use those directions to make the matrix *simple*?

Sometimes yes, and the result is beautiful. If you rotate your coordinate
system so that the eigenvectors become the new axes, the matrix stops being a
mix of everything and becomes a plain list of numbers on the diagonal — a row
of numbers doing nothing but being multiplied. Any complicated thing you do to
the matrix can then be done to those numbers instead, and they are trivial.
Raising a matrix to the thousandth power becomes arithmetic you could do in
your head.

Sometimes it does not work, and it is worth knowing exactly when. Some matrices
are like a tangle: every direction is tied to every other, and there simply are
not enough clean directions to build axes from. This is not a flaw in the
method — it is a fact about the matrix, and it tells you something real.

Then this lesson covers the case that matters enormously in machine learning:
when a matrix is *symmetric*, the tangle never happens. You always get
orthogonal axes, always real numbers, always a unique answer. Covariance
matrices and Hessians are symmetric, which is why so much of ML is
well-behaved.

## Why Computer Science Cares

- **`np.linalg.eigh` exists because of the spectral theorem.** It is faster
  and better conditioned than `np.linalg.eig` for symmetric input, and it is
  the function behind PCA, spectral clustering, and every quadratic-form
  calculation.
- **Matrix powers and exponentials.** `A^k = V D^k V⁻¹` turns an
  `O(n³ log k)` computation into `O(n³)`. This is how long-run Markov chain
  behaviour and the Kalman filter are computed.
- **PCA** is literally the eigendecomposition of a covariance matrix, which is
  symmetric positive definite. [Lesson 40](../part03_linear_algebra/40_svd_and_pca.md) derives it.
- **Convexity.** A symmetric matrix is positive definite exactly when all its
  eigenvalues are positive, which is exactly when `xᵀAx > 0` for all nonzero
  `x`. That is the algebraic condition for a convex loss, so "the Hessian is
  positive definite" is the standard test that an optimisation problem has a
  unique minimum.
- **Condition numbers and stability.** `np.linalg.cond` on a covariance matrix
  is how you detect collinear features before they silently destroy your fit.
- **Graph algorithms.** The Laplacian (lesson
  [41](../part03_linear_algebra/41_matrices_graphs_and_applications.md)) is symmetric positive definite,
  so spectral clustering and the algebraic connectivity of a network both fall
  out of this lesson.
- **Interview questions.** "Why are the eigenvalues of a symmetric matrix
  real?", "what is a defective matrix?", "what is Cholesky decomposition
  used for?" all come from here.

## The Formal Version

**Definition.** `A` is **diagonalisable** if there exist an invertible `V` and a
diagonal `D` with `A = V D V⁻¹`. Equivalently, `V⁻¹AV = D`.

**Explanation.** The similarity `V⁻¹AV` means: change basis by `V`, do the work
in the new basis, change back. Diagonalisability means there *is* a basis in
which `A` does nothing but scale each axis independently. The columns of `V`
are the eigenvectors, and the diagonal entries of `D` are the eigenvalues.

**Theorem.** `A` is diagonalisable if and only if it has `n` linearly
independent eigenvectors, if and only if `dim E_λ = mult_alg(λ)` for every
eigenvalue `λ`.

**Theorem (Cayley–Hamilton).** Every square matrix satisfies
`p_A(A) = det(A − λI)` evaluated at `A`, that is

```
A^n + c_{n-1}A^{n-1} + ⋯ + c_1 A + c_0 I = 0
```

**Explanation.** This is the practical workhorse of the lesson. It says a
matrix satisfies a polynomial equation of degree exactly `n`, so it behaves
like a single number that happens to have a richer algebra. Concretely, to
compute `f(A)` for any function `f`, expand `f` in terms of the minimal
polynomial and you need at most `n` matrix powers. For the matrix exponential
`e^A` that turns an infinite series into `n` multiplies — and `e^A` is how you
solve `x' = Ax`, the ODE underlying every linear Kalman filter.

**Definition.** The **minimal polynomial** `m_A` is the monic polynomial of
least degree with `m_A(A) = 0`.

**Theorem.** `m_A` divides `p_A` and has the same roots. `deg m_A` equals the
size of the largest Jordan block.

**Explanation.** Same roots because the roots of `m_A` are exactly the
eigenvalues. Smaller degree means a shorter chain of powers, so a
low-degree minimal polynomial means cheaper evaluation of every function of
`A`. A scalar matrix `λI` has `m_A = L − λ`, so `f(λI) = f(λ)I` for any `f` —
obvious, and a useful sanity check.

**Definition.** A matrix is **defective** if it is not diagonalisable.

**Theorem (Spectral theorem).** If `A` is real and symmetric then all its
eigenvalues are real, and it is diagonalisable by an **orthogonal** matrix:
`A = Q D Qᵀ` with `QᵀQ = I`.

**Explanation.** This is the single most important theorem in applied linear
algebra. Because `Q⁻¹ = Qᵀ`, the change of basis is numerically free. Proof
sketch: if `Au = λu` and `Av = μv` then `(λ−μ)(uᵀv) = 0` by symmetry of `A`, so
different eigenvalues give perpendicular eigenvectors; equal eigenvalues allow
an orthonormal basis by Gram–Schmidt.

**Definition.** `A` is **positive definite** if `xᵀAx > 0` for every nonzero
`x`. If `xᵀAx ≥ 0` for all `x` it is **positive semidefinite**.

**Theorem.** `A` is symmetric positive definite if and only if all its
eigenvalues are positive.

**Explanation.** In the eigenbasis, `xᵀAx = Σ λᵢcᵢ²` where `c` are the
coordinates of `x`. That is a weighted sum of squares, positive exactly when
every `λᵢ` is positive.

**Theorem (Sylvester's criterion).** A symmetric matrix is positive definite if
and only if every **leading principal minor** (the determinant of the top-left
`k × k` block) is positive.

**Explanation.** Cheaper than computing eigenvalues when you only want a yes/no
answer — and the basis of the Cholesky algorithm.

**Theorem (Cholesky).** Every symmetric positive definite matrix has a unique
lower-triangular `L` with positive diagonal such that `A = LLᵀ`.

**Explanation.** Uniqueness with a positive diagonal makes it canonical, unlike
a general matrix square root. It turns a linear solve into two triangular
solves, and it is a cheap positive-definiteness test in its own right: the
algorithm fails if and only if the matrix is not positive definite.

**Definition.** A **Jordan block** `J_λ` is a triangular matrix with `λ` on the
diagonal and `1`s on the superdiagonal.

**Theorem (Jordan form).** Every square matrix over `ℂ` is similar to a Jordan
form: a block-diagonal matrix of Jordan blocks. It is the simplest matrix
similar to `A`.

**Explanation.** Jordan form is the right answer when diagonalisation fails. It
encodes the chain of generalised eigenvectors, which is precisely the
information the eigenvalues discard. Computationally it is numerically
delicate — an arbitrarily small perturbation can split one block into several
— so in practice use the Schur decomposition or avoid it entirely via the SVD.

See [SYMBOLS.md](../SYMBOLS.md) for `λ`, `x`, `Aᵀ`, `A⁻¹`, `tr(A)`, `det(A)`, `Q`.

## Worked Example

Take `A = [[4, 1, 2], [1, 3, 0], [2, 0, 2]]`. It is symmetric, so the spectral
theorem applies and we can find `Q` orthogonally.

**Step 1: the characteristic polynomial.** Using Faddeev–LeVerrier
(`c_k = −tr(M_k)/k`), or by direct expansion of `det(A − λI)`, we get

```
p_A(λ) = λ³ − 9λ² + 21λ − 6
```

**Step 2: the eigenvalues.** Solving `p_A(λ) = 0` numerically gives
`λ ≈ 0.6385`, `2.8326`, `5.5289`. All three are **real**, as promised by
symmetry. Sanity check: `tr(A) = 4 + 3 + 2 = 9`, and `0.6385 + 2.8326 +
5.5289 = 9.0000` ✓. Also `det(A) = 6`, and `0.6385 × 2.8326 × 5.5289 ≈ 10.0`
— hmm, that does not match, which means the polynomial above is wrong.

Let me redo the constant term. `det(A) = 4(3·2 − 0·0) − 1(1·2 − 0·2) + 2(1·0 − 3·2)
= 4(6) − 1(2) + 2(−6) = 24 − 2 − 12 = 10`. So `p_A(λ) = λ³ − 9λ² + c₂λ − 10`,
and the eigenvalues must multiply to 10. The correct expansion gives
`p_A(λ) = λ³ − 9λ² + 21λ − 10`, whose roots are indeed `0.6385, 2.8326,
5.5289` — and `0.6385 × 2.8326 × 5.5289 = 10.00` ✓.

**Step 3: the eigenvectors.** Solve `(A − λI)u = 0` for each `λ`. Using
Jacobi rotations, which diagonalise the matrix directly, gives an orthonormal
set:

```
Q = [ 0.5474   0.8227   0.1535 ]      D = [0.6385  0     0   ]
    [-0.2318   0.3253  -0.9168]          [ 0      2.8326 0  ]
    [-0.8041   0.4662   0.3688]          [ 0      0      5.5289]
```

**Step 4: verify orthogonality.** `QᵀQ = I` to machine precision — the
off-diagonal entries are of order `1e-16`. Compare this with lesson 36, where
the eigenvectors of the *non*-symmetric matrix had to be normalised by hand
and were not mutually perpendicular at all. Symmetry is doing real work.

**Step 5: verify the decomposition.** `QᵀSQ = D` exactly (up to rounding), and
therefore `S = Q D Qᵀ`. Because `Q⁻¹ = Qᵀ`, no matrix inverse is ever computed.

**Step 6: exploit it.** `S^k = Q D^k Qᵀ`, so `S^10` costs one diagonal
exponentiation rather than ten matrix multiplies. Check: the largest entry of
`S^10` is `5.5289^10 ≈ 2.4 × 10^7`, dominated entirely by the top eigenvalue —
which is the practical content of "the data spreads along one direction more
than the others", i.e. PCA.

**Step 7: positive definiteness.** All three eigenvalues are positive, so `S`
is positive definite. Leading minors: `4`, `11`, `10` — all positive, confirming
by Sylvester's criterion. Cholesky gives

```
L = [ 2.0000   0       0    ]
    [ 0.5000   1.6583  0    ]
    [ 1.0000  -0.3015  0.9535]
```

and `LLᵀ = S` exactly. Solving `Sx = (1,2,3)` by two triangular solves gives
`x = (−1.6, 1.2, 3.1)`, matching a full matrix inverse.

## Runnable Code

Cayley–Hamilton and the minimal polynomial:

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

def matmul_list(*Ms):
    out = Ms[0]
    for M in Ms[1:]:
        out = matmul(out, M)
    return out

def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

def trace(A):
    return sum(A[i][i] for i in range(len(A)))

def det(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    total = 0.0
    for j in range(n):
        minor = [row[:j] + row[j + 1:] for row in A[1:]]
        total += ((-1) ** j) * A[0][j] * det(minor)
    return total

def print_matrix(A, title=""):
    if title:
        print(title)
    for row in A:
        print("   " + "".join(f"{v:9.4f}" for v in row))
    print()

def poly_mul(p, q):
    """Multiply two polynomials given as coefficient lists, highest power first."""
    out = [0.0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out

def poly_eval(c, x):
    acc = 0.0
    for coef in c:
        acc = acc * x + coef
    return acc

def poly_str(c, var="L"):
    n = len(c) - 1
    out = ""
    for k, coef in enumerate(c):
        p = n - k
        if abs(coef) < 1e-12:
            continue
        s = "-" if coef < 0 else ("+" if out else "")
        m = f"{abs(coef):g}"
        body = {0: m, 1: f"{m}*{var}"}.get(p, f"{m}*{var}^{p}")
        out = f"{out} {s} {body}" if out else body
    return out or "0"

def poly_deriv(c):
    n = len(c) - 1
    return [c[i] * (n - i) for i in range(n)]

def poly_divmod(a, b):
    a, b = list(a), list(b)
    q = [0.0] * max(1, len(a) - len(b) + 1)
    while len(a) >= len(b) and len(a) >= 1 and abs(a[-1]) > 1e-13:
        f = a[-1] / b[-1]
        d = len(a) - len(b)
        q[d] += f
        for i, coef in enumerate(b):
            a[d + i] -= f * coef
        while len(a) > 1 and abs(a[-1]) < 1e-13:
            a.pop()
    return q, a

def charpoly(A):
    n = len(A)
    c = [1.0]
    M = identity(n)
    for k in range(1, n + 1):
        M = matmul(A, M)
        c.append(-trace(M) / k)
        for i in range(n):
            M[i][i] += c[k]
    return c

# ---------- Cayley-Hamilton: the practical punchline ----------

def poly_horner_matrix(coeffs, A):
    """Evaluate the polynomial with coefficients `coeffs` (highest power first)
    AT THE MATRIX A, using Horner's rule. This is the only sane evaluation
    order: k matrix multiplies, no huge intermediate powers."""
    n = len(A)
    I = identity(n)
    acc = [[coeffs[0] * I[i][j] for j in range(n)] for i in range(n)]
    for coef in coeffs[1:]:
        acc = matmul(acc, A)
        for i in range(n):
            acc[i][i] += coef
    return acc

A = [[4.0, 1.0, 0.0],
     [0.0, 3.0, 1.0],
     [0.0, 0.0, 2.0]]

print("--- Cayley-Hamilton: p_A(A) is exactly the zero matrix ---")
print("The characteristic polynomial of A is")
p = charpoly(A)
print(f"   p_A(L) = {poly_str(p)}")
print("A is upper triangular, so the eigenvalues are its diagonal 4, 3, 2 and")
print("p_A(L) = (L-4)(L-3)(L-2) = L^3 - 9L^2 + 26L - 24. Substitute A for L:")
resid = poly_horner_matrix(p, A)
print_matrix(resid, "   p_A(A) =")
print(f"   every entry is 0: {all(abs(x) < 1e-9 for row in resid for x in row)}")
print()
print("This is not a curiosity. It is the reason a k x k matrix behaves like a")
print("polynomial of degree k, and it is how you compute ANY function of a")
print("matrix -- including the matrix exponential, which is how you solve an")
print("ODE system like a Kalman filter. Cost: k matrix multiplies instead of an")
print("infinite series.")
print()
print("Cross-checks that hold for every matrix:")
print(f"   trace(A) = {trace(A)}   and  -c_1 = {-p[1]}   (equal: sum of eigenvalues)")
print(f"   det(A)   = {det(A)}   and   c_3 = {p[3]}    (equal: product of eigenvalues)")

print("\n--- the minimal polynomial: the shortest relation that kills A ---")

def poly_trim(c):
    c = list(c)
    while len(c) > 1 and abs(c[-1]) < 1e-11 * max(abs(x) for x in c):
        c.pop()
    return c

def _bisect(co, lo, hi):
    f_lo = poly_eval(co, lo)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f_lo * poly_eval(co, mid) <= 0:
            hi = mid
        else:
            lo, f_lo = mid, poly_eval(co, mid)
    return 0.5 * (lo + hi)

def real_roots_by_deflation(c, grid=4000):
    """Every real root, with multiplicity, by sign-change scanning and
    deflation. A root of even multiplicity has no sign change, but it is also
    a root of the derivative, so the derivative is scanned too."""
    c = poly_trim([float(x) for x in c])
    out = []
    while len(c) > 1:
        b = 1.0 + max(abs(x) for x in c[1:]) / abs(c[0])
        scale = max(abs(x) for x in c)
        tol = 1e-12 * scale
        dc = poly_trim(poly_deriv(c))
        step = 2 * b / grid
        found = None
        # pass 1: a root either sits ON a grid point (so the value is ~0, which
        # is what happens for exact integer roots) or between two of them and
        # flips the sign. Both cases must be caught.
        x_prev, y_prev = -b, poly_eval(c, -b)
        seeds = []
        for i in range(1, grid + 1):
            x = -b + i * step
            y = poly_eval(c, x)
            if abs(y) <= tol:
                seeds.append(("exact", x))
            elif y_prev * y < 0:
                seeds.append(("bracket", 0.5 * (x_prev + x)))
            x_prev, y_prev = x, y
        for kind, s in seeds:
            if kind == "exact":
                found = s
                break
            lo, hi = s - step, s + step
            if poly_eval(c, lo) * poly_eval(c, hi) < 0:
                found = _bisect(c, lo, hi)
                break
        # pass 2: even-multiplicity roots sit on a critical point
        if found is None and len(c) > 2 and len(dc) > 1:
            x_prev, y_prev = -b, poly_eval(dc, -b)
            crit = []
            for i in range(1, grid + 1):
                x = -b + i * step
                y = poly_eval(dc, x)
                if y_prev * y < 0:
                    crit.append(0.5 * (x_prev + x))
                x_prev, y_prev = x, y
            for s in crit:
                lo, hi = s - step, s + step
                t = _bisect(dc, lo, hi) if poly_eval(dc, lo) * poly_eval(dc, hi) < 0 else s
                if abs(poly_eval(c, t)) <= tol:
                    found = t
                    break
        if found is None:
            break
        out.append(found)
        c = poly_trim(poly_divmod(c, [1.0, -found])[0])
    return out

def minimal_poly(A):
    """The monic polynomial of least degree with m(A) = 0.

    It is always a DIVISOR of the characteristic polynomial, formed by choosing
    an exponent e_i in 0..a_i for each eigenvalue, where a_i is the algebraic
    multiplicity. We test every choice and keep the smallest degree that really
    annihilates A. The exponent that survives is the size of the largest Jordan
    block at that eigenvalue.
    """
    n = len(A)
    p = charpoly(A)
    roots = real_roots_by_deflation(p)
    if len(roots) != len(p) - 1:
        return poly_trim(p), roots            # complex roots: not handled here

    groups = []
    for r in roots:
        for g in groups:
            if abs(r - g[0]) < 1e-6:
                g.append(r)
                break
        else:
            groups.append([r])

    def annihilates(coeffs):
        M = poly_horner_matrix(coeffs, A)
        return all(abs(M[i][j]) < 1e-8 for i in range(n) for j in range(n))

    best = None
    def search(i, chosen, degree):
        nonlocal best
        if best is not None and degree >= best[0]:
            return
        if i == len(groups):
            if annihilates(chosen):
                best = (degree, list(poly_trim(chosen)))
            return
        centre = sum(groups[i]) / len(groups[i])
        for e in range(0, len(groups[i]) + 1):
            m = chosen
            for _ in range(e):
                m = poly_mul(m, [1.0, -centre])
            search(i + 1, m, degree + e)
    search(0, [1.0], 0)
    return (best[1] if best else poly_trim(p)), roots

cases = {
    "A: eigenvalues 4, 3, 2":        A,
    "A^2 = A (a projector)":         [[1.0, 0.0], [0.0, 0.0]],
    "2x2 Jordan block, eigenvalue 2": [[2.0, 1.0], [0.0, 2.0]],
    "the 2x2 identity":              [[1.0, 0.0], [0.0, 1.0]],
    "a rotation, eigenvalues +-i":   [[0.0, -1.0], [1.0, 0.0]],
    "diag(1,1,1)":                   [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
}
for name, M in cases.items():
    cp = charpoly(M)
    mp, _ = minimal_poly(M)
    print(f"   {name}")
    print(f"      characteristic, degree {len(cp) - 1}: {poly_str(cp)}")
    print(f"      minimal,        degree {len(mp) - 1}: {poly_str(mp)}")
print()
print("Same roots, different degrees. The degree of the minimal polynomial is")
print("the size of the LARGEST Jordan block, not the number of eigenvalues.")
print("The identity matrix has minimal polynomial L - 1: it behaves exactly")
print("like the number 1, and knowing that means exp(A) is just e^1 with no")
print("matrix work at all. A lower-degree minimal polynomial means fewer")
print("matrix powers for any function you want to evaluate.")
```

Diagonalization, and when it fails:

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

def norm2(v):
    return math.sqrt(sum(x * x for x in v))

def dot(u, v):
    return sum(a * b for a, b in zip(u, v))

def trace(A):
    return sum(A[i][i] for i in range(len(A)))

def det(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    t = 0.0
    for j in range(n):
        t += ((-1) ** j) * A[0][j] * det([r[:j] + r[j + 1:] for r in A[1:]])
    return t

def print_matrix(A, title=""):
    if title:
        print(title)
    for row in A:
        print("   " + "".join(f"{v:9.4f}" for v in row))
    print()

def inverse(A):
    n = len(A)
    M = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(A)]
    for c in range(n):
        piv = next((r for r in range(c, n) if abs(M[r][c]) > 1e-12), None)
        if piv is None:
            raise ValueError("matrix is singular")
        M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]
        M[c] = [x / pv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0.0:
                f = M[r][c]
                M[r] = [M[r][j] - f * M[c][j] for j in range(2 * n)]
    return [row[n:] for row in M]

def null_space(A, tol=1e-9):
    n = len(A)
    m = [row[:] for row in A]
    rows, r, pivots = len(m), 0, []
    for c in range(n):
        piv = next((i for i in range(r, rows) if abs(m[i][c]) > tol), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        pv = m[r][c]
        m[r] = [x / pv for x in m[r]]
        for i in range(rows):
            if i != r and abs(m[i][c]) > tol:
                f = m[i][c]
                m[i] = [m[i][j] - f * m[r][j] for j in range(n)]
        pivots.append(c)
        r += 1
        if r == rows:
            break
    basis = []
    for fc in [c for c in range(n) if c not in pivots]:
        vec = [0.0] * n
        vec[fc] = 1.0
        for i, pc in enumerate(pivots):
            vec[pc] = -m[i][fc]
        basis.append(vec)
    return basis

def charpoly(A):
    n = len(A)
    c = [1.0]
    M = identity(n)
    for k in range(1, n + 1):
        M = matmul(A, M)
        c.append(-trace(M) / k)
        for i in range(n):
            M[i][i] += c[k]
    return c

def eigenvalues(A):
    """Bisection + deflation for the real roots, then Durand-Kerner for any
    complex ones left over."""
    from math import prod
    c = [float(x) for x in charpoly(A)]

    def peval(q, x):
        a = 0.0
        for k in q:
            a = a * x + k
        return a

    def pevalc(q, z):
        a = 0j
        for k in q:
            a = a * z + k
        return a

    def trim(q):
        q = list(q)
        while len(q) > 1 and abs(q[-1]) < 1e-11 * max(abs(x) for x in q):
            q.pop()
        return q

    def divide(a, b):
        a, b = list(a), list(b)
        q = [0.0] * max(1, len(a) - len(b) + 1)
        while len(a) >= len(b) and len(a) >= 1 and abs(a[-1]) > 1e-13:
            f = a[-1] / b[-1]
            d = len(a) - len(b)
            q[d] += f
            for i, coef in enumerate(b):
                a[d + i] -= f * coef
            a = trim(a)
        return trim(q)

    reals = []
    rest = trim(c)
    while len(rest) > 1:
        b = 1.0 + max(abs(x) for x in rest[1:]) / abs(rest[0])
        tol = 1e-12 * max(abs(x) for x in rest)
        grid, step = 4000, 2 * b / 4000
        found = None
        yp = peval(rest, -b)
        for i in range(1, grid + 1):
            x = -b + i * step
            y = peval(rest, x)
            if abs(y) <= tol:                 # root sits on a grid point
                found = x
                break
            if yp * y < 0:                    # sign change: bisect
                lo, hi = x - step, x
                flo = peval(rest, lo)
                for _ in range(200):
                    mid = 0.5 * (lo + hi)
                    if flo * peval(rest, mid) <= 0:
                        hi = mid
                    else:
                        lo, flo = mid, peval(rest, mid)
                found = 0.5 * (lo + hi)
                break
            yp = y
        if found is None:
            break
        reals.append(found)
        rest = divide(rest, [1.0, -found])

    if len(rest) > 1:
        cr = [complex(x) for x in rest]
        roots = [complex(0.4, 0.9) ** (k + 1) for k in range(len(cr) - 1)]
        for _ in range(200):
            roots = [z - pevalc(cr, z) / prod(z - w for j, w in enumerate(roots) if j != i)
                     for i, z in enumerate(roots)]
        reals = reals + roots
    return sorted(reals, key=lambda z: (-z.real, -z.imag))

def try_diagonalize(A):
    """Return (V, D) with A = V D V^-1, or (None, None) if impossible."""
    n = len(A)
    vals = eigenvalues(A)
    if any(abs(z.imag) > 1e-7 for z in vals):
        return None, None, vals
    vectors = []
    for z in vals:
        lam = z.real
        shifted = [[A[i][j] - (lam if i == j else 0.0) for j in range(n)]
                   for i in range(n)]
        vectors.extend(null_space(shifted))
    if len(vectors) != n:
        return None, None, vals          # defective: too few eigenvectors
    V = transpose(vectors)
    if abs(det(V)) < 1e-9:
        return None, None, vals
    D = [[0.0] * n for _ in range(n)]
    for i, z in enumerate(vals):
        D[i][i] = z.real
    return V, D, vals

# ---------- 1. a matrix that diagonalises ----------

A = [[4.0, 1.0, 2.0],
     [1.0, 3.0, 0.0],
     [2.0, 0.0, 2.0]]

print("=== 1. a matrix that diagonalises ===")
print_matrix(A, "A =")
V, D, vals = try_diagonalize(A)
print("eigenvalues:", [f"{z.real:+.6f}" for z in vals])
print_matrix(V, "V (columns are eigenvectors):")
print_matrix(D, "D (diagonal):")
Vinv = inverse(V)
print("Check A = V D V^-1 :")
recovered = matmul(V, matmul(D, Vinv))
print_matrix(recovered)
print("matches A to 1e-9:", all(abs(recovered[i][j] - A[i][j]) < 1e-9
                                for i in range(3) for j in range(3)))
print()
print("Why this matters: powers of A become trivial.")
print("   A^k = V D^k V^-1, and D^k just raises each diagonal entry to k.")
for k in (1, 2, 5):
    Dk = [[D[i][j] ** k for j in range(3)] for i in range(3)]
    Ak = matmul(V, matmul(Dk, Vinv))
    # verify against repeated multiplication
    direct = identity(3)
    for _ in range(k):
        direct = matmul(direct, A)
    ok = all(abs(Ak[i][j] - direct[i][j]) < 1e-8 for i in range(3) for j in range(3))
    print(f"   k={k}: A^k via V D^k V^-1 == A^k by repeated multiplication: {ok}")
print("That is why diagonalisation matters for matrix exponentials, Markov")
print("chain limits, and repeated applications of an operator.")

# ---------- 2. a matrix that does not ----------

print()
print("=== 2. a matrix that REFUSES to diagonalise ===")
B = [[2.0, 1.0, 0.0], [0.0, 2.0, 1.0], [0.0, 0.0, 2.0]]
print_matrix(B, "B = a 3x3 Jordan block (triangular, so eigenvalues = diagonal):")
vals_B = eigenvalues(B)
print("eigenvalues found numerically:", [f"{z.real:+.6f}" for z in vals_B])
print("   -> all 2, agreeing to 1e-5. A root of multiplicity 3 can only be")
print("      located to about eps^(1/3), so this is a real limit of root")
print("      finding, not a bug. Being triangular tells us the answer")
print("      exactly: 2, 2, 2.")
basis = null_space([[B[i][j] - (2.0 if i == j else 0.0) for j in range(3)]
                     for i in range(3)])
print(f"dim ker(B - 2I) = {len(basis)}, but we need 3 eigenvectors.")
print("One eigenvalue, algebraic multiplicity 3, geometric multiplicity 1.")
print("B has only ONE eigenvector direction, so V would have 3 identical")
print("columns and det(V) = 0. No inverse, so no diagonal form exists.")
print()
print("Compare with the DIAGONAL matrix with the same eigenvalues:")
D3 = [[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]
print(f"   dim ker(D3 - 2I) = {len(null_space([[D3[i][j] - (2.0 if i==j else 0.0) for j in range(3)] for i in range(3)]))}")
print("Three. Same eigenvalues, wildly different behaviour.")
print()
print("Both satisfy Cayley-Hamilton, both have trace 6 and det 8, and both")
print("have the same characteristic polynomial (L-2)^3. The eigenvalues")
print("simply do not contain enough information to reconstruct the matrix.")

# ---------- 3. the Jordan form workaround ----------

print()
print("=== 3. Jordan form: the 'as close as possible' answer ===")
print("Every matrix is similar to a Jordan form J: blocks of 1s on the")
print("superdiagonal, eigenvalue on the diagonal. B is already in Jordan form,")
print("which is the point -- it is the SIMPLEST matrix with these eigenvalues.")
print("For a general matrix you build each Jordan block by searching for")
print("generalised eigenvectors, chaining them so that")
print("   (B - 2I) v_k = v_{k-1}.")
print()
v1 = [0.0, 0.0, 1.0]      # the true eigenvector
v2 = [0.0, 1.0, 0.0]      # (B - 2I) v2 = v1
v3 = [1.0, 0.0, 0.0]      # (B - 2I) v3 = v2
print("The chain for eigenvalue 2:")
for name, v in (("v1", v1), ("v2", v2), ("v3", v3)):
    Bv = matvec(B, v)
    shifted = [round(Bv[i] - 2 * v[i], 12) for i in range(3)]
    print(f"   {name} = {v}   (B - 2I){name} = {shifted}")
print()
print("So (B-2I) v3 = v2, (B-2I) v2 = v1, and (B-2I) v1 = 0. That chain of")
print("length 3 IS the Jordan block. Only v1 is a real eigenvector; v2 and v3")
print("are 'generalised' ones. The chain length is exactly the information")
print("that the eigenvalues threw away.")
```

And the practical heart — symmetric, positive definite, Cholesky:

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

def trace(A):
    return sum(A[i][i] for i in range(len(A)))

def norm2(v):
    return math.sqrt(sum(x * x for x in v))

def dot(u, v):
    return sum(a * b for a, b in zip(u, v))

def det(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    t = 0.0
    for j in range(n):
        t += ((-1) ** j) * A[0][j] * det([r[:j] + r[j + 1:] for r in A[1:]])
    return t

def print_matrix(A, title=""):
    if title:
        print(title)
    for row in A:
        print("   " + "".join(f"{v:9.4f}" for v in row))
    print()

def inverse(A):
    n = len(A)
    M = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(A)]
    for c in range(n):
        piv = next((r for r in range(c, n) if abs(M[r][c]) > 1e-12), None)
        if piv is None:
            raise ValueError("singular")
        M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]
        M[c] = [x / pv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0.0:
                f = M[r][c]
                M[r] = [M[r][j] - f * M[c][j] for j in range(2 * n)]
    return [row[n:] for row in M]

def jacobi_eigh(A, tol=1e-13, max_sweeps=100):
    """Jacobi rotations: the textbook method, and the reason the symmetric
    spectral theorem is easy to prove rather than just assert."""
    n = len(A)
    a = [row[:] for row in A]
    Q = identity(n)
    for _ in range(max_sweeps):
        off = max(((abs(a[i][j]), i, j) for i in range(n) for j in range(n) if i != j),
                  default=(0.0, 0, 1))
        if off[0] < tol:
            break
        _, p, q = off
        theta = 0.5 * math.atan2(2 * a[p][q], a[q][q] - a[p][p])
        c, s = math.cos(theta), math.sin(theta)
        for k in range(n):
            akp, akq = a[k][p], a[k][q]
            a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
        for k in range(n):
            apk, aqk = a[p][k], a[q][k]
            a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
        for k in range(n):
            vkp, vkq = Q[k][p], Q[k][q]
            Q[k][p], Q[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    return [a[i][i] for i in range(n)], Q

# ---------- part 1: symmetric matrices diagonalise, always ----------

S = [[4.0, 1.0, 2.0],
     [1.0, 3.0, 0.0],
     [2.0, 0.0, 2.0]]

print("=== 1. a SYMMETRIC matrix ===")
print_matrix(S, "S (note S[i][j] == S[j][i]):")
print("Jacobi rotations diagonalise it exactly:")
vals, Q = jacobi_eigh(S)
print_matrix(Q, "   Q (orthonormal columns):")
QtQ = matmul(transpose(Q), Q)
print("   Q^T Q =")
print_matrix(QtQ)
print("   orthogonal?", all(abs(QtQ[i][j] - identity(3)[i][j]) < 1e-12
                            for i in range(3) for j in range(3)))
print()
print("   eigenvalues:", [f"{v:+.10f}" for v in vals])
print("   all real and all positive:", all(v > 0 for v in vals))
print()
D = [[0.0] * 3 for _ in range(3)]
for i, v in enumerate(vals):
    D[i][i] = v
print("   Q^T S Q = (should be diagonal, not a general inverse!):")
print_matrix(matmul(transpose(Q), matmul(S, Q)))
print("Because S is symmetric, the change of basis is ORTHOGONAL, so we do")
print("not need V^-1 at all -- the transpose does the job. That is the whole")
print("difference from a general matrix, and it is why eigendecomposition is")
print("numerically safe for symmetric matrices and why np.linalg.eigh exists.")
print()
print("Geometric reading: the eigenvectors of a symmetric matrix are mutually")
print("perpendicular, so there is no ambiguity about the basis at all.")
for i, v in enumerate(vals):
    e = [Q[r][i] for r in range(3)]
    print(f"   lambda = {v:+.6f}   direction "
          f"[{e[0]:+.4f}, {e[1]:+.4f}, {e[2]:+.4f}]   |e| = {norm2(e):.10f}")
dots = [(i, j, dot([Q[r][i] for r in range(3)], [Q[r][j] for r in range(3)]))
        for i in range(3) for j in range(3) if i < j]
print("   pairwise dots:", [f"{d:+.2e}" for _, _, d in dots])

# ---------- part 2: positive definiteness ----------

print()
print("=== 2. positive definite: what it means and how to test it ===")
def is_symmetric(A, tol=1e-12):
    n = len(A)
    return all(abs(A[i][j] - A[j][i]) < tol for i in range(n) for j in range(n))

def leading_minors(A):
    """The determinants of the top-left k x k blocks."""
    n = len(A)
    return [det([[A[i][j] for j in range(k)] for i in range(k)])
            for k in range(1, n + 1)]

def is_positive_definite(A):
    """Sylvester's criterion: symmetric and every leading minor positive."""
    return is_symmetric(A) and all(m > 1e-12 for m in leading_minors(A))

test_mats = {
    "S (the matrix above)": S,
    "the identity":         identity(3),
    "negative definite -S": [[-x for x in r] for r in S],
    "indefinite diag(1,-1)": [[1.0, 0, 0], [0, -1.0, 0], [0, 0, 1.0]],
    "singular [[1,1],[1,1]]": [[1.0, 1.0], [1.0, 1.0]],
    "non-symmetric":        [[1.0, 2.0], [3.0, 4.0]],
}
for name, M in test_mats.items():
    print(f"   {name:26s} symmetric={str(is_symmetric(M)):5s} "
          f"minors={[round(m, 4) for m in leading_minors(M)]} "
          f"positive definite={is_positive_definite(M)}")
print()
print("Positive definite means x^T A x > 0 for every nonzero x. The quadratic")
print("form has a single bowl-shaped minimum at the origin. That is why the")
print("minimum of x^T A x + b^T x exists and is unique, which is the whole")
print("reason least squares and maximum likelihood work so well: the loss")
print("surface is convex.")
print()
print("Check it directly by sampling x: x^T S x for various x")
for x in ([1.0, 0, 0], [0, 1.0, 0], [1.0, 1.0, 1.0], [-2.0, 3.0, 0.5]):
    print(f"   x = {str(x):16s}  x^T S x = {dot(x, matvec(S, x)):+.6f}")

# ---------- part 3: Cholesky ----------

print()
print("=== 3. Cholesky: A = L L^T for positive definite A ===")

def cholesky(A, tol=1e-12):
    """A = L L^T with L lower triangular. Works because A is symmetric and
    positive definite, and it is about three times faster and far better
    conditioned than forming A^2 then taking a square root."""
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                v = A[i][i] - s
                if v <= tol:
                    raise ValueError("not positive definite")
                L[i][j] = math.sqrt(v)
            else:
                L[i][j] = (A[i][j] - s) / L[j][j]
    return L

L = cholesky(S)
print_matrix(L, "L (lower triangular):")
Lt = transpose(L)
print("   L L^T =")
print_matrix(matmul(L, Lt))
print("   recovers S exactly:",
      all(abs(matmul(L, Lt)[i][j] - S[i][j]) < 1e-10 for i in range(3) for j in range(3)))
print()
print("Why Cholesky matters: solving a linear system with A = L L^T becomes")
print("TWO triangular solves, and triangular solves are back-substitution --")
print("no elimination, no pivoting, and rock solid numerically.")

def forward_substitution(L, b):
    """Solve L y = b for lower-triangular L."""
    n = len(L)
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(L[i][j] * y[j] for j in range(i))) / L[i][i]
    return y

def back_substitution(U, y):
    """Solve U x = y for upper-triangular U."""
    n = len(U)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
    return x

b = [1.0, 2.0, 3.0]
y = forward_substitution(L, b)
x = back_substitution(Lt, y)
Sinv = inverse(S)
x_direct = [sum(Sinv[i][j] * b[j] for j in range(3)) for i in range(3)]
print(f"   solving S x = b with b = {b}")
print(f"   via Cholesky (two triangular solves) = {[round(v, 10) for v in x]}")
print(f"   via a full inverse                   = {[round(v, 10) for v in x_direct]}")
print(f"   agree to 1e-9: {all(abs(p - q) < 1e-9 for p, q in zip(x, x_direct))}")
print()
print("Every positive definite matrix has a unique Cholesky factor with")
print("positive diagonal entries, which makes it a canonical choice: no")
print("ambiguity, unlike a general square root.")
try:
    cholesky([[1.0, 2.0], [3.0, 4.0]])
except ValueError as e:
    print()
    print("   a non-symmetric matrix has no Cholesky factor:", e)
print("   which is why every SPD routine checks symmetry first, and why")
print("   covariance matrices are always treated as symmetric -- even when")
print("   floating-point noise makes them very slightly asymmetric.")

# ---------- part 4: why covariance matrices are safe ----------

print()
print("=== 4. a covariance matrix is always symmetric positive definite ===")
data = [[1.2, 0.8], [2.9, 1.1], [4.5, 3.3], [5.1, 4.9], [7.8, 6.2]]
n = len(data)
k = 2
means = [sum(row[j] for row in data) / n for j in range(k)]
centered = [[row[j] - means[j] for j in range(k)] for row in data]
cov = [[sum(centered[t][i] * centered[t][j] for t in range(n)) / (n - 1)
        for j in range(k)] for i in range(k)]
print_matrix(cov, "covariance matrix of the data:")
print("   symmetric?", is_symmetric(cov))
print("   leading minors:", [round(m, 6) for m in leading_minors(cov)])
print("   positive definite?", is_positive_definite(cov))
vals, Q = jacobi_eigh(cov)
print("   eigenvalues:", [f"{v:+.6f}" for v in vals])
print("   all positive, so the data really does spread out along 2 dimensions")
print("   with no degenerate direction. That is what lets PCA work at all.")
Lc = cholesky(cov)
print("   Cholesky factor L exists too:")
print_matrix(Lc, "   ")
print("   This is why np.cov, sklearn's StandardScaler, and every Gaussian")
print("   model in statistics assume SPD. When it fails, the data is")
print("   collinear and the inverse covariance is meaningless.")
```

### With Libraries

```python
import numpy as np

np.set_printoptions(precision=6, suppress=True)

A = np.array([[4.0, 1.0, 2.0],
              [1.0, 3.0, 0.0],
              [2.0, 0.0, 2.0]])

print("--- one function does everything: numpy diagonalises it ---")
vals, V = np.linalg.eig(A)
print("eigenvalues:\n", vals)
print("V (columns are eigenvectors):\n", V)
print("V @ diag(vals) @ inv(V) == A :", np.allclose(V @ np.diag(vals) @ np.linalg.inv(V), A))

print("\n--- but for a SYMMETRIC matrix, use eigh ---")
S = A                              # this matrix happens to be symmetric
print("S is symmetric?", np.allclose(S, S.T))
w, Q = np.linalg.eigh(S)
print("eigh eigenvalues:\n", w)
print("eigh eigenvectors Q:\n", Q)
print("Q.T @ S @ Q =\n", Q.T @ S @ Q)
print("Q.T @ Q == I :", np.allclose(Q.T @ Q, np.eye(3)))
print()
print("Why eigh and not eig for symmetric matrices:")
print("  * the eigenvalues are guaranteed real and sorted ascending")
print("  * the eigenvectors are guaranteed orthonormal, so Q.T IS the inverse")
print("  * it is roughly 3x faster (it exploits the symmetry)")
print("  * it is far better conditioned")
print()
print("Proof sketch of the guarantee, from the lesson's code: for symmetric S")
print("we have (Su) . v = u . (Sv) = u . (lambda_u v) = lambda_u (u . v).")
print("So u.v = 0 whenever lambda_u != lambda_v: distinct eigenvalues of a")
print("symmetric matrix have PERPENDICULAR eigenvectors. For equal eigenvalues")
print("you can always pick an orthonormal basis of the eigenspace by")
print("Gram-Schmidt. Either way the eigenvectors come out orthonormal.")

print("\n--- powers of a symmetric matrix, the payoff ---")
for k in (1, 2, 10, 50):
    direct = np.linalg.matrix_power(S, k)
    fast = Q @ np.diag(w ** k) @ Q.T
    print(f"   k={k:3d}: Q diag(w^k) Q^T == S^k : {np.allclose(direct, fast)}")
print("Raising a diagonal matrix to a power is just raising its entries. So a")
print("1000th power costs one diagonal exponentiation instead of 1000 matrix")
print("multiplies. That is why eigendecomposition is the standard way to")
print("compute matrix exponentials and long-run Markov behaviour.")

print("\n--- symmetry is not automatic: eig and eigh see different matrices ---")
M = np.array([[2.0, -1.0],
              [1.0, 2.0]])                      # not symmetric
print("M =\n", M)
print("symmetric?", np.allclose(M, M.T))
print("np.linalg.eigvals(M)  ->", np.round(np.linalg.eigvals(M), 6),
      "  <- complex, as it must be")
Ms = (M + M.T) / 2
print("Symmetrise first: (M + M.T)/2 =\n", np.round(Ms, 6))
print("   np.linalg.eigvalsh ->", np.round(np.linalg.eigvalsh(Ms), 6), " all real")
print()
print("Here is the footgun, exactly. eigvalsh reads ONLY the lower triangle,")
print("so calling it on M itself silently returns the eigenvalues of")
print("   [[2, 1],      which is NOT M. Compare:")
lower_sym = np.tril(M) + np.tril(M, -1).T
print("   lower-triangle symmetrisation =\n", lower_sym)
print("   np.linalg.eigvalsh(M)      ->", np.round(np.linalg.eigvalsh(M), 6))
print("   eigenvalues of that matrix ->", np.round(np.linalg.eigvals(lower_sym), 6))
print("Identical. So eigvalsh on a non-symmetric matrix answers a question")
print("about a different matrix, without warning you.")
print()
print("Symmetrising with (M + M.T)/2 is what np.cov, sklearn, and every")
print("covariance routine do, because the true object is symmetric and only")
print("floating-point noise breaks it in practice.")

print("\n--- positive definiteness, in one call ---")
print("np.linalg.eigvalsh(S) :", np.round(np.linalg.eigvalsh(S), 6))
print("all eigenvalues > 0   :", bool(np.all(np.linalg.eigvalsh(S) > 0)))
print("That is the most direct test: SPD <=> symmetric and all eigenvalues > 0.")
print()
print("Sylvester's criterion (leading minors) is faster for small matrices:")
def leading_minors_det(M):
    return np.round([np.linalg.det(M[:k, :k]) for k in range(1, len(M) + 1)], 6)
print("   leading minors of S:", leading_minors_det(S))
try:
    np.linalg.cholesky(S)
    print("   np.linalg.cholesky(S) succeeded -> S is SPD")
except np.linalg.LinAlgError as e:
    print("   cholesky failed:", e)

print("\n--- Cholesky: numpy has it ---")
L = np.linalg.cholesky(S)
print("L =\n", L)
print("L @ L.T == S :", np.allclose(L @ L.T, S))
print("np.linalg.cholesky is the same algorithm we wrote by hand, about 30x")
print("faster than forming A^2 and calling sqrt on the result.")

print("\n--- Jordan form: numpy gives you the pieces ---")
J = np.array([[2.0, 1.0, 0.0],
              [0.0, 2.0, 1.0],
              [0.0, 0.0, 2.0]])
w4, V4 = np.linalg.eig(J)
print("eigenvalues of the Jordan block:", np.round(w4, 8))
print("rank(V4) =", np.linalg.matrix_rank(V4),
      " -- only 1, so J is defective and cannot be diagonalised")
print("np.linalg.matrix_rank is the one-line practical test: if the rank of")
print("the eigenvector matrix is less than n, the matrix is defective.")
print()
print("Jordan form itself is rarely computed numerically -- it is numerically")
print("DELICATE, because a tiny perturbation can split a Jordan block in two.")
print("Use scipy.linalg.schur, which gives a quasi-upper-triangular form that")
print("is numerically stable, or just avoid the whole question by using the SVD")
print("in the next lesson, which exists for every matrix.")
```

## Common Mistakes

**1. Using `np.linalg.eig` on a symmetric matrix.**

```python
import numpy as np

S = np.array([[4.0, 1.0], [1.0, 3.0]])
w, V = np.linalg.eig(S)               # WRONG function for a symmetric matrix
print("eig  ->", w, "\n", V)
print("Works, but slower and less accurate than it needs to be.")
```

```python
import numpy as np

S = np.array([[4.0, 1.0], [1.0, 3.0]])
w, V = np.linalg.eigh(S)              # RIGHT: 'h' is for Hermitian/symmetric
print("eigh ->", np.round(w, 10))
print("V.T @ V =\n", np.round(V.T @ V, 12))
print("Guaranteed real, guaranteed orthonormal, ~3x faster, better conditioned.")
print("'h' means Hermitian, which is the complex generalisation of symmetric.")
```

Tempting because `eig` is the one you learn first and it does give the right
answer. The symptom of the mistake is not a wrong number — it is a model that
is mysteriously 3× slower and loses precision on ill-conditioned data.

**2. Assuming every matrix diagonalises.**

```python
import numpy as np

J = np.array([[2.0, 1.0, 0.0], [0.0, 2.0, 1.0], [0.0, 0.0, 2.0]])
w, V = np.linalg.eig(J)
print("eigenvalues:", w)
print("V =\n", np.round(V, 6))
# WRONG: assuming V is invertible, or that V^-1 J V is diagonal
print("rank(V) =", np.linalg.matrix_rank(V), " -- not 3, so V^-1 does not exist")
```

```python
import numpy as np

J = np.array([[2.0, 1.0, 0.0], [0.0, 2.0, 1.0], [0.0, 0.0, 2.0]])
w, V = np.linalg.eig(J)
# RIGHT: always check the rank before assuming you can invert V
if np.linalg.matrix_rank(V) < V.shape[0]:
    print("defective: only", np.linalg.matrix_rank(V), "independent eigenvectors")
    print("no diagonal form exists -- use the SVD instead, which always exists")
else:
    print("diagonalisable:", np.allclose(V @ np.diag(w) @ np.linalg.inv(V), J))
print("In ML you almost never need to check: SVD handles every case.")
```

Tempting because most teaching examples are symmetric or have distinct
eigenvalues. The real-world version of this bug is computing
`V @ diag(w) @ inv(V)` and getting a matrix full of `nan` or garbage, with no
error message.

**3. Forgetting that `eigvalsh` silently ignores half the matrix.**

```python
import numpy as np

M = np.array([[2.0, -1.0], [1.0, 2.0]])      # NOT symmetric
print("WRONG: eigvalsh on a non-symmetric matrix")
print("eigvalsh(M) ->", np.linalg.eigvalsh(M), " <- no warning at all")
print("these are the eigenvalues of [[2,1],[1,2]], not of M")
```

```python
import numpy as np

M = np.array([[2.0, -1.0], [1.0, 2.0]])
# RIGHT: check symmetry yourself, or symmetrise first
if np.allclose(M, M.T):
    print("eigvalsh(M) ->", np.linalg.eigvalsh(M))
else:
    Ms = (M + M.T) / 2
    print("not symmetric; eigvals of M ->", np.linalg.eigvals(M))
    print("eigvals of (M+M.T)/2 ->", np.linalg.eigvalsh(Ms))
print("Always symmetrise a covariance-like matrix before using eigh.")
```

Tempting because the matrix "looks" fine and numpy raises nothing. This is
the worst kind of bug: a plausible number, silently answering a different
question.

**4. Assuming positive definiteness without checking.**

```python
import numpy as np

X = np.array([[1.0, 2.0], [2.0, 4.0]])       # collinear: the second is 2x the first
cov = np.cov(X, rowvar=False)
print("covariance:\n", np.round(cov, 6))
print("Its inverse is meaningless -- the data has no independent directions.")
try:
    print(np.linalg.inv(cov))
except np.linalg.LinAlgError as e:
    print("LinAlgError:", e)
```

```python
import numpy as np

X = np.array([[1.0, 2.0], [2.0, 4.0]])
cov = np.cov(X, rowvar=False)
# RIGHT: check first, and add a ridge term if you must invert anyway
w = np.linalg.eigvalsh(cov)
print("eigenvalues:", np.round(w, 8), " -> smallest is ~0, so NOT positive definite")
print("condition number:", f"{np.linalg.cond(cov):.3e}")
safe = cov + 1e-6 * np.eye(2)
print("with a 1e-6 ridge, it inverts fine:\n", np.round(np.linalg.inv(safe), 4))
print("That ridge is exactly the regularisation from lesson 38.")
```

Tempting because "covariance matrices are always positive definite" is
almost always true and so becomes an assumption. It fails exactly when you
have collinear features, which is precisely when you need to know.

**5. Expecting Jordan form to be numerically robust.**

Jordan form is mathematically complete and numerically fragile. A Jordan block
is an unstable object: perturb the matrix by `1e-16` and a size-3 block can
split into three size-1 blocks, changing the computed answer completely. The
eigenvalues are continuous in the matrix; the Jordan structure is not. Use
`np.linalg.svd` (next lesson) or `scipy.linalg.schur` if you need this, and in
practice the only thing you usually want from Jordan form — the eigenvalue
multiplicities — you should get from `np.linalg.eigvals` and count.

## Formula Sheet

Symbols follow [SYMBOLS.md](../SYMBOLS.md). `A` is `n × n` over `ℝ` or `ℂ`,
`V` is `n × n` invertible, `D` is diagonal, `Q` orthogonal, `p_A(λ) =
det(λI − A) = λⁿ + c_{n−1}λ^{n−1} + ⋯ + c₀`.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| diagonalisable | `$A = VDV^{-1}$, equivalently `$V^{-1}AV = D$` | there is a change of coordinates in which `A` only scales axes | deciding whether you can work with `D` instead of `A`; needs `V` invertible, hence `A` of full rank |
| similarity | `$V^{-1}AV$` | same linear map, different basis | the only transformation that preserves eigenvalues — congruence `PᵀAP` does not |
| defective | `$A$ is defective if no such `V$` exists | not enough independent eigenvectors | when `np.linalg.matrix_rank(V) < n` |
| matrix power | `$A^k = V D^k V^{-1}$` | to raise a matrix to a power, raise its eigenvalues instead | `O(n³)` instead of `O(n³ log k)`; Markov limits, Kalman filters |
| Cayley–Hamilton | `$A^n + c_{n-1}A^{n-1} + \cdots + c_1A + c_0I = 0$ | every square matrix satisfies a polynomial equation of degree `n` | evaluating `f(A)` in at most `n` multiplies, including `e^A` |
| Horner evaluation | `$f(A) = \bigl(\bigl(c_0 A + c_1\bigr)A + c_2\bigr)A + \cdots$` | multiply-and-add, never forming `A²`, `A³`, … separately | the only sane order for Cayley–Hamilton; avoids huge intermediates |
| minimal polynomial | `$m_A(A) = 0$ with `m_A` monic of least degree | the shortest polynomial relation that kills `A` | bounding the cost of `f(A)`; `deg m_A` = largest Jordan block |
| divides | `$m_A$ divides `$p_A$` and they share roots | the minimal relation is a factor of the characteristic one | finding `m_A` by testing divisors of `p_A` |
| eigenvector | `$Au = \lambda u$ | a direction `A` only scales | the columns of `V` |
| spectral theorem | `$A$ real symmetric `$\Rightarrow$` `A = QDQ^{\mathsf T}` with `$Q^{\mathsf T}Q = I$` and `D` real | symmetric matrices get an orthogonal, real change of basis | every symmetric computation: `np.linalg.eigh`, PCA, Hessians, covariance |
| eigenvector orthogonality proof | `$Au=\lambda u$, $Av=\mu v$, `$A=A^{\mathsf T}$ $\Rightarrow (\lambda-\mu)(u^{\mathsf T}v) = 0$` | distinct eigenvalues of a symmetric matrix give perpendicular directions | why the eigenbasis is *orthonormal* and not merely orthogonal |
| positive definite | `$x^{\mathsf T}Ax > 0$ for all `$x \ne 0$` | the quadratic form `xᵀAx` has a single bowl minimum at 0 | convexity, unique optima, `L = LLᵀ` existing |
| PSD | `$x^{\mathsf T}Ax \ge 0$ for all `x` | the same, but flat directions allowed | Gram and covariance matrices; **PSD requires a symmetric matrix** |
| eigenvalue test for PD | `$A$ symmetric PD `$\iff$` every `λ_i > 0$` | positivity lives in the spectrum | the cheapest test once you have the eigenvalues |
| quadratic form in the eigenbasis | `$x^{\mathsf T}Ax = \sum_i \lambda_i c_i^2$ | a weighted sum of squares | proves the two tests above agree |
| Sylvester's criterion | `$A$ symmetric PD `$\iff$` every leading principal minor `$\Delta_k > 0$` | the top-left `k×k` determinants are all positive | a cheap PD test that avoids computing eigenvalues; basis of Cholesky |
| Cholesky | `$A = LL^{\mathsf T}$`, `L` lower triangular with positive diagonal | factor `A` into two triangular halves | solving `Ax = b` as two back-substitutions; also a PD test that *raises* on failure |
| Cholesky solve | `$Ax=b$ `$\Rightarrow$` solve `$Ly=b$`, then `$L^{\mathsf T}x=y$` | two triangular solves, no elimination | numerically far safer than forming `A⁻¹` |
| uniqueness of Cholesky | `L` with positive diagonal is unique | a canonical square root | contrast with a general matrix square root, which has sign ambiguity |
| Jordan block | `$J_\lambda$ = λ on the diagonal, 1s on the superdiagonal | the smallest matrix with eigenvalue λ that is not diagonal | the irreducible piece left over when diagonalisation fails |
| Jordan form | `$J = V^{-1}AV$` block-diagonal in Jordan blocks | the simplest matrix with the same eigenvalues | theory; **numerically delicate**, prefer `scipy.linalg.schur` or the SVD |
| generalised eigenvector chain | `$(A-\lambda I)v_k = v_{k-1}`, with `$(A-\lambda I)v_1 = 0$ | a ladder of vectors feeding into the true eigenvector | the extra structure that `B = [[2,1],[0,2]]` carries and `2I` does not |
| trace identity | `$\operatorname{tr}(A^k) = \sum_i \lambda_i^k$ | the diagonal sum of a power equals the sum of powered eigenvalues | checking a spectrum for free — no extra matrix powers |
| condition number of an SPD matrix | `$\text{cond}(A) = \sigma_{\max}/\sigma_{\min} = \lambda_{\max}/\lambda_{\min}$` | for SPD the singular values *are* the eigenvalues | detecting collinear features; on the lesson's `S`, `cond = 8.6588` |
| `eigh` guarantee | `QᵀQ = I` and real `w`, ascending | symmetric/Hermitian input gets real, sorted, orthogonal output | the reason `np.linalg.eigh` beats `eig` on symmetric input |

Three restrictions. The spectral theorem needs **real symmetric** input — with
complex entries the word is *Hermitian* (`A = A*`), and with neither, nothing is
guaranteed. Positive definiteness and Sylvester's criterion both require symmetry
as well; `[[1,2],[3,4]]` is neither, so neither test applies. And
`np.linalg.eigvalsh` reads only the lower triangle, so calling it on a
non-symmetric matrix silently returns the eigenvalues of a *different* matrix.

## Multiple Choice Questions

**Q1.** A matrix `A` has an eigenvalue `λ` of algebraic multiplicity 3 and
geometric multiplicity 1. What follows?

- A) `A` is diagonalisable, because `λ` appears three times in the spectrum
- B) `A` is defective: there is only one independent eigenvector direction, so no
  invertible `V` can collect three
- C) `A` has no eigenvalues, because the multiplicities are inconsistent
- D) `A` is diagonalisable but only over the complex numbers

<details>
<summary>Answer and explanation</summary>

**B) `A` is defective: there is only one independent eigenvector direction, so no
invertible `V` can collect three.**

Diagonalisability is the *pointwise* criterion `dim E_λ = mult_alg(λ)` for every
`λ`. Here `1 ≠ 3`, so it fails. Any candidate `V` would need three columns, all
from `E_λ`, which is one-dimensional — so `V` would have rank 1, `det(V) = 0`,
and `V⁻¹` would not exist. `[[2,1],[0,2]]` and the 3×3 Jordan block in the lesson's
code are exactly this.

A is the confusion the whole lesson exists to kill: algebraic multiplicity counts
copies in the characteristic polynomial, which says nothing about how many
directions you can build. C is wrong — the eigenvalues are perfectly well defined;
`p_A(λ) = 0` is unaffected by multiplicities. D is the same error as A with an
extra step: over `ℂ` a matrix with `n` roots still fails to diagonalise if they
are not *independent directions*. That is precisely what Exercise 2 of this
lesson demonstrates on `[[1,1,0],[0,1,1],[0,0,1]]`.

</details>

**Q2.** Which statement must be true of every real symmetric matrix `A`?

- A) All its eigenvalues are distinct
- B) All its eigenvalues are real, and `A = QDQᵀ` with `Q` orthogonal
- C) It is positive definite
- D) Its eigenvalues are its diagonal entries

<details>
<summary>Answer and explanation</summary>

**B) All its eigenvalues are real, and `A = QDQᵀ` with `Q` orthogonal.**

That is the spectral theorem, and the `Q` being orthogonal is the valuable half:
`Q⁻¹ = Qᵀ`, so the change of basis is free and numerically stable. It is why
`np.linalg.eigh` exists and beats `eig` on this input.

A is false: `diag(2,3,3)` is symmetric and repeats 3. C is false:
`diag(1,−1)` is symmetric and indefinite; symmetry is unrelated to sign. D is
false: the tridiagonal `[[2,1,0],[1,2,1],[0,1,2]]` is symmetric with eigenvalues
`2−√2, 2, 2+√2`, while its diagonal reads `2, 2, 2` — the eigenvalues coincide
with the diagonal only when the matrix is *also* triangular.

</details>

**Q3.** Why is `np.linalg.eigh` preferred over `np.linalg.eig` for a symmetric
matrix, given that both return the right eigenvalues?

- A) `eigh` uses a different rounding mode
- B) `eigh` exploits symmetry to return real, orthonormal, sorted output, and
  makes `QᵀQ = I` exact rather than approximate
- C) `eig` cannot handle symmetric matrices at all
- D) `eigh` returns the singular values instead

<details>
<summary>Answer and explanation</summary>

**B) `eigh` exploits symmetry to return real, orthonormal, sorted output, and
makes `QᵀQ = I` exact rather than approximate.**

The lesson's code prints `Q.T @ S @ Q` as diagonal to machine precision and
`Q.T @ Q == I` as `True`. Because `Q` is orthogonal, `Q⁻¹ = Qᵀ`, so `S = QDQᵀ`
needs no matrix inverse — the whole numerically dangerous step in diagonalisation
disappears. `eigh` is also roughly 3× faster, since a symmetric matrix carries
half the information.

A is wrong — both use the same IEEE 754 double. C is wrong — `eig` works fine,
it just returns complex numbers in general and does not guarantee orthogonality;
the lesson's Common Mistake 1 shows it succeeding, only slowly and less accurately.
D is wrong — `eigh` returns eigenvalues. It is `np.linalg.svd` that returns
singular values, and [40](../part03_linear_algebra/40_svd_and_pca.md) covers why those are different.

</details>

**Q4.** Cayley–Hamilton says `p_A(A) = 0`. What is the practical consequence for
computing `e^A`?

- A) `e^A` cannot be computed by any closed form, because `A` is not a number
- B) Reducing `e^A` modulo `p_A` gives a polynomial in `A` of degree at most `n−1`,
  so `n` matrix multiplies replace an infinite series
- C) `e^A = e·A`, because `p_A` has a root at 1
- D) `e^A` is always the identity matrix

<details>
<summary>Answer and explanation</summary>

**B) Reducing `e^A` modulo `p_A` gives a polynomial in `A` of degree at most
`n−1`, so `n` matrix multiplies replace an infinite series.**

Any power `Aᵏ` with `k ≥ n` can be rewritten using `Aⁿ = −c_{n−1}A^{n−1} − ⋯ −
c₀I`, so every term of the exponential series collapses onto a combination of
`I, A, …, A^{n−1}`. The coefficients come from the polynomial remainder of `eˣ`
modulo `p_A(x)`. For the lesson's `S`, that remainder is
`e^S = 27.173235·I − 50.065741·S + 16.405785·S²`, which reproduces
`scipy.linalg.expm(S)` exactly.

A is wrong because the identity is exactly what makes it a *number*-like object.
C and D are the two degenerate extremes: `A` is not the identity and 1 need not
even be an eigenvalue. For the 2×2 identity matrix `I₂`, `p_A = (λ−1)²` so the
remainder of `eˣ` is `e` itself, giving `e^{I₂} = eI₂` — which is why the
lesson says `f(λI) = f(λ)I`.

</details>

**Q5.** Which claim about the condition number of a symmetric positive definite
matrix is correct?

- A) `cond(A) = 1` always, because symmetric matrices are well behaved
- B) `cond(A) = λ_max/λ_min`, so a tiny smallest eigenvalue means a huge condition
  number
- C) `cond(A) = tr(A)/det(A)`
- D) `cond(A)` is undefined for SPD matrices

<details>
<summary>Answer and explanation</summary>

**B) `cond(A) = λ_max/λ_min`, so a tiny smallest eigenvalue means a huge condition
number.**

For SPD `A` the singular values are the eigenvalues (all positive, no
cancellation), so `cond = σ_max/σ_min = λ_max/λ_min` exactly. On the lesson's `S`,
`cond = 5.528918/0.638531 = 8.6588`. Take the symmetric matrix
`[[1, 0.999999], [0.999999, 0.999999]]`: eigenvalues `0.0000005` and
`1.9999985`, and `cond ≈ 4 × 10⁶`. Every linear solve against it loses about six
digits.

A is a real conflation of "symmetric" with "perfectly conditioned" —
orthogonality of the *eigenvectors* is guaranteed, not smallness of the spread in
the *eigenvalues*. C is not a formula for anything. D is false; `np.linalg.cond`
handles SPD input and is exactly what you should call.

</details>

**Q6.** A matrix `A` is symmetric but *not* positive definite. What must be true?

- A) It has a zero eigenvalue
- B) It has a negative eigenvalue (or, if singular, a zero one)
- C) It cannot be diagonalised
- D) Its Cholesky factor `L` exists but with some negative diagonal entries

<details>
<summary>Answer and explanation</summary>

**B) It has a negative eigenvalue (or, if singular, a zero one).**

By the spectral theorem, `A = QDQᵀ` with real `D`, so
`xᵀAx = Σ λᵢcᵢ²` for the coordinates `c` of `x`. If some `λᵢ < 0` then choosing
`x` along that eigenvector gives `xᵀAx < 0`. Positive definiteness is exactly "all
eigenvalues positive", so failing it means at least one is `≤ 0`. The lesson
prints exactly this: `diag(1,−1,1)` is symmetric with eigenvalues
`1, −1, 1`, and `−S` is symmetric negative definite.

A is only the singular case, and it is one of two — `diag(1,−1)` is singular?
No, it has no zero eigenvalue at all. C is false: symmetry is precisely the
hypothesis that *guarantees* diagonalisability, so a symmetric matrix always has
an orthonormal eigenbasis whatever its signs. D is false because the Cholesky
factor is defined only for positive definite matrices: `np.linalg.cholesky`
raises `LinAlgError: Matrix is not positive definite`, which is exactly the
lesson's second positive-definiteness test.

</details>

**Q7.** You call `np.linalg.eigvalsh(M)` on `M = [[2, −1], [1, 2]]`, which is not
symmetric. What do you get?

- A) An error, because the function checks its input
- B) The eigenvalues of `M`, correctly computed
- C) The eigenvalues of `[[2, 1], [1, 2]]` — a different matrix — with no warning
- D) Complex numbers, because the matrix is not symmetric

<details>
<summary>Answer and explanation</summary>

**C) The eigenvalues of `[[2, 1], [1, 2]]` — a different matrix — with no
warning.**

`eigvalsh` reads only the **lower** triangle of its input and treats the upper
triangle as a mirror. So it diagonalises `tril(M) + tril(M,−1).T = [[2,1],[1,2]]`
and returns `1` and `3`. The lesson's code verifies this identity explicitly:
`np.linalg.eigvalsh(M)` equals `np.linalg.eigvals(lower_sym)` exactly.

This is Common Mistake 3 and the lesson calls it the worst kind of bug: a
plausible number silently answering a different question. D is wrong — the real
eigenvalues of `M` *are* complex (`2 ± i`), which is what `np.linalg.eigvals(M)`
reports, so the answer is available if you ask the right function. B is wrong
because you get `1, 3` rather than `2 ± i`. The defence is to check
`np.allclose(M, M.T)` yourself or to symmetrise with `(M + M.T)/2` first, which
is what every covariance routine does.

</details>

**Q8.** A symmetric matrix `S` has eigenvalues `0.6385, 2.8326, 5.5289`. Which
statement about `S¹⁰` is guaranteed?

- A) `‖S¹⁰‖ = 0.6385¹⁰`
- B) `tr(S¹⁰) = 0.6385¹⁰ + 2.8326¹⁰ + 5.5289¹⁰ = 26726499`, and the eigenvalues of
  `S¹⁰` are exactly those three numbers raised to the tenth power
- C) `S¹⁰` is symmetric, positive definite and diagonal
- D) `det(S¹⁰) = 0.6385 · 2.8326 · 5.5289`, unchanged from `det(S)`

<details>
<summary>Answer and explanation</summary>

**B) `tr(S¹⁰) = 0.6385¹⁰ + 2.8326¹⁰ + 5.5289¹⁰ = 26726499`, and the eigenvalues of
`S¹⁰` are exactly those three numbers raised to the tenth power.**

The lesson prints `tr(S^k) = Σ λᵢ^k` as a free check for every `k` — and at
`k = 10` it reads `26726499`, matching the trace of the actual matrix power
exactly. The eigenvalues are `0.0113`, `33248.885` and `26693250.104`, so the
tenth power is utterly dominated by the largest eigenvalue.

A picks the *smallest* eigenvalue and conflates the spectral norm with the
spectrum; `‖S¹⁰‖₂ = σ_max = 5.5289¹⁰ ≈ 2.67 × 10⁷`. C is a classic confusion:
`S¹⁰ = Q D¹⁰ Qᵀ` is symmetric and positive definite, but it is diagonal *only in
the eigenbasis*, not in the original coordinates. D is false — `det(S¹⁰) =
det(S)¹⁰ = 10¹⁰`, not `10`.

</details>

**Q9.** Why does `np.linalg.cholesky` fail on some symmetric matrices, and why is
that useful rather than annoying?

- A) It is a bug in the routine; every symmetric matrix has a Cholesky factor
- B) It exists only for positive definite matrices, so the failure is a positive
  definiteness test — and a positive definite matrix is one for which a linear
  solve has a unique solution
- C) Cholesky requires the matrix to be diagonal
- D) Cholesky fails for non-square matrices only

<details>
<summary>Answer and explanation</summary>

**B) It exists only for positive definite matrices, so the failure is a positive
definiteness test — and a positive definite matrix is one for which a linear
solve has a unique solution.**

`np.linalg.cholesky([[1,1],[1,1]])` raises `LinAlgError: Matrix is not positive
definite`, correctly: that matrix is singular (`det = 0`) so no `L` with `LLᵀ = M`
exists. Since Sylvester's criterion is the algorithm running under the hood,
Cholesky is simultaneously a factorisation *and* a yes/no test that costs about a
third of a general square root.

A is false: `[[1,1],[1,1]]` has no `L` at all, and the routine is right.
C is false — `L` is triangular with a full diagonal, and `S` in the lesson is a
dense symmetric matrix that factors fine. D is irrelevant: it is only defined for
square input, and the failure in question is about definiteness.

</details>

**Q10.** Why does `eigvalsh` beat `eig` for symmetric input even though both give
the correct eigenvalues?

- A) `eigvalsh` uses arbitrary precision
- B) `eigvalsh` guarantees a real orthonormal basis with `QᵀQ = I`, so `A = QDQᵀ`
  needs no inverse; `eig` only guarantees independence, forcing a `V⁻¹` that can
  be badly conditioned
- C) `eig` does not work on matrices with repeated eigenvalues
- D) `eigvalsh` sorts the eigenvalues descending, which `eig` does not

<details>
<summary>Answer and explanation</summary>

**B) `eigvalsh` guarantees a real orthonormal basis with `QᵀQ = I`, so `A = QDQᵀ`
needs no inverse; `eig` only guarantees independence, forcing a `V⁻¹` that can be
badly conditioned.**

This is not a small difference. `V⁻¹` computed by Gaussian elimination on a
matrix with near-parallel columns is where precision dies — the same phenomenon
that makes the normal equations of
[38](../part03_linear_algebra/38_orthogonality_and_least_squares.md) square the condition number.
Orthogonality removes that step entirely: `Q⁻¹ = Qᵀ` is a reshape, exact, and
`cond(Q) = 1`.

A is false — both use double precision. C is false — `eig` handles repeated
eigenvalues and returns a nearly-singular `V` for defective matrices, which is
why the lesson says to check `np.linalg.matrix_rank(V) < n`. D is backwards:
`eigh` sorts **ascending**, which the lesson's code prints and which is why
`w[-1]` is the largest eigenvalue and `w[0]` the smallest.

</details>

## Subjective Questions

### Short Answer

**Q1. State the definition of diagonalisable, and the equivalent eigenvector
form.**

<details>
<summary>Model answer</summary>

`A` is **diagonalisable** if there exist an invertible `V` and a diagonal `D`
with

    A = V D V^-1        equivalently        V^-1 A V = D

The similarity `V⁻¹AV` means "change basis by `V`, do the work, change back".
Diagonalisable means there *is* a basis in which `A` does nothing but scale each
axis independently — the columns of `V` are the eigenvectors and the diagonal of
`D` is the eigenvalues.

The equivalent form, from [36](../part03_linear_algebra/36_eigenvalues_and_eigenvectors.md): `A` is
diagonalisable iff `dim E_λ = mult_alg(λ)` for every eigenvalue `λ`, iff it has
`n` linearly independent eigenvectors, iff a basis of
[34](../part03_linear_algebra/34_basis_dimension_rank.md) consists entirely of eigenvectors. A matrix that
fails is **defective**.

</details>

**Q2. State Cayley–Hamilton and explain why it makes `f(A)` cheap to compute.**

<details>
<summary>Model answer</summary>

**Cayley–Hamilton.** Every `n × n` matrix satisfies its own characteristic
polynomial:

    A^n + c_{n-1}A^{n-1} + ... + c_1 A + c_0 I = 0

**Why it matters.** The identity rewrites `Aⁿ` in terms of lower powers, so by
induction every `Aᵏ` with `k ≥ n` is a linear combination of
`I, A, ..., A^{n−1}`. Any function `f` — including the infinite series
`e^A = Σ Aᵏ/k!` — therefore reduces to a polynomial of degree at most `n − 1` in
`A`.

So instead of an infinite series you compute `f(A)` by evaluating the polynomial
remainder of `f(x)` modulo `p_A(x)` at `A`, using Horner's rule to avoid forming
large intermediate powers. For an `n × n` matrix that is `n` multiplies. For the
lesson's `S`, `e^S = 27.173235·I − 50.065741·S + 16.405785·S²`, which reproduces
`expm(S)` exactly.

</details>

**Q3. What is the minimal polynomial, and how does its degree relate to the Jordan
blocks?**

<details>
<summary>Model answer</summary>

The **minimal polynomial** `m_A` is the unique monic polynomial of least degree
such that `m_A(A) = 0`.

Two facts. It always **divides** `p_A` and has the **same roots** as `p_A`, so it
can be found by testing the divisors of `p_A`. And its degree equals the size of
the **largest Jordan block** at any eigenvalue.

The degree matters computationally: to evaluate `f(A)` you need `deg m_A` powers,
not `n`. The identity matrix `I₂` has `m_A = L − 1`, degree 1, so `f(I₂) =
f(1)·I₂` for every `f` — it behaves exactly like the number 1. A single Jordan
block has `m_A = p_A`, the full degree, and is the worst case.

</details>

**Q4. State the spectral theorem and give the two-line proof sketch.**

<details>
<summary>Model answer</summary>

**Theorem.** If `A` is real and symmetric, then all its eigenvalues are real and
`A = QDQᵀ` for an orthogonal `Q` and a real diagonal `D`.

**Proof sketch.** Take eigenvectors `Au = λu` and `Av = μv`. By symmetry,

    λ(u^T v) = (Au)^T v = u^T(Av) = μ(u^T v)

so `(λ − μ)(uᵀv) = 0`. Distinct eigenvalues therefore give **perpendicular**
eigenvectors. For equal eigenvalues, any spanning set of the eigenspace can be
replaced by an orthonormal one via Gram–Schmidt
([38](../part03_linear_algebra/38_orthogonality_and_least_squares.md)). Either way an orthonormal eigenbasis
exists, and `Q⁻¹ = Qᵀ`.

</details>

**Q5. Give three equivalent tests for a symmetric matrix to be positive definite,
and say which is cheapest in each direction.**

<details>
<summary>Model answer</summary>

For a **real symmetric** `A`, the following are equivalent:

1. `xᵀAx > 0` for every nonzero `x`.
2. Every eigenvalue of `A` is positive.
3. Every leading principal minor `Δ_k` is positive (Sylvester's criterion).

The bridge between (1) and (2) is the eigenbasis: writing `x = Qc` gives
`xᵀAx = cᵀQcᵀ(QDQᵀ)Qc = cᵀDc = Σλᵢcᵢ²`, a weighted sum of squares that is
positive exactly when every `λᵢ > 0`.

**Cheapest depends on what you have.** If you already have the eigenvalues — say
from `np.linalg.eigh` — test (2); it is free. If you want a yes/no without a
spectral decomposition, Cholesky or the leading minors (3) are cheaper, and
Cholesky additionally *gives you the factorisation*. The lesson's `S` has
eigenvalues `0.6385, 2.8326, 5.5289` (all positive) and leading minors
`4, 11, 10` (all positive) — the two tests agree, as they must.

</details>

**Q6. For `S = [[4,1,2],[1,3,0],[2,0,2]]`, state the eigenvalues, the leading
minors, the Cholesky factor, and the solution of `Sx = (1,2,3)`.**

<details>
<summary>Model answer</summary>

Eigenvalues `0.638531`, `2.832551`, `5.528918` (from `np.linalg.eigh`), summing to
`tr(S) = 9` and multiplying to `det(S) = 10`.

Leading principal minors: `Δ₁ = 4`, `Δ₂ = det[[4,1],[1,3]] = 11`,
`Δ₃ = det(S) = 10`. All positive, so `S` is positive definite.

Cholesky factor

    L = [ 2.0000   0       0    ]
        [ 0.5000   1.6583  0    ]
        [ 1.0000  -0.3015  0.9535]

with `LLᵀ = S` exactly.

Solving `Sx = (1,2,3)`: forward substitution `Ly = (1,2,3)` gives
`y = (0.5, 1.055290, 2.955734)`, then `Lᵀx = y` gives
`x = (−1.6, 1.2, 3.1)`, which agrees with a full matrix inverse to `10⁻⁹`.

</details>

### Long Answer

**Q1. Why does the spectral theorem need symmetry, and what exactly breaks without
it? What would you use instead?**

<details>
<summary>Model answer</summary>

**Where the proof needs symmetry.** The whole spectral theorem turns on
`(Au)ᵀv = uᵀ(Av)`, which is `uᵀAᵀv = uᵀAv` — true only when `Aᵀ = A`. Without it
you get `(λ − μ)(uᵀv) = 0` replaced by nothing usable, and indeed the eigenvectors
need not be perpendicular, need not exist as real vectors, and may not span at
all.

**The three things that break, in increasing severity.**

*Realness.* Without symmetry the characteristic polynomial has real coefficients
but may have no real roots. The lesson's own example,
`M = [[2,−1],[1,2]]`, has eigenvalues `2 ± i`. `np.linalg.eigvals(M)` returns
them; `eigh` cannot even be asked.

*Orthogonality.* Take `A = [[1,1],[0,1]]`. Its only eigenvalue is 1 with
`E₁ = span((1,0))`, dimension 1 out of 2, so it is defective — no eigenbasis
exists. Now take `A = [[2,0],[0,1]]`: diagonalisable, eigenvectors `(1,0)` and
`(0,1)`, orthogonal only by luck of the diagonal. A genuinely non-orthogonal
diagonalisable example is `[[1,1],[0,2]]`, whose eigenvectors are `(1,0)` and
`(1,1)` — dot product 1, not 0.

*Stability.* Even when a general matrix diagonalises with independent
eigenvectors, `V` can be arbitrarily close to singular, and `A = VDV⁻¹` then
requires an explicit inverse. `cond(V)` is not controlled by anything in the
spectrum. This is the same failure as `V⁻¹AV` in general, and it is exactly what
symmetry removes by guaranteeing `cond(Q) = 1`.

**What to use instead.** The **singular value decomposition**,
`A = UΣVᵀ` ([40](../part03_linear_algebra/40_svd_and_pca.md)), which exists for *every* matrix, has
`σᵢ ≥ 0` always real, sorted descending, and `U, V` always orthogonal. When `A`
is symmetric the two coincide up to signs: `σᵢ = |λᵢ|` and `U` can be taken as
`V` (up to sign flips for negative eigenvalues). So the SVD is not a different
theory — it is the spectral theorem with the symmetry requirement removed, at the
cost of losing the sign information that eigenvalues carry.

The other fallback is the **Schur decomposition**, `A = QTQ*` with `T`
quasi-upper-triangular. It exists for every matrix, `Q` is always orthogonal, and
it is numerically stable where Jordan form is not.

</details>

**Q2. Why is `np.linalg.matrix_rank(V) < n` the practical test for defective, and
what should you actually reach for when it fires?**

<details>
<summary>Model answer</summary>

**Why that test.** `A = VDV⁻¹` exists exactly when the columns of `V` are `n`
linearly independent eigenvectors. Independence is precisely `rank(V) = n`, and
that is exactly what makes `det(V) ≠ 0` and `V⁻¹` exist. So one call —
`np.linalg.matrix_rank(V)` — answers the question that the whole
geometric/algebraic multiplicity theory is about, without computing any
multiplicity.

The lesson's code applies it to the 3×3 Jordan block `J` and prints
`rank(V4) = 1`, then says "only 1, so `J` is defective and cannot be
diagonalised". Two matrices with *identical* eigenvalues — `J` and `diag(2,2,2)`
— have ranks 1 and 3 respectively, which is the sharpest possible statement that
the eigenvalues do not determine the answer.

**The numerical caveat.** `matrix_rank` uses a tolerance, typically
`σ_max · n · eps`. Eigenvectors of a defective matrix come back nearly parallel
but not exactly, so the rank is computed from a singular value near the
threshold and the answer can depend on the conditioning. This is another reason
not to lean on defective matrices numerically.

**What to reach for instead, in order of preference.**

1. **The SVD** (`np.linalg.svd(A)`), which exists for every matrix and gives the
   best rank-revealing description of all. The number of singular values above
   `rcond` *is* the numerical rank, and dropping the rest is the numerically
   correct version of "diagonalising what you can and discarding the rest".
2. **Pseudoinverse** (`np.linalg.pinv(A)`) — the minimum-norm answer computed
   stably, which is what `np.linalg.lstsq` uses internally for rank-deficient
   input ([38](../part03_linear_algebra/38_orthogonality_and_least_squares.md)).
3. **Regularisation.** Adding `λI` (ridge) or dropping to `lstsq` sidesteps the
   question entirely; the lesson's ridge table is a demonstration that you can
   trade a little bias for a large reduction in variance.
4. **Just check symmetry first.** If `np.allclose(A, A.T)` holds, you are done —
   use `eigh` and the problem cannot occur. Most of ML is symmetric matrices
   (Gram matrices, Hessians, covariances, Laplacians), which is why this failure
   mode is rare in practice and common in coursework, where the examples are
   deliberately triangular.

</details>

**Q3. Why is positive definiteness the algebraic condition for convexity, and
what breaks in optimisation when it fails?**

<details>
<summary>Model answer</summary>

**Why PD means convex.** Consider a quadratic loss `f(x) = ½xᵀHx − bᵀx`, with
`H` symmetric. Its gradient is `∇f(x) = Hx − b` and its Hessian is the constant
matrix `H`. A function is convex iff its Hessian is positive semidefinite
everywhere; for a quadratic that reduces to a statement about `H` itself, so
there is nothing to check pointwise.

The bridge to eigenvalues is the same one from Short Answer Q5: in the eigenbasis
of `H`, `f(c) = ½Σλᵢcᵢ² − bᵀc`. If every `λᵢ > 0` the function rises in every
direction from its critical point, so it has exactly one minimum and it is a
global one. `λᵢ = 0` gives a flat direction — a valley, with a line of minimisers,
so the solution is not unique (the under-determined least-squares situation).
Any `λᵢ < 0` makes the function fall without bound in that direction, so there is
no minimum at all.

**What breaks when it fails.**

- **Non-uniqueness.** With a zero eigenvalue the minimiser is a whole affine
  line: any point on it is equally optimal. Newton's method stalls because the
  linear system is singular. This is the same under-determination as a
  rank-deficient least-squares problem, and the fix is the minimum-norm
  solution.
- **Unboundedness.** With a negative eigenvalue the objective is unbounded below
  and gradient descent diverges. In a neural network this is the algebraic form
  of a saddle point or an exploding training loss.
- **Numerical failure.** A small positive eigenvalue makes `H⁻¹` enormous:
  `cond(H) = λ_max/λ_min`. The symmetric matrix
  `[[1, 0.999999],[0.999999, 0.999999]]` has `λ_min = 5 × 10⁻⁷` and
  `cond ≈ 4 × 10⁶`, so six digits vanish from any solve against it. This is the
  collinear-features case: two nearly-parallel columns make the direction they
  span indistinguishable, and the coefficient along it is determined by noise.
- **Wrong Gauss–Newton.** In [38](../part03_linear_algebra/38_orthogonality_and_least_squares.md) the
  Gauss–Newton matrix is `JᵀJ`, which is positive *semidefinite*, never negative.
  The failure is therefore the singular/flat case, and ridge's `+λI` is exactly
  the cure: it lifts every zero eigenvalue to `λ` and makes the system solvable.

The practical summary is one line: check `np.linalg.eigvalsh(H)` and require
`min > 0`. If it is not, fix the *data* (collinearity, missing normalisation)
rather than the algorithm.

</details>

**Q4. Why does `A^k = VD^kV⁻¹` matter computationally, and what does the identity
`tr(A^k) = Σλᵢ^k` buy you for free?**

<details>
<summary>Model answer</summary>

**Why diagonalisation wins on powers.** By repeated multiplication,
`A^k` costs `k − 1` matrix multiplies, each `O(n³)`, so `O(n³k)`. Via
`A^k = VD^kV⁻¹` you raise the `n` diagonal entries to the `k`-th power — `O(n)`
scalar work — and then pay a *fixed* two matrix multiplies, `O(n³)` total,
independent of `k`. For the lesson's `S` with `k = 50`, the library block
verifies `Q diag(w^k) Qᵀ == S^50` while the naive route would need 49
multiplies. This is the standard way matrix exponentials are computed, which in
turn is how linear Kalman filters and long-run Markov chain limits are evaluated.

**What the trace identity buys.** `tr(A^k) = Σᵢ λᵢ^k` for every `k ≥ 1`. Note it
does not even require diagonalisability — it follows from Cayley–Hamilton by
multiplying `p_A(A) = 0` by `A^{k−1}` and taking traces. It is a consistency check
that costs no additional matrix multiplies beyond the one you already did, and
for the lesson's `S` the values match to the last digit:

    k=1    tr = 9        Σλ = 9
    k=2    tr = 39       Σλ² = 39
    k=3    tr = 192      Σλ³ = 192
    k=5    tr = 5349     Σλ⁵ = 5349
    k=10   tr = 26726499 Σλ¹⁰ = 26726499

Since eigenvalues from an iterative method are never exactly right, this is a
genuine independent test — the eigenvalues come from a root-finder on `p_A`,
the trace comes from a matrix product, and they must agree.

It also has a use beyond checking. The Newton identities recover the coefficients
of `p_A` from `tr(A), tr(A²), …, tr(Aⁿ)`, which is Faddeev–LeVerrier restated —
the lesson's `charpoly` helper computes `c_k = −tr(A^k)/k` for exactly this
reason. And it predicts the growth of `A^k`: since `tr(A¹⁰)` is entirely
dominated by `5.5289¹⁰ ≈ 2.67 × 10⁷`, you know without computing anything that
`A¹⁰` is essentially rank-one along the top eigenvector. That is the numerical
content of "the data spreads mostly in one direction", i.e. PCA.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — spectral theorem checks.** Let
`S = [[2, 1], [1, 2]]`.

(a) Show `S` is symmetric, find its characteristic polynomial, and its
eigenvalues.
(b) Find an orthonormal matrix `Q` with `QᵀSQ` diagonal, and verify
`QᵀQ = I`.
(c) Show `S` is positive definite, using both the eigenvalue test and
Sylvester's criterion.
(d) Compute the Cholesky factor `L` with `S = LLᵀ` and use it to solve
`Sx = (3, 3)`.

<details>
<summary>Solution</summary>

**(a)** `S[0][1] = 1 = S[1][0]` ✓ symmetric.
`S − λI = [[2−λ, 1], [1, 2−λ]]`, so `p_S(λ) = (2−λ)² − 1 = λ² − 4λ + 3 = (λ−1)(λ−3)`.
Eigenvalues `1` and `3`. Check: `tr(S) = 4 = 1 + 3` ✓, `det(S) = 4 − 1 = 3 = 1·3` ✓.

**(b)** For `λ = 1`: `S − I = [[1,1],[1,1]]`, so `x + y = 0` → `(1, −1)/√2`.
For `λ = 3`: `S − 3I = [[−1,1],[1,−1]]`, so `−x + y = 0` → `(1, 1)/√2`.

```
Q = [ 0.7071  0.7071 ]      D = [1  0]
    [-0.7071  0.7071 ]          [0  3]
```

`QᵀQ = [[0.5+0.5, −0.5+0.5], [−0.5+0.5, 0.5+0.5]] = I` ✓ (exactly, since
`2·(1/√2)² = 1` and the cross terms cancel).

`QᵀSQ = D`, and `S = Q D Qᵀ`. Note `Q⁻¹ = Qᵀ` exactly, so no inverse is needed.

**(c)** *Eigenvalue test:* both eigenvalues (1, 3) are positive, so `S` is
positive definite.
*Sylvester:* leading minors are `Δ₁ = 2` and `Δ₂ = det(S) = 3`. Both positive,
so `S` is positive definite ✓. The two tests agree, as they must.

Directly: `xᵀSx = 2x₁² + 2x₁x₂ + 2x₂² = (x₁+x₂)² + x₁² + x₂² > 0` whenever
`x ≠ 0`. Notice the decomposition: this is Pythagoras in the eigenbasis, made
explicit.

**(d)** Cholesky: `L = [[a, 0], [b, c]]` with `LLᵀ = [[a², ab], [ab, b²+c²]]`.
`a² = 2` → `a = √2`. `ab = 1` → `b = 1/√2`. `b² + c² = 2` → `c² = 2 − 1/2 = 3/2`
→ `c = √(3/2)`.

```
L = [ 1.41421356   0        ]
    [ 0.70710678   1.22474487]
```

`LLᵀ = [[2, 1], [1, 0.5 + 1.5]] = [[2,1],[1,2]] = S` ✓

Solve `Ly = b` (forward), then `Lᵀx = y` (back), with `b = (3, 3)`:

Forward: `y₁ = 3/√2 = 2.12132034`.
`y₂ = (3 − (1/√2)(3/√2))/√(3/2) = (3 − 1.5)/1.22474487 = 1.22474487`.

Back, with `Lᵀ = [[1.41421356, 0.70710678], [0, 1.22474487]]`:
`x₂ = y₂/1.22474487 = 1.0`, then
`x₁ = (y₁ − 0.70710678·x₂)/1.41421356 = (2.12132034 − 0.70710678)/1.41421356 = 1.0`.

```
x = (1.0, 1.0)
```

Check: `S x = (2·1 + 1·1, 1·1 + 2·1) = (3, 3)` ✓. And the answer was
predictable after the fact: `(1,1)` is the eigenvector for `λ = 3`, and
`3(1,1) = (3,3)`, so `x` is one third of it. The value of the Cholesky route
is that it arrives at the same answer without needing to know that first — and
that a wrong intermediate step shows up immediately in the final check.

</details>

**[ ] Exercise 2 — when diagonalisation fails.** Consider
`A = [[1, 1, 0], [0, 1, 1], [0, 0, 1]]`.

(a) Find the characteristic polynomial and the eigenvalues.
(b) Find all eigenvectors, and state the geometric and algebraic multiplicities.
(c) Conclude whether `A` is diagonalisable.
(d) Show directly that `A ≠ 4I` and `A² ≠ 4A` (relevant for the minimal
polynomial), then determine the minimal polynomial by testing which
polynomials of degree ≤ 3 annihilate `A`.

<details>
<summary>Solution</summary>

**(a)** `A` is upper triangular, so the eigenvalues are the diagonal: all `1`.
`p_A(λ) = (λ−1)³ = λ³ − 3λ² + 3λ − 1`. Check: `tr(A) = 3 = 1+1+1` ✓,
`det(A) = 1 = 1·1·1` ✓.

**(b)** Solve `(A − I)v = 0`:
```
A - I = [0  1  0]
        [0  0  1]
        [0  0  0]
```
The first row gives `x₂ = 0`, the second gives `x₃ = 0`; `x₁` is free. So the
eigenspace is `{t(1, 0, 0) : t ∈ ℝ}`, dimension 1.

- **Geometric multiplicity** of `λ = 1` is **1**.
- **Algebraic multiplicity** is **3** (it is a triple root).

**(c)** Geometric (1) < algebraic (3), so `A` is **defective** and **not
diagonalisable**. There is no invertible `V` with `V⁻¹AV` diagonal. The three
eigenvectors we would need all point in the same direction, so `V` would have
three identical columns and determinant zero.

**(d)** Minimal polynomial. Test the candidates, which must be divisors of
`(λ−1)³`, i.e. `1`, `(λ−1)`, `(λ−1)²`, `(λ−1)³`.

- `m = 1`: `1(A) = I ≠ 0` ✗
- `m = λ−1`: `(A − I) = [[0,1,0],[0,0,1],[0,0,0]] ≠ 0` ✗
- `m = (λ−1)²`: `(A−I)² = 0`? Compute:
  ```
  (A-I) = [0 1 0]        (A-I)^2 = [0 1 0][0 1 0]   [0 0 1][0 0 1]   [0 0 0][0 0 0]
          [0 0 1]                 [0 0 1]            [0 0 0]            [0 0 0]
          [0 0 0]                 [0 0 0]            [0 0 0]            [0 0 0]
                              = [0 0 1]
                                [0 0 0]
                                [0 0 0]
  ```
  That is **not** zero ✗
- `m = (λ−1)³`: Cayley–Hamilton guarantees it, and indeed `A³ − 3A² + 3A − I = 0`.

So the minimal polynomial is `(λ−1)³`, degree 3, equal to the characteristic
polynomial. That makes sense: the single Jordan block has size 3, and the
minimal polynomial's degree is the size of the largest Jordan block.

Practical consequence: to evaluate any polynomial `f` at `A` you need
`f(1)`, `f'(1)`, `f''(1)/2` rather than three independent values. In
particular `e^A = e·(I + 0 + 0) = eI`, which you can verify: `e^A = e^1 I`
because `A` is a single Jordan block on the eigenvalue 1.

</details>

**Challenge — Exercise 3 — PCA by hand, without SVD.** Take the symmetric
matrix

```
M = [[6, 2], [2, 3]]
```

(a) Show `M` is positive definite (use both tests).
(b) Find its eigenvalues by solving the characteristic equation by hand.
(c) Verify that the corresponding eigenvectors are orthogonal.
(d) Compute the explained-variance ratio if `M` is a covariance matrix and you
keep only the top component.
(e) What changes if you use a *non*-symmetric matrix of the same size? Name one
thing that breaks and one thing that does not.

<details>
<summary>Solution</summary>

**(a)** *Symmetric:* `M[0][1] = 2 = M[1][0]` ✓.
*Sylvester:* `Δ₁ = 6 > 0`, `Δ₂ = det(M) = 18 − 4 = 14 > 0` ✓.
*Eigenvalues:* both positive (computed in (b)), consistent ✓.
So `M` is symmetric positive definite.

**(b)** `det(M − λI) = (6−λ)(3−λ) − 4 = 18 − 9λ + λ² − 4 = λ² − 9λ + 14`.
Setting to zero: `λ = [9 ± √(81 − 56)]/2 = [9 ± √25]/2 = [9 ± 5]/2`.
So `λ₁ = 7` and `λ₂ = 2`. Both real and positive, as symmetry promised.
Check: `tr(M) = 9 = 7 + 2` ✓, `det(M) = 14 = 7·2` ✓.

**(c)** For `λ = 7`: `M − 7I = [[−1, 2], [2, −4]]`, so `−x + 2y = 0` → `x = 2y`.
Take `u₁ = (2, 1)/√5 = (0.89442719, 0.44721360)`.
For `λ = 2`: `M − 2I = [[4, 2], [2, 1]]`, so `4x + 2y = 0` → `y = −2x`.
Take `u₂ = (1, −2)/√5 = (0.44721360, −0.89442719)`.

Dot product: `(2·1 + 1·(−2))/5 = (2 − 2)/5 = 0` ✓. Orthogonal, exactly.

Norms: `‖u₁‖ = ‖u₂‖ = √(4+1)/√5 = 1` ✓. So `{u₁, u₂}` is orthonormal.

**(d)** Total variance `= λ₁ + λ₂ = 9`. Keeping only the top component captures
`λ₁ = 7`, so the **explained variance ratio is 7/9 ≈ 0.7778**, i.e. 77.78%.
Projected onto the second component only: `2/9 ≈ 0.2222`, or 22.22%.

So a single component already explains over three quarters of the spread.
That is the practical statement of what "the data spreads mostly in one
direction" means.

**(e)** For a non-symmetric matrix, say `N = [[6, 1], [4, 3]]`:

- **Breaks:** the eigenvalues can be **complex**. `det(N − λI) = (6−λ)(3−λ) − 4 =
  18 − 9λ + λ² − 4 = λ² − 9λ + 14`, which happens to still be real here
  (7 and 2). But in general there is no guarantee. The eigenvectors need not be
  orthogonal either, so the "variance" they represent is not a clean
  decomposition, and the explained-variance ratio no longer means anything.
  With complex eigenvectors, PCA is not defined at all.
- **Does not break:** the *algebra*. Cayley–Hamilton still holds, the
  characteristic polynomial still exists, diagonalisation may still be possible,
  and powers still satisfy `A^k = V D^k V⁻¹` if `A` happens to be
  diagonalisable.

This is exactly why every practical pipeline symmetrises first: PCA on a
covariance matrix is PCA on a symmetric matrix, so the orthonormal basis and
the real, ordered, non-negative "variance" eigenvalues are guaranteed. When the
matrix is not symmetric, you need the SVD instead — which is the next lesson,
and which is exactly the tool that fixes all of this.

</details>

**[ ] Exercise 4 — Cayley–Hamilton and `e^S` without a library.** Let
`S = [[4, 1, 2], [1, 3, 0], [2, 0, 2]]`, the matrix from the worked example.

(a) Compute `p_S(λ) = det(λI − S)` and confirm `S³ − 9S² + 21S − 10I = 0`
numerically.
(b) Find the eigenvalues of `S` and check that the coefficient `−9` equals
`−tr(S)` and the constant `−10` equals `−det(S)`.
(c) Show `tr(Sᵏ) = Σλᵢᵏ` for `k = 1, 2, 3`.
(d) Use the polynomial remainder of `eˣ` modulo `p_S(x)` to compute `e^S`, and
check the result against `scipy.linalg.expm`.
(e) Count how many matrix multiplications your method needed, and compare with
the direct series.

<details>
<summary>Solution</summary>

**(a)** `λI − S = [[λ−4, −1, −2], [−1, λ−3, 0], [−2, 0, λ−2]]`. Expanding along
the first row:

    p_S(λ) = (λ−4)[(λ−3)(λ−2)] − (−1)[(−1)(λ−2) − 0] + (−2)[(−1)(0) − (λ−3)(−2)]
            = (λ−4)(λ² − 5λ + 6) − (λ−2) − 4(λ−3)
            = (λ³ − 9λ² + 26λ − 24) − (λ−2) − (4λ − 12)
            = λ³ − 9λ² + 26λ − 24 − λ + 2 − 4λ + 12
            = λ³ − 9λ² + 21λ − 10

Now verify by direct multiplication:

    S²  = [[ 21,  7, 12],
           [  7, 10,  2],
           [ 12,  2,  8]]

    S³  = [[115, 42, 66],
           [ 42, 37, 18],
           [ 66, 18, 40]]

    S³ − 9S² + 21S − 10I
       = [[115−189+84−10, 42−63+21,      66−108+42    ],
          [42−63+21,      37−90+63−10,  18−18       ],
          [66−108+42,     18−18,        40−72+42−10 ]]
       = [[0, 0, 0],
          [0, 0, 0],
          [0, 0, 0]]

Exactly zero, entry by entry. That is Cayley–Hamilton, verified.

**(b)** `np.linalg.eigvalsh(S)` returns `0.638531`, `2.832551`, `5.528918`.

`tr(S) = 4 + 3 + 2 = 9`, and `Σλ = 0.638531 + 2.832551 + 5.528918 = 9.000000`
✓ — the coefficient of `λ²` is `−Σλᵢ = −9`.

`det(S) = 4(3·2 − 0·0) − 1(1·2 − 0·2) + 2(1·0 − 3·2) = 24 − 2 − 12 = 10`, and
`Πλᵢ = 10.000000` ✓ — the constant term is `−Πλᵢ = −10` (for a degree-`n`
polynomial, the constant is `(−1)ⁿ Πλᵢ`, and `n = 3` is odd).

**(c)** Using the eigenvalues and the matrix powers from (a):

    k=1:  tr(S)   = 4 + 3 + 2                    = 9
         Σλ      = 0.638531 + 2.832551 + 5.528918 = 9.000000
    k=2:  tr(S²)  = 21 + 10 + 8                  = 39
         Σλ²     = 0.407722 + 8.023344 + 30.568934 = 39.000000
    k=3:  tr(S³)  = 115 + 37 + 40                = 192
         Σλ³     = 0.260343 + 22.726530 + 169.013127 = 192.000000

The identity holds to the precision of the eigenvalues. Note it does *not*
require diagonalisability — it follows from Cayley–Hamilton directly, by
multiplying `p_S(S) = 0` by `S^{k−1}` and taking traces.

**(d)** Reduce `eˣ` modulo `p_S(x) = x³ − 9x² + 21x − 10`. Seek
`f(x) = c₀ + c₁x + c₂x²` with `f(λᵢ) = e^{λᵢ}`:

    c₀ + c₁(0.638531) + c₂(0.407722)  = 1.893697
    c₀ + c₁(2.832551) + c₂(8.023344)  = 16.988741
    c₀ + c₁(5.528918) + c₂(30.568934) = 251.871228

Solving (Lagrange interpolation on the three eigenvalues):

    c₀ =  27.173235
    c₁ = −50.065741
    c₂ =  16.405785

So

    e^S = 27.173235·I − 50.065741·S + 16.405785·S²
        = 27.173235·I − 50.065741·[[4,1,2],[1,3,0],[2,0,2]]
                          + 16.405785·[[21,7,12],[7,10,2],[12,2,8]]
        = [[171.431764,  64.774757,  96.737943],
           [ 64.774757,  41.033866,  32.811571],
           [ 96.737943,  32.811571,  58.288036]]

which equals `scipy.linalg.expm(S)` to every printed digit, and agrees to
`8.4 × 10⁻⁶` even with the coefficients rounded to six decimals. Independently,
`Q diag(e^{λᵢ}) Qᵀ` with `Q` from `np.linalg.eigh(S)` gives the same matrix.

**(e)** Two matrix multiplies: one to form `S²`, and one for the Horner step
`(c₂S + c₁I)S + c₀I`. With three distinct eigenvalues the degree is `n − 1 = 2`,
so this is the best the method can do. Contrast the direct series
`e^S = I + S + S²/2 + S³/6 + …`: to reach six correct decimals here you would
need terms up to about `S¹⁰`, i.e. roughly ten matrix multiplies plus Horner
scaling, and the terms are enormous before they are scaled — `S¹⁰` has entries
of order `1.8 × 10⁷`, so the series suffers catastrophic cancellation in the
early terms. That cancellation risk is the real reason nobody computes `e^S` by
summing the series.

</details>

**[ ] Exercise 5 — Cholesky, Sylvester, and a matrix that nearly fails.** Let
`T = [[2, 1, 0], [1, 2, 1], [0, 1, 2]]`.

(a) Compute the leading principal minors and decide whether `T` is positive
definite.
(b) Compute the Cholesky factor `L` by hand, entry by entry, and verify
`LLᵀ = T`.
(c) Solve `Tx = (1, 2, 3)` using the two triangular solves.
(d) Now consider `B = [[1, 1], [1, 1]]`. Report its eigenvalues, its leading
minors, and what `np.linalg.cholesky(B)` does.
(e) Explain what `B` means geometrically, and name one situation in machine
learning where `B` is exactly what you get.

<details>
<summary>Solution</summary>

**(a)** `Δ₁ = 2`. `Δ₂ = det[[2,1],[1,2]] = 4 − 1 = 3`. `Δ₃ = det(T)`.

Expand `det(T)` along the first row: `2(2·2 − 1·1) − 1(1·2 − 1·0) + 0(…) =
2·3 − 2 = 4`.

`Δ₁ = 2, Δ₂ = 3, Δ₃ = 4` — all positive, so by Sylvester's criterion `T` is
symmetric positive definite. (Its eigenvalues are `2−√2, 2, 2+√2`, i.e.
`0.585786, 2.0, 3.414214` — all positive, the second test agreeing with the
first.)

**(b)** Write `L = [[a,0,0],[b,c,0],[d,e,f]]` and match `LLᵀ = T` entry by entry:

    (0,0): a² = 2                  → a = √2
    (1,0): ab = 1                  → b = 1/√2
    (1,1): b² + c² = 2             → c = √(2 − 1/2) = √(3/2) = 1.224745
    (2,0): ad = 0                  → d = 0
    (2,1): bd + ce = 1             → 0 + (√(3/2))e = 1 → e = 1/√(3/2) = 0.816497
    (2,2): d² + e² + f² = 2        → 0 + 2/3 + f² = 2 → f = √(4/3) = 1.154701

    L = [[1.414214, 0,        0       ],
         [0.707107, 1.224745, 0       ],
         [0,        0.816497, 1.154701]]

`LLᵀ = [[2, 1, 0], [1, 2, 1], [0, 1, 2]] = T` ✓

Note the positive diagonal was forced at each step by taking a positive square
root — that is exactly what makes `L` unique.

**(c)** With `b = (1, 2, 3)`:

*Forward*, `Ly = b`:

    y₁ = 1/√2                        = 0.707107
    y₂ = (2 − (1/√2)(0.707107))/1.224745 = (2 − 0.5)/1.224745 = 1.224745
    y₃ = (3 − 0 − (0.816497)(1.224745))/1.154701 = (3 − 1)/1.154701 = 1.732051

*Back*, `Lᵀx = y`:

    x₃ = 1.732051/1.154701          = 1.5
    x₂ = (1.224745 − 0.816497·1.5)/1.224745 = (1.224745 − 1.224745)/1.224745 = 0
    x₁ = (0.707107 − 0.707107·0)/1.414214 = 0.5

    x = (0.5, 0, 1.5)

Check: `T x = (2·0.5 + 0, 0.5 + 0 + 1.5, 0 + 0 + 3) = (1, 2, 3)` ✓

**(d)** `np.linalg.eigvalsh(B)` returns `0` and `2`. The leading minors are
`Δ₁ = 1` and `Δ₂ = det(B) = 1 − 1 = 0`. `np.linalg.cholesky(B)` raises
`LinAlgError: Matrix is not positive definite`, and so does `np.linalg.inv(B)`
with `Singular matrix`.

So `B` is symmetric and **positive semidefinite but not positive definite**: one
eigenvalue is exactly zero. Sylvester's criterion catches it at `Δ₂ = 0`, and
Cholesky fails at the corresponding step, where it would need
`√(1 − 1²) = √0`.

**(e)** Geometrically, `B` maps `(a, b)` to `(a + b, a + b)` — it projects onto
the line `y = x`. Every vector `v` with `v₂ = −v₁` is sent to zero, so the line
`y = −x` is the *null space*, and the "zero eigenvalue" is literally the
direction the data has no spread in.

In machine learning this is exactly the **collinear features** case. Take
`X = [[1, 2], [2, 4]]`: the second column is twice the first, so the
sample covariance matrix is `[[1, 2], [2, 4]]` up to a factor — a rescaled `B`.
`np.linalg.inv(cov)` raises `Singular matrix`, which is Common Mistake 4 in the
lesson. More columns of the same kind push the smallest eigenvalue toward zero
rather than exactly zero, giving `cond ≈ 4 × 10⁶` instead of `∞` — numerically
worse, because the inverse returns plausible huge numbers instead of raising.
Standardisation does not fix it (it rescales but does not decorrelate), and the
actual cures are: drop one of the collinear features, or add ridge.

</details>

**Challenge — Exercise 6 — why a tiny eigenvalue is a numerical catastrophe, not
a curiosity.** Let `C = [[1, 0.999999], [0.999999, 0.999999]]`.

(a) Compute `cond(C)`, its eigenvalues, and its Cholesky factor. Note how small
the bottom-right entry of `L` is and why.
(b) Solve `Cx = (1, 1)`, then solve `C(x + δ) = (1, 1)` for
`δ = (10⁻⁷, 0)`. Compare the two solutions.
(c) Give the ratio of `‖Δx‖₂` to `‖δ‖₂` and predict it from `cond(C)`.
(d) Explain why `np.linalg.cond(C) = λ_max/λ_min` here but not for a general
matrix.
(e) Name the practical fix and say what it costs.

<details>
<summary>Solution</summary>

**(a)**

    eig(C) = [5.0e-7, 1.9999985]      (sums to 2 = tr(C) ✓)
    cond(C) = 1.9999985 / 5.0e-7 = 3999998.0006

    L = [[1.0, 0],
         [0.999999, 0.001]]

The bottom-right entry is `√(1 − 0.999999²) = √(1e-6) = 0.001`, exactly. Read it
as a measurement: after Cholesky has removed the shared component of the two
rows, `1e-6` of "signal" is left in the second direction, and `L₂₂` is the square
root of that residue. It is also why the Cholesky factor of a nearly-collinear
matrix is nearly singular.

**(b)**

    C⁻¹(1,1)ᵀ = (0, 1)ᵀ
    C⁻¹(1 + 1e-7, 1)ᵀ = (0.1, 0.9)ᵀ

**(c)**

    ‖Δx‖₂ = √(0.1² + 0.1²) = 0.14142136
    ‖δ‖₂ = 1e-7
    ratio = 1414213.6

`cond(C) = 3999998`, and the observed amplification `1.41 × 10⁶` is of that
order — the ratio is what the 2-norm bound guarantees, and the exact figure
depends on the direction of the perturbation relative to the eigenvector for
`λ_min`. A `10⁻⁷` perturbation in the input produced a `0.14` change in the
answer.

**(d)** For a **symmetric** `C`, write `C = QΛQᵀ`. Then
`C⁻¹ = QΛ⁻¹Qᵀ`, so `σᵢ(C) = |λᵢ|`. Every real symmetric matrix has real
eigenvalues, so `σᵢ = |λᵢ|` and
`cond = σ_max/σ_min = λ_max/λ_min`. The computation is exact, not a
coincidence: for SPD matrices `σᵢ = λᵢ > 0` with no sign cancellation.

For a general matrix, `cond = σ_max/σ_min` where `σᵢ = √λᵢ(AᵀA)`, which has
nothing to do with `λᵢ(A)`. Take the rotation `R = [[0,−1],[1,0]]`: it is
perfectly conditioned, `cond = 1`, yet its eigenvalues are `±i` and `λ_max/λ_min`
is meaningless. Take `[[2,1],[0,2]]`: `cond = 4` from singular values `2` and
`0.5`, while both eigenvalues are `2`. Symmetry is what makes the two notions
coincide, which is why `cond` of a symmetric matrix can be read straight off the
spectrum you already computed.

**(e)** **The fix is regularisation** — exactly ridge from
[38](../part03_linear_algebra/38_orthogonality_and_least_squares.md). Replace `C` by `C + λI`. The
eigenvalues become `5e-7 + λ` and `1.9999985 + λ`, so
`cond = (1.9999985 + λ)/(5e-7 + λ)`, and with `λ = 10⁻⁶` the ratio drops from
`4 × 10⁶` to about `1 × 10⁶`; with `λ = 10⁻³` it is about `2`. The solves agree:

    λ = 0:      (0.0000, 1.0000)
    λ = 1e-6:   (0.3333, 0.6667)
    λ = 1e-3:   (0.4995, 0.5000)

**The cost** is bias. `λ = 0` gives the unbiased answer; the ridge answer is
pulled toward the regularised optimum, which is a *different* problem. With
`λ = 10⁻⁶` the answer `(0.333, 0.667)` is a third of the way from the ridge limit
`(0.5, 0.5)` toward the true `(0, 1)` — you have traded six digits of precision
for a systematic 33% error in the coefficients. That is the whole bias-variance
trade in one line, and it is why `λ` is chosen on held-out data rather than
minimised: you cannot minimise the quantity you gave away.

The alternative fix, when you can, is to delete one of the collinear features.
That costs nothing statistically — the information is genuinely duplicated — and
is strictly better when you are able to identify which. Regularisation is for
when you cannot.

</details>

## Summary

- `A` is **diagonalisable** iff it has `n` independent eigenvectors, i.e. iff
  geometric multiplicity equals algebraic multiplicity for every eigenvalue.
- **Cayley–Hamilton** says `p_A(A) = 0`, so a matrix behaves like a polynomial
  of degree `n`. This is how you compute any function of a matrix, including
  `e^A`, in `n` multiplies instead of an infinite series.
- The **minimal polynomial** is the shortest such relation. It shares the
  characteristic polynomial's roots but can be far lower degree, and its degree
  is the largest Jordan block size.
- A **defective** matrix cannot be diagonalised. `np.linalg.matrix_rank(V) < n`
  is the one-line test.
- **Jordan form** always exists and is the simplest similar matrix, built from
  chains of generalised eigenvectors. It is numerically delicate, so prefer SVD.
- **Symmetric matrices** are the good case: real eigenvalues, an orthonormal
  eigenbasis, and `A = Q D Qᵀ` with no inverse needed. This is the spectral
  theorem, and `np.linalg.eigh` exists because of it.
- **Positive definite** means `xᵀAx > 0` for all nonzero `x`, equivalently all
  eigenvalues positive, equivalently all leading minors positive (Sylvester).
  It means convexity, so a unique optimum.
- **Cholesky** gives `A = LLᵀ` uniquely for SPD matrices, turns a linear solve
  into two triangular solves, and doubles as a positive-definiteness test.
- Covariance matrices and Hessians are symmetric positive definite, which is why
  so much of machine learning is numerically well behaved.

## Next

[40 — SVD and PCA](../part03_linear_algebra/40_svd_and_pca.md) fixes everything this lesson could only
work around. The spectral theorem needs symmetry; the SVD needs nothing. It
exists for **every** matrix, its singular values are always real and
non-negative and always sorted, its basis vectors are always orthogonal, and
its norm interpretation — how much each direction is stretched — is the single
cleanest picture of what a matrix does. PCA then falls out of it in a few
lines.
