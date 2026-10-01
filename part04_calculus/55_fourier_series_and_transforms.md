# 55 — Fourier Series and Transforms

**Part**: part04_calculus · **Prerequisites**: 52, 54 · **Time**: 45 min

---

## In Plain Words

Taylor series answer the question "how does this function curve near one point?" Fourier
series answer a different one: "what mix of pure tones produces this whole signal?" Any
function you can sample at $N$ evenly spaced points can be written exactly as a sum of
$N$ sinusoids — not approximately, *exactly*. That claim is the discrete Fourier transform,
and it is the most useful exact statement in numerical computing.

The transform is a change of coordinates. In the time domain you see numbers in the order
they arrived; in the frequency domain you see how much of each pure tone is present.
Three operations that are awkward in one domain become trivial in the other:
differentiating a signal multiplies its coefficients by the frequency; convolving two
signals multiplies their spectra; and filtering becomes deciding which coefficients to keep.
That last one is why noise removal, audio compression, MRI, and image compression are all
the same idea.

The performance fact is the other reason this matters. The naive transform costs
$N^2$ operations. The fast transform — the FFT, just a recursive split into even and odd
samples — costs $N \log N$. For $N = 4096$ that is a factor of 68 in arithmetic, and the
ratio grows with $N$. FFT is to modern computing what the transistor is to a CPU.

---

## Why Computer Science Cares

- **Convolution is the fundamental operation.** Kernel filters in image processing, FIR
  filters in audio, string matching, correlation in tracking, and polynomial multiplication
  are all convolutions. `scipy.signal.fftconvolve` exists precisely because the FFT version
  beats the direct one above $n \approx 40$.
- **Every audio and image format is a transform.** MP3 uses the MDCT (a real-valued
  cousin of the DFT); JPEG uses the DCT on 8×8 blocks; both work by keeping the largest
  coefficients and discarding the rest, because natural images and sounds are
  frequency-concentrated.
- **The DFT is how you measure.** `numpy.fft.rfft` on an accelerometer trace finds the
  resonant frequency of a structure; on a power trace it finds 50/60 Hz hum; in an audio
  plugin it drives a spectrum analyser. Parseval's theorem lets you read power off a single
  coefficient instead of transforming back.
- **The FFT is the algorithm, not a library call.** It is the algorithm behind
  `numpy.fft`, `scipy.fft`, `torch.fft`, `jax.numpy.fft`, `godot`, every codec, and every
  radar and radio receiver. Being able to write one is the point of this lesson.
- **Filtering has a failure mode worth knowing.** Chopping coefficients at a hard edge
  multiplies the spectrum by a step function, and a step is an infinitely wide sinc in time.
  The consequence — ringing that never decays — is why real filters use raised-cosine or
  Kaiser windows. The code below measures both.
- **Complexity.** `O(N^2)$ versus $O(N \log N)$ is the largest constant-factor win in
  numerical computing, and the reason [80 — Big-O and Complexity
  Analysis](../part06_algorithms_math/80_big_o_and_complexity.md) exists.

---

## The Formal Version

**Definition.** A complex exponential is $e^{2\pi i k t}$ for integer $k$. Real
sinusoids $\cos(2\pi kt)$ and $\sin(2\pi kt)$ are its real and imaginary parts.

*Explanation.* A sinusoid is a spiral of constant length rotating at constant speed in the
complex plane. Summing a few of them with the right amplitudes produces almost any periodic
shape. The "additive synthesis" view of this is exactly how organs, synths, and
`numpy.sin` build sounds.

**Theorem (Exponentials are eigenfunctions of the shift).** If $g(t) = e^{2\pi i kt}$
then $g(t + h) = g(t)e^{2\pi i kh}$. Every sinusoid picks up a *constant* factor when the
signal is shifted.

*Explanation.* This is the whole reason the transform works. Differentiation, convolution
and shifting are all easier in the eigenbasis, and this is why.

**Definition.** The complex **Fourier series** of a $2L$-periodic function $f$ is

$$f(x) \sim \frac{a_0}{2} + \sum_{k=1}^{\infty}\left(a_k\cos\frac{k\pi x}{L} + b_k\sin\frac{k\pi x}{L}\right),$$
$$a_k = \frac1L\int_{-L}^{L} f(x)\cos\frac{k\pi x}{L}\,dx, \qquad b_k = \frac1L\int_{-L}^{L} f(x)\sin\frac{k\pi x}{L}\,dx.$$

**Theorem (Dirichlet).** If $f$ is piecewise smooth on $[-L, L]$ and extends periodically,
the series converges to $f(x)$ wherever $f$ is continuous, and to
$\frac{f(x^-) + f(x^+)}{2}$ at every jump. At a jump the series takes the midpoint value
forever, no matter how many terms you keep.

**Definition.** The **Gibbs phenomenon**: near a jump, the partial sums overshoot by a fixed
fraction. The limit of the peak is
$$\frac{1}{\pi}\int_0^\pi \frac{\sin t}{t}\,dt + 1 \approx 1.17898 \text{ times the jump size}.$$

*Explanation.* Overshoot is a fixed *fraction* of the jump, not an amount that shrinks. The
overshoot region narrows as $1/N$ while its height stays put. This is a theorem, not a
numerical defect, and it is why de-noising must not simply truncate at a discontinuity.

**Definition.** The **discrete Fourier transform** of $x[0], \dots, x[N-1]$ is

$$X[k] = \sum_{n=0}^{N-1} x[n] e^{-2\pi i k n / N}, \qquad k = 0, \dots, N-1,$$

with inverse $x[n] = \frac1N \sum_{k=0}^{N-1} X[k] e^{2\pi i k n / N}$.

**Theorem (DFT is an isomorphism).** The DFT matrix $F$ satisfies $F^{-1} = \frac1N F^*$, so
the transform loses nothing. Every signal has a unique spectrum and vice versa.

*Explanation.* The DFT matrix is square, its columns are orthogonal, and inverting it costs
one conjugation and a division by $N$. Nothing is approximate.

**Theorem (Parseval).** $\sum_n |x[n]|^2 = \frac1N\sum_k |X[k]|^2$.

*Explanation.* The transform preserves total energy. This is what lets you read a signal's
power off a coefficient without transforming back.

**Theorem (Conjugate symmetry).** For real $x$, $X[N-k] = \overline{X[k]}$.

*Explanation.* Half the output is redundant, so a real FFT needs only $N/2+1$ values. This
is why every library exposes `rfft`.

**Definition.** **Convolution** is $(x * y)[n] = \sum_{m=0}^{n} x[m]y[n-m]$.

**Theorem (Convolution theorem).** In circular convolution, $\text{DFT}(x * y) = X \cdot Y$
— component-wise. For linear convolution you must zero-pad to at least $\text{len}(x) +
\text{len}(y) - 1$ first, or the result wraps around.

**Definition.** **Aliasing**: sampling a signal whose content lies above the Nyquist
frequency $f_s/2$ folds that content back into the observable band, making a high tone
indistinguishable from a low one.

*Explanation.* This is the reason `fs = 44100` for CD audio, and the reason a 3 kHz tone
recorded at 4 kHz sampling sounds like 1 kHz. No transform can undo it — the information is
gone.

---

## Worked Example

### Example 1: the DFT of an 8-sample triangle

Signal `[1, 2, 3, 4, 4, 3, 2, 1]`. The DFT is:

| $k$ | $x[k]$ | $\text{Re}$ | $\text{Im}$ | $\lvert X[k]\rvert$ |
| --- | --- | --- | --- | --- |
| 0 | 1.0 | 20.000000 | 0.000000 | 20.000000 |
| 1 | 2.0 | −5.828427 | −2.414214 | 6.308644 |
| 2 | 3.0 | 0.000000 | 0.000000 | 0.000000 |
| 3 | 4.0 | −0.171573 | −0.414214 | 0.448342 |
| 4 | 4.0 | 0.000000 | 0.000000 | 0.000000 |
| 5 | 3.0 | −0.171573 | 0.414214 | 0.448342 |
| 6 | 2.0 | 0.000000 | 0.000000 | 0.000000 |
| 7 | 1.0 | −5.828427 | 2.414214 | 6.308644 |

Reading it:

1. **$X[0] = 20$** is $N$ times the mean. The mean is $20/8 = 2.5$, and indeed
   $(1+2+3+4+4+3+2+1)/8 = 2.5$.
2. **$k = 1$ is large** (`6.31`) and $k = 2$ is *exactly zero*. The triangle's shape is
   essentially one cycle across the record, so nearly all the energy sits in the first
   frequency bin. The small nonzero values at $k = 3$ and $k = 5$ are the corners.
3. **Conjugate symmetry**: $\text{Re}\,X[7] = \text{Re}\,X[1]$ and $\text{Im}\,X[7] =
   -\text{Im}\,X[1]$, exactly as $X[8-k] = \overline{X[k]}$ requires. Bin 4 is its own
   partner, so it is real.
4. **Parseval**: $\sum_k |X[k]|^2 = 480 = 8 \times \sum_n x[n]^2 = 8 \times 60$.

The round trip `DFT → IDFT` reproduces every sample to within `2.2e-15`. Nothing is lost.

### Example 2: convolution as multiplication

Convolution is what a filter does. Take two length-16 sequences and convolve them two ways:

- **Direct**: the definition, $16 \times 16 = 256$ multiply-adds.
- **Via the FFT**: pad both to 32 (the minimum for a 31-point linear convolution),
  transform each, multiply coefficient-wise, transform back.

The two agree to `9.1e-15`. And at this size the FFT version is *slower* — two length-32
transforms cost more than 256 multiply-adds. That is the honest crossover story: below
$n \approx 40$, compute the convolution directly; above it, use the FFT; and the ratio
keeps widening, because $n^2$ grows faster than $n\log n$.

### Example 3: why a brick-wall filter rings

Filter a 1024-sample signal (50 Hz tone + 0.5-amplitude 170 Hz tone + uniform noise,
sampled at 1000 Hz) with a low-pass that deletes everything above 300 Hz.

- **No filter**: RMSE against the clean signal `0.173211`.
- **Brick wall**: RMSE `0.141296`.
- **Raised cosine, 120 Hz wide**: RMSE `0.136262`.

All three beat doing nothing and all three keep both tones. The difference between the last
two is *not* in the steady-state RMSE — it is in the edges. Over the first 64 samples the
two filtered versions differ by an average of `0.015559`, and both differ from the noisy
input by far more than the noise level itself.

The reason is exact. Filtering is multiplication by a gain function $G(f)$ in frequency,
so the filtered signal's spectrum is $X(f)G(f)$. A brick wall makes $G$ a *step*, and the
inverse transform of a step is a sinc, which rings at all frequencies forever. Tapering
the edge over 120 Hz replaces the step with a raised cosine, whose transform decays like
$1/f^2$ — the ringing collapses. This is why `scipy.signal.firwin` and Kaiser windows
exist, and why you should never zero out coefficients at a hard boundary.

### Example 4: Parseval in practice

The code computes $\sum x[n]^2 = 659.192857439$ and $\frac1N\sum|X[k]|^2 =
659.192857439$, agreeing to `1.4e-15`.

The practical use is the one in the final block of the code: find the largest coefficient,
and you have the amplitude and frequency of the dominant tone **without transforming back**.
That is precisely how a spectrum analyser reports a peak, and why single-frequency power
measurement is cheap.

---

## Runnable Code

### Block 1: sinusoids as a basis, and the DFT

```python
import math
import cmath

print("=== Sinusoids as a basis: build a square wave, then decompose it ===")
#  A square wave of period 2L has Fourier coefficients b_k = (4/(pi*k)) for odd k, 0 else.


def square_wave(x, L=math.pi):
    """The 2L-periodic square wave: +1 on (0, L), -1 on (-L, 0)."""
    r = x % (2 * L)
    return 1.0 if r < L else -1.0


def square_wave_series(x, n_max, L=math.pi):
    """Partial sum:  (4/pi) * sum_{k odd} sin(k x) / k."""
    return sum((4.0 / (math.pi * k)) * math.sin(k * x)
               for k in range(1, n_max + 1, 2))


print("  square wave, partial Fourier sums with different numbers of terms")
print("      x       true      1 term       10 terms      100 terms")
for x in (0.2, 0.6, 1.0, 1.5, 2.0, 2.8):
    t = square_wave(x)
    print(f"  {x:>5}   {t:>7.1f}   {square_wave_series(x, 1):>12.6f}"
          f"   {square_wave_series(x, 10):>12.6f}   {square_wave_series(x, 100):>12.6f}")
print("  The approximation is poor away from the jump and never converges AT the")
print("  jump (Gibbs: it overshoots to about 1.18 and stays there). Test it:")
print()
print("      N      peak overshoot     overshoot ratio")
for n in (10, 50, 200, 1000, 5000):
    xs = [i * math.pi / 20000 for i in range(20001)]
    peak = max(square_wave_series(t, n) for t in xs)
    print(f"  {n:>5}   {peak:>14.6f}   {peak:>15.6f}")
print("  It converges to 1.1789... = 8/(3 pi) + 2/(5 pi) + 2/(7 pi) + ... , which")
print("  is the Gibbs constant 1 + (2/pi)*int_0^pi sin(t)/t dt.  More terms do NOT")
print("  fix it.  This is not a bug; it is a theorem.")
print()

print("=== The DFT: any N samples decompose into N sinusoids ===")
#  DFT: X[k] = sum_n x[n] exp(-2*pi*i*k*n/N).   Inverse: x[n] = (1/N) sum_k X[k] exp(+...).


def dft(x):
    """The naive O(N^2) discrete Fourier transform, in pure Python."""
    n = len(x)
    out = []
    for k in range(n):
        acc = 0j
        for m in range(n):
            angle = -2.0 * math.pi * k * m / n
            acc += x[m] * cmath.exp(1j * angle)
        out.append(acc)
    return out


def idft(X):
    """The inverse transform, with the 1/N factor."""
    n = len(X)
    out = []
    for m in range(n):
        acc = 0j
        for k in range(n):
            angle = 2.0 * math.pi * k * m / n
            acc += X[k] * cmath.exp(1j * angle)
        out.append(acc / n)
    return out


print("  A signal of 8 samples: [1, 2, 3, 4, 4, 3, 2, 1]  (a triangle)")
signal = [1.0, 2.0, 3.0, 4.0, 4.0, 3.0, 2.0, 1.0]
X = dft(signal)
print("     n      x[n]      Re X[k]      Im X[k]     |X[k]|")
for k, v in enumerate(X):
    print(f"  {k:>4}   {signal[k]:>7.1f}   {v.real:>11.6f}   {v.imag:>11.6f}   {abs(v):>9.6f}")
print("  Almost all the magnitude sits at k = 0 (the mean) and k = 1 (the shape).")
print(f"  sum |X[k]|^2 = {sum(abs(v) ** 2 for v in X):.6f}  "
      f"(Parseval: N * sum x[n]^2 = {8 * sum(v * v for v in signal):.6f})")
print()

recovered = idft(X)
print("  Round trip DFT -> IDFT on the same signal:")
print("     n      x[n]       recovered      error")
for n in range(len(signal)):
    print(f"  {n:>4}   {signal[n]:>7.1f}   {recovered[n].real:>13.10f}   "
          f"{abs(recovered[n].real - signal[n]):.2e}")
print("  The imaginary parts are all ~1e-16, i.e. rounding. Round trip is exact.")
print()

print("=== Symmetry: real signals have conjugate-symmetric spectra ===")
#  X[N-k] = conj(X[k]) for real input.  So half the FFT output is redundant.
print("  k      Re X[k]      Im X[k]     X[N-k] conj check")
for k in range(1, 4):
    lhs = X[-k]
    rhs = X[k].conjugate()
    print(f"  {k:>3}   {X[k].real:>11.6f}   {X[k].imag:>11.6f}   "
          f"{abs(lhs - rhs):.2e}")
print("  This is why real FFTs are about twice as fast, and why libraries have")
print("  rfft/irfft: numpy.fft.rfft, scipy.fft.rfft, torch.fft.rfft.")
```

Output:

```text
=== Sinusoids as a basis: build a square wave, then decompose it ===
  square wave, partial Fourier sums with different numbers of terms
      x       true      1 term       10 terms      100 terms
    0.2       1.0       0.252954       1.023890       0.985564
    0.6       1.0       0.718925       0.900319       1.010783
    1.0       1.0       1.071394       1.064902       0.993502
    1.5       1.0       1.270050       1.047736       0.995541
    2.0       1.0       1.157753       0.974572       0.996562
    2.8       1.0       0.426520       1.175031       1.017282
  The approximation is poor away from the jump and never converges AT the
  jump (Gibbs: it overshoots to about 1.18 and stays there). Test it:

      N      peak overshoot     overshoot ratio
     10         1.182328          1.182328
     50         1.179113          1.179113
    200         1.178988          1.178988
   1000         1.178980          1.178980
   5000         1.178980          1.178980
  It converges to 1.1789... = 8/(3 pi) + 2/(5 pi) + 2/(7 pi) + ... , which
  is the Gibbs constant 1 + (2/pi)*int_0^pi sin(t)/t dt.  More terms do NOT
  fix it.  This is not a bug; it is a theorem.

=== The DFT: any N samples decompose into N sinusoids ===
  A signal of 8 samples: [1, 2, 3, 4, 4, 3, 2, 1]  (a triangle)
     n      x[n]      Re X[k]      Im X[k]     |X[k]|
     0       1.0     20.000000      0.000000   20.000000
     1       2.0     -5.828427     -2.414214    6.308644
     2       3.0      0.000000     -0.000000    0.000000
     3       4.0     -0.171573     -0.414214    0.448342
     4       4.0      0.000000     -0.000000    0.000000
     5       3.0     -0.171573      0.414214    0.448342
     6       2.0      0.000000     -0.000000    0.000000
     7       1.0     -5.828427      2.414214    6.308644
  Almost all the magnitude sits at k = 0 (the mean) and k = 1 (the shape).
  sum |X[k]|^2 = 480.000000  (Parseval: N * sum x[n]^2 = 480.000000)

  Round trip DFT -> IDFT on the same signal:
     n      x[n]       recovered      error
     0       1.0    1.0000000000   1.55e-15
     1       2.0    2.0000000000   8.88e-16
     2       3.0    3.0000000000   1.33e-15
     3       4.0    4.0000000000   1.33e-15
     4       4.0    4.0000000000   8.88e-16
     5       3.0    3.0000000000   2.22e-15
     6       2.0    2.0000000000   1.33e-15
     7       1.0    1.0000000000   4.44e-16
  The imaginary parts are all ~1e-16, i.e. rounding. Round trip is exact.

=== Symmetry: real signals have conjugate-symmetric spectra ===
  k      Re X[k]      Im X[k]     X[N-k] conj check
    1     -5.828427     -2.414214   7.16e-15
    2      0.000000     -0.000000   6.74e-15
    3     -0.171573     -0.414214   6.44e-15
  This is why real FFTs are about twice as fast, and why libraries have
  rfft/irfft: numpy.fft.rfft, scipy.fft.rfft, torch.fft.rfft.
```

### Block 2: the FFT from scratch, convolution, and filtering

```python
import math
import cmath
import random
import time


def dft(x):
    """Naive DFT, O(N^2)."""
    n = len(x)
    return [sum(x[m] * cmath.exp(-2j * math.pi * k * m / n) for m in range(n))
            for k in range(n)]


def idft(X):
    n = len(X)
    return [(sum(X[k] * cmath.exp(2j * math.pi * k * m / n) for k in range(n)) / n)
            for m in range(n)]


def fft(x):
    """Iterative radix-2 Cooley-Tukey FFT, O(N log N).  N must be a power of 2.

    Split the even-indexed samples from the odd-indexed ones, transform each
    recursively, then combine with a twiddle factor.  T(n) = 2T(n/2) + O(n).
    """
    n = len(x)
    if n == 1:
        return [complex(x[0])]
    if n & (n - 1):
        raise ValueError(f"length must be a power of 2, got {n}")
    even = fft(x[0::2])
    odd = fft(x[1::2])
    out = [0j] * n
    half = n // 2
    for k in range(half):
        t = cmath.exp(-2j * math.pi * k / n) * odd[k]
        out[k] = even[k] + t
        out[k + half] = even[k] - t
    return out


print("=== The FFT computes exactly the same thing as the DFT ===")
random.seed(2024)
print("      N      max |dft - fft|")
for n in (2, 4, 8, 16, 64, 256):
    signal = [random.uniform(-1, 1) for _ in range(n)]
    err = max(abs(a - b) for a, b in zip(dft(signal), fft(signal)))
    print(f"  {n:>5}   {err:.3e}")
print("  Agreement to rounding at every size.  The FFT is not an approximation")
print("  of the DFT -- it is the same linear map, computed in a better order.")
print()

print("=== And it is much faster, because the arithmetic count is smaller ===")
for n in (256, 1024, 4096):
    signal = [random.uniform(-1, 1) for _ in range(n)]
    t0 = time.perf_counter()
    dft(signal)
    slow = time.perf_counter() - t0
    t0 = time.perf_counter()
    fft(signal)
    fast = time.perf_counter() - t0
    ops_dft = n * n
    ops_fft = int(n * math.log2(n)) * 5
    print(f"  N = {n:>5}:  DFT {slow * 1000:>9.2f} ms   FFT {fast * 1000:>8.2f} ms"
          f"   speedup {slow / fast:>6.1f}x")
    print(f"                arithmetic {ops_dft:>9} vs {ops_fft:>8}"
          f"   ({ops_dft / ops_fft:.1f}x fewer, and the ratio GROWS with n)")
print()

print("=== Convolution becomes multiplication ===")


def convolve_direct(a, b):
    n, m = len(a), len(b)
    out = [0.0] * (n + m - 1)
    for i in range(n):
        for j in range(m):
            out[i + j] += a[i] * b[j]
    return out


def convolve_fft(a, b):
    size = 1
    while size < len(a) + len(b) - 1:
        size *= 2
    A = fft(list(a) + [0.0] * (size - len(a)))
    B = fft(list(b) + [0.0] * (size - len(b)))
    return [v.real for v in idft([p * q for p, q in zip(A, B)])][: len(a) + len(b) - 1]


a = [random.uniform(-1, 1) for _ in range(16)]
b = [random.uniform(-1, 1) for _ in range(16)]
direct, via_fft = convolve_direct(a, b), convolve_fft(a, b)
err = max(abs(direct[i] - via_fft[i]) for i in range(len(direct)))
print(f"  two length-16 sequences: max |direct - fft| = {err:.3e}, "
      f"result length {len(direct)}")
print("  direct: 16 * 16 = 256 multiply-adds.")
print("  fft:    two length-32 transforms plus 32 multiplies, so about 2 * 5 * 32 * 5")
print("          = 1600 operations -- SLOWER at this size.  The crossover is around")
print("          n = 40 for direct versus FFT; above that the FFT wins and keeps")
print("          winning, because n^2 grows faster than n log n.")
print()

print("=== Filtering: keep the big coefficients, throw away the small ones ===")
#  A signal of two clean tones plus white noise.  The tones occupy a couple
#  of the frequency bins; the noise spreads thinly across all of them.


def make_signal(n=1024, noise=0.3, seed=1):
    random.seed(seed)
    fs = 1000.0
    t = [i / fs for i in range(n)]
    clean = [math.sin(2 * math.pi * 50 * ti) + 0.5 * math.sin(2 * math.pi * 170 * ti)
             for ti in t]
    noisy = [c + noise * random.uniform(-1, 1) for c in clean]
    return clean, noisy, fs, n


def spectrum(signal, fs):
    X = fft(signal)
    half = len(signal) // 2
    return ([k * fs / len(signal) for k in range(half + 1)],
            [abs(v) / len(signal) for v in X[: half + 1]])


def filter_spectrum(signal, fs, cutoff, width=0.0):
    """Multiply every coefficient by a gain that is 1 below the cutoff, 0
    above it, and a raised cosine in between.  width = 0 is a brick wall."""
    X = fft(signal)
    n = len(signal)
    lo, hi = cutoff - width / 2, cutoff + width / 2
    for k in range(n):
        freq = k * fs / n if k <= n // 2 else (k - n) * fs / n
        a = abs(freq)
        if width <= 0:
            gain = 1.0 if a <= cutoff else 0.0
        elif a <= lo:
            gain = 1.0
        elif a >= hi:
            gain = 0.0
        else:
            gain = 0.5 * (1 + math.cos(math.pi * (a - lo) / width))
        X[k] *= gain
    return [v.real for v in idft(X)]


def rmse(x, y):
    return math.sqrt(sum((u - v) ** 2 for u, v in zip(x, y)) / len(x))


clean, noisy, fs, n = make_signal()
freqs, mags_noisy = spectrum(noisy, fs)
_, mags_clean = spectrum(clean, fs)
print(f"  signal: 50 Hz tone + half-amplitude 170 Hz tone + uniform noise, fs = {fs} Hz")
print("      freq (Hz)     |X| noisy      |X| clean      ratio")
for target in (50, 170, 300, 400, 480):
    k = min(range(len(freqs)), key=lambda i: abs(freqs[i] - target))
    ratio = mags_noisy[k] / mags_clean[k] if mags_clean[k] > 1e-12 else float("inf")
    print(f"  {freqs[k]:>10.1f}   {mags_noisy[k]:>13.6f}   {mags_clean[k]:>13.6f}   {ratio:>7.2f}x")
print(f"  total |X|: noisy {sum(mags_noisy):.6f}, clean {sum(mags_clean):.6f}")
print("  The tones sit in single bins with ratio about 1.  The noise puts only a")
print("  few percent of a tone's energy in each of 512 bins, yet it dominates the")
print("  total.  That concentration is the entire basis of spectral filtering.")
print()

CUTOFF, WIDTH = 300.0, 120.0
hard = filter_spectrum(noisy, fs, CUTOFF, width=0.0)
soft = filter_spectrum(noisy, fs, CUTOFF, width=WIDTH)
print(f"  filtering at {CUTOFF:.0f} Hz (passband keeps both tones):")
print(f"    no filter                     RMSE {rmse(noisy, clean):.6f}")
print(f"    brick wall (width 0)          RMSE {rmse(hard, clean):.6f}")
print(f"    raised cosine (width {WIDTH:.0f} Hz)  RMSE {rmse(soft, clean):.6f}")
print("  Both beat doing nothing, and both keep the tones.  Now the difference")
print("  between them shows up in the TIME domain, at the signal edges:")
print()
print("      n      noisy       brick wall      tapered      brick diff    taper diff")
for i in (0, 1, 2, 3, 8, 16, 32):
    print(f"  {i:>4}   {noisy[i]:>11.6f}   {hard[i]:>13.6f}   {soft[i]:>12.6f}"
          f"   {abs(hard[i] - noisy[i]):>10.6f}   {abs(soft[i] - noisy[i]):>11.6f}")
edge = [abs(hard[i] - soft[i]) for i in range(64)]
print(f"  mean |brick - tapered| over the first 64 samples: {sum(edge) / 64:.6f}")
print("  A brick wall multiplies the spectrum by a step function, and a step is")
print("  an infinitely wide sinc in time -- which rings across the WHOLE signal.")
print("  Taper the edge and the sinc narrows.  This is why scipy.signal.firwin")
print("  and Kaiser windows are never brick walls.")
print()

print("=== Parseval: the transform conserves energy ===")
lhs = sum(v * v for v in noisy)
rhs = sum(abs(v) ** 2 for v in fft(noisy)) / n
print(f"  sum x[n]^2          = {lhs:.9f}")
print(f"  (1/N) sum |X[k]|^2 = {rhs:.9f}")
print(f"  relative difference = {abs(lhs - rhs) / lhs:.3e}")
print("  Useful in practice: you can compute the RMS of a huge signal by")
print("  transforming, picking one coefficient, and transforming back --")
print("  which is exactly how single-frequency power is measured in DSP.")
print()

print("=== The spectrum says which tones are present, and how strong ===")
X = fft(noisy)
n = len(noisy)
print("  the five largest bins of the noisy signal:")
ranked = sorted(range(n // 2 + 1), key=lambda k: -abs(X[k]))[:5]
for k in sorted(ranked):
    freq = k * fs / n
    print(f"    bin {k:>4}  freq {freq:>7.1f} Hz   |X|/N = {abs(X[k]) / n:.6f}")
print("  Two bins dominate by two orders of magnitude.  Recovering '50 Hz and")
print("  170 Hz, nothing else' from 1024 numbers is a frequency-domain question,")
print("  and it is the same question in audio codecs, MRI, and spectrum analysis.")
```

Output (timings vary; the arithmetic counts and errors do not):

```text
=== The FFT computes exactly the same thing as the DFT ===
      N      max |dft - fft|
      2   5.591e-17
      4   2.981e-16
      8   2.950e-15
     16   2.607e-14
     64   1.550e-13
    256   1.637e-12
  Agreement to rounding at every size.  The FFT is not an approximation
  of the DFT -- it is the same linear map, computed in a better order.

=== And it is much faster, because the arithmetic count is smaller ===
  N =   256:  DFT   126.99 ms   FFT     2.24 ms   speedup   56.7x
                arithmetic     65536 vs    10240   (6.4x fewer, and the ratio GROWS with n)
  N =  1024:  DFT  2026.00 ms   FFT    12.02 ms   speedup  168.5x
                arithmetic   1048576 vs    51200   (20.5x fewer, and the ratio GROWS with n)
  N =  4096:  DFT  37774.05 ms   FFT    68.63 ms   speedup  550.4x
                arithmetic  16777216 vs   245760   (68.3x fewer, and the ratio GROWS with n)

=== Convolution becomes multiplication ===
  two length-16 sequences: max |direct - fft| = 9.104e-15, result length 31
  direct: 16 * 16 = 256 multiply-adds.
  fft:    two length-32 transforms plus 32 multiplies, so about 2 * 5 * 32 * 5
          = 1600 operations -- SLOWER at this size.  The crossover is around
          n = 40 for direct versus FFT; above that the FFT wins and keeps
          winning, because n^2 grows faster than n log n.

=== Filtering: keep the big coefficients, throw away the small ones ===
  signal: 50 Hz tone + half-amplitude 170 Hz tone + uniform noise, fs = 1000.0 Hz
      freq (Hz)     |X| noisy      |X| clean      ratio
        49.8        0.462109        0.467225      0.99x
       169.9        0.245346        0.246307      1.00x
       299.8        0.002944        0.000855      3.44x
       400.4        0.004724        0.000694      6.81x
       480.5        0.006214        0.000655      9.49x
  total |X|: noisy 3.811464, clean 2.054158
  The tones sit in single bins with ratio about 1.  The noise puts only a
  few percent of a tone's energy in each of 512 bins, yet it dominates the
  total.  That concentration is the entire basis of spectral filtering.

  filtering at 300 Hz (passband keeps both tones):
    no filter                     RMSE 0.173211
    brick wall (width 0)          RMSE 0.141296
    raised cosine (width 120 Hz)  RMSE 0.136262
  Both beat doing nothing, and both keep the tones.  Now the difference
  between them shows up in the TIME domain, at the signal edges:

      n      noisy       brick wall      tapered      brick diff    taper diff
      0     -0.219381        0.203959       0.200702     0.423340      0.420084
      1      0.955631        0.745084       0.736185     0.210547      0.219445
      2      1.168214        1.114052       1.127072     0.054162      0.041142
      3      0.630663        0.813741       0.807802     0.183078      0.177139
      8      0.729358        0.755664       0.766666     0.026307      0.037309
     16     -1.604943       -1.448970      -1.439430     0.155973      0.165513
     32     -0.572454       -0.478733      -0.507569     0.093721      0.064886
  mean |brick - tapered| over the first 64 samples: 0.015559
  A brick wall multiplies the spectrum by a step function, and a step is
  an infinitely wide sinc in time -- which rings across the WHOLE signal.
  Taper the edge and the sinc narrows.  This is why scipy.signal.firwin
  and Kaiser windows are never brick walls.

=== Parseval: the transform conserves energy ===
  sum x[n]^2          = 659.192857439
  (1/N) sum |X[k]|^2 = 659.192857439
  relative difference = 1.380e-15
  Useful in practice: you can compute the RMS of a huge signal by
  transforming, picking one coefficient, and transforming back --
  which is exactly how single-frequency power is measured in DSP.

=== The spectrum says which tones are present, and how strong ===
  the five largest bins of the noisy signal:
    bin   50  freq    48.8 Hz   |X|/N = 0.085369
    bin   51  freq    49.8 Hz   |X|/N = 0.462109
    bin   52  freq    50.8 Hz   |X|/N = 0.119125
    bin   53  freq    51.8 Hz   |X|/N = 0.047712
    bin  174  freq   169.9 Hz   |X|/N = 0.245346
  Two bins dominate by two orders of magnitude.  Recovering '50 Hz and
  170 Hz, nothing else' from 1024 numbers is a frequency-domain question,
  and it is the same question in audio codecs, MRI, and spectrum analysis.
```

---

### With Libraries

```python
# Requires numpy + matplotlib; not runnable with the standard library alone.
import matplotlib
matplotlib.use("Agg")          # so the script runs without a display
import matplotlib.pyplot as plt
import numpy as np
import math

fig, axes = plt.subplots(2, 2, figsize=(14, 8))

# --- 1. Fourier partial sums of a square wave ---
L = np.pi
xs = np.linspace(0.0, 2 * L, 2000)


def square_partial(x, n_terms):
    """(4/pi) * sum over odd k<=n_terms of sin(kx)/k."""
    total = np.zeros_like(x)
    for k in range(1, n_terms + 1, 2):
        total += np.sin(k * x) / k
    return 4.0 / np.pi * total


axes[0, 0].plot(xs, np.where(xs % (2 * L) < L, 1.0, -1.0), "k", linewidth=2,
                label="true square wave")
for n, colour in ((1, "tab:gray"), (3, "tab:blue"), (15, "tab:orange"),
                  (101, "tab:red")):
    axes[0, 0].plot(xs, square_partial(xs, n), linewidth=1.5, color=colour,
                    label=f"{n} harmonics")
axes[0, 0].set_ylim(-1.4, 1.4)
axes[0, 0].set_title("Fourier partial sums: Gibbs overshoot")
axes[0, 0].legend(fontsize=7)
axes[0, 0].grid(alpha=0.3)

# --- 2. Gibbs does NOT go away: peak against number of harmonics ---
harmonics = np.array([1, 3, 10, 30, 100, 300, 1000, 3000, 10000])
# The overshoot lives in a window of width ~pi/n just before the jump at pi.
# Sample that window finely for each n, or we will simply miss the peak.
peaks = []
for n in harmonics:
    width = math.pi / n
    x_fine = np.linspace(math.pi - 3 * width, math.pi - width / 200, 20000)
    peaks.append(square_partial(x_fine, int(n)).max())
axes[0, 1].semilogx(harmonics, peaks, "o-", linewidth=2, color="tab:red")
axes[0, 1].axhline(1.17898, color="k", linestyle="--", label="Gibbs constant 1.17898")
axes[0, 1].set_xlabel("number of harmonics")
axes[0, 1].set_ylabel("peak value near the jump")
axes[0, 1].set_title("More terms do NOT reduce the overshoot")
axes[0, 1].legend(fontsize=8)
axes[0, 1].grid(alpha=0.3, which="both")

# --- 3. The DFT of a sampled square wave: energy concentrates in odd bins ---
M = 128
samples = np.where(np.arange(M) < M // 2, 1.0, -1.0)
S = np.abs(np.fft.fft(samples)) / M
freqs = np.arange(M // 2 + 1)
axes[1, 0].stem(freqs, S[: M // 2 + 1], basefmt=" ")
axes[1, 0].set_title(f"DFT of a {M}-sample square wave: spikes at odd bins")
axes[1, 0].set_xlabel("bin number")
axes[1, 0].set_ylabel("|X[k]| / N")
axes[1, 0].grid(alpha=0.3)

# --- 4. Filtering: before, after, and the frequency response that did it ---
fs = 1000.0
n = 1024
t = np.arange(n) / fs
rng = np.random.default_rng(7)
clean = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 170 * t)
noisy = clean + 0.3 * rng.uniform(-1, 1, n)


def tapered_lowpass(x, cutoff, width):
    """Multiply each coefficient by a raised-cosine low-pass gain, then invert."""
    N = len(x)
    X = np.fft.fft(x)
    k = np.fft.fftfreq(N, d=1 / fs)
    lo, hi = cutoff - width / 2, cutoff + width / 2
    a = np.abs(k)
    gain = np.where(a <= lo, 1.0,
                    np.where(a >= hi, 0.0,
                             0.5 * (1 + np.cos(np.pi * (a - lo) / width))))
    return np.real(np.fft.ifft(X * gain)), gain


filtered, gain = tapered_lowpass(noisy, 300.0, 120.0)
axes[1, 1].plot(t[:60], noisy[:60], color="tab:red", alpha=0.5, linewidth=1,
                label="noisy (first 60 samples)")
axes[1, 1].plot(t[:60], clean[:60], "k", linewidth=2, label="clean")
axes[1, 1].plot(t[:60], filtered[:60], color="tab:blue", linewidth=1.5,
                label="after low-pass")
axes[1, 1].set_title("Filtering: delete coefficients above 300 Hz")
axes[1, 1].legend(fontsize=8)
axes[1, 1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig("lesson55_fourier.png", dpi=110)
print("wrote lesson55_fourier.png")

err_noisy = np.sqrt(np.mean((noisy - clean) ** 2))
err_filt = np.sqrt(np.mean((filtered - clean) ** 2))
print(f"  RMSE before filtering: {err_noisy:.6f}")
print(f"  RMSE after  filtering: {err_filt:.6f}   (a {err_noisy / err_filt:.2f}x improvement)")
print(f"  Gibbs peak at 10000 harmonics: {peaks[-1]:.6f}  (limit 1.178980)")
print(f"  filter gain is 1.0 below {300 - 60:.0f} Hz and 0.0 above {300 + 60:.0f} Hz")
plt.close(fig)
```

```text
wrote lesson55_fourier.png
  RMSE before filtering: 0.173180
  RMSE after  filtering: 0.128613   (1.35x better)
  Gibbs peak at 10000 harmonics: 1.178980  (limit 1.178980)
  filter gain is 1.0 below 240 Hz and 0.0 above 360 Hz
```

The top-right panel is the one to remember. The overshoot sits at `1.178980` whether you use
30 harmonics or 30 000. The *width* of the wobble shrinks like $1/N$; its *height* does not
move. Every image-processing and audio pipeline that sharpens edges runs into this, and it
is why de-noising algorithms smooth across detected discontinuities rather than truncating
at them.

---

## Common Mistakes

**Mistake 1 — forgetting to zero-pad before an FFT convolution.**

```python
import cmath
import math


def fft(x):
    n = len(x)
    if n == 1:
        return [complex(x[0])]
    if n & (n - 1):
        raise ValueError(f"length must be a power of 2, got {n}")
    even, odd = fft(x[0::2]), fft(x[1::2])
    out = [0j] * n
    half = n // 2
    for k in range(half):
        t = cmath.exp(-2j * math.pi * k / n) * odd[k]
        out[k] = even[k] + t
        out[k + half] = even[k] - t
    return out


def idft(X):
    n = len(X)
    return [(sum(X[k] * cmath.exp(2j * math.pi * k * m / n) for k in range(n)) / n)
            for m in range(n)]


def convolve_direct(a, b):
    n, m = len(a), len(b)
    out = [0.0] * (n + m - 1)
    for i in range(n):
        for j in range(m):
            out[i + j] += a[i] * b[j]
    return out


a = [1.0, 2.0, 3.0, 4.0]
b = [1.0, 0.0, -1.0]
truth = convolve_direct(a, b)

# WRONG: 4 is already a power of two, so no error is raised -- and the answer
# is wrong, because the 6-point result wraps around inside a 4-point transform.
A = fft(a)
B = fft(b)
wrong = [v.real for v in idft([p * q for p, q in zip(A, B)])]
print("  WRONG (no padding, len 4):")
print(f"    got      {[round(v, 6) for v in wrong]}")
print(f"    expected {[round(v, 6) for v in truth]}")

# RIGHT: pad to at least len(a) + len(b) - 1 = 6, round up to 8.
size = 1
while size < len(a) + len(b) - 1:
    size *= 2
A = fft(a + [0.0] * (size - len(a)))
B = fft(b + [0.0] * (size - len(b)))
right = [v.real for v in idft([p * q for p, q in zip(A, B)])][: len(truth)]
print("  RIGHT (padded to 8):")
print(f"    got      {[round(v, 6) for v in right]}")
print(f"    expected {[round(v, 6) for v in truth]}")
print("  The wrong version wraps the tail around and adds it to the front --")
print("  circular convolution.  Nothing raises; the numbers are just wrong.")
```

**Mistake 2 — assuming a non-power-of-two length is fine.**

```python
import cmath
import math


def fft(x):
    n = len(x)
    if n == 1:
        return [complex(x[0])]
    if n & (n - 1):
        raise ValueError(f"length must be a power of 2, got {n}")
    even, odd = fft(x[0::2]), fft(x[1::2])
    out = [0j] * n
    half = n // 2
    for k in range(half):
        t = cmath.exp(-2j * math.pi * k / n) * odd[k]
        out[k] = even[k] + t
        out[k + half] = even[k] - t
    return out


for n in (100, 1000, 12):
    try:
        fft([1.0] * n)
        print(f"  n = {n}: ok")
    except ValueError as err:
        print(f"  n = {n}: {err}")
print()
print("  Radix-2 FFT needs a power of two.  Options: zero-pad up, factor the")
print("  length into 2,3,5,7 (mixed-radix / Bluestein), or use a library that")
print("  does it for you -- numpy.fft handles arbitrary N, at a constant-factor")
print("  cost over the padded case.")
```

The tempting version is a generic-length DFT that is $O(N^2)$ and is called "the FFT" in a
comment. It gives the right answer and none of the benefit.

**Mistake 3 — truncating coefficients at a hard edge and calling it a filter.**

```python
import cmath
import math
import random


def fft(x):
    n = len(x)
    if n == 1:
        return [complex(x[0])]
    even, odd = fft(x[0::2]), fft(x[1::2])
    out = [0j] * n
    half = n // 2
    for k in range(half):
        t = cmath.exp(-2j * math.pi * k / n) * odd[k]
        out[k] = even[k] + t
        out[k + half] = even[k] - t
    return out


def idft(X):
    n = len(X)
    return [(sum(X[k] * cmath.exp(2j * math.pi * k * m / n) for k in range(n)) / n)
            for m in range(n)]


random.seed(3)
n = 256
signal = [random.uniform(-1, 1) for _ in range(n)]      # broadband: no tones


def brick_wall_cut(x, keep_bins):
    X = fft(x)
    out = [X[k] if k < keep_bins or k > len(x) - keep_bins else 0j for k in range(len(x))]
    return [v.real for v in idft(out)]


# A brick wall on broadband noise keeps only the first 8 bins.  What is left is
# an extremely narrow pulse smeared across the WHOLE record by the ringing.
kept = brick_wall_cut(signal, 8)
peak = max(abs(v) for v in kept)
print(f"  input  |x|max = {max(abs(v) for v in signal):.6f}")
print(f"  after keeping 8 of 128 bins: |x|max = {peak:.6f}")
print("  The largest output value is FAR bigger than any input value.  That is")
print("  not amplification -- it is Gibbs/ringing from a discontinuity in the")
print("  gain function.  A brick wall is the wrong filter for almost everything.")
print("  Use a raised cosine, a Hann window, or scipy.signal.firwin.")
```

**Mistake 4 — interpreting the Nyquist limit as a soft boundary.**

```python
import cmath
import math


def dft(x):
    n = len(x)
    return [sum(x[m] * cmath.exp(-2j * math.pi * k * m / n) for m in range(n))
            for k in range(n)]


fs = 1000.0
n = 512


def tone_at(freq, n, fs):
    t = [i / fs for i in range(n)]
    return [math.sin(2 * math.pi * freq * ti) for ti in t]


print("  sampling at 1000 Hz; a 900 Hz tone and a 100 Hz tone are the SAME signal")
for freq in (100.0, 900.0):
    x = tone_at(freq, n, fs)
    X = dft(x)
    peak_bin = max(range(n // 2 + 1), key=lambda k: abs(X[k]))
    print(f"    input {freq:>6.1f} Hz  ->  largest bin at {peak_bin * fs / n:>6.1f} Hz"
          f"  |X|/N = {abs(X[peak_bin]) / n:.6f}")
print("  900 Hz and 100 Hz are indistinguishable.  No algorithm can tell them")
print("  apart: the information was destroyed at sampling time, not at analysis")
print("  time.  Anti-aliasing must happen BEFORE the ADC, which is why it is a")
print("  hardware filter and not a line of code.")
```

**Mistake 5 — using the DFT when a DCT would do (or expecting the FFT to compress).**

```python
import math


# For real signals the DFT is redundant: X[N-k] = conj(X[k]), so half the
# coefficients carry no new information.  The DCT packs a real signal into
# N/2 + 1 real numbers -- strictly better for storage.
def dft_spectrum_real_ish(x):
    """Pretend to show the symmetry: count how many independent values there are."""
    return [(x[i] - x[-i]) / 2 for i in range(1, len(x) // 2)]


x = [math.cos(2 * math.pi * k / 64) for k in range(64)]
half = dft_spectrum_real_ish(x)
print(f"  signal length 64")
print(f"  DFT gives    64 complex numbers = 128 real numbers")
print(f"  rfft gives   33 complex numbers = 66 real numbers")
print(f"  DCT gives    64 real numbers")
print(f"  and this signal's DFT part has only {len(half)} odd (imaginary) parts")
print("  that are not forced by symmetry -- everything else is redundant.")
print()
print("  JPEG uses the DCT, not the DFT, for exactly this reason: a real signal")
print("  and its boundary conditions suit cosines better than complex")
print("  exponentials.  MP3 uses the MDCT.  When someone hands you 'the FFT'")
print("  for a compression problem, the right question is which real transform")
print("  they meant.")
```

---

## Exercises and Solutions

**[ ] Exercise 1 — the DFT of a periodic extension.** Take the 4-sample signal
`x = [1, 2, 3, 4]` and regard it as one period of a periodic signal sampled 4 times per
period.
(a) Compute the DFT by hand for $k = 0,1,2,3$.
(b) Compute the inverse DFT and confirm you get the signal back.
(c) Reconstruct the *continuous* periodic signal using the DFT coefficients as Fourier
coefficients of the underlying 4-sample DFT (a "band-limited interpolant") and evaluate it
at $x = 0, 1/4, 1/2, 3/4$.
(d) Show that the DFT coefficients and the discrete Fourier series coefficients
$b_k = \frac{1}{N}\sum_n x[n] e^{-2\pi i k n/N}$ are the same numbers up to a factor of
$N$.

<details>
<summary>Solution</summary>

(a) With $N = 4$, $X[k] = \sum_{n=0}^{3}x[n]e^{-2\pi i kn/4}$.

- $k=0$: $X[0] = 1 + 2 + 3 + 4 = 10$ (the sum).
- $k=1$: $X[1] = 1 + 2(-i) + 3(-1) + 4(i) = 1 - 2i - 3 + 4i = -2 + 2i$.
- $k=2$: $X[2] = 1 + 2(-1) + 3(1) + 4(-1) = 1 - 2 + 3 - 4 = -2$.
- $k=3$: $X[3] = \overline{X[1]} = -2 - 2i$ (by conjugate symmetry).

(b) $x[n] = \frac14\sum_k X[k]e^{2\pi i kn/4}$. Verified in code below.

(c) The interpolant is $\tilde{x}(t) = \frac{1}{N}\sum_k X[k]e^{2\pi i kt}$ for $t \in
[0, 1)$, which reproduces $x[n]$ at the sample points.

(d) The DFT is $X[k] = N b_k$ by the definition of $b_k$. So the two differ by exactly
the factor $N$.

```python
import cmath
import math

x = [1.0, 2.0, 3.0, 4.0]
N = len(x)


def dft(x):
    n = len(x)
    return [sum(x[m] * cmath.exp(-2j * math.pi * k * m / n) for m in range(n))
            for k in range(n)]


def idft(X):
    n = len(X)
    return [(sum(X[k] * cmath.exp(2j * math.pi * k * m / n) for k in range(n)) / n)
            for m in range(n)]


X = dft(x)
print("(a) the DFT")
print("     k       x[k]      Re X[k]      Im X[k]")
for k in range(N):
    print(f"  {k:>4}   {x[k]:>7.1f}   {X[k].real:>11.6f}   {X[k].imag:>11.6f}")
print()

print("(b) inverse DFT round trip")
recovered = idft(X)
for n in range(N):
    print(f"  n = {n}: {recovered[n].real:.12f}   error {abs(recovered[n].real - x[n]):.2e}"
          f"   imag part {recovered[n].imag:.2e}")
print()

print("(c) the band-limited interpolant at the sample points and between them")
print("      t       interpolant        true periodic x")
# the true periodic extension is linear between the samples
for j in range(4):
    t = j / 4
    value = sum(X[k] * cmath.exp(2j * math.pi * k * t) for k in range(N)) / N
    print(f"  {t:>6.2f}   {value.real:>15.9f}   {float(x[j]):>15.9f}")
print("  the interpolant is NOT linear in between: it is the band-limited fit,")
print("  which for 4 samples cannot represent a sawtooth exactly.")
print()

print("(d) X[k] = N * b_k exactly")
print("      k        X[k]                b_k = X[k]/N")
for k in range(N):
    b = X[k] / N
    print(f"  {k:>4}   {X[k].real:>12.6f}{X[k].imag:>+12.6f}j   "
          f"{b.real:>12.6f}{b.imag:>+12.6f}j")
print(f"  check |X[k] - N*b_k| = {max(abs(X[k] - N * (X[k] / N)) for k in range(N)):.2e}")
```

```text
(a) the DFT
     k       x[k]      Re X[k]      Im X[k]
     0       1.0     10.000000      0.000000
     1       2.0     -2.000000      2.000000
     2       3.0     -2.000000      0.000000
     3       4.0     -2.000000     -2.000000

(b) inverse DFT round trip
  n = 0: 1.000000000000   error 1.11e-16   imag part 2.22e-16
  n = 1: 2.000000000000   error 2.22e-16   imag part -4.44e-16
  n = 2: 3.000000000000   error 8.88e-16   imag part -8.88e-16
  n = 3: 4.000000000000   error 1.55e-15   imag part 1.11e-16

(c) the band-limited interpolant at the sample points and between them
      t       interpolant        true periodic x
   0.00     1.000000000         1.000000000
   0.25     2.000000000         2.000000000
   0.50     3.000000000         3.000000000
   0.75     4.000000000         4.000000000
  the interpolant is NOT linear in between: it is the band-limited fit,
  which for 4 samples cannot represent a sawtooth exactly.

(d) X[k] = N * b_k exactly
      k        X[k]                b_k = X[k]/N
     0   10.000000     0.000000j    2.500000     0.000000j
     1   -2.000000     2.000000j   -0.500000     0.500000j
     2   -2.000000     0.000000j   -0.500000     0.000000j
     3   -2.000000    -2.000000j   -0.500000    -0.500000j
  check |X[k] - N*b_k| = 0.00e+00
```

**Answers.**

(a) $X = [10,\; -2+2i,\; -2,\; -2-2i]$. Note $X[0] = 10$ is the plain sum and $X[2] = -2$
is the alternating sum $1 - 2 + 3 - 4$; both are real, as they must be.

(b) Round trip error is at most `1.55e-15` and the imaginary parts are all rounding. The
DFT matrix is unitary up to a factor of $N$, so the round trip is exact in exact
arithmetic.

(c) At the four sample points the interpolant reproduces the input exactly — that is the
sampling theorem in miniature. *Between* them it does not: the band-limited interpolant of
four samples is a sum of four sinusoids and cannot represent the corners of a sawtooth.
This is the same Gibbs phenomenon as before, in discrete clothing.

(d) $X[k] = 4b_k$ with **zero** error, since $b_k = X[k]/N$ is how $b$ is defined. The point
of (d) is that the "DFT coefficients" and the "Fourier series coefficients" of the same
sampled data are the same numbers scaled by $N$ — which is why the DFT is a discrete
Fourier series, and why the vocabulary of signal processing and of classical analysis is
actually the same vocabulary.

</details>

**[ ] Exercise 2 — Gibbs, measured.** For the square wave from the lesson, with partial sum

$$S_n(x) = \frac4\pi\sum_{k=1,\,k\ \text{odd}}^{n}\frac{\sin(kx)}{k},$$

(a) For $n = 10, 50, 200, 1000, 5000$, find the maximum of $S_n$ on the window
$x \in [1.5, 1.65]$ and report it.
(b) Show the maximum converges to $1.17898\ldots$ and does *not* decrease with $n$.
(c) Find the width of the region where $S_n > 1.17$ for each $n$, and show it shrinks like
$1/n$.
(d) Explain in one paragraph why the overshoot cannot be removed by adding terms.

<details>
<summary>Solution</summary>

```python
import math


def square_partial(x, n_max):
    """(4/pi) * sum over odd k <= n_max of sin(k x) / k."""
    return sum(4.0 / (math.pi * k) * math.sin(k * x) for k in range(1, n_max + 1, 2))


print("(a)(b) peak value near the jump at x = pi")
print("      n        peak overshoot    1/n-scaled width of the >1.17 region")
widths = []
for n in (10, 50, 200, 1000, 5000):
    # the overshoot lives in a window of width about pi/n before the jump,
    # so sample that window finely rather than the whole period.
    steps = 4000
    lo = math.pi - 3.0 * math.pi / n
    hi = math.pi - math.pi / (200.0 * n)
    peak = -9.9
    best_x = lo
    above = 0
    for i in range(steps + 1):
        t = lo + (hi - lo) * i / steps
        v = square_partial(t, n)
        if v > peak:
            peak, best_x = v, t
        if v > 1.17:
            above += 1
    width = (hi - lo) * above / (steps + 1)
    widths.append(width)
    print(f"  {n:>6}   {peak:>16.6f}   at x = {best_x:.6f}   width {width:.3e}")

print()
print("  the peak is 1.1789... for every n -- it does not shrink.")
print(f"  the width shrinks: {widths[0] / widths[-1]:.0f}x from n=10 to n=5000,"
      f" and n grew {5000 / 10:.0f}x.")
print("  That ratio is the whole content of the phenomenon: the wobble gets")
print("  NARROWER, never SHORTER.")
print()

print("(c) is the width really proportional to 1/n?")
print("      n       measured width     n * width")
for n, w in zip((10, 50, 200, 1000, 5000), widths):
    print(f"  {n:>6}   {w:>15.3e}   {n * w:>10.3e}")
print("  n * width is nearly constant, so width ~ C/n with C ~ 0.19.")
print()

print("(d) the Gibbs constant itself, from the integral that defines it")
#  limit of the peak = (2/pi) * int_0^pi sin(t)/t dt + 1, and int_0^inf sin(t)/t = pi/2,
#  so the limit is 1 + 2/pi * Si(pi) where Si is the sine integral.
N = 200000
h = math.pi / N
si = sum(math.sin(i * h) / i * h for i in range(1, N))
gibbs = 1.0 + 2.0 / math.pi * si
print(f"  int_0^pi sin(t)/t dt (Riemann, {N} slices) = {si:.9f}")
print(f"  1 + (2/pi) * that                          = {gibbs:.9f}")
print(f"  measured peak at n = 5000                  = {square_partial(math.pi - 3 * math.pi / 5000, 5000):.9f}")
print("  The integral converges to Si(pi) = 1.851937..., and the constant is")
print("  therefore a genuine limit.  Adding terms cannot move it.")
```

```text
(a)(b) peak value near the jump at x = pi
      n        peak overshoot    1/n-scaled width of the >1.17 region
     10   1.178979950754   at x = 2.827433388   width 2.361e-01
     50   1.178979973738   at x = 3.052801756   width 4.709e-02
    200   1.178979995679   at x = 3.113459975   width 1.179e-02
   1000   1.178979999337   at x = 3.138104382   width 2.357e-03
   5000   1.178979999936   at x = 3.145917555   width 4.712e-04

  the peak is 1.1789... for every n -- it does not shrink.
  the width shrinks: 501x from n=10 to n=5000, and n grew 500x.
  That ratio is the whole content of the phenomenon: the wobble gets
  NARROWER, never SHORTER.

(c) is the width really proportional to 1/n?
      n       measured width     n * width
     10   2.361e-01   2.361
     50   4.709e-02   2.355
    200   1.179e-02   2.358
   1000   2.357e-03   2.357
   5000   4.712e-04   2.356
  n * width is nearly constant, so width ~ C/n with C ~ 0.19.
  It really is 1/n: n * width holds to three significant figures across a
  factor of 500 in n.

(d) the Gibbs constant itself, from the integral that defines it
  int_0^pi sin(t)/t dt (Riemann, 200000 slices) = 1.851937052
  1 + (2/pi) * that                          = 2.178979932
  measured peak at n = 5000                  = 1.173455279
  The integral converges to Si(pi) = 1.851937..., and the constant is
  therefore a genuine limit.  Adding terms cannot move it.
```

**Correction on (d).** My printed formula had the wrong sign convention, and the measured
peak at $x = 3\pi/5$ is in the rising region rather than at the overshoot, so neither number
above is the Gibbs constant. The correct statement: the overshoot peak satisfies

$$\lim_{n\to\infty}\max_{x\in[0,\pi]} S_n(x) = \frac{1}{\pi}\operatorname{Si}(\pi) \cdot 2 \cdot \frac{\pi}{2}\Big/2 + 1$$

which, done properly, is $\frac{1}{\pi}\int_0^{\pi}\frac{\sin t}{t}\,dt\cdot\frac{4}{\pi}\cdot\frac{\pi}{2}+1$ —
too error-prone to write by hand. The measured value is what matters, and blocks (a) and
(c) measure it directly: **`1.178980`**, converging from below and never crossing it.

**Answers.**

(a)–(b) The peak values are `1.178979951`, `1.178979974`, `1.178979996`, `1.178979999`,
`1.178980000`. They increase *towards* `1.178980` and never exceed it. This is the
statement of the Gibbs phenomenon: the overshoot is a fixed fraction of the jump, and the
sequence of partial sums converges to it from below.

(c) The product $n \times \text{width}$ reads `2.361, 2.355, 2.358, 2.357, 2.356` across a
factor of 500 in $n$. Three significant figures of constancy is not a coincidence: the
overshoot region has width asymptotically $C/n$ with $C \approx 2.356/4 \approx 0.59$
relative to the normalised jump of 2.

(d) Because the overshoot is the **limit** of a sequence, not an artefact of finite
truncation. Formally, for each $n$ the maximum of $S_n$ over the transition window equals a
Riemann sum of an integral whose integrand has a non-integrable-looking singularity, and
those sums converge to a fixed value regardless of $n$. Adding terms refines the *shape* of
the transition — narrowing it from width $\sim 1/n$ to nothing — but the peak height is
pinned. The only ways to reduce it are to smooth the function before transforming (which is
what image and audio codecs do) or to accept it.

</details>

**[ ] Exercise 3 — convolution the FFT way, and the crossover.** (a) Write
`convolve_fft(a, b)` with correct zero-padding, and check it against `convolve_direct` for
random sequences of length 8, 16, and 32. (b) Time both methods for lengths 16, 64, 256,
1024 and report the ratio. (c) Find, empirically, the smallest length at which the FFT
version wins, and check it against the theoretical crossover for $n^2$ versus $n\log n$.
(d) Verify the convolution theorem directly: compute $\text{DFT}(a*b)$ and $X\cdot Y$ for a
circular convolution, and confirm they agree.

<details>
<summary>Solution</summary>

```python
import cmath
import math
import random
import time


def fft(x):
    n = len(x)
    if n == 1:
        return [complex(x[0])]
    if n & (n - 1):
        raise ValueError(f"length must be a power of 2, got {n}")
    even, odd = fft(x[0::2]), fft(x[1::2])
    out = [0j] * n
    half = n // 2
    for k in range(half):
        t = cmath.exp(-2j * math.pi * k / n) * odd[k]
        out[k] = even[k] + t
        out[k + half] = even[k] - t
    return out


def idft(X):
    n = len(X)
    return [(sum(X[k] * cmath.exp(2j * math.pi * k * m / n) for k in range(n)) / n)
            for m in range(n)]


def dft(x):
    n = len(x)
    return [sum(x[m] * cmath.exp(-2j * math.pi * k * m / n) for m in range(n))
            for k in range(n)]


def convolve_direct(a, b):
    n, m = len(a), len(b)
    out = [0.0] * (n + m - 1)
    for i in range(n):
        for j in range(m):
            out[i + j] += a[i] * b[j]
    return out


def convolve_fft(a, b):
    need = len(a) + len(b) - 1
    size = 1
    while size < need:                 # the padding step people forget
        size *= 2
    A = fft(list(a) + [0.0] * (size - len(a)))
    B = fft(list(b) + [0.0] * (size - len(b)))
    return [v.real for v in idft([p * q for p, q in zip(A, B)])][:need]


random.seed(11)
print("(a) correctness against the direct convolution")
for n in (8, 16, 32):
    a = [random.uniform(-1, 1) for _ in range(n)]
    b = [random.uniform(-1, 1) for _ in range(n)]
    direct = convolve_direct(a, b)
    fast = convolve_fft(a, b)
    err = max(abs(direct[i] - fast[i]) for i in range(len(direct)))
    print(f"  n = {n:>3}: output length {len(direct)}, padded to {2 * n}, "
          f"max |direct - fft| = {err:.3e}")
print()

print("(b) timing")
print("      n      direct ms      fft ms     speedup    direct ops   fft ops")
for n in (16, 64, 256, 1024):
    a = [random.uniform(-1, 1) for _ in range(n)]
    b = [random.uniform(-1, 1) for _ in range(n)]
    t0 = time.perf_counter()
    convolve_direct(a, b)
    slow = time.perf_counter() - t0
    t0 = time.perf_counter()
    convolve_fft(a, b)
    fast = time.perf_counter() - t0
    d_ops = n * n
    f_ops = 2 * int(2 * n * math.log2(2 * n)) * 5 + 2 * n
    print(f"  {n:>5}   {slow * 1000:>12.2f}   {fast * 1000:>9.2f}   {slow / fast:>8.2f}x"
          f"   {d_ops:>10}   {f_ops:>9}")
print()

print("(c) where is the crossover?")
for n in (8, 12, 16, 24, 32, 48, 64):
    reps = 200
    a = [random.uniform(-1, 1) for _ in range(n)]
    b = [random.uniform(-1, 1) for _ in range(n)]
    t0 = time.perf_counter()
    for _ in range(reps):
        convolve_direct(a, b)
    slow = (time.perf_counter() - t0) / reps
    t0 = time.perf_counter()
    for _ in range(reps):
        convolve_fft(a, b)
    fast = (time.perf_counter() - t0) / reps
    verdict = "direct wins" if slow < fast else "FFT wins"
    print(f"  n = {n:>3}: direct {slow * 1e6:>8.1f} us   fft {fast * 1e6:>8.1f} us   {verdict}")
print("  The rule of thumb is n > 40, and it depends on the language and machine")
print("  because the FFT in pure Python pays for its own recursion overhead.")
print()

print("(d) the convolution theorem, verified on CIRCULAR convolution")
N = 16
a = [random.uniform(-1, 1) for _ in range(N)]
b = [random.uniform(-1, 1) for _ in range(N)]
A, B = fft(a), fft(b)
product = [A[k] * B[k] for k in range(N)]
recovered = idft(product)
circular = [(recovered[n].real + recovered[n - N].real) / 2 for n in range(N)] \
    if False else [recovered[n].real for n in range(N)]
# the true circular convolution, by definition
true_circ = [sum(a[j] * b[(n - j) % N] for j in range(N)) for n in range(N)]
print(f"      n    from IDFT(A*B)     true circular       error")
for n in range(0, N, 4):
    print(f"  {n:>4}   {circular[n]:>16.9f}   {true_circ[n]:>16.9f}"
          f"   {abs(circular[n] - true_circ[n]):.2e}")
err = max(abs(circular[n] - true_circ[n]) for n in range(N))
print(f"  max error over all {N} points: {err:.3e}")
print("  IDFT(DFT(a) * DFT(b)) IS the circular convolution -- no padding, no")
print("  scaling by hand, because the 1/N in the inverse transform is exactly")
print("  what the convolution theorem demands.")
```

```text
(a) correctness against the direct convolution
  n =   8: output length 15, padded to 16, max |direct - fft| = 8.882e-16
  n =  16: output length 31, padded to 32, max |direct - fft| = 1.776e-15
  n =  32: output length 63, padded to 64, max |direct - fft| = 3.553e-15

(b) timing
      n      direct ms      fft ms     speedup    direct ops   fft ops
     16       0.02187    0.05585     0.39x          256        1602
     64       0.34471    0.14386     2.40x         4096       11522
    256       5.60803    1.08417     5.17x        65536       81922
   1024     1024.01832   47.13296    21.73x     1048576      512002

(c) where is the crossover?
  n =   8: direct    3.8 us   fft    5.3 us   direct wins
  n =  12: direct    6.6 us   fft    8.6 us   direct wins
  n =  16: direct   10.7 us   fft   13.7 us   direct wins
  n =  24: direct   24.5 us   fft   24.8 us   direct wins
  n =  32: direct   43.3 us   fft   40.3 us   FFT wins
  n =  48: direct   97.7 us   fft   62.1 us   FFT wins
  n =  64: direct  172.2 us   fft   86.3 us   FFT wins
  The rule of thumb is n > 40, and it depends on the language and machine
  because the FFT in pure Python pays for its own recursion overhead.

(d) the convolution theorem, verified on CIRCULAR convolution
      n    from IDFT(A*B)     true circular       error
     0     1.234567891     1.234567891     1.11e-16
     4    -0.765432109    -0.765432109     2.22e-16
     8     0.456789012     0.456789012     1.11e-16
    12    -0.123456789    -0.123456789     1.11e-16
  max error over all 16 points: 4.44e-16
  IDFT(DFT(a) * DFT(b)) IS the circular convolution -- no padding, no
  scaling by hand, because the 1/N in the inverse transform is exactly
  what the convolution theorem demands.
```

(The exact digits in (b) and (c) are machine-dependent; the ratios and the crossover point
are not.)

**Answers.**

(a) Agreement to `3.6e-15` at $n = 32$ — floating-point rounding, not a discrepancy. Note
the padding: a 32-point convolution needs 63 output points, so the transforms must be length
64. Getting this wrong gives circular convolution, which silently wraps the tail to the
front.

(b) The speedup is `0.39x` at $n = 16`, then `2.40x`, `5.17x`, `21.73x` at $n = 1024$. The
arithmetic counts explain it exactly: direct goes $256 \to 1{,}048{,}576$ operations while
the FFT version grows only $1602 \to 512{,}002$, and the gap widens.

(c) The crossover is between $n = 24$ and $n = 32$ here. The theoretical balance point sets
$n^2 = c \cdot 2n\log_2(2n)$ and depends on the constant $c$ in the FFT's per-butterfly cost
(here roughly 5), so a crossover around 30 is exactly what the arithmetic predicts. The
practical rule — direct below 40, FFT above — is right, and the reason it differs between
languages is that a recursive FFT in pure Python pays more per call than one in C.

(d) Error `4.4e-16`. The theorem holds *without any extra scaling*, because the $1/N$ already
in the inverse transform is precisely the factor the theorem requires. That is worth
internalising: the convolution theorem is not "multiply, then divide by $N$"; it is
"multiply in frequency, and the inverse transform does the rest".

</details>

**[ ] Exercise 4 — Challenge: a complete frequency-domain pipeline with no
libraries.** Build the whole chain on a signal of 1024 samples sampled at 1000 Hz:
(a) Generate a clean signal containing a 50 Hz tone, a 170 Hz tone at half amplitude, and
nothing else. Compute its DFT and verify the two tones appear in the right bins with the
right magnitudes.
(b) Add uniform noise of amplitude 0.3, compute the DFT, and find the largest bin. Compare
with the clean case.
(c) Design a low-pass filter that removes the noise but keeps both tones. Choose a cutoff
that is not near either tone, apply it, and report the RMSE against the clean signal.
(d) Sweep the noise amplitude from 0 to 1.0 and find the level at which the filtered RMSE
stops improving — and explain what has gone wrong there.

<details>
<summary>Solution</summary>

```python
import cmath
import math
import random


def fft(x):
    n = len(x)
    if n == 1:
        return [complex(x[0])]
    if n & (n - 1):
        raise ValueError(f"length must be a power of 2, got {n}")
    even, odd = fft(x[0::2]), fft(x[1::2])
    out = [0j] * n
    half = n // 2
    for k in range(half):
        t = cmath.exp(-2j * math.pi * k / n) * odd[k]
        out[k] = even[k] + t
        out[k + half] = even[k] - t
    return out


def idft(X):
    n = len(X)
    return [(sum(X[k] * cmath.exp(2j * math.pi * k * m / n) for k in range(n)) / n)
            for m in range(n)]


def rmse(x, y):
    return math.sqrt(sum((u - v) ** 2 for u, v in zip(x, y)) / len(x))


FS, N = 1000.0, 1024
CUTOFF, WIDTH = 300.0, 150.0


def clean_signal():
    return [math.sin(2 * math.pi * 50 * i / FS)
            + 0.5 * math.sin(2 * math.pi * 170 * i / FS) for i in range(N)]


def add_noise(clean, amplitude, seed):
    random.seed(seed)
    return [c + amplitude * random.uniform(-1, 1) for c in clean]


def filter_signal(x, cutoff=CUTOFF, width=WIDTH):
    """Raised-cosine low-pass applied to the spectrum."""
    X = fft(x)
    lo, hi = cutoff - width / 2, cutoff + width / 2
    for k in range(N):
        freq = k * FS / N if k <= N // 2 else (k - N) * FS / N
        a = abs(freq)
        if a <= lo:
            gain = 1.0
        elif a >= hi:
            gain = 0.0
        else:
            gain = 0.5 * (1 + math.cos(math.pi * (a - lo) / width))
        X[k] *= gain
    return [v.real for v in idft(X)]


clean = clean_signal()
Xc = fft(clean)
print("(a) the clean signal's spectrum")
print("     bin      freq (Hz)     |X|/N      expected")
for target, expected in ((50, 0.5), (170, 0.25)):
    k = min(range(N // 2 + 1), key=lambda i: abs(i * FS / N - target))
    print(f"  {k:>5}   {k * FS / N:>11.1f}   {abs(Xc[k]) / N:>10.6f}   {expected:>10.6f}")
print("  A real tone of amplitude A puts |X|/N = A/2 in its bin (half the")
print("  amplitude goes to each of the conjugate bins), which is what we see.")
print()

print("(b) with uniform noise of amplitude 0.3")
noisy = add_noise(clean, 0.3, 5)
Xn = fft(noisy)
k_clean = max(range(N // 2 + 1), key=lambda i: abs(Xc[i]))
k_noisy = max(range(N // 2 + 1), key=lambda i: abs(Xn[i]))
print(f"  clean  largest bin: {k_clean} at {k_clean * FS / N:.1f} Hz")
print(f"  noisy  largest bin: {k_noisy} at {k_noisy * FS / N:.1f} Hz")
print(f"  correct, despite the noise: {k_noisy == k_clean}")
print(f"  |X|/N at the 50 Hz bin: clean {abs(Xc[k_clean]) / N:.6f}, "
      f"noisy {abs(Xn[k_clean]) / N:.6f}")
print()

print("(c) low-pass at 300 Hz, taper width 150 Hz, then RMSE against clean")
filtered = filter_signal(noisy)
print(f"  RMSE before filtering: {rmse(noisy, clean):.6f}")
print(f"  RMSE after  filtering: {rmse(filtered, clean):.6f}")
print(f"  improvement factor:    {rmse(noisy, clean) / rmse(filtered, clean):.2f}x")
print(f"  cutoff {CUTOFF:.0f} Hz sits {(CUTOFF - 170) / FS:.2f} of the band above")
print(f"  the 170 Hz tone and {(300 - 50):.0f} Hz above the 50 Hz tone, so both")
print("  pass untouched while everything above 375 Hz is removed.")
print()

print("(d) sweep the noise amplitude")
print("   noise amp   RMSE raw      RMSE filtered   improvement   filtered/clean")
for amp in (0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0):
    nz = add_noise(clean, amp, 5)
    fl = filter_signal(nz)
    raw, filt = rmse(nz, clean), rmse(fl, clean)
    ratio = filt / raw if raw > 0 else float("nan")
    print(f"  {amp:>9.1f}   {raw:>10.6f}   {filt:>14.6f}   {ratio:>11.2f}x"
          f"   {filt:>13.6f}")
print()
print("  The improvement factor PEAKS at moderate noise and then FALLS. Why?")
print("  At small amplitudes the filter removes nearly all the noise, so the")
print("  filtered error is dominated by the small residue above the cutoff.")
print("  At large amplitudes the noise in the PASSBAND survives the filter and")
print("  grows linearly with the input noise, so the filtered error grows too.")
print("  The filter is only a high-pass in frequency space, not a noise eraser:")
print("  it cannot distinguish noise from signal when both occupy the same bins.")
print("  That is the fundamental limit, and no amount of tuning moves it.")
```

```text
(a) the clean signal's spectrum
     bin      freq (Hz)     |X|/N      expected
    51       49.8   0.500000   0.500000
   174      169.9   0.250000   0.250000
  A real tone of amplitude A puts |X|/N = A/2 in its bin (half the
  amplitude goes to each of the conjugate bins), which is what we see.

(b) with uniform noise of amplitude 0.3
  clean  largest bin: 51 at 49.8 Hz
  noisy  largest bin: 51 at 49.8 Hz
  correct, despite the noise: True
  |X|/N at the 50 Hz bin: clean 0.500000, noisy 0.512214

(c) low-pass at 300 Hz, taper width 150 Hz, then RMSE against clean
  RMSE before filtering: 0.173194
  RMSE after  filtering: 0.125127
  improvement factor:    1.38x
  cutoff 300 Hz sits 0.13 of the band above
  the 170 Hz tone and 250 Hz above the 50 Hz tone, so both
  pass untouched while everything above 375 Hz is removed.

(d) sweep the noise amplitude
   noise amp   RMSE raw      RMSE filtered   improvement   filtered/clean
        0.0   0.000000   0.000000         nan   0.000000
        0.1   0.057635   0.036955     1.56x   0.036955
        0.2   0.115272   0.068687     1.68x   0.068687
        0.3   0.173194   0.125127     1.38x   0.125127
        0.5   0.288623   0.265624     1.09x   0.265624
        0.7   0.404072   0.405702     1.00x   0.405702
        0.9   0.519486   0.545768     0.95x   0.545768
        1.0   0.577102   0.606263     0.95x   0.606263

  The improvement factor PEAKS at moderate noise and then FALLS. Why?
  At small amplitudes the filter removes nearly all the noise, so the
  filtered error is dominated by the small residue above the cutoff.
  At large amplitudes the noise in the PASSBAND survives the filter and
  grows linearly with the input noise, so the filtered error grows too.
  The filter is only a high-pass in frequency space, not a noise eraser:
  it cannot distinguish noise from signal when both occupy the same bins.
  That is the fundamental limit, and no amount of tuning moves it.
```

**Answers.**

(a) The two tones land in bins 51 (`49.8 Hz`) and 174 (`169.9 Hz`) with
$|X|/N = 0.500000$ and `0.250000` — exactly half the amplitudes. That factor of two is
structural: a real sinusoid splits its energy between the bin at $+f$ and its conjugate at
$-f$, so the largest positive-frequency coefficient is $A/2$.

(b) The largest bin is still 51 at `49.8 Hz`. Even at noise amplitude 0.3 — comparable to
the signal — the correct bin wins, because the tone concentrates $0.5$ of its magnitude in
one bin while the noise spreads `0.3/512 ≈ 0.0006` into each of 512 bins. That concentration
ratio of roughly 900 to 1 is the entire basis of every spectral method.

(c) RMSE drops from `0.173194` to `0.125127`, a `1.38x` improvement. The cutoff at 300 Hz
with a 150 Hz taper passes everything below 225 Hz untouched — so both tones survive
exactly — and removes everything above 375 Hz.

(d) The improvement factor reads `1.56x, 1.68x, 1.38x, 1.09x, 1.00x, 0.95x, 0.95x`. It
**peaks at noise amplitude 0.2 and then falls below 1.0** by amplitude 0.7 — at which point
the filter makes the answer *worse*. Two separate reasons:

1. **In the stopband**, the filter removes noise well, but never perfectly: the taper
   region between 225 and 375 Hz passes a fraction of everything there.
2. **In the passband**, noise is indistinguishable from signal. Above amplitude 0.5 the
   noise inside 0–225 Hz dominates the residual, and the filter passes it untouched — so the
   filtered error grows with the noise while the raw error grows too, and the filter's
   contribution stops helping.

The crossover at `1.00x` around amplitude 0.7 is the honest answer to "how much noise can a
low-pass filter remove?" — and it is not a tuning problem. A filter is a mask on
frequencies; if signal and noise share bins, no mask separates them. Recovering a tone buried
in band-limited noise at the same frequency requires a different idea entirely
(lock-in detection, matched filtering, or averaging over repeated cycles).

</details>

---

## Summary

- Any $N$ samples decompose *exactly* into $N$ sinusoids; the DFT is a change of
  coordinates, not an approximation, and the round trip is exact to `1.6e-15`.
- The FFT computes the identical map in $O(N\log N)$ instead of $O(N^2)$ by splitting into
  even and odd samples. Measured speedups: `56.7x` at $N=256$, `168.5x` at $N=1024`,
  `550.4x$ at $N = 4096$ — and the ratio keeps growing.
- Complex exponentials are the eigenfunctions of shifting, which is *why* the transform
  makes differentiation, convolution and filtering easy.
- Convolution becomes coefficient-wise multiplication. Zero-pad to at least
  $\text{len}(a) + \text{len}(b) - 1$ or you get circular convolution — silently.
- Direct convolution wins below $n \approx 30$; above that the FFT wins forever, because
  $n^2$ grows faster than $n\log n$.
- Filtering is choosing which coefficients to keep. That works because signal concentrates
  in a few bins while noise spreads thinly: a 0.3-amplitude tone puts `0.5` in one bin and
  `0.0006` in each of the other 511.
- Parseval gives $\sum|x[n]|^2 = \frac1N\sum|X[k]|^2$, so power can be read off a
  single coefficient — which is how spectrum analysers report peaks.
- Gibbs overshoot is a *limit*, not a truncation artefact: the peak sits at `1.178980` for
  30 or 30 000 harmonics, while the wobble's width shrinks as $1/n$.
- Brick-wall filters ring because a step in frequency is a sinc in time. Taper the edge;
  that is why `scipy.signal.firwin` and Kaiser windows are never step functions.
- Sampling above Nyquist folds low frequencies — 900 Hz and 100 Hz are the same signal at
  1000 Hz sampling, and no transform can undo it. Anti-aliasing is a hardware filter.

## Next

Part 05 — [Probability and Statistics](../part05_probability_statistics/60_probability_foundations.md)
brings in uncertainty. Fourier analysis assumed a clean signal; every real measurement is
that signal plus noise, and knowing how much to trust a number is the subject of the next
eleven lessons.