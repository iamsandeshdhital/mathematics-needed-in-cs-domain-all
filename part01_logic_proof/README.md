# Part 01 — Logic and Proof

The foundation for everything else in the repository. Six lessons, about 4
hours of reading and 5 hours of exercises. If you take one part and no other,
take this one.

## What this part covers

| # | Lesson | What it does |
| --- | --- | --- |
| 10 | [Propositions and Connectives](../part01_logic_proof/10_propositions_and_connectives.md) | Statements, AND, OR, NOT, implication, biconditional, and why `if p then q` is not `p and q`. Negating a compound statement correctly. The single most misused piece of notation in all of programming. |
| 11 | [Truth Tables, Equivalence, and Normal Forms](../part01_logic_proof/11_truth_tables_and_equivalence.md) | Truth tables, tautologies, contradictions, logical equivalence, De Morgan's laws, disjunctive and conjunctive normal form, and why that matters for circuit design and for simplifying a condition in your code. |
| 12 | [Predicates and Quantifiers](../part01_logic_proof/12_predicates_and_quantifiers.md) | Predicates over a stated domain, universal and existential quantification, negating quantifiers, nested quantifiers, and the connection to SQL, type systems and test coverage. |
| 13 | [Proof Techniques](../part01_logic_proof/13_proof_techniques.md) | Direct proof, contrapositive, contradiction, the anatomy of a proof, and how each one appears in program verification. |
| 14 | [Mathematical Induction](../part01_logic_proof/14_mathematical_induction.md) | The induction template, why both halves are load-bearing, strong induction, and the exact correspondence with recursive functions and loop invariants. |
| 15 | [Sets and Cardinality](../part01_logic_proof/15_sets_and_cardinality.md) | Set operations, power sets, cardinality, infinite sets and countability including why pairs of naturals can be counted, and how sets appear in data structures. |

## What this part assumes

- You can read Python. `if`, `and`, `or`, `not`, functions, and loops.
- You have read [Lesson 01 — How to Read Notation](../part00_orientation/01_how_to_read_notation.md)
  or an equivalent. This part uses quantifiers and set-builder notation heavily
  from Lesson 12 onward.
- You do **not** need any calculus, linear algebra, or prior exposure to proof.

## How long it takes

| Lesson | Reading | Exercises |
| --- | --- | --- |
| 10 | 30 min | 40 min |
| 11 | 40 min | 50 min |
| 12 | 40 min | 50 min |
| 13 | 45 min | 60 min |
| 14 | 40 min | 55 min |
| 15 | 40 min | 50 min |

Total: **235 minutes** of reading, about **4 hours**, and **305 minutes** of
exercises, about **5 hours**. Plan on **9 hours** for the part. The exercises are
not optional; they are where the material actually lands.

## The one warning

Do not skip Lesson 13 or Lesson 14 on the grounds that you are an engineer.
Lesson 14's induction template *is* the recursive function template and the loop
invariant template, and you already use both. Naming them will make you better
at both. Lesson 13's techniques are the ones you will reach for when a test suite
passes and you still do not know whether the code is right.

## Where to go next

[Part 02 — Discrete Mathematics and Combinatorics](../part02_discrete_combinatorics/README.md)
takes counting, graphs and recurrences, and it uses every technique here.
[Part 06 — Mathematics for Algorithms](../part06_algorithms_math/README.md) uses
proof and sets directly and is only three lessons long if you need big-O now.

The notation used throughout is listed in [SYMBOLS.md](../SYMBOLS.md), and the
lesson-writing conventions are in [CONTRIBUTING.md](../CONTRIBUTING.md).