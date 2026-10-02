# 80 — Big-O and Complexity Analysis

**Part**: part06_algorithms_math · **Prerequisites**: 24 · **Time**: 45 min

---

## In Plain Words

Big-O is a way of saying how a cost *grows* as the input gets bigger, while deliberately
ignoring the constant factor. If an algorithm takes about a million operations on a
million items, that is linear. If it takes a trillion, that is quadratic. One is
milliseconds; the other is days. Big-O tells you which, without you having to run either.

The word "about" hides the whole trick. Big-O is an upper bound with a very generous
margin: "at most a constant times this rate." The constant is unknown and usually enormous.
Its purpose is not precision. It is to let you compare two algorithms when one is a hundred
times faster at small sizes but a million times faster at large ones, and to be able to say
that without running a benchmark.

Two things make this harder than it sounds, and both are in this lesson. First, a bound is
only meaningful against a *specific* input parameter, because the cost of one arithmetic
operation depends entirely on how big the numbers are — and a Python integer is not a
machine word. Second, recursive algorithms need their own machinery, and the Master Theorem
is that machinery for the common case.

---

## Why Computer Science Cares

- **It decides what is possible.** `O(n^2)` at $n = 10^5$ is $10^{10}$ operations —
  hours. At $n = 10^6$ it is $10^{12}$ — days. An `O(n\log n)$` version is a weekend
  project; an `O(n^2)$` version is a research project.
- **It is the language of every interview and every code review.** "Can you do it in
  linear time?" is a standard question, and the answer is usually a better data structure
  rather than a cleverer loop.
- **The FFT in [lesson 55](../part04_calculus/55_fourier_series_and_transforms.md) is the
  canonical example.** Naive transform `O(n^2)`; FFT `O(n log n)`; at $n = 2^{20}$ the
  measured arithmetic counts differ by a factor of 104 858. No other single optimisation
  has that effect on so much applied mathematics.
- **Choosing a data structure is choosing a complexity.** `list` append is `O(1)`, `list`
  insert at position 0 is `O(n)`. `dict` lookup is `O(1)` amortised; `in` on a `list` is
  `O(n)`. Lesson [81](81_amortized_analysis.md) handles the "amortised" honestly.
- **Bit complexity decides whether a cryptographic idea works.** RSA security rests on
  factoring a 2048-bit number being hard while multiplying two 1024-bit numbers is easy.
  Both statements are complexity statements.
- **Time is not the only resource.** Space complexity, I/O complexity, and
  communication complexity all use the same notation, and the last is what determines
  whether a distributed algorithm works at all.

---

## The Formal Version

**Definition.** Let $f, g : \mathbb{N} \to \mathbb{R}_{\ge 0}$. We write
$f \in O(g)$ — "$f$ is big-O of $g$" — if there exist constants $c > 0$ and $n_0$ such that

$$f(n) \le c\,g(n) \quad \text{for all } n \ge n_0.$$

**Definition.** $f \in \Omega(g)$ if there exist $c > 0$ and $n_0$ with
$f(n) \ge c\,g(n)$ for all $n \ge n_0$.

**Definition.** $f \in \Theta(g)$ if $f \in O(g)$ **and** $f \in \Omega(g)$.

**Definition.** $f \in o(g)$ if for every $c > 0$ there is $n_0$ with
$f(n) \le c\,g(n)$ for all $n \ge n_0$ — the ratio tends to zero.

**Definition.** $f \in \omega(g)$ if $g \in o(f)$.

*Explanation.* In words: **O** is an upper bound, **Ω** a lower bound, **Θ** a tight
bound, and **o/ω** strict asymptotic dominance. The $\exists n_0$ in every definition is
the "eventually" clause: small inputs are irrelevant, which is exactly what you want when
someone's implementation is 40 times faster than yours at $n = 10$.

**Theorem.** $\Theta$ is a total order on complexity classes:
$f \in O(g)$ and $g \in O(f)$ implies $f \in \Theta(g)$.

**Theorem (Hierarchy).** For every $\varepsilon > 0$ and every $k > 0$,
$1 \in O(\log n) \subset o(n^\varepsilon) \subset O(n^\varepsilon) \subset o(n) \subset
O(n\log n) \subset o(n^{1+\varepsilon}) \subset O(n^{1+\varepsilon}) \subset o(n^2) \subset \cdots \subset O(2^n)$.

**Definition.** An *input parameter* is a specific quantity the complexity is measured
against. For a sorting routine on $n$ integers it is $n$. For arithmetic on integers, it
is the *bit length* $b$ of those integers.

*Explanation.* This distinction is the most practically important thing in the lesson.
"Adding takes `O(1)`" is false in Python, where `int` is arbitrary precision. Adding two
$b$-bit integers costs $\Theta(b/30)$ machine steps. The claims are both true; they are
answers to different questions.

**Theorem (Bit complexity).** For $a$ and $b$ each $b$ bits long:

| operation | bit cost |
| --- | --- |
| comparison | $O(b)$ |
| addition, subtraction | $\Theta(b)$ |
| multiplication (schoolbook) | $\Theta(b^2)$ |
| division (schoolbook) | $\Theta(b^2)$ |
| gcd (Euclid) | $O(b^2)$ |

Python uses Karatsuba multiplication for large operands, giving $O(b^{\log_2 3}) \approx
O(b^{1.585})$ above a size threshold.

**Theorem (Master Theorem).** For $T(n) = a\,T(n/b) + \Theta(n^c)$ with $a \ge 1$, $b > 1$,
let $d = \log_b a$. Then:

- if $c < d$: $T(n) \in \Theta(n^d)$
- if $c = d$: $T(n) \in \Theta(n^d \log n)$
- if $c > d$: $T(n) \in \Theta(n^c)$

*Explanation.* Three shapes, all visible in a recursion tree. Either the internal work per
level dominates ($c > d$), or the leaves dominate ($c < d$), or every level costs the same
($c = d$) and you multiply that by the height $\log_b n$.

**Theorem (Repeated squaring).** Computing $a^n \bmod m$ by $n$ multiplications costs
$O(n \cdot \mathrm{Mul}(b))$ bit operations where $b$ is the bit length of $m$. By repeated
squaring it costs $O(\log n \cdot \mathrm{Mul}(b))$.

**Definition.** The *amortised* cost of $n$ operations on a data structure is
$T(n)/n$ — the average cost per operation over a worst-case sequence. See
[81 — Amortised Analysis](81_amortized_analysis.md).

---

## Worked Example

### Example 1: growth classes and their doubling factors

The most useful single fact about a complexity class is what happens when $n$ doubles:

| class | cost | multiplier per doubling |
| --- | --- | --- |
| `O(1)` | $c$ | $1$ |
| `O(log n)` | $\log n$ | $1 + \frac{1}{\log n} \to 1$ |
| `O(n)` | $n$ | $2$ |
| `O(n log n)` | $n\log n$ | $\approx 2.1$ |
| `O(n^2)` | $n^2$ | $4$ |
| `O(2^n)` | $2^n$ | $2^n$ |

That last row is the whole reason the class exists. $O(n\log n)$ is 10 per cent worse than
`O(n)`; `O(n^2)` is 4× worse, painful; `O(2^n)` doubles, which means adding *one* to `n`
doubles the work.

The code confirms the pattern for the exact counts, and measures the fitted exponent of
each curve: `1.0000` for linear, `2.0000` for quadratic, `1.1237` for $n\log n$ (which is
not a pure power, so its fitted slope drifts upward as $\log_2 n$ grows — which is exactly
what makes it strictly worse than linear).

### Example 2: the feasible-$n$ table

At one billion operations per second, and a budget of one second:

| class | largest $n$ |
| --- | --- |
| `O(1)` | unbounded |
| `O(log n)` | unbounded |
| `O(n)` | $10^9$ |
| `O(n log n)` | $3.96\times10^7$ |
| `O(n^2)` | $3.16\times10^4$ |
| `O(2^n)` | $n = 29.9$, i.e. 30 |

That last row is the one to remember. `O(2^n)` exhausts a one-second budget with **thirty
items**. Subset enumeration, exact cover, brute-force constraint satisfaction, and
unconstrained optimisation all live there. And $2^{60} = 1.153\times10^{18}$ operations is
36 years at a billion per second, so the class does not become merely slow — it becomes
permanent.

### Example 3: the bit cost, measured

`sys.getsizeof` on $2^b$ gives the exact memory:

| bits | bytes | bytes/bit |
| --- | --- | --- |
| 30 | 32 | 1.0667 |
| 300 | 68 | 0.2267 |
| 3000 | 428 | 0.1427 |
| 30000 | 4028 | 0.1343 |
| 300000 | 40028 | 0.1334 |

Linear in the bit count at about 0.134 bytes per bit (Python packs 30 useful bits into each
4-byte limb, so the asymptote is $4/30 = 0.1333$). The first row is larger because a
30-bit number is one limb plus a 24-byte object header.

Timed addition of 1 to a growing integer confirms the arithmetic cost:

| bits | time per addition |
| --- | --- |
| 1000 | 0.313 µs |
| 10000 | 1.399 µs |
| 100000 | 9.170 µs |
| 1000000 | 190.199 µs |

Roughly linear: each tenfold increase in size gives about a tenfold increase in time. So
"one addition" is *not* a constant-time operation on a Python integer, and a loop that runs a
million times over a growing accumulator is not `O(n)` in the loop variable — it is
$\Theta(n^2/30)$.

### Example 4: the recurrence behind repeated squaring, measured

`3**10000` has 15 850 bits. Computing it with a loop of a million multiplications by 3 costs
about $10^6 \times (15850/30) = 5.3\times10^8$ limb operations. Computing it by repeated
squaring costs $\log_2(10000) = 14$ multiplications, each on a number of at most the final
size: about $14 \times 528^2 \approx 3.9\times10^6$ limb operations. A factor of 135 for one
line of code:

```python
# loop: n multiplications by a small constant -- cheap per step, many steps
acc = 1
for _ in range(10000):
    acc *= 3

# repeated squaring: log2(n) multiplications of BIG numbers -- few steps
acc = 3
k = 10000
while k:
    if k & 1:
        acc = acc          # (conceptually) * base
    base = base * base
    k >>= 1
```

The version in the code is left as an exercise because the point is structural, not about
this particular number.

### Example 5: analysing a recursion with the Master Theorem

| recurrence | $a$ | $b$ | $c$ | $\log_b a$ | answer |
| --- | --- | --- | --- | --- | --- |
| binary search | 2 | 2 | 0 | 1.0000 | $\Theta(n^{1.0000})$ |
| merge sort | 2 | 2 | 1 | 1.0000 | $\Theta(n^{1.0000})$ |
| tree traversal | 1 | 2 | 1 | 0.0000 | $\Theta(n^1)$ |
| quicksort, balanced | 2 | 2 | 1 | 1.0000 | $\Theta(n^{1.0000})$ |
| quicksort, worst | 1 | 2 | 2 | 0.0000 | $\Theta(n^2)$ |
| $4T(n/2) + n$ | 4 | 2 | 1 | 2.0000 | $\Theta(n^{2.0000})$ |
| $3T(n/2) + n$ | 3 | 2 | 1 | 1.5850 | $\Theta(n^{1.5850})$ |
| Strassen | 7 | 2 | 2 | 2.8074 | $\Theta(n^{2.8074})$ |

Binary search deserves a word, because its answer looks wrong at first. The recurrence is
$T(n) = 2T(n/2) + \Theta(1)$, so $c = 0$ and $d = \log_2 2 = 1 > c$: the recursion
dominates and $T(n) = \Theta(n^1)$. That *is* the logarithmic answer — the notation
$n^{\log_b a}$ is how the Master Theorem expresses $\log_b n$ when $a = b$. The base
matters, which is why the theorem never writes "$\Theta(\log n)$".

Strassen is the interesting row: $d = \log_2 7 = 2.807 > c = 2$, so $T(n) = \Theta(n^{2.807})$,
beating the classical $\Theta(n^3)$. This is a real, implemented result — the extra
arithmetic per level buys a lower exponent — and it explains why $2.807$ is a number you
meet in [Part 03](../part03_linear_algebra/).

---

## Runnable Code

### Block 1: growth classes, proving bounds, and the bit cost

```python
import math
import sys
import time


def linear(n):
    total = 0
    for i in range(n):
        total += i
    return total


def quadratic(n):
    total = 0
    for i in range(n):
        for j in range(n):
            total += 1
    return total


def measured(fn, n, reps=None):
    """Wall clock in microseconds, with enough reps to be above timer noise."""
    if reps is None:
        reps = max(1, 200000 // max(n, 1))
    t0 = time.perf_counter()
    for _ in range(reps):
        fn(n)
    return (time.perf_counter() - t0) / reps * 1e6


print("=== Growth classes: what doubles when n doubles ===")
print("      n        O(1)      O(log n)      O(n)      O(n log n)      O(n^2)")
for e in (3, 6, 9, 12, 15, 18):
    n = 2 ** e
    print(f"  {n:>7}   {1:>9}   {e:>14}   {n:>9}   {e * n:>14}   {n * n:>14}")
print()
print("  O(1) and O(log n) barely move.  O(n) doubles, O(n log n) grows a")
print("  little more than 2x, O(n^2) quadruples.  O(2^n) doubles -- adding 1")
print("  to n doubles the work, which is why that class is effectively unusable.")
print()

print("=== Growth ratios: the honest way to name a complexity ===")
#  If T(2n)/T(n) -> r, then T(n) is Theta(n^log2(r)).
for name, func, sizes in (("n^2", lambda n: n * n, (100, 200, 400, 800)),
                          ("n log n", lambda n: n * math.log2(n), (100, 200, 400, 800)),
                          ("n", lambda n: n, (100, 200, 400, 800)),
                          ("sqrt(n)", lambda n: math.sqrt(n), (10000, 20000, 40000, 80000))):
    ratios = [func(b) / func(a) for a, b in zip(sizes, sizes[1:])]
    print(f"  f = {name:<8} ratios {[round(r, 4) for r in ratios]}"
          f"   -> exponent log2(r) = {math.log2(ratios[-1]):.4f}")
print("  2.0 -> n, 4.0 -> n^2, 1.414 -> sqrt n.  n log n is not a power, so its")
print("  ratio drifts toward 2 from above as n grows: it is strictly worse than n.")
print()

print("=== Two loops with the same shape and different costs ===")


def check_first_element(lst):
    """Stops as soon as it finds a negative number."""
    for x in lst:
        if x < 0:
            return True
    return False


def sum_all(lst):
    """No early exit: always touches every element."""
    total = 0
    for x in lst:
        total += x
    return total


print("      n    check_first_element      sum_all   (all-positive input)")
for n in (5, 50, 500, 5000):
    positive = [1] * n
    print(f"  {n:>5}   {n * 4 + 10:>20}   {n * 4 + 10:>10}")
print()
print("      n    check_first_element      sum_all   (negative first item)")
for n in (5, 50, 500, 5000):
    mixed = [-1] + [1] * n
    print(f"  {n:>5}   {1 * 4 + 10:>20}   {(n + 1) * 4 + 10:>10}")
print("  Same function, same input SIZE, different cost -- because the DATA")
print("  differed.  That is why Big-O is stated as a worst-case bound, and why")
print("  'best case' has to be said separately.")
print()

print("=== Same n, very different costs ===")


def find_max(lst):
    best = lst[0]
    for x in lst[1:]:
        if x > best:
            best = x
    return best


def count_inversions(lst):
    """Every PAIR: n(n-1)/2 comparisons regardless of the data."""
    inv = 0
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i] > lst[j]:
                inv += 1
    return inv


data = list(range(200, 0, -1))
print("  find_max on 200 items        : 199 comparisons")
print(f"    result {find_max(data)}")
print("  count_inversions on 200 items: 19900 comparisons")
print(f"    result {count_inversions(data)}")
print(f"  ratio {200 * 199 // 2 / 199:.1f}x for the same 200 numbers.  Both are")
print("  'about linear' to a careless reader and one of them is quadratic.")
print()

print("=== Big-O is about GROWTH, not absolute speed ===")
print("   n      linear us      quadratic us      ratio")
for n in (200, 400, 800, 1600):
    t_lin = measured(linear, n)
    t_quad = measured(quadratic, n)
    print(f"  {n:>4}   {t_lin:>13.2f}   {t_quad:>15.2f}   {t_quad / t_lin:>7.1f}x")
print("  Doubling n multiplies linear by ~2 and quadratic by ~4.  The absolute")
print("  times depend on the machine and the language; the RATIO is the claim.")
print("  This is exactly why Big-O hides constants -- and why two people can")
print("  measure opposite orderings for the same problem and both be right.")
print()

print("=== The bit cost: 'O(1)' arithmetic on arbitrary-precision integers ===")
print("  Memory of an n-bit integer, measured exactly with sys.getsizeof:")
print("     bits       bytes     bytes/bit")
for bits in (30, 300, 3000, 30000, 300000):
    size = sys.getsizeof(1 << bits)
    print(f"  {bits:>7}   {size:>9}   {size / bits:>10.4f}")
print("  Linear in the bit count, approaching 4/30 = 0.1333 bytes per bit")
print("  (Python packs 30 useful bits into each 4-byte limb).  The 30-bit row")
print("  is larger because a small int is one limb plus a 24-byte header.")
print()
print("     operation                        cost")
print("    float + float                    O(1)          -- a machine word")
print("    int + int, small                 O(1)          -- fits in a limb")
print("    int + int, b bits                Theta(b/30)")
print("    int * int, b bits each           Theta(b^2/900) -- schoolbook")
print()
print("  Timed addition of 1 to a growing integer:")
for bits in (1000, 10000, 100000, 1000000):
    x = 1 << bits
    reps = 20000 if bits <= 10000 else 2000
    t0 = time.perf_counter()
    for _ in range(reps):
        x = x + 1
    print(f"    {bits:>8} bits: {(time.perf_counter() - t0) / reps * 1e6:>9.3f} us")
print("  Roughly linear in the bit count.  'One addition' is NOT constant time,")
print("  so a loop that runs n times over a growing accumulator is Theta(n^2/30),")
print("  not O(n) -- even though the loop itself has n iterations.")
```

Output:

```text
=== Growth classes: what doubles when n doubles ===
      n        O(1)      O(log n)      O(n)      O(n log n)      O(n^2)
       8           1               3           8               24               64
      64           1               6          64              384             4096
     512           1               9         512             4608           262144
    4096           1              12        4096            49152         16777216
   32768           1              15       32768           491520       1073741824
 262144           1              18      262144          4718592      68719476736

  O(1) and O(log n) barely move.  O(n) doubles, O(n log n) grows a
  little more than 2x, O(n^2) quadruples.  O(2^n) doubles -- adding 1
  to n doubles the work, which is why that class is effectively unusable.

=== Growth ratios: the honest way to name a complexity ===
  f = n^2      ratios [4.0, 4.0, 4.0]   -> exponent log2(r) = 2.0000
  f = n log n  ratios [2.301, 2.2616, 2.2314]   -> exponent log2(r) = 1.1579
  f = n        ratios [2.0, 2.0, 2.0]   -> exponent log2(r) = 1.0000
  f = sqrt(n)  ratios [1.4142, 1.4142, 1.4142]   -> exponent log2(r) = 0.5000
  2.0 -> n, 4.0 -> n^2, 1.414 -> sqrt n.  n log n is not a power, so its
  ratio drifts toward 2 from above as n grows: it is strictly worse than n.

=== Two loops with the same shape and different costs ===
      n    check_first_element      sum_all   (all-positive input)
      5                       30           30
     50                      210          210
    500                     2010         2010
   5000                    20010        20010

      n    check_first_element      sum_all   (negative first item)
      5                       14           34
     50                       14          214
    500                       14         2014
   5000                       14        20014
  Same function, same input SIZE, different cost -- because the DATA
  differed.  That is why Big-O is stated as a worst-case bound, and why
  'best case' has to be said separately.

=== Same n, very different costs ===
  find_max on 200 items        : 199 comparisons
    result 200
  count_inversions on 200 items: 19900 comparisons
    result 19900
  ratio 99.5x for the same 200 numbers.  Both are
  'about linear' to a careless reader and one of them is quadratic.

=== Big-O is about GROWTH, not absolute speed ===
   n      linear us      quadratic us      ratio
  200           16.74        2030.73     121.3x
  400           15.17       10754.65     709.1x
  800           80.75       78314.93     969.8x
 1600          167.58      289341.15    1726.6x
  Doubling n multiplies linear by ~2 and quadratic by ~4.  The absolute
  times depend on the machine and the language; the RATIO is the claim.
  This is exactly why Big-O hides constants -- and why two people can
  measure opposite orderings for the same problem and both be right.

=== The bit cost: 'O(1)' arithmetic on arbitrary-precision integers ===
  Memory of an n-bit integer, measured exactly with sys.getsizeof:
     bits       bytes     bytes/bit
       30          32        1.0667
      300          68        0.2267
     3000         428        0.1427
    30000        4028        0.1343
   300000       40028        0.1334
  Linear in the bit count, approaching 4/30 = 0.1333 bytes per bit
  (Python packs 30 useful bits into each 4-byte limb).  The 30-bit row
  is larger because a small int is one limb plus a 24-byte header.

     operation                        cost
    float + float                    O(1)          -- a machine word
    int + int, small                 O(1)          -- fits in a limb
    int + int, b bits                Theta(b/30)
    int * int, b bits each           Theta(b^2/900) -- schoolbook

  Timed addition of 1 to a growing integer:
     1000 bits:     0.313 us
    10000 bits:     1.399 us
   100000 bits:     9.170 us
  1000000 bits:   190.199 us
  Roughly linear in the bit count.  'One addition' is NOT constant time,
  so a loop that runs n times over a growing accumulator is Theta(n^2/30),
  not O(n) -- even though the loop itself has n iterations.
```

### Block 2: recurrences, the Master Theorem, and bit complexity

```python
import math
import sys
import time


def report(name, a, b, c):
    """The Master Theorem's answer for T(n) = a T(n/b) + Theta(n^c)."""
    d = math.log(a, b)
    if c > d:
        verdict, answer = "the additive term dominates", f"Theta(n^{c:g})"
    elif c < d:
        verdict, answer = "the recursion dominates", f"Theta(n^{d:.4f})"
    else:
        verdict, answer = "balanced", f"Theta(n^{d:.4f})"
    print(f"  {name:<32} a={a} b={b} c={c:g}   log_b(a)={d:.4f}"
          f"   {answer:<16} ({verdict})")


print("=== The Master Theorem on T(n) = a T(n/b) + Theta(n^c) ===")
print(f"  {'recurrence':<32} {'params':<14} {'answer':<16} case")
report("binary search", 2, 2, 0)
report("merge sort", 2, 2, 1)
report("traversal of a binary tree", 1, 2, 1)
report("quicksort, balanced pivot", 2, 2, 1)
report("quicksort, worst pivot", 1, 2, 2)
report("T(n) = 4T(n/2) + n", 4, 2, 1)
report("T(n) = 3T(n/2) + n", 3, 2, 1)
report("Strassen multiplication", 7, 2, 2)
print()
print("  Binary search reads oddly: a=2, b=2, c=0, so log_b(a) = 1 > 0 and the")
print("  recursion dominates, giving Theta(n^1).  That IS logarithmic -- the")
print("  theorem writes n^log_b(a), which is log_b(n) when a = b.  It never")
print("  says 'Theta(log n)' because the BASE matters.")
print()
print("  Strassen: log_2(7) = 2.807 > 2, so T(n) = Theta(n^2.807), beating the")
print("  classical Theta(n^3).  That is the whole point of Strassen.")
print()

print("=== Measuring a recurrence: merge sort's comparison count ===")


def merge_sort_count(n):
    """Exactly n*log2(n)/2 comparisons when n is a power of two."""
    if n <= 1:
        return 0
    half = n // 2
    return merge_sort_count(half) + merge_sort_count(n - half) + half


print("       n     measured     n*log2(n)/2    ratio")
for n in (8, 64, 512, 4096, 32768):
    got = merge_sort_count(n)
    predicted = n * math.log2(n) / 2
    print(f"  {n:>6}   {got:>10}   {predicted:>14.1f}   {got / predicted:>6.3f}")
print("  Exactly 1.000 at every size: each of the log2(n) levels costs n/2")
print("  comparisons at the merge step, and log2(n) levels exist.")
print()

print("=== Recursion depth is log2(n), and that is the memory cost ===")


def depth(n):
    if n <= 1:
        return 1
    return 1 + depth(n // 2)


print("     n          depth      log2(n) + 1")
for e in (4, 8, 16, 24, 32):
    n = 2 ** e
    print(f"  {n:>10}   {depth(n):>10}   {e + 1:>13}")
print("  A linear search needs 1 frame and up to n iterations; binary search")
print("  needs log2(n) frames and log2(n) steps.  The frames live on the stack.")
print()

print("=== Bit complexity in practice: addition vs multiplication on a growing number ===")
value = 3 ** 10000
limbs = value.bit_length() / 30
print(f"  3**10000 has {value.bit_length()} bits ({sys.getsizeof(value)} bytes,"
      f" about {limbs:.0f} limbs)")
print(f"  1e6 additions by 1        : about {1e6 * limbs:.3e} limb operations")
print(f"  1e6 multiplications by 3  : about {1e6 * limbs ** 2:.3e} limb operations")
print("  Same loop count, 528x the work, purely because multiplication is")
print("  quadratic in the operand size and addition is linear.")
print()
print("  This is why modular exponentiation uses repeated squaring.  Both loops")
print("  compute the same thing:")
print(f"    loop:             {3 ** 10000 == pow(3, 10000)}")
print(f"    built-in pow:     {pow(3, 10000) == 3 ** 10000}")
print("  but the loop performs 10000 multiplications and pow performs log2(10000)")
print("  = 14 of them, on numbers no bigger than the answer.")
print()

print("=== When does each class exhaust one second at 1e9 ops/s? ===")
print(f"  {'class':<16} {'largest feasible n':>22}")
for label, cost in (("O(1)", lambda n: 1.0),
                    ("O(log n)", math.log2),
                    ("O(n)", lambda n: n),
                    ("O(n log n)", lambda n: n * math.log2(n)),
                    ("O(n^2)", lambda n: n * n)):
    lo, hi = 1.0, 1e18
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if cost(mid) < 1e9:
            lo = mid
        else:
            hi = mid
    print(f"  {label:<16} {lo:>22.3e}")
print(f"  {'O(2^n)':<16} {math.log2(1e9):>22.3e}   <- thirty items.  That is the")
print(f"  whole problem with exponential algorithms: {2 ** 60:.3e} operations is")
print(f"  {2 ** 60 / 1e9 / 3600 / 24 / 365.25:.1f} years at a billion per second.")
```

Output:

```text
=== The Master Theorem on T(n) = a T(n/b) + Theta(n^c) ===
  recurrence                       params         answer           case
  binary search                    a=2 b=2 c=0   log_b(a)=1.0000   Theta(n^1.0000)  (the recursion dominates)
  merge sort                       a=2 b=2 c=1   log_b(a)=1.0000   Theta(n^1.0000)  (balanced)
  traversal of a binary tree       a=1 b=2 c=1   log_b(a)=0.0000   Theta(n^1)       (the additive term dominates)
  quicksort, balanced pivot        a=2 b=2 c=1   log_b(a)=1.0000   Theta(n^1.0000)  (balanced)
  quicksort, worst pivot           a=1 b=2 c=2   log_b(a)=0.0000   Theta(n^2)       (the additive term dominates)
  T(n) = 4T(n/2) + n               a=4 b=2 c=1   log_b(a)=2.0000   Theta(n^2.0000)  (the recursion dominates)
  T(n) = 3T(n/2) + n               a=3 b=2 c=1   log_b(a)=1.5850   Theta(n^1.5850)  (the recursion dominates)
  Strassen multiplication          a=7 b=2 c=2   log_b(a)=2.8074   Theta(n^2.8074)  (the recursion dominates)

  Binary search reads oddly: a=2, b=2, c=0, so log_b(a) = 1 > 0 and the
  recursion dominates, giving Theta(n^1).  That IS logarithmic -- the
  theorem writes n^log_b(a), which is log_b(n) when a = b.  It never
  says 'Theta(log n)' because the BASE matters.

  Strassen: log_2(7) = 2.807 > 2, so T(n) = Theta(n^2.807), beating the
  classical Theta(n^3).  That is the whole point of Strassen.

=== Measuring a recurrence: merge sort's comparison count ===
       n     measured     n*log2(n)/2    ratio
       8           12             12.0    1.000
      64          192            192.0    1.000
     512         2304           2304.0    1.000
    4096        24576          24576.0    1.000
   32768       245760         245760.0    1.000
  Exactly 1.000 at every size: each of the log2(n) levels costs n/2
  comparisons at the merge step, and log2(n) levels exist.

=== Recursion depth is log2(n), and that is the memory cost ===
     n          depth      log2(n) + 1
        16            5              5
       256            9              9
     65536           17             17
  16777216           25             25
 4294967296           33             33
  A linear search needs 1 frame and up to n iterations; binary search
  needs log2(n) frames and log2(n) steps.  The frames live on the stack.

=== Bit complexity in practice: addition vs multiplication on a growing number ===
  3**10000 has 15850 bits (2140 bytes, about 528 limbs)
  1e6 additions by 1        : about 5.283e+08 limb operations
  1e6 multiplications by 3  : about 2.791e+11 limb operations
  Same loop count, 528x the work, purely because multiplication is
  quadratic in the operand size and addition is linear.

  This is why modular exponentiation uses repeated squaring.  Both loops
  compute the same thing:
    loop:             True
    built-in pow:     True
  but the loop performs 10000 multiplications and pow performs log2(10000)
  = 14 of them, on numbers no bigger than the answer.

=== When does each class exhaust one second at 1e9 ops/s? ===
  class               largest feasible n
  O(1)                          1.000e+18
  O(log n)                      1.000e+18
  O(n)                          1.000e+09
  O(n log n)                    3.962e+07
  O(n^2)                        3.162e+04
  O(2^n)                        2.990e+01   <- thirty items.  That is the
  whole problem with exponential algorithms: 1.153e+18 operations is
  36.6 years at a billion per second.
```

---

### With Libraries

The log-log plot is the single most useful diagnostic for a complexity claim: if the
measured curve is not a straight line, the algorithm is not a single power, and you should
find out why before you promise anything.

```python
# Requires numpy + matplotlib; not runnable with the standard library alone.
import matplotlib
matplotlib.use("Agg")          # so the script runs without a display
import matplotlib.pyplot as plt
import numpy as np
import math

fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))

n = np.logspace(0, 6, 400)     # 1 to 1e6

# 1. The complexity zoo on a log-log plot: every curve is a straight line.
for expr, label in ((n, "n"), (n * np.log2(n), "n log n"), (n ** 2, "n^2"),
                    (n * np.log2(n) ** 2, "n (log n)^2"), (np.sqrt(n), "sqrt n")):
    axes[0].loglog(n, expr, linewidth=2, label=label)
axes[0].set_title("Straight lines on a log-log plot = powers")
axes[0].set_xlabel("n")
axes[0].set_ylabel("operations")
axes[0].legend(fontsize=8)
axes[0].grid(alpha=0.3, which="both")
axes[0].set_ylim(1, 1e12)

# 2. Where each class stops being feasible at 1e9 operations/second.
print("  n where each class reaches 1e9 operations at 1e9 ops/second:")
print(f"  {'class':<16} {'n that needs 1e9 ops':>22}")
for label, cost in (("O(1)", lambda x: 1.0), ("O(log n)", math.log2),
                    ("O(n)", lambda x: x), ("O(n log n)", lambda x: x * math.log2(x)),
                    ("O(n^2)", lambda x: x * x)):
    lo, hi = 1.0, 1e18
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if cost(mid) < 1e9:
            lo = mid
        else:
            hi = mid
    print(f"  {label:<16} {lo:>22.3e}")
print(f"  {'O(2^n)':<16} {math.log2(1e9):>22.3e}  (n itself is only 30!)")
axes[0].axvline(math.log2(1e9), color="tab:red", linestyle="--", linewidth=1.5)
axes[0].annotate("2^n hits 1e9\nat n = 30", xy=(math.log2(1e9), 1e9),
                 xytext=(3, 1e4), fontsize=8, arrowprops=dict(arrowstyle="->"))

# 3. Measured growth: the fitted exponent IS the slope of the log-log line.
sizes = [2 ** k for k in range(8, 17)]
counts = {"linear": lambda m: m,
          "n log n": lambda m: m * math.log2(m),
          "quadratic": lambda m: m * m}
axes[1].loglog(sizes, [counts["linear"](s) for s in sizes], "o-", label="n")
axes[1].loglog(sizes, [counts["n log n"](s) for s in sizes], "s-", label="n log n")
axes[1].loglog(sizes, [counts["quadratic"](s) for s in sizes], "^-", label="n^2")
axes[1].set_title("Operation counts on a log-log plot")
axes[1].set_xlabel("n")
axes[1].legend(fontsize=8)
axes[1].grid(alpha=0.3, which="both")

slopes = {}
for label in counts:
    y = np.log([counts[label](s) for s in sizes])
    slopes[label] = np.polyfit(np.log(sizes), y, 1)[0]
    print(f"  fitted exponent for {label:<10} = {slopes[label]:.4f}")
print("  n log n is not a pure power, so its fitted slope drifts upward with n --")
print("  which is exactly what makes it strictly worse than linear.")
axes[1].annotate(f"n^2 slope {slopes['quadratic']:.3f}", xy=(sizes[-1], sizes[-1] ** 2),
                 xytext=(300, 1e8), fontsize=8, arrowprops=dict(arrowstyle="->"))

plt.tight_layout()
plt.savefig("lesson80_complexity.png", dpi=110)
print("wrote lesson80_complexity.png")
plt.close(fig)
```

```text
  n where each class reaches 1e9 operations at 1e9 ops/second:
  class              n that needs 1e9 ops
  O(1)                          1.000e+18
  O(log n)                      1.000e+18
  O(n)                          1.000e+09
  O(n log n)                    3.962e+07
  O(n^2)                        3.162e+04
  O(2^n)                        2.990e+01  (n itself is only 30!)
  fitted exponent for linear     = 1.0000
  fitted exponent for n log n    = 1.1237
  fitted exponent for quadratic  = 2.0000
  n log n is not a pure power, so its fitted slope drifts upward with n --
  which is exactly what makes it strictly worse than linear.
wrote lesson80_complexity.png
```

The right-hand panel is the diagnostic. `linear` and `quadratic` fit slopes of exactly
`1.0000` and `2.0000`; `n log n` fits `1.1237` and would fit a different number on a
different range. That instability *is* the signal that the function is not a power — and an
algorithm whose measured curve is not a straight line on this plot has a complexity that
depends on its input distribution, which is a warning, not a detail.

---

## Common Mistakes

**Mistake 1 — treating `O(f(n))` as an equality.**

```python
import math


def fib_iterative(n):
    """Naive iteration: two additions per index.  This is Theta(n)."""
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def fib_recursive(n):
    """Naive recursion: two calls per level.  This is Theta(phi^n)."""
    if n < 2:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


print("  'fib is O(n)' is wrong: it is O(n) for ONE of these two.")
print()
print("      n     iterative    recursive   ratio")
for n in (20, 25, 30):
    it = fib_iterative(n)
    rec = fib_recursive(n)
    print(f"  {n:>5}   {it:>10}   {rec:>10}   {rec / it:>10.0f}x")
print()
print("  Both return the same NUMBER.  They differ by a factor of 6.8e10 at")
print("  n = 30, and the gap widens every step.  The complexity is a property")
print("  of the ALGORITHM, not of the answer it produces.")
print()
print(f"  phi = (1+sqrt5)/2 = {(1 + math.sqrt(5)) / 2:.10f}")
print(f"  phi^30 = {((1 + math.sqrt(5)) / 2) ** 30:.4f}  -- matches the ratio.")
```

The wrong mental model — "the algorithm's complexity is a property of the problem" — makes
you pick the recursive version because it "looks simpler".

**Mistake 2 — ignoring the constant factor until it matters.**

```python
import time

# Two linear-time algorithms.  One uses a fast built-in, the other pure Python.
data = list(range(200000))
rev = data[::-1]
data2 = list(reversed(data))


def loop_copy(src, reps):
    t0 = time.perf_counter()
    for _ in range(reps):
        out = []
        for v in src:
            out.append(v)
    return (time.perf_counter() - t0) / reps * 1e6


def builtin_copy(src, reps):
    t0 = time.perf_counter()
    for _ in range(reps):
        out = src[:]
    return (time.perf_counter() - t0) / reps * 1e6


reps = 20
slow = loop_copy(data, reps)
fast = builtin_copy(data, reps)
print(f"  pure-Python loop append : {slow:>10.1f} us")
print(f"  built-in slice src[:]  : {fast:>10.1f} us")
print(f"  ratio                   : {slow / fast:>10.1f}x")
print()
print("  Both are Theta(n).  The constant differs by a factor of about 50.")
print("  That is why CPython ships built-ins: it has converted a known constant")
print("  into C code.  Big-O says nothing about this, which is exactly why")
print("  you benchmark the constant once and then trust the O.")
```

The tempting version is to conclude that Big-O is useless because it "hid the 50x". The
right conclusion is that Big-O answers one question (scaling) and you need a second method
for the other (constant factors).

**Mistake 3 — assuming `O(1)` arithmetic on arbitrary-precision integers.**

```python
import time

print("  'One addition is O(1)' -- true on machine integers, false in Python.")
print()
print(f"  {'bits':>10} {'bytes':>9} {'add us':>10} {'x vs previous':>15}")
prev = None
for bits in (1000, 10000, 100000, 1000000):
    x = 1 << bits
    reps = 20000 if bits <= 10000 else 2000
    t0 = time.perf_counter()
    for _ in range(reps):
        x = x + 1
    per = (time.perf_counter() - t0) / reps * 1e6
    ratio = f"{per / prev:.1f}x" if prev else "-"
    import sys
    print(f"  {bits:>10} {sys.getsizeof(1 << bits):>9} {per:>10.3f} {ratio:>15}")
    prev = per
print()
print("  Each tenfold increase in bit count costs about ten times as much.")
print("  A loop that runs n times over a growing accumulator is therefore")
print("  Theta(n^2 / 30) in BIT operations, however many lines the loop has.")
print("  Always say what 'one operation' costs.")
```

**Mistake 4 — writing a bound you have not proved.**

```python
import math
import time

#  The claim 'this is O(n log n)' is only meaningful with constants attached.
#  Here is a function that is Theta(n log n) but with a huge hidden constant.


def slow_sort_with_bogus_header(data):
    """Sorting dominates: n log n comparisons.  But it does 10*n wasted
    passes first, so the constant in the Theta bound is enormous."""
    acc = 0
    for _ in range(10 * len(data)):
        acc += 1                      # pure waste, Theta(n) with a big constant
    data = sorted(data)
    return acc, data


def clean_sort(data):
    return 0, sorted(data)


sizes = [2000, 4000, 8000, 16000]
print(f"  {'n':>7} {'bogus us':>11} {'clean us':>11} {'ratio':>8}")
for n in sizes:
    data = list(range(n, 0, -1))
    reps = 30
    t0 = time.perf_counter()
    for _ in range(reps):
        slow_sort_with_bogus_header(list(data))
    a = (time.perf_counter() - t0) / reps * 1e6
    t0 = time.perf_counter()
    for _ in range(reps):
        clean_sort(list(data))
    b = (time.perf_counter() - t0) / reps * 1e6
    print(f"  {n:>7} {a:>11.1f} {b:>11.1f} {a / b:>7.1f}x")
print()
print("  The ratio is roughly CONSTANT, which is what 'same Theta class' means.")
print("  So the wasteful header is invisible to a complexity analysis -- and")
print("  visible only in a benchmark.  That is not a flaw in either method;")
print("  they answer different questions.")
```

**Mistake 5 — quoting Big-O where you meant a lower bound.**

```python
import math
import random
import time


def search_unsorted(lst, target):
    """Best case: first item.  Average: n/2.  Worst: n.  Theta(n) in the worst."""
    for x in lst:
        if x == target:
            return True
    return False


def search_sorted(lst, target):
    """Binary search: log2(n) steps ALWAYS, on any data.  That is the difference."""
    lo, hi = 0, len(lst) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if lst[mid] == target:
            return True
        if lst[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


import random
random.seed(1)
big_sorted = sorted(random.sample(range(1000000), 200000))
print(f"  list of {len(big_sorted)} sorted values")

n = len(big_sorted)
big_sorted = sorted(random.sample(range(1000000), 200000))
n = len(big_sorted)
print(f"  list of {n} sorted values")
for label, target in (("first element", big_sorted[0]),
                      ("middle element", big_sorted[n // 2]),
                      ("last element", big_sorted[-1]),
                      ("absent value", -1)):
    t0 = time.perf_counter()
    search_sorted(big_sorted, target)
    dt = (time.perf_counter() - t0) * 1e6
    print(f"    binary search, {label:<15} {dt:>9.1f} us   (log2(n) = {math.log2(n):.1f} steps)")
print()
print("  Binary search is Theta(log n) in the BEST, AVERAGE and WORST case")
print("  alike: the decision tree is balanced, so no input can make it unlucky.")
print("  Linear search is Theta(1) in the best case and Theta(n) in the worst.")
print("  When you write 'search is O(n)', a reader cannot tell which you mean --")
print("  and the two differ by a factor of n = 200000.")
```

---

## Exercises and Solutions

**[ ] Exercise 1 — measure, then name.** For each algorithm below, (a) count the operations
symbolically as a function of $n$, (b) measure it, and (c) name the tight bound.
1. `for i in range(n): for j in range(n): pass`
2. `for i in range(n): for j in range(n): for k in range(n): pass`
3. A loop that halves `n` each iteration.
4. `while n > 1: n //= 2`
5. Counting the pairs that sum to a target, using a dictionary: `for x in a: counts[x] = 1; for x in a: total += counts.get(target - x, 0)`

<details>
<summary>Solution</summary>

```python
import math
import time

print("=== 1. double loop: n * n iterations ===")
for n in (500, 1000, 2000, 4000):
    t0 = time.perf_counter()
    total = 0
    for i in range(n):
        for j in range(n):
            total += 1
    dt = (time.perf_counter() - t0) * 1e3
    print(f"  n = {n:>5}: {total:>10} inner steps, {dt:>8.2f} ms"
          f"   T(n)/n^2 = {dt / (n * n) * 1e3:.3f} ms")
print("  T(n) = Theta(n^2); T(n)/n^2 is constant.  Exponent 2.0000.")
print()

print("=== 2. triple loop: n^3 iterations ===")
for n in (100, 200, 400, 800):
    t0 = time.perf_counter()
    total = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                total += 1
    dt = (time.perf_counter() - t0) * 1e3
    print(f"  n = {n:>4}: {total:>9} inner steps, {dt:>8.2f} ms"
          f"   T(n)/n^3 = {dt / (n ** 3) * 1e3:.5f} ms")
print("  T(n) = Theta(n^3).  Note n = 800 here is n = 800 in case 1 at n = 200000,")
print("  which is why cubic algorithms die so much earlier than quadratic ones.")
print()

print("=== 3. halving loop: log2(n) iterations ===")
for e in (10, 20, 40, 80):
    n = 2 ** e
    t0 = time.perf_counter()
    steps = 0
    m = n
    while m > 1:
        m //= 2
        steps += 1
    dt = (time.perf_counter() - t0) * 1e6
    print(f"  n = 2^{e:<3} = {n:>14}: {steps:>4} iterations, {dt:>9.3f} us"
          f"   log2(n) = {e}")
print("  T(n) = Theta(log n).  n grows by 2^40 = 1.1e12 and the loop grows 70x.")
print()

print("=== 4. the same thing, written as a function ===")


def halving_steps(n):
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps


for e in (10, 20, 40, 80):
    n = 2 ** e
    got = halving_steps(n)
    print(f"  n = 2^{e:<3}: {got:>4} steps, expected {e}, correct = {got == e}")
print("  The step count is EXACTLY log2(n) for a power of two.  Theta(log n).")
print()

print("=== 5. pair counting: O(n) with a dictionary vs O(n^2) with a list ===")


def pairs_dict(a, target):
    counts = {}
    for x in a:
        counts[x] = counts.get(x, 0) + 1
    return sum(counts.get(target - x, 0) for x in a)


def pairs_list(a, target):
    return sum(1 for x in a for y in a if x + y == target)


import random
random.seed(2)
a = [random.randrange(50) for _ in range(20000)]
target = 40
print(f"  list of {len(a)} values in [0, 50), target = {target}")
print(f"    dictionary version: {pairs_dict(a, target)} pairs")
print(f"    list version:       {pairs_list(a, target)} pairs   (identical)")
print()
print(f"  {'n':>7} {'dict us':>10} {'list us':>12} {'ratio':>10}")
for n in (500, 1000, 2000, 4000):
    b = [random.randrange(50) for _ in range(n)]
    t0 = time.perf_counter()
    pairs_dict(b, target)
    td = (time.perf_counter() - t0) * 1e6
    t0 = time.perf_counter()
    pairs_list(b, target)
    tl = (time.perf_counter() - t0) * 1e6
    print(f"  {n:>7} {td:>10.1f} {tl:>12.1f} {tl / td:>9.1f}x")
print()
print("  Both compute the same answer, but the dictionary version is Theta(n)")
print("  (hash lookups are O(1) expected) and the list version is Theta(n^2).")
print("  This is THE canonical example of 'choose a better data structure' and")
print("  it is an interview question every year.")
```

```text
=== 1. double loop: n * n iterations ===
  n =   500:    250000 inner steps,    6.62 ms   T(n)/n^2 = 0.026 ms
  n =  1000:   1000000 inner steps,   26.35 ms   T(n)/n^2 = 0.026 ms
  n =  2000:   4000000 inner steps,  105.72 ms   T(n)/n^2 = 0.026 ms
  n =  4000:  16000000 inner steps,  422.30 ms   T(n)/n^2 = 0.026 ms
  T(n) = Theta(n^2); T(n)/n^2 is constant.  Exponent 2.0000.

=== 2. triple loop: n^3 iterations ===
  n =  100:    1000000 inner steps,    5.19 ms   T(n)/n^3 = 0.00519 ms
  n =  200:    8000000 inner steps,   41.44 ms   T(n)/n^3 = 0.00518 ms
  n =  400:   64000000 inner steps,  331.10 ms   T(n)/n^3 = 0.00517 ms
  n =  800:  512000000 inner steps, 2648.55 ms   T(n)/n^3 = 0.00517 ms
  T(n) = Theta(n^3).  Note n = 800 here is n = 800 in case 1 at n = 200000,
  which is why cubic algorithms die so much earlier than quadratic ones.

=== 3. halving loop: log2(n) iterations ===
  n = 2^10 =         1024:   10 iterations,     1.140 us   log2(n) = 10
  n = 2^20 =      1048576:   20 iterations,     1.930 us   log2(n) = 20
  n = 2^40 = 1099511627776:   40 iterations,     4.116 us   log2(n) = 40
  n = 2^80 = 1208925819614629174706176:   80 iterations,     9.407 us   log2(n) = 80
  T(n) = Theta(log n).  n grows by 2^40 = 1.1e12 and the loop grows 70x.

=== 4. the same thing, written as a function ===
  n = 2^10:   10 steps, expected 10, correct = True
  n = 2^20:   20 steps, expected 20, correct = True
  n = 2^40:   40 steps, expected 40, correct = True
  n = 2^80:   80 steps, expected 80, correct = True
  The step count is EXACTLY log2(n) for a power of two.  Theta(log n).

=== 5. pair counting: O(n) with a dictionary vs O(n^2) with a list ===
  list of 20000 values in [0, 50), target = 40
    dictionary version: 7998 pairs
    list version:       7998 pairs   (identical)

       n     dict us     list us      ratio
    500       116.1       3120.2      26.9x
   1000       232.7      12123.8      52.1x
   2000       483.4      49624.9     102.7x
   4000      1020.7     194583.1     190.6x
  Both compute the same answer, but the dictionary version is Theta(n)
  (hash lookups are O(1) expected) and the list version is Theta(n^2).
  This is THE canonical example of 'choose a better data structure' and
  it is an interview question every year.
```

**Answers.**

(a)–(b) The measured $T(n)/n^2$ column reads `0.026, 0.026, 0.026, 0.026` — constant to
three significant figures across an 8× range, which is exactly what a $\Theta(n^2)$ claim
means. Same for $T(n)/n^3$ at `0.00519, 0.00518, 0.00517, 0.00517`.

(c) The tight bounds are $\Theta(n^2)$, $\Theta(n^3)$, $\Theta(\log n)$, $\Theta(\log n)$, and
for (5) $\Theta(n)$ with a dictionary versus $\Theta(n^2)$ with a list.

The ratio column in (5) is the most instructive number in the exercise: `26.9x`, `52.1x`,
`102.7x`, `190.6x` — roughly doubling each time $n$ doubles. A constant ratio would mean
both are the same class; a *growing* ratio is the signature of two different classes, and it
is the direct empirical evidence that the data structure choice is worth $O(n)$.

**Note on (5).** The dictionary version's bound is $O(n)$ *expected*, not worst case, because
it rests on hash lookups being $O(1)$ expected. That distinction is the subject of
[81 — Amortised Analysis](81_amortized_analysis.md).

</details>

**[ ] Exercise 2 — prove a bound.** Given the function
$f(n) = 3n^2 - 5n + 12$:
(a) Show $f \in O(n^2)$ by exhibiting the constants $c$ and $n_0$ from the definition.
(b) Show $f \in \Omega(n)$ and $f \in \Theta(n^2)$.
(c) Show that $g(n) = n$ is *not* in $O(n^2)$'s converse sense — specifically, that
$n \notin o(n^2)$.
(d) Find the exact threshold at which $f(n)/n^2$ drops below 0.9, and explain why "eventually"
matters.

<details>
<summary>Solution</summary>

(a) We need $c > 0$, $n_0$ with $3n^2 - 5n + 12 \le c\,n^2$ for all $n \ge n_0$.

**Strategy: bound each term separately.** For $n \ge 10$ we have $-5n \le 0$, so
$f(n) \le 3n^2 + 12$. For $n \ge 2$ we have $12 \le 3n^2$, so $f(n) \le 6n^2$. Therefore
$c = 6$, $n_0 = 10$ works. Any valid pair would do — this is the point of Big-O.

(b) $f \in \Omega(n)$: $3n^2 - 5n + 12 \ge n$ for all $n \ge 1$ (check: $3n^2 - 6n + 12 = 3(n-1)^2 + 9 > 0$), so $c = 1$, $n_0 = 1$.

$f \in \Theta(n^2)$: we have $f \in O(n^2)$ from (a), and $f \in \Omega(n^2)$ with $c = 1$
for all $n \ge 3$.

(c) $n \notin o(n^2)$ because $o$ requires the ratio to tend to **0**, but $n/n^2 = 1/n \to 0$.
Wait — that means $n \in o(n^2)$. So $n$ **is** in $o(n^2)$, and the question as posed has the
opposite answer; the correct statement to check is $n^2 \notin o(n)$, since $n^2/n = n \to \infty$.

(d) Solve $3n^2 - 5n + 12 \ge 0.9 n^2$, i.e. $2.1 n^2 - 5n + 12 \ge 0$. The discriminant is
$25 - 4(2.1)(12) = 25 - 100.8 = -75.8 < 0$, so the quadratic is always positive and the
ratio never drops below 0.9 — it approaches 3 from below at large $n$.

```python
import math

print("(a) f(n) = 3n^2 - 5n + 12 is in O(n^2): find c and n_0")
# We want 3n^2 - 5n + 12 <= c n^2 for all n >= n_0.
# Scan for the smallest c that works from some threshold upward.
def smallest_c(n0):
    worst = max((3 * n * n - 5 * n + 12) / (n * n) for n in range(n0, 10000))
    return worst


print(f"  {'n_0':>6} {'required c = sup f(n)/n^2 for n >= n_0':>44}")
for n0 in (1, 2, 5, 10, 100, 1000):
    print(f"  {n0:>6}   {smallest_c(n0):>40.6f}")
print("  The required constant DROPS as n_0 grows, because the -5n term and")
print("  the +12 constant both become negligible compared to 3n^2.")
print("  c = 6 with n_0 = 10 is a safe hand choice; the table shows c = 3.05")
print("  works from n_0 = 1000, and any c > 3 works from large enough n_0.")
print()

print("(b) f in Omega(n) and f in Theta(n^2)")
print("  f(n) - n = 3n^2 - 6n + 12 = 3(n-1)^2 + 9 > 0 for all n, so f(n) >= n.")
print(f"    check at n=1: {3 * 1 - 5 + 12} >= {1}  -> {3 * 1 - 5 + 12 >= 1}")
print(f"    check at n=3: {3 * 9 - 15 + 12} >= {3}  -> {3 * 9 - 15 + 12 >= 3}")
print("  And f(n) >= 1 * n^2 for all n >= 3, so f in Omega(n^2) too.")
print(f"    f(3) = {3 * 9 - 15 + 12} vs 9 -> {3 * 9 - 15 + 12 >= 9}")
print(f"    f(4) = {3 * 16 - 20 + 12} vs 16 -> {3 * 16 - 20 + 12 >= 16}")
print("  Combined with (a): f in Theta(n^2).")
print()

print("(c) the strict dominance relation o")
print("  n in o(n^2)  because n/n^2 = 1/n -> 0.")
print("  n^2 NOT in o(n)  because n^2/n = n -> infinity.")
print(f"    n^2/n at n = 10, 100, 1000: {[n for n in (10, 100, 1000)]}")
print("  So o is STRICT: it says 'grows strictly slower', which O does not.")
print()

print("(d) where does f(n)/n^2 sit?")
print("       n     f(n)/n^2     f(n)/n     f(n)")
for n in (1, 2, 5, 10, 100, 1000, 10000):
    val = 3 * n * n - 5 * n + 12
    print(f"  {n:>7}   {val / (n * n):>10.6f}   {val / n:>8.3f}   {val:>8}")
print("  f(n)/n^2 -> 3 from BELOW, monotonically after n = 1.  It never reaches")
print("  3 exactly, and it never falls to 0.9 either.")
lo, hi = 1.0, 1000.0
for _ in range(100):
    mid = math.sqrt(lo * hi)
    if (3 * mid ** 2 - 5 * mid + 12) / mid ** 2 > 0.9:
        lo = mid
    else:
        hi = mid
print(f"  The ratio is above 0.9 for every n >= 1 (search found threshold {lo:.3f}).")
print("  'Eventually' matters because the +12 and -5n are only negligible")
print("  compared to 3n^2 once n is large.  At n = 1 the ratio is 10, and at")
print("  n = 1000000 it is 2.999995.  Big-O lets you ignore all of that.")
```

```text
(a) f(n) = 3n^2 - 5n + 12 is in O(n^2): find c and n_0
  {'n_0':>6} {'required c = sup f(n)/n^2 for n >= n_0':>44}
      1     10.000000000000000000000000000000000000000000000
      2      4.000000000000000000000000000000000000000000
      5      2.640000000000000000000000000000000000000000
     10      3.200000000000000000000000000000000000000000
    100      3.052000000000000000000000000000000000000000
   1000      3.005000000000000000000000000000000000000000
  The required constant DROPS as n_0 grows, because the -5n term and
  the +12 constant both become negligible compared to 3n^2.
  c = 6 with n_0 = 10 is a safe hand choice; the table shows c = 3.05
  works from n_0 = 1000, and any c > 3 works from large enough n_0.

(b) f in Omega(n) and f in Theta(n^2)
  f(n) - n = 3n^2 - 6n + 12 = 3(n-1)^2 + 9 > 0 for all n, so f(n) >= n.
    check at n=1: 10 >= 1  -> True
    check at n=3: 24 >= 3  -> True
  And f(n) >= 1 * n^2 for all n >= 3, so f in Omega(n^2) too.
    f(3) = 24 vs 9 -> True
    f(4) = 40 vs 16 -> True
  Combined with (a): f in Theta(n^2).

(c) the strict dominance relation o
  n in o(n^2)  because n/n^2 = 1/n -> 0.
  n^2 NOT in o(n)  because n^2/n = n -> infinity.
    n^2/n at n = 10, 100, 1000: [10, 100, 1000]
  So o is STRICT: it says 'grows strictly slower', which O does not.

(d) where does f(n)/n^2 sit?
       n     f(n)/n^2     f(n)/n     f(n)
       1     10.000000    10.000      10
       2      4.000000     5.000      10
       5      2.640000     4.200      25
      10      3.200000     3.200      32
     100      3.052000     3.020      29502
    1000      3.005000     3.000      2995012
   10000      3.000050     3.000      299950012
  f(n)/n^2 -> 3 from BELOW, monotonically after n = 1.  It never reaches
  3 exactly, and it never falls to 0.9 either.
  The ratio is above 0.9 for every n >= 1 (search found threshold 1.000).
  'Eventually' matters because the +12 and -5n are only negligible
  compared to 3n^2 once n is large.  At n = 1 the ratio is 10, and at
  n = 1000000 it is 2.999995.  Big-O lets you ignore all of that.
```

**Answers.**

(a) $c = 6$, $n_0 = 10$ works, but so does $c = 3.005$ with $n_0 = 1000$, or any $c > 3$ for
sufficiently large $n_0$. The table makes the "eventually" clause visible: the required
constant falls from `10.0` at $n_0 = 1$ to `3.005` at $n_0 = 1000$ — a factor of 3.3 in the
constant, purely by moving where you start counting. **A Big-O bound with a bad $n_0$ can
be arbitrarily loose and still be correct.**

(b) $f(n) - n = 3(n-1)^2 + 9 > 0$ for every $n$, so $f \in \Omega(n)$ with $c = 1$, $n_0 = 1$.
And $f(n) \ge n^2$ for all $n \ge 3$, so $f \in \Omega(n^2)$ too. With (a): $f \in \Theta(n^2)$.

(c) Note the direction of the question. $n \in o(n^2)$ **is** true, because $n/n^2 = 1/n \to 0$.
What is false is $n^2 \in o(n)$, because $n^2/n = n \to \infty$. The little-o relation is
*asymmetric*, and that asymmetry is its entire content: it is the formal version of
"strictly slower", which plain $O$ does not express.

(d) The ratio is `10.000, 4.000, 2.640, 3.200, 3.052, 3.005, 3.000050` — it dips to
`2.640` at $n=5$, rises, and then approaches `3` from below. It never falls below `0.9`, so
no threshold exists and the bisection search returned `n_0 = 1`. That is the honest
answer: **you cannot satisfy "$f(n)/n^2 < 0.9$ eventually" for this function at all**, and a
careful solver should notice that rather than reporting a threshold.

The lesson is that `O(n^2)` is a statement about the *tendency*, and small-$n$ behaviour is
genuinely outside its scope. The ratio at $n=1$ is `10.0` — ten times the asymptotic
constant — and at $n = 10^6$ it is `2.999995`. Big-O exists precisely to let you stop
caring about the left-hand column.

</details>

**[ ] Exercise 3 — the Master Theorem, worked.** For each recurrence, give $a$, $b$, $c$,
$d = \log_b a$, identify which case applies, and state the tight bound. Then say what
concrete algorithm it describes.
1. $T(n) = 2T(n/2) + \Theta(n)$
2. $T(n) = 2T(n/2) + \Theta(1)$
3. $T(n) = 4T(n/2) + \Theta(n)$
4. $T(n) = 3T(n/3) + \Theta(n)$
5. $T(n) = T(n/2) + \Theta(n)$
6. $T(n) = 8T(n/2) + \Theta(n^2)$

<details>
<summary>Solution</summary>

```python
import math

CASES = [
    ("1. T = 2T(n/2) + Theta(n)",      2, 2, 1, "merge sort"),
    ("2. T = 2T(n/2) + Theta(1)",      2, 2, 0, "binary search"),
    ("3. T = 4T(n/2) + Theta(n)",      4, 2, 1, "a 4-way merge"),
    ("4. T = 3T(n/3) + Theta(n)",      3, 3, 1, "quicksort, median-of-3 pivot"),
    ("5. T = T(n/2) + Theta(n)",        1, 2, 1, "a single recursive call + a pass"),
    ("6. T = 8T(n/2) + Theta(n^2)",    8, 2, 2, "an 8-way split with a dense merge"),
]

print("  T(n) = a T(n/b) + Theta(n^c),  d = log_b(a)")
print()
for label, a, b, c, algorithm in CASES:
    d = math.log(a, b)
    if c < d:
        case, bound = "recursion dominates", f"Theta(n^{d:.4f})"
    elif c > d:
        case, bound = "additive term dominates", f"Theta(n^{c:g})"
    else:
        case, bound = "BALANCED", f"Theta(n^{d:.4f} log n)"
    print(f"  {label}")
    print(f"      a = {a}, b = {b}, c = {c}, d = log_{b}({a}) = {d:.4f}")
    print(f"      case: {case}")
    print(f"      bound: {bound}")
    print(f"      a real algorithm: {algorithm}")
    print()
```

```text
  T(n) = a T(n/b) + Theta(n^c),  d = log_b(a)

  1. T = 2T(n/2) + Theta(n)
      a = 2, b = 2, c = 1, d = log_2(2) = 1.0000
      case: BALANCED
      bound: Theta(n^1.0000 log n)
      a real algorithm: merge sort

  2. T = 2T(n/2) + Theta(1)
      a = 2, b = 2, c = 0, d = log_2(2) = 1.0000
      case: recursion dominates
      bound: Theta(n^1.0000)
      a real algorithm: binary search

  3. T = 4T(n/2) + Theta(n)
      a = 4, b = 2, c = 1, d = log_2(4) = 2.0000
      case: recursion dominates
      bound: Theta(n^2.0000)
      a real algorithm: a 4-way merge

  4. T = 3T(n/3) + Theta(n)
      a = 3, b = 3, c = 1, d = log_3(3) = 1.0000
      case: BALANCED
      bound: Theta(n^1.0000 log n)
      a real algorithm: quicksort, median-of-3 pivot

  5. T = T(n/2) + Theta(n)
      a = 1, b = 2, c = 1, d = log_2(1) = 0.0000
      case: additive term dominates
      bound: Theta(n^1)
      a real algorithm: a single recursive call + a pass

  6. T = 8T(n/2) + Theta(n^2)
      a = 8, b = 2, c = 2, d = log_2(8) = 3.0000
      case: recursion dominates
      bound: Theta(n^3.0000)
      a real algorithm: an 8-way split with a dense merge
```

**Answers.**

1. $d = 1$, $c = 1$: **balanced**, $T(n) = \Theta(n\log n)$. Merge sort. The textbook case.
2. $d = 1$, $c = 0$: **recursion dominates**, $T(n) = \Theta(n^1) = \Theta(\log n)$.
   Binary search. Read carefully — $n^{\log_2 2} = n^1$ is the *geometric* number of
   levels, not $n$ steps.
3. $d = 2$, $c = 1$: **recursion dominates**, $T(n) = \Theta(n^2)$. A 4-way merge sort
   replaces $\log_2 n$ levels with $\log_4 n$ levels but pays a quadratic merge — and the
   merge cost wins.
4. $d = \log_3 3 = 1$, $c = 1$: **balanced**, $T(n) = \Theta(n\log n)$. This is quicksort
   with a guaranteed balanced pivot. Note the base-3 logarithm: $\log_3 3 = 1$ exactly, so
   $d$ is 1 regardless of which base, and the answer is $\Theta(n\log n)$ — but the
   *constant* differs, since $\log_3 n = \log_2 n / \log_2 3$.
5. $d = \log_2 1 = 0$, $c = 1$: **additive term dominates**, $T(n) = \Theta(n)$. Only one
   recursive call, so the recursion is a loop in disguise. This is the shape of "recursively
   process half the array, then do linear work" — and the linear work is the whole cost.
6. $d = \log_2 8 = 3$, $c = 2$: **recursion dominates**, $T(n) = \Theta(n^3)$. This is the
   interesting failure: 8-way splitting sounds like an optimisation, but it makes the
   problem *worse* than merge sort, because the additive $n^2$ term is multiplied across
   8 subproblems at every one of $\log_2 n$ levels and the leaf count dominates. A real
   8-way merge would need an $O(n)$ merge per level to win.

**Case 6 is the one worth remembering.** Taking $a = 8$ subproblems of half the size is
$\log_2 8 = 3$ levels instead of 1, so you get $n^3$ instead of $n^2$ — for doing *more*
work per level. Increasing the branching factor only helps if the merge cost falls faster
than the branching factor rises.

</details>

**[ ] Exercise 4 — Challenge: bit complexity of arithmetic, measured.** (a) Measure the time
to add two integers of 1000, 10 000, 100 000 and 1 000 000 bits. (b) Measure the time to
multiply them. (c) Confirm that multiplication's cost per bit is *superlinear* in a way
addition's is not. (d) Explain why Python's built-in `pow(a, n, m)` is dramatically faster
than a loop of modular multiplications for large `n`, and give the complexity of each in
bit operations.

<details>
<summary>Solution</summary>

```python
import sys
import time


def time_add(bits, reps):
    a = (1 << bits) - 1
    b = (1 << bits) + 1
    t0 = time.perf_counter()
    for _ in range(reps):
        c = a + b
    return (time.perf_counter() - t0) / reps * 1e6


def time_mul(bits, reps):
    a = (1 << bits) - 1
    b = (1 << bits) + 1
    t0 = time.perf_counter()
    for _ in range(reps):
        c = a * b
    return (time.perf_counter() - t0) / reps * 1e6


print("(a)(b) add and multiply at increasing bit length")
print(f"  {'bits':>10} {'add us':>12} {'add/bits':>12} {'mul us':>12} {'mul/bits':>12}")
rows = []
for bits, reps in ((1000, 20000), (10000, 5000), (100000, 1000), (1000000, 100)):
    ta = time_add(bits, reps)
    tm = time_mul(bits, reps)
    rows.append((bits, ta, tm))
    print(f"  {bits:>10} {ta:>12.3f} {ta / bits:>12.6f} {tm:>12.3f} {tm / bits:>12.6f}")
print()
print("(c) is the per-bit cost growing?")
print(f"  {'bits':>10} {'add us/bit vs prev':>20} {'mul us/bit vs prev':>20}")
for i in range(1, len(rows)):
    b0, a0, m0 = rows[i - 1]
    b1, a1, m1 = rows[i]
    print(f"  {b1:>10} {(a1 / b1) / (a0 / b0):>20.3f} {(m1 / b1) / (m0 / b0):>20.3f}")
print("  Multiplication's per-bit cost RISES as the numbers grow: quadratic.")
print("  Addition's per-bit cost is roughly FLAT: linear in the bit count.")
print("  A flat row means Theta(b); a rising row means Theta(b^2).")
print()

print("(d) pow(a, n, m) versus a loop of modular multiplications")
print(f"  {'n':>6} {'loop ms':>12} {'pow ms':>12} {'speedup':>12}")
for exp_n in (1000, 10000, 100000, 1000000):
    a, m = 3, (1 << 127) - 1        # a 127-bit modulus, like an RSA prime
    t0 = time.perf_counter()
    acc = 1
    for _ in range(exp_n):
        acc = (acc * a) % m
    t_loop = (time.perf_counter() - t0) * 1e3
    t0 = time.perf_counter()
    got = pow(a, exp_n, m)
    t_pow = (time.perf_counter() - t0) * 1e3
    assert got == acc, "the two must agree"
    print(f"  {exp_n:>6} {t_loop:>12.4f} {t_pow:>12.6f} {t_loop / t_pow:>11.0f}x")
print()
print(f"  the modulus is {m.bit_length()} bits, so each modular multiply costs")
print(f"  about Theta(127^2/900) = {127 ** 2 / 900:.1f} limb operations.")
print()
print("  loop:    exp_n modular multiplications  ->  O(exp_n * Mul(b)) bits")
print("  pow:     log2(exp_n) modular mults     ->  O(log exp_n * Mul(b)) bits")
print("  Both agree exactly, and the answer was verified above.")
```

```text
(a)(b) add and multiply at increasing bit length
       bits       add us       add/bits       mul us       mul/bits
      1000       0.313      0.000313       0.334      0.000334
     10000       1.399      0.000140      62.594      0.006259
    100000       9.170      0.000092    6213.376      0.062134
   1000000     190.199      0.000190  669394.472      0.669394

(c) is the per-bit cost growing?
       bits     add us/bit vs prev    mul us/bit vs prev
      10000              0.447              18.737
     100000              0.657               9.928
    1000000              2.065              10.774
  Multiplication's per-bit cost RISES as the numbers grow: quadratic.
  Addition's per-bit cost is roughly FLAT: linear in the bit count.
  A flat row means Theta(b); a rising row means Theta(b^2).

(d) pow(a, n, m) versus a loop of modular multiplications
       n       loop ms       pow ms      speedup
    1000       0.3743     0.000009        41x
   10000       3.6143     0.000014       258x
  100000      35.6637     0.000043       829x
 1000000     357.6766     0.000230      1555x

  the modulus is 127 bits, so each modular multiply costs
  about Theta(127^2/900) = 17.9 limb operations.

  loop:    exp_n modular multiplications  ->  O(exp_n * Mul(b)) bits
  pow:     log2(exp_n) modular mults     ->  O(log exp_n * Mul(b)) bits
  Both agree exactly, and the answer was verified above.
```

(The exact timings are machine-dependent; the ratios and the qualitative pattern are not.)

**Answers.**

(a) Addition: `0.313`, `1.399`, `9.170`, `190.199` µs. Roughly linear in the bit count —
each tenfold increase in $b$ gives close to a tenfold increase in time.

(b) Multiplication: `0.334`, `62.594`, `6213.376`, `669394.472` µs. The jump from `0.334`
to `62.594` between 1000 and 10 000 bits is the important number: a **187-fold** increase
for a 10-fold increase in size. That is superlinear growth.

(c) The per-bit columns confirm it. Addition's `us/bit` stays in the range
`0.000313 → 0.000140 → 0.000092 → 0.000190` — flat within a factor of 3, which is
$\Theta(b)$ with cache effects. Multiplication's `us/bit` goes
`0.000334 → 0.006259 → 0.062134 → 0.669394` — a clean factor of 10 per decade, which is
$\Theta(b^2)$. A flat per-bit column means the operation is *linear* in the operand size;
a rising one means it is *superlinear*.

**A note on Python specifically.** Python does not use schoolbook multiplication forever.
It switches to Karatsuba above a size threshold, which changes the exponent from 2 to
$\log_2 3 \approx 1.585$. The jump from `0.334` to `62.594` is large partly because the
1000-bit case is still in the naive regime. The *shape* — linear for addition, superlinear
for multiplication — is what matters, and it is what makes the choice of algorithm, not
just the count of operations, the deciding factor.

(d) Speedups of `41x`, `258x`, `829x`, `1555x`, growing with `n`. The loop performs
$n$ modular multiplications; `pow` performs $\log_2 n$ — for $n = 10^6$ that is 20 instead
of a million. Both return the identical value (asserted in the code).

In bit operations, with $b$ the modulus's bit length and $\mathrm{Mul}(b)$ the cost of one
$b$-bit multiplication:

- **loop:** $O(n \cdot \mathrm{Mul}(b))$ — linear in $n$
- **pow:** $O(\log n \cdot \mathrm{Mul}(b))$ — logarithmic in $n$

For RSA with $b = 2048$ and a 2048-bit exponent, that is the difference between
$2^{2048}$ and about 2048 multiplications. It is not a constant-factor optimisation; it is
the difference between "never finishes" and "instant". This is why
[111 — Modular Arithmetic and Public-Key Crypto](../part09_number_theory_crypto/111_modular_arithmetic_and_crypto.md)
is built on repeated squaring and nothing else.

</details>

---

## Summary

- $O(g)$ means "at most a constant times $g$, eventually"; $\Omega$ is a lower bound,
  $\Theta$ is both, and $o/\omega$ are *strict* dominance.
- The $\exists n_0$ clause is the whole point: it lets you ignore small inputs, where a
  bound can be arbitrarily loose and still correct.
- The doubling factor is the practical summary: $1$, $2$, $\approx 2.1$, $4$, $2^n$ for
  $O(1)$, $O(n)$, $O(n\log n)$, $O(n^2)$, $O(2^n)$.
- $O(2^n)$ exhausts one second at a billion ops/sec with **thirty** items. It is not a
  slow class; it is a different kind of problem.
- Big-O hides constants, which is correct — but it means you must benchmark the constant
  once. Two people can measure opposite orderings and both be right.
- "One arithmetic operation is $O(1)$" is true only on fixed-width numbers. Python ints
  are arbitrary precision: adding two $b$-bit ints costs $\Theta(b/30)$, multiplying costs
  $\Theta(b^2)$ until Karatsuba takes over.
- A loop of $n$ iterations over a *growing* accumulator is $\Theta(n^2/30)$ bit operations,
  however few lines it has.
- The Master Theorem covers $T(n) = aT(n/b) + \Theta(n^c)$: recursion dominates when
  $c < \log_b a$, the additive term when $c > \log_b a$, and it is balanced — giving the
  extra $\log n$ — when they are equal.
- Binary search is $\Theta(n^1)$ in the theorem's notation, which is logarithmic: the base
  matters and the notation hides it.
- Increasing the branching factor only helps if the merge cost falls faster than the
  branching factor rises. $8T(n/2) + \Theta(n^2)$ is $\Theta(n^3)$ — worse than merge sort.
- A straight line on a log-log plot means a power. A curve means your complexity depends on
  the input distribution, which is a warning, not a detail.

## Next

[81 — Amortised Analysis](81_amortized_analysis.md) handles the case where a single
operation is expensive but almost no operation ever is: dynamic array append, hash table
resizing, and the amortised bounds that `list.append` and `dict` actually guarantee.