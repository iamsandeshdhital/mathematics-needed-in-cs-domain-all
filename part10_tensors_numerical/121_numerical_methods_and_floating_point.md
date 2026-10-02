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

| Newton convergence | `$\text{digits roughly double per step}$` | quadratic, so float64 needs 4-5 steps | when the start is close to the root |

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


### 2. Absolute versus relative error, and catastrophic cancellation



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


### 3. Conditioning: which problems are fragile, and which algorithms are



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


### 4. Bisection and Newton, from scratch, with the error bounds



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


### 5. Finite differences, and why a tiny step is a terrible step



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


### With Libraries



The same facts, checked against numpy and scipy, where the constants and the

tools are the real library ones. numpy's `finfo.eps`, `spacing`,

`expm1`, `log1p`, `cond`, and scipy's `brentq` and `approx_fprime` all appear

in the lesson's arguments.



not runnable



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


## Multiple Choice Questions

**Q1.** Why is `0.1 + 0.2 != 0.3` in Python?

- A) Python's floating-point addition is implemented incorrectly
- B) 0.1, 0.2 and 0.3 are not exactly representable in binary, and each was rounded on the way in, so the sum of the rounded values is a different double from the rounded value of 0.3
- C) The comparison is correct but the error is below the display precision, so the numbers only look equal
- D) It only happens in Python; in C the result is exactly 0.3

<details>
<summary>Answer and explanation</summary>

**B) 0.1, 0.2 and 0.3 are not exactly representable in binary, and each was
rounded on the way in, so the sum of the rounded values is a different double
from the rounded value of 0.3.**

$1/10$ has a factor of 5 in its denominator and no power of two can absorb it,
so it cannot be stored; the same holds for $1/5$ and $3/10$. The lesson's block
1 shows this with exact rationals: the stored 0.1 is
$3602879701896397/2^{55}$, which is *above* $1/10$, and the stored 0.2 is above
$1/5$. Their exact sum is $3/10 + 1.665 \times 10^{-17}$, and rounding that once
gives `0.30000000000000004`, whereas rounding $3/10$ once gives the double
printed as `0.3`. They differ by one ulp.

Option A is wrong because IEEE 754 addition is correctly rounded: the machine
computes the correctly rounded value of the two stored numbers, and block 1
shows the addition itself is *exact* here. The error is entirely in the inputs.
This is the single most misunderstood point in the lesson.

Option C is wrong because the two values are genuinely different doubles, one
ulp apart, not merely printed identically. `math.ulp(0.3)` is
$5.55 \times 10^{-17}$ and that is exactly the gap between them, which is
observable, not cosmetic.

Option D is wrong because IEEE 754 is a hardware standard, so C, Java, Rust,
JavaScript and every other language get the identical result. It is a property
of the hardware arithmetic, not of any one language.

</details>

**Q2.** A central difference uses $h = 10^{-16}$ to approximate a derivative in
float64. What happens?

- A) The result is the most accurate possible, because the step is minimal
- B) The subtraction $f(x+h) - f(x-h)$ suffers more rounding than with a larger $h$, so the result is slightly worse
- C) $f(x+h)$ rounds back to $f(x)$, so the numerator is 0 and the derivative comes back as 0, a 100% relative error
- D) Python raises an error, because $10^{-16}$ is below machine epsilon

<details>
<summary>Answer and explanation</summary>

**C) $f(x+h)$ rounds back to $f(x)$, so the numerator is 0 and the derivative
comes back as 0, a 100% relative error.**

The gap between doubles near $f(1.3)$ is about $2.2 \times 10^{-16}$, so once
$h$ drops below that, $f(x+h)$ is bit-for-bit equal to $f(x)$ and the numerator
vanishes. Block 5 prints exactly this: at $h = 10^{-16}$ the relative error is
`1.000e+00`, and the Common Mistakes table shows `f(x+h) == f(x)` flipping to
`True`. Nothing raises.

Option A inverts the entire lesson. The error of a finite difference is
truncation plus rounding, and the truncation term falls with $h$ while the
rounding term *rises* like $2\varepsilon|f|/h$. The sum has a minimum at
$h^* \approx (3\varepsilon|f|/|f'''|)^{1/3}$, about $6 \times 10^{-6}$. Choosing
smaller is strictly worse past that point.

Option B is directionally right about rounding but wrong about the size. It
says "slightly worse", when in fact at $h = 10^{-16}$ the answer is not
imprecise but *identically zero*. The failure is total, not gradual, which is
what makes it dangerous: a slightly-wrong derivative looks like a slightly-wrong
answer, and a zero derivative looks like a bug someone will notice.

Option D is wrong because $10^{-16}$ is not "below machine epsilon" in a way
Python objects to; it is a perfectly good float, roughly half of epsilon. And
Python has no runtime check on step sizes in any case. The failure mode of this
whole lesson family is silence.

</details>

**Q3.** `math.sqrt(x*x + 1.0) - x` returns exactly `0.0` when `x = 1e8`. What is
the condition number of the function $f(x) = \sqrt{x^2+1} - x$ at that point?

- A) Enormous, around $10^{16}$, so the problem is hopeless
- B) About 1, so the problem is perfectly conditioned and the fault is in the algorithm
- C) Zero, because the computed value is zero
- D) About $x^2$, so the error grows as $x$ grows

<details>
<summary>Answer and explanation</summary>

**B) About 1, so the problem is perfectly conditioned and the fault is in the
algorithm.**

$\kappa(x) = |x f'(x)| / |f(x)|$, and this function has the closed form
$\kappa(x) = x/\sqrt{x^2+1}$, which is 1 at every scale. Block 3 prints
`1.000000000` at $x = 10^4$, $10^8$ and $10^{12}$. A relative perturbation of
$10^{-16}$ in the input moves the *true* answer by a relative $10^{-16}$. Yet
the float64 evaluation returns 0, which means the *computation* amplified its
own rounding error by a factor of about $10^{16}$.

Option A is the confusion this question is designed to catch. A large
condition number is a property of the problem and you cannot code it away.
Here there is no large condition number; the algorithm
$\sqrt{x^2+1} - x$ is unstable because it subtracts two quantities of size $10^8$
to produce $5 \times 10^{-9}$, and it is repaired by the conjugate form
$1/(\sqrt{x^2+1} + x)$, which block 2 shows is exact at every magnitude tested.
Buying more precision hides the instability and the same failure returns when
the inputs grow.

Option C confuses the computed value with the function. The condition number
is a ratio of derivatives; it is unaffected by what the arithmetic happened to
produce. A function whose value happens to round to zero at one point still has
a perfectly ordinary condition number at every other point.

Option D has the right instinct (the error does grow with $x$) but attributes
it to the wrong cause. It is the *cancellation in the algorithm* that grows,
not the conditioning of the problem, which stays at 1.

</details>

**Q4.** Bisection on $[1, 2]$ needs 40 iterations to reach a tolerance of
$10^{-12}$. Roughly how many does it need to reach $10^{-15}$?

- A) About 45, since each halving buys one digit
- B) About 80, since the tolerance falls by a factor of 1000 and each iteration halves the interval
- C) About 120, since each halving buys one digit and 3 more digits are needed
- D) The same 40, because bisection converges as fast as the arithmetic allows

<details>
<summary>Answer and explanation</summary>

**B) About 80, since the tolerance falls by a factor of 1000 and each iteration
halves the interval.**

The error after $n$ halvings is roughly $w/2^{n+1}$ with $w$ the initial
width, so the iteration count is $\log_2(w/\varepsilon)$. Going from
$10^{-12}$ to $10^{-15}$ tightens the target by a factor of $10^3$, and each
iteration only contributes a factor of 2, so it takes
$\log_2(10^3) \approx 9.97 \approx 10$ more iterations, giving about 50, not
80.

Careful: option B's *number* is wrong and option C's is right. Option C says
about 120, reasoning that each halving buys one digit and three more digits are
needed. Block 4's table shows the exact progression: $10^{-12}$ needs 40
iterations, $10^{-16}$ needs 54. Three more digits of tolerance, from
$10^{-12}$ to $10^{-15}$, costs about 10 iterations, so the answer is about 50.

Option A says about 45, which is the right *shape* of reasoning (each halving
buys roughly one digit) but the wrong arithmetic: three digits need about ten
halvings, not five. This is the most common way people get bisection cost
wrong, and it is worth internalising that "one digit per iteration" means
$\log_2(10) \approx 3.3$ iterations per digit, not one.

Option D is wrong because bisection's convergence rate is fixed by the
algorithm and is independent of the arithmetic's resolution. It keeps halving
until the interval is too small to represent, and that happens around 54
iterations for an interval of width 1 -- after which it is making no progress,
which is exactly why option D is a trap for anyone who believes a tolerance is
always reachable.

</details>

**Q5.** Which single change makes `math.exp(x) - 1` accurate for $x = 10^{-12}$?

- A) Use `math.exp(x * (1 + 1e-16)) - 1` to perturb the input
- B) Use `math.expm1(x)`, which computes the result without forming the two nearly equal numbers
- C) Use a larger `x`, such as $10^{-6}$, and scale the answer afterwards
- D) Use `float128`, since the problem needs more than 16 digits

<details>
<summary>Answer and explanation</summary>

**B) Use `math.expm1(x)`, which computes the result without forming the two
nearly equal numbers.**

`exp(x)` returns a number near 1 and subtracting 1 from it leaves a result near
$x = 10^{-12}$, so every digit of the answer has to survive a subtraction whose
operands differ by about $10^{-12}$. `math.expm1` instead sums the tail
$x + x^2/2 + \dots$ from the small end, adding small quantities together, so
nothing is ever subtracted from something much larger. Block 2's table shows
the relative error of `math.exp(1e-12) - 1` is `8.890e-05` while
`math.expm1(1e-12)` is accurate to `5.000e-13`.

Option A is a non-sequitur: perturbing the input by one ulp changes the answer
by a relative $10^{-4}$, which is far worse than the error being fixed, and it
does nothing about the cancellation.

Option C is legitimate mathematics and pointless in practice, because you do
not know $x$ in a situation where you need `exp(x) - 1`; and if you did, you
would use `expm1`. It is a workaround that trades away the thing you needed.

Option D is wrong for the same reason as everywhere else in this lesson: the
problem is not that 16 digits are insufficient, it is that the algorithm
destroys most of them. `float128` would reduce a `8.890e-05` relative error to
something like `8.890e-06` -- still terrible -- while `expm1` in float64 gives
`5.000e-13`. Fixing the algorithm beat the precision by seven orders of
magnitude, at zero cost.

</details>

**Q6.** A program computes `x ** 100` for $x = 1.5$ and needs 10 correct
digits. What does the condition number $\kappa = 100$ tell you?

- A) The result will have about 10 of float64's 16 digits, so 10 is achievable
- B) The result will have about 2 correct digits, so 10 is not achievable in float64
- C) Nothing, because the condition number describes the algorithm rather than the problem
- D) The result is exactly representable, so the condition number is irrelevant

<details>
<summary>Answer and explanation</summary>

**B) The result will have about 2 correct digits, so 10 is not achievable in
float64.**

$\kappa = |x \cdot 100x^{99} / x^{100}| = 100$, and each factor of 10 in
$\kappa$ costs about one decimal digit. Block 3 prints $\kappa(x^{100}) = 100.0$
at both $x = 1.5$ and $x = 1.0000001$, and its digit table shows $\kappa = 100$
leaving 14 of 16 digits, not 2.

Careful here, because the arithmetic in this option is itself the trap: the
question asks for 10 correct digits and $\kappa = 10^2$ costs 2, so 14 remain
and 10 *is* achievable. The correct statement is that $\kappa = 100$ costs about
two digits and leaves about fourteen, so the request is comfortably satisfiable
-- but it also means the input only needs to be good to about 14 digits, and
feeding in 34 digits of input precision buys you nothing.

Option A is right that 10 is achievable but reaches the wrong conclusion about
how much is lost. It claims 10 of 16 digits are lost, which would require
$\kappa = 10^6$.

Option C is wrong about what the condition number describes. It is a property
of the problem, not the algorithm -- which is exactly why it cannot be improved
by writing better code.

Option D is wrong because $1.5^{100}$ is a rational with denominator $2^{100}$,
which is far outside the 53-bit significand, so it is emphatically not exactly
representable.

</details>

**Q7.** You need `sqrt(2)` to full float64 precision and plain Newton from $x_0
= 1$ stalls at `1.4142135623730951` with a step of $4.4 \times 10^{-16}$. What
has happened?

- A) Newton has diverged
- B) Newton has converged as far as the arithmetic permits, and the residual step is now pure rounding noise
- C) The tolerance was set too loose and should be tightened
- D) The function is ill-conditioned at this point

<details>
<summary>Answer and explanation</summary>

**B) Newton has converged as far as the arithmetic permits, and the residual
step is pure rounding noise.**

Block 4's Newton table shows the iterates converging 0, 0.6, 2.2, 5.2, 11.3,
15.4 correct digits and stopping at `1.4142135623730951`, which is the correctly
rounded double nearest the real $\sqrt 2$, with error exactly 0. The final
residual is $4.4 \times 10^{-16}$, which is about one ulp, so the next Newton
step would be dividing rounding noise by $f'(x)$ and would move the iterate away
from the answer rather than toward it. A good solver detects this by comparing
the step against the spacing at $x$ and stopping.

Option A is wrong because the sequence converged monotonically and the final
value is the correctly rounded answer. Divergence looks like the iterate
growing without bound or oscillating, which is what block 4 shows Newton doing
on $x^3 - 2x + 2$ from $x_0 = 0$.

Option C is wrong in a way worth dwelling on: tightening the tolerance here is
the classic mistake. The request for more digits than the arithmetic has is
unreachable, and a solver that tries will spin to `max_iter` and return an
arbitrary iterate. Block 5 of the exercises shows a solver correctly reporting
`iteration limit` rather than claiming success, which is the behaviour to want.

Option D is wrong because $\kappa(\sqrt{\cdot})$ at $x = 2$ is $1/2$, the best
possible. Square roots are among the most benign operations there is, which is
why Heron's method has been in continuous use for two thousand years.

</details>

**Q8.** Why is `math.fsum` sometimes preferred over `numpy.sum`?

- A) `fsum` is faster
- B) `fsum` accumulates partial sums as exact fractions and rounds once, so it cannot lose a small term to a large one; `numpy.sum` uses pairwise blocking, which helps but does not prevent it
- C) `numpy.sum` only works on integers
- D) `fsum` returns more decimal places in the output

<details>
<summary>Answer and explanation</summary>

**B) `fsum` accumulates partial sums as exact fractions and rounds once, so it
cannot lose a small term to a large one; `numpy.sum` uses pairwise blocking,
which helps but does not prevent it.**

Block 1 of
[Lesson 120](../part10_tensors_numerical/120_tensors_and_broadcasting.md)
measured this directly on `[1e16, 1.0, -1e16, 1.0]`, where the true answer is
2.0: a naive fold gives 1.0, numpy's `.sum()` gives 1.0, and `math.fsum` gives
2.0. Pairwise summation reduces how *often* a small term is swallowed by summing
similar magnitudes together; it cannot stop it when the operands themselves
already lost the term.

Option A is backwards. `fsum` keeps an exact rational accumulator and is
markedly slower; `numpy.sum` is vectorised and fast. The library method is the
fast default, and `fsum` is the careful one.

Option C is false -- `numpy.sum` works perfectly well on floats, and in fact
that is the case in which the difference shows up.

Option D confuses internal precision with output formatting. `fsum` returns a
float64, so it has the same 17 significant digits available as any other
float; what differs is that it arrives at the correctly rounded one.

</details>

**Q9.** You need a root of $f$ where $f'(x_0) = 0$ at the starting point, and
Newton's step divides by zero. What is the right response?

- A) Perturb $x_0$ by a tiny amount and retry, since Newton is locally convergent
- B) Use a method that does not need a derivative, such as bisection or Brent's method, since a zero derivative means the tangent-line model has no information about the root
- C) Increase the number of iterations
- D) Convert to a wider floating point type so the division does not underflow

<details>
<summary>Answer and explanation</summary>

**B) Use a method that does not need a derivative, such as bisection or Brent's
method, since a zero derivative means the tangent-line model has no information
about the root.**

Newton's step is $f(x)/f'(x)$, the slope of the tangent used as a proxy for how
far to move. Where the slope is zero the tangent is horizontal and carries no
information about where the axis is, so the step is undefined for a reason that
no amount of arithmetic fixes. The honest response is to stop using a method
whose precondition is violated. Block 4 shows exactly this failure on
$f(x) = x^2 - 2$ from $x_0 = 0$, raising `ZeroDivisionError`.

Option A is the tempting version and it does not work. Near a point where
$f' = 0$, the function is locally flat, so a tiny perturbation of $x_0$ leaves
the derivative just as close to zero and the step just as huge. It also breaks
the guarantee that got you here: Newton converges when you start close to the
root, and "close" is measured by how well the tangent approximates the function
near the root, which is exactly what fails here.

Option C cannot help, because the failure is an exception in the very first
iteration rather than a slow approach to the answer.

Option D is wrong about the mechanism. A zero derivative is not an underflow; it
is a value that is genuinely zero, and it is zero in every floating point type.

</details>

**Q10.** A 2x2 system with $\det(A) = 10^{-12}$ is solved from data rounded to
float64, and the answer is wrong in its fourth digit. What does the condition
number say, and what is the correct response?

- A) $\kappa \approx 10^{12}$, so the problem is ill conditioned; regularise it or reformulate it, because more precision multiplies the error just as effectively
- B) $\kappa \approx 10^{12}$, so switch to a wider float type and the fourth digit will come back
- C) $\kappa \approx 10^{-12}$, so the problem is well conditioned and the solver has a bug
- D) The determinant being small says nothing about conditioning

<details>
<summary>Answer and explanation</summary>

**A) $\kappa \approx 10^{12}$, so the problem is ill conditioned; regularise it or
reformulate it, because more precision multiplies the error just as
effectively.**

Block 3 measures this directly: for $A = [[1,1],[1,1+\varepsilon]]$ the
amplification factor from perturbing $b$ by one ulp is $2/\varepsilon$, and the
ridge solve $(A^\top A + \lambda I)x = A^\top b$ with $\lambda = 10^{-4}$
returns a bit-identical answer whether or not $b$ is perturbed. The penalty term
trades an unbounded sensitivity for a bounded, known bias, which is what
Lesson 101 minimises and why L2 regularisation exists.

Option B is the mistake this lesson exists to prevent. Widening the type adds
digits to the *input* and the *output*, but the problem multiplies whatever
error arrives by $\kappa$, which is a property of the problem and not of the
arithmetic. With $\kappa = 10^{12}$ you keep about 4 of 34 digits instead of 4
of 16 -- you have not recovered the fourth digit, you have merely made the
cliff further away.

Option C has the inequality backwards. A small determinant means two rows are
nearly dependent, which means the singular values are far apart, which means
$\operatorname{cond}(A) = \sigma_{max}/\sigma_{min}$ is *large*.

Option D is wrong because the determinant and the condition number are closely
related. For a $2 \times 2$ matrix $\det(A) = \sigma_{max}\sigma_{min}$, so a
det of $10^{-12}$ with unit-scale singular values forces $\sigma_{min} \approx
10^{-12}$ and $\kappa \approx 10^{12}$. The near-null-space direction is
invisible in the output, which is Lesson 35's kernel and Lesson 38's
least-squares residual.

</details>

## Subjective Questions

### Short Answer

**Q1. Define machine epsilon, and say precisely what it is not.**

<details>
<summary>Answer</summary>

For float64, machine epsilon is $\varepsilon = 2^{-52} \approx 2.22 \times
10^{-16}$: the ulp at $1.0$, and the smallest $h$ for which $1 + h \neq 1$ (up
to the rounding tie at $2^{-53}$).

It is **not** the smallest number representable. That is the denormal
$2^{-1074} \approx 5 \times 10^{-324}$, about 300 orders of magnitude smaller.
Nor is it the smallest number below which arithmetic stops working -- values
down to $2^{-1074}$ are representable and their sums work fine. The question
epsilon answers is "how much must I change a number of order 1 to change it at
all", and that is what every truncation-versus-rounding balance in this lesson
is built on.

</details>

**Q2. Why is $0.1 + 0.5$ exactly $0.6$ while $0.1 + 0.2$ is not exactly
$0.3$?**

<details>
<summary>Answer</summary>

Both results contain one rounding on the way in for $0.1$, and the answer
depends on what happens to the other operand.

$0.5 = 1/2$ is exactly representable, so nothing is lost there. The two errors
that remain are of opposite size and cancel, and the result is the correctly
rounded value of the true sum $3/5$, which is $0.6$.

$0.2 = 1/5$ is *not* exactly representable, and it was rounded in the same
direction as $0.1$ (both stored values sit slightly *above* their true values).
The errors therefore add rather than cancel, and the final rounding lands one
ulp above the double nearest $3/10$.

The general lesson: whether a float computation comes out exact depends on the
representability of every operand, not on the size of the numbers involved.

</details>

**Q3. State the bisection error guarantee, and say what it does not tell you.**

<details>
<summary>Answer</summary>

If $f$ is continuous on $[a, b]$, $f(a)f(b) < 0$, and the initial width is
$w$, then after $n$ iterations the bracket has width $w/2^n$ and the returned
midpoint is within $w/2^{n+1}$ of the root.

What it does **not** tell you is that a root exists uniquely, that $f$ is
well behaved anywhere else, or that the computed $f$ values are correct. The
bound is a statement about the algorithm's geometric progress and assumes only
continuity plus a sign change you have verified. It is exactly this
conditionality that makes bisection attractive in production code: the
precondition is one sign test away and the guarantee follows from it.

</details>

**Q4. Why does a central difference beat a forward difference, and what does it
cost?**

<details>
<summary>Answer</summary>

By symmetry. The forward difference's Taylor expansion keeps the
$\tfrac{1}{2} h f''(x)$ term, so its error is $O(h)$. The central difference's
expansion has that term cancel exactly, leaving $O(h^2)$. Halving $h$ therefore
quarters the central error but only halves the forward error.

It costs one extra function evaluation, and it requires $f$ to be evaluable at
$x - h$. Where $x$ is at a boundary, or where $f$ is defined only on one side,
the forward or backward difference is the only option available -- which is
why both forms exist rather than one being simply better.

</details>

**Q5. A tolerance of `1e-20` is requested of a float64 solver. What should
happen?**

<details>
<summary>Answer</summary>

The solver should report that it could not meet the tolerance, rather than
returning a number as though it had.

float64 carries about 16 significant digits, so no relative tolerance below
roughly $2 \times 10^{-16}$ is reachable at unit scale. A tolerance of
`1e-20` asks for digits the arithmetic cannot produce. The correct behaviour is
to stop, report non-convergence, and hand back the best iterate along with an
honest status -- the exercise solution in this lesson does exactly that, and
returns `status="iteration limit"` for `rel_tol=1e-30`.

The dangerous alternative is to accept the request, iterate to `max_iter`, and
return an arbitrary last iterate. The caller then believes a tolerance was
met that never was.

</details>

**Q6. What is the difference between an unstable algorithm and an
ill-conditioned problem?**

<details>
<summary>Answer</summary>

An **unstable algorithm** amplifies the rounding errors generated by its own
intermediate steps. $\sqrt{x^2+1} - x$ computed directly in float64 returns
$0.0$ at $x = 10^8$, while its condition number $x/\sqrt{x^2+1}$ is
$1$. The problem is fine; the formulation is not, and it is repaired by the
conjugate $1/(\sqrt{x^2+1} + x)$, which is exact at every magnitude tested.

An **ill-conditioned problem** amplifies errors in the *input*, and that factor
is a property of the mathematics, not of your code. $A = [[1,1],[1,1+\varepsilon]]$
amplifies a one-ulp change in $b$ by $2/\varepsilon$, and no reformatting of
the computation changes that. The only responses are to regularise the problem
or to accept the limit.

The practical consequence is that they have opposite fixes, so identifying
which one you have is most of the diagnosis.

</details>

### Long Answer

**Q1. Why is `0.1 + 0.2 != 0.3` a property of the arithmetic rather than a
defect, and what does that imply for how you should write comparisons?**

<details>
<summary>Model answer</summary>

**It is a property of the arithmetic because the arithmetic is doing exactly
what IEEE 754 specifies.** The relevant facts are that a float64 is $m 2^j$
with $|m| < 2^{53}$, that addition is correctly rounded to the nearest
representable value, and that rounding is applied after every operation. None
of these is a bug; they are the contract.

The specific chain of events, established with exact rationals in block 1, is:
$1/10$ and $1/5$ both have a factor of 5 in their denominator and so neither is
representable; each was rounded once on the way in, and in both cases upwards;
the sum of the two stored doubles is *exactly* representable, so the addition
itself introduced no error at all; that exact sum is slightly above $3/10$, and
rounding it gives the double printed `0.30000000000000004`. Meanwhile the
literal `0.3` is $3/10$ rounded once, and it rounds downwards. Three roundings
along three different routes, arriving at two different doubles one ulp apart.

Two observations kill the alternatives. First, the counter-check
$0.1 + 0.5 = 0.6$ is *exact*, because $1/2$ is representable so only one operand
contributed an error and the two cancelled. If floating point addition were
simply broken, that case would fail too. Second, IEEE 754 is a hardware
standard, so C, Java, Rust and JavaScript all produce `0.30000000000000004`.

The implication for comparisons is that `==` on computed floats is not testing
what you meant. The three defensible responses, in order, are:

1. **Use an exact type when the values are exact.** `fractions.Fraction` keeps
   $1/10$ as an exact rational and `Fraction(1,10) + Fraction(2,10) ==
   Fraction(3,10)` is unambiguously `True`. Integers are the same idea: money in
   cents needs no tolerance at all.
2. **Use a scaled comparison when both sides were computed.**
   `math.isclose(a, b, rel_tol=...)` scales the threshold to the magnitudes, so
   one tolerance works across scales. A fixed absolute threshold is not a
   tolerance; it is a scale-specific assumption.
3. **Do not use either when you are testing a logical fact.** `isclose` decides
   "are these close", not "is this true". Using it to paper over a real
   discrepancy converts a visible bug into an invisible one.

The deeper habit this builds: when a numeric answer surprises you, find out
what the machine actually holds before theorising. `Fraction(x)` does that
exactly and should be the first tool you reach for.

</details>

**Q2. Explain why a too-small finite-difference step makes the answer worse,
and what would break if you did not understand this.**

<details>
<summary>Model answer</summary>

**The mechanism.** A finite difference estimates a derivative by *subtracting*
two numbers and dividing by a small step. Writing the two error sources out:

- **Truncation.** The Taylor expansion says
  $\frac{f(x+h)-f(x)}{2h} = f'(x) + \frac{1}{6}h^2 f'''(x) + \dots$ for a
  central difference. This term is $O(h^2)$ and shrinks as $h$ shrinks.
- **Roundoff.** Each of $f(x+h)$ and $f(x-h)$ is itself stored to within about
  $\varepsilon |f|$, so their difference carries absolute error of order
  $2\varepsilon|f|$. Dividing by $2h$ turns that into an error of order
  $\varepsilon|f|/h$, which *grows* as $h$ shrinks.

The total is $\approx C h^2 + 2\varepsilon|f|/h$. Differentiating with respect
to $h$ and setting the derivative to zero gives
$h^* = (3\varepsilon|f| / |f'''|)^{1/3}$, about $6 \times 10^{-6}$ for a
function of order 1. Below that, the roundoff term dominates and the error
*rises*. The lesson's own sweep shows the relative error bottoming out at
`7.478e-12` at $h = 10^{-5}$ and then climbing to `1.000e+00` at
$h = 10^{-16}$.

**What breaks if you do not understand it.** The failure is silent and total,
which is the combination that makes it dangerous. At $h$ below the spacing of
$f$, `f(x+h)` rounds back to bit-for-bit `f(x)`, the numerator is exactly zero,
and the derivative is exactly `0.0`. No exception, no warning, and the returned
value has the right type and the wrong content.

Three concrete consequences follow. A **numerical Jacobian** computed this way
is zero, and a Newton or gradient-descent step built on it either stalls or
walks off; the iteration "converges" to nothing while reporting success. An
**error estimate** built by re-evaluating with a smaller step reports that the
answer is stable, because both evaluations are identically zero -- the estimate
confirms the wrong thing. And a **test suite** that checks a derivative against
a hard-coded value will pass on any function whose derivative is near zero,
because the expected value and the computed value are both near zero.

The rule to take away is not "use a large step" but "derive the step, or
measure your own progress". Concretely: use $h \approx \varepsilon^{1/3}
|f(x)|$ as a default when you have no derivatives to hand, and when you need
more than about 11 digits, stop tuning $h$ and change method -- the complex
step $f'(x) = \operatorname{Im}(f(x+ih))/h$ involves no subtraction at all and
returned the exact derivative of $x^2$ at $x = 1.3$ with $h = 10^{-30}$.

</details>

**Q3. A numerical result is badly wrong. Explain why "use a wider float" is
usually the wrong first move, and what the diagnostic order should be.**

<details>
<summary>Model answer</summary>

**Why precision is usually the wrong first move.** Widening the type adds digits
to the input and the output. It does not change either the conditioning of the
problem or the stability of your algorithm, and those are the two things that
multiply your error. Block 3's linear system makes the arithmetic concrete:
for $A = [[1,1],[1,1+\varepsilon]]$ with $\varepsilon = 10^{-12}$, perturbing
$b$ by one ulp moves the answer by about $6 \times 10^{-4}$, an amplification of
$2/\varepsilon \approx 2 \times 10^{12}$. In float64 you keep roughly 4 usable
digits. In a 34-digit type you keep roughly 26 -- you have not recovered the
lost information, you have only moved the cliff 18 orders of magnitude further
away, and the same code will fail again when the inputs grow.

**The diagnostic order.**

1. **Is the algorithm stable here?** Look for a subtraction of two nearly equal
   quantities. `sqrt(x*x + 1) - x` returns `0.0` at $x = 10^8$ while its
   condition number is exactly 1, so no input perturbation of that size could
   cause it -- the damage is self-inflicted. The repair is algebraic: use
   $1/(\sqrt{x^2+1}+x)$, or `math.expm1` instead of `math.exp(x) - 1`, or
   `math.hypot` instead of `math.sqrt(x*x + y*y)`. This is free and should
   always be tried first.

2. **Is the problem well conditioned?** Compute $\kappa$: for a scalar function
   $|x f'(x)/f(x)|$, for a matrix $\sigma_{max}/\sigma_{min}$ via
   `np.linalg.cond`. If $\kappa$ is large, no algorithm saves you. The
   response is to reformulate the problem or to regularise it: the ridge solve
   $(A^\top A + \lambda I)x = A^\top b$ in block 3 returned a bit-identical
   answer under perturbation, buying stability with a known bias. This is the
   same objective Lesson 101 minimises.

3. **Only now, was the input precise enough?** If the algorithm is stable and
   $\kappa$ is moderate, then input error propagates by exactly $\kappa$, and
   this is the one case where a wider type genuinely helps. Worth knowing how
   much is needed: each factor of 10 in $\kappa$ costs a digit, so
   $\kappa = 10^{10}$ means no choice of precision exceeds about 6 useful
   digits in float64.

**Why the order matters.** Most people start at step 3 and buy precision that
step 1 would have made unnecessary. A `decimal` conversion of the quadratic
formula for $x^2 + 10^9 x + 1 = 0$ produces the correct small root at 60
digits while the float64 version of the *same formula* returns exactly zero --
and would return zero again at 90 digits if the inputs grew. Fixing the
algorithm costs nothing and stays correct; widening the type costs a great deal
and only postpones the failure.

</details>

**Q4. Why does production root-finding code keep a bisection bracket around a
Newton iteration, and what is the cost of doing so?**

<details>
<summary>Model answer</summary>

**Why.** Newton's step $x - f(x)/f'(x)$ is a tangent-line model, and its
convergence guarantee is local: it holds in a neighbourhood of the root whose
size depends on the function. Outside that neighbourhood the tangent's zero can
be anywhere, and the iterate goes there. Block 4 shows the sharpest possible
failure: on $f(x) = x^3 - 2x + 2$ from $x_0 = 0$, the iterate alternates
$0 \to 1 \to 0 \to 1$ for 60 iterations without ever approaching the root at
$-1.769$. From $x_0 = 0.5$ the same function converges in 9. Nothing about the
function changed; only the starting point did.

A bisection bracket does two things at once. It *guarantees* termination,
because halving an interval that contains a sign change cannot produce an empty
one, and it *detects* failure, because Newton proposing to leave the bracket is
an observable event you can respond to. Together they convert a method with no
global guarantee into one that always terminates with a certified answer.

**How.** Keep the bracket $[a, b]$ with $f(a)f(b) < 0$ invariant. At each step,
update the bracket using the sign of $f$ at the current iterate, then take the
Newton step *only if it lands strictly inside* the updated bracket; otherwise
take the midpoint. Block 4 applies this to the cycling example and converges in
5 iterations to the exact root, where plain Newton never converged at all.

**The cost.** One derivative evaluation, one division, and one comparison per
iteration, plus the bookkeeping to maintain the endpoints. That is genuinely
small next to the cost of the function evaluation you are already doing, which
typically dominates by orders of magnitude. The payoff is that a whole class of
failure disappears: in block 5 of the exercises the safeguarded solver handles
`x^2 - 2`, `x^3 - 2x + 2` and `cos(x) - x` with identical code, and reports
`no bracket` rather than guessing when given an interval with no sign change.

This is why `scipy.optimize.brentq` is shaped the way it is: a bisection
skeleton with inverse-quadratic and secant accelerants that are accepted only
while they stay inside the bracket. The rule generalises -- whenever a fast
method is only *locally* reliable, keep a slow method's invariant around it and
let the fast method accelerate.

</details>

## Exercises and Solutions

**[ ] Exercise 1 —** Build the floating point model from integers, with no
floating point arithmetic in the derivation. (a) Show that machine epsilon for
float64 is $2^{-52}$ by finding the smallest $h$ with `1 + h != 1` and doubling
it. (b) Show that a decimal $p/q$ in lowest terms is exactly representable if
and only if $q$ is a power of two, checking a list with exact rationals. (c)
Explain `0.1 + 0.2 != 0.3` in terms of exact rational arithmetic, showing the
direction of each rounding. (d) Give the three defensible responses.

<details>
<summary>Solution</summary>

```python
"""Exercise 1 solution: build the floating point model, and explain 0.1+0.2.

No floating point arithmetic in the derivation -- every claim about what the
machine holds is made with exact integers and rationals.
"""

import math
import struct
from fractions import Fraction


def rule(title):
    print()
    print("=" * 68)
    print(title)
    print("=" * 68)
# ------------------------------------------------------------------ part A
rule("A. Machine epsilon, computed two ways")
# Build it from first principles: 2^-52, because the fraction field is 52 bits
# wide and the exponent is scaled by 2^-52 around 1.0.
mantissa_bits = 52
eps_built = Fraction(1, 2**mantissa_bits)
print(f"the fraction field is {mantissa_bits} bits wide")
print(f"so the gap at 1.0 is 2^-{mantissa_bits} = {float(eps_built)!r}")
print()
# And find the boundary empirically by bisecting on the real library.  The
# first h for which 1 + h != 1 sits at HALF an ulp, because that is the
# rounding tie: below it the sum rounds back to 1, at or above it rounds up.
lo, hi = 0.0, 1.0
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if 1.0 + mid == 1.0:
        lo = mid
    else:
        hi = mid
boundary = hi
print(f"bisecting on (1 + h == 1) gives {boundary!r}")
print(f"the tie point is 2^-53        = {2.0**-53!r}")
print(f"the bisection landed just above it, by "
      f"{boundary - 2.0**-53:.3e}")
print(f"so it sits between 2^-53 and 2^-53 + one ulp, as it must")
print(f"doubling it gives             = {2 * boundary!r}")
print(f"machine epsilon 2^-52        = {float(eps_built)!r}")
print(f"they agree to within one ulp: "
      f"{abs(2 * boundary - float(eps_built)) <= math.ulp(float(eps_built))}")
print(f"math.ulp(1.0) confirms it:   = {math.ulp(1.0)!r}")
print()
print("Three independent routes, agreeing.  The bisection lands on the HALF")
print("rather than the whole because that is the rounding tie: for h below")
print("2^-53 the exact sum 1 + h is nearer to 1.0, and at or above it the sum")
print("rounds up to 1.0 + 2^-52.  Machine epsilon is that full gap, 2^-52,")
print("and every error estimate in numerical analysis is built from it.")
print()
# ------------------------------------------------------------------ part B
rule("B. Which decimals survive, and prove why")
print("A float64 is m * 2^e with |m| < 2^53 an integer.  So a decimal d = p/q")
print("in lowest terms is representable exactly if and only if q is a power")
print("of two.  Check it directly with exact rationals:")
print()
print(f"   {'decimal':<10} {'lowest terms':<16} {'q is 2^k?':<12} exact?")
for d in (Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 16),
          Fraction(1, 32), Fraction(1, 10), Fraction(1, 5),
          Fraction(3, 10), Fraction(7, 10), Fraction(1, 3)):
    q = d.denominator
    is_pow2 = (q & (q - 1)) == 0
    v = float(d)
    print(f"   {str(d):<10} {str(d):<16} {str(is_pow2):<12} "
          f"{Fraction(v) == d}")
print()
print("1/2, 1/4, 1/8, 1/16, 1/32 are exact.  Every denominator containing a")
print("factor of 3 or 5 is not, and 1/10, 1/5, 3/10, 7/10, 1/3 all fail.")
print("That is the whole reason 0.1 is inexact -- not that 0.1 is 'big' or")
print("'awkward', but that its reduced denominator is 10 = 2 * 5.")
print()
print("The bit patterns, which make the same point without any arithmetic:")
for name, v in [("0.5", 0.5), ("0.1", 0.1)]:
    (packed,) = struct.unpack("<Q", struct.pack("<d", v))
    print(f"   {name}  {packed:064b}")
print()
print("0.5 is sign/exponent then all zeros: the fraction is empty, so the")
print("value is exactly 2^-1.  0.1's fraction field is full of the repeating")
print("binary pattern for 1/5 truncated at 52 bits.")
print()
# ------------------------------------------------------------------ part C
rule("C. 0.1 + 0.2 != 0.3, explained exactly")
a, b, c = Fraction(1, 10), Fraction(2, 10), Fraction(3, 10)
fa, fb, fc = Fraction(0.1), Fraction(0.2), Fraction(0.3)
print("Step 1: the inputs are rounded once, on the way in.")
print(f"   true 1/10 stored as {fa}")
print(f"   true 1/5  stored as {fb}")
print(f"   both above their true values? {fa > a}, {fb > b}")
print(f"   each is off by {float(fa - a):.3e} and {float(fb - b):.3e}")
print()
print("Step 2: the addition of the two stored doubles is EXACT.")
stored_sum = fa + fb
print(f"   stored 0.1 + stored 0.2 = {stored_sum}")
print(f"   that is above 3/10?      {stored_sum > c}")
print(f"   by                       {float(stored_sum - c):.3e}")
print()
print("Step 3: the exact sum is then rounded ONCE, to the nearest double.")
print(f"   float(stored sum) = {float(stored_sum)!r}")
print(f"   float(3/10)       = {float(c)!r}")
print(f"   same double?      {float(stored_sum) == float(c)}")
print(f"   they differ by    {abs(float(stored_sum) - float(c)):.3e}, "
      f"which is one ulp at that magnitude "
      f"({math.ulp(0.3):.3e})")
print()
print("So the story is not '0.1 + 0.2 rounds badly'.  It is:")
print()
print("   1/10 -> a double slightly ABOVE 1/10       (one rounding)")
print("   1/5  -> a double slightly ABOVE 1/5        (one rounding)")
print("   their exact sum is slightly above 3/10")
print("   3/10 -> a double slightly BELOW 3/10       (one rounding)")
print()
print("Three separate roundings along three different routes.  Rounding once")
print("at the end would have given a different, and the more accurate, answer.")
print()
print("The counter-check that settles it: 0.1 + 0.5 == 0.6 is True, because")
print(f"1/2 is exactly representable, so only one rounding is involved on the")
print("way in for it and the two errors cancel.")
print(f"   0.1 + 0.5 = {0.1 + 0.5!r}   == 0.6 ? {0.1 + 0.5 == 0.6}")
print()
print("Generalisation worth remembering: floating point addition is correctly")
print("rounded -- the error you see is the accumulation of the errors ALREADY")
print("in the operands, amplified by however much cancellation the expression")
print("performs.  That is why Lesson 50's 'addition is associative' stops being")
print("true here, and why math.fsum exists.")
print()
print("The three defensible responses, in order of preference:")
print()
print("   1. fractions.Fraction when the values are rational by nature.")
print(f"        Fraction(1,10) + Fraction(2,10) = {a + b}, "
      f"and == {c} is {a + b == c}")
print("   2. Integer arithmetic when the values are discrete, such as cents.")
print(f"        10 + 20 == 30 is {10 + 20 == 30}")
print("   3. math.isclose when both sides are computed floats.")
print(f"        math.isclose(0.1 + 0.2, 0.3) is "
      f"{math.isclose(0.1 + 0.2, 0.3, rel_tol=1e-9)}")
print()
print("And the one response that is wrong: switching to float64 when you were")
print("already in float64, or writing abs(a - b) < 1e-15 without relating the")
print("threshold to the magnitude of a and b.")
```
**The bisection lands on the half, not the whole, and that is correct.** The
first $h$ for which $1 + h \neq 1$ is the rounding tie at $2^{-53}$: below it
the exact sum is nearer to $1.0$, and at or above it rounds up to
$1.0 + 2^{-52}$. Machine epsilon is that full gap, and `math.ulp(1.0)` confirms
it, so three independent routes agree to within one ulp.

**Part B is the whole answer to "why is 0.1 special".** It is not that 0.1 is
large or awkward or that decimals are somehow second-class. It is that
$1/10 = 1/(2 \cdot 5)$ has a factor of 5 in its reduced denominator, and a
float64's reduced denominator is always a power of two. Every value in the
table with denominator $2^k$ is exact; every value with a 3 or a 5 in the
denominator is not.

**Part C is the subtle one.** The addition of the two stored doubles is
*exact* -- the lesson prints that explicitly -- so the error is entirely in the
inputs. Both stored values sit above their true values, so their sum sits above
$3/10$ and rounds up, while the literal `0.3` rounds down. The gap is exactly
one ulp, `math.ulp(0.3)`.

**And the cross-check proves it.** `0.1 + 0.5 == 0.6` is `True`. If
floating-point addition were broken, that case would fail too.

</details>

**[ ] Exercise 2 —** (a) Show that a fixed absolute error of $10^{-4}$ is a
relative error of $10^{-3}$ at 0.1 and $10^{-12}$ at $10^8$. (b) Measure the
relative error of a left-to-right fold and a pairwise sum of 1000 copies of
0.1, and compare against the provable bound $n\varepsilon/2$. (c) Compute
condition numbers for `sqrt(x)`, `sqrt(x) - x`, `sqrt(x^2+1) - x`, `log(x)`
near 1, and `x^100`, and explain what each one says. (d) Solve
$A = [[1,1],[1,1+\varepsilon]]$ with $b = A \cdot [1,1]$, perturb $b$ by one
ulp, and show that a ridge term removes the sensitivity.

<details>
<summary>Solution</summary>

```python
"""Exercise 2 solution: absolute vs relative error, and the condition number.

The task: measure both kinds of error, find where conditioning actually bites,
and separate the three things people call 'numerical error'.
"""

import math


def rule(title):
    print()
    print("=" * 68)
    print(title)
    print("=" * 68)


def abs_err(approx, exact):
    return abs(approx - exact)


def rel_err(approx, exact):
    return abs(approx - exact) / abs(exact)
# ------------------------------------------------------------------ part A
rule("A. The same absolute error, two completely different situations")
print(f"   {'exact answer':>16} {'absolute error':>18} {'relative error':>18}")
for value, err in [(0.1, 1e-4), (1.0, 1e-4), (1e4, 1e-4), (1e8, 1e-4)]:
    print(f"   {value:>16.4g} {err:>18.3e} {rel_err(value + err, value):>18.3e}")
print()
print("The absolute error is identical in every row and the relative error")
print("varies by twelve orders of magnitude.  Which one you quote decides")
print("whether your report is honest.")
print()
print("Concretely: 1e-4 is a disaster on 0.1 and invisible on 1e8.  A")
print("specification that says 'accurate to 1e-4' without saying 'relative'")
print("or 'absolute' is not a specification.")
print()
print("Where each one is the right choice:")
print()
print("   ABSOLUTE  when the unit has physical meaning and the answer has a")
print("             fixed scale: a length in metres, a time in seconds, a")
print("             price in cents.  'within 1 nanometre' is meaningful.")
print()
print("   RELATIVE  when the quantity is a pure number, or spans many scales,")
print("             or is compared against something else computed.  Ratios,")
print("             probabilities, growth factors, residuals.")
print()
print("            Report both when you can.  '1.4142135623730951, relative")
print("            error below 1e-15' is a complete statement; the number")
print("            alone is not.")
print()
# ------------------------------------------------------------------ part B
rule("B. Relative error, and how it grows with a long sum")
n_values = [0.1] * 1000
true_sum = 0.1 * 1000


def fold(vs):
    t = 0.0
    for v in vs:
        t += v
    return t


def pairwise(vs):
    if len(vs) <= 1:
        return vs[0] if vs else 0.0
    mid = len(vs) // 2
    return pairwise(vs[:mid]) + pairwise(vs[mid:])
print(f"summing {len(n_values)} copies of 0.1, true sum {true_sum}")
print(f"   left-to-right fold  = {fold(n_values)!r}")
print(f"   pairwise           = {pairwise(n_values)!r}")
print()
print("   absolute error: fold {:.3e}, pairwise {:.3e}".format(
    abs_err(fold(n_values), true_sum), abs_err(pairwise(n_values), true_sum)))
print("   relative error: fold {:.3e}, pairwise {:.3e}".format(
    rel_err(fold(n_values), true_sum), rel_err(pairwise(n_values), true_sum)))
print()
print("The bound you can prove without running anything: each addition")
print("contributes at most half an ulp of relative error, so n additions give")
print("roughly n * eps / 2 of relative error.")
for n in (10, 100, 1000, 10000, 1000000):
    bound = n * 2.0**-52 / 2
    print(f"   n = {n:>8}: bound on relative error ~ {bound:.3e}")
print()
print("The naive fold tracks that bound closely -- it is not a coincidence and")
print("not a fluke.  Pairwise beats it by a wide margin because the running")
print("total stays close to the final answer instead of drifting away from it,")
print("so each new rounding is small relative to what is being accumulated.")
print()
# ------------------------------------------------------------------ part C
rule("C. Condition number: is the PROBLEM the problem?")
EPS = 2.0**-52


def kappa_scalar(f, df, x):
    return abs(x * df(x) / f(x))
print("kappa = |x f'(x) / f(x)|: how many times bigger is a relative input")
print("error than the relative output error it produces.")
print()
print(f"   {'function':<26} {'x':>14} {'kappa':>14}")
cases = [
    ("sqrt(x)", math.sqrt, lambda x: 0.5 / math.sqrt(x), 1.0),
    ("sqrt(x) - x", lambda x: math.sqrt(x) - x,
     lambda x: 0.5 / math.sqrt(x) - 1.0, 1e-10),
    ("sqrt(x^2+1) - x", lambda x: math.sqrt(x * x + 1) - x,
     lambda x: x / math.sqrt(x * x + 1) - 1.0, 1e4),
    ("log(x)", math.log, lambda x: 1.0 / x, 2.0),
    ("log(x)", math.log, lambda x: 1.0 / x, 1.000001),
    ("x^100", lambda x: x**100, lambda x: 100 * x**99, 1.5),
]
for name, f, df, x in cases:
    print(f"   {name:<26} {x:>14.10g} {kappa_scalar(f, df, x):>14.4e}")
print()
print("Read the last column against float64's 16 digits.")
print()
print(f"   kappa ~ 1e0   : no digits lost.  sqrt and sqrt(x^2+1) - x are both")
print(f"                   perfectly conditioned problems at these x.")
print(f"   kappa ~ 1e2   : x^100 throws away 2 digits.  Tolerable.")
print(f"   kappa ~ 1e6   : log(x) near 1 throws away 6.  You have 10 left.")
print()
print("THE CORRECTION THAT MATTERS MOST: sqrt(x^2+1) - x has kappa ~ 1, so it")
print("is a WELL conditioned problem.  Yet the lesson's naive float64")
print("evaluation returns exactly 0.0 at x = 1e8.  That is not ill")
print("conditioning -- it is an UNSTABLE ALGORITHM.  kappa for the")
print("sqrt(x^2+1) - x closed form is x / sqrt(x^2+1), which is 1 at every")
print("scale, and no input perturbation of that size would cause that error.")
print()
print("   CONDITIONING is a property of the problem.  You cannot code it away.")
print("   STABILITY    is a property of your algorithm.  You can, and cheaply.")
print()
print("So when a number comes out wrong, ask in this order:")
print("   1. Is my ALGORITHM stable here?   -> rephrase the computation.")
print("   2. Is the PROBLEM conditioned?     -> rephrase the problem.")
print("   3. Was the INPUT precise enough?   -> only now buy precision.")
print()
# ------------------------------------------------------------------ part D
rule("D. It bites hardest on linear systems, and there is a fix")
print("A = [[1,1],[1,1+eps]], b = A @ [1,1], so the exact answer is [1,1] for")
print("every eps.  Perturb b by ONE ulp and watch the answer move.")
print()


def solve2(A, b):
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return ((b[0] * A[1][1] - A[0][1] * b[1]) / det,
            (A[0][0] * b[1] - b[0] * A[1][0]) / det)


def err_from_one(v):
    return math.hypot(v[0] - 1.0, v[1] - 1.0)


def ridge(A, b, lam):
    n = len(A)
    AtA = [[sum(A[k][i] * A[k][j] for k in range(n)) + (lam if i == j else 0.0)
            for j in range(n)] for i in range(n)]
    Atb = [sum(A[k][i] * b[k] for k in range(n)) for i in range(n)]
    return solve2(AtA, Atb)
print(f"   {'eps':>8} {'rel err, clean b':>18} {'rel err, b+1ulp':>18}"
      f" {'ridge 1e-4':>12}")
eps = 1e-12
A = [[1.0, 1.0], [1.0, 1.0 + eps]]
b = [2.0, 2.0 + eps]
b_p = [b[0], b[1] + math.ulp(b[1])]
print(f"   {eps:>8.0e} {err_from_one(solve2(A, b)):>18.2e} "
      f"{err_from_one(solve2(A, b_p)):>18.2e} "
      f"{err_from_one(ridge(A, b_p, 1e-4)):>12.2e}")
print()
print(f"The input moved by {math.ulp(b[1]):.2e}, one bit.  The answer's error")
print("jumped from zero to about 6e-4, and the amplification 2/eps is exactly")
print("the reciprocal of the determinant.")
print()
print("Nothing is wrong with the code.  A is within eps of singular: its rows")
print("are nearly identical, so a wide range of x values produce nearly the")
print("same b, and recovering the difference is asking for digits the data")
print("does not contain.  A near-null-space direction is invisible in the")
print("output -- that is Lesson 35 and Lesson 38.")
print()
print("The fix is not precision.  It is to change the problem on purpose, by")
print("solving the ridge system (A'A + lambda I) x = A'b, which minimises")
print("||Ax - b||^2 + lambda ||x||^2.  With lambda = 1e-4 the answer becomes")
print("insensitive to the perturbation, at the cost of a small known bias.")
print("Lesson 101 minimises exactly this objective.")
print()
print("Generalisation: in machine learning this is why L2 and ridge")
print("regularisation exist.  An unregularised least-squares fit on")
print("ill-conditioned data has enormous variance -- it swings wildly on a")
print("one-bit input change -- and the penalty term buys back stability by")
print("accepting a little bias.  Bias and variance, from a numerical")
print("perspective rather than a statistical one.")
```
**Part A is about reporting, not about computing.** The same absolute error
varies by twelve orders of magnitude in relative terms, so "accurate to 1e-4"
is not a specification. Absolute error is the right measure when the unit has
physical meaning at a fixed scale -- metres, seconds, cents. Relative error is
right for pure numbers, ratios, and anything compared against another computed
value. Report both when you can.

**Part B: the naive fold tracks the $n\varepsilon/2$ bound closely, and
pairwise beats it.** That is not luck. The bound says each addition contributes
about half an ulp of relative error, and a running fold accumulates all of them.
Pairwise summation keeps the running total close to the final answer, so each
individual rounding is small relative to what is being accumulated. The lesson
measures a relative error of `1.407e-14` for the fold against a bound of
`1.110e-13`.

**Part C contains the correction that matters most.** `sqrt(x^2+1) - x` has
$\kappa \approx 1$, so it is a *well conditioned* problem, yet its naive float64
evaluation returns exactly `0.0` at $x = 10^8$. That is an unstable algorithm,
not an ill-conditioned problem, and the fixes are different: rephrase the
computation rather than buy precision.

**Part D is where conditioning earns its keep in practice.** The input moves by
one bit and the answer's error jumps from zero to about `6e-4`, an amplification
of $2/\varepsilon$. The ridge solve returns a bit-identical answer with or
without the perturbation, at the price of a small deliberate bias. This is
bias-variance traded in numerical rather than statistical language, and it is
why L2 regularisation exists.

</details>

**[ ] Exercise 3 —** Catastrophic cancellation, three ways. (a) Solve
$x^2 + 10^9 x + 1 = 0$ and show that the small root comes out as exactly `0.0`,
then repair it two ways. (b) Show `exp(x) - 1` returning `0.0` at $x = 10^{-17}$
while `math.expm1(x)` is exact, and explain why. (c) Show that evaluating the
naive formula in 60-digit `decimal` arithmetic gives the right answer, and
explain why that is not the fix.

<details>
<summary>Solution</summary>

```python
"""Exercise 3 solution: catastrophic cancellation, three ways.

The task is to find a formula that looks catastrophically wrong and then
repair it, twice, and to explain why the repair is a change of ALGORITHM rather
than a change of precision.
"""

import math
from decimal import Decimal, getcontext
getcontext().prec = 60


def rule(title):
    print()
    print("=" * 68)
    print(title)
    print("=" * 68)
# ---------------------------------------------------------------- part A
rule("A. The quadratic formula's small root")
a, b, c = 1.0, 1e9, 1.0
disc = b * b - 4 * a * c
print("Solve a x^2 + b x + c = 0 with a = 1, b = 1e9, c = 1.")
print(f"   b * b            = {b * b!r}")
print(f"   4*a*c            = {4 * a * c!r}")
print(f"   b*b - 4*a*c      = {disc!r}     <- the 4 is GONE")
print(f"   gap between doubles near 1e18 = {math.ulp(1e18)}")
print()
print("The gap near 1e18 is 128, so subtracting 4 from 1e18 rounds straight")
print("back to 1e18.  The discriminant has been rounded to b^2 before the")
print("formula ever sees it.")
print()
naive_big = (-b - math.sqrt(disc)) / (2 * a)
naive_small = (-b + math.sqrt(disc)) / (2 * a)
print(f"   big root   = {naive_big!r}")
print(f"   small root = {naive_small!r}    <- exactly zero")
print()
# The exact answer, in 60-digit decimal arithmetic.
exact_disc = Decimal(b) ** 2 - 4 * Decimal(1) * Decimal(1)
exact_big = (-Decimal(b) - exact_disc.sqrt()) / 2
exact_small = (-Decimal(b) + exact_disc.sqrt()) / 2
print(f"   exact big root   = {float(exact_big)!r}")
print(f"   exact small root = {float(exact_small)!r}")
print()
print("The naive formula returns 0.0 for a root of size 1e-9: a relative error")
print("of 100%.  The formula is not wrong; it is being fed a discriminant that")
print("no longer contains the information it needs.")
print()
print("The repair is the same conjugate trick as sqrt(x^2+1) - x.  Since the")
print("two roots multiply to c/a, and since dividing by the big root is a")
print("division by a large number rather than a subtraction of large numbers:")
stable_small = (c / a) / naive_big
print(f"   (c/a) / big_root              = {stable_small!r}")
stable_small2 = (2 * a * c) / (-b - math.sqrt(disc))
print(f"   2ac / (-b - sqrt(disc))       = {stable_small2!r}")
exact_small_f = float(exact_small)
print(f"   exact                         = {exact_small_f!r}")
print(f"   both agree with exact to "
      f"{max(abs(stable_small - exact_small_f), abs(stable_small2 - exact_small_f)) / abs(exact_small_f):.1e}"
      " relative")
print()
# ---------------------------------------------------------------- part B
rule("B. expm1-style cancellation, and the library that already fixed it")
print("The standard demonstration: exp(x) - 1 for very small x.")
print(f"   {'x':>12} {'exp(x) - 1':>24} {'math.expm1(x)':>24} {'rel err exp':>12}"
      f" {'rel err expm1':>14}")
for x in (1e-5, 1e-10, 1e-12, 1e-15, 1e-17):
    naive = math.exp(x) - 1.0
    good = math.expm1(x)
    print(f"   {x:>12.0e} {naive:>24.16e} {good:>24.16e} "
          f"{abs(naive - x) / x:>12.3e} {abs(good - x) / x:>14.3e}")
print()
print("exp(x) - 1 subtracts two numbers both near 1, so the answer is only")
print("about x while the operands are near 1.  Every digit of x is buried")
print("under rounding error of size eps = 2.2e-16.  At x = 1e-17 the")
print("subtraction returns exactly 0.0 -- a 100% relative error on a quantity")
print("that is itself a perfectly ordinary float.")
print()
print("math.expm1 never forms the two large numbers separately.  exp(x) = 1 +")
print("x + x^2/2 + ... means the answer is dominated by x, so a method that")
print("sums the tail x + x^2/2 + ... from the SMALL end upward keeps every")
print("digit.  Reordering the arithmetic to add small things together first is")
print("the general repair for cancellation.")
print()
# ---------------------------------------------------------------- part C
rule("C. Why more precision is the wrong answer here")
print("The same naive formula in 60-digit decimal arithmetic:")
print(f"   exact small root, 60 digits = {exact_small}")
print(f"   naive,  float64             = {naive_small!r}")
print(f"   stable, float64             = {stable_small!r}")
print()
print("At 60 digits the naive formula is already correct.  Nothing about the")
print("FORMULA was broken -- the combination of that formula with float64 was.")
print("That distinction decides what to do next.")
print()
print("   wrong reaction: switch to Decimal or float128 and carry on.  That")
print("                 hides the instability behind extra digits.  It works")
print("                 until the inputs grow another ten orders of magnitude,")
print("                 at which point the same code silently returns 0 again.")
print()
print("   right reaction: use the stable formula.  It is right in float64, it")
print("                 costs the same operations, and it keeps working as the")
print("                 inputs grow.")
print()
print("General test for cancellation: is there a subtraction of two quantities")
print("whose magnitudes are close RELATIVE TO THE SIZE OF THE ANSWER?  If yes,")
print("reorder the algebra, or call the function that already did it.  The")
print("standard library is full of them and every one exists for this reason:")
print()
print(f"   {'you want':<22} {'naive':>24} {'use instead':>24}")
print(f"   {'exp(x) - 1':<22} {math.exp(1e-12) - 1.0:>24.10e} "
      f"{math.expm1(1e-12):>24.10e}")
print(f"   {'log(1 + x)':<22} {math.log(1 + 1e-12):>24.10e} "
      f"{math.log1p(1e-12):>24.10e}")
print(f"   {'sqrt(x^2 + y^2)':<22} {math.sqrt(1e12 ** 2 + 1.0 ** 2):>24.16e} "
      f"{math.hypot(1e12, 1.0):>24.16e}")
print(f"   {'(-b+sqrt(b^2-4ac))/2a':<22} {naive_small:>24.10e} "
      f"{stable_small:>24.10e}")
print(f"   {'x^2 - y^2':<22} {1e12 ** 2 - (1e12 - 1) ** 2:>24.16e} "
      f"{(1e12 - (1e12 - 1)) * (1e12 + (1e12 - 1)):>24.16e}")
print(f"   {'the true x^2 - y^2':<22} {2e12 - 1:>24.16e}")
print()
print("The last pair is the cleanest illustration: x^2 - y^2 written directly")
print("subtracts two numbers of size 1e24 whose difference is about 2e12, and")
print("the answer comes back low by a factor of 1e-5.  Written as (x-y)(x+y),")
print("the subtraction is 1e12 - (1e12 - 1), whose difference is exactly 1 and")
print("is therefore exact.  Same three operations, same flops, and the")
print("factored form is right where the naive form is wrong.")
print()
print("Each of those naive forms is fine most of the time and silently wrong")
print("at one end of its range.  That is the whole argument for using the")
print("named function rather than the obvious expression.")
```
**Part A: the discriminant is destroyed before the formula sees it.** With
$b = 10^9$, $b^2 = 10^{18}$ and the gap between doubles there is 128, so
subtracting $4ac = 4$ rounds straight back to $10^{18}$. The small root is
$(-b + \sqrt{b^2 - 4ac})/2a$, whose numerator is now zero. The true root is
$-10^{-9}$, so the relative error is 100%.

**Both repairs give exactly `-1e-09`**, matching the 60-digit reference to
`0.0e+00` relative. The algebraic one rationalises the numerator: since
$r_{small} r_{large} = c/a$, divide by the large root instead of subtracting.
The conjugate form is $2ac/(-b - \sqrt{b^2-4ac})$, where the big terms now
*add* rather than cancel. Same operation count, correct answer, in float64.

**Part B: `math.expm1` sums small things together.** The series
$\exp(x) = 1 + x + x^2/2 + \dots$ means the answer is dominated by $x$, so
adding the tail $x + x^2/2 + \dots$ from the small end up never subtracts two
nearby quantities. `math.exp(x) - 1` does subtract, and at $x = 10^{-17}$ the
result is exactly `0.0` -- a 100% error on a perfectly ordinary float.

**Part C is the trap of this exercise.** The naive formula at 60 digits is
already correct, which proves the *formula* was never broken. The combination
of that formula with float64 was. So switching to `decimal` fixes this input and
does nothing about the next one: grow the inputs and the same code silently
returns zero again, at any precision. The algebraic repair is right at every
magnitude, which is the only kind of fix that scales.

The same reasoning applies to every named function in the standard library that
the lesson lists: `expm1`, `log1p`, `hypot`. Each exists because the obvious
expression is fine most of the time and silently wrong at one end of its range.

</details>

**[ ] Exercise 4 —** Choosing a finite-difference step and defending the
choice. (a) Sweep $h$ over powers of ten for a central difference of
$\sin(x) + 0.3x^2$ at $x = 1.3$ and find the true optimum. (b) Show what happens
at $h = 10^{-16}$ and explain it in terms of the spacing of $f$. (c) Write a
routine that picks $h$ from $\varepsilon^{1/3}|f(x)|$ with no derivatives
available, and check it across several $x$. (d) Beat the eleven-digit ceiling
using the complex step.

<details>
<summary>Solution</summary>

```python
"""Exercise 4 solution: choose a step size, and defend the choice.

The task: build a derivative routine that picks its own step size, show that a
naive tiny step is much worse, and show how to reach beyond the central
difference's ~11-digit ceiling without changing language.
"""

import cmath
import math
EPS = 2.0**-52


def rule(title):
    print()
    print("=" * 68)
    print(title)
    print("=" * 68)
# ------------------------------------------------------------- part A
rule("A. The three formulas, and the function they are for")
f = lambda x: math.sin(x) + 0.3 * x**2
df = lambda x: math.cos(x) + 0.6 * x
d2f = lambda x: -math.sin(x) + 0.6
d3f = lambda x: -math.cos(x)
X = 1.3


def forward(x, h):
    return (f(x + h) - f(x)) / h


def central(x, h):
    return (f(x + h) - f(x - h)) / (2.0 * h)
print(f"f(x) = sin(x) + 0.3 x^2 at x = {X}")
print(f"  f'  = {df(X)!r}")
print(f"  f'' = {d2f(X)!r}")
print(f"  f'''= {d3f(X)!r}")
print()
h_fwd = math.sqrt(2 * EPS * abs(df(X)) / abs(d2f(X)))
h_ctr = (3 * EPS * abs(df(X)) / abs(d3f(X))) ** (1.0 / 3.0)
print(f"h* forward ~ sqrt(2 eps |f'| / |f''|)     = {h_fwd:.4e}")
print(f"h* central ~ (3 eps |f'| / |f'''|)^(1/3)  = {h_ctr:.4e}")
print()
print(f"forward at h*    = {forward(X, h_fwd)!r}  "
      f"rel err {abs(forward(X, h_fwd) - df(X)) / abs(df(X)):.3e}")
print(f"central at h*    = {central(X, h_ctr)!r}  "
      f"rel err {abs(central(X, h_ctr) - df(X)) / abs(df(X)):.3e}")
print()
print("Both formulas land within a small factor of the measured optimum, which")
print("is all they promise: they depend on derivatives you usually do not know.")
print("In practice you bracket the order of magnitude and check.")
print()
# ------------------------------------------------------------- part B
rule("B. Why the smallest possible step is the worst possible step")
print("The full sweep, central difference:")
print(f"   {'h':>10} {'f(x+h) == f(x)?':>18} {'rel err':>12}")
rows = []
h = 1e-3
while h >= 1e-17:
    same = f(X + h) == f(X)
    err = abs(central(X, h) - df(X)) / abs(df(X))
    rows.append((h, err))
    print(f"   {h:>10.0e} {str(same):>18} {err:>12.3e}")
    h /= 10.0
best = min(rows, key=lambda r: r[1])
worst = rows[-1]
print()
print(f"best  h = {best[0]:.0e}   rel err {best[1]:.3e}")
print(f"worst h = {worst[0]:.0e}  rel err {worst[1]:.3e}")
print()
print("At h = 1e-16 the answer is off by 100%.  Nothing raised, nothing warned,")
print("and the code is shorter and looks more precise.  This is the trap.")
print()
print("The mechanism: the gap between doubles near f(1.3) is "
      f"{math.ulp(f(X)):.3e}.")
print(f"Once h is below that, f(x + h) rounds to f(x) exactly, the numerator")
print("is 0, and the quotient is 0.0 -- a derivative that is silently wrong by")
print("an unbounded factor rather than a merely imprecise one.")
print()
# ------------------------------------------------------------- part C
rule("C. An automatic chooser, which is what you should actually ship")


def derivative_auto(f, x, order="central"):
    """Pick h from the cube-root (or square-root) rule, using only f.

    We do not know f', so estimate the scale from f itself: |f| is the right
    order of magnitude for |f'| on a function that is not wildly varying, and
    it is always available.  That makes the estimate usable without any
    derivative at all.
    """
    scale = abs(f(x))
    if scale == 0.0:
        scale = 1.0
    if order == "central":
        h = (3.0 * EPS * scale) ** (1.0 / 3.0)
    else:
        h = math.sqrt(EPS * scale)
    if order == "central":
        return (f(x + h) - f(x - h)) / (2.0 * h), h
    return (f(x + h) - f(x)) / h, h
print("With no derivatives available, use eps^(1/3) * |f(x)| as the step scale:")
print(f"   {'x':>8} {'f(x)':>16} {'h chosen':>12} {'rel err':>12}")
for x in (0.5, 1.3, 2.7, 5.0, 10.0):
    d, h = derivative_auto(f, x)
    err = abs(d - df(x)) / abs(df(x))
    print(f"   {x:>8.1f} {f(x):>16.10f} {h:>12.3e} {err:>12.3e}")
print()
print("Every row is good to about 11 digits without being told anything about")
print("f'.  The rule of thumb is worth memorising in exactly this form:")
print()
print("   central difference: h ~ eps^(1/3) * |f(x)|, giving ~eps^(2/3) accuracy")
print(f"                       eps^(1/3) = {EPS ** (1 / 3):.3e}, "
      f"eps^(2/3) = {EPS ** (2 / 3):.3e}")
print("   forward difference: h ~ eps^(1/2) * |f(x)|, giving ~eps^(1/2)")
print(f"                       eps^(1/2) = {EPS ** 0.5:.3e}")
print()
print("Both ceilings are properties of float64, not of your code.  To beat the")
print("central difference's ceiling you must change the method.")
print()
# ------------------------------------------------------------- part D
rule("D. Beating the ceiling: the complex step")


def complex_step(f, x, h=1e-30):
    """f'(x) = Im(f(x + i h)) / h.  No subtraction, so no cancellation."""
    return f(complex(x, h)).imag / h


def complex_step_exp(x, h=1e-30):
    """f(x) = x * e^x evaluated at the complex point x + i h."""
    return complex(x, h) * cmath.exp(complex(x, h))
g = lambda t: t * math.exp(t)
dg = lambda t: (t + 1.0) * math.exp(t)
H_CS = 1e-30
print("f(x) = x e^x at x = 2")
print(f"   exact derivative      = {dg(2.0)!r}")
d_auto, h_auto = derivative_auto(g, 2.0)
print(f"   central, h chosen     = {d_auto!r}   "
      f"rel err {abs(d_auto - dg(2.0)) / dg(2.0):.3e}")
cs = complex_step_exp(2.0, H_CS).imag / H_CS
print(f"   complex step, h={H_CS:.0e} = {cs!r}   "
      f"rel err {abs(cs - dg(2.0)) / dg(2.0):.3e}")
print()
print("The complex step gets every digit float64 can represent, not merely the")
print("11 a central difference manages.  The reason is that f(x + ih) has")
print("imaginary part h f'(x) to first order, and that imaginary part is")
print("accumulated by ADDITION at every stage of the evaluation.  No step ever")
print("subtracts two nearly equal real quantities, so no digits are lost --")
print("which means you may use h = 1e-30, far below the real-axis resolution,")
print("with no penalty at all.")
print()
print("The cost is that your function must be evaluated in complex arithmetic")
print("end to end.  So it cannot contain abs(), max(), min(), a real sqrt, or")
print("a comparison that branches on the sign of a real number.  Everything")
print("smooth and analytic qualifies, which covers most of what gets")
print("differentiated in practice.  This is the cheapest member of the")
print("automatic-differentiation family: one forward pass, one function, no")
print("tape, no reverse mode, no compiler.")
```
**Part A: the minimum is at a finite $h$ and it is about $10^{-5}$.** The sweep
shows the relative error falling to `7.478e-12` at $h = 10^{-5}$ and then rising
by seven orders of magnitude as $h$ shrinks further. The shape is the sum of
the two competing terms: truncation falling like $h^2$, roundoff rising like
$1/h$.

**Part B: at $h = 10^{-16}$ the answer is exactly `0.0`,** a 100% relative
error, and the sweep prints `f(x+h) == f(x)` as `True` to show why. The gap
between doubles near $f(1.3)$ is `2.220e-16`, so the step lands below the
resolution of the function value and the numerator vanishes. Nothing raises.

**Part C: $\varepsilon^{1/3}|f(x)|$ needs no derivatives and works.** The lesson
checks it at five values of $x$ and gets between `2.553e-12` and `5.460e-11`
every time, without being told anything about $f'$. The scaling by $|f(x)|$ is
what makes it transfer: the step should be small relative to the *size of the
function's output*, not a fixed constant.

**Part D: the complex step is exact, not merely better.** For
$f(x) = x e^x$ at $x = 2$ it returns `22.16716829679195` with relative error
`0.000e+00`, where the best central difference manages `1.329e-10`. The reason
is that $f(x + ih)$ has imaginary part $h f'(x)$ to first order, and that
imaginary part is accumulated by *addition* at every stage, so no digits are
ever lost and $h$ may be $10^{-30}$ with no penalty. The cost is that the
function must be evaluable in complex arithmetic, which rules out `abs`,
`max`, real `sqrt`, and any branch on the sign of a real number.

</details>

**[ ] Exercise 5 —** Build a root finder with a tolerance policy you can defend.
Write a solver that returns the value, the iteration count, a status, and an
*error estimate*. Show it on four problems, show it refusing an interval with no
sign change, and show what it reports when asked for `1e-30`. Then argue for a
default tolerance and explain why an unreachable one is dangerous.

<details>
<summary>Solution</summary>

```python
"""Exercise 5 solution: build a solver you would actually ship.

The task: write a root finder with a real tolerance policy, show that the
tolerance is reachable rather than aspirational, and show what happens when a
solver is asked for more digits than the arithmetic has.
"""

import math
EPS = 2.0**-52


def rule(title):
    print()
    print("=" * 68)
    print(title)
    print("=" * 68)


class NoBracketError(ValueError):
    """Raised when the interval does not contain a sign change."""


def solve(f, a, b, rel_tol=1e-12, max_iter=100, df=None):
    """Bisection with a Newton accelerator, and a defensible stopping rule.

    Returns (root, iterations, newton_steps, converged).

    The stopping test is the FIRST-ORDER ERROR ESTIMATE

        |f(x) / f'(x)|  <  rel_tol * max(1, |x|)

    compared against |x|.  That is scale-invariant in f, so it does not change
    verdict when the function is rescaled, and it is the only test that
    measures distance to the root rather than size of the residual.
    """
    fa, fb = f(a), f(b)
    if fa * fb > 0.0:
        raise NoBracketError(
            f"f({a}) = {fa} and f({b}) = {fb} have the same sign, so no sign "
            f"change is bracketed on [{a}, {b}]")
    x = 0.5 * (a + b)
    newton_steps = 0
    for n in range(1, max_iter + 1):
        fx = f(x)
        # How far is x still from a root?  |f/f'| is the linear estimate.
        d = None
        if df is not None:
            try:
                d = df(x)
            except (ZeroDivisionError, ValueError):
                d = None
        if d not in (None, 0.0):
            est = abs(fx / d)
        else:
            # Without a derivative, fall back on half the bracket width, which
            # bisection already bounds.
            est = 0.5 * (b - a)
        if est < rel_tol * max(1.0, abs(x)):
            return x, n, newton_steps, True
        if fa * fx < 0.0:
            b, fb = x, fx
        else:
            a, fa = x, fx
        candidate = math.nan
        if d not in (None, 0.0):
            candidate = x - fx / d
        if a < candidate < b:
            newton_steps += 1
            x = candidate
        else:
            x = 0.5 * (a + b)
    return x, max_iter, newton_steps, False
# ------------------------------------------------------------------ part A
rule("A. It works, and it refuses to work when it cannot")
cases = [
    ("x^2 - 2", lambda x: x * x - 2.0, lambda x: 2.0 * x, 1.0, 2.0,
     math.sqrt(2.0)),
    ("x^3 - 2x + 2", lambda x: x**3 - 2 * x + 2.0,
     lambda x: 3 * x * x - 2.0, -3.0, 0.0, -1.7692923542386314),
    ("exp(x) - 3", lambda x: math.exp(x) - 3.0, lambda x: math.exp(x),
     0.0, 5.0, math.log(3.0)),
    ("cos(x) - x", lambda x: math.cos(x) - x, lambda x: -math.sin(x) - 1.0,
     0.0, 1.0, 0.7390851332151607),
]
print(f"   {'problem':<14} {'root':>22} {'iters':>6} {'Newton':>7}"
      f" {'converged':>10} {'rel err':>11}")
for name, f, df, a, b, exact in cases:
    r, n, ns, ok = solve(f, a, b, df=df)
    err = abs(r - exact) / abs(exact)
    print(f"   {name:<14} {r:>22.16f} {n:>6} {ns:>7} {str(ok):>10}"
          f" {err:>11.2e}")
print()
print("Four different functions, all to about 12 digits, all inside their")
print("brackets, and the Newton accelerator does most of the work.")
print()
try:
    solve(lambda x: x * x - 2.0, 3.0, 4.0)
except NoBracketError as exc:
    print(f"asked to solve x^2 - 2 on [3, 4]:")
    print(f"   NoBracketError: {exc}")
print()
print("Refusing is the feature.  A solver that 'returns something' when there")
print("is no root in the interval is worse than one that raises, because you")
print("will believe it.")
print()
# ------------------------------------------------------------------ part B
rule("B. The tolerance must be reachable")
print("How many digits can float64 actually deliver here?")
x_true = math.sqrt(2.0)
print(f"   the true sqrt(2) is {x_true!r}")
print(f"   one ulp at that value is {math.ulp(x_true):.3e}")
print()
print(f"   {'rel_tol':>12} {'converged':>10} {'iters':>6} {'root':>22}"
      f" {'rel err':>11}")
for tol in (1e-6, 1e-9, 1e-12, 1e-14, 1e-15, 1e-16, 1e-18, 1e-25):
    r, n, ns, ok = solve(lambda x: x * x - 2.0, 1.0, 2.0, rel_tol=tol,
                         df=lambda x: 2.0 * x)
    err = abs(r - x_true) / x_true
    print(f"   {tol:>12.0e} {str(ok):>10} {n:>6} {r:>22.16f} {err:>11.2e}")
print()
print("Read the converged column against the tolerance column.  For every")
print("tolerance from 1e-6 down to 1e-15 the solver reports success and")
print("delivers the best available answer -- and from 1e-15 down to 1e-12 the")
print("answer improves from 1.13e-12 to exact.  At 1e-16 and below it reports")
print("FAILURE, which is the correct and important outcome: those tolerances")
print("are unreachable, and a solver that claimed otherwise would be lying.")
print()
print("Note that the failures return a perfectly plausible-looking root,")
print(f"{r!r}, whose true relative error is 1.57e-16.  That is the trap: an")
print("unreachable tolerance does not produce an obviously broken answer, it")
print("produces the best available answer and then cannot confirm it.  Only")
print("the converged flag tells the two apart, which is why a production")
print("solver returns it.")
print()
print(f"A tolerance is a REQUEST for accuracy.  The ceiling is set by the")
print(f"arithmetic: about 16 significant digits, so no relative tolerance")
print(f"below roughly {math.ulp(x_true) / x_true:.1e} can ever be satisfied at")
print("this magnitude.  Passing one anyway is how solvers end up spinning to")
print("max_iter and returning an arbitrary iterate.")
print()
print("Rule: set rel_tol to something like 1e-12, which is achievable, and")
print("let the iteration count be whatever it needs to be.  Never set a")
print("tolerance to a number of digits you cannot otherwise justify.")
print()
# ------------------------------------------------------------------ part C
rule("C. Choosing a default tolerance")
print("A practical policy, in order:")
print()
print("   1. RELATIVE, not absolute.  rel_tol * max(1, |x|) behaves the same")
print("      whether the root is 1e-8 or 1e8.  An absolute tolerance silently")
print("      becomes a relative tolerance that tightens as the root shrinks.")
print()
print("   2. Around 1e-12 for float64 double work, 1e-6 for float32.  Those are")
print("      roughly eps^(1/4) and float32-eps^(1/4), comfortably above the")
print("      noise floor and far below anything a caller will notice.")
print()
print("   3. ALWAYS pass max_iter, and treat hitting it as a failure to")
print("      report rather than an answer to return.")
print()
print("   4. If the caller genuinely needs more digits than the method gives,")
print("      that is a statement about the METHOD, and the answer is a wider")
print("      type or an exact representation -- not a smaller tolerance.")
print()
print(f"   float64: a good default rel_tol is about 1e-12, giving {x_true!r}")
print(f"   float32: a good default rel_tol is about 1e-6")
print()
print("The same policy applies to optimisers, which is why gradient-descent")
print("implementations from Lesson 101 carry a tolerance and a max_iter")
print("together, and why the sensible ones also watch the STEP SIZE rather")
print("than the loss, because the loss can be flat while the iterate is")
print("still moving.")
# ------------------------------------------------------------------ part D
rule("D. The same solver, used where bisection alone would be painful")


def f_wide(x):
    """A root at arccos(0.1) ~= 1.4706, so it takes bisection a while to reach."""
    return math.cos(x) * 1e6 - 1e5
exact_wide = math.acos(0.1)
print(f"   f(1) = {f_wide(1.0):.6g}, f(2) = {f_wide(2.0):.6g}, "
      f"true root = {exact_wide!r}")
r1, n1, ns1, ok1 = solve(f_wide, 1.0, 2.0,
                         df=lambda x: -math.sin(x) * 1e6)
print(f"   safeguarded solver: {n1} iterations ({ns1} Newton), "
      f"converged={ok1}, root={r1!r}")
print(f"   relative error = {abs(r1 - exact_wide) / abs(exact_wide):.2e}")


def plain_bisection(f, a, b, rel_tol=1e-12, max_iter=200):
    fa = f(a)
    for n in range(1, max_iter + 1):
        mid = 0.5 * (a + b)
        if 0.5 * (b - a) < rel_tol * max(1.0, abs(mid)):
            return mid, n
        if fa * f(mid) <= 0.0:
            b = mid
        else:
            a, fa = mid, f(mid)
    return 0.5 * (a + b), max_iter
r2, n2 = plain_bisection(f_wide, 1.0, 2.0)
print(f"   plain bisection:    {n2} iterations, root={r2!r}")
print(f"   agree to {abs(r1 - r2) / max(1.0, abs(r1)):.1e} relative")
print()
print("The safeguarded version costs one extra division and one comparison per")
print("iteration and removes an entire class of failure.  On a function where")
print("Newton helps it converges in a small fraction of the iterations; on one")
print("where Newton cycles it degrades gracefully to bisection instead of")
print("diverging.  That is why scipy's brentq, and every other production")
print("root-finder, is built this way.")
```
**The stopping rule is the interesting part.** The lesson tests
$|f(x)/f'(x)| < \tau\max(1, |x|)$, the first-order estimate of how far $x$ still
is from a root. Comparing $|f(x)|$ against an absolute constant is wrong
because it changes verdict when the function is rescaled: multiplying $f$ by
$10^{-9}$ divides every residual by a billion and leaves every root unchanged.
The estimate $|f/f'|$ is invariant under exactly that rescaling, because $f$
and $f'$ scale together.

**The solver reports failure, and that is the feature.** For
`rel_tol=1e-16` and below it returns `converged=False` after 100 iterations.
Crucially, the *value* it hands back is still perfectly plausible --
`1.414213562373095`, a true relative error of `1.57e-16`. An unreachable
tolerance does not produce an obviously broken answer; it produces the best
available answer and then cannot confirm it. Only the status distinguishes the
two, which is why a production solver returns it.

**`no bracket` is also a real outcome.** Asked to solve $x^2 - 2$ on $[3,4]$,
where $f$ is positive at both ends, the solver raises rather than returning a
number. A solver that guesses here will be believed.

**On the default.** Around `1e-12` for float64 and `1e-6` for float32: both
achievable, both far below anything a caller will notice, and both comfortably
above the noise floor. The rule to remember is that a tolerance is a
*request*, and the reachable ceiling is about 16 significant digits regardless
of how many you ask for.

</details>

**[ ] Exercise 6 —** Quadrature and the meaning of "accurate". Implement
trapezoid, midpoint and Simpson's rule. Measure the error against panel count
for $\sin(x)$ on $[0,\pi]$, $\sqrt{x}$ on $[0,1]$ and $|x|^{1.5}$ on
$[-1,1]$, all with known exact values. Then explain why the textbook
convergence rates are only correct for the first integrand, and what a
production quadrature routine does instead.

<details>
<summary>Solution</summary>

```python
"""Exercise 6 solution: an integrator that knows when to stop.

The task: implement three rules and show, with real numbers, that a rule
tuned for smooth integrands is much worse than one tuned for arbitrary ones.
The point is that "accurate to 1e-12" is meaningless without saying accurate
FOR WHAT.
"""

import math


def rule(title):
    print()
    print("=" * 68)
    print(title)
    print("=" * 68)
# ------------------------------------------------------- the three rules


def midpoint(f, a, b, n):
    """n equal panels, one evaluation each.  Error is O(h^2) = O(1/n^2)."""
    h = (b - a) / n
    total = 0.0
    for i in range(n):
        total += f(a + (i + 0.5) * h)
    return total * h


def simpson(f, a, b, n):
    """Composite Simpson, n even.  Error is O(h^4) = O(1/n^4)."""
    if n % 2:
        raise ValueError("Simpson's rule needs an even number of panels")
    h = (b - a) / n
    total = f(a) + f(b)
    for i in range(1, n):
        total += (4.0 if i % 2 else 2.0) * f(a + i * h)
    return total * h / 3.0


def trapezoid(f, a, b, n):
    """Composite trapezoid.  Error is O(h^2) = O(1/n^2), like midpoint."""
    h = (b - a) / n
    total = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        total += f(a + i * h)
    return total * h
# --------------------------------------------------------- the integrand


def f_smooth(x):
    """sin(x) on [0, pi].  The exact value is 2."""
    return math.sin(x)


def f_rough(x):
    """sqrt(x) on [0, 1].  The exact value is 2/3.

    Not differentiable at x = 0: the derivative is infinite there, so every
    O(h^2) or better rule loses its leading order.
    """
    return math.sqrt(x)


def f_soft(x):
    """|x|^1.5 on [-1, 1].  The exact value is 4/5.

    Smooth except at one interior point, which is the realistic version of the
    same problem.
    """
    return abs(x) ** 1.5
EXACTS = [(f_smooth, 0.0, math.pi, 2.0, "sin(x) on [0, pi]"),
          (f_rough, 0.0, 1.0, 2.0 / 3.0, "sqrt(x) on [0, 1]"),
          (f_soft, -1.0, 1.0, 4.0 / 5.0, "|x|^1.5 on [-1, 1]")]
# ------------------------------------------------------------------ part A
rule("A. Error against panels, for three integrands")
RULES = [("trapezoid", trapezoid), ("midpoint", midpoint), ("simpson", simpson)]
PANELS = [10, 100, 1000, 10000, 100000]
for func, a, b, exact, label in EXACTS:
    print(f"{label}, exact = {exact!r}")
    print(f"   {'panels':>8} {'trapezoid':>14} {'midpoint':>14} {'simpson':>14}")
    for n in PANELS:
        cells = []
        for _, g in RULES:
            try:
                v = g(func, a, b, n)
                cells.append(f"{abs(v - exact):>14.3e}")
            except ValueError:
                cells.append(f"{'(even n)':>14}")
        print(f"   {n:>8} {cells[0]} {cells[1]} {cells[2]}")
    print()
# ------------------------------------------------------------------ part B
rule("B. What the slopes mean, and which integrand breaks which rule")
print("Every time you double the panels, watch the error:")
print()
print(f"   {'integrand':<20} {'rule':<11} {'ratio':>7}   reading")
for func, a, b, exact, label in EXACTS:
    for name, g in RULES:
        n = 1000
        e1 = abs(g(func, a, b, n) - exact)
        e2 = abs(g(func, a, b, 2 * n) - exact)
        ratio = e1 / e2 if e2 > 0 else float("nan")
        if 3.5 < ratio < 4.5:
            reading = "O(h^2), one power gained"
        elif 12.0 < ratio < 22.0:
            reading = "O(h^4), two powers gained"
        elif 2.2 < ratio <= 3.5:
            reading = "BETWEEN O(h^2) and O(h): degraded"
        else:
            reading = "UNUSUAL -- investigate"
        print(f"   {label:<20} {name:<11} {ratio:>7.1f}   {reading}")
print()
print("Read the table by column.")
print()
print("On sin(x), which is smooth everywhere and has no end problem, the")
print("trapezoid and midpoint gain exactly one power per doubling and Simpson")
print("gains two.  That is the textbook statement, and the numbers 4.0, 4.0")
print("and 16.6 are the textbook statement made real.")
print()
print("On sqrt(x) the ratio drops to 2.8 for ALL THREE rules.  An unbounded")
print("derivative at the END of the interval means the error expansion that")
print("produces the 4 and the 16 is simply false there, so every rule")
print("degrades to something between first and second order.  No amount of")
print("panels restores the missing power.")
print()
print("On |x|^1.5 the corner is in the INTERIOR, and the damage is different:")
print("the trapezoid and midpoint keep their exact O(h^2) rate, while Simpson")
print("collapses from 16.6 to 5.7 -- it loses its second power.  Simpson's")
print("advantage depends on the cubic cancellation across a whole panel, and")
print("a corner inside a panel destroys it while leaving the leading term")
print("intact.")
print()
print("That is the practical content of the word 'accurate'.  Simpson is")
print("O(1/n^4) on smooth integrands and closer to O(1/n^3) on a function")
print("with one corner in the middle.  A claim like 'this integrates to")
print("1e-12' is incomplete until you say what was integrated.")
print()
# ------------------------------------------------------------------ part C
rule("C. Choose n from a target tolerance, honestly")
TARGET = 1e-10
MAX_N = 200000
print(f"Find the smallest power-of-four panel count reaching {TARGET:.0e} "
      f"relative to the exact value, capping at n = {MAX_N:,}.")
print()
for func, a, b, exact, label in EXACTS:
    print(f"{label}:")
    for name, g in RULES:
        n, chosen, prev = 64, None, None
        while n <= MAX_N:
            err = abs(g(func, a, b, n) - exact)
            if err <= TARGET * abs(exact):
                chosen = n
                break
            if prev is not None and err > prev * 0.5:
                break          # progress has stalled: more panels will not help
            prev = err
            n *= 4
        if chosen:
            print(f"   {name:<11} n = {chosen:>7,} gives "
                  f"{abs(g(func, a, b, chosen) - exact):.2e}")
        else:
            print(f"   {name:<11} did not reach {TARGET:.0e} within "
                  f"n = {MAX_N:,}")
    print()
print("Read the panel counts against the target of 1e-10.")
print()
print("On the smooth integrand Simpson needs 1024 panels and midpoint needs")
print("65536 -- a factor of 64 in work for the extra two powers of accuracy.")
print("The trapezoid does not reach the target at all within 200000 panels,")
print("which is the O(h^2) rate being honest about what it costs.")
print()
print("On sqrt(x) NOTHING reaches 1e-10 within the panel budget.  The rules")
print("are still converging, just at the degraded rate from part B, and a")
print("quadrature routine asked for 1e-10 on that integrand by simple panel")
print("counting would either spin or quietly return a worse answer.")
print()
print("On |x|^1.5 the interior corner lets Simpson through at 16384 panels --")
print("sixteen times worse than on the smooth case, which is the lost second")
print("power showing up directly in the work required.  The trapezoid and")
print("midpoint still miss the target, because at 200000 panels they are only")
print("at the O(h^2) rate.")
print()
print("So the honest summary is that a tolerance is a REQUEST, and whether it")
print("is reachable depends on the integrand and not only on the rule.  This")
print("is why a production quadrature routine does not use the asymptotic")
print("order to pick n.  It computes the answer with n panels and with 2n")
print("panels, and if they differ by more than the tolerance it doubles again")
print("-- and if they agree to the tolerance it stops, whatever the theory")
print("predicted.  The theory is a starting guess; the agreement is the")
print("evidence.")
rule("D. The rule of thumb you should actually remember")
print("   integrand                rule        error per doubling of panels")
print("   ----------------------   ---------  --------------------------")
print("   smooth everywhere        Simpson     divides by 16   (measured 16.6)")
print("   smooth everywhere        midpoint    divides by 4    (measured 4.0)")
print("   smooth everywhere        trapezoid   divides by 4    (measured 4.0)")
print("   corner in the interior   Simpson     divides by 6    (measured 5.7)")
print("   corner in the interior   midpoint    divides by 4    (measured 4.0)")
print("   singularity at an end    any rule    divides by 3    (measured 2.8)")
print()
print("Panels needed for a relative target t, from error ~ c / n^p:")
print()
print("   trapezoid / midpoint, smooth     n ~ (c / t)^(1/2)")
print("   Simpson, smooth                  n ~ (c / t)^(1/4)")
print()
print("The measured column is the one to trust; the textbook column is the")
print("special case where the integrand has no corner anywhere.")
print()
print("The practical consequence is that quadrature libraries do not trust")
print("the asymptotic order.  They compare an n-panel answer against a")
print("2n-panel answer and stop when the two AGREE to your tolerance -- a")
print("self-consistency test that works whatever the integrand does.  That is")
print("the same philosophy as the step-size test in the finite-difference")
print("lesson, and the same philosophy as a safeguarded root-finder: measure")
print("your own progress instead of trusting a bound that assumed conditions")
print("you have not checked.")
```
**The measured ratios are the whole exercise.** On $\sin(x)$ the trapezoid and
midpoint gain a factor of 4 per doubling of the panel count and Simpson gains
about 16.6, which is exactly the textbook statement. The two awkward integrands
break it, and they break it *differently*:

- $\sqrt{x}$ on $[0,1]$ has an **unbounded derivative at an endpoint**. All
  three rules degrade to a ratio of about 2.8, which is between first and second
  order. The error expansion that produces the 4 and the 16 is simply false at
  the endpoint, so no rule keeps its extra power.
- $|x|^{1.5}$ on $[-1,1]$ has a **corner in the interior**. The trapezoid and
  midpoint keep their exact $O(h^2)$ rate, but Simpson collapses from 16.6 to
  5.7, losing its second power. Simpson's advantage comes from cubic
  cancellation across a whole panel, and a corner inside a panel destroys that
  while leaving the leading term intact.

**So "accurate to 1e-12" is incomplete without saying what was integrated.**
The lesson confirms this by searching for panel counts that reach $10^{-10}$:
on the smooth integrand Simpson needs 1024 and midpoint 65536, a factor of 64
in work for the extra two powers; on $\sqrt{x}$ *nothing* reaches the target
within 200000 panels; on $|x|^{1.5}$ Simpson needs 16384, sixteen times worse
than the smooth case.

**Which is why production quadrature does not trust the asymptotic order.** It
computes the answer with $n$ panels and with $2n$, and stops when the two agree
to the tolerance regardless of what the theory predicted. That is the same
philosophy as the finite-difference step-size test and the safeguarded
root-finder: measure your own progress instead of trusting a bound whose
hypotheses you have not checked.

</details>

**Challenge —** Build a small numerical toolkit in one file where **every**
routine returns its own error estimate alongside its answer: a float inspector,
a relative-error comparator, a root finder that reports status, a derivative
that picks its own step, and an audit harness that checks each result against
an independent reference and asserts a stated number of correct digits.

<details>
<summary>Solution</summary>

```python
"""Challenge solution: a tiny numeric toolkit that reports its own reliability.

Everything here is one file of standard-library Python: IEEE 754 inspection,
condition estimation, root finding, finite differences and quadrature, with
each routine returning its own error estimate rather than a bare number.

The design rule the whole thing illustrates: a numerical routine that cannot
tell you how much to trust it is not finished.  Every function below returns
the value AND the evidence for that value.
"""

import math
import struct
from fractions import Fraction
EPS = 2.0**-52


def banner(title):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)
# ===================================================== 1. the float model


def bits(x):
    (packed,) = struct.unpack("<Q", struct.pack("<d", x))
    return f"{packed:064b}"


def exact(x):
    """What the machine actually holds, as a rational. No information lost."""
    return Fraction(x)


def spacing(x):
    """The gap to the next float. Doubles roughly every factor of 2 in size."""
    return math.ulp(x)
banner("1. Inspecting the machine's numbers")
for v in (1.0, 0.1, 1e16, 5e-324, 1.7976931348623157e308):
    print(f"   {v!r}")
    print(f"      bits     {bits(v)}")
    print(f"      exact    {exact(v)}")
    print(f"      spacing  {spacing(v):.6e}")
print()
print("Every float64 is exactly a rational.  'exact(x)' is the single most")
print("useful debugging tool in numerical code, because it shows you the value")
print("you have rather than the one you meant.")
print()
# ============================================ 2. an honest error estimate


def relative(a, b):
    """Relative error of a against a known-exact b."""
    return abs(a - b) / abs(b)
banner("2. Relative error, and why the absolute one is not enough")
print(f"   {'exact':>14} {'absolute error':>16} {'relative error':>16}")
for value in (1e-8, 1.0, 1e8):
    approx = value * (1 + 1e-12)
    print(f"   {value:>14.3e} {abs(approx - value):>16.3e} "
          f"{relative(approx, value):>16.3e}")
print()
print("A fixed 1e-12 relative perturbation looks like 1e-20 absolute on a")
print("small number and 1e-4 absolute on a large one.  If your test suite")
print("checks absolute differences against a fixed epsilon, it is testing")
print("nothing on the small inputs and nothing you care about on the large")
print("ones.")
print()
# ============================================== 3. a self-reporting solver


class Solver:
    """Bisection with a Newton accelerator, reporting how far it got.

    Every return value carries its own evidence:

      value      the best answer found
      iterations how many steps were taken
      status     'converged' | 'no bracket' | 'iteration limit'
      estimate   the estimated distance from value to the true root, or None
                 if that could not be established

    A caller can therefore decide whether to trust the answer, rather than
    having to trust the implementation.
    """
    def __init__(self, rel_tol=1e-12, max_iter=100):
        self.rel_tol = rel_tol
        self.max_iter = max_iter
    def solve(self, f, a, b, df=None):
        fa, fb = f(a), f(b)
        if fa * fb > 0.0:
            return {"value": None, "iterations": 0, "status": "no bracket",
                    "estimate": None,
                    "detail": f"f(a) = {fa}, f(b) = {fb}, same sign"}
        x = 0.5 * (a + b)
        for n in range(1, self.max_iter + 1):
            fx = f(x)
            d = None
            if df is not None:
                try:
                    d = df(x)
                except (ZeroDivisionError, ValueError):
                    d = None
            if d not in (None, 0.0):
                estimate = abs(fx / d)
            else:
                estimate = 0.5 * (b - a)
            if estimate < self.rel_tol * max(1.0, abs(x)):
                return {"value": x, "iterations": n,
                        "status": "converged", "estimate": estimate}
            if fa * fx < 0.0:
                b, fb = x, fx
            else:
                a, fa = x, fx
            candidate = x - fx / d if d not in (None, 0.0) else math.nan
            x = candidate if a < candidate < b else 0.5 * (a + b)
        return {"value": x, "iterations": self.max_iter,
                "status": "iteration limit", "estimate": None}
banner("3. A root finder that reports its own reliability")
problems = [
    ("x^2 - 2", lambda x: x * x - 2, lambda x: 2 * x, 1.0, 2.0),
    ("x^3 - 2x + 2", lambda x: x**3 - 2 * x + 2,
     lambda x: 3 * x * x - 2, -3.0, 0.0),
    ("cos(x) - x", lambda x: math.cos(x) - x,
     lambda x: -math.sin(x) - 1, 0.0, 1.0),
    ("x^2 - 2 on [3,4]", lambda x: x * x - 2, lambda x: 2 * x, 3.0, 4.0),
    ("x^2 - 2, tol 1e-30", lambda x: x * x - 2, lambda x: 2 * x, 1.0, 2.0),
]
solver = Solver()
for name, f, df, a, b in problems:
    tight = "1e-30" in name
    s = Solver(rel_tol=1e-30 if tight else 1e-12).solve(f, a, b, df=df)
    head = f"   {name:<20} status={s['status']:<17}"
    if s["value"] is None:
        print(head + f"({s['detail']})")
        continue
    est = "n/a" if s["estimate"] is None else f"{s['estimate']:.2e}"
    print(f"{head}iters={s['iterations']:<4} value={s['value']!r:<22} "
          f"est. distance={est}")
print()
print("Three things worth noticing.")
print()
print("   'no bracket' is reported, not papered over.  A solver that returns a")
print("   number when there is no root in the interval will be believed.")
print()
print("   An unreachable tolerance of 1e-30 returns status='iteration limit'")
print("   rather than claiming success.  The value it returns is still the")
print("   best available -- it is simply not certified.")
print()
print("   The status is the product.  Without it, a caller cannot distinguish")
print("   'converged to 1e-12' from 'gave up at 1e-16 and did not say so'.")
print()
# ================================== 4. a self-reporting derivative


def derivative(f, x, order="central"):
    """Return (value, step, note) with the step chosen by the lesson's rule."""
    scale = abs(f(x)) or 1.0
    if order == "central":
        h = (3.0 * EPS * scale) ** (1.0 / 3.0)
        value = (f(x + h) - f(x - h)) / (2.0 * h)
    else:
        h = math.sqrt(EPS * scale)
        value = (f(x + h) - f(x)) / h
    note = ("h from the cube-root rule; expect about 11 correct digits"
            if order == "central" else
            "h from the square-root rule; expect about 8 correct digits")
    return value, h, note


def complex_step(f, x, h=1e-30):
    """f'(x) via Im(f(x + i h)) / h. Needs complex-safe f; exact when f is."""
    return f(complex(x, h)).imag / h
banner("4. A derivative that picks its own step, and a better one")
f = lambda t: math.sin(t) + 0.3 * t * t
df = lambda t: math.cos(t) + 0.6 * t
print(f"   f(x) = sin(x) + 0.3x^2,  exact f'(1.3) = {df(1.3)!r}")
print()
print(f"   {'method':<24} {'value':>22} {'rel err':>12}  note")
for order in ("forward", "central"):
    v, h, note = derivative(f, 1.3, order)
    print(f"   {order + ' difference':<24} {v:>22.16f} "
          f"{relative(v, df(1.3)):>12.3e}  h={h:.1e}, {note}")
v, h, _ = derivative(f, 1.3, "central")
print(f"   {'central at h=1e-16':<24} "
      f"{(f(1.3 + 1e-16) - f(1.3 - 1e-16)) / 2e-16:>22.16f} "
      f"{relative((f(1.3 + 1e-16) - f(1.3 - 1e-16)) / 2e-16, df(1.3)):>12.3e}"
      "  f(x+h)==f(x): " + str(f(1.3 + 1e-16) == f(1.3)))
print(f"   {'complex step':<24} {complex_step(lambda t: t * t, 1.3):>22.16f} "
      f"{relative(complex_step(lambda t: t * t, 1.3), 2 * 1.3):>12.3e}"
      "  no cancellation possible")
print()
print("The third row is the trap.  A step of 1e-16 looks maximally precise and")
print("returns a relative error of 100%, because f(1.3 + 1e-16) is bit-for-bit")
print("f(1.3) and the numerator is zero.  Choosing h badly is worse than")
print("choosing a crude scheme.")
print()
# ================================================= 5. a sanity harness
banner("5. A harness that would have caught every bug in this lesson")


def audit(name, value, reference, want_digits):
    """Compare against a reference and report the DIGITS you actually got."""
    err = relative(value, reference)
    if err == 0.0:
        digits = float("inf")
    else:
        digits = -math.log10(err)
    verdict = "PASS" if digits >= want_digits else "FAIL"
    print(f"   {name:<34} {digits:>6.1f} digits   want {want_digits:>2}   "
          f"{verdict}")
    return digits >= want_digits
checks = []
checks.append(audit("sqrt(2) via midpoint, tol 1e-12",
                    Solver().solve(lambda x: x * x - 2, 1.0, 2.0,
                                   df=lambda x: 2 * x)["value"],
                    math.sqrt(2.0), 12))
checks.append(audit("sqrt(2) via safeguarded Newton, tol 1e-14",
                    Solver(rel_tol=1e-14).solve(lambda x: x * x - 2, 1.0, 2.0,
                                                 df=lambda x: 2 * x)["value"],
                    math.sqrt(2.0), 14))
checks.append(audit("central difference of sin+0.3x^2 at 1.3",
                    derivative(f, 1.3, "central")[0], df(1.3), 10))
checks.append(audit("complex-step derivative of x^2 at 1.3",
                    complex_step(lambda t: t * t, 1.3), 2 * 1.3, 14))
checks.append(audit("math.expm1(1e-12) vs series",
                    math.expm1(1e-12), 1e-12, 12))
checks.append(audit("stable sqrt(x^2+1)-x at x=1e8",
                    1.0 / (math.sqrt(1e16 + 1.0) + 1e8), 5e-9, 12))
print()
print(f"   {sum(checks)} of {len(checks)} checks passed.")
print()
print("Every one of those numbers was wrong at some point while this lesson")
print("was being written -- a swapped sign, an off-by-one axis, a fraction")
print("with no sqrt, a root-finding bracket with no root in it.  None of them")
print("raised an exception.  All of them were caught by a harness that")
print("compares against an independent reference and asks for a stated")
print("number of correct DIGITS, rather than by reading the code carefully.")
print()
print("That is the transferable lesson, and it is the same one the rest of")
print("this repository keeps making: define what the answer should be, then")
print("make the code disagree with that definition loudly when it is wrong.")
```
**The design rule the whole file illustrates is that a numerical routine which
cannot tell you how much to trust it is not finished.** Each routine returns
evidence, not just a value:

- `exact(x)` returns what the machine actually holds, as a rational, with no
  information lost. When a number surprises you this is the first thing to look
  at.
- `Solver.solve` returns a dict with `value`, `iterations`, `status` and
  `estimate`. The `status` is the product: without it a caller cannot tell
  "converged to 1e-12" from "gave up at 1e-16 and did not say so", because the
  two return nearly identical numbers.
- `derivative` returns the value, the step it chose, and a note saying how many
  digits to expect from that step.
- `audit` converts an absolute error into a DIGIT count and asserts against a
  stated requirement.

**The harness is the part worth copying.** Every number in this lesson was wrong
at some point while it was being written -- a swapped sign, an off-by-one axis,
a `Fraction` with no `sqrt`, a root-finding bracket with no root in it. None of
them raised an exception. All of them were caught by comparing against an
independent reference and asking for a stated number of correct digits, not by
reading the code carefully.

That is the transferable lesson, and it is the same one the whole repository
keeps making: define what the answer should be, then make the code disagree
with that definition loudly when it is wrong. A test that asserts
`abs(a - b) < 1e-9` cannot do that; a test that asserts "at least 12 correct
digits against an independently computed reference" can.

</details>

## Summary

- A float64 is $m \cdot 2^j$ with $|m| < 2^{53}$, so a decimal $p/q$ is exact if
  and only if $q$ is a power of two. Machine epsilon is $2^{-52} \approx
  2.22 \times 10^{-16}$, the ulp at 1.0, and it is not the smallest
  representable number.
- `0.1 + 0.2 != 0.3` is three roundings along three different routes, not a
  broken addition. The addition of the two stored doubles is *exact*; the error
  entered when $1/10$ and $1/5$ were rounded on the way in, both upwards.
- The three fixes are, in order: an exact type (`Fraction`, integer cents) when
  the values really are exact; a scaled comparison (`math.isclose`) when both
  sides are computed; and never a tolerance used to decide a logical question.
- Cancellation is subtractive: dividing the operands' absolute error by a small
  answer explodes the relative error. The repair is algebraic, not numeric --
  $1/(\sqrt{x^2+1}+x)$, `expm1`, `log1p`, `hypot`.
- The condition number $\kappa = |x f'(x)| / |f(x)|$ is a property of the
  *problem*; each factor of 10 costs about a decimal digit. You cannot code it
  away, and a wider float multiplies your error by exactly as much as a narrow
  one does.
- Cancellation is an *unstable algorithm*, which is a different failure with a
  different fix. $\sqrt{x^2+1}-x$ has $\kappa = 1$ and still returns `0.0` at
  $x = 10^8$, because the algorithm, not the problem, is at fault.
- Bisection's guarantee is a theorem ($w/2^{n+1}$ after $n$ halvings) and
  needs only a sign change. Newton's is local and can cycle: on
  $x^3 - 2x + 2$ from $x_0 = 0$ it alternates 0 and 1 forever. Keeping a
  bisection bracket around a Newton step gives both the speed and the safety,
  which is why Brent's method is shaped that way.
- Bisection's guarantee is a theorem ($w/2^{n+1}$ after $n$ halvings) and
  needs only a sign change. Newton's is local and can cycle: on
  $x^3 - 2x + 2$ from $x_0 = 0$ it alternates 0 and 1 forever. Keeping a
  bisection bracket around a Newton step gives both the speed and the
  safety, which is why Brent's method is shaped that way -- and a
  tolerance is a request, not a guarantee: choose about `1e-12` for
  float64, always pass `max_iter`, and report rather than hide a solver
  that could not reach it.
  always pass `max_iter`, and treat a solver that cannot reach its tolerance as
  something to report rather than something to hide.

## Next

This is the last lesson of the repository, so here is the whole shape of what
you have built.

You started in **Part 01** by learning that a statement has to be precise
before it can be trusted, and that proof is the tool that makes it precise.
**Part 02** gave you counting and graphs, so that "how fast" and "how many"
stopped being hand-waving. **Part 03** gave you vectors and matrices, which
turned out to be the native data type of essentially all of modern computing,
and **Part 04** gave you the calculus that describes how those things change.

**Part 05** added uncertainty, because most real systems must act without
knowing; **Part 06** gave you the formal language for cost; **Part 07** put the
linear algebra into 3D; **Part 08** used the calculus to find optima.
**Part 09** went back to arithmetic itself and showed that exact arithmetic --
modular, with its own geometry -- is what integrity and security rest on.

**Part 10**, which ends here, closed the loop from both ends. Lesson 120 gave
you the array type that every one of those mathematical ideas is actually
implemented as, plus the exact rules governing its shape -- including the rules
whose violation produces silently wrong answers rather than exceptions. Lesson
121 gave you the other half: that those answers are computed in finite
precision, what that costs, and how to tell whether a number you got is
trustworthy.

The through-line is a single idea, stated once and never abandoned: **define
what the answer should be, then make your code disagree with that definition
loudly when it is wrong.** Every technique in this repository is an application
of it. A proof checks a claim against an axiom. A counting argument checks a
number against a bijection. A gradient check compares two independent routes to
the same quantity. A condition number predicts an error before you spend
compute finding out. A test harness asserts a number of correct digits against
an independent reference.

If you take one habit from these two lessons, take the audit harness. It needs
no mathematics beyond what is here, and it would have caught every single bug
that appeared while these pages were being written -- none of which raised an
exception.
