# 120 — Tensors and Broadcasting

**Part**: part10_tensors_numerical · **Prerequisites**: 31, 41 · **Time**: 35 min

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

Notation follows [SYMBOLS.md](../../SYMBOLS.md).

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

## Exercises and Solutions

**[ ] Exercise 1 — ** Implement the broadcasting rules for two operands, then use
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

**[ ] Exercise 2 — ** Implement `einsum` from scratch and use it to verify five
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

**Challenge — ** Build a strided array view class like the one in the lesson,
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
  must be 1, and a 1 stretches. Incompatible axes raise rather than guess.
- A 1D array broadcasts over the **last** axis, which is why `x * w` on a
  `(batch, features)` array scales feature columns, not rows.
- einsum sums a letter when it appears in more than one operand **and is absent
  from the output**. Keeping it in the output turns a batched contraction into a
  collapsed one, with identical operands.
- `'ij,jk->ik'` is matrix multiply; `'bij,bjk->bik'` is a batch of matrix
  multiplies; `'ii->i'` is a diagonal; `'ij,ij->'` is the Frobenius inner
  product.
- A tensor is a flat buffer plus a shape plus strides. Stride = elements to
  jump to increment that axis; row-major means the last stride is 1.
- Transposing reverses the stride tuple and copies nothing. Reshaping re-reads
  row-major, so `reshape(3,2)` is **not** `transpose`.
- A reshape is a view only when the new axes come from splitting or merging
  consecutive old ones; otherwise numpy must copy.
- A strided slice is non-contiguous, which costs memory bandwidth downstream
  until you call `.copy()`.
- Float addition is not associative, so summation order — which layout controls
  — can change the last digits, as `[1e16, 1, -1e16, 1]` shows.

## Next

[121 — Numerical Methods and Floating Point](121_numerical_methods_and_floating_point.md)
moves from how to *hold* numbers to how *accurate* they are. The
`1e16 + 1.0 = 1e16` result at the end of this lesson is a preview:
[IEEE 754](121_numerical_methods_and_floating_point.md), catastrophic
cancellation, conditioning, and root-finding all follow from that one fact.
