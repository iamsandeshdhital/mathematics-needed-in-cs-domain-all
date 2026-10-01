# 22 — The Binomial Theorem

**Part**: part02_discrete_combinatorics · **Prerequisites**: 21 · **Time**: 30 min

---

## In Plain Words

Take a sum like (2 + 3) and raise it to a power, say ten times. If you multiply
it out by hand you would do 2¹⁰ + 2⁹·3 + 2⁸·3² + ... + 3¹⁰ — eleven enormous
terms that you then have to add up. The binomial theorem says you never have to
expand it. You only need the row of numbers

    1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1

and then multiply each of those by a term of the expansion. The row of numbers
is the same row no matter what you are expanding, and it is the same row no
matter how large the power is.

That row is the row of *counts*: how many ways to pick 0 things from 10, how many
ways to pick 1, how many ways to pick 2, and so on. The coefficients in an
expansion are not mysterious — they are answers to counting questions. This is
why the theorem matters in computer science rather than merely being algebra you
memorised. Once a coefficient is understood as a count, the theorem becomes a
computational tool: it evaluates weighted sums over "choose k" without touching
each term, which is the trick behind fast moment calculations in probability and
behind the fast subset-sums used in hashing and error correction.

There is a second, sneakier payoff. Every n-bit pattern is a subset of n bit
positions, and "the subsets of size k" is counted by the k-th number in the row.
That single observation explains why counting bits set in a word, counting masks
with a fixed number of bits set, and counting ways to split a payload between two
machines are all the same problem. By the end of this lesson you will see
`bin(x).count("1")` as a counting routine wearing a disguise.

## Why Computer Science Cares

- **Bit counting and popcount.** The k-th coefficient of (1 + x)ⁿ is the number
  of n-bit words with exactly k bits set. Computing a Hamming weight, and the
  distribution of Hamming weights across all codewords, is binomial
  mathematics. Every code's weight enumerator in coding theory is built from
  this lesson.
- **Subset sums without a loop.** Σ C(n, k) = 2ⁿ evaluates the sum of a whole row
  in one step. Σ k·C(n, k) = n·2ⁿ⁻¹ and Σ k²·C(n, k) = n(n+1)·2ⁿ⁻² evaluate
  weighted rows in one step each. These appear in birthday-paradox second
  moments and in variance calculations for sampling.
- **Thue–Morse as a hash.** The parity of the popcount of n, taken for n = 0, 1, 2,
  ..., defines the Thue–Morse sequence. It is a real hash function used for
  scatter tables, for recursive-subdivision load balancing, and as a
  pathological input generator for testers — it looks random and is not.
- **Distinct subsequences.** The number of distinct subsequences of a binary
  string has a closed form built from products of binomial coefficients — a
  standard exercise in dynamic programming interviews.
- **Secret sharing and Reed–Solomon.** Shamir's scheme relies on "a polynomial of
  degree t − 1 has at most t − 1 roots", and Reed–Solomon corrects
  ⌊(d−1)/2⌋ errors because of how error-locator polynomials combine. Both are
  stated and used in [Lessons 111](../part09_number_theory_crypto/111_modular_arithmetic_and_crypto.md)
  and [113](../part09_number_theory_crypto/113_error_correcting_codes.md).
- **Choosing a hyperparameter.** "Try all 70 subsets of size 4 out of 8" is a
  binomial coefficient, not a guess. The count decides feasibility before you
  write the loop.

## The Formal Version

**Definition.** The **binomial coefficient** C(n, k) for integers 0 ≤ k ≤ n is

    C(n, k) = n! / (k! (n − k)!)

It is also written C(n, k) = C(n, n − k) and appears in the triangle of Pascal.

**Theorem (Binomial theorem).** For any numbers a, b and any non-negative
integer n,

    (a + b)ⁿ = Σ_{k=0}^{n} C(n, k) a^{n−k} b^k

**Explanation.** Expand the product of n copies of (a + b). Each of the 2ⁿ terms in
the raw expansion is produced by choosing a or b independently in each of the n
positions, so there are 2ⁿ terms with multiplicity. Group equal terms: a term
with b chosen in exactly k positions and a in the other n − k positions. To count
how many expansions give that term, choose which k of the n positions hold b —
C(n, k) ways. Each group contributes C(n, k) · a^{n−k} b^k. Summing over all k
gives the formula.

**Theorem (Pascal's recursion).** C(n, k) = C(n − 1, k − 1) + C(n − 1, k), with
base cases C(n, 0) = C(n, n) = 1 and C(n, k) = 0 for k > n.

**Explanation.** Partition the k-element subsets of an n-set by whether they
contain a specific element. This is the same case split as in Lesson
[21](../part02_discrete_combinatorics/21_permutations_and_combinations.md), which is why the two lessons share a
recurrence: both describe the same subsets.

**Theorem (Specialisations).** For any n ≥ 0:

    Σ_k C(n, k)          = 2ⁿ          (set a = b = 1)
    Σ_k (−1)ᵏ C(n, k)    = 0  for n > 0  (set a = 1, b = −1)
    Σ_k C(n, k) a^{n−k}  = (a + 1)ⁿ  (set b = 1)

**Explanation.** These are not separate results. They are the binomial theorem
with different values plugged in, which is exactly the point: choosing a, b is
choosing what combinatorial question to ask.

**Theorem (Weighted sums).** For n ≥ 1,

    Σ_k k·C(n, k)        = n · 2ⁿ⁻¹
    Σ_k k(k − 1)·C(n, k) = n(n − 1)·2ⁿ⁻²
    Σ_k k²·C(n, k)       = n(n + 1)·2ⁿ⁻²

**Explanation.** Note k² = k(k − 1) + k, so the third identity follows from the
first two. To derive them, multiply the binomial theorem by x and substitute
x = 1: x(a + b)ⁿ with b = x and a = 1 gives Σ k C(n,k) xᵏ = n x (1 + x)ⁿ⁻¹,
and setting x = 1 yields n·2ⁿ⁻¹. Differentiate twice for the falling-factorial
identity. This is the standard "differentiate then substitute" trick, and it is
worth memorising because it converts any weighted binomial sum into a closed form.

**Theorem (Vandermonde's identity).** For non-negative m, n, r,

    Σ_k C(m, k)·C(n, r − k) = C(m + n, r)

**Explanation.** Count r-subsets of a disjoint union of an m-set and an n-set in
two ways. Directly: C(m + n, r). By how many elements the subset takes from the
first part: choose k from the m-set and r − k from the n-set, then sum over k. This
is the template behind the coefficient-matching technique used throughout this
part.

**Theorem (Generating-function form).** If f(x) = Σ_k f_k xᵏ and g(x) = Σ_k g_k xᵏ
are polynomials given by their coefficient lists, then the coefficient of xᵏ in
f(x)g(x) is

    Σ_{i + j = k} f_i · g_j

**Explanation.** Multiply out and collect: an x term from the first factor times an
x term from the second gives one contribution to the total degree. This is the
workhorse for the "choosing with limits" technique from Lesson
[21](../part02_discrete_combinatorics/21_permutations_and_combinations.md) and for counting strings that avoid a
local pattern.

## Worked Example

**The question.** A trading system sends 8-bit messages over a channel where each
bit flips independently with probability 0.1. It adds no error correction. How many
messages arrive with **exactly one** corrupted bit, out of 256 possible messages?

**Step 1 — Identify the coefficient.** An 8-bit message has 8 bit positions. A
message with exactly one corrupted bit is determined by a choice of 8. So the
count is C(8, 1) = 8, which is the second number in row 8 of Pascal's triangle:

    row 8:  1,  8, 28, 56, 70, 56, 28,  8,  1

**Step 2 — Get the whole distribution from the theorem, not from reasoning.** The
count of messages with exactly k corrupted bits is C(8, k). Reading across the row
gives the distribution directly. We did not derive 28 or 70 — we *looked them up*
from the structure the theorem guarantees. That is the win: one row of nine
numbers replaced eight separate arguments.

**Step 3 — The binomial theorem, applied.** If you write (0.9 + 0.1)⁸ and expand
it, the coefficient of (0.9)⁷(0.1) is C(8, 1) = 8, and the coefficient of
(0.9)⁸ is C(8, 0) = 1. The whole probability distribution is

    P(k errors) = C(8, k) · 0.1ᵏ · 0.9^(8−k)

so the theorem hands you the multiplier *and* explains where it comes from. This
is the standard binomial-distribution derivation, and
[Lesson 66](../part05_probability_statistics/66_common_distributions.md) turns it
into a probability model.

**Step 4 — Compute without a loop, using weighted sums.** Sometimes the question
asks for something like "the expected number of errors" or "the variance", and
those are weighted sums over the row. By the weighted-sums theorem:

    E[errors] = Σ k C(8, k) 0.1ᵏ 0.9^(8−k) = 8 · 0.1 · (0.9 + 0.1)⁷ = 0.8

The n · 2ⁿ⁻¹ identity, translated to probabilities, becomes n · p · (1)⁷ — which
is just "8 bits, each wrong with probability 0.1". The algebra and the intuition
agree, which is the point: the closed form is not a trick, it is the intuition
written down.

**Step 5 — Sanity-check by summing.** The probabilities must total 1. By the
specialisation with a = 0.9, b = 0.1, the sum of the whole expansion is
(0.9 + 0.1)⁸ = 1⁸ = 1. If your computed distribution does not sum to 1, you have a
bug, and this check costs one line.

## Runnable Code

Build row *n* of Pascal's triangle, then use the theorem to evaluate a large
expansion without expanding it.

```python
from math import comb, factorial

def pascal_row(n):
    """Row n of Pascal's triangle: row[n][k] == C(n, k).

    Built by C(n, k) = C(n-1, k-1) + C(n-1, k), so no factorials are involved."""
    row = [1]
    for _ in range(n):
        row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]
    return row

def binomial_expansion(a, b, n):
    """The list of terms of (a + b)^n, without multiplying anything out."""
    return [comb(n, k) * a ** (n - k) * b**k for k in range(n + 1)]

row8 = pascal_row(8)
print(f"row 8 of Pascal's triangle: {row8}")
print(f"C(8, 1) via the theorem    : {comb(8, 1)}  (coefficient of x^1 in (1+x)^8)")
print(f"C(10, 5)                   : {comb(10, 5)}")
print(f"C(10, 5) via 10!/(5!5!)    : {factorial(10)//(factorial(5)*factorial(5))}")

# The theorem evaluates the sum directly.
terms = binomial_expansion(2, 3, 10)
print(f"(2+3)^10 by theorem  = {sum(terms):,}")
print(f"(2+3)^10 by repeated squaring = {5**10:,}")
print(f"terms in the expansion: {len(terms)}  largest: {max(terms):,}")
```

Now the specialisations, each checked by brute force. These are one-line
shortcuts for sums you would otherwise loop over.

```python
from math import comb

n = 8
row = [comb(n, k) for k in range(n + 1)]

print(f"sum C(8,k)   = {sum(row)} = 2^8 = {2**n}")
print(f"alt sum      = {sum((1 if k % 2 == 0 else -1) * c for k, c in enumerate(row))} (0 for n>0)")
print(f"sum k*C(8,k) = {sum(k * c for k, c in enumerate(row))} = n*2^(n-1) = {n * 2**(n-1)}")
print(f"sum k^2*C    = {sum(k * k * c for k, c in enumerate(row))} = n(n+1)2^(n-2) = {n*(n+1)*2**(n-2)}")
print(f"sum k(k-1)C  = {sum(k*(k-1)*c for k, c in enumerate(row))} = n(n-1)2^(n-2) = {n*(n-1)*2**(n-2)}")

# The counting interpretation: n-bit strings with exactly k bits set.
from itertools import product as iproduct

strings = list(iproduct((0, 1), repeat=n))
for k in range(n + 1):
    brute = sum(1 for s in strings if sum(s) == k)
    assert brute == comb(n, k), (k, brute, comb(n, k))
print(f"checked all k = 0..{n}: C(n,k) equals the brute-force count")

# Strings over a 3-letter alphabet, grouped by how many 0s they use:
# sum over k of C(n,k) * 2^k must equal 3^n.
grouped = sum(comb(n, k) * 2**k for k in range(n + 1))
print(f"sum C(4,k)*2^k = {grouped} = 3^4 = {3**n}")
```

Vandermonde and the hockey-stick identity, both proved by counting and both
verified numerically.

```python
from math import comb

# Vandermonde: choose r from a union of an m-set and an n-set.
m, n, r = 4, 6, 3
lhs = sum(comb(m, k) * comb(n, r - k) for k in range(0, min(m, r) + 1))
print(f"Vandermonde: sum_k C({m},k)C({n},{r}-k) = {lhs} = C({m+n},{r}) = {comb(m+n, r)}")

# Hockey stick: C(j, 2) summed over j is a binomial coefficient.
total = sum(comb(j, 2) for j in range(2, 6))
print(f"hockey stick: sum_j=2..5 C(j,2) = {total} = C(6,3) = {comb(6, 3)}")
```

Popcount: the coefficient of xᵏ is the number of *k*-bit-set words, and three
ways of counting the same bits.

```python
def popcount_naive(x):
    return bin(x).count("1")

def popcount_kernighan(x):
    """Clear the lowest set bit repeatedly; the loop runs once per set bit."""
    c = 0
    while x:
        x &= x - 1  # n & (n-1) removes the lowest set bit
        c += 1
    return c

assert all(popcount_kernighan(v) == popcount_naive(v) == v.bit_count() for v in range(4096))
print("all three popcount implementations agree on 0..4095")
print(f"popcount(0b1011011) = {popcount_naive(0b1011011)} "
      f"(Kernighan took {popcount_kernighan(0b1011011)} iterations)")

# Total population count over all n-bit words is n * 2^(n-1):
# each of the n positions is set in exactly half the words.
for n in (4, 8, 12):
    brute = sum(popcount_naive(x) for x in range(1 << n))
    print(f"n={n:2d}: total popcount = {brute:6d} = n*2^(n-1) = {n * 2**(n-1):6d}")

# Parity of popcount is the Thue-Morse sequence.
tm = [v.bit_count() % 2 for v in range(16)]
print(f"Thue-Morse (popcount parity), n = 0..15: {tm}")
```

Coefficient extraction: counting binary strings that avoid a local pattern. Two
methods — a two-state DP, and the closed-form generating function — checked against
brute force.

```python
def avoid_consecutive_ones(n):
    """Number of n-bit strings containing no adjacent 1s.

    Two states: how many valid strings so far end in 0, and how many end in 1.
    Appending a 0 is allowed after either; appending a 1 only after a 0. So the
    update is new_end0 = end0 + end1 and new_end1 = end0."""
    end0, end1 = 1, 0  # the empty string ends in neither, so start with one way
    for _ in range(n):
        end0, end1 = end0 + end1, end0
    return end0 + end1

def brute(n):
    return sum(1 for x in range(1 << n) if "11" not in format(x, f"0{n}b"))

def generating_function(N):
    """Coefficients of Q(x) = (1 + x) / (1 - x - x^2), i.e. of sum_n P(n) x^n.

    Solving (1 - x - x^2) Q(x) = 1 + x coefficient by coefficient gives
    q_0 = 1, q_1 - q_0 = 1 so q_1 = 2, and q_n = q_{n-1} + q_{n-2} for n >= 2.
    Those coefficients are the Fibonacci numbers F(n+2)."""
    q = [0] * (N + 1)
    q[0] = 1
    q[1] = 2
    for n in range(2, N + 1):
        q[n] = q[n - 1] + q[n - 2]
    return q

N = 12
q = generating_function(N)
print("n : two-state DP : generating function : brute force")
for n in range(1, N + 1):
    print(f"{n:2d} : {avoid_consecutive_ones(n):13d} : {q[n]:20d} : {brute(n):12d}")
print(f"coefficients are Fibonacci: {q[1:9] == [2, 3, 5, 8, 13, 21, 34, 55]}")
print(f"fraction of 12-bit strings with no adjacent 1s: {q[12]}/4096 "
      f"= {q[12] / 4096:.4f}")
```

Finally, binomial coefficients modulo a prime — the technique behind fast
coefficients in checksums and Reed–Solomon codes.

```python
from math import comb

def lucas(n, k, p):
    """C(n, k) mod p for prime p, in O(log_p n) steps.

    Write n and k in base p. Then C(n,k) = product of C(n_i, k_i) mod p, where
    n_i, k_i are the base-p digits -- each a single-digit binomial coefficient."""
    result = 1
    nn, kk = n, k
    while nn or kk:
        ni, ki = nn % p, kk % p
        if ki > ni:
            return 0  # a digit exceeds its counterpart: the coefficient is 0 mod p
        result = result * comb(ni, ki) % p
        nn //= p
        kk //= p
    return result

for n, k, p in ((50, 20, 13), (1000, 437, 101), (100, 30, 7), (64, 17, 7)):
    fast = lucas(n, k, p)
    exact = comb(n, k) % p
    print(f"C({n},{k}) mod {p}: Lucas {fast}, exact {exact}, agree {fast == exact}")
```

## Common Mistakes

**1. Treating the coefficients as algebraic accidents.**

> Wrong: "The binomial theorem is a formula I memorise: (a+b)ⁿ expands with
> C(n,0), C(n,1), ... in the coefficients."
> Right: The k-th coefficient is the number of ways to choose k items. Once you
> know that, you can *look up* any coefficient rather than derive each expansion.
> Why the wrong one is tempting: it is presented as algebra, and algebra invites
> memorisation. The counting reading is what makes it reusable for bit patterns,
> error models, and subset counts.

**2. Reversing a and b and getting the wrong term.**

> Wrong: "In (a+b)ⁿ the coefficient of aᵏbⁿ⁻ᵏ is C(n, k)."
> Right: In (a + b)ⁿ = Σ C(n,k) a^(n−k) bᵏ, the coefficient of a^(n−k)bᵏ is
> C(n, k). By the symmetry C(n,k) = C(n, n−k) the *set* of coefficients is
> palindromic, so a symmetric list hides a reversed indexing bug until n is odd —
> where you will be off by a position.
> Why the wrong one is tempting: the row is symmetric, so it looks as if the
> order cannot matter. It cannot, for the total sum — but it does for which
> specific power of x you are extracting.

**3. Adding the weighted-sum identities incorrectly.**

> Wrong: "Σ k² C(n, k) = n·2ⁿ⁻¹, same as the mean case."
> Right: k² = k(k − 1) + k, so Σ k²C(n,k) = n(n − 1)2ⁿ⁻² + n2ⁿ⁻¹ =
> n(n + 1)2ⁿ⁻². For n = 8 that is 4,608, not 1,024.
> Why the wrong one is tempting: the two identities look similar, and it is easy
> to carry over the n2ⁿ⁻¹ pattern. Write the falling-factorial identity
> explicitly before converting it.

**4. Dividing instead of multiplying when factoring.**

> Wrong: "To get Σ C(n,k)a^(n−k)bᵏ I should multiply the terms."
> Right: For fixed a and b the sum *is* (a + b)ⁿ — there is nothing to multiply;
> the multiplication happened inside each term and the sum rule collapses the
> whole row. Confusing which operation the theorem performs is the sign that you
> are treating it as algebra instead of counting.
> Why the wrong one is tempting: the *expansion* is a multiplication of n copies
> of a sum, so "multiply" is the right word for the derivation — just not for the
> evaluation step.

**5. Computing a giant coefficient exactly when you only need it modulo p.**

> Wrong: `comb(10**6, 5 * 10**5) % 998244353` — build a number with 10⁶ bits, then
> reduce it.
> Right: Use Lucas' theorem (above), which touches only the base-p digits, or
> compute the product of ratios mod p with modular inverses. Work is O(log_p n)
> instead of O(k).
> Why the wrong one is tempting: `math.comb` is fast enough on small inputs that
> you never learn where the wall is. The wall is real: checkums and
> Reed–Solomon codecs evaluate C(n, k) mod p routinely with n in the thousands.

---

## Exercises and Solutions

**[ ] Exercise 1 — Row lookup.** Without computing any factorials, find C(20, 7),
C(20, 13), and C(20, 0), and explain why the first two are equal.

<details>
<summary>Solution</summary>

C(20, 7) = 77,520. C(20, 13) = 77,520 — equal because C(n,k) = C(n, n−k), the
complement bijection. C(20, 0) = 1 — there is exactly one empty selection.

Built by Pascal's recursion, no factorials involved:

```python
def pascal_row(n):
    row = [1]
    for _ in range(n):
        row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]
    return row

r = pascal_row(20)
print(r[7], r[13], r[0])
from math import comb
print(comb(20, 7) == comb(20, 13) == 77520, comb(20, 7))
```
</details>

**[ ] Exercise 2 — Counting k-subsets.** A 20-element set has C(20, 12) =
125,970 twelve-element subsets. Show, using only Pascal's recursion and no
factorials, that the number of those subsets containing a particular fixed element
is 75,582, and how many contain none of three particular elements.

<details>
<summary>Solution</summary>

**Subsets containing a fixed element.** Partition the 12-subsets of the 20-set by
whether they contain element 1:

    C(20, 12) = C(19, 12) + C(19, 11)

Those that contain element 1 are in bijection with the 11-subsets of the
remaining 19 elements — delete 1 from one, adjoin 1 to the other — so the count is
C(19, 11) = 75,582. Recursing down by symmetry, C(19, 11) = C(19, 8), and by the
symmetry rule once more you can read the value off the diagonal where n = 8.

**Subsets containing none of three fixed elements.** Delete all three, leaving a
17-element set, and the count is C(17, 12) = C(17, 5) = 6,188.

Both numbers are consistent with the total: the subsets containing at least one of
the three number 125,970 − 6,188 = 119,782.

Pascal's recursion is what makes this computable without factorials, but note
that it always yields a *sum*, never a single coefficient — collapsing a column
of the triangle is a separate step, and the only mechanical way to do it is to
build the rows.

```python
from math import comb

def pascal_row(n):
    row = [1]
    for _ in range(n):
        row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]
    return row

r = pascal_row(19)
print(f"C(19,11) = {r[11]:,}   C(19,8) = {r[8]:,}   (symmetric: {r[11] == r[8]})")
print(f"C(17,12) = C(17,5) = {comb(17, 5):,}")
print(f"total C(20,12) = {comb(20, 12):,}, at least one of three = "
      f"{comb(20, 12) - comb(17, 5):,}")
```
</details>

**[ ] Exercise 3 — Direct expansion.** Expand (1 + x)⁵ by hand, then check your
coefficients against row 5 of Pascal's triangle and against `math.comb`.

<details>
<summary>Solution</summary>

(1 + x)⁵ = 1 + 5x + 10x² + 10x³ + 5x⁴ + x⁵.

Row 5 is [1, 5, 10, 10, 5, 1], matching term by term. Note the symmetry: the
coefficients for xᵏ and x⁵⁻ᵏ are equal, because C(5,k) = C(5, 5−k).

```python
from math import comb
coeffs = [comb(5, k) for k in range(6)]
print("1 +", " + ".join(f"{c}x^{k}" for k, c in enumerate(coeffs[1:], 1)))
print(coeffs)
```
</details>

**[ ] Exercise 4 — Weighted sums without a loop.** Compute Σ k·C(10, k) and
Σ k²·C(10, k) by brute force, then confirm both against the closed forms.

<details>
<summary>Solution</summary>

Brute force: Σ k·C(10,k) = 5,120 and Σ k²·C(10,k) = 28,160.

Closed forms: n·2ⁿ⁻¹ = 10 · 512 = 5,120, and n(n+1)·2ⁿ⁻² = 10 · 11 · 256 =
28,160. Both agree.

```python
from math import comb
n = 10
row = [comb(n, k) for k in range(n + 1)]
b1 = sum(k * c for k, c in enumerate(row))
b2 = sum(k * k * c for k, c in enumerate(row))
print(b1, n * 2**(n - 1), b2, n * (n + 1) * 2**(n - 2))
```
</details>

**[ ] Exercise 5 — Vandermonde by brute force.** Verify Σ_k C(4,k)·C(6,3−k) =
C(10, 3) = 120, and then find a combinatorial reason the sum should be 120
independent of the split 4 + 6.

<details>
<summary>Solution</summary>

Numerically: k = 0: 1·20 = 20; k = 1: 4·15 = 60; k = 2: 6·6 = 36; k = 3: 4·1 = 4.
Sum = 120 ✓.

The reason: the left side counts 3-element subsets of a set that is the disjoint
union of a 4-element part and a 6-element part, grouped by how many elements they
take from the first part. The right side counts the same 3-element subsets
directly. The split is irrelevant because it is the same set being counted; that
is what an identity *is*.

```python
from math import comb
parts = [comb(4, k) * comb(6, 3 - k) for k in range(4)]
print(parts, sum(parts), comb(10, 3))
```
</details>

**[ ] Exercise 6 — Binomial error model.** A 4-bit message crosses a channel that
flips each bit with probability 0.1. Use the binomial theorem to compute the
probability of exactly two errors, and check that the full distribution sums to 1.

<details>
<summary>Solution</summary>

P(k errors) = C(4, k) · 0.1ᵏ · 0.9^(4−k).

- k = 0: 0.6561
- k = 1: 0.2916
- k = 2: 0.0486
- k = 3: 0.0036
- k = 4: 0.0001

Sum = 1.0000, which is (0.9 + 0.1)⁴ = 1 by the binomial theorem.

```python
from math import comb
p = 0.1
dist = [comb(4, k) * p**k * (1 - p) ** (4 - k) for k in range(5)]
for k, pr in enumerate(dist):
    print(f"  P({k} errors) = {pr:.4f}")
print(f"  sum = {sum(dist):.4f}  ((0.9+0.1)^4 = {(0.9+0.1)**4:.4f})")
```
</details>

**[ ] Exercise 7 — Coefficient extraction with a constraint.** A password must
be exactly 8 characters long and contain **exactly two** digits (from 10) and six
letters (from 6). Use coefficient extraction on (1 + x)⁸ to confirm the count
equals C(8, 2) · 10² · 6⁶, and then verify that number by brute force.

<details>
<summary>Solution</summary>

Position factor: each of the 8 positions either holds a digit or does not, so the
polynomial is (1 + x)⁸ and the coefficient of x² is C(8, 2) = 28. That coefficient
counts *which two positions* hold digits — it is exactly the binomial-coefficient-as-
count idea.

Then the two digit slots fill in 10 ways each and the six letter slots in 6 ways
each, independently, giving

    C(8, 2) · 10² · 6⁶ = 28 · 100 · 46,656 = 130,636,800

Enumerating all of them directly is hopeless — 130,636,800 strings, each built
one at a time, would take hours. But the *count* can be checked by summing over
the position choice, which is exactly the binomial-coefficient idea:

```python
from itertools import combinations
from math import comb

total = comb(8, 2) * 10**2 * 6**6

# Sum the per-position-pair counts instead of materialising the strings.
# For a fixed pair of digit positions the slots fill in 10 * 10 * 6**6 ways.
fillings = 10 * 10 * 6**6
brute = sum(fillings for _ in combinations(range(8), 2))

print(f"closed form = {total:,}")
print(f"summed over position pairs = {brute:,}")
print(f"agree: {total == brute}")
print()
print(f"There are {total:,} strings, so enumerating every one to count them")
print(f"would take on the order of {total:,} steps. The closed form replaces")
print("that with a single multiplication.")
```

And the formula generalises: for *k* digits among *n* slots the count is
`comb(n, k) * 10**k * 6**(n-k)`, a weighted binomial coefficient.
</details>

**[ ] Challenge 8 — Vandermonde for weighted counts.** A message is 12 bytes.
Each byte is either compressed (weight 0.7) or stored raw (weight 1.0). Show
that the total weight of all 4096 compressed-or-not variants of a message is

    (0.7 + 1.0)¹² = 1.7¹² ≈ 582.6

and then verify it by brute force. Explain in one sentence why the number of
variants does not appear in the answer.

<details>
<summary>Solution</summary>

By the binomial theorem, Σ_k C(12, k) · 0.7ᵏ · 1^(12−k) = (0.7 + 1.0)¹². Brute
force over all 4096 variants gives the same total.

The count does not appear because the coefficients C(12, k) *are* the counts of
variants with exactly k compressed bytes. The 4096 is already inside the
expansion as Σ_k C(12, k) = 2¹²; multiplying by a per-variant weight and summing
collapses to evaluating at the sum of the two weights.

```python
from itertools import product as iproduct
from math import comb

brute = sum(0.7 ** bin(v).count("1") for v in range(1 << 12))
print(f"brute force      = {brute:.4f}")
print(f"(0.7 + 1.0)^12  = {1.7**12:.4f}")
print(f"also: 2^12 variants, average weight = {brute / 2**12:.4f}")
```
</details>

## Summary

- (a + b)ⁿ = Σ C(n,k) a^(n−k) bᵏ, and C(n,k) is the number of ways to choose k
  positions — the coefficients are counts, not algebraic accidents.
- Specialising gives the shortcuts: Σ C(n,k) = 2ⁿ and the alternating sum is 0 for
  n > 0.
- Differentiate-then-substitute gives weighted sums: Σ k·C(n,k) = n·2ⁿ⁻¹ and
  Σ k²·C(n,k) = n(n+1)·2ⁿ⁻².
- Vandermonde, Σ C(m,k)C(n,r−k) = C(m+n,r), is proved by counting r-subsets of a
  disjoint union and grouping by how many come from each part.
- Coefficient of xᵏ in (1+x)ⁿ is the number of n-bit words with exactly k bits
  set — which is why popcount distributions are binomial.
- The parity of popcount is the Thue–Morse sequence, a genuine hash function used
  in practice.
- Binomial coefficients modulo a prime are computed with Lucas' theorem in
  O(log_p n) steps instead of building an enormous integer.

## Next

[Lesson 23 — Inclusion–Exclusion and the Pigeonhole Principle](../part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md)
assumes you can count subsets with confidence; it handles the case the sum rule
*cannot* handle — overlapping cases — and the theorem that turns "at least one"
into arithmetic you can rely on.