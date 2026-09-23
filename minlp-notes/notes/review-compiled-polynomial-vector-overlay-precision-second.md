# Independent second review: implicit polynomial-vector knot overlays

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Verdict: **PASS** for both complete constructions:

- [Convex-vector overlay](compiled-convex-vector-knot-overlay.md), with
  `p_out<=p_conv+11+ceil(log2 m)`.
- [Arbitrary polynomial-vector overlay](compiled-polynomial-vector-overlay-precision.md),
  with `p_out<=p_conv+12+ceil(log2(sum_j D_j))` over nonlinear outputs.

This is an independent full dependency audit of the convex overlay as well
as the general extension. The scalar hybrid, its certified integration
algorithms, and the arbitrary-polynomial scalar construction were previously
checked in the linked
[hybrid](review-compiled-convex-polynomial-hybrid-precision-second.md) and
[scalar nonconvex](review-nonconvex-polynomial-binary-integer-gap-second.md)
audits. No unproved computation oracle is introduced by the overlay.

## Canonical bisection returns ordered knots

The quantile routine has a fixed root bracket, fixed maximum depth, fixed
accuracy, and a deterministic estimate at every node. Its estimate at a
given midpoint is independent of the target. Thus all targets traverse
one common decision tree. At a node, the target ranges for the left branch,
the midpoint return, and the right branch are ordered by the two thresholds
`Fhat-zeta` and `Fhat+zeta`.

All outputs below a left branch lie on the left of the node midpoint,
and all outputs below a right branch lie on its right. At the final depth
the output is the bracket midpoint; early returns also lie between the
possible left and right outputs. Induction on the finite tree proves
that the returned input is nondecreasing in the target. This argument
does not assume the numerical estimates at different midpoints are
monotone or accurate. Accuracy is needed separately for the mass guarantee,
which was already proved by the scalar construction.

For that induction, canonical evaluation is substantive: the same local
polynomial, midpoint, precision, and deterministic integration algorithm
must be used for all targets. The stated scalar implementation permits
exactly this choice. Padding early returns to a common dyadic precision
does not change values, and forcing the first and last knots to 0 and 1
preserves ordering because every returned interior point lies in the domain.

The greedy branch of the scalar hybrid already gives increasing knots.
For a reflected local interval, the original-coordinate knots are obtained
by reversing the local index order as well as reflecting their values.
For example `a_k=b-(b-a)R_(K-k)` is nondecreasing in `k`. Its endpoints
are the original interval endpoints. Concatenation of successive pieces
identifies their shared endpoint and introduces exactly the sum of their
cell counts, with no extra cells beyond those already counted.

## Source array counts and rational representation

For globally convex output `j`, projection of any admissible vector lift
onto that scalar output preserves exact coverage, its component tolerance,
and the integer count. The scalar hybrid therefore supplies the actual
cell bound `K_j<1458*2^p_conv`; its small-count branch has the stronger
bound `27*2^p_conv`. An affine output can use one cell and also satisfies
the displayed bound, or be imposed exactly without an array.

For an arbitrary polynomial output, the scalar construction first splits
at rational brackets around roots of its second derivative. Each of at
most `2D_j` pieces uses at most `2^(p_conv+11)` cells or a single narrow
bracket cell. Thus its actual concatenated count obeys
`K_j<=4096 D_j*2^p_conv`. This uses the scalar proof's actual cell sum,
not merely its rounded logarithmic count theorem; rounding that theorem
alone would give a weaker constant.

Every array admits polynomial-time indexed knot evaluation. There are
polynomially many rational piece endpoints, even when the local scalar
construction has nested rational normalizations. Mapping those endpoints
back to original coordinates produces rational numbers of polynomial
encoding. Local quantile knots are dyadic before their rational affine
map. Consequently the product of the original-coordinate piece-endpoint
denominators, times `2^Q` for the largest local dyadic precision, is a
common denominator `H` of polynomial bit length for all source input knots.
No product over exponentially many knots is taken.

## Exact implicit order statistics

Merge the right endpoints of every array with multiplicity and prepend one
zero. Their total multiplicity is `K=sum K_j`, so there are exactly `K`
consecutive merged cells, including possible zero-width cells. The final
endpoint is 1. Every noninitial source knot is present; omission of each
redundant initial zero loses no boundary.

For a rational grid threshold `v/H`, binary search in an ordered source
array returns the largest index whose knot is at most the threshold.
Because index zero is not among the right endpoints, this largest index
is exactly the number of counted right endpoints, including repeated
values. Summing over arrays gives the multiset rank count.

For rank `k>=1`, the least integer `v` with count at least `k` is exactly
the numerator of the `k`-th multiset endpoint. The count is monotone in
`v`, so another binary search over `[0,H]` finds this numerator with
`O(log(H+1))` count queries. Duplicate endpoints require no separate
tie rule and no search for the number of distinct knots.

Each count query uses `O(sum_j log(K_j+1))` calls to polynomial-time
source indexed routines. Counts, indices, and `H` have polynomial bit
length. A polynomial number of nested polynomial computations remains
polynomial in the total dense input and tolerance encoding. Nothing is
enumerated in proportion to `K` or the numerical value of `H`.

## Source-cell containment and metadata

Take a positive-width merged cell `[a,b]`. In a given source array, find
the last knot at most `a`. Since `a<b<=1`, that knot has a successor.
The successor is greater than `a`; if it were below `b`, it would itself
appear as an intermediate merged endpoint, a contradiction. Thus `[a,b]`
is contained in that source cell. Searching for the last such index is
important when several source knots equal `a`.

At a repeated merged endpoint, any source cell containing that input
can be used. At input 1 the final source cell always contains it, even
if it is a zero-width cell. The analogous endpoint convention at zero
is harmless. These choices can be made deterministically by bounded
index searches and comparisons.

Each source-cell index retrieves its original piece type: convex, concave,
or a narrow second-derivative root bracket. Reflected local indices can
be mapped back by subtraction from the known local count, and this
requires no new integers. A type selected at a shared boundary is valid
because the resulting cell remains inside the corresponding closed piece.

## Convex-vector error bands

Every source interval in the globally convex case has exact chord gap
between zero and `13epsilon_j/16`. Restricting a convex chord interval
cannot increase that gap: the new chord is no higher than the original
chord at its two endpoints and hence throughout the subinterval. It is
still no lower than the convex graph.

Evaluate the polynomial at the merged rational endpoints and round down
with error at most `epsilon_j/8`. Interpolating those rounded values gives

```
-epsilon_j/8 <= y_j-f_j(x) <=13epsilon_j/16.
```

The stated band `y_j-13epsilon_j/16<=w_j<=y_j+epsilon_j/8` therefore
contains the exact graph and admits only absolute error at most
`15epsilon_j/16`. A zero-width cell is just the same rounding enclosure
at one input. A single common interpolation parameter determines the
input and every output, so coverage is simultaneous vector-graph coverage,
not merely separate coverage by incompatible input choices.

## Arbitrary-output signs and bracket allowance

On a convex or concave source cell, restriction preserves the original
absolute chord-error bound by applying convexity to `f_j` or `-f_j`.
Directed endpoint rounding by at most `epsilon_j/16` yields residuals

```
[-epsilon_j/16,13epsilon_j/16]       for convex cells,
[-13epsilon_j/16,epsilon_j/16]       for concave cells.
```

The convex and reflected concave bands in the candidate contain zero
relative to each such residual and have admitted error at most
`15epsilon_j/16`.

On a narrow bracket, no sign of curvature is needed. Every subinterval
has width at most the original bracket width and the same first-derivative
bound. Its exact chord error is therefore in
`[-epsilon_j/16,epsilon_j/16]`. Downward endpoint rounding contributes
another error in `[-epsilon_j/16,0]`, giving
`y_j-f_j(x) in [-epsilon_j/8,epsilon_j/16]`.
The chosen convex-style band contains the exact graph in this case as
well. Its largest possible negative error is `-15epsilon_j/16`, and
its largest positive error is only `3epsilon_j/16`. Thus the apparently
asymmetric treatment of brackets is valid and has sufficient rounding
slack. Repeated endpoints satisfy the same estimates.

These polynomial evaluations are fresh evaluations at the merged endpoints,
which may come from other outputs. No claim that a merged endpoint was
already a source knot is used. Exact dense rational polynomial evaluation
at a polynomial-bit rational input has polynomial bit cost and output
length, followed by certified directed dyadic rounding.

## Shared-index compilation and final counts

The indexed routine returns the two merged endpoint numerators, all rounded
output values, and any required source-cell type flags. Input knots decode
using the fixed rational denominator `H`. Rounded outputs can use fixed
dyadic denominators and a sufficiently large fixed integer offset to encode
negative values by nonnegative numerators. Such offsets and precisions have
polynomial bit length. The rational band offsets, which depend only on
the selected type and component tolerance, are decoded by linear equations
from the same forced Boolean wires.

Unrolling the deterministic polynomial computation gives the standard
polynomial-size Boolean circuit. Only `ceil(log2 K)` input bits are
declared integral. All internal gate variables are continuous but forced
to their Boolean values by the input bits. Products of endpoint bits
with the common continuous interpolation parameter are exact under the
binary-product inequalities. Type flags and interval localization require
no independent integer selectors. Invalid global cell indices are excluded.

The globally convex arrays give
`K<1458m*2^p_conv`, implying
`ceil(log2 K)<=p_conv+11+ceil(log2 m)`. For the arbitrary polynomial
vector, the actual count gives
`K<=4096(sum_j D_j)*2^p_conv`, implying
`ceil(log2 K)<=p_conv+12+ceil(log2(sum_j D_j))`.
These arguments compare to the unknown optimum only in the proof;
the algorithm computes actual source counts and their sums.

If every output is affine, its entire graph is linear and needs no
integer variable. Otherwise affine outputs can be imposed exactly using
the shared input, without contributing an array or a degree term in the
arbitrary-output bound. All claimed comparisons use componentwise box
errors. No extension to an arbitrary coupled error body is supplied by
this argument.

## Supporting exact checks

Inspected and reran `code/quadratic_rank/check_implicit_knot_overlay.py`.
It passed 2,304 ordered-search comparisons, 60 exact multiset order
statistics, 180 source-cell containments, eight implicit large-grid rank
checks including `2^40` cells, and 99 directed-band checks. The search
examples include a deliberately nonmonotone node oracle, illustrating
that ordering follows from the common tree rather than oracle monotonicity.
All arithmetic in these checks is rational.

The checker supports the ordering, merge, localization, and band mechanisms.
It does not implement the certified curvature integration routines, whose
analytical and bit proofs were audited separately. No mathematical correction
or unresolved encoding dependency was identified in either overlay note.
