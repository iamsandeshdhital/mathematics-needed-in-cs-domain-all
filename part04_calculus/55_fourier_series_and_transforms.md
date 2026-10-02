# 55 — Fourier Series and Transforms

**Part**: part04_calculus · **Prerequisites**: 54 · **Time**: 40 min

---

## In Plain Words

Sine and cosine waves are the only shapes that repeat perfectly, and that is not
an aesthetic judgement — it is a fact with two parts: two different frequencies
never agree with each other over a full cycle, and differentiating one gives you
another. Almost nothing else has both properties, which is why the whole subject
exists. Because of the first fact, you can take any repeating signal, ask "how
much of this is a slow wave and how much is a slightly faster wave", and get
exact answers with no cross-talk — the list of answers is called the spectrum,
and putting them back together rebuilds the signal exactly. This is the great
counterpart to the [Taylor series](54_taylor_series.md): Taylor describes a
function by how fast it changes, Fourier describes it by what it is made of. On a
computer you work with a finite list of samples instead, the discrete version of
the same idea takes a suspicious number of multiplications, and rearranging that
formula to need only a small fraction of the work — the fast Fourier transform —
is one of the great results of numerical computing. Once samples-to-frequencies
is cheap, a lot of operations become trivial: mixing two signals turns into
multiplying their spectra number by number, and removing an unwanted frequency
turns into deleting a number.

---

## Why Computer Science Cares

- **Convolution.** Sliding a filter over a signal, cross-correlating two
  sequences, computing the likelihood of every alignment of two files,
  multiplying polynomials — all of these are convolutions, and all of them are
  quadratic as written. `numpy.fft.convolve` (which dispatches to
  `scipy.signal.fftconvolve` for large inputs) exists only because of the
  convolution theorem. The same theorem computes the running cross-correlation
  behind template matching in OpenCV and the `im2col` step in convolutional
  neural networks.
- **MP3, AAC, Opus, and every audio and video codec.** A perceptual codec
  transforms a block of samples, keeps only the coefficients a human ear cannot
  hear, and transforms back. The transform underneath is the DFT, in its
  windowed real-valued form (MDCT). The reason codecs work at all is the
  observation that musical energy is concentrated in a few frequency bins.
- **Image and video compression.** JPEG applies a two-dimensional DCT — the
  cosine transform — to 8×8 blocks and quantises the coefficients. `scipy.fft.dctn`
  and the `libjpeg` implementation are the same mathematics. The visible
  blocking artefacts come straight from the Gibbs ringing in the plots below.
- **Filtering and denoising.** A notch filter for mains hum, a low-pass for
  sensor noise, a Wiener filter for a blurred photograph: all are "multiply the
  spectrum by a transfer function". `scipy.signal.filtfilt`, `scipy.signal.wiener`
  and `skimage.restoration` are three spellings of $Y[k] = H[k]X[k]$.
- **Spectra in engineering.** `scipy.signal.welch`, vibration analysis of
  machines, ECG/EEG analysis in `mne`, and the `torchaudio` transforms all
  return a spectrum. Reading a spectrum correctly — knowing that bin $k$ means
  $kf_s/N$ hertz, and that a real signal's second half is a mirror — is a
  required skill.
- **The FFT is the reason `$O(n^2)$` algorithms lose.** The transform is
  $\Theta(n^2)$ as written and $\Theta(n\log n)$ after Cooley and Tukey. The
  lesson's own counts: at $n = 2^{20}$, $1{,}099{,}511{,}627{,}776$ complex
  multiplications against $10{,}485{,}760$. Every fast transform in every
  library is a tuned descendant of the twenty lines below.
- **Partial differential equations and physics.** Finite-difference
  discretisation of the heat equation gives an update that is a convolution
  with a kernel, solved by transforming once and multiplying. FFT methods are
  the standard way to do spectral, acoustics and image simulations.

---

## The Formal Version

Throughout, $N$ is the number of samples, $n$ and $k$ index time and frequency,
$f_s$ is the sample rate in samples per second, and $\mathbb{C}$ is the complex
numbers. See [SYMBOLS.md](../SYMBOLS.md).

**Definition (Euler's formula).** For every real $\theta$,

$$e^{i\theta} = \cos\theta + i\sin\theta,\qquad e^{-i\theta} = \cos\theta - i\sin\theta.$$

*Explanation.* This is the bridge. A complex exponential is one object; a
cosine and a sine are its real and imaginary parts. Everything below is easier
written with one exponential than with two trigonometric functions, which is why
the DFT is a sum over $e^{\cdot}$ and not a pair of sums.

**Definition (Orthogonality of the trigonometric system).** Let $T > 0$ and let
$\omega_k = 2\pi k/T$. Then for $k, m \ge 1$,

$$\int_0^T \cos(\omega_k t)\cos(\omega_m t)\,dt = \begin{cases} T/2 & k = m \\ 0 & k \ne m,\end{cases}
\quad \int_0^T \sin(\omega_k t)\sin(\omega_m t)\,dt = \begin{cases} T/2 & k = m \\ 0 & k \ne m,\end{cases}$$

and every mixed integral $\int_0^T \cos(\omega_k t)\sin(\omega_m t)\,dt$ and
non-constant $\int_0^T\cos(\omega_k t)\,dt$, $\int_0^T \sin(\omega_k t)\,dt$
is zero.

*Explanation.* These are the *only* functions in common use that are mutually
orthogonal over a whole period, and orthogonality is what makes projection
work. Averaging $f(t)\cos(\omega_k t)$ over a period annihilates every component
except the $\cos(\omega_k t)$ component, which is multiplied by $T/2$. That is the
entire mechanism of Fourier analysis: a perfect matched filter, obtained by
multiplying and averaging.

**Definition (Fourier series).** If $f$ is $2\pi$-periodic and piecewise smooth,
then

$$f(t) \sim \frac{a_0}{2} + \sum_{k=1}^{\infty}\big(a_k\cos(kt) + b_k\sin(kt)\big),
\quad a_k = \frac{1}{\pi}\int_{-\pi}^{\pi} f(t)\cos(kt)\,dt, \quad
b_k = \frac{1}{\pi}\int_{-\pi}^{\pi} f(t)\sin(kt)\,dt.$$

At a point where $f$ is continuous the series converges to $f(t)$; at a jump of
size $J$ it converges to the midpoint of the two one-sided limits, and no partial
sum ever exceeds either side by more than $0.08949\,J$ (the Gibbs bound).

*Explanation.* The $\sim$ matters: for a discontinuous $f$ the series is not
pointwise equal to $f$ at the jumps, though it still equals $f$ almost
everywhere and in the mean-square sense. A square wave with $J = 2$ overshoots
by `8.95%` of the jump at *every* truncation, forever, as the code below
measures. The ringing only narrows; its height never improves.

**Definition (Complex form).** With $T$ the period, the $T$-periodic complex
Fourier coefficients are

$$c_k = \frac{1}{T}\int_0^{T} f(t)e^{-2\pi i kt/T}\,dt, \qquad
f(t) = \sum_{k\in\mathbb{Z}} c_k e^{2\pi i kt/T}.$$

*Explanation.* The same object with one sum instead of two, because
$e^{i\theta} = \cos\theta + i\sin\theta$ packages the pair. The coefficients are
literally *inner products* against the complex exponentials — the same
orthogonality argument, and the same operation a discrete transform performs.

**Theorem (Parseval, continuous).** If $f$ is square-integrable over a period
then

$$\frac{1}{T}\int_0^T |f(t)|^2\,dt = \sum_{k} |c_k|^2,$$

or in real form, $\frac1\pi\int_{-\pi}^{\pi} f(t)^2 dt = \frac{a_0^2}{2} + \sum_{k\ge1}(a_k^2 + b_k^2)$.

*Explanation.* The transform preserves total energy. A signal that is
concentrated in a few frequency bins has large coefficients there and small ones
elsewhere, and Parseval says the sum of the squares is the same number in both
domains. This is the reason "energy" and "spectrum" are interchangeable
vocabularies, and the reason the sum of squared magnitudes is the natural
measure.

**Definition (Discrete Fourier transform).** For $x = (x_0,\dots,x_{N-1})$ with
$x_n \in \mathbb{C}$,

$$X_k = \sum_{n=0}^{N-1} x_n\,e^{-2\pi i kn/N},\qquad k = 0,\dots,N-1.$$

The inverse, with the sign flipped and one factor of $1/N$:

$$x_n = \frac{1}{N}\sum_{k=0}^{N-1} X_k\,e^{+2\pi i kn/N}.$$

*Explanation.* Replace the integral by a sum over $N$ equally spaced samples
and the exponential by its value at the grid points $kn/N$. The normalisation is
fixed by requiring the round trip to be the identity: no factor on the forward
transform, exactly $1/N$ on the inverse. Any other split is a different
convention, and mixing conventions is a bug you will make.

**Definition (Bin, and its frequency).** $X_k$ is the coefficient of frequency
$f_k = kf_s/N$. Because the sum runs over $k$ and $N-k$ together,
$X_{N-k} = \overline{X_k}$ whenever $x$ is real: the second half of the array is
the mirror image of the first and carries no new information. The frequencies
$f_0,\dots,f_{N/2}$ are the only ones in the data; anything above $f_s/2$ is
not represented at all.

*Explanation.* The frequency spacing $\Delta f = f_s/N$ is set by the length of
the record, not by the sample rate. Double the record and you halve the spacing.
This is the "resolution" of a spectrum, and it is the reason a 4096-point FFT of
one second of audio resolves 0.24 Hz while a 256-point FFT resolves 31 Hz.

**Definition (Spectral leakage).** If $x_n = A\cos(2\pi f_0 n/N + \phi)$ with
$f_0$ an integer, then $X_{f_0} = AN/2$ and every other $X_k$ is zero. If $f_0$
is not an integer, the energy spreads over all bins, decaying like
$1/|\sin(\pi(f_0-k))|$ away from the peak.

*Explanation.* A tone that lands exactly on the grid is representable and
concentrates in one bin. Any other frequency is not, and the transform has to
smear it. The measure of how badly is the *main lobe* width; the cure is either
zero-padding (which does not reduce leakage but makes the lobe narrower in
absolute terms) or a window, which trades a wider main lobe for much lower
sidelobes. The code compares both.

**Theorem (Convolution theorem).** With $(x \circledast y)_m = \sum_{n=0}^{N-1}
x_n y_{(m-n) \bmod N}$ (the *circular* convolution of two $N$-vectors),

$$\text{DFT}(x \circledast y) = X \cdot Y, \qquad
x \circledast y = \text{IDFT}\big(X_k Y_k\big).$$

*Explanation.* Substitute both transforms and interchange the sums; orthogonality
collapses the double sum into a single $N$. The direction that matters is that
the $\Theta(N^2)$ sum becomes $N$ pointwise multiplications, so convolution can
be done in $\Theta(N\log N)$ — three transforms plus a loop. The theorem is an
identity, not an approximation: the code checks the two routes agree to `1e-14`
on random data. Note the word *circular*: linear convolution of lengths $M$ and
$L$ needs at least $M + L - 1$ points, or you must pad, or the tail wraps
around onto the front.

**Definition (Filtering in the frequency domain).** Choose a transfer function
$H = (H_0,\dots,H_{N-1})$ and set

$$Y_k = H_k X_k, \qquad y = \text{IDFT}(Y).$$

For a real input and real $H$, $H_{N-k} = H_k$ preserves conjugacy symmetry, so
$y$ comes back real.

*Explanation.* Convolution with $h$ is multiplication by $H = \text{DFT}(h)$, so
filtering is convolution is a pointwise product. Every frequency-domain filter
is a loop over $N$ numbers. The design questions — what is $H$ — are the
interesting ones, and they are answered in the frequency domain too, where the
answer is a picture.

**Definition (Response of a box average).** For a centred moving average of
width $W$ applied circularly, $h_n = 1/W$ for $|n| \le W/2$, and

$$H_k = \frac{|\sin(\pi k W / N)|}{W\,|\sin(\pi k/N)|},\qquad H_0 = 1.$$

*Explanation.* $H_0 = 1$ because a constant is unchanged by averaging. The
formula tends to $\left|\frac{\sin \pi fW}{W \sin \pi f}\right|$ for small
$f/N$, which is $\approx 1$ for $fW \ll N$ and $\approx 0$ for $fW \gg N$:
averaging neighbours *is* a low-pass filter, and the closed form tells you its
cutoff without running a single sample through it. Wider $W$ means more noise
removed and more signal distorted, and that is the entire trade-off.

**Theorem (FFT recurrence and complexity).** Let $E$ be the transform of the
even-indexed samples and $O$ the transform of the odd-indexed samples, each of
length $N/2$. Then for $k = 0,\dots,N/2-1$,

$$X_k = E_k + e^{-2\pi i k/N} O_k, \qquad X_{k+N/2} = E_k - e^{-2\pi i k/N} O_k.$$

Hence $T(N) = 2T(N/2) + \Theta(N)$, giving

$$T(N) = \Theta(N \log N),$$

with exactly $\frac{N}{2}\log_2 N$ complex multiplications when $N$ is a power of
two.

*Explanation.* The two halves of the answer are not independent: $X_{k+N/2}$
reuses $E_k$ and differs only by the sign of the twiddle term, because
$e^{-2\pi i (k+N/2)/N} = -e^{-2\pi i k/N}$. Halving the problem twice per level
and doing only $\Theta(N)$ combining work per level gives $\log_2 N$ levels at
$\Theta(N)$ cost each. The exact count is the reproducible part of the claim —
see the code, which counts multiplications rather than trusting a clock.

**Theorem (Forward vs central differencing).** For $f$ twice continuously
differentiable and $f'$ Lipschitz with constant $L$ on the interval,

$$\left|\frac{f(x+h)-f(x)}{h} - f'(x)\right| \le \tfrac{1}{2}Lh, \qquad
\left|\frac{f(x+h)-f(x-h)}{2h} - f'(x)\right| \le \tfrac{1}{2}Lh^2.$$

*Explanation.* Same function, same code shape, and the order changes from
$\Theta(h)$ to $\Theta(h^2)$ because the truncation term is halved while the
rounding term doubles. This is the lesson's most transferable fact: the
asymptotic rate is the whole game, and the constant in front of it is a
second-order concern. It is also why the *fast* method is not automatically the
right one at a given step size.

**Theorem (Rounding still bites).** Both formulas are exact in real arithmetic,
but each divides by a power of $h$, so the relative error of a floating-point
difference is bounded below by roughly $\epsilon/h$. The total error of a
central difference is therefore $\Theta(h^2) + \Theta(\epsilon/h)$, minimised at
$h \approx \epsilon^{1/3}$, giving an achievable accuracy of $\Theta(\epsilon^{2/3})$.

*Explanation.* Drive $h$ to $10^{-12}$ and the truncation term vanishes, but
$rounding takes over: the two samples you subtract differ by about $10^{-4}$ of
their own size. This is the same wall as
[Lesson 54](54_taylor_series.md) hit with `1 - exp(-x)`, reached from the other
direction. Optimal $h$ for forward differences is $\Theta(\epsilon^{1/2})$ with
accuracy $\Theta(\epsilon^{1/2})$; central gains a factor $\epsilon^{1/6}$.

---

## Formula Sheet

`$N$` is the number of samples, `$n \in \{0,\dots,N-1\}$` the time index, `$k$` the
frequency index, `$f_s$` the sample rate in samples per second, `$T$` the period
of a continuous signal, `$W$` a filter width, and `$\epsilon \approx 2.22\times10^{-16}$`
the double-precision unit roundoff. `$i$` is the imaginary unit.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$e^{i\theta}$` | `$\cos\theta + i\sin\theta$` | one complex exponential is a cosine plus a sine | turning two trig sums into one; the reason the DFT is written with exponentials |
| `$\omega_k$`, `$\omega_0$` | `$\omega_0 = 2\pi/T$`, `$\omega_k = k\omega_0$` | angular frequencies, the spacing is `$\omega_0$` | harmonic analysis of a continuous periodic signal |
| orthogonality | `$\int_0^T\cos(\omega_k t)\cos(\omega_m t)\,dt = T/2$` if `$k=m$`, else `0` | different frequencies cancel exactly over a period | the whole justification for Fourier coefficients being exact projections; **valid for `$k,m\ge1$`, period `$T$`** |
| `$\int_0^T\sin(\omega_k t)\,dt = \int_0^T\cos(\omega_k t)\,dt = 0$` for `$k\ge1$` | zero mean of a non-constant sinusoid | averaging removes it | detecting a DC offset separately from real content |
| Fourier series | `$f(t)\sim\frac{a_0}{2}+\sum_{k\ge1}(a_k\cos kt + b_k\sin kt)$` | every periodic function is a sum of sinusoids | `$\sim$` not `=`: **converges to `$f(t)$` only where `$f$` is continuous** |
| `$a_k$` | `$\frac{1}{\pi}\int_{-\pi}^{\pi} f(t)\cos(kt)\,dt$` | how much cosine-of-frequency-`$k$` is in `$f$` | need `$2\pi$`-periodicity; the general form carries `$\frac{2}{T}$` |
| `$b_k$` | `$\frac{1}{\pi}\int_{-\pi}^{\pi} f(t)\sin(kt)\,dt$` | how much sine-of-frequency-`$k$` is in `$f$` | an **odd** `$f$` has `$a_k=0` for every `$k$` |
| `$c_k$` | `$\frac{1}{T}\int_0^{T}f(t)e^{-2\pi i kt/T}\,dt$` | the same information, packed into one complex number | the compact form; `$a_k = 2\operatorname{Re} c_k$`, `$b_k = -2\operatorname{Im} c_k$` |
| Parseval (continuous) | `$\frac1T\int_0^T\lvert f\rvert^2 dt = \sum_k\lvert c_k\rvert^2$` | energy is the same in both domains | deciding whether a truncated series kept enough of the signal; **needs `$f$` square-integrable** |
| square wave coefficients | `$a_k=0`, `$b_k=\frac{4}{\pi k}` for odd `$k$`, `0` for even | a jump discontinuity gives a `1/k` tail | the canonical example of slow convergence; the source of Gibbs ringing |
| Gibbs bound | overshoot `$\le 0.08949\,J$` for every partial sum, where `$J$ is the jump size | ringing height never shrinks, only its width (`$\Theta(1/N)$) | explaining why image codecs produce ringing near sharp edges; **not a rounding artefact** |
| DFT | `$X_k = \sum_{n=0}^{N-1} x_n e^{-2\pi i kn/N}$` | how much of each frequency is in the signal | the workhorse; **no `1/N` on the forward transform** |
| inverse DFT | `$x_n = \frac{1}{N}\sum_{k=0}^{N-1} X_k e^{2\pi i kn/N}$` | put the frequencies back | **exactly one factor `1/N`, in the inverse** — this is the normalisation convention |
| FFT butterfly | `$X_k = E_k + e^{-2\pi ik/N}O_k$`, `$X_{k+N/2}=E_k - e^{-2\pi ik/N}O_k$` | combine two half-size transforms with twiddle factors | implementing the transform; **needs `$N$` a power of two for the plain radix-2 version** |
| `$E_k$`, `$O_k$` | transforms of `$(x_0,x_2,\dots)$` and `$(x_1,x_3,\dots)$` | even-indexed and odd-indexed halves | the recursive step |
| FFT recurrence | `$T(N) = 2T(N/2)+\Theta(N)=\Theta(N\log N)$` | halve twice, combine in linear work, for `$\log_2 N$` levels | the complexity claim; compare the naive `$T(N)=\Theta(N^2)$` |
| exact FFT work | `$\frac{N}{2}\log_2 N$` complex multiplications | `1024` at `N=1024`, `10{,}485{,}760` at `N=2^{20}` | the reproducible part of "FFT is faster"; **only for `$N$` a power of two** |
| naive DFT work | `$N^2$` complex multiplications | `1{,}099{,}511{,}627{,}776` at `$N=2^{20}$` | the cost the FFT exists to avoid |
| bin → frequency | `$f_k = kf_s/N$ | bin number times record length inverse | reading a spectrum; a `100` Hz tone at `f_s=8000`, `N=256` is in bin `3.20` |
| frequency spacing | `$\Delta f = f_s/N$ | resolution | longer record, finer spectrum; double `N`, halve `$\Delta f$` |
| Nyquist ceiling | `$f_{N/2} = f_s/2$ | the highest frequency present in the data | anything faster has aliased onto a low frequency before the transform ran |
| conjugacy symmetry | `$X_{N-k} = \overline{X_k}$ for real `$x$ | the top half mirrors the bottom half | **filter both halves**; zeroing one alone returns a complex signal; why `numpy.fft.rfft` returns `N/2+1` values |
| linear convolution | `$(x*y)_m=\sum_n x_n y_{m-n}`, length `M+L-1` | slide one over the other, no wrapping | always what you want in practice |
| circular convolution | `$(x\circledast y)_m=\sum_{n=0}^{N-1}x_n y_{(m-n)\bmod N}` | same, but the indices wrap | what `DFT` multiplication actually computes |
| zero-padding rule | `N \ge M + L - 1` | pad **both** inputs to at least the sum of lengths minus one | turning circular into linear; the single most common FFT bug |
| convolution theorem | `$\text{DFT}(x\circledast y)=X_kY_k$` | multiply numbers instead of summing pairs | makes convolution `$\Theta(N\log N)$` instead of `$\Theta(N^2)$` |
| frequency filtering | `$Y_k = H_kX_k$ | scale each frequency by a chosen gain | low-pass, high-pass, notch, Wiener; a three-line loop |
| box response | `$H_k=\frac{\lvert\sin(\pi kW/N)\rvert}{W\lvert\sin(\pi k/N)\rvert}$, `$H_0=1$` | moving average is a low-pass with a closed-form cutoff | designing a smoother without running it; **circular (wrapped) averaging** |
| noise reduction | improvement `$\approx\sqrt{\frac{N/2-1}{\text{cut}}}$` for white noise | delete a fraction of the bins, lose that fraction of the noise energy | predicting whether a low-pass is worth it *before* trying cutoffs; `$\sqrt{127/40}=1.78$` measured `1.74` |
| forward difference | `$\frac{f(x+h)-f(x)}{h}=f'(x)+O(h)$` | one-sided estimate, error `$\Theta(h)$` | cheap derivative, big step; **truncation `$\Theta(h)`, rounding `$\Theta(\epsilon/h)$` |
| central difference | `$\frac{f(x+h)-f(x-h)}{2h}=f'(x)+O(h^2)$` | two-sided estimate, error `$\Theta(h^2)$` | gradients and Jacobians; costs one extra function call |
| optimal forward step | `$h\approx\sqrt{\epsilon}$`, error `$\approx\epsilon^{1/2}\approx 1.5\times10^{-8}$` for `$\epsilon=2.22\times10^{-16}$` | the best a one-sided difference can do in double precision | stopping a gradient-descent line search; **not the same as "use small h"** |
| optimal central step | `$h\approx\epsilon^{1/3}\approx 6.1\times10^{-6}$`, error `$\approx\epsilon^{2/3}\approx 3.7\times10^{-11}$` | two-sided buys a factor `$\epsilon^{1/6}\approx 24$` | the default for numerical Jacobians (`scipy.optimize._numdiff.approx_derivative` uses exactly this) |

---

## Worked Example

Take the eight samples

$$x = [1,\; 2,\; 3,\; 4,\; 4,\; 3,\; 2,\; 1],\qquad N = 8,$$

and find the 8-point DFT by hand, then find it again with the FFT recursion, then
check Parseval.

### Step 1 — The definition, one row at a time

$$X_k = \sum_{n=0}^{7} x_n\,e^{-2\pi i k n/8}.$$

**Row $k = 0$** (the DC component, the plain sum of the samples):

$$X_0 = 1 + 2 + 3 + 4 + 4 + 3 + 2 + 1 = 20.$$

**Row $k = 4$** (the alternating sum, since $e^{-2\pi i \cdot 4 n/8} = (-1)^n$):

$$X_4 = 1 - 2 + 3 - 4 + 4 - 3 + 2 - 1 = 0.$$

**Row $k = 2$** (since $e^{-2\pi i \cdot 2n/8} = e^{-i\pi n/2}$ the real parts
are $1,0,-1,0,1,0,-1,0$ and the imaginary parts are $0,-1,0,1,0,-1,0,1$):

$$X_2 = (1 - 3 + 4 - 2) + i(0 - 2 + 4 - 3 + 0 - 2 + 0 + 1) = 0 + 0i.$$

**Why rows 2 and 4 vanish.** $x$ is symmetric about its centre, $x_n = x_{7-n}$.
A symmetric real sequence has a *purely real* spectrum, and here two of those real
values happen to be zero. The symmetry argument is worth doing every time: it
halves the arithmetic and it is a correctness check on your indices.

**Row $k = 1$** (the one that does not cancel). The angles are
$0, \pi/4, \pi/2, 3\pi/4, \pi, 5\pi/4, 3\pi/2, 7\pi/4$, so

$$\operatorname{Re} X_1 = 1 + 2\!\cdot\!0.70711 + 0 - 4\!\cdot\!0.70711 - 4 - 3\!\cdot\!0.70711 + 0 + 1\!\cdot\!0.70711 = -5.82843,$$
$$\operatorname{Im} X_1 = -\big(0 + 2(0.70711) + 3(1) + 4(0.70711) + 0 - 3(0.70711) - 2(1) - 0.70711\big) = -2.41421.$$

So

$$X_1 = -(3 + 2\sqrt2) - (1+\sqrt2)i,\qquad |X_1| = \sqrt{20 + 14\sqrt2} = 6.308644,$$
$$\arg X_1 = -\tfrac{7}{8}\pi \quad (\text{printed as } -0.8750\text{ in units of }\pi).$$

Rows 5, 6, 7 follow by conjugacy: $X_{8-k} = \overline{X_k}$.

| $k$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\operatorname{Re} X_k$ | 20 | −5.82843 | 0 | −0.17157 | 0 | −0.17157 | 0 | −5.82843 |
| $\operatorname{Im} X_k$ | 0 | −2.41421 | 0 | −0.41421 | 0 | 0.41421 | 0 | 2.41421 |
| $\lvert X_k\rvert$ | 20 | 6.308644 | 0 | 0.448342 | 0 | 0.448342 | 0 | 6.308644 |

### Step 2 — The same thing by the FFT recursion, with every intermediate value

Split into even and odd indices:

$$[x_0,x_2,x_4,x_6] = [1,3,4,2], \qquad [x_1,x_3,x_5,x_7] = [2,4,3,1].$$

**Level 2 (2-point transforms).** A 2-point DFT is just a sum and a difference:
$[a,b] \mapsto [a+b,\; a-b]$.

| pair | sum | difference |
| --- | --- | --- |
| $[1,4]$ (from the evens of the evens) | 5 | −3 |
| $[3,2]$ (from the odds of the evens) | 5 | 1 |
| $[3,4]$ (from the evens of the odds) | 7 | −1 |
| $[4,1]$ (from the odds of the odds) | 5 | 3 |
| $[2,3]$ (evens of the odd-index list) | 5 | −1 |
| $[4,1]$ (odds of the odd-index list) | 5 | 3 |
| $[4,2]$ (evens of the odd-index list) | 6 | 2 |
| $[3,1]$ (odds of the odd-index list) | 4 | 2 |

**Level 1 (4-point transforms).** Combine pairs with the 4-point twiddle
$e^{-2\pi i/4} = -i$:

$$E = \text{DFT}_4[1,3,4,2] = \big[\,5 + 5,\;\; -3 + (-i)(1),\;\; 5 - 5,\;\; -3 - (-i)(1)\,\big] = [10,\; -3 - i,\; 0,\; -3 + i],$$
$$O = \text{DFT}_4[2,4,3,1] = \big[\,5 + 5,\;\; -1 + (-i)(3),\;\; 5 - 5,\;\; -1 - (-i)(3)\,\big] = [10,\; -1 - 3i,\; 0,\; -1 + 3i].$$

**Level 0 (8-point transform).** The 8-point twiddles are
$w_0 = 1$, $w_1 = \tfrac{1}{\sqrt2} - \tfrac{i}{\sqrt2}$, $w_2 = -i$,
$w_3 = -\tfrac{1}{\sqrt2} - \tfrac{i}{\sqrt2}$. Combining:

$$X_0 = E_0 + w_0O_0 = 10 + 10 = 20, \qquad X_4 = E_0 - w_0O_0 = 0,$$
$$X_1 = (-3 - i) + w_1(-1 - 3i) = (-3-i) + (-2.82843 - 1.41421i) = -5.82843 - 2.41421i,$$
$$X_5 = (-3 - i) - w_1(-1-3i) = -0.17157 + 0.41421i,$$
$$X_2 = 0 + (-i)\cdot 0 = 0, \qquad X_6 = 0,$$
$$X_3 = (-3+i) + w_3(-1+3i) = (-3+i) + (2.82843 - 1.41421i) = -0.17157 - 0.41421i,$$
$$X_7 = (-3+i) - w_3(-1+3i) = -5.82843 + 2.41421i.$$

Every value matches the direct computation. The code confirms this with
`max |DFT - FFT| = 7.700e-15` at $N = 8$.

**What the recursion bought.** Direct: $8^2 = 64$ complex multiplications.
FFT: $\tfrac82\log_2 8 = 4 \cdot 3 = 12$. At $N = 1024$ the same ratio is
$1{,}048{,}576$ against $5120$, a factor of 205.

### Step 3 — Parseval as a check

$$\sum_{n} x_n^2 = 1+4+9+16+16+9+4+1 = 60,$$
$$\frac{1}{8}\sum_k \lvert X_k\rvert^2 = \frac{1}{8}\big(400 + 39.799 + 0 + 0.201 + 0 + 0.201 + 0 + 39.799\big) = \frac{480}{8} = 60.$$

Both are 60. The code prints `59.99999999999999` against `60.0`, which is
rounding and nothing else. When a transform and an identity disagree, run
Parseval first: it separates "my indices are wrong" from "my arithmetic is
wrong" in one line.

### Step 4 — Reading the spectrum

Bin 0 holds 20, which is the sum of the samples: the mean level. Bins 1 and 7
hold magnitude 6.3: the slowest oscillation present. Bins 2, 4 and 6 are zero:
this signal has no content at a quarter, a half, or three quarters of the
record. Bins 3 and 5 hold 0.45: a small fast wiggle. If this were audio sampled
at 8000 Hz, bin 1 would be 1000 Hz, bin 3 would be 3000 Hz, and the transform
could not tell you anything at all about 440 Hz — that is bin 0.14, and the
spectrum of this eight-sample record simply does not resolve it.

---

## Runnable Code

### Block 1: orthogonality, the coefficients, and the Gibbs phenomenon

```python
import math

TAU = 2.0 * math.pi

print("=== Why sine and cosine are the special ones ===")
#  Two facts, both provable in a line, that almost nothing else has.
#   (1) ORTHOGONALITY over a whole period: the inner product of two different
#       frequencies is zero, so averaging over a period picks out one
#       frequency and annihilates every other one.
#   (2) DERIVATION maps them into each other, scaling by the frequency:
#       d/dt sin(w t) = w cos(w t).
print("     w1   w2   int of sin(w1 t) sin(w2 t) over [0, 2pi]   exact    err")
for w1, w2 in ((1, 1), (1, 2), (1, 3), (2, 3), (3, 3)):
    M = 20000
    h = TAU / M
    total = sum(math.sin(w1 * (i + 0.5) * h) * math.sin(w2 * (i + 0.5) * h)
                for i in range(M)) * h
    exact = math.pi if w1 == w2 else 0.0
    print(f"    {w1:>3}  {w2:>3}   {total:>34.6f}   {exact:>6.3f}   {abs(total - exact):.1e}")
print("  Only the w1 == w2 row survives.  Averaging is therefore a PERFECT")
print("  matched filter, and the Fourier coefficients are just inner products.")
print()

print("=== Fourier coefficients of a square wave, computed by integration ===")
#  f(x) = -1 on (-pi, 0) and +1 on (0, pi), extended with period 2*pi.
#    a_n = (1/pi) int f(x) cos(nx) dx        b_n = (1/pi) int f(x) sin(nx) dx
#  Exact answer:  a_n = 0 for every n,  b_n = 4/(pi*n) for ODD n, 0 for even n.
M = 200000
h = TAU / M
mid = [(i + 0.5) * h - math.pi for i in range(M)]
vals = [(-1.0 if t < 0.0 else 1.0) for t in mid]


def a_coeff(n):
    return sum(f * math.cos(n * t) for t, f in zip(mid, vals)) * h / math.pi


def b_coeff(n):
    return sum(f * math.sin(n * t) for t, f in zip(mid, vals)) * h / math.pi


print("      n   b_n numeric     b_n exact       err       a_n numeric")
for n in range(1, 10):
    bn = b_coeff(n)
    exact = (4.0 / (math.pi * n)) if n % 2 == 1 else 0.0
    print(f"  {n:>4}   {bn:>13.9f}   {exact:>13.9f}   {abs(bn - exact):>9.1e}"
          f"   {a_coeff(n):>12.1e}")
print("  a_n is numerically ZERO for every n: the square wave is odd, and an odd")
print("  function has no cosine content.  The 1e-10 gaps in the b_n column are")
print("  QUADRATURE error in the midpoint rule, not error in the formula -- the")
print("  coefficients themselves are exactly 4/(pi n).  And b_n decays like 1/n,")
print("  and that slow decay is the jump discontinuity, not a defect.")
print()

print("=== Rebuilding the signal from a truncated series: the 1/n tail ===")


def square_series(x, n_terms):
    """b_n = 4/(pi*n) for odd n, a_n = 0.  a0/2 = 0 because f is odd."""
    total = 0.0
    for n in range(1, n_terms + 1, 2):        # even terms are exactly zero
        total += (4.0 / (math.pi * n)) * math.sin(n * x)
    return total


print("       N        value at x = 1.0    true          err        err*N")
for N in (9, 99, 999, 9999, 99999, 999999):
    v = square_series(1.0, N)
    e = abs(v - 1.0)
    print(f"  {N:>7}   {v:>22.12f}   {1.0:>6.1f}   {e:>10.2e}   {e * N:>9.4f}")
print("  err*N settles near 0.7, so the error really is Theta(1/N).  Reaching")
print("  1e-9 at that rate needs about 7e8 terms -- which is exactly why nobody")
print("  evaluates a raw Fourier series at a discontinuity, and why audio codecs")
print("  use windowed MDCT blocks instead.")
print()

print("=== The Gibbs phenomenon: the overshoot does NOT shrink ===")
#  At a jump the series converges to the MIDPOINT of the jump, and the peak
#  overshoot is always about 8.949% of the jump height, for EVERY truncation.
#  Only the width of the overshoot shrinks, like 1/N.
print("       N     max overshoot    % of jump     peak at x     back under 1 at x   N*width")
for N in (51, 201, 801, 3201):
    steps = 20000
    hi = 6.0 * math.pi / N          # the overshoot lives within a few 1/N of x = 0
    peak_i, best = 0, -1e9
    for i in range(1, steps):
        v = square_series(hi * i / steps, N)
        if v > best:
            best, peak_i = v, i
    back = hi
    for i in range(peak_i + 1, steps):      # search FORWARD from the peak
        t = hi * i / steps
        if square_series(t, N) <= 1.0:
            back = t
            break
    width = back - hi * peak_i / steps
    print(f"  {N:>6}   {best - 1.0:>14.5f}   {50.0 * (best - 1.0):>10.4f}"
          f"   {hi * peak_i / steps:>11.6f}   {back:>19.6f}   {N * width:>7.4f}")
print("  The height sits at 8.95% of the 2-unit jump for every N you try, and")
print("  never improves.  N*width converges to about 1.75, so the overshoot only")
print("  narrows, like 1/N.  A genuine limit of the method, not rounding: this is")
print("  why a sharp edge in a signal stays sharp with a visible ring next to it.")
```

Output:

```text
=== Why sine and cosine are the special ones ===
     w1   w2   int of sin(w1 t) sin(w2 t) over [0, 2pi]   exact    err
      1    1                             3.141593    3.142   2.2e-15
      1    2                            -0.000000    0.000   1.9e-16
      1    3                            -0.000000    0.000   1.4e-15
      2    3                             0.000000    0.000   1.3e-16
      3    3                             3.141593    3.142   2.2e-15
  Only the w1 == w2 row survives.  Averaging is therefore a PERFECT
  matched filter, and the Fourier coefficients are just inner products.

=== Fourier coefficients of a square wave, computed by integration ===
      n   b_n numeric     b_n exact       err       a_n numeric
     1     1.273239545     1.273239545     5.2e-11        3.6e-16
     2    -0.000000000     0.000000000     1.5e-16       -7.7e-17
     3     0.424413182     0.424413182     1.6e-10        2.1e-16
     4     0.000000000     0.000000000     3.5e-17        3.4e-17
     5     0.254647909     0.254647909     2.6e-10        4.8e-16
     6     0.000000000     0.000000000     1.5e-16        3.4e-19
     7     0.181891364     0.181891364     3.7e-10        2.6e-16
     8     0.000000000     0.000000000     2.5e-16        9.6e-17
     9     0.141471061     0.141471061     4.7e-10        1.2e-16
  a_n is numerically ZERO for every n: the square wave is odd, and an odd
  function has no cosine content.  The 1e-10 gaps in the b_n column are
  QUADRATURE error in the midpoint rule, not error in the formula -- the
  coefficients themselves are exactly 4/(pi n).  And b_n decays like 1/n,
  and that slow decay is the jump discontinuity, not a defect.

=== Rebuilding the signal from a truncated series: the 1/n tail ===
       N        value at x = 1.0    true          err        err*N
        9           1.064902291262      1.0     6.49e-02      0.5841
       99           0.993501845190      1.0     6.50e-03      0.6433
      999           0.999574127934      1.0     4.26e-04      0.4254
     9999           1.000072037352      1.0     7.20e-05      0.7203
    99999           1.000007560721      1.0     7.56e-06      0.7561
   999999           0.999999291295      1.0     7.09e-07      0.7087
  err*N settles near 0.7, so the error really is Theta(1/N).  Reaching
  1e-9 at that rate needs about 7e8 terms -- which is exactly why nobody
  evaluates a raw Fourier series at a discontinuity, and why audio codecs
  use windowed MDCT blocks instead.

=== The Gibbs phenomenon: the overshoot does NOT shrink ===
       N     max overshoot    % of jump     peak at x     back under 1 at x   N*width
      51          0.17910       8.9552      0.060411              0.094118    1.7191
     201          0.17899       8.9494      0.015553              0.024228    1.7436
     801          0.17898       8.9490      0.003917              0.006103    1.7511
    3201          0.17898       8.9490      0.000981              0.001528    1.7521
  The height sits at 8.95% of the 2-unit jump for every N you try, and
  never improves.  N*width converges to about 1.75, so the overshoot only
  narrows, like 1/N.  A genuine limit of the method, not rounding: this is
  why a sharp edge in a signal stays sharp with a visible ring next to it.
```

Two numbers in that output are worth pausing on. The `err*N` column settles
around `0.7` rather than growing, which is the evidence that the convergence is
exactly $\Theta(1/N)$ and not something faster. And the overshoot column is
`8.9490%` at both $N = 801$ and $N = 3201$: a four-fold increase in work moved
the fifth digit of the overshoot by nothing. If you are reconstructing a sharp
edge and the ringing is still there after quadrupling your resolution, the
ringing is not going away — that is the design, not a bug in your loop.

### Block 2: a from-scratch naive DFT and a from-scratch recursive radix-2 FFT

```python
import math
import time

TAU = 2.0 * math.pi


# ---------------------------------------------------------------- the naive DFT
def dft(x, stats=None):
    """X[k] = sum_n x[n] exp(-2*pi*i*k*n/N), computed as written: Theta(N^2)."""
    N = len(x)
    out = []
    for k in range(N):
        acc = 0j
        for n in range(N):
            angle = -TAU * k * n / N          # Euler: e^{i*angle} = cos + i sin
            acc += x[n] * complex(math.cos(angle), math.sin(angle))
        out.append(acc)
        if stats is not None:
            stats["complex mults"] += N
            stats["trig calls"] += 2 * N
    return out


# ----------------------------------------------------------------- the radix-2 FFT
def fft(x, stats=None):
    """Recursive Cooley-Tukey radix-2 FFT.  len(x) must be a power of two.

    The identity exploited is: an N-point transform of the even-index samples
    plus an N-point transform of the odd-index samples, combined with the right
    twiddle factors, gives the N-point transform of the whole signal.  Two
    problems of size N/2 instead of one of size N: T(N) = 2 T(N/2) + O(N).
    """
    N = len(x)
    if N == 1:
        return list(x)
    if N & (N - 1):
        raise ValueError("radix-2 FFT needs a power of two, got " + str(N))
    even = fft(x[0::2], stats)               # N/2-point transform of x[0], x[2], ...
    odd = fft(x[1::2], stats)                # N/2-point transform of x[1], x[3], ...
    out = [0j] * N
    for k in range(N // 2):
        w = complex(math.cos(-TAU * k / N), math.sin(-TAU * k / N))   # twiddle
        t = w * odd[k]
        out[k] = even[k] + t                # X[k]
        out[k + N // 2] = even[k] - t       # X[k+N/2]; the twiddle at k+N/2 is -w
    if stats is not None:
        stats["complex mults"] += N // 2
        stats["trig calls"] += 2 * (N // 2)
    return out


def idft(X):
    """x[n] = (1/N) sum_k X[k] exp(+2*pi*i*k*n/N).  Naive O(N^2) form."""
    N = len(X)
    out = []
    for n in range(N):
        acc = 0j
        for k in range(N):
            angle = TAU * k * n / N
            acc += X[k] * complex(math.cos(angle), math.sin(angle))
        out.append(acc / N)
    return out


# ------------------------------------------------------------------ a test signal
def test_signal(N):
    """Three clean sinusoids, landing exactly on bins 3, 7 and 20 of an N-point DFT."""
    return [1.0 * math.cos(TAU * 3 * n / N)
            + 0.5 * math.sin(TAU * 7 * n / N)
            + 0.25 * math.cos(TAU * 20 * n / N)
            for n in range(N)]


print("=== The forward transform finds the frequencies, and only those ===")
N = 64
X = dft(test_signal(N))
print(f"  signal: 1.0*cos(3) + 0.5*sin(7) + 0.25*cos(20), sampled at N = {N}")
print("   bin k      |X[k]|    phase/pi    exact |X[k]|  exact phase/pi")
for k, mag, ph in ((3, N / 2.0, 0.0), (7, N / 2.0, 0.5), (20, N / 4.0, 0.0)):
    got_mag = abs(X[k])
    got_ph = math.atan2(X[k].imag, X[k].real) / math.pi
    print(f"    {k:>4}   {got_mag:>9.4f}   {got_ph:>9.4f}   {mag:>10.1f}   {ph:>14.1f}")
loud = [k for k in range(1, N // 2) if abs(X[k]) > 1e-9]
print(f"  every bin with |X[k]| > 1e-9 for 1 <= k < N/2: {loud}")
print("  Three bins out of 31.  A pure tone that lands on the grid puts ALL of")
print("  its energy in ONE bin; a tone that does not land on the grid smears")
print("  across neighbours, and that smearing is spectral leakage.")
print()

print("=== Naive DFT and recursive FFT agree to machine precision ===")
print("      N     max |DFT - FFT|      max |x - IDFT(FFT(x))|")
for N in (8, 16, 64, 256, 1024):
    x = test_signal(N)
    diff = max(abs(p - q) for p, q in zip(dft(x), fft(x)))
    rt = max(abs(p - q) for p, q in zip(x, idft(fft(x))))
    print(f"  {N:>5}   {diff:>18.3e}   {rt:>25.3e}")
print("  Two algorithms for the same object, so they must agree; what is left is")
print("  rounding.  The round trip returning the input is orthogonality in")
print("  disguise: the transform matrix is unitary up to a factor 1/sqrt(N).")
print()

print("=== EXACT operation counts: the complexity claim, counted not timed ===")
print("  Counting is deterministic, unlike a wall clock.  'complex mults' is the")
print("  number of complex multiply-accumulates; 'trig calls' counts cos/sin.")
print("      N   DFT mults   DFT trig   FFT mults   FFT trig   ratio mults   ratio trig")
prev = None
for N in (16, 32, 64, 128, 256, 512, 1024):
    x = test_signal(N)
    sd = {"complex mults": 0, "trig calls": 0}
    sf = {"complex mults": 0, "trig calls": 0}
    dft(x, sd)
    fft(x, sf)
    if prev is None:
        rm = rt = "     -"
    else:
        rm = f"{sd['complex mults'] / prev[0]:>9.2f}x"
        rt = f"{sf['complex mults'] / prev[1]:>9.2f}x"
    print(f"  {N:>5}   {sd['complex mults']:>9}   {sd['trig calls']:>8}"
          f"   {sf['complex mults']:>9}   {sf['trig calls']:>8}   {rm}   {rt}")
    prev = (sd["complex mults"], sf["complex mults"])
print("  DFT mults = N^2 exactly, so every doubling costs exactly 4.00x.")
print("  FFT mults = (N/2)*log2(N), so every doubling costs")
print("     2*(log2(N)+1)/log2(N) = 2.50x at N=16, 2.20x at N=1024, 2.13x at N=16384.")
print("  That is the whole n-vs-n-log-n difference, exactly, with no noise:")
for N in (16, 1024, 16384):
    lg = math.log2(N)
    print(f"     N = {N:>6}: predicted doubling factor = {2 * (lg + 1) / lg:.4f}")
print()
N = 1 << 20
print(f"  At N = 2^20 = {N:,} points the two counts are:")
print(f"     naive DFT : N^2            = {N * N:,} complex multiplications")
print(f"     FFT       : (N/2)*log2(N)  = {(N // 2) * 20:,} complex multiplications")
print(f"     ratio     : N / (2*log2 N) = {N * N / ((N // 2) * 20):,.0f}")
print("  A factor of 104,858 at one million points, and the factor is N/(2 log2 N),")
print("  which grows without bound.  That is the sentence 'the FFT is O(n log n)")
print("  instead of O(n^2)' actually asserting.")
print()

print("=== Projecting to the sizes real systems use, from the COUNTS ===")
print("  A wall clock is not tabulated anywhere in this block: the numbers would")
print("  change when you moved the machine, and a number that changes with the")
print("  machine is not evidence about an algorithm.  Everything below is derived")
print("  arithmetically from the operation counts already measured above.")
print()
print("  The ratio of work is exact:")
for N in (1024, 8192, 65536, 1048576):
    lg = math.log2(N)
    dft_ops = N * N
    fft_ops = (N // 2) * lg
    print(f"    N = {N:>9,}: DFT {dft_ops:>16,}   FFT {int(fft_ops):>13,}   "
          f"ratio {dft_ops / fft_ops:>10,.0f}x")
print()
print("  Projecting seconds needs ONE number from your own machine -- the cost of a")
print("  single complex multiply-accumulate -- and then everything else is arithmetic.")
print("  Take c = 2 ns per complex multiply-accumulate, a mid-range figure for")
print("  interpreted Python, and the projections are:")
print(f"    {'N':>10}   {'naive DFT':>14}   {'FFT':>12}   {'speed-up':>10}   {'predicted':>12}")
c_ns = 2.0
for N in (1024, 8192, 65536, 1048576):
    lg = math.log2(N)
    t_dft = c_ns * 1e-9 * N * N
    t_fft = c_ns * 1e-9 * (N // 2) * lg
    ratio = t_dft / t_fft
    print(f"    {N:>10,}   {t_dft:>11.3f} s   {t_fft:>9.4f} s   {ratio:>8,.0f}x   "
          f"{'yes' if ratio > 100 else 'no':>10}")
print()
print("  The predicted column is the whole argument in one word: at N = 2^20 the")
print("  quadratic route is more than 100x slower, so nobody runs it, and at")
print("  N = 2^16 it is already 2,000x slower.  Change c to 0.5 ns and every number")
print("  moves by a factor of four and the RATIOS do not move at all -- which is")
print("  precisely why the counts are the evidence and the clock is not.")
print()
print("  One caveat worth stating because it is real: the naive loop in this lesson")
print("  calls math.cos and math.sin inside the inner loop, which no serious")
print("  implementation does.  A production quadratic DFT precomputes the twiddle")
print("  table and saves roughly a factor of two, and a good one also uses the")
print("  real-symmetry of real input to halve the work again.  Neither changes the")
print("  class, and both are worth remembering when you read someone else's")
print("  quadratic implementation and wonder why it is faster than yours.")

```

Output:

```text
=== The forward transform finds the frequencies, and only those ===
  signal: 1.0*cos(3) + 0.5*sin(7) + 0.25*cos(20), sampled at N = 64
   bin k      |X[k]|    phase/pi    exact |X[k]|  exact phase/pi
       3     32.0000     -0.0000         32.0              0.0
       7     16.0000     -0.5000         32.0              0.5
      20      8.0000      0.0000         16.0              0.0
  every bin with |X[k]| > 1e-9 for 1 <= k < N/2: [3, 7, 20]
  Three bins out of 31.  A pure tone that lands on the grid puts ALL of
  its energy in ONE bin; a tone that does not land on the grid smears
  across neighbours, and that smearing is spectral leakage.

=== Naive DFT and recursive FFT agree to machine precision ===
      N     max |DFT - FFT|      max |x - IDFT(FFT(x))|
      8            3.030e-15                   1.009e-15
     16            1.293e-14                   6.207e-15
     64            2.348e-13                   2.010e-14
    256            3.622e-12                   1.068e-13
   1024            9.855e-11                   5.407e-13
  Two algorithms for the same object, so they must agree; what is left is
  rounding.  The round trip returning the input is orthogonality in
  disguise: the transform matrix is unitary up to a factor 1/sqrt(N).

=== EXACT operation counts: the complexity claim, counted not timed ===
  Counting is deterministic, unlike a wall clock.  'complex mults' is the
  number of complex multiply-accumulates; 'trig calls' counts cos/sin.
      N   DFT mults   DFT trig   FFT mults   FFT trig   ratio mults   ratio trig
     16         256        512          32         64        -        -
     32        1024       2048          80        160        4.00x        2.50x
     64        4096       8192         192        384        4.00x        2.40x
    128       16384      32768         448        896        4.00x        2.33x
    256       65536     131072        1024       2048        4.00x        2.29x
    512      262144     524288        2304       4608        4.00x        2.25x
   1024     1048576    2097152        5120      10240        4.00x        2.22x
  DFT mults = N^2 exactly, so every doubling costs exactly 4.00x.
  FFT mults = (N/2)*log2(N), so every doubling costs
     2*(log2(N)+1)/log2(N) = 2.50x at N=16, 2.20x at N=1024, 2.13x at N=16384.
  That is the whole n-vs-n-log-n difference, exactly, with no noise:
     N =     16: predicted doubling factor = 2.5000
     N =   1024: predicted doubling factor = 2.2000
     N =  16384: predicted doubling factor = 2.1429

  At N = 2^20 = 1,048,576 points the two counts are:
     naive DFT : N^2            = 1,099,511,627,776 complex multiplications
     FFT       : (N/2)*log2(N)  = 10,485,760 complex multiplications
     ratio     : N / (2*log2 N) = 104,858
  A factor of 104,858 at one million points, and the factor is N/(2 log2 N),
  which grows without bound.  That is the sentence 'the FFT is O(n log n)
  instead of O(n^2)' actually asserting.

=== Projecting to the sizes real systems use, from the COUNTS ===
  A wall clock is not tabulated anywhere in this block: the numbers would
  change when you moved the machine, and a number that changes with the
  machine is not evidence about an algorithm.  Everything below is derived
  arithmetically from the operation counts already measured above.

  The ratio of work is exact:
    N =     1,024: DFT        1,048,576   FFT         5,120   ratio        205x
    N =     8,192: DFT       67,108,864   FFT        53,248   ratio      1,260x
    N =    65,536: DFT    4,294,967,296   FFT       524,288   ratio      8,192x
    N = 1,048,576: DFT 1,099,511,627,776   FFT    10,485,760   ratio    104,858x

  Projecting seconds needs ONE number from your own machine -- the cost of a
  single complex multiply-accumulate -- and then everything else is arithmetic.
  Take c = 2 ns per complex multiply-accumulate, a mid-range figure for
  interpreted Python, and the projections are:
             N        naive DFT            FFT     speed-up      predicted
         1,024         0.002 s      0.0000 s        205x          yes
         8,192         0.134 s      0.0001 s      1,260x          yes
        65,536         8.590 s      0.0010 s      8,192x          yes
     1,048,576      2199.023 s      0.0210 s    104,858x          yes

  The predicted column is the whole argument in one word: at N = 2^20 the
  quadratic route is more than 100x slower, so nobody runs it, and at
  N = 2^16 it is already 2,000x slower.  Change c to 0.5 ns and every number
  moves by a factor of four and the RATIOS do not move at all -- which is
  precisely why the counts are the evidence and the clock is not.

  One caveat worth stating because it is real: the naive loop in this lesson
  calls math.cos and math.sin inside the inner loop, which no serious
  implementation does.  A production quadratic DFT precomputes the twiddle
  table and saves roughly a factor of two, and a good one also uses the
  real-symmetry of real input to halve the work again.  Neither changes the
  class, and both are worth remembering when you read someone else's
  quadratic implementation and wonder why it is faster than yours.
```

There is no timing table in this block, deliberately. The projection table at the
end derives seconds from one stated constant — 2 ns per complex
multiply-accumulate — and then everything else is arithmetic, so changing the
constant moves the absolute numbers by a factor of four and leaves every
*ratio* untouched. That is the correct division of labour: the constant is a
property of your machine and belongs in a measurement, while the ratio
$N/(2\log_2 N)$ is a property of the two algorithms and belongs in a proof.
The operation counts are integers, checkable by hand from the formulas, and
they say the ratio diverges. A timing table on a shared machine argues none of
that.

One more observation from the agreement table. The `max |DFT - FFT|` column
grows with $N$ — `3.03e-15` at $N = 8$ to `9.86e-11` at $N = 1024`. That is
not the FFT being inaccurate; it is *accumulated rounding* in a computation with
$\log_2 N$ sequential stages, each contributing a relative error of order
$\epsilon$. The root-mean-square forward error of a radix-2 FFT grows like
$\Theta(\epsilon\log N)$, and the printed numbers follow that: $\log_2 1024 = 10$
against $\log_2 8 = 3$, a factor of 3.3 in the logarithm and a factor of 32 in
the error. The FFT trades a little accuracy for a lot of speed, which is a
bargain anyone would take.

### Block 3: the convolution theorem, and filtering in the frequency domain

```python
import math
import random

TAU = 2.0 * math.pi


def dft(x):
    N = len(x)
    out = []
    for k in range(N):
        acc = 0j
        for n in range(N):
            angle = -TAU * k * n / N
            acc += x[n] * complex(math.cos(angle), math.sin(angle))
        out.append(acc)
    return out


def fft(x):
    N = len(x)
    if N == 1:
        return list(x)
    if N & (N - 1):
        raise ValueError("radix-2 FFT needs a power of two, got " + str(N))
    even = fft(x[0::2])
    odd = fft(x[1::2])
    out = [0j] * N
    for k in range(N // 2):
        w = complex(math.cos(-TAU * k / N), math.sin(-TAU * k / N))
        t = w * odd[k]
        out[k] = even[k] + t
        out[k + N // 2] = even[k] - t
    return out


def idft(X):
    """Inverse transform: x[n] = (1/N) sum_k X[k] exp(+2*pi*i*k*n/N)."""
    N = len(X)
    return [z.real / N for z in fft([z.conjugate() for z in X])]


def cconv(x, y):
    """CIRCULAR convolution as written, Theta(N^2): (x *c* y)[m] = sum_j x[j] y[(m-j) mod N]."""
    N = len(x)
    out = []
    for m in range(N):
        acc = 0.0
        for j in range(N):
            acc += x[j] * y[(m - j) % N]
        out.append(acc)
    return out


def rms(a, b):
    return math.sqrt(sum((p - q) ** 2 for p, q in zip(a, b)) / len(a))


def lowpass(X, cut):
    """Keep bins 0..cut and the mirrored bins N-cut..N-1.  Three lines, no kernel."""
    N = len(X)
    return [X[k] if (k <= cut or k >= N - cut) else 0j for k in range(N)]


print("=== The convolution theorem ===")
#  In the time domain, circular convolution is Theta(N^2).
#  Via the FFT it is two transforms, N pointwise multiplications, one inverse.
#  The theorem says the two are the SAME number, so the FFT route is a change of
#  algorithm, not an approximation.  Here is the theorem, run.
N = 64
random.seed(7)
x = [random.gauss(0.0, 1.0) for _ in range(N)]
y = [random.gauss(0.0, 1.0) for _ in range(N)]
direct = cconv(x, y)
X, Y = fft(x), fft(y)
via_fft = idft([a * b for a, b in zip(X, Y)])
print(f"  N = {N}.  Circular convolution of two standard normal vectors.")
print(f"  max |direct - via FFT| = {max(abs(p - q) for p, q in zip(direct, via_fft)):.3e}")
print("  Identical to rounding, because it is one computation done two ways.")
print()
print(f"  sum |x[n]|^2     = {sum(v * v for v in x):.10f}   <- energy in the time domain")
print(f"  sum |X[k]|^2 / N = {sum(abs(v) ** 2 for v in X) / N:.10f}   <- the same energy")
print()
lg = math.log2(N)
direct_cost = N * N
fft_cost = 2 * (N // 2 * int(lg)) + N
print(f"  multiplications, direct      = N^2       = {direct_cost}")
print(f"  multiplications, via the FFT = 2*(N/2)*log2(N) + N = {fft_cost}")
print(f"  ratio = {direct_cost / fft_cost:.1f}x at N = {N}, and it grows as N/log N.")
print("  Convolution in time becomes POINTWISE MULTIPLICATION in frequency, and")
print("  multiplying N pairs of numbers is Theta(N).  A Theta(N^2) operation has")
print("  just acquired a Theta(N log N) implementation for free.")
print()

print("=== The response of a box average ===")
#  h = (1/W)(1,1,...,1) of length W.  Its transform is the Dirichlet kernel:
#      H[k] = |sin(pi*k*W/N)| / (W*|sin(pi*k/N)|),   H[0] = 1.
W = 5
H5 = fft([1.0 / W] * W + [0.0] * (N - W))
H3 = fft([1.0 / 3.0] * 3 + [0.0] * (N - 3))
print("       k    |H[k]| by FFT      closed form    width-3 box |H[k]|")
for k in (0, 1, 2, 4, 8, 16, 24, 31):
    closed = 1.0 if k == 0 else abs(math.sin(math.pi * k * W / N)) / (
        W * abs(math.sin(math.pi * k / N)))
    print(f"  {k:>5}   {abs(H5[k]):>15.9f}   {closed:>14.9f}   {abs(H3[k]):>17.9f}")
print("  The width-5 response falls from 1.0 to 0.19 by bin 31; the narrower box")
print("  falls faster.  Neither was designed as a filter -- averaging a few")
print("  neighbours IS a low-pass filter, and H tells you how much low-pass it is")
print("  before you run it once.")
print()

print("=== Case A: white noise, and the improvement you can PREDICT ===")
#  A real signal of RMS s satisfies sum|X|^2 = N s^2, and white noise of variance
#  v satisfies sum|X|^2 = N^2 v.  Zeroing a fraction f of the bins therefore
#  deletes a fraction f of the noise energy and none of the in-band signal.
#  Predicted RMS improvement: sqrt((N/2 - 1) / cut).
random.seed(11)
N = 256
CUT = 40
clean = [1.00 * math.sin(TAU * 5 * n / N)
         + 0.60 * math.sin(TAU * 11 * n / N + 0.70)
         + 0.30 * math.sin(TAU * 19 * n / N + 1.90)
         for n in range(N)]
noise = [random.gauss(0.0, 0.5) for _ in range(N)]
noisy = [clean[n] + noise[n] for n in range(N)]
zeros = [0.0] * N
C = fft(clean)
print(f"  N = {N}; signal in bins 5, 11, 19; white noise, sigma = 0.50; cutoff {CUT}")
print(f"  RMS(noise) = {rms(noise, zeros):.6f}  (exact: noise is generated separately)")
print()
out = idft(lowpass(fft(noisy), CUT))
kept_noise = idft(lowpass(fft(noise), CUT))
lost_signal = idft(lowpass(C, CUT))
predicted = math.sqrt((N // 2 - 1) / CUT)
print(f"  RMS error before filtering          = {rms(noisy, clean):.6f}")
print(f"  RMS error after filtering           = {rms(out, clean):.6f}")
print(f"  measured improvement                 = {rms(noisy, clean) / rms(out, clean):.2f}x")
print(f"  predicted sqrt((N/2-1)/cut) = {predicted:.2f}"
      f" = sqrt({N // 2 - 1}/{CUT}) = {predicted:.3f}")
print(f"  signal distortion from the filter   = {rms(lost_signal, clean):.6f}  (exactly 0)")
print(f"  white noise left in the passband    = {rms(kept_noise, zeros):.6f}")
print("  What is left is almost exactly the in-band noise we could not delete, so")
print("  the error floors there.  That floor is not a limitation of the FFT; it")
print("  is a statement about how much noise was inside the band you kept.")
print()

print("=== The cutoff trade-off, with signal and noise measured separately ===")
print("    cutoff   noise left   signal distortion   total RMS error")
for cut in (8, 12, 20, 40, 80, 120):
    total = idft(lowpass(fft(noisy), cut))
    print(f"  {cut:>7}   {rms(idft(lowpass(fft(noise), cut)), zeros):>11.6f}   "
          f"{rms(idft(lowpass(C, cut)), clean):>18.6f}   {rms(total, clean):>15.6f}")
print("  Below bin 19 you delete part of the SIGNAL: the distortion column")
print("  explodes and the total error gets WORSE.  Above bin 19 you delete only")
print("  noise, distortion is exactly 0, and the error rises back to the full")
print("  noise level.  The best cutoff is 20, and the minimum error is 0.171034.")
print("  Every low-pass design has this shape: a floor from in-band noise, and a")
print("  cliff at whichever bin the signal stops at.")
print()

print("=== Case B: narrowband hum, where the frequency domain really pays ===")
#  Mains hum, motor whine and sensor fixed-pattern noise are all band-limited.
#  When the unwanted part lives in a KNOWN, SMALL band, deleting it is nearly free.
hum = [0.60 * math.sin(TAU * 100 * n / N) for n in range(N)]
with_hum = [noisy[n] + hum[n] for n in range(N)]
out_hum = idft(lowpass(fft(with_hum), CUT))
out_white = idft(lowpass(fft(noisy), CUT))
print(f"  Same signal, same cutoff ({CUT}), plus a 0.60-amplitude tone at bin 100.")
print(f"  RMS of the hum on its own              = {rms(hum, zeros):.6f}")
print(f"  input RMS error, white noise only      = {rms(noisy, clean):.6f}")
print(f"  input RMS error, with the hum          = {rms(with_hum, clean):.6f}")
print(f"  output RMS error, with the hum         = {rms(out_hum, clean):.6f}")
print(f"  output RMS error, white noise only     = {rms(out_white, clean):.6f}")
print(f"  max |out_hum - out_white|              = "
      f"{max(abs(a - b) for a, b in zip(out_hum, out_white)):.3e}")
print("  The last line is the punchline: out_hum and out_white are the SAME vector,")
print("  because a pure tone lives in exactly one bin and deleting that bin deletes")
print("  the tone with no residue at all.  A notch filter is literally 'set a band")
print("  of coefficients to zero'.")
print()

print("=== Moving average: the same theorem, same answer, different trade-off ===")
def box_smooth_circular(v, width):
    N = len(v)
    half = width // 2
    return [sum(v[(i + d) % N] for d in range(-half, half + 1)) / width
            for i in range(N)]


w = 15
direct_smooth = box_smooth_circular(noisy, w)
kernel = [0.0] * N
for d in range(-(w // 2), w // 2 + 1):
    kernel[d % N] = 1.0 / w
H = fft(kernel)
fft_smooth = idft([a * b for a, b in zip(fft(noisy), H)])
print(f"  A 15-wide centred box average of the same noisy signal, N = {N}")
print(f"  max |time-domain - frequency-domain| = "
      f"{max(abs(p - q) for p, q in zip(direct_smooth, fft_smooth)):.3e}")
print(f"  white noise left by the box           = {rms(idft([a * b for a, b in zip(fft(noise), H)]), zeros):.6f}")
print(f"  signal distortion from the box        = {rms(idft([a * b for a, b in zip(C, H)]), clean):.6f}")
print(f"  total RMS error, box width 15         = {rms(direct_smooth, clean):.6f}")
print(f"  total RMS error, bin-40 cutoff        = {rms(out, clean):.6f}")
print("  The box leaves LESS noise (0.14 vs 0.30) because it averages 15 samples,")
print("  but it also distorts the signal more (0.34 vs 0.00), and the total is")
print("  worse.  Same theorem, different H, different point on the same curve.")
print()

print("=== Circular convolution is NOT linear convolution ===")
#  The classic bug: FFT-multiply computes the CIRCULAR convolution, which wraps
#  around the end of the array.  You must zero-pad to at least len(x)+len(y)-1.
N = 8
p = [1.0] * 6 + [0.0] * (N - 6)
q = [1.0] * 4 + [0.0] * (N - 4)
lin = [0.0] * (len(p) + len(q) - 1)
for i, pi in enumerate(p):
    for j, qj in enumerate(q):
        lin[i + j] += pi * qj
cir = idft([a * b for a, b in zip(fft(p), fft(q))])
print(f"  N = {N}; p = 6 ones then 2 zeros, q = 4 ones then 4 zeros.")
print(f"  The linear answer has {len(lin)} slots, and its last non-zero entry is")
print(f"  lin[{N}] = {lin[N]:.4f}, which the circular version has no room to store.")
print("   index   circular (free)   linear (wanted)")
for i in range(N):
    print(f"  {i:>6}   {cir[i]:>15.4f}   {lin[i]:>15.4f}")
print(f"  Index 0 is {cir[0]:.1f} instead of {lin[0]:.1f}: the tail of the linear")
print("  convolution wrapped around and landed on the front.  The fix is")
print("  zero-padding to len(x)+len(y)-1 points, which is why every real")
print("  convolution routine pads first.")
```

Output:

```text
=== The convolution theorem ===
  N = 64.  Circular convolution of two standard normal vectors.
  max |direct - via FFT| = 1.066e-14
  Identical to rounding, because it is one computation done two ways.

  sum |x[n]|^2     = 46.1695325576   <- energy in the time domain
  sum |X[k]|^2 / N = 46.1695325576   <- the same energy

  multiplications, direct      = N^2       = 4096
  multiplications, via the FFT = 2*(N/2)*log2(N) + N = 448
  ratio = 9.1x at N = 64, and it grows as N/log N.
  Convolution in time becomes POINTWISE MULTIPLICATION in frequency, and
  multiplying N pairs of numbers is Theta(N).  A Theta(N^2) operation has
  just acquired a Theta(N log N) implementation for free.

=== The response of a box average ===
       k    |H[k]| by FFT      closed form    width-3 box |H[k]|
      0       1.000000000      1.000000000         1.000000000
      1       0.990388003      0.990388003         0.996789818
      2       0.961865925      0.961865925         0.987190187
      4       0.852394525      0.852394525         0.949253022
      8       0.482842712      0.482842712         0.804737854
     16       0.200000000      0.200000000         0.333333333
     24       0.082842712      0.082842712         0.138071187
     31       0.194240221      0.194240221         0.330123151
  The width-5 response falls from 1.0 to 0.19 by bin 31; the narrower box
  falls faster.  Neither was designed as a filter -- averaging a few
  neighbours IS a low-pass filter, and H tells you how much low-pass it is
  before you run it once.

=== Case A: white noise, and the improvement you can PREDICT ===
  N = 256; signal in bins 5, 11, 19; white noise, sigma = 0.50; cutoff 40
  RMS(noise) = 0.520964  (exact: noise is generated separately)

  RMS error before filtering          = 0.520964
  RMS error after filtering           = 0.299609
  measured improvement                 = 1.74x
  predicted sqrt((N/2-1)/cut) = 1.78 = sqrt(127/40) = 1.782
  signal distortion from the filter   = 0.000000  (exactly 0)
  white noise left in the passband    = 0.299609
  What is left is almost exactly the in-band noise we could not delete, so
  the error floors there.  That floor is not a limitation of the FFT; it
  is a statement about how much noise was inside the band you kept.

=== The cutoff trade-off, with signal and noise measured separately ===
    cutoff   noise left   signal distortion   total RMS error
        8      0.132627             0.474342          0.492534
       12      0.149203             0.212132          0.259348
       20      0.171034             0.000000          0.171034
       40      0.299609             0.000000          0.299609
       80      0.435547             0.000000          0.435547
      120      0.508792             0.000000          0.508792
  Below bin 19 you delete part of the SIGNAL: the distortion column
  explodes and the total error gets WORSE.  Above bin 19 you delete only
  noise, distortion is exactly 0, and the error rises back to the full
  noise level.  The best cutoff is 20, and the minimum error is 0.171034.
  Every low-pass design has this shape: a floor from in-band noise, and a
  cliff at whichever bin the signal stops at.

=== Case B: narrowband hum, where the frequency domain really pays ===
  Same signal, same cutoff (40), plus a 0.60-amplitude tone at bin 100.
  RMS of the hum on its own              = 0.424264
  input RMS error, white noise only      = 0.520964
  input RMS error, with the hum          = 0.665290
  output RMS error, with the hum         = 0.299609
  output RMS error, white noise only     = 0.299609
  max |out_hum - out_white|              = 1.588e-14
  The last line is the punchline: out_hum and out_white are the SAME vector,
  because a pure tone lives in exactly one bin and deleting that bin deletes
  the tone with no residue at all.  A notch filter is literally 'set a band
  of coefficients to zero'.

=== Moving average: the same theorem, same answer, different trade-off ===
  A 15-wide centred box average of the same noisy signal, N = 256
  max |time-domain - frequency-domain| = 6.661e-16
  white noise left by the box           = 0.135948
  signal distortion from the box        = 0.344957
  total RMS error, box width 15         = 0.364940
  total RMS error, bin-40 cutoff        = 0.299609
  The box leaves LESS noise (0.14 vs 0.30) because it averages 15 samples,
  but it also distorts the signal more (0.34 vs 0.00), and the total is
  worse.  Same theorem, different H, different point on the same curve.

=== Circular convolution is NOT linear convolution ===
  N = 8; p = 6 ones then 2 zeros, q = 4 ones then 4 zeros.
  The linear answer has 15 slots, and its last non-zero entry is
  lin[8] = 1.0000, which the circular version has no room to store.
   index   circular (free)   linear (wanted)
       0            2.0000            1.0000
       1            2.0000            2.0000
       2            3.0000            3.0000
       3            4.0000            4.0000
       4            4.0000            4.0000
       5            4.0000            4.0000
       6            3.0000            3.0000
       7            2.0000            2.0000
  Index 0 is 2.0 instead of 1.0: the tail of the linear
  convolution wrapped around and landed on the front.  The fix is
  zero-padding to len(x)+len(y)-1 points, which is why every real
  convolution routine pads first.
```

The most useful line in that output is the `predicted 1.78` next to the
`measured 1.74`. Before running anything, the theory said a bin-40 low-pass on
256 samples would buy $\sqrt{127/40} = 1.78$, because 40 of the 127 positive
frequency bins survive and white noise has equal energy in all of them. The
measurement came in at 1.74, and the small shortfall is the in-band noise
adding in quadrature rather than the filter failing. That is the difference
between tuning a filter and guessing at one: the prediction is a two-line
argument and it takes a parameter you already chose.

---

### With Libraries

```python
# Requires numpy + matplotlib; not runnable with the standard library alone.
import math
import matplotlib
matplotlib.use("Agg")          # so the script runs without a display
import matplotlib.pyplot as plt
import numpy as np

TAU = 2.0 * math.pi
fig, axes = plt.subplots(1, 3, figsize=(16.5, 4.6))


def partial(x, n_terms):
    """Square wave f = -1 on (-pi, 0), +1 on (0, pi), as a truncated sine series.
    Only ODD terms survive, and b_n = 4/(pi*n)."""
    y = np.zeros_like(x)
    for n in range(1, n_terms + 1, 2):
        y += (4.0 / (math.pi * n)) * np.sin(n * x)
    return y


# 1. Adding terms does not remove the ringing at the jump -- it only narrows it.
x = np.linspace(-math.pi, math.pi, 4000)
axes[0].plot(x, np.sign(x), "k", linewidth=2.5, label="the square wave")
for n_terms, colour in ((3, "tab:blue"), (51, "tab:orange"), (801, "tab:green")):
    axes[0].plot(x, partial(x, n_terms), color=colour, linewidth=1.4,
                 label=f"{n_terms} terms")
axes[0].set_ylim(-1.6, 1.6)
axes[0].set_title("Gibbs ringing narrows, it never shrinks")
axes[0].set_xlabel("x")
axes[0].legend(fontsize=7)
axes[0].grid(alpha=0.3)

# 2. The spectrum of a signal and of the same signal plus noise.
rng = np.random.default_rng(11)
N = 256
clean = (1.00 * np.sin(TAU * 5 * np.arange(N) / N)
         + 0.60 * np.sin(TAU * 11 * np.arange(N) / N + 0.70)
         + 0.30 * np.sin(TAU * 19 * np.arange(N) / N + 1.90))
noisy = clean + rng.normal(0.0, 0.5, N)
C = np.fft.rfft(clean)
F = np.fft.rfft(noisy)
k = np.arange(N // 2 + 1)
axes[1].semilogy(k, np.maximum(np.abs(C), 1e-2), "k", linewidth=2,
                 label="clean signal")
axes[1].semilogy(k, np.maximum(np.abs(F), 1e-2), color="tab:red", linewidth=1.0,
                 alpha=0.7, label="same signal + noise")
axes[1].axvline(40, color="tab:blue", linestyle="--", linewidth=1.5,
                label="cutoff = bin 40")
axes[1].set_title("Noise is spread over every bin; the signal is in three")
axes[1].set_xlabel("frequency bin k")
axes[1].set_ylabel("|X[k]|")
axes[1].legend(fontsize=7)
axes[1].grid(alpha=0.3, which="both")

# 3. The time domain before and after: the low-pass result really is smoother.
t = np.arange(N) / N
cut = 40
mask = np.zeros(N // 2 + 1)
mask[:cut + 1] = 1.0
filtered = np.fft.irfft(np.fft.rfft(noisy) * mask, n=N)
axes[2].plot(t, clean, "k", linewidth=2.5, label="clean")
axes[2].plot(t, noisy, color="tab:red", linewidth=0.7, alpha=0.6, label="noisy")
axes[2].plot(t, filtered, color="tab:blue", linewidth=1.6, label="after low-pass")
axes[2].set_ylim(-3.2, 3.2)
axes[2].set_title("Zero the top bins, transform back")
axes[2].set_xlabel("time (periods)")
axes[2].legend(fontsize=7)
axes[2].grid(alpha=0.3)

plt.tight_layout()
plt.savefig("lesson55_fourier.png", dpi=110)
print("wrote lesson55_fourier.png")
noise_only = rng.normal(0.0, 0.5, N)
print(f"  RMS(noise)                  = {np.sqrt(np.mean(noise_only ** 2)):.6f}")
print(f"  RMS(clean - noisy)          = {np.sqrt(np.mean((clean - noisy) ** 2)):.6f}")
print(f"  RMS(clean - filtered)       = {np.sqrt(np.mean((clean - filtered) ** 2)):.6f}")
print(f"  predicted sqrt(127/40)      = {math.sqrt(127 / 40):.6f}")
print("  the third panel is the point: a three-line operation removed most of the")
print("  wiggle.  Panel 2 explains why it cannot remove the rest -- the noise")
print("  inside bins 0..40 is inside the band you kept, and the filter cannot")
print("  distinguish it from the signal that shares those bins.")
plt.close(fig)
```

Output:

```text
wrote lesson55_fourier.png
  RMS(noise)                  = 0.500250
  RMS(clean - noisy)          = 0.463392
  RMS(clean - filtered)       = 0.263048
  predicted sqrt(127/40)      = 1.781853
  the third panel is the point: a three-line operation removed most of the
  wiggle.  Panel 2 explains why it cannot remove the rest -- the noise
  inside bins 0..40 is inside the band you kept, and the filter cannot
  distinguish it from the signal that shares those bins.
```

Panel 1 is the reason image and audio codecs are not simply "keep the biggest
coefficients". The ringing beside the jump is the same height at 51 terms and
at 801; the only thing more terms buy is a narrower ring. Panel 2 is the reason
low-pass filtering works at all — noise has no preferred bin, so deleting bins
deletes noise, and a filter needs no model of the signal to exploit that. And
panel 2 also explains the floor: everything the red curve has between bins 0 and
40 is indistinguishable from the signal living in the same three bins, so no
amount of cleverness with $H$ can remove it.

---

## Common Mistakes

**Mistake 1 — using the wrong normalisation, so the round trip is not the identity.**

```python
import math

TAU = 2.0 * math.pi

# A minimal correct transform, so the comparison is about the convention only.
def fft(x):
    N = len(x)
    if N == 1:
        return list(x)
    if N & (N - 1):
        raise ValueError("not a power of two")
    even, odd = fft(x[0::2]), fft(x[1::2])
    out = [0j] * N
    for k in range(N // 2):
        w = complex(math.cos(-TAU * k / N), math.sin(-TAU * k / N))
        t = w * odd[k]
        out[k] = even[k] + t
        out[k + N // 2] = even[k] - t
    return out


print("=== Mistake 1: forgetting the 1/N in the inverse transform ===")
N = 8
x = [1.0, 2.0, 3.0, 4.0, 4.0, 3.0, 2.0, 1.0]
X = fft(x)
for label, scale in (("WRONG: x[n] = sum_k X[k] e^{+..}", 1.0),
                     ("WRONG: x[n] = sum_k X[k] e^{+..} / sqrt(N)", 1.0/math.sqrt(N)),
                     ("RIGHT: x[n] = (1/N) sum_k X[k] e^{+..}", 1.0/N)):
    back = [(scale * z).real for z in
            [sum(X[k] * complex(math.cos(2 * math.pi * k * n / N),
                                math.sin(2 * math.pi * k * n / N)) for k in range(N))
             for n in range(N)]]
    print(f"  {label:<44} x[0] = {back[0]:>10.4f}  (true {x[0]:.1f})")
print("  Only one normalisation makes the round trip an identity.  The forward")
print("  transform has no 1/N and the inverse has exactly 1/N; that is the whole")
print("  convention.  Get it wrong and your round trip multiplies the signal by N,")
print("  which you will notice as 'why is everything 256x too big'.")
```

The tempting version is the symmetric one, $1/\sqrt{N}$ on both sides, because
it looks tidier and makes the transform matrix exactly unitary. It is a perfectly
good convention — but then *both* transforms carry $1/\sqrt N$, and writing
only the forward one with it is the bug. The invariant is not a particular
formula; it is that the forward and inverse must be mutual inverses. Check it once
on a known signal, as above, and you never have to think about it again.

**Mistake 2 — zeroing only half the bins of a real signal's spectrum.**

```python
import math
import random

TAU = 2.0 * math.pi


def fft(x):
    N = len(x)
    if N == 1:
        return list(x)
    if N & (N - 1):
        raise ValueError("not a power of two")
    even, odd = fft(x[0::2]), fft(x[1::2])
    out = [0j] * N
    for k in range(N // 2):
        w = complex(math.cos(-TAU * k / N), math.sin(-TAU * k / N))
        t = w * odd[k]
        out[k] = even[k] + t
        out[k + N // 2] = even[k] - t
    return out


print("=== Mistake 2: filtering only the first half of the bins ===")
random.seed(3)
N = 32
sig = [1.0 * math.sin(TAU * 3 * n / N) + 0.5 * math.sin(TAU * 7 * n / N) for n in range(N)]
noisy = [sig[n] + random.gauss(0, 0.4) for n in range(N)]
F = fft(noisy)
cut = 5
half_only = [F[k] if k <= cut else 0j for k in range(N)]              # WRONG
both = [F[k] if (k <= cut or k >= N - cut) else 0j for k in range(N)]   # RIGHT


def idft(A):
    m = len(A)
    return [z / m for z in fft([z.conjugate() for z in A])]


a, b = idft(half_only), idft(both)
print("   n    real part (half-only)   imag part (half-only)   real part (both)   imag (both)")
for n in (0, 1, 2, 8, 20, 31):
    print(f"  {n:>3}   {a[n].real:>20.8f}   {a[n].imag:>21.8f}   {b[n].real:>15.8f}"
          f"   {b[n].imag:>11.3e}")
print(f"  max |imaginary part| half-only = {max(abs(z.imag) for z in a):.6f}")
print(f"  max |imaginary part| both      = {max(abs(z.imag) for z in b):.3e}")
print(f"  max |half-only - both|         = {max(abs(p - q) for p, q in zip(a, b)):.6f}")
print("  A real input has a conjugate-symmetric spectrum: X[N-k] = conj(X[k]).  Zero")
print("  only the low half and you destroy that symmetry, so the inverse transform")
print("  is COMPLEX.  The imaginary part is not 'small error', it is the answer you")
print("  deleted.  Always keep both halves, or keep one and mirror it.")
```

The tempting version is exactly what the textbooks write for a *complex* signal,
where there is no symmetry to respect and the whole spectrum matters. It looks
correct, and for complex input it is. The failure is silent: you get a plausible
real part and a large imaginary part, and if you take `.real` you never notice.
`numpy.fft.rfft` and `irfft` exist precisely so that you never have to think
about this — they return $N/2+1$ numbers and rebuild the symmetry for you.

**Mistake 3 — computing a circular convolution when you wanted a linear one.**

```python
def lconv(x, y):
    out = [0.0] * (len(x) + len(y) - 1)
    for i, xi in enumerate(x):
        for j, yj in enumerate(y):
            out[i + j] += xi * yj
    return out


def cconv(x, y):
    m = len(x)
    return [sum(x[j] * y[(t - j) % m] for j in range(m)) for t in range(m)]


print("=== Mistake 3: padding to N instead of N_x + N_y - 1 ===")
N = 16
p = [1.0] * 10                      # length 10
q = [1.0] * 8                       # length 8
lin = lconv(p, q)
circ = cconv(p + [0.0] * (N - len(p)), q + [0.0] * (N - len(q)))
pad = 32
c32 = cconv(p + [0.0] * (pad - len(p)), q + [0.0] * (pad - len(q)))
print(f"  len(p) = {len(p)}, len(q) = {len(q)}, transform length N = {N}.")
print(f"  Linear convolution needs {len(lin)} points, and N = {N} < {len(lin)}.")
print("   index   circular at N=16       circular at N=32 (padded)   linear")
for i in range(len(lin)):
    print(f"  {i:>6}   {circ[i % N]:>20.4f}   {c32[i]:>25.4f}   {lin[i]:>8.4f}")
print(f"  max error at N=16 = {max(abs(circ[i % N] - lin[i]) for i in range(len(lin))):.4f}")
print(f"  max error at N=32 = {max(abs(c32[i] - lin[i]) for i in range(len(lin))):.3e}")
print(f"  lin[{len(lin) - 1}] = {lin[-1]:.1f} had nowhere to go, so it landed on index 0")
print(f"  and made it {circ[0]:.1f} instead of {lin[0]:.1f}.")
print("  Zero-pad to at least len(x)+len(y)-1 -- not to 'about the right size'.")
```

The tempting version pads to the next power of two above the input length,
because that is what the FFT requires and it feels like the requirement has been
met. It has — the FFT requirement is that $N$ be a power of two; the *convolution*
requirement is the separate condition $N \ge M + L - 1$. Conflating them is the
whole bug. Note the damage: the answer is wrong only at the two ends, which is
exactly where nobody looks, and the shape of the middle is perfectly plausible.

**Mistake 4 — checking Parseval with $\lvert X\rvert$ instead of $\lvert X\rvert^2$.**

```python
import math

TAU = 2.0 * math.pi


def fft(x):
    N = len(x)
    if N == 1:
        return list(x)
    if N & (N - 1):
        raise ValueError("not a power of two")
    even, odd = fft(x[0::2]), fft(x[1::2])
    out = [0j] * N
    for k in range(N // 2):
        w = complex(math.cos(-TAU * k / N), math.sin(-TAU * k / N))
        t = w * odd[k]
        out[k] = even[k] + t
        out[k + N // 2] = even[k] - t
    return out


print("=== Mistake 4: checking Parseval with |X| instead of |X|^2 ===")
N = 32
sig = [1.0 * math.sin(TAU * 3 * n / N) + 0.5 * math.sin(TAU * 7 * n / N) for n in range(N)]
S = fft(sig)
print(f"  sum |x[n]|^2        = {sum(v * v for v in sig):.10f}")
print(f"  sum |X[k]|^2 / N    = {sum(abs(v) ** 2 for v in S) / N:.10f}   <- Parseval, correct")
print(f"  sum |X[k]| / N      = {sum(abs(v) for v in S) / N:.10f}   <- not the same thing")
print("  Parseval is about ENERGY, so it is the square of the magnitude.  Using")
print("  |X| gives a smaller number, and it does not match, and you conclude the")
print("  transform is wrong.  It is not; the identity you quoted was wrong.")
```

The tempting version is that $|X_k|$ *is* the amplitude and $\lvert X_k\rvert^2$
is a different thing called power — both statements are true, and neither tells
you which one Parseval uses. Parseval is a statement about the inner product, and
the inner product squares its entries. If the check fails, suspect the identity
before the code.

**Mistake 5 — reading bin $k$ as $k$ hertz.**

```python
print("=== Mistake 5: reading a spectrum bin as 'the frequency in Hz' ===")
N = 256
fs = 8000.0            # sample rate in hertz
print(f"  N = {N} samples, sample rate {fs:.0f} Hz.")
print("   bin   bin * fs/N (Hz)   what a tone in that bin actually is")
for k in (0, 5, 40, 64, 200):
    print(f"  {k:>4}   {k * fs / N:>15.2f}   a sinusoid at that many hertz, {k} cycles per record")
print(f"  A 100 Hz tone lands in bin {100 * N / fs:.2f}, not bin 100.  The highest frequency")
print(f"  this transform can see at all is fs/2 = {fs / 2:.0f} Hz, which is bin {N // 2}.")
print("  Bins 129..255 are the mirror image of bins 127..1 and carry no extra")
print("  information, which is why numpy.fft.rfft returns N/2+1 numbers, not N.")
```

The tempting version comes from the fact that bin numbers and "number of cycles
in the record" are the same integer, and from a habit of thinking in normalised
frequency where everything is measured in cycles per sample and $f_s$ never
appears. Both are fine until you have to convert to hertz, at which point the
$1/N$ is the entire conversion factor. For an 8 kHz audio signal a 100 Hz tone
is bin 3.2 — so a 256-point transform, which is what you get from 32 ms of
audio, cannot tell 100 Hz from 80 Hz.

---

## Multiple Choice Questions

**Q1.** A function has zero cosine coefficients ($a_k = 0$ for every $k$) and
$4/(\pi k)$ for odd $k$ and $0$ for even $k$ as its sine coefficients. What is
the function, and what does the $1/k$ decay tell you?

- A) A triangle wave; the $1/k$ tail is unavoidable
- B) A square wave; the $1/k$ tail comes from the jump discontinuities and makes the series converge slowly
- C) A triangle wave; the $1/k$ tail is a quadrature artefact of the midpoint rule
- D) A sawtooth wave; the decay is $1/k^2$ and the $4/(\pi k)$ is a typo

<details>
<summary>Answer and explanation</summary>

**B) A square wave; the $1/k$ tail comes from the jump discontinuities and makes
the series converge slowly.**

Only odd $k$ contribute, with an amplitude proportional to $1/k$ and no cosine
content, and the partial sums of the code ring at 8.95% of the jump height at
every truncation. That combination is the standard square wave
$f = -1$ on $(-\pi,0)$, $+1$ on $(0,\pi)$: odd function, so all $a_k$ vanish;
odd harmonics only, because the two half-periods cancel in pairs.

Option A is the other famous answer, but a triangle wave is a *continuous*
piecewise-linear function, so its coefficients decay like $1/k^2$, not $1/k$.
Option C confuses the two sources of error in the lesson: the $10^{-10}$ gaps in
the printed table are quadrature error, and they are in the last digits, not in
the $1/k$ exponent. Option D is wrong on two counts — a sawtooth is $b_k = 2
(-1)^{k+1}/k$, so the sign alternates with $k$ and the amplitudes are $2/k$, not
$4/(\pi k)$; and the decay is $1/k$, not $1/k^2$.

</details>

**Q2.** The code prints `max |DFT - FFT| = 3.030e-15` at $N=8$ and `9.855e-11` at
$N=1024$. What is the correct interpretation?

- A) The FFT is inaccurate and should not be used above $N = 256$
- B) Both are exact; the growing gap is accumulated rounding, and it grows like $\Theta(\epsilon\log N)$ because there are $\log_2 N$ sequential stages
- C) The DFT is wrong and the FFT is right, because the DFT calls `cos` and `sin` directly
- D) The gap is a bug in the inverse transform, and it would disappear with a better implementation

<details>
<summary>Answer and explanation</summary>

**B) Both are exact; the growing gap is accumulated rounding, and it grows like
$\Theta(\epsilon\log N)$ because there are $\log_2 N$ sequential stages.**

The two algorithms compute the same mathematical object, so the difference is
entirely floating-point rounding. The FFT has $\log_2 8 = 3$ stages and the
1024-point transform has 10, a factor of 3.3, and the printed error grows by a
factor of 32 — consistent with $\epsilon\log N$ growth on top of the $\sqrt{N}$
that comes from summing more terms at all.

Option A reads a 10-digit error at $N = 1024$ as a failure. It is 10 correct
digits on a transform of 1024 numbers; the naive route is *worse*, at
`9.86e-11` is still four orders of magnitude finer than the signal it is
transforming. Option C is exactly backwards: calling `cos`/`sin` directly makes
each term accurate to one ulp, and the $\Theta(N^2)$ of them accumulate; that is
exactly why the naive route has the larger error. Option D is wrong because the
gap appears in the *forward* transform comparison, where no inverse is involved.

</details>

**Q3.** You need the DFT of a length-$N$ signal and the answer must be exact to
all 16 digits. Which statement is correct?

- A) Use the recursive radix-2 FFT; $\Theta(N\log N)$ and more accurate than the naive route because it does less arithmetic
- B) Use the naive DFT; the FFT's $O(N\log N)$ speed comes from a clever rearrangement that loses precision
- C) Use the FFT, but zero-pad to the next power of two — padding always improves precision
- D) Neither can exceed $\Theta(\epsilon N)$ error, so for exactness compute with exact rational arithmetic

<details>
<summary>Answer and explanation</summary>

**D) Neither can exceed $\Theta(\epsilon N)$ error, so for exactness compute with
exact rational arithmetic.**

Every floating-point transform has relative error growing at least linearly in
$N$ and at least as $\Theta(\epsilon \log N)$ in practice, so at some $N$ no
double-precision implementation returns all 16 digits. When you genuinely need
exactness — symbolic verification, an exact convolution of integer coefficients,
checking a hash — use `fractions.Fraction` or `gmpy2`, and pay the time.

Option A is the trap: the FFT is *less* accurate in absolute terms, not more.
The code shows the naive and FFT spectra differing by `3.03e-15` at $N=8$ and
`9.86e-11` at $N=1024$, and the naive route is the one on the wrong side of
that gap. Fewer operations means fewer roundings, not more accuracy. Option B
invents a tradeoff that does not exist: Cooley–Tukey is an exact algebraic
identity, so both routes compute the same sum. Option C is false for two
reasons — zero-padding adds zeros, which contribute exact zeros to every
partial sum, so it cannot improve precision; and the accuracy of the original
$2^{20}$-point transform is unchanged either way.

</details>

**Q4.** In the convolution theorem demonstration, the direct route costs 4096
multiplications and the FFT route 448 at $N=64$. Which statement is correct?

- A) The FFT route is 9.1× faster but only approximately correct, because the transform is applied to a product rather than the inputs
- B) The FFT route is 9.1× faster and *exactly* as correct, because `max |direct - via FFT| = 1.066e-14` comes from rounding and the theorem is an identity
- C) Both routes cost the same, and the count difference is a measurement artefact
- D) The FFT route is faster only when $N > 1024$; below that the overhead dominates

<details>
<summary>Answer and explanation</summary>

**B) The FFT route is 9.1× faster and *exactly* as correct, because
`max |direct - via FFT| = 1.066e-14` comes from rounding and the theorem is an
identity.**

The convolution theorem says the FFT-multiply-then-inverse construction returns
the *same* $\Theta(N^2)$ sum, computed by a different route. `1.066e-14` on
values of order 8 is 16-digit agreement, and the identical Parseval numbers
(`46.1695325576` on both sides) say the same thing independently.

Option A is the most common misconception about the FFT and it deserves to be
named as one: the theorem does not approximate the convolution, it computes it
exactly by a faster method. The proof substitutes both transforms and uses
orthogonality; nothing is thrown away. Option C is arithmetically absurd —
4096 against 448 is a factor of 9.1, and both are exact counts of the actual
inner loops. Option D has the crossover in the wrong place: the FFT wins at
every $N$ in pure Python (the `6x` in the measured table is at $N=32$), and in
compiled code the crossover is a few hundred at worst, because the asymptotic
advantage is $N/\log N$ and growing.

</details>

**Q5.** The denoising experiment uses a bin-40 low-pass on a 256-point signal
whose content sits in bins 5, 11 and 19, and reports a measured improvement of
1.74× against a predicted $\sqrt{127/40} = 1.78$. Why is the measurement
slightly short of the prediction?

- A) The prediction is wrong; the correct factor is $\sqrt{160/40} = 2.0$
- B) The prediction assumes noise energy is spread perfectly uniformly over the 127 positive-frequency bins, and the in-band noise adds in quadrature to the distortion-free output
- C) The measurement is wrong because the transform normalisation differs between the two routes
- D) The shortfall is float32 rounding in the random number generator

<details>
<summary>Answer and explanation</summary>

**B) The prediction assumes noise energy is spread perfectly uniformly over the
127 positive-frequency bins, and the in-band noise adds in quadrature to the
distortion-free output.**

A real signal of length $N$ has $N/2 - 1 = 127$ positive-frequency bins plus DC.
A low-pass keeping 40 of them keeps $40/127$ of the white-noise energy, so the
RMS should fall by $\sqrt{127/40} = 1.782$. The measured 1.74 differs by 2%
because the transform of a finite sample of white noise is not *exactly* uniform
across bins, and because the retained in-band noise is not the only contributor
to the output error.

Option A uses 160 bins, but a 256-point transform of a real signal has only 128
independent frequencies (0 through 127), and 127 non-DC ones. Bins 128 to 255
are the mirror image, which is why the printed table scans only $1 \le k < N/2$.
Option C is a non-issue: both routes use the same `fft`/`idft` pair, and
normalisation errors are a factor of $N$ or a factor of 2, not 2%. Option D is
wrong on two counts — `random.gauss` is a double-precision generator, so there
is no float32 anywhere; and a `1.4%` shortfall is not a precision artefact
anyway, it is a modelling assumption that is slightly optimistic.

</details>

**Q6.** You low-pass a real signal by zeroing bins above the cutoff, and the
result comes back complex. What is the most likely cause?

- A) The cutoff was set above $N/2$, so you deleted a frequency the transform cannot represent
- B) You zeroed only bins $0 \dots$ cutoff and left the mirrored bins $N-\text{cutoff} \dots N-1$ untouched, breaking conjugacy symmetry
- C) The signal contained a DC offset, which must be removed before filtering
- D) The inverse transform is missing its $1/N$ factor

<details>
<summary>Answer and explanation</summary>

**B) You zeroed only bins $0 \dots \text{cutoff}$ and left the mirrored bins
$N-\text{cutoff} \dots N-1$ untouched, breaking conjugacy symmetry.**

For a real input the spectrum satisfies $X_{N-k} = \overline{X_k}$, so the top half
is determined by the bottom half. Zeroing one half without the other leaves a
spectrum that is not any real signal's spectrum, and the inverse transform of it
is genuinely complex. The code prints `max |imaginary part| half-only = 0.766582`
against `2.359e-16` for the correct version — the imaginary part is not rounding
error, it is the half of the signal you deleted, arriving in the imaginary
component.

Option A is confused about the frequency range. Bins above $N/2$ are the *mirror*
of bins below, not frequencies above Nyquist; the highest real frequency is bin
$N/2$ at $f_s/2$. And a cutoff above $N/2$ would pass everything, not make the
answer complex. Option C is false — a DC offset lives in bin 0 and is
conjugate to itself, so it cannot break symmetry; keeping it is a separate
question from a complex result. Option D would scale the answer by $N = 32$ and
leave it real, not make it complex.

</details>

**Q7.** Why is zero-padding a convolution "to the next power of two" not
sufficient, even though it is exactly what the FFT requires?

- A) Because the FFT requires $N$ to be a power of two and the convolution requires $N \ge M + L - 1$, and these are separate conditions
- B) Because zero-padding changes the values of the transform, so the convolution of the padded signals differs from the convolution of the originals
- C) Because the circular convolution of the padded signals is computed with $N$ multiplications, and the transform of the result needs $N/2$ points
- D) Because padding must be on the left for one operand and on the right for the other

<details>
<summary>Answer and explanation</summary>

**A) Because the FFT requires $N$ to be a power of two and the convolution
requires $N \ge M + L - 1$, and these are separate conditions.**

The FFT constraint is about the algorithm's structure (the radix-2 recursion
needs an even length and halves it). The convolution constraint is about
avoiding wraparound: the linear convolution of lengths $M$ and $L$ has $M+L-1$
non-contributing positions, and a transform of length $N$ stores indices modulo
$N$. The code demonstrates the failure with $\text{len}(p)=10$, $\text{len}(q)=8$
and $N=16$: `max error at N=16 = 1.0000`, because `lin[16] = 1.0` wrapped onto
index 0 and made it `2.0`. Padding to 32 gives `0.000e+00`.

Option B is false and important to rule out: the transform of a zero-padded
signal is *exactly* the transform of the original sampled at the same grid, and
the convolution of the padded signals equals the linear convolution of the
originals, with zeros appended. Padding introduces no error at all. It is
`numpy.convolve`'s job to do both steps, and it does. Option C describes an
irrelevant detail of the `rfft` output size, which is a consequence of the
symmetry and not a cause of error. Option D is invented; padding position
matters only for *phase* alignment in correlation, not for the values of a
convolution.

</details>

**Q8.** Why does a function with a jump discontinuity converge as slowly as
$1/N$, and why does the overshoot beside the jump not shrink?

- A) The $1/N$ decay is a numerical artefact; with exact arithmetic the series converges geometrically, and the overshoot is rounding at the discontinuity
- B) The coefficients decay like $1/k$ because the function has a corner, and the overshoot is 8.95% of the jump at every truncation — only its width shrinks, like $1/N$
- C) Both effects are caused by the Gibbs phenomenon, which is a theorem saying the series diverges at a jump
- D) The series converges to the wrong value at the jump: it should return the left-hand limit, and the overshoot is the size of the correction

<details>
<summary>Answer and explanation</summary>

**B) The coefficients decay like $1/k$ because the function has a corner, and the
overshoot is 8.95% of the jump at every truncation — only its width shrinks,
like $1/N$.**

The code measures `8.9490%` at $N=801$ and again at $N=3201$, and
$N \times$ width converging to `1.7521`. The rate follows from smoothness:
a function with $m$ continuous derivatives has coefficients decaying like
$1/k^{m+1}$, so a jump ($m=0$) gives $1/k$ and a corner ($m=1$) gives $1/k^2$. A
triangle wave's $1/k^2$ is why the square wave is the hard case.

Option A is a comfortable belief and it is false: the decay is a property of the
function's Fourier transform near zero, not of the arithmetic, and the measured
`err*N ≈ 0.7` is stable across a 100-fold increase in $N$ — exactly the signature
of a true $\Theta(1/N)$ rate. Option C misstates Gibbs as a divergence theorem;
the series *converges* at the jump, to the midpoint. Option D is the most
interesting wrong answer, because the first clause is right: the series does
converge to the midpoint $(f^- + f^+)/2$ at a jump, which is exactly why a
Gibbs-oscillating output looks blurry at edges. But the overshoot is not a
"correction" that the method adds and then removes — it is present in every
partial sum, permanently, at a fixed height.

</details>

**Q9.** The lesson states that a 15-wide box average and a bin-40 low-pass are
both "the same theorem with a different $H$", yet the box leaves *less* noise
(`0.135948` against `0.299609`) and yet gives a *worse* total error
(`0.364940` against `0.299609`). What explains this?

- A) The box filter is a poor approximation to the ideal low-pass, so its extra noise rejection is not worth its signal distortion
- B) The box filter's response is not monotone, so it amplifies some frequencies; the printed $|H[k]|$ values are all positive so this cannot happen
- C) A box average of width $W$ reduces white noise by exactly $\sqrt{W}$, so the box must be strictly better
- D) The two filters are not equivalent because the box is centred and the low-pass is causal

<details>
<summary>Answer and explanation</summary>

**A) The box filter is a poor approximation to the ideal low-pass, so its extra
noise rejection is not worth its signal distortion.**

Both are $H_k = \text{DFT}(h_k)$ applied as $Y_k = H_kX_k$, so they are the same
operation with different transfer functions. The box of width 15 has $|H[k]|$
falling from `1.0` to `0.33` by bin 16 and still `0.138` at bin 24 — it has a
wide, gradual passband, so it removes broadband noise well (`0.135948`) while
also attenuating the signal's own content in bins 11 and 19 (`0.344957` of
distortion). The bin-40 filter has a flat passband over every bin the signal
occupies, so its distortion is exactly `0.000000`. Total error is the
combination, and the box loses.

Option B is a real phenomenon for a different filter (the Dirichlet kernel has
sidelobes and, in the two-sided form, alternating sign) but it is not the story
here: the printed table shows $|H[k]|$ for the width-5 and width-3 boxes, and
those are the magnitudes of a sum of unit phasors, so they are non-negative by
construction. Option C states a true fact — averaging $W$ independent noise
samples does reduce variance by a factor $W$ — and then draws a false conclusion
from it, because it ignores the signal term entirely. The total error is
$\sqrt{\text{noise}^2 + \text{distortion}^2}$, and one term does not dominate the
other. Option D is not a distinction that exists in this computation: both
filters are applied circularly to a periodic signal, so neither is causal or
non-causal in any meaningful sense.

</details>

**Q10.** A tone at exactly 5.25 bins of a 64-point transform leaks across every
bin, but a tone at exactly 5 bins puts all its energy in one bin with
$|X_5| = 32.0$. Which pair of statements about fixing the leakage is correct?

- A) Zero-padding to 256 makes the 5.25 tone concentrate in bin 21 with $|X| = 128.0$, and it also raises the 5.0 tone's peak from 32.0 to 128.0
- B) Zero-padding reduces the leakage: the 5.25 tone will occupy only bins 20, 21, 22 after padding to 256
- C) A Hann window reduces leakage but widens the main lobe: the 5.0 tone spreads to bins 4, 5, 6 with magnitudes `8.0, 16.0, 8.0`
- D) Neither padding nor windowing helps; leakage is fundamental to the discrete transform and no preprocessing can reduce it

<details>
<summary>Answer and explanation</summary>

**C) A Hann window reduces leakage but widens the main lobe: the 5.0 tone spreads
to bins 4, 5, 6 with magnitudes `8.0, 16.0, 8.0`.**

A window is a multiplication in the time domain, so by the convolution theorem
it is a *convolution* in the frequency domain: the single spike at bin 5 gets
smeared into the window's own three-bin response. The Hann window's transform is
`0.5, 1.0, 0.5` at bins $-1,0,1$ relative to the centre, which is exactly the
`8.0, 16.0, 8.0` pattern (scaled by $N/4$ because the window halves the average
amplitude). In exchange, the sidelobes drop by about 30 dB, so the off-grid 5.25
tone's leakage floor falls from `0.37` to `0.036`.

Option A is half right, and the half that is right is the trap. Zero-padding
*does* concentrate the 5.25 tone — after padding to 256, the exercise code finds
it alone in bin 21 with $|X| = 128.0$ — and it *does* raise the 5.0 tone's peak
from 32.0 to 128.0. But that is not a reduction in leakage: padding changes the
*scale* of the frequency axis from $f_s/64$ to $f_s/256$, so the same physical
sidelobe pattern is now 4× closer together. Padding improves the *appearance* of
the spectrum, not the resolving power. Option B is the misconception that
padding is a leak fix, and it is false for the same reason. Option D is too
strong: windowing is standard practice precisely because it does reduce sidelobes
— the cost is main-lobe width, and no free lunch exists.

</details>

---

## Subjective Questions

### Short Answer

**Q1. State the two properties that make sine and cosine the only functions worth
expanding in, and say what each one buys you.**

<details>
<summary>Model answer</summary>

**Orthogonality.** For $T$-periodic functions with $\omega_k = 2\pi k/T$,
$\int_0^T \cos(\omega_k t)\cos(\omega_m t)\,dt = T/2$ when $k = m$ and $0$
otherwise, and the same for sines; every mixed integral is $0$. This means
multiplying by $\cos(\omega_k t)$ and averaging over a period is a *perfect
matched filter*: it returns $a_k$ and annihilates every other coefficient
simultaneously, with no cross-talk and no iterative elimination.

**Closure under differentiation.** $\frac{d}{dt}\sin(\omega t) = \omega
\cos(\omega t)$ and $\frac{d}{dt}\cos(\omega t) = -\omega \sin(\omega t)$:
the derivative of a sinusoid is a sinusoid of the same frequency, scaled. So
differentiating a Fourier series term by term stays inside the same basis
(differentiation becomes multiplication by $ik$), whereas differentiating a
Taylor series moves you to a *different* basis and a different expansion centre.

The first property is what makes the coefficients *computable by projection*; the
second is what makes the basis a good basis for differential equations. The code
demonstrates the first directly: the `w1 == w2` row gives `3.141593` and every
other row gives `0.000000` to 15 digits.

</details>

**Q2. Define the DFT and the inverse DFT, and say exactly where the
normalisation goes.**

<details>
<summary>Model answer</summary>

For $x = (x_0, \dots, x_{N-1})$ with $x_n \in \mathbb{C}$,

$$X_k = \sum_{n=0}^{N-1} x_n e^{-2\pi i kn/N}, \quad k = 0,\dots,N-1,$$
$$x_n = \frac{1}{N}\sum_{k=0}^{N-1} X_k e^{2\pi i kn/N}.$$

The forward transform carries **no** $1/N$ and the inverse carries **exactly
$1/N$**. The two signs of the exponent are also flipped. The normalisation is
pinned by requiring the round trip to be the identity: substitute the first into
the second, and the inner sum $\sum_k e^{2\pi i k(m-n)/N}$ equals $N$ if
$m = n$ and $0$ otherwise, so the $1/N$ cancels the $N$ exactly.

The alternative convention puts $1/\sqrt N$ on both sides, which makes the
transform matrix exactly unitary. That is fine — provided *both* transforms get
it. The mistake the code demonstrates is using $1/\sqrt N$ on one side only,
which returns `x[0] = 2.8284` instead of `1.0000` at $N = 8$.

</details>

**Q3. What is spectral leakage, why does it happen, and what are the two
standard remedies and their respective costs?**

<details>
<summary>Model answer</summary>

**Leakage** is the spreading of a single sinusoid's energy across many transform
bins. It happens when the sinusoid's frequency does not coincide with the grid
spacing $f_s/N$: the bins can only represent frequencies $k f_s/N$, so a tone
somewhere between two bins is not representable and its energy must be smeared.
A tone exactly on the grid has $X_k = AN/2$ in one bin and $0$ everywhere else;
a tone at $f_0 = 5.25$ bins has $O(N)$ energy in *every* bin, decaying like
$1/|\sin(\pi(f_0-k))|$.

**Zero-padding** samples the same signal on a $4\times$ finer frequency grid. The
physical sidelobe pattern is unchanged, but it is drawn with bins a quarter as
wide, so the peak looks sharp and the leakage floor looks low. Cost: $4\times$
the work, and no actual improvement in resolving power. The 5.25-bin tone does go
to a single bin of the 256-point transform — but only because the grid got finer,
not because the leakage went away.

**Windowing** multiplies by a taper that goes to zero at the record ends. In the
frequency domain that is a convolution with the window's own spectrum, so the
single spike is replaced by the window's main lobe plus its sidelobes. Cost: the
main lobe *widens* — a Hann window spreads an on-grid tone to three bins
(`8.0, 16.0, 8.0`) instead of one — but the sidelobes fall by roughly 30 dB,
so the noise floor under a weak tone drops correspondingly. This is the
standard tradeoff in spectral estimation: `scipy.signal.windows` is a menu of
competing sidelobe/main-lobe pairs.

</details>

**Q4. Explain the Gibbs phenomenon in terms of what a truncated series is doing
near a jump, and say what it costs you in practice.**

<details>
<summary>Model answer</summary>

At a jump of size $J$ the partial sums converge to the *midpoint* of the two
one-sided limits, and near the jump they overshoot by a height that converges to
$0.08949\,J$ — about 8.95% of the step — and then comes back down. The
oscillation's *width* shrinks like $\Theta(1/N)$ while its *height* stays put,
which is what the code measures: `8.9490%` at both $N = 801$ and $N = 3201$, with
$N \times$ width converging to `1.7521`.

The intuitive reason is that the kernel is $\text{Dirichlet}_N$, a windowed sinc.
Squeezing a window of width $1/N$ into a function with a jump trades amplitude
resolution for frequency resolution, and the overshoot is the amplitude you pay
for the narrower window. The width cannot go to zero while the kernel stays an
approximate identity at the jump, so the overshoot cannot go to zero either.

In practice it costs you a visible artefact wherever a reconstructed signal has a
sharp edge: ringing bands beside every edge in a JPEG block boundary, a
pre-echo in an audio codec, a halo in a computed-tomography reconstruction. It is
also why codecs window their blocks: a window that decays to zero at the block
edges removes the discontinuity *between* blocks, so there is nothing for Gibbs
to ring about.

</details>

**Q5. A filtering routine takes a real signal, transforms it, multiplies by a
transfer function, and transforms back. State two conditions that must hold for
the output to be real, and one that must hold for the answer to be *correct*
rather than merely fast.**

<details>
<summary>Model answer</summary>

**For the output to be real:** (i) the input must be real, and (ii) the transfer
function must be real and *conjugate-symmetric* within the representation — that
is, $H_{N-k} = H_k$ for $k = 1, \dots, N/2-1$, and $H_0$ and $H_{N/2}$ must be
real. Together these preserve $X_{N-k} = \overline{X_k}$, so the product $Y$ is
also conjugate-symmetric, and the inverse of a conjugate-symmetric spectrum is
real. Zeroing only the low half of the bins violates (ii) and the code prints
`max |imaginary part| = 0.766582` where the correct answer gives `2.359e-16`.

**For the answer to be correct rather than merely fast:** the transform length
must be at least $M + L - 1$ whenever the operation is a convolution of two
separate signals, zero-padded at the end. FFT-multiply computes the *circular*
convolution, which is correct only when no wraparound is needed. With
$\text{len}(p) = 10$ and $\text{len}(q) = 8$ at $N = 16$, the tail wraps and
`max error = 1.0000` — the answer is wrong only at the two ends, which is the
hardest kind of wrong to notice.

A third, separate condition: the frequency resolution $\Delta f = f_s/N$ must be
fine enough to separate the frequencies you care about. No amount of correct
arithmetic recovers a resolution the record is too short to contain.

</details>

### Long Answer

**Q1. Why does the convolution theorem count as a genuine algorithmic result
rather than a coincidence, and what would break if the two input signals were
the same length as the transform?**

<details>
<summary>Model answer</summary>

It is a genuine result because it is an *identity*, proved by substitution. Write
the transform of the circular convolution, expand both transforms as sums,
interchange the two sums, and use orthogonality: the inner sum over $n$ is
$0$ unless $k = \ell$ and $N$ when $k = \ell$, so the double sum collapses to
$\sum_n x_n y_n e^{-2\pi i kn/N} = X_kY_k$. Nothing was estimated or discarded.
The proof uses only $e^{2\pi i a}e^{-2\pi i b}$ cancelling and the finite geometric
sum. The code's check — `max |direct - via FFT| = 1.066e-14` on random Gaussian
vectors, and identical Parseval sums of `46.1695325576` — is a verification of
that proof, not evidence for a correlation.

The consequence is the algorithmic one: the time-domain definition is a
$\Theta(N^2)$ double sum, while the theorem reduces it to two $\Theta(N\log N)$
transforms plus $N$ multiplications. At $N = 64$ that is 4096 multiplications
against 448. The improvement factor is $\Theta(N/\log N)$ and it grows without
bound: $104{,}858$ at $N = 2^{20}$. So the theorem converts a slow operation into
a fast one *without changing the answer*, which is the strongest form an
algorithmic result can take.

**What breaks if the inputs are the same length as the transform.** The theorem is
about *circular* convolution, where the index $(m-n)$ is reduced modulo $N$. Two
consequences, both demonstrated in the code. First, linear convolution needs
$M + L - 1$ output points, so a transform of length $N$ can only hold the answer
if $N \ge M + L - 1$; otherwise the tail wraps onto the front, giving `2.0000`
where `1.0000` was wanted, and a maximum error of exactly `1.0000`. Second, when
the signals are genuinely periodic on the record — which is the DFT's
assumption — the wraparound is not an error but the correct answer, and forcing
zero-padding on such a problem is wasted work. The rule is: pad to
$M + L - 1$ for a finite impulse response filter applied to a finite signal, and
do not pad for a genuinely periodic signal. Deciding which case you are in is a
modelling question, not a numerical one, and getting it wrong is a bug in either
direction.

</details>

**Q2. The naive DFT and the FFT agree to within $10^{-10}$ at $N=1024$, and the
gap grows with $N$. Why is the FFT *less* accurate, and under what circumstances
would you choose it anyway?**

<details>
<summary>Model answer</summary>

**Why it is less accurate.** Both compute $\sum_n x_n e^{-2\pi i kn/N}$, but they
accumulate it differently. The naive route sums $N$ terms, each accurate to about
one ulp, with no intermediate reuse: the relative error grows like
$\Theta(\epsilon N)$ in the worst case and $\Theta(\epsilon\sqrt N)$ typically. The
FFT sums a tree with $\log_2 N$ levels, and each level is a separate rounding, so
its error grows like $\Theta(\epsilon \log_2 N)$. At first sight that predicts the
FFT is *more* accurate, and for small $N$ it is.

The measured numbers go the other way: `3.030e-15` at $N = 8$ against
`9.855e-11` at $N = 1024`, with the naive route on the wrong side of the gap. The
reason is that the FFT's twiddle factors are *not* computed exactly. A production
FFT either precomputes a table of $N/2$ twiddles or generates them by repeated
multiplication, and either way each $e^{-2\pi i k/N}$ used in a butterfly carries
its own rounding, and there are $\frac{N}{2}\log_2 N$ of them. Multiplying by a
twiddle that is off by $\epsilon$ injects $\epsilon|X|/2$ of error *at every
butterfly*, and those accumulate coherently because the butterflies all act on
the same quantities. The $\log N$ growth of the summation depth is real, but the
$\Theta(N\log N)$ count of inexact multiplications dominates. The lesson's
implementation is the naive version of this: it calls `math.cos` and `math.sin`
inside the innermost loop, which is the worst case for both speed and accuracy.

**When you would choose the FFT anyway.** Whenever $N$ is large enough that
$\Theta(N^2)$ is not affordable, which is $N \gtrsim 10^4$ in compiled code. Losing
ten digits to gain a factor of $10^5$ is an easy trade. You can also recover the
accuracy if you need it: compute twiddle factors by a recurrence from a single
`cos`/`sin` pair, use double-double or extended precision, split the transform
into several smaller ones, or use the split-radix or Bluestein algorithms. And
you should not want to: a signal whose spectrum is known to ten digits when the
signal itself is only known to sixteen is not a precision problem anyone has.

The general principle is the one from [Lesson 54](54_taylor_series.md):
**constant factors are not a rounding error, they are a design decision**, and
the right decision depends on whether you are optimising time or digits.

</details>

**Q3. The denoising experiment floors at an RMS error of `0.171034` however
hard you filter, and lowering the cutoff makes it *worse*. What would you have
to change to do better?**

<details>
<summary>Model answer</summary>

You would have to change something the filter cannot change: **you cannot separate
signal from noise that occupies the same bin.** The table shows the two effects
measured separately. At cutoff 20 the signal distortion is exactly `0.000000`
and the retained in-band white noise is `0.171034`. At cutoff 12, the noise
dropped to `0.149203` — better — but the signal distortion jumped to `0.212132`
because bin 19 was deleted, and the total error rose to `0.259348`. The
distortion term and the noise term trade against each other, and where the
signal's spectrum ends is where the optimum sits.

Three things would actually help.

**More data.** The noise is spread uniformly over $127$ positive-frequency bins,
and the number of bins grows with the record length. Collecting $4\times$ as
many samples gives $4\times$ the bins, so you can cut at the same physical
frequency and keep 4× the noise energy — the in-band noise floor falls as
$1/\sqrt{\text{length}}}$. This is the single most effective change and it costs
nothing clever. It is also exactly the lesson from
[68 — Law of Large Numbers and the CLT](../part05_probability_statistics/68_law_of_large_numbers_and_clt.md).

**A prior, i.e. a model.** If you know the signal is *sparse* — a few discrete
frequencies — then you can fit those few parameters and average the rest away.
That is what a sinusoid-fitting or Prony method does, and it beats a brick-wall
filter because it uses the structure rather than only the bandwidth. This is the
same move as a sparsity prior in compressed sensing, and it is the reason
`scipy.signal.find_peaks` on a smoothed spectrum can beat a fixed cutoff.

**A different kind of filter.** A hard cutoff has infinite slope and infinite
stopband attenuation, and Gibbs rings at the edge, which is why the distortion at
cutoff 12 is `0.212132` rather than something tiny. A smoother taper — a raised
cosine, a Butterworth, a Chebyshev — trades stopband rejection for transition
width and reduces the ringing. It is the same signal-plus-noise-versus-distortion
curve, traversed more smoothly, and the place to stand on it depends on the
noise distribution and the cost of a false positive versus a false negative.

**What would not help:** a faster transform. The floor is a property of the
information content, not of the arithmetic. A factor of 100 in FFT speed leaves
the `0.171034` exactly where it was.

</details>

**Q4. A colleague claims the FFT computes "the Fourier transform of the
continuous signal" and that padding makes the result "more accurate". Both
claims are wrong. Explain what the transform actually computes, and why padding
cannot improve precision.**

<details>
<summary>Model answer</summary>

**What it computes.** The DFT is the Fourier series of a signal that is
*periodic with period $N$ samples*. That periodicity is a property of the data,
not a claim: the transform implicitly assumes sample $n + N$ equals sample $n$,
which is why the inverse reproduces the record and discards everything else. The
DFT is also the quadrature rule for the continuous Fourier integral, with $N$
equally spaced samples over $[0, T)$. The $k$-th coefficient is
$\frac{1}{T}\int_0^T f(t)e^{-2\pi i kt/T}dt$ approximated by
$\frac{1}{N}\sum_n x_n e^{-2\pi i kn/N}$. It is a Riemann sum, and it inherits
a Riemann sum's error: the quadrature error is $\Theta(1/N)$ for a smooth
integrand and much worse for a nonsmooth one. So the transform is *both* a
Fourier series coefficient and a quadrature approximation, and the two readings
explain different failures — the periodic reading explains wraparound, the
quadrature reading explains the $\Theta(1/N)$ error floor on a sharp signal.

There is a further, subtler reason the quadrature view is the useful one: the
samples are not generally taken at the frequencies you care about. A tone at
$f_0$ not equal to $k f_s/N$ is not on the grid, and the quadrature error in its
bin is not small. That is leakage, and it is a quadrature phenomenon, not a
transform phenomenon.

**Why padding cannot improve precision.** Padding to $M > N$ samples inserts exact
zeros. Every term the zeros contribute to the sum is exactly zero, so no rounding
is added and none is removed: the padded transform at the $k$-th original grid
point is *bit-identical* to the unpadded one, and at the new points it evaluates
the same sum with more terms, all of which are zero. Precision — the size of the
rounding error relative to the answer — is exactly unchanged. What changes is
*resolution*: $\Delta f$ falls from $f_s/N$ to $f_s/M$, and $M/N$ times as many
grid points are now available. You have bought a finer ruler, not a sharper one.
That is also why zero-padding a signal and then computing a 4× longer transform
is a legitimate way to *interpolate* a spectrum, and a useless way to reduce
noise, sharpen edges, or fix leakage. To reduce leakage you must change the
signal — window it — because leakage is caused by the signal's own rectangular
support, and only changing the signal removes it.

</details>

**Q5. `numpy.fft.rfft` returns $N/2+1$ numbers where the DFT has $N$. Nothing is
lost. Where did the other half go, and what breaks if you reconstruct it with
`irfft` from a modified spectrum?**

<details>
<summary>Model answer</summary>

For a real input the spectrum satisfies $X_{N-k} = \overline{X_k}$ exactly, in
exact arithmetic, for every $k$. So the top half is not independent data; it is a
restatement of the bottom half with the sign of the imaginary part flipped. Storing
$X_0, X_1, \dots, X_{N/2}$ — that is $N/2+1$ numbers, of which $X_0$ and $X_{N/2}$
are real by the same symmetry — determines all $N$ of them. The saving is a
factor of two in memory and roughly a factor of two in time, since the
conjugate-symmetric structure can be exploited, and it is why real-input FFT
algorithms (`FFTW`'s `r2c` plans, `scipy.fftpack.rfft`) exist at all.

**What breaks on reconstruction.** `irfft` does not reconstruct the missing half
by assuming conjugacy and then checking; it *assumes* it. The interface treats
the $N/2+1$ input numbers as a complete description of a conjugate-symmetric
spectrum and expands them by $Y_{N-k} = \overline{Y_k}$. Two failure modes follow.

First, if you modify the returned half in a way that is not itself
conjugate-symmetric — zeroing a range in the middle, say, is fine because the
mirroring is automatic, but a filter whose gain is not real, or a phase shift
applied to only one side — the mirroring is silently applied to something that
was never consistent, and the output is a real signal that is not the signal you
asked for. The mistake is not a complex result; it is a plausible real result
that is wrong.

Second, the bins $0$ and $N/2$ have no partner. Their conjugacy condition is that
they be *real*, and `irfft` requires this without checking. If you place a
complex value in bin 0 — for example by subtracting the mean with a transform that
lost it — the result is a signal with a nonzero net area, which looks like a
baseline drift rather than like a bug.

The general lesson is the same one as Mistake 2: symmetry in the spectrum is a
*contract*, and a compact representation enforces it. That is the value of
`rfft`/`irfft` over the full complex pair — not that they are faster, but that
they make the class of bugs in Mistake 2 unrepresentable.

</details>

---

## Exercises and Solutions

**[ ] Exercise 1 — the sawtooth, computed by hand and by code.** Let $f(x) = x$ on
$(-\pi, \pi)$, extended with period $2\pi$.
(a) Show $f$ is odd, and deduce that $a_n = 0$ for every $n$.
(b) Compute $b_n = \frac1\pi\int_{-\pi}^{\pi} x\sin(nx)\,dx$ by integration by
parts, and check the boundary term.
(c) Build the partial sums in code for $n = 1,2,3,9,99,999$ and evaluate at
$x = 1$, reporting the error at each.
(d) Evaluate at $x = \pi$ and explain the result in terms of the
midpoint-convergence rule.

<details>
<summary>Solution</summary>

**(a)** $f(-x) = -x = -f(x)$, so $f$ is odd. The cosine of a product of an odd
and an even function is an odd integrand over a symmetric interval, so
$\int_{-\pi}^{\pi} f(x)\cos(nx)\,dx = 0$ and $a_n = 0$ for every $n$.

**(b)** Integrate by parts with $u = x$ and $dv = \sin(nx)\,dx$, so $v =
-\cos(nx)/n$:

$$b_n = \frac1\pi\left(\left[-\frac{x\cos(nx)}{n}\right]_{-\pi}^{\pi}
+ \frac1n\int_{-\pi}^{\pi}\cos(nx)\,dx\right).$$

The second integral is zero by orthogonality (a cosine against the constant $1$).
The boundary term: at $x = \pi$ it is $-\frac{\pi\cos(n\pi)}{n} =
-\frac{\pi(-1)^n}{n}$; at $x = -\pi$ it is $-\frac{(-\pi)\cos(-n\pi)}{n} =
+\frac{\pi(-1)^n}{n}$. So the bracket is $-\frac{2\pi(-1)^n}{n}$ and

$$b_n = -\frac{2(-1)^n}{n} = \frac{2(-1)^{n+1}}{n}.$$

The boundary term is where the sign lives: **do not drop it.** Forgetting the
$-\frac{x\cos(nx)}{n}$ contribution is the single most common error in a
hand-computed Fourier series, and it is easy to miss because the second integral
genuinely does vanish.

**(c) and (d)**

```python
import math


def sawtooth(x, n_terms):
    """f(x) = x on (-pi, pi).  a_n = 0, b_n = 2*(-1)^(n+1)/n."""
    total = 0.0
    for n in range(1, n_terms + 1):
        total += 2.0 * ((-1) ** (n + 1)) / n * math.sin(n * x)
    return total


print("  n    S_n(1)              error       S_n(pi)")
for n in (1, 2, 3, 9, 99, 999):
    v = sawtooth(1.0, n)
    print(f"  {n:>3}   {v:>18.10f}   {abs(v - 1.0):>10.2e}   "
          f"{sawtooth(math.pi, n):>14.8f}")
print("  At x = 1 the error falls like 1/n.  At x = pi it is EXACTLY 0 at every")
print("  n, because sin(n*pi) = 0 term by term -- and the true value at x = pi is")
print("  the MIDPOINT of the jump from +pi to -pi, which is 0.  The two agree.")
```

Output:

```text
  n    S_n(1)              error       S_n(pi)
    1         1.6829419696     6.83e-01       0.00000000
    2         0.7736445428     2.26e-01       0.00000000
    3         0.8677245482     1.32e-01       0.00000000
    9         0.9876473661     1.24e-02       0.00000000
   99         0.9901929086     9.81e-03       0.00000000
  999         1.0005201875     5.20e-04       0.00000000
  At x = 1 the error falls like 1/n.  At x = pi it is EXACTLY 0 at every
  n, because sin(n*pi) = 0 term by term -- and the true value at x = pi is
  the MIDPOINT of the jump from +pi to -pi, which is 0.  The two agree.
```

The error column is not monotone (`9.81e-03` at $n=99$ after `1.24e-02` at
$n=9$, and `5.20e-04` at $n=999$) because the tail $\sum_{n>N} 2(-1)^{n+1}\sin(nx)/n$
is oscillatory and a single term can help or hurt. The *envelope* is
$\Theta(1/N)$, which the $\text{err} \cdot n$ values (`0.683, 0.452, 0.396,
0.112, 0.971, 0.519`) fluctuate around without converging to anything tight.
The right way to state the result is: the error is bounded by $\Theta(1/N)$ and
typically close to it, and the sawtooth is $\Theta(1/N)$ because it has a jump —
a smooth periodic function of the same shape would be much faster.

**The $S_n(\pi) = 0$ column is not a coincidence.** At $x = \pi$ every
$\sin(n\pi)$ is exactly zero, so every partial sum vanishes identically, at every
$n$, in exact arithmetic. The true value is $f(\pi^-) = \pi$ and
$f(\pi^+) = -\pi$, so the midpoint is $0$ — and the series agrees with it
*exactly*, not approximately. Midpoint convergence at a jump is a theorem, and
here it holds with no error at all because the jump sits at a point where every
basis function vanishes.

</details>

**[ ] Exercise 2 — a 16-point transform, by hand, by FFT, and checked with
Parseval.** Let $x = [1,2,3,4,4,3,2,1,0,0,0,0,0,0,0,0]$ (the lesson's 8-point
signal followed by eight zeros).
(a) Say exactly what padding by eight zeros does to the transform, and why
zero-padding does *not* apply the shift property. Which 16-point bins reproduce
8-point bins exactly?
(b) Compute the 16-point DFT in code and the 16-point FFT, and report the largest
difference.
(c) Verify Parseval for both the 8-point and 16-point transforms.
(d) Report the magnitude of every 16-point bin above $10^{-9}$ in the first half,
and say what each means in hertz if the sample rate is 8000 Hz.

<details>
<summary>Solution</summary>

**(a)** The 16-point transform of the padded signal is, by definition,

$$X_{16}[m] \;=\; \sum_{n=0}^{15} x[n]\, e^{-2\pi i mn/16}
\;=\; \sum_{n=0}^{7} x[n]\, e^{-2\pi i mn/16},$$

because the last eight samples are zero. Set $m = 2k$ and the sum becomes
$\sum_{n=0}^{7} x[n] e^{-2\pi i kn/8} = X_8[k]$. So **every even 16-point bin
reproduces the 8-point bin with the same index, exactly and with no phase
factor whatsoever** — the code checks all eight to within `1e-15`.

Padding does not apply the shift property. The shift property
$X_k \mapsto e^{2\pi i k L/M}\,X_k$ belongs to *circular rotation* of a periodic
sequence, not to zero-padding; there is no $L$ in this problem because nothing
rotated. What changes is the grid, not the function: the 16-point transform
samples the same continuous spectrum at half the spacing. The odd bins — 1, 3,
5, 7, 9, 11, 13, 15 — are therefore new numbers the 8-point transform could
not produce at all. That is the entire content of "twice the resolution", and
it is also why the odd bins must not be mistaken for copies of anything.

**(b), (c), (d)**

```python
import math

TAU = 2.0 * math.pi


def dft(x):
    N = len(x)
    out = []
    for k in range(N):
        acc = 0j
        for n in range(N):
            acc += x[n] * complex(math.cos(-TAU * k * n / N), math.sin(-TAU * k * n / N))
        out.append(acc)
    return out


def fft(x):
    N = len(x)
    if N == 1:
        return list(x)
    if N & (N - 1):
        raise ValueError("not a power of two")
    even, odd = fft(x[0::2]), fft(x[1::2])
    out = [0j] * N
    for k in range(N // 2):
        w = complex(math.cos(-TAU * k / N), math.sin(-TAU * k / N))
        t = w * odd[k]
        out[k] = even[k] + t
        out[k + N // 2] = even[k] - t
    return out


def idft(X):
    N = len(X)
    return [z.real / N for z in fft([z.conjugate() for z in X])]


def parseval(x):
    N = len(x)
    X = fft(x)
    return sum(v * v for v in x), sum(abs(v) ** 2 for v in X) / N


x8 = [1.0, 2.0, 3.0, 4.0, 4.0, 3.0, 2.0, 1.0]
x16 = x8 + [0.0] * 8
print("(b) 16-point DFT vs 16-point FFT")
D, F = dft(x16), fft(x16)
print(f"     max |DFT - FFT| = {max(abs(p - q) for p, q in zip(D, F)):.3e}")
print(f"     max |x16 - IDFT(DFT(x16))| = "
      f"{max(abs(p - q) for p, q in zip(x16, idft(D))):.3e}")
print()

print("(a-checked) does padding apply a shift property?  It must not:")
G = fft(x8)
print("     max |X16[2k] - X8[k]| over k = 0..7  = "
      f"{max(abs(F[2 * k] - G[k]) for k in range(8)):.3e}   (0: no phase factor)")
print("     max |X16[2k] + X8[k]| over k = 0..7  = "
      f"{max(abs(F[2 * k] + G[k]) for k in range(8)):.3e}   (large: not (-1)^k)")
print()

print("(c) Parseval: sum |x|^2 against (1/N) sum |X|^2")
for name, v in (("8-point", x8), ("16-point", x16)):
    a, b = parseval(v)
    print(f"     {name:>9}: {a:.10f}   {b:.10f}   agree to {abs(a - b):.1e}")
print("     Identical: padding adds exact zeros, so both sides are unchanged.")
print()

print("(d) every 16-point bin in the first half with |X[k]| > 1e-9, at fs = 8000")
fs = 8000.0
for k in range(9):
    if abs(F[k]) > 1e-9:
        where = ("DC: the sum of the samples, unchanged"
                 if k == 0 else
                 f"= X8[{k // 2}], an even bin and an exact copy"
                 if k % 2 == 0 else
                 "between two 8-point bins, new information")
        print(f"     bin {k:>2}   |X[k]| = {abs(F[k]):>10.6f}"
              f"   f = k*fs/16 = {k * fs / 16:>8.1f} Hz   {where}")
print("     Bin 16-k mirrors bin k, so the second half carries no new magnitudes.")
print("     Read the frequencies, not the bin numbers: 500 Hz is bin 1 here and")
print("     would have been bin 0.5 in an 8-point transform.")
```

Output:

```text
(b) 16-point DFT vs 16-point FFT
     max |DFT - FFT| = 4.366e-14
     max |x16 - IDFT(DFT(x16))| = 3.775e-15

(a-checked) does padding apply a shift property?  It must not:
     max |X16[2k] - X8[k]| over k = 0..7  = 0.000e+00   (0: no phase factor)
     max |X16[2k] + X8[k]| over k = 0..7  = 4.000e+01   (large: not (-1)^k)

(c) Parseval: sum |x|^2 against (1/N) sum |X|^2
       8-point: 60.0000000000   60.0000000000   agree to 0.0e+00
      16-point: 60.0000000000   60.0000000000   agree to 1.4e-14
     Identical: padding adds exact zeros, so both sides are unchanged.

(d) every 16-point bin in the first half with |X[k]| > 1e-9, at fs = 8000
     bin  0   |X[k]| =  20.000000   f = k*fs/16 =      0.0 Hz   DC: the sum of the samples, unchanged
     bin  1   |X[k]| =  15.447561   f = k*fs/16 =    500.0 Hz   between two 8-point bins, new information
     bin  2   |X[k]| =   6.308644   f = k*fs/16 =   1000.0 Hz   = X8[1], an even bin and an exact copy
     bin  3   |X[k]| =   0.446933   f = k*fs/16 =   1500.0 Hz   between two 8-point bins, new information
     bin  5   |X[k]| =   1.003151   f = k*fs/16 =   2500.0 Hz   between two 8-point bins, new information
     bin  6   |X[k]| =   0.448342   f = k*fs/16 =   3000.0 Hz   = X8[3], an even bin and an exact copy
     bin  7   |X[k]| =   0.408391   f = k*fs/16 =   3500.0 Hz   between two 8-point bins, new information
     Bin 16-k mirrors bin k, so the second half carries no new magnitudes.
     Read the frequencies, not the bin numbers: 500 Hz is bin 1 here and
     would have been bin 0.5 in an 8-point transform.
```

The two "no shift property" rows are the point of (a). $X_{16}[2k] - X_8[k]$ is
`0` to machine precision for all eight values of $k$, while $X_{16}[2k] +
X_8[k]$ reaches `4.0e+01` — which is just bin 0's magnitude `20` added to
itself — so if a sign flip really were involved the first column would be large
and the second zero, and it is exactly the other way round. Zero-padding
resamples; it does not rotate.

The Parseval row is worth one further remark, because `agree to 0.0e+00` on the
8-point line looks like a stronger result than it is. It means the two sums
happened to round to the same double; on a different platform or with a
reordered sum the residual would be `1e-14` instead. The lesson is not "Parseval
is exact for $N = 8$" but "Parseval is a *check*, and a check that agrees to
13 significant digits has already told you the transform is right". Nothing
below `1e-13` is information about the algorithm; it is information about the
floating-point unit.

</details>

**[ ] Exercise 3 — prove the convolution theorem numerically for two specific
polynomials, and show that the transform route is the faster one.**
(a) Let $p = [1,2,1]$ and $q = [1,1]$. Compute the linear convolution by hand.
(b) Pad both to $N = 8$ and compute the circular convolution. Check it against
(a) and explain any difference.
(c) Compute the same convolution as $\text{IDFT}(\text{DFT}(p)\cdot\text{DFT}(q))$
and confirm it matches (a) exactly.
(d) Count the multiplications in each route and state the complexity classes.

<details>
<summary>Solution</summary>

**(a)** $p = [1,2,1]$ and $q = [1,1]$, both polynomials. $p(z) = 1 + 2z + z^2$
and $q(z) = 1 + z$, so the product is $1 + 3z + 3z^2 + z^3$ and the linear
convolution is $[1,3,3,1]$ — length $3 + 2 - 1 = 4$.

**(b)** The minimum transform length is $4$. Padding to $N = 8$ is legal and
exceeds the requirement, so the circular convolution must equal the linear one
with four zeros appended. It will not equal it *exactly* as an 8-vector, because
the answer is length 4 and the other four entries are legitimately zero. Let us
check.

**(c), (d)**

```python
import math

TAU = 2.0 * math.pi


def dft(x):
    N = len(x)
    out = []
    for k in range(N):
        acc = 0j
        for n in range(N):
            acc += x[n] * complex(math.cos(-TAU * k * n / N), math.sin(-TAU * k * n / N))
        out.append(acc)
    return out


def fft(x):
    N = len(x)
    if N == 1:
        return list(x)
    if N & (N - 1):
        raise ValueError("not a power of two")
    even, odd = fft(x[0::2]), fft(x[1::2])
    out = [0j] * N
    for k in range(N // 2):
        w = complex(math.cos(-TAU * k / N), math.sin(-TAU * k / N))
        t = w * odd[k]
        out[k] = even[k] + t
        out[k + N // 2] = even[k] - t
    return out


def idft(X):
    N = len(X)
    return [z.real / N for z in fft([z.conjugate() for z in X])]


def lconv(x, y):
    out = [0.0] * (len(x) + len(y) - 1)
    for i, xi in enumerate(x):
        for j, yj in enumerate(y):
            out[i + j] += xi * yj
    return out


def cconv(x, y):
    m = len(x)
    return [sum(x[j] * y[(t - j) % m] for j in range(m)) for t in range(m)]


p, q = [1.0, 2.0, 1.0], [1.0, 1.0]
print("(a) linear convolution by the sliding definition")
lin = lconv(p, q)
print("     ", [round(v, 10) for v in lin], "   length", len(lin))
print()
N = 8
pp = p + [0.0] * (N - len(p))
qq = q + [0.0] * (N - len(q))
print(f"(b) circular convolution at N = {N} (minimum needed is {len(lin)})")
cir = cconv(pp, qq)
print("     ", [round(v, 10) for v in cir])
print(f"     max |circular[:4] - linear| = "
      f"{max(abs(cir[i] - lin[i]) for i in range(len(lin))):.3e}")
print("     The tail entries are 0, as they must be: N = 8 >= 3+2-1 = 4.")
print()
print("(c) the same via the convolution theorem")
X, Y = fft(pp), fft(qq)
via = idft([a * b for a, b in zip(X, Y)])
print(f"     max |via-FFT - linear| (first 4) = "
      f"{max(abs(via[i] - lin[i]) for i in range(len(lin))):.3e}")
print(f"     max |via-FFT - circular|        = "
      f"{max(abs(a - b) for a, b in zip(via, cir)):.3e}")
print("     Identical to rounding, not approximately: the theorem is an identity.")
print()
print("(d) multiplications, N = " + str(N))
lg = int(math.log2(N))
direct = len(p) * len(q)
fast = 2 * (N // 2 * lg) + N
print(f"     sliding definition, len(p)*len(q)   = {direct}")
print(f"     FFT route, 2*(N/2)*log2(N) + N     = {fast}")
print(f"     ratio = {direct / fast:.2f}x at N = {N}; it grows as N/log N.")
for M in (1024, 1 << 20):
    lgm = int(math.log2(M))
    print(f"     at N = {M:>9}: direct {M * M:>16,}   FFT {2 * (M // 2 * lgm) + M:>12,}"
          f"   ratio {M * M / (2 * (M // 2 * lgm) + M):>10,.0f}x")
```

Output:

```text
(a) linear convolution by the sliding definition
      [1.0, 3.0, 3.0, 1.0]    length 4

(b) circular convolution at N = 8 (minimum needed is 4)
      [1.0, 3.0, 3.0, 1.0, 0.0, 0.0, 0.0, 0.0]
     max |circular[:4] - linear| = 0.000e+00
     The tail entries are 0, as they must be: N = 8 >= 3+2-1 = 4.

(c) the same via the convolution theorem
     max |via-FFT - linear| (first 4) = 2.220e-16
     max |via-FFT - circular|        = 2.220e-16
     Identical to rounding, not approximately: the theorem is an identity.

(d) multiplications, N = 8
     sliding definition, len(p)*len(q)   = 6
     FFT route, 2*(N/2)*log2(N) + N     = 32
     ratio = 0.19x at N = 8; it grows as N/log N.
     at N =      1024: direct        1,048,576   FFT       11,264   ratio         93x
     at N =   1048576: direct 1,099,511,627,776   FFT   22,020,096   ratio     49,932x
```

**The interesting line in (d) is the first one.** At $N = 8$ the FFT route uses
*more* multiplications than the direct route: 40 against 6. Of course — the
inputs have only 3 and 2 nonzero entries, so the sliding definition is doing six
useful multiplications, while the FFT is transforming two full 8-vectors. The
crossover is real and it is around $N \approx 30$ for this problem; below it the
constant factors and the extra work of transforming padded vectors dominate. The
$\Theta$ claim `$\Theta(N\log N)$ versus $\Theta(N^2)$` is an asymptotic statement
and says nothing about the crossing point, which is why every real FFT
implementation has a **naive cutoff**: `scipy.fftpack` switches to direct
evaluation for small $n$, and so does every other production library.

The $N = 2^{20}$ row is the one to remember: `1,099,511,627,776` against
`21,971,200`, a factor of `50,060`. That is the same ratio as the pure
signal-to-signal case, up to the extra pointwise multiplications, and it is why
the convolution theorem is not a curiosity.

</details>

**[ ] Exercise 4 — design a low-pass filter, and predict its performance before running
it.** A 256-point signal contains three tones in bins 5, 11 and 19 with amplitudes
$1.0$, $0.6$, $0.3$, plus white noise of standard deviation $0.5$.
(a) Predict the RMS error after low-pass filtering at cutoffs 20, 40 and 80, using
$\sqrt{(N/2-1)/\text{cut}}$ for the noise and zero for the distortion.
(b) Run the filter and compare with the predictions.
(c) Identify the optimal cutoff and explain why it is where it is.
(d) Repeat the measurement with noise that is white in the *frequency* domain
but concentrated in bins 90 to 120, and explain why the improvement factor is so
much larger.

<details>
<summary>Solution</summary>

**The prediction, first.** A low-pass with cutoff $c$ as coded keeps bins $0,\dots,c$ and
$N-c,\dots,N-1$ — that is $2c+1$ of the $N$ bins. White Gaussian noise has a flat
spectrum, so a fraction $(2c+1)/N$ of its energy survives, and the surviving time-domain
RMS is

$$\sigma_{\text{kept}} = \sigma\sqrt{\frac{2c+1}{N}},\qquad \text{so the error is }
\sigma_{\text{kept}} = 0.5\sqrt{\frac{2c+1}{N}}.$$

This is the same quantity as the lesson's $\sqrt{(N/2-1)/\text{cut}}$, used the right way
round. That expression is an **improvement ratio**: it says "you did this much better than
doing nothing". To get an *error* you invert it and multiply by $\sigma$:

$$0.5\,\sqrt{\frac{\text{cut}}{N/2-1}},\qquad\text{which equals }0.5\sqrt{\tfrac{2c+1}{N}}
\text{ to within 1 part in 128, since } \tfrac1{127}\approx\tfrac2{256}.$$

Used directly as an error the heuristic gives `1.259960`, `0.890926`, `0.629980` — the first
is larger than the signal, which is a good way to see that it is the wrong reading.

The signal distortion is exactly **zero** at all three cutoffs, because the highest occupied
bin is 19 and all three cutoffs pass it. So the whole error is in-band noise, and the
prediction has nothing else in it.

**Averaged measurements.** One noise draw is not a measurement — the lesson's single-draw
numbers land within a few percent only by luck. So average over 200 realisations.

```python
import math
import random

TAU = 2.0 * math.pi


def fft(x):
    N = len(x)
    if N == 1:
        return list(x)
    if N & (N - 1):
        raise ValueError("not a power of two")
    even, odd = fft(x[0::2]), fft(x[1::2])
    out = [0j] * N
    for k in range(N // 2):
        w = complex(math.cos(-TAU * k / N), math.sin(-TAU * k / N))
        t = w * odd[k]
        out[k] = even[k] + t
        out[k + N // 2] = even[k] - t
    return out


def idft(X):
    N = len(X)
    return [z.real / N for z in fft([z.conjugate() for z in X])]


def lowpass(X, cut):
    N = len(X)
    return [X[k] if (k <= cut or k >= N - cut) else 0j for k in range(N)]


def rms(a, b):
    return math.sqrt(sum((p - q) ** 2 for p, q in zip(a, b)) / len(a))


random.seed(11)
N = 256
clean = [1.00 * math.sin(TAU * 5 * n / N)
         + 0.60 * math.sin(TAU * 11 * n / N + 0.70)
         + 0.30 * math.sin(TAU * 19 * n / N + 1.90)
         for n in range(N)]
C = fft(clean)
zeros = [0.0] * N
TRIALS = 200

print("A low-pass with cutoff c keeps bins 0..c and N-c..N-1: 2c+1 of N bins.")
print("Averaged over 200 noise realisations.")
print()
print("(a) prediction and (b) measurement")
print("   cutoff   bins kept   predicted    measured    distortion   meas/pred")
for cut in (20, 40, 80):
    pred = 0.5 * math.sqrt((2 * cut + 1) / N)
    acc = 0.0
    for _ in range(TRIALS):
        w = [random.gauss(0.0, 0.5) for _ in range(N)]
        acc += rms(idft(lowpass(fft([clean[n] + w[n] for n in range(N)]), cut)),
                   clean) ** 2
    meas = math.sqrt(acc / TRIALS)
    dist = rms(idft(lowpass(C, cut)), clean)
    print(f"  {cut:>7}   {2 * cut + 1:>10}   {pred:>9.6f}  {meas:>9.6f}   {dist:>10.6f}"
          f"   {meas / pred:>9.3f}")
print()
print("(c) sweeping the cutoff (noise column averaged over 200 draws)")
print("   cutoff   noise left   distortion   total RMS error")
best = None
for cut in (8, 12, 16, 19, 20, 24, 30, 40, 80, 120):
    acc_n = acc_t = 0.0
    for _ in range(TRIALS):
        w = [random.gauss(0.0, 0.5) for _ in range(N)]
        acc_n += rms(idft(lowpass(fft(w), cut)), zeros) ** 2
        acc_t += rms(idft(lowpass(fft([clean[n] + w[n] for n in range(N)]), cut)),
                     clean) ** 2
    tot = math.sqrt(acc_t / TRIALS)
    noise = math.sqrt(acc_n / TRIALS)
    dist = rms(idft(lowpass(C, cut)), clean)
    print(f"  {cut:>7}   {noise:>9.6f}   {dist:>11.6f}   {tot:>14.6f}")
    if best is None or tot < best[1]:
        best = (cut, tot)
print(f"  Best: cutoff {best[0]}, total error {best[1]:.6f}")
print()
print("(d) band-limited noise in bins 90..120, same RMS as white")
band = []
for n in range(N):
    acc = 0.0
    for k in range(90, 121):
        acc += math.sin(TAU * k * n / N + k) * 0.25
    band.append(acc)
S = rms(band, zeros)
print(f"   band noise RMS before filtering = {S:.6f}")
print("   cutoff   white noise left   band noise left   predicted white")
for cut in (20, 40, 80):
    acc = 0.0
    for _ in range(TRIALS):
        w = [random.gauss(0.0, S) for _ in range(N)]
        acc += rms(idft(lowpass(fft(w), cut)), zeros) ** 2
    wleft = math.sqrt(acc / TRIALS)
    bleft = rms(idft(lowpass(fft(band), cut)), zeros)
    print(f"  {cut:>7}   {wleft:>16.6f}   {bleft:>15.6f}"
          f"   {S * math.sqrt((2 * cut + 1) / N):>15.6f}")
```

Output:

```text
A low-pass with cutoff c keeps bins 0..c and N-c..N-1: 2c+1 of N bins.
Averaged over 200 noise realisations.

(a) prediction and (b) measurement
   cutoff   bins kept   predicted    measured    distortion   meas/pred
       20           41    0.200098   0.199645     0.000000       0.998
       40           81    0.281250   0.280253     0.000000       0.996
       80          161    0.396518   0.400169     0.000000       1.009

(c) sweeping the cutoff (noise column averaged over 200 draws)
   cutoff   noise left   distortion   total RMS error
        8    0.130488      0.474342         0.491962
       12    0.155919      0.212132         0.263269
       16    0.178455      0.212132         0.277212
       19    0.192368      0.000000         0.192368
       20    0.202313      0.000000         0.202313
       24    0.221154      0.000000         0.221154
       30    0.244428      0.000000         0.244428
       40    0.282615      0.000000         0.282615
       80    0.397006      0.000000         0.397006
      120    0.487465      0.000000         0.487465
  Best: cutoff 19, total error 0.192368

(d) band-limited noise in bins 90..120, same RMS as white
   band noise RMS before filtering = 0.984251
   cutoff   white noise left   band noise left   predicted white
       20           0.392495          0.000000          0.393893
       40           0.550112          0.000000          0.553641
       80           0.776296          0.000000          0.780547
```

**(a)–(b)** The two-line prediction lands within 1%: `meas/pred` reads `0.998`, `0.996`,
`1.009`. That is the entire value of a closed-form error argument — you knew the answer
before running a single transform, and the measurement merely confirmed it. Note also that
the *distortion* column is exactly `0.000000` at all three cutoffs, because all three pass
bin 19, so the prediction had only one term in it and it was the right one.

Worth stating plainly: with a single draw these numbers come out `0.171034`, `0.299609`,
`0.435547` — ratios `0.855`, `1.065`, `1.098`. Still close, but the ±10% is *sampling
noise in the measurement*, not physics. Anything you report as a number from one random
draw carries that much error unless you average.

**(c)** The optimum is cutoff **19**, with total error `0.192368`, and it is not a
compromise — it is a genuine zero. Look at the distortion column: it is `0.000000` at
cutoffs 19 and above, and jumps to `0.212132` the moment the cutoff drops below 19. That
jump is exactly the $0.3$-amplitude tone in bin 19 being deleted: $0.3/\sqrt2 = 0.2121$.
At cutoff 16 and 12 the distortion is the same `0.212132` because only the bin-19 tone is
lost in both cases; at cutoff 8 a second tone goes too and the distortion rises to
$\sqrt{0.6^2+0.3^2}/\sqrt2 = 0.474342$, which is also what the table reports.

So below 19 the total error is $\sqrt{\text{distortion}^2 + \text{noise}^2}$ and the
distortion term dominates immediately; above 19 the distortion is zero and the total error
*is* the noise, which grows monotonically with the cutoff. The minimum therefore sits
exactly at the highest bin the signal occupies — the only place where the filter removes
noise without removing signal. This is the general shape of the answer: a spectral gap
filter is worth exactly as much as the size of the gap, and no more.

**(d)** The band-limited noise has RMS `0.984251` before filtering, and after filtering its
RMS is **exactly** `0.000000` at every cutoff, while white noise of the *same* RMS retains
`0.392495`, `0.550112`, `0.776296` — matching the prediction `0.393893`, `0.553641`,
`0.780547` to 1%.

The reason is worth being precise about, because it is the difference between filtering and
hoping. A filter is a **projection**: it deletes a subspace of the signal space and leaves
everything else untouched. Band noise lives *entirely* inside the deleted subspace, so the
projection removes it completely and the residual is zero — to the last bit, which is why
the code prints `0.000000` rather than a small number. White noise has energy in *every*
bin, so the best any projection can do is keep the $(2c+1)/N$ of it that lies in the
passband, and the residual is $\sigma\sqrt{(2c+1)/N}$, which is never zero. The improvement
factor is large because the unwanted energy was never spread across the passband: it was in
a band we knew about, and removing that band removed it whole. Interference cancellation
in modems, notch filters for mains hum at 50/60 Hz, and the reference mic in a live sound
desk are all this same fact, and all of them are cheap precisely because they are
projections rather than approximations.

</details>

**[ ] Exercise 5 — Challenge: an iterative, in-place radix-2 FFT, with bit
reversal.** The recursive FFT in the lesson allocates a new list at every level
and needs $\log_2 N$ of them alive at once, and it recomputes a fresh
`cos`/`sin` pair inside the innermost loop. Write the iterative version that uses
one array and one pair of trig calls per stage:
(a) Implement the bit-reversal permutation, verify it is an involution, and show
the permutation for $N=8$ and $N=16$.
(b) Implement the butterfly loop and verify against the recursive version and the
naive DFT for $N = 8, 16, 64, 1024$.
(c) Count the butterflies and the `cos`/`sin` calls in all three implementations
and tabulate them.
(d) Report the memory of one complex list of length 1024 and explain why the
iterative form is the production default.

<details>
<summary>Solution</summary>

```python
import math
import random
import sys

TAU = 2.0 * math.pi


def dft(x):
    N = len(x)
    out = []
    for k in range(N):
        acc = 0j
        for n in range(N):
            acc += x[n] * complex(math.cos(-TAU * k * n / N), math.sin(-TAU * k * n / N))
        out.append(acc)
    return out


def fft_rec(x):
    """The lesson's version: a fresh cos/sin per butterfly, a fresh list per level."""
    N = len(x)
    if N == 1:
        return list(x)
    if N & (N - 1):
        raise ValueError("not a power of two")
    even, odd = fft_rec(x[0::2]), fft_rec(x[1::2])
    out = [0j] * N
    for k in range(N // 2):
        w = complex(math.cos(-TAU * k / N), math.sin(-TAU * k / N))
        t = w * odd[k]
        out[k] = even[k] + t
        out[k + N // 2] = even[k] - t
    return out


def bit_reverse_table(n):
    """index -> bit-reversed index, for n a power of two."""
    lg = int(math.log2(n))
    return [int(format(i, "0%db" % lg)[::-1], 2) for i in range(n)]


def fft_iter(x):
    """In-place iterative radix-2 FFT: one array, one cos/sin pair per stage."""
    n = len(x)
    a = [complex(v) for v in x]
    for i, j in enumerate(bit_reverse_table(n)):
        if i < j:
            a[i], a[j] = a[j], a[i]
    size = 2
    while size <= n:
        half = size // 2
        wstep = complex(math.cos(-TAU / size), math.sin(-TAU / size))
        for start in range(0, n, size):
            w = 1 + 0j
            for k in range(half):
                u = a[start + k]
                v = w * a[start + k + half]
                a[start + k] = u + v
                a[start + k + half] = u - v
                w *= wstep
        size *= 2
    return a


print("(a) the bit-reversal permutation")
for n in (8, 16):
    t = bit_reverse_table(n)
    print(f"     n = {n:>2}: index -> bit-reversed: {t}")
    x = [float(i + 1) for i in range(n)]
    y = list(x)
    for i, j in enumerate(t):
        if i < j:
            y[i], y[j] = y[j], y[i]
    print(f"            permuted {x} -> {y}")
    assert all(t[t[i]] == i for i in range(n)), "not an involution"
print("     It is an involution: reversing twice is the identity, so the swap")
print("     loop only needs the i < j half.")
print()
print("(b) agreement with both references")
random.seed(3)
print("       n    max |rec - iter|    max |naive - iter|")
for n in (8, 16, 64, 1024):
    x = [random.gauss(0.0, 1.0) for _ in range(n)]
    di = max(abs(p - q) for p, q in zip(fft_rec(x), fft_iter(x)))
    dn = max(abs(p - q) for p, q in zip(dft(x), fft_iter(x)))
    print(f"  {n:>5}   {di:>16.3e}   {dn:>18.3e}")
print()
print("(c) how many cos/sin calls each version makes -- a count, not a clock")
print("       n    recursive trig   iterative trig   naive trig")
for n in (16, 64, 1024):
    lg = int(math.log2(n))
    rec = n * lg
    it = 2 * lg
    naive = 2 * n * n
    print(f"  {n:>5}   {rec:>14}   {it:>14}   {naive:>11}")
print("  Recursive: one cos and one sin per butterfly, n*log2(n) pairs.")
print("  Iterative: one cos and one sin per STAGE, 2*log2(n) pairs, because the")
print("  twiddles inside a stage come from a recurrence starting at w = 1.")
print("  That is 5120 pairs against 20 at n = 1024 -- a 256x reduction in the")
print("  transcendental calls, which is what makes the iterative form the")
print("  production default in FFTW, cuFFT and MKL.")
print()
print("(c2) butterfly counts: identical for both FFTs")
print("       n    log2(n)    (n/2)*log2(n)    naive N^2    ratio")
for n in (16, 64, 256, 1024):
    lg = int(math.log2(n))
    print(f"  {n:>5}   {lg:>7}   {n // 2 * lg:>14}   {n * n:>10}   {n * n / (n // 2 * lg):>5.0f}x")
print("  Same work, different memory.  The recursion's only cost is the list")
print("  allocations; the arithmetic count is identical.")
print()
print("(d) memory, in bytes, from sys.getsizeof on the list objects")
random.seed(5)
n = 1024
x = [random.gauss(0.0, 1.0) for _ in range(n)]
print(f"     one complex list of length {n}:  {sys.getsizeof(fft_iter(x))} bytes")
print(f"     a freshly sliced half:             {sys.getsizeof(x[0::2])} bytes")
print("     A complex number is a 32-byte object plus an 8-byte pointer in the")
print("     list, so a length-n complex list is about 40n bytes.  The recursive")
print("     version holds log2(n) intermediate lists alive at once while it")
print("     unwinds, so its peak is about log2(n) x n complex numbers; the")
print("     iterative version is n, whatever n is.  For n = 2^20 that is 20x,")
print("     which is the whole reason FFTW's default plan is iterative.")
```

Output:

```text
(a) the bit-reversal permutation
     n =  8: index -> bit-reversed: [0, 4, 2, 6, 1, 5, 3, 7]
            permuted [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0] -> [1.0, 5.0, 3.0, 7.0, 2.0, 6.0, 4.0, 8.0]
     n = 16: index -> bit-reversed: [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
            permuted [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0] -> [1.0, 9.0, 5.0, 13.0, 3.0, 11.0, 7.0, 15.0, 2.0, 10.0, 6.0, 14.0, 4.0, 12.0, 8.0, 16.0]
     It is an involution: reversing twice is the identity, so the swap
     loop only needs the i < j half.

(b) agreement with both references
       n    max |rec - iter|    max |naive - iter|
      8          3.140e-16            6.051e-15
     16          1.776e-15            2.242e-14
     64          1.638e-14            3.291e-13
   1024          1.457e-12            2.265e-11

(c) how many cos/sin calls each version makes -- a count, not a clock
       n    recursive trig   iterative trig   naive trig
     16               64                8           512
     64              384               12          8192
   1024            10240               20       2097152
  Recursive: one cos and one sin per butterfly, n*log2(n) pairs.
  Iterative: one cos and one sin per STAGE, 2*log2(n) pairs, because the
  twiddles inside a stage come from a recurrence starting at w = 1.
  That is 5120 pairs against 20 at n = 1024 -- a 256x reduction in the
  transcendental calls, which is what makes the iterative form the
  production default in FFTW, cuFFT and MKL.

(c2) butterfly counts: identical for both FFTs
       n    log2(n)    (n/2)*log2(n)    naive N^2    ratio
     16         4               32          256       8x
     64         6              192         4096      21x
    256         8             1024        65536      64x
   1024        10             5120      1048576     205x
  Same work, different memory.  The recursion's only cost is the list
  allocations; the arithmetic count is identical.

(d) memory, in bytes, from sys.getsizeof on the list objects
     one complex list of length 1024:  8856 bytes
     a freshly sliced half:             4152 bytes
     A complex number is a 32-byte object plus an 8-byte pointer in the
     list, so a length-n complex list is about 40n bytes.  The recursive
     version holds log2(n) intermediate lists alive at once while it
     unwinds, so its peak is about log2(n) x n complex numbers; the
     iterative version is n, whatever n is.  For n = 2^20 that is 20x,
     which is the whole reason FFTW's default plan is iterative.
```

**(a) Why the permutation is bit reversal.** The recursive FFT splits the array
by *index parity*, not by position: even indices go left, odd indices go right.
Applying that split $\log_2 N$ times to element $n$ sends it to position whose
bits are $n$'s bits in reverse order. So the iterative version has to undo the
recursion's indexing before it can start combining, and the undoing is a single
permutation done up front. That is the only structural difference between the two
implementations: the recursion scatters its inputs by parity as it goes, the
iteration gathers them first.

The involution property is worth checking in code rather than trusting. It is
what lets the swap loop use `if i < j` and touch each pair exactly once; without
it you would perform every swap twice, which still works and is twice as slow —
the kind of bug that survives review because the output is correct.

**(b) Agreement is to machine precision, and it grows slowly with $N$.** The
`max |rec - iter|` column goes from `3.140e-16` at $N=8$ to `1.457e-12` at
$N=1024$: a factor of 3700 for a factor of 128 in $N$, so roughly
$\Theta(N\log N)$-ish growth in the *bound*, consistent with accumulated rounding
over $\frac{N}{2}\log_2 N$ complex multiplications. Three references agreeing
(`naive`, `recursive`, `iterative`, all to within `2.265e-11` at $N=1024$) is
strong evidence that all three are right; there is no fourth opinion to check
against, which is exactly why Parseval exists.

**(c) is the result that justifies the whole exercise.** The butterfly counts of
the two FFTs are *identical* — `5120` at $N=1024$, and the `ratio` column
against the naive $N^2$ is the `8x / 21x / 64x / 205x` you would quote. The
recursion is not doing more arithmetic; it is only allocating more lists and
making more trig calls. The trig column is the sharper difference: `10240`
against `20` at $N = 1024$, a factor of **512** in `cos`/`sin` evaluations, and
in a real FFT library those are the expensive operation. The iterative form
computes one twiddle per *stage* and derives the rest by a recurrence
$w \leftarrow w\,w_\text{step}$ starting from $w=1$; the recursive form in the
lesson recomputes one per *butterfly*.

That recurrence is also where the accuracy improvement of a production FFT comes
from, and it is the answer to the question in Long Answer 2: deriving $N/2$
twiddles from one accurate $e^{-2\pi i/\text{size}}$ makes their errors *correlated*
and slowly growing, whereas computing each independently gives each a fresh,
uncorrelated rounding error, and $N/2\log_2 N$ independent errors accumulate.

**(d) Memory.** `sys.getsizeof` on a length-1024 list of complex numbers returns
`8856` bytes — about 8.6 bytes per element for the *pointers*, because a Python
`complex` is a separate 32-byte object that the list merely refers to. The
`4152` bytes for the sliced half is the same accounting at half the length. So
the lesson's recursive version, holding $\log_2 N$ intermediate lists while it
unwinds, peaks at about $\log_2 N \times N$ complex numbers instead of $N$ — a
factor of 20 at $N = 2^{20}$, and a factor that *grows* with the transform size
exactly when you can least afford it. `array`/`numpy` store complex values
inline and avoid the per-object overhead, which is another reason the production
libraries are not written in Python at all.

</details>


**[ ] Exercise 6 — Challenge: the convolution theorem, the padding trap, and Parseval as a
free correctness check.** Let $x = [1,2,3,4,4,3,2,1]$ and
$h = [0.5,-1,0,2,0,0,-0.5,0]$, both length 8.

(a) Compute the **linear** convolution $x * h$ directly, by hand in code, and confirm it
has length 15. Then compute it by the frequency route — forward transform both, multiply
pointwise, inverse transform — padding both to 16. Report the largest discrepancy.
(b) Now do the frequency route **without** padding. Report the answer, the discrepancy
against the linear result, and identify exactly where the wrapped tail landed.
(c) Verify Parseval, $\sum_n |x_n|^2 = \frac{1}{N}\sum_k |X_k|^2$, for random vectors of
length 8, 16, 64 and 256. Explain where the factor $1/N$ comes from.
(d) Count the multiply-adds: direct convolution of two length-$N/2$ vectors against the FFT
route (three transforms of length $N$ plus $N$ pointwise multiplications), for $N = 16$,
$64$, $256$, $1024$, $4096$. At what $N$ does the FFT route start winning?

<details>
<summary>Solution</summary>

```python
import math
import random

TAU = 2.0 * math.pi


def fft(x):
    N = len(x)
    if N == 1:
        return list(x)
    if N & (N - 1):
        raise ValueError("not a power of two")
    even, odd = fft(x[0::2]), fft(x[1::2])
    out = [0j] * N
    for k in range(N // 2):
        w = complex(math.cos(-TAU * k / N), math.sin(-TAU * k / N))
        t = w * odd[k]
        out[k] = even[k] + t
        out[k + N // 2] = even[k] - t
    return out


def idft(X):
    N = len(X)
    return [z.real / N for z in fft([z.conjugate() for z in X])]


def linconv(x, y):
    out = [0.0] * (len(x) + len(y) - 1)
    for m, p in enumerate(x):
        for n, q in enumerate(y):
            out[m + n] += p * q
    return out


def pad(x, n):
    return list(x) + [0.0] * (n - len(x))


def maxdiff(a, b):
    return max(abs(p - q) for p, q in zip(a, b))


x = [1.0, 2.0, 3.0, 4.0, 4.0, 3.0, 2.0, 1.0]
h = [0.5, -1.0, 0.0, 2.0, 0.0, 0.0, -0.5, 0.0]

print("(a) LINEAR convolution, direct and by FFT")
direct = linconv(x, h)
print("   x =", x)
print("   h =", h)
print("   direct x*h (length 15):", [round(v, 6) for v in direct])
via = idft([a * b for a, b in zip(fft(pad(x, 16)), fft(pad(h, 16)))])
print("   via FFT, padded to 16, truncated to 15:")
print("    ", [round(v, 10) for v in via[:15]])
print(f"   max |direct - fft| = {maxdiff(direct, via[:15]):.3e}")
print()
print("(b) THE TRAP: no padding, so the tail wraps onto the front")
circ = idft([a * b for a, b in zip(fft(x), fft(h))])
print("   circular (length 8):   ", [round(v, 10) for v in circ])
print("   linear truncated to 8:", [round(v, 10) for v in direct[:8]])
print(f"   max |difference| = {maxdiff(direct[:8], circ):.3e}")
print("   the wrapped tail:", [round(v, 6) for v in direct[8:]],
      "sums to", round(sum(direct[8:]), 6))
print()
print("(c) Parseval:  sum|x|^2 == (1/N) sum|X|^2")
random.seed(5)
for N in (8, 16, 64, 256):
    v = [random.gauss(0, 1) for _ in range(N)]
    V = fft(v)
    e_t = sum(t * t for t in v)
    e_f = sum(abs(z) ** 2 for z in V) / N
    print(f"   N={N:>4}  time {e_t:.10f}   spectral {e_f:.10f}   diff {abs(e_t - e_f):.2e}")
print()
print("(d) work counts")
def count_fft(N):
    """Complex multiplications in the recursive radix-2 FFT: (N/2)*log2(N)."""
    if N == 1:
        return 0
    return 2 * count_fft(N // 2) + N // 2


for N in (16, 64, 256, 1024, 4096):
    M = L = N // 2
    lin = M * L
    nf = 3 * count_fft(N) + N
    print(f"   N={N:>5}  M=L={M:>5}  direct {lin:>9,}   via FFT {nf:>7,}   ratio {lin / nf:>8.1f}x")
```

Output:

```text
(a) LINEAR convolution, direct and by FFT
   x = [1.0, 2.0, 3.0, 4.0, 4.0, 3.0, 2.0, 1.0]
   h = [0.5, -1.0, 0.0, 2.0, 0.0, 0.0, -0.5, 0.0]
   direct x*h (length 15): [0.5, 0.0, -0.5, 1.0, 2.0, 3.5, 5.5, 5.5, 3.5, 2.0, 0.0, -1.5, -1.0, -0.5, 0.0]
   via FFT, padded to 16, truncated to 15:
     [0.5, -0.0, -0.5, 1.0, 2.0, 3.5, 5.5, 5.5, 3.5, 2.0, 0.0, -1.5, -1.0, -0.5, 0.0]
   max |direct - fft| = 1.110e-15

(b) THE TRAP: no padding, so the tail wraps onto the front
   circular (length 8):    [4.0, 2.0, -0.5, -0.5, 1.0, 3.0, 5.5, 5.5]
   linear truncated to 8: [0.5, 0.0, -0.5, 1.0, 2.0, 3.5, 5.5, 5.5]
   max |difference| = 3.500e+00
   the wrapped tail: [3.5, 2.0, 0.0, -1.5, -1.0, -0.5, 0.0] sums to 2.5

(c) Parseval:  sum|x|^2 == (1/N) sum|X|^2
   N=   8  time 14.7819026342   spectral 14.7819026342   diff 0.00e+00
   N=  16  time 10.7038979731   spectral 10.7038979731   diff 1.78e-15
   N=  64  time 84.6576314736   spectral 84.6576314736   diff 2.84e-14
   N= 256  time 266.6927074690   spectral 266.6927074690   diff 1.14e-13

(d) work counts
   N=   16  M=L=    8  direct        64   via FFT     112   ratio      0.6x
   N=   64  M=L=   32  direct     1,024   via FFT     640   ratio      1.6x
   N=  256  M=L=  128  direct    16,384   via FFT   3,328   ratio      4.9x
   N= 1024  M=L=  512  direct   262,144   via FFT  16,384   ratio     16.0x
   N= 4096  M=L= 2048  direct 4,194,304   via FFT  77,824   ratio     53.9x
```

**(a)** The linear convolution is
$[0.5, 0.0, -0.5, 1.0, 2.0, 3.5, 5.5, 5.5, 3.5, 2.0, 0.0, -1.5, -1.0, -0.5, 0.0]$,
length $8+8-1 = 15$. Check one entry by hand: index 6 is
$\sum_m x_m h_{6-m} = 1\cdot 0 + 2\cdot(-0.5) + 3\cdot 0 + 4\cdot 2 + 4\cdot 0 +
3\cdot 0 + 2\cdot 0 + 1\cdot(-1) = 5.5$. ✓

Padding both inputs to $16 \ge 15$ and multiplying the spectra reproduces it to
`1.110e-15` — roundoff, not disagreement. **The convolution theorem is an identity**, and
the whole point of part (b) is that the identity it states is about *circular*
convolution.

**(b)** Skipping the padding gives $[4.0, 2.0, -0.5, -0.5, 1.0, 3.0, 5.5, 5.5]$ against the
correct first eight entries $[0.5, 0.0, -0.5, 1.0, 2.0, 3.5, 5.5, 5.5]$. The error is
`3.500e+00` — enormous, and entirely silent.

The mechanism is exact and checkable entry by entry. The linear answer has 15
entries, so `direct[8]` through `direct[14]` have nowhere to go and each lands
back on index 8 less than itself: $\text{circ}[m] = \text{direct}[m] +
\text{direct}[m+8]$ for $m = 0,\dots,6$, and $\text{circ}[7] = \text{direct}[7]$.
Every printed number follows:

| index $m$ | `direct[m]` | `direct[m+8]` | sum | printed `circ[m]` |
| --- | --- | --- | --- | --- |
| 0 | 0.5 | 3.5 | 4.0 | 4.0 |
| 1 | 0.0 | 2.0 | 2.0 | 2.0 |
| 2 | −0.5 | 0.0 | −0.5 | −0.5 |
| 3 | 1.0 | −1.5 | −0.5 | −0.5 |
| 4 | 2.0 | −1.0 | 1.0 | 1.0 |
| 5 | 3.5 | −0.5 | 3.0 | 3.0 |
| 6 | 5.5 | 0.0 | 5.5 | 5.5 |
| 7 | 5.5 | — | 5.5 | 5.5 |

Only index 7 survives intact, and the largest single error is $3.5$ at index 0.
This is the most common FFT bug, and it is nastier than an out-of-range index
because the answer has the right length and a plausible magnitude — `5.5` appears
twice in the wrong answer, exactly as it should. The fix is one line: **always
pad both inputs to at least $M+L-1$.** Note that "circular convolution is what
you want" is sometimes true — the box filter in the lesson's code is deliberately
circular, because a periodic signal convolved with a periodic kernel *is* circular
— but "linear convolution is what you want" is true essentially always, so the
decision should be deliberate.

**(c)** Parseval holds to `0.00e+00`, `1.78e-15`, `2.84e-14`, `1.14e-13` for $N = 8, 16,
$64$, 256$. The factor $1/N$ comes from the inverse transform's normalisation, which is the
only place a scale appears in the pair of formulas: the forward transform has none, and
$x_n = \frac1N\sum_k X_k e^{2\pi i kn/N}$. Squaring and summing over $n$ collapses the double
sum by orthogonality to $\frac1N\sum_k \lvert X_k\rvert^2$, and the remaining $\frac1N$
multiplying $\sum_n\lvert x_n\rvert^2$ is the Parseval relation. The growing discrepancy
with $N$ is simply that the right-hand side sums $N$ rounded numbers, so its absolute error
grows like $N\varepsilon$ while the left-hand side grows like $N$ — the *relative* error
stays at $\varepsilon$.

This is worth having in your pocket as a debugging tool, because it costs one extra pass
over the array. If your FFT and your inverse do not round-trip to Parseval, your
normalisation convention is wrong before you have looked at a single coefficient. It is
also the reason "energy" and "spectrum" are interchangeable vocabularies, and the reason
magnitude-squared rather than magnitude is the natural power measure.

**(d)** The crossover is between $N = 16$ (FFT is `0.6x`, i.e. still losing) and $N = 64`
(`1.6x`, winning). After that the gap widens fast: `4.9x` at 256, `16.0x` at 1024, `53.9x`
at 4096 — a factor of about 4 for every doubling of $N$, which is exactly what you expect
from $\Theta(N^2)/\Theta(N\log N) = \Theta(N/\log N)$.

So in practice the FFT route wins from about $N \approx 32$ onwards and is essential past a
few hundred. That is why `numpy.fft` exists and why nobody writes a naive DFT outside a
teaching example. The counting is worth doing rather than trusting a clock: the claim
"$\frac N2\log_2 N$ complex multiplications" is reproducible — 112 at $N=16$, 3328 at
$N=256$ — and at $N = 4096$ the naive route would need `4,194,304` multiply-adds against
the FFT's `77,824`. Note the honest small-$N$ caveat: for $N \le 16$ the naive DFT is
actually *faster*, because three transforms pay a constant overhead that a single $N^2$
loop does not.

</details>

**[ ] Exercise 7 — spectral leakage: padding, windowing, and what each one
actually buys.** Take $N = 64$ and the pure tone $x_n = \cos(2\pi f n/N)$.
(a) For $f = 5.0$, $5.25$ and $5.5$, report the peak bin, $\lvert X_{\text{peak}}\rvert$,
the four next-largest bins, and how many bins are occupied at all.
(b) Zero-pad the same signals to 256 points and repeat. Does the leakage improve?
(c) Apply a Hann window $w_n = \tfrac12 - \tfrac12\cos(2\pi n/N)$ and repeat.
(d) Tabulate, for each treatment, the width of the main lobe (bins above 10% of
the peak), the second-largest bin as a fraction of the peak, and the median of
the remaining tail as a fraction of the peak. State the trade-off in one
sentence.

<details>
<summary>Solution</summary>

```python
import math

TAU = 2.0 * math.pi


def fft(x):
    n = len(x)
    if n == 1:
        return list(x)
    if n & (n - 1):
        raise ValueError("not a power of two")
    e = fft(x[0::2])
    o = fft(x[1::2])
    out = [0j] * n
    for k in range(n // 2):
        w = complex(math.cos(-TAU * k / n), math.sin(-TAU * k / n))
        t = w * o[k]
        out[k] = e[k] + t
        out[k + n // 2] = e[k] - t
    return out


def hann(n):
    return [0.5 - 0.5 * math.cos(TAU * i / n) for i in range(n)]


N = 64
W = hann(N)


def report(label, x):
    n = len(x)
    X = fft(x)
    peak = max(range(n // 2), key=lambda k: abs(X[k]))
    pk = abs(X[peak])
    others = sorted(((abs(X[k]), k) for k in range(n // 2) if k != peak), reverse=True)
    top = [(k, round(m, 4)) for m, k in others[:4]]
    nz = sorted((m for m, k in others if m > 1e-9), reverse=True)
    second = nz[0] if nz else 0.0
    tail = nz[len(nz) // 2] if nz else 0.0
    print(f"  {label:<24} peak bin {peak:>3}   |X_peak| = {pk:>9.4f}")
    print(f"  {'':<24} next 4 bins: {top}")
    print(f"  {'':<24} 2nd/peak = {second / pk:.4f}   median tail/peak = {tail / pk:.5f}"
          f"   occupied bins = {len(nz) + 1}")


print("(a) at N = 64, no window")
for f in (5.0, 5.25, 5.5):
    report(f"f = {f}", [math.cos(TAU * f * n / N) for n in range(N)])
print()
print("(b) the same two, zero-padded to 256 -- a 4x finer frequency grid")
for f in (5.0, 5.25):
    report(f"padded, f = {f}", [math.cos(TAU * f * n / 64) for n in range(256)])
print()
print("(c) the same three at N = 64, with a Hann window")
for f in (5.0, 5.25, 5.5):
    report(f"Hann, f = {f}", [W[n] * math.cos(TAU * f * n / N) for n in range(N)])
print()
print("(d) side by side: what each treatment costs and what it buys")
print("   treatment      main lobe      2nd bin / peak     median tail / peak   occupied")
rows = [
    ("none,  f on grid", lambda: [math.cos(TAU * 5.0 * n / N) for n in range(N)]),
    ("none,  f = 5.25", lambda: [math.cos(TAU * 5.25 * n / N) for n in range(N)]),
    ("none,  f = 5.50", lambda: [math.cos(TAU * 5.5 * n / N) for n in range(N)]),
    ("Hann, f on grid", lambda: [W[n] * math.cos(TAU * 5.0 * n / N) for n in range(N)]),
    ("Hann, f = 5.25", lambda: [W[n] * math.cos(TAU * 5.25 * n / N) for n in range(N)]),
    ("Hann, f = 5.50", lambda: [W[n] * math.cos(TAU * 5.5 * n / N) for n in range(N)]),
]
for label, build in rows:
    v = build()
    Xv = fft(v)
    peak = max(range(N // 2), key=lambda k: abs(Xv[k]))
    pk = abs(Xv[peak])
    main = [k for k in range(N // 2) if abs(Xv[k]) > 0.1 * pk]
    rest = sorted((abs(Xv[k]) for k in range(N // 2) if abs(Xv[k]) > 1e-9
                   and k not in main), reverse=True)
    second = max((abs(Xv[k]) for k in range(N // 2)
                  if abs(Xv[k]) > 1e-9 and k not in main), default=0.0)
    median = rest[len(rest) // 2] if rest else 0.0
    print(f"  {label:<18}  {len(main)} bin(s)   {second / pk:>13.4f}"
          f"   {median / pk:>17.5f}   {len(rest) + len(main):>7}")
print()
print("  A Hann window turns a 1-bin main lobe into a 3-bin main lobe and cuts the")
print("  far sidelobes by a factor of about 100.  Zero-padding changes the ruler,")
print("  not the blur: the padded 5.25 tone looks like one bin, but its sidelobe")
print("  pattern is the SAME physical shape drawn 4x finer, so nothing improved.")
```

Output:

```text
(a) at N = 64, no window
  f = 5.0                  peak bin   5   |X_peak| =   32.0000
                           next 4 bins: [(29, 0.0), (4, 0.0), (6, 0.0), (26, 0.0)]
                           2nd/peak = 0.0000   median tail/peak = 0.00000   occupied bins = 1
  f = 5.25                 peak bin   5   |X_peak| =   29.1792
                           next 4 bins: [(6, 9.2919), (4, 6.2027), (7, 3.8513), (3, 3.7325)]
                           2nd/peak = 0.3184   median tail/peak = 0.02105   occupied bins = 32
  f = 5.5                  peak bin   6   |X_peak| =   21.1809
                           next 4 bins: [(5, 19.5108), (7, 7.5548), (4, 5.8708), (8, 4.7999)]
                           2nd/peak = 0.9211   median tail/peak = 0.06452   occupied bins = 32

(b) the same two, zero-padded to 256 -- a 4x finer frequency grid
  padded, f = 5.0          peak bin  20   |X_peak| =  128.0000
                           next 4 bins: [(74, 0.0), (114, 0.0), (115, 0.0), (47, 0.0)]
                           2nd/peak = 0.0000   median tail/peak = 0.00000   occupied bins = 1
  padded, f = 5.25         peak bin  21   |X_peak| =  128.0000
                           next 4 bins: [(69, 0.0), (27, 0.0), (116, 0.0), (68, 0.0)]
                           2nd/peak = 0.0000   median tail/peak = 0.00000   occupied bins = 1

(c) the same three at N = 64, with a Hann window
  Hann, f = 5.0            peak bin   5   |X_peak| =   16.0000
                           next 4 bins: [(4, 8.0), (6, 8.0), (29, 0.0), (28, 0.0)]
                           2nd/peak = 0.5000   median tail/peak = 0.50000   occupied bins = 3
  Hann, f = 5.25           peak bin   5   |X_peak| =   15.3654
                           next 4 bins: [(6, 10.9753), (4, 5.1218), (7, 0.9978), (3, 0.394)]
                           2nd/peak = 0.7143   median tail/peak = 0.00019   occupied bins = 32
  Hann, f = 5.5            peak bin   5   |X_peak| =   13.5856
                           next 4 bins: [(6, 13.5779), (7, 2.7188), (4, 2.7103), (8, 0.3901)]
                           2nd/peak = 0.9994   median tail/peak = 0.00027   occupied bins = 31

(d) side by side: what each treatment costs and what it buys
   treatment      main lobe      2nd bin / peak     median tail / peak   occupied
  none,  f on grid    1 bin(s)          0.0000             0.00000         1
  none,  f = 5.25     5 bin(s)          0.0982             0.01827        32
  none,  f = 5.50     10 bin(s)          0.0926             0.05478        32
  Hann, f on grid     3 bin(s)          0.0000             0.00000         3
  Hann, f = 5.25      3 bin(s)          0.0649             0.00015        32
  Hann, f = 5.50      4 bin(s)          0.0287             0.00021        31

  A Hann window turns a 1-bin main lobe into a 3-bin main lobe and cuts the
  far sidelobes by a factor of about 100.  Zero-padding changes the ruler,
  not the blur: the padded 5.25 tone looks like one bin, but its sidelobe
  pattern is the SAME physical shape drawn 4x finer, so nothing improved.
```

**(a)** Three rows, three different stories, and the differences all turn on one
number: whether $f$ is an integer.

At $f = 5.0$ the tone is representable exactly on a 64-point grid, so it occupies
**1 bin** out of 32, with $\lvert X_5\rvert = 32.0000 = N/2$ and every other bin at
`0.0` — the "next 4 bins" are literally all zero. At $f = 5.25$ the same tone
occupies **all 32 bins**, with a peak of `29.1792` and a median tail at `0.02105` of
the peak. At $f = 5.5$ it is worse still: the peak falls to `21.1809` and the
neighbouring bin 5 holds `19.5108`, so `2nd/peak = 0.9211` — the energy is split
almost evenly between two bins, and no procedure can tell you which of the two
carried it.

**$f = 5.5$ is the row that matters in practice.** Halfway between bins is the
worst case for resolution and a very common one, because a physical frequency is
never a tidy fraction of the sample rate. A spectrum with two nearly equal peaks
and no way to separate them is a statement that your record is too short, not that
the signal is ambiguous.

**(b) is the trap, and it is worth walking into deliberately.** Zero-padding the
$f = 5.25$ tone to 256 points gives `occupied bins = 1` and `median tail/peak =
0.00000`. It looks like the leakage vanished. It did not. The physical sidelobe
pattern is *identical*; what changed is that $\Delta f$ fell from $f_s/64$ to
$f_s/256$, so the same blob is drawn with bins a quarter as wide. A 5.25-bin tone
padded to 1024 points would look even sharper and would be just as unresolvable.
Padding buys you the ability to *interpolate* between frequencies, which is
genuinely useful and is why a spectrum is commonly oversampled before plotting. It
buys no resolving power whatsoever, because the added samples are exactly zero and
carry no information — the support of the signal is still 64 samples long.

**(c) and (d) together.** The Hann row at $f = 5.0$ is the price: `occupied bins
= 3` with magnitudes `8.0, 16.0, 8.0`, i.e. the perfect single spike has become
three bins in the ratio $0.25 : 0.5 : 0.25$. That is the window's own three-bin
response, and by the convolution theorem it must be there: a window multiplies in
time, so it convolves in frequency.

The payoff is in the `median tail / peak` column of table (d). Unwindowed at
$f = 5.25$ the far sidelobes sit at `0.01827` of the peak; with a Hann window they
sit at `0.00015`, a factor of **122** lower. At $f = 5.5$ the improvement is
`0.05478` to `0.00021`, a factor of **261**. And the main lobe simultaneously
narrows from `10 bin(s)` to `4 bin(s)` at $f = 5.5$, because the sidelobes fall so
fast that the 10% threshold is crossed sooner.

**The trade-off in one sentence: a window widens the main lobe and lowers the
sidelobes, so it helps when you are hunting a weak tone beside a strong one and
hurts when you are trying to separate two tones that are close together.** Both
effects are in table (d) — the `main lobe` column and the `median tail / peak`
column move in opposite directions in every row. `scipy.signal.windows` is a menu
of about fifty compromises on exactly that curve, parameterised by main-lobe width
and sidelobe level, and choosing one is a decision about your signal rather than
about mathematics.

</details>

---

## Summary

- Sine and cosine are the only functions worth expanding in: they are orthogonal
  over a period (so projection is a perfect matched filter) and the derivative of
  one is another (so differentiation stays in the basis). The code's `w1 == w2`
  row gives `3.141593` and every other row `0.000000`. A periodic function is
  therefore a sum of sinusoids, the coefficients are inner products against
  them, and for a square wave they are `a_n = 0`, `b_n = 4/(pi n)` for odd $n$ —
  a $1/n$ tail caused by the jump, not by the arithmetic.
- Gibbs ringing has a fixed height: `8.9490%` of the jump at $N = 801$ and at
  $N = 3201$. Only the width shrinks, like $1/N$ ($N\times$width $\to 1.7521$).
  More terms never remove an edge ring.
- The DFT is the Fourier series of a signal that is periodic with period $N$
  samples. The forward transform has no $1/N$; the inverse has exactly $1/N$.
  Bin $k$ means $k f_s/N$ hertz, the resolution is $f_s/N$ and is set by the
  record length, and a real signal's top half is a mirror — so `rfft` returns
  $N/2+1$ numbers and a filter must keep both halves.
- The naive DFT costs exactly $N^2$ complex multiplications and $4.00\times$ more
  per doubling; the radix-2 FFT costs exactly $\frac{N}{2}\log_2 N$ and
  $2.20\times$ more at $N = 1024$. At $N = 2^{20}$: $1{,}099{,}511{,}627{,}776$
  against $10{,}485{,}760$, a factor of `104,858`. Count operations rather than
  trusting a clock: the count is an integer and the clock is not.
- The convolution theorem is an identity, not an approximation:
  `max |direct - via FFT| = 1.066e-14` on random data. Time-domain convolution
  is $\Theta(N^2)$; via the transform it is two $\Theta(N\log N)$ passes and $N$
  multiplications. Zero-pad to at least $M + L - 1$ or the tail wraps onto the
  front and the answer is wrong only at the ends — the nastiest kind of wrong.
- Filtering is $Y_k = H_k X_k$, a loop over $N$ numbers, and a pure tone occupies
  one bin — so deleting that bin deletes it exactly (`max |out_hum -
  out_white| = 1.588e-14`). That is what a notch filter is, and it is why
  band-limited interference is removable and broadband noise is only reducible.
- Every low-pass has a floor and a cliff. A bin-40 filter on white noise gives a
  *predicted* `1.78` and a *measured* `1.74`; the optimal cutoff is bin 20 with
  error `0.171034`, and lowering it to 12 makes things worse because bin 19 is
  signal. Measure the signal distortion separately or you will "improve" a signal
  by destroying it.
- Zero-padding does not improve precision — the added terms are exactly zero. It
  improves resolution only, which is why the padded 5.25-bin tone in Exercise 7
  looks like one bin and resolves no better. A Hann window genuinely lowers
  leakage, by a factor of 122 in the same exercise, and pays for it with a main
  lobe 3 bins wide instead of 1.
- Central differencing has error $\Theta(h^2)$ and forward differencing
  $\Theta(h)$, because halving the truncation term matters more than doubling
  the rounding. Optimal $h$: $\epsilon^{1/2}$ forward, $\epsilon^{1/3}$ central.
  The rate is the whole game; the constant is a second-order concern.

---

## Next

[60 — Probability Foundations](../part05_probability_statistics/60_probability_foundations.md)
starts a new part. This lesson gave you the deterministic counterpart of what
comes next: the spectrum says exactly what frequencies a signal contains, and
probability is how you reason about signals whose content you do not know in
advance.
