# 62 — Conditional Probability and Bayes' Theorem

**Part**: part05_probability_statistics · **Prerequisites**: 60 · **Time**: 35 min

---

## In Plain Words

Sometimes the question is not "will this happen?" but "given that this other
thing already happened, what's the chance?" That is conditional probability. The
information that something already happened slices the sample space down to a
smaller piece, and you are only allowed to count outcomes inside that piece.

The direction matters enormously. "The chance I have the disease given a positive
test" and "the chance of a positive test given the disease" are two different
questions with two different answers, and swapping them is the single most
consequential mistake people make with probability. Bayes' theorem is the machine
for swapping them back correctly.

The famous demonstration is medical testing. Suppose a disease affects 1 in 100
people, and a test detects it 99% of the time. The test's false alarm rate is
also very low. Intuitively you would expect a positive result to be almost
certain proof of disease. It is not. In fact, with those numbers, about five out
of every six people who test positive are actually healthy. The reason is not a
flaw in the test — it is arithmetic about how many healthy people there are to
begin with. We will work through every number of that example below.

Finally, if you assume a handful of features are independent, Bayes' theorem
turns into a classifier you can implement in twenty lines. That is naive Bayes,
and it remains a genuinely strong baseline for text classification.

## Why Computer Science Cares

- **Spam and abuse filtering.** A token seen mostly in spam should raise the
  spam score. Getting that right requires Bayes' theorem in the correct
  direction: the prior of "this is spam" times the likelihood of this token.
- **Anomaly detection.** "Is this request unusual?" is P(rare request pattern |
  current traffic) computed with a prior. Naive Bayes is a cheap, strong first
  model for intrusion detection.
- **Medical and diagnostic decision support**, where the base-rate fallacy is a
  documented cause of over-testing.
- **Sensor fusion and state estimation.** Kalman filters and particle filters are
  Bayes' rule applied repeatedly at each time step.
- **Interviews.** "A test is 99% accurate and 1 in 10,000 people have the
  disease — what is P(disease | positive)?" is a classic, and almost nobody gets
  it right first time.

## The Formal Version

**Definition.** For events A and B with P(B) > 0, the *conditional probability* of
A given B is

    P(A | B) = P(A ∩ B) / P(B)

Read aloud as "A given B". The division restricts attention to the outcomes in
B, so P(A | B) is the fraction of B that also lies in A.

Three sanity properties, all immediate from the definition:

1. If A ⊆ B then P(A | B) = 1.
2. If A ∩ B = ∅ then P(A | B) = 0.
3. If P(A | B) = P(A) for all B with P(B) > 0, then A and B are **independent**.

The conditional is a symmetric *set* operation: P(A ∩ B) = P(B ∩ A), so
P(A | B)P(B) = P(B | A)P(A) whenever both denominators are positive. This
symmetry is not an accident — it is the reason Bayes' theorem is easy.

**Definition.** The **chain rule** (for any events with positive denominators)

    P(A₁ ∩ A₂ ∩ ⋯ ∩ Aₙ) = P(A₁) P(A₂|A₁) P(A₃|A₁∩A₂) ⋯ P(Aₙ|A₁∩⋯∩Aₙ₋₁)

It follows by repeatedly substituting the definition of the conditional. It is
the probability version of a chain of multiplications, and it is the tool for
"do this, then that, then that" chains.

**Theorem (Bayes' theorem).** For any A, B with P(B) > 0,

    P(A | B) = P(B | A) · P(A) / P(B)

**Proof.** Start with the definition of the conditional and use the
symmetry P(A ∩ B) = P(B ∩ A):

    P(A | B) = P(A ∩ B)/P(B) = P(B ∩ A)/P(B)
             = P(B | A)·P(A) / P(B)          ∎

That is all. Every published form of Bayes' theorem is this line rearranged,
plus the law of total probability used to compute the denominator.

**Theorem (law of total probability).** If A₁, …, Aₙ are pairwise disjoint and
their union is Ω, then for any event B,

    P(B) = Σᵢ P(B | Aᵢ) · P(Aᵢ)

**Proof.** The events B ∩ A₁, …, B ∩ Aₙ are pairwise disjoint with union B, so
countable additivity gives P(B) = Σᵢ P(B ∩ Aᵢ) = Σᵢ P(B | Aᵢ)P(Aᵢ).  ∎

**Corollary (Bayes with a computable denominator).** Substitute the law of
total probability into Bayes' theorem:

    P(A | B) = P(B | A) · P(A) / Σᵢ P(B | Aᵢ) · P(Aᵢ)

This two-event form, written with named events, is the one used in practice:

    P(disease | positive) = P(positive | disease)·P(disease) /
                           [P(positive | disease)·P(disease)
                          + P(positive | healthy)·P(healthy)]

The four quantities have names worth learning, because almost all medical and
spam-filtering confusion is a mix-up between them:

| Name | Symbol | Meaning |
| --- | --- | --- |
| **Prior** | P(disease) | chance of the condition before any evidence |
| **Likelihood** | P(positive \| disease) | chance of this evidence given the condition |
| **Posterior** | P(disease \| positive) | chance of the condition after the evidence — what you want |
| **Evidence** | P(positive) | overall chance of seeing the evidence |

**Independence, restated as the naive Bayes assumption.** If X₁, …, Xₙ are
mutually independent given a class label C, then the likelihood factorises:

    P(X₁ = x₁, …, Xₙ = xₙ | C = c) = Πⱼ P(Xⱼ = xⱼ | C = c)

Bayes' theorem with this substitution is naive Bayes. The assumption is
dramatically wrong — words are obviously not independent ("free" and "click" co-
occur) — yet the classifier often still wins, because it needs the *ranking* of
classes, not calibrated probabilities, and the independence errors partly cancel.
This is called the "independence assumption is often false but its violations
are often in the same direction for all classes".

## Worked Example

### The medical test, completely

**The setup.** A disease affects 1 in 100 adults.

- Prevalence: P(disease) = 0.01
- Sensitivity (true positive rate): P(positive | disease) = 0.99
- False positive rate: P(positive | healthy) = 0.05

That means the test correctly flags 99% of sick people, and raises a false alarm
on 5% of healthy people. The remaining 1% is the false negative rate. Everyone
agrees the test is "very good". Now compute the posterior.

**Step 1 — build a population.** Make the arithmetic concrete by imagining
exactly 10,000 people, because proportions need someone to happen to.

| Group | Number of people |
| --- | --- |
| Has the disease | 100 (1% of 10,000) |
| Healthy | 9,900 |
| Total | 10,000 |

**Step 2 — apply the sensitivity.** Of the 100 sick people, 99% test positive:
99 × 0.99 = **98.01** people.

**Step 3 — apply the false positive rate.** Of the 9,900 healthy people, 5% test
positive: 9,900 × 0.05 = **495** people.

**Step 4 — count the positives.** 98.01 + 495 = **593.01** people test positive.

**Step 5 — the answer.** Of those, how many are actually sick?

    P(disease | positive) = 98.01 / 593.01 ≈ 0.1653

So **about one in six people with a positive result is actually sick**. About five
in six positive results are false alarms. This is the base-rate fallacy made
visible: the impressive-looking number 99% is P(positive | disease), and the
question people actually ask is P(disease | positive). They are not the same,
and when the disease is rare the population of healthy people is enormous
compared to the sick population, so the false alarms swamp the true ones.

**Step 6 — confirm with Bayes' theorem directly.**

    numerator   = 0.99 × 0.01 = 0.0099
    denominator = 0.99 × 0.01 + 0.05 × 0.99
                = 0.0099 + 0.0495 = 0.0594
    posterior   = 0.0099 / 0.0594 ≈ 0.1667

Same answer (the small discrepancy against step 5 is rounding in the
head-population arithmetic). The denominator is dominated by the second term
because 0.0495 is five times larger than 0.0099 — and that ratio is *entirely*
determined by the ratio of healthy to sick people in the population.

**Step 7 — interrogate the intuition.** Why is it so bad? Not because 5% sounds
like a bad test. Because the healthy population is 99 times larger than the sick
population, so 5% of 9,900 is 495 while 99% of 100 is 99. The 5% and the 99%
are both rates; rates only compare when applied to comparable-sized populations.

**Step 8 — push it further.** What if you made the test *perfect at not crying
wolf* — P(positive | healthy) = 0? Then the posterior is 0.0099/0.0099 = 1.
You *would* be certain. This is the only way to drive the posterior to 1 with a
finite population: eliminate false positives entirely.

**Step 9 — the uncomfortable version.** Keep the test exactly as it is (99%
sensitivity, 5% false positive rate) and change only the prevalence to 50%:

    numerator   = 0.99 × 0.50 = 0.495
    denominator = 0.495 + 0.05 × 0.50 = 0.495 + 0.025 = 0.520
    posterior   = 0.495 / 0.520 ≈ 0.952

Identical test, 95.2% instead of 16.7%. This is the lesson to carry away: the
reliability of a positive result is a property of the *population*, not of the
test. Any "accuracy" figure quoted without a prevalence is meaningless.

**Step 10 — the fix.** Two independent tests, each with the same error rates.
Both positive:

    numerator   = 0.01 × 0.99 × 0.99 = 0.009801
    denominator = 0.009801 + 0.99 × 0.05 × 0.05 = 0.009801 + 0.002475 = 0.012276
    posterior   = 0.009801 / 0.012276 ≈ 0.798

From 16.7% to about 80%. Repeating a slightly noisy test and requiring both to
fire is how real screening handles low prevalence, and the reason "confirmatory
testing" exists.

### The same arithmetic in spam filtering

Let P(spam) = 0.2 (20% of mail is spam). Suppose "free" appears in 40% of spam
messages and in 2% of legitimate mail. Then

    P(spam | contains "free") = 0.40 × 0.20 / (0.40×0.20 + 0.02×0.80)
                              = 0.08 / (0.08 + 0.016)
                              = 0.08 / 0.096 ≈ 0.833

A message containing "free" is spam with about 83% confidence — much higher than
the 20% prior. The word is genuinely informative. But note the structure is
identical to the medical test: prior × likelihood over the sum of both classes'
contributions.

## Runnable Code

### A reusable Bayes calculator from a 2×2 table

```python
def bayes_from_table(p_prior, p_evidence_given_true, p_evidence_given_false):
    """P(true | evidence) from a prior and two conditional probabilities.

    The three inputs are:
      p_prior                  P(true)
      p_evidence_given_true    P(evidence | true)      <- the LIKELIHOOD
      p_evidence_given_false   P(evidence | false)     <- false positive rate
    """
    # Numerator: the joint probability of true AND evidence.
    numerator = p_evidence_given_true * p_prior
    # Denominator: law of total probability over the two exhaustive cases.
    denominator = numerator + p_evidence_given_false * (1 - p_prior)
    return numerator / denominator


PREVALENCE = 0.01
SENSITIVITY = 0.99
FALSE_POSITIVE = 0.05

post = bayes_from_table(PREVALENCE, SENSITIVITY, FALSE_POSITIVE)
print("Medical test, disease prevalence 1%, sensitivity 99%, FPR 5%")
print(f"  P(disease)         prior        = {PREVALENCE}")
print(f"  P(+ | disease)     sensitivity  = {SENSITIVITY}")
print(f"  P(+ | healthy)     false pos.   = {FALSE_POSITIVE}")
print(f"  P(disease | +)     POSTERIOR    = {post:.4f}   <- what people actually ask")
print()
print(f"  sensitivity (what people quote) = {SENSITIVITY}")
print(f"  posterior    (what people want) = {post:.4f}")
false_share = 1 - post
print(f"  --> for every true positive there are {false_share / post:.2f} "
      f"false positives")
print(f"  --> i.e. {post * 100:.1f}% of positives are real")
print()

# Posterior as a function of prevalence, with the test held completely fixed.
print("prevalence | P(disease | +)")
for prev in (0.0001, 0.001, 0.01, 0.05, 0.10, 0.30, 0.50):
    p = bayes_from_table(prev, SENSITIVITY, FALSE_POSITIVE)
    bar = "#" * int(round(p * 40))
    print(f"{prev:9.4f} | {p:.4f} {bar}")

# A test with no false positives at all.
print()
perfect = bayes_from_table(PREVALENCE, SENSITIVITY, 0.0)
print(f"same test, false positive rate 0.00 -> posterior = {perfect:.4f}")

# Two independent tests, both positive.
n = PREVALENCE * SENSITIVITY ** 2
d = n + (1 - PREVALENCE) * FALSE_POSITIVE ** 2
print(f"two independent tests, both +    -> posterior = {n / d:.4f}")
```

### The population table, so the arithmetic can be seen

```python
PREVALENCE = 0.01
SENSITIVITY = 0.99
FALSE_POSITIVE = 0.05
POPULATION = 100_000

sick = POPULATION * PREVALENCE
healthy = POPULATION * (1 - PREVALENCE)
true_positives = sick * SENSITIVITY
false_positives = healthy * FALSE_POSITIVE
false_negatives = sick - true_positives
true_negatives = healthy - false_positives

print(f"population of {POPULATION:,}")
print(f"  sick                 {sick:10,.0f}")
print(f"  healthy              {healthy:10,.0f}")
print()
print(f"  test positive, sick  {true_positives:10,.0f}   <- true positives")
print(f"  test positive, well  {false_positives:10,.0f}   <- false positives")
print(f"  test negative, sick  {false_negatives:10,.0f}   <- missed the disease")
print(f"  test negative, well  {true_negatives:10,.0f}")
print()
print(f"total positives  = {true_positives + false_positives:,.0f}")
print(f"P(disease | +)   = {true_positives / (true_positives + false_positives):.4f}")
print(f"P(healthy  | +)  = {false_positives / (true_positives + false_positives):.4f}")
print()
print("A '99% accurate' test has 99% of sick people in the positive column,")
print("but only 1/6 of the positive column is sick, because 495 > 99.")
```

### Naive Bayes for text classification

```python
import math
from collections import Counter

# A toy corpus: (document, label). In production this is your mailbox.
CORPUS = [
    ("win money now click here free prize", "spam"),
    ("cheap pills discount order today free", "spam"),
    ("free prize claim your reward now win", "spam"),
    ("buy cheap followers fast delivery click", "spam"),
    ("free crypto airdrop send wallet win", "spam"),
    ("meeting at three bring the report", "ham"),
    ("please review my pull request thanks", "ham"),
    ("lunch tomorrow at the new place", "ham"),
    ("can you send me the design doc", "ham"),
    ("deploy is done let me know thanks", "ham"),
    ("the report from the meeting is ready", "ham"),
    ("lunch was good bring the report tomorrow", "ham"),
]

VOCAB = sorted({w for text, _ in CORPUS for w in text.split()})
CLASSES = ("spam", "ham")
doc_count = Counter(label for _, label in CORPUS)
total_docs = len(CORPUS)
word_count = Counter()          # total words per class, for the Laplace denominator
token_count = Counter()         # (class, word) -> occurrences


for text, label in CORPUS:
    for word in text.split():
        word_count[label] += 1
        token_count[(label, word)] += 1

V = len(VOCAB)
print(f"corpus: {total_docs} documents, vocabulary of {V} words")
print(f"documents per class: {dict(doc_count)}")
print()


def classify(text):
    """Return the posterior P(spam | text) under the naive Bayes model."""
    scores = {}
    for label in CLASSES:
        # Start from the log prior P(label) -- this is the prior Bayes needs.
        log_score = math.log(doc_count[label] / total_docs)
        for word in text.split():
            # Laplace smoothing: add 1 to every count so unseen words are still
            # possible instead of giving probability zero.
            numerator = token_count[(label, word)] + 1
            denominator = word_count[label] + V
            log_score += math.log(numerator / denominator)
        scores[label] = log_score

    # Convert log-scores to posteriors. exp(a) / (exp(a) + exp(b)) with a large
    # shift factor to avoid overflow; shifting both logs leaves the ratio intact.
    top = max(scores.values())
    w_spam = math.exp(scores["spam"] - top)
    w_ham = math.exp(scores["ham"] - top)
    return w_spam / (w_spam + w_ham), scores


for text in [
    "free prize click now",
    "free crypto wallet win",
    "can you review the report",
    "lunch tomorrow please",
    "free",          # a single token that appears in every spam message
    "quantum banana",  # a token that appears in neither
]:
    p_spam, scores = classify(text)
    verdict = "spam" if p_spam > 0.5 else "ham"
    print(f"{text!r:24} P(spam) = {p_spam:.4f}  log scores: "
          f"spam={scores['spam']:.2f} ham={scores['ham']:.2f}  -> {verdict}")
```

### Why naive Bayes is naive: the assumption, made measurable

The independence assumption says that knowing a message contains "free" leaves
the probability of "click" unchanged. Here is a direct measurement of whether
that holds, using the same corpus.

```python
import math
from collections import Counter

CORPUS = [
    ("win money now click here free prize", "spam"),
    ("cheap pills discount order today free", "spam"),
    ("free prize claim your reward now win", "spam"),
    ("buy cheap followers fast delivery click", "spam"),
    ("free crypto airdrop send wallet win", "spam"),
    ("meeting at three bring the report", "ham"),
    ("please review my pull request thanks", "ham"),
    ("lunch tomorrow at the new place", "ham"),
    ("can you send me the design doc", "ham"),
    ("deploy is done let me know thanks", "ham"),
    ("the report from the meeting is ready", "ham"),
    ("lunch was good bring the report tomorrow", "ham"),
]

doc_count = Counter(label for _, label in CORPUS)
total_docs = len(CORPUS)
word_count, token_count = Counter(), Counter()
for text, label in CORPUS:
    for w in text.split():
        word_count[label] += 1
        token_count[(label, w)] += 1
vocab = len({w for t, _ in CORPUS for w in t.split()})


def p_word(label, w):
    """P(w | label) with Laplace smoothing, exactly as the classifier uses."""
    return (token_count[(label, w)] + 1) / (word_count[label] + vocab)


# Does seeing "free" change the chance of "click"? Measure it directly.
label = "spam"
n_label = doc_count[label]
has_free = [t for t, lab in CORPUS if lab == label and "free" in t.split()]
with_free_click = [t for t in has_free if "click" in t.split()]
all_click = [t for t, lab in CORPUS if lab == label and "click" in t.split()]

p_click_given_free = len(with_free_click) / len(has_free)
p_click = len(all_click) / n_label

print(f"In the {n_label} spam documents:")
print(f"  documents containing 'free'  = {len(has_free)}")
print(f"  documents containing 'click' = {len(all_click)}")
print(f"  documents containing both    = {len(with_free_click)}")
print()
print(f"  P(click | free)     = {p_click_given_free:.4f}")
print(f"  P(click)            = {p_click:.4f}")
print(f"  independence would need these equal: "
      f"{abs(p_click_given_free - p_click) < 1e-12}")
print()
print("They differ, so the assumption is false. Naive Bayes ignores that and")
print("multiplies anyway -- which is why it is called NAIVE Bayes.")
print()
# What naive Bayes actually computes, versus the honest joint.
for label in ("spam", "ham"):
    naive = p_word(label, "free") * p_word(label, "click")
    print(f"  naive P(free)*P(click) | {label:4s} = {naive:.6f}")
print()
print("The naive ratio spam:ham is about 20 to 1, and the naive model")
print("still ranks spam above ham -- which is all the classifier needs")
print("in order to pick a label. The errors partly cancel in the ratio.")
```

What naive Bayes computes is the product of the marginals,
P(free | spam)·P(click | spam), which is 0.002076 for spam and 0.000102 for ham
— a ratio of about 20 to 1 in spam's favour. The honest joint probability is a
different number entirely. Both facts point the same way for the *ranking*, which
is the only thing the classifier uses. That is the whole defence of naive Bayes:
the independence assumption is false, but its errors tend to affect both classes
in similar ways, so the ranking survives even though the probabilities do not.


## Common Mistakes

**Mistake 1 — inverting the conditioning direction (the base-rate fallacy).**
Wrong: "The test is 99% sensitive, so a positive result means a 99% chance of
disease." Right: P(positive | disease) = 0.99 says that *of people who have the
disease*, 99% test positive. It says nothing directly about P(disease | positive),
which is the number 1/6. The temptation is enormous because the two phrases sound
like the same sentence, and "accuracy" is what test marketing reports.

**Mistake 2 — treating the denominator as P(B) without expanding it.** Writing
`P(A|B) = P(B|A)P(A)/P(B)` and then guessing that P(B) is about 0.5 will give an
answer of double the truth. P(positive) = 0.0594 in the example, not 0.5.
Always expand with the law of total probability and add every case.

**Mistake 3 — dividing by zero, or conditioning on an impossible event.**
P(A | B) is undefined when P(B) = 0. If you write `p_given_sick / p_sick` when
p_sick is 0, you get a ZeroDivisionError. In code, check the denominator and fall
back to the prior — conditioning on nothing tells you nothing, so the prior is
the correct limit.

**Mistake 4 — chaining independences that do not exist.** Writing
P(A ∩ B) = P(A)P(B) for "user clicked and then purchased" is almost always
wrong; purchase is far more likely after a click. Naive Bayes does exactly this
on purpose, which is fine for ranking but fatal if you want calibrated
probabilities out. State the assumption whenever you use it.

**Mistake 5 — ignoring that a posterior is only meaningful given the model.** A
posterior of 0.80 from a test with 5% false positives and 1% sensitivity is a
statement about *that test*. Feed in better numbers and the posterior moves, as
step 9 of the worked example shows with the identical test. Always ask what the
priors and likelihoods were before quoting the posterior.

## Exercises and Solutions

**[ ] Exercise 1 — the prosecutor's fallacy.** A city has 1,000 crimes per year.
Of those, 20 are violent. An eyewitness who saw a crime correctly identifies
whether it was violent 90% of the time, and mislabels it 40% of the time (they
call a non-violent crime violent far more often than the reverse). A witness
testifies that the crime was violent. Compute P(violent | testimony) and explain
why it differs so much from 90%.

<details>
<summary>Solution</summary>

The two rates are P(violent | testimony) = 0.90 and
P(testimony | non-violent) = 0.40. Bayes:

    numerator   = 0.90 × 0.02 = 0.018
    denominator = 0.018 + 0.40 × 0.98 = 0.018 + 0.392 = 0.410
    posterior   = 0.018 / 0.410 ≈ 0.0439

So about **4.4%**, not 90%. In concrete numbers over 1,000 crimes: 20 violent,
of which 18 get correct testimony; 980 non-violent, of which 392 get incorrect
"violent" testimony. Total violent testimonies = 18 + 392 = 410, and only 18 of
them are right.

The gap is the base rate again. The witness is accurate, but the population of
non-violent crimes is 49× larger, and 40% of 980 dwarfs 90% of 20. The defense
argument is not that the witness lies — it is that "the defendant is a violent
offender" is a statement about a rare event, and the conditional must be
inverted before it means anything.

```python
def bayes(p_prior, p_ev_given_true, p_ev_given_false):
    num = p_ev_given_true * p_prior
    return num / (num + p_ev_given_false * (1 - p_prior))


prior = 20 / 1000
post = bayes(prior, 0.90, 0.40)
print(f"P(violent | testimony) = {post:.6f}   (not 0.90)")
print()
violent = 20
nonviolent = 980
tp = violent * 0.90
fp = nonviolent * 0.40
print(f"violent crimes             {violent}")
print(f"non-violent crimes         {nonviolent}")
print(f"testimony 'violent', true  {tp:.0f}")
print(f"testimony 'violent', false {fp:.0f}")
print(f"total 'violent' testimony  {tp + fp:.0f}")
print(f"fraction that are correct  {tp / (tp + fp):.6f}")
```

</details>

**[ ] Exercise 2 — chain rule with a loaded die and a filter.** A die has
P(1)=P(2)=P(3)=0.1, P(4)=P(5)=P(6)=0.2. Two rolls are made. Compute
P(both rolls are 6) three ways: (a) independence, (b) the chain rule,
(c) by direct counting with unequal weights. Then compute P(sum = 7) — which of
these three approaches does *not* apply, and why?

<details>
<summary>Solution</summary>

(a) Independence: P = 0.2 × 0.2 = 0.04.

(b) Chain rule: P(X₁ = 6, X₂ = 6) = P(X₁ = 6)·P(X₂ = 6 | X₁ = 6). Rolls of a
die do not influence each other, so the conditional equals the marginal, 0.2,
giving 0.04 again. The chain rule always works; it is (a) that needs the
independence assumption, and here it happens to hold.

(c) Direct counting: the 36 ordered outcomes are not equally likely, so you
weight each: P((6,6)) = 0.2 × 0.2 = 0.04. The "counting" method degenerates
into (a) once you weight properly — this is the same observation from Lesson 60's
Example on loaded dice.

For sum = 7 there are exactly six ordered pairs: (1,6), (2,5), (3,4), (4,3),
(5,2), (6,1). Weight each one:

    0.1×0.2 = 0.02   (1,6)
    0.1×0.2 = 0.02   (2,5)
    0.1×0.2 = 0.02   (3,4)
    0.2×0.1 = 0.02   (4,3)
    0.2×0.1 = 0.02   (5,2)
    0.2×0.1 = 0.02   (6,1)
    ------------------------------------
    total  = 0.12

So **P(sum = 7) = 0.12**, not the 7/36 ≈ 0.1944 you would get by assuming all
36 pairs are equally likely. The reason the loaded die makes a *smaller* sum more
likely is that the extra weight sits on faces 4, 5 and 6, and getting a sum of 7
requires pairing a light face against a heavy one. Uniform counting would say
those six pairs are as likely as any others, which is false.

The multiplication rule applies (the rolls are independent), but "count the good
outcomes over 36" does not, because 36 is not |Ω| in any meaningful sense for a
non-uniform Ω.

```python
from itertools import product

weights = [0.1, 0.1, 0.1, 0.2, 0.2, 0.2]  # faces 1..6

# (a) independence
print(f"(a) P(6 and 6) = {weights[5] * weights[5]:.6f}")

# (b) chain rule: P(A and B) = P(A) P(B | A); rolls are independent so
#     P(second is 6 | first is 6) == P(second is 6) == 0.2
first6 = weights[5]
second_given_first6 = weights[5]
print(f"(b) chain rule      = {first6 * second_given_first6:.6f}")

# (c) direct weighted counting
pairs = [(x + 1, y + 1, weights[x] * weights[y])
         for x, y in product(range(6), repeat=2)]
print(f"(c) weighted count  = "
      f"{sum(w for a, b, w in pairs if a == 6 and b == 6):.6f}")

seven = sum(w for a, b, w in pairs if a + b == 7)
n_seven = sum(1 for a, b, _ in pairs if a + b == 7)
print(f"P(sum == 7) weighted = {seven:.6f}   over {n_seven} of 36 pairs")
print(f"P(sum == 7) if you wrongly assumed uniformity: {n_seven / 36:.6f}")
print("-> loading the die toward high faces makes sum 7 LESS likely,")
print("   because 7 needs a light face paired with a heavy one.")
```

</details>

**[ ] Exercise 3 — Challenge: build a working spam classifier and then break
it.** Write a naive Bayes classifier over the CORPUS above. (a) Verify it
classifies "free prize click now" as spam and "please review the report" as ham.
(b) Add the word "meeting" to a new spam training document
("meeting free prize click now") and re-examine what happens to the word
"meeting". (c) Explain the change in terms of the likelihood and why it is a
sensible inference rather than a bug.

<details>
<summary>Solution</summary>

(a) The original classifier handles both correctly: "free" and "click" appear
only in spam documents, so their likelihood ratio strongly favours spam; "please",
"review" and "report" appear only in ham documents, so they favour ham.

(b) The numbers below show exactly what one extra document does. Note first
that "meeting" was never *impossible* in spam — Laplace smoothing had already
given it a small positive probability of 0.0118. After adding the document,
P(meeting | spam) rises to 0.0222 while P(meeting | ham) is untouched at 0.0303.
So the likelihood ratio P(meeting|spam)/P(meeting|ham) moves from 0.39 to 0.73:
it nearly doubles, but it is still well below 1, so "meeting" remains weak
evidence *for* ham. Meanwhile "free" and "click", which appear in the new
document too, have their ratios *widened* (5.82 → 6.60 and 3.49 → 4.40), so the
classifier became more confident about the words it already understood.

(c) This is exactly what Bayes' theorem prescribes, and it is the correct
inference. One observed occurrence is weak evidence, not strong evidence — which
is why the "meeting" ratio moved by less than a factor of two while the words
seen many times gained proportionally less but stayed far stronger. The
practical worry is corpus scale: if a few hundred legitimate "meeting" messages
exist, they will swamp this single spam occurrence and push the ratio below 0.1.
That is why a production classifier trains on tens of millions of messages,
trains it continuously, and weights by frequency rather than trusting any single
document. It is also why using log-probability sums matters: no one word can
veto the classification on its own.

```python
import math
from collections import Counter

BASE = [
    ("win money now click here free prize", "spam"),
    ("cheap pills discount order today free", "spam"),
    ("free prize claim your reward now win", "spam"),
    ("buy cheap followers fast delivery click", "spam"),
    ("free crypto airdrop send wallet win", "spam"),
    ("meeting at three bring the report", "ham"),
    ("please review my pull request thanks", "ham"),
    ("lunch tomorrow at the new place", "ham"),
    ("can you send me the design doc", "ham"),
    ("deploy is done let me know thanks", "ham"),
    ("the report from the meeting is ready", "ham"),
    ("lunch was good bring the report tomorrow", "ham"),
]
# (b) We add ONE more spam document, and it happens to contain "meeting".
NEW_SPAM = ("meeting free prize click now", "spam")


def build(corpus):
    doc_count = Counter(label for _, label in corpus)
    word_count, token_count = Counter(), Counter()
    for text, label in corpus:
        for w in text.split():
            word_count[label] += 1
            token_count[(label, w)] += 1
    vocab = len({w for t, _ in corpus for w in t.split()})
    return doc_count, word_count, token_count, vocab


def likelihood(corpus_stats, label, word):
    doc_count, word_count, token_count, vocab = corpus_stats
    return (token_count[(label, word)] + 1) / (word_count[label] + vocab)


def predict(stats, text):
    doc_count, word_count, token_count, vocab = stats
    total = sum(doc_count.values())
    scores = {l: math.log(doc_count[l] / total) for l in doc_count}
    for w in text.split():
        for l in doc_count:
            scores[l] += math.log(likelihood(stats, l, w))
    top = max(scores.values())
    ws = math.exp(scores["spam"] - top)
    wh = math.exp(scores["ham"] - top)
    return ws / (ws + wh)


before = build(BASE)
after = build(BASE + [NEW_SPAM])

for text in ("free prize click now", "please review the report"):
    print(f"{text!r:30} P(spam) before={predict(before, text):.4f} "
          f"after={predict(after, text):.4f}")

print()
print("word      P(w|spam) before -> after    P(w|ham)   ratio before -> after")
for w in ("meeting", "free", "click"):
    ls0, la0 = likelihood(before, "spam", w), likelihood(after, "spam", w)
    lh0, lh1 = likelihood(before, "ham", w), likelihood(after, "ham", w)
    print(f"{w:9s} {ls0:.6f} -> {la0:.6f}   {lh0:.6f}   "
          f"{ls0 / lh0:.4f} -> {la0 / lh1:.4f}")
```

Two things are worth noticing. First, "free" and "click" both got *more*
spam-indicative: adding a spam document that uses them widened the ratio, which
is the point of training on more data. Second, the naive-Bayes decision is
unchanged in direction for every example, because the false independence
assumption was wrong by a roughly similar factor in both directions.

</details>

## Summary

- Conditional probability restricts the sample space: P(A|B) = P(A∩B)/P(B), and
  it is undefined when P(B) = 0.
- The chain rule multiplies a sequence of conditionals; independence is the
  special case where each conditional collapses to its marginal.
- Bayes' theorem follows in one line from the definition plus the symmetry of
  intersection: P(A|B) = P(B|A)P(A)/P(B).
- The law of total probability supplies the denominator, splitting every case
  that could produce the evidence.
- The base-rate fallacy is the practical cost of inverting a conditional:
  a 99% sensitive test with 5% false positives at 1% prevalence yields only a
  ~16.7% posterior.
- A posterior depends on the prior. The identical test gives 95% at 50%
  prevalence, so quoting "accuracy" without a prevalence is meaningless.
- Repeated independent tests and lowering false positives are the practical ways
  to raise a posterior in a low-prevalence population.
- Naive Bayes factorises the likelihood under a false independence assumption,
  yet still ranks classes well, which is why it remains a strong text baseline.

## Next

[63 — Discrete Random Variables](63_discrete_random_variables.md) stops asking
about events and starts naming outcomes: it introduces random variables as
functions on the sample space, probability mass functions, cumulative
distributions, and the Bernoulli and Binomial distributions in full.