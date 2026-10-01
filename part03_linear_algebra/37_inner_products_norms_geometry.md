# 37 — Inner Products, Norms, and Geometry

**Part**: part03_linear_algebra · **Prerequisites**: 35 · **Time**: 35 min

---

## In Plain Words

Everything so far has treated a vector as an abstract list of numbers, and a
matrix as a machine that shuffles such lists. That is enough for algebra but
not enough for intuition, because you cannot ask how *long* a vector is unless
you say how to measure length, and you cannot measure length without deciding
what counts as straight.

This lesson supplies that missing ruler. You measure a vector's length with a
rule you choose. There are several sensible rules and they genuinely disagree:
the straight-line distance, the distance if you had to walk along the axes one
at a time, and the size of the biggest single step. Once you have a ruler, you
can talk about angles, about how similar two directions are, and about what it
means for two directions to point at right angles.

The punchline is that this choice is not bookkeeping. Change the ruler and you
change which answer is "nearest", which changes which model you fit and which
one wins. This is the lesson where "all of machine learning is a choice of
distance function" stops being a slogan.

## Why Computer Science Cares

- **Every loss function is a norm.** `MSELoss` is L2, `MAELoss` is L1,
  `smooth_l1` is in between. Choosing between them changes which outliers your
  model ignores and which features it zeroes out.
- **L1 gives sparsity, L2 does not.** LASSO (`sklearn.linear_model.Lasso`, or
  `penalty='l1'`) sets coefficients to exactly zero; ridge (`Ridge`,
  `penalty='l2'`) only shrinks them. This one fact explains most of the
  difference between the two algorithms in practice.
- **Cosine similarity is the default for text.** `TfidfVectorizer` plus
  `cosine_similarity` is the classic retrieval stack. It is scale-invariant on
  purpose, so a long document is not treated as more relevant than a short one
  about the same thing.
- **k-NN's `metric` argument.** `KNeighborsClassifier(..., metric='manhattan')`
  versus `'minkowski'`, or `metric='cosine'`, changes which neighbour wins.
  On high-dimensional data this choice matters more than the choice of `k`.
- **Condition numbers.** `np.linalg.cond` measures how badly a skewed basis
  distorts everything downstream. Orthogonal bases are the best conditioned, and
  that is why QR and SVD work in orthogonal coordinates.
- **Adversarial examples** are built by finding a tiny perturbation in L2 that
  is large in L-infinity. The gap between those two norms is the vulnerability.

## The Formal Version

**Definition.** An **inner product** on a real vector space is a function
`⟨x, y⟩` that is bilinear, symmetric (`⟨x,y⟩ = ⟨y,x⟩`), and **positive
definite**: `⟨x,x⟩ > 0` for every `x ≠ 0`.

**Explanation.** Positive definiteness is the important clause. It is what makes
zero the only vector of length zero, and it is what lets us talk about angles at
all. Drop it and you can have nonzero vectors of zero length, and everything
downstream breaks.

On `ℝⁿ` the standard inner product is the **dot product**

```
xᵀy = Σᵢ xᵢ yᵢ
```

**Definition.** Given an inner product, the **norm** of `x` is
`‖x‖ = sqrt(⟨x, x⟩)`. For the standard dot product this is the Euclidean norm
`‖x‖₂ = sqrt(Σ xᵢ²)`.

**Definition.** The three norms you will meet most, for `p ≥ 1`:

```
‖x‖₁   = Σ |xᵢ|                 (L1, taxicab, Manhattan)
‖x‖₂   = sqrt(Σ xᵢ²)            (L2, Euclidean)  <- the default, always
‖x‖∞   = max |xᵢ|               (L-infinity, Chebyshev)
```

and in general `‖x‖ₚ = (Σ|xᵢ|ᵖ)^(1/p)`.

**Explanation.** L2 is the shortest path if you may move diagonally. L1 is the
shortest path if you may only move along the axes. L-infinity is how far you
must go if all your moves happen simultaneously. All are legitimate; they
answer different questions.

**Definition.** The **angle** between `x` and `y` is defined by

```
cos θ = ⟨x, y⟩ / (‖x‖ ‖y‖)
```

written `θ = arccos(⟨x,y⟩ / (‖x‖‖y‖))`.

**Definition.** The **cosine similarity** of `x` and `y` is
`cos θ` above, sometimes scaled to `[0, 1]` as `(1 + cos θ)/2`.

**Theorem (Cauchy–Schwarz).** For all `x, y`, `|⟨x, y⟩| ≤ ‖x‖ ‖y‖`, with
equality iff `x` and `y` are parallel.

**Explanation.** This is *why* the angle is well defined: the ratio can never
leave `[-1, 1]`, so `arccos` never sees an impossible argument. Without it
"angle" would be meaningless.

**Definition.** Vectors `x` and `y` are **orthogonal** (written `x ⊥ y`) iff
`⟨x, y⟩ = 0`, equivalently iff the angle between them is 90°.

**Theorem.** If `x ⊥ y` then `‖x + y‖² = ‖x‖² + ‖y‖²`.

**Explanation.** The ordinary Pythagorean theorem. Expand the left side and the
cross term `2⟨x,y⟩` vanishes. This is the single most useful fact in the whole
subject: the squared length of a sum of orthogonal pieces is the sum of the
squares, with no cross terms to fight. Parseval's identity, least squares, and
the theory of Fourier series are all this one fact repeated.

**Definition.** `x` and `y` are **parallel** iff `y = cx` for some scalar `c`.
Orthogonal and parallel are mutually exclusive for nonzero vectors.

**Definition.** The **distance** induced by a norm is `d(x, y) = ‖x − y‖`.

**Theorem.** A norm, and therefore its distance, satisfies positivity
(`‖x‖ ≥ 0`, with equality iff `x = 0`), homogeneity
(`‖cx‖ = |c|‖x‖`), and the triangle inequality (`‖x + y‖ ≤ ‖x‖ + ‖y‖`).

**Explanation.** The triangle inequality is the formal version of "the shortest
route between two points is a straight line" — and note that this is only true
in the L2 geometry. In L1 the shortest route is any monotone staircase, and
"distance" no longer behaves the way the picture in your head suggests. That is
the whole reason to care which norm you picked.

See [SYMBOLS.md](../../SYMBOLS.md) for `xᵀy`, `‖x‖`, `x ⊥ y`.

## Worked Example

Take the two vectors `x = (3, 4)` and `y = (1, 2)`.

**Step 1: the dot product.** `xᵀy = 3·1 + 4·2 = 3 + 8 = 11`.

**Step 2: the norms.**

```
‖x‖₂ = sqrt(3² + 4²) = sqrt(25) = 5
‖y‖₂ = sqrt(1² + 2²) = sqrt(5)  ≈ 2.23607
```

**Step 3: the cosine.** `cos θ = 11 / (5 · 2.23607) = 11 / 11.18034 = 0.98387`.

**Step 4: the angle.** `θ = arccos(0.98387) = 10.3894°`. So the two directions
are about 10° apart — nearly parallel.

**Step 5: verify Cauchy–Schwarz.** `|11| ≤ 5 · 2.23607 = 11.18034` ✓, and the
ratio `0.98387` sits just below 1, as it must for nearly-parallel vectors.

**Step 6: the same two vectors under L1.** `‖x − y‖₁ = |3−1| + |4−2| = 2 + 2
= 4`, while `‖x − y‖₂ = sqrt(4 + 4) = 2.828`. The L1 distance is *larger* than
the L2 distance, because L1 charges for the total travel and L2 for the
shortcut. Same vectors, same pair, different answers — which is the point of the
lesson.

## Runnable Code

```python
import math

# ---------- shared helpers ----------

def dot(u, v):
    return sum(a * b for a, b in zip(u, v))

def norm2(v):
    return math.sqrt(dot(v, v))

def norm1(v):
    return sum(abs(x) for x in v)

def norminf(v):
    return max(abs(x) for x in v)

def normalize(v):
    n = norm2(v)
    return [x / n for x in v]

def print_matrix(A, title=""):
    if title:
        print(title)
    for row in A:
        print("   " + "".join(f"{v:9.4f}" for v in row))
    print()

u = [3.0, 4.0]

print("One vector, three different 'lengths':")
print(f"   u = {u}")
print(f"   L2 (Euclidean) = sqrt(3^2 + 4^2)   = {norm2(u):.6f}   <- straight line")
print(f"   L1 (Manhattan) = |3| + |4|         = {norm1(u):.6f}   <- taxicab distance")
print(f"   Linf (Chebyshev) = max(|3|, |4|)    = {norminf(u):.6f}   <- largest single jump")
print()
print("All three are valid 'how far did I travel' measures. They disagree")
print("because they count different journeys:")
print("   L2 assumes you can move diagonally: sqrt(25) = 5 units")
print("   L1 assumes axis-aligned moves:       3 + 4 = 7 units")
print("   Linf assumes all moves happen at once: max single step = 4 units")
print()
print("L2 is the default in machine learning, and almost everything else in")
print("this part assumes it. Lesson 38 shows what changes when you swap it out.")

print("\n--- the Cauchy-Schwarz inequality: the reason the angle exists ---")
print("For every u, v:  |u.v| <= ||u|| ||v||, so cos(theta) always lands in [-1, 1].")
probes = [([1.0, 0.0], [0.0, 1.0]),
          ([1.0, 0.0], [1.0, 0.0]),
          ([1.0, 0.0], [-1.0, 0.0]),
          ([1.0, 1.0], [1.0, -1.0]),
          ([2.0, 3.0], [4.0, 6.0])]
for a, b in probes:
    cos = dot(a, b) / (norm2(a) * norm2(b))
    ang = math.degrees(math.acos(max(-1.0, min(1.0, cos))))
    print(f"   cos = {cos:+.6f}   angle = {ang:8.3f} deg   u={a} v={b}")
print("cos = 0 means a right angle. That is the whole content of orthogonality.")
print("The inequality is what stops acos from ever getting an argument outside")
print("[-1, 1] -- without it the angle would not be well defined.")

print("\n--- cosine similarity: scale-invariant, direction-only ---")
print("cosine(a, b) ignores the LENGTH of both vectors entirely.")
docs = {
    "cat document":  [1.0, 0.9, 0.8, 0.1, 0.0],
    "same, x10":     [10.0, 9.0, 8.0, 1.0, 0.0],
    "dog document":  [0.0, 0.1, 0.2, 0.9, 1.0],
}
keys = list(docs)
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        a, b = docs[keys[i]], docs[keys[j]]
        print(f"   cosine({keys[i]:>13}, {keys[j]:>13}) = {dot(a, b) / (norm2(a) * norm2(b)):+.6f}")
print("'same, x10' scores identically to 'cat document' -- as it should, because")
print("it is the same document with a different length. This is exactly what")
print("makes cosine similarity the default for text search: a long document is")
print("not more relevant than a short one about the same thing.")
```

Now the part that matters most — showing the choice of norm changing the answer:

```python
import math

# ---------- shared helpers ----------

def dot(u, v):
    return sum(a * b for a, b in zip(u, v))

def sub(u, v):
    return [a - b for a, b in zip(u, v)]

def norm2(v):
    return math.sqrt(dot(v, v))

def norm1(v):
    return sum(abs(x) for x in v)

def norminf(v):
    return max(abs(x) for x in v)

def angle(u, v):
    cos = dot(u, v) / (norm2(u) * norm2(v))
    return math.degrees(math.acos(max(-1.0, min(1.0, cos))))

target = [1.0, 0.0]

cands = [("A", [1.0, 0.1]), ("B", [0.95, 0.4]), ("C", [0.9, 0.6])]
far = [("D", [2.0, 2.0]), ("E", [0.3, 0.3]), ("F", [1.9, 0.5])]

METRICS = [
    ("L2", norm2),
    ("L1", norm1),
    ("Linf", norminf),
    ("angle", lambda v: angle(v, target)),
]

def table(rows, title):
    print(title)
    print(f"   {'pt':4s} {'vector':>14}  {'L2':>8} {'L1':>8} {'Linf':>8} {'angle':>9}")
    for label, v in rows:
        d = sub(v, target)
        print(f"   {label:4s} {str(v):>14}  {norm2(d):8.4f} {norm1(d):8.4f} "
              f"{norminf(d):8.4f} {angle(v, target):8.3f}d")
    print()
    for name, fn in METRICS:
        order = sorted(rows, key=lambda kv: fn(sub(kv[1], target)))
        print(f"   nearest by {name:6s} -> " + "  ".join(lbl for lbl, _ in order))
    print()

print("Target direction (1, 0). Which candidate is 'closest' to it?")
print()
table(cands, "A: all three candidates are genuinely nearby, so all metrics agree.")

table(far, "B: push them further out and the metrics disagree.")

print("L2, L1 and Linf all rank E (0.3, 0.3) first: it is a short hop from the")
print("target. The angle ranks F (1.9, 0.5) first instead, because F is only")
print("14.7 degrees off the target, while E is a full 45 degrees off. F is")
print("further away in absolute terms (L2 = 1.03 against 0.76) but points much")
print("more directly at the target, so the angle criterion prefers it.")
print()
print("Note that E and D tie on angle at exactly 45.000 degrees -- they lie on")
print("the same ray, so no angle test can ever separate them. Only a metric that")
print("notices length can. No single metric dominates the others.")
print()
print("So the choice is a MODELLING decision, not a technicality:")
print()
print("  * k-NN regression on house prices: use L2. If two houses are 10")
print("    metres apart in absolute terms, that is what matters, regardless of")
print("    which direction they differ in.")
print()
print("  * image or document retrieval by 'what is this like': use the angle.")
print("    A photo taken in bright light is the same photo, and cosine")
print("    similarity is blind to the overall scale factor exactly as intended.")
print()
print("  * L1 grows more slowly than L2 as a coefficient grows, so penalising")
print("    by L1 pushes unimportant coefficients all the way to zero instead of")
print("    merely shrinking them. That is exactly why LASSO (L1) produces SPARSE")
print("    models and ridge regression (L2) does not.")
print()
print("  * L-infinity is the 'worst component' norm, and it is what makes")
print("    adversarial examples work: a perturbation that is tiny in L2 can be")
print("    maximised in L-infinity, which is the norm attackers optimise.")
```

And the payoff — why orthogonality is the good case:

```python
import math

# ---------- shared helpers ----------

def dot(u, v):
    return sum(a * b for a, b in zip(u, v))

def add(*vs):
    return [sum(xs) for xs in zip(*vs)]

def scale(c, v):
    return [c * x for x in v]

def sub(u, v):
    return [a - b for a, b in zip(u, v)]

def norm2(v):
    return math.sqrt(dot(v, v))

def normalize(v):
    n = norm2(v)
    return [x / n for x in v]

def is_orthogonal(u, v, tol=1e-9):
    return abs(dot(u, v)) <= tol

def print_matrix(A, title=""):
    if title:
        print(title)
    for row in A:
        print("   " + "".join(f"{v:9.4f}" for v in row))
    print()

def print_vec(v, label=""):
    print(f"   {label:<22} {v}")

print("--- orthogonality is a dot product of zero ---")
pairs = [([1, 0, 0], [0, 1, 0]), ([1, 1], [1, -1]), ([1, 2, 3], [2, -1, 0]),
         ([1, 2], [2, -1]), ([3, 0], [1, 0])]
for a, b in pairs:
    print(f"   {str(a):<16} . {str(b):<14} = {dot(a, b):+5d}   "
          f"orthogonal: {is_orthogonal(a, b)}")

print()
print("The standard basis vectors are mutually orthogonal, and every OTHER")
print("basis is just a rotated version of it. Orthogonal bases are the good")
print("ones, and Lesson 38 builds them on purpose with Gram-Schmidt.")

print("\n--- Pythagoras, the reason orthogonal bases are special ---")
u, v = [3.0, 4.0], [4.0, -3.0]          # u . v = 12 - 12 = 0
w = add(u, v)                            # (7, 1)
print(f"   u   = {u}    |u|^2 = {dot(u, u)}")
print(f"   v   = {v}    |v|^2 = {dot(v, v)}")
print(f"   u+v = {w}   |u+v|^2 = {dot(w, w)}")
print(f"   |u|^2 + |v|^2 = {dot(u, u) + dot(v, v)}   equal? "
      f"{dot(u, u) + dot(v, v) == dot(w, w)}")
print("This is the ordinary Pythagorean theorem. It is exactly what makes")
print("Fourier analysis, Parseval's identity and least squares work: the")
print("squared length of a sum of orthogonal pieces is the SUM of the squares.")

# and a non-orthogonal counterexample
a, b = [1.0, 0.0], [1.0, 1.0]
print(f"\n   without orthogonality, a = {a}, b = {b}:")
print(f"   |a+b|^2 = {dot(add(a, b), add(a, b))}  but  "
      f"|a|^2 + |b|^2 = {dot(a, a) + dot(b, b)}")
print("The cross term 2(a.b) is non-zero, so the squares do not simply add.")
print("That extra cross term is the entire cost of using a bad basis.")

print("\n--- preview: projection is the orthogonal leftover ---")
p = [1.0, 1.0]
t = [3.0, 0.0]
proj = scale(dot(p, t) / dot(p, p), p)
resid = sub(t, proj)
print(f"   target t = {t}")
print(f"   onto   p = {p}")
print(f"   projection  = {proj}   (the part of t that lies along p)")
print(f"   leftover    = {resid}   (the part of t that does not)")
print(f"   leftover . p = {dot(resid, p):.10f}  <- zero, by construction")
print("Minimise |t - c*p| over all c and the derivative forces exactly this.")
print(f"   |t - proj|^2 = {dot(resid, resid):.6f},  the SMALLEST possible error")
print()
print("This is the whole idea behind least squares, PCA, and orthogonal")
print("projection of data. Lesson 38 does the derivation properly.")

print("\n--- the cosine is the dot product in disguise ---")
a, b = [2.0, 1.0], [3.0, -1.0]
cos = dot(a, b) / (norm2(a) * norm2(b))
print(f"   a = {a}, b = {b}")
print(f"   dot      = {dot(a, b)}")
print(f"   |a||b|   = {norm2(a) * norm2(b):.6f}")
print(f"   cos      = {cos:.6f}")
print(f"   angle    = {math.degrees(math.acos(cos)):.4f} degrees")
print("Dividing by the two lengths turns the raw dot product into a pure")
print("direction comparison. That single normalisation is cosine similarity,")
print("and it is why cos in [-1, 1] always: Cauchy-Schwarz bounds the numerator")
print("by the denominator.")
```

### With Libraries

```python
import numpy as np

print("Everything in this lesson is one numpy call.")

# ---- norms ----
u = np.array([3.0, 4.0])
print("u =", u)
print("np.linalg.norm(u)        =", np.linalg.norm(u), "  (L2, the default)")
print("np.linalg.norm(u, 1)     =", np.linalg.norm(u, 1), "  (L1 / Manhattan)")
print("np.linalg.norm(u, np.inf)=", np.linalg.norm(u, np.inf), "  (L-infinity)")
print("The default is ord=None, which means 2-norm. That single default is")
print("why 'L2' appears in almost every loss function you will ever write.")

# ---- dot, angle, cosine similarity ----
a = np.array([1.0, 0.0])
b = np.array([0.0, 1.0])
print("\nnp.dot(a, b) =", np.dot(a, b), " -> orthogonal, a 90 degree angle")
cos = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
print("cosine =", cos, " angle =", np.degrees(np.arccos(cos)))

X = np.array([[1.0, 0.9, 0.8, 0.1, 0.0],      # a document about cats
              [1.0, 0.0, 0.1, 0.9, 1.0]])     # a document about dogs
print("\n--- vectorised cosine similarity: one line, no loop ---")
Xn = X / np.linalg.norm(X, axis=1, keepdims=True)   # normalise each ROW
S = Xn @ Xn.T                                        # all pairs at once
print("the similarity matrix (row i vs column j):")
print(np.round(S, 6))
print("Diagonal is 1 by construction, and off-diagonal entries are the")
print("cosine similarities. This is the whole of vector search.")
print("scikit-learn wraps it:  cosine_similarity(X)  or  TfidfVectorizer")

# ---- distances ----
P = np.array([0.0, 0.0])
Q = np.array([3.0, 4.0])
print("\n--- three distances between (0,0) and (3,4) ---")
print("Euclidean   :", np.linalg.norm(Q - P))
print("Manhattan   :", np.linalg.norm(Q - P, ord=1))
print("Chebyshev   :", np.linalg.norm(Q - P, ord=np.inf))
print("scipy also has:")
from scipy.spatial.distance import cdist, cityblock, chebyshev
pts = np.array([[0.0, 0.0], [3.0, 4.0]])
print("   cdist(pts, pts, 'euclidean') =\n", cdist(pts, pts, 'euclidean'))
print("   cdist(pts, pts, 'cityblock') =\n", cdist(pts, pts, 'cityblock'))
print("   cdist(pts, pts, 'chebyshev') =\n", cdist(pts, pts, 'chebyshev'))

# ---- orthogonality and bases ----
print("\n--- orthogonality is a matrix product ---")
V = np.array([[1.0, 1.0], [1.0, -1.0]])     # columns are orthogonal
print("V =\n", V)
print("V.T @ V =\n", V.T @ V, "  <- diagonal, so the columns are orthogonal")
print("The off-diagonal entries are exactly 0. Gram-Schmidt in lesson 38 is")
print("just the procedure that forces this to happen for an arbitrary basis.")

print("\n--- why orthogonal bases matter: no cancellation in the inverse ---")
B = np.array([[1.0, 1.0], [1.0, -1.0]])
C = np.array([[1.0, 1.0], [1.0, 2.0]])       # nearly parallel columns
print("orthogonal-ish B:\n", B, "\n B^-1 =\n", np.round(np.linalg.inv(B), 4))
print("skewed C:\n", C, "\n C^-1 =\n", np.round(np.linalg.inv(C), 4))
print("np.linalg.cond(C) =", round(np.linalg.cond(C), 4),
      " vs cond(B) =", round(np.linalg.cond(B), 4))
print("A higher condition number means small input errors cause large output")
print("errors. Skewed bases have high condition numbers; orthogonal ones are")
print("as well conditioned as it is possible to be. That is why QR")
print("factorisation and SVD prefer to work in orthogonal coordinates.")
```

## Common Mistakes

**1. Forgetting that cosine ignores length, or expecting it not to.**

```python
import numpy as np

a = np.array([1.0, 1.0])
b = np.array([100.0, 100.0])
# WRONG: treating cosine as a distance that grows with size
print("are these 'far apart'?", np.linalg.norm(a - b))
print("cosine says:", np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
```

```python
import numpy as np

a = np.array([1.0, 1.0])
b = np.array([100.0, 100.0])
# RIGHT: they point the same way, so similarity is 1 no matter the magnitude
cos = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
print("cosine similarity =", round(float(cos), 12))
print("Euclidean distance =", np.linalg.norm(a - b))
print("Two different questions, two different answers. Deciding which one")
print("you meant is the modelling decision.")
```

Tempting because "similarity" sounds like it should agree with "distance", but
they are different functions. A common real bug: deduplicating documents with
Euclidean distance and being surprised that every document of similar *length*
looks like a near-duplicate.

**2. Assuming L1 and L2 rank points the same way.**

```python
import math

def l2(a, b):
    return math.dist(a, b)                                  # euclidean
def l1(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))            # manhattan
def linf(a, b):
    return max(abs(x - y) for x, y in zip(a, b))            # chebyshev

P = [(0.0, 0.0), (3.0, 4.0)]
for i, p in enumerate(P):
    for q in P[i + 1:]:
        print(p, q, "L2 =", round(l2(p, q), 4), "L1 =", round(l1(p, q), 4),
              "Linf =", round(linf(p, q), 4))
print("L1 (7.0) > L2 (5.0) > Linf (4.0) for the same pair, always: the")
print("higher the p, the more the norms converge. See the norm inequality")
print("||x||_inf <= ||x||_2 <= ||x||_1 for any vector.")
```

The tempting wrong belief is that "Manhattan is always shorter, because it is
the shortest path in a grid". That confuses the *path* with the *distance*: the
distance is still 5, it is just measured differently. The inequality
`‖x‖∞ ≤ ‖x‖₂ ≤ ‖x‖₁` holds for every vector, which is worth memorising.

**3. Dividing by the norm of a zero vector.**

```python
import numpy as np

v = np.zeros(5)
# WRONG: dividing by zero. numpy warns and hands back nan, and if you never
# check, the nan propagates silently through your whole model.
with np.errstate(invalid="ignore", divide="ignore"):
    cos = np.dot(v, v) / (np.linalg.norm(v) * np.linalg.norm(v))
print("cosine with a zero vector =", cos, " <- nan, silently")
print("np.dot(v, v) =", np.dot(v, v), "and np.linalg.norm(v) =", np.linalg.norm(v))
print("The numerator and denominator are both exactly 0, so this is 0/0.")
```

```python
import numpy as np

def safe_cosine(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na < 1e-12 or nb < 1e-12:      # no direction defined for the zero vector
        return 0.0
    return float(np.dot(a, b) / (na * nb))

print("cosine with a zero vector =", safe_cosine(np.zeros(5), np.array([1.0, 2.0])))
print("This is why TF-IDF and every embedding model discard empty documents,")
print("and why you should check for zero rows before normalising a matrix.")
```

Tempting because the zero vector is a perfectly legal input and the formula
looks harmless. The angle is genuinely undefined for it — there is no direction
to compare.

**4. Treating every basis as equally good.**

```python
import numpy as np

good = np.array([[1.0, 1.0], [1.0, -1.0]])
bad = np.array([[1.0, 1.0], [1.001, 1.0]])     # nearly parallel columns
for name, B in (("orthogonal", good), ("nearly parallel", bad)):
    x = np.array([1.0, 1.0])
    print(f"{name:16s} cond = {np.linalg.cond(B):10.2f}   "
          f"B^-1 @ x = {np.round(np.linalg.inv(B) @ x, 6)}")
print("A tiny change in the input produces an enormous change in the answer")
print("for the skewed basis. Orthogonal bases are the best conditioned that")
print("any basis can be, which is why QR and SVD build them deliberately.")
```

**5. Assuming "orthogonal" and "independent" mean the same thing.**

```python
import math

def dot(u, v):
    return sum(a * b for a, b in zip(u, v))

# three independent vectors in R^2 -- possible, so they are not orthogonal
a, b, c = [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]
print("det of [a, c] =", a[0] * c[1] - a[1] * c[0])
print("a . b =", dot(a, b), " b . c =", dot(b, c), " a . c =", dot(a, c))
print("Independent, and yet NO TWO of them are orthogonal.")
print("Orthogonal => independent always. Independent => orthogonal NEVER.")
```

Tempting because in `ℝⁿ` an orthogonal set is automatically a basis, so the two
words blur together. The converse fails hard: in `ℝ²` you can have three
independent vectors, and at most two mutually orthogonal ones. Lesson
[38](38_orthogonality_and_least_squares.md) separates them properly and builds
orthogonal bases on purpose.

## Formula Sheet

Symbols follow [SYMBOLS.md](../../SYMBOLS.md). `x, y ∈ ℝⁿ` are column vectors,
`W` is a diagonal weighting matrix, `p ≥ 1`.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| dot product | `$x^{\mathsf T}y = \sum_i x_i y_i$` | multiply matching coordinates and add | the default pairing of two vectors; first line of almost every scoring function |
| inner product | `$\langle x, y \rangle$` | bilinear, symmetric, and zero only for `x = 0` | defining an angle at all; requires **positive definiteness**, which the other properties do not imply |
| L2 norm | `$\lVert x\rVert_2 = \sqrt{\sum_i x_i^2}$` | straight-line distance from the origin | the default in machine learning; `MSELoss`, `np.linalg.norm(x)` with no `ord` |
| L1 norm | `$\lVert x\rVert_1 = \sum_i \lvert x_i\rvert$` | total travel if you move only along axes | `MAELoss`, `penalty='l1'` (LASSO), `metric='manhattan'` — the source of sparsity |
| L-infinity norm | `$\lVert x\rVert_\infty = \max_i \lvert x_i\rvert$` | size of the single largest coordinate | `metric='chebyshev'`; adversarial attacks maximise this |
| general `p`-norm | `$\lVert x\rVert_p = \left(\sum_i \lvert x_i\rvert^p\right)^{1/p}$` | `p`-powered root sum of absolute values | `KNeighborsClassifier(metric='minkowski', p=…)`; valid only for `p ≥ 1` — below that it fails the triangle inequality |
| norm inequality | `$\lVert x\rVert_\infty \le \lVert x\rVert_2 \le \lVert x\rVert_1$` | for any vector, all three numbers are ordered this way | sanity-checking a norm computation; implies the three unit balls nest |
| unit vector | `$\lVert x\rVert_2 = 1$` | a pure direction with length 1 | cosine similarity and projection both require both inputs normalised |
| normalisation | `$\hat x = x / \lVert x\rVert_2$` | rescale a vector to length 1 without turning it | `Xn = X / np.linalg.norm(X, axis=1, keepdims=True)` for cosine similarity |
| weighted inner product | `$\langle x, y\rangle_W = (W^{1/2}x)^{\mathsf T}(W^{1/2}y) = x^{\mathsf T}Wy$` | the dot product after per-coordinate rescaling by `√Wᵢᵢ` | feature weighting in k-NN and regularised regression |
| weighted norm | `$\lVert x\rVert_W = \sqrt{x^{\mathsf T}Wx}$` | length measured with coordinates `xᵢ` counting `Wᵢᵢ` times as much | any application where features have different natural units |
| restriction on `W` | `W` diagonal with `W_{ii} > 0` | every coordinate must get a strictly positive weight | `x^{\mathsf T}Wx = 0` must force `x = 0`; a zero or negative weight breaks positive definiteness |
| angle | `$\theta = \arccos\!\big(\langle x,y\rangle / (\lVert x\rVert\lVert y\rVert)\big)$` | the angle between two directions | only defined for nonzero `x` and `y` — dividing by `‖0‖` gives 0/0 |
| cosine similarity | `$\cos\theta = \dfrac{x^{\mathsf T}y}{\lVert x\rVert_2\lVert y\rVert_2}$` | agreement of direction, ignoring size | text retrieval, `cosine_similarity`, `metric='cosine'`; values in `[−1, 1]` |
| rescaled cosine | `$(1 + \cos\theta)/2$ | the same thing moved from `[−1,1]` into `[0,1]` | needed when a downstream API insists on nonnegative scores |
| orthogonal | `$x \perp y \iff x^{\mathsf T}y = 0$` | the two vectors make a right angle | checking a basis is orthogonal; the precondition for everything in [38](38_orthogonality_and_least_squares.md) |
| parallel | `$y = cx$ for some scalar $c$ | one vector is a scalar copy of the other | the equality case of Cauchy–Schwarz |
| Cauchy–Schwarz | `$\lvert x^{\mathsf T}y\rvert \le \lVert x\rVert_2\lVert y\rVert_2$` | the dot product can never exceed the product of lengths | the reason `arccos` never sees an argument outside `[−1, 1]`; requires a real inner product |
| Pythagoras for vectors | `$x \perp y \Rightarrow \lVert x+y\rVert_2^2 = \lVert x\rVert_2^2 + \lVert y\rVert_2^2$` | squared lengths of perpendicular pieces just add | the entire reason orthogonal bases are worth building — no cross terms |
| distance | `$d(x,y) = \lVert x - y\rVert$` | how far apart two points are | `k`-NN, clustering, `math.dist` |
| norm axioms | `$\lVert x\rVert \ge 0$`, `$\lVert x\rVert = 0 \iff x = 0$`, `$\lVert cx\rVert = \lvert c\rVert\lVert x\rVert$`, `$\lVert x+y\rVert \le \lVert x\rVert + \lVert y\rVert$` | positivity, homogeneity, triangle inequality | what makes "length" a length; the triangle inequality is false for L1-style *paths* |
| projection preview | `$\text{proj}_p(t) = \dfrac{p^{\mathsf T}t}{p^{\mathsf T}p}\,p$` | the point on the line through `p` nearest to `t` | introduced at the end of this lesson, derived fully in [38](38_orthogonality_and_least_squares.md); needs `p ≠ 0` |
| residual | `$t - \text{proj}_p(t)$, with `$p^{\mathsf T}\bigl(t - \text{proj}_p(t)\bigr) = 0$` | what is left over, and it is perpendicular to `p` | the leftover is the smallest achievable error — this is least squares |
| condition number | `$\text{cond}(B) = \sigma_{\max}(B)/\sigma_{\min}(B) \ge 1$ | worst-case amplification of input error by `B⁻¹` | `np.linalg.cond`; equals 1 exactly when `B` is a scalar multiple of an orthogonal matrix |
| Gram matrix | `$G = V^{\mathsf T}V$ | cross-multiplies a set of vectors into a matrix | testing orthogonality: `V` has orthogonal columns **iff** `G` is diagonal. Diagonal entries are `‖vᵢ‖²` |

Two restrictions to carry forward. Every formula with `‖x‖` in the denominator
needs `x ≠ 0`, which is why library code checks `‖x‖ < 1e-12` before
normalising. And `p ≥ 1` is not a convention: for `p < 1` the triangle inequality
fails, so `‖·‖ₚ` is not a norm and `k`-NN will silently stop satisfying the
triangle-inequality-based guarantees.

## Multiple Choice Questions

**Q1.** What does `cos θ = 0` say about two nonzero vectors?

- A) They are the same length
- B) They are orthogonal, i.e. the angle between them is 90°
- C) One of them is the zero vector
- D) They are parallel but pointing in opposite directions

<details>
<summary>Answer and explanation</summary>

**B) They are orthogonal, i.e. the angle between them is 90°.**

`arccos(0) = π/2 = 90°`, and `cos θ = 0` is equivalent to `xᵀy = 0`, which is
the definition of orthogonality. The code block prints exactly this: for
`(1,0)` and `(0,1)` it reports `cos = +0.000000, angle = 90.000 deg`, and for
`(1,1)` and `(1,−1)` the same, with the dot product `1·1 + 1·(−1) = 0`.

A confuses the *angle* with the *lengths*: the angle knows nothing about `‖x‖`
or `‖y‖` because both were divided out. D is the opposite confusion — parallel
vectors have `cos θ = ±1`, not 0. In the code's probe list, `(1,0)` against
`(−1,0)` gives `cos = −1` and angle `180°`, which is the antiparallel case, and it
is precisely as far from orthogonal as parallelism is. C is wrong because both
vectors are assumed nonzero; `cos` is `0/0` for a zero vector and `nan`, which is
Common Mistake 3.

</details>

**Q2.** A document and a 10× longer version of the same document have cosine
similarity 1 but Euclidean distance about 9× larger. Which statement explains
this?

- A) Cosine similarity ignores length; Euclidean distance is dominated by it
- B) The two metrics disagree, so at least one of them has a numerical bug
- C) Cosine similarity ignores direction and measures only length
- D) Euclidean distance is not defined for vectors of different lengths

<details>
<summary>Answer and explanation</summary>

**A) Cosine similarity ignores length; Euclidean distance is dominated by it.**

Cosine divides by `‖x‖‖y‖`, so scaling *either* vector by a positive constant
leaves it unchanged. The code shows this with `"cat document"` and
`"same, x10"`: the similarity is `+1.000000` in both pairings, while
`‖a − b‖₂` for `(1,1)` against `(100,100)` is about 140.

C has it exactly backwards — cosine is the *direction* measure, and dividing out
the norms is the only thing it does. That is why `TfidfVectorizer` plus
`cosine_similarity` is the standard retrieval stack: a 5000-word essay about
cats should not outrank a 200-word one. B is false because both functions are
behaving exactly as their definitions require; two different questions have two
different answers. D is false — `‖x − y‖₂` is defined for any pair of same-length
vectors, and `(100,100) − (1,1) = (99,99)` is an ordinary vector with norm
`99√2 ≈ 140.0`.

</details>

**Q3.** For `x = (1, 0)` and `y = (1.9, 0.5)`, what are the L2 distance between
them and the angle between their directions?

- A) L2 distance 1.03, angle 14.7°
- B) L2 distance 0.87, angle 14.7°
- C) L2 distance 1.03, angle 75.3°
- D) L2 distance 0.90, angle 14.7°

<details>
<summary>Answer and explanation</summary>

**A) L2 distance 1.03, angle 14.7°.**

The distance: `y − x = (0.9, 0.5)`, so `‖y − x‖₂ = √(0.81 + 0.25) =
√1.06 ≈ 1.0296 ≈ 1.03`. This is the value the lesson's table prints for
candidate `F`.

The angle: `cos θ = xᵀy / (‖x‖‖y‖) = 1.9 / (1 · √(1.9² + 0.5²)) = 1.9 / √3.86 =
1.9/1.96469 = 0.96708`, so `θ = arccos(0.96708) = 14.744°`. Equivalently
`arctan(0.5/1.9) = arctan(0.2632)`, since one vector lies along the x-axis.

The point of the question is that these are two *different* quantities and both
are correct: `y` is 1.03 units away in absolute terms while pointing only 14.7°
off `x`. That gap is exactly what makes the metric choice matter — the lesson's
code finds the closest candidate by L2 and the most *similar* one by angle, and
they are not the same point.

B inverts the coordinate differences (`0.5 − 0.9` instead of `0.9 − 0.5` squared)
and gets a spurious norm. C takes the complement `90° − 14.7° = 75.3°`, which
would be the angle to the vector *perpendicular* to `x`, not to `y`. D uses the
first coordinate difference alone, `0.9`, forgetting that `y` is also displaced by
`0.5` in the second direction — the mistake of computing a distance
componentwise and then failing to square-and-add.

</details>

**Q4.** Why does Cauchy–Schwarz matter beyond being a nice inequality?

- A) It proves that `‖x‖₂ ≥ 0` for every `x`
- B) It guarantees `xᵀy / (‖x‖‖y‖)` stays in `[−1, 1]`, so the angle and `arccos` are well defined
- C) It shows that every norm satisfies the triangle inequality
- D) It proves that orthogonal vectors are linearly independent

<details>
<summary>Answer and explanation</summary>

**B) It guarantees `xᵀy / (‖x‖‖y‖)` stays in `[−1, 1]`, so the angle and `arccos`
are well defined.**

Without the inequality, `arccos` could receive `1.7` and return `nan`. The code
wraps the call in `max(-1.0, min(1.0, cos))` precisely because floating-point
rounding can push the ratio a hair outside the interval, and the lesson says so:
"The inequality is what stops `acos` from ever getting an argument outside
`[-1, 1]` — without it the angle would not be well defined."

A is one of the norm axioms, which hold for any norm and have nothing to do
with two vectors at once. C is also a norm axiom (the triangle inequality), and
Cauchy–Schwarz would follow from it — not the other way round; moreover the
triangle inequality is *not* what Cauchy–Schwarz is usually cited for. D is true
but is a different theorem, proved from `x = 0 ⇒ ‖x‖² = 0 ⇒ xᵀy = 0 ⇒ y = 0`, not
from Cauchy–Schwarz. The lesson's Mistake 5 makes exactly this separation:
orthogonal ⇒ independent always, independent ⇒ orthogonal never.

</details>

**Q5.** In `ℝ²`, let `a = (1,0)`, `b = (0,1)`, `c = (1,1)`. Which statement is
true?

- A) All three are pairwise orthogonal
- B) All three are linearly independent
- C) `a` and `c` are orthogonal because their first coordinates match
- D) At most two of them can be pairwise orthogonal, and `a ⊥ b`

<details>
<summary>Answer and explanation</summary>

**D) At most two of them can be pairwise orthogonal, and `a ⊥ b`.**

`a·b = 0`, `b·c = 1`, `a·c = 1`. So `a` and `b` are orthogonal and nothing else
is. The lesson's Mistake 5 code prints exactly these dot products with the
conclusion "Independent, and yet NO TWO of them are orthogonal."

A fails on the two nonzero dot products. B fails because `c = a + b`, so the
three are dependent — three vectors cannot be independent in `ℝ²`. C is
nonsense: matching coordinates has nothing to do with orthogonality, and
`(1,0)·(1,1) = 1 ≠ 0`. The real content of D is the one-way implication:
orthogonality is a *stronger* condition than independence, so it can never hold
for more vectors than the dimension allows. Every orthogonal set is a basis of
its span, but not every basis is orthogonal — which is why
[38](38_orthogonality_and_least_squares.md) has to work to build one.

</details>

**Q6.** Which norm gives a sparsity-inducing penalty on a linear model's
coefficients?

- A) L2, because it sets small coefficients to exactly zero
- B) L1, because the penalty is not differentiable at zero
- C) L2, because it grows fastest as a coefficient grows
- D) L1, because it is always the largest of the three norms

<details>
<summary>Answer and explanation</summary>

**B) L1, because the penalty is not differentiable at zero.**

`|c|` has a corner at `c = 0`, so the subgradient there is the interval `[−1, 1]`
rather than a single number. Zero-gradient-descent can therefore sit *at* zero,
and the resulting model has genuinely zero coefficients. This is exactly the
`sklearn.linear_model.Lasso` behaviour the lesson reports, and `smooth_l1` is
mentioned as the compromise that gives up hard zeros to gain a gradient.

A has the two halves swapped: L2's `c²` penalty has derivative `2c`, which is
zero *only* at zero, so gradient descent approaches zero without ever reaching
it — ridge shrinks, LASSO zeroes. C is backwards; for large `|c|`, `|c|` grows
*slower* than `c²`, which is precisely why L1 penalises less overall but zeroes
rather than shrinks. D is true but irrelevant: `‖x‖₁ ≥ ‖x‖₂` always holds, and
that ordering has nothing to do with sparsity. The mechanism is the kink, not the
size.

</details>

**Q7.** Two basis matrices are `B = [[1,1],[1,−1]]` and `C = [[1,1],[1.001,1]]`.
Both are invertible. What does `np.linalg.cond` tell you that the determinant
does not?

- A) That `C` is singular, since its determinant is nearly zero
- B) That `C`'s columns are nearly parallel, so `C⁻¹` amplifies input error by up to about 4002×
- C) That `B` is orthogonal and therefore has no eigenvalues
- D) That `C` has smaller entries, so it must be better conditioned

<details>
<summary>Answer and explanation</summary>

**B) That `C`'s columns are nearly parallel, so `C⁻¹` amplifies input error by up
to about 4002×.**

The lesson prints `cond = 1.00` for `B` and `cond = 4002.00` for `C`. The
demonstration is stark: with `x = (1, 1)`, adding `10⁻⁴` to the first coordinate
gives solution `(1.00005, 0.00005)` for `B` — an error of 5×10⁻⁵ for a
perturbation of 10⁻⁴, essentially no amplification — and `(−0.1, 1.1001)` for
`C`, an error of about 0.1 for the same 10⁻⁴. A factor of 1000.

A is wrong: `det(C) = 1·1 − 1·1.001 = −0.001`, which is small but nonzero, so
`C` is invertible. Small determinant is a *symptom*; the condition number
measures it properly. `det(B) = −2` and `det(C) = −0.001` differ by 2000×, which
is the same story told less sharply — the condition number is scale-invariant,
the determinant is not. C is confused about orthogonality: `BᵀB = 2I`, so `B` is
orthogonal up to scale, and it has real eigenvalues 2 and −2 like any matrix. D
is backwards on every count.

</details>

**Q8.** You want to compare two text snippets for *topical* similarity, ignoring
how long either one is. Which setup is the defensible one?

- A) Normalise each document to unit L2 length, then take the dot product
- B) Take the raw dot product of the TF-IDF vectors
- C) Compare Euclidean distances between the raw vectors
- D) Normalise each document so its largest coordinate is 1, then take the dot product

<details>
<summary>Answer and explanation</summary>

**A) Normalise each document to unit L2 length, then take the dot product.**

That is precisely cosine similarity, and it is what
`Xn = X / np.linalg.norm(X, axis=1, keepdims=True)` followed by `Xn @ Xn.T`
does in the lesson's library section. Dividing by each vector's length removes
the length information while keeping the direction, so a document and a 10×
longer version of it score identically at 1.

B is the natural first attempt and the reason TF-IDF exists at all: raw term
frequency makes a long document score high just for being long. TF-IDF's inverse
document frequency already fights this, but it does not eliminate length, so
cosine is still applied on top. C inherits exactly that problem — the lesson's
Mistake 1 names deduplicating with Euclidean distance and finding every
similarly-*sized* pair looks like a near-duplicate. D is a genuine trap: it is
L-infinity normalisation, and it is *not* scale-invariant in the sense cosine is
— scaling a document by `c > 0` leaves its cosine similarity untouched but
changes its max-normalised form whenever the scale factor shifts which
coordinates are largest. The lesson notes the L∞ unit ball is a square, not a
sphere, precisely because that norm is not rotation-symmetric.

</details>

**Q9.** You must compute distances in a feature vector whose first coordinate is
in metres and second in milliseconds. Which choice is defensible?

- A) Whichever norm you like — the units do not matter, norms are unitless
- B) L2 on the raw numbers, since `‖x‖₂` already corrects for scale
- C) A weighted inner product with positive diagonal weights that put the two coordinates on a comparable footing
- D) The zero vector, so no unit ever matters

<details>
<summary>Answer and explanation</summary>

**C) A weighted inner product with positive diagonal weights that put the two
coordinates on a comparable footing.**

This is `xᵀWy` with `W` diagonal and `W_{ii} > 0`; the induced length is
`‖x‖_W = √(xᵀWx)`. For example with `W = diag(4, 1)` the length of `(2,1)` is
`√(4·4 + 1·1) = √17 ≈ 4.1231`, so the metre coordinate counts four times as much
as the millisecond one. Every requirement of the lesson's definition is
preserved: positivity, homogeneity and the triangle inequality all survive for
positive diagonal `W`, and `‖x‖_W = 0` still forces `x = 0`.

A confuses the norm with the coordinates. A norm *is* measured in the units of
its input — `‖x‖₂` for `(3,4)` is `5` of whatever those numbers are. B is the
most tempting mistake, because `‖x‖₂ = √(Σxᵢ²)` does involve squares, which
sounds like a scale correction. It is not: squaring does not remove units, and
`√(3² + 4²)` in metres-and-milliseconds is not a length in any useful sense. D
is not a norm at all — the zero vector has no direction, so distance to it is
degenerate and `k`-NN collapses.

</details>

**Q10.** The triangle inequality `‖x + y‖ ≤ ‖x‖ + ‖y‖` is claimed to encode "the
straight line is the shortest route". Why is that intuition misleading for L1?

- A) Because L1 does not satisfy the triangle inequality at all
- B) Because under L1 many different staircase paths are equally shortest, so there is no unique "shortest route" to generalise from
- C) Because L1 is always larger than L2, so the inequality is trivially satisfied
- D) Because L1 is only defined on integer coordinates

<details>
<summary>Answer and explanation</summary>

**B) Because under L1 many different staircase paths are equally shortest, so
there is no unique "shortest route" to generalise from.**

Going from `(0,0)` to `(3,4)` under L1 costs `|3| + |4| = 7`. Any monotone
staircase — one vertical step of 4 then one horizontal step of 3, or three
thousands of tiny interleaved steps — costs exactly 7. The picture in your head
("the straight line wins uniquely") does not survive, and the inequality
`‖x‖∞ ≤ ‖x‖₂ ≤ ‖x‖₁` means L1 is the *largest* of the three, so the bound looks
slack rather than tight.

A is false: the lesson states the triangle inequality as a property of a norm
generally, and L1 satisfies it. C is true but is not the reason — the
satisfaction is uninformative when it is far from tight. D is false; L1 is
defined on all of `ℝⁿ`, and the lesson's code computes it on `(0.3, 0.4)`. This
is why the lesson calls the choice of norm a modelling decision: in L1 geometry
the "straightest line" intuition simply has no privileged object.

</details>

## Subjective Questions

### Short Answer

**Q1. State the three properties an inner product must satisfy, and say which one
does the real work.**

<details>
<summary>Model answer</summary>

An inner product `⟨x, y⟩` must be **bilinear** (linear in each argument
separately), **symmetric** (`⟨x,y⟩ = ⟨y,x⟩`), and **positive definite**
(`⟨x,x⟩ > 0` for every `x ≠ 0`).

Positive definiteness is the one that does the work. It makes zero the only
vector of length zero, so `‖x‖ = √⟨x,x⟩` is a genuine length and
`x ⊥ y ⇔ ⟨x,y⟩ = 0` is a genuine right angle. The lesson says it directly:
"Drop it and you can have nonzero vectors of zero length, and everything
downstream breaks." A degenerate symmetric bilinear form like `⟨x,y⟩ = x₁y₁` on
`ℝ²` is bilinear and symmetric and is not an inner product, because `(0,1)` has
`⟨x,x⟩ = 0`.

</details>

**Q2. Define the L1, L2 and L-infinity norms and state the inequality relating
them.**

<details>
<summary>Model answer</summary>

`‖x‖₁ = Σᵢ|xᵢ|` (taxicab, axis-aligned travel), `‖x‖₂ = √(Σᵢxᵢ²)` (Euclidean,
straight line), `‖x‖∞ = maxᵢ|xᵢ|` (largest single step). More generally
`‖x‖ₚ = (Σᵢ|xᵢ|ᵖ)^(1/p)`.

They always satisfy `‖x‖∞ ≤ ‖x‖₂ ≤ ‖x‖₁` for every `x` and every `p ≥ 1`. Proof of
the first: `Σxᵢ² ≤ n·maxᵢ|xᵢ|²`, and `√n·max|xᵢ|` is an upper bound on the L2 norm,
so `max|xᵢ| ≤ ‖x‖₂`. For the second, `Σ|xᵢ|² ≤ (Σ|xᵢ|)²`, since the square of a
sum of nonnegatives expands to include all the cross terms.

</details>

**Q3. Why is the L2 unit ball a disc while the L1 and L-infinity unit balls are
squares? State the geometric reason.**

<details>
<summary>Model answer</summary>

The L2 unit ball is `{x : xᵀx = 1}` — a circle, because `‖x‖₂² = Σxᵢ²` is a sum
of squares, the standard equation of a sphere. The L1 unit ball is
`{x : Σ|xᵢ| = 1}`, a diamond in 2D, and the L-infinity unit ball is
`{x : max|xᵢ| = 1}`, an axis-aligned square with corners at `(±1, ±1)`.

They nest — box ⊇ disc ⊇ diamond — because of `‖x‖∞ ≤ ‖x‖₂ ≤ ‖x‖₁`: for a fixed
threshold of 1, a smaller norm accepts a larger set of points. Note the two
squares have different *orientations*: the L1 diamond's diagonals lie on the
axes while the L∞ box's edges do. That anisotropy is why L1-based models can
treat `(1,1)` and `(1,−1)` directions differently.

</details>

**Q4. Explain why `‖x‖₂ = ‖c‖x‖₂` holds and why the absolute value is necessary.**

<details>
<summary>Model answer</summary>

Because `‖cx‖₂ = √(Σ(cxᵢ)²) = √(c²Σxᵢ²) = |c|√(Σxᵢ²) = |c|‖x‖₂`.

The absolute value is necessary because a length is nonnegative and lengths do
not carry a sign. Scaling by `c = −2` moves a vector to the opposite side of the
origin, which is a distance of twice as much, not "negative twice as much". Drop
the bars and `‖−x‖₂ = −‖x‖₂ < 0`, which contradicts the positivity axiom. This is
exactly the same reason `λ < 0` in `Ax = λx` in [36](36_eigenvalues_and_eigenvectors.md)
flips a direction end to end rather than shrinking it.

</details>

**Q5. What does it mean for two vectors to be orthogonal, and what does it buy you
in terms of lengths?**

<details>
<summary>Model answer</summary>

`x ⊥ y` means `xᵀy = 0`, equivalently that the angle between them is 90°. The
payoff is the vector form of Pythagoras: `‖x + y‖₂² = ‖x‖₂² + ‖y‖₂²`, because
expanding the left side gives `‖x‖² + 2xᵀy + ‖y‖²` and the cross term vanishes.

So the squared length of a sum of mutually orthogonal pieces is just the sum of
their squared lengths, with no cross terms to fight. That single identity is
what Parseval's identity, least squares, the Fourier transform and PCA are all
restatements of. The lesson's code prints `|u|² + |v|² = 50, |u+v|² = 50` for
the perpendicular pair `(3,4)` and `(4,−3)`, and contrasts it with
`(1,0)`, `(1,1)` where the cross term `2(a·b) = 2` makes the sum larger.

</details>

**Q6. Give a concrete example where the choice of norm changes which point is
"nearest", using numbers.**

<details>
<summary>Model answer</summary>

Target `(1, 0)`; candidates `E = (0.3, 0.3)` and `F = (1.9, 0.5)`.

`‖E − t‖₂ = √(0.49 + 0.09) = √0.58 ≈ 0.762`, `‖F − t‖₂ = √(0.81 + 0.25) =
√1.06 ≈ 1.030`. So L2, L1 and L-infinity all pick `E` — every absolute-distance
metric does, because `E` is genuinely closer.

But the *angle* to the target differs sharply: `E` is at `arctan(0.3/0.3) = 45°`
while `F` is at `arctan(0.5/1.9) ≈ 14.74°`. Any angle-based criterion picks `F`.
So for "which image is this like", the answer is `F`; for "which house is this
near", it is `E`. Same pair of points, same target, two different winners — the
choice of metric is a statement about what you mean.

</details>

### Long Answer

**Q1. Why is Cauchy–Schwarz necessary for the angle to exist, and what breaks if
you try to define an angle without it?**

<details>
<summary>Model answer</summary>

The definition `cos θ = xᵀy / (‖x‖‖y‖)` is a definition *of* the angle only if the
right-hand side is a real number in `[−1, 1]`, because that is exactly the range
of `cos`. Cauchy–Schwarz, `|xᵀy| ≤ ‖x‖‖y‖`, delivers that: divide both sides by
the positive product of norms and the ratio is bounded by 1 in absolute value.
So `arccos` receives a legal argument and returns a number in `[0°, 180°]`.

Without it, the "angle" would be a formula that sometimes returns a complex
number. Take `x = (1, 2)` and `y = (2, 1)`: the ratio is
`4/√5√5 = 0.8`, harmless. Now `x = (1, 10)` and `y = (10, 1)`: the ratio is
`20/√101·√101 = 0.198`. These stay inside by luck. The inequality is what makes
it *always* so, and it is not cosmetic — the ratio can equal 1, and at `1` the
vectors are parallel, which is the equality case the theorem states.

Two further points.

The equality case carries information. `|xᵀy| = ‖x‖‖y‖` holds **iff** `y = cx`,
so Cauchy–Schwarz is simultaneously the existence proof for the angle and the
characterisation of when the angle degenerates to 0° or 180°. The probe list in
the code shows the three regimes: `cos = 0` (orthogonal, `(1,0)` vs `(0,1)`),
`cos = +1` (parallel, `(1,0)` vs `(1,0)`), `cos = −1` (antiparallel, `(1,0)` vs
`(−1,0)`).

And the inequality is what forces the *numerical* guard the code needs.
`max(-1.0, min(1.0, cos))` in the angle function exists because floating-point
rounding can return `1.0000000000000002` for perfectly parallel vectors, and
`math.acos(1.0000000000000002)` returns `nan`. Without Cauchy–Schwarz the
formula has no privileged range at all, so there would be nothing to clamp to.

</details>

**Q2. Why does L1 produce sparse models while L2 does not? Explain the mechanism,
not just the observation.**

<details>
<summary>Model answer</summary>

Both penalties are convex, so both admit a unique minimiser (the residual
squared-error part is strictly convex, so uniqueness is not the issue). The
difference is entirely in the *shape* of the penalty at zero.

L2 penalises `Σcⱼ²`. Its gradient is `2cⱼ`, which is zero **only** at `cⱼ = 0`.
Gradient descent driven by `2cⱼ` therefore approaches zero asymptotically and
reaches it only in the limit. For any finite amount of data or any finite
tolerance, the fitted coefficient is small but nonzero. Ridge regression shrinks
its whole coefficient vector toward zero and stops just short of it.

L1 penalises `Σ|cⱼ|`. At zero it has a corner: `|c|` has left derivative `−1`
and right derivative `+1`, so the subdifferential at `0` is the whole interval
`[−1, 1]`. Optimality for the convex program asks whether `0` belongs to the
subdifferential of the objective at the candidate. At `cⱼ = 0` with
subgradient `s ∈ [−1,1]` that condition is satisfiable whenever the gradient of
the data-fitting term is small enough to be cancelled by some `s` in that
interval. So the optimiser can sit exactly at a whole interval of solutions, and
the coordinates that land there are *exactly* zero.

A second, more intuitive mechanism: the penalty curve. `c²` rises steeply as `|c|`
grows, so the penalty "overshoots" — it can shrink a coefficient to `0.001` and
still charge a lot. `|c|` rises more slowly, so shrinking to `0.001` is cheap. In
a model where one feature is genuinely useless, L1 can make the trade of
`0.001` of coefficient for the risk saved and prefers to go all the way to `0`,
because the last step costs almost nothing. L2 never finds that step worthwhile.

The practical consequences run through everything: `Lasso` at `scikit-learn`
returns a sparse `coef_` with literal zeros, which is why you can prune whole
features and read off which ones mattered; `Ridge` returns a dense vector of
small numbers that is not interpretable. The cost of L1 is that it is not
differentiable at zero, so gradient-descent solvers need subgradient methods,
proximal operators, or coordinate descent — which is why `smooth_l1` exists as a
compromise, and why FISTA and proximal SGD ([82](../part06_algorithms_math/82_tools_for_algorithm_design.md))
are written the way they are.

</details>

**Q3. Why is an orthogonal matrix invertible, and what is its inverse? What would
break this if a column were merely "almost" orthogonal?**

<details>
<summary>Model answer</summary>

Let `Q` be square with orthonormal columns: `QᵀQ = I`. Take transposes: `QᵀQ =
I` implies `(QᵀQ)ᵀ = QᵀQ = I`, and `(QᵀQ)ᵀ = QᵀQᵀᵀ`… writing the product of the
two square matrices as `QQᵀ` by rearranging is the step that needs `Qᵀ` and `Q` to
be the same size, which is guaranteed here since `Q` is square. Both `QᵀQ` and
`QQᵀ` are products of square matrices, and taking the transpose of `QᵀQ = I`
gives `QᵀQ = I`, so `Qᵀ` is a two-sided inverse of `Q`. **The inverse of an
orthogonal matrix is its transpose, and it is orthogonal too:** if `QᵀQ = I` then
`‖Qv‖² = vᵀQᵀQv = vᵀv = ‖v‖²`, so every vector keeps its length, and
`‖Q(x+y)‖² = ‖x+y‖²` gives angles too.

The deeper reason is that orthogonality is the *maximal* possible determinant.
Expanding `det(QᵀQ) = det(I) = 1` as `det(Q)²`, we get `|det(Q)| = 1` — the
largest absolute value any invertible matrix can have. The columns cannot be
collinear (they are orthogonal), so nothing can make the parallelepiped they
span thinner or longer than the unit cube. Invertibility is not luck; it is
forced by the geometry.

Now what "almost" costs. Take `C = [[1, 1], [1.001, 1]]`. Its columns are
`(1, 1.001)` and `(1, 1)` — angle between them is `arctan(0.001/1) ≈ 0.057°`, not
90°. The singular values are `2.0005` and `0.0005`, so
`cond(C) = 2.0005/0.0005 ≈ 4002`. Perturb `x = (1,1)` by `10⁻⁴` in its first
coordinate: `B` returns `(1.00005, 0.00005)` — the answer moved by about half the
input perturbation, `cond = 1` — while `C` returns `(−0.1, 1.1001)`, an answer
that moved by about 1000× the perturbation. `C⁻¹` exists, but it is a noise
amplifier.

Two things break concretely. First, **sign**: `x → −x` can be achieved by the tiny
rotation between the columns, and `C⁻¹` magnifies that rotation enormously. Second,
**the QR and SVD algorithms**, which are designed to be numerically stable
precisely because their factors are orthogonal, lose that guarantee the moment the
factors drift from orthogonality. This is why `np.linalg.qr` returns a `Q` with
`QᵀQ` diagonal to machine precision while `np.linalg.cond` on a naive basis can
be `10⁸` or worse, and why anyone who computes a projection or a least-squares
solution in a non-orthogonal basis should check the condition number first.

</details>

**Q4. Why does the choice of distance function change which model wins, rather
than being a rescaling that leaves the answer the same?**

<details>
<summary>Model answer</summary>

Because the norms are not related by a constant factor. `‖x‖∞ ≤ ‖x‖₂ ≤ ‖x‖₁`
holds pointwise, but the ratio between them is not constant: for `(1, 1, 1)` the
three norms are `1`, `√3 ≈ 1.732`, `3`, ratios `1 : 1.73 : 3`; for `(1, 0, 0)`
they are `1, 1, 1`, ratios `1 : 1 : 1`. A monotone transformation of the target
would not change any ranking — and if the only effect of switching norms were a
rescaling, every nearest-neighbour search and every regularised fit would be
unaffected.

The norm is a *choice of which directions count more*. L∞ is indifferent to
everything except the worst coordinate. L1 adds absolute coordinate magnitudes,
so it is more sensitive to features with large spread. L2 weights by
`xᵢ²`, so a coordinate that is 3× as large counts 9× as much. These are three
genuinely different orderings of "how different are these two points", and each
one matches a different real-world notion.

The lesson's own table shows the disagreement concretely. With target `(1,0)`:

    pt  vector    L2      L1     Linf    angle
    E  (0.3,0.3) 0.7616  1.0    0.7     45.000
    F  (1.9,0.5) 1.0296  1.4    0.9     14.744
    D  (2.0,2.0) 2.2361  3.0    2.0     45.000

L2, L1 and L∞ all rank `E` first; the angle ranks `F` first, and it can never
separate `D` from `E` because they lie on the same ray. So switching from an
absolute metric to an angular one changes the answer from `E` to `F` — that is a
different model, not a reparametrisation.

In machine learning the same point appears as the difference between `MSELoss`
and `MAELoss`, between `metric='minkowski'` and `metric='manhattan'` in
`KNeighborsClassifier`, and between LASSO and ridge. `MSE` and `MAE` have the
same shape argument as L2 and L1: the squared error grows faster on outliers, so
MSE is dominated by them and MAE is not. Whichever one you pick, you have
asserted something about which errors you care about, and the data will answer
differently. Hence the slogan: all of machine learning is a choice of distance
function. It is a modelling decision, and the honest thing to do is to try more
than one and report the difference.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — compute and interpret.** For `x = (1, 2, 2)` and
`y = (3, −1, 0)`:

(a) compute `xᵀy`, `‖x‖₂`, `‖y‖₂`, and the angle between them;
(b) compute the same quantities under L1 and report whether an "angle" exists;
(c) confirm Cauchy–Schwarz numerically;
(d) state whether `x` and `y` are orthogonal.

<details>
<summary>Solution</summary>

**(a)** `xᵀy = 1·3 + 2·(−1) + 2·0 = 3 − 2 + 0 = 1`.
`‖x‖₂ = sqrt(1 + 4 + 4) = sqrt(9) = 3`.
`‖y‖₂ = sqrt(9 + 1 + 0) = sqrt(10) ≈ 3.162278`.
`cos θ = 1 / (3 · 3.162278) = 1 / 9.486833 ≈ 0.105409`.
`θ = arccos(0.105409) ≈ 83.95°`. Nearly a right angle, slightly acute.

**(b)** `‖x‖₁ = 1 + 2 + 2 = 5`, `‖y‖₁ = 3 + 1 + 0 = 4`, distance
`‖x − y‖₁ = |1−3| + |2−(−1)| + |2−0| = 2 + 3 + 2 = 7`.
No angle is defined from L1. The formula `cos θ = ⟨x,y⟩/(‖x‖‖y‖)` needs an
inner product, and L1 gives a norm without a compatible inner product. In `ℝⁿ`
you *can* find a weird inner product that induces the L1 norm, but its
"angle" does not behave geometrically and nobody uses it.

**(c)** `|xᵀy| = 1 ≤ ‖x‖₂‖y‖₂ = 3 · 3.162278 = 9.486833` ✓. The ratio
`0.105409` lies in `[−1, 1]` ✓. Equality is not approached, so `x` and `y` are
not parallel.

**(d)** `xᵀy = 1 ≠ 0`, so they are **not** orthogonal. Consistent with the
83.95° angle from part (a): orthogonal would mean exactly 90°, i.e. `cos θ = 0`.

</details>

**[ ] Exercise 2 — the shape of a sphere changes with the norm.** For
`u = (0.3, 0.4)`, compute `‖u‖₁`, `‖u‖₂`, `‖u‖∞`. Then find all points
`(x, y)` on the unit circle under each norm, by solving `|x| + |y| = 1`,
`x² + y² = 1`, and `max(|x|, |y|) = 1` respectively, and describe the shape
each one traces.

<details>
<summary>Solution</summary>

`‖u‖₁ = 0.3 + 0.4 = 0.7`, `‖u‖₂ = sqrt(0.09 + 0.16) = 0.5`, `‖u‖∞ = 0.4`.
Note the ordering: `0.4 ≤ 0.5 ≤ 0.7`, as the norm inequality requires.

**L1 unit ball**, `|x| + |y| = 1`: a square with vertices at
`(±1, 0)` and `(0, ±1)`. Diagonal edges, side length √2.

**L2 unit ball**, `x² + y² = 1`: the ordinary circle. Every point on it is at
distance 1 from the origin.

**L-infinity unit ball**, `max(|x|, |y|) = 1`: a square with vertices at
`(±1, ±1)`. Axis-aligned edges, side length 2, so it is strictly *larger* than
the L1 square.

Why: `‖x‖∞ ≤ ‖x‖₂ ≤ ‖x‖₁` for every vector, so the set where the norm equals 1
is *larger* under the smaller-norm-in-the-inequality sense. The L-infinity ball
contains the L2 disc, which contains the L1 square. `u` sits just inside the L2
circle (0.5 < 1) but outside the L-infinity square (0.4 < 1 is false — 0.4 < 1 is
true, so `u` is inside it too; note the corner of the Linf ball is at distance
1.414).

Practical consequence: the two squares have different *orientations*. The L1
ball is a diamond aligned to the axes, the L-infinity ball is a box aligned to
the axes. Anisotropy in one, the other diagonal, means the choice of norm can
favour or punish directions like `(1,1)` versus `(1,−1)` — which is precisely
why L1-based models can behave differently on positively versus negatively
correlated features.

</details>

**Challenge — Exercise 3 — nearest neighbour, four ways.** Let the target be
`t = (2, 0)` and the candidates
`A = (2.1, 0.0)`, `B = (2.0, 0.3)`, `C = (1.7, 1.0)`, `D = (3.0, 0.0)`.
Rank all four by L2 distance, by L1 distance, and by angle. Report any ranking
that differs, and say which metric you would use to find the most similar
*image* and which for the closest *physical location*.

<details>
<summary>Solution</summary>

Compute each distance from `t = (2, 0)`, so the difference is `(x − 2, y)`:

| pt | vector | L2 | L1 | angle to (1,0) |
| --- | --- | --- | --- | --- |
| A | (2.1, 0) | 0.1 | 0.1 | 0.000° |
| B | (2.0, 0.3) | 0.3 | 0.3 | 8.531° |
| C | (1.7, 1.0) | 1.0440 | 1.3 | 30.466° |
| D | (3.0, 0) | 1.0 | 1.0 | 0.000° |

Precise values: for C, `L2 = sqrt(0.09 + 1) = sqrt(1.09) ≈ 1.044031`,
`L1 = 0.3 + 1 = 1.3`, `angle = arctan(1/0.3) = arctan(3.3333) ≈ 73.3°` — but
careful: the angle is measured from `t = (2,0)`, i.e. from the positive
x-axis, and `C − t = (−0.3, 1)` points *backwards*, so the angle from `t` to `C`
is `180° − 73.3° = 106.7°`. If instead you compare the *directions* of `C` and
`t` from the origin, `t` is at 0° and `C = (1.7, 1.0)` is at `arctan(1/1.7) ≈
30.47°`. Both framings are defensible; the second (compare the vectors
themselves) is the usual one for "which is most similar to `t`".

**Rankings, comparing vector directions (angle of each point from the origin):**
- L2: A (0.1), B (0.3), D (1.0), C (1.0440)
- L1: A (0.1), B (0.3), D (1.0), C (1.3)
- angle: A (0°), D (0°), B (8.531°), C (30.47°)

**Rankings, comparing displacement directions (angle of `point − t`):**
- L2 and L1 as above
- angle: A and D tie at 0° (both lie along the x-axis from `t`), B at 8.531°,
  C at 106.7°

Either way the interesting disagreement is **D versus C**. Under L2, C
(`1.0440`) is *further* than D (`1.0`), so D wins. Under L1, C (`1.3`) is also
further. But C is at 30.47° while D is at 0° from the origin, so any
angle-based measure puts D ahead too — and note that D and A tie exactly on
angle at 0° while L2 clearly separates them (0.1 against 1.0).

**Choice of metric:**
- *Most similar image*: the **angle** (cosine similarity). A brighter, larger,
  or slightly cropped version of a picture is still the same picture, and its
  direction barely moves. Use `cosine_similarity` or `metric='cosine'`.
- *Closest physical location*: the **L2 distance**. Ten metres away is ten
  metres away, whatever the compass bearing. This is `metric='minkowski'` with
  default `p=2`, which is the scikit-learn default for `KNeighborsClassifier`.

</details>

**[ ] Exercise 4 — the norm inequality, and why switching norms is not a
rescaling.** For each vector `v`, compute `‖v‖₁`, `‖v‖₂`, `‖v‖∞` and the ratios
`‖v‖₁/‖v‖₂` and `‖v‖₂/‖v‖∞`:

(a) `v = (1, 1, 1)`;
(b) `v = (1, 0, 0)`;
(c) `v = (3, 4)`;
(d) `v = (1, 1, 0)`.

Then (e) explain why the fact that the inequality `‖v‖∞ ≤ ‖v‖₂ ≤ ‖v‖₁` holds for
every `v` does **not** mean the three norms are interchangeable.

<details>
<summary>Solution</summary>

| vector | `‖v‖₁` | `‖v‖₂` | `‖v‖∞` | `‖v‖₁/‖v‖₂` | `‖v‖₂/‖v‖∞` |
| --- | --- | --- | --- | --- | --- |
| (1,1,1) | 3 | √3 ≈ 1.732051 | 1 | 1.7321 | 1.7321 |
| (1,0,0) | 1 | 1 | 1 | 1.0000 | 1.0000 |
| (3,4) | 7 | 5 | 4 | 1.4000 | 1.2500 |
| (1,1,0) | 2 | √2 ≈ 1.414214 | 1 | 1.4142 | 1.4142 |

**(e)** The inequality only says one norm is at most the other. It says nothing
about *by how much*, and the ratios above are the answer: they range from 1.0000
for `(1,0,0)` to 1.7321 for `(1,1,1)`.

If the norms differed by a constant factor, `‖x‖₁ = c‖x‖₂` for all `x`, then any
minimisation of `‖x − y‖₁` over a candidate set would have exactly the same
argmin as minimising `c‖x − y‖₂`, and `k`-NN would be invariant under the choice.
Because the ratio is not constant, that invariance fails: the norms induce
genuinely different orderings of the candidate set.

The vector `(1,0,0)` is the degenerate case worth naming — all three agree because
a single nonzero coordinate is simultaneously the total, the Euclidean and the
largest. Vectors with more spread get increasing disagreement, and `(1,1,1)` is
already 73% worse under L1 than under L∞.

Proof sketch of the inequality for `n = 3`: `‖v‖∞ ≤ ‖v‖₂` because
`max vᵢ² ≤ Σvᵢ²`. And `‖v‖₂ ≤ ‖v‖₁` because `Σvᵢ² ≤ (Σ|vᵢ|)²`, since squaring a
sum of nonnegatives expands to include all the cross terms `2|vᵢvⱼ| ≥ 0`.

</details>

**[ ] Exercise 5 — a weighted inner product.** Let `W = diag(4, 1)` and define
`⟨x, y⟩_W = xᵀWy`.

(a) Compute `⟨u,u⟩_W`, `⟨v,v⟩_W`, and `⟨u,v⟩_W` for `u = (2, 1)` and
`v = (1, 2)`.
(b) Compute the angle between `u` and `v` under this inner product and compare
it with the unweighted angle.
(c) Find all `z` with `⟨u, z⟩_W = 0`, i.e. the vectors orthogonal to `u` in this
geometry, and check that they are a different set from the unweighted ones.
(d) Explain why a *negative* entry on the diagonal of `W` would make
`⟨x,x⟩_W` a bad thing to call a squared length.

<details>
<summary>Solution</summary>

**(a)** With `W = diag(4,1)`, `⟨x,y⟩_W = 4x₁y₁ + x₂y₂`.

`⟨u,u⟩_W = 4·4 + 1·1 = 17`
`⟨v,v⟩_W = 4·1 + 1·4 = 8`
`⟨u,v⟩_W = 4·2·1 + 1·1·2 = 10`

Sanity check: `⟨x,x⟩_W = 4x₁² + x₂² ≥ 0`, with equality only when `x = 0`. Positive
definiteness holds, so this really is an inner product.

**(b)** `cos θ_W = ⟨u,v⟩_W / (‖u‖_W‖v‖_W) = 10 / (√17 · √8) = 10/11.6619 =
0.857493`, so `θ_W = arccos(0.857493) = 30.964°`.

Unweighted: `uᵀv = 2 + 2 = 4`, `‖u‖ = √5`, `‖v‖ = √8`, so `cos θ = 4/√40 =
0.632456`, giving `θ = 50.769°`. The weighted angle is *smaller* — the geometry
says `u` and `v` are more alike than the plain dot product suggests, because the
coordinate they differ most on is the one the metric discounts.

**(c)** `⟨u,z⟩_W = 8z₁ + z₂ = 0`, so `z₂ = −8z₁`: the orthogonal complement is
the whole family `(s, −8s)` for `s ∈ ℝ`, spanned by `z = (1, −8)`.

Unweighted, `uᵀz = 0` means `2z₁ + z₂ = 0`, i.e. `z₂ = −2z₁`, spanned by
`(1, −2)`. **Different sets.** Concretely, `(1, −2)` satisfies the unweighted
condition but `⟨u,(1,−2)⟩_W = 8 − 2 = 6 ≠ 0`.

That is the whole content of "changing the inner product changes the geometry":
orthogonality is defined *relative to* the inner product, not intrinsic to the
coordinates. This is why [38](38_orthogonality_and_least_squares.md) has to say
"orthonormal with respect to the standard inner product" rather than just
"orthonormal".

**(d)** Take `W = diag(1, −1)`. Then `⟨x,x⟩_W = x₁² − x₂²`, and for `x = (1, 1)`
this is `0` despite `x ≠ 0`. Worse, for `x = (3, 4)` it is `9 − 16 = −7`, a
*negative* "squared length".

Two axioms break at once. **Positivity** fails, so `‖x‖ = √(⟨x,x⟩_W)` is not
even real for some `x` — you cannot take the square root of `−7`. And
**homogeneity** fails with it: Cauchy–Schwarz states
`|⟨x,y⟩| ≤ √(⟨x,x⟩)√(⟨y,y⟩)`, but with `⟨x,x⟩ = −7` and `⟨y,y⟩ = −7` the right
side is `7` while `|⟨x,y⟩|` can exceed it, so the "angle" leaves `[−1, 1]` and
`arccos` breaks. A zero weight is also illegal: it makes every vector on the
corresponding axis have length 0, which is the degenerate case the lesson's
definition rules out. Positive definiteness is exactly the clause that forbids
this.

</details>

**Challenge — Exercise 6 — projection onto a line, and why the leftover is
perpendicular.** (a) Let `t = (3, 0)` and let `p = (1, 1)` be a direction. By
hand, minimise `‖t − c·p‖₂` over all scalars `c`: compute the function, take its
derivative, solve, and evaluate. (b) Verify that the leftover `t − c*·p` is
perpendicular to `p`. (c) Now find the point on the line `y = 2x + 1` closest to
the point `(5, 1)`, and check the connecting segment is perpendicular to the line.
(d) Explain why the leftover is the *smallest possible* error, not just a small
one — what would go wrong if you chose a different `c`?

<details>
<summary>Solution</summary>

**(a)** The error function is

    f(c) = ‖(3,0) − c(1,1)‖₂ = √((3−c)² + c²)

Minimising `f` is the same as minimising `f²`, which is smoother:

    f(c)² = (3−c)² + c² = 9 − 6c + c² + c² = 2c² − 6c + 9

Differentiate: `d/dc (2c² − 6c + 9) = 4c − 6`. Setting it to zero gives `c = 1.5`,
and the second derivative is `4 > 0`, so this is a minimum.

At `c = 1.5`: `proj = 1.5·(1,1) = (1.5, 1.5)`, leftover `t − proj = (1.5, −1.5)`,
error `‖(1.5, −1.5)‖₂ = √(2.25 + 2.25) = √4.5 ≈ 2.121320`.

This matches the lesson's projection block exactly, which prints
`projection = [1.5, 1.5]`, `leftover = [1.5, -1.5]`.

**(b)** `(1.5, −1.5)·(1,1) = 1.5 − 1.5 = 0`. The leftover is orthogonal to `p`,
by construction. The general reason: if `proj = c*p` then
`pᵀ(t − c*p) = pᵀt − c·(pᵀp) = 0` exactly when `c = (pᵀt)/(pᵀp)`, which is the
value the minimisation produced.

**(c)** Write the line as `base + s·d` with `base = (0, 1)` and `d = (1, 2)`. We
minimise `‖(5,1) − base − s·d‖₂²`, i.e.

    g(s) = (5 − s)² + (1 − 1 − 2s)² = (5 − s)² + 4s²

    g'(s) = −2(5 − s) + 8s = −10 + 2s + 8s = 10s − 10 = 0  ⟹  s = 1

So the closest point is `base + 1·d = (1, 3)`, and the distance is
`‖(5,1) − (1,3)‖₂ = √(16 + 4) = √20 ≈ 4.472136`.

Perpendicularity check: the connecting segment is `(5,1) − (1,3) = (4, −2)`, and
`(4, −2)·(1, 2) = 4 − 4 = 0` ✓. The segment meets the line at a right angle,
which is the elementary geometric statement of "shortest distance to a line".

**(d)** Any other choice `c ≠ 1.5` makes the error *larger*, and the reason is
already in the algebra. Write `t = c*p + r` where `r` is the leftover. For any
other scalar `ĉ`,

    ‖t − ĉ p‖₂² = ‖c p + r − ĉ p‖₂² = ‖(c − ĉ)p + r‖₂²
                = (c − ĉ)²‖p‖₂² + ‖r‖₂² + 2(c − ĉ) pᵀ r
                = (c − ĉ)²‖p‖₂² + ‖r‖₂²        (since pᵀ r = 0)

So the error at any other `ĉ` equals the minimum plus a strictly positive term
`(c − ĉ)²‖p‖₂²`, which vanishes **only** at `ĉ = c`. The minimum is unique and
the leftover's perpendicularity is exactly what makes the minimum that good. This
one identity is the whole of least squares: decompose the target into a part
inside the span and an orthogonal leftover, and the leftover is the error you
cannot remove.

Two practical corollaries worth stating, because they are what
[38](38_orthogonality_and_least_squares.md) turns into algorithms. First,
`‖p‖₂²` must be positive, which is another way of saying `p ≠ 0`: a zero direction
means the line is a single point and the whole construction divides by zero.
Second, once the basis is orthogonal, minimising `‖Ax − b‖₂` separates
coordinate-wise with no cross terms at all — that is why the normal equations
`AᵀAx = Aᵀb` are cheap in an orthonormal basis and messy otherwise.

</details>

## Summary

- An **inner product** turns a bare vector space into a geometry: the dot
  product on `ℝⁿ` is the standard one.
- A **norm** is the length: `‖x‖ = sqrt(xᵀx)` for L2, with L1 and L-infinity as
  the other two you will meet constantly.
- **Cauchy–Schwarz** guarantees `|xᵀy| ≤ ‖x‖‖y‖`, which is the only reason the
  angle and `arccos` are well defined.
- **Cosine similarity** normalises by both lengths, so it measures direction
  only and is scale-invariant — the default for text and images.
- **Orthogonal** means `xᵀy = 0`, i.e. a 90° angle. Orthogonal ⇒ independent, but
  never the reverse.
- Orthogonality gives **Pythagoras for vectors**: `‖x+y‖² = ‖x‖² + ‖y‖²`, with
  the cross terms vanishing. This one fact powers least squares and PCA.
- The norm inequality `‖x‖∞ ≤ ‖x‖₂ ≤ ‖x‖₁` always holds, so the three "unit
  balls" are different shapes: box, disc, diamond.
- **The choice of norm is a modelling decision**: L1 penalises large
  coefficients harder and yields sparsity, L2 shrinks smoothly, and angles
  ignore scale entirely.

## Next

[38 — Orthogonality and Least Squares](38_orthogonality_and_least_squares.md)
turns projection into an algorithm. This lesson showed that the leftover after
projecting is orthogonal to what you projected onto; the next one builds
orthogonal bases deliberately with Gram-Schmidt, introduces the orthogonal
matrix, and derives linear regression as pure geometry — arriving at the normal
equations without ever differentiating a loss.
