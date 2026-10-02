# 02 — Study Plan and Prerequisites

**Part**: part00_orientation · **Prerequisites**: 00, 01 · **Time**: 15 min

---

## In Plain Words

This lesson gives you three concrete week-by-week schedules, tells you which
parts of the course you can skip if you already know them, and gives you a
twenty-question test to work out which schedule is right for you. There is no
advice here beyond that. The plans are dates and lesson numbers.

The reason plans matter more in this subject than in most is that the
prerequisite chain is long and the failure mode is silent. If you start a
lesson on eigenvalues without the idea of a vector space, you will not get a
clear error; you will just not follow the argument, and you will not notice
until three lessons later when the symbols start multiplying. The plan is
organised to prevent that, not to keep you busy.

Read the self-diagnostic first. It takes eight minutes and it decides which of
the three plans you should follow.

## Why Computer Science Cares

**Onboarding is a curriculum problem.** Companies that teach new engineers the
mathematics needed for compiler work, ML infrastructure, or cryptography end up
with the same curriculum the hard way. Knowing what someone already knows is
what makes that possible.

**Interview preparation has a specific shape.** You are not asked about entropy.
You are asked about counting, complexity, and graph traversal. The interview
track in this lesson is built from what is actually asked.

**Reading a paper you cannot verify is a trap.** If a paper claims a
`2^40`-speedup, you need enough linear algebra and complexity analysis to know
whether that is plausible. The ML and systems tracks in this lesson are ordered
so that you can check claims rather than believe them.

**Knowing which foundation is missing saves weeks.** "My gradient descent does
not converge" is usually a convexity problem. "My model's loss is NaN" is usually
a numerical-methods problem. The prerequisite graph below tells you which lesson
to go back to.

## The Formal Version

**Prerequisites.** A lesson `L₂` is a *prerequisite* of lesson `L₁`, written
`L₂ → L₁`, if `L₁` cannot be understood or done properly without `L₂`. This is a
partial order: prerequisites are transitive, so if `A → B` and `B → C` then
`A → C`.

**Transitive closure.** The set of prerequisites of `L` is every lesson
reachable by following prerequisite edges backwards, including the direct ones.
This is the set you must actually have done, not the two or three printed next to
the lesson title.

**A study order** of a set of lessons is a sequence containing every lesson
exactly once, such that no lesson appears before any of its prerequisites. Such
an ordering always exists for this course because the prerequisite relation is
acyclic. A *topological sort* produces one.

**Syllogism.** A prerequisite graph is a directed acyclic graph. A program that
plans your study schedule is a topological sort of that graph, with a tie-break
rule to make the output deterministic. Both are on the list because the same
algorithm schedules your semester, your build, and your reading queue.

## Worked Example

You are a backend engineer, 34 years old, comfortable in Python, you took calculus
at university and remember roughly half of it, you have never done proof, and
you want to be able to read an ML paper. The `03_linear_algebra` track is the
relevant one, but you cannot start at Lesson 30 without Lesson 15, and Lesson 15
sits at the end of Part 01, which you have never opened. Here is how the
arithmetic works out.

**Step 1. Start from the goal.** Lesson 40, SVD and PCA. Look up its direct
prerequisites: `[39]`.

**Step 2. Take the transitive closure.** Lesson 39 needs 38, which needs 37,
which needs 36, and so on down through 35, 34, 33, 32, 31, 30. Lesson 30 needs
15. Lesson 15 needs 14, which needs 13, 12, 11, 10, and Lesson 10 needs 1.

**Step 3. Count.** That is lessons `1, 10, 11, 12, 13, 14, 15` (7 lessons) plus
`30` through `39` (10 lessons) = 17 lessons before you touch PCA. At roughly 45
minutes of reading plus 60 minutes of exercises each, that is about 29 hours.
Over a schedule of four sessions a week, that is seven weeks. This is a
realistic number and worth knowing before you start.

**Step 4. Apply what you already know.** Two things on that list are now partly
done. Lesson 51 (derivatives) is not on it, but calculus was, and Lesson 50's
content is a review for you. Nothing else on the list is salvageable: you have
never done proof, and Lessons 13 and 14 are the ones that unlock everything.

**Step 5. Reorder with your knowledge.** Since you know calculus, put Lesson 30
in week 1 alongside Lessons 1 and 10 to 12. Since you have never done proof, do
not try to compress Lessons 13 to 15. Those three lessons are where the time
goes, and they are the ones where skipping shows up later as "I don't know why
this step is valid."

**Step 6. Find your actual week 1.** Monday: Lesson 01, the notation lesson, 25
minutes plus 30. Wednesday: Lesson 10, propositions, 30 plus 40. Saturday: Lesson
11, truth tables, 40 plus 50, and Lesson 12's `In Plain Words` section as a
preview. That is about three hours for the week including exercises, which is
slower than the fast track and about right for someone meeting proof for the
first time.

**Step 7. Notice what you actually decided.** You chose a track from a graph,
applied what you already had, and put the unfamiliar material on the critical
path. That is the whole procedure, and the code below automates steps 1 through
4.

## Runnable Code

### The 20-question self-diagnostic

```python
# Answer each question OUT LOUD before reading the answer key.
# The point is to find out what to skip, not to feel bad about the rest.

questions = [
    ("Part 01 logic", "Is 'if p then q' the same statement as 'p and q'?",
     "No. p -> q is false only when p is true and q is false; it is true in three cases."),
    ("Part 01 logic", "State the negation of 'for every x, P(x)'.",
     "'There exists an x with not P(x)'. Flip the quantifier AND negate the predicate."),
    ("Part 01 logic", "What distinguishes a contradiction from a tautology?",
     "It is false for every assignment. A tautology is true for every assignment."),
    ("Part 01 proof", "Name the four proof styles used in this part.",
     "Direct, contrapositive, contradiction, induction."),
    ("Part 01 proof", "Why does induction need a base case?",
     "The step case only proves 'if it holds for n then it holds for n+1'. With no "
     "starting point the chain attaches to nothing and proves nothing."),
    ("Part 01 sets", "How many subsets does a set with 3 elements have?",
     "8. Each element is independently in or out, so 2^3 = 8."),
    ("Part 01 sets", "Can a set contain another set?",
     "Yes. {1, {2,3}} has one element, and that element is the set {2,3}."),
    ("Part 02 combinatorics", "How many ways to choose 3 of 10, order irrelevant?",
     "C(10,3) = 10! / (3! * 7!) = 120."),
    ("Part 02 combinatorics", "Is there an infinite set larger than the naturals?",
     "No. Every infinite set can be put into one-to-one correspondence with N. "
     "Counting alone cannot reach infinity."),
    ("Part 06 algorithms", "Difference between O(n) and Theta(n)?",
     "O(n) is only an upper bound. Theta(n) says the growth is exactly linear."),
    ("Part 06 algorithms", "Binary search over 1,000,000 sorted items: how many steps?",
     "About log2(1000000) = 20 comparisons. 2^20 is already over a million."),
    ("Part 03 linear algebra", "What is a matrix, dimensionally?",
     "A function from pairs of indices to numbers: an m x n matrix maps |A| x |B| into R."),
    ("Part 03 linear algebra", "What does it mean for v to be an eigenvector of A?",
     "A*v = lambda*v for some scalar lambda. The direction survives, only the length changes."),
    ("Part 04 calculus", "What does the derivative of f at a point represent?",
     "The best linear approximation near that point: the slope of the tangent line."),
    ("Part 04 calculus", "What does an integral add up?",
     "Infinitely many tiny contributions. Signed area, or accumulated change."),
    ("Part 05 probability", "What is the probability of an impossible event?",
     "0. The empty set has measure zero."),
    ("Part 05 probability", "State Bayes' theorem in words.",
     "The probability of the cause given the effect, from the reverse and the priors."),
    ("Part 09 number theory", "Why does repeated squaring make modular exponentiation fast?",
     "It turns about 2^k multiplications into k of them, by squaring instead of accumulating."),
    ("Part 09 number theory", "Why can a hash table be O(1) if it still collides?",
     "A good hash spreads keys over a large output range, so collisions stay rare."),
    ("Part 05 information", "What does entropy measure?",
     "Average surprise per observation, in bits. Zero means nothing is unpredictable."),
]

print("A 20-question self-diagnostic across the whole course.")
print("Answer out loud BEFORE reading the answer key below.")
print()
current = None
for part, q, a in questions:
    if part != current:
        print(f"-- {part}")
        current = part
    print(f"  Q: {q}")
    print(f"  A: {a}")
print()
print("Scoring guide:")
print("  16-20 correct : take the thorough track. You will move fast, and the")
print("                  exercises are where your time should go.")
print("  10-15 correct : take the fast track, then slow down on whatever you got")
print("                  right by luck rather than by reasoning.")
print("   4-9  correct : start at Part 01 and do not skip it. Almost everyone who")
print("                  thinks they can skip proof should not.")
print("  0-3   correct : start at Part 00 and work in order. This is the normal")
print("                  path, not the embarrassing one.")
```

### The prerequisite graph, as runnable data

```python
class Lesson:
    """A lesson, its reading time, and the lessons that must come first."""

    def __init__(self, number, title, part, minutes, prereqs=None):
        self.number = number
        self.title = title
        self.part = part
        self.minutes = minutes
        self.prereqs = list(prereqs) if prereqs else []

    def __repr__(self):
        return f"Lesson({self.number}, {self.title!r}, {self.minutes} min)"


CATALOG = [
    Lesson(0, "Why Mathematics Matters", "part00", 15),
    Lesson(1, "How to Read Notation", "part00", 25),
    Lesson(2, "Study Plan", "part00", 15),
    Lesson(10, "Propositions and Connectives", "part01", 30, [1]),
    Lesson(11, "Truth Tables and Equivalence", "part01", 40, [10]),
    Lesson(12, "Predicates and Quantifiers", "part01", 40, [11]),
    Lesson(13, "Proof Techniques", "part01", 45, [12]),
    Lesson(14, "Mathematical Induction", "part01", 40, [13]),
    Lesson(15, "Sets and Cardinality", "part01", 40, [14]),
    Lesson(20, "Counting Principles", "part02", 35, [15]),
    Lesson(21, "Permutations and Combinations", "part02", 35, [20]),
    Lesson(22, "The Binomial Theorem", "part02", 25, [21]),
    Lesson(23, "Inclusion-Exclusion and Pigeonhole", "part02", 40, [22]),
    Lesson(24, "Recurrence Relations", "part02", 45, [23]),
    Lesson(25, "Relations and Equivalence Classes", "part02", 40, [24]),
    Lesson(26, "Graph Theory", "part02", 50, [25]),
    Lesson(27, "Trees and Spanning Trees", "part02", 45, [26]),
    Lesson(28, "Counting Strategies", "part02", 30, [21, 26]),
    Lesson(30, "Vectors and Vector Spaces", "part03", 40, [15]),
    Lesson(31, "Matrices and Matrix Algebra", "part03", 45, [30]),
    Lesson(32, "Linear Systems and Gaussian Elimination", "part03", 45, [31]),
    Lesson(33, "Determinant and Inverse", "part03", 40, [32]),
    Lesson(34, "Basis, Dimension, and Rank", "part03", 40, [33]),
    Lesson(35, "Linear Transformations and Kernels", "part03", 45, [34]),
    Lesson(36, "Eigenvalues and Eigenvectors", "part03", 50, [35]),
    Lesson(37, "Inner Products, Norms, Geometry", "part03", 40, [36]),
    Lesson(38, "Orthogonality and Least Squares", "part03", 45, [37]),
    Lesson(39, "Diagonalization and Spectral Theory", "part03", 45, [38]),
    Lesson(40, "SVD and PCA", "part03", 50, [39]),
    Lesson(41, "Matrices, Graphs, Applications", "part03", 35, [40]),
    Lesson(50, "Functions, Limits, Continuity", "part04", 45, [30]),
    Lesson(51, "Derivatives", "part04", 50, [50]),
    Lesson(52, "Integration", "part04", 50, [51]),
    Lesson(53, "Multivariable Calculus", "part04", 50, [51]),
    Lesson(54, "Taylor Series", "part04", 45, [51, 52]),
    Lesson(55, "Fourier Series and Transforms", "part04", 50, [52]),
    Lesson(60, "Probability Foundations", "part05", 35, [15]),
    Lesson(61, "Probability Axioms and Rules", "part05", 40, [60]),
    Lesson(62, "Conditional Probability and Bayes", "part05", 45, [61]),
    Lesson(63, "Discrete Random Variables", "part05", 40, [62]),
    Lesson(64, "Expectation and Variance", "part05", 45, [63]),
    Lesson(65, "Continuous Random Variables", "part05", 40, [64]),
    Lesson(66, "Common Distributions", "part05", 45, [64]),
    Lesson(67, "Joint Random Variables and Covariance", "part05", 45, [64]),
    Lesson(68, "Law of Large Numbers and CLT", "part05", 50, [64, 52]),
    Lesson(69, "Estimation and Hypothesis Testing", "part05", 50, [64, 68]),
    Lesson(70, "Information Theory and Entropy", "part05", 40, [64, 69]),
    Lesson(80, "Big-O and Complexity", "part06", 50, [24, 30]),
    Lesson(81, "Amortised Analysis", "part06", 40, [80]),
    Lesson(82, "Tools for Algorithm Design", "part06", 45, [81, 23]),
    Lesson(90, "Vectors in 3D and Cross Product", "part07", 35, [30]),
    Lesson(91, "Transformations for Graphics", "part07", 45, [90, 31]),
    Lesson(92, "Geometric Algorithms", "part07", 45, [91, 26]),
    Lesson(100, "Convexity", "part08", 40, [38, 51]),
    Lesson(101, "Gradient Descent", "part08", 45, [100, 36]),
    Lesson(102, "Lagrange Multipliers", "part08", 45, [101, 32]),
    Lesson(110, "Number Theory", "part09", 45, [21, 23]),
    Lesson(111, "Modular Arithmetic and Crypto", "part09", 45, [110]),
    Lesson(112, "Hashing", "part09", 40, [110, 23]),
    Lesson(113, "Error-Correcting Codes", "part09", 40, [111, 22]),
    Lesson(120, "Tensors and Broadcasting", "part10", 45, [31, 35]),
    Lesson(121, "Numerical Methods and Floating Point", "part10", 45, [52, 120]),
]

BY_NUMBER = {lesson.number: lesson for lesson in CATALOG}
TOTAL_MINUTES = sum(lesson.minutes for lesson in CATALOG)
print(f"catalog loaded: {len(CATALOG)} lessons, {TOTAL_MINUTES:,} minutes of reading")
print()


def all_prereqs(number):
    """Every lesson reachable by following prerequisite edges, transitively."""
    seen = set()
    stack = list(BY_NUMBER[number].prereqs)
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        stack.extend(BY_NUMBER[current].prereqs)
    return seen


print("Direct vs transitive prerequisites for a few late lessons:")
for n in (24, 40, 70, 113, 121):
    lesson = BY_NUMBER[n]
    direct = sorted(lesson.prereqs)
    transitive = sorted(all_prereqs(n) - set(direct))
    print(f"  {n:>3} {lesson.title}")
    print(f"      direct      : {direct}")
    print(f"      also needed : {transitive}")
print()

# This is exactly the procedure from the worked example, automated.
def study_order(lessons):
    """Topological sort: a lesson appears only after everything it needs."""
    done = set()
    order = []
    remaining = list(lessons)
    while remaining:
        ready = [l for l in remaining if set(l.prereqs) <= done]
        if not ready:
            raise ValueError(f"cycle, blocked: {[l.number for l in remaining]}")
        chosen = min(ready, key=lambda l: l.number)   # deterministic tie-break
        order.append(chosen.number)
        done.add(chosen.number)
        remaining.remove(chosen)
    return order


order = study_order(CATALOG)
violations = [
    (n, p) for position, n in enumerate(order)
    for p in BY_NUMBER[n].prereqs if p not in set(order[:position])
]
print("the scheduler never puts a lesson before something it depends on:")
print(f"  prerequisite violations : {len(violations)}")
print(f"  first 8 lessons          : {order[:8]}")
print(f"  last 5 lessons           : {order[-5:]}")
print()

# --- The ML track, priced out, exactly as in the worked example.
GOAL = 40                                    # SVD and PCA
needed = sorted(all_prereqs(GOAL)) + [GOAL]
track_minutes = sum(BY_NUMBER[n].minutes for n in needed)
print(f"cost of reaching lesson {GOAL} ({BY_NUMBER[GOAL].title}):")
print(f"  lessons on the path        : {len(needed)}")
print(f"  reading time               : {track_minutes / 60:.1f} hours")
print(f"  with exercises at 60 min   : {(track_minutes + 60 * len(needed)) / 60:.1f} hours")
print(f"  at 4 sessions a week       : {track_minutes / (4 * 60):.1f} weeks of reading alone")
print(f"  the path                   : {needed}")
print()

# --- Session planning: pack lessons into 60-minute slots, never splitting one.
def make_sessions(order, slot_minutes=60):
    sessions, current, used = [], [], 0
    for number in order:
        lesson = BY_NUMBER[number]
        if used + lesson.minutes > slot_minutes and current:
            sessions.append(current)
            current, used = [], 0
        current.append(number)
        used += lesson.minutes
    if current:
        sessions.append(current)
    return sessions


sessions = make_sessions(order)
print(f"packing all {len(order)} lessons into 60-minute slots:")
print(f"  sessions         : {len(sessions)}")
print(f"  average session  : {len(order) / len(sessions):.1f} lessons")
print(f"  shortest / longest: {min(len(s) for s in sessions)} / {max(len(s) for s in sessions)} lessons")
print(f"  session 1        : {sessions[0]}")
print(f"  session 2        : {sessions[1]}")
print()
print(f"Total reading time for the whole course: {TOTAL_MINUTES / 60:.1f} hours.")
print("Reading is about 40% of the work. The rest is doing the exercises by hand,")
print("which is the part that actually moves the needle.")
```

## Common Mistakes

**Wrong: "I will just read the lessons straight through from 00 to 121."**
Right: 62 lessons at 43 hours of reading is roughly 100 hours with exercises, and
there is no point in paying it twice. Take the diagnostic first, skip what you
already know, and spend the saved time on the exercises in Part 01, which are the
ones people skip and the ones everything else depends on.
Why tempting: it feels like cheating to skip material, and a linear path is
comfortable. The skips are not a way of avoiding difficulty; they are a way of
putting the difficulty where it pays.

**Wrong: "I can skip Part 01 because I only care about ML."**
Right: Part 01 is 6 lessons and about 4 hours. It teaches you that a statement
needs a domain and a quantifier, that negating flips quantifiers, and what a
proof obligation actually is. Those three things are what separate people who can
read a paper from people who can only skim it. Skip Part 02's tail if you like;
do not skip Part 01.
Why tempting: Part 01 contains no matrices and no gradients, so it does not look
like it is on the path. The connection is not topical, it is structural.

**Wrong: "I will read a lesson and move on, and do the exercises later if there
is time."**
Right: there will not be time, and the exercises are not revision. The worked
examples in this repository are worked twice, once in the prose and once in
Python, and the exercises are the only place you find out whether you can do it
without the prose. Budget 60 to 90 minutes per lesson, not the header's 25 to 50.
Why tempting: the reading feels like progress and the exercises feel like
drudgery, which is exactly backwards for retention.

**Wrong: "I should understand the whole derivation of an algorithm before using
it."**
Right: you need enough to use it correctly and enough to know when it fails. For
big-O that means being able to compute the complexity of the algorithm you are
writing and having a rough sense of the constants. You do not need a proof of
every theorem in sight. Decide per topic: proofs in Part 01, because they are
about reasoning and you cannot skip them; derivations elsewhere, because they
are about one specific result you will look up again in six months anyway.
Why tempting: completeness feels safer than depth, and it is the wrong trade for
everything except Part 01.

**Wrong: "I will learn the notation as I need it, so I can skip Lesson 01."**
Right: Lesson 01 is 25 minutes and it is the only lesson that pays off
immediately in every part that follows. The people who skip it are the ones who
end up re-reading the same three pages of every chapter for a year. It is the
highest-return 25 minutes in the repository.
Why tempting: notation feels like bookkeeping rather than mathematics, so it
looks like something you can pick up in passing. You can, and then you pay for it
in every later lesson.

## Formula Sheet

This lesson is about a graph, not about a theorem, so the formulas are the
prerequisite relation, the transitive closure, and the arithmetic used to price a
track. Notation follows [SYMBOLS.md](../SYMBOLS.md).

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$L_2 \to L_1$` | | Lesson `L₂` is a prerequisite of `L₁`: you cannot do `L₁` properly without `L₂` | labelling the edge in the header of a lesson. Note the direction: prerequisite **to** dependent, so an edge points *forward* in study order |
| transitive closure | `$P(L) = \{\, M : M \to \cdots \to L \,\}$` over any path of length $\ge 1$ | every lesson you can reach by walking prerequisite edges backwards from `L` | the list you must actually have done. **The one or two prerequisites printed on a lesson are not this set** — for Lesson 40 the closure is 17 lessons, not 1 |
| partial order | `A → B` and `B → C ⟹ A → C` | prerequisites chain: if you need `B` for `C`, you need `A` for `B` and therefore for `C` | justifying "you have to do 10 before 40" without listing every intermediate edge |
| acyclic | no cycle: `$\nexists\, L_1 \to L_2 \to \cdots \to L_k \to L_1$` with $k \ge 1$ | you can never end up needing a lesson in order to take itself | the hypothesis under which a study order **exists**. A cycle means the plan is impossible, not merely hard |
| a *study order* | a sequence containing each lesson exactly once, with no lesson before any of its prerequisites | a legal reading schedule | the output of a topological sort. Every legal order is equally valid; the graph does not pick one for you |
| topological sort | | repeatedly take any lesson whose prerequisites are all done, until none remain | the `study_order` function. The `if not ready` guard is what turns a cycle into a `ValueError` instead of an infinite loop |
| tie-break rule | `chosen = min(ready, key=number)` | when several lessons are ready, take the lowest-numbered one | makes the schedule **deterministic**. Without it the same catalog gives a different plan on every run, which makes the output untestable |
| `all_prereqs(L)` | seen-set filled by a stack walk from `L.prereqs` | the transitive closure, computed | costs $O(\lvert V\rvert + \lvert E\rvert)$ on the whole graph if you do it for every lesson, but $O(\lvert E\rvert)$ per goal because each node is visited once and re-visits are skipped via `seen` |
| `dangling_prereqs` | `$\{p : p \in L.\mathrm{prereqs},\ p \notin \mathrm{catalog}\}$` | prerequisites that name a lesson which does not exist | a **distinct failure** from a cycle. A dangling edge makes the scheduler report "blocked", which reads like a cycle but means a missing node |
| track cost | `needed = P(goal) ∪ {goal}`; `minutes = Σ minutes(l), l ∈ needed` | the lessons you must read, and their total reading minutes | pricing a goal. For Lesson 40: 18 lessons, 12.4 hours of reading |
| `hours` | `minutes / 60` | reading time in hours | the lesson reports **reading only**, about 40% of the real work |
| real cost | `(minutes + 60·|needed|) / 60` | reading plus 60 minutes of exercises per lesson | the honest figure. For Lesson 40 it is **30.4 hours**, not 12.4 — the ratio the lesson's own Common Mistakes section insists on |
| `weeks@k` | `minutes / (k · 60)` | how many weeks of reading at `k` sessions a week | `k = 4` in the lesson. 12.4 h of reading is 3.1 weeks; with exercises it is 7.6 |
| session packing | pack lessons in order into slots, start a new slot when `used + minutes > 60` | group lessons into study sessions of at most an hour | `make_sessions`. Gives **59** sessions. The *volume* bound $\lceil 2570/60\rceil = 43$ is **unreachable**: 51 of the 62 lessons are 40 min or longer, so the true optimum is **57** and the greedy packer is within 2 of it |
| the achievable bound | any pair summing to $\le 60$ must contain a lesson $\le 30$, and only 6 lessons are | at most 6 pairs, so at least `62 - 6 = 56` sessions; the two 30s cannot take a 35, so at most 5 pairs and the optimum is **57** | the honest yardstick for a packer. Report against the *achievable* bound, not the volume bound - the lesson's own "report both numbers" rule |
| capability score | `points_earned / (5 · |lessons|)` | the fraction of the five-item checklist you can actually demonstrate | measuring progress. Never `hours read` — see the Challenge's 9.0-versus-20.0 minutes-per-point contrast |
| minutes per point | `minutes / max(points, 1)` | how long each demonstrated capability cost | the diagnostic column. High values mean you are re-reading rather than practising |
| diagnostic bands | thorough `16–20`, fast `10–15`, Part 01 `4–9`, Part 00 `0–3` | which track your score picks | applied to a 20-question test. **A coin-flip guesser scores 10 on average**, and has a 58.8% chance of landing 10 or more, so a score of 10 means nothing without knowing how you got it |

## Multiple Choice Questions

**Q1.** Lesson 40 prints one direct prerequisite, `[39]`, but its transitive
closure is 17 lessons. A reader plans to start at 40 and moves back to 39, then
39's prerequisites, and so on. What is the most likely outcome?

- A) They reach Part 01 and stop, having read six lessons, because Part 01 is the only part that looks like proof
- B) They reach Lesson 1 and realise they have 17 lessons to do, about 12.4 hours of reading and 30.4 hours in total
- C) They find the graph has a cycle between Part 01 and Part 03 and cannot plan
- D) They skip to Lesson 30 and start there, since Lesson 30 is the first lesson in the linear algebra chain

<details>
<summary>Answer and explanation</summary>

**B) They reach Lesson 1 and realise they have 17 lessons to do, about 12.4
hours of reading and 30.4 hours in total.**

This is exactly the lesson's Step 2 and Step 3, and the point of the transitive
closure: the number printed on a lesson is not the work in front of you. Walking
backwards from 40 gives `39, 38, …, 30`, then `15, 14, 13, 12, 11, 10, 1` — 17
lessons before the goal lesson itself, 18 on the path including it. The lesson's
`all_prereqs(40)` returns exactly that set, and the code prices it at 12.4 hours
of reading.

A is the version where someone follows a *topical* intuition rather than the
graph. Part 01 does contain no matrices, so it looks off the path, and the
lesson's second Common Mistake is precisely this error: the connection is
structural, not topical. Skipping it is the single most expensive plan decision
in the course.

C is wrong, and the code proves it: `study_order(CATALOG)` completes and reports
`prerequisite violations : 0`. There is no cycle. The lesson is explicit that the
relation is acyclic, which is exactly why a legal order exists.

D is a real temptation — Lesson 30 is genuinely the first linear algebra lesson
and genuinely needs only Lesson 15. But skipping 15 means skipping the whole of
Part 01, and the failure is silent: you will not get an error, you will just stop
following the argument three lessons later, which is the lesson's opening claim
about why plans matter more here than in most subjects.

</details>

**Q2.** Someone knows counting and calculus (`ALREADY_KNOWN = {21, 22, 50, 51}`)
and asks how much shorter the road to Lesson 40 (SVD and PCA) gets. The lesson's
Exercise 2 reports a saving of exactly 0 minutes. Why?

- A) The prerequisite graph is computed before the skip set is applied, so the skip is ignored
- B) None of Lessons 21, 22, 50, 51 is on the path to 40, so removing them changes nothing
- C) The skip set is applied twice, cancelling out
- D) Knowing calculus lets you skip Lesson 30, which is where the saving would have come from

<details>
<summary>Answer and explanation</summary>

**B) None of Lessons 21, 22, 50, 51 is on the path to 40, so removing them
changes nothing.**

The path to 40 is `[1, 10, 11, 12, 13, 14, 15, 30, 31, …, 39, 40]` — Part 01 and
the linear algebra chain. The counting lessons 21 and 22 belong to Part 02's
chain (which feeds 23, then 24, then 25, 26), and 50 and 51 belong to Part 04's
calculus chain. None of those four is in the set, so `(all_prereqs(40) ∪ {40}) -
ALREADY_KNOWN` is identical to `all_prereqs(40) ∪ {40}`.

This is the most useful result in the whole exercise, and it is a real finding
rather than a bug. The lesson spells it out: "Proving you remember calculus does
not shorten the road to eigenvalues, because eigenvalues need the linear algebra
chain and the whole of Part 01." Prior experience in one part buys you nothing in
a part whose prerequisites live in a different subtree.

A and C are both wrong about the mechanism. `cost_to_reach` computes
`all_prereqs(goal)` first and subtracts the skip set second, exactly once, and the
Exercise 2 output confirms the subtraction is live — goal 70 saves 95 minutes and
goal 92 saves 60, from the same `ALREADY_KNOWN` set.

D is wrong because the skip set does not include 30, and would not help if it did.
Lesson 30 needs Lesson 15, and 15 needs the whole of Part 01. Knowing calculus is
irrelevant to every step of that chain.

</details>

**Q3.** The lesson scores the 20-question diagnostic with bands `16–20` thorough,
`10–15` fast, `4–9` Part 01, `0–3` Part 00. A colleague who admits they "mostly
guessed" scores 11. What does the band structure tell you about that result?

- A) Nothing — 11 is inside the fast band, so the fast track is validated
- B) The band cannot distinguish a reasoned 11 from a guessed 11, because a coin-flip guesser averages exactly 10
- C) The scoring guide should be changed, because 20 questions is statistically too few to discriminate
- D) A score of 11 must be a fluke, since the probability of guessing 11 or more is negligible

<details>
<summary>Answer and explanation</summary>

**B) The band cannot distinguish a reasoned 11 from a guessed 11, because a
coin-flip guesser averages exactly 10.**

For 20 two-sided questions, a guesser gets 10 on average, and the probability of
getting 10 or more is **58.8%** — better than even. So the entire `10–15` "fast
track" band is inside the range that luck produces. A score of 11 is the *most
likely single outcome* for someone who knows nothing.

This is why the lesson's scoring guide says "take the fast track, then slow down on
whatever you got right by luck rather than by reasoning." The score is a starting
point for self-suspicion, not a measurement of knowledge. The diagnostic is
useful because of the *distribution of your wrong answers*, not the total.

A is the trap. The band boundary is crossed, so the guide says fast track, and the
colleague proceeds confidently through a course they cannot follow. The lesson's
Common Mistakes section describes this exact failure as silent: no error, just
suddenly not following the argument.

C is wrong, and it is the wrong diagnosis. Twenty questions is a fine instrument
for what it is used for; the problem is not sample size but the scoring rule's
failure to weight *which* questions were missed.

D is false in the interesting direction. The probability of reaching 16+ by pure
chance is about **0.59%**, not negligible but genuinely small — so the *thorough*
band is meaningful and the *fast* band is not. That asymmetry is the real design
insight: the top band is trustworthy, the middle band is not, and a diagnostic
that cannot tell you which band you landed in is only half a diagnostic.

</details>

**Q4.** `study_order` raises `ValueError` when no lesson is ready. The lesson
calls this "the failure is `ValueError`, not a hang". Why does the guard matter?

- A) Because `min(ready, ...)` on an empty list raises `ValueError` anyway, so the guard is only for a clearer message
- B) Because without the guard the `while remaining` loop never terminates — no lesson ever becomes ready, so nothing is removed from `remaining`
- C) Because a cycle makes `remaining` grow rather than shrink, which would exhaust memory
- D) Because `study_order` is recursive, and a cycle would cause a stack overflow

<details>
<summary>Answer and explanation</summary>

**B) Because without the guard the `while remaining` loop never terminates — no
lesson ever becomes ready, so nothing is removed from `remaining`.**

The loop condition is `while remaining`. Each pass computes `ready` and removes
one lesson. If `ready` is empty, nothing is removed, `remaining` is unchanged,
and the next pass computes the same empty `ready`. That is an infinite loop that
consumes no memory and produces no output — the worst kind of hang, because it
looks like a slow run rather than a crash.

This is not a hypothetical: Exercise 1 step 3 constructs the cycle deliberately
(42 needs 43, 43 needs 42) and confirms `cycle, blocked: [42, 43]`. The lesson
notes that "real schedulers hit this on every build that introduces a dependency
cycle" — which is why build systems fail with an explicit message rather than
spinning.

A is wrong: `min([])` does raise `ValueError`, but the *reason* is incidental.
The value of the explicit guard is that the message names the blocked lessons,
which is the diagnostic you actually need. It converts a coincidence into a
deliberate report.

C is wrong: `remaining` is a list that only ever shrinks via `remove`. A cycle
cannot make it grow.

D is wrong: `study_order` is iterative, with a `while` loop and a `stack` in
`all_prereqs`. Nothing recurses, so no stack overflow is possible. The cycle
manifests as non-termination, not as recursion depth.

</details>

**Q5.** `make_sessions` packs the 62 lessons into 59 slots of at most 60 minutes.
The total reading time is 2570 minutes, and 51 of the 62 lessons are 40 minutes
or longer. What is the correct assessment of the packer?

- A) It is badly suboptimal, because `ceil(2570/60) = 43` is a lower bound on sessions and the packer uses 59
- B) It is within 2 of optimal: the 43-session bound is unreachable, 51 of the 62 lessons are 40 minutes or longer and barely pair at all, and the true optimum is 57
- C) It is optimal at 59, since no two lessons in the catalog can share a slot
- D) It is optimal at 59, since the packer runs in prerequisite order and no other order is legal

<details>
<summary>Answer and explanation</summary>

**B) It is within 2 of optimal: the 43-session bound is unreachable, 51 lessons
cannot pair with anything above 20 minutes, and the true optimum is 57.**

`ceil(2570/60) = 43` is the *volume* bound: it asks only whether the minutes fit.
They do not, because minutes are not divisible. A 50-minute lesson can share a slot
with nothing at all; a 45- or 40-minute lesson can share only with one of the two
15-minute lessons. The length distribution is 2×15, 2×25, 2×30, 5×35, 18×40,
23×45, 10×50 — so 51 of the 62 lessons are 40 or longer and only 6 are 30 or
shorter.

Since any pair summing to at most 60 must contain a lesson of at most 30, at most
6 pairs are possible, hence at least 56 sessions. And the two 30s cannot take a
35 (`30+35 = 65`), so the 30s either pair with each other or consume smaller
partners — which caps the pairing at 5. So the optimum is `62 − 5 = 57`, and
first-fit-decreasing achieves it. The greedy packer produces 59, wasting 970
minutes where 850 is the unavoidable minimum: a gap of **2 sessions**.

A is the seductive answer, and it is the error the lesson's own warning about
constants invites. Comparing 59 against a bound you have not shown to be
achievable tells you nothing; the 16-session "gap" is mostly an artefact of a
bound that no packing can reach. This is the same mistake as comparing your
algorithm against a lower bound that ignores the problem's structure.

C is wrong because pairs *are* possible: `30+30 = 60`, `25+35 = 60`, `15+40 = 55`,
`15+45 = 60`. At least 5 pairs exist, so 59 is not optimal.

D is wrong for the same reason inverted: the packer is within 2 of a bound that
holds for *any* ordering, and first-fit-decreasing reaches 57 while ignoring
prerequisite order entirely. The order is not what stops it improving.

</details>

**Q6.** The Challenge's capability tracker records one lesson twice: 30 minutes
for capability 1 (abandoned), then 140 minutes for capability 4. The collapse
rule sums the minutes and takes the **max** of the capabilities, giving 170 minutes
at 4 points. Why max and not sum, and what would sum have produced?

- A) Sum would give 180 minutes at 5 points, which would overstate the achievement; max is right because capability is demonstrated once, not accumulated
- B) Sum would give 170 minutes at 5 points, overstating it
- C) Max is wrong; sum is right, because each attempt contributed real effort
- D) Max would give 30 minutes at 4 points, understating the effort

<details>
<summary>Answer and explanation</summary>

**A) Sum would give 180 minutes at 5 points, which would overstate the
achievement; max is right because capability is demonstrated once, not
accumulated.**

Summed, the record would read 170 minutes and 5 points — a perfect score on the
five-item checklist, achieved by a lesson where the first attempt scored 1. That
is precisely the measurement error the tracker exists to prevent: the lesson's
whole argument is that capability is something you *demonstrate*, and you cannot
demonstrate item 4 (solve a problem the lesson never posed) twice.

Max is also the operation that makes retries safe to record at all. Because a
retry replaces the previous score rather than adding to it, you can log every
attempt honestly — including the failed one, which is the record that explains
the 42.5 minutes-per-point figure — without the score becoming a function of how
many times you tried.

B gets the arithmetic wrong: 1 + 4 = 5 points and 30 + 140 = 170 minutes, so the
summed record is 170 min at 5, not at 5 with 180 minutes. C and D both misidentify
what each operation touches. Effort is additive and time is additive — the code
sums minutes for exactly that reason. Capability is neither, and D has the
direction of the error backwards: max takes the *longer* record's minutes only if
it is longer, which it is here.

</details>

**Q7.** The lesson's `## Why Computer Science Cares` says "Reading a paper you
cannot verify is a trap", and justifies the ML and systems tracks by saying they
are "ordered so that you can check claims rather than believe them". Which
concrete skill makes a `2^40`-speedup claim checkable?

- A) Running the benchmark on faster hardware
- B) Computing the complexity of the proposed algorithm and comparing it against the complexity of the baseline
- C) Reading the abstract carefully and trusting the authors' affiliations
- D) Checking that the paper has more than ten citations

<details>
<summary>Answer and explanation</summary>

**B) Computing the complexity of the proposed algorithm and comparing it against
the complexity of the baseline.**

A speedup claim of `2^40` is a claim about *asymptotic* rates plus a constant
factor, and the asymptotic half is checkable by hand. If the paper's method is
`O(n log n)` and the baseline is `O(n²)`, then `2^40` is plausible for large `n`
and absurd for small `n` — and the crossover point is computable. If both are
`O(n²)` and the claim is `2^40`, the claim is entirely a constant-factor
assertion, which is a different and much more suspicious thing to say.

This is the skill the diagnostic's Part 06 questions target: "O(n) is only an
upper bound; Θ(n) says the growth is exactly linear." Reading `O` and `Θ`
correctly is what separates checking from believing.

A does not help at all, and this is the trap. A `2^40` speedup is not something
faster hardware reveals — it is either in the asymptotic rate or it is not there.
A benchmark on hardware four times faster cannot tell you whether the paper's
claim is about the exponent or about an implementation detail.

C is not a check, and affiliation is not evidence of an asymptotic claim. D
counts agreement, not correctness; a wrong claim can be widely cited, and
citation counts measure popularity.

</details>

**Q8.** The lesson says "Never skip Part 01. It is 6 lessons and every other
part's proofs use its techniques." Which of these is a *proof* that skipping it
is costly, rather than an assertion?

- A) The fact that Lesson 12 lists Lesson 11 as a prerequisite and Lesson 13 lists Lesson 12
- B) The fact that Part 01 is only about 4 hours of reading out of 42.8
- C) The fact that Part 01 contains no matrices, so nothing later depends on its *content*
- D) The fact that Lesson 20 needs Lesson 15, so the chain is transitive

<details>
<summary>Answer and explanation</summary>

**A) The fact that Lesson 12 lists Lesson 11 as a prerequisite and Lesson 13
lists Lesson 12.**

This is the load-bearing argument, because it is structural. The edges
`11 → 12`, `12 → 13`, `13 → 14`, `14 → 15` mean that every lesson numbered 20
or higher inherits the whole of Part 01 through the closure. The code verifies
this mechanically: `all_prereqs(40)`, `all_prereqs(70)`, `all_prereqs(113)` and
`all_prereqs(121)` all contain `[1, 10, 11, 12, 13, 14, 15]`. That is a
demonstration, not a claim.

B is the *opposite* of an argument against skipping. Four hours out of 42.8 is
9% of the reading — a small price, which is exactly why the claim needs
structural support rather than an appeal to volume. If skipping were expensive
merely in hours, the calculus answer would be to skip it.

C is a misreading of the argument. The lesson says the connection is "not topical,
it is structural." Part 01 containing no matrices is the *reason* the mistake is
tempting, not a reason it is safe. Lesson 15 (sets) is the bridge: it is a
direct prerequisite of both Lesson 30 and Lesson 60, so it is the single node
through which everything downstream passes.

D is true but it is the *wrong part* of the graph. `20 → 15` shows the chain is
transitive, which is a fact about the relation; it does not show the cost of
skipping. The cost is visible only in a closure containing all six Part 01
lessons for a goal like 40 or 70.

</details>

**Q9.** The worked example puts Lesson 30 in week 1 "alongside Lessons 1 and 10 to
12" because the reader knows calculus, and then declines to compress Lessons 13
to 15. What is the actual justification for declining?

- A) Those three lessons are unusually long: 45 + 40 + 40 = 125 minutes
- B) They are the lessons the reader has never encountered, and the goal's transitive closure requires all of them, so time spent anywhere else does not shorten the path
- C) The reader is not old enough for proof, and the lesson refuses to make that judgment
- D) Lesson 13 is a prerequisite of Lesson 14 but not of Lesson 15, so only two are required

<details>
<summary>Answer and explanation</summary>

**B) They are the lessons the reader has never encountered, and the goal's
transitive closure requires all of them, so time spent elsewhere does not shorten
the path.**

The lesson's Step 5 says it directly: "Since you have never done proof, do not try
to compress Lessons 13 to 15. Those three lessons are where the time goes, and
they are the ones where skipping shows up later as 'I don't know why this step is
valid.'" The whole procedure is *graph plus what you already have*: the
prerequisites you satisfy are removed, and the ones you do not are on the
critical path.

The reason this matters is the same lesson's opening claim — the failure mode is
silent. There is no error when you read an induction proof without induction; you
simply cannot tell that a step is unjustified. The cost of compression here is not
"three lessons take longer", it is that the compression is invisible until much
later, when you cannot recover the diagnosis.

A is arithmetically irrelevant. 125 minutes is about two hours out of a 30.4-hour
budget, and the lesson gives no length-based argument anywhere. Being longest is
not the criterion; being *unsatisfied* is.

C invents a demographic objection the lesson does not make. It says "you have
never done proof" as a fact about the reader in the worked example, and it is a
statement about preparation, not age.

D is false: the catalog declares `Lesson(15, "Sets and Cardinality", 40, [14])`,
so 13, 14 and 15 form an unbroken chain, and 15 is a direct prerequisite of both
30 and 60.

</details>

**Q10.** Exercise 3's checklist item 4 is "you can solve a problem in the lesson's
area that is not in the lesson", and the lesson says this is the item that fails
on reading alone. Why is item 4 not satisfiable by re-reading?

- A) Because re-reading does not change what is printed in the lesson
- B) Because items 1, 2, 3 and 5 can all be checked against the text, while item 4 requires producing something the text does not contain
- C) Because item 4 is deliberately unfair and no one can satisfy it
- D) Because the lesson's own exercises are not problems in the lesson's area

<details>
<summary>Answer and explanation</summary>

**B) Because items 1, 2, 3 and 5 can all be checked against the text, while item 4
requires producing something the text does not contain.**

Item 1 is compression of what the lesson says. Item 2 is explaining the code
blocks, which are printed. Item 3 is finding a counterexample, and after reading
you can at least locate candidate claims and their negations. Item 5 is naming a
downstream lesson, which is a lookup in the catalog. All four are *retrieval or
restructuring of content that exists somewhere in the lesson or the repository*.

Item 4 is the only one that is *generation*. The lesson's own worked answer
makes this concrete: no exercise in Lesson 11 asks for the shortest formula
computing a given truth-table column, and finding that the truth table is a finite
object you can search over is a step the lesson never takes. Re-reading cannot
supply it, because there is nothing there to re-read.

A is a true-sounding statement that does not bear on the question. Re-reading
*does* improve your recall of the content, which is what items 1, 2, 3 and 5
measure. The asymmetry is about the *type* of task, not about the efficacy of
re-reading.

C is wrong: the lesson's worked answer satisfies item 4 for real, by writing the
`truth_column` search and the `(a + b + c) >= 2` shortcut. It is demanding, not
impossible.

D is wrong because the lesson's exercises are in the lesson's area — that is what
makes item 3 answerable. Item 4 asks for a problem the author did not think to
pose, which is the difference.

</details>

## Subjective Questions

### Short Answer

**Q1. State the definition of "prerequisite" from this lesson, and say what
makes the relation a partial order.**

<details>
<summary>Answer</summary>

Lesson `L₂` is a *prerequisite* of lesson `L₁`, written `L₂ → L₁`, if `L₁` cannot
be understood or done properly without `L₂`.

It is a partial order because it is **transitive**: if `A → B` and `B → C` then
`A → C`. So if you need `B` to do `C`, you need `A` for `B` and therefore for
`C` too — which is why the closure, not the printed edge, is the real work.

</details>

**Q2. How many lessons are on the path to Lesson 40, and what does the code
report for reading hours versus total hours?**

<details>
<summary>Answer</summary>

18 lessons on the path: `[1, 10, 11, 12, 13, 14, 15, 30, 31, 32, 33, 34, 35, 36,
37, 38, 39, 40]` — the 17 from the closure plus the goal itself.

Reading time is 12.4 hours. Adding 60 minutes of exercises per lesson gives 30.4
hours. That factor of about 2.4 is the lesson's point about budgeting 60 to 90
minutes per lesson rather than the header's 25 to 50.

</details>

**Q3. The volume bound for 2570 minutes in 60-minute slots is 43 sessions, and
the lesson's greedy packer produces 59. Which bound is the right one to compare
against, and what is the true optimum?**

<details>
<summary>Answer</summary>

The volume bound, $\lceil 2570/60 \rceil = 43$, is a **relaxation and is
unreachable**: 51 of the 62 lessons are 40 minutes or longer, so most of them
cannot share a slot with anything.

The achievable bound comes from noticing that any pair summing to at most 60 must
contain a lesson of at most 30, and only 6 lessons are that short — at most 6
pairs. The two 30s cannot take a 35, which caps the pairing at 5.

So the true optimum is **57** sessions, and the greedy packer's **59** is within 2
of it. First-fit-decreasing reaches 57 exactly.

</details>

**Q4. Which four lessons does the `ALREADY_KNOWN = {21, 22, 50, 51}` skip set
actually save time on, out of the four goals priced in Exercise 2?**

<details>
<summary>Answer</summary>

Three of the four, partially. Goal 70 saves 95 minutes (1.6 h) — 50 and 51 are on
its path. Goal 92 saves 60 minutes (1.0 h) — 21 and 22 are on its path, and 50
and 51 are not. Goal 113 saves 60 minutes (1.0 h) — 21 and 22 are on its path.

Goal 40 saves **0 minutes**, because none of the four appears in
`all_prereqs(40) ∪ {40}`.

</details>

**Q5. What does the "most time on" row of the capability tracker report, and what
does the "highest capability" row report?**

<details>
<summary>Answer</summary>

Most time: **Proof Techniques**, 170 minutes, capability 4. That is the collapsed
record of the abandoned 30-minute attempt (capability 1) plus the 140-minute retry
(capability 4), with minutes summed and capability maximised.

Highest capability: **Why Mathematics Matters**, 45 minutes, capability 5 — the
tied-maximum case broken by least time.

</details>

**Q6. What probability does a pure guesser have of scoring 10 or more on the
20-question diagnostic, and what is the probability of 16 or more?**

<details>
<summary>Answer</summary>

10 or more: **58.8%** — better than even, since a guesser averages exactly 10.

16 or more: about **0.59%** — small but not negligible.

The asymmetry is the design insight: the thorough band is statistically
meaningful and the fast band is not.

</details>

### Long Answer

**Q1. The lesson argues that the prerequisite graph, not a topic list, is what
determines a study plan. Take the two most plausible-looking shortcuts a reader
might use instead, and show concretely — using the lesson's own graph and its
closure computation — that each one produces a wrong plan. Then say what general
property of the reader's situation makes the graph-based method the right one
even when the shortcuts look reasonable.**

<details>
<summary>Model answer</summary>

**Shortcut 1: follow the parts in order, skipping any part that "does not look
relevant".** This is the shortcut the lesson's second Common Mistake names, and
the reason it fails is visible in the closure computation. `all_prereqs(40)`
returns `{1, 10, 11, 12, 13, 14, 15, 30, …, 39}` — so Lesson 40's path contains
all six Part 01 lessons. The same holds for `all_prereqs(70)`, `all_prereqs(113)`
and `all_prereqs(121)`: every one of those closures begins with the identical
seven-element prefix `[1, 10, 11, 12, 13, 14, 15]`.

Why it *looks* reasonable: Part 01 contains no matrices, no gradients, no
probabilities. By topic, nothing in it connects to eigenvalue decomposition. The
reader has a genuine reason to think it is off the path, and the lesson concedes
the point — the connection is "not topical, it is structural".

Why it is wrong: Lesson 15 is a direct prerequisite of both Lesson 30 (the first
linear algebra lesson) and Lesson 60 (the first probability lesson). It is the
single node through which every downstream part passes. Skip it and you skip
every part, not one. And the failure is silent, which is the lesson's opening
observation: you will not get an error, you will simply stop following the
argument somewhere in the third linear algebra lesson, and you will not be able to
diagnose it then because the missing prerequisite is six lessons back.

**Shortcut 2: start from what you already know and work forward from the last
thing you understand.** This is the shortcut the "already know calculus" reader in
the Worked Example nearly takes, and Exercise 2 measures exactly what it costs.
With `ALREADY_KNOWN = {21, 22, 50, 51}`, goal 40 saves **0 minutes**. Not reduced
— unchanged. The reader knows two lessons that live in Part 02's chain and two in
Part 04's chain, and not one of them is on the path to 40, because the path runs
through Part 01 and then straight down the linear algebra chain.

Why it *looks* reasonable: it is the intuition behind every "fast track" ever
written. Prior experience is real capital, and the fastest route usually starts
where you already are.

Why it is wrong here: the graph is a *forest of chains sharing roots*, not a
single trunk. Experience in one subtree buys you nothing in a sibling subtree. The
lesson's general rule is that prior experience only shortens the path through the
lessons it actually satisfies, and you cannot know which those are without
computing the closure — which is exactly what `cost_to_reach` does, and exactly
why it applies the skip set *after* the closure rather than instead of it.

**Why the graph method is the right one in general.** Two properties of the
reader's situation make the alternatives unreliable, and both are stated in the
lesson.

The first is **silent failure**. A missing prerequisite produces no exception, no
failed test, no crash. It produces a reader who cannot follow a derivation and has
no idea why. Every shortcut here is a shortcut *around material whose absence is
invisible*, which is the worst possible category to self-assess. This is also why
the lesson insists on the diagnostic's `4–9` band meaning "start at Part 01": the
people who most need that advice are the people least able to detect needing it.

The second is that **the graph is the ground truth and the reader's intuition is a
hypothesis about it**. `study_order` is ~10 lines and reports
`prerequisite violations : 0`, which is a checkable statement. "Part 01 does not
look relevant" is not checkable, and when the two disagree the graph is right —
it is the artefact somebody maintained, and the intuition is a prediction about
it. The lesson's Step 7 is the honest summary: "You chose a track from a graph,
applied what you already had, and put the unfamiliar material on the critical
path."

The general form: when a dependency structure is *encoded* somewhere and the cost
of computing it is trivial, compute it. Optimising by intuition is only correct
when the structure is unencoded or the computation is expensive, and neither
condition holds for 62 lessons and a dictionary lookup.

</details>

**Q2. `make_sessions` produces 59 sessions. Show that the obvious bound of 43 is
unreachable, find the true optimum, show that the greedy packer is close to it,
and explain why the bound you reach first is the wrong one to report.**

<details>
<summary>Model answer</summary>

**The volume bound, and why it is wrong to stop there.** $\lceil 2570/60\rceil = 43$
comes from asking one question: do the minutes fit in 43 slots? They do, as a sum.
But minutes are not divisible, and the lesson lengths are clustered hard against
the slot size. The distribution over the 62 lessons is

    15 min:  2      25 min:  2      30 min:  2      35 min:  5
    40 min: 18      45 min: 23      50 min: 10

so 51 of 62 lessons are 40 minutes or longer, and the largest is 50. That single
fact determines everything: a 50-minute lesson can share a slot with *nothing*,
because the smallest lesson in the catalog is 15 minutes and $50 + 15 = 65 > 60$.
A 45- or 40-minute lesson can share with exactly one of the two 15s
($45 + 15 = 60$, $40 + 15 = 55$), and nothing else.

**The achievable bound.** Any pair of lessons summing to at most 60 must contain a
lesson of at most 30, because $35 + 35 = 70 > 60$. Only 6 lessons qualify (two
15s, two 25s, two 30s), so there can be at most 6 pairs, hence at least
$62 - 6 = 56$ sessions.

Then tighten by one. The two 30s cannot take a 35 ($30 + 35 = 65$), so they either
pair with each other ($30 + 30 = 60$, one pair) or each consume a 15 or 25 —
which means a partner is spent on a 30 and lost to the 35s. Counting both cases:
either the 30s pair together, giving at most one pair among the smalls plus
$2 \times 15$ used on bigs and $2 \times 25$ used on 35s, for 5 pairs; or they
each take a small, giving 2 pairs and leaving 25s unavailable, for at most 4. The
maximum is 5 pairs, so the optimum is $62 - 5 = \mathbf{57}$ sessions, and it is
achieved by the explicit pairing $15{+}40$, $15{+}40$, $25{+}35$, $25{+}35$,
$30{+}30$.

**How close the greedy packer actually is.** The lesson's `make_sessions` produces
**59**, so it is within **2** of optimal — wasting 970 minutes where 850 is
unavoidable. First-fit-decreasing, which sorts by length descending and never
considers order, reaches exactly 57, confirming the bound. So the packer is
approximately right, and the honest summary is that the 16-session "gap" against
the volume bound is almost entirely an artefact of an unachievable bound.

**Why the first bound is the wrong one to report — the general point.** The volume
bound is a *relaxation*: it forgets everything about the shape of the problem. Its
only content is the total, so it cannot distinguish 62 lessons of 41 minutes (which
pack at close to 43) from 62 lessons of 40 and 50 (which do not). Comparing a
result to a relaxation you have not shown to be attainable produces a number that
looks like an inefficiency and is not one. The lesson's own reporting discipline —
printing reading hours *and* total hours, printing the path *and* the count —
is the same instinct applied to scheduling: a single summary number is only
meaningful next to the right comparison.

**The tension the packer silently resolved.** And here the honest finding is that
the 2-session gap is not the interesting part. The interesting part is that this
packer is *not solving a packing problem at all*. Because 51 of 62 lessons are 40
minutes or longer, and the longest is 50, the number of sessions is forced close
to the number of big lessons no matter how you order them — which is exactly why
ascending, descending, longest-first, shortest-first and topological order all
return 59. The ordering decides only *which* small lessons get stranded, never how
many sessions there are. So there is no tension between compactness and order
here to resolve; the question is a red herring posed by a catalog whose lesson
lengths are too uniform to make packing interesting.

The tension that *is* real is between session length and fatigue. Packing to 60
minutes yields 59 sessions; packing to 120 minutes yields 29 sessions, at the
cost of two-hour sittings. The packer chose 60 implicitly by its default argument
and never said so, which is the genuine defect: not the 2-session gap, but an
unstated assumption about how long a reader can concentrate. Every scheduling
decision in this lesson rests on an unstated constant in that family — 45 minutes
of reading plus 60 of exercises, four sessions a week, one hour per slot — and
those constants, not the algorithm, are what the reader should be scrutinising.

</details>

**Q3. The diagnostic's scoring guide says a 10–15 score means "take the fast
track, then slow down on whatever you got right by luck rather than by
reasoning". A coin-flip guesser scores 10 on average and has a 58.8% chance of
10 or more, so the fast band is inside the guesser's range. Propose a better
scoring rule for the same 20 questions, show what it would do to the guesser, and
say what property any such rule must have to be worth anything at all.**

<details>
<summary>Model answer</summary>

**Why the current rule fails, precisely.** The band is a threshold on a total, and
the total is a sum of 20 independent two-sided items, so it is approximately
normal with mean 10 and standard deviation $\sqrt{20 \cdot 0.25} = 2.24$. A
threshold at 10 sits at the *mean* of that distribution, so about 58.8% of pure
guessers land in the fast band. The threshold at 16 sits about 2.7 standard
deviations up, where the guesser mass is 0.59%. The diagnostic is therefore
reliable at the top and worthless in the middle — and the middle is where most
readers land.

**A better rule, in three parts.**

**Part 1: weight the items by what they discriminate.** Not all 20 questions are
equally informative, and the current rule treats them identically. The three
Part 01 logic questions are *load-bearing* in a way the others are not, because
the lesson's own claim is that skipping Part 01 is the expensive mistake — a
reader who cannot distinguish `p → q` from `p ∧ q` has exactly the deficit that
makes the rest unreadable. Give those items weight 2, or better, make them
*gating*: a single failure on the negation question should force the "start at
Part 01" recommendation regardless of the total. This is the standard fix for a
test whose items have unequal diagnostic value, and it costs nothing.

**Part 2: require the fast band to be justified item by item.** Replace the
threshold with a two-part test: score 10–15 *and* correctly answer at least two
of the three Part 01 logic questions. A reader who scored 13 by genuinely knowing
probability and matrices, and who flubbed the quantifier-negation question, has a
specific and fixable gap; a reader who scored 13 with all three logic questions
wrong has a structural gap. Same total, different plans, and the total cannot tell
them apart.

**Part 3: report the score against its own null.** Print, alongside the total, the
probability that a guesser would score at least that much. 11 becomes
"P(≥ 11 by chance) ≈ 41%", which is a genuinely alarming number to see next to
your own 11, and 18 becomes "P ≈ 0.011%", which is genuinely reassuring. This
costs three lines and it converts the diagnostic from a verdict into a measurement
— the reader can now apply their own standard of evidence instead of the test
dictating one.

**What it does to the guesser.** A guesser fails Part 1 by construction: they
cannot reliably answer the gating questions, so they land in "start at Part 01"
regardless of how many coin flips went their way. Their maximum achievable score
under the new rule is the fast band, entered with an asterisk — and a reader who
reaches the fast band by reasoning is *not* subject to the asterisk, because the
gating questions are answerable by someone who knows the material. That asymmetry
is the entire point: the new rule is designed so that guessing is the *worst*
strategy rather than a roughly equally good one.

**What property makes any such rule worth having.** A scoring rule must be
**uninformative for the uninformative**. Concretely: if two readers are
indistinguishable in knowledge, they must be indistinguishable in score. The
current rule violates this because the guesser's most likely score, 10, is inside
the confident band. A rule earns its keep only if the expected score of a reader
with zero knowledge is *strictly below* the threshold for any recommendation other
than "start from the beginning" — and ideally, the expected score of an ideal
reader is strictly *above* every threshold, with no overlap in between.

This is the same shape as a test with low false-positive rate at the operating
point you care about, and the arithmetic above is the same arithmetic: you are
choosing thresholds on a sampling distribution whose width is fixed by the number
of items. You cannot fix it by adding more questions cheaply — going from 20 to
40 items only shrinks the standard deviation by $\sqrt{2}$, moving the 16-threshold
probability from 0.59% to about 0.02% while leaving the 10-threshold probability at
49%. The middle band is structurally insensitive to test length. If you want the
middle band to mean something, the items in it have to carry more information per
item, not more items.

The lesson's own instinct is right in its advice — slow down on what you got right
by luck — and the improved rule simply automates that advice instead of asking the
reader to supply it. That is the general form of every fix here: the score is a
summary, and a summary is only as good as the decision procedure built on top of
it.

</details>

**Q4. The capability tracker collapses retries by summing minutes and taking the
max of capability scores. Argue that this is the right choice, then find a case
where it is wrong. Then say what single change to the record would fix that case
without losing the property that makes the original rule safe.**

<details>
<summary>Model answer</summary>

**Why max is right.** The tracker measures what the exercise asked for: *the
fraction of the five-item checklist you can demonstrate.* Each of the five items
is a binary capability — you can solve an unlisted problem or you cannot — so
summing them across attempts would count the same capability twice, which is
meaningless. It would also make the score a function of how many times you
attempted a lesson, and the whole point of the tracker is that a retry is not
progress.

Summing the *minutes* is correct for the opposite reason: effort is genuinely
additive, and it is the number that reveals the pathology. The Challenge's own
analysis depends on it — 170 minutes at 4 points, giving 42.5 minutes per point,
is the row that diagnoses "I spent 30 minutes before I knew enough to start". Had
minutes been maximised too, that lesson would have read 140 minutes at 4 and the
signal would have vanished.

So the asymmetry is not arbitrary: **time is a resource that accumulates,
capability is a state that saturates.** Max is the correct aggregation for a
saturating state and sum for an accumulating resource.

**Where it is wrong.** Consider a lesson where the reader satisfies items 1, 2 and
5 on the first attempt, and items 3 and 4 after the exercises. The first attempt
scores 3, the second scores 5, and max gives 5 — which is right. Now consider the
reverse: the first attempt scores 5 because the reader worked through the
exercises *before* doing the checklist honestly, and the second attempt, done
properly from scratch a week later, scores 3. Max reports 5, but the honest
current state is 3.

The failure is that `max` assumes capability only ever grows. Retrying a lesson
can *lose* capability, in at least three real ways: the first attempt was
performed with the answer key or a solution visible; the material decayed before
the retry; or the reader performed the checklist items in an order that leaked
later items (item 1 phrased as a hint makes item 2 easy). In all three cases the
*first* number was inflated and the *later* number is the honest one. `max` keeps
the inflated value permanently.

**The single change that fixes it.** Record the capability of the **most recent**
attempt rather than the maximum — that is, change the collapse to take the *last*
record's capability while still summing the minutes. This keeps the property that
matters (a retry cannot inflate the score, because the score is a single
observation, not an accumulation) and it makes the score reflect the reader's
state *now*, which is the only thing a progress tracker is for.

That has a cost, and it is worth naming: last-attempt scoring makes the tracker
hostile to experimentation. If you try a lesson, score 1, and then come back and
score 4, last-attempt is right. If you score 4, then go study something else for a
week, then honestly retest and score 3 because you have decayed, last-attempt
records a regression for a lesson you genuinely have not lost. Max smooths that;
last-attempt reports it.

The honest resolution is that the two rules answer different questions, and the
record should carry both. Max answers "what is the best evidence I have ever
produced?" and is the right input for "is this lesson worth revisiting?". Last
answers "what can I do right now?" and is the right input for "should I move
on?". A tracker that reports only one of them is answering a question nobody
asked, which is a failure mode this repository keeps naming in a different guise:
a single summary number standing in for a distinction the reader actually needs.

</details>

**Q5. The lesson insists that reading time and total time must be reported
together — 12.4 hours versus 30.4 hours for Lesson 40's path — and that
big-O-style thinking does not apply to a study plan. Explain what a "complexity
analysis of a study plan" would mean, why the lesson is right that it is the wrong
tool, and what would actually go wrong if you planned by asymptotic estimate.**

<details>
<summary>Model answer</summary>

**What it would mean.** You would want a function of the goal's position in the
graph. The natural candidate is the size of the transitive closure, $|P(L)|$, which
for Lesson 40 is 17. A complexity-style claim would say: reading a goal costs
$O(|P(L)|)$ lessons, and if lessons in Part 01 cost $c_1$ and lessons in Part 03
cost $c_3$ then total time is $O(c_1 \cdot |P(L) \cap \text{Part 01}| + c_3 \cdot
|P(L) \cap \text{Part 03}|)$. That is a correct statement and it is completely
unhelpful.

**Why the lesson is right to reject it.** Three reasons, and they are the standard
reasons big-O is the wrong tool for planning.

*The constants are the whole answer.* Big-O deliberately discards constants,
because for algorithm comparison they are engineering details. For a study plan
they are the entire content: 12.4 hours versus 30.4 hours is a factor of 2.4
arising from one assumption — 60 minutes of exercises per lesson — and that
assumption is the decision. Big-O cannot represent a factor of 2.4; it is exactly
the kind of thing the notation is designed to discard.

*There is no asymptotic regime.* Big-O is a statement about $n \to \infty$. Nobody
is going to read 62 lessons, and there is no larger $n$ to extrapolate to. The
"complexity" of this plan is a fixed finite number of hours, and the correct
answer to "how long will this take" is arithmetic, not a bound.

*The graph has no regularity.* The closure sizes are not a smooth function of the
lesson number. `all_prereqs(24)` returns 10 lessons beyond the direct one;
`all_prereqs(40)` returns 17; `all_prereqs(113)` returns 11 and `all_prereqs(121)`
returns 15. A node's cost is set by which part it lives in, and the mapping from
lesson number to cost jumps around. A bound tight in $n$ would be tight over a
range where the actual values vary by a factor of two for no reason a reader could
predict. The lesson's own comparison makes this concrete: goal 70 needs 19 lessons
and 13.2 hours while goal 92 needs 19 lessons and 12.3 hours — same $n$, different
cost, because the *composition* of the closure differs.

**What would actually go wrong if you planned by asymptotic estimate.** The failure
is not a bad number; it is a decision that never gets made.

Estimating by closure size alone tells you goal 40 costs 18 lessons and goal 113
costs 14, so 113 looks cheaper. Exercise 2 confirms it is cheaper — 8.8 hours
against 12.4. The trap is that this comparison is *between two closure sizes* when
the decision is about *which subtree you will be living in afterwards*. Goal 113's
path is narrow: it goes through Part 02's combinatorics and Part 09's number
theory, and it teaches you nothing that feeds the parts you will actually work in.
Goal 70's path is 19 lessons and 13.2 hours, and the lesson's argument is that
information theory is the only idea in the catalog that pays out in compression,
in search ranking, in cross-validation, in alerting thresholds, and in log lines.

Neither of those is an asymptotic question, and no bound would ever answer it.
The quantity that decides the plan is the *number of downstream consumers*, which
is a different graph property entirely — the number of lessons that list a given
lesson as a prerequisite — and it has nothing to do with the size of any closure.

The same mistake appears in the `ALREADY_KNOWN = {21, 22, 50, 51}` result. The
asymptotic move is to note that a 62-lesson course minus 4 lessons is "basically
62 lessons", so the saving is negligible. True: goal 40 saves 0. But the reason it
saves 0 is *structural* — those four lessons are in sibling subtrees, not on the
path — and the structural reason is the thing worth knowing, because it tells you
that learning calculus has not advanced you toward eigenvalues by a single hour.

The general form is the lesson's own, in its first Common Mistake: big-O is about
growth, not milliseconds. Applied to a study plan, the question is not "how does
this scale" but "which of these finite options should I pick, and why". Those need
different instruments. Compute the graph, price it exactly, and then make the
value judgement — the last step is not computable and not pretending to be is the
point.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — Extend the catalog and verify the graph.**

**[ ] Exercise 2 — Price the tracks and compare.** Using the catalog, compute for
each of these goals: (a) the number of lessons that must be read, (b) the total
reading minutes, (c) the weeks required at four 60-minute sessions per week, and
(d) the same figures after excluding a set of lessons you already know. Do this
for goal 40 (SVD and PCA), goal 70 (Information Theory), goal 92 (Geometric
Algorithms), and goal 113 (Error-Correcting Codes). Then state which goal is
cheapest to reach, and why that is not the goal you should probably pick. Take
the "already known" set to be `{21, 22, 50, 51}`: counting and calculus are
familiar, proof is not.

<details>
<summary>Solution</summary>

```python
# number -> (title, reading minutes, direct prerequisites)
RAW = {
    0:   ("Why Mathematics Matters", 15, []),
    1:   ("How to Read Notation", 25, []),
    2:   ("Study Plan", 15, []),
    10:  ("Propositions and Connectives", 30, [1]),
    11:  ("Truth Tables and Equivalence", 40, [10]),
    12:  ("Predicates and Quantifiers", 40, [11]),
    13:  ("Proof Techniques", 45, [12]),
    14:  ("Mathematical Induction", 40, [13]),
    15:  ("Sets and Cardinality", 40, [14]),
    20:  ("Counting Principles", 35, [15]),
    21:  ("Permutations and Combinations", 35, [20]),
    22:  ("The Binomial Theorem", 25, [21]),
    23:  ("Inclusion-Exclusion and Pigeonhole", 40, [22]),
    24:  ("Recurrence Relations", 45, [23]),
    25:  ("Relations and Equivalence Classes", 40, [24]),
    26:  ("Graph Theory", 50, [25]),
    30:  ("Vectors and Vector Spaces", 40, [15]),
    31:  ("Matrices and Matrix Algebra", 45, [30]),
    32:  ("Linear Systems and Gaussian Elimination", 45, [31]),
    33:  ("Determinant and Inverse", 40, [32]),
    34:  ("Basis, Dimension, and Rank", 40, [33]),
    35:  ("Linear Transformations and Kernels", 45, [34]),
    36:  ("Eigenvalues and Eigenvectors", 50, [35]),
    37:  ("Inner Products, Norms, Geometry", 40, [36]),
    38:  ("Orthogonality and Least Squares", 45, [37]),
    39:  ("Diagonalization and Spectral Theory", 45, [38]),
    40:  ("SVD and PCA", 50, [39]),
    50:  ("Functions, Limits, Continuity", 45, [30]),
    51:  ("Derivatives", 50, [50]),
    52:  ("Integration", 50, [51]),
    60:  ("Probability Foundations", 35, [15]),
    61:  ("Probability Axioms and Rules", 40, [60]),
    62:  ("Conditional Probability and Bayes", 45, [61]),
    63:  ("Discrete Random Variables", 40, [62]),
    64:  ("Expectation and Variance", 45, [63]),
    68:  ("Law of Large Numbers and CLT", 50, [64, 52]),
    69:  ("Estimation and Hypothesis Testing", 50, [64, 68]),
    70:  ("Information Theory and Entropy", 40, [64, 69]),
    90:  ("Vectors in 3D and Cross Product", 35, [30]),
    91:  ("Transformations for Graphics", 45, [90, 31]),
    92:  ("Geometric Algorithms", 45, [91, 26]),
    110: ("Number Theory", 45, [21, 23]),
    111: ("Modular Arithmetic and Crypto", 45, [110]),
    113: ("Error-Correcting Codes", 40, [111, 22]),
}

PREREQS = {n: RAW[n][2] for n in RAW}
MINUTES = {n: RAW[n][1] for n in RAW}
TITLES = {n: RAW[n][0] for n in RAW}


def all_prereqs(number):
    """Transitive closure of the prerequisite relation."""
    seen, stack = set(), list(PREREQS[number])
    while stack:
        current = stack.pop()
        if current not in seen:
            seen.add(current)
            stack.extend(PREREQS[current])
    return seen


# Someone with a CS degree: counting and calculus are familiar, proof is not.
ALREADY_KNOWN = {21, 22, 50, 51}


def cost_to_reach(goal, skip=frozenset()):
    """Lessons to read to reach `goal`, and their total reading minutes."""
    needed = (all_prereqs(goal) | {goal}) - set(skip)
    return sorted(needed), sum(MINUTES[n] for n in needed)


GOALS = [40, 70, 92, 113]
print(f"{'goal':>5} {'lessons':>8} {'hours':>7} {'weeks@4':>9}   "
      f"{'after skipping known':>26}")
print("-" * 74)
results = {}
for goal in GOALS:
    full, full_min = cost_to_reach(goal)
    trimmed, trim_min = cost_to_reach(goal, ALREADY_KNOWN)
    results[goal] = (full, full_min, trimmed, trim_min)
    print(f"{goal:>5} {len(full):>8} {full_min / 60:>7.1f} {full_min / 240:>9.1f}"
          f"   {len(trimmed):>5} lessons, {trim_min / 60:>4.1f} h")
print()

for goal in GOALS:
    full, full_min, trimmed, trim_min = results[goal]
    saved = full_min - trim_min
    print(f"goal {goal:>3} ({TITLES[goal]}):")
    print(f"  full path : {full}")
    print(f"  after skip: {trimmed}")
    print(f"  saving    : {saved} min ({saved / 60:.1f} h)")
print()

cheapest = min(GOALS, key=lambda g: results[g][1])
print(f"cheapest goal to reach: {cheapest} ({TITLES[cheapest]})")
print()
print("And that is not the goal to pick. Cost to reach is not value of reaching.")
print("Goal 92 is cheap because geometry reuses linear algebra and graph theory.")
print("Goal 70 is expensive because probability, calculus and estimation all")
print("feed it, but information theory is the most reusable idea in the list:")
print("it shows up in compression, in search, in model selection, in every")
print("monitoring dashboard, and in every 'how surprising was that' log line.")
print("Pick by what you will use, not by what is quick to arrive at.")
```

Output (lesson counts and hours are deterministic):

```
 goal  lessons   hours   weeks@4         after skipping known
--------------------------------------------------------------------------
   40       18    12.4       3.1      18 lessons, 12.4 h
   70       19    13.2       3.3      17 lessons, 11.6 h
   92       19    12.3       3.1      17 lessons, 11.3 h
  113       14     8.8       2.2      12 lessons,  7.8 h

goal  40 (SVD and PCA):
  full path : [1, 10, 11, 12, 13, 14, 15, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
  after skip: [1, 10, 11, 12, 13, 14, 15, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
  saving    : 0 min (0.0 h)
goal  70 (Information Theory and Entropy):
  full path : [1, 10, 11, 12, 13, 14, 15, 30, 50, 51, 52, 60, 61, 62, 63, 64, 68, 69, 70]
  after skip: [1, 10, 11, 12, 13, 14, 15, 30, 52, 60, 61, 62, 63, 64, 68, 69, 70]
  saving    : 95 min (1.6 h)
goal  92 (Geometric Algorithms):
  full path : [1, 10, 11, 12, 13, 14, 15, 20, 21, 22, 23, 24, 25, 26, 30, 31, 90, 91, 92]
  after skip: [1, 10, 11, 12, 13, 14, 15, 20, 23, 24, 25, 26, 30, 31, 90, 91, 92]
  saving    : 60 min (1.0 h)
goal 113 (Error-Correcting Codes):
  full path : [1, 10, 11, 12, 13, 14, 15, 20, 21, 22, 23, 110, 111, 113]
  after skip: [1, 10, 11, 12, 13, 14, 15, 20, 23, 110, 111, 113]
  saving    : 60 min (1.0 h)

cheapest goal to reach: 113 (Error-Correcting Codes)
```

Three results worth reading twice.

Goal 40 saves **nothing**, despite knowing calculus and counting. None of its
prerequisites happen to be in `ALREADY_KNOWN`. Proving you remember calculus does
not shorten the road to eigenvalues, because eigenvalues need the linear algebra
chain and the whole of Part 01.

Goal 113 is the cheapest at 8.8 hours, dropping to 7.8 once the counting lessons
go. It is also the narrowest. Error-correcting codes matter enormously if you work
on storage, RAID, or QUIC, and not at all otherwise.

Goal 70 is the most expensive and the most reusable. Information theory is the
only idea in this list that pays out in compression, in search ranking, in
cross-validation, in every alerting threshold, and in every log line that says
"how surprising was this". If you can only pick one track, pick by what you will
use in the next two years, not by what is fastest to arrive at.

</details>

**[ ] Exercise 3 — Write your own contract for "I have finished a lesson".** A
study plan fails the same way every time: it defines progress as *finished
reading*, which is not progress. Write a five-item checklist for "I have finished
Lesson N" where every item is something you can **do**, not something you have
**seen**. Then apply the checklist to Lesson 11 of this course (Truth Tables and
Equivalence) and report honestly which items you could satisfy after only
reading, and which needed the exercises. Be specific about item 4, which is the
one most people cannot satisfy by reading.

<details>
<summary>Solution</summary>

**The checklist.** Five items, each a capability rather than an exposure:

1. **You can state the central claim of the lesson in one sentence, using no
   notation from the lesson.** "Two formulas are logically equivalent when they
   agree on every input, and that lets you rewrite a condition without changing
   what it does" — not "it covers truth tables". If you cannot compress it to a
   sentence, you have not identified what the lesson is for.

2. **You can run every code block and explain what each printed number means.**
   Not that it ran. That you can say why the loop and the closed form both print
   `338350` for `n = 100`, and why the DNF printer reports 3 terms and 5 literals.

3. **You can produce the smallest counterexample to a claim in the lesson, or
   state that no counterexample exists.** This is a test of understanding, not
   recall. Finding one is worth less than building it.

4. **You can solve a problem in the lesson's area that is not in the lesson.**
   This is the item that fails on reading alone. It requires building something
   the lesson never showed you, and it is the only item that demonstrates
   transfer rather than retention.

5. **You can name a later lesson that depends on this one, and say why.** If you
   cannot name a downstream consumer, you cannot tell whether you actually needed
   this lesson, and you will not know when the gap will bite.

**Applying it to Lesson 11.**

| Item | After reading only? | Notes |
| --- | --- | --- |
| 1. One-sentence claim, no notation | Yes | Equivalence means agreement on every input, which licenses rewriting code. |
| 2. Explain every printed value | Mostly | Needs one more pass over the DNF printer. The counts 3 terms and 5 literals are checkable by hand, but only if you actually check them. |
| 3. Build a counterexample | No | Requires building it, not finding one in the prose. |
| 4. Solve an unlisted problem | **No** | The item that fails. |
| 5. Name a downstream consumer | Yes | Lesson 12 needs negation of compound formulas. Lesson 82 uses DNF for symbolic pruning in search. |

**Item 4, in detail.** Every exercise in Lesson 11 is shaped like Lesson 11.
Item 4 asks for something else: given a boolean formula over `n` variables,
search for the *shortest* formula computing the same function. Nothing in the
lesson does that. It requires noticing that a truth table is a finite object you
can enumerate over, which is the lesson's actual content put into a new shape.

```python
import itertools


def truth_column(formula, variables):
    """The output of `formula` for every assignment to `variables`, in order."""
    assignments = itertools.product([0, 1], repeat=len(variables))
    return [int(formula(*values)) for values in assignments]


# An awkward formula for "at least two of a, b, c are true".
def at_least_two(a, b, c):
    return (a and b) or (a and c) or (b and c)


# A shorter one computing exactly the same function.
def at_least_two_short(a, b, c):
    return (a + b + c) >= 2


print("assignments            :", list(itertools.product([0, 1], repeat=3)))
print("awkward formula column :", truth_column(at_least_two, "abc"))
print("short  formula column  :", truth_column(at_least_two_short, "abc"))
print("they agree             :",
      truth_column(at_least_two, "abc") == truth_column(at_least_two_short, "abc"))
print()
print("Searching over all formulas is a finite problem, because the truth")
print("table is finite. That is the lesson's idea, applied somewhere the")
print("lesson never went.")
```

Output:

```
assignments            : [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
awkward formula column : [0, 0, 0, 1, 0, 1, 1, 1]
short  formula column  : [0, 0, 0, 1, 0, 1, 1, 1]
they agree             : True

Searching over all formulas is a finite problem, because the truth
table is finite. That is the lesson's idea, applied somewhere the
lesson never went.
```

The honest summary: after reading Lesson 11 you could satisfy items 1, 2 and 5,
and you can probably satisfy item 3 now that you have been asked. Item 4 you
could not. That is not a flaw in the lesson; it is the lesson doing its job. It
is also why the header says 40 minutes when the prose might take 20 to read.

</details>

**[ ] Challenge 4 — Build a tracker that measures progress by capability, not by
pages
read.** Write a program that keeps a per-lesson record with two fields: minutes
spent, and the number of checklist items from Exercise 3 you satisfied (0 to 5).
Compute a "real progress" score defined as the total capability points earned
divided by the total possible, and compare it against a naive "hours read"
score. Then report which lesson you spent the most time on and which gave the
highest capability score, and explain what a divergence between the two rankings
means about where your time went. Include at least one lesson you abandoned and
later retried, so the retry behaviour is visible.

<details>
<summary>Solution</summary>

```python
class Record:
    """Minutes spent on one attempt at one lesson, and what it earned."""

    def __init__(self, number, title, minutes, capability):
        self.number = number
        self.title = title
        self.minutes = minutes
        self.capability = capability     # 0..5 from the Exercise 3 checklist

    def __repr__(self):
        return f"Record({self.number}, {self.title!r}, {self.minutes}, " \
               f"{self.capability})"


# A plausible history: some lessons long and easy, one abandoned and retried.
LOG = [
    Record(0,  "Why Mathematics Matters", 45, 5),
    Record(1,  "How to Read Notation", 120, 5),
    Record(10, "Propositions and Connectives", 95, 4),
    Record(11, "Truth Tables and Equivalence", 150, 5),
    Record(12, "Predicates and Quantifiers", 40, 2),      # skimmed, then regretted
    Record(13, "Proof Techniques", 30, 1),                # got stuck, abandoned
    Record(13, "Proof Techniques", 140, 4),               # retried and finished
    Record(14, "Mathematical Induction", 110, 3),
    Record(15, "Sets and Cardinality", 85, 4),
    Record(20, "Counting Principles", 70, 4),
]

# Collapse retries: time is summed, capability is the best single attempt.
by_lesson = {}
for r in LOG:
    prev = by_lesson.get(r.number)
    if prev is None:
        by_lesson[r.number] = r
    else:
        by_lesson[r.number] = Record(r.number, r.title,
                                     prev.minutes + r.minutes,
                                     max(prev.capability, r.capability))

records = sorted(by_lesson.values(), key=lambda r: r.number)
total_minutes = sum(r.minutes for r in records)
total_capability = sum(r.capability for r in records)
max_capability = 5 * len(records)

print(f"lessons attempted        : {len(records)}")
print(f"minutes spent            : {total_minutes}")
print(f"capability points earned : {total_capability} of {max_capability}")
print(f"naive score              : {total_minutes / 60:.1f} hours read")
print(f"real score               : {total_capability / max_capability * 100:.0f}% "
      f"of the checklist satisfied")
print()

print(f"{'lesson':<28} {'min':>5} {'cap':>4} {'min/point':>10}")
print("-" * 50)
for r in sorted(records, key=lambda r: -r.minutes):
    print(f"{r.title:<28} {r.minutes:>5} {r.capability:>4} "
          f"{r.minutes / max(r.capability, 1):>10.1f}")

most_time = max(records, key=lambda r: r.minutes)
best_cap = max(records, key=lambda r: (r.capability, -r.minutes))
print()
print(f"most time on        : {most_time.title} "
      f"({most_time.minutes} min, capability {most_time.capability})")
print(f"highest capability  : {best_cap.title} "
      f"({best_cap.minutes} min, capability {best_cap.capability})")
print()

worst = sorted(records, key=lambda r: -(r.minutes / max(r.capability, 1)))[:3]
print("worst minutes per capability point:")
for r in worst:
    print(f"  {r.title:<28} {r.minutes / max(r.capability, 1):>6.1f}")
print()
print("Reading this table")
print()
print("If the two rankings agree, your time is going where the learning is, and")
print("you are on the fast track. If a lesson ranks high on minutes and low on")
print("capability, you are re-reading rather than practising, which feels like")
print("progress and is not. That is the single most common failure mode of")
print("self-directed study, and it is invisible unless capability is tracked")
print("separately from time.")
print()
print("A lesson scoring 4+ points in under 100 minutes is a good one to revisit")
print("before an interview. A lesson at 2 or below after 100 minutes is a lesson")
print("to go back and re-plan, not to read again.")
```

Output:

```
lessons attempted        : 9
minutes spent            : 885
capability points earned : 36 of 45
naive score              : 14.8 hours read
real score               : 80% of the checklist satisfied

lesson                         min  cap  min/point
--------------------------------------------------
Proof Techniques               170    4       42.5
Truth Tables and Equivalence   150    5       30.0
How to Read Notation           120    5       24.0
Mathematical Induction         110    3       36.7
Propositions and Connectives    95    4       23.8
Sets and Cardinality            85    4       21.2
Counting Principles             70    4       17.5
Why Mathematics Matters         45    5        9.0
Predicates and Quantifiers      40    2       20.0

most time on        : Proof Techniques (170 min, capability 4)
highest capability  : Why Mathematics Matters (45 min, capability 5)

worst minutes per capability point:
  Proof Techniques               42.5
  Mathematical Induction         36.7
  Truth Tables and Equivalence   30.0
```

Proof Techniques is the interesting row. It has both the most time *and* a
respectable capability score of 4, and it is also the worst possible ratio at 42.5
minutes per point. Those are consistent, not contradictory: proof is genuinely the
hardest lesson in Part 01 and it deserved 170 minutes. But the ratio says the time
was badly *ordered*, not badly spent. The diagnosis to act on is not "proof is too
hard", it is "I spent 30 minutes on Proof Techniques before I knew enough to start
it" — the abandoned attempt, sitting in the log as a separate record with
capability 1. Reordering would have cost nothing and saved 30 minutes.

Compare the two ends of the minutes column. Why Mathematics Matters took 45
minutes and scored 5 out of 5, at 9.0 minutes per point. Predicates and
Quantifiers took 40 minutes and scored 2 out of 5, at 20.0 minutes per point. By
hours read they look comparable. By capability they are not comparable at all, and
only one of them was worth the time.



**[ ] Exercise 5 — Prove the achievable session bound, and beat the lesson's
packer.** Using only `MINUTES` (read them out of the catalog the lesson's code
builds), do all of the following.

1. Print the length distribution of the 62 lessons.
2. Compute the volume bound `ceil(total / 60)` and explain in one sentence why it
   is not attainable.
3. Compute the achievable lower bound from the observation that any pair summing
   to at most 60 must contain a lesson of at most 30. Tighten it by noting the two
   30s cannot take a 35. Report the true optimum.
4. Implement first-fit-decreasing and confirm it reaches the optimum. Report how
   many sessions the lesson's greedy `make_sessions` uses and the gap.
5. Run the greedy packer over four different orderings — ascending, descending,
   longest-first, shortest-first — and report the session count for each. Then
   explain why they agree, in terms of the length distribution.

<details>
<summary>Solution</summary>

```python
from collections import Counter
from math import ceil

# The lesson's own catalog, reduced to what the packer needs.
MINUTES = {
    0: 15, 1: 25, 2: 15, 10: 30, 11: 40, 12: 40, 13: 45, 14: 40, 15: 40,
    20: 35, 21: 35, 22: 25, 23: 40, 24: 45, 25: 40, 26: 50, 27: 45, 28: 30,
    30: 40, 31: 45, 32: 45, 33: 40, 34: 40, 35: 45, 36: 50, 37: 40, 38: 45,
    39: 45, 40: 50, 41: 35, 50: 45, 51: 50, 52: 50, 53: 50, 54: 45, 55: 50,
    60: 35, 61: 40, 62: 45, 63: 40, 64: 45, 65: 40, 66: 45, 67: 45, 68: 50,
    69: 50, 70: 40, 80: 50, 81: 40, 82: 45, 90: 35, 91: 45, 92: 45,
    100: 40, 101: 45, 102: 45, 110: 45, 111: 45, 112: 40, 113: 40,
    120: 45, 121: 45,
}
CAP = 60
TOTAL = sum(MINUTES.values())
print(f"lessons: {len(MINUTES)}   total reading: {TOTAL} min   slot: {CAP} min")
print()

# 1. The length distribution.
dist = Counter(MINUTES.values())
print("== 1. length distribution ==")
for length in sorted(dist):
    print(f"   {length:>3} min : {dist[length]:>2} lessons")
big = sum(1 for v in MINUTES.values() if v >= 40)
print(f"   {big} of {len(MINUTES)} lessons are 40 min or longer "
      f"({100 * big / len(MINUTES):.0f}%)")
print(f"   longest lesson: {max(MINUTES.values())} min;  "
      f"shortest: {min(MINUTES.values())} min")
print()

# 2. The volume bound, and why it is not attainable.
volume = ceil(TOTAL / CAP)
print("== 2. the volume bound ==")
print(f"   ceil({TOTAL} / {CAP}) = {volume}")
print(f"   but a {max(MINUTES.values())}-min lesson plus the shortest lesson in the "
      f"catalog is {max(MINUTES.values())} + {min(MINUTES.values())} = "
      f"{max(MINUTES.values()) + min(MINUTES.values())} > {CAP},")
print("   so the longest lessons cannot share a slot with anything. The bound")
print("   assumes minutes are divisible; they are not.")
print()

# 3. The achievable bound.
print("== 3. the achievable bound ==")
SMALL = 30          # 35 + 35 = 70 > 60, so every pair contains a lesson <= 30
small_lessons = [k for k, v in MINUTES.items() if v <= SMALL]
print(f"   any pair summing to <= {CAP} must contain a lesson <= {SMALL} "
      f"(35+35 = 70 > 60)")
print(f"   lessons of {SMALL} min or under: {len(small_lessons)} "
      f"{[MINUTES[k] for k in sorted(small_lessons, key=lambda k: MINUTES[k])]}")
print(f"   => at most {len(small_lessons)} pairs, so at least "
      f"{len(MINUTES) - len(small_lessons)} sessions")

# Tighten: the 30s cannot take a 35, so spending a small on a 30 loses a partner.
thirties = [k for k, v in MINUTES.items() if v == 30]
print(f"   but {SMALL} + 35 = {SMALL + 35} > {CAP}, so each 30 either pairs with the")
print(f"   other 30 ({thirties} -> 1 pair) or consumes a 15/25, losing a partner")
print(f"   for a 35. Either way at most 5 pairs, so the optimum is "
      f"{len(MINUTES) - 5} sessions.")
print()

# 4. First-fit-decreasing reaches it.
def first_fit_decreasing(table, cap):
    """Longest lesson first, each into the first session with room for it."""
    sessions = []
    for number in sorted(table, key=lambda n: -table[n]):
        for session in sessions:
            if sum(table[m] for m in session) + table[number] <= cap:
                session.append(number)
                break
        else:
            sessions.append([number])
    return sessions


def greedy_in_order(table, order, cap):
    """The lesson's make_sessions: walk in order, never revisit a closed session."""
    sessions, current, used = [], [], 0
    for number in order:
        if used + table[number] > cap and current:
            sessions.append(current)
            current, used = [], 0
        current.append(number)
        used += table[number]
    if current:
        sessions.append(current)
    return sessions


OPTIMUM = len(MINUTES) - 5
ffd = first_fit_decreasing(MINUTES, CAP)
greedy = greedy_in_order(MINUTES, sorted(MINUTES), CAP)
waste = lambda ss: sum(CAP - sum(MINUTES[n] for n in s) for s in ss)
print("== 4. first-fit-decreasing versus the lesson's greedy ==")
print(f"   achievable optimum    : {OPTIMUM} sessions")
print(f"   first-fit-decreasing  : {len(ffd):>2} sessions   "
      f"waste {waste(ffd):>3} min   matches optimum: {len(ffd) == OPTIMUM}")
print(f"   lesson's greedy       : {len(greedy):>2} sessions   "
      f"waste {waste(greedy):>3} min   gap {len(greedy) - OPTIMUM}")
print(f"   slots used by greedy  : {len(greedy)} of "
      f"{len(greedy) * CAP} available minutes "
      f"({100 * TOTAL / (len(greedy) * CAP):.0f}% full)")
print(f"   greedy sessions with one lesson: "
      f"{sum(1 for s in greedy if len(s) == 1)} of {len(greedy)}")
print(f"   FFD sessions with two lessons  : "
      f"{sum(1 for s in ffd if len(s) == 2)}")
print()

# 5. Four orderings, all giving the same answer.
print("== 5. does the input order matter? ==")
orders = {
    "ascending lesson number": sorted(MINUTES),
    "descending lesson number": sorted(MINUTES, reverse=True),
    "longest first": sorted(MINUTES, key=lambda n: -MINUTES[n]),
    "shortest first": sorted(MINUTES, key=lambda n: MINUTES[n]),
}
for label, order in orders.items():
    sessions = greedy_in_order(MINUTES, order, CAP)
    print(f"   {label:<24}: {len(sessions)} sessions")
print()
print("All four agree because the distribution is so concentrated. With 51 of 62")
print("lessons at 40 min or longer, almost every session holds exactly one, so")
print("the ordering decides WHICH small lessons get stranded, never HOW MANY")
print("sessions there are. Reordering is not a fix here.")
print()
print("The 2-session gap is also the honest limit: 5 pairs is the most this")
print("distribution allows, so 57 is optimal and greedy's 59 is near-best.")
print("The lesson's real unstated choice was cap = 60, not the algorithm. At")
for cap in (90, 120, 150):
    ss = greedy_in_order(MINUTES, sorted(MINUTES), cap)
    print(f"   cap {cap:>3}: {len(ss):>2} sessions, "
          f"{len(MINUTES) / len(ss):.1f} lessons each")
print("Packing tighter buys fewer sittings at the cost of longer ones.")
```

Output:

```
lessons: 62   total reading: 2570 min   slot: 60 min

== 1. length distribution ==
    15 min :  2 lessons
    25 min :  2 lessons
    30 min :  2 lessons
    35 min :  5 lessons
    40 min : 18 lessons
    45 min : 23 lessons
    50 min : 10 lessons
   51 of 62 lessons are 40 min or longer (82%)
   longest lesson: 50 min;  shortest: 15 min

== 2. the volume bound ==
   ceil(2570 / 60) = 43
   but a 50-min lesson plus the shortest lesson in the catalog is 50 + 15 = 65 > 60,
   so the longest lessons cannot share a slot with anything. The bound
   assumes minutes are divisible; they are not.

== 3. the achievable bound ==
   any pair summing to <= 60 must contain a lesson <= 30 (35+35 = 70 > 60)
   lessons of 30 min or under: 6 [15, 15, 25, 25, 30, 30]
   => at most 6 pairs, so at least 56 sessions
   but 30 + 35 = 65 > 60, so each 30 either pairs with the
   other 30 ([10, 28] -> 1 pair) or consumes a 15/25, losing a partner
   for a 35. Either way at most 5 pairs, so the optimum is 57 sessions.

== 4. first-fit-decreasing versus the lesson's greedy ==
   achievable optimum    : 57 sessions
   first-fit-decreasing  : 57 sessions   waste 850 min   matches optimum: True
   lesson's greedy       : 59 sessions   waste 970 min   gap 2
   slots used by greedy  : 59 of 3540 available minutes (73% full)
   greedy sessions with one lesson: 57 of 59
   FFD sessions with two lessons  : 5

== 5. does the input order matter? ==
   ascending lesson number : 59 sessions
   descending lesson number: 59 sessions
   longest first           : 59 sessions
   shortest first          : 59 sessions

All four agree because the distribution is so concentrated. With 51 of 62
lessons at 40 min or longer, almost every session holds exactly one, so
the ordering decides WHICH small lessons get stranded, never HOW MANY
sessions there are. Reordering is not a fix here.

The 2-session gap is also the honest limit: 5 pairs is the most this
distribution allows, so 57 is optimal and greedy's 59 is near-best.
The lesson's real unstated choice was cap = 60, not the algorithm. At
   cap  90: 34 sessions, 1.8 lessons each
   cap 120: 29 sessions, 2.1 lessons each
   cap 150: 20 sessions, 3.1 lessons each
Packing tighter buys fewer sittings at the cost of longer ones.
```

**Why the volume bound fails.** It asks whether the *sum* of the lengths fits in 43
slots, and it does — 43 × 60 = 2580 ≥ 2570. But no actual packing achieves it,
because the longest lesson in the catalog is 50 minutes and the shortest is 15, so
$50 + 15 = 65 > 60$: a 50-minute lesson cannot share with anything. All 10
fifty-minute lessons are therefore alone, and so are nearly all of the 23
forty-fives. The bound is a relaxation that discards the distribution, and it is
unattainable.

**Why 57 is the true optimum.** Any pair summing to at most 60 contains a lesson of
at most 30, since $35 + 35 = 70$. Only 6 lessons are that short, so at most 6 pairs
exist and at least 56 sessions are needed. The tightening: $30 + 35 = 65$, so each
30-minute lesson either pairs with the *other* 30 (Lessons 10 and 28, one pair) or
spends a 15 or 25 that a 35 could otherwise have used. Spending on a 30 yields
`30+30`, `15+40`, `15+40` = 3 pairs; the alternative `15+45`, `15+45`, `25+35`,
`25+35` = 4 pairs plus no 30-pair = 4. The maximum is 5, achieved by
`15+40`, `15+40`, `25+35`, `25+35`, `30+30`, giving $62 - 5 = 57$.

**How the packers compare.** First-fit-decreasing reaches 57, exactly the proved
optimum — a useful confirmation that the bound is right rather than merely
plausible. The lesson's greedy packer uses 59 and fills its slots to 73%, with 57
of its 59 sessions holding a single lesson. So the packer is **within 2 of optimal**,
and the 970 minutes it wastes over the unavoidable 850 is a real but small defect.

**Why the orderings agree.** With 51 of 62 lessons at 40 minutes or longer, almost
every session holds exactly one lesson whatever the order, and the count is pinned
by the number of big lessons. The ordering only decides which 5 small lessons find
partners and which 4 are stranded. This is worth noticing because the reflex is to
blame the input order: reordering is the first thing a reader would try, and here
it changes nothing at all.

**The actual finding.** The lesson's `make_sessions` is close to right, and the
2-session gap is not the interesting number. The interesting number is the one
printed last: the packer's real decision was `slot_minutes=60`, and that default was
never stated. At 120 minutes the same catalog fits in 29 sittings instead of 59.
Whether that is better is a question about concentration, not about algorithms, and
the code cannot answer it — which is exactly the kind of unstated constant the
lesson warns about in its fifth Common Mistake, showing up in its own code.

</details>

**[ ] Exercise 6 — Audit the diagnostic's scoring bands against the null
hypothesis.** (a) Compute the probability that a reader who answers every question
by coin flip scores 10 or more, and 16 or more. (b) Report which scoring bands
those probabilities fall inside, and state what fraction of pure guessers lands in
each band. (c) Compute the expected score and standard deviation of a guesser, and
show that the guesser's most likely single score is inside the "fast track" band.
(d) Then design a better rule using only the 20 questions and no new ones: give the
three Part 01 logic questions weight 2 and make them gating (a single failure
forces "start at Part 01"), and report what a guesser scores under the new rule.

<details>
<summary>Solution</summary>

```python
from math import comb, sqrt
from itertools import product

QUESTIONS = 20


def binom_tail(k, n=QUESTIONS, p=0.5):
    """P(at least k successes) for n fair trials."""
    return sum(comb(n, i) * p ** n for i in range(k, n + 1))


# --- (a) the null distribution of a pure guesser.
expected = QUESTIONS / 2
sigma = sqrt(QUESTIONS * 0.25)
print("== (a) and (c) a coin-flip guesser ==")
print(f"   expected score   : {expected}")
print(f"   standard dev     : {sigma:.3f}")
print(f"   most likely score: {int(expected)}  "
      f"(that is the middle of the distribution)")
print(f"   P(score >= 10)   : {binom_tail(10) * 100:.1f}%")
print(f"   P(score >= 16)   : {binom_tail(16) * 100:.4f}%")
print(f"   P(score >= 4)    : {binom_tail(4) * 100:.1f}%")
print(f"   P(score >= 20)   : {binom_tail(20) * 100:.7f}%")
print(f"   P(20 correct)    : {0.5 ** 20 * 100:.6f}%")
print()

# --- (b) which bands is the guesser inside?
BANDS = [("thorough", 16, 20), ("fast", 10, 15), ("Part 01", 4, 9),
         ("Part 00", 0, 3)]
print("== (b) the bands, measured against the guesser ==")
print(f"{'band':<10} {'range':>7} {'P(guesser lands here)':>24}  verdict")
for name, lo, hi in BANDS:
    # P(lo <= X <= hi) = P(X >= lo) - P(X >= hi + 1)
    inside = binom_tail(lo) - binom_tail(hi + 1)
    if inside > 0.10:
        verdict = "USELESS as a signal"
    elif inside > 0.01:
        verdict = "weak"
    else:
        verdict = "informative"
    print(f"{name:<10} {f'{lo}-{hi}':>7} {inside * 100:>23.2f}%  {verdict}")
print()
print("The fast band is the guesser's home. A reader who scored 11 and admitted")
print("guessing has told you nothing you did not already know.")
print()

# --- (d) a better rule: weight the Part 01 logic questions, and gate on them.
WEIGHTS = [1] * QUESTIONS
GATING = {0, 1, 2}          # indices of the three Part 01 logic questions
for i in GATING:
    WEIGHTS[i] = 2
MAX_WEIGHTED = sum(WEIGHTS)


def weighted_score(correct):
    return sum(WEIGHTS[i] for i in correct)


def rule(correct):
    """correct is a set of indices the reader got right."""
    gating = len(GATING & correct)
    total = weighted_score(correct)
    fraction = total / MAX_WEIGHTED
    if gating < len(GATING):
        # One failure on a Part 01 logic question forces the Part 01 advice.
        return f"Part 01 (gated: {gating}/3 logic, {total}/{MAX_WEIGHTED} weighted)"
    if fraction >= 0.80:
        return f"thorough ({total}/{MAX_WEIGHTED} = {fraction:.0%})"
    if fraction >= 0.60:
        return f"fast ({total}/{MAX_WEIGHTED} = {fraction:.0%})"
    return f"fast, but review gaps ({total}/{MAX_WEIGHTED} = {fraction:.0%})"


print("== (d) the improved rule ==")
print(f"   weighted maximum : {MAX_WEIGHTED} (the three logic items count double)")
print()

# A guesser: every subset of size k is equally likely, so enumerate them.
for k in (10, 11, 13, 16, 18, 20):
    counts = {}
    for subset in product((0, 1), repeat=QUESTIONS):
        if sum(subset) != k:
            continue
        correct = {i for i, v in enumerate(subset) if v}
        label = rule(correct).split(" (")[0]
        counts[label] = counts.get(label, 0) + 1
    best = max(counts, key=counts.get)
    print(f"   a guesser scoring {k:>2}: most likely recommendation -> {best}")

# Reaching 'thorough' needs all 3 gating items right AND >= 0.80 of the weight,
# i.e. 6 + 13 of the remaining 17. So the guesser's false-positive rate there is
# 0.5**3 * P(Bin(17, 0.5) >= 13).
need = 13
new_fp = 0.5 ** 3 * sum(comb(17, i) * 0.5 ** 17 for i in range(need, 18))
old_fp = binom_tail(16)
print()
print("P(guesser gets all 3 gating items right) =", f"{0.5 ** 3 * 100:.1f}%")
print("P(guesser is told 'thorough')            =", f"{new_fp * 100:.4f}%")
print(f"P(guesser was told 'thorough') before   = {old_fp * 100:.4f}%")
print(f"   a {old_fp / new_fp:.1f}x tightening, from {1 / old_fp:.0f}-in-1 to")
print(f"   {1 / new_fp:.0f}-in-1, bought by making three questions load-bearing.")
print()
print("Why only 2x, and not the 8x the gating alone would suggest: the gating")
print("factor 0.5**3 = 0.125 is multiplied by P(Bin(17,0.5) >= 13) = 0.245, and")
print("that second factor is barely smaller than the unweighted P(>= 16) = 0.28.")
print("Gating moves the false-positive mass but does not remove it, because a")
print("guesser who clears the three gating items by luck then has to clear the")
print("rest by luck too. Tightening the thorough threshold to 90% of the weight")
print("cuts it further; weighting the gating items 3x instead of 2x does too.")
print()
print("The honest summary: the guesser is NOT eliminated. At 18 or 20 out of 20")
print("the modal recommendation is still 'thorough'. What changed is the odds,")
print(f"from about 1 in {1 / old_fp:.0f} to about 1 in {1 / new_fp:.0f}.")
print()
print("The trade is deliberate: a reader who misses ONE quantifier-negation")
print("question is told to revisit Part 01 even if they scored 20 overall. That")
print("is the right call here, because the lesson's own claim is that skipping")
print("Part 01 is the expensive mistake -- this rule makes it cheap to catch.")
```

Output:

```
== (a) and (c) a coin-flip guesser ==
   expected score   : 10.0
   standard dev     : 2.236
   most likely score: 10  (that is the middle of the distribution)
   P(score >= 10)   : 58.8%
   P(score >= 16)   : 0.5909%
   P(score >= 4)    : 99.9%
   P(score >= 20)   : 0.0000954%
   P(20 correct)    : 0.000095%

== (b) the bands, measured against the guesser ==
band         range    P(guesser lands here)  verdict
thorough     16-20                    0.59%  informative
fast         10-15                   58.22%  USELESS as a signal
Part 01        4-9                   41.06%  USELESS as a signal
Part 00        0-3                    0.13%  informative

The fast band is the guesser's home. A reader who scored 11 and admitted
guessing has told you nothing you did not already know.

== (d) the improved rule ==
   weighted maximum : 23 (the three logic items count double)

   a guesser scoring 10: most likely recommendation -> Part 01
   a guesser scoring 11: most likely recommendation -> Part 01
   a guesser scoring 13: most likely recommendation -> Part 01
   a guesser scoring 16: most likely recommendation -> Part 01
   a guesser scoring 18: most likely recommendation -> thorough
   a guesser scoring 20: most likely recommendation -> thorough

P(guesser gets all 3 gating items right) = 12.5%
P(guesser is told 'thorough')            = 0.3065%
P(guesser was told 'thorough') before   = 0.5909%
   a 1.9x tightening, from 169-in-1 to
   326-in-1, bought by making three questions load-bearing.

Why only 2x, and not the 8x the gating alone would suggest: the gating
factor 0.5**3 = 0.125 is multiplied by P(Bin(17,0.5) >= 13) = 0.245, and
that second factor is barely smaller than the unweighted P(>= 16) = 0.28.
Gating moves the false-positive mass but does not remove it, because a
guesser who clears the three gating items by luck then has to clear the
rest by luck too. Tightening the thorough threshold to 90% of the weight
cuts it further; weighting the gating items 3x instead of 2x does too.

The honest summary: the guesser is NOT eliminated. At 18 or 20 out of 20
the modal recommendation is still 'thorough'. What changed is the odds,
from about 1 in 169 to about 1 in 326.

The trade is deliberate: a reader who misses ONE quantifier-negation
question is told to revisit Part 01 even if they scored 20 overall. That
is the right call here, because the lesson's own claim is that skipping
Part 01 is the expensive mistake -- this rule makes it cheap to catch.
```
 A guesser's expected score is exactly 10, with a
standard deviation of 2.24, and 10 is the *mode*. So the most likely outcome for
someone who knows nothing is the first score in the "fast track" band, and the
probability of landing in that band at all is 58.8% — better than even.

**What (b) shows.** The bands are not equally informative, and the useful
measurement is the guesser's probability of landing in each one. The thorough band
carries a 0.59% false-positive rate. The fast band carries **58.2%** — better
than even, and the guesser's modal score of 10 sits at its bottom edge. The
"Part 01" band is nearly as contaminated at 41.1%, though a false positive there
costs little because the band recommends the conservative path. The "Part 00" band
is effectively guess-proof at 0.13%.

So the diagnostic is trustworthy at both ends and useless in the middle, and the
middle is where most readers land. That is a real design defect rather than a
rounding issue: a reader told "take the fast track" on a 58%-likely-to-be-noise
signal will proceed confidently through material they cannot read.

**What (d) buys, and what it does not.** Weighting the three Part 01 logic items
double and making them gating cuts the top band's false-positive rate from 0.59%
to **0.31%** — a 1.9× tightening, from about 1-in-169 to about 1-in-326. It also
flips the modal recommendation to "start at Part 01" for every guesser score from
10 through 16, which is the entire range where the old rule was uninformative.

The gain is smaller than the gating factor alone suggests, and the reason is worth
stating because it is the actual lesson: the $0.5^3 = 0.125$ from clearing three
gating items is multiplied by $P(\mathrm{Bin}(17, 0.5) \ge 13) = 0.245$, and
that second factor is barely below the unweighted $P(\ge 16) = 0.28$. Gating moves
the false-positive mass; it does not remove it, because a guesser who clears the
gating items by luck must then clear the rest by luck too. Tightening the
thorough threshold to 90% of the weight, or weighting the gating items 3×, both cut
it further. Neither is free.

**The honest cost.** The rule is strict: a reader who scored 20 out of 20 but
missed the quantifier-negation question is told to revisit Part 01. That is
deliberate, and it is defensible for *this* course because the lesson's own central
claim is that skipping Part 01 is the expensive mistake — the rule makes the costly
mistake cheap to catch at the price of a few false alarms. In a course where Part
01 were optional, the same weighting would be wrong, which is the general point: a
diagnostic's weights encode what that particular course most needs its readers to
get right, and a weighting that is right for one course is arithmetic noise in
another.

**The property that makes it worth having.** A scoring rule must be
*uninformative for the uninformative*: two readers indistinguishable in knowledge
must be indistinguishable in score. The old rule fails because the guesser's modal
outcome sits inside a confident band. Any rule worth shipping keeps the guesser's
whole distribution below the threshold for every recommendation except "start from
the beginning", and pushes it strictly below the top band's threshold as well.
Adding questions would not have achieved this — going from 20 items to 40 only
shrinks the standard deviation by $\sqrt{2}$, leaving the median band untouched.
The middle band is structurally insensitive to test length; the fix has to be
information *per item*, which is what weighting and gating provide.

</details>

**[ ] Challenge 7 — Write a dependency checker for the real repository, and make
it fail on the real catalog.** Take the `CATALOG` from the lesson's Runnable Code
and write four checks, each of which finds a *real* defect in the data rather than
a synthetic one:

1. **Dangling prerequisites** — a lesson naming a prerequisite that is not in the
   catalog. Report what you find and explain why `study_order` cannot tell the
   difference between this and a cycle.
2. **Wrong sort count** — a lesson whose direct prerequisites are listed in
   descending order, which is a data-entry smell. Report any.
3. **Unreachable lesson** — a lesson that appears in no other lesson's
   prerequisite list and has no dependents, i.e. dead weight in the index.
4. **Ordering claim check** — verify that `study_order`'s output really does
   respect every edge, and report the count of violations.

Then: pick the check with the most severe consequences for a reader, and explain
what a reader following the *printout* rather than the graph would do.

<details>
<summary>Solution</summary>

```python
# The lesson's own CATALOG, verbatim: number, title, part, minutes, prereqs.
CATALOG_RAW = [
    (0, "Why Mathematics Matters", "part00", 15, []),
    (1, "How to Read Notation", "part00", 25, []),
    (2, "Study Plan", "part00", 15, []),
    (10, "Propositions and Connectives", "part01", 30, [1]),
    (11, "Truth Tables and Equivalence", "part01", 40, [10]),
    (12, "Predicates and Quantifiers", "part01", 40, [11]),
    (13, "Proof Techniques", "part01", 45, [12]),
    (14, "Mathematical Induction", "part01", 40, [13]),
    (15, "Sets and Cardinality", "part01", 40, [14]),
    (20, "Counting Principles", "part02", 35, [15]),
    (21, "Permutations and Combinations", "part02", 35, [20]),
    (22, "The Binomial Theorem", "part02", 25, [21]),
    (23, "Inclusion-Exclusion and Pigeonhole", "part02", 40, [22]),
    (24, "Recurrence Relations", "part02", 45, [23]),
    (25, "Relations and Equivalence Classes", "part02", 40, [24]),
    (26, "Graph Theory", "part02", 50, [24]),
    (27, "Trees and Spanning Trees", "part02", 45, [26]),
    (28, "Counting Strategies", "part02", 30, [21, 26]),
    (30, "Vectors and Vector Spaces", "part03", 40, [15]),
    (31, "Matrices and Matrix Algebra", "part03", 45, [30]),
    (32, "Linear Systems and Gaussian Elimination", "part03", 45, [31]),
    (33, "Determinant and Inverse", "part03", 40, [32]),
    (34, "Basis, Dimension, and Rank", "part03", 40, [33]),
    (35, "Linear Transformations and Kernels", "part03", 45, [34]),
    (36, "Eigenvalues and Eigenvectors", "part03", 50, [35]),
    (37, "Inner Products, Norms, Geometry", "part03", 40, [36]),
    (38, "Orthogonality and Least Squares", "part03", 45, [37]),
    (39, "Diagonalization and Spectral Theory", "part03", 45, [38]),
    (40, "SVD and PCA", "part03", 50, [39]),
    (41, "Matrices, Graphs, Applications", "part03", 35, [40]),
    (50, "Functions, Limits, Continuity", "part04", 45, [30]),
    (51, "Derivatives", "part04", 50, [50]),
    (52, "Integration", "part04", 50, [51]),
    (53, "Multivariable Calculus", "part04", 50, [51]),
    (54, "Taylor Series", "part04", 45, [51, 52]),
    (55, "Fourier Series and Transforms", "part04", 50, [52]),
    (60, "Probability Foundations", "part05", 35, [15]),
    (61, "Probability Axioms and Rules", "part05", 40, [60]),
    (62, "Conditional Probability and Bayes", "part05", 45, [61]),
    (63, "Discrete Random Variables", "part05", 40, [62]),
    (64, "Expectation and Variance", "part05", 45, [63]),
    (65, "Continuous Random Variables", "part05", 40, [64]),
    (66, "Common Distributions", "part05", 45, [64]),
    (67, "Joint Random Variables and Covariance", "part05", 45, [64]),
    (68, "Law of Large Numbers and CLT", "part05", 50, [64, 52]),
    (69, "Estimation and Hypothesis Testing", "part05", 50, [64, 68]),
    (70, "Information Theory and Entropy", "part05", 40, [64, 69]),
    (80, "Big-O and Complexity", "part06", 50, [24, 30]),
    (81, "Amortised Analysis", "part06", 40, [80]),
    (82, "Tools for Algorithm Design", "part06", 45, [81, 23]),
    (90, "Vectors in 3D and Cross Product", "part07", 35, [30]),
    (91, "Transformations for Graphics", "part07", 45, [90, 31]),
    (92, "Geometric Algorithms", "part07", 45, [91, 26]),
    (100, "Convexity", "part08", 40, [38, 51]),
    (101, "Gradient Descent", "part08", 45, [100, 36]),
    (102, "Lagrange Multipliers", "part08", 45, [101, 32]),
    (110, "Number Theory", "part09", 45, [21, 23]),
    (111, "Modular Arithmetic and Crypto", "part09", 45, [110]),
    (112, "Hashing", "part09", 40, [110, 23]),
    (113, "Error-Correcting Codes", "part09", 40, [111, 22]),
    (120, "Tensors and Broadcasting", "part10", 45, [31, 35]),
    (121, "Numerical Methods and Floating Point", "part10", 45, [52, 120]),
]

BY_NUMBER = {n: (title, part, mins, list(prereqs))
             for n, title, part, mins, prereqs in CATALOG_RAW}
DEPENDENTS = {n: [] for n in BY_NUMBER}
for n, (_, _, _, prereqs) in BY_NUMBER.items():
    for p in prereqs:
        if p in DEPENDENTS:
            DEPENDENTS[p].append(n)

print(f"catalog: {len(BY_NUMBER)} lessons")
print()

# --- CHECK 1: dangling prerequisites.
dangling = sorted({p for _, (_, _, _, pre) in BY_NUMBER.items()
                   for p in pre if p not in BY_NUMBER})
print("== check 1: dangling prerequisites ==")
print(f"   found: {dangling if dangling else 'none'}")
print("   A dangling edge is NOT a cycle, but study_order reports both the same")
print("   way: 'cycle, blocked: [...]'. The reader cannot tell a missing lesson")
print("   from an impossible order, and the fixes differ entirely.")
print("   A dangling edge is NOT a cycle, but study_order reports both the same")
print("   way: 'cycle, blocked: [...]'. The reader cannot tell a missing lesson")
print("   from an impossible order, and the fixes differ entirely.")
print()

# --- CHECK 2: prerequisite lists in descending order (data-entry smell).
unsorted_pre = [n for n, (_, _, _, pre) in BY_NUMBER.items()
                if pre != sorted(pre)]
print("== check 2: unsorted prerequisite lists ==")
for n in unsorted_pre:
    print(f"   lesson {n:>3} {BY_NUMBER[n][0]}: {BY_NUMBER[n][3]}")
if not unsorted_pre:
    print("   none")
print("   A set's order does not change its closure, so the plan is unaffected.")
print("   But an out-of-order list is a hand-edited list, and the next edit can")
print("   drop an entry. It is a leading indicator, not a bug.")
print()

# --- CHECK 3: leaves with no dependents, and roots with no prerequisites.
leaves = sorted(n for n in BY_NUMBER
                if not DEPENDENTS[n] and BY_NUMBER[n][3])
roots = sorted(n for n in BY_NUMBER
               if not DEPENDENTS[n] and not BY_NUMBER[n][3])
print("== check 3: dead weight ==")
print(f"   have prereqs but nothing depends on them: {leaves}")
print(f"   no prereqs and no dependents               : {roots}")
print("   These are ENDPOINTS, not errors: a course has to end somewhere, and")
print("   lesson 121 is the natural terminus. But 'no dependents' is also what a")
print("   TYPO looks like: misspell 121 as 12 in a later lesson's list and 121")
print("   becomes a dead end while 12 gains a spurious dependent. This check")
print("   cannot tell those two cases apart either.")
print()

# --- CHECK 4: does study_order actually respect every edge?
def study_order(table):
    done, order, remaining = set(), [], list(table)
    while remaining:
        ready = [n for n in remaining if set(BY_NUMBER[n][3]) <= done]
        if not ready:
            raise ValueError(f"blocked: {remaining}")
        chosen = min(ready)          # deterministic tie-break, as in the lesson
        order.append(chosen)
        done.add(chosen)
        remaining.remove(chosen)
    return order


order = study_order(sorted(BY_NUMBER))
position = {n: i for i, n in enumerate(order)}
edges = [(n, p) for n in BY_NUMBER for p in BY_NUMBER[n][3]]
violations = [(n, p) for n, p in edges if position[p] > position[n]]
print("== check 4: does the topological order respect every edge? ==")
print(f"   edges checked : {len(edges)}")
print(f"   violations    : {len(violations)}")
print(f"   first 6       : {order[:6]}")
print(f"   last 4        : {order[-4:]}")
print()
print("Every unsorted list in check 2 turns out to be a CROSS-PART lesson:")
print("68, 82, 91, 92, 101, 102, 112 and 113 each take prerequisites from two")
print("different parts, written high-number-first because the author appended")
print("the second one later. So check 2 found structure rather than noise: the")
print("graph is not a bundle of chains, and the places it branches across parts")
print("are the places that get hand-edited.")
print()
print("== which defect hurts a reader most? ==")
print("   Not the unsorted lists: a set's order changes nothing about a closure.")
print("   Not the endpoints: those are the shape of a course that ends.")
print("   It is check 1's CATEGORY. A dangling prerequisite and a real cycle are")
print("   different faults with different fixes, and study_order reports both as")
print("   ValueError('blocked: [...]'). A reader who sees it will go looking for")
print("   a circular dependency, will not find one, and will conclude the tool is")
print("   broken. The message misleads in the direction that costs most effort.")
```

Output:

```
catalog: 62 lessons

== check 1: dangling prerequisites ==
   found: none
   A dangling edge is NOT a cycle, but study_order reports both the same
   way: 'cycle, blocked: [...]'. The reader cannot tell a missing lesson
   from an impossible order, and the fixes differ entirely.
   A dangling edge is NOT a cycle, but study_order reports both the same
   way: 'cycle, blocked: [...]'. The reader cannot tell a missing lesson
   from an impossible order, and the fixes differ entirely.

== check 2: unsorted prerequisite lists ==
   lesson  68 Law of Large Numbers and CLT: [64, 52]
   lesson  82 Tools for Algorithm Design: [81, 23]
   lesson  91 Transformations for Graphics: [90, 31]
   lesson  92 Geometric Algorithms: [91, 26]
   lesson 101 Gradient Descent: [100, 36]
   lesson 102 Lagrange Multipliers: [101, 32]
   lesson 112 Hashing: [110, 23]
   lesson 113 Error-Correcting Codes: [111, 22]
   A set's order does not change its closure, so the plan is unaffected.
   But an out-of-order list is a hand-edited list, and the next edit can
   drop an entry. It is a leading indicator, not a bug.

== check 3: dead weight ==
   have prereqs but nothing depends on them: [25, 27, 28, 41, 53, 54, 55, 65, 66, 67, 70, 82, 92, 102, 112, 113, 121]
   no prereqs and no dependents               : [0, 2]
   These are ENDPOINTS, not errors: a course has to end somewhere, and
   lesson 121 is the natural terminus. But 'no dependents' is also what a
   TYPO looks like: misspell 121 as 12 in a later lesson's list and 121
   becomes a dead end while 12 gains a spurious dependent. This check
   cannot tell those two cases apart either.

== check 4: does the topological order respect every edge? ==
   edges checked : 76
   violations    : 0
   first 6       : [0, 1, 2, 10, 11, 12]
   last 4        : [112, 113, 120, 121]

Every unsorted list in check 2 turns out to be a CROSS-PART lesson:
68, 82, 91, 92, 101, 102, 112 and 113 each take prerequisites from two
different parts, written high-number-first because the author appended
the second one later. So check 2 found structure rather than noise: the
graph is not a bundle of chains, and the places it branches across parts
are the places that get hand-edited.

== which defect hurts a reader most? ==
   Not the unsorted lists: a set's order changes nothing about a closure.
   Not the endpoints: those are the shape of a course that ends.
   It is check 1's CATEGORY. A dangling prerequisite and a real cycle are
   different faults with different fixes, and study_order reports both as
   ValueError('blocked: [...]'). A reader who sees it will go looking for
   a circular dependency, will not find one, and will conclude the tool is
   broken. The message misleads in the direction that costs most effort.
```

Every unsorted list in check 2 is a **cross-part** lesson: 68 (`[64, 52]`),
82 (`[81, 23]`), 91 (`[90, 31]`), 92 (`[91, 26]`), 101 (`[100, 36]`), 102
(`[101, 32]`), 112 (`[110, 23]`) and 113 (`[111, 22]`) each name prerequisites
from two different parts of the course, and each is listed high-number-first
because the author added the second prerequisite later. So the check has found
real structure, not noise: the graph is not a set of chains, and the points where
it branches across parts are exactly the points that get hand-edited. A closure
does not care about the order of a set, so the *plan* is unaffected — which is
why this is a leading indicator rather than a bug.

Check 3's 17 endpoints are the same story from the other side. Lesson 25
(Relations and Equivalence Classes) has no dependents at all, which means
nothing in the declared catalog requires it — Lesson 26 graph theory declares
`[24]` rather than `[25]`. Lesson 28, 70, 82, 92, 112 and 113 are similar: real
lessons, and leaves. Whether that is a mistake or a fact about how the course was
written cannot be decided from the graph. It *can* be decided by reading the
repository index, which is the point of the lesson's claim that hand-maintained
catalogs go stale.

**Which defect hurts a reader most.** Not the unsorted lists, which change
nothing about the plan. Not the endpoints, which are the shape of a course that
ends. It is check 1's *category*, and the defect is in the error reporting rather
than the data.

A dangling prerequisite and a genuine cycle are different situations with
different fixes — one needs a lesson added to the table, the other needs a
prerequisite removed — and `study_order` reports both as
`ValueError("cycle, blocked: ...")`. A reader who sees `blocked: [39]` will look
for a circular dependency, will not find one, and will conclude the tool is
broken. The message is actively misleading in the direction that costs the most
diagnostic effort.

The worse case is the one the check did *not* find, which is why it is worth
having. Check 1 reports none, and every closure in the catalog is therefore
well defined — but Exercise 1 had to manufacture a dangling edge to demonstrate
the failure, which means nobody knows whether the catalog is actively maintained
or merely currently intact. If the table ever does go stale, the failure surfaces
at *study* time rather than plan time: the reader reaches Lesson 40, follows the
chain to 39, finds nothing there, and gets no signal at all that the plan was
incomplete. That is the lesson's own stated failure mode — silent, with no error
and no explanation — and it is the reason a checker that distinguishes four
categories is worth more than one that merely reports failure. A tool that says
"something is wrong" is worth much less than a tool that says *which* something.

</details>
 Build a cut-down
catalog of 14 lessons that includes Lesson 40 with prerequisite `[39]` while
Lesson 39 is *not* declared. Report which prerequisites dangle. Then fill in the
missing linear algebra chain 31 through 39 and confirm nothing dangles. Then add
a hypothetical Lesson 42, "Applications of SVD", with prerequisites `[40, 70]`,
and confirm the topological sort produces a valid order with 42 appearing after
both 40 and 70. Finally, deliberately create a cycle by giving Lesson 42 the
prerequisite `[43]` and giving 43 the prerequisite `[42]`, and confirm
`study_order` raises `ValueError` rather than looping forever. Report exactly
what each step printed.

<details>
<summary>Solution</summary>

```python
class Lesson:
    """A lesson: its number, title, reading time, and direct prerequisites."""

    def __init__(self, number, title, minutes, prereqs=None):
        self.number = number
        self.title = title
        self.minutes = minutes
        self.prereqs = list(prereqs) if prereqs else []


# A cut-down catalog: enough structure to exercise the graph, small enough to read.
CATALOG = [
    Lesson(0, "Why Mathematics Matters", 15),
    Lesson(1, "How to Read Notation", 25),
    Lesson(2, "Study Plan", 15),
    Lesson(10, "Propositions and Connectives", 30, [1]),
    Lesson(11, "Truth Tables and Equivalence", 40, [10]),
    Lesson(12, "Predicates and Quantifiers", 40, [11]),
    Lesson(13, "Proof Techniques", 45, [12]),
    Lesson(14, "Mathematical Induction", 40, [13]),
    Lesson(15, "Sets and Cardinality", 40, [14]),
    Lesson(30, "Vectors and Vector Spaces", 40, [15]),
    Lesson(40, "SVD and PCA", 50, [39]),          # 39 is not declared yet
    Lesson(60, "Probability Foundations", 35, [15]),
    Lesson(64, "Expectation and Variance", 45, [60]),
    Lesson(70, "Information Theory and Entropy", 40, [64]),
]

BY_NUMBER = {lesson.number: lesson for lesson in CATALOG}


def dangling_prereqs(table):
    """Prerequisite numbers that no lesson in `table` satisfies."""
    return sorted({p for l in table.values() for p in l.prereqs if p not in table})


def study_order(lessons):
    """Topological sort. A lesson appears only after everything it needs."""
    done, order, remaining = set(), [], list(lessons)
    while remaining:
        ready = [l for l in remaining if set(l.prereqs) <= done]
        if not ready:
            raise ValueError(f"cycle, blocked: {[l.number for l in remaining]}")
        chosen = min(ready, key=lambda l: l.number)
        order.append(chosen.number)
        done.add(chosen.number)
        remaining.remove(chosen)
    return order


# --- Step 0: the graph has a hole. Lesson 40 needs 39, which is not declared.
print(f"lessons declared: {len(CATALOG)}")
print(f"dangling prerequisites: {dangling_prereqs(BY_NUMBER)}")
print()

# --- Step 1: fill the missing linear algebra chain 31..39.
for number, title, minutes, needs in [
    (39, "Diagonalization and Spectral Theory", 45, [38]),
    (38, "Orthogonality and Least Squares", 45, [37]),
    (37, "Inner Products, Norms, Geometry", 40, [36]),
    (36, "Eigenvalues and Eigenvectors", 50, [35]),
    (35, "Linear Transformations and Kernels", 45, [34]),
    (34, "Basis, Dimension, and Rank", 40, [33]),
    (33, "Determinant and Inverse", 40, [32]),
    (32, "Linear Systems and Gaussian Elimination", 45, [31]),
    (31, "Matrices and Matrix Algebra", 45, [30]),
]:
    BY_NUMBER[number] = Lesson(number, title, minutes, needs)

declared = {l.number for l in CATALOG}
CATALOG.extend(BY_NUMBER[n] for n in sorted(BY_NUMBER) if n not in declared)
print(f"dangling prerequisites after filling 31..39: {dangling_prereqs(BY_NUMBER)}")
print()

# --- Step 2: add a hypothetical Lesson 42 that needs both 40 and 70.
BY_NUMBER[42] = Lesson(42, "Applications of SVD", 40, [40, 70])
CATALOG.append(BY_NUMBER[42])

order = study_order(CATALOG)
pos = {n: i for i, n in enumerate(order)}
print(f"catalog size with the chain and 42 added: {len(CATALOG)}")
print(f"lesson 42 prerequisites: {BY_NUMBER[42].prereqs}")
print(f"  position of 42 : {pos[42]}")
print(f"  position of 40 : {pos[40]}")
print(f"  position of 70 : {pos[70]}")
print(f"  42 after both  : {pos[42] > pos[40] and pos[42] > pos[70]}")
print()

# --- Step 3: break the graph on purpose. 42 needs 43, and 43 needs 42.
BY_NUMBER[42].prereqs = [40, 70, 43]
BY_NUMBER[43] = Lesson(43, "A Lesson That Does Not Exist", 30, [42])
CATALOG.append(BY_NUMBER[43])

try:
    study_order(CATALOG)
    print("BUG: the cycle was not detected")
except ValueError as err:
    print(f"cycle detected, as required: {err}")
print()
print("Without the `if not ready` guard the `while remaining` loop never")
print("terminates, because no lesson ever becomes ready. Real schedulers hit")
print("this on every build that introduces a dependency cycle.")
```

Output:

```
lessons declared: 14
dangling prerequisites: [39]

dangling prerequisites after filling 31..39: []

catalog size with the chain and 42 added: 24
lesson 42 prerequisites: [40, 70]
  position of 42 : 23
  position of 40 : 19
  position of 70 : 22
  42 after both  : True

cycle detected, as required: cycle, blocked: [42, 43]
```

Two things came out of this worth keeping. First, the dangling prerequisite at
step 0 was invisible to `study_order`: it reported `40` as "blocked", which reads
like a cycle but is actually a missing node. Those are different bugs with
different fixes, so a real scheduler should distinguish them, and the
`dangling_prereqs` helper is exactly that distinction. Second, the honest answer
to "does the catalog omit lessons?" is that it does not: all 62 lesson numbers in
the full catalog above are covered by the repository index. The omissions people
find when they write such a catalog by hand are how a real index goes stale.

</details>
</details>

## Summary
- Three tracks: **fast** (6 weeks, skim proofs), **thorough** (14 weeks, all
  exercises), **interview** (4 weeks, Parts 02 and 06 focused).
- The prerequisite graph is transitive. The two prerequisites printed on a
  lesson are not the list; the transitive closure is, and for Lesson 40 it is
  29 lessons.
- Never skip Part 01. It is 6 lessons and every other part's proofs use its
  techniques. Everything else in the course is skippable; that is not.
- A cycle in the prerequisite graph makes a topological sort fail rather than
  loop forever, and the failure is `ValueError`, not a hang.
- Cost to reach a lesson is not value in reaching it. Lesson 113 is reachable
  fastest and is the narrowest; lesson 70 is the most reusable.
- Define progress as a capability you can demonstrate, never as a page you
  have read. The five-item checklist in Exercise 3 is a usable version.
- Watch the minutes-per-capability-point column. A lesson where that number is
  high is a lesson where you are re-reading instead of practising.
- Budget 60 to 90 minutes per lesson, not the header's 25 to 50. The header is
  reading time only, and the exercises are not revision.

## Next

[Part 01 — Logic and Proof](../part01_logic_proof/README.md) is next. Lesson 10,
Propositions and Connectives, assumes you can read a formula out loud and run
Python, and nothing else.
