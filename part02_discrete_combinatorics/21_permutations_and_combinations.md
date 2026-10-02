# 21 — Permutations, Combinations, and Choosing With Limits

**Part**: part02_discrete_combinatorics · **Prerequisites**: 20 · **Time**: 35 min

---

## In Plain Words

You have already met the two rules that generate every counting formula in this
part. This lesson turns them into named tools, and — more importantly — gives
you a decision procedure for picking the right one.

Two words do all the work. Does **order matter**? Are **repeats allowed**? Those
two yes/no questions put any counting problem into exactly one of four boxes:

- Order matters, repeats allowed: each of the *r* slots picks freely from *n*
  things, so you get n raised to the power r. Strings, passwords, functions.
- Order matters, no repeats: you fill the first slot *n* ways, the second *n* − 1
  ways, and so on. Call it nPr. Timetables, execution orders, PINs from distinct
  digits.
- Order does not matter, no repeats: the "divide by the rearrangements"
  version. Call it nCr. Committees, handshakes, test selections.
- Order does not matter, repeats allowed: the number of ways to pick 3 flavours
  of ice cream from 6 flavours, where you can pick the same one twice. This is
  the one nobody remembers, and its answer is a trick: pretend the repeats are
  extra distinct objects.

The one-sentence decision rule is this. **If swapping two of the chosen items
gives a different answer, order matters.** "Choose Alice and Bob for the review"
— swapping them changes nothing, so nCr. "Rank Alice above Bob" — swapping
changes the answer, so nPr.

The final topic is choosing with limits: you may take at most two of each kind
of thing. That sounds fiddly, but it has a clean mechanical answer. For each
kind of thing, write down the list of ways to take 0, 1, or 2 of it. Multiply
the lists together like polynomials, and the coefficient of the term for "total
k" is your answer. No case analysis required.

## Why Computer Science Cares

- **nCr(n, 2) is the cost of pairwise comparison.** C(n, 2) = n(n − 1)/2 is the
  number of edges in a complete graph, the number of comparisons bubble sort
  performs, and the number of collisions a naive nearest-neighbour search
  checks. Whenever you see "compare everything against everything", that
  formula is the runtime.
- **Choosing a replica set.** Picking 3 healthy servers from a pool of 20 is
  C(20, 3) = 1,140 — the size of the action space a combinatorial-bandit
  scheduler must reason about. Choosing 3 *and ordering them as a failover
  priority* is P(20, 3) = 6,840, six times bigger.
- **Bootstrap and random forests.** The bootstrap resamples *with* replacement:
  every one of the n draws has n options, so there are nⁿ possible resamples, and
  the number of *distinct* multisets that can appear is C(2n − 1, n). Both
  formulas show up when you reason about how much diversity a forest can have.
- **Exhaustive subset search.** Enumerating every k-subset of n items to find the
  best-scoring one is C(n, k) states, which is why k-means++ and beam search cap
  k and use sampling instead. Lesson [82](../part06_algorithms_math/82_tools_for_algorithm_design.md)
  returns to this.
- **Bitmask indexes.** Storing a subset as an n-bit integer is the *bijection*
  from Lesson [20](../part02_discrete_combinatorics/20_counting_principles.md) in disguise, and it is why `1 << n`
  appears in database and compiler code constantly.
- **Anagram solvers and test-data generators.** Counting the distinct
  arrangements of a word with repeated letters is a multiset permutation, and
  11!/(4!4!2!) = 34,650 is the number of distinct arrangements of MISSISSIPPI —
  a number small enough to search, which is exactly why it is a favourite
  interview question.

## The Formal Version

Symbols follow [SYMBOLS.md](../SYMBOLS.md). For finite A we write |A| = n and
choose r ≤ n items.

**Definition.** An *r-permutation* of A is a sequence (a₁, …, a_r) of **distinct**
elements of A. The set P(A, r) of r-permutations has size

    P(n, r) = n! / (n − r)!  =  n(n − 1) ⋯ (n − r + 1)

**Definition.** An *r-combination* of A is an r-element subset of A. The set
C(A, r) of r-combinations has size

    C(n, r) = n! / (r! (n − r)!)

**Theorem (P from C).** P(n, r) = C(n, r) · r! for r ≤ n.

*Explanation.* Fix an r-element subset S. Every ordering of S is a valid
r-permutation using exactly the elements of S, and there are r! of them
(the product rule over the r positions). So the r-combinations partition P(A, r)
into classes of size r!, and dividing by the class size gives the count. This is
the formal version of "order matters, so multiply by the rearrangements", and it
is why the answer to "does order matter?" is worth 20 minutes of thought.

**Definition.** A *combination with repetition* (a multiset) is a way to choose r
items from A allowing repeats, where two choices are the same if they use the
same items with the same multiplicities. Its count is

    C(n + r − 1, r) = C(n + r − 1, n − 1)

**Explanation (stars and bars).** Write r stars and n − 1 bars. Each bar
separates one kind of item from the next, so the stars before the first bar are
"how many of kind 1", and so on. A choice maps to exactly one bar pattern and
back, so this is a bijection; the patterns are strings of length n + r − 1 with
n − 1 distinguished bars, hence C(n + r − 1, n − 1).

**Definition.** A *multiset permutation* is an ordering of a multiset with
multiplicities k₁, …, k_m summing to n. Its count is

    n! / (k₁! k₂! ⋯ k_m!)

**Explanation.** Start from all n! orderings of the labelled copies, then divide
by the kᵢ! ways of permuting each group of identical copies — each distinct
arrangement is counted k₁! ⋯ k_m! times.

**Theorem (Pascal's recursion).** C(n, r) = C(n − 1, r − 1) + C(n − 1, r), with
C(n, 0) = C(n, n) = 1 and C(n, r) = 0 for r > n.

*Explanation.* Partition the r-subsets of an n-set by whether they contain a
fixed element. Those that do: choose the remaining r − 1 from n − 1. Those that
do not: choose all r from n − 1. The two cases are disjoint and exhaustive, so
the sum rule applies. This is the dynamic-programming form used in
[Lesson 24](../part02_discrete_combinatorics/24_recurrence_relations.md).

**Theorem (Symmetry and special values).** C(n, r) = C(n, n − r), C(n, 1) = n,
C(n, 0) = 1, and C(n, 2) = n(n − 1)/2.

*Explanation.* The symmetry has a bijection: take the complement inside A. C(n, 2)
is the count of unordered pairs, equivalently of edges of a complete graph, and
is the single most useful special case in computer science.

**Theorem (Choosing with limits).** Suppose there are m kinds of item, kind *i*
allowing at most cᵢ copies. The number of unordered selections totalling r items
is the coefficient of xʳ in

    (1 + x + x² + ⋯ + x^{c₁})(1 + x + ⋯ + x^{c₂}) ⋯ (1 + ⋯ + x^{c_m})

The number of *ordered* selections with the same limits is

    Σ over (k₁ + ⋯ + k_m = r, 0 ≤ kᵢ ≤ cᵢ) of r! / (k₁! ⋯ k_m!)

**Explanation.** Expanding the first factor, you choose a term x^{k₁} from it;
the product term you land on is x^{k₁ + k₂ + ⋯ + k_m}. Collecting all terms of
degree r counts each valid multiplicity vector once. The ordered count multiplies
each vector by its multinomial coefficient from the previous definition.

## Worked Example

**The situation.** A test suite has 6 tests: A, B, C, D, E, F. You must build a
compact test manifest. Answer four questions about it, and label each with the
tool that applies.

**Q1 — Which 3 tests run?** The report lists them as a set; order carries no
meaning. Order does not matter, no repeats, so:

    C(6, 3) = 6! / (3! · 3!) = 720 / 36 = 20

Computed without factorials, the multiplicative form is 6 · 5 · 4 / (1 · 2 · 3) =
120/6 = 20. Same number, no 720 involved.

**Q2 — In what order do they run?** Now the manifest is a schedule: ABC and ACB
are different artifacts. Order matters, no repeats:

    P(6, 3) = 6 · 5 · 4 = 120

**Q3 — Why exactly six times bigger?** The theorem above answers this: for each
of the 20 chosen sets there are 3! = 6 orderings, and 20 · 6 = 120. This is the
step people skip. If your nPr answer is not r! times your nCr answer, you have
made an error, and this is the cheapest possible self-check.

**Q4 — "Test A must not be last."** A constraint, so we subtract. All 4-long
schedules:

    P(6, 4) = 6 · 5 · 4 · 3 = 360

Schedules with A in the final slot: fix A there, and fill the first three slots
with distinct tests from the remaining five, in order:

    5 · 4 · 3 = 60

    360 − 60 = 300

Note the subtlety that makes this correct: when A occupies slot 4 the *other*
slots have 5, 4, 3 options, not 6, 5, 4. Fixing one position removes that test
from the pool. This "fix a position, then count the rest" move works for
permutations but not for combinations — for combinations, "A is in the set" is
C(5, 2), not 5 · 4, precisely because the other members are unordered.

**Q5 — A repetition case, for practice.** Group the tests as {A,B}, {C,D},
{E,F} and allow at most 2 from each group, choosing 5 tests total. Caps are
(2, 2, 2), total is 5. Expand:

    (1 + x + x²)(1 + x + x²)(1 + x + x²)

Picking terms of degree 5 means multiplicities summing to 5 with each at most 2,
so the pattern is (2, 2, 1) in some order — 3 arrangements, one per choice of
which group contributes 1. The coefficient of x⁵ is 3.

If the manifest were an *ordered* schedule instead, each (2,2,1) pattern gives
5!/(2!2!1!) = 30 orderings, so 3 · 30 = 90. Same multisets, six times as many
schedules per multiset on average (5!/2!2!1! divided appropriately).

## Runnable Code

The four formulas, written both ways: by hand so you see the machinery, then with
the standard library.

```python
from collections import Counter
from math import comb, perm, factorial

def nCr(n, r):
    """C(n, r): choose r from n, order irrelevant.

    Multiplicative form n(n-1)...(n-r+1) / r! keeps every intermediate value an
    integer, so it never builds n! the way the naive formula does."""
    if r < 0 or r > n:
        return 0
    r = min(r, n - r)  # C(n, r) == C(n, n-r): take the shorter loop
    total = 1
    for i in range(r):
        total = total * (n - i) // (i + 1)  # exact: total is C(n, i+1) here
    return total

def nPr(n, r):
    """P(n, r): order r distinct items from n. A falling product, no division."""
    total = 1
    for i in range(r):
        total *= n - i
    return total

def multiset_pr(elements):
    """Orderings of a multiset: n! / (k1! k2! ... ). Each partial division is a
    product of binomial coefficients, so integer division stays exact."""
    counts = Counter(elements)
    total = factorial(len(elements))
    for k in counts.values():
        total //= factorial(k)
    return total

print(f"C(6,3) by hand {nCr(6,3):4d}  math.comb {comb(6,3):4d}")
print(f"P(6,3) by hand {nPr(6,3):4d}  math.perm {perm(6,3):4d}")
print(f"C(10,5) = {nCr(10,5):6d}  = {comb(10,5):6d}")
print(f"P(10,5) = {nPr(10,5):8d}  = {perm(10,5):8d}")
print(f"factorial(20) = {factorial(20)}")
print(f"P(n,r) / C(n,r) = r!  ->  {nPr(8,4)} / {nCr(8,4)} = {nPr(8,4)//nCr(8,4)} = {factorial(4)}")
```

Pascal's recursion — combinations computed the dynamic-programming way, checked
against brute-force enumeration of actual subsets.

```python
from itertools import combinations

def pascal_row(n):
    """Row n of Pascal's triangle, built by C(n, r) = C(n-1, r-1) + C(n-1, r)."""
    row = [1]
    for _ in range(n):
        # every interior entry is the sum of the two above it
        row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]
    return row

A = "ABCDEF"
n = len(A)
by_dp = [pascal_row(n)[r] for r in range(n + 1)]
by_brute = [
    len(list(combinations(A, r))) for r in range(n + 1)
]
print("C(6, r) via Pascal recursion:", by_dp)
print("C(6, r) via enumeration    :", by_brute)
print("agree:", by_dp == by_brute)
print("row 10 of Pascal:", pascal_row(10))
print(f"sum of row 10 = {sum(pascal_row(10))} = 2^10 = {2**10}")
```

The two easy-to-forget cases: repetition allowed, and repeated items ordered.

```python
from collections import Counter
from math import comb, perm, factorial

# Choose 3 flavours from 6, repeats allowed: C(n + r - 1, r).
print(f"3 scoops from 6 flavours      : {comb(6 + 3 - 1, 3)}")
print(f"  (strips and bars: {comb(8, 7)} by the other form)")

# Anagrams of a word with repeated letters.
word = "MISSISSIPPI"
counts = Counter(word)
label = ", ".join(f"{c}x{letter}" for letter, c in sorted(counts.items()))
raw = factorial(len(word))
for c in counts.values():
    raw //= factorial(c)
print(f"{word} ({label}): {raw} distinct arrangements")
print(f"  math.perm(11,11) would be {perm(11,11)} - far too big to be right")

# Why the division is sound: the multiset count is a product of binomials.
print(f"  C(11,4)*C(7,4)*C(3,2) = {comb(11,4)*comb(7,4)*comb(3,2)}")
```

Choosing with limits, solved by polynomial coefficient extraction. The caps are
the only input.

```python
from itertools import product as iproduct
from math import factorial

def bounded_selections(caps, total):
    """Unordered selections of `total` items taking at most caps[i] of each kind.

    Coefficient of x^total in prod(1 + x + ... + x^caps[i]).

    Implementation: keep the coefficient list of the polynomial built so far and
    multiply by the next factor with the schoolbook rule."""
    coeffs = [1]  # coefficients of the empty product, which is 1
    for cap in caps:
        nxt = [0] * (len(coeffs) + cap)
        for degree, c in enumerate(coeffs):
            for take in range(cap + 1):  # term x^take from 1 + x + ... + x^cap
                nxt[degree + take] += c
        coeffs = nxt
    return coeffs[total]

def brute_vectors(caps, total):
    """Count the same thing by listing every valid multiplicity vector."""
    count = 0
    for vec in iproduct(*[range(c + 1) for c in caps]):
        if sum(vec) == total:
            count += 1
    return count

print(f"caps (2,2,2), total 5 -> {bounded_selections([2,2,2], 5)} (brute force {brute_vectors([2,2,2], 5)})")
print(f"caps (2,2,2), total 4 -> {bounded_selections([2,2,2], 4)} (brute force {brute_vectors([2,2,2], 4)})")
print(f"caps (1,3,2), total 5 -> {bounded_selections([1,3,2], 5)} (brute force {brute_vectors([1,3,2], 5)})")
print("full table for caps (2,2,2), totals 0..6:",
      [bounded_selections([2, 2, 2], t) for t in range(7)])

# Ordered version: each multiplicity vector contributes its multinomial count.
def bounded_ordered(caps, total):
    ways = 0
    for vec in iproduct(*[range(c + 1) for c in caps]):
        if sum(vec) != total:
            continue
        perms = factorial(total)
        for k in vec:
            perms //= factorial(k)
        ways += perms
    return ways

print(f"ordered, caps (2,2,2), total 5 -> {bounded_ordered([2,2,2], 5)}")
```

A worked reference table of classic problems. Every number here comes from the
functions above, so this doubles as a lookup table you can extend.

```python
from math import comb, perm, factorial

problems = [
    ("handshakes among 8 people",            lambda: comb(8, 2)),
    ("3 servers chosen from 20",             lambda: comb(20, 3)),
    ("same 3, given failover priority order", lambda: perm(20, 3)),
    ("8-bit strings of weight exactly 3",    lambda: comb(8, 3)),
    ("6-char lowercase strings",             lambda: 26**6),
    ("6-char strings, repeats allowed",      lambda: comb(6 + 6 - 1, 6)),
    ("2 rooks placed on a 8x8 board",        lambda: comb(64, 2)),
    ("8-letter arrangements of AABBCCDD",    lambda: factorial(8) // factorial(2) ** 4),
    ("committees of 2 or 3 from 10 people",  lambda: comb(10, 2) + comb(10, 3)),
    ("bootstrap multisets from 10 items",   lambda: comb(19, 10)),
]
for label, f in problems:
    print(f"  {label:38s} {f():>14,}")
```

## Common Mistakes

**1. Using nPr when order does not matter.**

> Wrong: "Pick 2 of 5 servers as a replica pair: 5 · 4 = 20."
> Right: C(5, 2) = 10. {A,B} and {B,A} are the same pair.
> Why the wrong one is tempting: the product rule is the first counting tool you
> learned, so it is the default. The 2× overcount here is exactly r! = 2, and it
> grows as (5 choose 2) → (5 choose 3) blows the error up to 6×.

**2. Using nCr when order matters.**

> Wrong: "How many 3-digit PINs with distinct digits? C(10, 3) = 120."
> Right: P(10, 3) = 720. PIN 123 and PIN 321 are different PINs.
> Why the wrong one is tempting: "choosing digits" sounds like choosing. Look for
> the words rank, order, sequence, schedule, PIN, path, password — each of those
> means swapping two choices changes the answer.

**3. Forgetting repetition in combinations with repetition.**

> Wrong: "3 scoops from 6 flavours with repetition allowed: C(6, 3) = 20."
> Right: C(6 + 3 − 1, 3) = C(8, 3) = 56.
> Why the wrong one is tempting: you carry the nCr muscle memory from the
> no-repeats case. The fix is to ask "can the same thing appear twice?" — if yes,
> the formula changes and the new top argument is n + r − 1.

**4. Dividing by the wrong factorial for repeated items.**

> Wrong: "MISSISSIPPI has 4 S's, 4 I's and 2 P's, so 11!/4! = 1,663,200."
> Right: 11!/(4!·4!·2!) = 34,650.
> Why the wrong one is tempting: dividing once feels like it should capture "the
> repeats". It captures only the first group. Divide once per *distinct* letter,
> because each group of identical copies can be permuted in k! ways that produce
> the same visible arrangement.

**5. Hand-rolling factorials for large n.**

> Wrong: `def C(n, r): return factorial(n) // (factorial(r) * factorial(n-r))` on
> n = 1000 — and then also writing this in a hot loop.
> Right: use `math.comb(n, r)`, or the multiplicative form with `r = min(r, n-r)`.
> Why the wrong one is tempting: the factorial formula is the pretty one, and it
> *does* work for n = 20. It breaks at n ≈ 1000 where 1000! has 2568 digits, and
> it is O(n) instead of O(min(r, n−r)). `math.comb` is C-implemented and does
> the division more carefully than you will.

---

## Formula Sheet

Every symbol and formula this lesson introduces. `n` is the size of the pool, `r`
is how many items are selected, `k₁, …, k_m` are multiplicities with
`k₁ + ⋯ + k_m = n`, and `cᵢ` is the cap on copies of kind `i`. All counts are
exact integers.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `P(n, r)` | `$P(n,r) = n!/(n-r)! = n(n-1)\cdots(n-r+1)$` | order `r` **distinct** items from `n`: the choice set shrinks at every step | timetables, schedules, PINs from distinct digits |
| `C(n, r)` | `$C(n,r) = n!/\bigl(r!\,(n-r)!\bigr)$` | `r`-element **subset** of an `n`-element set; order irrelevant | committees, handshakes, test selections |
| P from C | `$P(n,r) = C(n,r)\cdot r!$` | every chosen set has exactly `r!` orderings | the cheapest self-check on any nCr/nPr pair |
| Multiplicative `C(n,r)` | `$C(n,r) = n(n-1)\cdots(n-r+1)\,/\,r!$` | multiply the falling factorial, divide by `r!`; every intermediate is an integer | when you want the machinery visible, or `n!` is too big to build |
| Shrinking the loop | `C(n,r) = C(n,r')` with `$r' = \min(r,\,n-r)$` | the shorter of the two loops, using the symmetry | turning an `O(n)` computation into `O(min(r, n−r))` |
| Combination with repetition | `$C(n+r-1,\;r) = C(n+r-1,\;n-1)$` | unordered selection of `r` from `n` with repeats allowed | 3 scoops from 6 flavours: $C(8,3) = 56$ |
| Stars and bars | `$r$ stars and $n-1$ bars` | each bar separates one kind from the next; the stars before a bar are that kind's multiplicity | the bijection proving the formula above |
| Multiset permutation | `$n!/\bigl(k_1!\,k_2!\cdots k_m!\bigr)$` | orderings of `n` objects with multiplicities `k₁, …, k_m`; divide once per *distinct* item | MISSISSIPPI: $11!/(4!\,4!\,2!) = 34{,}650$ |
| Pascal's recursion | `$C(n,r) = C(n-1,r-1) + C(n-1,r)$` | split the `r`-subsets of an `n`-set by whether they contain one fixed element | the dynamic-programming form of the same subsets |
| Pascal base cases | `$C(n,0) = C(n,n) = 1$; `$C(n,r) = 0$ for `$r > n$` | the empty selection and the whole set are each unique; out-of-range is zero | stopping the recursion; keeps the DP table rectangular |
| Symmetry | `$C(n,k) = C(n,k')` with `$k' = n-k$` | take the complement inside the `n`-set | explains why $C(20,7) = C(20,13) = 77{,}520$ |
| `C(n, 1)` | `$C(n,1) = n$` | one item from `n` is just `n` choices | sanity checks |
| `C(n, 2)` | `$C(n,2) = n(n-1)/2$` | unordered pairs = edges of a complete graph = pairwise comparisons | `C(9,2) = 36` handshakes; the cost of compare-everything |
| Choosing with limits (unordered) | `$\bigl[x^{r}\bigr]\prod_{i=1}^{m}(1 + x + \cdots + x^{c_i})$` | expand the product and read off the coefficient of `x^r` | "at most 2 of each of 3 kinds, take 5 in total" gives 3 |
| Choosing with limits (ordered) | `$\sum_{k_1+\cdots+k_m=r,\ 0\le k_i\le c_i} \dfrac{r!}{k_1!\cdots k_m!}$` | each admissible multiplicity vector contributes its multinomial count | the same problem with an order: `(2,2,2)`, `r = 5` gives 90 |
| Admissible vectors | `$\lvert\{(k_1,\dots,k_m) : \sum k_i = r,\ 0 \le k_i \le c_i\}\rvert$ | the multiplicity vectors, one per unordered selection | the brute-force referee for the coefficient method |
| Subtract a bad case (permutations) | `$P(n,r) - (n-1)(n-2)\cdots(n-r+1)$` | fix the offending item in a slot, then count the rest from the *remaining* pool | 4-long schedules of 6 tests with A not last: $360 - 60 = 300$ |
| "At least one digit" subtraction | `$(26+10)^{5} - 26^{5}$` | all strings minus the all-letter ones | 5-character passwords: $36^5 - 26^5 = 48{,}584{,}800$ |
| Same count as a binomial sum | `$\sum_{k=1}^{r} C(r,k)\,k^{\text{digits}}(26)^{r-k}$` | choose which `k` slots hold digits | must agree with the subtraction: also 48,584,800 |
| Multiplications, when the object is a *pair* of choices | `C(12,3)\cdot 3` | choose the committee, then choose its chair | 12 people → 660 |

---

## Multiple Choice Questions

**Q1.** "Choose Alice and Bob to review the patch." Which formula counts the
outcomes, and why?

- A) `P(2, 2) = 2`, because two people are being chosen in an order the
  sentence fixes by naming Alice first
- B) `C(n, 2) = n(n−1)/2`, because swapping the two reviewers gives the same
  outcome
- C) `n²`, because each of the two slots picks freely from `n` people
- D) `n!/2`, because any pair can be ordered in two ways and both count

<details>
<summary>Answer and explanation</summary>

**B) `C(n, 2) = n(n−1)/2`, because swapping the two reviewers gives the same
outcome.**

The decision rule is *if swapping two of the chosen items gives a different
answer, order matters*. {Alice, Bob} and {Bob, Alice} are the same review team,
so order does not matter and there are no repeats: `C(n, 2)`.

- A) is the over-count in Mistake 1. `P(2,2) = 2` counts "Alice then Bob" and
  "Bob then Alice" as different outcomes, which doubles the answer for every
  team size.
- C) is right only if repeats were allowed *and* order mattered — it is the
  count of 2-letter passwords over `n` symbols, not of review teams.
- D) confuses two corrections. The `2` in `C(n,2) = n(n−1)/2` comes from
  dividing the ordered count by `2!`; `n!/2` is not a pair count at all for
  `n > 2`.

</details>

**Q2.** A system issues 3-digit PINs with no repeated digit, chosen from 0
through 9. How many PINs are there?

- A) `C(10, 3) = 120`
- B) `P(10, 3) = 720`
- C) `10³ = 1,000`
- D) `10³ − 1 = 999`

<details>
<summary>Answer and explanation</summary>

**B) `P(10, 3) = 720`.**

PIN 123 and PIN 321 are different PINs, so order matters. Digits must be
distinct, so no repeats, so the choice set shrinks: 10 · 9 · 8 = 720. This is
Mistake 2 of this lesson — "choosing digits" *sounds* like choosing, but PIN,
rank, order, sequence, schedule and password all signal that swapping two
choices changes the answer.

- A) is the nCr answer. It is exactly a factor of 3! = 6 too small, and the gap
  grows with `r`: at `r = 4` it would be a factor of 24.
- C) is right for *any* 3-digit PIN, and wrong only because of the no-repeat
  clause. The clause changes the second and third factors from 10 to 9 and 8.
- D) subtracts a single string rather than the 10 · 10 = 100 strings that use a
  repeated digit somewhere.

</details>

**Q3.** How many ways can you choose 3 scoops of ice cream from 6 flavours if
the same flavour may be chosen twice?

- A) `C(6, 3) = 20`
- B) `P(6, 3) = 120`
- C) `C(8, 3) = 56`
- D) `C(6, 3) · 3! = 120`

<details>
<summary>Answer and explanation</summary>

**C) `C(8, 3) = 56`.**

Order does not matter and repeats are allowed, which is the box whose answer is
the trick: `C(n + r − 1, r) = C(6 + 3 − 1, 3) = C(8, 3) = 56`. The
correspondence is r stars and n − 1 bars: the stars before each bar are that
flavour's multiplicity, and there are `n + r − 1` symbols of which `n − 1` are
bars.

- A) is the no-repeats answer and is Mistake 3 of this lesson. It is too small
  because it omits every multiset containing a double or a triple.
- B) also forgets the repeats, and additionally counts order — two separate
  errors that happen to multiply out to the same number as D.
- D) is `C(6,3) · 3!`, which equals option B. Both are wrong for the same reason:
  order and repeats are each mis-handled, and the two factors cancel in
  appearance without cancelling in fact.

</details>

**Q4.** `P(8, 4) = 1,680` and `C(8, 4) = 70`. What is the quotient, and what does
the identity `P(n,r) = C(n,r)·r!` say?

- A) 24, because each 4-element set has exactly 4! = 24 orderings
- B) 12, because reversing an order is a factor of 2 and there are 4 rotations
- C) 4, because the choice set shrinks four times
- D) 24, but only because 8 − 4 = 4 and `2^4 = 16` rounds up

<details>
<summary>Answer and explanation</summary>

**A) 24, because each 4-element set has exactly 4! = 24 orderings.**

1,680 / 70 = 24 = 4!, exactly as the theorem predicts. The identity is the
formal version of "order matters, so multiply by the rearrangements": fix a
4-element subset, and all 4! of its orderings are valid 4-permutations using
precisely those elements, so the combinations partition the permutations into
classes of size 4!.

- B) is the count of an *undirected cycle* on 5 vertices, not of orderings of 4
  objects.
- C) is a genuine factor in this example — the last factor of `P(8,4)` is
  `8 − 3 = 5`, not 4 — but it is a factor of one term in the product, not the
  ratio of the two counts.
- D) reaches the right number for the wrong reason. `2^4 = 16 ≠ 24`, so the
  parenthetical arithmetic does not even hold; the correct reading of the
  identity is the one in A.

</details>

**Q5.** How many distinct arrangements are there of the letters in MISSISSIPPI?

- A) `11! = 39,916,800`
- B) `11!/4! = 1,663,200`
- C) `11!/(4!·4!·2!) = 34,650`
- D) `11!/(4! + 4! + 2!) = 39,916,800`

<details>
<summary>Answer and explanation</summary>

**C) `11!/(4!·4!·2!) = 34,650`.**

MISSISSIPPI has 11 letters with multiplicities 4 × S, 4 × I, 2 × P, so the
multiset permutation formula divides 11! once per *distinct* letter:
39,916,800 / (24 · 24 · 2) = 34,650. The lesson notes that this is small enough
to search, which is exactly why it is a favourite interview question.

- A) counts the arrangements of 11 *labelled* objects. It overcounts each
  visible arrangement 4! · 4! · 2! = 1,152 times.
- B) is Mistake 4 of this lesson: dividing once captures only the first group of
  repeats. It is a factor of 48 too big.
- D) adds the factorials instead of multiplying them. `(4! + 4! + 2!) = 72`
  against a true divisor of 1,152 — a factor of 16 off, and the formula is not
  even the right shape.

</details>

**Q6.** The lesson gives Pascal's recursion as `C(n, r) = C(n − 1, r − 1) +
C(n − 1, r)`. Which pair of sets do the two terms count?

- A) The `r`-subsets that contain a fixed element, and those that do not
- B) The `r`-subsets of the first `n − 1` elements, and the `r`-subsets of the
  last `n − 1` elements
- C) The `r`-subsets of an `r`-set, and the `r`-subsets of an `(n − r)`-set
- D) The subsets containing the first element, and the subsets containing the
  last element

<details>
<summary>Answer and explanation</summary>

**A) The `r`-subsets that contain a fixed element, and those that do not.**

Fix one element of the `n`-set. A subset either contains it — delete it and you
get an `(r − 1)`-subset of the other `n − 1`, giving `C(n − 1, r − 1)` — or does
not, giving an `r`-subset of the other `n − 1`, counted by `C(n − 1, r)`. The two
cases are disjoint and exhaustive, so the sum rule applies. This is precisely the
theorem [Lesson 22](../part02_discrete_combinatorics/22_binomial_theorem.md)
re-derives from the binomial expansion.

- B) counts subsets that mostly agree, and the two families are *not* disjoint —
  a subset avoiding the first element and one avoiding the last can both be
  present in the intersection. Adding would overcount.
- C) uses the wrong sizes. The pieces have sizes `n − 1` with `r − 1` and `r`
  selections, not `r` and `n − r`.
- D) splits on two different elements, so a subset containing both is in both
  families. That is a classic double-count, and the reason a correct partition
  must fix *one* element.

</details>

**Q7.** The symmetry `C(n, k) = C(n, n − k)` — what bijection proves it, and
what does it predict about the two numbers below?

- A) It has no combinatorial proof; it is an algebraic accident. So `C(20,7)` and
  `C(20,13)` need not agree
- B) Take the complement inside the `n`-set: `C(20,7) = C(20,13) = 77,520`
- C) It is proved by induction on `n` using Pascal's recursion, and predicts
  `C(20,7) = C(20,20) = 1`
- D) It comes from `P(n,r) = C(n,r)·r!` and predicts `C(20,7) = C(20,7!)`

<details>
<summary>Answer and explanation</summary>

**B) Take the complement inside the `n`-set: `C(20,7) = C(20,13) = 77,520`.**

Sending a `k`-subset to its complement is a bijection from the `k`-subsets onto
the `(n − k)`-subsets — so it is proved combinatorially, and being able to say
*why* two unrelated-looking counts coincide is the difference between having
computed a number and having understood it.

- A) is the memorise-instead-of-understand view. The identity is also true
  algebraically, but the point of the bijection is that it explains the equality
  rather than asserting it.
- C) offers a real proof route but draws a false conclusion: `n − k = 20 − 7 = 13`,
  not 20. `C(20,20) = 1` because the only 20-subset is the whole set.
- D) does not follow from `P = C·r!` at all. `C(20, 20!)` is undefined; the
  symmetry replaces `k` by `n − k`, which for `n = 20, k = 7` is 13.

</details>

**Q8.** A manifest takes at most 2 tests from each of 3 groups, 5 tests in total.
How many manifests are there?

- A) 3 — the multiplicity pattern must be `(2, 2, 1)`, and there are 3 choices
  for the group contributing 1
- B) 6 — one for each ordering of `(2, 2, 1)`
- C) 30 — the multinomial count `5!/(2!2!1!)` for one pattern
- D) 90 — six times the unordered count

<details>
<summary>Answer and explanation</summary>

**A) 3 — the multiplicity pattern must be `(2, 2, 1)`, and there are 3 choices for
the group contributing 1.**

This is the coefficient of `x⁵` in `(1 + x + x²)(1 + x + x²)(1 + x + x²)`. Each
group contributes `x^kᵢ` with `kᵢ ≤ 2`; landing on `x⁵` forces a permutation of
`(2, 2, 1)`, and there are three. The lesson's `bounded_selections([2,2,2], 5)`
returns 3, refereed by enumerating every multiplicity vector.

- B) counts orderings of the pattern. In an unordered manifest the pattern
  `(2, 2, 1)` with the *third* group contributing 1 is the same manifest as the
  pattern with the first group contributing 1 — only the identity of the groups
  differs, and there are 3 groups, so 3, not 6.
- C) is the number of *ordered* schedules for one fixed multiplicity vector.
  It is the right per-vector weight, applied to one vector instead of all three.
- D) is the total ordered count: 3 · 30 = 90. That answers "how many 5-long
  schedules of 5 distinct tests drawn at most twice per group", which is a
  different object from the manifest the question asks for.

</details>

**Q9.** From the worked example: how many 4-long schedules of the 6 tests have
test A *not* in the last slot?

- A) 300
- B) 360
- C) 240
- D) 120

<details>
<summary>Answer and explanation</summary>

**A) 300.**

All 4-long schedules: `P(6,4) = 6 · 5 · 4 · 3 = 360`. Those with A last: fix A
there, then fill the first three slots with distinct tests from the *remaining*
five, giving 5 · 4 · 3 = 60. So 360 − 60 = 300.

- B) is the count before applying the constraint — the classic answer you get by
  reading "how many schedules" and stopping.
- C) counts schedules with A in the *first* slot as well as excluding some other
  set of 120; 360 − 240 would be subtracting twice as many as the bad set holds.
- D) is `C(6,4) · 4! = 15 · 24 = 360` halved, i.e. it treats the question as
  unordered. Fixing A in one slot of a schedule makes the remaining slots
  ordered, so the product rule applies to them, not `C(5,3)`.

</details>

**Q10.** A script builds `C(n, r)` as `factorial(n) // (factorial(r) *
factorial(n-r))`. Calling it with `n = 1000, r = 500` is slow and memory-hungry.
What breaks, and what is the fix?

- A) Nothing breaks; the formula is exact, so the cost is only constant overhead
- B) The arithmetic is exact but wasteful: 1000! has 2,568 digits, so the naive
  form does `O(n)` big-integer work where `O(min(r, n−r))` suffices — use
  `math.comb` or the multiplicative form with `r = min(r, n−r)`
- C) Integer division truncates, so the result is wrong whenever the factorial
  ratio is not an integer
- D) It breaks only for `r > n`, and this call is fine

<details>
<summary>Answer and explanation</summary>

**B) The arithmetic is exact but wasteful: 1000! has 2,568 digits, so the naive
form does `O(n)` big-integer work where `O(min(r, n−r))` suffices.**

This is Mistake 5 of this lesson. The factorial ratio *is* an exact integer, so
there is no correctness bug — but you build three enormous factorials, do two
huge multiplications, and throw most of the digits away in the division.
`math.comb` is C-implemented and performs the divisions with more care.

- A) is wrong because "exact" is not the same as "cheap". At `n = 20` the naive
  version looks fine, which is what makes the wall invisible until it is hit.
- C) is a real misconception about factorial ratios: `n!` is always divisible by
  `r!(n−r)!` for `0 ≤ r ≤ n`, so truncation never corrupts the answer.
- D) misreads the failure. `r > n` does force `C(n,r) = 0`, but that is a
  different guard, and the lesson states the `0` convention explicitly. The cost
  problem at `n = 1000` is real regardless.

</details>

---

## Subjective Questions

### Short Answer

**Q1. State the four-box decision table: for each combination of "does order
matter" and "are repeats allowed", give the formula and one example.**

<details>
<summary>Answer</summary>

| | repeats allowed | no repeats |
| --- | --- | --- |
| **order matters** | `$n^{r}$` — strings, passwords, functions | `$P(n,r) = n!/(n-r)!$` — schedules, PINs from distinct digits |
| **order irrelevant** | `$C(n+r-1, r)$` — 3 scoops from 6 flavours | `$C(n,r) = n!/(r!(n-r)!)$` — committees, handshakes |

The one-sentence test: **if swapping two of the chosen items gives a different
answer, order matters.** Choosing Alice and Bob for a review — swapping changes
nothing, so `C`. Ranking Alice above Bob — swapping changes the answer, so `P`.
Order matters and repeats are allowed gives $n^{r}$ because each of the `r` slots
picks freely and independently from the whole pool.

</details>

**Q2. Write `C(n, r)` in its multiplicative form and say why you would prefer it
to the factorial form.**

<details>
<summary>Answer</summary>

$$C(n,r) = \frac{n(n-1)(n-2)\cdots(n-r+1)}{r!} = \frac{n(n-1)\cdots(n-r+1)}{1\cdot 2\cdot 3\cdots r}$$

You prefer it for three reasons. It never constructs `n!`, so it stays usable at
`n = 1000` where the factorial has thousands of digits. Every intermediate value
in the numerator is smaller than `n!`, so the big-integer work is much cheaper.
And combining it with the symmetry — `r = min(r, n−r)` — turns an `O(n)`
computation into `O(min(r, n−r))`, which matters when `r` is small and `n` is
large.

</details>

**Q3. Why is `P(n, r) = C(n, r) · r!`? Give the partition argument.**

<details>
<summary>Answer</summary>

Fix an `r`-element subset `S`. Every ordering of `S` is a valid `r`-permutation
using exactly the elements of `S`, and by the product rule there are `r!` of
them. So each `r`-subset contributes exactly `r!` permutations, and the
`r`-subsets partition `P(A, r)` into classes of equal size — a partition, because
each permutation uses one specific set of elements and no two sets share a
permutation.

Dividing the total `P(n,r)` by the class size `r!` gives `C(n,r)`. This is the
formal version of "order matters, so multiply by the rearrangements", and it is
why your `nPr` answer should always be `r!` times your `nCr` answer — the
cheapest available self-check.

</details>

**Q4. How many unordered selections of `r` items from `n` kinds are there when
repeats are allowed? Describe the bijection you use to prove it.**

<details>
<summary>Answer</summary>

$$C(n+r-1,\;r) = C(n+r-1,\;n-1)$$

The bijection is stars and bars. Write `r` stars and `n − 1` bars in a row. Each
bar separates one kind from the next, so the stars before the first bar are
"how many of kind 1", between the first and second bar "how many of kind 2", and
so on.

A selection maps to exactly one bar pattern, and a bar pattern maps back to
exactly one selection, so this is a bijection. The patterns are strings of length
`n + r − 1` with `n − 1` distinguished positions for the bars, of which
`C(n+r−1, n−1)` exist. Worked: 3 scoops from 6 flavours gives
`C(6 + 3 − 1, 3) = C(8, 3) = 56`.

</details>

**Q5. State Pascal's recursion with its base cases, and say what the recursion
tree computes.**

<details>
<summary>Answer</summary>

$$C(n,r) = C(n-1,\,r-1) + C(n-1,\,r), \qquad C(n,0) = C(n,n) = 1, \quad C(n,r) = 0 \text{ for } r > n$$

The recursion tree computes a whole row of Pascal's triangle from the row above:
each entry is the sum of the two entries diagonally above it. Starting from the
single row `[1]` and repeating `n` times yields row `n`, which is exactly the
list `[C(n,0), C(n,1), …, C(n,n)]`.

This is the dynamic-programming form: fill a table instead of recomputing shared
subproblems. The lesson's `pascal_row(6)` gives
`[1, 6, 15, 20, 15, 6, 1]`, which enumeration of the actual subsets confirms,
and the sum of row 10 is `2¹⁰ = 1,024`.

</details>

### Long Answer

**Q1. The lesson's decision rule is "if swapping two of the chosen items gives a
different answer, order matters". Why is that rule reliable, and where does it
stop being reliable?**

<details>
<summary>Model answer</summary>

The rule is reliable because "order matters" is not a stylistic judgement about
the sentence — it is a statement about the *object being counted*. If swapping
two items produces a different object, then the counted objects are sequences
and `nCr` merges distinct objects into one, undercounting by exactly `r!` per
class. If swapping produces the same object, the counted objects are sets, and
`nPr` invents distinctions that do not exist, overcounting by `r!`. The rule
gets this right for both failure directions, which is why it beats the default
of reaching for whichever formula is more familiar.

It stops being reliable in two places, and both are about the *object* being
ambiguous rather than the rule being wrong.

The first is when the object is not fully described by the sentence. "Choose two
servers" is ambiguous about order; "choose two servers and give them a failover
priority" is not. Here the lesson's answer is to look for the signalling words —
rank, order, sequence, schedule, PIN, path, password, manifest — each of which
tells you swapping changes the artifact. Absent such a signal, and absent an
explicit statement, the honest move is to say which reading you are using, which
is what the lesson does in Mistake 2.

The second and more interesting failure is circular arrangement. Around a round
table of `n` people, `(n − 1)!` arrangements are distinct, not `n!`, because
rotating the whole table gives the same seating. The swap test says order
matters, and it does — but the group that is "the same" is larger than the one
the swap test detects, so the answer is `n!` divided by `n`, not by `r!`. This is
exactly the structural point the lesson's own Exercise 1 makes: "divide by the
rearrangements" is only as good as your identification of *which* rearrangements
count as the same. And the identification itself is a modelling decision, which is
why the lesson prefers the enumeration referee in Mistake 5: brute force builds
the objects and therefore cannot get the equivalence wrong.

</details>

**Q2. Why is "at most two of each kind" solved by reading a coefficient out of a
polynomial instead of by case analysis? Explain why the coefficient reading is
exact and not merely suggestive.**

<details>
<summary>Model answer</summary>

The case-analysis route is not wrong, it is just bad bookkeeping. With `m` kinds
and `r` items you must enumerate every admissible multiplicity vector, and for
caps like `(2, 2, 2)` at `r = 5` that means writing out the permutations of
`(2, 2, 1)`. Change the numbers — `(3, 3, 3)` at `r = 6`, or eight kinds — and
the case list grows while the polynomial does not.

The polynomial works because of how a product behaves. Expanding
`(1 + x + … + x^{c₁})(1 + x + … + x^{c₂})⋯(1 + x + … + x^{c_m})`, each of the 2ⁿ⁰
terms is formed by taking one `x^{kᵢ}` from the `i`-th factor, and the product of
those terms is `x^{k₁ + k₂ + ⋯ + k_m}`. Collecting every term of degree `r` is
therefore *precisely* the set of admissible multiplicity vectors, each
contributing `1` — no vector is counted twice, because the factors are
distinguishable and a vector records one choice per factor.

That is the sense in which the coefficient is exact rather than suggestive. It is
not a numerical coincidence that the coefficient of `x⁵` in `(1+x+x²)³` is 3; it
is a restatement of the fact that the expansion is a sum over all vectors, grouped
by degree. The lemma's phrase — "collecting all terms of degree `r` counts each
valid multiplicity vector once" — is the whole proof.

The same mechanism handles the ordered version, and the two together show why the
technique is worth having. Each unordered selection contributes its multinomial
count `r!/(k₁!⋯k_m!)` as the number of orderings, so the ordered count is
`Σ r!/(k₁!⋯k_m!)` over admissible vectors: `3 · 5!/(2!·2!·1!) = 3 · 30 = 90` for
caps `(2,2,2)` at `r = 5`. Restricting a factor to `(1 + x + … + x^{cᵢ})` is
precisely how the cap is imposed, and dropping it is how the "unlimited" version
falls out as a special case. The lesson's `bounded_selections` builds the
coefficient list with the schoolbook rule and checks every result against
`brute_vectors`, which enumerates the vectors directly — the two agreeing is what
turns the argument into a verified computation.

</details>

**Q3. Why does the factorial form of `C(n, r)` degrade so badly, and what would
actually break if you ignored that in production code?**

<details>
<summary>Model answer</summary>

The degradation is in the size of the integers involved, not in correctness.
`n!/(r!(n−r)!)` is always an exact integer for `0 ≤ r ≤ n`, so the formula never
produces a wrong answer. What it produces is *enormous intermediates*: at
`n = 1000`, `1000!` has 2,568 decimal digits, and you build three such numbers,
multiply two of them, and then divide — discarding nearly all the digits you just
computed.

What breaks in production is a stack of things. In fixed-width integer
arithmetic the factorial overflows first: even `21!` exceeds a 64-bit unsigned
integer, so at `n = 21` the "exact" formula silently wraps and returns a
plausible wrong number. In exact big-integer arithmetic the cost is wall-clock
and memory: the work is `O(n)` multiplications of numbers with `Θ(n log n)` bits,
and it happens on every call if the function sits in a hot loop. And the
asymptotic claim is wrong too — the multiplicative form with `r = min(r, n−r)`
is `O(min(r, n−r))`, so with `r = 2` and `n = 10⁹` you do three steps rather
than a billion.

The fixes are all already in the lesson. Use `math.comb(n, r)`, which is
C-implemented and does the division more carefully than a hand-rolled loop will.
Or write the multiplicative form, keeping every intermediate an integer by
dividing at each step. Or, when you only need the count as a feasibility
number, keep it as `C(n, r)` symbolically and take `log₂` of it — which is the
habit the lesson picks up in the sizing step of Worked Example 1, and which stays
correct even when the count itself would not fit in a machine word.

The wider point is that "exact" is not the property you want. Every formula in
this lesson is exact. What differs between them is the resource profile, and
exponential-time-but-correct is still wrong when it has to run on every request.

</details>

**Q4. Why is the check `P(n, r) = C(n, r) · r!` genuinely useful, and what does a
violation of it tell you?**

<details>
<summary>Model answer</summary>

It is useful because it tests two independent computations against each other.
`P(n,r)` and `C(n,r)` are computed by different code paths — one is a falling
product, the other a product followed by division — so agreement is evidence that
both are right. It costs one multiplication and one exact division. A division
that comes out integral is itself a check, since `C(n,r)·r!` is a count and
counts are integers.

A violation is diagnostic rather than merely "a bug is somewhere". Because the
factor is exactly `r!`, a quotient that is not `r!` tells you the *ratio* between
your ordered and unordered counts is wrong, which is a statement about the
problem's shape, not about your arithmetic. The usual causes, in order of
frequency:

- You applied `nPr` to a problem whose objects are sets. The quotient then comes
  out as something smaller than `r!` — for `n = 5, r = 3` you would see 20/10 = 2
  instead of 6 — and the fix is to re-read the sentence for the words that signal
  order.
- You applied `nCr` to a problem whose objects are sequences. The quotient then
  comes out larger than `r!`, and again the fix is the same reading, not the
  arithmetic.
- You miscounted the pool: a slot was supposed to be excluded (as when test A is
  forbidden from the last position) and was not. The quotient is then not `r!` in
  a way that does not match any factorial, which is a signal that the *set* being
  drawn from was wrong.
- The "repeats allowed" clause was handled inconsistently between the two
  formulas, as in option D of Q3 above, where `C(6,3)·3!` and `P(6,3)` coincide
  while both being wrong.

What the check cannot do is tell you *which* of two correct-looking counts the
problem wants. It certifies internal consistency, not interpretation. For that you
still need to write the objects down — which is why the lesson's habit of
refereeing against `itertools.permutations` or `itertools.combinations` is the
step that catches an error the ratio test passes.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — Handshakes.** In a room of 9 people, how many handshakes
occur if everyone shakes hands with everyone else exactly once? Express the
answer as nCr and explain what each part means.

<details>
<summary>Solution</summary>

C(9, 2) = 9 · 8 / 2 = 36. A handshake is an *unordered* pair of distinct people,
so order does not matter and repeats are impossible. Dividing by 2 removes the
double counting of {A,B} vs {B,A}.

```python
from math import comb
print(comb(9, 2), 9 * 8 // 2)
```
</details>

**[ ] Exercise 2 — A password question.** A system requires passwords of exactly
5 characters from 26 lowercase letters and 10 digits, with at least one digit.
How many such passwords exist? Solve it as a subtraction, and then as an explicit
sum over "how many digits", and check the two agree.

<details>
<summary>Solution</summary>

Subtraction: total minus all-letters.

    (26 + 10)⁵ − 26⁵ = 36⁵ − 26⁵ = 60,466,176 − 11,881,376 = 48,584,800

Sum over the number of digits k = 1..5, choosing the positions with C(5, k):

    Σ_{k=1..5} C(5,k)·10ᵏ·26^(5−k)
    = 5·10·26⁴ + 10·100·26³ + 10·1000·26² + 5·10000·26 + 100000
    = 22,818,000 + 17,576,000 + 6,760,000 + 1,300,000 + 100,000 = 48,554,000

Hmm — that does not match, so let me redo it. C(5,1)=5, C(5,2)=10, C(5,3)=10,
C(5,4)=5, C(5,5)=1. So the terms are

    k=1: C(5,1)·10¹·26⁴ = 5·10·456,976      = 22,848,800
    k=2: C(5,2)·10²·26³ = 10·100·17,576    = 17,576,000
    k=3: C(5,3)·10³·26² = 10·1000·676      =  6,760,000
    k=4: C(5,4)·10⁴·26¹ = 5·10000·26       =  1,300,000
    k=5: C(5,5)·10⁵·26⁰ = 1·100000·1       =    100,000
    total                                = 48,584,800 ✓

which matches the subtraction exactly. The arithmetic error in my first pass was
in the k = 1 term (26⁴ = 456,976, not 456,956).

```python
from math import comb
total = 36**5 - 26**5
by_sum = sum(comb(5, k) * 10**k * 26 ** (5 - k) for k in range(1, 6))
print(total, by_sum, total == by_sum)
```
</details>

**[ ] Exercise 3 — Distinguishing the two.** For each problem, say whether order
matters, whether repeats are allowed, give the formula, and compute the answer:
(a) the 5-card hand in poker; (b) arranging 8 sprinters for a 100 m final with
no ties; (c) a 3-letter US airport code; (d) a 3-letter airport code where
repeating a letter is banned.

<details>
<summary>Solution</summary>

(a) Order does not matter, no repeats: C(52, 5) = 2,598,960.
(b) Order matters, no repeats. If you rank all 8 sprinters, P(8, 8) = 40,320; if
you only want the winner, P(8, 1) = 8.
(c) Order matters, repeats allowed: 26³ = 17,576.
(d) Order matters, no repeats: P(26, 3) = 26 · 25 · 24 = 15,600.

Cases (c) and (d) differ only by the "no repeats" clause, and that single clause
turns 26·26·26 into 26·25·24 — a factor of about 1.13 at this size. The
correction is small only because r = 3 is close to n = 26. With r = 2 out of
100 options the same correction changes 10,000 into 9,900, and with r = 2 out of
4 it changes 16 into 12 — a factor of 1.33.

```python
from math import comb, perm
print(comb(52, 5), perm(8, 8), 26**3, perm(26, 3))
```
</details>

**[ ] Exercise 4 — Stars and bars.** Choose 7 identical chocolate bars from 4
flavours, repeats allowed, order irrelevant. Count it two ways: with the formula,
and by enumerating every multiplicity vector.

<details>
<summary>Solution</summary>

Formula: C(n + r − 1, r) = C(4 + 7 − 1, 7) = C(10, 7) = 120.

Enumeration: every quadruple (a, b, c, d) of non-negative integers with
a + b + c + d = 7, which is C(10, 3) = 120 vectors.

```python
from itertools import product as iproduct
from math import comb

vectors = [v for v in iproduct(range(8), repeat=4) if sum(v) == 7]
print(comb(10, 7), len(vectors))
print("first few vectors:", vectors[:5])
```
</details>

**[ ] Exercise 5 — Constrained orderings.** How many orderings of the 6 letters
A, B, C, D, E, F contain A and B next to each other, in either order?

<details>
<summary>Solution</summary>

Treat (A,B) and (B,A) as a single block. Then you are permuting 5 objects: the
block plus C, D, E, F. Each arrangement of those 5 objects corresponds to exactly
2 arrangements of the letters, because the block expands to AB or BA.

    P(5, 5) · 2 = 120 · 2 = 240

Check by subtraction: all 720 orderings, minus those with A and B separated. The
count of separated ones is 720 − 240 = 480, which is the classic "treat the pair
as one object" result restated.

```python
from itertools import permutations
from math import perm

listed = [p for p in permutations("ABCDEF") if abs(p.index("A") - p.index("B")) == 1]
print(perm(5, 5) * 2, len(listed))
```
</details>

**[ ] Exercise 6 — Choosing with limits.** A warehouse stocks 3 sizes of bolt.
A shipment must contain exactly 6 bolts with **at most 3 of each size**. How many
different shipments are possible? Give the generating polynomial and compute the
coefficient.

<details>
<summary>Solution</summary>

Polynomial: (1 + x + x² + x³)³. Coefficient of x⁶.

Expand: (1 + x + x² + x³)² = 1 + 2x + 3x² + 4x³ + 3x⁴ + 2x⁵ + x⁶.
Multiplying by (1 + x + x² + x³) again, the degree-6 coefficients sum to

    1 (from degree 6) + 2 (degree 5) + 3 (degree 4) + 4 (degree 3) = 10

So there are 10 shipments. Enumerating the vectors confirms it: the valid
multiplicities are the permutations of (3, 3, 0) — 3 of them — and (2, 3, 1) and
(3, 2, 1) and (2, 2, 2) — 6 permutations each of (2,3,1) and 1 of (2,2,2).
3 + 6 + 1 = 10 ✓.

```python
def bounded(caps, total):
    coeffs = [1]
    for cap in caps:
        nxt = [0] * (len(coeffs) + cap)
        for degree, c in enumerate(coeffs):
            for take in range(cap + 1):
                nxt[degree + take] += c
        coeffs = nxt
    return coeffs[total]

from itertools import product as iproduct
vecs = [v for v in iproduct(range(4), repeat=3) if sum(v) == 6]
print(bounded([3, 3, 3], 6), len(vecs), vecs)
```
</details>

**[ ] Exercise 7 — Bitmask subsets.** An 8-bit register has 256 possible values.
How many of them have exactly 4 bits set? How many distinct 12-bit masks are
there in total, and how do those two facts combine in a feature-selection search?

<details>
<summary>Solution</summary>

Exactly 4 bits set: choose which 4 of the 8 positions, so C(8, 4) = 70.

Total 12-bit masks: 2¹² = 4096.

In feature selection with 12 candidate features you can search the whole mask
space exhaustively in 4096 iterations, but if you require exactly 4 features
chosen, the search space drops to 70 — a 58× reduction. That reduction is why
constraints like "exactly k features" make exhaustive search viable where the
unconstrained space does not.

```python
from math import comb
print(comb(8, 4), 2**12, 2**12 / comb(8, 4))
```
</details>

**[ ] Challenge 8 — Bridge hands with a shape constraint.** How many 13-card
bridge hands contain exactly 4 spades? Check your answer by computing it two
ways: the closed form, and a coefficient extraction that builds the binomial rows
by repeated polynomial multiplication instead of calling `comb`.

<details>
<summary>Solution</summary>

Closed form: choose 4 of the 13 spades, then 9 of the 39 non-spades.

    C(13, 4) · C(39, 9) = 715 · 211,915,132 = 151,519,319,380

Coefficient route. The pile of 13 spades contributes the polynomial (1 + y)¹³,
whose coefficient of y^k is the number of ways to take k spades; the non-spade pile
contributes (1 + y)³⁹. So the answer is the coefficient of y⁴ in (1 + y)¹³ times
the coefficient of y⁹ in (1 + y)³⁹ — the same coefficient-extraction idea as
Lesson [22](../part02_discrete_combinatorics/22_binomial_theorem.md), here built by hand:

```python
from math import comb

def conv(a, b):
    """Multiply two polynomials given as coefficient lists."""
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out

one_plus_y = [1, 1]          # the polynomial 1 + y
p13, p39 = [1], one_plus_y
for _ in range(13):          # multiply by (1 + y) thirteen times -> (1 + y)^13
    p13 = conv(p13, one_plus_y)
for _ in range(39 - 1):
    p39 = conv(p39, one_plus_y)

print(f"[y^4](1+y)^13 = {p13[4]}  equals C(13,4) = {comb(13, 4)}")
print(f"[y^9](1+y)^39 = {p39[9]}  equals C(39,9) = {comb(39, 9):,}")
print(f"exactly 4 spades = {p13[4] * p39[9]:,}")
print(f"closed form      = {comb(13, 4) * comb(39, 9):,}")
print(f"share of all 13-card hands = {comb(13,4)*comb(39,9)/comb(52,13):.4%}")
```
</details>

## Summary

- Two questions decide everything: **does order matter?** and **are repeats
  allowed?** They place a problem in exactly one of four boxes.
- The four counts: nⁿ (ordered, repeats), P(n, r) = n!/(n−r)!, C(n, r), and
  C(n + r − 1, r) for unordered selections with repeats.
- P(n, r) = C(n, r) · r! is a theorem and a self-check: if your permutation count
  is not r! times your combination count, you made an arithmetic slip.
- For "A must not be last", fix the position first, then count the remaining
  slots from the *reduced* pool. The factors shrink, not repeat.
- Multiset arrangements divide by one factorial per distinct repeated item, once
  per item type.
- Choosing with limits is coefficient extraction: the answer is the coefficient
  of xʳ in the product of the per-kind polynomials. Ordered versions multiply
  each multiplicity vector by its multinomial count.
- Prefer the multiplicative form or `math.comb` over raw factorials; n! is exact
  only while it fits in memory.
- C(n, 2) = n(n − 1)/2 is the arithmetic behind every "compare all pairs"
  algorithm.

## Next

[Lesson 22 — The Binomial Theorem](../part02_discrete_combinatorics/22_binomial_theorem.md) assumes you can pick
between nCr and nPr; it shows that the binomial coefficients are themselves
counts, which turns expansion into a way of computing large combinatorial sums
without a loop.