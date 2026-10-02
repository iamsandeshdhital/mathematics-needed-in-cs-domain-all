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

## Formula Sheet

Every symbol and formula this lesson introduces. `A₁, …, A_n` are finite sets,
`[n] = {1, …, n}` is the index set, `S ⊆ [n]` is a subset of the *indices*, and
`U` is a finite universe of size `|U|`.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| Pairwise disjoint | `$A_i \cap A_j = \emptyset$ for every $i \ne j$` | no element sits in two of the sets | the hypothesis the plain sum rule needs |
| Two-set inclusion–exclusion | `$\lvert A \cup B\rvert = \lvert A\rvert + \lvert B\rvert - \lvert A\cap B\rvert$` | add both, then remove one copy of each doubly-counted element | exactly two overlapping sets; valid always |
| Finite inclusion–exclusion | `$\lvert \bigcup_{i} A_i\rvert = \sum_{\emptyset \ne S \subseteq [n]} (-1)^{\lvert S\rvert+1}\lvert \bigcap_{i\in S} A_i\rvert$` | add singles, subtract pairs, add triples, … | many overlapping sets; the sum runs over the **2ⁿ − 1 non-empty** index subsets |
| Complement form | `$\lvert \bigcap_i \overline{A_i}\rvert = \sum_{S\subseteq[n]} (-1)^{\lvert S\rvert}\lvert \bigcap_{i\in S} A_i\rvert$` | count "none of them", with signs starting the other way | often easier; the empty `S` contributes `$\lvert U\rvert$` |
| Per-element coefficient | `$\sum_{j=1}^{r} (-1)^{j+1} C(r,j) = 1` | an element in exactly `r` sets ends up counted once | **the proof** that the formula is correct; `r ≥ 1` |
| Term count | `$2^{n} - 1$` | how many terms the formula has | 5 sets → 31 terms; 30 sets → 1,073,741,823 |
| Surjections | `$\sum_{j=0}^{k} (-1)^{j} C(k,j)(k-j)^{n}$` | all `$k^n$` functions, minus those missing a target, plus back those missing two | `\|A\| = n`, `\|B\| = k`; `onto(4,3) = 81 − 48 + 3 = 36` |
| Derangements | `$!n = \sum_{j=0}^{n} (-1)^{j} C(n,j)(n-j)! = n!\sum_{j=0}^{n}\dfrac{(-1)^{j}}{j!}$` | permutations with no fixed point | `!5 = 44`, `!6 = 265` |
| Derangement approximation | `$!n \approx n!/e$ | about 36.8% of all permutations move every element | valid for large `n`; `!6/6! = 0.3681` vs `1/e = 0.3679` |
| Pigeonhole (general form) | `n` objects into `k` boxes ⟹ some box holds at least `$\lceil n/k\rceil$` | crowded-box guarantee | the useful form; `⌈100/12⌉ = 9` |
| Pigeonhole (classic form) | `$n+1$` objects into `n` boxes ⟹ some box holds at least 2 | collision guarantee | `366` items, `365` boxes |
| Cap corollary | at most `nc` fit in `n` boxes of capacity `c`; so `n > nc ⟹ ` some box exceeds `c` | contrapositive of the general form | 1000 items, 100 boxes: some bucket holds ≥ 10, but ≥ 11 is **not** forced |
| Load factor | `$n/m$` for `n` items in an `m`-slot table | how full the table is | 1,000,000 items in 2²⁰ slots is 0.954 — over-full, yet nothing bad is *forced* |
| Existence via pigeonhole | for every `n ≥ 2` there is a prime `p > n` | `n! + 1 > 1` has a prime divisor, and every `p ≤ n` divides `n!` | valid for `n ≥ 2`; contains no primality computation |
| Divisibility shortcut | `$A_d \cap A_e = A_{de}$` when `d` and `e` are coprime | intersections are just multiples of the product | worked example: `\|A₂ ∩ A₃\| = \|multiples of 6\| = 16` |
| Worked triple | `$\lvert A_2 \cup A_3 \cup A_5\rvert = 103 - 32 + 3 = 74$` | 50 + 33 + 20 singles, 16 + 10 + 6 pairs, 3 triples | complement in `[1,100]` is `100 − 74 = 26` |
| Symmetric-relation count | `$2^{C(n,2)}$` | each of the `C(n,2)` unordered pairs is an edge or is not | a pigeonhole argument in disguise: with `n+1` people two repeat a degree |
| φ from the degree argument | `$\varphi \approx 1.618` | ratio such that `φ² = φ + 1` | the sizes that maximise how far apart successive turns sit |

---

## Multiple Choice Questions

**Q1.** In `[1, 100]`, how many integers are divisible by 4 **or** by 5?

- A) 45
- B) 40
- C) 25 + 20 = 45
- D) 25 + 20 − 1 = 44

<details>
<summary>Answer and explanation</summary>

**B) 40.**

`|A ∪ B| = |A| + |B| − |A ∩ B|`. There are 25 multiples of 4 and 20 multiples
of 5 up to 100, and their intersection is the multiples of 20, of which there
are 5. So 25 + 20 − 5 = 40.

- A) is the correct arithmetic applied to a wrong overlap: 100/20 = 5, not 1.
- C) is the sum rule applied where the hypothesis fails. Multiples of 4 and 5
  are *not* disjoint — 20, 40, 60, 80 and 100 are in both — which is exactly the
  gap Lesson 20 warns about.
- D) is the same mistake with the overlap counted as a single element instead of
  five. Recognising that `|A ∩ B| = |A_{de}|` for coprime `d, e` is the shortcut
  the worked example uses.

</details>

**Q2.** In `[1, 100]`, `|A₂ ∪ A₃ ∪ A₅|` is 74. What is the correct line of
arithmetic, and why does the two-line version fail?

- A) 103 − 32 = 71; two sets need no triple term
- B) 103 − 32 + 3 = 74; 30 is in all three sets, so the pairs over-subtract it
- C) 103 + 3 = 106; triple intersections are added, never subtracted
- D) 50 + 33 + 20 − 16 − 10 − 6 = 71; pairwise overlaps are enough

<details>
<summary>Answer and explanation</summary>

**B) 103 − 32 + 3 = 74; 30 is in all three sets, so the pairs over-subtract it.**

Singles: 50 + 33 + 20 = 103. Pairs: 16 + 10 + 6 = 32. Triple: 3. The element 30
(also 60 and 90) is counted three times by the singles, subtracted three times by
the three pair terms — it appears in every pair intersection — and so nets
`3 − 3 = 0` until the triple term brings it back to 1. Every element nets exactly
one, which is the theorem.

- A) and D) are the same arithmetic and the same failure: the moment a third set
  is added the formula changes shape. This is Mistake 1 of this lesson. The
  intuition that carries over is "with two sets there are no triples", which is
  true and irrelevant once you have three.
- C) gets the sign pattern backwards. Triple intersections are *added* in the
  union formula and *subtracted* in the complement formula, and C uses the former
  with the latter's signs.

</details>

**Q3.** An element `x` lies in exactly 3 of the sets being combined. What is its
net coefficient in the inclusion–exclusion sum?

- A) 0, because it was counted and subtracted equally often
- B) 1, because `3 − 3 + 1 = 1`
- C) 2, because it survives in two pair intersections
- D) 3, because the singles counted it three times and nothing removed it

<details>
<summary>Answer and explanation</summary>

**B) 1, because `3 − 3 + 1 = 1`.**

The general statement is `Σ_{j=1}^{r} (−1)^{j+1} C(r, j) = 1` for `r ≥ 1`: an
element in exactly `r` sets is counted in `C(r,1)` singles with `+`, in `C(r,2)`
pairs with `−`, in `C(r,3)` triples with `+`, and so on. For `r = 3` the three
coefficients are `C(3,1) = 3`, `−C(3,2) = −3`, `+C(3,3) = +1`, summing to 1.

- A) describes the situation after the pair terms but before the triple term. It
  is the correct diagnosis of *why* the triple term exists — the pairs subtract
  the element once too often — but it is not the final answer.
- C) misapplies `C(3,2) = 3`. The pair *terms* are intersected, so an element in
  three sets appears in all `C(3,2) = 3` of them, and each contributes `−1`.
- D) forgets all the subtraction. The alternating binomial sum equals 1 precisely
  because `(1 − 1)ʳ = 0` kills everything from `j = 2` onwards, leaving the `j = 1`
  term — which is the entire proof that each element nets exactly one.

</details>

**Q4.** How many terms does the finite inclusion–exclusion formula have for `n`
sets, and what does that force?

- A) `n + 1`, so it is practical for any number of sets
- B) `C(n, 2)`, so it stays cheap for large `n`
- C) `2ⁿ − 1`, so 30 sets would need 1,073,741,823 terms and the method is
  unusable there
- D) `2ⁿ`, and the extra term is the empty intersection, which must be dropped

<details>
<summary>Answer and explanation</summary>

**C) `2ⁿ − 1`, so 30 sets would need 1,073,741,823 terms and the method is unusable
there.**

Each of the `n` sets is either in the index subset `S` or not, giving `2ⁿ`
subsets, minus the empty one. For 5 sets that is 31 terms and the formula is
perfectly comfortable; for 30 it is over a billion.

- A) counts the singles and forgets that higher intersections exist. The formula
  for two sets has 2 terms, which is why the mistake is invisible at small `n`.
- B) counts only the pair terms — a formula that is wrong for every `n ≥ 3`,
  because it omits the triple, quadruple and higher corrections that Mistake 2
  of this lesson is about.
- D) has the right base and the wrong constant. The empty subset *is* excluded
  from the union formula, but it is *included* in the complement form, where it
  contributes `|U|`. Both formulas are legitimate; they are different formulas.

</details>

**Q5.** How many functions from a 4-element set to a 3-element set hit every
element of the codomain?

- A) 3⁴ = 81
- B) 81 − 3·2⁴ + 3·1⁴ = 36
- C) 4! = 24
- D) 4³ − 1 = 63

<details>
<summary>Answer and explanation</summary>

**B) 81 − 3·2⁴ + 3·1⁴ = 36.**

The surjection formula `Σ_{j=0..k} (−1)ʲ C(k,j)(k−j)ⁿ` with `n = 4, k = 3` gives
3⁴ − 3·2⁴ + 3·1⁴ − 0⁴ = 81 − 48 + 3 = 36. Read it as: all 81 functions, minus
the 3·16 = 48 that miss one specified target, plus back the 3·1 = 3 that miss two.
The lesson's code checks this against exhaustive enumeration of all 3⁴ = 81
functions and gets 36 both ways.

- A) counts *all* functions, surjective or not. Of the 81, 45 miss at least one
  target.
- C) counts bijections on a 4-element set. A surjection onto 3 elements need not
  be injective at all — the 36 include functions with image sizes 3, 2 and 1 in
  the sense of "misses at most nothing".
- D) subtracts a single function. "Misses at least one target" is a union of
  three overlapping events, and the correction for that is what options B is
  computing.

</details>

**Q6.** What is `!5`, and why is `!n` close to `n!/e`?

- A) `!5 = 120 − 24 = 96`, close to `n!/e` because there are `n!` permutations
- B) `!5 = 44`, close to `n!/e` because `!n = n!·Σ (−1)ʲ/j!` and the partial sum of
  `Σ (−1)ʲ/j!` approaches `1/e`
- C) `!5 = 60`, close to `n!/e` because half of all permutations move the first
  element
- D) `!5 = 44`, close to `n!/e` because `n!` is asymptotically `e^n`, so the
  quotient is asymptotically 1

<details>
<summary>Answer and explanation</summary>

**B) `!5 = 44`, close to `n!/e` because `!n = n!·Σ (−1)ʲ/j!` and the partial sum
of `Σ (−1)ʲ/j!` approaches `1/e`.**

`!5 = Σ_{j=0..5} (−1)ʲ C(5,j)(5−j)! = 120 − 120 + 60 − 20 + 5 − 1 = 44`. Dividing
every term by `5!` collapses the sum to `Σ_{j=0..5} (−1)ʲ/j!`, which is a partial
sum of the alternating series for `1/e`. The lesson's code prints `!6/6! = 0.3681`
against `1/e = 0.3679`.

- A) subtracts one factorial, which is what the *first* two terms do — and they
  cancel. The formula has six terms; two of them is not the formula.
- C) gives 60, which is the `j = 3` term alone. Half of all 5-permutations move
  the first element, but "moves the first element" and "moves *every* element"
  are different conditions, and the second implies the first.
- D) reaches the right approximation for the wrong reason. The quotient
  `!n/n!` tends to `1/e` because the *series* converges, not because `n!` is
  `e^n` (it is not; Stirling's estimate involves `√(2πn)`).

</details>

**Q7.** 100 users sign up in one month, and birth month has 12 values. What does
the pigeonhole principle force?

- A) At least two users share a birth month
- B) Some month holds at least `⌈100/12⌉ = 9` users
- C) Some month holds at least 100/12 = 8.3 users, i.e. 9
- D) Two users share the same birthday, day and month

<details>
<summary>Answer and explanation</summary>

**B) Some month holds at least `⌈100/12⌉ = 9` users.**

The general form — `n` objects in `k` boxes ⟹ some box has at least `⌈n/k⌉` — is
the useful one, and it is the form the engineering statements use. `⌈100/12⌉ = 9`.

- A) is true but is the frozen weak version, and it is Mistake 4 of this lesson:
  the guarantee is about a *crowded* box, not merely a non-empty one. "Some month
  has 9 signups" is actionable; "some month has 2" is not.
- C) rounds 8.3 down to 8 and then says 9 in the same breath. The floor is *not*
  what pigeonhole gives: if every month held at most 8 the total would be at most
  96 < 100. So 9 is forced and 8 is not — the ceiling is exactly the point.
- D) strengthens "month" to "day and month", which is a different and much
  larger box structure. Pigeonhole says nothing about the 365 possible days here.

</details>

**Q8.** A table has 2⁶⁴ slots. What does pigeonhole guarantee?

- A) A collision, because 2⁶⁴ is a large number of slots
- B) Nothing, because items ≤ slots means some items may still be distinct
- C) A collision, provided at least 2⁶⁴ + 1 items are inserted
- D) A collision among any 366 items, as in the birthday argument

<details>
<summary>Answer and explanation</summary>

**C) A collision, provided at least 2⁶⁴ + 1 items are inserted.**

Pigeonhole forces a collision only when items exceed boxes. The lesson's code
prints exactly this contrast: `2^64 slots, 2^64 + 1 items: collision guaranteed
True` and `2^64 slots, 2^64 items: collision guaranteed False (nothing is forced
yet)`.

- A) is Mistake 5 of this lesson in its purest form: it upgrades an existence
  theorem into a claim about the situation you happen to be in. The theorem's
  hypothesis is about items versus boxes, not about how impressive either number
  looks.
- B) is the correct conclusion for `2⁶⁴` items, and it is the honest one. It is
  not "64 bits is safe", though — it is "pigeonhole alone says nothing".
- D) confuses the general form with the birthday argument. 366 items force a
  collision among 365 *days*, not among 2⁶⁴ slots. Reaching 2⁶⁴ + 1 items is not
  necessary in practice because collisions arrive far earlier *with high
  probability* — which is a probability statement, from
  [Lesson 70](../part05_probability_statistics/70_information_theory_entropy.md),
  not a pigeonhole statement.

</details>

**Q9.** The lesson proves "for every `n ≥ 2` there is a prime `p > n`". Which
ingredient does the work?

- A) Computing `n! + 1` and testing divisibility by every prime up to `n`
- B) The fact that every prime `p ≤ n` divides `n!`, so `p | n! + 1` would force
  `p | 1`
- C) The fact that `n! + 1` is itself prime for every `n ≥ 2`
- D) Euclid's algorithm applied to `n!` and `n`

<details>
<summary>Answer and explanation</summary>

**B) The fact that every prime `p ≤ n` divides `n!`, so `p | n! + 1` would force
`p | 1`.**

`n! + 1 > 1` so it has a prime divisor `p`. If `p ≤ n` then `p` is one of the
factors of `n!`, so `p | n!` and `p | (n! + 1)`, hence `p | 1`, a contradiction.
Therefore `p > n`. The proof contains **no computation of any primality** — it is
pure existence, which is the pigeonhole principle's peculiar power.

- A) is what a program would do, and it works; it is just not the proof. The
  lesson's `prime_divisor_of_factorial_plus_one` does exactly that, and its value
  is that it *finds* the prime, whereas the theorem only asserts one exists.
- C) is false, and famously so: `n = 4` gives `4! + 1 = 25 = 5²`. Nothing here
  requires `n! + 1` to be prime, only that some prime divides it — every integer
  above 1 has a prime divisor.
- D) applies a different theorem. Euclid's *algorithm* on a pair of integers
  finds a gcd; the argument above is a divisibility contradiction and would still
  work if `n! + 1` had a huge number of prime factors.

</details>

**Q10.** A cache has 100 buckets and receives 1,000 requests. Which statement does
pigeonhole justify?

- A) Some bucket receives at least 11 requests
- B) Some bucket receives at least 10 requests, and nothing forces 11
- C) Exactly 10 requests land in some bucket
- D) Some bucket receives at most 10 requests

<details>
<summary>Answer and explanation</summary>

**B) Some bucket receives at least 10 requests, and nothing forces 11.**

`⌈1000/100⌉ = 10`, so some bucket holds at least 10. The cap form says more: if
every bucket held at most 9, at most 900 would fit, and 1,000 > 900 — so 9 is
exceeded. If every bucket held at most 10, at most 1,000 would fit, which does
not contradict anything. The lesson's code makes both checks:
`cap 9 -> must exceed: True` and `cap 10 -> must exceed: False`.

- A) is the over-strong reading. To force 11 you would need more than 1,000
  requests, since 100 buckets holding ≤ 10 each accommodate exactly 1,000.
- C) confuses a lower bound with an equality. The guarantee is one crowded bucket;
  the requests could be distributed 1,000, 0, 0, … and still satisfy it.
- D) reverses the direction of the conclusion entirely. Pigeonhole forces
  *crowding*; that a bucket receives at most 10 is false in general and true for
  a different reason (the total is 1,000).

</details>

---

## Subjective Questions

### Short Answer

**Q1. State the two-set inclusion–exclusion formula, and explain what the minus
sign is doing.**

<details>
<summary>Answer</summary>

$$\lvert A \cup B\rvert = \lvert A\rvert + \lvert B\rvert - \lvert A \cap B\rvert$$

`|A| + |B|` counts every element of `A ∪ B` at least once and every element of
`A ∩ B` exactly twice. Elements outside the union are not counted at all.
Subtracting `|A ∩ B|` removes one spurious copy of each doubly-counted element
and none of the correctly-counted ones. That is the whole reason for the minus
sign: it is a correction for double counting, not an average or a probability.

</details>

**Q2. State the finite inclusion–exclusion formula and the complement form, and
say where they differ.**

<details>
<summary>Answer</summary>

Union form, for finite `A₁, …, A_n`:

$$\lvert \bigcup_{i=1}^{n} A_i\rvert = \sum_{\emptyset \ne S \subseteq [n]} (-1)^{\lvert S\rvert+1}\, \lvert \bigcap_{i\in S} A_i\rvert$$

Complement form, for the same sets inside a universe `U`:

$$\lvert \bigcap_{i=1}^{n} \overline{A_i}\rvert = \sum_{S\subseteq[n]} (-1)^{\lvert S\rvert}\, \lvert \bigcap_{i\in S} A_i\rvert$$

They differ in two ways. The complement form ranges over **all** subsets of
`[n]` including the empty one, and the empty intersection is `U`, so the `j = 0`
term is `|U|`; the union form omits it. And the signs are shifted by one, because
one formula counts the bad ones and the other their complement.

</details>

**Q3. State the surjection formula and explain where each factor comes from.**

<details>
<summary>Answer</summary>

For `|A| = n` and `|B| = k`, the number of functions hitting every element of `B`
is

$$\sum_{j=0}^{k} (-1)^{j} C(k,j)(k-j)^{n}$$

Start with all `kⁿ` functions. Let `B_j` be the set of functions whose image misses
element `j`; we want the complement of the union of the `B_j`. Applying the
complement form of inclusion–exclusion gives `Σ (−1)ʲ Σ_{|S|=j} |∩ B_i|`. There
are `C(k, j)` ways to choose `S`, and each intersection has `(k − j)ⁿ` members,
because each input may map to any of the `k − j` allowed targets.

</details>

**Q4. State the derangement formula in both its forms, and say why the second
form exists.**

<details>
<summary>Answer</summary>

$$!n = \sum_{j=0}^{n} (-1)^{j} C(n,j)(n-j)! \qquad = \qquad n!\sum_{j=0}^{n}\frac{(-1)^{j}}{j!}$$

The first is the complement form with `B_j` = permutations fixing `j`. The second
exists because `C(n,j)(n−j)! = n!/j!`, so every term divided by `n!` collapses to
`(−1)ʲ/j!` and the sum factors. That collapse is also the explanation of the
approximation `!n ≈ n!/e`: the partial sum of the alternating series
`Σ (−1)ʲ/j!` approaches `1/e`.

</details>

**Q5. State the pigeonhole principle in its general form, and state the cap
corollary that follows from it.**

<details>
<summary>Answer</summary>

**General form.** If `n` objects are placed into `k` boxes, some box contains at
least `⌈n/k⌉` objects.

**Cap corollary.** If each of `n` boxes holds at most `c` objects, then at most
`nc` objects fit. So if you have more than `nc` objects, some box exceeds `c`.

This is the contrapositive of the general form, and it is the form you alert on:
"some bucket holds at least 10" is the load-factor guarantee, while "some bucket
holds at least 11" needs more than `nc` items and is not available at exactly
`nc`.

</details>

**Q6. Prove that for every `n ≥ 2` there is a prime `p > n`, without computing any
primality test.**

<details>
<summary>Answer</summary>

Consider `n! + 1`. It is larger than 1, so it has a prime divisor `p`. Now
`n! = 1 · 2 · … · n`, so every prime `p ≤ n` divides `n!`. If `p` also divided
`n! + 1`, then it would divide their difference, which is 1 — impossible. Hence
`p > n`.

The argument is pure existence. It never decides whether `n! + 1` is prime (for
`n = 4` it is 25 = 5²), and it never tests a candidate: it only asserts that a
prime factor exists and that it must be large.

</details>

### Long Answer

**Q1. Why does inclusion–exclusion actually work? What would break if the signs
did not alternate, and how does the per-element argument show they must?**

<details>
<summary>Model answer</summary>

The whole theorem reduces to one claim: that an element belonging to exactly `r`
of the sets has net coefficient 1 in the sum, and an element belonging to none has
net coefficient 0. Because the formula is a sum of cardinalities of
intersections, and an element contributes 1 to `|∩_{i∈S} A_i|` precisely when it
lies in every set of `S`, you can compute each element's coefficient separately —
and then check the whole theorem at once.

For an element in exactly `r` sets, the total coefficient is
`Σ_{j=1}^{r} (−1)^{j+1} C(r, j)`. The binomial theorem with `a = 1, b = −1` gives
`Σ_{j=0}^{r} (−1)ʲ C(r,j) = (1−1)ʳ = 0` for `r ≥ 1`, so the terms from `j = 2`
onward sum to `−C(r,0) = −1`, leaving `+1`. For `r = 0` no term includes the
element at all, so its coefficient is 0. Done: every element of the union is
counted once and every other element zero times, hence the formula equals the
union's size.

This also explains what breaks if the signs do not alternate. The correction
process is self-defeating unless each term undoes exactly the error the previous
one introduced. An element in 3 sets is over-counted by 2 by the singles, so the
pair terms must remove 3 to overshoot by exactly 1, so the triple term must
restore 1. Get the pattern wrong — all signs positive, say — and you get `2ʳ − 1`
contributions for an element in `r` sets, which grows exponentially and is not a
count of anything. Get the third sign wrong (subtract the triple) and every
element in three sets nets `3 − 3 − 1 = −1`: you would be counting the union and
subtracting a correction for it at the same time.

The practical lesson is that "add singles, subtract pairs, add triples" is not a
pattern to memorise from the first two cases. It is forced by the requirement
that one term cancel the previous term's error, and the per-element argument is
the proof. This is exactly the argument the lesson runs through by hand on the
worked example, checking that 30 nets `3 − 3 + 1 = 1`, that 6 nets `2 − 1 = 1`,
and that 100 nets `2 − 1 = 1`.

</details>

**Q2. When must you stop using inclusion–exclusion and switch to the complement?
What exactly is the failure mode, and why does it fail silently?**

<details>
<summary>Model answer</summary>

The failure mode is the term count: `2ⁿ − 1`. The formula is *correct* for any
number of sets, so there is never a moment at which it is obviously wrong. It
simply stops being finishable. Five sets cost 31 terms, which is nothing. Twelve
sets cost 4,095. Twenty sets cost about a million. Thirty sets cost
1,073,741,823, and the correct answer is sitting there in the formula while no
program will produce it in your lifetime. This is Mistake 3 of the lesson, and its
danger is precisely the correctness: there is no crash, no negative number, no
sanity check that fires. The result is right in principle and absent in practice.

The switch is to the complement. "How many satisfy at least one of these
constraints" is often far harder than "how many satisfy none of them", because the
"none" version frequently decomposes — it is exactly what you can count with a
product rule, a bijection, or a recurrence. The lesson's worked example shows the
extreme: the same 74 either way, but the complement `100 − 103 + 32 − 3 = 26`
frames the count as "the integers coprime to 30 up to 100", which has an order of
magnitude you can check against `φ(30)/30 × 100 ≈ 26.7`.

Two more honest exits, and both are legitimate:

- **Recognise the closed form.** Surjections have one; derangements have one and a
  good approximation. So do onto-mappings with `!n`-style recurrences, and
  bipartite graphs by the `C(m+n-2, n-1)` bijection of König's theorem. Finding
  the bijection is the work, and the formula is then free.
- **Change the question.** If the exact count is hopeless, sample. The lesson's
  birthday-bound analysis is the model: exact inclusion–exclusion over the
  `C(n,2)` pairwise collision events has `2^C(n,2)` terms, hopeless from `n = 6`
  upwards, and a twenty-thousand-trial sample gives a usable number in a fixed
  budget. Saying "I need an estimate, not a count" is a legitimate answer, not a
  retreat.

The habit worth forming is to compute the term count *before* you commit, and to
state the scope of whatever number you end up with — an approximation labelled as
an approximation is checkable by anyone, and an exact count you cannot compute is
not a result at all.

</details>

**Q3. The pigeonhole principle proves things exist without telling you how to
find them. Why is that limitation a feature rather than a defect, and what can and
cannot be concluded from it?**

<details>
<summary>Model answer</summary>

Because the questions it is used on are questions about *whether* something
happens, not about which something. "Do two of these values collide?" is a yes/no
question about the system. The engineer needs to know a collision is inevitable so
they can budget for it; they do not need the colliding pair, and by the time they
do need it, the table implementation has already found it. The theorem supplies
exactly the half of the answer that a structural argument can supply, and leaves
the other half to the data.

It is a feature for a second reason. Its proof is a one-line contradiction — if
every box held at most one object the boxes would hold at most `n`, contradicting
`n + 1` — and that proof generalises to situations where no counting argument is
available. The prime-existence theorem contains no primality test at all. It
contains no computation of `n! + 1`'s factors, no sieve, no trial division; it
only observes that `n!` is divisible by everything below `n` and that `n! + 1` is
bigger than 1. That is a kind of statement arithmetic alone cannot make, and it is
the reason the technique appears in proofs where computation is useless.

What it cannot do is give probabilities, and the distinction is worth keeping
sharp. With `2⁶⁴` slots, pigeonhole forces a collision only once `2⁶⁴ + 1` items
are inserted. It says nothing at all about 366 items — yet in practice collisions
are overwhelmingly likely long before that, because with many items and many
boxes there are many chances for the pigeonhole to be the pair that lands
together. That is the birthday argument, a probability statement needing
[Lesson 70](../part05_probability_statistics/70_information_theory_entropy.md), and
the lesson's Mistake 5 is exactly the error of reading it back out of this lesson.
"The words 'there exists' sound stronger than 'with high probability', and it is
easy to upgrade an existence theorem into a probability claim without noticing."

The second thing it cannot do is *design*. `⌈n/k⌉` is a lower bound on the worst
bucket, and a guarantee about the worst case says nothing about the typical case.
A hash function that maps all `n` keys into one bucket satisfies pigeonhole
exactly and is useless in production; a near-uniform one has the same worst case.
The lesson makes this point in the opposite direction too: the table with load
factor below 1 is *fine*, and the alert threshold should sit above what pigeonhole
forces — 1,000 items in 100 buckets guarantees 10, but you page someone at 11, not
at 10, because 10 is information rather than trouble.

</details>

**Q4. Why does a hash table with load factor below 1 still suffer collisions, and
what does the load-factor bound actually buy you?**

<details>
<summary>Model answer</summary>

Because pigeonhole constrains the *worst* bucket and almost nothing else. A table
with `m` slots receiving `n < m` items admits a placement where one bucket holds
`⌈n/m⌉ = 1` item and the rest hold zero — that satisfies the principle perfectly.
But it also admits a placement where one bucket holds all `n`. Pigeonhole cannot
rule that out, and it certainly cannot rule it out for a *particular* hash
function: the theorem is about any placement whatsoever, so it is silent about
the placement your hash function actually produces. Collisions in practice are
decided by how close to uniform the function is, which is a statistical property
and needs the birthday analysis, not this lesson.

So what does the bound buy? Three things, and they are real.

It certifies that the *average* bucket is not a catastrophe. `n/m` is the mean
occupancy by construction — the total is `n` spread over `m` buckets — and a mean
of 1 is a mean, not a worst case. Choosing `m` with `n/m` bounded by a small
constant keeps the expected number of probes per lookup bounded, which is the
entire basis of expected `O(1)` lookup.

It tells you where the *forced* trouble starts, so you can separate information
from alarm. Pigeonhole says some bucket holds at least `⌈n/m⌉`. At load factor
0.954 — 1,000,000 items in 2²⁰ slots — that is 1, and it means nothing. But push
past `n = m` and the guarantee jumps to 2, and past `2m` to 3: there is a genuine
phase change at each integer multiple, and it is exactly at those multiples that
resizing stops being optional. Sizing the table at `n = m` therefore buys you a
factor of 2 in collision probability for free relative to `n = m/2`, and the
arithmetic to see that is one line.

And it bounds the worst case, which is not nothing. Even with a perfect hash
function, some bucket holds `⌈n/m⌉` items, so a lookup must in the worst case scan
that bucket's chain. The bound is what lets you write a worst-case bound at all:
`O(⌈n/m⌉)` probes, which is `O(1)` exactly when the load factor is bounded and a
constant. Without pigeonhole you would have no bound to write, because "the hash
function is usually good" is not a complexity claim.

</details>

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