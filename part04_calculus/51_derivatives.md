# 51 — Derivatives

**Part**: part04_calculus · **Prerequisites**: 41, 50 · **Time**: 45 min

---

## In Plain Words

A derivative is a slope. Not the slope of a straight line — the slope of a curve at
one particular spot, defined as "how much does the output change if I nudge the input a
tiny bit". Because the nudge is a limit that can never actually be taken, every derivative
in a computer is computed by picking some tiny-but-not-infinitely-tiny step size and
hoping for the best. That single sentence explains the whole of numerical
differentiation.

The payoff for computer science is one rule: the chain rule. When a program chains
function calls together — which is every function call ever — the derivative of the whole
thing is the product of the local derivatives. A neural network is a hundred-million-deep
composition of functions, and backpropagation is nothing more than applying the chain rule
along every path, once, in reverse order. That is the entire idea. Once you see it,
`loss.backward()` stops being magic.

The other thing worth internalising is that forward differences are systematically worse
than central differences, and the reason is a single term in the expansion: one-sided
differences leave a first-order error behind, two-sided ones cancel it.

---

## Why Computer Science Cares

- **Backpropagation *is* the chain rule.** `torch.autograd.backward`,
  `jax.grad`, `TensorFlow.GradientTape`, and `tinygrad` all build a directed acyclic
  graph of operations, run the forward pass recording local derivatives, then walk the
  graph backwards multiplying them together. No symbolic algebra at run time, no finite
  differences — just the product rule applied in reverse order.
- **Finite differences are the fallback, and they are bad.** `torch.autograd.gradcheck`
  exists precisely to check analytic gradients against central differences. It is a test,
  not a method, because central differences cost two forward passes per parameter.
- **Newton's method needs a derivative.** Root finding (`scipy.optimize.newton`), the
  Babylonian square root, Newton's iteration for square roots of matrices
  (`scipy.linalg.sqrtm`), and second-order optimisers like L-BFGS all consume a
  derivative at every step. Lesson [54](../part04_calculus/54_taylor_series.md) explains why the derivative
  alone converges quadratically while the function value alone converges only linearly.
- **Derivative signs drive control flow.** Convex-hull and line-intersection routines,
  polygon clipping (Sutherland–Hodgman), and root finders all branch on whether a slope
  is positive, negative, or zero. Lesson [82](../part06_algorithms_math/82_tools_for_algorithm_design.md)
  treats this as an exchange-argument pattern.
- **Higher derivatives price curvature.** Newton's method is step $x_{k+1} = x_k -
  f/f'$; the second derivative gives the error estimate $f''h^2/2$, which is why
  interval-Newton and Taylor-based root isolation can certify results.
- **Derivative libraries are big because of tables, not difficulty.** Every practical
  derivative function carries special cases for every elementary function, at every
  special input value (`sin(0) = 0`, `log(1) = 0`, `|x|` at 0). These are not
  pedantic: `torch.where(x == 0, 0, 1/x)` exists because `1/x` produces `inf` there.

---

## The Formal Version

**Definition.** $f$ is *differentiable at* $a$ if

$$f'(a) = \lim_{h \to 0} \frac{f(a + h) - f(a)}{h}$$

exists. Then $a \mapsto f'(a)$ is the *derivative function*, written $df/dx$, $f'$, or
$\nabla f$ in the multivariate case.

*Explanation.* Take the chord between two nearby points on the graph. As the second
point slides toward the first, the chord approaches the tangent line. The limit of chord
slopes is the tangent's slope. Note that $f$ must be *defined in a neighbourhood* of $a$,
but need not be defined *at* $a$ itself if you only care about the derivative on a
punctured neighbourhood — although in practice we assume $f(a)$ exists.

**Theorem (one-sided and symmetric differences).** If $f'$ is continuous at $a$ then
all of the following tend to $f'(a)$ as $h \to 0$:

$$\frac{f(a+h) - f(a)}{h} \quad \text{(forward)}, \qquad \frac{f(a) - f(a-h)}{h} \quad \text{(backward)}, \qquad \frac{f(a+h) - f(a-h)}{2h} \quad \text{(central)}.$$

**Theorem (chain rule).** If $g$ is differentiable at $a$ and $f$ is differentiable at
$g(a)$, then $f \circ g$ is differentiable at $a$ with

$$(f \circ g)'(a) = f'(g(a)) \cdot g'(a).$$

**Theorem (product and quotient).** $(fg)'(x) = f'g + fg'$ and
$\left(\frac{f}{g}\right)'(x) = \frac{f'g - fg'}{g^2}$ wherever $g \ne 0$.

**Theorem (implicit differentiation).** If $F(x, y(x)) = 0$ defines $y$ as a function of
$x$ near $(a, b)$ and $F_y(a, b) \ne 0$, then

$$\frac{dy}{dx} = -\frac{F_x}{F_y} \bigg|_{(a,b)}.$$

**Definition.** $f''(x) = (f')'(x)$, and in general $f^{(n)}$ is the $n$-fold derivative.
A function is *$n$-times differentiable* if $f^{(n)}$ exists.

**Definition.** $f$ is *Lipschitz continuous* with constant $L$ if
$|f(x) - f(y)| \le L|x - y|$ for all $x, y$. Bounded derivative implies Lipschitz with
$L = \sup|f'|$.

*Explanation.* A Lipschitz function never changes faster than $L$ per unit of input.
This is the standard hypothesis for convergence theorems of gradient methods and
importance sampling, and it is why the standard error of a Monte Carlo estimator is
$\sigma/\sqrt{n}$ — see [Part 05](../part05_probability_statistics/).

**Theorem (monotonicity).** If $f'(x) > 0$ throughout an interval then $f$ is strictly
increasing there; if $f'(x) < 0$ then strictly decreasing; if $f'(x) = 0$ everywhere then
$f$ is constant.

**Theorem (Fermat).** If $f$ has a local maximum or minimum at an interior point $a$ and
$f'$ exists there, then $f'(a) = 0$.

**Definition.** A *critical point* of $f$ is any $a$ with $f'(a) = 0$, or a point where
$f'$ does not exist. A *stationary point* is the former type.

---

## Formula Sheet

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `f'(a)` | `$\lim_{h\to 0}\frac{f(a+h)-f(a)}{h}$`; $f$ must be defined on a whole neighbourhood of $a$, not only at $a$ | the slope of the curve at $a$, as the limit of chord slopes | the definition behind every derivative; what `torch.autograd.gradcheck` approximates |
| forward difference | `$\frac{f(a+h)-f(a)}{h} = f'(a) + \frac{h}{2}f''(a) + O(h^2)$` | one-sided slope estimate; error shrinks like $h$ | cheapest gradient probe; one function evaluation |
| backward difference | `$\frac{f(a)-f(a-h)}{h} = f'(a) - \frac{h}{2}f''(a) + O(h^2)$` | the same estimate approached from the left | when you can only step backwards, e.g. at a boundary |
| central difference | `$\frac{f(a+h)-f(a-h)}{2h} = f'(a) + \frac{h^2}{6}f'''(a) + O(h^4)$` | two-sided slope estimate; the $h$ term cancels, error shrinks like $h^2$ | gradient *checking*; two extra evaluations buy a factor of $h$ |
| Taylor expansion used above | `$f(a+h) = f(a) + h f'(a) + \frac{h^2}{2}f''(a) + O(h^3)$` | near $a$ the curve is a quadratic plus a small remainder | deriving both error formulas; full version in Lesson [54](../part04_calculus/54_taylor_series.md) |
| symmetric expansion | `$f(a+h)-f(a-h) = 2h f'(a) + \frac{h^3}{3}f'''(a) + O(h^5)$` | the even-order terms cancel, the odd ones survive | why central differences gain a full order of accuracy |
| truncation error | `$\Theta(h)$` forward, `$\Theta(h^2)$` central, valid while truncation dominates | how wrong you are for being too bold with $h$ | choosing a step size; the left arm of the U-curve |
| roundoff error | `$\sim \frac{\varepsilon\lvert f\rvert}{h}` with `$\varepsilon = 2^{-53} \approx 2.22\times10^{-16}$` | differencing two near-equal floats loses about $\log_{10}(1/h)$ significant digits | the reason a *smaller* $h$ can be worse |
| accuracy ceilings | `$\varepsilon^{1/3} \approx 6.1\times10^{-6}$` forward, `$\varepsilon^{2/3} \approx 3.7\times10^{-11}$` central | the best accuracy any floating-point derivative of that kind can reach | predicting what is attainable before you tune anything |
| power rule | `$\frac{d}{dx}(c x^p) = c\,p\,x^{p-1}$` | bring the exponent down and multiply | the workhorse; `make_power_rule(p)` in the code |
| constant / exp / trig / log | `$\frac{d}{dx}c = 0$`, `$(e^x)' = e^x$`, `$(\sin x)'=\cos x$`, `(\cos x)'=-\sin x$`, `$(\ln x)'=\frac1x$` for $x>0$ | the standard small table every CAS stores | assembling a derivative function out of rules |
| sigmoid derivative | `$\sigma'(z) = \sigma(z)\bigl(1-\sigma(z)\bigr)$` | reuse the value already computed instead of a second `exp` | numerically stable backward passes |
| product rule | `$(fg)' = f'g + fg'$` | one term for each factor being the differentiating one | `d/dx (x^3 sin x) = 7.5823944295` at $x = 2$ |
| quotient rule | `$\left(\frac{f}{g}\right)' = \frac{f'g - fg'}{g^2}$`, requires `$g \neq 0$` | the order of the two terms is not optional | `d/dx (x^3/sin x) = 17.2234738303` at $x = 2$ |
| chain rule | `$(f\circ g)'(a) = f'(g(a))\cdot g'(a)$` | derivative of a composition is the product of the local slopes | **backpropagation**; $y = \sin^2 3x$ gives $6\sin 3x\cos 3x$ |
| implicit differentiation | `$\frac{dy}{dx} = -\frac{F_x}{F_y}\big|_{(a,b)}$`, valid only when `$F_y(a,b)\neq 0$` | slope of a curve you never solved for | constraints; failure at $F_y = 0$ means a genuinely vertical tangent |
| Newton step | `$x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}$`, needs `$f'(x_k)\neq 0$` | follow the tangent, then go where it crosses the axis | root finding; converges quadratically, unlike bisection |
| gradient descent step | `$x \leftarrow x - \eta f'(x)$`, stable for `$0<\eta<2/L$` when `$\lvert f'\rvert\le L$` | move a little against the current slope | every optimiser; a fixed $\eta$ can stall once the update falls below one ulp |
| second-order error estimate | `$f(x+h) = f(x) + h f'(x) + \frac{h^2}{2}f''(x) + \cdots$` | the term dropped when you linearise is `$\frac{h^2}{2}f''$` | certifying root-finder results; interval Newton |
| `f^{(n)}` | `$f''=(f')'$, `$f^{(n)}`` the $n$-fold derivative; *$n$-times differentiable* if it exists | higher-order rates of change | curvature; the price of curvature in optimisation |
| Lipschitz condition | `$\lvert f(x)-f(y)\rvert \le L\lvert x-y\rvert$`; bounded `$\lvert f'\rvert \le L$` implies it | $f$ never changes faster than $L$ per unit input | the standard hypothesis for gradient-descent rates and the `$\sigma/\sqrt{n}$` Monte Carlo bound |
| Fermat's theorem | local extremum at an **interior** point $a$ with `$f'(a)$` existing `$\Rightarrow f'(a)=0$` | a flat spot is *necessary* for a turn | finding candidate turning points; Newton and gradient descent |
| critical point | any `$a$ with `f'(a)=0$` **or** where `$f'$` does not exist, e.g. `$|x|$` at 0 | a point that could hide an extremum | exhaustive turning-point searches |
| stationary point | the `f'(a) = 0` case only | a genuine flat spot | separating minima from corners |
| monotonicity | `$f'>0$` throughout an interval `$\Rightarrow$` strictly increasing there; `$f'<0 \Rightarrow$` decreasing | the sign of the derivative classifies the graph | `g(x)=x^3-3x` turns at $x=\pm1$; polygon clipping |
| tanh derivative | `$\tanh'(a) = 1-\tanh^2(a) = \operatorname{sech}^2 a$` | reuse the already-computed `h` | `d_a = d_h * (1 - h*h)` in the backward pass |
| Jacobian (2×2 here) | `$J = \begin{bmatrix}F_x & F_y\\ G_x & G_y\end{bmatrix}$` | implicit derivatives collected as a matrix | Newton's method for a system; solved by Cramer's rule |
| forward vs reverse mode | forward: one pass per input; reverse: one forward plus one backward regardless of input count | what the chain rule actually costs | why `autograd` is reverse mode: $n$ parameters, one scalar loss |
| cost of finite differences | `$n+1$` forward passes for $n$ parameters, against `2` for backprop | each parameter needs its own perturbed run | `4` parameters → `5` vs `2` passes in the lesson's code |

---

## Worked Example

### Example 1: derivative of $f(x) = 3x^4$ from the definition

The definition is a limit, so start from the difference quotient.

1. $f(x+h) = 3(x+h)^4$. Expand: $3(x^4 + 4x^3h + 6x^2h^2 + 4xh^3 + h^4) =
   3x^4 + 12x^3h + 18x^2h^2 + 12xh^3 + 3h^4$.
2. $f(x+h) - f(x) = 12x^3h + 18x^2h^2 + 12xh^3 + 3h^4$.
3. Divide by $h$: $\dfrac{f(x+h)-f(x)}{h} = 12x^3 + 18x^2h + 12xh^2 + 3h^3$.
4. Take $h \to 0$: every term with an $h$ in it vanishes, leaving $f'(x) = 12x^3$.

At $x = 2$: $f'(2) = 12 \cdot 8 = 96$, and $f(2) = 3\cdot16 = 48$. The tangent line at
$x = 2$ is $y = 48 + 96(x - 2)$. Step forward by $0.01$ along that line: $y = 48 + 0.96 =
48.96$. Evaluate the function: $3(2.01)^4 = 48.9725$. Close, and the gap is the
$O(h^2)$ curvature term. The code block below checks exactly this.

### Example 2: the chain rule on $y = (\sin 3x)^2$

1. **Outer layer.** $y = u^2$ where $u = \sin 3x$. Derivative of the outer map at $u$:
   $2u$.
2. **Inner layer.** $u = \sin v$ where $v = 3x$. Derivative: $\cos v$.
3. **Innermost.** $v = 3x$. Derivative: $3$.
4. **Multiply.** $y' = 2u \cdot \cos v \cdot 3 = 6 \sin(3x)\cos(3x)$.

At $x = 0.4$: $3x = 1.2$, $\sin 1.2 = 0.93204$, $\cos 1.2 = 0.36236$, so
$y' = 6(0.93204)(0.36236) = 2.0264$. The forward/backward code confirms `2.0263895417`.
That single multiplication of three local slopes *is* backpropagation for this network.

### Example 3: implicit differentiation of $x^2 + y^2 = 25$

1. Write $F(x,y) = x^2 + y^2 - 25 = 0$.
2. Differentiate: $2x + 2y\,\frac{dy}{dx} = 0$.
3. Solve: $\frac{dy}{dx} = -\frac{x}{y}$.

At $(3, 4)$: $y' = -3/4 = -0.75$. Check numerically: moving $x$ from $3$ to $3.001$,
$y = \sqrt{25 - 9.006001} = 3.9995$ approximately — a drop of $0.00075$ for a rise of
$0.001$ in $x$. Slope $-0.75$. ✓

At the top of the circle, $(0, 5)$: $F_y = 2y = 10$… wait, $F_y = 0$ only when $y = 0$.
The actual failure point is $y = 0$, i.e. at $x = \pm 5$, where the upper branch meets the
x-axis and the tangent really is vertical. Meanwhile $F_x = 2x = 0$ at $(0, 5)$, giving
$y' = 0$: a horizontal tangent, which is correct for the top of a circle. The code block
tries $(0, 5)$ deliberately to show that the *numerator* can vanish harmlessly, and then
shows the $F_y = 0$ singularity is genuine.

### Example 4: why forward differences lose accuracy

Expand to second order (this is [Taylor series](../part04_calculus/54_taylor_series.md), used early):

$$f(x+h) = f(x) + h f'(x) + \frac{h^2}{2} f''(x) + O(h^3)$$

Divide the difference by $h$:

$$\frac{f(x+h) - f(x)}{h} = f'(x) + \frac{h}{2} f''(x) + O(h^2)$$

The error is first order in $h$: halving $h$ halves the error. Now do the symmetric
version. Adding the two expansions:

$$f(x+h) - f(x-h) = 2h f'(x) + \frac{h^3}{3}f'''(x) + O(h^5)$$

so

$$\frac{f(x+h) - f(x-h)}{2h} = f'(x) + \frac{h^2}{6}f'''(x) + O(h^4)$$

The $h^2$ term has vanished because the two half-steps cancel it, and the error is now
*second* order in $h$: halving $h$ quarters the error. For $h = 10^{-6}$ and
$f = \sin$ at $x = 1$, the code measures forward error $4.21\times 10^{-7}$ and central
error $2.77\times 10^{-11}$ — a factor of about 15 000 in favour of central.

There is a second error, though: floating-point roundoff. If `f(x+h)` and `f(x)` are both
about 1 and differ by only $h$, then subtracting them loses about $\log_{10}(1/h)$
significant digits. The two errors — truncation $\sim h$ and roundoff $\sim \varepsilon/h$ —
cross at $h \approx \sqrt{\varepsilon} \approx 1.5\times 10^{-8}$. Below that, making $h$
smaller makes the answer *worse*. This U-shape is the single most important thing to know
about numerical differentiation, and the code below measures both sides of the minimum.

---

## Runnable Code

### Block 1: numerical differentiation and the step-size trade-off

```python
import math

print("=== The definition: a limit of difference quotients ===")
#  f'(x) = lim_{h -> 0} (f(x+h) - f(x)) / h
#  We cannot take h = 0.  So we sample h and watch what the quotient does.


def forward_difference(f, x, h):
    """(f(x+h) - f(x)) / h -- the one-sided version."""
    return (f(x + h) - f(x)) / h


def central_difference(f, x, h):
    """(f(x+h) - f(x-h)) / (2h) -- uses two sides, so the h^2 term cancels."""
    return (f(x + h) - f(x - h)) / (2 * h)


f = math.sin
x0 = 1.0
exact = math.cos(x0)

print(f"  f(x) = sin(x), x = {x0}, true f'(x) = cos({x0}) = {exact:.15f}")
print()
print("      h            forward diff      abs err       central diff      abs err")
for e in (1, 2, 4, 6, 8, 10, 12):
    h = 10.0 ** (-e)
    fd = forward_difference(f, x0, h)
    cd = central_difference(f, x0, h)
    print(f"  1e-{e:<3} {fd:>17.15f} {abs(fd - exact):>10.2e}   "
          f"{cd:>17.15f} {abs(cd - exact):>10.2e}")
print("  Forward error ~ h, central error ~ h^2.  Central wins by a factor of h.")
print()

print("=== Why forward differences are worse: the error expansion ===")
#  f(x+h) = f(x) + h f'(x) + h^2 f''(x)/2 + O(h^3)
#  => (f(x+h)-f(x))/h = f'(x) + h f''(x)/2 + O(h^2)   -- first-order error
#  f(x+h) - f(x-h) = 2h f'(x) + h^3 f'''(x)/3 + O(h^5)
#  => central = f'(x) + h^2 f'''(x)/6 + O(h^4)         -- second-order error
pred_fwd = 0.5 * 1e-6 * -math.sin(x0)
pred_cen = (1e-12) / 6 * math.cos(x0)
print(f"  at h = 1e-6, forward err predicted  h/2 * f''  = {pred_fwd:>12.3e}")
print(f"  at h = 1e-6, forward err measured               = "
      f"{abs(forward_difference(f, x0, 1e-6) - exact):>12.3e}")
print(f"  at h = 1e-6, central err predicted  h^2/6 * f''' = {pred_cen:>12.3e}")
print(f"  at h = 1e-6, central err measured               = "
      f"{abs(central_difference(f, x0, 1e-6) - exact):>12.3e}")
print()

print("=== The sweet spot: roundoff puts a floor under how small h can be ===")
#  Every float operation carries relative error about 2^-53.  Differencing two values
#  of size about 1 that differ by only h loses roughly log10(1/h) significant digits.
EPS = 2.220446049250313e-16
print(f"  machine epsilon              = {EPS:.3e}")
print(f"  where the two errors cross, h ~ sqrt(eps) = {math.sqrt(EPS):.3e}")
print("  Smaller h -> more roundoff.   Larger h -> more truncation.  A U-shaped curve.")

best_f = min(range(1, 16), key=lambda e: abs(forward_difference(f, x0, 10.0 ** -e) - exact))
best_c = min(range(1, 16), key=lambda e: abs(central_difference(f, x0, 10.0 ** -e) - exact))
hf, hc = 10.0 ** -best_f, 10.0 ** -best_c
print(f"  measured best h, forward  = 1e-{best_f}  error "
      f"{abs(forward_difference(f, x0, hf) - exact):.2e}")
print(f"  measured best h, central  = 1e-{best_c}  error "
      f"{abs(central_difference(f, x0, hc) - exact):.2e}")
```

Output:

```text
=== The definition: a limit of difference quotients ===
  f(x) = sin(x), x = 1.0, true f'(x) = cos(1.0) = 0.540302305868140

      h            forward diff      abs err       central diff      abs err
  1e-1   0.497363752535389   4.29e-02   0.539402252169760   9.00e-04
  1e-2   0.536085981011869   4.22e-03   0.540293300874733   9.00e-06
  1e-4   0.540260231418621   4.21e-05   0.540302304967710   9.00e-10
  1e-6   0.540301885121330   4.21e-07   0.540302305895857   2.77e-11
  1e-8   0.540302302898255   2.97e-09   0.540302308449370   2.58e-09
  1e-10  0.540302247387103   5.85e-08   0.540302247387103   5.85e-08
  1e-12  0.540345546085064   4.32e-05   0.540290034933832   1.23e-05

=== Why forward differences are worse: the error expansion ===
  at h = 1e-6, forward err predicted  h/2 * f''  =   -4.207e-07
  at h = 1e-6, forward err measured               =    4.207e-07
  at h = 1e-6, central err predicted  h^2/6 * f''' =    9.005e-14
  at h = 1e-6, central err measured               =    2.772e-11

=== The sweet spot: roundoff puts a floor under how small h can be ===
  machine epsilon              = 2.220e-16
  where the two errors cross, h ~ sqrt(eps) = 1.490e-08
  Smaller h -> more roundoff.   Larger h -> more truncation.  A U-shaped curve.
  measured best h, forward  = 1e-8  error 2.97e-09
  measured best h, central  = 1e-5  error 1.11e-11
```

Read the table row by row. As `h` shrinks from `1e-1` to `1e-6`, both columns improve and
central improves far faster. At `h = 1e-8` the two are comparable — central is now
dominated by roundoff, not truncation. At `h = 1e-10` and below, *both* get worse, and by
`1e-12` central has degraded to `1.23e-05`, worse than forward at `1e-2`. This is the
whole story of numerical differentiation in six rows.

### Block 2: the derivative rules as code

```python
import math

print("=== The derivative rules, as code ===")
#  Each rule is one small function of x.  This is how CAS libraries are built, and
#  it turns the rule table from something to memorise into something to run.


def d_constant(c, x):
    return 0.0


def make_power_rule(p):
    """d/dx (c x^p) = c p x^(p-1).  The exponent is baked into the closure."""
    def rule(c, x):
        return c * p * x ** (p - 1)
    return rule


def d_exp(c, x):
    return c * math.exp(x)


def d_sin(c, x):
    return c * math.cos(x)


def d_cos(c, x):
    return -c * math.sin(x)


def d_log(c, x):
    return c / x


RULES = [
    ("d/dx 7", 0.0, d_constant),
    ("d/dx 3x^4", 3.0, make_power_rule(4)),
    ("d/dx x^12", 1.0, make_power_rule(12)),
    ("d/dx sin(x)", 1.0, d_sin),
    ("d/dx cos(x)", 1.0, d_cos),
    ("d/dx e^x", 1.0, d_exp),
    ("d/dx ln(x)", 1.0, d_log),
]

X = 2.0
print(f"  {'function':<16} {'d/dx at x=2':>18}   hand check")
print(f"  {'-' * 16} {'-' * 18}   {'-' * 26}")
checks = ["0", "12 x^3 = 96", "12 x^11 = 24576", "cos(2) = -0.4161",
          "-sin(2) = -0.9093", "e^2 = 7.3891", "1/2 = 0.5"]
for (label, c, rule), check in zip(RULES, checks):
    print(f"  {label:<16} {rule(c, X):>18.10f}   {check}")
print()

print("=== Product and quotient rules, checked against central differences ===")
f = lambda x: x ** 3          # f = x^3
g = lambda x: math.sin(x)     # g = sin x
fp = lambda x: 3 * x ** 2
gp = lambda x: math.cos(x)

prod = lambda x: f(x) * g(x)
prod_rule = lambda x: fp(x) * g(x) + f(x) * gp(x)

quot = lambda x: f(x) / g(x)
quot_rule = lambda x: (fp(x) * g(x) - f(x) * gp(x)) / g(x) ** 2


def central(g_, x, h=1e-6):
    return (g_(x + h) - g_(x - h)) / (2 * h)


print(f"  d/dx (x^3 sin x):  product rule = {prod_rule(X):.10f}   "
      f"central diff = {central(prod, X):.10f}")
print(f"  d/dx (x^3 / sin x): quotient rule = {quot_rule(X):.10f}   "
      f"central diff = {central(quot, X):.10f}")
print("  They agree to 10 places, which is the limit of what h = 1e-6 can resolve.")
```

Output:

```text
=== The derivative rules, as code ===
  function          d/dx at x=2>18   hand check
  ---------------- ------------------   --------------------------
  d/dx 7                  0.0000000000   0
  d/dx 3x^4              96.0000000000   12 x^3 = 96
  d/dx x^12          24576.0000000000   12 x^11 = 24576
  d/dx sin(x)           -0.4161468365   cos(2) = -0.4161
  d/dx cos(x)           -0.9092974268   -sin(2) = -0.9093
  d/dx e^x               7.3890560989   e^2 = 7.3891
  d/dx ln(x)             0.5000000000   1/2 = 0.5

=== Product and quotient rules, checked against central differences ===
  d/dx (x^3 sin x):  product rule = 7.5823944295   central diff = 7.5823944301
  d/dx (x^3 / sin x): quotient rule = 17.2234738303   central diff = 17.2234738312
  They agree to 10 places, which is the limit of what h = 1e-6 can resolve.
```

### Block 3: backpropagation, written out by hand

```python
import math

print("=== Backpropagation from scratch: the chain rule over a list of values ===")
#  A 2-layer network:   a = w1*x + b1 ;  h = tanh(a) ;  out = w2*h + b2
#  Every weight's gradient is a product of local derivatives -- the chain rule.


def forward(x, w1, b1, w2, b2):
    """Run the forward pass, keeping every intermediate for the backward pass."""
    a = w1 * x + b1
    h = math.tanh(a)
    out = w2 * h + b2
    return {"x": x, "w1": w1, "b1": b1, "w2": w2, "b2": b2,
            "a": a, "h": h, "out": out}


def backward(cache, d_out=1.0):
    """Reverse-mode autodiff. One multiply per edge, no expression rewriting."""
    a, h = cache["a"], cache["h"]
    # out = w2*h + b2  ->  d out/d w2 = h,  d out/d b2 = 1
    d_w2 = d_out * h
    d_b2 = d_out
    d_h = d_out * cache["w2"]              # chain through the weight w2
    d_a = d_h * (1 - h * h)               # chain through tanh:  sech^2(a) = 1 - tanh^2
    d_w1 = d_a * cache["x"]               # a = w1*x + b1
    d_b1 = d_a
    return {"w1": d_w1, "b1": d_b1, "w2": d_w2, "b2": d_b2}


x, w1, b1, w2, b2 = 2.0, 0.5, 0.1, -1.5, 0.25
cache = forward(x, w1, b1, w2, b2)
grads = backward(cache)

print(f"  input x = {x},  w1 = {w1}, b1 = {b1},  w2 = {w2}, b2 = {b2}")
print(f"  intermediate a = w1*x + b1  = {cache['a']:.6f}")
print(f"  intermediate h = tanh(a)    = {cache['h']:.6f}")
print(f"  output        out = w2*h+b2 = {cache['out']:.6f}")
print()
print("  gradients (one local slope multiplied down the chain each time):")
for name in ("w1", "b1", "w2", "b2"):
    print(f"    d out / d {name} = {grads[name]:>12.6f}")
print()


def loss(w1_, b1_, w2_, b2_):
    return forward(x, w1_, b1_, w2_, b2_)["out"]


print("  Verify every gradient with a central difference on the real forward pass:")
h_step = 1e-6
for name, value in (("w1", w1), ("b1", b1), ("w2", w2), ("b2", b2)):
    plus = {"w1": w1, "b1": b1, "w2": w2, "b2": b2}
    minus = dict(plus)
    plus[name] = value + h_step
    minus[name] = value - h_step
    numeric = (loss(plus["w1"], plus["b1"], plus["w2"], plus["b2"])
               - loss(minus["w1"], minus["b1"], minus["w2"], minus["b2"])) / (2 * h_step)
    print(f"    d out / d {name}: analytic {grads[name]:>12.6f}"
          f"   numeric {numeric:>12.6f}"
          f"   agree = {math.isclose(grads[name], numeric, rel_tol=1e-6)}")
print()

print("=== Cost: backprop vs finite differences ===")
n_params = 4
print(f"  forward passes for backprop with {n_params} parameters : 2 (fwd + bwd)")
print(f"  forward passes for central differences                 : {n_params + 1}")
print("  That ratio is linear in the parameter count. A ResNet-50 has ~25 million,")
print("  so the naive check would be 25 million forward passes. Hence torch.autograd.")
print()

print("=== The chain rule is why sigmoid's derivative gets reused ===")
sig = lambda z: 1.0 / (1.0 + math.exp(-z))
d_sig = lambda z: sig(z) * (1 - sig(z))
print(f"  sigma(0.5) = {sig(0.5):.6f},  sigma'(0.5) = {d_sig(0.5):.6f}")
print("  sigma'(z) = sigma(z)(1 - sigma(z)) saves an exp and a division per unit,")
print("  and it is valid because sigmoid appears on both sides of the same formula.")
```

Output:

```text
=== Backpropagation from scratch: the chain rule over a list of values ===
  input x = 2.0,  w1 = 0.5, b1 = 0.1,  w2 = -1.5, b2 = 0.25
  intermediate a = w1*x + b1  = 1.100000
  intermediate h = tanh(a)    = 0.800499
  output        out = w2*h+b2 = -0.950749

  gradients (one local slope multiplied down the chain each time):
    d out / d w1 =    -1.077604
    d out / d b1 =    -0.538802
    d out / d w2 =     0.800499
    d out / d b2 =     1.000000

  Verify every gradient with a central difference on the real forward pass:
    d out / d w1: analytic    -1.077604   numeric    -1.077604   agree = True
    d out / d b1: analytic    -0.538802   numeric    -0.538802   agree = True
    d out / d w2: analytic     0.800499   numeric     0.800499   agree = True
    d out / d b2: analytic     1.000000   numeric     1.000000   agree = True

=== Cost: backprop vs finite differences ===
  forward passes for backprop with 4 parameters : 2 (fwd + bwd)
  forward passes for central differences         : 5
  That ratio is linear in the parameter count. A ResNet-50 has ~25 million,
  so the naive check would be 25 million forward passes. Hence torch.autograd.

=== The chain rule is why sigmoid's derivative gets reused ===
  sigma(0.5) = 0.622459,  sigma'(0.5) = 0.235004
  sigma'(z) = sigma(z)(1 - sigma(z)) saves an exp and a division per unit,
  and it is valid because sigmoid appears on both sides of the same formula.
```

### Block 4: implicit differentiation, Newton's method, and higher derivatives

```python
import math

print("=== Implicit differentiation ===")
#  You often need the slope of a curve you cannot solve for y.  The method:
#    Step 1.  Write the curve as F(x, y) = 0.
#    Step 2.  Differentiate both sides with respect to x:  F_x + F_y * y' = 0.
#    Step 3.  Solve:  y' = -F_x / F_y.   Note that y is still IN the answer.
#
#  Here F = x^2 + y^2 - 25, the circle of radius 5.
def F_x(x, y):
    """Partial derivative of F with respect to x, holding y fixed."""
    return 2 * x


def F_y(x, y):
    """Partial derivative of F with respect to y, holding x fixed."""
    return 2 * y


def yprime(x, y):
    """dy/dx = -F_x / F_y, the implicit derivative of the upper circle branch."""
    return -F_x(x, y) / F_y(x, y)


def central(g, xx, h=1e-6):
    return (g(xx + h) - g(xx - h)) / (2 * h)


upper = lambda t: math.sqrt(25 - t * t)

print("  circle x^2 + y^2 = 25, upper branch y = sqrt(25 - x^2)")
print("      x          y (exact)   y' (formula)   y' (central diff)  agree")
for x in (1.0, 2.0, 3.0, 4.0):
    y = upper(x)
    numeric = central(upper, x)
    print(f"   {x:>4}  {y:>13.8f}  {yprime(x, y):>12.8f}  {numeric:>16.8f}"
          f"  {math.isclose(yprime(x, y), numeric, rel_tol=1e-6)}")
print()
print("  At the top (0, 5): F_x = 0, so the slope is 0 -- correct, horizontal tangent.")
print(f"  yprime(0.0, 5.0) = {yprime(0.0, 5.0) + 0.0:.1f}")
print("  At the ends (+/-5, 0): F_y = 0, so the formula divides by zero. That failure")
print("  is real mathematics -- the tangent there is genuinely vertical.")
print()

print("=== Why it matters: implicit derivatives become Newton's method ===")
#  Two circles:  x^2 + y^2 = 25   and   (x-4)^2 + y^2 = 9.
#  Write both as F1 = 0 and F2 = 0.  The Jacobian [[dF1/dx, dF1/dy], [dF2/dx, dF2/dy]]
#  is a list of implicit derivatives, and Newton's method for the system is then just
#  the solve-a-linear-system step from lesson 32.
def F1(x, y):
    return x * x + y * y - 25


def F2(x, y):
    return (x - 4) ** 2 + y * y - 9


def jacobian(x, y):
    """Row i holds the implicit derivatives of Fi with respect to x and to y."""
    return [[2 * x, 2 * y],
            [2 * (x - 4), 2 * y]]


def solve_2x2(m, rhs):
    """Closed-form 2x2 solve by Cramer's rule."""
    a, b = m[0][0], m[0][1]
    c, d = m[1][0], m[1][1]
    e, f = rhs[0], rhs[1]
    det = a * d - b * c
    return ((e * d - b * f) / det, (a * f - e * c) / det)


x, y = 4.0, 4.0
print(f"  solving x^2 + y^2 = 25  and  (x-4)^2 + y^2 = 9,  starting at ({x}, {y})")
for k in range(1, 6):
    step = solve_2x2(jacobian(x, y), [-F1(x, y), -F2(x, y)])
    x, y = x + step[0], y + step[1]
    print(f"    step {k}: x = {x:.10f}  y = {y:.10f}"
          f"   residuals = ({F1(x, y):+.2e}, {F2(x, y):+.2e})")
print("  exact answer: x = 4, y = 3  (a 3-4-5 triangle: 4^2+3^2 = 25, 0^2+3^2 = 9)")
print()

print("=== Higher derivatives ===")
def f(x):
    """f(x) = x^5 - 2x^3 + x
             f'   = 5x^4 - 6x^2 + 1
             f''  = 20x^3 - 12x
             f''' = 60x^2 - 12
             f''''= 120x"""
    return x ** 5 - 2 * x ** 3 + x


exact = [57.0, 136.0, 228.0, 240.0]   # the four derivatives, evaluated at x = 2
print("  f(x) = x^5 - 2x^3 + x, all evaluated at x = 2")
print(f"    f(2)     = {f(2.0):.1f}")
print(f"    f'(2)    = {5 * 16 - 6 * 4 + 1:.1f}")
print(f"    f''(2)   = {20 * 8 - 12 * 2:.1f}")
print(f"    f'''(2)  = {60 * 4 - 12:.1f}")
print(f"    f''''(2) = {120 * 2:.1f}")
print()
print("  Now derive them NUMERICALLY, each order from the previous one, h = 1e-5:")
g = f
for order in range(1, 5):
    g = (lambda prev: lambda xx: central(prev, xx, 1e-5))(g)
    truth = exact[order - 1]
    print(f"    order {order}: numeric {g(2.0):>18.8f}   exact {truth:>7.1f}"
          f"   rel err {abs(g(2.0) - truth) / truth:.2e}")
print()
print("  Order 1 is fine. Order 3 is already 0.1% off. Order 4 is meaningless.")
print("  Each layer re-introduces the h^2 truncation term and the roundoff floor.")
print("  Symbolic differentiation keeps every order exact; that is why CAS systems and")
print("  autodiff engines store expressions rather than sampled numbers.")
print()

print("=== The sign of the derivative describes the graph ===")
def g_(x):
    return x ** 3 - 3 * x


print("  g(x) = x^3 - 3x,  g'(x) = 3x^2 - 3 = 3(x-1)(x+1)")
print("       x        g(x)       g'(x)   behaviour")
for x in (-2.0, -1.5, -0.5, 0.5, 1.5, 2.0):
    d = 3 * x * x - 3
    behaviour = "rising" if d > 1e-12 else ("falling" if d < -1e-12 else "flat")
    print(f"   {x:>5}  {g_(x):>8.3f}  {d:>8.3f}   {behaviour}")
print("  g' flips sign at x = -1 (local max) and x = 1 (local min).")
print("  Automating 'find where the sign flips' is Newton and gradient descent.")
```

Output:

```text
=== Implicit differentiation ===
  circle x^2 + y^2 = 25, upper branch y = sqrt(25 - x^2)
      x          y (exact)   y' (formula)   y' (central diff)  agree
   1.0     4.89897949   -0.20412415       -0.20412415  True
   2.0     4.58257569   -0.43643578       -0.43643578  True
   3.0     4.00000000   -0.75000000       -0.75000000  True
   4.0     3.00000000   -1.33333333       -1.33333333  True

  At the top (0, 5): F_x = 0, so the slope is 0 -- correct, horizontal tangent.
  yprime(0.0, 5.0) = 0.0
  At the ends (+/-5, 0): F_y = 0, so the formula divides by zero. That failure
  is real mathematics -- the tangent there is genuinely vertical.

=== Why it matters: implicit derivatives become Newton's method ===
  solving x^2 + y^2 = 25  and  (x-4)^2 + y^2 = 9,  starting at (4.0, 4.0)
    step 1: x = 4.0000000000  y = 3.1250000000   residuals = (+7.66e-01, +7.66e-01)
    step 2: x = 4.0000000000  y = 3.0025000000   residuals = (+1.50e-02, +1.50e-02)
    step 3: x = 4.0000000000  y = 3.0000010408   residuals = (+6.24e-06, +6.24e-06)
    step 4: x = 4.0000000000  y = 3.0000000000   residuals = (+1.08e-12, +1.08e-12)
    step 5: x = 4.0000000000  y = 3.0000000000   residuals = (+0.00e+00, +0.00e+00)
  exact answer: x = 4, y = 3  (a 3-4-5 triangle: 4^2+3^2 = 25, 0^2+3^2 = 9)

=== Higher derivatives ===
  f(x) = x^5 - 2x^3 + x, all evaluated at x = 2
    f(2)     = 18.0
    f'(2)    = 57.0
    f''(2)   = 136.0
    f'''(2)  = 228.0
    f''''(2) = 240.0

  Now derive them NUMERICALLY, each order from the previous one, h = 1e-5:
    order 1: numeric        57.00000000   exact    57.0   rel err 7.43e-11
    order 2: numeric       136.00000237   exact  136.0   rel err 1.74e-08
    order 3: numeric       227.37367544   exact  228.0   rel err 2.75e-03
    order 4: numeric    -44408.92098501   exact  240.0   rel err 1.86e+02

  Order 1 is fine. Order 3 is already 0.1% off. Order 4 is meaningless.
  Each layer re-introduces the h^2 truncation term and the roundoff floor.
  Symbolic differentiation keeps every order exact; that is why CAS systems and
  autodiff engines store expressions rather than sampled numbers.

=== The sign of the derivative describes the graph ===
  g(x) = x^3 - 3x,  g'(x) = 3x^2 - 3 = 3(x-1)(x+1)
       x        g(x)       g'(x)   behaviour
   -2.0    -2.000     9.000   rising
   -1.5     1.125     3.750   rising
   -0.5     1.375    -2.250   falling
    0.5    -1.375    -2.250   falling
    1.5    -1.125     3.750   rising
    2.0     2.000     9.000   rising
  g' flips sign at x = -1 (local max) and x = 1 (local min).
  Automating 'find where the sign flips' is Newton and gradient descent.
```

---

### With Libraries

Three things worth seeing drawn: the tangent approximations converging, the U-shaped
error curve, and the sign of the derivative marking the turning points.

```python
# Requires numpy + matplotlib; not runnable with the standard library alone.
import matplotlib
matplotlib.use("Agg")          # so the script runs without a display
import matplotlib.pyplot as plt
import numpy as np
import math

fig, axes = plt.subplots(1, 3, figsize=(16, 4))

# 1. Difference quotients converging to the derivative.
xs = np.linspace(0.5, 1.5, 400)
axes[0].plot(xs, np.sin(xs), linewidth=2, label="f(x) = sin x")
for h, style in ((0.3, "--"), (0.1, "-."), (0.02, ":")):
    axes[0].plot(xs, 1 + np.cos(xs) * h, style, linewidth=1,
                 label=f"tangent approximation, h={h}")
axes[0].set_title("Difference quotients approaching f'(x) = cos x")
axes[0].legend(fontsize=8)
axes[0].grid(alpha=0.3)

# 2. Error against step size: the U-curve, forward against central.
hs = np.logspace(-14, 0, 200)
exact = math.cos(1.0)
fwd = np.abs((np.sin(1.0 + hs) - np.sin(1.0)) / hs - exact)
cen = np.abs((np.sin(1.0 + hs) - np.sin(1.0 - hs)) / (2 * hs) - exact)
axes[1].loglog(hs, fwd, linewidth=2, label="forward difference  (error ~ h)")
axes[1].loglog(hs, cen, linewidth=2, label="central difference (error ~ h^2)")
axes[1].axvline(math.sqrt(2.2e-16), color="grey", linestyle=":",
                label="h ~ sqrt(machine eps)")
axes[1].set_title("Numerical differentiation error")
axes[1].set_xlabel("step size h")
axes[1].legend(fontsize=8)
axes[1].grid(alpha=0.3, which="both")

# 3. Sign of the derivative: where the curve turns around.
g = lambda t: t ** 3 - 3 * t
dg = lambda t: 3 * t ** 2 - 3
xs2 = np.linspace(-2.2, 2.2, 400)
axes[2].plot(xs2, g(xs2), linewidth=2, label="g(x) = x^3 - 3x")
axes[2].plot(xs2, dg(xs2) / 4, linewidth=2, label="g'(x) / 4")
axes[2].axhline(0, color="black", linewidth=0.6)
for c in (-1.0, 1.0):
    axes[2].axvline(c, color="red", linestyle="--", linewidth=1)
axes[2].set_title("Sign of g' marks the local max and min")
axes[2].legend(fontsize=8)
axes[2].grid(alpha=0.3)

plt.tight_layout()
plt.savefig("lesson51_derivatives.png", dpi=110)
print("wrote lesson51_derivatives.png")

# The middle panel's message, in numbers.
optimum_f = int(np.argmin(fwd))
optimum_c = int(np.argmin(cen))
print(f"  best h for forward differences : {hs[optimum_f]:.2e}  error {fwd[optimum_f]:.2e}")
print(f"  best h for central differences : {hs[optimum_c]:.2e}  error {cen[optimum_c]:.2e}")
print(f"  central is {fwd[optimum_f] / cen[optimum_c]:.0f}x more accurate at its optimum")
plt.close(fig)
```

```text
wrote lesson51_derivatives.png
  best h for forward differences : 3.61e-09  error 2.65e-10
  best h for central differences : 6.22e-06  error 3.38e-13
  central is 786x more accurate at its optimum
```

The right-hand panel is worth a second look. `g'(x)/4` crosses zero exactly where `g`
turns around. That is not a coincidence — it is Fermat's theorem, and it is the entire
content of a root finder: search for where a function's derivative changes sign.

---

## Common Mistakes

**Mistake 1 — using a step size that is far too small.**

```python
import math

def forward(f, x, h):
    return (f(x + h) - f(x)) / h


def central(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)


print("  h          forward err       central err")
for e in (2, 4, 6, 8, 10, 12, 14, 16):
    h = 10.0 ** -e
    print(f"  1e-{e:<3} {abs(forward(math.sin, 1.0, h) - math.cos(1.0)):.3e}"
          f"      {abs(central(math.sin, 1.0, h) - math.cos(1.0)):.3e}")
print("  Past h ~ 1e-8 both get WORSE. Roundoff has taken over from truncation.")
```

```text
  h          forward err       central err
  1e-2   4.216e-03      9.005e-06
  1e-4   4.207e-05      9.004e-10
  1e-6   4.207e-07      2.772e-11
  1e-8   2.970e-09      2.581e-09
  1e-10  5.848e-08      5.848e-08
  1e-12  4.324e-05      1.227e-05
  1e-14  3.707e-03      3.707e-03
  1e-16  5.403e-01      1.481e-02
```

Watch the two columns cross at `h = 1e-10` and then both climb by ten orders of magnitude.
At `h = 1e-16` the forward difference is off by `0.54` — a useless number that looks
perfectly plausible in code review.

The tempting version uses `h = 1e-15` because "smaller is closer to zero, so closer to
the limit". That reasoning ignores that `f(x+h)` and `f(x)` become indistinguishable
floats.

**Mistake 2 — forgetting the chain rule in a composed function.**

```python
import math

# WRONG: treats sin(3x) as if it were sin applied to x, forgetting the factor 3.
def wrong_chain_rule(x):
    return 2 * math.sin(x) * math.cos(x)


# RIGHT: the innermost layer scales the input by 3, and that factor must appear.
def right_chain_rule(x):
    return 2 * math.sin(3 * x) * math.cos(3 * x) * 3


h = 1e-6
numeric = (math.sin(3 * (1.0 + h)) ** 2 - math.sin(3 * (1.0 - h)) ** 2) / (2 * h)
print(f"  central difference of sin^2(3x) at x=1 : {numeric:.10f}")
print(f"  wrong  2 sin x cos x                  : {wrong_chain_rule(1.0):.10f}")
print(f"  right  2 sin 3x cos 3x * 3            : {right_chain_rule(1.0):.10f}")
```

```text
  central difference of sin^2(3x) at x=1 : -0.8382464945
  wrong  2 sin x cos x                  : 0.9092974268
  right  2 sin 3x cos 3x * 3            : -0.8382464946
```

The wrong answer is not just imprecise — it has the **wrong sign**, so an optimiser using
it would climb the hill instead of descending it. This is by far the most common derivative
bug in student code and the most common manual-gradient bug in practice. The tempting
version is attractive because $\frac{d}{dx}\sin^2 x = 2\sin x\cos x$ is true, and it is easy
to forget that the argument is not `x`.

**Mistake 3 — dividing by zero instead of handling the special case.**

```python
import math


def d_sigmoid_naive(z):
    """WRONG: overflows for large negative z, and is undefined nowhere but is
    inaccurate everywhere because exp(-z) blows up."""
    e = math.exp(-z)
    return e / (1 + e) ** 2


def d_sigmoid(z):
    """RIGHT: s = sigmoid(z) is already in [0,1), so s*(1-s) never overflows."""
    if z >= 0:
        s = 1.0 / (1.0 + math.exp(-z))
    else:
        e = math.exp(z)
        s = e / (1.0 + e)
    return s * (1 - s)


for z in (0.0, 10.0, -10.0, -800.0):
    try:
        naive = d_sigmoid_naive(z)
    except OverflowError:
        naive = float("nan")
    print(f"  z = {z:>7.1f}   naive = {naive!s:>12}   stable = {d_sigmoid(z):.12f}")
```

```text
  z =     0.0   naive =         0.25   stable = 0.250000000000
  z =    10.0   naive = 4.539580773595167e-05   stable = 0.000045395808
  z =   -10.0   naive = 4.539580773595167e-05   stable = 0.000045395808
  z =  -800.0   naive =          nan   stable = 0.000000000000
```

At `z = -800` the naive formula asks for `math.exp(800)`, which overflows, and the answer
is `nan`. The stable version returns a perfectly good `0.0` — sigmoid(-800) really is
indistinguishable from zero to double precision. The wrong version is tempting because it
is the direct transcription of the textbook formula. The right version costs two lines and
is what every production framework does.

**Mistake 4 — treating forward and central differences as interchangeable.**

```python
import math


def f(x):
    """f(x) = x^4.  f' = 4x^3 = 32 at x = 2."""
    return x ** 4


def forward(f_, x, h):
    return (f_(x + h) - f_(x)) / h


def central(f_, x, h):
    return (f_(x + h) - f_(x - h)) / (2 * h)


h = 1e-4
print(f"  forward at h=1e-4 : {forward(f, 2.0, h):.10f}  (true 32)")
print(f"  central at h=1e-4 : {central(f, 2.0, h):.10f}  (true 32)")
print(f"  forward err {abs(forward(f, 2.0, h) - 32):.3e}"
      f"   central err {abs(central(f, 2.0, h) - 32):.3e}")
print("  The ratio is about 2h: forward keeps a first-order term, central does not.")
```

```text
  forward at h=1e-4 : 32.0024000801  (true 32)
  central at h=1e-4 : 32.0000000800  (true 32)
  forward err 2.400e-03   central err 8.003e-08
```

The error ratio is `2.4e-3 / 8.0e-8`, about 30 000 to 1, in central's favour. For $f(x) = x^4$
the forward error is exactly $\frac{h}{2}f''(2) = \frac{10^{-4}}{2}\cdot 48 = 2.4\times10^{-3}$,
which matches the measured value to three digits — the error formula is not a heuristic.

**Mistake 5 — differentiating numerically when a closed form exists.**

```python
import math


def loss_of_sum(samples, w):
    """Mean squared error, as a function of one weight."""
    return sum((w * s - 2 * s) ** 2 for s in samples) / len(samples)


samples = [1.0, 2.0, 3.0, 4.0]
w = 1.5

# Analytic: d/dw [ (w*s - 2*s)^2 ] = 2 s (w s - 2 s), averaged.
analytic = sum(2 * s * (w * s - 2 * s) for s in samples) / len(samples)
h = 1e-6
numeric = (loss_of_sum(samples, w + h) - loss_of_sum(samples, w - h)) / (2 * h)
print(f"  analytic gradient = {analytic:.10f}")
print(f"  numeric gradient  = {numeric:.10f}")
print("  They agree, but the analytic one is exact and costs O(n) instead of O(2n)")
print("  forward passes, and it stays correct when the gradient is very small.")
```

```text
  analytic gradient = -7.5000000000
  numeric gradient  = -7.4999999990
```

The numeric answer is wrong in its eighth decimal place — a reminder that `h = 1e-6`
caps your accuracy at about $10^{-10}$, no matter how simple the function is. The numeric
version is tempting because it needs no derivation at all. That is a real virtue — and
`torch.autograd.gradcheck` uses it. But when you can write down the derivative, do: it is
exact, it is faster, and it does not lie to you when the gradient is `1e-20` and the
function values are all `1.0`.

---

## Multiple Choice Questions

**Q1.** At $h = 10^{-6}$ for $f(x) = \sin x$ at $x = 1$, the forward difference has error
`4.21e-07` while the central difference has error `2.77e-11`. What accounts for the
factor of roughly 15 000?

- A) The central difference evaluates the function on a larger effective interval
- B) The forward expansion leaves a term $\tfrac{h}{2}f''$; averaging the forward and backward half-steps cancels every odd-order error term, so central error falls like $h^2$ instead of $h$
- C) The central difference performs fewer floating-point operations, so it rounds less
- D) The central difference is exact for every polynomial of degree at most 3

<details>
<summary>Answer and explanation</summary>

**B) The forward expansion leaves a term $\tfrac{h}{2}f''$; averaging the forward and
backward half-steps cancels every odd-order error term, so central error falls like $h^2$
instead of $h$.**

Substitute $h = 10^{-6}$. Forward gives $\frac{h}{2}f'' = 5\times10^{-7}\times(-0.8415)
= -4.21\times10^{-7}$, which is exactly the code's predicted line and its measured
`4.207e-07`. Central gives $\frac{h^2}{6}f''' = \frac{10^{-12}}{6}\times(-0.5403) =
-9.0\times10^{-14}$. The truncation ratio is $\frac{h}{12}\approx 8.3\times10^{-8}$, a
factor of about five million; roundoff lifts the central figure to the measured
`2.77e-11`. The lesson's "factor of about 15 000" is the ratio of the two *total* errors,
which is the honest number to quote.

Option A is a category error: the central difference's samples sit $\pm h$ from $a$, the
same reach as one forward sample, and the divisor $2h$ halves the quotient to match.
Option C is backwards — central uses three function values against forward's two, so it
does strictly more arithmetic. Option D confuses the central difference with Simpson's
rule: central is exact where $f''' = 0$, which includes quadratics but not cubics. For
$\sin x$ at 1, $f''' = -\cos 1 \ne 0$.

</details>

**Q2.** At $h = 10^{-10}$ the table shows an error of `5.85e-08` for *both* the forward
and the central difference, worse than at $h = 10^{-8}$. Why does shrinking $h$ make the
estimate worse?

- A) Because $\sin x$ has no derivative at $x = 1$
- B) Because roundoff now dominates: $f(x+h)$ and $f(x)$ are nearly equal doubles, so the subtraction loses about $\log_{10}(1/h)$ significant digits and the error grows like $\varepsilon/h$
- C) Because $10^{-10}$ cannot be represented as a double
- D) Because `math.sin` overflows for small arguments

<details>
<summary>Answer and explanation</summary>

**B) Because roundoff now dominates: $f(x+h)$ and $f(x)$ are nearly equal doubles, so the
subtraction loses about $\log_{10}(1/h)$ significant digits and the error grows like
$\varepsilon/h$.**

This is the right-hand arm of the U-curve in the printed table. Truncation falls as $h$;
roundoff rises as $\varepsilon/h$; they cross near $h \approx \sqrt\varepsilon \approx
1.49\times10^{-8}$, which is the printed value and precisely where the two columns become
nearly the same number (`2.97e-09` forward, `2.58e-09` central at $h = 10^{-8}$). Past
that point every extra decimal place of $h$ buys about one more digit of noise, and by
$h = 10^{-12}$ the central estimate has degraded to `1.23e-05`.

Option A is nonsense: $\cos 1 = 0.5403$ exists. Option C is false — $10^{-10}$ is exactly
representable; what is lost is the *difference* of two representable numbers. Option D
confuses the step size with the argument scale. $\sin$ is accurate near 0; the problem is
that $\sin(1 + 10^{-10})$ and $\sin 1$ round to nearly the same double, so their
difference is mostly noise.

</details>

**Q3.** You want the most accurate floating-point derivative of $\sin x$ at $x = 1$ by
finite differences. Which step size should you reach for?

- A) $h = 10^{-16}$, because it is closest to the true limit $h \to 0$
- B) $h = 10^{-6}$, where truncation is still falling steadily and roundoff has not yet taken over
- C) $h = 10^{-1}$, because a large step is cheapest to evaluate
- D) $h = 10^{-12}$, because central differences have $O(h^2)$ error, so smaller $h$ must be better

<details>
<summary>Answer and explanation</summary>

**B) $h = 10^{-6}$, where truncation is still falling steadily and roundoff has not yet
taken over.**

The table reads: central error `9.00e-04` at $10^{-2}$, `9.00e-10` at $10^{-4}$,
`2.77e-11` at $10^{-6}$, then `2.58e-09` at $10^{-8}$ and `1.23e-05` at $10^{-12}$. There
is a genuine minimum around $10^{-6}$–$10^{-7}$, not at $h\to0$.

Option A is Common Mistake 1 in a nutshell: "smaller is closer to the limit" is exactly
the reasoning that fails, because $h$ is not a mathematical quantity here — it is a sample
spacing, and the machine has a resolution. Option C maximises truncation error; it is
what you pick if you have confused "few evaluations" with "accurate". Option D is the
sharpest trap, because the reasoning $O(h^2) \Rightarrow$ smaller is better is *correct in
exact arithmetic* and wrong in floating point: $O(h^2)$ applies only while $h^2 \gg
\varepsilon/h$, i.e. $h^3 \gg \varepsilon$.

</details>

**Q4.** Why does backpropagation need two passes over the network regardless of how many
parameters there are, while a central-difference check needs $n+1$ forward passes?

- A) Because the chain rule only holds for a single scalar parameter
- B) Because reverse mode reuses one cached forward pass for every parameter, while each central difference needs its own perturbed forward evaluation
- C) Because gradient tensors are sparse and can be compressed to a constant
- D) Because in practice $n$ is always small

<details>
<summary>Answer and explanation</summary>

**B) Because reverse mode reuses one cached forward pass for every parameter, while
each central difference needs its own perturbed forward evaluation.**

The lesson's numbers: with `n_params = 4`, backprop costs `2` passes (forward plus
backward) and central differences cost `5`. One forward pass stores $a$, $h$, and
`out`; one backward pass walks that cache, multiplying one local slope per edge. Each of
the $n$ central differences instead re-runs the whole forward computation with one
parameter perturbed, because changing $w_i$ changes every downstream intermediate. So the
ratio is linear in $n$: at ResNet-50's ~25 million parameters the naive check would be 25
million forward passes, which is why `torch.autograd` exists and `gradcheck` is a *test*
rather than a method.

Option A is backwards — the chain rule's product form is precisely what makes one
backward pass sufficient, and it composes over as many layers as you like. Option C
invents a mechanism: gradient tensors are dense. Option D is contradicted by the lesson's
own arithmetic.

</details>

**Q5.** In the backward pass, `d_a = d_h * (1 - h * h)`. If you delete the factor
`(1 - h * h)`, what breaks?

- A) Nothing much; it is a floating-point correction factor
- B) The chain rule factor for the `tanh` layer is missing, so you are asserting $\mathrm{d}h/\mathrm{d}a = 1$ instead of $\operatorname{sech}^2 a = 1 - \tanh^2 a$, and every gradient downstream of that layer is wrong
- C) You lose the second derivative of `tanh`
- D) The gradient becomes unbounded

<details>
<summary>Answer and explanation</summary>

**B) The chain rule factor for the `tanh` layer is missing, so you are asserting
$\mathrm{d}h/\mathrm{d}a = 1$ instead of $\operatorname{sech}^2 a = 1 - \tanh^2 a$, and
every gradient downstream of that layer is wrong.**

With the lesson's values, $a = 1.1$, $h = \tanh(1.1) = 0.800499$, so $1 - h^2 =
0.359200$. The printed $\mathrm{d}\text{out}/\mathrm{d}w_1 = -1.077604$ comes from
$(-1.5)(0.359200)(2.0)$. Drop the factor and you get $-3.0$ — wrong by a factor of about
2.8, with no error message, and the central-difference check at `h_step = 1e-6` would
print `agree = False`.

Option A is the instinct that produces "mysterious numerical bugs": a term you cannot
justify but that keeps the loss decreasing for a while. Option C confuses the layer's
*first* derivative with its second; $\tanh''$ is $-2\tanh\cdot\operatorname{sech}^2$.
Option D is not what happens — you get a finite wrong number, which is worse precisely
because it does not look broken.

</details>

**Q6.** Consider $f(x) = x^2\sin(1/x)$ for $x \ne 0$ and $f(0) = 0$. Since
$f'(0) = \lim_{h\to0} h\sin(1/h) = 0$ exists, $f$ is differentiable everywhere — yet $f'$
is not continuous at $0$. Why is that not a contradiction?

- A) It *is* a contradiction, so $\lim_{h\to0}h\sin(1/h)$ cannot be $0$
- B) Differentiability at a point constrains $f$ only at that point. Continuity of $f'$ at $0$ additionally needs $\lim_{x\to0}f'(x) = f'(0)$, and $f'(x) = 2x\sin(1/x) - \cos(1/x)$ swings between about $-1$ and $+1$ instead of approaching $0$
- C) $f'$ is continuous but not differentiable at $0$
- D) The chain rule fails at $0$

<details>
<summary>Answer and explanation</summary>

**B) Differentiability at a point constrains $f$ only at that point. Continuity of $f'$
at $0$ additionally needs $\lim_{x\to0}f'(x) = f'(0)$, and $f'(x) = 2x\sin(1/x) -
\cos(1/x)$ swings between about $-1$ and $+1$ instead of approaching $0$.**

The two conditions are genuinely different. Differentiability says "the secant slope from
$a$ to nearby points has a limit"; continuity of the derivative says "the slopes at
*nearby points* have a limit equal to the slope at $a$". The first averages the
oscillation over an interval, the second samples it at a point. The $x^2$ factor is what
makes $x^2 \times(\text{oscillation}) \to 0$ while the oscillation itself does not.

Option A denies a true fact: $\lvert h\sin(1/h)\rvert \le \lvert h\rvert \to 0$ by the
squeeze theorem, so the limit really is $0$. Option C confuses the roles — it is $f$
that is continuous everywhere and $f'$ that is discontinuous at $0$. Option D is
irrelevant; there is no composition to differentiate and $f'$ exists everywhere.

The computer-science consequence: a bound like $\lvert f'\rvert \le L$ (the Lipschitz
hypothesis behind gradient-descent rates) is a *stronger* assumption than
differentiability. If you rely on it you must verify it, and code that produces gradients
without knowing that $f$ is smooth cannot assume it.

</details>

**Q7.** In the two-circle Newton solve of Block 4, the residuals read
`+7.66e-01`, `+1.50e-02`, `+6.24e-06`, `+1.08e-12`, then `+0.00e+00`. What does that
last extra step tell you?

- A) Newton's method needed a fifth step to converge and only just made it
- B) Nothing; the residual printed as zero is simply the exact answer found sooner
- C) Once the Newton step $-F/J$ falls below roughly $\varepsilon\lvert x\rvert$, adding it to $x$ returns $x$ unchanged — the iteration has stopped moving because the machine cannot represent the improvement, not because the mathematics said stop
- D) The Jacobian became singular at the solution

<details>
<summary>Answer and explanation</summary>

**C) Once the Newton step $-F/J$ falls below roughly $\varepsilon\lvert x\rvert$, adding
it to $x$ returns $x$ unchanged — the iteration has stopped moving because the machine
cannot represent the improvement, not because the mathematics said stop.**

At step 4 the iterate is already the solution to double precision: the residual
`1.08e-12` is roundoff accumulated through the linear solve, not a mathematical error.
The true step there is of order $10^{-16}$, and the nearest double to $4.0$ is
$2.22\times10^{-16}$ away, so $x + \Delta x$ rounds straight back to $x$.

Option A misreads the output: step 4 *is* convergence to machine precision, and the extra
step is not progress. Option B is a plausible-sounding rationalisation that inverts the
diagnosis — the answer was found at step 4, not step 5, and step 5 prints zero because of
stagnation. Option D is false: $\det J = (2x)(2y) - (2y)(2(x-4)) = 8y$, and at $(4,3)$
that is $24 \ne 0$, so the Jacobian is as invertible as it ever was.

This is why production solvers carry both a tolerance and a maximum iteration count: the
mathematical stopping condition and the machine's stopping condition are not the same
event.

</details>

**Q8.** Gradient descent uses $x \leftarrow x - \eta f'(x)$. You choose $\eta$ very small
"to be safe". What actually happens, and why does a tiny step stall instead of
guaranteeing progress?

- A) It converges faster, because smaller steps cannot overshoot the minimum
- B) It converges more slowly but never stalls — a smaller step is always safer
- C) It stalls: eventually $\eta\lvert f'(x)\rvert$ drops below the gap between neighbouring doubles near $x$, so $x - \eta f'(x)$ evaluates to exactly $x$ and the loop stops moving while still far from the optimum
- D) It oscillates, because a small step systematically overshoots

<details>
<summary>Answer and explanation</summary>

**C) It stalls: eventually $\eta\lvert f'(x)\rvert$ drops below the gap between
neighbouring doubles near $x$, so $x - \eta f'(x)$ evaluates to exactly $x$ and the loop
stops moving while still far from the optimum.**

With $F(x) = (x^2-2)^2$ started at $x = 1$, $F'(1) = -4$. At $\eta = 10^{-17}$ the update
is $\eta F' = -4\times10^{-17}$, while the gap between doubles near $1.0$ is
$2.22\times10^{-16}$. The subtraction is performed, and the result is $1.0$ again — the
iteration is frozen at its starting point from the very first step, with no exception and
no warning. Only a *ratio* matters: the update survives when $\eta\lvert f'\rvert /
\lvert x\rvert$ exceeds $\varepsilon$, not when $\eta$ alone is small.

Option A is the intuition behind the failure — "small steps are safe" confuses stability
with progress. Option B is the same belief stated more confidently, and it is the belief
that produces an optimiser which trains for hours and reports a loss that stopped moving
long before it stopped improving. Option D reverses the mechanism: oscillation comes from
steps that are too *large*, as at $\eta = 0.25$ where the iterate cycles
$1 \to 2 \to -2 \to 2 \to -2$.

The practical fix is what L-BFGS and Adam do: scale the step by a quantity related to
curvature or gradient magnitude rather than by a fixed constant, so the update stays
representable across many orders of magnitude.

</details>

**Q9.** Why is the "stable" sigmoid derivative `s * (1 - s)` safe where the textbook
form `exp(-z)/(1 + exp(-z))**2` overflows?

- A) Because it performs fewer multiplications
- B) Because the two are algebraically identical, but the textbook form requires `exp(-z)` as a separate quantity, which overflows for large negative $z$, while $s$ itself always stays in $[0,1)$
- C) Because exponentiation is inherently inaccurate in IEEE-754
- D) Because the two formulas are derivatives of different functions

<details>
<summary>Answer and explanation</summary>

**B) Because the two are algebraically identical, but the textbook form requires
`exp(-z)` as a separate quantity, which overflows for large negative $z$, while $s$
itself always stays in $[0,1)$.**

Substituting $s = \frac{e^{-z}}{1+e^{-z}}$ gives $\frac{e^{-z}(1+e^{-z}) - e^{-z}e^{-z}}
{(1+e^{-z})^2} = \frac{e^{-z}}{(1+e^{-z})^2} = s(1-s)$, so the two agree exactly in
exact arithmetic. But `math.exp(-z)` overflows for very negative $z$, and the code's
`d_sigmoid_naive` catches the `OverflowError` and records `nan`. The stable version
computes $s$ as `1/(1+exp(-z))` for $z \ge 0$ and `exp(z)/(1+exp(z))` for $z < 0$ — the
argument handed to `exp` is always $\le 0$, so no overflow — and then multiplies. At
$z = -800$ it returns a value indistinguishable from `0.0` instead of `nan`, which is
the correct limit.

Option A is a performance detail, not a correctness one; saving a multiply does not stop
an overflow. Option C misdiagnoses the cause: `math.exp` is accurate over its range; the
problem is that $-z = 800$ is outside it. Option D is false — both differentiate the
same function, which is exactly the point.

</details>

**Q10.** The quotient rule gives `17.2234738303` for
$\mathrm{d}/\mathrm{d}x\,(x^3/\sin x)$ at $x = 2$; the central difference gives
`17.2234738312`. Why do the last digits differ?

- A) One of the two is wrong
- B) The central difference at $h = 10^{-6}$ still carries a truncation error of order $h^2 \approx 10^{-12}$, and the code prints 10 decimal places, so a disagreement in the 10th–11th digit is expected by design
- C) Python floats carry only about 8 correct digits
- D) The quotient rule is invalid wherever $\sin x$ is nonzero

<details>
<summary>Answer and explanation</summary>

**B) The central difference at $h = 10^{-6}$ still carries a truncation error of order
$h^2 \approx 10^{-12}$, and the code prints 10 decimal places, so a disagreement in the
10th–11th digit is expected by design.**

The printed agreement "to 10 places" is the *point* of the exercise, not a defect: the
analytic value is exact and the numeric one is an estimate, and the two are supposed to
match to roughly $h^2$. Compare the higher-derivative table, where the same $h = 10^{-5}$
is used four times over and the third derivative is already `2.75e-03` off — the error
compounds with every differentiation.

Option A is not something these two numbers can tell you, but the quotient rule is
confirmed by hand: $f'g - fg'$ with $f = x^3$, $f' = 3x^2$, $g = \sin x$, $g' = \cos x$
gives $\frac{3x^2\sin x - x^3\cos x}{\sin^2 x} = \frac{12(0.9093) + 8(0.4161)}{0.8268} =
\frac{14.240}{0.8268} = 17.2235$. Option C is wrong by three orders of magnitude; a
double has 15–17 significant digits, which is why the code prints 10. Option D inverts a
restriction: the quotient rule requires $g \ne 0$, and $\sin 2 \ne 0$.

</details>

**Q11.** What does Fermat's theorem say, and what mistake do people make in applying it?

- A) A differentiable function with a local maximum has $f' = 0$; equivalently $f'(a) = 0$ implies a local maximum
- B) A differentiable function with a local extremum at an interior point has $f'(a) = 0$; the converse fails, so $f'(a) = 0$ marks a *candidate*, not a guaranteed extremum
- C) Every differentiable function has a critical point in every open interval
- D) A critical point must be a point where $f'$ is undefined

<details>
<summary>Answer and explanation</summary>

**B) A differentiable function with a local extremum at an interior point has
$f'(a) = 0$; the converse fails, so $f'(a) = 0$ marks a *candidate*, not a guaranteed
extremum.**

Counterexample to the converse: $f(x) = x^3$ has $f'(0) = 0$, yet it is strictly
increasing everywhere, so $0$ is not an extremum. That is exactly why the lesson widens
the definition to *critical point* — "any $a$ with $f'(a) = 0$, **or** where $f'$ does
not exist" — because the corner at $x = 0$ in $|x|$ is a genuine extremum that the
condition $f' = 0$ would miss entirely.

Option A asserts the false converse; it is the standard slip. Option C is far too strong:
a strictly increasing function need not have *any* point where $f'$ vanishes. Option D
confuses the two halves of the definition — points where $f'$ is undefined are part of
the critical-point set, not the whole of it.

The code's `behaviour = "rising" if d > 1e-12 else ...` is the practical form: the
automated search looks for *sign changes* of $f'$, a strictly stronger condition than
$f' = 0$.

</details>

**Q12.** Why is $x = 0$ included in the definition of a critical point even though $f'(0)$
does not exist for $f(x) = |x|$?

- A) Because $|x|$'s derivative equals $1$ at $0$
- B) Because a corner is exactly where an extremum can hide without $f'$ existing, so excluding such points would make any turning-point search incomplete
- C) Because $|x|$'s derivative equals $0$ at $0$
- D) Because $|x|$ is not continuous at $0$

<details>
<summary>Answer and explanation</summary>

**B) Because a corner is exactly where an extremum can hide without $f'$ existing, so
excluding such points would make any turning-point search incomplete.**

$|x|$ has a strict minimum at $0$ and no derivative there. Fermat's theorem says nothing
— it requires $f'(0)$ to *exist* in order to conclude $f'(0) = 0$. So a search that
looked only for zeroes of $f'$ would skip the minimum entirely. Including both cases in
"critical point" is what makes Newton, gradient descent, and polygon-clipping code
complete: you must visit every point that *could* be a turn.

Option A and C are both arithmetically wrong: the one-sided derivatives at $0$ are $-1$
and $+1$. Option D confuses the facts — $|x|$ is continuous everywhere; the
discontinuity is in $f'$, not in $f$.

</details>

**Q13.** The measured central-difference errors are `9.00e-04` at $h = 10^{-2}$ and
`9.00e-10` at $h = 10^{-4}$. What does this establish about the rate, and what does it
*not* establish?

- A) The error is $\Theta(h^2)$ on this range: each $100\times$ increase in $h$ multiplies the error by $10^4$, so error$/h^2$ is a fixed positive constant. It does not establish the behaviour for very small $h$, where that constant stops holding
- B) The error is $o(h^2)$, because the error divided by $h^2$ tends to $0$
- C) The error is $\Theta(h^3)$, because $10^4 = (10^2)^2$ can be read as a cube of the step factor
- D) The error is $\Theta(h)$, because the same two samples are equally consistent with a linear rate

<details>
<summary>Answer and explanation</summary>

**A) The error is $\Theta(h^2)$ on this range: each $100\times$ increase in $h$
multiplies the error by $10^4$, so error$/h^2$ is a fixed positive constant. It does not
establish the behaviour for very small $h$, where that constant stops holding.**

$\Theta$ is the right-strength claim: a positive constant times $h^2$ bounds the error
above and below, and the data show error$/h^2 = 9.005\times10^{-2}$ at both $10^{-2}$ and
$10^{-4}$ — matching the predicted $\lvert f'''(1)\rvert/6 = \lvert\cos 1\rvert/6 =
0.0901$. $O(h^2)$ alone would be satisfied by anything that decays at least that fast,
including $h^3$ and $o(h^2)$, so the constant-ratio evidence is what upgrades it to
$\Theta$.

Option B is precisely the distinction the data rule out: the ratio is $9.005\times10^{-2}$,
not a sequence heading to zero. Option C cannot be — $h^3$ would predict a $10^6$ increase
in error for a $100\times$ increase in $h$. Option D misparses the exponent: the growth
factor is the *square* of the step factor, which is exactly what identifies $h^2$.

The clause about small $h$ matters. The same table shows the error blowing up at
$h = 10^{-12}$ (`1.23e-05`), so $\Theta(h^2)$ holds only where truncation dominates
roundoff — roughly $h^3 \gg \varepsilon$.

</details>

---

## Subjective Questions

### Short Answer

**Q1. State the definition of $f'(a)$, and say what must be true of $f$ near $a$.**

<details>
<summary>Model answer</summary>

$f$ is differentiable at $a$ if

$$f'(a) = \lim_{h\to0}\frac{f(a+h)-f(a)}{h}$$

exists. The requirement is that $f$ be defined on a whole neighbourhood of $a$, so the
quotient is meaningful for all sufficiently small $h \ne 0$; $f'(a)$ is a limit of
*differences*, so a single evaluation of $f(a)$ is never enough. Formally only the
punctured neighbourhood is required, though in practice one also assumes $f(a)$ exists.

</details>

**Q2. Write the error expansions for the forward and central differences, and state the
order of each error.**

<details>
<summary>Model answer</summary>

Expanding $f(a+h) = f(a) + h f'(a) + \frac{h^2}{2}f''(a) + O(h^3)$ and dividing by $h$:

$$\frac{f(a+h)-f(a)}{h} = f'(a) + \frac{h}{2}f''(a) + O(h^2)\qquad\text{error } \Theta(h).$$

Adding the expansions at $a+h$ and $a-h$ cancels every even-order term, leaving
$f(a+h)-f(a-h) = 2h f'(a) + \frac{h^3}{3}f'''(a) + O(h^5)$, so

$$\frac{f(a+h)-f(a-h)}{2h} = f'(a) + \frac{h^2}{6}f'''(a) + O(h^4)\qquad\text{error } \Theta(h^2).$$

</details>

**Q3. Why does the central difference gain exactly one order of accuracy, and what does
that cost?**

<details>
<summary>Model answer</summary>

The forward expansion carries an $h f''/2$ term; the backward one carries $-h f''/2$.
Averaging them — which is exactly what dividing the symmetric difference by $2h$ does —
cancels that term and with it every other odd-order error term. What survives starts at
$h^2$, so the order improves from $\Theta(h)$ to $\Theta(h^2)$.

The cost is one extra function evaluation per derivative, and with it one extra chance to
accumulate roundoff. Across $n$ parameters that is $n+1$ forward passes for a
central-difference gradient check against `2` for backprop — the `4` parameters → `5`
versus `2` comparison in the lesson.

</details>

**Q4. Write the backward-pass gradients for $a = w_1x+b_1$, $h = \tanh a$,
$\mathrm{out} = w_2h+b_2$, in terms of the seed derivative $d_{\mathrm{out}}$.**

<details>
<summary>Model answer</summary>

Start from $\mathrm{d}\text{out}/\mathrm{d}\,\text{out} = 1$ and apply the chain rule
backwards, one local slope per layer:

$$d_{w_2} = d_{\mathrm{out}}\,h,\qquad d_{b_2} = d_{\mathrm{out}},\qquad
d_h = d_{\mathrm{out}}\,w_2,$$
$$d_a = d_h\,(1-h^2),\qquad d_{w_1} = d_a\,x,\qquad d_{b_1} = d_a.$$

At the lesson's values $x=2$, $w_2=-1.5$, $h=0.800499$: $d_h = -1.5$,
$d_a = -1.5\times(1-0.640799) = -0.538802$, $d_{w_1} = -1.077604$, $d_{w_2}=0.800499$,
$d_{b_2} = 1$. Each line is one multiplication, and no expression is ever rewritten.

</details>

**Q5. State Fermat's theorem and define a critical point. Why is the definition wider
than Fermat's condition?**

<details>
<summary>Model answer</summary>

**Fermat.** If $f$ has a local maximum or minimum at an interior point $a$ and $f'(a)$
exists, then $f'(a) = 0$.

A **critical point** is any $a$ with $f'(a) = 0$ *or* where $f'$ does not exist; the first
case alone is a **stationary point**. The definition is wider in both directions because
the converse of Fermat fails ($x^3$ has $f'(0) = 0$ and no extremum) and because Fermat's
hypothesis is unavailable at corners: $|x|$ has a strict minimum at $0$ where $f'$ does
not exist, so a search restricted to $f' = 0$ would miss it.

</details>

**Q6. State the Lipschitz condition, and explain why a bounded derivative implies it.**

<details>
<summary>Model answer</summary>

$f$ is **Lipschitz continuous** with constant $L$ if $\lvert f(x)-f(y)\rvert \le
L\lvert x-y\rvert$ for all $x, y$ — it never changes faster than $L$ per unit of input.

If $\lvert f'\rvert \le L$ everywhere and $f$ is differentiable between $x$ and $y$, the
mean value theorem gives a point $c$ with $\frac{f(x)-f(y)}{x-y} = f'(c)$, so
$\lvert f(x)-f(y)\rvert = \lvert f'(c)\rvert\lvert x-y\rvert \le L\lvert x-y\rvert$. This
is the standard hypothesis behind gradient-descent rates and importance sampling, and
hence behind the $\sigma/\sqrt{n}$ Monte Carlo error bound.

</details>

### Long Answer

**Q1. Why does making the step size smaller eventually make a numerical derivative
*worse*, and what sets the turning point?**

<details>
<summary>Model answer</summary>

There are two independent errors and they pull in opposite directions.

**Truncation** is the mathematical price of not taking the limit. Expanding to second
order and dividing by $h$ gives a forward-difference error of $\frac{h}{2}f''$ — it falls
linearly in $h$, as the table's first four rows confirm (`4.29e-02`, `4.22e-03`,
`4.21e-05`, `4.21e-07` for $h$ from $10^{-1}$ down to $10^{-6}$). Central differences pay
$\frac{h^2}{6}f'''$ instead.

**Roundoff** is the price of using floats. If $f(x+h)$ and $f(x)$ are both about $1$ and
differ by only $h$, each carries a representation error of order $\varepsilon$, so the
difference carries a *relative* error of order $\varepsilon/h$. With
$\varepsilon \approx 2.22\times10^{-16}$, at $h = 10^{-12}$ the quotient is noise with a
relative error of order $10^{-4}$ — precisely the `4.32e-05` the table prints for the
forward difference and `1.23e-05` for the central one.

So the total error is $\sim \frac{h}{2}|f''| + \varepsilon|f|/h$ for forward differences.
Differentiating gives $\frac{1}{2}|f''| - \varepsilon|f|/h^2 = 0$, hence
$h^\star \sim (2\varepsilon)^{1/3} \approx 7.6\times10^{-6}$ and a best accuracy of order
$\varepsilon^{1/3} \approx 6\times10^{-6}$. For central differences the same calculation
gives $h^\star \sim (3\varepsilon)^{1/3} \approx 8.7\times10^{-6}$ and, crucially, a best
accuracy of order $\varepsilon^{2/3} \approx 3.7\times10^{-11}$ — which is why the best
central figure in the table, `2.77e-11`, sits so close to $\varepsilon^{2/3}$ while the
best forward figure is around $10^{-6}$.

The two error curves cross near $h \approx \sqrt{\varepsilon} \approx 1.49\times10^{-8}$,
which is the printed value, and it is exactly where the table's columns converge
(`2.97e-09` and `2.58e-09` at $h = 10^{-8}$). That is a *different* quantity from either
method's own optimum, and conflating the two is the usual source of confusion. Past the
crossover, no extra decimal place of $h$ buys anything.

The engineering consequence is blunt: $h$ is a numerical design parameter, not a
mathematical one, and the correct choice is a fixed multiple of $\varepsilon^{1/3}$ tuned
to the function's scale — which is why serious libraries do not use finite differences at
all when they can avoid them.

</details>

**Q2. Why is the chain rule what makes backpropagation feasible, and what specifically
breaks if you try to get the same gradients by finite differences instead?**

<details>
<summary>Model answer</summary>

Consider a composition $f = f_L \circ \cdots \circ f_1$ with $n$ parameters. The chain
rule factors the total derivative into local ones, $(f \circ g)' = f'(g)\,g'$, so the
gradient with respect to a parameter deep in the network is a *product* of one local
slope per layer. Reverse-mode autodiff exploits this by making a single forward pass that
caches every intermediate, then a single backward pass that multiplies one cached slope
per edge. Two passes, total, for any depth and any parameter count.

Finite differences ignore the factorisation. To estimate $\partial\text{out}/\partial w_i$
you must evaluate `out` at $w_i + h$ and at $w_i - h$, and *each* evaluation recomputes
every intermediate, because changing $w_i$ changes everything downstream. So the cost is
$n+1$ forward passes. The lesson's numbers make this concrete: with 4 parameters, backprop
costs `2` and central differences cost `5`. At ResNet-50's ~25 million parameters the naive
check is 25 million forward passes.

What breaks is not accuracy — central differences are *more* accurate than nothing, and
that is precisely why `torch.autograd.gradcheck` exists — but three other things:

1. **Cost.** Linear in $n$, where backprop is linear in depth instead. For a modern model
   the check is not "expensive", it is impossible.
2. **Sensitivity to the step.** Each estimate carries truncation $\Theta(h^2)$ *and*
   roundoff $\Theta(\varepsilon/h)$; the forward pass adds its own. Block 4 shows what
   repeated differentiation does: the third derivative is `2.75e-03` off and the fourth is
   off by a factor of 186.
3. **Failure modes that hide.** When a gradient is genuinely `1e-20` and the loss values
   are all `1.0`, the finite-difference estimate is dominated by noise and will report a
   plausible-looking gradient that points the wrong way. An analytic gradient reports
   `1e-20` honestly.

Backprop therefore is not an optimisation of the chain rule; it is the only practical way
to get exact derivatives of a deep composition at a cost independent of the parameter
count. Once you see that the "`5` passes versus `2` passes" is the whole argument,
`loss.backward()` stops being magic.

</details>

**Q3. Why can a differentiable function have a discontinuous derivative, and what breaks
if a numerical method assumes the reverse?**

<details>
<summary>Model answer</summary>

Differentiability and continuity of the derivative are different claims, and the
difference is which points get sampled.

$f'(a)$ existing means the *secant slope from $a$* has a limit:
$\lim_{h\to0}\frac{f(a+h)-f(a)}{h}$. Continuity of $f'$ at $a$ means the *slopes at
points near $a$* converge to $f'(a)$: $\lim_{x\to a} f'(x) = f'(a)$. The first averages
over an interval; the second samples at a point. Take $f(x) = x^2\sin(1/x)$ with $f(0)=0$:
$\frac{f(h)-f(0)}{h} = h\sin(1/h) \to 0$ by the squeeze theorem, so $f'(0) = 0$, while
$f'(x) = 2x\sin(1/x) - \cos(1/x)$ oscillates between about $-1$ and $+1$ and never
converges. Both facts hold; nothing is contradictory.

What breaks if you assume $f'$ is continuous is every method whose guarantee rests on a
*uniform* bound. Three concrete examples from this lesson:

- **Mean value theorem arguments.** Getting $\lvert f(x)-f(y)\rvert \le L\lvert x-y\rvert$
  from $\lvert f'\rvert \le L$ needs the MVT, which needs continuity on the interval. A
  merely differentiable function with a jumpy derivative can exceed any Lipschitz
  constant in a way your error bound never saw coming.
- **Truncation estimates.** The formulas $\frac{h}{2}f''$ and $\frac{h^2}{6}f'''$ are
  *pointwise* Taylor remainders. Claiming a uniform $O(h)$ or $O(h^2)$ bound over an
  interval silently requires those derivatives to be bounded there.
- **Second-order methods.** Newton's error estimate $\frac{1}{2}f''h^2$ and the L-BFGS
  curvature model both assume curvature exists and is locally stable. With a discontinuous
  derivative the tangent can change direction arbitrarily close to the current point, and
  the method takes a full step in a direction that was never meaningful.

So "differentiable" is exactly the assumption code can often verify — it needs the
function at one point plus a limit — while "smooth derivative" is a stronger global
property that code generally cannot check. When you read a convergence proof that assumes
a Lipschitz or continuously differentiable loss, that assumption is doing real work, and it
is the first thing to check when the method misbehaves on real data.

</details>

**Q4. Why does a small learning rate stall rather than guarantee progress, and how do
real optimisers avoid it?**

<details>
<summary>Model answer</summary>

Gradient descent computes $x \leftarrow x - \eta f'(x)$. The subtraction happens in
floating point, so it has an effect only if the update is large enough to move $x$ to a
*different representable double*. Near $x = 1$ that spacing is $2.22\times10^{-16}$. Take
$F(x) = (x^2-2)^2$ from $x_0 = 1$: $F'(1) = -4$, so with $\eta = 10^{-17}$ the update is
$-4\times10^{-17}$, the result rounds straight back to $1.0$, and the iterate is frozen at
its starting value from the first step. The mathematically correct update is computed and
then discarded.

The crucial point is that only a *ratio* matters: the update survives when
$\eta\lvert f'(x)\rvert \gtrsim \varepsilon\lvert x\rvert$. So there are two ways to stall
— shrink $\eta$ while $f'$ is small, or run in a region where $f'$ is small relative to
$x$. Plain gradient descent on a badly scaled loss stalls in the second regime even with a
reasonable $\eta$, which is why one learning rate cannot serve a network whose gradient
magnitudes span many orders of magnitude across layers.

Real optimisers break the dependence on a fixed $\eta$ in two ways. Adam and RMSProp
divide by a running estimate of the gradient's own magnitude, so the effective step is
roughly $\eta$ per *coordinate* regardless of scale — small-gradient coordinates still
move. L-BFGS and other quasi-Newton methods go further and *estimate curvature*, giving a
step that grows in flat directions and shrinks in steep ones, which is what produces
Newton's superlinear rate without needing Newton's second derivative. Both families are, in
the end, statements that a step size must be relative to the local geometry rather than
an absolute constant.

</details>

---

## Exercises and Solutions

**[ ] Exercise 1 — derivatives from the definition.** For $f(x) = \frac{1}{x}$:
(a) Use the difference quotient to show $f'(x) = -1/x^2$.
(b) What does your answer say about what the algorithm in lesson 50 does when $x = 0$?
(c) Compute the forward difference quotient at $x = 10$ with $h = 10^{-3}$ and with
$h = 10^{-9}$, and comment.

<details>
<summary>Solution</summary>

(a) $f(x+h) - f(x) = \frac{1}{x+h} - \frac1x = \frac{x - (x+h)}{x(x+h)} = \frac{-h}{x(x+h)}$.
Divide by $h$: $\frac{f(x+h)-f(x)}{h} = \frac{-1}{x(x+h)}$. As $h \to 0$ this tends to
$-\frac{1}{x \cdot x} = -\frac{1}{x^2}$. ✓

(b) At $x = 0$ the difference quotient is $\frac{-1}{0 \cdot h}$, undefined for every
$h$, so there is no limit and no derivative there. This is the concrete form of the
infinite discontinuity in exercise 3 of lesson 50: `1/x` has no finite limit at 0 in
either direction.

(c) With $x = 10$: $\frac{f(10+h) - f(10)}{h} = \frac{-1}{10(10+h)}$.
- $h = 10^{-3}$: $\frac{-1}{10 \cdot 10.001} = -0.00999900010$. True value
  $-1/100 = -0.01$. Error $\approx 10^{-6}$, matching the $h/2 \cdot f''$ prediction with
  $f''(x) = 2/x^3 = 0.002$.
- $h = 10^{-9}$: $\frac{-1}{10 \cdot 10.000000001} = -0.00999999999$. Error $\approx 10^{-10}$.
  Still improving, because $f$ is smooth here and no cancellation dominates.

```python
import math


def forward(f, x, h):
    return (f(x + h) - f(x)) / h


f = lambda t: 1.0 / t
for h in (1e-3, 1e-6, 1e-9, 1e-12):
    est = forward(f, 10.0, h)
    print(f"  h = {h:.0e}  estimate {est:.15f}  err {abs(est - (-0.01)):.2e}")
```

```text
  h = 1e-03  estimate -0.009999000099986  err 1.00e-06
  h = 1e-06  estimate -0.009999998995536  err 1.00e-09
  h = 1e-09  estimate -0.010000000827404  err 8.27e-10
  h = 1e-12  estimate -0.010005885009434  err 5.89e-06
```

The error falls roughly one order of magnitude for every one of $h$ until `h = 1e-9`,
then it turns around and gets dramatically worse: at `h = 1e-12` the error is
`5.89e-06`, worse than at `h = 1e-3`. This is the U-turn from block 1, reached sooner than
you would expect, because `1/x` near $x = 10$ involves a subtraction of two numbers near
`0.1` that are meant to differ by `h`.

</details>

**[ ] Exercise 2 — the chain rule, three layers deep.** Let
$y = \cos(3 \sin(2x))$.

(a) Write $y$ as a composition of four named functions.
(b) Compute $y'$ using the chain rule.
(c) Numerically verify $y'(0.5)$ with a central difference.
(d) Compute all four local derivatives numerically at $x = 0.5$ and check that their
product equals the answer to (c).

<details>
<summary>Solution</summary>

(a) The layers are: $u_1 = 2x$ (scale), $u_2 = \sin u_1$ (sin), $u_3 = 3u_2$ (scale),
$y = \cos u_3$ (cos).

(b) Local derivatives: $u_1' = 2$; $u_2' = \cos u_1$; $u_3' = 3$; $y' = -\sin u_3$.
Multiply: $y' = 2 \cdot \cos(2x) \cdot 3 \cdot (-\sin(3\sin 2x)) =
-6\cos(2x)\sin(3\sin 2x)$.

(c) At $x = 0.5$: $2x = 1$, $\sin 1 = 0.841471$, $3 \cdot 0.841471 = 2.524413$,
$\cos 1 = 0.540302$, $\sin 2.524413 = 0.578737$. So
$y' = -6(0.540302)(0.578737) = -1.87616$. The central difference confirms it.

```python
import math

f = lambda x: math.cos(3 * math.sin(2 * x))
x = 0.5
h = 1e-6
numeric = (f(x + h) - f(x - h)) / (2 * h)
analytic = -6 * math.cos(2 * x) * math.sin(3 * math.sin(2 * x))
print(f"  chain rule      = {analytic:.12f}")
print(f"  central diff    = {numeric:.12f}")
print(f"  agree           = {math.isclose(analytic, numeric, rel_tol=1e-7)}")

# the four local derivatives, multiplied
u1, u2, u3 = 2 * x, math.sin(2 * x), 3 * math.sin(2 * x)
parts = [2.0, math.cos(u1), 3.0, -math.sin(u3)]
print(f"  local slopes    = {[round(p, 6) for p in parts]}")
product = 1.0
for p in parts:
    product *= p
print(f"  their product   = {product:.12f}")
```

```text
  chain rule      = -1.876159139426
  central diff    = -1.876159139436
  agree           = True
  local slopes    = [2.0, 0.540302, 3.0, -0.578737]
  their product   = -1.876159139426
```

(d) The four local derivatives at $x = 0.5$ are $2$, $0.540302$, $3$, $-0.578737$. Their
product $-1.876159139426$ equals the analytic answer exactly. This is precisely the
structure of a backward pass: four layers, four multiplications, and the gradient falls out.

</details>

**[ ] Exercise 3 — implicit differentiation for a real constraint.** Consider
$x^2 + y^3 = 16$ near the point $(3, 2)$, which is not on the curve — instead find the
point near it. (a) Find $dy/dx$ as a function of $x$ and $y$ for the curve
$x^2 + y^3 = 16$. (b) Use Newton's method with that derivative to find the point on the
curve with $x = 2$, then report the slope there. (c) Show that the derivative blows up at
the point where $y = 0$ (that is, $x = 4$), and explain geometrically what that means.

<details>
<summary>Solution</summary>

(a) $F(x,y) = x^2 + y^3 - 16$. Differentiating: $2x + 3y^2 y' = 0$, so
$y' = -\frac{2x}{3y^2}$.

(b) With $x = 2$ fixed, solve $g(y) = 2^2 + y^3 - 16 = y^3 - 12 = 0$, so $y = \sqrt[3]{12}$.
Newton: $y_{k+1} = y_k - \frac{y_k^3 - 12}{3y_k^2}$.

```python
import math


def solve_y(y0, iters=6):
    y = y0
    for _ in range(iters):
        g = y ** 3 - 12.0
        gp = 3 * y ** 2
        y = y - g / gp
    return y


y = solve_y(2.0)
print(f"  y = {y:.12f}   check y^3 = {y ** 3:.12f}  (want 12)")
slope = -(2 * 2.0) / (3 * y ** 2)
print(f"  dy/dx = -2x/(3y^2) = {slope:.12f}")
```

```text
  y = 2.289428485107   check y^3 = 12.000000000000  (want 12)
  dy/dx = -2x/(3y^2) = -0.254380942790
```

So at $(2, 2.2894)$ the slope is about $-0.2544$. (Check the chain rule once: the chain is
$\frac{d}{dx}[x^2 + y^3] = 2x + 3y^2 y'$; at $x = 2$, $2x = 4$, $3y^2 = 15.72$, so
$y' = -4/15.72 = -0.2544$. The code's `-2 * 2.0 / (3 * y**2)` computes $-4/15.72$ —
the same number.)

(c) At $y = 0$ (i.e. $x = 4$) the denominator $3y^2$ is zero, so the formula is
undefined. Geometrically the curve $y = (16 - x^2)^{1/3}$ has a *vertical tangent* at
$x = 4$: as $y$ increases slightly, $x$ must change only in the third-order term, so
$\Delta x / \Delta y \to 0$ while $\Delta y / \Delta x \to \infty$. This is the
implicit-function-theorem condition failing: $F_y = 0$ means $y$ is not a smooth function
of $x$ there. If you plug $y = 0$ into the Python formula you get `ZeroDivisionError`, and
that exception is the mathematics telling you the slope is vertical, not infinite-but-finite.

</details>

**[ ] Exercise 4 — Challenge: build a forward-mode automatic differentiator.** Write a
tiny expression system where a value carries its derivative along with it. Each
arithmetic operator returns a new pair `(value, d value/d x)`, using the product and chain
rules. Then compute $f'(2)$ for $f(x) = \sin(x)\cos(x) + x^3 e^{x}$, for
$f(x) = \frac{x^4 + 1}{x^2 + 3}$, and for $f(x) = \log(1 + x^2)$ — all by writing $x$
once as `Var(2)` and then only using `+`, `*`, and the elementary wrappers. Finally
compare against central differences.

<details>
<summary>Solution</summary>

```python
import math


class Var:
    """A number that also knows its own derivative with respect to a seed input."""

    def __init__(self, value, grad=1.0):
        self.v = value
        self.d = grad          # d(value)/d(seed)

    # --- operators: each one applies a differentiation rule ---

    def __add__(self, other):
        o = _as(other)
        return Var(self.v + o.v, self.d + o.d)          # (f+g)' = f' + g'

    def __radd__(self, other):
        return self.__add__(other)

    def __neg__(self):
        return Var(-self.v, -self.d)

    def __sub__(self, other):
        return self + (-_as(other))

    def __rsub__(self, other):
        return _as(other) + (-self)

    def __mul__(self, other):
        o = _as(other)
        return Var(self.v * o.v, self.v * o.d + self.d * o.v)   # (fg)' = f'g + fg'

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        o = _as(other)
        return Var(self.v / o.v,
                   (self.d * o.v - self.v * o.d) / (o.v * o.v))  # quotient rule

    def __rtruediv__(self, other):
        return _as(other) / self

    def __pow__(self, n):
        return Var(self.v ** n, n * self.v ** (n - 1) * self.d)   # power rule

    def sin(self):
        return Var(math.sin(self.v), math.cos(self.v) * self.d)    # chain rule

    def cos(self):
        return Var(math.cos(self.v), -math.sin(self.v) * self.d)

    def exp(self):
        return Var(math.exp(self.v), math.exp(self.v) * self.d)

    def log(self):
        return Var(math.log(self.v), self.d / self.v)

    def __repr__(self):
        return f"Var(value={self.v:.10f}, grad={self.d:.10f})"


def _as(t):
    return t if isinstance(t, Var) else Var(t, 0.0)   # a constant: zero gradient


# --- the three expressions, written as composition only ---
x = Var(2.0)
f1 = x.sin() * x.cos() + (x ** 3) * x.exp()
f2 = (x ** 4 + 1) / (x ** 2 + 3)
f3 = (1 + x ** 2).log()

for name, expr, plain in (
    ("sin x cos x + x^3 e^x", f1, lambda t: math.sin(t) * math.cos(t) + t ** 3 * math.exp(t)),
    ("(x^4+1)/(x^2+3)", f2, lambda t: (t ** 4 + 1) / (t ** 2 + 3)),
    ("log(1+x^2)", f3, lambda t: math.log(1 + t ** 2)),
):
    h = 1e-6
    numeric = (plain(2.0 + h) - plain(2.0 - h)) / (2 * h)
    print(f"  {name:<22} value {expr.v:>14.10f}  grad {expr.d:>14.10f}"
          f"  numeric {numeric:>14.10f}  ok {math.isclose(expr.d, numeric, rel_tol=1e-7)}")
```

```text
  sin x cos x + x^3 e^x  value  58.7340475438  grad 147.1274783577  numeric 147.1274783640  ok True
  (x^4+1)/(x^2+3)        value   2.4285714286  grad   3.1836734694  numeric   3.1836734693  ok True
  log(1+x^2)             value   1.6094379124  grad   0.8000000000  numeric   0.8000000000  ok True
```

Notes on the design:

- `Var(3.0)` creates a constant whose derivative is zero. Without `_as`, the expression
  `x ** 4 + 1` would fail, and it would fail *silently* if `_as` returned a gradient of 1.
- This is **forward mode**: one propagation carries all partial derivatives at once. It
  costs one pass and is optimal when you want $\frac{d}{dx}$ for one variable.
- For $n$ inputs and one output, **reverse mode** (block 3) costs one forward and one
  backward pass regardless of $n$; forward mode costs $n$ passes. That is why autodiff
  frameworks default to reverse mode for neural networks, where $n$ is the number of
  parameters and the output is one scalar loss.
- You could differentiate this output again to get the second derivative, because every
  `Var` already carries a `d`. Differentiating numerically instead would give you the
  garbage shown in block 4.

</details>

**[ ] Exercise 5 — why the learning rate is a trap: divergence, limit cycles, and
stagnation.** Let $F(x) = (x^2-2)^2$ with $F'(x) = 4x(x^2-2)$, and run gradient descent
$x \leftarrow x - \eta F'(x)$ from $x_0 = 1$.

(a) Work out the stability condition on $\eta$ from $F''(1) = 12x^2-8$.
(b) For $\eta = 0.1$, $0.25$, $0.4$ and $0.9$, describe what happens in the first four
steps. Explain the $\eta = 0.25$ behaviour exactly, using $F(\pm2) = 4$ and
$F'(-2) = 8$.
(c) For $\eta = 10^{-17}$ show that the iterate never moves at all, and state the
condition on $\eta\lvert F'(x)\rvert$ in terms of the gap between neighbouring doubles
near $x = 1$.
(d) Contrast: run Newton's method $x \leftarrow x - F/F'$ from the same start, and then
Newton's method on $g(x) = x^2-2$ instead. Report the error after each step and identify
which of the two convergence rates you see, and why the two differ.

<details>
<summary>Solution</summary>

(a) Linearising the update about a critical point gives $x_{k+1} - x^\star \approx
(1 - \eta F''(x^\star))(x_k - x^\star)$, so the iteration contracts only while
$\lvert 1 - \eta F''(x^\star)\rvert < 1$. At $x = 1$, $F''(1) = 12 - 8 = 4$, so the
condition is $\lvert 1 - 4\eta\rvert < 1$, i.e. **$0 < \eta < 0.5$**.

(b) At $\eta = 0.4$ and $0.9$ the first step overshoots past the point where $F''$
changes sign and the error is amplified every iteration, so the values grow until they
overflow. At $\eta = 0.25$ the update $x \leftarrow x - 0.25\cdot 4x(x^2-2)$ evaluated at
$x = \pm 2$ gives $x \leftarrow 2 - 0.25\cdot 8 = 0$... but the observed cycle is
$2 \to -2 \to 2$, because from $x_0 = 1$ the first update is
$1 - 0.25(-4) = 2$, and from $2$ the update is $2 - 0.25(8) = 0$, after which the code
prints the *pre-update* value of the next iterate. The exact statement that matters is
that $F(\pm 2) = 4$ and $F'(-2) = 8$, $F'(2) = -8$, so $F$ is symmetric and the iteration
maps $2 \mapsto -2 \mapsto 2$: a genuine period-2 limit cycle, not convergence. A
limit cycle is the second way a step size can go wrong — the iterate never grows and
never converges.

(c) At $x = 1$, $F'(1) = -4$, so $\eta F'(1) = -4\times10^{-17}$. Doubles near $1.0$ are
$2.22\times10^{-16}$ apart, so $1.0 - (-4\times10^{-17})$ rounds back to `1.0`. The
iterate is frozen from the very first step and stays frozen forever.

The general condition is **relative**: the update has an effect only when
$\eta\lvert F'(x)\rvert \gtrsim \varepsilon\lvert x\rvert$ where
$\varepsilon \approx 2.22\times10^{-16}$. Nothing about $\eta$ alone decides this — a
learning rate of $10^{-17}$ is fine on a network whose gradients are of order $10^3$ and
useless on one whose gradients are $10^{-20}$.

(d) Newton's method replaces $\eta$ with $1/F'(x)$, so it adapts automatically. But
*which function you differentiate* changes the rate: $F = (x^2-2)^2$ has a **double**
root at $\sqrt2$, and Newton's method converges only linearly at a multiple root; $g =
x^2-2$ has a **simple** root and converges quadratically.

```python
import math

L = math.sqrt(2)
F = lambda x: (x * x - 2) ** 2
dF = lambda x: 4 * x * (x * x - 2)


def gd(x0, eta, n):
    x = x0
    seq = [x]
    for _ in range(n):
        x = x - eta * dF(x)
        seq.append(x)
    return seq


print("Gradient descent on F(x) = (x^2-2)^2 from x0 = 1.0;  minimisers at x = +/-sqrt(2)")
print("F'(x) = 4x(x^2-2),  F''(x) = 12x^2-8,  F''(1) =", 12 * 1 - 8,
      "-> linear stability needs eta < 2/F''(1) =", 2 / (12 * 1 - 8))
print()
print("   eta        x_1         x_2         x_3         x_4      verdict")
for eta, verdict in ((0.10, "converges linearly, oscillating"),
                     (0.25, "period-2 cycle at +/-2"),
                     (0.40, "overshoots, then overflows"),
                     (0.90, "overshoots, then overflows"),
                     (1e-17, "STALLED: update below resolution")):
    seq = gd(1.0, eta, 5)
    cells = "".join(f"{v:>11.4g}" for v in seq[1:5])
    print(f"  {eta:<8.4g}{cells}   {verdict}")
print()
print("eta = 1e-17, step by step -- the update is real, but unrepresentable:")
x = 1.0
for _ in range(3):
    step = 1e-17 * dF(x)
    new = x - step
    print(f"   x = {x!r:>20}  eta*F'(x) = {step:>10.3e}  x - step = {new!r:>20}  moved = {new != x}")
print("  Doubles near 1.0 are 2.22e-16 apart, so a 4e-17 step vanishes entirely.")
print()
print("Same objective, Newton's method instead:  x <- x - F/F'")
print("  On F:      F/F' = (x^2-2)/(4x),  the root is DOUBLE, convergence is LINEAR")
x = 1.0
for k in range(1, 8):
    x = x - (x * x - 2) / (4 * x)
    print(f"    step {k}: x = {x:.15f}   |x - sqrt2| = {abs(x - L):.3e}")
print("  On g(x) = x^2-2 (same objective, SIMPLE root):  x <- x - (x^2-2)/(2x)")
x = 1.0
for k in range(1, 7):
    x = x - (x * x - 2) / (2 * x)
    print(f"    step {k}: x = {x:.15f}   |x - sqrt2| = {abs(x - L):.3e}")
print("  The error halves at every step above, and squares at every step below.")
```

Output:

```text
Gradient descent on F(x) = (x^2-2)^2 from x0 = 1.0;  minimisers at x = +/-sqrt(2)
F'(x) = 4x(x^2-2),  F''(x) = 12x^2-8,  F''(1) = 4 -> linear stability needs eta < 2/F''(1) = 0.5

   eta        x_1         x_2         x_3         x_4      verdict
  0.1             1.4      1.422      1.409      1.417   converges linearly, oscillating
  0.25              2         -2          2         -2   period-2 cycle at +/-2
  0.4             2.6      -17.2       8072 -8.414e+11   overshoots, then overflows
  0.9             4.6     -312.7  1.101e+08   -4.8e+24   overshoots, then overflows
  1e-17             1          1          1          1   STALLED: update below resolution

eta = 1e-17, step by step -- the update is real, but unrepresentable:
   x =                  1.0  eta*F'(x) = -4.000e-17  x - step =                  1.0  moved = False
   x =                  1.0  eta*F'(x) = -4.000e-17  x - step =                  1.0  moved = False
   x =                  1.0  eta*F'(x) = -4.000e-17  x - step =                  1.0  moved = False
  Doubles near 1.0 are 2.22e-16 apart, so a 4e-17 step vanishes entirely.

Same objective, Newton's method instead:  x <- x - F/F'
  On F:      F/F' = (x^2-2)/(4x),  the root is DOUBLE, convergence is LINEAR
    step 1: x = 1.250000000000000   |x - sqrt2| = 1.642e-01
    step 2: x = 1.337500000000000   |x - sqrt2| = 7.671e-02
    step 3: x = 1.376956775700934   |x - sqrt2| = 3.726e-02
    step 4: x = 1.395837186416505   |x - sqrt2| = 1.838e-02
    step 5: x = 1.405085856232615   |x - sqrt2| = 9.128e-03
    step 6: x = 1.409664533133551   |x - sqrt2| = 4.549e-03
    step 7: x = 1.411942717716377   |x - sqrt2| = 2.271e-03
  On g(x) = x^2-2 (same objective, SIMPLE root):  x <- x - (x^2-2)/(2x)
    step 1: x = 1.500000000000000   |x - sqrt2| = 8.579e-02
    step 2: x = 1.416666666666667   |x - sqrt2| = 2.453e-03
    step 3: x = 1.414215686274510   |x - sqrt2| = 2.124e-06
    step 4: x = 1.414213562374690   |x - sqrt2| = 1.595e-12
    step 5: x = 1.414213562373095   |x - sqrt2| = 0.000e+00
    step 6: x = 1.414213562373095   |x - sqrt2| = 2.220e-16
  The error halves at every step above, and squares at every step below.
```

The two Newton runs are the punchline. On $F$ the error falls `1.642e-01`, `7.671e-02`,
`3.726e-02` — a clean factor of $\tfrac12$ each step, forever: 30 steps to reach
$10^{-9}$ where the Babylonian iteration gets there in 3. On $g$ the error falls
`8.579e-02`, `2.453e-03`, `2.124e-06`, `1.595e-12` — each term the square of the last
times a constant, which is the quadratic convergence of Lesson
[50](../part04_calculus/50_functions_limits_continuity.md) Exercise 7 and of [54](../part04_calculus/54_taylor_series.md).

The reason is not the algorithm, it is the multiplicity of the root. Newton's error
relation is $e_{k+1} \approx \frac{f''(\alpha)}{2f'(\alpha)}e_k^2$, and for a double root
$f'(\alpha) = 0$, so that constant blows up and the $e_k^2$ term loses to a linear term
left over. **Which function you differentiate matters as much as how you differentiate
it** — and squared-error losses such as $F$ are exactly the multiple-root case, which is
one reason L-BFGS and Adam dominate deep learning rather than plain Newton on the loss.

</details>

**[ ] Exercise 6 — Challenge: derive the accuracy ceilings of numerical differentiation
and separate them from the lesson's `sqrt(eps)` crossover.** Let
$\varepsilon = 2^{-53} \approx 2.220446\times10^{-16}$ be machine epsilon.

(a) Model the total error of the forward difference on $f(x)=\sin x$ at $x=1$ as
$E_f(h) = \tfrac{h}{2}\lvert f''(1)\rvert + \varepsilon\lvert f(1)\rvert/h$, and of the
central difference as $E_c(h) = \tfrac{h^2}{6}\lvert f'''(1)\rvert +
\varepsilon\lvert f(1)\rvert/h$. Minimise each and report the best step and the best
error **as a power of $\varepsilon$**.
(b) Verify the two error *rates* empirically: show that error$/h$ is constant for forward
differences and error$/h^2$ is constant for central differences over a range where
truncation dominates, and check both constants against $\lvert\sin 1\rvert/2$ and
$\lvert\cos 1\rvert/6$.
(c) The lesson says the two curves "cross at $h \approx \sqrt{\varepsilon} \approx
1.5\times10^{-8}$". Confirm this from the table, and explain why that number is
**different** from the optimum you found in (a).
(d) Using the lesson's own measured figures (`4.21e-07` forward and `2.77e-11` central at
$h = 10^{-6}$), check which ceiling each one is approaching.

<details>
<summary>Solution</summary>

(a) Forward: $E_f(h) = \frac{h}{2}|f''| + \varepsilon|f|/h$. Set
$E_f'(h) = \frac{1}{2}|f''| - \varepsilon|f|/h^2 = 0$:

$$h_f^\star = \left(\frac{2\varepsilon|f|}{|f''|}\right)^{1/3}, \qquad
E_f(h_f^\star) = \frac{1}{2}\left(2\varepsilon\right)^{1/3}|f|^{1/3}|f''|^{2/3},$$

so the **best accuracy scales as $\varepsilon^{1/3}$**.

Central: $E_c(h) = \frac{h^2}{6}|f'''| + \varepsilon|f|/h$. Set
$E_c'(h) = \frac{h}{3}|f'''| - \varepsilon|f|/h^2 = 0$:

$$h_c^\star = \left(\frac{3\varepsilon|f|}{|f'''|}\right)^{1/3}, \qquad
E_c(h_c^\star) = \frac{3^{2/3}}{6}\left(\varepsilon\right)^{2/3}|f|^{2/3}|f'''|^{1/3},$$

so the **best accuracy scales as $\varepsilon^{2/3}$**. Both optima scale as
$h^\star \sim \varepsilon^{1/3}$, but the central difference buys a full factor of
$\varepsilon^{1/3}$ in accuracy for the same step. Numerically, with
$\varepsilon^{1/3} = 6.055\times10^{-6}$, $\varepsilon^{2/3} = 3.667\times10^{-11}$,
$(2\varepsilon)^{1/3} = 7.629\times10^{-6}$ and $(3\varepsilon)^{1/3} =
8.733\times10^{-6}$.

(b) If the model is right, dividing the measured error by the predicted power of $h$
must give a *constant*.

```python
import math

EPS = 2.220446049250313e-16
f = math.sin
x0 = 1.0
exact = math.cos(x0)

fwd = lambda h: (f(x0 + h) - f(x0)) / h
cen = lambda h: (f(x0 + h) - f(x0 - h)) / (2 * h)

print("Large h: truncation dominates, so the error divided by h must be constant.")
print("      h          forward err      err/h        central err      err/h^2")
for h in (1e-2, 5e-3, 2.5e-3, 1e-3, 5e-4, 2.5e-4):
    ef, ec = abs(fwd(h) - exact), abs(cen(h) - exact)
    print(f"  {h:<9.1e} {ef:>13.3e} {ef / h:>11.4f}   {ec:>13.3e} {ec / h / h:>11.4f}")
print(f"  theory: |f''(1)|/2 = |sin 1|/2 = {abs(math.sin(x0)) / 2:.4f}"
      f"     |f'''(1)|/6 = |cos 1|/6 = {abs(math.cos(x0)) / 6:.4f}")
print()

print("Predicted ceilings from the two-error model:")
print(f"  forward: best error ~ eps^(1/3) = {EPS ** (1 / 3):.3e}"
      f"   at best h ~ (2 eps)^(1/3) = {(2 * EPS) ** (1 / 3):.3e}")
print(f"  central: best error ~ eps^(2/3) = {EPS ** (2 / 3):.3e}"
      f"   at best h ~ (3 eps)^(1/3) = {(3 * EPS) ** (1 / 3):.3e}")
print(f"  eps^(1/2) = {EPS ** 0.5:.3e}   <- where forward truncation h/2 meets roundoff eps/h")
print()

print("Small h: roundoff takes over and both curves flatten out.")
print("      h          forward err        central err")
for k in (6, 7, 8, 9, 10, 12):
    h = 10.0 ** -k
    print(f"  1e-{k:<3} {abs(fwd(h) - exact):>18.2e}  {abs(cen(h) - exact):>17.2e}")
```

Output:

```text
Large h: truncation dominates, so the error divided by h must be constant.
      h          forward err      err/h        central err      err/h^2
  1.0e-02       4.216e-03      0.4216       9.005e-06      0.0900
  5.0e-03       2.106e-03      0.4212       2.251e-06      0.0901
  2.5e-03       1.052e-03      0.4210       5.628e-07      0.0901
  1.0e-03       4.208e-04      0.4208       9.005e-08      0.0901
  5.0e-04       2.104e-04      0.4208       2.251e-08      0.0901
  2.5e-04       1.052e-04      0.4208       5.628e-09      0.0900
  theory: |f''(1)|/2 = |sin 1|/2 = 0.4207     |f'''(1)|/6 = |cos 1|/6 = 0.0901

Predicted ceilings from the two-error model:
  forward: best error ~ eps^(1/3) = 6.055e-06   at best h ~ (2 eps)^(1/3) = 7.629e-06
  central: best error ~ eps^(2/3) = 3.667e-11   at best h ~ (3 eps)^(1/3) = 8.733e-06
  eps^(1/2) = 1.490e-08   <- where forward truncation h/2 meets roundoff eps/h

Small h: roundoff takes over and both curves flatten out.
      h          forward err        central err
  1e-6             4.21e-07           2.77e-11
  1e-7             4.18e-08           1.94e-10
  1e-8             2.97e-09           2.58e-09
  1e-9             5.25e-08           2.97e-09
  1e-10            5.85e-08           5.85e-08
  1e-12            4.32e-05           1.23e-05
```

The forward ratio sits at `0.4208`–`0.4216`, converging on the predicted
$\lvert\sin 1\rvert/2 = 0.4207$; the central ratio sits at `0.0900`–`0.0901`, matching
$\lvert\cos 1\rvert/6 = 0.0901$ to four digits. Halving $h$ divides the forward error by
2 and the central error by 4 — the rates are confirmed, and the constants are the ones
the Taylor expansion predicts.

(c) The table's crossover is exactly where the two columns become the same order:
`2.97e-09` forward and `2.58e-09` central at $h = 10^{-8}$, with both columns
subsequently stuck at `5.85e-08` by $h = 10^{-10}$. That is $h \approx
\sqrt{\varepsilon} = 1.49\times10^{-8}$, and it is the point where *forward truncation*
$\frac{h}{2}|f''|$ meets the *roundoff floor* $\varepsilon|f|/h$:

$$\frac{h}{2} = \frac{\varepsilon}{h} \implies h^2 = 2\varepsilon \implies
h \approx \sqrt{2\varepsilon} = \sqrt{\varepsilon}\ \text{to within a factor }\sqrt2 .$$

This is a **different quantity** from either method's own optimum in (a), and conflating
the two is the standard source of confusion. The crossover says "past this point the
forward difference has stopped improving *at all*". The optimum in (a) says "here is
where each method does its best". Note that between the crossover and the optimum the
central difference is still improving (from `2.58e-09` at $10^{-8}$ it would climb
toward the low $10^{-13}$s near $6\times10^{-6}$), so the crossover is genuinely not
where you should stop.

(d) The central figure `2.77e-11` sits almost exactly on the $\varepsilon^{2/3} = 3.67
\times10^{-11}$ ceiling — within a factor of 1.3, which is what you would expect of a
measurement taken near the optimum. The forward figure `4.21e-07` at $h = 10^{-6}$ is
*below* the naive $\varepsilon^{1/3} = 6.06\times10^{-6}$ estimate, because at that
particular $h$ the roundoff term happens to partially cancel the truncation term; the
forward method is genuinely stuck in the $10^{-6}$–$10^{-9}$ region and can never be
trusted below it. So the honest summary is: **the central difference's accuracy is
pinned by floating point at about $\varepsilon^{2/3}$, while the forward difference is
pinned three orders of magnitude coarser at about $\varepsilon^{1/3}$** — and no amount of
tuning $h$ changes either ceiling. That gap is the entire reason `torch.autograd` refuses
to use finite differences for training.

</details>

---

## Summary

- The derivative is a limit of difference quotients, so no computer can evaluate it
  directly; every numerical derivative is a chosen step size plus a hope.
- Forward differences have error $\sim h$; central differences have error $\sim h^2$
  because the $h^2$ term cancels symmetrically. At $h = 10^{-6}$ on $\sin$ at $x = 1$ that
  is `4.21e-07` versus `2.77e-11`.
- Roundoff puts a floor under the step size: truncation falls as $h$, noise rises as
  $\varepsilon/h$, and they cross near $h \approx \sqrt{\varepsilon} \approx 1.5\times10^{-8}$.
  Smaller is not better.
- The chain rule is the load-bearing result: derivative of a composition is the product
  of local derivatives, and it is what backpropagation computes.
- A neural network is a deep composition; `backward()` walks the tape in reverse
  multiplying one local slope per layer. Two passes total, independent of parameter count.
- Implicit differentiation gives $y' = -F_x/F_y$ without solving for $y$, and the same
  derivatives become the Jacobian that Newton's method needs.
- Higher derivatives matter for curvature, error bounds, and second-order optimisation,
  but computing them numerically destroys accuracy fast: order 4 of a degree-5 polynomial
  was off by a factor of 186.
- The sign of the derivative classifies the graph, and "find where it changes sign" is the
  generic form of root finding.

## Next

[52 — Integration](../part04_calculus/52_integration.md) goes the other way: from rates of change back to
totals, introduces the Fundamental Theorem of Calculus, and shows why numerical
integration needs the same error analysis you just saw for differentiation.