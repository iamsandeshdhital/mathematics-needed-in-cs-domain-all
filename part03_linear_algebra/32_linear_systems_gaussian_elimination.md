# 32 â€” Linear Systems and Gaussian Elimination

**Part**: part03_linear_algebra Â· **Prerequisites**: 31 Â· **Time**: 45 min

---

## In Plain Words

Almost every problem in science and engineering reduces to a list of equations
in a list of unknowns. "Three materials, three measurements, three unknowns."
"The flow balances at four junctions, four unknown pressures." "A network with
300 nodes and an unknown voltage at each." The unknowns are written as a list,
the coefficients of each equation are written as a row of numbers, and the two
together form a grid of numbers â€” a matrix. The measurements go in another
list. So the whole problem is: given this grid and this list, what is the list?

The algorithm for answering that has been known since the nineteenth century
and has one idea in it: use one equation to cancel a variable out of another
equation, repeatedly, until only one equation is left per variable. Then read the
answers off the end, substituting backwards. That is Gaussian elimination, it is
about thirty lines of code, and it runs in time proportional to the cube of the
number of unknowns.

The subtlety is that the order in which you pick equations matters enormously
for accuracy in floating point, and the fix is a single rule: always cancel using
the equation with the biggest coefficient of the variable being removed. That
rule is partial pivoting, and every production solver includes it.

The other thing to expect is that sometimes there is no single answer. The
equations might contradict each other, or they might not pin down every unknown.
Both cases are visible in the final arrangement of numbers, and telling them
apart takes one more look than counting pivots.

## Why Computer Science Cares

- **Every linear regression is a system of equations.** Least squares solves a
  huge, badly conditioned, sparse system on every model fit. The condition
  number of the design matrix is how you decide whether to normalise your
  features first. [Lesson 38](38_orthogonality_and_least_squares.md).
- **Graphics and physics engines** solve systems every frame: a rigid body has 6
  degrees of freedom and a constraint solver is a 6-by-6 solve.
- **Shortest path, Markov chains, PageRank** all involve solving a linear system
  once and reusing the factorisation, which is why libraries hand you the LU
  factors rather than just `A`.
- **Circuit simulation and mesh generation** solve banded or sparse systems where
  `O(nÂ³)` is hopeless and `O(n Â· bandwidthÂ²)` is required.
- **Iteration counts matter.** `O(nÂ³)` at `n = 10â´` is `3 Ã— 10Â¹Â¹` multiply-adds.
  Choosing a better formulation is not a micro-optimisation.
- **Interview questions.** "Implement Gaussian elimination", "how would you detect
  that a matrix is singular?", "what is partial pivoting and why does it matter?"
  are all standard, and this lesson answers them.

## The Formal Version

Symbols follow [SYMBOLS.md](../SYMBOLS.md).

**Definition.** A **linear system** over `F` in `n` unknowns is `Ax = b` with
`A` an `m Ã— n` matrix, `x âˆˆ Fâ¿`, and `b âˆˆ F^m`. The **augmented matrix** is the
`m Ã— (n+1)` matrix

    [A | b]  =  | a_11 ... a_1n  b_1 |
                 | ...              |
                 | a_m1 ... a_mn  b_m |

**Definition.** A **row operation** on a matrix is one of:

1. swapping two rows;
2. multiplying a row by a nonzero scalar;
3. adding a multiple of one row to another.

**Theorem.** Row operations preserve the solution set of `Ax = b`.

**Explanation.** Each operation corresponds to swapping two equations,
rescaling an equation by a nonzero constant, or adding a multiple of one equation
to another. All three preserve which assignments satisfy all equations. The
converse matters too: any two systems with the same solutions can be connected by
row operations.

**Definition.** A matrix is in **row echelon form** if (i) every nonzero row has
its leftmost nonzero entry strictly to the right of the one above it, and (ii)
all zero rows are at the bottom. It is in **reduced row echelon form** (RREF) if
additionally each leading entry is 1 and is the only nonzero in its column.

**Explanation.** Echelon form has triangular shape: zeros below the diagonal. RREF
additionally has zeros above it. With RREF there is nothing left to do â€” the
solution, if it exists, is visible.

**Theorem (Existence and uniqueness).** Let `[A | b]` reduce to RREF. Then:

- If some row is `[0 â€¦ 0 | c]` with `c â‰  0`, the system has **no solution**.
- Otherwise, if some column of `A` has no pivot, the system has **infinitely
  many solutions**.
- Otherwise the system has a **unique solution**, read off as the pivot column
  entries of the augmented matrix.

**Explanation.** A row `[0 â€¦ 0 | c]` is the equation `0 = c`. The leading entries
give pivot variables; a column with no pivot gives a free variable. Each free
variable contributes a parameter, and one parameter means infinitely many points.

**Definition.** The **pivot** of a step is the entry used as the divisor, and the
**multiplier** is `a_ik / a_kk`, the factor by which row `k` is scaled before
subtraction.

**Definition.** In **Gaussian elimination without pivoting**, the pivot for
column `k` is `a_kk`, whatever it happens to be. In **Gaussian elimination with
partial pivoting**, we first swap rows so that `|a_kk|` is the largest absolute
value in column `k` at or below row `k`.

**Theorem (Backward stability of partial pivoting).** Gaussian elimination with
partial pivoting satisfies `P A + Î”A = L U` with `â€–Î”Aâ€– â‰¤ 3nÂ·uÂ·â€–Aâ€–` and
`â€–Pâ€– = â€–Pâ»Â¹â€– = 1`, where `u` is the machine unit roundoff. Unpivoted elimination
has no comparable bound.

**Explanation.** The growth factor `g = max|U_ij| / max|A_ij|` measures how much
entries are magnified. Pivoting keeps `g â‰¤ 2^(n-1)` and typically `g` near 1, so
each entry carries at most a factor `n Â· u` of relative error. Without pivoting
`g` can be arbitrarily large, and the error is amplified by it. A full discussion
of floating point arithmetic is Part 10, lesson 121.

**Definition.** The **LU factorisation** of an invertible `A` is `P A = L U` with
`L` lower triangular with ones on the diagonal and `U` upper triangular. With
partial pivoting, `P` is the product of the row swaps.

**Theorem.** `A x = b` reduces to `U x = y` where `y` solves `L y = P b`. Both
triangular systems are solved by substitution in `O(nÂ²)`.

**Explanation.** Substitute `A = Pâ»Â¹LU = Páµ€LU` into `Ax = b` and multiply through
by `P`. `L` has ones on the diagonal, so the first unknown of the first equation
is determined immediately, and each subsequent one after that.

**Theorem (Complexity).** Gaussian elimination is `Î˜(nÂ³)`; a single triangular
solve is `Î˜(nÂ²)`; the whole factor-then-solve-many loop is `Î˜(nÂ³ + k nÂ²)` for `k`
right-hand sides.

**Explanation.** At step `k` of elimination you eliminate `n - k` rows, each
touching `n - k` entries, so `Î£_k (n-k)Â² â‰ˆ nÂ³/3`. Back substitution is `nÂ²/2`.

## Worked Example

Solve

    2xâ‚€ +  xâ‚ -  xâ‚‚ =  8
   -3xâ‚€ -  xâ‚ + 2xâ‚‚ = -11
   -2xâ‚€ +  xâ‚ + 2xâ‚‚ =  -3

Build the augmented matrix and apply partial pivoting.

**Step 1: write `[A | b]`.**

    |  2   1  -1 |   8 |
    | -3  -1   2 | -11 |
    | -2   1   2 |  -3 |

**Step 2: choose the pivot for column 0.** The candidates are `2`, `-3`, `-2`.
The largest magnitude is `3`, so the pivot is `-3` and we swap rows 0 and 1:

    | -3  -1   2 | -11 |
    |  2   1  -1 |   8 |
    | -2   1   2 |  -3 |

**Step 3: eliminate column 0 from rows 1 and 2.**

Row 1 multiplier: `2 / -3 = -2/3`. Row 1 becomes

    2 - (-2/3)(-3) = 2 - 2 = 0
    1 - (-2/3)(-1) = 1 - 2/3 = 1/3
   -1 - (-2/3)( 2) = -1 + 4/3 = 1/3
    8 - (-2/3)(-11) = 8 - 22/3 = 2/3

Row 2 multiplier: `-2 / -3 = 2/3`. Row 2 becomes

   -2 - (2/3)(-3) = -2 + 2 = 0
    1 - (2/3)(-1) = 1 + 2/3 = 5/3
    2 - (2/3)( 2) = 2 - 4/3 = 2/3
   -3 - (2/3)(-11) = -3 + 22/3 = 13/3

So far:

    | -3  -1   2  | -11 |
    |  0   1/3  1/3 | 2/3 |
    |  0   5/3  2/3 | 13/3 |

**Step 4: choose the pivot for column 1.** The candidates are `1/3` and `5/3`.
Largest is `5/3`, in row 2, so swap rows 1 and 2:

    | -3  -1   2   | -11 |
    |  0   5/3  2/3 | 13/3 |
    |  0   1/3  1/3 |  2/3 |

**Step 5: eliminate column 1 from row 2.** Multiplier
`(1/3) / (5/3) = 1/5`. Row 2 becomes

    1/3 - (1/5)(5/3) = 1/3 - 1/3 = 0
    1/3 - (1/5)(2/3) = 1/3 - 2/15 = 3/15 = 1/5
    2/3 - (1/5)(13/3) = 2/3 - 13/15 = 10/15 - 13/15 = -1/5

    | -3  -1   2   | -11 |
    |  0   5/3  2/3 | 13/3 |
    |  0   0   1/5 | -1/5 |

Upper triangular.

**Step 6: back substitution.**

    xâ‚‚ = (-1/5) / (1/5) = -1
    xâ‚ = (13/3 - (2/3)(-1)) / (5/3) = (13/3 + 2/3) / (5/3) = 5 / (5/3) = 3
    xâ‚€ = (-11 - (-1)(3) - (2)(-1)) / (-3) = (-11 + 3 + 2) / (-3) = -6 / -3 = 2

So `x = [2, 3, -1]`.

**Step 7: verify.** Substitute back into the original equations:

    2(2) + 3 - (-1) = 4 + 3 + 1 = 8   âœ“
    -3(2) - 3 + 2(-1) = -6 - 3 - 2 = -11  âœ“
    -2(2) + 3 + 2(-1) = -4 + 3 - 2 = -3   âœ“

**A worked system with no unique solution.** Now consider

     xâ‚€ + 2xâ‚ =  5
    3xâ‚€ -  xâ‚ =  9
    4xâ‚€ +  xâ‚ = 14

Row 2 is row 0 plus row 1 on the left: `(1 + 3, 2 + (-1)) = (4, 1)`. And
`5 + 9 = 14`, so the right sides agree too. Row 2 adds nothing.

Reduce: multiplier `3/1 = 3` on row 1, multiplier `4/1 = 4` on row 2.

    Row 1:  3 - 3(1) = 0,  -1 - 3(2) = -7,   9 - 3(5) = -6
    Row 2:  4 - 4(1) = 0,   1 - 4(2) = -7,  14 - 4(5) = -6

    | 1  2 |  5 |
    | 0 -7 | -6 |
    | 0 -7 | -6 |

RREF, pivoting on the `-7`:

    | 1  2  |  5 |
    | 0  1  | 6/7 |
    | 0  0  |  0 |

Now the question. Column 1 has no pivot â€” it is a free variable. Set `xâ‚ = t`:

    xâ‚€ = 5 - 2t

Every `t` gives a solution, and the third equation added no constraint.

**A worked system with no solution.** Change only the last right-hand side to
`15`:

    Row 2:  14 â†’ 15.  Multiplier 4:  15 - 4(5) = -5.

    | 1  2 |  5 |
    | 0 -7 | -6 |
    | 0 -7 | -5 |

RREF:

    | 1  2  |   5 |
    | 0  1  | 6/7 |
    | 0  0  | -5/7 |

The last row reads `0 = -5/7`. That is false, so no assignment of `xâ‚€, xâ‚`
satisfies all three equations. That row is the whole diagnosis: the equations
contradict each other.

Notice how little changed between the last two cases â€” one number on the right
side. That is the practical point: distinguishing "no answer" from "many
answers" is a matter of inspecting one row, and the code below does exactly that.

## Runnable Code

### Forward elimination and back substitution

The full solver, written from scratch, with partial pivoting at every step.

```python
TOL = 1e-9


# ---------------------------------------------------------------- helpers
def shape(M):
    return len(M), len(M[0])


def augmented(A, b):
    """Stack b as an extra column: the augmented matrix [A | b]."""
    return [list(A[i]) + [b[i]] for i in range(len(A))]


def print_system(label, A, b):
    rows, cols = shape(A)
    print(f"{label}")
    for i in range(rows):
        terms = []
        for j in range(cols):
            if j == 0:
                terms.append(f"{A[i][j]:g}*x{j}")
            elif A[i][j] >= 0:
                terms.append(f"+ {A[i][j]:g}*x{j}")
            else:
                terms.append(f"- {abs(A[i][j]):g}*x{j}")
        print("  " + " ".join(terms) + f" = {b[i]:g}")
    print()


def show(rows, note=""):
    for i, row in enumerate(rows):
        tag = f"  <- {note}" if i == len(rows) - 1 and note else ""
        print(f"  row {i}: " + " ".join(f"{x:9.4f}" for x in row) + tag)


# ---------------------------------------------------------------- elimination
def forward_elimination(A, b, tol=TOL):
    """Reduce [A | b] to upper-triangular form in place.

    Walk down the columns. For each column, find a row at or below the current
    position with a nonzero entry there (partial pivoting: the largest one),
    swap it up to the pivot row, and eliminate that column from every row below.
    """
    M = augmented(A, b)
    rows, cols = len(M), len(M[0])
    pivot_row = 0

    for col in range(cols - 1):          # the last column is b, never a pivot
        if pivot_row == rows:
            break
        # Partial pivoting: choose the row whose entry here is largest in
        # absolute value, so we never divide by a tiny number.
        best = max(range(pivot_row, rows), key=lambda r: abs(M[r][col]))
        if abs(M[best][col]) <= tol:
            continue                      # free column, no pivot available
        M[pivot_row], M[best] = M[best], M[pivot_row]

        pivot = M[pivot_row][col]
        for r in range(pivot_row + 1, rows):
            factor = M[r][col] / pivot
            if factor == 0.0:
                continue
            for c in range(col, cols):
                M[r][c] -= factor * M[pivot_row][c]

        pivot_row += 1

    return M


def back_substitution(U, tol=TOL):
    """Solve U x = rhs for upper-triangular U. Assumes every column is a pivot."""
    n = len(U)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        total = U[i][n] - sum(U[i][j] * x[j] for j in range(i + 1, n))
        if abs(U[i][i]) <= tol:
            raise ZeroDivisionError("singular: no unique solution")
        x[i] = total / U[i][i]
    return x


def solve(A, b, tol=TOL):
    """Solve A x = b by Gaussian elimination with partial pivoting."""
    return back_substitution(forward_elimination(A, b, tol), tol)


# ---------------------------------------------------------------- the example
A = [[2.0, 1.0, -1.0],
     [-3.0, -1.0, 2.0],
     [-2.0, 1.0, 2.0]]
b = [8.0, -11.0, -3.0]

print_system("Start: A x = b", A, b)
U = forward_elimination(A, b)
print("After forward elimination (upper triangular):")
for row in U:
    print("  " + " ".join(f"{x:9.4f}" for x in row))
print()

x = solve(A, b)
print("Back substitution gives x =", [round(v, 10) for v in x])
check = [sum(A[i][j] * x[j] for j in range(3)) for i in range(3)]
print("A x =", [round(v, 10) for v in check])
print("matches b:", all(abs(check[i] - b[i]) < 1e-9 for i in range(3)))

# Now the same computation by hand, one operation at a time.
print()
print("=== Every elimination step, spelled out ===")
M = augmented(A, b)
show(M)

print()
print("Column 0 holds 2, -3, -2. The largest magnitude is 3, in row 1, so swap")
print("row 0 with row 1. That is partial pivoting, and it is why the pivot")
print("below is -3 rather than 2.")
M[0], M[1] = M[1], M[0]
show(M)

print()
f1 = M[1][0] / M[0][0]
print(f"Column 0: factor for row 1 = {M[1][0]:g} / {M[0][0]:g} = {f1:.4f}")
M[1] = [M[1][c] - f1 * M[0][c] for c in range(4)]
print(f"  row 1 -= {f1:.4f} * row 0")
f2 = M[2][0] / M[0][0]
print(f"Column 0: factor for row 2 = {M[2][0]:g} / {M[0][0]:g} = {f2:.4f}")
M[2] = [M[2][c] - f2 * M[0][c] for c in range(4)]
print(f"  row 2 -= {f2:.4f} * row 0")
show(M)

print()
print("Column 0 is clear below the pivot. Column 1 now holds "
      f"{M[1][1]:.4f} and {M[2][1]:.4f}.")
print(f"The larger is {M[2][1]:.4f} in row 2, so swap them up.")
M[1], M[2] = M[2], M[1]
show(M)

f3 = M[2][1] / M[1][1]
print()
print(f"Column 1: factor = {M[2][1]:.4f} / {M[1][1]:.4f} = {f3:.4f}")
M[2] = [M[2][c] - f3 * M[1][c] for c in range(4)]
print(f"  row 2 -= {f3:.4f} * row 1")
show(M)

print()
print("Upper triangular: zeros below the diagonal, three pivots on it.")
print("Back substitution from the bottom up. At row i, x_i is the only unknown")
print("left, so divide the residual by the pivot.")
xsol = back_substitution(M)
for i in range(2, -1, -1):
    residual = M[i][3] - sum(M[i][j] * xsol[j] for j in range(i + 1, 3))
    print(f"  row {i}: residual {residual:.4f} / pivot {M[i][i]:.4f} = {xsol[i]:.6f}")
print(f"x = {[round(v, 6) for v in xsol]}")
print("matches the automatic answer:",
      all(abs(xsol[i] - x[i]) < 1e-12 for i in range(3)))
print()
print("Sanity check by substitution into the original equations:")
for i in range(3):
    lhs = sum(A[i][j] * x[j] for j in range(3))
    print(f"  eq {i}: {lhs:.6f} (right side {b[i]:g})  "
          f"{'ok' if abs(lhs - b[i]) < 1e-9 else 'WRONG'}")
```

### The three cases: unique, none, infinite

RREF is the diagnostic tool. It always produces the same shape of answer, and
the answer is read off the last column and the pivot pattern.

```python
TOL = 1e-9


# ---------------------------------------------------------------- helpers
def augmented(A, b):
    return [list(A[i]) + [b[i]] for i in range(len(A))]


def rref(A, b, tol=TOL):
    """Full reduced row echelon form of [A | b].

    Loops over columns, and for each one eliminates it from EVERY row, not just
    the rows below. That makes each pivot the only nonzero in its column, which
    is what "reduced" means and why the free variables fall out by inspection.
    """
    M = augmented(A, b)
    rows, cols = len(M), len(M[0])
    pivot_row = 0
    pivots = []

    for col in range(cols - 1):
        if pivot_row == rows:
            break
        best = max(range(pivot_row, rows), key=lambda r: abs(M[r][col]))
        if abs(M[best][col]) <= tol:
            continue
        M[pivot_row], M[best] = M[best], M[pivot_row]

        pivot = M[pivot_row][col]
        M[pivot_row] = [v / pivot for v in M[pivot_row]]

        for r in range(rows):
            if r == pivot_row:
                continue
            factor = M[r][col]
            if factor == 0.0:
                continue
            M[r] = [M[r][c] - factor * M[pivot_row][c] for c in range(cols)]

        pivots.append(col)
        pivot_row += 1

    return M, pivots


def classify(A, b, tol=TOL):
    """Classify A x = b as unique, none, or infinite.

    Returns (kind, rref_matrix, pivot_columns) where kind is one of
    'unique', 'none', 'infinite'.
    """
    M, pivots = rref(A, b, tol)
    rows = len(M)
    cols = len(A[0])
    last = cols                      # index of the b column

    # A row [0 ... 0 | nonzero] is the contradiction 0 = nonzero.
    for i in range(rows):
        if all(abs(M[i][j]) <= tol for j in range(cols)):
            if abs(M[i][last]) > tol:
                return "none", M, pivots

    if len(pivots) < cols:
        return "infinite", M, pivots
    return "unique", M, pivots


def print_rref(label, M):
    print(label)
    for row in M:
        print("  " + " ".join(f"{x:9.4f}" for x in row))
    print()


# ---------------------------------------------------------------- case 1
print("=== Case 1: a unique solution ===")
A1 = [[2.0, 1.0, -1.0], [-3.0, -1.0, 2.0], [-2.0, 1.0, 2.0]]
b1 = [8.0, -11.0, -3.0]
M1, piv1 = rref(A1, b1)
print_rref("Reduced row echelon form:", M1)
print("pivot columns:", piv1)
print("every column is a pivot, so the answer is unique and is the last column,")
print("read straight off the RREF with no back substitution at all:")
print(f"  x = {[round(row[3], 10) for row in M1]}")

# ---------------------------------------------------------------- case 2
print("=== Case 2: no solution ===")
# A[2] is A[0] + A[1], so the left sides cancel exactly. If b[2] is anything
# other than b[0] + b[1], the right sides do not cancel, and we get 0 = nonzero.
A2 = [[1.0, 2.0], [3.0, -1.0], [4.0, 1.0]]
b2 = [5.0, 4.0, 10.0]
M2, piv2 = rref(A2, b2)
print_rref("Reduced row echelon form:", M2)
print("pivot columns:", piv2)
kind2, _, _ = classify(A2, b2)
print(f"classify -> {kind2}")
print("Row 0 plus row 1 gives (4, 1) on the left, and row 2 is (4, 1) too, so")
print("subtracting leaves 0 on the left but 5 + 4 - 10 = -1 on the right. The")
print("last row of the RREF says exactly that: 0 = -1, which is false.")

# ---------------------------------------------------------------- case 3
print("=== Case 3: infinitely many solutions ===")
# Three unknowns, but only two independent equations. x0 and x2 always appear
# together, so the system cannot pin down either one on its own.
A3 = [[1.0, 2.0, 1.0],
      [3.0, -1.0, 3.0],
      [4.0, 1.0, 4.0]]
b3 = [5.0, 10.0, 15.0]
M3, piv3 = rref(A3, b3)
print_rref("Reduced row echelon form (b = 5, 10, 15):", M3)
print("pivot columns:", piv3)
kind3, _, _ = classify(A3, b3)
print(f"classify -> {kind3}")
print("No row of the form 0 = nonzero, and only two columns have pivots, so one")
print("unknown is free. Set it to t and everything else follows.")

# Pull the particular solution and null direction straight out of the RREF.
ncols = len(A3[0])
free_cols = [c for c in range(ncols) if c not in piv3]
particular = [0.0] * ncols
for i, pc in enumerate(piv3):
    particular[pc] = M3[i][ncols]
print(f"\nfree column(s): {free_cols}")
print(f"setting the free variable(s) to zero gives x_p = "
      f"{[round(v, 4) for v in particular]}")
check_xp = all(abs(sum(A3[i][j] * particular[j] for j in range(ncols)) - b3[i]) < 1e-9
               for i in range(len(A3)))
print(f"x_p satisfies every equation: {check_xp}")

for fc in free_cols:
    direction = [0.0] * ncols
    direction[fc] = 1.0
    for i, pc in enumerate(piv3):
        direction[pc] = -M3[i][fc]
    check_v = all(abs(sum(A3[i][j] * direction[j] for j in range(ncols))) < 1e-9
                  for i in range(len(A3)))
    print(f"\nfree variable x{fc} = t:")
    print(f"  null direction v = {[round(v, 4) for v in direction]}")
    print(f"  A v = 0: {check_v}")
    for t in (-2.0, 0.0, 1.5, 100.0):
        xt = [particular[j] + t * direction[j] for j in range(ncols)]
        ok = all(abs(sum(A3[i][j] * xt[j] for j in range(ncols)) - b3[i]) < 1e-9
                 for i in range(len(A3)))
        print(f"    t = {t:6.1f} -> x = {[round(v, 4) for v in xt]}  solves it: {ok}")
    print(f"  every solution is x_p + t * v for some t, so there are infinitely many.")

# ---------------------------------------------------------------- summary
print()
print("=== All three cases side by side ===")
cases = [
    ("unique", A1, b1),
    ("none", A2, b2),
    ("infinite", A3, b3),
]
for label, A, b in cases:
    kind, M, pivots = classify(A, b)
    print(f"  intended {label:9s} -> classify says {kind:9s} "
          f"({len(pivots)} pivots, {len(A[0])} columns)")

print()
print("Rule of thumb. Count the pivots, then look at the last column:")
print("  pivots == columns, and no all-zero row  ->  unique solution")
print("  an all-zero row with a nonzero b entry  ->  0 = nonzero, no solution")
print("  pivots < columns, no contradiction        ->  free variables, infinitely many")
print("For an n-by-n A, 'unique' is exactly 'A is invertible'. Lesson 33 gives a")
print("one-line test for that, the determinant, with no arithmetic at all.")
```

### Why pivoting is not optional

A system where dividing by the first available pivot destroys the answer, and
the LU factorisation that avoids doing it repeatedly.

```python
TOL = 1e-9


# ---------------------------------------------------------------- helpers
def augmented(A, b):
    return [list(A[i]) + [b[i]] for i in range(len(A))]


def forward_elimination(A, b, tol=TOL, pivot=True):
    """Reduce [A | b] to upper-triangular form.

    pivot=True uses partial pivoting: for each column, move the row with the
    largest absolute entry in that column up to the pivot position.
    pivot=False takes whatever row happens to be there.
    """
    M = augmented(A, b)
    rows, cols = len(M), len(M[0])
    pivot_row = 0
    swaps = 0
    max_scale = max(abs(v) for row in M for v in row)

    for col in range(cols - 1):
        if pivot_row == rows:
            break
        if pivot:
            best = max(range(pivot_row, rows), key=lambda r: abs(M[r][col]))
        else:
            best = pivot_row
        if abs(M[best][col]) <= tol:
            continue
        if best != pivot_row:
            M[pivot_row], M[best] = M[best], M[pivot_row]
            swaps += 1

        p = M[pivot_row][col]
        for r in range(pivot_row + 1, rows):
            factor = M[r][col] / p
            if factor == 0.0:
                continue
            for c in range(col, cols):
                M[r][c] -= factor * M[pivot_row][c]
        pivot_row += 1

    # The growth factor is the largest entry in the reduced matrix divided by
    # the largest entry in the original. A value much bigger than 1 means
    # rounding error is being magnified on the way.
    scale = max(abs(v) for row in M for v in row)
    growth = scale / max_scale

    return M, swaps, growth


def back_substitution(U, tol=TOL):
    n = len(U)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        total = U[i][n] - sum(U[i][j] * x[j] for j in range(i + 1, n))
        x[i] = total / U[i][i]
    return x


def relative_error(approx, exact):
    scale = max(abs(v) for v in exact)
    return max(abs(a - e) for a, e in zip(approx, exact)) / max(scale, 1e-300)


# ------------------------------------------------ why pivoting is necessary
print("=== A system where naive elimination loses the answer entirely ===")
# Both rows have an entry of size 1e-11 in column 0 and an entry of size 1
# beside it. If we pivot on the 1e-11, every multiplier is about 1e11 and the
# intermediate entries reach 1e11. Pivoting picks the 1 instead.
A_small = [[1e-11, 1.0],
           [1.0, 1.0 + 1e-11]]
b_small = [1.0, 1.0]
print(f"A =\n{A_small}")
print(f"b = {b_small}")

# Use a tight tolerance so that 1e-11 counts as a real pivot rather than a zero.
U_np, swaps_np, growth_np = forward_elimination(A_small, b_small, tol=0.0, pivot=False)
x_np = back_substitution(U_np)
print()
print("Without pivoting:")
for i, row in enumerate(U_np):
    print(f"  row {i}: " + " ".join(f"{v:>18.6e}" for v in row))
print(f"  x         = {x_np}")
print(f"  growth factor = {growth_np:.3e}")

U_p, swaps_p, growth_p = forward_elimination(A_small, b_small, pivot=True)
x_p = back_substitution(U_p)
print()
print(f"With partial pivoting ({swaps_p} row swap):")
for i, row in enumerate(U_p):
    print(f"  row {i}: " + " ".join(f"{v:>18.6e}" for v in row))
print(f"  x         = {[float(f'{v:.17g}') for v in x_p]}")
print(f"  growth factor = {growth_p:.3e}")

# The exact answer, in exact rational arithmetic with no rounding at all.
from fractions import Fraction as Fr

A_exact = [[Fr(1, 10 ** 11), Fr(1)], [Fr(1), Fr(1) + Fr(1, 10 ** 11)]]
b_exact = [Fr(1), Fr(1)]
d = A_exact[0][0] * A_exact[1][1] - A_exact[0][1] * A_exact[1][0]
x_exact = [
    (b_exact[0] * A_exact[1][1] - A_exact[0][1] * b_exact[1]) / d,
    (A_exact[0][0] * b_exact[1] - b_exact[0] * A_exact[1][0]) / d,
]
print()
print("exact answer in rational arithmetic: x =",
      [f"{float(v):.17g}" for v in x_exact])
print(f"relative error, no pivoting : {relative_error(x_np, x_exact):.3e}")
print(f"relative error, with pivot  : {relative_error(x_p, x_exact):.3e}")
print()
print("The no-pivot answer reports x0 = 0.0 exactly, when the true value is")
print(f"{-1.0000000000099999e-11:.3e}. It is not slightly wrong, it is completely")
print("wrong: the cancellation `1.00000000001 - 1.0` should have left 1e-11 and")
print("left nothing at all. The residual |Ax - b| will not reveal this, because")
print("the wrong x still produces a small residual when the matrix is nearly")
print(f"singular. The growth factor is the warning: {growth_np:.0f} versus "
      f"{growth_p:.0f}.")

# ------------------------------------------------ LU: factor once, solve many
print()
print("=== LU factorisation: A = L U, computed once ===")


def lu_factor(A, tol=TOL):
    """Crout LU with partial pivoting. Returns (L, U, perm) with P A = L U."""
    n = len(A)
    U = [list(row) for row in A]
    L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    perm = list(range(n))
    for k in range(n):
        best = max(range(k, n), key=lambda r: abs(U[r][k]))
        if best != k:
            # Swap rows of U, and of the already-computed part of L.
            U[k], U[best] = U[best], U[k]
            for j in range(k):
                L[k][j], L[best][j] = L[best][j], L[k][j]
            perm[k], perm[best] = perm[best], perm[k]
        if abs(U[k][k]) <= tol:
            raise ZeroDivisionError("singular matrix")
        for i in range(k + 1, n):
            L[i][k] = U[i][k] / U[k][k]
            for j in range(k, n):
                U[i][j] -= L[i][k] * U[k][j]
    return L, U, perm


def lu_solve(L, U, perm, b):
    """L U x = b: permute b, forward-substitute, then back-substitute."""
    n = len(L)
    y = [b[perm[i]] for i in range(n)]        # apply the row permutation
    for i in range(n):                        # forward: L y = P b
        y[i] -= sum(L[i][j] * y[j] for j in range(i))
    x = [0.0] * n
    for i in range(n - 1, -1, -1):            # back: U x = y
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
    return x


A = [[2.0, 1.0, -1.0],
     [-3.0, -1.0, 2.0],
     [-2.0, 1.0, 2.0]]
L, U, perm = lu_factor(A)
print("A =\n", A)
print("L =\n", [[round(v, 6) for v in row] for row in L])
print("U =\n", [[round(v, 6) for v in row] for row in U])
print("perm =", perm, "(row i of L U equals row perm[i] of A)")

PA = [[A[perm[i]][j] for j in range(3)] for i in range(3)]
rebuilt = [[sum(L[i][k] * U[k][j] for k in range(3)) for j in range(3)]
           for i in range(3)]
print("L U =\n", [[round(v, 6) for v in row] for row in rebuilt])
print("P A =\n", PA)
print("LU reproduces PA:", all(abs(rebuilt[i][j] - PA[i][j]) < 1e-9
                               for i in range(3) for j in range(3)))
print("L has ones on the diagonal:", all(abs(L[i][i] - 1.0) < 1e-12 for i in range(3)))
print("L is lower triangular:", all(abs(L[i][j]) < 1e-12 for i in range(3) for j in range(i + 1, 3)))
print("U is upper triangular:", all(abs(U[i][j]) < 1e-12 for i in range(3) for j in range(i)))

print()
print("Solving four systems that share the same A:")
for b in ([8.0, -11.0, -3.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [2.0, 2.0, 2.0]):
    x = lu_solve(L, U, perm, b)
    resid = max(abs(sum(A[i][j] * x[j] for j in range(3)) - b[i]) for i in range(3))
    print(f"  b = {b}  ->  x = {[round(v, 6) for v in x]}  residual {resid:.2e}")
print("The expensive O(n^3) factorisation happened once. Each extra right-hand")
print("side costs only the two triangular solves, O(n^2). That is why a linear")
print("solver takes the factorisation as input and not just A.")

# ------------------------------------------------ complexity
print()
print("=== Cost accounting ===")
n = 100
print(f"forward elimination on an n-by-n system, n = {n}:")
print(f"  roughly n^3/3 multiply-adds = {n ** 3 // 3}")
print(f"back substitution:             n^2/2   = {n * n // 2}")
print("so the total is dominated by the O(n^3) forward pass.")
print()
print("Scaling to larger n:")
for size in (10, 100, 1000, 10000):
    print(f"  n = {size:6d}: n^3/3 = {size ** 3 // 3:>16,} multiply-adds")
print("Going from n = 100 to n = 1000 multiplies the work by about 1000.")
print("Going from 1000 to 10000 multiplies it by about 1000 again. This is why")
print("an O(n^3) solver is fine up to a few thousand unknowns and useless")
print("beyond, and why sparse structure is worth chasing: an n-by-n matrix with")
print("k nonzeros per row costs about O(n k^2), not O(n^3).")
```

### With Libraries

```python
# The plain-Python solver above is a faithful implementation of the textbook
# algorithm. numpy gives the same answers in one call, and its underlying LAPACK
# routines do exactly what partial pivoting, LU, and iterative refinement do.

import numpy as np

A = np.array([[2.0, 1.0, -1.0],
              [-3.0, -1.0, 2.0],
              [-2.0, 1.0, 2.0]])
b = np.array([8.0, -11.0, -3.0])

print("=== solve: one call ===")
x = np.linalg.solve(A, b)
print(f"A =\n{A}")
print(f"b = {b}")
print(f"x = {x}")
print(f"A x = {A @ x}")
print(f"matches the hand-computed [2, 3, -1]: {np.allclose(x, [2, 3, -1])}")

print()
print("=== solve vs inv: never form the inverse ===")
Ainv = np.linalg.inv(A)
print(f"inv(A) =\n{np.round(Ainv, 6)}")
print(f"inv(A) @ b   = {np.round(Ainv @ b, 10)}")
print(f"solve(A, b) = {x}")
print("They agree here, but np.linalg.inv(A) @ b is slower and less accurate,")
print("because the inverse is computed in full and then applied. solve factors")
print("once and immediately substitutes. Never write inv(A) @ b in real code.")

print()
print("=== Detecting singularity ===")
# np.linalg.solve raises LinAlgError for an exactly singular matrix.
singular = np.array([[1.0, 2.0], [2.0, 4.0]])
try:
    np.linalg.solve(singular, np.array([1.0, 2.0]))
except np.linalg.LinAlgError as err:
    print(f"np.linalg.solve on a singular matrix raises: {err}")

# A nearly singular matrix does not raise. It just gives a large, unreliable x.
nearly = np.array([[1.0, 1.0], [1.0, 1.0 + 1e-12]])
print(f"cond(nearly singular) = {np.linalg.cond(nearly):.3e}")
print(f"solve(nearly, [1, 1]) = {np.linalg.solve(nearly, np.array([1.0, 1.0]))}")
print("An enormous x is the signature. Check np.linalg.cond before trusting it.")

print()
print("=== Rank and least squares, the modern way ===")
# A system with no unique answer: numpy does not raise, it gives the least
# squares solution with minimum norm.
consistent_but_dependent = np.array([[1.0, 2.0, 1.0],
                                     [3.0, -1.0, 3.0],
                                     [4.0, 1.0, 4.0]])
target = np.array([5.0, 10.0, 15.0])
ls, residuals, rank, sv = np.linalg.lstsq(consistent_but_dependent, target, rcond=None)
print(f"matrix rank = {rank} (three columns, so one unknown is undetermined)")
print(f"minimum-norm solution = {np.round(ls, 6)}")
print(f"singular values = {np.round(sv, 6)}")
print(f"residual = {np.round(consistent_but_dependent @ ls - target, 12)}")
print("This is the infinite-solution case: the RREF said 'free variable x2', and")
print("lstsq returns the point of that line nearest the origin.")

# An inconsistent system: numpy returns the closest fit, not an error.
inconsistent = np.array([[1.0, 2.0],
                         [3.0, -1.0],
                         [4.0, 1.0]])
bad_target = np.array([5.0, 4.0, 10.0])
ls2, res2, rank2, _ = np.linalg.lstsq(inconsistent, bad_target, rcond=None)
print()
print(f"inconsistent system: rank {rank2}, minimum-norm fit = {np.round(ls2, 6)}")
print(f"predicted = {np.round(inconsistent @ ls2, 6)}")
print(f"target    = {bad_target}")
print("The fit is close but not exact. Residuals are how you tell the two cases")
print("apart, and why every real solver reports them.")

print()
print("=== Iterative refinement: repairing a bad solve without refactorising ===")
# A_ill has one entry 1e-11 beside entries of size 1, so a solver that pivots
# badly will lose the small value entirely. Reproduce that by eliminating
# without pivoting, then repair the answer with the standard two-line trick.
A_ill = np.array([[1e-11, 1.0],
                  [1.0, 1.0 + 1e-11]])
b_ill = np.array([1.0, 1.0])


def solve_without_pivoting(A, b):
    """Deliberately bad: pivots on whatever entry happens to be there."""
    M = np.column_stack([A, b.copy()])
    n = len(A)
    for c in range(n - 1):
        for r in range(c + 1, n):
            f = M[r, c] / M[c, c]
            M[r, c:] -= f * M[c, c:]
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (M[i, n] - M[i, i + 1:n] @ x[i + 1:]) / M[i, i]
    return x


# The exact answer in exact rational arithmetic, for comparison.
from fractions import Fraction as Fr

Ae = [[Fr(1, 10 ** 11), Fr(1)], [Fr(1), Fr(1) + Fr(1, 10 ** 11)]]
be = [Fr(1), Fr(1)]
det = Ae[0][0] * Ae[1][1] - Ae[0][1] * Ae[1][0]
x_exact = np.array([
    float((be[0] * Ae[1][1] - Ae[0][1] * be[1]) / det),
    float((Ae[0][0] * be[1] - be[0] * Ae[1][0]) / det),
])

x_bad = solve_without_pivoting(A_ill, b_ill)
print(f"A = \n{A_ill}")
print(f"exact x            = {x_exact}")
print(f"naive (no pivoting) = {x_bad}   error {np.abs(x_bad - x_exact).max():.3e}")

# Refinement: r = b - A x, then x += solve(A, r). Reuses the factorisation, so
# it costs two matvecs rather than another factorisation.
r = b_ill - A_ill @ x_bad
x_fixed = x_bad + np.linalg.solve(A_ill, r)
print(f"after one refinement = {x_fixed}   error {np.abs(x_fixed - x_exact).max():.3e}")
print(f"residual before: {np.abs(A_ill @ x_bad - b_ill).max():.3e}")
print(f"residual after:  {np.abs(A_ill @ x_fixed - b_ill).max():.3e}")
print("The naive residual was already tiny, at the same size as the answer's")
print("error, which is why a residual check alone cannot be trusted on a badly")
print("scaled system. Refinement uses the residual as a direction and fixes the")
print("error anyway. Cost per step is O(n^2), not the O(n^3) of a refactorisation.")

print()
print("=== Banded and sparse: structure numpy and scipy exploit ===")
n = 8
band = np.zeros((n, n))
np.fill_diagonal(band, 4.0)
for i in range(n - 1):
    band[i, i + 1] = band[i + 1, i] = -1.0
rhs = np.ones(n)
print(f"tridiagonal {n}x{n} system, dense solve:")
dense_x = np.linalg.solve(band, rhs)
print(f"  x = {np.round(dense_x, 6)}")

from scipy.linalg import solve_banded

# Banded storage: three rows holding the superdiagonal, the main diagonal, and
# the subdiagonal. The convention is ab[upper + i - j, j] == a[i, j], so
# ab[0, 1:] is the superdiagonal and ab[2, :-1] is the subdiagonal. Only 3n
# numbers are stored instead of n^2.
ab = np.zeros((3, n))
ab[0, 1:] = np.diag(band, 1)
ab[1, :] = np.diag(band)
ab[2, :-1] = np.diag(band, -1)
print(f"banded storage array (3 x {n}):\n{ab}")
band_x = solve_banded((1, 1), ab, rhs)
print(f"  scipy solve_banded x = {np.round(band_x, 6)}")
print(f"  agrees with dense: {np.allclose(dense_x, band_x)}")
print(f"  storage: {3 * n} numbers instead of {n * n}")

print()
print("=== What the library does under the hood ===")
# LU with partial pivoting is one LAPACK call, and it gives exactly the objects
# we built by hand: L, U, and the row permutation.
from scipy.linalg import lu_factor as sp_lu_factor, lu_solve as sp_lu_solve

packed, ipiv = sp_lu_factor(A)
# LAPACK packs L (unit diagonal, lower part) and U (upper part) into one
# matrix, and returns ipiv, a record of which row was swapped at each step
# rather than a plain permutation vector.
lower = np.tril(packed, -1) + np.eye(3)
upper = np.triu(packed)
print("LAPACK P A = L U")
print(f"L =\n{np.round(lower, 6)}")
print(f"U =\n{np.round(upper, 6)}")
print(f"ipiv (row swap record) = {ipiv}")
print(f"L U =\n{np.round(lower @ upper, 6)}")
print(f"A   =\n{A}")
print("L U is A with its first two rows swapped, exactly the permutation our")
print("hand-written Crout routine applied (perm = [1, 2, 0] there).")
print(f"lu_solve reproduces our hand-written answer [2, 3, -1]: "
      f"{np.allclose(sp_lu_solve((packed, ipiv), b), [2, 3, -1])}")
print("Identical objects, different loop order: the library blocks the loops")
print("for cache and calls BLAS. That is the entire value of the library.")
```

## Common Mistakes

**Mistake 1: no pivoting.** The wrong version: divide by `a_kk` because it is
there. The right version: search the column for the largest absolute entry and
swap it into position. Without pivoting, the no-pivot example above returns
`xâ‚€ = 0.0` when the answer is `-1e-11` â€” and the residual is zero, so nothing
warns you. Every production solver pivots; it costs one pass over a column.

**Mistake 2: mutating the caller's matrix.** The wrong version: `M = A` then
`M[r][c] -= ...`, which destroys `A` for the caller. The right version: build
the augmented matrix as a fresh list of copied rows. Bugs from shared mutation
in a solver are notoriously hard to find, because the first call works and the
second one gives a different answer.

**Mistake 3: reporting "no unique solution" for a rectangular system.** The
wrong version: treating "fewer pivots than columns" as an error. The right
version: an `m Ã— n` system with `m < n` is *underdetermined* and usually has
infinitely many solutions. Only the `0 = nonzero` row means no solution, and for
a square matrix, only a missing pivot means singular.

**Mistake 4: dividing by a pivot without a tolerance check.** The wrong version:
`1.0 / M[r][c]` and hope. The right version: test `abs(pivot) > tol` first, and
skip the column if it fails, because a small pivot means the column is free, not
that the matrix is broken. Choosing `tol` sensibly is the subject of Part 10,
lesson 121.

**Mistake 5: computing `inv(A) @ b` instead of solving.** The wrong version:
`x = np.linalg.inv(A).dot(b)`. The right version: `x = np.linalg.solve(A, b)`.
The inverse is strictly more work and strictly less accurate, because it
computes all `nÂ²` entries when you needed one answer. This is the most repeated
advice in numerical linear algebra.

---

## Formula Sheet

Every symbol and formula this lesson introduces. `A` is `m Ã— n`, `x âˆˆ Fâ¿`,
`b âˆˆ F^m`; `a_ij` is row `i`, column `j`; `[A | b]` is the `m Ã— (n+1)` augmented
matrix, whose last column index is `n`; `U` is an upper-triangular matrix with
zeros below the diagonal; `tol` is a tolerance for "is this zero"; `u` is the
machine unit roundoff.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `Ax = b` | `Î£_j a_ij x_j = b_i` for `i = 1â€¦m` | One equation per row, one unknown per column. The universal form of "linked measurements". | Every linear system |
| `[A | b]` | `m Ã— (n+1)`, `A` with `b` stacked as an extra column | Write `b` down once and treat everything as one matrix. Index of `b` is column `n`. | Every elimination step |
| Row operations | (i) swap rows; (ii) multiply a row by `c â‰  0`; (iii) `R_i â† R_i + c R_j` | The only moves allowed. (ii) with `c = 0` is forbidden â€” it would lose a row. | The whole algorithm |
| Row-equivalence | `A x = b` and `A' x = b'` have the same solutions iff `A' = E A`, `b' = E b` for invertible `E` | Row operations change the *look* of a system, never its answers. | Why reduction is legitimate |
| Row echelon form (REF) | (i) every nonzero row's leftmost nonzero sits strictly right of the one above; (ii) zero rows at the bottom | Staircase shape. **No requirement** that the pivots be `1` or that above be zero. | Output of forward elimination |
| Reduced REF (RREF) | REF **plus** every leading entry is `1` and is the only nonzero in its column | Fully normalised. The solution, if there is one, is visible without any substitution. | Diagnosis of all three cases |
| Pivot | `a_kk` at step `k` (or the swapped-in entry) | The nonzero used as the divisor. | Every step of elimination |
| Multiplier | `m_ik = a_ik / a_kk` | How much of the pivot row to subtract. Always `|m_ik| â‰¤ 1` under partial pivoting, which is the point. | Each row update |
| Back substitution | `x_n = b_n / a_nn`, then `x_i = (b_i - Î£_{j>i} a_ij x_j) / a_ii` for `i = n-1 â€¦ 1` | Solve from the bottom up, one unknown per row. | After elimination |
| Partial pivoting rule | pick `r â‰¥ k` maximising `\|a_rk\|`, then `R_k â†” R_r` | Always divide by the biggest available number in the column. | **Every** floating-point solve |
| No-pivoting rule | pivot is `a_kk`, whatever it is | Fast in exact arithmetic; unsafe in floating point. | Textbook proofs only |
| Growth factor | `g = max\|U_ij\| / max\|A_ij\|` | How much elimination magnifies entries. `g = 1` means no amplification. | Detecting an unstable run |
| Growth bound, pivoted | `g â‰¤ 2^(n-1)`, typically `â‰ˆ 1` | Entries can at most double per step. Error per entry `â‰¤ nÂ·u`. | Justifies pivoting |
| Growth bound, unpivoted | `g` **unbounded** in `n` | Can grow like `2^(n-1)` or worse; the answer is then garbage. | Why production solvers pivot |
| Backward stability | `P A + Î”A = L U` with `â€–Î”Aâ€– â‰¤ 3nÂ·uÂ·â€–Aâ€–`, `â€–Pâ€– = â€–Pâ»Â¹â€– = 1` | The computed factors are exact for a matrix within rounding of `A`. | The formal guarantee |
| `[0 â€¦ 0 \| c]`, `c â‰  0` | the row means `0 = c` | **Contradiction.** No solution exists. | Diagnosing "no solution" |
| `[0 â€¦ 0 \| 0]` | the row means `0 = 0` | Redundant equation. Says nothing, so it is harmless. | Diagnosing "not a contradiction" |
| Pivot count test | `pivots == n` âŸ¹ unique; `pivots < n` âŸ¹ a free variable | One parameter per free variable, so infinitely many. | The one-line classification |
| Free variable | a column with no pivot | Set it to `t âˆˆ F`; every pivot variable is then determined by `t`. | Describing the solution set |
| Particular solution | `x_p` from setting all free variables to `0` | One point of the solution set. Any other is `x_p` plus null directions. | Reporting "infinite" answers |
| Null direction | `v` from setting one free variable to `1`, others to `0` | `A v = 0`. Moves along the solution set without leaving it. | Describing the solution set |
| Full solution set | `x = x_p + tâ‚vâ‚ + â€¦ + t_k v_k`, `t_i âˆˆ F` | A particular point plus a span of directions. | The complete answer for a singular system |
| LU factorisation | `P A = L U`, `L` unit lower triangular, `U` upper triangular | One expensive factorisation, many cheap solves. `L` has `1`s on the diagonal, so forward substitution is immediate. | Repeated right-hand sides |
| Two-stage solve | `L y = P b` then `U x = y` | Substitute `A = Pâ»Â¹LU` into `Ax = b` and multiply by `P`. | Implementing `lu_solve` |
| Solve cost | `Î˜(nÂ²)` forward, `Î˜(nÂ²)` back | Triangular, not cubic. | Why factor-then-solve wins |
| Factor-then-solve-`k` | `Î˜(nÂ³ + k nÂ²)` | The `O(nÂ³)` is paid once. | Many right-hand sides, e.g. PageRank iterations |
| Elimination cost | `Î£_k (n-k)Â² â‰ˆ nÂ³/3` | At step `k`, `n-k` rows each touching `n-k` entries. | Complexity statements |
| Back substitution cost | `nÂ²/2` | Dominated by elimination. | Complexity statements |
| Pivoting overhead | `O(n)` per step, `O(nÂ²)` total | One pass over a column to find the max. Negligible against `nÂ³`. | Cost-benefit of pivoting |
| `n = 10â´` | `nÂ³/3 â‰ˆ 3 Ã— 10Â¹Â¹` multiply-adds | Why a dense solve is hopeless at that size. | Choosing an algorithm |
| Banded solve | `O(n Â· kÂ²)` for `k` nonzeros per row | Structure beats density. | Tridiagonal PDE and mesh systems |
| Banded storage | `ab[u + i - j, j] = a_ij`; `3n` numbers for bandwidth 1 | `scipy.linalg.solve_banded` convention. | Banded systems |
| Iterative refinement | `r = b - A x`, then `x â† x + solve(A, r)`, repeat | Uses the residual as a *direction*, not a test. Costs `O(nÂ²)` per step, not `O(nÂ³)`. | Repairing a badly scaled solve |
| Refinement, why it works | rounding is *backward*; the exact solution of the perturbed system is computed, so the error shrinks | The tiny residual `r` contains the whole error signal. | Mixed-precision solvers |
| `cond(A)` | `â€–Aâ€– Â· â€–Aâ»Â¹â€–`; `Îº = 1` is perfect, `Îº â‰ˆ 10Â¹â¶` is hopeless | Digits lost `â‰ˆ logâ‚â‚€ Îº`. | Deciding whether to trust an answer |
| `solve` vs `inv` | `x = solve(A, b)` costs `O(nÂ³)` once; `x = inv(A) @ b` costs the same but with more rounding | Forming the inverse computes all `nÂ²` entries to use `n` of them. | Never write `inv(A) @ b` |

## Multiple Choice Questions

**Q1.** The augmented matrix of `Ax = b` reduces to a matrix whose last row is
`[0, 0, 0 | 0]`. What does that tell you?

- A) The system has no solution, because one equation reduced to nothing
- B) The system has infinitely many solutions, because an unknown dropped out
- C) The system is consistent, and this row is a redundant equation that
  constrains nothing
- D) The system is singular, which is the same statement as having no solution

<details>
<summary>Answer and explanation</summary>

**C) The system is consistent, and this row is a redundant equation that
constrains nothing.**

The last row reads `0 = 0`, which is true of every assignment of the unknowns. It
therefore removes no candidates and eliminates none â€” it is *redundant*, and
redundancy is harmless. This is the "infinitely many" worked example in the
lesson: with `b = [5, 9, 14]` the RREF is

```
 1  2  |  5
 0  1  | 6/7
 0  0  |  0
```

and the answer is the family `xâ‚€ = 5 - 2t`, `xâ‚ = t`.

- A) confuses `[0 â€¦ 0 | 0]` with `[0 â€¦ 0 | c]`, `c â‰  0`. Those two rows look
  almost identical in a printout and mean opposite things. The lesson's second
  worked example changes exactly one number â€” the last right-hand side from `14`
  to `15` â€” and the bottom row becomes `0 = 1`, which *is* a contradiction. One
  digit flips the entire classification.
- B) is right that an unknown dropped out, but that shows up in the **pivot
  count**, not in this row. Here column 1 had no pivot, and that is a separate
  piece of information. Do not read the verdict off one row when two facts are
  needed.
- D) is a genuine confusion and the lesson addresses it head-on in Mistake 3.
  For a *square* `A`, a missing pivot does mean singular, and singular does
  **not** mean "no solution" â€” it means "no *unique* solution", which is
  normally infinitely many. `A = [[1,2],[2,4]]` and `b = [2, 4]` is a
  consistent, infinitely-many-solutions system whose `A` is very much singular.

</details>

**Q2.** Why does the lesson's `classify` inspect the *last column* of the RREF
before counting pivots?

- A) Because the last column of `[A | b]` is the only one whose values are not
  coefficients of an unknown, so a nonzero there with a zero row to its left is a
  contradiction rather than a free variable
- B) Because the last column is always the largest in absolute value after
  reduction, since pivoting selects for magnitude
- C) Because pivot counts are unreliable for rectangular systems, but the last
  column always is
- D) Because `A` may be rectangular while `b` must have exactly one column

<details>
<summary>Answer and explanation</summary>

**A) Because the last column of `[A | b]` is the only one whose values are not
coefficients of an unknown, so a nonzero there with a zero row to its left is a
contradiction rather than a free variable.**

Every column of `[A | b]` except the last is indexed by an unknown `x_j`. A
column with no pivot in `A` is therefore a *free variable* â€” the solution set
stays consistent and grows a parameter. The last column is different: it holds
the right-hand sides, which are data, not unknowns. A row that is all zeros there
is asserting `0 = b_i'`, which is either trivially true (`b_i' = 0`, redundant)
or false (`b_i' â‰  0`, no solution). No other column can carry that meaning, which
is exactly why the check comes first: it can override the pivot count.

- B) is false on both counts. Nothing in the algorithm makes the last column
  large â€” in the code's case 2, `b = [5, 4, 10]` and the final RREF reads
  `[[1,0,2],[0,1,2],[0,0,-1]]`, where `-1` is not a maximum of anything. And
  partial pivoting searches a *column for its own max*; it never compares across
  columns.
- C) reverses the reliability. Pivot counting is exactly what handles the
  rectangular case â€” `m < n` is underdetermined *by* the pivot count. The last
  column is the robust test, because `0 = nonzero` is unambiguous in any shape.
- D) is a garbled version of a true statement: `b` is always a single column
  vector of length `m`, which is why it can be stacked as column `n` of the
  augmented matrix. That tells you about the *layout*, not about the
  classification.

</details>

**Q3.** Under partial pivoting, why is the multiplier `m_ik = a_ik / a_kk`
guaranteed to satisfy `|m_ik| â‰¤ 1`?

- A) Because the pivot is the diagonal entry, and diagonal entries dominate
  off-diagonal ones
- B) Because the pivot was chosen as the largest absolute value in its column at
  or below the pivot row, so no other candidate in that range exceeds it
- C) Because row operations are chosen to preserve the solution set, and that
  forces the multipliers to be small
- D) Because the matrix is normalised so every entry has absolute value at most 1

<details>
<summary>Answer and explanation</summary>

**B) Because the pivot was chosen as the largest absolute value in its column at
or below the pivot row, so no other candidate in that range exceeds it.**

`|m_ik| = |a_ik| / |a_kk|`, and partial pivoting sets `a_kk` to the maximum of
`|a_rk|` over all `r â‰¥ k`. Since row `i â‰¥ k` is in that range, `|a_ik| â‰¤ |a_kk|`,
hence `|m_ik| â‰¤ 1`. This is the mechanism behind the whole stability story: the
row update `R_i â† R_i - m_ik R_k` subtracts at most as much as it is removing,
so entries *shrink* rather than grow. That is why the pivoted run in the lesson
has growth factor `1.0` while the unpivoted run reaches `9.9999999998e+07`.

- A) is not a property of matrices. Diagonal entries are routinely smaller than
  off-diagonal ones â€” the pivoting example is built on
  `A = [[1e-11, 1],[1, 1+1e-11]]`, where the diagonal entry `1e-11` is ten
  orders of magnitude *smaller* than the off-diagonal `1`.
- C) confuses two different things. Solution-set preservation says row
  operations are *legal*; it says nothing about their magnitude. You could add
  `10^12` times one row to another and preserve the solutions perfectly while
  destroying every digit.
- D) is a technique, not a property. No normalisation is applied; Part 10,
  lesson 121 is where rescaling would be discussed. A matrix with entries of
  size `10^9` behaves identically in relative terms.

</details>

**Q4.** In the pivoting example, `A = [[1e-11, 1],[1, 1+1e-11]]` with
`b = [1, 1]`. Elimination *without* pivoting returns `x = [0.0, 1.0]` while the
exact answer is `[-1e-11, 1.0]`. Why is a residual check unable to catch this?

- A) Because the residual is computed in single precision and loses the
  difference
- B) Because `1.00000000001 - 1.0` rounds to `1e-11` exactly in binary floating
  point, so the subtraction is fine
- C) Because the matrix is nearly singular, so a whole family of `x` values
  reproduce `b` to within rounding, and the wrong one is on that family â€” giving
  a residual of exactly `0.000e+00`
- D) Because the residual is `â€–Aâ€–Â·â€–xâ€–` and both factors are rounded

<details>
<summary>Answer and explanation</summary>

**C) Because the matrix is nearly singular, so a whole family of `x` values
reproduce `b` to within rounding, and the wrong one is on that family â€” giving
a residual of exactly `0.000e+00`.**

The lesson prints it: `residual of the wrong answer: 0.000e+00`, while the
relative error in `xâ‚€` is `1.000e-11` â€” the *entire* answer. The mechanism is
that `cond(A) â‰ˆ 2.6` is not the problem; the problem is that `xâ‚€` itself is
`1e-11`, so "exactly zero" and "off by `1e-11`" are the same thing at double
precision. `â€–Aâ»Â¹â€–` is enormous in the direction that matters, so the map from
`b` to `x` amplifies the `1e-16`-level rounding of `b` into a `100%` error in
`xâ‚€`.

- A) is wrong: everything is double precision, and the issue is not precision
  but *scaling*. In single precision it would be far worse, not better.
- B) is the arithmetic detail that explains the damage, but it has the claim
  backwards. `1.00000000001 - 1.0` does not represent `1e-11`; the
  catastrophic part is that the *eliminated entry* is a difference of two numbers
  of size `1` whose true value is `1e-11`, so relative rounding error of `1e-16`
  becomes absolute error of `1e-16` on a quantity that should be `1e-11` â€” a
  `1e-5` relative error, and the lesson's intermediate entry is `-9.9999999999e+10`,
  having been amplified by the `1e11` multiplier.
- D) describes a formula nobody uses. The residual is `b - A x`, computed with
  three matvec entries, and it is not the issue.

</details>

**Q5.** You have factorised `A` once and now need to solve `A x = b` for 1000
different right-hand sides. What should you do?

- A) Call `np.linalg.solve(A, b)` 1000 times, since it is the documented way
- B) Call `np.linalg.inv(A)` once and multiply, since one inverse beats 1000
  factorisations
- C) Keep the `L`, `U` and permutation, and do two triangular solves per
  right-hand side
- D) Row reduce `A` once to RREF and reuse that, since RREF is canonical

<details>
<summary>Answer and explanation</summary>

**C) Keep the `L`, `U` and permutation, and do two triangular solves per
right-hand side.**

The cost accounting is `Î˜(nÂ³ + k nÂ²)` for `k` right-hand sides against
`Î˜(k nÂ³)` if you refactorise. At `n = 1000` and `k = 1000` that is about `10â¹`
versus `2 Ã— 10â¹` multiply-adds â€” and the ratio `k/n` grows without bound. The
lesson's code demonstrates this directly: one `lu_factor` call, then four
`lu_solve` calls, each residual at the `1e-15` level. This is exactly why
`scipy.linalg.lu_factor` and `lu_solve` are separate functions, and why
PageRank-style iterative solvers are built on a reused factorisation.

- A) is correct code and the wrong plan. `np.linalg.solve` refactorises on every
  call, so 1000 calls pay `1000 nÂ³`. It is right for a *single* solve, which is
  the case the lesson is arguing for when it says "never write `inv(A) @ b`" â€”
  the advice is about not forming the inverse, not about reusing factors.
- B) inverts the argument. One inverse is one factorisation plus `Î˜(nÂ³)` more
  work to build the full inverse, and then each multiply is `Î˜(nÂ²)` â€” total
  `Î˜(nÂ³ + k nÂ²)`, numerically the same as C but with strictly worse rounding,
  because the inverse is never formed accurately. So B is the same asymptotic
  cost as C with worse constants and worse accuracy, wrapped in the API the
  lesson tells you not to use.
- D) is a real misconception. RREF *is* canonical, which is its virtue for
  *diagnosis* â€” one pass answers "unique, none, or infinite" â€” but the lesson
  pays for it with the full reduction of **all** rows against **all** pivots,
  which is more work than the LU forward pass. It is a diagnostic tool, not a
  solve kernel.

</details>

**Q6.** `A` is `2 Ã— 3` and `b` is a 2-vector. Which statement must be true?

- A) The system has no solution, because there are more unknowns than equations
- B) The system either has no solution or has infinitely many, never a unique one
- C) The system has a unique solution, provided `A` has rank 2
- D) The system has a unique solution, provided `b` is not the zero vector

<details>
<summary>Answer and explanation</summary>

**B) The system either has no solution or has infinitely many, never a unique
one.**

Three unknowns, two independent equations, so one column of `A` gets no pivot.
The pivot count is therefore at most 2 and can never equal `n = 3`. With no
contradictory row you get a free variable and a one-parameter family; with a
contradictory row you get `0 = c`. Uniqueness is structurally impossible, which
is the `k â‰¤ n` side of the counting argument from
[lesson 30](30_vectors_and_vector_spaces.md). This is Mistake 3: reporting
"no unique solution" as an *error* for a rectangular system is wrong; an
underdetermined system is an ordinary situation, and `np.linalg.lstsq` exists
to answer it.

- A) is a real misconception â€” "more unknowns than equations" sounds like it must
  be unsolvable, but it is the opposite of "impossible". Overdetermination
  (`m > n`) is what risks *no* solution, and even then it usually has one.
  Underdetermination means the answer is not unique, not that there is none.
- C) is the trap. Rank 2 does mean the two rows are independent, so the map
  `â„Â³ â†’ â„Â²` is onto and *some* `b` in the image is reachable â€” but reaching it
  takes infinitely many different `x`. `rank(A) = 2` guarantees at least one
  solution exists for compatible `b`, never that the solution is unique.
- D) is meaningless. Uniqueness depends only on `A` (and the right-hand side
  cannot help it): if `A` has a null vector `v â‰  0` then `x` and `x + v` are
  both solutions whenever either one is. Choosing `b` changes *which* line you
  land on, not whether there is a line.

</details>

**Q7.** When you reduce `[A | b]` to RREF and find every column of `A` carrying a
pivot, what have you learned?

- A) `A` is invertible, and `x` is the last column of the RREF
- B) `A` is invertible, but you still need back substitution to recover `x`
- C) `A` has full row rank, and `x` is the last column of `rref(A)`, which
  excludes `b`
- D) The system is consistent, but you cannot tell whether it is unique without
  computing `det(A)`

<details>
<summary>Answer and explanation</summary>

**A) `A` is invertible, and `x` is the last column of the RREF.**

RREF makes every pivot the only nonzero in its column, so if all `n` columns of
`A` pivot then `rref([A|b])` is `[I | x]` and the answer is sitting in the last
column. The lesson's Case 1 says exactly this â€” "every column is a pivot, so the
answer is unique and is the last column, read straight off the RREF with no back
substitution at all" â€” and the code prints `x = [2.0, 3.0, -1.0]`. Full pivot
coverage is also exactly invertibility, which is the bridge to
[lesson 33](33_determinant_and_inverse.md)'s one-line test.

- B) is true of *echelon* form and false of RREF. In the upper-triangular `U`
  from the worked example, `xâ‚‚` must be read first and substituted upward, which
  is back substitution. RREF is the stronger object: it has already done that
  substitution for you by clearing above the pivots as well as below.
- C) mixes two things. `rref(A)` computed *without* `b` has no `x` in it at all â€”
  it is a statement about `A`. And the relevant statement is full *column* rank
  for an `n Ã— n` matrix; "full row rank" is the right phrase for a rectangular
  system with no solution.
- D) is half-right in an unhelpful way. It is true that you cannot tell
  invertibility from a *determinant* you have not computed, and `det(A) â‰  0` is
  indeed the criterion. But the pivot pattern you already have *is* the test, and
  the lesson says so: "for an `n`-by-`n` `A`, 'unique' is exactly 'A is
  invertible'. Lesson 33 gives a one-line test for that." No `det` required.

</details>

**Q8.** In the worked example, elimination reaches

```
 -3  -1   2  | -11 |
  0   5/3 2/3 | 13/3 |
  0   0   1/5 | -1/5 |
```

What is `(AB)_ij` for this product, and what does the `-1/5` become?

- A) `(AB)_ij = Î£_k a_ik b_kj`, and `-1/5` becomes `xâ‚‚ = -1` after dividing by
  the pivot `1/5`
- B) `(AB)_ij = a_ij b_ij`, and `-1/5` is the answer for `xâ‚‚` because row 2 has
  only one nonzero
- C) `(AB)_ij = Î£_k a_ik b_kj`, and `-1/5` is already `xâ‚‚` because the row is the
  last equation
- D) `(AB)_ij = a_ij + b_ij`, and `-1/5` becomes `xâ‚‚ = -1/5` unchanged

<details>
<summary>Answer and explanation</summary>

**A) `(AB)_ij = Î£_k a_ik b_kj`, and `-1/5` becomes `xâ‚‚ = -1` after dividing by
the pivot `1/5`.**

The last row of an upper-triangular system reads `a_33 xâ‚ƒ = bâ‚ƒ` with nothing
above, so `xâ‚‚ = (-1/5)/(1/5) = -1` immediately. Then
`xâ‚ = (13/3 - (2/3)(-1)) / (5/3) = 3` and `xâ‚€ = (-11 + 3 + 2) / (-3) = 2`,
giving `x = [2, 3, -1]`, which the lesson verifies against all three original
equations. The product formula is the one from
[lesson 31](31_matrices_and_matrix_algebra.md): a row of the left factor dotted
with a column of the right factor.

- B) confuses the matrix product with the Hadamard product, Mistake 1 in that
  lesson and the single most common matrix bug. That is also not what this
  triangle is: the entries here are the coefficients of *equations*, not a
  product of two matrices.
- C) is the subtler distractor, and worth pausing on. `-1/5` is a right-hand
  side, not an unknown, so it cannot be `xâ‚‚` until you divide. Reading a
  coefficient off the wrong side of the augmented bar is exactly the mistake the
  layout is designed to make possible, which is why the lesson's
  `print_system` prints the `=` sign explicitly for every row.
- D) has two errors: addition is not multiplication, and dividing is required.
  It happens to preserve `-1/5`, which is why it is a plausible wrong answer â€”
  but `x = [2, 3, -1]`, and `[2, 3, -1/5]` fails the first equation with
  `4 + 3 + 1/5 = 7.2 â‰  8`.

</details>

**Q9.** The lesson's `forward_elimination` has a `if abs(M[best][col]) <= tol:
continue` branch that skips the column. What does that branch mean, and what
happens if you delete it?

- A) It means the column is a free column. Deleting it makes the routine divide
  by a value indistinguishable from zero and produce enormous multipliers
- B) It means the matrix is singular. Deleting it makes the routine raise, which
  is what the tolerance test is for
- C) It means the entry is exactly zero, so the whole column can be discarded
  from `A`
- D) It means pivoting failed and the routine should restart from the top

<details>
<summary>Answer and explanation</summary>

**A) It means the column is a free column. Deleting it makes the routine divide
by a value indistinguishable from zero and produce enormous multipliers.**

If every entry in column `col` at or below the pivot row is below `tol`, there
is no pivot available, and the column of the *system* is a free variable â€” the
unknown is not determined, which is information, not an error. The guard exists
so the routine never divides by a number that cannot be trusted. Remove it and
`factor = M[r][col] / pivot` uses a pivot like `1e-300`; the resulting multiplier
is astronomical and every surviving entry is destroyed. This is Mistake 4, and
`Exercise 4`'s challenge is `is_singular` written with exactly this guard.

- A's rival B is wrong because a skipped column does **not** mean the matrix is
  singular. A perfectly nonsingular `2 Ã— 2` matrix never skips a column, but a
  `3 Ã— 3` matrix with rank 2 skips one and is not square-singular in the sense
  that matters. The code's Case 3 has rank 2 out of 3 columns, skips column 2,
  and is correctly reported as an infinite-solution system.
- C) is false in an important way: `tol` is a *numerical* threshold, not exact
  zero. An entry of `1e-12` is nonzero in exact arithmetic and the column may
  well be pivotable, but it is below the noise floor, so the routine declines to
  trust it. Discarding the column outright would be a stronger claim than the
  code makes.
- D) is a misreading of the loop. The routine walks columns left to right with
  `pivot_row` advancing monotonically; a skipped column leaves `pivot_row`
  unchanged and the next column is tried in the same position. There is no
  restart.

</details>

**Q10.** The code prints `growth = 1.0` for the pivoted run on
`A = [[1e-11, 1],[1, 1+1e-11]]` and about `1e8` for the unpivoted run. What is
the growth factor measuring, and why does a large value warn you?

- A) How much the entries grow during elimination, relative to the largest
  original entry; large growth means rounding error is being magnified on the
  way
- B) How many times the matrix had to be row-swapped during the run
- C) The ratio of the condition number to the machine epsilon
- D) The fraction of the original entries that were replaced by exact zeros

<details>
<summary>Answer and explanation</summary>

**A) How much the entries grow during elimination, relative to the largest
original entry; large growth means rounding error is being magnified on the
way.**

`g = max|U_ij| / max|A_ij|`, computed by the code as `scale / max_scale` from
the reduced matrix and the original. Its whole purpose is to be a *warning
light*. Every entry carries relative rounding error of order `u â‰ˆ 10â»Â¹â¶`; if
that error is attached to an entry of magnitude `|A|_max` and the entry is then
magnified by `g`, the absolute error reaching `U` is `gÂ·uÂ·|A|_max`. With
`g â‰ˆ 10â¸` the answer's error is `10â»â¸` relative â€” total garbage, which is
precisely what the unpivoted run produced with `xâ‚€ = 0.0`.

- B) is the swap count, which the code returns separately as `swaps` and prints
  as "With partial pivoting (1 row swap)". Swaps are cheap and harmless; it is
  the *magnitude* that matters. A run can have zero swaps and still be unstable.
- C) is a made-up composite. `cond(A) â‰ˆ 2.6` for this matrix and `u â‰ˆ 2.2e-16`
  are both printed elsewhere in the lesson, but the growth factor is a property
  of the *algorithm's output*, not a product of the conditioning and the
  machine. Keeping them separate is the point: pivoting bounds `g` regardless of
  how well or badly conditioned `A` is.
- D) describes sparsity, and it is unrelated. Nothing in `forward_elimination`
  counts how many entries became exactly zero.

</details>

**Q11.** The lesson's `lu_factor` swaps rows of `U` *and* of the already-computed
part of `L`. Why is the second swap necessary?

- A) Because `L` must remain unit lower triangular for `lu_solve`'s forward
  substitution to be valid
- B) Because `perm` must stay in sorted order
- C) Because `U` would otherwise be lower triangular instead of upper
- D) Because the identity `LU = PA` only holds if both factors are permuted

<details>
<summary>Answer and explanation</summary>

**D) Because the identity `LU = PA` only holds if both factors are permuted.**

Swapping rows `k` and `best` of `U` alone changes which *input* row sits in which
position, but the already-computed `L[i][k] = U[i][k]/U[k][k]` entries encode
the multipliers for the *old* row ordering. Swapping the corresponding segment
`L[k][0:k]` and `L[best][0:k]` realigns them, and only then does
`L U = P A` hold â€” which the code verifies directly: `LU == PA: True` with
`L U = P A = [[-3,-1,2],[-2,1,2],[2,1,-1]]` and `perm = [1, 2, 0]`. Skipping
the `L` swap is the classic Crout bug, and it produces an `L` whose multipliers
no longer match the permuted `U`.

- A) is true as a *consequence* but not as the reason. Unit lower triangularity
  is preserved by any row swap among rows `k..n` acting on the sub-`k` columns
  only, because the diagonal `1`s live in columns `< k` and are untouched. The
  reason for the swap is correctness of the product, and `lu_solve`'s
  requirement is the reason *that* matters.
- B) is not a requirement at all. `perm = [1, 2, 0]` is a cycle, not a sorted
  list, and `lu_solve` consumes it exactly as returned:
  `y = [b[perm[i]] for i in range(n)]`. Sorting it would silently permute `b`
  wrongly.
- C) reverses the roles. `U` is the upper-triangular factor and `L` the lower
  one; a row swap among rows at or below `k` preserves `U`'s upper-triangular
  shape for the same reason as A. The lesson's checks â€”
  `L is lower triangular` and `U is upper triangular` â€” both pass.

</details>

**Q12.** The worked example's second system reduces to

```
 1  2  |  5
 0  1  | 6/7
 0  0  |  0
```

and the lesson concludes `xâ‚€ = 5 - 2t`, `xâ‚ = t`. How does that follow from the
RREF alone?

- A) From the last row, `0 = 0`, which is satisfied by every `t`
- B) From the second row, `xâ‚ = 6/7`, and the first row then forces a range of
  `xâ‚€`
- C) From the second row, `xâ‚ = 6/7` is *particular*; to get the family you
  back-substitute in *echelon* form, where row 1 reads `xâ‚€ + 2xâ‚ = 5`, and set
  `xâ‚ = t` to obtain `xâ‚€ = 5 - 2t`
- D) From the fact that the third equation was a linear combination of the first
  two, so the system has one degree of freedom

<details>
<summary>Answer and explanation</summary>

**C) From the second row, `xâ‚ = 6/7` is *particular*; to get the family you
back-substitute in *echelon* form, where row 1 reads `xâ‚€ + 2xâ‚ = 5`, and set
`xâ‚ = t` to obtain `xâ‚€ = 5 - 2t`.**

This is a genuine slip in the lesson's prose, and the correction matters. With
**every** column pivoted in RREF, `xâ‚` is *not* a free variable â€” it is pinned at
`6/7`, and `xâ‚€` at `5 - 2(6/7) = 23/7 â‰ˆ 3.2857`. The unique solution is
`x = [23/7, 6/7]`. The family `xâ‚€ = 5 - 2t, xâ‚ = t` is the answer for the
**echelon** system

```
 1  2  |  5
 0 -7  | -6
 0  0  |  0
```

where column 1 has no pivot, and you read `xâ‚` off the `t` you chose. The lesson
correctly says "column 1 has no pivot â€” it is a free variable" *before* it
displays the RREF, and then displays the RREF, which changes that conclusion.

- A) is right about the last row and wrong about the source of the family. The
  `0 = 0` row tells you the third equation is redundant, i.e. that the system has
  a *one*-parameter family rather than being determined â€” it does not give you
  the parameterisation.
- B) is a plausible reading of the RREF and it is exactly the trap: if you accept
  it, you conclude the solution set is the single point `[23/7, 6/7]`, i.e. that
  the system is uniquely solvable. It is not â€” the *coefficient* matrix has rank
  2 in a 2-column system only because the third equation is redundant, and
  redundancy is not determination.
- D) is a true observation with a false conclusion attached. Yes, the third
  equation is `row 0 + row 1` on both sides (`(1+3, 2-1) = (4, 1)` and
  `5 + 9 = 14`), and yes there is one degree of freedom. But "one degree of
  freedom" is a statement about the *original* `3 Ã— 2` system, and RREF
  deliberately erases the redundancy â€” it cannot tell you how many equations
  were redundant, only how many unknowns are determined. This is exactly the
  distinction the code's Case 3 gets right: there column 2 genuinely has no
  pivot, and the code prints `free column(s): [2]`, `x_p = [3.5714, 0.7143, 0]`,
  and `null direction v = [-1, 0, 1]`.

</details>

## Subjective Questions

### Short Answer

**Q1. List the three allowed row operations and state the theorem about them.**

<details>
<summary>Model answer</summary>

The three row operations are: (1) swap two rows; (2) multiply a row by a nonzero
scalar; (3) add a multiple of one row to another.

The theorem: row operations preserve the solution set of `Ax = b`. Each one
corresponds to something harmless at the level of equations â€” reordering,
rescaling an equation by a nonzero constant, or combining two equations. The
converse also holds: two systems with the same solution set can be connected by a
sequence of row operations, so row operations classify systems completely. Note
that operation (2) requires the scalar to be **nonzero**; scaling a row by `0`
discards an equation and can change the solution set.

</details>

**Q2. State the difference between row echelon form and reduced row echelon form,
and give the shape of each.**

<details>
<summary>Model answer</summary>

**Row echelon form (REF)** requires only: (i) every nonzero row has its leftmost
nonzero entry strictly to the right of the one above it, and (ii) all zero rows
sit at the bottom. Nothing is required about the *values* of the pivots or about
what is above them. Its shape is a staircase: `[[*,*,*],[0,*,*],[0,0,*]]`.

**Reduced row echelon form (RREF)** adds: each leading entry is `1`, **and** it
is the only nonzero in its column. Its shape is the identity block: `[[1,*,*],
[0,1,*],[0,0,1]]` for a full-rank square case, with zeros below the pivots (REF)
*and* above them (RREF). The extra cost is eliminating each pivot column against
**every** other row rather than only the rows below.

REF is what forward elimination produces and needs back substitution. RREF is
what the diagnosis uses, and needs no substitution at all â€” the solution is the
last column.

</details>

**Q3. State the existence-and-uniqueness theorem in terms of the RREF, and say
what each of the three cases looks like.**

<details>
<summary>Model answer</summary>

Reduce `[A | b]` to RREF. Then exactly one of these holds:

- **No solution.** Some row is `[0 â€¦ 0 | c]` with `c â‰  0`. It reads `0 = c`,
  which is false, so no assignment satisfies everything.
- **Infinitely many solutions.** No such row, but some column of `A` has no
  pivot. That column is a free variable; each free variable contributes one
  parameter, and a parameter means infinitely many points.
- **Unique solution.** Neither of the above: every column of `A` is a pivot. The
  solution is then read directly off the last column of the RREF, with no back
  substitution.

The order of the tests is not arbitrary. The contradiction test comes **first**
because it overrides the pivot count: a system with a `0 = c` row has no solution
no matter how many pivots it has. Case 3 in the code is the shape of the middle
case: `A = [[1,2,1],[3,-1,3],[4,1,4]]`, `b = [5,10,15]`, two pivots in three
columns, `x_p = [3.5714, 0.7143, 0]` and `v = [-1, 0, 1]`.

</details>

**Q4. What is a pivot, and what is a multiplier? Give both in terms of the
step-`k` entry of the augmented matrix.**

<details>
<summary>Model answer</summary>

The **pivot** of step `k` is the entry used as the divisor for that column. Under
partial pivoting it is the largest absolute value in column `k` among rows `k`
through `m - 1`, after any needed row swap. Under plain Gaussian elimination it
is simply `a_kk`, whatever that happens to be.

The **multiplier** is `m_ik = a_ik / a_kk` for each row `i > k` â€” the factor by
which the pivot row is scaled before being subtracted from row `i`. The row
update is `R_i â† R_i - m_ik R_k`.

The reason the multiplier deserves a name: it is precisely the quantity that
partial pivoting controls. Because the pivot is the maximum in the column, every
multiplier satisfies `|m_ik| â‰¤ 1`, so the update subtracts at most as much as it
removes and entries shrink rather than grow. In the worked example the two
multipliers for column 0 are `2/(-3) = -2/3` and `(-2)/(-3) = 2/3`, both of
magnitude below 1.

</details>

**Q5. Define the growth factor and state what partial pivoting guarantees about
it.**

<details>
<summary>Model answer</summary>

The **growth factor** is `g = max|U_ij| / max|A_ij|`, where `U` is the
upper-triangular result of elimination and the denominator is the largest
absolute entry of the original matrix. It measures how much elimination
*magnifies* entries.

Partial pivoting guarantees `g â‰¤ 2^(n-1)`, and in practice `g` is close to 1
because each multiplier is at most 1 in magnitude, so each step can at most
double the largest entry. Unpivoted elimination has no such bound: `g` can be
arbitrarily large in `n`, and the lesson's `2 Ã— 2` example produces
`g â‰ˆ 10â¸` on a matrix whose largest entry is `1`.

The diagnostic value is that `g` is computable after the fact, so a solver can
report a stability warning without any theoretical argument. That is why the code
returns it alongside the reduced matrix.

</details>

**Q6. State the LU factorisation and the cost of the factor-then-solve-`k`
loop. Why do libraries expose the factors separately?**

<details>
<summary>Model answer</summary>

The **LU factorisation** of an invertible `A` is `P A = L U`, where `L` is lower
triangular with `1`s on the diagonal, `U` is upper triangular, and `P` is the
product of the row swaps. (`P` is absent in the no-pivot case: `A = LU`.)

The cost: elimination is `Î˜(nÂ³)` and each triangular solve is `Î˜(nÂ²)`, so `k`
right-hand sides cost `Î˜(nÂ³ + k nÂ²)`. Refactorising for each solve would cost
`Î˜(k nÂ³)`. The saving is real and grows with `k`.

Libraries expose the factors separately (`scipy.linalg.lu_factor` returns a
packed `(L, U)` and an `ipiv` record; `lu_solve` consumes them) because the
expensive step is the `O(nÂ³)` factorisation and it is *input-independent* â€” it
does not depend on `b` at all. A loop over many right-hand sides, a Monte Carlo
propagation, or a PageRank-style fixed-point iteration, all share one `A` and
differ only in `b`, so they should share one factorisation. The lesson's code
does exactly this: one `lu_factor`, then four `lu_solve` calls, all residuals at
the `1e-15` level.

</details>

### Long Answer

**Q1. Why does row reduction need pivoting for numerical stability? What
specifically goes wrong, and why doesn't the residual catch it?**

<details>
<summary>Model answer</summary>

**What goes wrong.** The row update is `R_i â† R_i - m_ik R_k` with
`m_ik = a_ik / a_kk`. Every entry of `R_k` carries relative rounding error of
order `u â‰ˆ 10â»Â¹â¶`. The subtraction can only be as accurate as the *larger* of
the two terms. So if `a_kk` is tiny and `a_ik` is of size 1, then `m_ik â‰ˆ 1/a_kk`
is huge, and the intermediate entries `a_ij - m_ik a_kj` are differences of large
numbers whose result is small. The absolute error stays at `u Â· m_ik Â· |a_kj|`,
which is enormous relative to the quantity being computed. The lesson's
`2 Ã— 2` case makes this vivid: pivoting on `a_00 = 1e-11` gives
`m_10 = 1e11` and the single surviving row entry becomes `-99999999999.0`,
against a true value of about `1e-11`.

**Why pivoting fixes it.** Partial pivoting chooses the largest `|a_rk|` in the
column as the pivot, which forces `|m_ik| â‰¤ 1` for every multiplier. The
subtraction then removes at most as much magnitude as it started with, entries
shrink rather than grow, and the formal statement is the growth bound
`g â‰¤ 2^(n-1)`, giving backward stability `â€–Î”Aâ€– â‰¤ 3nÂ·uÂ·â€–Aâ€–` with `â€–Pâ€– = 1`. The
code measures this directly: `growth = 1.0` pivoted versus about `1e8`
unpivoted, a factor of `10â¸` in the error being carried.

**Why the residual does not catch it.** This is the part worth understanding,
because it is why a residual check is not a correctness proof. The lesson's
output is stark: `no pivot = [0.0, 1.0]`, `relative error 1.000e-11`,
`residual of the wrong answer: 0.000e+00`. The `xâ‚€` component is *entirely
wrong* â€” the true value is `-1e-11` and we report `0.0` â€” and the residual is
exactly zero.

The reason is that the error is not in `A` or `b`; it is in `x`, and it is an
error in the *direction that `A` cannot see*. The matrix is nearly singular: its
two columns are nearly proportional, so there is a near-null vector `v` with
`A v â‰ˆ 0`. If `x` is wrong by `Î´` where `Î´` is nearly parallel to `v`, then
`A Î´ â‰ˆ 0` and `A(x + Î´) â‰ˆ A x`, so the residual barely moves. Here `xâ‚€` is of
magnitude `1e-11` while `xâ‚` is `1.0`; an error of `1e-11` in `xâ‚€` is a `100%`
error in that component, but it is a `1e-11` change to `A x`, which is below the
noise floor of the computation. "Residual zero" and "answer completely wrong" are
compatible, and they are compatible precisely when the matrix is ill-conditioned
for that direction.

**What to do instead.** Do not trust the residual; trust the conditioning. Check
`np.linalg.cond(A)` before believing a solve (the lesson prints
`cond â‰ˆ 2.6` for the example and warns that an enormous `x` is the signature).
Scale the rows of `A` so no row is dwarfed by another, and scale the columns so
no column is dwarfed â€” pivoting cannot rescue a badly scaled matrix. And if the
residual *is* suspiciously small, use it as information rather than as
exoneration: iterative refinement, `r = b - A x` then `x â† x + solve(A, r)`,
reuses the factorisation at `O(nÂ²)` per step and repairs the answer, because the
tiny residual is precisely where the error signal lives. The lesson's refinement
block shows the error dropping from `1.0` relative to `8.3e-19`.

</details>

**Q2. Why is a row `[0 â€¦ 0 | c]` with `c â‰  0` the whole diagnosis for "no
solution", and what would break if you tried to decide consistency by counting
pivots alone?**

<details>
<summary>Model answer</summary>

**The diagnosis is complete because of a theorem about rank.** Reduce `[A | b]` to
RREF. Every row operation is invertible, so the reduced system
`rref(A) x = rref(b)` has exactly the same solutions as the original. Now write
`R = rref(A)`. A row of `rref([A|b])` of the form `[0 â€¦ 0 | c]` is a row of `R`
equal to zero, and it exists precisely when the *augmented* matrix
`[A | b]` has larger rank than `A` alone: `rank([A|b]) > rank(A)`.

That is the classical consistency criterion, and it is a one-line consequence of
a dimension count. If `b` were in the column space of `A`, then `Ax = b` would
have a solution and `b` would be a combination of `A`'s columns, so appending `b`
to `A` could not add rank. Therefore:

- `rank(A) = rank([A|b])` âŸº consistent;
- `rank(A) < rank([A|b])` âŸ¹ inconsistent.

Row reduction computes both ranks simultaneously and displays the comparison as
a single row. `[0 â€¦ 0 | 0]` is a zero row on both sides â€” redundant equation.
`[0 â€¦ 0 | c]`, `c â‰  0` is a zero row on the left and not on the right â€” and that
is the *only* way inconsistency can manifest, because everything else in the
matrix has been arranged into `1`s on pivots. So the diagnosis needs one
inspection of one row.

**What breaks if you count pivots alone.** You conflate two independent facts.
Consider the lesson's Case 3: `A = [[1,2,1],[3,-1,3],[4,1,4]]`, `b = [5,10,15]`.
There are 2 pivots in 3 columns â€” a free variable â€” so a pivot-only rule says
"infinitely many". Correct. Now change one number: `b = [5, 4, 10]` with
`A = [[1,2],[3,-1],[4,1]]`. There are still 2 pivots in 2 columns, so a
pivot-only rule now says "unique". Wrong â€” the RREF's last row is `[0, 0 | -1]`,
the equation `0 = -1`, and there is no solution at all.

The failure mode is that "fewer pivots than columns" and "pivots equal columns"
are statements about `A`, while consistency is a statement about `A` *and* `b`
together. Collapsing them loses the information. Worse, the error is silent in
the dangerous direction: a pivot-only classifier on the inconsistent system
returns "unique" and hands you a number, whereas the correct answer is that the
number does not exist. This is Mistake 3 in the lesson, and the reason the code
checks the contradiction row *before* the pivot count:

```python
def rref(A, b, tol=1e-9):
    M = [list(A[i]) + [b[i]] for i in range(len(A))]
    rows, cols = len(M), len(M[0])
    pivot_row, pivots = 0, []
    for col in range(cols - 1):
        best = max(range(pivot_row, rows), key=lambda r: abs(M[r][col]))
        if abs(M[best][col]) <= tol:
            continue
        M[pivot_row], M[best] = M[best], M[pivot_row]
        p = M[pivot_row][col]
        M[pivot_row] = [v / p for v in M[pivot_row]]
        for r in range(rows):
            if r != pivot_row and M[r][col] != 0.0:
                f = M[r][col]
                M[r] = [M[r][c] - f * M[pivot_row][c] for c in range(cols)]
        pivots.append(col)
        pivot_row += 1
    return M, pivots


def classify(A, b, tol=1e-9):
    M, pivots = rref(A, b, tol)
    rows, cols = len(M), len(A[0])
    last = cols                            # the index of the b column
    for i in range(rows):
        if all(abs(M[i][j]) <= tol for j in range(cols)):
            if abs(M[i][last]) > tol:
                return "none", M, pivots   # the 0 = nonzero row wins
    if len(pivots) < cols:
        return "infinite", M, pivots
    return "unique", M, pivots


# The order of the two tests is the point: the contradiction check comes first,
# so a system that is both rank-deficient AND inconsistent is reported as having
# no solution rather than as having infinitely many.
print(classify([[1.0, 2.0], [3.0, -1.0], [4.0, 1.0]], [5.0, 4.0, 10.0])[0])    # none
print(classify([[1.0, 2.0, 1.0], [3.0, -1.0, 3.0], [4.0, 1.0, 4.0]],
               [5.0, 10.0, 15.0])[0])                                           # infinite
print(classify([[2.0, 1.0, -1.0], [-3.0, -1.0, 2.0], [-2.0, 1.0, 2.0]],
               [8.0, -11.0, -3.0])[0])                                          # unique
```

There is a second thing a pivot count alone will never tell you, which is *how
many* free variables there are â€” the count `n - len(pivots)` â€” and each one is an
independent parameter, so the solution set is an affine space of dimension
`n - rank(A)`, not a line. The lesson's Case 3 has one free column and prints the
whole family by generating `x_p + t v` for `t âˆˆ {-2, 0, 1.5, 100}`.

</details>

**Q3. Why does `LU` let you solve `k` systems for the price of roughly one, and
what breaks if you form the inverse instead?**

<details>
<summary>Model answer</summary>

**The asymmetry is structural.** The factorisation depends only on `A`. Every
number in `L` is a ratio of entries of `A`; every number in `U` is an entry of `A`
or a combination of them; `P` records row permutations of `A`. Not one of these
depends on `b`. So computing `L, U, P` once and reusing them is not a caching
trick, it is the recognition that a quantity genuinely does not involve the
variable that is changing. The solve, by contrast, is `Î˜(nÂ²)`: forward
substitution for `L y = P b`, then back substitution for `U x = y`. Both are
triangular, so the first unknown of the first equation is determined immediately
and each subsequent one after that.

The accounting is `Î˜(nÂ³ + k nÂ²)` for `k` right-hand sides against `Î˜(k nÂ³)` for
refactorising every time, and the gap widens with `k` because `n` is fixed. The
lesson's code shows one `lu_factor` and four `lu_solve` calls with residuals at
`1e-15`, and its complexity note gives the `Î˜(nÂ³ + knÂ²)` figure explicitly. This
is why `scipy.linalg.lu_factor` and `lu_solve` are separate entry points, and
why iterative algorithms built on a fixed matrix â€” PageRank's power iteration,
a Markov chain's `P^k`, Monte Carlo propagation of many sources â€” are structured
as *factorise once, substitute many*.

**What breaks with the inverse.** Three things, in increasing order of how quietly
they go wrong.

1. **Cost.** `Aâ»Â¹` requires the same `Î˜(nÂ³)` work as the factorisation, so the
   arithmetic count is the same â€” you have not saved anything, you have only
   moved the work. For a single right-hand side the lesson's advice is blunt:
   `x = inv(A) @ b` is "slower and less accurate" than `x = solve(A, b)`, and
   "never write `inv(A) @ b` in real code."

2. **Accuracy.** The inverse is the worst-conditioned quantity associated with a
   matrix. Forming it produces `nÂ²` entries, each carrying accumulated rounding,
   and then you multiply â€” a second `Î˜(nÂ²)` of rounding on top. Solving directly
   never materialises the badly-scaled intermediate. The lesson reports the two
   agreeing on the `3 Ã— 3` example, but the agreement is luck, not a guarantee.

3. **The information you throw away.** `Aâ»Â¹ b` answers one question; `Aâ»Â¹`
   answers `nÂ²`. If you only need `x`, computing the inverse means computing a
   table of answers to `nÂ²` questions in order to read off one of them â€” and
   those `nÂ²` entries are exactly the quantities most contaminated by
   ill-conditioning, so you have paid in accuracy for answers you never read.

The general principle underneath: prefer the operation that computes what you
need. `solve(A, b)` computes one solution; `inv(A) @ b` computes an entire
operator in order to apply it once. The same logic reappears in
[lesson 33](33_determinant_and_inverse.md), where the determinant is introduced
precisely so you can *test* invertibility in `O(nÂ³/3)` multiplications without
forming anything â€” and the `O(nÂ³)` closed form via the adjugate is explicitly
marked as the thing not to compute.

</details>

**Q4. What would break if you tried to solve a least-squares problem with
Gaussian elimination on the normal equations, and when is the direct method
better?**

<details>
<summary>Model answer</summary>

**What breaks: the condition number.** Minimising `â€–Ax - bâ€–` by setting the
gradient to zero gives the normal equations `(Aáµ€A) x = Aáµ€ b`, and this lesson's
algorithm will happily solve them. The problem is what has happened to the
matrix. Two facts combine badly.

First, squaring doubles the logarithm of the condition number:
`Îº(Aáµ€A) = Îº(A)Â²`. Numerically, if `A` is moderately ill-conditioned with
`Îº = 10â¸`, then `Aáµ€A` has `Îº = 10Â¹â¶`, which is at the limit of double precision â€”
`logâ‚â‚€ 10Â¹â¶ = 16` digits are lost, and there are only about 16 to begin with. The
solved `x` is then garbage even though the algorithm reported success and
computed a residual of essentially zero. This is not a hypothetical: the lesson's
pivoting example is exactly a case where a small residual accompanies a
completely wrong answer, and forming `Aáµ€A` makes the conditioning dramatically
worse before you even start.

Second, `Aáµ€A` destroys sparsity structure. If `A` is banded with bandwidth `b`,
`Aáµ€A` is banded with bandwidth `2b` â€” a constant-factor loss that is tolerable â€”
but if `A` is **sparse with an irregular pattern**, `Aáµ€A` can be *dense*. The
nonzeros of column `j` and column `k` land in entry `(j, k)`, so a column with `k`
nonzeros interacts with every other such column. For a large sparse problem, the
`O(nÂ·kÂ²)` banded solve the lesson recommends at `n = 10â´` becomes a full
`O(nÂ³)` dense solve, and the whole point of the sparse formulation is lost. This
is the standard reason CG, MINRES, and LSQR exist: they never form `Aáµ€A` at all.

There is also an accuracy point about squaring. Forming `Aáµ€A` rounds `nÂ²` entries
and then rounds again when solving; a QR-based method forms the triangular factor
of `A` itself, so the squaring never happens.

**When the direct method is better.** QR on `A` directly, minimising `â€–Ax-bâ€–` in
`O(mnÂ²)` rather than `O(mnÂ² + nÂ³)` for the normal equations, and with
`Îº` unchanged rather than squared. That is why `np.linalg.lstsq` uses a
least-squares routine that does not build the normal equations, and why
[lesson 38](38_orthogonality_and_least_squares.md) develops the orthogonal
machinery.

**When the normal equations are fine.** When the problem is small and
well-conditioned, and especially when you want to reuse the system. If you are
solving the *same* `(Aáµ€A)` for many right-hand sides `Aáµ€báµ¢`, the `Î˜(nÂ³ + k nÂ²)`
argument from Q3 applies with full force: factorise `Aáµ€A` once, then two
triangular solves per `báµ¢`, and nothing is lost. This is standard in
regularised regression, where the "ridge" term `(Aáµ€A + Î»I)` is *added* â€” and
`I` is diagonal, so it costs `O(n)` to apply and does not densify anything. The
lesson's banded block makes the same structural point: a matrix with `k`
nonzeros per row costs `O(n kÂ²)`, and a diagonal or banded perturbation preserves
that.

**The practical rule.** Check `np.linalg.cond(A)` first, not `cond(Aáµ€A)`. If the
conditioning is moderate, the normal equations are fine and cheapest to
implement. If it is large, use QR or an iterative method. And when the answer you
get has a suspiciously small residual, treat that as evidence of a
near-singularity rather than as a success.

</details>

## Exercises and Solutions

**[ ] Exercise 1 â€” solve a 4Ã—4 system by hand.** Solve

    2xâ‚€ +  xâ‚ +  xâ‚‚ -  xâ‚ƒ =  4
     xâ‚€ -  xâ‚ + 2xâ‚‚       =  5
    3xâ‚€        -  xâ‚‚ +  xâ‚ƒ = 10
    xâ‚€ +  xâ‚ +  xâ‚‚ +  xâ‚ƒ =  6

Show the augmented matrix after each pivot step, then verify by substitution.
Check your answer against `numpy.linalg.solve`.

<details>
<summary>Solution</summary>

```python
import numpy as np

A = [[2.0, 1.0, 1.0, -1.0],
     [1.0, -1.0, 2.0, 0.0],
     [3.0, 0.0, -1.0, 1.0],
     [1.0, 1.0, 1.0, 1.0]]
b = [4.0, 5.0, 10.0, 6.0]


def augmented(A, b):
    return [list(A[i]) + [b[i]] for i in range(len(A))]


def forward_elimination(A, b, tol=1e-9):
    M = augmented(A, b)
    rows, cols = len(M), len(M[0])
    pivot_row = 0
    for col in range(cols - 1):
        if pivot_row == rows:
            break
        best = max(range(pivot_row, rows), key=lambda r: abs(M[r][col]))
        if abs(M[best][col]) <= tol:
            continue
        M[pivot_row], M[best] = M[best], M[pivot_row]
        p = M[pivot_row][col]
        for r in range(pivot_row + 1, rows):
            f = M[r][col] / p
            if f == 0.0:
                continue
            for c in range(col, cols):
                M[r][c] -= f * M[pivot_row][c]
        pivot_row += 1
    return M


def back_substitution(U, tol=1e-9):
    n = len(U)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (U[i][n] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
    return x


print("=== Exercise 1: a 4x4 system ===")
for i in range(4):
    print("  | " + " ".join(f"{v:7.3f}" for v in A[i]) + f" | {b[i]:6.2f} |")

M = augmented(A, b)
print("\nstep 0 (input):")
for row in M:
    print("  " + " ".join(f"{v:8.4f}" for v in row))

# Do it step by step so the pivot choices are visible.
pivot_row = 0
for col in range(4):
    best = max(range(pivot_row, 4), key=lambda r: abs(M[r][col]))
    if best != pivot_row:
        M[pivot_row], M[best] = M[best], M[pivot_row]
    p = M[pivot_row][col]
    for r in range(pivot_row + 1, 4):
        f = M[r][col] / p
        if f != 0.0:
            M[r] = [M[r][c] - f * M[pivot_row][c] for c in range(5)]
    pivot_row += 1
    print(f"\nafter pivot in column {col} (pivot {p:.3f}):")
    for row in M:
        print("  " + " ".join(f"{v:8.4f}" for v in row))

x = back_substitution(M)
print(f"\nback substitution: x = {[round(v, 10) for v in x]}")
for i in range(4):
    lhs = sum(A[i][j] * x[j] for j in range(4))
    print(f"  eq {i}: {lhs:.10f} (right side {b[i]:g})  "
          f"{'ok' if abs(lhs - b[i]) < 1e-9 else 'WRONG'}")

ref = np.linalg.solve(np.array(A), np.array(b))
print(f"\nnumpy agrees: {np.allclose(x, ref)}  x = {ref}")
```

Output:

```
=== Exercise 1: a 4x4 system ===
  |   2.000    1.000    1.000   -1.000 |   4.00 |
  |   1.000   -1.000    2.000    0.000 |   5.00 |
  |   3.000    0.000   -1.000    1.000 |  10.00 |
  |   1.000    1.000    1.000    1.000 |   6.00 |
```

Run it and compare the intermediate matrices with your own work; the pivot in
column 0 is the `3` in row 2, not the `2` in row 0, which is the first place
partial pivoting changes your hand answer's intermediate values. The final
answer is identical either way.

</details>

**[ ] Exercise 2 â€” classify three systems.** For each system below, compute the
RREF of the augmented matrix, state the number of pivots, and classify it as
unique, no solution, or infinitely many. Then say *why* in one sentence.

1. `xâ‚€ + xâ‚ = 3`, `xâ‚€ - xâ‚ = 1`, `2xâ‚€ + 2xâ‚ = 6`
2. `xâ‚€ + xâ‚ = 3`, `xâ‚€ - xâ‚ = 1`, `2xâ‚€ + 2xâ‚ = 9`
3. `xâ‚€ + 2xâ‚ = 5`, `3xâ‚€ + 6xâ‚ = 15`

<details>
<summary>Solution</summary>

Systems 1 and 2 differ only in one number on the right-hand side, and that is
enough to move the answer from "unique" to "no solution". System 3 has fewer
independent equations than unknowns, so it has free variables.

```python
def rref(A, b, tol=1e-9):
    """Full reduced row echelon form of the augmented matrix.

    Returns (matrix, pivot_columns) where pivot_columns lists, in order, the
    columns of A that ended up with a pivot.
    """
    rows, cols = len(A), len(A[0])
    M = [list(A[i]) + [b[i]] for i in range(rows)]
    pivot_row = 0
    pivots = []
    for col in range(cols):
        best = None
        for r in range(pivot_row, rows):
            if abs(M[r][col]) > tol:
                best = r
                break
        if best is None:
            continue          # no pivot available, so this column is free
        M[pivot_row], M[best] = M[best], M[pivot_row]
        p = M[pivot_row][col]
        M[pivot_row] = [v / p for v in M[pivot_row]]
        for r in range(rows):
            if r != pivot_row and M[r][col] != 0.0:
                f = M[r][col]
                M[r] = [M[r][c] - f * M[pivot_row][c] for c in range(cols + 1)]
        pivots.append(col)
        pivot_row += 1
    # Adding 0.0 turns -0.0 into 0.0 so the printed matrix has no minus signs
    # on entries that are mathematically zero.
    M = [[v + 0.0 for v in row] for row in M]
    return M, pivots


def classify(A, b, tol=1e-9):
    """Return (kind, rref_matrix, pivot_columns).

    Three outcomes, tested in this order:
      no solution       some row is [0 ... 0 | nonzero]
      infinitely many   fewer pivots than unknowns, no contradiction
      unique            every unknown has a pivot
    """
    M, pivots = rref(A, b, tol)
    cols = len(A[0])
    left = [row[:cols] for row in M]
    rhs = [row[cols] for row in M]

    if any(all(abs(v) <= tol for v in left[i]) and abs(rhs[i]) > tol
           for i in range(len(M))):
        return "no solution", M, pivots
    if len(pivots) < cols:
        return "infinitely many", M, pivots
    return "unique", M, pivots


systems = [
    ("1", [[1.0, 1.0], [1.0, -1.0], [2.0, 2.0]], [3.0, 1.0, 6.0]),
    ("2", [[1.0, 1.0], [1.0, -1.0], [2.0, 2.0]], [3.0, 1.0, 9.0]),
    ("3", [[1.0, 2.0], [3.0, 6.0]], [5.0, 15.0]),
]

for label, A, b in systems:
    cols = len(A[0])
    kind, M, pivots = classify(A, b)
    free = [j for j in range(cols) if j not in pivots]
    print(f"=== System {label}: {kind} ===")
    print(f"  {len(A)} equations, {cols} unknowns, "
          f"pivots in columns {pivots}, free columns {free}")
    for row in M:
        print("  " + " ".join(f"{v:8.4f}" for v in row))

    if kind == "unique":
        x = [0.0] * cols
        for i, pc in enumerate(pivots):
            x[pc] = M[i][cols]
        residuals = [round(sum(A[i][j] * x[j] for j in range(cols)) - b[i], 12)
                     for i in range(len(A))]
        print(f"  x = {[round(v, 6) for v in x]}   residuals {residuals}")
    elif kind == "no solution":
        print(f"  the last row reads 0 = {M[-1][cols]:.4f}, which is false")
    else:
        print("  the family of solutions is x0 = 5 - 2*t, x1 = t for any t")
        for t in (0.0, 1.0, -3.5):
            xt = [5.0 - 2.0 * t, t]
            ok = all(abs(sum(A[i][j] * xt[j] for j in range(cols)) - b[i]) < 1e-9
                     for i in range(len(A)))
            print(f"    t = {t:5.1f} -> x = {xt}   satisfies both equations: {ok}")
    print()
```

Output:

```
=== System 1: unique ===
  3 equations, 2 unknowns, pivots in columns [0, 1], free columns []
    1.0000   0.0000   2.0000
    0.0000   1.0000   1.0000
    0.0000   0.0000   0.0000
  x = [2.0, 1.0]   residuals [0.0, 0.0, 0.0]
=== System 2: no solution ===
  3 equations, 2 unknowns, pivots in columns [0, 1], free columns []
    1.0000   0.0000   2.0000
    0.0000   1.0000   1.0000
    0.0000   0.0000   3.0000
  the last row reads 0 = 3.0000, which is false
=== System 3: infinitely many ===
  2 equations, 2 unknowns, pivots in columns [0], free columns [1]
    1.0000   2.0000   5.0000
    0.0000   0.0000   0.0000
  the family of solutions is x0 = 5 - 2*t, x1 = t for any t
    t =   0.0 -> x = [5.0, 0.0]   satisfies both equations: True
    t =   1.0 -> x = [3.0, 1.0]   satisfies both equations: True
    t =  -3.5 -> x = [12.0, -3.5]   satisfies both equations: True
```

In words. System 1's third equation is exactly twice its first, and `2Â·3 = 6`
matches, so the extra equation is redundant rather than contradictory: two
independent equations in two unknowns, one point. System 2 has the same left
sides with `2xâ‚€ + 2xâ‚ = 9`, and since twice the first equation demands `= 6`,
the RREF ends in `0 = 3`, which is the whole diagnosis. System 3's two equations
are multiples of each other, so only one is independent, and `xâ‚` is
unconstrained except through `xâ‚€ + 2xâ‚ = 5`.

The practical habit this exercise is really about: check the residuals before
trusting a reported solution. The `residuals [0.0, 0.0, 0.0]` line in the output
is a free correctness check, and a classifier you have not verified against
residuals is a classifier you do not yet trust.

</details>

**[ ] Exercise 3 â€” LU, and reusing it.** Implement `lu_factor` (Crout, with
partial pivoting, returning `L`, `U`, `perm` with `P A = L U`) and `lu_solve`.
Verify that `L U` really equals `P A`. Then solve `A x = b` for four different
right-hand sides using a single factorisation, and check each residual.

<details>
<summary>Solution</summary>

```python
def lu_factor(A, tol=1e-9):
    n = len(A)
    U = [list(row) for row in A]
    L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    perm = list(range(n))
    for k in range(n):
        best = max(range(k, n), key=lambda r: abs(U[r][k]))
        if best != k:
            U[k], U[best] = U[best], U[k]
            for j in range(k):
                L[k][j], L[best][j] = L[best][j], L[k][j]
            perm[k], perm[best] = perm[best], perm[k]
        if abs(U[k][k]) <= tol:
            raise ZeroDivisionError("singular matrix")
        for i in range(k + 1, n):
            L[i][k] = U[i][k] / U[k][k]
            for j in range(k, n):
                U[i][j] -= L[i][k] * U[k][j]
    return L, U, perm


def lu_solve(L, U, perm, b):
    n = len(L)
    y = [b[perm[i]] for i in range(n)]
    for i in range(n):
        y[i] -= sum(L[i][j] * y[j] for j in range(i))
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
    return x


A = [[2.0, 1.0, -1.0], [-3.0, -1.0, 2.0], [-2.0, 1.0, 2.0]]
L, U, perm = lu_factor(A)

print("=== Exercise 3: LU factorisation ===")
print("L =\n", [[round(v, 6) for v in row] for row in L])
print("U =\n", [[round(v, 6) for v in row] for row in U])
print("perm =", perm)

PA = [[A[perm[i]][j] for j in range(3)] for i in range(3)]
LU = [[sum(L[i][k] * U[k][j] for k in range(3)) for j in range(3)]
      for i in range(3)]
print("L U =\n", [[round(v, 6) for v in row] for row in LU])
print("P A =\n", PA)
print("LU == PA:",
      all(abs(LU[i][j] - PA[i][j]) < 1e-9 for i in range(3) for j in range(3)))

print("\nFour systems, one factorisation:")
for b in ([8.0, -11.0, -3.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [2.0, 2.0, 2.0]):
    x = lu_solve(L, U, perm, b)
    resid = max(abs(sum(A[i][j] * x[j] for j in range(3)) - b[i]) for i in range(3))
    print(f"  b = {b}  ->  x = {[round(v, 6) for v in x]}  residual {resid:.2e}")
```

Output:

```
=== Exercise 3: LU factorisation ===
L =
 [[1.0, 0.0, 0.0], [0.666667, 1.0, 0.0], [-0.666667, 0.2, 1.0]]
U =
 [[-3.0, -1.0, 2.0], [0.0, 1.666667, 0.666667], [0.0, 0.0, 0.2]]
perm = [1, 2, 0]
L U =
 [[-3.0, -1.0, 2.0], [-2.0, 1.0, 2.0], [2.0, 1.0, -1.0]]
P A =
 [[-3.0, -1.0, 2.0], [-2.0, 1.0, 2.0], [2.0, 1.0, -1.0]]
LU == PA: True
```

</details>

**[ ] Exercise 4 â€” show that pivoting is necessary.** Construct a 2Ã—2 system
where the entry in position `(0,0)` is `1e-11` and the other entries are of size
1. Solve it once without pivoting and once with it, compute the exact answer with
`fractions.Fraction`, and report the relative error of each. Explain in two
sentences why the wrong answer has a tiny residual.

**Challenge.** A square matrix is singular exactly when elimination fails to find
a pivot in some column. Write `is_singular(A)` using only forward elimination and
show that it returns `True` for `[[1, 2], [2, 4]]` and `False` for
`[[1, 2], [3, 4]]`.

<details>
<summary>Solution</summary>

```python
def forward_elimination(A, b, tol, pivot):
    M = [list(A[i]) + [b[i]] for i in range(len(A))]
    rows, cols = len(M), len(M[0])
    pivot_row = 0
    for col in range(cols - 1):
        if pivot_row == rows:
            break
        best = (max(range(pivot_row, rows), key=lambda r: abs(M[r][col]))
                if pivot else pivot_row)
        if abs(M[best][col]) <= tol:
            continue
        M[pivot_row], M[best] = M[best], M[pivot_row]
        p = M[pivot_row][col]
        for r in range(pivot_row + 1, rows):
            f = M[r][col] / p
            if f != 0.0:
                M[r] = [M[r][c] - f * M[pivot_row][c] for c in range(cols)]
        pivot_row += 1
    return M


def back_substitution(U):
    n = len(U)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (U[i][n] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
    return x


print("=== Exercise 4: pivoting is necessary ===")
A = [[1e-11, 1.0], [1.0, 1.0 + 1e-11]]
b = [1.0, 1.0]
print(f"A =\n{A}")

x_bad = back_substitution(forward_elimination(A, b, 0.0, pivot=False))
x_good = back_substitution(forward_elimination(A, b, 1e-9, pivot=True))

from fractions import Fraction as Fr

Ae = [[Fr(1, 10 ** 11), Fr(1)], [Fr(1), Fr(1) + Fr(1, 10 ** 11)]]
be = [Fr(1), Fr(1)]
d = Ae[0][0] * Ae[1][1] - Ae[0][1] * Ae[1][0]
xe = [(be[0] * Ae[1][1] - Ae[0][1] * be[1]) / d,
      (Ae[0][0] * be[1] - be[0] * Ae[1][0]) / d]
print(f"exact x   = {[float(v) for v in xe]}")
print(f"no pivot  = {x_bad}   relative error "
      f"{abs(x_bad[0] - float(xe[0])):.3e}")
print(f"pivoted   = {x_good}   relative error "
      f"{abs(x_good[0] - float(xe[0])):.3e}")
print(f"residual of the wrong answer: {abs(A[0][0] * x_bad[0] + A[0][1] * x_bad[1] - b[0]):.3e}")
print("Explanation: the matrix is nearly singular, so both columns are almost")
print("proportional. Any x that reproduces b well is within rounding distance of")
print("a whole family of correct-looking answers, and the wrong one is on it.")

print()
print("=== Challenge: detecting singularity with elimination only ===")


def is_singular(A, tol=1e-9):
    """True if forward elimination cannot find a pivot in every column."""
    n = len(A)
    M = [list(row) for row in A]
    pivot_row = 0
    for col in range(n):
        best = max(range(pivot_row, n), key=lambda r: abs(M[r][col]))
        if abs(M[best][col]) <= tol:
            return True                      # no pivot for this column
        M[pivot_row], M[best] = M[best], M[pivot_row]
        p = M[pivot_row][col]
        for r in range(pivot_row + 1, n):
            f = M[r][col] / p
            if f != 0.0:
                M[r] = [M[r][c] - f * M[pivot_row][c] for c in range(cols_of(M))]
        pivot_row += 1
    return False


def cols_of(M):
    return len(M[0])


print(f"  [[1, 2], [2, 4]] singular: {is_singular([[1.0, 2.0], [2.0, 4.0]])}")
print(f"  [[1, 2], [3, 4]] singular: {is_singular([[1.0, 2.0], [3.0, 4.0]])}")
print(f"  [[2, 0], [0, 3]] singular: {is_singular([[2.0, 0.0], [0.0, 3.0]])}")
```

Output:

```
=== Exercise 4: pivoting is necessary ===
A =
[[1e-11, 1.0], [1.0, 1.00000000001]]
exact x   = [-1e-11, 1.0]
no pivot  = [0.0, 1.0]   relative error 1.000e-11
pivoted   = [-1.000000082740371e-11, 1.0]   relative error 8.273e-19
residual of the wrong answer: 0.000e+00

=== Challenge: detecting singularity with elimination only ===
  [[1, 2], [2, 4]] singular: True
  [[1, 2], [3, 4]] singular: False
  [[2, 0], [0, 3]] singular: False
```


</details>

**[ ] Exercise 6 â€” the three cases, and what a library does with each.**
Take the three systems the lesson's code uses:

- **Unique.** `A = [[2,1,-1],[-3,-1,2],[-2,1,2]]`, `b = [8,-11,-3]`
- **None.** `A = [[1,2],[3,-1],[4,1]]`, `b = [5,4,10]`
- **Infinite.** `A = [[1,2,1],[3,-1,3],[4,1,4]]`, `b = [5,10,15]`

1. For each, reduce `[A | b]` to RREF, count the pivots, and classify it.
2. For the infinite case, extract a particular solution `x_p` and a null
   direction `v`, and verify `A x_p = b` and `A v = 0` numerically. Then report
   `x = x_p + t v` for `t âˆˆ {-2, 0, 1.5, 100}` and check each one.
3. For the unique case, compute the LU factorisation `P A = L U`, verify `L U`
   reproduces `P A`, and confirm `U` is upper triangular and `L` is lower
   triangular with ones on the diagonal.
4. Report the residual `â€–A x - bâ€–_âˆž` for the LU solves with right-hand sides
   `[8,-11,-3]`, `[1,0,0]`, `[0,1,0]`, and `[2,2,2]`.
5. Hand-check the answer to the unique case in all three original equations.

**Challenge.** Take the infinite-solution case and show that the minimum-norm
point on the solution line `x_p + t v` is the perpendicular foot from the origin,
so it is the value `np.linalg.lstsq` returns. Then take the *none* case and
explain why `np.linalg.lstsq` returns a point at all instead of raising: the
solution set is empty, so what is the returned point, and how would you tell it
apart from a genuine solution if you were handed only the output?

<details>
<summary>Solution</summary>

Parts 1 and 2 by hand. For the **unique** system the pivot columns are `0, 1, 2`
and the RREF is

```
 1  0  0  |  2 |
 0  1  0  |  3 |
 0  0  1  | -1 |
```

so `x = [2, 3, -1]` â€” the last column, no substitution needed.

For the **none** system, `A[2] = A[0] + A[1]` on the left: `(1+3, 2-1) = (4, 1)`,
which is row 2. On the right, `5 + 4 = 9 â‰  10`, so subtracting leaves `0` on the
left and `-1` on the right. RREF:

```
 1  0  |  2 |
 0  1  |  2 |
 0  0  | -1 |
```

The last row is `0 = -1`, which is false. No solution.

For the **infinite** system, `A[2] = A[0] + A[1]` on the left
(`(1+3, 2-1, 1+3) = (4, 1, 4)`) and `5 + 10 = 15` on the right, so row 2 is
redundant. Two pivots in three columns, so column 2 is free:

```
 1  0  0  | 25/7 |
 0  1  0  |  5/7 |
 0  0  0  |  0   |
```

`25/7 â‰ˆ 3.571429` and `5/7 â‰ˆ 0.714286`. Setting the free variable to `0` gives
`x_p = [25/7, 5/7, 0]`. Setting it to `1` and reading off the pivot rows gives
`v = [-1, 0, 1]`: row 0 says `xâ‚€ + xâ‚‚ = 25/7`, so `xâ‚€ = 25/7 - xâ‚‚`, and with
`xâ‚‚ = 1` that is `25/7 - 1 = 18/7`. The code reports the pivot-row form
directly, `direction[pc] = -M3[i][fc]`, which for `pc = 0, fc = 2` gives
`-25/7`. The code's own output prints `null direction v = [-1.0, 0.0, 1.0]`; note
that this vector satisfies `A v = 0` exactly, which is the only property that
matters â€” its scale is arbitrary, and any nonzero multiple is the same direction.

```python
import numpy as np

TOL = 1e-9


def augmented(A, b):
    return [list(A[i]) + [b[i]] for i in range(len(A))]


def rref(A, b, tol=TOL):
    M = augmented(A, b)
    rows, cols = len(M), len(M[0])
    pivot_row, pivots = 0, []
    for col in range(cols - 1):
        if pivot_row == rows:
            break
        best = max(range(pivot_row, rows), key=lambda r: abs(M[r][col]))
        if abs(M[best][col]) <= tol:
            continue
        M[pivot_row], M[best] = M[best], M[pivot_row]
        p = M[pivot_row][col]
        M[pivot_row] = [v / p for v in M[pivot_row]]
        for r in range(rows):
            if r != pivot_row:
                f = M[r][col]
                if f != 0.0:
                    M[r] = [M[r][c] - f * M[pivot_row][c] for c in range(cols)]
        pivots.append(col)
        pivot_row += 1
    return M, pivots


def classify(A, b, tol=TOL):
    M, pivots = rref(A, b, tol)
    ncols = len(A[0])
    for row in M:
        if all(abs(row[j]) <= tol for j in range(ncols)) and abs(row[ncols]) > tol:
            return "none", M, pivots
    if len(pivots) < ncols:
        return "infinite", M, pivots
    return "unique", M, pivots


def matvec(M, v):
    return [sum(M[i][j] * v[j] for j in range(len(M[0]))) for i in range(len(M))]


def lu_factor(A, tol=TOL):
    """Crout LU with partial pivoting. Returns (L, U, perm) with P A = L U."""
    n = len(A)
    U = [list(row) for row in A]
    L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    perm = list(range(n))
    for k in range(n):
        best = max(range(k, n), key=lambda r: abs(U[r][k]))
        if best != k:
            U[k], U[best] = U[best], U[k]
            for j in range(k):
                L[k][j], L[best][j] = L[best][j], L[k][j]
            perm[k], perm[best] = perm[best], perm[k]
        if abs(U[k][k]) <= tol:
            raise ZeroDivisionError("singular matrix")
        for i in range(k + 1, n):
            L[i][k] = U[i][k] / U[k][k]
            for j in range(k, n):
                U[i][j] -= L[i][k] * U[k][j]
    return L, U, perm


def lu_solve(L, U, perm, b):
    n = len(L)
    y = [b[perm[i]] for i in range(n)]
    for i in range(n):
        y[i] -= sum(L[i][j] * y[j] for j in range(i))
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
    return x


def inf_norm(v):
    return max(abs(t) for t in v)


systems = [
    ("unique",   [[2.0, 1.0, -1.0], [-3.0, -1.0, 2.0], [-2.0, 1.0, 2.0]], [8.0, -11.0, -3.0]),
    ("none",     [[1.0, 2.0], [3.0, -1.0], [4.0, 1.0]], [5.0, 4.0, 10.0]),
    ("infinite", [[1.0, 2.0, 1.0], [3.0, -1.0, 3.0], [4.0, 1.0, 4.0]], [5.0, 10.0, 15.0]),
]

print("=== Part 1: RREF, pivot count, classification ===")
for intended, A, b in systems:
    kind, M, pivots = classify(A, b)
    ncols = len(A[0])
    print(f"  intended {intended:9s} -> {kind:9s}  "
          f"{len(pivots)} pivot(s) in {ncols} column(s)")
    for row in M:
        print("     " + " ".join(f"{v:9.4f}" for v in row))
    flag = "ok" if kind == intended else "MISMATCH"
    print(f"     {flag}")
    if kind == "none":
        print(f"     the last row reads 0 = {M[-1][-1]:.4f}, which is false")

print()
print("=== Part 2: particular solution and null direction, infinite case ===")
A_inf = systems[2][1]
b_inf = systems[2][2]
M, pivots = rref(A_inf, b_inf)
ncols = len(A_inf[0])
free = [c for c in range(ncols) if c not in pivots]
particular = [0.0] * ncols
for i, pc in enumerate(pivots):
    particular[pc] = M[i][ncols]
print(f"pivot columns {pivots}, free column(s) {free}")
print(f"x_p = {[round(v, 4) for v in particular]}")
print(f"A x_p = {[round(v, 10) for v in matvec(A_inf, particular)]} (should be b)")

direction = [0.0] * ncols
direction[free[0]] = 1.0
for i, pc in enumerate(pivots):
    direction[pc] = -M[i][free[0]]
print(f"null direction v = {[round(v, 4) for v in direction]}")
print(f"A v = {[round(v, 10) for v in matvec(A_inf, direction)]} (should be all zeros)")
print()
for t in (-2.0, 0.0, 1.5, 100.0):
    xt = [particular[j] + t * direction[j] for j in range(ncols)]
    resid = inf_norm([matvec(A_inf, xt)[i] - b_inf[i] for i in range(len(b_inf))])
    print(f"  t = {t:6.1f} -> x = {[round(v, 4) for v in xt]}   residual {resid:.2e}")

print()
print("=== Part 3: LU of the unique system, and the structural checks ===")
A_u = systems[0][1]
L, U, perm = lu_factor(A_u)
print("L =")
for row in L:
    print("  " + " ".join(f"{v:8.4f}" for v in row))
print("U =")
for row in U:
    print("  " + " ".join(f"{v:8.4f}" for v in row))
print(f"perm = {perm}  (row i of L U is row perm[i] of A)")

n = len(A_u)
PA = [[A_u[perm[i]][j] for j in range(n)] for i in range(n)]
LU = [[sum(L[i][k] * U[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
max_err = max(abs(LU[i][j] - PA[i][j]) for i in range(n) for j in range(n))
print(f"max |L U - P A| = {max_err:.2e}")
print(f"L has a unit diagonal:     {all(abs(L[i][i] - 1.0) < 1e-12 for i in range(n))}")
print(f"L is lower triangular:     {all(L[i][j] == 0.0 for i in range(n) for j in range(i + 1, n))}")
print(f"U is upper triangular:     {all(U[i][j] == 0.0 for i in range(n) for j in range(i))}")

print()
print("=== Part 4: four right-hand sides, one factorisation ===")
for b in ([8.0, -11.0, -3.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [2.0, 2.0, 2.0]):
    x = lu_solve(L, U, perm, b)
    resid = inf_norm([matvec(A_u, x)[i] - b[i] for i in range(n)])
    print(f"  b = {b}  ->  x = {[round(v, 6) for v in x]}   residual {resid:.2e}")

print()
print("=== Part 5: hand-check x = [2, 3, -1] in the three original equations ===")
x = [2.0, 3.0, -1.0]
for i, row in enumerate(A_u):
    terms = " + ".join(f"{row[j]:g}*{x[j]:g}" for j in range(n))
    lhs = matvec(A_u, x)[i]
    print(f"  eq {i}: {terms} = {lhs:g}   right side {b_u if False else systems[0][2][i]:g}"
          f"   {'ok' if abs(lhs - systems[0][2][i]) < 1e-9 else 'WRONG'}")

print()
print("=== Challenge: lstsq on the infinite and the inconsistent case ===")
A3 = np.array(systems[2][1])
b3 = np.array(systems[2][2])
ls, _, rank, sv = np.linalg.lstsq(A3, b3, rcond=None)
xp = np.array(particular)
vdir = np.array(direction)
print(f"infinite case: rank {rank} of {A3.shape[1]} columns")
print(f"lstsq          = {np.round(ls, 6)}")
print(f"||x_p||        = {np.linalg.norm(xp):.6f}")
print(f"||lstsq||      = {np.linalg.norm(ls):.6f}  (smaller: closer to the origin)")

# The perpendicular foot. Minimise |x_p + t v|^2 = |x_p|^2 + 2 t (x_p . v) + t^2 |v|^2,
# whose derivative 2 (x_p . v) + 2 t |v|^2 vanishes at t = -(x_p . v) / |v|^2.
t_star = -float(xp @ vdir) / float(vdir @ vdir)
foot = xp + t_star * vdir
print(f"x_p . v        = {float(xp @ vdir):.6f}")
print(f"t* = -(x_p.v)/(v.v) = {t_star:.6f}")
print(f"foot x_p + t* v = {np.round(foot, 6)}")
print(f"foot equals lstsq:  {np.allclose(foot, ls)}")
print(f"foot . v        = {float(foot @ vdir):.2e}  (perpendicular to the line direction)")
print(f"residual ||A foot - b|| = {np.linalg.norm(A3 @ foot - b3):.2e}")
print("A foot = b exactly, so the foot is a genuine solution AND the closest to")
print("the origin. That is what 'minimum-norm solution' means.")

A2 = np.array(systems[1][1])
b2 = np.array(systems[1][2])
ls2, _, rank2, _ = np.linalg.lstsq(A2, b2, rcond=None)
resid2 = A2 @ ls2 - b2
print()
print(f"inconsistent case: rank {rank2} of {A2.shape[1]} columns")
print(f"lstsq returns  = {np.round(ls2, 6)}   (a point, not an exception)")
print(f"predicted      = {np.round(A2 @ ls2, 6)}")
print(f"target         = {b2}")
print(f"residual       = {np.round(resid2, 6)}")
print(f"||residual||   = {np.linalg.norm(resid2):.6f}")
print("The solution set is EMPTY, so this point is not a solution at all. It is the")
print("closest point of the column space of A to b. You tell the two situations")
print("apart by the residual: zero (to rounding) means every target is reachable,")
print("and a nonzero residual means the target was out of reach and the fit is")
print("approximate. Note the residual here is exactly (1/3, 1/3, -1/3): nonzero,")
print("so the answer is genuinely approximate and no choice of x would have done")
print("better.")
```

Output:

```
=== Part 1: RREF, pivot count, classification ===
  intended unique    -> unique    3 pivot(s) in 3 column(s)
          1.0000   0.0000   0.0000   2.0000
          0.0000   1.0000   0.0000   3.0000
          0.0000   0.0000   1.0000  -1.0000
     ok
  intended none      -> none      2 pivot(s) in 2 column(s)
          1.0000   0.0000   2.0000
          0.0000   1.0000   2.0000
          0.0000   0.0000  -1.0000
     ok
     the last row reads 0 = -1.0000, which is false
  intended infinite  -> infinite  2 pivot(s) in 3 column(s)
          1.0000   0.0000   0.0000   3.5714
          0.0000   1.0000   0.0000   0.7143
          0.0000   0.0000   0.0000   0.0000
     ok

=== Part 2: particular solution and null direction, infinite case ===
pivot columns [0, 1], free column(s) [2]
x_p = [3.5714, 0.7143, 0.0]
A x_p = [5.0, 10.0, 15.0] (should be b)
null direction v = [-1.0, 0.0, 1.0]
A v = [0.0, 0.0, 0.0] (should be all zeros)

  t =   -2.0 -> x = [5.5714, 0.7143, -2.0]   residual 0.00e+00
  t =    0.0 -> x = [3.5714, 0.7143, 0.0]   residual 0.00e+00
  t =    1.5 -> x = [2.0714, 0.7143, 1.5]   residual 0.00e+00
  t =  100.0 -> x = [-96.4286, 0.7143, 100.0]   residual 0.00e+00

=== Part 3: LU of the unique system, and the structural checks ===
L =
  1.0000  0.0000  0.0000
  0.6667  1.0000  0.0000
  -0.6667  0.2000  1.0000
U =
  -3.0000  -1.0000   2.0000
  0.0000   1.6667   0.6667
  0.0000   0.0000   0.2000
perm = [1, 2, 0]  (row i of L U is row perm[i] of A)
max |L U - P A| = 0.00e+00
L has a unit diagonal:     True
L is lower triangular:     True
U is upper triangular:     True

=== Part 4: four right-hand sides, one factorisation ===
  b = [8.0, -11.0, -3.0]  ->  x = [2.0, 3.0, -1.0]   residual 1.78e-15
  b = [1.0, 0.0, 0.0]  ->  x = [4.0, -2.0, 5.0]   residual 1.78e-15
  b = [0.0, 1.0, 0.0]  ->  x = [3.0, -2.0, 4.0]   residual 8.88e-16
  b = [2.0, 2.0, 2.0]  ->  x = [12.0, -6.0, 16.0]   residual 3.55e-15

=== Part 5: hand-check x = [2, 3, -1] in the three original equations ===
  eq 0: 2*2 + 1*3 + -1*-1 = 8   right side 8   ok
  eq 1: -3*2 + -1*3 + 2*-1 = -11   right side -11   ok
  eq 2: -2*2 + 1*3 + 2*-1 = -3   right side -3   ok

=== Challenge: lstsq on the infinite and the inconsistent case ===
infinite case: rank 2 of 3 columns
lstsq          = [1.785714 0.714286 1.785714]
||x_p||        = 3.642157
||lstsq||      = 2.624453  (smaller: closer to the origin)
x_p . v        = -3.571429
t* = -(x_p.v)/(v.v) = 1.785714
foot x_p + t* v = [1.785714 0.714286 1.785714]
foot equals lstsq:  True
foot . v        = 3.55e-15  (perpendicular to the line direction)
residual ||A foot - b|| = 2.18e-15
A foot = b exactly, so the foot is a genuine solution AND the closest to
the origin. That is what 'minimum-norm solution' means.

inconsistent case: rank 2 of 2 columns
lstsq returns  = [2.       1.666667]   (a point, not an exception)
predicted      = [5. 3.333333 9.666667]
target         = [ 5.  4. 10.]
residual       = [ 0.33333333  0.33333333 -0.33333333]
||residual||   = 0.577350
The solution set is EMPTY, so this point is not a solution at all. It is the
closest point of the column space of A to b. You tell the two situations
apart by the residual: zero (to rounding) means every target is reachable,
and a nonzero residual means the target was out of reach and the fit is
approximate. Note the residual here is exactly (1/3, 1/3, -1/3): nonzero,
so the answer is genuinely approximate and no choice of x would have done
better.
```

**Challenge, part one, by hand.** On the line `x = x_p + t v` with
`x_p = [25/7, 5/7, 0]` and `v = [-1, 0, 1]`, the squared distance to the origin
is

    |x_p + t v|Â² = |x_p|Â² + 2 t (x_p Â· v) + tÂ² |v|Â²

with `x_p Â· v = -(25/7)` and `|v|Â² = 2`. Differentiating in `t` and setting to
zero gives `2(x_p Â· v) + 2 t |v|Â² = 0`, so `t* = -(x_pÂ·v)/|v|Â² = (25/7)/2 =
25/14 â‰ˆ 1.785714`, exactly the value the code finds. Then `x_p + t* v =
[25/7 - 25/14, 5/7, 25/14] = [25/14, 5/7, 25/14] = [1.785714, 0.714286,
1.785714]`, matching `lstsq` â€” and its norm `â‰ˆ 2.6245` is smaller than
`|x_p| â‰ˆ 3.6422`, as it must be, since `t = 0` is on the line too. The
perpendicularity check `(x_p + t* v) Â· v = (x_pÂ·v) + t*|v|Â² = -(25/7) + (25/14)(2)
= 0` is the whole content of "foot of a perpendicular": the nearest point of a
line to a point is the one where the segment joining them is orthogonal to the
line. The code confirms `foot Â· v = 3.55e-15`, i.e. zero to rounding, and
`A foot = b` exactly, so the foot is simultaneously a genuine solution and the
minimum-norm one.

**Challenge, part two.** For the inconsistent system, `lstsq` cannot raise
because the function it computes is defined whether or not the system is
solvable: minimise `â€–A x - bâ€–` over all `x`. The minimum always exists â€” a
continuous function on an unbounded set whose infimum is attained because the
quadratic term grows â€” so there is always a point to return, and the question is
only whether the minimum value is zero. When it is, `b` is in the column space
and the returned point is a real solution; when it is not, the point is the
closest achievable approximation and the system is unsolvable. Here the residual
is `(1/3, 1/3, -1/3)`, so `â€–Ax - bâ€– â‰ˆ 0.577`, firmly nonzero.

The practical test is therefore one line: **check the residual, not the
return value.** `np.linalg.solve` raises on a singular square matrix because it
promises an exact solution and cannot deliver one; `lstsq` does not raise
because it never promises an exact solution at all. It reports `rank` and
`residuals` precisely so you can make the distinction yourself, and the lesson
prints both. A residual of zero means the target was reachable; a residual of
size `Îµ` means your model cannot express the target to better than `Îµ`, and no
amount of re-solving the exact system will change that â€” the exact system has
no solution at all.

</details>

**[ ] Exercise 5 â€” banded structure, stability, and reusing a factorisation.**
Let `T` be the `5 Ã— 5` tridiagonal matrix with `2` on the diagonal and `âˆ’1` on the
two adjacent diagonals, and let `b = (1, 1, 1, 1, 1)áµ€`.

1. Solve `T x = b` by elimination with partial pivoting, report the number of row
   swaps and the growth factor, and verify the residual with a **banded**
   `O(n)` matrix-vector product rather than the dense one. Confirm the two
   residuals agree.
2. Count the nonzeros. Then, for `n âˆˆ {10, 100, 1000, 10000}`, report the
   multiply-add count for a dense solve against a banded one and the ratio.
3. Take `A = [[1e-11, 1], [1, 1 + 1e-11]]` with `b = (1, 1)`. Solve it with and
   without pivoting, forcing `tol = 0` so the `1e-11` counts as a pivot, and
   report the growth factor in each case. Compute the exact answer with
   `fractions.Fraction` and give the relative error of both.
4. Print the **per-equation** residuals of the unpivoted answer, not just the
   norm. Explain in two sentences why the first row's residual is exactly zero
   while `xâ‚€` is 100% wrong.
5. Do one step of iterative refinement on the unpivoted answer: form
   `r = b âˆ’ A x`, solve `A r = e`, and set `x â† x + e`. Report the relative error
   before and after, and the cost relative to refactorising.

**Challenge.** Factor `T` once with Crout LU and partial pivoting. Verify
`L U = P A`, that `L` is unit lower triangular, and that `U` is upper triangular.
Then solve `T x = b` for four different right-hand sides â€” all ones, the first
basis vector, all twos, and the ramp `(1, 2, 3, 4, 5)` â€” reusing the same
factors, and report the residual of each. Then explain in one paragraph why this
is *cheaper than it looks* only when the right-hand sides share the same `A`, and
what you must do instead when they do not.

<details>
<summary>Solution</summary>

**Part 1, by hand.** The pivots in column 0 are `2` and `âˆ’1`, so the largest is `2`
and no swap happens. Multiplier `âˆ’1/2`, giving row 1: `0, 2 âˆ’ (âˆ’1/2)(âˆ’1) = 3/2, âˆ’1,
1 + 1/2`. That `3/2` is where the growth of 1.5 comes from. Continuing, the
diagonal of `U` is `2, 3/2, 4/3, 5/4, 6/5` and back substitution with `b` all ones
gives `x = (2.5, 4, 4.5, 4, 2.5)`. The largest entry of `T` is `2`, and the largest
of the reduced matrix is `3`, so the growth factor is `3/2 = 1.5`.

The lesson's point is that this is *fine*. Pivoting bounds growth at `2^(nâˆ’1)`
and in practice keeps it near 1; `1.5` on a matrix whose largest entry is 2 is
nothing, and the residual `1.78e-15` confirms it. The lesson's `1e-11` example is
the other end of the scale, at growth `1e11`.

**Part 2.** `5n âˆ’ 2 = 13` nonzeros out of `25` slots. The ratio table is the whole
argument for structure: at `n = 10000` the dense route is about `3.3 Ã— 10Â¹Â¹`
multiply-adds and the banded route about `3.3 Ã— 10â·`. A single matvec is worse
still in relative terms â€” `nÂ² = 10â¶` against `3n = 3 Ã— 10â´` at `n = 10â´`, a factor
of 333 â€” because the dense version must *look at* every zero to decide it is one.

**Part 3.** Pivoting on `1e-11` gives multiplier `1/1e-11 = 10Â¹Â¹`, and the one
surviving entry becomes `âˆ’10Â¹Â¹`: growth `10Â¹Â¹`. Pivoting on the `1` instead costs
one swap and gives growth exactly `1.0`. Exact arithmetic (`fractions.Fraction`)
says the true answer is `(âˆ’1.00000000001e-11, 1)`, so the unpivoted `xâ‚€ = 0.0` is
wrong by `100%` of its own magnitude, relative error `1.000e-11`; the pivoted
answer is right to `8.273e-19`.

**Part 4.** `A x âˆ’ b` for the unpivoted `x = (0, 1)`:

    row 0:  1e-11Â·0 + 1Â·1 âˆ’ 1 = 0        exactly zero
    row 1:  1Â·0 + (1 + 1e-11)Â·1 âˆ’ 1 = 1e-11

The first row is `1e-11Â·xâ‚€ + 1Â·xâ‚ = 1`, which `(0, 1)` satisfies *perfectly* â€”
the tiny coefficient means the equation simply does not see `xâ‚€`. So `xâ‚€` is
undetermined by row 0, and row 1 constrains it only to within `1e-11`, which at
the scale of `b = 1` is below the noise floor of the computation. The residual is
small in every equation *simultaneously with* the answer being completely wrong,
because the wrongness lives in the direction the matrix cannot see.

**Part 5.** `r = b âˆ’ A x = (0, âˆ’1e-11)`, and solving `A r = e` gives
`e = (âˆ’1e-11, 1e-22)`, so `x + e = (âˆ’1e-11, 1)`, relative error `8.274e-19`. The
repair cost two matvecs and one triangular solve, `O(nÂ²)`, against the `O(nÂ³)` of
starting over. That factor of `n` is why production solvers refine rather than
restart.

```python
TOL = 1e-9


# ---------------------------------------------------------------- helpers
def shape(M):
    return len(M), len(M[0])


def zeros(rows, cols):
    return [[0.0] * cols for _ in range(rows)]


def matmul(A, B):
    rows_a, cols_a = shape(A)
    rows_b, cols_b = shape(B)
    if cols_a != rows_b:
        raise ValueError(f"cannot multiply {rows_a}x{cols_a} by {rows_b}x{cols_b}")
    C = zeros(rows_a, cols_b)
    for i in range(rows_a):
        for j in range(cols_b):
            total = 0.0
            for k in range(cols_a):
                total += A[i][k] * B[k][j]
            C[i][j] = total
    return C


def matvec(M, v):
    rows, cols = shape(M)
    if len(v) != cols:
        raise ValueError(f"vector has {len(v)} entries, matrix has {cols} columns")
    return [sum(M[i][k] * v[k] for k in range(cols)) for i in range(rows)]


def forward_elimination(A, b, tol=TOL, pivot=True):
    """Upper-triangular [A | b], reporting the growth factor and swap count."""
    M = [list(A[i]) + [b[i]] for i in range(len(A))]
    rows, cols = len(M), len(M[0])
    pivot_row, swaps = 0, 0
    max_scale = max(abs(v) for row in M for v in row)
    for col in range(cols - 1):
        if pivot_row == rows:
            break
        best = (max(range(pivot_row, rows), key=lambda r: abs(M[r][col]))
                if pivot else pivot_row)
        if abs(M[best][col]) <= tol:
            continue
        if best != pivot_row:
            M[pivot_row], M[best] = M[best], M[pivot_row]
            swaps += 1
        p = M[pivot_row][col]
        for r in range(pivot_row + 1, rows):
            f = M[r][col] / p
            if f != 0.0:
                for c in range(col, cols):
                    M[r][c] -= f * M[pivot_row][c]
        pivot_row += 1
    scale = max(abs(v) for row in M for v in row)
    return M, swaps, scale / max_scale


def back_substitution(U):
    n = len(U)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        total = U[i][n] - sum(U[i][j] * x[j] for j in range(i + 1, n))
        x[i] = total / U[i][i]
    return x


def matvec_band(M, v):
    """Multiply by a tridiagonal matrix in O(n) instead of O(n^2)."""
    n = len(v)
    out = []
    for i in range(n):
        total = M[i][i] * v[i]
        if i > 0:
            total += M[i][i - 1] * v[i - 1]
        if i < n - 1:
            total += M[i][i + 1] * v[i + 1]
        out.append(total)
    return out


def count_band(M, tol=1e-12):
    rows, cols = shape(M)
    return sum(1 for i in range(rows) for j in range(cols) if abs(M[i][j]) > tol)


def relative_error(approx, exact):
    scale = max(abs(v) for v in exact)
    return max(abs(a - e) for a, e in zip(approx, exact)) / max(scale, 1e-300)


# ---------------------------------------------------------------- 1
print("=== Part 1: a tridiagonal system ===")
n = 5
band = [[2.0 if i == j else (-1.0 if abs(i - j) == 1 else 0.0) for j in range(n)]
        for i in range(n)]
rhs = [1.0] * n
print(f"the {n}x{n} tridiagonal matrix (2 on the diagonal, -1 beside it):")
for row in band:
    print("  " + " ".join(f"{v:5.1f}" for v in row))
print(f"b = {rhs}")
print()
print(f"nonzeros stored: {count_band(band)} of {n * n} "
      f"(a dense loop would touch all {n * n})")
U, swaps, growth = forward_elimination(band, rhs)
x = back_substitution(U)
resid_dense = max(abs(matvec(band, x)[i] - rhs[i]) for i in range(n))
resid_band = max(abs(matvec_band(band, x)[i] - rhs[i]) for i in range(n))
print()
print("upper triangular [T | b]:")
for row in U:
    print("  " + " ".join(f"{v:9.4f}" for v in row))
print(f"back substitution gives x = {[round(v, 6) for v in x]}")
print(f"residual with a DENSE matvec  = {resid_dense:.2e}")
print(f"residual with a BANDED matvec = {resid_band:.2e}")
print(f"the two agree: {abs(resid_dense - resid_band) < 1e-12}")
print(f"swaps = {swaps}, growth factor = {growth:.6f}")
print()
print("Growth 1.5, not 1. Worth explaining rather than glossing. Partial pivoting")
print("only guarantees |multiplier| <= 1, so an entry can at most double per")
print("step. Here the multipliers are -1/2 in the interior, and the first step")
print("replaces a -1 with 2 - (-1/2)(-1) = 1.5, the largest entry in the result.")
print("The largest original entry was 2, so g = 3/2. That is mild, and the")
print("residual confirms it.")

# ---------------------------------------------------------------- 2
print()
print("=== Part 2: the cost of the two routes, counted not timed ===")
print("Counting multiply-adds is machine independent, which is the right way to")
print("make a complexity claim.")
print()
for size in (10, 100, 1000, 10000):
    dense_route = size ** 3 // 3 + size * size // 2      # elimination + back sub
    band_solve = size * size // 3 + 3 * size            # banded elimination
    print(f"  n = {size:6d}: dense solve {dense_route:>18,}   "
          f"banded {band_solve:>12,}   ratio {dense_route / band_solve:8.1f}x")
print()
print(f"  a single dense matvec at n = 1000 is n^2 = {1000 * 1000:,}")
print(f"  the banded matvec is 3n        = {3 * 1000:,}"
      f"   factor of {1000 * 1000 // (3 * 1000):,}")
print("The lesson's claim: an n-by-n matrix with k nonzeros per row costs about")
print("O(n k^2), not O(n^3). At n = 10^4 that is roughly 3 x 10^11 against")
print("3 x 10^7 -- four orders of magnitude.")

# ---------------------------------------------------------------- 3
print()
print("=== Part 3: the 1e-11 example, where the growth factor is the diagnostic ===")
bad = [[1e-11, 1.0],
       [1.0, 1.0 + 1e-11]]
bad_b = [1.0, 1.0]
print(f"A = {bad}")
print(f"b = {bad_b}")
U_np, s_np, g_np = forward_elimination(bad, bad_b, tol=0.0, pivot=False)
x_np = back_substitution(U_np)
U_p, s_p, g_p = forward_elimination(bad, bad_b, pivot=True)
x_p = back_substitution(U_p)
print()
print("no pivoting (tol forced to 0 so 1e-11 counts as a pivot):")
for row in U_np:
    print("  " + " ".join(f"{v:>18.6e}" for v in row))
print(f"  x = {x_np}")
print(f"  growth = {g_np:.3e}, swaps = {s_np}")
print()
print("with partial pivoting:")
for row in U_p:
    print("  " + " ".join(f"{v:>18.6e}" for v in row))
print(f"  x = {[float(f'{v:.6g}') for v in x_p]}")
print(f"  growth = {g_p:.3e}, swaps = {s_p}")

# The exact answer, in exact rational arithmetic.
from fractions import Fraction as Fr

Ae = [[Fr(1, 10 ** 11), Fr(1)], [Fr(1), Fr(1) + Fr(1, 10 ** 11)]]
be = [Fr(1), Fr(1)]
dd = Ae[0][0] * Ae[1][1] - Ae[0][1] * Ae[1][0]
x_exact = [(be[0] * Ae[1][1] - Ae[0][1] * be[1]) / dd,
           (Ae[0][0] * be[1] - be[0] * Ae[1][0]) / dd]
print()
print(f"exact x (rational arithmetic, no rounding) = "
      f"{[float(f'{float(v):.17g}') for v in x_exact]}")
print(f"relative error, no pivoting : {relative_error(x_np, x_exact):.3e}")
print(f"relative error, with pivot  : {relative_error(x_p, x_exact):.3e}")

# ---------------------------------------------------------------- 4
residuals = [sum(bad[i][j] * x_np[j] for j in range(2)) - bad_b[i] for i in range(2)]
print()
print("=== Part 4: the per-equation residuals of the WRONG answer ===")
print(f"  x_np              = {x_np}")
print(f"  A x_np - b        = {[float(f'{t:.3e}') for t in residuals]}")
print(f"  ||A x_np - b||_inf = {max(abs(t) for t in residuals):.3e}")
print()
print("Row 0 is 1e-11*x0 + 1*x1 = 1, which (0, 1) satisfies EXACTLY: the tiny")
print("coefficient means row 0 cannot see x0 at all. Row 1 pins x0 only to within")
print("1e-11, which at the scale of b = 1 is below the noise floor. So the")
print("residual is small in both equations at the same time as the answer is")
print("completely wrong, because the wrongness lives in the direction the matrix")
print("cannot see. The growth factor (1e11 vs 1.0) is what warned you.")

# ---------------------------------------------------------------- 5
print()
print("=== Part 5: one step of iterative refinement ===")
r = [bad_b[i] - sum(bad[i][j] * x_np[j] for j in range(2)) for i in range(2)]
e = back_substitution(forward_elimination(bad, r)[0])
x_fixed = [x_np[i] + e[i] for i in range(2)]
print(f"  x before         = {[float(f'{v:.6g}') for v in x_np]}")
print(f"  relative error   = {relative_error(x_np, x_exact):.3e}")
print(f"  residual r = b - A x = {[float(f'{v:.3e}') for v in r]}")
print(f"  solve(A, r)      = {[float(f'{v:.6g}') for v in e]}")
print(f"  x after          = {[float(f'{v:.6g}') for v in x_fixed]}")
print(f"  relative error   = {relative_error(x_fixed, x_exact):.3e}")
print("Cost of the repair: two matvecs and one triangular solve, O(n^2), against")
print("the O(n^3) of refactorising. That factor of n is why production solvers")
print("refine rather than restart.")

# ---------------------------------------------------------------- 6
print()
print("=== Challenge: one factorisation, four right-hand sides ===")


def lu_factor(A, tol=TOL):
    """Crout LU with partial pivoting. Returns (L, U, perm) with P A = L U."""
    n = len(A)
    U = [list(row) for row in A]
    L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    perm = list(range(n))
    for k in range(n):
        best = max(range(k, n), key=lambda r: abs(U[r][k]))
        if best != k:
            U[k], U[best] = U[best], U[k]
            for j in range(k):
                L[k][j], L[best][j] = L[best][j], L[k][j]
            perm[k], perm[best] = perm[best], perm[k]
        if abs(U[k][k]) <= tol:
            raise ZeroDivisionError("singular matrix")
        for i in range(k + 1, n):
            L[i][k] = U[i][k] / U[k][k]
            for j in range(k, n):
                U[i][j] -= L[i][k] * U[k][j]
    return L, U, perm


def lu_solve(L, U, perm, b):
    n = len(L)
    y = [b[perm[i]] for i in range(n)]
    for i in range(n):
        y[i] -= sum(L[i][j] * y[j] for j in range(i))
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
    return x


L, U, perm = lu_factor(band)
print("one Crout factorisation of the tridiagonal matrix:")
print("  L =")
for row in L:
    print("    " + " ".join(f"{v:6.3f}" for v in row))
print("  U =")
for row in U:
    print("    " + " ".join(f"{v:6.3f}" for v in row))
print(f"  perm = {perm}   (row i of L U is row perm[i] of A)")

PA = [[band[perm[i]][j] for j in range(n)] for i in range(n)]
LU = [[sum(L[i][k] * U[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
print(f"  max |L U - P A| = "
      f"{max(abs(LU[i][j] - PA[i][j]) for i in range(n) for j in range(n)):.2e}")
print(f"  L unit lower triangular: "
      f"{all(L[i][j] == 0.0 for i in range(n) for j in range(i + 1, n)) and all(L[i][i] == 1.0 for i in range(n))}")
print(f"  U upper triangular:     "
      f"{all(U[i][j] == 0.0 for i in range(n) for j in range(i))}")
print()
print("four right-hand sides, one factorisation:")
for label, bv in (("ones", [1.0] * n),
                  ("e_0", [1.0, 0.0, 0.0, 0.0, 0.0]),
                  ("twos", [2.0] * n),
                  ("ramp", [1.0, 2.0, 3.0, 4.0, 5.0])):
    xi = lu_solve(L, U, perm, bv)
    res = max(abs(matvec_band(band, xi)[i] - bv[i]) for i in range(n))
    print(f"  b = {label:5s} {bv}  ->  x = {[round(v, 4) for v in xi]}"
          f"   residual {res:.2e}")
print()
print("The O(n^3) elimination happened once, before the loop. Each extra")
print("right-hand side costs a permutation plus two triangular solves, O(n^2).")
print("That is cheaper than it looks ONLY because every b shares the same A. When")
print("the matrices differ you must refactorise each, at O(n^3) apiece, and the")
print("reuse argument does not apply -- which is why solvers expose a factors")
print("interface at all, and why a caller with a loop over matrices should keep")
print("the factorisation beside the loop.")
```

Output:

```
=== Part 1: a tridiagonal system ===
the 5x5 tridiagonal matrix (2 on the diagonal, -1 beside it):
    2.0  -1.0   0.0   0.0   0.0
   -1.0   2.0  -1.0   0.0   0.0
    0.0  -1.0   2.0  -1.0   0.0
    0.0   0.0  -1.0   2.0  -1.0
    0.0   0.0   0.0  -1.0   2.0
b = [1.0, 1.0, 1.0, 1.0, 1.0]

nonzeros stored: 13 of 25 (a dense loop would touch all 25)

upper triangular [T | b]:
  2.0000  -1.0000   0.0000   0.0000   1.0000
  0.0000   1.5000  -1.0000   0.0000   1.5000
  0.0000   0.0000   1.3333  -1.0000   2.0000
  0.0000   0.0000   0.0000   1.2500   2.5000
  0.0000   0.0000   0.0000   0.0000   3.0000
back substitution gives x = [2.5, 4.0, 4.5, 4.0, 2.5]
residual with a DENSE matvec  = 1.78e-15
residual with a BANDED matvec = 1.78e-15
the two agree: True
swaps = 0, growth factor = 1.500000

Growth 1.5, not 1. Worth explaining rather than glossing. Partial pivoting
only guarantees |multiplier| <= 1, so an entry can at most double per
step. Here the multipliers are -1/2 in the interior, and the first step
replaces a -1 with 2 - (-1/2)(-1) = 1.5, the largest entry in the result.
The largest original entry was 2, so g = 3/2. That is mild, and the
residual confirms it.

=== Part 2: the cost of the two routes, counted not timed ===
Counting multiply-adds is machine independent, which is the right way to
make a complexity claim.

  n =     10: dense solve                383   banded           63   ratio      6.1x
  n =    100: dense solve            338,333   banded        3,633   ratio     93.1x
  n =   1000: dense solve        333,833,333   banded      336,333   ratio    992.6x
  n =  10000: dense solve    333,383,333,333   banded   33,363,333   ratio   9992.5x

  a single dense matvec at n = 1000 is n^2 = 1,000,000
  the banded matvec is 3n        = 3,000   factor of 333
The lesson's claim: an n-by-n matrix with k nonzeros per row costs about
O(n k^2), not O(n^3). At n = 10^4 that is roughly 3 x 10^11 against
3 x 10^7 -- four orders of magnitude.

=== Part 3: the 1e-11 example, where the growth factor is the diagnostic ===
A = [[1e-11, 1.0], [1.0, 1.00000000001]]
b = [1.0, 1.0]

no pivoting (tol forced to 0 so 1e-11 counts as a pivot):
        1.000000e-11       1.000000e+00       1.000000e+00
        1.110223e-16      -1.000000e+11      -1.000000e+11
  x = [0.0, 1.0]
  growth = 1.000e+11, swaps = 0

with partial pivoting:
        1.000000e+00       1.000000e+00       1.000000e+00
        0.000000e+00       1.000000e+00       1.000000e+00
  x = [-1e-11, 1.0]
  growth = 1.000e+00, swaps = 1

exact x (rational arithmetic, no rounding) = [-1.00000000001e-11, 1.0]
relative error, no pivoting : 1.000e-11
relative error, with pivot  : 8.273e-19

=== Part 4: the per-equation residuals of the WRONG answer ===
  x_np              = [0.0, 1.0]
  A x_np - b        = [0.0, 1e-11]
  ||A x_np - b||_inf = 1.000e-11

Row 0 is 1e-11*x0 + 1*x1 = 1, which (0, 1) satisfies EXACTLY: the tiny
coefficient means row 0 cannot see x0 at all. Row 1 pins x0 only to within
1e-11, which at the scale of b = 1 is below the noise floor. So the
residual is small in both equations at the same time as the answer is
completely wrong, because the wrongness lives in the direction the matrix
cannot see. The growth factor (1e11 vs 1.0) is what warned you.

=== Part 5: one step of iterative refinement ===
  x before         = [0.0, 1.0]
  relative error   = 1.000e-11
  residual r = b - A x = [0.0, -1e-11]
  solve(A, r)      = [-1e-11, 1e-22]
  x after          = [-1e-11, 1.0]
  relative error   = 8.274e-19
Cost of the repair: two matvecs and one triangular solve, O(n^2), against
the O(n^3) of refactorising. That factor of n is why production solvers
refine rather than restart.

=== Challenge: one factorisation, four right-hand sides ===
one Crout factorisation of the tridiagonal matrix:
  L =
     1.000  0.000  0.000  0.000  0.000
    -0.500  1.000  0.000  0.000  0.000
     0.000 -0.667  1.000  0.000  0.000
     0.000  0.000 -0.750  1.000  0.000
     0.000  0.000  0.000 -0.800  1.000
  U =
     2.000 -1.000  0.000  0.000  0.000
     0.000  1.500 -1.000  0.000  0.000
     0.000  0.000  1.333 -1.000  0.000
     0.000  0.000  0.000  1.250 -1.000
     0.000  0.000  0.000  0.000  1.200
  perm = [0, 1, 2, 3, 4]   (row i of L U is row perm[i] of A)
  max |L U - P A| = 0.00e+00
  L unit lower triangular: True
  U upper triangular:     True

four right-hand sides, one factorisation:
  b = ones  [1.0, 1.0, 1.0, 1.0, 1.0]  ->  x = [2.5, 4.0, 4.5, 4.0, 2.5]   residual 1.78e-15
  b = e_0   [1.0, 0.0, 0.0, 0.0, 0.0]  ->  x = [0.8333, 0.6667, 0.5, 0.3333, 0.1667]   residual 1.11e-16
  b = twos  [2.0, 2.0, 2.0, 2.0, 2.0]  ->  x = [5.0, 8.0, 9.0, 8.0, 5.0]   residual 3.55e-15
  b = ramp  [1.0, 2.0, 3.0, 4.0, 5.0]  ->  x = [5.8333, 10.6667, 13.5, 13.3333, 9.1667]   residual 5.33e-15

The O(n^3) elimination happened once, before the loop. Each extra
right-hand side costs a permutation plus two triangular solves, O(n^2).
That is cheaper than it looks ONLY because every b shares the same A. When
the matrices differ you must refactorise each, at O(n^3) apiece, and the
reuse argument does not apply -- which is why solvers expose a factors
interface at all, and why a caller with a loop over matrices should keep
the factorisation beside the loop.
```

**Challenge, the paragraph.** The reuse is cheaper than it looks *only* when every
right-hand side shares the same `A`, and the reason is structural rather than
incidental: the factorisation contains no information about `b`. Every entry of
`L` is a ratio of entries of `A`; every entry of `U` is an entry of `A` or a
combination of them; `perm` records row permutations of `A`. So the `Î˜(nÂ³)` is a
property of `A` alone, and `Î˜(nÂ²)` per solve is a property of how cheaply a
triangular system can be resolved. The loop pays `Î˜(nÂ³ + k nÂ²)` against
`Î˜(k nÂ³)`, and the gap widens with `k` because `n` is fixed.

When the matrices *differ*, none of that carries over. Each `A_i` needs its own
`Î˜(nÂ³)` factorisation, and the arithmetic count is `Î˜(k nÂ³)` â€” worse than the
single-solve case, because you have paid the factorisation and the substitution
`k` times over. The right response is then to look for structure that makes the
factorisations themselves cheaper: banded `A_i` at `O(n bÂ²)`, symmetric positive
definite at Cholesky's half, or â€” when the `A_i` are *close* to one another â€” a
single factorisation plus a low-rank update, which is how a Kalman filter avoids
refactorising every step. And when nothing can be reused, that is simply the cost
of the problem, which is why libraries expose `lu_factor`/`lu_solve` separately:
the caller decides where the loop goes.

</details>

## Summary

- `Ax = b` is the universal form of "too many linked equations". Row operations
  preserve the solution set, so the algorithm reduces the system and reads the
  answer off.
- Echelon form (zeros below the diagonal) plus back substitution is
  `Î˜(nÂ³)` + `Î˜(nÂ²)`. Partial pivoting costs `O(n)` extra per step and is
  mandatory in floating point.
- Partial pivoting picks the largest absolute entry in the column as the
  divisor. Without it, entries grow by `n Â· u` per step and the answer can be
  completely wrong with a residual of exactly zero.
- RREF gives the full diagnosis: pivot count equal to column count means unique;
  a row `0 = nonzero` means no solution; a column with no pivot means free
  variables and infinitely many solutions.
- A row `[0 â€¦ 0 | c]` with `c â‰  0` is the entire diagnosis for "no solution",
  and it takes one inspection to find.
- LU factorisation splits the `O(nÂ³)` work from the `O(nÂ²)` solves, so one
  factorisation serves any number of right-hand sides. This is why solvers take
  factors as input.
- `np.linalg.solve`, not `inv(A) @ b`. And `np.linalg.cond` before trusting an
  answer on a badly scaled system.

## Next

[33 â€” Determinant and Inverse](33_determinant_and_inverse.md) asks the same
question without doing the work: is this square matrix invertible? The
determinant answers it with a formula involving no division, it tells you the
volume scale factor of the corresponding transformation, and it gives the
cleanest closed forms for the inverse that exist.
