# Part 06 — Mathematics for Algorithms

Formalising what "fast" means, and then proving it.

## What this part covers

Three lessons on the mathematics that turns a working program into a claim you
can defend. The part has one running idea: **an algorithm's cost is a number,
and every claim about that number is a theorem with hypotheses you are allowed
to check**. Lesson 80 develops the vocabulary — what grows like what, why the
constant factor is real, why the input parameter is a choice you have to make.
Lesson 81 handles the case where one operation is expensive and almost none
ever is. Lesson 82 is the rest of the toolkit: solving recurrences, proving
correctness, choosing between greedy and dynamic programming, and proving that
a problem is intrinsically hard.

That gives the shape of the part. 80 is the measuring instrument: growth
classes, the doubling table, the feasible-$n$ table, and the recursion
machinery for recursive algorithms. 81 is the correction to the most common
misuse of that instrument — an amortised bound is not a per-operation bound,
and the difference is a promise about totals, not about latency. 82 is the
applied half: once you can measure, you need to design, and design means
solving a recurrence, proving an invariant, and knowing when a problem is
hard on purpose.

The through-line from 80 to 82 is quantifiers. "This is $O(n \log n)$" is a
statement about all inputs; "this is $O(1)$ amortised" is a statement about all
*sequences of operations*; "this is expected $O(1)$" is a statement about a
distribution; "no comparison sort is faster" is a statement about a model.
Lesson 82's lower bounds are the sharpest version of the same idea, and
Lesson 81's distinction between amortised and average is the sharpest version
before that. Learn to say *which quantifier* and the rest of the part follows.

## The lessons

| # | Lesson | What it gives you |
| --- | --- | --- |
| 80 | [Big-O and Complexity Analysis](80_big_o_and_complexity.md) | Growth classes $O, \Omega, \Theta, o, \omega$ and the "eventually" clause that makes them usable; the doubling multiplier for every class; the feasible-$n$ table at a billion operations per second; input parameters and bit complexity, including Python's arbitrary-precision `int`; recurrences, the recursion tree, the Master Theorem and its three cases; Akra–Bazzi and where the Master Theorem fails; repeated squaring |
| 81 | [Amortised Analysis](81_amortized_analysis.md) | Aggregate cost over a worst-case sequence and the amortised cost $\frac{1}{n}\sum T_i$; the three proof techniques — accounting, the potential method, and the telescoping identity; dynamic arrays with geometric growth and the series $1+2+4+\dots$ that bounds the copying; the growth-factor trade, measured, with CPython's real over-allocation; hash-table resizing as an amortised guarantee separated from the expected cost of finding a free slot; binary counters as a second worked potential; why one $\Theta(n)$ operation is not a contradiction |
| 82 | [Mathematical Tools for Algorithm Design](82_tools_for_algorithm_design.md) | Recurrences solved three ways, with $T(n) = 3T(n/2) + n$ worked to the exact closed form $3^{k+1} - 2^{k+1}$; why the naive substitution guess fails and the slack term that repairs it; merge sort's exact comparison counts and Karatsuba's $3^k$ leaves; greedy algorithms and the exchange argument, with activity selection proved and 0/1 knapsack as the counterexample; matroids; dynamic programming, the LCS table, knapsack tables, bitmask states and memoisation; Bellman–Ford, DAG shortest paths, and the single negative edge that breaks Dijkstra; loop invariants and their three obligations; the $\Omega(n\log n)$ comparison-sorting lower bound by counting, Stirling's formula, and why counting sort escapes it |

## What this part assumes

- Lesson 24 (recurrence relations) — for solving $T(n) = a\,T(n/b) + \Theta(n^c)$
  by expansion. Lessons 81 and 82 are applications of it, not new theory.
- Lesson 21 (permutations and combinations) — for the $n!$ that the sorting
  lower bound counts, and for the $C(n,k)$ state counts of bitmask DP.
- Lesson 11 or 12 (proofs and induction) — for the substitution method and the
  loop-invariant template in 82. The proofs in this part are two lines each and
  are meant to be followed, not skipped.
- Lesson 15 (sets and cardinality) for the idea of a family of feasible sets,
  which is what the matroid definition in 82 is talking about.
- Basic Python: lists, loops, functions, a class or two, and
  `heapq`/`functools` from the standard library. Every example runs on Python
  3.11 with the standard library alone; the `### With Libraries` subsections are
  optional.

You do **not** need calculus, you do not need to have taken a algorithms course,
and you do not need to know what a matroid is before Lesson 82 — it is defined
there from scratch. You need to be willing to write one algebraic line and
check it.

## A suggested route

The dependencies are real and short:

```
80 (what fast means: growth classes, bit cost, the Master Theorem)
  └─> 81 (fast in total rather than per operation: amortised analysis)
        └─> 82 (designing and proving: greedy, DP, invariants, lower bounds)
```

Roughly two hours for all three at the stated pace — 45 minutes for 80, 35 for
81, 45 for 82 — and the exercises, which have full worked solutions in the same
files, roughly double that.

Read them in order. If you already know big-O cold and write competitive
programming, start at 81 and skim 80's worked examples: 81 assumes the notation
and nothing else, and its union-by-rank and hash-table sections are the parts
that repay the most.

If you are preparing for an algorithms course or an interview loop, 80 and 82
are the two that get asked; 81 is the one that makes you sound precise about
`dict` and `list.append`, and precision about those is worth real money in a
systems discussion.

## What you should be able to do afterwards

- Look at a piece of code and say what its cost is *as a function of which
  parameter*, then say which parameter you should have chosen.
- Take a recurrence in the Master Theorem's shape, name the case, and give the
  class — and explain in one sentence which part of the recursion tree
  dominates.
- Explain why `list.append` is $O(1)$ amortised, what number it is amortised
  *over*, and why that is not a latency guarantee for any single call.
- Decide between a greedy algorithm and dynamic programming by attempting to
  write the exchange argument, and produce a two-line counterexample when you
  cannot.
- Give the number of states in a DP solution *before* writing it, and say
  whether it will fit in memory.
- Prove a loop correct with an invariant, check the invariant with assertions
  in the code, and prove termination separately.
- State a lower bound together with the model it holds in, and explain how
  counting sort and Dijkstra are not counterexamples to theirs.

## Where to go next

[Part 07 — Geometry for Graphics](../part07_geometry_graphics/) takes the
algorithms of 92 and asks them about space: hulls, closest pairs,
point-in-polygon, and broad-phase structures whose whole purpose is to avoid
the $\Theta(n^2)$ this part has been pricing. Start with
[Lesson 90 — Vectors in 3D and the Cross Product](../part07_geometry_graphics/90_vectors_3d_and_cross_product.md).

[Part 08 — Optimization](../part08_optimization/) is where convexity arrives,
and convexity is the reason a greedy algorithm can be proved correct at all;
[Lesson 100 — Convexity](../part08_optimization/100_convexity.md) develops it.

[Part 05 — Probability and Statistics](../part05_probability_statistics/) is
the other half of the quantifier story. This part keeps amortised (a statement
about every sequence) strictly separate from average case (a statement about a
distribution), and the distribution needs probability —
[Lesson 68 — Law of Large Numbers and the Central Limit Theorem](../part05_probability_statistics/68_law_of_large_numbers_and_clt.md)
is where "the average really does show up" becomes a theorem rather than an
intuition.

For the notation, see [SYMBOLS.md](../SYMBOLS.md). The symbols used here that
are not in the general table — $\Phi$, $\hat{c}_i$, $\alpha(n)$ — are defined
where they appear. Verify the whole part at any time with
`python run_all.py part06_algorithms_math`.