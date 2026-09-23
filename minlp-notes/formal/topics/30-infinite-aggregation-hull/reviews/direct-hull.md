# Independent semantic review of the direct hull proof

Reviewed modules: `HullCoreRoots` and `HullCore` in namespace
`InfiniteAggregation`. Machine verification is recorded separately by the
coordinator; this review does not duplicate builds.

The scalar lemma `two_roots_weights` starts from arbitrary real `d` and
positive `k`. The roots `-d±sqrt(d²+k)` have opposite signs and solve
`2*d*t+t²=k`. Its explicit nonnegative weights sum to one and have weighted
root sum zero. The positive denominator follows from `k>0`; there is no
hidden nondegeneracy assumption on `d`.

The vector proof starts with an actual point satisfying all three strict
hull inequalities. Writing `a=sqrt(1-u·u)` and `b=sqrt(1-v·v)`, both are
positive. It chooses `k` strictly between
`max(0,(1/2-u·v)/(a*b))` and one. This interval is nonempty by the strict
scalar hull inequality.

The important dimension step chooses a unit vector `e` perpendicular to
`b*u-a*v`. Such a vector exists already when `r=2`, including when the
weighted difference is zero. It uses the established actual Gram-frame
theorem and does not assume a direction perpendicular to both `u` and `v`.
Consequently `u·e=a*d` and `v·e=b*d` for one real `d`.

For either root `t`, the perturbed pair `(u+t*a*e,v+t*b*e)` has squared
norms `u·u+a²*k` and `v·v+b²*k`, and inner product `u·v+a*b*k`.
The choice `k<1` makes both norm bounds strict; its lower bound makes the
inner-product inequality strict. Both endpoints therefore belong to the
original feasible set, not merely a relaxation. The scalar root weights
recover the original pair exactly. Convexity of the actual convex hull
then proves `hullRegion_subset_convexHull`.

This establishes the sufficiency direction of frozen claim H02 for every
`r≥2`, including four original variables. It uses neither a BDS hull theorem
premise nor an unproved generic exactness assertion. Necessity and the
final equality are reviewed with the cone and consequence interfaces.
No mathematical defect or hidden source-level assumption was found.
