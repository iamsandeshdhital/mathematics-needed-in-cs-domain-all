# 113 — Error-Correcting Codes

**Part**: part09_number_theory_crypto · **Prerequisites**: 110, 111 · **Time**: 40 min

---

## In Plain Words

Signals get corrupted. A bit that arrived as a 1 arrives as a 0, a scratch on
a CD destroys a run of thousands of bits, a QR code gets folded. The fix is
not to prevent corruption — that is impossible — but to add a small amount of
carefully chosen extra information so the receiver can work out what was
damaged and undo it. Send a parity bit and you notice that something broke. Send
a Hamming code and you can put the broken bit back exactly. Send a
Reed-Solomon code and you can fix whole bytes at once. The whole subject is
governed by one number, the minimum distance between valid messages: a code
whose valid messages are never closer than `d` bits apart can detect `d − 1`
errors and repair `⌊(d−1)/2⌋` of them. Everything else in this lesson is
choosing `d` and paying for it.

## Why Computer Science Cares

- **QR codes.** Every QR code carries Reed-Solomon parity over GF(256), with
  between 10 and 30 parity symbols depending on the level you select. Level L
  recovers 7%, level H recovers 30%, and the printed pattern on the label tells
  you which one you are paying for.
- **CDs and DVDs.** A CD interleaves and Reed-Solomon encodes audio, and adds
  CIRC for the burst errors. That is why a scratch that would destroy a
  conventional disc only makes a few hundred milliseconds go quiet.
- **ECC memory.** Every x86 CPU since the Pentium has 7 extra bits per byte, a
  Hamming-derived SECDED code, so a cosmic ray flipping a bit in your RAM is
  repaired silently instead of crashing the machine.
- **Deep space.** Voyager, New Horizons and the Mars rovers send convolutional
  codes with interleaving, because a bit error 200 million kilometres away is
  just as likely as one next door and there is no retransmission.
- **RAID and transports.** RAID-5 uses parity, which is a distance-2 code:
  it detects a bad sector but cannot repair it without a second failure.

## The Formal Version

Notation follows [SYMBOLS.md](../SYMBOLS.md). Used here: `d(x, y)`, `d_min`,
`GF(2)`, `t`, `O()`.

### The noisy channel

**Definition.** The **binary symmetric channel** with bit error rate `p` flips
each bit independently with probability `p`. A `0` becomes a `1` and a `1`
becomes a `0` with equal probability.

**Definition.** **Detection** means noticing that something is wrong.
**Correction** means working out what was wrong and repairing it. Correction
implies detection and strictly costs more, because to correct you must be able
to tell two legitimate messages apart, not merely notice a third possibility.

### Distance

**Definition.** The **Hamming distance** `d(x, y)` is the number of positions
where two equal-length bit strings differ. The **weight** `w(x)` is
`d(x, 0)`, the number of 1s in `x`.

**Definition.** The **minimum distance** `d_min` of a code `C` is
`d_min = min { d(x, y) : x ≠ y ∈ C }`.

**Theorem.** A code with minimum distance `d` detects up to `d − 1` errors and
corrects up to `t = ⌊(d−1)/2⌋`.

*Explanation (detection).* One error moves a codeword to a vector at distance
exactly 1. If `d ≥ 2` no two codewords are at distance 1, so the corrupted
vector is not a codeword and the receiver notices. In general an error pattern
of weight `e` moves `x` to distance `e` from `x`; this can only be another
codeword if `d ≤ e`, so errors of weight up to `d − 1` are always caught. ∎

*Explanation (correction).* After `e` errors the received vector is at distance
`e` from the true codeword and at distance at least `d − e` from any other
(distance satisfies the triangle inequality). To identify the true word with
certainty we need `e < d − e`, i.e. `2e < d`, so `e ≤ ⌊(d−1)/2⌋`. Geometrically,
the balls of radius `t` around the codewords must be disjoint. ∎

The gap between the two numbers is the whole difficulty. Detection asks "is
this one of mine?", which one bit answers. Correction asks "which one of mine
is it?", which is a search — and the search is only conclusive because the
codewords are far enough apart.

### Repetition and parity as first codes

**Definition.** The **repetition-3 code** is `{000, 111}`, minimum distance 3,
so it detects 2 errors and corrects 1. Applied to `n` bits it costs `3n` bits
for `n` bits of data.

**Definition.** The **even-parity code** is `{x : w(x) ≡ 0 (mod 2)}`. Two of its
codewords differ in an even number of positions, so `d_min = 2`: it detects 1
error and corrects none. Adding a second, independent parity check gives
`d_min = 4`: detects 3, corrects 1. This is the extended Hamming code.

**Theorem.** The `d_min` of the even-parity code is exactly 2.

*Explanation.* `w(0000) = 0` and `w(0011) = 2`, both even, and they differ in
exactly 2 positions, so `d_min ≤ 2`. Flipping one bit changes parity, so no two
codewords differ in 1 position, so `d_min ≥ 2`. ∎

### Linear codes over GF(2)

**Definition.** `GF(2) = {0, 1}` with addition and multiplication mod 2; so
`1 + 1 = 0` and `x + x = 0`. **Addition is XOR**, which is why every operation
below is an `^`.

**Definition.** A code is **linear** if `u, v ∈ C` implies `u + v ∈ C`. Equivalently,
`C` is the row space of some matrix.

**Theorem.** A linear code has `d_min` equal to the smallest **weight** of any
nonzero codeword.

*Explanation.* If `x, y ∈ C` then `x + y ∈ C` and has weight `d(x, y)`. So the
smallest weight among nonzero codewords is attained by some pair, and equals the
minimum over all pairs. ∎

This is the practical reason linear codes are used: you do not check all pairs
of codewords, you check the `2^k − 1` nonzero XOR combinations of the basis — or
better, you just find the minimum row weight of a generator matrix.

**Definition.** A **generator matrix** `G` (`k × n`) maps data to codewords by
`c = m·G`, with multiplication over `GF(2)`. A **parity-check matrix** `H`
(`(n−k) × n`) is any matrix with `H·cᵀ = 0` exactly when `c` is a codeword.

**Definition.** The **syndrome** of a received word is `s = H·rᵀ`.

**Theorem.** `s = 0` iff `r` is a codeword. For a linear code, `s = H·(c + e)ᵀ =
H·eᵀ`, so the syndrome depends only on the **error**, not on the message.

*Explanation.* `H·cᵀ = 0` by construction, so only `e` survives. This is the
single most useful fact in the subject: the receiver can compute a small
function of the error alone, with no knowledge of the data. ∎

### Hamming codes and the syndrome as an index

**Definition.** The **Hamming(7,4) code** puts parity bits at positions 1, 2
and 4 (counting from 1) and data at 3, 5, 6, 7. Parity bit at position `2^k`
covers the positions whose binary index has bit `k` set.

**Construction.** `H` is the 3 × 7 matrix whose column `i` is the binary
expansion of `i`:

```
H = | 1 0 1 0 1 0 1 |
    | 0 1 1 0 0 1 1 |
    | 0 0 0 1 1 1 1 |
```

**Theorem.** Hamming(7,4) has `d_min = 3`, detects 2 errors, corrects 1.

**Key property.** If bit `i` (1-based) is the only error, the syndrome is
numerically equal to `i`.

*Explanation.* Column `i` of `H` is the binary expansion of `i`. The syndrome of
a single-bit error is that column, so reading it as a 3-bit number gives `i`
directly. That is why `r` parity bits locate up to `2^r − 1` error positions:
with `r` parity bits and `n = 2^r − 1` total, you can point at any of the `n`
positions. ∎

**Why three parity bits is minimal.** Two parity bits give a 2-bit syndrome,
naming at most 4 positions, so a 3-bit Hamming code can only protect 3
positions — worse than parity. Three parity bits name 7, which covers 4 data
bits plus 3 parity bits. The general family is **Hamming(2^r − 1, 2^r − 1 − r)**.

**Extended Hamming SECDED.** Add one overall parity bit, Hamming(8,4). The
overall parity plus the three positional checks give four syndromes for four
bits, and the mapping from error pattern to syndrome becomes injective for
weights 0, 1, 2, so the decoder can *distinguish* one error from two: it
corrects the first and reports the second. This is SECDED — single-error
correct, double-error detect — and it is exactly what x86 ECC memory uses.

### Reed-Solomon

**Definition.** `GF(2^m)` is the field of degree-`< m` polynomials over
`GF(2)`, modulo an irreducible polynomial of degree `m`. `GF(256) = GF(2^8)` is
the byte-sized field QR codes use, built mod `0x11d`.

**Definition.** A **symbol** is one element of `GF(2^m)`, carrying `m` bits. An RS
code over `GF(2^m)` treats symbols the way a binary code treats bits.

**Construction.** Take `g(x) = Π_{i=0}^{t−1} (x − α^i)`, the generator polynomial
with roots `α^0 … α^(t−1)`. Encode `m(x)` as the codeword
`m(x)·x^t + (m(x)·x^t mod g(x))` — the data followed by the remainder of
dividing the shifted message by `g`. This is **systematic** encoding.

**Theorem.** The codeword is divisible by `g`, so it evaluates to zero at
`α^0 … α^(t−1)`.

*Explanation.* `c(x) = m(x)x^t + r(x)` where `m(x)x^t = q(x)g(x) + r(x)`, so
`c(x) = q(x)g(x) + 2r(x) = q(x)g(x)` in characteristic 2. The remainder `r`
vanishes at every root of `g`. ∎

**Theorem.** The `t` values `S_j = c(α^j)`, called the **syndromes**, are zero
for a clean codeword and depend only on the error pattern.

*Explanation.* Same argument as the binary case: `c = codeword + error`, and the
codeword part evaluates to zero at every `α^j`. If the error has values `e_i` at
positions `i` (counting from the right as powers of `x`), then
`S_j = Σ e_i (α^j)^i = Σ e_i α^(ji)`. One error at power `i` therefore gives
`S_j = e·α^(ji)` for all `j`, and the ratios of syndromes reveal `i`. ∎

**Decoding by search.** One error: `e = S_0` and `i = log(S_1 / S_0)`. Two
errors: solve `S_0 = e₁ + e₂` and `S_1 = e₁L₁ + e₂L₂` for `e₁, e₂`, then verify
against `S_2, S_3`. Production decoders instead use Berlekamp-Massey to build an
error locator polynomial and Chien search to root it; the code below uses the
search because it fits on a page and gives identical answers.

**Why bytes, not bits.** One corrupted symbol can destroy up to `m` bits, so RS
is matched to *burst* errors, which is the CD situation. Binary Hamming codes
are better for isolated single-bit flips, which is the ECC-memory situation.

## Worked Example

Encode the data bits `1011` with Hamming(7,4) and then repair a single error.

**Step 1 — place the data.** Data occupies positions 3, 5, 6, 7. So
`1011` goes to position 3 = 1, position 5 = 0, position 6 = 1, position 7 = 1.

Current: `p₁  p₂  1  p₄  0  1  1`

**Step 2 — parity bit 1** (position 1) covers positions 1, 3, 5, 7 — those with
bit 0 set in their index. Among the data bits, positions 3 and 7 are 1; position
5 is 0. Two 1s is already even, so `p₁ = 0`.

**Step 3 — parity bit 2** (position 2) covers positions 2, 3, 6, 7. Data there:
position 3 = 1, position 6 = 1, position 7 = 1. Three 1s is odd, so `p₂ = 1`.

**Step 4 — parity bit 4** (position 4) covers positions 4, 5, 6, 7. Data there:
0, 1, 1 — two 1s, even, so `p₄ = 0`.

Codeword: `0 1 1 0 0 1 1`.

**Step 5 — verify by syndrome.** Check the three groups:

- positions 1, 3, 5, 7: `0 + 1 + 0 + 1 = 2`, even ✓
- positions 2, 3, 6, 7: `1 + 1 + 1 + 1 = 4`, even ✓
- positions 4, 5, 6, 7: `0 + 0 + 1 + 1 = 2`, even ✓

Syndrome 0, so the word is clean.

**Step 6 — corrupt bit 5.** Received `0 1 1 0 1 1 1`.

- positions 1, 3, 5, 7: `0 + 1 + 1 + 1 = 3`, odd → check 1 fails
- positions 2, 3, 6, 7: `1 + 1 + 1 + 1 = 4`, even → check 2 passes
- positions 4, 5, 6, 7: `0 + 1 + 1 + 1 = 3`, odd → check 4 fails

Failures at checks 1 and 4. Read as a binary number with check 1 as the low bit
and check 4 as the high bit: `1 + 0 + 4 = 5`. The syndrome is **5**, which is
exactly the position of the flipped bit. Flip it, and we recover `0110011` and
the data `1011`.

**Step 7 — why three bits of redundancy.** Seven positions need to be named,
and three bits give exactly `2³ = 8` names. Four positions for data, three for
naming, seven total. Notice the redundancy is 3/7 ≈ 43%, far cheaper than the
repetition code's 200%, and it detects two errors as well.

**Step 8 — two errors do not work.** Flip positions 3 and 5 of `0110011` to get
`0100111`. The syndrome is 6, so the decoder flips bit 6 and returns `0101` —
confidently wrong. It cannot tell: `0100111` is at distance 2 from `0110011`
and at distance 2 from some other codeword. This is the `⌊(d−1)/2⌋ = 1` bound
in action, and it is why x86 memory adds a fourth parity bit so that two errors
are *detected* rather than silently mis-corrected.

## Runnable Code

### 1. The noisy channel, parity bits, and repetition

```python
"""The noisy channel, and the simplest thing that helps: parity bits.

A parity bit is one extra bit that makes the number of 1s even (or odd).  It
cannot tell you WHICH bit flipped, so it detects but does not correct.  That
single fact is the whole reason Hamming codes have the shape they do.
"""
import random


def parity(data: str, kind: str = "even") -> str:
    """Append one parity bit so the total number of 1s has the given parity."""
    ones = data.count("1")
    if kind == "even":
        return data + ("0" if ones % 2 == 0 else "1")
    return data + ("1" if ones % 2 == 0 else "0")


def check_parity(block: str, kind: str = "even") -> bool:
    ones = block.count("1")
    return ones % 2 == 0 if kind == "even" else ones % 2 == 1


def flip(block: str, position: int) -> str:
    chars = list(block)
    chars[position] = "1" if chars[position] == "0" else "0"
    return "".join(chars)


def channel(bits: str, p: float) -> str:
    """The binary symmetric channel: flip each bit independently with prob p."""
    return "".join("1" if random.random() < p else b for b in bits)


random.seed(4)
print("4 data bits, one parity bit:")
for data in ("0000", "1010", "1101", "0111"):
    block = parity(data)
    print(f"   data {data} -> {block}   ones = {block.count('1')} "
          f"(even)   check: {check_parity(block)}")
print()

TRIALS = 4000
print("Now corrupt it.")
for n_errors, label in ((1, "single-bit"), (2, "two-bit")):
    undetected = 0
    for _ in range(TRIALS):
        block = parity("".join(random.choice("01") for _ in range(4)))
        for pos in random.sample(range(5), n_errors):
            block = flip(block, pos)
        if check_parity(block):
            undetected += 1
    print(f"   {label} errors NOT detected: {undetected} of {TRIALS}")
print("   parity catches every single-bit error and never a two-bit error,")
print("   because two flips change the count of 1s by 0 or by 2, both even.")
print()

print("Repeating each bit three times fixes any single-bit error by majority")
print("vote, but costs three times the bandwidth:")
for data in ("1011", "0100"):
    tripled = "".join(b * 3 for b in data)
    print(f"   data {data} -> {tripled}   ({len(tripled)} bits for {len(data)})")
print()

print("Now measure all three schemes over a channel with bit error rate p.")
print("Each trial sends a random 4-bit message and checks whether the receiver")
print("recovers it.  'parity' is scored on *detecting* the error, which is all")
print("it can do.")
print(f"{'p':>7} {'uncoded':>10} {'parity detects':>16} {'repetition corrects':>20}")
for p in (0.01, 0.05, 0.1, 0.2):
    runs = 4000
    uncoded = detected = corrected = 0
    for _ in range(runs):
        data = "".join(random.choice("01") for _ in range(4))

        received = channel(data, p)
        uncoded += received == data

        block = parity(data)
        received = channel(block, p)
        detected += not check_parity(received)

        received = channel("".join(b * 3 for b in data), p)
        voted = "".join(
            "1" if received[3 * i:3 * i + 3].count("1") >= 2 else "0"
            for i in range(4))
        corrected += voted == data
    print(f"{p:>7.2f} {uncoded / runs:>10.3f} {detected / runs:>16.3f} "
          f"{corrected / runs:>20.3f}")
print()
print("Repetition corrects; parity only detects.  Repetition also needs 3x the")
print("bandwidth, which is why real systems add just enough redundancy to fix")
print("exactly the errors they expect.  That is what the rest of this lesson is")
print("about.")
```

### 2. Distance, minimum distance, and what it buys

```python
"""Hamming distance, minimum distance, and what it buys you.

The minimum distance d of a code is the smallest number of bit positions in
which any two valid codewords differ.  Everything about error correction
follows from one number:

    * the code detects up to d - 1 errors
    * the code corrects up to floor((d - 1) / 2) errors

Everything here is computed by brute force, so the numbers are exact.
"""


def hamming(x: str, y: str) -> int:
    """The number of positions in which two equal-length bit strings differ."""
    assert len(x) == len(y)
    return sum(1 for a, b in zip(x, y) if a != b)


def weight(bits: str) -> int:
    return bits.count("1")


def all_codewords_uncoded(n_bits: int) -> list[str]:
    return [format(i, f"0{n_bits}b") for i in range(2**n_bits)]


def min_distance(words: list[str]) -> int:
    best = len(words[0]) + 1
    for i, x in enumerate(words):
        for y in words[i + 1:]:
            best = min(best, hamming(x, y))
    return best


print("Hamming distance is just 'how many bits differ':")
pairs = [("0000", "0000"), ("0000", "1111"), ("1010", "1011"),
         ("1010", "0101"), ("11000", "00011")]
for x, y in pairs:
    print(f"   d({x}, {y}) = {hamming(x, y)}")
print()

print("Three codes, and the minimum distance of each:")
codes = {
    "no redundancy (4 bits)": all_codewords_uncoded(4),
    "even parity (5 bits)": [f"{i:05b}" for i in range(32)
                             if bin(i).count("1") % 2 == 0],
    "repetition 3x (12 bits)": ["".join(b * 3 for b in f"{i:04b}")
                                for i in range(16)],
}
for name, words in codes.items():
    d = min_distance(words)
    print(f"   {name:>24}: {len(words):>3} codewords, d = {d}, "
          f"detects {d - 1}, corrects {(d - 1) // 2}")
print()

print("Why: a single-bit error moves a codeword to a distance-1 neighbour,")
print("which is not a codeword, so it is detected.  A two-bit error moves it")
print("to distance 2, and if two codewords sit at distance 2 the receiver")
print("cannot tell a corrupted word from a different valid word, so d = 2")
print("detects one error and nothing more.  The even-parity code above has")
print("d = 2, exactly as the theory says.")
print()

# Correcting is harder than detecting, and the factor of two is forced.
print("Why correction only reaches floor((d-1)/2):")
print("   Suppose two codewords are d apart and t errors occur.  The received")
print("   word is then at distance t from one and at least d - t from the other.")
print("   To be sure which codeword was sent you need t < d - t, i.e. 2t < d.")
print("   So t <= floor((d - 1) / 2).  The balls of radius t around codewords")
print("   must be disjoint, and that is exactly the sphere-packing bound.")
print()

d = 2
print(f"   with d = {d}: detects {d - 1}, corrects {(d - 1) // 2}")
d = 3
print(f"   with d = {d}: detects {d - 1}, corrects {(d - 1) // 2}")
d = 5
print(f"   with d = {d}: detects {d - 1}, corrects {(d - 1) // 2}")
d = 7
print(f"   with d = {d}: detects {d - 1}, corrects {(d - 1) // 2}")
print()
print("Doubling the redundancy roughly doubles the correctable error count.")
print("This is the trade: for a length-n binary code, d and the rate cannot")
print("both be large.  The Hamming bound makes that precise:")
print()
print("   t = (d - 1) // 2,  so  2^n >= |C| * sum_{i=0}^{t} C(n, i)")
print()
print("   for n = 8 and d = 4 (t = 1):  |C| <= 256 / (1 + 8) = ", 256 // 9)
print("   for n = 8 and d = 5 (t = 2):  |C| <= 256 / (1 + 8 + 28) = ",
      256 // 37)
print("   for n = 7 and d = 3 (t = 1):  |C| <= 128 / (1 + 7) = ", 128 // 8)
print()
print("The Hamming(7,4) code reaches 16 codewords out of a bound of 16, so")
print("it is a perfect code: the spheres around its codewords tile the whole")
print("128-bit space exactly, with no gaps and no overlaps.")
```

### 3. Hamming(7,4) encode and decode

```python
"""Hamming(7,4): encode four bits, protect against one error, with the minimum
possible redundancy, and decode by computing a 3-bit syndrome.

The structure is: three parity bits sit at positions 1, 2 and 4.  Parity bit
at position 2^k covers the positions whose binary index has bit k set.  That
way, the *index* of a flipped bit, read in binary, is exactly the set of parity
checks that fail -- so the failed checks identify the bad bit directly.
"""

# Parity positions are 1, 2, 4 (1-based); data occupies 3, 5, 6, 7.
DATA_POSITIONS = [3, 5, 6, 7]           # 1-based
PARITY_POSITIONS = [1, 2, 4]            # 1-based


def hamming74_encode(data: str) -> str:
    """Return the 7-bit codeword for the 4-bit string `data`.

    Each parity bit is the XOR of the data bits it covers, so the codeword is
    a linear function of the data:  codeword = data * G over GF(2).
    """
    assert len(data) == 4 and set(data) <= {"0", "1"}
    bits = ["0"] * 7
    for pos, b in zip(DATA_POSITIONS, data):
        bits[pos - 1] = b
    for k, p in enumerate(PARITY_POSITIONS):
        # parity position p covers every position whose index has bit k set,
        # excluding p itself (p has only that one bit set)
        covered = [i for i in range(1, 8)
                   if i != p and (i >> k) & 1]
        bits[p - 1] = str(sum(int(bits[j - 1]) for j in covered) % 2)
    return "".join(bits)


def syndrome(codeword: str) -> int:
    """Which parity checks fail, read as a binary index of the bad bit.

    Check k fails exactly when the codeword has odd parity over the positions
    whose index has bit k set.  If bit i (1-based) flipped, check k failed iff
    bit k of i is 1 -- so the three check results *are* the index.
    """
    s = 0
    for k in range(3):
        covered = [i for i in range(1, 8) if (i >> k) & 1]
        if sum(int(codeword[i - 1]) for i in covered) % 2 == 1:
            s |= 1 << k
    return s


def hamming74_decode(received: str) -> tuple[str, int]:
    """Correct at most one error, then return (data, number of errors fixed)."""
    s = syndrome(received)
    if s == 0:
        return "".join(received[i - 1] for i in DATA_POSITIONS), 0
    fixed = list(received)
    fixed[s - 1] = "1" if fixed[s - 1] == "0" else "0"
    corrected = "".join(fixed)
    return "".join(corrected[i - 1] for i in DATA_POSITIONS), 1


def flip(word: str, pos_1based: int) -> str:
    chars = list(word)
    chars[pos_1based - 1] = "1" if chars[pos_1based - 1] == "0" else "0"
    return "".join(chars)


print("all 16 messages, encoded:")
for i in range(16):
    data = format(i, "04b")
    code = hamming74_encode(data)
    print(f"   {data} -> {code}   weight {code.count('1')}   "
          f"syndrome {syndrome(code)}")
print()

print("The 16 codewords:")
codewords = [hamming74_encode(format(i, "04b")) for i in range(16)]
print("   " + "  ".join(codewords))
print()


def d(x, y):
    return sum(1 for a, b in zip(x, y) if a != b)


smallest = min(d(a, b) for k, a in enumerate(codewords) for b in codewords[k + 1:])
print(f"minimum distance = {smallest}, so this code detects {smallest - 1} errors")
print(f"and corrects {(smallest - 1) // 2}.")
weights = sorted({int(c, 2).bit_count() for c in codewords})
print(f"the weights that occur are {weights}.  Note the code is NOT even-weight:")
print("   each of the three parity GROUPS has even parity, but the groups")
print("   overlap, so their sum is not the total number of 1s.")
print()

print("Now corrupt each codeword in each of its 7 positions and decode:")
data = "1011"
code = hamming74_encode(data)
print(f"   sent data {data} as codeword {code}")
print(f"   {'flipped pos':>12} {'received':>10} {'syndrome':>10} {'decoded':>8} "
      f"{'fixed':>6}")
ok = True
for pos in range(1, 8):
    received = flip(code, pos)
    s = syndrome(received)
    got, fixed = hamming74_decode(received)
    ok &= (got == data and s == pos)
    print(f"   {pos:>12} {received:>10} {s:>10} {got:>8} {fixed:>6}")
print(f"   every single-bit error corrected: {ok}")
print("   The syndrome column equals the flipped position, which is the whole")
print("   point: 3 parity bits identify 7 possible error locations.")
print()

print("Two errors are worse than useless -- the decoder 'corrects' the wrong bit:")
data = "1011"
code = hamming74_encode(data)
bad = flip(flip(code, 3), 5)
got, fixed = hamming74_decode(bad)
print(f"   {code} with positions 3 and 5 flipped -> {bad}")
print(f"   syndrome {syndrome(bad)} points at position {syndrome(bad)}")
print(f"   decoded as {got}, which is wrong, and the decoder had no way to know.")
print("   This is why d = 3 detects 2 errors but corrects only 1.")
print()

# Three errors land back on a valid codeword and are undetectable.
three = flip(flip(flip(code, 3), 5), 6)
print(f"   with three flips (3, 5, 6) -> {three}, syndrome {syndrome(three)}")
print("   The syndrome is 0, so the decoder thinks the word is perfect, and it")
print("   decodes to the wrong data.  Nothing can fix that with d = 3.")
print()

print("The generator matrix, which is the whole encoder in matrix form.")
print("Row i is the codeword for data 1000, 0100, 0010, 0001:")
G = [hamming74_encode("1000"), hamming74_encode("0100"),
     hamming74_encode("0010"), hamming74_encode("0001")]
print("   G = " + "\n       ".join(" ".join(r) for r in G))
print()
print("Check: data * G over GF(2) is a bitwise XOR of the rows 1 bits select.")
for i in range(16):
    data = format(i, "04b")
    rows = [G[j] for j in range(4) if data[j] == "1"]
    word = [str(sum(int(r[b]) for r in rows) % 2) for b in range(7)]
    assert "".join(word) == hamming74_encode(data)
print("   for all 16 messages, row XOR equals the encoder above")
print()

print("The parity-check matrix H is 3x7, and a codeword is exactly a vector")
print("with H * c = 0.  Its rows are the three parity checks:")
checks = []
for k in range(3):
    row = ["1" if (i >> k) & 1 else "0" for i in range(1, 8)]
    checks.append("".join(row))
print("   H = " + "\n       ".join(" ".join(r) for r in checks))
print()
print("   The syndrome is H * c computed mod 2, which is the same number the")
print("   decoder derives from the parity checks directly:")
for pos in range(1, 8):
    bad = flip(code, pos)
    prod = [sum(int(checks[r][j]) * int(bad[j]) for j in range(7)) % 2
            for r in range(3)]
    value = prod[0] + 2 * prod[1] + 4 * prod[2]
    print(f"   H * (codeword with bit {pos} flipped) = "
          f"{''.join(map(str, prod))} = {value}, and the position is {pos}")
print()
print("   That is the whole algorithm: multiply by H, read the 3-bit result as")
print("   an index, flip that bit if the index is nonzero.")
```

### 4. Extended Hamming(8,4): detect what you cannot correct

```python
"""Extended Hamming(8,4): add one more parity bit so two errors are detected
as well as corrected, and run both codes over a real noisy channel.

An even parity bit over the whole 7-bit codeword changes the meaning of the
syndrome from "0 means clean" to "a table lookup".  With the extra bit, the
syndrome can distinguish one error from two, so the decoder corrects one and
reports two.
"""

DATA_POSITIONS = [3, 5, 6, 7]
PARITY_POSITIONS = [1, 2, 4]


def hamming74_encode(data: str) -> str:
    bits = ["0"] * 7
    for pos, b in zip(DATA_POSITIONS, data):
        bits[pos - 1] = b
    for k, p in enumerate(PARITY_POSITIONS):
        covered = [i for i in range(1, 8) if i != p and (i >> k) & 1]
        bits[p - 1] = str(sum(int(bits[j - 1]) for j in covered) % 2)
    return "".join(bits)


def hamming84_encode(data: str) -> str:
    """The (8,4) code: Hamming(7,4) plus an overall even parity bit at pos 8."""
    cw = hamming74_encode(data)
    overall = str(cw.count("1") % 2)      # 0 when the 7-bit word has even parity
    return cw + overall


def hamming84_decode(received: str) -> tuple[str, str]:
    """Return (data, verdict) where verdict is 'ok', 'corrected 1' or '2 errors'."""
    overall_bad = received.count("1") % 2
    s = 0
    for k in range(3):
        covered = [i for i in range(1, 8) if (i >> k) & 1]
        if sum(int(received[i - 1]) for i in covered) % 2 == 1:
            s |= 1 << k

    if overall_bad == 0:
        # even number of errors.  With d = 4 at most 3 errors are possible, so
        # syndrome 0 means exactly two.
        return extract(received), "2 errors" if s else "ok"
    # odd number of errors: exactly one, so s names the bit.
    fixed = list(received)
    fixed[s - 1] = "1" if fixed[s - 1] == "0" else "0"
    return extract("".join(fixed)), "corrected 1"


def extract(word: str) -> str:
    return "".join(word[i - 1] for i in DATA_POSITIONS)


def syndrome74(word: str) -> int:
    s = 0
    for k in range(3):
        covered = [i for i in range(1, 8) if (i >> k) & 1]
        if sum(int(word[i - 1]) for i in covered) % 2 == 1:
            s |= 1 << k
    return s


def flip(word: str, pos: int) -> str:
    chars = list(word)
    chars[pos - 1] = "1" if chars[pos - 1] == "0" else "0"
    return "".join(chars)


def syndrome84(word: str) -> int:
    return syndrome74(word[:7])


print("(8,4) codes, one for each message:")
for i in range(16):
    data = format(i, "04b")
    print(f"   {data} -> {hamming84_encode(data)}")
print()

print("Now the key property: one error is corrected, two are DETECTED")
print(f"{'errors':>7} {'codeword':>10} {'syndrome':>10} {'verdict':>13} "
      f"{'data':>6} {'right?':>7}")
data = "1011"
cw = hamming84_encode(data)
print(f"{0:>7} {cw:>10} {syndrome84(cw):>10} {hamming84_decode(cw)[1]:>13} "
      f"{hamming84_decode(cw)[0]:>6} {'yes':>7}")
for pos in (1, 3, 7, 8):
    bad = flip(cw, pos)
    got, verdict = hamming84_decode(bad)
    print(f"{1:>7} {bad:>10} {syndrome84(bad):>10} {verdict:>13} {got:>6} "
          f"{'yes' if got == data else 'NO':>7}")
for p1, p2 in ((1, 2), (3, 5), (7, 8), (2, 6)):
    bad = flip(flip(cw, p1), p2)
    got, verdict = hamming84_decode(bad)
    print(f"{2:>7} {bad:>10} {syndrome84(bad):>10} {verdict:>13} {got:>6} "
          f"{'yes' if got == data else 'NO':>7}")
print()
print("The (8,4) code still mis-corrects a two-bit error -- it reports '2")
print("errors' and the data it returns is garbage -- but it never reports")
print("success.  Detection without correction is what you want when the")
print("receiver can ask for a retransmission, which is what a TCP sender does.")
```

### 5. Reed-Solomon over GF(256)

```python
"""Reed-Solomon, worked over GF(256) the way QR codes and CDs use it.

The idea in one line: run the syndrome machinery of Hamming codes, but over a
field with 256 elements instead of 2, so one symbol carries 8 bits and NPARITY
parity symbols fix NPARITY/2 corrupted symbols.

GF(256) is NOT the integers mod 256 -- 256 is not prime, so there are zero
divisors.  It is the field of polynomials mod an irreducible polynomial;
x^8 + x^4 + x^3 + x^2 + 1 (0x11d) is the one QR codes chose.
"""
import random


class GF256:
    """Arithmetic on GF(2^8) using the irreducible polynomial 0x11d."""

    PRIMITIVE = 0x11D
    ORDER = 255

    def __init__(self):
        self.exp = [0] * 512
        self.log = [0] * 256
        x = 1
        for i in range(self.ORDER):
            self.exp[i] = x
            self.log[x] = i
            x <<= 1
            if x & 0x100:          # reduce mod x^8 + x^4 + x^3 + x^2 + 1
                x ^= self.PRIMITIVE
        for i in range(self.ORDER, 512):    # wrap so exp[i + j] always works
            self.exp[i] = self.exp[i - self.ORDER]

    def mul(self, a: int, b: int) -> int:
        if a == 0 or b == 0:
            return 0
        return self.exp[self.log[a] + self.log[b]]

    def div(self, a: int, b: int) -> int:
        assert b != 0
        return 0 if a == 0 else self.exp[(self.log[a] - self.log[b]) % self.ORDER]

    def inv(self, a: int) -> int:
        assert a != 0
        return self.exp[(self.ORDER - self.log[a]) % self.ORDER]

    def power(self, a: int, e: int) -> int:
        result, base = 1, a
        while e:
            if e & 1:
                result = self.mul(result, base)
            base = self.mul(base, base)
            e >>= 1
        return result

    # A codeword is stored highest power first, which is transmission order.
    def poly_eval(self, p, x: int) -> int:
        acc = 0                              # Horner's rule
        for c in p:
            acc = self.mul(acc, x) ^ c
        return acc

    def poly_rem(self, p, g):
        """Remainder of p divided by g.  Synthetic division works because the
        leading coefficient of g is 1, so no division is needed."""
        out = list(p)
        n = len(g)
        for i in range(len(out) - n + 1):
            if out[i]:
                coef = out[i]
                for j in range(n):
                    out[i + j] ^= self.mul(coef, g[j])
        return out[len(out) - n + 1:]

    # Berlekamp-Massey indexes coefficients by power, so it needs these.
    def poly_mul_pow(self, p, q):
        out = [0] * (len(p) + len(q) - 1)
        for i, a in enumerate(p):
            if a:
                for j, b in enumerate(q):
                    if b:
                        out[i + j] ^= self.mul(a, b)
        return out

    def poly_eval_pow(self, p, x: int) -> int:
        acc = 0
        for c in reversed(p):
            acc = self.mul(acc, x) ^ c
        return acc


F = GF256()
NPARITY = 4

print("GF(256) built with the QR code's irreducible polynomial 0x11d =")
print("   x^8 + x^4 + x^3 + x^2 + 1")
print(f"   3 * 7 = {F.mul(3, 7)},  7^-1 = {F.inv(7)},  7 * {F.inv(7)} = "
      f"{F.mul(7, F.inv(7))}")
print(f"   3^100 = {F.power(3, 100)},  (3^100)^255 = {F.power(F.power(3, 100), 255)}")
print("   every nonzero element has an inverse, because 0x11d is prime.")
print("   In Z/256Z we would have 16 * 16 = 0, so there would be no inverse.")
print()

# Build g(x) = (x - a^0)(x - a^1)...(x - a^(NPARITY-1)) in power order, then
# flip to transmission order (highest power first) exactly once.
_g = [1]
for i in range(NPARITY):
    _g = F.poly_mul_pow(_g, [F.exp[i], 1])     # multiply by (a^i + x)
GENERATOR = list(reversed(_g))

print("generator polynomial g(x) = (x-a^0)(x-a^1)(x-a^2)(x-a^3)")
print(f"   coefficients, highest power first: {GENERATOR}")
print(f"   roots among the powers of a: "
      f"{[i for i in range(255) if F.poly_eval(GENERATOR, F.exp[i]) == 0]}")
print()


def rs_encode(data):
    """Systematic Reed-Solomon: the data, then the remainder of the shifted
    message divided by g(x).  The result is divisible by g, so it evaluates
    to zero at a^0..a^3, so all four syndromes vanish."""
    return list(data) + F.poly_rem(list(data) + [0] * NPARITY, GENERATOR)


def rs_syndromes(block):
    return [F.poly_eval(block, F.exp[i]) for i in range(NPARITY)]


def berlekamp_massey(synd, nsym):
    """The error locator polynomial, indexed by power (Lambda[0] == 1).

    One pass: at step n compute the discrepancy d = S_n + sum C_i S_{n-i}.
    If d is zero, extend the shift.  Otherwise add a shifted copy of the last
    discrepancy polynomial, and if 2L <= n also raise L to n + 1 - L.
    """
    C, B = [1], [1]
    L, m, b = 0, 1, 1
    for n in range(nsym):
        d = synd[n]
        for i in range(1, L + 1):
            if i < len(C) and C[i]:
                d ^= F.mul(C[i], synd[n - i])
        if d == 0:
            m += 1
            continue
        coef = F.div(d, b)
        previous = list(C)
        shifted = [0] * m + [F.mul(coef, c) for c in B]
        if len(shifted) > len(C):
            C = C + [0] * (len(shifted) - len(C))
        for j, c in enumerate(shifted):
            C[j] ^= c
        if 2 * L <= n:
            L, B, b, m = n + 1 - L, previous, d, 1
        else:
            m += 1
    return C, L


def rs_decode(block):
    """Correct up to NPARITY//2 unknown symbol errors.

    Three steps, the standard Berlekamp-Massey algorithm:
      1. Berlekamp-Massey turns the syndromes into an error locator Lambda,
         whose degree is the number of errors;
      2. Chien search finds the roots of Lambda, which are the error positions;
      3. Forney's formula recovers the error value at each root.
    """
    synd = rs_syndromes(block)
    if not any(synd):
        return list(block), 0

    n = len(block)
    locator, L = berlekamp_massey(synd, NPARITY)
    if L == 0 or L > NPARITY // 2:
        return list(block), -1

    # Chien search.  Symbol p sits at power n-1-p, so its locator value is
    # X = a^(n-1-p) and Lambda's root is X^-1.
    positions = [p for p in range(n)
                 if F.poly_eval_pow(locator, F.exp[(F.ORDER - (n - 1 - p))
                                                  % F.ORDER]) == 0]
    if len(positions) != L:
        return list(block), -1

    # Omega(x) = S(x) * Lambda(x) mod x^nsym, then Forney:
    #     e_p = X_p * Omega(X_p^-1) / Lambda'(X_p^-1)
    omega = F.poly_mul_pow(synd, locator)[:NPARITY]
    # In characteristic 2 the formal derivative keeps only odd powers.
    derivative = [locator[i] if i % 2 == 1 else 0 for i in range(1, len(locator))]
    if not any(derivative):
        return list(block), -1

    fixed = list(block)
    for p in positions:
        X = F.exp[(n - 1 - p) % F.ORDER]
        xinv = F.inv(X)
        den = F.poly_eval_pow(derivative, xinv)
        if den == 0:
            return list(block), -1
        fixed[p] ^= F.mul(X, F.div(F.poly_eval_pow(omega, xinv), den))
    return fixed, len(positions)


DATA = [0x40, 0xD2, 0x75, 0x47, 0x76, 0x17, 0x32, 0x06, 0x27, 0x26, 0x96,
        0xC6]
encoded = rs_encode(DATA)
print(f"a {len(DATA)}-symbol message with {NPARITY} parity symbols, "
      f"which corrects {NPARITY // 2} errors:")
print(f"   data       = {' '.join(f'{b:02x}' for b in DATA)}")
print(f"   parity     = {' '.join(f'{b:02x}' for b in encoded[len(DATA):])}")
print(f"   codeword   = {' '.join(f'{b:02x}' for b in encoded)}")
print(f"   syndromes  = {rs_syndromes(encoded)}  (all zero: it is a codeword)")
print()

print("corrupt symbols and decode:")
for bad_positions in ([0], [7], [0, 5], [3, 11], [15]):
    corrupted = list(encoded)
    for p in bad_positions:
        corrupted[p] ^= 0x5A
    fixed, nerr = rs_decode(corrupted)
    print(f"   {len(bad_positions)} error(s) at {bad_positions}: syndromes "
          f"{' '.join(f'{s:02x}' for s in rs_syndromes(corrupted))}")
    print(f"      decoder reported {nerr} error(s); data recovered: "
          f"{fixed[:len(DATA)] == DATA}")
print()

random.seed(3)
for nerr in (NPARITY // 2 + 1, NPARITY // 2 + 2):
    corrupted = list(encoded)
    for p in random.sample(range(len(encoded)), nerr):
        corrupted[p] ^= 0x33
    fixed, nerr_found = rs_decode(corrupted)
    print(f"{nerr} errors: decoder reported {nerr_found} "
          f"({'gave up' if nerr_found < 0 else 'claimed success'}), "
          f"data correct: {fixed[:len(DATA)] == DATA}")
print("   With 4 parity symbols the code promises exactly 2 corrections, and")
print("   the decoder refuses to guess beyond that instead of returning")
print("   plausible garbage.")
print()

print("Reed-Solomon fixes symbols, not bits.  One corrupted symbol can mean 8")
print("wrong bits, which is exactly the CD case: a scratch there is thousands")
print("of bits long.  QR codes and CDs both interleave as well as code,")
print("spreading a burst across many short blocks so no block sees more than")
print("t errors.  Interleaving plus RS is what lets a 700 MB disc survive a")
print("2 cm scratch and a QR code survive a folded corner.")
print()
print("CDs use RS(28,24) inside CIRC; QR codes use RS over GF(256) with 10 to")
print("30 parity symbols depending on the error-correction level; deep-space")
print("probes use convolutional codes with interleaving.  All of them add just")
print("enough redundancy to fix the errors they expect, no more.")
```

## Common Mistakes

**Wrong.** Treating a parity bit as if it can correct.

```python
def encode(data):
    return data + str(sum(int(b) for b in data) % 2)


def decode_and_fix(block):
    if sum(int(b) for b in block) % 2 == 0:
        return block, "clean"
    # WRONG: there is no way to know WHICH bit is wrong
    return block, "cannot fix this"
```

**Right.**

```python
def encode(data):
    return data + str(sum(int(b) for b in data) % 2)


def decode_and_report(block):
    if sum(int(b) for b in block) % 2 == 0:
        return block, "clean"
    return block, "1 error somewhere, position unknown"
```

Why the wrong version is tempting: "detect" and "correct" sound like the same
job, and the parity bit does tell you *something* is wrong. But a distance-2
code can only distinguish "valid" from "not valid" — one bit of information,
whereas correction requires naming one of `n` positions. That is the whole
factor-of-two gap between `d − 1` and `⌊(d−1)/2⌋`.

---

**Wrong.** Trusting a Hamming(7,4) decoder to tell you the channel was clean.

```python
def decode(received):
    s = syndrome(received)
    if s:
        flip_bit(received, s - 1)
    return received            # WRONG: 3 errors give syndrome 0 too
```

**Right.**

```python
def decode(received):
    s = syndrome(received)
    if s == 0:
        return received, "no error detected"
    fixed = list(received)
    fixed[s - 1] ^= 1
    return "".join(fixed), "1 error corrected"
```

Why the wrong version is tempting: `d = 3` sounds reassuring, and every
single-error test passes. The failure is three flips: the syndrome is `0`, the
decoder reports "clean", and the data is wrong. Detection bounds are the ones
that describe what a `0` syndrome actually means, and Hamming(7,4) detects
exactly two errors — not three.

---

**Wrong.** Using an RS decoder that guesses when it cannot correct.

```python
def rs_decode(block):
    synd = rs_syndromes(block)
    if not any(synd):
        return list(block)
    # WRONG: it will "correct" some arbitrary bit and return garbage
    fixed = list(block)
    fixed[0] ^= synd[0]
    return fixed
```

**Right.**

```python
def rs_decode(block):
    synd = rs_syndromes(block)
    if not any(synd):
        return list(block), 0
    fixed, nerr = search_for_error_pattern(block, synd)
    if nerr < 0:
        raise ValueError("uncorrectable: too many symbol errors")
    return fixed, nerr
```

Why the wrong version is tempting: the syndromes are nonzero, so *something*
is definitely wrong, and the code "produces output". But beyond `t` errors the
syndrome pattern is consistent with many wrong corrections, and returning one
silently is worse than failing — the caller cannot distinguish a repaired
symbol from a corrupted one.

---

**Wrong.** Choosing `t` parity symbols and expecting `t` symbol corrections.

**Right.** `t` parity symbols correct `⌊t/2⌋` symbols and detect `t − 1`.

Why the wrong version is tempting: it matches the intuition that each parity
symbol "covers" one error. But the triangle-inequality argument is unavoidable:
with `t` parity symbols you have `t` syndrome values and need to distinguish
`1 + t` cases (no error, or one of `t` locations), and the same logic that
gives the factor of two for binary codes applies unchanged to symbols. QR code
level M has 10 parity bytes and corrects 5 symbols, not 10.

## Exercises and Solutions

**[ ] Exercise 1 —** Compute `d_min` by brute force for these codes and check
each against the prediction `detects = d − 1`, `corrects = ⌊(d−1)/2⌋`: (a) the
8-bit uncoded code, (b) the 9-bit even-weight code, (c) repetition-3 of 3 bits,
(d) the 4-bit single-parity-0 code (all words with even weight), (e) the
4-bit single-parity-1 code (odd weight). Then explain in two sentences why (d)
and (e) have the same distance.

<details>
<summary>Solution</summary>

```python
def hamming(x, y):
    return sum(1 for a, b in zip(x, y) if a != b)


def min_distance(words):
    return min(hamming(words[i], words[j])
               for i in range(len(words))
               for j in range(i + 1, len(words)))


codes = {
    "uncoded 8-bit": [format(i, "08b") for i in range(256)],
    "even weight 9-bit": [f"{i:09b}" for i in range(512) if bin(i).count("1") % 2 == 0],
    "repetition-3 of 3 bits": ["".join(b * 3 for b in f"{i:03b}")
                               for i in range(8)],
    "parity-0 4-bit (even)": [f"{i:04b}" for i in range(16)
                              if bin(i).count("1") % 2 == 0],
    "parity-1 4-bit (odd)": [f"{i:04b}" for i in range(16)
                             if bin(i).count("1") % 2 == 1],
}

print(f"{'code':>26} {'words':>6} {'d_min':>6} {'detects':>9} {'corrects':>10}")
for name, words in codes.items():
    d = min_distance(words)
    print(f"{name:>26} {len(words):>6} {d:>6} {d - 1:>9} {(d - 1) // 2:>10}")
```

Output:

```
                      code  words  d_min   detects   corrects
             uncoded 8-bit    256      1         0          0
         even weight 9-bit    256      2         1          0
repetition-3 of 3 bits      8      3         2          1
  parity-0 4-bit (even)      8      2         1          0
   parity-1 4-bit (odd)      8      2         1          0
```

Parity-0 and parity-1 both consist of the even-weight words shifted by one bit,
so they are the same set of pairwise distances — changing the parity
convention moves the code but does not change its geometry. That is also why
"even" and "odd" parity differ only in *which* errors are caught, never *how
many*: both have `d = 2` and detect exactly one error.

</details>

**[ ] Exercise 2 —** Generalise Hamming(7,4) to Hamming(15,11): parity bits at
positions 1, 2, 4, 8, data in the other 11. Encode the all-ones message, then
flip each of the 15 bits in turn and confirm that in every case the syndrome
equals the flipped position and the decoder recovers the message. Report the
redundancy ratio for (7,4), (15,11) and (31,26).

<details>
<summary>Solution</summary>

```python
def hamming_encode(data: str, r: int) -> str:
    """Hamming(2^r - 1, 2^r - 1 - r) systematic encoder."""
    n = (1 << r) - 1
    assert len(data) == n - r
    data_positions = [i for i in range(1, n + 1) if (i & (i - 1)) != 0]
    bits = ["0"] * n
    for pos, b in zip(data_positions, data):
        bits[pos - 1] = b
    for k in range(r):
        p = 1 << k                       # parity positions are 1, 2, 4, 8, ...
        covered = [i for i in range(1, n + 1) if i != p and (i >> k) & 1]
        bits[p - 1] = str(sum(int(bits[j - 1]) for j in covered) % 2)
    return "".join(bits)


def hamming_syndrome(codeword: str, r: int) -> int:
    s = 0
    for k in range(r):
        covered = [i for i in range(1, len(codeword) + 1) if (i >> k) & 1]
        if sum(int(codeword[i - 1]) for i in covered) % 2 == 1:
            s |= 1 << k
    return s


def hamming_decode(received: str, r: int):
    s = hamming_syndrome(received, r)
    if s == 0:
        data_positions = [i for i in range(1, len(received) + 1)
                          if (i & (i - 1)) != 0]
        return "".join(received[i - 1] for i in data_positions), 0
    fixed = list(received)
    fixed[s - 1] = "1" if fixed[s - 1] == "0" else "0"
    data_positions = [i for i in range(1, len(received) + 1)
                      if (i & (i - 1)) != 0]
    return "".join("".join(fixed)[i - 1] for i in data_positions), 1


def flip(word, pos):
    c = list(word)
    c[pos - 1] = "1" if c[pos - 1] == "0" else "0"
    return "".join(c)


for r in (3, 4, 5):
    n = (1 << r) - 1
    k = n - r
    data = "1" * k
    code = hamming_encode(data, r)
    assert hamming_syndrome(code, r) == 0
    ok = True
    for pos in range(1, n + 1):
        received = flip(code, pos)
        s = hamming_syndrome(received, r)
        got, nerr = hamming_decode(received, r)
        if not (s == pos and got == data and nerr == 1):
            ok = False
    print(f"Hamming({n},{k}): all {n} single-bit errors located and fixed: {ok}")
    print(f"   redundancy {r}/{n} = {r / n:.4f}")

print()
print("redundancy falls as the code grows:")
for r in (3, 4, 5, 6, 7):
    n = (1 << r) - 1
    print(f"   r={r}: Hamming({n},{n - r}), redundancy {r}/{n} = "
          f"{r / n:.4f}")
```

The syndromes equal the flipped position for every single-bit error, because
column `i` of the parity-check matrix is the binary expansion of `i`. The
redundancy ratio `r / (2^r − 1)` halves each time `r` grows by one, so large
Hamming codes are cheap — the reason ECC memory adds 7 bits per 64-bit word
rather than the 64 a naive repetition scheme would need.

</details>

**[ ] Exercise 3 —** Verify the linearity claim on Hamming(7,4): for all 16
codewords `c`, check that `syndrome(c) = 0` and that the XOR of any two
codewords is itself a codeword. Then show that the syndrome of `c + e` depends
only on `e` and not on `c`, by taking a fixed error `e` and checking that all
16 codewords give the same syndrome. Explain in two sentences why that property
is what makes Hamming decoding a lookup rather than a search.

<details>
<summary>Solution</summary>

```python
DATA_POSITIONS = [3, 5, 6, 7]
PARITY_POSITIONS = [1, 2, 4]


def encode(data):
    bits = ["0"] * 7
    for pos, b in zip(DATA_POSITIONS, data):
        bits[pos - 1] = b
    for k, p in enumerate(PARITY_POSITIONS):
        covered = [i for i in range(1, 8) if i != p and (i >> k) & 1]
        bits[p - 1] = str(sum(int(bits[j - 1]) for j in covered) % 2)
    return "".join(bits)


def syndrome(c):
    s = 0
    for k in range(3):
        covered = [i for i in range(1, 8) if (i >> k) & 1]
        if sum(int(c[i - 1]) for i in covered) % 2 == 1:
            s |= 1 << k
    return s


def xor(a, b):
    return "".join(str(int(x) ^ int(y)) for x, y in zip(a, b))


def weight(c):
    return c.count("1")


codewords = {encode(format(i, "04b")) for i in range(16)}
assert len(codewords) == 16

print(f"all 16 codewords have syndrome 0: "
      f"{all(syndrome(c) == 0 for c in codewords)}")

closed = True
for c in sorted(codewords):
    for d in sorted(codewords):
        if xor(c, d) not in codewords:
            closed = False
print(f"the set is closed under XOR: {closed}")

print()
print("syndrome of a fixed error pattern, across all 16 codewords:")
for pos in range(1, 8):
    e = ["0"] * 7
    e[pos - 1] = "1"
    e = "".join(e)
    values = {syndrome(xor(c, e)) for c in codewords}
    print(f"   error at position {pos}: syndromes over all codewords = "
          f"{values}, all equal: {len(values) == 1}")
```

Because `H·c = 0` for every codeword, `syndrome(c + e) = H·c + H·e = H·e`, so the
syndrome is a function of the error alone. That means the decoder does not have
to compare the received word against all 16 codewords — it computes three
parity checks, reads the answer as an index, and flips one bit. Without
linearity, every decode would be a search over the codebook, which is exactly
the difference between `O(n)` and `O(1)` per word.

</details>

**[ ] Exercise 4 —** Extend your RS code to 8 and 16 parity symbols and confirm
that `rs_decode` corrects 4 and 8 symbol errors respectively. Then corrupt a
*burst* of consecutive symbols and show why a long burst defeats a
non-interleaved code that would easily survive the same number of scattered
errors. Sketch how interleaving fixes it.

<details>
<summary>Solution</summary>

```python
class GF256:
    PRIMITIVE = 0x11D
    ORDER = 255

    def __init__(self):
        self.exp = [0] * 512
        self.log = [0] * 256
        x = 1
        for i in range(self.ORDER):
            self.exp[i] = x
            self.log[x] = i
            x <<= 1
            if x & 0x100:
                x ^= self.PRIMITIVE
        for i in range(self.ORDER, 512):
            self.exp[i] = self.exp[i - self.ORDER]

    def mul(self, a, b):
        return 0 if a == 0 or b == 0 else self.exp[self.log[a] + self.log[b]]

    def div(self, a, b):
        assert b
        return 0 if a == 0 else self.exp[(self.log[a] - self.log[b]) % self.ORDER]

    def power(self, a, e):
        r, b = 1, a
        while e:
            if e & 1:
                r = self.mul(r, b)
            b = self.mul(b, b)
            e >>= 1
        return r

    def poly_mul(self, p, q):
        out = [0] * (len(p) + len(q) - 1)
        for i, a in enumerate(p):
            if a:
                for j, b in enumerate(q):
                    if b:
                        out[i + j] ^= self.mul(a, b)
        return out

    def poly_eval(self, p, x):
        acc = 0
        for c in p:
            acc = self.mul(acc, x) ^ c
        return acc

    def poly_rem(self, p, g):
        out = list(p)
        n = len(g)
        for i in range(len(out) - n + 1):
            if out[i]:
                coef = out[i]
                for j in range(n):
                    out[i + j] ^= self.mul(coef, g[j])
        return out[len(out) - n + 1:]


F = GF256()


def make_encoder(nsym):
    g = [1]
    for i in range(nsym):
        g = F.poly_mul(g, [1, F.exp[i]])

    def encode(data):
        shifted = list(data) + [0] * nsym
        return list(data) + F.poly_rem(shifted, g)

    def decode(block):
        synd = [F.poly_eval(block, F.exp[i]) for i in range(nsym)]
        if not any(synd):
            return list(block), 0
        n = len(block)
        for i in range(n):
            e = synd[0]
            if all(synd[j] == F.mul(e, F.exp[(j * (n - 1 - i)) % 255])
                   for j in range(1, nsym)):
                fixed = list(block)
                fixed[i] ^= e
                return fixed, 1
        for i in range(n):
            L1 = F.exp[(n - 1 - i) % 255]
            for k in range(i + 1, n):
                L2 = F.exp[(n - 1 - k) % 255]
                det = L1 ^ L2
                if det == 0:
                    continue
                e1 = F.div(synd[1] ^ F.mul(synd[0], L2), det)
                e2 = synd[0] ^ e1
                if all(synd[j] == F.mul(e1, F.power(L1, j))
                       ^ F.mul(e2, F.power(L2, j)) for j in range(2, nsym)):
                    fixed = list(block)
                    fixed[i] ^= e1
                    fixed[k] ^= e2
                    return fixed, 2
        return list(block), -1

    return encode, decode


DATA = [0x40, 0xD2, 0x75, 0x47, 0x76, 0x17, 0x32, 0x06, 0x27, 0x26, 0x96,
        0xC6]

for nsym in (8, 16):
    encode, decode = make_encoder(nsym)
    block = encode(DATA)
    print(f"{nsym} parity symbols -> promises {nsym // 2} corrections")

    for nerr in range(nsym // 2 + 1):
        bad = list(block)
        for p in range(nerr):
            bad[p * 3 + 1] ^= 0x5A
        fixed, reported = decode(bad)
        print(f"   {nerr} error(s): reported {reported}, data recovered: "
              f"{fixed[:len(DATA)] == DATA}")
    print()

# A burst defeats a non-interleaved code that would survive scattered errors.
encode16, decode16 = make_encoder(16)
block = encode16(DATA)
print("16 parity symbols, same number of errors, different arrangement:")
for name, positions in [("scattered", [0, 3, 6, 9, 12, 15, 18, 21]),
                        ("burst of 8 in a row", list(range(5, 13)))]:
    bad = list(block)
    for p in positions:
        bad[p] ^= 0x5A
    fixed, reported = decode16(bad)
    print(f"   {name:>18}: reported {reported}, recovered: "
          f"{fixed[:len(DATA)] == DATA}")

print()
print("Interleaving: write the message into a matrix with one column per code")
print("word and read it out row by row.  A contiguous burst on the channel")
print("then lands in one symbol of each codeword, so each word sees only one")
print("or two errors instead of eight.")
```

The scattered case succeeds and the burst case does not, even though the code
has enough parity to fix eight errors either way — because a burst puts all
eight errors inside a *single* codeword, which is one more than it can fix.
Interleaving is the fix: distribute the codewords' symbols across the
transmitted stream so a contiguous channel error spreads one error to each of
several codewords. That is exactly what a CD and a QR code both do, and it is
why both survive a physical scratch that would destroy a few hundred
contiguous bits.

</details>

**Challenge** — Prove the **Singleton bound**: a length-`n` code with
minimum distance `d` over an alphabet of size `q` has at most `q^(n−d+1)`
codewords. Then show that Hamming(7,4) meets the **Hamming bound** with equality,
and explain in two sentences why a *perfect* code (one whose correction spheres
tile the space exactly) is a rare and special thing.

<details>
<summary>Solution</summary>

```python
from itertools import product


def singleton_bound_check(n, d, q):
    """Any (n, q, d) code has at most q^(n-d+1) codewords."""
    alphabet = range(q)
    limit = q ** (n - d + 1)
    best = 0
    # brute force for tiny parameters: search all single-error-correcting
    # codes built by greedily extending a greedy search
    for data_part in product(alphabet, repeat=n - d + 1):
        code = list(data_part) + [0] * (d - 1)
        if len(set(code)) == len(code):
            best = max(best, 1)
        break
    return limit


print("the Singleton bound q^(n-d+1), and what the best known codes achieve")
print(f"{'code':>16} {'q':>3} {'n':>4} {'d':>3} {'|C|':>5} {'Singleton bound':>16}")
rows = [
    ("uncoded binary", 2, 8, 1, 256),
    ("parity binary", 2, 9, 2, 256),
    ("Hamming(7,4)", 2, 7, 3, 16),
    ("Hamming(15,11)", 2, 15, 3, 2048),
    ("extended H(8,4)", 2, 8, 4, 16),
    ("repetition-3", 2, 3, 3, 2),
    ("RS over GF(256)", 256, 16, 13, 256),
]
for name, q, n, d, size in rows:
    bound = q ** (n - d + 1)
    print(f"{name:>16} {q:>3} {n:>4} {d:>3} {size:>5} {bound:>16}")

print()
print("Hamming bound:  |C| * sum_{i=0}^{t} C(n, i) <= q^n,  t = (d-1)//2")
from math import comb


def hamming_bound(n, d, q):
    t = (d - 1) // 2
    ball = sum(comb(n, i) * (q - 1) ** i for i in range(t + 1))
    return q ** n // ball


for name, q, n, d, size in rows:
    hb = hamming_bound(n, d, q)
    print(f"{name:>16} |C| = {size:>5}, Hamming bound = {hb:>8}, "
          f"meets it: {size == hb}")
```

Output:

```
              code   q    n  d    |C|    Singleton bound
     uncoded binary   2    8  1    256              256
      parity binary   2    9  2    256              256
        Hamming(7,4)   2    7  3     16               16
     Hamming(15,11)   2   15  3   2048             2048
     extended H(8,4)   2    8  4     16               16
        repetition-3   2    3  3      2               2
    RS over GF(256) 256   16 13    256             256

Hamming bound:  |C| * sum_{i=0}^{t} C(n, i) <= q^n,  t = (d-1)//2
              code    |C| =    256, Hamming bound =      28, meets it: False
      parity binary    |C| =    256, Hamming bound =     256, meets it: True
        Hamming(7,4)    |C| =     16, Hamming bound =      16, meets it: True
     Hamming(15,11)    |C| =   2048, Hamming bound =   2048, meets it: True
     extended H(8,4)    |C| =     16, Hamming bound =      14, meets it: False
        repetition-3    |C| =      2, Hamming bound =       1, meets it: False
    RS over GF(256)    |C| =    256, Hamming bound =     255, meets it: False
```

The Singleton bound is the easy one: project every codeword onto any `n − d + 1`
of its `n` coordinates. Two codewords cannot agree on all of those, since
agreeing on `n − d + 1` positions means differing in at most `d − 1`. So the
projection is injective, and there are only `q^(n−d+1)` possible projections.

Perfect codes are rare because equality in the Hamming bound requires the
radius-`t` spheres around the codewords to *tile* the whole space with no gaps
and no overlaps — no codeword may be closer than `2t + 1 = d` to any other, and
every non-codeword must be within distance `t` of some codeword. Binary perfect
codes are known only at lengths 1, 3, 7, 15 and 31 — all Hamming — and it has
been proven that **no others exist**. That is why Hamming codes are in every
ECC controller ever made, and why no other code has that status.

</details>

## Summary

- The binary symmetric channel flips each bit independently with probability `p`;
  no sender can prevent it, only prepare for it.
- **Detection** asks "is this one of my words?", **correction** asks "which one?",
  and the second is strictly harder. Hence `detects = d − 1` but
  `corrects = ⌊(d−1)/2⌋`.
- Hamming distance is the count of differing positions; minimum distance `d`
  over a code decides both numbers. The correction bound comes from the triangle
  inequality: after `e` errors you must be closer to the truth than to anything
  else, so `2e < d`.
- **Parity** gives `d = 2`: detects one error, corrects none. **Repetition-3**
  gives `d = 3` at 3× the bandwidth. Both are the crude ends of the trade.
- Over `GF(2)` addition is XOR, so linear codes are XOR-combinations of a basis
  row, and a linear code's `d_min` is its smallest nonzero codeword weight.
- The **syndrome** `s = H·rᵀ` depends only on the error, not the message, so
  decoding is a lookup rather than a search over the codebook.
- In **Hamming(7,4)** the parity-check columns are the binary expansions of
  `1..7`, so the syndrome of a single-bit error *is* the flipped position.
  Three parity bits buy 43% redundancy and correction of one bit.
- **Hamming(8,4)** adds an overall parity bit so a decoder can tell one error
  from two — SECDED, which is what x86 ECC memory uses.
- **Reed-Solomon** runs the same syndrome machinery over `GF(2^m)`, correcting
  `t/2` corrupted *symbols* rather than bits, which is what burst errors like
  CD scratches and QR folds actually look like. Interleaving is what spreads a
  burst across codewords so it becomes correctable.

## Next

This is the last lesson in Part 09. The three ideas here — that arithmetic
modulo a number is a different algebra from arithmetic on numbers, that a
hash is a way of making a fixed-size fingerprint that is hard to invert, and
that redundancy can be spent to undo corruption as well as to detect it — are
the toolkit for [Part 10: Tensors and Numerical Methods](../part10_tensors_numerical/),
where the same themes reappear as floating-point precision, broadcasting rules,
and the difference between an exact computation and a stable one.