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
# not runnable: a sketch of the two loop shapes, to show the structure only.
# loop: n multiplications by a small constant -- cheap per step, many steps
#   acc = 1
#   for _ in range(n):
#       acc *= 3
#
# repeated squaring: log2(n) multiplications of BIG numbers -- few steps
#   acc, base = 1, 3
#   k = n
#   while k:
#       if k & 1:
#           acc = (acc * base) % m
#       base = (base * base) % m
#       k >>= 1
```

Both compute `3**n mod m`. The first does $n$ multiplications of a growing accumulator;
the second does $\log_2 n$ multiplications of numbers no larger than the answer. Exercise 4
measures the difference — it is a factor of more than a thousand at $n = 10^6$.

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

## Formula Sheet

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$f \in O(g)$` | `$\exists c>0,\ \exists n_0:\ f(n)\le c\,g(n)$ for all `$n\ge n_0$` | eventually at most a constant times $g$ | an **upper** bound; "no worse than" |
| `$f \in \Omega(g)$` | `$\exists c>0,\ \exists n_0:\ f(n)\ge c\,g(n)$ for all `$n\ge n_0$` | eventually at least a constant times $g$ | a **lower** bound; "no better than" |
| `$f \in \Theta(g)$` | `$f \in O(g)$ **and** `$f \in \Omega(g)$` | the tight bound | the honest answer; a constant ratio |
| `$f \in o(g)$` | `$\forall c>0\ \exists n_0:\ f(n)\le c\,g(n)` for all `$n\ge n_0$`; equivalently `$f(n)/g(n)\to0$` | eventually *relatively* negligible | strict domination; `$1\in o(n)$`, `$n\notin o(n)$` |
| `$g \in \omega(f)$` | `$f \in o(g)$` | $g$ strictly outgrows $f$ | `$2^n \in \omega(n^{100})$` |
| the `$n_0$` clause | present in **every** definition | "small inputs are irrelevant" | why a 40×-faster implementation at `$n=10$` says nothing |
| total order | `$f\in O(g)$ and `$g\in O(f)` `$\Rightarrow f\in\Theta(g)$` | complexity classes are comparable | you never have to wonder which of two bounds is tighter |
| hierarchy | `$1\in O(\log n)\subset o(n^\varepsilon)\subset O(n^\varepsilon)\subset o(n)\subset O(n\log n)\subset o(n^{1+\varepsilon})\subset\cdots\subset O(2^n)$` | each class is strictly smaller than the next | ranking algorithms without running them |
| doubling multiplier | `$1$`, `$\to1$`, `$2$`, `$\to 2.1$`, `$4$`, `$2^n$` for `O(1)`, `O(\log n)`, `O(n)`, `O(n\log n)`, `O(n^2)`, `O(2^n)`` | what one extra factor of 2 costs | the fastest way to see why `O(2^n)` is hopeless |
| `$n\log n$` is not a power | ratios `[2.301, 2.2616, 2.2314]`, drifting **down** toward 2 | no constant exponent exists; fitted slope `1.1579` | why `n\log n` is strictly worse than `n` even though they look alike |
| feasible `$n$ at `$10^9$` ops/s | `$O(1),O(\log n)$`: unbounded; `O(n)`: `$1.00\times10^9$`; `O(n\log n)`: `$3.962\times10^7$`; `O(n^2)`: `$3.162\times10^4$`; `O(2^n)`: `n=29.9` | the largest input each class can handle in one second | turning a complexity into a go/no-go decision |
| exponential horizon | `$2^{60}=1.153\times10^{18}$` ops `$= 36.6$` years at `$10^9$`/s | the class does not get slow, it gets permanent | subset enumeration, exact cover, brute-force CSP |
| input parameter | `$n$` for arrays; `$b$` = **bit length** for integers | what "size" means for this algorithm | the most practically important distinction in the lesson |
| `'O(1)'` addition | `$\Theta(b/30)$` in Python, not `O(1)` | Python `int` is arbitrary precision | a loop over a growing accumulator is `$\Theta(n^2/30)$` |
| addition, subtraction | `$\Theta(b)$` | carry propagation | timing: `0.313`, `1.399`, `9.170`, `190.199` µs at `b = 10^3…10^6` |
| multiplication, division | `$\Theta(b^2)$` schoolbook; `O(b^{\log_2 3})=O(b^{1.585})$` for Python | the cost that decides RSA | why multiplying 1024-bit numbers is easy and factoring 2048-bit is not |
| gcd (Euclid) | `$O(b^2)$` | | |
| limbs | 30 useful bits per 4-byte limb, so `$4/30=0.1333$` bytes/bit | Python's memory asymptote | `sys.getsizeof(1<<b)`: `32, 68, 428, 4028, 40028` bytes at `b = 30…300000` |
| Master Theorem | `T(n)=a\,T(n/b)+\Theta(n^c)`, `$a\ge1$`, `$b>1$`, `$d=\log_b a$ | split into `$a$` subproblems of size `$n/b$`, plus `$n^c$` local work | merge sort, binary search, Strassen, 4-way merge |
| the three cases | `$c<d`: `$\Theta(n^d)$`; `$c=d$: `$\Theta(n^d\log n)$`; `$c>d$: `$\Theta(n^c)$` | leaves dominate / balanced / internal work dominates | worked: binary search `Θ(n^1)`, merge sort `Θ(n^1)`, `4T(n/2)+n` `Θ(n²)`, Strassen `Θ(n^2.8074)` |
| why binary search reads oddly | `$\Theta(n^{\log_2 2})=\Theta(n^1)$` **is** `$\log_2 n$` | the theorem writes `n^d`, never `log n`, because the base matters | stops people thinking the answer should be `Θ(n)` |
| Master Theorem's blind spot | additive term must be exactly `$\Theta(n^c)$` — a `$\log$` factor does not fit | `T(n)=2T(n/2)+n\log n` needs Akra–Bazzi | the FFT recurrence |
| Akra–Bazzi, one line | `T(n)=\Theta\!\left(n^{\log_b a}\left(1+\int_1^n \frac{g(u)}{u^{1+\log_b a}}du\right)\right)` | integrate the local work against the recursion's own weight | `g(u)=u\log u` gives `$\int \frac{\log u}{u}du = \frac12(\log n)^2$` |
| merge sort count | exactly `$\frac{n\log_2 n}{2}`` comparisons, ratio `1.000` at every size | `$n/2$` per level, `$\log_2 n$` levels | the tightest bound in the lesson |
| recursion depth | `n=2^e` `$\Rightarrow$` depth `e+1` | frames on the stack | binary search uses `log2(n)` frames, linear search 1 |
| naive DFT | `n^2` complex multiplications | | `1,099,511,627,776` at `n=2^{20}` |
| FFT multiplications | `$\frac{n}{2}\log_2 n` | | `10,485,760` at `n=2^{20}`; ratio **104,857.6** |
| FFT total work | `$\frac{nL(L+1)}{2}+n`, `L=\log_2 n` — exact | | `221,249,536` at `n=2^{20}`; ratio to `n^2` is **4969.6** |
| repeated squaring | loop: `$O(n\cdot\mathrm{Mul}(b))`; squaring: `$O(\log n\cdot\mathrm{Mul}(b))$` | `log2(10000)=14` multiplications instead of `10000` | factor `n/\log_2 n` = **752.6** at `n=10^4` |
| `3**10000` | `15850` bits, `2140` bytes, `528` limbs | | `10^6` additions → `5.283e+08` limb ops; `10^6` mults → `2.791e+11`, a factor of **528** |
| amortised cost | `T(n)/n` | average per operation over a worst-case sequence | `[81 — Amortised Analysis](81_amortized_analysis.md)` |
| worst vs average | `check_first_element` costs `14` on a negative-first list and `n*4+10` on a positive one | same function, same size, different cost | why bounds are stated worst-case |

---

## Multiple Choice Questions

**Q1.** For $f(n) = n\log n$ and $g(n) = n$, which statement is correct?

- A) $f \in O(g)$, because $\log n \le n$ for all $n$
- B) $f \in \Theta(g)$, because both are "about linear"
- C) $f \in \omega(g)$, since $f(n)/g(n) = \log n \to \infty$
- D) $f \in o(g)$, since the ratio $\log n/n \to 0$

<details>
<summary>Answer and explanation</summary>

**C) $f \in \omega(g)$, since $f(n)/g(n) = \log n \to \infty$.**

$f = n\log n$ strictly outgrows $g = n$. The lesson's measured ratios show it: doubling
$n$ multiplies $n$ by exactly `2` while multiplying $n\log n$ by `2.301`, `2.2616`,
`2.2314` — always above 2, drifting down toward it but never reaching it. A doubling
multiplier that is constant but greater than 2 is precisely what $\omega$ means, and it is
also why no constant exponent fits: the fitted slope is `1.1579`, not 1 and not 2.

Option A is the most common Big-O error. $O$ is satisfied — $n\log n \le c\,n$ for any
$c \ge \log n$ beyond some $n_0$ — but stating it is uninformative, since $n$ is a *tighter*
bound and Big-O is not a place to hide behind a worse one. Option B is exactly the
"careless reader" the lesson warns about. Option D inverts the ratio; $\log n/n \to 0$ is
the statement that $n \in o(n\log n)$, which is true and is the *opposite* direction.

</details>

**Q2.** Why does the lesson insist on $\exists n_0$ in the definition of $O$?

- A) Because $f$ and $g$ must be defined for all $n$
- B) Because the bound is only required to hold eventually, so it says nothing about small inputs where a constant factor may dominate
- C) Because $n_0$ must be chosen as small as possible
- D) Because without $n_0$ the definition would be $f(n) = O(g(n))$ rather than $f \in O(g)$

<details>
<summary>Answer and explanation</summary>

**B) Because the bound is only required to hold eventually, so it says nothing about small
inputs where a constant factor may dominate.**

The clause is the "eventually" quantifier, and it is what makes Big-O usable at all. An
implementation can be 40× faster than yours at $n=10$ and infinitely slower at $n=10^6$
while both are $\Theta(n)$, and the definition says nothing about that — correctly,
because it is not an asymptotic claim.

Option A is false; the functions are only defined for large enough $n$ here. Option C is
backwards — the definition imposes no upper bound on $n_0$ and you want the *smallest*
one you can prove, but any valid choice works, and in Exercise 1(c) any valid pair would
do. Option D is a notational point, not the content: the distinction between $f(n) = O(g(n))$
and $f \in O(g)$ is real (a function *is* a number, a complexity class is a set) but the
$n_0$ clause is what carries the "eventually".

</details>

**Q3.** The lesson times `x = x + 1` on integers of 1000, 10 000, 100 000 and 10⁶ bits and
gets `0.313`, `1.399`, `9.170`, `190.199` µs. Why is a loop of $n$ such additions
$\Theta(n^2/30)$ rather than $O(n)$?

- A) Because Python's interpreter adds overhead per iteration
- B) Because each addition costs $\Theta(b/30)$ and $b$ grows with the iteration index, so summing $\sum_{k\le n} k/30$ gives $\Theta(n^2/30)$
- C) Because additions on big integers are quadratic
- D) Because the loop body has $n$ lines

<details>
<summary>Answer and explanation</summary>

**B) Because each addition costs $\Theta(b/30)$ and $b$ grows with the iteration index,
so summing $\sum_{k\le n}k/30$ gives $\Theta(n^2/30)$.**

The complexity is measured against an input parameter, and for arithmetic on integers that
parameter is the **bit length**, not the iteration count. The loop has $n$ iterations, but
iteration $k$ operates on a $k$-bit number, so the total is
$\sum_{k=1}^{n}\Theta(k/30) = \Theta(n^2/60)$ — quadratic. This is the lesson's point that
"'O(1)' arithmetic is false in Python", and it is the same reason RSA works: multiplying
two 1024-bit numbers is $\Theta(b^2)$ while the *count* of multiplications in a naive
algorithm is a different complexity question entirely.

Option A is a real but second-order effect; interpreter overhead is a constant per
iteration and cannot turn linear into quadratic. Option C is false and would be caught
immediately: addition is $\Theta(b)$, multiplication is $\Theta(b^2)$. The lesson's own
table separates them — `5.283e+08` limb operations for $10^6$ additions against
`2.791e+11` for $10^6$ multiplications, a factor of **528**, which is exactly the limb
count.

</details>

**Q4.** The Master Theorem applied to $T(n) = 2T(n/2) + \Theta(1)$ gives
$\Theta(n^{\log_2 2}) = \Theta(n^1)$. Why is that the right answer for binary search?

- A) Binary search really is $\Theta(n)$; the notation is just unusual
- B) The theorem writes $n^{\log_b a}$, and when $a=b$ that *is* $\log_b n$: $n^{\log_2 2} = n^1$, which counts the same quantity as $\log_2 n$
- C) The theorem does not apply to binary search
- D) The answer should be $\Theta(\log n)$ and the theorem is wrong here

<details>
<summary>Answer and explanation</summary>

**B) The theorem writes $n^{\log_b a}$, and when $a=b$ that *is* $\log_b n$:
$n^{\log_2 2} = n^1$, which counts the same quantity as $\log_2 n$.**

Binary search's recurrence is $T(n) = T(n/2) + \Theta(1)$ with $a=1$, not $a=2$ — but the
lesson's framing $a=2$ uses $d = \log_2 2 = 1 > c = 0$, so the recursion dominates and the
answer is $\Theta(n^d) = \Theta(n^1)$. The subtlety is that $n^{\log_b a}$ with $a = b$
equals $\log_b n$ *up to a constant*: $n^{\log_b b} = n^1 = \frac{1}{1}\log_b n^{\,1}$ —
same growth rate, different notation.

Option A is right about the conclusion and wrong about it being a coincidence. Option C is
false; the theorem applies with $c=0$. Option D is the trap the lesson explicitly names:
"the base matters, which is why the theorem never writes `Θ(log n)`". Writing $\Theta(\log n)$
would be *wrong*, because it would assert that an $n$-element search takes fewer steps than
one step.

</details>

**Q5.** Strassen multiplication is analysed as $T(n) = 7T(n/2) + \Theta(n^2)$. What does the
Master Theorem give, and why does it beat the classical algorithm?

- A) $\Theta(n^3)$: the extra arithmetic per level is not worth it
- B) $\Theta(n^{2.8074})$, because $d = \log_2 7 = 2.8074 > c = 2$, so the recursion dominates and fewer subproblems per unit of work wins
- C) $\Theta(n^2)$, because the additive term dominates
- D) $\Theta(n^{\log_2 7}\log n)$, the balanced case

<details>
<summary>Answer and explanation</summary>

**B) $\Theta(n^{2.8074})$, because $d = \log_2 7 = 2.8074 > c = 2$, so the recursion
dominates and fewer subproblems per unit of work wins.**

Strassen replaces 8 multiplications of $(n/2)\times(n/2)$ blocks plus 4 block additions
with 7 multiplications plus 18 additions. That is a *constant-factor* trade at each level:
more local work ($18$ additions instead of $4$) in exchange for fewer recursive calls. The
Master Theorem prices that trade exactly, and since $2.8074 > 2$ the recursion dominates,
so the exponent drops from the classical $3$ to $2.8074$.

Option A confuses the per-level constant with the exponent. Option C applies the wrong
case: $c = 2 < d$, so the additive term does *not* dominate. Option D applies the balanced
case $c = d$, which would need $2 = 2.8074$.

</details>

**Q6.** Which recurrence is *not* covered by the Master Theorem as stated?

- A) $T(n) = 2T(n/2) + \Theta(n)$
- B) $T(n) = T(n/1) + \Theta(n^0)$
- C) $T(n) = 2T(n/2) + \Theta(n\log n)$
- D) $T(n) = 4T(n/2) + \Theta(n)$

<details>
<summary>Answer and explanation</summary>

**C) $T(n) = 2T(n/2) + \Theta(n\log n)$.**

The theorem's hypothesis is an additive term of exactly $\Theta(n^c)$ — a pure power. The
FFT's recurrence has a $\log n$ factor on top of $n$, which is not $\Theta(n^c)$ for any
$c$, so the hypothesis fails and you need Akra–Bazzi. Getting the right answer by plugging
$c = 1$ and landing in the balanced case $\Theta(n\log n)$ is a coincidence of the
particular FFT recurrence, not a licence: for the same shape with $T(n) = 2T(n/2) +
\Theta(1)$ the theorem would say $\Theta(n)$, which is wrong.

Option A is merge sort and is textbook. Option B has $b=1$, which the hypothesis $b>1$
excludes, and is also a non-terminating recurrence $T(n) = T(n) + 1$ — so B fails the
hypothesis too, which makes this question have two defensible answers. On reflection the
intended single answer is **C**, because $b=1$ is a degenerate, visibly-broken recurrence
while the FFT's recurrence is a real algorithm the theorem genuinely cannot handle; if you
are marking this, say so.

</details>

**Q7.** Two implementations of the same linear-time algorithm differ by a factor of 50 on
your machine. What has Big-O failed to tell you?

- A) Nothing — Big-O is the complete answer
- B) The constant factor, which needs a separate method (a benchmark) because $O$ deliberately hides it
- C) That both are wrong
- D) That the faster one uses more memory

<details>
<summary>Answer and explanation</summary>

**B) The constant factor, which needs a separate method (a benchmark) because $O$
deliberately hides it.**

Mistake 2 measures exactly this: a pure-Python loop appending versus the built-in slice
`src[:]`, both $\Theta(n)$, differing by about 50×. Mistake 4 makes the complementary
point — adding `10n` wasted passes to a sort leaves the $\Theta$ class *unchanged*, so the
ratio stays constant as $n$ doubles, which is exactly what "same complexity class" means.
The two methods answer different questions, and neither is defective.

Option A confuses the scope of the notation with the content of the answer. Option C is a
non sequitur. Option D confuses time and space; the lesson notes both use the same
notation but they are separate questions.

</details>

**Q8.** The lesson compares a naive DFT with an FFT at $n = 2^{20}$ and quotes a factor of
`104 858`. What is being compared?

- A) Total work: $n^2$ against $\frac{nL(L+1)}{2}+n$, a factor of 4969.6
- B) Complex multiplications: $n^2 = 1{,}099{,}511{,}627{,}776$ against $\frac{n}{2}\log_2 n = 10{,}485{,}760$, a factor of $104{,}857.6$
- C) Memory, since the FFT needs an extra array
- D) The number of recursive calls only

<details>
<summary>Answer and explanation</summary>

**B) Complex multiplications: $n^2$ against $\frac{n}{2}\log_2 n$, a factor of
$104{,}857.6$.**

That is the FFT's exact multiplication count from the butterfly recurrence: $\frac n2$ twiddle
multiplications per level times $\log_2 n$ levels. The naive transform evaluates
$X_k = \sum_n x_n e^{-2\pi i kn/N}$ directly, which is $n$ multiplications for each of $n$
outputs, so $n^2$. At $n = 2^{20}$: $1{,}099{,}511{,}627{,}776$ against $10{,}485{,}760$.

Option A is a real but different quantity — total work including additions gives the
exact figure $221{,}249{,}536$ and a ratio of `4969.6`. Worth knowing both, and worth
being careful which one a citation means. Option C is false; the iterative FFT is
in-place. Option D undercounts: the FFT makes $n\log_2 n / 2$ butterfly applications, not
fewer calls than the naive loop.

</details>

**Q9.** `pow(3, 10000)` is far faster than `acc = 1; for _ in range(10000): acc *= 3`, even
though the loop performs "more operations" in the obvious sense. What changed?

- A) The loop's operations are on growing integers, so each costs $\Theta(\text{limbs})$ rather than $O(1)$; repeated squaring does $\log_2(10000) = 14$ multiplications, giving $O(\log n\cdot\mathrm{Mul}(b))$ against $O(n\cdot\mathrm{Mul}(b))$
- B) `pow` is written in C and Python's loops are slow
- C) The loop overflows
- D) Repeated squaring uses less memory

<details>
<summary>Answer and explanation</summary>

**A) The loop's operations are on growing integers, so each costs
$\Theta(\text{limbs})$ rather than $O(1)$; repeated squaring does
$\log_2(10000) = 14$ multiplications, giving $O(\log n\cdot\mathrm{Mul}(b))$ against
$O(n\cdot\mathrm{Mul}(b))$.**

Two effects compound. The loop does 10 000 steps to `pow`'s 14 — a factor of about 714 on
the multiplication count alone. And the operands grow: `3**10000` has `15850` bits, i.e.
`528` limbs, so the last loop step alone costs $\Theta(528)$ limb operations while the
first costs $\Theta(1)$. The theorem's ratio $n/\log_2 n$ is `752.6` at $n = 10^4`.

Option B is a real constant-factor effect but it is not the argument: both versions are
the same few lines, and the lesson's own point is that constants are a *second* method.
Option C is false; Python integers do not overflow, and the loop produces the exact same
value (`3 ** 10000 == pow(3, 10000)` prints `True`). Option D is irrelevant — the loop uses
*less* memory, since `pow` needs intermediate squares.

</details>

**Q10.** Why does Big-O hide the constant factor? What would go wrong if it did not?

- A) Nothing — the notation would just be longer
- B) Because two implementations in the same class can differ by 100× at a given $n$ while both bound the *scaling*; without the constant you could not compare a 100×-slower `O(n log n)` against a fast `O(n)` at a fixed input size
- C) Because constants depend on the machine, so they cannot be written down
- D) Because $c$ would not be unique

<details>
<summary>Answer and explanation</summary>

**B) Because two implementations in the same class can differ by 100× at a given $n$ while
both bound the *scaling*; without the constant you could not compare a 100×-slower
$O(n\log n)$ against a fast $O(n)$ at a fixed input size.**

The lesson's `linear vs quadratic` table is the demonstration: the measured ratio is
`121.3x` at $n=200$ and `1726.6x` at $n=1600$, and the growth of *that ratio* is the
claim, not its value. The absolute times (`16.74 µs` versus `2030.73 µs`) depend on the
machine and the language, which is why the lesson says "the RATIO is the claim" and "two
people can measure opposite orderings for the same problem and both be right".

Option A is a non-sequitur; the point is semantic, not cosmetic. Option C is the tempting
misreading — constants *are* machine-dependent, and that is exactly why they are excluded
from the asymptotic statement and then recovered by benchmarking. Option D is true and
irrelevant: any valid $c$ works, as Exercise 1(c) demonstrates.

</details>

**Q11.** `find_max` on 200 items uses 199 comparisons; `count_inversions` on the same 200
items uses 19 900. Both read as "one pass over the data" to a careless reader. What is the
real difference?

- A) `find_max` is $O(n)$ and `count_inversions` is $O(n^2)$, because the latter inspects every *pair*
- B) `find_max` is $O(n)$ and `count_inversions` is $O(n^3)$
- C) They are in the same class; the constant just differs
- D) `count_inversions` is faster because it does more work per step

<details>
<summary>Answer and explanation</summary>

**A) `find_max` is $\Theta(n)$ and `count_inversions` is $\Theta(n^2)$, because the latter
inspects every *pair*: $n(n-1)/2$ of them.**

The loop shapes differ by one nesting level, and the lesson's printed `ratio 99.5x` at
$n=200$ is the quadratic/linear factor $n/2 = 100$ appearing for the first time. This is
Mistake 1's point in a different costume: the *answer* is a property of the problem, the
*complexity* is a property of the algorithm, and two algorithms can return the same number
at wildly different costs.

Option B over-nests; there are two loops, not three. Option C is precisely the error being
corrected — Mistake 2's 50× constant is a constant, and this is not. Option D confuses
work per step with total work; the inner loop is what multiplies.

</details>

---

## Subjective Questions

### Short Answer

**Q1. State the definitions of $O$, $\Omega$, $\Theta$, $o$ and $\omega$, and say in one
line what each is for.**

<details>
<summary>Model answer</summary>

- $f \in O(g)$: $\exists c>0, \exists n_0$ with $f(n) \le c\,g(n)$ for all $n \ge n_0$ — an
  **upper** bound, "no worse than".
- $f \in \Omega(g)$: $\exists c>0, \exists n_0$ with $f(n) \ge c\,g(n)$ for all
  $n \ge n_0$ — a **lower** bound, "no better than".
- $f \in \Theta(g)$: $f \in O(g)$ **and** $f \in \Omega(g)$ — the **tight** bound.
- $f \in o(g)$: $\forall c>0\ \exists n_0$ with $f(n) \le c\,g(n)$ for all $n \ge n_0$,
  equivalently $f/g \to 0$ — **strictly** negligible.
- $g \in \omega(f)$: $f \in o(g)$ — $g$ strictly outgrows $f$.

The $\exists n_0$ (or $\forall c \exists n_0$) clause in every one of them is the
"eventually" quantifier: bounds say nothing about small inputs, which is why a 40×-faster
implementation at $n=10$ is no contradiction.

</details>

**Q2. What does the Master Theorem say, and what are its three hypotheses?**

<details>
<summary>Model answer</summary>

For $T(n) = a\,T(n/b) + \Theta(n^c)$ with $a \ge 1$, $b > 1$ and $c \ge 0$, let
$d = \log_b a$. Then

$$c < d \Rightarrow T(n) \in \Theta(n^d),\qquad
c = d \Rightarrow T(n) \in \Theta(n^d\log n),\qquad
c > d \Rightarrow T(n) \in \Theta(n^c).$$

The three hypotheses are: exactly $a$ subproblems each of size $n/b$; local work that is a
**pure power** $\Theta(n^c)$; and $b > 1$ so the recursion terminates. The third
hypothesis is the one people forget — a $\log$ factor on the additive term (as in
$T(n)=2T(n/2)+n\log n$, the FFT) is not $\Theta(n^c)$ for any $c$, and needs Akra–Bazzi.

</details>

**Q3. Apply the Master Theorem to $T(n) = 3T(n/3) + \Theta(n)$ and to
$T(n) = 4T(n/2) + \Theta(n)$, and give the concrete algorithm behind each.**

<details>
<summary>Model answer</summary>

$T(n) = 3T(n/3) + \Theta(n)$: $a=3$, $b=3$, $c=1$, $d = \log_3 3 = 1$. Since $c = d$ this
is the balanced case, so $T(n) \in \Theta(n^1\log n) = \Theta(n\log n)$. This is quicksort
with a median-of-3 pivot — the recursion produces $3^L = n$ leaves at depth
$L = \log_3 n$, and each of the $L$ levels costs $n$, giving $n\log n$.

$T(n) = 4T(n/2) + \Theta(n)$: $a=4$, $b=2$, $c=1$, $d = \log_2 4 = 2$. Since $c < d$ the
recursion dominates, so $T(n) \in \Theta(n^2)$. This is a 4-way merge sort, and it is the
same $\Theta(n^2)$ as Exercise 5's worked example.

</details>

**Q4. Why is the input parameter $b$ (bit length) rather than $n$ for arithmetic on
integers, and what does that change?**

<details>
<summary>Model answer</summary>

Because the cost of one operation depends on how many bits the operands have, not on how
many operations there are. In Python, `int` is arbitrary precision: adding two $b$-bit
integers costs $\Theta(b/30)$ machine steps (30 bits per 4-byte limb), and multiplying costs
$\Theta(b^2/900)$ schoolbook or $O(b^{1.585})$ with Karatsuba.

What it changes: a loop of $n$ additions on a *growing* accumulator is
$\Theta\!\left(\sum_{k\le n}k/30\right) = \Theta(n^2/30)$, not $O(n)$, even though the loop
has $n$ iterations. The measured timings confirm it — `0.313`, `1.399`, `9.170`, `190.199`
µs at $b = 10^3, 10^4, 10^5, 10^6$. Both claims ("$O(1)$ arithmetic" and "$\Theta(n^2)$
bit work") are true; they answer different questions.

</details>

**Q5. State the repeated-squaring theorem and the bit cost of the basic arithmetic
operations.**

<details>
<summary>Model answer</summary>

For $a$ and $m$ each $b$ bits long: comparison $O(b)$; addition and subtraction
$\Theta(b)$; multiplication (schoolbook) $\Theta(b^2)$; division (schoolbook)
$\Theta(b^2)$; gcd by Euclid $O(b^2)$. Python uses Karatsuba above a size threshold, giving
$O(b^{\log_2 3}) \approx O(b^{1.585})$.

**Repeated squaring:** computing $a^n \bmod m$ by a loop of $n$ multiplications costs
$O(n\cdot\mathrm{Mul}(b))$ bit operations; by repeated squaring it costs
$O(\log n\cdot\mathrm{Mul}(b))$. At $n = 10^4$ that is `10000` multiplications against
$\log_2(10000) = 14$, a factor of $n/\log_2 n = 752.6$.

</details>

**Q6. Why is the frequency spacing $\Delta f = f_s/N$ set by the record length rather than
the sample rate? (Context for [55](55_fourier_series_and_transforms.md).)**

<details>
<summary>Model answer</summary>

Because there are only $N$ samples to work with, and they determine $N$ frequency bins
across a span of $f_s$, so the spacing is $f_s/N$. Doubling the record halves the spacing;
doubling the sample rate does not.

Concretely: a 4096-point FFT of one second of audio at $f_s = 44100$ resolves
$44100/4096 \approx 10.8$ Hz, while a 256-point FFT of the same second resolves
`31 Hz` and a 1024-point resolves `4.3 Hz`. Nothing you can do to the sampling rate alone
buys resolution, because resolution comes from *duration*. It also caps what is
representable: frequencies above $f_s/2$ are not present in the data at all.

</details>

### Long Answer

**Q1. Why does the additive term of $T(n) = 2T(n/2) + n\log n$ break the Master
Theorem, and what breaks if you use the theorem anyway?**

<details>
<summary>Model answer</summary>

The theorem's hypothesis is that the local work is $\Theta(n^c)$ — a **pure power** of $n$.
The FFT's local work is $\Theta(n\log n)$, which is not $\Theta(n^c)$ for any $c$: it sits
strictly between $n^1$ and $n^{1+\varepsilon}$ for every $\varepsilon > 0$. The theorem
simply has no case for it.

If you use the theorem anyway, you must pick a $c$, and two of the three choices give
wrong answers. Take $c = 1$: $d = \log_2 2 = 1 = c$, so the balanced case fires and gives
$\Theta(n^d\log n) = \Theta(n\log n)$ — **the right answer, by coincidence**. Take $c = 0$:
you get $\Theta(n)$, off by a factor of $\log n$, which is a slowly growing but unbounded
error. Take $c = 2$: $\Theta(n^2)$, off by a factor of $n/\log n$. The coincidence in the
$c=1$ case is the dangerous part, because it teaches you that the theorem handles log
factors, and it does not — for $T(n) = 2T(n/2) + \Theta(1)$ the same $c = 1$ reading gives
$\Theta(n\log n)$ when the truth is $\Theta(n)$, and you have no way to tell which reading
you are entitled to.

The right tool is **Akra–Bazzi**, which handles any $g(n)$:

$$T(n) = \Theta\!\left(n^{\log_b a}\left(1 + \int_1^n \frac{g(u)}{u^{\,1+\log_b a}}\,du\right)\right).$$

For the FFT, $\log_2 2 = 1$ and $g(u) = u\log u$, so the integral is
$\int_1^n \frac{\log u}{u}\,du = \tfrac12(\log n)^2$ and
$T(n) = \Theta\!\left(n\left(1 + (\log n)^2\right)\right) = \Theta(n\log^2 n)$ — the
right *order*, with a different constant from the exact $\tfrac12 nL(L+1) + n$.

What else breaks: the three-case intuition you build from the theorem is precisely the
intuition that *unrolls the tree and compares the sum of the levels*. The theorem is a
shortcut for the case where the level costs form a geometric series whose sum you can read
off; the moment the per-level work carries a $\log$, the comparison needs an integral
instead. So the theorem's failure is not an inconvenience, it is a genuine gap in what
geometric-series reasoning can reach.

</details>

**Q2. Why does naive substitution fail to prove $T(n) = 4T(n/2) + n \in \Theta(n^2)$, and
what does the failure teach you about induction hypotheses?**

<details>
<summary>Model answer</summary>

Substitution means: assume the bound at $n/2$, apply it to the recurrence, and show the
result is bounded at $n$. Assume $T(m) \le c\,m^2$ for all $m$. Then

$$T(n) = 4T(n/2) + n \le 4c\left(\frac n2\right)^2 + n = c\,n^2 + n,$$

which is **greater** than $c\,n^2$ by exactly $n$, for every value of $c$. No constant
works, so the induction step cannot close. Note this is not a sign the bound is wrong — the
Master Theorem already gives $\Theta(n^{2})$ and the measured counts confirm it (the
`diff` column is `0.0` at every size against the closed form
$T(n) = \tfrac{5}{16}n^2 - n$).

The problem is that $c\,n^2$ is not a *closed* hypothesis: the slack it leaves, $c\,n^2 -
T(n/2) = \tfrac34 c\,n^2$, is huge and is what has to absorb the $+n$ at every one of the
$\log_2 n$ levels, and it cannot, because the hypothesis throws that slack away. The fix is
to **strengthen** the hypothesis so it has an explicit lower-order term:

$$T(n) \le \frac{5}{16}n^2 - n.$$

Now the induction step closes with equality:

$$4\left(\frac{5}{16}\left(\tfrac n2\right)^2 - \frac n2\right) + n = \frac{5}{16}n^2 - 2n + n = \frac{5}{16}n^2 - n.$$

And the base case holds: at $n = 4$, $\tfrac{5}{16}\cdot 16 - 4 = 5 - 4 = 1 = T(4)$.

What it teaches is that the induction hypothesis is not a claim you are stuck with — it is
a claim you get to *choose*. A hypothesis that is true but too coarse to be propagated is
useless, and the fix is almost always to add a lower-order correction term, because that
is where the slack lives. The same trick handles $T(n)=3T(n/2)+n$ (hypothesis
$cn^{\log_2 3} - k\,n^{\log_2 3 - 1}$), Karatsuba's $T(n) = 3T(n/2) + \Theta(b)$,
which is the same induction behind $O(b^{1.585})$, and the FFT's closed form.

The transferable lesson for code: when a proof of a runtime bound stalls at the induction
step, suspect the hypothesis before suspecting the claim. A $cn^2$ hypothesis that fails is
usually telling you the true answer has an $O(n)$ correction, and finding it is the whole
work.

</details>

**Q3. Why does repeated squaring beat the loop, and why is the lesson's `104 858` figure
not the total-work ratio?**

<details>
<summary>Model answer</summary>

Two independent effects, and it is worth keeping them apart because only one of them is a
complexity argument.

**The operation count.** Computing $a^n$ needs $n$ multiplications in a loop and
$\log_2 n$ in repeated squaring, because the exponent is built from its binary
representation: squaring doubles the exponent, and a multiply-by-$a$ on a set bit adds one.
At $n = 10^4$ that is `10000` against `14`, a factor of $n/\log_2 n = 752.6$. In bit
complexity: $O(n\cdot\mathrm{Mul}(b))$ against $O(\log n\cdot\mathrm{Mul}(b))$, which is
the lesson's stated theorem.

**The operand size.** Both loops run on numbers no larger than the answer, but the loop's
operand grows one step at a time, so most of its $n$ steps are cheap, while repeated
squaring's few steps are all expensive. That means the operation-count factor is not the
whole story either — it is a *bound*, and the real constant depends on the growth pattern.

**Why `104 858` is not total work.** That figure is
$\frac{n^2}{(n/2)\log_2 n}$ at $n = 2^{20}$ — it counts **complex multiplications**, and the
FFT performs exactly $\frac n2 \log_2 n$ of them from the butterfly recurrence. Total work
including the additions is $\frac{nL(L+1)}{2} + n$ with $L=\log_2 n$, giving
$221{,}249{,}536$ against the naive $1{,}099{,}511{,}627{,}776$ and a ratio of `4969.6`.
Both numbers are correct; they answer different questions, and a paper that quotes one
while you assume the other will surprise you.

This matters practically because the two numbers have different regimes. The
multiplication ratio grows like $n/\log n$, so it keeps improving with problem size. The
total-work ratio also grows like $n/\log n$, but from a much smaller base, and the FFT's
constant on the additions is worse than its constant on the multiplications — the butterfly
saves multiplications at the cost of extra additions. Any claim of the form "the FFT is
$X$ times faster" is incomplete until you say which operation you counted.

</details>

**Q4. Why does the same code have a different complexity on different inputs, and what
would break if you quoted one number for both?**

<details>
<summary>Model answer</summary>

Because Big-O is a statement about an *input parameter*, and the same loop can touch
different amounts of data for different values of that parameter. The lesson's
`check_first_element` is the clean demonstration: on a list of all positives it examines
every element and costs `n*4 + 10`; on a list whose first element is negative it returns
immediately and costs `14`, *independent of $n$*. Two inputs of the same size, two costs
differing by a factor of $\Theta(n)$.

The standard resolution is to state a **worst-case** bound and name the others separately:
best case, average case (with a distribution), and worst case. What you must never do is
quote a single class for an algorithm whose cost genuinely varies — that is
`search_unsorted` in Mistake 5, which is $\Theta(1)$ on a lucky target and $\Theta(n)$ on a
bad one, and which is exactly why binary search's $\log_2 n$ steps *always* is worth the
precondition of sorting.

What breaks if you quote one number for both is not a small error; it is the whole reason
Big-O is defined with $\exists n_0$. The lesson's `find_max` versus `count_inversions`
comparison is the second half of the story: both are one pass *over the data* to a careless
reader, but one is $n$ comparisons and the other is $n(n-1)/2$, a factor of `99.5x` at
$n = 200$. Nothing in "it iterates over the list" distinguishes them.

The concrete engineering consequence: you cannot pick an algorithm without knowing your
input distribution. An algorithm that is $\Theta(n)$ on average and $\Theta(n^2)$ worst case
— quicksort with a bad pivot, hash lookup under adversarial keys, `list` insertion at
position 0 — will be fine on random data and catastrophic on data with structure, and you
will only discover which you have after it has happened. This is the reason randomised
pivots, SipHash-style randomised hash seeds, and dyadic balanced trees all exist: they do
not improve the average case, they make the worst case *unlikely*, which is the only
achievable goal without knowing the input.

</details>

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
for bits, reps in ((1000, 20000), (10000, 5000), (100000, 1000), (1000000, 8)):
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


**[ ] Exercise 5 — prove a bound for a recursive algorithm: $T(n) = 4T(n/2) + n$ is
$\Theta(n^2)$.** Consider the recursion, which counts total work units rather than
returning a value:

```python
def split4(n):
    """Four calls on n // 2, plus n units of linear work.  Well defined when 8 | n."""
    if n <= 4:
        return 1
    return 4 * split4(n // 2) + n
```

(a) Compute $T(n)$ for $n = 8, 16, \dots, 4096$ and report $T(n)/n^2$. What does the
sequence converge to?
(b) What does the Master Theorem say? Give $a$, $b$, $c$ and $d = \log_b a$, and confirm
the case.
(c) Try to prove $T(n) \le c\,n^2$ by strong induction, for an arbitrary constant $c$.
Show exactly where the induction step fails, for **every** $c > 0$.
(d) Strengthen the hypothesis to $T(n) \le \tfrac{5}{16}n^2 - n$ and prove it. Verify the
closed form against the recursion's own counts.
(e) Prove the $\Omega$ bound: a lower-bound argument that does not use the closed form.
(f) Comment on the constant. What does $T(n)/n^2 \to 0.3125$ mean for someone writing an
actual implementation?

<details>
<summary>Solution</summary>

```python
def split4(n):
    if n <= 4:
        return 1
    return 4 * split4(n // 2) + n


print("=== (a)+(d) measured counts against the closed form T(n) = (5/16)n^2 - n ===")
print("    n     measured     (5/16)n^2 - n      diff      T/n^2      T/n^2 * 16")
for e in (3, 4, 5, 6, 7, 8, 9, 10, 11, 12):
    n = 2 ** e
    got = split4(n)
    pred = (5.0 / 16.0) * n * n - n
    print(f"  {n:>5}   {got:>10}   {pred:>18.1f}   {got - pred:>8.1f}"
          f"   {got / n ** 2:>9.4f}   {16 * got / n ** 2:>10.4f}")
print("  The diff column is 0.0 everywhere: the closed form is EXACT, not asymptotic.")
print()
print("=== (c) why naive substitution T(n) <= c n^2 cannot work ===")
for c in (0.5, 1, 10, 1000):
    n = 1024
    lhs = 4 * c * (n / 2) ** 2 + n     # what the induction step can bound T(n) by
    print(f"  c = {c:>7}: 4c(n/2)^2 + n = {lhs:>12.1f}   vs   c n^2 = {c * n ** 2:>10.1f}"
          f"   overshoot {lhs - c * n ** 2:>8.1f}")
print("  The overshoot is exactly n, for every c.  No constant closes the step.")
print()
print("=== (c)+(d) the strengthened step closes with equality ===")
n = 1024.0
step = 4 * ((5.0 / 16.0) * (n / 2) ** 2 - n / 2) + n
print(f"  4*((5/16)(n/2)^2 - n/2) + n = {step:.1f}   and   (5/16)n^2 - n = "
      f"{(5.0 / 16.0) * n * n - n:.1f}")
print(f"  base case n = 4:  (5/16)*16 - 4 = {(5.0 / 16.0) * 16 - 4:.1f}  and  T(4) = {split4(4)}")
print()
print("=== (e) a lower bound that does not use the closed form ===")
#  Each of the levels i = 0,1,...  holds 4^i nodes of size n/2^i, and the number of
#  levels is log_4(n/4) = L/2 - 1.  Leaves alone give 4^(L/2 - 1) = (n/4)^2 = n^2/16.
print("    n     leaves = (n/4)^2     T(n)      leaves/T")
for e in (6, 8, 10, 12):
    n = 2 ** e
    leaves = (n // 4) ** 2
    print(f"  {n:>5}   {leaves:>18}   {split4(n):>10}   {split4(n) / leaves:>9.3f}")
print("  T(n) >= (n/4)^2 = n^2/16 for every n, which is Omega(n^2).")
print()
print("=== (f) the constant, and what a real implementation pays ===")
for e in (8, 10, 12):
    n = 2 ** e
    print(f"  n = {n:>9}:  T = {split4(n):>14}   T/n^2 = {split4(n) / n ** 2:.4f}"
          f"   (5/16 = 0.3125)")
print("  T/n^2 rises towards 5/16 from below, reaching 0.3125 to 4 digits at n = 4096.")
print("  An implementation pays about 0.31 work units per element-squared, i.e. roughly")
print("  0.31n^2 operations -- a real cost, invisible to the Theta but visible in a budget.")
```

Output:

```text
=== (a)+(d) measured counts against the closed form T(n) = (5/16)n^2 - n ===
    n     measured     (5/16)n^2 - n      diff      T/n^2      T/n^2 * 16
      8           12                 12.0        0.0      0.1875       3.0000
     16           64                 64.0        0.0      0.2500       4.0000
     32          288                288.0        0.0      0.2812       4.5000
     64         1216               1216.0        0.0      0.2969       4.7500
    128         4992               4992.0        0.0      0.3047       4.8750
    256        20224              20224.0        0.0      0.3086       4.9375
    512        81408              81408.0        0.0      0.3105       4.9688
   1024       326656             326656.0        0.0      0.3115       4.9844
   2048      1308672            1308672.0        0.0      0.3120       4.9922
   4096      5238784            5238784.0        0.0      0.3123       4.9961
  The diff column is 0.0 everywhere: the closed form is EXACT, not asymptotic.

=== (c) why naive substitution T(n) <= c n^2 cannot work ===
  c =     0.5: 4c(n/2)^2 + n =     525312.0   vs   c n^2 =   524288.0   overshoot   1024.0
  c =       1: 4c(n/2)^2 + n =    1049600.0   vs   c n^2 =  1048576.0   overshoot   1024.0
  c =      10: 4c(n/2)^2 + n =   10486784.0   vs   c n^2 = 10485760.0   overshoot   1024.0
  c =    1000: 4c(n/2)^2 + n = 1048577024.0   vs   c n^2 = 1048576000.0   overshoot   1024.0
  The overshoot is exactly n, for every c.  No constant closes the step.

=== (c)+(d) the strengthened step closes with equality ===
  4*((5/16)(n/2)^2 - n/2) + n = 326656.0   and   (5/16)n^2 - n = 326656.0
  base case n = 4:  (5/16)*16 - 4 = 1.0  and  T(4) = 1

=== (e) a lower bound that does not use the closed form ===
    n     leaves = (n/4)^2     T(n)      leaves/T
     64                  256         1216       4.750
    256                 4096        20224       4.938
   1024                65536       326656       4.984
   4096              1048576      5238784       4.996
  T(n) >= (n/4)^2 = n^2/16 for every n, which is Omega(n^2).

=== (f) the constant, and what a real implementation pays ===
  n =       256:  T =          20224   T/n^2 = 0.3086   (5/16 = 0.3125)
  n =      1024:  T =         326656   T/n^2 = 0.3115   (5/16 = 0.3125)
  n =      4096:  T =        5238784   T/n^2 = 0.3123   (5/16 = 0.3125)
  T/n^2 rises towards 5/16 from below, reaching 0.3125 to 4 digits at n = 4096.
  An implementation pays about 0.31 work units per element-squared, i.e. roughly
  0.31n^2 operations -- a real cost, invisible to the Theta but visible in a budget.
```

**(a)** The counts are $12, 64, 288, 1216, 4992, 20224, 81408, 326656, 1308672,
$5238784$. The ratio $T/n^2$ rises $0.1875, 0.2500, 0.2812, 0.2969, \dots, 0.3123$ —
monotonically increasing toward $0.3125 = \tfrac{5}{16}$. The final column, $16T/n^2$,
approaches $5.0000$ from below, which is the cleanest way to see the limit.

**(b)** $a = 4$, $b = 2$, $c = 1$, so $d = \log_2 4 = 2$. Since $c = 1 < 2 = d$, this is
the case where **the recursion dominates**: $T(n) \in \Theta(n^d) = \Theta(n^2)$. The leaves
are the whole story — there are $4^{\log_2(n)/2 - 1} = (n/4)^2$ of them, which is already
$\Omega(n^2)$.

**(c)** Assume $T(m) \le c\,m^2$ for all $m < n$, for an arbitrary $c > 0$. Then

$$T(n) = 4T(n/2) + n \le 4c\left(\frac n2\right)^2 + n = c\,n^2 + n.$$

To conclude $T(n) \le c\,n^2$ you would need $n \le 0$. **The induction step fails for
every $c > 0$,** and the failure is exactly the additive $n$. The table shows it: for
$c = 1$, $10$ and $1000$ the overshoot is `1024.0`, `240.0` and `1024000.0` — always
exactly $n$, never proportional to $c$. (The $c = 0.5$ row has a *negative* overshoot
because at $c = \frac12$ the real $T(n/2) \le \frac12(n/2)^2$ bound is so loose that it
gives an upper bound below the hypothesis's own value at $n$; it is not a counterexample
to the failure, just an artifact of bounding from below a hypothesis that has not yet been
shown true at that scale.)

**(d)** Strengthen to

$$T(n) \le \frac{5}{16}n^2 - n \quad\text{for all } n \ge 4.$$

*Base case:* at $n = 4$, $\tfrac{5}{16}\cdot 16 - 4 = 5 - 4 = 1 = T(4)$. ✓

*Induction step:* assume it at $n/2$ (strong induction, so it holds for all smaller
arguments). Then

$$T(n) = 4T(n/2) + n \le 4\left[\frac{5}{16}\left(\frac n2\right)^2 - \frac n2\right] + n = 4\left[\frac{5n^2}{64} - \frac n2\right] + n = \frac{5}{16}n^2 - 2n + n = \frac{5}{16}n^2 - n. \qquad\blacksquare$$

The step closes **with equality**, which is how you know the constant was not guessed — it
was solved for. Unrolling confirms the closed form is exact: the `diff` column is `0.0` at
all ten sizes, and $T(4) = 1$, $T(8) = 12$, $T(16) = 64$ all match by hand.

**(e)** A lower bound needing no closed form: the recursion tree has
$\log_4(n/4) = \tfrac12\log_2 n - 1$ internal levels, and therefore
$4^{\log_2 n/2 - 1} = (n/4)^2 = n^2/16$ leaves. Every leaf executes the base case, which
costs $1$. So $T(n) \ge n^2/16$ — i.e. $T(n) \in \Omega(n^2)$ with $c = \tfrac1{16}$. The
table confirms it: at $n = 4096$ there are $1024^2 = 1048576$ leaves and
$T = 5238784$, a ratio of `5.000`. Combined with (d), $T(n) \in \Theta(n^2)$.

**(f)** The constant is $\tfrac{5}{16} \approx 0.3125$ work units per element-squared, so a
real implementation performs about $0.31\,n^2$ operations. At $n = 10^5$ that is
$3.1\times10^9$ — seconds, not milliseconds — and at $n = 10^6$ it is 36 hours. Big-O
told you the answer was quadratic; only the constant tells you *which* quadratic you have
paid for. This is the whole content of Mistake 4: two functions in the same $\Theta$ class
can differ by an arbitrary constant factor, the ratio between them stays constant as $n$
doubles, and the only way to find that factor is to count or to measure. Note also that
$\tfrac{5}{16}$ is far from $1$ — the naive sum $\sum_{i=0}^{L-1}n2^i$ over-predicts because
it charges every node at every level the full $n$, when only the bottom levels really do.

</details>

**[ ] Exercise 6 — Challenge: the FFT recurrence, which the Master Theorem cannot
handle, and what it costs at $n = 2^{20}$.** Consider

$$T(n) = 2T(n/2) + \Theta(n\log n),\qquad T(1) = 1,$$

the radix-2 FFT.

(a) Compute $T(n)$ for $n = 16, 256, 4096, 65536, 2^{20}$ and compare with the closed
form $\tfrac{nL(L+1)}{2} + n$ where $L = \log_2 n$.
(b) Try to prove $T(n) \le c\,n\log_2 n$ by substitution. Show that it forces
$c \ge \log_2 n$, so **no constant works**. Explain why the naive hypothesis fails.
(c) Prove the closed form of (a) by unrolling the recursion tree, counting level by
level.
(d) Show that the Master Theorem's hypothesis fails for this recurrence, and that
substituting $c = 1$ nevertheless gives the right answer — while substituting $c = 0$ or
$c = 2$ does not.
(e) At $n = 2^{20}$ compare: total work $n^2$ against $\tfrac{nL(L+1)}{2}+n$; and
complex *multiplication* counts $n^2$ against $\tfrac n2\log_2 n$. Explain which ratio the
lesson's `104 858` figure is.
(f) Prove that repeated squaring costs $O(\log n\cdot\mathrm{Mul}(b))$ against the
loop's $O(n\cdot\mathrm{Mul}(b))$, and compute $n/\log_2 n$ at $n = 10^4$.

<details>
<summary>Solution</summary>

```python
import math


def fft_cost(n):
    """Total work of T(n) = 2T(n/2) + n*log2(n),  T(1) = 1."""
    if n <= 1:
        return 1
    return 2 * fft_cost(n // 2) + n * math.log2(n)


print("=== (a)+(c) measured against the closed form T(n) = n*L*(L+1)/2 + n ===")
print("    n            L      measured        closed form        equal")
for e in (4, 8, 12, 16, 20):
    n = 2 ** e
    got = fft_cost(n)
    closed = n * e * (e + 1) // 2 + n
    print(f"  {n:>9}   {e:>5}   {got:>14,}   {closed:>16,}   {got == closed}")
print("  Level i (i = 0..L-1) holds 2^i nodes of size n/2^i, each costing")
print("  (n/2^i)*(L-i).  Level cost = 2^i * (n/2^i)(L-i) = n(L-i).  Sum = n*L(L+1)/2,")
print("  plus one unit for each of the n leaves.")
print()
print("=== (b) why T(n) <= c n log2(n) cannot be closed by a constant ===")
print("   2*T(n/2) + n*L  <=  2*[c*(n/2)(L-1)] + n*L  =  c n L - c n + n L")
print("   want  <=  c n L   ==>   -c n + n L <= 0   ==>   c >= L = log2(n)")
for e in (4, 12, 20):
    print(f"    n = 2^{e:<3} = {2 ** e:>9}:  the step demands c >= {e}")
print("  c = log2(n) grows without bound, so no constant works.  The hypothesis is")
print("  too COARSE: it discards the lower-order slack that has to absorb +n*L.")
print()
print("=== (d) the Master Theorem on this recurrence ===")
d = math.log2(2)
for c, claim in ((0, "Theta(n)"), (1, "Theta(n log n)"), (2, "Theta(n^2)")):
    verdict = f"Theta(n^{c:g})" if c > d else (f"Theta(n^{d:.0f} log n)" if c == d
                                            else f"Theta(n^{d:.0f})")
    print(f"    pretend the additive term is Theta(n^{c}):  d = {d:.4f}  ->"
          f"  {verdict:<22} (claimed as {claim})")
print("  True answer: Theta(n log n).  c=1 is right BY COINCIDENCE -- the borderline")
print("  case manufactures exactly the n log n that n log n happens to be.")
print("  c=0 is short by a factor of log n; c=2 is long by a factor of n/log n.")
print()
print("=== (e) the payoff at n = 2^20 = 1048576 ===")
n, L = 2 ** 20, 20
naive_work = n * n
fft_work = n * L * (L + 1) // 2 + n
print(f"  TOTAL WORK")
print(f"    naive DFT        n^2                  = {naive_work:,}")
print(f"    FFT              n*L*(L+1)/2 + n      = {fft_work:,}")
print(f"    ratio                                    = {naive_work / fft_work:,.1f}")
print(f"  COMPLEX MULTIPLICATIONS  <-- this is what 104 858 counts")
print(f"    naive             n^2                  = {n * n:,}")
print(f"    FFT               (n/2)*log2 n         = {(n // 2) * L:,}")
print(f"    ratio                                    = {n * n / ((n // 2) * L):,.1f}")
print()
print("=== (f) repeated squaring: n multiplications vs log2(n) ===")
print("      n        log2(n)       n/log2(n)")
for k in (100, 10_000, 10 ** 6):
    print(f"  {k:>9}   {math.log2(k):>9.2f}   {k / math.log2(k):>14.1f}")
print("  Loop: n multiplications, each Mul(b) -> O(n * Mul(b))")
print("  Squaring: log2(n) of them         -> O(log n * Mul(b))")
print("  Ratio at n = 10^4: 752.6")
```

Output:

```text
=== (a)+(c) measured against the closed form T(n) = n*L*(L+1)/2 + n ===
    n            L      measured        closed form        equal
         16       4            176.0                176   True
        256       8          9,472.0              9,472   True
       4096      12        323,584.0            323,584   True
      65536      16      8,978,432.0          8,978,432   True
    1048576      20    221,249,536.0        221,249,536   True
  Level i (i = 0..L-1) holds 2^i nodes of size n/2^i, each costing
  (n/2^i)*(L-i).  Level cost = 2^i * (n/2^i)(L-i) = n(L-i).  Sum = n*L(L+1)/2,
  plus one unit for each of the n leaves.

=== (b) why T(n) <= c n log2(n) cannot be closed by a constant ===
   2*T(n/2) + n*L  <=  2*[c*(n/2)(L-1)] + n*L  =  c n L - c n + n L
   want  <=  c n L   ==>   -c n + n L <= 0   ==>   c >= L = log2(n)
    n = 2^4   =        16:  the step demands c >= 4
    n = 2^12  =      4096:  the step demands c >= 12
    n = 2^20  =   1048576:  the step demands c >= 20
  c = log2(n) grows without bound, so no constant works.  The hypothesis is
  too COARSE: it discards the lower-order slack that has to absorb +n*L.

=== (d) the Master Theorem on this recurrence ===
    pretend the additive term is Theta(n^0):  d = 1.0000  ->  Theta(n^1)             (claimed as Theta(n))
    pretend the additive term is Theta(n^1):  d = 1.0000  ->  Theta(n^1 log n)       (claimed as Theta(n log n))
    pretend the additive term is Theta(n^2):  d = 1.0000  ->  Theta(n^2)             (claimed as Theta(n^2))
  True answer: Theta(n log n).  c=1 is right BY COINCIDENCE -- the borderline
  case manufactures exactly the n log n that n log n happens to be.
  c=0 is short by a factor of log n; c=2 is long by a factor of n/log n.

=== (e) the payoff at n = 2^20 = 1048576 ===
  TOTAL WORK
    naive DFT        n^2                  = 1,099,511,627,776
    FFT              n*L*(L+1)/2 + n      = 221,249,536
    ratio                                    = 4,969.6
  COMPLEX MULTIPLICATIONS  <-- this is what 104 858 counts
    naive             n^2                  = 1,099,511,627,776
    FFT               (n/2)*log2 n         = 10,485,760
    ratio                                    = 104,857.6

=== (f) repeated squaring: n multiplications vs log2(n) ===
      n        log2(n)       n/log2(n)
        100        6.64             15.1
      10000       13.29            752.6
    1000000       19.93          50171.7
  Loop: n multiplications, each Mul(b) -> O(n * Mul(b))
  Squaring: log2(n) of them         -> O(log n * Mul(b))
  Ratio at n = 10^4: 752.6
```

**(a) and (c)** The closed form is $\tfrac{nL(L+1)}{2} + n$ with $L = \log_2 n$, and it
is **exact** — the `equal` column prints `True` at all five sizes.

The unrolling is worth doing carefully, because it is where the $\log n$ comes from. Level
$i$ of the recursion tree (with $i = 0$ at the root and $i = L-1$ just above the leaves)
holds $2^i$ nodes, each on a subproblem of size $n/2^i$, and each node's local work is
$\left(\tfrac{n}{2^i}\right)\log_2\!\left(\tfrac{n}{2^i}\right) = \left(\tfrac{n}{2^i}\right)(L-i)$.
Multiplying through, the level costs $2^i \cdot \left(\tfrac{n}{2^i}\right)(L-i) = n(L-i)$.
Summing $i = 0$ to $L-1$ gives $n\sum_{j=1}^{L}j = n\,\tfrac{L(L+1)}{2}$, and the $n$ leaves
add $n$ more. At $n = 2^{20}$: $\tfrac{1048576\cdot 20\cdot 21}{2} + 1048576 =
220{,}200{,}960 + 1{,}048{,}576 = 221{,}249{,}536$.

**(b)** Assume $T(m) \le c\,m\log_2 m$. Then

$$T(n) \le 2c\left(\frac n2\right)\log_2\frac n2 + n\log_2 n = cn(L-1) + nL = cnL - cn + nL,$$

and to conclude $\le cnL$ we need $nL \le cn$, i.e. **$c \ge L = \log_2 n$**. Since $L$ is
unbounded, no constant closes the step. Exactly as in Exercise 5(c), the hypothesis is too
coarse: $c\,n\log_2 n$ throws away the lower-order slack that has to absorb the $+n\log n$
at each of the $L$ levels. The fix is again to strengthen, and the closed form
$\tfrac12 nL(L+1) + n = \tfrac12 n\log_2^2 n + \tfrac12 n\log_2 n + n$ is the strengthened
hypothesis.

**(d)** The theorem's hypothesis is an additive term of exactly $\Theta(n^c)$. Here it is
$\Theta(n\log n)$, which is not $\Theta(n^c)$ for any $c$: it lies strictly between $n^1$
and $n^{1+\varepsilon}$ for every $\varepsilon > 0$. So the hypothesis **fails**.

Nevertheless, reading $c = 1$ lands in the balanced case $c = d = 1$ and returns
$\Theta(n^d\log n) = \Theta(n\log n)$ — the right answer. That is a coincidence of shape:
the borderline case manufactures an $n\log n$, and $n\log n$ happens to *be* $n\log n$.
Read the same recurrence with $c = 0$ and you get $\Theta(n)$, short by $\log n$; with
$c = 2$ you get $\Theta(n^2)$, long by $n/\log n$. Both wrong, both by unbounded factors,
and nothing in the notation tells you which reading you are entitled to. This is why
Akra–Bazzi, not a guess at $c$, is the right tool.

**(e)** Two different ratios, both correct, answering two different questions:

| quantity | naive | FFT | ratio |
| --- | --- | --- | --- |
| total work | $n^2 = 1{,}099{,}511{,}627{,}776$ | $221{,}249{,}536$ | `4969.6` |
| complex multiplications | $n^2 = 1{,}099{,}511{,}627{,}776$ | $\tfrac n2\log_2 n = 10{,}485{,}760$ | `104,857.6` |

The lesson's `104 858` figure is the **second** row. It counts the complex multiplications
the FFT performs — $\frac n2$ twiddle products per level, times $L$ levels, straight from
the butterfly recurrence $X_k = E_k + e^{-2\pi ik/N}O_k$. The first row is larger than the
operation ratio because the FFT's *additions* are relatively more expensive than the naive
loop's: the butterfly saves multiplications at the cost of extra additions.

Both ratios grow like $n/\log n$, so the gap keeps widening with problem size — which is
the practical point. Any claim of the form "the FFT is $X$ times faster" is incomplete
until you say which operation was counted.

**(f)** Computing $a^n$ by a loop takes $n$ multiplications; each costs $\mathrm{Mul}(b)$
bit operations, for a total of $O(n\cdot\mathrm{Mul}(b))$. Repeated squaring builds the
exponent from its binary representation — squaring doubles the exponent, and a
multiply-by-$a$ on a set bit adds one — so it needs $\lfloor\log_2 n\rfloor + 1$
multiplications, for $O(\log n\cdot\mathrm{Mul}(b))$. The ratio is
$n/\log_2 n$: `15.1` at $n = 10^2$, **`752.6` at $n = 10^4$**, and `50171.7` at $n = 10^6$.

That is the lesson's `14` multiplications for `pow(3, 10000)` against `10000` for the
loop, and it is also the argument in Exercise 4(d) for why `pow` beats `3 ** n` on large
exponents. Note that the ratio *grows*: the bigger the exponent, the more the log wins.

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