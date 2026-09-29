# Research continuation: September 27, 2026

Research resumed under an open-ended instruction. On September 28, the
user requested completion of the current directions without starting new
ones. That work is now finished; the
[closing record](closing-research-results.md) summarizes the final results,
reviews, corrections, and limits. No result in this batch is currently
designated publication-ready. The [Hessian-span synthesis](hessian-span-main-results.md)
is the entry point for the quadratic structural theorem package, its dependencies,
precise outputs, and prior-work distinctions.

A stronger reviewed [exact-decision classification](exact-convex-quartic-complexity.md)
combines a [lower bound](unconstrained-quartic-posslp-reduction.md) and
a [general upper bound](strong-convex-quartic-posslp-upper.md): exact
unconstrained minimum and minimizer-coordinate order comparisons are
PosSLP-complete for rational quartics with a supplied positive definite
rational Hessian Gram. Equality has a one-PosSLP upper bound; a matching
equality lower bound is not claimed. The lower construction's
full rational Hessian Gram is supplied and is at least the identity.
Every constructed optimum is strictly positive or strictly negative.
The positive branch has a rational positive definite polynomial Gram;
after reversing the integer comparison, the construction also proves
PosSLP-hardness of rational SOS membership, real SOS membership, and
global nonnegativity under the supplied curvature certificate. The
upper bound gives completeness for the latter two, and for existence
of a rational positive definite polynomial Gram. Rational SOS with
singular Grams remains distinct at a zero minimum.
The [fresh proof review](posslp-unconstrained-quartic-adversarial-review.md)
checks the quantitative perturbation and its consequences. The
[independent upper review](strong-convex-quartic-posslp-upper-independent-review.md)
checks real algebraic separation, Newton circuits, and all zero cases.
The [upper prior audit](strong-convex-quartic-posslp-upper-prior.md)
credits established many-one Newton reductions for probabilistic
polynomial systems. The
[primary comparison](posslp-convex-quartic-prior.md) credits established
SDP and SOCP hardness and qualifies publication priority. No claim that
PosSLP is NP-hard or outside polynomial time is made.

The reviewed [rational-optimizer strengthening](rational-optimizer-posslp-coordinate-comparison.md)
shows that coordinate comparison stays PosSLP-complete when the optimizer
is promised rational and bounded, the minimum is known to be zero, and
short rational square factors are supplied. A
[quaternion sign compiler](quaternion-circuit-posslp-reduction.md)
and [quartic realization](unit-quaternion-circuit-quartic-realization.md)
provide the lower reduction. Two fresh compiler reviews and a separate
realization review passed; the root checked their composition.
The [independent prior audit](quaternion-circuit-posslp-prior-review.md)
credits existing matrix-circuit and commutator methods, including prior
shared computation. This strengthening concerns coordinates; rationality
of the optimizer after a minimum-value perturbation is not claimed.

A reviewed [monotone-map extension](strong-monotone-cubic-posslp-upper.md)
gives the same one-instance upper bound for degree-four polynomial
observables at the unique zero of a globally strongly monotone cubic
map. The map need not be a gradient; an explicit example has a
nonconstant skew part in its Jacobian. Rational ellipsoid initialization
and nonsymmetric Newton steps supply the construction. These are
established algorithmic tools; the note identifies their exact
arithmetic consequence and qualifies priority.
For quartics on arbitrary rational polyhedra, a separate reviewed
[active-set theorem](polyhedral-strong-quartic-unambiguous-upper.md)
places exact value and coordinate comparisons in
\(\mathrm{UP}^{\mathrm{PosSLP}}\cap
\mathrm{coUP}^{\mathrm{PosSLP}}\). It checks the unique full active
set using rational LP with a circuit objective, including degenerate
polyhedra. It does not find that set in deterministic polynomial oracle
time. A [supplied inactive-slack gap](polyhedral-strong-quartic-active-gap.md)
does permit a deterministic one-instance reduction; the gap's encoding
length is part of that promise.

The reduction uses a reviewed
[simulation by bounded cubic-root circuits](posslp-certified-cubic-root-reduction.md)
whose raw radicands contain only rational affine combinations of earlier
roots and their individual squares. Explicit rational boxes certify
every gate. A matching reviewed [upper bound](posslp-certified-cubic-root-upper.md)
uses classical algebraic separation and Newton approximation to reduce
comparison in that particular circuit language to one PosSLP instance.
Thus the specified root-comparison language is PosSLP-complete. The
lower construction also gives a rational SOS quartic on a fixed unit
cube whose minimum is zero or positive according to the input answer.
The general upper bound additionally constructs a polynomial-size
shared rational arithmetic-circuit feasible point whenever the
unconstrained zero sublevel is strictly feasible. Expanded rational
coordinate size can nevertheless be very large.

A reviewed [fixed-parameter candidate-list theorem](fixed-integer-strong-quartic-fpt.md)
separates integer search from exact value comparison. For a globally
strongly convex quartic with unrestricted continuous fibers and a
rational polyhedron on \(k\) integer variables, ordinary computation
constructs a list containing every optimal integer block in
\(2^{O(k\log(k+1))}L^C\) time, with absolute \(C\).
Nonadaptive PosSLP comparisons then select all optimal blocks; there
are at most \(2^k\). The continuous dimension is unrestricted.
The [fresh review](fixed-integer-strong-quartic-fpt-independent-review.md)
checks the all-optima statement, source contracts, and uniform bit
bounds. The integer-query method is established prior. The contribution
is its coarse rational-cut implementation for quartic fibers and its
separation from exact arithmetic. This does not subsume established
ordinary FPT algorithms for convex mixed-integer quadratic programming,
which allow broader constraints and do not need strong curvature.

The reviewed [mixed-linear extension](mixed-linear-strong-quartic-candidate-list.md)
allows arbitrary coupled constraints \(Az+By\le c\). It constructs
the all-optima integer list in ordinary \(a(k)L^C\) time using
approximate primal-dual cuts, without a Slater condition or multiplier
norm bound. A separate reviewed
[constraint-rank algorithm](constraint-rank-strong-monotone-oracle.md)
uses classical violator-space sampling for exact continuous observables.
Their reviewed [composition](mixed-quartic-integer-constraint-rank-oracle.md)
gives expected \(F(k,\operatorname{rank}B)L^C\) exact optimization
with a PosSLP oracle, unrestricted continuous dimension, and absolute
input-length exponent. The algorithm is Las Vegas and returns an
implicit continuous optimizer; expanded algebraic output is not promised.
The rank parameter concerns all continuous constraint normals.

A separate reviewed [rational-witness theorem](strict-convex-quartic-rational-witness-lower-bound.md)
constructs a polynomial-size quartic in \(n=2k\) variables with a
full rational Hessian Gram at least the identity. Its zero sublevel
set is compact, has nonempty interior, and lies in \((-1,5)^n\),
yet every rational feasible point needs \(\Omega(n2^{n/2})\)
denominator bits in its first coordinate. A short root circuit and
quadratic perturbation localize the whole set near a cubic irrational.
The [fresh review](strict-quartic-rational-witness-independent-review.md)
checks the universal localization and integer-numerator bound. The
[prior comparison](strict-convex-quartic-witness-prior.md) credits
established large-witness convex systems and the general exponential
rational-sampling upper bound. The obstruction is superpolynomial in
the constructed total input length; it does not imply nonmembership
in NP or exclude succinct arithmetic-circuit witnesses. Priority for
the combined curvature and boundedness restrictions remains unestablished.

A reviewed [rational-minimizer construction](rational-convex-quartic-minimizer-height.md)
strengthens the exact-output obstruction in a different direction.
Repeated squaring on a rational unit circle gives a unique rational
minimizer in \([-1,1]^N\) whose terminal denominators have
\(2^{\Omega(N)}\) bits. A polynomial-size strongly SOS-convex
quartic realizes that point and has short rational square factors and
a short full positive definite Hessian Gram. Thus rationality and a
bounded minimizer do not ensure short exact output. The
[certificate consequence](rational-circle-optimal-gram-height.md)
forces long entries in every maximal-rank optimal Gram and every
nonzero rational matrix exposing the optimal Gram face, although a
short lower-rank optimal Gram is supplied. The moment optimum is unique
and also has long entries. The [prior comparison](rational-minimizer-height-prior.md)
credits existing optimizer-height obstructions and exact algorithms
that assume a rational-height bound. Generic SDP examples already
separate short feasible matrices from long maximal-rank matrices;
the restricted quartic realization is the additional feature here.
A reviewed [local-conditioning refinement](rational-circle-minimizer-local-conditioning.md)
keeps the optimizer's Euclidean norm bounded and gives its Hessian a
polynomial condition number, while preserving the long rational
denominators. This is a statement at the exact minimizer; it supplies
no uniform smoothness bound on a fixed neighborhood.

Reviewed [interior-Gram lower](interior-gram-bit-lower-bound.md) and
[upper](interior-gram-single-exponential-upper.md) bounds distinguish
strict SOS certification from general SOS certification. Under a
supplied full positive definite rational Hessian Gram, strict positivity
guarantees a rational positive definite polynomial Gram of size
\(\operatorname{poly}(L)2^{O(n)}\). Some polynomial-size inputs
require \(\Omega(n2^{n/2})\) denominator bits in every interior
Gram, even though they have short singular rational Grams and short
rational SOS certificates. The upper uses established open-set rational
sampling and Taylor SOS integration; the lower uses a tiny positive
value and determinant arithmetic. Separate fresh reviews and a full
root read checked both proofs. The [literature audit](gram-bit-size-prior.md)
credits existing Gram compactness and precision-dependent exact SOS
algorithms. An all-PSD certificate lower bound remains unresolved.

Reviewed [block-separation](rational-block-sos-splitting-obstruction.md)
and [strong-convexity](strongly-sos-convex-block-splitting-obstruction.md)
theorems identify a different, proved certificate cost. A strongly
SOS-convex rational quartic can have a short joint rational SOS but no
rational SOS respecting a prescribed two-block variable partition.
After a positive perturbation, rational block certificates exist, yet
every pair of local rational PSD Grams needs an exponentially long
entry; every explicit separated SOS has exponential total coefficient
length. The unrestricted certificate remains short. Real block
certificates exist throughout. The [prior audit](rational-block-sos-splitting-prior.md)
distinguishes this arithmetic obstruction from established real sparse
relaxation gaps. Fresh review corrected one input specification: the
padding construction counts its supplied baseline SOS certificate.
The concrete application already provides it.

The reviewed [quadratic-graph realization](quadratic-graph-quartic-realization.md)
also completes the growing-field extension. Given a zero-minimum quartic
with a supplied full positive definite rational Hessian Gram, it constructs
in polynomial time a rational SOS quartic whose unique zero records the
original optimizer and all its quadratic products. The output has a short
full positive definite rational Hessian Gram. Applying this construction
to the block lift makes both blocks strongly SOS-convex while preserving
the least separated coefficient field \(\mathbb Q(2^{1/5^k})\).
The resulting degree bound is exponential in the square root of the total
variable count. Every positive semidefinite joint Hessian Gram is singular
on the full joint basis because of additive block separation.

A reviewed [integer quartic in two variables](convex-quartic-irrational-zero.md)
has a globally positive definite Hessian and minimum zero at the unique
point \((\sqrt[3]{2},\sqrt[3]{4})\). Thus even one strongly convex
quartic inequality can have no rational feasible point. This gives a
negative answer to the rational-witness possibility left unresolved in
Table 1 of the inspected November 2025 arXiv version of
Slot--Steurer--Wiedmer's manuscript.
The [fresh review](convex-quartic-irrational-zero-review.md) and
[root audit](convex-quartic-root-audit.md) independently check the global
bound \(\nabla^2F\succeq4124I\), exact identities, and the source's
scope. It is neither a hardness result for exact decision nor an
obstruction to algebraic certificates. A separate
[rational SOS certificate](convex-quartic-rational-sos.md) proves the
slightly weaker bound \(4096I\). The
[Lean verification](convex-quartic-lean-verification.md) now checks the
actual directional derivative bound, global convexity, the unique real
zero, and the absence of rational feasible points. The stronger analytic
constant \(4124\) is outside that formalization. The
[publication assessment](convex-quartic-publication-assessment.md)
compares the closest constructions and records that the STOC 2026
proceedings text remains uninspected. Publication priority is unestablished.

A reviewed [general realization theorem](general-strongly-convex-quartic-singleton.md)
shows that a real algebraic number occurs as a coordinate of such a
rational strongly convex quartic singleton exactly when it has one real
conjugate. The construction is polynomial time in the dense minimal
polynomial's encoding and produces a rational sum of squares. A further
[SOS-convexity theorem](sos-convex-quartic-realization.md) supplies a
positive definite rational Gram matrix for its Hessian, with polynomial
encoding length. Thus a short exact convexity certificate can coexist
with arbitrarily high algebraic degree of the unique feasible point.
The root read both full proofs and their quantitative construction
dependency; fresh independent reviews found no remaining gap. The
interpolation, Gram projection, and regularization techniques have close
prior results, which the publication assessment explicitly credits.
A [smaller realization](dimension-optimal-quartic-realization.md) uses
\((d+1)/2\) variables for degree \(d\), with the same quantitative
guarantees. This count is optimal for the prescribed consecutive-power
coordinates, not for arbitrary embeddings of the field. Its fresh
review and the root's independent reconstruction found no gap.

A reviewed [cyclic family](cyclic-quartic-exponential-degree.md) gives
much larger degree per variable: the unique zero of one integer quartic
in \(n\) variables has field degree
\((2^{n+1}-(-1)^{n+1})/3\). Its coefficients have
\(O(\log(n+1))\) bits, its support has \(O(n^2)\) terms, and it
has a rational positive definite Hessian Gram certificate. Its Hessian
at the zero has polynomially bounded condition number. A reviewed
[rational square compression](cyclic-quartic-square-compression.md)
reduces the construction to \(n+1\) integer quadratic squares.
The reviewed [SOS-length theorem](convex-quartic-minimal-sos-length.md)
proves that this is the minimum number even over real coefficients:
every globally convex quartic with a zero and positive definite Hessian
there needs at least \(n+1\) squares. Its proof uses a convex reduction
of flat leading directions and classical topological degree.
An affine coordinate translation forces exponential dense and ordinary
sparse minimal-polynomial output; succinct root expressions remain
possible. The graph determinant and binomial-system ingredients are
classical, and priority for their convex quartic assembly is unestablished.
A separate [binomial-network bound](cyclic-quartic-noncirculant-search.md)
proves that this degree is optimal within the minimum-size binomial
exposing construction, using classical interlace identities. Improving
the degree through that method requires a broader class of equations.

Separate [degree bounds](quartic-zero-degree-adversarial.md) give
at most \(2^n-1\) for rational SOS quartics with an isolated unique
real zero and positive definite Hessian there. Global convexity improves
this to \(2^n-3\) for \(n\ge3\) and \(2^n-5\) for \(n\ge4\).
The cyclic family therefore attains the exact maxima three, five,
and eleven in dimensions two, three, and four in this class.
A reviewed [five-variable continuation](five-variable-positive-base-bound.md)
now proves the sharp maximum twenty-one as well. It handles
nonreduced residual schemes and possible complex base components;
the [root review](five-variable-degree-root-review.md) checks both
parts and their classical dependencies.
The proofs use classical Cayley--Bacharach and additional control of
positive-dimensional components and real points at infinity.
These bounds require rational SOS; they are not asserted for every
convex quartic.

A reviewed [three-variable integer quartic](ternary-rational-sos-convex-counterexample.md)
has \(\nabla^2F\succeq I\), a rational positive definite Hessian Gram,
and minimum zero, but no rational polynomial SOS. It has just 31
monomials, with coefficients of magnitude at most 448. For every real
field \(E\), an SOS or positive semidefinite Gram over \(E\) exists
exactly when \(2^{1/5}\in E\). Three is the smallest affine dimension
under this strict Hessian Gram assumption. Every positive rational
constant perturbation has rational SOS, so rational SOS lower bounds
approach the attained optimum without certifying it exactly.
The [root audit](rational-sos-convex-descent-root-audit.md) supplements
two independent reviews and the primary-literature comparison.
The earlier [four-variable construction](rational-sos-convex-descent.md)
is retained for its different linear obstruction. These claims concern
polynomial SOS certificates. A separate
[Lean certificate](ternary-sos-descent-lean-verification.md) checks the
actual second derivative bound and the zero identity, conditional on
\(a^5=2\); it does not formalize the coefficient-field obstruction.
A reviewed [quadratic multiplier](rational-denominator-certificate-frontier.md)
gives rational-function squares with an everywhere-positive common
denominator of minimum degree two. Nevertheless, a reviewed
[scaling theorem](rational-radial-exponent-obstruction.md) forces the
least rational SOS multiplier order for \(1+\|x\|^2\) to tend to
infinity. The Hessian at the minimizer stays unchanged, and an
adapted quadratic denominator still has a short certificate. This
is an arithmetic obstruction to a prescribed hierarchy, not to
real SOS or numerical optimization. An
[exact recursive separator](rational-radial-quantitative-separation.md)
and its reviewed [height bound](rational-radial-height-lower-bound.md)
give the quantitative order lower bound
\(\Omega(\log L/\log\log L)\) in binary input length \(L\),
while an adapted certificate has size \(O(L)\).

A stronger reviewed [quintic-tower family](exponential-least-sos-field.md)
has polynomial-size rational input and a positive definite rational
Hessian Gram in \(3k\) variables, but its exact least SOS and PSD
Gram coefficient field is \(\mathbb Q(2^{1/5^k})\).
Every real coefficient field carrying either certificate must contain
this field. A separately checked Galois argument further forces one
individual algebraic coefficient to have degree at least \(5^k\).
Thus even separate dense minimal-polynomial output is necessarily
large; sparse, radical, and tower output remain outside the bound.
The [fresh review](exponential-least-sos-field-fresh-review.md) and
[root audit](exponential-least-sos-field-root-audit.md) cover the
construction and its quantitative dependency. The
[primary-literature comparison](exponential-sos-field-prior.md)
distinguishes this from excluding one prescribed field and from
high-degree SDP optima. Priority remains unestablished. Rational-function
SOS certificates also have a constructive bound: after increasing the
rational scale, the reviewed
[quadratic-denominator theorem](rational-tower-quadratic-denominator.md)
gives a polynomial-size rational certificate with an everywhere-positive
common denominator of minimum degree two and numerators of degree at
most four. Its general multiplier lemma uses a positive quadratic
relation and an explicit ideal-membership identity; it is not a theorem
for all strongly SOS-convex quartics.

Two reviewed companions further delimit the output obstruction.
[Shared root circuits](tower-sos-coefficient-encoding.md) give
polynomial-size exact polynomial SOS certificates for the same tower.
[Retaining the root variables](tower-rational-auxiliary-certificate.md)
gives a polynomial-size rational SOS certificate modulo a solvable
quadratic system, of certificate degree four with two redundant
equations or degree five using only the root equations. These upper
bounds use established Taylor SOS theory and do not establish a new
general proof system or decision-complexity lower bound.

Two further reviewed structural notes describe the tower's entire
rational certificate space. Its [quadratic vanishing space](tower-quadratic-vanishing-space.md)
has exactly five basis relations per gate, and all their unordered
pair-products are independent. Its [stationary quartic space](tower-quartic-stationary-space.md)
is exactly the span of those products; its stationary cubic space is
zero. Thus rational SOS recognition for a quartic with this supplied
tower zero reduces in polynomial time to linear algebra and one PSD
test, with a unique rational PSD polynomial Gram when one exists.
This special recognition result does not decide real SOS, locate an
unknown zero, or establish a general MINLP speedup. Fresh reviews and
the root's complete proof reads found no remaining gap.

The reviewed [moment and Gram consequence](strict-hessian-moment-arithmetic.md)
shows that the full positive definite Hessian Gram gives a unique
rank-one optimal moment matrix. The optimizer field is exactly the
least field for maximal-rank optimal Grams and for nonzero exposing
matrices of the real optimal Gram face. At an irrational minimizer,
no rational exposing step preserves all real feasible Grams, although
one real step suffices. Exactness of SOS-convex moment relaxations and
conjugate-kernel restrictions are established prior; these are
arithmetic consequences with their scope explicitly separated.

A reviewed [univariate degree obstruction](univariate-convex-degree-lower-bound.md)
shows that some \(O(b)\)-bit cubic inputs require degree
\(2^{\Omega(b)}\) in every rational globally convex univariate
zero realization, even if arbitrarily many convex polynomial rows are
allowed. The same number has a polynomial-size two-variable convex
quartic realization. A separately reviewed
[compressed construction](compressed-univariate-convex-zero-realization.md)
also gives a short univariate arithmetic circuit, without claiming
short expanded polynomial or rational-value output. These results
distinguish degree, dimension, and output format rather than proving
an optimization hardness theorem.

The main results now include a [coefficient-sensitive bound for finite
mixed-integer convex semialgebraic values](unbounded-misocp-multiple-integer-frontier.md),
including unattained infima. It gives full exact affine MISOCP optimization
at fixed integer dimension and continuous squared-Hessian span. Under the
stronger common-range restriction, [full optimization is FPT](common-range-unbounded-optimization.md),
even with an arbitrary-rank convex quadratic objective excluded from the
parameter. These extensions have fresh independent proof reviews. Their
geometric and algebraic ingredients have substantial classical precedents;
the [dedicated value-theorem audit](generic-convex-mixed-value-prior.md)
separates those consequences from the proposed height bound. Priority
remains unestablished.

The [quasiconvex mixed-value extension](quasiconvex-mixed-value-frontier.md)
requires convex strict sublevels instead of a jointly convex epigraph.
Convexity of the weak optimal slice is separately needed for the small
optimal integer witness. This yields reviewed
[full affine-fractional optimization](common-range-fractional-frontier.md)
in FPT time under the common-range restriction, including attainment and
exact algebraic output. A maximum of ratios additionally depends on the
rank of denominator gradients in the otherwise linear directions.
A shared reciprocal cone lift also covers explicitly positive
denominator domains. These conclusions concern exact structural
complexity; practical improvements are not established.
A further reviewed [quadratic-fractional theorem](common-range-quadratic-fractional.md)
permits one arbitrary-rank PSD quadratic numerator, excluded from the
native common-range parameter. It supplies the same full exact FPT
classification and output. The continuous polyhedral exact-value and
attainment case has a strong predecessor in Chandrasekaran--Tamir (1984);
the proposed addition concerns the mixed-integer and native nonlinear
constraint structure. Its three fresh reviews and the root's full read
found no remaining gap in the stated composition.
The [shared-curvature maximum extension](common-range-shared-curvature-fractional.md)
allows many ratios whose numerator Hessians are strictly positive
multiples of one unrestricted PSD matrix. It is FPT in integer
dimension, native range, and denominator-gradient rank. The root
provided the fresh full value and algorithm review; the canonical
field argument has a separate review. A reviewed
[nonnegative-weight extension](nonnegative-shared-curvature-fractional.md)
also permits zero curvature multipliers, including affine objective
floors. It changes the selected optimizer and uses a separately
reviewed [exact number-field QP algorithm](number-field-psd-qp-review.md).
The root read the full extension and supporting algorithm. The
recorded counterexamples still exclude extending the old
minimum-norm selector unchanged.

The quadratic foundation is a [value-degree and separation bound for
convex quadratics with a small Hessian span](hessian-span-reduction.md).
It gives [polynomial-time exact feasibility at fixed span dimension](hessian-span-exact-feasibility.md),
including degenerate feasible sets. A
[minimum-norm radius theorem](unbounded-hessian-span.md) removes continuous
input bounds, and [algebraic witness recovery](algebraic-witness-recovery.md)
constructs an exactly feasible point as coordinate minimal polynomials and
isolating intervals. These results have independent reviews. A
[source comparison](hessian-span-prior.md)
distinguishes this parameter from the number of constraints, matrix rank,
and generic algebraic-degree bounds. The resulting
[compact rational MILP](mixed-integer-span-frontier.md) preserves exactly
all feasible integer assignments, without adding integer variables. It
gives exact feasibility and optimal integer assignment for fixed integer
dimension and fixed continuous Hessian span. A
[fresh package assessment](hessian-package-assessment.md) found no proof
gap, identified an important integer-preserving approximation precedent,
and narrowed the proposed contribution to the uniform continuous-fiber
gap. An [audit under alternative terminology](hessian-span-alternate-terminology-audit.md)
compares quadratic maps, small SDP descriptions, simultaneous
diagonalization, and classical algebraic optimization. Priority remains
unestablished; useful numerical precision bounds and practical formulation
size remain open. The [unbounded integer theorem](unbounded-integer-frontier.md)
now gives exact feasibility and integer-only convex quadratic optimization
for fixed integer dimension and continuous Hessian span. The
[continuous optimizer theorem](exact-convex-optimizer-recovery.md) returns
an exact algebraic optimum and optimizer without input bounds. The
[full mixed-integer optimization theorem](mixed-integer-attainment-frontier.md)
now extends this to jointly convex quadratic objectives involving both
variable types, for fixed integer dimension and continuous Hessian span.
Its independent review checks recession elimination, the algebraic value
bound, and a bounded optimal assignment in the original coordinates.
An [explicit elimination refinement](explicit-span-separation.md) tracks
coefficient size directly. [Ordered perturbations](ordered-perturbation-optimizer.md)
give the canonical optimizer coordinate coefficient bounds
`N^O(h+1)`. A [sharp degree theorem](multihomogeneous-span-degree.md) bounds
that field and the value by `max_{s<=min(h,n)} 2^s binom(n,s)`.
[Rational strictly convex instances](multihomogeneous-degree-sharpness.md)
attain the bound. Fixing an optimal integer assignment gives the same
degree bound regardless of integer dimension; the height bound still
depends on the assignment's bit length.
[Small-input families](sharp-degree-effective-hilbert-audit.md) show that
the degree can grow as `n^Omega(h)` even when the input has polynomial
length. A [direct arithmetic construction](short-input-qcqp-degree-lower-bound.md)
makes its coefficients computable and keeps every constraint Hessian
positive definite. These are unconditional obstructions to an FPT algorithm
that writes a dense minimal polynomial, not to decision or succinct output.
A [refinement of the output obstruction](sparse-algebraic-output-boundary.md)
also covers ordinary sparse minimal-polynomial lists and separate
coordinate minimal polynomials. Circuit, tower, and shifted-basis output
remain outside that obstruction.
The [common-field recovery algorithm](constructive-common-field-recovery.md)
now returns one primitive real algebraic number and rational polynomials for
all coordinates. [Optimality certificates](algebraic-primal-dual-certificates.md)
use that field and at most `h` curved reductions before a final KKT identity.
[Infeasibility certificates](rational-infeasibility-certificates.md) can be
entirely rational, with total length `N^O(h+1)`. These are supporting
output and verification results, not new general certificate mechanisms.

A [sharp metric error bound](hessian-span-holder-geometry.md) gives exponent
`2^-h` on bounded regions without strict feasibility. For rational boxed
systems, a [separately reviewed arithmetic proof](hessian-span-holder-height-review.md)
bounds the logarithm of its constant by `N^O(h+1)`, using a
[direct number-field precision refinement](algebraic-coefficient-span-precision.md).
The argument keeps
all facial reductions in the number field of one canonical feasible point.
The [source comparison](hessian-span-holder-prior.md) and a
[full Shor-lift derivation](hessian-span-holder-hu-li-comparison.md) identify
the qualitative exponent as a modest structural corollary of established
conic error bounds. The arithmetic estimate is a separate contribution.
Reviewed [consequences](hessian-span-holder-consequences.md) give exact
penalties with `h` squaring equations and MILP outer models with a prescribed
distance to feasibility in each integer slice. Access to some original
sources remains unresolved.

A reviewed [polynomial escape construction](succinct-unboundedness-curves.md)
provides a short circuit with integer polynomial increments when an
unbounded problem has no decreasing straight ray. Together with an exact
anchor it gives a checkable unboundedness certificate. The underlying
conditional boundedness algorithm and continuous/integer equivalence are
already established by Obuchowska (2008); the proposed addition is the
explicit circuit and its local checks.

A [nonconvex extension](nonconvex-hessian-span-frontier.md) bounds the size
of an exact algebraic feasible-point certificate by `N^O(h+1)`, without
input bounds or positive semidefinite Hessians. Exact feasibility is
therefore in NP at fixed span; it is already NP-hard at span one. A supplied
box also gives this size bound for a global optimum and some optimizer,
without supplying a certificate of global optimality. Two proof reviews
found no gap, including a [separately staffed adversarial review](nonconvex-hessian-span-adversarial.md).
The [subsequent source audit](nonconvex-hessian-span-prior-audit.md) derives
the feasibility certificate and radius bounds more simply from established
component sampling on a suitable polyhedral face. Those conclusions are
therefore positioned as structural corollaries. The separate value proof
keeps every affine inequality, perturbs a lifted system of `h` quadratic
equations, and controls the algebraic limits of regular KKT points.
A reviewed [finite-infimum extension](nonconvex-finite-infimum.md) removes
the box for the value bound, including when the infimum is unattained.
For fixed span, exact infeasibility, unboundedness, and finite-value
classification and recovery are possible with an NP oracle. This gives no
polynomial-time global optimization algorithm without that oracle.
A reviewed [attainment and optimizer theorem](nonconvex-attainment-and-optimizer.md)
completes this classification and returns an exact minimum-norm global
optimizer when one exists. Its proof removes an unknown box before
coefficient elimination; the box size never enters the equations. Attainment
is already NP-hard with one quadratic inequality and a supplied infimum
of zero. The notes separate the sharp encoding bound from weaker optimizer
certificates obtainable through established sampling results.

A reviewed [general second-order cone extension](socp-hessian-span-frontier.md)
gives exact feasibility in polynomial time at fixed span of the squared
constraint Hessians, which may be indefinite. With bounded integer variables,
a rational MILP preserves exactly their feasible assignments. A separate
[projection argument](unbounded-misocp-frontier.md) removes all input bounds
for exact mixed-integer feasibility when the integer dimension is also fixed.
An [algebraic recovery procedure](socp-exact-witness-recovery.md) returns
an exactly feasible continuous point after the integer assignment is fixed.
The [prior-art audit](socp-hessian-span-prior.md) credits rational cone lifts,
classical integer optimization, and older one-cone consequences. Priority
for the broader structural class remains unestablished. These feasibility
results do not transfer the earlier attainment or unboundedness conclusions
to general cones.
A separate [continuous SOCP optimization theorem](continuous-socp-optimization.md)
now gives exact affine values, attainment decisions, and canonical algebraic
optimizers at fixed squared-Hessian span. It uses the new general optimizer
bound and rational queries on compact sets. For an
[integer-only convex quadratic objective](integer-objective-misocp.md),
the unbounded mixed-integer model also permits full exact optimization at
fixed integer dimension and continuous squared-Hessian span; discreteness
ensures attainment whenever its value is finite.
A reviewed [bounded-integer extension](boxed-misocp-optimization.md)
also permits affine objectives involving continuous variables, with exact
value, attainment status, and optimizer output. It is polynomial time at
fixed integer dimension and continuous Hessian span, and belongs to
`FP^NP` at fixed span when the integer dimension varies. Supplied finite
integer bounds are essential to that proof.
A separate [one-integer theorem](unbounded-misocp-value-frontier.md)
removes that bound when there is one integer variable. It covers the same
four status outcomes and exact output. Its value-size argument also applies
to arbitrary nonconvex quadratic systems with one integer variable, giving
`FP^NP` at fixed continuous Hessian span. The proof controls algebraic
branches at infinity; it does not replace integer optimization by the
continuous relaxation.
A [several-integer extension](unbounded-misocp-multiple-integer-frontier.md)
now gives full exact affine MISOCP optimization for fixed integer dimension
and continuous squared-Hessian span, with no supplied bounds. Its general
convex semialgebraic theorem controls finite values by rational affine
lattice restrictions, including when integer assignments escape to infinity.
The [fresh adversarial review](unbounded-misocp-multiple-integer-adversarial.md)
and [independent height audit](bounded-forms-height-independent-audit.md)
check the geometry and linear dependence on coefficient bit length.
The qualitative slice argument already implies algebraicity and a degree
bound; controlling the slice coefficients supplies the additional height
bound. The nonconvex one-integer extension is separate and does not follow
from this convex argument.
A reviewed [common-field extension](algebraic-threshold-misocp.md)
also permits exactly represented algebraic cone coefficients and objective
thresholds at fixed integer dimension and squared-Hessian span. All
coefficients must be supplied in one explicitly represented real number
field. The final decision problem is a rational MILP.

A reviewed [common-range theorem](common-range-fpt-frontier.md) gives
true fixed-parameter exact feasibility: `f(k,r) N^C` with an absolute
input exponent. It covers native PSD quadratics and SOC representations,
without Slater or supplied bounds. For unbounded mixed-integer SOC systems,
the parameter must also count continuous directions participating in
integer-continuous quadratic terms. Bounded common range is a narrower
class than bounded matrix span; the improvement is the uniform polynomial
exponent. The [source audit](common-range-fpt-prior.md) credits the
classical projection, algebraic radius, and integer optimization inputs.
The separate [witness recovery theorem](common-range-witness-recovery.md)
returns an original feasible algebraic point in the same FPT regime,
with common-field degree `2^O(r)`. Its
[fresh adversarial review](common-range-witness-adversarial.md) is recorded
separately from the earlier review that contributed a proof simplification.
A reviewed [optimization extension](common-range-optimization.md) excludes
an arbitrary-rank PSD objective Hessian from the common-range parameter.
Constant-matrix parametric QP charts reduce its arithmetic bounds to
quartic expressions in the retained nonlinear coordinates. The
[unbounded-integer composition](common-range-unbounded-optimization.md)
then gives FPT exact values, attainment decisions, and complete optimal
points using the general convex semialgebraic value theorem. It handles
finite nonattainment as well as unboundedness. The
[prior comparison](common-range-optimization-prior.md) credits classical
QP charts and the existing FPT quadratic and integer algorithms; the
candidate addition is their exact structural extension.

A reviewed [convex-polynomial feasibility extension](polynomial-nonlinear-dimension-frontier.md)
gives FPT exact feasibility in integer dimension, nonlinear continuous
dimension, and polynomial degree. It permits arbitrarily many linear
continuous variables, and assumes no bounds or strict feasibility.
A controlled relaxation and a grid in only the nonlinear coordinates
reduce the task to an implicit polynomial integer problem. An LP returns
individual violated polynomials without enumerating the projection.
The [oracle audit](polynomial-nonlinear-dimension-oracle-audit.md) and
[full review](polynomial-nonlinear-dimension-review.md) check strict
inequalities, rational shallow cuts, and coefficient growth through
lattice recursion. The [completed optimization theorem](polynomial-nonlinear-dimension-optimization.md)
returns the exact value and full optimal point with the same FPT bound,
including the objective in the nonlinear core. Its common-field degree
depends only on nonlinear continuous dimension and degree; the integer
dimension also affects time and height. Classical finite attainment is
credited to Bank--Mandel. The [fresh full review](polynomial-nonlinear-dimension-optimization-review.md)
checks the uniform canonical-point box and exact recovery.
A reviewed [globally quasiconvex extension](quasiconvex-polynomial-nonlinear-dimension-frontier.md)
gives the same full exact FPT conclusion. A row that depends affinely
and nontrivially on the eliminated variables must already be convex;
only independent rows require quasiconvex separation. The proof uses
classical quasiconvex integer methods and finite attainment, with fresh
reviews of its implicit projection, oracle, and arithmetic composition.
It is positioned as an extension, with no separate major novelty claim.

Three reviewed boundaries clarify these conclusions. A
[native convex quadratic system](convex-qcqp-rationality-boundary.md) can
have a single irrational feasible point and require irrational exposing
multipliers. A [convexity promise alone](convex-representation-boundary.md)
cannot replace the supplied convex representation in a general polynomial
algorithm unless `RP = NP`. Finally, [rational cone examples](socp-unboundedness-boundaries.md)
separate continuous from integer unboundedness and rule out polynomial
integer escape curves in a strictly feasible unbounded strip. These are
supporting scope boundaries with their prior antecedents recorded.
The irrational native PSD example has span three. A reviewed
[rationality theorem for span at most two](two-span-rationality-frontier.md)
proves polynomial-size rational witnesses, dense rational feasible points,
and rational affine hulls. It makes this native PSD threshold sharp;
publication priority remains unestablished.
A reviewed [constructive refinement](two-span-rational-output.md) returns
a rational feasible point at span at most two in polynomial time. It
detects the relevant affine face and uses either controlled rounding with
a strict margin or the rational tangency multiplier. This differs from
rounding an arbitrary algebraic boundary point.
A [general three-ellipsoid construction](few-quadratic-unbounded-degree.md)
now shows that span three can force arbitrarily large feasible-point
degree. Independent blocks give an unconditional obstruction to FPT
feasible output in dense or ordinary sparse minimal-polynomial formats.
The construction realizes every algebraic number with exactly one real
conjugate as a coordinate of a rational three-ellipsoid singleton.
The converse holds for singletons defined by rational convex polynomial
inequalities. Its [source comparison](singleton-field-characterization-prior.md)
credits prior irrational singletons, root-interpolation constructions,
and spectrahedral representations; equivalence to earlier results is
not ruled out.

An [exact moment-order separation on a quadratic path](structure-frontier.md)
requires order `2^(m-1)` in its edge decomposition, while width-two bags
give an order-two proof. A perturbed version retains a constant gap with
distinct computations. [Proof review](chebyshev-proof-review.md) and
[source review](chebyshev-prior-review.md) narrow the contribution to its
quantitative threshold: qualitative sparse-versus-dense failures and the
quadrature mechanism are prior work. The underlying optimization instance
is easy, so this is a limit of a specified relaxation architecture.

An [exact SDP projection for continuous-center, binary-leaf stars](binary-leaf-star-hull.md)
gives an [exact projected moment hull on forests](binary-separator-forest-hull.md).
A stronger [objective theorem](stable-positive-submodular-exactness.md)
makes PSD plus upper RLT exact on arbitrary submodular interaction graphs
when the positive diagonal vertices form a stable set. It includes explicit
threshold rounding and a fixed-mean convex-closure identity. Independent
[forest](forest-hull-review.md) and
[upper-RLT](stable-positive-submodular-review.md) reviews found no gap.
Tractability of the latter objective class is established prior work;
the candidate contribution is the relaxation representation.
A [four-variable path counterexample](positive-pair-sdp-frontier.md)
rules out the natural extension allowing adjacent positive diagonal
vertices, even after all Boolean quadric cuts. It refines an existing
preprint example rather than introducing a new general gap mechanism.

Supporting results include:

- [Rank-sensitive metric error and norm-penalty bounds](penalty-frontier.md),
  including indefinite quadratic objectives under the stated native
  convexity and feasible-slice Slater assumptions.
- [Budgeted diagonal-plus-low-rank quadratic selection](positive-update-spectral-approximation.md),
  an approximation consequence of existing repository matrix-cover theory.
- [Approximation with few positive interactions](free-frontier.md), with
  explicit comparison to ordinary coordinate gridding.
- [A strict cube-quadratic extreme-ray classification](cube-strict-extreme-classification.md),
  which leaves boundary cases and full completeness unresolved.
- [Singular-equality certification limits](equality-frontier.md) and
  [succinct exact root penalties](succinct-root-penalties.md), both retained
  as supporting consequences with close established antecedents.

Several initial proposals duplicate prior work. The
[attractive-interaction source review](attractive-literature-review.md)
records one correction: arbitrary signed linear terms and sign-switchable
Stieltjes indicator quadratics already have a published polynomial
optimization theorem.

The [research log](root-research-log.md) records decisions, validation, and
remaining questions. Independent review here means review by another research
agent. It does not establish priority or replace external peer review. All
verification is targeted; project-wide checks and CI inspection are excluded.
