# 24 — Recurrence Relations

**Part**: part02_discrete_combinatorics · **Prerequisites**: 23 · **Time**: 40 min

---

## In Plain Words

A recurrence relation is a rule that says: to get the next value, take the
previous ones and apply this formula. Start it off with one or two known values
and you can generate everything after that. The Fibonacci sequence is the
famous one — each number is the sum of the two before it — but the pattern is
everywhere: the running total of an array, the number of comparisons merge sort
performs, the number of calls a recursive function makes, the number of ways to
tile a corridor with dominoes.

The reason this lesson sits inside a counting course, and the reason it deserves
its own lesson, is that a recurrence relation is how you talk about an algorithm.
When you write "this function calls itself twice on half the input and then does
linear work", you have written a recurrence. Solving it — finding a closed form
for what the recurrence produces — is how you find out that your algorithm is
fine, or that it takes 30 years.

Solving usually goes one of three ways. You unroll the recurrence a few times and
guess the pattern from the numbers, which works for anything you can actually
compute. You look for the *characteristic equation* — substitute rⁿ into the
recurrence and solve the resulting polynomial — which gives you an exact formula
for linear recurrences, and it is about four lines of algebra once you know it. Or,
for the divide-and-conquer recurrences that dominate computer science, you use the
**master theorem**, a lookup table that says "if the work done at the top matches
the work done below, you get a log factor, and if not, one of the two wins".

There is a fourth thing happening underneath all of this. When a recursive
function keeps asking for the same answer, you remember the answers instead of
recomputing them, and that is *dynamic programming*. A recurrence relation is the
mathematics of a memo table. Memoised Fibonacci is 70 times faster for n = 30 and
it is the same technique as bottom-up tabulation, as the Viterbi algorithm, and as
the Bellman equation in reinforcement learning.

## Why Computer Science Cares

- **Runtime analysis is recurrence analysis.** Every divide-and-conquer algorithm
  gives you a recurrence. The master theorem turns `2·T(n/2) + O(n)` into
  Θ(n log n) in one lookup, which is how you know merge sort is optimal and how
  you know that adding a second recursive call per level is catastrophic.
- **Naive recursion vs memoisation.** `fib(30)` written as `fib(n-1) + fib(n-2)`
  makes 1,346,268 calls. The same function with a cache makes 31. That gap is the
  entire argument for dynamic programming, and Lesson
  [81](../part06_algorithms_math/81_amortized_analysis.md) makes it precise.
- **Logarithmic Fibonacci.** Fast doubling and matrix exponentiation compute
  F(200) — a 42-digit number — in a few dozen operations instead of 10⁴², by
  multiplying 2×2 matrices. This is the template for every "compute this huge
  number" problem: Fibonacci, matrix powers, Catalan numbers, Stirling numbers,
  integer partitions.
- **Counting with structure.** Tiling a 2×n corridor, counting binary strings with
  no consecutive ones, counting independent sets on a path — all are recurrences,
  and all appear in coding interviews precisely because they are easy to state and
  easy to check.
- **Fibonacci numeration.** Zeckendorf's theorem says every positive integer has a
  unique representation as a sum of non-consecutive Fibonacci numbers. This is a
  real numeral system, it is near-optimal in expected length (1.44 bits per
  integer), and the related Fibonacci coding is prefix-free and instantly
  decodable.
- **Fibonacci in nature.** The golden ratio φ ≈ 1.618 shows up in phyllotaxis — the
  arrangement of leaves around a stem and florets in a flower head — where the
  divergence angle is 137.5°, chosen because successive turns are as far apart as
  possible. Pinecones, sunflowers, and the spirals of succulents all show it. It
  is a genuine and much-discussed phenomenon, though not the universal proof of
  design that folklore claims.
- **Melting an ice cube.** Cutting it into pieces, one cut at a time, takes exactly
  n − 1 cuts regardless of strategy — an invariant, because each cut increases the
  piece count by exactly one. Recurrences are how you find invariants like this.

## The Formal Version

**Definition.** A **recurrence relation** for a sequence a₀, a₁, a₂, … expresses
aₙ for n ≥ n₀ in terms of earlier terms. The fixed values a₀, …, a_{n₀−1} are the
**initial conditions**. A recurrence together with its initial conditions
determines the sequence uniquely.

**Definition.** A recurrence is **linear** if aₙ appears only to the first power
and no other term depends nonlinearly on it. It is **homogeneous** if the
right-hand side contains no term depending only on n.

**Theorem (Unrolling).** For a linear homogeneous recurrence of order k, the
sequence is determined and can be computed in O(n) time by iterating from the
initial conditions.

*Explanation.* Each step uses only values already computed, so the sequence is
built in order. This is exactly a `for` loop, and it is the fallback whenever the
closed form is unknown.

**Theorem (Characteristic equation).** Consider

    aₙ = c₁aₙ₋₁ + c₂aₙ₋₂ + ⋯ + c_k a_{n−k} + f(n)

with real coefficients. For the homogeneous part (f(n) = 0), set

    rᵏ = c₁rᵏ⁻¹ + c₂rᵏ⁻² + ⋯ + c_k

This is the **characteristic equation**. If it has k distinct real roots
r₁, …, r_k, then every solution is

    aₙ = A₁r₁ⁿ + A₂r₂ⁿ + ⋯ + A_k r_kⁿ

where the constants A₁, …, A_k are fixed by the k initial conditions. If r is a
root of multiplicity m, its contribution is (A₁ + A₂n + ⋯ + A_m n^{m−1})·rⁿ.

*Explanation.* Substitute aₙ = rⁿ into the homogeneous recurrence: every term
becomes a multiple of rⁿ, and the equation reduces to the characteristic
equation. So each root produces one genuine solution, and k independent solutions
span the k-dimensional space of solutions — the same dimension as the number of
free initial conditions. Note the solution must involve only rⁿ, never rⁿ⁻¹ or any
other power, because that is the form that was substituted in.

**Theorem (Particular solution).** For the non-homogeneous recurrence above with
f(n) = K·pⁿ, try a particular solution aₙ = A·pⁿ with A = K/(pᵏ − c₁pᵏ⁻¹ − ⋯ − c_k).
The general solution is the homogeneous part plus this particular solution.

*Explanation.* Substituting aₙ = A·pⁿ makes every term carry a factor pⁿ, and the
remaining coefficient is exactly the denominator above. If p is itself a root of
the characteristic equation of multiplicity m, multiply the trial form by nᵐ.

**Theorem (Dominant root / Θ estimate).** If r₁ is the characteristic root of
largest absolute value, then aₙ = Θ(|r₁|ⁿ) for any initial conditions that do not
cancel it.

*Explanation.* The other terms rᵢⁿ for |rᵢ| < |r₁| are eventually negligible
compared to r₁ⁿ. This is the single most important consequence: **the growth rate
of a linear recurrence is the largest root, and you never need the constants to
know it.**

**Theorem (Master theorem).** Let T(n) = a·T(n/b) + Θ(nᵈ) with a ≥ 1, b > 1,
d ≥ 0, and n a power of b. Then

    if a < bᵈ :  T(n) = Θ(nᵈ)
    if a = bᵈ :  T(n) = Θ(nᵈ log n)
    if a > bᵈ :  T(n) = Θ(n^{log_b a})

*Explanation.* Solve by the substitution n = bᵏ so the recurrence becomes
T(bᵏ) = a·T(b^{k−1}) + Θ(b^{kd}). The comparison that decides the case is between
the work done at the top level (nᵈ) and the total work of the a recursive calls
(a·nᵈ/bᵈ). If the top dominates, each level costs nᵈ and there are log_b n
levels, so nᵈ log n. If the recursion dominates, work multiplies by a each level
and depth is log_b n, giving n^{log_b a}. Full treatment in Lesson
[80](../part06_algorithms_math/80_big_o_and_complexity.md).

**Theorem (Zeckendorf's theorem).** Every positive integer has a unique
representation as a sum of non-consecutive Fibonacci numbers, using the sequence
1, 2, 3, 5, 8, 13, …

*Explanation.* Greedy from the largest Fibonacci number not exceeding n gives a
representation. Uniqueness is the deeper half: if a sum had two such
representations, take the largest Fibonacci number whose presence differs and note
that no sum of non-consecutive smaller Fibonacci numbers can equal it, since the
largest possible such sum below it is F_k − 1. The greedy algorithm terminates
because F_{k+1} − F_k = F_{k−1} and subtracting leaves a smaller remainder.

## Worked Example

**The recurrence.** A bacterial population doubles every hour, except that in every
third hour one cell is consumed by a phage. Let aₙ be the population after n
hours, starting from one cell:

    aₙ = 2·aₙ₋₁ − [3 | n],    a₀ = 1

where [3 | n] is 1 when n is divisible by 3 and 0 otherwise.

**Step 1 — Unroll and tabulate.** Never solve before computing; the table is
ground truth and it will catch any indexing error later.

| n | aₙ | rule applied |
| - | --- | - |
| 0 | 1 | given |
| 1 | 2 | 2·1, 3 ∩ 1 is false |
| 2 | 4 | 2·2 |
| 3 | 7 | 2·4 − 1, 3 \| 3 |
| 4 | 14 | 2·7 |
| 5 | 28 | 2·14 |
| 6 | 55 | 2·28 − 1, 3 \| 6 |
| 7 | 110 | 2·55 |
| 8 | 220 | 2·110 |
| 9 | 439 | 2·220 − 1, 3 \| 9 |

**Step 2 — The coefficients are periodic, not constant.** The rule “times
8, minus 1” does not hold for every step, so a fixed-coefficient characteristic
equation does not apply directly. But three doublings pass between consecutive
phage events, so look at the subsequence bₖ = a₃ₖ:

    b₀ = 1,  b₁ = 7,  b₂ = 55,  b₃ = 439

**Step 3 — Derive the subsequence recurrence carefully.** Starting from
a₃ₖ and stepping forward three times:

    a₃ₖ₊₁ = 2·a₃ₖ        (3k+1 not divisible by 3)
    a₃ₖ₊₂ = 2·a₃ₖ₊₁  (3k+2 not divisible by 3)
    a₃ₖ₊₃ = 2·a₃ₖ₊₂ − 1 = 8·a₃ₖ − 1

So bₖ = 8·bₖ₋₁ − 1, with b₀ = 1. This is the step where slips
happen: the third step's −1 must be applied *after* the doubling, not before,
and the three doublings apply to the *old* value, not to an intermediate one.
Note also that only one −1 appears in three steps, so it is not scaled by 8.

**Step 4 — Solve it.** Non-homogeneous: bₖ = 8bₖ₋₁ − 1.

- Homogeneous part: bₖ = 8bₖ₋₁, characteristic equation r − 8 = 0, root
  r = 8, giving A·8ᵏ.
- Particular solution: try a constant B. Then B = 8B − 1, so 7B = 1 and B = 1/7.
- General solution: bₖ = A·8ᵏ + 1/7.
- Initial condition: b₀ = 1 gives A + 1/7 = 1, so A = 6/7.

    a₃ₖ = (6·8ᵏ + 1) / 7

**Step 5 — Recover the other residue classes and verify.** Multiplying by 2 and
then by 4 gives the rest:

    a₃ₖ₊₁ = (12·8ᵏ + 2)/7        a₃ₖ₊₂ = (24·8ᵏ + 4)/7

Check against the table: k = 0 gives (6+1)/7 = 1, (12+2)/7 = 2, (24+4)/7 = 4 — matches
a₀, a₁, a₂. k = 1 gives 7, 14, 28 — matches a₃, a₄, a₅. k = 2 gives 55,
110, 220 — matches a₆, a₇, a₈. Every entry checks.

**Step 6 — The conclusion you actually needed.** The growth rate is the dominant
root 8 per three steps, which is 2 per step. So aₙ = Θ(2ⁿ) — the phage has no
effect on the asymptotics at all, it subtracts a constant once every three
doublings. That answer was available from Step 3 without any algebra at all, and
it is the answer that matters for a capacity plan. The closed form is only worth
computing when you need exact values.

## Runnable Code

Recurrences defined as data, then solved by three different methods and compared.

```python
def iterate(coeffs, initial, n):
    """a[n] = sum(coeffs[i] * a[n-1-i]).  Homogeneous, order len(coeffs).

    Build the sequence one term at a time from the initial conditions -- the most
    general and always-correct method."""
    a = list(initial)
    while len(a) <= n:
        nxt = sum(c * a[len(a) - 1 - i] for i, c in enumerate(coeffs))
        a.append(nxt)
    return a

def characteristic_roots(coeffs):
    """Real roots of r^k - c1 r^(k-1) - ... - ck = 0.

    Polynomial in descending powers is [1, -c1, -c2, ...]. We find roots by
    scanning for sign changes on a grid and polishing each with bisection -- simple
    and honest about its limits (it finds real roots only, which is all the
    recurrences in this lesson need)."""
    poly = [1.0] + [-float(c) for c in coeffs]

    def f(x):
        v = 0.0
        for c in poly:
            v = v * x + c
        return v

    def remember(r):
        if all(abs(r - g) > 1e-6 for g in found):
            found.append(r)

    lo, hi, steps = -50.0, 50.0, 100000
    found = []
    prev_x, prev_y = lo, f(lo)
    if prev_y == 0.0:
        remember(lo)
    for i in range(1, steps + 1):
        x = lo + (hi - lo) * i / steps
        y = f(x)
        if y == 0.0:
            remember(x)            # the grid landed exactly on a root
        elif prev_y * y < 0:
            # bisect the bracket [prev_x, x] to polish the root
            a, b, fa = prev_x, x, prev_y
            for _ in range(200):
                mid = (a + b) / 2
                fm = f(mid)
                if fa * fm <= 0:
                    b = mid
                else:
                    a, fa = mid, fm
            remember((a + b) / 2)
        prev_x, prev_y = x, y
    return sorted(found)

# The simplest case there is: a[n] = 2*a[n-1] with a[0] = 1. The characteristic
# equation is r - 2 = 0, so the solution is a[n] = A*2^n and a[0] = 1 gives A = 1.
seq = iterate([2], [1], 8)
roots = characteristic_roots([2])
print("a[n] = 2 a[n-1], a[0] = 1")
print(f"  iterated           : {seq}")
print(f"  characteristic root: {roots[0]:.6f}")
print(f"  closed form 2^n    : {[2**n for n in range(9)]}")
print(f"  matches            : {seq == [2**n for n in range(9)]}")

# a[n] = 3 a[n-1] - 2 a[n-2], a[0] = 1, a[1] = 3 -> solution 2^(n+1) - 1
coeffs, initial = [3, -2], [1, 3]
seq = iterate(coeffs, initial, 10)
r1, r2 = characteristic_roots(coeffs)
# A*r1^n + B*r2^n with A + B = a0, A*r1 + B*r2 = a1
A = (initial[1] - r2 * initial[0]) / (r1 - r2)
B = initial[0] - A
closed = [A * r1**n + B * r2**n for n in range(11)]
print(f"\na[n] = 3 a[n-1] - 2 a[n-2], a0 = 1, a1 = 3")
print(f"  iterated      : {seq}")
print(f"  roots         : {r1:.6f}, {r2:.6f}")
print(f"  closed form   : {[round(v, 9) for v in closed]}")
print(f"  exact 2^(n+1)-1: {[2**(n+1) - 1 for n in range(11)]}")
print(f"  max error     : {max(abs(s - c) for s, c in zip(seq, closed)):.2e}")
```

Fibonacci: iteration, recursion with a memo, fast doubling, and matrix
exponentiation.

```python
from functools import lru_cache

calls = 0

def fib_naive(n):
    """a[n] = a[n-1] + a[n-2]. Without a cache this recomputes the same values
    exponentially many times."""
    global calls
    if n < 2:
        return n
    calls += 1
    return fib_naive(n - 1) + fib_naive(n - 2)

@lru_cache(maxsize=None)
def fib_memo(n):
    """Same recurrence, but each (n) is computed once. The memo table *is* the
    dynamic program."""
    if n < 2:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)

def fib_fast_doubling(n):
    """F(2k) = F(k)(2F(k+1) - F(k)),  F(2k+1) = F(k)^2 + F(k+1)^2.

    Halves n at every step, so this is O(log n) instead of O(phi^n)."""
    def fd(k):
        if k == 0:
            return 0, 1
        a, b = fd(k // 2)          # (F(m), F(m+1)) with m = k // 2
        c = a * (2 * b - a)        # F(2m)
        d = a * a + b * b          # F(2m+1)
        return (d, c + d) if k % 2 else (c, d)
    return fd(n)[0]

def fib_matrix(n):
    """[[F(n+1), F(n)],[F(n), F(n-1)]] = [[1,1],[1,0]]^n, computed by repeated
    squaring in O(log n) matrix multiplications."""
    def mul(A, B):
        return [
            [A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
            [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]],
        ]

    result = [[1, 0], [0, 1]]
    base = [[1, 1], [1, 0]]
    while n:
        if n & 1:
            result = mul(result, base)
        base = mul(base, base)
        n //= 2
    return result[0][1]

calls = 0
print(f"F(25) = {fib_naive(25):,} computed by naive recursion")
print(f"  calls made (no memo)   : {calls:,}")
print(f"  distinct subproblems   : {26}   (memoised work)")
print(f"F(25) memoised           : {fib_memo(25):,}")
print(f"F(200) fast doubling     : {fib_fast_doubling(200)}")
print(f"F(200) matrix power      : {fib_matrix(200)}")
print(f"agree: {fib_fast_doubling(200) == fib_matrix(200)}")
print(f"F(200) has {len(str(fib_matrix(200)))} digits")

# The ratio of consecutive terms converges to the golden ratio.
seq = [fib_memo(i) for i in range(1, 15)]
ratios = [seq[i + 1] / seq[i] for i in range(len(seq) - 1)]
phi = (1 + 5**0.5) / 2
print(f"F(n+1)/F(n) for n=1..13 : {[round(r, 4) for r in ratios[:6]]} ...")
print(f"golden ratio phi        : {phi:.10f}")
print(f"F(13)/F(12)             : {ratios[-1]:.6f}")
```

The master theorem, and a merge sort whose comparisons are actually counted.

```python
from math import log2

def merge_sort(a):
    """Returns (number of comparisons, sorted list)."""
    if len(a) <= 1:
        return 0, a
    mid = len(a) // 2
    c_left, left = merge_sort(a[:mid])
    c_right, right = merge_sort(a[mid:])
    merged = []
    i = j = comparisons = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
        comparisons += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return c_left + c_right + comparisons, merged

def master_theorem(a, b, d):
    """T(n) = a T(n/b) + Theta(n^d), for a >= 1, b > 1, d >= 0."""
    if a < b**d:
        return f"Theta(n^{d})"
    if a == b**d:
        return "Theta(log n)" if d == 0 else f"Theta(n^{d} log n)"
    return f"Theta(n^{log2(a) / log2(b):.3f})"

recurrences = [
    ("binary search         ", 1, 2, 0),
    ("T(n)=2T(n/2)+1        ", 2, 2, 0),
    ("T(n)=2T(n/2)+n  merge", 2, 2, 1),
    ("T(n)=3T(n/2)+n        ", 3, 2, 1),
    ("T(n)=4T(n/2)+n        ", 4, 2, 1),
    ("T(n)=2T(n/2)+n^2      ", 2, 2, 2),
    ("T(n)=2T(n/3)+n  Karat", 2, 3, 1),
]

def expand(n, a, b, d):
    """Exact cost of the full recursion tree, for n a power of b."""
    if n <= 1:
        return 0
    return a * expand(n // b, a, b, d) + n**d

print(f"{'recurrence':22s} {'a':>2} {'b':>2} {'d':>2} {'master theorem':>18} {'exact T(32)':>13}")
for name, a, b, d in recurrences:
    print(f"{name:22s} {a:2d} {b:2d} {d:2d} {master_theorem(a, b, d):>18} "
          f"{expand(32, a, b, d):13,d}")

print()
print("worst-case merge sort comparisons, measured and checked against")
print("the closed form n*log2(n) - n + 1 for n = 2^k:")
from itertools import permutations
for n in (2, 4, 6, 8):
    worst = max(merge_sort(list(p))[0] for p in permutations(range(n)))
    k = 1
    while k < n:
        k *= 2
    print(f"  n={n}: exhaustive worst case = {worst}, "
          f"closed form at n={k} = {k * int(log2(k)) - k + 1}")
```

Zeckendorf's theorem and Fibonacci coding — a real numeral system built on the
recurrence.

```python
FIB = [1, 2]
while FIB[-1] <= 100_000:
    FIB.append(FIB[-1] + FIB[-2])  # 1, 2, 3, 5, 8, ... Fibonacci numbers

def zeckendorf(n):
    """Greedy decomposition into non-consecutive Fibonacci numbers.

    Returns the 1-based indices into FIB."""
    assert n > 0
    indices = []
    for i in range(len(FIB) - 1, -1, -1):
        if FIB[i] <= n:
            n -= FIB[i]
            indices.append(i + 1)
    assert n == 0
    return indices

def fib_encode(n):
    """Fibonacci code: '1' at each index of the Zeckendorf form, padded to the
    highest index, then a terminating '0'."""
    indices = zeckendorf(n)
    bits = ["0"] * max(indices)
    for i in indices:
        bits[i - 1] = "1"
    return "".join(bits) + "0"

def fib_decode(code):
    """Streaming decoder: walk the code left to right keeping (F_i, F_{i+1});
    every '1' adds F_i to the total."""
    a, b = 1, 2
    total = 0
    for bit in code:
        if bit == "1":
            total += a
        a, b = b, a + b
    return total

print("Zeckendorf decompositions:")
for v in (1, 2, 3, 4, 100, 255, 1000):
    idx = zeckendorf(v)
    print(f"  {v:5d} = {' + '.join(str(FIB[i-1]) for i in idx)}")

# The representation is always valid: non-consecutive indices, no two adjacent.
def is_valid_zeckendorf(indices):
    return all(abs(indices[i] - indices[i + 1]) > 1 for i in range(len(indices) - 1))

print(f"\nall decompositions non-consecutive: "
      f"{all(is_valid_zeckendorf(zeckendorf(v)) for v in range(1, 3000))}")

print("\nFibonacci coding (prefix-free, instantly decodable):")
for v in (1, 3, 4, 7, 100):
    code = fib_encode(v)
    print(f"  {v:4d} -> {code:12s} -> {fib_decode(code):4d}")

ok = all(fib_decode(fib_encode(v)) == v for v in range(1, 20000))
print(f"round-trip correct for every value 1..19999: {ok}")

# Why it is efficient: mean length per value is about log2(phi) bits.
import math
total_bits = sum(len(fib_encode(v)) for v in range(1, 20001))
print(f"mean code length: {total_bits / 20000:.3f} bits "
      f"(plain binary: {math.log2(20001):.3f} bits)")
```

## Common Mistakes

**1. Solving the recurrence and forgetting to check against computed values.**

> Wrong: derive aₙ = (2·4ᵏ + 1)/3, ship it.
> Right: compute a₁, a₂, a₃ from the recurrence first and compare. In the worked
> example above, a plausible-looking closed form disagreed with the table at the
> very first check, and the table was right.
> Why the wrong one is tempting: algebra that is internally consistent *feels*
> verified. Only comparison with ground truth catches an indexing mistake.

**2. Using r^{n-1} in the solution form.**

> Wrong: "For aₙ = 2aₙ₋₁ the characteristic root is 2, so aₙ = A·2^{n−1}."
> Right: A·2ⁿ. You substitute aₙ = rⁿ, so only rⁿ appears. Using 2^{n−1} is
> equivalent up to a rescaling of A, but it silently breaks when you have two
> roots and solve for two constants.
> Why the wrong one is tempting: the recurrence literally mentions aₙ₋₁, so
> matching indices feels natural. It is not what the substitution gives.

**3. Ignoring repeated roots.**

> Wrong: "aₙ = 2aₙ₋₁ − aₙ₋₂ has characteristic root 1 (double), so aₙ = A + B."
> Right: a repeated root of multiplicity m contributes a polynomial in n times that
> power: aₙ = (A + Bn)·1ⁿ = A + Bn. Dropping the n term makes it impossible to fit
> both initial conditions, and the sequence turns out to be n + 1.
> Why the wrong one is tempting: a quadratic with a double root is visually
> "one root", so it is easy to record one solution instead of two.

**4. Reading the master theorem as a total function.**

> Wrong: "T(n) = T(n/2) + n solves to Θ(n) by the master theorem."
> Right: It does not apply. The theorem requires T(n) = a·T(n/b) + Θ(nᵈ) with
> **a ≥ 1**. Your recurrence has a = 0. That is a linear scan, and the answer
> happens to be Θ(n), but the theorem did not tell you that — the *recurrence
> theorem* for a = 0 does, via the recursion tree.
> Why the wrong one is tempting: the shape matches, only one coefficient is off,
> and the guess is right. Being accidentally right here means you have learned
> nothing and will misapply the theorem somewhere it actually bites.

**5. Using the master theorem when the work is not polynomial.**

> Wrong: "T(n) = 2T(n/2) + n log n is Θ(n log² n) by the master theorem."
> Right: Not applicable; f(n) = n log n is not Θ(nᵈ). The recursion-tree method
> gives Θ(n log² n) — the top-level cost is n log n and there are log n levels, so
> n log² n — but you must use a different tool.
> Why the wrong one is tempting: n log n "feels like" a degree-2 polynomial, and
> the shape of the recurrence is otherwise perfect.

---

## Exercises and Solutions

**[ ] Exercise 1 — Iterate and verify.** Solve aₙ = 4aₙ₋₁ − 3aₙ₋₂ with a₀ = 3,
a₁ = 6 by unrolling, by the characteristic equation, and by checking that your
closed form reproduces the sequence.

<details>
<summary>Solution</summary>

Characteristic equation: r² = 4r − 3, i.e. r² − 4r + 3 = 0, which factors as
(r − 1)(r − 3) = 0. Roots 1 and 3.

General solution: aₙ = A·1ⁿ + B·3ⁿ. Initial conditions:
A + B = 3 and A + 3B = 6. Subtracting gives 2B = 3, so B = 3/2 and A = 3/2.

    aₙ = (3/2) + (3/2)·3ⁿ = (3/2)(1 + 3ⁿ)

Check n = 0: (3/2)(2) = 3 ✓. n = 1: (3/2)(4) = 6 ✓. n = 2: (3/2)(10) = 15, and the
recurrence gives 4·6 − 3·3 = 15 ✓.

```python
def iterate(coeffs, initial, n):
    a = list(initial)
    while len(a) <= n:
        a.append(sum(c * a[len(a) - 1 - i] for i, c in enumerate(coeffs)))
    return a

seq = iterate([4, -3], [3, 6], 8)
closed = [(3 / 2) * (1 + 3**n) for n in range(9)]
print(f"iterated : {seq}")
print(f"closed   : {[round(v, 6) for v in closed]}")
print(f"agree    : {all(abs(s - c) < 1e-9 for s, c in zip(seq, closed))}")
```
</details>

**[ ] Exercise 2 — Repeated root.** Solve aₙ = 2aₙ₋₁ − aₙ₋₂ with a₀ = 1, a₁ = 2, and
show why the naive form A + B cannot fit both initial conditions.

<details>
<summary>Solution</summary>

Characteristic equation: r² − 2r + 1 = 0 = (r − 1)². A double root at r = 1.

The naive form aₙ = A + B has only one free constant, so it can fit one initial
condition, not two. The repeated root contributes a polynomial in n:

    aₙ = (A + Bn)·1ⁿ = A + Bn

A = 1 and A + B = 2, so B = 1:

    aₙ = 1 + n

Check: a₂ = 3 and the recurrence gives 2·2 − 1 = 3 ✓. a₃ = 4, and 2·3 − 2 = 4 ✓.

```python
def iterate(coeffs, initial, n):
    a = list(initial)
    while len(a) <= n:
        a.append(sum(c * a[len(a) - 1 - i] for i, c in enumerate(coeffs)))
    return a

seq = iterate([2, -1], [1, 2], 8)
print(f"iterated : {seq}")
print(f"closed   : {[1 + n for n in range(9)]}")
```
</details>

**[ ] Exercise 3 — Master theorem, three cases.** Determine the asymptotic growth
of T(n) = 3T(n/2) + n, T(n) = 3T(n/2) + n³, and T(n) = 4T(n/4) + n². Verify
each by computing the recursion tree for a small n.

<details>
<summary>Solution</summary>

1. T(n) = 3T(n/2) + n: a = 3, b = 2, d = 1. bᵈ = 2 < 3, so a > bᵈ, giving
   Θ(n^{log₂3}) = Θ(n^1.585). (Compare with quicksort's Θ(n log n) — this is why
   the two-equal-halves assumption matters.)
2. T(n) = 3T(n/2) + n³: bᵈ = 4 > 3, so a < bᵈ, giving Θ(n³). The top-level work
   dominates every level below it.
3. T(n) = 4T(n/4) + n²: bᵈ = 4² = 16 > 4, so a < bᵈ, giving Θ(n²).

```python
from math import log2

def tree(n, a, b, d):
    """Total cost of the full recursion tree for input n."""
    if n <= 1:
        return 0
    return a * tree(n // b, a, b, d) + n**d

for label, a, b, d, n in [
    ("3T(n/2)+n  ", 3, 2, 1, 32),
    ("3T(n/2)+n^3", 3, 2, 3, 32),
    ("4T(n/4)+n^2", 4, 4, 2, 64),
]:
    print(f"{label:12s} T({n:3d}) = {tree(n, a, b, d):>12,}")

from math import log2
print(f"case 1: Theta(32^log2 3) = {32 ** log2(3):9.1f}, exact T(32) = {tree(32, 3, 2, 1):,}")
print(f"case 2: Theta(32^3)      = {32**3:9,d}, exact T(32) = {tree(32, 3, 2, 3):,}")
print(f"case 3: Theta(64^2)      = {64**2:9,d}, exact T(64) = {tree(64, 4, 4, 2):,}")
```
</details>

**[ ] Exercise 4 — Count the recursion.** How many times does
`f(n) = f(n-1) + f(n-2)` with f(0) = f(1) = 1 invoke *itself* when called as f(30)?
Measure it, then repeat with a memo and explain the ratio.

<details>
<summary>Solution</summary>

Measured: 2,692,537 total invocations for f(30), of which 1,346,268 are
non-base-case calls (those are the ones that make two further calls).

The growth is F(31)-ish, i.e. Θ(φⁿ) with φ ≈ 1.618, because the call tree is
literally a Fibonacci tree: the number of leaves equals the value returned.

With a memo, each argument is computed once: 31 distinct arguments (0 through 30),
and 30 recursive calls after the two base cases. That is a factor of about
88,000 fewer calls.

```python
calls = {"total": 0, "nonbase": 0}

def f(n):
    calls["total"] += 1
    if n < 2:
        return 1
    calls["nonbase"] += 1
    return f(n - 1) + f(n - 2)

f(30)
print(f"total invocations     : {calls['total']:,}")
print(f"non-base-case calls   : {calls['nonbase']:,}")
print(f"memoised: 31 distinct arguments, 30 recursive calls")

from functools import lru_cache

@lru_cache(maxsize=None)
def g(n):
    if n < 2:
        return 1
    return g(n - 1) + g(n - 2)

g.cache_clear()
print(f"g(30) = {g(30):,}")
print(f"distinct values computed: {g.cache_info().currsize}")
print(f"speedup in calls: {calls['total'] / g.cache_info().currsize:.0f}x")
```
</details>

**[ ] Exercise 5 — Growth without a closed form.** Give a Θ bound, with
justification from the dominant root, for aₙ = 6aₙ₋₁ − 11aₙ₋₂ + 6aₙ₋₃.

<details>
<summary>Solution</summary>

Characteristic equation: r³ = 6r² − 11r + 6, i.e. r³ − 6r² + 11r − 6 = 0, which
factors as (r − 1)(r − 2)(r − 3) = 0. Roots 1, 2, 3.

The dominant root is 3, so aₙ = Θ(3ⁿ). The general solution is
aₙ = A·1ⁿ + B·2ⁿ + C·3ⁿ, and the three initial conditions determine A, B, C — but
you do not need them to know the growth rate. This is the payoff of the dominant
root theorem.

```python
from math import comb, factorial

# Roots by factoring the characteristic polynomial directly.
def roots_of(c1, c2, c3):
    # r^3 - c1 r^2 + c2 r - c3 = 0; try small integers and divide out.
    poly = [1.0, -c1, c2, -c3]
    roots = []
    for cand in range(-20, 21):
        v = 0.0
        for co in poly:
            v = v * cand + co
        if abs(v) < 1e-9:
            roots.append(cand)
            new = []
            for i in range(len(poly) - 1):
                new.append(poly[i] + cand * (new[i - 1] if i else 0))
            poly = new
    return sorted(roots)

print(f"roots of r^3 - 6r^2 + 11r - 6 : {roots_of(6, 11, 6)}")

# With A = B = C = 1 the solution is a_n = 1 + 2^n + 3^n, giving a0=3, a1=6,
# a2=14. Iterating must reproduce that, and a_n / 3^n must settle at 1.
a = [3, 6, 14]
for _ in range(3, 16):
    a.append(6 * a[-1] - 11 * a[-2] + 6 * a[-3])
closed = [1 + 2**n + 3**n for n in range(len(a))]
print(f"iterated : {a[:8]}")
print(f"closed   : {closed[:8]}")
print(f"agree    : {a == closed}")
print(f"ratios a_n/3^n approaching 1: "
      f"{[round(a[n] / 3**n, 4) for n in range(6, 14)]}")
```
</details>

**[ ] Exercise 6 — Zeckendorf.** Find the Zeckendorf representation of 1000 and
of 4, then explain in one sentence why 1000 needs no two consecutive Fibonacci
numbers.

<details>
<summary>Solution</summary>

The Fibonacci sequence here is 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377,
610, 987.

1000 = 987 + 13 = F₁₅ + F₆ (1-based, F₁ = 1). Indices 15 and 6 are not adjacent.
4 = 3 + 1 = F₃ + F₁. Indices 3 and 1 are not adjacent.

Non-adjacency is forced by the theorem, but the local reason is instructive: if
F_k + F_{k+1} were used, their sum is F_{k+2}, so two adjacent terms could always be
collapsed into one — meaning a representation using adjacent terms was never the
reduced form. Greedy never produces them, since after taking F_k the remainder is
less than F_{k+1}.

```python
FIB = [1, 2]
while FIB[-1] <= 100_000:
    FIB.append(FIB[-1] + FIB[-2])

def zeckendorf(n):
    idx = []
    for i in range(len(FIB) - 1, -1, -1):
        if FIB[i] <= n:
            n -= FIB[i]
            idx.append(i + 1)
    return idx

for v in (1000, 4):
    idx = zeckendorf(v)
    print(f"{v:5d} = {' + '.join(str(FIB[i-1]) for i in idx)}   indices {idx}, "
          f"non-adjacent: {all(abs(idx[i]-idx[i+1]) > 1 for i in range(len(idx)-1))}")
```
</details>

**[ ] Challenge 7 — Counting with a recurrence.** Derive a recurrence for aₙ, the
number of binary strings of length n containing no two consecutive 1s, and compute
a₁₀ three ways: by the recurrence, by the generating-function closed form, and by
brute force.

<details>
<summary>Solution</summary>

**Derivation.** Split the strings by their first bit. Those starting with 0 are
followed by an arbitrary valid string of length n − 1: a_{n−1} of them. Those
starting with 1 must have 0 next, and are followed by a valid string of length
n − 2: a_{n−2} of them. The cases are disjoint and exhaustive, so the sum rule
gives

    aₙ = a_{n−1} + a_{n−2},  a₀ = 1, a₁ = 2

**Closed form.** With a₀ = 1, a₁ = 2, the solution is aₙ = F(n+2), where F₁ = 1,
F₂ = 1. Equivalently, the generating function is Σ aₙxⁿ = (1 + x)/(1 − x − x²).

**Values.** a₁₀ = F₁₂ = 144, out of 2¹⁰ = 1024 strings — about 14% of all binary
strings of length 10 avoid consecutive ones.

```python
def recurrence(n):
    a = [1, 2]
    for _ in range(2, n + 1):
        a.append(a[-1] + a[-2])
    return a

def brute(n):
    return sum(1 for x in range(1 << n) if "11" not in format(x, f"0{n}b"))

a = recurrence(10)
def fib_list(count):
    """F_1, F_2, ... with F_1 = F_2 = 1, built iteratively."""
    out = [1, 1]
    while len(out) < count:
        out.append(out[-1] + out[-2])
    return out[:count]

closed = fib_list(12)[1:]        # F_2 .. F_12  equals  a[0] .. a[10]
bruted = [brute(n) for n in range(11)]
print(f"recurrence a[0..10]  : {a}")
print(f"closed form F(n+2)   : {closed}")
print(f"brute force          : {bruted}")
print(f"all three agree      : {a == closed == bruted}")
print(f"a[10] = {a[10]} out of {2**10} strings = {a[10]/2**10:.2%}")
```
</details>

## Summary

- A recurrence plus initial conditions determines a sequence; iterating it is
  always correct and is what a memo table or a bottom-up DP does.
- Substituting aₙ = rⁿ gives the characteristic equation; distinct roots give
  A·r₁ⁿ + B·r₂ⁿ + ⋯, and a repeated root multiplies by a polynomial in n.
- The largest characteristic root alone determines the growth rate: aₙ = Θ(r^n).
  You rarely need the constants.
- Verify a closed form against computed values before trusting it; the table is
  always right.
- The master theorem handles T(n) = a·T(n/b) + Θ(nᵈ) with a ≥ 1; it does not apply
  to f(n) = n log n or to a = 0.
- Memoising a recurrence changes exponential time to linear: f(30) makes 1.3
  million calls naive, 30 with a cache.
- Matrix exponentiation and fast doubling compute F(n) in O(log n), and the same
  trick handles matrix powers, Catalan numbers, and Stirling numbers.
- Zeckendorf's theorem gives every positive integer a unique sum of
  non-consecutive Fibonacci numbers — a real, efficient numeral system.

## Next

[Lesson 25 — Relations and Equivalence Classes](../part02_discrete_combinatorics/25_relations_and_equivalence_classes.md)
assumes you can count subsets and follow a recurrence; it covers the structural
notion that makes union–find, database grouping, and type coercion all the same
idea.