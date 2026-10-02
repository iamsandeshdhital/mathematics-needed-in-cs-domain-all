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

## Formula Sheet

Every symbol and formula this lesson introduces. `n, k` are integers with
`0 ≤ k ≤ n`, `a, b` are any numbers, `x` is the polynomial variable, and `p` is a
prime. `k!` means `1 · 2 · … · k`, with `0! = 1`.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| Binomial coefficient | `$C(n,k) = n!/\bigl(k!\,(n-k)!\bigr)$` | the number of `k`-element subsets of an `n`-element set | valid only for `0 ≤ k ≤ n`; define `C(n,k) = 0` for `k > n` |
| Symmetry | `$C(n,k) = C(n,n-k)$` | complement inside the `n`-set | `C(20,7) = C(20,13) = 77,520`; halves the work of building a row |
| Binomial theorem | `$(a+b)^{n} = \sum_{k=0}^{n} C(n,k)\,a^{\,n-k}b^{k}$` | expand the `n`-fold product without multiplying it out | the coefficient of `$a^{n-k}b^k$` is `$C(n,k)$` |
| Pascal's recursion | `$C(n,k) = C(n-1,k-1) + C(n-1,k)$` | split `k`-subsets by whether they contain one fixed element | the dynamic-programming route to a row; no factorials |
| Pascal base cases | `$C(n,0) = C(n,n) = 1$; `$C(n,k) = 0$` for `$k > n$` | the empty and whole selections are unique | valid for all `n ≥ 0`; keeps the recursion terminating |
| Row sum | `$\sum_{k=0}^{n} C(n,k) = 2^{n}$` | the whole row adds to the power-set count | substitute `a = b = 1`; `Σ_k C(8,k) = 256` |
| Alternating row sum | `$\sum_{k=0}^{n} (-1)^{k} C(n,k) = 0$` | even and odd terms cancel exactly | substitute `a = 1, b = −1`; **valid only for `n ≥ 1`** — for `n = 0` the sum is 1 |
| Partial binomial sum | `$\sum_{k=0}^{n} C(n,k)\,a^{\,n-k} = (a+1)^{n}$` | set `b = 1` in the theorem | "at least one of a kind" counts by complement |
| First moment | `$\sum_{k=0}^{n} k\,C(n,k) = n\cdot 2^{\,n-1}$` | the weighted row in one step | **valid only for `n ≥ 1`**; `Σ_k k C(8,k) = 1,024` |
| Falling factorial | `$\sum_{k=0}^{n} k(k-1)\,C(n,k) = n(n-1)\cdot 2^{\,n-2}$` | differentiate twice, then substitute | **valid only for `n ≥ 2`**; for `n = 8` it is 3,584 |
| Second moment | `$\sum_{k=0}^{n} k^{2}C(n,k) = n(n+1)\cdot 2^{\,n-2}$` | use `$k^2 = k(k-1) + k$` on the two above | **valid only for `n ≥ 2`**; for `n = 8` it is 4,608 |
| Vandermonde's identity | `$\sum_{k} C(m,k)\,C(n,r-k) = C(m+n,r)$` | choose `r` items from a union of an `m`-set and an `n`-set, two ways | the template for coefficient matching; `m=4, n=6, r=3` gives 120 |
| Hockey-stick identity | `$\sum_{j=r}^{N} C(j,r) = C(N+1,\,r+1)$` | sum a diagonal of Pascal's triangle | `Σ_{j=2..5} C(j,2) = 20 = C(6,3)` |
| Coefficient of a product | `$[x^{k}]\,f(x)g(x) = \sum_{i+j=k} f_i\,g_j$` | multiply out, group by total degree | the workhorse for "choosing with limits" and pattern-avoidance counts |
| Binomial (error) distribution | `$P(k) = C(n,k)\,p^{k}(1-p)^{\,n-k}$` | `k` successes out of `n` independent trials | the theorem *is* the binomial law: `C(8,k)·0.1ᵏ·0.9^(8−k)` |
| Expectation of that law | `$E[K] = np$` | `n` trials each succeeding with probability `p` | `8 · 0.1 = 0.8` for the worked example |
| Total Hamming weight | `$\sum_{x=0}^{2^{n}-1} \mathrm{popcount}(x) = n\cdot 2^{\,n-1}$` | each of the `n` bit positions is set in exactly half the words | `n = 8` gives 1,024; the `n·2^(n−1)` identity read as a count |
| Thue–Morse | `$t(x) = \mathrm{popcount}(x) \bmod 2$` | parity of the number of 1 bits | a hash that looks random and is not: `t(0..15) = 0,1,1,0,1,0,0,1,…` |
| Strings with no adjacent 1s | `$q_n = q_{n-1} + q_{n-2}$, `$q_0 = 1$, `$q_1 = 2$` | split on the last bit: a `0`, or a `01` | `$q_n = F(n+2)$`, so `q₁₂ = 377` of the 4,096 twelve-bit words |
| Generating function for those strings | `$Q(x) = (1+x)/(1 - x - x^{2})$` | the denominator is the recurrence, read as a polynomial | `[x^n] Q(x) = F(n+2)`; the algebraic form of the DP |
| Lucas' theorem | `$C(n,k) \bmod p = \prod_i C(n_i, k_i) \bmod p$` | with `n = Σ n_i p^i`, `k = Σ k_i p^i` the base-`p` digits | `p` prime; `O(log_p n)` instead of `O(k)` |
| Lucas zero condition | `$\exists i$ with `$k_i > n_i$$ | if a digit of `k` exceeds the matching digit of `n`, the whole coefficient is `0 mod p` | `C(100,30) mod 7 = 0` because `30 = (42)_7`, `100 = (202)_7`, and `4 > 0` |
| Expansion of a power | `$\sum_k C(n,k)\,a^{\,n-k}b^{k}$` with `(a+b)^n` known in closed form | evaluate an expansion instead of expanding it | `(2+3)^10 = 9,765,625` without 2¹⁰ = 1,024 terms |

---

## Multiple Choice Questions

**Q1.** In `(a + b)ⁿ = Σ_{k=0}^{n} C(n, k) · aⁿ⁻ᵏ · bᵏ`, what is the coefficient of
the monomial `aᵏ · bⁿ⁻ᵏ`?

- A) `C(n, k)`
- B) `C(n, n − k)`
- C) `C(n, n − k)` — but only when `n` is even
- D) `n!`

<details>
<summary>Answer and explanation</summary>

**B) `C(n, n − k)`.**

Read the index off the theorem: the general term is `C(n,k) · a^(n−k) · b^k`, so
a term has exponent `n − k` on `a` exactly when `k` is the exponent on `b`. The
coefficient of `aᵏbⁿ⁻ᵏ` therefore carries `k` as the exponent of `b` in the
*other* reading, giving `C(n, n − k)`.

- A) is Mistake 2 of this lesson. `C(n,k)` and `C(n,n−k)` are equal by the
  symmetry, so this looks harmless — but the *symmetric list hides a reversed
  indexing bug*, and the error surfaces when you extract a specific power of `x`
  and the row has odd length, where there is no centre to absorb it.
- C) is a distractor with no content: the symmetry holds for every `n`, not just
  even ones. It is one extra word of wrongness attached to a correct formula.
- D) is the numerator of the factorial form. It is never the coefficient on its
  own; `C(n,k)` is `n!` divided by `k!(n−k)!`.

</details>

**Q2.** In the worked example, an 8-bit message arrives with corrupted bits.
Out of the 256 possible messages, how many arrive with **exactly three** corrupted
bits?

- A) 8
- B) 56
- C) 28
- D) 256

<details>
<summary>Answer and explanation</summary>

**B) 56.**

An 8-bit message with exactly three corrupted bits is determined by choosing
which 3 of the 8 bit positions flipped: `C(8,3) = 56`, the fourth number in row 8
of Pascal's triangle, `1, 8, 28, 56, 70, 56, 28, 8, 1`.

- A) is `C(8,1) = 8`, the count for **exactly one** corrupted bit. The whole
  point of Step 2 of the worked example is that you do not derive 28 or 70
  separately — you read them off the row the theorem guarantees.
- C) is `C(8,2) = 28`, the count for exactly two. Reading a palindromic row
  carelessly is how the wrong column gets picked; the row is symmetric about
  `k = 4`, so entries 2 and 6 are the same number and nothing tells you from the
  row alone which side you meant.
- D) is the size of the message space, i.e. the total over all `k` from 0 to 8.
  That is `Σ_k C(8,k) = 2⁸ = 256`.

</details>

**Q3.** What does the specialisation `Σ_{k=0}^{n} C(n, k) = 2ⁿ` count, and what
substitution produces it?

- A) The even entries of row `n`; substitute `a = b = 1`
- B) All subsets of an `n`-element set; substitute `a = b = 1` in the binomial
  theorem
- C) The subsets of even size; substitute `a = 1, b = 0`
- D) The strings of length `n` over a 2-symbol alphabet; substitute `a = 2, b = 0`

<details>
<summary>Answer and explanation</summary>

**B) All subsets of an `n`-element set; substitute `a = b = 1` in the binomial
theorem.**

With `a = b = 1` every monomial `a^(n−k)b^k` collapses to 1, so the expansion
becomes `2ⁿ = Σ_k C(n,k)`. The lesson reads this as the count of subsets — the
`k`-subsets are the `k`-th column and together they are all 2ⁿ subsets.

- A) is half the row. `Σ_{k even} C(n,k) = 2^(n−1)` for `n ≥ 1`, and that is the
  `a = 1, b = −1` identity applied to the even terms, not the `a = b = 1` one.
- C) is nonsense arithmetically: `a = 1, b = 0` leaves only the `k = 0` term, so
  it gives `1`, which is the number of *empty* selections.
- D) has the right answer for the wrong reason — there are indeed 2ⁿ binary
  strings of length `n` — but the derivation is wrong: `a = 2, b = 0` gives
  `(2+0)^n = 2^n` with a single surviving term `2ⁿ`, not a sum over `k`. The
  count coincides; the formula does not produce it.

</details>

**Q4.** What is `Σ_{k=0}^{n} (−1)ᵏ C(n, k)`?

- A) 0 for every `n ≥ 0`
- B) 0 for every `n ≥ 1`, and 1 when `n = 0`
- C) 1 for every `n`
- D) `(1 − 1)ⁿ`, which equals 0 for `n = 0` as well

<details>
<summary>Answer and explanation</summary>

**B) 0 for every `n ≥ 1`, and 1 when `n = 0`.**

Substitute `a = 1, b = −1` in the binomial theorem: `(1 + (−1))ⁿ = 0ⁿ`, which is 0
for `n ≥ 1` and, by the empty-product convention, `0⁰ = 1`. The lesson's code
prints `alt sum = 0 for n>0` at `n = 8`, and the domain restriction is real.

- A) drops the `n = 0` case. It matters: `C(0,0) = 1` and the empty string is a
  genuine object counted by every identity in the lesson, so an identity stated
  for `n ≥ 0` without the exception is wrong at exactly one input.
- C) is the `n = 0` answer promoted to a universal claim.
- D) repeats the mistake and makes it worse: it asserts `0⁰ = 0`, which is
  undefined. The subtlety is precisely that the empty product is 1.

</details>

**Q5.** Compute `Σ_{k=0}^{8} k · C(8, k)` using the lesson's identity.

- A) 1,024
- B) 512
- C) 4,608
- D) 2,048

<details>
<summary>Answer and explanation</summary>

**A) 1,024.**

The first-moment identity is `Σ_k k·C(n,k) = n·2^(n−1)`, valid for `n ≥ 1`. With
`n = 8` that is 8 · 2⁷ = 1,024. The lesson's code computes the sum by brute force
over the row and prints the same number, which is the check that the identity
says what it says.

- B) is `n·2^(n−2) = 8 · 64 = 512`, i.e. the falling-factorial identity with the
  wrong `n(n−1)` replaced by `n`. A factor of 2 low.
- C) is `n(n+1)·2^(n−2) = 8 · 9 · 64 = 4,608`, which is the `k²` identity, not the
  `k` one. It is strictly larger, which is the direction you would expect if you
  accidentally weighted by `k²`.
- D) is `n · 2ⁿ = 2,048`, forgetting that the exponent drops by one. The `−1`
  is the whole content of the identity: total population over all `n`-bit words
  is `n·2^(n−1)`, because each of the `n` bit positions is set in exactly half of
  the `2ⁿ` words.

</details>

**Q6.** Compute `Σ_{k=0}^{8} k² · C(8, k)` using the lesson's identities.

- A) 1,024
- B) 3,584
- C) 4,608
- D) 4,096

<details>
<summary>Answer and explanation</summary>

**C) 4,608.**

Since `k² = k(k−1) + k`, the second moment is the sum of the falling-factorial
identity and the first moment:
`8·7·2⁶ + 8·2⁷ = 3,584 + 1,024 = 4,608`, which is `n(n+1)·2^(n−2)`. This is
Mistake 3 of the lesson, written out: the two identities look similar, and
carrying the `n·2^(n−1)` pattern into the `k²` case is the error.

- A) is the `k`-weighted sum. It is too small by a factor of 4.5, which is the
  factor you would expect, since `k²` weights large `k` far more heavily than
  `k` does.
- B) is `Σ k(k−1)·C(8,k)`, the falling-factorial value. It is missing the `+ k`
  term, so it is short by exactly 1,024.
- D) is `2¹²`, the total number of 12-bit strings — an unrelated number that
  looks plausible because it is also a power of two.

</details>

**Q7.** Evaluate `Σ_{k=0}^{3} C(4, k) · C(6, 3 − k)`. Which identity is this an
instance of, and what is the value?

- A) Pascal's recursion; 20
- B) Vandermonde's identity; `C(10, 3) = 120`
- C) The hockey-stick identity; `C(6, 3) = 20`
- D) The binomial theorem with `a = 4, b = 6`; 1,000

<details>
<summary>Answer and explanation</summary>

**B) Vandermonde's identity; `C(10, 3) = 120`.**

Vandermonde states `Σ_k C(m,k)·C(n, r−k) = C(m+n, r)`. Here `m = 4`, `n = 6`,
`r = 3`, so the sum is `C(10, 3) = 120`. The counting story: count 3-subsets of a
disjoint union of a 4-set and a 6-set, either directly or by how many elements the
subset takes from the 4-set. The lesson's code verifies both routes give 120.

- A) is Pascal's recursion, which relates `C(n,k)` to two entries of row `n−1` of
  the *same* triangle — it has no product of two different coefficients in it.
- C) is the hockey-stick identity, which sums `C(j, 2)` over `j`; it has no
  product.
- D) applies the binomial theorem with numeric bases where the identity's `a` and
  `b` are *variables* being counted over. `4` and `6` here are sizes, not
  summands, and `(4+6)^10 = 10¹⁰` has nothing to do with the sum.

</details>

**Q8.** Evaluate `Σ_{j=2}^{5} C(j, 2)`. Which identity explains the result?

- A) Vandermonde; the answer is `C(10, 3) = 120`
- B) The hockey-stick identity; the answer is `C(6, 3) = 20`
- C) The row-sum identity; the answer is `2⁵ = 32`
- D) Pascal's recursion; the answer is `C(5, 2) = 10`

<details>
<summary>Answer and explanation</summary>

**B) The hockey-stick identity; the answer is `C(6, 3) = 20`.**

Sum a diagonal of Pascal's triangle and you get one binomial coefficient:
`Σ_{j=r}^{N} C(j,r) = C(N+1, r+1)`. With `r = 2`, `N = 5` that is `C(6,3) = 20`,
which you can check by hand: `1 + 3 + 6 + 10 = 20`.

- A) applies Vandermonde, whose summand is a *product* of two coefficients from
  different triangles. This sum has one coefficient per term.
- C) sums a whole row and gives `Σ_{k=0}^{5} C(5,k) = 32`. Here the top index
  moves and the bottom index is fixed, which is the diagonal, not the row.
- D) misreads the sum as one term. `C(5,2) = 10` is the largest single summand,
  not the total.

</details>

**Q9.** How many 12-bit strings contain no two adjacent 1s?

- A) 4,096
- B) 1,728
- C) 377
- D) 3,828

<details>
<summary>Answer and explanation</summary>

**C) 377.**

Split on the last bit: a string ending in `0` is any valid length-11 string
(`q₁₁` of them), and one ending in `1` must end in `01`, so it is any valid
length-10 string (`q₁₀`). Hence `q_n = q_{n−1} + q_{n−2}` with `q₀ = 1`, `q₁ = 2`,
which is `q_n = F(n+2)`, so `q₁₂ = F₁₄ = 377`. The lesson prints the two-state
DP, the generating function, and brute force in three columns and they agree.
That is `377/4096 = 0.092`, so about 9.2% of 12-bit words qualify.

- A) is the whole space. Every string is either valid or not, so 4,096 is the
  denominator of the fraction, not the count.
- B) is `F₁₂ = 144`, off by one Fibonacci index. With `q₀ = 1, q₁ = 2`, `q_n = F(n+2)`,
  so `n = 12` needs `F(14) = 377`; `F(12) = 144` is `q₁₀`.
- D) is 4,096 − 377 = 3,719 rounded up by a different path, and it is not a
  meaningful quantity: it is the count of *strings containing* an adjacent pair,
  which is a different object from the count avoiding one.

</details>

**Q10.** In the worked example, bits flip independently with probability 0.1.
What is the expected number of corrupted bits in an 8-bit message?

- A) 0.8
- B) 8
- C) 0.1
- D) 0.9

<details>
<summary>Answer and explanation</summary>

**A) 0.8.**

`E[K] = Σ_k k·C(8,k)·0.1ᵏ·0.9^(8−k)`, which the weighted-sums theorem collapses
to `n·p·(0.9 + 0.1)⁷ = 8 · 0.1 · 1 = 0.8`. The step 4 comment makes the point
that the closed form and the intuition agree: 8 bits, each wrong with
probability 0.1.

- B) is `n`, the maximum. It ignores the probability entirely and is what you
  would get if every bit flipped.
- C) is `p`, the per-bit probability. It forgets the 8 independent trials, and it
  is the answer to "how likely is one given bit to be wrong".
- D) is `1 − p`, the probability a given bit is *correct*. Multiplying by `n`
  would give 7.2, which is not any of the quantities here.

</details>

**Q11.** What does Lucas' theorem say about `C(100, 30) mod 7`?

- A) You must compute `C(100, 30)` exactly and then reduce, which is why the
  lesson provides it
- B) Writing `100 = (202)_7` and `30 = (42)_7`, a digit of `k` exceeds the matching
  digit of `n`, so `C(100, 30) ≡ 0 mod 7`
- C) It equals `C(4, 2) · C(0, 4) · C(2, 0) mod 7 = 12 mod 7 = 5`
- D) It equals `30! / (100! · 70!) mod 7`, which reduces to 1

<details>
<summary>Answer and explanation</summary>

**B) Writing `100 = (202)_7` and `30 = (42)_7`, a digit of `k` exceeds the matching
digit of `n`, so `C(100, 30) ≡ 0 mod 7`.**

Lucas says `C(n,k) ≡ Π_i C(n_i, k_i) mod p`. Reading digits from the
least significant end: `k` has digits `2, 4` and `n` has `2, 0, 2`. The factor
`C(0, 4) = 0` forces the product to 0. The lesson's code confirms it, printing
`C(100,30) mod 7: Lucas 0, exact 0, agree True`.

- A) is Mistake 5 of this lesson. Building `C(100,30)` exactly means a number
  with about 63 digits — feasible — but `C(10⁶, 5·10⁵)` has a million digits and
  is not. Lucas touches only the base-`p` digits, so it is `O(log_p n)`.
- C) is a genuine Lucas computation with the digits read backwards. The correct
  product is `C(2,2)·C(0,4)·C(2,0) = 0`; writing `C(4,2)` puts `k`'s digit where
  `n`'s belongs and then hits the zero anyway, arriving at 5 by accident.
- D) is not an integer — `30!/(100!·70!)` is `1/(...)`, a fraction far below 1 —
  and it reverses the roles of `n` and `k`.

</details>

---

## Subjective Questions

### Short Answer

**Q1. State the binomial theorem. Why is `C(n, k)` a *count* rather than a
coefficient that happens to appear?**

<details>
<summary>Answer</summary>

For any numbers `a, b` and any non-negative integer `n`:

$$(a+b)^{n} = \sum_{k=0}^{n} C(n,k)\,a^{\,n-k}b^{k}$$

The counting reading: expanding the product of `n` copies of `(a + b)` produces
2ⁿ terms, one per independent choice of `a` or `b` in each position. Group them
by how many positions chose `b`. A group with `k` copies of `b` and `n − k`
copies of `a` has `C(n, k)` members, because you choose which `k` of the `n`
positions hold `b`. So each group contributes `C(n,k) · a^(n−k)b^k`, and summing
over `k` gives the formula.

The coefficient is a count because it is the number of ways of doing the
choosing — not because the algebra produced a number that happens to be
interpretable.

</details>

**Q2. State the three specialisations of the binomial theorem and the
substitution that produces each.**

<details>
<summary>Answer</summary>

- `Σ_{k=0}^{n} C(n,k) = 2ⁿ` — set `a = b = 1`. Valid for all `n ≥ 0`.
- `Σ_{k=0}^{n} (−1)ᵏ C(n,k) = 0` — set `a = 1, b = −1`. Valid only for `n ≥ 1`;
  for `n = 0` the sum is 1.
- `Σ_{k=0}^{n} C(n,k) a^(n−k) = (a+1)ⁿ` — set `b = 1`. Valid for all `n ≥ 0`.

None of them is a separate theorem. Each is the binomial theorem with different
values plugged in, which is the point: choosing `a` and `b` is choosing which
combinatorial question to ask. `a = b = 1` asks "how many subsets"; `a = 1,
b = −1` asks "how do even and odd subset sizes balance".

</details>

**Q3. State the three weighted-sum identities, their domain restrictions, and the
algebra that derives the third from the first two.**

<details>
<summary>Answer</summary>

For `n ≥ 1`:

$$\sum_{k} k\,C(n,k) = n\cdot 2^{\,n-1}$$

For `n ≥ 2`:

$$\sum_{k} k(k-1)\,C(n,k) = n(n-1)\cdot 2^{\,n-2} \qquad \sum_{k} k^{2}C(n,k) = n(n+1)\cdot 2^{\,n-2}$$

The third follows from the algebraic identity `k² = k(k − 1) + k`:
`n(n−1)·2^(n−2) + n·2^(n−1) = n(n−1 + 2)·2^(n−2) = n(n+1)·2^(n−2)`.

The derivation is "differentiate, then substitute". Multiplying the theorem by
`x` and setting `b = x`, `a = 1` gives `Σ_k C(n,k) x^k = (1+x)^n`; differentiating
once gives `Σ_k k·C(n,k) x^(k−1) = n(1+x)^(n−1)`, and setting `x = 1` gives the
first identity. Differentiate twice for the falling factorial, then apply
`k² = k(k−1) + k`.

</details>

**Q4. State Vandermonde's identity and describe the double count that proves
it.**

<details>
<summary>Answer</summary>

For non-negative `m, n, r`:

$$\sum_{k} C(m,k)\,C(n,r-k) = C(m+n,r)$$

Count `r`-subsets of a disjoint union of an `m`-element set `X` and an
`n`-element set `Y`. Directly: `C(m+n, r)`. By how many elements the subset
draws from `X`: choose `k` from `X` and `r − k` from `Y`, then sum over `k`.

This is the template behind the coefficient-matching technique used throughout
this part — two ways of partitioning the same set of objects, one of them a sum
over a splitting variable.

</details>

**Q5. Why does Lucas' theorem help with large coefficients, and why is
`C(100, 30) ≡ 0 mod 7`?**

<details>
<summary>Answer</summary>

Computing `C(n, k)` exactly and then reducing means building a number with
`Θ(n)` bits — for `n = 10⁶` that is a million-digit integer, and you only wanted
a residue. Lucas' theorem says, for prime `p`:

$$C(n,k) \equiv \prod_i C(n_i, k_i) \pmod p$$

with `n = Σ n_i p^i` and `k = Σ k_i p^i` the base-`p` digits. Each factor is a
single-digit binomial coefficient, so the work is `O(log_p n)`.

For `n = 100, k = 30, p = 7`: `100 = (202)_7` and `30 = (42)_7`. Reading from the
least significant digit, `k`'s digit 4 sits above `n`'s digit 0, so
`C(0, 4) = 0` and the whole product vanishes. The lesson's code checks all four
of its examples against `comb(n,k) % p` and they agree.

</details>

**Q6. Sum the number of 1-bits over all `2ⁿ` `n`-bit words. Why is the answer
`n · 2^(n−1)`?**

<details>
<summary>Answer</summary>

$$\sum_{x=0}^{2^{n}-1} \mathrm{popcount}(x) = n \cdot 2^{\,n-1}$$

Count differently: fix one of the `n` bit positions and ask how many words have
that bit set. Writing that bit gives a free choice of the remaining `n − 1`
bits, so exactly `2^(n−1)` words have it set. Summing over the `n` positions
counts every (word, set bit) pair exactly once, and each pair is one unit of
popcount.

This is the `n·2^(n−1)` weighted-sum identity read as a combinatorial statement.
The lesson checks `n = 4, 8, 12` against a brute-force total.

</details>

### Long Answer

**Q1. Why does the binomial theorem *count* rather than merely compute? What work
would you have to do without the counting reading?**

<details>
<summary>Model answer</summary>

Without the counting reading, `(2 + 3)^10` is an exercise in expanding a product
of ten binomials: 2¹⁰ = 1,024 raw terms, each needing multiplication and then
addition, with nothing to look up. That is roughly 2,048 operations and a page of
arithmetic to produce 9,765,625.

With the counting reading, you never expand anything. You need one row of
eleven numbers — `1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1` — and then you
multiply each by one term. The saving is not constant-factor; it is that the
coefficient *structure* is known in advance and is independent of `a` and `b`. The
row is the same row whatever you are expanding, and it is the same row however
large the power is. Step 2 of the worked example makes the operational point: "we
did not derive 28 or 70 — we looked them up from the structure the theorem
guarantees."

The deeper reason the counting reading is load-bearing is that it transfers. Once
you know the `k`-th coefficient is the number of `k`-subsets, the same eleven
numbers answer questions that have nothing to do with algebra:

- **Bit patterns.** `C(8, k)` is the number of 8-bit words with exactly `k` bits
  set. That is a Hamming-weight enumerator, and it is the distribution the whole
  lesson's error model rests on.
- **Subset sums.** `Σ_k C(n,k) = 2ⁿ` evaluates a row in one step, and
  `Σ_k k·C(n,k) = n·2^(n−1)` evaluates a weighted row in one step. Those are
  second-moment calculations in birthday-paradox analysis.
- **Hashes.** `t(x) = popcount(x) mod 2` is the Thue–Morse sequence: a hash that
  looks random, is used in scatter tables and load balancing, and is completely
  predictable. You can only build it once you connect "subsets" to "bit strings".
- **Avoidance counts.** `Q(x) = (1+x)/(1 − x − x²)` gives the number of binary
  strings with no adjacent 1s as a coefficient of a rational function. The
  denominator is not algebra either — it is the recurrence `q_n = q_{n−1} + q_{n−2}`
  written in a different notation.

Algebra is the report of what the counting found. Treating the theorem as
algebra to be memorised is Mistake 1 of this lesson, and it costs you every one of
these applications, because none of them mentions `a` or `b`.

</details>

**Q2. Why does "differentiate, then substitute" work for weighted sums, and
exactly which step fails if you differentiate the wrong thing?**

<details>
<summary>Model answer</summary>

The trick works because the weight `k` and the power `k` of `x` are the same
number, so differentiation can convert one into the other. Start from the
generating form of the binomial theorem:

$$\sum_{k=0}^{n} C(n,k)\,x^{k} = (1+x)^{n}$$

Differentiate. The left side becomes `Σ_k k·C(n,k)·x^(k−1)` because the factor `k`
comes from differentiating `x^k`, and the right side becomes `n(1+x)^(n−1)`. Now
substitute `x = 1`, and every `x^(k−1)` becomes 1, leaving
`Σ_k k·C(n,k) = n·2^(n−1)`.

Differentiate twice instead and you get `Σ_k k(k−1)·C(n,k) = n(n−1)(1+x)^(n−2)`,
hence `n(n−1)·2^(n−2)`. The factorials `k(k−1)` are the falling factorials, which
is why the identity comes out in that shape rather than with a plain `k²`. To
recover `k²` you use `k² = k(k−1) + k` — Mistake 3 of the lesson is carrying the
`n·2^(n−1)` pattern into the `k²` case instead of doing this algebra explicitly,
which for `n = 8` gives 1,024 rather than 4,608.

The step that fails if you differentiate the wrong thing is the **substitution**.
The weighted sum you want is the value at `x = 1`; the differentiated expression
is `x^(k−1)` times something, so you must remove the powers of `x`, and only
`x = 1` (or `x = 0` for some terms) removes them all at once. Two concrete
failures:

- Substituting `x = 2` gives `Σ_k k·C(n,k)·2^(k−1) = n·3^(n−1)`, which is true
  and useless for your purpose — it is a different sum, weighted by `2^(k−1)`.
- Forgetting to substitute at all leaves an identity about a polynomial, not
  about a number, and it is tempting to stop there because the algebra "checked
  out".

There is a second failure mode, about the base form. The identity
`Σ_k C(n,k) x^k = (1+x)^n` is *not* the binomial theorem — it is the binomial
theorem with `a = 1` and `b = x`, which is legitimate only because you are now
treating `x` as a variable to be specialised afterwards. If you start from
`(a+b)^n = Σ_k C(n,k) a^(n−k) b^k` and differentiate with respect to `a`, you get
`(n−k)` factors rather than `k` ones, and you have to set `b = 1` as well as
`x = 1` before the powers disappear. Getting the base form wrong is why some
people conclude "you cannot differentiate this" — you can, but the clean version
requires `a = 1` first.

</details>

**Q3. The lesson counts strings avoiding "11" both with a two-state dynamic
program and with a generating function. What does the generating-function route
add, and what would break if you used only the dynamic program?**

<details>
<summary>Model answer</summary>

The generating function route adds a *closed, algebraic* description. From the
recurrence `q_n = q_{n−1} + q_{n−2}` with `q₀ = 1, q₁ = 2` one gets
`Q(x) = Σ_n q_n x^n` and solves `(1 − x − x²)Q(x) = 1 + x`, so
`Q(x) = (1+x)/(1 − x − x²)`. From here `q_n = F(n+2)`, the coefficient is a
*named sequence* rather than an entry in a table, and the answer becomes an
expression you can reason about: the growth rate is the golden ratio φ to the
power `n`, `φ ≈ 1.618`, so the fraction of valid strings tends to
`(3/4)^n (1 + 1/√3)`, a closed form for a probability.

What breaks with the dynamic program alone is everything you cannot do to a
table. You cannot take an asymptotic limit of an entry. You cannot combine two
problems by multiplying their polynomials and reading off coefficients, which is
the "choosing with limits" technique from
[Lesson 21](../part02_discrete_combinatorics/21_permutations_and_combinations.md)
and the general coefficient-extraction lemma
`[x^k] f(x)g(x) = Σ_{i+j=k} f_i g_j`. You cannot state, let alone prove,
`Vandermonde's identity`, whose proof *is* "count one thing two ways and match
coefficients". And you cannot read off generating-function theorems — that a
generating function is rational exactly when the sequence satisfies a linear
recurrence with constant coefficients, which is why `(1 + x)/(1 − x − x²)`
producing Fibonacci is not a coincidence but a mechanism.

The reverse is also true, and that is the part the lesson is really teaching. A
generating function does not tell you a coefficient without work. `Q(x)` above
looks like an answer; to get `q₁₂ = 377` from it you still run the recursion, and
that is why the lesson prints three columns — two-state DP, generating function,
brute force — and checks they agree. The generating function buys structure and
generality; the dynamic program buys speed and certainty. The mistake is treating
either as sufficient alone, and treating "it looked like a rational function so
the answer is φ^n" as a computation when φ is irrational and `q_n` is an integer.

</details>

**Q4. The lesson argues against computing a huge coefficient exactly when you
only need it modulo a prime. What would actually break, and what is the argument
for the modular route?**

<details>
<summary>Model answer</summary>

The breakage is resource exhaustion, and it arrives earlier than intuition
suggests. `C(100, 30)` has 63 digits — annoying but fine. `C(1000, 500)` has 300.
`C(10⁶, 5·10⁵)` has about 300,000 digits, and you are about to multiply two
numbers that large in order to divide them back down. The naive factorial form is
worse still: it builds `n!`, which for `n = 10⁶` has about 5.5 million digits,
before a single division happens. At that size `math.comb` is not "slow", it is
allocating more memory than the process is allowed.

The argument for the modular route is that it never builds the number at all.
Lucas' theorem factors `C(n,k) mod p` into a product of single-digit binomial
coefficients `C(n_i, k_i)`, each computable in constant time, so the work is
`O(log_p n)` multiplications of residues below `p`. Nothing grows with `n`. The
same is achievable without Lucas by multiplying numerator and denominator
products modulo `p` and inverting the denominator with a modular inverse — the
point is the modulus discipline, not the specific theorem.

Why the objection "I only need the residue, but I still have to be *correct*"
does not defeat it is worth stating, because it is the reason people do the
expensive thing. Modular arithmetic is not approximate: reducing after each step
is exactly equivalent to reducing at the end, because multiplication respects
congruence. The one thing you must not do is divide by a multiple of `p`, which is
why the denominator needs a modular inverse and why `p` must be prime — Fermat's
little theorem gives `a^(p−2)` as the inverse. In a composite-modulus scheme (as in
Chinese remainder reconstruction for NTT-based multiplications) you need the
denominator to be coprime to the modulus, and you handle the rest of the primes
separately.

This matters in practice because Reed–Solomon codecs and CRC/checksum schemes
evaluate `C(n, k) mod p` routinely with `n` in the thousands, on every block, as
part of encoding. Nothing else in this part is used at that scale, which is why
the lesson says the wall is real: `math.comb` is fast enough on small inputs that
you never learn where the boundary is.

</details>

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