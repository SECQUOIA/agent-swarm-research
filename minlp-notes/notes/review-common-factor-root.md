# Root review of reciprocal-anchor hull results

Date: 2026-09-04. Reviewer: root, independently of both developing agents.
This is an internal mathematical review, not external peer review or a novelty
certification.

Reviewed the complete written statements in
`results/common-factor-reciprocal-anchor-hulls.md` and
`results/common-factor-reciprocal-anchor-full-hull.md`.

## Findings

The small-block theorem, incompatibility example, and rational separating cut
are correct. The two conditional measures have prescribed mass and first
moment; Jensen and the endpoint secant give exactly their attainable inverse
moment intervals. Summing the intervals yields the two-SOC formulation,
including zero-mass boundary cases. Equality in the two weighted Cauchy
inequalities forces the claimed two support points for each leaf. The example's
support sets are disjoint. The four tangent-deficit minima exceed 1/400;
for the smallest listed bound it suffices to square
`sqrt(226)>15+1/40`.

The full anchored-star theorem is correct as written. Its central distribution
argument was independently reconstructed before reading the finished proof:

1. A measure with call function C and mean m supports a leaf (q,w) precisely
   when C(s)>=w-qs and C(s)>=m-w-(1-q)s for every s. The upper-tail threshold
   formula proves sufficiency as well as necessity, including q=0 and q=1.
2. McCormick bounds make the maximum of these affine functions, 0, and m-s a
   valid call function on [a,b]. Its slope jumps define the least feasible
   measure in convex order.
3. The positive second derivative of 1/X implies that this measure minimizes
   the reciprocal moment. The endpoint measure has the maximum reciprocal
   moment and dominates all feasible call functions. Mixing the two measures
   spans the entire interval and preserves feasibility of every leaf.
4. Each leaf can be chosen as a deterministic fractional selection function of
   X; no product of leaf endpoint patterns is needed. This justifies the
   finite constructive decomposition into at most 2n+3 original graph points.
5. Integrating the active affine functions gives exact rational values and
   valid affine cuts. Fixing the incumbent's active intervals produces a
   globally valid supporting cut, because the pointwise maximum at any other
   coordinates dominates the same selected lines. Rational intersection and
   summation bit lengths remain polynomial.

The stated qualifications are necessary: a>0, box-bounded leaves, no additional
original-point product bounds or linking constraints, and a specified exact
rational computational model. The n=0 and a=b cases are handled explicitly.
The number of envelope pieces, support points, and claimed rational arithmetic
operations is consistent with the construction.

No unresolved mathematical issue was found. Convex-order joins, call functions,
and lift-zonoid threshold formulas are established tools; application novelty
must be assessed separately and attributed accurately.
