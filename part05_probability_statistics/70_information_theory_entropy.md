# 70 — Information Theory and Entropy

**Part**: part05_probability_statistics · **Prerequisites**: 61 · **Time**: 45 min

---

## In Plain Words

Information theory starts with a deceptively simple question: how surprised are
you by an event? The answer it gives is measured in **bits**, and it is just the
negative logarithm of the probability.

That is it. A coin landing heads (p = 0.5) carries exactly one bit, because
−log₂(0.5) = 1. An event with probability 1/1000 carries about ten bits, because
you would need ten binary questions to distinguish it. An event you were certain
about carries zero bits. The log appears because surprisal must add up when
independent things happen — if two independent unlikely things both occur, the
total information is the sum, and only a logarithm converts multiplication into
addition.

From that single definition everything else follows. **Entropy** is the average
surprisal of a whole distribution: how unpredictable the next outcome is on
average. **Cross-entropy** is the average surprisal of your data under your
model's beliefs — and this is the punchline of the whole part: **cross-entropy is
exactly the loss that classification networks are trained to minimise.** The
loss function in your training loop is entropy. **KL divergence** measures how far
one distribution is from another. **Mutual information** measures how much
knowing one variable reduces your uncertainty about another.

## Why Computer Science Cares

- **Every classification loss is cross-entropy.** Binary cross-entropy in logistic
  regression, categorical cross-entropy in PyTorch's `CrossEntropyLoss`,
  `log_loss` in scikit-learn — all the same formula, all derived from entropy.
- **Perplexity**, the standard metric for language models, is the exponential of
  cross-entropy, and it is literally "how many choices the model is effectively
  narrowing it down to per token".
- **Compression.** Huffman coding, gzip, and arithmetic coding all follow from
  the fact that the ideal code length for a symbol of probability p is −log₂ p.
- **KL divergence as a regulariser.** Minimising KL(teacher ‖ student) is exactly
  knowledge distillation, and the temperature used there is a direct entropy
  device.
- **Minimum description length.** Model selection as "pick the model that best
  compresses the data plus the model itself".
- **Interviews.** "Explain what a loss function is doing" is best answered by
  saying it is entropy, which reframes the whole question.

## The Formal Version

**Definition.** The *self-information* (or surprisal) of an event with probability
p > 0 is

    I(x) = −log₂ p   bits

Properties, all immediate:

1. I(x) ≥ 0, with equality only when p = 1.
2. I is decreasing in p: rarer events are more surprising.
3. **Additivity on independent events:** if X and Y are independent, then
   I(X = x, Y = y) = I(X = x) + I(Y = y). This is the reason for the logarithm —
   and since information must combine that way, the log is forced.

**Definition.** The *entropy* of a discrete distribution P is the expected
self-information:

    H(P) = −Σ_x p(x) log₂ p(x)

with the convention 0 log 0 = 0 (needed because an impossible outcome should not
contribute infinite surprise — it just never happens).

**Theorem (bounds).** For a distribution on n outcomes, 0 ≤ H(P) ≤ log₂ n, with
maximum attained exactly by the uniform distribution.

**Explanation.** Each term −p log₂ p is maximised at p = 1/n, so the sum is
maximised when all outcomes are equally likely. Entropy measures *uniformity*, so
a distribution concentrated on one outcome has entropy 0 (completely predictable)
and a uniform one has maximum entropy (completely unpredictable).

**Definition.** For two distributions P and Q on the same alphabet, the
*cross-entropy* is

    H(P, Q) = −Σ_x p(x) log₂ q(x)

**Definition.** The *KL divergence* (relative entropy) is

    D_KL(P ‖ Q) = Σ_x p(x) log₂(p(x)/q(x)) = H(P, Q) − H(P)

**Theorem.** D_KL(P ‖ Q) ≥ 0, with equality if and only if P = Q.

**Proof.** This is Gibbs' inequality. Write D_KL(P‖Q) = −H(P) − Σ p log₂ q, and
note that H(P, Q) ≥ H(P) because the cross-entropy of a distribution under any
other distribution is at least its entropy, with equality only when they agree.
Equivalently, using log t ≤ t − 1 with t = q(x)/p(x): D_KL(P‖Q) =
Σ p log₂(p/q) ≥ Σ p (1 − q/p) log₂ e = (1 − Σ q) log₂ e = 0. ∎

**Explanation.** Gibbs' inequality is exactly the second law of thermodynamics in
disguise: you cannot extract information from a mismatched model. It is also why
KL divergence is the *correct* loss for probabilistic prediction and squared
error is not — squared error does not respect this structure.

**Definition.** The *joint entropy* is H(X, Y) and the *conditional entropy* is

    H(Y | X) = −Σ_x p(x) Σ_y p(y|x) log₂ p(y|x)

**Theorem (chain rule).** H(X, Y) = H(X) + H(Y | X).

**Proof.** Write H(X, Y) = −Σ_x Σ_y p(x,y) log₂ p(x,y) and substitute
p(x,y) = p(x)p(y|x), then split the log into two terms by log(ab) = log a + log b.
Each sum is one of the two entropies. ∎

**Explanation.** The chain rule says total uncertainty equals the uncertainty in X
plus what X leaves you uncertain about. Applied iteratively, entropy over a long
sequence decomposes into the sum of conditional entropies at each step — which is
literally how a language model computes the probability of a sentence.

**Definition.** *Mutual information* is

    I(X; Y) = H(X) − H(X | Y) = H(X) + H(Y) − H(X, Y)   bits

**Explanation.** It is the reduction in uncertainty about X gained by learning Y,
and by the chain rule it is symmetric and non-negative. It is exactly the KL
divergence between the joint distribution and the product of its marginals:
I(X; Y) = D_KL(p(x,y) ‖ p(x)p(y)). **Mutual information is independence
distance** — zero exactly when independent.

### The cross-entropy identity that explains loss functions

**Theorem.** For a single observation from distribution P, minimising the expected
loss

    L(θ) = E_{(x,y) ~ P}[−log₂ q_θ(y|x)]

over the model family {q_θ} yields the model q that equals P — provided P is in
the family. The minimiser of cross-entropy is the maximum likelihood model.

**Explanation.** Cross-entropy is H(P, Q) = H(P) + D_KL(P ‖ Q), and D_KL ≥ 0 with
equality only at Q = P. So H(P) is an additive constant nobody can reduce, and the
entire optimisation problem is "drive the KL divergence to zero". This single
identity is why gradient descent on cross-entropy works, and why the loss never
goes to zero even for a perfect model — there is a floor of H(P), which is the
irreducible randomness in the data.

## Worked Example

### Example A — information content of surprising events

Compute I(x) = −log₂ p for a spread of probabilities:

| p | −log₂ p | interpretation |
| --- | --- | --- |
| 1/2 | 1 bit | a fair coin |
| 1/4 | 2 bits | two coin flips, HH |
| 1/1024 | 10 bits | ten heads in a row |
| 1/1,000,000 | 19.93 bits | one in a million |
| 1e-100 | 332 bits | an essentially impossible event |
| 1 | 0 bits | a certainty |
| 0.9 | 0.152 bits | a biased coin, heads |

The 1e-100 entry is worth pausing on: −log₂(10⁻¹⁰⁰) = 100 × log₂ 10 = 332.19
bits. A vanishingly unlikely event is enormously surprising, and the measure grows
without bound as p → 0. This is why log-loss punishes confident mistakes infinitely:
predicting probability 1e-10 for something that does not happen costs about 33 bits
on that single example, more than an entire typical sentence.

The last row is also important. **Certainty carries no information.** If a
function is always the same, it tells you nothing. Information is precisely the
reduction in uncertainty, which is exactly the mutual information definition
later.

### Example B — entropy of three distributions

**(i) A fair coin.** H = −2 × (0.5 log₂ 0.5) = −2 × (0.5 × (−1)) = **1 bit**.

**(ii) A heavily biased coin**, P(head) = 0.9:
H = −[0.9 log₂ 0.9 + 0.1 log₂ 0.1] = −[0.9(−0.152) + 0.1(−3.322)]
= −[−0.1368 − 0.3322] = **0.469 bits**.

Note how low this is. You can predict a 90/10 coin quite well, so there is under
half a bit of uncertainty per flip. This is the formal statement of "a biased coin
is easier to predict", and it is the reason entropy is not the same as the number
of possible outcomes.

**(iii) A uniform die.** H = −6 × (1/6) log₂(1/6) = log₂ 6 = **2.585 bits**.
This is the maximum possible, achieved because all six outcomes are equally likely.

**(iv) A highly skewed distribution**, P = (0.97, 0.01, 0.01, 0.01) over four
outcomes:
H = −[0.97 log₂ 0.97 + 3 × 0.01 log₂ 0.01]
= −[0.97(−0.0445) + 3 × 0.01(−6.644)]
= −[−0.0432 − 0.1993] = **0.242 bits**.

Despite having four possible outcomes, this is *less* uncertain than the
90/10 coin, because one outcome dominates. **Entropy measures the effective number
of equally likely possibilities**: 2^0.242 = 1.18, versus 2^0.469 = 1.38 for the
biased coin and 2^2.585 = 6 for the die. The quantity 2^H is the cleanest summary —
it is the "effective number of outcomes".

### Example C — the additivity that forces the logarithm

Suppose a system emits one of four symbols with equal probability, but each symbol
is encoded as two binary bits. Ask: how much information is in one symbol?

The answer must be 2 bits, because one symbol rules out three of the four
possibilities and each bit halves the space: log₂ 4 = 2.

Now confirm the additivity property directly. The probability of the pair
(bits = "01") is 1/4, so

    I(bits="01") = −log₂(1/4) = 2 bits

and this equals I(first bit) + I(second bit) = 1 + 1, because the two bits are
independent. **Additivity on independent events holds for logarithms and fails
for everything else.** The natural log also works: −ln(0.01) = 4.605 and
−ln(0.1) + −ln(0.1) = 2.303 + 2.303 = 4.605. But the square root gives 0.1
against 0.316 + 0.316 = 0.632, and 1 − p gives 0.99 against 1.8.

So any logarithm works, and the choice of base is pure convention: base 2 makes
I(1/2) = 1, which is why we speak of **bits**, while the natural log gives
**nats** (divide bits by ln 2 ≈ 0.693 to convert). What is *not* conventional is
that a logarithm is required at all — additivity forces it.

### Example D — cross-entropy as a loss function

A model classifies images into 10 classes. Suppose the true label is class 3 and
the model assigns probability 0.7 to class 3.

**Per-example cross-entropy** = −log₂ 0.7 = **0.5146 bits**.

Now suppose the model is only 0.3 confident about the true class:
−log₂ 0.3 = **1.737 bits** — 3.4× the loss.

**KL divergence between the truth and the model.** The truth is a point mass at
class 3, so

    D_KL(P ‖ Q) = −log₂ q(3) = 0.5146 bits

(the terms p log p/q vanish for all other classes). **The cross-entropy is
identical**, because H(P) = 0 for a one-hot label. This is a special case worth
knowing: for one-hot labels, cross-entropy loss *is* the KL divergence.

**Across a dataset**, the average cross-entropy is the loss every framework prints,
and the fundamental identity H(P, Q) = H(P) + D_KL(P ‖ Q) splits it into an
irreducible part H(P) and a reducible part D_KL(P ‖ Q). Take a label distribution
of 60% class 1 and 40% class 3: H(P) = 0.9710 bits. A model that knows nothing
beyond those marginals, and always predicts them, achieves exactly 0.9710 bits of
loss — all of it label entropy, none of it model error. No amount of training
reduces the loss below H(P), because that remainder is not model error at all, it
is randomness in the labels. That is why loss curves plateau, and why comparing
your loss against 0 is meaningless — compare it against H(P).

**Perplexity** converts this into something more readable:

    perplexity = 2^(average cross-entropy)

An average cross-entropy of 0.5146 bits gives perplexity 2^0.5146 = 1.43: the
model is effectively narrowing the choice down to about 1.4 candidates. A
cross-entropy of 3.32 bits (chance on 10 classes) gives perplexity 10, meaning the
model has learned nothing at all. **Perplexity is literally an effective branching
factor**, which is why it is the natural metric for language models.

## Runnable Code

### Information content and surprise

```python
from math import log2, isfinite


def surprisal(p):
    """Self-information in bits. p == 0 is treated as infinite surprise."""
    if p <= 0:
        return float("inf")
    # p == 1 gives log2(1) == 0, whose negation is -0.0; normalise it to 0.0
    # so the printed table does not show a misleading negative zero.
    return -log2(p) + 0.0


print("information content of an event")
print(f"{'probability':>14} {'-log2(p)':>12} {'meaning':>28}")
for p in (1.0, 0.9, 0.5, 0.25, 1 / 1024, 1e-6, 1e-10, 1e-100):
    i = surprisal(p)
    label = {1.0: "certainty, no information",
             0.9: "biased coin",
             0.5: "fair coin",
             0.25: "two flips: HH",
             }.get(p, "")
    print(f"{p:14.3e} {i:12.4f} {label:>28}")

print()
print("p=1e-100 costs 332 bits on a SINGLE observation --")
print("more surprisal than an entire typical sentence.")
print()

# Additivity: the property that forces the logarithm.
print("additivity on independent events (the reason for the log)")
p1 = p2 = 0.1
joint = p1 * p2
print(f"  P(a)={p1}, P(b)={p2}, independent -> P(a and b)={joint}")
print(f"  I(a and b) = {surprisal(joint):.6f} bits")
print(f"  I(a)+I(b)  = {surprisal(p1) + surprisal(p2):.6f} bits")
print(f"  equal: {abs(surprisal(joint) - (surprisal(p1) + surprisal(p2))) < 1e-12}")
print()
print("  only a logarithm satisfies this. Other candidates fail:")
from math import log as natural_log

CANDIDATES = [
    ("log base 2", lambda p: -log2(p)),
    ("natural log", lambda p: -natural_log(p)),
    ("square root", lambda p: p ** 0.5),
    ("linear 1-p", lambda p: 1 - p),
    ("reciprocal", lambda p: 1 / p),
]
print(f"    {'candidate':12} {'I(0.01)':>10} {'I(0.1)+I(0.1)':>16}"
      f"  additive?")
for name, fn in CANDIDATES:
    joint_val = fn(joint)
    split = fn(p1) + fn(p2)
    ok = abs(joint_val - split) < 1e-9
    print(f"    {name:12} {joint_val:10.6f} {split:16.6f}"
          f"  {'yes' if ok else 'NO'}")
print()
print("Every logarithm is additive (base only rescales); nothing else is.")
print("Base 2 is chosen so that I(1/2) = 1, which makes bits the unit.")
print("The base would otherwise be arbitrary: nats uses the natural log and")
print("is the same information in different units (divide bits by ln 2).")
```

### Entropy of distributions, and the effective number of outcomes

```python
from math import log2


def entropy(dist, base=2.0):
    """Shannon entropy. 0*log(0) is taken as 0, as is conventional."""
    total = 0.0
    for p in dist.values():
        if p > 0:
            total -= p * log2(p)
    return total


def cross_entropy(p, q):
    """H(P, Q) = -sum p log2 q.  Infinite if P puts mass where Q does not."""
    total = 0.0
    for value, pv in p.items():
        qv = q[value]
        if pv == 0:
            continue
        if qv == 0:
            return float("inf")
        total -= pv * log2(qv)
    return total


def kl_divergence(p, q):
    """D_KL(P||Q) = H(P,Q) - H(P).  Always >= 0."""
    ce = cross_entropy(p, q)
    if ce == float("inf"):
        return ce
    return ce - entropy(p)


CASES = [
    ("fair coin", {"H": 0.5, "T": 0.5}),
    ("biased coin 90/10", {"H": 0.9, "T": 0.1}),
    ("uniform die", {str(i): 1 / 6 for i in range(1, 7)}),
    ("very skewed (0.97,...)", {"a": 0.97, "b": 0.01, "c": 0.01, "d": 0.01}),
    ("uniform over 4", {k: 0.25 for k in "abcd"}),
    ("uniform over 16", {format(i, "x"): 1 / 16 for i in range(16)}),
    ("point mass", {"a": 1.0}),
]

print(f"{'distribution':24} {'H (bits)':>10} {'2^H':>8}  {'#outcomes':>10}")
for name, dist in CASES:
    h = entropy(dist)
    print(f"{name:24} {h:10.4f} {2 ** h:8.3f}  {len(dist):10d}")

print()
print("2^H is the EFFECTIVE number of equally likely outcomes.")
print("It is the best summary of how unpredictable the distribution is:")
print(f"  the die really has 6 options (H=log2 6={log2(6):.4f}, 2^H=6.000)")
print(f"  but the 0.97-heavy distribution has 4 options yet only")
print(f"    2^H = {2 ** entropy(CASES[3][1]):.3f} effective ones.")
print()

# Entropy is maximised by the uniform distribution.
print("H is maximised exactly by the uniform distribution:")
n = 8
uniform = log2(n)
print(f"  uniform over {n}: H = log2({n}) = {uniform:.4f}")
for bias in (0.2, 0.35, 0.5, 0.7, 0.9):
    dist = {f"a{i}": bias if i == 0 else (1 - bias) / (n - 1)
            for i in range(n)}
    h = entropy(dist)
    print(f"  P(first)={bias:.2f}, rest split: H = {h:.4f}  "
          f"{'<-- max' if abs(h - uniform) < 1e-9 else ''}")
print(f"  no distribution exceeds {uniform:.4f} on {n} outcomes.")
```

### KL divergence, and its two key properties

```python
from math import log2


def H(dist):
    return -sum(p * log2(p) for p in dist.values() if p > 0)


def CE(p, q):
    total = 0.0
    for key, pv in p.items():
        if pv == 0:
            continue
        if q.get(key, 0.0) == 0:
            return float("inf")
        total -= pv * log2(q[key])
    return total


def KL(p, q):
    ce = CE(p, q)
    return float("inf") if ce == float("inf") else ce - H(p)


TRUE = {"cat": 0.5, "dog": 0.3, "bird": 0.2}

print("D_KL measures how far Q is from the true distribution P.")
print(f"P = {TRUE}, H(P) = {H(TRUE):.4f} bits\n")

models = [
    ("perfect", dict(TRUE)),
    ("close", {"cat": 0.45, "dog": 0.33, "bird": 0.22}),
    ("confident but wrong", {"cat": 0.1, "dog": 0.1, "bird": 0.8}),
    ("uniform", {"cat": 1 / 3, "dog": 1 / 3, "bird": 1 / 3}),
    ("inverted", {"cat": 0.1, "dog": 0.2, "bird": 0.7}),
]

print(f"{'model':22} {'H(P,Q)':>9} {'H(P)':>8} {'D_KL':>9}  note")
for name, q in models:
    ce = CE(TRUE, q)
    kl = KL(TRUE, q)
    note = "zero iff P == Q" if kl < 1e-12 else ""
    print(f"{name:22} {ce:9.4f} {H(TRUE):8.4f} {kl:9.4f}  {note}")

print()
print("Two facts, visible above:")
print(" 1. D_KL(P||Q) >= 0 always, with equality only at Q = P (Gibbs).")
print(" 2. KL divergence is NOT symmetric:")
q_inv = {"cat": 0.1, "dog": 0.2, "bird": 0.7}
print(f"    D_KL(P||Q_inv) = {KL(TRUE, q_inv):.4f}")
print(f"    D_KL(Q_inv||P) = "
      f"{KL(q_inv, TRUE):.4f}   <- different! Order matters.")
print()

# KL is infinite when Q rules out something P allows.
print("If Q assigns zero probability to an event P considers possible:")
bad = {"cat": 0.5, "dog": 0.5}   # 'bird' missing entirely
print(f"  CE = {CE(TRUE, bad)}, KL = {KL(TRUE, bad)}")
print("  Infinite: the model made a prediction that is impossible,")
print("  and log-loss punishes that without bound. This is why we")
print("  never let a model output a hard zero.")
print()

# KL between a product of marginals and the true joint == mutual information.
print("KL( joint || product of marginals ) is mutual information:")
joint = {"00": 0.30, "01": 0.20, "10": 0.20, "11": 0.30}
mx = {"0": joint["00"] + joint["01"], "1": joint["10"] + joint["11"]}
my = {"0": joint["00"] + joint["10"], "1": joint["01"] + joint["11"]}
product = {a + b: mx[a] * my[b] for a in "01" for b in "01"}
mi = KL(joint, product)
hx = H(mx)
hy = H(my)
hxy = H(joint)
print(f"  H(X)={hx:.4f}  H(Y)={hy:.4f}  H(X,Y)={hxy:.4f}")
print(f"  I(X;Y) = H(X)+H(Y)-H(X,Y) = {hx + hy - hxy:.4f} bits")
print(f"  I(X;Y) = KL(joint || product)  = {mi:.4f} bits")
print(f"  agree: {abs(mi - (hx + hy - hxy)) < 1e-12}")
print()
print("Now a GENUINELY INDEPENDENT pair, where mutual information must be 0:")
# Marginals P(X=0)=0.7, P(Y=0)=0.6, factorised exactly.
px = {"0": 0.7, "1": 0.3}
py = {"0": 0.6, "1": 0.4}
indep = {a + b: px[a] * py[b] for a in "01" for b in "01"}
mx2 = {"0": indep["00"] + indep["01"], "1": indep["10"] + indep["11"]}
my2 = {"0": indep["00"] + indep["10"], "1": indep["01"] + indep["11"]}
prod2 = {a + b: mx2[a] * my2[b] for a in "01" for b in "01"}
print(f"  product of marginals == the joint? "
      f"{all(abs(prod2[k] - v) < 1e-12 for k, v in indep.items())}")
print(f"  H(X)={H(mx2):.4f}  H(Y)={H(my2):.4f}  H(X,Y)={H(indep):.4f}")
print(f"  I(X;Y) = H(X)+H(Y)-H(X,Y) = {H(mx2) + H(my2) - H(indep):.2e} bits")
print(f"  KL(indep || product)        = {KL(indep, prod2):.2e} bits")
print()
print("So for DISCRETE variables, I(X;Y) = 0 if and only if X and Y are")
print("independent. That makes mutual information a COMPLETE dependence")
print("test, unlike correlation, which only detects LINEAR dependence and")
print("misses things like Y = X^2 entirely.")
```

### Cross-entropy as a loss function, and perplexity

```python
from math import log2, exp


def cross_entropy_loss(probs, label):
    """The loss every classification model minimises, in bits per example."""
    return -log2(probs[label])


def perplexity(bits):
    """Perplexity = 2^(average cross-entropy)."""
    return 2 ** bits


print("Per-example cross-entropy for a 10-class problem.")
print(f"{'model confidence in true label':>30} {'loss (bits)':>12} {'perplexity':>11}")
for conf in (0.9, 0.7, 0.5, 0.3, 0.1, 0.01, 0.001):
    loss = cross_entropy_loss({i: conf for i in range(10)}, 3)
    print(f"{conf:>30} {loss:12.4f} {perplexity(loss):11.3f}")
print()
print("Confidence of 0.01 costs 6.64 bits -- a PERFECTLY CONFIDENT")
print("mistake costs 9.97 bits, more than three such mistakes combined.")
print()

# For one-hot labels, cross-entropy IS the KL divergence.
print("For a one-hot label, cross-entropy == KL divergence exactly:")
q = [0.05, 0.9, 0.05]
TRUE_LABEL = 1
ce = -log2(q[TRUE_LABEL])
# KL(one-hot || q) = sum_k p(k) log2(p(k)/q(k)). Only the true label has p = 1;
# the other terms are 0 * log2(0/q) and must be skipped rather than evaluated,
# because log2(0) is undefined.
kl = 1.0 * log2(1.0 / q[TRUE_LABEL])
print(f"  cross-entropy = {ce:.6f} bits")
print(f"  KL(one-hot || model) = {kl:.6f} bits")
print(f"  equal: {abs(ce - kl) < 1e-12}   (because H(one-hot) = 0)")
print()

# The loss floor: a perfect model still pays the label entropy.
print("The loss has a floor at the label entropy H(P):")
label_entropy = -(0.6 * log2(0.6) + 0.4 * log2(0.4))
print(f"  label distribution: 60% class 1, 40% class 3")
print(f"  H(P) = {label_entropy:.4f} bits  <- the irreducible floor")
print()
print("  A model that knows the label DISTRIBUTION but not the individual")
print("  label cannot do better than this. Its expected loss is exactly H(P):")
for label, weight in ((1, 0.6), (3, 0.4)):
    q = {1: 0.6, 3: 0.4}          # the model always predicts the marginals
    print(f"    label={label}: weight {weight}, -log2({q[label]}) = "
          f"{-log2(q[label]):.4f}, contribution "
          f"{weight * -log2(q[label]):.4f}")
best = sum(w * -log2({1: 0.6, 3: 0.4}[l]) for l, w in ((1, 0.6), (3, 0.4)))
print(f"  total = {best:.4f} bits = H(P) exactly.")
print()
print("  Only a model with perfect knowledge of each label could push the")
print("  loss lower, and that is impossible when the labels are drawn from a")
print("  distribution -- an outcome always carries SOME surprisal. That is")
print("  why accuracy saturates below 100% on real tasks, and why the loss")
print("  curve plateaus rather than reaching zero.")
print()

# Perplexity interpretation.
print("Perplexity as an effective branching factor:")
print(f"{'cross-entropy':>14} {'perplexity':>11}  meaning")
for bits, meaning in ((0.0, "certain"),
                      (1.0, "effectively 2 choices"),
                      (2.585, "log2 6 = a fair 6-sided die"),
                      (3.322, "log2 10 = chance on 10 classes"),
                      (6.644, "log2 100 = chance on 100 classes")):
    print(f"{bits:14.3f} {perplexity(bits):11.3f}  {meaning}")
```

### The chain rule, applied to a real model

```python
from math import log2


def entropy(dist):
    """Shannon entropy in bits; keys are values, values are probabilities."""
    return -sum(p * log2(p) for p in dist.values() if p > 0)


# A joint distribution over (first letter, next-is-vowel).
#   letter -> P(vowel), P(other), with the letter's own marginal.
LETTERS = ["c", "t", "f", "s"]
MARGINAL = {"c": 0.25, "t": 0.25, "f": 0.20, "s": 0.30}
P_VOWEL = {"c": 0.40, "t": 0.20, "f": 0.10, "s": 0.07}

# Build the joint from (marginal, conditional) WITHOUT shadowing any variables.
joint = {}
for letter in LETTERS:
    p_x = MARGINAL[letter]
    p_v = P_VOWEL[letter]
    joint[(letter, True)] = p_x * p_v
    joint[(letter, False)] = p_x * (1 - p_v)

h_x = entropy(MARGINAL)
p_next_vowel = sum(joint[(l, True)] for l in LETTERS)
p_next_other = sum(joint[(l, False)] for l in LETTERS)
h_y = entropy({True: p_next_vowel, False: p_next_other})
h_xy = entropy(joint)


def conditional_entropy(target_index):
    """H(Y|X) = sum_x P(x) * H(Y | x), weighting each conditional by P(x)."""
    total = 0.0
    for letter in LETTERS:
        p_x = MARGINAL[letter]
        within = {True: joint[(letter, True)] / p_x,
                  False: joint[(letter, False)] / p_x}
        total += p_x * entropy(within)
    return total


h_y_given_x = conditional_entropy(1)

print(f"H(X)      = {h_x:.4f} bits  (which consonant starts the token)")
print(f"H(Y)      = {h_y:.4f} bits  (next char is a vowel, or not)")
print(f"H(X,Y)    = {h_xy:.4f} bits  (joint)")
print(f"H(Y|X)    = {h_y_given_x:.4f} bits")
print()
print(f"chain rule: H(X) + H(Y|X) = {h_x:.4f} + {h_y_given_x:.4f} = "
      f"{h_x + h_y_given_x:.4f}")
print(f"            H(X,Y)        = {h_xy:.4f}")
print(f"they match: {abs(h_x + h_y_given_x - h_xy) < 1e-12}")
print()
# H(B) + H(A|B) must give the same answer: the chain rule is symmetric in order.
h_x_given_y = 0.0
for is_vowel in (True, False):
    mass = sum(joint[(l, is_vowel)] for l in LETTERS)
    within = {l: joint[(l, is_vowel)] / mass for l in LETTERS}
    h_x_given_y += mass * entropy(within)
print(f"symmetric check: H(Y) + H(X|Y) = {h_y:.4f} + {h_x_given_y:.4f} = "
      f"{h_y + h_x_given_y:.4f}")
print(f"also matches:   {abs(h_y + h_x_given_y - h_xy) < 1e-12}")
print()

mi = h_x + h_y - h_xy
print(f"mutual information I(X;Y) = H(X)+H(Y)-H(X,Y) = {mi:.4f} bits")
print(f"Knowing the letter cuts uncertainty about the next char from "
      f"{h_y:.4f} to")
print(f"{h_y_given_x:.4f} bits -- a saving of {mi:.4f} bits "
      f"({mi / h_y * 100:.1f}%).")
print()

# Mutual information == KL(joint || product of marginals).
product = {(l, v): MARGINAL[l] * (p_next_vowel if v else p_next_other)
           for l in LETTERS for v in (True, False)}
kl_independence = sum(p * log2(p / product[(l, v)])
                      for (l, v), p in joint.items() if p > 0)
print(f"D_KL(joint || product of marginals) = {kl_independence:.4f} bits")
print(f"which equals the mutual information: "
      f"{abs(kl_independence - mi) < 1e-12}")
print()
print("I(X;Y) = 0 means INDEPENDENT, and mutual information detects")
print("dependence that correlation cannot -- it is a complete test for")
print("discrete distributions.")
print()

# The chain rule in log-space: multiply probabilities, or sum logs.
log_p_sentence = 0.0
p_sentence = 1.0
for letter in LETTERS:
    p_sentence *= MARGINAL[letter] * P_VOWEL[letter]
    log_p_sentence += log2(MARGINAL[letter]) + log2(P_VOWEL[letter])

print(f"P(one draw of letter + vowel-ness) by multiplying = {p_sentence:.6e}")
print(f"                                 by summing logs = "
      f"{2 ** log_p_sentence:.6e}")
print(f"-log2 P = {-log_p_sentence:.4f} bits of cross-entropy for this token")
print()
print("For a 1,000-token sequence the product underflows to 0.0 in float64,")
print("but the sum of log-probabilities stays perfectly finite. That is the")
print("entire reason models are trained and reported in log-space.")
```

## Common Mistakes

**Mistake 1 — reading −log₂ p as the probability of the event.**
Wrong: "the event has probability 1/1024, which is 10 bits, so it's 10% likely."
Right: 10 bits is a measure of *surprise*, not probability. The probability is
0.00098. Bits and probabilities are related by a logarithm, and confusing them
produces nonsense.

**Mistake 2 — thinking KL divergence is symmetric.**
It is not. D_KL(P‖Q) ≠ D_KL(Q‖P) in general, and the asymmetry is essential:
KL(P‖Q) punishes Q for missing mass that P has (infinite penalty), while
KL(Q‖P) punishes Q for putting mass where P does not. This is exactly why
generative models use KL(P‖Q) with P the data — it forces Q to cover P's support.
Running the code above on the "inverted" model shows the asymmetry concretely.

**Mistake 3 — expecting the loss to reach zero.**
The floor is H(P), the entropy of the labels. On a task with genuine label noise,
perfect prediction still costs positive loss. Teams reading a loss curve that
plateau at 0.6 and concluding "the model is broken" are usually seeing the
irreducible entropy. Compare against H(P), not against zero.

**Mistake 4 — computing probability by multiplying many small probabilities.**
For a 1,000-token sequence with per-token probability ~0.1, the product is 10⁻¹⁰⁰⁰
and underflows any float. This is why language models work in log-space:
log P = Σ log pᵢ, which never overflows. Any code that multiplies probabilities
across a long sequence will silently return 0.

**Mistake 5 — treating entropy as "amount of data" or "complexity of the
distribution" in general.**
Entropy is average surprisal of *one draw* from the distribution. It says nothing
directly about how compressible a specific sample is. A distribution with high
entropy can occasionally emit a highly predictable sequence by chance; and a
low-entropy distribution is still uncertain in a way that matters for a specific
observation. Use entropy for expectations over the distribution, not for
describing one sample.

## Exercises and Solutions

**[ ] Exercise 1 — the basics, computed three ways.** Let P = (0.4, 0.4, 0.1,
0.1) over four outcomes.

(a) Compute the self-information of each outcome. (b) Compute H(P). (c) Compute
the effective number of outcomes 2^H. (d) Compute H(P, U) and H(P, V) for two
different models and hence their KL divergences, verifying each is ≥ 0.

<details>
<summary>Solution</summary>

(a) I = −log₂ p:

- I(0.4) = −log₂(0.4) = 1.3219 bits (twice)
- I(0.1) = −log₂(0.1) = 3.3219 bits (twice)

(b) H(P) = −[0.4(1.3219) + 0.4(1.3219) + 0.1(3.3219) + 0.1(3.3219)]
= −[0.52876 + 0.52876 + 0.33219 + 0.33219] = −1.7219 bits.

Check by the shortcut form: −Σp log₂ p = −[0.8 log₂ 0.4 + 0.2 log₂ 0.1]
= −[0.8(−1.3219) + 0.2(−3.3219)] = 1.7219 ✓

(c) 2^H = 2^1.7219 = **3.290**. So despite four possible outcomes, the
distribution behaves like only 3.29 equally likely ones.

(d) Take U = the uniform model (0.25 each) and V = (0.5, 0.3, 0.1, 0.1).

H(P, U) = −[0.4 log₂ 0.25 + 0.4 log₂ 0.25 + 0.1 log₂ 0.25 + 0.1 log₂ 0.25]
= −log₂ 0.25 = **2.0000 bits**.

D_KL(P‖U) = 2.0000 − 1.7219 = **0.2781 bits**.

H(P, V) = −[0.4 log₂ 0.5 + 0.4 log₂ 0.3 + 0.1 log₂ 0.1 + 0.1 log₂ 0.1]
= −[0.4(−1) + 0.4(−1.7370) + 0.1(−3.3219) + 0.1(−3.3219)]
= −[−0.4 − 0.69479 − 0.33219 − 0.33219] = **1.75917 bits**.

D_KL(P‖V) = 1.75917 − 1.72193 = **0.03724 bits**.

Both KL values are positive, as Gibbs' inequality requires. Note how much better
V is than U: V is a genuinely informed model (it happens to be a mixture of the
true P with something else), while U ignores the data entirely. The 0.037 bits of
KL(P‖V) says V is a good fit — consistent with KL being small when the model is
close to the truth.

```python
from math import log2

P = {0: 0.4, 1: 0.4, 2: 0.1, 3: 0.1}
U = {0: 0.25, 1: 0.25, 2: 0.25, 3: 0.25}
V = {0: 0.5, 1: 0.3, 2: 0.1, 3: 0.1}


def H(dist):
    return -sum(p * log2(p) for p in dist.values() if p > 0)


def CE(p, q):
    return -sum(pv * log2(q[k]) for k, pv in p.items() if pv > 0)


def KL(p, q):
    return CE(p, q) - H(p)


print("(a) self-information")
for k, p in P.items():
    print(f"    outcome {k}: p={p:.2f}, -log2(p)={-log2(p):.4f} bits")

h = H(P)
print(f"(b) H(P) = {h:.6f} bits")
print(f"    shortcut -[0.8*log2(0.4) + 0.2*log2(0.1)] = "
      f"{-(0.8 * log2(0.4) + 0.2 * log2(0.1)):.6f}")
print(f"(c) 2^H = {2 ** h:.4f} effective outcomes (there are 4 real ones)")

for name, Q in (("uniform U", U), ("informed V", V)):
    ce, kl = CE(P, Q), KL(P, Q)
    print(f"(d) {name:12}: H(P,Q)={ce:.6f}  KL(P||Q)={kl:.6f}  "
          f"non-negative: {kl >= -1e-12}")

print()
print("Gibbs' inequality holds for both models, and V is a far better")
print("model than U (KL 0.037 bits vs 0.278 bits).")
```

</details>

**[ ] Exercise 2 — the chain rule on a real distribution.** Consider two binary
variables A and B with the joint table

| | B=0 | B=1 |
| --- | --- | --- |
| A=0 | 0.30 | 0.05 |
| A=1 | 0.15 | 0.50 |

(a) Compute H(A), H(B), and H(A,B). (b) Verify the chain rule H(A,B) = H(A) +
H(B|A) = H(B) + H(A|B). (c) Compute the mutual information. (d) Is I ≥ 0 always?
Verify on this table and construct a case where mutual information is 0 despite
dependence. (e) Use KL divergence to confirm that D_KL(joint ‖ product of
marginals) equals the mutual information.

<details>
<summary>Solution</summary>

The joint distribution: P(0,0)=0.30, P(0,1)=0.05, P(1,0)=0.15, P(1,1)=0.50.

(a) Marginals. P(A=0) = 0.35, P(A=1) = 0.65; P(B=0) = 0.45, P(B=1) = 0.55.

    H(A) = −[0.35 log₂ 0.35 + 0.65 log₂ 0.65] = **0.934068 bits**
    H(B) = −[0.45 log₂ 0.45 + 0.55 log₂ 0.55] = **0.992774 bits**
    H(A,B) = −[0.30 log₂ 0.30 + 0.05 log₂ 0.05 + 0.15 log₂ 0.15 + 0.50 log₂ 0.50]
           = **1.647731 bits**

(b) Chain rule. The step worth being careful about is that the conditional
entropies must be **weighted by P(A=a)** — an easy place to lose a factor.

    H(B|A=0) = 0.591673   (from the two cells of column A=0)
    H(B|A=1) = 0.779350   (from the two cells of column A=1)
    H(B|A)   = 0.35(0.591673) + 0.65(0.779350) = **0.713663**

    H(A) + H(B|A) = 0.934068 + 0.713663 = **1.647731** = H(A,B) ✓

By symmetry, H(B) + H(A|B) = 1.647731 as well. The chain rule holds in both
orders, which is the statement that joint entropy is symmetric.

(c) Mutual information:

    I(A;B) = H(A) + H(B) − H(A,B) = 0.934068 + 0.992774 − 1.647731
           = **0.279112 bits**

The same value comes from H(A) − H(A|B), confirming symmetry of I.

(d) Mutual information is always ≥ 0, because conditioning cannot *increase*
uncertainty: H(A|B) ≤ H(A). Here I = 0.279 bits, well above zero, so the
variables are strongly dependent.

On the subtler question — can dependence give zero mutual information? For
**discrete** variables, no: I(A;B) = 0 holds if and only if the joint equals the
product of the marginals, which is precisely the definition of independence. And
the code confirms this table is genuinely dependent: the product of marginals
does **not** reproduce the joint.

The "dependent but zero correlation" case people have in mind does exist, but it
shows up as zero *correlation*, not zero mutual information — for example
Y = X² with X symmetric, where ρ = 0 while mutual information is actually
**infinite** (any non-zero interval determines X up to sign). Mutual information is
strictly more sensitive than correlation, not less.

(e) The product of marginals is (0.1575, 0.1925, 0.2925, 0.3575) for the four
cells (0,0), (0,1), (1,0), (1,1). Then

    D_KL(joint ‖ product) = **0.279112 bits**

exactly equal to the mutual information from (c). This is a general identity:
**mutual information is the KL divergence between the true joint distribution
and the independence assumption.**

```python
from math import log2

JOINT = {(0, 0): 0.30, (0, 1): 0.05, (1, 0): 0.15, (1, 1): 0.50}


def H(dist):
    return -sum(p * log2(p) for p in dist.values() if p > 0)


def KL(p, q):
    return sum(pv * log2(pv / q[k]) for k, pv in p.items() if pv > 0)


marg_a = {0: JOINT[(0, 0)] + JOINT[(0, 1)],
          1: JOINT[(1, 0)] + JOINT[(1, 1)]}
marg_b = {0: JOINT[(0, 0)] + JOINT[(1, 0)],
          1: JOINT[(0, 1)] + JOINT[(1, 1)]}
h_ab = H(JOINT)

print("(a)")
print(f"    P(A=0)={marg_a[0]:.2f}  P(A=1)={marg_a[1]:.2f}   "
      f"P(B=0)={marg_b[0]:.2f}  P(B=1)={marg_b[1]:.2f}")
print(f"    H(A)   = {H(marg_a):.6f} bits")
print(f"    H(B)   = {H(marg_b):.6f} bits")
print(f"    H(A,B) = {h_ab:.6f} bits")

print()
print("(b) chain rule, both orders")
for a in (0, 1):
    within = {b: JOINT[(a, b)] / marg_a[a] for b in (0, 1)}
    print(f"    H(B|A={a}) = {H(within):.6f}  "
          f"(weighted by P(A={a})={marg_a[a]:.2f})")
h_b_given_a = sum(marg_a[a] * H({b: JOINT[(a, b)] / marg_a[a] for b in (0, 1)})
                  for a in (0, 1))
h_a_given_b = sum(marg_b[b] * H({a: JOINT[(a, b)] / marg_b[b] for a in (0, 1)})
                  for b in (0, 1))
print(f"    H(B|A) = {h_b_given_a:.6f}")
print(f"    H(A) + H(B|A) = {H(marg_a) + h_b_given_a:.6f} == H(A,B)? "
      f"{abs(H(marg_a) + h_b_given_a - h_ab) < 1e-12}")
print(f"    H(B) + H(A|B) = {H(marg_b) + h_a_given_b:.6f} == H(A,B)? "
      f"{abs(H(marg_b) + h_a_given_b - h_ab) < 1e-12}")

mi_ab = H(marg_a) + H(marg_b) - h_ab
mi_ba = H(marg_a) - h_a_given_b
print()
print(f"(c) I(A;B) = H(A)+H(B)-H(A,B) = {mi_ab:.6f} bits")
print(f"    I(A;B) = H(A)-H(A|B)      = {mi_ba:.6f} bits")
print(f"    symmetric: {abs(mi_ab - mi_ba) < 1e-12}")

product = {(a, b): marg_a[a] * marg_b[b] for a in (0, 1) for b in (0, 1)}
print()
print(f"(d) I >= 0: {mi_ab >= 0}")
print(f"    product of marginals == joint? "
      f"{all(abs(product[k] - v) < 1e-12 for k, v in JOINT.items())}"
      "   -> so the variables really are dependent")

print()
kl = KL(JOINT, product)
print(f"(e) D_KL(joint || product of marginals) = {kl:.6f} bits")
print(f"    equals the mutual information: {abs(kl - mi_ab) < 1e-12}")
```

The identity in (e) is worth memorising: **mutual information is the KL divergence
between the true joint distribution and the independence assumption.** Measuring how
badly independence fails is exactly measuring how much the two variables tell each
other.
between the true joint distribution and the independence assumption.** Measuring
how badly independence fails is exactly measuring how much the two variables tell
each other.

</details>

**[ ] Exercise 3 — Challenge: implement cross-entropy training and watch it
work.** A two-class problem. The true conditional distribution is
p(vowel | first letter) as follows: after "c" it is 0.4, after "t" 0.2, after "f"
0.1, after "s" 0.07. Marginal of the first letter: c=0.25, t=0.25, f=0.20,
s=0.30.

(a) Compute the model's cross-entropy per token under these exact
probabilities — this is the loss floor. (b) Fit a single-parameter model
q(vowel | letter) = sigmoid(θ + w·log p(letter)) by gradient descent on
cross-entropy, and compare its loss to the floor. (c) Compute perplexity for both.
(d) Compute the KL divergence between the fitted model and the true conditional
distributions. (e) Explain why the fitted model's KL is positive but its
cross-entropy is only slightly worse than the floor.

<details>
<summary>Solution</summary>

(a) The loss floor is the conditional entropy of the true distributions:

    H = −Σ_x p(x)[ p₁(x) log₂ p₁(x) + (1−p₁(x)) log₂(1−p₁(x)) ]

with p₁ = (0.4, 0.2, 0.1, 0.07) and p(x) = (0.25, 0.25, 0.20, 0.30).

Per-letter binary entropies:
- p = 0.40: H = 0.970951 bits
- p = 0.20: H = 0.721928 bits
- p = 0.10: H = 0.468996 bits
- p = 0.07: H = 0.365816 bits (approximately)

Weighted: 0.25(0.970951) + 0.25(0.721928) + 0.20(0.468996) + 0.30(0.365816)
= 0.242738 + 0.180482 + 0.093799 + 0.109745 = **0.626764 bits** per token.

(b) The fitted parameters are θ = −2.519 and w = −0.540. The **negative w** is
the revealing part. The family was specified as "probability rises with the log of
the marginal", but the true conditional probabilities move the *other* way for the
commonest letters: the most frequent letter "s" (marginal 0.30) has the lowest
vowel rate (0.07), while "c" (marginal 0.25) has the highest (0.40).

The constraint therefore fights the data, and gradient descent responds by pushing
w negative and compressing everything toward the mean. The fitted model predicts a
narrow band from 0.171 to 0.220 where the truth ranges from 0.07 to 0.40 — it has
learned the average and discarded the per-letter detail.

The cost is 0.075240 bits per token, a **12.0% increase** over the floor. That is
what model misspecification actually looks like: not a crash, not a NaN, just a
plateau slightly higher than it should be.

(c) Perplexity: the floor gives 2^0.626796 = **1.5441**, the fitted model gives
2^0.702036 = **1.6268**. Both say the model is narrowing a binary choice down to
about one-and-a-half options per token; the gap is the whole cost of the
misspecification.

(d) KL(P‖Q) per token = H(P,Q) − H(P) = fitted loss − floor = **0.075240 bits**,
confirmed by direct computation. That it is *exactly* the number from (b) is not a
coincidence — it is the identity KL = CE − H(P) for the same two distributions.

(e) The two quantities measure different things and both are needed.
**Cross-entropy measures how well you predict; KL measures how far your model is
from the truth.** They differ by H(P), the label entropy, which is identical for
every model and therefore invisible to the optimiser.

The gap between them is diagnostic:

- High cross-entropy, **low** KL: the model is nearly right but the task is
  intrinsically noisy. Good model, best possible performance; the remaining loss is
  not worth attacking.
- **Low** cross-entropy, high KL: the model found a shortcut that works on this
  data without modelling the true process. This is the pattern that later shows up
  as a train/test gap.

Here cross-entropy 0.702 with KL 0.075 against a floor of 0.627 is the first
pattern: the model is close, and task entropy explains the bulk of the loss.

```python
from math import log2, exp

MARGINAL = {"c": 0.25, "t": 0.25, "f": 0.20, "s": 0.30}
TRUE_P1 = {"c": 0.40, "t": 0.20, "f": 0.10, "s": 0.07}   # P(vowel | letter)


def binary_entropy(p):
    if p <= 0 or p >= 1:
        return 0.0
    return -(p * log2(p) + (1 - p) * log2(1 - p))


def sigmoid(x):
    return 1 / (1 + exp(-x))


def sigmoid_prime(x):
    s = sigmoid(x)
    return s * (1 - s)


def floor_loss():
    return -sum(MARGINAL[ch] * (TRUE_P1[ch] * log2(TRUE_P1[ch])
                                + (1 - TRUE_P1[ch]) * log2(1 - TRUE_P1[ch]))
                for ch in MARGINAL)


def model_p1(ch, theta, w):
    """The constrained one-parameter family."""
    return sigmoid(theta + w * log2(MARGINAL[ch]))


def loss(theta, w):
    total = 0.0
    for ch, px in MARGINAL.items():
        q = model_p1(ch, theta, w)
        q = min(max(q, 1e-12), 1 - 1e-12)
        total -= px * (TRUE_P1[ch] * log2(q) + (1 - TRUE_P1[ch]) * log2(1 - q))
    return total


def gradients(theta, w):
    """d/dtheta and d/dw of the cross-entropy (natural-log form)."""
    dt = dw = 0.0
    for ch, px in MARGINAL.items():
        x = theta + w * log2(MARGINAL[ch])
        q = sigmoid(x)
        # d(-y log q - (1-y) log(1-q))/dq = (q - y) / (q(1-q))
        g = px * (q - TRUE_P1[ch]) / (q * (1 - q))
        dt += g * sigmoid_prime(x)
        dw += g * sigmoid_prime(x) * log2(MARGINAL[ch])
    # chain rule for log base 2 adds a factor ln 2
    import math
    return dt / math.log(2), dw / math.log(2)


# (a) the loss floor
floor = floor_loss()
print(f"(a) loss floor (true conditional entropy) = {floor:.6f} bits/token")

# (b) gradient descent
theta, w, lr = 0.0, 1.0, 0.5
for step in range(4000):
    dt, dw = gradients(theta, w)
    theta -= lr * dt
    w -= lr * dw

fitted = loss(theta, w)
print(f"(b) fitted theta={theta:.6f}, w={w:.6f}")
print(f"    fitted cross-entropy = {fitted:.6f} bits/token")
print(f"    excess over floor     = {fitted - floor:.6f} bits "
      f"({(fitted / floor - 1) * 100:.2f}% worse)")

print()
print(f"    letter | P(marginal) | true P(vowel) | model P(vowel)")
for ch in MARGINAL:
    print(f"    {ch:6} | {MARGINAL[ch]:13.2f} | {TRUE_P1[ch]:13.2f} "
          f"| {model_p1(ch, theta, w):14.4f}")

# (c) perplexity
print()
print(f"(c) floor perplexity     = {2 ** floor:.4f}")
print(f"    fitted perplexity    = {2 ** fitted:.4f}")

# (d) KL divergence = cross-entropy minus label entropy
print()
print(f"(d) KL(true || model) per token = {fitted - floor:.6f} bits")
print("    (equal to the excess in (b), because KL = CE - H(P))")

# (e) explicit KL computation
kl = 0.0
for ch, px in MARGINAL.items():
    q = model_p1(ch, theta, w)
    p1 = TRUE_P1[ch]
    kl += px * (p1 * log2(p1 / q) + (1 - p1) * log2((1 - p1) / (1 - q)))
print(f"    computed directly, KL = {kl:.6f} bits  "
      f"(matches: {abs(kl - (fitted - floor)) < 1e-9})")
print()
print("(e) cross-entropy measures PREDICTION quality; KL measures DISTANCE")
print("    from the truth. They differ by H(P), which no model controls.")
```

The final lines are the payoff: cross-entropy and KL are the *same optimisation
problem* (differ by a constant independent of the parameters) but *different
measurements*. A trainer minimising cross-entropy is exactly minimising KL, and a
reporting dashboard that shows only cross-entropy is hiding the one number that
tells you how good the model could possibly be.

</details>

## Summary

- The self-information of an event is −log₂ p bits: 1 bit for a fair coin, 0 for a
  certainty, unbounded as p → 0.
- Information must add on independent events, and only a logarithm does that —
  which is why the base-2 log appears.
- Entropy H(P) = −Σp log₂ p is average surprisal, bounded by log₂ n and maximised
  by the uniform distribution.
- 2^H is the **effective number of equally likely outcomes**, often the most
  interpretable summary of a distribution.
- Cross-entropy H(P,Q) = H(P) + D_KL(P‖Q) splits prediction error into an
  irreducible part H(P) and a reducible part KL — and that is why the loss never
  reaches zero.
- Gibbs' inequality gives D_KL(P‖Q) ≥ 0 with equality iff P = Q; KL is **not**
  symmetric, and the asymmetry is why generative models use it in this direction.
- The chain rule H(X,Y) = H(X) + H(Y|X) is how language models factor sentence
  probabilities, and why they work in log-space.
- Mutual information I(X;Y) = H(X)+H(Y)−H(X,Y) = D_KL(joint ‖ product of
  marginals) measures dependence that correlation cannot see.
- Perplexity 2^H is an effective branching factor: cross-entropy 3.322 bits on 10
  classes means the model has learned nothing.

## Next

Part 06 turns to algorithms and complexity. Start with
[80 — Big-O and Complexity Analysis](../part06_algorithms_math/80_big_o_and_complexity.md),
which formalises "fast" — and where the √n results from
[Lesson 68](../part05_probability_statistics/68_law_of_large_numbers_and_clt.md) turn into complexity classes.