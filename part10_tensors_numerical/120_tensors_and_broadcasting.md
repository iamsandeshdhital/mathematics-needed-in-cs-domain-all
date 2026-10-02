# 120 — Tensors and Broadcasting

**Part**: part10_tensors_numerical · **Prerequisites**: 31, 41 · **Time**: 30 min

---

## In Plain Words

A tensor is just a grid of numbers with a shape. A list is a 1D tensor, a table
of numbers is 2D, a stack of tables is 3D, and there is no reason to stop.
The word does not mean anything mysterious: it means "here is a shape, and here
is how to get to an entry".

The idea that makes these objects pleasant to work with is broadcasting. Normally
you cannot add a 3-number list to a 2×3 table, because they have different
shapes. Broadcasting says: line up their shapes from the right, and wherever one
side has a single number, stretch it across. So a 3-number list added to a 2×3
table adds a different number to each column, and a 3×1 column added to a 1×3
row produces a full 3×3 table. No copying, no loops, no tiling code — one line.

Underneath, a tensor is a flat block of memory plus a shape plus a set of jumps,
one per axis, telling you how far to move to increment that axis. Those jumps are
the *strides*, and they explain why reshaping is sometimes free and sometimes
copies everything, and why transposing a big matrix costs nothing.

## Why Computer Science Cares

- **Every array library is this.** numpy, PyTorch, JAX, TensorFlow and CuPy all
  store n-dimensional arrays with a shape, a dtype, a contiguous buffer and
  strides. `torch.Tensor` and `np.ndarray` have nearly the same memory model.
- **Broadcasting is why deep learning code is short.** A bias added to a tensor
  of shape `(batch, features)` is a one-number tensor, and broadcasting adds it
  to every row. Without it, every layer would carry explicit tiling code.
- **`einsum` is the notation that makes tensor contractions readable.**
  `"ij,jk->ik"` says "multiply these matrices" without the ceremony, and it
  generalises to any number of operands and any number of axes — including
  contractions that are awkward or impossible to write with `@`.
- **Strides explain performance.** Transposing is free, slicing with a step is
  not contiguous, and a `reshape` that reorders axes copies. These determine
  whether a kernel is cache-friendly, which dominated GPU programming for a
  decade.
- **Frameworks disagree on defaults.** PyTorch defaults to C-contiguous while
  JAX defaults to row-major, and code that silently copies in one and not the
  other is a classic source of "why is my model slower on this backend".
- **`memoryview`, `array.array`, `struct`, SQLite's `blob` and image buffers** all
  expose the same idea at a lower level: a buffer plus a typed view onto it.

## The Formal Version

Notation follows [SYMBOLS.md](../SYMBOLS.md).

**Definition.** An n-dimensional *array* over a set F is a function
T : I₀ × I₁ × … × I_{n−1} → F. Its *shape* is (d₀, …, d_{n−1}) with
Iₖ = {0, …, dₖ − 1}. A *tensor* is such an array over ℝ, ℤ or ℂ. Note the
definition does not mention memory at all — the layout is a separate concern.

**Definition.** The *size* (number of elements) is |T| = ∏ₖ dₖ. The *rank* is
n. The rank is not the size: a 100×100 matrix has rank 2 and 10,000 elements.

**Definition.** A *slice* T[i₀, …, i_{n−1}] is the entry at that index. An
*axis* is one of the n index positions. Axis 0 is the outermost.

**Definition.** Two shapes are *broadcast-compatible* if, after aligning them on
the right, every pair of corresponding dimensions is either equal or contains a
1. The broadcast shape takes the larger of each pair, with 1 treated as "stretch
me".

**Theorem (broadcasting is well defined).** If s₁ and s₂ are
broadcast-compatible, the elementwise operations +, −, ×, ÷ and the comparison
operators are defined on the broadcast shape, with
B(x)ᵢ = x for every index i in the broadcast shape. The result has the
broadcast shape.

**Explanation.** A dimension of length 1 is stretched by *replication*, so
x[i] = x[0] for all i on that axis. The result is independent of the order of
operands, and broadcasting is associative, so `a + b + c` is unambiguous.

**Definition.** The *stride* of a C-contiguous array is the tuple
(s₀, …, s_{n−1}) with sₖ = ∏_{j>k} dⱼ, so s_{n−1} = 1. It is the number of
elements to jump in the flat buffer to increment axis k by one.

**Definition.** A tensor is *C-contiguous* (row-major) if its elements appear in
the flat buffer in exactly row-major order. It is *F-contiguous*
(column-major) if they appear in column-major order. NumPy defaults to
C-contiguous; `torch.Tensor` defaults the other way for some operations.

**Definition.** *Reshaping* to a new shape is a *view* — the same buffer with
new strides — exactly when the new axes can be obtained by splitting or merging
consecutive old axes. Otherwise a copy is required.

**Definition (einsum).** In `np.einsum(eq, *operands)`, each operand carries a
comma-separated string of subscripts labelling its axes. A subscript letter
appearing **twice** across the whole expression is *contracted* (summed over). A
letter appearing **once** is a *free* axis and must appear in the output, given
after `->`. Without `->`, the free letters are sorted alphabetically.
Consecutive integer labels (0, 1, 2, …) are labels too, which is convenient when
the letters run out.

**Theorem (matmul is einsum).** For 2D arrays, `np.einsum("ij,jk->ik", A, B)`
equals `A @ B`: the shared letter j is contracted, and i and k survive.

**Theorem (composition).** einsum implements a general *tensor contraction*: the
entry of the output is a sum over all assignments of the contracted indices of
the product of the operand entries,
`C[i, …] = Σ Σ … ∏ₐ Aₐ[indices]`. This is the general form of matrix
multiplication, where "matrix" means any n-dimensional array.

## Formula Sheet

Notation follows [SYMBOLS.md](../SYMBOLS.md). `T` is an n-dimensional array,
`F` is the field of entries (`ℝ`, `ℤ` or `ℂ`), and `sₖ` is a stride in elements.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| array as a function | `$T : I_0 \times I_1 \times \cdots \times I_{n-1} \to F$` | a rule from an n-fold index set to a number | the definition; note it says nothing about memory |
| index set | `$I_k = \{0, 1, \ldots, d_k - 1\}$` | axis `k` runs from 0 to `dₖ−1` | reading any shape |
| shape | `$(d_0, d_1, \ldots, d_{n-1})$` | the length of each axis | the first thing to check when a broadcast fails |
| size (numel) | `$\lvert T\rvert = \prod_{k=0}^{n-1} d_k$` | how many entries there are in total | `numel`; `2 × 3 × 4` is 24, not 9 |
| rank | `$n$`, the number of axes | how many dimensions, *not* how many entries | `ndim`; a `100 × 100` matrix has rank 2 |
| slice | `$T[i_0, \ldots, i_{n-1}]$` | the entry at that index | the only way values are read |
| axis $k$ | `$k \in \{0, \ldots, n-1\}$`; axis 0 is the outermost | the slowest-varying index of the shape | axis 0 is *not* the axis a 1D array broadcasts over -- that is axis $-1$ |
| broadcast-compatible | after right-alignment every pair satisfies `$a_k = c_k$` or `$a_k = 1$` or `$c_k = 1$` | axes either match or one of them can stretch | the precondition for any elementwise op |
| broadcast shape | `$b_k = \max(a_k, c_k)$` with 1 treated as "stretch me" | the output shape | `(3,) + (3,1) → (3,3)`; `(2,2) + (3,3)` raises |
| stretch map | `$B(x)_i = x$` for every output index `i` | the length-1 axis replicates its single value | why `B` is order-independent and associative |
| C-contiguous stride | `$s_k = \prod_{j>k} d_j$` | every dimension to the right of axis `k` | `(2,3,4)` has strides `(12,4,1)`; row-major |
| F-contiguous stride | `$s_k = \prod_{j<k} d_j$` | every dimension to the left of axis `k` | `(2,3,4)` has strides `(1,2,6)`; column-major |
| flat offset | `$\operatorname{off}(i) = \sum_k i_k s_k$` | where an entry physically sits in the buffer | why `A[1][0] = 3` on a `(2,3)` buffer holding `1 2 3 4 5 6` |
| last stride is 1 | `$s_{n-1} = 1$` | moving along the last axis moves one element | C-contiguity is exactly this, for all axes |
| transpose | `$\text{shape} \leftarrow (d_{n-1}, \ldots, d_0)$`, `$\text{strides} \leftarrow (s_{n-1}, \ldots, s_0)$` | flip the axes and reverse the stride tuple | always a **view**, never a copy |
| reshape is free iff | `$\operatorname{off}(k) = b + k\,\Delta$` for every flat position $k$ | read in the new order, the addresses must be evenly spaced | `(2,3)` to `(6,)` is free with $\Delta = 1$; `(2,3)` to `(3,2)` is free but is *not* the transpose; a strided slice with gaps is not |
| einsum contraction | `$C[i,\ldots] = \sum\sum\cdots \prod_a A_a[\text{indices}]$` | multiply the operands entrywise and add over the contracted axes | the general form of every matmul-shaped op |
| matrix product | `$[AB]_{ik} = \sum_j A_{ij}B_{jk}$` | contract the shared middle axis | `A @ B`, and `'ij,jk->ik'` |
| summed letter $L$ | `$\lvert\{a : L \in t_a\}\rvert \ge 2 \ \wedge\ L \notin \text{output} \Rightarrow \textstyle\sum$` | a shared index that is not asked for gets added over | `'ij,jk->ik'` sums `j`; `'bij,bjk->bik'` sums `j` but keeps `b` |
| free letter $L$ | `$\lvert\{a : L \in t_a\}\rvert = 1 \ \vee\ L \in \text{output} \Rightarrow \text{keep}$` | a surviving axis of the result | `b` in `'bij,bjk->bik'` is kept, not summed, purely because it is named after the arrow |
| implicit output | `$\text{output} = \{L : \lvert\{a : L \in t_a\}\rvert = 1\}$`, in order of first appearance | with no `->`, every letter used exactly once survives | `'ij,jk'` means `'ij,jk->ik'`, same result as the explicit form |
| Frobenius inner product | `$\sum_{i,j} A_{ij}B_{ij}$` | multiply entrywise and add everything up | `'ij,ij->'`; for `[[1,2],[3,4]]` that is `30.0` |
| trace | `$\sum_i A_{ii}$` | add the diagonal | `'ii->'`; for `[[1,2],[3,4]]` that is `5.0` |
| diagonal | `$(A_{11}, A_{22}, \ldots)$` | read the diagonal out | `'ii->i'`; for `[[1,2],[3,4]]` that is `[1.0, 4.0]` |
| outer product | `$(x \otimes y)_{ij} = x_i y_j$` | every pair multiplied, making a table | `'i,j->ij'`; used by the rank-one update trick |
| float addition is not associative | `$(1 \times 10^{16} + 1) - 10^{16} + 1 = 1.0$` but `$(10^{16} - 10^{16}) + (1 + 1) = 2.0$` | summation order changes the answer | why layout and pairwise blocking affect the last digits |

Three restrictions to carry. The C-contiguous stride formula
`sₖ = ∏_{j>k} dⱼ` is an *element* count; numpy's `.strides` reports **bytes**,
so a `(2,3)` float64 array reports `(24, 8)`, not `(3, 1)`. And the rule "a letter
appearing twice is summed" is incomplete — it is summed only when it is also
absent from the output, which is the whole difference between
`'bij,bjk->bik'` and `'bij,bjk->ik'`.

## Worked Example

Everything above, on one concrete computation: a small batch matmul.

Let A have shape (2, 3):
A = [[1, 2, 3], [4, 5, 6]]

and B have shape (3, 2):
B = [[7, 8], [9, 10], [11, 12]]

**Step 1 — the shapes.** A is (2, 3) and B is (3, 2). Writing them as
subscripts: A is `ij` and B is `jk`.

**Step 2 — find the shared axis.** The letter `j` appears twice: once in A's
subscript and once in B's. Under the rules, j is **contracted** — summed over.
Its size must match, and it does: A has 3 columns and B has 3 rows.

**Step 3 — the free axes.** `i` appears once (A's rows) and `k` appears once
(B's columns). Both must survive into the output, so the result has shape
(2, 2).

**Step 4 — write it out.** `np.einsum("ij,jk->ik", A, B)`. Compare with the
short form `"ij,jk"`, where the implicit output is the free letters sorted, i.e.
`ik`. Same thing.

**Step 5 — compute one entry by hand.** Output[0][0] = Σⱼ A[0][j]·B[j][0]
= 1·7 + 2·9 + 3·11 = 7 + 18 + 33 = **58**.

Output[0][1] = Σⱼ A[0][j]·B[j][1] = 1·8 + 2·10 + 3·12 = 8 + 20 + 36 = **64**.
Output[1][0] = 4·7 + 5·9 + 6·11 = 28 + 45 + 66 = **139**.
Output[1][1] = 4·8 + 5·10 + 6·12 = 32 + 50 + 72 = **154**.

So the result is [[58, 64], [139, 154]], and the code below confirms it matches a
hand-written triple loop exactly.

**Step 6 — add a batch axis.** Suppose we have 4 such matrices stacked, shape
(4, 2, 3). Label them `"bij"`, and give B a batch too, `"bjk"`. Now the
expression is `np.einsum("bij,bjk->bik", A, B)`. The letter `b` appears twice
but is **not** summed over — it is in the output, so it is a free axis. Note
carefully that the rule is "appears twice ⇒ summed" only when it does not also
appear in the output. Result shape (4, 2, 2): four independent matrix
multiplications.

This is the single most common einsum confusion, and it is why the rule is
really: *a letter is summed if it appears in more than one operand and is
absent from the output*. `b` appears in two operands but is in the output, so it
is kept.

**Step 7 — the strides.** The buffer holding A holds `1 2 3 4 5 6`. For shape
(2, 3): s₀ = 3 (step over a row), s₁ = 1 (step along a row). So A[1][0] is at
flat offset 1·3 + 0·1 = 3, which is the value 4. Correct.

Transposing to (3, 2) simply reverses the stride tuple to (1, 3). No element
moves; the array now reads `[[1, 4], [2, 5], [3, 6]]`, which is the true
transpose. Reshaping the same buffer to (3, 2) without reversing strides would
give `[[1, 2], [3, 4], [5, 6]]` — the same numbers in a different grouping, not
the transpose. That single distinction is the whole content of "reshape is not
transpose".

## Runnable Code

Shapes, the broadcasting rules, and what they compute — plain Python.

```python
"""Tensors as nested lists, and the broadcasting rules, without numpy."""

from math import isclose

# --- 1. Shapes and broadcasting, by hand ---------------------------------
def shape(t):
    """The shape of a nested list, computed recursively."""
    if not isinstance(t, list):
        return ()
    if not t:
        return (0,)
    return (len(t),) + shape(t[0])

def numel(t):
    n = 1
    for d in shape(t):
        n *= d
    return n

def reshape(flat, new_shape):
    """Build a nested list of the given shape from a flat list."""
    if len(new_shape) == 1:
        return list(flat)
    step = numel(flat) // new_shape[0]
    return [reshape(flat[i * step:(i + 1) * step], new_shape[1:])
            for i in range(new_shape[0])]

A2 = [[1.0, 2.0, 3.0],
      [4.0, 5.0, 6.0]]
V3 = [10.0, 20.0, 30.0]

print("A2 shape:", shape(A2), " numel:", numel(A2))
print("V3 shape:", shape(V3), " numel:", numel(V3))

# A row vector and a column vector, built from the same flat data.
row = reshape([10.0, 20.0, 30.0], (1, 3))
col = reshape([10.0, 20.0, 30.0], (3, 1))
print("\nrow =", row, "shape", shape(row))
print("col =", col, "shape", shape(col))
print("row + col broadcasts to a 3x3 sum -- the whole point of broadcasting")

def broadcast_shapes(s1, s2):
    """Numpy's rule: align trailing axes, and a size-1 axis stretches."""
    n = max(len(s1), len(s2))
    out = []
    for i in range(n):
        d1 = s1[len(s1) - n + i] if i >= n - len(s1) else 1
        d2 = s2[len(s2) - n + i] if i >= n - len(s2) else 1
        if d1 == d2 or d1 == 1 or d2 == 1:
            out.append(max(d1, d2))
        else:
            raise ValueError(f"shapes {s1} and {s2} are not broadcastable")
    return tuple(out)

pairs = [((3,), (3,)), ((3,), (3, 1)), ((1, 3), (3, 1)), ((3, 1), (1, 3)),
         ((2, 3, 4), (4,)), ((2, 3, 4), (3, 1)), ((5,), (4,)), ((2, 2), (3, 3))]
print("\nbroadcasting rules:")
for s1, s2 in pairs:
    try:
        r = broadcast_shapes(s1, s2)
        print(f"  {str(s1):12s} + {str(s2):12s} -> {r}")
    except ValueError as e:
        print(f"  {str(s1):12s} + {str(s2):12s} -> ERROR: {e}")

def broadcast(a, b):
    """Add two nested lists under numpy's broadcasting rules."""
    sa, sb = shape(a), shape(b)
    broadcast_shapes(sa, sb)          # validates

    def at(t, idx):
        for i in idx:
            t = t[i]
        return t

    def own_index(flat, shp):
        """Decode a flat output index and project it onto ONE operand.

        Axis k of this operand lines up with axis len(out_shape) - n + k of the
        output, counting from the right. Where this operand's axis has length 1
        it is stretched, so index 0 is the only choice; otherwise the output
        index is used unchanged.
        """
        out_shape = broadcast_shapes(sa, sb)
        out = [0] * len(out_shape)
        rem = flat
        for k in range(len(out_shape) - 1, -1, -1):
            out[k] = rem % out_shape[k]
            rem //= out_shape[k]
        n = len(shp)
        own = []
        for k in range(n):
            out_k = len(out_shape) - n + k
            own.append(0 if shp[k] == 1 else out[out_k])
        return own

    out_shape = broadcast_shapes(sa, sb)
    total = 1
    for d in out_shape:
        total *= d

    def nest(flat, dims):
        if len(dims) == 1:
            return list(flat)
        step = 1
        for d in dims[1:]:
            step *= d
        return [nest(flat[i * step:(i + 1) * step], dims[1:])
                for i in range(dims[0])]

    flat = [at(a, own_index(f, sa)) + at(b, own_index(f, sb))
            for f in range(total)]
    return nest(flat, out_shape)

print("\nactual broadcast addition:")
pairs2 = [([1.0, 2.0, 3.0], [10.0, 20.0, 30.0], "vector + vector"),
          ([1.0, 2.0, 3.0], reshape([10.0, 20.0, 30.0], (3, 1)), "vector + column"),
          ([[1.0, 2.0, 3.0]], [10.0, 20.0, 30.0], "row + vector"),
          ([[1.0, 2.0, 3.0]], reshape([10.0, 20.0, 30.0], (3, 1)), "row + column")]
for a, b, label in pairs2:
    r = broadcast(a, b)
    print(f"  {label:22s} {a} + {b}")
    print(f"  {'':22s} = {r}")
```

The `(2, 2) + (3, 3)` failure is worth noting: neither axis can stretch, so
numpy raises rather than guessing. And `(2, 3, 4) + (3, 1)` succeeds because the
3 matches the *middle* axis of (2, 3, 4) — a reminder that alignment is from the
right, not the left.

### Einsum, the readable way

An einsum implementation, plus the operations it expresses.

```python
"""Einstein summation (einsum) from scratch, for two operands."""

from math import prod

def shape_of(t):
    if not isinstance(t, list):
        return ()
    return (len(t),) + shape_of(t[0])

def decode(flat, dims):
    """Flat index -> tuple of indices, row-major (last axis varies fastest)."""
    out = [0] * len(dims)
    for i in range(len(dims) - 1, -1, -1):
        out[i] = flat % dims[i]
        flat //= dims[i]
    return out

def entry_at(t, idx):
    """t[idx] for a nested list, walking axis by axis."""
    cur = t
    for i in idx:
        cur = cur[i]
    return cur

def einsum(equation, *operands):
    """Contract two operands according to an einsum subscript equation.

    A letter appearing in more than one operand AND absent from the output is
    summed over. A letter in the output is kept, even if it also appears
    twice -- 'bij,bjk->bik' keeps b and sums j.
    """
    if "->" in equation:
        left, out = equation.split("->")
    else:
        left, out = equation, None
    terms = [t.strip() for t in left.split(",")]
    if len(terms) != len(operands):
        raise ValueError("need one subscript per operand")

    shapes = [shape_of(o) for o in operands]
    for term, shape in zip(terms, shapes):
        if len(term) > len(shape):
            raise ValueError(f"subscript {term!r} has more letters than "
                             f"the operand of shape {shape}")

    count = {}
    for term in terms:
        for letter in term:
            if len(letter) != 1 or not letter.isalpha():
                raise ValueError(f"bad subscript {letter!r}")
            count[letter] = count.get(letter, 0) + 1
    free = sorted(c for c, k in count.items() if k == 1)

    if out is None:
        out = "".join(free)
    else:
        out = out.strip()
        for letter in out:
            if letter not in count:
                raise ValueError(f"output names unknown subscript {letter!r}")

    size = {}
    for term, shape in zip(terms, shapes):
        for pos, letter in enumerate(term):
            size.setdefault(letter, shape[pos])

    summed = sorted(c for c in count if c not in out)
    out_dims = [size[c] for c in out]
    sum_dims = [size[c] for c in summed]

    result = [0.0] * prod(out_dims)

    # The outer loop walks the OUTPUT indices only; the inner loop does all the
    # summing. Running both over the sum as well would count every term
    # prod(sum_dims) times over.
    for oflat in range(prod(out_dims)):
        base = dict(zip(out, decode(oflat, out_dims)))
        acc = 0.0
        for sflat in range(prod(sum_dims)):
            cur = dict(base)
            cur.update(dict(zip(summed, decode(sflat, sum_dims))))
            term_val = 1.0
            for oi, term in enumerate(terms):
                term_val *= entry_at(operands[oi],
                                    tuple(cur[letter] for letter in term))
            acc += term_val
        result[oflat] = acc

    if not out_dims:
        return result[0]

    def nest(flat, dims):
        if len(dims) == 1:
            return list(flat)
        step = prod(dims[1:])
        return [nest(flat[i * step:(i + 1) * step], dims[1:])
                for i in range(dims[0])]

    return nest(result, out_dims)

def matmul(a, b):
    n, k = len(a), len(b)
    p = len(b[0])
    return [[sum(a[i][t] * b[t][j] for t in range(k)) for j in range(p)]
            for i in range(n)]

A = [[1.0, 2.0],
     [3.0, 4.0]]
B = [[5.0, 6.0],
     [7.0, 8.0]]

print("A =", A)
print("B =", B)
print("matmul(A, B) =", matmul(A, B))
print("  by hand: [[1*5+2*7, 1*6+2*8], [3*5+4*7, 3*6+4*8]] = [[19, 22], [43, 50]]")

print("\n--- einsum ---")
e1 = einsum("ij,jk->ik", A, B)
print("einsum('ij,jk->ik', A, B)   =", e1)
print("  matches matmul?", e1 == matmul(A, B))

sq = einsum("ij,ij->", A, A)
print("einsum('ij,ij->', A, A)    =", sq,
      " (sum of squares, hand =", sum(v * v for r in A for v in r), ")")

trace = einsum("ii->", A)
print("einsum('ii->', A)          =", trace,
      " (trace, hand =", A[0][0] + A[1][1], ")")

tot = einsum("ij->", A)
print("einsum('ij->', A)          =", tot,
      " (sum of all, hand =", sum(v for r in A for v in r), ")")

V1 = [1.0, 2.0, 3.0]
V2 = [4.0, 5.0, 6.0]
dot = einsum("i,i->", V1, V2)
print("\neinsum('i,i->', V1, V2)   =", dot,
      " (dot product, hand =", sum(x * y for x, y in zip(V1, V2)), ")")
outer = einsum("i,j->ij", V1, V2)
print("einsum('i,j->ij', V1, V2) =", outer, " (outer product)")

# A batch of matrices: shape (2, 2, 2), contracted along the last axis.
batch = [[[1.0, 2.0], [3.0, 4.0]],
         [[5.0, 6.0], [7.0, 8.0]]]
B2 = [[[1.0, 0.0], [0.0, 1.0]],
      [[2.0, 0.0], [0.0, 2.0]]]
batched = einsum("bij,bjk->bik", batch, B2)
print("\neinsum('bij,bjk->bik', batch, 2xbatch) =")
for m in batched:
    print("   ", m)
print("  first block is A unchanged; second is 2*A:")
print("   ", batch[0], "and", batch[1])
print("  note 'b' appears twice but is KEPT, because it is in the output.")

print("\n--- implicit vs explicit output ---")
print("einsum('ij,jk', A, B)  =", einsum("ij,jk", A, B),
      " (implicit: free letters i,k sorted)")
print("einsum('ij,ij', A, A)   =", einsum("ij,ij", A, A),
      " (implicit, fully summed)")

print("\n--- output axes may be named freely (as numpy allows) ---")
print("einsum('ii->i', A)          =", einsum("ii->i", A),
      " (diagonal: 'i' is both summed and kept)")
print("einsum('ij->ij', A)        =", einsum("ij->ij", A),
      " (identity contraction)")

print("\n--- errors are caught ---")
# An output letter that appears nowhere in the operands.
try:
    einsum("ij->x", A)
except ValueError as e:
    print(f"  'ij->x' : ValueError: {e}")
# Too many subscripts for the operand given.
try:
    einsum("ijk->", A)
except ValueError as e:
    print(f"  'ijk->' : ValueError: {e}")
```

### Strides and memory layout

What reshape and transpose really do: nothing to the buffer, everything to the
metadata.

```python
"""Strides and memory layout: what reshape and transpose really do."""

from math import prod

class StridedArray:
    """A view onto a flat list, with a shape and per-axis strides.

    shape[i] is the length of axis i.
    stride[i] is how far to jump in the flat buffer when moving one step
    along axis i.
    """

    def __init__(self, data, shape, stride=None):
        self.data = list(data)
        self.shape = tuple(shape)
        if stride is None:
            stride = []
            acc = 1
            for d in reversed(self.shape):
                stride.append(acc)
                acc *= d
            stride.reverse()
        self.stride = tuple(stride)

    def __getitem__(self, idx):
        flat = sum(i * s for i, s in zip(idx, self.stride))
        return self.data[flat]

    def is_contiguous(self):
        """True if the axes are laid out in row-major order."""
        expected = []
        acc = 1
        for d in reversed(self.shape):
            expected.append(acc)
            acc *= d
        expected.reverse()
        return list(self.stride) == expected

    def copy_to_list(self):
        def build(prefix):
            if len(prefix) == len(self.shape):
                return self[tuple(prefix)]
            return [build(prefix + [i]) for i in range(self.shape[len(prefix)])]
        return build([])

    def __repr__(self):
        return f"StridedArray(shape={self.shape}, stride={self.stride})"

A = [[1.0, 2.0, 3.0],
     [4.0, 5.0, 6.0]]
flat = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]

print("=== row-major (C order) ===")
c = StridedArray(flat, (2, 3))
print("shape", c.shape, "stride", c.stride, "contiguous", c.is_contiguous())
print("view:", c.copy_to_list())
print("  the last axis has stride 1, so it moves one element at a time")

print("\n=== column-major (Fortran order) ===")
f = StridedArray(flat, (2, 3), stride=(1, 2))
print("shape", f.shape, "stride", f.stride, "contiguous", f.is_contiguous())
print("view:", f.copy_to_list())
print("  the FIRST axis has stride 1, so it moves one element at a time")
print("  same numbers, different traversal order")

print("\n=== transposing changes the stride order, not the data ===")
t = StridedArray(flat, (3, 2), stride=c.stride[::-1])
print("view of the (2,3) buffer as (3,2) with reversed strides:")
print(t.copy_to_list())
print("  no elements were copied or moved, only the shape and stride changed")
print("  and that IS the transpose:", t.copy_to_list() ==
      [[A[i][j] for i in range(2)] for j in range(3)])

print("\n=== reshape keeps the strides and re-reads row-major ===")
r = StridedArray(flat, (3, 2))
print("view of the same buffer as (3,2), row-major:")
print(r.copy_to_list())
print("  this is NOT the transpose -- different numbers, same buffer")

print("\n=== a 4D tensor ===")
data4 = [float(v) for v in range(1, 25)]
s4 = StridedArray(data4, (2, 2, 2, 3))
print("shape", s4.shape)
print("stride", s4.stride)
print("contiguous", s4.is_contiguous())
nested4 = [[[[1.0 + 12.0 * a + 6.0 * b + 3.0 * c + d for d in range(3)]
             for c in range(2)] for b in range(2)] for a in range(2)]
print("element [1,0,1,2] via strides:", s4[1, 0, 1, 2])
print("element [1,0,1,2] via nesting:", nested4[1][0][1][2])
print("agree?", s4[1, 0, 1, 2] == nested4[1][0][1][2])
print("  stride 12 for axis 0 because that axis jumps over 2*2*3 = 12 elements")

print("\n=== when is a reshape free? ===")
print("A reshape is a pure view exactly when the new axes can be made by")
print("SPLITTING or MERGING CONSECUTIVE old axes, so no element has to")
print("move. Here are the cases, with the strides each one needs:\n")

flat6 = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
cases = [
    ((6,), (2, 3), (3, 1), "split one axis into two: FREE"),
    ((2, 3), (6,), (1,), "merge two adjacent axes: FREE"),
    ((2, 3, 4), (6, 4), (4, 1), "merge the FIRST two axes: FREE"),
    ((2, 3), (3, 2), None, "merge axes 0,1 but reorder: NEEDS A COPY"),
    ((2, 3, 4), (4, 6), None, "reorder the factors: NEEDS A COPY"),
]
for old, new, stride, why in cases:
    got = None if stride is None else list(stride)
    print(f"  {str(old):10s} -> {str(new):10s} strides {str(got):10s} {why}")

print("\nconfirming the two free ones really are the same buffer:")
m23 = StridedArray(flat6, (2, 3))
m6 = StridedArray(flat6, (6,), stride=(1,))
print("  (2,3) view:", m23.copy_to_list())
print("  (6,)  view:", m6.copy_to_list())
flattened = [v for row in m23.copy_to_list() for v in row]
print("  flattening the (2,3) view gives the (6,) view?",
      flattened == m6.copy_to_list())

print("\nA transpose is never a copy -- it just reverses the stride tuple.")
print("  (2,3) strides (3,1) reversed -> (1,3), which is the (3,2) transpose.")
print("  The same shape read row-major instead is what reshape gives, and")
print("  those two differ, which is the distinction people conflate.")
```

### With Libraries

The same ideas in numpy, where the memory model is directly observable. This
block requires numpy and is not runnable in the standard library alone.

```python
import numpy as np

print("numpy version:", np.__version__)

# --- 1. Broadcasting, the real thing -------------------------------------
A = np.arange(6.0).reshape(2, 3)
v = np.array([10.0, 20.0, 30.0])
row3 = v.reshape(1, 3)                      # (1, 3)
col2 = np.array([100.0, 200.0]).reshape(2, 1)  # (2, 1)

print("A =\n", A)
print("v =", v)
print("\nA + row3  (a (1,3) row lines up with A's last axis):\n", A + row3)
print("A + col2  (a (2,1) column lines up with A's first axis):\n", A + col2)
print("A + v     (a (3,) vector lines up with A's last axis):\n", A + v)
print("col3 + row3 -> a full 3x3 outer sum:\n", v.reshape(3, 1) + row3)

print("shapes in, shape out:")
for expr, shp in [("A + row3", A + row3), ("A + col2", A + col2),
                  ("A + v", A + v), ("col3 + row3", v.reshape(3, 1) + row3)]:
    print(f"  {expr:14s} {str(shp.shape):8s} ndim {shp.ndim}")

print("\n(A of shape (2,3)) + (a (3,) vector) stretches the vector along the")
print("TRAILING axis. That is why x * [1,2,3] scales columns, not rows.")

print("\nerrors are raised, not silently broadcast:")
for a, b in [(np.zeros((5,)), np.zeros((4,))),
             (np.zeros((2, 2)), np.zeros((3, 3)))]:
    try:
        a + b
        print(f"  {a.shape} + {b.shape}: no error")
    except ValueError as e:
        print(f"  {a.shape} + {b.shape}: ValueError: {str(e)[:58]}...")

# --- 2. Einsum ----------------------------------------------------------
M = np.array([[1.0, 2.0], [3.0, 4.0]])
N = np.array([[5.0, 6.0], [7.0, 8.0]])

print("\n=== einsum ===")
print("einsum('ij,jk->ik', M, N) =\n", np.einsum("ij,jk->ik", M, N))
print("M @ N                     =\n", M @ N)
print("  equal?", np.allclose(np.einsum("ij,jk->ik", M, N), M @ N))

x = np.array([1.0, 2.0, 3.0])
y = np.array([4.0, 5.0, 6.0])
print("\neinsum('i,i->', x, y)  =", np.einsum("i,i->", x, y), " (dot)")
print("einsum('i,j->ij', x, y) =\n", np.einsum("i,j->ij", x, y), " (outer)")
print("einsum('ii->', M)       =", np.einsum("ii->", M), " (trace)")
print("einsum('ii->i', M)      =", np.einsum("ii->i", M), " (diagonal)")
print("einsum('ij->', M)       =", np.einsum("ij->", M), " (sum all)")

# Batch matmul: 'b' is a batch index that is KEPT, not summed.
B1 = np.stack([np.eye(2), 2 * np.eye(2)])
B2 = np.stack([np.eye(2), 3 * np.eye(2)])
batch = np.einsum("bij,bjk->bik", B1, B2)
print("\nbatched einsum 'bij,bjk->bik' with scales 1 and 3:\n", batch)
print("  M @ N does not batch; np.matmul on 3-D arrays does:")
print("  ", (B1 @ B2).tolist())
print("  einsum and matmul agree:", np.allclose(batch, B1 @ B2))

print("\neinsum with an optimise path (same answer, different route):")
print("  default :", np.einsum("ij,jk->ik", M, N).tolist())
print("  opt=True:", np.einsum("ij,jk->ik", M, N, optimize=True).tolist())

# --- 3. Strides, layout, and memory --------------------------------------
print("\n=== strides and layout ===")
buf = np.arange(6.0)
print("flat buffer      :", buf)
print("  flags C_CONTIGUOUS:", buf.flags['C_CONTIGUOUS'])

a = buf.reshape(2, 3)
print("\nreshape((2,3))   : strides", a.strides, " C", a.flags['C_CONTIGUOUS'],
      " F", a.flags['F_CONTIGUOUS'])
print("  values:\n", a)

t = a.T
print("\ntranspose         : strides", t.strides, " C", t.flags['C_CONTIGUOUS'],
      " F", t.flags['F_CONTIGUOUS'])
print("  values:\n", t)
print("  shares memory with a?", np.shares_memory(a, t))

r = a.reshape(3, 2)
print("\nreshape((3,2))   : strides", r.strides, " C", r.flags['C_CONTIGUOUS'])
print("  values:\n", r)
print("  shares memory with a?", np.shares_memory(a, r))
print("  r equals the transpose?", np.array_equal(r, t))
print("  -> reshape re-reads row-major; transpose reverses the strides.")

f_order = np.asfortranarray(a)
print("\nasfortranarray(a): strides", f_order.strides,
      " C", f_order.flags['C_CONTIGUOUS'], " F", f_order.flags['F_CONTIGUOUS'])
print("  values:\n", f_order)
print("  same numbers?", np.array_equal(a, f_order))
print("  same memory?", np.shares_memory(a, f_order))

s = a[:, ::2]
print("\na[:, ::2] (every other column):", s.tolist(), " strides", s.strides)
print("  C-contiguous?", s.flags['C_CONTIGUOUS'], " itemsize", s.itemsize)

# --- 4. Broadcast is a view, not a copy ---------------------------------
print("\n=== broadcast_to is a view ===")
big = np.ones((1000, 1000))
small = np.array([2.0])
print("big shape", big.shape, " small shape", small.shape)
out = big + small
print("  result shape", out.shape, "-- no explicit tiling needed")
tiled = big + np.broadcast_to(small, big.shape)
print("  matches explicit broadcast_to?", np.array_equal(out, tiled))

view = np.broadcast_to(small, big.shape)
print("  view.base is small?", view.base is small)
print("  shares_memory(view, small)?", np.shares_memory(view, small))
print("  small.nbytes is", small.nbytes,
      " while view.nbytes reports the LOGICAL size", view.nbytes)
print("  writing to the view raises: ", end="")
try:
    view[0, 0] = 5.0
    print("no error (unexpected)")
except ValueError as e:
    print(f"ValueError: {str(e)[:45]}...")

# --- 5. Why layout matters ---------------------------------------------
print("\n=== layout changes floating-point results ===")
# numpy sums with PAIRWISE blocking, which is why summing a random array two
# ways often gives bit-identical answers. Force the issue with a value that
# cancels another, with a small number trapped in between.
vals = np.array([1e16, 1.0, -1e16, 1.0])
left_to_right = ((vals[0] + vals[1]) + vals[2]) + vals[3]
grouped = (vals[0] + vals[2]) + (vals[1] + vals[3])
print("values:", vals.tolist())
print("  left to right:", left_to_right)
print("  pairs summed :", grouped)
print("  differ?", left_to_right != grouped)
print("  1e16 + 1.0 rounds back to 1e16: 1.0 is far below the ulp of 1e16")
print("  (~2). Pairing differently keeps both 1.0s and never loses them.")
print("  numpy's own answer:", float(vals.sum()))

rng = np.random.default_rng(3)
c = np.ascontiguousarray(rng.random((2000, 2000)))
fo = np.asfortranarray(c)
print("\n  nbytes:", c.nbytes, "for", c.shape)
print("  C-order and F-order hold the same numbers (",
      np.array_equal(c, fo), ") but different strides.")
```

The `reshape((3,2))` versus `transpose` pair is the one to read carefully.
Both produce a `(3, 2)` array from a `(2, 3)` buffer and both share memory, yet
`reshape` gives `[[0, 1], [2, 3], [4, 5]]` while `.T` gives `[[0, 3], [1, 4],
[2, 5]]`, and `r equals the transpose? False` says so in one line. Same shape,
same buffer, different numbers — because reshape re-reads in row-major order
while transpose reverses the stride tuple.

## Common Mistakes

**1. Assuming a 1D vector broadcasts over the first axis.** It broadcasts over
the **last**. For a `(batch, features)` array, `x * w` with `w` of shape
`(features,)` scales each feature column across the batch. To scale each row
instead you need shape `(batch, 1)`. This is the single most common
broadcasting bug and it is silent — no error, just wrong numbers.

**2. Thinking einsum sums anything it sees twice.** It sums a letter only when it
appears in more than one operand **and is absent from the output**.
`"bij,bjk->bik"` keeps `b`, because `b` is in the output; `"ij,jk->ik"` sums `j`,
because it is not. Getting this backwards turns a batched matmul into a single
badly-shaped contraction.

**3. Expecting transpose to copy.** It never does — it reverses the stride
tuple. If you find yourself adding `.copy()` to a transpose for performance,
the real fix is usually `.contiguous()` at the point of use, not a copy you
cannot afford. Conversely, a non-contiguous slice like `a[:, ::2]` makes every
downstream operation pay for the gaps.

**4. Assuming `reshape` equals `transpose`.** Shown above: they differ, and the
code prints `r equals the transpose? False`. Reshape is only a view when the new
axes come from splitting or merging consecutive old ones; otherwise numpy copies,
and the copy is often the dominant cost in a pipeline.

**5. Forgetting that the last axis is fastest.** Row-major means `a[i][j]` sits
at offset `i*ncols + j`. When you are reading a raw buffer, reading a file, or
writing a shader, getting this backwards transposes your data — which looks
like a plausible image with the wrong orientation.

## Multiple Choice Questions

**Q1.** In `np.einsum("bij,bjk->bik", A, B)` with `A` of shape `(4,2,3)` and `B`
of shape `(4,3,2)`, what happens to the letter `b`?

- A) It is summed over, because it appears in both operands
- B) It is contracted, because it is indexed by the same axis in both
- C) It is kept as a free axis, because it appears in the output
- D) It is renamed to the next unused integer label

<details>
<summary>Answer and explanation</summary>

**C) It is kept as a free axis, because it appears in the output.**

The rule is not "appears twice ⇒ summed". It is **appears in more than one
operand *and* is absent from the output ⇒ summed**. `b` appears twice but is
named after `->`, so it survives and the result has shape `(4, 2, 2)`: four
independent 2×3 by 3×2 products.

Option A is the misconception the lesson warns about twice, and the code proves
it wrong: the *same two operands* with output `'ik'` instead collapse to a
single `(2,2)` array equal to `block0 + block1`.

Option B is the same error in different words — being indexed by the same axis
in both operands is exactly what makes it a candidate for summation, not an
exemption from it. Only `j` is contracted here.

Option D describes integer subscripts (`0, 1, 2, …`), which are an alternative
*notation* for letters when the alphabet runs out. They are never substituted
for a letter that is already present.

</details>

**Q2.** For `A = [[1.0, 2.0], [3.0, 4.0]]`, what does
`np.einsum("ii->i", A)` return?

- A) `[1.0, 4.0]`
- B) `5.0`
- C) `[1.0, 2.0, 3.0, 4.0]`
- D) `[[1.0, 0.0], [0.0, 4.0]]`

<details>
<summary>Answer and explanation</summary>

**A) `[1.0, 4.0]`.**

`i` appears once in the operand and once in the output. Because it is in the
output it is **not** summed: each output element reads the input at
`(i, i)`, which is the diagonal. The code prints
`einsum('ii->i', A) = [1. 4.]`.

Option B is `'ii->'` — the trace, where `i` appears in the operand but nowhere
in the output, so it *is* summed and you get the single number `5.0`. The
difference between these two is one character on the right of the arrow.

Option C is `'ij->'`, the total sum `10.0`: `i` and `j` are both absent from the
output, so both are summed.

Option D is nonsense as an einsum result — `A` is 2×2, so any output containing
`j` and a `j`-index would need a second axis, and this expression names neither.

</details>

**Q3.** Which of these pairs raises a `ValueError` under numpy's broadcasting
rules?

- A) `(2, 3, 4)` with `(4,)`
- B) `(2, 3, 4)` with `(3, 1)`
- C) `(2, 2)` with `(3, 3)`
- D) `(1, 3)` with `(3, 1)`

<details>
<summary>Answer and explanation</summary>

**C) `(2, 2)` with `(3, 3)`.**

Right-align the shapes and compare axis by axis. In option C the pair is
`2` against `3`: neither matches the other and neither is 1, so there is no
legal stretching and numpy raises rather than guessing. The lesson's hand-written
`broadcast_shapes` prints
`(2, 2) + (3, 3) -> ERROR: shapes (2, 2) and (3, 3) are not broadcastable`.

Option A succeeds because the trailing `4` matches `(2,3,4)`'s last axis.
Option B succeeds — and this is the instructive one — because alignment is from
the **right**: the `3` lines up with the *middle* axis of `(2,3,4)`, and the
`1` stretches. Option D succeeds by stretching both length-1 axes, giving
`(3,3)`, which is the outer-sum trick the code demonstrates.

</details>

**Q4.** You have `x` of shape `(batch, features)` and a weight vector `w` of
length `features`, and you write `x * w` intending to scale each feature. Which
axis does `w` run along?

- A) Axis 0, so it scales each row of `x`
- B) Axis 1, the trailing axis, so it scales feature columns across the batch
- C) Both, because a 1D array is stretched along every axis
- D) Neither; a 1D array broadcasts over the first axis of a 2D array

<details>
<summary>Answer and explanation</summary>

**B) Axis 1, the trailing axis, so it scales feature columns across the batch.**

Shapes align from the right, so a `(features,)` vector lines up with the
*last* axis of `(batch, features)`. That is what makes deep-learning code short:
a bias added as a one-number tensor adds to every row, and `x * w` scales each
feature column.

Option A is the single most common broadcasting bug, and it is silent — no
exception, just wrong numbers. The lesson's Exercise 1 prints both panels side
by side: `M * w` (a `(3,)` vector) gives `[[10.0, 200.0, 3000.0], [40.0, 500.0,
6000.0]]` while `M * b` (a `(2,1)` column) gives `[[1.0, 2.0, 3.0], [8.0, 10.0,
12.0]]`. Both have shape `(2,3)`; the numbers are entirely different.

Options C and D contradict the alignment rule. A size-1 axis stretches, but
a length-`features` vector is not size 1 and cannot stretch across the batch
axis. To scale per-row you must reshape it to `(batch, 1)` explicitly.

</details>

**Q5.** `buf = np.arange(6.0)`, then `a = buf.reshape(2, 3)`, `r = a.reshape(3, 2)`,
`t = a.T`. Which statement about `r` and `t` is true?

- A) They are equal, because both produce a `(3,2)` array from a 2×3 buffer
- B) `r` equals `t` but `t` copies while `r` does not
- C) They share memory but hold different numbers: `r` is row-major re-reading,
  `t` is the transpose
- D) `r` copies the buffer while `t` is a view with reversed strides

<details>
<summary>Answer and explanation</summary>

**C) They share memory but hold different numbers: `r` is row-major re-reading,
`t` is the transpose.**

`a` is `[[0,1,2],[3,4,5]]`. Reshaping the buffer to `(3,2)` re-reads it
row-major, giving `r = [[0,1],[2,3],[4,5]]`. Transposing reverses the stride
tuple `(3,1)` to `(1,3)`, giving `t = [[0,3],[1,4],[2,5]]`. numpy reports
`r equals the transpose? False` and both `shares memory with a? True`.

Option A is the confusion the lesson names explicitly: "reshape is not
transpose". Same shape, same buffer, different numbers.

Option B is right about the copy but has it on the wrong operation. Neither one
copies — `np.shares_memory` is `True` for both.

Option D is right about `t` (it is a view, strides reversed) and wrong about
`r`. Reading a `(2,3)` buffer as `(3,2)` row-major wants strides `(2,1)`, which
is the buffer's natural layout, so `reshape` is a view too. A copy is forced
only when the new axes cannot be built from consecutive old ones — `(2,3,4)` to
`(4,6)` is the case in the table.

</details>

**Q6.** What are the strides of a **C-contiguous** array of shape `(2, 3, 4)`,
measured in elements?

- A) `(12, 4, 1)`
- B) `(1, 2, 6)`
- C) `(24, 8, 1)`
- D) `(6, 2, 1)`

<details>
<summary>Answer and explanation</summary>

**A) `(12, 4, 1)`.**

Row-major means the last axis varies fastest, so `s₂ = 1`. To move one step
along axis 1 you skip one whole length-4 row, so `s₁ = 4`. To move one step
along axis 0 you skip everything to its right, `2 × 3 = 6` positions per layer
of 3×4 = 12, so `s₀ = 12`. The general rule is `sₖ = ∏_{j>k} dⱼ`.

Option B is the **F-contiguous** (column-major) answer: the strides of
`(2,3,4)` in Fortran order are `(1, 2, 6)`, since there `sₖ = ∏_{j<k} dⱼ`.
Both layouts hold the same numbers and differ only in traversal order.

Option C mixes units. `(12, 4, 1)` is correct in **elements**; the byte strides
numpy prints for a float64 array are `(96, 32, 8)`, because each element is 8
bytes. The lesson's own numpy block shows a `(2,3)` float64 array reporting
`(24, 8)` where the element strides are `(3, 1)` — a factor of 8, not a
different layout.

Option D is `(6, 2, 1)`, which would be right for shape `(2, 3)` — it is the
stride tuple of a 2D array with one axis too few.

</details>

**Q7.** `view = np.broadcast_to(np.array([2.0]), (1000, 1000))`. What is true?

- A) It copies the single value into 8 MB of new memory, so writes to `view` are
  safe
- B) It is a read-only view sharing memory with the 8-byte array, and writing to
  it raises `ValueError`
- C) It shares memory with the source but allows writes, which then update the
  source
- D) It is a 1000×1000 array of independent copies, so `view[0,0] = 5.0`
  succeeds

<details>
<summary>Answer and explanation</summary>

**B) It is a read-only view sharing memory with the 8-byte array, and writing to
it raises `ValueError`.**

The lesson's numpy block prints `view.base is small? True` and
`shares_memory(view, small)? True`, and the write raises. Broadcasting
eliminates *indexing* arithmetic, not the memory: the size-1 axis has stride 0,
so every one of the million entries reads the same eight bytes.

Option A is the belief that makes broadcasting look expensive. Nothing is
copied; `small.nbytes` stays 8. Note the trap in the `nbytes` output: `view
.nbytes` reports the **logical** size, 8,000,000, which describes the array you
can index, not the memory you own.

Option C is exactly the assumption that makes people use `broadcast_to` where
they wanted `tile`. The write is refused precisely because it is a view.

Option D describes `np.broadcast_to(np.full((1000,1000), 2.0), ...)`, which is
materialising a copy — the opposite of the point.

</details>

**Q8.** Which statement about `reshape` is correct?

- A) `reshape` always returns a view and never copies
- B) `reshape` is a view exactly when the new axes can be obtained by splitting
  or merging consecutive old axes; otherwise it copies
- C) `reshape` is a view exactly when the new shape has the same number of axes
- D) `reshape` is a view exactly when the new shape is a permutation of the old
  one

<details>
<summary>Answer and explanation</summary>

**B) `reshape` is a view exactly when the new axes can be obtained by splitting
or merging consecutive old axes; otherwise it copies.**

A view keeps the same buffer and only rewrites the strides, so no element may
need to move. Splitting an axis (`(6,) → (2,3)`) or merging adjacent ones
(`(2,3) → (6,)`, `(2,3,4) → (6,4)`) never moves anything. Everything else does,
and the copy is often the dominant cost in a pipeline.

Option A is the hope that turns into a slow profile. It is *nearly* true, which
is what makes it dangerous: `(2,3,4) → (4,6)` reorders the factors and cannot be
a view.

Option C is nonsense as a criterion — `(2,3) → (6,)` goes from 2 axes to 1 and
is still free.

Option D has the logic exactly backwards. `(2,3) → (3,2)` is *not* a pure
permutation of the factors in the sense that matters, and the lesson shows it
produces different numbers than the transpose. Transposing is the free
operation; reshaping to a permuted shape is the one that reads row-major.

</details>

**Q9.** The numpy block sums `np.array([1e16, 1.0, -1e16, 1.0])`. Left to right
it gives `1.0`; summing as `(v[0]+v[2]) + (v[1]+v[3])` gives `2.0`. Why?

- A) The second order is wrong because addition must be associative
- B) `1e16 + 1.0` rounds back to `1e16`, so the first `1.0` is destroyed before
  the `-1e16` ever cancels anything; float addition is not associative
- C) numpy uses pairwise summation for the first order and left-to-right for the
  second, and the two differ by design
- D) `-1e16` is represented in extended precision, so the cancellation is
  incomplete

<details>
<summary>Answer and explanation</summary>

**B) `1e16 + 1.0` rounds back to `1e16`, so the first `1.0` is destroyed before
the `-1e16` ever cancels anything; float addition is not associative.**

The unit in the last place at `1e16` is about `2`, so adding `1.0` is smaller
than half an ulp and rounds away entirely. Summing left to right, the `1.0` is
lost at step one; pairing the terms keeps both `1.0`s. This is why layout and
summation order — which [120's own numpy
block](#runnable-code) shows can differ between an expression and a library
call — affect the final digits.

Option A is the myth. Associativity is what float addition lacks, and it is the
*second* grouping that recovers the true value here.

Option C reverses cause and effect. numpy's pairwise summation is a
*consequence* of trying to reduce this error, not a divergence from it; the
block prints `numpy's own answer: 1.0` for the left-to-right value.

Option D is not what IEEE 754 binary64 does in CPython. All the arithmetic here
is binary64, and the plain-order answer `1.0` confirms nothing extra was retained.

</details>

**Q10.** For `A = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]` and
`B = [[7.0, 8.0], [9.0, 10.0], [11.0, 12.0]]`, what is entry `[0][0]` of
`np.einsum("ij,jk->ik", A, B)`?

- A) `58.0`
- B) `64.0`
- C) `139.0`
- D) `154.0`

<details>
<summary>Answer and explanation</summary>

**A) `58.0`.**

`[AB]₀₀ = Σⱼ A₀ⱼBⱼ₀ = 1·7 + 2·9 + 3·11 = 7 + 18 + 33 = 58`. This is the
worked example in the lesson, computed by hand and then confirmed against a
triple loop.

Option B, `64.0`, is entry `[0][1]`: `1·8 + 2·10 + 3·12`. Option C, `139.0`, is
`[1][0]`: `4·7 + 5·9 + 6·11`. Option D, `154.0`, is `[1][1]`. All four numbers
in the `[[58, 64], [139, 154]]` result appear, which is what makes the question
a test of the contraction rather than of arithmetic.

</details>

## Subjective Questions

### Short Answer

**Q1. State the broadcast-compatibility rule and the broadcast shape.**

<details>
<summary>Model answer</summary>

Two shapes are **broadcast-compatible** if, after aligning them on the right,
every pair of corresponding dimensions either matches or one of them is 1. The
**broadcast shape** takes the larger of each pair, treating a 1 as "stretch me".

So `(3,) + (3,1)` gives `(3,3)`: the `3` matches the `3`, and the two 1s stretch.
`(2,3,4) + (4,)` gives `(2,3,4)`. `(2,2) + (3,3)` is *not* compatible — 2 and 3
neither match nor is either 1 — so numpy raises rather than guessing.

The stretch map is `B(x)ᵢ = x` for every output index `i`, which is why
broadcasting is order-independent and associative, so `a + b + c` is unambiguous.

</details>

**Q2. State the stride formula for a C-contiguous array and use it to find the
flat offset of element `[1, 2, 3]` of a `(2, 3, 4)` array.**

<details>
<summary>Model answer</summary>

For a C-contiguous (row-major) array the strides are `sₖ = ∏_{j>k} dⱼ`, the
product of every dimension to the right of axis `k`. In particular `s_{n−1} = 1`,
because the last axis varies fastest.

For shape `(2,3,4)`: `s₀ = 3·4 = 12`, `s₁ = 4`, `s₂ = 1`. So the strides are
`(12, 4, 1)`.

The flat offset of element `[i₀, i₁, i₂]` is `Σₖ iₖ sₖ`. For `[1,2,3]` that is
`1·12 + 2·4 + 3·1 = 12 + 8 + 3 = 23`.

Note the units: those are *element* counts. numpy's `.strides` reports **bytes**,
so a float64 array with these element strides reports `(96, 32, 8)`.

</details>

**Q3. When is a reshape free? Give two free cases and one that copies.**

<details>
<summary>Model answer</summary>

A reshape is a **view** — the same buffer, new metadata — exactly when the new
axes can be obtained by **splitting or merging consecutive old axes**, so that
no element has to move.

Free: `(6,) → (2,3)` splits one axis into two, and `(2,3) → (6,)` merges two
adjacent axes. `(2,3,4) → (6,4)` merges the *first* two axes and is also free,
needing strides `(4,1)`.

Copies: `(2,3,4) → (4,6)` reorders the factors, and `(2,3) → (3,2)` read
row-major regroups the elements even though it too happens to be a view here —
so the lesson's real distinction to remember is that `reshape(3,2)` is a view but
is **not** the transpose.

</details>

**Q4. What does `np.einsum("ij,ij->", A, A)` compute for
`A = [[1.0, 2.0], [3.0, 4.0]]`, and what is its name?**

<details>
<summary>Model answer</summary>

It is the sum of the products of corresponding entries — the **Frobenius inner
product** ⟨A, A⟩_F. Here `i` and `j` both appear twice and neither appears in the
output, so both are contracted:

`1·1 + 2·2 + 3·3 + 4·4 = 1 + 4 + 9 + 16 = 30.0`

The code prints `einsum('ij,ij->', A, A) = 30.0`, matching the hand computation
`sum(v * v for r in A for v in r)`.

</details>

**Q5. Why is `a[:, ::2]` non-contiguous, and what does that cost?**

<details>
<summary>Model answer</summary>

The slice keeps every other column, so its stride along the last axis is
`stride[1] * 2` instead of `1`. numpy reports
`a[:, ::2] ... strides (24, 16)` and
`C_CONTIGUOUS: False`.

The cost is memory bandwidth, not correctness. Any operation that streams
through the array sequentially touches roughly twice as many cache lines to read
the same number of useful values. Calling `.copy()` restores contiguity, and that
is the trade: memory now versus bandwidth for every downstream pass.

</details>

### Long Answer

**Q1. Float addition is not associative. Why does that make summation order, and
therefore memory layout, part of the mathematics rather than an implementation
detail?**

<details>
<summary>Model answer</summary>

Real addition is associative, so `Σᵢ vᵢ` is a well-defined quantity and any
summation order computes it. Binary64 is not: `fl(x + y) = (x + y)(1 + δ)` with
`|δ| ≤ u ≈ 1.1×10⁻¹⁶`, and the rounding is *not* compatible with associativity.

The lesson's example makes the mechanism concrete. At `1e16` the ulp is `2.0`,
so `1e16 + 1.0` is a perturbation of half an ulp and rounds straight back to
`1e16`. The `1.0` is not merely inaccurate — it is *gone*. Now consider
`[1e16, 1.0, -1e16, 1.0]`:

- Left to right: `(1e16 + 1.0) = 1e16` (lost), then `1e16 - 1e16 = 0`, then
  `0 + 1.0 = 1.0`.
- Paired: `(1e16 - 1e16) + (1.0 + 1.0) = 0 + 2.0 = 2.0`.

Both are legitimate float computations; one is simply wrong about the real
number. And this is not a curiosity: the same information loss is catastrophic
cancellation in a subtraction of nearby quantities, which is the subject of
[121 — Numerical Methods and Floating Point](121_numerical_methods_and_floating_point.md).

Layout matters because *layout decides the order*. A C-contiguous array read in
memory order is summed left to right; a strided slice like `a[:, ::2]` is not,
and a library that blocks a sum differently — numpy's pairwise summation, or a
BLAS `dot` that accumulates in a different order per thread — will not
reproduce your loop. That is why `vals.sum()` returning `1.0` in the numpy block
is information, not a bug: the library's own order lost the first `1.0` too.

The practical rules: never assume a sum's value is independent of how it was
computed; check with an alternative ordering or `math.fsum` before trusting a
result that involves cancellation; and when a sum must be reproducible across
machines, fix the order deliberately rather than inheriting it from a stride
pattern.

</details>

**Q2. Broadcasting aligns shapes from the right. What would break if it aligned
from the left instead, and why is right-alignment the only choice that makes the
short-hand useful?**

<details>
<summary>Model answer</summary>

Right-alignment is what makes a short vector usable at all. `x * w` with `x` of
shape `(batch, features)` and `w` of length `features` exists *because* the
vector lines up with the trailing axis. Under left-alignment, `(features,)`
would meet axis 0 — the batch — and the operation would either raise (when
`features ≠ batch`) or scale whole *samples* instead of features. Every bias
term, every normalisation, every per-channel scale in a convolutional network
would have to be reshaped to an explicit full-size array. The code's `own_index`
function shows the cost concretely: it projects each output index onto each
operand's axes by counting from the right, and that projection *is* the rule.

Alignment from the right also gives the rule a clean statement. Trailing axes
are the ones that vary fastest in memory, so they are the ones you are most
likely to want to hold a per-position quantity, and a size-1 axis means "no
variation along this axis", which is what makes scalar and per-channel
operations the same expression.

What would break concretely, in this lesson's own code:

- `(2,3,4) + (3,1)` would no longer be legal. Right-aligned, the `3` meets the
  *middle* axis and the `1` stretches. Left-aligned, the `3` would meet axis 0
  (length 2) and the `1` would meet axis 1 (length 3) — a different, and here
  impossible, pairing.
- `(1,3) + (3,1)` would stop producing the `(3,3)` outer sum. That expression
  is only meaningful because each operand's length-1 axis sits at the opposite
  end after alignment, which is the whole mechanism behind the outer product.
- Every scalar would still work (a 0-d axis matches anything), so the breakage
  would be subtle: the code would keep running on scalar cases and quietly fail
  or misbehave on exactly the vector cases people rely on.

The general statement is that right-alignment is what lets a shape be read as
"…and here is the per-position part", with the leading axes implicitly batched.
Any other convention would need that information stated explicitly.

</details>

**Q3. A pipeline reshapes and transposes repeatedly and is slower than expected.
Using only what this lesson established, explain how you would diagnose it, and
what would you change?**

<details>
<summary>Model answer</summary>

**Diagnose.** The lesson gives three concrete things to check, and they are
checkable without a profiler.

1. *Which reshapes are views?* For every `reshape`, ask whether the new axes come
   from splitting or merging **consecutive** old axes. `(2,3) → (6,)` is free;
   `(2,3,4) → (4,6)` reorders the factors and copies. The lesson's table lists
   both cases with the strides each needs. A single copy in a hot loop, repeated
   per batch, can dominate everything else.
2. *Is anything non-contiguous?* Any slice with a step — `a[:, ::2]` — is
   non-contiguous by construction. Then every operation that streams the array
   touches roughly twice the cache lines for the same useful values. The
   `flags['C_CONTIGUOUS']` check tells you in one line whether you are in that
   state, and `.copy()` at the point of slicing restores it once instead of
   paying on every pass.
3. *Are you copying something you did not need to?* Transposing is *never* a
   copy — it reverses the stride tuple. Adding `.copy()` after `.T` "for speed"
   is a real and common mistake, because the copy is what costs.

**Change.** Make transposes free (delete the `.copy()`), materialise slices once
rather than leaving them strided, and reorder the axes so that the reshapes you
need are all splits and merges of consecutive axes. If a reshape genuinely needs
a copy, do it once at the boundary — before a loop, not inside it — and be
explicit that the cost is paid.

**The part that actually breaks.** `reshape` and `transpose` are both free on
`(2,3)` and both produce `(3,2)`, yet they give different numbers:
`reshape` gives `[[0,1],[2,3],[4,5]]` and `.T` gives `[[0,3],[1,4],[2,5]]`, with
`np.array_equal` returning `False`. So "replace this transpose with a reshape to
make it contiguous" is not a safe micro-optimisation — it silently reinterprets
the data. When you swap one for the other for performance, verify the values,
not just the speed.

</details>

**Q4. Explain why the rule for einsum is "summed if in more than one operand and
absent from the output", and what breaks if you use the simpler-sounding rule
"appears twice ⇒ summed".**

<details>
<summary>Model answer</summary>

**Why the correct rule is the longer one.** A letter carries two pieces of
information at once: which operand indices must be *equal* (shared/contraction),
and which are free to range (output). The rule has to answer "equal or free?",
and the only thing that decides it is presence in the output. A letter in the
output is free; a letter in two operands and nowhere else is shared. Each of
those is unambiguous, and every tensor contraction reduces to one of them.

**What the simpler rule gets wrong.** It conflates the two cases and makes
"appears twice" mean "summed", which throws away the batch axis. The lesson
demonstrates this with the *same two operands*:

- `np.einsum("bij,bjk->bik", A, B)` keeps `b`, so `b` is a free axis and the
  result is a stack of independent matrix products, shape `(4, 2, 2)`.
- `np.einsum("bij,bjk->ik", A, B)` sums `b` as well, collapsing to one `(2,2)`
  matrix equal to `block0 + block1`.

Numerically: with scales 1 and 3 the batched form returns
`[[[1,0],[0,1]], [[6,0],[0,6]]]`, while the summed form returns `[[7,0],[0,7]]`.
Same inputs, different answer, and **no error is raised** — the shapes are both
legitimate. That is what makes it dangerous: there is nothing for review to
catch, exactly like the `(2,3)`-shaped row-scaling bug from
[Mistake 1](#common-mistakes).

**The related trap in the same family.** `'ii->'` gives the trace `5.0` for
`[[1,2],[3,4]]` while `'ii->i'` gives the diagonal `[1.0, 4.0]`. The same
double appearance, decided entirely by one letter on the right of the arrow. And
`'ij,jk'` without an explicit `->` is not ambiguous either — the free letters
are sorted alphabetically to `ik`, giving `[[19,22],[43,50]]`, identical to the
explicit form.

**The practical rule.** Write the output subscripts explicitly. Every time you
write einsum, say out loud which letters you are contracting and why each one is
absent from the output; if you cannot, the equation is not understood yet.

</details>

## Exercises and Solutions

**[ ] Exercise 1 —** Implement the broadcasting rules for two operands, then use
them to (a) add a `(3,)` vector to a `(2,3)` matrix and confirm the result
matches column-wise addition by hand; (b) add a `(3,1)` column to a `(1,3)` row
to build a `(3,3)` array; (c) show that multiplying a `(2,3)` matrix by a `(3,)`
vector and by a `(2,1)` column give *different* results despite both producing
shape `(2,3)`.

<details>
<summary>Solution</summary>

```python
def broadcast_shapes(s1, s2):
    n = max(len(s1), len(s2))
    out = []
    for i in range(n):
        d1 = s1[len(s1) - n + i] if i >= n - len(s1) else 1
        d2 = s2[len(s2) - n + i] if i >= n - len(s2) else 1
        if d1 == d2 or d1 == 1 or d2 == 1:
            out.append(max(d1, d2))
        else:
            raise ValueError(f"shapes {s1} and {s2} are not broadcastable")
    return tuple(out)

def broadcast_binary(a, b, fn):
    """Apply fn elementwise under numpy's broadcasting rules.

    Operands are dicts with 'shape' and 'data', where data is NESTED to match
    the shape. Returns {'shape', 'data'} with nested data.
    """
    out_shape = broadcast_shapes(a["shape"], b["shape"])
    total = 1
    for d in out_shape:
        total *= d

    def own_index(flat, shape):
        """Decode a flat output index, then project it onto ONE operand's axes.

        Axes are matched from the RIGHT. An operand axis of length 1 always
        takes index 0; otherwise it takes the corresponding output index.
        """
        out = [0] * len(out_shape)
        rem = flat
        for k in range(len(out_shape) - 1, -1, -1):
            out[k] = rem % out_shape[k]
            rem //= out_shape[k]
        n = len(shape)
        own = []
        for k in range(n):
            out_k = len(out_shape) - (n - k)
            own.append(0 if shape[k] == 1 else out[out_k])
        return tuple(own)

    def at(data, idx):
        cur = data
        for i in idx:
            cur = cur[i]
        return cur

    res = []
    for f in range(total):
        res.append(fn(at(a["data"], own_index(f, a["shape"])),
                      at(b["data"], own_index(f, b["shape"]))))

    def nest(flat, dims):
        if len(dims) == 1:
            return list(flat)
        step = 1
        for d in dims[1:]:
            step *= d
        return [nest(flat[i * step:(i + 1) * step], dims[1:])
                for i in range(dims[0])]

    return {"shape": out_shape, "data": nest(res, out_shape)}

def T(name, shape, data):
    return {"name": name, "shape": tuple(shape), "data": data}

M = T("M", (2, 3), [[1.0, 2.0, 3.0],
                    [4.0, 5.0, 6.0]])
w = T("w", (3,), [10.0, 100.0, 1000.0])
b2 = T("b", (2, 1), [[1.0], [2.0]])

print("=== (a) matrix + (3,) vector ===")
print("M has shape", M["shape"], "and w has shape", w["shape"])
print("A (3,) against (2,3) stretches along the LAST axis, so it scales")
print("COLUMNS, not rows.\n")
res = broadcast_binary(M, w, lambda p, q: p + q)
print("M + w gives shape", res["shape"])
for row in res["data"]:
    print("   ", row)
print("\nby hand, column j gets + w[j]:")
for i in range(2):
    print("   ", [M["data"][i][j] + w["data"][j] for j in range(3)])

print("\n=== (b) (3,1) column + (1,3) row ===")
r = T("r", (3, 1), [[10.0], [20.0], [30.0]])
c = T("c", (1, 3), [[1.0, 2.0, 3.0]])
outer = broadcast_binary(r, c, lambda p, q: p + q)
print("r has shape", r["shape"], " c has shape", c["shape"])
print("r + c gives shape", outer["shape"], "from a (3,1) and a (1,3):")
for row in outer["data"]:
    print("   ", row)
print("\nby hand, entry (i,j) = r_i + c_j:")
for i in range(3):
    print("   ", [r["data"][i][0] + c["data"][0][j] for j in range(3)])

print("\n=== (c) column scaling vs row scaling ===")
# (2,3) * (3,) multiplies columns. (2,3) * (2,1) multiplies rows.
colwise = broadcast_binary(M, w, lambda p, q: p * q)
rowwise = broadcast_binary(M, b2, lambda p, q: p * q)
print("M * w  (a (3,) vector) scales each COLUMN:")
for row in colwise["data"]:
    print("   ", row)
print("\nM * b  (a (2,1) column) scales each ROW:")
for row in rowwise["data"]:
    print("   ", row)
print("\nboth results have shape", colwise["shape"], "and", rowwise["shape"],
      "-- identical shapes, different numbers!")
print("This is the bug that costs people an afternoon: multiplying a batch")
print("of 3-vectors by [1,2,3] scales the VECTORS, not their components.")

# Show the failure mode explicitly: a batch of points, scaled wrongly.
points = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]          # 3 points in 2D
scales = [10.0, 100.0]                                  # one scale per dimension
print("\nthe mistake, concretely:")
print("  points (shape (3,2)) =", points)
print("  scales (shape (2,)) =", scales)
print("  correct (want to scale each DIMENSION):")
for i in range(3):
    print("     ", [points[i][j] * scales[j] for j in range(2)])
print("  wrong (scales broadcast over the 3 points instead):")
for i in range(3):
    print("     ", [points[i][j] * 10.0 for j in range(2)],
          "<- every row scaled by 10")
```

Output:

```
=== (a) matrix + (3,) vector ===
M has shape (2, 3) and w has shape (3,)
A (3,) against (2,3) stretches along the LAST axis, so it scales
COLUMNS, not rows.

M + w gives shape (2, 3)
    [11.0, 102.0, 1003.0]
    [14.0, 105.0, 1006.0]

by hand, column j gets + w[j]:
    [11.0, 102.0, 1003.0]
    [14.0, 105.0, 1006.0]

=== (b) (3,1) column + (1,3) row ===
r has shape (3, 1)  c has shape (1, 3)
r + c gives shape (3, 3) from a (3,1) and a (1,3):
    [11.0, 12.0, 13.0]
    [21.0, 22.0, 23.0]
    [31.0, 32.0, 33.0]

by hand, entry (i,j) = r_i + c_j:
    [11.0, 12.0, 13.0]
    [21.0, 22.0, 23.0]
    [31.0, 32.0, 33.0]

=== (c) column scaling vs row scaling ===
M * w  (a (3,) vector) scales each COLUMN:
    [10.0, 200.0, 3000.0]
    [40.0, 500.0, 6000.0]

M * b  (a (2,1) column) scales each ROW:
    [1.0, 2.0, 3.0]
    [8.0, 10.0, 12.0]

both results have shape (2, 3) and (2, 3) -- identical shapes, different numbers!
This is the bug that costs people an afternoon: multiplying a batch
of 3-vectors by [1,2,3] scales the VECTORS, not their components.

the mistake, concretely:
  points (shape (3,2)) = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
  scales (shape (2,)) = [10.0, 100.0]
  correct (want to scale each DIMENSION):
     [10.0, 200.0]
     [30.0, 400.0]
     [50.0, 600.0]
  wrong (scales broadcast over the 3 points instead):
     [10.0, 20.0] <- every row scaled by 10
     [30.0, 40.0] <- every row scaled by 10
     [50.0, 60.0] <- every row scaled by 10
```

Part (c) is the important one. Both results have shape `(2,3)` and both "look
reasonable", but `M * w` gives `[[10, 200, 3000], ...]` while `M * b` gives
`[[1, 2, 3], [8, 10, 12]]` — completely different numbers from the same matrix.
The shapes agreeing is exactly why the bug survives review: there is nothing to
catch, no exception, no shape assertion.

The concrete failure at the end is the same error in its most common form. You
have three 2D points and want to scale x by 10 and y by 100. Correctly, `[1,2]`
becomes `[10, 200]`. Written as `points * scales`, the `(2,)` vector aligns with
the *last* axis — which is length 2 — so each point is scaled correctly and you
get `[10, 200]`. But if the scales vector had length 3 instead of 2, the same
code would silently align it with the *points* axis and multiply whole points by
10, which is what the "wrong" panel shows. The rule that prevents it: **if a 1D
array's length matches a dimension other than the last one, reshape it
explicitly** — `scales.reshape(1, -1)` or `scales[:, None]`.

The `own_index` function is where the whole rule lives. For each output index it
projects onto one operand's axes, taking index 0 wherever that operand's axis
has length 1 and taking the output index otherwise. Axes are matched by counting
from the right, which is why `(2,3,4) + (3,1)` pairs the 3 with the *middle*
axis of the first shape.

</details>

**[ ] Exercise 2 —** Implement `einsum` from scratch and use it to verify five
operations against hand computations: matrix multiply `'ij,jk->ik'`, row sums
`'ij->i'`, the total sum `'ij->'`, the Frobenius inner product `'ij,ij->'`, and
the diagonal `'ii->i'`. Then use `'bij,bjk->bik'` on a stack of two matrices and
explain why `b` is not summed.

<details>
<summary>Solution</summary>

```python
from math import prod

def shape_of(t):
    if not isinstance(t, list):
        return ()
    return (len(t),) + shape_of(t[0])

def decode(flat, dims):
    out = [0] * len(dims)
    for i in range(len(dims) - 1, -1, -1):
        out[i] = flat % dims[i]
        flat //= dims[i]
    return out

def entry_at(t, idx):
    cur = t
    for i in idx:
        cur = cur[i]
    return cur

def einsum(equation, *operands):
    """A letter appearing in more than one operand AND absent from the output
    is summed over. A letter in the output is kept, even if it also appears
    twice -- 'bij,bjk->bik' keeps b and sums j."""
    if "->" in equation:
        left, out = equation.split("->")
    else:
        left, out = equation, None
    terms = [t.strip() for t in left.split(",")]
    shapes = [shape_of(o) for o in operands]
    for term, shape in zip(terms, shapes):
        if len(term) > len(shape):
            raise ValueError("too many subscripts for an operand")

    count = {}
    for term in terms:
        for letter in term:
            count[letter] = count.get(letter, 0) + 1
    free = sorted(c for c, k in count.items() if k == 1)
    if out is None:
        out = "".join(free)
    else:
        out = out.strip()
        for letter in out:
            if letter not in count:
                raise ValueError(f"output names unknown subscript {letter!r}")

    size = {}
    for term, shape in zip(terms, shapes):
        for pos, letter in enumerate(term):
            size.setdefault(letter, shape[pos])

    summed = sorted(c for c in count if c not in out)
    out_dims = [size[c] for c in out]
    sum_dims = [size[c] for c in summed]
    result = [0.0] * prod(out_dims)

    for oflat in range(prod(out_dims)):
        base = dict(zip(out, decode(oflat, out_dims)))
        acc = 0.0
        for sflat in range(prod(sum_dims)):
            cur = dict(base)
            cur.update(dict(zip(summed, decode(sflat, sum_dims))))
            tv = 1.0
            for oi, term in enumerate(terms):
                tv *= entry_at(operands[oi], tuple(cur[l] for l in term))
            acc += tv
        result[oflat] = acc
    if not out_dims:
        return result[0]
    if len(out_dims) == 1:
        return result

    def nest(flat, dims):
        if len(dims) == 1:
            return list(flat)
        step = prod(dims[1:])
        return [nest(flat[i * step:(i + 1) * step], dims[1:])
                for i in range(dims[0])]

    return nest(result, out_dims)

# A is (2,3) and Bv is (3,2), so 'ij,jk->ik' contracts over the shared axis j.
A = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
Bv = [[7.0, 8.0], [9.0, 10.0], [11.0, 12.0]]

print("A  =", A, "shape", shape_of(A))
print("Bv =", Bv, "shape", shape_of(Bv))

dotv = einsum("ij,jk->ik", A, Bv)
print("\n1) einsum('ij,jk->ik') =", dotv, " shape", shape_of(dotv))
manual = [[sum(A[i][t] * Bv[t][j] for t in range(3)) for j in range(2)]
          for i in range(2)]
print("   hand-written matmul =", manual)
print("   agree?", dotv == manual)
print("   by hand, entry (0,0) = 1*7 + 2*9 + 3*11 =", 1 * 7 + 2 * 9 + 3 * 11)

print("\n2) einsum('ij->i')  (row sums) =", einsum("ij->i", A))
print("   by hand:", [sum(A[i]) for i in range(2)])

print("\n3) einsum('ij->')   (sum of all) =", einsum("ij->", A))
print("   by hand:", sum(v for row in A for v in row))

print("\n4) einsum('ij,ij->', A, A) (Frobenius inner product) =",
      einsum("ij,ij->", A, A))
print("   by hand:", sum(v * v for row in A for v in row))

print("\n5) einsum('ii->i')  (diagonal) =", einsum("ii->i", A))
print("   by hand:", [A[0][0], A[1][1]])

print("\n6) einsum('bij,bjk->bik') on two stacked matrices:")
batchA = [[[1.0, 0.0], [0.0, 1.0]], [[2.0, 0.0], [0.0, 2.0]]]
batchB = [[[3.0, 0.0], [0.0, 3.0]], [[0.5, 0.0], [0.0, 0.5]]]
bb = einsum("bij,bjk->bik", batchA, batchB)
for m in bb:
    print("   ", m)
print("   shape", shape_of(bb))
print("   block 0 = 1*I times 3*I = 3I; block 1 = 2I times 0.5I = I")
print("   'b' appears in BOTH operands but is in the output, so it is KEPT")
print("   not summed. Only j is summed. Drop b from the output and you")
print("   would get a single (2,2) sum over both blocks instead.")

# Prove the difference explicitly.
summed_b = einsum("bij,bjk->ik", batchA, batchB)
print("\n   same operands, output 'ik' (b now summed):", summed_b)
print("   which is block0 + block1 =", [[3.0, 0.0], [0.0, 3.0]],
      "+", [[1.0, 0.0], [0.0, 1.0]], "=", summed_b)
```

Output:

```
A  = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]] shape (2, 3)
Bv = [[7.0, 8.0], [9.0, 10.0], [11.0, 12.0]] shape (3, 2)

1) einsum('ij,jk->ik') = [[58.0, 64.0], [139.0, 154.0]]  shape (2, 2)
   hand-written matmul = [[58.0, 64.0], [139.0, 154.0]]
   agree? True
   by hand, entry (0,0) = 1*7 + 2*9 + 3*11 = 58

2) einsum('ij->i')  (row sums) = [6.0, 15.0]
   by hand: [6.0, 15.0]

3) einsum('ij->')   (sum of all) = 21.0
   by hand: 21.0

4) einsum('ij,ij->', A, A) (Frobenius inner product) = 91.0
   by hand: 91.0

5) einsum('ii->i')  (diagonal) = [1.0, 5.0]
   by hand: [1.0, 5.0]

6) einsum('bij,bjk->bik') on two stacked matrices:
    [[3.0, 0.0], [0.0, 3.0]]
    [[1.0, 0.0], [0.0, 1.0]]
   shape (2, 2, 2)
   block 0 = 1*I times 3*I = 3I; block 1 = 2I times 0.5I = I
   'b' appears in BOTH operands but is in the output, so it is KEPT
   not summed. Only j is summed. Drop b from the output and you
   would get a single (2,2) sum over both blocks instead.

   same operands, output 'ik' (b now summed): [[4.0, 0.0], [0.0, 4.0]]
   which is block0 + block1 = [[3.0, 0.0], [0.0, 3.0]] + [[1.0, 0.0], [0.0, 1.0]] = [[4.0, 0.0], [0.0, 4.0]]
```

All five verifications match their hand computations, and entry (0,0) = 58 is
exactly the worked example, so the implementation is not merely self-consistent.

The last block is the payoff. The *same two operands* give two different answers
depending only on whether `b` appears in the output:

- `'bij,bjk->bik'` keeps `b`, so you get two separate 2×2 results, shape
  (2, 2, 2) — a batch of two matrix multiplications.
- `'bij,bjk->ik'` sums `b`, so you get one 2×2 result, shape (2, 2), equal to
  block 0 plus block 1: `3I + I = 4I`, exactly as printed.

That is the rule stated precisely. It is not "appears twice ⇒ summed", it is
**"appears in more than one operand and is absent from the output ⇒ summed"**,
and one letter in the output is the whole difference between a batched
operation and a collapsed one. This is why einsum is worth learning properly:
the same notation expresses operations that `@` cannot distinguish, because
`@` always sums over the second axis of its left operand and always treats a
3-D input as a batch.

</details>


**[ ] Exercise 3 —** Write a function `pairwise(left, right)` that returns
every product of one element of `left` with one element of `right`. Call it on a
3-element list and a 5-element list, then call it again with the arguments
swapped. Show that the two results contain the same numbers, that one is the
transpose of the other, and that their shapes differ. Finally, repeat the test
with two equal-length lists and show that the shapes now look identical, so a
test written that way cannot detect the swap.

<details>
<summary>Solution</summary>

```python
"""Exercise 3 solution: the non-square pairwise product.

`pairwise` returns the same 15 numbers no matter which order the arguments
arrive in, but the shape it hands back depends entirely on that order.  The
whole point is that nothing raises: you have to notice.
"""


def pairwise(left, right):
    """Every product of one element of `left` with one of `right`.

    Returned as nested lists, so len(left) rows of len(right) columns.
    """
    return [[l * r for r in right] for l in left]


def pairwise_by_broadcast(left, right):
    """The same thing, spelled as a broadcast of a column against a row."""
    return pairwise_by_broadcast_helper(left, right)


def pairwise_by_broadcast_helper(left, right):
    # As (n, 1) and (1, m): one column of `left`, one row of `right`.  Under
    # broadcasting the two size-1 axes stretch and the product is (n, m).
    column = [[l] for l in left]
    row = [list(right)]
    n, m = len(left), len(right)
    out = [[0.0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            out[i][j] = column[i][0] * row[0][j]
    return out


A = [1.0, 2.0, 3.0]                    # 3 items
B = [10.0, 20.0, 30.0, 40.0, 50.0]     # 5 items

as_rows = pairwise(A, B)
as_cols = pairwise(B, A)

print(f"pairwise(A, B): {len(as_rows)} rows of {len(as_rows[0])}")
for row in as_rows:
    print("   ", row)
print(f"pairwise(B, A): {len(as_cols)} rows of {len(as_cols[0])}")
for row in as_cols:
    print("   ", row)

transposed = [list(column) for column in zip(*as_cols)]
print(f"as_rows is the transpose of as_cols: {as_rows == transposed}")
print(f"the shapes agree: {len(as_rows) == len(as_cols)} "
      f"({len(as_rows)} vs {len(as_cols)} rows)")
print()

# The same computation through broadcasting gives the same answer.
print("through broadcasting, as (3, 1) times (1, 5):")
for row in pairwise_by_broadcast(A, B):
    print("   ", row)
print("   and as (5, 1) times (1, 3):")
for row in pairwise_by_broadcast(B, A):
    print("   ", row)
print("   identical to the list version:",
      pairwise_by_broadcast(A, B) == as_rows)
print()

# Why a square test cannot catch this.
S = [1.0, 2.0, 3.0]
sq_rows = pairwise(S, S)
sq_cols = pairwise(S, S)[::-1]
print("now with a SQUARE input, S = [1.0, 2.0, 3.0]:")
print(f"   pairwise(S, S) is {len(sq_rows)} x {len(sq_rows[0])}, "
      f"and swapping the arguments gives {len(sq_cols)} x {len(sq_cols[0])}")
print(f"   the shapes are indistinguishable: "
      f"{len(sq_rows) == len(sq_cols)}")
print(f"   but the numbers differ: {sq_rows == sq_cols}")
print("   pairwise(S, S)     ", sq_rows)
print("   pairwise(S, S)[::-1]", sq_cols)
print()
print("So a test written with equal-length inputs passes, whatever the code")
print("does.  The bug only appears the day the two lengths differ, and then it")
print("appears as a matrix with the wrong shape rather than an exception.")
print()
print("The defence is not 'be careful'.  It is to state the orientation in the")
print("name and the type: name the function for the order it produces --")
print("pairwise_rows_of(left, right) -- and check `.shape` at the boundary")
print("where the two lengths come from different places.")
```

**The numbers never disagreed, only the shape.** Both results hold the same 15
products; `as_rows == transpose(as_cols)` is `True`. What differs is whether
you get 3 rows of 5 or 5 rows of 3, and the rule that decides it is simply
which argument came first.

**The square case is why the bug survives.** With `S = [1.0, 2.0, 3.0]` both
calls return a 3x3 array, so `len(...)` checks pass and a shape assertion
written as `(3, 3)` passes. Yet the arrays are different: one is
`[[1, 2, 3], [2, 4, 6], [3, 6, 9]]` and the other is
`[[3, 6, 9], [2, 4, 6], [1, 2, 3]]`. The orientation bug is present in both,
invisible in both, and only becomes a shape error when the two inputs happen to
have different lengths.

**What actually fixes it** is not vigilance. It is making the orientation part
of the interface: name the function for the order it returns, and assert the
shape where the two lengths come from different sources -- at a function
boundary, not in the middle of an algorithm where the lengths are already
assumed.

</details>

**[ ] Exercise 4 —** Compute a batched matrix product twice: once by
broadcasting the operands up to rank 4 and summing along the contracted axis,
and once by contracting directly in the innermost loop. Use a batch of 2
matrices of size 3x4 against a batch of 2 matrices of size 4x5. Count how many
numbers each version writes, confirm both give the same 2x3x5 result, and state
the rule that decides when broadcasting a product is acceptable.

<details>
<summary>Solution</summary>

```python
"""Exercise 4 solution: what broadcasting a product actually costs.

A broadcast that REPEATS an axis (a bias add) writes only the output.  A
broadcast that builds an OUTER PRODUCT writes the product of every pair before
any of it is summed away.  This counts the difference exactly, with real
arithmetic, rather than asserting it.
"""

from itertools import product


def shape_of(x):
    if not isinstance(x, list):
        return ()
    if len(x) == 0:
        return (0,)
    return (len(x),) + shape_of(x[0])


def zeros(shape):
    if not shape:
        return 0
    return [zeros(shape[1:]) for _ in range(shape[0])]


def put(arr, idx, value):
    node = arr
    for i in idx[:-1]:
        node = node[i]
    node[idx[-1]] = value


# A batch of 2 matrices 3x4, and a batch of 2 matrices 4x5.  Result: 2 of 3x5.
Bt, N, M, K = 2, 3, 4, 5
A = [[[10 * b + 10 * i + j for j in range(M)] for i in range(N)]
     for b in range(Bt)]
Bm = [[[100 * b + 10 * j + k for k in range(K)] for j in range(M)]
      for b in range(Bt)]

print(f"A shape {shape_of(A)}, B shape {shape_of(Bm)}, "
      f"expected result {(Bt, N, K)}")

# --- the broadcast route ------------------------------------------------------

intermediate = zeros((Bt, N, M, K))
for b, i, j, k in product(range(Bt), range(N), range(M), range(K)):
    put(intermediate, (b, i, j, k), A[b][i][j] * Bm[b][j][k])
print(f"route 1 builds an intermediate of shape {shape_of(intermediate)}: "
      f"{Bt * N * M * K} numbers")
out1 = zeros((Bt, N, K))
for b, i, k in product(range(Bt), range(N), range(K)):
    out1[b][i][k] = sum(intermediate[b][i][j][k] for j in range(M))
print(f"        then reduces to {shape_of(out1)}: {Bt * N * K} numbers")

# --- the contracting route ---------------------------------------------------

out2 = zeros((Bt, N, K))
for b, i, k in product(range(Bt), range(N), range(K)):
    total = 0
    for j in range(M):
        total += A[b][i][j] * Bm[b][j][k]
    out2[b][i][k] = total
print(f"route 2 writes only {shape_of(out2)}: {Bt * N * K} numbers")
print(f"the two agree: {out1 == out2}")
print(f"batch 0 of route 1: {out1[0]}")
print(f"batch 0 of route 2: {out2[0]}")
print()

writes1 = Bt * N * M * K + Bt * N * K
writes2 = Bt * N * K
print(f"numbers written: route 1 = {writes1}, route 2 = {writes2}, "
      f"ratio {writes1 / writes2:.0f}x")
print(f"the intermediate alone is M = {M} times the output, so the ratio is "
      f"M + 1 = {M + 1}")
print()

# The rule, as a function of the summed-over dimension.
print("so broadcast the product only when the summed dimension is tiny:")
for m in (1, 2, 4, 16, 64):
    out_size = Bt * N * K
    print(f"   M = {m:>3}: intermediate {out_size * m:>6} numbers, "
          f"total writes {out_size * (m + 1):>6}")
print("   M = 1 is just a scaling, and M = 2 doubles it.  Everything past")
print("   that is a different asymptotic cost, not a constant factor.")
print()

# A bias add, for contrast: repeating an axis costs the output and nothing more.
BIAS = [[[100 + 10 * i + k for k in range(K)] for i in range(N)]]   # (1, N, K)
added = [[[x + BIAS[0][i][k] for k, x in enumerate(row)]
          for i, row in enumerate(item)] for item in out2]
print(f"a bias add with bias shape {shape_of(BIAS)} writes {Bt * N * K} "
      f"numbers, exactly the output")
print(f"batch 0 with bias: {added[0]}")
print()
print("The distinction is whether the stretched axis has to be SUMMED.")
print("Repeating it: cost is the output.  Summing over it: broadcasting has to")
print("build the full outer product first, and the cost is the output TIMES")
print("that axis.  Matrix products and attention sum.  Biases, normalisation")
print("and residual connections repeat.  That one sentence decides 90% of the")
print("shape work in a deep-learning layer.")
```

**The rule is about whether the stretched axis is summed.** A bias add
*repeats* its axis, so it writes exactly the output and costs nothing extra --
30 numbers here for a 30-number answer. A matrix product must *sum* over the
shared axis, and broadcasting can only do that by first building every pairwise
product. That intermediate is `M` times the output: 120 numbers for a 30-number
result, so 150 written against 30, a factor of `M + 1 = 5`.

**Why the factor is `M + 1` and not `M`.** The intermediate is `M` times the
output, and the reduction pass then writes the output again. One pass to build,
one to reduce. This is why the ratio grows without bound as `M` grows, and why
"it is only a factor of 5" stops being a defence at `M = 512`: at
`(32, 512, 512)` against itself the intermediate is 32768 MiB against an input
of 64 MiB, and numpy refuses to allocate it.

**The practical form of the rule.** Broadcasting a product is fine when the
summed dimension is tiny and constant -- an outer product of two short vectors
is exactly what you wanted. It is wrong the moment the summed dimension is
another layer's width, because then you have chosen a different asymptotic cost
without being told. Writing it as `'bij,bjk->bik'` states the contraction in
the notation, so the cost is visible in the source instead of discovered in a
profile.

</details>

**[ ] Exercise 5 —** Show that floating-point addition is not associative in
a way that changes the answer. Write a left-to-right `fold` and a `pairwise`
sum (split in half, recurse, add the halves), and an exact comparison using
`math.fsum`. Try them on `[1e16, 1.0, -1e16, 1.0]`, on `[big] + [1.0]*4` for
`big` in `1e8, 1e12, 1e16, 1e20`, and on 1000 copies of `0.1`. Then take the
2x3 array `[[1e16, 1.0, -1e16], [1.0, 1.0, 1.0]]` and sum it by reducing along
axis -1 and along axis 0. Explain each result.

<details>
<summary>Solution</summary>

```python
"""Exercise 5 solution: summation order changes the answer.

Floating-point addition is not associative, so "sum these numbers" is not a
complete instruction -- the ORDER is part of the answer.  Worse, neither of the
two obvious orders has to be right.  `math.fsum` is, because it tracks the
partial sums exactly and rounds once at the end.
"""

import math


def fold(values):
    """Left to right, the way a naive Python loop does it."""
    total = 0.0
    for v in values:
        total += v
    return total


def pairwise(values):
    """Split in half and recurse, which is what numpy and BLAS do.

    Each half is summed first, then the two halves are added.  That keeps the
    magnitudes that meet each other similar, so small terms are less likely to
    be swallowed -- but 'less likely' is not 'never', as the first example
    shows.
    """
    if len(values) <= 1:
        return values[0] if values else 0.0
    mid = len(values) // 2
    return pairwise(values[:mid]) + pairwise(values[mid:])


# --- 1. the textbook disaster, and the surprise that pairwise does not save ---

xs = [1e16, 1.0, -1e16, 1.0]
print("the list", xs)
print(f"   the answer you want       2.0   (1e16 - 1e16 cancels, both 1's survive)")
print(f"   fold, strictly left to right  {fold(xs)}")
print(f"   pairwise, halves first         {pairwise(xs)}")
print(f"   math.fsum, exactly then round  {math.fsum(xs)}")
print()
print("Left to right, 1e16 + 1.0 rounds back to 1e16: at that magnitude the")
print("gap between representable numbers is 2.0, so the 1.0 is no longer there.")
print("The -1e16 then cancels to exactly 0.0 and takes the last 1.0 with it.")
print("Every individual step obeys the rounding rule and the total is wrong.")
print()
print("The surprise is the pairwise column.  It is also wrong, for a subtler")
print("reason: it computes (1e16 + 1.0) + (-1e16 + 1.0), and BOTH halves")
print("internally round their 1.0 away before the halves ever meet.  Pairwise")
print("summation reduces how often a small term gets eaten; it does not stop it.")
print("Only fsum, which never rounds until the very end, gets 2.0.")
print()

# --- 2. when the small terms DO survive, and what that depends on ------------

print("now with a single large term and a tail of ones:")
for big in (1e8, 1e12, 1e16, 1e20):
    xs = [big, 1.0, 1.0, 1.0, 1.0]
    print(f"   big = {big:.0e}: fold {fold(xs):>22.1f}, "
          f"pairwise {pairwise(xs):>22.1f}, fsum {math.fsum(xs):>22.1f}")
print()
print("At 1e8 and 1e12, big + 1.0 is still exactly representable, so every")
print("order keeps the tail and all three agree on the right answer.")
print()
print("At 1e16, fold returns 1e16 and is simply wrong: it dropped the whole")
print("tail of ones.  Pairwise and fsum both get 1e16 + 4, the correct value,")
print("because pairwise happens to add the four small numbers together before")
print("they meet the big one.  So pairwise is not a guarantee, it is a bet that")
print("usually pays.")
print()
print("At 1e20 every method returns 1e20, and here that is CORRECT: the exact")
print("total is 1e20 + 4, but the gap between representable numbers near 1e20 is")
print("about 16384, so 1e20 + 4 rounds to 1e20 no matter how you sum it.  The")
print("information was never there to keep.  A method cannot be blamed for a")
print("loss the format already committed.")
print()
print("The threshold is therefore not a property of the algorithm at all.  It")
print("is the size of the gap between representable numbers near the leading")
print("magnitude, compared with the size of the terms you are trying to keep.")
print("When the terms are smaller than the gap, they are gone before any")
print("algorithm sees them.  That is catastrophic cancellation, and Lesson 121")
print("is entirely about it.")
print()

# --- 3. many comparable terms: the case pairwise was invented for ------------

xs = [0.1] * 1000
print(f"summing 1000 copies of 0.1, true sum {0.1 * 1000}:")
print(f"   fold     {fold(xs)}")
print(f"   pairwise {pairwise(xs)}")
print(f"   fsum     {math.fsum(xs)}")
print()
print("Here the terms are all the same size, so there is no magnitude for a")
print("small term to hide behind.  Pairwise keeps the running total close to")
print("the final answer and lands on it exactly; a running fold accumulates one")
print("rounding per step and drifts.  This is the case the pairwise trick is")
print("genuinely good at, and it is the common case: summing many similar")
print("numbers.")
print()

# --- 4. the layout point: the SAME numbers, reduced in two orders ------------

GRID = [[1e16, 1.0, -1e16], [1.0, 1.0, 1.0]]

row_major = [v for row in GRID for v in row]
column_major = [GRID[i][j] for j in range(len(GRID[0])) for i in range(len(GRID))]

print(f"the same 6 numbers, reduced two ways")
print(f"   row-major order    {row_major}")
print(f"     fold gives {fold(row_major)}")
print(f"   column-major order {column_major}")
print(f"     fold gives {fold(column_major)}")
print(f"   fsum on either gives {math.fsum(row_major)}")
print()
print("Reducing along axis -1 sums each row, then adds the row sums.")
print("Reducing along axis 0 sums each column, then adds those.  Both are legal")
print("and both are 'the sum', and they disagree: 3.0 against 1.0, for a true")
print("answer of 4.0.  Whichever axis you reduce along, the ORDER is part of the")
print("problem, and no shape check will warn you.")
print()

# --- 5. what to actually do ---------------------------------------------------

print("the practical rules this yields:")
print("   1. If you need the answer to be right, use math.fsum (or an equivalent")
print("      exact accumulator).  It is a few times slower and exactly right.")
print("   2. If you need it fast, reduce along the axis that groups similar")
print("      magnitudes together, and use a library, because they already do.")
print("   3. If a sum is supposed to be near zero and the terms are large, you")
print("      have a cancellation problem no summation order will save.  Restructure")
print("      the algebra instead -- that is the subject of Lesson 121.")
print()
print(f"the three methods give {fold(row_major)}, {math.fsum(row_major)} and")
print("the true value 4.0, so on six numbers the spread between a naive loop")
print("and an exact accumulator is the entire answer.")
```

**The three methods are not a ranking, they are different guarantees.** On
`[1e16, 1.0, -1e16, 1.0]` the true answer is 2.0. `fold` gives 1.0 and
`pairwise` gives 0.0 -- both wrong, for different reasons -- and only `fsum`
gives 2.0. The instructive part is that pairwise fails too: it computes
`(1e16 + 1.0) + (-1e16 + 1.0)`, and each half has already rounded its `1.0`
away before the halves meet. Pairwise reduces how *often* a small term gets
swallowed; it does not make it impossible. `fsum` keeps every partial sum as an
exact rational and rounds once, which is why it cannot lose anything.

**The `big` sweep shows where the threshold is, and it is not in the
algorithm.** At `1e8` and `1e12` all three methods agree, because `big + 1.0` is
still exactly representable. At `1e16` only `fold` is wrong: `pairwise` happens
to add the four ones together before they meet the big term, and gets
`1e16 + 4`. At `1e20` all three return `1e20` and all three are *correct*, since
the exact total `1e20 + 4` rounds to `1e20` at that magnitude no matter how you
add it. The gap between representable numbers near `1e20` is about 16384, so
the information was destroyed before any algorithm saw it.

**The axis sweep is the one that matters for this lesson.** The same six
numbers reduce to 3.0 along axis -1 and 1.0 along axis 0, against a true value
of 4.0. Neither is a shape error, neither raises, and both are `arr.sum()` in
some library. The order of summation is part of the problem statement, and
choosing an axis is choosing an order.

**Where that leaves you.** Use `math.fsum` when correctness matters more than
speed and the list is short. Use a library reduction when speed matters, because
pairwise blocking is already the default there. And when a sum is supposed to be
near zero while the terms are large, no summation order will save you -- the
algebra has to be restructured so the large terms cancel symbolically instead of
numerically. That is the subject of
[Lesson 121](121_numerical_methods_and_floating_point.md).

</details>

**[ ] Exercise 6 —** You are given a 3x5 array, a bias of 3 values, and a
scale of 5 values. Write your own `broadcast_shape` from the rule, then show
that adding the 3-value bias directly to the 3x5 array is rejected, that adding
it to a 3x3 array is accepted, and that on the 3x3 array the "per row" and "per
column" readings give different answers with the same shape. Finally, show that
the mistake is silent on square data and loud on rectangular data.

<details>
<summary>Solution</summary>

```python
"""Exercise 6 solution: implement broadcasting, then catch a real bug with it.

You are given three functions that are individually fine and jointly wrong.  The
only way to find the bug is to build the operation the way a library does and
compare, which is the point of writing the rule out by hand.
"""


def broadcast_shape(*shapes):
    """The one rule: right-align, then each pair must match or contain a 1."""
    rank = max(len(s) for s in shapes)
    out = []
    for offset in range(1, rank + 1):
        dim = 1
        for shape in shapes:
            if offset > len(shape):
                continue
            d = shape[-offset]
            if d == 1:
                continue
            if dim == 1:
                dim = d
            elif d != dim:
                raise ValueError(
                    f"axis -{offset}: {dim} against {d}, neither is 1")
        out.append(dim)
    return tuple(reversed(out))


# The three functions, each individually reasonable.

def add_bias_rows(data, bias):
    """Add one bias per ROW.  bias has one entry per row."""
    return [[v + bias[i] for v in row] for i, row in enumerate(data)]


def add_bias_columns(data, bias):
    """Add one bias per COLUMN.  bias has one entry per column."""
    return [[v + bias[j] for j, v in enumerate(row)] for row in data]


def scale_columns(data, scale):
    """Multiply each COLUMN by one scale factor."""
    return [[v * scale[j] for j, v in enumerate(row)] for row in data]


# A deliberately asymmetric data set: 3 rows, 5 columns.
DATA = [
    [1.0, 2.0, 3.0, 4.0, 5.0],
    [10.0, 20.0, 30.0, 40.0, 50.0],
    [100.0, 200.0, 300.0, 400.0, 500.0],
]
ROWS, COLS = 3, 5
BIAS = [1.0, 2.0, 3.0]          # one per row: 3 values
SCALE = [1.0, 2.0, 3.0, 4.0, 5.0]   # one per column: 5 values

print(f"DATA is {ROWS} rows by {COLS} columns")
print(f"BIAS  is {len(BIAS)} values -- clearly per row")
print(f"SCALE is {len(SCALE)} values -- clearly per column")
print()

# Now do the same things with broadcasting, and look at the shapes.

# A bias per row, done naively as an ordinary 1D add, lands on the LAST axis.
# So `DATA + BIAS` is only legal when COLS == len(BIAS).  Here 5 != 3, so
# broadcasting refuses -- which is the good case.
try:
    broadcast_shape((ROWS, COLS), (len(BIAS),))
    print("DATA + BIAS was accepted, which should not happen")
except ValueError as exc:
    print(f"DATA + BIAS raises: {exc}")
print("   caught, because the row count and the bias length disagree with")
print("   the column count.  Broadcasting earned its keep.")
print()

# But a per-COLUMN bias is legal, and if the data is SQUARE the two cases are
# indistinguishable.  Show that on a square array.
SQUARE = [[1.0, 2.0, 3.0], [10.0, 20.0, 30.0], [100.0, 200.0, 300.0]]
VEC = [1.0, 2.0, 3.0]

broadcast = broadcast_shape((3, 3), (3,))
print(f"on a 3x3 array, a length-3 vector broadcasts: {broadcast}")
print("   added as a column (per row) :",
      add_bias_rows(SQUARE, VEC))
print("   added as a row (per column) :",
      add_bias_columns(SQUARE, VEC))
print(f"   the two are different: "
      f"{add_bias_rows(SQUARE, VEC) != add_bias_columns(SQUARE, VEC)}")
print("   the two have the same shape, so nothing catches it.")
print()

# The fix: state the axis.  Both forms are correct, but only one of them is
# correct for the thing you meant.
per_row = [[v + VEC[i] for v in row] for i, row in enumerate(SQUARE)]
per_column = [[v + VEC[j] for j, v in enumerate(row)] for row in SQUARE]
print("state the axis instead of relying on it:")
print(f"   rows broadcast a (3,1) column -> {broadcast_shape((3, 3), (3, 1))}")
print(f"   columns broadcast a (1,3) row    -> {broadcast_shape((3, 3), (1, 3))}")
print(f"   per-row    result: {per_row}")
print(f"   per-column result: {per_column}")
print("   neither is 'the' answer; you have to say which one you meant.")
print()

# Finally: scale_columns against the same data, which is where the original
# bug actually bites.  Scaling columns needs a length-COLS vector.
print(f"scale_columns with a length-{len(SCALE)} vector on {ROWS}x{COLS}:")
for row in scale_columns(DATA, SCALE):
    print("   ", row)
print(f"that is legal because {len(SCALE)} == COLS == {COLS}.")
print(f"Passing the per-ROW bias instead ({len(BIAS)} values) is not legal here:")
try:
    broadcast_shape((ROWS, COLS), (len(BIAS),))
except ValueError as exc:
    print(f"   ValueError: {exc}")
print()
print("So the same mistake that is silent on square data becomes a loud error")
print("the moment the data stops being square.  That is the whole lesson: shape")
print("bugs do not announce themselves, they wait for your dimensions to become")
print("equal, and then they hide again.")
```

**Why the rectangular case raises and the square case does not.** A bare 1D
vector aligns with axis $-1$. On the 3x5 array axis $-1$ has length 5 while the
bias has length 3, and neither is 1, so the rule rejects it: `axis -1: 5
against 3, neither is 1`. On the 3x3 array axis $-1$ has length 3 and the bias
has length 3, so it is accepted — and the alignment it chose was the one you
did not want, because it applied the bias down the columns.

**The two square results are genuinely different, not a formatting
difference.** Per row gives `[[2, 3, 4], [12, 22, 32], [103, 203, 303]]`; per
column gives `[[2, 4, 6], [11, 22, 33], [101, 202, 303]]`. Both are 3x3, so
`assert result.shape == (3, 3)` passes for either. This is the trap the lesson
keeps returning to: the shape is not the answer.

**What actually prevents it** is naming the axis rather than letting it be
inferred. Reshaping the bias to `(3, 1)` broadcasts down the rows and `(1, 3)`
across the columns, and both are legal and both are correct — for different
questions. Once you write `bias[:, None]` or `bias[None, :]`, a reader can see
which one you meant, and a wrong answer is a visible mistake rather than a
plausible one.

**The last observation is the one to carry.** The identical mistake is a loud
`ValueError` on 3x5 data and completely silent on 3x3 data. So a test suite
built on square fixtures proves nothing about the axis, and a shape bug waits
for your dimensions to become equal in order to hide. Test with a deliberately
non-square case, every time.

</details>

**Challenge —** Build a strided array view class like the one in the lesson,
then show that: (a) transposing a `(2,3)` array is free and equals the nested
transpose; (b) reshaping the same buffer to `(3,2)` does **not** equal the
transpose; (c) a slice with step 2 is non-contiguous; and (d) a `(2,2,2,3)`
tensor's stride for axis 0 is 12. Verify each claim numerically.

<details>
<summary>Solution</summary>

```python
class View:
    """A view onto a flat buffer with a shape and per-axis strides.

    Note that `data` is stored, not copied: a view shares the buffer with
    whatever it was made from, which is the entire reason transposing and
    reshaping can be free. Only `copy()` should ever duplicate the numbers.
    """

    def __init__(self, data, shape, stride=None):
        self.data = data          # shared on purpose -- this is a VIEW
        self.shape = tuple(shape)
        if stride is None:
            stride, acc = [], 1
            for d in reversed(self.shape):
                stride.append(acc)
                acc *= d
            stride.reverse()
        self.stride = tuple(stride)

    def __getitem__(self, idx):
        return self.data[sum(i * s for i, s in zip(idx, self.stride))]

    def is_contiguous(self):
        exp, acc = [], 1
        for d in reversed(self.shape):
            exp.append(acc)
            acc *= d
        exp.reverse()
        return list(self.stride) == exp

    def transpose(self):
        """Reverse the axes. No data moves: only the metadata changes."""
        return View(self.data, self.shape[::-1], self.stride[::-1])

    def reshape(self, new_shape):
        """A row-major view. Only valid if the new shape's axes come from
        splitting or merging consecutive old axes."""
        if prod(self.shape) != prod(new_shape):
            raise ValueError("cannot reshape: different number of elements")
        return View(self.data, new_shape)

    def step_slice_axis1(self, step):
        """Take every `step`-th element along axis 1 (rows stay whole)."""
        new_cols = (self.shape[1] + step - 1) // step
        return View(self.data, (self.shape[0], new_cols),
                    (self.stride[0], self.stride[1] * step))

    def to_list(self):
        def build(prefix):
            if len(prefix) == len(self.shape):
                return self[tuple(prefix)]
            return [build(prefix + [i]) for i in range(self.shape[len(prefix)])]
        return build([])

def prod(dims):
    n = 1
    for d in dims:
        n *= d
    return n

A = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
flat = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
v = View(flat, (2, 3))

print("=== (a) transpose is free and correct ===")
print("shape", v.shape, "stride", v.stride, "contiguous", v.is_contiguous())
t = v.transpose()
print("transposed shape", t.shape, "stride", t.stride,
      "contiguous", t.is_contiguous())
print("  view:", t.to_list())
nested_T = [[A[i][j] for i in range(2)] for j in range(3)]
print("  nested transpose:", nested_T)
print("  equal?", t.to_list() == nested_T)
print("  same buffer object?", t.data is v.data)
print("  stride is just the old one reversed:", v.stride, "->", t.stride)

print("\n=== (b) reshape is NOT the transpose ===")
r = v.reshape((3, 2))
print("reshaped shape", r.shape, "stride", r.stride,
      "contiguous", r.is_contiguous())
print("  view:", r.to_list())
print("  transpose was:", t.to_list())
print("  equal to the transpose?", r.to_list() == t.to_list())
print("  same buffer?", r.data is v.data)
print("  Same buffer, same shape, DIFFERENT numbers: reshape re-reads the")
print("  buffer row-major; transpose reverses the strides.")

print("\n=== (c) a step-2 slice is not contiguous ===")
s = v.step_slice_axis1(2)
print("sliced shape", s.shape, "stride", s.stride,
      "contiguous", s.is_contiguous())
print("  view:", s.to_list())
print("  stride for axis 1 is doubled:", v.stride[1], "->", s.stride[1])
print("  contiguous?", s.is_contiguous(), "(elements are 2 apart, so any")
print("  operation reading them sequentially touches twice the memory.)")
print("  a .copy() of the slice is contiguous:",
      View([x for row in s.to_list() for x in row],
           (s.shape[0], s.shape[1])).is_contiguous())

print("\n=== (d) the (2,2,2,3) stride for axis 0 is 12 ===")
data4 = [float(v) for v in range(1, 25)]
v4 = View(data4, (2, 2, 2, 3))
print("shape", v4.shape)
print("stride", v4.stride)
print("  axis 0 stride =", v4.stride[0],
      "= 2*2*3 =", 2 * 2 * 3, " (everything to its right)")
print("  matches?", v4.stride[0] == 2 * 2 * 3)

nested4 = [[[[1.0 + 12.0 * a + 6.0 * b + 3.0 * c + d for d in range(3)]
             for c in range(2)] for b in range(2)] for a in range(2)]
print("\nchecking every entry of the 4D view against the nested form:")
bad = 0
for a in range(2):
    for b in range(2):
        for c in range(2):
            for d in range(3):
                if v4[a, b, c, d] != nested4[a][b][c][d]:
                    bad += 1
print("  mismatches:", bad)
print("  e.g. v4[1,0,1,2] =", v4[1, 0, 1, 2],
      " nested:", nested4[1][0][1][2])

print("\n=== column-major view of the same buffer ===")
colmajor = View(flat, (2, 3), stride=(1, 2))
print("shape", colmajor.shape, "stride", colmajor.stride,
      "contiguous", colmajor.is_contiguous())
print("  view:", colmajor.to_list())
print("  same numbers as the row-major view, different order:")
print("  row-major:", v.to_list())
print("  equal?", colmajor.to_list() == v.to_list())

print("\n=== reshape vs transpose: which one needs a copy? ===")
print("v has strides", v.stride, "and shape", v.shape)
print("To read it as (3,2) row-major you need stride (2,1), which is exactly")
print("the buffer's natural layout -- so reshape is a view, no copy.")
print("To read it as the transpose you need stride (1,3), which reverses")
print("the axis order -- and that is also a view, no copy.")
print("  reshape((3,2)) strides", v.reshape((3, 2)).stride)
print("  transpose()   strides", v.transpose().stride)
print("A copy would only be forced if the new axes could not be built")
print("from consecutive old ones, e.g. (2,3,4) -> (4,6).")
```

Output:

```
=== (a) transpose is free and correct ===
shape (2, 3) stride (3, 1) contiguous True
transposed shape (3, 2) stride (1, 3) contiguous False
  view: [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]
  nested transpose: [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]
  equal? True
  same buffer object? True
  stride is just the old one reversed: (3, 1) -> (1, 3)

=== (b) reshape is NOT the transpose ===
reshaped shape (3, 2) stride (2, 1) contiguous True
  view: [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
  transpose was: [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]
  equal to the transpose? False
  same buffer? True
  Same buffer, same shape, DIFFERENT numbers: reshape re-reads the
  buffer row-major; transpose reverses the strides.

=== (c) a step-2 slice is not contiguous ===
sliced shape (2, 2) stride (3, 2) contiguous False
  view: [[1.0, 3.0], [4.0, 6.0]]
  stride for axis 1 is doubled: 1 -> 2
  contiguous? False (elements are 2 apart, so any
  operation reading them sequentially touches twice the memory.)
  a .copy() of the slice is contiguous: True

=== (d) the (2,2,2,3) stride for axis 0 is 12 ===
shape (2, 2, 2, 3)
stride (12, 6, 3, 1)
  axis 0 stride = 12 = 2*2*3 = 12  (everything to its right)
  matches? True

checking every entry of the 4D view against the nested form:
  mismatches: 0
  e.g. v4[1,0,1,2] = 18.0  nested: 18.0

=== column-major view of the same buffer ===
shape (2, 3) stride (1, 2) contiguous False
  view: [[1.0, 3.0, 5.0], [2.0, 4.0, 6.0]]
  same numbers as the row-major view, different order:
  row-major: [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
  equal? False

=== reshape vs transpose: which one needs a copy? ===
v has strides (3, 1) and shape (2, 3)
To read it as (3,2) row-major you need stride (2,1), which is exactly
the buffer's natural layout -- so reshape is a view, no copy.
To read it as the transpose you need stride (1,3), which reverses
the axis order -- and that is also a view, no copy.
  reshape((3,2)) strides (2, 1)
  transpose()   strides (1, 3)
A copy would only be forced if the new axes could not be built
from consecutive old ones, e.g. (2,3,4) -> (4,6).
```

Every claim is verified numerically, and two of them are the ones people get
wrong.

**Part (b) is the headline.** Both operations return the same shape `(3,2)` from
the same buffer with `same buffer object? True` confirming nothing was copied —
and `equal to the transpose? False` says the numbers differ. Reshape gives
`[[1,2],[3,4],[5,6]]`, the transpose gives `[[1,4],[2,5],[3,6]]`. The last block
prints both stride tuples: reshape gets `(2,1)` and transpose gets `(1,3)`, the
reverse.

**Part (c) shows why non-contiguity costs money.** The slice has stride 2 along
its last axis because every retained element is two positions from the next. The
array is not contiguous, so any operation that streams through memory touches
twice as many cache lines for the same number of useful values — and
`is_contiguous` reports `False`. Copying restores contiguity, which is the whole
trade: memory now versus memory bandwidth later.

**Part (d) confirms the stride rule.** Axis 0 of a `(2,2,2,3)` tensor has stride
12 = 2·2·3, the product of every dimension to its right. The check over all 24
entries finds `mismatches: 0`, so the stride arithmetic is right and not just
right for the one example printed.

The last block is the easy case people get wrong in their heads: reading a `(2,3)`
buffer as `(3,2)` needs **no** copy either way. Row-major reading wants stride
`(2,1)`, which is the buffer's natural layout, so `reshape` is free. The transpose
wants `(1,3)`, which reorders the axes but is still just metadata. A copy is
forced only when the new axes cannot be built from consecutive old ones — swapping
factors, as in `(2,3,4)` to `(4,6)`, is the case that actually moves memory.

</details>

## Summary

- An n-dimensional array is a function from a product of index sets to a set of
  numbers; its shape is the tuple of axis lengths and its size is their product.
- Broadcasting aligns shapes from the right; each pair of axes must match or one
  must be 1, and a 1 stretches. Incompatible axes raise rather than guess. A 1D
  array therefore broadcasts over the **last** axis, which is why `x * w` on a
  `(batch, features)` array scales feature columns and not rows.
- einsum sums a letter when it appears in more than one operand **and is absent
  from the output**. Keeping it in the output turns a batched contraction into a
  collapsed one, from identical operands. `'ij,jk->ik'` is matrix multiply,
  `'bij,bjk->bik'` a batch of them, `'ii->i'` a diagonal, `'ij,ij->'` the
  Frobenius inner product.
- A tensor is a flat buffer plus a shape plus strides, where a stride is how
  many elements to jump to increment that axis. Row-major means the last stride
  is 1, so transposing is just reversing two tuples and copies nothing.
- A reshape is a view exactly when the addresses, read in the new order, are
  evenly spaced; otherwise numpy must copy. Reshaping re-reads row-major, so
  `reshape(3,2)` is **not** `transpose` even though both are free.
- Broadcasting an axis that gets *summed* builds the whole outer product first,
  at `M` times the output size; broadcasting one that gets *repeated* costs only
  the output. Matrix products sum, biases repeat, and that decides the memory
  bill for a layer.
- A strided slice is non-contiguous, which costs memory bandwidth downstream
  until you call `.copy()`.
- Float addition is not associative, so summation order -- which layout controls
  -- can change the last digits, as `[1e16, 1, -1e16, 1]` shows.

## Next

[121 — Numerical Methods and Floating Point](121_numerical_methods_and_floating_point.md)
moves from how to *hold* numbers to how *accurate* they are. The
`[1e16, 1.0, -1e16, 1.0]` sum that folds to `1.0` when the true answer is `2.0`
is the preview: IEEE 754, machine epsilon, catastrophic cancellation,
conditioning and root-finding all follow from that one fact.
