# 31 — Matrices and Matrix Algebra

**Part**: part03_linear_algebra · **Prerequisites**: 30 · **Time**: 40 min

---

## In Plain Words

A matrix is a grid of numbers. In code it is a list of lists, and that is the
whole data structure. What makes grids interesting is that there is a
particularly useful way to combine two of them, and that way has two
interpretations that turn out to be the same thing.

The first interpretation: a grid of coefficients in a set of equations, one
equation per row and one unknown per column. The second interpretation: a
machine that takes a list of numbers and returns a different list of numbers,
where the columns of the grid tell you what the machine does to each individual
coordinate. Multiplication is the same operation under both readings: chaining
the machines together.

Two facts drive everything else. Matrix multiplication is not commutative, so
the order of a product matters and you cannot rearrange one. But it is
associative, so you can reparenthesise freely, which is why a long chain of
transformations collapses into a single matrix.

## Why Computer Science Cares

- **Every neural network is a chain of matrix multiplies.** A dense layer is
  `y = W x + b`. Composition across layers means one big `W`, which is how
  inference engines optimise away per-layer overhead. See
  [lesson 120](../part10_tensors_numerical/120_tensors_and_broadcasting.md).
- **Graphics.** The 4×4 transformation matrix, its transpose, and its inverse
  are the core of every vertex transform in
  [lesson 91](../part07_geometry_graphics/91_transformations_graphics.md). Order
  matters because the matrices do not commute.
- **PageRank** is one matrix `P` with `Pᵀ` in the update; the two being different
  is the whole subtlety. [Lesson 41](../part03_linear_algebra/41_matrices_graphs_and_applications.md).
- **Databases and state.** A transition matrix over states, and matrix
  exponentiation for "how many paths of length k", shows up in scheduling,
  queueing, and Markov chain work.
- **Linear time tricks.** `tr(AB) = tr(BA)` for constant-time checks,
  `(AB)ᵀ = BᵀAᵀ` for reversing a pipeline, and repeated squaring for `A^n` in
  `O(log n)` multiplies rather than `n`.
- **Interview questions.** "What is the complexity of matrix multiplication?",
  "why does `X * Y` differ from `X @ Y` in numpy?", and "what does a sparse
  matrix buy me?" are all answered from this lesson.

## The Formal Version

Symbols follow [SYMBOLS.md](../SYMBOLS.md).

**Definition.** An `m × n` matrix `A` over a field `F` is a function
`{1, …, m} × {1, …, n} → F`, written `A = (a_ij)` with `m` rows and `n` columns.

**Definition.** The **transpose** `Aᵀ` of an `m × n` matrix is the `n × m` matrix
`(Aᵀ)_ji = a_ij`. The **conjugate transpose** `A*` satisfies `(A*)_ji = conj(a_ij)`;
over `ℝ` it is just `Aᵀ`.

**Definition.** For an `m × k` matrix `A` and a `k × n` matrix `B`, the product
`AB` is the `m × n` matrix

    (AB)_ij = Σ_{k=1..k} a_ik · b_kj

**Explanation.** The index `k` runs along a row of `A` and down a column of `B`,
so each entry of `AB` is a dot product of a row of `A` with a column of `B`.
The condition is that the *inner* dimensions agree: you multiply an `m × k` by a
`k × n` and get `m × n`. Anything else is undefined, not merely hard.

**Definition.** `I_n` is the `n × n` **identity matrix**, with `1` on the diagonal
(`(I_n)_ii = 1`) and `0` elsewhere. `A⁰ = I_n` for any `n × n` matrix `A`, and
`Aᵏ` is the product of `k` copies of `A`.

**Theorem.** Matrix multiplication is associative: `(AB)C = A(BC)` whenever the
products are defined.

**Explanation.** Both sides expand to a double sum
`Σ_j Σ_k a_ij b_kj c_kl` over the same set of triples, in the same order once
you fix `j` and `l`. Compare [the dot product derivation](../part02_discrete_combinatorics/28_counting_strategies.md);
the point is that a triple sum over a product of three sets is unambiguous.

**Theorem.** Matrix multiplication is not commutative in general: there exist
`A`, `B` with `AB ≠ BA`.

**Explanation.** `(AB)_ij = Σ_k a_ik b_kj` and `(BA)_ij = Σ_k b_ik a_kj` are
different sums over different pairings. Concretely, `A = [[0, 1], [1, 0]]`
swaps coordinates and `B = [[1, 1], [0, 1]]` adds the first coordinate to the
second. `AB` and `BA` give different results on `[1, 1]`.

**Theorem (Transpose rules).** For compatible `A`, `B`:

- `(AB)ᵀ = BᵀAᵀ`
- `(Aᵀ)ᵀ = A`
- `(A + B)ᵀ = Aᵀ + Bᵀ`

**Explanation.** Transposing reverses the order because `(AB)ᵀ_ij = (AB)_ji =
Σ_k a_jk b_ki = Σ_k b_ki a_jk = (BᵀAᵀ)_ij`.

**Definition.** The **trace** of a square matrix is `tr(A) = Σ_i a_ii`.

**Theorem.** `tr(AB) = tr(BA)` for square `A`, `B`, and `tr(A) = tr(Aᵀ)`.

**Explanation.** `tr(AB) = Σ_i Σ_k a_ik b_ki = Σ_k Σ_i a_ik b_ki = tr(BA)`. Note
`AB` and `BA` may be different matrices, but their traces agree.

**Definition.** `A` is **diagonal** if `a_ij = 0` whenever `i ≠ j`. It is
**sparse** if most entries are zero. Its **bandwidth** is the largest `|i - j|`
over nonzero entries.

**Theorem.** Diagonal matrices multiply in `O(n)` per matvec and their inverses
are found entrywise. If `A` and `B` have bandwidths `p` and `q` then `AB` has
bandwidth at most `p + q`.

**Explanation.** Row `i` of a diagonal matrix has one nonzero, so `Av` is `n`
multiplications. A product's entry `(AB)_ij` sums over `k` between `i - q` and
`i + p`, so nonzeros can only appear when `|i - j| ≤ p + q`.

**Definition.** A **block matrix** is a matrix whose entries are themselves
matrices, arranged in a grid. A **block-diagonal** matrix has square blocks on
the diagonal and zero blocks elsewhere.

**Theorem.** Block multiplication proceeds block by block. If `A` is partitioned
into `A_ij` and `B` into `B_jk` with matching block sizes, then `(AB)_ik =
Σ_j A_ij B_jk`.

**Explanation.** Just expand the definition; a zero block times anything is zero,
so block-diagonal matrices multiply block-diagonally.

**Theorem (Complexity).** Dense `m × k` by `k × n` multiplication costs
`Θ(mkn)` multiply-adds.

**Explanation.** There are `mn` entries and each sums `k` products.

## Worked Example

Two matrices, computed by hand:

    A = | 1  2  3 |     (2 × 3)
        | 4  5  6 |

    B = |  7   8 |      (3 × 2)
        |  9  10 |
        | 11  12 |

**Step 1: check the shapes.** `A` is `2 × 3` and `B` is `3 × 2`. The inner
dimensions agree (3 and 3), so `AB` exists and is `2 × 2`. `BA` also exists
(`3 × 3`), but that is a different product.

**Step 2: entry (0, 0).** Row 0 of `A` is `[1, 2, 3]`. Column 0 of `B` is
`[7, 9, 11]`.

    (AB)_00 = 1·7 + 2·9 + 3·11 = 7 + 18 + 33 = 58

**Step 3: entry (0, 1).** Row 0 of `A`, column 1 of `B` is `[8, 10, 12]`.

    (AB)_01 = 1·8 + 2·10 + 3·12 = 8 + 20 + 36 = 64

**Step 4: entry (1, 0).** Row 1 of `A` is `[4, 5, 6]`, column 0 of `B`.

    (AB)_10 = 4·7 + 5·9 + 6·11 = 28 + 45 + 66 = 139

**Step 5: entry (1, 1).**

    (AB)_11 = 4·8 + 5·10 + 6·12 = 32 + 50 + 72 = 154

So

    AB = |  58  64 |
         | 139 154 |

**Step 6: the composition reading.** To compose, `B` must live on the same space
`A` acts on, so replace the `3 × 2` matrix with a `3 × 3` one that swaps the
first two coordinates:

    B = | 0 1 0 |
        | 1 0 0 |
        | 0 0 1 |

    v = [7, 11, 2]

Apply `B` first, then `A`:

    B v    = [0·7 + 1·11 + 0·2,  1·7 + 0·11 + 0·2,  0·7 + 0·11 + 1·2]
           = [11, 7, 2]

    A(B v) = [1·11 + 2·7 + 3·2,  4·11 + 5·7 + 6·2]
           = [11 + 14 + 6,  44 + 35 + 12]
           = [31, 91]

Now the same thing as a single product. The `2 × 2` matrix from Steps 2 to 5 no
longer applies, because `B` is a different shape, so recompute `AB`:

    (AB)_00 = 1·0 + 2·1 + 3·0 = 2
    (AB)_01 = 1·1 + 2·0 + 3·0 = 1
    (AB)_02 = 1·0 + 2·0 + 3·1 = 3
    (AB)_10 = 4·0 + 5·1 + 6·0 = 5
    (AB)_11 = 4·1 + 5·0 + 6·0 = 4
    (AB)_12 = 4·0 + 5·0 + 6·1 = 6

    A B = | 2  1  3 |
         | 5  4  6 |

    (AB) v = [2·7 + 1·11 + 3·2,  5·7 + 4·11 + 6·2]
           = [14 + 11 + 6,  35 + 44 + 12]
           = [31, 91]

    A(B v) = (AB) v = [31, 91]  ✓

That is the whole content of the "composition" reading: multiplying two matrices
first and then applying the product gives the same answer as applying them one
after the other. It holds because `(AB)_ij = Σ_k a_ik b_kj` distributes
perfectly, which is the whole reason the formula has a sum in it.

**Step 7: associativity.** Let `F = [[1, 1], [1, 0]]`, `G = [[1, 0], [1, 0]]`,
`H = [[0, 1], [1, 0]]`.

Group left first:

    F G = | 1·1 + 1·1,  1·0 + 1·0 |  =  | 2  0 |
          | 1·1 + 0·1,  1·0 + 0·0 |     | 1  0 |

    (FG) H = | 2·0 + 0·1,  2·1 + 0·0 |  =  | 0  2 |
             | 1·0 + 0·1,  1·1 + 0·0 |     | 0  1 |

Group right first:

    G H = | 1·0 + 0·1,  1·1 + 0·0 |  =  | 0  1 |
          | 1·0 + 0·1,  1·1 + 0·0 |     | 0  1 |

    F(GH) = | 1·0 + 1·0,  1·1 + 1·1 |  =  | 0  2 |
            | 1·0 + 0·0,  1·1 + 0·1 |     | 0  1 |

Both groupings give `[[0, 2], [0, 1]]`. Associativity holds, as it must, and the
parenthesisation is free while the order is not — compare Step 1, where `AB` and
`BA` were even different shapes.

**Step 8: the shape check earns its keep.** `A` is `2 × 3` and `B` is `3 × 2`, so
`AB` is `2 × 2`. Trying to multiply `A` by `A` fails, because `2 ≠ 3`:

    cannot multiply 2x3 by 2x3

The `matmul` helper in this lesson raises on exactly this, with both shapes in
the message, rather than letting a stray `IndexError` surface three frames
later.

## Runnable Code

### Matrix helpers and multiplication

The helpers are defined once here and reused by the rest of the lessons in this
part. Later lessons either repeat them or point back to this section.

```python
# ---------------------------------------------------------------- helpers
# A matrix is a list of rows, and a row is a list of numbers. A vector is a
# list of numbers, so a matrix is a list of vectors. That is the whole data
# model; everything below is arithmetic on nested lists.

def shape(M):
    """(rows, columns) of a rectangular matrix."""
    return len(M), len(M[0])


def identity(n):
    """The n-by-n identity: 1 on the diagonal, 0 everywhere else."""
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def zeros(rows, cols):
    return [[0.0] * cols for _ in range(rows)]


def transpose(M):
    """Flip rows and columns: (A^T)[j][i] = A[i][j]."""
    rows, cols = shape(M)
    return [[M[i][j] for i in range(rows)] for j in range(cols)]


def matmul(A, B):
    """Multiply A by B.

    (A B)[i][j] = sum over k of A[i][k] * B[k][j]. The index k runs down a row
    of A and across a column of B, so the entry is a dot product. This is the
    only definition; everything else about matrix multiplication follows from it.
    """
    rows_a, cols_a = shape(A)
    rows_b, cols_b = shape(B)
    if cols_a != rows_b:
        raise ValueError(f"cannot multiply {rows_a}x{cols_a} by {rows_b}x{cols_b}")
    C = zeros(rows_a, cols_b)
    for i in range(rows_a):
        for j in range(cols_b):
            total = 0.0
            for k in range(cols_a):
                total += A[i][k] * B[k][j]
            C[i][j] = total
    return C


def matvec(M, v):
    """Multiply a matrix by a vector: one dot product per row."""
    rows, cols = shape(M)
    if len(v) != cols:
        raise ValueError(f"vector has {len(v)} entries, matrix has {cols} columns")
    return [sum(M[i][k] * v[k] for k in range(cols)) for i in range(rows)]


def print_matrix(label, M):
    rows, cols = shape(M)
    print(f"{label}  ({rows}x{cols})")
    for row in M:
        print("  | " + " ".join(f"{x:8.3f}" for x in row) + " |")


# ---------------------------------------------------------------- the example
# A 2x3 matrix times a 3x2 matrix gives a 2x2 matrix.
A = [[1.0, 2.0, 3.0],
     [4.0, 5.0, 6.0]]

B = [[7.0, 8.0],
     [9.0, 10.0],
     [11.0, 12.0]]

print("=== Row by column: every entry is one dot product ===")
print_matrix("A", A)
print_matrix("B", B)

# Entry (0,0) of A*B = row 0 of A dotted with column 0 of B.
col0_of_B = [B[0][0], B[1][0], B[2][0]]
print(f"row 0 of A        = {A[0]}")
print(f"column 0 of B     = {col0_of_B}")
print(f"their dot product = {sum(A[0][k] * col0_of_B[k] for k in range(3))}")
print("by hand: 1*7 + 2*9 + 3*11 = 7 + 18 + 33 = 58")

C = matmul(A, B)
print()
print_matrix("A B", C)
print(f"all four entries by hand:")
print("  (0,0) = 1*7  + 2*9  + 3*11 =", 1 * 7 + 2 * 9 + 3 * 11)
print("  (0,1) = 1*8  + 2*10 + 3*12 =", 1 * 8 + 2 * 10 + 3 * 12)
print("  (1,0) = 4*7  + 5*9  + 6*11 =", 4 * 7 + 5 * 9 + 6 * 11)
print("  (1,1) = 4*8  + 5*10 + 6*12 =", 4 * 8 + 5 * 10 + 6 * 12)

print()
print("=== Multiplication order changes the answer ===")
# AB is 2x2 and BA is 3x3. They are not even the same shape, let alone equal.
print(f"shape of A B = {shape(matmul(A, B))}")
print(f"shape of B A = {shape(matmul(B, A))}")
BA = matmul(B, A)
print_matrix("B A", BA)
print("The (0,0) entry of A B is", matmul(A, B)[0][0],
      "while the (0,0) entry of B A is", BA[0][0])
print("Matrices do not commute. Nearly every surprise in linear algebra is this,")
print("and it is why A^-1 A = I but A A^-1 needs its own proof.")

print()
print("=== Associativity does hold: (AB)C = A(BC) ===")
F = [[1.0, 2.0], [0.0, 1.0]]                 # 2x2, so both groupings are legal
left = matmul(matmul(A, B), F)               # (2x2)(2x2) = 2x2
right = matmul(A, matmul(B, F))              # (2x3)(3x2) = 2x2
print_matrix("(AB)F", left)
print_matrix("A(BF)", right)
print(f"equal: {left == right}")
print("Parentheses do not matter, but order does. That is exactly what you need")
print("to know to reason about a chain of transformations applied to a vector.")

print()
print("=== Matrix times vector: one dot product per row ===")
v = [1.0, 0.0, 2.0]
print(f"v = {v}")
print(f"A v = {matvec(A, v)}")
print("by hand: row0 = 1*1 + 2*0 + 3*2 = 1 + 0 + 6 = 7")
print(f"       row1 = 4*1 + 5*0 + 6*2 = 4 + 0 + 12 = 16")

print()
print("=== The identity matrix does nothing ===")
I3 = identity(3)
print_matrix("I3", I3)
S = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 10.0]]
print_matrix("S", S)
print_matrix("S I3", matmul(S, I3))
print_matrix("I3 S", matmul(I3, S))
print("Both products equal S. This is why we call I the identity: it is the")
print("multiplicative equivalent of adding zero.")
print(f"I3 v = {matvec(I3, v)} (unchanged)")
```

### Transpose, trace, and powers

```python
# ---------------------------------------------------------------- helpers
# The matrix helpers are defined in lesson 31, the previous lesson. They are
# repeated here so this block runs on its own.
def shape(M):
    return len(M), len(M[0])


def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def zeros(rows, cols):
    return [[0.0] * cols for _ in range(rows)]


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
    if len(v) != cols:
        raise ValueError(f"vector has {len(v)} entries, matrix has {cols} columns")
    return [sum(M[i][k] * v[k] for k in range(cols)) for i in range(rows)]


def trace(M):
    """Sum of the diagonal entries."""
    return sum(M[i][i] for i in range(shape(M)[0]))


def print_matrix(label, M):
    rows, cols = shape(M)
    print(f"{label}  ({rows}x{cols})")
    for row in M:
        print("  | " + " ".join(f"{x:7.2f}" for x in row) + " |")


# ---------------------------------------------------------------- transpose
M = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]

print("=== Transpose flips rows and columns ===")
print_matrix("M", M)
Mt = transpose(M)
print_matrix("M^T", Mt)
print(f"shape of M = {shape(M)}, shape of M^T = {shape(Mt)}")
print("Transposing twice gets you back:", transpose(Mt) == M)

# (A B)^T = B^T A^T. The transpose reverses the order.
A = [[1.0, 2.0], [3.0, 4.0]]
B = [[5.0, 6.0], [7.0, 8.0]]
lhs = transpose(matmul(A, B))
rhs = matmul(transpose(B), transpose(A))
print()
print(f"(A B)^T =\n{lhs}")
print(f"B^T A^T =\n{rhs}")
print(f"equal: {lhs == rhs}")

# Trace: diagonal sum. It is invariant under transpose and under swapping the
# two factors of a product: tr(AB) = tr(BA).
print()
print("=== Trace ===")
print(f"trace(M) = {trace(M)}")
print(f"trace(AB) = {trace(matmul(A, B))}, trace(BA) = {trace(matmul(B, A))}")
print("They agree, even though AB and BA are different matrices.")

# -------------------------------------------------------------- powers
def power(A, n):
    """A to the n-th power by repeated multiplication. n >= 0."""
    result = identity(shape(A)[0])
    for _ in range(n):
        result = matmul(result, A)
    return result


print()
print("=== Powers: repeated application ===")
P = [[1.0, 1.0], [1.0, 0.0]]   # the Fibonacci matrix
print_matrix("P", P)
v0 = [1.0, 0.0]                # start with [F(2), F(1)]
print(f"P^0 v0 = {matvec(identity(2), v0)}")
for n in range(1, 8):
    Pn = power(P, n)
    print(f"P^{n} v0 = {matvec(Pn, v0)}")
print("The numbers are Fibonacci numbers. P^8 would be big; the entries of P^n")
print("are the standard identity F(n) = (P^n)[0][1], which is a fast way to")
print("compute Fibonacci numbers in exact integer arithmetic.")

# A cheaper power by squaring: O(log n) matrix multiplications instead of n.
def power_fast(A, n):
    """A^n by repeated squaring. Far fewer multiplications for large n."""
    result = identity(shape(A)[0])
    base = [list(row) for row in A]
    while n > 0:
        if n % 2 == 1:
            result = matmul(result, base)
        base = matmul(base, base)
        n //= 2
    return result


print()
print("=== Repeated squaring gives the same answer, faster ===")
for n in (1, 5, 12):
    slow = power(P, n)
    fast = power_fast(P, n)
    print(f"P^{n}: naive matches fast = {slow == fast}")
print(f"P^12 =\n{power_fast(P, 12)}")
print("P^12[0][1] = 144 = F(12), confirming the Fibonacci identity.")
```

### Structured matrices: diagonal, sparse, banded, block

```python
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


def diagonal_scale(vals, n):
    """Build an n-by-n diagonal matrix from a list of n values."""
    D = zeros(n, n)
    for i, v in enumerate(vals):
        D[i][i] = v
    return D


def sparsity(M, tol=1e-12):
    """Fraction of entries that are zero."""
    rows, cols = shape(M)
    nonzero = sum(1 for i in range(rows) for j in range(cols) if abs(M[i][j]) > tol)
    return 1.0 - nonzero / (rows * cols)


def bandwidth(M, tol=1e-12):
    """Largest horizontal distance of a nonzero from the main diagonal."""
    rows, cols = shape(M)
    best = 0
    for i in range(rows):
        for j in range(cols):
            if abs(M[i][j]) > tol:
                best = max(best, abs(i - j))
    return best


def print_matrix(label, M, width=7):
    rows, cols = shape(M)
    print(f"{label}  ({rows}x{cols})")
    for row in M:
        print("  | " + " ".join(f"{x:{width}.2f}" for x in row) + " |")


# ---------------------------------------------------------------- diagonal
print("=== Diagonal matrices scale each coordinate and nothing else ===")
# A diagonal matrix has zeros everywhere except on the main diagonal, so
# multiplying by it just scales entry i of the vector by the i-th diagonal value.
v = [1.0, 2.0, 3.0]
D = diagonal_scale([10.0, 0.5, 2.0], 3)
print_matrix("D", D)
print(f"v = {v}")
print(f"D v = {[D[i][i] * v[i] for i in range(3)]}")
print("Row i of D has a single nonzero, so the dot product is just that value")
print("times v[i]. Cost is O(n) instead of O(n^2).")

print()
print("=== Diagonal matrices are cheap and invert easily ===")
D2 = diagonal_scale([4.0, 5.0, 2.0], 3)
print(f"D2 = {D2}")
print("D2 times its reciprocal diagonal matrix is the identity:")
inv_vals = [1.0 / D2[i][i] for i in range(3)]
D2_inv = diagonal_scale(inv_vals, 3)
print_matrix("D2 @ D2_inv", matmul(D2, D2_inv))
print("No row reduction needed. This is why normalising each feature by its")
print("standard deviation, which is a diagonal matrix, is so cheap.")

# ---------------------------------------------------------------- sparse
print()
print("=== Sparse matrices: mostly zeros ===")
n = 8
tridiag = [[1.0 if abs(i - j) == 1 else (2.0 if i == j else 0.0) for j in range(n)]
           for i in range(n)]
print_matrix("tridiagonal 8x8", tridiag, width=4)
print(f"sparsity = {sparsity(tridiag):.4f} (fraction of zeros)")
print(f"bandwidth = {bandwidth(tridiag)}")
print("Storage needed if we only store nonzeros: "
      f"{sum(1 for i in range(n) for j in range(n) if tridiag[i][j] != 0)} numbers "
      f"instead of {n * n}.")

dense = [[1.0 + i * n + j for j in range(n)] for i in range(n)]
print(f"a dense 8x8 has sparsity {sparsity(dense):.4f}")

print()
print("=== A sparse matrix can be stored as its nonzero positions ===")
entries = [(i, j, tridiag[i][j])
           for i in range(n) for j in range(n) if tridiag[i][j] != 0.0]
print(f"stored as (row, col, value): {entries}")
print(f"{len(entries)} stored values instead of {n * n}. For n = 10000 the")
print("difference between 3n and n^2 stored values is the difference between")
print("a few tens of thousands and a hundred million.")

# The cost of multiplying two banded matrices grows with the band, not the size.
print()
print("=== Multiplying two tridiagonal matrices stays banded ===")
# Two tridiagonal matrices multiply to something pentadiagonal (bandwidth 2).
n = 6
T = [[2.0 if i == j else (1.0 if abs(i - j) == 1 else 0.0) for j in range(n)]
     for i in range(n)]
TT = matmul(T, T)
print(f"bandwidth of T    = {bandwidth(T)}")
print(f"bandwidth of T*T  = {bandwidth(TT)}")
print(f"expected: 2 * {bandwidth(T)} = {2 * bandwidth(T)}")
print("Generally the bandwidths add, so banded times banded stays banded.")

# ---------------------------------------------------------------- block
print()
print("=== Block matrices: a grid of submatrices ===")
# Cut a 4x4 matrix into four 2x2 blocks and multiply block by block.
B = [[1.0, 2.0, 0.0, 0.0],
     [0.0, 1.0, 0.0, 0.0],
     [0.0, 0.0, 1.0, 3.0],
     [0.0, 0.0, 0.0, 1.0]]
print_matrix("B (already block diagonal)", B)
print("Read it as [[B11, 0], [0, B22]] with B11 = [[1,2],[0,1]] and")
print("B22 = [[1,3],[0,1]]. Multiplying block by block means")
print("  top-left  = B11 B11")
print("  top-right = B11 * 0 = 0")
print("  bottom-left = 0 * B22 = 0")
print("  bottom-right = B22 B22")
B11 = [[1.0, 2.0], [0.0, 1.0]]
B22 = [[1.0, 3.0], [0.0, 1.0]]
print_matrix("expected top-left block B11*B11", matmul(B11, B11))
print_matrix("expected bottom-right B22*B22", matmul(B22, B22))
print_matrix("full product B*B", matmul(B, B))
print("The zeros stay zeros, so block structure survives multiplication.")
print("That is the whole basis of sparse Cholesky factorisation in lesson 113")
print("(../part09_number_theory_crypto/113_error_correcting_codes.md) and of")
print("multigrid solvers.")

# ---------------------------------------------------------------- cost
print()
print("=== How much work does structure save? ===")
# Counting operations rather than timing: the counts are exact and machine
# independent, which is what belongs in a lesson.


def count_dense_mults(A, B):
    """Multiplications a naive triple loop performs, zeros included."""
    rows_a, cols_a = shape(A)
    _, cols_b = shape(B)
    return rows_a * cols_b * cols_a


def count_real_mults(A, B, tol=1e-12):
    """Multiplications actually needed, skipping zeros."""
    rows_a, cols_a = shape(A)
    rows_b, cols_b = shape(B)
    total = 0
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                if abs(A[i][k]) > tol and abs(B[k][j]) > tol:
                    total += 1
    return total


n = 100
Dbig = diagonal_scale([1.5] * n, n)
Rbig = [[float((i * 7 + j * 3) % 11) for j in range(n)] for i in range(n)]

naive = count_dense_mults(Dbig, Rbig)
useful = count_real_mults(Dbig, Rbig)
print(f"{n}x{n} by {n}x{n}: the naive loop does {naive} multiplications")
print(f"but only {useful} of them have two nonzero factors")
print(f"ratio {naive // useful}")
print("That gap is the entire reason sparse and structured formats exist.")

# Cost of a dense n-by-n matvec: n^2 multiply-adds. A diagonal matvec: n.
print()
print("matrix times vector, 1000 dimensions:")
print(f"  dense matvec  ~ {1000 * 1000} multiply-adds")
print(f"  diagonal      ~ {1000} multiply-adds")
print("Neural network inference is a long chain of these multiplies, so the")
print("shape of the weight matrix decides the cost.")
```

### Two readings of the same matrix

```python
# Two readings of the same formula. In lesson 30 a matrix was a table. Here it
# is a machine: multiply a vector on the left and it comes out changed.

def shape(M):
    return len(M), len(M[0])


def zeros(rows, cols):
    return [[0.0] * cols for _ in range(rows)]


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


def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def print_matrix(label, M, width=7):
    rows, cols = shape(M)
    print(f"{label}  ({rows}x{cols})")
    for row in M:
        print("  | " + " ".join(f"{x:{width}.2f}" for x in row) + " |")


# ------------------------------------------------------------ reading one
# The same matrix as a table of coefficients (left) and as a machine (right).
A = [[1.0, 2.0, 0.0],
     [0.0, 1.0, 1.0],
     [1.0, 0.0, 1.0]]

print("=== Reading 1: a table of coefficients in a linear system ===")
# A x = b means: one equation per row, one unknown per column.
x = [3.0, 4.0, 5.0]
b = matvec(A, x)
print_matrix("A (coefficients)", A)
print(f"unknowns x = {x}")
print("Rows give the equations:")
for i in range(shape(A)[0]):
    terms = " + ".join(f"{A[i][j]}*x{j}" for j in range(shape(A)[1]))
    print(f"  {terms} = {b[i]}")
print(f"so A x = b = {b}")
print("Read as a table, A is a list of equations.")

print()
print("=== Reading 2: a machine that transforms a vector ===")
# Columns are the images of the basis vectors. Column 0 is what the machine
# does to [1,0,0], column 1 what it does to [0,1,0], and so on.
print("What the machine does to each basis vector:")
for j in range(shape(A)[1]):
    e_j = [1.0 if i == j else 0.0 for i in range(shape(A)[0])]
    print(f"  A e_{j} = {matvec(A, e_j)}   (column {j} of A)")

print()
print("Any vector is a combination of basis vectors, and the machine respects")
print("scaling and adding, so A(3e0 + 4e1 + 5e2) = 3(A e0) + 4(A e1) + 5(A e2):")
by_columns = [sum(x[j] * A[i][j] for j in range(3)) for i in range(3)]
print(f"  3*(col 0) + 4*(col 1) + 5*(col 2) = {by_columns}")
print(f"  which equals A x              = {b}")
print("Read as a machine, A is a linear transformation. The two readings agree")
print("because both are the same array of numbers with the same rule.")

# ------------------------------------------------------------ composition
print()
print("=== Multiplication is composition ===")
# Doing B first then A gives A(B v). That is exactly (A B) v.
B = [[0.0, 1.0, 0.0],      # swaps the first two coordinates, leaves the third
     [1.0, 0.0, 0.0],
     [0.0, 0.0, 1.0]]
v = [7.0, 11.0, 2.0]
print(f"v        = {v}")
print(f"B v      = {matvec(B, v)}   (first two swapped)")
print(f"A(B v)   = {matvec(A, matvec(B, v))}   (swap, then A)")
print(f"(A B) v  = {matvec(matmul(A, B), v)}")
print(f"equal: {matvec(A, matvec(B, v)) == matvec(matmul(A, B), v)}")
print("So AB means 'B first, then A'. This is the reading that makes matrix")
print("powers obvious: A^n is the machine applied n times.")

# ------------------------------------------------------------ powers again
print()
print("=== A^n is n applications of A ===")


def power(A, n):
    result = identity(shape(A)[0])
    for _ in range(n):
        result = matmul(result, A)
    return result


S = [[1.0, 1.0], [0.0, 1.0]]     # shear: add y to x
w = [2.0, 3.0]
print(f"S = {S}   (the shear that maps (x, y) to (x + y, y))")
print(f"w = {w}")
for n in range(0, 5):
    wn = matvec(power(S, n), w)
    print(f"  S^{n} w = {wn}")
print("One application adds 3 to the first coordinate. Two add 6, three add 9.")
print("Ten would add 30, so the growth is exactly linear in n: the shear has")
print("eigenvalue 1, which is the subject of lesson 36.")

# ------------------------------------------------------------ chained map
print()
print("=== A chain of layers is one big matrix ===")
# The hidden state of a tiny "layer" is a 3-vector; the output is a 2-vector.
W1 = [[1.0, -1.0, 0.5],    # 2x3: hidden to output
      [0.0, 2.0, -1.0]]
W2 = [[1.0, 0.0],          # 3x2: input to hidden
      [0.5, 1.0],
      [-1.0, 0.5]]
h = [1.0, 2.0, 3.0]
print_matrix("W1 (2x3)", W1)
print_matrix("W2 (3x2)", W2)
print(f"h = {h}")
layer1 = matvec(W2, h)
print(f"W2 h = {layer1}   (first layer)")
layer2 = matvec(W1, layer1)
print(f"W1 (W2 h) = {layer2}   (second layer)")
combined = matmul(W1, W2)
print_matrix("W1 W2 (2x2)", combined)
print(f"(W1 W2) h = {matvec(combined, h)}")
print(f"identical: {matvec(combined, h) == layer2}")
print("This is why you can precompute the composed weight matrix once and")
print("evaluate the whole network with a single 2x2 multiply per sample.")
print("The same trick is what makes a compiled graph fast.")

# ------------------------------------------------------------ powers count
print()
print("=== Computing A^n: naive versus repeated squaring ===")


def power_fast(A, n):
    result = identity(shape(A)[0])
    base = [list(row) for row in A]
    while n > 0:
        if n % 2 == 1:
            result = matmul(result, base)
        base = matmul(base, base)
        n //= 2
    return result


F = [[1.0, 1.0], [1.0, 0.0]]     # Fibonacci matrix, entries grow fast
for n in (10, 20, 30):
    slow, fast = power(F, n), power_fast(F, n)
    print(f"  F^{n}: naive == fast -> {slow == fast}, "
          f"F^{n}[0][1] = {fast[0][1]:.0f}")
print("For n = 1000 the naive version needs 1000 matrix multiplications and")
print("the entries are about 200 digits long; repeated squaring needs 10.")
```

### With Libraries

```python
# The plain-Python blocks above implement everything with nested lists. numpy
# does the same arithmetic in compiled code, and adds the shapes, views, and
# factorisations that the rest of this part is built on.

import numpy as np

print("=== The same matrices, the same numbers ===")
A = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
B = np.array([[7.0, 8.0], [9.0, 10.0], [11.0, 12.0]])

print(f"A =\n{A}")
print(f"B =\n{B}")
print(f"A @ B =\n{A @ B}")
print(f"np.matmul(A, B) =\n{np.matmul(A, B)}")
print(f"(A @ B)[0][0] = {(A @ B)[0][0]}  = 1*7 + 2*9 + 3*11")

# The @ operator is the only new syntax. Everything else is indexing.
v = np.array([1.0, 0.0, 2.0])
print(f"\nA @ v = {A @ v}   (shape {A.shape} times {v.shape})")
# A (2,3) times a column vector (3,1) also works and always returns a column.
col = v.reshape(3, 1)
print(f"A @ v.reshape(3,1) = {(A @ col).ravel()}  (same numbers, column shape)")

print()
print("=== transpose, identity, trace ===")
M = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
print(f"M.T =\n{M.T}")
print(f"M.T.shape = {M.T.shape} (was {M.shape})")
print(f"np.eye(3) =\n{np.eye(3)}")
print(f"np.trace(M) = {np.trace(M)}")

print()
print("=== matrix_power: A^n without a loop ===")
P = np.array([[1.0, 1.0], [1.0, 0.0]])
for n in (1, 5, 10):
    print(f"P^{n} =\n{np.linalg.matrix_power(P, n)}")
print("np.linalg.matrix_power uses repeated squaring internally, so it is")
print("O(log n) matrix multiplications, not O(n).")

print()
print("=== Matrix multiplication is NOT elementwise ===")
X = np.array([[1.0, 2.0], [3.0, 4.0]])
Y = np.array([[10.0, 20.0], [30.0, 40.0]])
print(f"X * Y (elementwise) =\n{X * Y}")
print(f"X @ Y (matrix)      =\n{X @ Y}")
print("The elementwise product is the same object as Hadamard product and is")
print("routinely confused with matmul. If a shape error says 'operands could not")
print("be broadcast together', you probably wanted @ and wrote *.")

print()
print("=== Structured matrices have names in numpy ===")
d = np.diag([1.0, 2.0, 3.0])
print(f"np.diag([1,2,3]) =\n{d}")
print(f"np.diag(d) recovers the diagonal: {np.diag(d)}")

T = np.zeros((4, 4))
np.fill_diagonal(T, 2.0)
for i in range(3):
    T[i, i + 1] = T[i + 1, i] = 1.0
print(f"tridiagonal 4x4 =\n{T}")
print(f"scipy-style band counts: nonzeros = {np.count_nonzero(T)}, "
      f"shape = {T.shape}")

# Block matrices: stack 2x2 blocks into a 4x4 grid.
B1 = np.array([[1.0, 2.0], [0.0, 1.0]])
B2 = np.array([[1.0, 3.0], [0.0, 1.0]])
block_diag = np.block([[B1, np.zeros((2, 2))],
                       [np.zeros((2, 2)), B2]])
print(f"\nnp.block of two 2x2 blocks =\n{block_diag}")
print("np.block is the clean way to assemble block matrices and block vectors,")
print("which is exactly the Kronecker-sum structure of quantum circuit blocks.")
print(f"block_diag @ block_diag =\n{block_diag @ block_diag}")

print()
print("=== Structure numpy uses internally: strides ===")
C = np.arange(12, dtype=float).reshape(3, 4)
print(f"C =\n{C}")
print(f"C.strides = {C.strides} bytes (row jump, column jump)")
print(f"C.T.strides = {C.T.strides}  (transposed, same memory)")
print("A transpose is free: numpy just swaps the strides. Copying is what costs.")
D = C.T
print(f"D is a view of C, not a copy: {np.shares_memory(C, D)}")

V = C[:, 1:3]
print(f"\nC[:, 1:3] =\n{V}")
print(f"shares memory with C: {np.shares_memory(C, V)}")
print("Slicing gives a view. Assignment through the view edits the original:")
V[0, 0] = 999.0
print(f"C after writing to the view =\n{C}")

print()
print("=== Sparse matrices: scipy.sparse does the same job without the zeros ===")
# Dense storage of a 4x4 tridiagonal wastes 8 of 16 slots; a sparse matrix
# stores only the nonzeros. The multiplication API is the same.
from scipy import sparse

n = 6
dense_T = np.zeros((n, n))
np.fill_diagonal(dense_T, 2.0)
for i in range(n - 1):
    dense_T[i, i + 1] = dense_T[i + 1, i] = 1.0
sparse_T = sparse.csr_matrix(dense_T)
print(f"dense storage: {dense_T.size} slots")
print(f"sparse storage: {sparse_T.nnz} values + {sparse_T.shape[0] + 1} indices")
print(f"products agree: {np.allclose(dense_T @ dense_T, (sparse_T @ sparse_T).toarray())}")

print()
print("=== Why libraries insist on float ===")
# Integer matrix multiply overflows silently in numpy if you use the wrong dtype.
small = np.array([[100000, 100000], [100000, 100000]], dtype=np.int32)
print(f"dtype int32, product = {small @ small}")
print(f"that is above the int32 maximum of {np.iinfo(np.int32).max}, and it wrapped.")
print("int64 goes further before it wraps:")
big = np.array([[100000, 100000], [100000, 100000]], dtype=np.int64)
print(f"dtype int64, product = {big @ big}")
print("and Python's arbitrary-precision ints avoid the question entirely:")
pyints = [[100000 * 100000 for _ in range(2)] for _ in range(2)]
print(f"pure Python, product = {pyints}")
```

## Common Mistakes

**Mistake 1: assuming the product of two matrices is the same as their
elementwise product.** The wrong version: `C[i][j] = A[i][j] * B[i][j]`. The
right version: `C[i][j] = Σ_k A[i][k]·B[k][j]`. In numpy this is the
`*` versus `@` confusion, and it is the single most common matrix bug. If you
want elementwise, `*` is right; if you want composition, you need `@`.

**Mistake 2: multiplying in the wrong order.** The wrong version: writing `AB`
when you mean "apply `A` first, then `B`". The right version: `AB v` means
apply `B` first. This matters whenever you mix a camera transform with a world
transform, or compose layer weights in the wrong sequence, and it produces code
that runs and returns plausible-looking garbage.

**Mistake 3: ignoring the shape check.** The wrong version: `matmul` indexing
`B[k][j]` and letting `IndexError` surface from somewhere confusing. The right
version: check that the inner dimensions agree and raise immediately with both
shapes in the message. A `2×3` by `2×3` product is a bug, not a hard case.

**Mistake 4: thinking `(AB)ᵀ = (BA)ᵀ` or `AᵀBᵀ`.** The wrong version: applying the
transpose and assuming the order survives. The right version: `(AB)ᵀ = BᵀAᵀ`. The
transpose reverses the order, which is exactly why reverse-mode automatic
differentiation and backpropagation run gradients backwards through a network —
see [lesson 51](../part04_calculus/51_derivatives.md).

**Mistake 5: storing a large sparse matrix densely.** The wrong version: an
`n × n` list of lists for an adjacency matrix with 0.1% nonzeros. The right
version: store `(row, col, value)` triples, or use `scipy.sparse`. At `n = 10⁶`,
dense storage is `10¹²` bytes and sparse storage is a few times `10⁷`.

---

## Formula Sheet

Every symbol and formula this lesson introduces. `A` is `m × n`, `B` is
`k × p`, `v ∈ F^n` is a column vector of length `n`; `i` indexes rows, `j`
indexes columns, `k` is the contracted (inner) index.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `A = (a_ij)` | `A : \{1,\dots,m\} × \{1,\dots,n\} \to F` | An `m × n` grid: `m` rows, `n` columns, one field element per cell. | Every matrix in this lesson |
| `A + B` | `(A + B)_ij = a_ij + b_ij` | Componentwise. Requires **both** to be `m × n`, or the sum is undefined. | Accumulating gradients, averaging models |
| `c \cdot A` | `(cA)_ij = c\,a_ij` | Multiply every entry by one number. | Scaling a weight matrix |
| `AB` | `(AB)_ij = \sum_{k=1}^{k} a_{ik}\,b_{kj}` | Dot the **row** `i` of `A` with the **column** `j` of `B`. Not entrywise. | Every product in this lesson |
| Shape rule for `AB` | `A` is `m × k`, `B` is `k × p` ⟹ `AB` is `m × p`. Requires `A`'s columns `= B`'s rows. | The inner dimensions must match exactly. Otherwise the product is **undefined**, not merely hard. | The first thing to check before multiplying |
| `A(Bv)` vs `(AB)v` | `A(Bv) = (AB)v` for all `v` | Applying `B` then `A` equals applying the single matrix `AB`. | Justifies folding a pipeline into one matrix |
| Reading of `AB v` | `AB v` means "apply `B` first, then `A`" | The rightmost factor acts first. | Reading graphics and network code aloud |
| Associativity | `(AB)C = A(BC)` | Reparenthesise freely. Proof: both sides are `$\sum_l \sum_k a_{il}b_{kl}c_{kj}$` over the same triples. | Folding chains; reordering loop nests |
| Non-commutativity | `AB` need not equal `BA` | `(AB)_ij` pairs `a` with the **column** index of `B`; `BA` re-pairs them. | Why graphics and layer order matters |
| `I_n` | `(I_n)_ij = \begin{cases} 1 & i = j \\ 0 & i \ne j \end{cases}`, `A^0 = I_n` | The multiplicative identity: `I_n A = A I_n = A` for any `n × n` `A`. | Starting a power loop; the target of a solve |
| `A^k`, `A^n` | `A^{k+1} = A^k A`, `A^1 = A`, `A^0 = I_n` | `k` copies of `A` multiplied together. | Repeated application of a transformation |
| Repeated squaring | `A^n`: halve `n` each step, square the base | `O(log n)` matrix multiplications instead of `n`. | Huge exact powers, e.g. Fibonacci, modular exponentiation |
| Fibonacci identity | `(P^n)_{01} = F_{n+1}` for `P = [[1,1],[1,0]]` | A 0-indexed entry of a power is a Fibonacci number. | Exact integer arithmetic with no division |
| `Aᵀ` | `(Aᵀ)_ji = a_ij`; an `m × n` matrix becomes `n × m` | Flip rows and columns. In numpy this is a **view**: it swaps strides, it does not copy. | Swapping equation/unknown roles; `QᵀQ = I` |
| `A*` | `(A*)_ji = \operatorname{conj}(a_ij)` | Conjugate transpose. Over `ℝ` it is just `Aᵀ`. | Complex and Hermitian matrices |
| `(AB)ᵀ` | `(AB)ᵀ = BᵀAᵀ` | Transposing **reverses the order**. Not `(BA)ᵀ`, not `AᵀBᵀ`. | Backpropagation; reversing a pipeline |
| `(Aᵀ)ᵀ` | `= A` | Transposing twice is the identity. | Sanity checks |
| `(A + B)ᵀ` | `= Aᵀ + Bᵀ` | Transpose respects addition. | Differentiating sums |
| `tr(A)` | `$\operatorname{tr}(A) = \sum_{i=1}^{n} a_{ii}$` | Sum of the diagonal. **Only defined for square** `n × n` matrices. | Cheap checks, power sums, optimisation |
| `tr(AB) = tr(BA)` | `$\sum_i\sum_k a_{ik}b_{ki} = \sum_k\sum_i a_{ik}b_{ki}$` | The two products may differ, but their traces agree. | Swapping factors in `O(1)` |
| `tr(A) = tr(Aᵀ)` | — | The diagonal is unchanged by flipping. | Verifying a transpose |
| Diagonal `D` | `a_ij = 0` for `i \ne j`; `(Dv)_i = D_{ii} v_i` | Each coordinate scaled independently, nothing mixed. | Feature normalisation; `O(n)` per matvec |
| Inverse of a diagonal `D` | `$(D^{-1})_{ii} = 1/D_{ii}$, valid only if **no** `D_{ii} = 0` | Reciprocate the diagonal entries; no row reduction. | Undo a per-feature rescaling |
| Sparsity | `$\operatorname{sparsity}(A) = 1 - \dfrac{\#\{(i,j): a_{ij} \ne 0\}}{mn}$` | Fraction of the grid that is zero. | Choosing a storage format |
| Bandwidth | `$\operatorname{bw}(A) = \max \lvert i - j \rvert$ over nonzero `a_ij` | How far the nonzeros reach from the main diagonal. | Tridiagonal solvers, `O(n \cdot \operatorname{bw})` |
| Bandwidth of a product | `$\operatorname{bw}(AB) \le p + q$ when `A`, `B` have bandwidths `p`, `q` | Two bands add, because a nonzero `a_ik` and a nonzero `b_kj` force `k` to be near both `i` and `j`. | Why banded × banded stays banded |
| Block matrix | `(AB)_ik = \sum_j A_{ij}B_{jk}` for matching block partitions | Multiplying block by block; a zero block times anything is zero. | Sparse Cholesky, multigrid, Kronecker structure |
| Block-diagonal | Square blocks on the diagonal, zero blocks off it | The blocks are independent subproblems. | Two separable problems at once |
| Dense multiply cost | `$\Theta(mkp)$ multiply-adds` | `mkp` entries each summing `p` products. | Choosing an algorithm |
| Diagonal matvec cost | `$\Theta(n)$` | Row `i` has one nonzero. | Why normalising features is cheap |
| numpy `*` vs `@` | `X * Y` is elementwise (Hadamard); `X @ Y` is the matrix product | Two different products with two different definitions. | The most common matrix bug in numpy |

## Multiple Choice Questions

**Q1.** Let `A = [[0,1],[1,0]]` (swap the two coordinates) and
`B = [[1,1],[0,1]]` (add the first coordinate into the second). What is
`(AB)[1,1]`?

- A) 0, because the off-diagonal entry of `A` forces the whole product to have
  zeros below the diagonal
- B) 2, because `Σ_k a_1k b_k1 = a_10 b_01 + a_11 b_11 = 0·0 + 1·1 = 1` and the
  same computation for `BA` gives a different number
- C) 1, because every product of a permutation matrix with any matrix is the
  identity
- D) The entry is undefined, because `A` and `B` are not the same shape

<details>
<summary>Answer and explanation</summary>

**B) 2, because `Σ_k a_1k b_k1 = a_10 b_01 + a_11 b_11 = 0·0 + 1·1 = 1` and the
same computation for `BA` gives a different number.**

Row 1 of `A` is `[0, 1]`, column 1 of `B` is `[1, 1]`, and the entry is
`0·1 + 1·1 = 1`. The other order gives `BA = [[1, 1], [1, 0]]`, whose `(1,1)`
entry is `1·1 + 0·0 = 1` too — coincidence, not a rule. The clean
demonstration is on the vector `[1, 1]`: `AB[1,1]ᵀ = [1, 2]ᵀ` while
`BA[1,1]ᵀ = [2, 1]ᵀ`. Same input, two different outputs, which is exactly what
"not commutative" means.

- A) invents a symmetry the matrices do not have. `AB = [[0,1],[1,1]]` is not
  lower triangular at all; the permutation just *relabels* the rows, it does not
  zero them.
- C) is the trap that makes `A` look special. A permutation matrix on the left
  permutes the **rows** of `B`; only the right-identity `A = I` leaves `B`
  alone. `A·B = [[0,1],[1,1]]`, not `I`.
- D) is false on both counts: both matrices are `2 × 2`, so the inner dimensions
  agree, and "undefined" would be the answer to a shape *mismatch*, which is
  Mistake 3's subject.

</details>

**Q2.** Which expression equals `(AB)ᵀ`?

- A) `AᵀBᵀ`
- B) `(BA)ᵀ`
- C) `BᵀAᵀ`
- D) `(AB)⁻¹`

<details>
<summary>Answer and explanation</summary>

**C) `BᵀAᵀ`.**

The derivation is one line:
`(AB)ᵀ_ij = (AB)_ji = Σ_k a_jk b_ki = Σ_k b_ki a_jk = (BᵀAᵀ)_ij`. The
transposition renames the indices, and the renamed indices are exactly the
entries of `BᵀAᵀ`. This is the rule the lesson's code checks directly with
`transpose(matmul(A, B)) == matmul(transpose(B), transpose(A))`, which prints
`True`.

- A) is the classic error, and it is tempting because two of the three transpose
  rules in the lesson *do* preserve order: `(Aᵀ)ᵀ = A` and `(A + B)ᵀ = Aᵀ + Bᵀ`.
  The product is the one that reverses, and the pattern is not arbitrary — order
  reversal is the same thing that happens when you compose functions and then
  reverse the sequence.
- B) is true but useless: `(BA)ᵀ = AᵀBᵀ` is the same identity applied to the
  *reversed* product, so it tells you nothing about `A` and `B` as given. It
  becomes correct only if you also swap `A` and `B`, which is the whole point.
- D) is a different operation entirely. `AB` and `A⁻¹B` are unrelated; the
  transpose has nothing to do with inversion, and the inverse is
  [lesson 33](../part03_linear_algebra/33_determinant_and_inverse.md).

</details>

**Q3.** `A` is `2 × 3` and `B` is `3 × 2`. What is the shape of `BA`, and is it
equal to `AB`?

- A) `2 × 2`, and the two are equal because matrix multiplication is associative
- B) `3 × 3`, and the two cannot be equal because they are not even the same
  shape
- C) `3 × 3`, and the two may or may not be equal depending on the entries
- D) Undefined, because `B` has more columns than `A` has rows

<details>
<summary>Answer and explanation</summary>

**B) `3 × 3`, and the two cannot be equal because they are not even the same
shape.**

`B` is `3 × 2` and `A` is `2 × 3`, so `B`'s columns (`2`) must match `A`'s rows
(`2`) — they do — and `BA` is `3 × 3`. The code prints `shape of A B = (2, 2)`
and `shape of B A = (3, 3)`. The lesson's own `A` and `B` give
`AB = [[58, 64], [139, 154]]` and `BA = [[39, 54, 69], [49, 68, 87], [59, 82, 105]]`.

- A) is the double error: it asserts commutativity and gets the shape backwards.
  Associativity says nothing about order at all — it says `(XY)Z = X(YZ)`, and
  the parallel `AB` and `BA` are not of that form.
- C) is the subtle one. It is *true* as a general statement about square
  matrices, but it is false as an answer about **these** matrices, and a
  multiple-choice option has to be right about the case at hand. When the shapes
  differ, equality is not a question that arises; the lesson's
  `matmul` returns a `2 × 2` from one call and a `3 × 3` from the other.
- D) misapplies the shape rule. The rule constrains the *inner* dimensions only:
  `B`'s columns against `A`'s rows. Whether `B` has "more columns than `A` has
  rows" is irrelevant if those two numbers match, and here they are both 2.

</details>

**Q4.** In numpy, `X` and `Y` are both `2 × 2` float arrays. What does `X * Y`
compute?

- A) The matrix product `Σ_k X_ik Y_kj`, the same thing `X @ Y` computes
- B) The elementwise product, with `result[i][j] = X[i][j] * Y[i][j]` and no sum
  over `k`
- C) The scalar `Σ_i Σ_j X_ij Y_ij`, a single number
- D) A syntax error, because `*` is reserved for scalars in numpy

<details>
<summary>Answer and explanation</summary>

**B) The elementwise product, with `result[i][j] = X[i][j] * Y[i][j]` and no sum
over `k`.**

`*` is the Hadamard product for arrays. The lesson's numbers: for
`X = [[1,2],[3,4]]` and `Y = [[10,20],[30,40]]`, `X * Y = [[10, 40], [90, 160]]`
while `X @ Y = [[70, 100], [150, 220]]`. Everything structural — this is Mistake
1, the single most common matrix bug in numpy.

- A) is the actual bug: writing `*` where you meant `@`. The two operations have
  nothing in common for `k > 1`; they coincide only in the degenerate case where
  the contraction index has length 1.
- C) is `np.dot` on two *flattened* vectors, or `np.sum(X * Y)`. It is a
  completely different object with a completely different shape: a scalar rather
  than a matrix.
- D) is false. `*` is fully supported and widely used; the only reason to avoid
  it on matrices is that it is not the product you usually want. The error
  message you would see for a genuine shape problem is "operands could not be
  broadcast together", which is exactly what the lesson tells you to read as a
  hint that `@` was intended.

</details>

**Q5.** The lesson's code states `tr(AB) = tr(BA)`. Does that mean `AB = BA`?

- A) Yes, because a function that agrees on a scalar summary must agree on the
  whole matrix
- B) No — the two products may be entirely different matrices whose diagonal sums
  happen to coincide
- C) Yes, but only when `A` and `B` are both symmetric
- D) No, because the trace of a product is generally not defined

<details>
<summary>Answer and explanation</summary>

**B) No — the two products may be entirely different matrices whose diagonal sums
happen to coincide.**

The theorem is about a *summary statistic*, not the object. The lesson's own
example with `X = [[1,2],[3,4]]` and `Y = [[0,1],[1,0]]` gives
`XY = [[2,1],[4,3]]` and `YX = [[3,4],[1,2]]` — four of the eight entries differ
— while `trace(XY) = 2 + 3 = 5` and `trace(YX) = 3 + 2 = 5`. The proof
`tr(AB) = Σ_i Σ_k a_ik b_ki = Σ_k Σ_i a_ik b_ki = tr(BA)` is a double sum
commuted, so the terms are re-paired, not the matrices.

- A) is the error that makes trace equalities over-used. A summary has far fewer
  degrees of freedom than the object; `n` numbers cannot determine `n²`.
- C) is true but irrelevant, and it is a misleading condition. Symmetry is
  neither needed nor sufficient: `X` and `Y` above are not symmetric and the
  equality still holds. The one case where symmetry *does* force `AB = BA` is
  `A` symmetric **and** `B` symmetric, which is a statement about `AB` rather
  than about the trace.
- D) is false. `tr` is well defined for any product of square matrices, and
  indeed it is undefined for *non-square* matrices, which is the real restriction
  worth remembering.

</details>

**Q6.** `A` has bandwidth 2 and `B` has bandwidth 3. What can you say about
`AB`?

- A) Its bandwidth is at most 5, so it is still banded and an `O(n·bw)` solver
  still applies
- B) Its bandwidth is at most 2, because the bandwidth of a product can never
  exceed the larger of the two
- C) Its bandwidth is at least 5, so the structure is destroyed by multiplying
- D) Nothing, because bandwidth is only defined for symmetric matrices

<details>
<summary>Answer and explanation</summary>

**A) Its bandwidth is at most 5, so it is still banded and an `O(n·bw)` solver
still applies.**

The proof is the index constraint. `(AB)_ij = Σ_k a_ik b_kj` can be nonzero only
if some `k` has both `a_ik ≠ 0` and `b_kj ≠ 0`. The first forces
`|i - k| ≤ 2`, the second forces `|k - j| ≤ 3`, and the triangle inequality gives
`|i - j| ≤ |i - k| + |k - j| ≤ 5`. The lesson's code demonstrates the `n = 6`
case: `bandwidth of T = 1` and `bandwidth of T*T = 2`, with 24 nonzeros out of 36
slots.

- B) is intuitively appealing — "the product can't be rougher than its parts" —
  and wrong. Take `A` with a nonzero at `(1, 1)` and at `(1, 3)`, and `B` with
  nonzeros at `(1,1)` and `(3,1)`: `k = 3` is shared and `(AB)_{1,1}` picks up a
  product of two distant nonzeros. Bands *add*, they do not take a maximum.
- C) reverses the inequality. The bound is an upper bound; the actual bandwidth
  is often smaller, as when a projection matrix annihilates everything outside
  its range. "At most" is what makes the method applicable.
- D) is false: bandwidth is defined for any square matrix, symmetric or not. The
  code's `bandwidth` function makes no symmetry assumption at all, and the
  tridiagonal matrices it is applied to are symmetric only by coincidence.

</details>

**Q7.** `A` is `2 × 2` and `B` is `2 × 2`. The code checks that
`matmul(A, B)` succeeds and that `matmul(A, A)` fails. What is the reason the
second call fails?

- A) `A` is not square, so it cannot multiply itself
- B) The inner dimensions do not agree: `A` has 3 columns and 2 rows, so `2 ≠ 3`
- C) The product of a matrix with itself is always the trace
- D) It fails because the entries of `A` are not integers

<details>
<summary>Answer and explanation</summary>

**B) The inner dimensions do not agree: `A` has 3 columns and 2 rows, so
`2 ≠ 3`.**

The rule is that `A`'s **columns** must equal `B`'s **rows**. Squaring a
non-square matrix requires the matrix to be square in the first place. The
`matmul` helper raises immediately with both shapes in the message —
`cannot multiply 2x3 by 2x3` — precisely so the failure is legible at the call
site, which is Mistake 3.

- A) is the "cannot square a non-square matrix" restatement, and it is
  technically consistent with B, but it is not the *reason* the helper detects
  it. The code does not check squareness; it checks column/row agreement, and
  that single check is what rejects `A · A`, `A · B` in the wrong order, and
  every other shape error in the lesson. Naming the symmetry as the cause would
  leave a reader unable to diagnose a `3 × 5` by `4 × 2`.
- C) describes `tr(A)`, a completely different operation that consumes `A` and
  returns a scalar. `A² = A·A` is a matrix.
- D) is irrelevant; the matrices here are floats and the shape check happens
  before any arithmetic.

</details>

**Q8.** `P = [[1,1],[1,0]]`. You need `P^1000` exactly. Why does repeated
squaring beat the naive loop, and how many matrix multiplications does it take?

- A) The naive loop needs 1000 multiplications and repeated squaring needs 500,
  because each squaring covers two steps
- B) The naive loop needs 1000 and repeated squaring needs about
  `⌊log₂ 1000⌋ + 1 = 10`, because each squaring doubles the exponent it covers
- C) Both need 1000, and repeated squaring is only faster because of cache
  behaviour
- D) Repeated squaring needs about 10 *additions*, which is cheaper than the
  multiplications the naive loop performs

<details>
<summary>Answer and explanation</summary>

**B) The naive loop needs 1000 and repeated squaring needs about
`⌊log₂ 1000⌋ + 1 = 10`, because each squaring doubles the exponent it covers.**

`1000 = 1111101000₂` has ten binary digits, so at most ten squarings and ten
accumulating multiplies are needed. The `power_fast` loop halves `n` and squares
`base` on every pass, so the number of passes is `log₂ n`, not `n`. The lesson's
own check `for n in (1, 5, 12): naive matches fast = True` confirms the two
agree exactly, which is the only thing that makes the optimisation safe.

- A) is the naive one-step-per-two-powers mistake. Squaring `base` advances from
  covering `2^t` to covering `2^{t+1}`, so the exponent doubles and the *count*
  of steps is logarithmic, not halved.
- C) is false for both halves. The count of multiplications really is different
  — 1000 versus 10 is not a cache effect — and the naive loop's cost is
  dominated by multiplying numbers with hundreds of digits, not by memory.
- D) confuses the operation with the representation. The entries of `P^1000` are
  about 209 digits long, so each "multiplication" is already a big-integer
  multiply. The saving is doing 10 of them instead of 1000.

</details>

**Q9.** Under the "machine" reading of a matrix, what does column `j` of `A` tell
you?

- A) The coefficients of the `j`-th equation in the system `Ax = b`
- B) The image of the `j`-th basis vector, `A e_j` — what the machine does to
  that one coordinate
- C) The row-reduced form of `A`, which is what solvers return
- D) The `j`-th singular value of `A`, which controls how much it stretches

<details>
<summary>Answer and explanation</summary>

**B) The image of the `j`-th basis vector, `A e_j` — what the machine does to
that one coordinate.**

`e_j` is `j` ones in position `j` and zeros elsewhere, and
`(A e_j)_i = Σ_k a_ik (e_j)_k = a_ij`. So `A e_j` is literally column `j`. The
lesson prints this directly: for each `j` it forms `e_j` and shows
`A e_j = [column j of A]`. Because `A(cu + dv) = c(Au) + d(Av)`, knowing `A` on
the basis determines `A` everywhere, which is why
`A x = Σ_j x_j (A e_j)` = the linear combination of the columns.

- A) is the *other* reading, and it is not wrong — it is just the table
  interpretation, where rows are equations. The two readings are of the same
  array, which is the lesson's central point; this question asks specifically
  about the machine reading, where the columns are images and the rows are
  coefficient lists. Rows and columns are both real; you only have to know which
  question you are asking.
- C) confuses `A` with the output of a solver. Row reduction happens to
  [lesson 32](../part03_linear_algebra/32_linear_systems_gaussian_elimination.md) and changes the matrix;
  the original columns of `A` are untouched.
- D) is about a different decomposition. Singular values come from `AᵀA`, not
  from the columns directly, and are not introduced in this lesson.

</details>

**Q10.** The lesson's numpy block builds `C = np.arange(12).reshape(3, 4)` and
then `D = C.T`. Why is it essentially free?

- A) numpy transposes in place and then frees the original, so the memory is
  recycled
- B) `D` is a *view* — it reuses `C`'s buffer and only records different strides —
  so `np.shares_memory(C, D)` is `True` and writing to `D` edits `C`
- C) `C.T` is a lazy object that numpy only materialises when printed, and the
  print is the expensive step
- D) numpy recognises that `C` is small and takes a shortcut below its normal
  size threshold

<details>
<summary>Answer and explanation</summary>

**B) `D` is a *view* — it reuses `C`'s buffer and only records different strides —
so `np.shares_memory(C, D)` is `True` and writing to `D` edits `C`.**

An `ndarray` stores a pointer plus a tuple of byte offsets telling it how far to
jump to reach the next element along each axis. A transpose is exactly a
relabelling of those offsets, so no data moves. The lesson prints
`C.strides`, `C.T.strides`, and `np.shares_memory(C, D)`, and separately shows
that a slice `V = C[:, 1:3]` is *also* a view, so `V[0, 0] = 999` changes `C`.

- A) is the mental model of a copying implementation, and it is what makes people
  write `.copy()` defensively everywhere. Nothing is freed and nothing is
  recycled; the same buffer is shared.
- C) is not how numpy works, and the printout in the lesson proves it: the
  transposed array has a different `shape` and different `strides` before
  anything is printed. Laziness would also make `D[i, j] = 5` fail, which it does
  not.
- D) is fabricated. There is no small-array threshold for transposes, and the
  lesson's `C` is `3 × 4` — twelve elements — so the effect is visible at a size
  where any special case would be absurd.

</details>

**Q11.** `np.array([[100000, 100000], [100000, 100000]], dtype=np.int32) @ itself`
prints `1410065408`. What happened?

- A) The multiplication was performed in floating point and then rounded
- B) The true value `10¹⁰` exceeds the int32 maximum `2147483647`, and the
  result wrapped around modulo `2³²`
- C) numpy refuses to multiply int32 arrays and fell back to a default dtype
- D) The array was promoted to int64 and the printed value is a display artefact

<details>
<summary>Answer and explanation</summary>

**B) The true value `10¹⁰` exceeds the int32 maximum `2147483647`, and the result
wrapped around modulo `2³²`.**

`2³² = 4294967296`, and `10¹⁰ - 2·2³² = 10000000000 - 8589934592 = 1410065408`.
The arithmetic was exact integer arithmetic that overflowed its own storage and
kept only the low 32 bits. The lesson makes the point by showing `int64`
succeeding at the same product and pure Python ints being unlimited.

- A) is wrong because no floating point was involved. The tell is that the
  answer is a *negative-look* integer that happens to satisfy
  `result mod 2³² = true value` exactly; a float would have printed
  `10000000000.0`.
- B's rival, C, is false because numpy does not refuse and does not promote
  silently here — `int32 @ int32` stays `int32`. Silent overflow is precisely
  why this is on the lesson's list of things to know.
- D) is contradicted by the printed value, which is a small positive int32-range
  integer, not a display artefact. And even a correct `int64` result would print
  as `10000000000`, not `1410065408`.

</details>

**Q12.** Why does the lesson's `matmul` check the shapes and raise immediately,
instead of letting the indexing fail on its own?

- A) Because Python's `IndexError` is slow to raise compared to an explicit check
- B) Because the index `B[k][j]` can go out of range *and still look like a valid
  access*, so a silent wrong answer is worse than a crash
- C) Because `matmul` cannot compute the result without knowing the output shape
- D) Because `ValueError` is the only exception type numpy accepts

<details>
<summary>Answer and explanation</summary>

**B) Because the index `B[k][j]` can go out of range *and still look like a valid
access*, so a silent wrong answer is worse than a crash.**

`matmul` builds `C = zeros(rows_a, cols_b)` and then reads `B[k][j]` for
`k` in `range(cols_a)`. When the shapes disagree, `cols_a > rows_b`, so for
`k ≥ rows_b` the expression `B[k][j]` indexes past the end of `B`'s row list. In
some cases that is an `IndexError`; in others — when `j` also happens to be in
range and the row list is not the length you assumed — it is a *number*, and you
get a plausible-looking wrong answer with no error at all. Failing fast with both
shapes in the message names the actual bug, which is Mistake 3.

- A) is a real but negligible concern: the check is a couple of integer
  comparisons, and it turns a confusing failure into a clear one. Speed is not
  the reason.
- C) is false — the output shape is computed *after* the check, and the whole
  point of the check is that without it you cannot know whether the input is even
  legal.
- D) mixes up two libraries. `ValueError` is a plain Python builtin, used here
  and in the lesson's own `matvec` for the analogous length check on a vector.
  numpy has its own exception hierarchy, and it is not relevant to this helper.

</details>

## Subjective Questions

### Short Answer

**Q1. State the definition of the matrix product, and state the dimensional
restriction that must hold for it to be defined at all.**

<details>
<summary>Model answer</summary>

For `A` an `m × k` matrix and `B` a `k × p` matrix over a field `F`, the product
`AB` is the `m × p` matrix whose entries are

    (AB)_ij = Σ_{k=1}^{k} a_ik b_kj

for `i` from 1 to `m` and `j` from 1 to `p`. Each entry is the dot product of
**row** `i` of `A` with **column** `j` of `B`.

The restriction: `A` must have as many columns as `B` has rows, i.e. the *inner*
dimensions must be equal. This is the only constraint; there is no requirement
that `A` and `B` be square, and `A B` and `B A` are permitted to have different
shapes (`2 × 2` and `3 × 3` in the worked example). If the inner dimensions
differ, the product is **undefined** — not merely difficult — and the lesson's
`matmul` raises a `ValueError` naming both shapes.

</details>

**Q2. List the transpose rules from the lesson, and show why `(AB)ᵀ` reverses the
order.**

<details>
<summary>Model answer</summary>

The three rules, for compatible `A`, `B`:

- `(AB)ᵀ = BᵀAᵀ`
- `(Aᵀ)ᵀ = A`
- `(A + B)ᵀ = Aᵀ + Bᵀ`

The derivation of the first, entry by entry:

    (AB)ᵀ_ij = (AB)_ji = Σ_k a_jk b_ki = Σ_k b_ki a_jk = (BᵀAᵀ)_ij

The third equality is the key: the same sum has the two factors swapped, and
`(BᵀAᵀ)_ij = Σ_k (Bᵀ)_ik (Aᵀ)_kj = Σ_k b_ki a_jk`. So the transposition has
*renamed* the indices into the pattern of the reversed product. The order
reversal is not an arbitrary rule — it is the same reversal you get by composing
functions and then running the sequence backwards.

</details>

**Q3. What is the trace, and which two identities does it satisfy that a
non-scalar-valued quantity would not?**

<details>
<summary>Model answer</summary>

For a **square** `n × n` matrix, `tr(A) = Σ_{i=1}^{n} a_ii` — the sum of the
diagonal entries. It is undefined for a non-square matrix, which is the one
restriction worth remembering.

The two identities are:

- `tr(AB) = tr(BA)` for square `A`, `B`, because
  `Σ_i Σ_k a_ik b_ki = Σ_k Σ_i a_ik b_ki`. This is a *commuted double sum*:
  `AB` and `BA` are generally different matrices, but their traces agree.
- `tr(A) = tr(Aᵀ)`, because the diagonal of `Aᵀ` is the diagonal of `A` read in
  the same order.

The practical payoff is that `tr` lets you swap the order of factors in a product
at zero cost, which is a genuine `O(1)` trick in algorithms that would otherwise
have to build the product.

</details>

**Q4. Define the bandwidth of a matrix and state the bound on the bandwidth of a
product. Give the one-line reason.**

<details>
<summary>Model answer</summary>

The **bandwidth** of a square matrix `A` is `max |i - j|` over all nonzero entries
`a_ij` — the furthest horizontal distance any nonzero reaches from the main
diagonal. A tridiagonal matrix has bandwidth 1; a diagonal matrix has bandwidth 0.

The bound: if `A` has bandwidth `p` and `B` has bandwidth `q`, then
`bw(AB) ≤ p + q`. The reason is a single index constraint. `(AB)_ij = Σ_k a_ik b_kj`
can be nonzero only if some `k` makes *both* factors nonzero, which requires
`|i - k| ≤ p` and `|k - j| ≤ q`. By the triangle inequality
`|i - j| ≤ |i - k| + |k - j| ≤ p + q`. Nothing can appear further off the
diagonal than that.

</details>

**Q5. State the operation count for a dense `m × k` by `k × p` product, for a
diagonal matvec, and for a banded matvec of bandwidth `b`.**

<details>
<summary>Model answer</summary>

- **Dense product:** `Θ(mkp)` multiply-adds. There are `mp` entries in the
  result and each sums `k` products, so `mp · k = mkp`. The lesson's own `count_dense_mults`
  computes exactly this, and for `n = 100` gives `10⁶`.
- **Diagonal matvec:** `Θ(n)`. Row `i` of a diagonal matrix has a single nonzero,
  so `(Dv)_i = D_ii v_i` needs one multiplication per row, not `n`.
- **Banded matvec of bandwidth `b`:** `Θ(n(2b + 1))`. Only entries within `b` of
  the diagonal can be nonzero, so each of the `n` rows has at most `2b + 1`
  useful products — for a tridiagonal matrix that is 3 per row, which the lesson
  states as "about `3 · 100 · 100`" for `n = 100`.

The general shape of the answer: the cost tracks the *number of stored nonzeros*,
not the dimension, which is the entire justification for sparse and structured
storage.

</details>

**Q6. What does the lesson mean by saying that `AB v` means "apply `B` first"?**
Why is that the natural reading?

<details>
<summary>Model answer</summary>

It means that in the product `AB`, the rightmost factor acts on `v` first, and
then the result is passed leftward. So `AB v = A(Bv)`: `B` transforms `v`, and
then `A` transforms whatever `B` produced.

The natural reading comes from viewing each matrix as a machine. `Bv` is "run `B`
on `v`", and `A(Bv)` is "run `A` on the output of `B`". Multiplication is
composition, and in any composition `f ∘ g` the inner function runs first. The
lesson verifies the equivalence numerically — `matvec(A, matvec(B, v))` and
`matvec(matmul(A, B), v)` are printed and compared — and the identity is exactly
what makes a chain of `L` transformations collapsible into one matrix, which is
what a compiled inference engine exploits.

</details>

### Long Answer

**Q1. Matrix multiplication is associative but not commutative. What does each
fact license, and what does each one forbid?**

<details>
<summary>Model answer</summary>

**Associativity** is the permissive fact. `(AB)C = A(BC)` holds for all compatible
matrices, proved by expanding both sides to the same triple sum
`Σ_l Σ_k a_il b_kl c_kj` over the same set of index triples. What it licenses is
**reparenthesisation**: a chain of ten transformations can be written
`A(B(C(···)))` or `(AB)(CD)···` and it makes no difference. This is what lets a
compiler or inference engine fold a whole network into one matrix, and what lets
you choose the parenthesisation that minimises the *widths* involved — a
`1 × 100000` by `100000 × 1` product is `10⁵` work while `100000 × 100000` by
`100000 × 1` is `10¹⁰`. Associativity also justifies writing loop nests in
whichever order suits cache locality.

**Non-commutativity** is the restrictive fact, and it is a theorem about the
definition, not an accident. `(AB)_ij = Σ_k a_ik b_kj` pairs the column index of
`B` with the row index of `A`. `BA` pairs them the other way round, so the two
sums are over genuinely different pairings. The lesson's counterexample is
elementary: `A = [[0,1],[1,0]]` swaps coordinates, `B = [[1,1],[0,1]]` adds the
first into the second, and on `v = [1,1]` you get `[1,2]` one way and `[2,1]` the
other.

What non-commutativity forbids is any reordering — ever, silently, "for
convenience". It is why graphics code has a strict convention (world-to-camera
then camera-to-screen, never the reverse) and why the mistake produces code that
runs and returns plausible garbage. It is also why `(AB)ᵀ = BᵀAᵀ` must reverse:
transposing a composition reverses the sequence. And it is why `tr(AB) = tr(BA)`
is worth knowing as an exception — trace is the one summary that *is*
insensitive to the reordering, which is exactly what makes it useful as a cheap
sanity check.

The practical rule that falls out: **reparenthesise freely, reorder never.** If
you find yourself writing `BC` when you meant `CB`, the shape check may not catch
it when both are square, and the code will still compile.

</details>

**Q2. Why does `matmul` need an explicit shape check, and what actually goes
wrong if you let the indexing fail on its own?**

<details>
<summary>Model answer</summary>

Because the failure is not reliably loud. `matmul` allocates
`C = zeros(rows_a, cols_b)` and computes `C[i][j] = Σ_k A[i][k] * B[k][j]` for
`k` running over `range(cols_a)`. If the shapes disagree, then `cols_a ≠ rows_b`,
and the loop asks `B[k]` for `k` up to `cols_a - 1`. When `cols_a > rows_b` that
is out of range and Python raises `IndexError` — but `IndexError: list index out
of range` does not say which of the two matrices was wrong, nor what the intended
shapes were, and it surfaces from inside a triple loop rather than from the call
that caused it. Worse, when `cols_a < rows_b` the loop never reads past the end:
it just **silently computes the wrong answer**, truncating the sum and returning a
matrix with no error whatsoever.

That asymmetry is the whole argument. A shape error should be a `ValueError` at
the boundary, naming both shapes — `cannot multiply 2x3 by 2x3` — so the reader
sees the bug at the line that wrote the operands. The lesson's worked example is
built on this: Step 8 notes that a `2 × 3` by `2 × 3` product fails "because
`2 ≠ 3`", and the code raises with both shapes in the message "rather than
letting a stray `IndexError` surface three frames later."

There is a second, subtler reason to check rather than assume. The check is the
only place where a **non-square** product is caught at all. `A Aᵀ` and `Aᵀ A` are
both always legal, both always square, and both frequently the wrong one for what
you meant — and the shape check cannot help there, because the shapes agree. That
residual risk is what the transposed product rules are for: if you find yourself
reaching for `AᵀA` in a fit, ask whether you wanted `AAᵀ`, because
`(AᵀA)ᵀ = AᵀA` while `(AAᵀ)ᵀ = AAᵀ` and they are different matrices with
different traces only by coincidence.

</details>

**Q3. Why is repeated squaring `O(log n)` rather than `O(n)`, and why does that
matter more for *exact* arithmetic than for floating point?**

<details>
<summary>Model answer</summary>

The mechanism is that the naive loop maintains the invariant `result = A^k` after
`k` iterations and advances it by one power per iteration, so it needs `n`
matrix multiplications for `A^n`. Repeated squaring instead keeps a base and
halves the remaining exponent each pass:

    while n > 0:
        if n odd:  result = result · base
        base = base · base
        n = n // 2

Every pass squares the base, so the base covers `1, 2, 4, 8, …` factors. After
`t` passes the covered exponent is `2^t`, so the loop terminates after
`⌈log₂ n⌉` passes regardless of how large `n` is. For `n = 1000`,
`1000 = 1111101000₂` has ten bits, so ten passes suffice against the naive loop's
1000 — a 100× reduction in multiplications. The lesson checks `n ∈ {1, 5, 12}`
and confirms the two agree, which is the only thing that licenses the swap.

The reason it matters *more* for exact arithmetic is that the cost of a
multiplication is not constant. In floating point every entry is a fixed 8 or 16
bytes, so a `2 × 2` multiply is a fixed handful of cycles no matter how big `n`
is — the saving is a clean constant factor. But the entries of `P^n` grow
exponentially: `P^12[0][1] = 144`, `P^25[0][1] = 75025`, and `P^1000[0][1]` has
about 209 decimal digits. Each multiplication is therefore a big-integer
multiply on hundreds-of-digit numbers, whose cost is superlinear in the digit
count. Cutting the *number* of multiplications from 1000 to 10 then cuts the
total cost by far more than 100×, because the ten surviving multiplications are
also far smaller on average than the thousand the naive loop performs.

This is why the technique appears in exactly the places it does: `pow(base, exp,
mod)` in Python for modular exponentiation, which is the basis of fast RSA-style
exponentiation, and the same loop in `np.linalg.matrix_power`, which the lesson
notes uses repeated squaring internally. The lesson's `F = [[1,1],[1,0]]`
identity `(F^n)[0][1] = F_{n+1}` is the textbook demonstration: the matrix method
gives exact integer Fibonacci numbers with no division and no rounding.

</details>

**Q4. Structure beats cleverness in matrix code. Give the accounting, and explain
why a shipped sparse matrix formats rather than a clever dense kernel.**

<details>
<summary>Model answer</summary>

The accounting is embarrassingly simple, which is why it is worth memorising
rather than deriving. A dense `n × n` by `n × n` product costs `Θ(n³)`
multiply-adds. Now note what each structural class actually needs:

- **Diagonal** `D`: row `i` has one nonzero, so `Dv` costs `Θ(n)` — a factor of
  `n` better than the `Θ(n²)` dense matvec.
- **Banded** with bandwidth `b`: only `2b + 1` entries per row can be nonzero, so
  the matvec costs `Θ(n(2b+1))`. The lesson's numbers: `1000` multiply-adds
  dense versus `1000` diagonal, and about `3 · 100 · 100` for tridiagonal times
  dense against `10⁶` for the dense version.
- **Block-diagonal** with `k` blocks: the zero blocks cost `0 · anything = 0`, so
  the product is the sum of `k` independent block products and the cost is the
  sum of the blocks' costs, not the whole.

The lesson's decisive count is for `n = 100`: a diagonal matrix times a dense one
does `10⁶` multiply-adds in the naive triple loop but only `10⁴` of them have two
nonzero factors — a ratio of 100, and it grows with `n`.

Why ship sparse formats rather than a clever dense kernel: because a clever dense
kernel still has to *look at* every one of the `n²` slots to decide whether it is
zero, and that branch is what you were trying to avoid. `scipy.sparse.csr_matrix`
stores three parallel arrays — column indices, row pointers, and values — so the
nonzeros are enumerated directly and the zeros are never visited at all. The
lesson's measurement on a `6 × 6` tridiagonal is the shape of the whole argument:
`36` dense slots versus `18` stored values, and at `n = 10⁴` that is a few tens
of thousands of numbers against a hundred million. The asymptotic gap is
`O(n)` versus `O(n²)`, and the `O(1)` dense kernel cannot recover it.

The two failure modes to avoid, both of which the lesson's structure sections
guard against. First, storing a sparse matrix densely: at `n = 10⁶` an adjacency
matrix with 0.1% nonzeros costs `10¹²` bytes dense versus a few times `10⁷`
sparse — you have not made the arithmetic faster, you have made it impossible.
Second, assuming structure survives. Bandwidths *add* under multiplication, so a
banded-times-banded is banded but wider (`1` becomes `2` in the lesson's `T·T`),
and block-diagonal times block-diagonal stays block-diagonal only because the
off-diagonal blocks are genuinely zero. Products of general structured matrices
are not automatically structured, which is why you check the bandwidth after the
multiply rather than trusting it.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — compute a product by hand and in code.** Let

    A = | 1 2 3 |   B = | 2 0 1 |
        | 4 5 6 |       | 1 3 0 |
        | 7 8 10|       | 4 1 5 |

Compute every entry of `AB` with the row-by-column rule, then verify with a
three-line `matmul`.

<details>
<summary>Solution</summary>

```python
def shape(M):
    return len(M), len(M[0])


def zeros(rows, cols):
    return [[0.0] * cols for _ in range(rows)]


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


A = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 10.0]]
B = [[2.0, 0.0, 1.0], [1.0, 3.0, 0.0], [4.0, 1.0, 5.0]]

print("=== Exercise 1: a 3x3 product, entry by entry ===")
AB = matmul(A, B)
for i in range(3):
    for j in range(3):
        terms = " + ".join(f"{A[i][k]:.0f}*{B[k][j]:.0f}" for k in range(3))
        total = sum(A[i][k] * B[k][j] for k in range(3))
        print(f"  (AB)[{i}][{j}] = {terms} = {total:.0f}")
print(f"matrix form =\n{AB}")
```

Output:

```
=== Exercise 1: a 3x3 product, entry by entry ===
  (AB)[0][0] = 1*2 + 2*1 + 3*4 = 16
  (AB)[0][1] = 1*0 + 2*3 + 3*1 = 9
  (AB)[0][2] = 1*1 + 2*0 + 3*5 = 16
  (AB)[1][0] = 4*2 + 5*1 + 6*4 = 37
  (AB)[1][1] = 4*0 + 5*3 + 6*1 = 21
  (AB)[1][2] = 4*1 + 5*0 + 6*5 = 34
  (AB)[2][0] = 7*2 + 8*1 + 10*4 = 62
  (AB)[2][1] = 7*0 + 8*3 + 10*1 = 34
  (AB)[2][2] = 7*1 + 8*0 + 10*5 = 57
matrix form =
[[16.0, 9.0, 16.0], [37.0, 21.0, 34.0], [62.0, 34.0, 57.0]]
```

</details>

**[ ] Exercise 2 — the four laws.** For `X = [[1,2],[3,4]]`,
`Y = [[0,1],[1,0]]`, `Z = [[1,1],[1,0]]`, check that `XY ≠ YX`, that
`(XY)Z = X(YZ)`, that `XI = IX = X`, and that `(AB)ᵀ = BᵀAᵀ`.

<details>
<summary>Solution</summary>

```python
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


X = [[1.0, 2.0], [3.0, 4.0]]
Y = [[0.0, 1.0], [1.0, 0.0]]
Z = [[1.0, 1.0], [1.0, 0.0]]
A = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 10.0]]
B = [[2.0, 0.0, 1.0], [1.0, 3.0, 0.0], [4.0, 1.0, 5.0]]

print("=== Exercise 2: associativity, non-commutativity, identity ===")
print(f"X Y =\n{matmul(X, Y)}")
print(f"Y X =\n{matmul(Y, X)}")
print(f"X Y == Y X : {matmul(X, Y) == matmul(Y, X)}")
print(f"(XY)Z == X(YZ) : {matmul(matmul(X, Y), Z) == matmul(X, matmul(Y, Z))}")
print(f"X I == X : {matmul(X, identity(2)) == X}")
print(f"I X == X : {matmul(identity(2), X) == X}")
print(f"(AB)^T == B^T A^T : "
      f"{transpose(matmul(A, B)) == matmul(transpose(B), transpose(A))}")
```

Output:

```
=== Exercise 2: associativity, non-commutativity, identity ===
X Y =
[[2.0, 1.0], [4.0, 3.0]]
Y X =
[[3.0, 4.0], [1.0, 2.0]]
X Y == Y X : False
(XY)Z == X(YZ) : True
X I == X : True
I X == X : True
(AB)^T == B^T A^T : True
```

Notice `XY ≠ YX` while `(XY)Z = X(YZ)`. Those two facts together are why you may
reparenthesise a chain of transformations freely but may never reorder it.

</details>

**[ ] Exercise 3 — order of composition.** Let `R = [[0,-1],[1,0]]` rotate a
point 90° counterclockwise and `Sx = [[1,1],[0,1]]` shear it. Apply both, both
orders, to `v = [2, 1]`. Show that `R(Sx v) = (R Sx) v` and `Sx(R v) = (Sx R) v`,
and that the two results differ.

<details>
<summary>Solution</summary>

```python
def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(A[0]))) for j in range(len(B[0]))]
            for i in range(len(A))]


def matvec(M, v):
    return [sum(M[i][k] * v[k] for k in range(len(M[0]))) for i in range(len(M))]


R = [[0.0, -1.0], [1.0, 0.0]]      # rotate 90 degrees counterclockwise
Sx = [[1.0, 1.0], [0.0, 1.0]]     # shear: (x, y) -> (x + y, y)
v = [2.0, 1.0]

print("=== Exercise 3: composition order on a vector ===")
print(f"v = {v}")
print(f"rotate first, then shear: R(Sx v) = {matvec(R, matvec(Sx, v))}")
print(f"  because (R Sx) v   = {matvec(matmul(R, Sx), v)}")
print(f"shear first, then rotate: Sx(R v) = {matvec(Sx, matvec(R, v))}")
print(f"  because (Sx R) v   = {matvec(matmul(Sx, R), v)}")
print("Same two transforms, same vector, different answers. Order is the whole")
print("story, which is why (R Sx) v = v is not the same claim as (Sx R) v = v.")
```

Output:

```
=== Exercise 3: composition order on a vector ===
v = [2.0, 1.0]
rotate first, then shear: R(Sx v) = [-1.0, 3.0]
  because (R Sx) v   = [-1.0, 3.0]
shear first, then rotate: Sx(R v) = [1.0, 2.0]
  because (Sx R) v   = [1.0, 2.0]
```

By hand: `Sx v = [2+1, 1] = [3, 1]`, then `R[3,1] = [0·3 - 1·1, 1·3 + 0·1] = [-1, 3]`.
The other order: `R v = [0·2 - 1·1, 1·2 + 0·1] = [-1, 2]`, then
`Sx[-1,2] = [-1+2, 2] = [1, 2]`. Different, as expected.

</details>

**[ ] Exercise 4 — powers of the Fibonacci matrix.** The matrix
`F = [[1,1],[1,0]]` has the property that `(Fⁿ)[0][1]` is the `(n+1)`-th Fibonacci
number. Compute `F^n` for `n = 10`, `20`, `25` by repeated multiplication and by
repeated squaring, confirm they agree, and check the Fibonacci entries.

<details>
<summary>Solution</summary>

```python
def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(A[0]))) for j in range(len(B[0]))]
            for i in range(len(A))]


def power(A, n):
    """Naive: n matrix multiplications."""
    result = identity(len(A))
    for _ in range(n):
        result = matmul(result, A)
    return result


def power_fast(A, n):
    """Repeated squaring: O(log n) matrix multiplications."""
    result = identity(len(A))
    base = [list(row) for row in A]
    while n > 0:
        if n % 2 == 1:
            result = matmul(result, base)
        base = matmul(base, base)
        n //= 2
    return result


F = [[1.0, 1.0], [1.0, 0.0]]

print("=== Exercise 4: powers and repeated squaring ===")
for n in (0, 1, 10, 25):
    slow, fast = power(F, n), power_fast(F, n)
    print(f"  F^{n}: naive == fast -> {slow == fast}, F^{n} =\n{slow}")
print("Entries of F^n are Fibonacci numbers: F^n[0][1] is the (n+1)th one.")
```

Output:

```
=== Exercise 4: powers and repeated squaring ===
  F^0: naive == fast -> True, F^0 =
[[1.0, 0.0], [0.0, 1.0]]
  F^1: naive == fast -> True, F^1 =
[[1.0, 1.0], [1.0, 0.0]]
  F^10: naive == fast -> True, F^10 =
[[89.0, 55.0], [55.0, 34.0]]
  F^25: naive == fast -> True, F^25 =
[[121393.0, 75025.0], [75025.0, 46368.0]]
Entries of F^n are Fibonacci numbers: F^n[0][1] is the (n+1)th one.
```

`F^10[0][1] = 55`, which is the 11th Fibonacci number. `F^25[0][1] = 75025`.
This is the matrix form of the fast-doubling idea, and it is the same trick as
`pow(base, exp, mod)` in
[lesson 111](../part09_number_theory_crypto/111_modular_arithmetic_and_crypto.md).

</details>

**[ ] Exercise 5 — structure and its cost.** Build the `6 × 6` tridiagonal matrix
with 2 on the diagonal and 1 above and below. (a) Report its sparsity and
bandwidth. (b) Multiply it by itself and report the bandwidth of the result.
(c) Explain in one sentence why the bandwidth of the product is the sum. (d) For
a `100 × 100` product, count the multiply-adds a dense triple loop performs
versus a diagonal-times-dense routine.

**Challenge.** Build a block-diagonal `4 × 4` from `B11 = [[1,2],[0,1]]` and
`B22 = [[1,3],[0,1]]` with zero off-diagonal blocks. Verify by hand that
`B11·B11 = [[1,4],[0,1]]`, then show the full product's blocks are `B11·B11`,
zero, zero, `B22·B22`.

<details>
<summary>Solution</summary>

```python
def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(A[0]))) for j in range(len(B[0]))]
            for i in range(len(A))]


def shape(M):
    return len(M), len(M[0])


def sparsity(M, tol=1e-12):
    rows, cols = shape(M)
    nonzero = sum(1 for i in range(rows) for j in range(cols) if abs(M[i][j]) > tol)
    return 1.0 - nonzero / (rows * cols)


def bandwidth(M, tol=1e-12):
    rows, cols = shape(M)
    return max((abs(i - j) for i in range(rows) for j in range(cols)
                if abs(M[i][j]) > tol), default=0)


n = 6
T = [[2.0 if i == j else (1.0 if abs(i - j) == 1 else 0.0) for j in range(n)]
     for i in range(n)]

print("=== Exercise 5: structure and cost ===")
print(f"T =\n{T}")
print(f"shape {shape(T)}, sparsity {sparsity(T):.4f}, bandwidth {bandwidth(T)}")
print(f"T*T has bandwidth {bandwidth(matmul(T, T))} (the two bandwidths add)")
print(f"nonzeros in T*T = "
      f"{sum(1 for i in range(n) for j in range(n) if matmul(T, T)[i][j] != 0)}")

D = [[3.0, 0.0, 0.0], [0.0, 0.5, 0.0], [0.0, 0.0, 2.0]]
w = [2.0, 4.0, 5.0]
print()
print(f"D =\n{D}")
print(f"D w = {[sum(D[i][k] * w[k] for k in range(3)) for i in range(3)]} "
      f"(each coordinate scaled independently)")
print(f"D@D =\n{matmul(D, D)}  (diagonal entries squared)")

print()
print("Cost accounting for a 100x100 product:")
print(f"  dense triple loop  : {100 * 100 * 100} multiply-adds")
print(f"  diagonal x dense   : {100 * 100} multiply-adds")
print(f"  tridiagonal x dense: about {3 * 100 * 100} multiply-adds")
```

Output:

```
=== Exercise 5: structure and cost ===
T =
[[2.0, 1.0, 0.0, 0.0, 0.0, 0.0], [1.0, 2.0, 1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 2.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 2.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0, 2.0, 1.0], [0.0, 0.0, 0.0, 0.0, 1.0, 2.0]]
shape (6, 6), sparsity 0.5556, bandwidth 1
T*T has bandwidth 2 (the two bandwidths add)
nonzeros in T*T = 24
```

For (c): `(AB)_ij` sums over `k`, and `A_ik ≠ 0` requires `k` within `p` of `i`
while `B_kj ≠ 0` requires `k` within `q` of `j`. Both can hold only when
`|i - j| ≤ p + q`, so the product has bandwidth at most `p + q`.

```python
def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(A[0]))) for j in range(len(B[0]))]
            for i in range(len(A))]


B11 = [[1.0, 2.0], [0.0, 1.0]]
B22 = [[1.0, 3.0], [0.0, 1.0]]
print("=== Challenge: block-diagonal 4x4 ===")
print(f"B11 =\n{B11}, B11*B11 =\n{matmul(B11, B11)}")
print(f"B22 =\n{B22}, B22*B22 =\n{matmul(B22, B22)}")
B = [[1.0, 2.0, 0.0, 0.0],
     [0.0, 1.0, 0.0, 0.0],
     [0.0, 0.0, 1.0, 3.0],
     [0.0, 0.0, 0.0, 1.0]]
print(f"full block matrix B =\n{B}")
print(f"B*B =\n{matmul(B, B)}")
```

Output:

```
=== Challenge: block-diagonal 4x4 ===
B11 =
[[1.0, 2.0], [0.0, 1.0]], B11*B11 =
[[1.0, 4.0], [0.0, 1.0]]
B22 =
[[1.0, 3.0], [0.0, 1.0]], B22*B22 =
[[1.0, 6.0], [0.0, 1.0]]
full block matrix B =
[[1.0, 2.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 3.0], [0.0, 0.0, 0.0, 1.0]]
B*B =
[[1.0, 4.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 6.0], [0.0, 0.0, 0.0, 1.0]]
```

`B11·B11 = [[1·1+2·0, 1·2+2·1], [0·1+1·0, 0·2+1·1]] = [[1, 4], [0, 1]]` ✓ and the
off-diagonal blocks of `B·B` are zero, exactly as block multiplication predicts.

</details>

**[ ] Exercise 6 — folding a pipeline, and the one thing that will not fold.**
Take three transformations on `ℝ³`:

    C = | 1 0 1 |   adds z into x
        | 0 1 0 |
        | 0 0 1 |

    B = | 1 0 0 |   projects onto the x-y plane (throws z away)
        | 0 1 0 |
        | 0 0 0 |

    A = | 0 1 0 |   swaps x and y
        | 1 0 0 |
        | 0 0 1 |

1. Apply them one at a time to `v = [1, 2, 3]` and report each intermediate.
2. Form the single folded matrix `ABC` and confirm `(ABC)v` equals the staged
   result. Show `BC` and `A(BC)` explicitly.
3. Form the reversed product `CBA`, apply it to the same `v`, and say what that
   tells you about the rule you are allowed to apply to a chain of transforms.
4. Count the multiply-adds per sample for the three-stage pipeline and for the
   folded matrix, and report the nonzeros of each.

**Challenge.** Two affine layers `y = W₂(W₁x + b₁) + b₂` fold into
`(W₂W₁)x + (W₂b₁ + b₂)` — the bias becomes one constant vector. With
`W₁ = [[1,-1],[0,2]]`, `b₁ = [0.5,-0.5]`, `W₂ = [[0,1],[1,0]]`, `b₂ = [1,0]`,
(a) compute the folded map and (b) compute what the network actually returns for
`x = [-1, 2]` if a ReLU sits between the layers. Explain the discrepancy, and
then show an input for which the two agree exactly and say why that input is
degenerate.

<details>
<summary>Solution</summary>

**Parts 1 to 4 by hand.**

Stage 1, `C v`: row 0 is `[1,0,1]`, so `1·1 + 0·2 + 1·3 = 4`; rows 1 and 2 pass
the vector through. So `C v = [4, 2, 3]`.

Stage 2, `B(Cv)`: rows 0 and 1 of `B` pass through, row 2 of `B` is all zeros.
So `B(Cv) = [4, 2, 0]`.

Stage 3, `A(B(Cv))`: row 0 of `A` picks the second entry, row 1 picks the first,
row 2 picks the third. So `A(B(Cv)) = [2, 4, 0]`.

Now fold. `BC`, by hand: row 0 of `B` is `[1,0,0]`, which selects row 0 of `C`,
namely `[1,0,1]`; row 1 of `B` is `[0,1,0]`, selecting row 1 of `C`, namely
`[0,1,0]`; row 2 of `B` is `[0,0,0]`, selecting the zero row. So

    BC = | 1 0 1 |
         | 0 1 0 |
         | 0 0 0 |

Then `A(BC)`: row 0 of `A` is `[0,1,0]`, selecting row 1 of `BC`; row 1 of `A` is
`[1,0,0]`, selecting row 0 of `BC`; row 2 selects row 2 of `BC`, the zero row. So

    ABC = | 0 1 0 |
          | 1 0 1 |
          | 0 0 0 |

Then `(ABC)v = [0·1 + 1·2 + 0·3, 1·1 + 0·2 + 1·3, 0] = [2, 4, 0]`, which is the
staged result. Associativity is what licensed folding at all.

The reversed product `CBA`: `BA` first. Row 0 of `B` selects row 0 of `A`
`[0,1,0]`; row 1 of `B` selects row 1 of `A` `[1,0,0]`; row 2 of `B` selects the
zero row. So `BA = [[0,1,0],[1,0,0],[0,0,0]]`. Then `C(BA)`: row 0 of `C` is
`[1,0,1]`, so row 0 of the product is row 0 of `BA` plus row 2 of `BA` =
`[0,1,0]`; rows 1 and 2 pass through. So

    CBA = | 0 1 0 |
          | 1 0 0 |
          | 0 0 0 |

which differs from `ABC` only in the `(1,2)` entry — `0` versus `1`. Applied to
`v` that gives `[0·1 + 1·2 + 0·3, 1·1 + 0·2 + 0·3, 0] = [2, 1, 0]`, a *different*
answer from `[2, 4, 0]`. Same three matrices, same vector, legal product, wrong
picture. The rule you may apply to a chain is reparenthesise, never reorder.

Cost: three `3 × 3` matvecs is `3 · 9 = 27` multiply-adds per sample; one folded
matvec is `9`. That is a `3×` reduction before exploiting any sparsity, and the
folded matrix is itself sparser (3 nonzeros of 9) than any of the stages, because
`B` destroyed the third coordinate and `A` only permutes.

```python
def shape(M):
    return len(M), len(M[0])


def zeros(rows, cols):
    return [[0.0] * cols for _ in range(rows)]


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


def vecadd(u, v):
    return [a + b for a, b in zip(u, v)]


def transpose(M):
    rows, cols = shape(M)
    return [[M[i][j] for i in range(rows)] for j in range(cols)]


def nonzero_count(M):
    return sum(1 for i in range(shape(M)[0]) for j in range(shape(M)[1]) if M[i][j] != 0.0)


C = [[1.0, 0.0, 1.0],       # add z into x
     [0.0, 1.0, 0.0],
     [0.0, 0.0, 1.0]]
B = [[1.0, 0.0, 0.0],       # project onto the x-y plane
     [0.0, 1.0, 0.0],
     [0.0, 0.0, 0.0]]
A = [[0.0, 1.0, 0.0],       # swap x and y
     [1.0, 0.0, 0.0],
     [0.0, 0.0, 1.0]]
v = [1.0, 2.0, 3.0]

print("=== Part 1: three stages, applied one at a time ===")
s1 = matvec(C, v)
s2 = matvec(B, s1)
s3 = matvec(A, s2)
print(f"v            = {v}")
print(f"C v          = {s1}   (x becomes x + z)")
print(f"B (C v)      = {s2}   (z is thrown away)")
print(f"A (B (C v))  = {s3}   (x and y swapped)")

print()
print("=== Part 2: the same three stages folded into one matrix ===")
print("associativity lets us reparenthesise, so (A B C) is legal to form:")
print(f"B C =\n{matmul(B, C)}")
print(f"A (B C) =\n{matmul(A, matmul(B, C))}")
folded = matmul(A, matmul(B, C))
print(f"(folded) v = {matvec(folded, v)}")
print(f"identical to the staged result: {matvec(folded, v) == s3}")

print()
print("=== Part 3: the other order is a different machine, and also legal ===")
reversed_order = matmul(C, matmul(B, A))
print(f"C (B A) =\n{reversed_order}")
print(f"(reversed) v = {matvec(reversed_order, v)}")
print(f"same as forward order: {matvec(reversed_order, v) == s3}")

print()
print("=== Part 4: what folding costs and saves, per sample ===")
staged_cost = sum(shape(M)[0] * shape(M)[1] for M in (C, B, A))
folded_cost = shape(folded)[0] * shape(folded)[1]
print(f"three staged matvecs: {staged_cost} multiply-adds per sample")
print(f"one folded matvec:    {folded_cost} multiply-adds per sample")
print(f"{staged_cost / folded_cost:.1f}x faster on a batch of 1000000 samples: "
      f"{staged_cost * 1000000} -> {folded_cost * 1000000} multiply-adds")
print()
print("The folded matrix is sparser than any of the stages it replaces:")
for name, M in (("C", C), ("B", B), ("A", A), ("folded", folded)):
    print(f"  {name:7s} nonzeros = {nonzero_count(M)} of 9")

print()
print("=== Challenge: two affine layers fold, but only if nothing in between bends ===")
W1 = [[1.0, -1.0],
      [0.0, 2.0]]
b1 = [0.5, -0.5]
W2 = [[0.0, 1.0],
      [1.0, 0.0]]
b2 = [1.0, 0.0]
x = [-1.0, 2.0]

# (a) The folded affine map, with the bias collapsed into one constant vector.
W_folded = matmul(W2, W1)
b_folded = vecadd(matvec(W2, b1), b2)
y_folded = vecadd(matvec(W_folded, x), b_folded)
print(f"W2 W1      = {W_folded}")
print(f"W2 b1 + b2 = {b_folded}   (the bias folds into one constant vector)")
print(f"folded affine = {y_folded}")

# (b) The real network, with a ReLU between the two affine layers.
h_affine = vecadd(matvec(W1, x), b1)
h_relu = [max(0.0, t) for t in h_affine]
y_real = vecadd(matvec(W2, h_relu), b2)
print()
print(f"x              = {x}")
print(f"layer 1 affine = {h_affine}")
print(f"layer 1 relu   = {h_relu}   (the negative entry is clipped to 0)")
print(f"layer 2 affine = {y_real}   <- what the network actually returns")
print(f"agree: {y_folded == y_real}")

print()
print("The first coordinate agrees by luck; the second does not. The folded map")
print("produced -2.5 and the network clipped that to 0. Folding assumes the whole")
print("chain is linear, and relu(max(0, t)) is not: relu(a + b) != relu(a) + relu(b).")
y_real2 = vecadd(matvec(W2, [max(0.0, t) for t in vecadd(matvec(W1, [2.0, 1.0]), b1)]), b2)
y_folded2 = vecadd(matvec(W_folded, [2.0, 1.0]), b_folded)
print(f"Now with x = [2.0, 1.0]: network {y_real2}, folded {y_folded2}, "
      f"agree: {y_real2 == y_folded2}")
print("This input is degenerate: every pre-activation is positive, so relu is the")
print("identity on the whole path and the two models coincide by accident. One such")
print("input proves nothing; the disagreement on x = [-1.0, 2.0] proves the point.")
```

Output:

```
=== Part 1: three stages, applied one at a time ===
v            = [1.0, 2.0, 3.0]
C v          = [4.0, 2.0, 3.0]   (x becomes x + z)
B (C v)      = [4.0, 2.0, 0.0]   (z is thrown away)
A (B (C v))  = [2.0, 4.0, 0.0]   (x and y swapped)

=== Part 2: the same three stages folded into one matrix ===
associativity lets us reparenthesise, so (A B C) is legal to form:
B C =
[[1.0, 0.0, 1.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]]
A (B C) =
[[0.0, 1.0, 0.0], [1.0, 0.0, 1.0], [0.0, 0.0, 0.0]]
(folded) v = [2.0, 4.0, 0.0]
identical to the staged result: True

=== Part 3: the other order is a different machine, and also legal ===
C (B A) =
[[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
(reversed) v = [2.0, 1.0, 0.0]
same as forward order: False

=== Part 4: what folding costs and saves, per sample ===
three staged matvecs: 27 multiply-adds per sample
one folded matvec:    9 multiply-adds per sample
3.0x faster on a batch of 1000000 samples: 27000000 -> 9000000 multiply-adds

The folded matrix is sparser than any of the stages it replaces:
  C       nonzeros = 4 of 9
  B       nonzeros = 2 of 9
  A       nonzeros = 3 of 9
  folded  nonzeros = 3 of 9

=== Challenge: two affine layers fold, but only if nothing in between bends ===
W2 W1      = [[0.0, 2.0], [1.0, -1.0]]
W2 b1 + b2 = [0.5, 0.5]   (the bias folds into one constant vector)
folded affine = [4.5, -2.5]

x              = [-1.0, 2.0]
layer 1 affine = [-2.5, 3.5]
layer 1 relu   = [0.0, 3.5]   (the negative entry is clipped to 0)
layer 2 affine = [4.5, 0.0]   <- what the network actually returns
agree: False

The first coordinate agrees by luck; the second does not. The folded map
produced -2.5 and the network clipped that to 0. Folding assumes the whole
chain is linear, and relu(max(0, t)) is not: relu(a + b) != relu(a) + relu(b).
Now with x = [2.0, 1.0]: network [2.5, 1.5], folded [2.5, 1.5], agree: True
This input is degenerate: every pre-activation is positive, so relu is the
identity on the whole path and the two models coincide by accident. One such
input proves nothing; the disagreement on x = [-1.0, 2.0] proves the point.
```

**Challenge worked through by hand.** `W₂W₁`: row 0 of `W₂` is `[0,1]`, selecting
row 1 of `W₁` = `[0,2]`; row 1 of `W₂` is `[1,0]`, selecting row 0 of `W₁` =
`[1,-1]`. So `W₂W₁ = [[0,2],[1,-1]]`.

The bias: `W₂b₁ = [0·0.5 + 1·(-0.5), 1·0.5 + 0·(-0.5)] = [-0.5, 0.5]`, and adding
`b₂ = [1, 0]` gives `[0.5, 0.5]`.

The folded map at `x = [-1, 2]`: `W₂W₁ x = [0·(-1) + 2·2, 1·(-1) + (-1)·2] =
[4, -3]`, plus `[0.5, 0.5]` gives `[4.5, -2.5]`.

The real network: `W₁x = [1·(-1) + (-1)·2, 0·(-1) + 2·2] = [-3, 4]`, plus
`b₁` gives `[-2.5, 3.5]`; ReLU gives `[0, 3.5]`; `W₂[0, 3.5] = [0·0 + 1·3.5,
1·0 + 0·3.5] = [3.5, 0]`, plus `b₂` gives `[4.5, 0]`.

The first coordinates agree at `4.5`; the second is `-2.5` versus `0`. The cause
is exactly one nonlinearity. Folding works because `y = W₂(W₁x + b₁) + b₂`
expands to `(W₂W₁)x + (W₂b₁ + b₂)` using only distributivity, and distributivity
holds for **linear** maps. ReLU does not distribute over addition:
`relu(a + b) = max(0, a + b) ≠ max(0, a) + max(0, b)` in general — take
`a = -2.5`, `b = 3.5`, where `relu(1) = 1` but `relu(-2.5) + relu(3.5) = 3.5`.
So the folded map is a different function, and the input `x = [2, 1]` that makes
them agree is degenerate precisely because every pre-activation on the path
(`[1.5, 1.5]`) is positive, so ReLU is the identity there and the two models
coincide by accident. That is the general warning: a single agreeing test point
proves nothing about a fold that is supposed to hold on all inputs.

The upshot for real systems: you may fold a chain of **affine** maps into one
matrix, with all biases collapsing into a single constant vector, and that is
exactly what a compiled inference graph does. You may not fold across a ReLU, a
sigmoid, a softmax, or any nonlinearity, which is why "fuse the layers" is a
legitimate optimisation for a linear head and a correctness bug in the middle of
a deep network. And the fold is only ever a *precomputation*: you pay `O(mnk)` once
to build `W₂W₁` and then `O(n²)` per sample instead of two passes, which for a
million samples is the difference between the numbers the code prints.

</details>

## Summary

- A matrix is a grid of numbers, so in code it is a list of lists; the shape
  rule is that the inner dimensions of a product must agree.
- `(AB)_ij = Σ_k a_ik b_kj`, so each entry is a row of `A` dotted with a column
  of `B`. That single formula is both the table reading and the machine reading.
- `AB` means apply `B` first, then `A`, and `(AB)v = A(Bv)`. Composition, not
  convolution.
- Multiplication is associative but not commutative, so you can reparenthesise a
  chain of transforms but never reorder it.
- `(AB)ᵀ = BᵀAᵀ` reverses the order, which is the algebra behind backpropagation,
  and `tr(AB) = tr(BA)` lets you swap factors in `O(1)`.
- `Aⁿ` is `n` applications; repeated squaring gets there in `O(log n)`
  multiplications, and is how you compute huge exact powers like Fibonacci.
- Diagonal matrices cost `O(n)` per matvec and invert entrywise; sparse and
  banded matrices cost `O(n · bandwidth)`. Structure, not cleverness, is how you
  make matrices fast.
- In numpy, `*` is elementwise and `@` is matrix multiplication. Confusing them
  is the most common matrix bug there is.

## Next

[32 — Linear Systems and Gaussian Elimination](../part03_linear_algebra/32_linear_systems_gaussian_elimination.md)
uses everything here to answer one question: given `Ax = b`, what is `x`? It
builds the row-reduction algorithm by hand, explains partial pivoting and why it
is numerically stable, and works through a system that has no unique solution.
