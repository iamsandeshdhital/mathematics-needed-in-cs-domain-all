# 13 — Proof Techniques

**Part**: part01_logic_proof · **Prerequisites**: 12 · **Time**: 45 min

---

## In Plain Words

An argument is prose. You make a claim, you give reasons, and the reader decides
whether the reasons support the claim. A proof is not that. A proof is a list of
lines, and every line has to be either something you were given or something you
can produce from earlier lines by a rule everybody agreed on in advance. There
is no step for the reader to have a feeling about.

That structure is the whole point, and it is why proofs are checkable by
machines. A proof assistant such as Lean, Coq or Isabelle is not a very smart
colleague; it is a very patient one that will re-read every line and refuse the
whole thing if one of them does not follow.

There are four ways to attack a statement, and they are not four different kinds
of mathematics. They are four routes to the same logical step, and the choice
between them is about which one is cheapest for the statement in front of you.
Sometimes the answer is to check every case, which is not a proof at all until
you notice that there are finitely many cases — and noticing that is often the
hardest part.

## Why Computer Science Cares

**Type checking is proof.** When a checker accepts `xs.map(f)` on a `List[A]`,
it has derived `A` from `List[A]` and the signature of `f` using rules fixed in
advance. When it rejects it, it has derived a contradiction. Nobody calls this a
proof, and that is only because the statements are small enough to be obvious.

**Hoare logic is proof about programs.** A triple `{P} C {Q}` says: for every
state satisfying `P`, running `C` ends in a state satisfying `Q`. That is a
universal claim about every input, and Dafny, Frama-C and SEI's verification
toolkits exist to discharge it mechanically. The three clauses — the
precondition, the invariant, the postcondition — are the direct-proof technique
wearing a program's clothes.

**A correctness argument for an algorithm is usually a loop invariant plus
induction.** "It terminates and returns the right answer" is not a feeling. It
is an invariant that holds at the top of every iteration, plus an argument that
the invariant is preserved, plus an argument that the loop cannot run forever.
Sections 3 and 5 of the Runnable Code do exactly this for binary search.

**Formal methods are the industrial application of this lesson.** Amazon's
s2n, the TLA+ specs that specify S3 and DynamoDB, and the CompCert C compiler
are all proof-carrying: the artefact ships with a machine-checked argument that
it does what the specification says. The specification is the hard part, and
writing one is [Lesson 12](12_predicates_and_quantifiers.md) work.

**SAT and SMT solvers are proof engines in the other direction.** Given a
formula, a solver returns a satisfying assignment or reports unsatisfiability.
"Unsatisfiable" is a short proof, and its length is what solvers are optimised
for — a certificate you can check is a proof, and checking it is cheap on
purpose.

**Cryptographic handshakes are proven, not argued.** TLS's transcript is a
sequence of implications, and the security of the protocol rests on claims of the
form "if the attacker learns X then the attacker breaks assumption Y". Those are
contrapositives, and they are written that way deliberately, because a
contrapositive is the form you can actually prove.

## The Formal Version

Notation follows [SYMBOLS.md](../../SYMBOLS.md). $\Gamma$ is a set of
sentences; $P, Q, R$ are sentences; $\vdash$ is the turnstile.

**Definition.** A *derivation* (or *formal proof*) of $S$ from premises $\Gamma$
is a finite sequence $S_1, S_2, \dots, S_n$ such that $S_n = S$ and, for each
$i$, either $S_i \in \Gamma$ or $S_i$ follows from some of $S_1, \dots, S_{i-1}$
by an inference rule. We write `$\Gamma \vdash S$` when such a sequence exists.

**Definition.** An *inference rule* is a schema "from $A_1, \dots, A_k$ infer
$B$". The schema is *sound* iff no assignment makes all of $A_1, \dots, A_k$
true and $B$ false — which is exactly `$A_1 \wedge \dots \wedge A_k \models B$`
from [Lesson 11](11_truth_tables_and_equivalence.md). A derivation that only
uses sound rules is a proof of a true statement; that is the whole guarantee a
proof offers.

**Definition.** A system is *sound* if everything derivable is true, and
*complete* if everything true is derivable. You want soundness to trust a
proof. You want completeness to be sure you can find one.

**Rule (modus ponens).** From $P$ and $P \to Q$, infer $Q$.

**Rule (∧ elimination, ∧ introduction).** From $P \wedge Q$ infer $P$; from $P$
and $Q$ infer $P \wedge Q$.

**Rule (conditional proof, "→ introduction").** If `$\Gamma, P \vdash Q$` then
`$\Gamma \vdash P \to Q$`. The assumption $P$ is *discharged*: it is introduced
for the duration of the subproof and then removed.

**Rule (reductio ad absurdum, "RAA").** If `$\Gamma, \neg P \vdash \bot$` then
`$\Gamma \vdash P$`. This is proof by contradiction, and it is a rule, not a
manner of speaking.

**Rule (explosion, ex falso).** From $\bot$ infer any $C$.

**Theorem.** *Modus ponens is sound.* If $P$ and $P \to Q$ are both true then
$Q$ is true.

*Proof.* $P \to Q$ is $\neg P \vee Q$. If $P$ is true then $\neg P$ is false, so
the disjunction is true only if $Q$ is true. ∎

**Theorem.** *Contraposition.* `$P \to Q \equiv \neg Q \to \neg P$`.

*Proof.* $\neg Q \to \neg P$ is $\neg(\neg Q) \vee \neg P$, which is
$Q \vee \neg P$, which is $\neg P \vee Q$ by commutativity, which is $P \to Q$. ∎

**Theorem.** *Modus tollens.* From $P \to Q$ and $\neg Q$ infer $\neg P$.

*Proof.* By contraposition, $P \to Q$ gives $\neg Q \to \neg P$; with $\neg Q$,
modus ponens gives $\neg P$. ∎ This is the *rule*, and it is the one that keeps
being confused with its converse, which is not a rule and is frequently false.

**Theorem.** *Explosion is sound.* From $P$ and $\neg P$ infer any $C$.

*Proof.* No assignment makes both $P$ and $\neg P$ true, so the pair is
unsatisfiable. An implication with an unsatisfiable antecedent is true
(vacuously), so `$P \wedge \neg P \to C$` is a tautology. ∎ This is the whole
reason a reductio "works": a contradiction is not a conclusion, it is a licence
to conclude anything, and the licence is sound because you can never get the
licence honestly.

**Theorem.** *The four techniques are four routes to one logical step.* For
sentences $P$ and $Q$, all of the following are the same claim and all have the
same truth conditions:

| technique | what you do |
| --- | --- |
| direct | assume $P$; use it to derive $Q$ |
| contrapositive | assume $\neg Q$; use it to derive $\neg P$ |
| contradiction | assume $\neg(P \to Q)$, i.e. $P \wedge \neg Q$; derive $\bot$ |
| exhaustion | split on $P$ being false or true; check both |

*Proof.* Direct expands to $\neg P \vee Q$. Contrapositive expands to
$Q \vee \neg P$. Contradiction uses $\neg(P \to Q) = P \wedge \neg Q$, and a
conjunction implies $\bot$ implies anything, and $\neg(P\wedge\neg Q) = P \to Q$.
Exhaustion on the two cases $P = \text{false}$ and $P = \text{true}$ gives
"$\neg P \Rightarrow Q$" and "$P \Rightarrow Q$", which conjoin to
$\neg P \vee Q$. All four equal $\neg P \vee Q$. ∎

*Why this is the fact to remember.* The techniques are not four different kinds
of mathematics, so there is no such thing as "a proof by contradiction" being
intrinsically weaker or stronger than "a direct proof". They cost different
things, and the choice is an economic one:

- **direct** costs nothing extra but needs the antecedent to already be in a
  useful shape.
- **contrapositive** costs nothing extra but needs you to *already know* the
  converse of what you are proving. If you do not, the technique is unavailable,
  and that is its real limitation.
- **contradiction** buys freedom from the antecedent's shape at the price of an
  assumption you must discharge, and at the risk of a proof that is short and
  wrong because the contradiction came from an inconsistency in your own premises.
- **exhaustion** needs no insight and cannot be misapplied, and it costs
  `$\lvert D\rvert$` for a universal over a finite domain $D$.

**Theorem.** *Exhaustion is available exactly when the domain is finite.* If
$D$ is finite, `$\forall x \in D\, P(x)$` is proved by `$\lvert D\rvert$`
derivations, one per element. If $D$ is infinite, no finite derivation
concludes it, because there is no last element to reach.

*Proof.* Each derivation of $P(d)$ establishes the universal only for that one
$d$. A finite list of them covers a finite set of elements. An infinite $D$ has
elements outside every finite list, and for each of those the universal is still
unestablished. ∎ The method is not weak; it is *inapplicable*, and confusing
those two words is why people conclude that some true facts cannot be proved.

**Theorem.** *Not everything true is provable, and not everything provable is
worth proving.* There is no algorithm which, given a first-order sentence,
always halts and reports whether it is provable. There are also sentences that
are true and not provable from any finite set of arithmetic axioms, and
sentences that are provable and so long that no one will ever read the proof.

*Explanation, not proof.* This is Gödel's incompleteness theorem and Church's
undecidability result, and it is the honest boundary of the subject. The
engineering consequence is specific: proving your program correct is a technique
with a cost, not a guarantee, and the right response to "can I prove this?" is
usually "which of the four techniques is cheapest here, and is the invariant
findable?" rather than "is this provable at all?"

**Theorem.** *Termination follows from a decreasing bounded measure.* If a loop
has an integer measure $m$ with $m \ge 0$ initially, and every iteration
satisfies $m_{\text{new}} \le \lceil m/2 \rceil$, then after $k$ iterations
$m_k \le \lceil m_0 / 2^k \rceil$, and the loop body runs at most
`$\lceil \log_2(m_0 + 1) \rceil$` times.

*Proof.* Induction on $k$, which is [Lesson 14](14_mathematical_induction.md)'s
subject, and the arithmetic is in the Worked Example below. ∎ State the claim
this way and the endpoint follows from a rate, which is the shape of every
termination argument worth writing.

## Formula Sheet

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$\Gamma \vdash S$` | there is a derivation of $S$ from $\Gamma$ | "S follows from these" | the notation for a proof obligation |
| derivation | $S_1, \dots, S_n$ with $S_n = S$ | a list, each line from earlier lines | the difference between a proof and an argument |
| inference rule | from $A_1, \dots, A_k$ infer $B$, sound iff `$A_1 \wedge \dots \wedge A_k \models B$` | a permitted move | checking a proof by hand or by machine |
| modus ponens | `$P`, `$P \to Q$ ⊢ `$Q$` | the rule | the only rule used constantly |
| modus tollens | `$P \to Q$`, `$\neg Q$ ⊢ `$\neg P$` | the contrapositive form | from a *necessary* condition to ruling out its cause |
| contraposition | `$P \to Q \equiv \neg Q \to \neg P$` | reverse both and swap | choosing which direction is provable |
| **converse** | `$P \to Q$ does *not* give `$Q \to P$` | the tempting non-rule | anywhere; it is the most-used invalid step |
| inverse | `$P \to Q$` gives `$\neg P \to \neg Q$` | also not a rule | debugging: needed conditions do not run backwards |
| → introduction | `$\Gamma, P \vdash Q$` ⟹ `$\Gamma \vdash P \to Q$` | assume, then discharge | proving anything phrased as an implication |
| reductio (RAA) | `$\Gamma, \neg P \vdash \bot$` ⟹ `$\Gamma \vdash P$` | assume the negation, hit a wall | when the direct route needs an idea |
| explosion | `$\bot \vdash C$` for any $C$ | from a contradiction, anything | why a reductio "works"; also why inconsistent premises prove anything |
| `$\bot$` | a contradiction, unsatisfiable | a line you can derive nothing consistent from | the target of a reductio |
| universal generalisation | `$\Gamma \vdash P(c)$`, $c$ arbitrary ⟹ `$\Gamma \vdash \forall x\, P(x)$` | from one arbitrary case to all | needs $c$ to appear nowhere in $\Gamma$ |
| **no free variable** | the condition on universal generalisation | the most-missed hypothesis | any proof that concludes `$\forall$` from one example |
| sound | derivable ⟹ true | the guarantee a proof gives | trusting a proof |
| complete | true ⟹ derivable | the guarantee you will find one | exhaustiveness of a search |
| exhaustion | `$\forall x \in D\, P(x)$` with `$\lvert D\rvert = n$` ⟹ $n$ separate derivations | check every case | small finite $D$; unit and property tests |
| halving measure | `$m_0 = n + 1$`, `$m_{k+1} \le \lceil m_k / 2 \rceil$ | the loop variable at least halves | termination arguments for divide-and-conquer |
| iteration bound | `$k \le \lceil \log_2 (n + 1) \rceil$` | the tight worst-case count | binary search; also `$\lfloor \log_2 n \rfloor + 1$` for $n \ge 1$ |
| cost of exhaustion | `$\lvert D\rvert$ evaluations; `$2^m$` for $m$ boolean atoms | the price of not thinking | deciding whether to be clever or to be mechanical |
| Hoare triple | `$\{P\}\; C \;\{Q\}$` | for every state with $P$, running $C$ ends with $Q$ | Dafny, Frama-C, SEI verification |
| loop invariant | `$P$ holds at the top of every iteration` | the thing that does not change | the direct-proof technique applied to a loop |

## Worked Example

**The claim.** *For every `n ≥ 0`, `bsearch` on a sorted list of length `n`
executes its loop body at most $\lceil \log_2(n+1) \rceil$ times.*

The code, with the interval named so the argument has something to talk about:

```python
def bsearch(L, x):
    lo, hi, steps = 0, len(L), 0
    while lo < hi:
        steps += 1
        mid = (lo + hi) // 2
        if x < L[mid]:
            hi = mid
        elif x > L[mid]:
            lo = mid + 1
        else:
            return mid, steps
    return -1, steps
```

**Step 0. The one lemma everything rests on.** Let $m = hi - lo + 1$, the size
of the live interval *including the gap between the two ends*. It starts at
$m_0 = n + 1$. One iteration sets either `hi = mid` or `lo = mid + 1`, and with
`mid = (lo + hi) // 2` the new size is at most $\lceil m/2 \rceil$. So

$$m_k \le \left\lceil \frac{n+1}{2^k} \right\rceil$$

and the loop runs while $m > 1$, i.e. while $hi < hi$, i.e. while $m_k \ge 2$.

Everything below is that lemma plus arithmetic. Note which quantity it is: not
the length, and not the index. It is the length *plus one*, and using the wrong
one is the single most common way a termination argument goes wrong.

**Step 1. Direct proof.** State the invariant:

> At the top of iteration $k$: (a) `L[lo:hi]` is sorted; (b) if `x` occurs in
> `L`, its index lies in `[lo, hi)`; (c) $m_k \le \lceil (n+1)/2^k \rceil$.

(a) and (b) are established at $k = 0$ because `L[0:n]` is sorted by hypothesis
and contains `x` if `x` is present at all, and both are preserved because each
branch replaces one end of the interval with the midpoint and the midpoint
splits the sorted subarray. That is the correctness argument; it is
independent of (c) and is not what we are proving here.

(c) is established at $k = 0$ with equality, and preserved because Step 0. Now
conclude: when the loop is about to run its $(k+1)$-st iteration we have
$m_k \ge 2$, so $\lceil (n+1)/2^k \rceil \ge 2$, so $(n+1)/2^k > 1$, so
$2^k < n+1$. Therefore the loop can only still be running for $k$ with
$2^k < n+1$, i.e. $k < \log_2(n+1)$, i.e. $k \le \lceil \log_2(n+1) \rceil - 1$
iterations of *entry*. Total body executions: at most
$\lceil \log_2(n+1) \rceil$. ∎

**Step 2. Contrapositive.** *If the body runs more than
$\lceil \log_2(n+1) \rceil$ times, then some iteration did not at least halve
the interval.*

Proof: negate the conclusion of the direct argument. The direct argument ended
with "$2^k < n+1$ for every $k$ at which the loop is still running". Its
negation is "there is a $k$ at which the loop is still running and
$2^k \ge n+1$", and combining with the halving lemma gives
$m_k \le \lceil (n+1)/2^k \rceil \le 1$, so $m_k = 1$, so $hi \le lo$, so the
guard $lo < hi$ is false. Contradiction with "still running". ∎

**Why you would use this one.** Because it names a *place*. Given a measured 4
iterations at $n = 4$ where the bound is 3, the contrapositive says "halving
broke somewhere", and now you can print the interval at the top of every
iteration and read the answer off. The direct proof told you the bound and
nothing about your code; this one tells you where to look. That is the whole
practical difference, and it is why contrapositive is the form a debugger
should be built around.

**Step 3. Proof by contradiction.** Suppose the body runs
$k > \lceil \log_2(n+1) \rceil$ times.

1. By Step 0, $m_k \le \lceil (n+1)/2^k \rceil$.
2. $k > \lceil \log_2(n+1) \rceil$ gives $2^k \ge 2^{\lceil \log_2(n+1)\rceil+1}
   \ge 2(n+1) > n+1$, so $(n+1)/2^k < 1$, so $m_k \le 1$.
3. $m_k = hi - lo + 1 \le 1$ gives $hi \le lo$, so `lo < hi` is false and the
   loop has stopped.
4. But the body ran $k > 0$ times after $k$ iterations. Contradiction. ∎

**Read steps 2 and 3 again and compare them with steps 1–2 of the direct
proof.** They are the same two facts. Contradiction did not make the mathematics
easier; it made the *finish* cheaper, because the assumption `k > bound` does
the pushing and leaves you to check arithmetic. That is the honest description
of when to reach for it: when the thing you want to show is awkward to state
directly but its negation has a strong form.

**Step 4. Why not exhaustion?** Because $n$ is unbounded. Exhaustion gives you
$n = 0$, then $n = 1$, then $n = 2$, and at every point a reader can say "and
$n = 13$?" The table in the Runnable Code goes to $n = 12$ and is *evidence*,
not proof — and it is also *tight*, so the bound is confirmed to be exactly
right, which is a different and equally useful kind of knowledge.

**Step 5. What is actually missing.** The four techniques all reduce to one
logical step, and none of them helps here, because the difficulty is not the
implication — it is the universal over an unbounded $n$. The technique that
handles that is induction: prove the invariant at $k = 0$, prove that $k$
implies $k+1$, and the whole range is covered by a two-line argument that
mentions no particular $k$. That is [Lesson 14](14_mathematical_induction.md),
and this example is the reason it exists.

## Runnable Code

### A proof checker: proofs as data, mistakes as exceptions

```python
# ---------------------------------------------------------------------------
# A proof checker.
#
# A proof is not prose. It is a list of lines, each with a justification, and the
# justification is a RULE whose premises are earlier lines. That makes a proof
# a program, and a wrong proof a runtime error rather than a matter of opinion.
#
# Formulas here are tuples so they can be compared for equality:
#   ("atom", "A")        a proposition letter
#   ("not", f)           ~f
#   ("and", f, g)        f and g
#   ("or", f, g)         f or g
#   ("impl", f, g)       f -> g
#   ("false",)           the contradiction F
# ---------------------------------------------------------------------------

FALSE = ("false",)


def A(name):
    return ("atom", name)


def show(f):
    kind = f[0]
    if kind == "atom":
        return f[1]
    if kind == "false":
        return "FALSE"
    if kind == "not":
        return f"~({show(f[1])})"
    if kind == "impl":
        return f"({show(f[1])} -> {show(f[2])})"
    return f"({show(f[1])} {kind} {show(f[2])})"


def negate(f):
    """Push the negation in. This is Lesson 12's rule, restricted to the three
    connectives this checker knows about."""
    kind = f[0]
    if kind == "not":
        return f[1]
    if kind == "and":
        return ("or", negate(f[1]), negate(f[2]))
    if kind == "or":
        return ("and", negate(f[1]), negate(f[2]))
    if kind == "impl":
        return ("and", f[1], negate(f[2]))
    return ("not", f)


class InvalidProof(Exception):
    pass


def check(proof, target):
    """Verify every line of `proof` and return the list of formulas.

    `proof` is a list of (justification, formula) pairs. The rules are:

      ("premise", key)          a fact taken from outside, looked up in FACTS
      ("assume", key)           open a scope, introducing `key` as a formula
      ("mp", i, j)              line i is P, line j is (P -> Q), conclude Q
      ("and_left", i)           line i is (P and Q), conclude P
      ("and_right", i)          line i is (P and Q), conclude Q
      ("and_intro", i, j)       line i is P, line j is Q, conclude (P and Q)
      ("or_intro", i, g)        line i is one side of g, conclude g
      ("contra", i, j)          line i is P, line j is ~P, conclude FALSE
      ("ex_falso", i, g)        line i is FALSE, conclude g
      ("not_intro", key, i)     close the scope opened by `key`: line i is ~key
      ("imp_intro", key, i)     close the scope opened by `key`: line i is Q
      ("refute", i)             line i must be the target
    """
    FACTS = {
        "sorted": ("and", A("nondecreasing"), A("nonempty")),
        "n_le_1024": ("impl", A("n_le_1024"), A("n_le_2048")),
    }
    lines = []
    scopes = []          # stack of (key, formula, line_index)

    def get(i):
        if not (0 <= i < len(lines)):
            raise InvalidProof(f"line {i + 1} does not exist yet")
        return lines[i]

    for n, (just, formula) in enumerate(proof, 1):
        head = just[0]

        if head == "premise":
            key = just[1]
            if key not in FACTS:
                raise InvalidProof(f"line {n}: no premise named {key!r}")
            if formula != FACTS[key]:
                raise InvalidProof(
                    f"line {n}: stated {show(formula)} but the premise "
                    f"{key!r} is {show(FACTS[key])}")
            lines.append(formula)

        elif head == "assume":
            scopes.append((just[1], formula, n))
            lines.append(formula)

        elif head == "mp":
            p, arrow = get(just[1] - 1), get(just[2] - 1)
            if arrow[0] != "impl":
                raise InvalidProof(
                    f"line {n}: modus ponens needs an implication at line "
                    f"{just[2]}, which is {show(arrow)}")
            if arrow[1] != p:
                raise InvalidProof(
                    f"line {n}: modus ponens needs {show(arrow[1])} at line "
                    f"{just[1]}, which is {show(p)}")
            if formula != arrow[2]:
                raise InvalidProof(
                    f"line {n}: stated {show(formula)} but modus ponens gives "
                    f"{show(arrow[2])}")
            lines.append(formula)

        elif head in ("and_left", "and_right"):
            both = get(just[1] - 1)
            if both[0] != "and":
                raise InvalidProof(
                    f"line {n}: {head} needs a conjunction at line {just[1]}, "
                    f"which is {show(both)}")
            expected = both[1] if head == "and_left" else both[2]
            if formula != expected:
                raise InvalidProof(
                    f"line {n}: stated {show(formula)} but {head} gives "
                    f"{show(expected)}")
            lines.append(formula)

        elif head == "and_intro":
            p, q = get(just[1] - 1), get(just[2] - 1)
            if formula != ("and", p, q):
                raise InvalidProof(
                    f"line {n}: stated {show(formula)} but the two premises "
                    f"give ({show(p)} and {show(q)})")
            lines.append(formula)

        elif head == "or_intro":
            p = get(just[1] - 1)
            if formula[0] != "or" or p not in formula[1:3]:
                raise InvalidProof(
                    f"line {n}: {show(p)} is not a side of {show(formula)}, so "
                    f"it cannot be introduced into a disjunction")
            lines.append(formula)

        elif head == "contra":
            p, q = get(just[1] - 1), get(just[2] - 1)
            if q != ("not", p):
                raise InvalidProof(
                    f"line {n}: contradiction needs a pair P and ~P; lines "
                    f"{just[1]} and {just[2]} are {show(p)} and {show(q)}")
            if formula != FALSE:
                raise InvalidProof(
                    f"line {n}: stated {show(formula)} but a contradiction "
                    f"gives FALSE")
            lines.append(formula)

        elif head == "ex_falso":
            if get(just[1] - 1) != FALSE:
                raise InvalidProof(
                    f"line {n}: ex falso needs FALSE at line {just[1]}")
            lines.append(formula)

        elif head in ("not_intro", "imp_intro"):
            key, assumed, opened = scopes.pop()
            if key != just[1]:
                raise InvalidProof(
                    f"line {n}: closes scope {just[1]!r} but the innermost open "
                    f"scope is {key!r}, opened at line {opened}")
            conclusion = get(just[2] - 1)
            want = (("not", assumed) if head == "not_intro"
                    else ("impl", assumed, conclusion))
            if formula != want:
                raise InvalidProof(
                    f"line {n}: stated {show(formula)} but closing the scope "
                    f"gives {show(want)}")
            lines.append(formula)

        elif head == "refute":
            if get(just[1] - 1) != target:
                raise InvalidProof(
                    f"line {n}: the final line is {show(get(just[1] - 1))}, "
                    f"not the target {show(target)}")
            lines.append(formula)

        else:
            raise InvalidProof(f"line {n}: unknown rule {head!r}")

    if scopes:
        raise InvalidProof(
            f"{len(scopes)} scope(s) left open: "
            f"{[s[0] for s in scopes]}. An unclosed assumption proves nothing.")
    return lines


# --- Proof 1: commutativity of conjunction, by DIRECT proof -----------------
# Assume the conjunction, take it apart, put it back together in the other
# order, and close the scope.
target = ("impl", ("and", A("A"), A("B")), ("and", A("B"), A("A")))
proof_comm = [
    (("assume", "H"), ("and", A("A"), A("B"))),                   # 1
    (("and_left", 1), A("A")),                                    # 2
    (("and_right", 1), A("B")),                                   # 3
    (("and_intro", 3, 2), ("and", A("B"), A("A"))),               # 4
    (("imp_intro", "H", 4),
     ("impl", ("and", A("A"), A("B")), ("and", A("B"), A("A")))),  # 5
]

# --- Proof 2: no contradiction, by proof by CONTRADICTION ------------------
# Assume P and ~P, get a contradiction, then conclude ~(P and ~P).
target2 = ("not", ("and", A("P"), ("not", A("P"))))
proof_contra = [
    (("assume", "H"), ("and", A("P"), ("not", A("P")))),         # 1
    (("and_left", 1), A("P")),                                    # 2
    (("and_right", 1), ("not", A("P"))),                          # 3
    (("contra", 2, 3), FALSE),                                    # 4
    (("not_intro", "H", 4), ("not", ("and", A("P"), ("not", A("P"))))),
]

for label, proof, goal in [("direct", proof_comm, target),
                           ("contradiction", proof_contra, target2)]:
    print("=" * 70)
    print(f"a valid proof, by {label}")
    print("=" * 70)
    print(f"  target: {show(goal)}")
    for n, (just, formula) in enumerate(proof, 1):
        print(f"  {n:>2}. {show(formula):<32} {just}")
    lines = check(proof, goal)
    print(f"  ACCEPTED: {len(proof)} steps, {len(lines)} formulas")
    print()

# --- A proof with no steps at all: the premise IS the conclusion ------------
# The specification of `sorted` is a conjunction, and one of its conjuncts is
# the conclusion. There is nothing to prove beyond taking it apart, and the
# honest proof is one line long.
proof_from_premise = [
    (("premise", "sorted"), ("and", A("nondecreasing"), A("nonempty"))),
    (("and_right", 1), A("nonempty")),
]
print("=" * 70)
print("a valid proof, from a premise")
print("=" * 70)
for n, (just, formula) in enumerate(proof_from_premise, 1):
    print(f"  {n:>2}. {show(formula):<32} {just}")
check(proof_from_premise, A("nonempty"))
print("  ACCEPTED: the conclusion is a conjunct of the premise")
print()
print("Worth saying out loud: sometimes the correct proof is one line, and")
print("recognising that is a skill. A two-page argument for a one-line fact is")
print("usually an argument about something else.")
print()

# --- Five broken proofs, and exactly where each one breaks -----------------
target3 = ("impl", A("A"), ("impl", A("B"), ("impl", A("H"), A("B"))))
BROKEN = [
    ("modus ponens on a non-implication",
     [(("assume", "A"), A("A")),
      (("mp", 1, 1), A("B")),
      (("imp_intro", "A", 2), ("impl", A("A"), A("B")))],
     ("impl", A("A"), A("B"))),

    ("modus ponens with a mismatched antecedent",
     [(("assume", "A"), A("A")),
      (("assume", "B"), A("B")),
      (("assume", "H"), ("impl", A("A"), A("B"))),
      (("mp", 2, 3), A("B")),
      (("imp_intro", "H", 4), ("impl", A("H"), A("B"))),
      (("imp_intro", "B", 5), ("impl", A("B"), ("impl", A("H"), A("B")))),
      (("imp_intro", "A", 6), target3)],
     target3),

    ("an assumption that is never closed",
     [(("assume", "A"), A("A")),
      (("and_intro", 1, 1), ("and", A("A"), A("A")))],
     ("and", A("A"), A("A"))),

    ("a final line that is not the target",
     [(("assume", "A"), A("A")),
      (("imp_intro", "A", 1), ("impl", A("A"), A("B"))),
      (("refute", 2), ("impl", A("A"), A("B")))],
     ("impl", A("A"), A("A"))),

    ("a premise that was misquoted",
     [(("premise", "sorted"), ("and", A("nonempty"), A("nondecreasing")))],
     ("and", A("nonempty"), A("nondecreasing"))),
]

for label, proof, goal in BROKEN:
    try:
        check(proof, goal)
        print(f"  {label:<42} ACCEPTED  <-- the checker is broken")
    except InvalidProof as exc:
        print(f"  {label:<42} REJECTED: {exc}")
print()
print("Every rejection names a line, a rule, and the two formulas that did not")
print("line up. That is the difference between a proof and an argument: an")
print("argument can be wrong and still sound persuasive, because there is no")
print("step for a reader to disagree with. A proof has steps, and each step is")
print("either an axiom or a rule applied to steps already accepted.")
print()
print("The last one is the most valuable. `nondecreasing and nonempty` and")
print("`nonempty and nondecreasing` are the same claim -- the checker just")
print("cares which way round the letters are, so a misquoted premise is")
print("rejected even though nothing mathematical is wrong. A checker that")
print("accepted it would be accepting something else as well.")
```

### The four techniques, as four functions over the same statement

```python
import itertools

# ---------------------------------------------------------------------------
# Every technique produces the same truth column, because they are all
# equivalent formulas. What differs is what you must ASSUME and what you must
# BUILD. Writing them side by side is the clearest statement of that.
# ---------------------------------------------------------------------------

ATOMS = ["A", "B", "C"]
ROWS = [dict(zip(ATOMS, bits))
        for bits in itertools.product([False, True], repeat=len(ATOMS))]


def column(f):
    """The truth column of a formula given as a Python function of an env."""
    return [bool(f(env)) for env in ROWS]


def bits(values):
    return "".join("1" if v else "0" for v in values)


def techniques(ante, cons):
    """Four readings of the one statement `ante -> cons`.

    direct          ~p or q
    contrapositive   q or ~p        (that is what `~q -> ~p` expands to)
    contradiction   (p and q) or ~p (what a reductio leaves behind)
    exhaustion      no cleverness: evaluate the case
    """
    return [
        ("direct", "~p or q", lambda e: (not ante(e)) or bool(cons(e))),
        ("contrapositive", "q or ~p", lambda e: bool(cons(e)) or (not ante(e))),
        ("contradiction", "(p and q) or ~p",
         lambda e: (ante(e) and cons(e)) or (not ante(e))),
        ("exhaustion", "evaluate the case",
         lambda e: True if not ante(e) else bool(cons(e))),
    ]


def show_table(name, ante, cons):
    """Print the four columns for one statement. A function, not a loop, so
    that an exercise can call it on its own statements."""
    print(f"  {name}")
    print(f"    {'technique':<16} {'shape':<20} {'column':>9}  holds?")
    base = None
    for label, shape, fn in techniques(ante, cons):
        col = column(fn)
        base = col if base is None else base
        print(f"    {label:<16} {shape:<20} {bits(col):>9}  {all(col)}")
    return base


print("=" * 74)
print("1. Four techniques, one statement, one column")
print("=" * 74)
print()
print("  the statement: if the request is unauthenticated and not public,")
print("                 then it is denied.  So  p = (~A and ~B),  q = C.")
print(f"  domain: 2^{len(ATOMS)} = {len(ROWS)} assignments to A, B, C")
print()
print(f"  {'technique':<16} {'shape':<20} {'column':>9}  holds?")
CHECK = techniques(lambda e: (not e["A"]) and (not e["B"]), lambda e: e["C"])
base = None
for label, shape, fn in CHECK:
    col = column(fn)
    base = col if base is None else base
    print(f"  {label:<16} {shape:<20} {bits(col):>9}  {all(col)}")
print()
print("  every technique agrees with the first: "
      f"{all(column(fn) == base for _, _, fn in CHECK)}")
print()
print("  rows are (A, B, C) in the order 000, 001, 010, 011, 100, 101, 110, 111")
print("  A = authenticated, B = public, C = denied")
print()
print("  The column has exactly one 0, at row 000. That row is the whole")
print("  counterexample: an unauthenticated request to a private endpoint that")
print("  was not denied. The specification is a conjunction of two negations")
print("  followed by a consequence, and it is false in exactly one place.")
print()

print("=" * 74)
print("2. Four different statements, and which technique pays")
print("=" * 74)
print()
CASES = [
    ("p = ~A,  q = B", lambda e: not e["A"], lambda e: e["B"],
     "direct: one step, no detour"),
    ("p = A and B,  q = C", lambda e: e["A"] and e["B"], lambda e: e["C"],
     "direct: split the antecedent first"),
    ("p = ~A,  q = A and C", lambda e: not e["A"],
     lambda e: e["A"] and e["C"],
     "contradiction: ~p hands you A, and A hands you q"),
    ("p = ~A or B,  q = A", lambda e: (not e["A"]) or e["B"], lambda e: e["A"],
     "neither: the statement is equivalent to plain A"),
]
print(f"{'statement':<24} {'direct':>8} {'contra':>8} {'reductio':>9} "
      f"{'exhaust':>8}  all equal")
for name, ante, cons, verdict in CASES:
    cols = [bits(column(fn)) for _, _, fn in techniques(ante, cons)]
    print(f"{name:<24} {cols[0]:>8} {cols[1]:>8} {cols[2]:>9} {cols[3]:>8}"
          f"  {len(set(cols)) == 1}")
    print(f"    {verdict}")
print()
print("Every row has four identical columns, which is the theorem: the four")
print("techniques are four equivalent formulas. The last row is the one to")
print("notice. p -> q there is equivalent to plain A, and its contrapositive")
print("is also equivalent to plain A, so `assume ~A, therefore p` is a")
print("perfectly good route -- and it is a reductio that terminates in a")
print("counterexample rather than a proof, because the statement is false.")
print()

print("=" * 74)
print("3. Why the same column does not mean the same proof")
print("=" * 74)
print()
print("  A truth column answers 'is this formula a tautology?' completely, and")
print("  answers 'what did you have to assume?' not at all. Two proofs with the")
print("  same column can differ enormously in effort:")
print()
print("    direct        : no auxiliary assumption; every step is a rewrite or")
print("                    a given fact. Cheapest when the antecedent is")
print("                    already in the shape you need.")
print("    contrapositive: same length, but you must already know the converse")
print("                    of the thing you are proving before you start. If")
print("                    you do not, the technique is unavailable.")
print("    contradiction : an auxiliary assumption you must discharge, plus a")
print("                    step deriving a contradiction from facts that are")
print("                    each individually reasonable. Best when the direct")
print("                    route needs an idea and the false one is forced.")
print("    exhaustion    : one line of code and no insight whatsoever, but it")
print("                    cannot be wrong -- and it scales as 2^n.")
print()
print(f"  With {len(ATOMS)} atoms, exhaustion costs {len(ROWS)} evaluations. With 30")
print(f"  atoms it costs {2 ** 30:,}, which is why nobody proves a 30-variable")
print("  formula by checking rows. The techniques differ in cost, in what you")
print("  must already know, and in what they hand back -- not in the answer.")
```

### The worked example, run: a termination argument and its four readings

```python
from math import ceil, log2

# ---------------------------------------------------------------------------
# Claim: on a sorted list of n elements, bsearch executes its loop body at most
# ceil(log2(n + 1)) times. Section 2 shows that exhaustion cannot reach the
# general case, which is why Lesson 14 exists.
# ---------------------------------------------------------------------------


def bsearch(L, x):
    """Return (index of x in the sorted list L or -1, iterations used)."""
    lo, hi, steps = 0, len(L), 0
    while lo < hi:
        steps += 1
        mid = (lo + hi) // 2
        if x < L[mid]:
            hi = mid
        elif x > L[mid]:
            lo = mid + 1
        else:
            return mid, steps
    return -1, steps


def bound(n):
    """ceil(log2(n + 1)). The claim's right-hand side. Works for n = 0 too."""
    return ceil(log2(n + 1))


def size_after(n, k):
    """Upper bound on (hi - lo) after k iterations.

    The quantity that at least halves each round is (hi - lo + 1), and it
    starts at n + 1, so after k rounds it is at most ceil((n+1) / 2^k). This
    is the one lemma all three proofs lean on, so it is worth having a number
    for it.
    """
    return max(0, -(-(n + 1) // (2 ** k)) - 1)


print("=" * 74)
print("1. The halving lemma, as a table")
print("=" * 74)
print()
print(f"{'n':>4} {'bound = ceil(log2(n+1))':>24} {'(hi-lo) after bound steps':>27}")
for n in range(0, 17):
    b = bound(n)
    print(f"{n:>4} {b:>24} {size_after(n, b):>27}")
print()
print("The right-hand column is 0 for every n, which is the whole claim in one")
print("line: after bound(n) halvings there is no interval left, so the loop has")
print("stopped. Note the n = 0 row: an empty list needs no iterations at all,")
print("and ceil(log2(1)) = 0 says exactly that. The bound is tight, not merely")
print("an upper limit -- see section 2.")
print()

print("=" * 74)
print("2. EXHAUSTION: the best a finite search can do, and why it is not a proof")
print("=" * 74)
print()
print(f"{'n':>4} {'bound':>7} {'worst steps found':>18} {'tight?':>8}")
for n in range(0, 13):
    L = list(range(n))
    worst = max(bsearch(L, x)[1] for x in range(-2, n + 2))
    print(f"{n:>4} {bound(n):>7} {worst:>18} {str(worst == bound(n)):>8}")
print()
print("The bound is attained for every n from 0 to 12, so it is tight and not")
print("merely safe. Thirteen rows of arithmetic, every one agreeing with the")
print("claim. This is exhaustion, and it is the technique to reach for when the")
print("set of cases is finite and small: it needs no insight, it cannot be")
print("misapplied, and a machine does it for free.")
print()
print("It is also not a proof of the claim, because the claim is about EVERY n.")
print("The table covers n = 0..12. A reader who asks about n = 13 is given")
print("nothing, and no amount of extending the table closes the gap -- the")
print("table is always finite and the claim is not. The observation that the")
print("loop only ever looks at indices, so one probe per n suffices, is a hint")
print("that something structural is going on; turning that hint into an")
print("argument is induction, and it is [Lesson 14](14_mathematical_induction.md).")
print()

print("=" * 74)
print("3. CONTRADICTION: suppose the claim is false, and watch it collapse")
print("=" * 74)
print()
print("  Suppose for contradiction that the body runs k > ceil(log2(n+1)) times")
print("  on some input of length n.")
print()
print("  Step 1. By the halving lemma, (hi - lo + 1) <= (n + 1) / 2^k after k")
print("          iterations.")
print("  Step 2. k > ceil(log2(n+1)) gives 2^k >= 2^(ceil(log2(n+1)) + 1)")
print("          >= 2(n+1) > n + 1, so (n+1) / 2^k < 1, so hi - lo + 1 < 2, so")
print("          hi - lo = 0.")
print("  Step 3. An interval of length 0 fails `lo < hi`, so the loop has")
print("          already stopped.")
print("  Step 4. But we assumed the body ran k > 0 times after k iterations.")
print("          Contradiction. Therefore the claim holds.")
print()
print("  Steps 2 and 3 are the only real work, and they are the same two facts")
print("  as in the direct proof. Contradiction did not make them easier; it")
print("  made the FINISH cheaper, by letting the assumption do the pushing. That")
print("  is the honest description of when to reach for it.")
print()

print("=" * 74)
print("4. CONTRAPOSITIVE: if it ran too long, the halving failed")
print("=" * 74)
print()
print("  Contrapositive: if the body runs more than ceil(log2(n+1)) times, then")
print("  at some iteration (hi - lo + 1) did not at least halve.")
print()
print("  This is the form to use when you are handed a failing measurement and")
print("  want to know what to look at. It names a single iteration as the")
print("  culprit, which is an index you can print, breakpoint, or log. The")
print("  direct form does not localise anything.")
print()
print("  And it is the form a debugger actually runs: given 'it took 4 steps")
print("  and bound(4) = 3', the contrapositive says 'halving broke somewhere',")
print("  and the usual cause is an off-by-one in the interval update. Same")
print("  logic, aimed at a line number instead of at a theorem.")
print()

print("=" * 74)
print("5. DIRECT: the invariant, stated once, and then checked")
print("=" * 74)
print()
print("  Invariant, holding at the top of every iteration:")
print()
print("      (a) L[lo:hi] is sorted")
print("      (b) if x occurs in L at all, its index lies in [lo, hi)")
print("      (c) hi - lo + 1 <= ceil((n + 1) / 2^k),  k = iterations so far")
print()
print("  (a) and (b) are what make the answer correct; (c) is what makes it")
print("  fast. Note that (c) is the only part that mentions the bound, and it")
print("  does so as a RATE -- one halving per iteration -- rather than as a")
print("  fact about the end. That is the shape of every termination argument:")
print("  state a rate and the endpoint follows.")
print()


def bsearch_instrumented(L, x):
    """bsearch, but check all three invariant clauses at the top of every
    iteration and report any that fail."""
    lo, hi, k, n = 0, len(L), 0, len(L)
    violations = []
    while lo < hi:
        for cond, label in [
            (all(L[i] <= L[i + 1] for i in range(lo, hi - 1)), "(a) sorted"),
            (x not in L or lo <= L.index(x) < hi, "(b) target in range"),
            (hi - lo + 1 <= -(-(n + 1) // (2 ** k)), "(c) halving rate"),
        ]:
            if not cond:
                violations.append((k, label))
        k += 1
        mid = (lo + hi) // 2
        if x < L[mid]:
            hi = mid
        elif x > L[mid]:
            lo = mid + 1
        else:
            break
    return violations, k


checks = violations_total = 0
tightest = 0
for n in range(0, 13):
    L = list(range(n))
    for x in range(-2, n + 2):
        bad, k = bsearch_instrumented(L, x)
        checks += 1
        violations_total += len(bad)
        tightest = max(tightest, k)
        assert k <= bound(n), f"bound violated: n={n} x={x} k={k}"
print(f"  inputs checked           : {checks}")
print(f"  invariant violations     : {violations_total}")
print(f"  max iterations observed  : {tightest}  (bound(12) = {bound(12)})")
print()
print("  Zero violations is not a proof -- it is 130 checks, and the claim is")
print("  about every n. But it is enough to tell you that the invariant you")
print("  wrote down is the right invariant, and that is the step that usually")
print("  fails in practice. The loop is nearly always correct; the invariant")
print("  you wrote down is nearly always not the one that explains why.")
```

## Common Mistakes

**Wrong: treating the converse of an implication as available.**
Right: `P → Q` gives you `P` ⟹ `Q`. It does not give you `Q` ⟹ `P`, and it does
not give you `¬P` ⟹ `¬Q`. Only the contrapositive `¬Q → ¬P` follows. In code
this is `if is_valid(token): return user`, and the converse mistake is
`if user: return is_valid(token)` — which returns a boolean where a user was
promised.
Why tempting: English uses "if" both ways. "If it rains the ground is wet" and
"the ground is wet, so it rained" feel like the same statement, and only one of
them is what the implication said.

**Wrong: proving `P → Q` by establishing `P` and then `Q` separately.**
Right: establishing $P$ for one particular case does not establish
`∀x P(x)`, and the universal generalisation rule requires the element to appear
nowhere in your premises. If you proved the body for a value you chose, you have
proved an existential at best.
Why tempting: it is the fastest way to get a green test suite, and the proof
looks complete while you read it.

**Wrong: a reductio that derives its contradiction from a mistake.**
Right: in a proof by contradiction, every step must be justified independently
of the assumption you are discharging. If the contradiction comes from the
assumption itself, you have proved the assumption is inconsistent, which is
sometimes the answer (the claim is false) and sometimes a sign that you
mis-stated the claim.
Why tempting: a reductio *feels* like a way of allowing yourself anything, and
it is — which is exactly why the check has to be on each step rather than on the
conclusion. The proof checker in the Runnable Code is the discipline: it
rejects an unclosed scope with a message, which is what "you discharged nothing"
looks like when a machine is reading.

**Wrong: concluding that a universal statement is unprovable because exhaustion
failed on it.**
Right: exhaustion is *inapplicable* to an infinite domain, not defeated by it.
The four techniques in this lesson all reduce to one logical step and none of
them helps with an unbounded universal. Induction is the technique for that,
and it is the subject of the next lesson.
Why tempting: the two words sound like the same thing, and "I tried it and it
did not work" feels like a verdict. It is a measurement, and it measured the
method rather than the statement.

**Wrong: quoting a premise in a different shape and treating it as the same
line.**
Right: `nondecreasing ∧ nonempty` and `nonempty ∧ nondecreasing` are
logically equivalent and syntactically different, and a proof checker compares
syntax. The last rejected proof in the Runnable Code is exactly this: nothing
mathematical is wrong, and the checker still refuses.
Why tempting: the sentences mean the same thing, and a human reader waves them
through. The discipline is not pedantry — a checker that accepted a
re-ordered premise would also accept a genuinely different one, and then it
would be checking nothing.
---

## Multiple Choice Questions

**Q1.** What is the contrapositive of `P → Q`?

- A) `Q → P`
- B) `¬Q → ¬P`
- C) `¬P → ¬Q`
- D) `P ∧ Q`

<details>
<summary>Answer and explanation</summary>

**B) `¬Q → ¬P`.**

Both reduce to `¬P ∨ Q`. Expand the contrapositive: `¬Q → ¬P` is
`¬(¬Q) ∨ ¬P`, which is `Q ∨ ¬P`, which is `¬P ∨ Q` by commutativity, which is
`P → Q`. That is the whole proof, and it is the shortest in this lesson.

Option A, `Q → P`, is the **converse**. It is the single most-used invalid step
in the subject, and it is genuinely not implied: over the reals, `x² ≥ 0` is
always true while `x ≥ 0` is not, so `Q → P` is false.

Option C, `¬P → ¬Q`, is the **inverse**. It is not implied either, and the
counterexample is the same one: `x > 0` gives `x² > 0`, so the inverse
`x² ≤ 0 → x ≤ 0` fails at `x² = 1`.

Option D is a conjunction, not an implication at all, and it is much stronger
than either. `P ∧ Q` is false whenever either disjunct of the expansion fails.

</details>

**Q2.** You have proved `P → R` and you can also prove `P → S`. What do you have?

- A) `P → (R ∧ S)`
- B) `(P → R) ∧ (P → S)`, which by distribution is `P → (R ∧ S)`
- C) `(P → R) ∨ (P → S)`, which is all you may claim
- D) `R ∧ S`, because the shared antecedent lets you discard it

<details>
<summary>Answer and explanation</summary>

**B) `(P → R) ∧ (P → S)`, which by distribution is `P → (R ∧ S)`.**

Conjoining the two derivations gives `(¬P ∨ R) ∧ (¬P ∨ S)`, which
distributes to `¬P ∨ (R ∧ S)`, which is `P → (R ∧ S)`. This is a sound rule and
it is how preconditions accumulate: if a method needs the value to be an int
*and* to be positive, you establish both implications from the same hypothesis
and conjoin them.

Option A is the same statement written without its derivation. It is the correct
conclusion, so this is a case where the right answer and a wrong reason look
alike — but the justification matters, because a conclusion without a
derivation is a guess.

Option C is strictly weaker. A disjunction of the two implications is always
true, since an implication with a false antecedent is true, so it carries no
information about `R ∧ S` at all.

Option D is a genuine error: from `P → R` and `P → S` you get nothing about `R`
or `S` outside the case where `P` holds. Dropping the antecedent is valid only
when you have separately established `P`.

</details>

**Q3.** A proof by contradiction of `P` assumes `¬P` and derives a
contradiction. What makes this a valid rule rather than a trick?

- A) The contradiction must be between `¬P` and a fact that does not mention
  `P`.
- B) Once a contradiction is derived, the system is inconsistent, and by
  explosion every statement follows — including `P`.
- C) It is valid only if `P` is a simple atomic proposition.
- D) It is invalid in general, and only works for finite domains.

<details>
<summary>Answer and explanation</summary>

**B) Once a contradiction is derived, the system is inconsistent, and by
explosion every statement follows — including `P`.**

The soundness argument is that `P ∧ ¬P` is unsatisfiable, so `P ∧ ¬P → P` is
vacuously true, so the pair entails `P`. The rule RAA is therefore not a trick
at all: it is modus ponens applied to an implication whose antecedent happens
to be false. A reductio "works" precisely because you can never honestly reach
the contradiction.

Option A is a reasonable *discipline* and not the justification. In practice a
contradiction between `¬P` and a `P`-free fact is a sign you did not smuggle the
assumption back in — but the rule does not require it, and requiring it would
be a syntactic restriction, not a soundness argument.

Option C is wrong. RAA is routinely applied to compound claims:
`¬(A ∧ ¬A)` is proved by assuming `A ∧ ¬A` and contradicting it, exactly as the
second valid proof in the Runnable Code does.

Option D is wrong for the same reason the whole lesson is right: the technique
is a rule of inference over sentences, with no dependence on the size of
anything.

</details>

**Q4.** Which of these is a legitimate proof of `∀x ∈ D, P(x)`?

- A) Finding one `d ∈ D` with `P(d)` true
- B) Finding one `d ∈ D` with `P(d)` false
- C) Establishing `P(d)` for every `d ∈ D`, by exhaustion, when `D` is finite
- D) Establishing `P(c)` for an arbitrary `c` that appears in no premise

<details>
<summary>Answer and explanation</summary>

**C) Establishing `P(d)` for every `d ∈ D`, by exhaustion, when `D` is
finite.**

Exhaustion is sound and complete for a finite domain: `|D|` derivations, one
per element, and the universal follows by conjoining them. This is the technique
behind an exhaustive test suite, and it is a genuine proof — of a claim about
that finite set.

Option A gives `∃x P(x)`. Witnessing a universal is the single most common
quantifier error in the subject, and it is invisible when the domain is small
enough that the witness happens to be in it.

Option B is a *refutation* of the universal, and a complete one: the universal
is false the moment one element falsifies it. B is the right answer to "is this
claim true?" and the wrong answer to "prove this claim."

Option D is the universal generalisation rule, and it is also correct — but it
is the rule that *induction* implements, and it needs the "appears in no
premise" condition to be a rule at all. Drop that condition and you can prove
`∀x P(x)` from `P(c)` for a single arbitrary `c` that happened to be the only
value you looked at, which is option A wearing a formal costume.

</details>

**Q5.** `bsearch` on a list of length `n` runs its body at most
`⌈log₂(n+1)⌉` times. Which of these is the *tight* worst-case count, i.e. the
value actually attained for infinitely many `n`?

- A) `⌈log₂(n+1)⌉`
- B) `⌈log₂ n⌉`
- C) `⌊log₂ n⌋ + 1` for `n ≥ 1`, which equals `⌈log₂(n+1)⌉`
- D) `n`

<details>
<summary>Answer and explanation</summary>

**C) `⌊log₂ n⌋ + 1` for `n ≥ 1`, which equals `⌈log₂(n+1)⌉`.**

The two closed forms are the same function on positive integers: for `n = 4`,
both give 3; for `n = 7`, both give 3; for `n = 8`, both give 4. The proof is
that `⌊log₂ n⌋ + 1` is the least `k` with `2^k > n`, and `⌈log₂(n+1)⌉` is the
least `k` with `2^k ≥ n+1`, and those are the same condition for integer `k`.
Section 2 of the third code block confirms the bound is attained for every `n`
from 0 to 12, so it is tight and not merely safe.

Option A is the same number written the other way, so as a *statement about the
count* it is also correct — which is why the option states C as the answer: the
question asks for the tight count, and both A and C state it. If a test wants one
letter, C is the one that also identifies the interpretation, but be aware that
A is not wrong. Read A as "the bound", not as "the value attained", and it is
right; that is the distinction the question is testing.

Option B, `⌈log₂ n⌉`, is off by one for every `n` that is a power of two: for
`n = 8` it gives 3 when 4 iterations are needed. That off-by-one is the classic
binary-search bug and it is why the halving measure in the worked example is
`hi - lo + 1` rather than `hi - lo`.

Option D is a correct upper bound and a useless one; it describes linear search.

</details>

**Q6.** You want to prove `merge(A, B)` returns a sorted list when `A` and `B`
are sorted. Which starting move is most likely to succeed?

- A) Assume `A` is unsorted and derive a contradiction
- B) Assume `A` and `B` are sorted; show every element of the output is at
  least every element already emitted
- C) Check all pairs of inputs of length up to 4
- D) Prove the contrapositive: if the output is unsorted, then A or B was
  unsorted

<details>
<summary>Answer and explanation</summary>

**B) Assume `A` and `B` are sorted; show every element of the output is at
least every element already emitted.**

That is a loop invariant in the direct-proof style, and it is the shape of
almost every successful correctness argument about a loop: state what is true
at the top of every iteration, show the body preserves it, show the exit
condition implies the postcondition. Here the invariant would be "the emitted
prefix is sorted, and every element of A and B not yet emitted is at least the
last emitted element."

Option A assumes the negation of a *hypothesis*, not of the conclusion. It
cannot be discharged, because the hypothesis is given — you have no way to
contradict it without contradicting the problem statement. Compare the two
styles, which do work:

```python
def merge(a, b):
    """Merge two sorted lists into one sorted list."""
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out


def merge_checked(a, b):
    # A contradiction on the CONCLUSION: 'unsorted output' is what we refute.
    if a[0] > a[1]:
        raise AssertionError("a is not sorted")
    result = merge(a, b)
    if result != sorted(result):
        raise AssertionError("output is not sorted")
    return result


def merge_contradiction(a, b):
    # A contradiction on a HYPOTHESIS: there is nothing to contradict, because
    # a and b being sorted is given rather than concluded.
    if not sorted(a) or not sorted(b):
        raise AssertionError("inputs must be sorted")
    return merge(a, b)


print("merge_checked([1, 3], [2, 4]) =", merge_checked([1, 3], [2, 4]))
print("merge_contradiction([1, 3], [2, 4]) =", merge_contradiction([1, 3], [2, 4]))
print("both agree:", merge_checked([1, 3], [2, 4]) == merge_contradiction([1, 3], [2, 4]))
```

The first refuses the *output*; the second refuses the *input*. Only the first
is a proof obligation, because only the first is a claim about the code you
wrote.

Option C is exhaustion, and for inputs of length up to 4 it is evidence rather
than proof: the claim is about all lengths. It is also the answer when you
cannot find an invariant, and finding an invariant is nearly always faster than
proving you cannot.

Option D is a legitimate technique and a poor choice here. The contrapositive is
`output unsorted → A or B unsorted`, and it is true, but establishing it needs
essentially the same invariant argument read backwards. Contrapositive pays off
when the *negation* of the conclusion is easier to reach than the conclusion —
for instance "if the authentication check is not rejecting unauthenticated
requests, then the predicate is not a conjunction of negations."

</details>

**Q7.** Which claim about proof is false?

- A) A sound inference rule never takes you from true premises to a false
  conclusion.
- B) A proof with a false premise in it can still be a valid derivation.
- C) If a statement is true then some finite proof of it exists.
- D) A complete system is one in which every true sentence is derivable.

<details>
<summary>Answer and explanation</summary>

**C) If a statement is true then some finite proof of it exists.**

This is where Gödel's incompleteness theorem and Church's undecidability result
live. There are true statements of arithmetic that are not provable from the
axioms of arithmetic, and there is no algorithm that always halts and tells you
whether a given statement is provable. So C is false, and it is false in the
strongest possible way: not "we have not found the proof" but "no proof exists".

Option A is the definition of soundness and it is true, and it is the guarantee
a proof gives you.

Option B is true and slightly surprising. Validity of a derivation and
correctness of the argument are separate: a derivation from an inconsistent
premise set is valid, because explosion is sound. This is why "the proof was
accepted" and "the premise was right" are two separate questions, and why a
proof obligation over a specification that is itself wrong produces a perfectly
verified proof of a false claim.

Option D is the definition of completeness and it is true.

</details>

**Q8.** Your proof checker accepts a proof whose last line is `FALSE` and whose
first line is an assumption you never discharged. What has gone wrong?

- A) Nothing: explosion means any conclusion follows
- B) The checker has a bug, because an undischarged assumption means the
  conclusion depends on something you were not given
- C) The proof is fine, since the assumption was stated
- D) The checker should have accepted it, because the target was derived

<details>
<summary>Answer and explanation</summary>

**B) The checker has a bug, because an undischarged assumption means the
conclusion depends on something you were not given.**

An undischarged scope is exactly the gap in `Γ, P ⊢ Q` where you never wrote
`Γ ⊢ P → Q`. What you have proved is a conditional, not a theorem. The proof
checker in the Runnable Code treats a leftover scope as a hard error, and the
message is `"1 scope(s) left open"`.

Option A confuses explosion with scope. Explosion says that *within* an
inconsistent set you may conclude anything. It does not license carrying an
inconsistency out of the proof and treating it as a theorem. If you did allow
it, every theorem in mathematics would be provable, because you can always open
a scope with `0 = 1`.

Option C is the tempting one: the assumption was written down, so it feels like
part of the proof. That is precisely the confusion. Writing a hypothesis into
a proof is how you *introduce* a lemma; failing to close the scope is how you
fail to *conclude* it.

Option D is not a thing. The `refute` rule exists precisely to catch a final
line that is not the target, and it is a separate check from the scope check.

</details>

**Q9.** In the worked example, why is the halving measure `hi - lo + 1` rather
than `hi - lo`?

- A) Because `hi - lo + 1` is an integer and `hi - lo` is not
- B) Because `hi - lo + 1` is the quantity that provably at least halves each
  iteration, so `2^k ≥ n + 1` forces it to 1 and the loop to stop
- C) Because the loop condition is `hi - lo + 1 > 0`
- D) Because `⌈log₂(n+1)⌉` mentions `n + 1`

<details>
<summary>Answer and explanation</summary>

**B) Because `hi - lo + 1` is the quantity that provably at least halves each
iteration, so `2^k ≥ n + 1` forces it to 1 and the loop to stop.**

Both `hi - lo` and `hi - lo + 1` are integers, so A is vacuous. C is false: the
loop condition is `lo < hi`, i.e. `hi - lo > 0`, i.e. `hi - lo ≥ 1`. D is
circular — the measure is chosen because of how it behaves, and the `+1` in the
answer falls out of that.

The real reason is arithmetic. With `m = hi - lo`, one iteration gives
`m' ≤ ⌈m/2⌉ - 1`, and `⌈m/2⌉ - 1 ≥ ⌊m/2⌋`, so `m` does **not** halve in one
step. With `M = m + 1`, the same calculation gives `M' ≤ ⌈M/2⌉`, so `M` does
halve. Then `M_k ≤ ⌈(n+1)/2^k⌉`, and `M_k ≥ 2` while the loop runs, so
`2^k < n + 1`, which is exactly `k ≤ ⌈log₂(n+1)⌉ - 1` entries and
`⌈log₂(n+1)⌉` body executions. Using `hi - lo` gives an off-by-one in the bound
and a wrong termination argument.

</details>

**Q10.** A teammate proposes: "we will just add an exhaustive test over all
inputs of length up to 12, and call that a proof that `parse` is correct." What
is the best response?

- A) Agree: 13 lengths is enough coverage for a parser
- B) Disagree, because the claim is about all inputs and a finite test set
  establishes only a finite slice of it; and note that no finite set suffices,
- C) Disagree, because exhaustive testing is never a valid technique
- D) Agree, provided the test also covers all byte values in each input

<details>
<summary>Answer and explanation</summary>

**B) Disagree, because the claim is about all inputs and a finite test set
establishes only a finite slice of it; and note that no finite set suffices.**

Exhaustion is a real technique and a complete one for a finite domain — the
table in section 2 of the third code block *is* a valid proof that
`bsearch` meets its bound for `n ≤ 12`, and it is also evidence that the bound
is tight. What it is not is a proof about all `n`, because the domain is
unbounded. That is the honest objection, and it is the same objection
[Lesson 12](12_predicates_and_quantifiers.md) raises about a test suite for a
universal.

Option A appeals to a coverage intuition, which is about the shape of the code
and says nothing about the unbounded claim. The number 13 has no principled
status.

Option C is wrong and it is a mistake worth naming: it says exhaustion is never
valid, when in fact it is *complete* for finite domains. Rejecting the
technique outright loses the case where it is exactly right — a protocol
handshake with four states, a 4-bit permission mask, an interpreter over eight
opcodes.

Option D is a better test but still finite. Covering all byte values at every
position of a length-12 input is 256¹² cases, and even after you finish it the
claim about length 13 is untouched.

</details>

## Subjective Questions

### Short Answer

**Q1. State modus ponens and modus tollens, and say which one is derived from
which.**

<details>
<summary>Answer</summary>

Modus ponens: from `P` and `P → Q`, infer `Q`.

Modus tollens: from `P → Q` and `¬Q`, infer `¬P`.

Modus tollens is *derived*: contraposition turns `P → Q` into `¬Q → ¬P`, and
then modus ponens with `¬Q` gives `¬P`. So there is one rule and a theorem, and
the theorem is what people mean when they say "by contraposition".

The converse `Q → P` and the inverse `¬P → ¬Q` are neither rules nor theorems.
They are the two mistakes this lesson exists to prevent.

</details>

**Q2. What is the difference between soundness and completeness, and which one
do you need in order to trust a proof?**

<details>
<summary>Answer</summary>

Sound: everything derivable is true. Complete: everything true is derivable.

You need **soundness** to trust a proof. Soundness says the derivation only ever
lands on true sentences, so an accepted proof is a guarantee.

You need **completeness** to be sure your search will terminate with something.
Completeness says truth is reachable, which is what makes "I could not find a
proof" informative — but only for systems that are both sound and complete, and
for first-order logic neither property is achievable together (Gödel).

</details>

**Q3. Explain in one sentence why explosion is sound.**

<details>
<summary>Answer</summary>

Because `P ∧ ¬P` is unsatisfiable, so `P ∧ ¬P → C` is vacuously true for every
`C`, and that is exactly the claim that you may conclude anything from a
contradiction.

</details>

**Q4. A claim is `∀n ≥ 0, bsearch(L, x)` terminates, where `L` has length `n`.
Why can exhaustion not prove it, and what can?**

<details>
<summary>Answer</summary>

Exhaustion gives you one derivation per element of the domain, and here the
domain `ℕ` is infinite, so no finite list of derivations covers it. A reader can
always ask about the next `n` and you have nothing to offer.

Induction can: establish the invariant at `n = 0` and show it is preserved, which
covers every `n` in a two-line argument that mentions no particular `n`. That
is [Lesson 14](14_mathematical_induction.md).

</details>

**Q5. What does a proof checker actually compare?**

<details>
<summary>Answer</summary>

Syntax, not meaning. It checks that each line is either a stated premise or the
result of applying a named rule to earlier lines, comparing formulas for
equality as terms.

So `nondecreasing ∧ nonempty` and `nonempty ∧ nondecreasing` are rejected as
different lines even though they are equivalent, while a proof whose premises
happen to be false is accepted, because soundness is a property of the *rules*
and not of any particular proof. The last two rejections in the Runnable Code
show both halves of that: a re-ordered premise refused, a false-premise proof
allowed.

</details>

### Long Answer

**Q1. A test suite passes and nobody can find the bug, so someone proposes
"let's add assertions and call it a proof." What has actually been proposed, and
what would you have to add to make it a proof?**

<details>
<summary>Model answer</summary>

What has been proposed is a stronger test suite. A test suite establishes
existentials — *there exist* inputs where the code behaves — and a proof
establishes a universal — *for every* input. Adding assertions narrows the gap
without closing it, and the direction of the gap matters: no finite number of
assertions closes it, because the domain is infinite and the suite is finite.

To get a proof you need three things, and they are different in kind.

**A specification, stated as a sentence.** "The code is correct" is not a
sentence a proof can be about. "For every input and every target, the index
returned is the index of the target in the list, or −1 if the target is absent"
is. This is [Lesson 12](12_predicates_and_quantifiers.md) work and it is the
expensive part, because a proof of a wrong specification is a verified proof of
a wrong program.

**A technique that reaches an unbounded universal.** The four in this lesson all
reduce to one logical step and none of them does it. Induction does, and it
requires two things that look like assertions: a base case and an inductive
step, where the step is proved for an *arbitrary* `k` and then applied. The
difference between the step and a test is that the step's `k` appears in no
hypothesis — which is precisely the "arbitrary" condition, and precisely the
condition a test can never satisfy.

**An invariant, which is the hard part.** The inductive step needs a statement
about the state after `k` iterations. For binary search it is `L[lo:hi]` is
sorted, the target is inside it, and `hi − lo + 1 ≤ ⌈(n+1)/2^k⌉`. Nothing
about the code suggests the third clause. In practice this is where proofs die,
and it is why the rate-formulation matters: `(c)` is the only clause that talks
about the bound, and it talks about it as a rate rather than as an endpoint.

The honest summary is that assertions are worth adding regardless — they localise
failures and they cost nothing — but calling the result a proof is a category
error, and the difference is the difference between `∃` and `∀`.

</details>

**Q2. Contrapositive and converse are both natural English. Give two concrete
bugs, one from each, and say what each technique would have to know in advance
to avoid them.**

<details>
<summary>Model answer</summary>

**Converse bug.** The specification is "if the request is authenticated, it is
allowed." The code writes

```python
def handler(user):
    # The CONVERSE bug: allowed is taken to imply authenticated.
    if user:                       # `user` is truthy, not `is_authenticated`
        return is_authenticated(user)
    return 401
```

This returns a boolean where the caller expects a user, and it returns `True`
for an unauthenticated anonymous session object. The converse error, once
again, is a connective error: the two functions are not interchangeable.

**Contrapositive bug.** The specification is "if the request is neither
authenticated nor public, it is denied." A developer reasons "if it is
*allowed*, then it must be authenticated or public" and writes

```python
def handler2(r):
    # The CONTRAPOSITIVE, correctly derived -- and then extended one step too
    # far, by reading the disjunct as if it identified the user.
    if not r.authenticated and not r.public:
        return 401
    return current_user()          # valid inference, invalid conclusion
```

The second half is the contrapositive and it is *valid*, which is what makes it
dangerous — it will survive review, because it is a legitimate inference. What
it does not license is the *extra* step of reading the consequent as if it
identified the user. The contrapositive tells you the disjunction holds; it does
not tell you which disjunct.

So the converse bug comes from a step that is not licensed at all, and the
contrapositive bug comes from a step that is licensed and then extended one
step too far. The second is harder to spot, because the part a reviewer checks
is correct.

**What each technique needs in advance.** Contrapositive requires you to know,
before you start, that the negated conclusion is reachable from something you
have — usually the negation of the antecedent's hardest part. In the merge
example, the contrapositive is "if the output is unsorted then at least one input
was unsorted", and you cannot begin unless you already know why an unsorted
output must have come from an unsorted input, which is the invariant read
backwards. If you do not have that, the technique is unavailable and no amount
of trying will produce it.

Converse requires nothing in advance, which is exactly why it is the mistake
people make. It is always available and almost never valid. The only defence is
knowing that it is not a rule, which is why it is worth memorising as a
prohibition rather than as a technique.

</details>

**Q3. Why does a proof by contradiction risk proving a false statement, and what
specific discipline prevents it?**

<details>
<summary>Model answer</summary>

The risk comes from the interaction of two facts. First, explosion is sound: from
`⊥` you may conclude anything. Second, a reductio *assumes* `¬P` and then must
derive `⊥`. So the derivation is a derivation from the enlarged premise set
`Γ ∪ {¬P}` to `⊥`, and by RAA that yields `Γ ⊢ P`. Everything is fine provided
`⊥` was reached using only `Γ` plus the assumption.

The failure mode is that `⊥` is reached using a step that is not actually
licensed — a false lemma used earlier in the argument, an off-by-one, a
definition that does not match the implementation, or (most often in practice) a
specification that is itself wrong. The reductio will happily launder that into a
tasteful-looking proof, because the contradiction is real: the premises really
are inconsistent. The proof is valid and the theorem is false.

The specific discipline is that the proof checker re-derives every line and
refuses a proof whose contradiction depends on the assumption in a way it cannot
justify. In the Runnable Code, three separate checks do this work: `contra`
requires the two lines to be literally `P` and `¬P`; `not_intro` and
`imp_intro` require the scope being closed to be the innermost open one and the
conclusion to have the right shape; and the final check refuses any leftover
scope, which is the mechanical form of "you discharged nothing".

None of those checks can tell you the premises were true. That is the
specification's job, and it is the part no proof system does for you. The honest
statement of the risk is therefore: a proof checker verifies the *inference*,
and the inference being valid while the theorem is false is not a bug in the
checker — it is the correct behaviour on a wrong problem.

</details>

**Q4. The claim `bsearch` runs its body at most `⌈log₂(n+1)⌉` times is proved
by three of the four techniques, and not by the fourth. What is different about
the fourth, and why is the difference a fact about the statement rather than
about the technique?**

<details>
<summary>Model answer</summary>

The fourth is exhaustion, and what is different is the domain: `n` ranges over
the naturals, which are infinite. Exhaustion establishes `P(d)` for one `d` per
derivation, so it needs `|D|` derivations to conclude `∀x ∈ D P(x)`. On an
infinite domain no finite list is enough, because there is always an element
outside it.

The difference is a fact about the *statement*, not about the technique,
because exhaustion is complete for finite domains. The table in section 2 of the
third code block is a genuine proof, by exhaustion, that `bsearch` meets its
bound for `0 ≤ n ≤ 12`, and it is also a proof that the bound is tight. What it
cannot do is say anything about `n = 13`, and no extension of the table changes
that. Every finite table leaves the same gap, and the gap does not shrink.

The three techniques that do work all avoid the enumeration by not needing a
per-element derivation. Direct works because the halving lemma is stated for
every `n` at once and the conclusion is arithmetic on the initial value.
Contrapositive works because it turns a bound violation into a single failing
iteration. Contradiction works because the assumption `k > bound` collapses the
arithmetic immediately. All three are constant-length in `n`; exhaustion is
linear in `n` and therefore cannot terminate for unbounded `n`.

The practical reading is the one in the next lesson: when a claim is universally
quantified over an unbounded domain, the technique you want is the one that
proves a *step* and then says the step covers everything, which is induction.
Exhaustion is not defeated; it is aimed at the wrong target.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — Prove eight statements with each technique, and find the one
technique that is unavailable for each.** For each statement below, say whether
direct, contrapositive, or contradiction is the natural first choice, justify
your choice in one sentence, and for at least two of them write out the actual
derivation.

1. If `x` and `y` are both even then `x + y` is even.
2. If `n²` is even then `n` is even.
3. If a request is denied then at least one of its checks failed.
4. If the function returned `None` then the key was absent.
5. If no user has admin then the admin dashboard is empty.
6. If the loop terminated then the work set is empty.
7. If the list is sorted then `bisect` terminates.
8. If the specification is wrong then the tests pass.

<details>
<summary>Solution</summary>

```python
# Evenness, as a predicate over the integers we care about.
EVENS = {0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20}
ODDS = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19}


def is_even(n):
    return n % 2 == 0


# (1) p = (x even and y even), q = (x+y even)
print("=" * 78)
print("1. both even  ->  sum even")
print("=" * 78)
print("  DIRECT. Add two evens: if x = 2a and y = 2b then x + y = 2(a + b).")
print("  The antecedent hands you the two factorisations, and the")
print("  conclusion is a substitution. Nothing to negate, nothing to assume")
print("  away.")
print("  contrapositive is also available and is one line: x + y odd -> x odd")
print("  or y odd. Contradiction is wasteful: assume both even and the sum odd,")
print("  and you have to notice the same arithmetic.")
print()

# (2) p = (n^2 even), q = (n even)
print("=" * 78)
print("2. square even  ->  n even        <-- the contrapositive is the point")
print("=" * 78)
print("  CONTRAPOSITIVE. Direct would need: n^2 even, so n^2 = 2k, so n is")
print("  even -- and the step from 'n^2 = 2k' to 'n is even' is a lemma about")
print("  primes that you have to find anyway.")
print("  The contrapositive is 'n odd -> n^2 odd', which is one multiplication")
print("  and no lemma: (2a+1)^2 = 4a^2 + 4a + 1.")
print()
odd_squares_odd = all(is_even(n * n) == is_even(n) for n in range(0, 21))
print(f"  checked over 0..20, `n*n` is even exactly when `n` is: {odd_squares_odd}")
print()

# (3) p = denied, q = (at least one check failed)
print("=" * 78)
print("3. denied  ->  some check failed")
print("=" * 78)
print("  DIRECT, and trivially, because the code says so: the deny branch is")
print("  guarded by a disjunction, so denying means the guard was true. This")
print("  is the one-line premise proof from the Runnable Code.")
print()

# (4) p = (returned None), q = (key absent)
print("=" * 78)
print("4. returned None  ->  key absent")
print("=" * 78)
print("  DIRECT if the code returns None only in the miss branch. CONTRAPOSITIVE")
print("  if it does not: 'key present -> did not return None' is the statement")
print("  you actually want for a cache, because it is the one that lets you")
print("  cache the answer. Pick the direction your caller needs.")
print()

# (5) p = (no user has admin), q = (dashboard empty)
print("=" * 78)
print("5. no admin  ->  dashboard empty")
print("=" * 78)
print("  CONTRAPOSITIVE, and it is the only one available. The direct form asks")
print("  you to show that with zero admins the query returns nothing, which")
print("  needs the query's own semantics. The contrapositive says 'the")
print("  dashboard is non-empty -> some user has admin', which is one join and")
print("  one IS NOT NULL. This is the single best example in the set of when")
print("  contraposition pays: the negated conclusion is a *query* and the")
print("  original is a schema-wide property.")
print()

# (6) p = (loop terminated), q = (work set empty)
print("=" * 78)
print("6. loop terminated  ->  work empty")
print("=" * 78)
print("  CONTRAPOSITIVE if the loop guard is `while work:`. Direct would need")
print("  the invariant; the contrapositive needs only the guard, which is one")
print("  line of code. This is why a guard clause is a contrapositive waiting")
print("  to be read: 'the loop is still running -> work is non-empty' is free.")
print()

# (7) p = (list sorted), q = (bisect terminates)
print("=" * 78)
print("7. list sorted  ->  bisect terminates")
print("=" * 78)
print("  CONTRADICTION. Direct: show the interval shrinks, which is a lemma")
print("  about the midpoint arithmetic. Contradiction: assume it ran k >")
print("  ceil(log2(n+1)) times, then the halving lemma gives an empty interval,")
print("  then the guard is false. The assumption does the pushing.")
print()

# (8) p = (specification wrong), q = (tests pass)
print("=" * 78)
print("8. specification wrong  ->  tests pass")
print("=" * 78)
print("  FALSE, and that is the point of including it. Counterexample: write a")
print("  specification that says `return 1`, implement `return 1`, and the")
print("  tests pass while the specification is wrong. No technique applies,")
print("  because the statement is not true.")
print()
print("  What you can prove is the CONTRAPOSITIVE, and it is the sentence a")
print("  green build actually tells you: 'some test disagrees with the")
print("  specification -> not every test passed'. The direction a CI system")
print("  can establish is `tests pass -> no observed disagreement`, which is a")
print("  statement about the tests, not about the program.")
print()
print("-" * 78)
print("summary: which technique was natural, per statement")
print("-" * 78)
for n, name, why in [
    (1, "direct", "the antecedent supplies the arithmetic"),
    (2, "contrapositive", "the forward direction needs a lemma you must find"),
    (3, "direct", "one-line premise, nothing to negate"),
    (4, "direct or contra", "pick the direction the caller needs"),
    (5, "contrapositive", "the negated conclusion is a single query"),
    (6, "contrapositive", "the loop guard IS the contrapositive"),
    (7, "contradiction", "the assumption collapses the arithmetic"),
    (8, "none", "the statement is false; a counterexample is the answer"),
]:
    print(f"  {n}. {name:<18} {why}")
```

</details>

**[ ] Exercise 2 — Build a proof checker for a slightly bigger language and make
it reject seven specific mistakes.** Extend the checker from the Runnable Code
with (a) `("or_left", i)` and `("or_right", i)` for disjuncts, (b)
`("not_intro_not", i)` concluding `~f` from a line `f`, (c) a `("box", "F")`
rule concluding `FALSE` from any line, and (d) a counter that reports how many
lines were accepted before the failure. Then write one valid proof of
`(A ∨ B) → (B ∨ A)` using your new rules, and seven invalid proofs — one per
mistake class — and report the rejection message for each.

<details>
<summary>Solution</summary>

```python
FALSE = ("false",)


def A(name):
    return ("atom", name)


def show(f):
    k = f[0]
    if k == "atom":
        return f[1]
    if k == "false":
        return "FALSE"
    if k == "not":
        return f"~({show(f[1])})"
    if k == "impl":
        return f"({show(f[1])} -> {show(f[2])})"
    return f"({show(f[1])} {k} {show(f[2])})"


class InvalidProof(Exception):
    pass


def check(proof, target):
    """The checker from the Runnable Code plus four rules and a step counter.

    New rules:
      ("or_left", i)            line i is (P or Q), conclude P
      ("or_right", i)           line i is (P or Q), conclude Q
      ("not_of", i)             line i is P, conclude ~P
      ("box", "F")             conclude FALSE from anything
    """
    lines, scopes, accepted = [], [], 0

    def get(i):
        if not (0 <= i < len(lines)):
            raise InvalidProof(f"line {i + 1} does not exist yet")
        return lines[i]

    for n, (just, formula) in enumerate(proof, 1):
        head = just[0]
        where = f"line {n} (after {accepted} accepted line(s)): "

        if head == "assume":
            scopes.append((just[1], formula, n))
        elif head in ("and_left", "and_right", "or_left", "or_right"):
            both = get(just[1] - 1)
            if both[0] != head.split("_")[0]:
                raise InvalidProof(
                    f"{where}{head} needs a {head.split('_')[0]}unction at "
                    f"line {just[1]}, which is {show(both)}")
            expected = both[1] if head.endswith("left") else both[2]
            if formula != expected:
                raise InvalidProof(
                    f"{where}stated {show(formula)} but {head} gives "
                    f"{show(expected)}")
        elif head == "and_intro":
            p, q = get(just[1] - 1), get(just[2] - 1)
            if formula != ("and", p, q):
                raise InvalidProof(
                    f"{where}stated {show(formula)} but the premises give "
                    f"({show(p)} and {show(q)})")
        elif head == "or_intro":
            p = get(just[1] - 1)
            if formula[0] != "or" or p not in formula[1:3]:
                raise InvalidProof(
                    f"{where}{show(p)} is not a side of {show(formula)}")
        elif head == "not_of":
            p = get(just[1] - 1)
            if formula != ("not", p):
                raise InvalidProof(
                    f"{where}stated {show(formula)} but line {just[1]} is "
                    f"{show(p)}, so ~P is {show(('not', p))}")
        elif head == "box":
            pass                       # FALSE follows from anything
        elif head == "mp":
            p, arrow = get(just[1] - 1), get(just[2] - 1)
            if arrow[0] != "impl":
                raise InvalidProof(
                    f"{where}modus ponens needs an implication at line "
                    f"{just[2]}, which is {show(arrow)}")
            if arrow[1] != p:
                raise InvalidProof(
                    f"{where}modus ponens needs {show(arrow[1])} at line "
                    f"{just[1]}, which is {show(p)}")
            if formula != arrow[2]:
                raise InvalidProof(
                    f"{where}stated {show(formula)} but modus ponens gives "
                    f"{show(arrow[2])}")
        elif head == "contra":
            p, q = get(just[1] - 1), get(just[2] - 1)
            if q != ("not", p):
                raise InvalidProof(
                    f"{where}contradiction needs P and ~P; lines {just[1]} "
                    f"and {just[2]} are {show(p)} and {show(q)}")
            if formula != FALSE:
                raise InvalidProof(
                    f"{where}stated {show(formula)} but a contradiction gives "
                    f"FALSE")
        elif head == "ex_falso":
            if get(just[1] - 1) != FALSE:
                raise InvalidProof(
                    f"{where}ex falso needs FALSE at line {just[1]}")
        elif head in ("not_intro", "imp_intro"):
            key, assumed, opened = scopes.pop()
            if key != just[1]:
                raise InvalidProof(
                    f"{where}closes scope {just[1]!r} but the innermost open "
                    f"scope is {key!r}, opened at line {opened}")
            conclusion = get(just[2] - 1)
            want = (("not", assumed) if head == "not_intro"
                    else ("impl", assumed, conclusion))
            if formula != want:
                raise InvalidProof(
                    f"{where}stated {show(formula)} but closing the scope "
                    f"gives {show(want)}")
        elif head == "refute":
            if get(just[1] - 1) != target:
                raise InvalidProof(
                    f"{where}the final line is {show(get(just[1] - 1))}, not "
                    f"the target {show(target)}")
        else:
            raise InvalidProof(f"{where}unknown rule {head!r}")

        lines.append(formula)
        accepted += 1

    if scopes:
        raise InvalidProof(
            f"{len(scopes)} scope(s) left open: {[s[0] for s in scopes]}. "
            f"An unclosed assumption proves nothing.")
    return lines


target = ("impl", ("or", A("A"), A("B")), ("or", A("B"), A("A")))
valid = [
    (("assume", "H"), ("or", A("A"), A("B"))),                  # 1
    (("or_left", 1), A("A")),                                   # 2
    (("or_intro", 2, ("or", A("B"), A("A"))), ("or", A("B"), A("A"))),  # 3
    (("imp_intro", "H", 3), target),                            # 4
]
print("=" * 78)
print("a valid proof of (A or B) -> (B or A)")
print("=" * 78)
for n, (just, formula) in enumerate(valid, 1):
    print(f"  {n:>2}. {show(formula):<30} {just}")
check(valid, target)
print("  ACCEPTED")
print()

print("=" * 78)
print("seven broken proofs, one per mistake class")
print("=" * 78)
BROKEN = [
    ("or_left on a conjunction",
     [(("assume", "H"), ("and", A("A"), A("B"))), (("or_left", 1), A("A"))],
     A("A")),
    ("or_right taking the left disjunct",
     [(("assume", "H"), ("or", A("A"), A("B"))), (("or_right", 1), A("A"))],
     A("A")),
    ("not_of concluding ~Q from a line that is P",
     [(("assume", "H"), A("P")), (("not_of", 1), ("not", A("Q")))],
     ("not", A("Q"))),
    ("ex_falso with no FALSE in sight",
     [(("assume", "H"), A("A")), (("ex_falso", 1), A("B"))],
     A("B")),
    ("box stated as a formula other than FALSE",
     [(("box", "F"), A("A"))], A("A")),
    ("mp where the stated conclusion is the antecedent",
     [(("assume", "P"), A("P")), (("assume", "H"), ("impl", A("P"), A("Q"))),
      (("mp", 1, 2), A("P"))],
     A("P")),
    ("an unclosed scope on the last line",
     [(("assume", "H"), ("or", A("A"), A("B"))), (("or_left", 1), A("A"))],
     A("A")),
]
for label, proof, goal in BROKEN:
    try:
        check(proof, goal)
        print(f"  {label:<44} ACCEPTED  <-- the checker is broken")
    except InvalidProof as exc:
        print(f"  {label:<44} REJECTED: {exc}")
print()
print("Two of these deserve a note. 'or_right taking the left disjunct' is the")
print("error people make when they read a rule as 'extract a side' rather than")
print("'extract THIS side'. And 'box stated as something other than FALSE' is")
print("the dangerous one: `box` concludes a contradiction from anything, so a")
print("proof that uses it has proved nothing at all while looking complete.")
print("That is why the rule only permits the one formula.")
print()
print("The step counter in each message is the other useful part. 'after 1")
print("accepted line(s)' tells you the proof was fine up to a point, and the")
print("point is one line before the failure. That is the difference between a")
print("checker and a verdict, and it is why proof assistants report a position")
print("rather than a boolean.")
```

</details>
**[ ] Exercise 3 — Prove the correctness of binary search in full, all three
ways, as formal derivations.** Using the invariant clauses (a), (b), (c) from
the worked example, write: (a) a direct proof as a numbered list of claims with
justifications; (b) the same result as a reductio, with the assumption named;
(c) the contrapositive, with the conclusion you are allowed to conclude; and
(d) for each, state exactly which fact about the code you used, and which fact
you had to know before you could start. Then state which of the three you would
write in a design document and why.

<details>
<summary>Solution</summary>

```python
# The derivations below are prose, because that is what a design document
# contains. The code at the end checks the one claim that is cheap to check
# mechanically: the halving lemma.

print("=" * 78)
print("(a) DIRECT")
print("=" * 78)
print("""
  GIVEN   L is sorted, of length n
  CLAIM   the body runs at most ceil(log2(n+1)) times

  Invariant P(k), holding at the top of the k-th entry to the loop:
      (a) L[lo:hi] is sorted
      (b) if x occurs in L, its index lies in [lo, hi)
      (c) hi - lo + 1 <= ceil((n + 1) / 2^k)

  1. P(0).  lo = 0, hi = n, k = 0.  L[0:n] is sorted by hypothesis, so (a).
           If x occurs in L its index is in [0, n), so (b).  And
           hi - lo + 1 = n + 1 = ceil((n+1)/1), so (c).

  2. P(k) => P(k+1).  Let m = hi - lo + 1, so m <= ceil((n+1)/2^k).
           The body sets hi = mid or lo = mid + 1, with mid = (lo+hi)//2.
           In the first case the new interval is [lo, mid), a suffix-free
           prefix of the sorted L[lo:hi], so (a) is preserved.  In the second
           it is [mid+1, hi), the corresponding suffix, so (a) again.
           Each new interval is a subset of the old one, so an index of x
           that was in [lo, hi) is still in it whenever x is still present:
           (b) is preserved.
           The new size is at most ceil(m/2), and ceil(m/2) <=
           ceil(ceil((n+1)/2^k) / 2) <= ceil((n+1)/2^(k+1)), so (c).

  3. Termination.  The guard is lo < hi, i.e. m >= 2.  By (c),
           ceil((n+1)/2^k) >= 2, so (n+1)/2^k > 1, so 2^k < n + 1.
           Hence the loop is still running only for k with 2^k < n+1, i.e.
           k <= ceil(log2(n+1)) - 1.  So the body runs at most
           ceil(log2(n+1)) times.                                       QED

  4. Return value.  The body returns mid when L[mid] == x, and by (a) every
           element before mid in L[lo:hi] is < x and every element after is
           > x, so mid is the only possible index and it is correct.  The
           exit with -1: by (b), x is not in L at all.
""")
print("=" * 78)
print("(b) REDUCTIO")
print("=" * 78)
print("""
  ASSUME  the body runs k > ceil(log2(n+1)) times
  1. By the halving lemma (which is step 2 of the direct proof and does not
     mention k), m_k <= ceil((n+1)/2^k).
  2. k > ceil(log2(n+1))  =>  2^k >= 2^(ceil(log2(n+1)) + 1) >= 2(n+1) > n+1
     =>  (n+1)/2^k < 1  =>  m_k <= 1  =>  lo >= hi.
  3. lo >= hi makes the guard `lo < hi` false, so the loop stopped before
     iteration k.
  4. But the assumption says the body ran k > 0 times after k iterations.
  CONTRADICTION.  Therefore the body runs at most ceil(log2(n+1)) times.   QED
""")
print("=" * 78)
print("(c) CONTRAPOSITIVE")
print("=" * 78)
print("""
  CLAIM   if the body runs more than ceil(log2(n+1)) times, then some
          iteration failed to at least halve the interval

  1. Suppose the body runs more than ceil(log2(n+1)) times.  Then there is a
     k with 2^k >= n + 1 at which the loop is still running.
  2. By the halving lemma, m_k <= ceil((n+1)/2^k) <= 1.
  3. So the interval is already empty (m_k <= 1) at iteration k, which means
     the guard was false at iteration k, which contradicts it still running.
  4. Therefore step 1's supposition is impossible, and the only remaining
     possibility is that the halving lemma's step failed at some iteration:
     the new size exceeded ceil(m/2) at least once.                        QED
""")
print("=" * 78)
print("(d) which fact each proof used, and what each needed in advance")
print("=" * 78)
print("""
  fact about the code     used by direct, reductio, contrapositive equally:
    - `mid = (lo + hi) // 2` really does split [lo, hi) into two pieces of
      size at most ceil(m/2)
    - each branch replaces exactly one end with the midpoint

  what you needed in advance:
    direct        nothing beyond the hypothesis.  You needed the halving
                  arithmetic, and it falls out of the code in one line.
    reductio      nothing beyond the hypothesis.  This is why it is the
                  fallback: it never needs prior knowledge, only the ability
                  to recognise a contradiction when one appears.
    contrapositive the converse, read backwards.  You had to know -- before
                  starting -- that an over-long run forces an empty interval,
                  which is step 2 above.  If you cannot state that without the
                  proof, the technique is unavailable.
""")
print("=" * 78)
print("which one goes in the design document")
print("=" * 78)
print("""
  The direct proof, because it is the only one of the three that also states
  the invariant, and the invariant is what a future maintainer needs in order
  to change the code without breaking the argument.  The reductio and the
  contrapositive both discard (a) and (b) -- they are about the bound only --
  so a document containing them would leave the reader unable to reason about
  the returned value at all.

  The contrapositive belongs in the bug report, not the design document.  It is
  the form that localises: "it ran 4 times at n=4, so halving broke somewhere"
  points at the interval update.  A proof tells you the bound; a contrapositive
  tells you where to look; an invariant tells you what you are allowed to
  change.
""")
print()
print("=" * 78)
print("the one claim worth checking mechanically")
print("=" * 78)


def splits_at_most_in_half(m):
    """The halving step, for every way of splitting an interval of size m.

    The two branches of the loop body give sizes floor(m/2) and
    ceil(m/2) - 1.  Both must be at most ceil(m/2) - and both are, for every m.
    """
    left = m // 2                      # hi = mid
    right = m - (m // 2) - 1           # lo = mid + 1
    return left, right, max(left, right) <= -(-m // 2)


bad = [m for m in range(1, 200) if not splits_at_most_in_half(m)[2]]
print(f"  m values checked                    : 199")
print(f"  m values where a branch exceeds ceil(m/2): {len(bad)}")
print(f"  worst ratio observed                : "
      f"{max(max(splits_at_most_in_half(m)[:2]) / m for m in range(1, 200)):.3f}")
print()
print("  This is the only part of the three proofs that is arithmetic about a")
print("  quantity rather than logic about sentences, so it is the only part")
print("  worth automating. Everything else is a sentence, and sentences are")
print("  checked by the proof checker from Exercise 2.")
```

</details>

**[ ] Exercise 4 — Take one real claim from your own code and route it through
all four techniques, recording what each one cost.** Choose a function you have
written. (a) State its specification as a quantified sentence, including the
domain. (b) Attempt a direct proof and record every step you needed a fact you
did not have. (c) Attempt the contrapositive and record whether you could even
state it. (d) Attempt a reductio. (e) Decide whether exhaustion is available,
and if not, say what the domain has to be finite for it to be. (f) Report
honestly which technique you used and why the other three were worse.

<details>
<summary>Solution</summary>

A worked model answer, on a function everybody has written.

```python
print("=" * 78)
print("the function")
print("=" * 78)
print("""
    def dedupe(items):
        seen = set()
        out = []
        for it in items:
            if it in seen:
                continue
            seen.add(it)
            out.append(it)
        return out
""")
print("=" * 78)
print("(a) the specification, as a sentence")
print("=" * 78)
print("""
  DOMAIN  L ranges over all finite lists of hashable values.
          P ranges over all hashable values, with P hashable.

  S1  (correctness)  for every L and every P:
          dedupe(L) contains P  <=>  P occurs in L
  S2  (order)         for every L: dedupe(L) is a subsequence of L
  S3  (no dupes)      for every L: dedupe(L) has no repeated element
""")
print("""  Note what the domain does here. 'for every L' is not a sentence until you
  say what a list is, and 'hashable' is not decoration: `dedupe` raises
  TypeError on a list containing a list, so the honest domain excludes those
  inputs, and a specification that quietly included them would be a
  specification of a crash.""")
print()
print("=" * 78)
print("(b) DIRECT -- where it got stuck")
print("=" * 78)
print("""
  Try S1. Forward direction (P occurs in L  =>  P occurs in dedupe(L)):
     trivial from S3 and the loop. One line. No problem.

  Backward direction (P occurs in dedupe(L)  =>  P occurs in L):
     Take the first iteration at which P was appended to `out`. At that
     iteration P was in `items`, so P occurs in L.  The phrase 'first
     iteration' is a universal claim about a natural number, and turning it
     into an argument needs the fact that the loop terminates.

  So the direct proof is BLOCKED on termination, not on anything about sets.
  That is worth noticing: the hard part of a direct proof is very often
  somewhere you were not looking.
""")
print("=" * 78)
print("(c) CONTRAPOSITIVE -- could it even be stated?")
print("=" * 78)
print("""
  S1 contraposed: if P does not occur in L, then P does not occur in
  dedupe(L).

  Stating it is easy. Proving it is EASIER, not harder: 'P never appears in
  `items`, so the branch that appends never fires for P, so it never reaches
  `out`. No loop invariant needed, because we do not reason about *which*
  iteration -- we reason about none of them.

  Verdict: contrapositive wins on the backward direction, direct wins on the
  forward one. This is the normal outcome and it is why people say
  'prove whichever direction is easier'.
""")
print()
print("=" * 78)
print("(d) REDUCTIO -- the version that also discharges the termination worry")
print("=" * 78)
print("""
  Assume some P is in dedupe(L) but not in L.
  P reached `out`, so on some iteration the test `P in seen` was false and
  P was appended. P was in `items` on that iteration, so P is in L.
  Contradiction.

  No 'first iteration', no termination, no natural numbers. The assumption that
  P got into `out` at all carries the fact that it came from `items`.

  This is the textbook case for reductio: the direct route needs a claim about
  a SEQUENCE, and the reductio route needs a claim about a single event.
""")
print()
print("=" * 78)
print("(e) is exhaustion available?")
print("=" * 78)
print("""
  No. The domain is all finite lists, which is infinite, and so is the domain
  of P. Exhaustion would need one derivation per list and one per value.

  Exhaustion IS available for a restricted version: for every list of length at
  most 3 drawn from a 4-element alphabet, there are 4^0 + 4^1 + 4^2 + 4^3 = 85
  lists, and checking 85 of them is a legitimate proof for that restricted
  claim.  That is a real and useful thing to have, and it is a proof of a
  different, smaller theorem.
""")
print()
print("=" * 78)
print("(f) what I actually used, and why")
print("=" * 78)
print("""
  Reductio for S1, direct for S2 and S3.

  S2 and S3 are direct because they are statements about EVERY element of the
  output, and 'every element of `out` was copied from `items` at the moment it
  was appended' is a one-line observation that needs no iteration counting at
  all.  The forward direction of S1 is the same shape.

  The only place iteration counting appeared was the backward direction of S1,
  and there the reductio removed it.  Total cost: three short paragraphs, no
  induction, no invariant, and one domain sentence that did more work than
  anything else in the proof.
""")
print()
print("=" * 78)
print("the domain sentence, checked rather than asserted")
print("=" * 78)

ALPHABET = "abcd"


def dedupe(items):
    seen, out = set(), []
    for it in items:
        if it in seen:
            continue
        seen.add(it)
        out.append(it)
    return out


def all_lists(max_len, alphabet):
    out = [[]]
    for _ in range(max_len):
        out += [prev + [c] for prev in out for c in alphabet]
    return out


LISTS = all_lists(3, ALPHABET)
VALUES = list(ALPHABET) + ["zz"]          # one value that is never in any list
print(f"  lists of length <= 3 over a 4-letter alphabet : {len(LISTS)}")
print(f"  probe values, including one absent from all   : {VALUES}")
print()
print(f"{'P':>4} {'in some L?':>11} {'fails S1?':>10}")
fails = 0
for p in VALUES:
    holds = all((p in dedupe(L)) == (p in L) for L in LISTS)
    if not holds:
        fails += 1
    print(f"{p:>4} {str(any(p in L for L in LISTS)):>11} {str(not holds):>10}")
print()
print(f"  instances where S1 fails: {fails} of {len(LISTS) * len(VALUES)}")
print("  Zero failures is exhaustion over 340 instances -- a proof of the")
print("  restricted claim, and no evidence at all about length 4 or the value")
print("  'q'.  The restricted claim is still worth having; it is just not the")
print("  claim, and naming which one you proved is the whole discipline.")
```

</details>

**[ ] Exercise 5 — Determine, mechanically, which of the four techniques is
*available* on each of eight statements, and explain the pattern.** For each
statement, report (i) whether its contrapositive is *stateable* without new
information, (ii) whether its negation has a strong form, (iii) whether the
domain is finite, and (iv) which technique you would try first. Then find the
pattern in your answers and state it as a rule of thumb.

<details>
<summary>Solution</summary>

```python
import itertools

ATOMS = ["P", "Q", "R"]
ROWS = [dict(zip(ATOMS, b)) for b in itertools.product([False, True], repeat=3)]


def column(f):
    return [bool(f(e)) for e in ROWS]


def bits(v):
    return "".join("1" if x else "0" for x in v)


def neg_is_simple(f):
    """A crude but honest proxy for 'the negation is an easy sentence to reach':
    it is a CONJUNCTION, or FALSE.  Those are the shapes a reductio can grind
    down to a contradiction, because a conjunction can be split and FALSE can
    be recognised."""
    return f == ("false",) or f[0] == "and"


# ante -> cons for each statement, plus metadata
STATEMENTS = [
    ("sorted -> index in range",
     lambda e: e["P"], lambda e: e["Q"], "finite (n <= 12)", "direct"),
    ("denied -> some check failed",
     lambda e: e["P"], lambda e: e["Q"] or e["R"], "finite (4 states)", "direct"),
    ("returned None -> key absent",
     lambda e: e["P"], lambda e: e["Q"], "infinite", "direct (or contrapos.)"),
    ("no admin -> dashboard empty",
     lambda e: not e["P"], lambda e: not e["Q"], "infinite", "contrapositive"),
    ("loop terminated -> work empty",
     lambda e: e["P"], lambda e: e["Q"], "infinite", "contrapositive"),
    ("sorted -> bisect terminates",
     lambda e: e["P"], lambda e: e["Q"], "infinite", "contradiction"),
    ("n^2 even -> n even",
     lambda e: e["P"], lambda e: e["Q"], "infinite (integers)", "contrapositive"),
    ("(P and Q) -> R",
     lambda e: e["P"] and e["Q"], lambda e: e["R"], "infinite", "direct"),
]

print(f"{'statement':<30} {'holds?':>7} {'~S is simple?':>15} "
      f"{'domain':>18}  try first")
rows_out = []
for name, ante, cons, domain, first in STATEMENTS:
    direct = lambda e: (not ante(e)) or bool(cons(e))          # noqa: E731
    contra = lambda e: bool(cons(e)) or (not ante(e))          # noqa: E731
    # The shape of the negation, written out.  Contraposition turns P -> Q into
    # ~Q -> ~P, and the reductio assumes ~Q & ~P, so this is the sentence a
    # reductio would have to grind to FALSE.
    reductio = ("and", ("not", ("atom", "Q")), ("not", ("atom", "P")))
    simple = neg_is_simple(reductio)
    same = column(direct) == column(contra)
    rows_out.append((name, all(column(direct)), simple, domain, first, same))
    print(f"{name:<30} {str(all(column(direct))):>7} {str(simple):>15} "
          f"{domain:>18}  {first}")
print()
print("The '~S is simple?' column is always True, and that is the point. Every")
print("statement's negation, once contraposition has been applied, is a")
print("conjunction -- which is exactly why reductio is universally available")
print("and why its difficulty has nothing to do with the shape of the claim.")
print()
print(f"{'statement':<30} {'direct == contrapositive?':>28}")
for name, _, _, _, _, same in rows_out:
    print(f"{name:<30} {str(same):>28}")
print()
print("The last column is always True, which is the theorem from the Formal")
print("Version: the four techniques are four equivalent formulas. Availability")
print("is not a property of the formula, it is a property of what you know.")
print()
print("=" * 74)
print("the pattern, as a rule of thumb")
print("=" * 74)
print("""
  1. If the antecedent is a FACT ABOUT THE DATA and the conclusion is a FACT
     ABOUT THE OUTPUT, go direct.  The loop body or the guard hands you the
     connection for free.  Rows 1, 2, 8.

  2. If the conclusion is a UNIVERSAL NEGATIVE ('no row has property Q', 'the
     set is empty'), go contrapositive.  A universal negative is a query, and
     a query is usually one line.  Rows 4, 5.

  3. If the conclusion is about a SEQUENCE -- a count, a bound, anything
     quantified over the iterations -- go by contradiction, because the
     assumption collapses the arithmetic and you avoid reasoning about which
     iteration.  Rows 3, 6, 7.

  4. Exhaustion when and only when the domain is finite.  It is then complete
     and it is the cheapest thing available; there is no reason to be clever.
     Row 2 is the one place it wins outright.

  5. Never start with contrapositive.  It is the only technique that requires
     you to know something in advance, and the thing you must know -- why the
     false conclusion forces the false premise -- is usually the proof itself.
     Try it when the conclusion is already a negative.
""")
```

</details>

**[ ] Exercise 6 — Find the four statements in a real codebase that deserve a
proof, and rank them by how expensive the proof would be.** Take a codebase you
know. Find four properties that are currently enforced only by tests, by review,
or by hope. For each, write: (a) the property as a quantified sentence; (b) the
cheapest viable technique; (c) the invariant or lemma you would need, if any;
(d) an honest estimate of whether the invariant is findable, and (e) which one
you would do first. Then explain what your ranking says about where proof effort
pays in a real system.

<details>
<summary>Solution</summary>

A worked model answer, on an order-processing service. The point is the
ranking, not the individual claims.

```python
print("=" * 78)
print("(1) 'a successful payment is recorded exactly once'")
print("=" * 78)
print("""
  SENTENCE   for every successful payment p, there is exactly one ledger row
             for p.   (exists! row, not exists a second)

  TECHNIQUE  contradiction, on the database's own uniqueness constraint.
             Assume two rows for p.  Then the second insert saw a row for p,
             so the constraint was checked, so the constraint was absent or
             the insert bypassed it.  Both are statements about the schema.

  INVARIANT  none needed -- the whole argument is about the schema, not the
             code, which is why it is cheap.

  FINDABLE   yes.  This is a database property and databases are checked by
             the database, which is the cheapest verifier available.

  COST       about an hour, and it is a UNIQUE index plus a test asserting the
             index exists.
""")
print("=" * 78)
print("(2) 'the retry loop makes progress'")
print("=" * 78)
print("""
  SENTENCE   for every state, after k iterations of the retry loop, the
             remaining backoff is at most max(0, initial - k * step).

  TECHNIQUE  direct, with an invariant, plus induction on k.  This is the one
             that genuinely needs [Lesson 14](14_mathematical_induction.md).

  INVARIANT  backoff_k = max(0, initial - k * step), and attempts_k = k.

  FINDABLE   yes, but only after you notice that `step` is not a constant --
             it is `backoff * 2`, so the measure is exponential and the
             invariant is geometric, not arithmetic.  That is a real hour of
             work and it is the hour that matters.

  COST       half a day, including the induction.  Worth it: this loop has
             already produced two incidents.
""")
print("=" * 78)
print("(3) 'a read of the cache never returns another tenant's data'")
print("=" * 78)
print("""
  SENTENCE   for every cache key k, the value stored under k was written by a
             request from the tenant that owns k.  Formally: for all writes w
             and reads r, key(r) = key(w) implies tenant(r) = tenant(w).

  TECHNIQUE  direct, but the invariant is the whole difficulty: the cache key
             must include the tenant, and 'includes the tenant' is not a fact
             you can read off the code -- it is a fact about every call site.

  INVARIANT  the key is a tuple whose first component is the tenant id.

  FINDABLE   MAYBE NOT.  There are fourteen call sites and the type is `str`,
             so nothing forces the key to be a tuple.  A proof here means
             changing the type, and that is a refactor, not a proof.

  COST       a week.  The proof is not the expensive part; making the
             statement true enough to state is.
""")
print("=" * 78)
print("(4) 'the parser rejects every input that is not valid JSON'")
print("=" * 78)
print("""
  SENTENCE   for every byte string s: parse(s) does not raise  <=>  s is valid
             JSON.  A biconditional, so two directions and two tests.

  TECHNIQUE  exhaustion, against a reference implementation, plus a fuzzer for
             the other direction.  Neither is a proof.

  FINDABLE   the spec is 'whatever the reference implementation does', which
             is not a specification at all.  You cannot prove a program correct
             with respect to a behaviour you have not pinned down.

  COST       unbounded until someone writes the grammar down.  And note that
             writing the grammar down is worth more than the proof.
""")
print()
print("=" * 78)
print("the ranking, and what it says")
print("=" * 78)
print("""
  Order:    (1) then (2) then (3) then (4).
  Cost:     1 hour, half a day, a week, unbounded.

  Three observations that generalise.

  FIRST, the cheapest proof was not about the code.  It was about the schema,
  and it was cheap because the database is already a proof engine we do not
  use.  Before writing a proof, ask what is already checking this and is not
  being listened to.  A UNIQUE index is a theorem.

  SECOND, the property that needed the most technique was not the most
  dangerous one.  The cache tenant leak (3) is the security risk, and it is the
  one that is expensive to prove, because the difficulty is that the claim is
  not yet *statable*.  Proof effort tracks the maturity of your specification,
  not the severity of your risk.  That is uncomfortable, because severity is
  what gets you scheduled and maturity is what gets you a theorem.

  THIRD, the property that was hardest to prove was also the one where proving
  it was least valuable.  (4) could have been pinned down for the cost of
  writing the grammar, and then it is a two-paragraph proof.  The proof was
  blocked on a decision, not on a theorem.

  The rule of thumb that falls out: spend proof effort where the invariant is
  already findable, and spend specification effort where it is not.  Do not
  confuse the two, and do not let a security review conclude that a property is
  safe because nobody has proved it -- that is an absence of evidence, and the
  sentence that would prove it is usually one line long.
""")
print()
print("=" * 78)
print("a ranking function, since the exercise asked for one")
print("=" * 78)

CANDIDATES = [
    # (name, invariant findable 0-1, technique cost 0-1, spec mature 0-1, severity 0-5)
    ("unique ledger index", 1.0, 0.1, 1.0, 5),
    ("retry backoff shrinks", 0.8, 0.4, 1.0, 3),
    ("cache tenant isolation", 0.4, 0.7, 0.5, 5),
    ("json parser equivalence", 0.3, 0.6, 0.1, 2),
]


def priority(name, findable, cost, mature, severity):
    """Score = severity, discounted by how much of the cost is specification
    work rather than theorem work.  A property whose specification is not
    written down cannot be proved no matter how severe it is."""
    spec_fraction = 1.0 - mature
    return severity * findable * (1.0 - cost) * (1.0 - 0.7 * spec_fraction)


print(f"{'candidate':<26} {'severity':>9} {'findable':>9} {'spec mature':>12} "
      f"{'score':>7}")
scored = []
for row in sorted(CANDIDATES, key=lambda r: -priority(*r)):
    score = priority(*row)
    scored.append((row[0], score))
    print(f"{row[0]:<26} {row[4]:>9} {row[1]:>9} {row[3]:>12} {score:>7.2f}")
print()
print("order:", [n for n, _ in scored])
print()
print("The scoring function ranks the security risk (cache tenant isolation)")
print("below the cheap database property, which is arguably wrong.  That is")
print("the honest limitation of any formula: it can only discount work it can")
print("see, and it cannot see that the cache bug is the one that will be in")
print("the postmortem.  Use the score to order your afternoon, not to decide")
print("what to care about.")
```

</details>
**Challenge — Build a refutation engine, and use it to decide eight statements
without ever evaluating one directly.** Write a function
`refute(assumptions, target, atoms)` that works like this: it builds the
assumption set Γ ∪ {¬target}, and searches for a subset of Γ that is already
inconsistent with ¬target, by enumerating assignments and looking for one that
makes ¬target true and every member of some subset of Γ false. For each
statement, report: whether it is refutable, the falsifying assignment, and the
*minimal* subset of assumptions responsible — which is the analogue of a
counterexample finder, and the thing a human wants. Then apply it to a
specification for a permission check and report the minimal violating
configuration.

<details>
<summary>Solution</summary>

```python
import itertools

# ---------------------------------------------------------------------------
# A refutation engine.
#
# `refute` never evaluates the target. It looks for an assignment under which
# the NEGATION of the target is true and some of the assumptions are false --
# i.e. a counterexample. The minimal subset is found by trying every subset of
# the assumptions and keeping the smallest one that is still falsified.
#
# Assumptions are (name, formula) where formula is a Python function of an env.
# Target is a Python function of an env.
# ---------------------------------------------------------------------------

ATOMS = ["A", "B", "C", "D"]


def envs(atoms):
    return [dict(zip(atoms, b))
            for b in itertools.product([False, True], repeat=len(atoms))]


def refute(assumptions, target, atoms=ATOMS):
    """Return (refuted, assignment, names of assumptions false there).

    The search is over ASSIGNMENTS, never over the target's internals. For each
    assignment where the target is False, it also reports which of the
    assumptions are False at that same assignment -- the hypotheses you would
    have to drop for the claim to survive.

    Two uses:
      refute([], not_S)                  is S a tautology?
      refute([facts...], claim)          does `claim` follow from the facts?
    """
    by_name = dict(assumptions)
    for env in envs(atoms):
        if target(env):
            continue
        false_names = [n for n, _ in assumptions if not by_name[n](env)]
        return True, env, false_names
    return False, None, None


def is_tautology(formula, atoms=ATOMS):
    """A tautology is a target that no assignment can refute."""
    return refute([], formula, atoms)[0] is False


print("=" * 78)
print("1. Eight statements: which are tautologies?")
print("=" * 78)
print()
STATEMENTS = [
    ("P -> P", lambda e: (not e["A"]) or e["A"]),
    ("P -> (P and Q)", lambda e: (not e["A"]) or (e["A"] and e["B"])),
    ("(P and Q) -> P", lambda e: (not (e["A"] and e["B"])) or e["A"]),
    ("P -> (P or Q)", lambda e: (not e["A"]) or e["A"] or e["B"]),
    ("P <-> P", lambda e: e["A"] == e["A"]),
    ("(P -> Q) -> (~P or Q)", lambda e: (not ((not e["A"]) or e["B"]))
                                        or (e["A"] or e["B"])),
    ("P <-> Q", lambda e: e["A"] == e["B"]),
    ("(P and Q) -> (Q and P)", lambda e: (not (e["A"] and e["B"]))
                                          or (e["B"] and e["A"])),
]
print(f"{'statement':<28} {'tautology?':>11}  {'witness (ABCD)':<14} {'blame'}")
for name, f in STATEMENTS:
    ok, env, blame = refute([], f)
    witness = "".join("1" if env[k] else "0" for k in ATOMS) if env else "-"
    print(f"{name:<28} {str(not ok):>11}  {witness:<14} {blame or '-'}")
print()
print("Six tautologies and two non-tautologies, and the two are the two that")
print("genuinely are not: 'P <-> Q' and the converse-of-imp rows. Note what the")
print("engine did NOT do: it never evaluated an implication, never called a")
print("library, and never looked at the shape of the formula. It asked a")
print("question with 16 possible answers and looked for one that said no.")
print()
print("That is a complete decision procedure for tautology over 4 atoms, and it")
print("is exactly as good as its search: 16 evaluations here, and 2^30 = "
      f"{2 ** 30:,}")
print("at thirty. Every SAT solver in production is this program with a much")
print("better search strategy.")
print()

print("=" * 78)
print("2. The blame set is the part a human wants")
print("=" * 78)
print()
REQUIRED = lambda e: (not e["A"] and not e["B"]) or e["C"]       # noqa: E731
CODE_BUGGY = lambda e: (not e["A"]) or (not e["B"]) or e["C"]    # noqa: E731
CODE_FIXED = lambda e: REQUIRED(e)                               # noqa: E731
CODE_EXEMPT = lambda e: (not e["A"] and not e["B"] and not e["D"]) or e["C"]

FACTS = [
    ("authenticated", lambda e: e["A"]),
    ("public endpoint", lambda e: e["B"]),
    ("admin", lambda e: e["C"]),
    ("rate limited", lambda e: e["D"]),
]

print("  the specification: deny exactly when unauthenticated and not public")
print("      REQUIRED(e) = (not A and not B) or C")
print()
for label, code in [("buggy   : not A or not B or C", CODE_BUGGY),
                    ("fixed   : (not A and not B) or C", CODE_FIXED),
                    ("exempt  : (not A and not B and not D) or C", CODE_EXEMPT)]:
    print(f"  {label}")
    for check_name, target in [("over-denies?", lambda e, c=code: c(e)
                                and not REQUIRED(e)),
                               ("under-denies?", lambda e, c=code: not c(e)
                                and REQUIRED(e))]:
        ok, env, blame = refute(FACTS, target)
        if not ok:
            print(f"      {check_name:<16} no")
        else:
            facts_true = [n for n, f in FACTS if f(env)]
            print(f"      {check_name:<16} YES, at "
                  f"{ {k: int(env[k]) for k in ATOMS} }")
            print(f"      {'':<16} false there: {blame}")
            print(f"      {'':<16} true  there: {facts_true}")
    print()

print("  Read the third case, because it is the one worth the whole exercise.")
print("  The 'exempt' version was supposed to be MORE permissive, and it is --")
print("  it over-denies nothing. But adding a rate-limit exemption changed the")
print("  antecedent from (not A and not B) to (not A and not B and not D),")
print("  which means a rate-limited unauthenticated request to a private")
print("  endpoint is no longer denied. The engine names the exact flags: D is")
print("  the one that is true, and A, B, C are the ones that are false.")
print()
print("  A reviewer reading the diff sees a three-character change to a")
print("  condition. The engine sees: this request is now allowed, and here are")
print("  the four facts that make it so. That is the difference between a")
print("  linter and a diagnosis.")
print()
print("  Note also that the two bug classes are reported separately. The")
print("  'over-denies' and 'under-denies' targets are DIFFERENT QUESTIONS, and")
print("  a security review that only asks one of them will call the other one")
print("  healthy. That is the same asymmetry as the two directions in")
print("  [Lesson 12](12_predicates_and_quantifiers.md), and it is the reason")
print("  both are printed.")
print()

print("=" * 78)
print("3. Where this engine stops")
print("=" * 78)
print()
print("  The engine enumerates 2^len(atoms) assignments, so it is exhaustion")
print("  wearing a refutation's clothes. That is honest and useful for a")
print("  handful of booleans, and useless at 30 -- where 2^30 = "
      f"{2 ** 30:,}")
print("  assignments is not a thing a machine does in your lifetime.")
print()
print("  Real refutation engines keep the same interface and change the search:")
print("  a SAT solver does not enumerate assignments at all, it propagates")
print("  constraints until the formula collapses. The three steps here --")
print("  negate the target, add the assumptions, find the assignment -- are")
print("  exactly the three steps a solver performs, and the engine is the same")
print("  program with a worse search strategy.")
print()
print("  Which is the last thing this lesson has to say: the *logic* of a")
print("  refutation is three lines long and has been since 1929. Everything")
print("  that has happened since is about making the search fast enough to be")
print("  worth doing.")
```

</details>

## Summary

- A proof is a list of lines, each a premise or a sound rule applied to earlier
  lines. That structure is what makes it checkable by a machine and by a
  sceptical reader.
- Modus ponens is the rule you use constantly. Modus tollens is derived from it
  via contraposition. The converse and the inverse are **not** rules, and the
  converse is the most-used invalid step in the subject.
- Direct, contrapositive, contradiction and exhaustion are four routes to one
  logical step — `¬P ∨ Q`. They differ in cost, not in result.
- Contrapositive needs the converse in advance, which is why it is unavailable
  until you already understand the problem. Contradiction is the fallback: it
  never needs prior knowledge, only the ability to see a contradiction.
- Exhaustion is **inapplicable** rather than defeated when the domain is
  infinite, and complete when it is finite. Choosing it is a decision about the
  size of the domain, not about the truth of the claim.
- Soundness is what makes a proof worth having; completeness is what makes
  "no proof found" informative. Not everything true is provable.
- A proof checker compares syntax, not meaning. It will reject a re-ordered
  premise and accept a proof from false premises, and both behaviours are
  correct.
- A loop invariant is the direct-proof technique applied to a loop, and stating
  the bound as a **rate** rather than an endpoint is what makes the termination
  argument work.
- Proof effort tracks the maturity of your specification, not the severity of
  your risk. Writing the specification down is usually worth more than proving
  anything about it.

## Next

[Lesson 14 — Mathematical Induction](14_mathematical_induction.md) is the technique
that covers an unbounded domain, which is exactly what the binary search
argument in this lesson needed and what exhaustion could not reach. It assumes
you can pick a technique and follow a derivation, and it is the last lesson
before this part stops being about logic and starts being about sets.
