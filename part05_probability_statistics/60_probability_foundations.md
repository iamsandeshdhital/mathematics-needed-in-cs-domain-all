# 60 — Probability Foundations

**Part**: part05_probability_statistics · **Prerequisites**: 24 · **Time**: 30 min

---

## In Plain Words

Every program you write deals with things that are not certain. A network
request either comes back or it does not. A user clicks the button or scrolls
past it. A dice roll shows six or it shows four. Probability is the discipline
that turns "that might happen" into a number between 0 and 1, so that a program
can reason about it instead of guessing.

The key move is surprisingly simple. Before you can say how likely something
is, you have to write down *every* thing that could happen — the sample space.
Then you count how many of those things are "good" and divide by the total. That
is the whole classical recipe, and it is exactly the counting you learned in
[Part 02](../part02_discrete_combinatorics/20_counting_principles.md).

There are two other ways to attach a number to an event. You can run the
experiment a million times and count what happened — the relative frequency
view. Or you can state how strongly you believe it, as a gambler would — the
subjective view. The modern definition does not pick one of these. It says: a
probability is *any* function on events that satisfies three simple rules, and
those three rules are precisely designed so that all three views agree wherever
they overlap.

This lesson builds the vocabulary — sample space, event, probability model — and
shows why counting is the engine behind all of it. The formal rules arrive in
[61 — Probability Axioms and Rules](../part05_probability_statistics/61_probability_axioms_and_rules.md).

## Why Computer Science Cares

- **Monte Carlo and randomised algorithms.** Quicksort's pivot choice, K-means
  initialisation, and simulated annealing are all sampling from a probability
  model. `random.choice` in the standard library is the smallest possible
  program in this lesson.
- **Reliability engineering.** SLOs like "99.9% of requests succeed" are
  probability statements. Calculating whether a retry budget is enough is
  arithmetic on events, which is Lesson 61.
- **Hashing and load factors.** "How likely is a collision in a table of size
  m with n keys?" is the birthday problem, a counting question (Lesson 61).
- **A/B tests and experimentation.** Choosing between two designs means
  quantifying uncertainty, which is all of [Part 05](README.md).
- **Interviews.** "Two dice are rolled. What is the probability their sum is 8?"
  is a standard screen, and it separates people who can count from people who
  can only memorise.

## The Formal Version

**Definition.** A *random experiment* (also called a probability model or
*experiment*) is a procedure that produces an outcome, and it can in principle
be repeated under identical conditions. Rolling a die, flipping a coin,
drawing a card, and measuring the response time of your server are all random
experiments.

**Definition.** The *sample space* is the set of **all** possible outcomes of
the experiment. Write it as Ω (capital omega). For two six-sided dice it is the
36 ordered pairs (1,1), (1,2), …, (6,6).

Two properties matter, and both are decided *before* any probability is
assigned:

1. Ω is a set, so every outcome is distinct and order within the set carries no
   information. Whether you list the pairs as {(1,2), (2,1)} or as {12, 21}, the
   sample space is the same.
2. Every event must be expressible in terms of Ω. That is why the sample space
   must be chosen to be *complete*: an experiment whose sample space omits a
   possible outcome cannot be assigned probabilities consistently.

**Definition.** An *event* is any subset of the sample space, written A ⊆ Ω. The
certain event is Ω itself; the impossible event is the empty set ∅. An
experiment can have an enormous number of events — with n outcomes there are
2ⁿ of them, the power set 𝒫(Ω) from
[Lesson 15](../part01_logic_proof/15_sets_and_cardinality.md). Probability is a
function defined on subsets, not on individual outcomes.

**Definition.** A *probability* (or probability measure) on (Ω, 𝒫(Ω)) is a
function P from subsets of Ω to real numbers satisfying the three rules in
[Lesson 61](../part05_probability_statistics/61_probability_axioms_and_rules.md). Written P(A), it is read "the
probability of A". Its output is always in [0, 1].

### Three ways to give a number to an event

#### 1. Classical — counting

Assume every outcome in Ω is **equally likely**. Then

    P(A) = |A| / |Ω| = number of outcomes in A divided by the total

This is pure counting, and it is why [Part 02](../part02_discrete_combinatorics/)
sits directly upstream of this part. To compute a probability of this kind you
need exactly the machinery built there:

| What you need | Where it lives |
| --- | --- |
| Product rule (a × b) | [Lesson 20](../part02_discrete_combinatorics/20_counting_principles.md) |
| Permutations and combinations | [Lesson 21](../part02_discrete_combinatorics/21_permutations_and_combinations.md) |
| Choosing with limits | [Lesson 21](../part02_discrete_combinatorics/21_permutations_and_combinations.md) |
| Inclusion–exclusion | [Lesson 23](../part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md) |
| The pigeonhole principle | [Lesson 23](../part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md) |

The counting must be *done carefully*. "Rolling a 1 or a 6 has probability
2/6" is right; "two six-sided dice have 12 faces so 2/12" is right too, by
accident. Both give 1/6 here, but only one of them stays correct when you start
asking about the same object appearing twice — that lesson's job.

#### 2. Relative frequency — the long run

Forget the counting. Perform the experiment n times and let

    f_n(A) = (number of times A occurred in n runs) / n

This ratio converges as n grows: with more and more runs, f_n(A) settles on a
limit that depends only on the experiment's *mechanism*, not on your sample
size. This is the empirical, engineering view, and it is what you are trusting
when you say "this endpoint fails about 0.1% of the time".

Three consequences of taking frequency seriously:

- **It cannot give a probability to an experiment you cannot repeat.** A coin
  that is still in the shop has a frequency of zero; the classical view and the
  axiomatic view have no trouble with it.
- **It is a real measurement, so it can be wrong.** A biased die gives a stable
  wrong frequency — stable is what makes it dangerous.
- **It is the bridge to statistics.** [Lesson 68](../part05_probability_statistics/68_law_of_large_numbers_and_clt.md)
  turns this convergence into a theorem, which is what lets you quote an error
  bar.

#### 3. Subjective — degrees of belief

Write down a number representing how strongly you believe each event, with the
rules that beliefs must obey: a belief is never negative, never above 1,
believing everything gives 1, and mutually exclusive events cannot both be
highly likely. This is the Bayesian reading and it is the only one of the three
that assigns probability to non-repeatable claims ("I think this codebase has a
race condition", "the third seed in my test is the flaky one").

#### 4. Axiomatic — what the field actually adopted

Kolmogorov's 1933 definition is deliberately dull: take Ω, take the family of
events, and require three axioms. Everything else — every rule you use, every
distribution, every theorem in this part — is *derived* from those three lines.

The reason this is the right definition is not elegance. It is that it is
**consistent**: classical counting, long-run frequency, and honest degrees of
belief are all *examples* of it, so a theorem proved from the axioms applies to
all three at once. A definition that picked one view would make the other two
views unrigorous.

Note what the axioms do *not* say. They never say outcomes are equally likely.
"Choose a card uniformly" is not a theorem, it is an assumption about the
mechanism, and it is the assumption most often left unstated and wrong.

### Why counting is the engine

The classical approach looks like a special case, but in computer science it is
the load-bearing one, for a structural reason rather than a historical one.

A classical probability is a *ratio of cardinalities*. So computing one requires
exactly two things:

1. an exact count of the sample space, and
2. an exact count of the favourable subset.

That means the design problems you hit in code — how do I count without
enumerating 3ⁿ subsets? does order matter? are objects distinguishable? do I
double count? — are *identical* to the design problems of
[Lesson 28](../part02_discrete_combinatorics/28_counting_strategies.md). Probability
adds nothing new here; it just divides the answer by |Ω|.

Where counting stops working is when the sample space is infinite. Then
|A|/|Ω| is not defined, and you must switch to the axiomatic definition and use
the limit machinery of [Lesson 65](../part05_probability_statistics/65_continuous_random_variables.md). When you
see "probability" in a machine learning paper, check which world you are in: if
they write a finite sum, they are counting; if they write an integral, they are
in the continuous world.

## Worked Example

### Example A — two dice, counted completely

Roll two fair six-sided dice. Find the probability that the sum is 7.

Step 1: **Choose the sample space.** The outcomes are ordered pairs, because
die 1 showing 2 and die 2 showing 5 is physically distinguishable from die 1
showing 5 and die 2 showing 2. So Ω has 6 × 6 = 36 elements, by the product
rule.

Step 2: **Count the favourable outcomes.** Write them out:

    (1,6) (2,5) (3,4) (4,3) (5,2) (6,1)      → 6 outcomes

Step 3: **Divide.** P = 6/36 = 1/6 ≈ 0.1667.

Now the event "the sum is 7 **or** the sum is 11":

    sum 11: (5,6) (6,5)                                     → 2 outcomes

These two events are **disjoint** — no outcome has a sum that is both 7 and 11
— so you may simply add the counts: (6 + 2)/36 = 8/36 = 2/9 ≈ 0.2222.

Compare with "the sum is 7 **or** the die 1 shows a 6":

    sum 7  : 6 outcomes
    die1=6 : (6,1) (6,2) (6,3) (6,4) (6,5) (6,6)         → 6 outcomes
    both   : (6,1)                                          → 1 outcome

Naively 12/36 = 1/3, but (6,1) was counted twice, so the true answer is
(6 + 6 − 1)/36 = 11/36 ≈ 0.3056. The subtraction is not a trick; it is the
consequence of counting a set union, and [Lesson 61](../part05_probability_statistics/61_probability_axioms_and_rules.md)
states it as a rule.

### Example B — "at least one ace", where the complement does the work

Two cards are drawn without replacement from a standard 52-card deck (4 aces,
48 non-aces). Find P(at least one ace).

Counting "at least one" directly means partitioning into the cases 1 ace and 2
aces, which is fine but slower than necessary. The complement of "at least one
ace" is the single tidy event "no aces at all". So:

Step 1: sample space. Order is irrelevant for the answer, so use unordered
hands: |Ω| = C(52,2) = 52·51/2 = 1326.

Step 2: the complement. Hands with no ace: C(48,2) = 48·47/2 = 1128.

Step 3: subtract. P(no ace) = 1128/1326 ≈ 0.8507, so

    P(at least one ace) = 1 − 1128/1326 = 198/1326 ≈ 0.1493

Cross-check by the direct partition:

    exactly one ace:  4 · 48 = 192 hands
    exactly two aces: C(4,2) = 6 hands
    total:            192 + 6 = 198 hands ✓

The two routes agree, which is a theorem rather than luck — the addition rule
and the complement rule are both consequences of the axioms, so they cannot
disagree.

### Example C — what frequency actually measures

Suppose a service answers 10,000 requests per minute and 0.2% of them fail.
Over a minute the fraction that failed is 20/10000 = 0.002. Over an hour it is
about 0.002 as well — provided the failure rate really is that stable.

What does 0.002 *mean*, though? Not "20 requests will fail". It means: if the
failures were thrown into a bag, and you drew one request at random, 2 in 1000
draws would be a failure. The 20 is a long-run average over the whole minute, not
a promise about any particular minute. This distinction is why a per-minute
dashboard of an error *percentage* is often less useful than a count, and why
monitoring needs the variance machinery of
[Lesson 64](../part05_probability_statistics/64_expectation_variance.md) before you trust an average.

## Runnable Code

### Counting a sample space exactly

```python
from itertools import product
from collections import Counter
from math import comb

# The sample space for two fair six-sided dice: 36 ORDERED pairs,
# because die 1 and die 2 are distinguishable objects.
outcomes = list(product(range(1, 7), repeat=2))
print(f"sample space size |Omega| = {len(outcomes)}")

# Classical probability is a ratio of cardinalities: |A| / |Omega|.
one_over_36 = 1 / len(outcomes)

counts = Counter(a + b for a, b in outcomes)
print("sum | count | probability")
for total in range(2, 13):
    print(f"{total:3d} | {counts[total]:5d} | {counts[total] * one_over_36:.6f}")

print()
print(f"P(sum == 7)  = {counts[7]}/{len(outcomes)} = {counts[7] * one_over_36:.6f}")
print(f"P(sum == 11) = {counts[11]}/{len(outcomes)} = {counts[11] * one_over_36:.6f}")
print(f"P(sum == 7 or 11), disjoint so add = {(counts[7] + counts[11]) * one_over_36:.6f}")

# The overlap case: naive addition double counts (6,1).
union_naive = (counts[7] + 6) * one_over_36
union_fixed = (counts[7] + 6 - 1) * one_over_36
print(f"P(sum == 7 or die1 == 6): naive {union_naive:.6f} vs correct {union_fixed:.6f}")
```

### A deck, and why the complement is faster

```python
from itertools import combinations
from math import comb

deck = [rank + suit for suit in "SHDC" for rank in "23456789TJQKA"]

# Order does not affect the event, so the sample space is unordered hands.
# |Omega| = C(52, 2) -- exactly the formula from Lesson 21.
hands = list(combinations(deck, 2))
print(f"two-card hands |Omega| = {len(hands)} (C(52,2) = {comb(52, 2)})")

aces = {c for c in deck if c[0] == "A"}
no_aces = [h for h in hands if not (set(h) & aces)]
one_ace = [h for h in hands if len(set(h) & aces) == 1]
two_aces = [h for h in hands if len(set(h) & aces) == 2]

total = len(hands)
print(f"hands with no ace      = {len(no_aces)}  (C(48,2) = {comb(48, 2)})")
print(f"hands with exactly one = {len(one_ace)}  (4*48 = {4 * 48})")
print(f"hands with two aces    = {len(two_aces)}  (C(4,2) = {comb(4, 2)})")
print()
print(f"P(no ace)       = {len(no_aces)}/{total} = {len(no_aces) / total:.6f}")
print(f"P(at least one) = 1 - that       = {1 - len(no_aces) / total:.6f}")
print(f"P(at least one) by partition    = {(len(one_ace) + len(two_aces)) / total:.6f}")
print()
print("total hands accounted for:", len(no_aces) + len(one_ace) + len(two_aces), "of", total)
```

### Frequency converging on the classical answer

```python
import random
from collections import Counter

# The relative-frequency view: run the experiment a lot and count.
# A fixed seed makes this reproducible -- required whenever a lesson quotes
# a specific number, and good practice always.
random.seed(20240517)

N = 200_000
total_trials = 300_000

counts = {100: 0, 1_000: 0, 10_000: 0, N: 0}
hits = 0
for i in range(1, N + 1):
    if random.randint(1, 6) + random.randint(1, 6) == 7:
        hits += 1
    if i in counts:
        counts[i] = hits

print("trials | hits | frequency | exact 1/6 | absolute error")
for n in sorted(counts):
    freq = counts[n] / n
    err = abs(freq - 1 / 6)
    print(f"{n:6d} | {counts[n]:4d} | {freq:.6f} | {1/6:.6f} | {err:.6f}")

# Sanity check: the six possible sums really are equally likely, which is what
# makes the classical ratio legitimate in the first place.
freq_by_sum = Counter()
for _ in range(total_trials):
    freq_by_sum[random.randint(1, 6) + random.randint(1, 6)] += 1
print()
print("sum frequencies over", f"{total_trials:,}", "trials (each should be ~0.1667)")
for s in sorted(freq_by_sum):
    print(f"  sum {s:2d}: {freq_by_sum[s] / total_trials:.4f}")
```

## Common Mistakes

**Mistake 1 — treating outcomes as unordered when order is real.**
Wrong: "Two dice have 6 + 6 = 12 outcomes, so the chance of sum 7 is 6/12."
Right: there are 36 ordered outcomes, and the answer is 6/36 = 1/6. Both give the
same number here, which is exactly why the bug survives: it breaks the moment
you ask something like "P(die 1 shows 6)", where the counting basis must be
ordered pairs. The temptation is that writing down all 36 pairs feels like
tedium, and `6*6` feels like the same information.

**Mistake 2 — omitting outcomes from the sample space to make the arithmetic
nicer.** If the die is loaded, you may not list it as 36 equally likely
outcomes. Wrong: "P(6) = 1/6, so the loaded die is a fair die." Right: keep the
36 outcomes in Ω and assign the *weights* P({6}) = 0.27 and so on. A sample
space is about what can happen, not about what is convenient.

**Mistake 3 — treating probability as a statement about one specific outcome.**
Wrong: "There is a 1/6 chance that *this* die roll is a six, so it definitely is
not, since it already rolled." Right: probability describes the long-run rate of
a mechanism. Each individual roll either is a six or is not; the 1/6 describes
how often that happens across repeats. This error produces weird "quota"
reasoning in monitoring dashboards.

**Mistake 4 — assuming any numbers you write down are probabilities.**
Numbers in [0,1] are not automatically a probability model. P(A) = 0.4,
P(B) = 0.4, P(A and B) = 0.9 looks harmless and is impossible, since A and B
cannot both happen 90% of the time. The axioms exist precisely to rule this out
(Lesson 61). The temptation is that a table of plausible-looking numbers passes
every type check your code can write.

**Mistake 5 — forgetting to distinguish "0.2% of requests fail" from "20 requests
will fail".** The first is an average over a long run; the second is a
prediction about a specific interval, which needs variance and quantiles
([Lesson 64](../part05_probability_statistics/64_expectation_variance.md), [Lesson 65](../part05_probability_statistics/65_continuous_random_variables.md)).
The temptation is that dashboards constantly show the average, and averages read
like promises.

## Formula Sheet

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$\Omega$` | `$\Omega = \{o_1, o_2, \dots, o_n\}$` | The **sample space**: every outcome the experiment can produce, and nothing else. | First line of any model. If Ω is wrong, every probability you compute afterwards is wrong. |
| `$A \subseteq \Omega$` | `$A \in \mathcal{P}(\Omega)$` | An **event** is a subset of the sample space — a set of outcomes, not a single outcome. | Whenever someone says "something might happen": a roll is a 6, a request fails, a key collides. |
| `$\Omega$`, `$\varnothing$` | `$P(\Omega) = 1$`, `$P(\varnothing) = 0$` | The certain event and the impossible event. | Sanity check: any model giving $P(\Omega) = 0.9$ has a bug. |
| `$|\Omega|$` | number of elements of Ω | How many outcomes are possible. | The denominator of every classical probability. |
| `$|A|$` | number of elements of A | How many outcomes are favourable. | The numerator of every classical probability. |
| `$\mathcal{P}(\Omega)$`, `$2^n$` | `$|\mathcal{P}(\Omega)| = 2^n$` | Every subset of $n$ outcomes is an event, so there are $2^n$ events. | Deciding whether you can enumerate events at all: 16 outcomes gives 65,536 events. |
| `$P(A)$` | `$P : \mathcal{P}(\Omega) \to [0,1]$` | Probability is a *function on events*, never on outcomes. Its output is always between 0 and 1. | Whenever you write "the chance of". Check $0 \le P(A) \le 1$ before trusting it. |
| `$P(A) = \dfrac{\lvert A\rvert}{\lvert\Omega\rvert}$` | favourable ÷ total | **Classical probability.** Only legal when every outcome in Ω is equally likely. | Dice, coins, shuffled decks, `random.choice` over a list. Never for a loaded die, a skewed user, or an infinite Ω. |
| Uniformity assumption | `$\lvert\{o\}\rvert = 1$ for all $o \in \Omega$` | "Each outcome is equally likely." Not a theorem — an assumption about the mechanism. | State it explicitly whenever you divide by $|\Omega|$. |
| `$P(\{6\}) = 0.27$` | `$\sum_{o \in \Omega} P(\{o\}) = 1$` | A **loaded die**: keep all six faces in Ω and attach weights that sum to 1. | When outcomes are not equally likely. Counting cannot help; the weights are data. |
| `$f_n(A) = \dfrac{k_n}{n}$` | $k_n$ = number of runs in which A happened | **Relative frequency**: the observed fraction over $n$ runs. | Monitoring dashboards, load tests, "this endpoint fails 0.1% of the time". |
| `$f_n(A) \to P(A)$` | $\lim_{n \to \infty} f_n(A) = P(A)$ | Run it more and the observed fraction settles on the true probability of a stable mechanism. | Justifying simulation as an estimate. Made precise by [Lesson 68](../part05_probability_statistics/68_law_of_large_numbers_and_clt.md). |
| `$P(A \cup B)$` | `$= P(A) + P(B) - P(A \cap B)$` | **Addition rule with overlap.** You may only skip the last term when $A \cap B = \varnothing$. | Whenever two events can happen together. Also states inclusion–exclusion ([Lesson 23](../part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md)). |
| disjoint events | `$P(A \cup B) = P(A) + P(B)$ | P(\Omega) = 1$` for disjoint events | Adding "sum is 7" and "sum is 11" — no outcome is in both. | The dice example: `(6 + 2)/36 = 8/36`. |
| `$P(A^c)$` | `$P(A^c) = 1 - P(A)$` | **Complement rule**: flip the outcome and subtract from 1. | Any "at least one" question. Count the single easy "none" case instead. |
| `$P((a,b))$` | `$= P(a)\cdot P(b)$ | P(\Omega) = 1$` for independent rolls | Weight a loaded-die pair by multiplying the face weights. | Two dice: there are 36 *ordered pairs*, not 12 faces. |
| `$n^k$` | product rule over $k$ distinguishable objects | Count of outcomes when each of $k$ objects has $n$ choices. | $|\Omega| = 6^2 = 36$ for two dice, $6^3 = 216$ for three. |
| `$\binom{n}{k} = \dfrac{n!}{k!\,(n-k)!}$` | choose $k$ unordered items from $n$ | Use **combinations** only when order carries no information. | Hands from a deck: $\|\Omega\| = \binom{52}{2} = 1326$. Order matters for flips, not for hands. |
| `$\lvert A\rvert + \lvert A^c\rvert = \lvert\Omega\rvert$` | `$\dfrac{20}{10{,}000} = 0.002 = 0.2\%$` | A long-run *rate*, not a count for one interval. | "0.2% of requests fail" = 2 in 1000 on average, not "20 failed this minute". |

## Multiple Choice Questions

**Q1.** Why must the sample space for two dice be the 36 ordered pairs
`(a, b)` rather than the 11 possible sums 2 through 12?

- A) Because a set cannot contain more than 10 elements
- B) Because `(1,6)` and `(6,1)` are physically different outcomes, so an event like "die 1 shows a 6" cannot even be *stated* in terms of sums
- C) Because sums are not real numbers and Ω may only contain reals
- D) Because 36 is the only count that makes `P(sum = 7)` come out to 1/6

<details>
<summary>Answer and explanation</summary>

**B) Because `(1,6)` and `(6,1)` are physically different outcomes, so an event like "die 1 shows a 6" cannot even be *stated* in terms of sums.**

A sample space must be rich enough to express every event you care about. Sums
throw away which die produced which face, so "the first die shows a 6" is not a
subset of the sums. Option A is factually wrong — the sum space has 11 elements,
which already exceeds 10, and sets are never size-limited. Option C is
nonsense: sums are integers, hence reals. Option D is false: the sloppy
"12 faces" basis also gives 1/6 here, which is exactly why the error survives —
it produces the right number by accident and breaks on the next question.

</details>

**Q2.** A service is configured so that 0.2% of requests fail, and in one minute
it handles 10,000 requests. What does that configuration statement justify you
to assert?

- A) Exactly 20 requests failed during that particular minute
- B) At most 20 requests failed during that particular minute
- C) Over the long run about 2 in every 1000 requests fail; any single minute may deviate
- D) In the next minute, 20 requests will fail

<details>
<summary>Answer and explanation</summary>

**C) Over the long run about 2 in every 1000 requests fail; any single minute may deviate.**

0.002 is a long-run average. Option A treats the average as a promise about one
interval. Option B is not even a consequence: the *expected* count is 20, so
minutes with 23 or 31 failures are entirely ordinary, and there is no upper
bound at 20. Option D makes the same average-into-prediction error as A, just
about a different minute. Turning any of these into a decision needs the
variance and quantile machinery of
[Lesson 64](../part05_probability_statistics/64_expectation_variance.md), which this lesson deliberately
withholds. Note that a *separate* true statement is that any single request,
viewed across many requests, has a 0.2% failure rate — that is a claim about the
mechanism, not about one request's fate.

</details>

**Q3.** The axioms never state that the outcomes in Ω are equally likely. What
follows?

- A) The ratio $|A| / |\Omega|$ can never be used
- B) Equal likelihood is an assumption about the mechanism, so it must be stated and justified separately
- C) Every probability model must have an infinite sample space
- D) Loaded dice cannot be modelled at all

<details>
<summary>Answer and explanation</summary>

**B) Equal likelihood is an assumption about the mechanism, so it must be stated and justified separately.**

This is the point of the axiomatic definition. Option A is too strong: whenever
uniformity genuinely holds — a fair die, a shuffled deck, `random.choice` over a
list — the ratio is valid and is the cheapest route. Option C is backwards;
finite spaces are the easy case, and Lesson 65 exists precisely because infinite
spaces need different machinery. Option D is wrong because a loaded die is the
*easiest* model to write down: keep all six faces and attach weights summing to
1, as with `P(6) = 0.27`.

</details>

**Q4.** In the 36-outcome dice sample space, event $A$ contains 6 outcomes, event
$B$ contains 6 outcomes, and exactly 1 outcome lies in both. What is
$P(A \cup B)$?

- A) 1/3
- B) 11/36
- C) 5/18
- D) 11/18

<details>
<summary>Answer and explanation</summary>

**B) 11/36.**

Add the counts and subtract the double-counted overlap: $(6 + 6 - 1)/36 =
11/36 \approx 0.3056$. Option A is the naive sum: it counts the single shared
outcome twice, so it is too *large*, and 1/3 happens to be the number printed by
the `naive` line in the lesson's first code block. Option C (10/36) is a
guess with no counting behind it. Option D (22/36) counts the overlap twice and
then forgets to divide by 36 at all.

</details>

**Q5.** Someone proposes a model with $P(A) = 0.4$, $P(B) = 0.4$ and
$P(A \cap B) = 0.9$. What is wrong with it?

- A) Nothing — 0.9 is smaller than $0.4 + 0.4 = 0.8$ plus the overlap term
- B) Nothing — the two probabilities are equal, so A and B must be the same event
- C) An intersection can never be bigger than either of its events; 0.9 violates that
- D) Every probability in a finite uniform model must be a whole number of outcomes

<details>
<summary>Answer and explanation</summary>

**C) An intersection can never be bigger than either of its events; 0.9 violates that.**

Monotonicity gives $P(A \cap B) \le \min(P(A), P(B)) = 0.4$, so 0.9 is
impossible. Option A is self-defeating: $0.4 + 0.4 = 0.8 < 0.9$, so even the
addition rule rejects the table before overlap is considered. Option B confuses
equal probabilities with equal events — two different events can both have
probability 0.4. Option D is a real constraint only for *uniform finite*
models, and it is not the reason this table fails; probabilities in a weighted
model such as Exercise 2 are multiples of nothing in particular.

</details>

**Q6.** A model has $n$ distinguishable outcomes. How many events does it have,
and why does that number matter in code?

- A) $n$, because each outcome is exactly one event
- B) $2^n$, because every subset is an event, so enumerating all events is exponential in $n$
- C) $n!$, because events are orderings of the outcomes
- D) $2^n / 2$, because an event and its complement are the same event

<details>
<summary>Answer and explanation</summary>

**B) $2^n$, because every subset is an event, so enumerating all events is exponential in $n$.**

Four coins give 16 outcomes but 65,536 events. Option A is the common beginner
error: probability is a function on *subsets*, not on points. Option C confuses
events with permutations (Lesson 21). Option D is false — $A$ and $A^c$ are
different events whenever $A \ne \varnothing, \Omega$, which is exactly why the
complement rule $P(A^c) = 1 - P(A)$ carries information.

</details>

**Q7.** A die is loaded so that $P(6) = 0.27$. Nothing is known about the other
five faces. Which model is the right one?

- A) Take $\Omega = \{6\}$, the only outcome with nonzero probability
- B) Keep all six faces in Ω and attach a weight to each, with the five unknown weights sharing the remaining 0.73
- C) Keep all six faces, assign $P(6) = 1/6$, and correct the answer afterwards
- D) Treat it as a fair die and multiply the final answer by 0.27

<details>
<summary>Answer and explanation</summary>

**B) Keep all six faces in Ω and attach a weight to each, with the five unknown
weights sharing the remaining 0.73.**

A sample space records *what can happen*, so "the die shows 3" stays in Ω even
if you suspect $P(3) = 0$. Option A deletes a possible outcome to make the
arithmetic nicer — Mistake 2 in this lesson — and it destroys any question that
asks about faces 1 to 5. (Splitting the remaining 0.73 evenly gives 0.146 each,
which is a modelling choice you must declare, not a deduction.) Option C
builds a fair-die model and then mislabels one face, so the weights no longer
sum to 1 and the axioms fail. Option D applies the correction after doing the
counting, which cannot be right: the counting was only ever valid under
uniformity.

</details>

**Q8.** You roll two dice 300,000 times and observe the frequency of sum 7 is
0.16691, while the exact value is $1/6 \approx 0.166667$. What has been
established?

- A) The die is biased towards sums of 7
- B) Nothing at all: 300,000 trials cannot detect anything
- C) The observed frequency is consistent with $1/6$; the gap is ordinary sampling noise that shrinks as $1/\sqrt{n}$
- D) The true probability of sum 7 is 0.16691

<details>
<summary>Answer and explanation</summary>

**C) The observed frequency is consistent with 1/6; the gap is ordinary sampling
noise that shrinks as $1/\sqrt{n}$.**

The expected standard error at this sample size is
$\sqrt{p(1-p)/n} \approx \sqrt{0.1667 \cdot 0.8333 / 300000} \approx 0.00068$,
and the observed gap is 0.000243, well inside one standard error. Option A
asserts a bias that the data do not support — and with fair dice the theory
says there is none. Option B is an over-correction: the point of the frequency
view is that the number *does* pin down the mechanism once $n$ is large. Option
D confuses the estimate with the truth; 0.16691 is what *you* measured, and it
moves every time you re-run the experiment. Formalising "moves by $1/\sqrt{n}$"
is [Lesson 68](../part05_probability_statistics/68_law_of_large_numbers_and_clt.md).

</details>

**Q9.** Which counting machinery do you need to evaluate a classical
probability?

- A) Only the addition rule
- B) The product rule, permutations or combinations, and inclusion–exclusion — because you need $|\Omega|$ *and* $|A|$
- C) Only inclusion–exclusion
- D) Derivatives and integrals, because most experiments are continuous

<details>
<summary>Answer and explanation</summary>

**B) The product rule, permutations or combinations, and inclusion–exclusion —
because you need $|\Omega|$ *and* $|A|$.**

Classical probability is a ratio of two counts, so the entire problem is two
counting problems. Option A leaves $|A|$ uncounted. Option C leaves $|\Omega|$
uncounted — inclusion–exclusion is about not double counting the favourable
subset, not about the total. Option D is the interesting wrong answer: it is
right for infinite sample spaces, where $|A| / |\Omega|$ genuinely is undefined
and integral machinery replaces counting, but it is wrong for the finite
experiments this lesson is about.

</details>

**Q10.** In the deck example, $P(\text{no ace}) = 1128/1326$ and subtracting
gives $198/1326$ for "at least one ace", while counting "exactly one" and
"exactly two" separately also gives 192 + 6 = 198. Why is the agreement
guaranteed rather than lucky?

- A) Because $1128 + 198 = 1326$ happens to be true for these numbers
- B) Because both routes are consequences of the axioms, so they cannot disagree
- C) Because every probability model is additive over *all* events
- D) Because probabilities are always ratios of small integers

<details>
<summary>Answer and explanation</summary>

**B) Because both routes are consequences of the axioms, so they cannot
disagree.**

The complement rule and the addition rule are theorems derived from the same
three axioms, so any correct model must satisfy both. Option A confuses a
symptom with a cause: the sum $1128 + 198 = 1326$ is what the complement rule
*asserts*, not why it holds. Option C is the classic overreach — probabilities
add only for **disjoint** events; add 0.4 and 0.4 for overlapping events and you
get an answer above 1. Option D is false in general: with the weights from
Exercise 2 the answer is 0.1375, which is not a ratio of small integers.

</details>

## Subjective Questions

### Short Answer

**Q1. Define a *random experiment* and state the two properties the sample
space of that experiment must have.**

<details>
<summary>Answer</summary>

A random experiment is a procedure that produces one outcome and can in
principle be repeated under identical conditions — rolling a die, drawing a
card, timing a request. Its sample space Ω must be (1) **complete**: every
outcome that can occur is listed, including the ones you expect never to happen,
and (2) **expressive enough that every event of interest is a subset of Ω**. A
loaded die still has all six faces in Ω; it just has unequal weights. An Ω that
omits an outcome makes the mechanism unrepresentable and the resulting
assignment inconsistent.

</details>

**Q2. Why is "$P(A) = |A| / |\Omega|$" not a *definition* of probability?**

<details>
<summary>Answer</summary>

Because it only computes probabilities for finite sample spaces whose outcomes
are equally likely. It says nothing about a loaded die, a non-uniform user
distribution, or an infinite experiment — in each case the ratio either
contradicts intuition or is not defined ($\infty / \infty$). It also cannot be
the definition because the field needs one definition that covers classical
counting, long-run frequency and honest degrees of belief at the same time. It
is therefore a *derived result*: uniformity is an assumption, and if you assume
it, the axioms force the ratio.

</details>

**Q3. A die has $P(6) = 0.27$. Give one valid assignment of weights to the
other five faces and name the assumption you just made.**

<details>
<summary>Answer</summary>

Assume the remaining 0.73 is split evenly, giving $0.73/5 = 0.146$ to each of
faces 1 to 5. The full model is

$$P(\{1\}) = \cdots = P(\{5\}) = 0.146, \qquad P(\{6\}) = 0.27,$$

and the weights sum to $5(0.146) + 0.27 = 0.73 + 0.27 = 1$. The assumption is
the even split: the axioms only require the six weights to be nonnegative and to
sum to 1. A factory loading log might instead give you the real five numbers, in
which case use those.

</details>

**Q4. Write the relative frequency of event $A$ over $n$ runs, and give one
thing this view cannot do.**

<details>
<summary>Answer</summary>

$$f_n(A) = \frac{k_n}{n},$$

where $k_n$ is the number of runs in which $A$ occurred. It cannot assign a
probability to an experiment you cannot repeat: a coin still in the shop, the
third seed in your test suite, "this codebase has a race condition". It also
cannot distinguish a genuinely rare event from a temporarily broken one, and it
never converges if the mechanism itself drifts.

</details>

**Q5.** A model has four equally likely outcomes. How many events does it have,
and how many of them have probability exactly 1/4?

<details>
<summary>Answer</summary>

There are $2^4 = 16$ events, because each of the four outcomes may be in or out.
The events with probability exactly 1/4 are the subsets of size 1 or size 2:
$\binom{4}{1} = 4$ singletons and $\binom{4}{2} = 6$ pairs, so $4 + 6 = 10$
events. The remaining 6 events are the empty set, the full space, and the four
triples, with probabilities 0, 1 and 3/4.

</details>

**Q6. Why is it not a theorem that all outcomes in a sample space are equally
likely?**

<details>
<summary>Answer</summary>

Because the axioms say nothing about the mechanism. Kolmogorov's axioms
constrain how probabilities combine across events; the *values* are supplied by
the model. "Choose a card uniformly" and "this die is loaded" are both
consistent with the axioms — they are different assignments to the same Ω. So
uniformity is an assumption about the physics of the experiment, and the job of
the axioms is to guarantee that *given* the assignment, every rule you apply
downstream is consistent.

</details>

### Long Answer

**Q1. Applying $|A| / |\Omega|$ to a loaded die gives the wrong answer.
What exactly goes wrong, and how would you know from the axioms alone that
something is off?**

<details>
<summary>Model answer</summary>

Nothing goes wrong with the axioms — everything goes wrong with the *input*.
$|A| / |\Omega|$ is a ratio of cardinalities, so it treats every outcome as
equally likely by construction: it is a statement about sizes, not about
frequencies. For a die with $P(6) = 0.35$ and $P(1) = P(2) = 0.10$,
$|\{6\}| / |\Omega| = 1/6 \approx 0.1667$, while the correct answer is 0.35 — off
by a factor of two.

You can detect the error without any dice, because the two models contradict each
other on a set identity. The weighted model says $P(\Omega) = \sum_{o} P(\{o\})
= 2(0.10) + 3(0.15) + 0.35 = 1$. The uniform model built on the same six-element
Ω also satisfies $P(\Omega) = 6 \cdot (1/6) = 1$. Both are legal models of *a*
six-sided die; they simply are not the same model, and the axioms cannot tell
you which one your physical die follows.

What the axioms *can* tell you is that once you commit to the weights, every
derived rule holds — so for two independent rolls,
$P(\text{sum} = 8) = \sum_{a=2}^{6} P(a)P(7-a) = 0.1375$ exactly, matching the
simulation. The engineering lesson is that when outcomes are not equiprobable,
the model *is* the weights; you cannot recover them from cardinalities, and
declaring them is a modelling decision you must be able to defend.

</details>

**Q2. Why did the field adopt an axiom system rather than picking the
"relative frequency" or "degrees of belief" definition? What would be lost by
picking either one?**

<details>
<summary>Model answer</summary>

Because each of the three views is right in one place and silent in another.
Relative frequency is empirically convincing and is what you are trusting when a
dashboard says 0.2%, but it cannot assign a number to a non-repeatable claim,
and it depends on the mechanism staying fixed. Degrees of belief handle
non-repeatable claims, but "how strongly do you believe it" has no argument about
what counts as consistent — two honest people can assign different beliefs and
each satisfies the informal rules.

The axiomatic definition costs nothing and unifies them. Classical counting is
provably an instance of it (assign $1/|\Omega|$ to every outcome and check the
axioms). Relative frequency is provably an instance of it in the limit
(the law of large numbers, Lesson 68). Subjective belief is an instance of it
whenever the assignment obeys the axioms — which is precisely the Bayesian
position that degrees of belief *are* probabilities and therefore update by
Bayes' rule ([Lesson 62](../part05_probability_statistics/62_conditional_probability_and_bayes.md)).

So the gain is not elegance, it is *transfer*: a theorem proved from the axioms,
such as the central limit theorem, applies simultaneously to a mechanical
process, to an empirical measurement, and to a stated opinion. Pick the frequency
definition and the CLT only covers repeatable experiments; pick the belief
definition and it becomes a theorem about opinions, which nobody needs.

</details>

**Q3. A frequency estimate can be systematically wrong. Why is a *stable* wrong
frequency more dangerous in production than a noisy one?**

<details>
<summary>Model answer</summary>

Because every alert, threshold and SLO you write down is calibrated against
observed behaviour, not against the truth. A noisy estimate produces flaky
pages: the threshold sits near the true value, small fluctuations cross it, and
the noise itself tells you to distrust the alert. Engineers learn to ignore it,
which is already bad.

A stable wrong estimate produces no symptom at all. If a release silently shifts
the true failure rate from 0.2% to 0.25% and it stays there, the histogram looks
completely healthy — it is a tight, low-variance distribution around a number
nobody can see is wrong. Retries keep succeeding, dashboards stay green, and the
only evidence is a before-and-after comparison that nobody is running.

This is why `random.seed` matters even for a monitoring script: a demonstration
that re-runs to the same healthy number teaches the reader that the number is
stable, when it was only stable because the randomness was pinned. The
countermeasures are all in the later lessons — variance so you know what
deviation is normal ([Lesson 64](../part05_probability_statistics/64_expectation_variance.md)), the central limit
theorem so you know how much ([Lesson 68](../part05_probability_statistics/68_law_of_large_numbers_and_clt.md)),
and hypothesis testing so you can say whether a 12-to-15 shift is signal
([Lesson 69](../part05_probability_statistics/69_estimation_and_hypothesis_testing.md)).

</details>

**Q4. Why is "this event has probability 1" *not* the same claim as "this event
definitely happens"?**

<details>
<summary>Model answer</summary>

Because probability 1 describes a long-run rate, and a long-run rate of 1 does not
force every single trial to succeed. Take a fair coin and ask for the event
"heads". $P(\text{heads}) = 1/2$, so it certainly can fail. Now take an event
with probability exactly 1 that still fails in practice: in a model where a
continuous quantity is drawn uniformly, the event $X = 5$ has probability 1
under the discrete-style reasoning "P(5) = 1 out of 1" but probability 0 in the
continuous world ([Lesson 65](../part05_probability_statistics/65_continuous_random_variables.md)), and even
$P(X \ne 5) = 1$ does not mean $X \ne 5$ in any individual draw — it means the
draw lands somewhere other than exactly 5, which is not the same as being able to
name the point in advance.

Operationally this matters for exactly the questions programmers ask: "is this
branch guaranteed to run?", "will this cache hit always be present?". The
answer is that probability 1 tells you how often you can afford to be wrong,
which over $n$ runs means the failure rate is $0$ in the limit — not that the
next run is safe. If you need per-run safety you need an invariant in the code,
not a probability.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — two dice, a specific sum.** Two fair six-sided dice are
rolled. Compute P(sum = 8), P(sum is odd), and P(at least one die shows a 5).
Give each as an exact fraction and a decimal. Verify the three events are
genuinely different sizes.

<details>
<summary>Solution</summary>

|Ω| = 36 ordered outcomes.

- **P(sum = 8):** the outcomes are (2,6) (3,5) (4,4) (5,3) (6,2) → 5 outcomes,
  so 5/36 ≈ 0.138889.
- **P(sum odd):** the sum is odd exactly when one die is odd and the other is
  even. 3 odd faces × 3 even faces × 2 orderings = 18 outcomes, so 18/36 = 0.5.
- **P(at least one 5):** use the complement. No 5 means both dice come from
  {1,2,3,4,6}, so 5 × 5 = 25 outcomes. P = 1 − 25/36 = 11/36 ≈ 0.305556.
  Cross-check directly: exactly one 5 gives 2 × 5 = 10 outcomes, both 5s gives 1,
  total 11. ✓

They are all different: 0.1389 < 0.5 and 0.3056, confirming that "sum equals a
value" and "sum has a parity" and "a face appears" are unrelated shapes.

```python
from itertools import product

outcomes = list(product(range(1, 7), repeat=2))
n = len(outcomes)

p_sum8 = sum(1 for a, b in outcomes if a + b == 8) / n
p_odd = sum(1 for a, b in outcomes if (a + b) % 2 == 1) / n
p_has5 = sum(1 for a, b in outcomes if a == 5 or b == 5) / n

print(f"P(sum == 8)       = {p_sum8:.6f}  (5/36)")
print(f"P(sum odd)        = {p_odd:.6f}  (18/36)")
print(f"P(at least one 5) = {p_has5:.6f}  (11/36)")
```

</details>

**[ ] Exercise 2 — biased dice as weights.** A six-sided die has
P(1) = P(2) = 0.10, P(3) = P(4) = P(5) = 0.15, P(6) = 0.35. Compute P(sum = 8)
for two independent rolls of this die. Then compute the frequency of sum = 8
over 100,000 simulated rolls and confirm it is close.

<details>
<summary>Solution</summary>

The sample space is still 36 ordered pairs; only the weights change. Weight the
product: P((a,b)) = P(a)·P(b) because the rolls are independent.

The pairs summing to 8 are (2,6) (3,5) (4,4) (5,3) (6,2):

    0.10*0.35 = 0.035
    0.15*0.15 = 0.0225
    0.15*0.15 = 0.0225
    0.15*0.15 = 0.0225
    0.35*0.10 = 0.035
    --------------------
    total     = 0.1375

Note this is *below* the fair-die answer of 0.138889 — a plausible-looking
coincidence worth noticing, and a good reason not to eyeball probabilities.

```python
import random

weights = [0.10, 0.10, 0.15, 0.15, 0.15, 0.35]

def weighted_roll(rng):
    """Inverse transform sampling: walk the cumulative weights."""
    u = rng.random()
    running = 0.0
    for face, w in enumerate(weights, start=1):
        running += w
        if u < running:
            return face
    return 6

rng = random.Random(99)
print(f"sum of weights (must be 1.0): {sum(weights):.6f}")

exact = sum(weights[a - 1] * weights[7 - a] for a in range(2, 7))
print(f"P(sum == 8) exact = {exact:.6f}")

trials = 100_000
hits = sum(1 for _ in range(trials)
           if weighted_roll(rng) + weighted_roll(rng) == 8)
print(f"P(sum == 8) simulated = {hits / trials:.6f}")
```

</details>

**[ ] Exercise 3 — Challenge: three dice, no enumeration.** Three fair
six-sided dice are rolled. Compute P(the sum is 18) and P(at least one die shows
a 6) without writing code that enumerates all 216 outcomes, using only counting
principles. Then confirm both numbers by enumeration.

<details>
<summary>Solution</summary>

P(sum is 18): all three dice must show 6, so there is exactly 1 favourable
outcome out of 6³ = 216. P = 1/216 ≈ 0.004630.

P(at least one 6): complement. No die shows a 6, so each of the three dice has
5 options: 5³ = 125 outcomes. P = 1 − 125/216 = 91/216 ≈ 0.421296.

```python
from itertools import product

outcomes = list(product(range(1, 7), repeat=3))
n = len(outcomes)

by_counting_sum18 = 1 / 6**3
by_counting_any6 = 1 - 5**3 / 6**3
by_enumeration_sum18 = sum(1 for a, b, c in outcomes if a + b + c == 18) / n
by_enumeration_any6 = sum(1 for a, b, c in outcomes if 6 in (a, b, c)) / n

print(f"P(sum == 18):      counting {by_counting_sum18:.6f} "
      f"enumeration {by_enumeration_sum18:.6f}")
print(f"P(at least one 6): counting {by_counting_any6:.6f} "
      f"enumeration {by_enumeration_any6:.6f}")
```

</details>

**[ ] Exercise 4 — four coins, and how many events you are not going to
enumerate.** Four fair coins are tossed. (a) Give $|\Omega|$. (b) How many events
does this model have, and why is that number a problem for exhaustive code?
(c) Compute $P(\text{exactly two heads})$, $P(\text{the first two coins match})$,
and $P(\text{at least three heads})$ by counting. (d) Verify all three by
enumeration.

<details>
<summary>Solution</summary>

(a) The coins are distinguishable, so the outcomes are the $2^4 = 16$ strings.
$|\Omega| = 16$.

(b) There are $2^{16} = 65536$ events, because every subset of the 16 outcomes is
an event. That is the practical point: enumerating outcomes is $O(2^4) = 16$
steps, while enumerating events is $O(2^{16}) = 65536$ steps — and it gets worse
exponentially for each extra coin. Any question you can express as a subset test
can be answered by counting outcomes instead.

(c) **Exactly two heads:** choose which two coins are heads,
$\binom{4}{2} = 6$, so $P = 6/16 = 0.375$.

**First two coins match:** this event is "coin 1 = coin 2". Fix the last two coins
freely — $2^2 = 4$ choices — and then the first two must be either HH or TT,
which is 2 of the $2^2 = 4$ possible first-two patterns. So $|A| = 4 \times 2 = 8$
and $P = 8/16 = 0.5$.

Equivalently: flipping both of the first two coins pairs up the 16 outcomes so
that each pair contains one "match" and one "differ", which forces exactly half.
That is a nice reminder that a 50% answer usually has a clean symmetry argument
behind it.

**At least three heads:** exactly three heads gives $\binom{4}{3} = 4$ outcomes
and all four gives 1, so $|A| = 5$ and $P = 5/16 = 0.3125$.

(d) Enumeration confirms all three:

```python
from itertools import product

outcomes = list(product("HT", repeat=4))   # 16 distinguishable tosses
n = len(outcomes)
print(f"|Omega| = {n}, number of events = 2**{n} = {2**n}")

p_exactly2 = sum(1 for o in outcomes if o.count("H") == 2) / n
p_first2   = sum(1 for o in outcomes if o[0] == o[1]) / n
p_atleast3 = sum(1 for o in outcomes if o.count("H") >= 3) / n

print(f"P(exactly two heads) = {p_exactly2:.6f}  (6/16)")
print(f"P(first two match)   = {p_first2:.6f}  (8/16)")
print(f"P(at least 3 heads)  = {p_atleast3:.6f}  (5/16)")
```

</details>

**[ ] Exercise 5 — reading a frequency correctly.** A service has a long-run
failure rate of 0.2% and serves 6,000 requests per hour. (a) How many failures
does that describe per hour, and what exactly does it say about any particular
hour? (b) One hour shows 15 failures out of 6,000 requests, a rate of 0.25%. Can
you conclude the service has broken? (c) The next nine hours each return to
12 failures per 6,000 requests. What is the ten-hour rate, and what does that
demonstrate about per-hour alerting?

<details>
<summary>Solution</summary>

(a) $6000 \times 0.002 = 12$ failures. This is a long-run average: if you drew
one request at random from the whole day's traffic, about 2 in 1000 would be a
failure. It is *not* a prediction that the next hour produces exactly 12.

(b) 15 out of 6,000 is 0.25%, above the 0.2% rate — but one hour is a single
sample, and the mean count over that hour is 12, so a few extra failures are
ordinary variation. From the information given you cannot conclude a break: you
would need to know how much a single hour normally fluctuates, which is variance
([Lesson 64](../part05_probability_statistics/64_expectation_variance.md)) and hypothesis testing
([Lesson 69](../part05_probability_statistics/69_estimation_and_hypothesis_testing.md)).

(c) Total failures $15 + 9 \times 12 = 123$, total requests $10 \times 6000 =
60000$, so the ten-hour rate is $123/60000 = 0.00205 = 0.205\%$, essentially
back at the SLO. One 15-failure hour is diluted 10-to-1 and becomes invisible.

That is the argument for aggregating over a window long enough that the
long-run rate dominates the noise, or against comparing against a baseline
rather than a fixed threshold.

```python
long_run_rate = 0.002
requests_per_hour = 6_000
expected_failures = long_run_rate * requests_per_hour
print(f"expected failures per hour = {expected_failures}")

spike = 15
steady = 12
hours = 10
total_failures = spike + (hours - 1) * steady
total_requests = hours * requests_per_hour
print(f"spike hour rate      = {spike}/{requests_per_hour} = {spike/requests_per_hour:.5f}")
print(f"{hours}-hour rate       = {total_failures}/{total_requests} = {total_failures/total_requests:.5f}")
print(f"spike share of failures = {spike/total_failures:.4f} over 1 of {hours} hours")
```

</details>

**[ ] Exercise 6 — Challenge: an overlap you cannot see coming.** Three fair
six-sided dice are rolled. Let $A$ be "at least one die shows a 6" and $B$ be
"the sum is 12". Compute $P(A \cup B)$ by inclusion–exclusion, showing each count
separately and justifying it by counting rather than by listing all 216
outcomes. Then confirm by enumeration.

<details>
<summary>Solution</summary>

$|\Omega| = 6^3 = 216$ ordered triples.

**Count $|A|$ by the complement.** No die shows a 6, so each die has 5 choices:
$5^3 = 125$. Hence $|A| = 216 - 125 = 91$.

**Count $|B|$ by fixing the first die** and counting pairs for the other two.
For first die $a$, we need $b + c = 12 - a$ with $b, c \in \{1..6\}$; the number
of such pairs rises to 5 and then falls off at the top:

| first die $a$ | pairs $(b,c)$ | count |
| --- | --- | --- |
| 1 | $(5,6),(6,5)$ | 2 |
| 2 | $(4,6),(5,5),(6,4)$ | 3 |
| 3 | $(3,6),(4,5),(5,4),(6,3)$ | 4 |
| 4 | $(2,6),(3,5),(4,4),(5,3),(6,2)$ | 5 |
| 5 | $(1,6),(2,5),(3,4),(4,3),(5,2),(6,1)$ | 6 |
| 6 | $(1,5),(2,4),(3,3),(4,2),(5,1)$ | 5 |

Total $|B| = 2+3+4+5+6+5 = 25$. (Stars-and-bars agrees: $\binom{11}{2} - 3\binom{5}{2}
= 55 - 30 = 25$, subtracting the triples where one die exceeds 6.)

**Count $|A \cap B|$ by removing the all-at-most-5 triples from $B$.** Of the 25
triples summing to 12, those containing a 6 number 15. A cleaner way to see it:
count the triples summing to 12 whose dice are all at most 5, which is
$0 + 1 + 2 + 3 + 4 = 10$ as $a$ runs from 2 to 5, so $|A \cap B| = 25 - 10 =
15$.

**Combine.** $|A \cup B| = 91 + 25 - 15 = 101$, so
$P(A \cup B) = 101/216 \approx 0.467593$.

The trap in this exercise is that $91 + 25 = 116 > 101$ looks alarming but is
unavoidable: 15 triples satisfy *both* conditions, so the naive sum counts them
twice. A naive answer of 116/216 ≈ 0.537 is the classic double count.

```python
from itertools import product

outcomes = list(product(range(1, 7), repeat=3))
n = len(outcomes)

has6 = lambda o: 6 in o
sums12 = lambda o: sum(o) == 12

a = sum(1 for o in outcomes if has6(o))
b = sum(1 for o in outcomes if sums12(o))
both = sum(1 for o in outcomes if has6(o) and sums12(o))

print(f"|Omega| = {n}")
print(f"|A| (at least one 6) = {a}   by counting 216 - 5**3 = {216 - 5**3}")
print(f"|B| (sum == 12)     = {b}")
print(f"|A and B|           = {both}")
print(f"P(A union B) = ({a} + {b} - {both})/{n} = {(a + b - both) / n:.6f}")
print(f"naive double-counted answer = {(a + b) / n:.6f}  (too large)")
```

</details>

## Summary

- A probability model starts by naming the **sample space** Ω: every outcome that
  can occur, and nothing else.
- An **event** is a subset of Ω, so it is defined by set membership alone; with
  n outcomes there are 2ⁿ events.
- Probability is a function on events, defined by three axioms rather than by
  picking one interpretation ([Lesson 61](../part05_probability_statistics/61_probability_axioms_and_rules.md)).
- Classical probability is a **ratio of cardinalities**, |A| / |Ω|, which is why
  [Part 02](../part02_discrete_combinatorics/) is a hard prerequisite.
- Relative frequency and subjective belief are both *examples* of the
  axiomatic definition, so a theorem proved from the axioms covers all three.
- The axioms say nothing about outcomes being equally likely — uniformity is an
  assumption about the mechanism, not a mathematical fact.
- Choosing the sample space correctly (ordered versus unordered, weighted versus
  uniform) is where most wrong answers come from.
- Probability describes a long-run rate of a mechanism, never a guarantee about
  a single trial.

## Next

[61 — Probability Axioms and Rules](../part05_probability_statistics/61_probability_axioms_and_rules.md) states
the three axioms and derives every computational rule from them: the addition
rule, complements, multiplication, and inclusion–exclusion.