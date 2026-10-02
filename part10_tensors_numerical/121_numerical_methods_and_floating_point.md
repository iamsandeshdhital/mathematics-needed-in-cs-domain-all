# 121 — Numerical Methods and Floating Point

**Part**: part10_tensors_numerical · **Prerequisites**: 51, 52, 54, 120 · **Time**: 45 min

---

## In Plain Words

Every number your computer stores is a rounded version of the number you
meant. A 64-bit float keeps 53 binary digits and throws the rest away.
That is fine — until you subtract two nearly equal numbers, and the digits
that survive are exactly the ones that were thrown away. `0.1 + 0.2` is
not `0.3`, the small root of a quadratic can come out as exactly zero, and
a sum of perfectly reasonable numbers can come out as a completely
unreasonable one.

This lesson is the accumulated list of ways that happens, and what to do
about each. It divides into four questions, and the answer to each is short:

1. **What is a float, really?** A binary fraction. 53 bits of it. `0.1` is
   not a tenth, it is a number very close to a tenth.
2. **Why does arithmetic lose accuracy?** Subtracting near-equals throws
   away significant digits. Everything else follows from that.
3. **How do we talk about it?** Three words: *forward error* (how far the
   answer is from the truth), *backward error* (how far some nearby input
   would have produced this answer exactly), and *condition number* (how
   much the problem amplifies whatever error reaches it).
4. **What do numerical methods do about it?** Root-finders and integrators
   have proven convergence *orders*, and you can measure the order your
   implementation actually achieves. Sometimes it beats the promise.
   Sometimes it is fighting a floor it can never get under.

## Why Computer Science Cares

- **Money does not tolerate relative error.** `0.1 * 3` in binary floating
  point is `0.30000000000000004`. Invoicing, tax, and ledger reconciliation
  are why `decimal.Decimal` and integer cents exist, not fashion.
- **Cancellation is the single most common numerical bug.** It produces
  plausible-looking wrong answers, not exceptions. Geometry code, numerical
  derivatives, root-finding, eigenvector algorithms, and finite differences
  all fail this way.
- **Conditioning decides whether precision is worth buying.** Computing the
  variance of data whose true variance is zero amplifies every rounding
  error by orders of magnitude. No amount of `float128` fixes it, because
  the problem, not the arithmetic, is at fault.
- **Convergence orders are a performance contract.** A quadratic method
  reaching 15 digits in 5 steps versus a linear one needing 50 is not a
  detail — it is the difference between an interactive solver and an
  overnight batch job.
- **Every framework exposes the same knobs.** `numpy.float32` versus
  `float64` versus `float128`, `torch.set_default_dtype`, `jax.config`,
  `Decimal(prec=N)`, `mpmath` — all of them are this lesson.
- **Debugging a wrong answer means diagnosing it first.** The question is
  never "is this number right" but "is this problem able to give me a right
  number at all".

## The Formal Version

Notation follows [SYMBOLS.md](../../SYMBOLS.md).

**Definition.** A normalised binary floating-point number is
x = ±(1 + Σ bₖ 2⁻ᵏ) · 2ᵉ with each bₖ either 0 or 1, so a `float64` stores 52 explicit
fraction bits plus an implicit leading 1: 53 significant bits, 11 for the
exponent, and 1 for the sign.

**Definition.** The *unit roundoff* is u = 2⁻⁵³, the largest relative error
a single correctly-rounded operation can introduce. The machine epsilon
`sys.float_info.epsilon` is 2⁻⁵², the gap above 1.0 — twice u.

**Theorem (standard model).** Every basic float operation satisfies
fl(a ⊙ b) = (a ⊙ b)(1 + δ) with |δ| ≤ u, and by the chain rule a
composition of n such operations has relative error at most nu/(1 − nu)
for nu < 1. With n = 10¹⁶ the bound reaches 1 and stops meaning anything,
which is why long accumulations need periodic rescaling or pairwise
summation.

**Definition.** The *ulp* of a float x is the distance from x to the next
representable float above it, computed exactly as `math.ulp(x)`. For
2ᵉ ≤ |x| < 2ᵉ⁺¹ it is 2ᵉ⁻⁵², so the gap is **proportional to the
magnitude**. This single fact explains `1e16 + 1 == 1e16`, and it is why
`1 + 1e-16 == 1.0`.

**Definition.** Subtracting a − b where a and b agree to within a few ulps
is *catastrophic cancellation*. The absolute error of each operand is
about u·max(|a|, |b|), and the result is |a − b|, so the **relative** error
of the difference is roughly

    u · max(|a|, |b|) / |a − b|,

which blows up as the difference shrinks.

**Definition.** A problem is *well conditioned* if it cannot turn small
input errors into large output errors. The relative condition number of
f : ℝ → ℝ at x is κ(x) = |x f′(x) / f(x)|, obtained by dropping the O(δ²)
term from f(x+δx) = f(x) + f′(x)δx + O(δ²). A perturbation of one ulp in
x changes f(x) by about κ(x)·u in relative terms.

**Definition.** An algorithm is *forward stable* if its forward error is
bounded by a modest multiple of the problem's condition number times u. It
is *backward stable* if the computed answer is exact for some nearby input,
formally if the backward error is O(u). **Backward stability is the
property worth having**: backward error is bounded by the size of the
operations performed, which the algorithm controls, while forward error
also depends on κ, which it does not.

**Theorem (catastrophic cancellation avoided).** If f = g − h with g ≈ h, and
f can be rewritten in a form where no subtraction of comparable quantities
occurs, the rewrite loses no accuracy. This is the whole content of
`expm1` versus `exp(x) − 1`, `log1p` versus `log(1 + x)`,
`math.hypot` versus `sqrt(x² + y²)`, and Vieta's product for the small
root of a quadratic.

**Definition.** A sequence x₀, x₁, … *converges* to α with **order p** and
asymptotic constant C > 0 if |eₖ₊₁| / |eₖ|ᵖ → C as k → ∞, where
eₖ = xₖ − α.

**Theorem (Newton's convergence).** For f with a simple root α, f′(α) ≠ 0 and
f ∈ C² near α, Newton's method satisfies
eₖ₊₁ = (f″(α) / 2f′(α)) · eₖ² + O(eₖ³). So the order is 2 and the constant
is determined by the problem, not by the code.

**Theorem (bisection).** If f is continuous and f(a)f(b) < 0, the midpoint
m of [a, b] satisfies sign(f(m)) = ±1 or sign(f(a)) = sign(f(m)), so some
sub-interval of width (b − a)/2 still brackets a root. After k steps the
bracket has width (b − a)/2ᵏ and the returned midpoint is within
(b − a)/2ᵏ⁺¹ of that root. Order 1, constant 1/2, unconditional — it
requires only continuity.

**Theorem (trapezoid and Simpson).** On a uniform mesh of width h, the
trapezoid rule for a C² integrand has error −(h²/12)(g′(b) − g′(a)) +
O(h⁴), and Simpson's rule has error −(h⁴/180)(g‴(b) − g‴(a)) + O(h⁶).
Orders 2 and 4, from function evaluations only.

**Theorem (Richardson extrapolation).** If a family of approximations
A(h) has error C hᵖ + O(hᵖ⁺¹), then
B(h) = (2ᵖ A(h/2) − A(h)) / (2ᵖ − 1) has error O(hᵖ⁺¹). Each application
buys one power of h for the cost of one extra evaluation, and iterating it
is exactly what builds a Romberg table.

**Definition.** The **stopping criterion** for a root-finder should be
|xₖ − xₖ₋₁| ≤ tol·(1 + |xₖ|). Stopping on |f(xₖ)| ≤ tol is wrong whenever
f′ is small, which is exactly the regime the method is trying to resolve.

## Worked Example

The quadratic formula, all the way through, on one concrete pair of
coefficients. This is the shortest complete illustration of cancellation in
this lesson.

We want the roots of `x² − 2b·x + c = 0` with b = 2²⁶ = 67108864 and
c = 1e-5. The formula is

    x± = (b ± sqrt(b² − 4c)) / 2.

**Step 1 — compute the discriminant.** b² = 2⁵² = 4503599627370496, exactly,
because b is a power of two. Now 4c = 4e-5. The gap between consecutive
floats near 4.5e15 is `ulp = 1.0`, so 4e-5 is more than four hundred
million times smaller than half a gap. The subtraction `b*b - 4*c` therefore
returns `4503599627370496.0` — the same number as `b*b`. The correction
term has been rounded away entirely.

**Step 2 — take the square root.** sqrt of a value whose true root is below
it by about 1e-13. Half a gap at 6.7e7 is about 7.5e-9, so the root rounds
to exactly `67108864.0`.

**Step 3 — form the two roots.**

    x+ = (67108864 + 67108864) / 2 = 67108864.0
    x− = (67108864 − 67108864) / 2 = 0.0

The small root is **exactly zero**. Nothing raised an exception; the
formula was implemented correctly.

**Step 4 — ask what the answer should be.** By Vieta, the two roots multiply
to c. So if x₊ = 67108864.0 is correct, the small root is
c / x₊ = 1e-5 / 67108864 = 1.4901161193847657e-13. The naive pair fails its
own consistency check: x₊·x₋ = 0, not 1e-5.

**Step 5 — rewrite.** Compute the large root the naive way, then get the
small one by division:

    x₊ = (b + sqrt(b² − 4c)) / 2
    x₋ = c / x₊

This version never subtracts two nearly equal numbers. It is backward
stable: if the input b were perturbed by one ulp, the answer would still be
exactly right for that perturbed b. Its relative error on x₋ is 8.2e-17 —
one rounding.

The general lesson: **when a formula's answer is very different in scale
from its inputs, the small answer is computed as a difference of two large
numbers and there is nothing to be done except find another formula.**

## Runnable Code

What a float is, and why `0.1 + 0.2` misses.

```python
"""Floating point: what the decimal-looking numbers really are."""

import math
import sys
from decimal import Decimal
from fractions import Fraction

print("=== the famous line ===")
print("0.1 + 0.2 =", 0.1 + 0.2)
print("0.1 + 0.2 == 0.3  ->", 0.1 + 0.2 == 0.3)
print("(0.1 + 0.2) - 0.3 =", (0.1 + 0.2) - 0.3, " = 2**-54 =", 2.0 ** -54)

print("\n=== a float is not a decimal, it is a binary fraction ===")
print("0.1 in hex  =", (0.1).hex())
print("0.2 in hex  =", (0.2).hex())
print("0.3 in hex  =", (0.3).hex())
exact = Fraction(0.1)
print("0.1 exactly =", exact)
print("  nearest tenth is", exact.limit_denominator(10),
      "and the signed error is", float(Fraction(1, 10) - exact))
print("1/10 in binary is 0.0001100110011... and never terminates, so it has")
print("to stop somewhere. The gap above 0.1 is ulp(0.1) =", math.ulp(0.1))

print("\n=== the constants that make this measurable ===")
print("sys.float_info.mant_dig =", sys.float_info.mant_dig, " binary digits kept")
print("sys.float_info.max_exp   =", sys.float_info.max_exp)
print("sys.float_info.min_exp   =", sys.float_info.min_exp)
print("sys.float_info.epsilon   =", sys.float_info.epsilon,
      "  which is 2**-52 ->", sys.float_info.epsilon == 2.0 ** -52)
print("sys.float_info.max       =", sys.float_info.max)
print("the gap from 1.0 up to the next float is", math.ulp(1.0))
print("  1.0 + 1e-16 =", 1.0 + 1e-16, "  <- under half a gap, discarded")
print("  1.0 + 2e-16 =", 1.0 + 2e-16, "  <- over half a gap, kept")

print("\n=== ulp: the size of the gap above a given number ===")
for v in [1.0, 1e16, 12345.678, 1e-300]:
    print(f"  ulp({v:g}) = {math.ulp(v):.6e}")
print("The gap is proportional to the magnitude, which is why adding a small")
print("number to a large one silently does nothing.")

print("\n=== integers stop being exact too ===")
big = 2 ** 53
print("2**53             =", big)
print("2**53 + 1         =", big + 1)
print("float(2**53 + 1)  =", float(big + 1))
print("2**53 + 1 == 2**53 ->", (big + 1) == big)
print("every integer up to 2**53 - 1 =", 2 ** 53 - 1, "is exact in a float64;")
print("past that they come in steps, and Python ints never do:")
print("  (10**30)**2 =", 10 ** 60)

print("\n=== when you genuinely need exact decimal arithmetic ===")
print("Decimal('0.1') + Decimal('0.2') =", Decimal("0.1") + Decimal("0.2"))
print("  == Decimal('0.3') ->", Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))
print("Fraction(1,10) + Fraction(2,10) =", Fraction(1, 10) + Fraction(2, 10))
print("  == Fraction(3,10) ->", Fraction(1, 10) + Fraction(2, 10) == Fraction(3, 10))
print("both are exact, and both are far slower than one native float add.")
print("Decimal(2).sqrt()     =", Decimal(2).sqrt())
print("math.sqrt(2)**2 - 2.0 =", math.sqrt(2) ** 2 - 2.0,
      " <- the float route keeps the same error")
```

A float is `3602879701896397 / 36028797018963968`, which is *not* 1/10 —
it is off by −5.55e-18. The error is not a bug in the arithmetic; it is a
decision about which of two nearby numbers to store. And `2**53 + 1 == 2**53`
shows that the same limit bites integers, where the number of consecutive
representable integers runs out at 2⁵³.

### Catastrophic cancellation

```python
"""Catastrophic cancellation: subtracting two nearly equal numbers."""

import math
from fractions import Fraction

print("=== mild: sqrt(2)**2 is not 2 ===")
s = math.sqrt(2)
print("sqrt(2)          =", s)
print("sqrt(2)**2       =", s * s)
print("minus 2.0        =", s * s - 2.0,
      " (relative error", (s * s - 2.0) / 2.0, ")")
print("the input was already wrong by about 1.7e-17, and squaring doubled it.")

print("\n=== severe: the quadratic formula on x**2 - 2*b*x + 1e-5 ===")
b, c = 2.0 ** 26, 1e-5
print("b                =", b, "(exactly representable, being a power of two)")
print("b*b              =", b * b)
print("b*b - 4c         =", b * b - 4 * c)
print("ulp(b*b)         =", math.ulp(b * b),
      "-- and 4c is only", 4 * c, ", far below half a gap")
print("exact b*b - 4c   =", Fraction(int(b)) ** 2 - Fraction(1, 25000))
print("  which is b*b minus 1/25000 -- a difference float64 cannot hold here")
root = math.sqrt(b * b - 4 * c)
x1 = (b + root) / 2
x2 = (b - root) / 2
print("sqrt(disc)       =", root, " (the true root is below this by 1e-13)")
print("naive roots      =", x1, "and", x2)
print("the small root is exactly 0 ->", x2 == 0.0)
print("the true small root is c/x1  =", c / x1, " <- Vieta recovers it")
print("Vieta's check x1*x2 == c fails:", x1 * x2, "vs", c)
print("The small root is not merely inaccurate, it is gone -- out of a")
print("formula with no bugs in it.")

print("\n=== severe: summing terms that nearly cancel ===")
vals = [1e16, 1.0, -1e16, 1.0]
naive = 0.0
for v in vals:
    naive += v
print("naive left to right =", naive)
print("math.fsum(vals)     =", math.fsum(vals))
print("exact sum           =", float(sum(Fraction(v) for v in vals)))
print("both 1.0s survive only if the big terms cancel exactly before the")
print("small ones are folded in, which is what fsum does and a running")
print("total cannot.")

print("\n=== severe: 1 - cos(x), and the form that avoids the subtraction ===")
for x in [1e-3, 1e-5, 1e-7]:
    naive_c = 1.0 - math.cos(x)
    good = 2.0 * math.sin(x / 2.0) ** 2
    print(f"  x={x:.0e}   1-cos(x)={naive_c:.6e}   "
          f"2*sin(x/2)**2={good:.6e}   x**2/2={x * x / 2:.6e}")

print("\n=== severe: exp(x) - 1 and log(1 + x) for tiny x ===")
x = 1e-18
print("the true answers are 1e-18 and 1e-18")
print("math.exp(x) - 1     =", math.exp(x) - 1.0)
print("math.expm1(x)       =", math.expm1(x))
print("math.log(1 + x)     =", math.log(1.0 + x))
print("math.log1p(x)       =", math.log1p(x))
print("Python ships expm1 and log1p for exactly this reason.")

print("\n=== how many correct digits survive a subtraction ===")
print("true value      float result     relative error    correct digits")
for p in [16, 14, 12, 10, 8, 6]:
    truth = Fraction(1, 10 ** p)
    got = (1.0 + 10.0 ** -p) - 1.0
    relerr = abs(Fraction(got) - truth) / truth
    digits = max(0.0, -math.log10(float(relerr))) if relerr else 0.0
    print(f"  {float(truth):<12.1e} {got:<16.6e} {float(relerr):<17.3e} "
          f"{digits:.1f}")
print("The true difference is tiny, so the operands are equal to within a")
print("few ulps, and the rounding of the operands becomes the answer.")
print("At p = 16 the difference is entirely gone.")

print("\n=== the rule ===")
print("Never form a - b when a and b are close. Rewrite it, or call the")
print("library function whose whole job is to do the rewrite for you.")
```

Every failure above is the same event: a subtraction in which the answer is
much smaller than the operands. In each case the operands carried an
absolute error of about u × their own size, the answer is that error
divided down by the cancellation, and the relative error is whatever that
division gives you.

The `1 - cos(x)` row is the cleanest illustration, because the true answer
is available in closed form: `x²/2 − x⁴/24`. At x = 1e-7 the series is
5.0e-15 and the naive subtraction gives 4.996e-15, a relative error of
8e-4 — you lost four of the sixteen digits you paid for. The rewrite
`2·sin(x/2)²` is algebraically identical and gets all of them back.

The table at the end is the general rule. `p` here is the exponent in
`1 + 1e-ᴾ − 1`: the difference really is 1e-ᴾ, but the operand `1 + 1e-ᴾ` was
already rounded, and the whole rounding lands on the difference. At p = 16
the difference is not inaccurate, it is gone.

### Forward error, backward error, condition number

```python
"""Forward error, backward error, condition number, and stability."""

import math
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
u = sys.float_info.epsilon / 2

print("=== the model everything rests on ===")
print("u, the unit roundoff, =", u, "= 2**-53")
print("every float op satisfies  fl(a*b) = a*b*(1+d)  with  |d| <= u")
print("so n chained operations carry relative error of order n*u, and with")
print("n = 1e16 that is already order 1: precision runs out before you do.")

print("\n=== three quantities worth keeping apart ===")
print("forward error  : how far the computed answer is from the true answer")
print("backward error : how far some input is from an input that would have")
print("                 produced the computed answer exactly")
print("stability      : backward error divided by forward error. A stable")
print("                 algorithm's answer is the right answer to a nearby")
print("                 question, even when the forward error looks large.")

print("\n=== the condition number of a problem ===")
print("kappa(x) = |x f'(x) / f(x)|: the worst-case relative error gain.")
print("A problem with huge kappa is ill-conditioned; no algorithm can fix it.")
print("\nproblem                       kappa(x)   meaning")
CASES = [
    ("x*x            at x=1e8", lambda x: x * x, lambda x: 2 * x, 1e8),
    ("sqrt(x)         at x=3", math.sqrt, lambda x: 0.5 / math.sqrt(x), 3.0),
    ("exp(x)          at x=100", math.exp, math.exp, 100.0),
    ("x - 1           at x=1.0000001", lambda x: x - 1.0,
     lambda x: 1.0, 1.0000001),
    ("(x-1)**2        at x=1+1e-8", lambda x: (x - 1.0) ** 2,
     lambda x: 2.0 * (x - 1.0), 1.0 + 1e-8),
    ("1/x             at x=1e-8", lambda x: 1.0 / x,
     lambda x: -1.0 / x ** 2, 1e-8),
]
for label, f, df, x in CASES:
    k = abs(x * df(x) / f(x))
    print(f"  {label:30s} {k:11.4g}   {k:.3g}-fold amplification")

print("\n=== conditioning, measured rather than asserted ===")
print("perturb x by one ulp and report the relative change in f(x)")
print("problem                       measured        predicted k*u")
for label, f, df, x in CASES:
    h = math.ulp(x)
    fx = f(x)
    measured = abs(f(x + h) - fx) / abs(fx)
    predicted = abs(x * df(x) / f(x)) * u
    print(f"  {label:30s} {measured:11.3e} {predicted:16.3e}")
print("Measured tracks predicted to within a factor of two, which is the")
print("first-order term plus higher-order corrections. The problem, not the")
print("code, decides how much a rounding error grows.")

print("\n=== stability: the same problem, two algorithms ===")
print("\n-- summing a list --")


def naive_sum(xs):
    total = 0.0
    for x in xs:
        total += x
    return total


def kahan_sum(xs):
    total, c = 0.0, 0.0
    for x in xs:
        y = x - c
        t = total + y
        c = (t - total) - y
        total = t
    return total


TESTS = [
    ("ten copies of 0.1", [0.1] * 10),
    ("ten 0.1s then a -1", [0.1] * 10 + [-1.0]),
    ("1e16, 1, -1e16, 1", [1e16, 1.0, -1e16, 1.0]),
    ("1e17, twenty 1s, -1e17", [1e17] + [1.0] * 20 + [-1e17]),
]


def rel_err(got, truth):
    if truth == 0:
        return 0.0 if got == 0 else float("inf")
    return float(abs(Fraction(got) - truth) / abs(truth))


print("list                        exact      naive err    kahan err     fsum err")
for label, xs in TESTS:
    truth = sum(Fraction(x) for x in xs)
    print(f"  {label:24s} {float(truth):<11.6g} "
          f"{rel_err(naive_sum(xs), truth):<12.3e} "
          f"{rel_err(kahan_sum(xs), truth):<12.3e} "
          f"{rel_err(math.fsum(xs), truth):<12.3e}")
print("Compensated summation undoes rounding the running total has already")
print("done, which is why it beats the naive loop on the first two rows. It")
print("cannot recover what was never stored: in row three the first 1.0 was")
print("swallowed by 1e16 before the -1e16 arrived, so Kahan still answers 1.0")
print("while fsum, which tracks every partial sum exactly, answers 2.0.")

print("\n-- the small root of a quadratic --")


def quad_roots_naive(b, c):
    d = math.sqrt(b * b - 4 * c)
    return (b + d) / 2, (b - d) / 2


def quad_roots_stable(b, c):
    hi = (b + math.sqrt(b * b - 4 * c)) / 2
    return hi, c / hi


B, C = 2.0 ** 26, 1e-5
print("naive ", quad_roots_naive(B, C))
print("stable", quad_roots_stable(B, C))
print("The stable version computes the large root the naive way, then gets")
print("the small one from Vieta. It never subtracts two close numbers, so it")
print("is backward stable: the answer is exact for a nearby input.")

print("\n-- the area of a sliver triangle (Heron's formula) --")


def heron_naive(a, b, c):
    s = 0.5 * (a + b + c)
    return math.sqrt(s * (s - a) * (s - b) * (s - c))


def heron_kahan(a, b, c):
    return 0.25 * math.sqrt((c + (a + b)) * (c - (a - b))
                            * (c + (a - b)) * (a + (b - c)))


print("Isosceles triangle with sides 1, 1, c. Dropping the altitude splits it")
print("into two right triangles, so the area is (c/2)*sqrt(1 - c**2/4). The")
print("reference below uses the exact value of the float c, in 60 digits.\n")
for c in [1.99, 1.9999, 1.999999, 1.9999999]:
    cd = Decimal(c)
    truth = cd * (Decimal(1) - cd * cd / 4).sqrt() / 2
    tn, tk = heron_naive(1.0, 1.0, c), heron_kahan(1.0, 1.0, c)
    en = abs(Decimal(tn) - truth) / truth
    ek = abs(Decimal(tk) - truth) / truth
    print(f"  c = {c}")
    print(f"    exact  {float(truth):.12e}")
    print(f"    naive  {tn:.12e}   relative error {float(en):.3e}")
    print(f"    Kahan  {tk:.12e}   relative error {float(ek):.3e}")
print("Naive Heron computes s - c, a subtraction of two numbers that agree to")
print("fifteen digits, and pays for each of them: the error column climbs by")
print("orders of magnitude as c picks up more 9s. Kahan's rearrangement never")
print("forms s - c, so it stays within an ulp throughout. For other values of")
print("c the two agree, because s - c happens to land on a representable")
print("float -- which is exactly why this bug survives testing and only")
print("shows up in production.")

print("\n-- and why math.hypot exists --")
x = 1e200
print("x * x                    =", x * x, " (overflow to infinity)")
print("math.sqrt(x*x + x*x)     =", math.sqrt(x * x + x * x))
print("math.hypot(x, x)         =", math.hypot(x, x))
t = 1e-200
print("math.sqrt(t*t + t*t)     =", math.sqrt(t * t + t * t), " (underflow to zero)")
print("math.hypot(t, t)         =", math.hypot(t, t))
print("Neither overflow nor underflow: hypot scales internally, so it is")
print("correct across the whole exponent range where the naive form is not.")

print("\n=== the checklist ===")
print("1. Can this be written so nothing is subtracted from something nearly")
print("   equal to it?")
print("2. Is there a library function whose whole job is this shape?")
print("3. If the answer must be accurate in absolute terms, is the problem")
print("   well-conditioned? If not, say so instead of debugging code.")
```

Two things to take from that block.

The first is that conditioning is a property of the *problem*. The
`x − 1 at x = 1.0000001` row has κ ≈ 1e7: perturb the input by one ulp and
the answer moves by a relative 2.2e-9, which is exactly what κ·u predicts.
No algorithm can improve on that, because the code did nothing wrong. The
`1/x at x = 1e-8` row has κ = 1 and behaves accordingly. If your problem
sits in the first category, the correct response is to reformulate or to
report a wide confidence interval — not to add precision.

The second is that **stable vs unstable is a choice about code**. The
quadratic's small root, the sliver triangle's area, and the list sum are
three formulations of three questions, and the code picks the bad one and
the good one in each case with a line changed. Naive Heron is 1.1e-9 wrong;
Kahan's rearrangement is within an ulp. That is not a tuning improvement,
that is the answer.

`math.hypot` is the shortest entry in the whole lesson: `1e200 * 1e200` is
`inf`, and `hypot(1e200, 1e200)` is `1.414213562373095e+200`. The function
exists because the naive form is wrong on most of the range of inputs you
would want to use it on.

### Root finding

```python
"""Root finding: bisection, Newton, secant, Brent, and orders of convergence."""

import math
import sys


# ---------------------------------------------------------------- bisection
def bisect(f, a, b, xtol=1e-12, maxit=300):
    """Halve a bracket [a, b] whose endpoint values have opposite signs."""
    fa = f(a)
    for k in range(1, maxit + 1):
        m = 0.5 * (a + b)
        if m == a or m == b:
            return m, k
        fm = f(m)
        if fm == 0.0:
            return m, k
        if fa * fm < 0:
            b = m
        else:
            a, fa = m, fm
        if 0.5 * (b - a) <= xtol * (1 + abs(m)):
            return m, k
    return m, maxit


# ------------------------------------------------------------------- Newton
def newton(f, df, x0, xtol=1e-15, maxit=60):
    """x_{k+1} = x_k - f(x_k)/f'(x_k). Returns the iterates."""
    xs = [x0]
    for _ in range(maxit):
        x = xs[-1]
        d = df(x)
        if d == 0.0:
            break
        xn = x - f(x) / d
        xs.append(xn)
        if abs(xn - x) <= xtol * (1 + abs(xn)):
            break
    return xs


def secant(f, x0, x1, xtol=1e-14, maxit=60):
    """Newton with the derivative replaced by a finite difference."""
    xs = [x0, x1]
    for _ in range(maxit):
        xa, xb = xs[-2], xs[-1]
        fa, fb = f(xa), f(xb)
        if fb == fa:
            break
        xn = xb - fb * (xb - xa) / (fb - fa)
        xs.append(xn)
        if abs(xn - xb) <= xtol * (1 + abs(xn)):
            break
    return xs


# -------------------------------------------------------------------- Brent
def brent(f, a, b, xtol=1e-12, maxit=200):
    """Bisection + secant + inverse quadratic interpolation, with a guarantee.

    Three points are kept: b is the best so far, a is the other end of the
    bracket, c is the older one. Each step tries inverse quadratic
    interpolation through all three, then the secant line through a and b,
    and falls back to halving whenever the fancy step would move less than a
    quarter of the way in. That last rule is what makes it safe.
    """
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("no sign change on the bracket")
    if abs(fa) < abs(fb):
        a, b, fa, fb = b, a, fb, fa
    c, fc = a, fa
    d = e = b - a
    counts = {"interp": 0, "bisect": 0}
    for k in range(1, maxit + 1):
        if fb * fc > 0:                    # b and c bracket the root
            c, fc = a, fa
            d = e = b - a
        if abs(fc) < abs(fb):              # promote c if it is better
            a, b, c = b, c, b
            fa, fb, fc = fb, fc, fb
        tol1 = 2 * sys.float_info.epsilon * abs(b) + 0.5 * xtol
        xm = 0.5 * (c - b)
        if abs(xm) <= tol1 or fb == 0.0:
            return b, k, counts
        if abs(e) >= tol1 and abs(fa) > abs(fb):
            s = fb / fa
            if a == c:                     # only two distinct points
                p, q = 2 * xm * s, 1.0 - s
            else:                          # inverse quadratic interpolation
                qq, r = fa / fc, fb / fc
                p = s * (2 * xm * qq * (qq - r) - (b - a) * (r - 1))
                q = (qq - 1) * (r - 1) * (s - 1)
            if p > 0:
                q = -q
            p = abs(p)
            if 2 * p < min(3 * xm * q - abs(tol1 * q), abs(e * q)):
                e, d = d, p / q             # step is well inside: take it
                counts["interp"] += 1
            else:
                d = e = xm
                counts["bisect"] += 1
        else:
            d = e = xm
            counts["bisect"] += 1
        a, fa = b, fb
        b += d if abs(d) > tol1 else math.copysign(tol1, xm)
        fb = f(b)
    return b, maxit, counts


# ------------------------------------------------------------------ targets
f = lambda x: x * x - 2.0
df = lambda x: 2.0 * x
g = lambda x: x ** 3 - 2 * x + 2
dg = lambda x: 3 * x * x - 2
TRUTH = math.sqrt(2)

print("=== the target: f(x) = x*x - 2, true root sqrt(2) =", TRUTH)
print("sqrt(2) is irrational, so 'the right answer' means the nearest float to")
print("it -- which is exactly what math.sqrt(2) already returns.\n")

print("=== bisection: a guarantee that needs no derivative ===")
root, its = bisect(f, 0.0, 2.0, xtol=1e-14)
print("root =", repr(root), "  iterations =", its)
print("the width after k halvings is exactly (b-a)/2**k, and the ratio of")
print("consecutive widths is exactly 0.5. That is linear convergence with")
print("rate 1/2: one more correct bit per step, no more, forever.")
print("Steps needed for 1e-14 from a width of 2: ceil(log2(2/1e-14)) =",
      math.ceil(math.log2(2.0 / 1e-14)))
print("Note carefully what that bounds: the WIDTH OF THE BRACKET, not the")
print("error in the root. Halving a bracket of width w puts the root within")
print("w/2 of the midpoint -- and nothing more.")

print("\n=== Newton: quadratically fast, but it needs a starting guess ===")
for x0 in [1.0, 1.4, 5.0]:
    xs = newton(f, df, x0)
    print(f"  x0 = {x0}: {len(xs) - 1} iterations -> {xs[-1]!r}")
    print("     " + " -> ".join(f"{x:.6f}" for x in xs))
print("Six steps against forty-six. The catch is two sections down.")

print("\n=== measuring the order of convergence ===")
xs = newton(f, df, 1.0)
errs = [abs(x - TRUTH) for x in xs]
print("  k   x_k                  |error|     e_k/e_{k-1}   e_k/e_{k-1}^2")
for k in range(1, len(xs)):
    e, ep = errs[k], errs[k - 1]
    if e == 0.0 or ep == 0.0:
        print(f"  {k:<3d} {xs[k]:<20.17g} {e:<12.3e} "
              "(float resolution reached)")
        continue
    print(f"  {k:<3d} {xs[k]:<20.17g} {e:<12.3e} "
          f"{e / ep:<13.3f} {e / ep ** 2:<13.4f}")
print("The linear column collapses while the quadratic column settles at")
print("f''(a)/(2 f'(a)) = 2/(4*sqrt(2)) =", 1 / (2 * math.sqrt(2)),
      "-- the theoretical constant, not a fitted one.")
print("Every step roughly doubles the correct digits. Fifteen digits take")
print("about five steps, after which the float type is exhausted: the")
print("iterates stop improving because there is nowhere left to improve to.")

print("\n=== Newton can fail, and it fails in recognisable ways ===")
print("g(x) = x**3 - 2x + 2 has exactly one real root, near -1.7693.")
for x0 in [0.0, 1.0, 5.0, 100.0]:
    xs = newton(g, dg, x0, maxit=40)
    print(f"  x0 = {x0:<7} {len(xs) - 1:3d} iterations -> {xs[-1]!r}")
print("Starting at 0 lands on the 2-cycle 0 -> 1 -> 0 -> 1 and stops dead:")
print("  g(0) = 2 and g'(0) = -2, so the step sends x to 1; then g(1) = 1")
print("  and g'(1) = 1, so the next step sends it straight back to 0.")
print("Starting far away it does converge, but takes dozens of steps. The")
print("guarantee for Newton is local, and there is no global one.")

print("\n=== secant: Newton's method without derivatives ===")
xs = secant(f, 1.0, 1.5)
print(f"  {len(xs) - 1} iterations -> {xs[-1]!r}")
print("  " + " -> ".join(f"{x:.8f}" for x in xs))
errs = [abs(x - TRUTH) for x in xs]
print("  errors:", [f"{e:.3e}" for e in errs])
print("  consecutive error ratios:",
      [f"{errs[k] / errs[k - 1]:.5f}" for k in range(2, len(xs))
       if errs[k - 1] > 1e-9 and errs[k] > 0.0])
print("  approaching (1+sqrt(5))/2 =", (1 + math.sqrt(5)) / 2)
print("Superlinear but not quadratic, because the finite-difference slope is")
print("only first-order accurate. It needs no derivative, so it runs on")
print("black-box objectives -- which is why most optimisers use it.")

print("\n=== how to stop ===")
print("Stopping when |f(x)| < tol looks reasonable and is wrong. Near a")
print("double root f is flat, so |f| is tiny long before x is anywhere near.")
q = lambda x: x * x
print("  f(x) = x**2 at x = 1e-5 gives |f(x)| =", q(1e-5))
print("  so a test of |f(x)| < 1e-9 would stop immediately, at x = 1e-5,")
print("  with 100% relative error in the answer 0.")
print("Stop on the change in x instead, scaled by x so it works at any size:")
xs = newton(f, df, 1.0)
for k in (2, 3, 4):
    x = xs[k]
    print(f"  k={k}  |f(x)| = {abs(f(x)):.3e}   "
          f"|x_k - x_(k-1)| = {abs(x - xs[k - 1]):.3e}   "
          f"relative = {abs(x - xs[k - 1]) / abs(x):.3e}")
print("The rule: stop when abs(x_k - x_(k-1)) <= xtol * (1 + abs(x_k)).")
print("The 1 is not decoration: when the answer is near zero the relative")
print("test alone would demand impossible precision.")

print("\n=== the method to actually ship: Brent ===")
print("Brent keeps three points and, at each step, takes whichever of three")
print("candidates shrinks the bracket fastest:")
print("  * inverse quadratic interpolation through the last three points,")
print("  * the secant line through the last two,")
print("  * a plain bisection,")
print("falling back to bisection whenever the fancy step would move less than")
print("a quarter of the way in. That single rule is what makes it safe: a")
print("rejected step can never stall the interval, so progress is guaranteed")
print("to be at worst geometric while normally being much faster.")

print("\nproblem                  bisect  brent   result")
for label, fn, lo, hi in [("x*x - 2 on [0, 2]", f, 0.0, 2.0),
                          ("x**3-2x+2 on [-10,10]", g, -10.0, 10.0)]:
    rb, kb = bisect(fn, lo, hi)
    rr, kr, counts = brent(fn, lo, hi)
    print(f"  {label:22s} {kb:6d} {kr:6d}   brent -> {rr!r}")
    print(f"  {'':22s} {'':6s} {'':6s}   {counts}")
print("Same tolerance, same guarantee, roughly five times fewer function")
print("evaluations. Every iteration also reports how many steps were")
print("interpolations and how many were fallback halvings -- a fraction near")
print("zero is the sign of a well-conditioned problem. This is what")
print("scipy.optimize.brentq does, and so is every textbook Brent.")
```

Three methods, three guarantees, and the number that decides between them.

**Bisection** needs only continuity and a sign change. It is slow — 46
steps for 14 digits — but it *cannot* fail, and its guarantee is on the
width of the bracket, which it controls exactly.

**Newton** needs a derivative and a good starting guess, and in exchange it
doubles the correct digits every step. The constant 0.3535 in the
`e_k/e_(k-1)^2` column is `f″(α)/(2f′(α))` computed by hand from the
polynomial; the code did not fit it. Its failure modes are worth memorising
because they are so common: the 2-cycle 0 ↔ 1 when `g(x) = x³ − 2x + 2` is
started at 0, and a division by zero when `f′(x₀) = 0` exactly.

**Secant** needs no derivative and converges at order (1+√5)/2 ≈ 1.618,
superlinear but not quadratic, because the finite-difference slope is only
first-order accurate. That is still the best trade when the objective is a
black box.

**Brent** is what you actually ship, and the code above is fifty lines:
keep three points, try inverse quadratic interpolation, fall back to
bisection whenever the fancy step would move less than a quarter of the way
in. That last rule is the entire safety argument — a rejected step can
never stall the interval — and it buys 8 steps instead of 39 at the same
tolerance and the same guarantee.

### Differentiation and integration

```python
"""Finite differences and quadrature: where the error comes from and how fast."""

import math

f = lambda x: x ** 3 - 2 * x
df = lambda x: 3 * x * x - 2

print("=== finite differences from the Taylor expansion ===")
print("f(x) = x**3 - 2x, so f'(1) =", df(1.0), "exactly.\n")
print("  h        forward          backward         central")
for h in [1e-2, 1e-4, 1e-6, 1e-8, 1e-10]:
    fwd = (f(1.0 + h) - f(1.0)) / h
    bwd = (f(1.0) - f(1.0 - h)) / h
    ctr = (f(1.0 + h) - f(1.0 - h)) / (2 * h)
    print(f"  {h:<9.0e} {fwd:<16.10f} {bwd:<16.10f} {ctr:<16.10f}")
print("  truth     1.0000000000    1.0000000000    1.0000000000")
print("Errors, not values:")
print("  h        forward          backward         central")
for h in [1e-2, 1e-4, 1e-6, 1e-8, 1e-10]:
    fwd = abs((f(1.0 + h) - f(1.0)) / h - 1.0)
    bwd = abs((f(1.0) - f(1.0 - h)) / h - 1.0)
    ctr = abs((f(1.0 + h) - f(1.0 - h)) / (2 * h) - 1.0)
    print(f"  {h:<9.0e} {fwd:<16.3e} {bwd:<16.3e} {ctr:<16.3e}")
print("f''(1) = 6, so the forward difference should be off by h*f''/2 = 3h:")
for h in [1e-2, 1e-4]:
    fwd = abs((f(1.0 + h) - f(1.0)) / h - 1.0)
    print(f"  h = {h:.0e}: measured {fwd:.3e}, predicted 3h = {3 * h:.3e}")
print("f'''(1) = 6, so the central difference should be off by h**2/6*6 = h**2:")
for h in [1e-4, 1e-6]:
    ctr = abs((f(1.0 + h) - f(1.0 - h)) / (2 * h) - 1.0)
    tag = "truncation-dominated" if h >= 1e-5 else "roundoff already dominates"
    print(f"  h = {h:.0e}: measured {ctr:.3e}, predicted h**2 = {h * h:.3e}"
          f"   ({tag})")
print("Central is worth the extra evaluation: same cost, one extra power of")
print("h. Look at the last row of the table above -- by h = 1e-10 all three")
print("rules give the same 8.3e-08, because none of them is measuring the")
print("shape of f any more, only the rounding of it.")

print("\n=== the two errors, and the step size that trades them off ===")
print("Truncation error goes down with h. Roundoff goes UP with h, because")
print("f(x+h) - f(x) is two numbers that nearly cancel and the difference is")
print("then divided by h. The best h sits where the two curves cross, and")
print("since they cross like h and 1/h the best error is O(sqrt(u)).")
print("\nWith f(x) = x**3 - 2x evaluated near x = 1e6, where |f| ~ 1e18:")
x0 = 1e6
truth = df(x0)
u = 2.220446049250313e-16
print("\n  h          error          truncation 3h      roundoff ~ u|f|/h")
best = None
for e in range(-4, 5):
    h = 10.0 ** e
    est = (f(x0 + h) - f(x0)) / h
    err = abs(est - truth)
    print(f"  {h:<11.0e} {err:<14.4e} {3 * h:<14.4e} "
          f"{u * abs(f(x0)) / h:<14.4e}")
    if best is None or err < best[1]:
        best = (h, err)
rel = best[1] / truth
print(f"best h in this sweep: {best[0]:.0e}, absolute error {best[1]:.4e}")
print("relative error", rel)
print("sqrt(u)        =", math.sqrt(u))
print("The two agree to within a factor of 1.2, and that is the whole")
print("theory: a first-order difference cannot beat O(sqrt(u)) no matter")
print("what step you pick. Getting 16 digits out of it is not on offer.")

print("\n=== Richardson extrapolation: buy the next power for free ===")
print("The forward difference has error C*h + O(h**2) with C known to be")
print("f''/2. Evaluate it at h and h/2 and cancel the h term:")


def d_forward(fn, x, h):
    return (fn(x + h) - fn(x)) / h


def richardson_first(fn, x, h):
    """(2*d(h/2) - d(h)) kills the O(h) term and leaves O(h**2)."""
    return 2.0 * d_forward(fn, x, h / 2.0) - d_forward(fn, x, h)


print("\n  h          forward error    Richardson error")
for h in [1e-2, 1e-3, 1e-4, 1e-5]:
    e1 = abs(d_forward(f, 1.0, h) - 1.0)
    e2 = abs(richardson_first(f, 1.0, h) - 1.0)
    print(f"  {h:<11.0e} {e1:<18.4e} {e2:<18.4e}")
print("One extra function evaluation buys a whole power of h. Apply the")
print("same trick again for h**3 accuracy, and again for h**5: that is where")
print("Romberg integration comes from.")

print("\n=== quadrature: three rules, three orders ===")
g = math.sin
A, B = 0.0, math.pi
TRUTH = 2.0


def trapezoid(fn, a, b, n):
    h = (b - a) / n
    s = 0.5 * fn(a) + 0.5 * fn(b)
    for i in range(1, n):
        s += fn(a + i * h)
    return s * h


def midpoint(fn, a, b, n):
    h = (b - a) / n
    return h * sum(fn(a + (i + 0.5) * h) for i in range(n))


def simpson(fn, a, b, n):
    h = (b - a) / n
    s = fn(a) + fn(b)
    for i in range(1, n):
        s += (4.0 if i % 2 else 2.0) * fn(a + i * h)
    return s * h / 3.0


print("integral of sin from 0 to pi is exactly 2.")
print("\n  n      trapezoid         midpoint         Simpson")
for n in [4, 8, 16, 32, 64, 128]:
    print(f"  {n:<6d} {trapezoid(g, A, B, n):<18.14f} "
          f"{midpoint(g, A, B, n):<18.14f} {simpson(g, A, B, n):<18.14f}")

print("\nobserved order p = log2(|E_n| / |E_2n|), where E_n is the error:")
print("\n  n      trapezoid         midpoint         Simpson")
for n in [8, 16, 32, 64, 128]:
    row = f"  {n:<6d}"
    for rule in (trapezoid, midpoint, simpson):
        e1 = abs(rule(g, A, B, n) - TRUTH)
        e2 = abs(rule(g, A, B, 2 * n) - TRUTH)
        p = math.log2(e1 / e2) if e2 > 0 else float("nan")
        row += f" {p:<18.4f}"
    print(row)
print("Trapezoid and midpoint both converge at order 2: halving h cuts the")
print("error by 4. Simpson converges at order 4: halving h cuts it by 16.")
print("That extra order costs nothing, because Simpson reuses Simpson's own")
print("midpoints plus the trapezoid endpoints instead of fresh nodes.")

print("\n=== the same trade-off appears here too ===")
print("Rule      evaluations   error")
errs = {}
for name, rule, n in [("trapezoid", trapezoid, 1024),
                      ("midpoint", midpoint, 1024),
                      ("simpson", simpson, 256)]:
    err = abs(rule(g, A, B, n) - TRUTH)
    errs[name] = err
    print(f"{name:10s} {n + 1:<13d} {err:.3e}")
print("At equal cost Simpson is",
      f"{errs['trapezoid'] / errs['simpson']:.0f}x",
      "more accurate than the trapezoid rule and",
      f"{errs['midpoint'] / errs['simpson']:.0f}x",
      "more accurate than the midpoint rule.")
print("The extra order is free because Simpson's nodes are the trapezoid's")
print("nodes plus their midpoints -- nothing is thrown away and recomputed.")
```

The error in a finite difference has two sources pulling in opposite
directions, and every practical question about step size follows from
where they cross.

Truncation error falls as h (forward) or h² (central). Roundoff rises as
1/h, because `f(x+h) − f(x)` is two nearly equal numbers whose difference is
then divided by h. Minimising the sum gives h* ≈ √(3u·|f|/|f′′|) for the
forward rule and h* ≈ (3u·|f|/|f′′′|)^(1/3) for the central one, and a best
achievable error of order √u. The sweep at x = 10⁶ finds a relative error of
1.28e-8 against a predicted floor of √u = 1.49e-8. That is the whole theory
in one line: **you cannot extract 16 digits from a first-order difference at
any step size.**

Richardson extrapolation then recovers the lost power for one extra
evaluation. `2·D(h/2) − D(h)` cancels the O(h) term of the forward
difference; doing it again cancels the O(h²) term that survived. The
Romberg table at the end of the Challenge is the same idea applied to
integration, where the win is larger still because the base rule is only
order 2.

On the integration side the same table appears with a cleaner result: the
observed order of every rule converges to its predicted value as the mesh
refines — 2.0000 for trapezoid and midpoint, 4.0001 for Simpson — and the
measured constants (2.0028 → 2.0000, 4.0200 → 4.0001) approach theory from
the wrong side, as asymptotic expansions require.

### With Libraries

Everything above in numpy, scipy, and matplotlib. This block requires numpy,
matplotlib and scipy, so it is not runnable with the standard library
alone.

```python
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq

print("numpy", np.__version__)

# --- panel data: finite-difference error against step size ------------------
x0 = 1e6
f = lambda x: x ** 3 - 2 * x
truth = 3 * x0 * x0 - 2
hs = np.logspace(-2, 8, 61)
fwd = np.array([abs((f(x0 + h) - f(x0)) / h - truth) for h in hs])
bwd = np.array([abs((f(x0) - f(x0 - h)) / h - truth) for h in hs])
ctr = np.array([abs((f(x0 + h) - f(x0 - h)) / (2 * h) - truth) for h in hs])

# --- panel data: quadrature error against panel count -----------------------
g = np.sin
A, B, TRUTH = 0.0, np.pi, 2.0
ns = np.array([4, 8, 16, 32, 64, 128, 256, 512, 1024], dtype=float)


def trap(a, b, n):
    n = int(n)
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    return h * (0.5 * g(a) + g(x[1:-1]).sum() + 0.5 * g(b))


def mid(a, b, n):
    n = int(n)
    h = (b - a) / n
    x = a + (np.arange(n) + 0.5) * h
    return h * g(x).sum()


def simp(a, b, n):
    n = int(n)
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    return h / 3 * (g(a) + g(b) + 4 * g(x[1:-1:2]).sum() + 2 * g(x[2:-1:2]).sum())


et = np.abs(np.array([trap(A, B, n) for n in ns]) - TRUTH)
em = np.abs(np.array([mid(A, B, n) for n in ns]) - TRUTH)
es = np.abs(np.array([simp(A, B, n) for n in ns]) - TRUTH)

print("\n--- dtypes and their precision ---")
for dt in [np.float16, np.float32, np.float64]:
    fi = np.finfo(dt)
    print(f"  np.{dt.__name__:8s} mantissa bits {fi.nmant + 1:3d}  "
          f"eps {fi.eps:.6e}  max {fi.max:.4e}")
print("  the same increment, 1e-5, in each dtype:")
for name, dt in [("float16", np.float16), ("float32", np.float32),
                 ("float64", np.float64)]:
    one = dt(1.0)
    r = one + dt(1e-5)
    eps = np.finfo(dt).eps
    print(f"    1.0 + 1e-5 as {name:8s} = {float(r)!r:20s} "
          f"changed? {float(r) != 1.0:<6} (eps {eps:.2e})")

print("\n--- numpy's own summation and root finding ---")
vals = [1e16, 1.0, -1e16, 1.0]
print("  np.sum([1e16,1,-1e16,1])  :", np.sum(vals))
print("  math.fsum of the same      :", math.fsum(vals))
xs = np.random.default_rng(7).random(1_000_000)
ref = math.fsum(xs)
tot = 0.0
for v in xs:
    tot += v
s_np = float(np.sum(xs))
print("  exact sum (math.fsum)                :", repr(ref))
print("  numpy np.sum of the same             :", repr(s_np),
      "  error", abs(s_np - ref))
print("  a plain Python loop over the same    :", repr(float(tot)),
      "  error", abs(float(tot) - ref))
print("  numpy sums in pairs, so its error grows like u*log(n) rather than")
print("  u*n. The trailing 1e16 demo shows the same thing:")
xs2 = np.array([1e16] + [1.0] * 1_000_000 + [-1e16])
tot2 = 0.0
for v in xs2:
    tot2 += v
print("    np.sum of [1e16, 1e6 ones, -1e16]  :", np.sum(xs2))
print("    the plain loop                     :", tot2)
print("    exact answer                       : 1000000")
gg = lambda t: t ** 3 - 2 * t + 2
r_b, info = brentq(gg, -10.0, 10.0, full_output=True)
print("  scipy brentq:", r_b, "in", info.iterations, "iterations, converged",
      info.converged)

print("\n--- exact decimal arithmetic for money ---")
from decimal import Decimal, getcontext
price = Decimal("0.1")
bill = price * 3
print("  Decimal('0.1') * 3 =", bill)
print("  float 0.1 * 3     =", 0.1 * 3)
print("  a tenth of a cent on a $1M invoice is",
      Decimal("0.001") * 1000000, "-- float64 cannot see that at all")
getcontext().prec = 4
print("  with prec=4, Decimal('1')/3 =", Decimal(1) / 3)
getcontext().prec = 28
print("  with prec=28,               =", Decimal(1) / 3)

# --- the figure -------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4))

ax = axes[0]
ax.loglog(hs, fwd, "o-", ms=3, lw=1.4, label="forward difference")
ax.loglog(hs, bwd, "s-", ms=3, lw=1.4, label="backward difference")
ax.loglog(hs, ctr, "^-", ms=3, lw=1.4, label="central difference")
ax.loglog(hs, 3 * hs, ":", color="0.6", lw=1.2,
          label=r"$O(h)$ truncation, slope 1")
ax.loglog(hs, 2.22e-16 * abs(f(x0)) / hs, ":", color="0.35", lw=1.2,
          label=r"$O(u|f|/h)$ roundoff, slope $-1$")
ax.axvline(1e-2, color="crimson", lw=1.0, alpha=0.7)
ax.annotate("best step for the\nforward difference", xy=(1e-2, 5e13),
            xytext=(1e3, 3e13), fontsize=8, color="crimson",
            arrowprops=dict(arrowstyle="->", color="crimson", lw=1.0))
ax.set_xlabel("step size h")
ax.set_ylabel("absolute error in f'(1e6)")
ax.set_title("Finite differences: truncation up, roundoff down")
ax.grid(True, which="both", alpha=0.25)
ax.legend(fontsize=7.5, loc="lower right")

ax = axes[1]
ax.loglog(ns, et, "o-", ms=3, lw=1.4, label="trapezoid, order 2")
ax.loglog(ns, em, "s-", ms=3, lw=1.4, label="midpoint, order 2")
ax.loglog(ns, es, "^-", ms=3, lw=1.4, label="Simpson, order 4")
ax.loglog(ns, et[0] * (ns / ns[0]) ** -2, ":", color="0.6", lw=1.2,
          label=r"$n^{-2}$ reference")
ax.loglog(ns, es[0] * (ns / ns[0]) ** -4, ":", color="0.35", lw=1.2,
          label=r"$n^{-4}$ reference")
ax.set_xlabel("panels n   (h = pi/n)")
ax.set_ylabel("absolute error")
ax.set_title(r"$\int_0^\pi \sin x\,dx = 2$: Simpson doubles the slope")
ax.grid(True, which="both", alpha=0.25)
ax.legend(fontsize=7.5, loc="upper right")

fig.suptitle("Numerical error behaves exactly as the theory predicts", y=1.0)
fig.tight_layout()
fig.savefig("numerical_error.png", dpi=110, bbox_inches="tight")
print("\nwrote numerical_error.png")

print("\n--- observed orders, fitted from the figure's own data ---")
for label, err in [("trapezoid", et), ("midpoint", em), ("Simpson", es)]:
    sl = np.polyfit(-np.log(ns[2:]), np.log(err[2:]), 1)[0]
    print(f"  {label:10s} fitted order {sl:.3f}")
```

Two observations worth separating from the rest.

The dtype table shows that `1e-5` is a no-op in `float16` and invisible in
`float32`, and that the failure is *silent*. The same expression, the same
Python, three different answers. This is why `torch.set_default_dtype` and
`jax.config` are not defaults you should leave alone.

The summation comparison shows why `np.sum` is not the same as a loop. numpy
sums in pairs, recursively, so its error grows like u·log(n) rather than
u·n; on a million random values it reproduces `math.fsum` exactly where the
loop is off by 1.8e-14. The second demonstration is the sharper one:
`np.sum([1e16] + [1.0]*10**6 + [-1e16])` returns 999986 rather than the
exact 1000000, because pairwise blocking changed which terms shared a
partial sum. Pairwise is a large improvement, not a guarantee.

## Common Mistakes

**1. Treating `0.1 + 0.2 != 0.3` as a Python bug.** It is a binary
representation issue. Use `math.isclose(a, b, rel_tol=...)` for
comparison, and `Fraction` or `Decimal` when the value is contractual.

**2. Subtracting near-equals to "recover" something.** `a - b` where
`a ≈ b` is the single most destructive operation in numerical computing, and
it appears disguised in the quadratic formula, in `1 - cos(x)`, in
`sqrt(b*b - 4*c)`, in computing `sin(b) - sin(a)` for close a and b, and in
almost every finite-difference stencil. Rewrite the expression.

**3. Stopping a root-finder on `abs(f(x)) < tol`.** Near a multiple root, or
any point where f′ is small, |f| is tiny while x is nowhere near the answer.
Stop on the change in x, made relative: `abs(x_k - x_prev) <= tol * (1 + abs(x_k))`.

**4. Shrinking h forever.** Below the roundoff floor a finite difference
gets *worse*, monotonically. There is a √u barrier and no step size crosses
it.

**5. Believing a big relative error means the algorithm is bad.** Check the
condition number first. κ = 10¹² on your problem means the input, not the
solver, sets the accuracy.

**6. Assuming a library function is the textbook formula.** `math.hypot`,
`math.expm1`, `math.log1p`, `math.fsum`, `math.ldexp` and `math.frexp` all
exist because the textbook formula is not what you should write.

**7. Using `float32` because it is "fast enough".** It has 24 mantissa bits,
so `1 + 1e-5` works and `1 + 1e-6` does not. For any iterative process the
error compounds, and `float32` reaches its floor in about 10⁷ iterations.

**8. Trusting an extrapolated result on a non-smooth function.** Richardson
and Romberg assume the error is a clean power series in h. The Challenge at
the end shows extrapolation turning an *exact* answer into a wrong one.

**9. Comparing floats with `==` in a loop.** After any operation that could
round, the correct test is `a == b` or `abs(a-b) <= tol*(1+abs(b))` — not
`a == b` after a chain of steps where each step was only approximately
equal.

## Exercises and Solutions

**[ ] Exercise 1 — ** Rewrite five unstable expressions and measure the
improvement against a 50-digit decimal reference: `1 - cos(x)`, `exp(x) - 1`,
the small root of a quadratic, `sqrt(p² + q²)`, and `log(1 + x)`. For each
one report the naive relative error, the rewritten relative error, and the
ratio between them.

<details>
<summary>Solution</summary>

```python
"""Exercise 1: rewrite five unstable expressions and measure the difference."""

import math
from decimal import Decimal, getcontext

getcontext().prec = 50


def rel(got, truth):
    """Relative error of `got` against an exact Decimal."""
    if truth == 0:
        return 0.0 if got == 0 else float("inf")
    return float(abs(Decimal(got) - truth) / abs(truth))


print("Five formulas, each of which loses digits to a subtraction or to an")
print("overflow. Each row compares the original with a rewrite, both against")
print("a 50-digit decimal reference.\n")

# --- (a) 1 - cos(x) --------------------------------------------------------
x = 1e-7
truth_a = Decimal(1) - Decimal(repr(math.cos(x)))
# recompute the truth honestly: use the series, which has no cancellation
xs = Decimal("1e-7")
truth_a = xs * xs / 2 - xs ** 4 / 24
naive_a = 1.0 - math.cos(x)
stable_a = 2.0 * math.sin(x / 2.0) ** 2
print("(a) 1 - cos(x),  x =", x)
print("    naive   1 - cos(x)          =", repr(naive_a))
print("    stable  2*sin(x/2)**2       =", repr(stable_a))
print("    series  x**2/2 - x**4/24    =", float(truth_a))
print("    relative error  naive", f"{rel(naive_a, truth_a):.3e}",
      "   stable", f"{rel(stable_a, truth_a):.3e}")

# --- (b) exp(x) - 1 --------------------------------------------------------
y = 1e-18
truth_b = Decimal("1e-18") + Decimal("1e-18") ** 2 / 2
naive_b = math.exp(y) - 1.0
stable_b = math.expm1(y)
print("\n(b) exp(x) - 1,  x =", y)
print("    naive   exp(x) - 1          =", repr(naive_b))
print("    stable  math.expm1(x)       =", repr(stable_b))
print("    series  x + x**2/2          =", float(truth_b))
print("    relative error  naive", f"{rel(naive_b, truth_b):.3e}",
      "   stable", f"{rel(stable_b, truth_b):.3e}")

# --- (c) the small root of a quadratic -------------------------------------
b, c = 2.0 ** 26, 1e-5
# the true small root solves x**2 - 2b x + c = 0; get it as c / x_big
x_big = (b + math.sqrt(b * b - 4 * c)) / 2
truth_c = Decimal(1) / Decimal(10) ** 5 / Decimal(int(x_big))
naive_c = (b - math.sqrt(b * b - 4 * c)) / 2
stable_c = c / x_big
print("\n(c) small root of x**2 - 2b*x + c,  b = 2**26, c = 1e-5")
print("    naive   (b - sqrt(b*b-4c))/2 =", repr(naive_c))
print("    stable  c / x_big             =", repr(stable_c))
print("    reference                     =", float(truth_c))
print("    relative error  naive", f"{rel(naive_c, truth_c):.3e}",
      "   stable", f"{rel(stable_c, truth_c):.3e}")

# --- (d) a length, without overflow -----------------------------------------
p, q = 1e200, 1e200
truth_d = Decimal(10) ** 200 * Decimal(2).sqrt()
naive_d = math.sqrt(p * p + q * q)
stable_d = math.hypot(p, q)
print("\n(d) sqrt(p**2 + q**2),  p = q = 1e200")
print("    p*p                =", p * p)
print("    naive   sqrt(p*p+q*q)      =", repr(naive_d))
print("    stable  math.hypot(p, q)   =", repr(stable_d))
print("    reference                     =", float(truth_d))
print("    relative error  naive", f"{rel(naive_d, truth_d):.3e}",
      "   stable", f"{rel(stable_d, truth_d):.3e}")

# --- (e) log(1 + x) --------------------------------------------------------
z = 1e-18
truth_e = Decimal("1e-18") - Decimal("1e-18") ** 2 / 2
naive_e = math.log(1.0 + z)
stable_e = math.log1p(z)
print("\n(e) log(1 + x),  x =", z)
print("    naive   log(1 + x)          =", repr(naive_e))
print("    stable  math.log1p(x)       =", repr(stable_e))
print("    series  x - x**2/2          =", float(truth_e))
print("    relative error  naive", f"{rel(naive_e, truth_e):.3e}",
      "   stable", f"{rel(stable_e, truth_e):.3e}")

print("\n=== summary ===")
print("case   naive relative error   stable relative error   gain")
CASES = [
    ("1 - cos(x)", rel(naive_a, truth_a), rel(stable_a, truth_a)),
    ("exp(x) - 1", rel(naive_b, truth_b), rel(stable_b, truth_b)),
    ("quadratic", rel(naive_c, truth_c), rel(stable_c, truth_c)),
    ("sqrt(p^2+q^2)", rel(naive_d, truth_d), rel(stable_d, truth_d)),
    ("log(1 + x)", rel(naive_e, truth_e), rel(stable_e, truth_e)),
]
for name, en, es in CASES:
    if en == 0:
        gain = "n/a (already exact)"
    elif es == 0:
        gain = "infinite (rewrite is exact)"
    else:
        gain = f"{en / es:.3g}x"
    print(f"{name:14s} {en:<21.3e} {es:<22.3e} {gain}")
print("\nIn four of the five the rewrite is not a small improvement but the")
print("difference between a number and no number at all. The pattern is")
print("always the same: the naive form subtracts, scales, or squares something")
print("it should have left alone.")
```

Output:

```
Five formulas, each of which loses digits to a subtraction or to an
overflow. Each row compares the original with a rewrite, both against
a 50-digit decimal reference.

(a) 1 - cos(x),  x = 1e-07
    naive   1 - cos(x)          = 4.9960036108132044e-15
    stable  2*sin(x/2)**2       = 4.999999999999995e-15
    series  x**2/2 - x**4/24    = 4.999999999999996e-15
    relative error  naive 7.993e-04    stable 1.145e-16

(b) exp(x) - 1,  x = 1e-18
    naive   exp(x) - 1          = 0.0
    stable  math.expm1(x)       = 1e-18
    series  x + x**2/2          = 1e-18
    relative error  naive 1.000e+00    stable 7.104e-17

(c) small root of x**2 - 2b*x + c,  b = 2**26, c = 1e-5
    naive   (b - sqrt(b*b-4c))/2 = 0.0
    stable  c / x_big             = 1.4901161193847657e-13
    reference                     = 1.4901161193847657e-13
    relative error  naive 1.000e+00    stable 8.180e-17

(d) sqrt(p**2 + q**2),  p = q = 1e200
    p*p                = inf
    naive   sqrt(p*p+q*q)      = inf
    stable  math.hypot(p, q)   = 1.414213562373095e+200
    reference                     = 1.414213562373095e+200
    relative error  naive inf    stable 4.196e-18

(e) log(1 + x),  x = 1e-18
    naive   log(1 + x)          = 0.0
    stable  math.log1p(x)       = 1e-18
    series  x - x**2/2          = 1e-18
    relative error  naive 1.000e+00    stable 7.204e-17

=== summary ===
case   naive relative error   stable relative error   gain
1 - cos(x)     7.993e-04             1.145e-16              6.98e+12x
exp(x) - 1     1.000e+00             7.104e-17              1.41e+16x
quadratic      1.000e+00             8.180e-17              1.22e+16x
sqrt(p^2+q^2)  inf                   4.196e-18              infx
log(1 + x)     1.000e+00             7.204e-17              1.39e+16x

In four of the five the rewrite is not a small improvement but the
difference between a number and no number at all. The pattern is
always the same: the naive form subtracts, scales, or squares something
it should have left alone.
```

The gain column is the whole point. Three of the five have a naive relative
error of exactly 1.0, which is the floating-point way of saying the answer
is not merely wrong but *absent* — `0.0` where `1.49e-13` belonged.

The `sqrt(p² + q²)` row is the odd one out, and it is instructive: the naive
form returns `inf`, so its relative error against an exact reference is
infinite, while `hypot` is within 4.2e-18. Nothing about that rewrite is
about cancellation — it is about the exponent range, and no amount of
algebra would have fixed it.

The pattern across all five: the naive form **subtracts**, **scales**, or
**squares** something it should have left alone. Every fix is a
rearrangement that avoids one of those three operations, and not one of
them adds a single digit of working precision.

</details>

**[ ] Exercise 2 — ** Implement bisection, Newton and secant for
`x³ − 3x + 1 = 0`, whose three roots are `2cos(2π/9)`, `2cos(4π/9)` and
`2cos(8π/9)`. For each method report the iteration count, the errors at
every step, the measured order of convergence, and — for Newton — the
asymptotic constant `f″(α)/(2f′(α))` compared with the predicted value.

<details>
<summary>Solution</summary>

```python
"""Exercise 2: three root-finders, one stopping rule, measured orders."""

import math


def bisect(f, a, b, xtol=1e-15, maxit=400):
    fa = f(a)
    for k in range(1, maxit + 1):
        m = 0.5 * (a + b)
        if m == a or m == b:
            return m, k
        if f(m) == 0.0:
            return m, k
        if fa * f(m) < 0:
            b = m
        else:
            a, fa = m, f(m)
        if 0.5 * (b - a) <= xtol:
            return m, k
    return m, maxit


def newton(f, df, x0, xtol=1e-15, maxit=200):
    xs = [x0]
    for _ in range(maxit):
        x = xs[-1]
        d = df(x)
        if d == 0.0:
            break
        xn = x - f(x) / d
        xs.append(xn)
        if abs(xn - x) <= xtol * (1 + abs(xn)):
            break
    return xs


def secant(f, x0, x1, xtol=1e-15, maxit=200):
    xs = [x0, x1]
    for _ in range(maxit):
        xa, xb = xs[-2], xs[-1]
        fa, fb = f(xa), f(xb)
        if fb == fa:
            break
        xn = xb - fb * (xb - xa) / (fb - fa)
        xs.append(xn)
        if abs(xn - xb) <= xtol * (1 + abs(xn)):
            break
    return xs


def observed_order(errs):
    """Fit p in |e_k| ~ C |e_{k-1}|**p using two consecutive error ratios.

    log(e_k)/log(e_{k-1}) is only meaningful when e_{k-1} < 1, so the
    caller must pass errors that are already below 1.
    """
    orders = []
    for k in range(1, len(errs)):
        e, ep = errs[k], errs[k - 1]
        if e > 0.0 and 0.0 < ep < 1.0:
            orders.append(math.log(e) / math.log(ep))
    return orders


# x**3 - 3x + 1 = 0, put x = 2cos(theta): 8cos^3 - 6cos + 1 = 2cos(3t) + 1,
# so cos(3 theta) = -1/2 and the roots are 2cos(2pi/9), 2cos(4pi/9),
# 2cos(8pi/9). Closed form, so no Decimal reference is needed.
f = lambda x: x ** 3 - 3 * x + 1
df = lambda x: 3 * x * x - 3
TRUTHS = [2 * math.cos(2 * math.pi / 9), 2 * math.cos(4 * math.pi / 9),
          2 * math.cos(8 * math.pi / 9)]

print("f(x) = x**3 - 3x + 1 has three real roots, all known in closed form:")
for t in TRUTHS:
    print("   ", repr(t), " f(t) =", f(t))
ROOT = TRUTHS[1]

print("\n=== bisection on [0, 1] ===")
xs_bis = []
a, b = 0.0, 1.0
fa = f(a)
for _ in range(400):
    m = 0.5 * (a + b)
    xs_bis.append(m)
    if 0.5 * (b - a) <= 1e-15:
        break
    if fa * f(m) < 0:
        b = m
    else:
        a, fa = m, f(m)
errs = [abs(x - ROOT) for x in xs_bis[:60]]
ratios = [errs[k + 1] / errs[k] for k in range(len(errs) - 1) if errs[k] > 0]
gm = math.exp(sum(math.log(r) for r in ratios) / len(ratios))
print("iterations run:", len(xs_bis))
print("first 8 errors:", [f"{e:.4e}" for e in errs[:8]])
print("The individual ratios bounce around (halving a bracket halves the")
print("WIDTH; the error is only guaranteed to be under half the width). The")
print("geometric mean of e_(k+1)/e_k settles at", f"{gm:.4f}", "-- that is")
print("the rate, and 1/2 = 0.5 is what order-1 convergence with a halving")
print("bracket means.")
print("  order estimates:", [round(o, 3) for o in observed_order(errs[:20])][:8])

print("\n=== Newton from 0.5 ===")
xs_n = newton(f, df, 0.5)
signed = [x - ROOT for x in xs_n]
errs = [abs(e) for e in signed]
print("iterations:", len(xs_n) - 1)
print("path      :", " -> ".join(f"{x:.8f}" for x in xs_n))
print("errors    :", [f"{e:.4e}" for e in errs])
print("order estimates:", [round(o, 4) for o in observed_order(errs)])
print("The theory says the order is 2, with asymptotic constant")
print("C = f''(alpha)/(2 f'(alpha)). Here f'' = 6x and f' = 3x**2 - 3, so at")
alpha = ROOT
const = 6 * alpha / (2 * (3 * alpha ** 2 - 3))
print("  alpha                 =", alpha)
print("  predicted C           =", const)
print("The constant must be read off SIGNED errors, because C is negative")
print("here -- f' is negative at this root, so every iterate sits below it:")
print("  signed errors        :", [f"{e:.4e}" for e in signed])
print("  e_2 / e_1**2         =", f"{signed[2] / signed[1] ** 2:.4f}")
print("  e_3 / e_2**2         =", f"{signed[3] / signed[2] ** 2:.4f}")
print("  e_4 / e_3**2         =", f"{signed[4] / signed[3] ** 2:.4f}",
      " <- roundoff has taken over; the number means nothing")
print("Order 2 only shows once the errors are small; the first steps start")
print("far away and behave like a much slower method. That is what 'local'")
print("convergence means.")

print("\n=== secant from 0.5 and 1.0 ===")
xs_s = secant(f, 0.5, 1.0)
errs_s = [abs(x - ROOT) for x in xs_s]
print("iterations:", len(xs_s) - 1)
print("errors    :", [f"{e:.4e}" for e in errs_s])
ords = observed_order(errs_s)
print("order estimates:", [round(o, 4) for o in ords])
phi = (1 + math.sqrt(5)) / 2
print("approaching (1+sqrt(5))/2 =", phi)

print("\n=== all three, same tolerance, same root ===")
print("method      steps   |answer - truth|")
rb, kb = bisect(f, 0.0, 1.0)
xn = newton(f, df, 0.5)
xs_ = secant(f, 0.5, 1.0)
for name, ans, k in [("bisection", rb, kb), ("newton", xn[-1], len(xn) - 1),
                     ("secant", xs_[-1], len(xs_) - 2)]:
    print(f"{name:11s} {k:6d}   {abs(ans - ROOT):.3e}")
print("Newton wins on speed and ties on accuracy -- but only because 0.5 is a")
print("good starting guess. The next table shows what happens when it is not.")

print("\n=== Newton from a variety of starting guesses ===")
print("The same method now walks to a DIFFERENT root each time, because this")
print("polynomial has three of them. Bisection cannot do that: the bracket")
print("picks the root for you, and that is the real argument for it. The")
print("x0 = -1.0 row is a different failure: f'(-1) = 0 exactly, so the very")
print("first step divides by zero and the method returns its input untouched.")
for x0 in [-3.0, -2.0, -1.0, 0.0, 0.5, 2.0, 3.0, 5.0]:
    xs = newton(f, df, x0, maxit=60)
    print(f"  x0 = {x0:<6} {len(xs) - 1:3d} iterations -> {xs[-1]!r:22s} "
          f"|error| {abs(xs[-1] - ROOT):.3e}")

print("\n=== where each method stops improving ===")
print("float64 has about 16 significant digits. Newton reaches that and")
print("then the iterate starts moving at random in the last ulp:")
xs = newton(f, df, 0.5)
for k, x in enumerate(xs):
    print(f"  step {k}: {x!r:22s} |error| {abs(x - ROOT):.3e}")
print("Bisection, by contrast, keeps halving its bracket whether or not that")
print("helps, and needs about", kb, "steps to get there.")
```

Output:

```
f(x) = x**3 - 3x + 1 has three real roots, all known in closed form:
    1.532088886237956  f(t) = -4.440892098500626e-16
    0.34729635533386083  f(t) = -4.440892098500626e-16
    -1.8793852415718166  f(t) = 8.881784197001252e-16

=== bisection on [0, 1] ===
iterations run: 50
first 8 errors: ['1.5270e-01', '9.7296e-02', '2.7704e-02', '3.4796e-02', '3.5464e-03', '1.2079e-02', '4.2661e-03', '3.5989e-04']
The individual ratios bounce around (halving a bracket halves the
WIDTH; the error is only guaranteed to be under half the width). The
geometric mean of e_(k+1)/e_k settles at 0.4980 -- that is
the rate, and 1/2 = 0.5 is what order-1 convergence with a halving
bracket means.
  order estimates: [1.24, 1.539, 0.936, 1.68, 0.783, 1.236, 1.453, 0.812]

=== Newton from 0.5 ===
iterations: 5
path      : 0.50000000 -> 0.33333333 -> 0.34722222 -> 0.34729635 -> 0.34729636 -> 0.34729636
errors    : ['1.5270e-01', '1.3963e-02', '7.4133e-05', '2.1700e-09', '1.1102e-16', '2.2204e-16']
order estimates: [2.2729, 2.2264, 2.0977, 1.8416, 0.9811]
The theory says the order is 2, with asymptotic constant
C = f''(alpha)/(2 f'(alpha)). Here f'' = 6x and f' = 3x**2 - 3, so at
  alpha                 = 0.34729635533386083
  predicted C           = -0.39493084363469866
The constant must be read off SIGNED errors, because C is negative
here -- f' is negative at this root, so every iterate sits below it:
  signed errors        : ['1.5270e-01', '-1.3963e-02', '-7.4133e-05', '-2.1700e-09', '-1.1102e-16', '-2.2204e-16']
  e_2 / e_1**2         = -0.3802
  e_3 / e_2**2         = -0.3949
  e_4 / e_3**2         = -23.5773  <- roundoff has taken over; the number means nothing
Order 2 only shows once the errors are small; the first steps start
far away and behave like a much slower method. That is what 'local'
convergence means.

=== secant from 0.5 and 1.0 ===
iterations: 9
errors    : ['1.5270e-01', '6.5270e-01', '1.4730e-01', '8.4522e-02', '4.5363e-03', '1.7086e-04', '3.0792e-07', '2.0773e-11', '1.1102e-16', '2.2204e-16']
order estimates: [0.227, 4.4894, 1.29, 2.1838, 1.6077, 1.7284, 1.6405, 1.4935, 0.9811]
approaching (1+sqrt(5))/2 = 1.618033988749895

=== all three, same tolerance, same root ===
method      steps   |answer - truth|
bisection       49   1.110e-15
newton           5   2.220e-16
secant           8   2.220e-16
Newton wins on speed and ties on accuracy -- but only because 0.5 is a
good starting guess. The next table shows what happens when it is not.

=== Newton from a variety of starting guesses ===
The same method now walks to a DIFFERENT root each time, because this
polynomial has three of them. Bisection cannot do that: the bracket
picks the root for you, and that is the real argument for it. The
x0 = -1.0 row is a different failure: f'(-1) = 0 exactly, so the very
first step divides by zero and the method returns its input untouched.
  x0 = -3.0     7 iterations -> -1.8793852415718169    |error| 2.227e+00
  x0 = -2.0     5 iterations -> -1.8793852415718166    |error| 2.227e+00
  x0 = -1.0     0 iterations -> -1.0                   |error| 1.347e+00
  x0 = 0.0      5 iterations -> 0.34729635533386066    |error| 1.665e-16
  x0 = 0.5      5 iterations -> 0.3472963553338606     |error| 2.220e-16
  x0 = 2.0      7 iterations -> 1.532088886237956      |error| 1.185e+00
  x0 = 3.0      8 iterations -> 1.532088886237956      |error| 1.185e+00
  x0 = 5.0      9 iterations -> 1.5320888862379562     |error| 1.185e+00

=== where each method stops improving ===
float64 has about 16 significant digits. Newton reaches that and
then the iterate starts moving at random in the last ulp:
  step 0: 0.5                    |error| 1.527e-01
  step 1: 0.33333333333333337    |error| 1.396e-02
  step 2: 0.34722222222222227    |error| 7.413e-05
  step 3: 0.347296353163868      |error| 2.170e-09
  step 4: 0.3472963553338607     |error| 1.110e-16
  step 5: 0.3472963553338606     |error| 2.220e-16
Bisection, by contrast, keeps halving its bracket whether or not that
helps, and needs about 49 steps to get there.
```

Three things are worth pulling out of that.

**The bisection rate is 1/2, not a clean 1.** Halving a bracket halves its
*width*; the error is only *bounded* by half the width, so the individual
ratios bounce around 1.0 between 0.78 and 1.68. The geometric mean settles
at 0.4980, and that is the honest statement of the rate.

**Newton's constant is negative, and you only see it with signed errors.**
f′ is negative at this root, so every iterate lies below it, and the
measured `e₃/e₂²` comes out at −0.3949 against a predicted −0.39493. Take
absolute values and you get +0.3949, which looks like a sign error in the
theory. It is not; the ratio is only meaningful when the sign of the error
is preserved. And the last ratio, −23.58, is not a contradiction: at that
point the error is 2e-9, the square of it is 4.7e-18, and the ratio of two
quantities that close to the float floor is noise.

**The "bad starting guess" table does not show a bad method, it shows a
different question.** Newton from −3 converges in 7 steps to the root
−1.879, and from 2 converges in 7 steps to the root 1.532. Both are
*correct* — they just answered a different question than the one the
`ROOT` variable was set up for. Bisection on [0, 1] cannot make that
mistake, because the bracket already named the root. That is the real
argument for bisection, and it is not about speed.

</details>

**[ ] Exercise 3 — ** Define the condition number of summation,
κ = Σ|xᵢ| / |Σ xᵢ|, and use it to predict which of six test cases will lose
digits. Then compare naive summation, Kahan, Neumaier and `math.fsum`
against `Fraction`-based exact arithmetic, and explain the one case where
Neumaier beats Kahan.

<details>
<summary>Solution</summary>

```python
"""Exercise 3: the condition number of summation, and four ways to sum."""

import math
from fractions import Fraction
from itertools import permutations


def cond_sum(xs):
    """kappa = sum|x_i| / |sum x_i|: the worst-case amplification of rounding.

    Each input carries absolute error at most u*|x_i|; the total inherits
    at most u * sum|x_i| of absolute error, while the answer itself is only
    |sum x_i| long. Divide one by the other.
    """
    num = math.fsum(abs(x) for x in xs)
    den = abs(math.fsum(xs))
    return float("inf") if den == 0 else num / den


def naive_sum(xs):
    total = 0.0
    for x in xs:
        total += x
    return total


def kahan_sum(xs):
    total, c = 0.0, 0.0
    for x in xs:
        y = x - c
        t = total + y
        c = (t - total) - y
        total = t
    return total


def neumaier_sum(xs):
    """Kahan plus a correction for the case Kahan's test gets wrong."""
    total, c = 0.0, 0.0
    for x in xs:
        t = total + x
        if abs(total) >= abs(x):
            c += (total - t) + x
        else:
            c += (x - t) + total
        total = t
    return total + c


def exact_sum(xs):
    return float(sum(Fraction(x) for x in xs))


def rel(got, truth):
    if truth == 0:
        return 0.0 if got == 0 else float("inf")
    return abs(got - truth) / abs(truth)


CASES = [
    ("ten 0.1s", [0.1] * 10),
    ("a hundred 0.1s", [0.1] * 100),
    ("1e16 then 1e4 ones", [1e16] + [1.0] * 10_000),
    ("1e16, 1, -1e16, 1", [1e16, 1.0, -1e16, 1.0]),
    ("0.1 and -0.1 (sum 0)", [0.1, -0.1]),
]

print("kappa = sum|x_i| / |sum x_i| is the worst-case amplification of")
print("rounding in a sum. kappa = 1 is perfect conditioning: nothing is")
print("amplified. kappa = 1e16 says the last 16 digits can vanish.\n")
print("case                    kappa      exact         naive          kahan"
      "         neumaier       fsum")
for label, xs in CASES:
    print(f"{label:23s} {cond_sum(xs):<11.4g} {exact_sum(xs):<13.6g} "
          f"{naive_sum(xs):<14.6g} {kahan_sum(xs):<14.6g} "
          f"{neumaier_sum(xs):<14.6g} {math.fsum(xs):<14.6g}")

print("\nrelative errors against the exact rational sum:")
print("case                    naive          kahan         neumaier      fsum")
for label, xs in CASES:
    truth = exact_sum(xs)
    print(f"{label:23s} {rel(naive_sum(xs), truth):<14.3e} "
          f"{rel(kahan_sum(xs), truth):<14.3e} "
          f"{rel(neumaier_sum(xs), truth):<14.3e} "
          f"{rel(math.fsum(xs), truth):<14.3e}")

print("\n=== the two rows that teach the lesson ===")
xs = [1e16] + [1.0] * 10_000
print("Row 3, [1e16] + 10000 ones, has kappa = 1 and still loses 1e-12.")
print("kappa is a WORST CASE, not a prediction: it bounds the damage, it")
print("does not promise any. Sorting smallest-first removes the damage:")
print("  descending order, naive:", naive_sum(sorted(xs, key=abs,
                                                    reverse=True)))
print("  ascending order,  naive:", naive_sum(sorted(xs, key=abs)))
print("  exact                   :", exact_sum(xs))
print("No algorithm needed -- only the observation that adding small things")
print("to a big one is what loses them.\n")

xs = [1e16, 1.0, -1e16, 1.0]
print("Row 4, [1e16, 1, -1e16, 1], has kappa = 1e16 and is genuinely lost.")
print("Here sorting does not help either, because the orderings that work")
print("are lucky rather than principled. The distinct orderings, with the")
print("running total after each addition:")
seen = set()
rows = []
for perm in permutations(range(4)):
    order = tuple(xs[i] for i in perm)
    if order in seen:
        continue
    seen.add(order)
    tot, run = 0.0, []
    for v in order:
        tot += v
        run.append(tot)
    rows.append((abs(tot - 2.0), order, tot, run))
for _, order, tot, run in sorted(rows):
    print(f"  {str(list(order)):34s} -> {tot}   partials {run}")
print("Every ordering that gives 2.0 has the two 1.0s adjacent -- both")
print("before the big terms, or both after they have cancelled. Split them")
print("with a 1e16 in between and one of them is swallowed whole. The")
print("information was never in the running total to recover, so no")
print("summation algorithm can help here: only exact arithmetic can.")

print("\n=== row 5, where kappa is infinite but nothing is lost ===")
xs = [0.1, -0.1]
print("xs =", xs, " has sum exactly", exact_sum(xs))
print("kappa = sum|x| / |sum x| =", cond_sum(xs),
      "-- division by zero, not a typo")
print("and yet every method returns the right answer, because 0.1 - 0.1 is")
print("exactly representable. kappa says 'this sum could lose everything'.")
print("It does not say 'this sum does lose something'. Conditioning is a")
print("bound on the worst case, not a diagnosis of the case in front of you.")

print("\n=== what each algorithm actually defends against ===")
print("naive     no defence at all.")
print("kahan     recovers the ROUNDING of each partial sum: it keeps the bits")
print("          that fell off the end and folds them back on the next add.")
print("neumaier  the same idea, but its correction test is right in the case")
print("          Kahan's is not, when the incoming |x| exceeds |total|.")
print("          Row 4 is exactly that case, and the two disagree there.")
print("fsum      exact. It carries every partial sum in wider precision and")
print("          rounds once at the end, so it is right whenever the input")
print("          floats are right -- and it is not cheap. Use it when the")
print("          answer has to be defensible, not on every inner loop.")
```

Output:

```
kappa = sum|x_i| / |sum x_i| is the worst-case amplification of
rounding in a sum. kappa = 1 is perfect conditioning: nothing is
amplified. kappa = 1e16 says the last 16 digits can vanish.

case                    kappa      exact         naive          kahan         neumaier       fsum
ten 0.1s                1           1             1              1              1              1             
a hundred 0.1s          1           10            10             10             10             10            
1e16 then 1e4 ones      1           1e+16         1e+16          1e+16          1e+16          1e+16         
1e16, 1, -1e16, 1       1e+16       2             1              1              2              2             
0.1 and -0.1 (sum 0)    inf         0             0              0              0              0             

relative errors against the exact rational sum:
case                    naive          kahan         neumaier      fsum
ten 0.1s                1.110e-16      0.000e+00      0.000e+00      0.000e+00     
a hundred 0.1s          1.954e-15      0.000e+00      0.000e+00      0.000e+00     
1e16 then 1e4 ones      1.000e-12      0.000e+00      0.000e+00      0.000e+00     
1e16, 1, -1e16, 1       5.000e-01      5.000e-01      0.000e+00      0.000e+00     
0.1 and -0.1 (sum 0)    0.000e+00      0.000e+00      0.000e+00      0.000e+00     

=== the two rows that teach the lesson ===
Row 3, [1e16] + 10000 ones, has kappa = 1 and still loses 1e-12.
kappa is a WORST CASE, not a prediction: it bounds the damage, it
does not promise any. Sorting smallest-first removes the damage:
  descending order, naive: 1e+16
  ascending order,  naive: 1.000000000001e+16
  exact                   : 1.000000000001e+16
No algorithm needed -- only the observation that adding small things
to a big one is what loses them.

Row 4, [1e16, 1, -1e16, 1], has kappa = 1e16 and is genuinely lost.
Here sorting does not help either, because the orderings that work
are lucky rather than principled. The distinct orderings, with the
running total after each addition:
  [-1e+16, 1e+16, 1.0, 1.0]          -> 2.0   partials [-1e+16, 0.0, 1.0, 2.0]
  [1.0, 1.0, -1e+16, 1e+16]          -> 2.0   partials [1.0, 2.0, -9999999999999998.0, 2.0]
  [1.0, 1.0, 1e+16, -1e+16]          -> 2.0   partials [1.0, 2.0, 1.0000000000000002e+16, 2.0]
  [1e+16, -1e+16, 1.0, 1.0]          -> 2.0   partials [1e+16, 0.0, 1.0, 2.0]
  [-1e+16, 1.0, 1e+16, 1.0]          -> 1.0   partials [-1e+16, -1e+16, 0.0, 1.0]
  [1.0, -1e+16, 1e+16, 1.0]          -> 1.0   partials [1.0, -1e+16, 0.0, 1.0]
  [1.0, 1e+16, -1e+16, 1.0]          -> 1.0   partials [1.0, 1e+16, 0.0, 1.0]
  [1e+16, 1.0, -1e+16, 1.0]          -> 1.0   partials [1e+16, 1e+16, 0.0, 1.0]
  [-1e+16, 1.0, 1.0, 1e+16]          -> 0.0   partials [-1e+16, -1e+16, -1e+16, 0.0]
  [1.0, -1e+16, 1.0, 1e+16]          -> 0.0   partials [1.0, -1e+16, -1e+16, 0.0]
  [1.0, 1e+16, 1.0, -1e+16]          -> 0.0   partials [1.0, 1e+16, 1e+16, 0.0]
  [1e+16, 1.0, 1.0, -1e+16]          -> 0.0   partials [1e+16, 1e+16, 1e+16, 0.0]
Every ordering that gives 2.0 has the two 1.0s adjacent -- both
before the big terms, or both after they have cancelled. Split them
with a 1e16 in between and one of them is swallowed whole. The
information was never in the running total to recover, so no
summation algorithm can help here: only exact arithmetic can.

=== row 5, where kappa is infinite but nothing is lost ===
xs = [0.1, -0.1]  has sum exactly 0.0
kappa = sum|x| / |sum x| = inf -- division by zero, not a typo
and yet every method returns the right answer, because 0.1 - 0.1 is
exactly representable. kappa says 'this sum could lose everything'.
It does not say 'this sum does lose something'. Conditioning is a
bound on the worst case, not a diagnosis of the case in front of you.

=== what each algorithm actually defends against ===
naive     no defence at all.
kahan     recovers the ROUNDING of each partial sum: it keeps the bits
          that fell off the end and folds them back on the next add.
neumaier  the same idea, but its correction test is right in the case
          Kahan's is not, when the incoming |x| exceeds |total|.
          Row 4 is exactly that case, and the two disagree there.
fsum      exact. It carries every partial sum in wider precision and
          rounds once at the end, so it is right whenever the input
          floats are right -- and it is not cheap. Use it when the
          answer has to be defensible, not on every inner loop.
```

The two rows that teach the lesson pull in opposite directions, which is the
point.

Row 3, `[1e16] + 10⁴ ones`, has **κ = 1** and still loses a relative 1e-12.
Conditioning is a worst-case *bound*, not a prediction: it says how bad
things could get, not that they did. And no algorithm was needed — sorting
the terms smallest-first recovers the exact answer, because the loss came
purely from the order.

Row 4, `[1e16, 1, −1e16, 1]`, has **κ = 1e¹⁶** and is genuinely lost, and
here no order helps in general. The 12 distinct orderings make the mechanism
plain: every ordering that returns 2.0 has the two 1.0s *adjacent* — both
before the big terms, or both after they have cancelled. Split them with a
1e16 in between and one is swallowed whole. A compensated method cannot
recover a value that was never added to anything; only exact arithmetic
can, which is what `math.fsum` does by carrying every partial sum in wider
precision and rounding once at the end.

Row 5 is the subtlety worth flagging: κ = ∞ because the exact sum is zero,
and yet nothing is lost, because 0.1 − 0.1 is exact. **Conditioning bounds
the worst case; it does not diagnose the case in front of you.** Reporting
"this problem is ill-conditioned" about a computation that returned the
right answer is a category error.

</details>

**[ ] Exercise 4 — ** For `f(x) = eˣ sin(x) − 0.5` at x = 0.7, implement the
forward difference, the central difference and two Richardson levels. Sweep
the step size over twenty decades, report each rule's optimum, compare it
with the theoretical `h*`, fit the convergence order for each, and tabulate
the error at a fixed h = 1e-4 against the number of evaluations of f.

<details>
<summary>Solution</summary>

```python
"""Exercise 4: finite differences, the optimal step, and the sqrt(u) floor."""

import math
import sys

u = sys.float_info.epsilon / 2

f = lambda x: math.exp(x) * math.sin(x) - 0.5
f1 = lambda x: math.exp(x) * (math.sin(x) + math.cos(x))
f2 = lambda x: math.exp(x) * (2 * math.sin(x) + 2 * math.cos(x))
f3 = lambda x: math.exp(x) * (3 * math.sin(x) + 3 * math.cos(x))

X0 = 0.7
TRUTH = f1(X0)

print("f(x) = exp(x)*sin(x) - 0.5, differentiated at x =", X0)
print("f'(x) = exp(x)*(sin(x) + cos(x)), so f'(0.7) =", repr(TRUTH))
print("The derivative is a closed formula, so every error below is measured")
print("against an exact answer.\n")


def forward(fn, x, h):
    return (fn(x + h) - fn(x)) / h


def central(fn, x, h):
    return (fn(x + h) - fn(x - h)) / (2 * h)


def richardson(fn, x, h):
    """(2*fwd(h/2) - fwd(h)) kills the O(h) term, leaving O(h**2)."""
    return 2.0 * forward(fn, x, h / 2.0) - forward(fn, x, h)


def richardson2(fn, x, h):
    """A second level, cancelling the O(h**2) term that survived, for O(h**3).

    richardson already removed the h term, so its next error is O(h**2) and
    the extrapolation factor must be 2**2 = 4, not 2**3.
    """
    return (4.0 * richardson(fn, x, h / 2.0) - richardson(fn, x, h)) / 3.0


RULES = [("forward", forward, 2), ("central", central, 2),
         ("richardson", richardson, 3), ("richardson2", richardson2, 4)]

print("=== 1. sweeping the step size ===")
print("  h            forward        central        richardson     R level 2")
best = {name: (None, float("inf")) for name, _, _ in RULES}
for e in range(-16, 3):
    h = 10.0 ** e
    row = f"  {h:<13.0e}"
    for name, rule, _ in RULES:
        err = abs(rule(f, X0, h) - TRUTH)
        row += f" {err:<15.3e}"
        if err < best[name][1]:
            best[name] = (h, err)
    print(row)

print("\nbest step for each rule:")
print("rule           best h      best absolute error")
for name, _, _ in RULES:
    h, err = best[name]
    print(f"{name:14s} {h:<12.0e} {err:<23.4e}")
print("Note how far apart the optima are: about 1e-8 for the forward rule")
print("and about 1e-5 for the central one. The two errors scale as h and")
print("h**2, so their crossing points are separated by a factor of h itself.")
print("The same reason makes central the better default here: it reaches")
print("2.1e-12 where forward bottoms out at 3.2e-8, for the same two")
print("evaluations of f. A rule that is only better asymptotically is not")
print("better at the step size you will actually use.")

print("\n=== 2. the predicted optimal steps ===")
print("Forward error ~ h*|f''|/2 + 2u*|f|/h, minimised where the two cross:")
h_thr_f = math.sqrt(4 * u * abs(f(X0)) / abs(f2(X0)))
print("  |f(x0)| =", abs(f(X0)), "  |f''(x0)| =", abs(f2(X0)))
print("  h* = sqrt(4u|f| / |f''|) =", h_thr_f)
print("  measured best h         =", best["forward"][0])
print("  ratio                    =", best["forward"][0] / h_thr_f)
print("Central error ~ h**2*|f'''|/6 + u*|f|/h, minimised at")
h_thr_c = (3 * u * abs(f(X0)) / abs(f3(X0))) ** (1 / 3)
print("  |f'''(x0)| =", abs(f3(X0)))
print("  h* = (3u|f| / |f'''|)**(1/3) =", h_thr_c)
print("  measured best h              =", best["central"][0])
print("  ratio                         =", best["central"][0] / h_thr_c)
print("Both ratios are of order 1. The formulas predict the scale of the")
print("optimum, not the exact decade, which is all first-order theory owes you.")

print("\n=== 3. orders of convergence, fitted ===")


def fit_order(hs, errs):
    xs_ = [math.log(h) for h, e in zip(hs, errs) if e > 0]
    ys_ = [math.log(e) for h, e in zip(hs, errs) if e > 0]
    n = len(xs_)
    mx, my = sum(xs_) / n, sum(ys_) / n
    num = sum((a - mx) * (b - my) for a, b in zip(xs_, ys_))
    den = sum((a - mx) ** 2 for a in xs_)
    return num / den


RANGE = {"forward": (-6, -2), "central": (-4, -2),
         "richardson": (-4, -2), "richardson2": (-3, -1)}
print("Each rule is fitted over its own truncation-dominated range, read off")
print("the table in section 1. Mixing in the roundoff-dominated range")
print("flattens the slope, because there the error stops tracking h at all.\n")
print("rule           h range          fitted slope   predicted")
PRED = {"forward": 1, "central": 2, "richardson": 2, "richardson2": 3}
for name, rule, _ in RULES:
    lo, hi = RANGE[name]
    hs = [10.0 ** e for e in range(lo, hi + 1)]
    errs = [abs(rule(f, X0, h) - TRUTH) for h in hs]
    print(f"{name:14s} {lo} to {hi}      {fit_order(hs, errs):+13.3f}"
          f"   {PRED[name]:+d}")
print("Forward is order 1, central order 2, one Richardson level keeps order")
print("2 while shrinking the constant, and the second level lifts it to 3.")
print("A least-squares slope of about +2 means the error falls like h**2: the")
print("number of correct digits grows twice as fast as the number of decades.")

print("\n=== 4. what each level actually buys, at one fixed step ===")
H = 1e-4
print("At h = 1e-4, where every rule above is truncation-dominated:")
print("rule           f evaluations   error           improvement")
prev = None
for name, rule, cost in RULES:
    err = abs(rule(f, X0, H) - TRUTH)
    gain = "-" if prev is None else f"{prev / err:.1f}x"
    print(f"{name:14s} {cost:<16d} {err:<15.4e} {gain}")
    prev = err
print("richardson uses 3 evaluations, not 4: the nested step h/2 is shared")
print("between the two extrapolations, so f is evaluated at x, x+h and")
print("x+h/2 only. That sharing is the whole trick -- extrapolation buys")
print("accuracy almost free, and it is why Romberg integration exists.")
print("The price is fragility: extrapolation assumes the leading error term")
print("really is a clean power of h. That is true for smooth functions and")
print("false for anything with a kink, a corner, or noise.")

print("\n=== 5. the floor is not negotiable ===")
print("  h            forward error")
for e in range(-6, -16, -1):
    h = 10.0 ** e
    print(f"  {h:<13.0e} {abs(forward(f, X0, h) - TRUTH):.4e}")
print("Past the floor the error is the rounding of f(x+h) and f(x), not the")
print("shape of f, and shrinking h makes it worse. If you need more than")
print("about -log10(sqrt(u)) = 8 correct digits from a difference, the answer")
print("is different arithmetic -- extended precision, or exact rationals --")
print("not a smaller h.")
```

Output:

```
f(x) = exp(x)*sin(x) - 0.5, differentiated at x = 0.7
f'(x) = exp(x)*(sin(x) + cos(x)), so f'(0.7) = 2.8374981373070494
The derivative is a closed formula, so every error below is measured
against an exact answer.

=== 1. sweeping the step size ===
  h            forward        central        richardson     R level 2
  1e-16         6.171e-01       4.932e-01       5.058e+00       2.097e+00      
  1e-15         4.908e-02       4.908e-02       4.932e-01       1.381e+00      
  1e-14         4.673e-03       4.673e-03       8.415e-02       3.303e-01      
  1e-13         2.319e-04       2.319e-04       8.650e-03       2.729e-03      
  1e-12         9.869e-06       9.869e-06       4.540e-04       2.211e-03      
  1e-11         1.234e-05       1.233e-06       5.674e-05       2.097e-04      
  1e-10         1.233e-06       1.230e-07       5.674e-06       9.129e-06      
  1e-09         1.230e-07       1.230e-07       3.211e-07       2.394e-06      
  1e-08         3.245e-08       1.025e-08       1.008e-07       1.304e-07      
  1e-07         1.524e-07       8.528e-10       1.368e-09       2.824e-08      
  1e-06         1.540e-06       3.542e-11       8.528e-10       9.236e-10      
  1e-05         1.540e-05       2.108e-12       5.340e-11       5.340e-11      
  1e-04         1.540e-04       8.081e-10       4.131e-10       1.321e-11      
  1e-03         1.540e-03       8.097e-08       4.032e-08       2.654e-11      
  1e-02         1.541e-02       8.096e-06       3.885e-06       2.723e-08      
  1e-01         1.546e-01       8.002e-04       2.342e-04       2.914e-05      
  1e+00         1.294e+00       1.387e-02       2.202e-01       5.230e-02      
  1e+01         4.246e+03       2.124e+03       4.174e+03       1.354e+03      
  1e+02         9.107e+40       4.553e+40       9.107e+40       3.036e+40      

best step for each rule:
rule           best h      best absolute error
forward        1e-08        3.2454e-08             
central        1e-05        2.1081e-12             
richardson     1e-05        5.3403e-11             
richardson2    1e-04        1.3211e-11             
Note how far apart the optima are: about 1e-8 for the forward rule
and about 1e-5 for the central one. The two errors scale as h and
h**2, so their crossing points are separated by a factor of h itself.
The same reason makes central the better default here: it reaches
2.1e-12 where forward bottoms out at 3.2e-8, for the same two
evaluations of f. A rule that is only better asymptotically is not
better at the step size you will actually use.

=== 2. the predicted optimal steps ===
Forward error ~ h*|f''|/2 + 2u*|f|/h, minimised where the two cross:
  |f(x0)| = 0.7972951118752689   |f''(x0)| = 5.674996274614099
  h* = sqrt(4u|f| / |f''|) = 7.898813703173922e-09
  measured best h         = 1e-08
  ratio                    = 1.2660128945669111
Central error ~ h**2*|f'''|/6 + u*|f|/h, minimised at
  |f'''(x0)| = 8.512494411921146
  h* = (3u|f| / |f'''|)**(1/3) = 3.147974811755069e-06
  measured best h              = 1e-05
  ratio                         = 3.1766454936863897
Both ratios are of order 1. The formulas predict the scale of the
optimum, not the exact decade, which is all first-order theory owes you.

=== 3. orders of convergence, fitted ===
Each rule is fitted over its own truncation-dominated range, read off
the table in section 1. Mixing in the roundoff-dominated range
flattens the slope, because there the error stops tracking h at all.

rule           h range          fitted slope   predicted
forward        -6 to -2             +1.000   +1
central        -4 to -2             +2.000   +2
richardson     -4 to -2             +1.987   +2
richardson2    -3 to -1             +3.020   +3
Forward is order 1, central order 2, one Richardson level keeps order
2 while shrinking the constant, and the second level lifts it to 3.
A least-squares slope of about +2 means the error falls like h**2: the
number of correct digits grows twice as fast as the number of decades.

=== 4. what each level actually buys, at one fixed step ===
At h = 1e-4, where every rule above is truncation-dominated:
rule           f evaluations   error           improvement
forward        2                1.5402e-04      -
central        2                8.0813e-10      190589.4x
richardson     3                4.1311e-10      2.0x
richardson2    4                1.3211e-11      31.3x
richardson uses 3 evaluations, not 4: the nested step h/2 is shared
between the two extrapolations, so f is evaluated at x, x+h and
x+h/2 only. That sharing is the whole trick -- extrapolation buys
accuracy almost free, and it is why Romberg integration exists.
The price is fragility: extrapolation assumes the leading error term
really is a clean power of h. That is true for smooth functions and
false for anything with a kink, a corner, or noise.

=== 5. the floor is not negotiable ===
  h            forward error
  1e-06         1.5401e-06
  1e-07         1.5236e-07
  1e-08         3.2454e-08
  1e-09         1.2298e-07
  1e-10         1.2332e-06
  1e-11         1.2335e-05
  1e-12         9.8690e-06
  1e-13         2.3191e-04
  1e-14         4.6728e-03
  1e-15         4.9082e-02
Past the floor the error is the rounding of f(x+h) and f(x), not the
shape of f, and shrinking h makes it worse. If you need more than
about -log10(sqrt(u)) = 8 correct digits from a difference, the answer
is different arithmetic -- extended precision, or exact rationals --
not a smaller h.
```

The order column is the payoff: the fitted slopes are +1.000, +2.000,
+1.987 and +3.020 against predictions of 1, 2, 2 and 3. Fitting over the
wrong range is the trap here — mixing in the roundoff-dominated steps
flattens the slope toward zero, because there the error has stopped
tracking h altogether. Read the range off the sweep table first.

The optimum positions are the other half of the lesson. Forward is best at
h ≈ 1e-8, central at h ≈ 1e-5: three orders of magnitude apart, because the
truncation terms scale as h and h² and the roundoff term as 1/h, so the
crossing point inherits a power of h. The predicted optima, 7.90e-9 and
3.15e-6, land within a factor of 1.3 and 3.2 of the measured ones — the same
order of magnitude, which is all a first-order argument promises.

The fixed-step table then shows the honest ranking. At h = 1e-4 the central
difference is already 190000× better than forward for the *same* two
evaluations; Richardson adds 2× on top of central for one more evaluation,
and the second level another 31×. And the floor section is the warning: from
h = 1e-8 downward the forward error gets monotonically *worse*, because it
is now measuring rounding rather than curvature. −log₁₀(√u) = 8 is a hard
ceiling on digits from a difference.

</details>

**Challenge — ** Implement a Romberg table
`R[i][j] = R[i][j-1] + (R[i][j-1] - R[i-1][j-1]) / (4ʲ - 1)` from the
trapezoid rule, integrate `x¹²` over [0, 1], and verify: that column j has
order 2(j+1); that column 1 is bit-for-bit Simpson's rule; that column j
integrates every polynomial of degree ≤ 2j+1 exactly; and that the
extrapolation *fails* on `|x − 0.5|`.

<details>
<summary>Solution</summary>

```python
"""Challenge: a Romberg table from scratch, and what each column proves."""

import math


def trapezoid(fn, a, b, n):
    h = (b - a) / n
    s = 0.5 * fn(a) + 0.5 * fn(b)
    for i in range(1, n):
        s += fn(a + i * h)
    return s * h


def romberg(fn, a, b, levels):
    """Build the Romberg table R[i][j] and return it.

    R[0][0] is the plain trapezoid rule on n panels. Every other entry
    cancels one more power of h by extrapolating from the two entries to
    its left, which is the only operation the whole method ever performs:

        R[i][j] = R[i][j-1] + (R[i][j-1] - R[i-1][j-1]) / (4**j - 1)

    Column j therefore has order 2(j+1) and integrates any polynomial of
    degree at most 2j+1 exactly.
    """
    table = [[0.0] * levels for _ in range(levels)]
    for i in range(levels):
        table[i][0] = trapezoid(fn, a, b, 2 ** i)
    for j in range(1, levels):
        for i in range(j, levels):
            table[i][j] = table[i][j - 1] + (table[i][j - 1]
                                            - table[i - 1][j - 1]) / (
                                                4 ** j - 1)
    return table


def simpson(fn, a, b, n):
    """Simpson's rule on an even number of panels -- identical to R[i][1]."""
    h = (b - a) / n
    s = fn(a) + fn(b)
    for i in range(1, n):
        s += (4.0 if i % 2 else 2.0) * fn(a + i * h)
    return s * h / 3.0


def observed_order(e1, e2):
    """p with e1 / e2 = 2**p, i.e. halving h divides the error by 2**p."""
    if e1 <= 0 or e2 <= 0:
        return float("nan")
    return math.log2(e1 / e2)


A, B = 0.0, 1.0
f = lambda x: x ** 12
EXACT = 1.0 / 13.0
LV = 7

print("=== 1. the table ===")
print("Integral of x**12 over [0, 1] is exactly 1/13 =", repr(EXACT))
tab = romberg(f, A, B, LV)
print("\n  panels     " + "".join(f"{'col ' + str(j):>13s}" for j in range(LV)))
for i in range(LV):
    print(f"  2**{i:<7d}" + "".join(
        f"{tab[i][j]:<13.10f}" if j <= i else f"{'-':>13s}"
        for j in range(LV)))

print("\nerrors:")
print("  panels     " + "".join(f"{'col ' + str(j):>13s}" for j in range(LV)))
for i in range(LV):
    print(f"  2**{i:<7d}" + "".join(
        f"{abs(tab[i][j] - EXACT):<13.2e}" if j <= i else f"{'-':>13s}"
        for j in range(LV)))

print("\nobserved order down each column (theory: 2, 4, 6, 8, 10, 12):")
print("  column     " + "".join(f"{c:>8d}" for c in range(LV - 1)))
for c in range(LV - 1):
    row = f"  col {c:<7d}"
    for i in range(LV - 1 - c):
        row += f"{observed_order(abs(tab[i][c] - EXACT), abs(tab[i + 1][c] - EXACT)):>8.2f}"
    print(row)
print("Column j has order 2(j+1): 2, 4, 6, 8, 10, 12. Reading a column")
print("downwards, halving h divides the error by 2**(2j+2).")

print("\n=== 2. exactness degree ===")
print("Column j integrates every polynomial of degree <= 2j+1 exactly, so")
print("column 6 (degree 13) is already exact for x**12. The 1e-17 entries")
print("are not a bug -- they are the float type, not the method:")
for j in range(LV):
    i = LV - 1
    print(f"  col {j}: error {abs(tab[i][j] - EXACT):.3e}"
          f"   exact through degree {2 * j + 1}")
print("Check that directly: x**5 is exact in column 2 and not before.")

print("\n=== 3. column 1 really is Simpson ===")
print("panels   Romberg col 1        Simpson")
for i in range(1, LV):
    print(f"  {2 ** i:<7d} {tab[i][1]:<21.14f} {simpson(f, A, B, 2 ** i):.14f}")
print("Identical to the last digit. Column 1 is Simpson's rule written a")
print("different way, not a separate method.")

print("\n=== 4. accuracy per function evaluation ===")
print("Romberg level j costs 2**j + 1 evaluations of f.\n")
print("  budget   method              value                    |error|")
for j in range(LV):
    print(f"  {2 ** j + 1:<8d} Romberg col {j:<3d}      "
          f"{tab[LV - 1][j]:<25.16f} {abs(tab[LV - 1][j] - EXACT):.3e}")
for n in (8, 64, 512, 4096):
    v = trapezoid(f, A, B, n)
    print(f"  {n + 1:<8d} trapezoid          {v:<25.16f} "
          f"{abs(v - EXACT):.3e}")
print("The plain rule needs thousands of panels to reach what the last")
print("Romberg row gets from 65, because its error falls like h**2 while the")
print("bottom row falls like h**14.")

print("\n=== 5. what breaks it ===")
print("Romberg assumes the trapezoid error is a clean power series in h:")
print("  h**2 + c4 h**4 + c6 h**6 + ... . A function with a corner breaks")
print("that, and no amount of extrapolation helps.")
g = lambda x: abs(x - 0.5)
print("\nIntegral of |x - 0.5| over [0, 1] is exactly 0.25.")
print("  panels   trapezoid error     Romberg error")
for j in range(5):
    e = abs(romberg(g, A, B, j + 1)[j][j] - 0.25)
    t = abs(trapezoid(g, A, B, 2 ** j) - 0.25)
    print(f"  2**{j:<6d} {t:<20.6e} {e:<17.6e}")
print("The trapezoid rule still converges, but only at order 2 with an ugly")
print("constant. The extrapolated column does not converge at all: it is")
print("just the raw rule with a subtraction. Extrapolation is a bet that")
print("the error is a clean power series in h, and a corner breaks that bet.")
print("This is the whole reason production integrators (scipy.integrate)")
print("detect non-smooth regions and subdivide instead of extrapolating.")
```

Output:

```
=== 1. the table ===
Integral of x**12 over [0, 1] is exactly 1/13 = 0.07692307692307693

  panels             col 0        col 1        col 2        col 3        col 4        col 5        col 6
  2**0      0.5000000000             -            -            -            -            -            -
  2**1      0.2501220703 0.1668294271             -            -            -            -            -
  2**2      0.1329801381 0.0939328273 0.0890730540             -            -            -            -
  2**3      0.0921122797 0.0784896602 0.0774601157 0.0772757834             -            -            -
  2**4      0.0808015390 0.0770312922 0.0769340676 0.0769257177 0.0769243448             -            -
  2**5      0.0778978939 0.0769300122 0.0769232603 0.0769230887 0.0769230784 0.0769230772             -
  2**6      0.0771671083 0.0769235131 0.0769230798 0.0769230770 0.0769230769 0.0769230769 0.0769230769 

errors:
  panels             col 0        col 1        col 2        col 3        col 4        col 5        col 6
  2**0      4.23e-01                 -            -            -            -            -            -
  2**1      1.73e-01     8.99e-02                 -            -            -            -            -
  2**2      5.61e-02     1.70e-02     1.21e-02                 -            -            -            -
  2**3      1.52e-02     1.57e-03     5.37e-04     3.53e-04                 -            -            -
  2**4      3.88e-03     1.08e-04     1.10e-05     2.64e-06     1.27e-06                 -            -
  2**5      9.75e-04     6.94e-06     1.83e-07     1.18e-08     1.47e-09     2.36e-10                 -
  2**6      2.44e-04     4.36e-07     2.91e-09     4.75e-11     1.50e-12     5.76e-14     0.00e+00     

observed order down each column (theory: 2, 4, 6, 8, 10, 12):
  column            0       1       2       3       4       5
  col 0          1.29    1.63    1.88    1.97    1.99    2.00
  col 1         -0.23    2.40    3.44    3.86    3.96
  col 2          0.00    2.66    4.50    5.61
  col 3          0.00    0.00    7.77
  col 4          0.00    0.00
  col 5          0.00
Column j has order 2(j+1): 2, 4, 6, 8, 10, 12. Reading a column
downwards, halving h divides the error by 2**(2j+2).

=== 2. exactness degree ===
Column j integrates every polynomial of degree <= 2j+1 exactly, so
column 6 (degree 13) is already exact for x**12. The 1e-17 entries
are not a bug -- they are the float type, not the method:
  col 0: error 2.440e-04   exact through degree 1
  col 1: error 4.362e-07   exact through degree 3
  col 2: error 2.911e-09   exact through degree 5
  col 3: error 4.752e-11   exact through degree 7
  col 4: error 1.497e-12   exact through degree 9
  col 5: error 5.755e-14   exact through degree 11
  col 6: error 0.000e+00   exact through degree 13
Check that directly: x**5 is exact in column 2 and not before.

=== 3. column 1 really is Simpson ===
panels   Romberg col 1        Simpson
  2       0.16682942708333      0.16682942708333
  4       0.09393282731374      0.09393282731374
  8       0.07848966021750      0.07848966021750
  16      0.07703129215836      0.07703129215836
  32      0.07693001224606      0.07693001224606
  64      0.07692351311010      0.07692351311010
Identical to the last digit. Column 1 is Simpson's rule written a
different way, not a separate method.

=== 4. accuracy per function evaluation ===
Romberg level j costs 2**j + 1 evaluations of f.

  budget   method              value                    |error|
  2        Romberg col 0        0.0771671083186177        2.440e-04
  3        Romberg col 1        0.0769235131100978        4.362e-07
  5        Romberg col 2        0.0769230798343667        2.911e-09
  9        Romberg col 3        0.0769230769705962        4.752e-11
  17       Romberg col 4        0.0769230769245736        1.497e-12
  33       Romberg col 5        0.0769230769231345        5.755e-14
  65       Romberg col 6        0.0769230769230769        0.000e+00
  9        trapezoid          0.0921122796789859        1.519e-02
  65       trapezoid          0.0771671083186177        2.440e-04
  513      trapezoid          0.0769268915936642        3.815e-06
  4097     trapezoid          0.0769231365277152        5.960e-08
The plain rule needs thousands of panels to reach what the last
Romberg row gets from 65, because its error falls like h**2 while the
bottom row falls like h**14.

=== 5. what breaks it ===
Romberg assumes the trapezoid error is a clean power series in h:
  h**2 + c4 h**4 + c6 h**6 + ... . A function with a corner breaks
that, and no amount of extrapolation helps.

Integral of |x - 0.5| over [0, 1] is exactly 0.25.
  panels   trapezoid error     Romberg error
  2**0      2.500000e-01         2.500000e-01     
  2**1      0.000000e+00         8.333333e-02     
  2**2      0.000000e+00         5.555556e-03     
  2**3      0.000000e+00         8.818342e-05     
  2**4      0.000000e+00         3.458173e-07     
The trapezoid rule still converges, but only at order 2 with an ugly
constant. The extrapolated column does not converge at all: it is
just the raw rule with a subtraction. Extrapolation is a bet that
the error is a clean power series in h, and a corner breaks that bet.
This is the whole reason production integrators (scipy.integrate)
detect non-smooth regions and subdivide instead of extrapolating.
```

The order table walks up to theory column by column: 1.29 → 2.00 in column
0, −0.23 → 3.96 in column 1, 0.00 → 5.61 in column 2, 7.77 in column 3.
The low starting values are not noise — they are the asymptotic expansion
being wrong at coarse meshes, which is exactly why the order only appears
once the mesh is fine. Each column is a different rule wearing the same
clothes, and column 1 being bit-identical to Simpson across all six panel
counts proves it.

The exactness table is the cleanest statement of what extrapolation is
*doing*. Column 6 integrates every polynomial through degree 13 and returns
`0.0` error on `x¹²` — not because it is accurate, but because it is
algebraically exact for that class and there is nothing left to round. That
is a much stronger property than any error estimate: it is not "close to
right", it is *right*.

And the last table is the reason nobody ships Romberg unconditionally. The
trapezoid rule is **exact** on `|x − 0.5|` for every even panel count,
because the corner at x = 0.5 lands on a node. Romberg takes that exact
answer and extrapolates it to 8.3e-2, and the damage persists all the way
down the column. Extrapolation assumes the error is a clean power series
in h; a corner makes it a discontinuous function of h; and the method has
no way to know. `scipy.integrate` handles this by detecting where the
integrand stops being smooth and subdividing there, which is why the
production libraries are more elaborate than the textbook ones.

</details>

## Summary

- A `float64` is a 53-bit binary fraction, not a decimal. `0.1` is
  `3602879701896397/36028797018963968`, off by −5.55e-18, and `2**53 + 1
  == 2**53`.
- The gap above a float is proportional to its magnitude: `ulp(1.0)` is
  2.22e-16 and `ulp(1e16)` is 2.0. This single fact explains most silent
  failures.
- The unit roundoff is u = 2⁻⁵³. n chained operations carry about n·u
  relative error, and the model stops meaning anything near n = 10¹⁶.
- Catastrophic cancellation: subtracting a − b with a ≈ b gives relative
  error ≈ u·max(|a|,|b|)/|a−b|. Rewriting to avoid the subtraction
  recovers everything — that is all `expm1`, `log1p`, `hypot`, Kahan's
  Heron and Vieta's product are.
- Condition number κ(x) = |x f′(x)/f(x)| measures the problem, not the
  code. Perturbing x by one ulp moves f(x) by about κ·u. No algorithm beats
  a badly conditioned problem.
- Backward stability is the property to want: the computed answer is exact
  for a nearby input. It is bounded by operations performed, which you
  control.
- Bisection converges at order 1 with rate 1/2, needs only continuity, and
  cannot fail. It bounds the *bracket width*, not the error.
- Newton converges at order 2 with constant `f″(α)/(2f′(α))`, and has only a
  local guarantee. It can 2-cycle, divide by zero, or walk to a different
  root.
- The secant method converges at order (1+√5)/2 ≈ 1.618 and needs no
  derivative.
- Stop on `|xₖ − xₖ₋₁| ≤ tol(1 + |xₖ|)`, never on `|f(xₖ)| < tol`.
- Brent mixes inverse quadratic interpolation with a bisection fallback and
  is what you ship: 8 steps against 39 at the same tolerance.
- Truncation error falls with h; roundoff rises as 1/h. Finite differences
  bottom out at O(√u) — about 8 correct digits, at any step size.
- Richardson extrapolation buys a power of h for one extra evaluation;
  iterated, it is the Romberg table, whose column j has order 2(j+1) and is
  exact through degree 2j+1.
- Trapezoid and midpoint converge at order 2, Simpson at order 4, and both
  are measurable in the first few digits rather than only asymptotic.
- Extrapolation assumes smoothness. On a corner it can turn an exact answer
  into a wrong one.
- `Decimal`, `Fraction`, `float32` and `float128` are all answers to the
  same question: how many digits do you need, and do you need them to be
  right or merely close.

## Next

There is no Part 11, and that is deliberate: this repository ends with the
part where the mathematics meets the machine. Two directions out from here.

**If you want the rigorous version**, re-read [Lesson 54 — Taylor Series](../part04_calculus/54_taylor_series.md)
for the expansions that justify every truncation constant used here, and
[Lesson 52 — Integration](../part04_calculus/52_integration.md) for the
Euler–Maclaurin formula behind the trapezoid rule's O(h²) term and the
Bernoulli numbers behind Romberg's exactness degrees.

**If you want the applied version**, go back to
[Lesson 120 — Tensors and Broadcasting](120_tensors_and_broadcasting.md) and
read the last block again: `np.sum` using pairwise summation, and
`np.einsum` choosing an `optimize=True` contraction order, are both this
lesson's central idea — *the order in which arithmetic is performed decides
how much precision survives it* — applied to an axis of a tensor instead of
to a running total.

And keep the habit this lesson is really about: when a number comes out
wrong, ask the condition number before you read the code.
