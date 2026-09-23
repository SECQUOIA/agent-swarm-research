# Independent audit: bounded-power follower optimization in accuracy bits

Date: 2026-09-05. Reviewer: potential_flow_review. Verdict: full PASS.

I independently checked
[the candidate](bilevel-bounded-power-accuracy-bit-algorithm.md), including
all clipping endpoints, polynomial approximation constants, arrangement
closures, fixed-dimensional algebraic optimization, rational feasible
leader recovery, and the separate growing-power obstruction. No additional
assumption or unresolved mathematical defect was found in its stated scope.
This review does not establish publication priority.

## Follower response and approximation ledger

Each follower objective has derivative `z^p-ell(x)`, strictly increasing
on `[0,1]`. Thus its unique minimizer is the stated clipped root, including
`ell=0` and `ell=1`. A vanishing second derivative at zero for `p>1` does
not affect strict convexity or uniqueness; uniform strong convexity is not
used.

With `m=ceil(log2(1/eta))` and `K=Pm`, every `p<=P` satisfies
`2^(-K/p)<=2^(-m)<=eta`. The zero approximation is therefore valid below
the truncation threshold, including negative affine arguments. Above one,
the constant response is exact.

Every dyadic interval maps to `|u|<=1/3` with the stated rational center.
For `alpha=1/p`, the binomial coefficient recurrence gives absolute values
at most one. Summing the geometric majorants proves

```
|T_q|<=3/2,
tail <=3^(-q)/2<=eta/4,       q=m+1.
```

The last inequality follows from `2^(-m)<=eta` and
`2*3^(-(m+1))<=2^(-m)`. Replacing the possibly irrational base root by a
rational number within `eta/4` therefore contributes at most `3eta/8`,
and the Taylor remainder contributes at most `eta/4`. The total is at
most `5eta/8<eta`. No exact algebraic coefficient is retained in these
surrogate polynomials.

Ordinary rational bisection computes the base-root approximation in
polynomial time for bounded `p`. Binomial coefficients, inverse dyadic
scalings, and polynomial expansions have polynomial bit length in `m,K`
and the rational input. Coefficients may be numerically large near the
smallest interval, but their logarithms remain polynomially bounded.
Zero upper response coefficients and `A=0` have the stated harmless
treatment. Fixed `P`, fixed leader dimension, and a requested accuracy
count `B` give polynomial bounds in input length and `B`, as claimed.

## Clipping cells and polynomial coefficients

The hyperplanes at all dyadic thresholds give polynomially many realizable
cells in fixed leader dimension. Constant affine arguments are handled
by constant sign tests. A zero affine argument needs no separate clipping
hyperplane because it lies in the uniformly valid truncated region.

For a nonempty relative sign cell, replacing its strict inequalities by
weak ones inside `X` gives its closure: mix a candidate boundary point
with an actual relative-cell point. This also works for lower-dimensional
`X` and zero-sign cells. At a threshold, either adjacent valid approximation
has the proved error, including the constant branches at the two extreme
thresholds. Thus each chosen polynomial remains valid on its entire
closed cell.

The signed coefficient sum satisfies
`|H_C-H|<=sum_i |c_i| eta<=epsilon/16`. Adjacent surrogate polynomials
need not agree at a common boundary. Since each is uniformly valid there
and the closed cells cover `X`, this causes no optimization gap.
After substitution, the number of monomials grows with the fixed leader
dimension and surrogate degree, not with the number of follower variables.
All substituted coefficients retain polynomial rational encoding.

The same audited estimates are polynomial in the numerical maximum power
`P`; fixed `P` is not necessary when powers are unary or densely encoded.
Indeed `K=Pm`, rational power comparisons have polynomial bit length in
`P,m`, and arrangement complexity is polynomial in `N,P,m` for fixed
leader dimension. The author subsequently made this stronger encoding
scope explicit. It does not assert polynomial dependence on `log P` alone.

## Exact surrogate optimization and algebraic field scope

The cell polynomial has rational coefficients. Its exact minimization
can be expressed with only a fixed number of real variables, for example
using one leader vector, one competing leader vector, and the objective
value. Compactness guarantees attainment, including positive-dimensional
minimizer sets.

I checked the primary
[Basu survey](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf),
Theorem 2.18 for quantifier elimination with degree and bit-size bounds,
and Section 2.2.2 for univariate representations of algebraic points.
For fixed variable count these give polynomial complexity and polynomial
encoding. One algebraic sample of the minimizer set therefore has the
required bounded-degree representation.

Comparing polynomially many algebraic cell minima does not require a
common field for all of them: pairwise comparison of polynomial-degree
real algebraic numbers suffices. Within the selected cell, the coordinates
of its minimizer can share its univariate representation. Barycentric
weights are obtained by rational linear algebra applied to those same
coordinates, so their computations do not introduce independent follower
radicals or a tower of growing algebraic extensions.

## Exact feasible rational recovery

A nonempty compact rational cell has rational vertices. Even in lower
dimension, a vertex has a full-rank active system in the ambient leader
dimension, with its equalities included. Enumerating these systems and
affinely independent subsets of at most `r+1` vertices has polynomial
complexity for fixed `r`.

Caratheodory's theorem supplies a containing simplex. Its barycentric
coordinates can be tested exactly in the selected minimizer's algebraic
representation. Rounding its first `s-1` weights downward and placing the
remaining mass on the last vertex preserves nonnegativity, unit total
weight, and exact membership in the cell. In particular, it preserves
affine equalities that independent coordinate rounding could violate.

The weight one-norm change is at most `2(s-1)/R<=2r/R`. Because every
vertex is in the unit cube, the leader infinity-norm change is at most
`2r/R`. The displayed coefficient bound gives
`sum_i |partial_i Q|<=L` throughout that cube. Hence

```
Q(xhat)-Q(xstar)<=2rL/R<=epsilon/4.
```

The denominator `R` may be large, but its bit length is polynomial.
Each exact floor is found by binary search over `[0,R]`, using polynomially
many algebraic comparisons. Singleton cells need no rounding, and the
zero-dimensional leader case is likewise direct.

Combining the two `epsilon/16` surrogate errors with this `epsilon/4`
loss gives suboptimality at most `3epsilon/8`. Evaluating each clipped
root at the returned rational leader to a weighted total error at most
`epsilon/4` gives a rational value estimate with absolute error at most
`5epsilon/8` from the true optimum. These conclusions require no derivative
bound for the original root response near zero.

## The two separate limitations

The fixed-leader square-root example has affine arguments `a_i/M^2` in
the unit range and upper weights `M`, so its exact value is precisely
`sum_i sqrt(a_i)`. Thus the note correctly avoids claiming polynomial exact
threshold comparison of arbitrary radical sums.

For the growing-power example, writing `s=x^(1/p)` makes the objective
`(s-1/2)^2-1/4`. Suboptimality at most `1/64` forces
`s in [3/8,5/8]`, hence `0<x<=(5/8)^p`. A reduced positive rational
`a/b` in this range has `b>=(8/5)^p`, so explicit rational leader output
requires `Omega(p)` bits. The sparse input has length `O(log p)` and
constant accuracy. This is a valid unconditional output-length obstruction
for the two distinct local powers, and it makes no same-power or value-only
hardness claim.

## Independent diagnostics

[The separate rational recovery checker](../code/bilevel_bounded_power/check_rational_simplex_recovery.py)
passed 12 exact recovery cases up to 100 requested accuracy bits. It uses
a triangle with a degree-four algebraic minimizer and a line-segment cell
with an irrational minimizer; exact integer-square-root comparisons compute
the floors, and all output feasibility and polynomial objective bounds
are verified rationally. This supplements the author's root-approximation
checks and the general proof; it is not a general real-algebraic optimizer.
