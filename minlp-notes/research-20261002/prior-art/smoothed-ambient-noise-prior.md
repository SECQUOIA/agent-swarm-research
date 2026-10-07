# Prior art for exact QP under ambient coefficient noise

Date: 2026-10-02. This is a focused source comparison for the
[ambient-noise cell-closure theorem](../new-direction/smoothed-ambient-cell-closure.md).
Its new lemmas have now passed [independent review](../reviews/smoothed-ambient-cell-closure-review.md).
This note assesses the closest prior-art boundary and makes no novelty claim.

The candidate asks whether one can globally minimize a fixed rational
indefinite quadratic over a bounded rational polytope after independently
perturbing every original linear coefficient by one fixed finite rational-grid
law. Its negative inertia is `k`. It represents the negative-curvature
coordinates through a convex-QP value function, but the resulting factor
coefficients are dependent because the noise is sampled in the original
coordinates. The proposed expected cell count is

\[
H_{\rm amb}=\prod_{i=1}^k\left(2+
\frac{(1+2k)\alpha\sqrt n\,w_i}{2\sigma}\right),
\]

with `w_i` the auxiliary interval widths. The claim is polynomial in input
size for each fixed `k` when the stated width-to-noise ratios are polynomially
bounded. Its dependence on `k` is not an FPT bound: the factors contain
dimension-dependent terms raised across `k` coordinates. The claimed result
is exact for the sampled objective, including every finite-grid draw, using
the same-draw exponential fallback. It does not promise to optimize the
unperturbed quadratic and has no quadratic-growth assumption.

## Closest smoothed global-optimization precedent

Kelner and Nikolova already give expected-polynomial global optimization
under low-dimensional smoothing. Their Theorem 2.9 treats constant-rank
quasi-concave objectives over integral polytopes and bounds the expected
number of vertices in a randomly perturbed low-dimensional projection. The
perturbation randomly rotates the objective subspace, while the feasible
polytope stays fixed. This is a substantial antecedent for the pattern
“low-dimensional nonconvexity, random perturbation, expected enumeration of
candidate regions.” Its assumptions and guarantee do not directly cover an
arbitrary indefinite quadratic plus independent ambient cost-vector noise:
quasi-concavity, integral vertices, bounded coordinates, and the random
subspace model are substantive restrictions. The theorem also does not state
an exact rational Turing bound for this QP model. [[kelner2007-on-the-hardness-and-smoothed]] p.2-4

Beier and Vöcking supply the nearest independent-objective-noise precedent.
Their generalized isolation bounds and adaptive-precision theorem concern
finite binary feasible sets. The winner gap supports exact certification by
refinement, but a continuous polytope generally has no positive gap between
the optimum and all other feasible points. Their results therefore do not
give a distance-normalized growth bound or an expected count of near-optimal
continuous cells. [[beier2006-typical-properties-of-winners-and]] p.3-4,p.9-10

The existing review of Kelner–Nikolova, Beier–Vöcking, deterministic low
negative-inertia branch-and-bound, and exact fallback is in
[the expected-exact-QP audit](smoothed-exact-qp-prior.md). Those sources
already rule out an unqualified claim that low-rank smoothed global
optimization or random-objective exactness is new. The present candidate's
more specific ingredients are the dependent projection of independent
ambient noise, a cube-section bound, transfer from continuous noise to a
fixed finite grid through bounded one-coordinate event sections, and exact
closure of terminal cells.

## Gaussian-like ambient noise and fixed-parameter complexity

A separate, now-reviewed theorem replaces the uniform ambient grid with a
base-input-chosen finite rational law that approximates independent
isotropic Gaussian coefficients. See the full
[Gaussian cell-closure theorem](../new-direction/smoothed-gaussian-cell-closure.md)
and its [independent review](../reviews/smoothed-gaussian-cell-closure-review.md).
For a rational quadratic over a bounded rational polytope, with the supplied
rational convexifier and negative inertia `k`, it returns an exact rational
optimizer and value for the perturbed objective on every draw. Its expected
bit work is `C_0^k (1+H_G) poly(I)`. The rational spectral normalization
reduces this to

```text
f(k, nu * diam(X) / sigma) * poly(I),
```

with an absolute input-length exponent. This is an expected FPT bound in
negative inertia and the curvature/range-to-noise ratio, stronger than a
fixed-`k` polynomial bound whose input exponent depends on `k`. No growth,
uniqueness, or genericity promise is needed. The result optimizes the sampled
objective; it provides no guarantee for the unperturbed QP. The sampling
law is finite and rational, chosen before the draw, and only approximates a
Gaussian; this is not a Turing algorithm supplied with literal real
Gaussian coefficients.

Kelner and Nikolova are the closest parameterized smoothed-complexity
comparison. Their Theorem 2.9 gives expected time polynomial in the input
dimension, vertex-coordinate bound, and inverse perturbation scale, with
degree depending on the low rank. In parameterized terminology this is an
XP-style bound in rank, not an `f(k) poly(I)` bound. Their model randomly
rotates the low-rank objective subspace over an integral polytope and
optimizes a quasi-concave objective given by an oracle. It does not use
independent ambient cost perturbations, a quadratic objective, or rational
bit-exact output. [[kelner2007-on-the-hardness-and-smoothed]] p.3-4

Burer and Ye's Theorem 3 is a close random-data result for nonconvex
quadratic optimization: under their assumptions, a class of general QCQPs
has a rank-one exact Shor relaxation with probability tending to one when
the number of constraints is polynomial in the dimension. Their model
randomizes the quadratic constraint matrices (with Gaussian eigenvalues),
requires a positive-semidefinite objective matrix and feasibility/interior
conditions, and adds a finite-radius constraint. It does not perturb a
fixed indefinite QP only through independent linear coefficients, and it
states high-probability relaxation exactness rather than expected
fixed-parameter bit work. The theorem locator is Section 4, Theorem 3, in
the 2018 arXiv v2 preprint; the published article and a later correction
are distinct records, so this comparison is explicitly to the preprint
version. [[burer2018-exact-semidefinite-formulations-for-a]] §4, Thm. 3

Deterministic parametric-QP sources establish the critical-region
representation and traversal used in cell closure, but do not supply this
randomized bound. In particular, Patrinos and Sarimveis handle multivalued
convex piecewise-quadratic solution maps and give qualitative
output-sensitive traversal of all full-dimensional critical regions;
their work does not bound the region count or give smoothed expected bit
complexity. Ding's parametric reduction globally minimizes a
piecewise-quadratic envelope for structured indefinite QPs, without an
expected random-cell bound. See the focused
[critical-region audit](smoothed-cell-closure-prior.md).

## Parametric-QP machinery is established

Critical regions and piecewise-quadratic value functions are standard
parametric-QP machinery. In the read explicit-MPC source, Bemporad, Morari,
Dua, and Pistikopoulos derive affine KKT solutions on polyhedral active-set
regions; Theorem 4 and Corollary 1 establish the piecewise-affine optimizer
and convex piecewise-quadratic value for the positive-definite parametric
case. The number of active sets is exponential in the number of constraints,
so this result is a representation theorem and enumeration procedure, not a
smoothed region-count bound. [[bemporad2002-the-explicit-linear-quadratic-regulator]] p.7-12

Literature_grid independently checked the closely related exact adjacency
enumeration of Tøndel, Johansen, and Bemporad (2003; DOI
10.1016/S0005-1098(02)00250-9), the convex possibly non-strict
piecewise-quadratic traversal of Patrinos and Sarimveis (2011; DOI
10.1016/j.automatica.2011.04.003), and the tolerance-based approximate
multiparametric algorithm of Bemporad and Filippi (2006; DOI
10.1007/s10589-006-6447-z). These works provide established terminology and
algorithmic context for critical-region extraction. None of the reviewed
results supplies the candidate's expected near-optimal-cell count under
ambient independent coefficient noise, finite-grid transfer, or global
exactness for a fixed indefinite QP. This paragraph records the independent
reader's verified comparison; it is not a separate full-text review in this
audit.

Katz and Pistikopoulos (2020), DOI 10.1016/j.compchemeng.2020.107057, is a
nearby randomized explicit-MPC paper: it samples parameter space to find
high-volume or practically relevant critical regions. It is a computational
sampling strategy, not a theorem on expected active-region count or exact
global solution of an indefinite QP. The source has been routed to the sole
literature ingester and is not relied on here.

## Scope of the comparison

The prior work establishes nearby pieces separately: low-rank smoothed
global optimization in the quasi-concave/random-subspace setting;
independent noisy objective coefficients with exact adaptive certification
on discrete feasible sets; random-data SDP exactness for a class of QCQPs;
and finite critical-region decompositions for convex parametric QPs. The
ambient Gaussian-like theorem has a more specific guarantee: an expected
FPT bit bound in negative inertia and a numeric conditioning ratio, exact
optimization of each sampled rational objective, and a same-draw exact
fallback. A novelty assessment must distinguish the established region
machinery from the probabilistic complexity bound and must keep the finite
rational noise law explicit. No direct source combining this ambient
noise model with the theorem's exact expected-FPT guarantee was identified
in the focused searches; this is not evidence of novelty.

This is a scoped comparison, not a completeness or priority finding. No
direct prior with the combined ambient-noise, arbitrary-polytope,
indefinite-QP, expected exact rational-output, fixed-parameter guarantee was
identified in the focused searches. That absence is not evidence that no
such result exists. The unread Cen–Xia low-rank nonconvex-QP article remains
a nearby deterministic algorithmic source; no theorem-level comparison is
made unless its full text becomes available.
