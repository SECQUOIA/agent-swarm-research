# Independent semantic review of closure and the original weak system

Reviewed `HullClosure` and `HullClosedConsequences` in namespace
`InfiniteAggregation`. Targeted compilation, axiom auditing, and kernel
replay are separate verification evidence.

The candidate weak region is closed by continuity of its Euclidean
quadratic terms and the real square root. For a weak-region point `x` and
`0≤s<1`, the radial contraction `s*x` has strict norm bounds. Existing Gram
determinant concavity, applied with weights `s²` and `1-s²`, gives

`sqrt((1-s²*u·u)*(1-s²*v·v)) ≥ s²*sqrt(p*q)+(1-s²)`.

Together with the original weak cross-term bound, this yields a strict
margin of at least `(1-s²)/2` above `1/2`. It covers zero slacks and needs
neither division by a slack nor an assumed strictly feasible lift variable.
Letting `s` approach one from below proves the reverse closure inclusion;
closedness supplies the forward inclusion. This is an actual proof of
`closure(hullRegion)=closedRegion`, not a formal replacement of `<` by `≤`.

The original weak system is closed and bounded, hence compact in the
finite-dimensional real pair-vector space. The implementation then uses a
stronger direct fact than compactness of an arbitrary convex hull: the
union of all segments between two weak-feasible points is a continuous
image of the compact product `[0,1]×T×T`, and is therefore compact and
closed. The direct two-point strict decomposition puts every strict-region
point in this segment union. Closure puts the whole weak region in it.
Every such segment lies in the actual ordinary convex hull of `T`.

The other hull inclusion follows from `T⊆closedRegion` and convexity of
the closed region, itself obtained as the closure of the ordinary strict
hull. Consequently `convexHull_weakFeasible_eq_closedRegion` and
`convexHull_weakFeasible_eq_closure_convexHull_feasible` have the required
source-level meanings for all `r≥2`. `isCompact_convexHull_weakFeasible`
also records compactness of the resulting hull.

These interfaces satisfy the substantive closure and weak-system
obligations H05–H06, including the four-variable case. There is no circular
use of SDP exactness or unjustified interchange of hull and closure.
No mathematical or scope defect was found.
