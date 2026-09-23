# Exact hull and SDP representation of the infinite-aggregation example

Status: complete. All eight [frozen claims](CLAIMS.md) are proved in ten
new modules. Independent semantic review, warning-free targeted builds,
the 93-declaration axiom audit, and all ten kernel replays passed. See
[VERIFICATION.md](VERIFICATION.md) for commands and evidence.

For every integer `r≥2`, let `S` be the set of pairs `u,v∈R^r` satisfying
`u·u<1`, `v·v<1`, and `u·v>1/2`. This package proves its ordinary convex
hull, the closure of that hull, finite strict and weak SDP representations,
and equality of the closed hull with the hull of the original weak system.
The four-variable case `r=2` is required.

The package also identifies the ordinary and closed hulls with the
intersections of all strict and weak good aggregations, respectively. Here
“good” means the original spectral and hull-containment predicate from
[topic 29](../29-infinite-aggregation/README.md), not a newly defined cone.
The existing cone classification may be reused.

The [source inventory](SOURCE-REVIEW.md) records the exact formulas and the
main proof obligation: hull sufficiency must be proved, including `r=2`,
without assuming a BDS hull theorem as a new premise. The [coverage map](COVERAGE.md)
and [review record](REVIEW.md) map all obligations to the actual proved
interfaces, including a direct two-point sufficiency proof for `r≥2`.

The user selected the earlier two-package recommendation: this hull package,
then finite-aggregation accuracy. Accuracy bounds, coefficient bit bounds,
arbitrary-quadratic impossibility, countable closed-family sufficiency,
single-objective claims, and the general sharp Gram-map theorem are outside
this package. Topics 27–29 remain separate completed packages.

The [paper supplement](../../../paper-quadratic-aggregation/formal-exact-hull.tex)
and [formal account](../../../paper-quadratic-aggregation/sections/93-formal-exact-hull.tex)
record the verified results. The supplement builds cleanly to two pages.
