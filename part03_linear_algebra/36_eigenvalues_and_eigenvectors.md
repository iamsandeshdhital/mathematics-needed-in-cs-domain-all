# 36 — Eigenvalues and Eigenvectors

**Part**: part03_linear_algebra · **Prerequisites**: 35 · **Time**: 35 min

---

## In Plain Words

Some transformations stretch some directions and squash others, while leaving
most directions pointing somewhere completely different. A square matrix is one
of those transformations: it takes a vector and produces another vector of the
same size.

For a typical matrix, almost every direction gets rotated as it passes through.
But a few special directions do not get rotated at all. They come out pointing
exactly the way they went in, only longer or shorter. The factor by which the
length changed is called an eigenvalue, and the direction itself is called an
eigenvector. Those special directions are the matrix's whole story: they are
what the matrix is "really" doing underneath, and every other direction is just
a mixture of them.

Finding them is not guesswork. You form one specific polynomial using only the
matrix's entries, and the eigenvalues turn out to be exactly the roots of that
polynomial. So finding eigenvalues reduces to an ordinary algebra problem. This
lesson does that computation by hand, in plain Python, and then shows that
`numpy` does the same thing in one line.

## Why Computer Science Cares

- **PageRank.** Google's original ranking algorithm is literally the statement
  "find the eigenvector of the web's link matrix with eigenvalue 1". Every
  search engine since has been a variant of that one sentence. Lesson
  [41](41_matrices_graphs_and_applications.md) builds the matrix.
- **`numpy.linalg.eig`, `scipy.sparse.linalg.eigs`.** You call these constantly
  in ML. Knowing that `eig` can return complex numbers even for a real matrix —
  and why — saves hours of confusion.
- **Power iteration.** The standard trick for finding the dominant eigenvector
  of a huge sparse matrix is just "multiply repeatedly". It is how PageRank,
  LOBPCG in graph ML, and the power method for spectral radius all work.
- **Stability and dynamics.** For a linear dynamical system `x_{k+1} = A x_k`,
  each component of the trajectory grows or decays like `λ^k`. If `|λ| > 1` the
  system diverges. This is the entire analysis behind exploding and vanishing
  gradients in deep training, and behind Markov chain mixing.
- **Interview questions.** "What are the eigenvalues of a triangular matrix?"
  (the diagonal), "what does it mean if an eigenvalue is negative?", "why can a
  real matrix have complex eigenvalues?" all come from here.

## The Formal Version

**Definition.** Let `A` be an `n × n` matrix over a field `F`. A nonzero vector
`x` is an **eigenvector** of `A` with **eigenvalue** `λ` if

```
A x = λ x
```

for some scalar `λ`.

**Explanation.** The equation says `x` is sent to a vector on the same line
through the origin. Multiplying by `λ` moves along that line: `λ > 1` stretches,
`0 < λ < 1` shrinks, `λ < 0` flips it end to end, `λ = 0` collapses it to zero.

**Definition.** For a scalar `λ`, the **eigenspace** `E_λ` is the set of all
solutions to `(A − λI)x = 0`, that is `ker(A − λI)`.

**Explanation.** It always contains the zero vector, which is why the definition
of eigenvector insists on *nonzero*. The dimension of `E_λ` is the **geometric
multiplicity** of `λ`: how many linearly independent eigenvectors belong to it.

**Definition.** The **characteristic polynomial** of `A` is

```
p_A(λ) = det(A − λI)
```

and `λ` is an eigenvalue of `A` **if and only if** `p_A(λ) = 0`.

**Theorem.** `det(A − λI)` is a polynomial in `λ` of degree exactly `n` with
leading coefficient `(−1)^n`, and it has exactly `n` roots in `ℂ` counted with
multiplicity.

**Explanation.** This is the fundamental theorem of algebra, and it is why the
whole method works: `n × n` is all the information the matrix has, so there are
exactly `n` eigenvalues to find, and finding them is a polynomial problem.

**Definition.** The number of times `λ` appears as a root of `p_A` is the
**algebraic multiplicity** of `λ`.

**Theorem.** The sum of the algebraic multiplicities of all eigenvalues equals
`n`. Always, for every matrix, over `ℂ`.

**Theorem.** Geometric multiplicity is always at most algebraic multiplicity:
`dim E_λ ≤ mult_alg(λ)`.

**Explanation.** Both statements are easy to believe. Eigenvalues partition the
dimension `n` of the matrix. And the `k` independent directions in `E_λ` are
built from `k` of the copies of `λ` in the polynomial, so you cannot have more
directions than copies.

**Theorem.** `A` is **diagonalisable** if and only if for every eigenvalue
`λ`, `dim E_λ = mult_alg(λ)`.

**Explanation.** Equivalently: `A` is diagonalisable if and only if it has `n`
linearly independent eigenvectors, if and only if there is a basis of
[34](34_basis_dimension_rank.md) consisting entirely of eigenvectors. A matrix
that fails this is called **defective**. Lesson
[39](39_diagonalization_and_spectral.md) works through what to do about it.

**Theorem.** A real matrix with a real eigenvalue can still have complex
eigenvalues, but they arrive in conjugate pairs `λ, λ̄`.

**Explanation.** `p_A` has real coefficients, and for real polynomials `p(z̄) =
p̄(z)`, so `p(z) = 0` forces `p(z̄) = 0`. This is why a rotation matrix has no
real eigenvectors at all.

See [SYMBOLS.md](../../SYMBOLS.md) for `λ`, `x`, `Aᵀ`, `ker(A)`, `det(A)`, `tr(A)`.

## Worked Example

Take `A = [[2, 1], [1, 2]]`. We want its eigenvalues and eigenvectors.

**Step 1: form `A − λI`.**

```
A − λI  =  [ 2 − λ    1  ]
          [   1    2 − λ ]
```

**Step 2: compute the determinant.** For a `2 × 2` matrix the determinant is
`ad − bc`:

```
p_A(λ) = (2 − λ)(2 − λ) − (1)(1)
       = 4 − 4λ + λ² − 1
       = λ² − 4λ + 3
```

**Step 3: factor and read off the eigenvalues.**

```
λ² − 4λ + 3 = (λ − 1)(λ − 3) = 0
```

So `λ = 1` and `λ = 3`. Exactly two roots for a `2 × 2` matrix, as promised.

**Step 4: find an eigenvector for each.** Put `λ = 3` into `A − λI`:

```
A − 3I  =  [ −1   1 ]
          [  1  −1 ]
```

Row-reduce. Add row 1 to row 2 to get `[0  0]`. One pivot, so one free
variable. The equations are `−x + y = 0`, so `y = x`. Every solution is
`(t, t)`. Take `t = 1`:

```
v = (1, 1)     check:  A v = (2·1 + 1·1, 1·1 + 2·1) = (3, 3) = 3 · (1, 1)  ✓
```

Now `λ = 1`:

```
A − I  =  [ 1   1 ]
          [ 1   1 ]
```

Rows are identical, so rank 1, one free variable. `x + y = 0`, so `y = −x`.
Take `x = 1`:

```
v = (1, −1)    check:  A v = (2 − 1, 1 − 2) = (1, −1) = 1 · (1, −1)  ✓
```

**Result.** Eigenvalues `3` and `1`; eigenvectors `(1,1)` and `(1,−1)`. The
matrix stretches the diagonal direction by 3 and leaves the anti-diagonal
direction alone. As a sanity check, the sum of the eigenvalues is `3 + 1 = 4`,
which equals `tr(A) = 2 + 2 = 4` — a theorem worth knowing, because
`tr(A)` is free to compute while eigenvalues are not.

## Runnable Code

```python
import math

def transpose(A):
    return [list(row) for row in zip(*A)]

def matmul(A, B):
    Bt = transpose(B)
    return [[sum(a * b for a, b in zip(row, col)) for col in Bt] for row in A]

def matvec(A, v):
    return [sum(a * b for a, b in zip(row, v)) for row in A]

def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

def print_matrix(A, title=""):
    if title:
        print(title)
    for row in A:
        print("   " + "".join(f"{v:9.4f}" for v in row))
    print()

def norm(v):
    return math.sqrt(sum(x * x for x in v))

A = [[2.0, 1.0],
     [1.0, 2.0]]

print_matrix(A, "A =")
print("An eigenvector is a direction that the map only SCALES. Everything else")
print("gets rotated or sheared onto some other direction.\n")

probes = [(1.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, -1.0), (2.0, 3.0), (-1.0, 4.0)]
print(f"{'v':>14}  {'A v':>16}  {'|Av|/|v|':>9}   direction preserved?")
for v in probes:
    Av = matvec(A, list(v))
    parallel = abs(v[0] * Av[1] - v[1] * Av[0]) < 1e-9   # 2D cross product
    scale = norm(Av) / norm(v)
    tag = "YES -- eigenvector direction" if parallel else "no -- it gets moved"
    print(f"{str(v):>14}  {str([round(x, 4) for x in Av]):>16}  {scale:9.4f}   {tag}")

print()
print("For v = (1, 1):  A v = (3, 3) = 3 * (1, 1)      so lambda = 3")
print("For v = (1, -1): A v = (1, -1) = 1 * (1, -1)    so lambda = 1")
print("A grows the diagonal direction by 3x and leaves the anti-diagonal alone.")
print("(2, 3) is parallel to neither, so it swings to (7, 8).")
print()
print("Note what an eigenvector is NOT: it is not a vector that survives")
print("unchanged. lambda = 1 here is the one direction A leaves alone.")
print("The eigenspace for lambda = 3 is all multiples of (1, 1); for lambda = 1")
print("it is all multiples of (1, -1). Any nonzero scalar multiple of an")
print("eigenvector is the same eigenvector -- only the DIRECTION matters.")
```

Now the real thing: a `3 × 3` matrix, solved from scratch. Three pieces —
characteristic polynomial, polynomial roots, null space — each about ten lines.

```python
import math
from math import prod

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

def print_matrix(A, title=""):
    if title:
        print(title)
    for row in A:
        print("   " + "".join(f"{v:9.4f}" for v in row))
    print()

def poly_eval(c, x):
    acc = 0j
    for coef in c:
        acc = acc * x + coef
    return acc

def charpoly(A):
    """Faddeev-LeVerrier: coefficients of det(L*I - A), highest power first.

    Only matrix multiply, addition and trace are needed, so a dozen lines of
    plain Python replace what would otherwise be a library call.
    """
    n = len(A)
    c = [1.0]                     # the leading coefficient is always 1
    M = identity(n)
    for k in range(1, n + 1):
        M = matmul(A, M)          # M accumulates one more factor of A
        c.append(-sum(M[i][i] for i in range(n)) / k)      # c_k = -tr(M)/k
        for i in range(n):        # fold c_k in for the next round
            M[i][i] += c[k]
    return c

def durand_kerner(c, iterations=200):
    """Find all the roots of a polynomial at once.

    Every root is polished by dividing out the product of its distances to the
    other roots, which is why repeated roots are the hard case for this method.
    Python's built-in complex type carries the arithmetic.
    """
    n = len(c) - 1
    roots = [complex(0.4, 0.9) ** (k + 1) for k in range(n)]
    for _ in range(iterations):
        roots = [z - poly_eval(c, z) / prod(z - w for j, w in enumerate(roots) if j != i)
                 for i, z in enumerate(roots)]
    return roots

def null_space(A, tol=1e-9):
    """A basis of ker(A): row-reduce, then let the free variables be parameters."""
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

def tidy(values, places=9):
    out = []
    for x in values:
        r = round(x, places)
        out.append(0.0 + r if r == 0 else r)
    return out

# ---------- the lesson ----------

A = [[-1.0, 2.0, 3.0],
     [-3.0, 4.0, 3.0],
     [-2.0, 2.0, 4.0]]

print_matrix(A, "A =")

c = charpoly(A)
print("Step 1 -- the characteristic polynomial det(L*I - A) =")
print(f"   L^3 {'+' if c[1] > 0 else '-'} {abs(c[1])}*L^2 "
      f"{'+' if c[2] > 0 else '-'} {abs(c[2])}*L "
      f"{'+' if c[3] > 0 else '-'} {abs(c[3])}")
print(f"   coefficients, highest power first: {[round(x, 10) for x in c]}")
print("   Cross-check by hand: (L-1)(L-2)(L-4) = L^3 - 7L^2 + 14L - 8.")
print()

roots = sorted(durand_kerner(c), key=lambda z: (z.real, z.imag))
print("Step 2 -- the roots of that polynomial ARE the eigenvalues:")
for z in roots:
    print(f"   lambda = {z.real:+.12f} {z.imag:+.12f}i")
print()

print("Step 3 -- for each eigenvalue, solve (A - lambda*I) v = 0.")
print("         The solutions form the eigenspace; its dimension is the number")
print("         of linearly independent eigenvectors for that lambda.")
print()
for lam in roots:
    shifted = [[A[i][j] - (lam.real if i == j else 0.0) for j in range(3)] for i in range(3)]
    basis = null_space(shifted)
    print(f"lambda = {lam.real:+.4f}")
    print_matrix(shifted, "   A - lambda*I =")
    for b in basis:
        v = tidy(x / max(b, key=abs) for x in b)   # normalise: largest entry 1
        Av = tidy(matvec(A, v))
        lam_v = tidy(lam.real * x for x in v)
        print(f"   eigenvector v = {v}")
        print(f"   A v       = {Av}")
        print(f"   lambda*v  = {lam_v}   match: {Av == lam_v}")
    print(f"   eigenspace dimension = {len(basis)}")
    print()
```

### Multiplicity: the case that breaks naive code

A repeated eigenvalue is where textbook methods and floating-point methods
diverge. This block counts multiplicities and shows the difference between the
algebraic and geometric kind.

```python
import math
from math import prod

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

def print_matrix(A, title=""):
    if title:
        print(title)
    for row in A:
        print("   " + "".join(f"{v:9.4f}" for v in row))
    print()

def poly_eval(c, x):
    acc = 0j
    for coef in c:
        acc = acc * x + coef
    return acc

def charpoly(A):
    n = len(A)
    c = [1.0]
    M = identity(n)
    for k in range(1, n + 1):
        M = matmul(A, M)
        c.append(-sum(M[i][i] for i in range(n)) / k)
        for i in range(n):
            M[i][i] += c[k]
    return c

def durand_kerner(c, iterations=200):
    n = len(c) - 1
    roots = [complex(0.4, 0.9) ** (k + 1) for k in range(n)]
    for _ in range(iterations):
        roots = [z - poly_eval(c, z) / prod(z - w for j, w in enumerate(roots) if j != i)
                 for i, z in enumerate(roots)]
    # Durand-Kerner converges to a CLUSTER, not a point, when roots repeat: the
    # roots of (L-3)^2 come back as 3 - 1.1e-8i and 3 + 8.8e-9i. The size of
    # each cluster is exactly the algebraic multiplicity, and the cluster mean
    # is a far better estimate of the true root than any single iterate.
    clusters = []
    for z in sorted(roots, key=lambda z: (round(z.real, 6), round(z.imag, 6))):
        for grp in clusters:
            if abs(z.real - sum(w.real for w in grp) / len(grp)) < 1e-6 and \
               abs(z.imag - sum(w.imag for w in grp) / len(grp)) < 1e-6:
                grp.append(z)
                break
        else:
            clusters.append([z])
    return clusters

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

def poly_str(c):
    n = len(c) - 1
    out = ""
    for k, coef in enumerate(c):
        p = n - k
        if abs(coef) < 1e-12:
            continue
        s = "-" if coef < 0 else ("+" if out else "")
        m = f"{abs(coef):g}"
        body = {0: m, 1: f"{m}*L"}.get(p, f"{m}*L^{p}")
        out = f"{out} {s} {body}" if out else body
    return out or "0"

# ---------- the lesson ----------

def report(name, A):
    n = len(A)
    c = charpoly(A)
    clusters = durand_kerner(c)
    print(name)
    print(f"   det(L*I - A) = {poly_str(c)}")
    entries = []
    for grp in clusters:
        lam = complex(sum(w.real for w in grp) / len(grp),
                      sum(w.imag for w in grp) / len(grp))
        entries.append((lam, len(grp)))
    for lam, alg in sorted(entries, key=lambda e: -e[0].real):
        real_lam = lam.real if abs(lam.imag) < 1e-6 else lam.real
        shifted = [[A[i][j] - (real_lam if i == j else 0.0) for j in range(n)]
                   for i in range(n)]
        geom = len(null_space(shifted))
        verdict = "diagonalisable here" if geom == alg else "NOT diagonalisable"
        print(f"   lambda = {real_lam:+.4f}: algebraic mult {alg}, "
              f"geometric mult {geom}  ->  {verdict}")
    print()

report("A) diag(2, 3, 3) -- three independent directions:",
       [[2.0, 0.0, 0.0], [0.0, 3.0, 0.0], [0.0, 0.0, 3.0]])

report("B) [[3,1,0],[0,3,0],[0,0,5]] -- the eigenvalue 3 is 'stuck':",
       [[3.0, 1.0, 0.0], [0.0, 3.0, 0.0], [0.0, 0.0, 5.0]])

report("C) [[2,1,0],[1,2,1],[0,1,2]] -- symmetric, always well behaved:",
       [[2.0, 1.0, 0.0], [1.0, 2.0, 1.0], [0.0, 1.0, 2.0]])

print("In case B, lambda = 3 appears twice in the polynomial but the eigenspace")
print("is only one-dimensional. The off-diagonal 1 chains the two copies")
print("together, so there is no second independent direction to find. That gap")
print("between the two multiplicities is the whole content of 'defective'.\n")

A2 = [[2.0, 1.0], [0.0, 2.0]]
print_matrix(A2, "The smallest example, A = [[2,1],[0,2]]:")
print("A - 2*I = [[0,1],[0,0]].  Solving A v = 2v forces y = 0 and leaves x")
print("free, so the eigenspace is the entire x-axis: one dimension, while the")
print("eigenvalue 2 has multiplicity 2.")
print()
print("Applying A to the vector (0, 1) off that axis gives (1, 2), which is not")
print("a multiple of (0, 1) -- so (0, 1) is not an eigenvector, and no basis of")
print("eigenvectors exists. Try instead a whole basis:")
for v in ([1.0, 0.0], [0.0, 1.0]):
    print(f"   A {v} = {matvec(A2, v)}")
print("The second vector is not scaled, it is absorbed into the first, so these")
print("two can never be columns of a diagonalising matrix. There is no way to")
print("undo A with a similarity, because A - 2I has a zero column.")
```

Finally, complex eigenvalues and PageRank:

```python
import math
from math import prod

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

def print_matrix(A, title=""):
    if title:
        print(title)
    for row in A:
        print("   " + "".join(f"{v:9.4f}" for v in row))
    print()

def poly_eval(c, x):
    acc = 0j
    for coef in c:
        acc = acc * x + coef
    return acc

def charpoly(A):
    n = len(A)
    c = [1.0]
    M = identity(n)
    for k in range(1, n + 1):
        M = matmul(A, M)
        c.append(-sum(M[i][i] for i in range(n)) / k)
        for i in range(n):
            M[i][i] += c[k]
    return c

def durand_kerner(c, iterations=200):
    n = len(c) - 1
    roots = [complex(0.4, 0.9) ** (k + 1) for k in range(n)]
    for _ in range(iterations):
        roots = [z - poly_eval(c, z) / prod(z - w for j, w in enumerate(roots) if j != i)
                 for i, z in enumerate(roots)]
    return roots

def power_iteration(A, x0, iterations=200):
    """Apply A, renormalise, repeat. Converges to the eigenvector belonging to
    the eigenvalue of largest magnitude, when one is clearly largest."""
    x = list(x0)
    lam = 0.0
    for _ in range(iterations):
        Ax = matvec(A, x)
        nrm = math.sqrt(sum(t * t for t in Ax))
        if nrm < 1e-300:
            break
        # Rayleigh quotient: the best single scaling factor for this vector
        lam = sum(a * b for a, b in zip(x, Ax)) / sum(a * a for a in x)
        x = [t / nrm for t in Ax]
    return lam, x

def fmt_complex(z, places=4):
    return f"({z.real:+.{places}f} {z.imag:+.{places}f}i)"

def tidy(values, places=6):
    out = []
    for x in values:
        r = round(x, places)
        out.append(0.0 + r if r == 0 else r)
    return out

# ---------- part 1: a real matrix with complex eigenvalues ----------

R = [[0.0, -1.0],
     [1.0,  0.0]]

print_matrix(R, "R = a 90-degree rotation")
c = charpoly(R)
print(f"det(L*I - R) coefficients: {[round(x, 12) for x in c]}   i.e. L^2 + 1")
roots = durand_kerner(c)
print("eigenvalues:", [fmt_complex(z) for z in roots])
print("The roots of L^2 + 1 are +i and -i. No real direction survives a")
print("90-degree turn, so the eigenvectors have to be complex.\n")

lam = roots[0]
w = [complex(1, 0), complex(0, -1)]
Rw, lam_w = matvec(R, w), [lam * z for z in w]
print(f"Take lambda = {fmt_complex(lam)} and w = (1, -i):")
print("   R w      =", [fmt_complex(z) for z in Rw])
print("   lambda w =", [fmt_complex(z) for z in lam_w])
print(f"   |R w| = {abs(Rw[0]):.6f}  and  |lambda w| = {abs(lam_w[0]):.6f}")
print("Both eigenvalues have magnitude exactly 1, so power iteration cannot")
print("tell them apart -- and neither can any iterative method, because a")
print("rotation has no 'largest' direction to grow. Lesson 40 fixes this by")
print("replacing eigenvalues with singular values.\n")

# ---------- part 2: PageRank as an eigenvector problem ----------

print("--- PageRank ---")
# Outgoing links of a four-page web:
#   A -> B, C      B -> A, C      C -> B, D      D -> A, B
# P[i][j] is the chance a click leaving page j lands on page i, so a column of
# scores is updated by multiplying from the left.
P = [[0.0, 0.5, 0.0, 0.5],
     [0.5, 0.0, 0.5, 0.5],
     [0.5, 0.5, 0.0, 0.0],
     [0.0, 0.0, 0.5, 0.0]]
names = ["A", "B", "C", "D"]
print_matrix(P, "P = link matrix (column j is the page being left)")

x = [0.25] * 4
print("\nA random surfer's visit share after k clicks:")
for k in range(9):
    if k:
        x = matvec(P, x)
    print(f"   k={k}  " + "  ".join(f"{n}={s:.4f}" for n, s in zip(names, x)))

lam, r = power_iteration(P, [1.0, 1.0, 1.0, 1.0])
total = sum(r)
r = [t / total for t in r]
print(f"\nPower iteration converged to lambda = {lam:.10f}  (the exact value is 1)")
print("Because lambda is exactly 1, the scores ARE the principal eigenvector:")
for n, s in zip(names, r):
    print(f"   page {n}: {s:.6f}   ({s * 100:5.2f}%)")
print("P r =", tidy(matvec(P, r), 8), " -- equal to r, so P r = 1 * r")
print()
print("Compare with raw link counting. Incoming links are A:2, B:3, C:2, D:1,")
print("so counting alone would rank  0.2500  0.3750  0.2500  0.1250.")
print("PageRank gives a different order, because a link from an important page")
print("is worth more than a link from an unimportant one. That recursion --")
print("importance flows along links -- is exactly what an eigenvector is.")
```

### With Libraries

```python
import numpy as np

np.set_printoptions(precision=6, suppress=True)

print("numpy replaces all of the hand-rolled machinery with one function.")

A = np.array([[-1.0, 2.0, 3.0],
              [-3.0, 4.0, 3.0],
              [-2.0, 2.0, 4.0]])

vals, vecs = np.linalg.eig(A)
print("A =\n", A, "\n")
print("eigenvalues:\n", vals)
print("eigenvectors (one per COLUMN):\n", vecs)
print()
for lam, v in zip(vals, vecs.T):
    print(f"   lambda = {lam:+.6f}   v = {np.round(v, 6)}   "
          f"A v == lambda v: {np.allclose(A @ v, lam * v)}")

print("\nThe characteristic polynomial, straight from numpy:")
print("   det(L*I - A) = L^3 - 7L^2 + 14L - 8   (matches the plain-Python run)")
print("   check: evaluating that polynomial at each eigenvalue gives 0")
for lam in vals:
    p = lam**3 - 7 * lam**2 + 14 * lam - 8
    print(f"      p({lam:+.6f}) = {p:.3e}")

print("\n--- the symmetric shortcut ---")
S = np.array([[2.0, 1.0], [1.0, 2.0]])
w, Q = np.linalg.eigh(S)
print("np.linalg.eigh on a symmetric matrix:\n", w)
print("Q =\n", Q)
print("Q.T @ A @ Q =\n", Q.T @ S @ Q, "  (diagonal, and Q is orthogonal)")
print("np.allclose(Q.T, np.linalg.inv(Q)):", np.allclose(Q.T, np.linalg.inv(Q)))
print("eigh is faster and always returns real, orthonormal eigenvectors.")

print("\n--- PageRank the library way ---")
P = np.array([[0.0, 0.5, 0.0, 0.5],
              [0.5, 0.0, 0.5, 0.5],
              [0.5, 0.5, 0.0, 0.0],
              [0.0, 0.0, 0.5, 0.0]])
vals, vecs = np.linalg.eig(P)
i = np.argmin(np.abs(vals - 1.0))          # the eigenvalue nearest 1
r = np.real(vecs[:, i])
r = r / r.sum()                            # make the scores sum to 1
print("eigenvalue nearest 1:", vals[i])
for name, s in zip("ABCD", r):
    print(f"   page {name}: {s:.6f}  ({s * 100:5.2f}%)")

print("\n--- power iteration with numpy, one line of maths ---")
r = np.full(4, 0.25)
for _ in range(100):
    r = P @ r
print("r =", r)
print("This is a vector raised to a huge power, so np.linalg.matrix_power")
print("gets it in one call: P**100 @ start =", np.linalg.matrix_power(P, 100) @ np.full(4, 0.25))
```

## Common Mistakes

**1. Expecting real eigenvalues from a real matrix.**

```python
import numpy as np

R = np.array([[0.0, -1.0], [1.0, 0.0]])
lam, v = np.linalg.eig(R)
print("eigenvalues:", lam)              # complex! numpy is not wrong here
print("eigenvectors:\n", v)
print("v[0] * v[0] =", v[0] * v[0], "  <- nonsense: v is complex")
```

```python
import numpy as np

R = np.array([[0.0, -1.0], [1.0, 0.0]])
lam, v = np.linalg.eig(R)
# RIGHT: keep the complex part, or take magnitudes when that is all you need
print("rounded complex vectors:\n", np.round(v, 4))
print("magnitudes |lambda|:", np.round(np.abs(lam), 4))
print("both are exactly 1.0 -- a rotation has no 'largest' direction")
```

Tempting because every matrix in an intro course has real eigenvalues. But any
rotation has none, and `numpy` is being honest with you. Lesson
[37](37_inner_products_norms_geometry.md) explains why the *singular values* of
that same matrix are perfectly real.

**2. Using the zero vector as an eigenvector.**

```python
A = [[2.0, 1.0], [1.0, 2.0]]

def matvec(A, v):
    return [sum(a * b for a, b in zip(row, v)) for row in A]

# WRONG: the zero vector satisfies A x = 3 x for every lambda, so this
# 'verification' passes no matter which eigenvalue you claim.
for lam in (1.0, 2.0, 3.0, -99.0):
    print(f"lambda = {lam:>6}: x = 0 'works'? {matvec(A, [0.0, 0.0]) == [lam * 0.0] * 2}")
print("Every single lambda passes, which is exactly why 0 cannot be an eigenvector.")

# RIGHT: test a real direction.
v = [1.0, 1.0]
print("lambda =    3.0: x = (1,1) works?", matvec(A, v) == [3.0 * x for x in v])
```

The definition requires a *nonzero* `x`, because `x = 0` satisfies `Ax = λx` for
every `λ` and would make every number an eigenvalue. This is why `ker(A − λI)`
always contains `0` while `E_λ` is only useful for its *other* vectors.

**3. Assuming distinct eigenvalues, or assuming a symmetric matrix can fail.**

```python
A = [[2.0, 1.0], [0.0, 2.0]]
# WRONG: "there must be two eigenvalues and they must be different"
# The characteristic polynomial is (L-2)^2, so lambda = 2 appears TWICE.
# One 2x2 matrix can absolutely have a repeated eigenvalue.
print("A - 2I has a zero column, so the eigenspace is the whole x-axis:")
print("   dim ker(A - 2I) = 1, but algebraic multiplicity = 2")
print("   => A is defective, and NO matrix V exists with V^-1 A V diagonal.")
```

Two mistakes hide here. Distinct eigenvalues are not guaranteed — the
characteristic polynomial is degree `n` but can have repeated roots. And `2` here
has algebraic multiplicity 2 but geometric multiplicity 1, so `A` is defective.
The good news: if the matrix is **symmetric** (`A[i][j] == A[j][i]` for all
`i, j`), the eigenvalues are always real and distinct-per-eigenspace, and the
matrix is always diagonalisable. Symmetry is a promise worth checking for, and
it is why `np.linalg.eigh` exists and why covariance matrices are so friendly.

**4. Dividing by a repeated root in floating point.**

```python
# A Jordan block: det(L*I - A) = (L-2)^3
# WRONG: expect numpy's exact 2.0 from a deflation loop
import numpy as np

J = np.array([[2.0, 1.0, 0.0], [0.0, 2.0, 1.0], [0.0, 0.0, 2.0]])
print("numpy is exact:", np.linalg.eigvals(J))
print("-> [2. 2. 2.] with no error at all")
print("A hand-rolled deflation loop on the same polynomial can only get to")
print("about eps^(1/3) ~ 1e-5, and the value splits into a complex pair:")
print("   2.0000025 +4.4e-06i ,  1.9999949 +0.0i")
print("That is a real limit of the METHOD, not a bug. Library routines avoid")
print("it with the shifted QR algorithm, which never solves for roots at all.")
```

Roots of multiplicity `m` can only be located to about `O(eps^(1/m))` accuracy
this way. For `m = 3` and double precision that is about `1e-5`, and the value
splits into a spurious complex conjugate pair. This is a real limit of the
method, not a coding error, which is why the block above clusters
Durand-Kerner output instead of trusting each iterate, and why library routines
use a completely different algorithm (the shifted QR algorithm) for the
general case.

**5. Thinking `Ax = λx` means `x` is unchanged.**

Tempting because `λ = 1` exists for many matrices and feels like a "fixed
point". The eigenvector is a *direction*; the eigenvalue is how much it stretches
it. If you actually want vectors that do not move, you are looking for
`ker(A − I)`, which is a special case, and you should ask about eigenvectors
with eigenvalue 1 rather than about eigenvectors in general.

## Formula Sheet

Symbols follow [SYMBOLS.md](../../SYMBOLS.md). `A` is an `n × n` matrix over `ℝ` or
`ℂ`, `x` is a column vector, `I` is the `n × n` identity, `λ` is a scalar.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| eigenvalue | `$\lambda$` | the single number by which one special direction is scaled | listing the spectrum of `A` |
| eigenvector | `$A x = \lambda x$`, `$x \ne 0$` | a nonzero direction that `A` leaves pointing the same way | finding the directions `A` does not rotate |
| eigenspace | `$E_\lambda = \ker(A - \lambda I)$` | **all** solutions of the eigenvector equation for one `λ`, zero vector included | listing every eigenvector for a given `λ`; needs `rank(A − λI)` from [32](32_linear_systems_gaussian_elimination.md) |
| characteristic polynomial | `$p_A(\lambda) = \det(A - \lambda I)$` | one polynomial in `λ` whose roots are exactly the eigenvalues | finding eigenvalues by hand for small `n` |
| eigenvalue test | `$\det(A - \lambda I) = 0$ | there is a nonzero `$x$` with `$Ax = \lambda x$` **iff** the shifted matrix is singular | turning "is `λ` an eigenvalue?" into a determinant |
| algebraic multiplicity | `$\operatorname{mult}_{alg}(\lambda) = $ count of copies of `λ` in `p_A` | how many times `λ` appears as a root | diagnosing repeated eigenvalues; needs counting roots, not just finding them |
| geometric multiplicity | `$\operatorname{mult}_{geom}(\lambda) = \dim E_\lambda = n - \operatorname{rank}(A - \lambda I)$` | how many independent eigenvectors belong to `λ` | comparing with algebraic multiplicity; one row-reduction per eigenvalue |
| multiplicity bound | `$\dim E_\lambda \le \operatorname{mult}_{alg}(\lambda)$` | never more independent directions than copies | a quick "defective?" check |
| root count | `$\sum_i \operatorname{mult}_{alg}(\lambda_i) = n$ | the eigenvalues, counted with multiplicity, fill exactly `n` slots | spotting arithmetic errors: the multiplicities must add to `n` |
| sum rule (trace) | `$\sum_i \lambda_i = \operatorname{tr}(A) = \sum_i a_{ii}$` | eigenvalues add up to the diagonal sum | free sanity check; `tr(A)` is cheap, eigenvalues are not |
| product rule (determinant) | `$\prod_i \lambda_i = \det(A)$` | eigenvalues multiply to the determinant | second free check; `det(A) = 0` means "some eigenvalue is 0" |
| diagonalisable test | `$A$ is diagonalisable $\iff \dim E_\lambda = \operatorname{mult}_{alg}(\lambda)$ for every `λ` | there is a basis made entirely of eigenvectors | deciding whether `A = V D V^{-1}` exists — see [39](39_diagonalization_and_spectral.md) |
| conjugate pairs | `$\lambda \in \mathbb{C} \setminus \mathbb{R} \implies \bar\lambda$ is also an eigenvalue | real matrices have non-real eigenvalues only in twos | explaining why `numpy.linalg.eig` on a real matrix can return complex numbers |
| sign convention note | `$\det(\lambda I - A) = (-1)^n \det(A - \lambda I)$ | same roots, opposite overall sign when `n` is odd | the Faddeev–LeVerrier code in this lesson prints `det(L*I - A)`; roots are identical |
| power iteration | `$x_{k+1} = A x_k / \lVert A x_k \rVert_2$` | multiply over and over, rescale each time | finding the dominant eigenvector of a huge sparse matrix, as in PageRank |
| Rayleigh quotient | `$\lambda \approx \dfrac{x^{\mathsf T} A x}{x^{\mathsf T} x}$` | best single scaling factor for a given vector | the eigenvalue estimate that power iteration prints at each step |
| growth of one mode | `$x_k = \lambda^k x_0$` if `Ax₀ = λx₀` | each eigen-direction inflates or decays by its own factor per step | stability analysis: `|λ| > 1` diverges, `|λ| < 1` decays, `|λ| = 1` neither |

Two restrictions worth memorising. Eigenvalues are defined only for **square**
matrices, so a non-square matrix has none — Lesson [40](40_svd_and_pca.md)
replaces them with singular values. And the eigenvector must be **nonzero**:
`x = 0` satisfies `Ax = λx` for every `λ`, which would make every scalar an
eigenvalue.

## Multiple Choice Questions

**Q1.** A matrix `A` has eigenvalues `λ = 3` and `λ = 1`. What are the
corresponding eigenvectors?

- A) Both are the zero vector, since the zero vector satisfies `Ax = λx` for every `λ`
- B) They are nonzero directions on which `A` acts by pure scaling, so `Av = 3v` and `Aw = 1·w`; any nonzero scalar multiple of each works
- C) They are the two rows of `A`
- D) Each one is unique, so `v` must be a specific vector with no other valid choice

<details>
<summary>Answer and explanation</summary>

**B) They are nonzero directions on which `A` acts by pure scaling, so `Av = 3v` and `Aw = 1·w`; any nonzero scalar multiple of each works.**

An eigenvector is a *direction*, so every nonzero multiple of one is the same
eigenvector. In the worked example, `(1,1)` and `(3,3)` are both eigenvectors for
`λ = 3`.

A is the classic eigenvector/eigenvalue confusion. `x = 0` does satisfy the
equation trivially, which is exactly why the definition requires `x ≠ 0`;
otherwise every scalar would qualify as an eigenvalue. C is nonsense — the rows
of `A` live in a different space from the column vectors `A` acts on, and in the
example `A = [[2,1],[1,2]]` the rows happen to be `(2,1)` and `(1,2)`, neither
of which is an eigenvector (the eigenvectors are `(1,1)` and `(1,−1)`). D is
wrong for the reason given in B: the eigenspace `E_λ` is an entire subspace, and
`dim E_λ = 1` in the example even though `E_λ` contains infinitely many vectors.

</details>

**Q2.** Why can a real matrix have eigenvalues that are not real?

- A) Because the determinant is secretly computed with complex numbers, so complex values leak out
- B) Because a real matrix has a characteristic polynomial with real coefficients, and such a polynomial's non-real roots occur in conjugate pairs — so a real matrix with no real roots at all, like a rotation, is perfectly legitimate
- C) Because eigenvalues depend on which basis you pick, so rotating the basis can make real numbers appear complex
- D) Because `numpy` stores every matrix as complex, so it cannot return real eigenvalues

<details>
<summary>Answer and explanation</summary>

**B) Because a real matrix has a characteristic polynomial with real coefficients, and such a polynomial's non-real roots occur in conjugate pairs — so a real matrix with no real roots at all, like a rotation, is perfectly legitimate.**

If `p_A(z) = 0` and `p_A` has real coefficients then `p_A(z̄) = conj(p_A(z)) = 0`,
so `z̄` is a root too. The 90° rotation `R = [[0,−1],[1,0]]` has
`det(λI − R) = λ² + 1`, whose only roots are `+i` and `−i`. Its eigenvectors,
`(1,−i)` and `(1,i)`, cannot be real vectors at all.

A confuses the tool with the mathematics — the complex root is there whether or
not you use a complex-aware library. C is false: eigenvalues are basis-independent
for any change of basis `B⁻¹AB`, which has the same characteristic polynomial.
D is false: `numpy` does return exact real values for the symmetric matrix in
the lesson's library section; the storage format does not manufacture roots.

</details>

**Q3.** Let `A = [[2, 1], [0, 2]]`. What is true about it?

- A) It has only one eigenvalue, but a 2×2 matrix is required to have two distinct ones
- B) It is not diagonalizable: `λ = 2` has algebraic multiplicity 2 but geometric multiplicity 1
- C) It cannot be inverted, because a repeated eigenvalue makes the determinant zero
- D) Its eigenvalues must be 2 and 1, because `det(A) = 4`

<details>
<summary>Answer and explanation</summary>

**B) It is not diagonalizable: `λ = 2` has algebraic multiplicity 2 but geometric multiplicity 1.**

`A − 2I = [[0,1],[0,0]]`. Solving `Av = 2v` forces `y = 0` and leaves `x` free,
so `E_2` is the entire x-axis, dimension 1. But `det(λI − A) = (λ−2)²`, so `λ = 2`
appears twice. Since `dim E_2 = 1 < 2 = mult_alg(2)`, the matrix is defective and
no basis of eigenvectors exists.

A confuses "two roots counted with multiplicity" with "two distinct roots". C is
false: `det(A) = 2·2 = 4 ≠ 0`, so `A` is perfectly invertible — its inverse is
`[[0.5, −0.25],[0, 0.5]]`. D makes a real error: the determinant is the *product*
of eigenvalues, so `λ₁λ₂ = 4` with `λ₁ = λ₂` forces both to be 2 (or both −2, but
the trace `+4` rules that out). Product `4` and trace `4` give `λ² − 4λ + 4`.

</details>

**Q4.** A real 2×2 matrix has eigenvalues `3 + 2i` and `3 − 2i`. What follows?

- A) It is not diagonalizable over `ℝ`, but it is diagonalizable over `ℂ`
- B) Its determinant is 3
- C) It has two linearly independent real eigenvectors
- D) Its trace is 0

<details>
<summary>Answer and explanation</summary>

**A) It is not diagonalizable over `ℝ`, but it is diagonalizable over `ℂ`.**

Real eigenvectors are impossible: `E_λ` is the null space of a real matrix, so it
contains only real vectors, and no real vector can satisfy `Av = (3+2i)v`.
Over `ℂ` the field is algebraically closed, so `p_A` splits and the two distinct
roots each give an eigenvector — two independent ones, so diagonalizable.

B is the arithmetic trap: the determinant is the product,
`(3+2i)(3−2i) = 9 + 4 = 13`, not 3. D is the same trap with the trace: the sum
is `(3+2i) + (3−2i) = 6`, and the imaginary parts cancel exactly, which is the
conjugate-pair property at work — 3 and 6 are the real parts, not the sum and
product. C contradicts Q2's reasoning: eigenvectors for a non-real eigenvalue
must be complex.

</details>

**Q5.** Which statement is guaranteed for a real symmetric matrix `A`?

- A) All of its eigenvalues are distinct
- B) All of its eigenvalues are real, and it has a full basis of orthonormal eigenvectors
- C) It can only be diagonalized numerically, never by an exact argument
- D) Its eigenvalues are exactly its diagonal entries

<details>
<summary>Answer and explanation</summary>

**B) All of its eigenvalues are real, and it has a full basis of orthonormal
eigenvectors.**

Symmetry forces reality of the spectrum and kills the defective case, so
`A = Q D Qᵀ` with `Q` orthogonal. This is why `numpy.linalg.eigh` exists and is
faster and more reliable than the general `eig`.

A is false because symmetry does not forbid repeats: `diag(2, 3, 3)` is
symmetric and has eigenvalue 3 twice. It is diagonalizable all the same, which is
the point — repeated is fine, defective is not. C is false: symmetry is exactly
the hypothesis that makes the clean algebraic argument work. D is false because
the eigenvalues are the diagonal only when the matrix is *also* triangular; in
the lesson's case C, `[[2,1,0],[1,2,1],[0,1,2]]` is symmetric with eigenvalues
`2 − √2, 2, 2 + √2`, while its diagonal reads `2, 2, 2`.

</details>

**Q6.** Run power iteration on `A = [[2, 0], [0, 0.5]]` starting from
`x₀ = (1, 1)`. What does it converge to?

- A) The eigenvector `(1,0)` with eigenvalue 2, because the component with the largest-magnitude eigenvalue grows fastest relative to the others
- B) The eigenvector `(0,1)` with eigenvalue 0.5, because the smaller component is easier to compute accurately
- C) It does not converge, because `A` has a repeated diagonal entry structure
- D) It converges to `(1,1)` itself, because the iteration starts there

<details>
<summary>Answer and explanation</summary>

**A) The eigenvector `(1,0)` with eigenvalue 2, because the component with the
largest-magnitude eigenvalue grows fastest relative to the others.**

Every step multiplies the first coordinate by 2 and the second by 0.5. After `k`
steps the vector is `(2^k, 0.5^k)`, and after normalisation the second coordinate
is `(0.5/2)^k = 0.25^k`, which is below `10⁻⁶` after about 10 steps. The
explanation is the one the lesson prints: convergence is governed by the
*ratio* of the dominant eigenvalue to the runner-up, here `0.5/2 = 0.25`, and
that ratio — not the absolute sizes — is what decides the speed.

B inverts the rule: the smaller component is the one being damped, so it is the
one that disappears. C is wrong because the two eigenvalues here are distinct, so
there is no tie for the dominant one and no reason to oscillate; ties are exactly
what broke power iteration for the rotation `[[0,−1],[1,0]]`. D is wrong because
`(1,1)` is not an eigenvector at all — `A(1,1) = (2, 0.5)`, which is not a
multiple of `(1,1)`, so the very first step leaves the starting direction.

</details>

**Q7.** Power iteration is run on the 90° rotation `R = [[0,−1],[1,0]]`. What
happens?

- A) It converges to the eigenvector with eigenvalue 1, since every rotation fixes the vector it turns by
- B) It converges to a real eigenvector, because a rotation must preserve at least one direction
- C) It never converges to an eigenvector: the eigenvalues are `±i`, both of magnitude 1, so nothing grows and nothing decays, and there are no real eigenvectors to converge to
- D) It converges to `(1, 1)`, the diagonal direction the rotation leaves closest to unchanged

<details>
<summary>Answer and explanation</summary>

**C) It never converges to an eigenvector: the eigenvalues are `±i`, both of
magnitude 1, so nothing grows and nothing decays, and there are no real
eigenvectors to converge to.**

This is exactly what the lesson's code prints: `|λ| = 1` for both roots, so
"power iteration cannot tell them apart — and neither can any iterative method,
because a rotation has no 'largest' direction to grow."

A is false because 1 is not an eigenvalue of `R`; the fixed vectors of a rotation
by 90° are only the zero vector. B and D are the same mistake in different clothes:
a rotation preserves lengths and angles, but it preserves no *direction* at all
when the angle is not 0 or 180°, and `(1,1)` is turned to `(−1,1)`, a 90° change,
not a scaling. This failure is what motivates singular values in
[40](40_svd_and_pca.md): they are always real and nonnegative, so a rotation's
spectrum is perfectly well behaved.

</details>

**Q8.** The PageRank matrix from the lesson has eigenvalues `1`, `−0.5`, and
`−0.25 ± 0.433i`. Power iteration's error shrinks by roughly `|λ₂/λ₁|` per step.
Roughly how many multiplications are needed to shrink the initial error by a
factor of 10⁴?

- A) About 4, because the matrix has four pages
- B) About 13, because `0.5^k = 10⁻⁴` gives `k ≈ 13.3`
- C) Exactly 13, because convergence reaches machine precision and stops there
- D) About 40000, because the factor of 10⁴ applies at each of four coordinates

<details>
<summary>Answer and explanation</summary>

**B) About 13, because `0.5^k = 10⁻⁴` gives `k ≈ 13.3`.**

`|λ₁| = 1` and the runner-up magnitude is `max(0.5, |−0.25 + 0.433i|) = 0.5`,
so each step divides the error by 2. Solving `2^{-k} = 10^{-4}` gives
`k = 4·log₂(10) ≈ 13.3`, so 13 or 14 multiplications. The lesson's loop prints
`k = 0` through `k = 8`, by which point the scores have visibly settled.

A and D are number-coincidences: the rank of the matrix and the number of
coordinates have nothing to do with the convergence rate, which is set by the
spectral gap. C is wrong because the iteration does not stop — it would keep
refining toward `10⁻⁴` of the initial error and then toward `10⁻⁸`, `10⁻¹²`, and
so on, until round-off takes over. That is why production code sets an explicit
tolerance or iteration cap rather than trusting convergence to announce itself.

</details>

**Q9.** A matrix has eigenvalue `0.5` with algebraic multiplicity 2 and geometric
multiplicity 1. What can you conclude?

- A) The matrix is not diagonalizable, because one eigenvalue is short of a full set of independent eigenvectors
- B) The matrix has three linearly independent eigenvectors
- C) The matrix must be symmetric, since only symmetric matrices have repeated eigenvalues
- D) The determinant of the matrix is 0.5

<details>
<summary>Answer and explanation</summary>

**A) The matrix is not diagonalizable, because one eigenvalue is short of a full
set of independent eigenvectors.**

The criterion is pointwise: `A` is diagonalizable iff `dim E_λ = mult_alg(λ)` for
*every* `λ`. One eigenvalue failing is enough to fail the whole test, and this is
the concrete form of "defective" from the lesson.

B miscounts: geometric multiplicity 1 means one eigenvector for `λ = 0.5`, and
even adding eigenvectors for other eigenvalues cannot reach the full count, or
`A` would be diagonalizable. C reverses the lesson's point — it is symmetry that
*guarantees* repeated eigenvalues are harmless, and symmetry is an additional
property you must verify, not something forced by repetition. Case B of the code
(`[[3,1,0],[0,3,0],[0,0,5]]`) is symmetric-free and defective; case C
(`[[2,1,0],[1,2,1],[0,1,2]]`) is symmetric and well behaved. D confuses an
eigenvalue with the determinant, which is the *product* of all eigenvalues.

</details>

**Q10.** A root-finding routine is handed a matrix whose true characteristic
polynomial is `(λ − 2)³` and returns the values `2 + 10⁻⁸i`, `2 − 10⁻⁸i`, and
`2.0`. What has happened?

- A) The matrix has three distinct eigenvalues, two of which happen to be very close together
- B) The matrix is defective, and the library is returning an error
- C) There is a genuine triple root; a naive root-finder can only locate a root of multiplicity `m` to about `O(eps^(1/m))`, so the triple root splits into a nearly-complex pair
- D) The two complex values are harmless rounding noise and should simply be discarded, leaving one clean eigenvalue of 2

<details>
<summary>Answer and explanation</summary>

**C) There is a genuine triple root; a naive root-finder can only locate a root of
multiplicity `m` to about `O(eps^(1/m))`, so the triple root splits into a
nearly-complex pair.**

The lesson computes this: for a matrix whose `det(λI − A) = (λ−2)³`, the
Durand–Kerner block clusters its output and prints `2 − 1.1e-8i` and `2 + 8.8e-9i`
for two of the three copies. With `m = 3` in double precision,
`eps^(1/3) ≈ 1e-5`, so this is the best the method can do.

A takes the artefact at face value and invents two distinct eigenvalues, which
would then need to be counted as algebraic multiplicities 1, 1, 1 — three numbers
that cannot all be right, since they must sum to `n` only if none is repeated.
B mislabels a conditioning limit as a correctness failure: a defective matrix is
a perfectly valid matrix, and the routine returned a usable approximation to its
spectrum. D misreads the polynomial: `(λ−2)³ = λ³ − 6λ² + 12λ − 8` has `λ³ − 8`
as a different polynomial, whose only root is 2 but whose `λ²` and `λ`
coefficients are wrong.

</details>

## Subjective Questions

### Short Answer

**Q1. Define an eigenvector and an eigenvalue of a square matrix, and say why the
zero vector is excluded from the definition.**

<details>
<summary>Model answer</summary>

A nonzero vector `x` is an **eigenvector** of `A` with **eigenvalue** `λ` if
`Ax = λx`. Geometrically, `A` sends `x` to a point on the same line through the
origin, so the direction survives while the length may change: `λ > 1` stretches,
`0 < λ < 1` shrinks, `λ < 0` flips the direction end to end, `λ = 0` collapses it
to zero.

The zero vector is excluded because `A·0 = 0 = λ·0` holds for every scalar `λ`.
If `x = 0` counted, every number would be an eigenvalue of every matrix and the
whole theory would be vacuous.

</details>

**Q2. State the characteristic polynomial of `A` and the theorem that makes it
useful.**

<details>
<summary>Model answer</summary>

The characteristic polynomial is `p_A(λ) = det(A − λI)`. A scalar `λ` is an
eigenvalue **if and only if** `p_A(λ) = 0`.

`det(A − λI) = 0` holds exactly when `A − λI` is singular, which is exactly the
statement that there is a nonzero `x` with `(A − λI)x = 0`, that is, `Ax = λx`.
So finding eigenvalues reduces to a single polynomial problem.

`p_A` has degree exactly `n` with leading coefficient `(−1)ⁿ`, so by the
fundamental theorem of algebra it has exactly `n` complex roots counted with
multiplicity. That is why a 2×2 matrix gives two eigenvalues and a
Jordan block like `[[2,1],[0,2]]` gives "two copies of 2".

</details>

**Q3. Define algebraic and geometric multiplicity and state the relationship
between them.**

<details>
<summary>Model answer</summary>

**Algebraic** multiplicity of `λ` is the number of times `λ` occurs as a root of
`p_A(λ)`. **Geometric** multiplicity is `dim E_λ`, the dimension of the
null space of `A − λI`, i.e. the number of linearly independent eigenvectors for
`λ`.

The bound is `dim E_λ ≤ mult_alg(λ)`, and equality for every eigenvalue is
precisely the condition for `A` to be diagonalizable. So an eigenvalue with
`mult_alg = 3` and `mult_geom = 1` is the whole content of "defective".

</details>

**Q4. Give the eigenvalues of an upper-triangular matrix and justify it in one
sentence.**

<details>
<summary>Model answer</summary>

They are exactly the diagonal entries `a₁₁, a₂₂, …, a_nn`.

If `A` is upper-triangular then `A − λI` is too, and its diagonal is
`a₁₁ − λ, …, a_nn − λ`. The determinant of a triangular matrix is the product of
its diagonal entries, so `p_A(λ) = Π(a_ii − λ)`, whose roots are `λ = a_ii`.

</details>

**Q5. What does `tr(A)` tell you about the eigenvalues, and why is that useful
computationally?**

<details>
<summary>Model answer</summary>

The sum of the eigenvalues, counted with multiplicity, equals `tr(A)`, the sum of
the diagonal entries. In the worked example `A = [[2,1],[1,2]]` the eigenvalues
are 3 and 1, and `3 + 1 = 4 = 2 + 2`. Likewise the product of the eigenvalues is
`det(A)`.

It is useful because it is free. Eigenvalues usually require an iterative
algorithm whose output you cannot check by hand, while `tr(A)` is a single pass
over the diagonal and `det(A)` a row reduction. Together they pin down two
symmetric functions of the spectrum, which catches almost every arithmetic slip.

</details>

**Q6. For the four-page web in the lesson's PageRank code, state the principal
eigenvector as exact fractions and explain what the eigenvalue 1 means.**

<details>
<summary>Model answer</summary>

The link matrix is

    P = [[0, 0.5, 0,   0.5],
         [0.5, 0, 0.5, 0.5],
         [0.5, 0.5, 0,   0  ],
         [0,   0, 0.5, 0  ]]

and the eigenvector for `λ = 1`, normalised to sum to 1, is

    r = (5/21, 7/21, 6/21, 3/21) ≈ (0.238095, 0.333333, 0.285714, 0.142857)

which is what the code prints. The meaning of the eigenvalue being exactly 1 is
that a column of scores is reproduced unchanged by one step of the random
surfer: `P r = r`. Had the eigenvalue been any `λ ≠ 1`, the scores would have
been scaled by `λ` each visit and the *shares* would not have been stationary, so
the ranking itself would drift rather than settle.

Note this differs from raw link counting, which gives
`0.25, 0.375, 0.25, 0.125` and puts A above C. PageRank raises C above A because
C receives links from B, an important page.

</details>

### Long Answer

**Q1. Why can a real matrix have complex eigenvalues, and what does that tell us
about what an eigenvector is?**

<details>
<summary>Model answer</summary>

Because "has a real eigenvalue" and "has real eigenvectors" are different
properties, and the second is the one people assume from the first.

Take the 90° rotation `R = [[0,−1],[1,0]]`. Then

    λI − R = [[λ, 1], [−1, λ]]     p_R(λ) = λ² + 1

and `λ² + 1 = 0` has no real roots. So `R` has no real eigenvector at all. This is
not a defect of the analysis — it is a fact about the transformation. A 90°
rotation sends every nonzero real vector to a vector at right angles to it, so no
direction survives.

Formally the reason is arithmetic. `R` has real entries, so `p_R` has real
coefficients, and for real-coefficient polynomials `p(z̄) = conj(p(z))`. Hence if
`z` is a root, so is `z̄`. Non-real eigenvalues are therefore never alone; they
come in pairs, and for a real matrix the corresponding eigenvectors are
conjugate pairs too, as the lesson's code shows with `w = (1,−i)`.

What this teaches about eigenvectors is that they are a *complex* notion dressed
up in real clothing. The real content of "eigenvector" is "a direction that is not
rotated", and if the transformation genuinely rotates everything through 90°,
there is no such direction and the honest answer is a complex number. Forcing a
real answer here is not approximation, it is error. That is also why
`numpy.linalg.eig` returns complex arrays for real input and prints a warning
sometimes — it is reporting the truth, not failing.

</details>

**Q2. Why is the sum of the eigenvalues `tr(A)` and their product `det(A)`? What
would break if either identity failed?**

<details>
<summary>Model answer</summary>

Both come from the same place: the determinant. `det` is multiplicative,
`det(AB) = det(A)det(B)`, and by definition `det(Aᵀ) = det(A)`.

For the product, triangularise: `A = PLQ` with `P, Q` unit triangular, using
Gaussian elimination. Then `det(A) = det(P)det(L)det(Q) = det(L)`, since unit
triangular matrices have determinant 1, and `det(L) = Π a_ii`. Each `a_ii` is an
eigenvalue of `A` (Exercise 2), so `det(A) = Πλ_i`.

For the sum, apply the same argument to `λI − A`, whose triangular form has
diagonal `λ − a_ii`, giving `p_A(λ) = Π(λ − a_ii)`. Expanding, the coefficient of
`λ^{n−1}` is `−Σ a_ii = −tr(A)`. The coefficient of `λ^{n−1}` in any monic
polynomial is minus the sum of its roots, so `Σλ_i = tr(A)`.

What would break: these are the only handles we have on an answer we cannot
compute exactly. In the lesson's 3×3 example the numerical routine produces
roots of `λ³ − 7λ² + 14λ − 8` by an iterative scheme with no closed form, and
the only reason we trust them is that they satisfy both identities — `1 + 2 + 4 =
7 = tr(A)` and `1·2·4 = 8 = det(A)`. If a computed eigenvalue set violated either,
we would have no independent way to know which value was wrong; the trace and
determinant come from a completely different algorithm (diagonal sum, and
cofactor expansion). The identities also underpin entire downstream results —
`tr(A^k) = Σλ_i^k`, the connection between eigenvalues and traces of powers that
makes power iteration work.

</details>

**Q3. Why does power iteration find the eigenvector of the largest eigenvalue,
and what breaks the argument?**

<details>
<summary>Model answer</summary>

Suppose `A` has a full basis of eigenvectors `v_1, …, v_n` and we start from
`x₀ = Σ c_i v_i`. Then `A^k x₀ = Σ c_i λ_i^k v_i`. Dividing by `‖A^k x₀‖` removes
the overall scale, and as `k → ∞` the terms with `|λ_i| < |λ_1|` are divided by
`|λ_1|^k` and vanish relative to the dominant one. So the iterates converge to
`v₁`, up to scale and sign — which is all an eigenvector is.

Three things break this.

**Tied magnitudes.** If `|λ_2| = |λ_1|`, no term dominates. The 90° rotation in
the lesson is the clean case: eigenvalues `+i` and `−i`, both of magnitude 1, so
`A^k x₀` is rotated, never growing, and the normalised iterates cycle forever.
The lesson prints `|λ| = 1.0` for both roots and says outright that no iterative
method can pick a winner.

**The matrix is not diagonalizable.** Without a full basis of eigenvectors the
expansion above does not exist. Worse, a Jordan block `[[2,1],[0,2]]` has
`A^k = 2^k [[1, k/2],[0, 1]]`: the norm grows like `2^k k`, not like `2^k`, so the
estimate from eigenvalues alone understates the growth by a factor of `k`.
Eigenvalues do not control the transient.

**No spectral gap in practice.** In floating point, once the error has decayed to
round-off the last few bits are noise and further iterations wander. Hence
`scipy.sparse.linalg.eigs` adds `tol` and `maxiter`, and real PageRank adds a
damping factor `0.85`.

</details>

**Q4. Why does PageRank need the eigenvalue to be exactly 1, and what would go
wrong if the leading eigenvalue were, say, 0.9?**

<details>
<summary>Model answer</summary>

The construction is: put the random surfer somewhere, follow one link, and
record where they land. After `k` clicks the visit distribution is
`x_k = P^k x₀`, and `P` is column-stochastic, so each `x_k` is a probability
vector summing to 1. PageRank wants the *steady state*: the distribution that
reproduces itself, `P r = r`.

That equation has a solution only for `λ = 1`. If the leading eigenvalue were
`λ ≠ 1`, the stationary equation `P r = r` would have no solution at all, so no
"eventual visit share" would exist to speak of. PageRank would then be an
arbitrary scoring convention rather than a consequence of the random walk.

Concretely, if the dominant eigenvalue were 0.9, then `P^k x₀ → 0` as
`k → ∞`, because every step shrinks the whole vector by 0.9. The shape
stabilises — the *ratios* between coordinates settle — but the vector itself
decays to zero. Scores would need renormalising at every step, and any absolute
quantity such as "expected number of visits in 100 steps" would depend on the
starting vector rather than on the graph. Worse, with `0.9 < 1` the power
iteration loses about 5% of its signal per step, so it needs roughly
`log(10⁻⁶)/log(0.9) ≈ 131` steps to converge instead of the ~20 needed at
`λ = 1`. The eigenvalue being exactly 1 is not incidental; it is what makes the
process conservative and the ranking well defined.

</details>

**Q5. Why does an eigenvalue of algebraic multiplicity 3 split into a
near-complex pair in floating-point root-finding, and why is that not a bug?**

<details>
<summary>Model answer</summary>

Consider `p(λ) = (λ − 2)³ = 0` in double precision. Near a root, write
`λ = 2 + ε`. Then `p(λ) = ε³`, and the exact condition is `ε³ = 0`, i.e. `ε = 0`.
In floating point, `ε³` cannot be evaluated exactly and the arithmetic rounds, so
the computed value is perturbed by an amount on the order of machine epsilon
relative to the scale of the terms involved. The sensitive quantity is therefore
`ε ~ eps^{1/3}`, not `eps`.

With `eps ≈ 2.2 × 10⁻¹⁶`, `eps^{1/3} ≈ 6 × 10⁻⁶`. The algorithm is hunting for a
zero of a function that is flat to third order, so it cannot do better than a few
parts in `10⁻⁶`. And a real-coefficient polynomial's roots come in conjugate
pairs, so a perturbed real root shows up as `2 + 10⁻⁸i` and `2 − 10⁻⁸i`. The
lesson's Durand–Kerner block prints exactly this and then fixes it by clustering:
the number of roots in a cluster is the algebraic multiplicity, and the cluster
mean is a far better estimate of the true root than any single iterate.

This is not a bug because no algorithm can beat it in this representation —
the information is not there. That is why `numpy.linalg.eigvals` uses a
different algorithm entirely, the shifted QR algorithm, which extracts
eigenvalues from a Hessenberg form rather than from polynomial roots, and why
`numpy.linalg.eig` on a symmetric matrix is preferred: symmetry makes the roots
real and distinct, which is the well-conditioned case.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — 2×2 eigenvalues by hand.** For `A = [[4, 2], [1, 3]]`, find
the characteristic polynomial, both eigenvalues, and one eigenvector for each.
Verify each eigenvector numerically.

<details>
<summary>Solution</summary>

`A − λI = [[4−λ, 2], [1, 3−λ]]`, so
`p_A(λ) = (4−λ)(3−λ) − 2·1 = 12 − 7λ + λ² − 2 = λ² − 7λ + 10`.
Factor: `(λ − 5)(λ − 2)`. So `λ = 5` and `λ = 2`.
Check: `tr(A) = 4 + 3 = 7` and `5 + 2 = 7` ✓

For `λ = 5`: `A − 5I = [[−1, 2], [1, −2]]`. Rows are dependent, rank 1.
Equation `−x + 2y = 0`, so `x = 2y`. Take `y = 1`: `v = (2, 1)`.
Check: `A v = (4·2 + 2·1, 1·2 + 3·1) = (10, 5) = 5·(2, 1)` ✓

For `λ = 2`: `A − 2I = [[2, 2], [1, 1]]`. Rank 1.
Equation `2x + 2y = 0`, so `x = −y`. Take `y = 1`: `v = (−1, 1)`.
Check: `A v = (4·(−1) + 2·1, (−1) + 3·1) = (−2, 2) = 2·(−1, 1)` ✓

</details>

**[ ] Exercise 2 — triangular matrices are easy.** Prove that the eigenvalues
of an upper-triangular matrix are exactly its diagonal entries, and find the
eigenvectors of `A = [[1, 1, 0], [0, 2, 1], [0, 0, 3]]`.

<details>
<summary>Solution</summary>

For upper-triangular `A`, the matrix `A − λI` is also upper-triangular, and its
diagonal is `a_11 − λ, a_22 − λ, …, a_nn − λ`. The determinant of a triangular
matrix is the product of its diagonal entries (proved by cofactor expansion: all
off-diagonal cofactors vanish by induction). Therefore
`p_A(λ) = Π (a_ii − λ)`, whose roots are `λ = a_ii`.

For `A = [[1,1,0],[0,2,1],[0,0,3]]` the eigenvalues are `1, 2, 3`.

Eigenvectors, working from the bottom row up:

`λ = 3`: `A − 3I = [[−2,1,0],[0,−1,1],[0,0,0]]`. Row 2: `−y + z = 0` so
`z = y`. Row 1: `−2x + y = 0` so `y = 2x`. Free: `x`.
Take `x = 1`: `v = (1, 2, 2)`. Check: `Av = (1+2, 4+2, 6) = (3, 6, 6) = 3v` ✓

`λ = 2`: `A − 2I = [[−1,1,0],[0,0,1],[0,0,1]]`. Rows 2 and 3 both give
`z = 0`. Row 1: `y = x`. Free: `x`. Take `x = 1`: `v = (1, 1, 0)`.
Check: `Av = (1+1, 2, 0) = (2, 2, 0) = 2v` ✓

`λ = 1`: `A − I = [[0,1,0],[0,1,1],[0,0,2]]`. Row 3: `2z = 0` so `z = 0`.
Row 2: `y + z = 0` so `y = 0`. Row 1: `y = 0`, no constraint. Free: `x`.
Take `x = 1`: `v = (1, 0, 0)`.
Check: `Av = (1, 0, 0) = 1·v` ✓

All three are independent, so `A` is diagonalisable.

</details>

**Challenge — Exercise 3 — repeated roots and the rank trick.** Let
`A = [[2, 1, 0], [0, 2, 0], [0, 0, 5]]`.

(a) Find `p_A(λ)` and the algebraic multiplicity of each eigenvalue.
(b) Find `dim ker(A − 2I)` and `dim ker(A − 5I)`.
(c) Is `A` diagonalisable? Give a one-line argument.

<details>
<summary>Solution</summary>

**(a)** `A` is upper-triangular, so by Exercise 2 the eigenvalues are the
diagonal: `2` and `5`. The constant term of `p_A(λ) = det(A − λI)` is
`det(A) = 2·2·5 = 20`, and expanding the first row gives
`p_A(λ) = (2−λ)[(2−λ)(5−λ)] − 1·[0·(5−λ) − 0] = (2−λ)²(5−λ)`.
So `λ = 2` has **algebraic multiplicity 2** and `λ = 5` has multiplicity 1.

**(b)** `A − 2I = [[0,1,0],[0,0,0],[0,0,3]]`. Row 1 forces `y = 0`; rows 2 and 3
are then all zeros, so `x` and `z` are both free. Dimension **2**.

`A − 5I = [[−3,1,0],[0,−3,0],[0,0,0]]`. Row 2: `−3y = 0` so `y = 0`. Row 1:
`−3x = 0` so `x = 0`. Only `z` is free. Dimension **1**.

**(c)** Yes. For `λ = 2` the geometric multiplicity 2 equals the algebraic
multiplicity 2, and for `λ = 5` they are both 1, so every eigenvalue has enough
eigenvectors and `A` is diagonalisable. Explicitly,
`A = V D V⁻¹` with `V = [[1,0,0],[0,1,0],[0,0,1]]`… more usefully take the
eigenvectors `v_2 = (1, 0, 0)`, `w_2 = (0, 1, 0)` for `λ = 2` and `v_5 = (0, 0, 1)`
for `λ = 5`, giving `V = I` and `D = A`. Note the contrast with
`[[2,1],[0,2]]` in the lesson, where the off-diagonal 1 sits *between* the two
copies of the repeated eigenvalue and destroys diagonalisability; here it sits
between `2` and the distinct `5`, so it is harmless.

</details>

**[ ] Exercise 4 — power iteration by hand, four multiplications.** Let
`A = [[3, 1], [1, 3]]`, which has eigenvalues 4 and 2.

(a) Start from `x₀ = (1, 0)`. Apply `A`, renormalise, and repeat three times,
writing down the Rayleigh quotient `$x^{\mathsf T}Ax / x^{\mathsf T}x$` at
each step.
(b) Explain from the exact arithmetic why the iterates move towards `(1, 1)`.
(c) Predict the Rayleigh quotient's limit and say what it would be if you
started from `(1, −1)` instead.

<details>
<summary>Solution</summary>

**(a)** The iteration is `x_{k+1} = A x_k / ‖A x_k‖₂`, and the Rayleigh quotient is
`xᵀAx / xᵀx`.

`x₀ = (1, 0)`. `A x₀ = (3, 1)`, `‖A x₀‖ = √10 ≈ 3.1623`, so
`x₁ = (0.948683, 0.316228)`.
Rayleigh at `x₀`: `x₀ᵀA x₀ / x₀ᵀx₀ = 3 / 1 = 3.0`.

`A x₁ = (3·0.948683 + 0.316228, 0.948683 + 3·0.316228) = (3.162278, 1.897367)`.
Norm `≈ 3.6878`, so `x₂ = (0.857493, 0.514496)`.
Rayleigh at `x₁`: numerator `0.948683·3.162278 + 0.316228·1.897367 = 3.0 + 0.6 =
3.6`; denominator `0.9 + 0.1 = 1.0`. So **3.600000**.

`A x₂ = (3.086975, 2.400981)`. Norm `≈ 3.9108`, so `x₃ = (0.789352, 0.613941)`.
Rayleigh at `x₂`: numerator `0.857493·3.086975 + 0.514496·2.400981 = 2.647059 +
1.235294 = 3.882353`; denominator `0.735294 + 0.264706 = 1.0`. So **3.882353**.

One more step gives `x₄ = (0.749838, 0.661622)` with Rayleigh quotient
**3.992218**.

**(b)** Write `x₀` in the eigenbasis. With `u = (1,1)` for `λ = 4` and
`v = (1,−1)` for `λ = 2`, we have `x₀ = (u + v)/2`, so

    A^k x₀ = (4^k u + 2^k v) / 2

The `u` component grows like `4^k` while the `v` component grows like `2^k`, so
after normalising the relative weight of `v` versus `u` is `(2/4)^k = 0.5^k`.
After three multiplications that ratio is `0.125`, and the iterates have visibly
drifted towards the diagonal, as the numbers show: the second coordinate rises
from 0.316 to 0.514 to 0.614 to 0.662, heading towards `1/√2 ≈ 0.7071`.

**(c)** The limit is **4**, the eigenvalue of largest magnitude. Starting from
`(1, −1)` the answer is **2**: that vector is exactly `v`, an eigenvector itself,
so `A^k v = 2^k v` and every iterate stays on the same line while the Rayleigh
quotient is identically 2. This is the sharp edge of the method — it finds *an*
eigenvector of largest magnitude in the starting vector's own invariant
subspace, and only converges to the *dominant* one if that direction is present.

</details>

**[ ] Exercise 5 — a symmetric tridiagonal matrix, exactly.** Let
`S = [[2, 1, 0], [1, 2, 1], [0, 1, 2]]`.

(a) Compute `det(λI − S)` and factor it. Express the eigenvalues in closed form.
(b) Find one eigenvector for each, in exact form.
(c) Show the three eigenvectors are mutually orthogonal and normalise them.
(d) Explain why the off-diagonal 1s here do not make `S` defective, in contrast
to `[[2,1],[0,2]]`.

<details>
<summary>Solution</summary>

**(a)** Expand along the first row of `λI − S = [[λ−2, −1, 0], [−1, λ−2, −1],
[0, −1, λ−2]]`:

    det = (λ−2)·[ (λ−2)² − 1 ] − ( −1 )·[ −(λ−2) − 0 ]
        = (λ−2)[(λ−2)² − 1] − (λ−2)
        = (λ−2)[(λ−2)² − 2]

Check the sign: expanding `[[a, b, c],[d, e, f],[g, h, i]]` along the first row is
`a(ei − fh) − b(di − fg) + c(dh − eg)`. Here `a = λ−2, b = −1, d = −1, i = λ−2`,
so the second term is `−(−1)(−(λ−2) − 0) = +(−(λ−2)) = −(λ−2)`, as written.

Roots: `λ − 2 = 0` gives `λ = 2`; `(λ−2)² = 2` gives `λ = 2 + √2` and
`λ = 2 − √2`. Numerically: `3.414214`, `2.000000`, `0.585786`.
Check: sum `= 6 = tr(S)` ✓. Product `= 2(4−2) = 4 = det(S)` ✓.

**(b)** Write the system down once, carefully:

    S - λI = [[2-λ, 1, 0],
             [1,   2-λ, 1],
             [0,   1,   2-λ]]

The off-diagonals stay `+1` — subtracting `λI` only touches the diagonal — so the
three rows are `(2−λ)x + y = 0`, `x + (2−λ)y + z = 0`, and `y + (2−λ)z = 0`. Solve
the two outer rows first; they each fix one coordinate in terms of `x`, and then
the middle row is the consistency check.

For `λ = 2`, `2 − λ = 0`. Rows become `y = 0`, `x + z = 0`, `y = 0`.
Take `x = 1`: `v₂ = (1, 0, −1)`.
Check: `S v₂ = (2 + 0, 1 − 1, 0 − 2) = (2, 0, −2) = 2·(1, 0, −1)` ✓

For `λ = 2 + √2`, `2 − λ = −√2`.
Row 1: `−√2 x + y = 0` → `y = √2 x`
Row 3: `y − √2 z = 0` → `z = y/√2 = x`
Row 2 (check): `x + (−√2)(√2 x) + z = x − 2x + x = 0` ✓ automatically
Take `x = 1`: `v₊ = (1, √2, 1)`.
Check: `S v₊ = (2 + √2, 1 + 2√2 + 1, √2 + 2) = (2+√2, 2√2 + 2, 2+√2)`
and `(2+√2) v₊ = (2+√2, 2√2 + 2, 2+√2)` ✓

For `λ = 2 − √2`, `2 − λ = √2`.
Row 1: `√2 x + y = 0` → `y = −√2 x`
Row 3: `y + √2 z = 0` → `z = −y/√2 = x`
Row 2 (check): `x + √2(−√2 x) + x = 0` ✓
Take `x = 1`: `v₋ = (1, −√2, 1)`.
Check: `S v₋ = (2 − √2, 1 − 2√2 + 1, −√2 + 2) = (2−√2, 2 − 2√2, 2−√2)`
and `(2−√2) v₋ = (2−√2, 2 − 2√2, 2−√2)` ✓

The pattern is worth noticing: `v₊` and `v₋` differ only in the sign of the middle
coordinate, and `v₂` has no middle coordinate at all. Tridiagonal matrices with
constant off-diagonals have this mirror structure because the matrix commutes with
a flip of the middle axis.

**(c)** Dot products:

    v₂ · v₊ = 1·1 + 0·√2 + (−1)(1) = 0  ✓
    v₂ · v₋ = 1·1 + 0·(−√2) + (−1)(1) = 0  ✓
    v₊ · v₋ = 1 − 2 + 1 = 0  ✓

Lengths: `‖v₂‖ = √2`, `‖v₊‖ = ‖v₋‖ = √(1+2+1) = 2`. Normalised:

    q₂ = (1, 0, −1)/√2
    q₊ = (1, √2, 1)/2
    q₋ = (1, −√2, 1)/2

So `Q = [q₊ q₂ q₋]` is orthogonal, and `Qᵀ S Q = diag(2+√2, 2, 2−√2)` — no
eigenvector computation needed after the fact, and no normalisation drift.

**(d)** `[[2,1],[0,2]]` has *one* repeated eigenvalue, so both copies of `2` must
share a single eigenspace; the off-diagonal 1 chains them together and leaves only
one independent direction. Here `S` has three *distinct* eigenvalues
(`2 − √2 ≈ 0.5858`, `2`, `2 + √2 ≈ 3.4142`), each with algebraic multiplicity 1, so
the bound `dim E_λ ≤ mult_alg(λ)` forces `dim E_λ = 1 = mult_alg(λ)` for each, and
the matrix is diagonalisable with no room for the failure. More fundamentally,
`S` is symmetric, and symmetry guarantees diagonalisability for every `n`. Off-diagonal
entries only cause trouble when they sit *between two copies of the same
eigenvalue*, which is exactly the `2, 1 / 0, 2` pattern — compare Exercise 3's
`[[2,1,0],[0,2,0],[0,0,5]]`, where the same off-diagonal 1 is harmless because its
neighbour is 5, not 2.

</details>

**Challenge — Exercise 6 — Jordan blocks grow faster than their eigenvalues
predict.** Let `J = [[2, 1], [0, 2]]`.

(a) Show by induction that `J^k = [[2^k, k·2^{k−1}], [0, 2^k]]` for every
integer `k ≥ 1`.
(b) Both eigenvalues are 2, so the "each direction grows like `λ^k = 2^k`" rule from
the lesson predicts growth proportional to `2^k`. Show that is wrong by computing
`‖J^k (0,1)‖` for `k = 1, 3, 5, 10`.
(c) Explain what this says about using eigenvalues alone to predict the stability
of `x_{k+1} = A x_k`, and name the structural feature of `A` responsible.

<details>
<summary>Solution</summary>

**(a)** Base case `k = 1`: `[[2, 1], [0, 2]] = [[2^1, 1·2^0], [0, 2^1]]` ✓.

Inductive step. Assume `J^k = [[2^k, k·2^{k−1}], [0, 2^k]]`. Then

    J^(k+1) = J J^k = [[2, 1], [0, 2]] · [[2^k, k 2^{k-1}], [0, 2^k]]
            = [[2·2^k + 1·0,  2·k 2^{k-1} + 1·2^k],
               [0,             2·2^k]]
            = [[2^{k+1},      k 2^k + 2^k],
               [0,            2^{k+1}]]
            = [[2^{k+1}, (k+1) 2^k], [0, 2^{k+1}]]

which is the claimed formula with `k` replaced by `k + 1`. ∎

**(b)** `J^k (0,1) = (k·2^{k−1}, 2^k)`, so `‖J^k(0,1)‖ = 2^k √((k/2)² + 1) =
2^{k−1} √(k² + 4)`.

    k =  1:  2^0 · √5      = 2.236
    k =  3:  2^2 · √13     = 14.422
    k =  5:  2^4 · √29     = 86.163
    k = 10:  2^9 · √104    = 5221.396

Compare with the naive `2^k`: `2, 8, 32, 1024`. The ratios are
`√((k/2)²+1)/2 = 1.118, 1.803, 2.693, 5.099`. So the growth is `2^k` multiplied by
a factor that itself grows like `k/2` — the true growth is `Θ(k·2^k)`, not
`Θ(2^k)`. The output of `numpy` confirms it: `J^3 = [[8,12],[0,8]]` and
`J^5 = [[32,80],[0,32]]`.

**(c)** The lesson's rule `x_k = λ^k x_0` assumed `x₀` was an eigenvector. When `A`
is defective that assumption fails, and the missing factor is the **nilpotent
part**. Writing `J = 2I + N` with `N = [[0,1],[0,0]]`, the binomial theorem gives
`J^k = 2^k(I + (k/2)N)`, since `N² = 0`. The `k` appears because the same matrix
is being added to itself `k` times.

So the consequences are:

- **Stability still has the same threshold.** `|λ| > 1` still means growth and
  `|λ| < 1` still means decay, because the polynomial factor `k` never overtakes
  an exponential. But "decays" must be read as `Θ(2^{-k} k)`, which reaches
  round-off sooner or later than plain `2^{-k}` suggests.
- **Transients are longer and badly conditioned.** For `λ = 2` and `λ = 0.5`, the
  Jordan and diagonal versions of `A` have identical spectra, so any analysis
  using only eigenvalues gives the same answer for both — and that answer is
  wrong for one of them. This is exactly why `numpy.linalg.eig` returns vectors in
  arbitrary (often nearly parallel) order for defective matrices, and why one
  checks `dim E_λ` against `mult_alg(λ)` before trusting an eigendecomposition.
- **Practical rule.** For stability over long horizons, bound `‖A^k‖` directly —
  via repeated squaring, or with an induced norm such as `‖A‖₁` — rather than
  from `ρ(A) = max|λ|`, which is only a good approximation when `A` is
  diagonalisable. Lesson [39](39_diagonalization_and_spectral.md) develops the
  Jordan form that makes this precise.

</details>

## Summary

- An eigenvector is a **direction** the matrix only scales; the eigenvalue `λ`
  is the scaling factor in `Ax = λx`.
- The eigenvalues are exactly the roots of the **characteristic polynomial**
  `det(A − λI)`, a degree-`n` polynomial with exactly `n` complex roots.
- **Algebraic** multiplicity counts copies in the polynomial; **geometric**
  multiplicity counts independent eigenvectors. Geometric ≤ algebraic always.
- A matrix is **diagonalisable** iff the two multiplicities agree for every
  eigenvalue, i.e. iff it has a full basis of eigenvectors.
- Real matrices can have **complex** eigenvalues, always in conjugate pairs —
  rotations have no real eigenvectors at all.
- **Power iteration** (multiply repeatedly, renormalise) finds the eigenvector of
  largest-magnitude eigenvalue, and it fails when magnitudes tie.
- The sum of the eigenvalues is `tr(A)` and their product is `det(A)` — free
  consistency checks that cost nothing.
- **PageRank is an eigenvector problem**: the link matrix always has eigenvalue
  1, and the ranking is its eigenvector.
- Repeated roots of multiplicity ≥ 3 cannot be pinned down to full precision by
  root-finding — a real limit, which is why libraries use the QR algorithm.

## Next

[37 — Inner Products, Norms, and Geometry](37_inner_products_norms_geometry.md)
adds the missing ingredient from this lesson. So far "direction" has been
informal, because linear algebra has no built-in notion of length or angle.
This lesson finally defines both, and the choice turns out to change what
"closest" means.
