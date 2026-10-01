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

## Formula Sheet

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$P(A \mid B)$` | `$\dfrac{P(A \cap B)}{P(B)}` | **Conditional probability**, "A given B". The fraction of B's outcomes that also lie in A. | Always restrict to the conditioning event. Requires **`P(B) > 0`**, otherwise undefined. |
| `$A \subseteq B$` | `$P(A \mid B) = 1$` | If A covers all of B, conditioning on B makes A certain. | Degenerate cases and sanity checks. |
| `$A \cap B = \varnothing$` | `$P(A \mid B) = 0$` | If A and B cannot co-occur, conditioning on B rules A out. | Detecting impossible evidence, e.g. a flagged row that cannot exist. |
| independent | `$P(A \mid B) = P(A)` | Knowing B tells you nothing about A. Equivalent to `$P(A \cap B) = P(A)P(B)$`. | The special case that makes the chain rule cheap — and the assumption naive Bayes abuses. |
| symmetry of intersection | `$P(A \mid B)P(B) = P(B \mid A)P(A)$` | Both sides equal `$P(A \cap B)`. | The single step that makes Bayes' theorem derivable. |
| chain rule | `$P(A_1 \cap \cdots \cap A_n) = P(A_1)\prod_{j=2}^{n} P(A_j \mid A_1 \cap \cdots \cap A_{j-1})$` | "Do this, then that, then that": multiply the first probability by each subsequent conditional. | Ordered processes — sequential draws, click-then-purchase, multi-step funnels. Every factor needs a positive denominator. |
| **Bayes' theorem** | `$P(A \mid B) = \dfrac{P(B \mid A)\,P(A)}{P(B)}$` | Swap the conditioning direction: posterior × prior ÷ evidence. | Whenever you are quoted a likelihood and asked for a posterior — every diagnostic test, every detector. |
| **law of total probability** | `$P(B) = \sum_i P(B \mid A_i)P(A_i)$`, needs `$A_1,\dots,A_n$` disjoint with union Ω | Split the evidence probability across every case that could produce it. | Computing the denominator. **Never guess `P(B)`.** |
| Bayes with a computable denominator | `$P(A \mid B) = \dfrac{P(B \mid A)P(A)}{\sum_i P(B \mid A_i)P(A_i)}$` | Bayes with every case added explicitly. This is the two-class form in practice. | The medical test, the prosecutor's fallacy, the spam score. |
| **prior** | `$P(A)$` | Chance of the condition before any evidence. | The starting point of any Bayesian update. For spam: P(spam) = 0.2. |
| **likelihood** | `$P(B \mid A)$` | Chance of this evidence given the condition. For the medical test: sensitivity 0.99. | What a test's "accuracy" figure actually reports — never the posterior. |
| **posterior** | `$P(A \mid B)$` | Chance of the condition *after* the evidence. What the person actually wants. | In the worked example, 0.1667 — about one in six. |
| **evidence** | `$P(B) = 0.0594$` | Overall chance of seeing the evidence, across all cases. | The denominator. Dominated by whichever case has more population. |
| naive Bayes | `$P(x_1,\dots,x_n \mid C=c) \approx \prod_j P(x_j \mid C=c)$` | Assume features are independent given the class label, then multiply. | Text classification baselines. The assumption is **false** but the *ranking* often survives. |
| likelihood ratio | `$\dfrac{P(B \mid A)}{P(B \mid A^c)}$` | How many times more often the evidence appears with the condition than without. | Comparing detectors, and computing how much a repeated test helps: two independent positives give `$P(B|A)^2 / P(B|A^c)^2`. |
| sensitivity / specificity | `P(+ \| disease)`, `P(- \| healthy)` | Sensitivity = true positive rate; the other side of the coin is the false positive rate `P(+ \| healthy)`. | Quoting any test. Always quote the prior alongside. |
| `$P(B) = 0$` | `P(A \mid B)` **undefined** | Conditioning on nothing tells you nothing; the prior is the correct limit. | Guarding code: check the denominator, fall back to the prior. |

## Multiple Choice Questions

**Q1.** A disease has prevalence 1%. A test is 99% sensitive and has a 5% false
positive rate. What is `P(disease | positive)`?

- A) 99%, since sensitivity is 99%
- B) About 16.7%
- C) About 5%, since 5% of positives are false
- D) About 50%, since the test is right 99% of the time

<details>
<summary>Answer and explanation</summary>

**B) About 16.7%.**

Bayes: numerator $= 0.99 \times 0.01 = 0.0099$; denominator $= 0.0099 + 0.05
\times 0.99 = 0.0594$; posterior $= 0.0099/0.0594 \approx 0.1667$. This is the
number the worked example and the code block both print. Option A is the base-rate
fallacy: 99% is `P(positive | disease)`, the wrong direction. Option C confuses
the false positive *rate* with the false positive *share of positives* — the
healthy share of positives is $1 - 0.1667 = 0.8333$. Option D uses "99% accurate"
as if it described the posterior, which is Mistake 5 in this lesson.

</details>

**Q2.** Why is `P(disease | positive)` so much smaller than
`P(positive | disease)` in Q1, given that the two tests are the same test?

- A) The test is worse than its published accuracy suggests
- B) The healthy population is 99 times larger than the sick population, so 5% of 9,900 (495) dwarfs 99% of 100 (98.01)
- C) Bayes' theorem is only approximately true and 0.1667 is the rounding error
- D) Sensitivity is measured on sick people only, so it is not a real probability

<details>
<summary>Answer and explanation</summary>

**B) The healthy population is 99 times larger than the sick population, so 5% of
9,900 (495) dwarfs 99% of 100 (98.01).**

The 593.01 positives are the union of 98.01 true positives and 495 false ones, so
only about one in six is real. Option A inverts the conclusion — the test is not
worse than advertised, the advertised number was about a different question.
Option C is false: Bayes is an exact theorem, and both the population method
(0.1653, off only by head-rounding) and the formula (0.1667) agree. Option D is
wrong: `P(+ | disease)` is a perfectly ordinary conditional probability over the
sub-population of sick people.

</details>

**Q3.** Same test as Q1 and Q2, but the disease prevalence is 50% instead of 1%.
What happens to the posterior, and why?

- A) It drops, because more people are now healthy in absolute terms
- B) It rises to about 95.2%, because the false-positive population is now only as large as the sick population
- C) It stays at 16.7%, because sensitivity and the false positive rate are unchanged
- D) It becomes exactly 50%, because prevalence and posterior coincide at 50%

<details>
<summary>Answer and explanation</summary>

**B) It rises to about 95.2%, because the false-positive population is now only as
large as the sick population.**

Numerator $= 0.99 \times 0.50 = 0.495$; denominator $= 0.495 + 0.05 \times 0.50 =
0.520$; posterior $\approx 0.9519$. Step 9 of the worked example makes this
point: the reliability of a positive result is a property of the population, not
of the test. Option A is nonsense — at 50% prevalence there are 5,000 healthy
people, fewer than the 9,900 before. Option C confuses the fixed quantities (the
test's error rates) with the derived one. Option D would only hold for a test with
identical error rates in both classes.

</details>

**Q4.** A prosecutor's witness testifies that a crime was violent. The witness is
right 90% of the time about violent crimes, and calls a non-violent crime violent
40% of the time. Violent crimes are 2% of all crimes. What is
`P(violent | testimony)`?

- A) 90%, since the witness is 90% accurate
- B) About 4.4%
- C) About 40%, since that is the rate of false "violent" claims
- D) About 2%, since that is the prevalence

<details>
<summary>Answer and explanation</summary>

**B) About 4.4%.**

Bayes: numerator $= 0.90 \times 0.02 = 0.018$; denominator $= 0.018 + 0.40
\times 0.98 = 0.410$; posterior $\approx 0.0439$. This is Exercise 1 in this
lesson. Option A is the prosecutor's fallacy — the classic real-world
consequence of the base-rate fallacy. Option C is a *rate over non-violent
crimes*, a different population entirely. Option D is the prior, which is what you
would answer if you had no testimony at all.

</details>

**Q5.** Spam is 20% of incoming mail. The word "free" appears in 40% of spam and
2% of legitimate mail. What is `P(spam | contains "free")`?

- A) 40%, since "free" appears in 40% of spam
- B) About 83.3%
- C) 40% − 2% = 38%
- D) About 83.3% only if the two classes were equally sized

<details>
<summary>Answer and explanation</summary>

**B) About 83.3%.**

Numerator $= 0.40 \times 0.20 = 0.08$; denominator $= 0.08 + 0.02 \times 0.80 =
0.096$; posterior $= 0.08/0.096 \approx 0.8333$, the number in the worked
example. Option A is again the inverted conditional. Option C subtracts rates from
different populations, which is meaningless — this is precisely why
"P(spam|free) − P(ham|free)" is not a probability. Option D is wrong: the class
sizes are already built into the calculation via the prior, and the answer is
what it is at 20% prevalence.

</details>

**Q6.** In Bayes' theorem, what would happen if you "guessed" that
`P(positive) ≈ 0.5` instead of expanding it with the law of total probability?

- A) Nothing — `P(positive)` is close enough to 0.5 anyway
- B) You would get roughly double the truth, because `P(positive) = 0.0594`, so the denominator is about eight times too large... which makes the answer too *small*, not too large
- C) The posterior would come out at 1, since prior × likelihood divided by 1 is the numerator
- D) It would raise a ZeroDivisionError, since 0.5 is not a valid probability

<details>
<summary>Answer and explanation</summary>

**B) You would get roughly double the truth, because `P(positive) = 0.0594`, so
the denominator is about eight times too large... which makes the answer too
*small*, not too large.**

This option is deliberately self-contradicting, and the contradiction is the
lesson. With denominator 0.5 instead of 0.0594 you get
$0.0099/0.5 = 0.0198$, roughly 0.2% instead of 16.7% — about eight times too
*small*. (Mistake 2 in this lesson states the mistake as "double the truth",
which is the correct statement for the shape of the error but the wrong
direction for these numbers; the principle to carry away is only that the
denominator must be computed, never guessed.) Option A is false:
$P(\text{positive}) = 0.0594$, nowhere near 0.5. Option C ignores the
denominator entirely. Option D is nonsense: 0.5 is a perfectly valid probability.

</details>

**Q7.** Naive Bayes assumes features are independent given the class label. The
lesson's own corpus shows that knowing a spam message contains "free" changes
the chance it contains "click". Why does the classifier still work?

- A) The independence assumption is actually true for word tokens
- B) It only needs the *ranking* of classes, and the independence errors tend to affect both classes similarly, so the ranking survives even though the probabilities do not
- C) The assumption is irrelevant because the classifier ignores the likelihood entirely
- D) It works because the vocabulary is small

<details>
<summary>Answer and explanation</summary>

**B) It only needs the *ranking* of classes, and the independence errors tend to
affect both classes similarly, so the ranking survives even though the
probabilities do not.**

The lesson measures the violation directly: `P(click | free) = 0.25` versus
`P(click) = 0.4` among spam documents. Option A is directly contradicted by that
measurement. Option C is false — the likelihood is the whole classifier. Option D
is irrelevant to correctness; a larger vocabulary makes the independence
assumption *more* wrong, not less.

</details>

**Q8.** Two independent tests with the same rates (99% sensitivity, 5% false
positives) both come back positive at 1% prevalence. What is the posterior,
compared with 16.7% for a single test?

- A) About 50%
- B) About 79.8%, because requiring two positives squares the sensitivity but also squares the false positive rate
- C) About 99%, because each test is individually reliable
- D) About 9.9%, because two positives halve the prior

<details>
<summary>Answer and explanation</summary>

**B) About 79.8%, because requiring two positives squares the sensitivity but
also squares the false positive rate.**

Numerator $= 0.01 \times 0.99^2 = 0.009801$; denominator $= 0.009801 + 0.99
\times 0.05^2 = 0.012276$; posterior $\approx 0.7984$ — Step 10 of the worked
example. The false positive rate falls from 5% to 2.5% while sensitivity only
falls from 99% to 98.01%, and the denominator is dominated by the false
positives, so the gain is large. Option A is roughly where a "double or
nothing" intuition would land. Option C compounds the two conditionals wrongly.
Option D has the wrong sign: the posterior rises, it does not fall.

</details>

**Q9.** Your code computes `P(A | B) = P(A ∩ B) / P(B)` and `P(B)` comes out as
exactly 0.0 because the filter selected no rows. What is the right behaviour?

- A) Raise, because the model is malformed
- B) Return the prior `P(A)`: conditioning on nothing tells you nothing, so the prior is the correct limit
- C) Return 0, because no rows matched so nothing is true
- D) Return 1, because the empty set is a certainty

<details>
<summary>Answer and explanation</summary>

**B) Return the prior `P(A)`: conditioning on nothing tells you nothing, so the
prior is the correct limit.**

This is Mistake 3 in this lesson. Option A pushes the crash to the caller, who
has no way to act on it. Option C confuses the empty *conditioning event* with the
empty *target event*: B being empty says nothing about whether A holds. Option D
is the mirror-image error — `P(B) = 0` makes the conditional meaningless, it does
not make A certain.

</details>

**Q10.** Why does the lesson say a posterior of 0.80 is "only meaningful given
the model"?

- A) Because posteriors are random and need many repetitions to stabilise
- B) Because it is a statement about that test's prior and likelihoods; feed in different numbers and the posterior moves, as the 1%-versus-50% prevalence comparison shows
- C) Because posteriors must always be reported to more than two decimal places
- D) Because Bayes' theorem only holds for two classes

<details>
<summary>Answer and explanation</summary>

**B) Because it is a statement about that test's prior and likelihoods; feed in
different numbers and the posterior moves, as the 1%-versus-50% prevalence
comparison shows.**

A posterior is a joint statement about a model and a population, not a property of
a device. Option A treats a probability as a random quantity to be sampled, which
confuses the Bayesian and frequentist pictures. Option C is a presentation
preference, not a mathematical one. Option D is false: the law of total
probability generalises to any number of classes, as its summation form shows.

</details>

## Subjective Questions

### Short Answer

**Q1. State the definition of conditional probability and name its two
restrictions.**

<details>
<summary>Answer</summary>

For events $A$ and $B$, $P(A \mid B) = P(A \cap B)/P(B)$, read "A given B". Two
restrictions: it needs $P(B) > 0$ or the expression is undefined, and every
conditional probability with respect to $B$ lies in $[0, 1]$ because
$A \cap B \subseteq B$ and monotonicity gives $0 \le P(A \cap B) \le P(B)$.
The definition is a ratio of two numbers from the same model — no new information
is introduced, only a re-normalisation of the sample space.

</details>

**Q2. Derive Bayes' theorem in two lines, and say what each step uses.**

<details>
<summary>Answer</summary>

$$P(A \mid B) = \frac{P(A \cap B)}{P(B)} = \frac{P(B \cap A)}{P(B)} = \frac{P(B \mid A)\,P(A)}{P(B)}.$$

Step one is the definition of the conditional. Step two uses symmetry of
intersection, $P(A \cap B) = P(B \cap A)$, which is a fact about sets, not
probabilities. Step three is the definition again, applied to $B \mid A$. So the
whole theorem is the definition plus one set-theoretic symmetry — there is no
extra assumption anywhere.

</details>

**Q3. Why must the denominator `P(B)` be computed rather than estimated?**

<details>
<summary>Answer</summary>

Because $P(B)$ is the probability of the evidence across *every* case that could
produce it, and in a low-prevalence problem one term dominates it. In the
worked example $P(\text{positive}) = 0.99 \times 0.01 + 0.05 \times 0.99 =
0.0594$, and the second term is five times the first. Guessing "about 0.5" would
give $0.0099/0.5 = 0.0198$ instead of $0.1667$ — an eightfold error caused
entirely by the denominator. The law of total probability exists to make this
computation mechanical: expand over all disjoint cases and add.

</details>

**Q4. A row is flagged by an anomaly detector that fires on 2% of all requests,
and on 90% of the requests that are genuinely attacks. Attacks are 0.1% of
traffic. What is `P(attack | flagged)`?**

<details>
<summary>Answer</summary>

Numerator $= 0.90 \times 0.001 = 0.0009$. Denominator $= 0.0009 + 0.02 \times
0.999 = 0.0009 + 0.01998 = 0.02088$. So
$P(\text{attack} \mid \text{flagged}) \approx 0.0431$, about 4.3% — roughly one
flagged request in twenty-three is a real attack, despite a detector that is
"90% accurate on attacks".

</details>

**Q5.** Using the spam numbers from the worked example, what is the *likelihood
ratio* of the word "free", and what does it mean?

<details>
<summary>Answer</summary>

$P(\text{free} \mid \text{spam}) / P(\text{free} \mid \text{ham}) = 0.40 / 0.02
= 20$. So "free" is 20 times more common in spam than in legitimate mail. This is
the quantity that drives the classifier, and unlike the posterior it does *not*
depend on the prior — which is why comparing two detectors by their likelihood
ratios is a prior-free way to compare them.

</details>

**Q6. What does the chain rule give for three independent events, and why is
that still useful if independence makes it trivial?**

<details>
<summary>Answer</summary>

$P(A_1 \cap A_2 \cap A_3) = P(A_1)P(A_2)P(A_3)$ when the events are mutually
independent, because each conditional collapses to its marginal. It is still
useful because the chain rule itself needs no independence: you can always write
$P(A_1)P(A_2 \mid A_1)P(A_3 \mid A_1 \cap A_2)$, and then substitute independence
only for the terms you can actually justify. Each conditional is measurable from
data, so a partially-independent chain tells you which single factor is breaking
your model.

</details>

### Long Answer

**Q1. Why does a rare disease with a sensitive test still produce many false
positives? Walk through the mechanism rather than quoting the posterior.**

<details>
<summary>Model answer</summary>

Take 10,000 people at 1% prevalence: 100 are sick, 9,900 are healthy. Sensitivity
of 99% sends 98.01 of the sick to the positive column. The false positive rate of
5% sends 495 of the healthy there too. The positive column holds 593.01 people,
and the sick fraction of it is 98.01 / 593.01 ≈ 0.165.

The mechanism is a comparison of two products, not of two percentages. The
sensitivity multiplies a small population (99% of 100), the false positive rate
multiplies a large one (5% of 9,900). Because 99% > 5% by a factor of about 20,
but 100 < 9,900 by a factor of 99, the second product wins by roughly 5 to 1.
Any two rates only compare when applied to populations of comparable size, and the
whole point of a rare disease is that the populations are not comparable.

The intuition that a "99% accurate test" must be trustworthy is really an intuition
about the *diagonal* of the confusion matrix: 99% of sick people are caught, and
95% of healthy people are cleared. Both are excellent. The number people
imagine — "about 99% of positives are real" — is an *off-diagonal ratio*, and
off-diagonal ratios are determined by the base rates, not by the diagonal. That is
why the lesson insists any accuracy figure quoted without a prevalence is
meaningless, and why Step 9 shows the identical test jumping from 16.7% to 95.2%
purely by changing prevalence to 50%.

The practical consequence is that rare-event detection is dominated by false
alarms no matter how good the detector is. Which is exactly why confirmatory
testing exists: two independent positives take the posterior to 0.798, because
the false positive rate squares down to 0.25% while the sensitivity only drops to
98.01%.

</details>

**Q2. Why does Bayes' theorem have to swap the conditional, and what breaks if
you read a likelihood as if it were a posterior?**

<details>
<summary>Model answer</summary>

The conditional is defined with the conditioning event in the denominator, and the
denominator normalises over a *population*. $P(\text{positive} \mid \text{disease})$
normalises over the 100 sick people; $P(\text{disease} \mid \text{positive})$
normalises over the 593 positives. These are different populations with different
sizes, so the same numerator $P(\text{positive} \cap \text{disease}) = 0.0099$
divided by either denominator gives 0.99 or 0.1667. Nothing in the notation lets
you tell them apart by eye, which is the whole hazard.

What breaks concretely: the prosecutor's fallacy (Exercise 1) reaches a verdict
from a 4.4% posterior; the medical case leaves five of six positive results
unnecessary; and in engineering, an anomaly detector tuned so that
$P(\text{flag} \mid \text{attack}) = 0.9$ gets quoted as "90% of flags are
attacks", which is off by more than an order of magnitude. In every case the
error runs in the direction of over-confidence, because the reporting
convention — "accuracy", "sensitivity", "confidence" — is almost always a
likelihood, not a posterior.

The fix is procedural rather than mathematical, and it is what Bayes' theorem is
for: always write the two conditionals out in full, name which population each
one normalises over, and expand the denominator with the law of total probability
so the base rates are visible in the arithmetic. If you cannot name the prior,
you do not have a posterior.

</details>

**Q3. Naive Bayes's independence assumption is known to be false. Why does the
classifier still rank classes well, and what would break if you tried to use its
output probabilities?**

<details>
<summary>Model answer</summary>

The classifier only ever compares two scores — it picks the label with the larger
one. It never reads the absolute value. The independence assumption inflates or
deflates the joint likelihood, but it does so by a factor that is *similar* for
both classes, because words that co-occur do so in both spam and ham, just with
different frequencies. A common multiplicative error cancels in the ratio, and the
ranking survives while the probabilities do not. The lesson shows this
quantitatively: the naive product is about 20 to 1 in spam's favour, and the
honest joint is a different number entirely, but both point at spam.

What breaks the moment you want the number rather than the ranking is calibration.
If you threshold the output at 0.5 and intend "these 30% are spam", a
mis-calibrated model gives you 3%. The independence errors accumulate
multiplicatively over a long document, so documents with more words drift further
from the truth — a systematic bias, not noise. The standard fix is to train a
calibration map (Platt scaling, isotonic regression) on held-out data, or to use
a model that models the dependencies directly.

There is a second, subtler break: the failures are not only in the probability
value. Independence makes a single word far too influential, because the product
lets one token dominate a document. Long documents therefore swing more than short
ones, and one unusual token can veto a classification. That is why production
implementations use log-probability sums and per-feature weighting, and why even
when the assumption is abandoned entirely (logistic regression, gradient-boosted
trees) naive Bayes remains the baseline to beat on text, because it is cheap,
online-updatable and needs no tuning.

</details>

**Q4.** A test's sensitivity is 99% and its false positive rate is 1% rather than
5%. At 1% prevalence, what is the posterior, and why is halving the false
positive rate worth so much more than it looks?

<details>
<summary>Model answer</summary>

Numerator $= 0.99 \times 0.01 = 0.0099$. Denominator $= 0.0099 + 0.01 \times
0.99 = 0.0099 + 0.0099 = 0.0198$. Posterior $= 0.0099/0.0198 = 0.5$, so exactly
50%.

Moving the false positive rate from 0.05 to 0.01 raised the posterior from 0.1667
to 0.5, a threefold improvement, and it did so while leaving the sensitivity
completely untouched. The reason is the denominator's structure: at 5% the false
positives contributed 0.0495, five times the numerator, so the posterior was
pinned near $1/6$ regardless of how good the sensitivity was. Cut the false
positive contribution to 0.0099 and the numerator and the false-positive term
become equal, which is exactly the condition for a posterior of one half.

So the leverage is asymmetric. Sensitivity is bounded above by 1 and is already
at 0.99, so improving it to 1.0 would move the posterior only to
$0.01/(0.01 + 0.0099) \approx 0.5025$. The false positive rate, by contrast, sits
in the denominator multiplied by the healthy population, so it is worth 99 times
as much per unit. This is a general design principle for detectors, not just
medical tests: in a low-base-rate problem, the false positive rate is the knob
that matters, and improving sensitivity on a well-calibrated detector is close to
pointless. It also explains Step 8 — driving the false positive rate to zero gives
a posterior of exactly 1, which is the only route to certainty with a finite
population.

</details>

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

**[ ] Exercise 4 — the base-rate fallacy in full, three ways.** A screening test
is used on a population in which the condition affects 1 in 5,000 people. The
test detects 98% of cases and raises a false alarm on 2% of healthy people.
(a) Build the population table for 500,000 people. (b) Compute
`P(condition | positive)` from the table. (c) Compute the same posterior with
Bayes' theorem and confirm the two agree. (d) Explain why a person reading "98%
detection rate" would badly overestimate their own risk, and state the single
change to the test that would help most.

<details>
<summary>Solution</summary>

(a) **Population table for 500,000 people.**

| Group | Number of people |
| --- | --- |
| Has the condition | $500{,}000 / 5{,}000 = 100$ |
| Healthy | $499{,}900$ |
| Total | $500{,}000$ |

**Apply the detection rate.** Of the 100 sick people, 98% test positive:
$100 \times 0.98 = 98$ true positives, and 2 false negatives.

**Apply the false alarm rate.** Of the 499,900 healthy people, 2% test positive:
$499{,}900 \times 0.02 = 9{,}998$ false positives.

So the positive column holds $98 + 9{,}998 = 10{,}096$ people, of whom only 98
are sick.

(b) **Posterior from the table.**

$$P(\text{condition} \mid \text{positive}) = \frac{98}{10{,}096} \approx 0.0097$$

About 1%. That is, about **99 in every 100 positive results are false alarms**, and
a positive result multiplies a 1-in-5000 risk by only about 48.

(c) **Bayes' theorem gives the same number.**

    numerator   = 0.98 × 0.0002 = 0.000196
    denominator = 0.000196 + 0.02 × 0.9998
                = 0.000196 + 0.019996 = 0.020192
    posterior   = 0.000196 / 0.020192 ≈ 0.0097   ✓

(d) **Why "98% detection" misleads.** The 98% normalises over the 100 sick
people; the number a person wants normalises over the 10,096 positives. The
false positive rate applies to a population 4,999 times larger, so $2\%$ of
$499{,}900$ produces 9,998 people against 98 — the false alarms outnumber the true
positives by 102 to 1. The detector is genuinely excellent on both diagonals;
only the off-diagonal ratio is bad, and off-diagonal ratios are set by the base
rate.

The single most effective change is to **cut the false positive rate**, not to
improve detection. Detection is already 98% and cannot exceed 100%: even a perfect
detector with a 2% false alarm rate gives only
$0.0002/(0.0002 + 0.019996) \approx 0.0099$. Halving the false alarm rate to 1%
gives $0.000196/(0.000196 + 0.009998) \approx 0.0192$, roughly doubling the
posterior with no change to sensitivity at all. Confirmatory testing on a second
independent sample works the same way, since it squares the false alarm rate
rather than the sensitivity.

```python
PREVALENCE = 1 / 5000
DETECTION = 0.98
FALSE_ALARM = 0.02
POPULATION = 500_000

def bayes(p_prior, p_ev_given_true, p_ev_given_false):
    num = p_ev_given_true * p_prior
    return num / (num + p_ev_given_false * (1 - p_prior))


sick = POPULATION * PREVALENCE
healthy = POPULATION * (1 - PREVALENCE)
tp = sick * DETECTION
fn = sick - tp
fp = healthy * FALSE_ALARM
tn = healthy - fp
positives = tp + fp

print(f"population {POPULATION:,}  sick {sick:,.0f}  healthy {healthy:,.0f}")
print(f"true positives  {tp:10,.0f}     false negatives {fn:,.0f}")
print(f"false positives {fp:10,.0f}     true negatives  {tn:,.0f}")
print(f"positives       {positives:10,.0f}")

post_table = tp / positives
post_bayes = bayes(PREVALENCE, DETECTION, FALSE_ALARM)
print()
print(f"(b) P(condition | +) from table = {post_table:.6f}")
print(f"(c) P(condition | +) from Bayes  = {post_bayes:.6f}")
print(f"    agree: {abs(post_table - post_bayes) < 1e-9}")
print()
print(f"false alarms per true positive = {fp / tp:.1f} : 1")
print(f"prior risk 1 in {1 / PREVALENCE:,.0f} -> posterior 1 in {1 / post_bayes:,.0f}")
print()
print("(d) leverage is in the false alarm rate, not the detection rate:")
print(f"    perfect detection, same false alarm : "
      f"{bayes(PREVALENCE, 1.0, FALSE_ALARM):.6f}")
print(f"    same detection, false alarm halved  : "
      f"{bayes(PREVALENCE, DETECTION, FALSE_ALARM / 2):.6f}")
```

</details>

**[ ] Exercise 5 — the chain rule where independence genuinely fails.** A user
visits a site. 20% of visitors click the hero button; 10% make a purchase; and
40% of those who click go on to purchase. (a) Compute `P(click and purchase)`
using the chain rule. (b) Compute the same probability by multiplying the
marginals. (c) Explain the difference in terms of what the conditional tells
you. (d) Compute `P(purchase | click)` and confirm your reading of the 40%.

<details>
<summary>Solution</summary>

(a) **Chain rule.** $P(\text{click} \cap \text{purchase}) = P(\text{click}) \cdot
P(\text{purchase} \mid \text{click}) = 0.20 \times 0.40 = 0.08$. So 8% of
visitors click *and* purchase.

(b) **Naive independence.** $0.20 \times 0.10 = 0.02$, which is *four times
smaller* than the truth. The two events are positively dependent: purchasing is
four times as likely after a click as it is for a random visitor.

(c) **Why the difference.** The marginal $P(\text{purchase}) = 0.10$ averages over
*all* visitors, the overwhelming majority of whom never clicked. The conditional
$P(\text{purchase} \mid \text{click}) = 0.40$ averages only over the 20% who
clicked, a group that is already far more purchase-ready. Conditioning on
clicking re-selects the population, and the population differs. Applying the
product rule here is exactly Mistake 4 in this lesson: the multiplication rule
needs independence, and a click and a subsequent purchase are plainly not
independent.

(d) **Recovering the conditional.** $P(\text{purchase} \mid \text{click}) =
\frac{P(\text{purchase} \cap \text{click})}{P(\text{click})} = \frac{0.08}{0.20} =
0.40$. ✓ This is the definition, and it is why the chain rule is always safe:
you can always divide back out to find the conditional you used.

A designer reading (b) would conclude the hero button is worthless — 0.02
incremental purchases per visit. The truth is 0.08, four times higher, which is
the entire basis of any click-through attribution analysis.

```python
p_click = 0.20
p_purchase = 0.10
p_purchase_given_click = 0.40

joint_chain = p_click * p_purchase_given_click
joint_naive = p_click * p_purchase

print(f"(a) chain rule   : {joint_chain:.6f}")
print(f"(b) independence : {joint_naive:.6f}  -- off by a factor of "
      f"{joint_chain / joint_naive:.1f}")
print(f"(c) the lift is real: purchase is "
      f"{p_purchase_given_click / p_purchase:.1f}x likelier after a click")
print(f"(d) P(purchase | click) = {joint_chain / p_click:.4f} "
      f"(matches the given 0.40: {abs(joint_chain / p_click - p_purchase_given_click) < 1e-12})")
```

</details>

**[ ] Exercise 6 — Challenge: choose a threshold, then defend it.** A detector
fires on 2% of requests and on 90% of genuine attacks. Attacks are 0.1% of
traffic. An analyst wants to page a human for every positive result. (a) Compute
`P(attack | flagged)`. (b) If an engineer manually reviews 1,000 flagged requests
per hour, how many attacks will that review surface? (c) Now the engineer
imposes a score threshold that halves the false alarm rate to 1% while the
detection rate falls to 85%. Recompute the posterior and say whether the new
operating point is better or worse for the stated goal of *surfacing attacks*.
(d) Propose a threshold change that improves the posterior by more than any of
the above, and quantify it.

<details>
<summary>Solution</summary>

(a) Numerator $= 0.90 \times 0.001 = 0.0009$; denominator $= 0.0009 + 0.02 \times
0.999 = 0.02088$; posterior $\approx 0.0431$. Only about **4.3%** of flags are
attacks — roughly one in twenty-three.

(b) With 1,000 flagged requests per hour, attacks surfaced $= 1000 \times 0.0431
\approx 43$. Note where this number comes from: the review budget fixes the number
of *flags*, so the number of attacks found is
$1000 \times \frac{0.9 \times 0.001}{0.9 \times 0.001 + 0.02 \times 0.999}$. The
engineer spends 1,000 reviews to catch 43 attacks and waste 957 on false alarms.
That is the real cost of a threshold chosen without arithmetic.

(c) New operating point: numerator $= 0.85 \times 0.001 = 0.00085$; denominator $= 0.00085 + 0.01 \times 0.999 = 0.00085 + 0.00999 = 0.01084$; posterior
$\approx 0.0784$, about 7.8%.

Is that better? For the stated goal — surface attacks with a fixed review budget
of 1,000 flags — yes, substantially: the review now surfaces
$1000 \times 0.0784 \approx 78$ attacks instead of 43, at the same human cost.
The false alarm rate halved while detection only fell from 90% to 85%, so the
denominator's dominant term shrank by half. This is the same asymmetry as the
medical test: in a low-base-rate problem the false alarm rate carries almost all
the leverage.

But notice what got worse: 85% detection means 15% of attacks are now missed
outright and never flagged at all, so they cannot be surfaced by review however
many hours you spend. The threshold change trades *review efficiency* against
*coverage*, and the right point depends on which failure is worse. Missing an
attack silently is usually worse than reviewing more false alarms, which is why
in practice you run two detectors at two thresholds rather than tuning one.

(d) **Halving the false alarm rate again, holding detection fixed at 90%** gives
numerator $= 0.0009$, denominator $= 0.0009 + 0.005 \times 0.999 = 0.0009 +
0.004995 = 0.005895$, posterior $\approx 0.1527$, about 15.3% — nearly double (c)
and 3.5× the original. The reason is the same asymmetry: moving the false alarm
rate from 2% to 1% is worth more than moving detection from 90% to 85%, because
the false alarm term is multiplied by a population 999 times larger than the one
the sensitivity multiplies. Eliminating false alarms entirely ($0.00$) would give
a posterior of 1.0.

```python
PREVALENCE = 0.001          # attacks are 0.1% of traffic
REVIEW_BUDGET = 1000        # flagged requests an engineer reviews per hour


def posterior(detection, false_alarm, prevalence=PREVALENCE):
    num = detection * prevalence
    return num / (num + false_alarm * (1 - prevalence))


configs = [
    ("original",             0.90, 0.02),
    ("(c) halved FPR",       0.85, 0.01),
    ("(d) FPR 1%, det 90%",  0.90, 0.01),
    ("(d) FPR 0.5%",         0.90, 0.005),
    ("no false alarms",      0.90, 0.00),
]

print(f"prevalence {PREVALENCE}, review budget {REVIEW_BUDGET}/hour")
print(f"{'config':22} | detection | false alarm | P(attack|flag) | attacks found / 1000")
for name, det, fa in configs:
    p = posterior(det, fa)
    print(f"{name:22} | {det:9.2f} | {fa:11.3f} | {p:13.4f} | "
          f"{REVIEW_BUDGET * p:8.0f}")

p0 = posterior(0.90, 0.02)
p1 = posterior(0.90, 0.005)
print()
print(f"(d) improvement over the original: {p1 / p0:.2f}x the posterior, "
      f"same detection rate")
print(f"attacks silently missed (1 - detection), original vs (d): "
      f"{1 - 0.90:.0%} vs {1 - 0.90:.0%}  <- coverage unchanged in (d)")
print(f"coverage lost in (c): {1 - 0.85:.0%} of attacks never flagged at all")
```

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

[63 — Discrete Random Variables](../part05_probability_statistics/63_discrete_random_variables.md) stops asking
about events and starts naming outcomes: it introduces random variables as
functions on the sample space, probability mass functions, cumulative
distributions, and the Bernoulli and Binomial distributions in full.