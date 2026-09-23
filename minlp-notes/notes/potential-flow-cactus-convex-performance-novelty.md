# Cactus convex performance: paired source assessment

Date: 2026-09-05. Candidates:
[coupled convex hardness](potential-flow-cactus-convex-performance-hardness.md)
and [few-measurement maximization](potential-flow-cactus-few-measurement-maximization.md).
This is a bounded source assessment; independent mathematical audits were
assigned separately.

Both core optimization mechanisms are known. The hardness result realizes
the classical Max-Cut quadratic on an explicitly bounded passive cactus.
The positive result applies classical fixed-dimensional zonotope enumeration
with a bit-precision implementation that handles algebraic cycle lengths
and returns an allowed rational resistance scenario. No matching combined
passive-network statements were located. These are useful supporting
boundaries, with modest and qualified novelty.

## Convex maximization hardness

Alberto Del Pia, Santanu S. Dey, and Marco Molinaro, *Mixed-integer Quadratic
Programming is in NP*, arXiv:1407.4798, Section 1.1, Corollary 2, PDF p.2,
explicitly gives the familiar binary Max-Cut objective
`sum_(ij) (z_i+z_j-2z_i z_j)` and recalls its NP-completeness. This passage
was reopened and read. On binary points it equals
`sum_(ij) (z_i-z_j)^2`; extending the latter to a cube gives a convex
quadratic. These facts establish the standard combinatorial ingredient.
[Primary manuscript](https://arxiv.org/pdf/1407.4798).

The candidate's network-specific step is a triangle whose direct flow runs
over `[1/3,2/3]` as its resistance runs over `[1,16]`, with fixed alternate
path resistance four. Independent triangles then realize a rational cube.
This physical encoding preserves constant resistance and nomination data,
and the objective equals the cut size exactly at endpoints. Once that
encoding is verified, strong hardness and the fixed absolute gap follow
directly from unweighted Max-Cut. The hardness mechanism is not new.

The scope is nevertheless useful: the physical graph is a cactus of degree
at most three, while the comparisons in the objective may connect arbitrary
pairs of cycle flows. Thus complexity comes from objective coupling rather
than complicated physical topology. Endpoint attainment does not imply an
efficient endpoint search for an arbitrary convex objective.

The restricted family has rational endpoint flows and integer objective
values, so its NP/coNP membership is elementary. This does not justify
membership for arbitrary coupled performance polynomials evaluated on
independent quadratic algebraic flows. Also, constant absolute error before
objective normalization is the stated barrier; normalization to `[0,1]`
changes its size. No further approximation claim is assessed here.

## Fixed-dimensional zonotope enumeration is directly established

Shmuel Onn and Uriel Rothblum, *Convex Combinatorial Optimization*,
arXiv:math/0309083, Lemmas 2.1–2.3, PDF p.4, gives the polynomial vertex bound,
enumeration with exposing functionals, and normal-fan refinement using edge
directions. Algorithm 2.5 and Theorem 2.6, PDF pp.5–6, reduce a
fixed-dimensional convex objective to polynomially many linear optimization
queries and objective evaluations. The discussion on PDF p.8 explicitly
extends that algorithm to real data in a real-arithmetic model. These
passages were independently read here.
[Primary preprint](https://arxiv.org/pdf/math/0309083).

Our comparison: this is the direct general antecedent to the candidate.
Using the rational vectors `R Z_C` to enumerate normal sign cones is an
application of its edge-direction principle. Positive algebraic generator
lengths do not change those hyperplanes, so algebraic lengths do not create
a new geometric theorem. Zero-length generators merely refine a redundant
arrangement. The candidate's work is in supplying an explicit rational
implementation and the needed flow-scenario and numerical guarantees.

An additional direct predecessor is J.-A. Ferrez, K. Fukuda, and Th. M.
Liebling, *Solving the fixed rank convex quadratic maximization in binary
variables by a parallel zonotope construction algorithm*, European Journal
of Operational Research 166(1), 35–50 (2005), DOI
10.1016/j.ejor.2003.04.011. The primary publisher abstract and indexed
introduction explicitly reduce positive-semidefinite fixed-rank binary
quadratic maximization to zonotope vertices and hyperplane-arrangement
enumeration. They credit an earlier polynomial case of Allemand et al.
The full-text retrieval attempts from the publisher and CiteSeer failed;
this audit relies only on those identified primary excerpts.
[Publisher record](https://www.sciencedirect.com/science/article/pii/S0377221704003352).

The earlier source identified there is K. Allemand, K. Fukuda, T. M.
Liebling, and E. Steiner, *A polynomial case of unconstrained zero-one
quadratic optimization*, Mathematical Programming 91(1), 49–52 (2001).
It was not independently read in this bounded pass. Cite Ferrez–Fukuda–
Liebling's explicit attribution if using this historical priority point,
and retrieve the original before making a detailed theorem comparison.

Consequently, neither fixed-rank convex quadratic tractability on a box nor
fixed-dimensional convex maximization by zonotope enumeration is a new
algorithmic mechanism. Both should be credited prominently, including in
the quadratic specialization of the candidate.

## What the flow algorithm adds

For a cactus, each scalar circulation bound has a separate quadratic
algebraic encoding, and an exact rational resistance endpoint scenario
realizing it is available. The candidate uses rational normal directions
to construct polynomially many such original scenarios. It then encloses
the cycle roots and evaluates a densely encoded convex polynomial to
sufficient additive accuracy. This avoids exact comparison in the common
field of all cycle radicals.

That distinction matters: an exact evaluation oracle from a combinatorial
optimization theorem is not automatically a polynomial-bit implementation
for algebraic physical values. The proposed result returns a rational
scenario with an additive objective guarantee. It does not promise the
exact best candidate when comparing independent radical sums would be
required. The separate
[cactus flow-region assessment](potential-flow-cactus-flow-region-and-optimization-novelty.md)
documents that arithmetic issue and the older circuit-tolerance sources.

Fixed measurement dimension is essential to the enumeration bound. The
stated complexity is `N^{O(k)}`, not fixed-parameter tractability in `k`.
Dense polynomial encoding is also substantive: it bounds derivative
estimates and rational evaluation cost polynomially in the input. A sparse
polynomial with binary-encoded exponents is outside this guarantee.
Convexity is promised, not tested by a newly claimed algorithm.

Finite resistance sets cause no new geometric obstacle for convex
maximization because the required circulation endpoints are themselves
attainable and the finite flow set has the same convex hull as its interval
relaxation. This does not imply a finite-resistance convex-minimization
algorithm or easy target matching.

Recommended wording: “The cactus flow representation transfers classical
convex-maximization boundaries to passive networks: bounded physical data
already realize Max-Cut under coupled quadratic performance, while a fixed
number of linear measurements permits a zonotope-based additive endpoint-
scenario algorithm. The latter implements the classical enumeration method
using rational directions and separately approximated algebraic flows.”

Fresh searches covered convex quadratic box maximization, Max-Cut,
fixed-rank binary optimization, zonotope and hyperplane-arrangement
enumeration, and convex performance in uncertain cactus networks. No
equivalent passive-network scope was found. This is a bounded comparison,
not exhaustive novelty clearance, and does not supersede proof review.
