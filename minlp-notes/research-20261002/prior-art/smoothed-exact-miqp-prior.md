# Prior-art audit: smoothed exact MIQP and separable low-rank MINLP

Date: 2026-10-02. This focused audit compares two current candidate lanes:
the general bounded mixed-integer QP with fixed integer dimension and
negative inertia, and the separable mixed-box problem with low-rank
concave coupling. The candidate statements remain subject to the review
status recorded in their source notes. This audit records relevant
precedents and boundaries; it is not a completeness or publication-priority
claim.

## Candidate statements and their different scopes

The general mixed-integer QP candidate has a bounded rational polytope
\(\mathcal P\), feasible set
\(X=\mathcal P\cap(\mathbb Z^p\times\mathbb R^{n-p})\), rational quadratic
objective, and a supplied factorization
\(A+\alpha T^\mathsf{T}T\succeq0\), where \(T\) has \(k\) rows and
\(k\) is the negative inertia. It adds independent finite-grid noise to
all \(n\) original linear coefficients. The proposed algorithm closes
auxiliary cells only after certifying both one fixed-label quadratic
critical region and a best-other-integer-label gap. It uses at most \(2p\)
convex-MIQP exclusion solves to certify the latter. Integer-label
isolation bounds the probability of a small gap; a same-draw exact
enumeration fallback handles exceptional grid draws. The claimed bound is
\(f(p)C^k(1+H_{\rm amb})\operatorname{poly}(I)\), with \(H_{\rm amb}\)
containing factors of the form
\(2+(1+2k)\alpha\sqrt n\,w_i/(2\sigma)\). Thus it gives expected
polynomial bit work for fixed \(p,k\) when the displayed numerical
width-to-noise ratios are polynomially bounded, but it is not FPT in \(k\)
with an absolute polynomial exponent. The derivation has passed a fresh
independent review and targeted exact checks; see the
[reviewed candidate note](../new-direction/smoothed-miqp-cell-closure.md).

The separable mixed-box candidate has a different randomization and a
different structural promise. Its objective is a sum of convex univariate
rational functions minus a rank-\(r\) concave quadratic. Coordinates may
be continuous intervals or integer intervals, but the feasible set must
be a product box. It perturbs the \(r\) factor coordinates independently;
the induced perturbation in the original variables is correlated and
low-rank. Scalar convex recourse gives exact responses without enumerating
long integer intervals. The proposed mixed piecewise-quadratic version
claims exact output for every draw and expected work
\(C^r(1+H_{\rm aligned})\operatorname{poly}(I)\), with no uniqueness or
quadratic-growth promise. It does not handle coupled constraints or a
general dense convex residual. The mixed piecewise-quadratic note has
passed two independent reviews and targeted exact checks. The narrower
pure-integer quartic version also has a completed two-review proof:
exactness uses a rational objective-value lattice, and the number of
integer coordinates is unrestricted. See the
[reviewed mixed separable result](../new-direction/smoothed-mixed-separable-closure.md)
and the [reviewed pure-integer result](../new-direction/smoothed-integer-low-rank.md).

The mixed separable note also proves an ambient-noise variant on the same
product-box class: all original linear coefficients may be perturbed
independently, with exact output on every draw and expected polynomial
work at fixed coupling rank under its numerical bounds. The current
ambient count has powers of \(n\) depending on \(r\), so this is not FPT in
rank. It is a direct prior for the full-coordinate noise model, but its
separable objective and product domain are narrower than the general
mixed-polytope theorem.

The factor-noise and ambient-noise results on separable boxes are separate
laws. The general mixed-QP candidate uses independent ambient
coefficient perturbations and supports arbitrary bounded mixed
polytopes, with fixed \(p\). The separable-box lane supports arbitrarily
many integer coordinates only under a product domain and coordinatewise
convex recourse; it has both a factor-noise result and the narrower
ambient-noise variant just described.

## Exact convex-MIQP is an established oracle

Del Pia proves an exact Turing-model algorithm for rational mixed-integer
convex quadratic programming that is fixed-parameter tractable in the
number \(p\) of integer variables, with arbitrarily many continuous
variables. It handles feasibility and boundedness and returns an exact
solution when the optimum is finite. The theorem applies to each proposed
cell-closure recourse problem: after adding the auxiliary quadratic term,
the Hessian is positive semidefinite, and the integer-label exclusion
problems add only linear inequalities. This is a strong existing
algorithmic primitive, not a smoothed nonconvex-QP result. It explains why
the general candidate's integer dimension is a natural parameter.
[[pia2025-convex-quadratic-sets-and-the]] p.1-3,p.13-23

This oracle distinction matters. The candidate needs exact values and
attaining rational witnesses for cell and gap certificates, rather than
only a fast numerical convex-MIQP solve. In the separable-box lane, the
proposed recourse is simpler: each integer coordinate is solved by binary
search on nondecreasing forward differences, and each continuous
piecewise-quadratic coordinate has a finite list of affine or constant
response states. Neither recourse argument solves arbitrary coupled
integer constraints.

## Deterministic low-inertia approximation is close, but not exact

Del Pia's 2023 algorithm gives an objective-range-relative
\(\varepsilon\)-approximation for bounded MIQP when both the total Hessian
rank and the integer dimension are fixed. Its runtime is polynomial in
input size and \(1/\varepsilon\), with exponential dependence on the
fixed parameters. The 2026 rational-Jacobi result relaxes the rank
condition to fixed negative inertia plus fixed integer dimension, while
allowing unrestricted positive inertia; it is also an
objective-range-relative approximation with polynomial dependence on
\(1/\varepsilon\). These results are the closest deterministic
low-inertia MIQP algorithms and establish that negative inertia is a
meaningful parameter. They do not return an exact optimizer in the
stated bounds. Driving \(\varepsilon\) below the separation of rational
objective values can require exponentially small \(\varepsilon\), so the
approximation guarantees do not imply exact polynomial bit complexity.
[[pia2023-an-approximation-algorithm-for-indefinite]] p.1-3,p.29-31
[[pia2026-rational-jacobi-rotations-and-the]] p.1-4,p.15,p.20-21

For the separable integer lane, Del Pia's concave integer-QP approximation
is another useful nearby result. It treats a separable concave quadratic
with only \(s\) nonlinear integer coordinates and bounds its approximation
work using \(s\) and the constraint matrix's largest subdeterminant
\(\Delta\). The theorem is exponential in \(s\) and polynomial in
\(n,\Delta,1/\varepsilon\) for fixed \(s\); a totally unimodular
specialization is stronger. Its nonlinear-coordinate parameter is not
the rank of a dense concave interaction. It therefore does not directly
cover a low-rank term \(-\alpha\|Tx\|^2/2\) coupled across arbitrarily many
coordinates when all univariate terms are convex. It is approximate, not
an expected exact solver under factor-coordinate noise.
[[pia2019-subdeterminants-and-concave-integer-quadratic]] p.1-3,p.6-7

## Independent objective noise and integer-label isolation are known

Beier and Vöcking's STOC 2004 paper studies binary optimization with
independent stochastic objective or constraint coefficients. Its
isolating lemmas bound winner gaps, and its adaptive-precision algorithm
establishes a smoothed-complexity characterization through the
corresponding unary problem. Röglin and Vöcking extend this line to
integer programs: under objective-only noise, their Lemma 4 bounds the
best-versus-second-best gap for an arbitrary finite integer feasible set.
Their adaptive-rounding result uses a pseudopolynomial solver, but the
paper's smoothed-time convention is a high-probability tail bound; the
authors explicitly distinguish it from polynomial expected running
time. These works make both the label-isolation argument and the
“anti-concentration plus exact certification” pattern established
ingredients. The candidate's finite-grid isolation inequality is a
specialized version for integer labels with arbitrary costs, including a
continuous recourse value; its endpoint-grid correction and use in
continuous cell closure should not be presented as a new isolation
principle. The local
[integer-label isolation note](../new-direction/integer-label-isolation.md)
states the bound and its finite-grid correction explicitly.
[[beier2006-typical-properties-of-winners-and]] p.2-4,p.9-10
[[roglin2007-smoothed-analysis-of-integer-programming]] p.3-8,p.21-28

Beier, Röglin, Rösner, and Vöcking bound the expected size of the
Pareto-optimal set for an arbitrary finite integer feasible set under an
independent bounded-density random linear profit and an arbitrary fixed
ranking objective. Their continuous-density assumption does not cover the
candidate's finite grid directly.
After conditioning on the continuous-coordinate perturbation, the
mixed-label value function in the general candidate is an arbitrary
ranking cost on the feasible integer labels. With the sign of the random
profit chosen opposite to the additive integer perturbation, a label
minimizing the sum of the ranking cost and perturbation is Pareto-optimal
in that two-criterion view. This is a close additional comparator. Their
bound depends on the numeric domain size and range, and the algorithmic
consequences concern particular discrete Pareto-enumeration methods; it
does not provide a general procedure for finding the candidates without
enumerating labels, nor does it handle a continuous quadratic recourse
oracle or certify an auxiliary cell. The candidate's exact
convex-MIQP-based exclusion test and cell certificate remain separate
algorithmic requirements.
[[beier2022-the-smoothed-number-of-pareto]] p.2-8

The difference between expected and high-probability bounds must remain
explicit. Röglin--Vöcking and Beier--Vöcking provide strong discrete
smoothed-analysis precedents, but neither directly gives expected
polynomial Turing work for a continuous mixed-integer quadratic
optimization problem. The proposed candidates use a single finite
rational perturbation law selected from the base input, return exact
rational solutions on every draw, and use a same-draw fallback to pay
for grid atoms and ties. Those output and runtime details are not
consequences of the discrete isolation lemmas alone.

## Low-dimensional smoothed geometry and parametric-QP precedents

Kelner and Nikolova prove expected-polynomial optimization for a
constant-rank quasi-concave objective over an integral polytope after a
random rotation of its low-rank objective subspace. The method bounds
the expected number of vertices in a projected polytope. This is a
substantial precedent for expected algorithms based on low-dimensional
geometry, but it assumes quasi-concavity and uses random subspace
rotation; it is not independent additive noise on the original linear
coefficients of an arbitrary indefinite QP. It also does not state the
candidate's exact rational Turing-output guarantee.
[[kelner2007-on-the-hardness-and-smoothed]] p.2-4

For the cell-closure mechanism itself, Ding's thesis already reformulates
structured indefinite QPs as global minimization of a parametric convex-QP
value function and proves a global-minimizer/fiber correspondence. In
the one-negative-eigenvalue case it describes a piecewise-quadratic
scalar envelope. Multiparametric-QP work supplies affine active-set
responses, polyhedral critical regions, and quadratic value formulas.
These are genuine conceptual precedents for the value-function and
critical-region representations. They do not give a smoothed bound on
unresolved cells, independent integer-label gap control, or expected
exact mixed-integer bit complexity. The more detailed comparison and
locators are in the existing [cell-closure audit](smoothed-cell-closure-prior.md).
[[ding1996-a-parametric-solution-for-local]] p.18-19,p.28-34

## Easy and parameter-dependent discrete baselines

The binary special case should not be used to motivate a solver advantage
for the low-rank separable theorem. For rank one, a sign flip of binary
variables makes all pairwise coefficients of the negative rank-one
quadratic submodular, so an \(s\)-\(t\) min-cut solves the objective
deterministically. For fixed rank \(r\), the binary objective can be
lifted to the zonotope of \((Tx,c^\mathsf{T}x)\); fixed-dimensional
vertex enumeration gives an \(n^{O(r)}\) exact algorithm. Ferrez,
Fukuda, and Liebling give the fixed-rank PSD binary zonotope algorithm,
with \(O(n^{r-1})\) candidates for the no-linear-term form. Hladík,
Černý, and Rada cover arbitrary linear terms and arbitrary-sign
fixed-rank quadratic matrices on a continuous box, with a face-enumeration
bound polynomial in \(n\) for fixed rank. This covers the binary objective
after negation because its separable unary costs are affine there and the
remaining quadratic is positive semidefinite; maximizing a convex
function over the continuous box has an optimum at a vertex. With explicitly listed finite
coordinate labels, the analogous Minkowski-sum enumeration is polynomial
in the total listed label count for fixed rank. These methods are XP in
rank or use binary structure; they do not enumerate binary-encoded
integer intervals in time polynomial in their bit length.

The rank-one binary case is also exact by a sign flip and an \(s\)-\(t\)
min-cut: all pairwise coefficients of the transformed negative
rank-one quadratic are nonpositive, so the binary energy is submodular.
The continuous rank-one quadratic case has a direct scalar
piecewise-quadratic solution. The project's
[separable low-rank audit](separable-lowrank-minlp-prior.md) gives these
derivations and source locators. A recent synthesis by Soltanalian and
Mousavi distinguishes the positive-semidefinite fixed-rank maximization
case from unfavorable curvature and emphasizes that low rank alone does
not give an enumerable candidate set. Its rank-one
negative-semidefinite maximization hardness example has the opposite
curvature orientation to the binary minimization baseline above.
[[liebling2005-solving-the-fixed-rank-convex]] p.4-8
[[rada2021-a-new-polynomially-solvable-class]] p.1-8
[[mousavi2026-the-rank-collapse-principle-for]] p.1-3,p.8-9,p.13-14

The exact recourse for a convex univariate integer term over a long
interval is elementary discrete convexity: nondecreasing forward
differences let the algorithm locate the minimizer by binary search in
the encoded interval length. That avoids explicit label enumeration,
but by itself it does not minimize the outer nonconvex low-rank objective.
The candidate's additional claim is the combination of this recourse
with low-dimensional cell closure, a fixed rational noise grid, exact
gap transfer to original objective values, and a controlled fallback.

## Scope assessment

For the general mixed-QP lane, the strongest prior ingredients are:
exact convex-MIQP optimization FPT in integer dimension; parametric
convex-QP critical-region representations; deterministic
low-negative-inertia MIQP approximation; and discrete random-objective
isolation/adaptive precision. The candidate combines them by certifying
the best alternative integer label locally, controlling failures of
that certificate through independent noise on integer coefficients,
and using the low-inertia cell method for the continuous factor
coordinates. In the focused primary sources examined here, no one
statement gives that full conjunction. This is a scoped search result,
not a novelty or priority conclusion.

The combination is not an immediate corollary of any one ingredient.
Integer-label isolation controls competition between distinct discrete
labels, but a continuous feasible slice has no second-best positive value
gap. The exact convex-MIQP oracle solves a queried recourse problem, but
does not bound how many parameter cells must be explored. Critical-region
methods supply local quadratic formulas, but do not certify that a mixed
label remains best throughout a cell. The candidate's additional argument
has to join these certificates and account for finite-grid atoms through
the same-draw fallback.

For the separable-box lane, fixed-rank binary problems and explicitly
listed label sets already have deterministic enumeration methods.
Approximation algorithms cover several other low-inertia, few-nonlinear,
or low-subdeterminant regimes. The candidate's remaining comparison
boundary is the exact expected bit-work guarantee for dense low-rank
concave coupling with arbitrarily many separable coordinates and
binary-encoded integer intervals, under factor-coordinate noise. Its
fixed-parameter form depends on both rank and the displayed
curvature-range/noise ratios; a ratio that grows polynomially with input
length gives polynomial time for fixed rank, but does not by itself give
FPT in rank with an absolute input-polynomial exponent.
That statement is much narrower than a general tractability claim for
low-rank integer nonlinear optimization and still excludes coupled
constraints.

The targeted search found no directly matching primary theorem for
either complete candidate statement. Search absence is not evidence of
priority. No new source requiring literature-ingest routing was found:
the closest primary papers cited above are already available and read in
the local literature packages. Searches for smoothed mixed-integer
quadratic optimization mostly returned unrelated smoothed SDP results
or stochastic-program stability/approximation papers, which do not
provide exact solver complexity under random objective coefficients.

## Sources and local access

- Del Pia, “Convex Quadratic Sets and the Complexity of Mixed Integer
  Convex Quadratic Programming,” SIAM Journal on Optimization (2025),
  [DOI 10.1137/24M1636782](https://doi.org/10.1137/24M1636782).
  Local primary text: [[pia2025-convex-quadratic-sets-and-the]].
- Del Pia, “An Approximation Algorithm for Indefinite Mixed Integer
  Quadratic Programming,” Mathematical Programming (2023),
  [DOI 10.1007/s10107-022-01907-3](https://doi.org/10.1007/s10107-022-01907-3).
  Local primary text: [[pia2023-an-approximation-algorithm-for-indefinite]].
- Del Pia, “Rational Jacobi Rotations and the Complexity of Approximating
  Mixed Integer Quadratic Programming,” arXiv:2607.29386 (2026),
  [primary preprint](https://arxiv.org/abs/2607.29386).
  Local primary text: [[pia2026-rational-jacobi-rotations-and-the]].
- Beier and Vöcking, “Typical Properties of Winners and Losers in
  Discrete Optimization,” STOC 2004,
  [DOI 10.1145/1007352.1007409](https://doi.org/10.1145/1007352.1007409).
  The separately published 2006 SIAM version is a distinct unread record;
  this audit relies only on the read STOC text.
- Röglin and Vöcking, “Smoothed Analysis of Integer Programming,”
  Mathematical Programming (2007),
  [DOI 10.1007/s10107-006-0055-7](https://doi.org/10.1007/s10107-006-0055-7).
- Beier, Röglin, Rösner, and Vöcking, “The Smoothed Number of
  Pareto-Optimal Solutions in Bicriteria Integer Optimization,”
  Mathematical Programming (2023),
  [DOI 10.1007/s10107-022-01885-6](https://doi.org/10.1007/s10107-022-01885-6).
- Kelner and Nikolova, “On the Hardness and Smoothed Complexity of
  Quasi-Concave Minimization,” FOCS 2007,
  [DOI 10.1109/FOCS.2007.4389517](https://doi.org/10.1109/FOCS.2007.4389517).
- Del Pia, “Subdeterminants and Concave Integer Quadratic Programming,”
  SIAM Journal on Optimization (2019),
  [DOI 10.1137/18M121873X](https://doi.org/10.1137/18M121873X).
- Ferrez, Fukuda, and Liebling, “Solving the Fixed Rank Convex Quadratic
  Maximization in Binary Variables by a Parallel Zonotope Construction
  Algorithm,” European Journal of Operational Research (2005),
  [DOI 10.1016/j.ejor.2003.04.011](https://doi.org/10.1016/j.ejor.2003.04.011).
- Hladík, Černý, and Rada, “A New Polynomially Solvable Class of Quadratic
  Optimization Problems with Box Constraints,” Optimization Letters
  (2021), [DOI 10.1007/s11590-021-01711-6](https://doi.org/10.1007/s11590-021-01711-6).
- Soltanalian and Mousavi, “The Rank-Collapse Principle for Quadratic
  Optimization,” arXiv:2608.07828 (2026),
  [primary preprint](https://arxiv.org/abs/2608.07828).
- Ding, *A Parametric Solution for Local and Global Optimization*,
  University of Waterloo thesis (1996),
  [repository record](https://uwspace.uwaterloo.ca/items/0ee267e7-ed4c-4eab-adff-a202444a746a).

No literature knowledge-base files were edited. No project-wide checks or
CI inspection were run.
