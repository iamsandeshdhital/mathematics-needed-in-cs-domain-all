# 00 — Why Mathematics Matters in Computer Science

**Part**: part00_orientation · **Prerequisites**: none · **Time**: 15 min

---

## In Plain Words

You already use mathematics every day. You just call it other things. When you
index a dictionary and it takes the same time whether the dictionary holds ten
items or ten million, you are using a result about how numbers spread out when
you hash them. When `0.1 + 0.2 != 0.3` in your code and you shrug and use
`math.isclose`, you are using the fact that most decimal fractions have no exact
representation in binary. When a neural network gets better at its job, it is
following a direction of steepest ascent that a graduate student had to work
out with a pencil.

This lesson is not an argument that you need mathematics to program. It is a
catalogue of the mathematics already running inside software you use, with real
numbers, so you can see it is not abstract. There are eight examples. Every one
of them has a runnable Python block below that produces the actual output.

## Why Computer Science Cares

**1. Why a hash map lookup costs the same at any size.** `dict.__getitem__` is
O(1) on average, and the reason is arithmetic: the interpreter computes a
numeric hash of your key, reduces it modulo the table size, and jumps to that
slot. It never walks the table. A `list` does walk it. Same data, different
mathematics, three orders of magnitude.

**2. Why `0.1 + 0.2 == 0.3` is `False`.** A Python float is a 64-bit binary
fraction, and 1/10 has no finite binary expansion. The exact stored value of
`0.1` is `3602879701896397/36028797018963968`. This is why invoice systems use
integer cents, why `Decimal` exists, and why the correct float comparison is
`math.isclose`, not `==`.

**3. Why a neural network trains.** Gradient descent. You compute a loss, take
its derivative with respect to every weight, and move each weight against that
derivative by a small learning rate. The derivative is calculus; the loop is a
`for`; the whole thing is about 20 lines, shown below.

**4. Why RSA works.** Fermat's little theorem, plus repeated squaring. The
encryption is `pow(message, e, n)` and the decryption is `pow(ciphertext, d, n)`.
Both are modular exponentiation, which is O(log e) multiplications by squaring
rather than O(e) multiplications by accumulation. That is why a 2048-bit RSA
operation takes microseconds.

**5. Why PCA works.** Principal component analysis finds the direction along
which your data varies most and projects onto it. "Direction of greatest
variance" is an eigenvector of the covariance matrix. [Lesson 40](../part03_linear_algebra/40_svd_and_pca.md)
derives it properly; the code below does the 2D case in twenty lines.

**6. Why quicksort's worst case is quadratic.** The partitioning cost is linear,
and the number of partitions is n, so the total is a summation of n terms. Write
the summation down and the complexity follows. That is
[Lesson 24](../part02_discrete_combinatorics/24_recurrence_relations.md).

**7. Why a distributed rate limiter needs a formula.** Token bucket and leaky
bucket are arithmetic on rates and capacities, and the correctness condition is
an inequality over time. See [Lesson 66](../part05_probability_statistics/66_common_distributions.md).

**8. Why test suites can be exhaustive in a way nobody believed.** Program
correctness is a logical statement, and a statement with finitely many cases can
be checked on all of them. Verification tools like Dafny and Frama-C use exactly
this: an invariant plus a machine-checked step. See
[Lesson 13](../part01_logic_proof/13_proof_techniques.md).

## The Formal Version

None yet. This lesson deliberately contains no definitions, because it is
persuasion rather than content. The first definitions in the course are in
[Lesson 10](../part01_logic_proof/10_propositions_and_connectives.md).

What we do use informally here are three ideas that get formal versions later:

**Big-O.** For functions `f` and `g`, we say `f(n) = O(g(n))` if there exist
constants `c > 0` and `n₀ > 0` such that `f(n) ≤ c · g(n)` for all `n ≥ n₀`.
The claim is about growth as `n` grows, not about absolute speed. Formal version:
[Lesson 80](../part06_algorithms_math/80_big_o_and_complexity.md).

**Modular arithmetic.** Integers modulo `m` are the integers with `m` columns, so
addition wraps around. `a ≡ b (mod m)` means `a` and `b` leave the same
remainder when divided by `m`. Formal version:
[Lesson 111](../part09_number_theory_crypto/111_modular_arithmetic_and_crypto.md).

**Variance.** For a set of numbers, variance is the average squared distance
from the mean. It is the single number that summarises spread. Formal version:
[Lesson 64](../part05_probability_statistics/64_expectation_variance.md).

## Formula Sheet

This lesson has no formal definitions of its own — it is a catalogue — but it
does use three ideas informally (big-O, modular arithmetic, variance) and a
handful of formulas in its code. Every one of them is here.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$f(n) = O(g(n))$` | `$\exists\, c>0,\ n_0>0:\ \forall n \ge n_0,\ f(n) \le c\,g(n)$` | $f$ never grows faster than a fixed multiple of $g$, once $n$ is past a fixed threshold | describing how a cost **scales**, never as a speed. The constants $c$ and $n_0$ may be enormous; the label is about growth only |
| `$a \equiv b \pmod m$` | `$m \mid (a - b)$` | $a$ and $b$ leave the same remainder when divided by $m$ | hash slots (`hash(k) % size`), RSA keys, calendars. Requires $m > 0$; for $m=1$ every pair is congruent, which is a vacuous claim |
| `$\varphi(n)$` | for $n = pq$ with distinct primes: `$\varphi(n) = (p-1)(q-1)$`, here `$= 3120$` | how many numbers from 1 to $n$ share no factor with $n$ | computing the RSA private exponent $d$. It is also why knowing $\varphi(n)$ is equivalent to knowing $p$ and $q$, which is why factoring $n$ breaks RSA |
| `$\gcd(m,n) = 1$` | `$\gcd$` is the greatest common divisor | $m$ and $n$ share no factor, so $m$ may be cancelled from a congruence | **checking the hypothesis of Euler's theorem before trusting the RSA proof** |
| Euler's theorem | `$m^{\varphi(n)} \equiv 1 \pmod n$` | raising $m$ to $\varphi(n)$ gives back 1, for any $m$ sharing no factor with $n$ | the step that makes RSA decryption return $m$. **Requires `$\gcd(m,n)=1$`**; without it the value is 0 on the offending prime, not 1 |
| `$\operatorname{modpow}(b,e,m)$` | square the base and halve the exponent each step: $\lceil \log_2 (e+1) \rceil$ steps | compute $b^e \bmod m$ without ever building $b^e$ | `pow(m, e, n)` in RSA. $e = 17$ needs 5 steps here; the count depends on the *bit length* of $e$, not its value |
| `$e \cdot d \equiv 1 \pmod{\varphi(n)}$` | `$17 \cdot 2753 = 46801 = 15 \cdot 3120 + 1$` | $d$ undoes $e$ | making the surplus powers of $m$ in $m^{ed}$ cancel against Euler's theorem |
| `$\sigma(z) = \dfrac{1}{1+e^{-z}}$` | $e$ here is Euler's number, not the exponent $e$ above | squashes any real number into the open interval from 0 to 1 | the logistic regression output layer. Note `$\sigma(0) = 0.5$` and `$\sigma(z) \to 1$` as $z \to +\infty$, but never equals 1 |
| `$\hat y_i = \sigma(\mathbf{w} \cdot \mathbf{x}_i + b)$` | | the model's predicted pass probability for student $i$ | the forward pass |
| `$L(\mathbf{w}, b) = \dfrac{1}{n}\sum_{i=1}^{n} (\hat y_i - y_i)^2$` | the $1/n$ is the mean; dropping it changes the gradient's scale, not its direction | one number that has to shrink for learning to be happening | printed every few epochs. Averaging matters: it makes $L$ comparable between datasets of different size |
| `$\mathbf{w} \leftarrow \mathbf{w} - \eta \nabla L$` | minus, not plus: we walk downhill | move every weight against the slope of the loss | the training loop. $\nabla L$ is the vector of partial derivatives of $L$ with respect to the weights |
| `$\eta$` (learning rate) | `0.05` in the lesson's run | the size of one step downhill | too small crawls; too large makes the predictions saturate at 0 and 1. There is no universally safe value |
| `$\bar{x} = \dfrac{1}{n}\sum_i x_i$` | `$(3.500,\ 5.160)$` for the five PCA points | the average point of the data | centring, so the axis of greatest spread passes through the origin |
| `$\operatorname{Var}(X) = \dfrac{1}{n}\sum_i (x_i - \bar x)^2$` | | average squared distance from the mean | the quantity PCA maximises. Population variance, so it divides by $n$, not $n-1$ |
| `$\Sigma = \begin{pmatrix} s_{xx} & s_{xy} \\ s_{xy} & s_{yy} \end{pmatrix} = \begin{pmatrix} 8.000 & 9.400 \\ 9.400 & 11.154 \end{pmatrix}` | `$s_{xy} = s_{yx}$`, so $\Sigma$ is symmetric | how the two axes spread, and how much they lean together | the input to PCA. A symmetric matrix is what makes one real principal direction exist per eigenvalue |
| `$\theta = \tfrac12\operatorname{atan2}(2s_{xy},\, s_{xx} - s_{yy})$` | `$\approx 49.76°$` | the angle of the direction of greatest spread, in 2D | doing 2D PCA with no linear-algebra library. `atan2(y, x)` is safe where `atan` would divide by zero when $s_{xx} = s_{yy}$ |
| `$\operatorname{proj}_v(x) = (x \cdot v)\,v$` | valid when `$\|v\| = 1$`; in general divide by `$v \cdot v$` | the part of $x$ that lies along direction $v$ | turning 2D points into the 1D numbers PCA outputs: `(1.00, 2.00) ↦ −4.027` |
| `$\lambda_1,\ \lambda_2$` | `$\lambda_{1,2} = \dfrac{s_{xx}+s_{yy} \pm \sqrt{(s_{xx}-s_{yy})^2 + 4s_{xy}^2}}{2}$` $\approx 19.109,\ 0.046$ | the two variances, along the two principal directions | computing PCA exactly in 2D; the bigger one is the direction to keep |
| `$\lambda_1 / (\lambda_1 + \lambda_2)$` | `99.8%` in the lesson | the fraction of variance that survives the projection | deciding whether PCA is worth doing at all. `50%` on data with equal spread in every direction |
| a finite binary float | `$x = \dfrac{m}{2^k}$` with `$m \in \mathbb{Z}$` | every finite float is a whole number over a power of two | explaining `0.1 + 0.2 != 0.3`. The stored `0.1` is `$\frac{3602879701896397}{2^{62}}$` |
| `$\dfrac{1}{10} = \dfrac{1}{2 \cdot 5}$` | no power of two has a factor of 5, so the binary expansion never terminates | why `0.1` is inexact at 64, 128 or 256 bits alike | choosing `Decimal`, `Fraction`, or integer minor units. Widening the format shrinks the error, it never removes it |
| `math.isclose(a, b, rel_tol, abs_tol)` | | compare two floats with a tolerance instead of `==` | the only safe way to test float equality |

## Worked Example

The most convincing example is the one you have probably already been bitten by.
Compute the way your instinct says, then compute the way the hardware says.

**Step 1. The instinct.** You have a shopping cart. The prices are `0.1`,
`0.2`, and `0.3`. You write:

```
total = 0.1 + 0.2
total == 0.3   # -> False
```

**Step 2. What the hardware actually stored.** `0.1` is not one tenth. It is the
nearest 64-bit binary fraction to one tenth, and it is slightly larger:

```
Fraction(0.1) = 3602879701896397 / 36028797018963968
```

That fraction equals `0.1000000000000000055511151231257827`. The nearest double
to `0.2` is `0.200000000000000011102230246251565`. Add them and you get
`0.3000000000000000444089209850062616`, and the nearest double to that is
`0.30000000000000004`. Not `0.3`. The stored value of `0.3` is
`0.299999999999999988897769753748`.

**Step 3. Why the addition is where it shows up.** Each individual value is off
by about 1 part in `10^17`. Two such errors accumulate into roughly
`4.4 × 10^-17`, which is more than one unit in the last place of `0.3`, so the
result rounds to the *next* double up rather than back to `0.3`.

**Step 4. The error is not always negligible.** The relative error here is tiny.
The absolute error is what accumulates. Add `0.01` a million times:

```
10000.000000171856
```

The invoice is wrong by about `1.7 × 10^-7`. Rounded to two decimal places it
looks fine, which is exactly what makes this bug dangerous: it passes the
eyeball test and fails an audit.

**Step 5. The fix.** Count in integer cents. `1_000_000 × 0.01` becomes
`1_000_000 × 1`, which is exactly `100000000`. No error is possible because every
value is representable. This is why `Decimal`, `Fraction`, and the
"store money as integer minor units" advice all exist.

## Runnable Code

### Hash map lookup versus list scan

```python
import gc
import time

# A dict answers by hashing the key and jumping to one slot.
# A list answers by walking from the front. One is flat, one grows linearly.
# Build the tables once so we are measuring lookups, not allocation.

KEYS = [f"key-{i}" for i in range(200_000)]
tables = []
for size in (1_000, 10_000, 100_000, 200_000):
    table = {k: i for i, k in enumerate(KEYS[:size])}
    tables.append((size, table, list(table.values()), table[KEYS[size - 1]]))

gc.collect()
gc.disable()                     # keep the collector out of the timing run
try:
    print(f"{'entries':>9} {'dict lookup':>16} {'list scan':>16} {'ratio':>9}")
    for size, table, values, wanted in tables:
        reps = max(3, 200_000 // size)

        t0 = time.perf_counter()
        for _ in range(reps):
            table[KEYS[size - 1]]
        dict_ns = (time.perf_counter() - t0) / reps * 1e9

        t0 = time.perf_counter()
        for _ in range(reps):
            values.index(wanted)      # scans from the front, like a linear search
        list_ns = (time.perf_counter() - t0) / reps * 1e9

        print(f"{size:>9} {dict_ns:>13.1f} ns {list_ns:>13.1f} ns {list_ns / dict_ns:>7.0f}x")
finally:
    gc.enable()

print()
print("The dict column barely moves. The list column grows in proportion to size.")
print("That flat column is what O(1) means. Lesson 80 makes the definition precise.")
```

### Floating point

```python
import math
from fractions import Fraction

print("== the famous one ==")
print(f"0.1 + 0.2              -> {0.1 + 0.2!r}")
print(f"(0.1 + 0.2) == 0.3     -> {(0.1 + 0.2) == 0.3}")
print(f"math.isclose(...)      -> {math.isclose(0.1 + 0.2, 0.3)}")

print()
print("== why: 0.1 has no exact binary form ==")
print(f"0.1 as an exact fraction -> {Fraction(0.1)}")
print(f"0.5 as an exact fraction -> {Fraction(0.5)}   <- binary fractions terminate")
print(f"0.2 as an exact fraction -> {Fraction(0.2)}")

print()
print("== the error is tiny, but the total is wrong ==")
total = 0.0
for _ in range(1_000_000):
    total += 0.01
error = total - 10000.0
print(f"1,000,000 additions of 0.01 -> {total!r}")
print(f"the exact answer              -> 10000.0")
print(f"error                        -> {error:+.10f}")

print()
print("== what to do instead ==")
print(f"count in integer cents        -> {100 * 1_000_000}")
exact = sum(Fraction(1, 100) for _ in range(1_000_000))
print(f"exact rational sum            -> {exact} = {float(exact)}")
```

### A neural network training, in twenty lines

```python
# Logistic regression: the smallest network that has real weights to learn.
# Features: hours studied, hours slept, prior grade, revision sessions.
# Label 1 means the student passed. The data is noisy on purpose, so the loss
# falls a long way and then flattens rather than hitting zero.

X = [
    (1.0, 9.0, 2.0, 0.0),   # studied little, slept plenty
    (2.0, 8.0, 4.0, 1.0),
    (3.0, 7.0, 6.0, 1.0),
    (8.0, 3.0, 8.0, 2.0),   # studied hard, slept badly
    (9.0, 2.0, 9.0, 3.0),
    (5.0, 5.0, 7.0, 2.0),
    (6.0, 4.0, 3.0, 1.0),
    (4.0, 6.0, 5.0, 0.0),
]
y = [0, 0, 0, 1, 1, 1, 1, 0]

n, d = len(X), len(X[0])
weights = [0.0] * d
bias = 0.0
LEARNING_RATE = 0.05
EPOCHS = 3000


def sigmoid(z: float) -> float:
    """Squash any real number into (0, 1) so it can be read as a probability."""
    return 1.0 / (1.0 + pow(2.718281828459045, -z))


def predict(features, w, b):
    z = b + sum(wi * fi for wi, fi in zip(w, features))
    return sigmoid(z)


def loss_of(w, b):
    """Mean squared error: one number that must fall for learning to happen."""
    return sum((predict(x, w, b) - t) ** 2 for x, t in zip(X, y)) / n


print("weights at start", [round(w, 4) for w in weights], "bias", round(bias, 4))
print("predictions at start", [round(predict(x, weights, bias), 3) for x in X])
print("loss at start      ", round(loss_of(weights, bias), 6))

print()
print("epoch      loss")
for epoch in range(1, EPOCHS + 1):
    # Forward pass: predict, then accumulate how wrong each prediction was.
    grad_w = [0.0] * d
    grad_b = 0.0
    for features, label in zip(X, y):
        err = predict(features, weights, bias) - label   # prediction minus truth
        for j in range(d):
            grad_w[j] += err * features[j]      # how much this input contributed
        grad_b += err

    # Backward pass: move each weight against the gradient, a little.
    for j in range(d):
        weights[j] -= LEARNING_RATE * grad_w[j] / n
    bias -= LEARNING_RATE * grad_b / n

    if epoch in (1, 2, 5, 10, 50, 200, 1000, 3000):
        print(f"{epoch:>5}  {loss_of(weights, bias):>10.6f}")

print()
print("final weights", [round(w, 3) for w in weights])
print("final bias   ", round(bias, 3))
final = [round(predict(x, weights, bias), 3) for x in X]
print("predictions  ", final)
print("labels       ", y)
correct = sum((p >= 0.5) == bool(t) for p, t in zip(final, y))
print(f"correct: {correct}/{n}")

print()
print("What the model learned, in plain English:")
for name, w in zip(("studied", "slept", "prior", "revision"), weights):
    direction = "more pushes toward pass" if w > 0 else "more pushes toward fail"
    print(f"  {name:<9} weight {w:+.3f}  ->  {direction}")
```

Output worth knowing: the loss falls from `0.25` to `0.000043`, all eight
predictions end up on the correct side of `0.5`, and the largest weight by far
is the one on *hours slept*, at `-2.411`. Hours slept is the feature that
predicts failure, and the model found that on its own.

### RSA in a dozen lines

```python
def mod_pow(base: int, exp: int, mod: int) -> int:
    """base**exp mod mod by repeated squaring: O(log exp) multiplications.

    pow(base, exp, mod) does exactly this in C. That is what you should call.
    """
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:                       # this bit of the exponent is set
            result = (result * base) % mod
        base = (base * base) % mod         # square, then halve the exponent
        exp >>= 1
    return result


# A tiny, insecure, real RSA key pair. p and q are the secret factors.
p, q = 61, 53
n = p * q                        # 3233: the public modulus
phi = (p - 1) * (q - 1)          # 3120: known only to the key owner
e = 17                           # public exponent, small on purpose
d = pow(e, -1, phi)              # private exponent: the inverse of e mod phi

print(f"p = {p}, q = {q}")
print(f"n = p*q   = {n}   <- public")
print(f"phi(n)    = {phi}   <- secret")
print(f"e = {e}, d = {d}")
print(f"sanity check: (e*d) mod phi = {(e * d) % phi}")

print()
print("encrypt with e, decrypt with d, and you get the original back:")
for message in (2, 65, 1234, n - 1):
    encrypted = mod_pow(message, e, n)
    decrypted = mod_pow(encrypted, d, n)
    print(f"  m = {message:<5}  ->  c = {encrypted:<5}  ->  m' = {decrypted:<5}"
          f"   ok: {decrypted == message}")

print()
print("The entire security claim is one sentence of arithmetic:")
print("  c^d = (m^e)^d = m^(e*d) = m^(1 + k*phi(n)) = m, all mod n,")
print("  because m^phi(n) = 1 (mod n) by Euler's theorem, so the extra")
print("  k*phi(n) powers of m cancel out.")
print()
print(f"Factoring is what breaks it. n = {n} factors by hand in seconds.")
print(f"Trying every divisor up to sqrt({n}) = {int(n ** 0.5)} is the whole attack.")
print()
print("Why repeated squaring rather than m**e:")
print(f"  exponent e = {e} needs {e} multiplications done naively")
print(f"  repeated squaring needs {e.bit_length()} steps")
print("  for a real 2048-bit modulus the naive route needs about 2^2048 operations")
print("  repeated squaring needs 2048 steps regardless, so RSA-2048 is fast")
```

### PCA on two dimensions

```python
import math

# Five 2D points, clearly stretched along a diagonal with almost no spread across it.
points = [(1.0, 2.0), (2.0, 3.1), (2.5, 4.0), (3.0, 5.2), (9.0, 11.5)]
n = len(points)

# Step 1: centre the data. Subtracting the mean does not change its shape, it
# just moves it so the axis of greatest spread passes through the origin.
mx = sum(x for x, y in points) / n
my = sum(y for x, y in points) / n
centred = [(x - mx, y - my) for x, y in points]
print(f"mean = ({mx:.3f}, {my:.3f})")

# Step 2: the covariance matrix. Diagonal entries are spread along each axis;
# the off-diagonal entry is how much the axes lean together.
sxx = sum(x * x for x, y in centred) / n
syy = sum(y * y for x, y in centred) / n
sxy = sum(x * y for x, y in centred) / n
print()
print("covariance matrix:")
print(f"  [ {sxx:6.3f}  {sxy:6.3f} ]")
print(f"  [ {sxy:6.3f}  {syy:6.3f} ]")


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


# Step 3: for a 2x2 symmetric matrix the principal direction is analytic.
# tan(2*theta) = 2*sxy / (sxx - syy), and theta is half of that angle.
theta = 0.5 * math.atan2(2 * sxy, sxx - syy)
v1 = (math.cos(theta), math.sin(theta))      # direction of greatest spread
v2 = (-math.sin(theta), math.cos(theta))     # the direction about to be dropped


def spread_along(v):
    """Project every centred point onto v, then take the variance of the results."""
    projections = [dot(c, v) for c in centred]
    mean_p = sum(projections) / n
    return sum((p - mean_p) ** 2 for p in projections) / n


total = spread_along((1.0, 0.0)) + spread_along((0.0, 1.0))
kept = spread_along(v1)
print()
print(f"principal direction v1 = ({v1[0]:.4f}, {v1[1]:.4f})")
print(f"discarded direction v2 = ({v2[0]:.4f}, {v2[1]:.4f})")
print(f"v1 is perpendicular to v2: {abs(dot(v1, v2)) < 1e-12}")
print()
print(f"total variance              {total:.3f}")
print(f"variance kept along v1      {kept:.3f}")
print(f"variance thrown away in v2  {spread_along(v2):.3f}")
print(f"information kept: {kept / total * 100:.1f}%")

# Step 4: project to one dimension. That is the entire "compression".
print()
print("projected onto v1, the 1D PCA representation:")
for original, (cx, cy) in zip(points, centred):
    print(f"  ({original[0]:>5.2f}, {original[1]:>5.2f})  ->  {dot((cx, cy), v1):>7.3f}")

print()
print("Five 2D points became five numbers and 99.8% of the structure survived.")
print("That is PCA: project onto the directions of greatest spread, drop the rest.")
```

## Common Mistakes

**Wrong: "I do not need mathematics, I can look it up when I need it."**
Right: you can look up *which* algorithm to use, but not whether it is correct
or whether the constants in it are right. The RSA example above is 12 lines of
arithmetic that you must understand to know why `n` must be secret and `e` must
not be. Look-up gets you to the door; the mathematics is what tells you whether
the room is safe.
Why the wrong version is tempting: it worked for years. It stops working the
first time you need to debug a numerical issue, review a paper, or convince
someone that an algorithm is correct.

**Wrong: "Big-O is how fast something is in milliseconds."**
Right: big-O is a growth rate. An `O(n²)` algorithm can be faster than an
`O(n)` algorithm for every input you will ever run, because the constant factor
can differ by a million. The claim only becomes meaningful for inputs large
enough that the exponent wins, and proving an input is "large enough" is a real
part of the analysis.
Why tempting: people write "this is O(n) fast" after a quick benchmark on small
input, and benchmarks on small input measure the constant, not the rate.

**Wrong: "Floating point failure is a Python bug."**
Right: it is a property of binary floating point in every language. Java,
JavaScript, C and Rust all have it, because IEEE 754 mandates the format. It is
in fact extremely hard to avoid: you would have to give up the hardware.
Why tempting: the surprise is that a language designed by a numerical
mathematician still has it.

**Wrong: "PCA is compression, so it is lossless."**
Right: PCA discards the direction of least variance, which is the right choice
only when that direction carries little information. On data where the smallest
variance direction is the one you care about, PCA destroys the signal. In the
example above 99.8% survives; on a dataset with equal spread in every direction
you would keep 50% and lose half the data by throwing away half the axes.
Why tempting: "keep the important stuff" is easy to believe and easy to get
backwards.

**Wrong: "The proof is optional in an engineering course."**
Right: a proof is a guarantee that holds for every input, forever, checked once.
Testing checks finitely many inputs chosen by you. Every catastrophic bug you
have shipped was a case where testing missed something a proof would have
excluded, or where nobody wrote the specification precisely enough to prove
anything. See [Lesson 13](../part01_logic_proof/13_proof_techniques.md).
## Multiple Choice Questions

**Q1.** A Python `float` is a 64-bit binary floating point number. Which exact
value does the machine actually store when you write the literal `0.1`?

- A) $1/10$ exactly, because that is the value the decimal literal denotes
- B) $\frac{3602879701896397}{36028797018963968}$, the closest 64-bit binary fraction to $1/10$
- C) $2^{-55}$, the power of two that lies nearest to $1/10$
- D) $\frac{3602879701896397}{36028797018963968}$ plus $10^{-18}$, to make up for the rounding

<details>
<summary>Answer and explanation</summary>

**B) $\frac{3602879701896397}{36028797018963968}$, the closest 64-bit binary fraction to $1/10$.**

Writing `0.1` tells the interpreter "the rational number one tenth". Since no
64-bit binary fraction equals one tenth, the hardware stores the *nearest* one
instead, and the lesson prints that fraction.

A is the misconception that a decimal literal is stored as a decimal. The
stored quantity is a binary fraction, and the conversion rounds. The true error
is about $5.55 \times 10^{-18}$ and the stored value is slightly **above** $1/10$,
so `0.1 + 0.2` overshoots.

C confuses a finite binary fraction with a power of two. Every finite binary
fraction has the form $m/2^k$, but the numerator $m$ need not be 1 — here it is
the odd number 3602879701896397. $2^{-55}$ is about $2.8 \times 10^{-17}$, nowhere
near a tenth.

D is a "correction factor" that hardware does not apply. Rounding goes to the
nearest representable value, not to that value plus a fudge, and the direction of
the error here is upward by $5.55 \times 10^{-18}$, not downward.

</details>

**Q2.** The lesson adds `0.01` to a float one million times and ends with
`10000.000000171856`. Which explanation is correct?

- A) One million is too large to be held exactly in a double, so the loop corrupts its own counter
- B) Each `0.01` is a rounded binary fraction a little larger than one hundredth, and a million copies of that bias accumulate in the same direction
- C) Python rounds the running total to two decimal places on every iteration, to match the way it prints
- D) `0.01` is exactly representable in binary, so the error is introduced by the `+=` operation rounding the sum

<details>
<summary>Answer and explanation</summary>

**B) Each `0.01` is a rounded binary fraction a little larger than one hundredth, and a million copies of that bias accumulate in the same direction.**

`Fraction(0.01)` is `5764607523034235/576460752303423488`, which exceeds $1/100$
by about $2.08 \times 10^{-19}$. Multiply that by $10^6$ and you get
$2.08 \times 10^{-13}$; the observed error is larger because rounding of the
*running total* adds a second, order-dependent contribution. The signature is
one-signed drift: the total is too high and stays too high.

A is wrong because $10^6$ is exactly representable in a double — any integer
below $2^{53}$ is. The loop variable is not the problem.

C is wrong because Python never rounds to display precision. `repr` and `str`
choose a *shortest string that round-trips*; they do not modify the stored
value. `repr(total)` printing seventeen digits is a display decision.

D is the tempting one, and it is wrong in its premise. `0.01` is **not**
exactly representable: the denominator `576460752303423488` is $2^{59}$ and the
numerator is odd, so no cancellation happens. The lesson's own code makes this
point by showing that `0.5` is exactly $1/2$ while `0.2` is not. Note that
addition of two doubles is also not the culprit in the sense of an extra
rounding step per operation: rounding does happen there, but the error already
exists in the literals.

</details>

**Q3.** In the lesson's logistic regression the final weights are approximately
`(1.977, −2.411, 0.476, 1.718)` for *studied, slept, prior, revision*. What does
the size of the *slept* weight support, and what does it not support?

- A) That hours slept has the largest variance of the four features
- B) That hours slept is the strongest single separator of pass from fail in this eight-row training set, and nothing at all about causation
- C) That hours studied has no effect on passing, because its weight is smaller
- D) That the model is overfitting, because the largest weight belongs to a feature that should be irrelevant

<details>
<summary>Answer and explanation</summary>

**B) That hours slept is the strongest single separator of pass from fail in this eight-row training set, and nothing at all about causation.**

In a linear model a weight says how much the log-odds move per unit of that
feature, holding the others fixed. `−2.411` means one more hour of sleep pushes
the log-odds of passing down by 2.411, the largest single move in the vector.

A confuses a weight with a feature's spread. Weight magnitude is a property of
how the model uses the feature, not of how the feature varies in the data. (All
four features here happen to be on similar numeric ranges, so the comparison is
at least fair, but it is not measuring variance.)

C is a classic misreading of a multi-variable model. The four features are
correlated in this dataset, so the weights are not independent contributions
that can be ranked and then discarded. `studied` at `1.977` is not zero, and its
effect is conditional on the other three features holding still.

D is not what overfitting looks like. Overfitting is a low training loss paired
with a high loss on unseen data. A single large weight is a statement about the
data's geometry, and here the causal reading is wrong anyway: sleeping badly
predicts failure in this sample, and that is a correlation in eight rows.

</details>

**Q4.** The RSA block reports that the exponent `e = 17` needs 5 steps of
repeated squaring. Why does a 2048-bit RSA exponent not have the same problem?

- A) It does have it: a 2048-bit exponent means roughly $2^{2048}$ multiplications, so RSA-2048 would be unusable
- B) It does not: the number of steps is proportional to the *bit length* of the exponent, so a 2048-bit exponent costs about 2048 steps however large its value
- C) It does not, because `pow` builds a precomputed table of all 2048 possible residues once and reuses it
- D) It does not, because modular exponentiation is constant-time on modern hardware

<details>
<summary>Answer and explanation</summary>

**B) It does not: the number of steps is proportional to the *bit length* of the exponent, so a 2048-bit exponent costs about 2048 steps however large its value.**

Repeated squaring reads the exponent in binary, one bit per step. `17` is
`10001` in binary, hence 5 steps. A 2048-bit exponent is 2048 bits long, hence
about 2048 steps. The number of steps is a function of how many *bits* the
exponent needs to be written down, not of its magnitude — which is exactly why
`$e.bit_length()$` is the line of code the lesson prints.

A is the naive-accumulation cost, and it is the reason repeated squaring exists.
`base ** exp % mod` on a huge exponent would also have to build a number with
$e \cdot 2048$ bits, which is a memory problem as well as a time one.

C is invented. CPython's three-argument `pow` uses a sliding-window
multiplication in C, but no table of residues, and no precomputation survives
between calls.

D is irrelevant and backwards. Modern hardware makes each modular
multiplication fast; it does not change how many of them are needed. The
security claim and the speed claim are independent: RSA-2048 is *hard to break*
and *fast to compute* for the same underlying reason, that the private exponent
is a 2048-bit number.

</details>

**Q5.** The key pair uses $e = 17$, $\varphi(n) = 3120$ and $d = 2753$. Why must
$d$ be the inverse of $e$ **modulo $\varphi(n)$** rather than, say,
$\varphi(n) - e$?

- A) Because $\varphi(n) - e$ is negative and `pow` refuses negative exponents
- B) Because $e \cdot d \equiv 1 \pmod{\varphi(n)}$ is exactly what makes the surplus powers of $m$ in $m^{ed}$ cancel against Euler's theorem
- C) Because $e$ and $d$ must each be coprime to $n$ itself
- D) Because $d$ must be smaller than $n$ so that `mod_pow` terminates in reasonable time

<details>
<summary>Answer and explanation</summary>

**B) Because $e \cdot d \equiv 1 \pmod{\varphi(n)}$ is exactly what makes the surplus powers of $m$ in $m^{ed}$ cancel against Euler's theorem.**

Decryption computes $c^d = (m^e)^d = m^{ed}$. We need this to equal $m$, which
happens when $ed = 1 + k\varphi(n)$ for some integer $k$, because then
$m^{ed} = m \cdot (m^{\varphi(n)})^k \equiv m \cdot 1^k = m$. Here
$17 \cdot 2753 = 46801 = 15 \cdot 3120 + 1$, so $k = 15$ and the cancellation is
legal. That is the whole reason $d$ exists and the whole reason the key owner
needs $\varphi(n)$.

A is arithmetic nonsense: $\varphi(n) - e = 3103$, comfortably positive. And the
constraint is not a Python one.

C is a true-looking but irrelevant fact. $\gcd(2753, 3233) = 1$ does hold, but
it is not the design requirement. If the condition were only coprimality to $n$,
you could pick many values of $d$ that do not decrypt anything.

D confuses a consequence with a cause. $d < \varphi(n) < n$ does hold here
because $d$ is reduced modulo $\varphi(n)$, but the *reason* to reduce it modulo
$\varphi(n)$ is the congruence in B, not any size constraint on the loop.

</details>

**Q6.** Euler's theorem says $m^{\varphi(n)} \equiv 1 \pmod n$ when
$\gcd(m, n) = 1$. What exactly goes wrong when $\gcd(m, n) \ne 1$?

- A) Nothing goes wrong; the theorem holds for every integer $m$
- B) The value $m^{\varphi(n)}$ is not $1$ modulo $n$, so the step that cancels the surplus powers is an illegal inference
- C) The encryption step fails, so the ciphertext is no longer an integer
- D) $\varphi(n)$ is undefined unless $\gcd(m, n) = 1$

<details>
<summary>Answer and explanation</summary>

**B) The value $m^{\varphi(n)}$ is not $1$ modulo $n$, so the step that cancels the surplus powers is an illegal inference.**

Take $m = 61$ with $n = 3233 = 61 \cdot 53$. Then $61^{3120} \equiv 0 \pmod{61}$
— it is $0$, not $1$. Writing $m^{ed} = m \cdot (m^{\varphi(n)})^{15}$ and then
replacing the bracket by $1$ is the invalid move. The proof simply does not
apply outside its hypothesis, which is why the lesson's Challenge asks about
non-coprime messages at all.

A is the exact misconception this question is built to catch. The theorem has a
hypothesis, and "the theorem always holds" is the kind of belief that turns a
missing hypothesis into a security bug.

C is wrong because modular exponentiation is well defined for every
non-negative exponent and every positive modulus, coprime or not.
`mod_pow(53, 17, 3233)` returns a perfectly good integer.

D is wrong because $\varphi(n)$ counts residues coprime to $n$ and is defined for
every positive $n$; it is Euler's *congruence* that needs the hypothesis, not the
function.

</details>

**Q7.** The PCA example keeps 99.8% of the variance along one direction. Suppose
your data were instead a perfect circle, with exactly equal spread in every
direction. How much would one-dimensional PCA keep?

- A) About 100%, because a circle is symmetric so no direction deserves to be preferred
- B) Exactly 50%: PCA keeps the single largest of two equal variances
- C) 0%, because a circle has no principal direction at all
- D) 75%, because the two diagonal directions are each counted twice

<details>
<summary>Answer and explanation</summary>

**B) Exactly 50%: PCA keeps the single largest of two equal variances.**

For a unit circle centred at the origin the covariance matrix is
`[[0.5, 0.0], [0.0, 0.5]]`, so both eigenvalues are $0.5$, and the kept fraction
is `0.5 / (0.5 + 0.5) = 50%`. The lesson's own Common Mistakes section makes
this point: on data with equal spread in every direction you keep half the axes
and throw away the other half. Half the structure really does go.

A is the intuition that PCA is a "rotation", so nothing is lost. PCA is a
rotation *followed by* a projection, and the projection is the lossy part. A
rotation alone would keep 100% by definition.

C is wrong because a circle has principal directions, infinitely many of them.
Every direction is an eigenvector with eigenvalue $0.5$. The eigenvectors are not
missing; they are indistinguishable, so there is no basis for preferring one.

D has no derivation behind it. The two directions are orthogonal, not
double-counted, and the two variances sum to the total, so the kept fraction is
one of two equal halves.

</details>

**Q8.** A colleague benchmarks an $O(n^2)$ sort against an $O(n \log n)$ sort and
finds the "worse" one faster on every input up to $n = 10^6$. Which statement is
correct?

- A) The benchmark has established that the $O(n^2)$ sort has the better growth rate
- B) The benchmark is measuring the constant factor; the crossover point simply lies past $10^6$
- C) Big-O labels are unreliable and should be ignored when choosing an implementation
- D) The two timings cannot be compared because the sorts must use different amounts of memory

<details>
<summary>Answer and explanation</summary>

**B) The benchmark is measuring the constant factor; the crossover point simply lies past $10^6$.**

The $O$ label bounds growth: there exist constants $c$ and $n_0$ with
$f(n) \le c\,g(n)$ for $n \ge n_0$. Nothing says $c$ is small. An insertion sort
with a good constant beats merge sort on thousands of elements and loses to it on
hundreds of millions. The two statements — "$O(n^2)$ is asymptotically worse" and
"this implementation is faster today" — are both true and not in conflict.

A is the misconception the lesson's second Common Mistake targets head-on: the
asymptotic label is about the limit, and a benchmark cannot see the limit.

C over-corrects. Big-O is exactly the right tool for the question benchmarks
cannot answer: what happens when the input is ten times bigger.

D confuses two independent axes. A merge sort uses $O(n)$ auxiliary space and an
in-place variant does not; memory and time complexity are separate questions,
and the benchmark compared two programs on the same machine.

</details>

**Q9.** The lesson's Challenge shows that the message $m = n = 3233$ encrypts
to $0$ and decrypts back to $0$. Why is that a failure even though the
arithmetic never raised an error?

- A) It is not a failure: RSA permutes the residue classes mod $n$, and $0$ is the correct image of $0$
- B) The round trip returns a value that is not the message, so the information is destroyed; the coprimality hypothesis of the proof is what fails
- C) `mod_pow` overflows silently for inputs close to $n$
- D) $0$ cannot be represented in the message range, so the code raises on decryption

<details>
<summary>Answer and explanation</summary>

**B) The round trip returns a value that is not the message, so the information is destroyed; the coprimality hypothesis of the proof is what fails.**

$3233 \equiv 0 \pmod{3233}$, so encrypting gives $0$, and $0^d = 0$. The
function ran, returned integers, and lost the message. This is the worst shape of
bug: a success that is not one. The lesson's Challenge notes that $m = 53$ and
$m = 61$ also round-trip, but only by luck — for those the residue is $0$ on one
prime factor and Euler still applies on the other.

A is a real and instructive confusion. Textbook RSA *is* a permutation of
$\mathbb{Z}/n\mathbb{Z}$, and $3233$ and $0$ are the same residue class. The
point of A is that the scheme was defined on residues and used on integers, and
the integers run out of the residue system's range. That gap is exactly what
padding closes.

C is wrong: the loop reduces modulo $n$ on every multiplication, so no value
approaches $2^{2048}$.

D is wrong: `mod_pow` returns $0$ without complaint. The failure is silent,
which is the point of the exercise.

</details>

**Q10.** The lesson says a proof is a stronger guarantee than a test suite. Which
statement makes that comparison precise?

- A) A proof examines more cases than a test can, so it necessarily finds more bugs
- B) A proof establishes the claim for every input allowed by the specification; a test establishes it only for the inputs someone chose, and every unchosen input is unconstrained
- C) A proof runs faster than the test suite it replaces, which is the practical reason to prefer it
- D) A proof removes the need to run the program at all

<details>
<summary>Answer and explanation</summary>

**B) A proof establishes the claim for every input allowed by the specification; a test establishes it only for the inputs someone chose, and every unchosen input is unconstrained.**

A proof reasons from a specification, so it quantifies universally. A test
evaluates a finite list of points, so it establishes whatever those points happen
to exercise. The gap is not about effort or coverage; it is about the difference
between a universal and an existential claim. The lesson makes the same point in
its fifth Common Mistake: a proof is checked once and holds forever, and a test
is only as good as the imagination behind it.

A is wrong in an important way. A proof is not a bigger search — it finds no
bugs at all. It either establishes the claim or it does not, and the value is in
the second possibility being excluded by reasoning rather than by luck.

C is false: proofs are checked by a human or a kernel, and machine-checked
proofs (Dafny, Frama-C, Lean, Coq) can take hours. Speed is a tooling
convenience, not a mathematical advantage.

D is false and dangerous. A proof guarantees the *specification* is met, which is
only useful if the specification is right, and only if the code is the thing you
proved. Both failures — a wrong specification, a divergence between proof and
build — are ordinary, and no proof catches either.

</details>

## Subjective Questions

### Short Answer

**Q1. Give the exact rational value a Python `float` stores for `0.1`, its
denominator as a power of two, and the size of the error.**

<details>
<summary>Answer</summary>

`Fraction(0.1)` is `3602879701896397/36028797018963968`, and the denominator is
exactly $2^{62}$. The stored value is $1/10 + 5.551115123125783 \times 10^{-18}$,
i.e. slightly **above** one tenth — about 1 part in $10^{17}$ — which is why
adding the stored `0.2` overshoots the stored `0.3`. The information about $1/10$
was destroyed at the moment of assignment, not at any later conversion: once the
value is a double, `float(Fraction(0.1))` returns that same double.

</details>

**Q2. State, in one sentence each, what "modular" means when the lesson uses it
for hash-table slots and for RSA keys.**

<details>
<summary>Answer</summary>

For a hash table, modular means `hash(key) % size`: the slot is the remainder
when the key's integer hash is divided by the table size, so the number of slots
bounds the number of places to look.

For RSA it means every operation is arithmetic *modulo* $n$: $a \equiv b \pmod n$
holds exactly when $n$ divides $a - b$, and all the exponentiation is done in
those residue classes, so encrypting is `pow(m, e, n)` and decrypting is
`pow(c, d, n)`.

</details>

**Q3. Write the sigmoid, the loss, and the weight update used in the lesson's
logistic regression.**

<details>
<summary>Answer</summary>

`$\sigma(z) = 1/(1+e^{-z})$` with $\sigma(0) = 1/2$, so the prediction for
student $i$ is `$\hat y_i = \sigma(\mathbf{w} \cdot \mathbf{x}_i + b)`.

The loss is the mean squared error
`$L(\mathbf{w},b) = \frac{1}{n}\sum_i (\hat y_i - y_i)^2$`.

The update moves every weight against the gradient:
`$\mathbf{w} \leftarrow \mathbf{w} - \eta \nabla L$`, and the bias the same way,
with `$\eta = 0.05$`. The minus sign is what "descent" means — the loss must go
down.

</details>

**Q4. In the lesson's RSA example, name $p$, $q$, $n$, $\varphi(n)$, $e$ and $d$,
and say which of them are public.**

<details>
<summary>Answer</summary>

$p = 61$ and $q = 53$ are the secret primes. $n = pq = 3233$ is the public
modulus. $\varphi(n) = (p-1)(q-1) = 3120$ is secret — knowing it is equivalent to
knowing $p$ and $q$. $e = 17$ is the public encryption exponent, and
$d = 2753$ is the private decryption exponent, defined by
$e\,d \equiv 1 \pmod{\varphi(n)}$.

</details>

**Q5. What are the four features in the logistic regression, roughly what is the
final weight vector, and which feature dominates?**

<details>
<summary>Answer</summary>

The features are hours studied, hours slept, prior grade, and revision sessions;
the label is whether the student passed. The final weights are approximately
`(1.977, −2.411, 0.476, 1.718)` with bias about `−0.048`.

Hours slept dominates by magnitude. Its weight is negative, so more sleep pushes
toward failure in this sample. The model found that on its own, from eight rows,
with no feature engineering.

</details>

**Q6. Say in plain words what "$f(n) = O(g(n))$" asserts, and say what it does
not assert.**

<details>
<summary>Answer</summary>

It asserts that past some threshold size $n_0$, $f(n)$ never exceeds a fixed
constant multiple of $g(n)$. The threshold and the constant are part of the claim
and may be enormous.

It does not assert that $f$ is fast in milliseconds, nor that $f$ is bounded
below by $g$, nor that $f$ is *equal* to a constant times $g$. Two functions can
both be $O(n)$ while one is a thousand times slower at every size.

</details>

### Long Answer

**Q1. Why is `0.1 + 0.2 != 0.3` a property of the number format rather than a bug
in Python — and what exactly would you have to give up to make the comparison
come out right?**

<details>
<summary>Model answer</summary>

It is a property of the format. IEEE 754 binary floating point stores a value as
a whole number over a power of two: $x = m/2^k$. One tenth reduces to
$1/(2 \cdot 5)$, and no power of two contains a factor of $5$, so $1/10$ has no
finite binary expansion and cannot be stored. The hardware therefore stores the
nearest double, which is *above* $1/10$ by $5.55 \times 10^{-18}$; the nearest
double to $0.2$ is also above, and the two errors add to more than one unit in
the last place of the result, so the sum rounds to `0.30000000000000004` while the
literal `0.3` is stored as a double *below* $0.3$.

Nothing about this is Python's fault. Java, JavaScript, C, C++ and Rust all
reproduce it because the standard mandates the format. The mistake is not in the
arithmetic but in the assumption that a decimal literal denotes the rational it
looks like.

To make the comparison come out right you must stop using binary floating point
for the quantity. In increasing order of inconvenience: compare with a tolerance
(`math.isclose(0.1 + 0.2, 0.3)`, true); store money as an integer number of minor
units, so `1_000_000 * 1` instead of `1_000_000 * 0.01`, which is exactly
`100000000`; use `Decimal`, which stores decimal digits and tracks a precision;
use `fractions.Fraction`, which stores a rational exactly and is exact but slow
and memory-hungry.

What you give up in the first case is a guarantee — a tolerance hides real
errors — and in the second and third, the raw speed and compactness of hardware
floating point, which is precisely what makes it the default. Widening to 128 or
256 bits is not on the list, because it shrinks the error by a factor and never
removes it: the factor of $5$ is still there.

</details>

**Q2. Why can no learning rate between 0.05 and 3.0 make this training run blow
up, and what does the fact that the loss *can* be driven to zero tell you about
using training loss as a signal of model quality?**

<details>
<summary>Model answer</summary>

The reason is the shape of the sigmoid. `$\sigma(z) = 1/(1+e^{-z})$` has
derivative `$\sigma'(z) = \sigma(z)(1 - \sigma(z))$`, which is at most $1/4$ and
tends to $0$ as $|z|$ grows. So the gradient the loop uses — the summed
prediction-minus-label times the input — *shrinks* exactly when a weight becomes
large enough to be making big mistakes. A big step early pushes the weights far
out, but once they are far out the sigmoid saturates, the predictions are pinned
at 0 and 1, the residual vanishes, and the gradient with it. The loop settles
into a minimum rather than oscillating. Empirically: at `$\eta = 3.0` the loss
reaches about $8 \times 10^{-8}$ while the weights grow to roughly
`(9.7, −11.8, 4.2, 3.9)`.

That last number is the lesson. A loss of essentially zero came with weights
roughly five times larger than the lesson's headline run, and predictions like
`1.1e-05` for a student who failed. The model is not better; it is more
confident. Saturated outputs carry no information about how close a borderline
case is to the boundary, so a near-zero training loss says the model has
*memorised* the eight rows, not that it generalises.

The practical consequences: report training and held-out loss together, and treat
a gap between them as the real measurement; watch the weight magnitudes, because
they grow while the loss flattens; and prefer a loss with a bounded gradient
(cross-entropy rather than squared error) when saturation is a concern. The
concrete failure this prevents is shipping a classifier that is confidently wrong
on inputs near the decision boundary — exactly the inputs a human reviewer would
escalate.

</details>

**Q3. Write out the whole arithmetic chain that makes
`pow(pow(m, 17, 3233), 2753, 3233) == m mod 3233`, name every hypothesis you
used, and say what breaks and what real implementations do about it.**

<details>
<summary>Model answer</summary>

**The chain.** With $n = 3233 = 61 \cdot 53$, $\varphi(n) = (61-1)(53-1) =
3120$, and $d$ chosen so that $17 \cdot 2753 = 46801 = 15 \cdot 3120 + 1$, i.e.
$e\,d \equiv 1 \pmod{\varphi(n)}$:

1. $c \equiv m^{e} \pmod n$ by definition of encryption.
2. $c^{d} \equiv (m^{e})^{d} = m^{e\,d} \pmod n$ — the binomial law
   $(x^{a})^{b} = x^{ab}$ in the residue ring.
3. $m^{e\,d} = m^{1 + 15\varphi(n)} = m \cdot \left(m^{\varphi(n)}\right)^{15}$.
4. $m^{\varphi(n)} \equiv 1 \pmod n$ by Euler's theorem.
5. Therefore $c^{d} \equiv m \cdot 1^{15} = m \pmod n$.

**The hypotheses.** Euler's theorem needs $\gcd(m, n) = 1$ — that is the *only*
non-trivial hypothesis, and the ring arithmetic in steps 2 and 5 is otherwise
unconditional. Euler's theorem itself rests on Fermat's little theorem applied
to each prime factor and recombined by the Chinese Remainder Theorem, which needs
$n = pq$ with $p \ne q$ prime.

**What breaks.** Without coprimality, step 4 is false. For $m = 61$ and $n =
3233$, $61^{3120} \equiv 0 \pmod{61}$, not $1$, and the cancellation in step 3
has nothing to cancel against. The message $m = n$ is worse: it encrypts to $0$
and stays there, so the round trip is arithmetically fine and informationally
fatal. A sweep of all 3233 residues does happen to round-trip, but the 113
messages divisible by 61 or 53 do so for the wrong reason — $0$ on one prime
factor, Euler on the other, glued back by CRT. They are safe by accident of
algebra, not by permission of the theorem.

**What real implementations do.** They never encrypt a bare integer. PKCS#1 v1.5
prepends random nonzero bytes, and OAEP prepends structured random bytes, which
restores the coprimality the proof needed and simultaneously destroys two
textbook-RSA weaknesses. Encrypting the same message twice gives the same
ciphertext, so an attacker sees repeats; and textbook RSA is multiplicative,
`$\mathrm{enc}(m_1 m_2) = \mathrm{enc}(m_1)\,\mathrm{enc}(m_2)$`, so chosen
plaintexts recover factors. Random padding kills both. The lesson's
`mod_pow` and this argument together are the entire security claim of RSA, and
the entire attack surface: the proof holds on the padded message, and only on the
padded message.

</details>

**Q4. The five-point PCA example keeps 99.8% of the variance. Explain why the
projection is still lossy in principle, and describe a dataset where the lost
0.2% is the part you care about.**

<details>
<summary>Model answer</summary>

It is lossy because the projection *discards a coordinate*. Keeping only $v_1$
maps each point to the single number $\mathbf{x} \cdot v_1$. Two distinct points
with the same projection land on the same output, and no amount of care in
choosing $v_1$ prevents that. Here the discarded coordinate is
$\mathbf{x} \cdot v_2$ with $v_2 = (-0.7634, 0.646)$, whose variance is $0.046$
against a kept variance of $19.109$.

The number $99.8\%$ measures *variance*, not information, and variance is a
weighted sum of squared distances from the mean. A direction can carry almost no
variance and still carry the entire signal, because variance ignores sparsity,
nonlinear structure, and any variable you did not include in the feature vector
at all. Concretely, the failure mode is a variable that is nearly constant — so
nearly zero variance — but discrete and decision-relevant. Imagine a dataset of
running times where a handful of runs have a bimodal split between two server
configurations, and the two modes are $0.1$ apart in a direction where the bulk
of the data is tight; the variance ratio can be $99.9/0.1$ while the mode label
lives entirely in the $0.1$. PCA cannot see it, because PCA never looks at labels
and never looks at frequencies, only at second moments.

The diagnostic is to ask what the discarded coordinates are *for*, not how much
variance they held. Concretely: reconstruct the data from the retained
components and check whether the thing you are predicting survives; report the
retained fraction per feature group rather than overall; and if a variable
matters and PCA is dropping it, add the variance artificially (repeat or
whiten) or use a supervised method such as LDA, which optimises for
separability rather than spread. The lesson's own Common Mistakes section makes
the symmetric point from the other direction: on a circle, PCA keeps exactly 50%
and there is no signal to lose, which is a different failure — nothing matters
at all.

</details>

**Q5. The lesson insists that big-O describes growth and not milliseconds.
Explain exactly what a benchmark on small inputs tells you, and state the
condition under which its ranking would reverse.**

<details>
<summary>Model answer</summary>

A benchmark on small inputs tells you one thing: the *constant factor*, the
multiplicative overhead the big-O label deliberately ignores. If $f$ is
$O(n^2)$ and $g$ is $O(n \log n)$, big-O tells you that beyond some unknown
$n_0$ the exponent wins. On inputs below $n_0$ the ranking is whatever
$c_f g(n) < c_g n^2$ happens to make it, and $c_f$ and $c_g$ can differ by many
orders of magnitude — merge sort allocating and copying versus insertion sort
touching adjacent memory, for instance. The benchmark measures the part big-O
refuses to talk about.

The ranking reverses when $n$ passes the crossover, and the crossover is
determined by the constants. Concretely, $c_f n^2 > c_g n \log n$ exactly when
$n > (c_g/c_f)/\log n$, so the crossover is a single number determined by the
measured ratio divided by a slowly growing factor. If you measured the ratio on
n up to $10^6$ and the $O(n^2)$ side was ahead, the crossover is somewhere past
$10^6$ and *the $O(n)$ side is the one whose label you should believe about the
future*.

The condition for the reversal to actually happen is that the labels are right
and the constants are fixed: the input must grow without bound, the
implementation must not be asymptotically improved later (a quadratic loop with
an early exit is not $O(n^2)$ in the worst case but behaves far better in
practice), and the machine must not change the comparison, because a cache or
memory-bandwidth effect can make a constant-factor win permanent rather than
transient. That last one is the honest caveat: "the crossover will come" is a
claim about asymptotics, and there are real systems where it never arrives
because a physical constant, not the algorithm, is the binding constraint. What
you can say without the caveat is narrower and still useful — the label tells you
which function to distrust as the input grows, and the benchmark tells you which
to ship today.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — Time the two lookup strategies yourself.** Write a script
that builds a `dict` and a `list` of the same 100,000 integers, then times
looking up a key that exists at the *front* of the list rather than the back.
Report both times. Then explain, using the hash arithmetic described above, why
the `dict` time is roughly unchanged from the previous lesson's run while the
list time is now much smaller.

<details>
<summary>Solution</summary>

```python
import gc
import time

N = 100_000
keys = [f"key-{i}" for i in range(N)]
table = {k: i for i, k in enumerate(keys)}
values = list(table.values())

front_key = keys[0]              # sits at index 0 of the list
back_key = keys[-1]              # sits at index N-1 of the list

gc.collect()
gc.disable()
try:
    print(f"{'lookup':>12} {'dict ns':>10} {'list ns':>12} {'ratio':>8}")
    for label, key in (("front", front_key), ("back", back_key)):
        wanted = table[key]
        reps = 20_000

        t0 = time.perf_counter()
        for _ in range(reps):
            table[key]
        dict_ns = (time.perf_counter() - t0) / reps * 1e9

        t0 = time.perf_counter()
        for _ in range(reps):
            values.index(wanted)
        list_ns = (time.perf_counter() - t0) / reps * 1e9

        print(f"{label:>12} {dict_ns:>10.1f} {list_ns:>12.1f} {list_ns / dict_ns:>7.1f}x")
finally:
    gc.enable()

print()
print("The dict column is the same for both lookups: the hash of the key")
print("determines the slot regardless of where the value sits in insertion order.")
print("The list column shrinks by roughly the size of the table, because index()")
print("returns as soon as it reaches the match.")
```

Expected shape of output on a typical machine: both `dict` figures in the tens to
hundreds of nanoseconds, the `front` list figure around 20–50 µs, and the `back`
list figure around 2 ms. The absolute numbers vary; the ratios do not. A ratio
above roughly 100 for the front lookup means the dict really is doing a single
hash jump rather than anything resembling a scan.

</details>

**[ ] Exercise 2 — Find the exact float that represents 0.1.** Using only
`fractions.Fraction` and the standard library, print the exact rational value of
`0.1`, convert that rational back to a float, and print how far the round trip
is from the original decimal. Then explain in two sentences why no binary
floating point format, of any width, could have stored `0.1` exactly.

<details>
<summary>Solution</summary>

```python
from fractions import Fraction

exact = Fraction(0.1)
back = float(exact)

print(f"Fraction(0.1)          = {exact}")
print(f"float(Fraction(0.1))   = {back!r}")
print(f"abs error              = {float(abs(exact - Fraction(1, 10))):.20e}")
print(f"numerator              = {exact.numerator:,}")
print(f"denominator            = {exact.denominator:,}")
print(f"denominator = 2^62     -> {exact.denominator == 2 ** 62}")

print()
print("The stored value is the nearest double to 1/10, and it is slightly ABOVE 1/10.")
print("No power of two has a factor of 5, so 1/10 = 1/(2*5) cannot be written with")
print("a finite number of binary digits. Widening to 128 or 256 bits would shrink")
print("the error, but never remove it.")
```

Sample output:

```
Fraction(0.1)          = 3602879701896397/36028797018963968
float(Fraction(0.1))   = 0.1
abs error              = 5.55111512312578301027e-18
numerator              = 3,602,879,701,896,397
denominator            = 36,028,797,018,963,968
denominator = 2^62     -> True
```

The denominator being exactly `2^62` is the whole story. A binary float stores an
integer numerator over a power of two. `1/10` reduced is `1/(2·5)`, and the `5`
can never be cancelled by a power of two. Also note the round trip
`float(Fraction(0.1)) == 0.1` is `True`: once the value has been rounded into a
double, converting it back to a rational gives you exactly that double. The
information about `1/10` was lost at the first assignment, not at the
conversion.

</details>

**[ ] Exercise 3 — Show that float summation is not associative.** Build a
shopping cart of 500 items priced `19.99` and 500 priced `4.35`. Sum them in
arrival order, then sum them cheapest-first, then sum them exactly with
`fractions.Fraction`. Report whether the two float orders agree, and by how much
each misses the exact total. Then find the smallest demonstration you can:
over all subtotals in `(19.99, 99.99, 0.07, 1234.56, 45.00)` and all
percentages from 1 to 100, find every case where `(subtotal - discount) + discount
!= subtotal`, and explain why `100.00` never fails while `19.99` does. Finally,
convert the cart to integer cents and show that the problem disappears.

<details>
<summary>Solution</summary>

```python
from fractions import Fraction

# Float addition is not associative, so the same list of prices sums to
# different totals depending on the order you add them in.
line_items = [19.99] * 500 + [4.35] * 500

float_a = 0.0                       # arrival order
for item in line_items:
    float_a += item

float_b = 0.0                       # cheapest first: mathematically identical
for item in sorted(line_items):
    float_b += item

exact = sum(Fraction(str(item)) for item in line_items)

print(f"in arrival order       : {float_a!r}")
print(f"cheapest first         : {float_b!r}")
print(f"the two agree          : {float_a == float_b}")
print(f"exact value            : {exact} = {float(exact)!r}")
print(f"arrival order == exact : {Fraction(str(float_a)) == exact}")
print(f"cheapest  == exact     : {Fraction(str(float_b)) == exact}")
print()
print(f"drift, arrival order   : {float(Fraction(str(float_a)) - exact):+.10f}")
print(f"drift, cheapest first  : {float(Fraction(str(float_b)) - exact):+.10f}")
print()
cents_total = sum(round(i * 100) for i in line_items)
print(f"in integer cents       : {cents_total} cents = {cents_total / 100}")

# The small sharp version: apply a discount, then add it back.
# 100.00 is a bad subject because it IS exactly representable in binary.
print()
print("== apply a discount, then add it back ==")
subtotals = (19.99, 99.99, 0.07, 1234.56, 45.00)
total_failures = 0
for subtotal in subtotals:
    for percent in range(1, 101):
        discount = subtotal * percent / 100
        back = (subtotal - discount) + discount
        if back != subtotal:
            total_failures += 1
            if total_failures <= 5:
                print(f"  subtotal {subtotal:>8} at {percent:>3}% off: "
                      f"add-back gives {back!r}, expected {subtotal!r}")
print(f"  failures across {len(subtotals) * 100} pairs: {total_failures}")
print()
print("100.00 never fails because 100.00 = 1.953125 * 2^6 is exactly")
print("representable. 19.99 and 99.99 are not, so the round trip loses a bit.")

print()
print("== the fix: work in integer cents ==")
cents = [round(i * 100) for i in line_items]
print(f"  subtotal in cents      : {sum(cents)}")
print(f"  exact, no drift        : {Fraction(sum(cents), 100)}")
print(f"  each price exact       : "
      f"{all(Fraction(c, 100) == Fraction(str(c / 100)) for c in cents[:5])}")
print(f"  order no longer matters: {sum(cents) == sum(reversed(cents))}")
```

Output:

```
in arrival order       : 12170.000000000096
cheapest first         : 12169.99999999987
the two agree          : False
exact value            : 12170 = 12170.0
arrival order == exact : False
cheapest  == exact     : False

drift, arrival order   : +0.0000000001
drift, cheapest first  : -0.0000000001

in integer cents       : 1217000 cents = 12170.0

== apply a discount, then add it back ==
  subtotal    19.99 at  11% off: add-back gives 19.990000000000002, expected 19.99
  subtotal    99.99 at  11% off: add-back gives 99.98999999999998, expected 99.99
  subtotal    99.99 at  15% off: add-back gives 99.99000000000001, expected 99.99
  subtotal    99.99 at  19% off: add-back gives 99.98999999999998, expected 99.99
  subtotal    99.99 at  24% off: add-back gives 99.99000000000001, expected 99.99
  failures across 500 pairs: 7

100.00 never fails because 100.00 = 1.953125 * 2^6 is exactly
representable. 19.99 and 99.99 are not, so the round trip loses a bit.

== the fix: work in integer cents ==
  subtotal in cents      : 1217000
  exact, no drift        : 12170
  each price exact       : True
  order no longer matters: True
```

Note the two drifts have opposite signs. That is the signature of rounding in
different directions depending on order: the cheap items accumulate error one
way when they come first, and the expensive ones carry it differently when they
do. Mathematically the sum is a single number; floating point gives you two,
and neither is it.

</details>

**[ ] Challenge 4 — Prove the RSA round trip arithmetically, without running it.** For
the key `n = 3233`, `e = 17`, `d = 2753`, write out by hand why
`(m^17)^2753 mod 3233 = m` for every `m` coprime to 3233. You will need Fermat's
little theorem. Then answer: what goes wrong for a message that is *not* coprime
to `n`, and how do real implementations handle it?

<details>
<summary>Solution</summary>

**The argument.** Euler's theorem says that when `gcd(m, n) = 1`,
`m^phi(n) ≡ 1 (mod n)`. Here `n = 3233`, `phi(n) = (61-1)(53-1) = 3120`.

`d` was chosen so that `e·d ≡ 1 (mod phi(n))`, that is, `17 · 2753 = 46801`, and
`46801 = 15 · 3120 + 1`. So `e·d = 1 + 15·phi(n)`.

Now decrypt:
`c^d ≡ (m^e)^d = m^(e·d) = m^(1 + 15·phi(n)) = m · (m^phi(n))^15 ≡ m · 1^15 ≡ m (mod n)`.

The `m^phi(n) ≡ 1` step is the whole trick, and it is why the key owner needs
`phi(n)`, which is why the owner needs to know `p` and `q`, which is why
factoring breaks RSA.

**Non-coprime messages.** Euler's theorem has the coprimality hypothesis. If
`m` is a multiple of `61` or of `53`, then `m^phi(n) is not ≡ 1`, and the
cancellation above is invalid. In practice real RSA pads the message first:
PKCS#1 v1.5 prepends random nonzero bytes, and OAEP prepends structured random
bytes. Two consequences follow from the arithmetic, and both are real attacks if
you skip the padding:

1. If you ever encrypt the same message twice with textbook RSA you get the same
   ciphertext, so an attacker sees repeats. Real schemes include random padding
   so that identical plaintexts produce different ciphertexts.
2. Textbook RSA is multiplicative: `enc(m1·m2) = enc(m1)·enc(m2)`. With enough
   chosen-plaintext pairs an attacker recovers factors. Padding destroys this.

You can see the coprimality issue directly:

```python
n, e, d = 3233, 17, 2753


def mod_pow(base, exp, mod):
    """base**exp mod mod, by repeated squaring."""
    result, base = 1, base % mod
    while exp:
        if exp & 1:
            result = result * base % mod
        base = base * base % mod
        exp >>= 1
    return result


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


print(f"{'m':>6} {'gcd(m,n)':>9} {'encrypted':>10} {'decrypted':>10} {'ok':>6}")
for m in (2, 65, 1234, 53, 61, 0, 3233):
    c = mod_pow(m, e, n)
    back = mod_pow(c, d, n)
    print(f"{m:>6} {gcd(m, n):>9} {c:>10} {back:>10} {str(back == m):>6}")

print()
print("Everything coprime to n round-trips exactly. m = 53 and m = 61 also")
print("round-trip, but only by luck: for those, m*phi(n) is 0 mod n rather than")
print("1 mod n, so m^phi(n) = m and the extra factor cancels trivially.")
print("m = 3233 (equal to n) encrypts to 0 and comes back as 0: the message is")
print("destroyed. That is why real RSA never encrypts an unpadded plaintext.")
```

Output:

```
     m  gcd(m,n)  encrypted  decrypted     ok
     2         1       1752          2   True
    65         1       2790         65   True
  1234         1       2183       1234   True
    53        53       1802         53   True
    61        61        610         61   True
     0      3233          0          0   True
  3233      3233          0          0  False

Everything coprime to n round-trips exactly. m = 53 and m = 61 also
round-trip, but only by luck: for those, m*phi(n) is 0 mod n rather than
1 mod n, so m^phi(n) = m and the extra factor cancels trivially.
m = 3233 (equal to n) encrypts to 0 and comes back as 0: the message is
destroyed. That is why real RSA never encrypts an unpadded plaintext.
```

The last row is the visible failure: `m = n` encrypts to `0`, and `0` decrypts to
`0`, so the round trip "succeeds" numerically while the message is gone. The
coprimality hypothesis is what makes the *proof* work, and unproved cases are
where the attacks live.

</details>

**[ ] Exercise 5 — Diagnose the learning rate.** Reuse the lesson's eight
students and its gradient-descent loop. Run it three times: $\eta = 0.0001$,
$\eta = 0.05$ (the lesson's value) and $\eta = 3.0$. For each, report the loss
after 1, 50, 1000 and 3000 epochs, the final weight vector, and how many of the
eight predictions land on the correct side of $0.5$. Then answer two questions
in writing. (a) Which run is "stuck"? (b) The $\eta = 3.0$ run reaches a loss
near zero — does that make it the best model? Show at least one prediction that
argues against it.

<details>
<summary>Solution</summary>

```python
# The lesson's data and its gradient-descent loop, wrapped in a function so the
# learning rate can be varied. Nothing else changes between runs.
X = [
    (1.0, 9.0, 2.0, 0.0),
    (2.0, 8.0, 4.0, 1.0),
    (3.0, 7.0, 6.0, 1.0),
    (8.0, 3.0, 8.0, 2.0),
    (9.0, 2.0, 9.0, 3.0),
    (5.0, 5.0, 7.0, 2.0),
    (6.0, 4.0, 3.0, 1.0),
    (4.0, 6.0, 5.0, 0.0),
]
y = [0, 0, 0, 1, 1, 1, 1, 0]
LABELS = ("studied", "slept", "prior", "revision")

n, d = len(X), len(X[0])
MARKS = (1, 50, 1000, 3000)


def sigmoid(z):
    return 1.0 / (1.0 + pow(2.718281828459045, -z))


def predict(features, w, b):
    return sigmoid(b + sum(wi * fi for wi, fi in zip(w, features)))


def loss_of(w, b):
    return sum((predict(x, w, b) - t) ** 2 for x, t in zip(X, y)) / n


def train(lr, epochs=3000):
    w = [0.0] * d
    b = 0.0
    history = {}
    for epoch in range(1, epochs + 1):
        grad_w = [0.0] * d
        grad_b = 0.0
        for features, label in zip(X, y):
            err = predict(features, w, b) - label
            for j in range(d):
                grad_w[j] += err * features[j]
            grad_b += err
        for j in range(d):
            w[j] -= lr * grad_w[j] / n
        b -= lr * grad_b / n
        if epoch in MARKS:
            history[epoch] = loss_of(w, b)
    return w, b, history


for lr in (0.0001, 0.05, 3.0):
    w, b, history = train(lr)
    probs = [predict(x, w, b) for x in X]
    hits = sum((p >= 0.5) == bool(t) for p, t in zip(probs, y))
    biggest = max(range(d), key=lambda j: abs(w[j]))

    print(f"== learning rate {lr} ==")
    for epoch in MARKS:
        print(f"   epoch {epoch:>5}  loss {history[epoch]:.10f}")
    print(f"   weights {[round(v, 3) for v in w]}  bias {round(b, 3)}")
    print(f"   correct side of 0.5: {hits}/{n}")
    print(f"   largest |weight|: {LABELS[biggest]} at {w[biggest]:+.3f}")
    print(f"   most confident prediction: {max(probs, key=lambda p: abs(p - 0.5)):.6f}")
    print()
```

Output:

```
== learning rate 0.0001 ==
   epoch     1  loss 0.2498601932
   epoch    50  loss 0.2431859926
   epoch  1000  loss 0.1586524314
   epoch  3000  loss 0.0939402730
   weights [0.188, -0.229, 0.069, 0.067]  bias -0.006
   correct side of 0.5: 8/8
   largest |weight|: slept at -0.229
   most confident prediction: 0.885766

== learning rate 0.05 ==
   epoch     1  loss 0.1904858209
   epoch    50  loss 0.0227963772
   epoch  1000  loss 0.0003474270
   epoch  3000  loss 0.0000429801
   weights [1.977, -2.411, 0.476, 1.718]  bias -0.048
   correct side of 0.5: 8/8
   largest |weight|: slept at -2.411
   most confident prediction: 1.000000

== learning rate 3.0 ==
   epoch     1  loss 0.2066663736
   epoch    50  loss 0.0000000250
   epoch  1000  loss 0.0000000001
   epoch  3000  loss 0.0000000000
   weights [9.714, -11.846, 4.23, 3.923]  bias -0.326
   correct side of 0.5: 8/8
   largest |weight|: slept at -11.846
   most confident prediction: 0.000000
```

Read the "most confident prediction" column as the prediction furthest from
`0.5` in either direction. It is `0.885766` for the slow run, `1.000000` for the
lesson's run, and `0.000000` for the fast one — the fast run is not merely more
confident, it is confident in the *other* direction, having driven a failing
student's probability to seven printed zeros.

**(a) The stuck run is $\eta = 0.0001$.** After 3000 epochs the loss is still
`0.0939`, roughly two thousand times worse than the lesson's `0.000043`, and the
weights have barely moved from zero: `[0.188, -0.229, 0.069, 0.067]` against
`[1.977, -2.411, 0.476, 1.718]`. The step size is proportional to the learning
rate, so a hundredth of the rate buys roughly a hundredth of the progress per
epoch. It has not converged, it is merely moving slowly — note the loss is still
falling at epoch 3000, and the same run with more epochs would continue to
improve. Its best prediction is only `0.885766`, so it is also the least decisive
of the three, even though all three get 8/8 on the right side of `0.5`.

**(b) No, and the third block's last two lines are the evidence.** The
$\eta = 3.0$ run reports a loss of `0.0000000000`, but its weights are five times
larger than the lesson's and its most extreme prediction has been driven to
`0.000000` for a student who failed. The sigmoid never reaches exactly 0 or 1; it
approaches them, and it approaches them precisely when the input $\mathbf{w}
\cdot \mathbf{x} + b$ is large, which means large weights. So the loss hit zero
because the model saturated, not because it found better structure.

The reason the loss stops rising instead of exploding is the sigmoid's
derivative, `$\sigma'(z) = \sigma(z)(1-\sigma(z))$`, which is at most $1/4$ and
tends to zero as $|z|$ grows. Big weights produce a vanishing gradient, so the
loop cannot overshoot into divergence. Saturation protects you from
instability while quietly destroying calibration.

The practical reading: all three runs get 8/8 on the right side of $0.5$, so
the *classification* is identical. The differences are entirely in the
probabilities, and the two lower-loss runs are the less trustworthy ones on
inputs near the boundary. Measure this the way you would in practice — hold out
some data, and compare held-out loss against training loss.

</details>

**[ ] Exercise 6 — Sweep every message the toy RSA key can receive.** For
`n = 3233`, `e = 17`, `d = 2753`, encrypt and decrypt **every** residue from `0`
to `3232` and report how many round-trip. Count how many of those messages are
coprime to `n` and how many are not, and verify that the coprime count is exactly
$\varphi(n) = 3120$. Then, for the messages that are *not* coprime, work out why
they still round-trip using the Chinese Remainder Theorem, and state the precise
reason the Euler-theorem proof does not apply to them.

<details>
<summary>Solution</summary>

```python
def mod_pow(base, exp, mod):
    """base**exp mod mod, by repeated squaring."""
    result, base = 1, base % mod
    while exp:
        if exp & 1:
            result = result * base % mod
        base = base * base % mod
        exp >>= 1
    return result


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


p, q = 61, 53
n, e, d = p * q, 17, 2753
phi = (p - 1) * (q - 1)

failures = [m for m in range(n) if mod_pow(mod_pow(m, e, n), d, n) != m]
coprime = [m for m in range(n) if gcd(m, n) == 1]
# multiples of each prime, counted over the whole residue range 0..n-1
div_p = [m for m in range(n) if m % p == 0]
div_q = [m for m in range(n) if m % q == 0]

print(f"n = {n}, e = {e}, d = {d}, phi(n) = {phi}")
print(f"messages swept          : {n}")
print(f"round-trip failures     : {len(failures)} {failures}")
print(f"coprime to n            : {len(coprime)}")
print(f"phi(n) agrees           : {len(coprime) == phi}")
print(f"multiples of {p} in range    : {len(div_p)}  (0, {p}, ..., {p * (n // p - 1)})")
print(f"multiples of {q} in range    : {len(div_q)}  (0, {q}, ..., {q * (n // q - 1)})")
print(f"their union             : {len(set(div_p) | set(div_q))} = {len(div_p)} + {len(div_q)} - 1")
print(f"non-coprime total       : {n - len(coprime)}")
print()
print("CRT check on a non-coprime message: m = 53")
m = 53
c = mod_pow(m, e, n)
back = mod_pow(c, d, n)
print(f"  c = {c}, c^d mod n = {back}")
print(f"  mod {p}: c^d = {back % p}, m = {m % p}, agree: {back % p == m % p}")
print(f"  mod {q}: c^d = {back % q}, m = {m % q}, agree: {back % q == m % q}")
print(f"  e*d - 1 = {e * d - 1} = {phi} * {(e * d - 1) // phi}  (so ed = 1 mod phi)")
print(f"  e*d - 1 is a multiple of {p - 1} : {(e * d - 1) % (p - 1) == 0}")
print(f"  e*d - 1 is a multiple of {q - 1} : {(e * d - 1) % (q - 1) == 0}")
print()
print("m = n is outside the sweep and is the real failure:")
c = mod_pow(n, e, n)
print(f"  mod_pow({n}, {e}, {n}) = {c}, and {c}^d mod n = {mod_pow(c, d, n)}")
```

Output:

```
n = 3233, e = 17, d = 2753, phi(n) = 3120
messages swept          : 3233
round-trip failures     : 0 []
coprime to n            : 3120
phi(n) agrees           : True
multiples of 61 in range    : 53  (0, 61, ..., 3172)
multiples of 53 in range    : 61  (0, 53, ..., 3180)
their union             : 113 = 53 + 61 - 1
non-coprime total       : 113

CRT check on a non-coprime message: m = 53
  c = 1802, c^d mod n = 53
  mod 61: c^d = 53, m = 53, agree: True
  mod 53: c^d = 0, m = 0, agree: True
  e*d - 1 = 46800 = 3120 * 15  (so ed = 1 mod phi)
  e*d - 1 is a multiple of 60 : True
  e*d - 1 is a multiple of 52 : True

m = n is outside the sweep and is the real failure:
  mod_pow(3233, 17, 3233) = 0, and 0^d mod n = 0
```

**Every residue round-trips.** Zero failures out of 3233. That is a stronger
result than the lesson's Euler-theorem argument licenses, and the interesting
part of the exercise is *why*.

**The counting.** `gcd(m, 3233) = 1` exactly when $m$ is divisible by neither
61 nor 53. Over the residue range `0..3232` the multiples of 61 are
`0, 61, …, 3172`, which is 53 values, and the multiples of 53 are
`0, 53, …, 3180`, which is 61 values. The only number divisible by both is `0`
itself, since $61 \cdot 53 = 3233$ is out of range. So the union — the
non-coprime messages — has $53 + 61 - 1 = 113$ members, and
$3233 - 113 = 3120$ are coprime to $n$: exactly $\varphi(n)$, as it must be.
Note that the count includes `0`, so `0` is one of the 113.

**Why the non-coprime messages survive, via CRT.** Work modulo each prime
separately and take $m = 53$.

- Modulo 53: $m \equiv 0$, so $c = m^{e} \equiv 0$, and $0^{d} = 0 = m$. The
  exponent $d$ never appears; the only fact used is that zero stays zero.
- Modulo 61: $m = 53$ is coprime to 61, so Fermat gives $53^{60} \equiv 1 \pmod{61}$.
  We need $ed \equiv 1 \pmod{60}$, and indeed $ed - 1 = 46800 = 60 \cdot 780$.
- Since 61 and 53 are coprime, the Chinese Remainder Theorem says a residue mod
  3233 is determined by its two residues mod 61 and mod 53, and there is exactly
  one such residue in `0..3232`. The decrypted value has the right residue on both
  primes, so it *is* $m$ mod 3233.

In general the same argument works for any $m$: on the prime that divides $m$ the
computation gives $0 = 0$, on the prime that does not divide $m$ Fermat applies
because $ed \equiv 1 \pmod{q-1}$ follows from $ed \equiv 1 \pmod{\varphi(n)}$ and
$\varphi(n) = (p-1)(q-1)$ is a multiple of both $p-1$ and $q-1$. CRT glues the two
answers back together.

**Why the proof still does not apply.** Euler's theorem was invoked as
$m^{\varphi(n)} \equiv 1 \pmod n$, and for $m = 53$ that is false:
$53^{3120} \equiv 0 \pmod{53}$. The derivation in the lesson rewrites
$m^{ed} = m \cdot (m^{\varphi(n)})^{15}$ and replaces the bracket by $1$. For these
113 messages that substitution is illegal. They round-trip because a *different*
argument works, and an argument that is not the one you proved is not a
guarantee — it is a coincidence of this key's structure. Key sizes, padding
schemes and library choices have all been broken by treating "it worked in my
test" as "it is proved".

The sweep also shows the boundary that does break: $m = n = 3233$ is outside
`0..3232`, encrypts to `0`, and never returns. Real RSA never encrypts an
unpadded plaintext, which is why PKCS#1 and OAEP prepend random bytes — that both
restores the coprimality the proof needs and makes identical messages encrypt
differently.

</details>

**[ ] Challenge 7 — Derive the PCA direction from the covariance matrix, and find
the dataset where the lesson's advice fails.** (a) Starting only from the five
points in the lesson, compute the covariance matrix and solve
$\det(\Sigma - \lambda I) = 0$ by hand to get both eigenvalues. Show that
$\lambda_1 + \lambda_2$ equals the total variance the lesson printed, and that
$\Sigma v_1 = \lambda_1 v_1$ for the direction the lesson used. (b) Then build a
dataset with *equal* spread in every direction — a circle — run the same code on
it, and report the retained fraction. (c) Finally, explain in writing what the
lesson's claim "keep the direction of greatest variance" assumes about the data,
and give a concrete example where that assumption is false.

<details>
<summary>Solution</summary>

```python
import math


def analyse(points, label):
    n = len(points)
    mx = sum(x for x, y in points) / n
    my = sum(y for x, y in points) / n
    centred = [(x - mx, y - my) for x, y in points]

    sxx = sum(x * x for x, y in centred) / n
    syy = sum(y * y for x, y in centred) / n
    sxy = sum(x * y for x, y in centred) / n
    print(f"== {label} ==")
    print(f"  mean            = ({mx:.3f}, {my:.3f})")
    print(f"  covariance      = [[{sxx:.4f}, {sxy:.4f}], [{sxy:.4f}, {syy:.4f}]]")

    # (a) Eigenvalues by hand: det(Sigma - lambda I) = 0 gives
    #     lambda^2 - (sxx+syy)*lambda + (sxx*syy - sxy^2) = 0
    trace = sxx + syy
    discriminant = math.sqrt((sxx - syy) ** 2 + 4 * sxy ** 2)
    lam1 = (trace + discriminant) / 2
    lam2 = (trace - discriminant) / 2
    print(f"  trace sxx+syy   = {trace:.6f}")
    print(f"  discriminant   = {discriminant:.6f}")
    print(f"  lambda_1        = {lam1:.6f}")
    print(f"  lambda_2        = {lam2:.6f}")
    print(f"  lam1+lam2 == trace: {abs(lam1 + lam2 - trace) < 1e-9}")

    # (a) the eigenvector, and the lesson's closed form for its angle
    theta = 0.5 * math.atan2(2 * sxy, sxx - syy)
    v1 = (math.cos(theta), math.sin(theta))
    image = (sxx * v1[0] + sxy * v1[1], sxy * v1[0] + syy * v1[1])
    print(f"  theta           = {math.degrees(theta):.4f} degrees")
    print(f"  v1              = ({v1[0]:.6f}, {v1[1]:.6f})")
    print(f"  Sigma v1        = ({image[0]:.6f}, {image[1]:.6f})")
    print(f"  lambda_1 * v1   = ({lam1 * v1[0]:.6f}, {lam1 * v1[1]:.6f})")
    print(f"  Sigma v1 == lam1 v1: "
          f"{abs(image[0] - lam1 * v1[0]) < 1e-9 and abs(image[1] - lam1 * v1[1]) < 1e-9}")

    def spread(v):
        proj = [c[0] * v[0] + c[1] * v[1] for c in centred]
        mean_p = sum(proj) / n
        return sum((q - mean_p) ** 2 for q in proj) / n

    print(f"  total variance  = {spread((1.0, 0.0)) + spread((0.0, 1.0)):.6f}")
    print(f"  retained        = {lam1 / trace * 100:.4f}%")
    print()
    return lam1, lam2


# (a) the lesson's five points
analyse([(1.0, 2.0), (2.0, 3.1), (2.5, 4.0), (3.0, 5.2), (9.0, 11.5)],
        "the lesson's five points")

# (b) a circle: equal spread in every direction
circle = [(math.cos(2 * math.pi * k / 8), math.sin(2 * math.pi * k / 8))
          for k in range(8)]
analyse(circle, "an 8-point circle")

# (b') a square, for contrast: also isotropic on the axes, but not a circle
square = [(1.0, 1.0), (1.0, -1.0), (-1.0, 1.0), (-1.0, -1.0)]
analyse(square, "a 4-point square")
```

Output:

```
== the lesson's five points ==
  mean            = (3.500, 5.160)
  covariance      = [[8.0000, 9.4000], [9.4000, 11.1544]]
  trace sxx+syy   = 19.154400
  discriminant   = 19.062797
  lambda_1        = 19.108599
  lambda_2        = 0.045801
  lam1+lam2 == trace: True
  theta           = 49.7624 degrees
  v1              = (0.645959, 0.763372)
  Sigma v1        = (12.343370, 14.586972)
  lambda_1 * v1   = (12.343370, 14.586972)
  Sigma v1 == lam1 v1: True
  total variance  = 19.154400
  retained        = 99.7609%

== an 8-point circle ==
  mean            = (-0.000, -0.000)
  covariance      = [[0.5000, 0.0000], [0.0000, 0.5000]]
  trace sxx+syy   = 1.000000
  discriminant   = 0.000000
  lambda_1        = 0.500000
  lambda_2        = 0.500000
  lam1+lam2 == trace: True
  theta           = 45.0000 degrees
  v1              = (0.707107, 0.707107)
  Sigma v1        = (0.353553, 0.353553)
  lambda_1 * v1   = (0.353553, 0.353553)
  Sigma v1 == lam1 v1: True
  total variance  = 1.000000
  retained        = 50.0000%

== a 4-point square ==
  mean            = (0.000, 0.000)
  covariance      = [[1.0000, 0.0000], [0.0000, 1.0000]]
  trace sxx+syy   = 2.000000
  discriminant   = 0.000000
  lambda_1        = 1.000000
  lambda_2        = 1.000000
  lam1+lam2 == trace: True
  theta           = 0.0000 degrees
  v1              = (1.000000, 0.000000)
  Sigma v1        = (1.000000, 0.000000)
  lambda_1 * v1   = (1.000000, 0.000000)
  Sigma v1 == lam1 v1: True
  total variance  = 2.000000
  retained        = 50.0000%
```

**(a) The hand calculation.** The covariance matrix is
`[[8.0000, 9.4000], [9.4000, 11.1544]]`. Setting
`$\det(\Sigma - \lambda I) = (s_{xx}-\lambda)(s_{yy}-\lambda) - s_{xy}^2 = 0$`
gives

    lambda^2 - (s_xx + s_yy) * lambda + (s_xx * s_yy - s_xy^2) = 0
    lambda^2 - 19.1544 * lambda + 5.5613 = 0

and the quadratic formula gives `$\lambda_{1,2} = \frac{(s_{xx}+s_{yy}) \pm
\sqrt{(s_{xx}-s_{yy})^{2} + 4s_{xy}^{2}}}{2}$`, which is the code's
`discriminant` line: `sqrt(3.1536^2 + 4 * 88.36) = sqrt(363.39) = 19.062797`.
So `$\lambda_1 = 19.108599$` and `$\lambda_2 = 0.045801$`, and they sum to
`19.154400`, which is exactly the total variance the lesson printed. That sum is
not a coincidence: the trace of $\Sigma$ is the total variance along the two
coordinate axes, and eigenvalues are the variances along the principal
directions, so both decompositions must add to the same number.

Substituting $v_1 = (0.645959, 0.763372)$ into $\Sigma v_1$ gives
`(12.343370, 14.586972)`, and `$\lambda_1 v_1$` gives the same pair. So $v_1$ is
genuinely an eigenvector, and the lesson's `atan2` formula found it without
solving the matrix. Retained fraction: `19.108599 / 19.154400 = 99.76%`, the
`99.8%` in the lesson's prose.

**(b) The circle.** The covariance matrix is exactly `[[0.5, 0], [0, 0.5]]`, so
the discriminant is 0, both eigenvalues are `0.5`, and the retained fraction is
`0.5 / 1.0 = 50.0%`. Half the structure goes. The square is the same story: both
eigenvalues `1.0` and the same 50%. The lesson's closed form does not break here,
but it is not choosing anything either: the circle returns `theta = 45°` and the
square `theta = 0°`, and since every direction has eigenvalue `0.5` resp. `1.0`,
*every* angle would have been an equally correct answer. The formula produced an
answer because `atan2` was handed a number, not because that number was preferred
over any other. This is the degenerate case the Formula Sheet's note about
`atan2` is about: when the discriminant is 0 there is no single principal
direction to find.

**(c) What the advice assumes.** "Keep the direction of greatest variance"
assumes that variance is a proxy for the information you care about, and that
the information is *linear* and *present in the feature vector*. Both can fail.

Variance is a second moment. It knows nothing about labels, so it cannot know
that a near-constant direction is where your class boundary lives, and it knows
nothing about frequencies, so a direction holding 99% of your rows and 100% of
your signal is scored by the 1%. A concrete counterexample: response times of a
service, where 99% of requests take about 100 ms and the 1% that take about
105 ms are the ones that breach the SLA. If those two clusters differ only along
a low-variance direction, one-dimensional PCA removes the only feature that
separates pass from fail, and the retained percentage will read something like
99.8% the whole time. The square makes the extreme version obvious: keep 50% of
a square and you get a line segment, and the corner information is gone.

The second assumption is linearity. PCA finds straight lines. If your data lies
on a curve — a spiral, a circle, a manifold — the dominant directions are the
ones along the curve and the coordinate that identifies *where* on the curve you
are can be low variance. Kernel PCA lifts the data first, and the lesson's
`[Lesson 40]` SVD route is the numerically better version of the same idea.

The diagnostic to use instead of the retained percentage: reconstruct the data
from the kept components and check whether the quantity you are predicting
survives, and report the retained fraction per feature group rather than overall.

</details>

## Summary

- Hash map lookup is O(1) because a numeric hash picks the slot; a list scan
  grows linearly with the table.
- `0.1 + 0.2 != 0.3` because 1/10 has no finite binary expansion; the stored
  value of `0.1` is `3602879701896397/36028797018963968`.
- Tiny per-operation errors accumulate: a million additions of `0.01` give
  `10000.000000171856`. Money goes in integer cents.
- Neural network training is a loop, a derivative, and a learning rate.
  Gradient descent, twenty lines, no magic.
- RSA is Euler's theorem plus repeated squaring. `pow(m, e, n)` then
  `pow(c, d, n)` returns `m` because `e·d ≡ 1 (mod phi(n))`.
- Repeated squaring turns `2^k` multiplications into `k`, which is why RSA-2048
  is fast and naive exponentiation is not.
- PCA finds the eigenvector of the covariance matrix with the largest variance
  and projects onto it. In the 2D case above it kept 99.8% of the variance.
- Big-O describes growth, not milliseconds. The constant factor can make an
  `O(n²)` algorithm faster than an `O(n)` one on every input you will run.

## Next

[Lesson 01 — How to Read Mathematical Notation](../part00_orientation/01_how_to_read_notation.md)
takes the ideas here and teaches you to read them off a page. It assumes you can
run Python and nothing else.
