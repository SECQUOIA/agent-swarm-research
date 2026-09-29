# Exact optimization and error bounds from Hessian matrix span

Date: 2026-09-27. The principal results below have completed independent
proof reviews. Publication priority remains unestablished. Full proofs,
source comparisons and verification records are
in the linked notes; this file does not duplicate them.
Separate [initial](hessian-span-synthesis-review.md),
[degree-and-geometry](hessian-span-synthesis-degree-geometry-review.md), and
[common-field-and-certificate](hessian-span-synthesis-certificate-review.md)
scope reviews checked this synthesis against those notes.

The central candidate contribution is a structural precision theorem for
rational convex quadratic optimization. When the native constraint Hessians
span a fixed-dimensional space, finite optimal values and minimum-norm
optimizers have polynomial algebraic degree and coefficient bit length,
even with arbitrarily many variables and inequalities. This permits exact continuous
optimization and exact mixed-integer convex quadratic optimization for fixed
integer dimension, including algebraic optimal values and continuous
optimizers. Neither result requires input variable bounds. The theory also
gives explicit rational MILP formulations that preserve bounded integer assignments without adding
integer variables. No strict-feasibility assumption is needed.

The same parameter controls a sharp bounded-region Hölder error bound:
small constraint residual implies small distance to the feasible set, with
exponent \(2^{-h}\). For rational boxed data the constant has an effective
encoding bound. This connects exact precision to approximate solutions and
penalty formulations, including degenerate feasible sets.

These are exact Turing-model results. They do not establish a practical
speedup, a polynomial-time algorithm for unrestricted MINLP, or a new
general principle for converting approximations into exact integer models.

## 1. Model and parameter

For continuous problems, let

\[
 F=\{x\in\mathbb R^n:Ax\le b,\ Ex=e,\ q_i(x)\le0
                         \ (i=1,\ldots,m)\},
 \qquad q_i(x)=\tfrac12x^TQ_ix+a_i^Tx+c_i,
 \qquad Q_i\succeq0.
\]

All data are rational and explicitly encoded. Let \(N\ge2\) be their
total binary length, including any objective or supplied bounds, and put

\[
 h=\dim_{\mathbb Q}\operatorname{span}\{Q_1,\ldots,Q_m\}.
\]

For mixed-integer problems the variables are \((z,x)\), with
\(z\in\mathbb Z^k\). The analogous parameter counts only the continuous
blocks:

\[
 h=\dim_{\mathbb Q}\operatorname{span}
                  \{\nabla^2_{xx}q_i:i=1,\ldots,m\}.
\]

The mixed-integer formulation and unbounded-integer theorems require every
**full Hessian in \((z,x)\)** to be PSD. Merely convex continuous slices
do not suffice for those results. Arbitrary rational affine equations and
inequalities are allowed. Any objective is a rational convex quadratic;
in the mixed-integer theorem its full Hessian must be PSD too. The objective
Hessian is excluded from the constraint parameter \(h\).

The parameter is computable by rational matrix rank. It is neither the
number of rows, their aggregate rank, nor the span dimension of the complete
quadratic polynomials. For example, the rows
\(\|x\|^2+2x_i-1\) have \(h=1\), although their affine parts add
arbitrarily many independent polynomial directions. A full-rank Hessian can
also have \(h=1\). Throughout, “polynomial for fixed \(h\)” permits an
exponent depending on \(h\); no fixed-parameter-tractable running time
\(f(h,k)N^{O(1)}\) is claimed.

## 2. Principal results and exact outputs

“Reviewed” means that the linked proof received independent adversarial
review. It is evidence of correctness, not formal certification. Asymptotic
constants in the precision bounds are effective but have not been calibrated
for an implementation.

For the algebraic statements below, write
\[
 D(n,h)=\max_{0\le s\le\min(h,n)}2^s\binom ns,
 \qquad D(0,h)=1.
\]
The maximum matters: the expression need not increase with \(s\).
For example, \(D(3,3)=12\), attained at \(s=2\), whereas \(s=3\)
gives eight. The bound is at most \(3^n\) and is \(O(n^h)\) for fixed
\(h\).

| Result | Assumptions beyond Section 1 | Established output and complexity | Status and proof |
|---|---|---|---|
| Algebraic optimal-value bound | Nonempty continuous feasible set; convex quadratic objective with finite infimum; no input bounds | The infimum is attained. Its value has a primitive integer minimal polynomial of degree at most \(D(n,h)\) and coefficient bit length \(N^{O(h+1)}\). A nonzero value has magnitude at least \(2^{-N^{O(h+1)}}\). | Reviewed: [unbounded theorem](unbounded-value-optimization.md), [sharper degree bound](multihomogeneous-span-degree.md), [explicit height argument](explicit-span-separation.md). |
| Exact continuous optimization | Continuous model; arbitrary convex quadratic objective; no input bounds or Slater condition | Classify infeasibility or objective unboundedness; otherwise return the exact optimum and its minimum-norm optimizer in one explicitly constructed real number field: an isolated primitive generator and rational coordinate polynomials. The field degree is at most \(D(n,h)\), and representation coefficient bits are \(N^{O(h+1)}\). Coordinatewise minimal polynomials and isolators are also available. The established algorithm takes \(N^{\operatorname{poly}(h+1)}\) time. | Reviewed: [recovery algorithm](exact-convex-optimizer-recovery.md), [ordered optimizer and height](ordered-perturbation-optimizer.md), [common-field degree refinement](multihomogeneous-span-degree.md), [constructive common-field output](constructive-common-field-recovery.md). |
| Exact mixed-integer convex quadratic optimization | Jointly PSD constraint and objective Hessians; fixed \(k,h\); no input bounds or Slater condition | Classify infeasibility or objective unboundedness; otherwise return an optimal integer assignment, exact algebraic value and exact algebraic continuous optimizer in polynomial Turing time. Some optimal integer assignment has polynomial bit length, and the optimal value has polynomial degree and coefficient bits, for fixed \(k,h\). | Reviewed: [full optimization theorem](mixed-integer-attainment-frontier.md), [complexity review](mixed-integer-attainment-complexity-review.md); continuous output uses the reviewed optimizer theorem above. |
| Exact continuous feasibility and feasible-point recovery | No input bounds or Slater condition | Decide emptiness and otherwise return the unique minimum-norm feasible point, either coordinatewise or in one explicitly constructed real number field. The field degree is at most \(D(n,h)\), and coefficient bits are \(N^{O(h+1)}\); complete recovery is polynomial for fixed \(h\). | Reviewed: [radius](unbounded-hessian-span.md), [algebraic witness](algebraic-witness-recovery.md), [common-field construction](constructive-common-field-recovery.md). |
| Exact rational MILP integer projection | Joint convexity; explicit finite bounds on original integer variables; continuous variables may be unbounded | Construct a rational MILP with exactly the same feasible integer assignments and no additional integer variables. Its size and construction time are polynomial for fixed \(h\), even if \(k\) grows. | Reviewed: [boxed construction](mixed-integer-span-frontier.md), [removal of continuous bounds](unbounded-hessian-span.md). |
| Sharp Hölder error bound with controlled constant | Nonempty continuous feasible set; bounded trial region; real data allowed for the exponent, rational input box for the encoding bound | Distance to feasibility is at most \(C V^{2^{-h}}\), where \(V\) is maximum constraint violation. The exponent is uniformly sharp. For rational boxed data, \(\log_2\max(1,C)\le N^{O(h+1)}\), without Slater. | Reviewed: [geometry](hessian-span-holder-geometry.md), [direct number-field precision](algebraic-coefficient-span-precision.md), [precision review](algebraic-coefficient-span-review.md). |

The bounded-domain MILP construction has the sharper bound
\(N^{O(h+1)}\). Inserting the continuous radius conservatively gives
\(N^{O((h+1)^2)}\). Composing integer-witness bounds and subsequent
algorithms still gives polynomial time for fixed \(k,h\); the synthesis
does not assert an optimized exponent for that composition.

Exact outputs must be distinguished. A solution of the lifted MILP certifies
that its integer assignment has a nonempty original continuous fiber; its
displayed continuous coordinates can violate the original rows. The separate
algebraic recovery theorem returns an exactly feasible continuous point.
Rational output cannot be required in general: three convex quadratic
inequalities with rational data can have the singleton feasible set
\(\{(\sqrt[3]{2},\sqrt[3]{4})\}\), as proved in the
[value note](hessian-span-reduction.md). The reviewed common-field algorithm
now gives one selected real algebraic generator and a rational polynomial
for each coordinate. Substitution reduces every native affine or quadratic
sign check to exact univariate computation, without enumerating products of
coordinate degrees. This supplies efficiently checkable primal feasibility;
finite optimality certificates require the additional identities in Section 7.

For bounded integer variables, **slice convexity alone** does yield one
additional reviewed consequence: fixed-\(h\) feasibility belongs to NP,
because a polynomial-bit integer assignment can be checked by the continuous
decision algorithm. This does not imply the joint-convex MILP projection
theorem under the weaker hypothesis.

The [unbounded integer-witness theorem](unbounded-integer-frontier.md)
supplies the underlying feasibility bound
\(N^{O((h+1)(k+1)^4)}\) on the coordinate bits of some feasible integer
assignment. The full optimization theorem requires an additional argument
for a small **optimal** integer assignment. Its rational threshold queries
append the objective as a sublevel inequality, increasing \(h\) by at
most one. When the objective depends only on integer variables, the value
is rational and a [simpler discrete-value argument](integer-objective-review.md)
already suffices.

The degree bound \(D(n,h)\) also holds for the common field of the value
and the minimum-norm continuous optimizer in any optimal integer fiber of
an **attained** mixed-integer problem with convex continuous slices,
regardless of the number of integer variables: fix that assignment and
apply the continuous theorem with its \(n\) continuous variables.
This degree assertion does not give a
uniform height or running-time bound when \(k\) grows. The substituted
fiber's coefficient size depends on the assignment's bits; integer
repeated-squaring chains already have rational optima requiring exponentially
many bits.

The degree bound is [sharp for both the value and the joint optimizer field](multihomogeneous-degree-sharpness.md).
For every \(n\ge1\) and \(0\le h\le n(n+1)/2\), rational examples
attain \(D(n,h)\) with a positive definite objective, strict feasibility,
a compact feasible set and a unique optimizer. For \(h>0\), all native
quadratic constraint Hessians can be positive definite too. This is an
existence result, not an efficient construction of extremal coefficients
or a matching coefficient-height or running-time lower bound. The generic degree formula
and Hilbert irreducibility used for the convex rational specialization
are classical.

## 3. Why the precision theorem works

The proofs share one structural reduction; the consequences should not be
counted as independent discoveries of that reduction.

1. **Restrict at an optimizer.** Convexity permits deleting inactive rows
   while preserving the optimum: a better retained-feasible point would
   improve the original objective on a sufficiently short segment from the
   optimizer. Turn active affine rows into equations. For active quadratic
   rows, subtract their Hessian-basis combinations. These differences are
   affine and vanish at the optimizer. Imposing them makes the entire
   restricted quadratic polynomials span at most \(h\) dimensions.
2. **Compress stationarity.** Relax the remaining rows slightly and use a
   strongly convex objective. KKT multipliers exist for the relaxed problems.
   Their contribution depends on an \(h\)-dimensional coefficient vector,
   so conic Carathéodory reduction retains at most \(h\) native
   multipliers. Positive-definite stationarity eliminates all continuous
   primal variables through a matrix inverse. Every retained primal row
   remains in the resulting formula.
3. **Control algebraic precision.** The original proof uses fixed-support
   limits and coefficient-sensitive quantifier elimination. The explicit
   value refinement instead chooses independent active gradients, making
   the selected multiplier root nonsingular. A controlled polynomial
   deformation produces a finite quotient algebra; its multiplication
   determinant and ordered coefficient extractions control coefficient
   heights. Classical multihomogeneous root counting on the full selected
   KKT equations gives the sharper degree \(2^s\binom ds\), where
   \(d\le n\) is the affine dimension and \(s\le\min(h,d)\).
   A common parameter-polynomial identity passes this bound through the
   optimizer limits. Other complex KKT components may have positive
   dimension. Root bounds then yield positive-violation separation and a
   radius containing a feasible point. The root-counting, deformation and
   elimination tools themselves are classical.
4. **Obtain exact algorithms and integer preservation.** On each bounded
   integer fiber, minimum violation is zero or exceeds one uniform rational
   gap. Established continuous polyhedral square approximations with smaller
   error therefore preserve every feasible integer assignment. Classical
   fixed-integer-dimension MILP algorithms then give exact decision. Exact
   threshold queries and established algebraic recognition recover
   continuous feasible coordinates.
5. **Remove integer bounds.** Parameter-dependent affine charts describe the
   continuous projection using few quantified variables and controlled
   polynomial degrees and coefficient bits. The formula can have many
   disjuncts; it is used for a witness bound, not explicitly generated by the
   algorithm. Khachiyan–Porkolab's integer-witness theorem supplies a bounded
   integer representative, after which the reviewed bounded construction
   applies.
6. **Control unbounded mixed-integer optimization.** Rational recession
   elimination preserves all attainable objective values until it detects
   unboundedness or reaches a problem with compact objective sublevels.
   Continuous eliminations only delete coefficients; at most \(k\)
   eliminations change integer coordinates and can increase coefficient
   size. Compact terminal projections then have bounded algebraic endpoints,
   giving a polynomial algebraic bound for the common optimal value. Apply
   the integer-witness theorem to the **original** optimal set, using an
   isolated algebraic threshold, to bound an original optimal integer
   assignment. This avoids a potentially large sequential lift through the
   eliminated variables.

The unbounded-value extension additionally uses classical closedness and
finite-attainment results for convex quadratic systems. A feasible-point
radius alone is not a bound on an optimizer of an unrelated objective.
The sharper optimizer bound first regularizes by the norm in the original
coordinates, then relaxes rows. Taking the row-relaxation limit before the
norm-regularization limit selects the canonical optimizer on one common
support. Rational linear combinations and the primitive element theorem
bound the whole optimizer field, not a product of separate coordinate
degrees. The recovery algorithm still simulates decisions on the optimal
set through exact comparisons of rational-input value problems. It never
passes an irrational threshold to the rational-input feasibility algorithm.
Improved output bounds do not automatically improve its composed running
time by the same exponent.

To construct the common field, the algorithm recognizes sufficiently many
short rational linear combinations of the selected coordinates and chooses
one of maximum degree. It then recovers coordinate polynomials from field
norms of generator-plus-coordinate combinations by interpolation and
differentiation. Raising each sample's minimal polynomial to the appropriate
field-degree quotient handles samples that fail to generate the whole field.
This uses classical primitive-element, algebraic-recognition and rational
univariate representation methods; the polynomial overhead follows from the
new structural degree and height bounds.

In the final mixed-integer optimization step, a continuous box that merely
preserves feasibility is insufficient. Either add each objective threshold
before computing its feasible-point radius, or use the continuous optimizer
theorem to bound a canonical optimizer uniformly in every bounded integer
fiber. The first route preserves each threshold query; the second preserves
every fiber optimum. Separation of distinct fiber values identifies an
optimal integer assignment, after which exact continuous optimization
provides the value and vector. No decreasing straight ray in the original
variables is promised when unboundedness is reported.

## 4. From residual accuracy to distance and penalties

For a nonempty rational feasible set \(F\) inside an input box, let
\(V(x)\) be the maximum of zero, all inequality violations and the
absolute affine-equality violations. The reviewed geometric theorem gives

\[
 \operatorname{dist}(x,F)\le C V(x)^{2^{-h}},\qquad
 \log_2\max(1,C)\le N^{O(h+1)}
\]

for every trial point in that box. The underlying exponent theorem also
allows real data and arbitrary bounded trial regions, with an existential
constant. The encoding bound requires the rational bounded region as part
of the input. Neither statement asserts a global pure-power estimate on
an unbounded region.

The proof counts nonlinear facial reductions. A positive PSD combination
exposing the feasible set loses at most a square root in the residual and
kills a nonzero member of the restricted Hessian span. At most \(h\)
such steps occur; affine projections lose no additional fractional power.
The quantitative proof keeps all reductions in the joint number field of
one canonical feasible point, controls its linear-system constants, and
bounds the final strict-feasibility margin. The refined arithmetic argument
works directly over that field: its degree and coefficient height enter
the logarithmic margin bound linearly, avoiding a second exponentiation by
the span parameter. The classical chain
\(x_i^2\le x_{i+1}\), \(x_h^2\le0\) shows why no larger exponent
works uniformly in \(h\).

The [full Shor-lift comparison](hessian-span-holder-hu-li-comparison.md)
also derives the qualitative exponent from a short span-decrease argument
and established conic facial-reduction error bounds. It should therefore
be treated as a modest structural refinement or corollary. The effective
encoding bound for its constant is a separate candidate contribution;
the conic comparison does not establish that arithmetic conclusion.

The [consequence note](hessian-span-holder-consequences.md), with a separate
[completed review](hessian-span-holder-consequences-review.md), develops two
uses. In a fully boxed mixed-integer model with a nonempty feasible set,
slice convexity suffices for a uniform distance bound. A feasible slice
admits a repair in the same slice; an infeasible slice uses its positive
residual gap and a feasible point elsewhere. Thus
an objective that is \(L_f\)-Lipschitz on the entire boxed mixed-integer
domain has the same global minimizers after adding
\(\rho V^{2^{-h}}\), whenever \(\rho>L_fC\). For a rational
quadratic objective, even indefinite, a sufficient integer penalty has
\(N^{O(h+1)}\) bits. Exactly \(h\) squaring equations represent
the fractional power. That lift is nonconvex; minimizer-set exactness does
not make it easier to solve.

For that fully boxed model under full joint PSD, the outer MILP can
additionally approximate every nonempty continuous integer fiber within
distance \(\tau=2^{-p}\), \(p\in\mathbb Z_{\ge0}\),
while excluding all infeasible integer fibers and adding no integers.
Its size is polynomial in \(N+p\) for fixed \(h\), where \(p\)
is the requested number of accuracy bits. Every outer
point then has a repair within \(\tau\) in its own integer slice;
the displayed rational point need not itself be feasible. An affine
objective loses at most \(\|c_x\|_2\tau\), where \(c_x\) is its
continuous coefficient vector. Translating a rational outer point to the
origin and applying algebraic minimum-norm recovery constructs its nearest
feasible point; complexity includes the outer point's encoding length.
These are structural precision guarantees, not tested practical estimates
or a numerically efficient repair implementation.

## 5. Contribution relative to the strongest examined prior results

The following comparisons summarize primary-source inspections recorded in
[the first audit](hessian-span-prior.md),
[the alternative-terminology audit](hessian-span-alternate-terminology-audit.md),
[the package assessment](hessian-package-assessment.md), and
[the mixed-integer attainment audit](mixed-integer-attainment-prior.md).
The error-bound comparison is recorded in
[its initial audit](hessian-span-holder-prior.md) and
[the original-source follow-up](hessian-span-holder-original-source-audit.md).
[The degree audit](multihomogeneous-degree-prior.md) separates the classical
root count from its use in the present parameterization. The
[certificate comparison](algebraic-certificate-prior.md),
[rational-infeasibility comparison](rational-infeasibility-prior-review.md)
and [unboundedness comparison](succinct-unboundedness-prior.md) distinguish
the new encoding claims from older alternatives and algorithms. This synthesis
does not claim to have independently reread every cited primary paper.

The repository's earlier [fixed-count value proof](../paper-exact-penalties/sections/05-fixed-count.tex)
already supplied the active affine-face reduction, regularized KKT
elimination and quantified limit formula. The structural additions here
are the affine equations obtained from active Hessian dependencies and
the resulting multiplier compression to \(h\), followed by the broader
exact algorithmic consequences. This package should not claim the entire
proof architecture as new.

| Prior result or mechanism | What is already established | Proposed addition and remaining distinction |
|---|---|---|
| Grigoriev–Pasechnik and Kamminga–Rudolph few-quadratic algorithms; Nie–Ranestad algebraic degree | Polynomial algebraic complexity for fixed counts of complete quadratic forms, and strong generic or suitably isolated critical-point degree bounds | Arbitrarily many native rows and arbitrary affine parts reduce to a bound controlled by **Hessian matrix span**, without genericity or Slater. The active affine restriction is the missing step in the direct parameter substitution. |
| Basu–Pollack–Roy elimination; Kannan–Lenstra–Lovász algebraic recognition; Chandrasekaran–Tamir algebraic optimization | Effective degree and coefficient bounds, recognition of algebraic numbers from certified approximations, and separation followed by exact threshold search | These are used as established machinery. The new claim must be the structural bound that makes their use polynomial for the present class. |
| Bank–Mandel (1987); continuous attainment and closedness results of Terlaky and Luo–Zhang | Finite attainment is old, including a broader rational mixed-integer quasiconvex polynomial class in Bank–Mandel's result | Qualitative attainment is not a contribution claimed here. The recession reduction is useful for preserving the matrix-span parameter and controlling coefficient size in the exact algorithm. |
| Obuchowska (2008), Algorithm A, Theorem 5.1 and Corollary 5.1 | Polynomial-time boundedness classification for continuous convex quadratic optimization, and equivalence of continuous and mixed-integer objective unboundedness when the rational mixed-integer problem is feasible | These classification and equivalence statements are not new. The supporting refinement is a uniformly valid, succinct polynomial escape curve with integer increments and a locally checkable construction trace. |
| Del Pia's exact mixed-integer convex quadratic result | FPT in integer dimension for a convex quadratic objective over a polyhedron, with exact status, value and optimizer; corresponding one-quadratic-sublevel machinery | The current optimization class permits arbitrarily many quadratic rows of fixed continuous Hessian span. Its polynomial-time guarantee for each fixed \((k,h)\) is weaker than FPT and does not improve Del Pia's special-case running time. |
| Khachiyan–Porkolab convex semialgebraic integer optimization | Exact algorithms with fixed free and quantified dimensions, and small integer witnesses controlled by formula degrees and heights | The new projection description removes the unbounded continuous dimension from the relevant algebraic description. Directly quantifying all original continuous variables would not give the stated fixed-\(k,h\) result. |
| Ben-Tal–Nemirovski and sawtooth polyhedral approximations; Kocuk's exact integer-preserving approximations | Compact rational approximations, and exact preservation of integer points in certain balls and ellipsoids | Integer preservation is an old mechanism. The claimed extension controls the algebraic minimum violation of existential continuous fibers, where integer denominator separation alone is insufficient. |
| Wang–Pang quadratic error bounds; Sturm and Lourenço facial-reduction bounds; effective Łojasiewicz inequalities | Hölder error bounds without constraint qualifications, accumulated square-root losses, and general coefficient-sensitive constant bounds | The qualitative exponent follows from established full Shor-lift/conic theory plus a short Hessian-span decrease argument. Treat it as a structural corollary. Its uniform coefficient-encoding bound is separate; the original Wang–Pang comparison remains incomplete. |
| Facial reduction and extended duality of Ramana, Pataki, and related work; Jeyakumar–Li's alternative for SOS-convex systems | Exact alternatives without Slater, facial reduction followed by dual certificates, and real positive-aggregate certificates of infeasibility | The candidate refinement controls the number of curved sections and explicit certificate encoding by Hessian span, keeps finite-optimality certificates in the primal field, and gives rational infeasibility aggregates with a format-specific weight lower bound. It does not introduce the underlying alternatives. |

Canny's generalized characteristic-polynomial method and
Grigoriev–Pasechnik's ordered-infinitesimal and finite-quotient machinery
also precede the explicit algebraic refinements. The sharpness proof uses
classical generic QCQP degrees and Hilbert irreducibility inside a convex
open set. These are credited in the linked elimination, optimizer, degree
and sharpness notes; neither a new Bézout theorem nor a new generic degree
formula is claimed.

No equivalent theorem was identified in the examined sources. That bounded
search result does not establish originality. Fixed matrix span also does
not imply fixed semidefinite matrix size, simultaneous diagonalization, or
a bounded number of shared PSD generators. For the last distinction, the
matrices

\[
 Q(t)=\begin{pmatrix}I_r&tI_r\\tI_r&t^2I_r\end{pmatrix}
\]

have span dimension three for at least three distinct rational \(t\),
while two distinct matrices already have aggregate rank \(2r\).
Any nonzero PSD generator used positively in \(Q(t)\) has range inside
\(\{(u,tu):u\in\mathbb R^r\}\). Those ranges intersect only at
zero for distinct parameters, so \(m\) such matrices require at least
\(m\) shared PSD generators, even allowing generators outside their span.
This rules out that specific simple reduction; it does not exclude all
alternative formulations.

## 6. Concrete application: vector polynomial fitting with outlier choices

Let

\[
 P_x(t)=\sum_{j=0}^d x_jt^j,\qquad x_j\in\mathbb R^r,
\]

and let rational observations \((t_i,y_i)\) have rational squared
tolerances \(\tau_i\ge0\). A binary variable \(z_i=1\) permits
discarding observation \(i\); otherwise require

\[
 \|P_x(t_i)-y_i\|_2^2\le\tau_i.
\]

Arbitrary rational affine budget, group and coefficient constraints are
allowed, along with other bounded integer decisions. The continuous Hessians
are proportional to
\(v_d(t_i)v_d(t_i)^T\otimes I_r\), where
\(v_d(t)=(1,t,\ldots,t^d)^T\), so \(h\le2d+1\).
For fixed polynomial degree, the response dimension and number of
observations can grow without increasing that bound.

The reviewed [application corollary](hessian-span-applications-and-limits.md)
gives a polynomial-size rational MILP with exactly the same feasible bounded
integer choices and no new integer variables, even without supplied bounds
on the fitting coefficients. A uniform small-point radius supplies valid
big-M constants before applying the joint-convex construction. An objective
depending linearly on the discard variables is preserved exactly. This is a
precise structured Euclidean maximum-consensus model, rather than a claim
about arbitrary geometric fitting models. Scalar rational absolute-error
fitting is already linear; growing vector dimension is the informative case.

There is an important significance limit. For **purely binary** original
decisions, polynomial-time fixed-assignment feasibility already implies a
polynomial-size MILP with continuous auxiliaries: compile its Boolean
decision circuit into gate inequalities. Binary inputs force continuous
gate outputs to be Boolean. Thus existence of a polynomial MILP for the
binary application is not a separate complexity advance beyond the
continuous decision theorem. The geometric construction supplies a direct
formulation; whether it is useful computationally is untested. General
bounded integer variables do not obtain that no-new-integer conclusion
merely by replacing binary digit variables with continuous variables.

## 7. Exact outputs and independently checkable certificates

The common-field output above permits direct checking of algebraic primal
points. The following reviewed results give additional certificates. Their
construction guarantees differ and should not be conflated.

| Outcome | Certificate and bound | Construction status |
|---|---|---|
| Finite continuous optimum | At most \(h\) curved minimizer sections, followed by a KKT identity proving global optimality. The canonical primal point and all certificate coefficients lie in its one real number field, of degree at most \(D(n,h)\); total certificate bits are \(N^{O(h+1)}\). | Existence, size and a polynomial-time verifier are proved. The primal point can be constructed, but a complete polynomial algorithm to extract all exposing multipliers is not yet proved. See [the certificate theorem](algebraic-primal-dual-certificates.md) and [proof review](algebraic-certificate-proof-review.md). |
| Continuous infeasibility | A strictly positive convex quadratic aggregate with rational nonnegative weights, rational center and positive rational margin. At most \(n+1\) weights are positive, and total bits are \(N^{O(h+1)}\). | Existence, size and rational verification are proved. Conversion from a supplied controlled algebraic aggregate is polynomial; standalone polynomial extraction of that initial aggregate is not proved here. See [the rational theorem](rational-infeasibility-certificates.md) and [review](rational-infeasibility-review.md). |
| Mixed-integer objective unboundedness | An exact feasible anchor, a polynomial curve preserving integrality of its designated coordinates at integer parameters, and a rational local construction trace. Certificate size and independent verification are polynomial for fixed \(k,h\). | The complete certificate is constructible in polynomial time for fixed \(k,h\). Its curve increment alone is constructible in polynomial time without fixing these parameters. See [the escape theorem](succinct-unboundedness-curves.md) and [final review](all-integer-escape-review.md). |

For the finite continuous certificate, each curved section comes from a
nonnegative combination of native PSD quadratic rows whose minimum over the
current polyhedron is zero. It intersects that polyhedron with affine
equations forcing the aggregate's quadratic and supporting-linear terms to
vanish. The resulting sections preserve every feasible point, but need not
be faces of the original polyhedron. All coefficients stay in the primal
field because the exposing weights solve linear systems there; the
certificate does not require additional algebraic extensions. The verifier
checks signs and explicit identities in the selected real embedding.
Applying this certificate after fixing an integer assignment proves
optimality in that continuous fiber only. It does not certify a globally
optimal integer assignment.

For rational infeasibility, include affine rows, with each equality written
as two inequalities, in the list of polynomials. The certificate is
\[
 \sum_i w_iq_i(x)
   =\gamma+\tfrac12(x-c)^TH(x-c),\qquad
 w_i\ge0,\quad \sum_iw_i=1,\quad
 \gamma>0,\quad H=\sum_iw_iQ_i\succeq0.
\]
It contradicts simultaneous feasibility. Rational rounding must preserve
the aggregate's kernel and finite minimum; arbitrary rounding would not
suffice. A quadratic repeated-squaring chain forces
\(\Omega(2^h)\) bits in the explicit rational weights of every such
positive aggregate. This lower bound concerns that certificate format,
not arbitrary proof systems or decision running time. Nor does the
continuous certificate establish mixed-integer infeasibility when the
continuous relaxation is feasible.

For unboundedness, fix any rational radius \(R\ge1\). When the continuous
objective is unbounded below, the algorithm constructs
\(p(T)\in\mathbb Z[T]^{n+k}\), with \(p(0)=0\), and rational
\(\gamma>0\), such that **every** continuously feasible anchor \(a\)
with \(\|a\|_\infty\le R\) satisfies
\[
 a+p(T)\ \text{is feasible},\qquad
 q_0(a+p(T))=q_0(a)-\gamma T
 \quad(T\ge1).
\]
The integer-coefficient increment preserves integrality of every designated
integer coordinate at integer \(T\). Its arithmetic circuit has size and construction time
polynomial in \(N+\operatorname{bits}(R)\), without fixed \(k,h\);
expanded degree can be exponential. The complete fixed-\((k,h)\)
certificate adds a small integer assignment and a common-field continuous
anchor. Verification checks the native signs and local rational elimination
and majorant identities, rather than relying on a general circuit identity
test. The anchor may be irrational; a rational feasible anchor is not
promised. Obuchowska's older boundedness theorem supplies the qualitative
continuous/mixed-integer equivalence; this circuit and its checkable trace
are supporting refinements.

## 8. Limits, verification and next questions

Convexity, rational degree-two input and the parameter restriction are
substantive. General convex QCQP includes square-root-sum threshold problems;
the examined literature does not give the needed general polynomial exact
precision. Slice convexity can give a nonconvex integer projection that no
continuous polyhedral lift with the same integer coordinates can preserve.
An unbounded pure-integer parabola shows that a finite rational polyhedral
description preserving every unbounded integer assignment cannot always
exist. Removing input bounds from **optimization** does not remove this
formulation obstruction. The application note records exact counterexamples
and a convex quartic boundary; none should be read as a hardness theorem
for every nearby class. Full PSD of the native polynomials is stronger than
convexity of their feasible set: general second-order-cone formulations can
have nonattained finite infima and are not covered automatically.

Important proofs received independent adversarial reviews, including active
restriction, multiplier compression, finite-precision decision, the compact
square lift, small continuous and integer witnesses, algebraic feasible
point and optimizer recovery, and the full mixed-integer optimization
reduction. The latter review found a missing justification for using
continuous boxes in optimization; the corrected threshold and optimizer-box
arguments were independently rechecked. Separate reviews checked the Hölder
exponent and constant bound; the quantitative proof's exposing multipliers
were corrected to use only active native rows and independently rechecked.
Targeted exact calculations checked the irrational
singleton, PSD-generator example, square-approximation identities and small
lift instances, as well as obstructions in the explicit elimination lemma.
Those finite checks challenge formulas and boundary cases;
they do not prove universal complexity statements. The general theorems
rest on written proofs and the cited classical results. No Lean
formalization, solver-performance experiment, project-wide verification or
CI inspection is claimed for this package.

The newer common-field construction and certificate proofs also received
independent review. Exact symbolic examples check common-field interpolation
when a sample loses degree, as well as nonnormal and nonmonic cases.
These checks do not implement or validate the full algebraic-recognition
algorithm. A verifier for a supplied common-field point can use univariate
root and sign computations; it need not trust an asserted minimal-polynomial
label. The remaining certificate-construction gaps are stated in Section 7,
and the existing exact optimization algorithms do not depend on filling them.

The next consequential questions are:

- Identify broader constraint classes with comparable effective value and
  witness bounds, keeping the distinction between native PSD polynomials
  and convex feasible sets explicit.
- Obtain substantially sharper explicit precision bounds and algorithms that
  exploit matrix span directly, without constructing the worst-case lifts.
- Determine whether fixed-parameter tractability in \((k,h)\), or a better
  parameter dependence, is possible beyond polynomial time for each fixed
  \((k,h)\).
- Construct the small facial and rational infeasibility certificates
  directly, and identify a useful certificate format for global finite
  mixed-integer optimality.
- Test the direct formulation against existing conic methods on structured
  Euclidean fitting or scenario models, measuring both size and relaxation
  strength before asserting practical value.
- Extend the prior-art audit and seek an independent external assessment of
  the active affine restriction and its consequences. The present evidence
  supports a candidate contribution, not a priority claim.

The synthesis author ran a targeted inline Python check of this file's local
Markdown links, paired math delimiters, control characters, trailing
whitespace and final newline; all checks passed. This verifies the document's
basic consistency, not its mathematical claims.
