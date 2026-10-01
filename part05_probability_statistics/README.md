# Part 05 — Probability and Statistics

Everything in this part is about handling uncertainty: situations where the
answer is not known in advance and you have to reason about how much you should
believe in each possibility. If Part 02 gave you the counting, Part 04 gave you
the calculus, and Part 03 gave you the linear algebra that machine learning runs
on, this part gives you the ability to say how confident you are — and to be
right about *how* you are confident, which is where most mistakes happen.

The part is built in three movements.

**Lessons 60–62 build the foundation.** Probability starts as a ratio of
cardinalities, which is why
[Part 02](../part02_discrete_combinatorics/20_counting_principles.md) is a hard
prerequisite. Kolmogorov's three axioms then generate every rule you use, and
Bayes' theorem — derived carefully rather than asserted — gives you the ability to
invert a conditional. Lesson 62 spends most of its length on the base-rate
fallacy, because that single misreading of probability causes more damage in
engineering than any other.

**Lessons 63–68 build the machinery.** Random variables turn events into numbers.
Expectation and variance summarise them, and the crucial result is that
linearity of expectation needs no independence while the variance formula does —
an asymmetry that governs every analysis you will write. The CLT and the law of
large numbers then explain why averages converge and why they become normal,
which produces the standard error, and with it every confidence interval and
p-value you have ever read.

**Lessons 69–70 turn it into decisions and losses.** Estimation and hypothesis
testing give the machinery a decision procedure, including an honest account of
what p-values do not mean. Information theory closes the part by showing that the
loss function in your training loop is entropy — which ties the whole part back
to machine learning.

## What this part assumes

- **Counting** from Part 02, especially combinations and inclusion–exclusion. The
  Binomial distribution is a counting result.
- **Integration** from [Lesson 52](../part04_calculus/52_integration.md), which is
  what makes continuous distributions possible.
- **Sums and logarithms** from [Lesson 24](../part02_discrete_combinatorics/24_recurrence_relations.md)
  and earlier. Every expectation is a weighted sum, and information is measured in
  logs.

You do **not** need measure theory, and no lesson here uses integration beyond
what Lesson 52 covers. Proof technique from Part 01 is used lightly: the
derivations are included for understanding rather than as formal exercises, except
for Kolmogorov's axioms and Gibbs' inequality.

## The lessons

| # | Lesson | What you get out of it |
| --- | --- | --- |
| 60 | [Probability Foundations](60_probability_foundations.md) | Sample spaces, events, and the three ways people mean "probability" |
| 61 | [Probability Axioms and Rules](61_probability_axioms_and_rules.md) | Kolmogorov's axioms; addition, complement, multiplication, inclusion–exclusion |
| 62 | [Conditional Probability and Bayes](62_conditional_probability_and_bayes.md) | The chain rule, Bayes' theorem, the base-rate fallacy, naive Bayes |
| 63 | [Discrete Random Variables](63_discrete_random_variables.md) | PMFs, CDFs, Bernoulli, Binomial, and the indicator decomposition |
| 64 | [Expectation, Variance, and Laws](64_expectation_variance.md) | Linearity without independence, variance formulas, why E[X²] ≠ E[X]² |
| 65 | [Continuous Random Variables](65_continuous_random_variables.md) | Densities, Uniform, Exponential (memoryless), Normal, the 68-95-99.7 rule |
| 66 | [Common Distributions](66_common_distributions.md) | Seven distributions with from-scratch samplers and a plotting section |
| 67 | [Joint Variables and Covariance](67_joint_random_variables_covariance.md) | Marginals, independence, correlation is not causation, regression as conditional expectation |
| 68 | [Law of Large Numbers and the CLT](68_law_of_large_numbers_and_clt.md) | Why averages converge and become normal; standard errors; confidence intervals |
| 69 | [Estimation and Hypothesis Testing](69_estimation_and_hypothesis_testing.md) | MLE, bias and variance, p-values, Type I/II errors, power, A/B testing |
| 70 | [Information Theory and Entropy](70_information_theory_entropy.md) | Bits, entropy, KL divergence, cross-entropy loss, perplexity |

## The five ideas that matter most

If you remember nothing else from this part, remember these.

1. **A p-value is not the probability that the hypothesis is true.** It is
   P(data this extreme | the null holds). A "significant" result with a rare
   effect can mean under 2% probability of a real effect, because the base rate
   dominates.
2. **Correlation is not causation, and ρ = 0 does not mean independent.** A
   shared common cause produces correlation with no causal arrow at all; a
   curved relation like Y = X² has ρ = 0 while being completely dependent.
3. **Linearity of expectation needs no independence; the variance formula does.**
   This asymmetry is why means are robust to unmodelled dependencies and spreads
   are not.
4. **Convergence is √n-slow.** Precision scales with the square root of your
   sample size, so halving an error bar costs 4× the data, and detecting a
   0.2 percentage-point change in a 6% conversion rate needs a quarter of a
   million users per arm.
5. **Cross-entropy is entropy.** The loss your network minimises is
   H(P) + D_KL(P‖Q), which is why the loss never reaches zero and why a low loss
   plus a high KL signals a model that found a shortcut.

## How to run the examples

Every code block in this part runs on the Python standard library alone, which is
the point: the mathematics should be visible without a numerical library in the
way. Lessons 66, 67, and 69 have a clearly marked `### With Libraries` section
that adds `matplotlib`/`numpy`/`scipy` for plotting, and those are optional.

To check that every example in the part still produces the numbers quoted in the
prose:

```bash
python run_all.py part05
```

Statistical simulations that quote specific numbers use a fixed random seed, so
their output is reproducible run to run.