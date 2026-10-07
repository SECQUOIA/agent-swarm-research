# Structured and smoothed exact nonconvex optimization

Date: 2026-10-02. This program is paused at the user's request after finishing
the current ideas and extensions. The [closeout](CLOSEOUT.md) states the final
contributions and unresolved limits. Mathematical reviews and literature
comparison are separate; no claim of publication priority or competitive
solver performance is established.

The final point-output advance is the reviewed
[globally convex polynomial theorem](new-direction/globally-convex-polynomial-point-oracle.md).
At fixed degree it computes a polynomial-bit distance error constant and
a deterministic Cauchy name for the minimum-norm optimizer on a bounded
rational polytope. Unlike the cubic theorem below, it requires convexity
on all of Euclidean space. A global Jensen argument controls rational
gradient-sample residuals; unisolvence identifies the optimizer's affine
slice, and an integer-row Hoffman estimate makes the constant effective.
Its selected-core completion also gives full optimizer coordinates under
the inherited finite core-noise law when the supplied convexifier is
globally convex. An explicit sum of positive even powers of rational
affine forms plus a PSD quadratic is a
[verifiable application class](new-direction/affine-power-core-point-oracle.md).
The [source audit](prior-art/globally-convex-polynomial-point-prior.md)
distinguishes this effective result from qualitative global-convex error
bounds, ordinary weak value optimization and exact convex QP.

## The contribution being developed

The reviewed [sparse polynomial theorem](new-direction/smoothed-sparse-polynomial.md)
now gives exact optimization for explicit fixed-degree polynomial factors
on mixed boxes under a specified finite law of independent linear noise.
Its expected bit work is
`C^p [4+(1+n/2)L w_max/(2sigma)]^p poly_d(I)`, with no supplied growth,
uniqueness, integer-dimension, or boundary-Hessian assumption. The law
is chosen from the base input using polynomially many bits. Sparse
pruning fixes integers and active bounds, then certifies a strongly
convex continuous subproblem defining the exact optimizer. A same-draw
algebraic fallback covers ties and degeneracies.

This exact implicit output has a useful computational contract: a
successful patch's descriptor has polynomial size and supports certified
position and value evaluation in `poly_d(I+q)` work. The complete global
pruning certificate has an expected-size bound; it need not be small on
every successful sample. Exceptional algebraic outputs may be large,
but their expected construction and evaluation costs are controlled.
The result is fixed-width polynomial under the displayed numerical
scales, not FPT in width or polynomial in encoded integer widths alone.
The [prior-art audit](prior-art/sparse-smoothed-polynomial-prior.md)
already places qualitative generic global growth, including mixed boxes,
in prior work. The candidate contribution is the finite-law expected
exact-work theorem and its output contract. Competitive solver performance
and publication priority remain open.

The independent [significance assessment](new-direction/smoothed-sparse-polynomial-significance.md)
finds the main gain in nonlinear continuous discovery and exact closure,
including boundary optima. The noise need not dominate the objective:
bounded local factors on `[-1,1]^n` with fixed width and occurrence admit
constant `L`; choosing `sigma=n^-2` keeps the expected bound polynomial
at fixed width while changing any objective comparison by at most `2/n`.
This is a scaling consequence, not evidence of practical speedup or
hardness of that subclass. The complete sampler, fallback, and certified
evaluator have not been implemented or benchmarked.

The next width improvement requires a different mechanism. The reviewed
[global-error construction](new-direction/global-error-cell-barrier.md)
forces `(5n/(6p))^(p/2)` retained cells for the actual current algorithm,
uniformly over its noise support. This closes the possibility that its
`n^p` dependence is solely a loose analysis. The construction is easy by
endpoint DP, so it does not establish a lower bound for sparse optimization.
The [conditional-recourse interface](new-direction/local-error-recourse-interface.md)
would replace the global dimension in the expected count by bag size, but
requires certified optimization over the outside variables. A star quadratic
proves that existing grid messages do not supply that local accuracy and
that normalization does not cancel their separator-dependent error.

A reviewed [recourse theorem](new-direction/smoothed-box-stable-recourse.md)
now gives an expected FPT bound when a small supplied core leaves an
exact polynomial-time QP class closed under coordinate-box restrictions.
True recourse values round only the core. Additional restricted calls
certify that all relevant residual solutions lie in a local box; gradient
and Hessian tests then produce an exact rational optimizer. This excluded-
region certificate avoids a sampling-precision circle in rational
reconstruction and does not require a convex residual problem. For a core
of size `k` on the unit box, expected work is
`8^k [3+(1+k/2)L/(2sigma)]^k poly(I)` with correctness on every draw.
Deleting the core to a forest is a concrete application of the established
forest-QP oracle. It replaces the deterministic predecessor's growth
parameter by a specified finite noise model, while retaining the stronger
deletion-to-tractability assumption. It does not resolve treewidth alone.
The [prior audit](prior-art/smoothed-box-stable-recourse-prior.md) separates
its expected exact-work guarantee from established recourse and domain-
tightening ingredients; priority and practical performance remain open.

The reviewed [nonlinear completion](new-direction/smoothed-polynomial-box-recourse.md)
is a stronger structural capability: fixing the small continuous core can
leave a dense, jointly convex polynomial residual. Certified objective
intervals and feasible rational completions replace exact recourse values,
which can be irrational. Expected work is
`8^k [3+(1+k)L/(2sigma)]^k poly_d(I)` under full ambient linear noise.
Lower bounds on excluded residual slabs certify containment, then a
uniform nonlinear Hessian test gives the usual exact implicit output.
The concrete convex oracle uses a directly checkable tangent lower bound;
neither the oracle nor residual convexity requires a positive modulus.

A [checked family](new-direction/polynomial-recourse-rank-separation.md)
has degree five, one core coordinate, and dense convex residuals, but
every fixed PSD quadratic convexifier has rank at least the residual
dimension. Its core curvature stays fixed as mixed derivatives grow.
This distinguishes the theorem from supplied low-rank quadratic models;
it does not exclude nonlinear convexification or prove hardness. The
[significance assessment](new-direction/polynomial-box-recourse-significance.md)
and [prior audit](prior-art/smoothed-polynomial-box-recourse-prior.md)
credit classical partial-convex global search and convex optimization.
The main remaining conceptual target is core-only noise with residual
optimal fibers without uniform strong convexity. A
[rotating-fiber example](new-direction/core-only-noise-rotating-fiber.md)
has fixed projected and set-relative growth on every core-noise draw,
but no full-dimensional jointly convex patch. It has a short exact
sum-of-squares certificate, so this obstructs only the current closure
mechanism.

Two stronger recourse results now have completed independent reviews.
The [native-integer theorem](new-direction/smoothed-native-integer-recourse.md)
allows a fixed constrained integer residual problem with an exact
polynomial oracle under tightened coordinate bounds. At most `2r`
additional calls certify that one residual label remains optimal over
the retained core hull. The corresponding whole core slice then contains
a global optimizer, so exact algebraic optimization in its `k` continuous
variables finishes without gradient or Hessian closure. Expected work is
`[8^k(3+(1+k/2)L/(2sigma))^k+c_d^k] poly_d(I)`, with an effective
degree-dependent constant base. Ordinary algebraic optimizer/value output
has size `c_d^k poly_d(I)` on every draw, including exceptional samples.
The [classical TU/flow oracle](prior-art/integer-convex-flow-recourse-prior.md)
makes this a constrained MINLP capability with unrestricted integer
dimension and binary-encoded capacities. The core affects costs only;
general mixed feasibility constraints are not included.

The reviewed [interior-flow extension](new-direction/smoothed-interior-core-flow.md)
removes all residual perturbations for integer network recourse, while
allowing persistent ties. It assumes every optimal core point is interior
throughout the noise cube. At a rational query, a shortest-path tree in
the residual network supplies polynomial potentials. Exact small-core
sign tests certify one flow over the retained box. Stationary-noise
images of all possible certificate boundaries have lower dimension;
the tube bound controls them without enumerating the underlying flow
labels. Expected work and all-draw algebraic output retain the preceding
constant-base bounds. A two-arc example proves that boundary optima can
defeat this uniform-flow test on a positive-probability event. It is a
limitation of this certificate. The reviewed
[boundary-flow theorem](new-direction/smoothed-boundary-core-flow.md)
overcomes it by representing all tied optimal flows through tightened
arc intervals. Inward derivative minimization over those intervals is
again convex flow. A conformal-cycle distance bound and first outside
marginals control every other flow, yielding a sound core-face test.
Facewise tubes and normal-noise margins force that test to pass; a
fixed-dimensional algebraic value bound charges the larger precision
needed by nonlinear charts. Expected work is
`f_d(k)[3+(1+k/2)L/(2sigma)]^k poly_d(I)`, and both sampling length and
all-draw output have `f_d(k) poly_d(I)` bounds. The core may now be
optimal on any boundary, and residual perturbation remains unnecessary.

The reviewed [bilinear case](new-direction/smoothed-bilinear-core-flow.md)
restores `[8^k(3+(1+k/2)L/(2sigma))^k+c_d^k] poly_d(I)` expected work
and polynomial sampling precision. Affine adjusted marginals admit a
polynomial-bit margin from their cube-restricted zeros; online margin
tests use endpoint evaluations. Inward derivative recourse is linear.
The core Hessian is that of `phi`, so coupling strengths and native
capacities do not enter `L`. The
[assessment](new-direction/boundary-core-flow-significance.md) identifies
separable convex network costs with a small bilinear continuous core as
the strongest current application class. It also records a deterministic
accuracy-grid baseline: the result's additional capability is exact
sampled-instance optimization and certificates, not a new approximation
scheme or demonstrated implementation speedup.

The independently reviewed [TU extension](new-direction/smoothed-core-tu-recourse.md)
preserves both bounds for fixed totally unimodular equalities and bounded
native integers. Interpolation and TU integrality give a compact exact
dual. A base-bounded dual vertex supplies polynomial charts, and unit
conformal circuits give the required distance estimate. Explicit finite
zero-cost slacks extend the result to TU inequalities. These ingredients
are classical; the additional conclusion is their composition with the
core-only finite-noise global search. For example, a quadratic unit core
gives separable convex integer costs plus `k` concave clipped-quadratic
aggregate costs over a TU set, with `L=1` regardless of coupling size.
This interpretation does not require the separate interior-range premise
needed for an unrestricted negative-quadratic objective.

The [core-only-noise theorem](new-direction/core-only-noise-boundary-recourse.md)
handles continuous residuals with a supplied uniform modulus `mu>0`.
It removes both residual perturbations and residual-interiority premises.
The unique conditional optimizer is Lipschitz; active-pattern boundaries
and their stationary-noise images have lower dimension. Fixed-block
elimination and a classical singular-algebraic tube estimate bound
finite-grid proximity to those images without using coefficient heights.
On a stable branch, small nonnegative residual multipliers have small
derivatives. Their Schur-complement loss is controlled, so only large
active multipliers need be fixed before a full positive-Hessian test.
The algorithm uses ordinary recourse and local matrix certificates; it
does not construct the eliminated sets or discover an implicit branch.
Expected work remains `8^k[3+(1+k)L/(2sigma)]^k poly_d(I)`.

Uniform strong residual convexity is material. It also means the class
admits a fixed rank-`k` quadratic convexifier with core curvature shift
`alpha=M+M^2/mu`. The new parameter advantage is preserving the original
`L`, rather than charging this potentially much larger `alpha`; it is
not the rank separation proved for merely semidefinite residuals.
The exact finite core-only law and handling of weak active residual
bounds are the additional capabilities. The
[focused prior comparison](prior-art/core-only-noise-boundary-recourse-prior.md)
credits sensitivity, genericity, parametric optimization, and the tube
estimate separately. Publication priority and practical implementation
remain open.

The reviewed [regularization investigation](new-direction/core-only-noise-regularization-limit.md)
shows why vanishing residual curvature does not immediately extend this
theorem. A sparse convex quartic with bounded coefficients has a unique
optimizer, yet its isotropic regularized optimizer needs `2^n` parameter
bits merely to approach one coordinate within a constant error. Adding
an independent noisy core leaves this obstruction on every draw. A
[compact-polytope growth lemma](new-direction/canonical-convex-fiber-regularization.md)
does give `f-f*>=c dist(.,argmin f)^d` for a degree-`d` convex polynomial.
The same example forces `log(1/c)>=2^n`, regardless of the fixed distance
exponent. Thus better exponents alone cannot justify polynomial-precision
point extraction. The example has an easy direct solution; neither a
general point-optimization lower bound nor originality of the qualitative
growth lemma is claimed. A further obstacle is that repeated uses of the
strong-recourse theorem retune its finite noise law as the regularizer
shrinks. A valid exact coordinate oracle must keep the original draw
fixed and provide an effective convergence rule or a different certificate.

The reviewed [quartic point-output reduction](new-direction/convex-point-radical-comparison.md)
now identifies a broader arithmetic requirement. Two strongly convex
comparison problems have opposite active-bound tests. A jointly convex
quartic coupling makes one new coordinate exactly zero or one at every
optimizer according to the Square Root Sum comparison. After equality
preprocessing, the optimizer is unique; degree, coefficient magnitudes,
and treewidth remain bounded. Constant coordinate accuracy therefore
decides the source problem. An independent noisy core leaves the encoding
unchanged on every draw, so a merely-convex residual theorem with expected
polynomial point evaluation would give a Las Vegas Square Root Sum
algorithm. The full point-growth modulus is not controlled.
The [assessment](new-direction/convex-point-comparison-assessment.md)
keeps certified value approximation, compact definitions, and efficient
coordinate evaluation distinct. Its separate prime-radical family forces
superpolynomial size even for sparsely listed univariate coordinate
polynomials, while those particular coordinates remain easy to evaluate
numerically. The [source comparison](prior-art/convex-point-radical-prior.md)
credits established arithmetic reductions for strong approximation of
Nash equilibria and classical weak convex optimization. No NP-hardness,
unconditional computational separation, or publication priority is claimed.

The reviewed [PosSLP extension](new-direction/posslp-convex-point-extraction.md)
uses bounded numerator/denominator gates to represent an arbitrary integer
arithmetic circuit. Geometric weights make their squared residual sum
strongly convex on the entire box, with a polynomial-size proof. Two
opposite bound tests and the same quartic coupling then force a coordinate
to zero or one according to the integer circuit's sign. Constant point
accuracy therefore decides PosSLP, even with a unique optimizer and
bounded coefficient magnitudes after common objective scaling. Unlike
the Square Root Sum construction, this result does not bound treewidth.
The [source comparison](prior-art/convex-point-posslp-prior.md) identifies
existing PosSLP reductions to strong approximation of unique Nash
equilibria and to exact semidefinite feasibility. The scoped addition is
the convex-polynomial minimizer class and output contract; priority is
unresolved. This reinforces the choice to pursue structured recourse
certificates rather than treat general convex point recovery as routine.

The reviewed [fixed-law value theorem](new-direction/core-only-noise-value-oracle.md)
supplies a complementary positive result. For one or two nonconvex core
variables and arbitrary convex polynomial residuals, the same finite
core-only draw supports a certified global objective interval of width
`2^-q` and a feasible rational point in expected
`(1+L/sigma) poly_d(I+q)` work. The algorithm caps generated cells at
each level before making oracle calls. Projected growth bounds their
count by a constant times `max(1,L/g)^(k/2)`; integrating the finite-law
tail pays for both capped search and rare exact fallback when `k<=2`.
One random work factor controls all precisions, including meshes finer
than the sampling grid. The certificates are valid on every draw and
do not require a growth certificate. This supplies objective evaluation
without asserting efficient optimizer coordinates. The independent
[proof and arithmetic review](reviews/core-only-noise-value-review.md)
passes. The [prior audit](prior-art/core-only-noise-value-oracle-prior.md)
compares low-rank quasi-concave smoothing, parametric convex methods,
and the project's earlier cell counts; priority remains unresolved. Extending
the scalar-growth argument to larger cores leaves an uncontrolled
moment, motivating a search for a stronger geometric count.

That search now gives the reviewed
[all-scale theorem](new-direction/all-scale-core-value-oracle.md), removing
the core-size restriction. The padded convex hull of near-optimal core
points contains disjoint small cubes around the retained witnesses.
Its largest simplex bounds the cell count. A strongly convex conjugate
defines a locally finite subgradient-image measure; a covering argument
then gives a `1/T` tail for one count factor over all scales. Carathéodory
representations and a compact quadratic QR witness encode the strict
determinant event with two quantifier blocks, so the finite-grid transfer
is uniform in the threshold. The same cap and exact fallback yield
`f_d(k)(1+L/sigma)^k poly_d(I+q)` expected work for all precisions of one
sampled rational objective. Root independently checked the repaired
encoding and the [fresh review](reviews/all-scale-core-value-oracle-review.md).
The strongest application is a small nonlinear core with arbitrarily
many convex residual variables, whose point-growth modulus may vanish.
The result leaves the full residual-coordinate output limitation intact.
The [prior audit](prior-art/all-scale-core-value-oracle-prior.md) compares
standard measure theory, existing near-optimal counts and smoothed
optimization; it does not establish publication priority.

The reviewed [core-coordinate extension](new-direction/core-only-noise-core-oracle.md)
adds a Cauchy name of one fixed globally optimal core at the same expected
cost. Every retained hull contains all optimal cores and the incumbent's
core, so its rational diameter certifies coordinate error directly.
A base projected-growth threshold bounds the required depth. Failure of
the actual diameter test has probability small enough to pay for a fixed
lexicographic fallback, under one enlarged finite law for every precision.
The [review](reviews/core-only-noise-core-oracle-review.md) checks selector
consistency, including tied cores. Residual coordinates still have only
the objective-gap guarantee. The
[significance assessment](new-direction/all-scale-core-value-significance.md)
distinguishes this precision gain for the sampled objective from the
deterministic approximation baseline and the `k sigma` regret for the
original objective. The reviewed
[continuous-noise comparator](new-direction/continuous-core-noise-value-oracle.md)
instead reveals fixed random bitstreams as needed and avoids fallback;
its random-real input model is distinct from the finite-rational theorem.

The reviewed [coupled-polytope extension](new-direction/coupled-polytope-core-value-oracle.md)
replaces the product domain by arbitrary bounded rational linear
constraints, under a verified core quadratic convexification. Its
relative convex value interface includes lower-dimensional feasible
sets and exact rational repair of weakly feasible outputs. Near-optimal
joint witnesses pad to whole retained core cells, so the all-scale
measure argument does not require a continuous projected value function.
Both certified values and a
[fixed optimal core](new-direction/coupled-polytope-core-oracle.md)
have expected `f_d(k)(1+alpha/sigma)^k poly_d(I+q)` work. This is a
different assumption tradeoff: for
`F=(v^2+z^2)/2+M v z`, the box bound has `L=1`, while this particular
core convexification requires `alpha>=M^2-1`. Merely convex residual
fibers do not supply the coupled oracle.

For quadratics, the reviewed
[reconstruction consequence](new-direction/qp-core-cauchy-reconstruction.md)
recovers an exact rational global optimizer and value. The full
lexicographic optimizer is a vertex of a rational stationary-face
polytope, even with a singular restricted Hessian. Uniform denominator
bounds determine a polynomial-bit Cauchy precision; rational
reconstruction and exact convex fiber completion then suffice. A rational
QP fallback avoids processing large generic algebraic records. The
product result retains its original core-noise model and `L` parameter;
the coupled version retains `alpha`. Earlier aligned-noise work already
proves a related all-dimensional exact-QP guarantee, so the added value
here is the simpler output interface and the stated parameter distinction.

Global convexity permits a stronger smoothed point conclusion. The
reviewed [selected-coordinate theorem](new-direction/joint-convex-core-point-oracle.md)
has expected ordinary `poly_d(I+q)` work, without an exponential core-size
factor or a numerical inverse-noise factor. A buffered convex sublevel
set has a computable relative inner ball. Two weak convex optimizations
per requested coordinate give certified outward extrema; a diameter test
is correct on every draw. One small-growth event pays for fallback at
every precision. This exposes a useful distinction: random linear
perturbations can make strong approximation efficient in the perturbed
coordinates, while unperturbed residual point extraction remains subject
to the quartic barriers. The result concerns the sampled objective and
does not recover an optimizer of the original one.

A deterministic degree-three result now gives a different boundary.
The reviewed [convex cubic theorem](new-direction/convex-cubic-point-oracle.md)
provides polynomial-time approximation of the fixed minimum-norm optimizer
on a bounded rational box. Center reflection controls the affine PSD
Hessian by one rational matrix. Cubic third-derivative symmetry bounds
transverse displacement by the fourth root of the objective gap, and a
Hoffman estimate controls the remaining affine slice. All constants have
polynomial encoding length; the optimizer and its possibly irrational
slice offset need not be known. The resulting regularization schedule
uses `poly(I)+O(q)` bits, unlike the reviewed quartic counterexample.
This is a proved positive counterpart to the quartic strong-approximation
reductions, with convexity supplied or its verification charged. A solver
could use it for certified cubic continuous subproblems without an input
growth modulus. Practical algorithms, precise external priority, and
extensions to partially convex MINLP remain separate research questions.

Two current extensions have now passed independent review. The
[polytope cubic theorem](new-direction/convex-cubic-polytope-point-oracle.md)
uses rational affine-hull reduction and an interior ball to extend the
deterministic point guarantee to arbitrary bounded rational polytopes.
The [full-point core composition](new-direction/cubic-core-full-point-oracle.md)
handles a nonconvex total cubic when `F+alpha||v||^2/2` is convex on
that polytope. It returns the minimum-norm optimizer in the fiber of
the selected optimal core, using only core perturbations and retaining
`f(k)(1+alpha/sigma)^k poly(I+q)` expected work. The completion
coefficient `alpha+1` affects only precision bits. Its exact-core
surrogate is convex; rational rows from the supplied polynomial and
core selectors give an error bound uniform in the unknown irrational
core. A short rational core approximation and an original-coordinate
norm penalty then recover the declared full point. This is the
nonconvex cubic output advance: deterministic point approximation was
already available for the convex cubic itself. The
[assessment](new-direction/convex-cubic-point-significance.md) and
[source comparison](prior-art/convex-cubic-point-oracle-prior.md)
preserve the distinction from exact boundary labels, algebraic output
and classical low-dimensional perturbation algorithms.

A distinct [strong-field result](new-direction/strong-field-component-polynomial.md)
uses a reviewed exact polynomial component solver with deterministic
`c_d^k poly_d(H)` work, including all degeneracies. Large independent
linear fields pin most original coordinates by strict monotonicity.
The expected sum of weighted component costs is finite under an explicit
subcritical inequality. This gives expected polynomial exact optimization
at fixed degree without a graph-width parameter, with one algebraic
representation per component and a symbolic sum for the value. Its
noise requirement can be numerically large, especially with large native
integer ranges, and its original-objective loss bound can consequently
be weak. It is a separate capability, not an improvement of the sparse
theorem's weak-noise dependence. The algebraic construction uses classical
deformation and univariate-representation ideas; exact prior comparison
of its constant-base complexity is continuing.

The first reviewed constrained corollary handles
[overlapping polynomial graphs](new-direction/smoothed-polynomial-graph-constraints.md).
Bounded-depth substitution preserves bounded degree and a controlled bag
size; independent ambient noise on retained free coordinates survives
conditioning on the other coefficients. It inherits the box theorem using
pullback curvature. This is a parameterization corollary, not a general
coupled-constraint theorem. An always-feasible, width-three
[affine mixed reduction](new-direction/constrained-smoothing-barrier.md)
shows that objective noise can leave SUBSET SUM encoded in feasibility on
every draw. The reviewed
[simplex-block extension](new-direction/simplex-block-smoothed-extension.md)
now covers disjoint resource and probability simplices together with
native-integer intervals. Its additional mechanism is a joint count over
original faces, using tangent noise differences without assuming their
independence. Original-face tests and an explicitly evaluated relative
convex polytope give the same exact-output contract. The bound remains
fixed-width polynomial, and whole-block bags and block curvature bounds
are essential. The [source comparison](prior-art/simplex-block-smoothed-prior.md)
separates this composition from established ingredients.

Two further constrained theorems have now passed independent review.
The [implicit-graph theorem](new-direction/smoothed-implicit-graph-constraints.md)
allows genuinely algebraic reduced objectives: each dependent variable
is a unique monotone scalar root over the entire retained mixed box.
Certified approximate DP replaces exact comparisons of algebraic sums.
Polynomial graph KKT systems give the finite-noise tail, and a rational
weak separator permits certified evaluation of the reduced convex patch.
This preserves exact implicit physical feasibility, while requiring a
global chart, full retained-domain coverage, and verified reduced
curvature. Its [source comparison](prior-art/implicit-monotone-actuator-prior.md)
credits implicit-state relaxation and classical algebraic/convex tools.

The [continuous order theorem](new-direction/smoothed-sparse-order-polynomial.md)
covers overlapping order inequalities rather than a product of local
constraint blocks. Feasible common-threshold rounding uses a full Hessian
upper bound. Within each bag-order chamber, affine fiber maps give
semiconcavity without enumerating those maps. LP exposure gaps identify
active equalities; paired-coefficient counting bounds small gaps even
when active multipliers are not unique. The resulting expected exact
bound is polynomial at fixed width, with rational feasible evaluation
of its implicit convex output. The
[source comparison](prior-art/order-polytope-smoothed-prior.md) credits
Stanley's order-polytope geometry and Bach's common-quantile coupling
for nonconvex submodular isotonic optimization. General affine
constraints and FPT in width remain outside this theorem.

The reviewed [mixed order extension](new-direction/smoothed-mixed-order-polynomial.md)
now permits unrestricted binary variables. Conditional projected domains
can be nonconvex and values can jump at endpoints. A monotone transport
fixing zero and one preserves every binary label and provides an upper
support sufficient for counting. Along disjoint zero-one directions its
curvature is at most `NH`, yielding expected work
`C^p q!(q+1)[2+3NH/(4sigma)]^q poly_d(I)`, where `q` counts continuous
coordinates per bag. Exact closure fixes binary labels first; a checked
counterexample rules out applying continuous LP exposure prematurely.
Implications and continuous activation bounds are covered, arbitrary
integer ranges are not. This is still fixed-width polynomial work.

The exact-output contract also has substantive limits. Reviewed
[boundary enclosures](new-direction/deterministic-boundary-output.md)
give a certified approximation program under point growth alone, but a
nearby strict nonglobal local minimum defeats a general polynomial-radius
KKT/SOSC isolation argument. A separate
[radical-sum reduction](new-direction/convex-active-set-radical-comparison.md)
shows that recognizing one exact active bound would decide Square Root Sum,
even for uniformly strongly convex cubic objectives of treewidth two.
Neither construction obstructs compact implicit convex descriptions;
neither proves hardness of the approximation task.

The current constrained-MIQP frontier is the reviewed
[Gaussian-like theorem](new-direction/smoothed-gaussian-miqp.md), with
expected `f(m,k,1+nu diam(P)/sigma) poly(I)` exact work and an absolute
input exponent. It requires no growth or uniqueness promise and solves
every draw from one specified finite independent coefficient law.
The [sparse mixed theorem](new-direction/sparse-bag-cell-smoothed-miqp.md)
permits arbitrary integer dimension and negative inertia and gives expected polynomial work at
fixed treewidth under its numerical scale bounds. The target in both
results is the sampled objective. The following deterministic conditioned
results and nonlinear extensions remain separate capabilities.

The main reviewed deterministic sparse framework is an exact algorithm for rational
mixed-integer box QP with bit complexity `f(p,kappa) poly(I)`. Here `p`
is the largest bag size in a supplied tree decomposition, `I` is input
length, and `kappa=max(1,L/g)` compares upper coordinate curvature with
global quadratic growth around a unique optimum. The polynomial input
exponent is absolute. The algorithm needs no growth constant, occurrence
bound, gradient, or nonlinear optimization oracle.

The [filtered coordinate-grid theorem](new-direction/pruned-coordinate-grid.md)
combines globally valid rounding corrections with exact DP min-marginals.
Intervals whose conditional lower bounds exceed the incumbent are removed.
Growth confines the surviving coordinate hulls, so each subsequent grid
has only `O(sqrt(kappa) log(n+2))` states per coordinate, independently of
the accuracy stage. The factor `log(n+2)^p` is bounded by a function of
`p` times `n+2`, giving the fixed-parameter bound. Stored pruning records
preserve a certificate for the original domain.

This strengthens both the earlier shared-grid accuracy bound and the
occurrence-dependent rational-QP specialization. The earlier rebuilt bag
certificates remain useful for their different convex-oracle model,
certificate-size bound, and constrained extensions. The growth assumption
controls speed; certificates themselves remain valid without it.

A complementary reviewed theorem treats
[QP over any bounded rational polytope](new-direction/negative-inertia-qp.md).
Its exact bit complexity is `f(k,max(1,nu/g)) poly(I)`, where `k` counts
negative Hessian eigenvalues and `nu=max(0,-lambda_min(A))`. Only
negative curvature enters this parameter; positive curvature affects
preprocessing precision. It uses a
rational PSD-minus-low-rank decomposition, a small auxiliary problem, and
exact convex recourse. Its reviewed
[mixed-polytope extension](new-direction/negative-inertia-miqp.md) gives
`f(m,k,max(1,nu/g)) poly(I)` complexity with integer dimension `m` as an
additional parameter, using the existing exact convex MIQP oracle.
This covers dense and linearly constrained problems; the sparse theorem
permits arbitrary negative inertia and integer dimension on a product box.
Neither theorem establishes an efficient algorithm
without its structural and conditioning parameters.

The reviewed [proximal growth-grid theorem](new-direction/proximal-growth-grid.md)
and [exact recovery lemma](new-direction/proximal-exact-recovery.md) give
the same `f(p,kappa) poly(I)` bound for mixed-box QP with arbitrary optimal
sets. They require a supplied valid growth bound. A nearby feasible point
identifies a face whose linear stationarity equations recover an optimizer,
including when the optimal set is a continuum. This avoids counting its
components or coordinate projections. The interval and exactness guarantee
remain dependent on the supplied promise; final rational output checks do
not independently certify global optimality.
The [general-polytope recovery extension](new-direction/proximal-polytope-recovery.md)
gives the analogous exact mixed-polytope theorem under a supplied valid
full-distance growth bound, including arbitrary optimal sets. Its explicit
slack threshold selects constraint equalities for one linear stationarity
solve. The promise remains necessary for the current algorithm's guarantee.

The [finite-mode extension](new-direction/pruned-grid-finite-modes.md)
requires growth only in the gridded coordinates and permits tied mode
assignments. A [nonlinear low-rank extension](new-direction/approximate-convex-recourse.md)
uses certified approximate recourse for separable convex quartics minus a
low-rank quadratic. It supports any number of integer coordinates with
binary-encoded interval bounds. Its guarantees are certified approximation,
or exact optimization when all coordinates are integer; continuous quartic
optimizers need not be rational. Several simpler subclasses already admit
exact algorithms, as the [focused audit](prior-art/separable-lowrank-minlp-prior.md)
explains.

| Result | Assumptions beyond a supplied decomposition | Proved bound |
| --- | --- | --- |
| [Filtered mixed-box QP](new-direction/pruned-coordinate-grid.md) | Rational mixed product box; pointwise global growth; upper coordinate curvature `L`; supplied bags of size `p` | Exact optimizer and value in `f(p,max(1,L/g)) poly(I)` bit operations. An additive gap `2^-q` costs `f(p,kappa) poly(I+q)`. No occurrence parameter or supplied `g`. |
| [Explicit polynomial pruning](new-direction/polynomial-pruned-grid-extension.md) | Fixed-degree rational polynomial factors; mixed native-integer/continuous box; verified full-hull coordinate curvature; unique optimum with point growth | Certified gap `2^-q` in `f_d(p,kappa) poly(I+q)` work. Finds an exact optimum in `f_d(p,kappa) poly(I)` work on all-integer boxes by objective-value spacing. Extends the existing semiconcave mechanism; no exact continuous coordinates are promised. |
| [Exact implicit convex patch](new-direction/implicit-convex-patch-certificate.md) | Same polynomial model; additionally, the full continuous Hessian at the optimum dominates the growth scale | Constructs a verified strongly convex subproblem defining the exact optimizer in `f_d(p,kappa) poly(I)` work and output length; supports `q`-bit position/value evaluation in `f_d(p,kappa) poly(I+q)`. Interior optima satisfy the added Hessian assumption automatically; boundary optima need not. |
| [Sparse strict-copositivity certificate](new-direction/geometric-copositive-certificate.md) | Homogeneous rational quadratic on the nonnegative orthant; positive optimal Euclidean margin `g`; bags of size `p` | Discovers and independently certifies a margin `sigma` in `[g/16,g)` in `f(p,L/g) poly(I)` work. No supplied `g`, target accuracy, or coefficient-height-driven state refinement. A two-sided variant also finds a negative witness when `g<0`; the boundary case is not generally decided. |
| [Mixed-box candidate certificate](new-direction/mixed-shell-certificate.md) | Rational proposed solution of a mixed rational lattice box QP; supplied bags of size `p`; diagonal curvature upper bound `L>0` | Certifies unique global optimality and a physical Euclidean margin in `f(p,max(1,L/g)) poly(I)` work, with `L/sigma <= max(32,12L/g)`. No supplied growth promise is trusted; a correct unique candidate guarantees termination. Candidate discovery is separate. |
| [Mixed coordinate-fiber certificate](new-direction/geometric-product-face-certificate.md) | Supplied optimal-set candidate `{v} x Y`; active and free coordinates may both be mixed; full graph bags of size `p` | Certifies the entire fiber and physical distance-to-set growth in `f(p,max(1,L/g)) poly(I)` work, without a supplied growth bound or free-mode enumeration. Verifies constancy and uniform continuous KKT signs; does not discover an unknown optimal set. |
| [Polynomial mixed-box candidate certificate](new-direction/nonlinear-shell-certificate.md) | Supplied rational candidate; explicit fixed-degree polynomial factors; mixed product box; verified upper coordinate curvature on the full continuous hull | Sound growth and optimality certificate on acceptance; under positive point growth, work `f_d(p,max(1,L/g)) poly(I)` and `L/sigma <= max(32,20L/g)`. Taylor coefficients enter through logarithmic radius cost. Rational candidate and explicit encoding are substantive limits. |
| [Few negative directions](new-direction/negative-inertia-qp.md) | Rational QP over a bounded rational polytope; negative inertia `k`; pointwise global growth `g`; `nu=max(0,-lambda_min(A))` | Exact optimizer and value in `f(k,max(1,nu/g)) poly(I)` bit operations. The projected version permits nonunique optima with one common image. Requires exact convex QP solves; no sparsity assumption. |
| [Mixed polytope QP](new-direction/negative-inertia-miqp.md) | Bounded rational mixed polytope with `m` integer coordinates; negative inertia `k`; pointwise global growth `g` | Exact optimizer and value in `f(m,k,max(1,nu/g)) poly(I)` bit operations. Exact convex MIQP recourse retains integrality; no supplied growth constant. |
| [Arbitrary optimal sets on mixed boxes](new-direction/proximal-exact-recovery.md) | Rational mixed product box; bag size `p`; supplied valid `kappa` with growth at least `L/kappa` toward the full optimal set | Exact optimizer and value in `f(p,kappa) poly(I)` bit operations. No optimal-set cardinality or projection parameter. The stopping guarantee depends on the growth promise. |
| [Expected exact work](new-direction/expected-smoothed-qp.md) | Continuous bounded rational polytope; at most two negative Hessian eigenvalues; specified independent rational-grid linear noise of half-width `sigma` | Exact answer on every draw; expected bit work `poly(I) (1 + nu sum_i w_i / sigma)`. No supplied growth bound. The algorithm uses an exact fallback on the same sampled input. |
| [Exact algebraic cell closure](new-direction/smoothed-exact-cell-closure.md) | Continuous bounded rational polytope; arbitrary negative inertia `k`; specified rational noise in normalized factor coordinates | Exact answer on every draw; expected `f(k,1+nu diam(X)/sigma) poly(I)` bit work. No growth assumption or accuracy-dependent sampling law. Noise is generally correlated in original coordinates. |
| [Independent ambient noise](new-direction/smoothed-ambient-cell-closure.md) | Continuous bounded rational polytope; arbitrary negative inertia `k`; specified independent rational-grid noise on every original linear coefficient | Exact answer on every draw; expected `C^k (1+H_amb) poly(I)` with explicit numerical width/noise factor. Polynomial at fixed `k` when that factor is polynomially bounded; dimension dependence `n^{O(k)}`, not FPT in `k`. |
| [Gaussian-like ambient noise](new-direction/smoothed-gaussian-cell-closure.md) | Continuous bounded rational polytope; specified finite rational approximation to independent Gaussian coefficient noise | Exact answer on every draw; expected `f(k,nu diam(X)/sigma) poly(I)` with an absolute input exponent. Gaussian-weighted local counts and a bounded rational sampler remove the ambient dimension powers; no real-Gaussian input claim. |
| [Smoothed constrained MIQP](new-direction/smoothed-miqp-cell-closure.md) | Bounded rational mixed polytope; integer dimension `m`; negative inertia `k`; specified uniform ambient rational noise | Exact answer on every draw; expected `f(m) C^k (1+H_amb) poly(I)`. Best-other-label convex MIQP solves certify cell validity; the uniform-noise bound remains dimension-dependent. |
| [Gaussian-like constrained MIQP](new-direction/smoothed-gaussian-miqp.md) | General bounded rational mixed polytope; specified independent finite Gaussian-like original coefficient noise | Exact output every draw; expected `f(m,k,1+nu diam(P)/sigma) poly(I)` with absolute input exponent. `P` is the continuous relaxation; no growth or uniqueness assumption. |
| [Separable mixed closure](new-direction/smoothed-mixed-separable-closure.md) | Product mixed box; convex piecewise quadratics with rational knots and coefficients; supplied low-rank concave coupling | Any integer dimension; exact output every draw. Expected FPT under aligned noise and fixed-rank polynomial work under uniform ambient noise, with explicit projected-width/noise factors. |
| [Anisotropic Gaussian separable closure](new-direction/anisotropic-gaussian-separable-closure.md) | Same separable mixed model; supplied full-row-rank factor after fixed-coordinate preprocessing; specified independent finite Gaussian-like noise | Expected exact `f(k,1+beta diam(X)/sigma) poly(I)` with arbitrary integer dimension and no factor-conditioning parameter. `beta=alpha ||T||^2` is supplied concave curvature, not intrinsic negative curvature. |
| [Sparse smoothed QP](new-direction/sparse-bag-cell-smoothed-qp.md) | Continuous rational box; supplied bags of size `p`; upper diagonal curvature `L`; specified independent rational linear noise | Exact answer on every draw; expected `C^p [4+(1+n/2)Ls/(2sigma)]^p poly(I)`, where `s` is maximum coordinate width. Arbitrary negative inertia and occurrence. Fixed-width polynomial, not FPT in width. |
| [Sparse smoothed MIQP](new-direction/sparse-bag-cell-smoothed-miqp.md) | Mixed product box; supplied bags of size `p`; the same upper-curvature and finite independent noise assumptions | Same expected fixed-width polynomial bound with maximum mixed coordinate width. Arbitrary integer dimension, negative inertia, and occurrence. Every draw is exact; integer widths enter numerically. |
| [Sparse smoothed polynomial optimization](new-direction/smoothed-sparse-polynomial.md) | Explicit fixed-degree rational polynomial factors; mixed native-integer/continuous box; full-hull coordinate curvature bound; specified finite independent linear noise | Exact implicit optimizer every draw; expected `C^p [4+(1+n/2)L w_max/(2sigma)]^p poly_d(I)` work. No growth or boundary-Hessian promise. Usual output is a certified strongly convex patch; rare algebraic fallback handles ties and flat sets. Certified arbitrary-precision evaluation has polynomial expected work after construction. |
| [Exact low-rank integer nonlinear optimization](new-direction/smoothed-integer-low-rank.md) | Integer product box; separable convex rational quartics minus a supplied rank-`r` concave quadratic; specified rational factor noise | Exact answer on every draw, without growth or fallback; expected `8^r H poly(I)` with explicit projected-width/noise factor `H`. Arbitrary integer dimension and binary-encoded intervals. |
| [Expected approximation cells](new-direction/smoothed-semiconcave-cells.md) | Fixed-dimensional box; upper coordinate curvature; independent bounded-density linear noise; exact point oracle | Expected logarithmic accuracy dependence without growth. Convex recourse gives a low-rank QP application under aligned noise. Its rational noise law is chosen for the requested accuracy; no fixed-law exact conclusion. |
| [Fixed-parameter rational box QP](geometric-dp/regridded-qp-bit.md) | Continuous rational box QP; pointwise global growth; supplied bags of size `p`, occurrence `k`, and full bag Hessian bound `M`; `kappa=max(1,M/g)` | Exact optimizer and value in `f(p,k,kappa) poly(I)` bit operations, with an absolute polynomial exponent and no supplied `g`. Polynomial objectives also admit certified approximation when numerical degree is counted. |
| [Rebuilt bag certificates](regridded-certificates/note.md) | Continuous box; global growth `F-f* >= g ||x-x*||^2`; Lipschitz bag gradients; continuous convex lower models with quadratic error; bounded variable occurrence `k` | Final `O(N C^p J)` cells/leaves; total `O(N C^p J^2)` boxes created; `O(N 3^p C^p J^3)` exact local convex-oracle calls, with `p=w+1` and `J=O(log(N/eps))` including displayed scale constants. No branching-degree or interior-minimum requirement. |
| [Corrected coordinate grids](geometric-dp/theorem.md) | Mixed product box; global pointwise quadratic growth; upper coordinate curvature `L` | `O((N+M) theta^(-p) (J+1)^(p+1))` exact table work, where `theta` is proportional to `min(1,sqrt(g/L))`, `M` counts factors, and `J=O(log(nL s^2/eps))`. No gradient or nonlinear optimization oracle. |
| [Arithmetic and model extensions](geometric-dp/extensions.md) | Underlying grid hypotheses plus certified finite factor tables, or rational polynomial factors with numerical degree counted; optional private recourse or explicitly enumerated finite states | Approximate arithmetic preserves the accuracy rate; exact integer certificates can be found without a growth constant; a polynomial bit bound holds at fixed width, bounded conditioning, and polynomially bounded numerical degree. |
| [Exact rational mixed-integer box QP](geometric-dp/exact-box-qp.md) | Rational quadratic data on a mixed product box; unique optimizer; supplied width `p-1`; `kappa=max(1,L/g)` | Exact rational optimizer and value in bit complexity polynomial in input length and `kappa` at fixed `p`. The growth constant need not be supplied. Every unique optimum has some positive `g`, but it can be too small to give a useful complexity bound. |
| [Feedback vertex set QP](new-direction/fan-exploration.md) | Continuous rational box QP; a supplied core of `r` variables leaves a forest; unique optimal core with projected quadratic growth `g`; positive core diagonal curvature at most `L` | Exact optimization in `f(r,max(1,L/g)) poly(I)` bit operations, without occurrence dependence or a supplied growth constant. Recourse optima may contain a continuum. The exact forest oracle is prior work. |

The constants matter: `g` is a global margin around the optimum, not just local
Hessian curvature. Near-tied distant solutions can make it very small.
The reviewed [perturbation theorem](new-direction/smoothed-linear-growth.md)
quantifies one way favorable growth can arise: independent linear noise
gives a global modulus with high probability. Rational QP needs only
polynomial-bit sampled coefficients, using a finite-face count to control
discretization. On the stated bounded numerical scales, the main algorithms
therefore have high-probability polynomial work at fixed width or fixed
negative inertia. This does not bound expected runtime and solves the
sampled objective rather than the original one.
The [summed-response refinement](new-direction/summed-response-growth.md)
gives, for uniform rational noise of half-width `sigma`, growth at least
`rho sigma / [24 (sum_i w_i) (2+log(4n/rho))]` with probability
`1-rho`, where `w_i` are coordinate widths. Its
[significance review](reviews/smoothed-growth-significance.md) identifies
classical generic-growth arguments and the priority risk in the short
quantitative proof. An original-objective approximation follows with
additional error at most `sigma sum_i w_i`, which generally reintroduces
inverse-accuracy dependence.
The subsequent [proximal-map theorem](new-direction/proximal-growth-tail.md)
improves this to the sharp tail
`Pr(g* < eps) <= 2 eps sum_i phi_i w_i`, and to rational-grid growth
`g* >= rho sigma / (2 sum_i w_i)` with probability at least `1-rho`.
The finite-grid tail is uniform over every threshold, with a controlled
additive atom term. This is stronger than a single high-probability bound.

The [expected exact-work theorem](new-direction/expected-smoothed-qp.md)
then adds a distinct algorithmic step. The conditioned negative-inertia
solver uses `O(kappa^(k/2))` cells per level. Interleaving it with exact
active-face enumeration caps the cost on each sampled instance. The
capped inverse-growth moment is polynomial for `k <= 2`, including its
critical logarithm at `k=2`. Polynomial-bit sampling controls the tie
atoms against the fallback's combinatorial cost. This proves expected
work `poly(I) (1 + nu sum_i w_i / sigma)` and exact correctness on
every draw. It does not resample difficult instances. The argument does
not extend this expected polynomial bound to `k > 2`.

A separate [direct expected-cell proof](new-direction/smoothed-semiconcave-cells.md)
avoids growth moments altogether for approximation. Near-optimal grid
points satisfy neighboring-value comparisons that restrict each random
linear coefficient. Independence bounds their expected count uniformly
over the refinement levels. A concrete nested cell search realizes the
bound. Applied to the Fenchel envelope, it permits arbitrary fixed rank
under noise in the factor coordinates; those perturbations are correlated
in original coordinates. Its finite-bit version chooses noise precision
for a prescribed tolerance. An atomic fixed law can put positive mass on
a flat objective, so exact completion needs a separate mechanism.

That mechanism is now available for continuous QP in the reviewed
[algebraic cell-closure theorem](new-direction/smoothed-exact-cell-closure.md).
An exact convex-QP solve also supplies a rational region where its recourse
value has one quadratic formula. A cell contained in such a region is
solved exactly and removed. An unresolved near-optimal cell places the
random factor coefficients close to one of finitely many fixed hyperplanes.
Their count and curvature heights determine a polynomial-bit noise grid
and a polynomial number of stages before sampling. An exact fallback
handles every exceptional draw. Expected work is
`f(k,1+nu diam(X)/sigma) poly(I)` for arbitrary negative inertia, with
an absolute polynomial exponent. This removes the precision circularity
under aligned factor noise; it does not establish the same conclusion
under independent noise in every original coordinate.

The reviewed [ambient extension](new-direction/smoothed-ambient-cell-closure.md)
handles that perturbation model through a separate probability argument.
An ambient cube-volume bound retains dependence between projected factor
coefficients and residual noise. Uniform bounds on the interval components
of local events transfer the continuous estimate to one base-chosen finite
product grid. The exact closure and fallback then give expected work
`C^k (1+H_amb) poly(I)`, where normalized factors satisfy
`H_amb <= [2+(1+2k)(2n+2nu sqrt(n) diam(X)/sigma)]^k`.
Thus every fixed negative inertia has expected polynomial work under the
stated numerical bounds, without a growth assumption. This is not FPT in
the inertia and a dimension-free curvature ratio. The older two-direction
theorem retains its sharper displayed numerical dependence.
The [parametric-QP audit](prior-art/smoothed-cell-closure-prior.md) credits
Ding's older value-function reduction and established critical-region
machinery; the candidate contribution is the smoothed exact-work bound.

The reviewed [Gaussian-like theorem](new-direction/smoothed-gaussian-cell-closure.md)
provides a dimension-uniform FPT alternative. Gaussian factor and residual
vectors are independent, and the local events also locate the factor noise
relative to the projected feasible set. Summing their Gaussian density
bounds over a whole lattice removes the enlarged auxiliary width from the
expected count. A finite rational approximation with bounded sampling time
and controlled distribution-function error preserves that count and pays
for every exceptional atom. Its expected bound is
`f(k,nu diam(X)/sigma) poly(I)` for the specified independent finite law.

Two reviewed mixed extensions use distinct certificates. For
[general mixed polytopes](new-direction/smoothed-miqp-cell-closure.md),
exclusion solves compute the best alternative integer assignment, and a
Lipschitz bound preserves a sufficiently separated winner throughout a cell.
Failure near the optimum implies a global integer-label near-tie, bounded
by classical isolation reasoning. The uniform ambient expected bound is
`f(m) C^k (1+H_amb) poly(I)`. For
[separable mixed recourse](new-direction/smoothed-mixed-separable-closure.md),
scalar neighbor and derivative inequalities directly give a polyhedral
region of global validity, allowing arbitrary integer dimension. Every
active witness supplies a quadratic upper model even at nonsmooth ties.
The rational-knot assumption is necessary for the stated rational output:
rational piece formulas alone can have an irrational minimizing knot.
The reviewed [anisotropic Gaussian extension](new-direction/anisotropic-gaussian-separable-closure.md)
normalizes the factor using an exact rational change of rows and a positive
diagonal metric. It preserves every unary convex term. Weighted meshes and
Gaussian counts then remove numerical factor conditioning from the expected
bound, giving `f(k,1+beta diam(X)/sigma) poly(I)` with any integer dimension.
Full row rank after preprocessing is still required, and `beta` measures
the supplied concave term. It may be much larger than the negative curvature
of the complete objective; no replacement by that intrinsic parameter is
proved.

The separately reviewed [Gaussian MIQP composition](new-direction/smoothed-gaussian-miqp.md)
combines the weighted event count with the integer-gap certificate.
Conditional scalar Gaussian anti-concentration and its finite-law error
bound control original-label near-ties directly. The support-dependent
gap threshold makes the required level grow at most twice as fast as the
logarithm of trial support; the deterministic budget loop still has
polynomial size. This proves expected exact
`f(m,k,1+nu diam(P)/sigma) poly(I)` work on general bounded mixed
polytopes under the specified finite product law. It is the strongest
current constrained-MIQP guarantee in this continuation; it concerns the
perturbed objective and uses the established exact convex MIQP oracle.

The reviewed [sparse theorem](new-direction/sparse-bag-cell-smoothed-qp.md)
uses a different structure and permits arbitrary negative inertia. Retained
bag cells have a globally consistent near-optimal grid witness. Conditioning
on noise outside the bag leaves independent coefficients in its original
conditional value function, so neighboring comparisons bound expected bag
counts uniformly across scales. Sparse separator-key DP joins charge work
linearly in the stored rows. Retained coordinate hulls contain every optimum;
strict gradient signs force original endpoints, and a PSD test then gives
an unconditional exact convex-face certificate. The finite growth tail is
used only to bound closure failures and pay for the fallback. The resulting
bound is polynomial for each fixed bag size under the stated numerical
scales; its dimension powers depend on that size.
Its reviewed [mixed extension](new-direction/sparse-bag-cell-smoothed-miqp.md)
uses nested integer steps down to one, then singleton cells. The original
mixed conditional value has a real extension for curvature analysis, while
neighbor comparisons and minimization still use feasible mixed values.
Fine retained integer witnesses eventually agree under the good-growth
event, permitting sound singleton fixing. Convex closure is allowed only
after all integer variables are fixed. The same fixed-width expected bound
therefore holds with arbitrary integer dimension and explicit numerical
width dependence.

The reviewed [pure-integer nonlinear theorem](new-direction/smoothed-integer-low-rank.md)
uses a different exactness mechanism. Separable convex quartics give an
exact integer recourse oracle through monotone-difference binary search.
On a common `M`-point factor-noise grid, every original objective value
lies on a lattice of spacing `1/[D0(M-1)]`, where `D0` depends only on
base data. A predetermined mesh gives a certified gap of order `M^-2`,
below that spacing, while its noise resolution still supports the expected
cell bound. This returns an exact optimizer for every draw with arbitrary
integer dimension, no growth assumption, and no fallback. Numerical
projected ranges relative to noise remain in the bound. A normalized
long-interval family shows that exponentially many labels can leave that
factor unchanged, but binary and explicitly enumerable domains already
have deterministic fixed-rank algorithms. The
[focused comparison](prior-art/smoothed-exact-separable-lowrank-minlp-prior.md)
also explains the close expected-Pareto-count precedent and its limits as
an algorithm for an implicit projected feasible set.
General coupled nonlinear constraints are not included. Private recourse needs
a valid projected upper-curvature bound and a certified feasible-witness oracle.

Reviewed extensions broaden the domain beyond the table's assumptions.
The [coordinate-anchor method](new-direction/projection-anchors.md) permits
nonunique optima and measures their coordinate projections. The
[affine repair method](new-direction/affine-repair-exploration.md) permits
coupling equalities with a supplied box-preserving affine repair. Its
multiplier-corrected slopes remove a first-order error that defeats the
unmodified slope rule. Stable linear dynamics, including
[private finite controls](new-direction/mixed-stable-audit.md), give a
concrete constrained class with constants independent of the horizon.

The [stable nonlinear dynamics theorem](new-direction/nonlinear-dynamics.md)
extends this mechanism to smooth contractive state equations and continuous
controls. For fixed-degree rational polynomial data, its
[bit-complexity specialization](new-direction/nonlinear-dynamics-bit.md)
returns rational controls, an exact feasible trajectory represented by the
dynamics, and rational global objective bounds. It uses small linear
programs and contraction-aware enclosures. Exact expanded state fractions
can require exponentially many bits, so that output is not promised.

## Why recentering works

The two proofs share a simple estimate. Suppose an oracle run at center `z`
and scale `h` returns a feasible point `x` and bounds

`LB <= f* <= F(x) <= UB`,

whose gap satisfies

`UB-LB <= a ||x-z||^2 + b N h^2`.                            (1)

Assume `g,N,h_0>0`, `0<=a<g/10`, and `b>=0`, with
`F(x)-f* >= g ||x-x*||^2`. The estimate need only
hold for the returned point; the lower bound itself must be globally valid.
Set the next center to `x` and halve `h`.

Writing `e_j=||x_j-x*||^2`, (1) gives

`(g-2a)e_j <= 2a e_(j-1) + b N h_j^2`.                     (2)

If `h_j=h_0 2^-j`, then `e_j<=B N h_j^2` follows whenever

`B >= b/(g-10a)` and `e_(-1)<=B N h_0^2`.

Indeed, the inductive right side in (2) is at most
`(8a B+b)N h_j^2 <= (g-2a)B N h_j^2`; at stage zero the previous error
bound is stronger than needed. The observed gap is then at most

`(10a B+b)N h_j^2 <= g B N h_j^2`.

This proves contraction of the total squared error. It does not require
every bag to be close to the optimizer at the mesh scale, differentiability
of value functions, or stationarity at a boundary optimum.

Here `UB` bounds the objective of the point used as the next center. A
retained best incumbent may have an even smaller value; its stopping gap is
then no larger, but it is not substituted for `UB` in this argument.

The substantive part is constructing a cheap, globally valid bound with
(1). For shared grids, independent unbiased rounding makes the interpolation
error a sum of unary corrections. For rebuilt bag certificates, subtree
gradients at the current center cancel first-order copy errors, and bounded
coordinate occurrence controls the remaining total error. The two detailed
notes prove these constructions and count their actual subproblems. The
new min-marginal filter applies the same rounding bound conditionally on
a coordinate interval. Every surviving interval has a near-optimal grid
witness. Controlling all such witnesses, rather than only the returned
point, bounds the next grid independently of accuracy.

## An obstruction resolved without assuming it away

The older proposed route used a uniform bound on every bag's distance from
the optimizer. The [finite-certificate counterexample](tree-localization/counterexample.md)
shows that this is false on branching trees, even at fixed width, bounded
branching, uniform spectral conditioning, and exact slopes. The counterexample
uses legitimate finite dyadic partitions and concave-quadratic chord
relaxations; it is not merely a sensitivity analogy.

The familiar explanation is that many small influences can accumulate over a
growing tree. The new algorithms control their total error directly. The
counterexample does not establish failure of the older GR algorithm on its
own reachable partitions; that restricted question remains open.

## What this could enable

The reviewed [geometric copositivity certificate](new-direction/geometric-copositive-certificate.md)
provides a direct deterministic proof of a growth margin for a homogeneous
quadratic at an orthant corner. Independent rounding preserves cross terms
exactly, so only diagonal curvature enters the grid resolution. Homogeneity
reduces the certificate to a normalized shell, and one owned-variable OR
flag enforces its boundary condition in tree DP. The first accepted trial
discovers a verified margin within a factor sixteen of the best one. This
is a specialized certificate result, not a new general optimization class.

The [box-preordering obstruction](new-direction/box-preordering-growth-obstruction.md)
shows why certificate choice matters: a fixed rational Horn-matrix
perturbation, and connected chains of such blocks, have strong point growth
but no exact full box-preordering identity at any degree. Finite rectangular
subdivision does not repair that local obstruction. The geometric DP
certificate succeeds on the example; the note also gives a classical
vanishing-multiplier certificate. Thus no impossibility for all proof systems
or general solver hardness is asserted. The
[prior-art comparison](prior-art/box-quadratic-jet-certificate-prior.md)
separates these explicit bounds from established SPN, Pólya, local-global,
simplex-subdivision, and finite-state treewidth methods.

The reviewed [mixed-shell certificate](new-direction/mixed-shell-certificate.md)
extends this capability to a proposed rational point in a mixed box.
Physical distance shells separate lattice changes from the small continuous
neighborhood. Each shell has a geometric grid whose size depends on
`L/g` and logarithmically on dimension, while the encoded range affects
only the number of separate shell checks. An OR flag preserves the shell
condition under rounding. A final continuous ray argument covers the
neighborhood where all integer coordinates are fixed. The output is a
standalone growth and optimality certificate in the original metric.
Its advantage over the existing conditioned optimizer is the direct finite
certificate and verified conditioning, not a new solvability class.
The [earlier normalized version](new-direction/geometric-box-point-certificate.md)
remains valid but can inflate the parameter through side lengths or large
linear terms; the physical theorem avoids both losses.
Its reviewed [coordinate-fiber extension](new-direction/geometric-product-face-certificate.md)
handles nonunique optima when the supplied optimal-set candidate is
`{v} x Y`. After exact two-label unary reductions, constancy on the fiber
is a coefficient check. Free variables have only endpoint labels and add
no rounding loss; active mixed coordinates use physical shells. The
certificate proves distance-to-fiber growth in the original metric.
This is a specific extension beyond point optima, not a solution to
certifying arbitrary unknown unions or tilted optimal manifolds.
The reviewed [polynomial certificate](new-direction/nonlinear-shell-certificate.md)
extends point verification beyond quadratics. Outer rounding uses coordinate
semiconcavity instead of exact cross-term cancellation. Near the candidate,
the explicitly translated polynomial gives a rational bound on the higher
order remainder. One quadratic boundary test and continuous first-order
signs then certify that inner region. The construction discovers its growth
bound and keeps the physical conditioning parameter, but it requires a
rational candidate, explicit fixed-degree factors, and checked curvature
throughout the continuous hull. Nonrational optima and unique zero-growth
minima remain outside this exact certificate theorem.

A solver could use the continuous method as a component algorithm for a sparse
nonconvex box subproblem, with its existing convex relaxations. Its final
certificate has the size previously proved only around a known optimizer,
while the algorithm discovers a suitable center by global lower-bound solves.
The shared-grid method offers a different component for mixed boxes or
lower-envelope factors, including exact handling of finite modes and compressed
large integer intervals.

These are proved capabilities in specified oracle models. Competitive runtime
requires reliable subproblem solves, manageable curvature and growth ratios,
good decompositions, and sensible implementation. The work does not establish
a faster general MINLP solver. The reviewed
[inexact-oracle extension](regridded-certificates/inexact-oracles.md) permits
certified local lower and upper bounds, feasible local points, and controlled
gradient errors. Its selected local solve errors accumulate once per bag,
rather than once per task evaluated. Ordinary floating-point runs alone are
not certificates, and generic convex-oracle bit complexity remains outside
the proved bound.

## Prior work and verification

The [min-marginal audit](prior-art/minmarginal-prior.md),
[grid literature audit](prior-art/geometric-grid-prior.md), and
[sensitivity/DP audit](prior-art/tree-sensitivity-audit.md) identify the
strongest comparisons and their access limits. Exact DP already solves forest
box quadratics; certified treewidth approximation, continuous graphical-model
DP, adaptive grids, and iterative dynamic programming all have close prior
results. The potential contribution is the globally valid conditioned rate
and its stated extensions, not those individual mechanisms. Additional
terminology searches and source ingestion are ongoing.

The [hardness comparison](reviews/pruned-grid-hardness-sanity.md) checks
the actual width-two QP reduction. It has unique-optimum instances with
bounded coefficients but exponentially small global growth. This explains
why the new conditioning-dependent guarantee does not contradict that
hardness result; it is not evidence establishing the new proof.

Independent reviews support both main proofs, their arithmetic extensions,
and the tree counterexample. [The research record](PROGRESS.md) lists the
targeted commands and what their finite tests establish. A
[point-oracle lower bound](geometric-dp/oracle-limits.md) explains why the
shared-grid conditioning exponent cannot generally be removed in that model;
the hidden-well proof is classical in spirit and is not asserted as a new
complexity principle.

The occurrence parameter has now been removed for the mixed product-box
problem by changing the shared-grid algorithm. The
[feedback vertex set result and fan obstruction](new-direction/occurrence-free-qp.md)
remain useful: the former permits continuum recourse optima under growth
only in the core, while the latter limits the earlier closed-cell
certificate rather than all algorithms. The complementary negative-inertia
theorem, its mixed-polytope extension, nonlinear separable recourse, and
general-polytope nearby-point recovery have now passed independent review.
The sharp perturbation tail and expected exact-work theorem are further
reviewed milestones. Both the aligned-noise and independent ambient-noise
exact counterparts to the direct expected-cell method are now reviewed.
Current work seeks stronger mixed-integer extensions, improved dimension
dependence, and sparse certificates for arbitrary optimal sets without a
supplied growth bound. Significance is reassessed against
the strongest prior algorithms as these results develop.
The reviewed [scalar-message counterexample](new-direction/scalar-message-growth-obstruction.md)
rules out one proposed shortcut: even constant coefficients, treewidth two,
and uniformly bounded set-growth conditioning can require exponentially
many quadratic pieces in a complete scalar Bellman message. The example
has an immediate nonnegative-factor certificate, so this is a representation
obstruction, not hardness. The separate
[negative-curvature sparse note](new-direction/negative-curvature-sparse.md)
records a valid energy estimate and a classical proximal baseline; its
general sparse algorithm remains open.
The reviewed [PSD-extraction obstruction](new-direction/psd-extraction-curvature-obstruction.md)
rules out another specific shortcut. A scaled Horn family has fixed width,
fixed growth, and bounded negative curvature, yet every PSD-plus-nonnegative
subtraction leaving a copositive residual retains arbitrarily large
diagonal curvature. The prescribed common-grid rule consequently needs
arbitrarily many states. Joint convex recourse and coordinate changes are
outside the obstruction; a diagonal rescaling actually cures this family.
The [prior-art comparison](prior-art/psd-extraction-curvature-prior.md)
credits classical Horn and minimal-zero irreducibility results.

Two reviewed supporting results make the remaining sparse question more
precise. For any supplied strictly copositive residual, the
[Jacobi normalization calculation](new-direction/jacobi-copositive-residual.md)
gives the exact best curvature/growth ratio over positive diagonal
scalings; capping sufficiently large positive off-diagonal entries
preserves the normalized orthant margin. This removes the scaling search
but does not find a useful PSD/nonnegative extraction. Separately,
[articulation elimination](new-direction/articulation-copositive-elimination.md)
decides strict copositivity in `2^p poly(I)` when each biconnected block
has at most `p` vertices. Homogeneity makes a one-coordinate separator's
exact message a scalar quadratic, with rational witness recovery and
controlled bit length. This is a useful baseline under a stronger graph
restriction than treewidth; its relationship to classical block
decompositions is being audited, and no novelty is claimed.

Exact recovery with [finitely many optima](geometric-dp/exact-nonunique-box-qp.md), the
fixed-parameter bit bound, and stable nonlinear dynamics are now reviewed
milestones. Source ingestion and independent review continue. The reviewed
[algebraic-output example](geometric-dp/algebraic-output.md) also separates
the exact quadratic conclusion from polynomial approximation: expanded
minimal-polynomial output can be exponentially large for uniformly
conditioned quartics on a path, even though a compact radical representation
is small.
The reviewed [rectangular-precision obstruction](new-direction/implicit-optimum-precision-obstruction.md)
shows a distinct issue even with rational optimizers and global strong
convexity. Fixed-degree, fixed-width quartics with bounded `L/g` can force
exponentially many endpoint bits in any rational rectangle that verifies
an active derivative sign everywhere inside it. The bound holds for exact
range evaluation; it is not interval overestimation. Short correlated
recurrences and symbolic optimality proofs still exist, so this rules out
a specified enclosure format rather than compact implicit output generally.

The reviewed [convex-patch theorem](new-direction/implicit-convex-patch-certificate.md)
provides one constructive escape. It combines global polynomial pruning,
an extra integer-label filter, and a rational certificate of strong
convexity on the retained continuous box. The exact output is that verified
subproblem and its unique KKT point; arbitrary-precision position and value
evaluation have the same conditioned parameter bound. The hypothesis is
local Hessian positivity at the growth scale, not global convexity, so
the original problem may still be nonconvex. At boundary optima this
condition is genuinely stronger than point growth. A tiny positive
Hessian eigenvalue is insufficient for the stated bound. The
[focused comparison](prior-art/implicit-convex-patch-prior.md) credits the
classical ingredients and limits the contribution to the verified
construction and its parameterized bit guarantee.

The independent [nonlinear-frontier assessment](new-direction/nonlinear-frontier-significance.md)
keeps these capabilities distinct. Polynomial discovery is the broadest
solver consequence; the convex patch adds a useful exact output contract;
shells verify supplied rational candidates. None alone gives unrestricted
exact nonlinear optimization. That assessment's proposed sparse smoothed
polynomial target is now established in the reviewed theorem above. Its
separate deterministic boundary-certificate question remains open.

The exact preordering limitation is now sharpened by the reviewed
[width-two fan construction](new-direction/fan-preordering-growth-obstruction.md).
Its connected chains have fixed coefficients, exact growth `1/100`, and
`L/g<=206`, yet admit no exact unmultiplied box-preordering identity at
any degree. The non-SPN fan is classical; the explicit rational separator
and growth calculation make this certificate comparison checkable.
Geometric certificates remain applicable, and other certificate families
are outside the negative conclusion.
