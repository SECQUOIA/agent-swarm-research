# Review: exact active-bound recognition and radical-sum comparison

Date: 2026-10-02. Verdict: **PASS for the reduction and stated scope**.
This is an independent actual-file review of
[the construction](../new-direction/convex-active-set-radical-comparison.md).
It does not settle prior attribution or the complexity of Square Root Sum.

The normalization is rational and polynomial in the source encoding.
Taking `K>=max(2,n)` ensures a root even for one radicand; padded zero
signals need no extra leaf variables. All leaf minimizers lie in `[1,2)`,
including a possible lower-bound equality. Their normalized signals
average to the stated root value. The cutoff `B>=2KM` is a valid trivial
YES case, so the remaining parameter `b` is bounded.

The uniform Hessian argument is sound. Each child variable enters only
one parent row, so distinct rows of `P` have disjoint column supports,
even though a variable also indexes its own row. Thus `PP^T<=I/2`.
Leaf second derivatives are at least two, and internal residual squares
supply the remaining rows of `2(I-P)^T(I-P)`. The lower bound `I/8`
is conservative. Adding the root/new-variable cross term changes the
Hessian by a matrix of norm `1/32`, leaving at least `3I/32`.
The asserted growth `1/32` and upper coordinate curvature five follow.

The exact-bound equivalence follows from convex first-order conditions,
including equality in the radical comparison. An optimizer with `y=0`
must minimize the restriction to that face, whose unique optimizer is
the base solution. At that point its inward derivative is precisely
`epsilon(b-s*)`. A negative derivative excludes the face; a nonnegative
one proves global optimality. Padding-only zero internal coordinates and
leaves with `c_i=1` do not invalidate this argument. The upper endpoint
`y=1` is excluded by its strictly positive inward-opposing derivative.

The proposed bags cover every factor and have running intersection.
Maximum bag size three, coefficient magnitude, domain width, degree,
and `L/g` are all bounded independently of source length. This is a
reduction concerning exact active-set information. It is neither an
NP-hardness claim nor an obstruction to convex implicit output: the
constructed problem is already such an output, with a short explicit
convexity proof. Arbitrary-precision evaluation alone does not provide
an exact equality test.

Verification here consisted of reading the complete actual file and
checking its formulas and edge cases symbolically by hand. No numerical
solver, duplicate construction checker, project-wide check, or CI
inspection was run. Any author diagnostic is separate from this review.
