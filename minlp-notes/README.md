# MINLP theory notes (PSE-oriented)

Research notes on mixed-integer nonlinear optimization, guided by process systems
engineering. Mathematical review and novelty assessment are recorded separately.
“Independently reviewed” means checked by another research agent, not peer-reviewed
by a journal. An unsuccessful literature search does not establish novelty.

Code, protocols, compact results and verification instructions are tracked in
Git. Large raw traces, checkpoints and support-cut campaign records are preserved
separately, with checksums and restoration instructions in the
[evidence archive index](artifacts/README.md). Raw evidence remains available for
full replay; compact support-cut records allow table checks without downloading
the raw campaigns.

The [constructive separator-certificate manuscript](paper-separator-certificates/README.md)
gives a self-contained construction on arbitrary tree decompositions under
global quadratic growth, with certified inexact solves, exact rational
polynomial implementations, and a contracting nonlinear dynamics extension.
Its anonymous [PDF](paper-separator-certificates/main.pdf) and
[submission sources](paper-separator-certificates/submission-source.zip) are
available, with proof reviews, explicit complexity limits, and a qualified
literature comparison.

The [quadratic box-hull manuscript](paper-box-quadratic-hulls/README.md)
combines exact separating certificates, a compact family of three-variable
inequalities, an analytic edge-contact classification, and the sharp boundary
for finite semidefinite lifts. It also gives sparse graph obstructions and
small-component formulations. Its anonymous [PDF](paper-box-quadratic-hulls/main.pdf),
[submission sources](paper-box-quadratic-hulls/submission-source.zip), and
[computational companion](paper-box-quadratic-hulls/companion/README.md) are
available. Full family completeness and the all-positive path and star cases
remain explicit open questions.

The [hypermetric and binary quadratic separation manuscript](paper-binary-separation/README.md)
gives complete proofs of strong NP-completeness for unrestricted hypermetric
separation and related binary inequality families, including metric and strict
semidefinite promises, together with rank and threshold algorithms and the
gap-zero classification. Its anonymous [PDF](paper-binary-separation/main.pdf)
and [submission sources](paper-binary-separation/submission-source.zip) are
available, with independent proof reviews and a qualified literature audit.

The [arithmetic-complexity report](research-20261003-arithmetic/README.md)
develops topic 2 into one document covering values, optimizer points, exact
comparisons, and certificate representations. It adds global point oracles
on unbounded polyhedra, full residual-convex cubic recourse without joint
convexification, exact comparison in nonlinear dimension, structured box
and flow extensions, and compact circuit Grams. Proofs, independent reviews,
primary-source comparisons, and exact reference checkers are included. The
unrestricted polyhedral exact-comparison question remains explicitly open.

The [iterated and adaptive OBBT manuscript](paper-adaptive-obbt/README.md)
combines the September local-rate theory and October certificate developments
in an anonymous journal paper with complete proofs, corrected statements,
independent mathematical reviews, a literature audit, and an archived
reproducibility companion. Its [PDF](paper-adaptive-obbt/main.pdf) and
[submission sources](paper-adaptive-obbt/submission-source.zip) are available.

The earlier [adaptive OBBT study](research-20261003-adaptive-obbt/README.md) develops
finite certificates for remaining tightening benefit, an exact reference driver,
constrained and nonlinear extensions, and a local SCIP policy. Its prospective
120-run comparison found fewer auxiliary LPs but no additional solves or net
speed benefit; native SCIP remains the recommended default. The
[completion assessment](research-20261003-adaptive-obbt/CLOSEOUT.md) distinguishes
the developed results from open questions about cheap certificate discovery and
general allocation of solver effort.

The [joint-convexification study](research-20261003-convexification/README.md)
adds original-variable SCIP cuts, exact quadratic support over general small
rational polytopes, complete positive-tolerance separation for polynomial
graphs, and broader source-model preservation. Its integrated report includes
proofs, implementation contracts, independent reviews, and a new prospective
experiment. All three modes solved the same 25 of 30 new holdout models;
native SCIP remains the recommended default. A separate matched validation
records repairs for large-model discovery and budget enforcement.

The [earlier joint-convexification continuation](research-20261002-convexification/README.md)
retains the constrained-star support algorithm, the obstruction to composing
overlapping pair hulls, and its original unfavorable 316-run experiment. The
current report incorporates those mathematical foundations and keeps the two
experimental records distinct. Cut certificates do not certify a complete
numerical SCIP solve.

The [decomposition continuation](research-20261002-decomposition/README.md)
resumes topic 1 at the user's request. It brings the sparse global
optimization results into one technical report, adds a rational solver
with independently replayable certificates, and develops reviewed
extensions for recourse, coupled constraints, and nonunique optima.
Its result map distinguishes proved classes, implemented methods,
benchmark evidence, and the remaining general questions.

The earlier [October 2 continuation](research-20261002/README.md) was paused at the
user's request after finishing its current ideas and extensions. The
[closeout](research-20261002/CLOSEOUT.md) records the strongest completed
results, prior comparisons, verification, and unresolved limits.

The final reviewed [global-convex polynomial theorem](research-20261002/new-direction/globally-convex-polynomial-point-oracle.md)
gives deterministic `poly_D(I+q)` approximation of a fixed minimum-norm
optimizer on a bounded rational polytope, for fixed-degree rational
polynomials convex on all of Euclidean space. Its computable error
constant has polynomial bit length. A reviewed core-completion corollary
extends full-point output to nonconvex objectives with a supplied global
core quadratic convexifier under one finite core-noise law. The
[affine-power class](research-20261002/new-direction/affine-power-core-point-oracle.md)
provides an explicit verifiable higher-degree example. These are theoretical
output guarantees; publication priority and practical speedup remain unproved.

The continuation's
new [sparse polynomial theorem](research-20261002/new-direction/smoothed-sparse-polynomial.md)
gives reviewed expected exact optimization for fixed-degree polynomial
objectives on mixed boxes under one specified finite law of independent
linear perturbations. It permits arbitrary integer dimension and needs
no supplied growth bound. At fixed interaction width, expected work is
polynomial under the stated curvature/width/noise scales. Exact output
is usually a verified strongly convex subproblem with certified evaluation
to any requested precision; an exact algebraic fallback handles every
exceptional draw. The compact subproblem has polynomial size, while the
full global proof record has an expected-size bound. The result concerns
the sampled objective; priority and practical performance remain open.

A reviewed [graph-constraint corollary](research-20261002/new-direction/smoothed-polynomial-graph-constraints.md)
covers overlapping polynomial equalities with a sparse global parameterization
and independently perturbed free coordinates. A complementary
[state-count lower bound](research-20261002/new-direction/global-error-cell-barrier.md)
shows that the current pruning rule cannot give an FPT bound in width:
connected quartic instances force at least `(5n/(6p))^(p/2)` retained cells
on every draw. This is a limitation of that algorithm, not optimization
hardness; stronger conditional recourse remains a research target.
The reviewed [simplex extension](research-20261002/new-direction/simplex-block-smoothed-extension.md)
also permits disjoint resource or probability-simplex blocks coupled through
the polynomial objective, alongside native-integer intervals. Feasible
block rounding and face-based noise counts preserve expected exact implicit
optimization at fixed width; whole-block bags and block curvature bounds
are required.

A reviewed [conditional-recourse theorem](research-20261002/new-direction/smoothed-box-stable-recourse.md)
gives expected exact `f(k,L/sigma) poly(I)` optimization for unit-box QP
when fixing a supplied `k`-coordinate core leaves exact polynomial-time
recourse under further coordinate restrictions. Deletion to a forest is
a concrete case, even with a nonconvex residual problem. The new closure
test excludes distant residual solutions before solving a convex patch.
This uses a stronger structural parameter than treewidth alone.

The reviewed [nonlinear recourse theorem](research-20261002/new-direction/smoothed-polynomial-box-recourse.md)
extends this mechanism to certified approximate conditional values. Fixing
a small continuous core may leave an arbitrary dense convex polynomial
residual problem. Expected work is `f(k,L/sigma) poly_d(I)` under one
finite ambient-noise law, with exact implicit output on every draw.
Residual strong convexity is unnecessary. A checked degree-five family
has one core coordinate but requires unbounded rank for any fixed PSD
quadratic convexification. The [assessment](research-20261002/new-direction/polynomial-box-recourse-significance.md)
explains the structural gain, classical antecedents, and remaining solver
work. Convexity certificates and polynomial-time recourse on every
residual subbox are substantive premises.

A reviewed [native-integer recourse theorem](research-20261002/new-direction/smoothed-native-integer-recourse.md)
now gives ordinary exact algebraic output for a small continuous core
coupled to a fixed tractable integer feasible set. Convex-cost integer
flows and separable convex TU systems provide classical exact oracles.
Expected work is `f_d(k,L/sigma) poly(I)`; integer dimension, graph width,
and numerical capacities are outside the parameter factor. The core may
change costs, but not residual feasibility. A certificate excludes all
competing integer labels, then an exact small-core solve finishes.

A reviewed [flow extension](research-20261002/new-direction/smoothed-boundary-core-flow.md)
needs noise only on the continuous core, including when it is optimal
on a boundary face. Tightened arc intervals represent all tied optimal
flows, and derivative tests over that set certify the core face. Expected
work is fixed-parameter in the core size and curvature-to-noise ratio;
the sampling precision also has a parameter-dependent bound.
For [bilinear core–flow coupling](research-20261002/new-direction/smoothed-bilinear-core-flow.md),
the reviewed bound sharpens to
`[8^k(3+(1+k/2)L/(2sigma))^k+c_d^k] poly_d(I)` with polynomial
sampling precision. Here `L` comes only from the core objective.
The reviewed [TU extension](research-20261002/new-direction/smoothed-core-tu-recourse.md)
gives the same bounds for fixed totally unimodular equalities or
inequalities on bounded native integers. A compact dual certificate
replaces flow potentials; explicit bounded slacks handle inequalities.

The reviewed [core-only-noise theorem](research-20261002/new-direction/core-only-noise-boundary-recourse.md)
removes residual perturbations for continuous recourse with a verified
uniform strong-convexity modulus. Residual active faces may change and
their multipliers may vanish. Algebraic tube bounds and a curvature
argument justify exact convex closure without identifying those faces
in advance. Its count retains the original core curvature rather than
the potentially much larger curvature of a quadratic convexification.

A reviewed [regularization obstruction](research-20261002/new-direction/regularization-point-precision-obstruction.md)
explains why simply letting that residual modulus tend to zero is
insufficient. A convex quartic with bounded coefficients needs exponentially
many regularization-parameter bits in its dimension for constant point
accuracy. Its original optimization problem is easy by a structural
reduction; the result limits this extraction method, not convex optimization.

A stronger reviewed [point-output reduction](research-20261002/new-direction/convex-point-radical-comparison.md)
shows that constant-accuracy recovery of any optimizer of a convex
quartic can decide Square Root Sum, even at treewidth two. This is a
conditional arithmetic-complexity implication, not NP-hardness. It
clarifies why an efficient value oracle alone cannot justify an efficient
optimizer-coordinate oracle for general convex residuals.
The reviewed [arithmetic-circuit extension](research-20261002/new-direction/posslp-convex-point-extraction.md)
gives the corresponding implication for PosSLP using convex quartics
of unrestricted interaction width.

A reviewed [value-oracle theorem](research-20261002/new-direction/all-scale-core-value-oracle.md)
handles a supplied nonconvex core of any size with merely convex
residuals. One fixed finite core-noise draw supports every requested
objective accuracy `2^-q`, with expected work
`f_d(k)(1+L/sigma)^k poly_d(I+q)`. Each answer includes a feasible rational
point and a certified global value interval. A geometric count over all
refinement scales removes the earlier two-variable restriction. It gives
no residual optimizer-distance guarantee. The
[prior comparison](research-20261002/prior-art/all-scale-core-value-oracle-prior.md)
credits established convex-analysis and smoothed-optimization ingredients;
publication priority remains unresolved.

The reviewed [core-coordinate extension](research-20261002/new-direction/core-only-noise-core-oracle.md)
also approximates one fixed globally optimal core at the same expected
cost. A certified retained-region diameter controls core error; residual
coordinates carry only the objective-gap guarantee.

The reviewed [coupled-polytope extension](research-20261002/new-direction/coupled-polytope-core-value-oracle.md)
permits arbitrary bounded rational linear constraints when a supplied
core quadratic correction makes the objective convex. Its value and
selected-core guarantees retain expected
`f_d(k)(1+alpha/sigma)^k poly_d(I+q)` work. The correction `alpha` can
be much larger than the product-box theorem's original curvature `L`.
For quadratics, a reviewed [rational reconstruction corollary](research-20261002/new-direction/qp-core-cauchy-reconstruction.md)
turns these Cauchy guarantees into exact rational optimizer and value
output; the earlier aligned-QP theorem already provides a related
exact capability under its own parameterization.

Two reviewed point results sharpen this output distinction. For a
globally convex polynomial, the [selected-coordinate theorem](research-20261002/new-direction/joint-convex-core-point-oracle.md)
gives ordinary expected `poly_d(I+q)` work under one fixed finite law
of noise on the requested coordinates. Unperturbed coordinates have
no distance guarantee. For a rational polynomial of degree at most
three convex on a bounded rational box, the
[deterministic cubic theorem](research-20261002/new-direction/convex-cubic-point-oracle.md)
approximates its fixed minimum-norm optimizer in `poly(I+q)` bit time
without perturbation or strong convexity. Its reviewed
[polytope extension](research-20261002/new-direction/convex-cubic-polytope-point-oracle.md)
allows arbitrary bounded rational linear constraints. This gives a
positive degree-three counterpart to the quartic reductions above.
The [source comparison](research-20261002/prior-art/convex-cubic-point-oracle-prior.md)
distinguishes effective point bounds from classical value oracles;
no priority or practical-speedup claim is established.

The reviewed [cubic completion theorem](research-20261002/new-direction/cubic-core-full-point-oracle.md)
also returns a fixed full optimizer to any requested precision for a
possibly nonconvex cubic with a supplied core quadratic convexifier.
It preserves the coupled theorem's expected bound and perturbs only
the core. A convex surrogate and an effective regularization schedule
recover the unperturbed residual coordinates. The output remains a
Cauchy name, without exact active-set or expanded algebraic guarantees.

The reviewed [implicit-graph extension](research-20261002/new-direction/smoothed-implicit-graph-constraints.md)
handles locally coupled polynomial equalities with one globally bracketed
monotone dependent root over every retained mixed-box point. Certified
approximate DP avoids exact algebraic-value comparisons while preserving
exact feasible implicit output. A separate
[order-polytope theorem](research-20261002/new-direction/smoothed-sparse-order-polynomial.md)
covers continuous variables with overlapping order inequalities. It uses
feasible correlated rounding and LP certificates of active equalities.
Both give expected polynomial work at fixed interaction width under their
stated numerical and structural assumptions.
The reviewed [mixed order extension](research-20261002/new-direction/smoothed-mixed-order-polynomial.md)
also permits arbitrarily many binary variables, including implications
and continuous activation bounds. Binary-preserving transport supplies
the count, and binary labels are fixed before continuous face tests.
The input-size exponent depends on continuous coordinates per bag; the
result remains fixed-width polynomial, with a full Hessian bound.

The current constrained-MIQP result gives reviewed expected exact
`f(m,k,1+nu diam(P)/sigma) poly(I)` work under a specified independent
rational Gaussian-like coefficient law; see the
[complete theorem](research-20261002/new-direction/smoothed-gaussian-miqp.md).
Here `m` is integer dimension and `k` is negative inertia. Every sampled
draw is solved correctly. A separate
[sparse mixed theorem](research-20261002/new-direction/sparse-bag-cell-smoothed-miqp.md)
gives expected polynomial work at fixed treewidth with arbitrary integer
dimension and negative inertia. Both retain explicit numerical scale assumptions and concern the
sampled objective. Novelty and competitive solver performance remain open.

The reviewed deterministic
[filtered coordinate-grid algorithm](research-20261002/new-direction/pruned-coordinate-grid.md)
solves rational mixed-integer box quadratics exactly in
`f(p,kappa) poly(I)` bit operations, parameterized by bag size and upper
coordinate curvature relative to global quadratic growth. The polynomial
input exponent is absolute. Exact min-marginals filter coordinate domains,
removing the earlier occurrence parameter and accuracy-dependent exponent.
The growth constant need not be supplied; certificate validity is
independent of that assumption. Practical performance remains untested.
The reviewed [geometric copositivity certificate](research-20261002/new-direction/geometric-copositive-certificate.md)
also discovers and verifies a positive growth margin for sparse homogeneous
quadratics on the nonnegative orthant, in `f(p,L/g) poly(I)` work. Its
finite DP certificate needs no supplied margin or requested accuracy.
It applies to an explicit [connected family](research-20261002/new-direction/fan-preordering-growth-obstruction.md)
with treewidth two and bounded conditioning that admits no exact
unmultiplied box-preordering certificate at any degree. This separates
specific certificate families; it is not a general hardness claim.
The fan's failure of PSD-plus-nonnegative decomposition is classical;
the displayed rational construction checks its growth and certificate
consequences explicitly.
The reviewed [mixed-box shell certificate](research-20261002/new-direction/mixed-shell-certificate.md)
extends direct verification to any proposed rational mixed-box QP solution.
It certifies both unique global optimality and a physical Euclidean growth
margin, without receiving a growth bound. Discovery and verification cost
`f(p,max(1,L/g)) poly(I)`; the returned margin preserves this conditioning
up to a constant. This verifies a candidate rather than finding one.
Its reviewed [coordinate-fiber extension](research-20261002/new-direction/geometric-product-face-certificate.md)
can certify an entire supplied optimal set of the form `{v} x Y`, including
mixed free coordinates, without enumerating their assignments. General
unknown optimal sets remain outside this certificate.
The reviewed [polynomial extension](research-20261002/new-direction/nonlinear-shell-certificate.md)
certifies supplied rational candidates for mixed-box objectives given by
explicit bounded-degree polynomial factors. It combines outer shell bounds
with a checked local Taylor remainder. Its conditioned FPT guarantee needs
positive quadratic growth and a verified coordinate-curvature bound;
uniqueness alone is insufficient for polynomial objectives.
The same reviewed [polynomial grid algorithm](research-20261002/new-direction/polynomial-pruned-grid-extension.md)
also finds a candidate: it gives certified mixed-box approximation with
logarithmic precision cost, and exact optimization when all variables are
native integers. A further [convex-patch theorem](research-20261002/new-direction/implicit-convex-patch-certificate.md)
represents an unknown continuous optimum by a verified strongly convex
subproblem, with certified arbitrary-precision evaluation. That exact
implicit output additionally requires a comparable positive lower bound
on the continuous Hessian at the optimum, automatic for interior optima
but substantive at boundary optima. The construction and output size are
`f_d(p,kappa) poly(I)`; expanded algebraic coordinates are not promised.
A complementary [negative-inertia theorem](research-20261002/new-direction/negative-inertia-qp.md)
gives exact QP over any bounded rational polytope, parameterized by the
number of negative Hessian eigenvalues and the magnitude of the most
negative eigenvalue relative to growth. It uses exact convex recourse and has no
sparsity requirement. Its [mixed-polytope extension](research-20261002/new-direction/negative-inertia-miqp.md)
adds integer dimension as a parameter. A separate
[proximal-grid extension](research-20261002/new-direction/proximal-exact-recovery.md)
handles arbitrary optimal sets on mixed boxes, with the important restriction
that a valid growth bound must be supplied. A reviewed
[linear-perturbation theorem](research-20261002/new-direction/smoothed-linear-growth.md)
provides quantitative growth with high probability, including a rational
sampling scheme. Its algorithmic consequences concern perturbed inputs
and high-probability work, not expected runtime.
The sharper [proximal-tail theorem](research-20261002/new-direction/proximal-growth-tail.md)
now supports a reviewed [expected exact-work result](research-20261002/new-direction/expected-smoothed-qp.md):
with at most two negative Hessian eigenvalues, a specified polynomial-bit
linear perturbation law gives expected work
`poly(I) (1 + nu sum_i w_i / sigma)`. An exact fallback handles every
draw, including ties; the input is never resampled. This solves the
perturbed objective and requires numerical control of the displayed ratio.
Under noise in the negative-factor coordinates, the reviewed
[exact cell-closure theorem](research-20261002/new-direction/smoothed-exact-cell-closure.md)
extends expected exact work to arbitrary negative inertia, without a growth
assumption. It uses one fixed rational sampling law and recognizes quadratic
regions of the convex recourse value function. That noise is generally
correlated in original coordinates, so the two perturbation models remain
distinct.
The reviewed [ambient-noise extension](research-20261002/new-direction/smoothed-ambient-cell-closure.md)
now covers independent perturbations in every original linear coefficient
for any fixed negative inertia. It returns an exact solution on every draw
and has expected polynomial bit work under the stated numerical bounds.
Its dimension dependence is `n^{O(k)}`, so it does not provide the aligned
model's fixed-parameter bound. Classical parametric-QP reductions and
critical-region methods are credited; the proposed advance is the expected
exact-work analysis under the specified finite noise laws.
The reviewed [Gaussian-like noise theorem](research-20261002/new-direction/smoothed-gaussian-cell-closure.md)
now gives expected `f(k,nu diam(X)/sigma) poly(I)` exact work with
independent original coefficients. Its explicitly sampled finite rational
law approximates a Gaussian; it is not a real-Gaussian input model.
A weighted cell count removes the dimension powers in the uniform-noise
bound. The reviewed [constrained MIQP extension](research-20261002/new-direction/smoothed-miqp-cell-closure.md)
handles general bounded mixed polytopes under uniform rational noise,
using integer dimension as an additional parameter. A best-competing-label
gap certifies that one continuous formula remains valid across a cell.
Its reviewed [Gaussian-like composition](research-20261002/new-direction/smoothed-gaussian-miqp.md)
gives expected exact `f(m,k,1+nu diam(P)/sigma) poly(I)` work on general
bounded mixed polytopes, with an absolute input exponent. The specified
finite independent noise law is fixed before sampling, and every draw is
solved correctly.
For [separable mixed recourse](research-20261002/new-direction/smoothed-mixed-separable-closure.md),
convex piecewise-quadratic costs on product boxes permit arbitrarily many
integer coordinates; neighboring scalar choices give that certificate
directly. Rational coefficients and rational piece breakpoints are required.
Its reviewed [anisotropic Gaussian extension](research-20261002/new-direction/anisotropic-gaussian-separable-closure.md)
gives expected exact `f(k,1+beta diam(X)/sigma) poly(I)` work without
a numerical conditioning assumption on the supplied full-row-rank factor.
Here `beta` measures that supplied concave term; it is not the negative
curvature of the complete objective. Arbitrary integer dimension remains
allowed, and correctness holds for every draw of the specified finite law.
The reviewed [sparse smoothed-QP theorem](research-20261002/new-direction/sparse-bag-cell-smoothed-qp.md)
instead allows arbitrary negative inertia on continuous boxes. Sparse bag
tables, optimizer-preserving pruning, and exact convex-face closure give
expected polynomial work at fixed treewidth under specified independent
rational noise and numerical scale bounds. Its input exponent depends on
width; it does not require growth or variable-occurrence bounds.
Its reviewed [mixed extension](research-20261002/new-direction/sparse-bag-cell-smoothed-miqp.md)
adds unrestricted integer dimension. At unit resolution, integer cells
become singleton values; closure first fixes every integer coordinate,
then certifies the remaining continuous face. Integer widths remain in
the numerical runtime bound.
A reviewed [nonlinear integer theorem](research-20261002/new-direction/smoothed-integer-low-rank.md)
gives expected exact optimization for separable convex quartics with low-rank
concave coupling on integer boxes under a fixed rational factor-noise law.
It permits arbitrarily many integer variables and large encoded ranges,
with explicit numerical range/noise dependence, and needs neither a growth
bound nor a fallback. Simpler binary and explicit-label baselines are credited.
A complementary [feedback vertex set theorem](research-20261002/new-direction/fan-exploration.md)
removes occurrence dependence when fixing a small coordinate set leaves a
forest. It requires growth only in those coordinates and permits nonunique
recourse. It uses the existing exact forest-QP algorithm.
The independently reviewed [geometric-grid algorithm](research-20261002/geometric-dp/theorem.md)
gives certified global optimization on sparse mixed-integer boxes with
polylogarithmic accuracy dependence, under explicit upper-curvature and
global quadratic-growth assumptions. It permits branching decompositions
and boundary minima, compresses large integer domains, and eventually gives
exact integer certificates. [Extensions](research-20261002/geometric-dp/extensions.md)
cover certified approximate tables, polynomial-factor bit complexity,
private recourse, and fully enumerated discrete states. A separate
[finite-certificate counterexample](research-20261002/tree-localization/counterexample.md)
disproves unrestricted per-bag localization on uniformly conditioned
branching trees. The reviewed
[continuous regridding algorithm](research-20261002/regridded-certificates/note.md)
recovers smaller certificates by controlling aggregate error, with
[certified inexact oracles](research-20261002/regridded-certificates/inexact-oracles.md).
Reviewed extensions cover nonunique optimal sets through coordinate
projections and [stable nonlinear dynamics](research-20261002/new-direction/nonlinear-dynamics.md)
through convex graph strips, feasible repair, and adjoint slopes. A
[bit-complexity extension](research-20261002/new-direction/nonlinear-dynamics-bit.md)
uses rational local LPs and compressed feasible trajectories.
Novelty and solver performance remain unestablished; the
[research record](research-20261002/PROGRESS.md) distinguishes proofs,
targeted checks, and pending work.

The [September 29 continuation](research-20260929/README.md) studies how
problem structure changes the cost of global optimization; its
[synthesis](research-20260929/SYNTHESIS.md) separates proved results from
evidence. Single-tree spatial branch-and-bound with termwise relaxations
needs exponentially many leaves on path-structured problems even at a unique
nondegenerate minimizer (at least `0.57 (5/3)^n` with termwise McCormick),
while decomposition-aware certificates with Lagrangian slopes need
`O(|T| C^{w+1} log(|T|/eps))` work under quadratic growth, so treewidth
replaces dimension (on path decompositions with a zero-gradient, for
example interior, minimizer, an algorithm that does not know the minimizer
finds certificates of the same size form); the
separation is a statement about fixed termwise
relaxations, and a function-class view of separator consistency (for one
separator, an exact identity: the gap is twice the distance to the band of
exact splits) explains when affine splits suffice. SCIP 10's node counts
grow about fivefold per two added variables on such chains, while a chain
dynamic-programming prototype handles 8192 variables. Instance-specific
certificates, each independently verified (one partly by sampling), closed 31 MINLPLib instances
listed as open for the models as written (including camshape, chain,
catmix, dtoc5, lnts, optcdeg2, powerflow0030p/0039p/0039r, pindyck,
hvycrash, etamac, pricing050, two Gibbs-energy problems and the three eg_*
Gaussian-surrogate problems; 13 of them
against primal points that are feasible only to row violations of 1e-20 to
8e-12), certified the intended relaxation of six KAN instances whose models
are exactly infeasible, raised the waterno2 dual bounds by factors of
1.6–6.2 (waterno2_06 then to within 1.67% by branching on its level
separators with cell-dependent slopes), and brought ann_cumene_tanh to within 0.194% of its best known
point. A validity audit of all MINLPLib listed bounds proved 19 solver
dual bounds on 15 instances invalid (8 of them at tolerance scale), and
SCIP 10.0.2 returned wrong optimal values on waterno2 subproblems. A theory
of discrete calibrations describes the certificates of the transcribed
control instances and gives a window law at bang-bang switches; whether a
short window around a switch suffices is decided by the sign of one
data-determined curvature, and singular arcs are treated as well. The
[closing record](research-20260929/closing-research-results.md) collects
results and limits. A secondary line characterizes node counts through real
log canonical thresholds. The mechanisms of the certificates are classical;
novelty claims are qualified in each note.

The [second September 28 continuation](research-20260928b/README.md) is
complete at the user's requested scope; its
[closing record](research-20260928b/closing-research-results.md) collects
the results and limits. Its main line is a complexity theory of
branch-and-bound with nonlinear relaxations: rigorous node-count lower
bounds for adaptive spatial trees, with the `eps`-exponent equal to half
the dimension of the optimal set; separate theories for McCormick-type
relaxations and objective-cutoff propagation; a Lean-verified
4-competitive branching rule in one dimension and exponential lower
bounds for node-local rules in higher dimension; sharp thresholds for
linear-size B&B in random sparse regression, unchanged by stronger
lifted relaxations; superpolynomial certification cost for box-relaxation
B&B in binary least squares at logarithmic SNR; and class-number bounds
for integer branching. SCIP 10 node counts follow the predicted
exponents, while MINLPLib studies show that the branching-point theory
does not change practical performance. The continuation also found that
a published exactness theorem for the Boolean relaxation of sparse
regression (Pilanci–Wainwright–El Ghaoui 2015) is false as stated, and
proved split-inequality separation for integer QP strongly NP-complete.
The [synthesis](research-20260928b/bb-complexity/SYNTHESIS.md) separates
proved results, empirical evidence, and open questions.

The [September 28 continuation](research-20260928/README.md) is complete
at the user's requested scope. Its
[closing record](research-20260928/closing-research-results.md) collects
the results, verification, and limitations; no new directions are underway.
Its leading candidates give an unconditional `O(log^3(r)/r^2)` error bound
for sparse ordinary box quadratic modules and sharp rate boundaries for
convex private recourse. The ordinary-module bound per total coefficient
norm is uniform in the number of bags. The companion full-preordering rate
is inverse-square, with a matching fixed quadratic example; July 2025 and
February 2026 author presentations already state that rate, so its
originality is not claimed here. Affine recourse can instead force a sharp
inverse-order gap, even with private linear programs. Reviewed extensions
cover finite-state variables, large private convex blocks, and rational
certificates with quantitative slack. Regular projected recourse multipliers
restore inverse-square convergence; global geometric repair also gives
quantitative bounds with polynomial constraints. These are results about
specified hierarchies, not general MINLP runtime bounds. Other completed work concerns
graph-constrained switching, exact arithmetic, and the limitations of local
certificates. Publication priority remains unestablished.

The [September 27 continuation](research-20260927/README.md) has finished
its current directions at the user's request. The
[closing record](research-20260927/closing-research-results.md) collects
the final reviewed results, corrections, and remaining limits. No new
directions are underway. Its structural results concern exact
quadratic and second-order cone optimization when the constraint Hessians
have a small matrix span, including unbounded mixed-integer models and
algebraic output. A stronger common-range restriction gives fixed-parameter
algorithms, and a general convex semialgebraic theorem bounds finite
mixed-integer values even without attainment. Related results identify
sharp rationality and output-size boundaries. The continuation index
separates proposed contributions from established prior
work and modest supporting findings.
New independently reviewed
[lower](research-20260927/unconstrained-quartic-posslp-reduction.md) and
[upper](research-20260927/strong-convex-quartic-posslp-upper.md) bounds
show that exact unconstrained minimum and minimizer-coordinate order
comparisons are PosSLP-complete for rational quartics with a supplied
positive definite rational Hessian Gram. Real SOS membership and global
nonnegativity are also complete; rational SOS membership has the lower
bound, with its zero-minimum case requiring separate treatment.
The [synthesis](research-20260927/exact-convex-quartic-complexity.md)
states the certificate and output distinctions. This classifies exact
arithmetic, without claiming NP-hardness or a numerical-approximation
lower bound. Primary audits credit established exact SDP/SOCP hardness
and earlier Newton-circuit PosSLP reductions. Priority is unestablished.
A [reviewed strengthening](research-20260927/rational-optimizer-posslp-coordinate-comparison.md)
keeps coordinate comparison PosSLP-complete even when the bounded unique
optimizer is rational, the minimum is known to be zero, and short
rational square factors are supplied. Its quaternion compiler and
quartic realization have separate fresh proof reviews. This is an
exact-arithmetic classification, not a numerical approximation lower bound.
A reviewed [algorithmic consequence](research-20260927/mixed-quartic-integer-constraint-rank-oracle.md)
solves globally strongly convex quartic MINLP over arbitrary mixed
linear constraints in expected fixed-parameter time, with a PosSLP
oracle, parameterized by the number of integer variables plus the rank
of the continuous constraint matrix. Its
[integer candidate search](research-20260927/mixed-linear-strong-quartic-candidate-list.md)
uses ordinary rational computation; exact continuous selection uses
the oracle. The continuous dimension is unrestricted, and the returned
continuous optimizer is represented implicitly.
A separate reviewed [rational-witness lower bound](research-20260927/strict-convex-quartic-rational-witness-lower-bound.md)
gives a compact, strictly feasible sublevel set of one such quartic in
\(n\) variables, with bounded coordinates, where every rational feasible
point needs \(\Omega(n2^{n/2})\) denominator bits. The input has
polynomial size. This is an unconditional obstruction to expanded
rational output; it does not exclude short certificates in other formats.
A reviewed [rational-optimizer family](research-20260927/rational-convex-quartic-minimizer-height.md)
has a unique rational minimizer in a fixed coordinate box, yet its
denominators have exponentially many bits in the dimension. The
quartic, its rational square factors, and its strict Hessian certificate
all have polynomial size. Its [optimal moment and maximal-rank Gram certificates](research-20260927/rational-circle-optimal-gram-height.md)
also require long expanded rational entries, while a short lower-rank
Gram remains available. The literature comparison separates this
restricted construction from established large-output SDP examples.
One new [strongly convex integer quartic](research-20260927/convex-quartic-irrational-zero.md)
has minimum zero at a unique irrational point, resolving negatively the
rational-witness possibility marked unknown in the inspected November
2025 arXiv version of a paper. Global convexity and the irrational
singleton are now verified in Lean as well as independently reviewed.
A general construction realizes exactly the algebraic numbers with one
real conjugate and provides a short rational convexity certificate.
Priority remains unestablished. This example alone is a witness
obstruction; the separate reduction above addresses exact decision.
A subsequent [integer quartic family](research-20260927/cyclic-quartic-exponential-degree.md)
has short coefficients but an exponentially large zero field, with
reviewed rational convexity certificates. It separates exact algebraic
output size from local numerical conditioning and identifies sharp
degree bounds in the first few dimensions.
Another reviewed [small integer quartic](research-20260927/ternary-rational-sos-convex-counterexample.md)
has a strict rational convexity certificate and minimum zero, while
every polynomial SOS certificate must use a real coefficient field
containing \(2^{1/5}\). It separates rational convexity certification
from exact rational SOS certification, in the smallest dimension
under its stated Gram assumption.
A reviewed [quintic-tower construction](research-20260927/exponential-least-sos-field.md)
strengthens this to exponential degree: in \(3k\) variables, every
algebraic polynomial SOS or Gram certificate has a coefficient of
degree at least \(5^k\), while the input and its rational Hessian
certificate have polynomial size. The exact least coefficient field
is \(\mathbb Q(2^{1/5^k})\). This bounds explicit algebraic certificate
output. A [constructive companion](research-20260927/tower-sos-coefficient-encoding.md)
gives polynomial-size shared root circuits for those same certificates.
After increasing a rational scale, the family also has
[short rational-function certificates](research-20260927/rational-tower-quadratic-denominator.md)
with an everywhere-positive common denominator of minimum degree two.
A reviewed [denominator comparison](research-20260927/rational-radial-exponent-obstruction.md)
shows that fixed radial multipliers can need arbitrarily high
rational SOS order in this strict convexity class, while adapted
quadratic denominators retain short certificates. A
[quantitative refinement](research-20260927/rational-radial-height-lower-bound.md)
forces order at least \(\Omega(\log L/\log\log L)\) for binary input
length \(L\), while the adapted certificate has size \(O(L)\).

The [September 25 research batch](research-20260925/README.md) has completed
[publication preparation](research-20260925/publication-readiness.md), and
was then paused at the user's request. Its reviewed results include an
exact three-variable counterexample and a compact SDP for a family of missing
quadratic cuts; penalty encoding lower bounds, a fixed-quadratic-count upper
bound, and calibration inapproximability; and a quantitative accuracy
obstruction for a specified subset moment relaxation on uniformly conditioned
stars. The penalty encoding construction and its dual formulas have targeted
Lean coverage. The handoff includes scoped contribution assessments, fresh
adversarial reviews, versioned sources, and a reproduction guide. The notes
distinguish proved results from possible applications, classical consequences,
unresolved questions, and qualified novelty claims. Papers have not been written.

The September 21 continuation adds two solver-oriented results with code,
experiments, independent reviews and their negative findings.
[Envelopes of composite univariate subexpressions](results/composite-univariate-envelopes.md):
Gurobi, SCIP and BARON relax multi-term univariate expressions term by term
and fail on 20-variable separable quartic programs; a SCIP handler with
certified curvature and cuts valid for every slope solves all 48 test
instances in seconds and tightens the root relaxation on 35 of 81 comparable
MINLPLib instances, but as a Python plugin it solves 51 of 107 within 120 s
against 54 for native SCIP
([experiment record](notes/composite-univariate-envelopes-experiments.md)).
[Vertex binarization](results/separable-vertex-binarization.md) turns the
classical vertex property of separable concave structure into a cardinality
constraint on status binaries. It is provably solved in `2n+1`
branch-and-cut nodes on the repository's exponential lower-bound family,
where Gurobi and SCIP time out from `n = 24` on the original asymmetric
model; it is slower on random instances and is a targeted device only
([experiment record](notes/separable-vertex-binarization-experiments.md)).
Both records list solver errors observed in Gurobi and BARON.

The September 21 joint-convexification continuation studies
[row hulls](results/row-hull-separable-concave.md): the joint convex hull of
all separable concave terms on one linear row, used as root cuts for multi-row
models. For equal widths the hull is one min-sum inequality with a compact
extended form; a source check showed that it is the constant-capacity flow
cover polyhedron of Padberg, Van Roy and Wolsey in other variables, so the
contribution is the identification with arbitrary concave terms, inequality
rows, indicators with concave costs, a valid interval dynamic program for
general rows, and the computation. As static root cuts for unmodified solvers
the cuts raise solved instances within 300 s from 96 to 124 of 130 (Gurobi 13),
18 to 41 of 44 (SCIP 10) and 15 to 44 of 50 (BARON) on synthetic concave-cost
transportation and network-flow families; most of the gain comes from
equal-width families built to fit the closed form (with unequal widths Gurobi
goes from 72 to 77 of 80). They make easy instances slower; separating them on node boxes inside SCIP
was measured and does not pay (4.4–6.3 times slower than root-only). They are only
modestly stronger than the exhaustive closure of published tilted flow covers,
and apply structurally to 4.8% of MINLPLib
An independent code review found invalid cuts caused by a
pricing bug on two-decimal data; it was fixed and all affected runs repeated
([experiment record](notes/row-hull-experiments.md),
[theory review](notes/review-row-hull-theory.md),
[code review](notes/review-row-hull-code-experiments.md),
[MINLPLib scan](notes/row-hull-minlplib-scan.md)).

A second, exploratory line of the same continuation treats terms that share a
variable instead of a row:
[linking the auxiliary variables of univariate terms](results/shared-variable-term-links.md)
(`sin`/`cos` of one angle, several powers of one nonnegative variable) by exact
redundant relations. The hull theory is known (Ballerstein 2013); the automatic,
solver-independent reformulation is neutral or harmful on most of the 48
MINLPLib instances it applies to, but on the open water-network instances
`waterno2_06/09/12/18` it raises Gurobi's 30-minute dual bounds above the best
values listed by MINLPLib (uncertified single runs; BARON shows the same
direction on three of the four instances but not the values, and on
`waterno2_06` its bound falls from 73.7 to 72.8) and yields a `waterno2_18`
point with objective 5178.16 against the listed 5269.64, with all residuals bounded exactly in
rational arithmetic by `5.8e-11`. Replacing the link by the classical exact
hull of `(x, x^2, x^3)` (two cone constraints) raises those 30-minute bounds
further, by 21% to 130%, and also lifts `ghg_2veh` and `ex8_4_2` above their
listed best dual bounds. The record also documents a
SCIP 10 wrong optimum on `waterno2_02` and `waterno2_03`; an independent review
confirmed the bounds and validity and corrected two errors in the note. A
[pilot with bilinear items on a row](notes/row-hull-bilinear-items-pilot.md) was
negative.

The [certified-MINLP repair and replay record](notes/certified-minlp-repair-and-replay.md)
tracks the September 13 correction of the certificate pipeline: one exact
expression interpretation, rigorous nonlinear cuts, independent rational VIPR
proof replay, and separate complete/partial verdicts. It supersedes the earlier
269/289 acceptance claim and records the historical 188/92/9 replay and its
limitations. The [certified-MINLP paper](paper-certified-minlp/README.md)
reports the later primary uniform campaign on the same 289 models: 203
verified, 19 rejected, and 67 missing artifacts.
A [small complete example](code/minlp_solver_lab/certify/examples/quadratic/README.md)
can be replayed without a numerical solver. The
[solver discrepancy audit](notes/certified-minlp-solver-discrepancies.md)
checks actual invalid returned points and establishes the exact `clay0204m`
optimum with matching lower and feasible upper certificates.

The [convex GDP development record](notes/lbesh-development-log.md) tracks
the September 19 correction and development of logic-based extended
supporting hyperplanes. It identifies the cuts as established perspective OA,
records fresh theory and implementation reviews, and reports a completed
comparison of radial and point separation. Independent reviews accept
[publication readiness](notes/lbesh-publication-readiness.md) for a focused
computational study with modest impact and qualified claims. See the
[claim register](notes/lbesh-claim-evidence.md) and
[reproduction instructions](code/minlp_solver_lab/LBESH_RESEARCH.md).

The [September 12 evening closeout](notes/research-20260912b-closeout.md)
preserves the historical GDP and certified-MINLP results, superseded by their
respective development records. Its separate observation that MINLPLib's
`heatexch_gen1/2/3` share an unbounded guarded LMTD expression retains its own
scope: for `heatexch_gen1` numerical estimates indicate an ill-posed model, and
for `heatexch_gen2/3` only the structure was checked.

The [September 12 closeout](notes/research-20260912-closeout.md) collects the
current continuation's results, independent reviews, software, source-access
limits and corrected claims. Its strongest theoretical candidate is a relative
PSD approximation set over feasible paths and rationally represented matroid
bases. Its implemented methods provide exact global certificates for correlated
measurement selection, including robust kinetic designs and a latent-separator
relaxation. A fixed-physical-grid comparison also records where calendar memory
becomes too expensive. The [contribution map](notes/research-20260912-contribution-map.md)
distinguishes verified mathematical scope, practical evidence and unresolved
publication priority. The [research log](notes/research-20260912-log.md)
preserves the investigation and negative results.

The [Lean topic index](formal/topics/README.md) maps formal coverage by topic.
The [recommended-topic verification sequence](formal/RECOMMENDED-TOPICS-PLAN.md)
tracks the September 17 campaign, beginning with sharp marginal-floor gaps.
[Certified MINLP](formal/topics/14-certified-minlp/README.md) is also complete;
[many-leaf reciprocal hulls](formal/topics/13-many-leaf-reciprocal/README.md)
are now complete too.
[Flat-chain network–simplex thresholds](formal/topics/15-flat-chain-threshold/README.md)
are complete and independently reviewed.
[Deterministic potential-flow certificates](formal/topics/16-potential-flow-certificates/README.md)
are complete and independently reviewed as well: they verify the remaining
certified-computation mathematics of Paper A's appendix, including separate-edge
Bregman intervals, posterior scenario recovery, complete support certificates for
linear goals, sharp conservation-aware curvature bounds, and the exact two-path
comparison.
[Arbitrary-grid one-switch minimax and sharp grid transfer](formal/topics/17-grid-switching/README.md)
is complete and independently reviewed as well. It builds a general
switching-control model — arbitrary mode count, arbitrary grid, arbitrary
horizon — and verifies the exact one-switch minimax value on every grid, the
sharp grid-transfer theorem and its certified coarsening, and the supporting
instance algorithms. Its rounding step is proved from Hall's marriage theorem,
since the network-flow route the sources use has no counterpart in the pinned
Mathlib.
[Positive-box multilinear gaps](formal/topics/18-positive-box/README.md)
are also complete: the package proves the aspect-ratio bounds
`max{2, rho} <= C_box(rho) <= rho + 2` for `rho > 1`, the finite-dimensional refinement,
and transfer to original boxes, including fixed coordinates.
[Structural multilinear gaps](formal/topics/19-structural-multilinear/README.md)
are complete: feedback, frequency-two and incidence-treewidth-two bounds,
including sharpness and the stated box extensions. The [scalar quadratic precision proofs](formal/topics/20-scalar-quadratic/README.md)
are also complete, including the sharp square law, rank and inertia laws, and
explicit finite linear constructions. The [DAG spectral approximation-set
proofs](formal/topics/21-dag-spectral/README.md) are complete, including the
original-input path construction, singular ranges, size and bit-work bounds,
and criterion consequences. The [represented-matroid spectral package](formal/topics/22-represented-matroid-spectral/README.md)
is complete as well: all 37 claims, the original-input base producer, exact
singular ranges, polynomial size and bit-work bounds, criterion selectors,
and uniform, partition, and graphic representations. Its 65 modules passed
independent review, the axiom audit, and individual kernel replays.
Topics 00–22 are complete within their listed scopes; topics 23–26 remain queued. The separately prioritized
[quadratic aggregation package](formal/topics/27-quadratic-aggregation/README.md)
is also complete: the main certificate equivalence, its HHC specialization,
and all three supporting lemmas are proved in 11 Lean modules, with
independent reviews, a 178-declaration axiom audit, and module kernel replays.
Its [consequences extension](formal/topics/28-quadratic-aggregation-consequences/README.md)
also verifies the closed-system and Shor equivalences, exact finite SDP
characterization, and two boundary examples in 10 new modules.
The [infinite-aggregation package](formal/topics/29-infinite-aggregation/README.md)
verifies actual HHC, exact good multipliers, indispensable strict rays and
the finite closed-hull obstruction in 18 further modules. Both extensions
have completed independent reviews and targeted machine checks.
The [documentation follow-up](notes/lean-verification-documentation-followup.md)
records the resulting source corrections, independent reviews and rebuilt papers.
Local work uses targeted checks.
CI handles project-wide verification; do not run it locally or check CI.
The [sequential paper-verification record](formal/COMPLETION-PLAN.md) tracks
completion of the standalone multilinear paper before the focused cubic-gap
paper. Each topic has its own source map, review, and verification evidence.
Start with the [multilinear paper](paper-multilinear-gap/README.md) or
the [cubic paper](paper-cubic-gap/README.md) for a self-contained distribution.

The [Lean verification project](formal/README.md) formally proves the exact
integer-versus-binary counts for the fixed-degree convex box family, including
rational linear realizations. Its [coverage record](formal/COVERAGE.md) and
[verification report](formal/VERIFICATION.md) identify the checked claims and
reproducible build, axiom-audit, and kernel-replay commands.

The 2026-09-07 network–simplex continuation develops observation-sensitive
compressed hulls, complete exact separators, sharp rank-three coefficient bounds,
and exponential coefficient growth on sparse series–parallel networks. A
fixed-state flat-chain theorem gives a complementary positive result. The
[paper-readiness record](notes/network-simplex-paper-readiness.md) collects the
proofs, independent reviews, implementation evidence, measured limitations, and
remaining boundaries.

The switching-control continuation completed on 2026-09-07 has a
[paper-readiness record](notes/cia-reopened-paper-readiness.md): exact minimax
values on arbitrary one-switch grids, exact algorithms for small switch budgets
with minimum dwell times, sharp grid transfer, stronger general bounds, and a
verified correction to a published lower bound. Proofs, implementations,
independent reviews, source comparisons, and unresolved questions are linked there.

The later [bilevel continuation](notes/bilevel-reopened-closeout.md) develops
exact robustness to near-optimal follower choices, certified dense-quadratic
screening, nonlinear aggregate approximation, and response-dependent upper
constraints. It also adds exact scalar tariff algorithms and records independent
reviews, computational evidence, and qualified literature comparisons.
The [nonconvex follow-up](notes/bilevel-nonconvex-closeout.md) adds an exact
global-response implementation with nonconvex aggregate costs, repeated
benchmarks, and an audited classical-literature comparison. It distinguishes
large populations with few response types from costly heterogeneous cases.

The potential-flow continuation requested on 2026-09-06 is complete. Its
[paper-readiness record](notes/potential-flow-paper-readiness.md) collects the
new results, independent reviews, 19 passing validation commands, implemented
solvers and certificates, and remaining boundaries. The
[continuation log](notes/potential-flow-reopened-status.md) records its scope.
The earlier continued research program was closed on 2026-09-05. Its
[current closeout and verification record](notes/research-continuation-closeout.md)
identifies the completed results, corrections, review evidence, and questions
retained as unresolved. The
[earlier closeout](notes/research-closeout.md), [research log](notes/log.md), and
[historical continuation status](notes/reopened-run-status.md) preserve the
preceding work; the current closeout supersedes their running-task labels.

## Results and current investigations

The September 22 continuation develops these theoretical results:

- [Four aggregations for strict three-quadratic PDLC hulls](results/four-aggregation-strict-pdlc.md)
  removes the regularity and infinity assumptions from the published
  four-aggregation bound by inward compactification and a strict limiting
  argument. It covers every positive dimension, including dependent triples;
  the existing four-necessary example proves sharpness in dimensions at
  least three. The closed hull of the strict set has four oriented SOC
  constraints. Independent reviews and a primary-source priority audit are
  recorded; no efficient multiplier algorithm is established.
- [Infinite quadratic aggregation under hidden hyperplane convexity](results/infinite-quadratic-aggregation-hhc.md)
  gives an explicit four-variable, three-constraint example answering
  Conjecture 3.1 in the inspected Blekherman–Dey–Sun preprint. Its ordinary
  hull requires uncountably many good aggregation rays, and even its closed
  hull has no finite good aggregation description. A small SDP lift remains
  possible. Independent proof and novelty reviews distinguish this obstruction
  from established SDP exactness and earlier infinite-aggregation examples.
  [Lean verification](formal/topics/29-infinite-aggregation/README.md)
  now covers HHC, spectral goodness, strict-ray uncountability, and the finite
  closed-hull obstruction; the hull formula, SDP lift, and stronger arbitrary
  quadratic obstruction remain outside that formal scope.
- [Indicator quadratic hardness at bandwidth two](results/indicator-quadratic-treewidth-two-hardness.md)
  proves exact NP-completeness for Hessians arbitrarily close to identity
  on a chain of triangles. One construction has an input-independent Hessian
  and a constant absolute gap with large coefficients; another has unit
  penalties and bounded linear coefficients but a potentially exponentially
  small gap. The results complement tree algorithms and do not contradict
  existing approximation guarantees. Independent review and 3,072 exact
  support-QP checks are recorded. A
  [reviewed fixed-data message construction](notes/research-20260922-constant-data-messages.md)
  gives exponentially many indispensable exact quadratic formulas and a
  matching, horizon-independent support-pruning accuracy law. Its
  unconditioned objective is easy; it is a representation lower bound.
- [Exact smoothed indicator messages under spectral bounds](results/smoothed-spectral-indicator-messages.md)
  constructs complete bounded-parameter message dictionaries and an exact
  optimizer in polynomial expected bit time for fixed-treewidth positive
  definite indicator QPs with polynomial numerical bounds. Independent
  penalty perturbations use only logarithmically many random bits per
  coordinate. Two independent proof reviews and exact adversarial checks
  support the construction; novelty remains provisional. The algorithm
  enumerates nearly optimal supports through additive approximation oracles.
  It requires neither diagonal dominance nor bounded biconnected blocks.
  Earlier [scalar](results/smoothed-indicator-block-dp.md) and
  [direct treewidth](results/smoothed-fixed-treewidth-indicator-dp.md)
  constructions remain documented, along with a
  [planar region bound](notes/research-20260922-higher-dimensional-smoothing.md)
  and [all fixed support-count moments](notes/research-20260922-envelope-higher-moments.md).
  No practical speedup is claimed; additive approximation alone is already
  available from deterministic grid methods.

Priority remains provisional. The
[continuation record](notes/research-20260922-continuation.md) distinguishes
these contributions from classical corollaries, screened directions, and
reviewed supporting work and documented open questions.

The [2026-09-22 corrective audit](notes/review-minlp-developments-20260922.md)
records a ten-agent review of the developments below, the errors corrected,
and targeted verification. Historical positive review verdicts are qualified
by that record.

- [Cluster-free spatial branch-and-bound at nondegenerate constrained minima](results/cluster-free-branch-and-bound-constrained-minima.md)
  (2026-09-22, proof by the root agent, literature check and one
  independent review, followed by a corrective audit): with second-order pointwise convergent relaxations of objective
  and constraints, the fixed KKT multipliers give
  `L(Z) >= f* + (gamma/4) dist(Z, z*)^2 - c_2 w(Z)^2` for every box near a
  minimizer satisfying LICQ, strict complementarity and second-order
  sufficiency, whether or not the box contains the minimizer; hence the number
  of unfathomable, interior-disjoint boxes with all side lengths in
  `[delta/2, delta]` is locally bounded independently of tolerance and scale,
  assuming an optimal incumbent (or incumbent error below the tolerance).
  This supplies a mixed-bound substitute for the neighborhood convergence
  condition discussed by Kannan and Barton (2018), rather than a total search-tree
  or runtime guarantee. Numerical illustration on a
  nondegenerate and a degenerate example. A
  [later source comparison and simpler proof](notes/research-20260922-error-bound-transfer.md)
  identifies the central inequality as an application of classical
  exact-penalty growth and removes LICQ and strict complementarity under
  feasible quadratic growth and a linear error bound. The novelty assessment
  is narrowed accordingly.
- [Convex hull of a bounded two-variable monomial with real exponents on a wedge](results/monomial-wedge-envelopes-real-exponents.md)
  (2026-09-22, proofs by the root agent, numerical check and one
  independent review, followed by a corrective audit): extends Belotti (Math. Program. 2025)
  from positive to negative and mixed-sign exponents with `a_1 + a_2 != 0`,
  addressing his question on negative exponents; six principal regimes, each envelope being the
  cap or floor of one of four candidate functions (the monomial, the affine
  corner interpolant, a power of a linear form, a power of the monomial),
  selected by quasi-convexity type and the sign of `beta` and `beta - 1`.
  Separate cases treat a zero exponent and degree zero; the latter requires
  distinguishing the ordinary convex hull from its closure.
- [Aggregation certificates for a trivial convex hull of a quadratic system](results/quadratic-aggregation-trivial-hull-certificate.md)
  (2026-09-21, theorem and corollaries independently reviewed): proves
  Conjecture 3.3 of Blekherman, Dey and Sun (SIAM J. Optim. 2024): under hidden
  hyperplane convexity and nonemptiness, the convex hull of `{f_i < 0}` is the whole space if and
  only if every nonzero nonnegative aggregation with positive semidefinite quadratic part
  is a negative constant function (`A_lambda = 0`, `b_lambda = 0`, `c_lambda < 0`).
  Only hyperplanes near infinity need convex images; corollaries for closed systems, complete aggregation certification,
  an SDP decision procedure, triviality of the Shor relaxation exactly when the
  hull is trivial, and checkable hypotheses for two or three quadratics (PDLC of
  the quadratic parts, with the scope qualification in Corollary 5); an example
  shows hidden convexity of the homogenized map alone does not suffice.
  The theorem guarantees existence of a nontrivial convex aggregation for a
  proper hull, not that globally convex aggregations describe the entire hull.
  The main theorem and its three supporting lemmas now have
  [Lean proofs](formal/topics/27-quadratic-aggregation/README.md).
  The [consequences extension](formal/topics/28-quadratic-aggregation-consequences/README.md)
  adds Corollaries 1, 3 and 4, Lemma 4, and the strict-feasibility and
  relaxation-strength counterexamples; other ancillary claims remain outside
  the verified scope.
- [Links between univariate terms that share a variable](results/shared-variable-term-links.md)
  (2026-09-21, exploratory, independently reviewed with corrections applied):
  redundant exact relations between auxiliary variables; mixed results, large
  uncertified dual-bound gains on the `waterno2` family with Gurobi, and a
  documented SCIP 10 solver error.
- [Row hulls of separable concave terms](results/row-hull-separable-concave.md)
  (2026-09-21 joint-convexification continuation): closed-form hull for
  equal-width rows (equivalent to the Padberg–Van Roy–Wolsey constant-capacity
  description; extended here to inequality rows and to indicators with concave
  variable costs), a valid residual-interval inequality and interval dynamic
  program for general rows, a three-variable example where row hulls see
  nothing, and solver experiments including cut-generation, model-construction
  and solve time (instance generation excluded). Theory
  and code independently reviewed with corrections applied (including a
  pricing bug that gave invalid cuts; fixed and rerun); computational claims
  qualified by unfavorable cases and a 4.8% MINLPLib structural reach.
- [Joint weighted potential optimization on cacti](results/potential-flow-joint-weighted-cactus-accuracy-bits.md)
  (2026-09-06 continuation): a fixed number of affine load factors permits
  arbitrary weighted potential objectives and independent continuous resistance
  intervals, with polynomial input-and-accuracy-bit additive optimization and
  rational original-scenario recovery. The number of cycles is unrestricted.
  A twice-reviewed nomination-face reduction also permits full balanced load
  boxes when objective support is fixed. With fixed rational nominations,
  exact optimal rational resistance profiles are polynomial-time computable,
  including under rational arc capacities; exact scalar comparison of the
  total objective remains a separate radical-sum question. Fixed-factor
  capacity filters allow algebraic feasible output. Both full proof reviews
  passed; the [source comparison](notes/potential-flow-reopened-weighted-literature.md)
  credits prior cycle formulas, approximate algebraic summation, and resistance
  uncertainty models. No matching combined theorem was found in the inspected
  primary sources; publication priority remains qualified.
- [Original-instance envelope certificates](notes/potential-flow-certified-envelope-pipeline.md)
  (2026-09-06 continuation): a numerical producer and standard-library exact
  verifier now check the original graph, uncertainty data, envelope construction,
  target interval, and recovered endpoint scenario. Conservation-aware goal
  witnesses tighten the bounds without another physical-flow solve. Ten bounded
  benchmarks passed, including 80 edges, a resistance ratio of one million,
  near-zero flows, and a documented quadratic adaptation of an open water-network
  topology. Two independent implementation reviews passed. These are certified
  achieved errors, not a production-scale performance or hydraulic-calibration
  claim; the convex and electrical projection mechanisms are established.
- [Capacity witnesses and resistance sensitivity](results/potential-flow-capacity-rational-witness-boundary.md)
  (2026-09-06 continuation): ordinary positive-width upper capacities can force
  an irrational resistance already on a simple series-parallel rank-two network,
  unlike the fixed-nomination cactus rational-feasibility result. A reviewed
  all-graph Lipschitz estimate gives explicit rational-rounding budgets when
  capacity slack is available. Exact examples and independent checks cover zero
  flows, flow reversals, and nonconvex upper-pressure filters.

Research was reopened on 2026-09-04 and closed on 2026-09-05. Entries marked
"reopened run" belong to that completed continuation.

- [Polynomial construction with near-minimal integer dimension](results/quadratic-nonlinear-input-rank-precision.md)
  (2026-09-05 continuation): for rational quadratic systems and arbitrary
  rational output tolerances, a deterministic polynomial bit-time algorithm
  builds a rational MILP using at most `O(r log(r+1))` more binaries than
  the minimum integer dimension of any convex lift, including unrestricted
  integers, where `r` is the rank of the stacked Hessians. Two full proof
  audits passed for both the original construction and this input-rank
  refinement. Established metric selection and
  geodesic algorithms are credited; the whole-formulation guarantee is the
  apparent new contribution. No practical runtime claim is made.
  A reviewed [approximation-hardness theorem](results/quadratic-integer-precision-approximation-hardness.md)
  rules out additive or multiplicative `O(n^(1-delta))` construction
  guarantees for any fixed `delta>0`, unless `P=NP`, even when the optimum
  integer count is positive. The dimension exponent is therefore nearly sharp.
  The doubly reviewed [general output-norm extension](results/quadratic-general-norm-output-precision.md)
  permits arbitrary symmetric convex error bodies supplied by a rational
  strong separation oracle and known inner and outer radii. Its additive
  binary-count guarantee is independent of the number of outputs.
  For [diagonal convex quadratic systems](results/diagonal-psd-quadratic-linear-dimension-precision.md)
  with componentwise tolerances, two audits verified the sharper bound
  `p_out <= p_conv + 5r + 1` and its polynomial rational construction.
  For [positive rational powers](results/rational-power-compiled-integer-precision.md)
  with exponents greater than one, two full audits verified
  `p_out <= p_conv + 7r + 1`, improving to `6.5r+1` when all exponents are
  at least two. Formulation size is polynomial in the binary exponent
  encoding. The [sparse positive polynomial mixture theorem](results/sparse-positive-polynomial-circuit-precision.md)
  gives `p_out <= p_conv + 4.5r + sum_i ceil(log2(ceil(log2(D_i))+1)) + 1`,
  also with polynomial size in sparse binary exponent lengths.
  Both results permit unconditional convex error budgets with the stated
  oracle access. Circuit compilation and interpolation are established;
  the comparison against arbitrary convex lifts is the candidate
  contribution. For a [scalar sum of dense positive polynomials](results/separable-convex-graph-linear-dimension-precision.md),
  the reviewed bound `p_out<=p_conv+12r` removes the degree-dependent
  overhead; independent scalar outputs admit `9r`. This is not uniformly
  smaller than the sparse bound, which is smaller at low degrees. The same
  theorem gives finite, unrestricted-size comparisons for all continuous convex
  separable functions. A [scalar curvature algorithm](results/compiled-curvature-quantile-precision.md)
  supplies the compact construction through certified indexed knots.
  The broader [dense convex polynomial theorem](results/convex-polynomial-compiled-integer-precision.md)
  removes coefficient-sign and curvature-monotonicity restrictions: the
  polynomial rational construction uses at most `p_conv+11` binaries in one
  variable, `p_conv+16r` for scalar separable sums, and `p_conv+13r` for
  independent outputs. Both full proof audits passed.
  A paired [nonconvex polynomial theorem](results/polynomial-graph-binary-integer-degree-gap.md)
  proves the boundary is substantive: two general integers suffice for an
  explicit one-variable family, while its binary count grows logarithmically
  with degree. Every dense scalar polynomial admits a compact construction
  with additive overhead `12+ceil(log2 D)`, matching that worst-case order.
  The reviewed [coupled convex-vector theorem](results/convex-vector-curvature-rank-precision.md)
  gives `p_conv+12+ceil(log2 r)` for one input, where `r` is the rank of
  output curvatures, independent of output count and polynomial degree.
  Its [polyhedral error-body extension](results/convex-vector-facet-curvature-rank-precision.md)
  uses `+13+ceil(log2 r)`; weighted one-norm error needs only the constant 13.
  For [arbitrary unconditional oracle bodies](results/convex-vector-unconditional-compiled-precision.md),
  `+14+ceil(log2 m)` suffices with `m` outputs, using a rational inscribed
  box in the final MILP. A stronger [oracle-body curvature-rank theorem](results/convex-vector-oracle-curvature-rank-precision.md)
  replaces the output-count dependence by `17+2ceil(log2 r)`.
  For [coupled separable inputs](results/convex-separable-vector-oracle-curvature-rank-precision.md),
  the overhead is `21n+2nceil(log2 r)`; explicit facet bodies have the
  sharper [separable bound](results/convex-separable-vector-curvature-rank-precision.md).
  The [nonconvex vector construction](results/polynomial-vector-compiled-integer-precision.md)
  instead has overhead `12+ceil(log2(sum_j D_j))`. All have two proof audits;
  established scalarization, basis selection, and shared-knot methods are credited.
  An explicit [exact-count family](results/convex-polynomial-box-error-exact-integer-gap.md)
  shows that linear overhead in input dimension can be necessary:
  degree-32 convex outputs with unit box error have `p_conv=n` and
  `p_bin=ceil(n log2 3)`. This is an unconditional optimal-count separation.
  Further reviewed bounds cover
  [PSD coordinate blocks](results/block-psd-unconditional-error-precision.md)
  and [independent integer linear features](results/independent-integer-feature-quadratic-precision.md),
  including a linear-overhead [forest Laplacian case](results/forest-laplacian-quadratic-precision.md).
  A reviewed [encoding separation](results/small-exponent-milp-soc-encoding-separation.md)
  shows why integer count and rational formulation size are different:
  fixed-error graphs of `x^(1/2^B)` require `Theta(2^B)` rational MILP bits,
  but admit polynomial-size rational MISOCPs. Four binaries suffice in
  both constructions; the conic guarantee uses exact feasibility.
- [Exact bilevel robustness to near-optimal follower choices](results/bilevel-near-optimal-response-robustness.md)
  (2026-09-06/07 continuation): fixed leader, local-block, aggregate, resource,
  and per-criterion measurement dimensions permit polynomial exact robust
  feasibility, infimum computation, attainment decision, and algebraic
  adversarial witnesses. Follower dimension and upper-criterion count may grow;
  aggregate follower costs may be nonconvex. Two full proof audits passed.
  [Certified surrogate screening](results/bilevel-surrogate-screening-exact-optimization.md)
  solves dense quadratic followers exactly using at most `M*3^t` recovery LPs,
  where `t` counts uncertified statuses per surrogate cell. A computable
  perturbation neighborhood bounds `t` by `(r+1)q`, with `q` the vertex
  transition multiplicity. Both theorem and corollary passed two audits.
  [Convex polynomial aggregate coupling](results/bilevel-convex-aggregate-accuracy-bit-algorithm.md)
  extends global accuracy-bit approximation beyond separable followers.
  The [upper-constraint extension](results/bilevel-response-constraint-accuracy-bit-algorithm.md)
  covers polynomial objectives and constraints: unconditional bicriteria
  guarantees and exact rational feasibility under explicit tightening
  conditions. Both results have two full proof audits. The
  [scalar quadratic implementation](notes/bilevel-reopened-quadratic-algorithm.md)
  supplies exact response-path certificates and a complete aligned rank-one
  tariff sweep; recorded experiments are synthetic, not industrial validation.
  Known robustness, screening, and parametric-QP mechanisms are credited;
  the structural complexity combinations retain qualified novelty claims.
- [Exact global bilevel optimization with many follower variables](results/bilevel-fixed-aggregate-response-algorithm.md)
  (2026-09-05 continuation): a fixed number of leader variables, resource
  rows, and aggregate outputs permits polynomial exact optimistic bilevel
  optimization. The follower has positive diagonal quadratic local costs
  and a possibly nonconvex polynomial aggregate cost. Polynomial degree
  may grow under the stated dense or unary encoding. Two full audits and
  a separate exact-arithmetic audit passed. Global follower optimality is
  imposed by comparing all compressed stationary responses; it is not
  inferred from stationarity alone. Earlier resource-allocation methods
  are credited, and the full theorem's priority remains provisional.
  The doubly reviewed [quadratic-block extension](results/bilevel-fixed-block-response-algorithm.md)
  allows fixed-dimensional positive-definite local quadratic programs
  with arbitrarily many local polyhedral rows.
  The reviewed [full constraint-matrix variant](results/bilevel-compressed-response-infimum-semantics.md)
  permits polynomially varying normals and pessimistic follower choices.
  It computes exact infima and decides attainment, including cases with
  no optimizer.
  A complementary [well-conditioned NP-completeness theorem](results/bilevel-well-conditioned-box-exact-hardness.md)
  has one continuous leader, no upper constraints, an affine upper objective,
  and a unique quadratic follower response on a fixed unit box. The follower
  Hessian has condition number below two, and coefficient magnitudes are
  bounded by two. Its gap is exponentially small. The reviewed
  [additive approximation algorithm](results/bilevel-conditioned-box-additive-algorithm.md)
  runs in time polynomial in input size, condition number, and `1/epsilon`
  for fixed leader dimension, with error `epsilon*||a||_1` for follower
  objective coefficients `a`. Thus conditioning does not remove the barrier
  to polynomial dependence on accuracy bits. Both results have two audits.
  In contrast, [diagonal power-cost followers](results/bilevel-bounded-power-accuracy-bit-algorithm.md)
  admit rational additive optimization in time polynomial in input size,
  accuracy bits, and numerical maximum power, for fixed leader dimension.
  Dense or unary growing powers are covered. The reviewed
  [fixed-resource extension](results/bilevel-fixed-resource-accuracy-bit-algorithm.md)
  permits arbitrary dense strictly convex polynomial local costs, including
  signed coefficients, with fixed leader and resource dimensions. Its
  rational leader is exactly feasible; response-dependent upper constraints
  remain excluded. Both full extension audits passed. The
  [bilevel scope map](notes/bilevel-response-complexity-map.md) separates
  these exact, approximate, and representation guarantees.
  A reviewed [leader-interaction boundary](results/bilevel-leader-vertex-integrity-boundary.md)
  gives exact polynomial optimization when deleting a fixed leader core
  leaves components of fixed size. Even a path is weakly NP-complete when
  the component size is unrestricted. Identical local factors can also
  produce exponentially many pieces in an explicit elimination message.
- [Exact optimization with a fixed nonlinear core and small blocks](results/fixed-core-block-polyhedral-optimization.md)
  (2026-09-05 continuation): polynomial bit-time global optimization with
  fixed core dimension, local polyhedral block dimension, and aggregate
  constraint dimension. It gives exact pooling algorithms for fixed inputs
  and pools with unrestricted outputs, qualities, and bypasses; and for fixed
  pools and qualities with unrestricted inputs and outputs without arbitrary
  bypasses. Both proof audits passed. These answer the corresponding
  fixed-pool questions in Haugland (2016); later-literature priority is still
  being checked. The exponent depends on the fixed dimensions.
  The reviewed [bypass-structure theorem](results/pooling-bypass-structure-algorithm.md)
  unifies both corollaries: fixed pool count, affine quality rank, and bypass
  vertex integrity suffice, allowing arbitrarily many quality attributes
  and suitably structured bypasses.
- [The pooling problem is complete for the existential theory of the reals](results/pooling-existential-theory-of-reals.md)
  (2026-09-05; completed proof audits and closing reconciliation): Haugland's
  pooling threshold decision problem with one quality attribute, source
  qualities in `{0,1}`, and lower/upper terminal bounds is `∃R`-complete by a gadget reduction from
  ETR-INV. Hence it is not in `NP` unless `NP = ∃R`, and rational instances
  can require optimal flows of arbitrary algebraic degree. Two independent
  proof audits passed with corrections (applied); no matching statement was
  found in the inspected primary sources. General QCQP completeness is
  established and credited. A bounded-data variant
  (capacities, bounds, qualities, and costs from a fixed finite set; the
  objective threshold remains instance-dependent,
  in-degree at most two, out-degree at most three) passed a separate audit.
  The [one-pool sharpening](results/pooling-one-pool-bypass-existential-reals.md)
  (two audits passed with minor corrections, applied) shows that a single
  pool with bypass arcs and unboundedly many attributes is already
  `∃R`-complete, whereas one pool without bypasses or with fixed attributes
  is in `NP`. Whether one attribute with upper bounds only suffices is
  recorded as open. The attempted upper-only gadget route is incomplete;
  its connection to concave-only constraint systems is not an equivalence
  proof or a necessity result for other possible reductions.
- [AC power flow feasibility is `∃R`-complete](results/ac-power-flow-existential-reals.md)
  (2026-09-05; three audits, corrections applied): the resistive
  power-flow model with power-injection bounds (voltage times linear
  current) is `∃R`-complete by the same gadget technique. Under the stated
  real angle-difference restrictions, zero reactive injections force equal
  angles across purely resistive lines, so full AC
  feasibility is `∃R`-complete even with resistive lines, zero reactive
  injections, degree three, and fixed finite data. This sharpens the
  NP-membership doubt of Bienstock and Verma (2019) into a conditional
  impossibility; their specific lossless fixed-magnitude system is not
  covered. The audits caught and the text now handles a real subtlety:
  angle limits must be on real angle differences (or bus-angle boxes),
  since principal-difference limits admit winding solutions on cycles;
  membership in `∃R` for real angles is proved by a winding-number
  crossing count.
- [Two pools and two outputs already give NP-complete pooling](results/pooling-two-pools-two-outputs-hardness.md)
  (2026-09-05 continuation): with an unrestricted number of qualities, only
  upper quality bounds and capacities one or two suffice. The network is a
  tree with one mixing pool and one pure anchor pool. Two proof audits passed.
  This answers the fixed-terminal portion of Haugland's fixed-pool question
  negatively; a reviewed split-fraction certificate gives NP membership.
  Strong hardness is not claimed.
- [Quadratic systems and noncommutative rank](results/quadratic-system-noncommutative-rank-complexity.md)
  (2026-09-05 continuation): half the noncommutative rank of the Hessian
  space gives the exact leading integer-dimension coefficient as accuracy
  improves, for arbitrary convex lifts and for matching compact MILPs.
  This generalizes the common-accuracy, two-sided leading asymptotic rank
  laws of the graph and scalar results below; it does not replace their
  finite or one-sided bounds. Two proof
  audits passed; a separate primary-source audit
  found no matching theorem. The reviewed
  [rational construction](results/quadratic-ncrank-rational-construction.md)
  gives deterministic polynomial bit-time construction and uniform
  polynomial input-size overhead around the sharp precision coefficient.
  A reviewed [perspective transfer](results/perspective-integer-precision.md)
  gives the same sharp law for quadratic-over-linear systems.
- [Smooth nonlinear maps and local rank](results/smooth-map-local-rank-integer-complexity.md)
  (2026-09-05 continuation): noncommutative Hessian rank at one point gives
  an integer-precision lower bound through a classical oscillatory-integral
  estimate. Full rank gives the exact coefficient of half the input
  dimension. Fixed-degree polynomial maps have matching compact MILPs in
  that case. Two proof audits passed. General smooth
  maps have only a local/global rank bound, with counterexamples to equating
  the answer to global Hessian-span rank. The reviewed
  [constant scalar Hessian-rank theorem](results/constant-hessian-rank-smooth-precision.md)
  gives the exact coefficient even when the Hessian null spaces rotate.
- [Finite weighted quadratic precision](results/quadratic-weighted-covariance-precision.md)
  (2026-09-05 continuation): one maximum-determinant covariance problem
  characterizes integer dimension for arbitrary unequal output accuracies,
  within an additive term depending only on dimension. Two audits passed.
  The benchmark is geodesically convex; its reviewed polynomial bit-time
  optimizer supplies the construction listed above.
- [Strong NP-completeness with one pool and constant physical data](results/pooling-constant-data-two-feed-np-completeness.md)
  (2026-09-05 continuation): one scalar upper quality, exactly two pool
  feeds and two pool outputs, zero lower flow bounds, input out-degree at
  most two, and output in-degree at most three suffice. Qualities,
  capacities, costs, and revenues lie in fixed finite sets; the objective
  threshold is linear in network size. Two full audits and independent
  physical-network checks passed. Binary copy circuits and a contract
  completion objective strengthen the earlier large-coefficient reduction.
  Total external input count is unbounded. No approximation-gap or
  numerical-robustness guarantee is claimed; publication priority is being
  checked separately from the established broad one-pool hardness claim.
  A reviewed [linear-fiber certificate lemma](results/fixed-parameter-linear-fibers-np-membership.md)
  supplies NP membership despite potentially irrational mixing parameters.
  The complementary [degree-two bypass algorithm](results/pooling-degree-two-boundary-projection.md)
  gives polynomial feasibility and exact optimization with a fixed number
  of objective arc coordinates, even with many qualities. With one pool,
  two feeds and two outlets, and input total degree at most two, output
  degree two permits polynomial feasibility, while output degree three is
  strongly NP-complete. The hard feasibility side uses explicit positive
  flow contracts; all-zero lower bounds would make feasibility trivial.
  A further [product-contract algorithm](results/pooling-fixed-product-contracts-algorithm.md)
  allows arbitrarily many feeds and qualities when the outlet count is fixed.
  Exact source supplies and exact contracts at products not receiving pool
  flow reduce shared balances to a fixed boundary. It permits standard
  production costs and product revenues, with exact algebraic optimization.
  The stronger [contract-exception theorem](results/pooling-contract-exceptions-algorithm.md)
  allows arbitrarily many feeds, outlets, and qualities of arbitrary rank.
  A fixed number of external nodes may depart from exact flow and product
  quality contracts; shared pool bounds must be redundant. Degree-two
  bypass structure then permits exact standard economic optimization.
  Both full audits passed.
- [Contracted degree-two pooling with common throughput bounds](results/pooling-contracted-common-capacity-algorithm.md)
  with one pool admits polynomial exact feasibility with arbitrary common lower and upper
  pool bounds and individual arc lower bounds. It requires exact source and
  product contracts and scalar or affine-rank-one qualities. Both extension
  audits passed; witnesses may have polynomial algebraic degree.
- [Pooling feasibility with two source-quality vectors](results/pooling-two-source-qualities-convex-feasibility.md)
  is polynomial for one pool with arbitrary bypass topology, variable source supplies,
  exact product contracts, and restrictive upper pool capacities. Two final
  proof audits passed. A shared convex quadratic constraint gives exact
  rational feasibility; positive outlet or common pool lower bounds are
  outside this theorem.
- [Global energy maximization on any connected graph](results/potential-flow-global-energy-maximization.md)
  permits a global rational resistance polytope and fixed nominations.
  The reviewed conic formulation produces a rational additive-optimal
  resistance profile, with exact rational certificates for proposed designs.
  This is supporting theory based on classical energy concavity and duality;
  minimizing the same energy under global correlations can be strongly hard.
- [Potential optimization with bounded cycle rank in every block](results/potential-flow-bounded-block-rank.md)
  (2026-09-05 continuation): the cactus additive algorithm extends to
  interacting cycles, arbitrary shifted nomination intervals, and arbitrarily
  many blocks. Two proof audits and a separate source audit passed. The
  polynomial exponent depends on the maximum block cycle rank. The
  [joint resistance-uncertainty extension](results/potential-flow-joint-resistance.md)
  and [exact arc-capacity validation](results/potential-flow-exact-arc-capacity.md)
  also passed two proof audits. The latter decides all rational flow limits
  exactly, despite the separate arithmetic barrier for pressure comparisons.
  A reviewed [fractional-power boundary](results/potential-flow-fractional-power-arc-barrier.md)
  shows that exact arc comparison is already Square-Root-Sum-hard on one
  cycle for certain fixed fractional powers. Law representation matters.
  The [dense polynomial-law extension](results/potential-flow-polynomial-law-uncertainty.md)
  also passed two audits. It permits continuous piecewise laws, growing
  dense degrees, and independent affine coefficient uncertainty.
  The reviewed [fractional-power additive algorithm](results/potential-flow-fractional-additive-optimization.md)
  covers fixed finite exponent families in `(1,3)`, including different
  exponents on different edges, with joint nomination/resistance uncertainty.
  In contrast, reviewed [discrete-resistance hardness](results/potential-flow-discrete-resistance-hardness.md)
  shows that independent two-point resistance sets make high-precision
  pressure optimization NP-hard already on a graph with block cycle rank two.
  For discrete uncertainty, [exact arc validation](results/potential-flow-discrete-arc-capacity-hardness.md)
  is coNP-complete at block cycle rank three, whereas the reviewed
  [series-parallel theorem](results/potential-flow-series-parallel-arc-validation.md)
  gives polynomial exact validation at block cycle rank at most two.
  Classical nonlinear-circuit monotonicity is credited; priority relative
  to older tolerance-analysis work remains unresolved.
  With fixed nominations, the doubly reviewed
  [single-network uncertainty algorithm](results/potential-flow-series-parallel-envelope-optimization.md)
  removes the rank restriction on series-parallel graphs: a target-specific
  modified network gives the exact extremum identity, a linear-size SOCP,
  polynomial-bit additive approximation, and an endpoint resistance witness.
  The [flow complexity map](notes/potential-flow-complexity-map.md)
  distinguishes exact arithmetic, nomination uncertainty, discrete
  resistance choices, block rank, and different physical laws.
  For weighted potential objectives, [discrete resistance optimization is
  NP-complete already on one cycle](results/potential-flow-weighted-potential-cycle-hardness.md)
  with fixed nominations. With growing objective support, nomination
  optimization is [NP-complete on degree-three trees](results/potential-flow-weighted-tree-np-completeness.md)
  with fixed resistances. Both boundaries have two proof audits and retain
  explicit attribution to their established reduction ingredients.
  The reviewed [fixed-support tree algorithm](results/potential-flow-fixed-support-weighted-tree.md)
  returns exact rational optima with nomination and finite or interval
  resistance uncertainty. Fixed total cycle rank and fixed objective support
  also permit [exact algebraic optimization](results/potential-flow-fixed-support-global-rank.md)
  under resistance intervals; two full audits passed for each algorithm.
- [Spatial B&B beyond all quadratic box cuts](results/spatial-bb-quadratic-cut-exponential-lower-bound.md)
  (2026-09-05 continuation): sparse cubic instances need exponentially many
  certified spatial regions even with high-order box preorderings and the
  exact quadratic moment hull of every node box. The reviewed
  [monomial-lift extension](results/spatial-bb-monomial-lift-exponential-lower-bound.md)
  permits branching on arbitrary bounded-degree monomial auxiliaries,
  including a standard quadratic formulation with a linear objective.
  Two proof audits passed. Classical XOR pseudomoments are credited; the
  hull granted here is the box hull, not the hull of the feasible lifted graph.
- [Polynomial additive optimization of cactus potential flows](results/potential-flow-cactus-additive-optimization.md)
  (2026-09-05 continuation): arbitrary rational interval nominations on a
  quadratic passive cactus admit polynomial bit-time additive approximation,
  with a feasible rational nomination and a certified optimal-value interval.
  A new structural reduction leaves at most two free aggregate loads in one
  cycle. Two proof audits and a separate source audit passed. The result
  concerns MPD without imposed potential or arc-flow bounds; exact threshold
  comparison has a separate arithmetic barrier below.
- [Pooling with all four degrees exactly two](results/pooling-all-degrees-two.md)
  (2026-09-05 continuation): strong NP-hardness with one quality, unit
  capacities, and bounded constant costs. A polynomial rounding theorem
  converts every feasible flow into integral pure modes without losing profit,
  giving an exact independent-set reduction and a no-PTAS result. Two
  independent reviews and separate original-flow numerical checks passed.
  This closes the degree restriction left open by the preceding local result.
  A reviewed positive-purity-tolerance extension is linked.
- [Integer dimension of bilinear graph approximation](results/bilinear-graph-binary-complexity.md)
  (2026-09-05 continuation): fractional vertex cover gives the exact leading
  coefficient of the minimum integer dimension as accuracy improves. The
  lower bound permits unrestricted integer ranges and arbitrary convex lifts;
  a compact shared binary discretization matches it. Unequal accuracies have
  finite LP bounds within an additive graph-dependent constant. Two proof
  reviews passed; primary-literature comparison found no matching theorem,
  with known parity and discretization mechanisms credited.
- [Quadratic rank and integer dimension](results/quadratic-rank-integer-complexity.md)
  (2026-09-05 continuation): for a scalar quadratic graph on a box, half the
  Hessian rank is the exact leading integer-dimension coefficient as accuracy
  improves, regardless of signature. A maximal-simplex volume bound covers
  arbitrary convex lifts; a compact signed-square construction matches it.
  Independently reviewed, with established approximation geometry credited.
  The [one-sided extension](results/quadratic-inertia-one-sided-integer-complexity.md)
  gives half the negative inertia for epigraphs and half the positive inertia
  for hypographs. It also gives an exact convex-lift precision law for the
  product epigraph. Independently reviewed.
- [Exact cactus potential comparison](results/potential-flow-cactus-square-root-sum.md)
  (2026-09-05 continuation): single-source/sink quadratic cactus MPD threshold
  comparison is polynomial-time equivalent to Square-Root Sum. Hardness holds
  on degree-three triangle cacti with integer resistances and unit bookings.
  Proof and novelty audits are separate and complete. This is an exact
  arithmetic barrier, not NP-hardness or an approximation lower bound.
- [Spatial B&B lower bounds with full SDP and RLT](results/spatial-bb-sdp-rlt-exponential-lower-bound.md)
  (2026-09-05 continuation): exponentially many spatial boxes remain necessary
  at fixed tolerance even with a full second-moment SDP, all box RLT cuts,
  and equality products. Independently reviewed and numerically checked.
  Prior binary B&B lower bounds are explicitly distinguished from the
  arbitrary continuous split model here. The reviewed
  [higher-order SOS extension](results/spatial-bb-higher-sos-exponential-lower-bound.md)
  retains exponential covers through specified linear moment orders,
  including an asymmetric objective with a unique optimizer. Product-domain
  and local polynomial auxiliary extensions are linked from the investigation.
- [Scalar formulation binary and integer lower bounds](results/mip-relaxation-binary-lower-bounds.md)
  (2026-09-05 continuation): the previously unreviewed square/product draft
  passed independent review, with scope and wording repairs. The square
  has an exact binary optimum; the product has matching-order bounds. The
  established parity method extends lower bounds to unbounded general integers.
- [Geoffrion common-optimizer compactness boundary](results/geoffrion-property-p-conjecture.md)
  (2026-09-05 continuation): a reviewed SOC-representable counterexample
  separates the exact Property P-prime conditions despite Slater feasibility
  and attained individual maxima. Positive sufficient conditions are included.
  This does **not** refute the informal computational Property P conjecture;
  its contribution is a narrower structural clarification.
- [One-quality pooling with degree-two pools](results/pooling-one-quality-degree-two-hardness.md)
  (reopened run): open problems 2 and 3 of Boland, Kalinowski, and Rigterink
  (2017) are answered. With one quality, the standard pooling problem is
  strongly NP-hard when all in-degrees are at most two (outputs even of
  in-degree one) and, separately, when all out-degrees are at most two
  (inputs even of out-degree one); pools have the smallest hard degree
  pattern `(2,2)`, and the remaining layer needs degree only three. Reduction
  from `{1,2}`-weighted capacitated orientation. Gurobi cross-check and two
  independent reviews passed for the main theorems, and a third review
  passed the degree-three refinement. Novelty audit in
  [the companion note](notes/pooling-degree-two-novelty.md).
- [Exponential lower bound for spatial branch-and-bound](results/spatial-bb-exponential-lower-bound.md)
  (reopened run): for a separable concave QP with one knapsack equality, any
  variable-branching spatial B&B with separable (chord, McCormick, αBB)
  relaxations needs `2^{Ω(n)}` leaves to certify a fixed tolerance when the
  knapsack level is a constant fraction of `n`, whatever the branching rule;
  a matching `O(2^n)` tree exists, and fixed levels are polynomial. One
  independent review passed with corrections (applied). An initial novelty
  search found no prior spatial-B&B tree-size lower bound of this kind; a
  later comparison identified Coniglio's spatial lower bound under midpoint
  branching and Jarre's binary-SDP lower bound, so the tentative novelty
  claim is restricted to this arbitrary-split, fixed-gap separable-relaxation
  model.
- [Positive multilinear gap](results/positive-multilinear-gap.md):
  A [standalone paper and Lean bundle](paper-multilinear-gap/README.md)
  contains the conjecture disproof, exact dyadic gap, and sharp leading
  degree/dimension asymptotics, with a focused PDF and reproducible proofs.
  The result resolves the universal-constant conjecture and gives the
  sharp asymptotic worst ratio `ln d / ln ln d` by degree and
  `ln n / ln ln n` by dimension,
  with leading constant one. Sparse unit-coefficient lower examples and the
  [matching universal coupling](results/positive-multilinear-sharp-degree-growth.md)
  passed two independent reviews and root review. No prior resolution found in
  targeted searches; priority remains qualified. A reviewed
  [finite bound](results/positive-multilinear-second-order-upper.md) improves
  the lower-order loss without claiming a matching second-order lower bound.
  The [joint characterization](results/positive-multilinear-joint-gap-growth.md)
  combines dimension, degree, incidence width, and distance of the evaluation
  point from box faces, with a single lower family meeting every restriction.
- [Cubic positive multilinear gaps](results/positive-cubic-gap.md):
  exact certificates show that degree three already permits ratios above two;
  a reviewed [analytic family](results/positive-cubic-analytic-family.md)
  proves `R(3) >= 483/223`, with a small certified improvement of
  the lower bound to `1610000/743033` recorded in its proof.
  The [improved upper bound](results/positive-cubic-rounding-upper-bound.md)
  `R(3) <= 31/12` uses a reviewed mixture of three global couplings. The
  [focused cubic paper and Lean package](paper-cubic-gap/README.md) collects
  these bounds, fixed-mixture optimality, and exact finite witnesses with
  a complete mathematical claim map and verification records.
  [Coefficient removal](results/positive-multilinear-coefficient-removal.md)
  transfers fixed-degree suprema to homogeneous unit-coefficient polynomials
  when dimension may grow. Independently reviewed.
  A [simple explicit witness](results/positive-cubic-two-level-family.md)
  uses 52 variables, homogeneous cubic terms, unit coefficients, and strictly
  interior means. [Equal means](results/positive-multilinear-equal-marginals.md)
  (equal normalized coordinate values on the unit cube) always give ratio at
  most two, as a reviewed consequence of classical envelopes.
- [Frequency-two multilinear gaps](results/positive-multilinear-frequency-two-gap.md):
  sharp ratio `3/2` when each variable occurs in at most two nonlinear terms,
  with an odd-girth refinement and exactness for bipartite dual graphs.
  Independently reviewed; unit boxes and zero lower bounds only.
  A [three-variable counterexample](notes/multilinear-frequency-two-positive-box-obstruction.md)
  shows that bipartite exactness fails with positive lower bounds.
  The [convex-cardinality extension](results/convex-cardinality-frequency-two-gap.md)
  restores the sharp bounds on positive boxes with a common aspect ratio and
  includes a classical matching-based scalar-envelope oracle.
- [Feedback-variable multilinear gaps](results/positive-multilinear-feedback-gap.md):
  deleting `f` variable nodes to leave an incidence forest gives ratio at most
  `2^f`, independently of degree. Sharp for `f=1`; independently reviewed.
- [Sharp incidence-treewidth and sparsity growth](results/positive-multilinear-incidence-sharp-growth.md):
  the worst gap ratio is asymptotic to `k`, with leading constant one, by
  incidence treewidth, degeneracy, or minimum maximum orientation outdegree.
  A variable-radix construction and a matching coupling bound are independently
  reviewed. Unit boxes and zero lower bounds only. The separately reviewed
  [exact treewidth-two theorem](results/positive-multilinear-treewidth-two-exact.md)
  gives sharp constant two through a partition into two totally unimodular
  incidence matrices; larger fixed-width values remain open.
- [Sharp growth near lower box faces](results/positive-multilinear-marginal-floor-gap.md):
  with every normalized mean at least `delta`, the worst gap is asymptotic to
  `ln(1/delta)/ln ln(1/delta)`, independently of degree and dimension.
  Leading constant one; two independent reviews passed. The same asymptotic
  holds when all means lie in `[delta,1-delta]`.
- [Sharp positive-box aspect-ratio growth](results/positive-multilinear-positive-box-sharp.md):
  on strictly positive boxes, `max{2,rho} <= C_box(rho) <= rho+2`, where `rho`
  bounds every upper/lower endpoint ratio. Both upper-proof reviews and the
  separate lower-proof audit passed; degree and dimension are unrestricted.
  [Single-monomial hardness](results/positive-box-single-monomial-hardness.md)
  shows that exact envelope evaluation can still be NP-complete on narrow
  unequal boxes. It does not claim hardness at fixed additive accuracy.
  Its positive rank-one multimarginal optimal-transport consequence answers
  a published logarithmic-precision question negatively in the rational bit
  model unless P=NP. The [source and proof audit](notes/review-rank-one-mot-precision.md)
  and [later-literature check](notes/rank-one-mot-precision-later-literature.md)
  are complete; publication priority remains unestablished.
- [Rank-one correlation face and conic lower bounds](results/rank-one-correlation-face-conic-lower-bounds.md):
  a correlation-polytope face in the hull with zero lower bounds and unit capacities;
  unconditional lower bounds on exact SOCP and SDP lifts. Independently reviewed.
- [Rank-one hardness with zero lower bounds](results/rank-one-zero-lower-hardness.md):
  a quantitative repair lemma and exact penalty prove strong NP-hardness with only
  unit capacities. Independently reviewed; exact rational checks passed.
- [Rank-one optimization complexity](results/rank-one-row-column-hardness.md):
  strong NP-completeness, rational decision certificates, and an algorithm fixed-parameter
  tractable in the smaller matrix dimension. Independently reviewed.
- [Bilinear relaxation gap and graph density](results/mccormick-gap-degeneracy-bound.md):
  bounds `4√ρ`, `2√Δ`, and a sharper bipartite bound, where `ρ` is maximum induced
  edge density. Independently reviewed. [Graph-by-graph characterization](results/mccormick-hereditary-density-characterization.md)
  follows up with matching order, which is also a consequence of older Schur-multiplier
  theory; it is retained as an elementary proof and explicit MINLP application.
- [Low-interaction-rank flow costs](results/rank-one-low-rank-costs.md):
  polynomial exact optimization for fixed interaction rank and an exact pool
  Lagrangian subproblem oracle for a fixed number of qualities. Independently
  reviewed; earlier low-rank optimization methods are credited.
- [Pooling triviality and the uncapacitated conic hull](results/pooling-triviality-polynomial.md):
  a polynomial sign test for acyclic generalized pooling, a profitable witness
  using at most `K+1` paths for `K` qualities, and an exact polyhedral conic hull.
  Independently reviewed. These are explicit consequences of established
  destination-disaggregation machinery; the capacitated convex hull is different.
- [FBBT limiting-bound hardness](results/fbbt-monotone-system-hardness.md):
  constant-accuracy approximation is PosSLP-hard for a restricted feasible bilinear
  family. Independently reviewed; the [literature assessment](notes/fbbt-novelty.md)
  records the prior mechanisms and remaining priority limits.
- [Doubly exponential primitive-FBBT iteration bound](results/fbbt-doubly-exponential-convergence.md):
  a small circuit creates extremely slow interval propagation. Independently reviewed;
  the statement concerns the specified primitive contractors.
- [Rank-one face stability](results/rank-one-correlation-face-stability.md):
  quantitative face rounding and exponential approximate LP size at entrywise
  error of order `m^-2`. Independently reviewed.
- [Approximate SDP lower bounds](results/rank-one-approximate-sdp-lower-bound.md):
  stretched-exponential SDP order is necessary at the same `m^-2` error scale.
  Independently reviewed; precise constants and metrics are in the theorem.
- [Switching-control conjecture and sharp one-switch theorem](results/cia-uniform-switching-obstruction.md):
  exact counterexamples and a sharp continuous one-switch minimax formula for
  arbitrary numbers of modes. The [three-mode finite-grid result](results/cia-exact-three-mode-one-switch.md)
  gives exact values for every grid size. Independently reviewed; no prior
  resolution found in targeted searches.
- [Exact one-switch minimax on arbitrary finite grids](results/cia-finite-grid-one-switch-minimax.md):
  an explicit formula takes `O(N^2)` rational operations and constructs a worst
  control with two component types and at most three phases. It includes all
  `n>=3` and nonuniform grids; five modes and nine unit cells give `17/5`.
  Independent mathematical and implementation reviews passed.
- [Exact algorithms for a fixed switch budget](results/cia-fixed-switch-budget-algorithm.md):
  one-switch instance optimization takes `O(nN)` arithmetic operations and
  two-switch optimization takes `O(nN^2)`. A subset dynamic program permits
  repeated modes and mode-specific minimum dwell times. Exact implementations
  and public-profile benchmarks are independently checked.
- [Sharp switch-preserving grid transfer](results/cia-sharp-grid-transfer.md):
  uniform-grid restriction costs less than one grid width for each fixed input,
  without increasing switches. The universal constant is sharp; two modes admit
  a sharp half-width schedule transfer even on nonuniform grids. Established
  support-preserving rounding is credited.
- [Five-cell, three-mode, two-switch minimax](results/cia-five-interval-two-switch-minimax.md):
  the exact error is one cell width. Two independent integer enumerations prove
  the upper bound, contradicting the published Corollary 5 lower bound of `8/7`
  cell widths for these parameters.
- [Exact two-switch rounding](results/cia-exact-two-switch-worst-case.md):
  for arbitrary measurable controls and `n>=4` modes, the worst error is
  `T max{1/4, (n-1)^3/[n(3n^2-3n+1)]}`. Four through seven modes give
  `T/4`; uniform relaxed controls are worst-case from eight modes onward.
  Three independent proof reads passed, alongside exact rational checks.
  No prior matching formula found in the qualified literature audit.
- [Exact three-switch rounding](results/cia-exact-three-switch-worst-case.md):
  for `n>=5`, the worst error is `T max{1/5, 1/[n((n/(n-1))^4-1)]}`.
  The all-mode reach proof uses independently audited exact finite and symbolic
  certificates; the heavy-mode and transfer arguments are analytic.
  An [arbitrary-block bound](results/cia-arbitrary-block-one-sided-bound.md)
  supplies a general one-sided rounding guarantee.
- [General switching-control reduction and bounds](results/cia-universal-heavy-mode-rounding.md):
  a reviewed analytic heavy-mode theorem gives the exact identity
  `F_(n,k-1)=max{T/(k+1),G^-_(n,k)}` for `1<=k<n`, with repeated modes
  allowed in the one-sided problem. The [global consequence](results/cia-arbitrary-switch-global-bound.md)
  gives an exact plateau for `k+1<=n<=k(k+1)/2` and the sharp first
  correction in `1/n` for every fixed switching budget and arbitrary profiles.
  Exact finite-mode values outside the proved ranges remain open.
- [Stronger general bounds from the four-block seed](results/cia-seeded-arbitrary-switch-bound.md):
  a maximum/minimum-mass removal argument improves the general one-sided bound
  and proves the additional exact case `F_(16,4)(T)=T/6`. The general higher-budget
  exact formula remains open; an invalid event-relaxation route is documented.
- [Fixed-linking-row common-factor optimization](results/common-factor-fixed-linking-optimization.md):
  exact polynomial-time scalar-product optimization for fixed linking dimension,
  including integer multiplicities. Independently reviewed; close prior mechanisms credited.
- [Reciprocal-anchor hull](results/common-factor-reciprocal-anchor-full-hull.md):
  an explicit hull, exact rational separation, and constructive decomposition
  for arbitrarily many box-bounded leaves. Independently reviewed; classical
  convex-order foundations credited. [Small-block obstructions](results/common-factor-reciprocal-anchor-hulls.md)
  explain why intersecting individual leaf hulls fails. The independently reviewed
  [integer-anchor extension](results/common-factor-integer-anchor-hull.md) has an exact
  rational oracle polynomial in the encoded range, and also permits binary leaves.
- [Observation-sensitive network–simplex hulls](notes/network-simplex-observed-rank-elimination.md)
  (2026-09-07 continuation): a sparse exact extended formulation can be built
  using one auxiliary coordinate per independent cycle entirely unobserved by
  an active simplex label; necessity is not claimed. If every such unobserved
  subgraph is a forest, an explicit original-variable hull suffices on
  arbitrary graphs. Independent proof and
  implementation reviews passed. Reduced RLT reconstruction and simplex
  disaggregation are established and credited. The
  [general compressed implementation](code/network_simplex_compressed/README.md)
  combines exact rational model construction with numerical LP solves and
  separately verified rational Farkas cuts. Numerical feasibility is not an
  exact certificate. [Repeated synthetic benchmarks](notes/network-simplex-reopened-computation.md)
  favor compression over full disaggregation and repeated cutting; additional
  observed-coordinate elimination reduces size but did not reduce total runtime
  on those cases.
- [Bounded-rank network–simplex coefficients](results/network-simplex-bounded-rank-hull.md)
  (2026-09-07 continuation): an explicit original-variable separator has
  parameter-dependent preprocessing and input-linear arithmetic work at fixed
  maximum block cycle rank. Its integer flow/product coefficient bound depends
  only on that rank. The sharp rank-three bound is two, witnessed by a
  unit-capacity K4 example with seven observed products. Independent full proof
  review and exact/numerical checks passed. Normal-fan and network-matrix
  foundations are classical; this is not a new general separation-complexity
  result.
- [Exponential coefficients on sparse series–parallel networks](results/network-simplex-series-parallel-coefficient-growth.md)
  (2026-09-07 continuation): a Fibonacci construction forces product-facet
  coefficient ratios exponential in a parameter while using only linearly many
  network arcs, simplex states and observed products. Capacities and total flow
  are one; the graph can be simple, planar, and maximum degree three. Independent
  proof audits and original-state witness checks passed. The number of states
  grows. Conversely, [fixed-state flat chains](results/network-simplex-flat-chain-fixed-states.md)
  admit an explicit original-variable separator and a state-count-only
  coefficient bound even with arbitrarily many cycles. With two observed
  labels, the [residual-eliminated manuscript version](paper-network-simplex/sections/07-fixed-state-chains.tex)
  needs only five profile tests after original-domain and zero-row checks; the
  note's earlier unreduced formulation uses 41 circuit tests. This positive
  theorem and the simple-graph negative extension both passed independent review.
- [Sparse network–simplex hull obstruction](results/network-simplex-universality.md):
  arbitrary rational polytopes arise as coordinate sections already with two
  simplex coordinates on four-layer networks. Even unit capacities and unit flow
  permit facet coefficients exceeding every polynomial bound in model size.
  Independently reviewed; this transfers classical transportation universality.
- [Cycle and theta network hulls](results/network-simplex-cycle-theta-hull.md):
  exact original-space hulls and constructive separation for networks assembled
  from those blocks, with arbitrary simplex dimension. Two independent audits
  passed; rational-arithmetic and output-size limits are explicit.
  The reviewed [parallel-path extension](results/network-simplex-parallel-path-hull.md)
  permits arbitrarily many internally disjoint paths per block, with exact
  transportation cuts and polynomial max-flow separation.
- [Coordinate dependence of disjunctive epigraph relaxations](notes/common-factor-p-split-rotation-gap.md):
  a rational two-ball family has unbounded error even with the tightest convex
  hull in its chosen auxiliary function space. A fixed rational orthogonal
  coordinate change makes that construction exact. The entire retained domain
  is transformed, and all proof sections passed independent audit.
  A separate [published P-split theorem counterexample](notes/common-factor-p-split-correction.md)
  and [exact ball-relaxation formula](notes/common-factor-p-split-balls.md) are retained.
- [Scaling disjunctions](results/scaling-disjunctions-hull.md):
  corrected hull results and an exact characterization of universal cost separation.
  Original cost-separation claim was false; counterexamples are retained. Replacements
  independently reviewed; core results overlap known literature.
- [Point-packing relaxations](results/point-packing-relaxations-anstreicher-conjecture-4.md):
  corrected proofs of known formulas. The conjectures were already resolved by
  Khajavirad (2024); this is a rediscovery, not a novelty claim.
- [Generalized-power obstruction](notes/generalized-monomial-gap-obstruction.md):
  two positive one-variable terms already have an unbounded termwise gap ratio.
  This reviewed scope counterexample concerns the original variables; logarithmic
  reparameterization removes this particular obstruction. No novelty claim.

## Repository layout

- `results/`: statements, proofs, scope, sources, and verification status.
- `notes/`: independent audits, research directions, negative findings, and [research log](notes/log.md).
- `code/`: verification scripts; some require the `minlp-notes` conda environment.
- `literature/`: local paper knowledge base; see its `README.md` and `AGENTS.md`.
  This directory is excluded from version control.

Exploratory notes retain failed approaches and open conjectures. Consult each
file's final status; they are not all claims of verified new contributions.

The [exact aggregation hull package](formal/topics/30-infinite-aggregation-hull/README.md)
now verifies the strict and closed hull formulas, finite SDP lifts, and
weak-system hull equality, with a direct two-point proof already in four
variables. The [accuracy package](formal/topics/31-aggregation-accuracy/README.md)
also verifies the explicit Euclidean Hausdorff bounds, optimal inverse-square
rate, exact rational cut constructions and logarithmic coefficient sizes.
These two follow-ups add 25 modules and 325 audited declarations, with
independent reviews and successful targeted builds and kernel replays.
