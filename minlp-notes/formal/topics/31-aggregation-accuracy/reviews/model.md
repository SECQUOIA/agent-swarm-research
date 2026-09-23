# Independent semantic review of the Euclidean accuracy model

Reviewed `AccuracyModel` in namespace `InfiniteAggregation`. This review
does not duplicate compilation or the coordinator's package checks.

`EuclideanVar r` is `EuclideanSpace ℝ (Fin r ⊕ Fin r)`, and the coordinate
map places the actual two vectors in the two summands. The proved norm
identity is `||euclidean x||²=qnorm(x.1)+qnorm(x.2)`. Thus the radius of the
product of the unit balls is `sqrt(2)`, and `euclideanDist` is the required
full Euclidean distance. It does not inherit the raw pair/Pi supremum norm.

The review requested an explicit closed-hull transport theorem.
`euclideanEquiv` now gives the actual coordinate map as a continuous linear
equivalence, and `euclidean_closedRegion_eq_closedHull` proves its image is
exactly the Euclidean closure of the Euclidean convex hull of the original
feasible image for every `r≥2`. This closes the topology as well as the
metric correspondence; the target is not merely called a hull by definition.

`relaxation` tests the original aggregate at every member of a finite set
of weights. `admissibleFamily` uses the original spectral-and-validity
`Good` predicate. There is no boundary-ray, normalization, coefficient,
ratio, or boundedness restriction. Positive rescalings are consequently
included in the family quantification. A finite set removes identical
duplicates; distinct positive rescalings can still be present and counted,
which cannot exclude any better description under an at-most budget.

`hausdorffError` is the library's extended Hausdorff distance between the
actual Euclidean images. The target is proved nonempty and compact and is
contained in every admissible relaxation. The unboundedness theorem proves
the error is infinity: finite Hausdorff distance would put every relaxed
point within a finite distance of the bounded target, contradicting
unboundedness. No conversion to a real distance discards infinity.

`optimalError` is a nested infimum in `ℝ≥0∞` over all finite families and
the proof that each is admissible and within budget. The family comparison
and universal lower-bound lemmas follow the correct directions of that
infimum. They neither choose nor assume a minimizing family. The repair
and witness helpers use actual points in the original coordinate sets and
the proved Euclidean distance; both Hausdorff directions are accounted for.

These interfaces satisfy A01–A02. No hidden metric substitution, domain
restriction, or optimal-attainment assumption remains.
