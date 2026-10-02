# 10 — Propositions and Connectives

**Part**: part01_logic_proof · **Prerequisites**: 01 · **Time**: 30 min

---

## In Plain Words

Some sentences are true or false and stay that way no matter who says them.
"Two plus two is four" is one. "This request has a valid auth token" is one.
"Sort this list" is not, because it is an instruction rather than a claim.
"x is greater than five" is not either, until you say what x is.

A sentence that does have a definite truth value is called a proposition. The
point of logic is to study how propositions combine. Five words do almost all
the work: and, or, not, if-then, and if-and-only-if. This lesson is about what
those five words mean exactly, and the answer for the fourth one surprises
almost everybody.

The single most important thing in the lesson is that "if P then Q" does not
mean P and Q. It means something closer to "not P, or Q". Get that wrong and you
will write a security check that admits exactly the users it was supposed to
reject.

## Why Computer Science Cares

**Boolean conditions are propositions.** Every `if` you write takes a
proposition. Understanding what `not a or b` means relative to `not (a or b)`
is the difference between a working access check and one that fails open for the
precise users it was written to exclude.

**Implication is how specifications are written.** "If the request is not
authenticated then it must be rejected" is a proposition about every input.
Whether your handler satisfies it is a question of logic, not of testing.

**Short-circuit evaluation is an implementation of a connectives.** Python's
`and` stops at the first falsy operand, `or` at the first truthy one. That
behaviour only makes sense once you know these are connectives with specific
truth conditions.

**The `while` loop with a complex condition is a proposition to be negated
correctly.** "Keep going until nothing is left" is `while items:`, and getting
`while not items:` right requires reading `not` as binding to the whole
disjunction rather than to its first term.

**SAT solvers and equivalence checkers exist because of this material.** Every
hardware synthesis tool, every formal verification tool, and every compiler
constraint solver is working with the formulas in this lesson. Datasets, artifact
analysis, and program equivalence all compile down to "find an assignment that
makes this formula true".

**Type theory is this material with the domains filled in.** `∀α. α → α → α` is
literally "a function that takes two things of the same type and returns one of
that type".

## The Formal Version

**Definition.** A *proposition* is a declarative sentence that is either true or
false, but not both, and whose truth value does not depend on who is asking.

**Definition.** A *connective* is an operation that takes propositions and
produces a proposition.

**Definition.** Negation: for a proposition `P`, the proposition `¬P` is true
exactly when `P` is false. `¬¬P` is *logically equivalent* to `P`.

**Definition.** Conjunction: `P ∧ Q` is true exactly when both `P` and `Q` are
true.

**Definition.** Disjunction: `P ∨ Q` is true exactly when at least one of `P`
and `Q` is true. Note "at least one", not "exactly one". `P ∨ Q` is true when
both are true.

**Definition.** Implication: `P → Q` is true except in the one case where `P` is
true and `Q` is false. Equivalently, `P → Q` is false exactly when `P` is true
and `Q` is false.

**Definition.** Biconditional: `P ↔ Q` is true exactly when `P` and `Q` have the
same truth value, whether both true or both false.

**Definition.** Two propositions `P` and `Q` are *logically equivalent*, written
`P ≡ Q`, if they have the same truth value under every assignment. Not merely
"they happen to agree here", but "they agree everywhere".

**Definition.** A *tautology* is a proposition true under every assignment.
A *contradiction* is one false under every assignment. A *contingent*
proposition is neither, and most propositions you will meet are contingent.

**Definition.** The *principle of substitution for equivalence* (often called
Leibniz's law): if `P ≡ Q`, then `P` may be replaced by `Q` in any formula
without changing that formula's truth value. This is the formal justification
for every condition simplification you will ever do.

**Theorem.** `P → Q ≡ ¬P ∨ Q`.

*Why this is the central fact.* Read the definition of implication aloud: "true
except when `P` is true and `Q` is false". The disjunction `¬P ∨ Q` is false in
exactly that same case: it is false only when both `¬P` is false (so `P` is
true) and `Q` is false. Same false case, and a proposition is completely
determined by where it is false. So they are the same proposition. From this
one identity, the rest follow: `¬(P → Q) ≡ P ∧ ¬Q`, and the contrapositive
`P → Q ≡ ¬Q → ¬P`.

## Worked Example

The worked example is a security check, because that is where this material
actually costs money.

**The requirement, written as English.** "Deny the request unless the caller is
an administrator or a superuser."

**Step 1. Translate to a proposition.** Let `A` mean "the caller is an
administrator" and `S` mean "the caller is a superuser". Let `D` mean "deny".
The requirement is: if neither `A` nor `S`, then `D`. In symbols,
`¬(A ∨ S) → D`. Using the theorem, that is `¬¬(A ∨ S) ∨ D`, which simplifies to
`(A ∨ S) ∨ D`.

**Step 2. Simplify the logic.** A denial is granted only when at least one of
`A`, `S` holds. So the check is `if not (A or S): deny`. There is no other case.

**Step 3. Now write what a programmer writes under time pressure.**

```text
if not A or not S:
    deny()
```

**Step 4. Find where it differs.** `not A or not S` parses as `(¬A) ∨ (¬S)`. That
is true whenever `A` is false *or* `S` is false — that is, unless the caller is
**both** an administrator **and** a superuser. The correct version is
`not (A or S)`, true only when neither holds. Compare:

| A | S | `not (A or S)` (wanted) | `not A or not S` (written) |
| --- | --- | --- | --- |
| F | F | True — deny | True — deny |
| F | T | False — allow | True — **deny** |
| T | F | False — allow | True — **deny** |
| T | T | False — allow | False — allow |

**Step 5. Diagnose the mistake.** The programmer applied De Morgan *backwards*.
They turned `not (A or S)` into `¬A ∨ ¬S`, which is the rule for `not (A ∧ S)`.
They had the connective backwards.

**Step 6. Check whether Python would have caught it.** No, and this is the
important part. `not A or not S` is a perfectly well-formed Python expression
with a well-defined meaning. Python does not know what you meant. Neither does a
type checker, and in this case neither does a linter. The only defence is that
you can reason about the truth table, which is what this lesson is for.

**Step 7. Notice that the bug fails open or closed depending on the connective.**
Here it fails *closed*: it denies users it should have allowed. Swap `or` for
`and` in the original and the same mistake fails *open*, admitting users who
should have been denied. Both directions are live bugs, which is why the negation
rule is worth memorising rather than reconstructed.

## Runnable Code

### A tiny proposition language

```python
import itertools

# Each object is a FORMULA, not a value. A formula knows how to evaluate
# itself under an assignment of truth values to its letters.


class Formula:
    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __invert__(self):
        return Not(self)


class Var(Formula):
    def __init__(self, name):
        self.name = name

    def evaluate(self, assignment):
        return assignment[self.name]

    def __repr__(self):
        return self.name


class Not(Formula):
    def __init__(self, inner):
        self.inner = inner

    def evaluate(self, assignment):
        # `not`, not `~`: `~True` is -2, which would make the output ugly.
        return not self.inner.evaluate(assignment)

    def __repr__(self):
        return f"~{self.inner!r}"


class And(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, assignment):
        return self.left.evaluate(assignment) and self.right.evaluate(assignment)

    def __repr__(self):
        return f"({self.left!r} & {self.right!r})"


class Or(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, assignment):
        return self.left.evaluate(assignment) or self.right.evaluate(assignment)

    def __repr__(self):
        return f"({self.left!r} | {self.right!r})"


class Implies(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, assignment):
        # p -> q is FALSE in exactly one case: p is True and q is False.
        # Written this way so the code reads like the definition.
        return (not self.left.evaluate(assignment)) or self.right.evaluate(assignment)

    def __repr__(self):
        return f"({self.left!r} -> {self.right!r})"


class Iff(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, assignment):
        return self.left.evaluate(assignment) == self.right.evaluate(assignment)

    def __repr__(self):
        return f"({self.left!r} <-> {self.right!r})"


def assignments(names):
    """Every assignment to `names`, in a fixed order."""
    return [dict(zip(names, bits))
            for bits in itertools.product([False, True], repeat=len(names))]


def column(formula, names):
    """The truth values of `formula` under every assignment to `names`."""
    return [formula.evaluate(a) for a in assignments(names)]


def as_bits(values):
    """Render a truth column as a string of 1s and 0s."""
    return "".join("1" if v else "0" for v in values)


def print_truth_table(title, formula, names):
    print(title)
    print("  ".join(f"{n:>6}" for n in names) + "  |  result")
    print("-" * (7 * len(names) + 11))
    for a, value in zip(assignments(names), column(formula, names)):
        cells = "  ".join(f"{str(a[n]):>6}" for n in names)
        print(f"{cells}  |  {str(value):>6}")
    print()


p, q = Var("p"), Var("q")
NAMES = ["p", "q"]

print("=" * 64)
print("1. Implication is not conjunction")
print("=" * 64)
print_truth_table("p -> q", Implies(p, q), NAMES)
print_truth_table("p and q", And(p, q), NAMES)

imp = column(Implies(p, q), NAMES)
conj = column(And(p, q), NAMES)
disj = column(Or(p, q), NAMES)
iff = column(Iff(p, q), NAMES)

print(f"{'p':>6} {'q':>6} {'p and q':>9} {'p or q':>8} {'p -> q':>8} {'p <-> q':>9}")
for a, c, d, i, f in zip(assignments(NAMES), conj, disj, imp, iff):
    print(f"{str(a['p']):>6} {str(a['q']):>6} {str(c):>9} {str(d):>8} "
          f"{str(i):>8} {str(f):>9}")
print()
print(f"p -> q is False in {imp.count(False)} row. p and q is False in "
      f"{conj.count(False)} rows.")
print(f"p -> q agrees with p and q in {sum(a == b for a, b in zip(imp, conj))} of 4 rows.")
print(f"p -> q agrees with p or q  in {sum(a == b for a, b in zip(imp, disj))} of 4 rows.")
print(f"p <-> q agrees with p and q in {sum(a == b for a, b in zip(iff, conj))} of 4 rows.")
print()
print("Look at row 1 of the p <-> q column: it is True when both p and q are")
print("False. A biconditional is not 'both hold', it is 'the two agree'. Its")
print("real meaning is (p and q) or (not p and not q), which is why")
print("'p <-> q' and 'p and q' differ on the first row.")

print()
print("=" * 64)
print("2. Negating a compound statement")
print("=" * 64)
print()

pairs = [
    ("not (p and q)", ~And(p, q), "not p or not q", (~p) | (~q)),
    ("not (p or q)", ~Or(p, q), "not p and not q", (~p) & (~q)),
    ("not (p -> q)", ~Implies(p, q), "p and not q", p & (~q)),
    ("not (p <-> q)", ~Iff(p, q), "p or q", p | q),
]

for left_title, left, right_title, right in pairs:
    lc, rc = column(left, NAMES), column(right, NAMES)
    print(f"{left_title:<16} {as_bits(lc)}   vs   {right_title:<16} {as_bits(rc)}"
          f"   equal: {lc == rc}")
print()
print("rows of each column are (p, q) = (F,F), (F,T), (T,F), (T,T)")
print()
print("The first two rows are De Morgan's laws. The third is the negation of")
print("implication: not (p -> q) is 'p and not q', NOT 'p -> not q'.")
print()
print("The fourth is False, and that is the point of including it. Read it out:")
print("  not (p <-> q)  is True when p and q DIFFER, so the column is 0110.")
print("  p or q         is True when at least one holds, so the column is 0111.")
print("They differ on the last row, where both are true and so p <-> q holds,")
print("which makes its negation false.")
print()
xor = (p & (~q)) | (~p & q)
print("The correct rewrites for a biconditional are:")
print(f"  not (p <-> q)  ==  (p and not q) or (not p and q)  -> "
      f"{column(~Iff(p, q), NAMES) == column(xor, NAMES)}")
print(f"  its column     : {as_bits(column(xor, NAMES))}")

print()
print("=" * 64)
print("3. The bug this lesson exists to prevent")
print("=" * 64)
print()
print("Requirement: 'deny the request unless the user is an admin OR a superuser'.")
print()
print("  wanted  : not (is_admin or is_superuser)   # deny unless either")
print("  written : not is_admin or not is_superuser  # NOT what was wanted")
print()
print(f"{'is_admin':>9} {'is_superuser':>13} {'wanted':>8} {'written':>8} {'same?':>7}")
mismatches = []
for is_admin, is_super in [(False, False), (False, True), (True, False), (True, True)]:
    wanted = not (is_admin or is_super)
    written = (not is_admin) or (not is_super)
    if wanted != written:
        mismatches.append((is_admin, is_super))
    print(f"{str(is_admin):>9} {str(is_super):>13} {str(wanted):>8} "
          f"{str(written):>8} {str(wanted == written):>7}")
print()
print(f"the two disagree in {len(mismatches)} of 4 cases.")
print()
print("Python parses `not is_admin or is_superuser` as `(not is_admin) or")
print("is_superuser`, because `not` binds tighter than `or`. The grouping is")
print("not the bug. The bug is dropping the parentheses around the disjunction")
print("and so negating the wrong subformula. When you negate a compound")
print("condition, write the grouping out in full first, then simplify.")

print()
print("=" * 64)
print("4. Which sentences are even propositions?")
print("=" * 64)
print()
print("A proposition has a truth value. Some sentences do not, and treating")
print("them as if they do is the first error. Only two of the seven below are")
print("propositions; the rest have free variables, or are not claims about the")
print("world at all.")
print()

candidates = [
    ("2 + 2 = 4", "statement, and true", True),
    ("London is the capital of France", "statement, and false", True),
    ("x > 5", "not a statement: x is unbound, so no truth value", False),
    ("close the door", "imperative, not a claim about the world", False),
    ("is the server up", "a question", False),
    ("this sentence is false", "a liar: no consistent truth value", False),
    ("n! > 0 for every n", "statement, once you say n ranges over N", True),
]

for text, verdict, is_statement in candidates:
    print(f"  {'PROPOSITION' if is_statement else 'NOT       '}  {text}")
    print(f"              {verdict}")
print()
print("'x > 5' is the case that matters most in practice. It is not a")
print("proposition until you say what x is and what it has been assigned. That")
print("is exactly the domain question Lesson 12 makes precise, and it is why a")
print("type system exists: 'x > 5' has no meaning without a type.")
```

## Common Mistakes

**Wrong: `if not is_admin or is_superuser:` meaning "allow admins and
superusers".**
Right: Python parses this as `(not is_admin) or is_superuser`, so it also
admits anyone who is *not* an admin, which is everyone. The requirement
"allow if admin or superuser" needs `if is_admin or is_superuser:`. The bug is
assuming `not` distributes over `or` the way it distributes over `and`.
Why tempting: `not` binds tighter than `or` in every programming language you
have used, so the grouping is right; the error is believing the negation is
already distributed correctly. De Morgan says `¬(a ∨ b) = ¬a ∧ ¬b`, not
`¬a ∨ ¬b`.

**Wrong: "if p then q means p and q."**
Right: implication is true in three of the four cases, including both cases
where `p` is false. It only asserts a relationship when `p` holds. In code this
is why `if x is not None and x > 0:` is a valid guard — the second clause is
never evaluated when `x` is `None` — while `if x is None or x > 0:` asserts
something entirely different and raises `TypeError`.
Why tempting: in programming, "if" usually introduces a precondition, and
preconditions do feel conjunctive. That is a different connective from the one
in the specification.

**Wrong: treating `p or q` as "exactly one of p, q".**
Right: `or` is inclusive. `p or q` is true when both are true. In Python this is
why `self.x = self.y = None` then `if self.x or self.y: self.z = 1` sets `z` when
both are `None`... no, when *neither* is `None`; and why `bool(a or b)` is not
an exclusive-or. If you want exactly one, you need `(a and not b) or (not a and b)`
or, better, Python's `a != b` on booleans.
Why tempting: natural-language "either A or B" usually means exclusive, and the
same words in the same sentence often do. Mathematics and programming both take
the inclusive reading, and mixing them up in a comment is how bugs get written.

**Wrong: "not (p and q) is the same as not p or not q" without checking which
connective is inside.**
Right: `¬(p ∧ q) = ¬p ∨ ¬q` is true, and `¬(p ∨ q) = ¬p ∧ ¬q` is also true, but
they are different formulas from each other. The rule flips *and* to *or*. Getting
the flip backwards is the single most common logic error in code review, and the
worked example above is that mistake.
Why tempting: the shape "not... or not..." feels right for both, and the two
rules are stated in the same breath so they blur together.

**Wrong: assuming a sentence with a variable in it is not a statement.**
Right: "x is greater than five" has no truth value until `x` is assigned, but
"every natural number greater than five is odd" is a proposition with a free
variable, and once you state the domain it is decidable. The real requirement is
not the absence of variables but the absence of *unbound* ones. This is the gap
Lesson 12 fills.
Why tempting: the criterion "does it have a definite truth value" is correct, and
people apply it to the presence of variables rather than to their being bound,
which is a subtle and easy misreading.

## Formula Sheet

Notation follows [SYMBOLS.md](../SYMBOLS.md). `P` and `Q` are propositions, `T`
and `F` are the two truth values, and every truth column quoted below is taken
over the fixed row order `(P, Q) = (F,F), (F,T), (T,F), (T,T)`. Two columns are
comparable only when both were computed over the same rows in that same order.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| proposition | `$P \in \{T, F\}$` | a sentence with exactly one truth value | every `if` condition is one. A sentence with an *unbound* variable has none |
| connective | `$\odot(P, Q) = P'$` | an operation that takes propositions and returns a proposition | the only way formulas grow. Python has `not`, `and`, `or`, and no arrow |
| `$\neg P$` | `$\neg T = F$`, `$\neg F = T$` | flip the value | the only unary connective. Python `not`, **never** `~`: `~True` is `-2` |
| `$P \wedge Q$` | true only when **both** are true; column `0001` | AND | Python `and`. Short-circuits at the first falsy operand, so operand order is behaviour |
| `$P \vee Q$` | false only when **both** are false; column `0111` | OR, **inclusive** — at least one, not exactly one | Python `or`. Short-circuits at the first truthy operand |
| `$P \to Q$` | `$\neg P \vee Q$`; column `1101` | false only when `P` is true and `Q` is false | guards, preconditions, specifications. In Python: `if not p or q` |
| `$P \leftrightarrow Q$` | `$(P \to Q) \wedge (Q \to P) = (P \wedge Q) \vee (\neg P \wedge Q)$`; column `1001` | the two have the **same** truth value | Python `p == q` on booleans. **Not** `p and q`, whose column is `0001` |
| `$P \equiv Q$` | `$\operatorname{col}(P) = \operatorname{col}(Q)$` | they agree under **every** assignment | a claim about behaviour, not about spelling. This is what makes a rewrite provable |
| substitution for equivalence | `$P \equiv Q \;\Rightarrow\; C[P] \equiv C[Q]$` | you may swap `P` for `Q` inside any larger formula `C` | Leibniz's law: the licence behind every condition simplification anyone performs |
| tautology | `$P \equiv T$`, written `$\top$` | true on every row | an `if` whose condition is a tautology is a branch that can never be false: dead code |
| contradiction | `$P \equiv F$`, written `$\bot$` | false on every row | `p & ~p`. A `while` whose condition is a contradiction never runs its body |
| contingent | neither `$T$ nor $F$` | true on some rows and false on others | almost every real condition. Being contingent is not a criticism |
| exclusive-or | `$P \oplus Q = (P \wedge \neg Q) \vee (\neg P \wedge Q)$`; column `0110` | **exactly one** of them holds | Python `p != q` on booleans. Also equal to `$\neg(P \leftrightarrow Q)$` |
| De Morgan | `$\neg(P \wedge Q) \equiv \neg P \vee \neg Q$`, `$\neg(P \vee Q) \equiv \neg P \wedge \neg Q$` | push a `$\neg$` through and **flip** AND to OR, or OR to AND | rewriting a negated condition. Getting the flip backwards is the worked example |
| double negation | `$\neg\neg P \equiv P$` | two NOTs cancel | the step that leaves every literal a bare variable or its negation |
| idempotence | `$P \wedge P \equiv P$`, `$P \vee P \equiv P$` | saying it twice says it once | first thing to try when a condition has grown long |
| absorption | `$P \vee (P \wedge Q) \equiv P$`, `$P \wedge (P \vee Q) \equiv P$` | the wider term swallows the narrow one | the most common dead branch in real code |
| commutativity | `$P \wedge Q \equiv Q \wedge P$`, `$P \vee Q \equiv Q \vee P$` | order does not matter | regrouping a condition so a reader can parse it |
| associativity | `$(P \wedge Q) \wedge R \equiv P \wedge (Q \wedge R)$` | how a chain of one connective is bracketed | dropping redundant parentheses; `Exercise 3`'s grammar needs a choice here |
| contrapositive | `$P \to Q \equiv \neg Q \to \neg P$` | swap both sides and negate both | always safe, and the form used to prove things by induction |
| converse | `$\neg P \to \neg Q$, column `1011` against `1101` | the implication read backwards | **not** equivalent to `$P \to Q$`. [Lesson 13](13_proof_techniques.md) lives on that difference |
| negation of implication | `$\neg(P \to Q) \equiv P \wedge \neg Q$`; column `0010` | the premise holds and the conclusion does not | never `$\neg(P \to \neg Q)$`, which is a different formula entirely |
| negation of a biconditional | `$\neg(P \leftrightarrow Q) \equiv (P \wedge \neg Q) \vee (\neg P \wedge Q)$`; column `0110` | the two **differ** | exclusive-or. **Not** `$P \vee Q$`, whose column is `0111`; the two disagree only on `(T, T)` |
| precedence | `$\neg \;>\; \wedge \;>\; \vee$`, and `$\to$` is right-associative: `$P \to (Q \to R)$` | NOT binds tightest, then AND, then OR | Python agrees, so `not p and q or r` means `(($\neg p \wedge q$) \vee r$)` and `not p or q` means `($\neg p$) \vee q$` |
| truth column | `$0110$` for `$P \oplus Q$ over `(F,F), (F,T), (T,F), (T,T)` | the entire formula written as four bits | the unit of comparison for equivalence. Row order is part of the value |
| assignments | `$2^n$` | 4 rows for `p` and `q`, 16 for four variables | the price of proving an equivalence by exhaustion, and the reason a proof is only as strong as the row count |
| bound variable | every occurrence of `x` is bound by a quantifier | `x > 5` has no truth value; `every integer x greater than 5 is odd` has one | a proposition needs a definite truth value, not an absence of variables |

Domain restrictions, which is where answers go wrong. **`$\vee$` and `$\to$`
need the inclusive reading**: `p or q` is true when both hold, and `p → q` is
true on *both* rows where `p` is false. **Precedence applies only to
unparenthesised text**: `not a or b` is `(not a) or b`, so the grouping in the
worked example below is correct and the bug lies elsewhere. **Associativity is a
choice, not a fact** — `p → q → r` and `(p → q) → r` have different columns,
`11111101` and `01011101` over three variables, so a parser that picks the wrong
one is wrong in a way no test you happen to write will catch. And **a truth table
is complete only for the variables that actually appear**: `p & q | p & ~r`
mentions `r`, so a four-row table over `p` and `q` alone does not settle it.

## Multiple Choice Questions

**Q1.** What is the truth value of `P → Q` when `P` is false and `Q` is false?

- A) False
- B) True
- C) Undefined, because a false premise makes the implication vacuous
- D) True only if `P` and `Q` are equivalent

<details>
<summary>Answer and explanation</summary>

**B) True.**

`P → Q` is false in exactly one case: `P` true and `Q` false. Every other row
is true, including this one. Option A comes from reading implication as "both
must hold", which is `P ∧ Q`. Option C is a real philosophical position — the
principle of vacuous truth — and classical logic adopts it; but "undefined" is
not an option in a truth table, and programmers need a total function. Option D
confuses the connective with equivalence: `P ↔ Q` is a different connective that
does compare the two values.

</details>

**Q2.** Which Python expression is equivalent to `not (a and b)`?

- A) `not a or not b`
- B) `not a and not b`
- C) `not a or b`
- D) `a or not b`

<details>
<summary>Answer and explanation</summary>

**A) `not a or not b`.**

De Morgan's first law is `¬(P ∧ Q) ≡ ¬P ∨ ¬Q`, and it flips `and` to `or`.
Option B is De Morgan's *second* law, which applies to `not (a or b)` — the
connective has to match. This is the single most common logic error in code
review, and it is why both laws need to be in your head rather than one.
Options C and D keep the wrong connective in place and so are not equivalent to
anything useful: check `a=True, b=False`, where the original is `False` and both
C and D are `True`.

</details>

**Q3.** You want "allow the request if the caller is an admin **or** a
superuser". Which condition is correct?

- A) `if not (is_admin or is_superuser): allow()`
- B) `if not is_admin or not is_superuser: allow()`
- C) `if is_admin or is_superuser: allow()`
- D) `if is_admin and is_superuser: allow()`

<details>
<summary>Answer and explanation</summary>

**C) `if is_admin or is_superuser: allow()`.**

`or` is inclusive and does exactly what the requirement says. Option B is the
tempting wrong answer: `not is_admin or not is_superuser` is true whenever
*either* privilege is missing, so it allows almost everyone — the De Morgan
mistake from the lesson's worked example. Option A denies the common case and
inverts the whole guard. Option D requires both privileges, which is `and`
semantics and matches "admin **and** superuser", not "or".

</details>

**Q4.** `P → Q` and `¬Q → ¬P` are logically equivalent. What is
`¬P → ¬Q` in relation to `P → Q`?

- A) Equivalent, by contraposition
- B) The converse, and not equivalent
- C) The contrapositive, and equivalent
- D) A tautology

<details>
<summary>Answer and explanation</summary>

**B) The converse, and not equivalent.**

Swap and negate both sides of `¬P → ¬Q` and you get `P → Q`, which means it is
the *converse* of the original. Converse and contrapositive are different
things: the contrapositive is equivalent to the original, the converse generally
is not.

A concrete counterexample over the integers. Let `P` be "`n` is even" and `Q` be
"`n > 10`". At `n = 4` the premise `P` is true and the conclusion `Q` is false, so
`P → Q` is false. But `¬P` is false at `n = 4` too, so `¬P → ¬Q` is vacuously
true there. One formula false where the other is true: not equivalent.

Option A misnames the relationship. Option C describes what you get from
`¬Q → ¬P`, not from `¬P → ¬Q`. Option D is wrong because the converse is a
perfectly good proposition that simply is not a tautology — evaluate it at
`n = 4` as above and it is `False`.

</details>

**Q5.** `(p ∧ q) → (p ∨ q)` is a tautology. Why?

- A) Because `p` and `q` cannot both be false
- B) Because whenever both are true, at least one is true
- C) Because implication is false only when the premise is true and the
  conclusion false, and the conclusion follows from the premise
- D) Because `p ∨ q` is equivalent to `p`

<details>
<summary>Answer and explanation</summary>

**C) Because implication is false only when the premise is true and the
conclusion false, and the conclusion follows from the premise.**

That is the definition, applied. If `p ∧ q` is true then `p` is true, so `p ∨ q`
is true, so the implication is not false. Option A is a different claim — `p`
and `q` *can* both be false — and it is false as stated. Option B describes only
the row where both are true, ignoring the three rows where the premise is false
and the implication is vacuously true; a tautology has to hold in all four.
Option D is just wrong: `p ∨ q` and `p` differ at `p = False, q = True`.

</details>

**Q6.** Which of these is a proposition?

- A) "Sort this list in ascending order"
- B) "This list is sorted in ascending order"
- C) "Close the file"
- D) "x > 5"

<details>
<summary>Answer and explanation</summary>

**B) "This list is sorted in ascending order".**

A proposition is declarative — it asserts something rather than requesting
something — and has a truth value that does not depend on the reader. Option A
and option C are imperatives: they are instructions, so they are neither true nor
false. Option D looks like a proposition but contains an unbound `x`, so its
truth value depends on an assignment that has not been made; it becomes a
proposition once you say "every integer `x` greater than 5 is odd", which is
Lesson 12's territory.

</details>

**Q7.** You are told `P → Q` is true and `Q` is false. What follows?

- A) `P` is false, by modus tollens on the implication
- B) `P` is true
- C) Nothing at all follows
- D) `¬P → ¬Q`

<details>
<summary>Answer and explanation</summary>

**A) `P` is false, by modus tollens on the implication.**

The only row where `P → Q` is false is `P` true and `Q` false. Since the
implication is *true* and `Q` is *false*, `P` must be false. Option B is the
mistake of reading the arrow as `P ∧ Q`. Option C would be right if you knew
only that `P → Q` is true with nothing about `Q`; the extra fact is what makes
the deduction go through. Option D is a true formula but it tells you nothing
new, and its being a valid rewrite is a separate fact from the deduction asked
about.

</details>

**Q8.** Why does Python not catch `not is_admin or not is_superuser` when the
requirement was "allow admins and superusers"?

- A) Because Python evaluates `or` lazily and skips the second operand
- B) Because the expression is well-formed, has a well-defined value, and
  Python has no access to what you meant
- C) Because `not` has lower precedence than `or` in Python
- D) Because type checkers ignore boolean operators

<details>
<summary>Answer and explanation</summary>

**B) Because the expression is well-formed, has a well-defined value, and
Python has no access to what you meant.**

The bug is a mismatch between the requirement and the code, not between the code
and the language. Python parses `(not is_admin) or (not is_superuser)` exactly
as written and evaluates it correctly; the error was made before the code
existed. Option A is false — `or` returns the first truthy operand, which is a
short-circuit on *values*, not a skipping of evaluation of the second operand
when the first is truthy. Option C has the precedence backwards: `not` binds
*tighter* than `or` in Python, which is exactly why the grouping is `¬A ∨ ¬S`.
Option D is a distraction; the issue is not that a tool ignores the operator but
that the requirement was never expressed in a form a tool could check.

</details>

---

## Subjective Questions

### Short Answer

**Q1. State `P → Q` in terms of `or` and `not`, and explain in one sentence why
that rewrite is the one worth memorising.**

<details>
<summary>Answer</summary>

`P → Q ≡ ¬P ∨ Q`.

It is worth memorising because everything else follows from it. The negation
`¬(P → Q) ≡ P ∧ ¬Q` is obtained by negating both sides with De Morgan, and the
contrapositive `P → Q ≡ ¬Q → ¬P` is obtained by applying the rewrite to both
sides in a chain. De Morgan's laws, idempotence, and absorption are independent
identities, but implication needs this one to join them.

</details>

**Q2. What is the negation of `P ↔ Q`, and why is it not `P ∨ Q`?**

<details>
<summary>Answer</summary>

`¬(P ↔ Q) ≡ (P ∧ ¬Q) ∨ (¬P ∧ Q)` — the two propositions have *different*
truth values.

`P ↔ Q` is true when both are true or both are false, so its negation is the
union of the two mixed cases. `P ∨ Q` is much weaker: it is true whenever
either is true, so it also covers the case where both are true, which is exactly
the case where the biconditional holds. Since the biconditional is true there
and `P ∨ Q` is too, `P ∨ Q` cannot be its negation.

</details>

**Q3. Give a one-line proof that `P → (Q → P)` is a tautology.**

<details>
<summary>Answer</summary>

Take any assignment. If `Q` is false then `Q → P` is true, so the outer
implication is true. If `Q` is true then `Q → P` reduces to `P`, and in either
case `P → P` holds.

Equivalently, algebraically: `P → (Q → P) ≡ ¬P ∨ (¬Q ∨ P) ≡ (¬P ∨ P) ∨ ¬Q ≡
¬Q ∨ ¬Q ≡ ¬Q`, which is a tautology.

</details>

**Q4. Why is `p or q` not an exclusive-or, and what should you write when you
want exclusive-or?**

<details>
<summary>Answer</summary>

`or` is inclusive: it is true when both operands are true, as well as when
exactly one is. Exclusive-or wants the second case excluded.

Write `(a and not b) or (not a and b)`, or on booleans simply `a != b`. In
Python `bool(a) ^ bool(b)` also works if you convert first, but `^` on non-
booleans means something else entirely, so the explicit form is safer.

</details>

**Q5. You know `P → Q` and `Q → R`. What can you conclude, and what is the
resulting formula?**

<details>
<summary>Answer</summary>

You can conclude `P → R`. This is transitivity, also called the hypothetical
silicone, and it is what lets a chain of guards stand in for a single
requirement.

The proof: `P → Q ≡ ¬P ∨ Q` and `Q → R ≡ ¬Q ∨ R`, so chaining gives
`¬P ∨ (¬Q ∨ R)`, which by associativity is `(¬P ∨ ¬Q) ∨ R`. Now `¬P ∨ ¬Q`
*implies* `¬P`, so absorption gives `¬P ∨ R`, which is `P → R`.

</details>

**Q6. In `if not a and not b:`, does Python evaluate `not b` when `not a` is
false?**

<details>
<summary>Answer</summary>

No. Python's `and` returns the first falsy operand, and when `not a` is false it
returns that `False` immediately without evaluating `not b`.

This is why `if not a and not b:` is safe to write when `a` and `b` are values
whose evaluation could fail — `None > 0` will not be attempted once the guard has
already failed. It is *not* a general permission to skip null checks, because
the skipping depends on the order you wrote.

</details>

### Long Answer

**Q1. A security check is written `if not is_admin or not is_superuser:
deny()`. The requirement was "deny unless the caller is an admin or a
superuser". Diagnose the bug, explain why no tool catches it, and say what
defence exists.**

<details>
<summary>Model answer</summary>

The written expression parses as `(¬is_admin) ∨ (¬is_superuser)`, so it denies
whenever *either* privilege is missing. The correct guard is
`if not (is_admin or is_superuser): deny()` — equivalently
`if not is_admin and not is_superuser: deny()`.

The programmer applied De Morgan with the wrong connective. The rule
`¬(P ∨ Q) ≡ ¬P ∧ ¬Q` was used where `¬(P ∧ Q) ≡ ¬P ∨ ¬Q` was needed. The
result fails *closed*: it denies legitimate admins who are not superusers. The
same mistake with `or` swapped for `and` fails *open*, which is worse.

No tool catches it because the code is correct Python. `not is_admin or not
is_superuser` is a well-formed expression with a definite value; Python has no
access to the requirement, and no type checker or linter does either. The defect
lives in the gap between the specification and the program, which is precisely
the gap a truth table lets you inspect.

The defence is procedural rather than automated: translate the requirement into
propositions, write the truth table, and compare the code's column against the
requirement's. Here four rows are checkable, and they disagree on two. Where you
can make the requirement executable — as an assertion, a property test, or a
table of cases — you get a check. Absent that, the discipline is to parenthesise
deliberately and to distrust any rewrite that changes a connective.

</details>

**Q2. Explain why `P → Q` is not the same as `P ∧ Q`, and why treating it as
such produces bugs in both directions.**

<details>
<summary>Model answer</summary>

`P → Q` is true in three of four rows; `P ∧ Q` is true in one. They agree only
on `(P, Q) = (T, T)`, and they agree on both rows where `P` is false: both are
true when `Q` is false, but `P → Q` is also true when `Q` is true, because a
false premise makes the implication vacuously true.

Reading implication as conjunction produces two distinct failure modes.

**Failing open.** `if x is not None and x > 0:` is a correct guard written in
conjunctive form, and it is what a programmer writes when they think of "if" as
introducing a precondition. But `if x is not None then do_something(x)` needs no
such guard: when `x` is `None` the implication is simply true. Adding `x is not
None` to an `if x:` guard is redundant, and worse, writing
`if x is None or x > 0:` produces the opposite of the intent — the disjunction
passes when `x` is `None`, which is exactly the case to reject.

**Failing closed.** Treating "if `P` then `Q`" as "both `P` and `Q` must hold"
makes a requirement vacuous case into a hard requirement. A spec that says "if
the user is an admin, log the action" does not require that non-admins do not
log. Implemented as `if is_admin and log()`, the log becomes mandatory for
everyone.

The asymmetry to remember: conjunction is a *test* of two facts, implication is a
*conditional* about one. Reading a specification's "if" as a test adds
requirements the author did not state, and that is how a correct program becomes
incorrect without anything looking broken.

</details>

**Q3. You must show that a code change preserved behaviour across every
reachable state. Where does propositional logic help, and where do you need
something more?**

<details>
<summary>Model answer</summary>

Propositional logic helps when the property is *compositional*: it is built from
independent conditions combined with `and`, `or`, `not`, and `→`, with no
arithmetic and no quantification over a domain. Then equivalence is decidable by
exhaustion — enumerate all `2^n` assignments, evaluate the requirement and the
code, compare columns — and you get a proof rather than evidence. That is what a
truth table is for, and it is why the lesson's Challenge uses reachability to
cut the table down.

You need more when something leaves the propositional world. Three cases matter
in practice.

*Quantification over data.* `all(items)` and `any(items)` are quantifiers. "Every
item passes validation" is `∀i ∈ items. valid(i)`, and there are infinitely many
possible `items`, so no truth table covers it. You need an argument about the
loop, or a test over a sample plus the argument — which is Lesson 13 and Lesson
14.

*Arithmetic.* `len(x) > 0` is not a proposition about a boolean; it is a
comparison, and its behaviour depends on the value. A bitmask condition has `2^64`
inputs, not two. Modelling it as a boolean to get a truth table is what hides
the bug in the Challenge's case B: the unreachable-wrong row and the
reachable-wrong rows collapse together.

*Unbounded state and aliasing.* Whether a change is safe depends on the history
of the program, not just the current values. No truth table over booleans
captures "this list is aliased somewhere else".

The practical rule: reach for a truth table when the condition is a tree of
boolean operations with no arithmetic, and for a proof about the algorithm when
it is not. Reaching for the truth table in the second case produces a false
sense of completeness — you will have enumerated every case of a model that
omits the thing that matters.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — Build the truth table for eight propositions.** For each,
write the plain-English condition, then produce the truth column over
`(p, q) = (F,F), (F,T), (T,F), (T,T)` using the `Formula` classes from the
Runnable Code section. Report the column as a string of 1s and 0s, and state
whether it is a tautology, a contradiction, or contingent.

1. `¬(p ∧ q)`
2. `p → q`
3. `p ↔ q`
4. `¬p ∨ (q → p)`
5. `(p ∨ q) ∧ ¬(p ∧ q)`   (this is exclusive-or)
6. `p → (q → p)`           (this one is always true; find out why)
7. `¬p → ¬q`              (is this the contrapositive of 2, or its converse?)
8. `(p ∧ q) → (p ∨ q)`     (is this a tautology?)

<details>
<summary>Solution</summary>

```python
import itertools


# The formula classes, exactly as in the Runnable Code section.
class Formula:
    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __invert__(self):
        return Not(self)


class Var(Formula):
    def __init__(self, name):
        self.name = name

    def evaluate(self, a):
        return a[self.name]

    def __repr__(self):
        return self.name


class Not(Formula):
    def __init__(self, inner):
        self.inner = inner

    def evaluate(self, a):
        return not self.inner.evaluate(a)

    def __repr__(self):
        return f"~{self.inner!r}"


class And(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, a):
        return self.left.evaluate(a) and self.right.evaluate(a)

    def __repr__(self):
        return f"({self.left!r} & {self.right!r})"


class Or(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, a):
        return self.left.evaluate(a) or self.right.evaluate(a)

    def __repr__(self):
        return f"({self.left!r} | {self.right!r})"


class Implies(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, a):
        return (not self.left.evaluate(a)) or self.right.evaluate(a)

    def __repr__(self):
        return f"({self.left!r} -> {self.right!r})"


class Iff(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, a):
        return self.left.evaluate(a) == self.right.evaluate(a)

    def __repr__(self):
        return f"({self.left!r} <-> {self.right!r})"


p, q = Var("p"), Var("q")
NAMES = ["p", "q"]
ROWS = [dict(zip(NAMES, b)) for b in itertools.product([False, True], repeat=2)]


def column(f):
    """The truth column of a formula, as a list of booleans."""
    return [f.evaluate(a) for a in ROWS]


def bits(values):
    """Render a truth column as a string of 1s and 0s."""
    return "".join("1" if v else "0" for v in values)


def classify(f):
    """tautology, contradiction, or contingent."""
    col = column(f)
    if all(col):
        return "tautology"
    if not any(col):
        return "contradiction"
    return "contingent"


items = [
    ("not (p and q)", ~(p & q)),
    ("p -> q", Implies(p, q)),
    ("p <-> q", Iff(p, q)),
    ("not p or (q -> p)", ~p | Implies(q, p)),
    ("(p or q) and not (p and q)", (p | q) & ~(p & q)),
    ("p -> (q -> p)", Implies(p, Implies(q, p))),
    ("not p -> not q", Implies(~p, ~q)),
    ("(p and q) -> (p or q)", Implies(p & q, p | q)),
]

print(f"{'#':>2} {'proposition':<32} {'column':>7}  kind")
for i, (label, f) in enumerate(items, 1):
    print(f"{i:>2} {label:<32} {bits(column(f)):>7}  {classify(f)}")

print()
print("English, column by column. Rows are (p, q) = FF, FT, TF, TT.")
print()
print("1  not (p and q) is true when at least one of them is false.")
print("2  p -> q is false only when p is true and q is false.")
print("3  p <-> q is true when they agree: both true, or both false.")
print("4  not p or (q -> p) is a tautology. If p is false the first disjunct")
print("   holds; if p is true the second has a true consequent. Either way.")
print("5  exclusive-or is true when exactly one of p, q holds.")
print("6  p -> (q -> p) is a tautology, for a reason worth reading below.")
print("7  not p -> not q is the CONVERSE, not the contrapositive.")
print("8  (p and q) -> (p or q) is a tautology: nothing satisfies both")
print("   conjuncts without satisfying at least one disjunct.")

print()
print("=" * 68)
print("Why #6 is a tautology, one row at a time")
print("=" * 68)
for a in ROWS:
    inner = Implies(q, p).evaluate(a)
    outer = Implies(p, Implies(q, p)).evaluate(a)
    print(f"  p={str(a['p']):<5} q={str(a['q']):<5} "
          f"q->p={str(inner):<5} p->(q->p)={outer}")
print()
print("  When p is True, the inner q->p is automatically True because p holds,")
print("  so the outer implication has a True consequent and is True.")
print("  When p is False, the outer implication is True by definition.")
print("  Either way the outer is True. That is why it is a tautology.")

print()
print("=" * 68)
print("Converse versus contrapositive")
print("=" * 68)
original = column(Implies(p, q))
contrapositive = column(Implies(~q, ~p))
converse = column(Implies(~p, ~q))
print(f"  p -> q          {bits(original)}")
print(f"  not q -> not p  {bits(contrapositive)}   contrapositive, "
      f"equal to original: {contrapositive == original}")
print(f"  not p -> not q  {bits(converse)}   converse, "
      f"equal to original: {converse == original}")
print()
print("The contrapositive column is the original with the rows reversed, which")
print("is exactly what 'same false case' predicts. The converse column is not,")
print("and it is False on row 2 (p = F, q = T): p -> q is True there while")
print("not p -> not q is False. That single row is a real logical difference,")
print("and Lesson 13's contrapositive proof depends on it.")
```

Output:

```
 # proposition                       column  kind
 1 not (p and q)                       1110  contingent
 2 p -> q                              1101  contingent
 3 p <-> q                             1001  contingent
 4 not p or (q -> p)                   1111  tautology
 5 (p or q) and not (p and q)          0110  contingent
 6 p -> (q -> p)                       1111  tautology
 7 not p -> not q                      1011  contingent
 8 (p and q) -> (p or q)               1111  tautology

  p=False q=False q->p=True  p->(q->p)=True
  p=False q=True  q->p=False p->(q->p)=True
  p=True  q=False q->p=True  p->(q->p)=True
  p=True  q=True  q->p=True  p->(q->p)=True

  p -> q          1101
  not q -> not p  1101   contrapositive, equal to original: True
  not p -> not q  1011   converse, equal to original: False
```

Item 5's column `0110` is exactly `(p ∧ ¬q) ∨ (¬p ∧ q)`, which is
exclusive-or. Python's `^` on booleans computes the same thing: `True ^ True`
is `False`, and so is `True ^ True` here. Item 7 is the one to dwell on,
because the contrapositive being True while the converse is False is the single
most useful fact in Lesson 13.

</details>

**[ ] Exercise 2 — Audit three real conditions.** For each condition below,
(a) write the requirement in English, (b) build the truth table over the
relevant variables, (c) say whether the code matches the requirement, and (d) if
it does not, give the correct version and the single input combination that
exposes the difference.

1. Requirement: "return 400 if the request is malformed **or** unauthenticated".
   Code: `if not well_formed and not authenticated: return 400`
2. Requirement: "retry if the request failed **and** was idempotent".
   Code: `if not failed or not idempotent: retry()`
3. Requirement: "grant access if the user is an admin **or** the resource is
   public **and** not archived". Code: `if is_admin or is_public and not archived:`

<details>
<summary>Solution</summary>

```python
import itertools


def truth_table(labels, fn):
    """Print every row of a boolean function of `labels`, with its value."""
    rows = [dict(zip(labels, b)) for b in itertools.product([False, True],
                                                            repeat=len(labels))]
    for a in rows:
        cells = "  ".join(f"{label}={str(a[label]):<5}" for label in labels)
        print(f"  {cells}  ->  {fn(a)}")
    return rows


def column(labels, fn):
    """The truth column of a boolean function, as a list of booleans."""
    return [fn(dict(zip(labels, b))) for b in
            itertools.product([False, True], repeat=len(labels))]


def bits(values):
    """Render a truth column as a string of 1s and 0s."""
    return "".join("1" if v else "0" for v in values)


def required_1(a):
    """400 if the request is malformed OR unauthenticated."""
    return (not a["well_formed"]) or (not a["authenticated"])


def written_1(a):
    """The code under review, using AND where the requirement says OR."""
    return (not a["well_formed"]) and (not a["authenticated"])


L1 = ["well_formed", "authenticated"]

print("=" * 70)
print("1. 'return 400 if malformed OR unauthenticated'")
print("=" * 70)
print()
print("required : (not well_formed) or (not authenticated)")
print("written  : (not well_formed) and (not authenticated)")
print()
truth_table(L1, required_1)
print(f"  required column : {bits(column(L1, required_1))}")
print(f"  written column  : {bits(column(L1, written_1))}")
print(f"  agree           : {column(L1, required_1) == column(L1, written_1)}")
print()
witness_1 = {"well_formed": True, "authenticated": False}
print(f"witness: well_formed={witness_1['well_formed']}, "
      f"authenticated={witness_1['authenticated']}")
print("  a perfectly well-formed request that simply has no credentials")
print(f"  required says : {required_1(witness_1)}   -> 400")
print(f"  written says  : {written_1(witness_1)}   -> proceed as anonymous")
print()
print("Verdict: BUG, and it fails OPEN. The requirement rejects an")
print("unauthenticated request however well formed it is. The code only")
print("rejects a request that is BOTH malformed AND unauthenticated, so every")
print("anonymous request sails through to whatever the handler does next.")
print()
print("correct code:")
print("    if not well_formed or not authenticated:")
print("        return 400")
print()
print("3 of 4 rows disagree, and the row count is the diagnosis. A table that")
print("disagrees on most rows has the wrong connective. One disagreeing row")
print("usually means a boundary case, not a swapped AND.")
print()


def required_2(a):
    return a["failed"] and a["idempotent"]


def written_2(a):
    return (not a["failed"]) or (not a["idempotent"])


L2 = ["failed", "idempotent"]

print("=" * 70)
print("2. 'retry if failed AND idempotent'")
print("=" * 70)
print()
print("required : failed and idempotent")
print("written  : (not failed) or (not idempotent)")
print()
truth_table(L2, required_2)
print(f"  required column : {bits(column(L2, required_2))}")
print(f"  written column  : {bits(column(L2, written_2))}")
print(f"  agree           : {column(L2, required_2) == column(L2, written_2)}")
print()
witness_2 = {"failed": False, "idempotent": False}
print(f"witness: failed={witness_2['failed']}, idempotent={witness_2['idempotent']}")
print(f"  required says : {required_2(witness_2)}   -> do not retry")
print(f"  written says  : {written_2(witness_2)}   -> RETRY")
print()
print("Verdict: BUG. The written code retries whenever either the request did")
print("NOT fail, or it is not idempotent. So every successful non-idempotent")
print("request gets retried, which is precisely what idempotency exists to stop:")
print("a POST that succeeded, got retried, and charged the card twice.")
print()
print("correct code:")
print("    if failed and idempotent:")
print("        retry()")
print()
print("Or, if the real requirement is 'retry unless it succeeded', write that")
print("instead. Requirements of the form 'not (A and B)' are much harder to")
print("implement correctly than the thing you actually want:")
print("    if not succeeded:")
print("        retry()")
print()


def required_3(a):
    return a["is_admin"] or (a["is_public"] and not a["archived"])


def written_3(a):
    # Python binds `and` tighter than `or`, so this is the code under review.
    return (a["is_admin"] or a["is_public"]) and not a["archived"]


L3 = ["is_admin", "is_public", "archived"]

print("=" * 70)
print("3. 'grant if admin, or public and not archived'")
print("=" * 70)
print()
print("required : is_admin or (is_public and not archived)")
print("written  : is_admin or is_public and not archived")
print("            Python reads that as (is_admin or is_public) and not archived")
print()
print(f"{'is_admin':>9} {'is_public':>10} {'archived':>10} {'required':>10} "
      f"{'written':>8}  result")
mismatches = []
for b in itertools.product([False, True], repeat=3):
    a = dict(zip(L3, b))
    req, wr = required_3(a), written_3(a)
    if req != wr:
        mismatches.append((a, req, wr))
    print(f"{str(a['is_admin']):>9} {str(a['is_public']):>10} "
          f"{str(a['archived']):>10} {str(req):>10} {str(wr):>8}"
          f"  {'ok' if req == wr else 'BUG'}")
print()
print(f"{len(mismatches)} of 8 rows disagree.")
print()
print("Verdict: BUG. An admin is meant to reach an archived resource, but the")
print("written code ANDs `not archived` against the admin case too, so the")
print("admin is blocked from exactly the archive they need to fix.")
print()
print("correct code, with the parentheses written out:")
print("    if is_admin or (is_public and not archived):")
print()
print("Both failing rows have is_admin True and archived True, and they disagree")
print("only when is_public is False. The requirement grants access to the admin")
print("because is_admin alone suffices; the code demands the public branch too,")
print("because `not archived` was ANDed against the whole disjunction instead")
print("of only against the public branch.")
print()
print("The lesson from all three: when a requirement mixes and with or, write")
print("the parentheses in the code. Python will sometimes infer the wrong ones")
print("and will not warn you. And every one of these failed by swapping a")
print("connective or dropping a grouping, never by an arithmetic slip.")
print("Connective mistakes, not arithmetic mistakes.")
```

Output:

```
1. 'return 400 if malformed OR unauthenticated'
required : (not well_formed) or (not authenticated)
written  : (not well_formed) and (not authenticated)

  well_formed=False  authenticated=False  ->  True
  well_formed=False  authenticated=True   ->  True
  well_formed=True   authenticated=False  ->  True
  well_formed=True   authenticated=True   ->  False

  required column : 1110
  written column  : 1000
  agree           : False

2. 'retry if failed AND idempotent'
required : failed and idempotent
written  : (not failed) or (not idempotent)

  failed=False  idempotent=False  ->  False
  failed=False  idempotent=True   ->  False
  failed=True   idempotent=False  ->  False
  failed=True   idempotent=True   ->  True

  required column : 0001
  written column  : 1110
  agree           : False

witness: failed=False, idempotent=False
  required says : False   -> do not retry
  written says  : True   -> RETRY

3. 'grant if admin, or public and not archived'
required : is_admin or (is_public and not archived)
written  : is_admin or is_public and not archived
            Python reads that as (is_admin or is_public) and not archived

 is_admin  is_public   archived   required  written  result
    False      False      False      False    False  ok
    False      False       True      False    False  ok
    False       True      False       True     True  ok
    False       True       True      False    False  ok
     True      False      False       True     True  ok
     True      False       True       True    False  BUG
     True       True      False       True     True  ok
     True       True       True       True    False  BUG

2 of 8 rows disagree.
```

The number of disagreeing rows is the fastest diagnostic in the table. Condition
1 disagrees on three rows out of four, which says the connective itself is
wrong rather than a boundary case being mishandled. Condition 3 disagrees on two
rows out of eight, and both have the same shape, which points at one specific
grouping rather than a wholesale swap. Neither diagnosis could have been made by
reading the code, and both take one line of arithmetic to confirm.

</details>

**[ ] Exercise 3 — Build a formula parser and round-trip it against Python.** Write
a `Parser` class using recursive descent that turns a string like `"p & (q | ~r)"`
into a `Formula`. Grammar, loosest binding first:
`expr := impl ('|' impl)*`, `impl := conj ('->' impl)?`, `conj := unary ('&' unary)*`,
`unary := '~' unary | atom`, `atom := NAME | '(' expr ')'`. Then: (a) verify that
for each of ten test strings, the parsed formula agrees with Python's own `eval`
of the same text under `&`→`and`, `|`→`or`, `~`→`not`, across all 8 assignments of
three variables; (b) show that `~` binds tighter than `&`, which binds tighter than
`|`, by exhibiting two differently-grouped formulas with different columns; (c)
show that `p -> q` is the same formula as `~p | q`; (d) show that `->` is
right-associative by comparing the columns of `p -> q -> r` and `(p -> q) -> r`.

<details>
<summary>Solution</summary>

```python
import itertools


# --- The formula classes, as in the Runnable Code section.
class Formula:
    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __invert__(self):
        return Not(self)


class Var(Formula):
    def __init__(self, name):
        self.name = name

    def evaluate(self, a):
        return a[self.name]

    def __repr__(self):
        return self.name


class Not(Formula):
    def __init__(self, inner):
        self.inner = inner

    def evaluate(self, a):
        return not self.inner.evaluate(a)

    def __repr__(self):
        return f"~{self.inner!r}"


class And(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, a):
        return self.left.evaluate(a) and self.right.evaluate(a)

    def __repr__(self):
        return f"({self.left!r} & {self.right!r})"


class Or(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, a):
        return self.left.evaluate(a) or self.right.evaluate(a)

    def __repr__(self):
        return f"({self.left!r} | {self.right!r})"


class Implies(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, a):
        return (not self.left.evaluate(a)) or self.right.evaluate(a)

    def __repr__(self):
        return f"({self.left!r} -> {self.right!r})"


# --- A recursive descent parser. One method per grammar rule.
class Parser:
    def __init__(self, text):
        self.tokens = self.tokenize(text)
        self.pos = 0

    @staticmethod
    def tokenize(text):
        out, i = [], 0
        while i < len(text):
            ch = text[i]
            if ch.isspace():
                i += 1
            elif ch.isalpha():
                j = i
                while j < len(text) and text[j].isalpha():
                    j += 1
                out.append(("NAME", text[i:j]))
                i = j
            elif text[i:i + 2] == "->":
                out.append(("IMPLIES", "->"))
                i += 2
            elif ch in "&|~()":
                out.append((ch, ch))
                i += 1
            else:
                raise ValueError(f"unexpected character {ch!r}")
        return out

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def take(self, expected=None):
        kind, value = self.peek()
        if expected is not None and kind != expected:
            raise ValueError(f"expected {expected!r}, got {kind!r}")
        self.pos += 1
        return kind, value

    def parse(self):
        result = self.expr()
        if self.pos != len(self.tokens):
            raise ValueError(f"trailing tokens at position {self.pos}")
        return result

    def expr(self):
        left = self.impl()
        while self.peek()[0] == "|":
            self.take()
            left = Or(left, self.impl())
        return left

    def impl(self):
        left = self.conj()
        if self.peek()[0] == "IMPLIES":
            self.take()
            # Right-associative: a -> (b -> c), not (a -> b) -> c.
            return Implies(left, self.impl())
        return left

    def conj(self):
        left = self.unary()
        while self.peek()[0] == "&":
            self.take()
            left = And(left, self.unary())
        return left

    def unary(self):
        if self.peek()[0] == "~":
            self.take()
            return Not(self.unary())
        return self.atom()

    def atom(self):
        kind, value = self.peek()
        if kind == "NAME":
            self.take()
            return Var(value)
        if kind == "(":
            self.take()
            inner = self.expr()
            self.take(")")
            return inner
        raise ValueError(f"unexpected token {kind!r}")


def parse(text):
    return Parser(text).parse()


def column(formula, names):
    return [formula.evaluate(dict(zip(names, b)))
            for b in itertools.product([False, True], repeat=len(names))]


def bits(values):
    return "".join("1" if v else "0" for v in values)


def to_python_source(text):
    """Rewrite the token stream as a Python boolean expression.

    Python's precedence for `~`, `&`, `|` matches ours (unary, then and, then
    or), so only the spellings change. `->` has no Python spelling and is
    handled separately in part (c).
    """
    mapping = {"~": "not", "&": "and", "|": "or"}
    out = []
    for kind, value in Parser.tokenize(text):
        out.append(value if kind == "NAME" else mapping.get(kind, value))
    return " ".join(out)


NAMES = ["p", "q", "r"]

test_cases = [
    "p",
    "~p",
    "p & q",
    "p | q",
    "p & q | r",              # & binds tighter, so this is (p & q) | r
    "p & (q | r)",            # needs the parentheses to mean the same thing
    "~p & q | r",             # ~ binds tightest
    "~(p & q) | r",
    "p & q & r",
    "~p & ~q | ~r & (p | q)",
]

print("=" * 68)
print("(a) the parser agrees with Python's own reading of the same text")
print("=" * 68)
print()
print(f"{'text':<24} {'parsed as':<40} {'agrees':>7}")
all_agree = True
for text in test_cases:
    formula = parse(text)
    source = to_python_source(text)
    mismatches = 0
    for b in itertools.product([False, True], repeat=3):
        assignment = dict(zip(NAMES, b))
        mine = bool(formula.evaluate(assignment))
        theirs = bool(eval(source, dict(assignment)))
        if mine != theirs:
            mismatches += 1
    all_agree = all_agree and mismatches == 0
    print(f"{text:<24} {repr(formula):<40} {mismatches == 0:>7}")

print()
print("the python source each row was compared against:")
for text in test_cases:
    print(f"  {text:<24} -> {to_python_source(text)}")
print()
print(f"all ten agree on all 8 assignments: {all_agree}")

print()
print("=" * 68)
print("(b) precedence: ~ before & before |")
print("=" * 68)
print()
for text in ("~p & q", "~(p & q)", "p & q | r", "p | q & r"):
    print(f"  {text:<12} parses to {parse(text)!r}")
print()
print("If ~ bound loosely, '~p & q' would parse as ~(p & q). Compare columns:")
print(f"  (~p) & q   {bits(column(parse('~p & q'), NAMES))}")
print(f"  ~(p & q)   {bits(column(parse('~(p & q)'), NAMES))}")
print("Different columns, so the precedence is observable, and it is the tight")
print("one. This is the same rule as Python's own precedence table.")

print()
print("=" * 68)
print("(c) p -> q is the same formula as ~p | q")
print("=" * 68)
print()
imp_formula = parse("p -> q")
or_formula = parse("~p | q")
print(f"  p -> q   {imp_formula!r}   column {bits(column(imp_formula, NAMES))}")
print(f"  ~p | q   {or_formula!r}   column {bits(column(or_formula, NAMES))}")
print(f"  equivalent: {column(imp_formula, NAMES) == column(or_formula, NAMES)}")
print()
print("So a parser needs no special token for the arrow: NOT and OR already")
print("express it. That is why Python has no implication operator, and why")
print("anyone writing an implication in code writes 'if not p or q'.")

print()
print("=" * 68)
print("(d) -> is right-associative")
print("=" * 68)
print()
print(f"  p -> q -> r       parses to {parse('p -> q -> r')!r}")
print(f"  (p -> q) -> r     parses to {parse('(p -> q) -> r')!r}")
print()
print(f"  column of the first  : {bits(column(parse('p -> q -> r'), NAMES))}")
print(f"  column of the second : {bits(column(parse('(p -> q) -> r'), NAMES))}")
print()
print("Different formulas, so associativity was a choice and the wrong one is a")
print("real bug. Right-associative is correct because it reads like a nested")
print("if: 'if p then (if q then r)'.")
```

Output:

```
(a) the parser agrees with Python's own reading of the same text

text                     parsed as                                 agrees
p                        p                                              1
~p                       ~p                                             1
p & q                    (p & q)                                        1
p | q                    (p | q)                                        1
p & q | r                ((p & q) | r)                                  1
p & (q | r)              (p & (q | r))                                  1
~p & q | r               ((~p & q) | r)                                 1
~(p & q) | r             (~(p & q) | r)                                 1
p & q & r                ((p & q) & r)                                  1
~p & ~q | ~r & (p | q)   ((~p & ~q) | (~r & (p | q)))                   1

the python source each row was compared against:
  p                        -> p
  ~p                       -> not p
  p & q                    -> p and q
  p | q                    -> p or q
  p & q | r                -> p and q or r
  p & (q | r)              -> p and ( q or r )
  ~p & q | r               -> not p and q or r
  ~(p & q) | r             -> not ( p and q ) or r
  p & q & r                -> p and q and r
  ~p & ~q | ~r & (p | q)   -> not p and not q or not r and ( p or q )

all ten agree on all 8 assignments: True

(b) precedence: ~ before & before |
  ~p & q       parses to (~p & q)
  ~(p & q)     parses to ~(p & q)
  p & q | r    parses to ((p & q) | r)
  p | q & r    parses to (p | (q & r))
  (~p) & q   00110000
  ~(p & q)   11111100

(c) p -> q is the same formula as ~p | q
  p -> q   (p -> q)   column 11110011
  ~p | q   (~p | q)   column 11110011
  equivalent: True

(d) -> is right-associative
  p -> q -> r       parses to (p -> (q -> r))
  (p -> q) -> r     parses to ((p -> q) -> r)

  column of the first  : 11111101
  column of the second : 01011101
```

Part (d) is the one to slow down on. `p -> q -> r` and `(p -> q) -> r` are
different formulas with different columns, so associativity was a decision and
the wrong choice is a real bug that would survive any test you happened to write.
Right-associative is right because the arrow reads like a nested `if`.

</details>

**[ ] Exercise 4 — Prove the equivalence laws by exhaustion, and settle the
converse question.** (a) Write out the four rows of `p` and `q`, and report the
truth column of each of `¬p ∧ q`, `p ∨ q`, `p → q`, and `p ↔ q`. (b) For each
law below, verify it under all four assignments and report the two columns side
by side: double negation, commutativity of `∧` and `∨`, idempotence, absorption,
`p → q ≡ ¬p ∨ q`, both De Morgan laws, and `p ↔ q ≡ (p → q) ∧ (q → p)`. (c)
Compute the columns for `p → q`, its contrapositive `¬q → ¬p`, and its converse
`¬p → ¬q`, and state which pair is equivalent. (d) Give the specific assignment
that separates the converse from the original.

<details>
<summary>Solution</summary>

```python
import itertools


# ---------------------------------------------------------------------------
# The equivalence laws, checked exhaustively. For each one, the identity must
# hold under EVERY assignment, not most of them. 'Holds everywhere' is the
# definition of a tautology, and a tautology is what licenses a rewrite.
# ---------------------------------------------------------------------------

ATOMS = ["p", "q"]


def all_assignments(names):
    for values in itertools.product([False, True], repeat=len(names)):
        yield dict(zip(names, values))


def truth_table(formula, names):
    """Return the truth column as a string of 1s and 0s, in row order."""
    return "".join(
        "1" if formula(a) else "0"
        for a in all_assignments(names)
    )


# --- 1. The four rows we actually use -----------------------------------
print("1. The four rows, and which connectives are true in each")
print(f"  {'p':>3} {'q':>3} {'~p & q':>7} {'p | q':>7} {'p -> q':>7} {'p <-> q':>9}")
for a in all_assignments(ATOMS):
    p, q = a["p"], a["q"]
    print(f"  {int(p):>3} {int(q):>3} {int((not p) and q):>7} "
          f"{int(p or q):>7} {int((not p) or q):>7} {int(p == q):>9}")
print()
print("  Conjunction has one true row. Disjunction has three. Implication has")
print("  three, and its only false row is p=1, q=0 -- which is why")
print("  `p -> q` and `~p | q` are the same proposition.")

print()
print("2. The equivalence laws, each checked on all 4 assignments")


def check(name, left, right):
    """Verify left == right everywhere; report the truth columns side by side."""
    lt, rt = truth_table(left, ATOMS), truth_table(right, ATOMS)
    print(f"  {name:<34} {lt}  ==  {rt}   {'ok' if lt == rt else 'MISMATCH'}")
    return lt == rt


laws = [
    ("double negation",     lambda a: not not a["p"],
     lambda a: a["p"]),
    ("P & Q  ==  Q & P",    lambda a: a["p"] and a["q"],
     lambda a: a["q"] and a["p"]),
    ("P | Q  ==  Q | P",    lambda a: a["p"] or a["q"],
     lambda a: a["q"] or a["p"]),
    ("P & P  ==  P",        lambda a: a["p"] and a["p"],
     lambda a: a["p"]),
    ("P | P  ==  P",        lambda a: a["p"] or a["p"],
     lambda a: a["p"]),
    ("P | (P & Q) == P",    lambda a: a["p"] or (a["p"] and a["q"]),
     lambda a: a["p"]),
    ("P & (P | Q) == P",    lambda a: a["p"] and (a["p"] or a["q"]),
     lambda a: a["p"]),
    ("P -> Q  ==  ~P | Q",  lambda a: (not a["p"]) or a["q"],
     lambda a: (not a["p"]) or a["q"]),
    ("~(P & Q) == ~P | ~Q", lambda a: not (a["p"] and a["q"]),
     lambda a: (not a["p"]) or (not a["q"])),
    ("~(P | Q) == ~P & ~Q", lambda a: not (a["p"] or a["q"]),
     lambda a: (not a["p"]) and (not a["q"])),
    ("P <-> Q == (P->Q)&(Q->P)", lambda a: a["p"] == a["q"],
     lambda a: ((not a["p"]) or a["q"]) and ((not a["q"]) or a["p"])),
]

all_ok = True
for name, left, right in laws:
    all_ok &= check(name, left, right)

# Associativity needs three atoms, so it gets its own table.
three = ["p", "q", "r"]
assoc_l = "".join("1" if ((a["p"] and a["q"]) and a["r"]) else "0"
                  for a in all_assignments(three))
assoc_r = "".join("1" if (a["p"] and (a["q"] and a["r"])) else "0"
                  for a in all_assignments(three))
print()
print(f"  {'(P & Q) & R == P & (Q & R)':<34} {assoc_l}  ==  {assoc_r}"
      f"   {'ok' if assoc_l == assoc_r else 'MISMATCH'}")
all_ok &= assoc_l == assoc_r
print()
print(f"  every law holds on every assignment: {all_ok}")
print()
print("  These are tautologies: true under every assignment. A tautology is")
print("  exactly what makes a rewrite safe, because substituting one side for")
print("  the other cannot change a formula's value in any context. Note that")
print("  the columns for absorption, idempotence and double negation are all")
print("  `0011` -- the column of `p` itself, which is the signature of a law")
print("  that says 'this simplifies to P'.")

print()
print("3. Converse, contrapositive, inverse -- three different formulas")
print(f"  {'p':>3} {'q':>3} {'P->Q':>6} {'~Q->~P contra':>17} {'~P->~Q converse':>19}")
columns = []
for a in all_assignments(ATOMS):
    p, q = a["p"], a["q"]
    forward = (not p) or q
    contra = q or (not p)
    converse = p or (not q)
    columns.append((forward, contra, converse))
    print(f"  {int(p):>3} {int(q):>3} {int(forward):>6} {int(contra):>17} "
          f"{int(converse):>19}")
same_as_forward = all(f == c for f, c, _ in columns)
same_as_converse = all(f == v for f, _, v in columns)
print()
print(f"  the contrapositive matches P -> Q      : {same_as_forward}")
print(f"  the converse matches P -> Q            : {same_as_converse}")
print()
p, q, f, v = next(
    (a["p"], a["q"], row[0], row[2])
    for a, row in zip(all_assignments(ATOMS), columns)
    if row[0] != row[2])
print(f"  (d) The separating assignment is p={int(p)}, q={int(q)}:")
print(f"        P -> Q   = {int(f)}   (true: the premise is false)")
print(f"        ~P -> ~Q = {int(v)}   (false: P is true and ~Q is false)")
print()
print("  One is true and the other false, so they are not equivalent. The")
print("  contrapositive, by contrast, has the identical column in every row,")
print("  which is why proving the contrapositive proves the original -- the")
print("  technique Lesson 13 builds on.")
```

Output:

```text
1. The four rows, and which connectives are true in each
    p   q  ~p & q   p | q  p -> q   p <-> q
    0   0       0       0       1         1
    0   1       1       1       1         0
    1   0       0       1       0         0
    1   1       0       1       1         1

  Conjunction has one true row. Disjunction has three. Implication has
  three, and its only false row is p=1, q=0 -- which is why
  `p -> q` and `~p | q` are the same proposition.

2. The equivalence laws, each checked on all 4 assignments
  double negation                    0011  ==  0011   ok
  P & Q  ==  Q & P                   0001  ==  0001   ok
  P | Q  ==  Q | P                   0111  ==  0111   ok
  P & P  ==  P                       0011  ==  0011   ok
  P | P  ==  P                       0011  ==  0011   ok
  P | (P & Q) == P                   0011  ==  0011   ok
  P & (P | Q) == P                   0011  ==  0011   ok
  P -> Q  ==  ~P | Q                 1101  ==  1101   ok
  ~(P & Q) == ~P | ~Q                1110  ==  1110   ok
  ~(P | Q) == ~P & ~Q                1000  ==  1000   ok
  P <-> Q == (P->Q)&(Q->P)           1001  ==  1001   ok

  (P & Q) & R == P & (Q & R)         00000001  ==  00000001   ok

  every law holds on every assignment: True

  These are tautologies: true under every assignment. A tautology is
  exactly what makes a rewrite safe, because substituting one side for
  the other cannot change a formula's value in any context. Note that
  the columns for absorption, idempotence and double negation are all
  `0011` -- the column of `p` itself, which is the signature of a law
  that says 'this simplifies to P'.

3. Converse, contrapositive, inverse -- three different formulas
    p   q   P->Q     ~Q->~P contra     ~P->~Q converse
    0   0      1                 1                   1
    0   1      1                 1                   0
    1   0      0                 0                   1
    1   1      1                 1                   1

  the contrapositive matches P -> Q      : True
  the converse matches P -> Q            : False

  (d) The separating assignment is p=0, q=1:
        P -> Q   = 1   (true: the premise is false)
        ~P -> ~Q = 0   (false: P is true and ~Q is false)

  One is true and the other false, so they are not equivalent. The
  contrapositive, by contrast, has the identical column in every row,
  which is why proving the contrapositive proves the original -- the
  technique Lesson 13 builds on.
```

The rows to read off carefully are the two where `p` is false. Both `p → q` and
`¬p ∧ ¬q` are true there regardless of `q`, which is the vacuous-truth case and
the reason implication cannot be read as conjunction.

</details>

**[ ] Exercise 5 — Audit four conditions mechanically, and separate "wrong"
from "wrong only on rows the system cannot reach".** Write a helper that takes
a requirement and a code condition as functions of a dictionary of booleans,
enumerates every assignment, and returns the assignments where they disagree.
Then use it on: (1) "deny unless admin or superuser", (2) "return 400 if the
request is malformed **or** unauthenticated", (3) "retry if the request failed
**and** was idempotent", (4) "grant access if the user is an admin **or** the
resource is public **and** not archived". For each: print both truth columns,
state the disagreement count, and diagnose whether the connective is wrong or
only the grouping. Finally, re-run case 4 under the invariant that a public
resource is never archived, and report the reachable and unreachable
disagreement counts separately.

<details>
<summary>Solution</summary>

The whole exercise is four lines of machinery and then a column comparison per
condition. The count of disagreeing rows is the diagnostic: a condition that
disagrees on most rows has the wrong connective, while one that disagrees on a
few rows with the same shape has the wrong grouping.

```python
import itertools


# ---------------------------------------------------------------------------
# A checker for a small condition language. The point is not the parser, it is
# that you can hand the checker a REQUIREMENT and the CODE and get told whether
# they agree -- mechanically, on every row, with no reading involved.
# ---------------------------------------------------------------------------

def rows(names):
    for values in itertools.product([False, True], repeat=len(names)):
        yield dict(zip(names, values))


def column(formula, names):
    return tuple(1 if formula(a) else 0 for a in rows(names))


def find_disagreements(requirement, code, names):
    """Every assignment where requirement and code differ."""
    bad = []
    for a in rows(names):
        want, got = requirement(a), code(a)
        if want != got:
            bad.append((a, want, got))
    return bad


def report(label, requirement, code, names):
    bad = find_disagreements(requirement, code, names)
    total = 1 << len(names)
    print(f"  {label}")
    print(f"    requirement column : {column(requirement, names)}")
    print(f"    code column        : {column(code, names)}")
    print(f"    rows               : {total}")
    print(f"    disagreements      : {len(bad)}")
    if bad:
        print("    the disagreeing assignments:")
        shown = 0
        for a, want, got in bad:
            if shown == 4:
                print(f"      ... and {len(bad) - shown} more")
                break
            print(f"      {a}  want={int(want)}  got={int(got)}")
            shown += 1
    print()
    return bad


print("Four conditions, each as requirement against code.")
print("Read the two columns side by side: an all-1s requirement against an")
print("all-0s code is a condition that never fires, which is the failure mode")
print("in case 2.")
print()

# 1. "deny unless admin or superuser"
report(
    "1. deny unless admin or superuser",
    lambda a: not (a["is_admin"] or a["is_superuser"]),
    lambda a: (not a["is_admin"]) or (not a["is_superuser"]),
    ["is_admin", "is_superuser"])

# 2. "return 400 if malformed OR unauthenticated"
report(
    "2. 400 if malformed or unauthenticated",
    lambda a: (not a["well_formed"]) or (not a["authed"]),
    lambda a: (not a["well_formed"]) and (not a["authed"]),
    ["well_formed", "authed"])

# 3. "retry if failed AND idempotent"
report(
    "3. retry if failed and idempotent",
    lambda a: a["failed"] and a["idempotent"],
    lambda a: (not a["failed"]) or (not a["idempotent"]),
    ["failed", "idempotent"])

# 4. "grant if admin OR (public AND not archived)"
report(
    "4. grant if admin or (public and not archived)",
    lambda a: a["is_admin"] or (a["resource_public"] and not a["archived"]),
    lambda a: (a["is_admin"] or a["resource_public"]) and not a["archived"],
    ["is_admin", "resource_public", "archived"])

print("5. What Python actually computes for the same source text")
print("   Python binds `not` tighter than `or`, so these are the same formula:")
print(f"     not a or not b     -> "
      f"{column(lambda a: (not a['p']) or (not a['q']), ['p', 'q'])}")
print(f"     (not a) or (not b) -> "
      f"{column(lambda a: (not a['p']) or (not a['q']), ['p', 'q'])}")
print("   and this is a different formula, the one the author meant:")
print(f"     not (a or b)       -> "
      f"{column(lambda a: not (a['p'] or a['q']), ['p', 'q'])}")
print()
print("   The first two evaluate 'at least one privilege is missing'. The")
print("   third evaluates 'neither privilege is held'. Two of four rows")
print("   differ, and both are rows where exactly one privilege is held --")
print("   the entire population the check exists to serve.")
print()

print("6. Safe rewrites, tested by comparing columns rather than by eye")
require = lambda a: not (a["is_admin"] or a["is_superuser"])
names = ["is_admin", "is_superuser"]
base = column(require, names)
spellings = [
    ("not (a or s)",                   lambda a: not (a["is_admin"] or a["is_superuser"])),
    ("not a and not s",                lambda a: (not a["is_admin"]) and (not a["is_superuser"])),
    ("not (a or s or False)",          lambda a: not (a["is_admin"] or a["is_superuser"] or False)),
    ("not a and not s and not False",  lambda a: (not a["is_admin"]) and (not a["is_superuser"]) and not False),
    ("THE WRONG ONE: not a or not s",  lambda a: (not a["is_admin"]) or (not a["is_superuser"])),
]
print(f"     {'requirement':<38} {base}  baseline")
for label, fn in spellings:
    col = column(fn, names)
    tag = "same" if col == base else "DIFFERENT"
    print(f"     {label:<38} {col}  {tag}")
print()
print("   The four correct spellings have the same column as the requirement")
print("   and the wrong one does not. That is the entire test, and it takes")
print("   one line. No cleverness is required, only the columns.")
print()

print("7. Reachability changes the question, so report both counts")
print("   Everything above assumes any combination of flags is reachable.")
print("   Suppose the system guarantees public implies not archived:")
guaranteed = lambda a: not (a["resource_public"] and a["archived"])
names3 = ["is_admin", "resource_public", "archived"]
bad = find_disagreements(
    lambda a: a["is_admin"] or (a["resource_public"] and not a["archived"]),
    lambda a: (a["is_admin"] or a["resource_public"]) and not a["archived"],
    names3)
print(f"   rows in the table                    : {1 << len(names3)}")
print(f"   rows the invariant makes unreachable : "
      f"{sum(1 for a in rows(names3) if not guaranteed(a))}")
print(f"   total disagreements                  : {len(bad)}")
print(f"   disagreements on reachable rows      : "
      f"{sum(1 for a, _, _ in bad if guaranteed(a))}")
print(f"   disagreements on unreachable rows    : "
      f"{sum(1 for a, _, _ in bad if not guaranteed(a))}")
print()
print("   The two counts answer different questions. The reachable count says")
print("   whether the code is right where it can actually run. The")
print("   unreachable count says whether the code is wrong at all: a")
print("   disagreement on an unreachable row is still a disagreement with the")
print("   specification, and it goes live the moment someone relaxes the")
print("   invariant. Reporting only the reachable count hides a real defect;")
print("   reporting only the total count cries wolf on rows that cannot occur.")
```

Output:

```text
Four conditions, each as requirement against code.
Read the two columns side by side: an all-1s requirement against an
all-0s code is a condition that never fires, which is the failure mode
in case 2.

  1. deny unless admin or superuser
    requirement column : (1, 0, 0, 0)
    code column        : (1, 1, 1, 0)
    rows               : 4
    disagreements      : 2
    the disagreeing assignments:
      {'is_admin': False, 'is_superuser': True}  want=0  got=1
      {'is_admin': True, 'is_superuser': False}  want=0  got=1

  2. 400 if malformed or unauthenticated
    requirement column : (1, 1, 1, 0)
    code column        : (1, 0, 0, 0)
    rows               : 4
    disagreements      : 2
    the disagreeing assignments:
      {'well_formed': False, 'authed': True}  want=1  got=0
      {'well_formed': True, 'authed': False}  want=1  got=0

  3. retry if failed and idempotent
    requirement column : (0, 0, 0, 1)
    code column        : (1, 1, 1, 0)
    rows               : 4
    disagreements      : 4
    the disagreeing assignments:
      {'failed': False, 'idempotent': False}  want=0  got=1
      {'failed': False, 'idempotent': True}  want=0  got=1
      {'failed': True, 'idempotent': False}  want=0  got=1
      {'failed': True, 'idempotent': True}  want=1  got=0

  4. grant if admin or (public and not archived)
    requirement column : (0, 0, 1, 0, 1, 1, 1, 1)
    code column        : (0, 0, 1, 0, 1, 0, 1, 0)
    rows               : 8
    disagreements      : 2
    the disagreeing assignments:
      {'is_admin': True, 'resource_public': False, 'archived': True}  want=1  got=0
      {'is_admin': True, 'resource_public': True, 'archived': True}  want=1  got=0

5. What Python actually computes for the same source text
   Python binds `not` tighter than `or`, so these are the same formula:
     not a or not b     -> (1, 1, 1, 0)
     (not a) or (not b) -> (1, 1, 1, 0)
   and this is a different formula, the one the author meant:
     not (a or b)       -> (1, 0, 0, 0)

   The first two evaluate 'at least one privilege is missing'. The
   third evaluates 'neither privilege is held'. Two of four rows
   differ, and both are rows where exactly one privilege is held --
   the entire population the check exists to serve.

6. Safe rewrites, tested by comparing columns rather than by eye
     requirement                            (1, 0, 0, 0)  baseline
     not (a or s)                           (1, 0, 0, 0)  same
     not a and not s                        (1, 0, 0, 0)  same
     not (a or s or False)                  (1, 0, 0, 0)  same
     not a and not s and not False          (1, 0, 0, 0)  same
     THE WRONG ONE: not a or not s          (1, 1, 1, 0)  DIFFERENT

   The four correct spellings have the same column as the requirement
   and the wrong one does not. That is the entire test, and it takes
   one line. No cleverness is required, only the columns.

7. Reachability changes the question, so report both counts
   Everything above assumes any combination of flags is reachable.
   Suppose the system guarantees public implies not archived:
   rows in the table                    : 8
   rows the invariant makes unreachable : 2
   total disagreements                  : 2
   disagreements on reachable rows      : 1
   disagreements on unreachable rows    : 1

   The two counts answer different questions. The reachable count says
   whether the code is right where it can actually run. The
   unreachable count says whether the code is wrong at all: a
   disagreement on an unreachable row is still a disagreement with the
   specification, and it goes live the moment someone relaxes the
   invariant. Reporting only the reachable count hides a real defect;
   reporting only the total count cries wolf on rows that cannot occur.
```

**Diagnoses.** Case 1 disagrees on two of four rows, both with exactly one
privilege held, which is the De Morgan mistake with the wrong connective. Case
2's requirement column is all 1s except one row while the code's column is 1
only on the first row: the condition almost never fires, so malformed *and*
authenticated requests pass. That is the worst shape of this bug, because it
fails **open** — a request that should have been rejected is served. Case 3
disagrees on all four rows, the signature of both connectives being wrong at
once: it retries every request that succeeded and none that failed. Case 4
disagrees on two of eight rows, both with `is_admin` true and `archived` true,
which points at the grouping rather than a wholesale connective swap: the code
requires `not archived` of the whole disjunction rather than only of the public
branch.

</details>

**[ ] Exercise 6 — Build a formula library and use it to settle four questions
you would otherwise argue about.** (a) Implement `Var`, `Not`, `And`, `Or`,
`Implies`, and `Iff` so that each builds a formula object, each formula knows
which variables occur in it, and each formula evaluates under a complete
assignment. (b) Using those, check mechanically that `p → q ≡ ¬p ∨ q`, that
`p ∧ q ≢ p ∨ q`, that `p ∧ q ≢ p → q`, and that
`p ↔ q ≡ (p → q) ∧ (q → p)`. (c) Take the requirement "admin, or superuser and
not archived", then test four candidate rewrites plus two correct ones against
it by comparing truth columns, and say which are safe. (d) Implement negation
two ways — by reading the definition of each connective, and by De Morgan — and
check that they agree. (e) Classify ten formulas as tautology, contradiction,
or contingent from their columns alone.

<details>
<summary>Solution</summary>

Building formulas as objects rather than strings is what makes this mechanical.
`evaluate` walks the tree, `variables` tells you how big the table needs to be,
and `repr` gives you something to print. Once `column` exists, every question in
the exercise is a string comparison.

```python
import itertools


# ---------------------------------------------------------------------------
# A tiny formula language: build formulas as objects, evaluate them under an
# assignment, and print them. The point of building objects rather than strings
# is that equality becomes structural, so 'are these two conditions the same?'
# has an answer a machine can give.
# ---------------------------------------------------------------------------

class Formula:
    """Base class. Operators build new formulas; nothing is evaluated here."""

    def variables(self):
        """Every variable occurring anywhere in this formula."""
        raise NotImplementedError

    def evaluate(self, assignment):
        """The truth value under a complete assignment."""
        raise NotImplementedError


class Var(Formula):
    def __init__(self, name):
        self.name = name

    def variables(self):
        return {self.name}

    def evaluate(self, a):
        return a[self.name]

    def __repr__(self):
        return self.name


class Not(Formula):
    def __init__(self, inner):
        self.inner = inner

    def variables(self):
        return self.inner.variables()

    def evaluate(self, a):
        return not self.inner.evaluate(a)

    def __repr__(self):
        return f"~{self.inner!r}"


class And(Formula):
    def __init__(self, *parts):
        self.parts = list(parts)

    def variables(self):
        out = set()
        for part in self.parts:
            out |= part.variables()
        return out

    def evaluate(self, a):
        return all(part.evaluate(a) for part in self.parts)

    def __repr__(self):
        return "(" + " & ".join(repr(p) for p in self.parts) + ")"


class Or(Formula):
    def __init__(self, *parts):
        self.parts = list(parts)

    def variables(self):
        out = set()
        for part in self.parts:
            out |= part.variables()
        return out

    def evaluate(self, a):
        return any(part.evaluate(a) for part in self.parts)

    def __repr__(self):
        return "(" + " | ".join(repr(p) for p in self.parts) + ")"


class Implies(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def variables(self):
        return self.left.variables() | self.right.variables()

    def evaluate(self, a):
        # Implication is 'not p, or q'. Never evaluate the right side when the
        # left is false -- the same short circuit the language gives you.
        return (not self.left.evaluate(a)) or self.right.evaluate(a)

    def __repr__(self):
        return f"({self.left!r} -> {self.right!r})"


class Iff(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def variables(self):
        return self.left.variables() | self.right.variables()

    def evaluate(self, a):
        return self.left.evaluate(a) == self.right.evaluate(a)

    def __repr__(self):
        return f"({self.left!r} <-> {self.right!r})"


def all_assignments(names):
    """Every assignment to `names`, as a list of dicts."""
    return [dict(zip(names, values))
            for values in itertools.product([False, True], repeat=len(names))]


def column(formula):
    """The truth column of `formula`, as a tuple of 0s and 1s."""
    names = sorted(formula.variables())
    return tuple(1 if formula.evaluate(a) else 0
                 for a in all_assignments(names))


def equivalent(f, g):
    """True exactly when f and g agree under every assignment."""
    return column(f) == column(g)


def show(label, formula):
    print(f"  {label:<44} {''.join(str(c) for c in column(formula))}"
          f"   {formula!r}")
    return column(formula)


p, q, r = Var("p"), Var("q"), Var("r")

print("1. The same condition, several spellings")
print("   Equal columns mean the conditions are interchangeable.")
show("p -> q", Implies(p, q))
show("~p | q", Or(Not(p), q))
print(f"   p -> q  and  ~p | q  equivalent : "
      f"{equivalent(Implies(p, q), Or(Not(p), q))}")
print(f"   their columns are identical      : "
      f"{column(Implies(p, q)) == column(Or(Not(p), q))}")
print()
print(f"   ~p & q and p | q equivalent       : "
      f"{equivalent(And(Not(p), q), Or(p, q))}")
print(f"   p & q  and p | q  equivalent      : "
      f"{equivalent(And(p, q), Or(p, q))}")
print(f"   p & q  and p -> q  equivalent     : "
      f"{equivalent(And(p, q), Implies(p, q))}")
print(f"   p <-> q and (p->q)&(q->p) equal   : "
      f"{equivalent(Iff(p, q), And(Implies(p, q), Implies(q, p)))}")
print(f"   p <-> q and p | q     equivalent   : "
      f"{equivalent(Iff(p, q), Or(p, q))}")
print()
print("   The last two lines are the ones worth remembering. `p & q` is NOT")
print("   `p -> q`, and `p <-> q` is NOT `p | q`. Both pairs differ on exactly")
print("   one row, which is the row a careless reading skips.")
print()

print("2. Equivalence as a decidable question, not an intuition")
ADMIN, SUPER, ARCHIVED = Var("is_admin"), Var("is_superuser"), Var("archived")
requirement = Or(ADMIN, And(SUPER, Not(ARCHIVED)))
candidates = {
    "requirement: a | (s & ~v)": requirement,
    "safe:  ~(~a & (~s | v))":   Not(And(Not(ADMIN), Or(Not(SUPER), ARCHIVED))),
    "safe:  (a | s) & (a | ~v)": And(Or(ADMIN, SUPER), Or(ADMIN, Not(ARCHIVED))),
    "wrong: (a | s) & ~v":       And(Or(ADMIN, SUPER), Not(ARCHIVED)),
    "wrong: a | (s & v)":        Or(ADMIN, And(SUPER, ARCHIVED)),
    "wrong: a & (s | ~v)":       And(ADMIN, Or(SUPER, Not(ARCHIVED))),
    "wrong: ~(~a & ~s) | v":     Or(Not(And(Not(ADMIN), Not(SUPER))), ARCHIVED),
}
base = column(requirement)
print(f"  {'candidate':<32} {'column':<9} verdict")
safe_count = wrong_count = 0
for label, f in candidates.items():
    col = column(f)
    if col == base:
        verdict, safe_count = "equivalent", safe_count + 1
    else:
        verdict, wrong_count = "NOT equivalent", wrong_count + 1
    print(f"  {label:<32} {''.join(str(c) for c in col):<9} {verdict}")
print()
print(f"  equivalent rewrites: {safe_count}, wrong ones: {wrong_count}")
print()
print(f"  variables in the requirement : {sorted(requirement.variables())}")
print(f"  size of the table             : "
      f"{1 << len(requirement.variables())} rows")
print()
print("   This is the mechanical form of 'is that rewrite safe?'. You do not")
print("   have to be careful; you have to run the columns.")
print()

print("3. Negation, computed rather than guessed")
print("   `structural_negate` builds the negation by walking the tree. De")
print("   Morgan says it should agree with `demorgan_negate`, which flips")
print("   connectives and pushes the negation inward. Compare the columns.")


def structural_negate(f):
    """The negation built from the truth-table definition of each connective.

    Each case is read straight off the definition: a conjunction is false
    when either side is false, so its negation mentions the whole conjunction.
    Note that the children are NOT negated here -- that would apply the rule
    twice and hand back the original formula.
    """
    if isinstance(f, Var):
        return Not(f)
    if isinstance(f, Not):
        return f.inner
    if isinstance(f, And):
        return Not(And(*f.parts))
    if isinstance(f, Or):
        return Not(Or(*f.parts))
    if isinstance(f, Implies):
        return And(f.left, Not(f.right))
    if isinstance(f, Iff):
        return Or(And(f.left, Not(f.right)),
                  And(Not(f.left), f.right))
    raise TypeError(f)


def demorgan_negate(f):
    """The negation built by De Morgan: flip & to | and vice versa, recurse."""
    if isinstance(f, Var):
        return Not(f)
    if isinstance(f, Not):
        return f.inner
    if isinstance(f, And):
        return Or(*[demorgan_negate(part) for part in f.parts])
    if isinstance(f, Or):
        return And(*[demorgan_negate(part) for part in f.parts])
    if isinstance(f, Implies):
        return And(f.left, Not(f.right))
    if isinstance(f, Iff):
        return Or(And(f.left, Not(f.right)),
                  And(Not(f.left), f.right))
    raise TypeError(f)


negations = [
    ("p",            p),
    ("p & q",        And(p, q)),
    ("p | q",        Or(p, q)),
    ("p -> q",       Implies(p, q)),
    ("p <-> q",      Iff(p, q)),
    ("(p & q) | r",  Or(And(p, q), r)),
    ("(p | q) & ~r", And(Or(p, q), Not(r))),
    ("~p | q",       Or(Not(p), q)),
]
print(f"  {'formula':<14} {'column':<9} {'~f':<9} {'De Morgan ~f':<12} agree")
all_agree = True
for label, f in negations:
    col_f = column(f)
    col_s = column(structural_negate(f))
    col_d = column(demorgan_negate(f))
    agree = col_s == col_d == column(Not(f))
    all_agree &= agree
    print(f"  {label:<14} {''.join(map(str, col_f)):<9} "
          f"{''.join(map(str, col_s)):<9} {''.join(map(str, col_d)):<12} "
          f"{agree}")
print()
print(f"  De Morgan agrees with the truth-table definition everywhere: "
      f"{all_agree}")
print()
print("   The '~f' column is computed by recursion into the tree and the")
print("   'De Morgan ~f' column by flipping connectives. They are identical")
print("   in every row, which is why you can remember one rule instead of")
print("   building a negation routine -- and why, when the two disagree, the")
print("   recursion is the one to trust.")
print()
print("   Note `p -> q` and `~p | q` negate to the same formula, which is the")
print("   master identity restated as a computed fact rather than a thing to")
print("   memorise.")
print()

print("4. Tautology, contradiction, contingent -- decided mechanically")


def classify(f):
    """Decide which of the three classes f belongs to, from its column."""
    col = column(f)
    if all(col):
        return "tautology"
    if not any(col):
        return "contradiction"
    return "contingent"


samples = [
    ("p -> q", Implies(p, q)),
    ("~(p -> q)", Not(Implies(p, q))),
    ("(p & q) -> (p | q)", Implies(And(p, q), Or(p, q))),
    ("p -> (q -> p)", Implies(p, Implies(q, p))),
    ("~(p | q) -> (~p & ~q)", Implies(Not(Or(p, q)), And(Not(p), Not(q)))),
    ("p -> ~p", Implies(p, Not(p))),
    ("~p | p", Or(Not(p), p)),
    ("p & ~p", And(p, Not(p))),
    ("p <-> q", Iff(p, q)),
    ("p | ~p", Or(p, Not(p))),
]
print(f"  {'formula':<26} {'column':<9} class")
for label, f in samples:
    print(f"  {label:<26} {''.join(str(c) for c in column(f)):<9} "
          f"{classify(f)}")
print()
print("   `p -> ~p` is contingent, not a contradiction, and that surprises")
print("   people. It is true whenever p is false, which is half the table.")
print("   The contradiction is `p & ~p`, and the tautology is `p | ~p`.")
print("   Both are listed above so the contrast is visible: a class is about")
print("   the whole column, not about one row.")
print()

print("5. Three variables, one table, every row accounted for")
three = [And(p, q), Or(q, r), Implies(p, Not(r)), Not(Or(p, r))]
combined = three[0]
for extra in three[1:]:
    combined = And(combined, extra)
print(f"  formula  : {combined!r}")
print(f"  variables : {sorted(combined.variables())}, so "
      f"{1 << len(combined.variables())} rows")
print(f"  class     : {classify(combined)}")
print()
print("  The whole procedure scales as 2^n, which is why nobody does this by")
print("  hand past a handful of variables -- and why a real solver uses")
print("  satisfiability search with propagation instead of enumeration. Same")
print("  space, better strategy. See Lesson 11's BDD section.")
```

Output:

```text
1. The same condition, several spellings
   Equal columns mean the conditions are interchangeable.
  p -> q                                       1101   (p -> q)
  ~p | q                                       1101   (~p | q)
   p -> q  and  ~p | q  equivalent : True
   their columns are identical      : True

   ~p & q and p | q equivalent       : False
   p & q  and p | q  equivalent      : False
   p & q  and p -> q  equivalent     : False
   p <-> q and (p->q)&(q->p) equal   : True
   p <-> q and p | q     equivalent   : False

   The last two lines are the ones worth remembering. `p & q` is NOT
   `p -> q`, and `p <-> q` is NOT `p | q`. Both pairs differ on exactly
   one row, which is the row a careless reading skips.

2. Equivalence as a decidable question, not an intuition
  candidate                        column    verdict
  requirement: a | (s & ~v)        01110011  equivalent
  safe:  ~(~a & (~s | v))          01110011  equivalent
  safe:  (a | s) & (a | ~v)        01110011  equivalent
  wrong: (a | s) & ~v              01110000  NOT equivalent
  wrong: a | (s & v)               00110111  NOT equivalent
  wrong: a & (s | ~v)              00110001  NOT equivalent
  wrong: ~(~a & ~s) | v            01111111  NOT equivalent

  equivalent rewrites: 3, wrong ones: 4

  variables in the requirement : ['archived', 'is_admin', 'is_superuser']
  size of the table             : 8 rows

   This is the mechanical form of 'is that rewrite safe?'. You do not
   have to be careful; you have to run the columns.

3. Negation, computed rather than guessed
   `structural_negate` builds the negation by walking the tree. De
   Morgan says it should agree with `demorgan_negate`, which flips
   connectives and pushes the negation inward. Compare the columns.
  formula        column    ~f        De Morgan ~f agree
  p              01        10        10           True
  p & q          0001      1110      1110         True
  p | q          0111      1000      1000         True
  p -> q         1101      0010      0010         True
  p <-> q        1001      0110      0110         True
  (p & q) | r    01010111  10101000  10101000     True
  (p | q) & ~r   00101010  11010101  11010101     True
  ~p | q         1101      0010      0010         True

  De Morgan agrees with the truth-table definition everywhere: True

   The '~f' column is computed by recursion into the tree and the
   'De Morgan ~f' column by flipping connectives. They are identical
   in every row, which is why you can remember one rule instead of
   building a negation routine -- and why, when the two disagree, the
   recursion is the one to trust.

   Note `p -> q` and `~p | q` negate to the same formula, which is the
   master identity restated as a computed fact rather than a thing to
   memorise.

4. Tautology, contradiction, contingent -- decided mechanically
  formula                    column    class
  p -> q                     1101      contingent
  ~(p -> q)                  0010      contingent
  (p & q) -> (p | q)         1111      tautology
  p -> (q -> p)              1111      tautology
  ~(p | q) -> (~p & ~q)      1111      tautology
  p -> ~p                    10        contingent
  ~p | p                     11        tautology
  p & ~p                     00        contradiction
  p <-> q                    1001      contingent
  p | ~p                     11        tautology

   `p -> ~p` is contingent, not a contradiction, and that surprises
   people. It is true whenever p is false, which is half the table.
   The contradiction is `p & ~p`, and the tautology is `p | ~p`.
   Both are listed above so the contrast is visible: a class is about
   the whole column, not about one row.

5. Three variables, one table, every row accounted for
  formula  : ((((p & q) & (q | r)) & (p -> ~r)) & ~(p | r))
  variables : ['p', 'q', 'r'], so 8 rows
  class     : contradiction

  The whole procedure scales as 2^n, which is why nobody does this by
  hand past a handful of variables -- and why a real solver uses
  satisfiability search with propagation instead of enumeration. Same
  space, better strategy. See Lesson 11's BDD section.
```

**What the columns settle.** Part (b)'s fourth and fifth lines are the ones that
change how you write code: `p ∧ q` and `p → q` have different columns, and
`p ↔ q` and `p ∨ q` have different columns, so neither pair is a legal
substitution. In part (c), three of the seven candidates match the requirement
and four do not; the four wrong ones all fail on the same two rows, where
`is_admin` is true and `archived` is true, which is precisely where the
grouping matters. In part (e), note that `p → ¬p` is *contingent*, not a
contradiction — it is true on every row where `p` is false, which is half the
table. That is the row a casual reading skips.

</details>
**Challenge — Decide whether conditions are correct, using reachability as well
as equivalence.** Take three conditions and, for each: (1) enumerate every input
combination, (2) mark which combinations are actually reachable, using invariants
of the system rather than wishful thinking, (3) compare the code's value with the
requirement's value on every reachable row, and (4) state what the code does on
the unreachable rows. Use a condition with an integer-valued input (such as
`page_size`), because modelling it as a plain boolean hides exactly the thing you
are trying to find. Then report: for each condition, how many rows were reachable,
how many mismatched, and whether any unreachable row was wrong.

<details>
<summary>Solution</summary>

```python
import itertools

# ---------------------------------------------------------------------------
# A truth table has one row per input combination. Some rows describe states
# the program can never be in, because some invariant rules them out.
# Unreachable rows do not need to match the requirement. That is where bugs
# hide, because a test suite only ever visits the reachable ones.
#
# page_size below is NOT a boolean. It takes the values 0 and 25, because 0 is
# the bad value and 25 the normal one, and modelling that with a plain bool is
# what stops you seeing the problem.
# ---------------------------------------------------------------------------

PAGE_SIZES = [0, 25]


def pagination_rows():
    return [{"has_more": m, "page_size": ps, "has_cursor": c}
            for m, c in itertools.product([False, True], repeat=2)
            for ps in PAGE_SIZES]


def report(title, all_rows, code_fn, reachable_fn, req_fn):
    print(title)
    keys = list(all_rows[0])
    header = "  ".join(f"{k:>12}" for k in keys)
    print(f"  {header}   code  required  match  reachable")
    print("  " + "-" * (13 * len(keys) + 33))

    reachable_mismatches = []
    unreachable_wrong = []
    reachable_count = 0
    for a in all_rows:
        code_value = code_fn(a)
        req_value = req_fn(a)
        ok = bool(code_value) == bool(req_value)
        reachable = reachable_fn(a)
        if reachable:
            reachable_count += 1
            if not ok:
                reachable_mismatches.append((a, code_value, req_value))
        elif not ok:
            unreachable_wrong.append((a, code_value, req_value))
        cells = "  ".join(f"{str(a[k]):>12}" for k in keys)
        print(f"  {cells}   {str(code_value):>4}    {str(req_value):>7}"
              f"   {'ok ' if ok else 'BUG'}  {'yes' if reachable else 'NO':>3}")
    return reachable_count, reachable_mismatches, unreachable_wrong


def pagination_code(a):
    """As written. It adds a page_size guard nobody asked for."""
    return a["has_more"] and a["has_cursor"] and a["page_size"] > 0


def pagination_required(a):
    """More pages remain, and we have a cursor to continue from."""
    return a["has_more"] and a["has_cursor"]


ROWS = pagination_rows()

# The invariant: page_size comes from a constant, so it is never zero.
page_size_is_valid = lambda a: a["page_size"] > 0

print("=" * 74)
print("Case A: the invariant holds, so page_size is never zero")
print("=" * 74)
print()
print("code:    if has_more and has_cursor and page_size > 0:")
print("wanted:  if has_more and has_cursor:")
print()
r = report("", ROWS, pagination_code, page_size_is_valid, pagination_required)
print()
print(f"rows in the raw table              : {len(ROWS)}")
print(f"rows the invariant makes reachable : {r[0]}")
print(f"mismatches among reachable rows    : {len(r[1])}")
print(f"mismatches among unreachable rows  : {len(r[2])}")
print()
print("Verdict: correct in practice, wrong in general.")
print()
print("Every reachable row agrees. The unreachable wrong row has page_size == 0,")
print("which the invariant excludes, and in it the extra conjunct silently")
print("stops the fetch. The code is buggy and the table is right; the only")
print("thing standing between them is an assumption about where page_size")
print("comes from.")
print()
print("The moment someone reads page_size from a query parameter, or a config")
print("file that can be zero, or a user's saved preference, the invariant")
print("breaks. The endpoint then returns zero rows to a caller that expected a")
print("page, and the caller sees a valid empty response rather than an error.")
print("That is the worst failure mode a paginated API can have.")
print()

print("=" * 74)
print("Case B: the same guard once page_size can be zero")
print("=" * 74)
print()
r = report("", ROWS, pagination_code, lambda a: True, pagination_required)
print()
print(f"reachable rows now : {r[0]}")
print(f"mismatches now     : {len(r[1])}")
print()
print("Identical code, identical requirement. One row moved from 'unreachable")
print("and wrong' to 'reachable and wrong'. Nothing in the code changed; the")
print("only difference is whether the reader still believes an assumption about")
print("the caller. That is what the reachability column buys you: it turns an")
print("assumption into a line you can go and check.")
print()

print("=" * 74)
print("Case C: a rate limiter, where the bug is a connectiveswap")
print("=" * 74)
print()
print("code:    if over_limit or is_write or not has_credit:   # throttle")
print("wanted:  if over_limit and is_write and not has_credit:")
print()

L4 = ["over_limit", "is_write", "has_credit"]
RATE_ROWS = [dict(zip(L4, b)) for b in itertools.product([False, True], repeat=3)]


def rate_code(a):
    return a["over_limit"] or a["is_write"] or (not a["has_credit"])


def rate_required(a):
    return a["over_limit"] and a["is_write"] and not a["has_credit"]


# No invariant prunes anything: every combination occurs in real traffic.
r4 = report("", RATE_ROWS, rate_code, lambda a: True, rate_required)
print()
print(f"{len(RATE_ROWS)} rows, {len(r4[1])} reachable mismatches, "
      f"{len(r4[2])} unreachable mismatches.")
print()
print("No invariant saves this one, so every row is live and six of the eight")
print("disagree. Concretely: a READ request that is not over the limit and does")
print("have credit still gets throttled, because `is_write` alone makes the")
print("disjunction true. Roughly nine requests in ten are reads, so this rate")
print("limiter throttles most of all traffic on a perfectly healthy day.")
print()
print("The three questions, answered")
print()
print("  1. Which rows are reachable? From invariants, not from the code.")
print("     Anything you cannot justify excluding, count as reachable.")
print("  2. For unreachable rows, what does the code do? Anything at all. It is")
print("     unconstrained, and an unconstrained row is a landmine rather than a")
print("     neutral fact.")
print("  3. Do reachable rows match the requirement? The only question that")
print("     finds bugs, and the only one you can answer mechanically.")
print()
print("Case A is a bug that production is currently hiding. Case C is a bug")
print("with nothing hiding it, which means it should have been caught and was")
print("not. Both pass any test suite that only exercises reachable behaviour,")
print("and that is not a criticism of testing: a test suite cannot tell you")
print("which rows it failed to reach.")
```

Output (the Case A table, which is the one that matters):

```
      has_more     page_size    has_cursor   code  required  match  reachable
  ------------------------------------------------------------------------
         False             0         False   False      False   ok    NO
         False            25         False   False      False   ok   yes
         False             0          True   False      False   ok    NO
         False            25          True   False      False   ok   yes
          True             0         False   False      False   ok    NO
          True            25         False   False      False   ok   yes
          True             0          True   False       True   BUG    NO
          True            25          True    True       True   ok   yes

rows in the raw table              : 8
rows the invariant makes reachable : 4
mismatches among reachable rows    : 0
mismatches among unreachable rows  : 1
```

Case A is the interesting result and it is the reason to do the exercise with an
integer input rather than a boolean. If `page_size` had been modelled as a bool,
the unreachable-wrong row would have collapsed into the reachable-wrong rows and
you would have reported a bug with no explanation. The row is wrong, it is
unreachable, and the only thing saving you is an assumption about where
`page_size` comes from. Four reachable rows all agree, which is exactly why the
bug survived: production exercised four rows and they were the four that work.

</details>

## Summary

- A proposition is a declarative sentence with a definite truth value.
  "Sort this list" is not one, and "x > 5" is not one until `x` is bound.
- `P ∧ Q`, `P ∨ Q`, and `P ↔ Q` have exact truth conditions, and `∨` is
  inclusive: `P ∨ Q` is true when both are true.
- `P → Q` is false in exactly one case, `P` true and `Q` false. It is therefore
  true in three of four cases, and it is **not** `P ∧ Q`.
- The key identity is `P → Q ≡ ¬P ∨ Q`. Everything else about implication,
  including its negation and its contrapositive, follows from it.
- `¬(P ∧ Q) ≡ ¬P ∨ ¬Q` and `¬(P ∨ Q) ≡ ¬P ∧ ¬Q`. Applying these with the
  connectives swapped is the single most common logic error in code.
- The converse `¬P → ¬Q` is not equivalent to `P → Q`. The contrapositive
  `¬Q → ¬P` is. Lesson 13 needs that difference.
- Negating `P ↔ Q` gives `(P ∧ ¬Q) ∨ (¬P ∧ Q)`, not `P ∨ Q`.
- A tautology is true everywhere and a contradiction is false everywhere.
  Most propositions are contingent, and being contingent is not a criticism.

## Next

[Lesson 11 — Truth Tables, Equivalence, and Normal Forms](../part01_logic_proof/11_truth_tables_and_equivalence.md)
turns what you learned here into a mechanical procedure: enumerate every
assignment, compare columns, and simplify conditions by proof rather than by
intuition. It assumes you can negate a compound statement correctly.
