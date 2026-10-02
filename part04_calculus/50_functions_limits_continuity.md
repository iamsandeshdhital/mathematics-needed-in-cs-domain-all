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
  Lesson [51](../part04_calculus/51_derivatives.md) is entirely about this.
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

Symbols follow [SYMBOLS.md](../SYMBOLS.md).

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

## Formula Sheet

Every symbol and definition this lesson uses. Restrictions are stated in the last
column because omitting them is how people get answers wrong.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `f : X \to Y` | `$\mathrm{dom}(f) = X$, $\mathrm{codom}(f) = Y$, and every $x \in X$ has exactly one $f(x) \in Y$` | a machine that accepts anything in $X$ and answers with exactly one thing from $Y$ | writing down a function's contract before implementing it |
| `$(f \circ g)(x)$` | `$(f \circ g)(x) = f(g(x))$, valid when $\mathrm{codom}(g) \subseteq \mathrm{dom}(f)$` | run $g$ first, then feed its answer into $f$ | reading nested calls; stacking layers in a neural network |
| `$\mathrm{im}(f)$` | `$\mathrm{im}(f) = \{ f(x) : x \in X \} \subseteq Y$` | the outputs actually reachable, which may be a smaller set than the codomain | deciding where an inverse is defined |
| injective | `$f(a) = f(b) \Rightarrow a = b$` | no two different inputs share an output | the existence test for an inverse; why a hash table needs chaining |
| surjective | `$\mathrm{im}(f) = Y$` | every promised output is actually reached | checking a range scan really covers its declared range |
| bijective | injective **and** surjective | one-to-one and onto | when the inverse must live on the whole codomain |
| `f^{-1}` | `$f^{-1}(f(x)) = x$` and `$f(f^{-1}(y)) = y$`, with `$\mathrm{dom}(f^{-1}) = \mathrm{im}(f)$` | the undo function | solving an equation for its input; undoing a linear layer |
| limit point | `$a$ is a limit point of $\mathrm{dom}(f)$` | every neighbourhood of $a$ contains a point where $f$ is defined | checking that a limit at $a$ is even a meaningful question |
| `$\lim_{x\to a} f(x) = L$` | `$\forall \varepsilon > 0\ \exists \delta > 0\ \forall x:\ 0 < \lvert x - a \rvert < \delta \Rightarrow \lvert f(x) - L \rvert < \varepsilon$` | meet any accuracy demand $\varepsilon$ by narrowing a window $\delta$ | proving and testing limits; the basis of every convergence claim |
| `0 < \lvert x - a \rvert` | part of the limit definition above | $x$ is never allowed to *equal* $a$ | why a limit can exist where the function has no value (the `0/0` case) |
| one-sided limits | `$\lim_{x \to a^{+}} f(x) = L_+$, $\ \lim_{x \to a^{-}} f(x) = L_{-}$` | approach $a$ from the right only, or the left only | classifying jump discontinuities; $1/0^{+}$ is $+\infty$ while $1/0^{-}$ is $-\infty$ |
| limit laws | `$\lim (f+g) = L+M`, $\ \lim (fg) = LM$, $\ \lim \frac{f}{g} = \frac{L}{M}$ — the last needs `$M \neq 0$` | build new limits out of known ones | avoiding a table of thousands of memorised limits |
| seed limits | `$\lim_{x \to 0}\frac{\sin x}{x} = 1$, $\ \lim_{x \to 0}\frac{1-\cos x}{x^2} = \tfrac12$` | the two facts all the trigonometric limits come from | deriving trig limits; explaining `math.sin(x)/x` losing resolution |
| continuity at $a$ | `$\lim_{x \to a} f(x) = f(a)$, **and** `$a \in \mathrm{dom}(f)$` | the value there equals the value it was heading towards: no hole, no jump | checking a solver's hypothesis *before* trusting its answer |
| composition of continuous functions | `$f$ continuous at `$a$` and `$g$` continuous at `$f(a)$` $\Rightarrow f \circ g$ continuous at `$a$` | continuous things compose | proving a whole pipeline is continuous |
| Intermediate Value Theorem | `$f$ continuous on $[a,b]$ and `$f(a) < 0 < f(b)$` $\Rightarrow \exists c \in (a,b)$ with `$f(c) = 0$` | a sign change forces a crossing — **only** if $f$ is continuous | bisection search, every bracketing root finder |
| Extreme Value Theorem | `$f$ continuous on the closed bounded interval $[a,b]$ $\Rightarrow$ $f$ attains a max and a min there | on a closed bounded interval, a continuous function has a best point and a worst point | guaranteeing that the minimiser gradient descent is chasing actually exists |
| `$\lim_{n \to \infty} x_n = L$` | `$\forall \varepsilon > 0\ \exists N:\ n \ge N \Rightarrow \lvert x_n - L \rvert < \varepsilon$` | "eventually always this close", instead of "inside this small window" | the stopping criterion of every iterative loop |
| monotone bounded sequence | `$x_n$ increasing and bounded above $\Rightarrow x_n \to L$ (decreasing and bounded below likewise)` | monotone and fenced in must settle down | proving the Babylonian loop for `math.sqrt(2)` terminates |
| Babylonian step | `$x_{n+1} = \tfrac12\left(x_n + \frac{2}{x_n}\right)$, needs `$x_0 > 0$` | one Newton step on $x^2 - 2$, arranged symmetrically | producing `sqrt(2)` with provable quadratic convergence |
| fixed-point iteration | `$x_{k+1} = g(x_k)$ converges to a fixed point $L$ when `$\lvert g'(L) \rvert < 1$` | the update rule's own slope at the fixed point decides everything | diagnosing a `while` loop that drifts or oscillates instead of converging |
| forward difference | `$f'(x) \approx \frac{f(x+h) - f(x)}{h}$, error `$O(h)$` for `$h \to 0$` | slope measured with one step forward; overestimates on a convex function | cheap gradient estimates (finite differences, SPSA) |
| `f \in O(g)` | `$\exists c > 0,\ \exists n_0:\ f(n) \le c\,g(n)$ for all `$n \ge n_0$` | from some point on, $f$ stays under a fixed multiple of $g$ | every runtime guarantee in [Part 06](../part06_algorithms_math/80_big_o_and_complexity.md) |
| ratio form of Big-O | `$\lim_{n \to \infty} \frac{f(n)}{g(n)} = 0$` (or $\le c$) | compare growth by dividing, never by evaluating either side | ranking $n$, $n\log n$, $2^n$ |

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
the limit. Do not rely on it; see [54 — Taylor Series](../part04_calculus/54_taylor_series.md) for the
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

## Multiple Choice Questions

**Q1.** Let $f(x) = \dfrac{x^2-1}{x-1}$. What is $\lim_{x \to 1} f(x)$?

- A) The limit does not exist, because $f(1)$ is the indeterminate form $0/0$
- B) $2$
- C) $0$, because the numerator $x^2-1$ tends to $0$
- D) $1$, because that is the limit of $\sin(x)/x$

<details>
<summary>Answer and explanation</summary>

**B) 2.**

Factor the numerator for $x \ne 1$: $x^2 - 1 = (x-1)(x+1)$, so $f(x) = x + 1$ there, and
$\lim_{x\to1} f(x) = 1 + 1 = 2$. The worked example confirms it numerically
($f(0.999) = 1.999000$) and by epsilon-delta, where $f(x) - 2 = x - 1$ makes
$\delta = \varepsilon$ work.

Option A is the central trap: the limit definition contains $0 < |x - a|$, so $x$
never equals $1$ and $f(1)$ is irrelevant. That $f(1)$ crashes with
`ZeroDivisionError` is a fact about the *value*, not the *limit*.
Option C assumes a ratio's limit equals the numerator's limit, forgetting that a
denominator heading to zero does not preserve that. Option D transplants the limit of
a different function; $\sin(x)/x \to 1$ is true but is not what this function does —
its simplified form is $x+1$, not $\sin(x)/x$.

</details>

**Q2.** In the definition of $\lim_{x \to a} f(x) = L$, what does the requirement
$0 < |x - a| < \delta$ accomplish?

- A) It guarantees $f(a)$ is defined, so the function is total near $a$
- B) It excludes $x = a$, so the function does not have to be defined or to have a sensible value there
- C) It restricts $x$ to values greater than $a$, which is what makes the limit one-sided
- D) It forces $\delta < \varepsilon$, which ties the window size to the accuracy requested

<details>
<summary>Answer and explanation</summary>

**B) It excludes $x = a$, so the function does not have to be defined or to have a
sensible value there.**

That clause is exactly why $\lim_{x\to1}\frac{x^2-1}{x-1}$ exists even though the
function has no value at 1, and why `math.sin(x)/x` has a limit at 0 while the
expression itself is meaningless at 0.

Option A gets the logic backwards: the point of the definition is that $f(a)$ is
*irrelevant*. Option C confuses the two-sided limit (which is what
$\lim_{x\to a}$ means) with the one-sided limits $\lim_{x\to a^{+}}$ and
$\lim_{x\to a^{-}}$ — no inequality between $x$ and $a$ appears in the definition
of the two-sided limit. Option D is a real and tempting belief, but it is false:
nothing requires $\delta \le \varepsilon$. The epsilon-delta proof above deliberately
chooses $\delta = \varepsilon$ because that happens to work, not because it is
mandated. Formally, $\delta$ and $\varepsilon$ play different quantifier roles —
$\varepsilon$ is chosen by the challenger, $\delta$ by the prover — and no relation
between them is imposed.

</details>

**Q3.** Define $f(0) = 1$ and $f(x) = \sin(x)/x$ for $x \ne 0$. Is $f$ continuous at
$x = 0$?

- A) No, because $f$ contains a division and divisions always create discontinuities
- B) Yes, because $\lim_{x \to 0} \sin(x)/x = 1$ and $f(0) = 1$
- C) No, because $\sin(x)/x$ has no value at $x = 0$
- D) Yes, but only when the domain is restricted to $[0, \infty)$

<details>
<summary>Answer and explanation</summary>

**B) Yes, because $\lim_{x \to 0} \sin(x)/x = 1$ and $f(0) = 1$.**

Continuity at $a$ means two things at once: $a$ is in the domain, and the limit equals
the value. Both hold here. This is the *only* difference between this $f$ and the one
in Exercise 3 item 2, where $f(0) = 0$ and the function is therefore discontinuous at
0. The algebra is identical; one assignment decides it.

Option A is a genuine misconception — division is only dangerous when the divisor can
approach zero. Here the divisor $x$ does approach zero and the ratio still converges,
because $\sin(x) \sim x$. Option C is the confusion this whole lesson is built to
remove: the limit $\lim_{x\to0}\sin(x)/x = 1$ exists *precisely because* the expression
has no value at 0. Option D confuses continuity, a local property at one point, with the
choice of domain, a global declaration. $f$ is just as continuous at 0 when $x$ ranges
over all of $\mathbb{R}$.

</details>

**Q4.** The lesson's `bisect` function is run on
`hopping(t) = -1.0 if t < 0 else 1.0` over the bracket $[-1, 1]$. What happens, and
why?

- A) It raises `ValueError`, because the sign-change test at the endpoints is unreliable
- B) It returns a point near zero, and that point really is a root
- C) It returns about `-9.094947017729282e-13`, which is not a root, because the continuity hypothesis of the Intermediate Value Theorem is violated
- D) It fails to terminate, because the function is unbounded on the bracket

<details>
<summary>Answer and explanation</summary>

**C) It returns about `-9.094947017729282e-13`, which is not a root, because the
continuity hypothesis of the Intermediate Value Theorem is violated.**

`hopping(-0.001) = -1.0` and `hopping(0.001) = 1.0`, so the signs differ and
`bisect`'s guard passes. Each halving keeps a bracket whose endpoint signs still differ,
so the loop runs to its width tolerance and returns the midpoint, a tiny negative
number. But `hopping` of that number is `-1.0`: there is no $t$ anywhere with
$hopping(t) = 0$. The function jumps straight over zero.

Option A is wrong because the sign test is not broken — it is working exactly as
written. It detects a sign change; that is all it claims to do. Option B is the
dangerous one, since it is what a reader expects from a function called `bisect`.
Option D is wrong: `hopping` is bounded on $[-1,1]$, and the loop's exit condition
`0.5 * (hi - lo) < tol` guarantees termination in about $\log_2(2/10^{-12}) \approx 41$
iterations. The bug here is not divergence but **confidently wrong output**, which is
strictly worse.

</details>

**Q5.** What is $\lim_{x \to 0} \frac{1}{x}$?

- A) $0$, because every value of $1/x$ other than at $x = 0$ is finite
- B) It does not exist: $\lim_{x\to0^{+}} 1/x = +\infty$ while $\lim_{x\to0^{-}} 1/x = -\infty$
- C) $+\infty$, because $1/x$ grows without bound as $x$ shrinks
- D) It exists and equals $+\infty$, since infinity is a number a limit may equal

<details>
<summary>Answer and explanation</summary>

**B) It does not exist: $\lim_{x\to0^{+}} 1/x = +\infty$ while
$\lim_{x\to0^{-}} 1/x = -\infty$.**

The code in Exercise 6 shows the magnitudes growing together ($10^{1}, 10^{3},
10^{6}, 10^{10}$) while the signs flip. A two-sided limit requires the *same* answer
from both directions; here they are opposites, so there is no two-sided limit. This is
Exercise 3 item 1, an infinite discontinuity.

Option A confuses "the function is finite at each nearby point" with "the values settle
down to something". A limit asks about settling, not boundedness. Option C looks only at
the right-hand side — it is $\lim_{x\to0^{+}}$, not the two-sided limit, and the
magnitude alone is not a limit at all. Option D is the subtle one: $+\infty$ is a
perfectly legitimate one-sided limit value, but the two-sided limit at 0 does not equal
it, so "it exists and equals $+\infty$" is self-contradictory here. (Compare
$\lim_{x\to0} 1/x^2 = +\infty$, which *is* a legitimate two-sided infinite limit,
because both sides give $+\infty$.)

</details>

**Q6.** Using the numbers in the lesson's code, why does $g(x) = x^3 - 3x$ have no
inverse on all of $\mathbb{R}$?

- A) Because $g$ is not surjective: some real number is never produced by $g$
- B) Because $g$ is not injective: $g(-2) = g(1) = -2$ and $g(-1) = g(2) = 2$
- C) Because $g$ is not continuous at $x = 0$, so it cannot be inverted
- D) Because $g$ is not monotone increasing on all of $\mathbb{R}$

<details>
<summary>Answer and explanation</summary>

**B) Because $g$ is not injective: $g(-2) = g(1) = -2$ and $g(-1) = g(2) = 2$.**

An inverse exists exactly when the function is injective, and injectivity is refuted by
a single pair of distinct inputs with equal outputs. The code prints exactly these
collisions, followed by `equal? True`.

Option A describes a different defect. It is also true that $g$ is not surjective on
$\mathbb{R}$ — a cubic is onto, so in fact $g$ *is* surjective, which makes A simply
false here — but surjectivity is the wrong reason to look: injectivity is what forces
the inverse's existence. Option C is irrelevant; the inverse theorem needs injectivity,
not continuity (both $x^3-3x$ and its trouble spots are perfectly continuous).
Option D confuses a symptom with the cause: failure to be monotone is *why* the
collisions exist, and monotone-increasing is a sufficient but not necessary condition
for invertibility. Restricting the domain to $[-1, 1]$ is the standard repair — the same
move `math.sqrt` makes by refusing negative arguments.

</details>

**Q7.** The code prints $f(n)/g(n) = 1/\ln n$ for $n = 10, 100, 1000, 10^6, 10^9$:
$0.434294$, $0.217147$, $0.144765$, $0.072382$, $0.048255$. Since $\ln n \to \infty$,
what is the correct asymptotic statement about $n$ relative to $n \ln n$?

- A) $n = O(n \ln n)$, because the ratio is already below $1$ at $n = 10$
- B) $n = \Theta(n \ln n)$, because the ratio is positive and bounded
- C) $n = o(n \ln n)$, because the ratio tends to $0$
- D) Nothing yet; five sampled values cannot establish a limit

<details>
<summary>Answer and explanation</summary>

**C) $n = o(n \ln n)$, because the ratio tends to $0$.**

Since $1/\ln n \to 0$, the ratio of $n$ to $n\ln n$ vanishes. That is the definition of
little-$o$: $f = o(g)$ when $f(n)/g(n) \to 0$. The five printed values are not the proof;
the proof is $\ln n \to \infty$, which is a limit fact. The samples are evidence that
converges to the fact.

Option A is the sloppy version people write and it is *technically true* but far weaker:
for every $n \ge 10$ the ratio is at most $0.434$, so $n \le 0.434\,n\ln n$ and the
$O$ bound does hold. The error is claiming this is the informative conclusion when the
ratio actually tends to zero. Option B confuses $\Theta$ with positivity — $\Theta$
needs the ratio bounded above *and* bounded below by positive constants, and here it
falls to $0$. Option D is a good instinct applied to the wrong object: sampling cannot
establish a limit, but the five lines are accompanied by the closed form $1/\ln n$, and
that does.

</details>

**Q8.** Why is the Babylonian iteration $x_{n+1} = \tfrac12(x_n + 2/x_n)$, started at
$x_0 = 1$, *provably* going to terminate rather than merely appearing to?

- A) Because each step is a floating-point operation, so after enough steps the value cannot change
- B) Because the sequence is decreasing from $n = 1$ onward and bounded below by $0$, and a monotone bounded sequence converges
- C) Because the code prints the final value, so convergence has been demonstrated
- D) Because $\sqrt{2}$ is irrational, so the iteration can never reach it exactly

<details>
<summary>Answer and explanation</summary>

**B) Because the sequence is decreasing from $n = 1$ onward and bounded below by $0$,
and a monotone bounded sequence converges.**

Exercise 4 supplies the argument in full: $x_{n+1} - x_n = (2 - x_n^2)/(2x_n)$, which is
negative whenever $x_n > \sqrt{2}$; $x_1 = 3/2 > \sqrt{2}$ and $x_2 = 17/12 < \sqrt{2}$,
so the sequence is decreasing from $n = 1$ and bounded below by $0$. Continuity of
$x \mapsto \tfrac12(x + 2/x)$ on $(0,\infty)$ then lets you pass to the limit and solve
$L = \tfrac12(L + 2/L)$ to get $L = \sqrt{2}$.

Option A describes *numerical* termination — the printed table shows the change reaching
`0.000e+00` at step 6 because the double has no more resolution. That is a fact about
53 bits of mantissa, not about convergence, and it would be no guarantee at all with
exact rationals. Option C reverses cause and effect; printing a number witnesses nothing.
Option D is a red herring that is also self-defeating: the sequence approaches $\sqrt2$
without reaching it, and the reason the loop *stops* is the width tolerance, not arrival.

</details>

**Q9.** The code computes `(x**2 - 1)/(x - 1)` at `x = 1.0 + 1e-9` and prints exactly
`2.000000000000`. What has been established?

- A) The function is continuous at $x = 1$
- B) The cancellation problem from Common Mistake 2 is unfounded, since the code gives the right answer here
- C) Nothing about continuity: `x**2 - 1` and `x - 1` rounded to the same double, so the quotient landed on 2.0 by coincidence
- D) The limit of the function as $x \to 1$ is $0$, since the numerator vanishes

<details>
<summary>Answer and explanation</summary>

**C) Nothing about continuity: `x**2 - 1` and `x - 1` rounded to the same double, so
the quotient landed on 2.0 by coincidence.**

At $x = 1 + 10^{-9}$, $x^2 - 1 \approx 2\cdot 10^{-9}$ is computed by subtracting two
numbers of magnitude about $1$ — every digit of that result is cancellation error, and
with 16 significant digits there are none left to be significant. `x - 1` is exact
($\approx 10^{-9}$). The quotient $2.000001$ then rounds to `2.000000000000` simply
because it is within half an ulp of $2$. This is the lesson's own point: "the machine
has accidentally produced the limit. Do not rely on it."

Option A is the trap — the function is *not* even defined at $x = 1$; Python raises
`ZeroDivisionError` there. Option B mistakes agreement with correctness: the stable
form `x + 1` and the unstable form disagree badly at other inputs, which is exactly
what Common Mistake 2's table shows. Option D is nonsense twice over: the numerator's
limit being $0$ says nothing about the ratio's limit, and the ratio's limit is $2$,
not $0$.

</details>

**Q10.** The code computes `affine(double(5))` and prints $37$, where
$f(x) = 3x + 7$ and $g(x) = 2x$. Which statement is correct?

- A) $37$ is $f(g(5))$, and computing $g(f(5))$ would also give $37$ because composition of affine functions commutes
- B) $37$ is $g(f(5))$, and computing $f(g(5))$ would give $43$
- C) $37$ is $f(g(5))$, and composition in general does not commute
- D) $37$ is $g(f(5))$, and composition in general does not commute

<details>
<summary>Answer and explanation</summary>

**C) $37$ is $f(g(5))$, and composition in general does not commute.**

$g(5) = 10$ and then $f(10) = 3(10) + 7 = 37$, matching the printed output and the
formula $(f \circ g)(x) = 6x + 7$ from Worked Example 1. The reverse order gives
$g(f(5)) = g(22) = 44$, which is not $37$.

Option A asserts commutativity, the single most common function-theory error. It fails
even in this lesson, in a different pair: Exercise 1 has $f(x) = 2x-5$, $g(x) = x^2+1$,
where $(f\circ g)(1) = -1$ and $(g\circ f)(1) = 10$. Two particular *affine* maps
happened to commute here by accident of the numbers — $(f\circ g)(x) = 6x+7$ and
$(g\circ f)(x) = 6x + 14$, which agree only at $x = -7/8$. Option B has the order
reversed and the arithmetic wrong ($43$ matches neither composition; the true value is
$44$), which is what makes it attractive to a hurried reader. Option D pairs the wrong
order with a correct principle.

</details>

**Q11.** The lesson says gradient descent on a continuous loss over a closed domain is
"arguing inside" the Extreme Value Theorem. Which hypothesis does EVT actually require?

- A) The loss must be convex
- B) The loss must be continuous on a set that is closed and bounded
- C) The loss must be differentiable everywhere
- D) The loss must be strictly positive everywhere

<details>
<summary>Answer and explanation</summary>

**B) The loss must be continuous on a set that is closed and bounded.**

The Extreme Value Theorem says a continuous function on a *compact* set — which in
$\mathbb{R}^n$ means closed and bounded — attains its maximum and minimum. Closedness
matters because $1/x$ on $(0,1]$ is continuous but never reaches $0$; boundedness
matters because $\arctan x$ on $\mathbb{R}$ is continuous and never reaches $\pm\pi/2$.
Both counterexamples fail for the same reason as the bisection bug: a value that is
approached but not attained.

Option A is the most tempting error. Convexity guarantees that *any* local minimum is
global, which is a different and complementary statement — $\sin x$ is non-convex,
continuous and compactly bounded, and EVT applies to it perfectly well. Convexity
guarantees uniqueness of the minimiser; EVT guarantees existence.
Option C over-requires: EVT needs only continuity, and $\lvert x \rvert$ is continuous
everywhere but non-differentiable at $0$. Option D is far too strong — a log-loss is
negative near $x = 1$ and still has a well-behaved minimiser.

</details>

**Q12.** For $f(x) = x^2$, the forward difference
$\dfrac{f(x+h) - f(x)}{h}$ at $x = 1$ equals $2 + h$. What does this say about
approximating the derivative with a forward difference?

- A) It converges to $0$ as $h \to 0$, because $f$ is even
- B) It converges to $2$ from above, with error exactly $h$
- C) It converges to $2$ from below, with error exactly $h$
- D) It equals $2$ exactly for every $h$, because the $h^2$ term cancels

<details>
<summary>Answer and explanation</summary>

**B) It converges to $2$ from above, with error exactly $h$.**

Expand: $f(1+h) - f(1) = (1+h)^2 - 1 = 2h + h^2$, and dividing by $h$ gives $2 + h$.
So the true derivative $f'(1) = 2$ is approached from above, and the error is exactly
$h$ — first order. Because $x^2$ is convex, its tangent line lies below the curve, so a
forward secant must lie above the tangent, which is a one-sided bias rather than a
random error. That bias is what Lesson [51](../part04_calculus/51_derivatives.md) fixes with the central
difference, which throws the $h$ term away and gets error $O(h^2)$.

Option A misreads "even" — parity has nothing to do with what a secant does.
Option C is the central-difference behaviour, not the forward one: averaging
$f(1+h)$ and $f(1-h)$ gives $2 + h^2$, approaching from above but with the linear error
removed. Option D ignores that dividing by $h$ turns the $h^2$ term into $h$, not into
nothing.

</details>

---

## Subjective Questions

### Short Answer

**Q1. State the epsilon-delta definition of $\lim_{x\to a}f(x) = L$, and say what the
clause $0 < |x - a|$ is for.**

<details>
<summary>Model answer</summary>

$\lim_{x\to a}f(x) = L$ means: for every $\varepsilon > 0$ there exists $\delta > 0$
such that for every $x$ in the domain of $f$,

$$0 < |x - a| < \delta \implies |f(x) - L| < \varepsilon.$$

The clause $0 < |x - a|$ forbids $x$ from *equalling* $a$. That is what frees the
definition from requiring the function to be defined at $a$ at all: $\lim_{x\to1}
(x^2-1)/(x-1) = 2$ even though $f(1)$ raises `ZeroDivisionError`. $\varepsilon$ is the
accuracy demanded by the challenger; $\delta$ is the window the prover supplies in
response; the statement only says one always exists once the other is chosen.

</details>

**Q2. Give two functions with a discontinuity at $x = 1$: one whose limit exists
there, and one whose does not. Classify each.**

<details>
<summary>Model answer</summary>

Limit exists, function discontinuous — *removable*. $f(x) = (x^2-1)/(x-1)$ for
$x \ne 1$: $\lim_{x\to1} f(x) = 2$ exists, but $f(1)$ is undefined, so the value does
not match the limit. If instead you set $f(1) = 5$ instead, the limit still exists and
still does not equal the value — a removable discontinuity with a wrong value rather
than a hole, the shape of the code's `abs_but_five_at_zero`.

Limit does not exist — *jump*. $f(x) = \lfloor x \rfloor$ at $x = 1$:
$\lim_{x\to1^-} f(x) = 0$ and $\lim_{x\to1^+} f(x) = 1$, two different one-sided limits.
A third shape is the *infinite* discontinuity, $f(x) = 1/x$ at $x = 0$, where the
one-sided limits are $+\infty$ and $-\infty$.

</details>

**Q3. State the Intermediate Value Theorem, and say which single hypothesis bisection
search depends on.**

<details>
<summary>Model answer</summary>

**IVT.** If $f$ is continuous on $[a,b]$ and $f(a) < 0 < f(b)$, then there exists
$c \in (a,b)$ with $f(c) = 0$.

Bisection depends on the *continuity on the entire closed bracket*. It verifies only
the sign change ($f(lo)$ and $f(hi)$ have opposite signs); it cannot verify
continuity, so continuity is an assumption it takes on faith. Give it
`hopping(t) = -1.0 if t < 0 else 1.0` on $[-1,1]$ and it returns
`-9.094947017729282e-13`, a point where the function equals $-1.0$ and never equals
zero anywhere. The sign change is the hypothesis the code checks; continuity is the one
it cannot.

</details>

**Q4. Why does $f$ have an inverse exactly when it is injective, and why does that
make hash-table collisions unavoidable?**

<details>
<summary>Model answer</summary>

If $f^{-1}$ exists then $f(f^{-1}(y)) = y$ forces $f$ to send two different inputs to
different outputs, so $f$ is injective. Conversely, if $f$ is injective, assign
$f^{-1}(f(x)) = x$; this is well defined precisely because no two inputs collide, and
the inverse's domain is $\mathrm{im}(f)$, not necessarily the codomain.

A hash table is the same situation with $f = $ `hash` and $Y$ = the bucket index. Two
distinct keys mapping to one bucket means $f$ is not injective, so $f^{-1}$ does not
exist and the lookup cannot be decided from the bucket alone. The lesson's own "hash"
by string length does exactly this: `axe`, `bat`, `bee` all land in bucket 3. The repair
is not a better inverse but a collision *chain* — probe the bucket until the key is
found — which is why Python dicts and Rust's `HashMap` store entries rather than a bare
value.

</details>

**Q5. State the definition of $\lim_{n\to\infty} x_n = L$, and explain how it differs
from $\lim_{x\to a} f(x) = L$.**

<details>
<summary>Model answer</summary>

$\lim_{n\to\infty} x_n = L$ means: for every $\varepsilon > 0$ there is an $N$ such that
for all $n \ge N$, $|x_n - L| < \varepsilon$.

The difference is what plays the role of distance. For a function limit the quantifier
"$0 < |x-a| < \delta$" is about position on the number line; for a sequence it is
"$n \ge N$", about how many iterations have happened. Everything else is identical:
$\varepsilon$ and $N$ (or $\delta$) come from the same quantifier game, and neither
requires the function to be defined at the point. This is exactly why "has it stopped
moving?" — $|x_k - x_{k-1}| < \varepsilon$ for large $k$ — is a convergence question,
and why every iterative solver needs both a tolerance and a cap.

</details>

### Long Answer

**Q1. Why does bisection return a confidently wrong answer on the hopping step, and
what does that tell you about the relationship between a method's code and its
correctness proof?**

<details>
<summary>Model answer</summary>

Bisection's proof has two ingredients. The arithmetic ingredient is trivial: each
iteration halves the bracket, so after $k$ iterations the width is $(b-a)/2^k$ and the
midpoint is within half of that of *something*. The logical ingredient is the
Intermediate Value Theorem, and that is where continuity enters. A sign change tells
you $f$ takes a negative value somewhere and a positive value somewhere; **only**
continuity promotes that to "somewhere in between, $f$ is zero."

Without continuity the implication is simply false, and `hopping` is the counterexample:
$f(t) = -1$ for $t < 0$ and $1$ for $t \ge 0$ never takes the value zero. The bracket
$[lo, hi]$ keeps opposite signs at its endpoints forever, so the invariant the algorithm
maintains is real and true and irrelevant. Halving a bracket that contains no root still
gives a bracket that contains no root, and the returned midpoint
`-9.094947017729282e-13` has $f$ equal to $-1.0$.

The general lesson is worth stating precisely: a solver's output carries no evidence
about whether its hypotheses held. Every guarantee attached to bisection, Newton's
method, Brent's method, and gradient descent is a conditional guarantee — *if* the
function is continuous (or differentiable, or Lipschitz, or convex), *then* the output
satisfies such-and-such. Code cannot test continuity, so it cannot report a violation of
it. That is why the practical defence is external: bracketing chosen by the caller
(where the signs were actually observed), sanity checks on the residual
`abs(f(result))`, and trusting a library that refuses inputs it cannot handle over one
that answers everything.

</details>

**Q2. What would break if you tried to settle "is sorting $O(n\log n)$ or $O(n)$" by
evaluating the ratio at a handful of values of $n$?**

<details>
<summary>Model answer</summary>

You would be trying to certify a statement about all $n \ge n_0$ using finitely many
observations, and the definition of a limit explicitly quantifies over *every*
$\varepsilon > 0$. Five samples cannot discharge an infinite quantifier. Common Mistake
5 names this failure directly: `n log n` at $n = 1000$ is a perfectly definite number,
yet the runtime is not, so evaluating either side settles nothing.

The failure is not hypothetical, because ratios of the wrong kind are *not* monotone.
The lesson's $1/\ln n$ happens to shrink monotonically, which makes sampling look
reliable. Compare $f(n) = 2^{n}$ and $g(n) = 2^{n - 10^6}$: at $n = 10^6$ the ratio is
$1$, and for every $n$ below that it is astronomically small. Any sampled window
overlooks the crossing. Functions in real code can have overhead constants, cache
thresholds, and adaptive branches that make the true ratio rise, fall, and rise again;
$\log n$ versus $n$ on small arrays is the everyday version of this.

The repair is to prove something structural, not numeric. For sorting: the merge step
costs $\Theta(n)$ and there are $\log_2 n$ levels, giving $c\,n\log_2 n \le T(n)
\le C\, n \log_2 n$ by induction, with constants fixed and $n_0$ explicit. You may
then *measure* to find $c$ and $C$, but the proof of the bound came from the structure.
The sampling tells you which constant is plausible; it never tells you the rate.

</details>

**Q3. Why does the machine returning exactly `2.000000000000` for
`(x**2 - 1)/(x - 1)` at `x = 1.0 + 1e-9` establish nothing about continuity, and what
invariant would you need instead?**

<details>
<summary>Model answer</summary>

Look at what was actually subtracted. $x^2 - 1$ with $x \approx 1$ is a difference of
two numbers of size about $1$, so its magnitude is about $2\times 10^{-9}$ while the
operands carry 16 significant digits. Roughly 7 of those digits are the answer and the
remaining 9 are the rounding error of the subtraction itself — classic catastrophic
cancellation. The quotient $2.000001$ then happens to lie within half an ulp of $2.0$,
so it rounds to `2.000000000000`. Nothing was proved about the function; the error
budget was merely exhausted in a lucky direction.

The tell is that the same expression is *not* consistent with itself. Common Mistake 2's
table shows the unstable and stable forms agreeing at $x = 2$ and disagreeing wildly
near $x = 1$, which is what a genuine mathematical property would never do. A computed
value is evidence about the computation, not about the function.

The invariant you actually want is monotonicity of the error against $h$, or a relative
error that shrinks with the computation's resolution. If you shrink the perturbation and
the estimate converges, that is a real signal about differentiability; if the estimate
degenerates and the two algebraically equal forms part company, you have hit the
resolution floor. Practically: cancel in algebra first (`x + 1`), or use a form with no
subtraction of nearly equal numbers, and if you must difference numerically, use a
step size near the cube root of machine epsilon rather than pushing $h$ toward zero.
Lesson [51](../part04_calculus/51_derivatives.md) develops exactly this trade-off for derivatives.

</details>

**Q4. Why must a production solver expose a tolerance and a documentation note instead
of trying to detect continuity for you?**

<details>
<summary>Model answer</summary>

Continuity is a statement about every neighbourhood of every point, which no finite
amount of sampling can certify. Exercise 5's detector asks whether consecutive samples
move by more than a tolerance; it correctly flags the hopping step (largest jump
$2.0000$) and passes $x^2 - 2$ on $[0,2]$ (largest jump $0.0040$), but the exercise
itself shows the limit of the method: a function could have a narrow, tall spike between
two sample points and look perfectly smooth at that resolution. You can only fail to
disprove continuity, never prove it. So any "is this continuous?" check inside a
library is a heuristic wearing a formal costume, and honest libraries say so —
`scipy.optimize.brentq` *documents that it requires a continuous function* and does not
pretend to verify it.

There is a second, deeper reason, and it is about error estimates rather than detection.
`scipy.integrate.quad` estimates integration error from how much successive
subdivisions change the answer, which presumes the integrand behaves. Hand it a
discontinuity and that estimator diverges, so the adaptive loop stops subdividing and
reports a meaningless number. Similarly, `torch.autograd` refuses to differentiate at
points where the derivative does not exist rather than substituting a nearby value —
the missing derivative is information, and silently inventing one is worse than
failing.

The design consequence follows: expose `eps`/`tol` so the caller controls the trade-off
between work and accuracy, cap the iterations so a pathological input cannot hang the
caller, document the hypotheses in terms a caller can check themselves, and check the
*residual* — "is $f(\text{answer})$ actually small?" — because that is a verifiable
fact about the output, unlike continuity.

</details>

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

**[ ] Exercise 6 — one-sided limits and what Python does at a pole.** Let $f(x) = 1/x$
for $x \ne 0$.

(a) Compute $\lim_{x \to 0^{+}} 1/x$ and $\lim_{x \to 0^{-}} 1/x$, and state whether the
two-sided limit exists.
(b) The lesson claims IEEE-754 "decides" these by taking one-sided limits, returning
`inf` for one and `nan` for the other. Check what CPython actually does for
`1.0 / 0.0`, `-1.0 / 0.0` and `0.0 / 0.0`, and explain the discrepancy.
(c) Produce the IEEE-754 answers anyway, and show that one of the resulting values is
itself indeterminate.

<details>
<summary>Solution</summary>

(a) From the right, $1/x \to +\infty$; from the left, $1/x \to -\infty$. The two-sided
limit therefore **does not exist**: the definition needs the *same* $L$ from every
direction, and the directions disagree in sign. (Contrast $1/x^2$, whose two-sided
limit at 0 legitimately equals $+\infty$, because both sides give $+\infty$.)

(b) In CPython all three expressions raise `ZeroDivisionError`:

```python
import math

print("=== One-sided limits of 1/x at 0 ===")
print("   x -> 0^+      1/x")
for e in (1, 3, 6, 10):
    x = 10.0 ** (-e)
    print(f"   1e-{e:<11} {1.0 / x:>16.6e}")
print("   x -> 0^-      1/x")
for e in (1, 3, 6, 10):
    x = -(10.0 ** (-e))
    print(f"  -1e-{e:<11} {1.0 / x:>16.6e}")
print("  Magnitudes agree, signs do not -> the two-sided limit does not exist.")
print()

print("=== What Python actually returns at the pole ===")
for num, den in ((1.0, 0.0), (-1.0, 0.0), (0.0, 0.0)):
    try:
        value = num / den
        print(f"  {num} / {den} = {value}")
    except ZeroDivisionError as err:
        print(f"  {num} / {den} -> ZeroDivisionError: {err}")
print("  CPython tests for a zero divisor before the FPU ever sees it.")
print()

print("=== The IEEE-754 answers you must ask for by name ===")
print(f"  float('inf')    = {float('inf')}")
print(f"  float('-inf')   = {float('-inf')}")
print(f"  float('inf')/2  = {float('inf') / 2}")
print(f"  inf - inf       = {float('inf') - float('inf')}")
print(f"  math.inf * 0.0  = {math.inf * 0.0}")
print("  inf - inf is nan: the form inf - inf is indeterminate, exactly as 0/0 is,")
print("  so the machine refuses to invent a value for it.")
```

Output:

```text
=== One-sided limits of 1/x at 0 ===
   x -> 0^+      1/x
   1e-1               1.000000e+01
   1e-3               1.000000e+03
   1e-6               1.000000e+06
   1e-10              1.000000e+10
   x -> 0^-      1/x
  -1e-1              -1.000000e+01
  -1e-3              -1.000000e+03
  -1e-6              -1.000000e+06
  -1e-10             -1.000000e+10
  Magnitudes agree, signs do not -> the two-sided limit does not exist.

=== What Python actually returns at the pole ===
  1.0 / 0.0 -> ZeroDivisionError: float division by zero
  -1.0 / 0.0 -> ZeroDivisionError: float division by zero
  0.0 / 0.0 -> ZeroDivisionError: float division by zero
  CPython tests for a zero divisor before the FPU ever sees it.

=== The IEEE-754 answers you must ask for by name ===
  float('inf')    = inf
  float('-inf')   = -inf
  float('inf')/2  = inf
  inf - inf       = nan
  math.inf * 0.0  = nan
  inf - inf is nan: the form inf - inf is indeterminate, exactly as 0/0 is,
  so the machine refuses to invent a value for it.
```

The discrepancy is real and worth knowing: the *hardware* FPU would happily produce
$\pm\infty$ for a nonzero numerator over a zero denominator and `nan` for `0/0`, which
is precisely the one-sided-limit answer. CPython intercepts the zero divisor in the
interpreter loop and raises `ZeroDivisionError` before the division is issued, so the
IEEE result never reaches your code. That is a deliberate language design choice: a
silent `inf` propagating through a numeric pipeline produces much harder-to-diagnose
bugs than an exception at the point of the mistake. (This is also why
`1.0/0.0` in NumPy behaves differently from `1.0/0.0` in pure Python — NumPy deliberately
routes straight to the hardware semantics and gives you `inf` with a warning.)

(c) The IEEE-754 answers must be requested by name, and one of them is
indeterminate: `inf - inf` is `nan`, and so is `inf * 0.0`. Just as $0/0$ has no
limit, $\infty - \infty$ has no value, and the machine reports `nan` rather than
guessing. Note the practical consequence: `nan` propagates silently through every
subsequent arithmetic operation, so a single indeterminate form buried in a long
pipeline will surface as a `nan` metric several layers away from the mistake.

</details>

**[ ] Exercise 7 — Challenge: prove the Babylonian iteration converges
*quadratically*, and reproduce the lesson's table from the error identity.** Let
$x_0 = 1$ and $x_{n+1} = \tfrac12\left(x_n + \frac{2}{x_n}\right)$, with $L = \sqrt{2}$.

(a) Prove the exact identity $x_{n+1} - L = \dfrac{(x_n - L)^2}{2x_n}$.
(b) Deduce the recurrence for the relative error $e_n = x_n/L - 1$, and show that
$e_{n+1} \approx e_n^2 / 2$ for small $e_n$.
(c) Using $L = \sqrt{2} = 1.414213562373095\ldots$, compute $e_0, \dots, e_5$ and
confirm numerically that each error is roughly the *square* of the previous one, not
merely smaller. Contrast with Exercise 4's proof, which only showed monotone bounded
convergence — what does (a) buy you that (c) in Exercise 4 does not?

<details>
<summary>Solution</summary>

(a) Substitute $2 = L^2$ and expand:

$$x_{n+1} - L = \frac{1}{2}\left(x_n + \frac{L^2}{x_n}\right) - L
= \frac{x_n^2 + L^2 - 2L x_n}{2x_n}
= \frac{(x_n - L)^2}{2x_n}.$$

The numerator is a perfect square, so it is $\ge 0$ for every $x_n$. Two consequences
drop out immediately:

- $x_{n+1} \ge L$ always, so the iterates sit at or above $\sqrt{2}$ and converge *from
  above* — a stronger statement than Exercise 4's "decreasing and bounded".
- The error $x_{n+1} - L$ is proportional to the *square* of the current error. This is
  **quadratic convergence**: doubling the number of correct digits squares the number of
  correct digits.

(b) Write $x_n = L(1 + e_n)$. Then $x_n - L = Le_n$ and $x_n = L(1+e_n)$, so

$$L e_{n+1} = \frac{L^2 e_n^2}{2L(1+e_n)} \implies
e_{n+1} = \frac{e_n^2}{2(1 + e_n)}.$$

For $\lvert e_n \rvert \ll 1$ the denominator is approximately $2$, giving
$e_{n+1} \approx e_n^2/2$. Each step squares the error.

(c) Computed in floating point:

```python
import math

L = math.sqrt(2)


def babylonian(x, steps):
    for _ in range(steps):
        x = 0.5 * (x + 2.0 / x)
    return x


print("Exact identity  x_{n+1} - L  ==  (x_n - L)^2 / (2 x_n) :")
x = 1.0
for k in range(6):
    nxt = babylonian(x, 1)
    lhs = nxt - L
    rhs = (x - L) ** 2 / (2.0 * x)
    print(f"  k={k}  x_k={x:.15f}  lhs={lhs:.6e}  rhs={rhs:.6e}  |diff|={abs(lhs - rhs):.3e}")
    x = nxt

print()
print("Relative error e_k = x_k / L - 1,  compared with e_{k-1}^2 / (2(1+e_{k-1})):")
x = 1.0
prev = x / L - 1.0
for k in range(6):
    e = x / L - 1.0
    pred = prev * prev / (2.0 * (1.0 + prev))
    print(f"  k={k}  e_k={e:+.12e}  predicted={pred:+.12e}")
    prev = e
    x = babylonian(x, 1)
```

Output:

```text
Exact identity  x_{n+1} - L  ==  (x_n - L)^2 / (2 x_n) :
  k=0  x_k=1.000000000000000  lhs=8.578644e-02  rhs=8.578644e-02  |diff|=1.388e-16
  k=1  x_k=1.500000000000000  lhs=2.453104e-03  rhs=2.453104e-03  |diff|=2.390e-16
  k=2  x_k=1.416666666666667  lhs=2.123901e-06  rhs=2.123901e-06  |diff|=2.356e-16
  k=3  x_k=1.414215686274510  lhs=1.594724e-12  rhs=1.594862e-12  |diff|=1.375e-16
  k=4  x_k=1.414213562374690  lhs=-2.220446e-16  rhs=8.991378e-25  |diff|=2.220e-16
  k=5  x_k=1.414213562373095  lhs=-2.220446e-16  rhs=1.743153e-32  |diff|=2.220e-16

Relative error e_k = x_k / L - 1,  compared with e_{k-1}^2 / (2(1+e_{k-1})):
  k=0  e_k=-2.928932188135e-01  predicted=+6.066017177982e-02
  k=1  e_k=+6.066017177982e-02  predicted=+6.066017177982e-02
  k=2  e_k=+1.734606680942e-03  predicted=+1.734606680942e-03
  k=3  e_k=+1.501825092731e-06  predicted=+1.501825092945e-06
  k=4  e_k=+1.127542503809e-12  predicted=+1.127737610914e-12
  k=5  e_k=-1.110223024625e-16  predicted=+6.356760489476e-25
```

Read the middle column: $-2.93\times10^{-1}$, then $+6.07\times10^{-2}$, then
$+1.73\times10^{-3}$, then $+1.50\times10^{-6}$, then $+1.13\times10^{-12}$, then
machine epsilon. Each is the *square* of its predecessor (up to the factor $1/2$): $(6.07\times10^{-2})^2 \approx 3.7\times10^{-3}$, and $e_2 \approx e_1^2/2$; $(1.73\times10^{-3})^2 \approx 3.0\times10^{-6}$, and $e_3 \approx e_2^2/2$. The predicted column agrees with the measured one to about 12 digits, so the recurrence in (b) is confirmed. Note the sign flip at $k=0 \to k=1$: $x_0 = 1 < \sqrt2$, and by (a) $x_1 \ge L$, so the very first step crosses over and everything after approaches from above.

**What (a) buys you.** Exercise 4(c) proved convergence: the sequence exists, is
monotone, is bounded, and therefore has a limit — and then identified the limit as
$\sqrt{2}$. That is a statement about the long run and says nothing about how many
iterations are needed. The error identity gives a *rate*, and a rate is what you need
in practice:

- It tells you when to stop. With relative error $e_{n+1} \approx e_n^2/2$, going from
  $10^{-3}$ to $10^{-15}$ takes 5 iterations, not 12.
- It tells you the method is *self-correcting*: the squaring is why Newton's method
  survives being started from a merely decent guess, while the fixed-step loop of
  Common Mistake 4 ($\lvert g'(L)\rvert \ge 1$) converges at best linearly and at worst
  not at all.
- It explains the printed table's stopping point. At $k = 5$ the identity predicts an
  error of order $10^{-25}$, which is below the $2.22\times10^{-16}$ resolution of a
  double; the iteration is then stuck at $\sqrt2$ because it has run out of
  significant digits, not because it has run out of accuracy. Any further step returns
  exactly `1.414213562373095` — the mathematical answer is already there and the
  machine simply cannot record a smaller error.

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

[51 — Derivatives](../part04_calculus/51_derivatives.md) turns the limit idea from "approach a point" into
"measure instantaneous rate of change", and shows that the chain rule is exactly the
mechanism behind backpropagation.