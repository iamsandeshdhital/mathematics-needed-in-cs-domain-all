# Part 02 — Discrete Mathematics and Combinatorics

Counting, recurrences, relations, graphs, and trees. This is the part that makes
algorithm analysis possible.

Every object you build in computer science is made of a finite number of things
arranged in some structure. Discrete mathematics is the study of those objects:
how many there are, how they connect, and what follows from the connection. The
formal machinery is thin — a handful of rules and four theorems — but the
judgement required to apply them is real, and that judgement is what this part
teaches.

## What this part assumes

You should have finished [Part 01 — Logic and Proof](../part01_logic_proof/),
in particular [Lesson 15 — Sets and Cardinality](../part01_logic_proof/15_sets_and_cardinality.md).
You need to be comfortable with sets, subsets, the power set, cardinality, and
Cartesian products. Proof technique is used directly here, not decoratively: the
partition theorem in Lesson 25, the cut property in Lesson 27, and the handshake
lemma in Lesson 26 are all proved, and the proofs are short because they are
good.

You do **not** need calculus, linear algebra, or probability. Lesson 22 mentions
the binomial distribution but only uses it as motivation; Lesson 26's adjacency
matrix powers are computed by hand in plain Python and reappear properly in
[Lesson 41](../part03_linear_algebra/41_matrices_graphs_and_applications.md).

Basic Python only. Every example runs with no third-party packages.

## The lessons

| # | Lesson | What it gives you |
| --- | --- | --- |
| 20 | [Counting Principles](../part02_discrete_combinatorics/20_counting_principles.md) | The product rule, the sum rule, and bijections. Three ideas that generate every formula in the part. |
| 21 | [Permutations, Combinations, and Choosing With Limits](../part02_discrete_combinatorics/21_permutations_and_combinations.md) | nCr, nPr, combinations with repetition, the decision rule for choosing between them, and coefficient extraction for bounded selections. |
| 22 | [The Binomial Theorem](../part02_discrete_combinatorics/22_binomial_theorem.md) | Coefficients as counts, weighted sums without loops, popcount distributions, Vandermonde's identity, Lucas' theorem. |
| 23 | [Inclusion–Exclusion and the Pigeonhole Principle](../part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md) | Correcting overlapping cases, surjections, derangements, and existence proofs that require no computation. |
| 24 | [Recurrence Relations](../part02_discrete_combinatorics/24_recurrence_relations.md) | Iterating, characteristic roots, the master theorem, memoisation vs tabulation, fast-doubling Fibonacci, Zeckendorf's theorem. |
| 25 | [Relations and Equivalence Classes](../part02_discrete_combinatorics/25_relations_and_equivalence_classes.md) | Reflexive/symmetric/transitive, partitions, congruence mod n, union–find, `GROUP BY`, and the transitive closure. |
| 26 | [Graph Theory](../part02_discrete_combinatorics/26_graph_theory.md) | Degrees and the handshake lemma, BFS/DFS, bipartite graphs, Euler's theorem, planar bounds, adjacency matrices. |
| 27 | [Trees and Spanning Trees](../part02_discrete_combinatorics/27_trees_and_spanning_trees.md) | Tree invariants, the four traversals, heaps, tries, B-trees, Kruskal, Prim, Dijkstra. |
| 28 | [Counting Strategies and When to Use Each](../part02_discrete_combinatorics/28_counting_strategies.md) | A decision procedure for the whole part, worked classifications, and when to stop counting and write a program. |

## How to read this part

The lessons build on each other in a specific order, and the dependencies are
real rather than decorative:

    20 counting principles
      └─> 21 permutations and combinations
            └─> 22 binomial theorem
                  └─> 23 inclusion-exclusion
                        └─> 24 recurrence relations
                              └─> 25 relations and equivalence classes
                                    └─> 26 graph theory
                                          └─> 27 trees and spanning trees
                                                └─> 28 counting strategies

Lesson 25 is the hinge. Everything before it is about *how many*; everything after
it is about *how things connect*. Union–find appears in 25 and is used by Kruskal
in 27; the transitive closure appears in 25 and becomes connected components in
26; the adjacency matrix in 26 is the matrix whose powers count walks, which is
the first appearance of the linear algebra that Part 03 develops.

## What you should be able to do afterwards

- Take a counting problem and name the technique that applies, with a reason.
- Decide between nCr, nPr, and nⁿ without guessing, using the order/repetition
  questions.
- Compute a count by formula, by recurrence, and by enumeration, and reconcile
  the three.
- Explain why a closed form does not exist for some problems and what to do
  instead.
- Read a complexity claim and decide whether the recurrence behind it was
  analysed correctly.
- Recognise union–find, a trie, a B-tree, a heap, and an MST when you meet one
  outside a textbook.
- Write a brute-force checker for a small instance and use it to validate
  everything above.

## Time

Roughly **5 hours** for the nine lessons at the stated pace, plus several hours
for the exercises. Lessons 23, 27, and 28 are the densest; 20 and 22 are the
fastest. Every code block is executable, so the fastest way to study this part is
to edit the examples and watch the numbers move.

## Where to go next

- [Part 03 — Linear Algebra](../part03_linear_algebra/) picks up the adjacency
  matrices from Lesson 26 and the 2×2 matrices from Lesson 24, and develops the
  mathematics that machine learning is built on. The most-used part in modern CS.
- [Part 06 — Mathematics for Algorithms](../part06_algorithms_math/) turns the
  growth rates computed in Lessons 21 and 24 into the formal language of Big-O,
  amortised analysis, and algorithm design.
- [Part 09 — Number Theory and Cryptography](../part09_number_theory_crypto/)
  builds on the modular arithmetic previewed in Lesson 25, and uses Lucas' theorem
  from Lesson 22 in Reed–Solomon codes.

## Notation

Every symbol used in this part is listed in [SYMBOLS.md](../SYMBOLS.md). The
ones you will meet most: `|A|` for cardinality, `𝒫(A)` for the power set, `≤`
for "at most", `≡` for "congruent", `Σ` for summation, and `n!` for factorial.