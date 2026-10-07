# Prior-art audit: core-only smoothing for convex-recourse value output

Date: 2026-10-02. This focused comparison concerns the reviewed
[core-only-noise value-oracle theorem](../new-direction/core-only-noise-value-oracle.md).
It compares the result with low-dimensional smoothed global optimization,
semiconcave cell counting, random-tilt growth, and parametric convex
optimization. It is not a completeness or publication-priority claim.

## Candidate claim and output contract

The input is a fixed-degree rational polynomial `F0(v,z)` on a product box,
where the supplied core has dimension `k=1` or `2`. The diagonal core
curvatures have certified upper bound `L`, and the residual Hessian block is
certified positive semidefinite throughout the box. Independent linear noise
is applied only to the core coordinates, from one finite rational grid
chosen from the base input before sampling. For every draw and every requested
precision `q`, the algorithm returns a feasible rational point and a
certified interval of width at most `2^-q` containing the sampled instance's
global optimal value. The expected bit work is
`(1+L/sigma) poly_d(I+q)`. A single random work factor controls all q; the
noise law is not refined as q increases.

This is a value-output guarantee. The feasible point is within `2^-q` in
objective value, but the theorem does not promise that its coordinates
approach a selected optimizer. The residual optimizer may be nonunique, and
no residual strong-convexity or growth constant is assumed or supplied. The
finite grid can place positive mass on bad-growth or tied instances; the
algorithm remains correct there by using an exact same-draw fallback. The
expected bound, rather than a per-draw polynomial bound, pays for that branch.
The candidate's proof has a fresh actual-file review; this note addresses
prior art, not the proof review.

## Closest external algorithmic precedent: low-rank quasi-concave smoothing

Kelner and Nikolova's FOCS 2007 result is the closest checked external
precedent for expected global optimization under a low-dimensional
nonconvexity measure. Their Theorem 2.9 gives an expected polynomial-time
algorithm for minimizing a `rho`-perturbation of a constant-rank
quasi-concave function on an integral polytope with bounded integer vertex
coordinates and polynomially many facets. The perturbation randomly rotates
the objective's low-rank subspace. The algorithm enumerates vertices of a
projected-polytope shadow, whose expected size is bounded in Lemma 2.10.
This already establishes that low-dimensional global nonconvexity and
smoothed expected optimization are not new ideas.

The model and guarantee differ in ways that matter here. Kelner–Nikolova
perturb the objective subspace by a random rotation and work over an
integral polytope; the candidate adds independent finite-grid linear
coefficients to one or two continuous core coordinates and leaves a dense
convex polynomial recourse problem. The former bounds a projected vertex
count and gives expected smoothed minimization; it does not state an exact
rational Turing Cauchy-value oracle that remains valid for every draw and
all requested q under one fixed finite law. The candidate also returns a
feasible point, but only certifies its value gap, not its distance to the
optimal set. See the original
[Kelner–Nikolova paper](https://users.ece.utexas.edu/~nikolova/papers/QuasiConcave.pdf),
Theorem 2.9 and Lemma 2.10; the inspected local primary text is
[`fulltext.md`](../../literature/papers/kelner2007-on-the-hardness-and-smoothed/fulltext.md).

## Closest algorithmic mechanism: semiconcave grid-cell counts

The project's separate
[smoothed semiconcave cell-count result](../new-direction/smoothed-semiconcave-cells.md)
is the closest methodological antecedent. It bounds, at each grid level,
the expected number of near-optimal grid points from adjacent-point
comparisons under independent random linear coefficients. A corrected-corner
branch-and-bound algorithm then has an expected cell count per level that
does not grow as the mesh is refined. It assumes only an upper coordinate
curvature bound, not convexity, differentiability, uniqueness, or quadratic
growth.

That result uses a finite perturbation grid whose size is chosen using the
target accuracy level. Its theorem therefore does not give one fixed
finite-bit noise law that supports arbitrarily fine later queries. It also
uses its stated arithmetic-oracle model and does not provide the current
candidate's exact convex-recourse tangent certificates plus a same-instance
bit-complexity fallback. In the candidate, the projected value function is
semiconcave, but the expected work is controlled differently: a
distance-normalized growth tail is transferred uniformly to a sufficiently
fine finite noise law, and a per-level cap bounds all accuracies at once.
The ordinary branch gives sound value intervals without assuming the random
growth event; the tail is used only to charge the fallback and total work.

The finite-law growth transfer builds on the project's separate
[random-tilt growth-tail result](../new-direction/proximal-growth-tail.md)
and [finite-section transfer](../new-direction/polynomial-finite-noise-tails.md).
The first gives a continuous-noise tail for global quadratic growth of an
arbitrary continuous objective on a compact set; the second transfers it to
a base-chosen finite rational grid using a semialgebraic section-count
bound. These are ingredients of the current proof, not external precedents.
The closest established discrete comparison is Beier–Vöcking's winner-gap
isolation for finite binary feasible sets. A second-best value gap on a
finite set is not a growth modulus for a continuous value function; see the
existing [growth-tail audit](proximal-growth-tail-prior.md) for the exact
scope distinction.

## Convex recourse and parametric optimization are established components

For each fixed rational core point, the residual problem is ordinary convex
polynomial minimization on a rational box. The candidate uses standard
rational convex optimization to produce a feasible residual point and a
certified lower/upper value interval, including a tangent lower certificate.
This does not require residual strong convexity. The project records the
underlying weak-optimization interface in
[convex-patch-evaluation.md](../new-direction/convex-patch-evaluation.md)
and the broader polynomial recourse comparison in
[smoothed-polynomial-box-recourse-prior.md](smoothed-polynomial-box-recourse-prior.md).
The value-oracle construction is therefore not a new convex optimization
algorithm.

Classical parametric convex optimization supplies further context. Patrinos
and Sarimveis, in “Convex Parametric Piecewise Quadratic Optimization:
Theory and Algorithms,” *Automatica* 47(8) (2011), Proposition 5 and
Theorems 1 and 6, show that convex piecewise-quadratic parametric problems
have piecewise-quadratic value functions and give graph traversal of
full-dimensional critical regions, including when the optimizer map is
set-valued. The method is described as output-sensitive, but the paper does
not bound the number of regions in general. It is restricted to convex
piecewise-quadratic data. The candidate does not enumerate residual active
sets or construct a piecewise description of the value function; it queries
certified values on core-grid corners and uses convex recourse directly.
The checked primary text is the [author-hosted report](https://www.chemeng.ntua.gr/labs/control_lab/zipfiles/TR2010-01.pdf),
which matches the journal article [DOI 10.1016/j.automatica.2011.04.003](https://doi.org/10.1016/j.automatica.2011.04.003);
precise assumptions and locators are recorded in the project's
[strongly-convex recourse audit](core-only-noise-boundary-recourse-prior.md).

## Relation to nearby smoothing results

Two adjacent project results set useful boundaries. The
[strongly-convex residual theorem](../new-direction/core-only-noise-boundary-recourse.md)
perturbs only core coefficients and can return an exact implicit optimizer
for any core size, but it assumes a certified uniform residual modulus and
uses that modulus in its polynomial bit threshold. The present value theorem
removes that residual modulus and accepts nonunique recourse optimizers, at
the cost of restricting the noisy core to one or two coordinates and
returning objective accuracy rather than optimizer-distance accuracy.

Conversely, the [full-ambient polynomial recourse theorem](../new-direction/smoothed-polynomial-box-recourse.md)
handles any supplied core size and returns exact implicit optimization on
every draw without growth or uniqueness promises, but it perturbs all
original linear coefficients. The present result makes a materially
different smoothing promise: only the core coefficients are randomized.

## Assessment and limits

The checked literature already has strong pieces of the picture: expected
smoothed global optimization for low-rank quasi-concave objectives, expected
near-optimal cell counts under random tilts, qualitative and quantitative
random-tilt growth results in related settings, convex polynomial recourse,
and explicit critical-region methods for parametric quadratic programs.
The candidate's most specific comparison point is the combination of
core-only finite rational noise, arbitrary convex polynomial recourse with
possible ties and flat fibers, one law for all requested value precisions,
certified feasible/value output on every draw, and expected bit work for
`k<=2` obtained by integrating a capped growth tail and charging exact
same-draw fallback.

This is a bounded assessment rather than a novelty claim. No source checked
here states that exact combination, but failed searches do not establish
absence. The result does not claim exact algebraic optimizer output, an
optimizer-distance bound, deterministic polynomial work on every noise
draw, or an all-dimension finite-noise theorem. The proof's `k<=2` boundary
comes from the integrability of its truncated growth moment; it is not a
hardness result for larger core dimension.

## Sources and access

- Kelner and Nikolova, “On the Hardness and Smoothed Complexity of
  Quasi-Concave Minimization,” FOCS 2007, Theorem 2.9 and Lemma 2.10; read
  primary text in the local source package linked above.
- The related semiconcave-cell, growth-tail, finite-section, and convex
  recourse notes are local project results linked in the comparison; they
  are not external prior art.
- Primary sources for discrete winner-gap isolation and parametric convex
  QP are already checked in the local packages cited by the linked audits.

The targeted search looked for smoothed semiconcave/global value
optimization under additive linear tilts and low-dimensional continuous
nonconvexity, including alternate terms such as quasi-concave minimization,
low-rank nonconvexity, parametric value functions, and expected near-optimal
cell counts. It did not identify a closer external theorem than
Kelner–Nikolova. No new source or full-text retrieval is needed for this
scoped audit, so nothing was routed for literature ingestion. No KB or index
files were changed.
