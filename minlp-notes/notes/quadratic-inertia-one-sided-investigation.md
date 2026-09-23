# Investigation: one-sided quadratic approximation and inertia

Date: 2026-09-05. Candidate result:
`results/quadratic-inertia-one-sided-integer-complexity.md`.
The parent agent proposed extending the graph rank law to one-sided
approximations. The assigned agent independently checked the construction
and lower bound, wrote the proof, searched the literature, and submitted
it for another independent proof audit.

## Findings and distinctions

The epigraph needs one half of the negative-eigenvalue count times
`log2(1/ε)` auxiliary integer coordinates; the hypograph uses the
positive-eigenvalue count. The lower bound permits arbitrary convex
lifts and unbounded integer coordinates. A binary linear formulation
matches the coefficient while maintaining the required complete
unbounded epigraph or hypograph.

The distinction among graph, epigraph, and hypograph is essential.
The graph must approximate both signs of curvature. In an epigraph,
positive quadratic curvature can be represented directly by convex
constraints, or approximated with zero-binary LP lifts. Only negative
curvature causes the parity midpoint obstruction. The reverse applies
to a hypograph.

A full box allows a small parallelepiped in the negative eigenspace
through any interior point. Restriction to that actual domain slice
produces a strongly concave quadratic with the required dimension.
The lower argument does not assume that a negative-definite principal
minor of order equal to the negative inertia exists; that stronger
coordinate-specific claim would be false in general.

## Targeted primary-source review

The July 2026 preprint by Alberto Del Pia,
[Rational Jacobi Rotations and the Complexity of Approximating Mixed Integer Quadratic Programming](https://arxiv.org/html/2607.29386v1),
Theorem 1 and Section 1, is an important recent comparison. It studies
approximation algorithms under fixed original integer dimension and
negative inertia, including rational arithmetic and earlier spectral
mesh methods. Our proposed assertion is about the minimum number of
auxiliary integer coordinates for a uniform epigraph relaxation.
No algorithmic novelty should be inferred from the known practice of
approximating negative square directions.

The zero-binary square epigraph and binary square hypograph constructions
come from Beach and collaborators' sawtooth formulations. The parity
lower mechanism comes from
[[lubin2022-mixed-integer-convex-representability]] p.11-12.
Strong-concavity diameter bounds and Euclidean isodiametric volume bounds
are classical. The proposed synthesis is an exact leading coefficient
that is necessary across arbitrary convex lifts and sufficient with
compact linear binary lifts.

Searches on 2026-09-05 included:

- negative eigenvalues binary variables quadratic approximation;
- negative eigenvalues mixed-integer convex approximation;
- epigraph integer dimension quadratic;
- quadratic inertia mixed integer relaxation.

These searches identified close upper-construction and algorithmic
antecedents but no matching universal auxiliary-dimension lower theorem.
They do not establish publication priority. Expert comparison with
approximate representability and global quadratic optimization remains
needed before treating the result as new.

## Verification

`code/quadratic_rank/check_one_sided.py` directly constructs the
zero-binary square epigraph LP, with relaxed tooth auxiliaries, at
depths zero through five. Its optimized lower error matches
`2^(-2L-4)` on grids containing the analytic extrema. The square
hypograph interpolant error matches `2^(-2L-2)`. A signed quadratic
combination verifies the direction and weighted error allocation.
All checks passed. The tests support the sourced construction and do
not replace the general proof.

The completed independent audit, including the exact convex-lift product
corollary, is `notes/review-quadratic-inertia-one-sided.md`. The reviewer
reported PASS with no substantive correction.

## Exact product example

The epigraph of `xy` on the unit square has exact optimal convex-lift
error `2^(-2p-2)` with `p` arbitrary integer coordinates. The lower bound
restricts to `x+y=1`. The upper bound uses the identity
`xy=u²-v²+v-1/4`, with `u=(x+y)/2`, `v=(x-y+1)/2`, a direct convex
epigraph for `u²`, and the binary sawtooth hypograph for `v²`. The
hypograph follows by an affine reflection. This corollary also passed
independent review. General exact finite-LP attainment at the threshold
is not claimed (it does hold at zero binaries by McCormick).
