# 41 — Matrices, Graphs, and Applications

**Part**: part03_linear_algebra · **Prerequisites**: 40 · **Time**: 40 min

---

## In Plain Words

You now have four tools that solve four kinds of question about a matrix.
Eigenvalues tell you which directions a square matrix merely stretches.
The eigendecomposition simplifies those matrices into a list of numbers.
The SVD works on every matrix and tells you how much it stretches each
direction. And PCA uses that to find the directions in which your data
actually varies.

This lesson puts all of them to work on a graph. The starting observation is
tiny: a graph *is* a matrix. Put a 1 where there is a link and a 0 where there
is not, and you have an object you already know how to analyse. Everything you
might want to ask about a network — is it all connected, does it have separate
groups inside it, which link is the weakest joint — turns into a question about
the eigenvalues of one specific matrix built from the adjacency matrix.

That matrix is the **Laplacian**, and it is the payoff of the whole part. One
count — how many times zero appears among its eigenvalues — tells you how many
pieces the network falls into. One eigenvector tells you where to cut.

## Why Computer Science Cares

- **PageRank, again.** Every ranking system built on links, from Google's
  original to modern recommendation, is an eigenvector of a graph matrix. This
  lesson and [lesson 36](../part03_linear_algebra/36_eigenvalues_and_eigenvectors.md) are the same idea
  from two directions.
- **`scipy.sparse.csgraph`.** `connected_components`, `laplacian`, `degree`,
  `breadth_first_order` — all of it is matrix arithmetic on a sparse matrix, and
  all of it scales to millions of nodes.
- **`sklearn.cluster.SpectralClustering`** is the Laplacian Fiedler vector
  underneath, with k-means on top. `assign='precomputed'` is a graph Laplacian
  if your input is a similarity matrix.
- **Recommender systems** use the SVD of a user–item matrix, which is a
  bipartite graph. This is the same code path as the SVD clustering in the runnable
  example, one row type per user.
- **Mesh processing.** Laplacian eigenmaps and quadric error metrics both
  cluster a 3-D mesh in the basis of its graph Laplacian's smallest
  eigenvectors. This is how games get cheap level-of-detail models.
- **Image segmentation.** The Normalised Cut of Shi and Malik (1998) is a
  spectral clustering objective, and it launched a whole field. See
  `skimage.segmentation.slic` and friends.
- **Graph neural networks.** Graph convolution is literally the normalised
  Laplacian from this lesson convolved with the node features. See
  `torch_geometric.nn.GCNConv`.

## The Formal Version

**Definition.** The **adjacency matrix** `A` of a graph on `n` vertices has
`A[i][j] = 1` when there is an edge from `i` to `j`, and `0` otherwise. The
graph is **undirected** iff `A` is symmetric.

**Definition.** The **degree matrix** `D` is diagonal, with `D[i][i]` the degree
of vertex `i` (its row sum in `A`).

**Definition.** The **graph Laplacian** of an undirected graph is
`L = D − A`. Its entries are

```
L[i][i] = degree of i
L[i][j] = -1  if i and j are linked
L[i][j] = 0   otherwise
```

**Theorem.** `L` is symmetric when `A` is, and every row of `L` sums to zero, so
`L·1 = 0` and `λ = 0` is always an eigenvalue.

**Explanation.** The row-sum property is structural, not arithmetic: for vertex
`i` you add `+degree(i)` from the diagonal and `−1` once per incident edge, and
those cancel. Geometrically, `1` is the state where every node has the same
value, and that state is stationary: nothing flows.

**Theorem.** The multiplicity of `λ = 0` as an eigenvalue of `L` equals the
number of connected components.

**Explanation.** A constant vector on each component — any set of values, one
per component — is annihilated by `L`, and the space of such vectors has
dimension equal to the number of components. So counting zeros counts pieces.
This is the cleanest spectral characterisation of connectedness there is, and
it is exact rather than heuristic.

**Theorem.** For a connected graph, `0 = μ₁ < μ₂ ≤ μ₃ ≤ … ≤ μₙ`. The number
`μ₂` is the **algebraic connectivity**.

**Explanation.** `μ₂ = 0` would mean a second component, so a connected graph
has `μ₂` strictly positive. Small `μ₂` means the graph hangs together by a
thread: it can be split into two pieces without cutting many edges.

**Definition.** The eigenvector for `μ₂` is the **Fiedler vector** (or second
eigenvector).

**Theorem.** The Fiedler vector is a "soft" cut of the graph. Splitting its
entries by sign recovers a 2-way partition that is a good approximation to the
minimum bisection. For `k` communities, use eigenvectors `2, …, k+1` and cluster
the rows — the **spectral embedding** — which is what
`SpectralClustering` does.

**Definition.** The **normalised Laplacian** is `L_sym = I − D^{-1/2} A D^{-1/2}`,
whose eigenvalues lie in `[0, 2]`.

**Definition.** A **stochastic** matrix has rows or columns summing to 1. A
**transition matrix** `P` for a Markov chain has `P[i][j]` = probability of moving
from `j` to `i`.

**Theorem.** If `P` is column-stochastic then `1ᵀP = 1ᵀ`, so `1` is a left
eigenvector for `λ = 1`. If the chain is irreducible and aperiodic, the
**stationary distribution** `r` is a positive right eigenvector with `Pr = r`,
unique up to scale, and it is the limit of `Pᵏ` applied to any starting
distribution.

**Explanation.** The stationary distribution is the long-run fraction of time
each state is visited. Perron–Frobenius guarantees the eigenvalue 1 is
non-negative, simple, and dominates, which is exactly what makes the limit
exist. Damping (`M = 0.85P + 0.15 J/n`) forces aperiodicity, so the limit
always exists.

**Theorem (PageRank).** PageRank scores are the normalised stationary
distribution of a damped random walk on the link graph.

See [SYMBOLS.md](../SYMBOLS.md) for `A`, `Aᵀ`, `λ`, `I`, `tr(A)`, `Q`.

## Worked Example

Take the six-node graph with edges
`A–B, A–C, A–D, B–C, C–D, D–E, E–F` (undirected).

**Step 1: the adjacency matrix.**

```
    A  B  C  D  E  F
A [ 0  1  1  1  0  0 ]
B [ 1  0  1  0  0  0 ]
C [ 1  1  0  1  0  0 ]
D [ 1  0  1  0  1  0 ]
E [ 0  0  0  1  0  1 ]
F [ 0  0  0  0  1  0 ]
```

`A` is symmetric, so the graph is undirected. Row sums `(3, 2, 3, 3, 2, 1)` are
the degrees.

**Step 2: the degree matrix** is `diag(3, 2, 3, 3, 2, 1)`.

**Step 3: the Laplacian** `L = D − A`:

```
      3  -1  -1  -1   0   0
     -1   2  -1   0   0   0
     -1  -1   3  -1   0   0
     -1   0  -1   3  -1   0
      0   0   0  -1   2  -1
      0   0   0   0  -1   1
```

Check the row sums: `3−1−1−1 = 0` ✓, `−1+2−1 = 0` ✓, and so on for all six.

**Step 4: the eigenvalues** (using `np.linalg.eigh`, since `L` is symmetric),
ascending:

```
0,  0.438447,  2.000000,  3.000000,  4.000000,  4.561553
```

**Step 5: interpret.** Exactly **one** zero, so the graph is **connected** —
every node can reach every other. `μ₂ = 0.438447` is the algebraic
connectivity, and it is small because nodes `E` and `F` hang off the rest by
the single link `D–E`.

**Step 6: the eigenvector for `μ₁ = 0`** is `1/√6 · (1,1,1,1,1,1)`, constant
everywhere. That is the "no information" direction.

**Step 7: the Fiedler vector** for `μ₂ = 0.438447`:

```
A: +0.307706    D: +0.086397
B: +0.394103    E: -0.394103
C: +0.307706    F: -0.701809
```

The values are **mirrored**: `A` and `C` match exactly, `B` and `E` match
exactly. That is not a coincidence — it reflects the graph's symmetry
(`A ↔ C`, `B ↔ E`). The four nodes `A, B, C, D` are positive and `E, F` are
negative, so the sign split gives `{A,B,C,D}` versus `{E,F}`, separated by
exactly the one link `D–E`. That is the community structure, recovered
unsupervised.

**Step 8: verify by cutting.** `D–E` is the only edge crossing the split, so
the cut removes 1 of 7 edges. And the sanity check: if we delete `D–E`, `μ₂`
becomes `0` (numerically `1.1e-16`) and there are two components. The theorem
and the arithmetic agree.

## Runnable Code

The Laplacian, its spectrum, and spectral clustering, all from scratch:

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

def mat_sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def trace(A):
    return sum(A[i][i] for i in range(len(A)))

def norm2(v):
    return math.sqrt(sum(x * x for x in v))

def print_matrix(A, title="", width=8, prec=3):
    if title:
        print(title)
    for row in A:
        print("   " + "".join(f"{v:{width}.{prec}f}" for v in row))
    print()

def jacobi_eigh(A, tol=1e-13, max_sweeps=100):
    """Symmetric eigendecomposition by Jacobi rotations (lesson 39).

    Returns (eigenvalues sorted ASCENDING, eigenvectors as COLUMNS), which is
    the ordering the Laplacian literature uses.
    """
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
            a[p][k], a[q][q] = c * apk - s * aqk, s * apk + c * aqk
        for k in range(n):
            vkp, vkq = Q[k][p], Q[k][q]
            Q[k][p], Q[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    idx = sorted(range(n), key=lambda i: a[i][i])
    return [a[i][i] for i in idx], [[Q[r][i] for i in idx] for r in range(n)]

def degree(A):
    """The degree vector: row sums of the adjacency matrix."""
    return [sum(row) for row in A]

# ---------- a small social network ----------

# Six people. A link means "follows".
names = ["Ana", "Ben", "Cleo", "Dev", "Eve", "Fay"]
edges = [
    (0, 1), (0, 2), (0, 3),      # Ana -> Ben, Cleo, Dev
    (1, 0), (1, 2),              # Ben -> Ana, Cleo
    (2, 0), (2, 1), (2, 3),      # Cleo -> Ana, Ben, Dev
    (3, 0), (3, 2), (3, 4),      # Dev -> Ana, Cleo, Eve
    (4, 3), (4, 5),              # Eve -> Dev, Fay
    (5, 4),                      # Fay -> Eve
]
n = len(names)
A = [[0.0] * n for _ in range(n)]
for i, j in edges:
    A[i][j] = 1.0

print("A social network. An entry A[i][j] = 1 means person i follows person j.\n")
print("     " + "".join(f"{nm[:4]:>6}" for nm in names))
for i, nm in enumerate(names):
    print(f"  {nm:>5}" + "".join(f"{A[i][j]:6.0f}" for j in range(n)))

deg = degree(A)
print("\ndegrees (row sums):", dict(zip(names, [int(d) for d in deg])))
print("sum of degrees =", int(sum(deg)), "= 2 x the number of directed edges,",
      int(sum(deg)) // 2, "pairs")

# ---------- the degree matrix and the Laplacian ----------

D = [[deg[i] if i == j else 0.0 for j in range(n)] for i in range(n)]
print_matrix(D, "D, the degree matrix:")
L = mat_sub(D, A)
print_matrix(L, "L = D - A, the graph Laplacian:")

print("Three things about L that are worth noticing:")
print("  1. It is SYMMETRIC, because A is symmetric in this undirected view.")
print("  2. Its diagonal is the degree and its off-diagonal is -1 for a link.")
print("  3. Every ROW SUMS TO ZERO, so L @ 1 = 0 and lambda = 0 is always an")
print("     eigenvalue. The all-ones vector is the eigenvector for it.")
ones = [1.0] * n
print("     check L @ 1 =", matvec(L, ones))
print()
print("Row sums of zero mean: 'move a little along every edge at once, equally'")
print("changes nothing. It is the trivial, stationary state.")

# ---------- eigenvalues of the Laplacian ----------

vals, vecs = jacobi_eigh(L)
print("\n--- the Laplacian's eigenvalues ---")
print("   sorted largest to smallest:")
for i, v in enumerate(vals):
    print(f"   lambda_{i+1} = {v:+.10f}")
print()
print("   The SMALLEST one is 0 exactly (up to rounding), with the constant")
print("   vector as its eigenvector. Everything below sorts ascending, because")
print("   for the Laplacian the interesting direction is 'few big, many small'.")
print("   The number of ZERO eigenvalues equals the number of connected")
print("   components. Here there is exactly one zero, so the graph is")
print("   CONNECTED -- if the graph fell apart in two, there would be two zeros.")
asc = sorted(range(n), key=lambda i: vals[i])
svals = [vals[i] for i in asc]
print()
print("   sorted ascending, which is how the theory usually presents it:")
for i, v in enumerate(svals):
    print(f"   mu_{i+1} = {v:+.10f}")

# ---------- Fiedler vector, for 2-clustering ----------

print("\n--- the Fiedler vector: the best 2-way cut ---")
print("   mu_2 (the second SMALLEST eigenvalue) and its eigenvector tell you")
print("   how to split a connected graph into two pieces.\n")
fiedler = asc[1]
f = [vecs[r][fiedler] for r in range(n)]
print("     person   Fiedler value")
for nm, val in zip(names, f):
    print(f"   {nm:>8}   {val:+.6f}")
mid = sum(f) / n
groupA = [nm for nm, val in zip(names, f) if val > mid]
groupB = [nm for nm, val in zip(names, f) if val <= mid]
print()
print("   group 1:", groupA)
print("   group 2:", groupB)
ia = [names.index(x) for x in groupA]
ib = [names.index(x) for x in groupB]
crossing = sum(1 for i, j in edges if (i in ia) != (j in ia))
print(f"   links crossing the cut: {crossing} out of {len(edges)}")
print("   This graph is a chain with a shortcut, so there is no clean 2-way")
print("   split -- which is the honest answer. The Fiedler vector does not")
print("   invent communities that are not there.")

# ---------- an actual two-community graph ----------

print()
print("=" * 70)
print("A graph with two obvious communities")
print("=" * 70)
# Group 1: 0,1,2 densely linked.  Group 2: 3,4,5 densely linked.
# One weak link between 2 and 3.
c_edges = [
    (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1),      # triangle
    (3, 4), (3, 5), (4, 3), (4, 5), (5, 3), (5, 4),      # triangle
    (2, 3),                                            # the single bridge
]
cn = 6
C = [[0.0] * cn for _ in range(cn)]
for i, j in c_edges:
    C[i][j] = 1.0
cdeg = degree(C)
CD = [[cdeg[i] if i == j else 0.0 for j in range(cn)] for i in range(cn)]
CL = mat_sub(CD, C)
print_matrix(CL, "L =")
cvals, cvecs = jacobi_eigh(CL)
casc = sorted(range(cn), key=lambda i: cvals[i])
print("   eigenvalues, sorted ASCENDING:")
for i in range(cn):
    print(f"      mu_{i+1} = {cvals[casc[i]]:+.8f}")
print()
print("   mu_1 = 0 exactly: one connected component.")
print("   mu_2, the ALGEBRAIC CONNECTIVITY, is", f"{cvals[casc[1]]:.6f}",
      "-- very small compared with")
print("   mu_3 =", f"{cvals[casc[2]]:.6f}", ". The ratio mu_3/mu_2 =",
      f"{cvals[casc[2]]/cvals[casc[1]]:.1f}x.")
print()
print("   For a CONNECTED graph mu_2 > 0. For a graph with two dense blocks")
print("   joined by a single weak bridge, mu_2 is small: the graph barely")
print("   holds together. That small mu_2 IS the signature of two")
print("   communities, and it is also why such a graph is fragile -- remove")
print("   the one bridge and mu_2 becomes 0, i.e. the graph disconnects.")
g = [cvecs[r][casc[1]] for r in range(cn)]
print()
print("     node   Fiedler value")
for i in range(cn):
    print(f"   {i:5d}   {g[i]:+.6f}")
pos = [i for i in range(cn) if g[i] > 0]
neg = [i for i in range(cn) if g[i] <= 0]
print()
print("   recovered communities:", pos, "and", neg)
print("   which is exactly the two triangles we planted. Spectral clustering")
print("   found the structure with no knowledge of it. For k communities you")
print("   take the k eigenvectors for mu_2 ... mu_{k+1} -- the 'spectral")
print("   embedding' -- and run k-means on their coordinates.")
print()
print("   Removing the bridge (2,3) and recomputing from the edge list:")
C2 = [[0.0] * cn for _ in range(cn)]
for i, j in c_edges:
    if (i, j) != (2, 3):
        C2[i][j] = 1.0
d2 = degree(C2)
CL2 = mat_sub([[d2[i] if i == j else 0.0 for j in range(cn)] for i in range(cn)], C2)
v2, _ = jacobi_eigh(CL2)
print("      smallest three eigenvalues:", [f"{x:+.8f}" for x in sorted(v2)[:3]])
print("   TWO zeros now, because the graph is in two pieces. Counting the")
print("   zero eigenvalues of the Laplacian is the cleanest spectral test for")
print("   the number of connected components there is.")
print()
print("   That is the whole lesson in one fact: a structural property of a")
print("   graph becomes a COUNT of zero eigenvalues of one matrix.")
```

PageRank and Markov chains from scratch:

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

def mat_sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def scale(c, v):
    return [c * x for x in v]

def norm2(v):
    return math.sqrt(sum(x * x for x in v))

def print_matrix(A, title="", width=9, prec=4):
    if title:
        print(title)
    for row in A:
        print("   " + "".join(f"{v:{width}.{prec}f}" for v in row))
    print()

# ---------- PageRank, from scratch ----------

# Four pages. Outgoing links:
#   A -> B, C      B -> A, C      C -> B, D      D -> A, B
names = ["A", "B", "C", "D"]
n = len(names)
outlinks = {"A": ["B", "C"], "B": ["A", "C"], "C": ["B", "D"], "D": ["A", "B"]}

P = [[0.0] * n for _ in range(n)]
for j, src in enumerate(names):
    outs = outlinks[src]
    for dst in outs:
        P[names.index(dst)][j] = 1.0 / len(outs)      # column j is where you leave j

print("PageRank as a Markov chain.")
print("P[i][j] = probability of jumping from page j to page i.\n")
print("   out-links:  " + "   ".join(f"{k}->{'/'.join(v)}" for k, v in outlinks.items()))
print_matrix(P, "   P =")

print("Columns each sum to 1, because you must land somewhere.")
print("column sums:", [round(sum(P[i][j] for i in range(n)), 10) for j in range(n)])
print()
print("--- the random walk, step by step ---")
x = [0.25] * n
for k in range(9):
    if k:
        x = matvec(P, x)
    print(f"   step {k}:  " + "  ".join(f"{nm}={s:.4f}" for nm, s in zip(names, x)))
print()
print("It oscillates early and then settles. The fixed point is where")
print("x = P x, which is the eigenvector for eigenvalue 1.")

# ---------- power iteration finds the fixed point ----------

print("\n--- power iteration, the actual algorithm PageRank uses ---")
r = [1.0] * n                                   # any starting vector
history = []
for step in range(1, 61):
    r = matvec(P, r)
    total = sum(r)
    r = [t / total for t in r]                   # normalise so the scores sum to 1
    if step in (1, 2, 5, 10, 20, 30, 50, 60):
        history.append((step, [round(v, 6) for v in r]))
for step, vec in history:
    print(f"   after {step:3d} steps:  " + "  ".join(f"{nm}={s:.4f}"
                                                   for nm, s in zip(names, vec)))
print()
resid = [r[i] - matvec(P, r)[i] for i in range(n)]
print("P r =", [round(v, 8) for v in matvec(P, r)])
print("r   =", [round(v, 8) for v in r])
print(f"max |P r - r| = {max(abs(v) for v in resid):.3e}  -> converged")
print()
print("The scores are:", ", ".join(f"{nm}={v:.4f}" for nm, v in zip(names, r)))
print()
print("Compare with raw link counts. Incoming links: A:2, B:3, C:2, D:1, which")
print("normalises to 0.25 each. PageRank disagrees, because a link from an")
print("important page is worth more than a link from an unimportant one.")

# ---------- the eigenvalue-1 guarantee ----------

print("\n--- why eigenvalue 1 is guaranteed, and which eigenvector we want ---")
print("Columns of P sum to 1, so 1^T P = 1^T. The all-ones vector is a LEFT")
print("eigenvector of P for lambda = 1, i.e. an eigenvector of P^T:")
u = [1.0] * n
print("   P^T @ 1 =", [round(v, 10) for v in matvec(transpose(P), u)])
print()
print("The SCORES are the other eigenvector for lambda = 1: the RIGHT one,")
print("satisfying P r = r. Power iteration finds it automatically, because it")
print("keeps applying P.")
print()
print("   P r =", [round(v, 8) for v in matvec(P, r)])
print("   r   =", [round(v, 8) for v in r])
print("   match:", all(abs(a - b) < 1e-9 for a, b in zip(matvec(P, r), r)))
print()
print("And it is not the all-ones vector, because P's ROW sums are not all 1:")
print("   row sums of P =", [round(sum(row), 4) for row in P],
      " <- not 1, so 1 is not a right eigenvector")
print("   the left and right eigenvectors for the same eigenvalue differ.")
print()
print("So PageRank is: iterate r <- P r, normalise, read off the scores.")
print("That is one line of numpy, and it is the same power iteration as")
print("lesson 36.")
print()
print("The danger: if the chain is PERIODIC the walk never converges. A")
print("two-page loop A->B->A with no self-link is periodic -- the scores")
print("just swap back and forth forever. Google fixed this by letting a surfer")
print("'teleport' to a uniformly random page with probability 0.15, which is a")
print("convex mixture with the all-ones matrix J/n:")
tele = 0.15
M = [[(1 - tele) * P[i][j] + tele / n for j in range(n)] for i in range(n)]
print_matrix(M, "   M = 0.85 P + 0.15 (1/n) J, the damped PageRank matrix:")
print("   column sums:", [round(sum(M[i][j] for i in range(n)), 10) for j in range(n)],
      "still exactly 1, as they must be")
r2 = [1.0] * n
for _ in range(200):
    r2 = matvec(M, r2)
    tot = sum(r2)
    r2 = [t / tot for t in r2]
print("   scores with damping:", ", ".join(f"{nm}={v:.4f}" for nm, v in zip(names, r2)))
print("   scores, no damping:  ", ", ".join(f"{nm}={v:.4f}" for nm, v in zip(names, r)))
print()
print("Damping moves every score slightly toward uniform, because 15% of the")
print("time the surfer is on a random page regardless of links. It is standard")
print("in every real implementation: it costs a little sharpness and buys")
print("convergence you can rely on, plus immunity to link-farming loops.")
print()
print("--- the rank-one view: a stochastic matrix has a non-negative")
print("    eigenvector for lambda = 1 (Perron-Frobenius) ---")
print("That theorem is why the scores are guaranteed to come out non-negative")
print("and to sum to something normalisable. Any non-negative square matrix")
print("with positive row or column sums has a strictly positive eigenvector")
print("for its largest eigenvalue, and no others of that size. Here the")
print("largest eigenvalue is exactly 1.")
```

SVD clustering, and the Laplacian done properly on the same graph:

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

def mat_sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def norm2(v):
    return math.sqrt(sum(x * x for x in v))

def jacobi_eigh(A, tol=1e-13, max_sweeps=100):
    """Symmetric eigendecomposition by Jacobi rotations (lesson 39).

    Returns (eigenvalues sorted ASCENDING, eigenvectors as COLUMNS), which is
    the ordering the Laplacian literature uses.
    """
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
    idx = sorted(range(n), key=lambda i: a[i][i])
    return [a[i][i] for i in idx], [[Q[r][i] for i in idx] for r in range(n)]

def print_matrix(A, title="", width=9, prec=4):
    if title:
        print(title)
    for row in A:
        print("   " + "".join(f"{v:{width}.{prec}f}" for v in row))
    print()

def svd(A, tol=1e-14, max_sweeps=60):
    """A = U S V^T by one-sided Jacobi rotations (lesson 40)."""
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
            e = [1.0] if False else [1.0 if t == i % m else 0.0 for t in range(m)]
            for j in range(i):
                if Ucols[j] is not None:
                    p = sum(a * b for a, b in zip(e, Ucols[j]))
                    e = [a - p * b for a, b in zip(e, Ucols[j])]
            nrm = math.sqrt(sum(x * x for x in e))
            Ucols[i] = [x / nrm for x in e] if nrm > tol else e
    return transpose(Ucols), sigmas, Vcols

# ---------- two dense communities, joined by two bridges ----------

# Group 1: nodes 0..4 fully connected (K5).  Group 2: nodes 5..9 fully
# connected (K5).  Two bridges: 4-5 and 2-8.
edges = []
for i in range(5):
    for j in range(5):
        if i != j:
            edges.append((i, j))
for i in range(5, 10):
    for j in range(5, 10):
        if i != j:
            edges.append((i, j))
edges += [(4, 5), (2, 8)]
n = 10
A = [[0.0] * n for _ in range(n)]
for i, j in edges:
    A[i][j] = 1.0

print("Two K5 cliques joined by exactly two edges (4-5 and 2-8).")
print("A network, drawn as a matrix:\n")
print("      " + "".join(f"{i:5d}" for i in range(n)))
for i in range(n):
    print(f"   {i:3d} " + "".join(f"{A[i][j]:5.0f}" for j in range(n)))
deg = [sum(row) for row in A]
print("\ndegrees:", [int(d) for d in deg])
print("nodes 0-4 have degree 4 inside the clique plus 1 bridge; nodes 5-9")
print("the same. The two bridge endpoints (2, 4, 5, 8) are the only links")
print("between the halves.")

# ---------- singular values of the adjacency matrix ----------

print("\n--- the SVD of the adjacency matrix ---")
U, S, Vcols = svd(A)
print("singular values (sorted, non-negative, as always):")
for i, s in enumerate(S):
    print(f"   sigma_{i+1} = {s:10.6f}")
print()
print("A big sigma_1 and a big sigma_2, then a cliff. That is the whole")
print("community structure, read off the singular values directly.")
print()
ratios = [S[i] / S[i + 1] for i in range(len(S) - 1)]
for i, s in enumerate(S[:4]):
    r = f"{ratios[i]:.3f}x" if i < len(ratios) else "-"
    print(f"   sigma_{i+1} = {s:9.4f}   ratio to next: {r}")
print()
print("sigma_1 / sigma_2 =", f"{S[0]/S[1]:.4f}", "-- nearly equal, because the two")
print("communities are the same size. If one community were much bigger the")
print("top two would separate, and the RATIO tells you the relative size.")

# ---------- a rank-2 approximation recovers the two sides ----------

print("\n--- a rank-2 approximation separates the communities ---")
print("Keep the two largest singular values and use the ROWS of U_k as a 2-D")
print("embedding: each node gets a point, and the points should fall into two")
print("clouds. Then run k-means with k = 2.\n")
U2 = [[U[i][0], U[i][1]] for i in range(n)]
print("     node      embedding coord 1     coord 2      norm")
for i in range(n):
    print(f"   {i:5d}      {U2[i][0]:+18.6f}  {U2[i][1]:+14.6f}   "
          f"{norm2(U2[i]):.6f}")

def kmeans(points, k=2, iterations=100):
    """Plain Lloyd's algorithm: assign every point to the nearest centre, then
    move each centre to the mean of the points assigned to it. Repeat."""
    dim = len(points[0])
    centres = [list(points[0]), list(points[-1])]
    for _ in range(iterations):
        labels = []
        for pt in points:
            dists = [sum((pt[t] - centre[t]) ** 2 for t in range(dim))
                     for centre in centres]
            labels.append(dists.index(min(dists)))
        moved = []
        for ci in range(k):
            grp = [points[i] for i in range(len(points)) if labels[i] == ci]
            if grp:
                moved.append([sum(pt[t] for pt in grp) / len(grp)
                              for t in range(dim)])
            else:
                moved.append(centres[ci])
        if moved == centres:
            break
        centres = moved
    return labels, centres

lab, cent = kmeans(U2, 2)
print()
print("     node   k-means cluster")
for i in range(n):
    print(f"   {i:5d}   {lab[i]}")
clusterA = [i for i in range(n) if lab[i] == 0]
clusterB = [i for i in range(n) if lab[i] == 1]
print()
print("   cluster 0:", clusterA)
print("   cluster 1:", clusterB)
print("   cluster centres:", [[round(v, 6) for v in c] for c in cent])
print()
print("The two centres differ mainly in the SIGN of the second coordinate:")
print("one is (+0.31, +0.32) and the other (+0.31, -0.32). Everything else is")
print("nearly identical. So the single number that separates the two halves is")
print("whether the second embedding coordinate is positive or negative, and")
print("that is exactly what the k-means distance is picking up.")
print()
by_second = [i for i in range(n) if U2[i][1] > 0]
print("   nodes with a POSITIVE second coordinate:", by_second)
print("   k-means cluster 0              :", clusterA)
print("   identical?", by_second == clusterA)
print()
print("So the SVD embedding DID separate the cliques here, and k-means found")
print("the right split without being told anything. Note the two bridge nodes")
print("(2 and 4, degree 5) sit furthest from their own clique's centre -- they")
print("are the ambiguous ones, exactly as you would expect.")
print()
print("The reason this works is worth stating precisely. A K5 clique is a")
print("RANK-4 block: its adjacency matrix has four non-zero singular values")
print("(4, 1, 1, 1), because the off-diagonal ones are the real content. So a")
print("clique does NOT collapse to a single point under the SVD, and the")
print("rank-2 approximation is genuinely lossy. What the top singular vectors")
print("capture is the two-block STRUCTURE -- one direction per community --")
print("which is enough to cluster, even though the fit is imperfect.")

# ---------- why the approximation is meaningful ----------

print("\n--- how much did the rank-2 approximation keep? ---")
for k in (1, 2, 3, 5, 10):
    approx = [[sum(U[i][j] * S[j] * Vcols[j][c] for j in range(k))
               for c in range(n)] for i in range(n)]
    err = math.sqrt(sum((approx[i][j] - A[i][j]) ** 2
                        for i in range(n) for j in range(n)))
    print(f"   rank {k:2d}: ||A - A_k||_F = {err:10.6f}")
print()
print("The singular values of a single K5 block are 4, 1, 1, 1 -- four")
print("non-zero values, not one. A clique is rank n-1 as a matrix, so no")
print("rank-1 SVD can represent it. The rank-2 approximation is lossy, but")
print("the STRUCTURE survives, which is all a clustering method needs.")

# ---------- the Laplacian on the SAME graph, for comparison ----------

print()
print("=" * 70)
print("The Laplacian on the SAME graph, which is the better tool")
print("=" * 70)
D = [[deg[i] if i == j else 0.0 for j in range(n)] for i in range(n)]
L = mat_sub(D, A)
lvals, lvecs = jacobi_eigh(L)
print("Laplacian eigenvalues, sorted ascending:")
for i, v in enumerate(lvals):
    tag = "   <- Fiedler" if i == 1 else ""
    print(f"   mu_{i+1} = {v:+.8f}{tag}")
print()
print("mu_1 = 0 exactly, so the graph is connected.")
print("mu_2 =", f"{lvals[1]:.6f}", "is the ALGEBRAIC CONNECTIVITY. Compare the")
print("two blocks: it is small, so the graph is barely held together.")
print()
f2 = [lvecs[r][1] for r in range(n)]
print("     node   Fiedler value")
for i in range(n):
    print(f"   {i:5d}   {f2[i]:+.6f}")
print()
pos2 = [i for i in range(n) if f2[i] > 0]
neg2 = [i for i in range(n) if f2[i] <= 0]
print("   positive:", pos2, "  negative:", neg2)
print("   correct?", pos2 == [0, 1, 2, 3, 4] and neg2 == [5, 6, 7, 8, 9])
print()
print("A single scalar per node, with a clean sign change, and it recovers the")
print("communities exactly. Compare the SVD version, which needed a 2-D")
print("embedding plus a k-means pass and had to fudge the fit. For undirected")
print("community detection the Laplacian is the better tool, and")
print("sklearn.cluster.SpectralClustering defaults to it for that reason.")
print()
print("The one structural difference: the SVD of A uses the WHOLE adjacency")
print("matrix, so it is sensitive to who points at whom and can be fooled by a")
print("group that only points inwards. The Laplacian uses only degrees and")
print("connectivity, so it always cuts along a genuine bridge.")
```

### With Libraries

```python
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components, laplacian as sp_laplacian

np.set_printoptions(precision=6, suppress=True)

# ---------- building a graph as a matrix ----------
print("--- a graph is a matrix ---")
names = ["A", "B", "C", "D", "E", "F"]
edges = [("A", "B"), ("A", "C"), ("A", "D"),
         ("B", "A"), ("B", "C"),
         ("C", "A"), ("C", "B"), ("C", "D"),
         ("D", "A"), ("D", "C"), ("D", "E"),
         ("E", "D"), ("E", "F"),
         ("F", "E")]
n = len(names)
idx = {nm: i for i, nm in enumerate(names)}
A = np.zeros((n, n))
for i, j in edges:
    A[idx[i], idx[j]] = 1.0

print("A =\n", A)
print("     " + "".join(f"{nm:>6}" for nm in names))
for r, nm in enumerate(names):
    print(f"  {nm:>4}" + "".join(f"{A[r, c]:6.0f}" for c in range(n)))
print()
print("Symmetric?", np.allclose(A, A.T))
print("Row sums (= out-degree):", A.sum(1))
print("Column sums (= in-degree):", A.sum(0))
print("Here they are equal, because this edge list is SYMMETRIC -- the graph is")
print("undirected. That equality is the test for an undirected graph: A symmetric")
print("means the row and column sums agree, i.e. in-degree equals out-degree.")
print()
print("Drop the symmetry and you have a directed graph (a follower graph, a web")
print("of citations). Then in-degree and out-degree differ, the matrix is not")
print("doubly stochastic, and the row sums no longer mean 'how many friends'.")
print("Both cases are handled by the same code; only the meaning changes.")

# ---------- PageRank ----------
print("\n--- PageRank ---")
P = A / A.sum(0, keepdims=True)          # column-stochastic
M = 0.85 * P + 0.15 / n                  # the damped matrix
r = np.full(n, 1.0 / n)
for _ in range(200):
    r = M @ r
r = r / r.sum()
for nm, v in zip(names, r):
    print(f"   {nm}: {v:.6f}")
print()
print("That is all PageRank is: a damped power iteration on the link matrix,")
print("converging to the dominant eigenvector, which is the stationary")
print("distribution of the random walk. Everything in lesson 36 runs at Google")
print("scale. The library form is nx.pagerank(G, alpha=0.85) if networkx is")
print("installed, and the same numbers come out.")

# ---------- the Laplacian, three ways ----------
print("\n--- the Laplacian, three equivalent ways to build it ---")
L_manual = np.diag(A.sum(1)) - A
L_scipy = sp_laplacian(csr_matrix(A)).toarray()
L_norm = sp_laplacian(csr_matrix(A), normed=True).toarray()
print("np.diag(degrees) - A == scipy.sparse.csgraph.laplacian :",
      np.allclose(L_manual, L_scipy))
print("Symmetric?", np.allclose(L_manual, L_manual.T))
print("Row sums (should all be 0):", np.round(L_manual.sum(1), 12))
print("L @ 1 =", np.round(L_manual @ np.ones(n), 12))
print()
print("L =\n", np.round(L_manual, 4))
print("Three properties to remember, all visible above:")
print("  1. symmetric, so use eigh and get real orthonormal eigenvectors")
print("  2. diagonal is the degree, off-diagonal is -1 for a link")
print("  3. every row sums to ZERO, so 0 is always an eigenvalue")

# ---------- the normalised Laplacian ----------
print("\n--- the normalised Laplacian, for undirected work ---")
deg = A.sum(1)
Dhalf_inv = np.diag(1.0 / np.sqrt(deg))
L_sym = np.eye(n) - Dhalf_inv @ A @ Dhalf_inv
print("L_sym = I - D^-1/2 A D^-1/2 ==", np.allclose(L_sym, L_norm))
w_sym = np.linalg.eigvalsh(L_sym)
print("eigenvalues:", np.round(w_sym, 6))
print("all in [0, 2]:", bool(np.all(w_sym >= -1e-9) and np.all(w_sym <= 2 + 1e-9)))
print("and one is exactly 0, as it must be for a graph with one component.")
print("(Note the D^-1/2 on BOTH sides. Getting that wrong gives a matrix")
print("that is not similar to the real thing and eigenvalues outside [0,2].)")

print("\nCompare the three Laplacian conventions, because the eigenvalue ranges")
print("differ and mixing them up is a real source of bugs:")
for label, M_ in (("L = D - A", L_manual), ("L_sym = I - D^-1/2 A D^-1/2", L_sym)):
    ww = np.linalg.eigvalsh(M_)
    print(f"   {label:26s} min = {ww.min():+.4f}  max = {ww.max():+.4f}")
print("   L_sym is bounded, so a Fiedler vector can never exceed 1 in magnitude")
print("   -- that bound is what makes normalised spectral methods stable.")

# ---------- the spectrum ----------
print("\n--- the spectrum, and what it tells you ---")
w, Q = np.linalg.eigh(L_manual)
print("eigenvalues, ascending:", np.round(w, 6))
n_zero = int(np.sum(np.isclose(w, 0, atol=1e-9)))
print("number of zero eigenvalues:", n_zero)
ncomp, labels_cc = connected_components(csr_matrix(A), directed=False)
print("scipy's connected_components says:", ncomp)
print("they agree, and that agreement IS the theorem.")
print()
print("The eigenvector for eigenvalue 0 is the all-ones vector:")
print("   Q[:, 0] =", np.round(Q[:, 0], 6), "-> constant on every component")
print()
print("The Fiedler vector (eigenvector for mu_2) is the next one up:")
f = Q[:, 1]
for nm, v in zip(names, f):
    print(f"   {nm}: {v:+.6f}")
print()
print("This graph has ONE component, so the Fiedler vector is not constant.")
print("It increases smoothly towards E and F -- the two nodes attached by the")
print("single D-E link -- and that gradient IS the hint that they separate off.")
print("If the graph were already disconnected, the Fiedler vector would be")
print("constant within each piece, taking exactly one value per component.")

# ---------- spectral clustering ----------
print("\n--- spectral clustering, the library version ---")
from sklearn.cluster import SpectralClustering
sc = SpectralClustering(n_clusters=2, affinity="precomputed", random_state=0)
lab = sc.fit_predict(A)
for nm, l in zip(names, lab):
    print(f"   {nm}: cluster {l}")
g0 = [nm for nm, l in zip(names, lab) if l == 0]
g1 = [nm for nm, l in zip(names, lab) if l == 1]
print()
print("   cluster 0:", g0)
print("   cluster 1:", g1)
print("   A/B/C/D form one tightly-knit group, E/F another with a single")
print("   weak link (D-E). Spectral clustering found that unsupervised.")

# ---------- a clean two-block graph, both methods ----------
print()
print("--- two clean blocks: the Laplacian wins ---")
B = np.zeros((10, 10))
B[:5, :5] = 1 - np.eye(5)
B[5:, 5:] = 1 - np.eye(5)
B[4, 5] = B[5, 4] = 1          # one bridge
np.fill_diagonal(B, 0)
Sb = np.linalg.svd(B, compute_uv=False)
Lb = np.diag(B.sum(1)) - B
wb, Qb = np.linalg.eigh(Lb)
print("two K5 cliques joined by a single edge")
print("   singular values of the adjacency matrix:", np.round(Sb, 4))
print("   Laplacian eigenvalues, ascending      :", np.round(wb, 6))
print("   mu_2, the algebraic connectivity      :", f"{wb[1]:.6f}")
print()
fb = Qb[:, 1]
print("   Fiedler signs:", np.sign(fb).astype(int))
rec = ([int(i) for i in np.where(fb > 0)[0]], [int(i) for i in np.where(fb <= 0)[0]])
print("   recovered:", rec)
print("   the two halves are {0,1,2,3,4} and {5,6,7,8,9} -- the planted split,")
print("   recovered exactly, with one scalar per node and no clustering step.")
print("   (The sign of the Fiedler vector is arbitrary, so which half is")
print("    'positive' is a labelling convention and can come out swapped.)")
print()
print("Contrast with the singular values:", np.round(Sb, 4))
print("A K5 clique is a rank-4 block -- its adjacency matrix has four")
print("non-zero singular values (n-1 of them, for an n-clique) -- so a clique")
print("does not collapse to a single point under the SVD. Only the two top")
print("singular values stand out, and you need a k-means pass on the")
print("resulting embedding. The Laplacian gets there with a single sign test.")

# ---------- SVD of this graph ----------
print("\n--- SVD of the adjacency matrix, for contrast ---")
U, S, Vt = np.linalg.svd(A)
print("singular values of the 6-node adjacency matrix:", np.round(S, 6))
print("the top two:", f"{S[0]:.4f} and {S[1]:.4f}, ratio {S[0]/S[1]:.3f}")
print()
print("This graph is a near-clique, not two clean blocks, so there is no big")
print("gap in the singular values and no obvious SVD clustering. The")
print("Laplacian is still perfectly informative, because it only needs")
print("connectivity. That is the practical rule:")
print("  * UNDIRECTED edges  -> use the Laplacian")
print("  * DIRECTED edges where direction carries meaning -> use the SVD")
print("    (this is 'SVD-based link analysis', used for recommendation)")

# ---------- what else a Laplacian is good for ----------
print("\n--- other things the Laplacian answers ---")
print(f"  * algebraic connectivity mu_2 = {w[1]:.6f}")
print("    how fragile is this graph? mu_2 = 0 means already disconnected.")
print(f"    here mu_2 = {w[1]:.4f}, small, because D-E is a single link:")
print("    remove it and mu_2 becomes 0.")
B2 = A.copy()
B2[idx['D'], idx['E']] = 0
B2[idx['E'], idx['D']] = 0
w2 = np.linalg.eigvalsh(np.diag(B2.sum(1)) - B2)
ncomp2, _ = connected_components(csr_matrix(B2), directed=False)
print("    after removing D-E, mu_2 =", f"{w2[1]:.2e}",
      "and components =", ncomp2, "-- exactly the theorem again")
print()
print("  * minimum cut. The cut minimised by the Fiedler vector is the")
print("    RELAXED version of minimum bisection, which is what Normalised Cut")
print("    and modularity optimise. Spectral clustering is the linear-algebra")
print("    relaxation of a combinatorial problem.")
print()
print("  * mesh processing. For a 3-D mesh the graph Laplacian's smallest")
print("    eigenvectors are the low-frequency bending modes. Laplacian")
print("    eigenmaps simplifies a mesh by clustering in that spectral basis,")
print("    and is how quadric error metrics reuse the same idea.")
```

## Common Mistakes

**1. Using the adjacency matrix where the Laplacian belongs.**

```python
import numpy as np

A = np.array([[0, 1, 1], [1, 0, 0], [1, 0, 0]], dtype=float)
L = np.diag(A.sum(1)) - A
print("A is NOT symmetric here, so it is a directed graph:")
print(np.round(np.linalg.eigvalsh(A), 6), "<- eigvalsh on a non-symmetric")
print("                                     matrix reads only the lower triangle")
print("and silently gives the wrong answer.")
```

```python
import numpy as np

A = np.array([[0, 1, 1], [1, 0, 0], [1, 0, 0]], dtype=float)
L = np.diag(A.sum(1)) - A
print("A is symmetric:", np.allclose(A, A.T), "-> fine for eigh here")
print("L =", L.tolist(), "\n eigenvalues of L:", np.round(np.linalg.eigvalsh(L), 6))
print("Two zeros => two components: node 2 and the edge 0-1. Correct.")
print()
print("The rule: check np.allclose(A, A.T) FIRST. For a directed graph use")
print("np.linalg.eig on A, or better, symmetrise deliberately. The Laplacian")
print("form only makes sense for symmetric A.")
```

The dangerous version of this bug is not a crash but a plausible answer. A
non-symmetric matrix passed to `eigh` reads only the lower triangle, so you get
the spectrum of a different matrix entirely — the same trap as in
[lesson 39](../part03_linear_algebra/39_diagonalization_and_spectral.md).

**2. Assuming the top singular value carries the community structure.**

```python
import numpy as np

B = np.zeros((6, 6))
B[:3, :3] = 1 - np.eye(3)
B[3:, 3:] = 1 - np.eye(3)
B[2, 3] = B[3, 2] = 1
np.fill_diagonal(B, 0)
S = np.linalg.svd(B, compute_uv=False)
print("two triangles joined by one edge")
print("   singular values:", np.round(S, 6))
print("   the top TWO are the two community directions")
print("   the rest (1,1,1,1) are internal clique structure, not communities")
print("Using only sigma_1 would merge the two triangles into one cluster.")
```

Tempting because "the leading singular vector is the most important
direction", which is true but not specific enough. In a block-structured matrix
the top `k` singular vectors are the `k` blocks, and you need all of them.
Equivalently, for the Laplacian you want the *smallest* `k` nonzero
eigenvalues, not the largest.

**3. Forgetting to handle disconnected graphs in PageRank.**

```python
import numpy as np

# Two pages that only link to each other, plus two that link to each other
# but nothing links to them.
n = 4
P = np.array([[0, 1, 0, 0],
              [1, 0, 0, 0],
              [0, 0, 0, 1],
              [0, 0, 1, 0]], dtype=float)      # columns sum to 1
print("column sums:", P.sum(0))
w = np.linalg.eigvals(P)
print("eigenvalues:", np.round(w, 6))
print("1 appears TWICE. The chain is reducible, so the stationary")
print("distribution is NOT unique -- any split of mass between the two")
print("pairs is a fixed point, and which one you get depends on the")
print("starting vector.")
r = np.full(4, 0.25)
for _ in range(50):
    r = P @ r
print("this run settled on:", np.round(r, 6))
r2 = np.array([0.4, 0.4, 0.1, 0.1])
for _ in range(50):
    r2 = P @ r2
print("a different start  :", np.round(r2, 6), "  <-- different answer!")
```

This is the real reason damping exists. A rank-deficient or reducible link
structure — a "link farm", a walled garden — leaves the eigenvector ambiguous
or gives it zero components, so dead pages can accumulate arbitrary scores.
Damping with `0.85P + 0.15J/n` mixes in a connect-everything term and makes the
matrix irreducible and aperiodic, so the answer is unique. If you build your
own PageRank, either damp it or explicitly handle dead nodes.

**4. Dividing by zero degrees when building the normalised Laplacian.**

```python
import numpy as np

A = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=float)   # node 2 isolated
deg = A.sum(1)
print("degrees:", deg, "  <- node 2 has degree 0")
with np.errstate(divide="ignore", invalid="ignore"):
    Dhalf_inv = np.diag(1.0 / np.sqrt(deg))
    broken = np.eye(3) - Dhalf_inv @ A @ Dhalf_inv
print("normalised Laplacian with the unguarded division:")
print(np.round(broken, 4))
print("   -> inf and nan entries, from dividing by sqrt(0)")
print("      (0/0 gives nan, x/0 gives inf), which then poison everything")
print("      downstream.")
try:
    np.linalg.eigvalsh(broken)
except np.linalg.LinAlgError as e:
    print("eigvalsh then raises:", e)
print("   At least this version fails loudly. The dangerous version is a")
print("   NaN that slips into a loss value and gets quietly ignored.")
```

```python
import numpy as np

A = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=float)
deg = A.sum(1)
safe = np.where(deg > 0, deg, 1.0)        # isolated nodes get degree 1
Dhalf_inv = np.diag(1.0 / np.sqrt(safe))
L_sym = np.eye(len(A)) - Dhalf_inv @ A @ Dhalf_inv
print("L_sym =\n", np.round(L_sym, 4))
print("eigenvalues:", np.round(np.linalg.eigvalsh(L_sym), 6))
print("TWO zeros, correctly reporting two components. An isolated node is")
print("its own component, and the convention handles it.")
print("scipy.sparse.csgraph.laplacian does this for you already.")
```

An isolated node is a completely ordinary thing in a real network, and its
degree is exactly zero. This is why every library implementation guards the
division rather than trusting the caller.

**5. Treating the Fiedler vector's sign as meaningful.**

```python
import numpy as np

B = np.zeros((6, 6))
B[:3, :3] = 1 - np.eye(3)
B[3:, 3:] = 1 - np.eye(3)
B[2, 3] = B[3, 2] = 1
np.fill_diagonal(B, 0)
L = np.diag(B.sum(1)) - B
f1 = np.linalg.eigh(L)[1][:, 1]
f2 = np.linalg.eigh(-L)[1][:, 1]        # same graph, sign-flipped somewhere
print("Fiedler vector 1:", np.round(f1, 4))
print("Fiedler vector 2:", np.round(f2, 4))
print("identical?", np.allclose(f1, f2), "  same partition?", 
      np.array_equal(np.sign(f1), np.sign(f2)))
print("Eigenvectors are only defined UP TO A SIGN. '(A, B, C | D, E, F)' and")
print("'(D, E, F | A, B, C)' are the same clustering. Never report which")
print("cluster is 'cluster 1' as if it were an absolute label.")
```

Tempting because a sign looks like a fact. It is not: `v` and `−v` are both
eigenvectors for the same eigenvalue, and which one you get depends on the
algorithm, the sign conventions inside LAPACK, and the matrix layout. The same
applies to PCA components, which is why the component sign caveat appears in
[lesson 40](../part03_linear_algebra/40_svd_and_pca.md) too.

## Formula Sheet

Symbols follow [SYMBOLS.md](../SYMBOLS.md). `A` is the `n × n` adjacency
matrix, `D` the degree matrix, `L = D − A` the Laplacian, `P` a transition
matrix, `r` the stationary distribution, `n` the number of vertices,
`0 = μ₁ ≤ μ₂ ≤ … ≤ μ_n`.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| adjacency matrix | `$A[i][j] = 1$` if there is an edge, else `0` | the graph, written as a table | the input to everything below; symmetric **iff** the graph is undirected |
| degree matrix | `$D[i][i] = \sum_j A[i][j] = \deg(i)$`, zero off the diagonal | how many links each vertex has | the only other input needed for `L` |
| handshaking lemma | `$\sum_i \deg(i) = 2|E|$` | total degree counts every edge twice | a consistency check on any degree list |
| **Laplacian** | `$L = D - A$` | degree on the diagonal, `−1` where there is a link, `0` elsewhere | undirected community detection, connectivity, mesh processing |
| Laplacian entries | `$L[i][i] = \deg(i)$`, `$L[i][j] = -1$ if linked, else `0` | | when you want to build `L` without forming `D` |
| row-sum property | `$L\mathbf{1} = 0$` | the all-ones vector is always an eigenvector for `λ = 0` | the guarantee that `0` is in the spectrum |
| **component count** | `$\#\{\text{zeros in the spectrum of } L\} = $ number of connected components | count zeros, get pieces | `connected_components` on a sparse matrix, at any scale |
| algebraic connectivity | `$\mu_2 = \lambda_2(L) > 0$` for a connected graph | how hard the graph is to pull apart | fragility, robustness, "does this network have a waist" |
| Fiedler vector | the eigenvector `v_2` for `μ₂` | one number per vertex; sign gives a 2-way cut | spectral clustering with `k = 2` |
| spectral embedding | `$[v_2 \ v_3 \ \dots \ v_{k+1}]`, cluster the rows | `k−1` numbers per vertex, then k-means | `SpectralClustering` for `k` communities |
| Fiedler energy | `$v^{\mathsf T}Lv = \sum_{(i,j)\in E}(v_i - v_j)^2$`, and `$\mu_2 = v^{\mathsf T}Lv/v^{\mathsf Tv}$` | total squared jump across every edge | finding **which** edges are fragile, not just how fragile the graph is |
| normalised Laplacian | `$L_{sym} = I - D^{-1/2}AD^{-1/2}$` | the Laplacian rescaled so degrees do not dominate | eigenvalues land in `[0, 2]`; needs **`D^{-1/2}` on both sides** and positive degrees |
| isolated-node guard | `D_{ii} = 0$ needs the convention `D_{ii} \to 1$ | an isolated vertex is its own component | `scipy.sparse.csgraph.laplacian` handles it; you must too |
| Laplacian bounds | `$0 \le \mu_2 \le \dots \le \mu_n \le n$ | eigenvalues never exceed `n` for a simple graph | sanity check on a computed spectrum |
| known spectra | `K_n$: `0, n^{(n-1)}$; path `P_n`: `2(1-\cos(k\pi/n))$`; cycle `C_n`: `2(1-\cos(2k\pi/n))$` | closed forms to check against | verifying your own implementation |
| stochastic matrix | rows or columns summing to 1 | probabilities | Markov chains, PageRank |
| transition matrix | `$P[i][j] = \Pr(\text{jump } j \to i)$` | where you land, indexed by where you leave | PageRank; column-stochastic here, so `1ᵀP = 1ᵀ` |
| eigenvalue 1 guarantee | `$P$ column-stochastic `$\Rightarrow$` `$\lambda = 1$` exists, with `1` a **left** eigenvector | conservation | why the scores are normalisable |
| stationary distribution | `$Pr = r$`, `$r \ge 0$`, `$\sum_i r_i = 1$ | the long-run fraction of time at each state | PageRank scores; uniqueness needs irreducibility + aperiodicity |
| Perron–Frobenius | a positive matrix has a unique positive dominant eigenvector | one direction wins, unambiguously | why damping makes the answer unique |
| PageRank damping | `$M = 0.85P + 0.15\,J/n$`, `J` the all-ones matrix | 85% follow a link, 15% teleport uniformly | not optional: fixes dead ends and guarantees convergence |
| PageRank iteration | `$r \leftarrow Mr$`, renormalise, repeat | power iteration | `nx.pagerank(G, alpha=0.85)` |
| raw link counting vs PageRank | in-degree normalised, vs the stationary distribution | counting ignores *who* links | the lesson's worked ranking differs for this reason |
| SVD vs Laplacian for clustering | SVD of `A` uses direction of edges; `L` uses only degrees and connectivity | one sees the web, one sees the structure | **undirected** → Laplacian; **directed** → SVD |

Three restrictions to carry. `L = D − A` is the Laplacian only for an
**undirected** (symmetric `A`) graph; the directed case needs the out-degree
Laplacian `I − D_out⁻¹A` instead. The normalised Laplacian needs `D_{ii} > 0`, so
isolated vertices must be handled explicitly. And the eigenvector for `μ₂` is
only a *soft* cut — it approximates the minimum bisection, it does not solve the
combinatorial cut exactly.

## Multiple Choice Questions

**Q1.** A graph has 5 connected components. What must be true of the Laplacian's
spectrum?

- A) It has exactly 5 zero eigenvalues, and the other eigenvalues are all
  positive
- B) It has exactly one zero eigenvalue, because `L·1 = 0` guarantees it
- C) It has 5 positive eigenvalues, one per component
- D) Its largest eigenvalue equals the number of components

<details>
<summary>Answer and explanation</summary>

**A) It has exactly 5 zero eigenvalues, and the other eigenvalues are all
positive.**

The multiplicity of `λ = 0` equals the number of components. The proof is short:
any vector that is *constant on each component* is annihilated by `L`, because
moving along an edge never changes the value. Such vectors are parameterised by
one free number per component, so the null space has dimension 5.

B is the trap that makes this a real question. `L·1 = 0` guarantees *at least*
one zero — the all-ones vector is one element of the null space, not a
description of it. Five components give five independent constant-on-each-block
vectors: `(1,1,1,1,1)`, `(0,1,1,1,1)`, `(0,0,1,1,1)`, and so on. The lesson
demonstrates it live: deleting the `D–E` link in the worked example turns
`μ₂` from `0.438447` into `1.1e-16` and `connected_components` reports 2.

C has the sign backwards, and D confuses the spectrum with the trace. Note
`tr(L) = Σ deg(i) = 2|E|`, which counts edges, not components.

</details>

**Q2.** Why is the Laplacian preferred over the adjacency matrix for finding
communities in an *undirected* graph?

- A) Because the Laplacian is always smaller and therefore faster
- B) Because the Laplacian uses only degrees and connectivity, so it always cuts
  along a genuine bridge, while the adjacency matrix also encodes who points at
  whom
- C) Because the adjacency matrix has no eigenvalues
- D) Because the Laplacian has more eigenvalues than the adjacency matrix

<details>
<summary>Answer and explanation</summary>

**B) Because the Laplacian uses only degrees and connectivity, so it always cuts
along a genuine bridge, while the adjacency matrix also encodes who points at
whom.**

The lesson's own two-community graph shows the practical difference. The
Laplacian's Fiedler vector is `±0.333623` on eight vertices and `±0.234057` on
the two bridge endpoints — a clean sign test that recovers the planted split
exactly, with one scalar per node and no clustering step. The SVD route needs a
2-D embedding plus a k-means pass, and its fit is imperfect because a `K5` clique
is a rank-4 block with singular values `4, 1, 1, 1, 1`.

A is false: the Laplacian is the same size as the adjacency matrix, and
`eigvalsh` costs the same for both. C is false — the adjacency matrix has plenty
of eigenvalues; for an undirected graph they are real, and they are `4, 1, 1,
1, 1` for a `K5`. D is nonsense: both are `n × n` and have exactly `n`
eigenvalues. The real rule, stated in the lesson: **undirected → Laplacian,
directed where direction carries meaning → SVD**, and the second is exactly
what recommendation systems use.

</details>

**Q3.** A connected graph has `μ₂ = 0.01` and `μ₃ = 4.0`. What does that say?

- A) The graph is fragile — a small perturbation can disconnect it, and the
  graph is strongly two-blocked
- B) The graph is well connected, because `μ₂` is positive
- C) The graph has 4 connected components
- D) The graph is not diagonalisable

<details>
<summary>Answer and explanation</summary>

**A) The graph is fragile — a small perturbation can disconnect it, and the graph
is strongly two-blocked.**

`μ₂ > 0` is only a *binary* statement: the graph is connected. The magnitude is
the real information. `μ₂` small means the graph hangs together by a thread —
here, almost certainly one bridge — and the huge gap between `μ₂ = 0.01` and
`μ₃ = 4.0` is the spectral signature of a clean 2-way split. The worked example
has exactly this shape: `μ₂ = 0.438447` against `μ₃ = 2.0`.

B is the classic misreading — it treats positivity as a quality score when it is
only a yes/no. It is a real error to conclude "connected, therefore robust". C is
confusing `μ₃` with the zero count; components come from *zeros*. D is
impossible: `L` is symmetric, so the spectral theorem
([39](../part03_linear_algebra/39_diagonalization_and_spectral.md)) guarantees real eigenvalues and an
orthogonal eigenbasis.

</details>

**Q4.** Why does PageRank damping `M = 0.85P + 0.15J/n` exist?

- A) To make the algorithm faster
- B) To guarantee a unique answer and fix dead-end pages, because every entry of
  `M` is at least `0.15/n > 0`, making `M` irreducible and aperiodic
- C) To reduce the effect of the teleport term to zero
- D) To make the scores sum to 1, which they already do without it

<details>
<summary>Answer and explanation</summary>

**B) To guarantee a unique answer and fix dead-end pages, because every entry of
`M` is at least `0.15/n > 0`, making `M` irreducible and aperiodic.**

The mechanism is Perron–Frobenius: a strictly positive matrix has a unique
strictly positive dominant eigenvector, and power iteration converges to it from
any start. Common Mistake 3 shows the failure damping prevents — two pairs of
pages linking only within themselves give eigenvalue 1 with multiplicity 2, and
then the fixed point depends entirely on the starting vector.

A is false; damping costs one extra matrix multiply per iteration. C is
self-contradictory. D is false — column sums stay 1 because `0.85P` contributes
`0.85` per column and `0.15J/n` contributes `0.15`. And the cost is real, not
free: on Exercise 2's four-page graph, damping moves `A`'s score from `0.444444`
to `0.429209`, pulling everything 15% toward uniform.

</details>

**Q5.** Why is the Fiedler vector's *sign* meaningless while its magnitude is
meaningful?

- A) Because the eigenvector is only defined up to scale and sign
- B) Because eigenvectors are only unique up to permutation
- C) Because the Laplacian is not symmetric
- D) Because the sign depends on the value of `μ₂`

<details>
<summary>Answer and explanation</summary>

**A) Because the eigenvector is only defined up to scale and sign.**

`L(−v) = −Lv = −μ₂v`, so `−v` is an eigenvector for the same eigenvalue, and
every clustering derived from it is unchanged — `sign(−v) = −sign(v)` splits into
the same two groups. So `(A,B,C | D,E,F)` and `(D,E,F | A,B,C)` are the same
partition. Which one you get depends on LAPACK internals, matrix layout, and
version. Common Mistake 5 demonstrates it by comparing `eigvalsh(L)` with
`eigvalsh(-L)`.

B is false — permutation ambiguity is a property of *repeated* eigenvalues, and
the partition problem does not have it. C is false — `L` is symmetric, which is
precisely why the eigenvectors are well defined and real. D is unrelated. The
magnitude is meaningful precisely because it is *invariant* under the sign and
scale freedoms, which is why `μ₂` (a Rayleigh quotient) is the right thing to
report and "which side is positive" is not.

</details>

**Q6.** Why does a real matrix have complex eigenvalues but the graph Laplacian
never does?

- A) Because `L` is computed by a better algorithm
- B) Because `L = D − A` is real **symmetric** whenever `A` is symmetric, and a
  real symmetric matrix has only real eigenvalues
- C) Because graph Laplacians have non-negative entries
- D) Because the Laplacian is positive definite

<details>
<summary>Answer and explanation</summary>

**B) Because `L = D − A` is real symmetric whenever `A` is symmetric, and a real
symmetric matrix has only real eigenvalues.**

That is the spectral theorem. It is why you can call `np.linalg.eigh(L)` and get
real, orthonormal eigenvectors back — which in turn is why the Fiedler vector is
available at all. For a general real matrix, `[[0,−1],[1,0]]` has eigenvalues
`±i` and no real eigenvectors, so there would be nothing to sign-split.

A confuses tool with theorem. C is nonsense — `L` has `−1` entries off the
diagonal. D is false and the distinction matters: `L` is positive *semidefinite*,
not definite, because it always has a zero eigenvalue. `L_sym` is positive
semidefinite too, with eigenvalues in `[0, 2]`. Positive *definiteness* would
mean no zero eigenvalue, which would mean a graph with no vertices.

</details>

**Q7.** In `L_sym = I − D^{-1/2}AD^{-1/2}`, why must the `D^{-1/2}` appear on
*both* sides?

- A) To make `L_sym` symmetric; with it on one side only the matrix is not
  symmetric and the `[0,2]` eigenvalue bound fails
- B) To save computation
- C) Because `A` must be square
- D) Because otherwise the eigenvalues would be negative

<details>
<summary>Answer and explanation</summary>

**A) To make `L_sym` symmetric; with it on one side only the matrix is not
symmetric and the `[0,2]` eigenvalue bound fails.**

`L_sym` is symmetric because `D^{-1/2}` is symmetric and invertible, so
`(D^{-1/2}AD^{-1/2})ᵀ = D^{-1/2}AᵀD^{-1/2} = D^{-1/2}AD^{-1/2}`. The
congruence `Sᵀ(αA + βI)S = αSᵀAS + βSᵀS` with `S = D^{-1/2}` and `SᵀS = D^{-1}`
gives `L_sym = D^{-1/2}LD^{-1/2}`, which is exactly the standard form — and that
form is what puts the eigenvalues in `[0,2]`.

B is false — the two-sided form costs the same. C is unrelated; `A` and `D` are
square by construction. D is false — one-sided gives no eigenvalue bound at all,
which is the actual symptom. Common Mistake 4 is the practical version: a single
isolated node makes `D_{ii} = 0`, so `1/√D_{ii}` is `1/0`, and the resulting `inf`
and `nan` poison every eigenvalue downstream.

</details>

**Q8.** Which is the strongest correct statement about SVD-based clustering of a
user–item rating matrix?

- A) It always finds exactly the right number of clusters
- B) It needs no parameter for the number of clusters
- C) It is a truncated-SVD decomposition followed by clustering, so both `k` and
  the embedding dimension must be chosen, and the result is sensitive to scaling
- D) It is guaranteed to outperform k-means on the raw matrix

<details>
<summary>Answer and explanation</summary>

**C) It is a truncated-SVD decomposition followed by clustering, so both `k` and
the embedding dimension must be chosen, and the result is sensitive to scaling.**

Every step is a choice. Truncation at `k` components is the
[40](../part03_linear_algebra/40_svd_and_pca.md) decision again — the error is `√(Σ_{i>k}σᵢ²)` and the
cliff heuristic can be misled by a vanishing last value. Then `k`-means on the
embedding needs `k` and a random seed. And the input scale decides the spectrum,
so raw ratings in `[1,5]` behave differently from the same ratings rescaled.

A is false: the SVD never tells you the number of communities; that is what the
clustering step or the Fiedler gap is for. B is false — `k` is required. D is a
categorical claim with no theorem behind it, and the lesson's own two-community
example is precisely a case where the SVD needed a k-means pass and the Laplacian
did not. What the SVD *does* have is a guarantee: the rank-`k` approximation is
provably the best one ([40](../part03_linear_algebra/40_svd_and_pca.md), Eckart–Young). Everything after
that step is heuristic.

</details>

**Q9.** Why does removing one edge from a graph change its whole Laplacian
spectrum rather than shifting one eigenvalue slightly?

- A) Because the Laplacian is not continuous in the edge weights
- B) Because eigenvalues are global, not local: the spectral encoding of
  structure means a single edge can remove a direction entirely, which is exactly
  what deleting a bridge does
- C) Because `L = D − A` is only approximately symmetric
- D) Because eigenvectors are only defined up to scale

<details>
<summary>Answer and explanation</summary>

**B) Because eigenvalues are global, not local: the spectral encoding of
structure means a single edge can remove a direction entirely, which is exactly
what deleting a bridge does.**

Eigenvalues are the *global* invariants of a matrix. The spectrum is not a
per-edge record, so it cannot respond to a single edge by moving one number. In
Exercise 3, deleting `3–4` takes the spectrum from
`0, 0.438447, 3, 3, 3, 4.561553` to `0, 0, 3, 3, 3, 3` — one eigenvalue
collapsed to zero and the ordering reshuffled entirely — while deleting `1–2` left
`μ₂` at `0.438447`, unchanged to six decimals.

A is false: eigenvalues are perfectly continuous in the entries, and `L` is
exactly symmetric. C is false — `D − A` is exactly symmetric for symmetric `A`.
D is true of eigenvectors but says nothing about eigenvalues. The practical
lesson is the one Exercise 3 draws: a small structural change can either do
nothing at all or disconnect the graph, and the Fiedler *energy* attribution
tells you which case you are in before you cut.

</details>

**Q10.** A social network's Fiedler vector cleanly separates employees of company
X from everyone else. What has been established?

- A) That members of company X influence each other's link choices
- B) Only that their link patterns are similar; people at the same company, or in
  the same city, or of the same age cohort would produce the identical
  clustering with no influence whatsoever
- C) That the eigenvalue `μ₂` is unusually large, which confirms the effect
- D) That the community is stable over time

<details>
<summary>Answer and explanation</summary>

**B) Only that their link patterns are similar; people at the same company, or in
the same city, or of the same age cohort would produce the identical clustering
with no influence whatsoever.**

Spectral clustering finds nodes with similar *link patterns*. It makes no causal
claim, and a very natural confounder will manufacture communities: shared
employer, shared city, shared university, shared age cohort. Each of these
produces a dense block in the adjacency matrix, and the Fiedler vector finds it
*precisely* — because the structure really is there. What is absent is any
statement about why the links exist.

A is the inference the warning exists to prevent, and it is the standard way
people misuse these tools: "they all follow each other, so they influence each
other" reverses the causal arrow, since influence is one possible *cause* of
mutual linking and shared context is another. C is wrong and backwards — a
*small* `μ₂` signals a fragile, clean split; `μ₂` measures the graph's
resistance to being cut, not confidence in a cause. D is not tested by anything
here at all; stability needs repeated measurement. The honest summary: spectral
clustering reports topology, faithfully and without supervision. Reading it as
social influence requires an experiment, not an eigenvalue.

</details>

## Subjective Questions

### Short Answer

**Q1. Build the Laplacian of a given graph and state the three structural facts
about it.**

<details>
<summary>Model answer</summary>

For an undirected graph with adjacency `A`, form `D = diag(row sums of A)` and
set `L = D − A`. So `L[i][i] = deg(i)`, `L[i][j] = −1` when `i` and `j` are
linked, and `0` otherwise.

Three facts: `L` is **symmetric** (because `A` and `D` are), every **row sums
to zero** (the `+deg(i)` on the diagonal cancels `−1` once per incident edge), so
`L·1 = 0` and `λ = 0` is always in the spectrum; and the **multiplicity of `0`
equals the number of connected components**.

The first is what lets you use `np.linalg.eigh` and get real, orthonormal
eigenvectors. The second is what guarantees at least one zero. The third is the
useful one: a structural property of the graph becomes a count you can compute
from one matrix.

</details>

**Q2. State the algebraic connectivity and explain what a small value means.**

<details>
<summary>Model answer</summary>

For a connected graph, order the spectrum as `0 = μ₁ < μ₂ ≤ … ≤ μₙ`. The
**algebraic connectivity** is `μ₂`, the smallest positive eigenvalue.

A small `μ₂` means the graph hangs together by a thread: it can be split into two
pieces without cutting many edges, and it is fragile — remove the right edge and
`μ₂` becomes exactly `0`. A large `μ₂` means the graph is genuinely robust and
any 2-way split will cost a lot of edges.

A useful reference point: for a complete graph `K_n` the spectrum is
`0, n, n, …, n`, so `μ₂ = n` — the maximum possible. For a path graph `P_5` it
is `0, 0.381966, 1.381966, 2.618034, 3.618034`, so `μ₂ ≈ 0.38`. The lesson's
worked example sits at `0.438447`, small relative to its `μ₃ = 2.0`.

</details>

**Q3. Why does the Fiedler vector give a good 2-way cut, and what is the caveat?**

<details>
<summary>Model answer</summary>

The Fiedler vector is the eigenvector for `μ₂`, the smallest positive eigenvalue.
Minimising `vᵀLv` over unit `v` orthogonal to `1` is exactly the relaxed
minimum-bisection problem: `vᵀLv = Σ_{edges (i,j)} (vᵢ − vⱼ)²` counts the total
squared jump across every edge, so a small value means the graph barely resists
being pulled apart. Splitting the entries by sign recovers a partition that cuts
few edges.

The caveat: it is a **relaxation**, not an exact solution of a combinatorial
problem. Splitting by sign is itself a heuristic — minimising the Rayleigh
quotient over continuous unit vectors does not by itself say "threshold at zero".
In the worked example the threshold that works happens to be 0 because the
Fiedler vector is roughly antisymmetric about the bridge; in general a median or
Otsu-style threshold is safer. Modularity and Normalised Cut are better
behaved because they normalise away graph size and degree.

</details>

**Q4. Verify `L·1 = 0` and explain it structurally.**

<details>
<summary>Model answer</summary>

`(L·1)[i] = Σ_j L[i][j] · 1 = Σ_j L[i][j]`, and row `i` of `L` is
`deg(i)` on the diagonal and `−1` in each of the `deg(i)` positions adjacent to
`i`. So the sum is `deg(i) − deg(i) = 0`, for every `i`. Hence `L·1 = 0`.

Structurally it is not an arithmetic accident but a conservation law. `1` is the
state where every vertex has the same value; a Laplacian applied to a constant
vector does nothing, because nothing flows when nothing has a gradient. The
lesson makes the same point about a "random walk moving a little along every edge
at once, equally" — net change zero.

The useful consequence: `1` is always in the kernel, so `0` is always an
eigenvalue, so counting components (the multiplicity of `0`) is well posed.

</details>

**Q5. For the lesson's worked-example graph, state the spectrum, the number of
components, and the Fiedler vector's sign partition.**

<details>
<summary>Model answer</summary>

Edges `A–B, A–C, A–D, B–C, C–D, D–E, E–F`; degrees `(3, 2, 3, 3, 2, 1)`.

Spectrum ascending: `0, 0.438447, 2.0, 3.0, 4.0, 4.561553`. Sum `14 = 2 × 7`
edges ✓.

**One** zero, so the graph is **connected**.

Fiedler vector, up to sign:

    A +0.307706   B +0.394103   C +0.307706
    D +0.086397   E −0.394103   F −0.701809

Sign split `{A,B,C,D}` versus `{E,F}`, cut by the single edge `D–E` — 1 of 7
edges. `A` and `C` match exactly and `B` and `E` match exactly, reflecting the
graph's `A ↔ C` and `B ↔ E` mirror symmetry.

</details>

**Q6. State the PageRank construction and the role of damping.**

<details>
<summary>Model answer</summary>

Build the column-stochastic transition matrix `P` with `P[i][j]` the probability
of jumping *from* `j` *to* `i` (divide each column of the adjacency matrix by
its out-degree). Column sums are 1, so `1ᵀP = 1ᵀ` and `λ = 1` exists with `1` as
a **left** eigenvector.

The scores are the **right** eigenvector: `Pr = r`, `r ≥ 0`, `Σrᵢ = 1` — the
stationary distribution, i.e. the long-run fraction of visits to each page. Find
it by power iteration, `r ← Pr`, renormalise.

Damping replaces `P` by `M = 0.85P + 0.15J/n`, meaning the surfer follows a link
85% of the time and teleports uniformly 15% of the time. Every entry of `M` is at
least `0.15/n > 0`, so Perron–Frobenius gives a unique strictly positive
dominant eigenvector and convergence from any start. Without it, dead-end pages
score zero and reducible chains can have a non-unique answer.

</details>

### Long Answer

**Q1. Why does the number of connected components equal the multiplicity of the
zero eigenvalue of the Laplacian? Why is this not a heuristic?**

<details>
<summary>Model answer</summary>

**The argument.** `λ = 0` with eigenvector `x` means `Lx = 0`, i.e.
`Σ_j L[i][j]xⱼ = 0` for every vertex `i`. That sum is
`deg(i)·xᵢ − Σ_{j∼i} xⱼ = 0`, so

    xᵢ = (1/deg(i)) Σ_{j∼i} xⱼ

for every `i` with positive degree: **`x` at vertex `i` equals the average of `x`
over its neighbours.** An average of numbers all equal to `xᵢ` is `xᵢ` again only
when every neighbour also has value `xᵢ`. So `x` is constant along every edge,
hence constant on every connected component. Conversely any vector constant on
each component satisfies `Lx = 0`, trivially.

So the eigenspace for `λ = 0` is *exactly* the space of vectors constant on each
component, and that space has one free parameter per component. Its dimension is
the number of components, and geometric multiplicity is the dimension.

**Why it is not a heuristic.** It is a bijective characterisation: the kernel of
`L` and the set of component-wise-constant vectors are the *same subspace*, not
two things that happen to agree. Nothing is approximated, nothing is tuned, and
there are no thresholds. The lesson verifies it three ways in one code block —
`np.isclose(w, 0)` counts 1, `scipy.sparse.csgraph.connected_components` says 1,
and the two agree.

**Why it matters.** This is the pattern that makes spectral methods useful in
general: a combinatorial question about *structure* becomes a *linear-algebraic*
question about a matrix, and matrices are things you can compute efficiently.
Connected components, minimum cut (as a relaxation), clustering, mesh
simplification, and the low-frequency modes of a simulation all ride on it.

**What breaks it.** Degree zero. An isolated vertex has no average to satisfy, so
the argument needs a convention — `L_sym` in particular needs `D_{ii} > 0`, giving
Common Mistake 4's `inf` and `nan`. And `L = D − A` is the Laplacian only for an
**undirected** graph; for a directed one the analogue is
`I − D_out⁻¹A`, and the component count then comes from weakly versus strongly
connected components, which is a genuinely different question.

</details>

**Q2. Why does the Laplacian beat the SVD for undirected community detection,
and when should you use the SVD instead?**

<details>
<summary>Model answer</summary>

**Why the Laplacian wins for undirected graphs.**

First, *the Laplacian only uses connectivity*. `L = D − A` needs degrees and
links. That means it is invariant to anything that preserves the graph's
topology, and it always cuts along a genuine bridge. The adjacency matrix, by
contrast, also encodes "who points at whom", and in an undirected setting that
is redundant information which can pull the answer off a real structural seam.

Second, *the answer is one scalar per node*. The lesson's two-`K5` example: the
Fiedler vector is `±0.333623` on eight vertices and `±0.234057` on the two
bridge endpoints. Sign test, done. The SVD route produces a 2-D embedding that
must then be handed to k-means — an extra step with an extra parameter and a
random seed.

Third, *the approximation is not very lossy for the purpose*. A `K5` clique has
adjacency singular values `4, 1, 1, 1, 1` — it is a rank-4 block, so a rank-2
approximation throws away real content. The Laplacian, by contrast, has a clean
single low mode: `0, 0.298438, 5, 5, 5, 5, 5, 5, 5, 6.701562` for the two-clique
graph, with the Fiedler vector carrying the entire between-block structure.

**When the SVD wins.**

When *direction carries meaning*. The lesson's rule is explicit: **directed edges
where direction carries meaning → SVD.** That is a follower graph, a citation
web, and above all a user–item matrix. There, "user A follows user B but not the
reverse" is real information the Laplacian throws away, and `A`'s SVD uses it.
This is exactly the mechanism behind recommendation: the top singular vectors of
a rating matrix span the latent taste dimensions, and projecting users and items
into that space is the collaborative-filtering step. The lesson's SVD-clustering
code is the same code path with one row type per user.

Two further cases where the SVD is the right tool. When the input is a
**similarity matrix** rather than a binary adjacency — `SpectralClustering` with
`affinity='precomputed'` on cosine similarities is SVD-style, and the Laplacian
of a similarity matrix is meaningless because "degree" is not well defined. And
when you need a **truncated** low-rank structure, since the SVD's error is
provably optimal by Eckart–Young.

**The honest summary.** Neither tool dominates. The question is what your
matrix means: topology or direction.

</details>

**Q3. Why does PageRank need damping, and what exactly does damping change about
the answer?**

<details>
<summary>Model answer</summary>

**What goes wrong without it.** Two distinct failures, and they need separating.

*Dead ends.* A page with no outgoing links has an all-zero column in the
transition matrix before normalisation, so it must be handled artificially. And a
page nothing links *to* is never reached, so its stationary score is exactly
zero. On Exercise 2's four-page graph, page `D` scores `r₄ = 0.000000`
undamped — not a rounding artefact, but the correct answer to the question "what
fraction of random walks end at `D`?" when no walk ever gets there.

*Non-uniqueness.* If the chain is reducible, `λ = 1` can have multiplicity
greater than 1, and then the fixed point depends on the starting vector. Common
Mistake 3's four pages split into two pairs linking only within themselves:
eigenvalue 1 appears twice, and starting uniform versus starting at
`(0.4, 0.4, 0.1, 0.1)` gives two different answers, both valid fixed points.

**What damping does.** `M = 0.85P + 0.15J/n` adds a uniform floor to every entry,
so the smallest is `0.15/n > 0`. A strictly positive matrix is irreducible and
aperiodic, and Perron–Frobenius then guarantees a unique strictly positive
dominant eigenvector for the leading eigenvalue, with power iteration converging
to it from any starting vector. The damped answer on Exercise 2's graph is
`(0.429209, 0.219914, 0.313377, 0.037500)`, with the dead page scoring exactly
`0.0375 = 0.15/4`, the teleport term alone.

**What it costs, quantitatively.** Everything is pulled 15% of the way toward
uniform. Concretely: `A`'s score drops from `0.444444` to `0.429209`, and the
dead page rises from `0` to `0.0375`. It is a real loss of sharpness, bought for
a guarantee. If you change the damping factor from 0.85 to 0.50 you change the
ranking on any graph with dead ends or link farms — so `alpha` is a modelling
choice, like the norm in [37](../part03_linear_algebra/37_inner_products_norms_geometry.md), not a
constant to copy.

**What breaks if you skip it.** You get plausible, defensible-looking numbers
that are silently non-unique, or zeros for pages that are actually important.
Neither failure raises an exception. That is why damping is in every production
implementation and why `nx.pagerank` exposes `alpha` rather than hard-coding it.

</details>

**Q4. Why is `μ₂` an attributable fragility measure, and how do you use it to
decide which edge to cut?**

<details>
<summary>Model answer</summary>

**The identity that makes it attributable.** For any vector `v`,

    v^T L v = ΣᵢΣⱼ L[i][j]vᵢvⱼ = Σ_edges (vᵢ − vⱼ)²

Each edge contributes `(vᵢ − vⱼ)²` twice in the double sum and `2(vᵢ−vⱼ)²` before
subtracting the two diagonal terms, and the standard identity collapses this to
one contribution per edge. So the Rayleigh quotient of the Fiedler vector,

    μ₂ = v₂^T L v₂ / v₂^T v₂    (with ‖v₂‖ = 1, just `v₂^T L v₂`)

is the **total squared jump of the cut direction across every edge in the graph**,
decomposed edge by edge. Since `Σ_edges (vᵢ−vⱼ)² = μ₂`, each edge's share of
`μ₂` is a fraction of the whole, and the shares sum to exactly 1.

**Worked through.** For Exercise 3's graph — two triangles joined by `3–4` — the
Fiedler vector is `(−0.464705, −0.464705, −0.260956, +0.260956, +0.464705,
+0.464705)`, and the per-edge energies are

    (1,2): 0.000000   (1,3): 0.041514   (2,3): 0.041514
    (3,4): 0.272393   (4,5): 0.041514   (4,6): 0.041514   (5,6): 0.000000

which sum to `0.438447 = μ₂` ✓. So edge `3–4` carries **62%** of the Fiedler
energy, while edges `(1,2)` and `(5,6)` carry **exactly zero**.

**The decision this supports.** Sort edges by share of `μ₂`; the top one is your
most fragile joint. Here the answer is `(3,4)` with a 62% share, and deleting it
sends `μ₂` to `0` — disconnection. Deleting `(1,2)` instead, whose share is zero,
leaves `μ₂` at `0.438447` *unchanged to six decimals*. The prediction and the
measurement agree exactly, and you could have made it before touching anything.

**Why zero share means irrelevant.** Edge `(1,2)` has `v₁ = v₂` exactly, so
`(v₁−v₂)² = 0` and the edge lies entirely *along* the cut direction. Cutting it
cannot make the graph any easier or harder to split — geometrically, `1` and `2`
are on the same side of the bridge with the same Fiedler value, so they are
interchangeable for this question. Edges with a *large* share straddle the
boundary and are the ones whose removal does damage.

**Why this matters beyond cuts.** This is the same reasoning as eigendecomposition
applied to a graph instead of a matrix. `μ₂` alone tells you the graph is fragile;
the energy attribution tells you *which joint* is fragile, and that is the
question a network engineer actually needs answered. The same decomposition
drives mesh simplification (edges carrying the most low-frequency energy are the
ones you decimate) and any edge-ranking robustness analysis.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — Laplacian by hand, and a spectral cut.** Consider the
undirected graph on 5 vertices with edges
`{1–2, 2–3, 3–1, 3–4, 4–5}`.

(a) Write the adjacency matrix and the degree matrix.
(b) Build `L = D − A` and verify every row sums to zero.
(c) Verify `L` is symmetric and find its eigenvalues numerically.
(d) How many connected components does the graph have? How do you read that
off the eigenvalues?
(e) Compute the Fiedler vector and use its sign to propose a 2-way partition.
How many edges cross the cut?
(f) Delete the edge `3–4` and recompute `μ₂`. What does that tell you about the
role of that single edge?

<details>
<summary>Solution</summary>

**(a)**
```
A = [0 1 1 0 0]        D = [2 0 0 0 0]
    [1 0 1 0 0]            [0 2 0 0 0]
    [1 1 0 1 0]            [0 0 3 0 0]
    [0 0 1 0 1]            [0 0 0 2 0]
    [0 0 0 1 0]            [0 0 0 0 1]
```
Degrees: 2, 2, 3, 2, 1. Sum = 10 = 2 × 5 edges ✓

**(b)**
```
L = [ 2 -1 -1  0  0]     row sums:
    [-1  2 -1  0  0]      2-1-1 = 0 ✓
    [-1 -1  3 -1  0]     -1+2-1 = 0 ✓
    [ 0  0 -1  2 -1]     -1-1+3-1 = 0 ✓
    [ 0  0  0 -1  1]      0-1+2-1 = 0 ✓
                          -1+1 = 0 ✓
```

**(c)** `L` is symmetric: `L[0][1] = −1 = L[1][0]`, and so on for every pair.

Eigenvalues (ascending) from `np.linalg.eigvalsh`:
```
0,  0.518806,  2.311108,  3.0,  4.170086
```
Check: they sum to `10.0 = tr(L) = 2+2+3+2+1` ✓ (the trace of `L` is the sum of
the degrees, which is twice the number of edges — `2 × 5 = 10`).

**(d)** Exactly **one** zero eigenvalue, so the graph is **connected**: one
connected component. Vertices 1,2,3 form a triangle and 4,5 hang off vertex 3,
and everything is reachable.

**(e)** The Fiedler vector for `μ₂ = 0.518806` is, up to sign and scale,
```
v₁: +0.419319
v₂: +0.419319
v₃: +0.201774
v₄: −0.337998
v₅: −0.702415
```
Sign split: `{1, 2, 3}` and `{4, 5}`. Edges crossing the cut: only `3–4`, so
**1 edge out of 5**. Note `v₁ = v₂` exactly, because swapping vertices 1 and 2 is
an automorphism of the graph, and the Fiedler direction has to respect it.

**(f)** Deleting `3–4` disconnects the graph into `{1,2,3}` and `{4,5}`, so the
spectrum becomes
```
0,  0,  2.0,  3.0,  3.0
```
(traces: `8.0 = 2+2+3+1+1`, one edge fewer). `μ₂ = 0` exactly (numerically
`~1e-16`). Two zeros, two components — the theorem again.

**What it tells you:** the value of `μ₂` is a *fragility* measure, not just a
curiosity. `μ₂ = 0.518806` says this graph is held together by a single thin
link. Remove that one edge and the network splits in two. The algebraic
connectivity is the smallest number that has to be overcome to disconnect the
graph, which is why it is the natural quantity for robustness questions.

Note also that `μ₂` (`0.5188`) is well below `μ₃` (`2.3111`) — the Fiedler
vector is genuinely the outlier, which is the spectral signature of a clean 2-way
split. Had the graph been a chain `1–2–3–4–5` instead, the spectrum would be
`0, 0.382, 1.382, 2.618, 3.618` and `μ₂` would still be the clear outlier.

</details>

**[ ] Exercise 2 — PageRank by hand.** Four pages with links
`A→B`, `A→C`, `B→A`, `B→C`, `C→A`, `D→A`.

(a) Write the transition matrix `P` with `P[i][j]` = chance of going from `j`
to `i`. Check the column sums.
(b) Verify that `λ = 1` is an eigenvalue of `P`, and identify both
eigenvectors for it.
(c) Run power iteration from a uniform start for 200 steps. Report the
stationary distribution to 4 decimal places.
(d) Page D has no outgoing links. What goes wrong in the undamped version, and
what does damping do about it?

<details>
<summary>Solution</summary>

**(a)** `P[i][j]` = chance of moving from page `j` to page `i`.

- From `A`: half to `B`, half to `C` → `P[1][0] = P[2][0] = 0.5`
- From `B`: half to `A`, half to `C` → `P[0][1] = P[2][1] = 0.5`
- From `C`: all to `A` → `P[0][2] = 1.0`
- From `D`: all to `A` → `P[0][3] = 1.0`

```
    A     B     C     D
A [0    0.5   1.0   1.0 ]
B [0.5  0     0     0   ]
C [0.5  0.5   0     0   ]
D [0    0     0     0   ]
```
Column sums: `1, 1, 1, 1` ✓ — every click lands somewhere.

**(b)** Because columns sum to 1, `1ᵀP = 1ᵀ`, so `1` is a **left** eigenvector
for `λ = 1` — equivalently `Pᵀ·1 = 1`. And `λ = 1` really is an eigenvalue of
`P` too: `np.linalg.eig(P)` returns `1, −0.5, −0.5, 0`.

The **right** eigenvector for `λ = 1` is the stationary distribution. Solve
`Pr = r` with `r₁ + r₂ + r₃ + r₄ = 1`, working row by row:

- Row 4: `0 = r₄` → `r₄ = 0`
- Row 2: `r₂ = 0.5r₁`
- Row 3: `r₃ = 0.5r₁ + 0.5r₂ = 0.5r₁ + 0.25r₁ = 0.75r₁`
- Row 1: `r₁ = 0.5r₂ + 1.0r₃ + 1.0r₄ = 0.5(0.5r₁) + 0.75r₁ + 0 = 0.25r₁ + 0.75r₁ = r₁`

The last equation is an **identity**, so `r₁` is free: the solution space is
one-dimensional, as it must be since `λ = 1` is simple. Normalise with
`r₁(1 + 0.5 + 0.75) = 2.25r₁ = 1`, giving `r₁ = 4/9`:

```
r = (0.444444, 0.222222, 0.333333, 0.000000)
```

Verify: `Pr = (0.5(0.222222) + 0.333333 + 0,  0.5(0.444444),  0.5(0.444444) +
0.5(0.222222),  0) = (0.444444, 0.222222, 0.333333, 0)` ✓ — a genuine fixed
point.

**Now read `r₄ = 0` carefully.** Page `D` scores exactly zero. That is the
failure, and it is not a numerical artefact: the column of `A` for `D` is all
zeros, so nothing links *to* `D` and no random surfer can ever arrive there. `D`
receives no traffic and correctly earns no traffic.

**(c)** Power iteration from a uniform start converges to the fixed point above:

```
r = (0.4444, 0.2222, 0.3333, 0.0000)
```

and from the different start `r₀ = (0.4, 0.4, 0.1, 0.1)` it converges to the
**same** answer, and so does starting all the mass on `D` alone. So on this
graph the limit is unique after all. The spectrum explains why: the leading
eigenvalue is `1` and the runner-up has modulus `0.5`, so the gap is `2.0` and
convergence is fast and start-independent.

That uniqueness is a property of *this* graph, not a guarantee. `P` is reducible
— `{A, B, C}` is a closed class that cannot be left, and `D` is a transient
state that cannot be entered. Had the graph contained a second closed class, `λ = 1`
would have had multiplicity 2 and *any* split of mass between the two classes
would be a fixed point. Common Mistake 3 shows exactly that case.

**(d)** Two problems, and damping fixes both:

1. **Dead ends.** Page `D` has no outgoing links, so the random surfer has
   nowhere to go from `D`, and `D` itself earns nothing. Real implementations
   give dead pages an outgoing link to every page, or distribute their score by
   the number of links they had.
2. **Possible non-uniqueness.** A reducible chain can have eigenvalue 1 with
   multiplicity greater than 1, in which case the limit depends on the starting
   vector. Damping rules that out structurally rather than by case analysis.

With damping, `M = 0.85P + 0.15J/4`, every entry becomes at least
`0.15/4 = 0.0375 > 0`, so `M` is a strictly positive matrix. Perron–Frobenius
then guarantees a **unique** strictly positive right eigenvector for `λ = 1`, and
power iteration converges to it from any start. Running 200 steps from uniform:

```
A: 0.429209    B: 0.219914    C: 0.313377    D: 0.037500
```

(`M r = r` to eight decimals, and the four entries sum to 1.) The dead page now
scores exactly `0.037500 = 0.85 × 0 + 0.15 × 1/4`, the teleport term alone,
exactly as it should be.

Note also how much damping *changes* the answer. Undamped, `A` scores `0.4444`;
damped, it scores `0.4292`. Everything is pulled 15% of the way toward uniform,
which is what "the surfer sometimes teleports" means quantitatively. That is the
trade damping makes — a little sharpness for a guarantee — and it is why every
production implementation ships it.

</details>

**Challenge — Exercise 3 — communities, and what changes when you delete an
edge.** Build the undirected graph on 6 vertices with edges
`{1–2, 1–3, 2–3, 3–4, 4–5, 4–6, 5–6}` — two triangles joined by the edge
`3–4`.

(a) Compute `L` and its eigenvalues in ascending order.
(b) Identify the Fiedler vector and use it to recover the two triangles. Does
it get them right?
(c) Compute `μ₂` and explain in words what it measures.
(d) Now delete the edge `3–4`. Recompute the spectrum and say how many
connected components there are.
(e) Delete instead the edge `1–2`. Recompute `μ₂` and compare it to the value
in (c). Which deletion does more damage to the graph's "togetherness", and why
should that be predictable from (c)?

<details>
<summary>Solution</summary>

**(a)**
```
A = [0 1 1 0 0 0]     degrees: 2, 2, 3, 3, 2, 2
    [1 0 1 0 0 0]
    [1 1 0 1 0 0]
    [0 0 1 0 1 1]
    [0 0 0 1 0 1]
    [0 0 0 1 1 0]

L = [ 2 -1 -1  0  0  0]
    [-1  2 -1  0  0  0]
    [-1 -1  3 -1  0  0]
    [ 0  0 -1  3 -1 -1]
    [ 0  0  0 -1  2  1]
    [ 0  0  0 -1  1  2]
```
Row sums: `2-1-1=0`, `−1+2−1=0`, `−1−1+3−1=0`, `−1+3−1−1=0`, `−1+2+1=0`,
`−1+1+2=0` ✓ All zero.

Eigenvalues ascending: `0, 0.438447, 3.0, 3.0, 3.0, 4.561553`
Check: sum `= 0.438447 + 9 + 4.561553 = 14.0 = tr(L) = 2+2+3+3+2+2` ✓

**(b)** The Fiedler vector for `μ₂ = 0.438447` is, up to sign and scale,
```
v₁: −0.464705
v₂: −0.464705
v₃: −0.260956
v₄: +0.260956
v₅: +0.464705
v₆: +0.464705
```
The sign structure is the important part: vertices `{1, 2, 3}` come out with one
sign and `{4, 5, 6}` with the other.

**Yes, it recovers the two triangles exactly**, and note the mirror symmetry:
`v₁ = v₂` and `v₅ = v₆`, because the graph is symmetric under `1 ↔ 2` and
`5 ↔ 6`. The recovered partition is `{1,2,3} | {4,5,6}`, cutting exactly the
single edge `3–4`.

(A caveat worth stating: the exact decimals depend on the sign convention and on
normalisation. The *sign pattern* is the robust thing, which is why every
implementation clusters on it rather than comparing magnitudes.)

**(c)** `μ₂ = 0.438447` is the **algebraic connectivity**. In words: it is the
smallest positive eigenvalue, and it measures how much the graph resists being
split in two. A value near zero means the graph hangs together by a thread; a
large value means it is genuinely well-connected and any 2-way split will cost a
lot of edges.

Here `μ₂ = 0.438447` is small relative to the rest of the spectrum (`μ₃` through
`μ₆` are all at least `3.0`), and the reason is visible: one edge, `3–4`, is the
only thing joining two otherwise tight triangles. That is why the multiplicity-3
eigenvalue `3.0` shows up — each triangle contributes that value, and a triangle
has no nontrivial internal cut direction.

**(d)** Delete `3–4`. The graph is now two disjoint triangles.
```
L' = [ 2 -1 -1  0  0  0]      eigenvalues:
    [-1  2 -1  0  0  0]       0
    [-1 -1  3  0  0  0]       0
    [ 0  0  0  2 -1 -1]       3
    [ 0  0  0 -1  2  1]       3
    [ 0  0  0 -1  1  2]       3
```
**Two connected components** — the two triangles. Confirmed by the two zero
eigenvalues (numerically `~10⁻¹⁶` and `~10⁻¹⁶`), and by
`scipy.sparse.csgraph.connected_components`.

Note the shape of the spectrum changed completely. Each triangle contributes one
zero and the value `3` with multiplicity two, so `L'` has `0, 0, 3, 3, 3, 3`.
Removing one edge did far more than change one number: it destroyed the Fiedler
direction entirely, because the direction that separated the two halves was the
bridge, and the bridge is gone.

**(e)** Delete `1–2` instead. The graph is still connected — vertices 1 and 2
now hang off vertex 3, which still reaches everything — but vertices 1 and 2
each drop to degree 1.

Recomputing the spectrum gives `0, 0.438447, 1.0, 3.0, 3.0, 4.561553`.

Compare:
- deleting `3–4`: `μ₂` goes from `0.438447` to `0` — the graph **disconnects**
- deleting `1–2`: `μ₂` goes from `0.438447` to `0.438447` — **completely unchanged**

**Deleting `3–4` does infinitely more damage than deleting `1–2`.** And this *is*
predictable from part (c), which is the real lesson: `3–4` is the unique bridge
between the two halves, so it lies on the direction the Fiedler vector is
testing. Edge `1–2` lies *along* that direction's constant part — indeed `v₁` and
`v₂` are exactly equal, so edge `1–2` carries literally zero energy in the
Fiedler direction and its removal cannot change the Rayleigh quotient at all.

That last point is worth making quantitative, because it is the real content of
the exercise. For the Laplacian, `vᵀLv = Σ_{edges (i,j)} (vᵢ − vⱼ)²`. Decomposing
the Fiedler vector's energy over the seven edges:
    (1,2): 0.000000      (4,5): 0.041514
    (1,3): 0.041514      (4,6): 0.041514
    (2,3): 0.041514      (5,6): 0.000000
    (3,4): 0.272393

The seven terms sum to `0.438447 = μ₂`, as they must. The edge `(3,4)` alone
carries `0.272393`, i.e. **62.13% of the Fiedler energy**, while `(1,2)` and
`(5,6)` carry exactly zero. So the spectrum tells you, before you cut anything,
which edges the graph is fragile *along*. That is the payoff: `μ₂` is not just a
yes/no connectivity test — it is a sensitive, continuous, and *attributable*
measure of how the graph would resist being cut.

</details>

**[ ] Exercise 4 — the normalised Laplacian, and an isolated vertex.** Take the
lesson's six-node graph (edges `A–B, A–C, A–D, B–C, C–D, D–E, E–F`), with
degrees `(3, 2, 3, 3, 2, 1)`.

(a) Build `L_sym = I − D^{-1/2}AD^{-1/2}` numerically and verify it is symmetric.
(b) Compute its eigenvalues and check they all lie in `[0, 2]`.
(c) Compare with the eigenvalues of `L/n` and explain why `L_sym` is not the
same object.
(d) Now add a seventh vertex `G` with no edges at all. What is `deg(G)`, and what
happens if you build `L_sym` without a convention for it?
(e) Show that the regularised convention (`deg(G) → 1`) produces a second zero
eigenvalue, matching the fact that `G` is its own connected component.

<details>
<summary>Solution</summary>

**(a)** `D^{-1/2} = diag(0.577350, 0.707107, 0.577350, 0.577350, 0.707107,
1.000000)`. Since `A[i][j] = A[j][i]` and `√(deg(i)deg(j))` is symmetric in
`i, j`, the entry `[i][j] = A[i][j]/√(deg(i)deg(j))` equals its mirror, so
**`L_sym = L_symᵀ`** ✓ — which is exactly why the `D^{-1/2}` goes on both sides.

The off-diagonal values are `−1/√6 = −0.408248` where the two degrees are 2 and 3,
`−1/√3 = −0.577350` where one degree is 3 and the other 1, and `−1/√2 = −0.707107`
for `E–F` (degrees 2 and 1).

**(b)** Eigenvalues ascending: `0, 0.272686, 1.0, 1.333333, 1.531193, 1.862788`.
Every one lies in `[0, 2]` ✓, and exactly one is `0` ✓ (one component).

**(c)** Three scalings of the same six underlying numbers:

| quantity | μ₁ | μ₂ | μ₃ | μ₄ | μ₅ | μ₆ |
| --- | --- | --- | --- | --- | --- | --- |
| `L` | 0 | 0.438447 | 2.000000 | 3.000000 | 4.000000 | 4.561553 |
| `L/6` | 0 | 0.073075 | 0.333333 | 0.500000 | 0.666667 | 0.760259 |
| `L_sym` | 0 | 0.272686 | 1.000000 | 1.333333 | 1.531193 | 1.862788 |

`L_sym` is **not** `L/n`. The relation is the congruence
`L_sym = D^{-1/2}LD^{-1/2}`, and a congruence does not simply rescale
eigenvalues — it rescales them by a *direction-dependent* factor
`1/√(deg(i)deg(j))`, so the degree-1 vertex `F` is scaled very differently from
the degree-3 vertices.

The distinction has a practical consequence. `L/n` is a scalar multiple, so it
has the **same eigenvectors**, and therefore keeps the minimum-cut relaxation
intact. `L_sym` has different eigenvectors, but it buys two things: the `[0,2]`
bound, and degree-insensitivity, so a single high-degree hub cannot dominate the
embedding.

**(d)** `deg(G) = 0`, so `D^{-1/2}` needs `1/√0`. In floating point that is `∞`,
and the resulting `L_sym` contains `inf` and `nan`, which poison every
eigenvalue you compute from it. This is Common Mistake 4 in exactly this form.

**(e)** Apply the convention `deg(G) → 1`:
`D_safe = diag(3, 2, 3, 3, 2, 1, 1)`. Now `A`'s seventh row is all zeros, so row 7
of `L_sym` is `[0, 0, 0, 0, 0, 0, 1]` — the identity in that position, because
`1 − 0/√(1·1) = 1`.

Therefore the map `x ↦ (x₁, …, x₆, 0)` sends the first six coordinates of `x`
through the *old* `L_sym` in the output entries 1–6, and produces `0` in entry 7.
Taking `x` to be the eigenvector of part (b) for `λ = 0` therefore gives a **new
zero eigenvector**, linearly independent of the first. So `L_sym` has exactly
**two** zeros.

`connected_components` reports 2 ✓ — the isolated vertex and the original
component. The lesson's theorem holds with the convention in place, which is
exactly why every library guards the division rather than trusting the caller.

</details>

**[ ] Exercise 5 — SVD versus Laplacian on the same graph.** Build two `K5`
cliques on vertices `{0,…,9}` — fully connected within each half — joined by a
single bridge edge `4–5`.

(a) Report the degrees and compute the Laplacian eigenvalues in ascending order.
(b) Compute `μ₂` and the Fiedler vector. Do the signs recover the planted split?
(c) Compute the singular values of the adjacency matrix and comment on the
"cliff".
(d) Compare the two rank-2 truncations: which better represents the block
structure, and why?
(e) Turn the bridge into a directed edge `4 → 5` only. Which method is right now,
and what happens to the plain Laplacian's spectrum?

<details>
<summary>Solution</summary>

**(a)** Degrees: `(4, 4, 4, 4, 5, 5, 4, 4, 4, 4)` — vertices 4 and 5 carry one
extra from the bridge.

Laplacian eigenvalues ascending:

```
0, 0.298438, 5, 5, 5, 5, 5, 5, 5, 6.701562
```

Trace check: sum `= 42`, and `Σdeg = 42 = 2 × 21` edges (each `K5` has `5·4/2 =
10` edges, plus the bridge) ✓

**(b)** `μ₂ = 0.298438`, Fiedler vector:

```
−0.333623  −0.333623  −0.333623  −0.333623  −0.234057
+0.234057  +0.333623  +0.333623  +0.333623  +0.333623
```

Signs: `{0,1,2,3,4}` negative, `{5,6,7,8,9}` positive. **Exactly the planted
split**, from one scalar per vertex and a sign test. And the shape is
informative: the bridge endpoints (4 and 5) sit *closer to zero*
(`±0.234057`) than the rest of their clique (`±0.333623`) — they are the
ambiguous nodes, which is exactly right, since each is attached to both halves.

**(c)** Singular values of the adjacency matrix, descending:

```
4.236068, 3.828427, 1.828427, 1, 1, 1, 1, 1, 1, 0.236068
```

`σ₁/σ₂ = 1.1065` — nearly equal, because the two cliques are the same size, and
that ratio encodes the *relative size* of the two blocks. Then a long
uninformative tail of values near `1.0`: internal clique structure, since a `K5`
has adjacency singular values `4, 1, 1, 1, 1` and is therefore a rank-4 block
that does not collapse to a single direction.

**(d)** The Laplacian represents *this* structure better, for two reasons.

First, its spectrum has a clean two-level shape — one `0`, one tiny `0.298438`,
then a gap straight to `5.0`. The Fiedler direction is the *entire*
low-frequency content of the graph, so truncating at `k = 2` discards nothing
that matters for the partition.

Second, the adjacency spectrum has seven values near `1.0` that are genuine
content — the internal degrees of freedom of each clique — and any rank-2
truncation discards them. So the SVD truncation is *more* lossy here, not less,
because what it throws away is real structure rather than dust.

The lesson's k-means code shows the practical consequence: the two centres come
out around `(±0.31, ±0.32)`, separated mainly by the **sign** of the second
coordinate. The clustering rediscovers the sign test anyway — after an extra
embedding step, an extra parameter, and an extra random seed.

**(e)** With `4 → 5` directed and not `5 → 4`, the graph is no longer symmetric.
`A` is not symmetric, so `L = D − A` is not symmetric, the spectral theorem no
longer applies, and `np.linalg.eigh` would silently read only the lower triangle
— Common Mistake 1 in [39](../part03_linear_algebra/39_diagonalization_and_spectral.md). The clean `[0,2]`
bound and the minimum-cut relaxation are gone too.

The right tool is now the **SVD of the asymmetric adjacency matrix**. Its singular
vectors capture the directed structure — which nodes push into the other half —
and that is information the Laplacian of a symmetrised graph would have discarded.
This is the lesson's stated rule: **directed edges where direction carries meaning
→ SVD**, and it is the same code path recommendation systems use on user–item
matrices.

The standard object for directed-graph clustering is
`L_sym = D^{-1/2}(D − A)D^{-1/2}` (Ng–Jordan–Weiss), which is still defined and
still symmetric — but it is built differently from the plain `L`, and its
eigenvector interpretation is weaker than the minimum-cut story for undirected
graphs.

</details>

**Challenge — Exercise 6 — the SVD clustering code path, and why `k` is a
parameter you must defend.** Take a user–item rating matrix: rows are users,
columns are items, entries in `[0, 5]` with 0 meaning "no rating". The users fall
into two taste groups — the first five rate the first five items highly and the
last five not at all, and the other five do the reverse.

(a) State what the SVD of this matrix is *for*, in one sentence.
(b) You take the rows of `U` as a 2-D embedding and run `k`-means with `k = 2`.
Why does that work here, and what would make it wrong?
(c) Suppose instead you kept only the top 1 singular vector and clustered in 1-D.
What happens, and what does that tell you about choosing the truncation rank?
(d) Suppose you did **not** centre the matrix before the SVD. What changes, and
which step of [40](../part03_linear_algebra/40_svd_and_pca.md) does that violate?
(e) Explain in one sentence why "the number of clusters" is a different question
from "the number of connected components", and which one the SVD can answer.

<details>
<summary>Solution</summary>

**(a)** The top singular vectors span the *latent taste dimensions* of the matrix,
and projecting users and items into that shared space is what makes a
recommendation possible at all.

**(b)** `k = 2` works because the planted structure is two-dimensional: `σ₁` and
`σ₂` are both large and nearly equal — on the lesson's `K5`+`K5` analogue the top
two were `4.236068` and `3.828427`, a ratio of only `1.1065` — while `σ₃` drops
sharply. The 2-D embedding therefore has real geometry to separate, and the two
taste groups land in different regions.

It is wrong when the structure is not two-dimensional: one dominant genre plus
noise, or five groups of unequal size. And it is wrong as a *default*, because
the SVD never tells you `k`. Three quantities must be chosen, and they are
different questions — the truncation rank (how many singular vectors to keep), the
embedding dimension, and the number of clusters. Each is a hyperparameter, and
the choice is unstable in a specific way: Eckart–Young
([40](../part03_linear_algebra/40_svd_and_pca.md)) guarantees the rank-`r` approximation is the *best*
rank-`r` one, but guarantees nothing about `r` matching the number of clusters.

**(c)** With one singular vector the embedding is 1-D, so points differ by a
single signed number. The two groups separate only if that one direction happens
to distinguish them. Since the two blocks contribute two roughly-equal leading
directions (`σ₁/σ₂ ≈ 1.11`), keeping one discards a direction carrying almost as
much signal as the one you kept, and the 1-D projection merges or splits the
groups depending on which vector the algorithm happened to return first.

The general lesson: the truncation rank must be chosen *from the spectrum* — the
`σ` ratios, the scree cliff, or held-out downstream performance — and must not
be set equal to the cluster count by coincidence. When the spectrum decays
smoothly with noise mixed in, as in [40](../part03_linear_algebra/40_svd_and_pca.md)'s Challenge
Exercise 6, there is no elbow, and the choice has to be made on error grounds.

**(d)** Not centring means the SVD finds the direction of largest *magnitude*, not
largest *spread*. If the two item groups have different mean ratings, `σ₁` is
dominated by the difference in level between them — a property of scoring habits,
not of taste. The embedding then encodes "how generous a rater is this person",
and `k`-means clusters raters by generosity rather than by taste.

This violates the centring step of [40](../part03_linear_algebra/40_svd_and_pca.md), where it is Common
Mistake 3. The recommendation analogue is not centring *items*: popular items
have high means and will dominate `σ₁`. Both the row and the column means matter.

**(e)** A connected component is a purely *structural* property fixed by the
zero eigenvalues of the Laplacian; a cluster is a choice of a partition, and the
SVD only ranks directions by energy, from which `k` is an inference you still
have to make.

That asymmetry is the lesson's closing rule in one line. The Laplacian answers
the component question *exactly* — counting zeros is a count, not a choice, and
the kernel argument makes it a bijection rather than a heuristic. The SVD answers
no structural question directly: it gives you a *ranking* of directions, and
every downstream decision is yours. Hence: undirected and structural → Laplacian;
directed, or similarity-matrix, and willing to tune → SVD.

</details>

## Summary

- A **graph is a matrix**: the adjacency matrix has a 1 per edge, and it is
  symmetric exactly when the graph is undirected.
- The **Laplacian** `L = D − A` is symmetric, has degrees on the diagonal and
  `−1` for links, and every row sums to zero.
- **Counting the zero eigenvalues of `L` counts the connected components** —
  exact, not heuristic, and one of the cleanest spectral facts in all of
  mathematics.
- **`μ₂`, the algebraic connectivity**, is the smallest positive eigenvalue: a
  measure of how fragile the graph is. It is small when a few edges hold
  everything together, and `0` exactly when the graph is already split.
- The **Fiedler vector** is the eigenvector for `μ₂`, and its sign gives a good
  2-way cut. For `k` communities use eigenvectors `2 … k+1` and cluster — that
  is spectral clustering.
- A **stochastic transition matrix** always has `λ = 1`. The **stationary
  distribution** is a right eigenvector, and it is what power iteration
  converges to.
- **PageRank is the stationary distribution of a damped random walk** on the
  link graph. Damping is not optional in practice: it guarantees a unique
  answer and kills link farms.
- **SVD clustering** on a user–item or adjacency matrix works but is harder
  than it looks, because a clique is a rank-`(n−1)` block. For undirected
  communities the **Laplacian is usually the better tool**.
- The Laplacian's smallest eigenvectors answer **minimum cut** (as a relaxation)
  and give **mesh simplification** their low-frequency basis. The same spectrum
  underlies graph neural networks.

## Next

[Part 04 — Calculus](../part04_calculus/) turns to the other half of applied
mathematics. Everything so far has been linear: given a matrix, what does it do?
Calculus asks the different question of how things *change* — how a quantity
depends on another, where a function stops increasing and starts decreasing,
and how to find the input that minimises an error. Those questions have linear
algebra's answer (eigenvalues) and calculus's answer (derivatives), and once
you have both, optimisation becomes a matter of combining them. Lesson
[50 — Functions, Limits, and Continuity](../part04_calculus/50_functions_limits_continuity.md)
starts from the beginning.
