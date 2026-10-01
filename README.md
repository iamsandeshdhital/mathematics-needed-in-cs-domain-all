# Mathematics Needed in Computer Science

Every piece of mathematics a computer scientist actually needs, written in plain
language, with a runnable Python example and worked exercises on every topic.

This is a **step-by-step** course. Start at Lesson `00` and work forward. Every
lesson is self-contained, so you can jump to a topic directly if you already know
the earlier material.

```
62 lessons · 11 parts · no prerequisites beyond basic Python
```

---

## Why this repository exists

Most "learn math for CS" resources fail in one of two directions:

1. **Too theoretical.** They prove that a theorem holds and never say where the
   theorem shows up in code.
2. **Too shallow.** They hand you a formula and skip the reasoning, so you cannot
   use it on anything you have not already seen.

Every lesson here is built to avoid both problems. The fixed structure of each
lesson is:

| Section | What it gives you |
| --- | --- |
| **In plain words** | The idea without the notation, so you know what you are actually computing |
| **The formal version** | Precise definitions, so you are never guessing |
| **Why CS cares** | Where this appears in real systems, papers, or interviews |
| **Worked example** | A problem solved slowly, step by step, with the reasoning out loud |
| **Runnable code** | Python you can execute and change. Every snippet runs as-is |
| **Common mistakes** | The errors that actually happen, and how to spot them |
| **Exercises + solutions** | Problems to try, with the full answer underneath |

---

## The 11 parts

### Part 00 — Orientation
Get set up, learn to read mathematical notation, and get a study plan.

| # | Lesson |
| --- | --- |
| 00 | [Why Mathematics Matters in Computer Science](part00_orientation/00_why_math_matters.md) |
| 01 | [How to Read Mathematical Notation](part00_orientation/01_how_to_read_notation.md) |
| 02 | [Study Plan and Prerequisites](part00_orientation/02_study_plan.md) |

### Part 01 — Logic and Proof
The foundation of everything else. If a statement is not precisely defined, no
amount of computation makes it reliable.

| # | Lesson |
| --- | --- |
| 10 | [Propositions and Connectives](part01_logic_proof/10_propositions_and_connectives.md) |
| 11 | [Truth Tables, Equivalence, and Normal Forms](part01_logic_proof/11_truth_tables_and_equivalence.md) |
| 12 | [Predicates and Quantifiers](part01_logic_proof/12_predicates_and_quantifiers.md) |
| 13 | [Proof Techniques](part01_logic_proof/13_proof_techniques.md) |
| 14 | [Mathematical Induction](part01_logic_proof/14_mathematical_induction.md) |
| 15 | [Sets and Cardinality](part01_logic_proof/15_sets_and_cardinality.md) |

### Part 02 — Discrete Mathematics and Combinatorics
Counting, graphs, and recurrences. This is the part that makes algorithm
analysis possible.

| # | Lesson |
| --- | --- |
| 20 | [Counting Principles](part02_discrete_combinatorics/20_counting_principles.md) |
| 21 | [Permutations, Combinations, and Choosing With Limits](part02_discrete_combinatorics/21_permutations_and_combinations.md) |
| 22 | [The Binomial Theorem](part02_discrete_combinatorics/22_binomial_theorem.md) |
| 23 | [Inclusion–Exclusion and the Pigeonhole Principle](part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md) |
| 24 | [Recurrence Relations](part02_discrete_combinatorics/24_recurrence_relations.md) |
| 25 | [Relations and Equivalence Classes](part02_discrete_combinatorics/25_relations_and_equivalence_classes.md) |
| 26 | [Graph Theory](part02_discrete_combinatorics/26_graph_theory.md) |
| 27 | [Trees and Spanning Trees](part02_discrete_combinatorics/27_trees_and_spanning_trees.md) |
| 28 | [Counting Strategies and When to Use Each](part02_discrete_combinatorics/28_counting_strategies.md) |

### Part 03 — Linear Algebra
Vectors and matrices are the native data type of machine learning. This is the
most used part in modern CS.

| # | Lesson |
| --- | --- |
| 30 | [Vectors and Vector Spaces](part03_linear_algebra/30_vectors_and_vector_spaces.md) |
| 31 | [Matrices and Matrix Algebra](part03_linear_algebra/31_matrices_and_matrix_algebra.md) |
| 32 | [Linear Systems and Gaussian Elimination](part03_linear_algebra/32_linear_systems_gaussian_elimination.md) |
| 33 | [Determinant and Inverse](part03_linear_algebra/33_determinant_and_inverse.md) |
| 34 | [Basis, Dimension, and Rank](part03_linear_algebra/34_basis_dimension_rank.md) |
| 35 | [Linear Transformations and Kernels](part03_linear_algebra/35_linear_transformations_and_kernels.md) |
| 36 | [Eigenvalues and Eigenvectors](part03_linear_algebra/36_eigenvalues_and_eigenvectors.md) |
| 37 | [Inner Products, Norms, and Geometry](part03_linear_algebra/37_inner_products_norms_geometry.md) |
| 38 | [Orthogonality and Least Squares](part03_linear_algebra/38_orthogonality_and_least_squares.md) |
| 39 | [Diagonalization and Spectral Theory](part03_linear_algebra/39_diagonalization_and_spectral.md) |
| 40 | [SVD and PCA](part03_linear_algebra/40_svd_and_pca.md) |
| 41 | [Matrices, Graphs, and Applications](part03_linear_algebra/41_matrices_graphs_and_applications.md) |

### Part 04 — Calculus
Needed for optimisation, machine learning, graphics, and error analysis.

| # | Lesson |
| --- | --- |
| 50 | [Functions, Limits, and Continuity](part04_calculus/50_functions_limits_continuity.md) |
| 51 | [Derivatives](part04_calculus/51_derivatives.md) |
| 52 | [Integration](part04_calculus/52_integration.md) |
| 53 | [Multivariable Calculus](part04_calculus/53_multivariable_calculus.md) |
| 54 | [Taylor Series](part04_calculus/54_taylor_series.md) |
| 55 | [Fourier Series and Transforms](part04_calculus/55_fourier_series_and_transforms.md) |

### Part 05 — Probability and Statistics
Uncertainty handling. Essential for ML, A/B testing, and any system that learns
from noisy data.

| # | Lesson |
| --- | --- |
| 60 | [Probability Foundations](part05_probability_statistics/60_probability_foundations.md) |
| 61 | [Probability Axioms and Rules](part05_probability_statistics/61_probability_axioms_and_rules.md) |
| 62 | [Conditional Probability and Bayes' Theorem](part05_probability_statistics/62_conditional_probability_and_bayes.md) |
| 63 | [Discrete Random Variables](part05_probability_statistics/63_discrete_random_variables.md) |
| 64 | [Expectation, Variance, and Laws](part05_probability_statistics/64_expectation_variance.md) |
| 65 | [Continuous Random Variables](part05_probability_statistics/65_continuous_random_variables.md) |
| 66 | [Common Distributions](part05_probability_statistics/66_common_distributions.md) |
| 67 | [Joint Random Variables and Covariance](part05_probability_statistics/67_joint_random_variables_covariance.md) |
| 68 | [Law of Large Numbers and the Central Limit Theorem](part05_probability_statistics/68_law_of_large_numbers_and_clt.md) |
| 69 | [Estimation and Hypothesis Testing](part05_probability_statistics/69_estimation_and_hypothesis_testing.md) |
| 70 | [Information Theory and Entropy](part05_probability_statistics/70_information_theory_entropy.md) |

### Part 06 — Mathematics for Algorithms
Formalising what "fast" means and proving it.

| # | Lesson |
| --- | --- |
| 80 | [Big-O and Complexity Analysis](part06_algorithms_math/80_big_o_and_complexity.md) |
| 81 | [Amortised Analysis](part06_algorithms_math/81_amortized_analysis.md) |
| 82 | [Mathematical Tools for Algorithm Design](part06_algorithms_math/82_tools_for_algorithm_design.md) |

### Part 07 — Geometry for Graphics
Matrices in 3D, used by every rendering engine and game engine.

| # | Lesson |
| --- | --- |
| 90 | [Vectors in 3D and the Cross Product](part07_geometry_graphics/90_vectors_3d_and_cross_product.md) |
| 91 | [Transformations for Computer Graphics](part07_geometry_graphics/91_transformations_graphics.md) |
| 92 | [Geometric Algorithms](part07_geometry_graphics/92_geometric_algorithms.md) |

### Part 08 — Optimisation
How machines find the best answer when there are too many to check.

| # | Lesson |
| --- | --- |
| 100 | [Convexity](part08_optimization/100_convexity.md) |
| 101 | [Gradient Descent](part08_optimization/101_gradient_descent.md) |
| 102 | [Lagrange Multipliers and Constraints](part08_optimization/102_lagrange_multipliers_and_knt.md) |

### Part 09 — Number Theory and Cryptography
The arithmetic behind security, hashing, and error correction.

| # | Lesson |
| --- | --- |
| 110 | [Number Theory](part09_number_theory_crypto/110_number_theory.md) |
| 111 | [Modular Arithmetic and Public-Key Crypto](part09_number_theory_crypto/111_modular_arithmetic_and_crypto.md) |
| 112 | [Hashing](part09_number_theory_crypto/112_hashing.md) |
| 113 | [Error-Correcting Codes](part09_number_theory_crypto/113_error_correcting_codes.md) |

### Part 10 — Tensors and Numerical Methods
The practical bridge between the mathematics and modern frameworks.

| # | Lesson |
| --- | --- |
| 120 | [Tensors and Broadcasting](part10_tensors_numerical/120_tensors_and_broadcasting.md) |
| 121 | [Numerical Methods and Floating Point](part10_tensors_numerical/121_numerical_methods_and_floating_point.md) |

---

## Setup

```bash
git clone https://github.com/iamsandeshdhital/mathematics-needed-in-cs-domain-all.git
cd mathematics-needed-in-cs-domain-all
pip install -r requirements.txt
```

Then print the full index of lessons:

```bash
python index.py
```

Verify that every code example in the repository still runs:

```bash
python run_all.py
```

---

## How to study from this

**If you are starting from zero.** Work through the parts in order. Do not skip
Part 01. Proof technique in Part 01 is used directly in Parts 02, 03, and 05, and
skipping it makes everything later harder to check.

**If you remember some calculus or linear algebra.** Read `00`, then skim Parts
03, 04, and 05 to find the gaps, then start properly at Part 01.

**If you are preparing for an interview.** Focus on Part 02 (counting and
graphs), Part 06 (complexity), and the worked examples in Part 03.

**If you are learning ML.** Parts 03, 04, 05, and 08 are the ones you need. The
SVD/PCA lesson alone will change how you read papers.

---

## Conventions

- Notation follows the standard symbols listed in [SYMBOLS.md](SYMBOLS.md).
- Code is Python 3 and runs without modification.
- `[ ]` marks an exercise. `[x]` marks the worked solution underneath it.
- Every worked example is checked numerically, so if a printed value appears in
  the text it is what the code actually produced.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the lesson template and the rules for
adding new material.

## Licence

MIT — see [LICENSE](LICENSE). Use it, teach from it, translate it.