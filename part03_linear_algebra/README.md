# Part 03 — Linear Algebra

Vectors and matrices are the native data type of machine learning, scientific
computing, and graphics. This is the most-used part in modern computer science,
and the one with the best ratio of payoff to prerequisite: after these twelve
lessons you can read a linear-algebra result in a paper, implement a solver, and
reason about why a model is or is not identified by its data.

The part has one running idea. A matrix is a **map**: it takes a vector in and
produces a vector out. Almost everything else follows from that. Rank is how many
directions the map keeps. Kernel is how many it throws away. Rank-nullity says
those two numbers add to the input dimension. Eigenvalues and eigenvectors ask
what the map does to its own preferred directions. SVD is the tool that finds
those directions efficiently. The grammar is small; the reach is large.

## What this part assumes

- Lesson 24 (recurrence relations) — nothing more than comfort with indexed sums
  and a slight tolerance for notation.
- Lesson 15 (sets and cardinality) for the idea of a set and a subspace of one.
- Lessons 11–14 for reading the short proofs. The proofs here are one or two
  lines each and are meant to be followed, not skipped.
- Basic Python: lists, loops, nested lists. Every example runs with the standard
  library alone.

You do **not** need calculus, and you do not need any linear algebra beforehand.

## The lessons

| # | Lesson | What it gives you |
| --- | --- | --- |
| 30 | [Vectors and Vector Spaces](30_vectors_and_vector_spaces.md) | Vectors as lists; addition, scaling, span, linear independence, subspaces, and why a data point is a vector |
| 31 | [Matrices and Matrix Algebra](31_matrices_and_matrix_algebra.md) | Matrices as transformations and as tables of coefficients; multiplication, transpose, powers, identity, diagonal and sparse structure |
| 32 | [Linear Systems and Gaussian Elimination](32_linear_systems_gaussian_elimination.md) | Solving `Ax = b` by hand and in code; row reduction, partial pivoting, numerical stability, LU, and the three cases including no unique solution |
| 33 | [Determinant and Inverse](33_determinant_and_inverse.md) | The determinant as a signed volume and an invertibility test; Leibniz and cofactor formulas; computing it in `O(n³)`; the adjugate and its pitfalls |
| 34 | [Basis, Dimension, and Rank](34_basis_dimension_rank.md) | Span versus basis; the row rank = column rank theorem; computing rank; the four fundamental subspaces; rank as degrees of freedom |
| 35 | [Linear Transformations and Kernels](35_linear_transformations_and_kernels.md) | What a linear map is; matrix representations; kernel and image; rank-nullity; why this is the conceptual core |
| 36 | [Eigenvalues and Eigenvectors](36_eigenvalues_and_eigenvectors.md) | Directions a map only rescales; characteristic polynomials; why they decide convergence, stability, and which coordinates matter |
| 37 | [Inner Products, Norms, and Geometry](37_inner_products_norms_geometry.md) | Turning vectors into points; distance and angle; orthogonality; the geometric meaning of everything so far |
| 38 | [Orthogonality and Least Squares](38_orthogonality_and_least_squares.md) | Projection; normal equations and why they square the condition number; QR instead; what residuals mean |
| 39 | [Diagonalization and Spectral Theory](39_diagonalization_and_spectral.md) | When a matrix can be decomposed into eigen-directions; symmetric matrices and the spectral theorem; graph Laplacians |
| 40 | [SVD and PCA](40_svd_and_pca.md) | The best rank-`r` approximation of any matrix; principal component analysis; low-rank compression; the pseudoinverse |
| 41 | [Matrices, Graphs, and Applications](41_matrices_graphs_and_applications.md) | Adjacency and Laplacian matrices, PageRank, Markov chains, linear programming, and other places the whole part lands |

## How to read this part

**The spine is 30 → 31 → 32 → 33 → 34 → 35.** Those six build one argument, and
each one is used by the next. If you read only those, you will be able to read the
rest.

**36 and 37 are a pair.** Read 36 first: eigenvalues are about what a map does.
Then 37 gives you the geometry (length, angle, perpendicularity) that makes the
next lessons' claims concrete. If you are coming from a machine-learning
background, 36 → 37 → 38 → 40 is the route that pays fastest.

**38, 39, and 40 all depend on 37.** They use orthogonality heavily, and 40 in
particular is a direct application of projection. Skipping 37 costs more than it
saves.

**41 is the payoff.** It is a tour of applied uses — graphs, Markov chains, linear
programming — and it is the lesson to read when you want to know why any of this
was worth learning.

## Why the order matters

Lesson 32 introduces row reduction without justification, and lesson 34 explains
why pivots are the whole story. Lesson 33's determinant is a shortcut for lesson
32's existence test, and lesson 35 explains what that test is really about. If
you reorder these, each one loses the reason it is interesting.

The second half has a similar structure: 37 gives the geometry, 38 uses it for
projection, 39 gives the decomposition that makes powers and limits easy, and 40
is the numerical tool that ties it to data. 39 and 40 can be swapped if you are
mostly interested in PCA.

## Practical notes

- Every code block runs on Python 3.11 with the standard library. The
  `### With Libraries` subsections use numpy and scipy and are optional.
- Verify the whole part at any time with `python run_all.py part03_linear_algebra`.
- For the notation, see [SYMBOLS.md](../SYMBOLS.md). The symbols used here that
  are not in the general table are defined where they appear.
- Prerequisite lessons live in
  [Part 02](../part02_discrete_combinatorics/) and
  [Part 01](../part01_logic_proof/). Later parts build on this one:
  [Part 04](../part04_calculus/) uses these matrices for Jacobians and Hessians,
  [Part 05](../part05_probability_statistics/) uses them for covariance,
  [Part 08](../part08_optimization/) uses them for constrained optimisation, and
  [Part 10](../part10_tensors_numerical/) is the practical extension of all of it.
