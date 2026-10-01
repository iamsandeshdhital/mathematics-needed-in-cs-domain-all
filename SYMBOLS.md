# Notation Reference

The symbols used across this repository, and what they mean in plain English.

Knowing these symbols is most of what you need to read any textbook.

## Logic

| Symbol | Name | Means |
| --- | --- | --- |
| `¬P` or `~P` | negation | NOT P. P is false. |
| `P ∧ Q` | conjunction | P AND Q. Both are true. |
| `P ∨ Q` | disjunction | P OR Q. At least one is true. |
| `P → Q` | implication | If P then Q. P implies Q. |
| `P ↔ Q` | biconditional | P if and only if Q. Both directions hold. |
| `⊤` | top | always true |
| `⊥` | bottom | always false |
| `∀` | for all | every, for each |
| `∃` | there exists | at least one |
| `∄` | there does not exist | none |
| `∃!` | unique existence | exactly one |

## Sets

| Symbol | Name | Means |
| --- | --- | --- |
| `{a, b, c}` | set literal | the set containing exactly these items |
| `x ∈ S` | membership | x is an element of S |
| `x ∉ S` | non-membership | x is not in S |
| `A ⊆ B` | subset | every element of A is in B |
| `A ⊂ B` | proper subset | A is a subset of B, and A ≠ B |
| `A ∪ B` | union | everything in A or in B, or both |
| `A ∩ B` | intersection | only what is in both A and B |
| `A \ B` or `A − B` | set difference | in A but not in B |
| `A Δ B` | symmetric difference | in exactly one of A or B |
| `A × B` | Cartesian product | all ordered pairs (a, b) |
| `Aᶜ` or `Ā` | complement | everything not in A |
| `∅` | empty set | the set with no elements |
| `ℝ` | reals | all real numbers |
| `ℤ` | integers | all whole numbers, negative allowed |
| `ℕ` | naturals | 0, 1, 2, 3, … (sometimes starts at 1) |
| `ℚ` | rationals | all fractions p/q with q ≠ 0 |
| `ℂ` | complex | all a + bi |
| `\|A\|` or `\|A\|` | cardinality | how many elements are in A |
| `𝒫(A)` | power set | the set of all subsets of A |

## Functions and Calculus

| Symbol | Name | Means |
| --- | --- | --- |
| `f: X → Y` | function | maps inputs from X to outputs in Y |
| `f(x)` | evaluation | the output when the input is x |
| `f⁻¹` | inverse | undoes f |
| `f∘g` | composition | f applied to the result of g |
| `f′` or `df/dx` | derivative | the rate of change, the slope |
| `f″` | second derivative | the rate of change of the rate of change |
| `∂f/∂x` | partial derivative | derivative with respect to x only, others held fixed |
| `∇f` | gradient | the vector of all partial derivatives |
| `∫ f dx` | integral | area under the curve, accumulated change |
| `Σ` | summation | add up all the terms |
| `∏` | product | multiply up all the terms |
| `lim` | limit | the value the function approaches |
| `→∞` | to infinity | grows without bound |
| `≈` | approximately | close to, not exact |
| `≡` | identically equal / congruent | equal for all cases, not just this one |
| `∈` | in | belongs to |
| `∝` | proportional to | ratio stays constant |
| `O()`, `Θ()`, `o()` | asymptotic | grows at this rate |

## Linear Algebra

| Symbol | Name | Means |
| --- | --- | --- |
| **v** | vector | an arrow, a list of numbers |
| `A` | matrix | a grid of numbers |
| `Aᵀ` | transpose | flip rows and columns |
| `A⁻¹` | inverse | the matrix that undoes A |
| `A⁺` | pseudoinverse | best approximation to an inverse |
| `AB` | matrix product | apply A then B |
| `I` | identity | does nothing when multiplied |
| `tr(A)` | trace | sum of the diagonal entries |
| `det(A)` | determinant | volume scale factor, and invertibility test |
| `λ` | eigenvalue | the scaling factor of an eigenvector |
| `x` | eigenvector | a direction that only gets scaled |
| `Q` | orthogonal matrix | preserves lengths and angles |
| `xᵀy` | dot product | multiply and add |
| `‖x‖` | norm | the length of x |
| `x ⊥ y` | orthogonal | the vectors point at right angles |
| `x ⊗ y` | Kronecker / outer product | build a matrix from two vectors |
| `dim(V)` | dimension | how many independent directions are in V |
| `ker(A)` | null space | inputs that map to zero |
| `im(A)` | image / range | every output the matrix can produce |
| `span(S)` | span | everything buildable as linear combinations of S |

## Probability and Statistics

| Symbol | Name | Means |
| --- | --- | --- |
| `P(A)` | probability | chance of A, between 0 and 1 |
| `X` | random variable | an outcome that is not decided yet |
| `x` or `X = 5` | value | one specific outcome |
| `p_X(x)` | PMF | probability that X equals exactly x |
| `p_X(x)`, `f_X(x)` | PDF | density curve for continuous X |
| `E[X]` or `μ` | expectation | the average value over the long run |
| `Var(X)` or `σ²` | variance | how spread out the values are |
| `σ` | standard deviation | spread in the original units |
| `μ`, `σ` | mean and std | the two numbers describing a distribution |
| `Cov(X, Y)` | covariance | do they move together |
| `ρ` | correlation | do they move together, scaled to −1…1 |
| `~` | distributed as | follows this distribution |
| `E[·]` | expectation | average over all possible outcomes |
| `X ⟂ Y` | independent | knowing X tells you nothing about Y |
| `H(X)` | entropy | average surprise in bits |
| `D_KL(P‖Q)` | KL divergence | how far P is from Q |

## Number Theory

| Symbol | Name | Means |
| --- | --- | --- |
| `a \| b` | divides | b is a multiple of a |
| `a ∤ b` | does not divide | no whole number k gives b = ak |
| `gcd(a, b)` | greatest common divisor | largest shared factor |
| `lcm(a, b)` | least common multiple | smallest shared multiple |
| `a mod m` | remainder | the leftover after division |
| `a ≡ b (mod m)` | congruent | a and b leave the same remainder |
| `φ(n)` | Euler's totient | count of numbers from 1 to n coprime to n |
| `a⁻¹ mod m` | modular inverse | the number that multiplies back to 1 |
| `p` | prime | divisible only by 1 and itself |

## Common quantifier and complexity words

| Word | Means |
| --- | --- |
| `therefore` (∴) | it follows from the previous steps |
| `because` (∵) | the reason for the previous steps |
| `if and only if` (iff) | both directions are true |
| `without loss of generality` (WLOG) | the other cases are symmetric, so one case is enough |
| `QED` / `∎` | the proof ends here |
| `w.r.t.` | with respect to |
| `i.e.` | that is, in other words |
| `e.g.` | for example |
| `et al.` | and others |
| `cf.` | compared to, see also |