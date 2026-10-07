# Independent review of shell grids and rational complexity

Date: 2026-10-02. Scope: full-draft proof review of the positive-`L`
construction in [mixed-shell-certificate.md](mixed-shell-certificate.md),
focusing on lattice rounding, shell flags, state counts, and rational
bit lengths. The parent review covers global shell coverage, the bottom
radial step, and the separately added `L=0` branch. No external searches,
new tests, or CI checks were run for this review.

**Conclusion.** The grid construction and parameter-dependent bit bound
check out. The acceptance test is correctly nonstrict in both the draft
and the exact checker. Two small clarifications were requested and applied: explicitly
include supplied `L` in the input encoding length, and separate the
immediately clipped first-label case in the grid-count proof.

## 1. Feasible lattice rounding and the shell flag

Write `h` for one coordinate's lattice spacing and `U` for its feasible
side cap inside `[0,2S]`. The proposed point is lattice-feasible, so every
feasible displacement is an integer multiple of `h`. The grid starts at

```
a_0=min{U,h ceil(delta S/(2nh))}
```

and subsequently adds `h max{1,floor(delta a/h)}`, clipping to `U`.
All labels remain feasible lattice displacements. An interval of length
one lattice step contains no feasible target other than its endpoints;
rounding therefore has exactly zero variance there.

If the initial interval contains at least two steps, its width is at
most `delta S/n`: the relevant ceiling is at least two, and
`ceil(t)<=2t` for that case. A later interval of at least two steps
has width at most `delta a`, where `a` is its lower absolute label.
Clipping can only reduce this width. Inserting a lattice threshold
cannot split a one-step interval internally; when it splits a longer
interval, both new widths retain the bound, with the upper interval's
new lower label at least `a`. These observations justify the draft's
variance estimate for every feasible lattice target, including its
initial interval.

The added threshold `h ceil(S/h)` is equally essential. If an original
lattice displacement has magnitude at least `S`, it is at least this
threshold. The threshold is then feasible, and its insertion ensures
that both enclosing rounding endpoints retain magnitude at least `S`.
Reflection proves the negative-side statement. Continuous coordinates
use the exact threshold `S` and obey the same argument. Thus one
coordinate witnessing the original shell also witnesses the rounded
shell almost surely. Independent mean-preserving rounding consequently
preserves the linear and off-diagonal expectations without sacrificing
the OR constraint.

## 2. Number of labels

If `a_0=U`, there is only one positive label. Otherwise
`a_0>=delta S/(2n)`. For a lattice side, there are at most
`O(1/delta)` labels below `2h/delta`. Above that value, a nonterminal
step is at least `delta a/2`, so labels grow geometrically. The ratio
traversed is at most `2S/a_0<=4n/delta`. Thus each side has

```
O(delta^(-1) log(2n/delta))
```

labels, independently of its physical width and lattice spacing.
Clipping, the threshold label, and both signs change only constants.
The draft's use of `a_0>=delta S/(2n)` needs the just-stated exclusion
of an immediately clipped side; the final author draft includes that clarification.
The continuous count follows from the same ratio without the lattice
prefix.

Only the label count is independent of widths and spacings. The number
of shells is `O(1+log(D/r_0))`, and their encoded scales still contribute
to arithmetic and bit work. The draft states this distinction correctly.

## 3. Rational size and input dependence

Effective lattice endpoints, signed side widths, and `r_0` are computed
by rational arithmetic and integer floors or ceilings. They have
polynomial encoding length. The ratio `D/r_0` has polynomial encoding
length, so the number of dyadic shells is `O(I)`. Each radius
`S_j=2^j r_0` has polynomially many bits; it need not itself be a
power of two.

A lattice label is an integer multiple of an input spacing. The
multiplier is bounded by an encoded domain-to-spacing ratio and has
polynomially many bits, even when there are numerically many feasible
labels. The algorithm computes large initial multipliers directly;
it does not enumerate the intervening lattice points.

Let `D_0` clear the denominators of the input and computed rational
data, including `r_0`, translated objective coefficients, spacings,
endpoints, and `L`. Its bit length is polynomial in `I`. At trial
`delta=2^(-r)`, a common denominator for all displacement labels in
all shells divides

```
T=D_0 (2n) 2^(r(K+1)).
```

Indeed, a continuous geometric label is a rational starting label
times `(1+delta)^k`; shell indices contribute integer powers of two
to numerators. Threshold and clipped labels already have denominators
dividing the input-data denominator. Lattice floors and ceilings add
no denominators. A common denominator for corrected local factors and
the root comparison divides `D_0 2^(2r+3) T^2`.

Finite DP messages select sums of assigned factor values. They do not
multiply denominators across bags, and their numerator lengths include
only polynomial input costs and `O(rK)` grid costs. Hence the stated
`f(p,L/g) poly(I)` bit bound follows from the grid count and the
logarithmic-power absorption already used in the homogeneous proof.
It is necessary to include supplied `L` in `I`; the final author draft
now does so explicitly.

## 4. Nonstrict acceptance and verification scope

The draft checks `m_(S,delta)>=sigma S^2/n`. This nonstrict comparison
already certifies the positive margin `sigma`, because the shell
inequality gives `F(x)-F(s)-sigma||x-s||^2>=0`. Consequently the
discovery threshold `sigma<=g/3` is valid, including equality in
dimension one. A strict acceptance test would require adjusting that
threshold; neither the draft nor the inspected checker makes that
mistake.

I read [check_mixed_shell_certificate.py](check_mixed_shell_certificate.py).
Its shell acceptance assertion uses the required `>=`. It checks exact
scalar mean and variance identities, feasible lattice labels, threshold
preservation, reflected means, and a coupled mixed shell inequality.
Its shell minima are computed by direct product-grid enumeration. It
therefore checks the rounding argument and finite inequalities, but
does not independently implement or validate sparse OR-message DP.
The parent reports a successful run with 1,276 scalar cases and 156
mixed-shell or radial cases. This review did not rerun that command.
