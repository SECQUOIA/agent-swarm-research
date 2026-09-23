# Source inventory for the exact hull and SDP package

The authorized source is Sections 4–5 of
[the infinite-aggregation note](../../../results/infinite-quadratic-aggregation-hhc.md).
The user's clarification selects exact hull/SDP first, then
aggregation-accuracy bounds. It does not select a different research topic.
The [frozen claims](CLAIMS.md) include all conclusions in the recommended
exact-hull package and their required strict/weak aggregation identifications.

The source uses the same three inequalities and Euclidean pair-vector
variables as completed topic 29. Its formula (7) states the ordinary hull
using positive ball slacks and `u·v+sqrt(p*q)>1/2`. Formula (9) states a
single affine PSD lift for its closure. The source additionally states the
strict positive-definite lift and equality with the convex hull of the
original weak system. These are distinct obligations, not interchangeable
notations for one unproved assertion.

At scope freeze, the source obtained the all-dimensional hull formula
through BDS and offered a direct two-point proof only for `r≥3`. The
implemented proof now supplies a direct two-point construction for every
`r≥2`, and the source note records this stronger elementary argument.
Reusing topic 29's HHC and exact good-cone classification would not by
itself supply the missing hull theorem; the direct construction discharges
that obligation without assuming a general BDS result.

The strict cone calculation relies on positive diagonal slacks: the
infimum of `tau*p+q/tau` is attained at a positive parameter. The weak
calculation must also cover zero slacks, when the infimum may only be
approached as `tau` tends to zero or infinity. Coordinate multipliers
enforce the separate diagonal inequalities. The original good predicate
must be connected through the proved topic 29 classification.

For the lift, the Schur complement is
`[[p,sigma-u·v],[sigma-u·v,q]]`. Its PSD criterion includes `p,q≥0` and
`(sigma-u·v)^2≤p*q`; its PD criterion is strict. Existence of the scalar
`sigma`, with the correct strict or weak lower bound, must be established.
The source's closure argument mixes any weak lifted point with the origin
using the positive-definite lifted witness at `sigma=1/2`. The resulting
point satisfies the strict hull formula even though this particular lift
parameter may equal `1/2`; obtaining the strict lift uses a further small
increase in `sigma` or the proved strict scalar equivalence.

Equality with the hull of the original weak system uses compactness of the
weak system and its convex hull, together with the two containment
directions. No generic assertion that weak feasibility is the closure of
strict feasibility is needed or assumed.

The quartic irreducibility and arbitrary-quadratic obstruction in Section 4
are excluded. Section 5's PDLC observation, accuracy discussion, and
single-objective results are also excluded here. Countable dense-family
sufficiency from Section 3 and literature-priority claims are not required.
Accuracy is the separately authorized next package. No numerical solver or
computational speedup claim is part of this verification.
