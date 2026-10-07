# Frontier assessment: exact smoothed optimization and deterministic certificates

Date: 2026-10-02. Updated after the reviewed sparse mixed theorem,
anisotropic Gaussian separable closure, and deterministic geometric
copositivity certificate, together with the earlier smoothed results.
The proposed arbitrary-box-point certificate remains pending here.
This is a significance and next-priority assessment, not a proof review
or a publication-priority determination.

The earlier full-ambient FPT target has been achieved for continuous QP
and for MIQP parameterized also by integer dimension, under the specified
finite rational approximation to Gaussian noise. The
sparse theorem supplies a different advance: expected exact optimization
at fixed width while both negative inertia and integer dimension can grow.
Separable mixed recourse also has an ambient FPT theorem that preserves
its elementary oracle. The deterministic orthant result now gives a
specific compact certificate without trusting a growth constant. That is
progress on unperturbed certification, although it is specialized and
does not solve the general candidate-discovery problem.

## Current proved and pending scope

Here \(k\) denotes negative inertia or supplied concave coupling rank,
\(m\) integer dimension, \(p\) maximum bag size, and \(I\) input length.
Numerical range, curvature, and noise ratios are part of each bound.

| Reviewed result | Strongest conclusion | Main remaining boundary |
|---|---|---|
| [Gaussian-like ambient QP](../new-direction/smoothed-gaussian-cell-closure.md) | Expected \(f(k,1+\nu\operatorname{diam}(X)/\sigma)\operatorname{poly}(I)\) exact bit work on a bounded rational polytope, with independent noise in every original coefficient | A base-chosen finite rational law approximating Gaussian noise; sampled objective; numerical ratio remains a parameter |
| [Gaussian-like ambient MIQP](../new-direction/smoothed-gaussian-miqp.md) | Expected \(f(m,k,1+\nu\operatorname{diam}(\mathcal P)/\sigma)\operatorname{poly}(I)\) exact bit work on a bounded mixed rational polytope | Integer dimension remains a parameter; exact convex-MIQP recourse is charged; the prescribed finite law and sampled objective remain essential |
| [Sparse mixed box QP](../new-direction/sparse-bag-cell-smoothed-miqp.md), including the [continuous case](../new-direction/sparse-bag-cell-smoothed-qp.md) | Exact every draw; expected \(C^p[4+(1+n/2)Lw_{\max}/(2\sigma)]^p\operatorname{poly}(I)\), with arbitrary integer dimension, negative inertia, and variable occurrence | Fixed-width polynomial, not FPT in width; mixed product box; integer ranges enter numerically |
| [General uniform-noise MIQP](../new-direction/smoothed-miqp-cell-closure.md) | Exact every draw on a bounded mixed rational polytope; expected \(f(m)C^k(1+H_{\rm amb})\operatorname{poly}(I)\) | Integer dimension is a parameter; uniform ambient bound retains dimension powers depending on \(k\) |
| [Separable mixed closure](../new-direction/smoothed-mixed-separable-closure.md) | Arbitrarily many integer and continuous coordinates; aligned-noise expected FPT work; uniform ambient expected polynomial work at fixed rank | Product domain, supplied separable convex piecewise-quadratic residual, rational listed knots; ambient bound is not FPT |
| [Anisotropic Gaussian separable closure](../new-direction/anisotropic-gaussian-separable-closure.md) | Expected \(f(k,1+\beta\operatorname{diam}(X)/\sigma)\operatorname{poly}(I)\) exact work under independent original noise, with arbitrary integer dimension | Same separable mixed model; \(\beta=\alpha\|T\|^2\) is supplied concave-term curvature, not intrinsic negative curvature; full row rank after preprocessing |
| [Pure-integer quartics](../new-direction/smoothed-integer-low-rank.md) | Exact expected work on long binary-encoded integer intervals with arbitrary integer dimension and separable convex quartic recourse | All variables integer, product domain, low-rank concave coupling, aligned noise |
| [Aligned QP closure](../new-direction/smoothed-exact-cell-closure.md) | Expected FPT exact bit work for arbitrary bounded rational polytope QP | Perturbations lie in factor coordinates and are generally correlated in the original coordinates |

All these statements prescribe their sampling law from base data before
sampling and solve every draw, including ties. They neither discard hard
draws nor silently use literal real Gaussian inputs. The rational law and
its precision are part of the theorem, not a guarantee for every coarse
atomic approximation.

The Gaussian general-MIQP composition, sparse mixed extension, and
anisotropic separable result all have completed independent reviews.
The deterministic orthant certificate and exact box-preordering
obstruction also passed review; their scope is discussed below.
The [proposed arbitrary-box-point certificate](../new-direction/geometric-box-point-certificate.md)
has a complete draft but is excluded from the proved ranking while its
independent review is pending.

The factor and kernel conditions for general QP are supplied by the
reviewed rational spectral normalization. They are not additional
uniqueness, strict-complementarity, or full-dimensionality promises.
The sparse theorem uses random growth and margin estimates in its proof,
but does not assume or ask the algorithm to verify those properties.

## Which contributions are strongest

The Gaussian-like QP and MIQP theorems give the strongest completed
parameterized complexity statements. They keep independent original-coordinate noise,
general bounded linear feasibility, arbitrary positive curvature, exact
rational output on every draw, and an absolute input exponent. The
weighted count uses the projected feasible set rather than the enlarged
noise-support box. This resolves the ambient-dimension loss in the
earlier cube-volume analysis under a standard continuous proxy.

This does not establish the same FPT guarantee for uniform-cube noise.
The reviewed [ambient count obstruction](../new-direction/ambient-local-count-barrier.md)
shows that the present uniform-noise local and near-optimal node counts
can grow as powers of dimension depending on rank. It does not lower-bound
exact closure runtime or rule out a different uniform-noise algorithm.
Finishing every neighboring noise-law variant is not the most important
remaining task.

The sparse theorem is at least as important for structural scope.
Bounded-width Hessians can have many negative directions, so it covers
instances outside a useful low-inertia regime. Its additional mechanism
is a globally consistent sparse bag-cell whitelist: conditional DP
bounds prune cells while preserving all original optimizers. A retained
bag corner has an actual near-optimal full assignment, allowing original
in-bag noise to bound the number of stored rows. In the mixed extension,
unit integer intervals become singleton cells; retained singleton hulls
fix integer values. Gradient signs are used only on continuous variables,
and convex closure requires all integer coordinates to be fixed. The
expected row bound would not follow merely by running dense grid DP.
The numerical integer-width dependence remains important: this theorem
does not make arbitrarily long binary-encoded intervals cost-free.

For MINLP scope, the mixed extensions address two different obstacles.
General MIQP uses exact convex-MIQP recourse and a gap against every other
integer assignment, computed through \(2m\) exclusion solves. The gap
certifies a whole continuous region; failure near the optimum is controlled
by ordinary integer-label isolation. Separable mixed recourse instead uses
scalar neighbor inequalities, so it avoids a parameter exponential in
integer dimension. The latter has the more elementary and potentially
implementable oracle, but its domain and residual assumptions are much
narrower.

The anisotropic Gaussian extension removes a real restriction rather
than only changing a distribution label. It normalizes a supplied
full-row-rank factor by exact rational rotation and scaling while
preserving the separable residual. Small singular values affect precision,
not the numerical expected-work parameter. This yields ambient FPT with
arbitrarily many integer variables. The parameter is nevertheless
\(\beta=\alpha\|T\|^2\), which can greatly exceed the negative
curvature of the complete objective; replacing it by intrinsic curvature
could destroy separability and is not proved.

The pure-integer quartic theorem remains the clearest completed nonlinear
integer result. Its exactness uses the original objective lattice, not
piecewise-quadratic continuous responses. It is not superseded by the
piecewise-quadratic mixed theorem.

## Prior art and deterministic controls

The [critical-region audit](../prior-art/smoothed-cell-closure-prior.md)
substantially limits formulation-level novelty. Ding already reduces
structured indefinite QPs to global minimization of a piecewise-quadratic
parametric convex-QP value function and recovers original optimizers from
the minimizing fiber. Explicit-MPC and parametric optimization literature
already supply affine KKT responses, polyhedral critical regions, and
region traversal, including multivalued convex recourse. Ding's complete
local primary-source package has now been read.

The strongest candidate contribution is the combination of selective
certified exploration, an expected count independent of refinement depth,
base-chosen finite sampling, and same-draw exact fallback with charged bit
work. The Gaussian weighted count, mixed gap certificate, and sparse
whitelist argument are distinct extensions of that analysis. Integer
isolation, scalar convexity, KKT extraction, and tree DP should not be
presented as newly invented mechanisms.

The [ambient comparison](../prior-art/smoothed-ambient-noise-prior.md)
distinguishes Kelner--Nikolova's rank-dependent smoothed bound under random
subspace rotation and quasi-concavity from the independent linear-noise
QP model. The [sparse comparison](../prior-art/sparse-bag-cell-smoothed-qp-prior.md)
distinguishes exact forest QP, approximate treewidth formulations, and
adaptive continuous messages from the reviewed fixed-width smoothed
theorem. Some status paragraphs in those audits predate the completed
reviews; theorem status here follows the current artifacts and reviews.
These focused comparisons identify a plausible contribution, not priority.

The following controls materially affect claims of solver usefulness:

- Convex QP already has a direct exact algorithm. Coordinatewise-concave
  box QP reduces to endpoint optimization, and bounded-width endpoint DP
  is elementary. Continuous forest QP has a stronger deterministic exact
  baseline without growth or noise.
- For continuous separable piecewise-quadratic recourse, a fixed-rank
  arrangement of the scalar breakpoint hyperplanes gives a deterministic
  polynomial baseline. The expected FPT exponent is still a stronger
  parameterized statement, but this is not a newly tractable fixed-rank
  continuous class.
- Fixed-rank binary versions admit zonotope enumeration. Explicitly listed
  integer labels admit fixed-dimensional Minkowski-sum methods. Long
  binary-encoded integer ranges are where these enumerations can become
  exponential in input length.
- Rank-one ordered-label methods and projected-state DP are useful
  numerical-domain baselines. Monotone scalar responses do not by
  themselves justify binary search for a global auxiliary optimum:
  a reviewed one-dimensional quartic example has exponentially many
  response transitions and suboptimal stationary points.

No simpler deterministic method identified here collapses the complete
arbitrary-polytope low-inertia QP theorem or the arbitrary-width-two
continuous smoothed claim. That is a scoped assessment, not a hardness
claim for each example or a proof against undiscovered algorithms.

## A deterministic certificate milestone, with a narrow target

The reviewed
[geometric copositivity certificate](../new-direction/geometric-copositive-certificate.md)
is a concrete answer for a homogeneous quadratic \(Q=x^TAx\) at the
known orthant corner. If
\(g=\min_{x\ge0,\|x\|=1}Q(x)>0\), it finds a certified margin
\(g/16\le\sigma<g\) without receiving \(g\), in
\(f(p,L/g)\operatorname{poly}(I)\) bit work.
The accepted finite DP tables prove
\[
 Q(x)\ge\sigma\|x\|^2+b\|x\|_\infty^2,\qquad b>0.
\]
Acceptance is sound on every input, independently of the growth promise.
A second DP produces a negative rational witness when \(g<0\);
the two-sided search has the corresponding nonzero-margin bound and
does not generally terminate at \(g=0\).

This is stronger than merely logging a previously completed optimization
run: one normalized shell and a relative rounding correction give the
global inequality directly, with no target accuracy or moving centers.
It is also a short specialization of the existing pruned-grid ideas,
homogeneity, and ordinary finite-state DP. The OR flag avoids separate
anchored solves but is standard finite-state augmentation. Its possible
contribution is the diagonal-curvature/margin parameter, sparse FPT
dependence, and verified unknown-margin output, not the invention of
copositivity tests or geometric grids.

The [focused certificate audit](../prior-art/box-quadratic-jet-certificate-prior.md)
records existing finite-termination simplicial tests, Pólya and Bernstein
certificates, and treewidth approximation methods. Their exact comparison
remains necessary before any priority claim. Finding the origin optimal
in this homogeneous class is a certification problem, not yet a method
for finding an unknown optimizer of a general QP.

The companion [box-preordering obstruction](../new-direction/box-preordering-growth-obstruction.md)
shows why a certificate family must be specified. A positive diagonal
perturbation of the classical Horn matrix has fixed quadratic growth and
no finite exact identity in the full unmultiplied box-slack preordering.
The obstruction survives finite rectangular covers and connected chains
of unbounded dimension at fixed width and conditioning. Its local SPN
jet argument is an explicit application of established copositive
geometry; it is not a general certificate lower bound. A vanishing
Pólya-style multiplier already escapes it, and the geometric DP now
supplies a sparse alternative with a verified margin.

## Compact certificates: valuable, but distinguish three questions

A short rational optimizer is only a feasible upper-bound witness.
KKT conditions alone do not prove global optimality of an indefinite
quadratic. A global certificate must also justify every pruning step or
cover the remaining domain with valid lower bounds and solved regions.

For continuous recourse, much of a self-contained verifier is already
available: rational KKT identities verify inner QP values and critical
regions; refinement records establish coverage; corrected corner bounds
justify pruning; local face solves verify closed-cell minima. In separable
mixed recourse, scalar neighbor and derivative inequalities certify the
inner global responses directly. The sparse theorem already explicitly
records DP recurrences, discarded-cell bounds, gradient signs, a PSD test,
and final convex-QP KKT multipliers.

Consequently, recording the full search trace and observing that its
length is bounded by the work is a useful implementation step but a
largely routine theoretical corollary. Expected work does not imply a
small certificate on every draw: the rare fallback may still be large.
A stronger certificate result would bound a compressed region cover or
proof DAG independently of discarded search effort, and distinguish
verification cost from the cost of discovering it.

General MIQP has an additional issue. An attaining competitor proves an
upper bound on its value, whereas the gap certificate requires a global
lower bound over every exclusion MIQP. Logging an oracle's claimed value
does not make that claim independently checkable. A verifier must either
rerun the \(f(m)\)-time exact oracle or check an explicit integer
optimization proof. Neither ordinary continuous KKT multipliers nor the
winning integer label alone supplies that proof. A claim of an
oracle-free, input-polynomial verifier therefore requires new work.

Universal polynomial-size global-optimality certificates for unrestricted
QP or MIQP are not a reasonable default target. The meaningful target is
an explicit verifier with parameterized or output-sensitive cost in the
stated structural classes, together with honest certificate-size bounds.

## The next priority: certify the original problem efficiently

The most consequential next question is:

**Can a small collection of discovered regions and sparse pruning records
certify a nontrivial unperturbed instance, with substantially less work
than the applicable deterministic baseline?**

This gives a concrete next artifact: a narrow deterministic solver
component that emits a complete global certificate, plus a separate
verifier that checks it without trusting the search strategy or a growth
estimate. Start with continuous QP or separable mixed recourse, whose
inner proofs are explicit. Reuse the existing closure mechanisms; do not
rename logging as a new algorithm. Test rational instances with genuinely
interacting interior decisions, cycles for the sparse case, or dense
negative directions and coupled constraints for the recourse case.
Measure charged oracle work, generated versus certified regions,
certificate bytes, verification time, and exact original-objective output.
Include the deterministic controls above.

The more ambitious theoretical question is whether the work of
**finding** such a certificate can be bounded by a useful geometric or
certificate parameter, without assuming a random objective or a supplied
global growth constant. The orthant theorem settles one homogeneous
known-corner case. The pending box-point extension asks for a certificate
around an arbitrary supplied rational candidate; even a positive result
would still need a separate candidate-discovery argument and an explicit
treatment of nonunique optimal sets. Existing output-sensitive traversal
of all critical regions is a baseline, not an answer about selectively finding
a small global proof. This is a substantially different target from
another composition of the already reviewed smoothing interfaces.

Random perturbations may be useful for proposing active regions, but
every accepted bound must be rechecked for the original objective.
Aligned tilts leave the recourse function fixed and can expose reusable
regions; their pruning decisions still depend on the tilt. Ambient tilts
also change residual recourse. Neither form permits simply relabeling a
perturbed certificate as an original one. No expected-work guarantee for
this proposal-and-verification strategy has been proved here.

A second substantial theory target is a dimension-uniform sparse bound,
such as expected \(f(p,Ls/\sigma)\operatorname{poly}(I)\), or a precise
obstruction. The current sparse bound retains \(n^{O(p)}\), and the
global rounding error drives that loss. This would improve a structural
parameter rather than merely alter the noise law. It remains open in the
reviewed work.

## Limits for unperturbed objectives and general nonlinear MINLP

The sampled objective remains a material boundary. For bounded uniform
noise, an exact perturbed optimizer has original-objective error at most
\(\sigma\sqrt n\,\operatorname{diam}(X)\). The finite Gaussian-like law
also has a bounded support, but its support factor must be included in
any deterministic version of that estimate. The scale parameter
\(\sigma\) alone is not a coordinatewise support bound.

Shrinking uniform noise to obtain original error \(\varepsilon\) makes
the displayed ambient cell estimate behave as \(\varepsilon^{-k}\),
with other data fixed. A complete unperturbed recourse mesh already has
an \(\varepsilon^{-k/2}\)-type bound. Thus the smoothed exact theorem
does not automatically improve worst-case approximation of the original
problem. The [width-two hardness check](../new-direction/sparse-smoothed-hardness-sanity.md)
also gives bounded-coefficient instances with exponentially small exact
decision gaps; useful-scale perturbations can change their threshold
answers. It explains compatibility with that reduction, not a general
smoothed lower bound.

General nonlinear MINLP still lacks the interfaces used here. Nonconvex
constraints can destroy tractable recourse and box rounding. Arbitrarily
many integer variables make general convex MIQP itself difficult.
Continuous nonlinear recourse need not have rational affine responses or
finite polyhedral regions. Even a uniformly conditioned quartic path can
have exponentially large expanded algebraic optimizer representations;
the [output limitation](../geometric-dp/algebraic-output.md) is format
specific and does not rule out compact radical or circuit outputs.

For wider nonlinear models, a certified tolerance and an explicit feasible
witness format may therefore be more useful than an immediate exact
algebraic-output claim. The present separable quartic and piecewise-quadratic
results are meaningful subclasses, not a general MINLP oracle.

This assessment used current local theorem and review files, existing
prior-art audits, and an independent challenge of certificate claims and
deterministic baselines. No solver benchmark, project-wide verification,
CI inspection, new literature search, or knowledge-base edit was performed.

A scoped inline Python check passed trailing whitespace, paired mathematical
delimiters, and local links in this assessment and its two updated pointers.
