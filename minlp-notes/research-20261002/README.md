# October 2 research continuation

The research question was how structural assumptions can make certified global
optimization faster. The user then requested completion of the current ideas
and extensions followed by a stop. This continuation is paused. The
[closeout](CLOSEOUT.md) gives the final results, verification and remaining
limits; the longer account below preserves the development and earlier work.

The final reviewed [globally convex polynomial theorem](new-direction/globally-convex-polynomial-point-oracle.md)
gives a deterministic fixed minimum-norm optimizer Cauchy oracle in
`poly_D(I+q)` bit time on bounded rational polytopes. Global convexity on
all of Euclidean space and fixed degree are essential premises. A
polynomial-bit constant in a degree-only distance error bound makes this
stronger than ordinary value approximation. The same rational-gradient
argument completes the existing core-noise interface to full-point output
when the supplied core quadratic convexifier is globally convex. The
[explicit affine-power corollary](new-direction/affine-power-core-point-oracle.md)
supplies a directly verifiable quartic and higher-degree class. The
[source audit](prior-art/globally-convex-polynomial-point-prior.md)
compares the strongest checked qualitative error-bound and convex-value
baselines without claiming publication priority.

The new reviewed [sparse polynomial theorem](new-direction/smoothed-sparse-polynomial.md)
extends expected exact optimization to explicit fixed-degree polynomial
factors on mixed boxes. Under one finite rational law of independent linear
noise, it returns an exact optimizer on every draw and has expected work
`C^p [4+(1+n/2)L w_max/(2sigma)]^p poly_d(I)`. Here `p` is supplied bag
size, `L` bounds coordinate curvature on the full continuous hull, and
`sigma` is the noise half-width. The law has polynomially many sampling
bits and is chosen before sampling. Integer dimension is unrestricted;
no growth, uniqueness, or boundary-Hessian promise is required.

The usual exact output is a rational strongly convex subproblem defining
the optimizer, with certified `q`-bit position and value evaluation in
`poly_d(I+q)` work. Tied and degenerate draws use an exact algebraic
fallback on that same sample; its expected cost is paid for by the
finite-noise tails. Compact patch descriptors have polynomial size;
complete global pruning certificates have the displayed expected-size
bound. The [source comparison](prior-art/sparse-smoothed-polynomial-prior.md)
credits classical generic growth, real-algebraic algorithms, and convex
optimization. The added capability is the finite-noise sparse exact-work
composition, not a new genericity principle. The numerical scale and
fixed-width restrictions remain material; solver performance is untested.

The reviewed [polynomial graph corollary](new-direction/smoothed-polynomial-graph-constraints.md)
allows overlapping equalities whose bounded-depth polynomial parameterization
preserves sparse factors. It conditions on dependent-coordinate noise while
retaining independent free-coordinate noise. Curvature is measured after
substitution, and additional constraints cutting the free box are excluded.
An [affine feasibility reduction](new-direction/constrained-smoothing-barrier.md)
explains why objective perturbations alone cannot justify a corresponding
theorem for arbitrary sparse mixed constraints.

The width dependence is an actual limitation of the current rule. A reviewed
[connected quartic family](new-direction/global-error-cell-barrier.md) forces
at least `(5n/(6p))^(p/2)` retained cells on every noise draw. The instances
are easy by endpoint DP; the lower bound concerns the specified global-error
retention and whole-hull closure tests. A
[star counterexample and recourse interface](new-direction/local-error-recourse-interface.md)
show both why simply substituting a bag-local error is unsound and what
certified conditional optimization would suffice to remove the dimension
factor. An efficient general recourse construction remains open.

A reviewed [exact recourse theorem](new-direction/smoothed-box-stable-recourse.md)
does supply that route for a tractable residual class. On a continuous
unit box, fixing a supplied `k`-coordinate core must leave an exact
polynomial-bit QP solver that remains valid under further coordinate
interval restrictions. Expected work is
`8^k [3+(1+k/2)L/(2sigma)]^k poly(I)` under one finite independent
ambient-noise law; every draw returns an exact rational optimizer and
value. At most `2n` additional recourse calls exclude distant residual
solutions and certify containment in a local box before convex closure.
Deleting the core to a forest provides a concrete nonconvex residual
class through the established forest-QP oracle. This is FPT in the core
size and displayed ratio, with no growth promise, but it does not settle
FPT in treewidth. The global-error counterexample and general recourse
question remain relevant.

The reviewed [polynomial recourse theorem](new-direction/smoothed-polynomial-box-recourse.md)
allows certified approximate values and feasible completions in place of
exact rational recourse. Dense convex polynomial residuals satisfy the
interface, even without strong convexity. Expected work is
`8^k [3+(1+k)L/(2sigma)]^k poly_d(I)`, with exact implicit optimization
on every draw of one finite ambient-noise law. Certified lower bounds
exclude residual regions before a nonlinear Hessian test closes the
remaining patch. Rational tangent gaps make convex recourse certificates
directly checkable. A [degree-five family](new-direction/polynomial-recourse-rank-separation.md)
has one core variable while every fixed PSD quadratic convexification
requires rank at least the residual dimension. This separates structural
parameters, not computational hardness. The
[assessment](new-direction/polynomial-box-recourse-significance.md) and
[prior audit](prior-art/smoothed-polynomial-box-recourse-prior.md) distinguish
the expected exact-work contribution from classical partial-convex search.

The reviewed [integer recourse theorem](new-direction/smoothed-native-integer-recourse.md)
couples the continuous core to a fixed constrained native-integer set.
Its exact conditional oracle must remain polynomial under coordinate-bound
restrictions. Expected work is
`[8^k(3+(1+k/2)L/(2sigma))^k+c_d^k] poly_d(I)`, using the reviewed
constant-base algebraic solver. A gap certified by at most twice the residual
dimension in oracle calls fixes the entire integer assignment. Exact
algebraic optimization over the whole remaining core then returns ordinary
isolating-polynomial representations, even for degenerate core optima.
The [source audit](prior-art/integer-convex-flow-recourse-prior.md) verifies
classical convex-cost flow and TU oracles with logarithmic capacity
dependence. No integer-dimension or graph-width parameter is needed;
the residual feasible set must be independent of the core.

The reviewed [interior-flow extension](new-direction/smoothed-interior-core-flow.md)
retains that bound with noise only on the core. Its extra premise places
every optimal core point in the interior for every supported noise.
One flow's polynomial residual-cost potentials certify optimality over
the retained box without requiring a unique winning flow. A classical
algebraic tube estimate bounds proximity to changes of this certificate.
The [boundary example](new-direction/core-only-flow-boundary-obstruction.md)
shows why this particular test can fail on a fixed positive-probability
event despite well-conditioned core growth. The reviewed
[boundary-flow theorem](new-direction/smoothed-boundary-core-flow.md)
now removes interiority by representing the whole tied-flow set as
tightened arc intervals. Its inward-derivative and outside-cost tests
certify the correct core face without enumerating flows. Expected work is
`f_d(k)[3+(1+k/2)L/(2sigma)]^k poly_d(I)`, with exact output on every draw.
Its larger `f_d(k) poly_d(I)` sampling precision is charged explicitly.
The reviewed [bilinear specialization](new-direction/smoothed-bilinear-core-flow.md)
restores the preceding constant-base expected-work bound and polynomial
sampling precision. Its adjusted marginal charts are affine, so their
distance-to-zero margin has a direct polynomial-bit bound. Core curvature
depends only on the core objective. The
[significance assessment](new-direction/boundary-core-flow-significance.md)
compares exact sampled-instance optimization with the existing deterministic
objective-approximation baseline and explains the remaining solver work.
The reviewed [TU recourse extension](new-direction/smoothed-core-tu-recourse.md)
replaces network constraints by fixed totally unimodular equalities or
inequalities on bounded native integers. Compact adjacent-slope duals
and conformal unit circuits give the same certificate and bounds;
inequalities use explicit finite slack bounds. The
[prior audit](prior-art/tu-equality-separable-convex-prior.md) separates
these classical ingredients from the smoothed global-search guarantee.

The reviewed [core-only-noise theorem](new-direction/core-only-noise-boundary-recourse.md)
instead strengthens continuous recourse under a verified uniform residual
strong-convexity modulus. The same expected count needs noise only on the
small core, even with changing residual active faces and zero multipliers.
A [finite-grid tube bound](new-direction/core-noise-active-stratum-tube.md)
controls proximity to changes of active pattern, and a
[curvature lemma](new-direction/small-residual-multiplier-curvature.md)
allows weakly active residual coordinates to remain free. No interiority
or explicit residual chart is supplied. This class does admit a fixed
rank-`k` quadratic convexification; the gain is the original `L/sigma`
count and exact core-only-noise completion. The earlier
[rotating-fiber examples](new-direction/core-only-noise-rotating-fiber.md)
explain why merely convex or strictly convex residuals need a different
certificate.

The reviewed [regularization investigation](new-direction/core-only-noise-regularization-limit.md)
closes one attempted extension. An explicit convex quartic with bounded
coefficients requires at least `2^n` ordinary rational parameter bits for
constant point accuracy along its isotropic Tikhonov path. A complementary
[growth lemma](new-direction/canonical-convex-fiber-regularization.md)
gives a degree-only distance exponent on compact polytopes, but the
quartic forces a superpolynomial precision constant. These are limitations
of that method and its quantitative error bound; the example itself has
an easy structural solution. General efficient exact residual point
extraction remains open here, and the growth lemma's prior comparison
is recorded in the [focused audit](prior-art/convex-polynomial-error-bounds-prior.md).
The most closely related Yang paper remains abstract-only, so priority
is unresolved.

The reviewed [two-copy quartic reduction](new-direction/convex-point-radical-comparison.md)
goes beyond a regularization limitation. A point within distance `1/4`
of any optimizer decides Square Root Sum, even for a unique optimizer,
treewidth two, bounded coefficients, and a unit box. Deterministic
polynomial evaluation would put that comparison problem in P; an
always-correct expected-polynomial method gives a Las Vegas algorithm.
No NP-hardness or difficulty of objective approximation is claimed.
The [assessment](new-direction/convex-point-comparison-assessment.md)
separates these output contracts and proves a separate size bound for
explicit univariate coordinate polynomials. The
[prior comparison](prior-art/convex-point-radical-prior.md) credits the
established strong-approximation reductions for Nash equilibria;
publication priority for this convex optimization construction is open.
The separately reviewed [PosSLP construction](new-direction/posslp-convex-point-extraction.md)
encodes bounded arithmetic circuits by a strongly convex weighted
quartic, then applies the paired comparison mechanism. Constant point
accuracy decides the circuit's integer-output sign. The final polynomial
is convex on its box and has a unique optimizer; its interaction width
is unrestricted. The [prior audit](prior-art/convex-point-posslp-prior.md)
compares existing arithmetic reductions to Nash approximation and exact
semidefinite feasibility. Neither reduction establishes NP-hardness or
an obstruction to objective-value approximation.

The reviewed [fixed-law value oracle](new-direction/all-scale-core-value-oracle.md)
handles arbitrary convex polynomial recourse and any supplied core size,
with no residual noise. One finite draw supports every accuracy `2^-q`
with expected work `f_d(k)(1+L/sigma)^k poly_d(I+q)`. It returns a rational
feasible point and a global objective interval, without a residual
point-distance promise. A padded near-optimal convex hull gives a count
valid at every scale. Convex conjugacy and a covering argument bound its
tail; a compact semialgebraic formula transfers that bound to the fixed
finite law. Capping generated cells pays for exact fallback on exceptional
draws. The [fresh review](reviews/all-scale-core-value-oracle-review.md)
passes after an independently rechecked formula-encoding correction.
The simpler [one- and two-core proof](new-direction/core-only-noise-value-oracle.md)
is retained as the predecessor. The
[prior comparison](prior-art/all-scale-core-value-oracle-prior.md) credits
classical tools and related smoothed algorithms; priority remains unresolved.
The reviewed [core-coordinate addendum](new-direction/core-only-noise-core-oracle.md)
also gives arbitrary coordinate accuracy for one fixed globally optimal
core at the same expected cost. Its retained hull contains both every
optimal core and the feasible incumbent. A rational diameter test certifies
the error, and the projected-growth tail pays for a second fallback event.
No residual-coordinate accuracy is inferred. The
[independent assessment](new-direction/all-scale-core-value-significance.md)
explains the accuracy gain for one perturbed instance, the `k sigma`
original-objective regret, and the remaining solver requirements.

The reviewed [coupled-polytope theorem](new-direction/coupled-polytope-core-value-oracle.md)
allows general bounded rational linear constraints if the supplied
correction `F+alpha||v||^2/2` is convex on the feasible polytope.
Relative affine-hull reduction and rational feasibility repair provide
the convex cell oracle, including lower-dimensional cells. Whole-cell
packing extends the all-scale count without assuming continuity of a
partially minimized value function. Value and
[selected-core output](new-direction/coupled-polytope-core-oracle.md)
have expected `f_d(k)(1+alpha/sigma)^k poly_d(I+q)` work under one
finite law. This stronger feasibility model charges `alpha`, which
can exceed the product theorem's original coordinate curvature.
A reviewed [QP reconstruction corollary](new-direction/qp-core-cauchy-reconstruction.md)
uses polynomial rational height to recover exact core coordinates and
value, then completes the convex fiber exactly. It preserves the box
or coupled theorem's respective parameter; it is not the first local
exact-QP result or a new exact convex-QP algorithm.

For globally convex objectives, a reviewed
[coordinate theorem](new-direction/joint-convex-core-point-oracle.md)
removes the exponential core-size factor altogether. Convex optimization
bounds each coordinate of a buffered near-optimal sublevel set. Its
rational diameter certifies distance to one fixed selected optimal core;
the projected-growth tail pays for rare exact fallback. Expected work
is ordinary `poly_d(I+q)` under one finite rational noise law, with
coefficient and noise magnitudes charged through their binary lengths.
Only perturbed coordinates receive the distance guarantee. Full point
output therefore requires perturbing every coordinate.

The reviewed [convex cubic theorem](new-direction/convex-cubic-point-oracle.md)
gives a deterministic alternative on bounded rational boxes. An affine
PSD Hessian has a common rational kernel; cubic symmetry and an explicit
Hoffman bound give a computable polynomial-bit constant in a fourth-root
distance-to-optimum bound. A certified convex value solve consequently
approximates the optimizer set in `poly(I+q)` bit time. An effective
regularization schedule also approximates the fixed minimum-norm optimizer
in the original coordinates. No strong-convexity or unique-optimum promise
is needed. The proof and canonical corollary have independent reviews;
the degree-three versus degree-four comparison does not by itself establish
novelty or a complexity-class separation. The reviewed
[polytope addendum](new-direction/convex-cubic-polytope-point-oracle.md)
now covers arbitrary bounded rational polytopes, including lower-dimensional
ones. A rational interior ball replaces center symmetry, and exact
homothety repairs weakly feasible outputs. The
[source audit](prior-art/convex-cubic-point-oracle-prior.md) compares
exact convex QP, qualitative polynomial error bounds and convexity
recognition; priority remains unresolved.

The reviewed [full-point cubic completion](new-direction/cubic-core-full-point-oracle.md)
uses that structure for a possibly nonconvex total cubic with a supplied
joint core quadratic convexifier. For one fixed finite core-only noise
draw it approximates the minimum-norm point in the lexicographically
first optimal core's fiber, with expected
`f(k)(1+alpha/sigma)^k poly(I+q)` work. A separate completion penalty
uses `alpha+1` without changing the search parameter. Rational equality
rows describe the target fiber despite its unknown irrational core;
a short core approximation then suffices for a convex regularized solve
on the original polytope. This avoids assuming continuity of moving
optimal fibers. Full residual coordinates are now controlled, but exact
active labels and short expanded algebraic coordinates remain outside
the guarantee. The [independent assessment](new-direction/convex-cubic-point-significance.md)
separates this capability from the quadratic baseline and quartic barriers.
The [residual-convex cubic closing note](new-direction/residual-convex-cubic-boundary.md)
records fixed face kernels and conditional margin bounds under weaker
assumptions, but does not prove a full point algorithm. Its counterexamples
limit two proposed transfers without asserting hardness.

A separate reviewed [strong-field theorem](new-direction/strong-field-component-polynomial.md)
handles fixed-degree mixed-box polynomials without a width parameter
when linear noise dominates derivative variation and integer label counts.
Strict monotonicity pins coordinates; the remaining independent random
components are solved by a reviewed
[`c_d^k poly_d(H)` algebraic procedure](new-direction/polynomial-component-primitive-limit.md).
The exact output keeps separate component representations and a symbolic
value sum, with certified numerical refinement. The perturbation can be
large, and no general exact comparison of unrelated algebraic sums is
promised. Its probability argument and algebraic ingredients have separate
reviews; publication priority is unresolved.

The reviewed [simplex-block theorem](new-direction/simplex-block-smoothed-extension.md)
extends expected exact implicit optimization to products of resource
simplices `x>=0, sum x<=1`, probability simplices `sum x=1`, and native-
integer intervals. Factors may couple the blocks. Feasible block rounding,
counts stratified by original faces, and strict derivative differences
replace coordinatewise box arguments. A relative convex polytope defines
the usual exact output and supports certified polynomial-bit evaluation.
The rate remains fixed-width polynomial under explicit numerical bounds;
bags must contain whole blocks and curvature is bounded on block Hessians.
Overlapping resource constraints are excluded. The
[prior audit](prior-art/simplex-block-smoothed-prior.md) credits established
rounding, KKT, genericity, and convex optimization ingredients.

The reviewed [implicit-graph theorem](new-direction/smoothed-implicit-graph-constraints.md)
goes beyond explicit polynomial substitution. Dependent coordinates are
unique roots of sparse scalar polynomial equations with globally verified
brackets and positive derivative floors over a retained mixed product box.
Reduced costs can be algebraic. Rational interval costs give sound sparse
DP, and approximate derivative certificates close a strongly convex patch.
Expected work is `C^p [4+(1+n)L w_max/(2sigma)]^p poly(I)` in the expanded
retained bags. Every draw has an exact implicit optimizer; rational
retained coordinates with root equations represent exactly feasible
approximating points. Independently rounded physical coordinates need
not satisfy the equalities. The global parameterization and pullback
curvature premises are essential. Its
[prior audit](prior-art/implicit-monotone-actuator-prior.md) distinguishes
this guarantee from existing implicit-state spatial branch-and-bound.

The reviewed [order-polytope theorem](new-direction/smoothed-sparse-order-polynomial.md)
handles genuinely overlapping inequalities `x_i<=x_j` on a continuous
unit box, including cycles. Common-threshold rounding preserves every
order constraint and sparse whitelist. Bag order chambers permit a finite
noise count despite changing conditional feasible sets. LP exposure gaps
certify active equalities without choosing unique KKT multipliers, and
the retained convex patch gives exact implicit output on every draw with
same-draw fallback. Expected work is
`C^p p! (p+1) [2+nH(p+1)/(2sigma)]^p poly_d(I)`.
Here `H` bounds the full Hessian above; a diagonal curvature bound alone
does not suffice. The [source comparison](prior-art/order-polytope-smoothed-prior.md)
credits Stanley's geometry and Bach's common-quantile isotonic coupling.
The theorem is fixed-width polynomial.

The reviewed [mixed order theorem](new-direction/smoothed-mixed-order-polynomial.md)
adds unrestricted binary variables and improves the directional count:
`C^p q! (q+1) [2+3NH/(4sigma)]^q poly_d(I)`, where `N` counts continuous
variables and `q` their maximum number per bag. Endpoint-preserving
transport provides feasible conditional upper supports even when the
projected mixed domain is nonconvex. Pruning fixes every binary label
before applying continuous face certificates. This covers implications
and continuous activation bounds, but excludes arbitrary integer ranges
and general affine constraints. The rate is not FPT in width.

The current constrained-MIQP frontier is the reviewed
[Gaussian-like ambient theorem](new-direction/smoothed-gaussian-miqp.md):
expected exact `f(m,k,1+nu diam(P)/sigma) poly(I)` work under one
base-chosen independent finite rational law, with correctness on every
draw. The [sparse mixed theorem](new-direction/sparse-bag-cell-smoothed-miqp.md)
instead permits arbitrary integer dimension and negative inertia and gives a fixed-width
polynomial bound. These are distributional guarantees for sampled
objectives, with explicit numerical scales; prior art and practical value
are assessed separately below.

The main deterministic sparse framework is the reviewed
[filtered coordinate-grid algorithm](new-direction/pruned-coordinate-grid.md)
for exact rational mixed-integer box QP. It has bit complexity
`f(p,kappa) poly(I)`, where `p` is bag size and `kappa` compares upper
coordinate curvature with global quadratic growth. Exact min-marginals
remove intervals that cannot improve the incumbent, bounding subsequent
grids independently of accuracy. The polynomial input exponent is absolute;
there is no occurrence parameter or supplied growth constant. Two proof
reviews and targeted exact DP checks support the result. The
[prior-art audit](prior-art/minmarginal-prior.md) separates the conditioned
bound from established filtering and adaptive-grid methods.

A reviewed [geometric certificate](new-direction/geometric-copositive-certificate.md)
specializes the rounding argument to sparse homogeneous quadratics on the
nonnegative orthant. Without a supplied margin, it finds and verifies
`sigma` in `[g/16,g)` in `f(p,L/g) poly(I)` work. One normalized finite
grid and a two-state DP suffice per trial; no target accuracy or exact-value
recovery is needed. A separate [obstruction](new-direction/fan-preordering-growth-obstruction.md)
gives connected examples of arbitrary dimension with treewidth two and
bounded `L/g` that have no full unmultiplied box-preordering certificate at
any degree. The geometric certificate covers these examples, while a
classical vanishing-multiplier certificate provides another escape.
This sharpens the earlier [Horn construction](new-direction/box-preordering-growth-obstruction.md)
using a classical non-SPN fan. The explicit rational witness, growth
`1/100`, and chain curvature/growth bound `206` have passed fresh review;
discovery of a non-SPN fan is not claimed.
The [focused audit](prior-art/box-quadratic-jet-certificate-prior.md)
credits existing copositivity, positivity-certificate, and treewidth methods;
priority of the precise parameter bound remains unestablished.

The reviewed [physical-shell extension](new-direction/mixed-shell-certificate.md)
certifies a proposed rational solution of any mixed-box QP with a supplied
interaction decomposition. It discovers a valid Euclidean growth margin
`sigma` satisfying `L/sigma <= max(32,12L/g)` in
`f(p,max(1,L/g)) poly(I)` work. Each shell uses feasible integer and
continuous grids; only the innermost region uses a ray argument, with
integer coordinates fixed. The method preserves the original diagonal
curvature scale and charges encoded widths through a polynomial number
of shells. It verifies a candidate and does not discover it. The earlier
[signed normalized certificate](new-direction/geometric-box-point-certificate.md)
is retained with its metric and scale limitations explicit. The
[focused comparison](prior-art/mixed-shell-certificate-prior.md) distinguishes
the direct finite certificate from existing conditioned optimization,
treewidth DP, and exact branch-and-bound methods.
The reviewed [coordinate-fiber corollary](new-direction/geometric-product-face-certificate.md)
certifies an entire supplied optimal set `{v} x Y`, with both active and
free coordinates allowed to be mixed. It checks constancy on that set and
uses free endpoint labels alongside active physical shells, preserving
the same physical curvature/growth bound. This verifies a compact supplied
description; it does not discover arbitrary optimal sets.
The reviewed [nonlinear extension](new-direction/nonlinear-shell-certificate.md)
applies to explicit fixed-degree rational polynomial factors on mixed boxes.
Sequential mean-preserving rounding controls outer shells using a verified
upper coordinate-curvature bound on the entire continuous box hull. A
coefficient Taylor remainder and one quadratic boundary certificate handle
the small region where all lattice coordinates are fixed. It discovers a
valid margin with `L/sigma <= max(32,20L/g)` in conditioned FPT work.
The candidate must be supplied and rational, and positive point growth is
a genuine assumption: a unique polynomial minimum can have zero growth.
The [prior-art audit](prior-art/nonlinear-shell-certificate-prior.md)
compares sparse SOS, Bernstein, treewidth approximation, and polynomial
branch-and-bound results without claiming priority.

The reviewed [polynomial pruning theorem](new-direction/polynomial-pruned-grid-extension.md)
finds an optimizer rather than requiring a candidate. Explicit fixed-degree
polynomial factors give certified mixed-box approximation in
`f_d(p,kappa) poly(I+q)` for gap `2^-q`. For native-integer boxes, refining
below the rational objective-value spacing yields an exact optimum in
`f_d(p,kappa) poly(I)` work. This is a bit-complexity extension of the
existing semiconcave pruning argument, with a standard discrete stopping
step; it is not a new grid mechanism. The
[focused comparison](prior-art/polynomial-pruned-grid-prior.md) records the
strongest sparse and fixed-dimension polynomial approximation precedents.

The reviewed [convex-patch theorem](new-direction/implicit-convex-patch-certificate.md)
adds exact implicit output for mixed polynomial boxes. Global pruning
fixes the integer labels and retains every optimum in a rational box;
an exact Hessian certificate makes its continuous restriction strongly
convex. That subproblem uniquely defines the original optimizer, even
when its coordinates are irrational, and supports certified `q`-bit
position and value evaluation in `f_d(p,kappa) poly(I+q)` work. Construction
and output length are `f_d(p,kappa) poly(I)`. The runtime guarantee needs
the continuous Hessian at the optimum to dominate the growth scale.
Interior optima satisfy this automatically; boundary optima need the
additional assumption. The method avoids the reviewed
[rectangular active-sign precision obstruction](new-direction/implicit-optimum-precision-obstruction.md)
without resolving active signs explicitly. The
[prior-art comparison](prior-art/implicit-convex-patch-prior.md) separates
this conditioned construction from established interval, KKT, and
convexification methods.

Without the boundary-Hessian premise, reviewed
[coordinate enclosures](new-direction/deterministic-boundary-output.md)
still give certified position and value approximation in conditioned FPT
work. They do not provide a finite uniqueness certificate. The same note
constructs a strict nonglobal local minimum doubly exponentially close to
the global optimizer at fixed degree, width, and conditioning, limiting
closure by a polynomial-radius stationary-point neighborhood. Separately,
an [active-bound reduction](new-direction/convex-active-set-radical-comparison.md)
encodes Square Root Sum in a uniformly strongly convex cubic of width two.
It distinguishes exact active-set decisions from implicit convex output;
it is not an NP-hardness claim.

The earlier [regridded bit algorithm](geometric-dp/regridded-qp-bit.md)
has an additional occurrence parameter and stronger curvature assumptions.
Its continuous certificate framework and nonlinear constrained extensions
remain separate contributions.

A second reviewed [exact QP theorem](new-direction/negative-inertia-qp.md)
allows any bounded rational polytope and has bit complexity
`f(k,max(1,nu/g)) poly(I)`, with negative inertia `k` and
`nu=max(0,-lambda_min(A))`, the magnitude of the most negative Hessian
eigenvalue. Positive curvature affects input arithmetic rather than this
conditioning parameter. It uses rational spectral normalization and exact convex
recourse. This provides a complementary route for dense problems with
few nonconvex directions. A projected version permits continuum residual
optima. Its mechanisms have close prior results; the candidate addition
is the conditioned exact complexity bound.

The reviewed [mixed-polytope extension](new-direction/negative-inertia-miqp.md)
adds integer dimension `m` as a parameter, giving exact
`f(m,k,max(1,nu/g)) poly(I)` complexity. It uses the existing exact
fixed-parameter convex MIQP algorithm as its recourse oracle. Integrality
is retained inside that oracle.

A separate [proximal grid theorem](new-direction/proximal-growth-grid.md),
with [stationary-face recovery](new-direction/proximal-exact-recovery.md),
gives exact `f(p,kappa) poly(I)` mixed-box QP with arbitrary optimal sets,
including continua. This version requires a supplied valid growth bound.
Its interval and stopping guarantee depend on that promise; final rational
checks do not independently validate it. Neither the number of optimal
components nor their coordinate projections is a parameter.

Two reviewed extensions broaden these results. The
[finite-mode corollary](new-direction/pruned-grid-finite-modes.md) permits
tied discrete modes outside the growth metric, including endpoint choices
for nonpositive-diagonal coordinates. The
[nonlinear recourse theorem](new-direction/approximate-convex-recourse.md)
covers separable convex quartics with low-rank concave quadratic coupling
on mixed boxes, with arbitrarily many integer variables. It gives certified
approximation and exact purely integer optimization. The
[prior comparison](prior-art/separable-lowrank-minlp-prior.md) identifies
easy rank-one and binary subclasses that already have simpler algorithms.

A reviewed [linear-perturbation theorem](new-direction/smoothed-linear-growth.md)
gives an explicit high-probability global growth bound. For rational QP,
polynomial-bit noise sampling is sufficient; active faces enter only a
counting proof, not an enumeration algorithm. Combined with the two main
algorithms, this gives high-probability polynomial work at fixed structural
parameter when the displayed numerical scales are polynomially bounded.
It optimizes the perturbed instance and does not establish expected
smoothed polynomial time.
The reviewed [summed-response refinement](new-direction/summed-response-growth.md)
improves the dimension dependence from `n^2` to `n log(n/rho)` at failure
probability `rho`. The [significance review](reviews/smoothed-growth-significance.md)
explains the classical qualitative background and the remaining priority risk.

Two subsequent results strengthen that statement. The reviewed
[proximal growth tail](new-direction/proximal-growth-tail.md) proves the
sharp bound `Pr(g* < eps) <= 2 eps sum_i phi_i w_i` for any continuous
objective on a compact set under independent linear noise with density
bounds `phi_i` and coordinate widths `w_i`. Its rational QP version uses
polynomial-bit sampling. The reviewed
[expected exact-work theorem](new-direction/expected-smoothed-qp.md)
combines the conditioned solver with an exact fallback: for at most two
negative Hessian eigenvalues, expected bit work is
`poly(I) (1 + nu sum_i w_i / sigma)` under the specified rational-grid
noise of half-width `sigma`. It returns an exact answer on every draw,
including ties, and never resamples. This is expected polynomial time
when the displayed numerical ratio is polynomially bounded. It solves
the sampled objective; priority and practical performance remain unproved.

The reviewed [exact cell-closure theorem](new-direction/smoothed-exact-cell-closure.md)
removes the two-negative-direction restriction under a different noise
law: independent coefficients in the supplied negative-factor coordinates.
It recognizes quadratic regions of the convex recourse value function and
solves covered cells exactly. Unresolved cells force the noise near finitely
many hyperplanes; an exact fallback pays for those draws. This gives expected
`f(k,1+nu diam(X)/sigma) poly(I)` exact bit work under one fixed rational
sampling law, without a growth assumption. The original coefficient noise
is generally correlated, so this does not subsume the independent-coordinate
theorem's perturbation model.

The reviewed [ambient-noise extension](new-direction/smoothed-ambient-cell-closure.md)
now handles independent noise in every original linear coefficient for any
negative inertia. A cube-volume estimate bounds local events even though
the projected factor coefficients are dependent; scalar section counts
transfer that estimate to one fixed rational sampling law. Exact closure
and a same-draw fallback give an exact solution on every draw, with expected
polynomial bit work at each fixed inertia under the displayed numerical
bounds. Its `n^{O(k)}` dependence is weaker than the aligned model's FPT
bound. The [prior comparison](prior-art/smoothed-cell-closure-prior.md)
credits classical parametric global-QP reductions and critical-region
algorithms; the [ambient audit](prior-art/smoothed-ambient-noise-prior.md)
separates the expected-work claim from those ingredients.

The reviewed [Gaussian-like ambient theorem](new-direction/smoothed-gaussian-cell-closure.md)
improves that dimension dependence under a different independent noise
law. Gaussian projection separates the factor and residual vectors, and
a weighted grid sum controls local events without the auxiliary box width.
A bounded finite rational sampler, fixed from base data, transfers the
bound to exact bit computation. Expected work is
`f(k,nu diam(X)/sigma) poly(I)`, with an absolute input exponent.
It solves every sampled draw exactly; the continuous Gaussian is a proof
device, not a real-number input oracle.

The reviewed [general MIQP closure theorem](new-direction/smoothed-miqp-cell-closure.md)
extends uniform ambient noise to bounded mixed polytopes. At each query,
at most twice the integer dimension in additional convex MIQP solves finds
the best competing integer assignment. A sufficient gap certifies the
winner throughout a cell; a failed test near the optimum implies a rare
original-label near-tie. Expected work is
`f(m) C^k (1+H_amb) poly(I)` with the same explicit dimension-dependent
geometric factor. The exact fixed-parameter convex MIQP oracle is prior work.
The separately reviewed [Gaussian-like composition](new-direction/smoothed-gaussian-miqp.md)
removes those ambient dimension powers. It gives expected
`f(m,k,1+nu diam(P)/sigma) poly(I)` exact work, with an absolute input
exponent and `P` the continuous relaxation. A scalar Gaussian-isolation
bound controls label failures, while a base-only support/precision loop
handles the support-dependent gap threshold. The prior oracle and
isolation principles are credited in the [focused audit](prior-art/smoothed-exact-miqp-prior.md).

The reviewed [separable mixed theorem](new-direction/smoothed-mixed-separable-closure.md)
permits arbitrarily many integer and continuous variables on product boxes.
Convex piecewise quadratics with rational coefficients and breakpoints,
minus supplied low-rank concave coupling, admit exact scalar recourse and
polyhedral cell certificates. The aligned law gives an expected FPT bound;
the uniform ambient law gives the stated fixed-rank polynomial bound.
Neither version assumes growth, smooth recourse, or unique integer winners.
The reviewed [anisotropic Gaussian extension](new-direction/anisotropic-gaussian-separable-closure.md)
preserves scalar recourse while removing the numerical conditioning
assumption on a supplied full-row-rank factor. Its expected exact bound is
`f(k,1+beta diam(X)/sigma) poly(I)` under the specified finite independent
Gaussian-like coefficient law. Here `beta=alpha ||T||^2` measures the
supplied concave term, rather than the full objective's negative curvature.
Very small factor singular values affect precision and cutoff, but do not
enter the numerical parameter in the expected count.

For sparse problems, the reviewed
[bag-cell theorem](new-direction/sparse-bag-cell-smoothed-qp.md) gives exact
output on every draw with arbitrary negative inertia and variable occurrence.
Sparse min-marginal tables retain only cells with a consistent near-optimal
witness; independent bag noise bounds their expected number. Gradient-sign
tests on retained hulls identify original box bounds, and a PSD test permits
exact convex closure. The cutoff and noise law are fixed from base data;
rare draws use exact enumeration. Expected work is polynomial at fixed
treewidth under the displayed curvature/width/noise bounds, with an input
exponent depending on width. The [hardness check](new-direction/sparse-smoothed-hardness-sanity.md)
shows why inverse-polynomial noise does not preserve the decision threshold
in the known bounded-coefficient width-two reduction.
The reviewed [mixed extension](new-direction/sparse-bag-cell-smoothed-miqp.md)
uses integer grid steps down to one, followed by singleton integer cells.
Compatible rounding and independent bag-noise counts remain valid. Exact
closure first fixes every integer hull to a singleton, then applies the
continuous gradient and PSD tests. Integer dimension and negative inertia
are unrestricted; numerical integer widths remain in the expected count.

The reviewed [direct cell-count theorem](new-direction/smoothed-semiconcave-cells.md)
instead bounds expected approximation work without any growth assumption.
At fixed dimension, upper coordinate curvature and independent linear noise
give expected logarithmic accuracy dependence for a concrete cell search.
Convex recourse applies this to noise in the low-rank factor coordinates.
Its finite-bit noise law is chosen for the requested accuracy; exact
optimization under one fixed finite law requires the additional closure
mechanism above.

For nonlinear integer optimization, the reviewed
[low-rank integer theorem](new-direction/smoothed-integer-low-rank.md)
covers separable convex quartics minus a concave quadratic of supplied
rank. Under one fixed rational factor-noise law it returns an exact
optimizer on every draw, with expected fixed-parameter work in rank and
the displayed projected-range/noise ratios. There may be arbitrarily many
integer variables and binary-encoded interval lengths. Exact separable
recourse avoids label enumeration, and the original objective lattice
makes the final gap exact. No growth assumption or fallback is needed.
Binary and explicitly listed domains have stronger deterministic baselines;
the [prior audit](prior-art/smoothed-exact-separable-lowrank-minlp-prior.md)
also compares smoothed Pareto counts after projection.

The [general-polytope recovery extension](new-direction/proximal-polytope-recovery.md)
also permits arbitrary optimal sets in the mixed-polytope theorem when a
valid full-distance growth bound is supplied. A nearby feasible point
selects constraint equalities, and linear stationarity recovers an exact
optimizer. Its promise-dependent scope matches the proximal box theorem.

A complementary reviewed [feedback vertex set theorem](new-direction/fan-exploration.md)
gives exact `f(r,kappa) poly(I)` bit complexity when a supplied set of `r`
coordinates leaves a forest. It requires a unique optimal core and growth
only in those coordinates; residual optima may form a continuum. Such a
core automatically has some positive growth constant, but quantitative
conditioning still controls the runtime. The exact forest oracle and the
quadratic-growth box-counting principle are prior results. The
[occurrence-free overview](new-direction/occurrence-free-qp.md) explains
what this adds and why it does not settle arbitrary bounded treewidth.

The broader [geometric-grid method](geometric-dp/theorem.md) handles mixed
integer–continuous boxes under weaker coordinate-curvature assumptions.
Both methods cover branching decompositions and boundary minima. Their
proofs and arithmetic extensions have passed independent adversarial review;
targeted rational checks support the algebra. Practical significance and
prior art are assessed separately.
**Publication priority and competitive solver performance are not established.**

A companion [counterexample](tree-localization/counterexample.md) disproves
the unrestricted claim that relaxed dynamic-programming solutions remain
uniformly close to the optimum in every bag of a branching tree, even under
uniform spectral conditioning. A
[regridding algorithm](regridded-certificates/note.md) recovers smaller
continuous certificates through aggregate error control. Its exact and
[certified inexact](regridded-certificates/inexact-oracles.md) oracle versions
have passed independent adversarial review. The
[synthesis](SYNTHESIS.md) compares their assumptions and costs with the grid
method. The reviewed [exact rational mixed-integer box-QP corollary](geometric-dp/exact-box-qp.md)
recovers both the optimizer and value, with polynomial bit complexity at
fixed width and polynomially bounded conditioning. An
[algebraic-output example](geometric-dp/algebraic-output.md) explains why
the same exact-output claim cannot extend to general quartics in expanded
algebraic-number formats.

The reviewed [coordinate-anchor theorem](new-direction/projection-anchors.md)
handles nonunique optimal sets, with work controlled by their coordinate
projections. The reviewed [affine repair theorem](new-direction/affine-repair-exploration.md)
handles coupling constraints when a suitable box-preserving repair is
available. It includes stable linear dynamics and
[private finite controls](new-direction/mixed-stable-audit.md). The reviewed
[nonlinear-dynamics theorem](new-direction/nonlinear-dynamics.md) uses convex
graph strips and adjoints. Its [polynomial-data bit extension](new-direction/nonlinear-dynamics-bit.md)
returns rational objective bounds and a feasible trajectory represented by
rational inputs and the original recurrence.

The [research record](PROGRESS.md) lists contributions, targeted commands,
source-comparison status, and ongoing work.

Work is recorded in separate directories. Independent agent review is not
journal peer review. Only targeted checks are run; no project-wide verification
or CI inspection is part of this continuation. Existing uncommitted work is
preserved.
