# 20 — Counting Principles

**Part**: part02_discrete_combinatorics · **Prerequisites**: 15 · **Time**: 30 min

---

## In Plain Words

Counting is the easiest mathematics in computer science, and the easiest to get
subtly wrong. Almost everything in this part rests on just two moves.

The first move is: when you make one choice and then another choice, and the
second choice is made *after* you already know how you answered the first, you
**multiply** the numbers of possibilities. Picking a shirt and then a pair of
trousers: if there are five shirts and three pairs of trousers, there are
fifteen outfits.

The second move is: when you split a problem into cases that are genuinely
different, you **add** the case counts. A message is either delivered or it is
not; delivered messages number one thousand, undelivered number twelve, so there
are one thousand and twelve messages in total.

The third idea is not about arithmetic at all. It is that you can count
something by finding a **one-to-one correspondence** with something you already
know how to count. Subsets of a four-element collection, strings of four zeroes
and ones, and outcomes of four coin flips all number sixteen — not because the
numbers happen to match, but because each subset corresponds to exactly one
four-bit string: the bit is 1 exactly when that element is in the subset. A
correspondence like that, where every object on one side pairs with exactly one
object on the other side, is called a *bijection*. Finding one is usually the
creative part of counting. Once you have it, the arithmetic is trivial.

The rest of this lesson is about recognising which of the three moves a problem
is asking for, and building the correspondence carefully enough that nothing is
counted twice.

## Why Computer Science Cares

- **Security keyspaces.** "An 8-character password over 94 printable ASCII
  characters" is a product rule: 94⁸ ≈ 6 × 10¹⁵ possibilities. If that number is
  smaller than the attacker's throughput times the age of the universe, the
  system is broken. Getting this number wrong by a factor of ten is the
  difference between a safe hash and a dictionary lookup.
- **Hash table sizing.** A hash table with 128 slots holds at most 128 distinct
  values, but the number of distinct 32-bit inputs is 2³². That ratio is the
  load factor, and it comes straight from the power-set count. Birthday-bound
  collision estimates in Lesson [70](../part05_probability_statistics/70_information_theory_entropy.md)
  are built from it too.
- **Search space size.** Minimax, branch and bound, and Monte Carlo search all
  need to know how big the tree is before they start. A game tree with branching
  factor 7 and depth 8 has 7⁸ ≈ 5.8 million leaf positions, which is why
  alpha-beta pruning exists. The count is a sum rule across depths inside a
  product rule within each depth.
- **Bitmask DP.** Many exponential algorithms become tractable once you notice
  that the state is a *subset*. Choosing 3 of 8 items is 56 states, not 2⁸ —
  see Lesson [82](../part06_algorithms_math/82_tools_for_algorithm_design.md).
- **Column-count and schema choices.** "How many distinct columns can a row
  type have if you have 2⁸ flags?" is the power-set count, and it is how you
  decide whether a bitmask column is a sensible design.

## The Formal Version

Notation follows [SYMBOLS.md](../SYMBOLS.md). Cardinality is written |A|;
the power set is 𝒫(A); a Cartesian product is A × B.

**Definition.** A *bijection* from A to B is a function f : A → B that is
**injective** (different inputs give different outputs) and **surjective**
(every element of B is some f(a)). In plain terms, a perfect one-to-one pairing.

**Theorem (Product rule).** If A and B are finite, then |A × B| = |A| · |B|.

*Explanation.* An element of A × B is a pair. To describe a pair you name a
member of A and a member of B. You have |A| ways to do the first job and |B|
ways to do the second, and the two jobs are independent, so the total is the
product. The rule extends to any finite number of sets: |A₁ × … × A_k| =
|A₁| · … · |A_k|.

**Theorem (Sum rule).** If A₁, …, A_k are pairwise disjoint (no element in two
of them), then |A₁ ∪ … ∪ A_k| = |A₁| + … + |A_k|.

*Explanation.* Disjointness is the entire hypothesis and it does real work. If
the sets overlap, an element in the overlap is counted once per set it appears
in, and the sum overshoots. Correcting for overlaps is the subject of
[Lesson 23](../part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md).

**Theorem (Counting compositions).** If a process consists of k steps, step i
having n_i outcomes, and every sequence of choices is distinguishable, then the
number of complete processes is n₁ · n₂ · … · n_k.

*Explanation.* This is the product rule applied k times. Each step's outcome set
depends on nothing but the step index, so the choice sets form a Cartesian
product.

**Theorem (Bijection principle).** Two finite sets A and B have the same
cardinality if and only if a bijection A → B exists.

*Explanation.* A bijection is a re-labelling: it hands each element of A a
distinct name from B and uses every name exactly once. So counting A and
counting B give the same answer, and you may pick whichever is easier. This is
the single most useful counting technique in discrete mathematics, because the
target count is often something absurdly large while a correspondent is tiny.

**Corollary (Strings over an alphabet).** If A is an alphabet of size k, then the
number of length-n strings over A is kⁿ.

*Explanation.* Each of the n positions is one independent choice from A, so the
product rule gives k · k · … · k. The same argument with A = {0, 1} gives the
2ⁿ binary strings of length n.

**Corollary (Functions between finite sets).** The number of functions A → B is
|A|ᵇ where |A| = a and |B| = b. A bijection A → B exists exactly when a = b.

*Explanation.* A function is a string indexed by the domain: for each element of
A you must write down one element of B, independently, so b choices a times.

**Corollary (Power set).** |𝒫(A)| = 2^|A| for finite A.

*Explanation.* Bijection with {0, 1}^A. Send S ⊆ A to the string that has a 1 at
position a exactly when a ∈ S. Every subset gives a distinct string and every
string gives a distinct subset, and the strings number 2^|A| by the previous
corollary.

**Lemma (Monotonicity).** If A ⊆ B and B is finite, then |A| ≤ |B|.

*Explanation.* Restrict the identity function on A to B. It is still injective,
and no two elements of A collided into one element of B. This one line is the
whole proof, and it powers the pigeonhole principle in Lesson 23.

## Worked Example

**The question.** An internal service must mint unique user identifiers. Three
schemes are proposed. Count each one, and check them against a brute-force
enumeration.

**Scheme A — two letters then three digits.** Twenty-six letters and ten digits,
repetition allowed, positions fixed.

Each position is an independent choice, so this is the product rule:

    26 × 26 × 10 × 10 × 10 = 676 × 1000 = 676,000

Why multiply rather than add? Because the choices are *staged*: the number of
options for position 4 does not depend on what you chose for position 3. If
digits were forbidden after a digit, the choice sets would depend on earlier
answers and the plain product rule would not apply directly — you would need a
sum rule over cases. Nothing in the scheme says that, so we multiply.

**Scheme B — any 2 or 3 characters from the 36-symbol alphabet.** A length-2
string has 36² = 1,296 members; a length-3 string has 36³ = 46,656.

Here the two cases are *genuinely different* — a length-2 string is not a
length-3 string, no matter what symbols it uses, because the lengths differ. So
the cases are disjoint and the sum rule applies:

    36² + 36³ = 1,296 + 46,656 = 47,952

This is exactly why the word "or" in a counting question is a warning sign. "Two
or three characters" means add. "A letter and a digit" means multiply. When you
see "or", check whether the two branches can overlap; if they can, you owe the
reader an inclusion–exclusion correction, which is [Lesson 23](../part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md).

**Scheme C — three distinct letters, order matters.** Without repetition the
choice sets shrink as you go:

    26 × 25 × 24 = 15,600

Same product rule, but the factors are not all equal. This is where people
frequently write 26³ by mistake; the shrinking factors are the entire content
of "without repetition".

**Cross-check.** Scheme B is small enough to enumerate: 47,952 strings, built
in under a second. Enumeration is the referee. When a closed-form count and a
brute-force count disagree, one of them is wrong, and the brute-force one is
much easier to debug.

**Sizing question.** Does Scheme A fit in three bytes? Take log₂(676,000) ≈
19.4, so it needs 20 bits, which is 3 bytes. Scheme B needs log₂(47,952) ≈ 15.5,
so 2 bytes. This logarithm step is worth memorising as a habit: when a count
crosses 2⁶⁴ you have overflowed a 64-bit unsigned integer, and logs are how you
notice that before the code does.

## Runnable Code

Three helper functions that encode the two rules, then a brute-force check.

```python
from itertools import product as iproduct
from math import log2

def product_rule(*sizes):
    """Outcomes when choices are made one after another and the options do not
    depend on earlier answers: multiply."""
    total = 1
    for s in sizes:
        total *= s
    return total

def sum_rule(*sizes):
    """Outcomes when the branches are genuinely disjoint cases: add."""
    return sum(sizes)

# Scheme A: two letters then three digits. Independent positions, so multiply.
a = product_rule(26, 26, 10, 10, 10)

# Scheme B: length 2 or length 3. Disjoint cases, so add.
b = sum_rule(36**2, 36**3)

# Scheme C: three distinct letters, order matters. Product rule with shrinking
# factors because repetition is forbidden.
c = product_rule(26, 25, 24)

print(f"A  two letters + three digits : {a:,}")
print(f"B  length 2 or 3 of 36 symbols: {b:,}")
print(f"C  three distinct letters     : {c:,}")

# Brute-force referee for scheme B: generate every string and count them.
alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
listed = [s for n in (2, 3) for s in iproduct(alphabet, repeat=n)]
print(f"B  by enumeration             : {len(listed):,}  (agrees: {len(listed) == b})")

# How many bytes does a scheme need to store an index into?
for name, count in (("A", a), ("B", b), ("C", c)):
    print(f"{name}: log2 = {log2(count):6.2f} bits -> {(log2(count) // 8) + 1:.0f} bytes")
```

Now the bijection between subsets and bit strings, which is the most useful
correspondence in discrete mathematics.

```python
from itertools import combinations

def subsets_via_bits(elements):
    """Each subset of `elements` is represented by one integer mask: bit i is set
    exactly when elements[i] is in the subset. This is the bijection."""
    n = len(elements)
    return [
        frozenset(elements[i] for i in range(n) if (mask >> i) & 1)
        for mask in range(1 << n)
    ]

A = frozenset("abcd")
by_bits = subsets_via_bits(sorted(A))
# The independent count: pick a size k, then pick which k elements, for every k.
by_size = [
    frozenset(c)
    for k in range(len(A) + 1)
    for c in combinations(sorted(A), k)
]

key = lambda s: sorted(s)
print(f"|A| = {len(A)}, 2^|A| = {2**len(A)}")
print(f"subsets via bit strings : {len(by_bits)}")
print(f"subsets via sizes+combos: {len(by_size)}")
print(f"the two lists agree     : {sorted(map(key, by_bits)) == sorted(map(key, by_size))}")
print(f"empty subset present    : {frozenset() in by_bits}")

mask = 0b1010  # bit 1 and bit 3 set -> elements {'b', 'd'}
print(f"0b1010 decodes to        : {sorted(sorted(A)[i] for i in range(4) if (mask >> i) & 1)}")
```

Counting functions between sets, and the fact that a bijection needs equal
sizes.

```python
from itertools import product as iproduct, permutations

def all_functions(domain, codomain):
    """One function per string: the string's i-th entry is f(domain[i])."""
    return list(iproduct(codomain, repeat=len(domain)))

def onto(f, codomain):
    """True when the function hits every element of the codomain."""
    return set(f) == set(codomain)

A = [1, 2, 3]
B = ["a", "b", "c", "d"]
B3 = ["a", "b", "c"]

funcs = all_functions(A, B)
print(f"functions 3 -> 4 : {len(funcs)} (equals 4^3 = {4**3})")
print(f"  of those, surjective onto all 4: {sum(onto(f, B) for f in funcs)} (impossible)")
print(f"functions 3 -> 3 : {len(all_functions(A, B3))} (equals 3^3 = {3**3})")
print(f"  of those, bijective          : {sum(onto(f, B3) for f in all_functions(A, B3))} (equals 3! = 6)")

# A bijection A -> B exists only when |A| = |B|. Each bijection is a
# re-labelling, so counting bijections is counting permutations of B3.
print(f"bijections 3 -> 3 : {len(list(permutations(B3, 3)))}")
```

Counting paths in a directed acyclic graph. This is a product rule (choose one
incoming edge at each step) accumulated over levels, and it is the prototype
for the dynamic programming in [Lesson 24](../part02_discrete_combinatorics/24_recurrence_relations.md).

```python
# A tiny dependency graph, given by outgoing edges in a safe processing order.
edges = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["E"],
    "D": ["F"],
    "E": ["F"],
    "F": [],
}
order = ["A", "B", "C", "D", "E", "F"]

# ways[v] = number of paths from "A" to v. Each path into v comes from exactly
# one predecessor, so the contributions add: that is the sum rule.
ways = {v: 0 for v in order}
ways["A"] = 1  # one empty path from A to itself
for v in order:
    for w in edges[v]:
        ways[w] += ways[v]
print("paths from A to each vertex:")
for v in order:
    print(f"  {v}: {ways[v]}")

# Brute-force referee: enumerate every path to "F".
def all_paths(v, target="F"):
    if v == target:
        return [[v]]
    return [[v] + tail for w in edges[v] for tail in all_paths(w, target)]

found = all_paths("A")
print(f"paths to F by enumeration: {len(found)} -> {['-'.join(p) for p in found]}")
```

## Common Mistakes

**1. Multiplying when the branches are cases.**

> Wrong: "A packet is either text or an image, from 10 text types and 5 image types, so 10 × 5 = 50 packets."
> Right: 10 + 5 = 15 packets.
> Why the wrong one is tempting: 10 × 5 = 50 is exactly what you would write if
> a packet were *a text followed by an image*. The fix is to ask whether the
> packets are built by doing both things, or by doing one thing and stopping.

**2. Adding when the steps are sequential.**

> Wrong: "A user picks a username from 10^6 options and a password from 10^6 options, so there are 2 × 10^6 accounts."
> Right: 10^6 × 10^6 = 10^12 accounts.
> Why the wrong one is tempting: "two choices, so use the two-choice rule." The
> count of *sequences* is a product; a sum would be the count of sequences that
> stop after the first step.

**3. Treating a bijection as a coincidence.**

> Wrong: "There are 2ⁿ subsets and 2ⁿ bit strings, so they are in some sense
> interchangeable, so I can index subsets by whatever fits."
> Right: The bijection is explicit — bit i is 1 exactly when element i is in the
> subset. Without naming the correspondence, you have an equality of two numbers
> and no reason to believe the identification behaves well under anything you
> actually do (union, intersection, symmetric difference). Bitmask sets only
> work because the bijection is *compatible with the set operations*.

**4. Forgetting that positions may repeat.**

> Wrong: "There are 26 letters, choosing two gives 26 × 26 = 676 two-letter words."
> Right for distinct letters; for words it is also 676, but for the *set of two
> distinct letters* it is 26 × 25 = 650. Write down whether repetition is allowed
> before you write any formula. "26 × 25" and "26 × 26" differ by 26 — small here,
> and the difference between correct and wrong at scale.

**5. Trusting a hand count over an enumeration.**

> Wrong: computing 36³ + 36² = 47,952 and shipping it.
> Right: computing it, then generating all 47,952 strings and checking the length.
> Why the wrong one is tempting: the arithmetic is easy, so the count feels
> trustworthy. But the sum rule's hypothesis — that the cases are disjoint — is a
> claim about the *problem*, not about the arithmetic, and only enumeration
> tests that claim.

---

## Formula Sheet

Every symbol and formula this lesson introduces, in one place. `A` and `B` are
finite sets, `n` counts positions or elements, `k` counts choices available at
each position, and every count here is an exact integer — nothing in this lesson
is an approximation.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$\lvert A\rvert$` | `$\lvert A \rvert = \#\{a : a \in A\}` | the size of a finite set | the starting point for every count below |
| Product rule | `$\lvert A \times B\rvert = \lvert A\rvert \cdot \lvert B\rvert$` | make choice 1, then choice 2, and the counts multiply | "first pick a shirt, then pick trousers" |
| Product rule, `k` sets | `$\lvert A_1 \times \cdots \times A_k\rvert = \prod_{i=1}^{k} \lvert A_i\rvert$` | `k` independent choices, one per slot | passwords, schedules, execution orders |
| Counting compositions | `$\text{total} = n_1 \cdot n_2 \cdots n_k$` | step `i` has `n_i` outcomes, so the process has the product | counting complete processes step by step |
| Sum rule | `$\lvert A_1 \cup \cdots \cup A_k\rvert = \sum_{i=1}^{k} \lvert A_i\rvert$` | count each case, then add | **only** when the cases cannot coincide |
| Disjointness | `$A_i \cap A_j = \emptyset$ for every $i \ne j$` | the hypothesis the sum rule actually needs | check this before writing a `+` |
| Bijection | `$\lvert A\rvert = \lvert B\rvert` if and only if a bijection $A \to B$ exists | a perfect one-to-one pairing of two sets | finding a tiny correspondent for a huge set |
| Injective | `$f(a_1) = f(a_2) \Rightarrow a_1 = a_2$` | different inputs, different outputs | half of the definition of a bijection |
| Surjective | `$\forall b \in B,\ \exists a \in A$ with $f(a) = b$` | every element of `B` is actually hit | the other half; both are needed |
| Strings over an alphabet | `$k^{n}$` | `n` positions, `k` choices at each | keyspace and password-space sizes |
| Binary strings | `$2^{n}$` | `n` positions, two choices at each | bitmasks, flags, codewords |
| Functions `A -> B` | `$\#\{f : A \to B\} = \lvert B\rvert^{\,\lvert A\rvert} = b^{a}$` | one image per domain element, chosen freely; codomain size raised to domain size | enumerating assignments; a 3-element domain into a 4-element codomain gives $4^3 = 64$ |
| Bijections `A -> B` | `$\exists$ bijection $A \to B$ if and only if $a = b$ | equal sizes are necessary and sufficient | deciding feasibility before writing code |
| Power set | `$\lvert \mathcal{P}(A)\rvert = 2^{\lvert A\rvert}$` | every element is either in or out | flags, bitmasks, `1 << n` |
| Subset ↔ bit string | `$S \mapsto$ the string whose `i`-th bit is 1 exactly when element `i` is in `S` | the explicit pairing behind the power-set count | indexing subsets by integers; storing a subset in one word |
| Monotonicity | `$A \subseteq B \Rightarrow \lvert A\rvert \le \lvert B\rvert$` | a subset can never be larger than its container | one-line proof; powers the pigeonhole principle in [Lesson 23](../part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md) |
| Complement | `$\lvert U\rvert = \lvert A\rvert + \lvert U \setminus A\rvert$ | a set and its complement partition the universe | "at least one" constraints |
| Bits needed for `N` objects | `$\lceil \log_2 N\rceil$ bits, or `$\lfloor \log_2 N\rfloor + 1$` whole bytes | the log base 2 of a count is the width of an index into it | sizing a field; spotting a 64-bit overflow before the code does |
| `C(n, r)` | `$n! / \bigl(r!\,(n-r)!\bigr)$` | unordered choice of `r` from `n`, no repeats | developed in [Lesson 21](../part02_discrete_combinatorics/21_permutations_and_combinations.md); used in the exercises here as `math.comb` |
| `P(n, r)` | `$n! / (n-r)!$` | ordered choice of `r` from `n`, no repeats | `math.perm`; $P(5,3) = 5\cdot4\cdot3 = 60$ |
| P from C | `$P(n,r) = C(n,r)\cdot r!$` | every chosen set has exactly `r!` orderings | the cheapest self-check on any nCr/nPr pair |
| Symmetry | `$C(n,k) = C(n,n-k)$` | the complement pairing inside an `n`-set | explains why two unrelated-looking counts match |
| Unordered selection with repeats | `$C(n + r - 1, r)$` | `r` stars and `n - 1` bars, stars-and-bars | three scoops from six flavours: $C(8,3) = 56$ |
| Path counts in a DAG | `ways[v] = \sum_{u} ways[u]$ over predecessors `u` | every path into `v` arrives from exactly one predecessor | summing by level; the prototype for dynamic programming in [Lesson 24](../part02_discrete_combinatorics/24_recurrence_relations.md) |

---

## Multiple Choice Questions

**Q1.** A service sends a packet that is *either* a text message *or* an image.
There are 10 text types and 5 image types. How many distinct packets are there?

- A) 15
- B) 50
- C) 51
- D) 32,768

<details>
<summary>Answer and explanation</summary>

**A) 15.**

A packet is *one* of the two kinds, so the two cases are disjoint and the sum
rule gives 10 + 5 = 15.

- B) is Mistake 1 from this lesson: 10 × 5 = 50 is exactly what you would write
  if a packet were *a text followed by an image*. Asking "do we do both things,
  or one thing and stop?" settles it.
- C) adds one extra case that does not exist — there is no third packet type
  being counted.
- D) is a product of all the options at once, as if the choices were six
  independent decisions rather than one decision between two kinds.

</details>

**Q2.** Let `A` and `B` be finite sets with `|A| = 3` and `|B| = 4`. What must be
true?

- A) There is exactly one bijection from `A` to `B`
- B) There is no bijection from `A` to `B`
- C) There are 4³ = 64 bijections from `A` to `B`
- D) There are 3! = 6 bijections from `A` to `B`

<details>
<summary>Answer and explanation</summary>

**B) There is no bijection from `A` to `B`.**

A bijection pairs each element of `A` with a *distinct* element of `B` and uses
every element of `B`. Using all four elements of `B` needs four elements of `A`,
and there are only three. The code in the lesson makes exactly this check:
`surjective onto all 4: 0 (impossible)`.

- A) is worse than wrong — a bijection, if one existed, would never be unique.
  Re-labelling a set has at least two valid labellings whenever there is more
  than one element.
- C) is the count of *all* functions `A → B` (4³ = 64), not of bijections. Of
  those 64, none is surjective.
- D) counts bijections on a set *of the same size*: on a 3-element set there are
  indeed 3! = 6. It is the count you would get if `B` also had 3 elements.

</details>

**Q3.** Which rule pairs each subset of `{1, 2, 3, 4}` with a 4-bit string in a
way that is one-to-one and onto?

- A) The subset of size `k` is paired with the single string that has `k` ones
- B) A subset `S` is paired with the string whose `i`-th bit is 1 exactly when
  element `i` belongs to `S`
- C) A subset `S` is paired with the string that lists the elements of `S` in
  increasing order, one per position, padded on the right with 0s
- D) A subset `S` is paired with the string whose first `|S|` bits are 1 and whose
  remaining bits are 0

<details>
<summary>Answer and explanation</summary>

**B) A subset `S` is paired with the string whose `i`-th bit is 1 exactly when
element `i` belongs to `S`.**

This is the bijection the power-set corollary is proved from: every subset gives
a distinct string, and decoding a string by reading off its 1 positions gives
back exactly one subset.

- A) collapses 16 subsets onto 5 strings — the 6 subsets of size 2 would all
  become `1100`. Not injective.
- C) is not even well defined as a pairing of 16 objects onto 16 strings: the
  string length varies with the subset, and padding with 0s makes `{1}` and
  `{1, 4}` collide (`1000`).
- D) has the same defect as A in a different costume: all six 2-element subsets
  map to `1100`, so it loses the information *which* elements were chosen.

</details>

**Q4.** How many strings of length 10 over the alphabet `{0, 1}` exist?

- A) 2¹⁰ = 1024
- B) 10² = 100
- C) C(10, 2) = 45
- D) 2⁹ = 512

<details>
<summary>Answer and explanation</summary>

**A) 2¹⁰ = 1024.**

Ten positions, two choices each, independent: the product rule applied ten times
gives 2 · 2 · … · 2 = 2¹⁰. The lesson's Exercise 1 uses exactly this count and
then exhibits the bijection to the subsets of a 10-element set.

- B) swaps the two roles: it counts strings of length 2 over a 10-symbol
  alphabet. The length and the alphabet size are not interchangeable.
- C) counts the strings with *exactly two* 1s. That is a legitimate and
  interesting number, but it is 45 out of the 1024, not the total.
- D) is the answer minus one, produced by assuming the last bit is determined by
  the first nine. Nothing in the problem imposes that.

</details>

**Q5.** How many functions are there from a 3-element set to a 4-element set, and
how many of them are bijections?

- A) 3⁴ = 81 functions, and 0 of them are bijections
- B) 4³ = 64 functions, and 0 of them are bijections
- C) 4³ = 64 functions, and 6 of them are bijections
- D) 4! = 24 functions, and 6 of them are bijections

<details>
<summary>Answer and explanation</summary>

**B) 4³ = 64 functions, and 0 of them are bijections.**

A function is a string indexed by the domain, so each of the 3 domain elements
independently picks one of 4 images: 4 · 4 · 4 = 64. A bijection needs equal
sizes, and 3 ≠ 4, so there are none. The lesson's code prints
`functions 3 -> 4 : 64 (equals 4^3 = 64)`.

- A) has the bases the wrong way round: 3⁴ would count functions from a
  4-element domain to a 3-element codomain.
- C) has the right total and the wrong second half. There are 3! = 6 bijections
  *from a 3-element set to a 3-element set*, which the code confirms — but that
  is a different codomain.
- D) reports 4! = 24, which is neither the function count nor the bijection
  count; 24 is the number of permutations of a 4-element set.

</details>

**Q6.** Scheme A produces 676,000 identifiers. What is the width of an index into
that space, and how many whole bytes does it take to store one?

- A) 676,000 bits, because each identifier needs its own bit
- B) 20 bits, which rounds up to 3 whole bytes
- C) 19 bits, because 2¹⁹ = 524,288 is in the right ballpark
- D) 24 bits, because the width must be a multiple of 8

<details>
<summary>Answer and explanation</summary>

**B) 20 bits, which rounds up to 3 whole bytes.**

log₂(676,000) ≈ 19.37, and an index into `N` objects needs ⌈log₂ N⌉ bits. Since
2¹⁹ = 524,288 < 676,000 ≤ 2²⁰ = 1,048,576, nineteen bits can name only 524,288
of them, so twenty is the answer; ⌊19.37⌋ + 1 = 3 bytes.

- A) confuses the count with the width. No fixed-width index ever needs one bit
  per object; that is what makes indexing exponential in the number of bits.
- C) is the classic off-by-one from truncating instead of rounding up. It fails
  by a factor of 1.3, which is the difference between addressing half the table
  and addressing all of it.
- D) is the byte-rounded figure presented as the bit count. 3 bytes is right, but
  24 bits overstates the requirement: you do not need 24 bits of *information*.

</details>

**Q7.** Scheme B counts "any 2 or 3 characters from a 36-symbol alphabet" as
36² + 36³ = 47,952. Which argument justifies the `+`?

- A) The characters are chosen one position at a time, so this is the product
  rule
- B) A length-2 string and a length-3 string can never be the same object, so
  the two cases are disjoint and the sum rule applies
- C) The two cases can overlap, so inclusion–exclusion is required and the count
  is 36³ − 36² = 45,360
- D) The count is C(5, 2) = 10, because the only choice is how to split two and
  three characters

<details>
<summary>Answer and explanation</summary>

**B) A length-2 string and a length-3 string can never be the same object.**

Disjointness is exactly the hypothesis the sum rule needs, and here it holds
because the lengths differ. 36² = 1,296 and 36³ = 46,656, so the total is
47,952 — which the lesson checks by enumerating all 47,952 strings.

- A) describes the product rule, which is the mistake in Mistake 2 of this
  lesson: 36² · 36³ would count a length-5 string built from a length-2 part and
  a length-3 part, which is a different object entirely.
- C) invents an overlap that does not exist, and then applies inclusion–exclusion
  with the sign backwards.
- D) treats "2 or 3 characters" as a way of splitting a budget of 5, which would
  be right if the question were how to divide 5 identical objects.

</details>

**Q8.** `A ⊆ B` and both are finite. What follows?

- A) `|A| = |B|`
- B) `|A| ≤ |B|`, with equality possible but not forced
- C) `|A| ≥ |B|`
- D) `|A| ≠ |B|`, because `A` and `B` are different sets

<details>
<summary>Answer and explanation</summary>

**B) `|A| ≤ |B|`, with equality possible but not forced.**

Monotonicity: restrict the identity map on `A` to a map into `B`. It is still
injective — no two elements of `A` collided — so `|A| ≤ |B|`. Equality happens
when `A = B`.

- A) is true only in the special case `A = B`. The lesson's own example has
  `A = {1, 2}` inside `B = {1, 2, 3, 4}`, with 2 ≤ 4 and 2 ≠ 4.
- C) has the inequality reversed, which is the sign error people make because it
  "feels" like the bigger set must contain more.
- D) confuses `⊆` with `⊊`. A set is a subset of itself, and if you mean the
  proper subset you must say so. D is true for a *proper* subset and false for
  the relation as stated.

</details>

**Q9.** How many 6-character passwords over the 62 alphanumeric characters
contain **at least one** digit?

- A) 62⁶ = 56,800,235,584
- B) 52⁶ = 19,770,609,664
- C) 62⁶ − 52⁶ = 37,029,625,920
- D) 6 · 10 · 52⁵ = 22,812,241,920

<details>
<summary>Answer and explanation</summary>

**C) 62⁶ − 52⁶ = 37,029,625,920.**

The no-digit passwords use only the 52 letters, and "at least one digit" is the
complement of "no digit at all" inside the 62⁶ passwords. A set and its
complement partition the universe, so the subtraction is exact.

- A) counts *all* 6-character passwords and ignores the constraint entirely.
- B) counts the passwords the constraint *excludes*. This is the direction you
  want for "contains no digits", not for "contains at least one".
- D) counts passwords with **exactly** one digit — choose the position (6), the
  digit (10), then letters in the other five slots (52⁵). That is the count in
  the lesson's Challenge 7, and it is genuinely smaller, by exactly the
  at-least-two-digit passwords, 14,217,384,000.

</details>

**Q10.** A checkout has four steps. Step 1 has 3 options, step 2 has 3, step 3
has 2, and step 4 has 5. How many complete processes are there?

- A) 13
- B) 90
- C) 19
- D) 24

<details>
<summary>Answer and explanation</summary>

**B) 90.**

This is the counting-compositions theorem verbatim: a process of `k` steps with
`n_i` outcomes at step `i` has n₁ · n₂ · … · n_k complete processes, here
3 · 3 · 2 · 5 = 90.

- A) adds the step counts, which would be right if the customer picked *one* of
  the four steps — but a process does all four.
- C) is the same confusion applied inconsistently: a product inside each pair of
  steps and a sum between the pairs. It has no interpretation at all.
- D) counts the 4! = 24 orders in which the steps could be *performed*, a
  different question. The steps here happen in a fixed order.

</details>

---

## Subjective Questions

### Short Answer

**Q1. Define a *bijection* `f : A → B`, and say what "injective" and
"surjective" mean on their own.**

<details>
<summary>Answer</summary>

A *bijection* is a function `f : A → B` that is both **injective** (different
inputs give different outputs: if `f(a₁) = f(a₂)` then `a₁ = a₂`) and
**surjective** (every element of `B` is hit: for each `b ∈ B` there is an
`a ∈ A` with `f(a) = b`).

One-to-one pairing only, the other only, is not a bijection. A function `A → B`
with more domain elements than codomain elements can never be injective; one
with fewer can never be surjective. "Bijection" is a single word for "both at
once", which is why the bijection principle can say equal sizes rather than
listing two conditions.

</details>

**Q2. State the product rule and the sum rule, and name the hypothesis the sum
rule needs and does not need.**

<details>
<summary>Answer</summary>

**Product rule.** For finite `A` and `B`, `|A × B| = |A| · |B|`. It extends to
`|A₁ × … × A_k| = |A₁| · … · |A_k|`. No hypothesis beyond finiteness: the two
choices are *staged*, and the number of options for the second does not depend
on the first.

**Sum rule.** For pairwise disjoint `A₁, …, A_k`,
`|A₁ ∪ … ∪ A_k| = |A₁| + … + |A_k|`. The hypothesis is **disjointness**
(`A_i ∩ A_j = ∅` for `i ≠ j`). Without it the sum overshoots, because an element
in the overlap is counted once per set containing it. Correcting that overshoot
is the subject of
[Lesson 23](../part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md).

</details>

**Q3. How many subsets does a 5-element set have? Give the formula, and explain
where it comes from in one sentence.**

<details>
<summary>Answer</summary>

`|𝒫(A)| = 2^|A| = 2⁵ = 32`.

It comes from the bijection with `{0, 1}^A`: send `S ⊆ A` to the 5-bit string
whose `i`-th bit is 1 exactly when element `i` is in `S`. Each element
independently is either in or out, and the product rule gives 2 · 2 · 2 · 2 · 2.

</details>

**Q4. How many functions are there from an `a`-element set to a `b`-element set?
When is one of them a bijection?**

<details>
<summary>Answer</summary>

`b^a` — the codomain size raised to the domain size. Each of the `a` domain
elements independently picks one of `b` images, which is the product rule applied
`a` times. A 3-element domain into a 4-element codomain gives 4³ = 64.

A bijection exists **exactly when `a = b`**, by the bijection principle. When
`a = b`, each bijection is a re-labelling, so the number of them is `a!`.

</details>

**Q5. A count `N` needs an index of fixed width. How do you get that width from
`N`, and when does it matter?**

<details>
<summary>Answer</summary>

Take `log₂ N` and round up: `⌈log₂ N⌉` bits, because an `m`-bit index names at
most 2ᵐ objects. In whole bytes that is `⌊log₂ N⌋ + 1`.

For `N = 676,000`: log₂ ≈ 19.37, so 20 bits, so 3 bytes.

It matters twice. First, as sizing: it is how you decide whether an index fits
in a 16-bit or 32-bit field. Second, as a warning: any count that crosses 2⁶⁴
has overflowed a 64-bit unsigned integer, and the logarithm is how you notice
that *before* the code does.

</details>

### Long Answer

**Q1. The worked example counts Scheme B as 36² + 36³ and then enumerates all
47,952 strings to check. What exactly does that enumeration test that the
arithmetic cannot?**

<details>
<summary>Model answer</summary>

The arithmetic only computes a number. Whether that number is the *right* number
depends entirely on a claim about the problem that arithmetic cannot see: that the
two branches "length 2" and "length 3" are disjoint. That claim is a modelling
judgement, not an arithmetic step. `36² + 36³` is correct arithmetic for the sum
rule, and it is the wrong number the moment the two branches can coincide.

Enumeration tests the modelling claim directly. Generating every string of length
2 and every string of length 3 and counting the list gives 1,296 + 46,656 = 47,952
by a route that never used the sum rule at all — it used the definition of what
the objects *are*. If the two branches had overlapped, the enumeration would have
counted the overlapping objects once (or visibly twice, in which case the list
itself is wrong), and the two numbers would disagree. That disagreement localises
the fault to the hypothesis rather than to the multiplication.

There is a second thing enumeration tests that the closed form cannot: the
character of the objects. The closed form 36² + 36³ is also the answer to "how
many ways to pick two symbols and then three symbols as two separate choices".
The two problems have the same arithmetic and different answers. Only building
the objects tells them apart.

This is why the habit matters beyond this lesson. A formula encodes a solution to
a problem, and the expensive part of counting is recognising the problem. When
the state space is small enough to enumerate — and it usually is, at least in
part — enumeration is the referee. The lesson's own closing advice is the same
point stated as a workflow: write down the count, then build it, then compare.

</details>

**Q2. What is the decision procedure for choosing between the product rule and
the sum rule? Apply it to the lesson's three identifier schemes and to the
outfit example from the opening.**

<details>
<summary>Model answer</summary>

Ask one question: **does making choice 1 change how many options choice 2 has?**

If the number of options at the next step is unaffected by what you already
chose, the process is *staged* and you multiply — the product rule. If instead
the alternatives are branches of a single decision, where each branch is a
different kind of object and you finish after one of them, you add — the sum
rule, and only after checking that the branches cannot coincide.

Applied to the schemes. Scheme A (two letters then three digits) is staged:
position 4 has ten options whichever letters you used, so
26 · 26 · 10 · 10 · 10 = 676,000. Scheme B ("2 or 3 characters") is branched:
a length-2 string is never a length-3 string, so the cases are disjoint and you
add, 36² + 36³ = 47,952. Scheme C (three distinct letters) is staged, but the
choice set *shrinks* because repeats are banned: 26 · 25 · 24 = 15,600, not 26³.
Multiplication stays multiplication; the factors just stop being equal.

Applied to the outfit example: five shirts and three pairs of trousers give one
shirt *and then* one pair, staged and independent, so 5 · 3 = 15. The word "or"
is the warning sign that switches the question to addition — "a shirt *or* a
pair" is one object of one kind, giving 5 + 3 = 8, and the two branches are
trivially disjoint because a shirt is not a pair of trousers.

The two failures are symmetric and equally common. Adding when the steps are
sequential undercounts by the number of genuine interleavings; multiplying when
the branches are cases overcounts by the number of ways the branches could have
been combined, which is why 10 × 5 = 50 is the classic wrong answer for "either a
text or an image". Neither rule is safer by default; the question above decides.

</details>

**Q3. Why does the lesson insist that finding a bijection is the creative step,
rather than just a convenient trick? What would break if two sets merely had the
same size?**

<details>
<summary>Model answer</summary>

Knowing only that `|𝒫(A)| = 2^|A| = 2^|A|` tells you two counts are equal. It
tells you nothing about *which* subset corresponds to *which* bit string, so any
operation you perform on one side has no defined counterpart on the other. The
equality of two numbers is not a structure.

What the explicit bijection supplies is that structure. Send `S ⊆ A` to the
string with a 1 at position `a` exactly when `a ∈ S`, and now every operation on
subsets has an exact mirror: union becomes bitwise OR, intersection becomes AND,
complement becomes NOT, and `S ∪ T` corresponds precisely to the string whose 1s
are those of `S` together with those of `T`. That compatibility is exactly what
makes a bitmask set a legitimate representation rather than a coincidence of
cardinalities. It is why `mask_a | mask_b` computes a union and why a bitmask DP
can move a subset from one state to another by a single machine instruction.

The same point is why the lesson treats "the numbers happen to match" as the
error it is in Mistake 3. If you index subsets by whatever fits, you may well
produce the right *count* of states and still have no way to move between them,
no way to detect equality, and no way to invert the index. The power-set count
tells you how many DP states there are — a genuine and important fact, the reason
`C(8,3) = 56` is a manageable state space while 2⁸ = 256 states of a different
kind are not. But it is the bijection, not the count, that turns that number
into a representation you can compute with.

</details>

**Q4. Why does `|A₁ ∪ … ∪ A_k| = |A₁| + … + |A_k|` need disjointness, while
`|A × B| = |A| · |B|` needs nothing at all? Explain what each hypothesis is
really doing.**

<details>
<summary>Model answer</summary>

The product rule's job is to count *pairs*, and pairs are self-identifying: the
element `(a, b)` tells you unambiguously which `a` you chose and which `b` you
chose, because the two coordinates are separate slots. Writing down `a` then
writing down `b` produces exactly one pair, and different choices produce
different pairs. So the counting is honest with no conditions: the total really
is the number of things you could have written down.

The sum rule's job is to count a *union*, which is a set of objects with no
slots. Once the objects are dumped in a common bucket, the pairing between
"object" and "the set it came from" is lost. `|A₁| + |A₂|` is what you get if you
count each bucket separately and add — but that counts the *labelled* appearances
`(x, which set it came from)`, not the objects. When the buckets are disjoint,
every object appears in exactly one bucket and the two counts coincide. When they
overlap, an element in `A₁ ∩ A₂` contributes two appearances and one object, so
the sum overcounts by exactly `|A₁ ∩ A₂|`.

That diagnosis is why
[Lesson 23](../part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md)
exists: subtracting the pairwise overlaps restores the doubly-counted elements
to 1, and the alternating signs then handle the fact that the subtraction itself
double-counted the elements that were in three sets. The alternation is not a
pattern to memorise; each pass cancels the error made by the previous one, and
the residual coefficient of an element in exactly `r` sets is the alternating
binomial sum `Σ_{j=1..r} (−1)^{j+1} C(r, j) = 1`.

So the product rule needs no hypothesis because slots keep the information that
distinguishes choices; the sum rule needs disjointness precisely because a union
destroys that information, and disjointness is the condition under which nothing
is lost.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — Bit strings.** How many strings of length 10 over the alphabet
{0, 1} exist? Give a bijection to something whose size you can compute without
multiplying.

<details>
<summary>Solution</summary>

Each of the 10 positions is an independent choice from a 2-element set, so the
product rule gives 2 · 2 · … · 2 = 2¹⁰ = 1024.

For the bijection: send the string s₁s₂…s₁₀ to the *subset of positions* that
contain a 1. That subset is a subset of {1, …, 10}, so there are 2¹⁰ of them by
the power-set corollary, and each subset decodes back to exactly one string.

```python
print(2**10)
```
</details>

**[ ] Exercise 2 — Two-letter words.** How many two-letter sequences can be
formed from 26 letters if repetition is allowed? What is the count if the two
letters must be different? Explain which rule each uses.

<details>
<summary>Solution</summary>

Repetition allowed: 26 × 26 = 676 by the product rule — the second position has
26 options regardless of the first.

Letters must differ: 26 × 25 = 650, also the product rule, but the second factor
is 25 because one letter is now unavailable. The rule is unchanged; the choice
set shrinks.

```python
print(26 * 26, 26 * 25)
```
</details>

**[ ] Exercise 3 — Functions and bijections.** How many functions are there from
a 3-element set to a 4-element set? How many of those are bijections? Justify
the second answer without counting.

<details>
<summary>Solution</summary>

Functions: 4³ = 64. Each of the three domain elements independently picks one of
four images.

Bijections: none. A bijection pairs every element of A with a distinct element of
B, so |A| must equal |B|. Here 3 ≠ 4, so a bijection is impossible by the
bijection principle's direction: no pairing can use all four elements of B while
using only three elements of A.

```python
print(4**3)
```
</details>

**[ ] Exercise 4 — Passwords with a constraint.** How many 6-character passwords
over the 62 characters (26 upper, 26 lower, 10 digits) contain **at least one
digit**? Show the answer as a subtraction and explain why the subtraction is
valid.

<details>
<summary>Solution</summary>

All passwords: 62⁶ = 56,800,235,584.

Passwordes with no digit at all use only the 52 letters: 52⁶ = 19,770,609,664.

The at-least-one set is the complement of the no-digit set within the all-passwords
set, and a finite set and its complement partition it, so

    62⁶ − 52⁶ = 56,800,235,584 − 19,770,609,664 = 37,029,625,920

```python
print(62**6, 52**6, 62**6 - 52**6)
```
</details>

**[ ] Exercise 5 — Dice.** How many outcomes are possible when three fair
six-sided dice are rolled, if the dice are distinguishable (red, green, blue)?
How many unordered triples are possible? What counts are these, and what is the
relationship between them?

<details>
<summary>Solution</summary>

Distinguishable dice: 6 · 6 · 6 = 216, product rule.

Unordered triples (multisets of size 3 from 6 faces): the relationship is not a
simple ratio. The count is 6 with one die, 21 with two, and 56 with three. The
honest general method is the sum rule over multiplicity patterns: for three dice
sort the counts (3), (2,1), (1,1,1):

    6  +  6·5  +  C(6,3)  =  6 + 30 + 20 = 56

This is a preview of [Lesson 21](../part02_discrete_combinatorics/21_permutations_and_combinations.md): an
unordered selection with repetition is a combination *with repetition*, and
C(6 + 3 − 1, 3) = C(8, 3) = 56.

```python
from math import comb
print(6**3, comb(8, 3))
```
</details>

**[ ] Exercise 6 — Subsets of a power set.** A flag set has 8 boolean flags, each
on or off. How many distinct configurations exist? How many are non-trivial (at
least one flag on)? A configuration and its complement are considered the same
for a 4-bit checksum field — how many equivalence classes are there, and what
does that require?

<details>
<summary>Solution</summary>

Configurations: 2⁸ = 256, product rule (eight independent binary choices).

Non-trivial: 256 − 1 = 255. The one excluded configuration is "all flags off".

Pairing each configuration with its complement gives 256/2 = 128 pairs. Getting a
sensible answer requires that no configuration equal its own complement. For odd
width that fails: the 1-bit string "1" is its own complement, and "1" pairs with
"0" anyway; but consider that every pair {s, ~s} has two distinct members only
when the width is at least 1 and the field is a two's-complement integer of
nonzero width — the fixed point would need s = ~s bitwise, which is impossible
for any bit position. So all 128 classes exist.

For this pairing to be an *equivalence relation* (so it partitions cleanly, as in
[Lesson 25](../part02_discrete_combinatorics/25_relations_and_equivalence_classes.md)), use "equal up to complement":
two configurations are related when they are equal or complementary. That relation
is reflexive, symmetric, and transitive.

```python
print(2**8, 2**8 - 1, 2**8 // 2)
```
</details>

**[ ] Challenge 7 — Exactly one digit.** How many 6-character passwords over the
62-character alphabet contain **exactly one** digit? Then how many contain at
least two digits?

<details>
<summary>Solution</summary>

Exactly one digit: choose the position (6 ways), choose the digit (10 ways), and
fill the other five positions with letters (52 choices each). All three choices
are sequential and independent of each other, so the product rule gives

    6 · 10 · 52⁵ = 6 · 10 · 380,204,032 = 22,812,241,920

At least two digits: take all passwords and subtract the zero-digit ones and the
exactly-one-digit ones:

    62⁶ − 52⁶ − 6·10·52⁵ = 37,029,625,920 − 22,812,241,920 = 14,217,384,000

That second line is inclusion–exclusion in miniature — subtracting a set from
another, then noticing they overlap and subtracting the overlap. It is exactly
what [Lesson 23](../part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md) generalises.

```python
total = 62**6
no_digit = 52**6
one_digit = 6 * 10 * 52**5
print(total, no_digit, one_digit, total - no_digit - one_digit)
```
</details>

**[ ] Exercise 8 — Check every rule with `math.comb` and `math.perm`.** Let
$A = \{a,b,c,d,e\}$ be a 5-element set. Answer: (a) how many subsets does $A$
have; (b) how many 3-element subsets; (c) how many ordered triples of *distinct*
elements; (d) how many 2-element subsets; (e) how many unordered selections of 3
elements *with repetition*. Express (b)–(e) using `math.comb` or `math.perm`, then
confirm every number against a brute-force enumeration. Note which enumerator is
needed for (e) and why the naive one is wrong.

<details>
<summary>Solution</summary>

(a) `$\lvert\mathcal{P}(A)\rvert = 2^5 = 32$`, by the power-set corollary.

(b) Order irrelevant, no repeats: `comb(5, 3) = 10`.

(c) Order matters, no repeats: `perm(5, 3) = 5 · 4 · 3 = 60`. Cross-check:
`comb(5, 3) · 3! = 10 · 6 = 60`, so the two formulas agree.

(d) `comb(5, 2) = 10`. The fact that (b) and (d) come out equal is not luck: it is
the symmetry `$\binom{n}{k} = \binom{n}{n-k}$` with $n = 5$, $k = 3$ and $k = 2$.
Being able to say *why* two unrelated-looking counts coincide is the difference
between having computed a number and having understood it.

(e) Unordered with repeats: `comb(5 + 3 - 1, 3) = comb(7, 3) = 35`.

The enumeration for (e) is the subtle one. `itertools.combinations(A, 3)` forbids
repetition, so it gives 10, not 35. `itertools.product(range(5), repeat=3)`
filtered by a sum condition counts *ordered* triples of multiplicities, which is a
different object again. The enumerator that matches "unordered, repeats allowed"
is `itertools.combinations_with_replacement`.

```python
from itertools import combinations, combinations_with_replacement, permutations
from math import comb, perm

A = "abcde"

masks = [frozenset(A[i] for i in range(5) if (m >> i) & 1) for m in range(1 << 5)]
print("subsets         :", len(masks), "== 2^5 =", 2**5)

subs3 = list(combinations(A, 3))
print("3-subsets       :", len(subs3), "== comb(5,3) =", comb(5, 3))

perms3 = list(permutations(A, 3))
print("ordered triples :", len(perms3), "== perm(5,3) =", perm(5, 3))

print("2-subsets       :", len(list(combinations(A, 2))), "== comb(5,2) =", comb(5, 2))

multi = list(combinations_with_replacement(A, 3))
print("with repetition :", len(multi), "== comb(7,3) =", comb(7, 3))
print("P/C ratio       :", perm(5, 3) // comb(5, 3), "== 3! =", 6)
```

Output:

```
subsets         : 32 == 2^5 = 32
3-subsets       : 10 == comb(5,3) = 10
ordered triples : 60 == perm(5,3) = 60
2-subsets       : 10 == comb(5,2) = 10
with repetition : 35 == comb(7,3) = 35
P/C ratio       : 6 == 3! = 6
```

Note `combinations_with_replacement("abcde", 3)` enumerates non-decreasing triples
such as `('a','a','b')`, and it produces each multiset exactly once — that is the
programming counterpart of the stars-and-bars bijection, which writes r stars and
n − 1 bars and reads off the multiplicities from the gaps.

</details>

## Summary

- The **product rule** counts sequences of independent choices; the **sum rule**
  counts disjoint cases. Deciding between them is most of the skill.
- A **bijection** is a one-to-one correspondence; two finite sets have the same
  size exactly when one exists, and finding it is usually the creative step.
- The product rule applied n times to an alphabet of size k gives kⁿ: strings,
  functions A → B, and the 2ⁿ subsets all come from this one line.
- "Or" in a counting question hints at a sum; "and" hints at a product. Check
  whether the branches actually overlap before committing.
- With repetition, choice sets stay at full size. Without repetition, they shrink
  — 26 · 25 · 24, not 26³.
- When a count looks unfamiliar, enumerate it. Brute force is the referee that
  catches a misapplied rule.
- log₂ of a count tells you how many bits or bytes an index into that space needs,
  and warns you before a 64-bit counter overflows.

## Next

[Lesson 21 — Permutations, Combinations, and Choosing With Limits](../part02_discrete_combinatorics/21_permutations_and_combinations.md)
assumes you can tell the product rule from the sum rule and trust a bijection;
it turns that into the nCr and nPr formulas and the decision rule for choosing
between them.