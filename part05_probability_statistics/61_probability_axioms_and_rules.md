# 61 — Probability Axioms and Rules

**Part**: part05_probability_statistics · **Prerequisites**: 24 · **Time**: 30 min

---

## In Plain Words

Last lesson we said a probability is "any function that satisfies three rules".
This lesson writes those three rules down and derives everything else from them.
There are only three. They are: a probability is never negative, the certain
event has probability 1, and if you cut the sample space into pieces, the
probabilities of the pieces add up to 1.

Everything you use in practice falls out of those three lines. If you know the
probability of two things happening, the addition rule gives you the
probability of at least one of them. If you know the probability of a thing
*not* happening, subtracting from 1 gives you the probability of it happening.
If you know three overlapping events, inclusion–exclusion handles the
double-counting for you. None of these are extra facts about the world — they
are consequences of the axioms, which is exactly why they never fail, even for
weird mechanisms like loaded dice or cryptographic key collisions.

The single most useful habit in this lesson: when you are unsure how to combine
two events, draw a picture of the sample space as a rectangle and mark the
events as regions. Overlap is subtraction, no overlap is addition, and the
picture never lies.

## Why Computer Science Cares

- **Hash table sizing.** The birthday calculation decides when you must resize a
  table. Rehashing a million-entry table because you ignored it is a real
  outage, and the number that triggers it comes straight out of this lesson.
- **Tail latency budgets.** If one in 1000 requests is slow, "at least one slow
  request in a batch of 500" is not 0.5 — it is about 0.39, by inclusion–
  exclusion or the complement. SRE error budgets are computed this way.
- **Independent feature assumptions.** Naive Bayes assumes features are
  independent precisely because the multiplication rule then factors, turning
  an intractable joint distribution into a product of small ones
  ([Lesson 62](../part05_probability_statistics/62_conditional_probability_and_bayes.md)).
- **Monte Carlo error bars.** Union bound gives the "at most this many standard
  errors" reasoning behind simulation confidence intervals
  ([Lesson 68](../part05_probability_statistics/68_law_of_large_numbers_and_clt.md)).
- **A/B test overlap.** If variants A and B are not disjoint — for instance two
  mutually exclusive UI states on the same page — naive addition of their
  click-through rates double counts, and the discrepancy grows with the number
  of variants.

## The Formal Version

All statements below assume an experiment with sample space Ω and a function P
defined on subsets of Ω. From [Lesson 60](../part05_probability_statistics/60_probability_foundations.md), we
now say precisely what "a function P" means.

**Axiom 1 (non-negativity).** For every event A, P(A) ≥ 0.

**Axiom 2 (normalisation).** P(Ω) = 1.

**Axiom 3 (countable additivity).** If A₁, A₂, A₃, … are **pairwise disjoint**
events (no outcome lies in two of them), then

    P(A₁ ∪ A₂ ∪ A₃ ∪ ⋯) = P(A₁) + P(A₂) + P(A₃) + ⋯

"Countable" means the list may be infinite; the infinite sum is the limit of the
finite partial sums. Axiom 3 with a single event A₁ = Ω gives
P(Ω) = P(A₁), i.e. P(∅) = 0, so the empty set needs no separate axiom.

That is the entire definition. Everything below is a theorem.

### Derived fact 1 — the complement rule

For every event A, since Ω is the disjoint union of A and Aᶜ,

    P(Aᶜ) = 1 − P(A)          and          P(A) = 1 − P(Aᶜ)

**Explanation.** The two sets A and Aᶜ are disjoint and their union is Ω, so
Axiom 3 plus Axiom 2 give P(A) + P(Aᶜ) = 1.

This is the most-used rule in the subject, because "at least one" and "exactly
one" style questions are much easier via their complements.

### Derived fact 2 — monotone events

If A ⊆ B then P(A) ≤ P(B), because B is the disjoint union of A and B \ A:
P(B) = P(A) + P(B \ A) ≥ P(A).

### Derived fact 3 — the addition rule

For **any** two events A and B, whether or not they overlap,

    P(A ∪ B) = P(A) + P(B) − P(A ∩ B)

If A and B are **disjoint** the intersection term vanishes and you may simply
add: P(A ∪ B) = P(A) + P(B). Such events are also called *mutually exclusive*.

**Explanation.** A ∪ B is the disjoint union of A, B \ A and A ∩ B, so
P(A ∪ B) = P(A) + P(B) + P(A ∩ B) − P(A) = P(A) + P(B) − P(A ∩ B).

### Derived fact 4 — the multiplication rule

For any A and B with P(B) > 0,

    P(A ∩ B) = P(B) · P(A | B)

where P(A | B) is conditional probability: the probability of A *given* that B
has occurred, defined as P(A ∩ B) / P(B). So the joint probability is the
probability of the conditioner times the conditional probability.

When A and B are **independent**, meaning P(A | B) = P(A), the rule collapses to

    P(A ∩ B) = P(A) · P(B)

**Independence is an assumption, never a conclusion.** Two events are
independent exactly when knowing one gives you no information about the other,
and this must be argued from the mechanism, not inferred from the fact that you
could not see a pattern.

### Derived fact 5 — inclusion–exclusion for three or more events

For three events, applying the addition rule twice gives

    P(A ∪ B ∪ C) = P(A) + P(B) + P(C)
                 − P(A∩B) − P(A∩C) − P(B∩C)
                 + P(A∩B∩C)

The pattern: add all singles, subtract all pairs, add all triples. For four
events the last term is −P(A∩B∩C∩D). The general formula alternates signs:

    P(A₁ ∪ ⋯ ∪ Aₙ) = Σⱼ |Aⱼ| − Σ_{j<k} |Aⱼ ∩ Aₖ| + Σ_{j<k<l} |Aⱼ ∩ Aₖ ∩ Aₖ| − ⋯

**Explanation.** Each outcome in *m* of the sets is counted C(m,2) times by the
pair subtractions, C(m,3) times by the triple additions, and so on. The
alternating signs make the net count exactly 1 for every outcome (this is the
binomial identity Σ_{k=0}^{m} (−1)^k C(m,k) = 0 for m ≥ 1, proven in
[Lesson 14](../part01_logic_proof/14_mathematical_induction.md)). This is the
same object as the set-theoretic inclusion–exclusion principle of
[Lesson 23](../part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md),
specialised to cardinalities.

### Derived fact 6 — the union bound

For any events A₁, …, Aₙ, whether or not they overlap,

    P(A₁ ∪ ⋯ ∪ Aₙ) ≤ P(A₁) + ⋯ + P(Aₙ)

**Explanation.** Inclusion–exclusion is an alternating sum of non-negative terms.
Discarding every negative term and every higher-order positive term can only
lower the result, and the pair terms are also non-negative, so the total is at
most the sum of the singles. This bound is usually loose but it is free: it
works no matter how tangled the overlap is, and it is the standard tool for
"what is the chance anything at all goes wrong".

For three events the bound is tightened by the pair terms alone (Bonferroni):
P(A ∪ B ∪ C) ≥ ΣP(A) − ΣP(A∩B).

## Worked Example

### Example A — the birthday problem, all the way through

There are 365 days in a year (ignore leap years). A group of *k* people arrives.
Find the probability that at least two share a birthday.

**Step 1 — set up.** The outcome space is the assignment of birthdays to the k
people: 365^k equally likely outcomes. The event of interest is
"some two people collide", which is unpleasant to count directly.

**Step 2 — take the complement.** The complement is "all birthdays distinct".
That is beautifully countable, because it factors step by step.

**Step 3 — count the complement by a product.** Assign birthdays one person at a
time:

    person 1: 365 choices (all allowed)
    person 2: 364 choices (one day taken)
    person 3: 363 choices (two days taken)
    ...
    person k: 366 − k choices

So P(all distinct) = (365 · 364 · 363 · ⋯ · (366 − k)) / 365^k = Π_{j=0}^{k−1} (365 − j)/365.

Note this product *is* the multiplication rule applied k−1 times, with each step
being a conditional probability.

**Step 4 — subtract.** P(collision) = 1 − Π_{j=0}^{k−1}(365 − j)/365.

Evaluate:

| k people | P(no shared birthday) | P(at least one shared birthday) |
| --- | --- | --- |
| 10 | 0.8831 | 0.1169 |
| 20 | 0.5886 | 0.4114 |
| 22 | 0.5243 | 0.4757 |
| 23 | 0.4927 | 0.5073 |
| 30 | 0.2937 | 0.7063 |

So **with 23 people there is a better-than-even chance of a shared birthday**.

**Step 5 — be suspicious.** This feels absurd, so audit it. The intuition "23
people cannot fill 365 days" is the wrong model; the model is pairs. Each pair of
people has a 1/365 ≈ 0.00274 chance of colliding, and there are C(23,2) = 253
pairs. Summing gives 253/365 ≈ 0.693 — an *over*estimate, because a birthday
shared by three people gets counted three times. The union bound (0.693) is an
upper bound and the exact answer (0.507) is lower, exactly as the theory in
[Lesson 60](../part05_probability_statistics/60_probability_foundations.md) predicts: more overlap ⇒ smaller
union. This is a nice demonstration that intuition about "how full the calendar
is" is the wrong model, and pair counting is the right one.

**Why engineers care.** With 32-bit hashes and 77,163 entries, the collision
probability passes 50%. That is why Python's `dict` grows when it is about 2/3
full, and why database B-trees do not wait for 100%.

### Example B — inclusion–exclusion with three overlapping events

From a standard 52-card deck one card is drawn. Let:

- A = it is an ace (4 cards)
- B = it is a king (4 cards)
- C = it is a red card (26 cards)

Find P(A ∪ B ∪ C).

**Step 1 — singles.** P(A) = 4/52, P(B) = 4/52, P(C) = 26/52.

**Step 2 — pairs.** A ∩ B = ∅, since no card is both an ace and a king, so
P(A∩B) = 0. A ∩ C = the two red aces, so P = 2/52. By symmetry B ∩ C = 2/52.

**Step 3 — triple.** A ∩ B ∩ C = ∅ (the empty intersection from A ∩ B), so
P = 0.

**Step 4 — combine.**

    P(A∪B∪C) = (4 + 4 + 26)/52 − (0 + 2 + 2)/52 + 0/52
              = 34/52 − 4/52
              = 30/52 ≈ 0.576923

**Step 5 — check by complement.** The complement is "not an ace, not a king, not
red" = a black card that is neither ace nor king. Black cards: 26. Black aces: 0.
Black kings: 0. So all 26 black non-face cards qualify: 26/52. And
1 − 26/52 = 30/52. ✓ Two independent derivations agree, as they must.

Note the red card was already counted in A and in B, so the pair subtractions
remove exactly those two double counts. Forgetting that step gives 34/52 ≈
0.6538, which would claim you see a face card more often than you actually do.

## Runnable Code

### Checking the axioms and the addition rule by brute force

```python
from itertools import product
from fractions import Fraction

# A tiny experiment we can inspect entirely: three independent fair coins.
# The sample space has 2^3 = 8 outcomes, so we can list every event and every
# probability EXACTLY as fractions -- no floating point, no sampling error.
outcomes = list(product([0, 1], repeat=3))
weights = {o: Fraction(1, len(outcomes)) for o in outcomes}


def p(event):
    """Probability of a set of outcomes, as an exact Fraction."""
    return sum((weights[o] for o in event), Fraction(0))


def complement(event):
    return [o for o in outcomes if o not in event]


omega = set(outcomes)
a = {o for o in outcomes if o[0] == 1}
b = {o for o in outcomes if o[1] == 1}

print("Axiom 1 (non-negativity)  :", all(p(e) >= 0 for e in [a, b, omega, set()]))
print("Axiom 2 (normalisation)  :", p(omega), "== 1 ->", p(omega) == 1)
print("Axiom 3 (Axiom 2 on empty):", p(set()), "== 0 ->", p(set()) == 0)

# Axiom 3 for a disjoint partition of the sample space.
parts = [{(1, 1, 0), (1, 1, 1)}, {(1, 0, 0), (1, 0, 1)}, {(0, 1, 0), (0, 1, 1)},
         {(0, 0, 0), (0, 0, 1)}]
print("Axiom 3 (disjoint sum)   :", sum((p(x) for x in parts), Fraction(0)), "== 1")

# Derived fact 1: complements.
print()
print("P(A)                 =", p(a))
print("P(A complement)      =", p(complement(a)))
print("P(A) + P(A compl)    =", p(a) + p(complement(a)))

# Derived fact 3: addition rule with and without overlap.
print()
print("A and B overlap in    :", sorted(a & b))
print("P(A union B)         =", p(a | b))
print("naive sum P(A)+P(B)  =", p(a) + p(b), " (too big by exactly P(A and B) =", p(a & b), ")")
```

### Inclusion–exclusion against brute-force enumeration

```python
from itertools import combinations
from math import comb
from fractions import Fraction

deck = [rank + suit for suit in "SHDC" for rank in "23456789TJQKA"]
total = len(deck)

is_ace = lambda c: c[0] == "A"
is_king = lambda c: c[0] == "K"
is_red = lambda c: c[1] in ("H", "D")

A = {c for c in deck if is_ace(c)}
B = {c for c in deck if is_king(c)}
C = {c for c in deck if is_red(c)}

union_direct = len(A | B | C) / total

# Inclusion-exclusion for three events, computed from the SET sizes.
n1 = len(A) + len(B) + len(C)
n2 = len(A & B) + len(A & C) + len(B & C)
n3 = len(A & B & C)
union_formula = (n1 - n2 + n3) / total

print(f"|A|={len(A)}  |B|={len(B)}  |C|={len(C)}")
print(f"|A and B|={len(A&B)}  |A and C|={len(A&C)}  |B and C|={len(B&C)}")
print(f"|A and B and C|={len(A & B & C)}")
print()
print(f"singles sum          = {n1}/{total}")
print(f"pairs sum            = {n2}/{total}")
print(f"inclusion-exclusion  = {union_formula:.6f}   ({n1}-{n2}+{n3})/{total}")
print(f"brute-force union    = {union_direct:.6f}")
print(f"agree: {abs(union_formula - union_direct) < 1e-12}")
print()
print(f"forgetting the pair terms gives {n1 / total:.6f} -- an overcount.")
```

### The birthday problem and the union bound

```python
from math import comb, prod

DAYS = 365


def p_shared_birthday(k):
    """1 - P(all distinct), written exactly as the product from the worked example."""
    p_all_distinct = prod((DAYS - j) / DAYS for j in range(k))
    return 1 - p_all_distinct


# The union bound from Derived fact 6: count PAIRS of people instead of
# enumerating outcomes. Each pair collides with probability 1/DAYS, and there
# are C(k,2) pairs, so P(at least one collision) <= C(k,2)/DAYS.
print("people | exact P(shared) | union bound C(k,2)/365")
for k in (10, 20, 22, 23, 30, 57):
    exact = p_shared_birthday(k)
    bound = min(1.0, comb(k, 2) / DAYS)
    print(f"{k:6d} | {exact:14.4f} | {bound:.4f}")

print()
print("Note the exact answer is always BELOW the bound: a day shared by three")
print("people is counted three times by the pair argument but must count once.")


# The same calculation decides when a hash table must resize.
def p_hash_collision(n, bits=32):
    """P(two of n 32-bit hashes collide) -- the birthday problem in a huge space."""
    space = 2 ** bits
    p_all_distinct = prod((space - j) / space for j in range(n))
    return 1 - p_all_distinct


print()
print(f"{'entries':>9} | P(collision in a 2^32 space)")
for n in (1_000, 10_000, 50_000, 77_163, 100_000, 200_000):
    print(f"{n:9,} | {p_hash_collision(n):.4f}")
```

## Common Mistakes

**Mistake 1 — adding probabilities of overlapping events.**
Wrong: "P(A) = 0.1 and P(B) = 0.2, so P(A or B) = 0.3."
Right: 0.3 − P(A ∩ B). The addition rule is a statement about *sets*, and sets
overlap. The temptation is that adding is what you did in high school for
independent events, and overlapping events feel like they should be smaller than
independent ones — which they are, which is exactly the point.

**Mistake 2 — treating independence as automatic.**
Wrong: "These are different log lines, so their errors are independent."
Right: independence is a claim about the mechanism and must be argued. Two
requests hitting the same database will fail together; two requests to a
randomly chosen data centre usually will not. Assuming independence is the
single most common statistical error in systems work, because it makes
overlapping probabilities look smaller and failure bounds look better.

**Mistake 3 — using the product rule without the independence hypothesis.**
Wrong: P(A∩B) = P(A)P(B) applied to "two draws from a deck without
replacement." The draws are dependent: after an ace, the next card is more
likely to be a non-ace. The temptation is that P(A∩B) = P(A)P(B) looks like a
definition rather than a special case.

**Mistake 4 — forgetting that inclusion–exclusion only needs the pair terms to
be zero in the easy case, not the singles.** A frequent slip in the other
direction: seeing A ∩ B = ∅ and dropping the rest of the formula. If A and B are
disjoint but C overlaps both, you still need all three pair terms and the
triple term.

**Mistake 5 — using the union bound as if it were exact.** It is an *upper*
bound, so it can only ever tell you "at most this". Saying "P(at least one
failure) ≈ 0.39" when your inputs were three independent 0.15 estimates, is
usually fine, but quoting it as a precise forecast is not. Report it as a bound.

## Formula Sheet

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$P(A)$` | `$P : \mathcal{P}(\Omega) \to [0,1]$` | Probability of an event — a number between 0 and 1 assigned to a set of outcomes. | Always. If $P(A) > 1$ or $P(A) < 0$, the model is wrong. |
| **Axiom 1** | `$P(A) \ge 0$` for every event A | Probabilities are never negative. | Checking any table of numbers you have been handed. |
| **Axiom 2** | `$P(\Omega) = 1$` | The certain event, the whole sample space, has probability 1. | Checking that your weights sum to 1. |
| **Axiom 3** | `$P(A_1 \cup A_2 \cup \cdots) = \sum_i P(A_i)$ | **Countable additivity**, valid *only* for pairwise disjoint events. The list may be infinite. | Partitioning Ω into disjoint pieces. Axiom 3 with one piece, Ω, gives $P(\varnothing) = 0$, so that needs no axiom. |
| `$A^c$` | `$P(A^c) = 1 - P(A)$` | **Complement rule.** $A$ and $A^c$ are disjoint and cover Ω. | Any "at least one" question: count the "none" case instead. |
| `$A \subseteq B$` | `$P(A) \le P(B)$` | **Monotonicity.** A smaller set cannot be more likely. | Sanity-checking models; rules out $P(A \cap B) > P(A)$ immediately. |
| `$P(A \cup B)$` | `$= P(A) + P(B) - P(A \cap B)$` | **Addition rule**, overlap or not. | Combining two events you know individually. |
| disjoint | `$P(A \cup B) = P(A) + P(B)$` | For **disjoint / mutually exclusive** events the intersection is empty, so the subtraction vanishes. | Dice sums, distinct categories, "both aces *or* both kings". |
| `$P(A \cap B)$` | `$= P(B) \cdot P(A \mid B)$`, needs `$P(B) > 0$` | **Multiplication rule.** Joint = conditioner × conditional. Defined in detail in [Lesson 62](../part05_probability_statistics/62_conditional_probability_and_bayes.md). | Any "and" question where the second draw's rate changes. |
| independent | `$P(A \cap B) = P(A) \cdot P(B)`, equivalently `$P(A \mid B) = P(A)$` | Knowing one event tells you nothing about the other. | Coin flips, separate requests to independent backends. **Must be argued from the mechanism.** |
| `$A \cap B \cap C$` | `$P(A \cup B \cup C) = P(A)+P(B)+P(C) - P(A \cap B) - P(A \cap C) - P(B \cap C) + P(A \cap B \cap C)$` | **Inclusion–exclusion for three events**: add singles, subtract pairs, add the triple. | Deck questions, A/B tests with several mutually exclusive UI states. |
| `$\sum_{j<k<l} |A_j \cap A_k \cap A_l|$` | general form: add singles, subtract pairs, add triples, subtract quadruples, … | More than three events, or as an upper/lower bound when you only know the first few levels. |
| `$n$` events | `$P(A_1 \cup \cdots \cup A_n) \le \sum_j P(A_j)$` | **Union bound.** Always true, needs no overlap information. | "Chance anything at all goes wrong". Loose when the events overlap heavily; vacuous when $\sum_j P(A_j) \ge 1$. |
| **Bonferroni** | `$P(A \cup B \cup C) \ge P(A)+P(B)+P(C) - P(A \cap B) - P(A \cap C) - P(B \cap C)$` | Keep only singles and pairs for a **lower** bound. | When the triple term is hard to compute but you need a floor, not a ceiling. |
| `$k$ people, 365 days` | `$P(\text{all distinct}) = \prod_{j=0}^{k-1}\dfrac{365-j}{365}$, so `$P(\text{collision}) = 1 - \prod_{j=0}^{k-1}\dfrac{365-j}{365}$` | The birthday problem. Each new person must avoid the days already taken. | Sizing a hash table: with 32-bit hashes, 77,163 entries passes 50%. |
| `$n$ entries, $2^{32}$ slots` | `$P(\text{collision}) \approx 1 - e^{-n^2 / 2^{33}}$ | Same shape, enormous space: collisions appear near $n \approx 1.18 \times 2^{16}$, i.e. around $\sqrt{2 \cdot 2^{32}}$. | Choosing a key width. 32 bits breaks at ~77k entries; 64 bits is effectively never. |
| `$P(\text{at least one}) = 1 - (1-p)^n$ | needs **independence** | "Nothing failed" is easier than "something failed". | Tail-latency budgets, per-batch failure rates. Requires independent events. |

## Multiple Choice Questions

**Q1.** The three axioms are non-negativity, `P(Ω) = 1`, and countable
additivity over disjoint events. Why is `P(∅) = 0` *not* stated as a fourth axiom?

- A) Because an empty set has no elements, so the probability is vacuously 0
- B) Because it follows from axioms 2 and 3: Ω is the disjoint union of Ω and ∅, so `P(Ω) = P(Ω) + P(∅)`
- C) Because `P(∅) = 0` is only true for finite sample spaces
- D) Because countable additivity requires an infinite list of events

<details>
<summary>Answer and explanation</summary>

**B) Because it follows from axioms 2 and 3: Ω is the disjoint union of Ω and ∅,
so `P(Ω) = P(Ω) + P(∅)`.**

Subtracting `P(Ω)` from both sides gives `P(∅) = 0`. Option A is a plausible
s-sounding story but has no mathematical content — cardinality plays no role in
the axioms at all. Option C is false: the derivation uses nothing about the size
of Ω, so it holds for infinite sample spaces too. Option D misreads "countable";
a two-element list of disjoint events is a perfectly legal instance.

</details>

**Q2.** `P(A) = 0.1` and `P(B) = 0.2`. What is the tightest statement you can
make about `P(A ∪ B)`?

- A) Exactly 0.3
- B) Exactly 0.1
- C) At most 0.3, and at least 0.2
- D) At most 0.3, and at least 0.1

<details>
<summary>Answer and explanation</summary>

**C) At most 0.3, and at least 0.2.**

The union rule gives `P(A ∪ B) = 0.3 − P(A ∩ B)`, so it is at most 0.3. The
intersection satisfies `0 ≤ P(A ∩ B) ≤ min(P(A), P(B)) = 0.1` by monotonicity, so
`P(A ∪ B) ≥ 0.3 − 0.1 = 0.2`. Both extremes are attained: 0.3 when A and B are
disjoint, 0.2 when B ⊆ A. Option A assumes disjointness you were not given.
Option B describes P(A ∩ B)'s *maximum*, not the union. Option D uses the wrong
floor — the guaranteed overlap is bounded by the *smaller* probability, not the
larger.

</details>

**Q3.** Two cards are drawn from a 52-card deck without replacement. Which
statement is correct?

- A) `P(both aces) = (4/52)²`, because the two draws are from the same deck and therefore independent
- B) `P(both aces) = (4/52)(3/51) = 1/221 ≈ 0.004525`, because the second draw sees 3 aces in 51 cards
- C) `P(both aces) = (4/52)(4/52) + (4/52)`, because you add the two orders
- D) `P(both aces) = 4/52`, because once you know one card is an ace, the event is certain

<details>
<summary>Answer and explanation</summary>

**B) `P(both aces) = (4/52)(3/51) = 1/221 ≈ 0.004525`, because the second draw
sees 3 aces in 51 cards.**

This is exactly what Exercise 2 of this lesson computes. Option A applies the
product rule without its independence hypothesis — the defining error, and it
gives 1/169 ≈ 0.005917, about 31% too large. Option C is a category error: the two
orders are not disjoint *events*, they are the same outcome described twice;
adding them double counts every favourable outcome. Option D confuses the
*conditional* probability with the *joint*: `P(both aces) = P(first is ace) ×
P(second is ace | first is ace)`, and the second factor is 3/51, not 1.

</details>

**Q4.** In the worked birthday example, the union bound gives about 0.693 for
23 people while the exact answer is 0.507. Why is the exact value lower?

- A) The union bound is an approximation that converges from below
- B) A birthday shared by three people creates 3 colliding pairs but is only 1 collision, so the pair argument overcounts
- C) 365 days is an underestimate; leap years make the true answer smaller
- D) The exact answer is wrong because it uses the complement incorrectly

<details>
<summary>Answer and explanation</summary>

**B) A birthday shared by three people creates 3 colliding pairs but is only 1
collision, so the pair argument overcounts.**

The union bound `C(23,2)/365 = 253/365 ≈ 0.693` counts the union once per
colliding pair. Overlap between those pair-events can only reduce the union, so
the bound is an upper bound, exactly as Derived fact 6 says. Option A reverses
the direction — the lesson's code block prints the bound above the exact value
in every row. Option C is a red herring: leap days would make the space slightly
*larger*, lowering the collision probability further, but that is a refinement,
not the explanation for the gap. Option D is false because the complement route
is validated by the multiplication argument in Step 3 of the example.

</details>

**Q5.** A service gives each of 1,000 requests a 0.001 chance of timing out and
you assume the timeouts are independent. Which is closest to
`P(at least one timeout in a minute)`?

- A) `1000 × 0.001 = 1.0`
- B) `1 − (1 − 0.001)^1000 ≈ 0.6323`
- C) `(0.001)^1000`
- D) `0.001 × 1000 − C(1000,2)(0.001)^2 ≈ 0.5005`

<details>
<summary>Answer and explanation</summary>

**B) `1 − (1 − 0.001)^1000 ≈ 0.6323`.**

"Nothing failed" is a product of 1,000 independent survival probabilities, so
the complement gives 0.632305 — the number Exercise 3 prints. Option A is the
union bound, which here is vacuous: it cannot exceed 1, so it tells you nothing.
Option C multiplies the failure rates rather than the survival rates. Option D
stops inclusion–exclusion after the pair terms, giving ≈ 0.5005; the true value
sits above it, and this is the Bonferroni *lower* bound, not the answer.

</details>

**Q6.** Why does the lesson insist that independence "must be argued from the
mechanism, not inferred"?

- A) Because independence is hard to test, and untestable claims should not be made in engineering
- B) Because two different distributions can produce identical observed frequencies while having very different dependence structures
- C) Because the axioms already prove all pairs of events are independent
- D) Because independence only holds when the events have equal probabilities

<details>
<summary>Answer and explanation</summary>

**B) Because two different distributions can produce identical observed
frequencies while having very different dependence structures.**

The axioms do not decide dependence; the mechanism does. Two requests hitting the
same database fail together, and assuming independence would shrink the failure
bound that the union bound was applied to compute. Option A gets the engineering
intuition but the wrong reason: you *can* test for independence, you just cannot
deduce it from the fact that you saw no pattern. Option C contradicts the axioms.
Option D is false: a fair die's "first roll is 6" and "second roll is 6" are
independent and both have probability 1/6, but "first roll is 6" and "sum is 7"
are dependent and have unequal probabilities.

</details>

**Q7.** `P(A) = 0.4`, `P(B) = 0.4`, and `P(A ∩ B) = 0.9`. What does
monotonicity alone tell you?

- A) Nothing — monotonicity concerns sets, and you have no sets here
- B) The triple is impossible, because `A ∩ B ⊆ A` forces `P(A ∩ B) ≤ 0.4`
- C) The table is fine, since `0.9 ≤ 0.4 + 0.4` is false but no axiom forbids it
- D) `P(A)` and `P(B)` must both be 0.5

<details>
<summary>Answer and explanation</summary>

**B) The triple is impossible, because `A ∩ B ⊆ A` forces `P(A ∩ B) ≤ P(A) = 0.4`.**

Monotonicity alone kills it, before any other rule is applied. Option A misses
the point of monotonicity — it is precisely a statement about set inclusion.
Option C is self-refuting: `0.9 ≤ 0.8` is false, and Axiom 1 forbids negative
probabilities. Option D confuses marginals with a normalised pair of marginals;
nothing in the axioms forces symmetry.

</details>

**Q8.** In the deck example, `A ∩ B = ∅` because no card is both an ace and a
king. Why can you not then drop the rest of the inclusion–exclusion formula and
use `P(A ∪ B ∪ C) = P(A) + P(B) + P(C)`?

- A) Because inclusion–exclusion requires all intersections to be nonempty
- B) Because C overlaps A and B; only the A∩B term vanished
- C) Because the formula is only valid for exactly three events
- D) Because `A ∩ B = ∅` means A and B are dependent

<details>
<summary>Answer and explanation</summary>

**B) Because C overlaps A and B; only the A∩B term vanished.**

In the worked example `P(A∩C) = 2/52` and `P(B∩C) = 2/52` — the red aces and red
kings. Dropping those gives 34/52 ≈ 0.6538, overcounting, which is Mistake 4 in
this lesson. Option A is backwards: empty intersections are the easy case. Option
C is wrong because the general form in Derived fact 5 handles any number of
events. Option D is wrong on two counts — disjointness is a statement about the
events, not about dependence, and here A and B *are* independent.

</details>

**Q9.** Bonferroni's inequality for three events keeps the singles and pairs.
What does it give you?

- A) An upper bound on `P(A ∪ B ∪ C)`
- B) A lower bound, since every dropped term in inclusion–exclusion is nonnegative
- C) The exact value, whenever the triple intersection is empty
- D) A bound in bits rather than in probability

<details>
<summary>Answer and explanation</summary>

**B) A lower bound, since every dropped term in inclusion–exclusion is
nonnegative.**

Truncating an alternating sum after the pair terms leaves `P(A∪B∪C)` minus a sum
of nonnegative triple terms, so the truncation is a floor. Option A describes the
union bound, which keeps only the singles. Option C is the trap: it would be
exact only if all higher-order intersections were zero, and the triple term
`P(A∩B∩C)` here is exactly 0 — but the *pairs* are nonzero, so this is not the
truncation that gives the exact value. Option D is nonsense; these are
probabilities in $[0,1]$.

</details>

**Q10.** A/B test: variant A has a 5% click rate and variant B has a 6% click
rate, both measured over the same 10,000 users, and a user can click on both
variants' elements on the page. What does the lesson's arithmetic say?

- A) Add them to 11%, because the two click rates are on different users
- B) You need `P(A ∩ B)` before you can report a single "clicked either" number
- C) Multiply them, because clicks on independent page elements are independent
- D) Take the average, 5.5%, because the overlap cancels

<details>
<summary>Answer and explanation</summary>

**B) You need `P(A ∩ B)` before you can report a single "clicked either" number.**

The addition rule reduces to plain addition only when the events are disjoint,
which is exactly the "A/B test overlap" case in Why Computer Science Cares. The
overlap makes the true union strictly less than 11%. Option A is the mistake
those events invite. Option C invokes the product rule without establishing
independence, and the product would be the *intersection*, not the union. Option
D has no justification at all: overlap cancels in the *difference* of two rates,
not in their sum.

</details>

## Subjective Questions

### Short Answer

**Q1. State the three axioms, and explain in one sentence why countable
additivity is restricted to *disjoint* events.**

<details>
<summary>Answer</summary>

Axiom 1: $P(A) \ge 0$ for every event $A$. Axiom 2: $P(\Omega) = 1$. Axiom 3:
if $A_1, A_2, \ldots$ are pairwise disjoint, then $P(\bigcup_i A_i) =
\sum_i P(A_i)$.

The disjointness restriction is essential because the axiom is about *counting
each outcome once*. If an outcome lies in two of the sets, additivity would
count it twice and produce a number larger than 1 — which Axiom 1 forbids. The
whole of Derived fact 3 exists to repair exactly this.

</details>

**Q2. Two events $A$ and $B$ each have probability 0.3. Give the range of
possible values of $P(A \cup B)$ and say when each extreme is attained.**

<details>
<summary>Answer</summary>

$0.3 \le P(A \cup B) \le 0.6$. The union rule gives
$P(A \cup B) = 0.6 - P(A \cap B)$, and monotonicity bounds the intersection by
$0 \le P(A \cap B) \le 0.3$. The upper extreme $0.6$ is attained when
$P(A \cap B) = 0$ (disjoint events); the lower extreme $0.3$ is attained when
$B \subseteq A$, i.e. the intersection equals $A$ itself.

</details>

**Q3. Why is the complement rule $P(A^c) = 1 - P(A)$ a *derived fact* rather
than a fourth axiom?**

<details>
<summary>Answer</summary>

Because $\Omega = A \sqcup A^c$ is a disjoint union, so Axiom 3 gives
$P(\Omega) = P(A) + P(A^c)$, and Axiom 2 gives $P(\Omega) = 1$. Substituting and
rearranging yields $P(A^c) = 1 - P(A)$. The rule is forced, not chosen — which
is exactly why the complement route and the direct counting route can never
disagree, as both worked examples check.

</details>

**Q4. The lesson says the axioms never require outcomes to be equally likely.
Give one example of a valid model where they are not.**

<details>
<summary>Answer</summary>

A loaded die: keep all six faces in $\Omega$ and assign
$P(\{6\}) = 0.35$ with the remaining five faces sharing 0.65. The weights are
nonnegative and sum to 1, so Axioms 1 and 2 hold, and any disjoint partition of
the six faces has probabilities summing to 1, so Axiom 3 holds. Uniformity is an
assumption about the mechanism, never a theorem.

</details>

**Q5.** With 365 days, what is `P(at least two of 30 people share a birthday)`,
and which rule produced that number?

<details>
<summary>Answer</summary>

$P(\text{collision}) = 1 - \prod_{j=0}^{29}(365-j)/365 = 0.7063$, matching the
table in Example A. The rules involved are the complement rule (turning "some
collide" into "all distinct") and the multiplication rule applied 29 times, each
factor being a conditional probability: the $j$-th person must avoid the $j$
days already taken. The union bound gives the looser
$\binom{30}{2}/365 = 1.0$, which is vacuous.

</details>

**Q6. What does the union bound cost you, and when is it not worth using?**

<details>
<summary>Answer</summary>

It costs tightness. The bound equals the sum of the individual probabilities and
throws away all information about overlap, so whenever the events overlap
substantially it overstates. With 23 people the bound is 0.693 against an exact
0.507; with 30 people the bound is 1.0, which conveys nothing. The rule of thumb
is that the bound is informative only while $\sum_j P(A_j)$ stays comfortably
below 1 — which is why per-minute error budgets work and per-day ones usually
do not.

</details>

### Long Answer

**Q1. Why does the union bound stay valid when the events overlap heavily, even
though it explicitly ignores overlap? What would break if the events were not
independent?**

<details>
<summary>Model answer</summary>

Overlap is exactly what the bound is discarding, and discarding it can only move
the answer in the safe direction. Inclusion–exclusion is an alternating sum
$\sum_i P(A_i) - \sum_{i<j} P(A_i \cap A_j) + \cdots$ of nonnegative terms, so
deleting every negative term and every higher-order positive term leaves a
number at least as large as the true union. Heavy overlap means the pair terms
are *large*, which is what makes the bound loose — never what makes it invalid.

Independence is a different matter, because that is where the bound is used
quantitatively in practice. The bound $P(\text{at least one timeout}) \le 1000
\times 0.001$ is computable from per-request rates alone, and it is only
meaningful if those per-request rates are the right rates. But the *direction* of
independence matters for interpretation, not validity. If timeouts cluster — a bad
deploy takes out a correlated block of 200 requests at once — then
$P(\text{at least one})$ is *more* likely than the independent model predicts,
because one cause produced many events rather than many independent causes. The
bound still holds, but it understates the typical size of the incident, so it
answers "could a minute be bad?" rather than "how bad is a bad minute?".

What breaks if you assume independence and it is false is the *rate*: Exercise
3(d) shows that clustering changes the distribution of counts per minute
entirely, so a dashboard built on the independent baseline starts firing on
every healthy day. This is why correlation between failures is worth modelling
explicitly rather than optimising away.

</details>

**Q2. Inclusion–exclusion for $m$ overlapping sets works because of the identity
$\sum_{k=0}^{m}(-1)^k \binom{m}{k} = 0$. Explain why this makes the formula
correct, and what the cost of that proof tells you about computing it.**

<details>
<summary>Model answer</summary>

Consider one specific outcome $o$ that lies in exactly $m$ of the sets $A_1,
\dots, A_n$. In the inclusion–exclusion sum, $o$ contributes once from each of
the $m$ single terms, $\binom{m}{2}$ times from the pair terms, $\binom{m}{3}$
times from the triple terms, and so on. Its net contribution is
$\sum_{k=0}^{m}(-1)^k \binom{m}{k}$, which by the binomial theorem equals $(1-1)^m
= 0$ for $m \ge 1$. Summing over all outcomes gives $P(A_1 \cup \cdots \cup A_n)$,
so each outcome in the union is counted exactly once and each outcome outside it
zero times.

The cost is that the proof needs *all* $2^n$ intersections. Inclusion–exclusion is
correct but expensive, and it gets there by brute structural effort rather than
by a shortcut. That is why in practice you almost never evaluate it in full:
either the events are disjoint and you use the two-term addition rule, or you
fall back to the union bound, or — as in this lesson's birthday example — you
switch to the complement, which is both exact and much cheaper because the
complement is *separable*. The lesson's general formula for $n$ events is written
as an alternating sum precisely so that truncating it at any level gives you a
valid bound rather than a wrong answer.

</details>

**Q3.** Two log lines are written by different services and reference different
things. Why is "so their errors are independent" a dangerous default in systems
work?

<details>
<summary>Model answer</summary>

Independence is a claim about the mechanism, and "different log lines" says
nothing about mechanism — it says only that the events are separately *recorded*.
Two requests that hit the same database, or that both depend on a shared DNS
resolver or a shared deploy, will fail together. Assuming independence in that
setting makes the joint failure probability smaller than reality, and the union
bound applied on top of that compounds the error: the bound stays valid, so
nothing flags the mistake, but the number is optimistic in exactly the direction
you cannot afford.

The damage is structural, not a small numeric slip. Systems are built with
component-level budgets — "this service may use 5% of the cluster" — and those
budgets are only additive across components if the components fail independently.
Real components share dependencies, so failures are positively correlated, and the
whole cluster has fewer good days than the per-component error rates imply.

The fix is not to avoid the product rule but to earn it. For genuinely separate
randomised rollouts, "different user cohorts, different shards, randomised
backends" is a real argument for independence. For everything else you have to
name the shared dependency, and when you cannot rule out a common cause you
should widen the bound rather than tighten the arithmetic.

</details>

**Q4.** Why does the birthday problem pass 50% at 23 people, when a direct count
of "how full is the calendar" intuition says it should take far more?

<details>
<summary>Model answer</summary>

The intuition models the wrong objects. "How full is the calendar" counts
outcomes; the probability is driven by *pairs*, and there are many more pairs than
days. With 23 people there are $\binom{23}{2} = 253$ pairs, each colliding with
probability $1/365 \approx 0.00274$, so the pair argument gives about 0.693 — an
overestimate, because a birthday shared by three people contributes 3 colliding
pairs but only 1 collision. The exact complement calculation gives 0.5073, just
above one half. The threshold comes from $\binom{k}{2} \approx 365$, i.e.
$k \approx 27$, modified downward by the overlap correction to 23.

What makes this useful in computer science is that the shape survives the change of
interpretation. Replace days with $2^{32}$ slots and people with hash-table
entries, and the same formula says a table with 77,163 entries has a 50% chance of
containing a colliding pair — despite being less than 0.002% full. The
$\sqrt{n}$-ish growth is why Python's `dict` grows at roughly 2/3 load rather than
waiting for the space to fill, and why a birthday attack against a 32-bit key needs
only about $2^{16}$ attempts rather than $2^{32}$.

So the lesson is not that people are unusually repetitive. It is that the number
of *pairings* grows quadratically while the space grows linearly, and any system
that stores many items in a shared space inherits that ratio.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — three overlapping events from a deck.** From a 52-card deck,
one card is drawn. Let A = ace, B = face card (J, Q, K), C = black. Compute
P(A ∪ B ∪ C) two ways: inclusion–exclusion, and via the complement. Check they
agree.

<details>
<summary>Solution</summary>

Take the sizes first, being careful that a card cannot be both an ace and a
face card under this definition:

    |A| = 4            (the four aces)
    |B| = 12           (J, Q, K in each of four suits)
    |C| = 26           (spades and clubs)
    |A and B| = 0      -- an ace is not a J/Q/K, so these events are disjoint
    |A and C| = 2      (A-spades, A-clubs)
    |B and C| = 6      (J/Q/K in spades and clubs)
    |A and B and C| = 0

Inclusion-exclusion:

    P(A u B u C) = (4 + 12 + 26 - 0 - 2 - 6 + 0)/52 = 34/52 = 0.653846

Complement. The complement of "ace or face or black" is "red, and not an ace,
and not a face card":

    red cards                 = 26
    of which red aces         = 2
    of which red face cards   = 6
    so complement             = 26 - 2 - 6 = 18

P = 1 - 18/52 = 34/52 = 0.653846. The two routes agree exactly, as they must,
since the complement rule and the addition rule are both consequences of the
axioms.

The instructive step is |A and B| = 0. Because A and B are disjoint, one pair term
drops out -- but the *other* pair terms do not, and dropping them too would give
(4 + 12 + 26)/52 = 0.8077, which would claim that 80% of draws are an ace, a face
card, or black. Black aces and black face cards are counted twice in that sum,
and the two subtractions remove exactly those eight double counts.

```python
deck = [r + s for s in "SHDC" for r in "23456789TJQKA"]
n = len(deck)
A = {c for c in deck if c[0] == "A"}
B = {c for c in deck if c[0] in "JQK"}
C = {c for c in deck if c[1] in "SC"}

inc_exc = (len(A) + len(B) + len(C)
           - len(A & B) - len(A & C) - len(B & C)
           + len(A & B & C)) / n

not_all = {c for c in deck if c not in (A | B | C)}
via_complement = 1 - len(not_all) / n

print(f"|A|={len(A)} |B|={len(B)} |C|={len(C)}")
print(f"|A&B|={len(A & B)} |A&C|={len(A & C)} |B&C|={len(B & C)} "
      f"|A&B&C|={len(A & B & C)}")
print(f"inclusion-exclusion : {inc_exc:.6f}  ({n - len(not_all)}/{n})")
print(f"complement          : {via_complement:.6f}")
print(f"agree: {abs(inc_exc - via_complement) < 1e-12}")
print(f"forgetting both pair terms gives {(len(A) + len(B) + len(C)) / n:.6f}")
```

Watch out when writing this up: it is very easy to assume that "ace" and "face
card" must overlap, because in colloquial card language face cards sometimes
includes aces. Check each pairwise intersection against the *stated* definition
rather than against your memory of a different problem.

</details>

**[ ] Exercise 2 — the multiplication rule without replacement.** Two cards are
drawn from a 52-card deck without replacement. Compute P(both are aces) using
(1) the counting formula and (2) the multiplication rule with conditional
probabilities. Then do the same for "both are aces or both are kings", and notice
why you cannot multiply there.

<details>
<summary>Solution</summary>

(1) Counting: favourable hands C(4,2) = 6, total C(52,2) = 1326, so
6/1326 = 1/221 ≈ 0.004525.

(2) Multiplication rule: P(first is an ace) = 4/52. Given that, P(second is an
ace) = 3/51, because one ace has been removed from 52 cards. So

    P(both aces) = (4/52) · (3/51) = 12/2652 = 1/221 ✓

The factor 3/51 rather than 4/52 is the whole point: **without replacement the
events are dependent.** Had you used 4/52 for the second draw you would get
1/169 ≈ 0.005917, too big by about 31%.

For "both aces or both kings" the two events are disjoint, so you add, you do
not multiply:

    P = C(4,2)/C(52,2) + C(4,2)/C(52,2) = 2/221 ≈ 0.009050

The multiplication rule applies to *intersections*; disjoint unions need the
addition rule.

```python
from math import comb
from fractions import Fraction

total_hands = comb(52, 2)
print(f"|Omega| = C(52,2) = {total_hands}")

# (1) counting: choose which two of the four aces
by_counting = Fraction(comb(4, 2), total_hands)

# (2) multiplication rule: the SECOND draw sees only 3 aces among 51 cards,
# which is exactly why the draws are dependent.
by_multiplication = Fraction(4, 52) * Fraction(3, 51)

print(f"counting      : {float(by_counting):.8f}  = C(4,2)/C(52,2)")
print(f"multiplication: {float(by_multiplication):.8f}  = (4/52) * (3/51)")
print(f"equal: {by_counting == by_multiplication}")

# The tempting wrong answer assumes the draws are independent.
naive = Fraction(4, 52) ** 2
print(f"wrong (independent): {float(naive):.8f}  -- too large by "
      f"{float(naive / by_multiplication):.4f}x")

# "both aces OR both kings" is a union of two DISJOINT events: add, do not multiply.
union = 2 * by_counting
print(f"both aces or both kings (disjoint, so add): {float(union):.8f}")
```

</details>

**[ ] Exercise 3 — Challenge: the union bound on latency.** A service handles
1,000 requests per minute. Each request independently times out with probability
0.001. (a) Compute the exact probability that at least one timeout occurs in a
minute, using the complement. (b) Compute the union bound. (c) Explain the
difference. (d) Now suppose timeouts cluster: 90% of minutes have either 0 or
exactly 1 timeout. Compute the probability that a minute has 0 timeouts.

<details>
<summary>Solution</summary>

(a) Exact, via the complement: (1 − 0.001)^1000 = 0.999^1000 ≈ 0.367695, so
P(at least one) ≈ 0.632305.

(b) Union bound: 1000 × 0.001 = 1.0, and since a probability cannot exceed 1 the
bound is vacuous here — which is itself the lesson: the union bound is only
informative when ΣP is comfortably below 1. Try it for a *day* of 1,440,000
requests and it is far worse.

(c) The bound overstates by 0.367695, and the reason is that it counts each
outcome once per timeout that occurred. A minute with 5 timeouts is counted 5
times in the union bound but should count once. Inclusion–exclusion corrects
exactly this overcounting:
P(at least one) = 1000(0.001) − C(1000,2)(0.001)² + … which subtracts
499,500 × 0.000001 = 0.4995 for the pair terms alone, bringing 1.0 down to about
0.5, and further terms finish the job.

(d) If timeouts cluster, the events are *positively* dependent and the model
changes. Let t = P(exactly one timeout in a minute) and use the given 90%:
(1 − t) + t = 0.9. From the exact computation, P(0 timeouts) = 0.999^1000 ≈
0.367695 under independence, so t = 0.9 − 0.367695 = 0.532305. The remaining
0.1 of minutes contain two or more timeouts. Clustering makes "at least one"
*more* likely than independence predicts, which is exactly what real correlated
incidents do: a bad deploy does not fail one request out of a thousand, it
fails a large correlated block of them.

```python
n = 1000
p_timeout = 0.001

exact = 1 - (1 - p_timeout) ** n
union_bound = min(1.0, n * p_timeout)
print(f"(a) exact, via complement : {exact:.6f}")
print(f"(b) union bound           : {union_bound:.6f}  (vacuous: >= 1)")
print(f"(c) overcount             : {union_bound - exact:.6f}")

p_zero = (1 - p_timeout) ** n
p_exactly_one_given = 0.9 - p_zero
print(f"(d) P(0 timeouts)         : {p_zero:.6f}")
print(f"    P(exactly 1) if 90% of minutes have <=1 : {p_exactly_one_given:.6f}")
print(f"    remaining mass (2+ timeouts)        : {0.1:.6f}")
```

</details>

**[ ] Exercise 4 — verify the axioms on a loaded die.** Construct a probability
model on $\Omega = \{1,2,3,4,5,6\}$ with
$P(\{1\}) = P(\{2\}) = 0.10$, $P(\{3\}) = P(\{4\}) = P(\{5\}) = 0.15$,
$P(\{6\}) = 0.35$. (a) Check all three axioms numerically. (b) Compute
$P(\text{roll is even})$ two ways: by summing weights of the even faces, and by
the complement. (c) Compute $P(\text{roll is a multiple of 3})$ using set
addition, identifying the overlap explicitly. (d) Show that the classical ratio
$|A| / |\Omega|$ gives the wrong answer for the event $\{6\}$.

<details>
<summary>Solution</summary>

(a) **Axiom 1:** every weight is nonnegative — all six are. **Axiom 2:**
$P(\Omega) = 2(0.10) + 3(0.15) + 0.35 = 0.20 + 0.45 + 0.35 = 1$. **Axiom 3:**
any disjoint partition of the six faces has its weights summing to the same
total, so additivity holds by arithmetic. Concretely, the partition
$\{\{1,2\},\{3,4,5\},\{6\}\}$ gives $0.20 + 0.45 + 0.35 = 1$.

(b) Even faces are $\{2,4,6\}$, so
$P(\text{even}) = 0.10 + 0.15 + 0.35 = 0.60$.
The complement is $\{1,3,5\}$, giving
$P(\text{even}) = 1 - (0.10 + 0.15 + 0.15) = 1 - 0.40 = 0.60$. ✓ The two routes
agree, as the complement rule guarantees.

(c) Multiples of 3 are $\{3, 6\}$, so $P = 0.15 + 0.35 = 0.50$. The overlap is
real here and worth naming: $\{3\}$ and $\{6\}$ are disjoint, so the intersection
is empty and the plain sum is the whole answer. Compare with a genuinely
overlapping pair, e.g. "at least 3" and "at least 5" — those contain $\{3\}$
between them.

(d) The event $\{6\}$ has $|\{6\}| / |\Omega| = 1/6 \approx 0.1667$, but the model
says $0.35$. The ratio is off by a factor of 2.1 because it treats each face as
counting equally, which is the uniformity assumption the axioms never make. The
right tool is the weight, not the cardinality.

```python
from fractions import Fraction as F

w = [F(10, 100), F(10, 100), F(15, 100), F(15, 100), F(15, 100), F(35, 100)]

print(f"Axiom 1 (non-negativity): {all(x >= 0 for x in w)}")
print(f"Axiom 2 (normalisation): sum = {sum(w)} -> {sum(w) == 1}")

# Axiom 3 on a disjoint partition: {1,2}, {3,4,5}, {6}
parts = [w[0] + w[1], w[2] + w[3] + w[4], w[5]]
print(f"Axiom 3 (disjoint sum) : {[str(p) for p in parts]} -> {sum(parts, F(0))}")

p_even_direct = w[1] + w[3] + w[5]
p_odd = w[0] + w[2] + w[4]
print()
print(f"P(even) direct      = {float(p_even_direct):.6f}")
print(f"P(even) via 1 - odd = {float(1 - p_odd):.6f}")
print(f"agree: {p_even_direct == 1 - p_odd}")

A = {3}
B = {6}
print()
print(f"P({{3}}) = {float(w[2])}, P({{6}}) = {float(w[5])}, "
      f"P(intersection) = 0 (disjoint)")
print(f"P({{3,6}}) = {float(w[2] + w[5]):.6f}")
print(f"classical |A|/|Omega| for {{6}} = 1/6 = {1/6:.6f} "
      f"vs the correct weight {float(w[5]):.6f}")
```

</details>

**[ ] Exercise 5 — inclusion–exclusion on four A/B variants.** A page shows four
mutually exclusive UI states, and a user is counted as "engaged" if they
interact with at least one of them. Suppose each state is engaged by 20% of
users, but every pair of states is engaged by the same 6% of users (a user who
engages with two states is counted in both marginals). (a) Compute
$P(\text{engage with at least one state})$ by inclusion–exclusion on the given
information. (b) Show that the naive sum of marginals overcounts, and by how
much. (c) Explain what additional assumption would make the inclusion–exclusion
answer computable in general.

<details>
<summary>Solution</summary>

(a) Four events $A_1, \dots, A_4$ with $P(A_i) = 0.20$ and
$P(A_i \cap A_j) = 0.06$ for every pair. Six pairs, so

$$P\Big(\bigcup_{i=1}^{4} A_i\Big) = 4(0.20) - 6(0.06) + \text{higher-order terms} = 0.80 - 0.36 + \cdots = 0.44 + \cdots$$

The triple and quadruple terms are nonnegative, so this is a **lower bound** of
$0.44$, not the exact value.

(b) The naive sum is $4(0.20) = 0.80$, which exceeds $0.44$ by at least $0.36$.
Those 36 percentage points are double counts: each of the 6% who engaged with two
states was added twice and must be subtracted once, and each of the
three-way engagers was added three times, needing the triple term as well.

(c) The general formula needs the triple intersections
$P(A_i \cap A_j \cap A_k)$ and the quadruple intersection. Those are not
determinable from marginals and pairwise values alone — three numbers, in
general. If instead every state were engaged by 20% of users and any two states
were engaged independently of one another, then $P(A_i \cap A_j) = 0.04$ and the
naive addition would be the right thing to do. The reason the answer here differs
is exactly Mistake 2: overlapping UI states are not independent events.

Note also that the union bound gives $P \le 0.80$, so between the Bonferroni lower
bound $0.44$ and the union bound $0.80$ you have bracketed the answer without
computing any triple terms at all.

```python
from itertools import combinations

n = 4
marginal = 0.20
pairwise = 0.06

naive = n * marginal
pair_sum = len(list(combinations(range(n), 2))) * pairwise

print(f"naive sum of marginals : {naive:.6f}")
print(f"number of pairs        : {len(list(combinations(range(n), 2)))}")
print(f"pair subtractions      : {pair_sum:.6f}")
print(f"Bonferroni lower bound : {naive - pair_sum:.6f}")
print(f"union upper bound      : {naive:.6f}")
print(f"overcount by at least  : {pair_sum:.6f}")
```

</details>

**[ ] Exercise 6 — Challenge: sizing a hash table from the axioms alone.** (a)
A table has 8-bit keys, so the space has $2^8 = 256$ slots, and it stores $n$
random 8-bit keys. Compute $P(\text{at least one collision})$ for
$n = 12, 15, 16, 20$ using the complement. (b) At what value of $n$ does the
probability first exceed 0.5 for 8-bit keys, and how does it scale with the key
width? (c) A production table uses 32-bit keys and stores 77,163 entries. Using
the approximation $P(\text{collision}) \approx 1 - e^{-n^2/2^{33}}$, verify that
the collision probability is about 0.5, and explain why the lesson says Python's
`dict` grows at roughly 2/3 load rather than waiting for the table to fill.

<details>
<summary>Solution</summary>

(a) $P(\text{all distinct}) = \prod_{j=0}^{n-1}\frac{256-j}{256}$, so
$P(\text{collision}) = 1 - \prod_{j=0}^{n-1}\frac{256-j}{256}$.

| $n$ | $P(\text{collision})$ |
| --- | --- |
| 12 | 0.2303 |
| 15 | 0.3417 |
| 16 | 0.3803 |
| 20 | 0.5332 |

The jump from 12 to 20 entries, in a table holding 256 slots, is the whole point:
at 20 entries the table is 7.8% full and yet already has a majority chance of a
collision.

(b) Solve $1 - \prod \approx 0.5$, i.e. $\prod \approx 0.5$. Using the
approximation $\prod_{j<n}(1 - j/m) \approx e^{-n^2/(2m)}$, the threshold
satisfies $n^2 \approx 2m\ln 2$, so

$$n \approx \sqrt{2 \cdot 2^8 \cdot \ln 2} \approx \sqrt{355} \approx 18.8,$$

and the exact search finds the first $n$ above 0.5 is **20**. The scaling is
$n \approx 1.18\sqrt{m}$: doubling the table size only multiplies the threshold by
$\sqrt{2} \approx 1.41$, while doubling the number of entries multiplies it by 2.

(c) With $n = 77{,}163$ and $m = 2^{32}$:
$\frac{n^2}{2^{33}} \approx \frac{5.954 \times 10^9}{8.590 \times 10^9} \approx 0.6932$, so
$P \approx 1 - e^{-0.6932} \approx 1 - 0.5000 \approx 0.5000$. ✓ This matches the
0.5000 printed in the lesson's code block.

The reason `dict` grows early is that the relevant quantity is not what fraction
of slots are *occupied* — that is tiny — but how many *pairs* exist, which grows as
$n^2$ while the space grows as $2^{32}$. Resizing when the load factor passes about
2/3 keeps $n$ comfortably below the $\sqrt{2m}$ threshold, and the cost of resizing
is paid before collisions become likely rather than after. The same calculation
explains the birthday attack: breaking a 32-bit key takes about $2^{16}$ attempts
because of the square-root scaling.

```python
from math import prod

def p_collision(n, bits=8):
    space = 2 ** bits
    return 1 - prod((space - j) / space for j in range(n))

print(f"{'entries':>8} | P(collision) in a 2^8 space")
for n in (12, 15, 16, 20):
    print(f"{n:8d} | {p_collision(n):.6f}")

# (b) search for the first n whose collision probability exceeds 0.5
first = next(n for n in range(1, 257) if p_collision(n) > 0.5)
print(f"\nfirst n above 0.5 with 8-bit keys: {first}")
print(f"approximation n ~ sqrt(2 * 256 * ln 2) = {(2 * 256 * 0.693147)**0.5:.2f}")
# The threshold is about 1.18 * sqrt(space), NOT a fixed fraction of the space.
for bits in (8, 16, 24, 32):
    print(f"  2^{bits:2d} slots -> threshold about {1.1774 * (2 ** bits) ** 0.5:10.0f} entries")

# (c) verify the 32-bit number quoted in the lesson
n32 = 77_163
exponent = n32 ** 2 / 2 ** 33
approx = 1 - pow(2.718281828459045, -exponent)
exact = 1 - prod((2 ** 32 - j) / 2 ** 32 for j in range(n32))
print(f"\nn^2 / 2^33 = {exponent:.6f}  (close to ln 2 = {0.693147:.6f})")
print(f"exponential approximation = {approx:.4f}")
print(f"exact product              = {exact:.4f}")
```

</details>

## Summary

- Kolmogorov gives exactly three axioms: non-negativity, P(Ω) = 1, and countable
  additivity over disjoint events. Everything else is derived.
- P(Aᶜ) = 1 − P(A) is the workhorse rule; most "at least one" questions are
  easier via their complement.
- The addition rule P(A∪B) = P(A) + P(B) − P(A∩B) reduces to plain addition only
  for disjoint events.
- The product rule P(A∩B) = P(B)·P(A|B) becomes P(A)P(B) only under
  independence, which must be argued from the mechanism.
- Inclusion–exclusion alternates signs by level: singles, pairs, triples, and so
  on. For three events, singles − pairs + triples.
- The union bound P(⋃Aᵢ) ≤ ΣP(Aᵢ) is always valid and needs no information about
  overlap, but it is an upper bound and is often vacuous.
- Axioms never say outcomes are equally likely; uniformity is an assumption, and
  the most common one to leave unstated.

## Next

[62 — Conditional Probability and Bayes' Theorem](../part05_probability_statistics/62_conditional_probability_and_bayes.md)
uses the product rule to define conditioning, builds the chain rule and the law
of total probability from it, and derives Bayes' theorem — then explains the
base-rate fallacy, which is the most consequential misreading of probability in
engineering.