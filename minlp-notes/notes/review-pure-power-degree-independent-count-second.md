# Second review: degree-independent finite pure-power counts

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Reviewed note: `notes/pure-power-degree-independent-integer-count.md`.
Verdict: **PASS**, with the stated unrestricted-size real-coefficient
scope for the degree-independent upper construction.

This audit checks the mathematical claims and the distinction between
integer count and compact rational construction. It establishes no
publication priority.

## Degree-independent lower bound

For `D>=2`, convexity of `x^(D/2)` on the nonnegative interval gives

```
((a+b)/2)^D <= [(a^(D/2)+b^(D/2))/2]^2.
```

Subtracting from `(a^D+b^D)/2` proves the stated Jensen lower bound
with factor `1/4`. This factor has no degree dependence.

The coordinate map `t_i=x_i^(D_i/2)` is a homeomorphism of the unit cube,
including for odd degrees. Closed parity supports map to compact sets that
still cover that cube. For independent uniform points in a transformed
support, evaluate the original Jensen vector at their inverse images.
It is bounded and belongs to the closed convex body `K`; its expectation
therefore belongs to `K`. Positivity and the scalar inequality give

```
0<=(1/2)C diag(Sigma)<=EJ.
```

Unconditional domination consequently makes `p_i=Sigma_ii/2` feasible.
The cap follows from `Sigma_ii<=1/4`. Hadamard gives
`det Sigma<=2^r product_i p_i<=2^r D_alloc`, and the volume-covariance
inequality yields the factor `2^(r/2)` in the stated support-volume bound.
The transformed cover proves `p_conv>=Phi-A_r`. There is no assertion
that the power map preserves original volumes or support convexity.

The constant estimate is valid. For example, the Gaussian bound
`omega_r<=(2 pi e/r)^(r/2)` and `1+2/r<=3` imply
`omega_r(r+2)^(r/2)<8^r`, since `6 pi e<64`. Hence `A_r<7r/2`,
including dimension one. Inactive affine coordinates can be eliminated
by affine output subtraction and projection and restored continuously,
as in the reviewed base theorem.

## Uniform chord error

The chord lies above the convex power graph. If `A<=B/2`, its value
is at most `B^2`, so its nonnegative error is at most
`B^2<=4(B-A)^2`. This covers the endpoint `a=0`.

If `A>B/2`, then `a>0`. The second-derivative chord bound and the
mean-value lower bound for the power transform give

```
chord(x)-x^D
 <=[(D-1)/(2D)](b/a)^(D-2)(B-A)^2.
```

Here

```
(b/a)^(D-2)=(B/A)^(2-4/D)<=4,
```

because `D>=2` and `B/A<2`. The coefficient is therefore at most two.
The exponent is zero when `D=2`, so that boundary case is valid. The
two cases establish the claimed global bound `4(B-A)^2` without any
degree-dependent hidden constant.

## Cell bands and binary encoding

The selected depths give `4h_i^2<=p_i`. On every nonuniform cell the
true power and every allowed band value differ by at most `4h_i^2`:
if the chord error is `e in [0,4h_i^2]`, subtracting that interval
allows precisely errors in `[e-4h_i^2,e]`, a subset of
`[-4h_i^2,4h_i^2]`. Exact graph points are included. Nonnegative output
coefficients then yield `|w-f(x)|<=Cp`, and unconditionality places the
entire admitted error vector in `K`.

The finite disjunction has exactly `2^(L_i)` cells, so all cells can be
assigned distinct binary strings of length `L_i` with no unused strings.
Its polytope for a cell includes both the interval constraints on `x_i`
and the two chord-band inequalities. I requested that the interval
constraints be listed explicitly in the relaxed cell system; the author
added them. This makes the intended complete-cell encoding explicit.

For completeness, global bounds `0<=x_i<=1` and `-1<=z_i<=1` suffice:
the chord is between zero and one and `4h_i^2<=p_i<=1`. For each cell,
the Hamming distance from its assigned string is a linear function of
the binaries, equal to zero at that string and at least one at every
other assignment. Each cell inequality can therefore be relaxed by its
own finite constant times this distance, taking the constant to dominate
its maximum violation over the global rectangle. All such maxima are
finite, since the coefficients are finite and the rectangle is compact.

At an integer assignment exactly one complete cell system is imposed and
all others are redundant. Conversely every point of a cell is feasible
at its assigned string. Shared boundaries present no issue. This proves
the exact union representation using only `L_i` bits, with real
coefficients and finitely many rows. It does not depend on a bounded-size
or bounded-encoding big-M construction.

The allocation maximum is attained and has positive product because `K`
contains a neighborhood of zero. Thus an optimal positive allocation can
be used in the finite construction. Summing
`L_i<=-(1/2)log2 p_i+2` proves `p_bin<=Phi+2r`. Combining with the
lower bound gives the claimed degree-independent comparison with
`p_conv+11r/2`.

## The compactness qualification is essential and correctly retained

The nonuniform knots may be irrational, and the formulation explicitly
lists all cells. Their number can be exponential in the accuracy's binary
encoding. The proof therefore supplies a finite real-coefficient integer
count bound, not a compact rational algorithm attaining that count.

For rational dense input, the separately reviewed original-coordinate
prefix-power construction and rational allocation oracle remain applicable.
Their upper count is
`Phi+sum_i log2 D_i+r+1/(2 ln 2)`. Combining this with the stronger lower
bound from this note gives

```
p_out<=p_conv+sum_i log2 D_i+(9r/2)+1.
```

Polynomial time and size still refer to the dense degree representation,
not sparse binary encoding of arbitrarily large exponents. A single power
per active coordinate shared across all outputs is an explicit assumption;
the argument does not establish the same benchmark for arbitrary mixtures
of powers on one coordinate. No unresolved mathematical defect was found.

The later checker `code/quadratic_rank/check_pure_power_reciprocal_interpolation.py`
was inspected and rerun during the compact-interpolation audit. Its 3,348
exact chord inequalities through degree 32 all passed, including odd
degrees represented by rational squared endpoints. These finite checks
supplement the uniform proof above.
