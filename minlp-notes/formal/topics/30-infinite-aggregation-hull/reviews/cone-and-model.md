# Independent semantic review of the hull model and cone tests

Reviewed `HullModel` and `HullCone` in namespace `InfiniteAggregation`.
Targeted machine checks are separate coordinator evidence.

`hullRegion` and `closedRegion` use the actual Euclidean squared norms and
inner product from topic 29. Their strict/weak inequalities agree exactly
with source formulas (7) and (9)'s scalar projection. `weakFeasible` weakens
each original residual, and `mem_weakFeasible_iff` states the three intended
inequalities. None of these candidate regions is defined as a convex hull.

The strict cone test first uses both coordinate multipliers to obtain
positive diagonal slacks. The multiplier `[q,p,2*sqrt(p*q)]` is then
nonzero and lies on the boundary of the rotated cone. Its strict inequality
is precisely the strict square-root condition, after division by a
positive factor. This supplies the source's attained minimum without
assuming that an infimum of strict inequalities is strict.

The weak cone test again obtains both nonnegative slacks. When the required
cross-term `c` is nonpositive, the square-root bound is immediate. For
`c>0`, the proof excludes zero slacks using explicit cone multipliers.
For example, at `p=0` the multiplier
`[(q+1)^2,c^2,2*(q+1)*c]` has zero cone discriminant and evaluates the
slack to `-(q+2)*c^2<0`, contradicting all weak tests. The symmetric case
handles `q=0`. With both slacks positive, the same square-root multiplier
gives the weak bound. Thus no minimizer is incorrectly assumed at a
singular boundary, and the zero-slack cases are covered by finite
separation witnesses instead of a limiting argument.

The translation to actual aggregate residuals uses `aggregate_formula`.
`convexHull_subset_hullRegion` invokes the already proved strict validity
of every nonzero cone multiplier on the actual ordinary convex hull.
Together with the independently reviewed direct decomposition, this gives
the two necessary inclusions for H02. The final all-good equalities must
use topic 29's `good_iff_goodCone`, thereby preserving the source spectral
definition; these wrappers are reviewed in the final consequence review.

No mathematical defect, lost boundary case, or hidden exactness premise
was found in these interfaces.
