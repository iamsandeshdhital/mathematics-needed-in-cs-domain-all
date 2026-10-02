# 35 — Linear Transformations and Kernels

**Part**: part03_linear_algebra · **Prerequisites**: 34 · **Time**: 40 min

---

## In Plain Words

Everything so far has been about matrices as data. This lesson is about
matrices as *machines*: something that takes a list of numbers in and gives a
list of numbers out. A rule of that kind is linear if it treats scaling and
adding the way arithmetic does — double the input, double the output; add two
inputs, add the two outputs.

The whole subject of linear algebra is the study of what such a machine does to
the space around it, and two objects matter. The **kernel** is the set of inputs
that come out as zero: the information the machine throws away. The **image** is
the set of outputs it can produce: everything it can reach. Between them they
account for the entire input space. A machine with a trivial kernel loses
nothing and is reversible; a machine with a big kernel loses dimensions, and
every dimension it loses is a direction the data cannot distinguish.

Rank-nullity says this quantitatively, and it is the organising fact of the
part: the number of dimensions destroyed plus the number preserved equals the
number you started with.

## Why Computer Science Cares

- **Every neural network layer is a linear map** followed by a nonlinearity.
  Understanding what the linear part does — which directions it amplifies,
  which it kills — is what the next four lessons are about. Layers stack into
  compositions, and composition is matrix multiplication.
- **Backpropagation is the chain rule**, and the chain rule through a linear map
  is "multiply by the matrix, transpose the gradient". This is lesson 31's
  `(AB)ᵀ = BᵀAᵀ` appearing in a gradient computation.
- **Collapsing dimensions is a bug.** A graphics projection that maps two
  different 3-D points to the same 2-D point has a nontrivial kernel. So does an
  embedding that maps distinct customers to the same vector, and the resulting
  recommendations are identical for everyone in that direction.
- **Rank-deficient models are under-determined.** A kernel direction means the
  data cannot identify a coefficient. Regularisation
  ([lesson 100](../part08_optimization/100_convexity.md)) is what picks one.
- **Convolution as a linear map.** A convolution over an image is a linear
  operator whose kernel is empty unless the kernel matrix is degenerate. Writing
  it as `im2col` then a matmul is the standard optimisation.
- **Interview questions.** "What is the kernel of a matrix?", "why does
  backpropagation use the transpose?", "what does a rank-deficient model mean
  for interpretability?" are all answered here.

## The Formal Version

Symbols follow [SYMBOLS.md](../SYMBOLS.md).

**Definition.** A map `T : V → W` is **linear** if for all `u, v ∈ V` and all
scalars `c`:

    T(u + v) = T(u) + T(v)      and      T(cu) = cT(u)

**Explanation.** Equivalently `T(αu + βv) = αT(u) + βT(v)`. From these two,
`T(0) = 0`: put `u = v = 0` to get `T(0) = 2T(0)`. So a map that moves the
origin is not linear. A map of the form `x ↦ Ax + b` with `b ≠ 0` is **affine**,
not linear, which is why the bias in a neural layer is not part of the linear
structure.

**Theorem.** A map `T : Fⁿ → F^m` is linear if and only if there is an `m × n`
matrix `A` with `T(x) = A x` for all `x`.

**Explanation.** (⇐) Matrix multiplication is linear: `A(u+v) = Au + Av` by
distributivity, and `A(cx) = cAx` by factoring. (⇒) Write `x = Σ_j x_j e_j`.
Then `T(x) = Σ_j x_j T(e_j)`, so `T` is determined by the `m` vectors `T(e_j)`,
and the matrix whose columns are those vectors satisfies `A x = T(x)`. Uniqueness
follows too: if `A` and `A'` both work, they agree on every `e_j`, hence on
every `x`. So linear maps from `Fⁿ` to `F^m` are in bijection with `m × n`
matrices.

**Definition.** For a linear map `T`, the **kernel** is `ker(T) = {x : T(x) = 0}`
and the **image** is `im(T) = {T(x) : x ∈ V}`.

**Theorem.** `ker(T)` and `im(T)` are subspaces of `V` and `W` respectively.

**Explanation.** `T(0) = 0` so `0 ∈ ker(T)`. If `T(u) = T(v) = 0` then
`T(u + v) = 0` and `T(cu) = 0`. For the image: `0 = T(0) ∈ im(T)`, and
`T(u) + T(v) = T(u+v)` and `cT(u) = T(cu)` are both images of something.

**Theorem (First isomorphism theorem).** For a linear map `T : V → W` with `V`
finite-dimensional:

    dim(ker T) + dim(im T) = dim V

and `im(T) ≅ V / ker(T)`.

**Explanation.** Choose a basis `b₁, …, b_k` of `ker(T)` and extend it to a
basis `b₁, …, b_n` of `V`. Then `T(b₁), …, T(b_k)` are all zero and
`T(b_{k+1}), …, T(b_n)` are linearly independent (a combination giving zero is a
dependence in the kernel, which the `b_i` have none of) and span `im(T)`. So
`dim(im T) = n − k`, and the sum is `n`. The isomorphism statement says the same
thing structurally: the only thing distinguishing two inputs is their difference
modulo the kernel.

**Theorem (Injectivity and surjectivity).** For `T : V → W` finite-dimensional:

- `ker(T) = {0}` iff `T` is one-to-one (injective);
- `im(T) = W` iff `T` is onto (surjective);
- if `dim V = dim W` then these two are equivalent, and `T` is an isomorphism.

**Explanation.** One-to-one means `T(u) = T(v) ⇒ u = v`, and
`T(u) − T(v) = T(u − v)`, so injectivity is exactly "no nonzero kernel vector".
Onto means the image is all of `W`. When `dim V = dim W = n`, rank-nullity gives
`dim ker T + dim im T = n`, so `dim ker T = 0` iff `dim im T = n`.

**Theorem (Restriction to a subspace).** If `U ⊆ V` is a subspace then `T(U)` is a
subspace of `im(T)`, and `ker(T|_U) = ker(T) ∩ U`.

**Explanation.** Restricting a linear map to a subspace gives a linear map, and
the kernel of the restriction is by definition the vectors of `U` that `T` kills.

**Theorem (Composition).** If `T : V → W` and `S : W → X` are linear then
`S ∘ T : V → X` is linear, with

    ker(S ∘ T) = T⁻¹(ker S)     and     im(S ∘ T) = S(im T)

**Explanation.** `S(T(u + v)) = S(T(u) + T(v))` and so on. An input is killed by
the composition exactly when `T` sends it into `ker(S)`, and an output is
reachable exactly when `S` applied to some reachable point gives it. **This is
the key structural fact**: kernels and images compose, and the chain rule for
derivatives follows the same pattern.

**Definition.** `T` is **invertible** if there is `T⁻¹ : W → V` with
`T⁻¹T = id_V` and `TT⁻¹ = id_W`.

**Theorem.** `T` is invertible iff `ker(T) = {0}` and `im(T) = W`. For a linear
map on matrices, `ker(A) = {0}` iff `det(A) ≠ 0` iff `rank(A) = n`.

**Explanation.** If `T⁻¹` exists and `T(x) = 0` then `x = T⁻¹(0) = 0`. If
`ker(T) = {0}` and `T(x) = T(y)` then `T(x − y) = 0` so `x = y`, giving
injectivity; and the linear map on a basis matrix gives surjectivity, so an
inverse exists by solving `Ax = b` column by column.

## Worked Example

Take a matrix with a genuine kernel and work through every definition:

    A = | 1  2  3 |
        | 2  4  6 |
        | 1  1  1 |

Row 1 is exactly twice row 0, so `rank(A) ≤ 2`.

**Step 1: it is a linear map `T : ℝ³ → ℝ³`.** Nothing to prove — `T(x) = A x` is
matrix multiplication, which is linear by distributivity. And `T(0) = 0`, since
every entry of `A·0` is a sum of products with a zero.

**Step 2: row reduce.** `R1 ← R1 − 2R0` gives row 1 all zeros. Then `R2 ← R2 − R0`
gives `(0, −1, −2)`. Scale by `−1` to get a pivot of 1, giving `R2 = (0, 1, 2)`.
Then `R0 ← R0 − 2R2` gives `(1, 0, −1)`:

    rref(A) = | 1  0  −1 |
              | 0  1   2 |
              | 0  0   0 |

**Step 3: find the kernel.** Solve `A x = 0` using the RREF: `x₀ − x₂ = 0` and
`x₁ + 2x₂ = 0`, so `x₀ = x₂` and `x₁ = −2x₂`. Column 2 is free. Setting `x₂ = 1`:

    ker(A) = span{ (1, −2, 1)ᵀ }

Check directly:

    A (1, −2, 1) = (1 − 4 + 3,  2 − 8 + 6,  1 − 2 + 1) = (0, 0, 0)  ✓

**Step 4: find the image.** The image is the span of the columns:

    col0 = (1, 2, 1)ᵀ,   col1 = (2, 4, 1)ᵀ,   col2 = (3, 6, 1)ᵀ

`col2 = −col0 + 2·col1`, verified: `−(1,2,1) + 2(2,4,1) = (−1+4, −2+8, −1+2) =
(3, 6, 1)` ✓. And `col0`, `col1` are independent, since `col0` is not a multiple
of `col1` (`1/2 ≠ 2/4`). So

    im(A) = span{ (1, 2, 1)ᵀ, (2, 4, 1)ᵀ },   dim = 2

**Step 5: check rank-nullity.** `dim(ker A) + dim(im A) = 1 + 2 = 3 = dim(ℝ³` ✓

**Step 6: interpret.** The machine kills the direction `(1, −2, 1)` entirely: add
any multiple of it to an input and the output does not move. So the map is not
injective — it is not reversible, and `A x = b` has either no solution or
infinitely many. Meanwhile the image is a two-dimensional plane inside `ℝ³`, so
the map is not surjective either: some right-hand sides are unreachable. Three
input dimensions in, two output dimensions kept, one thrown away.

**Step 7: the decomposition, done properly.** To split `x = x_im + x_ker`, extend
a kernel basis to a basis of the domain. Kernel basis `(1, −2, 1)`; add
`e₀ = (1, 0, 0)` and `e₁ = (0, 1, 0)`. Are these three independent? `A e₀ =
(1, 2, 1) ≠ 0` and `A e₁ = (2, 4, 1) ≠ 0`, and the two are independent, so yes —
they span `ℝ³` with no kernel direction among them.

Take `x = (0, 0, 1)`. Write `x = α(1, −2, 1) + β(1, 0, 0) + γ(0, 1, 0)`. Third
component: `α = 1`. First: `α + β = 0`, so `β = −1`. Second: `−2α + γ = 0`, so
`γ = 2`.

    x = 1·(1, −2, 1) − 1·(1, 0, 0) + 2·(0, 1, 0)
      = (1, −2, 1) − (1, 0, 0) + (0, 2, 0)
      = (0, 0, 1)  ✓

So `x_ker = (1, −2, 1)` and `x_im = (−1, 2, 0)`. Verify both halves:

    A x_ker = (1 − 4 + 3,  2 − 8 + 6,  1 − 2 + 1) = (0, 0, 0)          ✓
    A x_im  = (−1 + 4,  −2 + 8,  −1 + 2)         = (3, 6, 1)          ✓
    A x     = (0 + 0 + 3,  0 + 0 + 6,  0 + 0 + 1) = (3, 6, 1)          ✓

`A x = A x_im` as it must be, since the kernel part contributes nothing. Note that
`x_im = (−1, 2, 0)` is not in the row space of the RREF (`(1,0,−1)`, `(0,1,2)`) —
that subspace lives in the codomain in the sense that its *dual* describes
reachable functionals. The adapted basis of the domain is what produces `x_im`,
and using the row space instead gives a wrong `x_im` whose image is wrong. The
dimensions still come out right, which is why the error is easy to make.

**Step 8: composition.** Let `S` swap the first two coordinates, so `S` is its own
inverse and `ker(S) = {0}`. Then

    ker(S ∘ T) = {x : T(x) ∈ ker(S)} = {x : T(x) = 0} = ker(T)

Composing with an invertible map must not change the kernel. Compute `SA` directly
— its rows are rows 1, 0, 2 of `A`:

    S A = | 2  4  6 |
          | 1  2  3 |
          | 1  1  1 |

    (SA)(1, −2, 1) = (2 − 8 + 6,  1 − 4 + 3,  1 − 2 + 1) = (0, 0, 0)  ✓

Same kernel, as predicted.

Now compose with a *singular* map instead, taking `P = [[1, 0, 0], [0, 1, 0],
[0, 0, 0]]`, which sets the third coordinate to zero. Here `ker(P) = {y : y₂ = 0}`,
the plane of vectors whose third component is already zero. So `x ∈ ker(P T)`
exactly when the third component of `T x` is zero, and that component is
`x₀ + x₁ + x₂`. Therefore

    ker(P T) = {x : x₀ + x₁ + x₂ = 0} = span{ (1, 0, −1)ᵀ, (0, 1, −1)ᵀ }

Check `(1, 0, −1)`: `T(1, 0, −1) = (1 − 3, 2 − 6, 1 − 1) = (−2, −4, 0)`, and
`P(−2, −4, 0) = (−2, −4, 0)`, which is **not** the zero vector. That is fine,
and it is the point: `x ∈ ker(P T)` requires `T x ∈ ker(P)`, not `T x = 0`. The
vector `(−2, −4, 0)` lies in `ker(P)` precisely because its third component is
zero, and `P` then maps it to itself. A kernel of a composition is the
*preimage* of a kernel, and a preimage can be much bigger than either kernel.

So `dim(ker(P T)) = 2`, strictly larger than `dim(ker T) = 1`. Composing with an
invertible map leaves the kernel alone; composing with a rank-losing map inflates
it. That is the entire content of `ker(S ∘ T) = T⁻¹(ker S)`.

## Runnable Code

### What linearity means, and kernel and image

```python
TOL = 1e-9


# ---------------------------------------------------------------- helpers
def shape(M):
    return len(M), len(M[0])


def zeros(rows, cols):
    return [[0.0] * cols for _ in range(rows)]


def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


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


def matvec(M, v):
    rows, cols = shape(M)
    if len(v) != cols:
        raise ValueError(f"vector has {len(v)} entries, matrix has {cols} columns")
    return [sum(M[i][k] * v[k] for k in range(cols)) for i in range(rows)]


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


def image_basis(A, tol=TOL):
    """The image is the column space, so a basis is the pivot columns of A."""
    _, pivots = rref(A, tol)
    return [[A[i][c] for i in range(len(A))] for c in pivots]


def vadd(u, v):
    return [a + b for a, b in zip(u, v)]


def vsub(u, v):
    return [a - b for a, b in zip(u, v)]


def vscale(c, u):
    return [c * a for a in u]


def print_matrix(label, M, width=7):
    rows, cols = shape(M)
    print(f"{label}  ({rows}x{cols})")
    for row in M:
        print("  | " + " ".join(f"{x:{width}.3f}" for x in row) + " |")


def print_vector(label, v, width=7):
    print(f"{label} = [" + ", ".join(f"{x:{width}.3f}" for x in v) + "]")


# ------------------------------------------------- what makes a map linear
print("=== A map is linear when it respects scaling and adding ===")
print("T(0) = 0,  T(cu) = c T(u),  T(u + v) = T(u) + T(v). All three follow from")
print("the first two, but all three are worth checking.")
print()

# Linear example: the shear (x, y) -> (x + y, y)
shear = [[1.0, 1.0], [0.0, 1.0]]
u = [2.0, 1.0]
v = [3.0, -2.0]
c = 4.0
print("T is the shear (x, y) -> (x + y, y).")
print(f"  T(u)     = {matvec(shear, u)}")
print(f"  T(v)     = {matvec(shear, v)}")
print(f"  T(u+v)   = {matvec(shear, vadd(u, v))}")
print(f"  T(u)+T(v)= {vadd(matvec(shear, u), matvec(shear, v))}"
      f"   equal: {matvec(shear, vadd(u, v)) == vadd(matvec(shear, u), matvec(shear, v))}")
print(f"  T(cu)    = {matvec(shear, vscale(c, u))}")
print(f"  c*T(u)   = {vscale(c, matvec(shear, u))}"
      f"   equal: {matvec(shear, vscale(c, u)) == vscale(c, matvec(shear, u))}")


def shifted(x):
    """(x, y) -> (x + 1, y): a translation, which is NOT linear."""
    return [x[0] + 1.0, x[1]]


print()
print("S is the shift (x, y) -> (x + 1, y). It is a perfectly good function")
print("and it is not linear:")
print(f"  S(0)          = {shifted([0.0, 0.0])}   (must be 0 for a linear map)")
print(f"  S(u)+S(v)     = {vadd(shifted(u), shifted(v))}")
print(f"  S(u+v)        = {shifted(vadd(u, v))}   differ, so S is not additive")
print("A translation is the standard non-linear map: it moves the origin, and")
print("a linear map must fix it. This is why `y = Wx + b` is an affine map, and")
print("why the bias `b` is not part of the linear structure.")

# ------------------------------------------------- matrix as a map
print()
print("=== Every matrix is a linear map, and vice versa ===")
A = [[1.0, 2.0, 3.0],
     [4.0, 5.0, 6.0],
     [7.0, 8.0, 10.0]]
print_matrix("A (3x3)", A)
print()
print("Read A three ways, and they agree:")
print("  as a machine: multiply a vector on the left")
print_vector("    A [1, 0, 2]", matvec(A, [1.0, 0.0, 2.0]))
print("  as a set of rules: one linear equation per row")
print(f"    row 0: 1*x0 + 2*x1 + 3*x2 = value for [1,0,2] is "
      f"{1 * 1 + 2 * 0 + 3 * 2}")
print("  as images of basis vectors: column j is T(e_j)")
for j in range(3):
    e_j = [1.0 if i == j else 0.0 for i in range(3)]
    print(f"    A e_{j} = {matvec(A, e_j)}")
print()
print("Any linear map on vectors of length 3 is determined by these three")
print("images, and the matrix that stores them is unique. So linear maps from")
print("R^n to R^m are in bijection with m x n matrices.")

# ------------------------------------------------- kernel and image
print()
print("=== Kernel and image, defined for any map ===")
print("ker(A) = {x : A x = 0}      the inputs that produce zero")
print("im(A)  = {A x}              every output the map can produce")
print()

B = [[1.0, 2.0, 3.0],
     [4.0, 5.0, 6.0],
     [7.0, 8.0, 10.0],
     [5.0, 7.0, 9.0]]       # row 3 = row 0 + row 1, so rank 3
print_matrix("B (4x3)", B)
r = rank(B)
print(f"rank {r}: ker has dimension {shape(B)[1] - r} and im has dimension {r}")
print()
ns = null_space(B)
print(f"ker basis has {len(ns)} vector(s) (the domain has {shape(B)[1]} "
      f"dimensions and the kernel keeps {shape(B)[1] - r} of them):")
for v in ns:
    print_vector("    v  =", v, width=8)
    print_vector("    B v =", matvec(B, v), width=8)
print("im basis (the pivot columns of B, which are outputs):")
for v in image_basis(B):
    print_vector("    ", v, width=8)

# A matrix with a genuinely nontrivial kernel: the same B with a fourth column
# equal to column 0 plus column 1.
C = [row + [row[0] + row[1]] for row in B]
print()
print_matrix("C (4x4, column 3 = column 0 + column 1)", C)
rc = rank(C)
print(f"rank {rc} of 4 columns, so ker has dimension {shape(C)[1] - rc} "
      f"and im has dimension {rc}")
ns_c = null_space(C)
print("ker basis (each vector vanishes):")
for v in ns_c:
    print_vector("    v  =", v, width=8)
    print_vector("    C v =", matvec(C, v), width=8)
print("v is the direction you can add to an input without changing the output.")
print("im basis (the pivot columns of C):")
for v in image_basis(C):
    print_vector("    ", v, width=8)

# Show im really is every reachable output.
print()
print("im is a span, so it is closed under scaling and adding:")
ib = image_basis(C)
print(f"  image basis has {len(ib)} vectors, so dim(im) = {len(ib)}")
p = [2.0, 3.0, -1.0, 4.0]
q = [-1.0, 0.5, 4.0, 0.25]
Ap = matvec(C, p)
Aq = matvec(C, q)
print(f"  C p       = {[round(v, 6) for v in Ap]}")
print(f"  C q       = {[round(v, 6) for v in Aq]}")
print(f"  C(p + q)  = {[round(v, 6) for v in matvec(C, vadd(p, q))]}")
print(f"  Cp + Cq   = {[round(v, 6) for v in vadd(Ap, Aq)]}   "
      f"equal: {matvec(C, vadd(p, q)) == vadd(Ap, Aq)}")
print(f"  3.5 * Cp  = {[round(v, 6) for v in vscale(3.5, Ap)]}")
print(f"  C (3.5 p) = {[round(v, 6) for v in matvec(C, vscale(3.5, p))]}")
print("im is closed by construction, since it is the span of the columns.")

# Show ker really is a subspace.
print()
print("ker is a subspace: zero is in it, and it is closed under the operations")
zero_in_ker = matvec(C, [0.0] * shape(C)[1]) == [0.0] * 4
v0, v1 = ns_c[0], ns_c[0]
sum_in_ker = matvec(C, vadd(v0, v1)) == [0.0] * 4
scale_in_ker = matvec(C, vscale(3.5, v0)) == [0.0] * 4
print(f"  C 0 = 0                   : {zero_in_ker}")
print(f"  C (v + v) = C v + C v = 0: {sum_in_ker}")
print(f"  C (3.5 v) = 3.5 * 0 = 0   : {scale_in_ker}")
print("Those three checks are the whole subspace test from lesson 30, applied to")
print("a set that is not given by a formula. Any set containing zero and closed")
print("under scaling and addition is a subspace, with no further conditions.")

# ------------------------------------------------- rank-nullity
print()
print("=== Rank-nullity: the dimension of the whole domain splits in two ===")
print("Every x decomposes uniquely as  x = x_img + x_ker,  where A x_img is in im")
print("and x_ker is in ker. That is why dim(ker) + dim(im) = n.")
print()
print(f"  n = {shape(C)[1]} columns")
print(f"  dim(ker) = {shape(C)[1] - rc}")
print(f"  dim(im)  = {rc}")
print(f"  sum      = {shape(C)[1] - rc} + {rc} = {shape(C)[1] - rc + rc}")
print()
print("Read it as degrees of freedom: a vector has n components, and the map")
print("destroys dim(ker) of them and keeps dim(im) of them. The kept part is")
print("recoverable if and only if the destroyed part is zero.")
print()
print("For C that means: adding t * [-1, -1, 0, 1] to any input changes nothing")
print("about the output. Inputs differing by such a vector are indistinguishable")
print("to the map, and the map has collapsed them onto the same point.")
```

### The decomposition, composition, and the chain rule

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


def matvec(M, v):
    rows, cols = shape(M)
    return [sum(M[i][k] * v[k] for k in range(cols)) for i in range(rows)]


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
    return null_space(transpose(A), tol)


def print_matrix(label, M, width=7):
    rows, cols = shape(M)
    print(f"{label}  ({rows}x{cols})")
    for row in M:
        print("  | " + " ".join(f"{x:{width}.3f}" for x in row) + " |")


# ------------------------------------------------- rank-nullity, proved
print("=== Rank-nullity, as a decomposition, verified numerically ===")
print("Every x splits uniquely into x = x_img + x_ker, where x_img is what the")
print("map can see and x_ker is what it throws away. Check it by brute force.")
print()

A = [[1.0, 2.0, 3.0],
     [2.0, 4.0, 6.0]]       # rank 1, so a big kernel
print_matrix("A (2x3, row 1 = 2 * row 0)", A)
r = rank(A)
ns = null_space(A)
print(f"rank {r}, so dim(im) = {r} and dim(ker) = {shape(A)[1] - r}")
print(f"kernel basis: {ns}")
for v in ns:
    print(f"  A v = {matvec(A, v)}")
print()
print("The row space is one-dimensional, spanned by (1, 2, 3), so every input")
print("splits as  x = c*(1, 2, 3) + x_ker  with x_ker in the kernel. Check that")
print("moving x by a kernel vector changes nothing about the output:")
row_dir = [1.0, 2.0, 3.0]
print(f"  A * (1, 2, 3) = {matvec(A, row_dir)}")
for c in (1.0, -3.5, 12.0):
    x_img = [c * t for t in row_dir]
    base = matvec(A, x_img)
    for v in ns:
        x = [x_img[i] + 2.0 * v[i] for i in range(3)]
        moved = matvec(A, x)
        same = all(abs(moved[i] - base[i]) < 1e-9 for i in range(2))
        print(f"  c = {c:6.1f}, add 2*{v}: A x = {[round(t, 6) for t in moved]}, "
              f"same as A x_img: {same}")
print()
print("Moving x by a kernel vector changes nothing about the output. That is the")
print("kernel's entire job, and it is why an under-determined system has many")
print("answers that all give the same predictions.")
print()
print(f"rank + nullity = {r} + {shape(A)[1] - r} = {r + shape(A)[1] - r} "
      f"= n = {shape(A)[1]}")
print("The two pieces partition the domain, so their dimensions must add to n.")

# ------------------------------------------------- invertibility, restated
print()
print("=== Invertibility is 'kernel trivial', and that is rank-nullity ===")
for label, M in [
    ("[[1, 2], [3, 4]]", [[1.0, 2.0], [3.0, 4.0]]),
    ("[[1, 2], [2, 4]]", [[1.0, 2.0], [2.0, 4.0]]),
    ("1x1 zero", [[0.0]]),
    ("1x1 [7]", [[7.0]]),
]:
    n = shape(M)[0]
    ker_dim = len(null_space(M))
    print(f"  {label:16s} rank {rank(M)}, dim(ker) {ker_dim}, "
          f"nullity = n - rank = {n - rank(M)}  matches: {ker_dim == n - rank(M)}")

print()
print("For a square map, ker = {0} exactly when dim(ker) = 0, which rank-nullity")
print("says is the same as dim(im) = n, which is the same as full rank, which")
print("is the same as det != 0. Four statements, one fact.")

# ------------------------------------------------- composition
print()
print("=== Composition: (T then S) is a map, and so is T after S ===")
T = [[1.0, 2.0], [0.0, 1.0]]          # shear
S = [[0.0, 1.0], [1.0, 0.0]]          # swap
x = [2.0, 5.0]
print_matrix("T (shear)", T)
print_matrix("S (swap)", S)
print(f"x = {x}")
print(f"  T x        = {matvec(T, x)}")
print(f"  S(T x)     = {matvec(S, matvec(T, x))}   (apply T, then S)")
print(f"  (S T) x    = {matvec(matmul(S, T), x)}")
print(f"  T(S x)     = {matvec(T, matvec(S, x))}   (apply S, then T)")
print(f"  (T S) x    = {matvec(matmul(T, S), x)}")
print("Order matters, as in lesson 31. Here the two orders differ, so S and T")
print("do not commute.")
print()
print("=== The chain rule is just composition ===")


def f(t):
    return t ** 2


def df(t):
    """The derivative of f at t."""
    return 2.0 * t


print("f(t) = t^2, so f'(t) = 2t. Consider the composed map g(v) = f(T v)[0].")
print(f"  T x            = {matvec(T, x)}")
print(f"  f(first entry) = {f(matvec(T, x)[0])}")
print(f"  d/dx of g      = f'(Tx[0]) * row 0 of T = "
      f"{df(matvec(T, x)[0])} * {[T[0][0], T[0][1]]} = "
      f"{[df(matvec(T, x)[0]) * t for t in T[0]]}")
print("The derivative of a composition is the composition of the derivatives,")
print("with the linear map acting on the gradient. That is the chain rule, and")
print("it is why backpropagation passes through matrices: (f o T)' = f' o T.")

# ------------------------------------------------- kernels in graphics
print()
print("=== Why a singular transform breaks graphics ===")
print("A 3D-to-2D projection that collapses a direction has a nonzero kernel,")
print("so two different 3-D points project to the same 2-D point. Two distinct")
print("points that look identical is exactly what you must avoid.")
print()
proj = [[1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0]]       # drops the z coordinate
print_matrix("projection (x, y, z) -> (x, y)", proj)
print(f"  rank {rank(proj)}, dim(ker) = {shape(proj)[1]} - {rank(proj)} = "
      f"{shape(proj)[1] - rank(proj)}")
ker = null_space(proj)
print(f"  kernel basis: {[[round(t, 6) for t in k] for k in ker]}")
p1 = [1.0, 2.0, 5.0]
p2 = [1.0, 2.0, 900.0]
print(f"  point A = {p1} -> {matvec(proj, p1)}")
print(f"  point B = {p2} -> {matvec(proj, p2)}")
print(f"  the same 2-D point, from points {abs(p2[2] - p1[2])} units apart in z")
print(f"  B - A = {[p2[i] - p1[i] for i in range(3)]}, which is "
      f"{(p2[2] - p1[2]) / ker[0][2]:.0f} * kernel basis")
print()
print("Add a fourth dimension and use the identity instead: no direction is")
print("lost, the kernel is trivial, and distinct points stay distinct.")
P = identity(4)
print_matrix("4x4 identity", P)
print(f"  rank {rank(P)}, dim(ker) = {shape(P)[1]} - {rank(P)} = 0")
print("This is why graphics pipelines carry a w coordinate through clip space:")
print("the perspective divide needs a dimension that survives.")

# ------------------------------------------------- the four spaces
print()
print("=== The four spaces, dimensions and sources ===")
M = [[1.0, 2.0, 3.0, 4.0],
     [5.0, 6.0, 7.0, 9.0],
     [2.0, 3.0, 4.0, 5.0]]
m, n = shape(M)
r = rank(M)
_, piv = rref(M)
Mrr, _ = rref(M)
row_b = [row for row in Mrr if any(abs(t) > TOL for t in row)]
col_b = [[M[i][c] for i in range(m)] for c in piv]
ker_b = null_space(M)
lker_b = left_null_space(M)
print_matrix("M (3x4)", M)
print(f"rank r = {r}, so {m} rows and {n} columns")
print(f"  column space   in R^{m}, dimension {len(col_b)}, basis = pivot columns {piv}")
print(f"  row space      in R^{n}, dimension {len(row_b)}, basis = nonzero RREF rows")
print(f"  kernel         in R^{n}, dimension {len(ker_b)} = n - r = {n} - {r}")
print(f"  left kernel    in R^{m}, dimension {len(lker_b)} = m - r = {m} - {r}")
print()
print(f"  r + (n - r) = {r + n - r} = n  (rank-nullity)")
print(f"  r + (m - r) = {r + m - r} = m  (the same, applied to M^T)")
print("Two numbers, one row reduction, four spaces. This table is the")
print("organisation of everything in this part.")
```

### With Libraries

```python
# The plain-Python implementations above are the definitions. numpy gives the
# same subspaces in one call, and adds the machinery for the applications:
# least squares, pseudoinverses, and SVD-based reductions.

import numpy as np

print("=== Matrix as a map: one call does everything ===")
A = np.array([[1.0, 2.0, 3.0],
              [4.0, 5.0, 6.0],
              [7.0, 8.0, 10.0]])
print(f"A =\n{A}")
v = np.array([1.0, 0.0, 2.0])
print(f"A @ v = {A @ v}")
print(f"shape {A.shape} means a map from R^{A.shape[1]} to R^{A.shape[0]}")

print()
print("=== rank, and the two subspaces, from numpy ===")
# A matrix with a genuine kernel: the 3x4 matrix from the worked example.
M = np.array([[1.0, 2.0, 3.0, 4.0],
              [5.0, 6.0, 7.0, 9.0],
              [2.0, 3.0, 4.0, 5.0]])
r = int(np.linalg.matrix_rank(M))
print(f"M =\n{M}")
print(f"M is {M.shape[0]}x{M.shape[1]}, rank {r}")
print(f"so the kernel has dimension {M.shape[1] - r} and the image {r}")

# A basis for the kernel: the vectors x with M x = 0. SVD gives them as the rows
# of V^T corresponding to the zero (or tiny) singular values.
u, s, vt = np.linalg.svd(M)
print(f"singular values = {s}")
print(f"the first {r} are the image directions, the rest are the kernel:")
print(f"  image basis (columns of U) =\n{np.round(u[:, :r], 6)}")
print(f"  kernel basis (rows of V^T) =\n{np.round(vt[r:, :], 6)}")

# Verify the kernel basis really is in the kernel.
for k in vt[r:, :]:
    print(f"  M @ {np.round(k, 6)} = {np.round(M @ k, 12)}")
print("Zero, as required. numpy gives you all four spaces from one SVD call,")
print("which is why SVD is the workhorse of lesson 40.")

print()
print("=== Image and kernel, computed the plain way, agree with SVD ===")
# Plain Python: RREF, then read off the pivot columns and free columns.
TOL = 1e-9


def rref(A, tol=TOL):
    Mx = [list(row) for row in np.asarray(A, dtype=float)]
    rows, cols = len(Mx), len(Mx[0])
    pivot_row = 0
    pivots = []
    for col in range(cols):
        best = None
        for i in range(pivot_row, rows):
            if abs(Mx[i][col]) > tol:
                best = i
                break
        if best is None:
            continue
        Mx[pivot_row], Mx[best] = Mx[best], Mx[pivot_row]
        p = Mx[pivot_row][col]
        Mx[pivot_row] = [v / p for v in Mx[pivot_row]]
        for i in range(rows):
            if i != pivot_row and Mx[i][col] != 0.0:
                f = Mx[i][col]
                Mx[i] = [Mx[i][c] - f * Mx[pivot_row][c] for c in range(cols)]
        pivots.append(col)
        pivot_row += 1
    return np.array(Mx), pivots


Mrr, piv = rref(M)
print(f"RREF pivot columns: {piv}")
print("column space basis (pivot columns of M) =")
print(np.array([[M[i][c] for i in range(M.shape[0])] for c in piv]))
print("row space basis (nonzero RREF rows) =")
print(Mrr)
print("Both have the same number of vectors, as row rank = column rank requires.")

print()
print("=== The kernel is exactly what makes the solve non-unique ===")
# A tall system: 5 equations, 3 unknowns, built to be consistent.
consistent = np.array([
    [1.0, 0.0, 1.0],
    [0.0, 1.0, 1.0],
    [1.0, 1.0, 2.0],   # = row 0 + row 1
    [2.0, 1.0, 3.0],
    [1.0, 2.0, 3.0],
])
b_consistent = consistent @ np.array([1.0, 2.0, 3.0])   # built to be consistent
rank_c = int(np.linalg.matrix_rank(consistent))
print(f"system is {consistent.shape[0]}x{consistent.shape[1]}, rank {rank_c}")
print(f"free unknowns = {consistent.shape[1]} - {rank_c} = "
      f"{consistent.shape[1] - rank_c}")
x_ls, residuals, _, _ = np.linalg.lstsq(consistent, b_consistent, rcond=None)
print(f"b = consistent @ [1, 2, 3] = {b_consistent}, built to be consistent")
print(f"lstsq gives the minimum-norm solution {np.round(x_ls, 6)}")
print(f"  residuals {np.round(consistent @ x_ls - b_consistent, 12)}")
print("  A consistent system has residuals all zero for every solution, so the")
print("  residuals cannot tell you which solution you got.")
print()
print(f"Rank-nullity: unknowns minus rank = {consistent.shape[1]} - {rank_c} = "
      f"{consistent.shape[1] - rank_c} free unknown. So the solution set is a")
print("line, and lstsq returns one particular point of it: the one nearest the")
print("origin. Add t times the kernel vector for any other solution, and the")
print("residuals stay zero:")
_, _, vt_c = np.linalg.svd(consistent)
k_dir = vt_c[rank_c, :]
print(f"  kernel direction = {np.round(k_dir, 6)}, norm {np.linalg.norm(k_dir):.4f}")
print(f"  consistent @ kernel direction = {np.round(consistent @ k_dir, 12)}")
print(f"  norm of the lstsq solution = {np.linalg.norm(x_ls):.4f}")
for t in (1.0, -1.0):
    y = x_ls + t * k_dir
    print(f"  t = {t:+.1f}: x = {np.round(y, 6)}, norm {np.linalg.norm(y):.4f} "
          f"(larger), residuals {np.round(consistent @ y - b_consistent, 12)}")

print()
print("=== A singular system: least squares and the pseudoinverse ===")
singular = np.array([[1.0, 2.0, 3.0],
                     [2.0, 4.0, 6.0]])     # rank 1
b_sing = np.array([1.0, 2.0])
print(f"singular system (2x3, rank {int(np.linalg.matrix_rank(singular))}):")
print(f"  A = {singular.tolist()}, b = {b_sing.tolist()}")
x_pinv, _, _, _ = np.linalg.lstsq(singular, b_sing, rcond=None)
print(f"  lstsq / pseudoinverse solution = {np.round(x_pinv, 6)}")
print(f"  residuals = {np.round(singular @ x_pinv - b_sing, 12)}")
print("  residuals are zero because the system is consistent.")
print("  but the solution is not unique: adding any multiple of a kernel vector")
print("  gives another solution. lstsq picks the one with smallest norm.")
pinv = np.linalg.pinv(singular)
print("  pseudoinverse =")
print(np.round(pinv, 6))
print(f"  A @ A^+ @ b = {np.round(singular @ pinv @ b_sing, 6)}")
print("The pseudoinverse is the least-squares answer for every b, and it")
print("minimises the norm of x among all minimisers. That is a choice the")
print("problem does not make for you, which is why regularisation is added.")

print()
print("=== Composition and the chain rule, numerically ===")
# d/dx of f(T x) for f(t) = t^2: the Jacobian is 2*(T x)[0] * T, by the chain rule.
T = np.array([[1.0, 2.0], [0.0, 1.0]])
x = np.array([2.0, 5.0])
f = lambda t: t ** 2
f_prime = lambda t: 2.0 * t
Tx = T @ x
print(f"T x = {Tx}, f(Tx[0]) = {f(Tx[0])}")
# Jacobian of g(x) = f((T x)[0]) with respect to x:
jacobian = f_prime(Tx[0]) * T[0, :]
print(f"Jacobian of g = f'(Tx[0]) * row 0 of T = {jacobian}")
# Verify against a finite difference.
eps = 1e-7
for j in range(2):
    e = np.zeros(2)
    e[j] = eps
    fd = (f((T @ (x + e))[0]) - f((T @ (x - e))[0])) / (2 * eps)
    print(f"  finite difference in x[{j}]: {fd:.6f}   analytic: {jacobian[j]:.6f}")
print("The chain rule is composition: the gradient of a composite passes")
print("through the linear map as a matrix. Backpropagation is this, run")
print("backwards through a stack of them.")

print()
print("=== Rank-nullity as a numeric fact, for a range of shapes ===")
print(f"  {'shape':>8}  {'rank':>4}  {'nullity':>7}  {'left nullity':>12}")
rng = np.random.default_rng(0)
for m, n in [(1, 1), (3, 3), (4, 3), (3, 4), (6, 6), (10, 4)]:
    # Rank-2 matrix: sum of two outer products.
    u1 = rng.standard_normal(m)
    v1 = rng.standard_normal(n)
    u2 = rng.standard_normal(m)
    v2 = rng.standard_normal(n)
    Mat = np.outer(u1, v1) + np.outer(u2, v2)
    rr = int(np.linalg.matrix_rank(Mat))
    print(f"  {f'{m}x{n}':>8}  {rr:>4}  {n - rr:>7}  {m - rr:>12}")
print("Every row satisfies rank + nullity = n and rank + left nullity = m.")
print("Note that nullity is bounded by n, so a matrix with many more rows than")
print("columns has a large kernel and many unidentifiable directions.")
```

## Common Mistakes

**Mistake 1: treating `y = Wx + b` as a linear map.** The wrong version: "a neural
layer is linear." The right version: `x ↦ Wx` is linear; `x ↦ Wx + b` is affine.
The bias moves the origin, and a linear map must fix it. This matters when you
reason about what a layer does to a subspace — an affine map does not preserve
them, and the output layer's bias in particular breaks any symmetry argument
about the network.

**Mistake 2: confusing the row space with the domain.** The wrong version:
"`x_im` is the part of `x` in the row space of the RREF." The right version: the
decomposition `x = x_img + x_ker` is found by extending a kernel basis to a basis
of the *domain*. The row space lives in the codomain, and using it produces an
`x_im` that does not map to the right place. The dimensions still come out right,
which is why the error survives a casual check.

**Mistake 3: expecting `ker(S∘T)` to be `ker(S) + ker(T)`.** The wrong version:
"a composition kills everything either map kills." The right version:
`ker(S ∘ T) = {x : T(x) ∈ ker(S)}`, the *preimage* of the kernel, which can be
much larger than either kernel. Two invertible maps composed have trivial kernel;
two singular maps composed can lose more dimensions than either one alone.

**Mistake 4: reading a rank drop as a numerical accident.** The wrong version:
"the rank changed when I switched to float32, so the implementation is
buggy." The right version: a small singular value is exactly the case where the
kernel is real in exact arithmetic and invisible in floating point. Report the
singular values and the threshold, as lesson 34 said.

**Mistake 5: treating `lstsq` on a rank-deficient system as "the" answer.** The
wrong version: "the coefficients are `np.linalg.lstsq(A, b)`." The right version:
those coefficients are the minimum-norm minimiser, which is a *choice* made by
the algorithm, not something the data determined. Adding any multiple of a kernel
vector gives an equally good fit. If you need a stable, interpretable, or
reproducible answer, add a regulariser and say so.

---

## Formula Sheet

`V`, `W` are vector spaces; `T : V → W` is a map; `A` is the `m × n` matrix
representing it; `u, v ∈ V` are inputs; `c`, `α`, `β` are scalars; `0` is the zero
vector of the relevant space; `T⁻¹` is an inverse map; `S` is a second map; `r` is
`rank(A)`.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| Linearity | `T(u + v) = T(u) + T(v)` and `T(cu) = cT(u)` | Respects adding and scaling. Equivalently `T(αu + βv) = αT(u) + βT(v)`. | Testing any candidate map |
| `T(0) = 0` | follows from additivity alone: `T(0) = 2T(0)` | A linear map must fix the origin. | Fastest linearity test |
| Affine map | `x ↦ Ax + b` with `b ≠ 0` | Same thing, shifted. **Not** linear: it moves the origin. | Neural layers with bias |
| Matrix of a linear map | `A = (T(e_1) \| … \| T(e_n))`, so `T(x) = Ax` | Column `j` is the image of basis vector `j`. Bijective with `m × n` matrices. | Building a map from its action |
| `ker(T)` | `\{x ∈ V : T(x) = 0\}`, dim `n − r` | Inputs the machine throws away. A **subspace** of `V`. | Collapsing dimensions, identifiability |
| `im(T)` | `\{T(x) : x ∈ V\} = span(columns of A)`, dim `r` | Everything the machine can produce. A **subspace** of `W`. | Reachability, output dimension |
| Kernel basis | free columns of `rref(A)` | One vector per free variable, from the **reduced** matrix. | Computing `ker` |
| Image basis | **pivot columns of the original `A`** | Not of the RREF — the classic mix-up. | Computing `im` |
| Rank-nullity | `dim ker(T) + dim im(T) = dim V` | Destroyed plus kept equals the original count. | The organising identity |
| First isomorphism | `im(T) ≅ V / ker(T)` | The only thing distinguishing two inputs is their difference *modulo* the kernel. | Why kernel directions are unidentifiable |
| `T` injective | `⟺ ker(T) = \{0\}` | One-to-one: no two inputs collide. | Model identifiability |
| `T` surjective | `⟺ im(T) = W` | Onto: every output reached. | Feasibility of a target |
| `T` isomorphism | injective **and** surjective; automatic when `dim V = dim W` | Fully reversible. | `rank = n` |
| `T` invertible | `∃ T⁻¹` with `T⁻¹T = id_V`, `TT⁻¹ = id_W` | Undoable. Needs both halves. | Solving by applying an inverse |
| Square invertibility chain | `ker(A) = \{0\} ⟺ det(A) ≠ 0 ⟺ rank(A) = n ⟺ A⁻¹ exists` | Four statements, one fact. Valid only for square `A`. | Quick invertibility test |
| Right inverse | `∃ R` with `T R = id_W` always when `T` is surjective | A choice of preimage per output. | Least-squares as a right inverse |
| Left inverse | `∃ L` with `L T = id_V` only when `T` is injective | Undoes the map on everything. | Uniqueness of solutions |
| Restriction | `U ⊆ V` ⟹ `T(U)` subspace of `im T`, `ker(T|_U) = ker(T) ∩ U` | A map on a subspace. | Analysing a sub-block |
| Composition | `(S ∘ T)(x) = S(T(x))`, matrix `S A` | Chaining machines is multiplying matrices. | Deep networks, nested loops |
| `ker(S ∘ T)` | `= T⁻¹(ker S) = \{x : T(x) ∈ ker S\}`, a **preimage** | Not `ker S + ker T`; the two kernels live in different spaces. | What a chain of layers destroys |
| `im(S ∘ T)` | `= S(im T)` | You can only pass on what you were handed. | What a chain produces |
| Invertible composition | `S, T` both invertible ⟹ `ker(S∘T) = \{0\}` | Nothing destroyed if nothing destroyed. | Mistake 3's correction |
| Domain decomposition | `x = x_im + x_ker` uniquely, with `A x_ker = 0` | The part you can see plus the part you cannot. | Interpreting a rank-deficient model |
| Adapted basis | extend a `ker(T)` basis to a basis of `V` | The correct way to get the decomposition. | Mistake 2's correction |
| Minimum-norm fit | `t* = -(x_p · v)/\|v\|²` on `x = x_p + t v` | The foot of the perpendicular, not `t = 0`. | What `lstsq` returns |
| Chain rule | `(f ∘ T)' = f' ∘ T` | Derivative of a composition is a composition. | Backpropagation |
| Backprop rule | `∂L/∂x = Wᵀ (∂L/∂y)` for `y = Wx` | Row gradient contracts the *columns* of `W`, hence the transpose. | Every layer of every network |
| Order reversal | `(W₂W₁)ᵀ = W₁ᵀW₂ᵀ` | Reversing a chain reverses the order. | Why depth matters |
| Collapsing projection | `P(x,y,z) = (x,y)`, `ker P = span{(0,0,1)}` | Distinct 3-D points land on one 2-D point. | Why graphics carries a `w` coordinate |
| Rank drop under float32 | not a bug: a small singular value is a real kernel in exact arithmetic | | Mistake 4; report singular values |

## Multiple Choice Questions

**Q1.** A map `T : ℝ³ → ℝ³` is `T(x) = Ax` with `A` of rank 2. What can you
conclude?

- A) `ker(T)` has dimension 2 and `im(T)` has dimension 2
- B) `ker(T)` has dimension 1 and `im(T)` has dimension 2
- C) `ker(T)` has dimension 3 and `im(T)` has dimension 1
- D) `ker(T)` is `{0}`, since `T` maps a space to itself

<details>
<summary>Answer and explanation</summary>

**B) `ker(T)` has dimension 1 and `im(T)` has dimension 2.**

`im(T)` is the column space, so `dim im(T) = rank = 2` — the row-rank-equals-
column-rank theorem from
[lesson 34](34_basis_dimension_rank.md) restated in map language. Rank-nullity
then forces `dim ker(T) = 3 − 2 = 1`. The lesson's code checks exactly this on the
`2 × 3` matrix of rank 1 (`dim ker = 2`, `dim im = 1`) and on the `4 × 4` matrix
`C` of rank 3 in four columns (`dim ker = 1`, `dim im = 3`).

- A) puts the kernel dimension equal to the rank, which is the misconception that
  rank-nullity exists to kill. The two coincide only when `n = 2r`.
- C) is wrong twice, yet still satisfies `dim ker + dim im = 3` — the trap. The
  identity constrains only the sum, so a wrong pair can pass an arithmetic check.
  `dim im` is not "the rank minus one"; it *is* the rank, because the image is the
  column space.
- D) is a real and seductive thought: a map from a space to *itself* sounds
  invertible. Invertibility needs `ker = {0}`, and a rank-2 map on `ℝ³` has a
  one-dimensional kernel, so its image is a plane strictly inside `ℝ³`.

</details>

**Q2.** For a linear map `T`, which statement about `T(0)` is correct?

- A) `T(0) = 0` always, and it follows from the linearity axioms alone
- B) `T(0) = 0` only if `T` is injective
- C) `T(0)` can be any vector, since linearity only constrains `T(u)` for `u ≠ 0`
- D) `T(0) = 0` is the definition of an affine map

<details>
<summary>Answer and explanation</summary>

**A) `T(0) = 0` always, and it follows from the linearity axioms alone.**

Take `u = v = 0` in additivity: `T(0) = T(0 + 0) = T(0) + T(0) = 2T(0)`, and
subtracting `T(0)` in the vector space `W` gives `T(0) = 0`. No injectivity or
surjectivity is needed — it is a *consequence*, not an extra hypothesis. The
lesson turns it into a one-line test: the shift `(x, y) ↦ (x+1, y)` returns
`[1.0, 0.0]` at the origin, so it is not linear.

- B) is a non-relation. `T(0) = 0` holds for maps with a large kernel — the
  lesson's rank-1 `2 × 3` matrix has a 2-dimensional kernel and satisfies it — and
  for the zero map, which is maximally non-injective. Injectivity is strictly
  stronger.
- C) is the belief that makes an affine map look linear. Linearity constrains
  `T` at *every* input including zero, and the code shows additivity failing too:
  `S(u) + S(v) = [7.0, -1.0]` while `S(u+v) = [6.0, -1.0]`.
- D) inverts the two. Affine maps are exactly the ones that *can* move the origin;
  a map with `b ≠ 0` has `T(0) = b ≠ 0`, which is what disqualifies it. Mistake 1
  is this confusion about `y = Wx + b`.

</details>

**Q3.** `T` and `S` are linear with `ker(T) = {0}` and `ker(S) = {0}`. What is
`ker(S ∘ T)`?

- A) `ker(S) + ker(T) = {0}`
- B) `{0}`, since a composition of maps that each destroy nothing also destroys
  nothing
- C) `T⁻¹(ker S)`, which is strictly larger than `{0}` in general
- D) It cannot be determined without knowing `dim V` and `dim W`

<details>
<summary>Answer and explanation</summary>

**B) `{0}`, since a composition of maps that each destroy nothing also destroys
nothing.**

The general formula is `ker(S ∘ T) = T⁻¹(ker S) = {x : T(x) ∈ ker S}`. With
`ker S = {0}` this is `{x : T(x) = 0} = ker T = {0}`. Directly: if
`(S∘T)(x) = 0` then `S(T(x)) = 0`, so `T(x) = 0` since `S` is injective, so `x = 0`
since `T` is injective.

- A) is Mistake 3, and note it lands on the right *answer* by accident — which is
  what makes it dangerous. The rule `ker S + ker T` is not merely wrong in
  general, it is not even well typed: `ker S ⊆ W` and `ker T ⊆ V`. Taking the
  product rule as a substitute for the preimage rule will fail as soon as either
  map is singular.
- C) is the correct *formula* with the wrong *evaluation*. `T⁻¹(ker S)` is right
  in general, and `ker T ⊆ T⁻¹(ker S)` always, but with `ker S = {0}` the
  preimage is exactly `ker T = {0}`. So "strictly larger" cannot hold here.
- D) is false: no dimensions are needed. The two injectivity hypotheses are exactly
  what is required, and the conclusion is immediate.

</details>

**Q4.** Why does the decomposition `x = x_im + x_ker` require extending a kernel
basis to a basis of the *domain*, rather than reading the row space of the RREF?

- A) Because the row space of the RREF is a subspace of the codomain, so a vector
  taken from it need not map to the right place
- B) Because the row space has dimension `r` and `x_im` must have dimension
  `n − r`
- C) Because the kernel basis must be orthogonal to the row space basis, which row
  reduction does not guarantee
- D) Because the RREF is numerically unstable, so its rows should never be used

<details>
<summary>Answer and explanation</summary>

**A) Because the row space of the RREF is a subspace of the codomain, so a vector
taken from it need not map to the right place.**

`x` and `x_ker` both live in the domain `V`. The row space of a matrix is a
subspace of `ℝ^n` too — which is why the error is so easy to make — but it is the
wrong `ℝ^n`: for an `m × n` matrix the row space indexes columns while the image
lives in `ℝ^m`, and the RREF's rows are reduced representatives, not a complement
to the kernel. The correct construction is the first-isomorphism one: take a
kernel basis, extend it to a basis of `V`, and the remaining vectors span the
complement. The lesson's worked example finds a wrong `x_im` this way and catches
it only because `A x_im ≠ A x`.

- B) has the dimensions backwards, which is worth checking deliberately. The
  complement has dimension `dim V − dim ker = r`, so `x_im` has dimension `r` and
  `x_ker` has `n − r`. The row space also has dimension `r`, so a dimension check
  cannot catch this error — which is exactly why the lesson warns that "the
  dimensions still come out right".
- C) is a non-requirement. Nothing in the decomposition asks for orthogonality.
  Any independent vectors complete a kernel basis; no inner product is involved
  and row reduction supplies none.
- D) is false as a reason. Row reduction reliably computes the row space *as a
  set*. The error is conceptual: a codomain subspace was fed into a domain-side
  decomposition.

</details>

**Q5.** A map `T : ℝ⁴ → ℝ²` has `im(T) = ℝ²`. What does that imply?

- A) `T` is injective, so `ker(T) = {0}`
- B) `T` is surjective, and `dim ker(T) = 2` by rank-nullity
- C) `T` is an isomorphism, because its image equals its codomain
- D) `T` is invertible, so a matrix `T⁻¹` exists

<details>
<summary>Answer and explanation</summary>

**B) `T` is surjective, and `dim ker(T) = 2` by rank-nullity.**

`im(T) = W` is the definition of surjective, and rank-nullity gives
`dim ker(T) = dim V − dim im(T) = 4 − 2 = 2`. So `T` is onto and definitely not
one-to-one. The lesson's graphics projection `(x,y,z,w) ↦ (x,y)` is the concrete
case: it reaches every point of `ℝ²` while discarding two dimensions.

- A) reverses the two. `ker(T) = {0}` is injectivity, and a kernel of dimension 2
  means infinitely many inputs share an output. `S(u) = S(v)` whenever
  `u − v ∈ ker S`, which is the identity the lesson uses to prove the equivalence.
- C) confuses surjective with isomorphism. An isomorphism needs **both**, and
  rank-nullity makes them equivalent only when `dim V = dim W`. Here `4 ≠ 2`, so
  the two are provably different properties.
- D) goes one step further, and it is worth being precise. A *right* inverse `R`
  with `T R = id_W` does exist — that is exactly a choice of preimage per output.
  A *left* inverse cannot, since `T(L T v) = T v` for all `v` would force `T`
  injective. "Invertible" means both sides, i.e. `ker = {0}` and `im = W`.

</details>

**Q6.** For `A = [[1, 2, 3], [2, 4, 6]]`, what is the image of the map and what
does the kernel contain?

- A) `im(A) = span{(1,2)}` and `dim ker(A) = 2`
- B) `im(A) = span{(1,2,3)}` and `dim ker(A) = 1`
- C) `im(A) = ℝ³` and `dim ker(A) = 0`
- D) `im(A) = {0}` and `dim ker(A) = 3`

<details>
<summary>Answer and explanation</summary>

**A) `im(A) = span{(1,2)}` and `dim ker(A) = 2`.**

Row 1 is twice row 0, so `rank = 1`. The image is the span of the columns, and
the columns are `(1,2)ᵀ`, `(2,4)ᵀ`, `(3,6)ᵀ` — all multiples of `(1,2)ᵀ`. So
`im(A)` is a **line** in `ℝ²`, and rank-nullity gives `dim ker(A) = 3 − 1 = 2`. The
code prints the kernel basis `[-2, 1, 0]` and `[-3, 0, 1]` and verifies `A v = 0`
for each.

- B) has the wrong space. `span{(1,2,3)}` is a line in `ℝ³`, but `A` is `2 × 3` so
  its image lies in `ℝ²`. The line `span{(1,2,3)}` is the **row space**, not the
  image — which is the lesson's own decomposition, restated in map language.
- C) is impossible twice over: `im(A)` is a subspace of `ℝ²` and so could not be
  `ℝ³` even at full rank, and rank-nullity would then need `dim ker = 0`,
  contradicting `rank = 1`.
- D) is a null matrix, and this one is not: `A e₀ = (1, 2)ᵀ ≠ 0`. For a nonzero
  matrix the image is never `{0}`, since a nonzero column *is* an output.

</details>

**Q7.** A graphics pipeline uses `P(x, y, z) = (x, y)`, and two distinct 3-D points
900 units apart in `z` project to the same 2-D point. What has gone wrong?

- A) `P` is nonlinear, because it discards a coordinate
- B) `P` is linear but has a nontrivial kernel containing `(0, 0, 1)`, so the two
  points differ by a vector the map cannot see
- C) `P` is singular in the sense that `det(P) = 0`, which is undefined for a
  non-square matrix
- D) The outputs should differ slightly, so this is a rounding artefact

<details>
<summary>Answer and explanation</summary>

**B) `P` is linear but has a nontrivial kernel containing `(0, 0, 1)`, so the two
points differ by a vector the map cannot see.**

`P` is the matrix `[[1,0,0],[0,1,0]]`, so `P(u+v) = Pu + Pv` and `P(cu) = cPu`:
perfectly linear, rank 2, `dim ker = 3 − 2 = 1`. The lesson's code prints
`kernel basis: [[0, 0, 1]]`, then shows `B − A = (0, 0, 895)`, which is exactly
895 times the kernel basis, and that both points map to the same output. Two
distinct points that look identical is the failure — and a *linear* map causes
it, which is why the lesson notes that clip space carries a `w` coordinate to give
the perspective divide a dimension that survives.

- A) is false and is the natural wrong guess. Dropping a coordinate is a matrix
  multiplication, hence linear. Affineness, not nonlinearity, is what moves the
  origin; the code's shift map is the counterexample there.
- C) attaches the word "singular" to the wrong concept. `det` is undefined for a
  non-square matrix, as [lesson 33](33_determinant_and_inverse.md) states. The
  right vocabulary is "not injective" or "has a nontrivial kernel", and the
  geometric reading is *lossy* rather than singular.
- D) is a plausible engineering guess worth dismissing carefully: the outputs are
  *exactly* equal because the difference lies entirely in the kernel. No numerical
  precision recovers the lost coordinate — the information is not in the data.

</details>

**Q8.** Backpropagation through a layer `y = Wx` passes the gradient back as
`Wᵀ g`. Why the transpose rather than `W`?

- A) Because the chain rule says the derivative of a composition is a composition,
  and premultiplying a row gradient by `Wᵀ` is what implements it
- B) Because `W` is not differentiable and `Wᵀ` is
- C) Because gradients must be row vectors, and `W` acts on column vectors
- D) Because `WᵀW = I` for a weight matrix

<details>
<summary>Answer and explanation</summary>

**A) Because the chain rule says the derivative of a composition is a
composition, and premultiplying a row gradient by `Wᵀ` is what implements it.**

The chain rule for a composition is `(f ∘ T)' = f' ∘ T`, and for `T(x) = Wx` the
derivative of `T` is `T` itself, so `∂L/∂x = Wᵀ (∂L/∂y)`. Concretely, with
`g = (g₁, …, g_m)` and `W` written row-wise, `∂L/∂x_j = Σ_i g_i w_ij` — a sum over
the **rows** of `W` weighted by `g`, which as a matrix product is `Wᵀ g`. This is
[lesson 31](31_matrices_and_matrix_algebra.md)'s `(AB)ᵀ = BᵀAᵀ` in a gradient
computation, and the lesson's "Why Computer Science Cares" bullet says exactly
that.

- B) is false: `W` is a constant, so it is trivially differentiable, and the
  transpose has nothing to do with differentiating `W`.
- C) confuses a storage convention with a mathematical necessity. Gradients can be
  written as rows or columns; the transpose is there because of how the
  contraction lines up, not because of how you store things. Keep them as columns
  and the same `Wᵀg` appears.
- D) is false — `WᵀW = I` is a *singular value* relation, not a weight-matrix
  identity, and nothing in a network guarantees it. Assuming it would be assuming
  orthogonal weights, which is a special case.

</details>

**Q9.** `np.linalg.lstsq(A, b)` returns a solution for rank-deficient `A`. What is
the most accurate description of the returned vector?

- A) The unique solution, because `lstsq` solves rather than approximates
- B) The minimum-norm minimiser: a valid solution when one exists and a
  least-squares fit when none does, chosen to be the point closest to the origin
- C) The solution with the fewest nonzero entries, found by Gaussian elimination
- D) The average of all solutions, which is well defined for a singular system

<details>
<summary>Answer and explanation</summary>

**B) The minimum-norm minimiser: a valid solution when one exists and a
least-squares fit when none does, chosen to be the point closest to the origin.**

`lstsq` minimises `‖Ax − b‖` over `x`, and that minimiser is *unique* even when
the solution set of `Ax = b` is a whole line, because the objective is strictly
convex along the kernel direction. The point it returns is the perpendicular foot:
writing `x(t) = x_p + t v`, the objective is `‖x_p‖² + 2t(x_p·v) + t²‖v‖²`,
minimised at `t* = -(x_p·v)/‖v‖²`, which is generally not `0`. So the answer is a
*choice* among equally good solutions, and adding any multiple of a kernel vector
also minimises but is not what came back.

- A) takes the function's name at face value. It is a least-squares routine, and
  when the system is inconsistent its output is not a solution at all — the
  residual is the evidence, per
  [lesson 32](32_linear_systems_gaussian_elimination.md).
- C) confuses two algorithms. Sparsity is `l1` regularisation (LASSO), not
  elimination, and it is not what `lstsq` does.
- D) is a real question with the same answer, but stated wrongly. On a line the
  closest point to the origin *is* the mean of any two symmetric points about it,
  so "the average" colloquially identifies the right vector — but a mean over an
  infinite set is not defined. The honest statement is the minimiser of a norm,
  which is defined for every `x`. Mistake 5 is treating the returned coefficients
  as "the" answer.

</details>

**Q10.** A `3 × 3` matrix has `det(A) = 0` and `rank(A) = 2`. Which must be true?

- A) `ker(A)` has dimension 3 and `im(A)` has dimension 0
- B) `ker(A)` has dimension 1, and `A` is not invertible but `Ax = b` has
  infinitely many solutions whenever it has any
- C) `A` is not invertible and `Ax = b` has no solution for any `b`
- D) `rank(A) = 2` contradicts `det(A) = 0`, since the determinant would then be
  nonzero

<details>
<summary>Answer and explanation</summary>

**B) `ker(A)` has dimension 1, and `A` is not invertible but `Ax = b` has
infinitely many solutions whenever it has any.**

Rank-nullity gives `dim ker(A) = 3 − 2 = 1`, and `det(A) = 0` gives
non-invertibility. If `x₀` is any solution of `Ax = b` and `v ≠ 0` spans
`ker(A)`, then `A(x₀ + tv) = b` for every real `t`, so there are infinitely many.
`det = 0` says "not exactly one solution", and with `rank = 2` the infinite case
is what happens whenever a solution exists at all.

- A) puts the whole kernel in and nothing in the image, which would mean
  `rank = 0`. The pair must sum to `3`: `1 + 2` does, `3 + 0` does not.
- C) is the error [lesson 33](33_determinant_and_inverse.md) spends a lot of space
  on: the determinant is a property of `A` and never sees `b`. `A = [[1,2],[2,4]]`
  with `b = (2,4)` is a consistent, infinitely-many-solutions system with a
  singular `A`.
- D) treats the two facts as contradictory when they are consistent. A singular
  matrix can have any rank below `n`; the determinant collapses all of that to one
  bit, which is precisely why
  [lesson 34](34_basis_dimension_rank.md) exists — it says the determinant cannot
  distinguish rank 0 from rank `n − 1`.

</details>

## Subjective Questions

### Short Answer

**Q1. State the two axioms of linearity, and show that they force `T(0) = 0`.**

<details>
<summary>Model answer</summary>

A map `T : V → W` is **linear** if for all `u, v ∈ V` and scalars `c`:

    T(u + v) = T(u) + T(v)      (additivity)
    T(cu)    = cT(u)             (homogeneity)

`T(0) = 0` follows from additivity alone. Take `u = v = 0`:
`T(0) = T(0 + 0) = T(0) + T(0) = 2T(0)`, and subtracting `T(0)` from both sides
in `W` gives `T(0) = 0`. Equivalently, `T(c·0) = c·T(0)` gives
`T(0) = c T(0)` for all `c`, and `c = 0` gives `T(0) = 0`.

So a linear map must fix the origin, which is the fastest way to disqualify a
candidate: compute `T(0)` first. The lesson's shift `(x, y) ↦ (x+1, y)` returns
`[1.0, 0.0]` and is therefore not linear — it is *affine*, which describes
`y = Wx + b` with `b ≠ 0` and therefore every neural layer with a bias.

</details>

**Q2. Define the kernel and the image of a linear map, and say where a basis for
each comes from when the map is a matrix.**

<details>
<summary>Model answer</summary>

    ker(T) = {x ∈ V : T(x) = 0}       the inputs the map throws away
    im(T)  = {T(x) : x ∈ V}           every output the map can produce

Both are subspaces: `T(0) = 0` puts `0` in the kernel, and `T(u+v) = T(u) + T(v)`
and `cT(u) = T(cu)` show closure under addition and scaling in both cases.

For a matrix `A` the two come from different matrices, and this is the point to
remember:

- `im(A)` is the **column space**, so a basis is the pivot columns of the
  **original** `A`.
- `ker(A)` comes from the RREF: one basis vector per free column, obtained by
  setting that free variable to `1` and reading the pivot entries off the reduced
  rows.

Taking the image basis from the RREF gives you unit vectors in `ℝ^n` that have
nothing to do with the machine's actual outputs.

</details>

**Q3. State rank-nullity in map language, and say what it means for a model.**

<details>
<summary>Model answer</summary>

    dim(ker T) + dim(im T) = dim V

For a matrix `A` this is `rank(A) + nullity(A) = n`, with `n` the number of
columns. The structural reason: choose a basis `b₁, …, b_k` of `ker(T)` and
extend it to `b₁, …, b_n` of `V`. The first `k` map to zero; the remaining `n − k`
map to linearly independent vectors spanning `im(T)` (a combination giving zero
would be a dependence in the kernel, which the `b_i` do not have). So
`dim im(T) = n − k` and the sum is `n`.

For a model, the input space splits in two: `dim ker T` dimensions are destroyed
and `dim im T` are kept. A model with a one-dimensional kernel on three features
cannot identify three coefficients — one combination of them is unconstrained and
every point on that line fits identically. The lesson's example has kernel vector
`[-10, -20, 1]`: raise hours by 10, lower attendance by 20, raise score by 1, and
no prediction changes.

</details>

**Q4. State the relationship between injectivity, surjectivity, and
invertibility, and say when the three coincide.**

<details>
<summary>Model answer</summary>

- `T` is **injective** iff `ker(T) = {0}`, since `T(u) = T(v) ⟺ T(u − v) = 0`.
- `T` is **surjective** iff `im(T) = W`.
- `T` is **invertible** iff both hold, equivalently iff `T⁻¹` exists with
  `T⁻¹T = id_V` and `TT⁻¹ = id_W`.

When `dim V = dim W`, rank-nullity makes injectivity and surjectivity equivalent:
`dim ker + dim im = n`, so one is `0` exactly when the other is `n`. Such a `T`
is an **isomorphism**. When the dimensions differ they are genuinely different:
`(x,y,z,w) ↦ (x,y)` is onto `ℝ²` with a 2-dimensional kernel.

The asymmetry that matters for `Ax = b`: a *right* inverse exists whenever `T` is
surjective (choose a preimage for each `b`), but a *left* inverse requires
injectivity. So "solvable for every `b`" and "uniquely solvable" are two different
questions whenever `dim V ≠ dim W`.

</details>

**Q5. State the composition rules for kernels and images, and explain why the
kernel rule involves a preimage rather than a sum.**

<details>
<summary>Model answer</summary>

For linear `T : V → W` and `S : W → X`:

    ker(S ∘ T) = T⁻¹(ker S) = {x : T(x) ∈ ker S}
    im(S ∘ T)  = S(im T)

The kernel rule is a preimage because the condition is stated on `T`'s **output**:
the composition kills `x` exactly when `T` sends `x` into the set that `S` kills.
`ker T ⊆ T⁻¹(ker S)` always, since `T` maps `ker T` to `0` and `0 ∈ ker S`.

A sum would be the wrong shape for two reasons. `ker S ⊆ W` and `ker T ⊆ V`, so
`ker S + ker T` is not even well typed unless the spaces coincide. And
conceptually, `S` and `T` do not both act on the input: an input can be entirely
unmolested by `T` and still be killed by the composition, because `T` steered it
into `ker S`. Nothing about such an input is in `ker T`.

The image rule is an image because a composition can only pass on what it was
handed. Two consequences worth keeping: composing with an invertible map preserves
the kernel exactly (`ker S = {0} ⟹ ker(S∘T) = ker T`), and two singular maps can
lose more dimensions than either alone.

</details>

**Q6. Why is `Wᵀ` the backpropagation rule through a layer `y = Wx`, and what does
it say about compositions?**

<details>
<summary>Model answer</summary>

The chain rule for a composition is `(f ∘ T)' = f' ∘ T`, and for a linear map
`T(x) = Wx` the derivative of `T` is `T` itself. So with `y = Wx` and incoming
gradient `∂L/∂y`,

    ∂L/∂x = Wᵀ (∂L/∂y)

The transpose appears because the gradient is a row vector and the partial
derivatives with respect to the inputs pair with the **columns** of `W`, whereas a
row vector contracting a matrix contracts along rows. In components,
`∂L/∂x_j = Σ_i g_i w_ij`. This is
[lesson 31](31_matrices_and_matrix_algebra.md)'s `(AB)ᵀ = BᵀAᵀ` doing real work.

The general rule is why the chain rule and backpropagation are the same thing: a
composition of maps has a derivative that is a composition of derivatives, and
reversing a chain of layers reverses the order — which is exactly where the
transposes come from. For `y = W₂W₁x` the gradient flows back as `W₁ᵀW₂ᵀ g`,
because `(W₂W₁)ᵀ = W₁ᵀW₂ᵀ`.

</details>

### Long Answer

**Q1. Why is `ker(S ∘ T)` a preimage rather than a sum, and what would break if
you believed it was a sum?**

<details>
<summary>Model answer</summary>

**The correct statement.** An input `x` is killed by the composition when
`(S ∘ T)(x) = S(T(x)) = 0`, which is exactly `T(x) ∈ ker(S)`. So

    ker(S ∘ T) = T⁻¹(ker S) = {x ∈ V : T(x) ∈ ker S}

and `ker T ⊆ ker(S ∘ T)` automatically, since `T` maps `ker T` to `0` and
`0 ∈ ker S` for any `S`.

**Why a sum is the wrong shape.** First, `ker S ⊆ W` and `ker T ⊆ V`, so
`ker S + ker T` is not well typed unless the spaces coincide. Second, the
underlying picture is wrong: `S` and `T` do not both act on the input. `T` acts
first and `S` acts on `T`'s output, so an input can be completely unmolested by
`T` and still be killed by the composition because `T` steered it into `ker S`.
Nothing about that input lies in `ker T`.

**A concrete counterexample where the two rules name different subspaces.** Take
`T(x, y) = (x, x)`, so `T` is injective and `ker T = {0}`; and take
`S(u, v) = (0, v)`, so `ker S = span{(1, 0)}`. Then

    ker(S ∘ T) = T⁻¹(span{(1,0)}) = span{(1, 1)}

using injectivity of `T`, and indeed `S(T(1,1)) = S(1,1) = (0,1) ≠ 0` while
`S(T(1,0)) = S(1,1)`... check directly: `T(1,1) = (1,1)` and `S(1,1) = (0,1)`, so
`(1,1)` is not in the kernel; and `T(1,0) = (1,1)` too, so find `x` with `T(x) ∈
span{(1,0)}`: `T(x) = (x₁, x₁)` is in that span iff `x₁ = 0`, giving
`ker(S∘T) = {0 : y} = span{(0,1)}`. Recomputing: `T(0,1) = (0,0)`, and
`S(0,0) = (0,0)`, so `(0,1)` is in the kernel, and the sum rule would predict
`ker S + ker T = span{(1,0)}`, a *different* one-dimensional space. That is the
point: the two rules can agree in dimension and still name different subspaces, so
no dimension check catches the error.

**What breaks if you believe the sum.**

*Dimension accounting goes wrong in the direction that matters.* If you computed
`dim ker(S∘T)` as `dim ker S + dim ker T`, you would overcount when both maps are
singular and undercount for a deep stack of small kernels. With `L` layers each of
width `w` and rank `w − 1`, the true kernel can reach `L` dimensions, while a naive
sum can exceed the input dimension entirely — which is impossible, and would be a
visible symptom if anyone checked.

*You would misdiagnose injectivity.* "The composition is not injective" is true
when `T` is not injective, and also when `T` is injective but its image meets
`ker S`. A sum-based test cannot distinguish those, so you would add regularisers
or shrink width in a case where nothing was wrong with `T`.

*You would misread what a network layer does.* The practical confusion is between
"this layer discards information" and "this layer rotates data into a region a
later layer ignores". The second is a conditioning issue; the first is a genuine
identifiability problem. Mistake 3 is exactly this, and the fix is to remember
the preimage form.

**The one-dimensional case worth memorising.** For matrices,
`ker(SA) = {x : Ax ∈ ker S}`. If `S` is invertible then `ker S = {0}` and
`ker(SA) = ker A` exactly. This is the sanity check the lesson's worked example
reaches after several wrong turns: it composed with a coordinate swap, which is
invertible, correctly concluded the kernel could not have changed, and that
immediately flagged the original claim as false.

</details>

**Q2. Why does the decomposition `x = x_im + x_ker` need an adapted basis, and
what goes wrong if you use the row space of the RREF instead?**

<details>
<summary>Model answer</summary>

**What the decomposition is.** Every `x ∈ V` splits *uniquely* as
`x = x_im + x_ker`, with `x_ker ∈ ker(T)` and `x_im` in a complement of the kernel
— the part on which `T` is injective, so `T x_im` captures everything `T` can see.
Uniqueness: a kernel vector plus a complement vector sums to zero only if both
are. This is what makes rank-nullity a genuine partition rather than a numerical
coincidence.

**How to construct it.** Take a basis `b₁, …, b_k` of `ker(T)` and extend it to a
basis `b₁, …, b_n` of `V`. The first `k` vectors are the kernel part; the
remaining `n − k` span the complement. Writing `x = Σ α_i b_i`, we get
`x_ker = Σ_{i≤k} α_i b_i` and `x_im = Σ_{i>k} α_i b_i`. This is the construction in
the first-isomorphism proof, and it is the only one guaranteed correct for the map
you actually have.

**Why the row space fails.** The row space of `A` is a subspace of `ℝ^n` for any
`m × n` matrix, so it *looks* like a candidate complement — which is why the error
is common. It is the wrong subspace for three reasons.

- It indexes the wrong axis. For an `m × n` matrix the row space is a subspace of
  `ℝ^n` and the image is a subspace of `ℝ^m`. The decomposition is about the
  **domain**, and when `m ≠ n` these are unrelated objects.
- Even when `A` is square, the RREF's rows are not the complement. They have the
  form `(1, 0, …, r_i)` and similar — reduced representatives of the row space,
  with nothing guaranteeing `A x_im = A x`.
- **Dimensions cannot catch it.** The row space has dimension `r` and the required
  complement also has dimension `r = n − dim ker`, so every dimension check passes
  while the vectors are wrong. The lesson's worked example has `A x_im` come out as
  `(3.5, 13.25, 16.25)` against `A x = (1, 3, 4)`: the decomposition failed its
  only real test.

**What actually goes wrong.** The `x_im` you produce is a vector whose image lies
somewhere else in the codomain entirely, so every downstream use is wrong in a way
no arithmetic reveals: a least-squares fit built on it fits the wrong thing, a
projection onto it projects the wrong way, and an interpretation of "the part of
`x` the model uses" is simply false. Mistake 2 notes that the dimensions still
come out right, and that is the trap.

**The habit that prevents it.** Work in the domain. Take a kernel basis, extend
it, read off the coefficients. The lesson's worked example does this in the end
with the adapted basis `{(-1,-2,1), (1,0,0), (0,0,1)}` and finds that for
`x = (1,0,0)` the kernel part is zero — correct, because `(1,0,0)` is already the
preimage of the column `(1,3,4)`, and the general family is
`(1,0,0) + t(-1,-2,1)`.

**The general form.** `V/ker(T) ≅ im(T)`: the only thing distinguishing two inputs
is their difference *modulo* the kernel. The decomposition is a concrete
representative of that quotient, unique once a complement is fixed.

</details>

**Q3. A rank-deficient model has a nontrivial kernel. What does that mean for
interpretation, for prediction, and for what a library returns?**

<details>
<summary>Model answer</summary>

**Interpretation: some coefficients do not exist.** The kernel is a set of
directions in coefficient space along which fitted values do not change. If
`v ∈ ker(A)` and `c` is any coefficient vector, then `c` and `c + t v` give
identical predictions on every input. So individual coefficients are not
determined by the data — only `r` independent combinations of them are. The
lesson's example is sharp: the null vector `[-10, -20, 1]` says you can raise the
hours coefficient by 10, lower attendance by 20, raise score by 1, and every
prediction is identical. A design matrix of rank 2 in 3 columns has one such
direction, and the fitted "coefficient on score" is a number the data never
chose. This is why `statsmodels` prints `inf` or enormous standard errors for such
coefficients: reporting one as if it were meaningful is worse than reporting
nothing.

**Prediction: unaffected, and that is the saving grace.** Every point on the line
predicts identically, so any of them is as good as any other *for fitting*. The
code confirms `A(x_p + t v) = b` for `t ∈ {-2, 0, 1, 3}`. What is lost is not
accuracy but transferability to inputs violating the relation, and stability under
small perturbations — the conditioning story from
[lesson 32](32_linear_systems_gaussian_elimination.md).

**What a library returns: a choice, not a fact.** `np.linalg.lstsq` minimises
`‖Ax − b‖`, and on a line of minimisers it returns the minimum-norm point, the
perpendicular foot: with `x(t) = x_p + t v`, the objective is
`‖x_p‖² + 2t(x_p·v) + t²‖v‖²`, minimised at `t* = -(x_p·v)/‖v‖²`, generally not
`0`. Every point on the line is an equally good solution; the returned one is the
closest to the origin. Mistake 5 is treating it as "the" answer.

The practical consequences:

- **Reproducibility.** Different column order, BLAS, or LAPACK version can return
  different points on the same line. Predictions agree to rounding; coefficients
  need not agree at all. Caching a coefficient vector and re-fitting later can move
  the numbers with no other change.
- **Regularisation turns a choice into a decision.** Adding `λ‖c‖²` makes the
  objective strictly convex, so the minimiser is unique and *defined*
  ([lesson 100](../part08_optimization/100_convexity.md)). But note what that buys:
  uniqueness, not correctness. The L2 answer is the closest point to the origin
  among the minimisers; the penalty picks a point, it does not make that point
  mean anything.
- **Dropping a column is the interpretable fix.** Keep a basis. Then the
  coefficients are unique *and* attached to named columns, so "the coefficient on
  hours" is a real number. This is why feature selection beats regularisation when
  the goal is interpretation.
- **Check `cond` and the singular values.** A small singular value means the kernel
  direction is nearly present rather than exactly present, and the fitted
  coefficients are correspondingly unstable. Mistake 4: report singular values and
  a threshold, not a bare rank.

**The warning.** Never compare coefficients across two models with different column
sets and interpret the difference. If one model dropped a near-duplicate column and
the other did not, the coefficient vectors live in different spaces and the
difference is meaningless. A coefficient moving within the kernel direction is not
a finding.

</details>

**Q4. Why is the transpose the right object in backpropagation, and what would
break if you propagated with `W` instead?**

<details>
<summary>Model answer</summary>

**Where the transpose comes from.** The chain rule for a composition is
`(f ∘ T)' = f' ∘ T`. For a linear layer `T(x) = Wx`, the derivative of `T` is `T`
itself, so with `y = Wx` and incoming row gradient `g = ∂L/∂y`,

    ∂L/∂x = Wᵀ g

The transpose is forced by how the contraction lines up. Write `g = (g₁, …, g_m)`
and `W` as `m × n` with rows `w_i`. Then `∂L/∂x_j = Σ_i g_i w_ij` — the gradient
component is a sum over the **rows** of `W` weighted by `g`, and as a matrix-vector
product that is `Wᵀ g`. This is
[lesson 31](31_matrices_and_matrix_algebra.md)'s `(AB)ᵀ = BᵀAᵀ` in a gradient
computation.

**Why substituting `W` is wrong.** Take `W = [[1,2,3],[4,5,6]]` (2 × 3) and
`g = (g₁, g₂)`. The correct gradient is
`(g₁ + 4g₂, 2g₁ + 5g₂, 3g₁ + 6g₂)`. Multiplying by `W` instead would need `Wg`,
which is undefined — `W` is `m × n` and `g` is length `m` — unless `m = n`. For a
square layer `Wg` *is* defined and still wrong: the coordinates pick up the wrong
entries, the shape matches, and nothing complains.

**What would break, in increasing order of subtlety.**

1. *It crashes immediately* on any non-square layer, which is most of them in a
   real network. A shape assertion catches this in development.
2. *It trains the wrong thing silently* on a square layer: right shape, wrong
   entries, optimisation still converges — to a worse model, with no error
   anywhere. This is the failure no assertion catches.
3. *It is wrong in the composed case even if every layer is right.* For
   `y = W₂W₁x` the gradient flows back as `W₁ᵀW₂ᵀ g`, the reverse of the forward
   order, because `(W₂W₁)ᵀ = W₁ᵀW₂ᵀ`. Propagating in forward order computes
   `W₂ᵀW₁ᵀ g` — a different matrix, equal only when the layers commute. Deep
   networks are built to be non-commutative precisely so layer order matters, so
   this is systematic, not a rounding error.

**The unifying statement.** The chain rule for derivatives and the
backpropagation rule are the same mathematics, and the transposes are what reverse
the order. Kernels and images compose, and the chain rule follows the same
pattern. If you remember one thing: *composing functions means composing
derivatives, and reversing a chain reverses the order* — which is exactly
`(AB)ᵀ = BᵀAᵀ`.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — is each map linear?** Check each of these maps for linearity
on the sample vectors `[1,2]`, `[3,−1]`, `[−2,0.5]`, `[0.5,0.5]`:

1. `T₁(x, y) = (x + y, y)`
2. `T₂(x, y) = (x, 2y)`
3. `T₃(x, y) = (y, x)`
4. `T₄(x, y) = (x, y)`
5. `T₅(x, y) = (−y, x)`
6. `T₆(x, y) = (x + 1, y)`
7. `T₇(x, y) = (x², y)`

For 6 and 7, which cannot be written as a matrix, check the conditions by hand
and say which one fails.

<details>
<summary>Solution</summary>

```python
TOL = 1e-9


def shape(M):
    return len(M), len(M[0])


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(A[0])))
             for j in range(len(B[0]))] for i in range(len(A))]


def matvec(M, v):
    return [sum(M[i][k] * v[k] for k in range(len(M[0]))) for i in range(len(M))]


def vadd(u, v):
    return [a + b for a, b in zip(u, v)]


def vsub(u, v):
    return [a - b for a, b in zip(u, v)]


def vscale(c, u):
    return [c * a for a in u]


def is_linear_on_samples(T, samples, tol=TOL):
    """Check T(0)=0, T(cu)=cT(u), T(u+v)=T(u)+T(v) on the given samples."""
    zero = matvec(T, [0.0] * len(samples[0]))
    ok_zero = all(abs(v) <= tol for v in zero)
    ok_scale = True
    ok_add = True
    for u in samples:
        for c in (2.0, -1.0, 0.5):
            lhs = matvec(T, vscale(c, u))
            rhs = vscale(c, matvec(T, u))
            if any(abs(lhs[i] - rhs[i]) > tol for i in range(len(lhs))):
                ok_scale = False
        for w in samples:
            lhs = matvec(T, vadd(u, w))
            rhs = vadd(matvec(T, u), matvec(T, w))
            if any(abs(lhs[i] - rhs[i]) > tol for i in range(len(lhs))):
                ok_add = False
    return ok_zero, ok_scale, ok_add


samples2 = [[1.0, 2.0], [3.0, -1.0], [-2.0, 0.5], [0.5, 0.5]]
maps = [
    ("T1 = (x + y, y), a shear", [[1.0, 1.0], [0.0, 1.0]]),
    ("T2 = (x, 2y), a scale", [[1.0, 0.0], [0.0, 2.0]]),
    ("T3 = (y, x), the swap", [[0.0, 1.0], [1.0, 0.0]]),
    ("T4 = (x, y), the identity", [[1.0, 0.0], [0.0, 1.0]]),
    ("T5 = (-y, x), a 90 degree rotation", [[0.0, -1.0], [1.0, 0.0]]),
]
for label, T in maps:
    z, sc, ad = is_linear_on_samples(T, samples2)
    verdict = "LINEAR" if (z and sc and ad) else "not linear"
    print(f"  {label:34s} T(0)=0: {str(z):5s} scales: {str(sc):5s} "
          f"adds: {str(ad):5s} -> {verdict}")

print()
print("Every one of those passes, because each is a 2x2 matrix. Now two that")
print("cannot be, checked by hand:")


def shift(x):
    """(x, y) -> (x + 1, y). Affine, not linear: it moves the origin."""
    return [x[0] + 1.0, x[1]]


def square_first(x):
    """(x, y) -> (x^2, y). Not linear: squaring is not additive."""
    return [x[0] ** 2, x[1]]


u = [2.0, 3.0]
w = [1.0, 4.0]
for name, f in (("shift (x+1, y)", shift), ("square (x^2, y)", square_first)):
    f0 = f([0.0, 0.0])
    fsum = f(vadd(u, w))
    fadd = vadd(f(u), f(w))
    print(f"  {name}")
    print(f"    f(0)      = {f0}      (a linear map must give [0, 0])")
    print(f"    f(u)      = {f(u)}")
    print(f"    f(w)      = {f(w)}")
    print(f"    f(u + w)  = {fsum}")
    print(f"    f(u)+f(w) = {fadd}   additive: {fsum == fadd}")

print()
print("The shift fails only T(0) = 0, which is the giveaway for every affine")
print("map, and it is why y = Wx + b is not a linear layer. The square fails")
print("additivity, because (u+w)^2 = u^2 + 2uw + w^2 and the cross term does not")
print("appear on the right. Every linear map from R^2 to R^2 is exactly a 2x2")
print("matrix, so a map that is not a matrix cannot be linear.")
```

Output:

```
  T1 = (x + y, y), a shear           T(0)=0: True  scales: True  adds: True  -> LINEAR
  T2 = (x, 2y), a scale              T(0)=0: True  scales: True  adds: True  -> LINEAR
  T3 = (y, x), the swap              T(0)=0: True  scales: True  adds: True  -> LINEAR
  T4 = (x, y), the identity          T(0)=0: True  scales: True  adds: True  -> LINEAR
  T5 = (-y, x), a 90 degree rotation T(0)=0: True  scales: True  adds: True  -> LINEAR

Every one of those passes, because each is a 2x2 matrix. Now two that
cannot be, checked by hand:
  shift (x+1, y)
    f(0)      = [1.0, 0.0]      (a linear map must give [0, 0])
    f(u)      = [3.0, 3.0]
    f(w)      = [2.0, 4.0]
    f(u + w)  = [4.0, 7.0]
    f(u)+f(w) = [5.0, 7.0]   additive: False
  square (x^2, y)
    f(0)      = [0.0, 0.0]      (a linear map must give [0, 0])
    f(u)      = [4.0, 3.0]
    f(w)      = [1.0, 4.0]
    f(u + w)  = [9.0, 7.0]
    f(u)+f(w) = [5.0, 7.0]   additive: False
```

Note `T₆` fails `f(0) = 0` but is otherwise additive on these samples only by
coincidence: `f(u + w) ≠ f(u) + f(w)` as shown, so it fails additivity too. Both
failures come from the constant.

</details>

**[ ] Exercise 2 — kernel, image, and rank-nullity.** For each matrix, report the
rank, a basis for the kernel, a basis for the image, and verify rank-nullity in
both directions:

1. `A = [[1,2],[2,4]]`
2. `B = [[1,2,3],[2,4,6]]`
3. `C = [[1,0],[0,1],[0,0]]`
4. `D = [[1,2],[3,4]]`

Which one is invertible, and what single fact decides it?

<details>
<summary>Solution</summary>

```python
TOL = 1e-9


def shape(M):
    return len(M), len(M[0])


def transpose(M):
    rows, cols = shape(M)
    return [[M[i][j] for i in range(rows)] for j in range(cols)]


def matvec(M, v):
    return [sum(M[i][k] * v[k] for k in range(len(M[0]))) for i in range(len(M))]


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


def image_basis(A, tol=TOL):
    _, pivots = rref(A, tol)
    return [[A[i][c] for i in range(len(A))] for c in pivots]


for label, M in [
    ("A = [[1,2],[2,4]]", [[1.0, 2.0], [2.0, 4.0]]),
    ("B = [[1,2,3],[2,4,6]]", [[1.0, 2.0, 3.0], [2.0, 4.0, 6.0]]),
    ("C = [[1,0],[0,1],[0,0]]", [[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]),
    ("D = [[1,2],[3,4]]", [[1.0, 2.0], [3.0, 4.0]]),
]:
    r = rank(M)
    ker = null_space(M)
    im = image_basis(M)
    n = shape(M)[1]
    left_dim = len(null_space(transpose(M)))
    print(f"--- {label}  ({shape(M)[0]}x{n}) ---")
    print(f"  rank {r}, dim(ker) {len(ker)}, dim(im) {len(im)}")
    print(f"  rank + nullity = {r} + {len(ker)} = {r + len(ker)}, and n = {n}, "
          f"equal: {r + len(ker) == n}")
    print(f"  rank + left nullity = {r} + {left_dim} = {r + left_dim}, "
          f"and rows = {shape(M)[0]}, equal: {r + left_dim == shape(M)[0]}")
    if ker:
        print("  kernel basis (each vector maps to zero):")
        for v in ker:
            print(f"    v = {[round(t, 4) for t in v]}, M v = "
                  f"{[round(t, 9) for t in matvec(M, v)]}")
    else:
        print("  kernel basis is empty: the kernel is {0}")
    print("  image basis (pivot columns, which are outputs):")
    for v in im:
        print(f"    {[round(t, 4) for t in v]}")
    print()

print("D is the only invertible one: trivial kernel, so it is onto and one-to-one.")
print("A and B have kernels, so each collapses whole lines to points, and the")
print("system A x = b has many solutions or none. C has a zero row, so it loses")
print("a dimension on output: rank 2, so the image is 2-dimensional inside R^3.")
```

Output:

```
--- A = [[1,2],[2,4]]  (2x2) ---
  rank 1, dim(ker) 1, dim(im) 1
  rank + nullity = 1 + 1 = 2, and n = 2, equal: True
  rank + left nullity = 1 + 1 = 2, and rows = 2, equal: True
  kernel basis (each vector maps to zero):
    v = [-2.0, 1.0], M v = [0.0, 0.0]
  image basis (pivot columns, which are outputs):
    [1.0, 2.0]

--- B = [[1,2,3],[2,4,6]]  (2x3) ---
  rank 1, dim(ker) 2, dim(im) 1
  rank + nullity = 1 + 2 = 3, and n = 3, equal: True
  rank + left nullity = 1 + 1 = 2, and rows = 2, equal: True
  kernel basis (each vector maps to zero):
    v = [-2.0, 1.0, 0.0], M v = [0.0, 0.0]
    v = [-3.0, 0.0, 1.0], M v = [0.0, 0.0]
  image basis (pivot columns, which are outputs):
    [1.0, 2.0]

--- C = [[1,0],[0,1],[0,0]]  (3x2) ---
  rank 2, dim(ker) 0, dim(im) 2
  rank + nullity = 2 + 0 = 2, and n = 2, equal: True
  rank + left nullity = 2 + 1 = 3, and rows = 3, equal: True
  kernel basis is empty: the kernel is {0}
  image basis (pivot columns, which are outputs):
    [1.0, 0.0, 0.0]
    [0.0, 1.0, 0.0]

--- D = [[1,2],[3,4]]  (2x2) ---
  rank 2, dim(ker) 0, dim(im) 2
  rank + nullity = 2 + 0 = 2, and n = 2, equal: True
  rank + left nullity = 2 + 0 = 2, and rows = 2, equal: True
  kernel basis is empty: the kernel is {0}
  image basis (pivot columns, which are outputs):
    [1.0, 3.0]
    [2.0, 4.0]
```

The single deciding fact: **`D` is the only one with a trivial kernel**. By the
theorem in the formal section, trivial kernel is equivalent to invertibility for
a square map. Notice `C` is *not* square and has a trivial kernel too, so it is
injective but not surjective — its image is a plane inside `ℝ³`, and some right-hand
sides have no solution at all.

</details>

**[ ] Exercise 3 — the four spaces.** For
`M = [[1,2,3,4],[5,6,7,9],[2,3,4,5]]`, compute the rank, all four subspaces with
their dimensions and explicit bases, and check both rank-nullity identities.

**Challenge.** The chain rule is composition. Let `f(t) = t²` and
`T = [[1,2],[0,1]]`. Show that the gradient of `g(v) = f((Tv)₀)` is
`f'((Tv)₀) · row 0 of T`, and verify against finite differences. Then explain
where the transpose comes from.

**Challenge (b).** A projection `(x, y, z) → (x, y)` has a one-dimensional
kernel. Explain why that is fatal for a renderer, and what a graphics pipeline
does instead.

<details>
<summary>Solution</summary>

```python
TOL = 1e-9


def shape(M):
    return len(M), len(M[0])


def transpose(M):
    rows, cols = shape(M)
    return [[M[i][j] for i in range(rows)] for j in range(cols)]


def matvec(M, v):
    return [sum(M[i][k] * v[k] for k in range(len(M[0]))) for i in range(len(M))]


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


def image_basis(A, tol=TOL):
    _, pivots = rref(A, tol)
    return [[A[i][c] for i in range(len(A))] for c in pivots]


def vadd(u, v):
    return [a + b for a, b in zip(u, v)]


def vsub(u, v):
    return [a - b for a, b in zip(u, v)]


def print_matrix(label, M, width=7):
    rows, cols = shape(M)
    print(f"{label}  ({rows}x{cols})")
    for row in M:
        print("  | " + " ".join(f"{x:{width}.3f}" for x in row) + " |")


M = [[1.0, 2.0, 3.0, 4.0],
     [5.0, 6.0, 7.0, 9.0],
     [2.0, 3.0, 4.0, 5.0]]
m, n = shape(M)
r = rank(M)
Mrr, piv = rref(M)
row_b = [row for row in Mrr if any(abs(t) > TOL for t in row)]
col_b = image_basis(M)
ker_b = null_space(M)
lker_b = null_space(transpose(M))
print_matrix("M (3x4)", M)
print(f"rank r = {r}, so {m} rows and {n} columns")
print(f"  column space   in R^{m}, dimension {len(col_b)}, basis = pivot columns {piv}")
print(f"  row space      in R^{n}, dimension {len(row_b)}, basis = nonzero RREF rows")
print(f"  kernel         in R^{n}, dimension {len(ker_b)} = n - r = {n} - {r}")
print(f"  left kernel    in R^{m}, dimension {len(lker_b)} = m - r = {m} - {r}")
print()
print(f"  r + (n - r) = {r + n - r} = n  (rank-nullity)")
print(f"  r + (m - r) = {r + m - r} = m  (the same, applied to M^T)")
print()
print("Bases, explicitly:")
print("  column space basis:")
for v in col_b:
    print(f"    {v}")
print("  row space basis:")
for v in row_b:
    print(f"    {v}")
print("  kernel basis (each vector vanishes):")
for v in ker_b:
    print(f"    {v}   M v = {[round(t, 9) for t in matvec(M, v)]}")
if lker_b:
    print("  left kernel basis (each vector gives a row relation):")
    for v in lker_b:
        weighted = [sum(v[i] * M[i][j] for i in range(m)) for j in range(n)]
        print(f"    {v}   weighted row sum = {weighted}")
else:
    print("  left kernel basis is empty: the rows are independent, so there are")
    print("  no relations among them and dim(ker(M^T)) = m - r = 0.")
print()
print("Two numbers, one row reduction, four spaces. The row space basis comes from")
print("the REDUCED matrix and the column space basis from the ORIGINAL one;")
print("mixing those up is the standard error, and it does not change any")
print("dimension, only which vectors you report.")

print()
print("=== Challenge: the chain rule as composition ===")
print("Let f(t) = t^2 and T = [[1,2],[0,1]]. The map g(v) = f((T v)_0) has gradient")
print("f'((T v)_0) * (row 0 of T). Verify against finite differences.")


def f(t):
    return t * t


def f_prime(t):
    return 2.0 * t


T = [[1.0, 2.0], [0.0, 1.0]]
v = [2.0, 5.0]
Tv = matvec(T, v)
print(f"  T v        = {Tv}")
print(f"  g(v)       = f({Tv[0]:.1f}) = {f(Tv[0])}")
grad = [f_prime(Tv[0]) * T[0][j] for j in range(2)]
print(f"  gradient   = f'({Tv[0]:.1f}) * {T[0]} = {grad}")

eps = 1e-7
for j in range(2):
    e = [0.0, 0.0]
    e[j] = eps
    fd = (f(matvec(T, vadd(v, e))[0]) - f(matvec(T, vsub(v, e))[0])) / (2 * eps)
    print(f"  finite difference in v[{j}]: {fd:.6f}   analytic: {grad[j]:.6f}")
print("They agree. The chain rule for a composition with a linear map is: take")
print("the derivative of the outer function, then multiply by the matrix. That is")
print("why backpropagation passes gradients through layers as matrix-vector")
print("products, and why the transpose shows up: the derivative of f at w")
print("multiplying T is the row vector f'(w) T, which is (T^T f'(w)^T)^T.")

print()
print("=== Challenge: what a projection kernel means for graphics ===")
proj = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
print_matrix("projection (x, y, z) -> (x, y)", proj)
ker = null_space(proj)
print(f"  rank {rank(proj)}, dim(ker) = {shape(proj)[1]} - {rank(proj)} = "
      f"{shape(proj)[1] - rank(proj)}")
print(f"  kernel basis: {[[round(t, 6) for t in k] for k in ker]}")
p1 = [1.0, 2.0, 5.0]
p2 = [1.0, 2.0, 900.0]
print(f"  point A = {p1} -> {matvec(proj, p1)}")
print(f"  point B = {p2} -> {matvec(proj, p2)}")
print(f"  same 2-D point, from points {abs(p2[2] - p1[2]):.0f} units apart in z")
print(f"  B - A = {[p2[i] - p1[i] for i in range(3)]}")
print()
print("Any two points differing by a kernel vector project to the same place.")
print("This is exactly what must not happen in a renderer, and it is why the")
print("pipeline keeps a homogeneous coordinate: the map to screen space must")
print("have a trivial kernel, or distinct geometry becomes indistinguishable.")
```

Output:

```
M (3x4)
  |    1.000    2.000    3.000    4.000 |
  |    5.000    6.000    7.000    9.000 |
  |    2.000    3.000    4.000    5.000 |
rank r = 3, so 3 rows and 4 columns
  column space   in R^3, dimension 3, basis = pivot columns [0, 1, 3]
  row space      in R^4, dimension 3, basis = nonzero RREF rows
  kernel         in R^4, dimension 1 = n - r = 4 - 3
  left kernel    in R^3, dimension 0 = m - r = 3 - 3

  r + (n - r) = 4 = n  (rank-nullity)
  r + (m - r) = 3 = m  (the same, applied to M^T)

Bases, explicitly:
  column space basis:
    [1.0, 5.0, 2.0]
    [2.0, 6.0, 3.0]
    [4.0, 9.0, 5.0]
  row space basis:
    [1.0, 0.0, -1.0, 0.0]
    [0.0, 1.0, 2.0, 0.0]
    [0.0, 0.0, 0.0, 1.0]
  kernel basis (each vector vanishes):
    [1.0, -2.0, 1.0, -0.0]   M v = [0.0, 0.0, 0.0]
  left kernel basis is empty: the rows are independent, so there are
  no relations among them and dim(ker(M^T)) = m - r = 0.

=== Challenge: the chain rule as composition ===
  T v        = [12.0, 5.0]
  g(v)       = f(12.0) = 144.0
  gradient   = f'(12.0) * [1.0, 2.0] = [24.0, 48.0]
  finite difference in v[0]: 24.000000   analytic: 24.000000
  finite difference in v[1]: 48.000000   analytic: 48.000000
```

The transpose appears because the derivative of `g` with respect to `v` is the
row vector `f'((Tv)₀) · T₀`, and writing that as a column vector requires
transposing: `(f'(Tv)₀ · T₀)ᵀ = T₀ᵀ f'(Tv)₀`. So the gradient flows backwards
through a layer as `Wᵀ`, which is exactly lesson 31's rule that the transpose of
a product reverses the order.

</details>

**[ ] Exercise 4 — kernel, image, and the decomposition, checked.** Take

    A = | 1  2  3 |
        | 2  4  6 |        (a 2x3 map R^3 -> R^2; row 1 = 2 * row 0)

1. Verify `A` is a linear map by checking `T(u+v) = T(u)+T(v)` and `T(cu) = cT(u)`
   for `u = (1, 0, 2)`, `v = (3, -1, 4)`, `c = -2`.
2. Report `rank(A)`, a basis for `im(A)`, a basis for `ker(A)`, and the
   dimensions of both. Check rank-nullity against `dim(R^3) = 3`.
3. Show `im(A)` is a **line** in `R^2` and not something else: express all three
   columns as multiples of one vector, and confirm that vector is an output.
4. Extend a basis of `ker(A)` to a basis of `R^3`, then decompose
   `x = (1, 0, 2)` into `x_im + x_ker` and verify `A x_ker = 0` and
   `A x_im = A x`.
5. Explain in one sentence why taking `x_im` from the row space of the RREF would
   give a different, wrong answer, and demonstrate it.

**Challenge.** (a) For `T(x, y) = (x, x)` and `S(u, v) = (0, v)`, both maps
`R^2 → R^2`, compute `ker(T)`, `ker(S)`, and `ker(S ∘ T)` explicitly. (b) Show
that `ker(S ∘ T) ≠ ker(S) + ker(T)`, and that the two rules can name subspaces of
the same dimension while still disagreeing — so no count separates them. (c) Find
a second pair of maps where the sum rule happens to give the *right set*, and
explain in one paragraph why a preimage is the right form and a sum is not.
(d) For the `2 × 3` matrix `A` of part 2, verify by computation that every
`x = x_p + t v` solves `A x = b` for `b = (6, 12)`, then compute the minimum-norm
one via `t* = -(x_p·v)/‖v‖²` and confirm `(x_p + t* v) · v = 0`. Note whether
`t*` is zero.

<details>
<summary>Solution</summary>

**Part 1.** `u + v = (4, -1, 6)` and `c u = (-2, 0, -4)`. Then

    T(u)      = (1 + 0 + 6,  2 + 0 + 12)    = (7, 14)
    T(v)      = (3 - 2 + 12,  6 - 4 + 24)   = (13, 26)
    T(u+v)    = (4 - 2 + 18,  8 - 4 + 36)   = (20, 40)
    T(u)+T(v) = (7 + 13,  14 + 26)          = (20, 40)     ✓
    T(cu)     = (-2 + 0 - 12,  -4 + 0 - 24) = (-14, -28)
    c T(u)    = -2(7, 14)                   = (-14, -28)  ✓

Both axioms hold, as they must: `A` is a matrix, and matrix multiplication is
linear by distributivity. Worth saying plainly — **a linear map can never fail one
of these tests**, so a failure is always an arithmetic slip in the test, never a
discovery about the map. (Writing `4 - 3 + 18` instead of `4 - 2 + 18` is the
classic way to manufacture a spurious failure.)

**Part 2.** Row 1 is twice row 0, so `rank(A) = 1`. The image is the span of the
columns, which are `(1,2)ᵀ`, `(2,4)ᵀ`, `(3,6)ᵀ` — all multiples of `(1,2)ᵀ` — so
`im(A)` has dimension 1 with basis `{(1,2)ᵀ}`. Rank-nullity gives
`dim ker(A) = n − r = 3 − 1 = 2`, and the code's basis is `[-2, 1, 0]` and
`[-3, 0, 1]`. Verified: `A(-2,1,0) = (-2+2, -4+4) = 0` and `A(-3,0,1) = (-3+3, -6+6)
= 0`. Rank-nullity: `1 + 2 = 3 = dim ℝ³` ✓.

**Part 3.** `(1,2)ᵀ`, `(2,4)ᵀ = 2(1,2)ᵀ`, `(3,6)ᵀ = 3(1,2)ᵀ`. So
`im(A) = {t(1,2)ᵀ : t ∈ ℝ}`, a **line**. And `(1,2)ᵀ` is genuinely an output because
it is column 0, i.e. `A e₀`. Equivalently: the second coordinate of every output
is twice the first, and that single constraint is what "one-dimensional" means.

**Part 4.** Kernel basis `{-2,1,0}, {-3,0,1}`; extend by `e₀ = (1,0,0)`. They are
independent: both kernel vectors have third component 0 while `e₀` has 1, so `e₀`
is not in their span, and the two are independent by construction. Write

    x = a(-2, 1, 0) + b(-3, 0, 1) + c(1, 0, 0)  =  (1, 0, 2)

Third component: `b = 2`. Second: `a = 0`. First: `-3b + c = 1`, so `c = 7`. Hence

    x_ker = 2·(-3, 0, 1) = (-6, 0, 2)     x_im = 7·(1, 0, 0) = (7, 0, 0)

Verify: `x_ker + x_im = (1, 0, 2)` ✓, `A x_ker = (-6+6, -12+12) = (0,0)` ✓, and
`A x_im = A(7,0,0) = (7, 14) = A x` ✓.

**Part 5.** The row space of `A` is spanned by `(1, 2, 3)`, so an `x_im` read from
it comes from writing `x = c(1,2,3) + x_ker`. The code solves that and gets
`c = 1/6`, `x_im = (1/6, 1/3, 1/2)` and `x_ker = (5/6, -1/3, 3/2)`. Now
`A x_ker = 0` ✓ and `x_im + x_ker = x` ✓, so the decomposition *looks* perfect —
but

    A x_im = (1/6 + 2/3 + 3/2,  1/3 + 4/3 + 3) = (7/3, 14/3)   ≠   A x = (7, 14)

so `x_im` is not the component `T` can see. One sentence for the reason: the row
space describes the *equations*, not a complement of the kernel, and both have
dimension `r`, so no count distinguishes them — the only reliable test is
`A x_im = A x`. That is Mistake 2.

```python
TOL = 1e-9


# ---------------------------------------------------------------- helpers
def shape(M):
    return len(M), len(M[0])


def matvec(M, v):
    rows, cols = shape(M)
    return [sum(M[i][k] * v[k] for k in range(cols)) for i in range(rows)]


def vadd(u, v):
    return [a + b for a, b in zip(u, v)]


def vscale(c, u):
    return [c * a for a in u]


def rref(A, tol=TOL):
    M = [list(row) for row in A]
    rows, cols = len(M), len(M[0])
    pivot_row, pivots = 0, []
    for col in range(cols):
        if pivot_row == rows:
            break
        best = max(range(pivot_row, rows), key=lambda r: abs(M[r][col]))
        if abs(M[best][col]) <= tol:
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
    return len(rref(A, tol)[1])


def null_space(A, tol=TOL):
    M, pivots = rref(A, tol)
    cols = shape(A)[1]
    basis = []
    for fc in [c for c in range(cols) if c not in pivots]:
        v = [0.0] * cols
        v[fc] = 1.0
        for i, pc in enumerate(pivots):
            v[pc] = -M[i][fc]
        basis.append(v)
    return basis


def image_basis(A, tol=TOL):
    _, pivots = rref(A, tol)
    return [[A[i][c] for i in range(len(A))] for c in pivots]


def solve_for_coeffs(basis, target, tol=1e-9):
    """Solve target = sum(c_i basis_i) by Gauss-Jordan on the small system."""
    n = len(target)
    M = [[basis[j][i] for j in range(len(basis))] + [target[i]] for i in range(n)]
    pivot_row = 0
    for col in range(len(basis)):
        best = max(range(pivot_row, n), key=lambda r: abs(M[r][col]))
        if abs(M[best][col]) <= tol:
            continue
        M[pivot_row], M[best] = M[best], M[pivot_row]
        p = M[pivot_row][col]
        M[pivot_row] = [w / p for w in M[pivot_row]]
        for r in range(n):
            if r != pivot_row and M[r][col] != 0.0:
                f = M[r][col]
                M[r] = [M[r][c] - f * M[pivot_row][c] for c in range(n + 1)]
        pivot_row += 1
    return [M[i][n] for i in range(n)]


def print_matrix(label, M, width=7):
    rows, cols = shape(M)
    print(f"{label}  ({rows}x{cols})")
    for row in M:
        print("  | " + " ".join(f"{x:{width}.3f}" for x in row) + " |")


def print_vector(label, v, width=7):
    print(f"{label} = [" + ", ".join(f"{x:{width}.3f}" for x in v) + "]")


# ---------------------------------------------------------------- 1
print("=== Part 1: is A a linear map? ===")
A = [[1.0, 2.0, 3.0],
     [2.0, 4.0, 6.0]]
print_matrix("A (2x3, map R^3 -> R^2)", A)
u = [1.0, 0.0, 2.0]
v = [3.0, -1.0, 4.0]
c = -2.0
print(f"u = {u}, v = {v}, c = {c}")
print(f"  T(u)      = {matvec(A, u)}")
print(f"  T(v)      = {matvec(A, v)}")
print(f"  T(u+v)    = {matvec(A, vadd(u, v))}")
print(f"  T(u)+T(v) = {vadd(matvec(A, u), matvec(A, v))}   "
      f"equal: {matvec(A, vadd(u, v)) == vadd(matvec(A, u), matvec(A, v))}")
print(f"  T(cu)     = {matvec(A, vscale(c, u))}")
print(f"  c*T(u)    = {vscale(c, matvec(A, u))}   "
      f"equal: {matvec(A, vscale(c, u)) == vscale(c, matvec(A, u))}")
print("Both axioms hold, as they must for a matrix. A failure here is always an")
print("arithmetic slip in the test, never a discovery about the map.")

# ---------------------------------------------------------------- 2
print()
print("=== Part 2: rank, image, kernel, and rank-nullity ===")
r = rank(A)
ib = image_basis(A)
ns = null_space(A)
print(f"rank = {r}  (row 1 is 2 * row 0)")
print(f"image basis ({len(ib)} vector):")
for w in ib:
    print(f"  {w}")
print(f"kernel basis ({len(ns)} vectors):")
for w in ns:
    print(f"  {w}      A w = {matvec(A, w)}")
print(f"dim(im)  = {len(ib)}")
print(f"dim(ker) = {len(ns)} = n - r = {shape(A)[1]} - {r}")
print(f"rank-nullity: {len(ib)} + {len(ns)} = {len(ib) + len(ns)} "
      f"= dim(R^3) = {shape(A)[1]}: {len(ib) + len(ns) == shape(A)[1]}")

# ---------------------------------------------------------------- 3
print()
print("=== Part 3: the image is a LINE, not a plane ===")
print("every column as a multiple of the first:")
for j in range(shape(A)[1]):
    col = [A[i][j] for i in range(len(A))]
    ratio = col[1] / col[0]
    print(f"  col{j} = {col} = {ratio:g} * {ib[0]}  : "
          f"{[ratio * t for t in ib[0]] == col}")
print(f"and {ib[0]} is genuinely an output: it is column 0, i.e. A e_0.")
print("The second coordinate is always twice the first, which is exactly what a")
print("one-dimensional image means.")

# ---------------------------------------------------------------- 4
print()
print("=== Part 4: the decomposition via an adapted basis ===")
e0 = [1.0, 0.0, 0.0]
adapted = ns + [e0]
print(f"kernel basis: {ns}")
print(f"extended by {e0}: {adapted}")
print("  both kernel vectors have third component 0 while e_0 has 1, so e_0 is")
print("  not in their span, and the three are independent.")
x = [1.0, 0.0, 2.0]
coeffs = solve_for_coeffs(adapted, x)
print()
print(f"x = {x} as a combination of the adapted basis:")
for vec, cf in zip(adapted, coeffs):
    print(f"  {cf:9.4f} * {vec} = {[round(cf * t, 6) for t in vec]}")
x_ker = [sum(coeffs[k] * ns[k][i] for k in range(len(ns))) for i in range(3)]
x_im = [coeffs[-1] * e0[i] for i in range(3)]
print()
print_vector("x_ker", x_ker)
print_vector("x_im ", x_im)
print_vector("sum  ", [x_ker[i] + x_im[i] for i in range(3)])
print(f"  A x_ker = {matvec(A, x_ker)}   (must be [0.0, 0.0])")
print(f"  A x_im  = {[round(t, 9) for t in matvec(A, x_im)]}")
print(f"  A x     = {[round(t, 9) for t in matvec(A, x)]}   equal: "
      f"{all(abs(matvec(A, x_im)[i] - matvec(A, x)[i]) < 1e-9 for i in range(2))}")

# ---------------------------------------------------------------- 5
print()
print("=== Part 5: the row space gives a WRONG x_im, and no count catches it ===")
row_dir = [1.0, 2.0, 3.0]
print(f"row space of A is spanned by {row_dir}, dimension {r} -- the SAME as the")
print("complement dimension, so a dimension check passes.")
best = None
for num in range(-40, 41):
    c_try = num / 12.0
    resid = [x[i] - c_try * row_dir[i] for i in range(3)]
    if all(abs(t) <= 1e-9 for t in matvec(A, resid)):
        best = (c_try, resid)
        break
c_row, x_ker_wrong = best
x_im_wrong = [c_row * t for t in row_dir]
print()
print_vector("wrong x_ker", x_ker_wrong)
print_vector("wrong x_im ", x_im_wrong)
print(f"  x_ker + x_im = x : "
      f"{all(abs(x_ker_wrong[i] + x_im_wrong[i] - x[i]) < 1e-9 for i in range(3))}")
print(f"  A x_ker         = {matvec(A, x_ker_wrong)}   (that part is fine)")
print(f"  A x_im          = {[round(t, 6) for t in matvec(A, x_im_wrong)]}")
print(f"  A x             = {[round(t, 6) for t in matvec(A, x)]}")
print(f"  A x_im == A x   : "
      f"{all(abs(matvec(A, x_im_wrong)[i] - matvec(A, x)[i]) < 1e-9 for i in range(2))}")
print("x_im + x_ker = x and A x_ker = 0 both hold, so the decomposition LOOKS")
print("valid. But A x_im != A x, so x_im is not the part T can see. Both")
print("candidates have dimension 1, so nothing countable separates them.")
print("Mistake 2, and the only reliable test is A x_im = A x.")
```

Output:

```
=== Part 1: is A a linear map? ===
A (2x3, map R^3 -> R^2)
  |  1.000   2.000   3.000 |
  |  2.000   4.000   6.000 |
u = [1.0, 0.0, 2.0], v = [3.0, -1.0, 4.0], c = -2.0
  T(u)      = [7.0, 14.0]
  T(v)      = [13.0, 26.0]
  T(u+v)    = [20.0, 40.0]
  T(u)+T(v) = [20.0, 40.0]   equal: True
  T(cu)     = [-14.0, -28.0]
  c*T(u)    = [-14.0, -28.0]   equal: True
Both axioms hold, as they must for a matrix. A failure here is always an
arithmetic slip in the test, never a discovery about the map.

=== Part 2: rank, image, kernel, and rank-nullity ===
rank = 1  (row 1 is 2 * row 0)
image basis (1 vector):
  [1.0, 2.0]
kernel basis (2 vectors):
  [-2.0, 1.0, 0.0]      A w = [0.0, 0.0]
  [-3.0, 0.0, 1.0]      A w = [0.0, 0.0]
dim(im)  = 1
dim(ker) = 2 = n - r = 3 - 1
rank-nullity: 1 + 2 = 3 = dim(R^3) = 3: True

=== Part 3: the image is a LINE, not a plane ===
every column as a multiple of the first:
  col0 = [1.0, 2.0] = 1 * [1.0, 2.0]  : True
  col1 = [2.0, 4.0] = 2 * [1.0, 2.0]  : True
  col2 = [3.0, 6.0] = 3 * [1.0, 2.0]  : True
and [1.0, 2.0] is genuinely an output: it is column 0, i.e. A e_0.
The second coordinate is always twice the first, which is exactly what a
one-dimensional image means.

=== Part 4: the decomposition via an adapted basis ===
kernel basis: [[-2.0, 1.0, 0.0], [-3.0, 0.0, 1.0]]
extended by [1.0, 0.0, 0.0]: [[-2.0, 1.0, 0.0], [-3.0, 0.0, 1.0], [1.0, 0.0, 0.0]]
  both kernel vectors have third component 0 while e_0 has 1, so e_0 is
  not in their span, and the three are independent.

x = [1.0, 0.0, 2.0] as a combination of the adapted basis:
   0.0000 * [-2.0, 1.0, 0.0] = [0.0, 0.0, 0.0]
   2.0000 * [-3.0, 0.0, 1.0] = [-6.0, 0.0, 2.0]
   7.0000 * [1.0, 0.0, 0.0] = [7.0, 0.0, 0.0]
x_ker = [-6.0, 0.0, 2.0]
x_im  = [7.0, 0.0, 0.0]
sum   = [1.0, 0.0, 2.0]
  A x_ker = [0.0, 0.0]   (must be [0.0, 0.0])
  A x_im  = [7.0, 14.0]
  A x     = [7.0, 14.0]   equal: True

=== Part 5: the row space gives a WRONG x_im, and no count catches it ===
row space of A is spanned by [1.0, 2.0, 3.0], dimension 1 -- the SAME as the
complement dimension, so a dimension check passes.
wrong x_ker = [0.833333, -0.333333, 1.5]
wrong x_im  = [0.166667, 0.333333, 0.5]
  x_ker + x_im = x : True
  A x_ker         = [0.0, 0.0]   (that part is fine)
  A x_im          = [2.333333, 4.666667]
  A x             = [7.0, 14.0]
  A x_im == A x   : False
x_im + x_ker = x and A x_ker = 0 both hold, so the decomposition LOOKS
valid. But A x_im != A x, so x_im is not the part T can see. Both
candidates have dimension 1, so nothing countable separates them.
Mistake 2, and the only reliable test is A x_im = A x.
```

**Challenge.** (a) The matrices are `T = [[1,0],[1,0]]` and `S = [[0,0],[0,1]]`.
`ker(T)`: row 0 forces `x = 0`, leaving `y` free, so `ker(T) = span{(0,1)}`.
`ker(S)`: row 1 forces `v = 0`, leaving `u` free, so `ker(S) = span{(1,0)}`. And

    S T = [[0·1+0·1, 0·0+0·0], [0·1+1·1, 0·0+1·0]] = [[0, 0], [1, 0]]

whose kernel is `{(0, y)} = span{(0,1)}`. So `ker(S ∘ T) = ker(T)` — composing
with `S` adds nothing. Direct check: `S(T(0,1)) = S(0,0) = 0` ✓ while
`S(T(1,1)) = S(1,1) = (0,1) ≠ 0` ✓. The reason is exactly the preimage rule: `T`'s
image is `{(a,a)}`, which meets `ker S = {(b,0)}` only at the origin, so
`T⁻¹(ker S) = ker T`.

(b) `ker(S) + ker(T) = span{(1,0)} + span{(0,1)} = ℝ²`, which is
**different** from `ker(S∘T) = span{(0,1)}` — so the rules disagree, and they even
have different dimensions (2 versus 1), so here a count would separate them. The
code's probe test makes it concrete: `(1,0)` lies in the sum but not in the true
kernel. Note which is the right answer: `(1,0)` maps to `T(1,0) = (1,1)`, and
`S(1,1) = (0,1) ≠ 0`, so `(1,0)` is genuinely not killed, and the sum rule
overcounts by including it.

(c) A second pair where the rules agree: take `T₂(x, y) = (x, 0)` and the same
`S`. `ker(T₂) = span{(0,1)}` and `S(T₂(x,y)) = S(x, 0) = (0, 0)` for every input,
so `ker(S ∘ T₂) = ℝ² = ker(S) + ker(T₂)`. The rules agree here and disagree above,
so agreement is luck, not a theorem — and no check on the answer reveals which case
you are in.

The paragraph: a preimage is the right form because the kernel of a composition is
defined on the **output** of the inner map — `x ∈ ker(S∘T)` exactly when
`T(x) ∈ ker(S)` — and the set of all inputs landing in a given set is by
definition a preimage. A sum is wrong twice over. It is the wrong *shape*:
`ker S ⊆ W` and `ker T ⊆ V`, so `ker S + ker T` is not even well typed unless the
spaces coincide. And it is the wrong *reasoning*: `S` never touches the input, so
an input's own properties matter only through where `T` sends it. The containment
that always holds is `ker(S∘T) ⊇ ker T`, because `T` maps `ker T` to `0` and `0 ∈
ker S`; a sum rule can never add the inputs that `T` steers *into* `ker S`, which
is precisely the extra content of a preimage. Mistake 3 is this error, and the fix
is to remember `ker(S∘T) = {x : T(x) ∈ ker S}`.

(d) `b = (6, 12) = 6·(1,2)ᵀ`, and `(1,2)ᵀ` is column 0, so `b` **is** in the image
and the system is consistent. Set the free variable `x₂ = 0`: both equations
collapse to the single equation `x₀ + 2x₁ = 6`, so take `x₁ = 0`, `x₀ = 6`, giving
`x_p = (6, 0, 0)` with `A x_p = b` ✓. With `v = (-2, 1, 0)` and `A v = 0`,
`A(x_p + t v) = A x_p + t A v = b` for **every** `t`, which the code confirms at
`t ∈ {-1, 0, 1, 2.4}`.

Minimum norm: `x_p · v = 6(-2) = -12`, `‖v‖² = 4 + 1 = 5`, so
`t* = -(-12)/5 = 12/5 = 2.4`, giving `x_min = (6, 0, 0) + 2.4(-2, 1, 0) =
(1.2, 2.4, 0)`. Orthogonality: `x_min · v = (1.2)(-2) + (2.4)(1) + 0 = 0` ✓, and
`‖x_min‖² = 1.44 + 5.76 = 7.2 < 36 = ‖x_p‖²`. So `t* = 2.4`, **not** `0`: the
minimum-norm point is a *different* point on the line from the one you get by
zeroing a free variable. That is why `lstsq`'s output is a choice rather than "the"
answer — Mistake 5 — and why regularisation, not the solver, is what makes the
choice deliberate.

```python
TOL = 1e-9


# ---------------------------------------------------------------- helpers
def shape(M):
    return len(M), len(M[0])


def matmul(A, B):
    rows_a, cols_a = shape(A)
    rows_b, cols_b = shape(B)
    if cols_a != rows_b:
        raise ValueError(f"cannot multiply {rows_a}x{cols_a} by {rows_b}x{cols_b}")
    return [[sum(A[i][k] * B[k][j] for k in range(cols_a)) for j in range(cols_b)]
            for i in range(rows_a)]


def matvec(M, v):
    rows, cols = shape(M)
    return [sum(M[i][k] * v[k] for k in range(cols)) for i in range(rows)]


def rref(A, tol=TOL):
    M = [list(row) for row in A]
    rows, cols = len(M), len(M[0])
    pivot_row, pivots = 0, []
    for col in range(cols):
        if pivot_row == rows:
            break
        best = max(range(pivot_row, rows), key=lambda r: abs(M[r][col]))
        if abs(M[best][col]) <= tol:
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
    return M, pivots


def null_space(A, tol=TOL):
    M, pivots = rref(A, tol)
    cols = shape(A)[1]
    basis = []
    for fc in [c for c in range(cols) if c not in pivots]:
        v = [0.0] * cols
        v[fc] = 1.0
        for i, pc in enumerate(pivots):
            v[pc] = -M[i][fc]
        basis.append(v)
    return basis


def print_matrix(label, M, width=7):
    rows, cols = shape(M)
    print(f"{label}  ({rows}x{cols})")
    for row in M:
        print("  | " + " ".join(f"{x:{width}.3f}" for x in row) + " |")


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def in_span_of(probe, vectors, tol=1e-9):
    return any(all(abs(probe[i] - v[i]) <= tol for i in range(len(probe)))
               for v in vectors)


print("=== (a) ker(T), ker(S), ker(S o T) ===")
T = [[1.0, 0.0], [1.0, 0.0]]      # (x, y) -> (x, x)
S = [[0.0, 0.0], [0.0, 1.0]]      # (u, v) -> (0, v)
print_matrix("T", T)
print_matrix("S", S)
ker_T = null_space(T)
ker_S = null_space(S)
ST = matmul(S, T)
print_matrix("S T", ST)
print(f"  ker(T)     = {[[round(t, 6) for t in v] for v in ker_T]}")
print(f"  ker(S)     = {[[round(t, 6) for t in v] for v in ker_S]}")
print(f"  ker(S o T) = {[[round(t, 6) for t in v] for v in null_space(ST)]}"
      f"   dimension {len(null_space(ST))}")
print(f"  check S(T(0,1)) = {matvec(S, matvec(T, [0.0, 1.0]))}   (zero)")
print(f"  check S(T(1,1)) = {matvec(S, matvec(T, [1.0, 1.0]))}   (nonzero)")
print("  T's image is {(a,a)}, which meets ker(S) = {(b,0)} only at 0, so")
print("  T^-1(ker S) = ker T: composing with S adds nothing here.")

print()
print("=== (b) the sum rule names a different, larger subspace ===")
sum_basis = ker_S + ker_T
print(f"  ker(S) + ker(T) = {[[round(t, 6) for t in v] for v in sum_basis]}"
      f"   dimension {len(sum_basis)}")
print(f"  ker(S o T)      = {[[round(t, 6) for t in v] for v in null_space(ST)]}"
      f"   dimension {len(null_space(ST))}")
for probe in ([1.0, 0.0], [0.0, 1.0], [1.0, 1.0]):
    print(f"  probe {probe}: in ker(S o T) = {in_span_of(probe, null_space(ST))!s:5s}"
          f"  in ker(S)+ker(T) = {in_span_of(probe, sum_basis)}")
print("  (1,0) is in the sum but NOT killed: T(1,0) = (1,1) and S(1,1) = (0,1).")
print("  The sum rule overcounts by including it.")

print()
print("=== (c) a second pair where the rules DO agree ===")
T2 = [[1.0, 0.0], [0.0, 0.0]]     # (x, y) -> (x, 0)
print_matrix("T2", T2)
ST2 = matmul(S, T2)
print_matrix("S T2", ST2)
ker_T2 = null_space(T2)
print(f"  ker(T2)     = {[[round(t, 6) for t in v] for v in ker_T2]}")
print(f"  ker(S o T2) = {[[round(t, 6) for t in v] for v in null_space(ST2)]}"
      f"   dimension {len(null_space(ST2))}")
print(f"  ker(S) + ker(T2) dimension {len(ker_S) + len(ker_T2)}")
print("  S(T2(x,y)) = S(x, 0) = (0, 0) for every input, so ker(S o T2) = R^2,")
print("  which equals ker(S) + ker(T2). The rules agree here and disagree above,")
print("  so agreement is luck, not a theorem.")
print()
print("  The invariant that always holds: ker(S o T) CONTAINS ker(T), because T")
print("  maps ker(T) to 0 and 0 is in ker(S). A sum rule can never add the inputs")
print("  that T steers INTO ker(S), which is the extra content of a preimage.")

print()
print("=== (d) minimum-norm solution on the line ===")
A = [[1.0, 2.0, 3.0],
     [2.0, 4.0, 6.0]]
b = [6.0, 12.0]
x_p = [6.0, 0.0, 0.0]
v = null_space(A)[0]
print(f"b = {b} = 6 * col0, and col0 is an output, so b IS in the image")
print(f"x_p (x2 = 0) = {x_p},  A x_p = {matvec(A, x_p)}")
print(f"v = {v},  A v = {matvec(A, v)}")
print()
print("every t is a solution, because A(x_p + t v) = A x_p + t (A v) = b:")
for t in (-1.0, 0.0, 1.0, 2.4):
    xt = [x_p[i] + t * v[i] for i in range(3)]
    got = matvec(A, xt)
    ok = all(abs(got[i] - b[i]) < 1e-9 for i in range(2))
    print(f"  t = {t:5.1f} -> x = ({xt[0]:.4f}, {xt[1]:.4f}, {xt[2]:.4f})"
          f"   A x = b: {ok}")
print()
print(f"x_p . v   = {dot(x_p, v):.6f}")
print(f"v . v     = {dot(v, v):.6f}")
t_star = -dot(x_p, v) / dot(v, v)
x_min = [x_p[i] + t_star * v[i] for i in range(3)]
print(f"t* = -(x_p.v)/(v.v) = {t_star:.6f}   (NOT 0)")
print(f"x_min = ({x_min[0]:.6f}, {x_min[1]:.6f}, {x_min[2]:.6f})")
print(f"  A x_min  = {matvec(A, x_min)}")
print(f"  x_min . v = {dot(x_min, v):.2e}   perpendicular, so it is the foot")
print()
print(f"||x_p||^2   = {dot(x_p, x_p):.6f}")
print(f"||x_min||^2 = {dot(x_min, x_min):.6f}   smaller, as it must be")
print("The minimum-norm point is a different point on the line from the one you")
print("get by zeroing a free variable, so lstsq returns a choice, not the answer.")
```

Output:

```
=== (a) ker(T), ker(S), ker(S o T) ===
T  (2x2)
  |  1.000   0.000 |
  |  1.000   0.000 |
S  (2x2)
  |  0.000   0.000 |
  |  0.000   1.000 |
S T  (2x2)
  |  0.000   0.000 |
  |  1.000   0.000 |
  ker(T)     = [[0.0, 1.0]]
  ker(S)     = [[1.0, 0.0]]
  ker(S o T) = [[0.0, 1.0]]   dimension 1
  check S(T(0,1)) = [0.0, 0.0]   (zero)
  check S(T(1,1)) = [0.0, 1.0]   (nonzero)
  T's image is {(a,a)}, which meets ker(S) = {(b,0)} only at 0, so
  T^-1(ker S) = ker T: composing with S adds nothing here.

=== (b) the sum rule names a different, larger subspace ===
  ker(S) + ker(T) = [[1.0, 0.0], [0.0, 1.0]]   dimension 2
  ker(S o T)      = [[0.0, 1.0]]   dimension 1
  probe [1.0, 0.0]: in ker(S o T) = False  in ker(S)+ker(T) = True
  probe [0.0, 1.0]: in ker(S o T) = True   in ker(S)+ker(T) = True
  probe [1.0, 1.0]: in ker(S o T) = False  in ker(S)+ker(T) = True
  (1,0) is in the sum but NOT killed: T(1,0) = (1,1) and S(1,1) = (0,1).
  The sum rule overcounts by including it.

=== (c) a second pair where the rules DO agree ===
T2  (2x2)
  |  1.000   0.000 |
  |  0.000   0.000 |
S T2  (2x2)
  |  0.000   0.000 |
  |  0.000   0.000 |
  ker(T2)     = [[0.0, 1.0]]
  ker(S o T2) = [[1.0, 0.0], [0.0, 1.0]]   dimension 2
  ker(S) + ker(T2) dimension 2
  S(T2(x,y)) = S(x, 0) = (0, 0) for every input, so ker(S o T2) = R^2,
  which equals ker(S) + ker(T2). The rules agree here and disagree above,
  so agreement is luck, not a theorem.

  The invariant that always holds: ker(S o T) CONTAINS ker(T), because T
  maps ker(T) to 0 and 0 is in ker(S). A sum rule can never add the inputs
  that T steers INTO ker(S), which is the extra content of a preimage.

=== (d) minimum-norm solution on the line ===
b = [6.0, 12.0] = 6 * col0, and col0 is an output, so b IS in the image
x_p (x2 = 0) = [6.0, 0.0, 0.0],  A x_p = [6.0, 12.0]
v = [-2.0, 1.0, 0.0],  A v = [0.0, 0.0]

every t is a solution, because A(x_p + t v) = A x_p + t (A v) = b:
  t = -1.0 -> x = (8.0000, -1.0000, 0.0000)   A x = b: True
  t =  0.0 -> x = (6.0000, 0.0000, 0.0000)   A x = b: True
  t =  1.0 -> x = (4.0000, 1.0000, 0.0000)   A x = b: True
  t =  2.4 -> x = (1.2000, 2.4000, 0.0000)   A x = b: True

x_p . v   = -12.000000
v . v     = 5.000000
t* = -(x_p.v)/(v.v) = 2.400000   (NOT 0)
x_min = (1.200000, 2.400000, 0.000000)
  A x_min  = [6.0, 12.0]
  x_min . v = 4.44e-16   perpendicular, so it is the foot

||x_p||^2   = 36.000000
||x_min||^2 = 7.200000   smaller, as it must be
The minimum-norm point is a different point on the line from the one you
get by zeroing a free variable, so lstsq returns a choice, not the answer.
```

</details>

**[ ] Exercise 5 — linearity, the two kinds of invertibility, and the chain
rule.** (a) Test three maps on `u = (1, 0, 2)`, `v = (3, -1, 4)`, `c = -2` for
`T(u+v) = T(u) + T(v)`, `T(cu) = cT(u)` and `T(0) = 0`: the matrix
`A = [[1,2,3],[2,4,6]]`, the shift `(x,y) ↦ (x+1, y)`, and
`(x,y) ↦ (x² + y², 0)`. (b) For the four matrices
`A`, the projection `(x,y,z) ↦ (x,y)`, the `3 × 3` full-rank
`[[1,0,0],[0,1,1],[0,0,1]]`, and the `2 × 4` `[[1,2,3,4],[2,4,6,8]]`, report
`rank`, `dim(im)`, `dim(ker)`, and check rank-nullity each time. (c) Mark each as
injective, surjective, invertible, and say which rows have `injectivity ==
surjectivity`. (d) Build a right inverse `R` for the projection by hand, verify
`P R = id` on `ℝ²`, and show `R P ≠ id` on `ℝ³`. (e) For
`T = [[1,2],[0,1]]` and `S = [[0,1],[1,0]]`, confirm
`S(T x) = (S T) x` and `T(S x) = (T S) x`, that the two orders differ, and that
`ker(T) = ker(S) = {0}` so `ker(S T) = ker(T S) = {0}`.

**Challenge.** Take a one-layer network `out = relu(W v + b)` with
`W = [[1,-1,0.5],[0,2,-1]]`, `b = [0.5,-0.25]`, and `L` the plain sum of the
outputs. For `v = (1, -2, 3)`: (a) compute `W v + b` and the post-ReLU values;
(b) hand-compute the backward pass — the ReLU mask, then `Wᵀ g` — and write out
component 0 as a dot product of a **row** of `W` with the gradient; (c) verify all
three components against central finite differences with `h = 1e-6`; and (d)
explain in one paragraph why the transpose is forced, and what would go wrong if
you propagated with `W` instead on a square layer.

<details>
<summary>Solution</summary>

**Part (a).** The matrix passes all three checks, and it *must* — `A(u+v) = Au + Av`
is distributivity and `A(cu) = cAu` is factoring, so a matrix can never fail them.
A failure there would be an arithmetic slip, not a fact about the map.

The shift fails `T(0) = 0` immediately: `shift([0,0]) = [1.0, 0.0]`. That single
check settles it, and it is the cheapest test to run. Additivity fails too:
`shift(u) + shift(v) = [7.0, -1.0]` against `shift(u+v) = [6.0, -1.0]`.

The squared norm is the instructive one, because it **passes** `T(0) = 0` and still
fails linearity. It fails homogeneity: `T(2u) = T(2, 0, 4) = (4 + 16, 0) = (20, 0)`
while `2T(u) = 2(1 + 4, 0) = (10, 0)`. So "does it fix the origin" is the first
test, not the only one, and the general case has to be checked properly.

**Part (b).** Rank-nullity holds in all four cases: `1 + 2 = 3`, `2 + 1 = 3`,
`3 + 0 = 3`, `1 + 3 = 4`. Every kernel vector the code prints satisfies `M w = 0`
exactly.

**Part (c).** Only the `3 × 3` row has `injectivity == surjectivity`, and that is
the `dim V == dim W` case. The projection is the clean counterexample to
conflating them: `dim(im) = 2` equals its codomain, so it is **surjective**, while
`dim(ker) = 1`, so it is **not** injective. A right inverse exists; a left inverse
does not.

**Part (d).** Take `R(x, y) = (x, y, 0)`. Then `P R = id` on `ℝ²` for every
target, verified for `(1, 2)`, `(0, 0)` and `(-3.5, 7.25)`. But `R P` is not the
identity on `ℝ³`:

    R P (1, 2, 5)  = (1, 2, 0)     vs (1, 2, 5)
    R P (0, 0, 9)  = (0, 0, 0)     vs (0, 0, 9)

`R P` is itself a projection — it kills the `z` direction, which is exactly `ker P`.
This is the asymmetry in full: a **right** inverse exists for any surjective map
(a choice of preimage per output), a **left** inverse only for an injective one,
and "invertible" demands both.

**Part (e).** `T x = (12, 5)`, `S(T x) = (5, 12) = (S T) x`; `T(S x) = (9, 2) =
(T S) x`. The two orders differ, as they must for a shear and a swap. Both `T` and
`S` are invertible, so by the preimage rule `ker(S T) = T⁻¹(ker S) = T⁻¹({0}) = {0}`
and likewise for the other order — the code confirms empty kernel bases in all
four cases. Composing with an invertible map preserves the kernel exactly, which
is the sanity check the lesson's own worked example reaches after several wrong
turns.

**Challenge.** (a) `W v + b = (1 - (-2) + 0.5(3) + 0.5, 0 + 2(-2) - 3 - 0.25) =
(5.0, -7.25)`, and after ReLU, `(5.0, 0.0)`.

(b) With `L` the plain sum of the outputs, `∂L/∂out = (1, 1)`. The ReLU derivative
is 1 where the pre-activation is positive and 0 where it is negative, so
`∂L/∂z = (1, 0)` — the second component is switched off because `-7.25 < 0`. Then
`∂L/∂v = Wᵀ (∂L/∂z) = (1.0, -1.0, 0.5)`. Component 0 by hand:

    1.0·1.0 + 0.0·0.0 = 1.0

which is the first **row** of `W` dotted with `∂L/∂z` — a transpose, because the
gradient is a row vector contracting the rows of `W` unless you flip it.

(c) The central differences give `(1.000000, -1.000000, 0.500000)`, matching the
analytic values to six digits. So the backward pass is right, and the check is
cheap enough to run in a test.

(d) The transpose is forced by how the contraction lines up: with `g` a row
vector and `W` of shape `m × n`, the component is `∂L/∂v_j = Σ_i g_i w_ij`, a sum
over the **rows** of `W` weighted by `g`, which as a matrix product is `Wᵀ g`. (This
is lesson 31's `(AB)ᵀ = BᵀAᵀ` in a gradient.) Substituting `W` fails in three ways,
in increasing order of danger. On a non-square layer, `W g` is *undefined* — `W` is
`m × n` and `g` has length `m` — so it crashes immediately and a shape assertion
catches it. On a **square** layer `W g` is defined and still wrong: the shape
matches, the entries do not, and optimisation proceeds to a worse model with no
error anywhere. And in a composition the error is systematic, not a rounding
artefact: for `y = W₂W₁x` the gradient flows back as `W₁ᵀW₂ᵀ g`, the reverse of the
forward order, because `(W₂W₁)ᵀ = W₁ᵀW₂ᵀ`; propagating in forward order computes
a different matrix, equal only when the layers commute — and deep networks are
built to be non-commutative precisely so that order matters.

```python
TOL = 1e-9


# ---------------------------------------------------------------- helpers
def shape(M):
    return len(M), len(M[0])


def zeros(rows, cols):
    return [[0.0] * cols for _ in range(rows)]


def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def matmul(A, B):
    rows_a, cols_a = shape(A)
    rows_b, cols_b = shape(B)
    if cols_a != rows_b:
        raise ValueError(f"cannot multiply {rows_a}x{cols_a} by {rows_b}x{cols_b}")
    return [[sum(A[i][k] * B[k][j] for k in range(cols_a)) for j in range(cols_b)]
            for i in range(rows_a)]


def matvec(M, v):
    rows, cols = shape(M)
    if len(v) != cols:
        raise ValueError(f"vector has {len(v)} entries, matrix has {cols} columns")
    return [sum(M[i][k] * v[k] for k in range(cols)) for i in range(rows)]


def rref(A, tol=TOL):
    M = [list(row) for row in A]
    rows, cols = len(M), len(M[0])
    pivot_row, pivots = 0, []
    for col in range(cols):
        if pivot_row == rows:
            break
        best = max(range(pivot_row, rows), key=lambda r: abs(M[r][col]))
        if abs(M[best][col]) <= tol:
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
    return len(rref(A, tol)[1])


def null_space(A, tol=TOL):
    M, pivots = rref(A, tol)
    cols = shape(A)[1]
    basis = []
    for fc in [c for c in range(cols) if c not in pivots]:
        v = [0.0] * cols
        v[fc] = 1.0
        for i, pc in enumerate(pivots):
            v[pc] = -M[i][fc]
        basis.append(v)
    return basis


def image_basis(A, tol=TOL):
    _, pivots = rref(A, tol)
    return [[A[i][c] for i in range(len(A))] for c in pivots]


def print_matrix(label, M, width=7):
    rows, cols = shape(M)
    print(f"{label}  ({rows}x{cols})")
    for row in M:
        print("  | " + " ".join(f"{x:{width}.3f}" for x in row) + " |")


def print_vector(label, v, width=7):
    print(f"{label} = [" + ", ".join(f"{x:{width}.3f}" for x in v) + "]")


# ---------------------------------------------------------------- (a)
print("=== (a) linearity tests on three maps ===")
A = [[1.0, 2.0, 3.0], [2.0, 4.0, 6.0]]


def shifted(w):
    """(x, y, z) -> (x + 1, y, z): affine, NOT linear."""
    return [w[0] + 1.0, w[1], w[2]]


def squared_norm(w):
    """(x, y, z) -> (x^2 + y^2 + z^2, 0, 0): passes T(0)=0, still not linear."""
    return [w[0] ** 2 + w[1] ** 2 + w[2] ** 2, 0.0, 0.0]


u = [1.0, 0.0, 2.0]
v = [3.0, -1.0, 4.0]
c = -2.0
u_plus_v = [a + b for a, b in zip(u, v)]
c_u = [c * t for t in u]
for name, f, out_dim in (("A  (a matrix: 3 in, 2 out)", lambda w: matvec(A, w), 2),
                         ("shift  (x,y,z) -> (x+1, y, z)", shifted, 3),
                         ("squared norm  -> (x^2+y^2+z^2, 0, 0)", squared_norm, 3)):
    add_ok = f(u_plus_v) == [a + b for a, b in zip(f(u), f(v))]
    scale_ok = f(c_u) == [c * t for t in f(u)]
    zero_ok = f([0.0] * 3) == [0.0] * out_dim
    verdict = "LINEAR" if (add_ok and scale_ok and zero_ok) else "not linear"
    print(f"  {name}")
    print(f"    T(u+v) == T(u)+T(v)  : {add_ok}")
    print(f"    T(cu)   == c T(u)    : {scale_ok}")
    print(f"    T(0)    == 0         : {zero_ok}")
    print(f"    => {verdict}")
print()
print("  shift: T(0) =", shifted([0.0, 0.0, 0.0]), "fails the cheapest test.")
print("  squared norm PASSES T(0) = 0 and still is not linear, because it fails")
print("    homogeneity: T(c u) =", [round(t, 4) for t in squared_norm(c_u)])
print("                 c T(u) =", [round(c * t, 4) for t in squared_norm(u)])
print("  so T(0) = 0 is the first test, not the only one.")
print("  A matrix can never fail the first two: those are distributivity and")
print("  factoring. A failure there is an arithmetic slip, not a fact.")

# ---------------------------------------------------------------- (b)
print()
print("=== (b) rank, image, kernel, rank-nullity ===")
matrices = [
    ("A (2x3, rank 1)", [[1.0, 2.0, 3.0], [2.0, 4.0, 6.0]]),
    ("projection (x,y,z) -> (x,y)", [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]),
    ("3x3 full rank", [[1.0, 0.0, 0.0], [0.0, 1.0, 1.0], [0.0, 0.0, 1.0]]),
    ("2x4, rank 1", [[1.0, 2.0, 3.0, 4.0], [2.0, 4.0, 6.0, 8.0]]),
]
for name, M in matrices:
    r = rank(M)
    ker = null_space(M)
    img = image_basis(M)
    print(f"  {name}: rank {r}, dim(im) {len(img)}, dim(ker) {len(ker)}"
          f" = n - r = {shape(M)[1]} - {r}")
    for w in ker:
        print(f"      ker {w}   M w = {matvec(M, w)}")
    for w in img:
        print(f"      im  {w}")
    assert len(ker) == shape(M)[1] - r and len(img) == r
print("  rank-nullity holds in every case and every kernel vector vanishes.")
print("  The projection: dim(im) = 2 = its codomain, so it is SURJECTIVE, yet")
print("  dim(ker) = 1, so it is not injective. dim(V) = 3 != dim(W) = 2.")

# ---------------------------------------------------------------- (c)
print()
print("=== (c) injective, surjective, invertible ===")
print(f"  {'map':34s} {'dim V':>6s} {'dim W':>6s} {'ker':>4s} "
      f"{'inj':>6s} {'surj':>6s} {'inv':>6s}")
for name, M in matrices:
    rows, cols = shape(M)
    ker_dim = len(null_space(M))
    inj = ker_dim == 0
    surj = len(image_basis(M)) == rows
    inv = inj and surj
    print(f"  {name:34s} {cols:6d} {rows:6d} {ker_dim:4d} "
          f"{str(inj):>6s} {str(surj):>6s} {str(inv):>6s}")
print()
print("Only the square 3x3 has inj == surj, and that is the dim V == dim W case.")
print("In every other row the two properties come apart.")

# ---------------------------------------------------------------- (d)
print()
print("=== (d) a right inverse for the projection, and why it is not a left one ===")
P = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]      # (x,y,z) -> (x,y)
R = [[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]   # (x,y) -> (x,y,0)
print_matrix("P (2x3)", P)
print_matrix("R (3x2)", R)
for target in ([1.0, 2.0], [0.0, 0.0], [-3.5, 7.25]):
    got = matvec(P, matvec(R, target))
    print(f"  P R {target} = {got}   correct: {got == target}")
print("  so R is a right inverse of P on R^2. But R P is not the identity on R^3:")
for w in ([1.0, 2.0, 5.0], [0.0, 0.0, 9.0]):
    got = matvec(R, matvec(P, w))
    print(f"    R P {w} = {got}   vs original {w}")
print("  R P is itself a projection: it kills the z direction, which is ker P.")
print("  A right inverse exists for any surjective map; a left inverse needs")
print("  injectivity; 'invertible' demands both.")

# ---------------------------------------------------------------- (e)
print()
print("=== (e) composition with invertible maps ===")
T = [[1.0, 2.0], [0.0, 1.0]]            # shear
S = [[0.0, 1.0], [1.0, 0.0]]            # swap
x = [2.0, 5.0]
print_matrix("T (shear)", T)
print_matrix("S (swap)", S)
print(f"  x = {x}")
print(f"  T x         = {matvec(T, x)}")
print(f"  S(T x)      = {matvec(S, matvec(T, x))}")
print(f"  (S T) x     = {matvec(matmul(S, T), x)}   equal: "
      f"{matvec(S, matvec(T, x)) == matvec(matmul(S, T), x)}")
print(f"  T(S x)      = {matvec(T, matvec(S, x))}")
print(f"  (T S) x     = {matvec(matmul(T, S), x)}   equal: "
      f"{matvec(T, matvec(S, x)) == matvec(matmul(T, S), x)}")
ST = matmul(S, T)
TS = matmul(T, S)
print(f"  the two orders differ: {ST != TS}")
print()
print(f"  ker(T)   = {[[round(t, 4) for t in v] for v in null_space(T)]}  (invertible)")
print(f"  ker(S)   = {[[round(t, 4) for t in v] for v in null_space(S)]}  (invertible)")
print(f"  ker(S T) = {[[round(t, 4) for t in v] for v in null_space(ST)]}")
print(f"  ker(T S) = {[[round(t, 4) for t in v] for v in null_space(TS)]}")
print("  All four are trivial, as the preimage rule predicts: with ker S = {0},")
print("  ker(S o T) = T^-1({0}) = {0} = ker T. Composing with an invertible map")
print("  preserves the kernel exactly.")
print()
print(f"  im(T) basis    = {image_basis(T)}")
print(f"  S(im T)        = {[matvec(S, w) for w in image_basis(T)]}")
print(f"  im(S T) basis  = {image_basis(ST)}")
print("  S(im T) IS the image of the composition, as im(S o T) = S(im T) says.")

# ---------------------------------------------------------------- Challenge
print()
print("=== Challenge: one layer, backprop by hand, verified numerically ===")
W = [[1.0, -1.0, 0.5],
     [0.0, 2.0, -1.0]]
b_layer = [0.5, -0.25]
print_matrix("W (2x3)", W)
print(f"bias b = {b_layer}")


def relu(t):
    return max(0.0, t)


def network(vv):
    z = [sum(W[i][k] * vv[k] for k in range(3)) + b_layer[i] for i in range(2)]
    return [relu(t) for t in z], z


v = [1.0, -2.0, 3.0]
out, z = network(v)
print(f"v           = {v}")
print(f"W v + b     = {[round(t, 6) for t in z]}")
print(f"after ReLU  = {[round(t, 6) for t in out]}")
print()
print("(a) done above: the first pre-activation is positive, the second negative.")
print()
g = [1.0, 1.0]        # dL/dout, with L the plain sum of the outputs
mask = [1.0 if t > 0 else 0.0 for t in z]
g_z = [g[i] * mask[i] for i in range(2)]
g_in = [sum(W[i][k] * g_z[i] for i in range(2)) for k in range(3)]
print("(b) the backward pass, by hand:")
print(f"  dL/dout = {g}   (L is the plain sum of the outputs)")
print(f"  ReLU mask (z > 0) = {mask}")
print(f"  dL/dz   = {g_z}   (the second component is switched off)")
print(f"  dL/dv   = W^T (dL/dz) = {[round(t, 6) for t in g_in]}")
c0 = sum(W[i][0] * g_z[i] for i in range(2))
print(f"  component 0 by hand: row 0 of W dotted with dL/dz = "
      f"{W[0][0]:g}*{g_z[0]:g} + {W[1][0]:g}*{g_z[1]:g} = {c0:g}")
print("  that is a ROW of W, so the product is a TRANSPOSE: W^T g.")
print()
h = 1e-6
print(f"(c) central differences on v, h = {h:g}:")
for k in range(3):
    vp = list(v)
    vm = list(v)
    vp[k] += h
    vm[k] -= h
    fd = (sum(network(vp)[0]) - sum(network(vm)[0])) / (2 * h)
    print(f"  v_{k}: finite difference {fd:12.6f}   analytic {g_in[k]:12.6f}"
          f"   match: {abs(fd - g_in[k]) < 1e-5}")
print()
print("(d) The transpose is forced: dL/dv_j = sum_i g_i w_ij sums over the ROWS")
print("of W weighted by g, which as a matrix product is W^T g. Substituting W:")
print("  - on a 2x3 layer, W g is undefined, so it crashes and a shape check")
print("    catches it immediately;")
print("  - on a SQUARE layer W g is defined and still wrong: right shape, wrong")
print("    entries, and optimisation converges to a worse model with no error;")
print("  - in a composition it is systematic, not rounding: the gradient through")
print("    y = W2 W1 x is W1^T W2^T g, the reverse order, since (W2 W1)^T =")
print("    W1^T W2^T. Forward order gives a different matrix unless the layers")
print("    commute, and deep networks are built not to.")
```

Output:

```
=== (a) linearity tests on three maps ===
  A  (a matrix)
    T(u+v) == T(u)+T(v)  : True
    T(cu)   == c T(u)    : True
    T(0)    == 0         : True
    => LINEAR
  shift  (x,y,z) -> (x+1, y, z)
    T(u+v) == T(u)+T(v)  : False
    T(cu)   == c T(u)    : False
    T(0)    == 0         : False
    => not linear
  squared norm  -> (x^2+y^2+z^2, 0, 0)
    T(u+v) == T(u)+T(v)  : False
    T(cu)   == c T(u)    : False
    T(0)    == 0         : True
    => not linear

  shift: T(0) = [1.0, 0.0, 0.0] fails the cheapest test.
  squared norm PASSES T(0) = 0 and still is not linear, because it fails
    homogeneity: T(c u) = [20.0, 0.0, 0.0]
                 c T(u) = [-10.0, -0.0, -0.0]
  so T(0) = 0 is the first test, not the only one.
  A matrix can never fail the first two: those are distributivity and
  factoring. A failure there is an arithmetic slip, not a fact.

=== (b) rank, image, kernel, rank-nullity ===
  A (2x3, rank 1): rank 1, dim(im) 1, dim(ker) 2 = n - r = 3 - 1
      ker [-2.0, 1.0, 0.0]   M w = [0.0, 0.0]
      ker [-3.0, 0.0, 1.0]   M w = [0.0, 0.0]
      im  [1.0, 2.0]
  projection (x,y,z) -> (x,y): rank 2, dim(im) 2, dim(ker) 1 = n - r = 3 - 2
      ker [-0.0, -0.0, 1.0]   M w = [0.0, 0.0]
      im  [1.0, 0.0]
      im  [0.0, 1.0]
  3x3 full rank: rank 3, dim(im) 3, dim(ker) 0 = n - r = 3 - 3
      im  [1.0, 0.0, 0.0]
      im  [0.0, 1.0, 0.0]
      im  [0.0, 1.0, 1.0]
  2x4, rank 1: rank 1, dim(im) 1, dim(ker) 3 = n - r = 4 - 1
      ker [-2.0, 1.0, 0.0, 0.0]   M w = [0.0, 0.0]
      ker [-3.0, 0.0, 1.0, 0.0]   M w = [0.0, 0.0]
      ker [-4.0, 0.0, 0.0, 1.0]   M w = [0.0, 0.0]
      im  [1.0, 2.0]
  rank-nullity holds in every case and every kernel vector vanishes.
  The projection: dim(im) = 2 = its codomain, so it is SURJECTIVE, yet
  dim(ker) = 1, so it is not injective. dim(V) = 3 != dim(W) = 2.

=== (c) injective, surjective, invertible ===
  map                                 dim V  dim W  ker    inj   surj    inv
  A (2x3, rank 1)                         3      2    2  False  False  False
  projection (x,y,z) -> (x,y)             3      2    1  False   True  False
  3x3 full rank                           3      3    0   True   True   True
  2x4, rank 1                             4      2    3  False  False  False

Only the square 3x3 has inj == surj, and that is the dim V == dim W case.
In every other row the two properties come apart.

=== (d) a right inverse for the projection, and why it is not a left one ===
P (2x3)
  |  1.000   0.000   0.000 |
  |  0.000   1.000   0.000 |
R (3x2)
  |  1.000   0.000 |
  |  0.000   1.000 |
  |  0.000   0.000 |
  P R [1.0, 2.0] = [1.0, 2.0]   correct: True
  P R [0.0, 0.0] = [0.0, 0.0]   correct: True
  P R [-3.5, 7.25] = [-3.5, 7.25]   correct: True
  so R is a right inverse of P on R^2. But R P is not the identity on R^3:
    R P [1.0, 2.0, 5.0] = [1.0, 2.0, 0.0]   vs original [1.0, 2.0, 5.0]
    R P [0.0, 0.0, 9.0] = [0.0, 0.0, 0.0]   vs original [0.0, 0.0, 9.0]
  R P is itself a projection: it kills the z direction, which is ker P.
  A right inverse exists for any surjective map; a left inverse needs
  injectivity; 'invertible' demands both.

=== (e) composition with invertible maps ===
T (shear)  (2x2)
  |   1.000   2.000 |
  |   0.000   1.000 |
S (swap)  (2x2)
  |   0.000   1.000 |
  |   1.000   0.000 |
  x = [2.0, 5.0]
  T x         = [12.0, 5.0]
  S(T x)      = [5.0, 12.0]
  (S T) x     = [5.0, 12.0]   equal: True
  T(S x)      = [9.0, 2.0]
  (T S) x     = [9.0, 2.0]   equal: True
  the two orders differ: True

  ker(T)   = []  (invertible)
  ker(S)   = []  (invertible)
  ker(S T) = []
  ker(T S) = []
  All four are trivial, as the preimage rule predicts: with ker S = {0},
  ker(S o T) = T^-1({0}) = {0} = ker T. Composing with an invertible map
  preserves the kernel exactly.

  im(T) basis    = [[1.0, 0.0], [2.0, 1.0]]
  S(im T)        = [[0.0, 1.0], [1.0, 2.0]]
  im(S T) basis  = [[0.0, 1.0], [1.0, 2.0]]
  S(im T) IS the image of the composition, as im(S o T) = S(im T) says.

=== Challenge: one layer, backprop by hand, verified numerically ===
W (2x3)
  |   1.000  -1.000   0.500 |
  |   0.000   2.000  -1.000 |
bias b = [0.5, -0.25]
v           = [1.0, -2.0, 3.0]
W v + b     = [5.0, -7.25]
after ReLU  = [5.0, 0.0]

(a) done above: the first pre-activation is positive, the second negative.

(b) the backward pass, by hand:
  dL/dout = [1.0, 1.0]   (L is the plain sum of the outputs)
  ReLU mask (z > 0) = [1.0, 0.0]
  dL/dz   = [1.0, 0.0]   (the second component is switched off)
  dL/dv   = W^T (dL/dz) = [1.0, -1.0, 0.5]
  component 0 by hand: row 0 of W dotted with dL/dz = 1*1 + 0*0 = 1
  that is a ROW of W, so the product is a TRANSPOSE: W^T g.

(c) central differences on v, h = 1e-06:
  v_0: finite difference     1.000000   analytic     1.000000   match: True
  v_1: finite difference    -1.000000   analytic    -1.000000   match: True
  v_2: finite difference     0.500000   analytic     0.500000   match: True

(d) The transpose is forced: dL/dv_j = sum_i g_i w_ij sums over the ROWS
of W weighted by g, which as a matrix product is W^T g. Substituting W:
  - on a 2x3 layer, W g is undefined, so it crashes and a shape check
    catches it immediately;
  - on a SQUARE layer W g is defined and still wrong: right shape, wrong
    entries, and optimisation converges to a worse model with no error;
  - in a composition it is systematic, not rounding: the gradient through
    y = W2 W1 x is W1^T W2^T g, the reverse order, since (W2 W1)^T =
    W1^T W2^T. Forward order gives a different matrix unless the layers
    commute, and deep networks are built not to.
```

</details>

**[ ] Exercise 6 — four spaces, redundancy, preimages, and what a kernel
destroys.** (a) For the `3 × 4` design matrix

    A = | 1  2  3  4 |
        | 5  6  7  9 |
        | 2  3  4  5 |

report the rank, a basis for the row space, a basis for the column space (using
pivot columns of the **original** `A`), and a basis for the kernel. Give the
ambient space of each one, and check rank-nullity twice: as
`dim(ker) = n - r`, and as `dim(row) = dim(col) = r`.

(b) Take the `5 × 5` dataset of five students, with columns
`hours`, `rate`, `score`, `projects`, `rating`:

    | 3.0  0.90  48.0  10.0  6.0 |
    | 5.0  0.80  66.0  12.0  7.0 |
    | 2.0  0.60  32.0   8.0  5.0 |
    | 4.0  0.95  59.0  11.0  6.5 |
    | 6.0  0.85  77.0  13.0  8.0 |

Find the kernel, name the columns that appear in the nonzero coordinates of the
null vector, and verify the relation row by row. Then drop the `score` column
and recompute the rank, to confirm you removed redundancy rather than
information.

(c) For `T(x, y) = (x, x)` and `S(u, v) = (0, v)`, compute `ker(T)`, `ker(S)` and
`ker(S T)` directly. Then show by explicit substitution that
`ker(S T) = T⁻¹(ker S)` is the right rule and
`ker(S T) = ker(S) + ker(T)` is the wrong one, and say in one sentence what
makes it wrong.

(d) The screen projection `P(x, y, z) = (x, y)` has a kernel. Find it, then take
the two 3-D points `(1, 2, 5)` and `(1, 2, 900)` and show that `B - A` is a
scalar multiple of your kernel vector. Explain in one sentence what a renderer
loses by using `P`, and then show that the `4 × 4` homogeneous version has a
trivial kernel.

(e) For `W = [[1, -1, 0.5], [0, 2, -1]]` and `b = [0.5, -0.25]`, take
`u = (1, -2, 3)` and `v = u + k` for a kernel vector `k` of `W`. Show
`W u + b = W v + b`, and then show the ReLU outputs agree too. Explain in one
paragraph why no layer placed *after* `W` can undo this, and identify the
different set of inputs the ReLU itself makes indistinguishable.

**Challenge.** A colleague claims that a neural network "has a kernel, like every
linear map". (a) Refute the claim for the network `relu(W v + b)` above by
producing two distinct inputs the ReLU network *does* separate, and say what
condition on the stack would make the claim true instead. (b) Characterise the
set of inputs the ReLU collapses, and say which subspace axiom it fails — try the
zero vector first, since that is the cheapest test, and say what to do when it
comes back inconclusive. (c) For a stack of `L` purely linear layers with widths
`w₁, …, w_L`, give the dimension of the kernel of the composed map, and explain
in one paragraph why the nonlinearity is the only thing in the stack that widens
it.

<details>
<summary>Solution</summary>

**Part (a).** The rank is `3`, which is the maximum for a `3`-row matrix, so `A`
is surjective onto `ℝ³` and the column space is all of `ℝ³`.

The three spaces and their ambient homes:

| space | ambient | dimension | where the basis comes from |
|---|---|---|---|
| row space | `ℝ⁴` | `3` | the nonzero rows of the RREF |
| column space | `ℝ³` | `3` | pivot columns `[0, 1, 3]` of the **original** `A` |
| kernel | `ℝ⁴` | `1` | free variable `x₃` set to `1` |

The ambient space is the single most commonly botched detail here. The row space
is a set of 4-vectors because a row is read as a coefficient vector for the
model; the column space is a set of 3-vectors because a column is a prediction
for one of the three observations. They have the same dimension and live in
different rooms.

Rank-nullity checks out both ways: `dim(ker) = 4 - 3 = 1`, and
`3 + (4 - 3) = 4 = n`, so the domain splits completely. And
`dim(row) = dim(col) = 3 = r`, the row-rank-equals-column-rank theorem stated in
map language.

**Part (b).** The rank is `4` of `5`, so the kernel is one-dimensional and there
is exactly one relation among the columns — up to scaling. It is

    score = 10 · hours + 20 · rate

and the null vector `(-10, -20, 1, 0, 0)` reads off that identity directly: the
coefficient of a column is how many times it appears on the right. The zeros in
positions 3 and 4 are the substantive part of the answer. They say `projects`
and `rating` are *not* involved in the redundancy — this is one local
dependency, not a general collapse of the dataset.

The row-by-row subtraction is the honest verification, and every residual is
`+0.000000`, not "small". The relation was built to be exact, so if you see
`1e-13` here your data or your arithmetic is wrong.

Dropping `score` leaves the rank at `4`. That is the point: `score` was a
*linear combination of columns already present*, so it added a kernel direction
without adding any reachable prediction. Removing it costs you no rank. The
practical reading is that you can predict the score from the other four features
exactly and should not spend a coefficient on it.

**Part (c).** Directly:

    ker(T)   = span{(0, 1)}     since T(x, y) = (x, x) = 0 forces x = 0
    ker(S)   = span{(1, 0)}     since S(u, v) = (0, v) = 0 forces v = 0
    ker(S T) = span{(0, 1)}

`S T` maps `(x, y) ↦ (0, x)`, so `S T = 0` forces `x = 0` and leaves `y` free.
The preimage rule is right: `ker(S T) = T⁻¹(ker S)`, and since `ker S = {(0, 0)}`,
the preimage is exactly the set `T` sends to `0`, namely `ker T`. The
substitutions confirm it: `T(0, 1) = (0, 0)` is in `ker S`; `T(1, 1) = (1, 1)` and
`T(5, 0) = (5, 5)` are not.

The sum rule predicts dimension `1 + 1 = 2` and the truth is `1`. It is wrong
because `S` never touches the input — it acts on `T`'s **output**. Only the
inputs whose *outputs* land in `ker S` qualify, and `ker T` is generally a
subset of that set, not a co-equal summand. Here `T⁻¹(ker S)` happens to equal
`ker T` because `ker S` is trivial, so the two rules differ only in the
arithmetic; on a less degenerate example they differ as sets.

**Part (d).** `ker(P) = span{(0, 0, 1)}`, and the difference of the two points is
`B - A = (0, 0, 895) = 895 · (0, 0, 1)` — a pure kernel vector, which is the
only way two points can share an image. Two points 895 units apart in depth
produce the identical pixel, so a 3-D renderer has thrown away exactly the
coordinate its depth buffer exists to sort on. Z-fighting is not a precision
problem here; it is a rank problem, and no amount of depth precision fixes it.

The `4 × 4` homogeneous matrix has rank `4`, so `dim(ker) = 4 - 4 = 0` and
distinct points stay distinct. Keeping the divide until the very end is what
preserves this.

**Part (e).** With `k = (0, 0.5, 1)`, the pre-activations are
`W u + b = (5.0, -7.25)` and `W v + b = (5.0, -7.25)` — equal, because
`W k = 0`. The ReLU outputs agree too: `(5.0, 0.0)` both times.

The reason nothing downstream helps is not about ReLU specifically. A kernel
collision means two inputs reach the rest of the network as the *same* number.
Any function whatsoever of an equal argument is equal, so if the next layer is a
deterministic map — linear, ReLU, softmax, or a composition of all three — it
receives one value and has nothing to work with. The information is destroyed
at the linear layer, not hidden at the ReLU.

The ReLU is itself not injective, for a different reason: it collapses the whole
negative orthant. `relu(-1, -2) = relu(-3, -7) = (0, 0)`. That is a much milder
and structurally different failure than a linear kernel — it is a half-space
sitting at the origin, not a subspace through it.

```python
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
    rows, cols = shape(M)
    if len(v) != cols:
        raise ValueError(f"vector has {len(v)} entries, matrix has {cols} columns")
    return [sum(M[i][k] * v[k] for k in range(cols)) for i in range(rows)]


def rref(A, tol=TOL):
    M = [list(row) for row in A]
    rows, cols = len(M), len(M[0])
    pivot_row, pivots = 0, []
    for col in range(cols):
        if pivot_row == rows:
            break
        best = max(range(pivot_row, rows), key=lambda r: abs(M[r][col]))
        if abs(M[best][col]) <= tol:
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
    return len(rref(A, tol)[1])


def null_space(A, tol=TOL):
    M, pivots = rref(A, tol)
    cols = shape(A)[1]
    basis = []
    for fc in [c for c in range(cols) if c not in pivots]:
        v = [0.0] * cols
        v[fc] = 1.0
        for i, pc in enumerate(pivots):
            v[pc] = -M[i][fc]
        basis.append(v)
    return basis


def image_basis(A, tol=TOL):
    _, pivots = rref(A, tol)
    return [[A[i][c] for i in range(len(A))] for c in pivots]


def print_matrix(label, M, width=7):
    rows, cols = shape(M)
    print(f"{label}  ({rows}x{cols})")
    for row in M:
        print("  | " + " ".join(f"{x:{width}.3f}" for x in row) + " |")


def say(text=""):
    print(text)


# ---------------------------------------------------------------- 1
say("=== Part 1: the four spaces of a 3x4 design matrix ===")
A = [[1.0, 2.0, 3.0, 4.0],
     [5.0, 6.0, 7.0, 9.0],
     [2.0, 3.0, 4.0, 5.0]]
print_matrix("A (3x4: 3 observations, 4 features)", A)
m, n = shape(A)
r = rank(A)
Mrr, piv = rref(A)
row_b = [row for row in Mrr if any(abs(t) > TOL for t in row)]
col_b = image_basis(A)
ker_b = null_space(A)
say()
say(f"rank r = {r}, m = {m} rows, n = {n} columns")
say(f"  row space     in R^{n}, dim {len(row_b)}   basis = nonzero RREF rows")
for w in row_b:
    say(f"      {w}")
say(f"  column space  in R^{m}, dim {len(col_b)}   basis = pivot columns {piv} of the ORIGINAL A")
for w in col_b:
    say(f"      {w}")
say(f"  kernel        in R^{n}, dim {len(ker_b)} = n - r = {n} - {r}")
for w in ker_b:
    say(f"      {[round(t, 4) for t in w]}      A w = {[round(t, 12) for t in matvec(A, w)]}")
say()
say(f"  r + (n - r) = {r} + {n - r} = {r + n - r} = n = {n}   (rank-nullity)")
say(f"  dim(row) = {len(row_b)} = dim(col) = {len(col_b)} = r = {r}")
say()
say("The row space lives in R^4 (one entry per COLUMN, so a coefficient vector")
say("for the model) and the column space in R^3 (one entry per ROW, so a")
say("prediction). Different ambient spaces, same dimension: the row-rank-equals-")
say("column-rank theorem of lesson 34, seen from the map side.")

# ---------------------------------------------------------------- 2
say()
say("=== Part 2: a dataset with one genuinely redundant feature ===")
D = [[3.0, 0.90, 48.0, 10.0, 6.0],
     [5.0, 0.80, 66.0, 12.0, 7.0],
     [2.0, 0.60, 32.0,  8.0, 5.0],
     [4.0, 0.95, 59.0, 11.0, 6.5],
     [6.0, 0.85, 77.0, 13.0, 8.0]]
say("5 observations x 5 features, built so col 2 = 10*col 0 + 20*col 1 exactly:")
for row in D:
    say(f"  {row}")
rd = rank(D)
ncol = shape(D)[1]
say()
say(f"rank = {rd} of {ncol} columns, so dim(ker) = {ncol} - {rd} = {ncol - rd}")
for w in null_space(D):
    # Round for display: the rref arithmetic leaves 1e-14 noise in the
    # coefficients that are mathematically zero.
    shown = [0.0 if abs(t) < 1e-9 else round(t, 4) for t in w]
    say(f"  null vector {shown}")
    say(f"    A w = {[round(t, 12) for t in matvec(D, w)]}")
    nz = [(i, shown[i]) for i in range(ncol) if shown[i] != 0.0]
    say(f"    nonzero entries at {nz}")
    say("    so the relation involves exactly those columns; every other")
    say("    coefficient is zero, and the redundancy is confined to them.")
say()
say("Column 2 is score, and col 2 - 10*col 0 - 20*col 1 = 0 row by row:")
for row in D:
    say(f"  {row[2]} - 10*{row[0]} - 20*{row[1]} = {row[2] - 10 * row[0] - 20 * row[1]:+.6f}")
say()
trimmed = [row[:2] + row[3:] for row in D]
say(f"rank with 5 columns = {rd}")
say(f"rank with 4 columns (score dropped) = {rank(trimmed)}")
say("Same rank, so nothing inside the span was lost.")

# ---------------------------------------------------------------- 3
say()
say("=== Part 3: ker(S o T) is a PREIMAGE, verified ===")
T = [[1.0, 0.0], [1.0, 0.0]]      # (x, y) -> (x, x)
S = [[0.0, 0.0], [0.0, 1.0]]      # (u, v) -> (0, v)
print_matrix("T  (x,y) -> (x,x)", T)
print_matrix("S  (u,v) -> (0,v)", S)
print_matrix("S T", matmul(S, T))
ker_T = null_space(T)
ker_S = null_space(S)
ker_ST = null_space(matmul(S, T))
say()
say(f"  ker(T)   = {[[round(t, 4) for t in w] for w in ker_T]}")
say(f"  ker(S)   = {[[round(t, 4) for t in w] for w in ker_S]}")
say(f"  ker(S T) = {[[round(t, 4) for t in w] for w in ker_ST]}")
say(f"  the SUM rule would give dim {len(ker_S)} + {len(ker_T)} = {len(ker_S) + len(ker_T)}")
say(f"  the truth is dim ker(S T) = {len(ker_ST)}")
say()
say("  Direct check of the preimage rule: ker(S o T) = T^-1(ker S) = ker T,")
say("  because ker S = {(0,0)} and only the inputs T maps to 0 qualify.")
for w in ([0.0, 1.0], [1.0, 1.0], [5.0, 0.0]):
    t_out = matvec(T, w)
    s_out = matvec(S, t_out)
    in_ker_S = all(abs(t) <= TOL for t in t_out)
    say(f"    T{w} = {t_out}  in ker(S)? {in_ker_S}   S(T w) = {s_out}")
say()
say("  Both (0,1) and (0,0) are in ker(S T): T sends them to 0 and S kills 0.")
say("  (1,1) is NOT: T(1,1) = (1,1) is not in ker(S), and S(1,1) = (0,1) != 0.")
say()
say("  The sum rule overcounts here and undercounts in general: S never touches")
say("  the input, it acts on T's OUTPUT. What matters is which of T's outputs S")
say("  kills, not which inputs S would have killed on its own.")

# ---------------------------------------------------------------- 4
say()
say("=== Part 4: a projection has a kernel, which is fatal for rendering ===")
P = [[1.0, 0.0, 0.0],
     [0.0, 1.0, 0.0]]      # (x, y, z) -> (x, y)
print_matrix("P  (x,y,z) -> (x,y)", P)
kp = null_space(P)
say(f"  rank {rank(P)}, dim(ker) = {shape(P)[1]} - {rank(P)} = {shape(P)[1] - rank(P)}")
say(f"  ker(P) = {[[round(t, 6) for t in w] for w in kp]}")
p1 = [1.0, 2.0, 5.0]
p2 = [1.0, 2.0, 900.0]
say()
say(f"  point A = {p1}  ->  P A = {matvec(P, p1)}")
say(f"  point B = {p2}  ->  P B = {matvec(P, p2)}")
say(f"  same 2-D point from points {abs(p2[2] - p1[2]):g} units apart in z")
diff = [p2[i] - p1[i] for i in range(3)]
scale = diff[2] / kp[0][2]
say(f"  B - A = {diff}")
say(f"  that is {scale:g} * the kernel basis {kp[0]}")
say(f"  check: {scale:g} * {[round(t, 6) for t in kp[0]]} = {[scale * t for t in kp[0]]}")
say()
say("  Two DISTINCT 3-D points give the SAME 2-D point. That is the whole failure:")
say("  the projection has a nontrivial kernel, so the renderer cannot tell them")
say("  apart and the depth buffer stores z-fighting instead of resolving it.")
say("  Adding a 4th homogeneous coordinate and keeping the divide until the end")
say("  gives an invertible 4x4 matrix:")
Q = [[1.0, 0.0, 0.0, 0.0],
     [0.0, 1.0, 0.0, 0.0],
     [0.0, 0.0, 1.0, 0.0],
     [0.0, 0.0, 0.0, 1.0]]
say(f"    rank of the 4x4 identity = {rank(Q)}, dim(ker) = {shape(Q)[1]} - {rank(Q)} = 0")
say("  no direction is lost, so distinct points stay distinct. That is the standard")
say("  reason clip space is 4-D rather than 3-D.")

# ---------------------------------------------------------------- 5
say()
say("=== Part 5: a kernel collision is fatal; ReLU has its own collapsed set ===")


def relu(v):
    return [max(0.0, t) for t in v]


W = [[1.0, -1.0, 0.5],
     [0.0, 2.0, -1.0]]
b = [0.5, -0.25]
say(f"W = {W}, bias b = {b}")


def net(v):
    """One affine layer, then ReLU. The bias makes the affine part, not the ReLU."""
    z = [sum(W[i][k] * v[k] for k in range(len(v))) + b[i] for i in range(len(W))]
    return z, relu(z)


u = [1.0, -2.0, 3.0]
kv = null_space(W)[0]
v_collide = [u[i] + kv[i] for i in range(3)]
say()
say("The affine part is linear, so it has a kernel. Take a probe point and one")
say("kernel step:")
say(f"  u         = {u}")
say(f"  ker basis = {[round(t, 4) for t in kv]}")
say()
say("A kernel collision is FATAL, and no later layer can undo it:")
say(f"  v = u + ker = {v_collide}")
say(f"  W u + b = {net(u)[0]}")
say(f"  W v + b = {net(v_collide)[0]}")
say(f"  equal: {net(u)[0] == net(v_collide)[0]}, because W times a kernel vector is 0.")
say("  The two pre-activations are IDENTICAL, so relu cannot separate them either:")
say(f"  relu(W u + b) = {net(u)[1]}")
say(f"  relu(W v + b) = {net(v_collide)[1]}")
say("  Any function of an equal argument is equal, so once a linear layer collides")
say("  two inputs, nothing downstream can recover the difference.")
say()
say("The ReLU is not injective either, but for a completely different reason: it is")
say("the NEGATIVE orthant that collapses.")
for p, q in (([-1.0, -2.0], [-3.0, -7.0]), ([0.0, -0.5], [0.0, -9.0])):
    say(f"  relu{p} = {relu(p)}   relu{q} = {relu(q)}   equal: {relu(p) == relu(q)}")
say("  Every negative input maps to 0, so the whole negative orthant is one")
say("  indistinguishable set -- a kernel in the same practical sense.")
say()
say("So a network has no single kernel: each layer has its own set of")
say("indistinguishable inputs, and a stack of PURE linear maps has exactly the")
say("kernel of the single matrix they collapse to, of rank r. That is why the")
say("nonlinearity buys expressiveness, and why a layer of width w bottlenecks to")
say("r dimensions the moment you remove it.")
```

Output:

```
=== Part 1: the four spaces of a 3x4 design matrix ===
A (3x4: 3 observations, 4 features)  (3x4)
  |   1.000   2.000   3.000   4.000 |
  |   5.000   6.000   7.000   9.000 |
  |   2.000   3.000   4.000   5.000 |

rank r = 3, m = 3 rows, n = 4 columns
  row space     in R^4, dim 3   basis = nonzero RREF rows
      [1.0, 0.0, -1.0, 0.0]
      [0.0, 1.0, 2.0, 0.0]
      [0.0, 0.0, 0.0, 1.0]
  column space  in R^3, dim 3   basis = pivot columns [0, 1, 3] of the ORIGINAL A
      [1.0, 5.0, 2.0]
      [2.0, 6.0, 3.0]
      [4.0, 9.0, 5.0]
  kernel        in R^4, dim 1 = n - r = 4 - 3
      [1.0, -2.0, 1.0, -0.0]      A w = [0.0, 0.0, 0.0]

  r + (n - r) = 3 + 1 = 4 = n = 4   (rank-nullity)
  dim(row) = 3 = dim(col) = 3 = r = 3

The row space lives in R^4 (one entry per COLUMN, so a coefficient vector
for the model) and the column space in R^3 (one entry per ROW, so a
prediction). Different ambient spaces, same dimension: the row-rank-equals-
column-rank theorem of lesson 34, seen from the map side.

=== Part 2: a dataset with one genuinely redundant feature ===
5 observations x 5 features, built so col 2 = 10*col 0 + 20*col 1 exactly:
  [3.0, 0.9, 48.0, 10.0, 6.0]
  [5.0, 0.8, 66.0, 12.0, 7.0]
  [2.0, 0.6, 32.0, 8.0, 5.0]
  [4.0, 0.95, 59.0, 11.0, 6.5]
  [6.0, 0.85, 77.0, 13.0, 8.0]

rank = 4 of 5 columns, so dim(ker) = 5 - 4 = 1
  null vector [-10.0, -20.0, 1.0, 0.0, 0.0]
    A w = [0.0, 0.0, 0.0, 0.0, 0.0]
    nonzero entries at [(0, -10.0), (1, -20.0), (2, 1.0)]
    so the relation involves exactly those columns; every other
    coefficient is zero, and the redundancy is confined to them.

Column 2 is score, and col 2 - 10*col 0 - 20*col 1 = 0 row by row:
  48.0 - 10*3.0 - 20*0.9 = +0.000000
  66.0 - 10*5.0 - 20*0.8 = +0.000000
  32.0 - 10*2.0 - 20*0.6 = +0.000000
  59.0 - 10*4.0 - 20*0.95 = +0.000000
  77.0 - 10*6.0 - 20*0.85 = +0.000000

rank with 5 columns = 4
rank with 4 columns (score dropped) = 4
Same rank, so nothing inside the span was lost.

=== Part 3: ker(S o T) is a PREIMAGE, verified ===
T  (x,y) -> (x,x)  (2x2)
  |   1.000   0.000 |
  |   1.000   0.000 |
S  (u,v) -> (0,v)  (2x2)
  |   0.000   0.000 |
  |   0.000   1.000 |
S T  (2x2)
  |   0.000   0.000 |
  |   1.000   0.000 |

  ker(T)   = [[-0.0, 1.0]]
  ker(S)   = [[1.0, -0.0]]
  ker(S T) = [[-0.0, 1.0]]
  the SUM rule would give dim 1 + 1 = 2
  the truth is dim ker(S T) = 1

  Direct check of the preimage rule: ker(S o T) = T^-1(ker S) = ker T,
  because ker S = {(0,0)} and only the inputs T maps to 0 qualify.
    T[0.0, 1.0] = [0.0, 0.0]  in ker(S)? True   S(T w) = [0.0, 0.0]
    T[1.0, 1.0] = [1.0, 1.0]  in ker(S)? False   S(T w) = [0.0, 1.0]
    T[5.0, 0.0] = [5.0, 5.0]  in ker(S)? False   S(T w) = [0.0, 5.0]

  Both (0,1) and (0,0) are in ker(S T): T sends them to 0 and S kills 0.
  (1,1) is NOT: T(1,1) = (1,1) is not in ker(S), and S(1,1) = (0,1) != 0.

  The sum rule overcounts here and undercounts in general: S never touches
  the input, it acts on T's OUTPUT. What matters is which of T's outputs S
  kills, not which inputs S would have killed on its own.

=== Part 4: a projection has a kernel, which is fatal for rendering ===
P  (x,y,z) -> (x,y)  (2x3)
  |   1.000   0.000   0.000 |
  |   0.000   1.000   0.000 |
  rank 2, dim(ker) = 3 - 2 = 1
  ker(P) = [[-0.0, -0.0, 1.0]]

  point A = [1.0, 2.0, 5.0]  ->  P A = [1.0, 2.0]
  point B = [1.0, 2.0, 900.0]  ->  P B = [1.0, 2.0]
  same 2-D point from points 895 units apart in z
  B - A = [0.0, 0.0, 895.0]
  that is 895 * the kernel basis [-0.0, -0.0, 1.0]
  check: 895 * [-0.0, -0.0, 1.0] = [-0.0, -0.0, 895.0]

  Two DISTINCT 3-D points give the SAME 2-D point. That is the whole failure:
  the projection has a nontrivial kernel, so the renderer cannot tell them
  apart and the depth buffer stores z-fighting instead of resolving it.
  Adding a 4th homogeneous coordinate and keeping the divide until the end
  gives an invertible 4x4 matrix:
    rank of the 4x4 identity = 4, dim(ker) = 4 - 4 = 0
  no direction is lost, so distinct points stay distinct. That is the standard
  reason clip space is 4-D rather than 3-D.

=== Part 5: a kernel collision is fatal; ReLU has its own collapsed set ===
W = [[1.0, -1.0, 0.5], [0.0, 2.0, -1.0]], bias b = [0.5, -0.25]

The affine part is linear, so it has a kernel. Take a probe point and one
kernel step:
  u         = [1.0, -2.0, 3.0]
  ker basis = [-0.0, 0.5, 1.0]

A kernel collision is FATAL, and no later layer can undo it:
  v = u + ker = [1.0, -1.5, 4.0]
  W u + b = [5.0, -7.25]
  W v + b = [5.0, -7.25]
  equal: True, because W times a kernel vector is 0.
  The two pre-activations are IDENTICAL, so relu cannot separate them either:
  relu(W u + b) = [5.0, 0.0]
  relu(W v + b) = [5.0, 0.0]
  Any function of an equal argument is equal, so once a linear layer collides
  two inputs, nothing downstream can recover the difference.

The ReLU is not injective either, but for a completely different reason: it is
the NEGATIVE orthant that collapses.
  relu[-1.0, -2.0] = [0.0, 0.0]   relu[-3.0, -7.0] = [0.0, 0.0]   equal: True
  relu[0.0, -0.5] = [0.0, 0.0]   relu[0.0, -9.0] = [0.0, 0.0]   equal: True
  Every negative input maps to 0, so the whole negative orthant is one
  indistinguishable set -- a kernel in the same practical sense.

So a network has no single kernel: each layer has its own set of
indistinguishable inputs, and a stack of PURE linear maps has exactly the
kernel of the single matrix they collapse to, of rank r. That is why the
nonlinearity buys expressiveness, and why a layer of width w bottlenecks to
r dimensions the moment you remove it.
```

**Challenge.**

(a) The set of inputs the network sends to `0` is the preimage of `0` under
ReLU, which is

    Z = { v : W v + b ≤ 0 componentwise }

Start with the zero vector, as instructed. Is `0 ∈ Z`? No:

    W 0 + b = (0.5, -0.25)      first entry positive, so 0 ∉ Z
    net(0)  = (0.5, 0.0)        not the zero output

That single check is decisive, and it is the strongest form of the refutation
available: a kernel *always* contains `0`, because `0` is the one input whose
image is forced regardless of the map. `Z` does not contain it, so `Z` is not a
kernel and none of the machinery attached to kernels — dimension counting,
rank-nullity, the `V_kept ⊕ ker` decomposition — applies to it.

Setting `b = 0` repairs the zero test and loses the argument, which is worth
seeing. Now `Z₀ = {v : W v ≤ 0}` does contain `0`, but it is not closed under
negation: `(-1, 0, 0)` is in `Z₀` and `(1, 0, 0)` is not, since
`W(1, 0, 0) = (1, 0)`. Closure under all real scalars is the axiom that fails.
`Z₀` is a convex cone.

What the network has *instead* is one kernel per linear layer — here
`dim(ker W) = 3 - 2 = 1`, with basis `(0, 0.5, 1)` — and part (e) already
showed that a kernel step in that layer is fatal. The preimage rule from part (c)
does not chain across a ReLU, because ReLU is not linear and has no kernel in
that sense, so there is never a single set whose dimension you can count.

(b) The claim becomes correct exactly when there is **no nonlinearity anywhere**
in the stack. Then the whole network is a composition of linear maps,

    V(W v + b) + c = (V W) v + (V b + c),

and only the single matrix `V W` matters. For the swap `V` and the `W` above,
`V W = [[0, 2, -1], [1, -1, 0.5]]` has rank `2`, so the network does have a
genuine one-dimensional kernel of dimension `3 - 2 = 1`. That is Exercise 5(d)
wearing a network's clothes.

Worth noting that the claim is never about individual pairs. `p = (0, 0, 3)` and
`q = (0, 0, -1)` are separated by the linear stack *and* by the ReLU, because
`q - p = (0, 0, -4)` is not in `ker(V W)` — `V W` sends it to `(4, -2)`. The
claim is about whether a single kernel-like set exists, and across a ReLU none
does.

The set the ReLU itself collapses is the closed negative orthant

    C = { x : xᵢ ≤ 0 for all i }

which is the entire preimage of `0`. The zero vector **is** in `C`, so the
cheapest test comes back inconclusive — and that is already the difference from
a kernel, where `0` is the generator and every other member is a multiple of it.
The axiom that fails is closure under negative scaling: `(-1, 0, 0) ∈ C` but
`(1, 0, 0) ∉ C`. `C` *is* closed under addition (`(-1,0,0) + (0,-1,0) =
(-1,-1,0)` stays in it) and *is* convex, so it is a convex set. The difference
in one line: a kernel is symmetric about the origin and `C` is not.

(c) For `L` purely linear layers,

    dim(ker of the stack) = w₁ - min(w₁, …, w_L)

Purely linear layers compose into one matrix, and by Exercise 5(e) composing
with an invertible map preserves the kernel exactly, so the entire stack has the
kernel of whichever layer is narrowest. Widths `(5, 8, 4, 6)` give `1`;
`(5, 9, 7, 12)` give `0`; `(3, 3, 3)` give `0`. Depth, surplus width above the
bottleneck, and parameter count are all irrelevant to that one number, and no
amount of training changes it.

A nonlinearity is the only thing in the stack that widens it, because it breaks
the composition. `relu(W₂ W₁ x)` is not a function of `W₂ W₁ x` in any way that
factors into a single matrix, so there is no matrix left to take a kernel of.
Depth then multiplies *representations* rather than composing matrices, and the
rank ceiling of an individual layer stops being the rank ceiling of the network.

```python
TOL = 1e-9

W = [[1.0, -1.0, 0.5],
     [0.0, 2.0, -1.0]]
b = [0.5, -0.25]


def matvec(M, v):
    return [sum(M[i][k] * v[k] for k in range(len(v))) for i in range(len(M))]


def relu(v):
    return [max(0.0, t) for t in v]


def z_of(v):
    """The affine pre-activation, the part that is genuinely linear."""
    return [matvec(W, v)[i] + b[i] for i in range(2)]


def net(v):
    return relu(z_of(v))


def rref(A, tol=TOL):
    M = [list(row) for row in A]
    rows, cols = len(M), len(M[0])
    pivot_row, pivots = 0, []
    for col in range(cols):
        if pivot_row == rows:
            break
        best = max(range(pivot_row, rows), key=lambda r: abs(M[r][col]))
        if abs(M[best][col]) <= tol:
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


ZERO3 = [0.0, 0.0, 0.0]
ZERO2 = [0.0, 0.0]

print("=== (a) the network's zero-preimage is not a kernel ===")
print("net(v) = relu(W v + b), so net(v) = 0 exactly when W v + b <= 0")
print("componentwise. Call that set Z. Is 0 in Z?")
print(f"  W 0 + b = {z_of(ZERO3)}")
print(f"  every entry <= 0? {all(t <= TOL for t in z_of(ZERO3))}")
print(f"  net(0)  = {net(ZERO3)}   equal to 0? {net(ZERO3) == ZERO2}")
print()
print("  NO. The bias puts the origin outside Z, and a kernel must contain 0,")
print("  so Z cannot be a kernel. The affine part already broke the axiom that")
print("  makes a kernel a subspace.")
print()
print("Drop the bias and the zero test is no longer decisive, but negation still")
print("fails. With b = 0, Z0 = {v : W v <= 0}:")
v = [-1.0, 0.0, 0.0]
neg = [-v[i] for i in range(3)]
print(f"  v   = {v}   W v   = {matvec(W, v)}   in Z0? "
      f"{all(t <= TOL for t in matvec(W, v))}")
print(f"  -v  = {neg}   W(-v) = {matvec(W, neg)}   in Z0? "
      f"{all(t <= TOL for t in matvec(W, neg))}")
print("  Closed under negation? No. A subspace must be closed under every real")
print("  scalar, so Z0 is a convex cone, not a subspace.")
print()
print("What the network DOES have is one kernel per linear layer:")
print(f"  W (2x3): rank {rank(W)}, dim(ker) = {len(W[0])} - {rank(W)} = "
      f"{len(W[0]) - rank(W)}, basis {[[round(t, 6) for t in w] for w in null_space(W)]}")
print("  and the preimage rule ker(S o T) = T^-1(ker S) does NOT chain across a")
print("  ReLU, because ReLU is not linear and has no kernel in that sense.")
print("  Take v = (0, 0, 1) and v + (0, 0.5, 1) (a kernel step of W):")
kv = null_space(W)[0]
base = [0.0, 0.0, 1.0]
stepped = [base[i] + kv[i] for i in range(3)]
print(f"    v     = {str(base):<18}  W v + b = {z_of(base)}  relu = {net(base)}")
print(f"    v + k = {str(stepped):<18}  W v + b = {z_of(stepped)}  relu = {net(stepped)}")
print("  equal, as part (e) showed, so the affine layer's kernel is real. The")
print("  network's own zero-preimage is a different, non-subspace set.")

print()
print("=== (b) when the claim becomes true, and what ReLU collapses ===")
V = [[0.0, 1.0], [1.0, 0.0]]
c = [0.25, -0.5]
VW = [[sum(V[i][k] * W[k][j] for k in range(2)) for j in range(3)]
      for i in range(2)]
print("  A ReLU-free network V(W v + b) + c = (V W) v + (V b + c):")
print(f"    V W = {VW}   rank {rank(VW)}, so dim(ker) = {len(VW[0])} - "
      f"{rank(VW)} = {len(VW[0]) - rank(VW)}")
p = [0.0, 0.0, 3.0]
q = [0.0, 0.0, -1.0]
for name, x in (("p", p), ("q", q)):
    lin = [sum(V[i][k] * matvec(W, x)[k] for k in range(2)) + c[i] for i in range(2)]
    print(f"    linear stack: {name} -> {lin}    with relu: {net(x)}")
diff = [q[i] - p[i] for i in range(3)]
print(f"  q - p = {diff}, which is NOT in ker(V W): "
      f"{[round(t, 6) for t in matvec(VW, diff)]}")
print("  So even the linear stack separates p and q, and the ReLU separates them")
print("  too. The claim is not about individual pairs; it is about a single set")
print("  that behaves like a kernel, and no such set exists across a ReLU.")
print()
print("  The set the ReLU collapses is C = {x : relu(x) = 0} = {x_i <= 0}:")
for x in ((-1.0, 0.0, 0.0), (0.0, -1.0, 0.0), (-0.5, -0.5, 0.0), (0.0, 0.0, 0.0)):
    out = relu(list(x))
    print(f"    relu{list(x)} = {out}   in C? {out == ZERO3}")
print()
print("  Test 1, the zero vector: relu(0,0,0) = (0,0,0), and 0 IS in C.")
print("  Inconclusive, which is itself the difference from a kernel: there the")
print("  zero vector is the generator and everything else follows from it.")
print()
x = [-1.0, 0.0, 0.0]
y = [0.0, -1.0, 0.0]
s = [x[i] + y[i] for i in range(3)]
mid = [(x[i] + y[i]) / 2 for i in range(3)]
nx = [-x[i] for i in range(3)]
print("  Test 2, closure under NEGATIVE scaling, which settles it:")
print(f"    x    = {x} in C? {relu(x) == ZERO3}")
print(f"    -x   = {nx} in C? {relu(nx) == ZERO3}")
print("    Not closed under negation, so not a subspace. It IS closed under")
print(f"  addition (x + y = {s}, in C? {relu(s) == ZERO3}) and convex (midpoint")
print(f"  {mid}, in C? {relu(mid) == ZERO3}), so C is a convex set. The whole")
print("  difference in one line: a kernel is symmetric about the origin, C is not.")

print()
print("=== (c) a purely linear stack of given widths ===")
for widths in ([5, 8, 4, 6], [5, 9, 7, 12], [3, 3, 3]):
    n = widths[0]
    print(f"  widths {str(widths):<16} dim(ker of stack) = {n} - min(widths) = "
          f"{n - min(widths)}")
print("  Only the NARROWEST layer matters. Depth and parameter count are")
print("  irrelevant to it, and a nonlinearity is the only thing in the stack that")
print("  widens it, because it stops the layers from composing into one matrix.")
```

Output:

```
=== (a) the network's zero-preimage is not a kernel ===
net(v) = relu(W v + b), so net(v) = 0 exactly when W v + b <= 0
componentwise. Call that set Z. Is 0 in Z?
  W 0 + b = [0.5, -0.25]
  every entry <= 0? False
  net(0)  = [0.5, 0.0]   equal to 0? False

  NO. The bias puts the origin outside Z, and a kernel must contain 0,
  so Z cannot be a kernel. The affine part already broke the axiom that
  makes a kernel a subspace.

Drop the bias and the zero test is no longer decisive, but negation still
fails. With b = 0, Z0 = {v : W v <= 0}:
  v   = [-1.0, 0.0, 0.0]   W v   = [-1.0, 0.0]   in Z0? True
  -v  = [1.0, -0.0, -0.0]   W(-v) = [1.0, 0.0]   in Z0? False
  Closed under negation? No. A subspace must be closed under every real
  scalar, so Z0 is a convex cone, not a subspace.

What the network DOES have is one kernel per linear layer:
  W (2x3): rank 2, dim(ker) = 3 - 2 = 1, basis [[-0.0, 0.5, 1.0]]
  and the preimage rule ker(S o T) = T^-1(ker S) does NOT chain across a
  ReLU, because ReLU is not linear and has no kernel in that sense.
  Take v = (0, 0, 1) and v + (0, 0.5, 1) (a kernel step of W):
    v     = [0.0, 0.0, 1.0]     W v + b = [1.0, -1.25]  relu = [1.0, 0.0]
    v + k = [0.0, 0.5, 2.0]     W v + b = [1.0, -1.25]  relu = [1.0, 0.0]
  equal, as part (e) showed, so the affine layer's kernel is real. The
  network's own zero-preimage is a different, non-subspace set.

=== (b) when the claim becomes true, and what ReLU collapses ===
  A ReLU-free network V(W v + b) + c = (V W) v + (V b + c):
    V W = [[0.0, 2.0, -1.0], [1.0, -1.0, 0.5]]   rank 2, so dim(ker) = 3 - 2 = 1
    linear stack: p -> [-2.75, 1.0]    with relu: [2.0, 0.0]
    linear stack: q -> [1.25, -1.0]    with relu: [0.0, 0.75]
  q - p = [0.0, 0.0, -4.0], which is NOT in ker(V W): [4.0, -2.0]
  So even the linear stack separates p and q, and the ReLU separates them
  too. The claim is not about individual pairs; it is about a single set
  that behaves like a kernel, and no such set exists across a ReLU.

  The set the ReLU collapses is C = {x : relu(x) = 0} = {x_i <= 0}:
    relu[-1.0, 0.0, 0.0] = [0.0, 0.0, 0.0]   in C? True
    relu[0.0, -1.0, 0.0] = [0.0, 0.0, 0.0]   in C? True
    relu[-0.5, -0.5, 0.0] = [0.0, 0.0, 0.0]   in C? True
    relu[0.0, 0.0, 0.0] = [0.0, 0.0, 0.0]   in C? True

  Test 1, the zero vector: relu(0,0,0) = (0,0,0), and 0 IS in C.
  Inconclusive, which is itself the difference from a kernel: there the
  zero vector is the generator and everything else follows from it.

  Test 2, closure under NEGATIVE scaling, which settles it:
    x    = [-1.0, 0.0, 0.0] in C? True
    -x   = [1.0, -0.0, -0.0] in C? False
    Not closed under negation, so not a subspace. It IS closed under
  addition (x + y = [-1.0, -1.0, 0.0], in C? True) and convex (midpoint
  [-0.5, -0.5, 0.0], in C? True), so C is a convex set. The whole
  difference in one line: a kernel is symmetric about the origin, C is not.

=== (c) a purely linear stack of given widths ===
  widths [5, 8, 4, 6]     dim(ker of stack) = 5 - min(widths) = 1
  widths [5, 9, 7, 12]    dim(ker of stack) = 5 - min(widths) = 0
  widths [3, 3, 3]        dim(ker of stack) = 3 - min(widths) = 0
  Only the NARROWEST layer matters. Depth and parameter count are
  irrelevant to it, and a nonlinearity is the only thing in the stack that
  widens it, because it stops the layers from composing into one matrix.
```

</details>

## Summary

- A map is **linear** when `T(u+v) = T(u) + T(v)` and `T(cu) = cT(u)`. Both imply
  `T(0) = 0`, so any map with an offset is affine, not linear.
- Linear maps from `ℝⁿ` to `ℝ^m` are in bijection with `m × n` matrices. The matrix
  is determined by its values on the standard basis, since
  `T(x) = Σ x_j T(e_j)`.
- The **kernel** is the set of inputs that vanish; the **image** is every
  reachable output. Both are subspaces.
- **Rank-nullity**: `dim(ker T) + dim(im T) = dim V`. The domain splits as
  `V = V_kept ⊕ ker T`, and the map is invertible exactly when the kernel is
  trivial.
- Composition respects both: `ker(S∘T)` is the *preimage* of `ker S`, and
  `im(S∘T) = S(im T)`. This is the structural fact behind the chain rule.
- For a square map, trivial kernel ⟺ full rank ⟺ `det ≠ 0` ⟺ invertible. Four
  phrasings of one fact.
- `y = Wx + b` is affine, not linear. The bias moves the origin, and linear maps
  must fix it.
- A nonzero kernel means distinct inputs collide. In graphics that is z-fighting
  in the wrong dimension; in a linear model it is unidentified coefficients.

## Next

[36 — Eigenvalues and Eigenvectors](36_eigenvalues_and_eigenvectors.md) asks what
a linear map does to its *own* preferred directions: the vectors that come out
parallel to themselves, merely rescaled. Those directions turn out to determine
everything about how the map behaves — whether it expands, contracts, or rotates —
and they are what makes a matrix decomposable into a form that is easy to read.
