# Prior-art audit: expected exact QP under random linear tilts

Date: 2026-10-02. This focused audit compares the project's reviewed
[expected-work theorem](../new-direction/expected-smoothed-qp.md) with
smoothed optimization, low-negative-inertia QP, exact branch-and-bound,
and graphical-model results. It records close precedents and scope limits;
the audit does not establish publication priority.

## Candidate claim

The theorem starts from a rational quadratic objective on a bounded
rational polytope and independently adds small, rational-grid linear
coefficients. If the fixed Hessian has at most two negative eigenvalues,
it combines a growth-pruned low-inertia solver with a deterministic
exponential exact fallback. It samples once and interleaves both solvers
on that same perturbed input. Its expected bit-work bound is
\((I+1)^K(1+\nu S/\sigma)\), where \(I\) is the base input length,
\(\nu=\max\{0,-\lambda_{\min}(A)\}\), \(S\) is the sum of coordinate
widths of the polytope, and \(\sigma\) is the noise half-width. Thus the
expected time is polynomial when that numerical ratio is polynomially
bounded; its short binary encoding alone is not enough. The output is an
exact optimizer and value for the sampled objective; it does not solve
the unperturbed problem.

The finite rational grid matters. A continuous-noise theorem alone does
not give a finite-bit Turing input. On a grid, ties and zero-growth draws
can have positive probability, so the theorem includes a grid-atom
correction and chooses the grid fine enough that its contribution times
the fallback bound is controlled. This is distinct from conditioning on a
“good” sample or resampling until the fast solver succeeds.

## Closest expected smoothed optimization result

Kelner and Nikolova's FOCS 2007 paper is the closest broad algorithmic
precedent. Theorem 2.9 gives expected-time polynomial minimization of a
constant-rank quasi-concave objective over an integral polytope with
coordinate-bounded vertices and polynomially many facets. Its perturbation
randomly rotates the objective's low-rank subspace while keeping the
feasible polytope fixed. The proof bounds the expected number of vertices
in the projected polytope and enumerates that shadow. This is already an
expected smoothed global-optimization result parameterized by a low
nonconvexity dimension, so it rules out broad claims that expected
polynomial global solution under low-rank smoothing is new. Its model is
different: a general indefinite QP plus a linear tilt need not be
quasi-concave, the randomness is a subspace rotation rather than
independent additive coefficient noise, and the theorem does not state an
exact rational Turing bound for QP. [[kelner2007-on-the-hardness-and-smoothed]] p.3-4

Beier and Vöcking's STOC 2004 paper gives a closer perturbation-model
analogue, but for finite discrete optimization. Its generalized isolation
lemmas bound the winner gap under independent random objective
coefficients, and Theorem 3 uses adaptive rounding and certification to
derive polynomial smoothed complexity from randomized pseudopolynomial
solvability. This establishes the general pattern “anti-concentration,
then refine precision until the exact winner is certified.” A continuous
polytope has no second-best feasible point separated by a positive
objective gap, so this discrete theorem does not provide the required
continuous growth bound, retained-cell moment, or exact QP recovery.
Use the readable 2004 conference source (DOI
10.1145/1007352.1007409); the distinct 2006 SIAM journal record is
metadata-only in the local KB and is not evidence for these statements.
[[beier2006-typical-properties-of-winners-and]] p.3-4 [[beier2006-typical-properties-of-winners-and]] p.9-10

Lee and Phạm establish qualitative genericity for linear tilts of fixed
semialgebraic programs. On compact domains their generic uniqueness and
local quadratic growth imply that some positive global growth constant
exists. Their theorems do not bound its distribution near zero in terms of
the perturbation density, coordinate widths, or input length, and give no
solver runtime bound. This makes generic uniqueness and positive growth
known ingredients; the candidate's quantitative tail and its use in
expected exact work are the additional claims requiring comparison.
[[lee2016-stability-and-genericity-for-semi]] p.1-3 [[lee2017-generic-properties-for-semialgebraic-programs]] p.3-4

## Low-negative-inertia global QP algorithms

Vavasis's general compact-polytope algorithm and Luo et al.'s spectral
branch-and-bound method already isolate the negative-curvature subspace
and solve convex relaxations. Their guarantees are objective
approximations with work polynomial in inverse accuracy for each fixed
negative inertia, not exact rational recovery with logarithmic accuracy
dependence. Luo et al. bound the number of relaxations by a product of
terms proportional to the negative-coordinate range divided by
\(\sqrt{\varepsilon}\). Cen and Xia's publisher abstract likewise reports
a branch-and-bound method with \(O(1/\sqrt{\varepsilon})\) iterations
for one negative eigenvalue, extended to more negative directions. Its
full text remains unavailable in the local package, so no stronger
technical comparison is made. None of these sources gives a random-tilt
expectation or uses a quadratic-growth tail.
[[vavasis1992-approximation-algorithms-for-indefinite-quadratic]] p.2-7 [[luo2019-new-global-algorithms-for-quadratic]] p.4,p.13-15

Del Pia's 2026 rational-Jacobi result is the strongest recent bit-model
comparison: for fixed integer dimension and fixed number of negative
eigenvalues, it returns objective-range-relative \(\varepsilon\)-approximate
solutions of rational MIQP in time polynomial in the input size and
\(1/\varepsilon\). Its rational spectral preprocessing is directly
relevant. But driving \(\varepsilon\) to the separation needed for exact
rational recovery can require exponentially small \(\varepsilon\), and
the stated polynomial dependence on \(1/\varepsilon\) then becomes
exponential. It does not give expected exact work under linear tilts.
[[pia2026-rational-jacobi-rotations-and-the]] p.1-4,p.15,p.20-21

Burer and Ye's Theorem 3, as stated in the read 2018 arXiv v2, gives
asymptotic high-probability rank-one exactness of the Shor SDP relaxation
for a random class of general QCQPs. The model has a positive-semidefinite
objective matrix and random quadratic constraint matrices, with
feasibility, SDP-interiority, and an added finite-radius constraint; it
does not perturb the linear objective of a fixed indefinite QP. The
conclusion is SDP-relaxation exactness with high probability, not expected
exact rational QP runtime under fixed low inertia. The separate 2020
published article and 2021 correction are both unread because their
journal texts were not available; the correction's impact is unknown.
This comparison is limited to the arXiv-v2 statement and must not be
treated as a checked corrected-journal theorem. [Read arXiv v2](https://arxiv.org/html/1802.02688v2). [[burer2018-exact-semidefinite-formulations-for-a]] p.1

The finite fallback has a general exact-enumeration analogue in prior
work: Burer and Vandenbussche prove finite termination of a KKT/SDP
branch-and-bound algorithm for nonconvex QP under their boundedness and
relaxation hypotheses. That result supplies no expected or polynomial
node bound. The candidate's fallback is simpler face enumeration and is
used specifically to cap the rare bad-conditioning tail.
[[burer2008-a-finite-branch-and-bound]] p.10-12

## Treewidth and graphical-model boundary

Treewidth and negative inertia describe different structure. A sparse
path Hessian can have many negative eigenvalues, while a low-negative-
inertia QP can have a dense interaction graph. Del Pia and Khajavirad give
an exact strongly polynomial dynamic program for rational box QP on
forests, and show strong NP-hardness at treewidth two for unrestricted
box-QP. This is a sharper structural baseline when the interaction graph
is a forest, but it does not yield a smoothed expected result for general
bounded treewidth or arbitrary polytopes.
[[pia2026-treewidth-and-the-complexity-of]] p.3-4,p.20

Bounded-treewidth LP approximations for polynomial optimization by
Bienstock and Muñoz have explicit accuracy dependence and do not return
exact rational optima. Random-reward cavity and correlation-decay results
such as Gamarnik, Goldberg, and Weber's are for finite-action graph
optimization; their guarantees are approximate and rely on discrete
reward models or influence-decay assumptions. These connect naturally to
min-sum and finite-horizon dynamic programming, but do not establish the
continuous exact QP statement.
[[bienstock2018-lp-formulations-for-polynomial-optimization]] p.6-7 [[gamarnik2014-correlation-decay-in-random-decision]] p.8-9,p.11-18

## Assessment

The closest prior-art boundaries are now clear. Expected smoothed global
optimization at fixed low rank exists for randomly rotated low-rank
quasi-concave objectives; exact smoothed optimization with independent
random objective coefficients exists for finite binary feasible sets;
and deterministic low-inertia QP branch-and-bound already gives
fixed-parameter approximation algorithms. The reviewed sources do not
combine the candidate's setting and guarantee: an arbitrary bounded
rational polytope, a fixed indefinite QP with at most two negative
directions, independent small rational-grid linear tilts, a quantitative
global-growth tail, exact rational Turing output, and expected work
controlled by the same-sample exponential fallback.

That comparison is scoped, not a completeness or novelty proof. In
particular, the adaptive-rounding analogy to Beier–Vöcking and the
expected-projection analogy to Kelner–Nikolova are substantial conceptual
antecedents. The feature most likely to distinguish the theorem is the
conversion of a continuous growth tail into expected exact Turing work on
a fixed finite rational perturbation law, including tie atoms and a
same-sample fallback. Random perturbation, low-rank subdivision, and an
exponential fallback are each known ingredients in their own settings.

## Sources and access notes

- Kelner and Nikolova, “On the Hardness and Smoothed Complexity of
  Quasi-Concave Minimization,” FOCS 2007, DOI
  [10.1109/focs.2007.4389517](https://doi.org/10.1109/focs.2007.4389517);
  [full text](https://users.ece.utexas.edu/~nikolova/papers/QuasiConcave.pdf).
- Beier and Vöcking, “Typical Properties of Winners and Losers in
  Discrete Optimization,” STOC 2004, DOI
  [10.1145/1007352.1007409](https://doi.org/10.1145/1007352.1007409).
- Cen and Xia, “A New Global Optimization Scheme for Quadratic Programs
  with Low-Rank Nonconvexity,” INFORMS Journal on Computing 33(4),
  1368–1383 (2021), DOI
  [10.1287/ijoc.2020.1017](https://doi.org/10.1287/ijoc.2020.1017).
  The publisher abstract is available; full text was not retrieved in the
  local KB, so the comparison above is limited to its abstract.
- Burer and Ye, “Exact Semidefinite Formulations for a Class of (Random
  and Non-Random) Nonconvex Quadratic Programs,” arXiv:1802.02688v2,
  [read primary text](https://arxiv.org/html/1802.02688v2). The separate
  2020 journal article, DOI
  [10.1007/s10107-019-01367-2](https://doi.org/10.1007/s10107-019-01367-2),
  and its 2021 correction, DOI
  [10.1007/s10107-021-01684-5](https://doi.org/10.1007/s10107-021-01684-5),
  are paywalled and unread; the correction's effect is unknown.
- Del Pia, “Rational Jacobi Rotations and the Complexity of Approximating
  Mixed Integer Quadratic Programming,” arXiv:2607.29386,
  [primary preprint](https://arxiv.org/abs/2607.29386).
- Del Pia and Khajavirad, “Treewidth and the Complexity of Box-Constrained
  Quadratic Programs,” arXiv:2609.35595,
  [primary preprint](https://arxiv.org/abs/2609.35595).
