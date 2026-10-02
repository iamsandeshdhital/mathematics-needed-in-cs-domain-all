# 121 — Numerical Methods and Floating Point

**Part**: part10_tensors_numerical · **Prerequisites**: 113 · **Time**: 30 min

---

## In Plain Words

Everything so far in this repository was done with exact mathematics: integers
never lose precision, and a conclusion that follows from the premises is
unarguable. This lesson is about the day your answers stop being exact. A
computer stores most real numbers as a long string of ones and zeros in a
fixed number of bits, so most real numbers simply cannot be stored, and the
ones that can be stored are the only ones available. Every calculation after
that is a real calculation with a small amount of noise added, and the skill
this lesson teaches is telling how much noise, and where it comes from.

Three ideas carry the whole lesson. First, some questions are fragile in a way
that no amount of care can fix, usually because the answer you want is a tiny
difference between two huge numbers. Second, some questions are fragile because
of how you wrote them down, and those you can rewrite until they are not.
Third, even a perfect algorithm will not rescue you on a question that was
fragile to begin with, and knowing which kind of fragility you are looking at
is most of the diagnosis.

## Why Computer Science Cares

- **`0.1 + 0.2 != 0.3` is in every language.** It is not a bug in Python, it is
  a fact about binary. Anyone who writes a test with `assert a + b == c` on
  floating-point values will eventually ship that failure. The correct response
  is a scaled comparison or an exact type, and the reasoning is in this lesson.
- **Money.** Storing an amount as a float and adding it up accumulates error
  until a reconciliation fails and nobody can explain why. Integer cents, or
  `decimal.Decimal`, is the answer, and the reason why is the first section.
- **`np.linalg.solve` versus `np.linalg.lstsq`.** The first is fast and breaks on
  near-singular matrices; the second is slower and returns a stable, biased
  answer. The condition number is what tells you which one you need, and
  Lesson 101's regularisation is what fixes the problem.
- **Simulators, games and physics engines.** Fixed timestep integration with
  `dt = 0.001` is a claim that your error is small. Whether it is depends on
  how stiff your equations are, and the answer is a step size, not a wish.
- **Convergence tests in optimisation.** A gradient descent that stops when the
  loss changes by less than `1e-9` can stop on a plateau or in a region where
  the loss has stopped responding to the parameters at all. The condition
  number of your problem is why, and it decides whether more iterations or more
  precision can possibly help.
- **`scipy.optimize.brentq` versus a hand-rolled Newton loop.** Brent's method
  is a bisection skeleton with Newton accelerants, and that specific shape
  exists because Newton alone cycles. This lesson builds both and shows the
  cycle.

## The Formal Version

Notation follows [SYMBOLS.md](../SYMBOLS.md). Used here: $\varepsilon$, $O()$,
$h$, $n$, $\kappa$, $|x|$, $\delta$.

**Definition.** A **float64** is a float64 is a 64-bit encoding of

$$x = (-1)^s \cdot (1 + f) \cdot 2^{e - 1023}$$

with a 1-bit sign $s$, an 11-bit exponent $e$, and a 52-bit fraction $f$ taken
as an integer in $[0, 2^{52})$. Equivalently, every non-negative float64 is
exactly $m \cdot 2^j$ for integers $m < 2^{53}$ and $j$.

**Definition.** The **unit in the last place** (ulp) at $x > 0$ is
$\operatorname{ulp}(x) = 2^{j-52}$ where $x = m 2^j$ with $m$ odd. It is the gap
to the next float up.

**Definition.** **Machine epsilon** for float64 is
$\varepsilon = 2^{-52} \approx 2.22 \times 10^{-16}$, the ulp at $1.0$ and also
the smallest $h$ for which $1 + h \neq 1$ up to the rounding tie.

**Theorem (representable decimals).** A decimal $d = p/q$ in lowest terms is
exactly representable in binary floating point **iff** $q$ is a power of two.
Hence $1/2, 1/4, 1/8$ are exact and $1/10, 1/5, 3/10$ are not.

*Explanation.* A float64 is $m 2^j$, so its reduced denominator is a power of
two. $1/10 = 1/(2 \cdot 5)$ has a factor of 5, which no power of two absorbs. ∎

**Definition.** The **absolute error** of $\hat{x}$ for exact $x$ is
$|\hat{x} - x|$. The **relative error** is $|\hat{x} - x| / |x|$.

**Definition.** **Cancellation** occurs when a formula subtracts two quantities
of similar magnitude to produce a much smaller result, so the absolute error of
the operands becomes a large relative error of the output.

**Definition.** The **condition number** of a function at $x$ is
$\kappa(x) = |x f'(x)| / |f(x)|$. It is the factor by which a relative input
error is amplified into a relative output error, to first order. For a linear
system it is $\operatorname{cond}(A)$, the ratio of largest to smallest
singular value.

**Theorem (error amplification).** If the relative input error is $\le \delta$
then the relative output error is $\approx \kappa \delta$, and this is
asymptotically tight. $\kappa$ is a property of the problem and does not depend
on the algorithm.

**Theorem (error bound for bisection).** If $f$ is continuous, $f(a)f(b) < 0$,
and the bracket $[a_n, b_n]$ has width $w$, then after $n$ halvings
$w_n = w / 2^n$ and the returned midpoint is within $w / 2^{n+1}$ of the root.

**Definition.** Newton's iteration is $x_{n+1} = x_n - f(x_n)/f'(x_n)$. It is
**quadratically convergent** near a root: the number of correct digits roughly
doubles per iteration. It is **linearly convergent** for bisection.

**Definition.** A forward difference $D^+f(x) = (f(x+h) - f(x))/h$ has
truncation error $O(h)$; a central difference
$Df(x) = (f(x+h) - f(x-h))/(2h)$ has truncation error $O(h^2)$.

**Theorem (the step-size optimum).** The total error of a finite difference is
truncation plus rounding, roughly

$$\text{forward: } C_1 h + \frac{2\varepsilon |f|}{h},
\qquad \text{central: } C_2 h^2 + \frac{2\varepsilon |f|}{h}.$$

The first term falls with $h$ and the second rises with $h$, so the optimum is
where they balance:

$$h^*_{\text{forward}} = \sqrt{\frac{2\varepsilon |f|}{|f''|}},
\qquad h^*_{\text{central}} = \left(\frac{3\varepsilon |f|}{|f'''|}\right)^{{1/3}}.$$

Choosing $h$ smaller than $h^*$ makes the answer strictly worse, because
$f(x+h)$ rounds back to $f(x)$ and the numerator is zero.

*Explanation.* The Taylor expansion gives the $C_1 h$ and $C_2 h^2$ terms; each
of $f(x+h)$ and $f(x-h)$ carries a rounding error of order $\varepsilon |f|$,
so their difference carries order $2 \varepsilon |f|$, and dividing by $h$
turns that into $2\varepsilon|f|/h$. Setting the derivative of the sum to zero
gives the two formulas. The central optimum is a cube root against a square
root, so it is about 1000 times larger for the same function, and the best
attainable relative accuracy is about $\varepsilon^{2/3} \approx 3.7 \times
10^{-11}$ -- eleven digits, not sixteen. ∎

## Formula Sheet

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| float64 value | `$x = (-1)^s (1 + f) 2^{e-1023}$` | sign, times 11 exponent bits, times 52 fraction bits | understanding what can and cannot be stored |
| machine epsilon | `$\varepsilon = 2^{-52} \approx 2.22\times10^{-16}$` | the gap between 1.0 and the next double | every error estimate; `sys.float_info.epsilon` |
| ulp at $x$ | `$\operatorname{ulp}(x) = 2^{j-52}$`, $x = m2^j$, $m$ odd | how far to the next float from $x$ | asking "is this step even representable?" |
| representable decimals | $d = p/q$ exact **iff** $q$ is a power of two | only binary fractions are exact | why 0.1 is not 0.1 |
| absolute error | `$|\hat{x} - x|$` | how far off, in these units | physical quantities with a fixed scale |
| relative error | `$\lvert \hat{x}-x\rvert / \lvert x\rvert$` | how far off compared to the target | unit-free quantities, computed values |
| condition number | `$\kappa(x) = \lvert x f'(x)\rvert / \lvert f(x)\rvert$` | input error is amplified by this factor | deciding whether a problem is solvable at all |
| matrix condition number | `$\operatorname{cond}(A) = \sigma_{max}/\sigma_{min}$` | largest vs smallest singular value | `np.linalg.cond`; choosing solve vs lstsq |
| digits lost | `$\approx \log_{10}\kappa$` | each factor of 10 in kappa costs a digit | "will float64 be enough here?" |
| error amplification | relative error out $\approx \kappa \cdot$ relative error in | the problem decides, not your code | diagnosing a wrong answer |
| stable $\sqrt{x^2+1}-x$ | `$\dfrac{1}{\sqrt{x^2+1}+x}$` | the same number, no subtraction | the canonical cancellation repair |
| error of a long sum | `$\approx n\varepsilon/2$` | $n$ additions cost about $n\varepsilon/2$ relative | `math.fsum`, pairwise summation |
| bisection width after $n$ | `$w_n = w/2^n$` | halving every step | predicting iteration counts |
| bisection error | `$\lvert x_n - r\rvert \le w/2^{n+1}$` | the guarantee | choosing a tolerance |
| Newton iteration | `$x_{n+1} = x_n - f(x_n)/f'(x_n)$` | follow the tangent to the axis | fast roots where you have a derivative |
| Newton convergence | quadratic: digits double per step | about 4-5 iterations for float64 | when the start is close |
| forward difference | `$D^+ = \dfrac{f(x+h)-f(x)}{h}$`, error $O(h)$ | one extra evaluation | boundary cases, cheapness |
| central difference | `$D = \dfrac{f(x+h)-f(x-h)}{2h}$`, error $O(h^2)$ | two extra evaluations | accuracy, when you can go both ways |
| optimal step, forward | `$h^* = \sqrt{2\varepsilon\lvert f\rvert/\lvert f''\rvert}$` | balance truncation against rounding | choosing a step |
| optimal step, central | `$h^* = (3\varepsilon\lvert f\rvert/\lvert f'''\rvert)^{1/3}$` | the cube-root rule | choosing a step, no derivatives known |
| practical step rule | `$h \approx \varepsilon^{1/3}\lvert f(x)\rvert \approx 6\times10^{-6}$` | usable with no derivative at all | shipping a derivative routine |
| central-difference ceiling | `$\varepsilon^{2/3} \approx 3.7\times10^{-11}$` | about 11 digits is all you get | when a caller wants more, change method |
| complex-step derivative | `$f'(x) = \operatorname{Im}(f(x+ih))/h$` | no subtraction, so no cancellation | beating the 11-digit ceiling |
| convergence test | `$\lvert f(x)/f'(x)\rvert < \tau\max(1,\lvert x\rvert)$` | estimated distance to the root | scale-invariant stopping rule |
| Simpson error | `$O(h^4) = O(1/n^4)$` | four orders in panel count | smooth integrands |
| Richardson comparison | compare $n$ panels against $2n$ | trust agreement, not theory | picking $n$ honestly |

Three restrictions to carry. The definitions of $\varepsilon$ and ulp are for
float64 specifically; float32 has $\varepsilon = 2^{-23}$, which is why a GPU
default is about a thousand times coarser. The condition number measures
sensitivity to **input** error and says nothing about whether your algorithm is
stable, which is a separate and often more important question. And every error
formula here assumes the arithmetic was well conditioned; a single badly chosen
subtraction destroys all of them at once.

## Worked Example

The smallest interesting example in the repository: **why
$0.1 + 0.2 \neq 0.3$**, done exactly.

**Step 1. Establish what the machine stores.** Both $1/10$ and $1/5$ have a
factor of 5 in their denominator, so by the theorem above neither is
representable. Each is rounded to the nearest double when written. The stored
values, computed with `fractions.Fraction`, are

$$\mathrm{fl}(0.1) = \frac{3602879701896397}{36028797018963968},
\qquad \mathrm{fl}(0.2) = \frac{3602879701896397}{18014398509481984}.$$

**Step 2. Check the direction of the error.** Both fractions are *above* their
true values: $\mathrm{fl}(0.1) > 1/10$ and $\mathrm{fl}(0.2) > 1/5$. This
matters, because it means the sum will be too large.

**Step 3. Add, exactly.** Using a common denominator $2^{55}$,

$$\mathrm{fl}(0.1) + \mathrm{fl}(0.2)
  = \frac{10808639105689191}{36028797018963968}
  = \frac{3}{10} + 1.665 \times 10^{-17}.$$

This addition is **exact**: the sum has a denominator of $2^{55}$, so it is a
representable double. No error is introduced here. This is the step everyone
gets wrong -- floating-point addition is correctly rounded, so $a + b$ is the
correctly rounded value of the two stored numbers.

**Step 4. Compare against the other route.** Writing the literal `0.3` rounds
$3/10$ once, to $\frac{5404319552844595}{18014398509481984}$, which is
*below* $3/10$. The literal and the sum round in opposite directions.

**Step 5. Conclude.** The two results are one ulp apart:

$$\mathrm{fl}(0.1) + \mathrm{fl}(0.2) = 0.30000000000000004 \neq 0.3,$$

and they differ by $5.55 \times 10^{-17}$. Three roundings happened along
three different routes: two on the way in, one on the sum, and one on the
literal. Rounding once, at the end, would have given a different and more
accurate answer.

**Step 6. Sanity check that settles it.** $0.1 + 0.5 = 0.6$ **exactly**, because
$1/2$ is representable, so only one rounding is involved on its side and the
two errors cancel. If the story were "floating point addition is broken", this
case would also fail. It does not.

The lesson generalises past this example. Any subtraction of two nearly equal
quantities amplifies the operands' errors by the ratio of the operand size to
the answer size. That single mechanism explains `exp(x) - 1` for small `x`, the
quadratic formula's small root, and `sqrt(x*x + 1) - x` at large `x` -- and all
three are repaired the same way, by rewriting the algebra so nothing is
subtracted.

## Runnable Code

### 1. IEEE 754, machine epsilon, and the addition that does not add up

```python
```python
"""IEEE 754 and why 0.1 + 0.2 != 0.3.

Binary floating point stores a sign, an exponent and a mantissa.  For a
double-precision float the 64 bits are

    1 sign bit | 11 exponent bits | 52 fraction bits

Normalised, the value is  (-1)^sign * 1.fraction * 2^(exponent - 1023), so the
smallest amount you can add to 1.0 and get a different number is 2^-52, about
2.22e-16.  That is machine epsilon for float64.

Every non-negative float64 is a binary fraction k / 2^52, so "is 0.1 exactly
representable?" is really "is 0.1 = k / 2^52 for some integer k?"  It is not:
1/10 has a factor of 5 in the denominator and no power of two absorbs it.
Exactly representable decimals are only the ones whose reduced denominator is a
power of two -- 0.5, 0.25, 0.125, 0.0625.

Use fractions.Fraction for the exact reasoning below.  A float64 is always
exactly a rational, so Fraction(0.1) tells you what the machine actually holds.
"""

import math
import struct
from fractions import Fraction


def bits(x):
    """The 64 bits of a float64, as a string of 0s and 1s."""
    (packed,) = struct.unpack("<Q", struct.pack("<d", x))
    return f"{packed:064b}"


def binary_expansion(x, places=60):
    """The binary expansion of a positive float, by repeated doubling."""
    frac, digits = x, ""
    for _ in range(places):
        frac *= 2
        if frac >= 1.0:
            digits += "1"
            frac -= 1.0
        else:
            digits += "0"
        if frac == 0.0:
            break
    return "0." + digits


def rule(title):
    print()
    print("=" * 68)
    print(title)
    print("=" * 68)


# ---------------------------------------------------------------- 1. epsilon
rule("1. Machine epsilon: the gap between 1.0 and the number just above it")

EPS = 2.0**-52
print(f"2^-52                   = {EPS!r}")
print(f"1.0 + that              = {1.0 + EPS!r}")
print(f"1.0 + that == 1.0       = {1.0 + EPS == 1.0}")
print(f"math.nextafter(1.0, 2.0) = {math.nextafter(1.0, 2.0)!r}")
print(f"the two agree           = {1.0 + EPS == math.nextafter(1.0, 2.0)}")
print(f"math.ulp(1.0)           = {math.ulp(1.0)!r}")
print()
print("Epsilon is NOT the smallest number you can store.  It is the smallest")
print("amount that changes 1.0.  The smallest positive float64 is the denormal")
print(f"2^-1074 = {2.0**-1074!r}, which is 2^-1022 times smaller than epsilon")
print("and about 300 orders of magnitude below it.  'How small can a float be'")
print("and 'how much can I add before something changes' are different")
print(f"questions.  The smallest NORMAL float is 2^-1022 = {2.0**-1022!r},")
print(f"and math.ulp(0.0) returns {math.ulp(0.0)!r}.")
print()
print("float32, the default on most GPUs, is far coarser:")
print(f"   its epsilon is 2^-23 = {2.0**-23!r}")
print(f"   0.1 as float32          = "
      f"{struct.unpack('<f', struct.pack('<f', 0.1))[0]!r}")
print("   0.1 as float64          = 0.1")
print("   That is roughly 1 part in a million of error before you start, and")
print("   it is why GPU training uses float32 for speed and float64 for the")
print("   quantities that have to be right.")

# ------------------------------------------------------------- 2. exactness
rule("2. Which decimals are exact, and why 0.1 is not one of them")

print("`exact` means Fraction(the float) equals the intended rational exactly:")
print(f"   {'decimal':<10} {'rational':<10} {'exact?':<8} the stored double")
for name, exact in [("0.5", Fraction(1, 2)), ("0.25", Fraction(1, 4)),
                    ("0.125", Fraction(1, 8)), ("0.0625", Fraction(1, 16)),
                    ("0.1", Fraction(1, 10)), ("0.2", Fraction(1, 5)),
                    ("0.3", Fraction(3, 10)), ("0.7", Fraction(7, 10))]:
    value = float(exact)
    print(f"   {name:<10} {str(exact):<10} "
          f"{str(Fraction(value) == exact):<8} {value!r}")
print()
print("0.5, 0.25, 0.125 and 0.0625 have power-of-two denominators, so they are")
print("binary fractions and survive exactly.  0.1 = 1/10 has a factor of 5 in")
print("the denominator and nothing binary can hold it.  Same for 0.2, 0.3, 0.7.")
print("That is the entire story behind the famous example.")
print()

# --------------------------------------------------------- 3. binary digits
rule("3. The binary expansions, so you can see it")

for name, x in [("0.5", 0.5), ("0.1", 0.1), ("0.2", 0.2), ("0.3", 0.3)]:
    digits = binary_expansion(x)
    head, tail = digits[:10], digits[10:]
    terminated = not tail or tail.strip("0") == ""
    print(f"{name}  ->  {head}{'' if terminated else tail + '... (never stops)'}")
print()
print("0.5 is 0.1 in binary and stops.  0.1 in binary is the repeating block")
print("0011 0011 0011 ..., because 1/10 = 1/8 * 0.8 and 0.8 is not a binary")
print("fraction.  The stored value is the expansion cut off after 52 fraction")
print("bits and rounded.")
print(f"   0.1 is stored as {bits(0.1)}")
print(f"   0.5 is stored as {bits(0.5)}")
print("   the tail of 0.1's pattern repeats forever; 0.5 is all zeros after the")
print("   leading 1.")
print()

# ----------------------------------------------------------- 4. the addition
rule("4. The addition, in exact arithmetic")

a, b, c = 0.1, 0.2, 0.3
fa, fb = Fraction(a), Fraction(b)
tenth, fifth, three_tenths = Fraction(1, 10), Fraction(1, 5), Fraction(3, 10)

print(f"0.1 + 0.2 in Python       = {a + b!r}")
print(f"0.3 in Python             = {c!r}")
print(f"equal?                    = {a + b == c}")
print(f"they differ by            = {abs((a + b) - c)!r}")
print(f"as a fraction of 0.3      = {abs((a + b) - c) / c!r}")
print()
print("Now the exact reasoning, using rationals so there is no rounding at all:")
print(f"   what the machine stores for 0.1 = {fa}")
print(f"   what the machine stores for 0.2 = {fb}")
print(f"   is stored 0.1 equal to 1/10?   = {fa == tenth}")
print(f"   is stored 0.2 equal to 1/5?    = {fb == fifth}")
print(f"   stored 0.1 is above 1/10       = {fa > tenth}")
print(f"   stored 0.2 is above 1/5        = {fb > fifth}")
print()
stored_sum = fa + fb
print(f"   exact sum of the two stored values = {stored_sum}")
print(f"   the true three tenths              = {three_tenths}")
print(f"   is the stored sum above 3/10?      = {stored_sum > three_tenths}")
print(f"   by how much                        = "
      f"{float(stored_sum - three_tenths)!r}")
print()
print("So the error does not come from the addition -- the addition of the two")
print("stored doubles is EXACT, because the sum is representable.  The error was")
print("already there: both stored values sit slightly above the numbers you")
print("typed.  Then one final rounding happens:")
print(f"   0.1 + 0.2 rounds the exact stored sum to {float(stored_sum)!r}")
print(f"   0.3       rounds 3/10 to                 {float(three_tenths)!r}")
print(f"   same double?                           "
      f"{float(stored_sum) == float(three_tenths)}")
print(f"   they are one ulp apart, {abs(float(stored_sum) - float(three_tenths))!r}")
print()
print("This is the key insight and it is why the example is not a curiosity.")
print("Floating point addition is NOT generally inexact: a + b is computed as")
print("the correctly rounded value of the two stored numbers.  The inexactness")
print("was introduced when 1/10 and 1/5 were each rounded ONCE on the way in,")
print("and rounding twice through different routes gives a different answer")
print("than rounding once.")
print()
print(f"and 0.1 + 0.5 == 0.6 is {0.1 + 0.5 == 0.6} -- because 0.5 is exact, so")
print("only one rounding is involved on the way in for it, and the errors happen")
print("to cancel.  Exactness of the operands is what decides these cases.")

# ------------------------------------------------------------- 5. what to do
rule("5. What to do about it")

print("WRONG: use == when you meant mathematical equality.")
print(f"   (0.1 + 0.2 == 0.3) = {a + b == c}   <- and this is not a rare corner")
print("   case; it is the first thing anyone writes.")
print()
print("RIGHT 1: compare two computed values with a tolerance scaled to them.")
print(f"   math.isclose(0.1 + 0.2, 0.3) = "
      f"{math.isclose(a + b, c, rel_tol=1e-9)}")
print("   Use isclose when both sides came out of arithmetic.  Never use it to")
print("   decide whether something is logically true.")
print()
print("RIGHT 2: use an exact type when the values really are exact.")
print(f"   Fraction(1,10) + Fraction(2,10) = {Fraction(1, 10) + Fraction(2, 10)}")
print(f"   ... == Fraction(3,10)            "
      f"{Fraction(1, 10) + Fraction(2, 10) == Fraction(3, 10)}")
print("   No rounding anywhere, so == means what you think it means.  This is")
print("   the same contrast as Lesson 110 against Lesson 111: modular arithmetic")
print("   is exact and associative, and real-number arithmetic is exact only")
print("   when the answer is representable -- which for 1/10 it never is.")
print()
print("RIGHT 3: count in integers.  Money in cents needs no tolerance at all.")
print(f"   10 + 20 == 30   ->  {10 + 20 == 30}")
print()
print("The summary: 0.1 + 0.2 != 0.3 is a true statement about binary, not a")
print("defect in Python.  The defect is code that assumes real arithmetic where")
print("it has floating point -- and that is the subject of the rest of this")
print("lesson.")
```
```

### 2. Absolute versus relative error, and catastrophic cancellation

```python
```python
"""Absolute versus relative error, and catastrophic cancellation.

Absolute error answers "how far off, in these units".  Relative error answers
"how far off, compared to what I was aiming at".  You need both, and when they
disagree sharply you are looking at cancellation.

Catastrophic cancellation is subtractive cancellation: you subtract two nearly
equal numbers, each carrying a rounding error, and the answer is tiny compared
with the inputs.  The absolute error in the inputs survives; the relative error
in the answer explodes.  No amount of care at the subtraction will help,
because the information was already lost when the operands were rounded.

The standard example is sqrt(x^2 + 1) - x for small x.  Mathematically it is
1 / (sqrt(x^2 + 1) + x), and the two forms agree for large x but not for small.
"""

import math
import struct
from fractions import Fraction


def absolute_error(computed, exact):
    return abs(computed - exact)


def relative_error(computed, exact):
    return abs(computed - exact) / abs(exact)


def rule(title):
    print()
    print("=" * 68)
    print(title)
    print("=" * 68)


# ------------------------------------------------------------ absolute error
rule("1. Two ways to be wrong, and which one matters")

print(f"   answer {0.1:.6f} with error 1e-4   ->  relative error "
      f"{relative_error(0.1 + 1e-4, 0.1):.2e}")
print(f"   answer {1e6:.6f} with error 1e-4   ->  relative error "
      f"{relative_error(1e6 + 1e-4, 1e6):.2e}")
print()
print("The same absolute error is a thousandth of the small answer and a")
print("trillionth of the large one.  Relative error is the only measure that")
print("survives a change of units, and it is what you should be quoting.")
print()
print("Rule of thumb, and it is a real rule rather than a heuristic:")
print("   relative error <= about 1e-16 * n   for n sequential float64 adds")
print("because each addition contributes at most half an ulp of relative")
print("error, and those errors compound.")
print(f"   summing 1000 terms: bound is about {1e-16 * 1000:.0e}")
print()

# ------------------------------------------------------------ cancellation 1
rule("2. Catastrophic cancellation: sqrt(x^2 + 1) - x")

print("The true value is 1/(sqrt(x^2+1) + x), computed here in exact rational")
print("arithmetic via fractions.Fraction, so the reference is trustworthy.")
print()
print(f"   {'x':>8} {'naive sqrt(x^2+1)-x':>24} {'rel err':>10}"
      f" {'stable 1/(sqrt+x)':>22} {'rel err':>10}")
for x in (1.0, 1e2, 1e4, 1e6, 1e8, 1e10, 1e12):
    naive = math.sqrt(x * x + 1.0) - x
    stable = 1.0 / (math.sqrt(x * x + 1.0) + x)
    exact = 1 / (math.sqrt(Fraction(x) ** 2 + 1) + Fraction(x))
    print(f"   {x:>8.0e} {naive:>24.16g} {relative_error(naive, exact):>10.2e}"
          f" {stable:>22.16g} {relative_error(stable, exact):>10.2e}")
print()
print("At x = 1e8 the naive form returns exactly 0.0 -- a relative error of")
print("100% -- because it is subtracting two doubles of size 1e8 whose true")
print("difference is 5e-9, and the doubles do not differ at all.  The stable")
print("form is exact at every x shown, because it adds rather than subtracts.")
print()
print("This is the general signature: a subtraction of two nearly equal")
print("quantities.  It appears in")
print("   - (a + b) - a   instead of   b")
print("   - solving a nearly singular linear system   (Lesson 32)")
print("   - the quadratic formula's b^2 - 4ac when b^2 >> 4ac")
print("   - computing sin(x) as x - sin(x) near 0")
print()

# ------------------------------------------------------------ cancellation 2
rule("3. The same lesson in integers, where there is no rounding at all")

print("Floating point is not required for cancellation.  Here every value is a")
print("Python int, so the arithmetic is exact and there is no epsilon at all:")
a, b = 10**16, 10**16 + 1
print(f"   a = {a}")
print(f"   b = {b}")
print(f"   b - a = {b - a}   (exact, as an int)")
print(f"   float(b) = {float(b)!r}")
print(f"   float(a) = {float(a)!r}")
print(f"   float(a) == float(b) = {float(a) == float(b)}")
print(f"   float(b) - float(a) = {float(b) - float(a)}   <- the true answer is 1")
print()
print(f"The gap between doubles near 1e16 is {math.ulp(float(a)):.0f}, so a and")
print("a+1 land on the SAME double and the difference is annihilated.  Nothing")
print("was wrong with the subtraction; the two operands had already become the")
print("same number before it ran.")
print()
print("Find the threshold by asking when the gap exceeds 1:")
for e in (12, 14, 15, 16, 17):
    m = 10.0**e
    print(f"   near 1e{e}: gap = {math.ulp(m):>10.6g}, "
          f"10^{e}+1 survives? {float(10**e + 1) != float(10**e)}")
print()
print("So the crossover is at 2^52 = 4503599627370496, which is exactly where")
print("float64 stops being able to represent every integer.  Beyond that,")
print("integers themselves start rounding.")
print()
print("float32 crosses much earlier, at 2^24 = 16777216:")


def f32(v):
    """Round a Python float to the nearest float32 and back."""
    return struct.unpack("<f", struct.pack("<f", v))[0]


def f32_ulp(x):
    """The gap to the next float32 above x, found by incrementing its bits."""
    (bits,) = struct.unpack("<I", struct.pack("<f", x))
    (nxt,) = struct.unpack("<f", struct.pack("<I", bits + 1))
    return nxt - x


base = f32(1e17)
print(f"   float32 gap near 1e17            = {f32_ulp(base):.0f}")
print(f"   float64 gap near 1e17            = {math.ulp(1e17):.0f}")
print(f"   float32(1e17) == float32(1e17+1) = {f32(1e17) == f32(1e17 + 1)}")
print(f"   float64(1e17) == float64(1e17+1) = {float(1e17) == float(1e17 + 1)}")
print("   which is why float32 stops being able to count past 2^24 = 16777216,")
print("   long before float64 stops at 2^52.")
print()

# ------------------------------------------------------------ the repair
rule("4. How you repair cancellation: change the algebra")

# The classic repair for (a + b) - a when b is small.
small = 1e-9
big = 1.0
print(f"   (big + small) - big  = {(big + small) - big!r}")
print(f"   which should be         {small!r}")
print(f"   relative error         "
      f"{relative_error((big + small) - big, small):.3e}")
print()
print("Reformulating so the small quantity is never added to the large one")
print("first -- (a + b) - a with |a| >> |b| becomes b - (a - a), or simply b")
print("-- is the only fix.  Precision is already lost at `big + small`.")
print()
print("For the sqrt example the repair was algebraic: multiply by the")
print("conjugate so the big term cancels symbolically instead of numerically.")
print("Symbolic cancellation is free; numeric cancellation is not.")
print()
print("Rule: if you can arrange for the answer to be computed without")
print("subtracting two nearly equal numbers, do that instead of adding")
print("precision.  Extra precision buys you a few more digits; a reformulation")
print("buys you all of them.")

# ------------------------------------------------------------ ulp and spacing
rule("5. Spacing grows with magnitude, which is why relative error is the norm")

print(f"   {'magnitude':>12} {'gap to the next double':>26}")
for m in (1.0, 1e3, 1e6, 1e9, 1e12, 1e15):
    print(f"   {m:>12.0e} {math.ulp(m):>26.6g}")
print()
print("The gap doubles as the exponent rises, so a fixed absolute error is a")
print("shrinking relative error as numbers get bigger.  That is why 'accurate")
print("to 15 decimal places' is a statement about RELATIVE error and about the")
print("range of magnitudes involved.")
print()
print("It also means small numbers near zero are perfectly well resolved.")
print(f"   nextafter(0.0, 1.0)      = {math.nextafter(0.0, 1.0)!r}")
print(f"   smallest positive float64 = {5e-324!r}")
print("There is no problem with small numbers.  The problem is always")
print("subtracting large ones.")
```
```

### 3. Conditioning: which problems are fragile, and which algorithms are

```python
```python
"""Conditioning: how much a small input change can move the answer.

A problem is WELL conditioned when a relative input change of size eps gives a
relative output change of about the same size.  The amplification factor is the
condition number

    kappa = (relative output change) / (relative input change)

and for a scalar function it has the closed form

    kappa(x) = |x f'(x)| / |f(x)|

kappa is a property of the PROBLEM, not of your code.  No extra precision, no
clever algorithm and no amount of care will change it.  That is exactly why an
ill-conditioned problem is not a code failure -- and exactly why "buy more
precision" is often the wrong response.

The sharp distinction this block insists on: CANCELLATION is an instability in
your ALGORITHM, and ILL-CONDITIONING is a property of the PROBLEM.  They look
identical in the output and they have opposite fixes.
"""

import math


def condition_number(f, df, x):
    """kappa = |x f'(x) / f(x)|, the analytic condition number of f at x."""
    return abs(x * df(x) / f(x))


def rule(title):
    print()
    print("=" * 68)
    print(title)
    print("=" * 68)


# -------------------------------------- 1. cancellation is NOT conditioning
rule("1. First, a correction that matters: cancellation is not conditioning")

print("Last lesson's star example was sqrt(x^2+1) - x evaluated in floating")
print("point, which returns exactly 0.0 at x = 1e8.  It is tempting to call")
print("that an ill-conditioned problem.  It is not.")
print()
h = lambda x: math.sqrt(x * x + 1.0) - x
dh = lambda x: x / math.sqrt(x * x + 1.0) - 1.0
print("   kappa for f(x) = sqrt(x^2+1) - x, which simplifies to x/sqrt(x^2+1):")
for x in (1.0, 1e4, 1e8, 1e12):
    print(f"      x = {x:>9.0e}:  kappa = {x / math.sqrt(x * x + 1.0):.9f}")
print()
print("kappa is about 1 at every scale.  The problem is beautifully conditioned:")
print("perturb x by a relative 1e-16 and the true answer moves by a relative")
print("1e-16.  Yet the float64 computation returns 0.0, a relative error of 1.")
print()
print("So the error did not come from the input.  It came from the SEQUENCE of")
print("operations, which subtracts two numbers of size 1e8 whose difference is")
print("5e-9.  That is an unstable ALGORITHM, and the fix is to change the")
print("algorithm -- multiply by the conjugate, as Lesson 120 did -- not to buy")
print("more digits.  In arbitrary precision the naive form works perfectly.")
print()
print("Keeping these apart matters, because the two failures have opposite")
print("responses:")
print("   unstable algorithm  -> rephrase the computation.  More precision")
print("                         helps but is not the real fix.")
print("   ill-conditioned     -> rephrase the PROBLEM, or accept the answer is")
print("                         not knowable.  More precision buys you")
print("                         digits divided by kappa.")
print()

# ------------------------------------------- 2. a genuinely bad function
rule("2. A genuinely ill-conditioned function: log(x) near x = 1")

log = lambda x: math.log(x)
dlog = lambda x: 1.0 / x
print("As x approaches 1, log(x) approaches 0 while x stays at 1.  The answer")
print("becomes tiny while the inputs stay ordinary, so a fixed relative input")
print("error becomes an unbounded relative output error.")
print()
print(f"   {'x':<24} {'log(x)':>14} {'kappa':>14}")
for x in (2.0, 1.1, 1.000001, 1.000000001):
    print(f"   {x!r:<24} {log(x):>14.6e} "
          f"{condition_number(log, dlog, x):>14.6e}")
print()
print("kappa is 1.4 at x = 2 and 1e9 at x = 1 + 1e-9.  It is unbounded as")
print("x -> 1, because kappa = 1 / log(x) and log(x) -> 0.")
print()
print("The demonstration to remember: push x close enough to 1 and the answer")
print("vanishes into the rounding.")
for x in (1 + 1e-8, 1 + 1e-12, 1 + 1e-16):
    print(f"   x = {x!r:<22} math.log(x) = {math.log(x):.6e}")
print()
print("At x = 1 + 1e-16, log(x) comes back as 0.0 -- not a small number, zero.")
print("The true value is about 1e-16, which is entirely below the resolution")
print("of the input itself.  There is no algorithm that recovers it from that")
print("input.  The information is not in the number you were given.")
print()

rule("3. Two more, for shape: a pole and a high power")

tan = lambda x: math.tan(x)
dtan = lambda x: 1.0 / math.cos(x) ** 2
print("tan(x) has a pole at pi/2, so kappa explodes on approach:")
for x in (1.0, 1.5, 1.56, math.pi / 2 - 1e-4):
    print(f"   tan(x) at x = {x:.10f}: kappa = "
          f"{condition_number(tan, dtan, x):.4e}")
print()
pow100 = lambda x: x ** 100
dpow100 = lambda x: 100 * x ** 99
print("x^100 has kappa = 100 wherever x is near 1, because a 1% change in x")
print("becomes a 100% change in the answer:")
print(f"   kappa(x^100) at x = 1.5          = "
      f"{condition_number(pow100, dpow100, 1.5):.4f}")
print(f"   kappa(x^100) at x = 1.0000001    = "
      f"{condition_number(pow100, dpow100, 1.0000001):.4f}")
print("Raising to a power is the simplest way to manufacture an ill-conditioned")
print("problem out of a well-conditioned one, which is why high powers of")
print("small numbers appear in so many overflow bugs.")
print()

# ------------------------------------------- 4. systems: the practical case
rule("4. Ill-conditioned linear systems, where it actually bites")

print("Solve A x = b for A = [[1,1],[1,1+eps]] and b = A @ [1,1], so the exact")
print("answer is [1,1] for every eps.  Then perturb b by ONE ulp and watch.")
print()


def solve2(A, b):
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return ((b[0] * A[1][1] - A[0][1] * b[1]) / det,
            (A[0][0] * b[1] - b[0] * A[1][0]) / det)


print(f"   {'eps':>8} {'x (exact answer is [1,1])':>28} {'rel in':>10}"
      f" {'rel out':>10} {'amplification':>14}")
for eps in (1e-2, 1e-4, 1e-8, 1e-12):
    A = [[1.0, 1.0], [1.0, 1.0 + eps]]
    b = [2.0, 2.0 + eps]
    x = solve2(A, b)
    db = math.ulp(b[1])
    x2 = solve2(A, [b[0], b[1] + db])
    rel_in = db / abs(b[1])
    rel_out = abs(x2[0] - x[0]) / abs(x[0])
    print(f"   {eps:>8.0e} {f'({x[0]:.12f}, {x[1]:.12f})':>28} "
          f"{rel_in:>10.2e} {rel_out:>10.2e} {rel_out / rel_in:>14.4e}")
print()
print("The input moved by 2e-16 -- one bit.  The answer moved by up to 4e-4.")
print("The amplification is 2/eps, exactly the inverse of the determinant.")
print()
print("Nothing here is a bug.  A is within eps of being singular -- its rows")
print("are nearly identical, so A @ [1,1] and A @ [1.0000001, 0.9999999] are")
print("almost the same vector, and recovering the difference between the")
print("inputs from that is asking for digits the data does not contain.")
print("This is Lesson 35 and Lesson 38: a near-null-space direction is")
print("invisible in the output.")
print()
print("The practical response is not more precision.  It is regularisation --")
print("change the problem on purpose, by solving the ridge problem")
print("(A'A + lambda I) x = A'b instead.")


def solve(A, b):
    """Gaussian elimination with partial pivoting on a small dense system."""
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r == c:
                continue
            factor = M[r][c] / M[c][c]
            for k in range(c, n + 1):
                M[r][k] -= factor * M[c][k]
    return [M[i][n] / M[i][i] for i in range(n)]


def ridge(A, b, lam):
    """The Tikhonov solution: minimise ||Ax - b||^2 + lambda * ||x||^2."""
    n = len(A)
    AtA = [[sum(A[k][i] * A[k][j] for k in range(n)) + (lam if i == j else 0.0)
            for j in range(n)] for i in range(n)]
    Atb = [sum(A[k][i] * b[k] for k in range(n)) for i in range(n)]
    return solve(AtA, Atb)


def err(x):
    return math.hypot(x[0] - 1.0, x[1] - 1.0)


eps = 1e-12
A = [[1.0, 1.0], [1.0, 1.0 + eps]]
b = [2.0, 2.0 + eps]
b_perturbed = [b[0], b[1] + math.ulp(b[1])]
print()
print(f"   exact answer                                    [1.0, 1.0]")
print(f"   plain solve, correct b                          "
      f"{[round(v, 12) for v in solve(A, b)]}   err {err(solve(A, b)):.2e}")
print(f"   plain solve, b perturbed by 1 ulp                "
      f"{[round(v, 12) for v in solve(A, b_perturbed)]}   "
      f"err {err(solve(A, b_perturbed)):.2e}")
r = ridge(A, b, 1e-4)
r2 = ridge(A, b_perturbed, 1e-4)
print(f"   ridge lambda=1e-4, correct b                    "
      f"{[round(v, 12) for v in r]}   err {err(r):.2e}")
print(f"   ridge lambda=1e-4, b perturbed by 1 ulp          "
      f"{[round(v, 12) for v in r2]}   err {err(r2):.2e}")
print()
print("The plain solve's error jumped from 0 to 6e-4 on a one-bit change of")
print("the input.  The ridge solve gives the SAME answer either way, to twelve")
print("decimals: it has bought insensitivity at the price of a known, smooth")
print("bias of 3.5e-5.  That trade -- bounded bias instead of unbounded noise --")
print("is the whole point of regularisation, and Lesson 101 minimises exactly")
print("this objective.")
print()
print("Note what did NOT happen: nobody reached for a wider float.  The")
print("information destroyed by the near-singular A was already gone.")
print()

# ------------------------------------------- 5. digits you actually keep
rule("5. Turning kappa into a digit count")

print("float64 carries about 16 significant decimal digits.  A condition")
print("number of 10^k costs you about k of them.")
print()
print(f"   {'kappa':>12} {'digits lost':>13} {'usable':>9}  verdict")
for k in (1, 10, 1e3, 1e6, 1e10, 1e14, 1e16, 1e20):
    lost = math.log10(k)
    usable = 16 - lost
    if usable > 12:
        verdict = "fine"
    elif usable > 6:
        verdict = "usable with care"
    elif usable > 0:
        verdict = "marginal"
    else:
        verdict = "hopeless in float64"
    print(f"   {k:>12.4g} {lost:>13.2f} {usable:>9.2f}  {verdict}")
print()
print("So the answer to 'my float64 result has 12 wrong digits' is often not")
print("a more precise type.  If kappa is 1e10, switching to float128 (about 34")
print("digits) leaves you with 24, and switching to exact arithmetic leaves you")
print("with the error that was already in the input.  The digits were never")
print("recoverable.")
print()

rule("6. So: an ill-conditioned problem is a property, not a failure")

print("Three things that get confused, and the order to check them.")
print()
print("  CONDITIONING  a property of the problem, fixed before you write code.")
print("                You can only rephrase the problem, or accept the limit.")
print()
print("  STABILITY     a property of your algorithm.  An unstable algorithm is")
print("                bad even on a perfect problem, and fixing it is often")
print("                free -- that is what the conjugate trick was.")
print()
print("  ACCURACY      how close you actually got.  Conditioning BOUNDS it for")
print("                you at roughly kappa times the input's own error.")
print()
print("Diagnostic order when a number comes out wrong:")
print("  1. Is the ALGORITHM stable here?   -> rephrase the computation.")
print("  2. Is the PROBLEM conditioned?     -> rephrase the problem, or accept.")
print("  3. Was the INPUT accurate enough?   -> only now is precision the answer.")
print()
print("Most people start at 3 and buy precision that step 1 or 2 would have")
print("made unnecessary.")
```
```

### 4. Bisection and Newton, from scratch, with the error bounds

```python
```python
"""Bisection and Newton-Raphson, from scratch, with their error guarantees.

BISECTION needs only continuity and a sign change.  It is unconditionally
stable and its error bound is a theorem: after n iterations on an interval of
width w, the error is at most w / 2^(n+1).  It converges slowly and linearly,
but it cannot be made to fail by a bad starting point.

NEWTON uses the derivative.  It converges quadratically -- the number of
correct digits roughly doubles each step -- but it is only locally convergent
and it can walk off to somewhere useless.  The safeguard everyone actually uses
is Newton's method with a bisection fallback, which keeps the speed and cannot
lose the bracket.

Both are below, both print their iterates, and both are checked against a
correct reference.
"""

import math


def rule(title):
    print()
    print("=" * 68)
    print(title)
    print("=" * 68)


# ================================================================ bisection
def bisection(f, a, b, tol=1e-12, max_iter=200):
    """Return (root, iterations, history).

    Precondition: f(a) and f(b) have opposite signs.  Each step halves the
    bracket, so after n steps the interval is (b-a)/2^n wide and the returned
    midpoint is within half of that of the true root.
    """
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("f(a) and f(b) must have opposite signs")
    history = []
    for n in range(max_iter):
        mid = 0.5 * (a + b)
        fm = f(mid)
        history.append((n, a, b, mid, fm))
        if fa * fm <= 0.0:
            b, fb = mid, fm
        else:
            a, fa = mid, fm
        if 0.5 * (b - a) < tol:
            return 0.5 * (a + b), n + 1, history
    return 0.5 * (a + b), max_iter, history


def bisection_iterations(width, tol):
    """How many halvings of `width` are needed to get under `tol`?"""
    n = 0
    w = width
    while w > tol:
        w /= 2.0
        n += 1
    return n


# =================================================================== newton
def newton(f, df, x0, tol=1e-12, max_iter=100):
    """Return (root, iterations, history) using the plain Newton iteration.

    x_{n+1} = x_n - f(x_n) / f'(x_n)
    """
    history = []
    x = x0
    for n in range(max_iter):
        fx = f(x)
        history.append((n, x, fx))
        if abs(fx) < tol:
            return x, n, history
        step = fx / df(x)
        x = x - step
    return x, max_iter, history


def newton_bisected(f, df, a, b, tol=1e-12, max_iter=200):
    """Newton when it behaves, bisection whenever it does not.

    Keep the bracket [a, b] invariant at all times.  Take a Newton step only
    while it lands strictly inside the bracket; otherwise fall back to the
    midpoint.  This cannot diverge and cannot lose the sign change, so it is as
    safe as bisection and as fast as Newton on a well-behaved function.
    """
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("f(a) and f(b) must have opposite signs")
    history = []
    x = 0.5 * (a + b)
    newton_steps = 0
    for n in range(max_iter):
        fx = f(x)
        dfx = df(x)
        history.append((n, x, fx))
        if abs(fx) < tol:
            return x, n, history, newton_steps
        if fa * fx < 0.0:                 # root is between a and x
            b, fb = x, fx
        else:                             # root is between x and b
            a, fa = x, fx
        candidate = x - fx / dfx if dfx != 0.0 else math.nan
        if a < candidate < b:
            newton_steps += 1
            x = candidate
        else:
            x = 0.5 * (a + b)             # Newton wanted to leave the bracket
    return x, max_iter, history, newton_steps


# ===================================================== worked case: sqrt(2)
rule("1. Worked example: the square root of 2, step by step")

TARGET = math.sqrt(2.0)
print(f"f(x) = x^2 - 2,  f'(x) = 2x,  true root = {TARGET!r}")
print(f"{TARGET!r} is the correctly rounded double nearest the real sqrt(2).")
print()

print("BISECTION on [1, 2].  f(1) = -1, f(2) = 2, so the root is bracketed.")
print(f"   {'n':>3} {'a':>22} {'b':>22} {'midpoint':>22} {'f(midpoint)':>14}")
root, iters, hist = bisection(lambda x: x * x - 2.0, 1.0, 2.0, tol=1e-12)
for n, a, b, mid, fm in hist[:8]:
    print(f"   {n:>3} {a:>22.17f} {b:>22.17f} {mid:>22.17f} {fm:>14.3e}")
print("   ...")
for n, a, b, mid, fm in hist[-3:]:
    print(f"   {n:>3} {a:>22.17f} {b:>22.17f} {mid:>22.17f} {fm:>14.3e}")
print(f"   stopped after {iters} iterations at {root!r}")
print(f"   error = {abs(root - TARGET):.3e}")
print()

print("NEWTON from x0 = 1.  x_{n+1} = x - (x^2 - 2)/(2x) = (x + 2/x)/2, which")
print("is the Babylonian / Heron method -- the same one a square-root routine uses.")
print(f"   {'n':>3} {'x':>22} {'f(x)':>14} {'correct digits':>16}")
root2, iters2, hist2 = newton(lambda x: x * x - 2.0, lambda x: 2.0 * x,
                              1.0, tol=1e-12)
for n, x, fx in hist2:
    digits = -(math.log10(abs(fx))) if fx != 0.0 else float("inf")
    print(f"   {n:>3} {x:>22.17f} {fx:>14.3e} {digits:>16.1f}")
print(f"   stopped after {iters2} iterations at {root2!r}")
print(f"   error = {abs(root2 - TARGET):.3e}")
print()
print("Newton went from 0 correct digits to about 4, then 8, then 15.  That is")
print("quadratic convergence: each step doubles the number of correct digits.")
print("Bisection added about one digit per step and needed 40 iterations for")
print("the same precision.")
print()

rule("2. The error guarantee, and why bisection is bulletproof")

width = 1.0
print("Bisection's bound is a theorem, not an observation.  Starting from an")
print("interval of width w, after n iterations the interval has width w / 2^n,")
print("and the returned midpoint is at most half of that from the true root.")
print()
print(f"   {'tolerance':>12} {'iterations needed':>19} {'2^-n':>12}")
for tol in (1e-1, 1e-4, 1e-8, 1e-12, 1e-16):
    n = bisection_iterations(width, tol)
    print(f"   {tol:>12.0e} {n:>19} {2.0 ** -n:>12.3e}")
print()
print("Getting to float64's own resolution -- about 1e-16 -- takes 54 halvings,")
print("because you can halve until the interval is smaller than the gap between")
print("two doubles, and then not usefully further.")
print()
print("That guarantee is unconditional.  Bisection cannot be given a bad")
print("starting point, cannot diverge, and cannot oscillate.  Its only")
print("requirement is a sign change, which you can verify:")
print()


def sign_change(f, a, b):
    fa, fb = f(a), f(b)
    return fa * fb <= 0


print(f"   f(1)*f(2) <= 0 ? {sign_change(lambda x: x * x - 2.0, 1.0, 2.0)}")
print(f"   f(1)*f(1) <= 0 ? {sign_change(lambda x: x * x - 2.0, 1.0, 1.0)}"
      "   (no sign change, so bisection correctly refuses)")
try:
    bisection(lambda x: x * x - 2.0, 1.0, 1.0)
except ValueError as exc:
    print(f"   ValueError: {exc}")
print()

rule("3. Newton is fast until it is not")

print("Quadratic convergence is LOCAL.  It is a statement about a neighbourhood")
print("of the root, not a global guarantee, and the textbook example of the")
print("difference is f(x) = x^3 - 2x + 2 with f'(x) = 3x^2 - 2.")
print()
print("There is exactly one real root, near -1.7693.  Watch what Newton does:")
print()


def cubic(x):
    return x ** 3 - 2.0 * x + 2.0


def dcubic(x):
    return 3.0 * x ** 2 - 2.0


REAL_ROOT = -1.7692923542386314
print(f"   {'x0':>6} {'iterations':>11} {'final x':>24} {'f(x)':>14} {'converged':>10}")
for x0 in (0.0, 1.0, 0.5, -1.0, -2.0, 2.0):
    r, n, hist = newton(cubic, dcubic, x0, tol=1e-12, max_iter=60)
    ok = abs(cubic(r)) < 1e-12
    print(f"   {x0:>6.1f} {n:>11} {r:>24.17f} {cubic(r):>14.3e} {str(ok):>10}")
print()
print("From x0 = 0 and x0 = 1 it never converges at all -- it cycles.  The")
print("iterates are:")
_, _, hist = newton(cubic, dcubic, 0.0, tol=1e-12, max_iter=8)
print(f"   {'n':>3} {'x':>20} {'f(x)':>14}")
for n, x, fx in hist:
    print(f"   {n:>3} {x:>20.17f} {fx:>14.3e}")
print()
print("0 goes to 1, 1 goes to 0, and it repeats forever.  The tangent at 0")
print("crosses the axis at 1; the tangent at 1 crosses it back at 0.  From any")
print("other starting point it converges in 4 to 9 steps.")
print()
print("The other failure is arithmetic rather than geometric: on f(x) = x^2 - 2")
print("starting at x0 = 0, f'(0) = 0 and the step divides by zero.")
try:
    newton(lambda x: x * x - 2.0, lambda x: 2.0 * x, 0.0, max_iter=10)
except ZeroDivisionError as exc:
    print(f"   ZeroDivisionError: {exc}")
print()
print("The lesson is not 'Newton is dangerous'.  It is that Newton needs a")
print("bracket or a verified-good starting point, and the verification is")
print("cheap.")
print()

rule("4. The fix everyone uses: Newton with a bisection fallback")

print("Keep a bracket [a, b] whose endpoints have opposite signs.  Take the")
print("Newton step when it lands strictly inside the bracket; otherwise take")
print("the midpoint.  You keep quadratic convergence near the root and")
print("bisection's safety everywhere else, and you can prove the bracket never")
print("shrinks to nothing.")
print()
print("On f(x) = x^3 - 2x + 2 with the bracket [-3, 0] -- the case where plain")
print("Newton cycled forever from x0 = 0:")
root3, iters3, hist3, nsteps = newton_bisected(
    cubic, dcubic, -3.0, 0.0, tol=1e-12)
print(f"   plain Newton from x0 = 0:  never converges")
print(f"   safeguarded: {iters3} iterations, {nsteps} of them Newton steps")
print(f"   root = {root3!r}")
print(f"   error = {abs(root3 - REAL_ROOT):.3e}")
print()
print("For contrast, plain bisection on the same bracket:")
root4, iters4, _ = bisection(cubic, -3.0, 0.0, tol=1e-12)
print(f"   {iters4} iterations, root = {root4!r}, "
      f"error = {abs(root4 - REAL_ROOT):.3e}")
print()
print("Same answer, and the safeguarded version provably never left the")
print("bracket.  This is what scipy.optimize.brentq and essentially every")
print("production root-finder is: a bisection skeleton with Newton")
print("accelerants.")
print()
print("The engineering rule: pure Newton if you can prove your starting point")
print("is good, pure bisection if you need a guarantee and can afford the")
print("iterations, and the safeguarded hybrid in every other case.  It costs")
print("one comparison per iteration and removes a whole class of bug.")
print()

rule("5. Choosing a tolerance, which is a real decision")

print("A tolerance that is too loose returns a number you did not want.  A")
print("tolerance that is too tight makes the solver spin: it cannot reach the")
print("target, because the target is below the resolution of the arithmetic.")
print()
print("   the gap between doubles near 1.0  = %.3e" % math.ulp(1.0))
print("   the gap between doubles near 7.0  = %.3e" % math.ulp(7.0))
print("   the gap between doubles near 1e8   = %.3e" % math.ulp(1e8))
print()
print("So a tolerance of 1e-20 is unreachable in float64: there is no double")
print("between 1.0 and the next one along.  Asking for it is asking the solver")
print("to iterate until max_iter and then return something arbitrary.")
print()
print("Sensible choices, in order of preference:")
print("   1. Scale the tolerance to the problem: 1e-12 for a value of order 1,")
print("      1e-9 for a value of order 1e3.  Relative, not absolute.")
print("   2. Use a RELATIVE or error-estimate test rather than a bare absolute")
print("      one.  |f(x)/f'(x)| / max(1, |x|) < tol is invariant under")
print("      rescaling f, so it works whatever units the function uses.")
print("   3. Stop on the STEP size as well as the residual: if |x_{n+1} - x_n|")
print("      is below the gap at x_n, further iteration is arithmetic noise.")
print("   4. Always pass max_iter, and treat hitting it as a failure to report,")
print("      not as an answer to return.")
print()


def relative_converged(f, x, tol):
    """The tolerance test to actually use: residual scaled by the magnitude."""
    return abs(f(x)) < tol * max(1.0, abs(x))


print(f"   at the exact root, every test agrees it has converged: "
      f"abs {abs(cubic(REAL_ROOT)) < 1e-12}, "
      f"rel {relative_converged(cubic, REAL_ROOT, 1e-12)}, "
      f"err {abs(cubic(REAL_ROOT) / dcubic(REAL_ROOT)) < 1e-12}")
print()
print("Where tests disagree is a point that is NOT yet converged.  Build one,")
print("a little way short of the root:")
near = REAL_ROOT + 1e-6 / abs(dcubic(REAL_ROOT))    # |cubic(near)| ~ 1e-6
print(f"   x                        = {near!r}")
print(f"   cubic(x)                 = {cubic(near):.3e}")
print(f"   |cubic / cubic'|  (error in x) = {abs(cubic(near) / dcubic(near)):.3e}")
print(f"   relative to |x|          = "
      f"{abs(cubic(near) / dcubic(near)) / abs(near):.3e}")
print()
print("That third line is the one to test against.  |f(x)/f'(x)| is a")
print("first-order estimate of how far x still is from the root, and it is the")
print("only version of the test that is invariant under rescaling f.  Rescale")
print("the function by a billion and the residual moves but the estimate does")
print("not:")
g = lambda x: 1e-9 * cubic(x)
dg = lambda x: 1e-9 * dcubic(x)
print()
print(f"   {'function':<12} {'|f|':>12} {'|f/fprime|':>14} {'relative to |x|':>18}")
for name, f, df in [("cubic", cubic, dcubic), ("1e-9*cubic", g, dg)]:
    est = abs(f(near) / df(near))
    print(f"   {name:<12} {abs(f(near)):>12.3e} {est:>14.3e} "
          f"{est / abs(near):>18.3e}")
print()
print("The residual column changes by a factor of a billion.  The estimate")
print("columns do not change at all -- and both say 7.7e-8 relative, which is")
print("nowhere near the 1e-12 we asked for.  So the solver correctly keeps")
print("going, on either function.")
print()
print("A test that compares |f(x)| against tol will declare this point")
print(f"converged for the scaled function ({abs(g(near)) < 1e-12}) and, worse,")
print("will do so for any function written in small units.  Test the estimated")
print("error in x, or the step size -- never the raw residual against an")
print("absolute constant.")
```
```

### 5. Finite differences, and why a tiny step is a terrible step

```python
```python
"""Finite differences: measuring a derivative you cannot differentiate for.

Two errors fight each other, and the step size h is where you choose which one
wins.

  TRUNCATION error comes from the Taylor series.  For a forward difference the
  first neglected term is h f''(x)/2, so the error is O(h) -- halving h halves
  the error.  For a central difference the h^2 terms cancel by symmetry and the
  error is O(h^2) -- halving h quarters the error.

  ROUNDOFF error comes from the arithmetic.  f(x+h) and f(x) are each known to
  within about eps|f|, so their difference has an absolute error of about
  2 eps |f|.  Dividing by h turns that into an error of about 2 eps |f| / h --
  which GROWS as h shrinks.

Total error is roughly  C1 * h        +  2 eps |f| / h     (forward)
                  roughly  C2 * h^2     +  2 eps |f| / h     (central)

The truncation term wants h small; the roundoff term wants h LARGE.  The best
h is where they balance:

  forward:   h* ~ sqrt(2 eps |f| / |f''|)
  central:   h* ~ (3 eps |f| / |f'''|)^(1/3)

which is why the optimum for a central difference is about 6e-6 rather than
1e-8.  Choosing h "as small as possible" makes the answer WORSE, and this block
measures exactly how much worse.
"""

import math


def rule(title):
    print()
    print("=" * 68)
    print(title)
    print("=" * 68)


EPS = 2.0**-52

# A function with a known derivative, so the error can be measured exactly.
F = lambda x: math.sin(x) + 0.3 * x**2
DF = lambda x: math.cos(x) + 0.6 * x
D2F = lambda x: -math.sin(x) + 0.6
D3F = lambda x: -math.cos(x)

X = 1.3


def forward(x, h):
    """(f(x+h) - f(x)) / h.  Error is O(h)."""
    return (F(x + h) - F(x)) / h


def backward(x, h):
    """(f(x) - f(x-h)) / h.  Also O(h), same constant."""
    return (F(x) - F(x - h)) / h


def central(x, h):
    """(f(x+h) - f(x-h)) / (2h).  Error is O(h^2)."""
    return (F(x + h) - F(x - h)) / (2.0 * h)


def rel_err(approx):
    return abs(approx - DF(X)) / abs(DF(X))


# ------------------------------------------------------------------- 1
rule("1. Forward versus central, at the same step size")

exact = DF(X)
print(f"f(x) = sin(x) + 0.3x^2,  f'(x) = cos(x) + 0.6x")
print(f"at x = {X}:  f'(x) = {exact!r}")
print()
print(f"   {'h':>12} {'forward err':>14} {'central err':>14} {'ratio':>10}")
for h in (1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8):
    ef, ec = rel_err(forward(X, h)), rel_err(central(X, h))
    print(f"   {h:>12.0e} {ef:>14.3e} {ec:>14.3e} {ef / ec:>9.1f}x")
print()
print("Central wins by four orders of magnitude in the middle of the range:")
print("at h = 1e-4 the forward error is 1.7e-5 and the central error is 4.3e-10,")
print("a ratio of 40736.  That is the asymmetry doing the work -- quartering")
print("the forward error needs halving h, while the central error falls as h^2.")
print()
print("But look at the last two rows.  From 1e-6 to 1e-8 the CENTRAL error")
print("gets WORSE (7.5e-12, then 5.6e-11, then 1.6e-10), and by h = 1e-8 the two")
print("are identical to one digit.  Central is not simply better; it has a")
print("window, and 1e-8 is outside it.  Section 2 explains why.")
print()
print("The reason for the window is symmetry.  The forward difference's")
print("expansion is")
print("   f'(x) + h f''(x)/2 + h^2 f'''(x)/6 + ...  <- the h term survives")
print("The central difference's is")
print("   f'(x) + h^2 f'''(x)/6 + ...               <- the h term cancels")
print()
print("The cost of central is that it needs f at two extra points, and for a")
print("function with a boundary or a domain edge, x-h may not be available.")
print()

# ------------------------------------------------------------------- 2
rule("2. Where the optimum step size is, and why it is not 'as small as possible'")

print("Halving h reduces truncation and increases roundoff, so the error curve")
print("has a U shape with a minimum.  Walk into that minimum from both sides:")
print()
print(f"   {'h':>12} {'forward rel err':>18} {'central rel err':>18}")
rows = []
h = 1e-2
while h >= 1e-17:
    rows.append((h, rel_err(forward(X, h)), rel_err(central(X, h))))
    h /= 10.0
for h, ef, ec in rows:
    print(f"   {h:>12.0e} {ef:>18.3e} {ec:>18.3e}")
best_f = min(rows, key=lambda r: r[1])
best_c = min(rows, key=lambda r: r[2])
BEST_F_H, BEST_F_ERR = best_f[0], best_f[1]
BEST_C_H, BEST_C_ERR = best_c[0], best_c[2]
print()
print(f"   best forward error {BEST_F_ERR:.3e} at h = {BEST_F_H:.0e}")
print(f"   best central error {BEST_C_ERR:.3e} at h = {BEST_C_H:.0e}")
print()
print("The forward error improves all the way down to 1e-8 and then turns")
print("back up; the central error bottoms out at 1e-5 and climbs steeply after")
print("1e-6.  Both curves have a minimum, and both minima are at FINITE h.")
print()
print("   THE OPTIMUM IS FINITE, AND IT IS MUCH LARGER THAN YOU GUESS.")
print("   A step of 1e-16 is not 'more accurate'.  At that size f(x+h) == f(x)")
print("   for most functions, so the numerator is 0 or pure rounding noise and")
print("   the derivative comes back as 0, or as an enormous wrong number.")
print("   Shrinking the step makes the answer strictly worse, and the code")
print("   still runs, and nothing raises.")
print()

# ------------------------------------------------------------------- 3
rule("3. The formulas for h*, and the order of magnitude they predict")

f1 = abs(DF(X))
f2 = abs(D2F(X))
f3 = abs(D3F(X))
h_star_forward = math.sqrt(2.0 * EPS * f1 / f2)
h_star_central = (3.0 * EPS * f1 / f3) ** (1.0 / 3.0)
print("forward:   h* ~ sqrt(2 eps |f'| / |f''|)")
print(f"          = sqrt(2 * {EPS:.3e} * {f1:.6f} / {f2:.6f}) = {h_star_forward:.3e}")
print(f"   measured best was {BEST_F_H:.0e}  (same order of magnitude)")
print()
print("central:   h* ~ (3 eps |f'| / |f'''|)^(1/3)")
print(f"          = (3 * {EPS:.3e} * {f1:.6f} / {f3:.6f})^(1/3) = "
      f"{h_star_central:.3e}")
print(f"   measured best was {BEST_C_H:.0e}  (same order of magnitude)")
print()
print("Note the cube root against the square root: for the same numbers the")
print(f"central optimum ({h_star_central:.0e}) is about "
      f"{h_star_central / h_star_forward:.0f}x LARGER than the forward one")
print(f"({h_star_forward:.0e}).  Central differences tolerate a much bigger step,")
print("which is the practical payoff, not just the accuracy payoff.")
print()

# ------------------------------------------------------------------- 4
rule("4. The floor: how good can a finite difference possibly be?")

print("The roundoff floor for the central difference is about 2 eps |f| / h*,")
print("and with h* ~ eps^(1/3) that becomes about eps^(2/3) -- around 1e-11.")
print(f"   EPS^(2/3)      = {EPS ** (2.0 / 3.0):.3e}")
print(f"   measured floor = {BEST_C_ERR:.3e}")
print()
print("So in float64 a central difference of a smooth function is good to")
print("about 10 or 11 digits, and no choice of h will do better.  If you need")
print("more, you need a different tool: a complex-step derivative, which")
print("computes f'(x) = Im(f(x + ih))/h with NO subtraction and therefore no")
print("cancellation at all.")
print()
print("Complex step, the cheapest trick in numerical analysis:")
X_C = 1.3
h_c = 1e-20
f_complex = complex(X_C, h_c) ** 2
cs_deriv = f_complex.imag / h_c
print(f"   f(x) = x^2 at x = {X_C}, h = {h_c:.0e}")
print(f"   complex-step derivative  = {cs_deriv!r}")
print(f"   exact derivative          = {2 * X_C!r}")
print(f"   relative error           = {abs(cs_deriv - 2 * X_C) / (2 * X_C):.3e}")
print(f"   a real central difference with the best h gave {BEST_C_ERR:.3e}")
print()
print("It came out EXACTLY right here, not merely close, because the imaginary")
print("part never suffers cancellation: (x + ih)^2 has imaginary part exactly")
print("2xh, with no subtraction of nearby quantities anywhere in the whole")
print("evaluation.  Complex-step differs from an automatic-differentiation tool")
print("only in that it differentiates one function, once, and needs no reverse")
print("pass.")
print()
print("The constraint is real: the function must be evaluated with complex")
print("arithmetic all the way through, so it cannot contain abs, max, or a")
print("branch on the sign of a real number.  Everything smooth and analytic")
print("works, which is most of what you differentiate in practice.")
print()

# ------------------------------------------------------------------- 5
rule("5. A worked choice of h you can defend")

print("You are asked for f'(2.0) of f(x) = x * exp(x), to 10 correct digits.")
print("You do not know f''' but you can bound it, and that is enough.")
print()


def g(x):
    return x * math.exp(x)


def dg(x):
    return (x + 1.0) * math.exp(x)


def g_forward(x, h):
    return (g(x + h) - g(x)) / h


def g_central(x, h):
    return (g(x + h) - g(x - h)) / (2.0 * h)


XG = 2.0
print(f"   f'(2) = {dg(XG)!r}")
print()
print("Step 1: find the best h empirically on a log grid, which is what you")
print("would actually do in code.")
grid = [10.0**(-k) for k in range(2, 19)]
bf = min(grid, key=lambda h: abs(g_forward(XG, h) - dg(XG)))
bc = min(grid, key=lambda h: abs(g_central(XG, h) - dg(XG)))
print(f"   forward: best h = {bf:.0e}, rel err "
      f"{abs(g_forward(XG, bf) - dg(XG)) / dg(XG):.3e}")
print(f"   central: best h = {bc:.0e}, rel err "
      f"{abs(g_central(XG, bc) - dg(XG)) / dg(XG):.3e}")
print()
print("Step 2: check the rule of thumb predicts the same order of magnitude.")
print("   |f'(2)| = %.6f, |f''(2)| = %.6f, |f'''(2)| = %.6f"
      % (abs(dg(XG)), abs((XG + 2.0) * math.exp(XG)),
         abs((XG + 3.0) * math.exp(XG))))
print(f"   forward h* ~ {math.sqrt(2 * EPS * abs(dg(XG)) / abs((XG + 2.0) * math.exp(XG))):.1e}")
print(f"   central h* ~ {(3 * EPS * abs(dg(XG)) / abs((XG + 3.0) * math.exp(XG))) ** (1 / 3):.1e}")
print()
print("They agree to within a factor of a few, which is all the rule promises.")
print()
print("Step 3: state the deliverable honestly.  With float64 you can promise")
print("about 10 or 11 digits from a central difference.  To promise 15, say so")
print("and use the complex step:")
h_cs = 1e-20
gs = complex(XG, h_cs) * complex(math.e, 0) ** complex(XG, h_cs)
cs = gs.imag / h_cs
print(f"   complex-step f'(2) = {cs!r}")
print(f"   rel err            = {abs(cs - dg(XG)) / dg(XG):.3e}")
print()
print("Never promise more digits than the method delivers.  A gradient that is")
print("quietly wrong in its twelfth digit will corrupt a Newton step or a")
print("convergence test long before anyone notices the value itself.")
```
```

### With Libraries

The same facts, checked against numpy and scipy, where the constants and the
tools are the real library ones. numpy's `finfo.eps`, `spacing`,
`expm1`, `log1p`, `cond`, and scipy's `brentq` and `approx_fprime` all appear
in the lesson's arguments.

not runnable

```python
```python
"""The same facts, checked against numpy, mpmath and Python's own tools.

Run with: python -c "import numpy, mpmath; print(numpy.__version__, mpmath.__version__)"
"""

import math
import struct
from fractions import Fraction

import numpy as np

# --- IEEE 754 and epsilon -----------------------------------------------------

print("numpy agrees about what float64 is:")
print(f"   eps          = {np.finfo(np.float64).eps!r}")
print(f"   1 + eps == 1 = {1.0 + np.finfo(np.float64).eps == 1.0}")
print(f"   float32 eps  = {np.finfo(np.float32).eps!r}")
print(f"   float32 0.1  = {np.float32(0.1)!r}")
print(f"   float64 0.1  = {np.float64(0.1)!r}")
print(f"   float16 eps  = {np.finfo(np.float16).eps!r}")
print(f"   np.spacing(1.0)   = {np.spacing(1.0)!r}")
print(f"   np.spacing(1e12)  = {np.spacing(1e12)!r}")
print(f"   math.ulp(1.0)     = {math.ulp(1.0)!r}   (the same number)")
print()

print("and about which decimals are exact -- nextafter resolves it bit by bit:")
for d in (0.5, 0.25, 0.125, 0.0625, 0.1, 0.2, 0.3, 0.7):
    v = float(d)
    exact = Fraction(v) == Fraction(d).limit_denominator(10**9)
    print(f"   {d:<8} = {v!r:<24} exact to 9 places: {exact}")
print()

# --- 0.1 + 0.2 != 0.3, with exact arithmetic ---------------------------------

print("the addition, and numpy's own two 'equal' ways:")
a, b, c = 0.1, 0.2, 0.3
print(f"   0.1 + 0.2            = {a + b!r}")
print(f"   0.3                  = {c!r}")
print(f"   == ?                 = {a + b == c}")
print(f"   np.float64(0.1)+0.2  = {np.float64(0.1) + np.float64(0.2)!r}   (same)")
print(f"   np.isclose           = {np.isclose(a + b, c)}")
print(f"   difference           = {abs((a + b) - c)!r}")
print(f"   ulps apart           = "
      f"{abs(np.float64(a + b).view(np.int64) - np.float64(c).view(np.int64))}")
print()
stored = Fraction(a) + Fraction(b)
print(f"   exact sum of stored values = {stored}")
print(f"   that is above 3/10?         {stored > Fraction(3, 10)}")
print(f"   float(exact sum)            = {float(stored)!r}")
print(f"   float(3/10)                 = {float(Fraction(3, 10))!r}")
print()
print("The np.spacing function is the machine-precise way to ask 'how big is a")
print("step at this magnitude', which is what a step-size choice needs.")
print()

# --- catastrophic cancellation, in numpy --------------------------------------

print("catastrophic cancellation, computed two ways:")
xs = np.array([1e8, 1e10, 1e12])
naive = np.sqrt(xs**2 + 1.0) - xs
stable = 1.0 / (np.sqrt(xs**2 + 1.0) + xs)
exact = 1.0 / (np.sqrt(xs.astype(np.longdouble)**2 + 1.0) + xs.astype(np.longdouble))
print(f"   {'x':>8} {'naive':>24} {'stable':>24} {'exact (longdouble)':>22}")
for i, x in enumerate(xs):
    print(f"   {x:>8.0e} {naive[i]:>24.16g} {stable[i]:>24.16g} "
          f"{float(exact[i]):>22.16g}")
print()
print("The naive form returns exactly 0.0 for x >= 1e8: relative error 100%.")
print("The stable form is right to the last bit at every magnitude.")
print()
print("numpy also gives you the tools to not do this by hand:")
print(f"   np.expm1(x) instead of np.exp(x) - 1:")
tiny = 1e-12
print(f"      exp(1e-12) - 1     = {math.exp(tiny) - 1.0!r}")
print(f"      np.expm1(1e-12)    = {np.expm1(tiny)!r}")
print(f"      true value          = {tiny!r}")
print(f"      relative error of exp-1  = "
      f"{abs((math.exp(tiny) - 1.0) - tiny) / tiny:.3e}")
print(f"      relative error of expm1 = "
      f"{abs(np.expm1(tiny) - tiny) / tiny:.3e}")
print()
print("   np.log1p(x) instead of np.log(1 + x):")
print(f"      math.log(1 + 1e-12) = {math.log(1.0 + 1e-12)!r}")
print(f"      np.log1p(1e-12)    = {np.log1p(1e-12)!r}")
print()
print("These three -- expm1, log1p, and the algebra of a conjugate -- are the")
print("whole standard library of cancellation avoidance.  numpy has them")
print("because everyone needed them and nobody could remember to factor them")
print("out of their own code.")
print()

# --- summation order ----------------------------------------------------------

print("summation order, which numpy documents rather than hides:")
v = np.array([1e16, 1.0, -1e16, 1.0])
fold = 0.0
for x in v:
    fold += x
print(f"   {v.tolist()}")
print(f"   fold, left to right      = {fold}")
print(f"   numpy .sum()             = {v.sum()}")
print(f"   math.fsum (exact)        = {math.fsum(v.tolist())}")
print(f"   true value               = 2.0")
print()
print("Both the naive loop and numpy get 1.0, not 2.0.  numpy's pairwise")
print("summation has an unrolled block of 8, and with only four terms it never")
print("gets the chance to help.")
print()
n = 1000
ones = np.full(n, 0.1)
print(f"   summing {n} copies of 0.1 (true sum {0.1 * n}):")
print(f"      numpy pairwise .sum()  = {ones.sum()!r}")
print(f"      naive loop             = ", end="")
acc = 0.0
for x in ones:
    acc += x
print(f"{acc!r}")
print(f"      math.fsum              = {math.fsum(ones.tolist())!r}")
print()
print("numpy uses pairwise summation with an unrolled block of 8, which is why")
print("it beats a naive loop on many similar terms.  It still loses the 1e16")
print("case above: pairwise reduces how OFTEN a small term is swallowed, it does")
print("not prevent it.  math.fsum, which never rounds until the end, gets 2.0.")
print()

# --- conditioning --------------------------------------------------------------

print("condition numbers, where numpy can measure instead of you deriving:")
A_good = np.array([[3.0, 1.0], [1.0, 3.0]])
A_bad = np.array([[1.0, 1.0], [1.0, 1.0 + 1e-12]])
for name, A in [("well conditioned", A_good), ("nearly singular", A_bad)]:
    k = np.linalg.cond(A)
    print(f"   {name:<20} cond(A) = {k:.6e}   "
          f"singular values {np.linalg.svd(A, compute_uv=False)}")
print()
print("cond(A) is the ratio of the largest to the smallest singular value, which")
print("is the matrix generalisation of |x f'(x) / f(x)|.  A cond of 1e12 means")
print("the problem has thrown away 12 of your 16 digits -- which is what the")
print("previous block measured by perturbing b by one ulp.")
print()
b = np.array([2.0, 2.0 + 1e-12])
print(f"   solving A_bad x = b with np.linalg.solve:")
print(f"      {np.linalg.solve(A_bad, b)}")
print(f"   and with lstsq, which uses a least-squares / SVD path:")
print(f"      {np.linalg.lstsq(A_bad, b, rcond=None)[0]}")
print()
print("np.linalg.lstsq is the numpy answer to 'the problem is ill conditioned',")
print("and it is exactly what Lesson 38 and Lesson 40 are for.  It does not")
print("recover the true answer -- the information is gone -- but it returns")
print("the minimum-norm one instead of something enormous.")
print()

# --- root finding ---------------------------------------------------------------

print("root finding, and the tools that already know about the failure modes:")
from scipy.optimize import brentq

target = math.sqrt(2.0)
print(f"   the true sqrt(2) is {target!r}")
xs = np.linspace(0.0, 2.0, 21)
ys = xs**2 - 2.0
print(f"   brentq on [1, 2]           = {brentq(lambda t: t * t - 2, 1, 2)!r}")
print(f"   error                     = {abs(brentq(lambda t: t * t - 2, 1, 2) - target):.3e}")
print()
print("brentq is the safeguarded hybrid: a bisection skeleton with inverse")
print("quadratic and secant accelerants.  It cannot leave the bracket, which is")
print("why it never cycles the way plain Newton does on x^3 - 2x + 2.")
print()
print("The condition for brentq is the same one bisection needs, and checking it")
print("is a two-line job:")
f = lambda t: t**3 - 2 * t + 2
print(f"   f(-3)*f(0) = {f(-3) * f(0.0):.3f}  (<= 0, so a root is bracketed)")
print(f"   f(0)*f(3)  = {f(0.0) * f(3):.3f}  (> 0, so no sign change on [0, 3])")
print()
print("   brentq raises ValueError on the second pair, which is the correct")
print("   behaviour: refusing a bracket is how bisection-based methods stay")
print("   trustworthy.")
print()

# --- finite differences ---------------------------------------------------------

print("finite differences, and what scipy's defaults actually buy you:")
from scipy.optimize import approx_fprime

func = lambda t: np.sin(t) + 0.3 * t**2
x0 = np.array([1.3])
exact = math.cos(1.3) + 0.6 * 1.3
eps64 = np.finfo(np.float64).eps
print(f"   f'(1.3) = {exact!r}")
print()
print("   scipy.optimize.approx_fprime is a FORWARD difference, so the right")
print("   step for it is about sqrt(eps) rather than eps^(1/3):")
print(f"      {'rel_step':>12} {'approx':>22} {'rel err':>12}")
for rs in (None, 1e-6, 1e-8, 3.6e-8, 1e-10, eps64 ** (1 / 3)):
    d = approx_fprime(x0, func, rs)[0]
    label = "default" if rs is None else f"{rs:.1e}"
    print(f"      {label:>12} {d:>22.16f} {abs(d - exact) / exact:>12.3e}")
print()
print("   The default rel_step lands near 1e-8 and gives about 9 digits, which")
print("   is roughly what a forward difference can do.  Note that eps^(1/3),")
print("   the right step for a CENTRAL difference, is the wrong step here: at")
print(f"   {eps64 ** (1 / 3):.1e} it only reaches "
      f"{abs(approx_fprime(x0, func, eps64 ** (1 / 3))[0] - exact) / exact:.1e}.")
print()
print("   A central difference, with the step from the lesson's cube-root rule:")
print(f"      {'h':>10} {'rel err':>12}")
for h in (1e-3, 1e-4, 1e-5, 6.1e-6, 1e-6, 1e-7, 1e-9, 1e-12, 1e-16):
    d = (func(x0 + h) - func(x0 - h)) / (2 * h)
    print(f"      {h:>10.1e} {abs(d[0] - exact) / exact:>12.3e}")
print()
print("That last row is the one people get wrong.  A step of 1e-16 returns a")
print("relative error of 100%: f(x + 1e-16) == f(x), the numerator is zero, and")
print("nothing raises.  The best row is h = 6.1e-6, right where the lesson's")
print(f"cube-root rule put it (eps^(1/3) = {eps64 ** (1 / 3):.3e}), and it gives")
print("13 digits.  Move one decade in either direction and you have given up")
print("two or three digits; move four decades and the answer is meaningless.")
print()
print("   If you want more than about 11 digits reliably, use the complex step")
print("   on a polynomial, where it is exact:")
c = complex(1.3, 1e-30)
print(f"      f(x) = x^2 at x=1.3, h=1e-30")
print(f"      Im((x + ih)^2) / h = {(c ** 2).imag / 1e-30!r}")
print(f"      exact derivative    = {2 * 1.3!r}")
print()

# --- the summary numbers -------------------------------------------------------

print("summary of the constants this lesson turned on:")
print(f"   float64 eps        = {np.finfo(np.float64).eps:.6e}")
print(f"   float64 eps^(2/3)  = {np.finfo(np.float64).eps ** (2 / 3):.6e}"
      "  (central-difference floor)")
print(f"   float64 eps^(1/3)  = {np.finfo(np.float64).eps ** (1 / 3):.6e}"
      "  (the best h)")
print(f"   float32 eps        = {np.finfo(np.float32).eps:.6e}")
print(f"   2**53              = {2 ** 53}   (integers stop being exact here)")
```
```

## Common Mistakes

**Wrong.** Testing floats with `==`, or with a fixed absolute epsilon.

```python
import math

a, b, c = 0.1 + 0.2, 0.1 + 0.2, 0.3

print("the two computed values are equal:", a == b)
print("but neither equals the literal:  ", a == c)
print()
print("a fixed ABSOLUTE threshold, which is scale-dependent:")
for value in (1e-2, 1.0, 1e4):
    approx = value * (1 + 1e-9)
    print(f"   value {value:>8.0e}, abs error {abs(approx - value):.2e}, "
          f"same 1e-9 threshold {'passes' if abs(approx - value) < 1e-9 else 'FAILS'}")
print()
print("a RELATIVE threshold, which scales with the quantity:")
for value in (1e-2, 1.0, 1e4):
    approx = value * (1 + 1e-9)
    ok = math.isclose(approx, value, rel_tol=1e-9)
    print(f"   value {value:>8.0e}, rel error "
          f"{abs(approx - value) / value:.2e}, isclose(rel_tol=1e-9) {ok}")
print()
print("math.isclose(0.1 + 0.2, 0.3) =", math.isclose(a, c, rel_tol=1e-9))
```

Why the wrong version is tempting: `==` is the reflexive test, and a fixed
`abs(...) < eps` looks like it accounts for rounding. It does not account for
it *correctly*: 1e-9 absolute is 1e-10 relative on a value of 10 and 1e-7
relative on a value of 1e-2, so one threshold cannot be right for both. And
`==` fails for ordinary arithmetic, not for exotic inputs.

---

**Wrong.** Choosing a finite-difference step as small as possible.

```python
import math

EPS = 2.0**-52
f = math.sin
X = 1.3


def central(x, h):
    return (f(x + h) - f(x - h)) / (2.0 * h)


exact = math.cos(1.3)
print(f"{'h':>10} {'f(x+h) == f(x)':>16} {'central difference':>20} {'rel err':>10}")
for h in (1e-3, 1e-5, 1e-7, 1e-9, 1e-12, 1e-16, 1e-20):
    d = central(X, h)
    print(f"{h:>10.0e} {str(f(X + h) == f(X)):>16} {d:>20.16f} "
          f"{abs(d - exact) / abs(exact):>10.3e}")
print()
good = (3.0 * EPS * abs(f(X))) ** (1.0 / 3.0)
print(f"the cube-root rule picks h = {good:.3e}, giving a relative error of "
      f"{abs(central(X, good) - exact) / abs(exact):.3e}")
print(f"h = 1e-16 gives a relative error of "
      f"{abs(central(X, 1e-16) - exact) / abs(exact):.3e}")
print()
print("A step of 1e-16 looks maximally careful and returns 0.0, because")
print("f(1.3 + 1e-16) is bit-for-bit f(1.3) and the numerator vanishes.")
```

Why the wrong version is tempting: a smaller step looks like a more faithful
approximation of the defining formula, and it is exactly what you would write
if you were thinking of the derivative as a limit. But the finite-difference
formula assumes the subtraction is exact, and below the spacing of $f$ it is
not. The error curve has a finite minimum and you are past it.

---

**Wrong.** Running plain Newton and hoping the starting point is good.

```python
import math


def f(x):
    return x**3 - 2.0 * x + 2.0


def df(x):
    return 3.0 * x * x - 2.0


def plain_newton(x0, n=12):
    x = x0
    path = []
    for _ in range(n):
        x = x - f(x) / df(x)
        path.append(x)
    return x, path


def safeguarded_newton(a, b, n=12):
    fa = f(a)
    x = 0.5 * (a + b)
    path = []
    for _ in range(n):
        fx = f(x)
        if fa * fx < 0.0:
            b = x
        else:
            a, fa = x, fx
        step = x - fx / df(x)
        x = step if a < step < b else 0.5 * (a + b)
        path.append(x)
    return x, path


print(f"{'n':>3} {'plain Newton from x0=0':>26} {'safeguarded from [-3,0]':>26}")
p, ppath = plain_newton(0.0)
s, spath = safeguarded_newton(-3.0, 0.0)
for i in range(12):
    print(f"{i:>3} {ppath[i]:>26.17f} {spath[i]:>26.17f}")
print()
print(f"plain Newton ends at {p!r}, and |f(x)| there is {abs(f(p)):.3e}"
      f" -- it never converged")
print(f"safeguarded ends at {s!r}, |f(x)| = {abs(f(s)):.3e}")
print(f"the true root is near {plain_newton(-2.0, 40)[0]!r}")
```

Why the wrong version is tempting: Newton is quadratically convergent, which
makes it look like the obviously superior algorithm, and on a well-behaved
function it is. But quadratic convergence is a *local* claim, and nothing in
the plain loop checks that the iterate is still inside the region where it
applies. Here the tangent at 0 crosses the axis at 1 and the tangent at 1
crosses it back at 0, forever.

---

**Wrong.** Treating a near-singular system as a precision problem.

```python
import math


def solve2(A, b):
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return ((b[0] * A[1][1] - A[0][1] * b[1]) / det,
            (A[0][0] * b[1] - b[0] * A[1][0]) / det)


def ridge(A, b, lam):
    n = len(A)
    AtA = [[sum(A[k][i] * A[k][j] for k in range(n)) + (lam if i == j else 0.0)
            for j in range(n)] for i in range(n)]
    Atb = [sum(A[k][i] * b[k] for k in range(n)) for i in range(n)]
    return solve2(AtA, Atb)


eps = 1e-12
A = [[1.0, 1.0], [1.0, 1.0 + eps]]
b = [2.0, 2.0 + eps]
perturbed = [b[0], b[1] + math.ulp(b[1])]

# Wrong: spend effort adding precision.  In float64 there is none to add, and
# in a wider type the AMPLIFICATION of 2/eps is unchanged, so you gain a fixed
# number of digits and then the same disaster returns.
print(f"condition number ~ 2/eps = {2 / eps:.3e}")
print(f"float64 gives you about 16 digits, so you keep about "
      f"{16 - math.log10(2 / eps):.0f}")
print(f"a 34-digit type would give you about {34 - math.log10(2 / eps):.0f}"
      " -- and break again when eps shrinks by the same factor")
print()
# Right: change the problem.  A ridge term makes the answer insensitive to the
# perturbation, in exchange for a small deliberate bias.
for label, bb in (("clean b", b), ("b perturbed by 1 ulp", perturbed)):
    plain = solve2(A, bb)
    ridged = ridge(A, bb, 1e-4)
    print(f"{label:<22} plain {[round(v, 9) for v in plain]}   "
          f"ridge {[round(v, 9) for v in ridged]}")
print()
print("The plain answer jumps by 1e-3 on a one-bit input change.  The ridge")
print("answer is identical either way, and both differ from [1, 1] by a")
print("predictable 3.5e-5.  Bounded bias instead of unbounded noise.")
```

Why the wrong version is tempting: the answer is wrong, and "wrong" usually
sounds like "not enough precision". But the condition number says the problem
multiplies whatever error you feed it by $2/\varepsilon$, and widening the type
does not shrink that ratio -- it only moves the cliff. Regularisation changes
the problem on purpose and accepts a known bias in exchange for stability,
which is the trade that actually helps.
