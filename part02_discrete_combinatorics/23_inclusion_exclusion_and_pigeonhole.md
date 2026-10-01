# 23 — Inclusion–Exclusion and the Pigeonhole Principle

**Part**: part02_discrete_combinatorics · **Prerequisites**: 22 · **Time**: 40 min

---

## In Plain Words

The sum rule from [Lesson 20](../part02_discrete_combinatorics/20_counting_principles.md) has one condition you
cannot skip: the cases must not overlap. Count how many integers from 1 to 100
are even, and how many are multiples of 3, and add. You get 83. But 6 is both, so
you counted it twice, and the true answer is 74. This lesson is about fixing that
kind of error, and about a much simpler idea that turns out to be shockingly
powerful.

**Inclusion–exclusion** is the fix. If you count each set on its own and then
subtract every pairwise overlap, the doubly-counted elements get subtracted once
and are back where they started. But the elements that were counted *three* times
have been subtracted twice too many, so you add back the triple overlaps, and that
over-corrects in the other direction, so you subtract the quadruple overlaps, and
on it goes. The signs alternate: add singles, subtract pairs, add triples. The
alternation is not arbitrary — each term's job is to cancel the error introduced by
the previous one, and each pass fixes exactly one extra layer of overcounting. The
pattern is: for every non-empty subset of your sets, add or subtract according to
whether that subset has an odd or even number of members.

The cost is the number of terms, which is 2ⁿ − 1 for n sets. For five sets that is
thirty-one terms, which is fine. For thirty sets it is a billion, which is not. So
the practical advice in this lesson is: **use the complement**. "How many satisfy
none of these constraints" is far easier than "how many satisfy at least one", and
when both are hard, switch to counting the good cases directly or to a program.

**The pigeonhole principle** is a different idea and needs no arithmetic at all.
If you put n + 1 objects in n boxes, two objects share a box. That is it. The
general form is that some box holds at least ⌈n/k⌉ of the n objects in k boxes.
The reason it matters is that it proves things *exist* without telling you how to
find them. It is the formal reason that some two of your one million users share a
birthday, that some two hash inputs collide, that some two integers in your file
are near-duplicates, and that some prime number bigger than n exists. It is an
existence theorem you can apply in one line, and it is used constantly in
production systems — bucket sizes, dedup guarantees, and table sizing are all
pigeonhole arguments.

## Why Computer Science Cares

- **Hash table sizing.** A table of size m receiving n items must have a bucket
  with at least ⌈n/m⌉ items. This is not a possibility, it is a guarantee, and it
  is why load factor is the number you alert on. It also tells you the table is
  *fine* — you only need to act when some bucket exceeds a threshold that the
  pigeonhole principle does not force.
- **Birthday bounds and collision probability.** With 2⁶⁴ hash values, 366 items
  already force a collision — a number that shocks people who expect "64 bits is
  plenty". The generalised form (⌈n/k⌉) is what turns this into the birthday
  paradox analysis in [Lesson 70](../part05_probability_statistics/70_information_theory_entropy.md).
- **Counting "clean" configurations.** The number of functions from an n-element
  domain that hit *every* codomain element is nⁿ minus the ones that miss at least
  one — inclusion–exclusion, and it is how you count valid assignments,
  surjective heap layouts, and onto mappings in schedulers. The related result
  that the count is divisible by n! is a genuine restriction you can use as a
  sanity check.
- **Derangements.** The count of permutations with no fixed point, !n ≈ n!/e, is the
  inclusion–exclusion formula and shows up in "my files will never be corrupted by
  chance" arguments, in permutation-based anonymisation, and in testing shuffle
  implementations.
- **Surjective hashing and perfect hashing.** Minimum perfect hash functions exist
  only when the key set size equals the table size — a pigeonhole consequence that
  the whole CHD algorithm family is built on.
- **Deduplication guarantees.** If you put n records through a bloom filter with m
  bits, at least one bit is set in ⌈n/k⌉ positions. Bloom filter sizing formulas are
  pigeonhole arithmetic.
- **Proving an algorithm terminates or that a bound is tight.** Pigeonhole proves
  that n items cannot all land in distinct buckets when buckets < items, which is
  how you lower-bound the number of comparisons any sorting algorithm needs.

## The Formal Version

**Definition.** Sets A₁, …, A_n are **pairwise disjoint** if A_i ∩ A_j = ∅ for
i ≠ j.

**Theorem (Two-set inclusion–exclusion).** For finite A, B,

    |A ∪ B| = |A| + |B| − |A ∩ B|

**Explanation.** |A| + |B| counts every element of A ∪ B at least once, and every
element of A ∩ B exactly twice. Elements outside A ∪ B are not counted at all.
Subtracting |A ∩ B| removes one spurious copy of each doubly-counted element and
none of the correctly-counted ones. This is the whole reason for the minus sign.

**Theorem (Inclusion–exclusion, finite form).** For finite A₁, …, A_n and finite
S_1, …, S_m (here S_k is the k-element set of indices),

    |∪_{i=1..n} A_i| = Σ_{∅≠S⊆S_m} (−1)^{|S|+1} · |∩_{i∈S} A_i|

    |∩_{i=1..n} Ā_i| = Σ_{S⊆S_m} (−1)^{|S|} · |∩_{i∈S} A_i|

*Explanation.* Consider an element x belonging to exactly r of the sets, so it is
counted in exactly r of the intersections appearing in the sum. Its total
coefficient in the first formula is

    Σ_{j=1..r} (−1)^{j+1} · C(r, j)  =  1

because the alternating binomial sum for r ≥ 1 equals (1 − 1)ʳ = 0 for the terms
from j = 2 on, leaving 1. So every element of the union is counted exactly once and
every element outside it exactly zero times. The complement formula follows by the
same argument applied to the A_iᶜ.

**Corollary (Term count).** The formula has 2ⁿ − 1 non-empty subsets to sum over.

*Explanation.* Each of the n sets may be in the subset S or not, giving 2ⁿ
subsets, minus the empty one. This is the practical limit of the method.

**Theorem (Surjections).** The number of functions f : A → B with |A| = n, |B| = k
that hit every element of B is

    Σ_{j=0..k} (−1)ʲ · C(k, j) · (k − j)ⁿ

**Explanation.** Start with all kⁿ functions. Let B_j be the set of functions whose
image misses element j; we want the complement of the union of the B_j. By the
complement form of inclusion–exclusion the count is Σ (−1)ʲ Σ_{|S|=j} |∩ B_i|, and
there are C(k, j) ways to choose S, each with |∩ B_i| = (k − j)ⁿ functions (each
input may map to any of the k − j allowed targets).

**Theorem (Derangements).** The number of permutations of an n-element set with no
fixed point is

    !n = n! · Σ_{j=0..n} (−1)ʲ / j!   =  n! Σ_{j=0..n} (−1)ʲ C(n, j)/C(n, j)  (and !n ≈ n!/e)

*Explanation.* !n = Σ (−1)ʲ C(n, j)(n − j)!, again the complement formula with
B_j = permutations fixing j. Dividing the j-th term by n! gives (−1)ʲ C(n,j)(n−j)!/n!
= (−1)ʲ C(n,j)/C(n,j) · 1/j! — more usefully, C(n,j)(n−j)! = n!/j!, so the sum is
n! Σ (−1)ʲ/j!.

**Theorem (Pigeonhole principle).** If n + 1 objects are placed into n boxes, some
box contains at least two objects.

*Explanation.* Assume every box held at most one object. Then the boxes hold at
most n objects in total, contradicting n + 1. The general form: if n objects are
placed into k boxes, some box contains at least ⌈n/k⌉ objects.

**Corollary (Pairing form).** If each of n boxes holds at most c objects, then at
most nc objects fit. So if you have more than nc objects, some box exceeds c.

*Explanation.* Direct contrapositive of the general form.

**Theorem (Existence via pigeonhole).** For every n ≥ 2 there is a prime p > n.

*Explanation.** Consider n! + 1. It is larger than 1, so it has a prime divisor p.
Now n! = 1 · 2 · ... · n, and every prime p ≤ n divides n!, so p | n! + 1 would
give p | 1, impossible. Hence p > n. The proof contains no computation of any
primality — it is pure existence.

## Worked Example

**The question.** How many integers from 1 to 100 are divisible by 2, or by 3, or
by 5? Solve it with inclusion–exclusion, then verify by brute force.

**Step 1 — Name the sets.** A₂ = multiples of 2 in [1, 100], A₃ = multiples of 3,
A₅ = multiples of 5. We want |A₂ ∪ A₃ ∪ A₅|.

**Step 2 — Singles.** |A₂| = 50, |A₃| = 33 (because 99 is the largest multiple of
3 ≤ 100), |A₅| = 20. Sum = 103. Already 3 too many.

**Step 3 — Pairs.** Intersections are multiples of the product, since 2, 3, 5 are
pairwise coprime:
|A₂ ∩ A₃| = |multiples of 6| = 16, |A₂ ∩ A₅| = |multiples of 10| = 10,
|A₃ ∩ A₅| = |multiples of 15| = 6. Sum = 32.

**Step 4 — Triple.** |A₂ ∩ A₃ ∩ A₅| = |multiples of 30| = 3.

**Step 5 — Combine with alternating signs.**

    103 − 32 + 3 = 74

**Step 6 — Check the correction is sensible.** We started 3 above and ended 3 below
100's worth of "countable" mass... more concretely, the complement is 100 − 74 = 26
integers divisible by none of 2, 3, 5 — these are the integers coprime to 30 up to
100. That is the right order of magnitude for φ(30)/30 × 100 = 8/30 × 100 ≈ 26.7.
Brute force gives exactly 26. Good.

**Why the signs work, restated on this example.** The number 30 was counted three
times in the singles (103), subtracted in all three of its pair-intersections
(−3), and added back in the triple (+1): net 3 − 3 + 1 = 1. ✓ The number 60: also
in all three sets, also counted 3 times, and also in all three pairs — same net 1.
✓ The number 6: in A₂ and A₃ only, counted twice, subtracted once — net 1. ✓
The number 100: in A₂ and A₅ only, counted twice, subtracted once — net 1. ✓ Every
element nets exactly one, which is the whole theorem.

**The complement version, which is often easier.** "Divisible by none of 2, 3, 5" =
100 − |A₂ ∪ A₃ ∪ A₅| = 26, or directly by the complement formula:
100 − 103 + 32 − 3 = 26. Same work, but the framing "count the clean ones" is
usually the right instinct when a constraint says "at least one", and "count the
dirty ones" when it says "at most".

## Runnable Code

A general inclusion–exclusion solver over any universe, refereed by brute force.
Build the sets, apply the formula, apply `set.union`, compare.

```python
from itertools import combinations, chain

def inclusion_exclusion(sets):
    """|A1 u A2 u ... u An| for a list of finite sets.

    Sums over every non-empty subset S of the indices with sign (-1)^(|S|+1):
    odd-sized intersections are added, even-sized subtracted."""
    n = len(sets)
    total = 0
    for size in range(1, n + 1):
        sign = 1 if size % 2 == 1 else -1
        for combo in combinations(range(n), size):
            inter = set.intersection(*(sets[i] for i in combo))
            total += sign * len(inter)
    return total

def complement_ie(sets, universe_size):
    """Count the elements of the universe in NONE of the sets.

    Sum over ALL subsets S (including empty) with sign (-1)^|S|."""
    n = len(sets)
    total = universe_size  # the empty intersection is the whole universe
    for size in range(1, n + 1):
        sign = -1 if size % 2 == 1 else 1
        for combo in combinations(range(n), size):
            total += sign * len(set.intersection(*(sets[i] for i in combo)))
    return total

U = set(range(1, 11))
sets = [
    {x for x in U if x % 2 == 0},
    {x for x in U if x % 3 == 0},
    {x for x in U if x % 5 == 0},
]
union = set().union(*sets)
print(f"sets: {[sorted(s) for s in sets]}")
print(f"union by inclusion-exclusion : {inclusion_exclusion(sets)}")
print(f"union by brute force         : {len(union)}")
print(f"union by set.union           : {len(union)}")
print(f"none of them, complement IE  : {complement_ie(sets, len(U))}")
print(f"none of them, brute force    : {len(U) - len(union)}")
```

The divisibility example from the worked solution, in full.

```python
from itertools import combinations
from math import comb

U = range(1, 101)
divisors = [2, 3, 5]
sets = [{x for x in U if x % d == 0} for d in divisors]

singles = sum(len(s) for s in sets)
pairs = sum(len(set.intersection(sets[i], sets[j]))
            for i, j in combinations(range(3), 2))
triple = len(set.intersection(*sets))
result = singles - pairs + triple
print(f"single terms  (+): {singles}")
print(f"pair terms    (-): {pairs}")
print(f"triple term   (+): {triple}")
print(f"union = {singles} - {pairs} + {triple} = {result}")
print(f"brute force    = {len(set().union(*sets))}")

# A sieve is the better tool once the divisor set is large: cross off every
# multiple of each divisor, then count what survives.
sieve = [True] * 101  # sieve[0] is irrelevant; we only read 1..100
for p in divisors:
    for multiple in range(p, 101, p):
        sieve[multiple] = False
print(f"sieve count   = {sum(1 for x in range(1,101) if sieve[x])}")
print(f"coprime to 30 = {[x for x in range(1,101) if sieve[x]]}")
```

Surjections: inclusion–exclusion against exhaustive enumeration of functions.

```python
from itertools import product
from math import comb

def onto(n, k):
    """Functions from an n-element set onto a k-element set.

    sum_{j=0..k} (-1)^j C(k,j) (k-j)^n: all k^n functions, minus those missing a
    given element, plus back those missing two, and so on."""
    return sum((-1) ** j * comb(k, j) * (k - j) ** n for j in range(k + 1))

def brute(n, k):
    return sum(1 for f in product(range(k), repeat=n) if set(f) == set(range(k)))

print("n -> k :  IE : brute force")
for n in range(1, 5):
    for k in range(1, min(n, 3) + 1):
        print(f"{n} -> {k} : {onto(n, k):3d} : {brute(n, k):3d}")
print(f"onto(5,3) = {onto(5,3)} (IE only; brute force over 3^5 = {3**5} functions)")
```

Derangements, the most famous inclusion–exclusion application.

```python
from itertools import permutations
from math import comb, factorial

def derangements(n):
    """!n = sum_{j=0..n} (-1)^j C(n,j) (n-j)!  =  n! * sum (-1)^j / j!."""
    return sum((-1) ** j * comb(n, j) * factorial(n - j) for j in range(n + 1))

def brute(n):
    return sum(1 for p in permutations(range(n)) if all(p[i] != i for i in range(n)))

print("n :  !n (IE) : !n (brute) : n!/e :")
for n in range(0, 7):
    approx = factorial(n) / 2.718281828459045
    print(f"{n} : {derangements(n):6d} : {brute(n):9d} : {approx:9.1f}")
print(f"!6/6! = {derangements(6) / factorial(6):.4f}  approaches 1/e = 0.3679")
```

The pigeonhole principle in code: guaranteed collisions, guaranteed crowding, and
existence checks.

```python
from math import ceil

def guaranteed_collisions(n_items, n_boxes):
    """Any placement of n_items objects in n_boxes boxes puts at least two
    together. Returns True exactly when some box must hold >= 2."""
    return n_items > n_boxes

def guaranteed_max_load(n_items, n_boxes):
    """Some box holds at least ceil(n_items / n_boxes) objects."""
    return ceil(n_items / n_boxes)

def guaranteed_over(n_items, n_boxes, cap):
    """Some box must hold more than cap objects when n_boxes * cap < n_items."""
    return n_items > n_boxes * cap

print(f"366 items, 365 boxes -> collision guaranteed: {guaranteed_collisions(366, 365)}")
print(f"365 items, 366 boxes -> not guaranteed      : {guaranteed_collisions(365, 366)}")
print(f"100 items in 12 buckets -> some holds >= {guaranteed_max_load(100, 12)}")
print(f"1M items in 2^20 slots -> load factor {1_000_000 / 2**20:.3f}, "
      f"some slot holds >= {guaranteed_max_load(1_000_000, 2**20)}")
print(f"2^64 slots, 2^64 + 1 items: collision guaranteed "
      f"{guaranteed_collisions(2**64 + 1, 2**64)}")
print(f"2^64 slots, 2^64 items     : collision guaranteed "
      f"{guaranteed_collisions(2**64, 2**64)} (nothing is forced yet)")
# The cap form is the one you alert on: 1000 items in 100 boxes forces a bucket
# above 9, but says nothing at all about exceeding 10.
print(f"1000 items, 100 boxes, cap  9 -> must exceed: {guaranteed_over(1000, 100, 9)}")
print(f"1000 items, 100 boxes, cap 10 -> must exceed: {guaranteed_over(1000, 100, 10)}")
```

Existence proofs the pigeonhole principle gives for free, without any computation.

```python
from math import factorial

def prime_divisor_of_factorial_plus_one(n):
    """n! + 1 has a prime factor; that factor is > n. Return the smallest one."""
    value = factorial(n) + 1
    p = 2
    while p * p <= value:
        if value % p == 0:
            return p
        p += 1
    return value

def all_symmetric_relations(labels):
    """Every possible undirected 'knows' relation on `labels`.

    Each unordered pair of people is either an edge or not, so this enumerates
    2^(C(n,2)) acquaintance patterns -- feasible for n <= 5."""
    pairs = [(a, b) for i, a in enumerate(labels) for b in labels[i + 1:]]
    for mask in range(1 << len(pairs)):
        yield {pairs[k] for k in range(len(pairs)) if (mask >> k) & 1}

def degree(v, edges):
    """How many of the group v knows."""
    return sum(1 for a, b in edges if v in (a, b))

# Among n+1 people two must know the same number of the others, because the
# degrees can never be exactly 0, 1, ..., n: whoever knows nobody is known by
# nobody, so nobody can know everybody. Checked here by exhaustive enumeration.
for V in ([0, 1, 2], [0, 1, 2, 3], [0, 1, 2, 3, 4]):
    patterns = [
        tuple(sorted(degree(v, e) for v in V)) for e in all_symmetric_relations(V)
    ]
    all_repeat = all(len(set(c)) < len(V) for c in patterns)
    distinct = tuple(range(len(V))) in patterns
    print(f"{len(V)} people: {len(patterns):4d} patterns, every one repeats a "
          f"degree: {all_repeat}, degrees 0..n-1 ever occur: {distinct}")

for n in range(2, 7):
    p = prime_divisor_of_factorial_plus_one(n)
    print(f"n={n}: {n}!+1 smallest prime factor = {p} (> n: {p > n})")

print(f"2^n > n^2 for n = 5,6,7: {[2**n > n**2 for n in range(5, 8)]}")
print("the only obstacle to degrees being 0,1,...,n is that 0 and n are "
      "mutually impossible, which is the whole proof.")
```

## Common Mistakes

**1. Subtracting overlaps but forgetting the triple.**

> Wrong: "Multiples of 2, 3, or 5 in [1,100]: 103 − 32 = 71."
> Right: 103 − 32 + 3 = 74. The number 30 is in all three sets. Adding singles
> counted it three times, subtracting pairs subtracted it three times, so it nets
> to zero; the triple term brings it back to one.
> Why the wrong one is tempting: with two sets there are no triples, so the habit
> from the two-set case carries over. The moment you add a third set, the formula
> changes shape.

**2. Counting pairs with C(k, 2) but forgetting there are more than 2 sets.**

> Wrong: "Four sets, so subtract the six pairwise overlaps and stop."
> Right: subtract the six pairwise overlaps, add the four triple overlaps,
> subtract the one quadruple overlap. The general rule is a sum over all 2ⁿ − 1
> non-empty subsets.
> Why the wrong one is tempting: pairwise overlap is the visible, tangible
> double-counting. Triples are invisible until you try to write out a small
> example and find element 30 sitting at zero.

**3. Using inclusion–exclusion when there are too many sets.**

> Wrong: apply the formula to 40 hash functions to find the probability that at
> least one collides.
> Right: use the complement in the right direction and the Poisson approximation
> instead. The IE formula has 2⁴⁰ − 1 terms; the birthday analysis in Lesson
> [70](../part05_probability_statistics/70_information_theory_entropy.md) gives a
> usable answer in a few lines.
> Why the wrong one is tempting: IE is *correct* for any n, so there is never a
> moment where it is obviously wrong — only when it becomes too slow to run. Check
> the term count before you commit.

**4. Misreading the pigeonhole conclusion.**

> Wrong: "100 users, 12 birth months, so two share a month."
> Right: some month holds at least ⌈100/12⌉ = 9 users. Two sharing is true but
> wildly understates it — the guarantee is about a *crowded* box, not a *full* one.
> Why the wrong one is tempting: the classic version (n + 1 objects, n boxes) is
> memorised as "two collide", and the conclusion gets frozen at the weakest form.
> The interesting engineering statements — a 9× hot bucket, some value seen at
> least k times — require the general ⌈n/k⌉ form.

**5. Concluding existence where the pigeonhole principle does not apply.**

> Wrong: "With 2⁶⁴ hash values, two inputs must collide, so 64-bit hashes are
> unsafe."
> Right: two inputs *can* collide, and they will if you have 2⁶⁴ + 1 of them, or —
> by the birthday argument — already with far fewer in practice. "Must collide"
> requires items > boxes; "will collide with high probability" is the birthday
> bound, a probability statement that needs Lesson
> [70](../part05_probability_statistics/70_information_theory_entropy.md), not this
> lesson.
> Why the wrong one is tempting: the words "there exists" sound stronger than "with
> high probability", and it is easy to upgrade an existence theorem into a
> probability claim without noticing.

---

## Exercises and Solutions

**[ ] Exercise 1 — IE for a small universe.** Let the universe be {1, …, 20} and
let A = multiples of 2, B = multiples of 3, C = multiples of 5. Compute
|A ∪ B ∪ C| by inclusion–exclusion and check it by brute force. Then compute the
complement both ways.

<details>
<summary>Solution</summary>

Singles: |A| = 10, |B| = 6, |C| = 4; sum 20.
Pairs: multiples of 6 → 3, of 10 → 2, of 15 → 1; sum 6.
Triple: multiples of 30 in [1,20] → 0.

Union = 20 − 6 + 0 = 14. Complement = 6.

```python
from itertools import combinations

U = range(1, 21)
sets = [{x for x in U if x % d == 0} for d in (2, 3, 5)]
union = set().union(*sets)
print(sorted(union), len(union))              # 14 elements
print(sorted(set(U) - union))                 # the 6 coprime-to-30 ones
print(f"inclusion-exclusion = {len(sets[0]) + len(sets[1]) + len(sets[2]) - 6 + 0}")
```
</details>

**[ ] Exercise 2 — Surjections.** How many functions from a 4-element set to a
3-element set hit all three targets? Compute by inclusion–exclusion and by
enumeration.

<details>
<summary>Solution</summary>

onto(4, 3) = Σ_{j=0..3} (−1)ʲ C(3,j)(3−j)⁴ = 3⁴ − 3·2⁴ + 3·1⁴ − 0 = 81 − 48 + 3 = 36.

```python
from itertools import product
from math import comb

def onto(n, k):
    return sum((-1) ** j * comb(k, j) * (k - j) ** n for j in range(k + 1))

brute = sum(1 for f in product(range(3), repeat=4) if set(f) == {0, 1, 2})
print(onto(4, 3), brute)   # 36, 36
```
</details>

**[ ] Exercise 3 — Derangements.** Verify that !5 = 44 by both inclusion–exclusion
and enumeration, and explain in one sentence why !n is close to n!/e.

<details>
<summary>Solution</summary>

!5 = Σ_{j=0..5} (−1)ʲ C(5,j)(5−j)! = 120 − 120 + 60 − 20 + 5 − 1 = 44.

It is close to n!/e because !n = n! Σ_{j=0..n} (−1)ʲ/j!, and the partial sum of
the alternating series Σ (−1)ʲ/j! approaches 1/e.

```python
from itertools import permutations
from math import comb, factorial

def der(n):
    return sum((-1) ** j * comb(n, j) * factorial(n - j) for j in range(n + 1))

print(der(5))   # 44
print(sum(1 for p in permutations(range(5)) if all(p[i] != i for i in range(5))))
print(f"{der(6)/factorial(6):.4f} vs 1/e = {1/2.718281828459045:.4f}")
```
</details>

**[ ] Exercise 4 — Pigeonhole load factor.** A cache holds 4096 entries and receives
1,000,000 requests. By the pigeonhole principle, how many requests must hit the
same entry? Express the load factor and check the arithmetic.

<details>
<summary>Solution</summary>

⌈1,000,000 / 4096⌉ = ⌈244.14⌉ = 245. So some entry receives at least 245 requests —
the cache must have a hot key.

Load factor = 1,000,000 / 4096 ≈ 244.14, so the ceiling is just the next integer up.

```python
from math import ceil

n_items, n_boxes = 1_000_000, 4096
print(ceil(n_items / n_boxes))               # 245
print(f"load factor = {n_items / n_boxes:.2f}")
print(f"guaranteed to exceed cap {n_boxes * 244}: {n_items > n_boxes * 244}")
```
</details>

**[ ] Exercise 5 — Guaranteed collision.** Show that with 51 requests against 50
cache slots, a collision is forced. What is the smallest number of requests that
forces a collision in 1000 slots?

<details>
<summary>Solution</summary>

With 51 requests and 50 slots, 51 > 50, so by the pigeonhole principle two requests
land on the same slot. The smallest number that forces a collision in 1000 slots is
1001 — with exactly 1000 requests it is *possible* (though not likely) that all are
distinct.

```python
print(51 > 50)                # forced
print(min(m for m in range(1, 5000) if m > 1000))   # 1001
```
</details>

**[ ] Exercise 6 — A classic existence proof.** Prove that among any n + 1
integers there are two whose difference is divisible by n. Show how this becomes a
duplicate-detection guarantee.

<details>
<summary>Solution</summary>

Take the n + 1 integers modulo n. There are only n residue classes, so by the
pigeonhole principle two of the integers are congruent mod n, and their difference
is divisible by n.

For duplicate detection: store each key modulo n in n buckets. Two keys in the same
bucket *might* be equal, but if they differ by a multiple of n they land together —
so bucketing by mod n guarantees that any two keys differing by a multiple of n
are candidates for comparison. This is exactly how hash functions detect that two
values belong to the same bucket before comparing them.

```python
# Three integers from {0..99}; by pigeonhole two are congruent mod n.
def witness(n):
    from itertools import combinations
    for triple in combinations(range(100), 3):
        if any((a - b) % n == 0 for a, b in combinations(triple, 2)):
            return triple, n
    return None

print(witness(3))   # some triple with two congruent mod 3
```
</details>

**[ ] Challenge 7 — Birthday bound via pigeonhole.** With 365 days in a year, how
many people must be present before *some* two share a birthday? Then argue why the
typical number is much smaller (about 23).

<details>
<summary>Solution</summary>

Guaranteed by pigeonhole: 366 people. That is a worst-case statement — it says at
366 people a collision is unavoidable, not that it is likely earlier.

The typical number is ~23 because that is where the collision *probability*
crosses 50%. The probability that all k people have distinct birthdays is

    P(no match) = (365/365)(364/365)(363/365)···(365−k+1)/365)

which for k = 23 is about 0.493, so P(some match) ≈ 0.507. Computing this requires
probability, not pigeonhole — which is why the gap between 366 and 23 is the whole
point of Lesson [70](../part05_probability_statistics/70_information_theory_entropy.md).

```python
from math import ceil

# Pigeonhole: guaranteed at 366.
print(f"guaranteed at: {365 + 1}")

# Birthday probability: first k where P(match) > 0.5.
p = 1.0
for k in range(1, 400):
    p *= (365 - (k - 1)) / 365
    if 1 - p > 0.5:
        print(f"over 50% likely at k = {k}, P(match) = {1 - p:.3f}")
        break
```
</details>

## Summary

- The sum rule fails on overlapping cases; inclusion–exclusion is the fix, with
  signs alternating by subset size.
- The two-set version is |A ∪ B| = |A| + |B| − |A ∩ B|; the general version sums
  over all 2ⁿ − 1 non-empty subsets with sign (−1)^{|S|+1}.
- The general form has 2ⁿ − 1 terms, so it is only useful for small n; beyond that,
  count the complement or use a sieve.
- Surjections onto a k-element set from n inputs number Σ (−1)ʲ C(k,j)(k−j)ⁿ.
- Derangements number !n = n! Σ (−1)ʲ/j!, converging to n!/e.
- Pigeonhole: n + 1 objects in n boxes forces a pair; n objects in k boxes forces
  ⌈n/k⌉ in some box.
- Pigeonhole proves existence without computing anything — that every n has a
  prime factor above it, that any two of n + 1 people share a birthday among 365
  days, that two congruent mod n exist among n + 1 integers.
- Existence is weaker than high probability. The 366-day birthday guarantee is a
  worst case; 23 is a probability statement.

## Next

[Lesson 24 — Recurrence Relations](../part02_discrete_combinatorics/24_recurrence_relations.md) assumes you can
count with confidence and recognise an inclusion–exclusion structure; it turns
"same subproblem, smaller input" into a formula for runtime, which is what makes
algorithm analysis possible.