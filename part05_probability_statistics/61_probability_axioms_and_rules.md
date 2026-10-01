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
  ([Lesson 62](62_conditional_probability_and_bayes.md)).
- **Monte Carlo error bars.** Union bound gives the "at most this many standard
  errors" reasoning behind simulation confidence intervals
  ([Lesson 68](68_law_of_large_numbers_and_clt.md)).
- **A/B test overlap.** If variants A and B are not disjoint — for instance two
  mutually exclusive UI states on the same page — naive addition of their
  click-through rates double counts, and the discrepancy grows with the number
  of variants.

## The Formal Version

All statements below assume an experiment with sample space Ω and a function P
defined on subsets of Ω. From [Lesson 60](60_probability_foundations.md), we
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
[Lesson 60](60_probability_foundations.md) predicts: more overlap ⇒ smaller
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

[62 — Conditional Probability and Bayes' Theorem](62_conditional_probability_and_bayes.md)
uses the product rule to define conditioning, builds the chain rule and the law
of total probability from it, and derives Bayes' theorem — then explains the
base-rate fallacy, which is the most consequential misreading of probability in
engineering.