# Second independent audit of convex-vector curvature-rank precision

Date: 2026-09-05. Verdict: PASS on the complete finite and constructive
theorems in [the candidate](convex-vector-curvature-rank-precision.md).

I checked every proof step and constant independently. No correction is
required. The scalar compiler remains the explicitly imported reviewed
dependency; no additional approximation or real-arithmetic oracle is used.

## Finite comparison

In the finite-dimensional quotient by affine functions, maximum absolute
determinant among original output rows gives representation coefficients of
magnitude at most one by the single-row replacement identity. The important
point is that the basis consists of original convex outputs: their chord
gaps are nonnegative. Hence signed representation coefficients still imply
`0<=g_j<=sum g_basis`. An arbitrary algebraic basis would not justify this.

For each parity group, exact graph witnesses approaching its hull endpoints
give midpoint gaps at most one in every normalized component. The limit is
only in continuous projected quantities and closed scalar error inequalities,
so no closedness or boundedness assumption on the lifted witnesses is needed.
The chosen sum has midpoint gap at most `r` and full gap at most `2r`.

The level-cut lemma is valid also with plateaus: concavity makes superlevel
sets intervals; successive levels partition both sides into portions whose
original gap range is at most the level spacing. The new local gap subtracts
the affine interpolation of the endpoint gaps, so it is bounded by that range.
The central interval subtracts the last retained level. With maximum `2r`
and spacing one, there are at most `4r-1` intervals. The resulting downward
component chord bands contain the exact graph and permit only unit error.
Counting a binary disjunction proves the finite formula.

## Rational basis construction

Selecting independent columns preserves all row relations. In a row-basis
exchange, a coefficient exceeding two in magnitude multiplies the absolute
determinant by more than two. Because every basis remains a submatrix of the
fixed input matrix, the stated rational height bounds give a polynomial
number of exchanges and polynomial bit lengths throughout. Choosing a row
already present cannot trigger an invalid exchange: its representation has
only zero and one entries.

This procedure yields coefficients bounded by two without computing a global
maximum determinant. The selected normalized convex outputs remain rational
dense polynomials of polynomial total encoding, and their sum is nonaffine
for positive rank. The target component gaps are therefore bounded by twice
the scalar sum gap.

With spacing `1/2` and parity-hull gap at most `2r`, the exact level lemma
uses `8r-1` intervals per parity. A finite covering of the compact input
interval by admissible intervals can be replaced by a partition with no more
cells: extend from the current endpoint using a covering interval reaching
farthest right, and restrict to the part traversed. No selected interval
needs to be reused. This confirms `N_(1/2)<= (8r-1)2^p`.

## Compiled vector graph and constants

The scalar compiler supplies at most `486 N_(1/2)` cells with exact sum
chord gap at most `13/32`. Every target gap is at most `13/16`. Downward
endpoint rounding by at most `1/8` gives `y-G` between `-1/8` and `13/16`.
The proposed band includes zero error and has maximum absolute admitted
error `15/16`. The same input segment and interpolation weight are used for
all components, which is essential for simultaneous graph containment.
Reversing or repeated scalar knots do not invalidate any interval inequality
or the complete input coverage argument.

Evaluating additional dense polynomials at rational indexed knots is a
polynomial-bit computation. Continuous Boolean wires and exact products with
the interpolation weight add no declared integer variables. Normalization
by rational tolerances and final output rescaling preserve polynomial bit
length. The cell-count estimate is
`486(8r-1)2^p<3888r2^p<4096r2^p`, which proves the stated
`p+12+ceil(log2 r)` upper bound. The algorithm does not require access to
the comparator lift or its unknown optimum count.

The rank-zero case, variable degree and output count, one-input restriction,
and absence of a claimed necessary rank overhead are correctly stated.
