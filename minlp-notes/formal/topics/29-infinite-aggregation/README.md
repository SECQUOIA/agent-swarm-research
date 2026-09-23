# Infinite aggregation under hidden hyperplane convexity

Status: complete. All 12 [frozen claims](CLAIMS.md) are proved in 18 Lean
modules, with independent semantic reviews, a warning-free targeted build,
a 248-declaration axiom audit, and successful module kernel replays.

This package addresses the recommended three-inequality construction from
[the infinite aggregation note](../../../results/infinite-quadratic-aggregation-hhc.md).
For every `r≥2`, its variables are `u,v∈R^r` and its strict inequalities are
`u·u<1`, `v·v<1`, and `u·v>1/2`. The package proves actual hidden hyperplane
convexity, exact classification of BDS-good aggregation multipliers, an
uncountable family of indispensable rays for any exact strict description
of the ordinary hull, and impossibility of a finite weak good-aggregation
description of its closed hull. The case `r=2` has four original variables
and is part of the required scope.

The [source inventory](SOURCE-REVIEW.md) fixes the meaning of good aggregation,
its spectral condition, and the distinction between the ordinary and closed
hulls. Good multipliers must be derived from the original homogeneous
matrix and hull-containment definition, not defined to be the proposed
rotated quadratic cone. Hyperplane convexity must likewise be proved from
the actual quadratic map.

The full hull formula, finite lifted formulation, countable sufficiency for
the closed hull, obstruction to arbitrary quadratic descriptions, quantitative
approximation, and a general Gram-map theorem are outside this package.
The package does not assert a numerical solver or complexity result, or
establish literature priority.

The completed [certificate core](../27-quadratic-aggregation/README.md) and
[consequences](../28-quadratic-aggregation-consequences/README.md) remain
separate packages. The [declaration map](COVERAGE.md), [independent reviews](REVIEW.md),
and [verification record](VERIFICATION.md) give the exact evidence. No
project-wide checks or CI inspection were run.

The related [paper supplement](../../../paper-quadratic-aggregation/formal-infinite-aggregation.tex)
and [formal account](../../../paper-quadratic-aggregation/sections/92-formal-infinite-aggregation.tex)
state these results and their limits. The two-page supplement builds cleanly;
it does not replace the concurrent main manuscript's separate staged review.

Public results include `hhc`, `good_iff_goodCone`,
`good_strict_description_contains_rays`,
`good_strict_description_uncountable_rays`,
`no_countable_good_strict_description`, and
`no_finite_good_closed_description` in namespace `InfiniteAggregation`.
The cardinality result concerns distinct scale-normalized rays, and the
closed result concerns exactly `closure(convexHull S)`.
