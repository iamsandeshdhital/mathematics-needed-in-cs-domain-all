# 50 — Functions, Limits, and Continuity

**Part**: part04_calculus · **Prerequisites**: 41 · **Time**: 30 min

---

## In Plain Words

A function is a machine that takes one input and gives back exactly one output. The
set of inputs it accepts is its *domain*, and the set of outputs it promises is its
*codomain*. When you feed one machine into another you are doing *composition*, and
composition is literally what every line of code that calls a function is doing. A
function has an *inverse* only when no two different inputs produce the same output;
when that fails, two different things look identical after processing, which is exactly
the collision problem a hash table has to solve.

A *limit* answers a question your code constantly asks: as the input gets closer and
closer to some point, what does the output do? The answer can be perfectly sensible even
when the function crashes at that exact point — dividing by something that is heading
towards zero, or dividing by something heading towards zero.

A function is *continuous* at a point when its value there equals the limit approaching
that point, meaning there is no hole and no jump. Continuity matters because a huge
number of standard algorithms — bisection search, Newton's method, gradient descent —
have a correctness proof that assumes the function has no holes.

---

## Why Computer Science Cares

- **Finite differences are limits you cannot take.** To measure the slope of a curve in
  code you compute `(f(x+h) - f(x)) / h` and try smaller and smaller `h`. Every
  numerical derivative is an attempt at `h → 0`, and it fails in both directions: `h`
  too large gives a bad approximation, `h` too small gives floating-point garbage.
  Lesson [51](51_derivatives.md) is entirely about this.
- **Big-O is a limit at infinity.** Saying `n = O(n log n)` literally means
  `lim_{n→∞} n/(n log n) = 0`. Every statement about asymptotic cost in
  [Part 06](../part06_algorithms_math/80_big_o_and_complexity.md) is a limit claim.
- **Iterative solvers need convergence.** `math.sqrt`, Newton-Raphson, k-means Lloyd's
  algorithm, power iteration for eigenvalues, and `while` loops in general all ask:
  does this sequence of values settle down, and where?
- **`0.0 / 0.0` has no answer, but `1.0 / 0.0` does.** IEEE-754 floating point decides
  these by taking one-sided limits, which is why one returns `nan` and the other returns
  `inf`. Understanding *why* avoids a class of confusing bugs.
- **Robust numerical libraries check continuity for you.** `scipy.optimize.brentq`
  documents that it "requires a continuous function"; `torch.autograd` rejects
  non-differentiable points; `scipy.integrate.quad` warns about discontinuities because
  its adaptive error estimate breaks on them.

---

## The Formal Version

Symbols follow [SYMBOLS.md](../../SYMBOLS.md).

**Definition.** A *function* from a set $X$ to a set $Y$ is a relation that assigns to
every $x \in X$ exactly one element $f(x) \in Y$. We write $f : X \to Y$. The set $X$ is
the **domain**, $Y$ is the **codomain**, and $\mathrm{im}(f) = \{f(x) : x \in X\} \subseteq Y$
is the **image** (what actually comes out).

*Explanation.* A function is total on its domain: no input may be skipped, and no input
may produce two outputs. That is the entire content of the definition.

**Definition.** The *composition* of $f : X \to Y$ and $g : Y \to Z$ is the function
$(f \circ g) : X \to Z$ given by $(f \circ g)(x) = f(g(x))$.

*Explanation.* Run $g$ first, then feed its answer to $f$. In code:
`f(g(x))`.

**Definition.** $f$ is *injective* (one-to-one) if $f(a) = f(b) \Rightarrow a = b$. It is
*surjective* (onto) if $\mathrm{im}(f) = Y$. It is *bijective* if both hold.

**Definition.** $f : X \to Y$ is *invertible* if there is a function
$f^{-1} : \mathrm{im}(f) \to X$ with $f^{-1}(f(x)) = x$ and $f(f^{-1}(y)) = y$.

**Theorem.** A function has an inverse exactly when it is injective; the inverse's domain
is the image, not necessarily the codomain.

**Definition.** Let $f : \mathbb{R} \to \mathbb{R}$ and let $a$ be a *limit point* of the
domain. We write

$$\lim_{x \to a} f(x) = L$$

if for every $\varepsilon > 0$ there is a $\delta > 0$ such that for all $x$ in the domain,

$$0 < |x - a| < \delta \quad \Longrightarrow \quad |f(x) - L| < \varepsilon.$$

*Explanation.* Read it as: "no matter how tight a target tolerance $\varepsilon$ you
pick, I can choose a neighbourhood of size $\delta$ so that every point inside it lands
inside the target." Crucially, $x$ never equals $a$: the function does not have to be
defined at $a$, or even defined anywhere near it.

**Theorem (Limit laws).** If $\lim_{x\to a} f(x) = L$ and $\lim_{x \to a} g(x) = M$ then

$$\lim_{x\to a}\big(f(x) + g(x)\big) = L + M, \qquad \lim_{x\to a} f(x)g(x) = LM, \qquad \lim_{x\to a} \frac{f(x)}{g(x)} = \frac{L}{M} \ \ (M \neq 0).$$

The limit laws let you compute almost everything from a handful of known limits such as
$\lim_{x\to 0}\sin x / x = 1$ and $\lim_{x \to 0}(1-\cos x)/x^2 = 1/2$.

**Definition.** $f$ is *continuous at* $a$ if $a$ is in the domain of $f$ and

$$\lim_{x \to a} f(x) = f(a).$$

$f$ is continuous on a set if it is continuous at every point of it.

*Explanation.* The value the function takes at $a$ is exactly the value it was heading
towards. No surprise at the point itself.

**Theorem.** If $f$ is continuous at $a$ and $g$ is continuous at $f(a)$, then
$f \circ g$ is continuous at $a$.

**Theorem (Intermediate Value Theorem).** If $f$ is continuous on $[a, b]$ and
$f(a) < 0 < f(b)$, then there is a $c \in (a, b)$ with $f(c) = 0$.

*Explanation.* This is the theorem that makes bisection search correct. It fails without
continuity — see the worked example, and the code below where bisection happily returns a
point that is not a root.

**Definition.** $f$ is *continuous on a compact interval* if it is continuous at every
point of $[a,b]$. Then it attains a maximum and a minimum there (Extreme Value Theorem).

*Explanation.* No matter how wild the interior is, on a closed bounded interval a
continuous function has a best point and a worst point. Machine learning gradient
descent on a continuous loss over a closed domain is arguing inside this theorem.

**Definition (Limit of a sequence).** The sequence $(x_n)$ *converges to* $L$ if for every
$\varepsilon > 0$ there is $N$ such that $n \ge N \Rightarrow |x_n - L| < \varepsilon$.
We write $\lim_{n \to \infty} x_n = L$.

*Explanation.* Same epsilon-delta game, with "distance in space" replaced by "how many
steps", and `$|x-a| < \delta$" replaced by "`$n$ is large enough". Iterative algorithms
are the source of sequences; [Part 05](../part05_probability_statistics/) is where the
probabilistic version shows up.

---

## Worked Example

### Example 1: A function, composed, and inverted

Let $g(x) = 2x$ and $f(x) = 3x + 7$, both on $\mathbb{R}$.

1. **Compute the composition.** By definition $(f \circ g)(x) = f(g(x)) = 3(2x) + 7 = 6x + 7$.
   Check at $x = 5$: $g(5) = 10$, then $f(10) = 37$. The formula gives $6(5) + 7 = 37$.
2. **Is $f$ invertible?** Solve $y = 3x + 7$ for $x$: $x = (y - 7)/3$. That is
   $f^{-1}(y) = (y-7)/3$.
3. **Verify.** $f(f^{-1}(100)) = f(31) = 3(31) + 7 = 100$. And
   $f^{-1}(f(100)) = f^{-1}(307) = (307-7)/3 = 100$. Both compositions are the identity.
4. **Why the algebra matters.** Solving for $x$ is what you are doing when you write
   `x = (y - b) / a` to undo a linear layer in a neural network, or when you rearrange
   an equation in a solver.

### Example 2: A limit that exists although the function does not

Let $f(x) = \dfrac{x^2 - 1}{x - 1}$.

1. **At $x = 1$ the function is undefined**: $0/0$. No value exists.
2. **Look nearby.** For $x \ne 1$, factor the numerator: $x^2 - 1 = (x-1)(x+1)$, so
   $f(x) = x + 1$ for every $x \ne 1$.
3. **So the limit as $x \to 1$ is $1 + 1 = 2$.** Numerically, walking towards 1:

   | $x$ | $f(x)$ |
   | --- | --- |
   | 0.9 | 1.900000 |
   | 0.99 | 1.990000 |
   | 0.999 | 1.999000 |
   | 1.001 | 2.001000 |
   | 1.01 | 2.010000 |

4. **Prove it with epsilon-delta.** We need: for all $\varepsilon > 0$, there is
   $\delta > 0$ such that $0 < |x - 1| < \delta \Rightarrow |f(x) - 2| < \varepsilon$.
   Substituting the simplified form: $f(x) - 2 = (x+1) - 2 = x - 1$. So
   $|f(x) - 2| = |x - 1| < \delta$. Choosing $\delta = \varepsilon$ closes the argument
   for every $\varepsilon$, which is what a proof needs.
5. **Conclusion.** $f$ has a *removable discontinuity* at $x = 1$: a single wrong value,
   or a missing one, in an otherwise continuous function. This is exactly the shape of the
   classic bug `0/0` — a signal that you should cancel algebraically rather than
   numerically.

### Example 3: Continuity as a hypothesis, not a nicety

Consider

$$h(t) = \begin{cases} -1 & t < 0 \\ 1 & t \ge 0\end{cases}$$

1. $h(-\varepsilon) = -1 < 0$ and $h(+\varepsilon) = 1 > 0$ for every $\varepsilon > 0$.
   So the two endpoint signs differ and bisection would happily begin halving the
   interval.
2. But $h$ jumps over zero. There is **no** $t$ with $h(t) = 0$. The Intermediate Value
   Theorem does not apply because $h$ is not continuous.
3. The code below runs bisection on exactly this function. It returns
   `-9.094947017729282e-13`, and `h` of that number is `-1.0`. A confident-looking answer
   that is entirely wrong.

The lesson: a numerical method's guarantee is always conditional on the mathematical
hypotheses being satisfied. Bisection needs continuity; Newton's method needs
differentiability; gradient descent needs bounded curvature. When a method misbehaves in
practice, check the hypotheses before rewriting the method.

### Example 4: A limit at infinity is exactly Big-O

Let $f(n) = n$ and $g(n) = n \ln n$.

1. The claim "$f \in O(g)$" means: there exist $c > 0$ and $n_0$ with
   $f(n) \le c \cdot g(n)$ for all $n \ge n_0$.
2. Ratio form: $f(n)/g(n) = 1/\ln n$. The ratio is $0.434$ at $n = 10$, $0.217$ at
   $n = 100$, $0.145$ at $n = 1000$, $0.0724$ at $n = 10^6$, and $0.0483$ at
   $n = 10^9$.
3. It shrinks without bound, so $c = 1$ works for every $n \ge 10$. Hence
   $n = O(n \log n)$.
4. This is why in practice "sorting is $O(n \log n)$" and "scanning is $O(n)$" can be
   compared at all: one grows slower relative to the other, so on large inputs the ratio
   of their runtimes has a limit.

---

## Runnable Code

### Block 1: functions, composition, inverses, and collisions

```python
import math

print("=== 1. A function is a machine: inputs in, exactly one output out ===")
print()


def affine(x):
    """f: R -> R,  f(x) = 3x + 7."""
    return 3 * x + 7


print("f(x) = 3x + 7")
for x in (-2, 0, 1, 2.5):
    print(f"  f({x:>4}) = {affine(x):>6}")

print()
print("=== 2. Composition: the output of one machine is the input of another ===")


def double(x):
    """g: R -> R,  g(x) = 2x."""
    return 2 * x


print("g(x) = 2x, f(x) = 3x + 7")
print(f"  g then f applied to 5 : {double(5)} -> {affine(double(5))}")
print(f"  algebra: 3(2*5) + 7    = {3 * (2 * 5) + 7}")

print()
print("=== 3. Inverses: a function that undoes another one ===")


def affine_inverse(y):
    """f^-1: R -> R,  y -> (y - 7)/3.  Undoes affine."""
    return (y - 7) / 3


print(f"  affine(affine_inverse(100)) = {affine(affine_inverse(100)):.12f}")
print(f"  affine_inverse(affine(100)) = {affine_inverse(affine(100)):.12f}")

print()
print("=== 4. Why not every function has an inverse: collisions ===")


def polynomial_cube(x):
    """g: R -> R, g(x) = x^3 - 3x.  Not one-to-one, so no inverse on all of R."""
    return x ** 3 - 3 * x


for a, b in ((-2.0, 1.0), (-1.0, 2.0)):
    print(f"  g({a:>4}) = {polynomial_cube(a):>6}   g({b:>4}) = {polynomial_cube(b):>6}"
          f"   equal? {polynomial_cube(a) == polynomial_cube(b)}")

print()
print("  A hash table hits the same wall, and solves it the same way:")
buckets = {}
for word in ("apple", "apricot", "axe", "bat", "bee"):
    buckets.setdefault(len(word), []).append(word)   # terrible "hash": string length
for size, words in sorted(buckets.items()):
    print(f"    bucket {size}: {words}")
print("  Two words in one slot = a collision; Python resolves it with a chain.")
```

Output:

```text
=== 1. A function is a machine: inputs in, exactly one output out ===

f(x) = 3x + 7
  f(  -2) =      1
  f(   0) =      7
  f(   1) =     10
  f( 2.5) =   14.5

=== 2. Composition: the output of one machine is the input of another ===
g(x) = 2x, f(x) = 3x + 7
  g then f applied to 5 : 10 -> 37
  algebra: 3(2*5) + 7    = 37

=== 3. Inverses: a function that undoes another one ===
  affine(affine_inverse(100)) = 100.000000000000
  affine_inverse(affine(100)) = 100.000000000000

=== 4. Why not every function has an inverse: collisions ===
  g(-2.0) =   -2.0   g( 1.0) =   -2.0   equal? True
  g(-1.0) =    2.0   g( 2.0) =    2.0   equal? True

  A hash table hits the same wall, and solves it the same way:
    bucket 3: ['axe', 'bat', 'bee']
    bucket 5: ['apple']
    bucket 7: ['apricot']
  Two words in one slot = a collision; Python resolves it with a chain.
```

### Block 2: what a limit is, and epsilon-delta checked exactly

```python
import math
from fractions import Fraction

print("=== Epsilon-delta, checked exactly with rational arithmetic ===")
#  Claim:  lim_{x -> 1} (x^2 - 1)/(x - 1) = 2.
#  Definition: for every eps > 0 there is delta > 0 such that
#      0 < |x - 1| < delta  ==>  |f(x) - 2| < eps.
#  Exactly: f(x) - 2 = (x^2 - 1)/(x - 1) - 2 = (x - 1), so delta = eps suffices.


def f(frac_x):
    """f(x) = (x^2 - 1)/(x - 1) in exact rational arithmetic -- no rounding."""
    return (frac_x * frac_x - 1) / (frac_x - 1)


LIM = Fraction(2)
print("   eps         delta chosen      worst |f(x)-2|    holds?")
for exp in (1, 3, 6, 10):
    eps = Fraction(1, 10 ** exp)
    delta = eps
    # Worst case allowed by delta: x just inside 1 + delta.
    x = Fraction(1) + delta * Fraction(10 ** 12 - 1, 10 ** 12)
    worst = abs(f(x) - LIM)
    print(f"   1e-{exp:<9} {str(delta):<18} {float(worst):<19.3e} {worst < eps}")
print("  Exact arithmetic makes the identity |f(x) - 2| = |x - 1| airtight.")
print("  In floating point the same test can fail; see lesson 54 on cancellation.")
print()

print("=== Code reality: value at a point != limit at that point ===")
try:
    (1.0 ** 2 - 1) / (1.0 - 1)
except ZeroDivisionError as err:
    print(f"  f(1.0) -> ZeroDivisionError: {err}")
print("  but lim_{x->1} f(x) = 2, which is what the algebra says.")
print()

print("=== Limits in code: convergence of an iterative method ===")
# Newton's method for sqrt(2): repeatedly compose x -> (x + 2/x)/2.
def babylonian(x, steps=0):
    for _ in range(steps):
        x = (x + 2 / x) / 2
    return x


x = 1.0
print("   k   x_k (15 dp)               change")
for k in range(1, 7):
    prev = x
    x = babylonian(prev, 1)
    print(f"   {k}   {x:.15f}    {abs(x - prev):.3e}")
print(f"  exact sqrt(2) = {math.sqrt(2):.15f}")
print("  Monotone after k=1 and bounded above by sqrt(2): it converges.")
print()

print("=== Limits in code: Big-O IS a limit at infinity ===")
print("  f(n) = n, g(n) = n ln n.  Claim n = O(n ln n) means f/g -> 0.")
for n in (10, 100, 1000, 1_000_000, 1_000_000_000):
    print(f"    n = {n:>13}   f/g = {1 / math.log(n):.6f}")
print("  The ratio falls without bound. Part 06 turns this into formal notation.")
print()

print("=== Limits in code: sin(x)/x -> 1, and why we never evaluate it at 0 ===")
print("   x             sin(x)/x           error from 1")
for x in (1.0, 0.1, 1e-2, 1e-4, 1e-8, 1e-16):
    val = math.sin(x) / x
    print(f"   {x:<12.1e} {val:.17f}   {abs(val - 1):.2e}")
print("  The limit is 1. At x = 1e-16 the quotient is exactly 1.0 --")
print("  floating point has run out of resolution, not the maths.")
```

Output:

```text
=== Epsilon-delta, checked exactly with rational arithmetic ===
   eps         delta chosen      worst |f(x)-2|    holds?
   1e-1         1/10               1.000e-01           True
   1e-3         1/1000             1.000e-03           True
   1e-6         1/1000000          1.000e-06           True
   1e-10        1/10000000000      1.000e-10           True
  Exact arithmetic makes the identity |f(x) - 2| = |x - 1| airtight.
  In floating point the same test can fail; see lesson 54 on cancellation.

=== Code reality: value at a point != limit at that point ===
  f(1.0) -> ZeroDivisionError: float division by zero
  but lim_{x->1} f(x) = 2, which is what the algebra says.

=== Limits in code: convergence of an iterative method ===
   k   x_k (15 dp)               change
   1   1.500000000000000    5.000e-01
   2   1.416666666666667    8.333e-02
   3   1.414215686274510    2.451e-03
   4   1.414213562374690    2.124e-06
   5   1.414213562373095    1.595e-12
   6   1.414213562373095    0.000e+00
  exact sqrt(2) = 1.414213562373095
  Monotone after k=1 and bounded above by sqrt(2): it converges.

=== Limits in code: Big-O IS a limit at infinity ===
  f(n) = n, g(n) = n ln n.  Claim n = O(n ln n) means f/g -> 0.
    n =            10   f/g = 0.434294
    n =           100   f/g = 0.217147
    n =          1000   f/g = 0.144765
    n =       1000000   f/g = 0.072382
    n =    1000000000   f/g = 0.048255
  The ratio falls without bound. Part 06 turns this into formal notation.

=== Limits in code: sin(x)/x -> 1, and why we never evaluate it at 0 ===
   x             sin(x)/x           error from 1
   1.0e+00      0.84147098480789650   1.59e-01
   1.0e-01      0.99833416646828155   1.67e-03
   1.0e-02      0.99998333341666645   1.67e-05
   1.0e-04      0.99999999833333342   1.67e-09
   1.0e-08      1.00000000000000000   0.00e+00
   1.0e-16      1.00000000000000000   0.00e+00
  The limit is 1. At x = 1e-16 the quotient is exactly 1.0 --
  floating point has run out of resolution, not the maths.
```

### Block 3: continuity, and why bisection depends on it

```python
import math

print("=== Continuity test: no jump in the limit across a point ===")
#  f is continuous at a  <=>  lim_{x->a} f(x) = f(a).
#  Numerical proxy: the values approaching from both sides must match f(a).


def probe(f, a, h=1e-9):
    """Return (f(a-h), f(a), f(a+h)).  For continuous f these all agree."""
    return f(a - h), f(a), f(a + h)


def step(x):
    """A jump: 0 below 0.5, 1 at or above.  Discontinuous at 0.5."""
    return 0.0 if x < 0.5 else 1.0


def abs_but_five_at_zero(x):
    """|x| everywhere except f(0) = 5.  Limit at 0 is 0, value is 5."""
    return 5.0 if x == 0 else abs(x)


print("  f(x) = sin(x) at a = pi/2 (continuous)")
L, V, R = probe(math.sin, math.pi / 2)
print(f"    f(a-h) = {L:.9f}  f(a) = {V:.9f}  f(a+h) = {R:.9f}   gap = {abs(L - R):.1e}")
print()

print("  f(x) = step at a = 0.5 (jump discontinuity)")
L, V, R = probe(step, 0.5)
print(f"    f(a-h) = {L}  f(a) = {V}  f(a+h) = {R}   gap = {abs(L - R)}")
print()

print("  f(x) = |x| except f(0) = 5 (removable discontinuity)")
L, V, R = probe(abs_but_five_at_zero, 0.0)
print(f"    f(a-h) = {L:.1e}  f(a) = {V}  f(a+h) = {R:.1e}")
print("    both sides tend to 0, so lim f = 0 but f(0) = 5 -- the limit exists, the function is not continuous")
print()

print("=== Continuity is what makes bisection safe ===")
#  Bisection needs opposite signs at the two ends.  That implies a root only
#  if f is continuous on the bracket.


def bisect(f, lo, hi, tol=1e-12, max_iter=200):
    """Classic bisection.  Its correctness proof assumes continuity."""
    flo = f(lo)
    if (flo < 0) == (f(hi) < 0):
        raise ValueError("no sign change on the bracket")
    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        fmid = f(mid)
        if fmid == 0.0 or 0.5 * (hi - lo) < tol:
            return mid
        if (fmid < 0) == (flo < 0):
            lo, flo = mid, fmid
        else:
            hi = mid
    return 0.5 * (lo + hi)


root = bisect(lambda t: t * t - 2, 0.0, 2.0)
print(f"  bisect(x^2 - 2 on [0, 2]) = {root:.15f}")
print(f"  math.sqrt(2)              = {math.sqrt(2):.15f}")
print(f"  agree to {abs(root - math.sqrt(2)):.1e}")

# Sign change, but NO root: f jumps straight over zero.
hopping = lambda t: -1.0 if t < 0 else 1.0
print(f"\n  hopping jump at 0: f(-0.001) = {hopping(-0.001)}, f(0.001) = {hopping(0.001)}")
print("  signs differ, so the 'keep the half with a sign change' step would proceed,")
try:
    bad = bisect(hopping, -1.0, 1.0)
    print(f"  and bisect would report {bad} -- which is NOT a root (f(bad) = {hopping(bad)})")
except ValueError as err:
    print(f"  bisect refuses: {err}")
print("  Continuity is the hypothesis that makes bisection correct, not a detail.")
```

Output:

```text
=== Continuity test: no jump in the limit across a point ===
  f(x) = sin(x) at a = pi/2 (continuous)
    f(a-h) = 1.000000000  f(a) = 1.000000000  f(a+h) = 1.000000000   gap = 0.0e+00

  f(x) = step at a = 0.5 (jump discontinuity)
    f(a-h) = 0.0  f(a) = 1.0  f(a+h) = 1.0   gap = 1.0

  f(x) = |x| except f(0) = 5 (removable discontinuity)
    f(a-h) = 1.0e-09  f(a) = 5.0  f(a+h) = 1.0e-09
    both sides tend to 0, so lim f = 0 but f(0) = 5 -- the limit exists, the function is not continuous

=== Continuity is what makes bisection safe ===
  bisect(x^2 - 2 on [0, 2]) = 1.414213562372424
  math.sqrt(2)              = 1.414213562373095
  agree to 6.7e-13

  hopping jump at 0: f(-0.001) = -1.0, f(0.001) = 1.0
  signs differ, so the 'keep the half with a sign change' step would proceed,
  and bisect would report -9.094947017729282e-13 -- which is NOT a root (f(bad) = -1.0)
  Continuity is the hypothesis that makes bisection correct, not a detail.
```

---

### With Libraries

The three pictures below are worth more than the tables. A discontinuity that a table of
values hides completely is obvious the moment you plot it.

```python
# Requires numpy + matplotlib; not runnable with the standard library alone.
import matplotlib
matplotlib.use("Agg")          # so the script runs without a display
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3.2, 3.2, 4000)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# 1. sin(x)/x: a removable hole at 0.
axes[0].plot(x, np.sinc(x / np.pi), linewidth=2)
axes[0].plot(0, 0, "o", color="red", markersize=8)          # the limit value
axes[0].set_title("sin(x)/x: limit 1 at 0, no value")
axes[0].set_ylim(-0.4, 1.4)

# 2. The same rational function: undefined at 1, limit 2.
axes[1].plot(x, (x ** 2 - 1) / (x - 1), linewidth=2)
axes[1].plot([1], [2], "o", color="red", markersize=8)
axes[1].set_title("(x^2-1)/(x-1): hole at x=1, limit 2")

# 3. A step function: discontinuous at every nearby point.
axes[2].step(x, (x > 0.5).astype(float), where="post", linewidth=2)
axes[2].set_title("step: discontinuous at every nearby point")

for ax in axes:
    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("lesson50_continuity.png", dpi=110)
print("wrote lesson50_continuity.png")

# How close does the hole look?  Sample just to the right of 1 and watch 2 approach.
print("   x                 (x^2-1)/(x-1)")
for extra in (1.0, 0.1, 0.01, 1e-3, 1e-6, 1e-9):
    xval = 1.0 + extra
    print(f"   {xval:<18.12f} {(xval ** 2 - 1) / (xval - 1):.12f}")
plt.close(fig)
```

```text
wrote lesson50_continuity.png
   x                 (x^2-1)/(x-1)
   2.000000000000     3.000000000000
   1.100000000000     2.100000000000
   1.010000000000     2.010000000000
   1.001000000000     2.001000000000
   1.000001000000     2.000001000089
   1.000000001000     2.000000000000
```

The last line is instructive. At `x = 1 + 1e-9` the computed value is *exactly* 2.0 —
not because the function is defined there, but because `(x**2 - 1)` and `(x - 1)` round
to the same double and the quotient lands on 2.0. The machine has accidentally produced
the limit. Do not rely on it; see [54 — Taylor Series](54_taylor_series.md) for the
cancellation error hiding behind that line.

---

## Common Mistakes

**Mistake 1 — assuming the value at a point equals the limit at that point.**

```python
# WRONG: this is not a function on all of R, and evaluating it will crash.
def f(x):
    return (x * x - 1) / (x - 1)

try:
    f(1)
except ZeroDivisionError as err:
    print(f"  f(1) crashed: {err}")
```

The right move is to simplify symbolically (`f(x) = x + 1` for `x != 1`) and keep the
excluded point explicit. The tempting version is attractive because it "works everywhere
else", but it hides the one input that breaks. This is the same shape as calling
`f(0)` on `sin(x)/x`, or indexing a list at `len(a)` after a loop that overran.

**Mistake 2 — cancelling in floating point instead of in algebra.**

```python
# WRONG: catastrophic cancellation when x is close to 1.
def unstable(x):
    return (x * x - 1) / (x - 1)

# RIGHT: factor first, so no subtraction of nearly equal numbers happens.
def stable(x):
    return x + 1


print("        x                unstable            stable")
for e in (0, -6, -9, -12, -15):
    x = 1.0 + 10.0 ** e
    print(f"  {x:<18.12f} {unstable(x):<20.12f} {stable(x):.12f}")
print("  Identical functions in exact arithmetic; wildly different in floats.")
```

The wrong version is tempting because it looks like the "simplest" transcription of the
formula, and it agrees with the right version for most inputs. Only near the trouble
point does it fail, which is the worst possible time to discover the bug.

**Mistake 3 — using a function value as a derivative.**

```python
# WRONG: f(x) is the height, not the slope.
import math
f = math.cos
print(f"  f(2.0) = {f(2.0):.6f}   <- that is a height, not a slope")
print(f"  true f'(2.0) = {-math.sin(2.0):.6f}")
```

Correct slope at a point requires a limit; you cannot get it from a single evaluation.
This misconception is what makes people think `dy/dx` is a number attached to a point.
It is not — it is a limit of *differences*, attached to a point, but built from pairs of
points.

**Mistake 4 — trusting an iterative method to converge.**

```python
# WRONG SHAPE: a fixed-step loop with no stopping criterion and no iteration cap.
# Shown with a cap ONLY so this snippet terminates; remove the cap and it hangs forever.
x = 1.0
for _ in range(1_000_000):
    x = x - 0.3
print(f"  after a million steps of x -= 0.3, x = {x:.1f}")
print("  Subtract a constant and you drift off to -infinity, not to a root of anything.")
print("  The fix is a real convergence criterion plus a cap, e.g. Newton for sqrt(2):")
```

```python
import math

x = 1.0
for k in range(1, 7):
    x = 0.5 * (x + 2 / x)
    print(f"  Newton step {k}: {x:.15f}")
print(f"  exact sqrt(2)      : {math.sqrt(2):.15f}")
print("  Here each step is derived from the derivative, so the error squares away.")
```

The Babylonian method for `sqrt(2)` converges from any positive start, but Newton on a
non-convex function can walk off to infinity, and fixed-point iteration $x_{k+1} = g(x_k)$
diverges when $|g'|$ at the fixed point exceeds 1 — which is exactly what `x -= 0.3` does:
the "derivative" it assumes is 1, so it converges to $1/0.3 \approx 3.333$ for any function
whose actual derivative there is not 1. A real implementation needs a stopping criterion and
a maximum iteration count. Both are limits in disguise: "has it stopped moving?"

**Mistake 5 — assuming `O()` means "equal to", or that a limit must be evaluated exactly.**

```python
# WRONG: trying to evaluate "the" limit to settle a complexity question.
import math

n = 1000
print(f"  n log n at n={n} is exactly {n * math.log(n):.4f}")
print("  but the runtime is not; it is only BOUNDED by some c * n log n for large n.")
print("  Deciding O(n) vs O(n log n) needs the ratio's limit, not either value.")
```

You never need the exact limit value to use asymptotic analysis. You need to know which
bound grows slowest, and that is decided by comparing ratios, not by computing limits.
See [80 — Big-O and Complexity Analysis](../part06_algorithms_math/80_big_o_and_complexity.md).

---

## Exercises and Solutions

**[ ] Exercise 1 — composition and inverse.** Let $f(x) = 2x - 5$ and $g(x) = x^2 + 1$.
(a) Compute $(f \circ g)(x)$ and $(g \circ f)(x)$. (b) Show explicitly that composition need
not commute. (c) Find $f^{-1}$ and verify $f(f^{-1}(y)) = y$. (d) Does $g$ have an inverse
on all of $\mathbb{R}$? Justify with two specific inputs.

<details>
<summary>Solution</summary>

(a) $(f \circ g)(x) = f(x^2+1) = 2(x^2+1) - 5 = 2x^2 - 3$.
$(g \circ f)(x) = g(2x-5) = (2x-5)^2 + 1 = 4x^2 - 20x + 26$.

(b) At $x = 1$: $(f\circ g)(1) = 2 - 3 = -1$ but $(g\circ f)(1) = 4 - 20 + 26 = 10$.
Different, so composition does not commute. (In linear algebra language, function
composition is like matrix multiplication, which is not commutative.)

(c) Solve $y = 2x - 5$: $x = (y+5)/2$, so $f^{-1}(y) = (y+5)/2$.
Then $f(f^{-1}(y)) = 2\cdot\frac{y+5}{2} - 5 = (y+5) - 5 = y$. ✓
Also $f^{-1}(f(x)) = \frac{2x-5+5}{2} = x$. ✓

(d) No. $g(1) = 2$ and $g(-1) = 2$, so $g$ is not injective on $\mathbb{R}$ and has no
inverse there. Restricted to $[0, \infty)$ it is strictly increasing, so there it *does*
have an inverse: $g^{-1}(y) = \sqrt{y - 1}$. Restricting the domain is the standard way to
repair this — and it is exactly what `math.sqrt` does.

</details>

**[ ] Exercise 2 — compute a limit and prove it.** Let $f(x) = \dfrac{3x - 6}{x - 2}$.
(a) What is $f(2)$ in Python, and why does it fail? (b) What is
$\lim_{x \to 2} f(x)$? (c) Write the epsilon-delta proof with an explicit choice of
$\delta(\varepsilon)$.

<details>
<summary>Solution</summary>

(a) `f(2)` computes `0/0`. In Python that is either `ZeroDivisionError` (for floats) or
`nan` (via `float('nan')`/`math.nan`), because there is no value to return.

(b) Factor: $3x - 6 = 3(x-2)$, so for $x \ne 2$ we have $f(x) = 3$. Therefore
$\lim_{x\to 2} f(x) = 3$. Every sampled value should print as exactly 3.0.

(c) We need: for all $\varepsilon > 0$ there is $\delta > 0$ with
$0 < |x - 2| < \delta \Rightarrow |f(x) - 3| < \varepsilon$. Since $f(x) - 3 = 0$ for all
$x \ne 2$, the left-hand side is $0 < \varepsilon$ for any positive $\varepsilon$. So
$\delta$ can be anything at all — take $\delta = 1$. This is a *constant* function with a
hole, and constants satisfy every epsilon-delta requirement trivially.

</details>

**[ ] Exercise 3 — classifying discontinuities.** For each function, say whether the limit
at the named point exists, and if so whether the function is continuous there:

1. $f(x) = \dfrac{1}{x}$ at $x = 0$
2. $f(x) = \sin(x)/x$ for $x \ne 0$, $f(0) = 0$ at $x = 0$
3. $f(x) = \lfloor x \rfloor$ (the floor function) at $x = 2$
4. $f(x) = x^2$ at $x = 0$

<details>
<summary>Solution</summary>

1. **Infinite discontinuity.** As $x \to 0^+$, $1/x \to +\infty$; as $x \to 0^-$ it tends to
   $-\infty$. The two-sided limit does not exist at all, and the function is not defined at
   0. This is exactly the shape of `1.0 / 0.0` returning `inf` in Python.

2. **Removable discontinuity.** $\lim_{x\to 0} \sin(x)/x = 1$ exists, but $f(0) = 0 \ne 1$.
   So the limit exists and the function is *not* continuous. This is a genuine bug shape:
   the code produces plausible numbers everywhere and one wrong number at the special
   point. Compare with the worked example, where the special point had no value at all.

3. **Jump discontinuity.** $\lim_{x\to 2^-} \lfloor x \rfloor = 1$ and
   $\lim_{x\to 2^+} \lfloor x \rfloor = 2$. Two different one-sided limits, so no limit
   exists. In code, this is `int(x)` on negative values — a function with a jump at every
   integer, and the reason `int()` behaves asymmetrically around zero.

4. **Continuous.** $\lim_{x\to 0} x^2 = 0 = f(0)$. Polynomials are continuous everywhere;
   more generally any function built from continuous pieces by arithmetic and composition
   is continuous (limit laws plus the composition theorem).

</details>

**[ ] Exercise 4 — a convergent iteration and its limit.** Starting from $x_0 = 1$, define

$$x_{n+1} = \tfrac{1}{2}\left(x_n + \frac{2}{x_n}\right)$$

(a) Prove by induction that $x_n > 0$ for all $n$.
(b) Prove that $x_{n+1} < x_n$ whenever $x_n > \sqrt{2}$. (Hint: expand
$x_{n+1} - x_n = \frac{2 - x_n^2}{2 x_n}$.)
(c) Using (a) and (b) plus the fact that a monotone bounded sequence converges, argue that
$(x_n)$ converges, and identify the limit.

<details>
<summary>Solution</summary>

(a) Base case: $x_0 = 1 > 0$. Step: if $x_n > 0$ then $2/x_n > 0$, so the average
$x_{n+1} = \frac12(x_n + 2/x_n) > 0$. ✓

(b) $x_{n+1} - x_n = \frac{1}{2}(x_n + \frac{2}{x_n} - 2x_n) = \frac{2/x_n - x_n}{2}
= \frac{2 - x_n^2}{2 x_n}$. If $x_n > \sqrt 2$ then $x_n^2 > 2$, so the numerator is
negative; the denominator $2x_n$ is positive. Hence $x_{n+1} - x_n < 0$, i.e.
$x_{n+1} < x_n$. ✓

(c) $x_1 = \frac32 < \sqrt 2$, so the sequence is *decreasing from n = 1 onward*. It is
bounded below by 0 by (a). A monotone decreasing sequence bounded below converges. Let the
limit be $L$. Passing to the limit in the recurrence is legitimate because $x \mapsto
\frac12(x + 2/x)$ is continuous on $(0,\infty)$:

$$L = \tfrac12\left(L + \frac{2}{L}\right) \Rightarrow 2L = L + 2/L \Rightarrow L^2 = 2
\Rightarrow L = \sqrt 2$$

(Reject $L = -\sqrt2$ using $L > 0$.) Note every step: the monotone-bounded-sequence
theorem is a *limit* result, and it is the reason this loop terminates.

</details>

**[ ] Exercise 5 — Challenge: prove the Intermediate Value Theorem's contrapositive in
code.** Write a function `no_root_despite_sign_change(f, lo, hi, n)` that samples `f` at
`n` evenly spaced points and returns `True` if it detects a sign change **and** a
discontinuity (measured as `max |f(x_{i+1}) - f(x_i)|` exceeding a tolerance larger than
the sign change itself). Demonstrate it on a continuous function like $x^2 - 2$ on
$[0, 2]$ (no warning) and on a hopping step (warning). Then explain what hypothesis of
the theorem your detector is approximating.

<details>
<summary>Solution</summary>

```python
def scan(f, lo, hi, n=2001, tol=0.5):
    """Return (sign_change_found, jump_size) over n samples."""
    sign_change = False
    jump = 0.0
    prev_x, prev_y = lo, f(lo)
    for i in range(1, n):
        x = lo + (hi - lo) * i / (n - 1)
        y = f(x)
        if (prev_y < 0) != (y < 0):
            sign_change = True
        jump = max(jump, abs(y - prev_y))
        prev_x, prev_y = x, y
    return sign_change, jump


continuous = lambda t: t * t - 2
hopping = lambda t: -1.0 if t < 0 else 1.0

for name, f, lo, hi in (("x^2 - 2 on [0,2]", continuous, 0.0, 2.0),
                        ("hopping step on [-1,1]", hopping, -1.0, 1.0)):
    sc, jump = scan(f, lo, hi)
    print(f"{name:24} sign change={sc}  largest jump between samples={jump:.4f}"
          f"  flagged={sc and jump > 0.5}")
```

```text
x^2 - 2 on [0,2]         sign change=True  largest jump between samples=0.0040  flagged=False
hopping step on [-1,1]   sign change=True  largest jump between samples=2.0000  flagged=True
```

The theorem's hypothesis is **continuity on the whole closed interval**. Our detector
approximates it by checking that the function does not move much between adjacent sample
points — a crude finite-difference estimate of the *maximum* change over the interval.
This is exactly how `scipy.integrate.quad` and `scipy.optimize.brentq` warn you: they
watch the function's behaviour between probes rather than trying to verify a limit.

Note also what the detector cannot do: a function could have a very narrow, very tall
spike between two samples and look perfectly continuous at this resolution. No finite
sampling can certify continuity; it can only fail to disprove it. That gap is why
production solvers expose an `eps` tolerance and document that they "assume" continuity
rather than checking it.

</details>

---

## Summary

- A function maps every element of its domain to exactly one element of its codomain;
  composition `f(g(x))` is what every function call in your program is.
- A function has an inverse exactly when it is injective (no two inputs share an output);
  hash-table collisions are the same problem with the same repair, chaining.
- `lim x->a f(x) = L` means you can meet any accuracy demand by narrowing a neighbourhood;
  it does not require `f(a)` to exist or to equal `L`.
- Epsilon-delta is the only honest definition; everything else is a theorem about it, and
  `Fraction` lets you test it with zero rounding error.
- Limit laws let you compute new limits from known ones, which is how you avoid a table of
  thousands of standard results.
- Continuity means the value at a point matches the limit there: no holes, no jumps.
- Continuity is a *hypothesis*, not a nicety. Bisection returns a wrong answer with total
  confidence when given a discontinuous function.
- Big-O is a limit at infinity, so asymptotic claims are limit claims; the comparison
  technique (`n = O(n log n)`) lives in [Part 06](../part06_algorithms_math/).

## Next

[51 — Derivatives](51_derivatives.md) turns the limit idea from "approach a point" into
"measure instantaneous rate of change", and shows that the chain rule is exactly the
mechanism behind backpropagation.