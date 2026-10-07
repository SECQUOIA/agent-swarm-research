# Prior-art audit: smoothed exact QP with box-stable recourse

Date: 2026-10-02. This focused audit compares the completed
[box-stable recourse theorem](../new-direction/smoothed-box-stable-recourse.md)
with exact sparse QP dynamic programming, deterministic core search, and
smoothed parameterized optimization. The theorem has an independent
mathematical review; this note is a literature comparison, not an independent
proof review or publication-priority claim.

## Claim and assumptions

The input is a rational continuous box QP on `[0,1]^n`. A supplied set of
`k` core coordinates has upper diagonal curvature `L`. The essential oracle
assumption is stronger than one exact solve of the residual problem: after
fixing any rational core vector and restricting every other coordinate to
any rational subinterval, an algorithm must return an exact rational global
minimizer and value in polynomial bit time with an absolute input-length
exponent. Empty restricted boxes must also be detected. The theorem then
uses one base-input-selected finite rational uniform law for independent
linear objective perturbations. It returns an exact optimizer and value on
every draw, with expected work bounded by

`8^k [3+(1+k/2)L/(2 sigma)]^k poly(I)`.

Thus the displayed bound is FPT in the joint parameters `k` and `L/sigma`;
for fixed `k`, it gives polynomial work in the input length when `L/sigma`
is polynomially bounded. It is not a treewidth-only theorem, and a binary
encoding for an extremely small `sigma` does not itself make the expected
work polynomial. The proof needs only the
curvature of the core conditional value and the box-stable exact recourse
interface. The excluded-region certificate makes up to `2|R|` restricted
recourse calls; a same-draw exact face-enumeration fallback handles draws
that do not close by the base-chosen cutoff.

## Exact conditional optimization is established on forests

Del Pia and Khajavirad give the closest exact residual oracle. Their
Theorem 1 represents the value function of a rational continuous box QP on
a forest by concave piecewise-quadratic messages and solves the problem by
leaf-to-root dynamic programming in `O(n^2)` arithmetic operations and
comparisons. Their strong-polynomial definition accounts for polynomial-bit
intermediate values in the Turing model, and Lemma 19 recovers a rational
optimizer of polynomial encoding length. Fixing core coordinates only
changes residual linear and constant terms. Restricting residual variables
to rational subintervals keeps the same forest box-QP class. Therefore this
existing algorithm does satisfy the theorem's box-stable recourse interface
when deleting the core leaves a forest.
[[pia2026-treewidth-and-the-complexity-of]] Theorem 1, Lemmas 15–19

This gives a concrete corollary parameterized by the size of a supplied
feedback vertex set and `L/sigma`. The forest algorithm is the established
recourse primitive; the proposed addition is the random core search,
expected count of near-optimal core grid tuples, and exact excluded-region
closure. The result does not imply FPT in interaction treewidth alone.
Del Pia and Khajavirad prove strong NP-hardness for unrestricted box QP at
treewidth two, so any wider claim must retain a structural restriction,
conditioning premise, or tractable recourse condition. That hardness
result does not rule out the present FVS-parameterized smoothed theorem.
[[pia2026-treewidth-and-the-complexity-of]] Theorem 3

The project's earlier deterministic
[feedback-vertex-set algorithm](../new-direction/fan-exploration.md) uses
the same basic core/forest-value-function decomposition. It gives exact
FPT optimization under a unique projected optimum and a quadratic-growth
promise, with a bound depending on the core curvature-to-growth ratio.
That is the closest internal algorithmic predecessor. The smoothed theorem
does not require growth or uniqueness as input; it instead pays for
conditioning through `L/sigma`, expects over a finite perturbation law,
and works whenever the residual subproblem has the stated exact box-stable
oracle, not only when it is a forest.

## Other conditional-message and domain-filtering precedents

Function-valued conditional minima are standard in dynamic programming.
Hoang, Yeoh, Yokoo, and Rabinovich's EC-DPOP exactly eliminates continuous
variables for linear or quadratic utilities on tree-structured graphs.
Their messages are separator value functions. AC-DPOP extends to smooth
utilities by discretization and gives a gradient-and-mesh approximation
bound. This is direct precedent for exact conditional messages and
continuous graphical-model DP, but their stated exact class is tree
structured and linear/quadratic; the approximate guarantee is not an
expected exact bit-time result for a nonconvex box QP.
[[hoang2020-new-algorithms-for-continuous-distributed]] pp. 1, 6–7

In the candidate, the restricted recourse minima play two roles. They
evaluate the conditional value at core grid points, and they certify that
every conditional optimizer over the surviving core hull lies inside a
small residual box. Solving optimization problems on restricted domains is
also a standard component of optimization-based bound tightening and
spatial branch-and-bound. Belotti et al. describe OBBT and incumbent-based
domain pruning for nonconvex MINLP. Those methods establish the operations
as standard solver practice; their paper does not give this exact
conditional-value separation test, a finite-noise expected node bound, or
the core-dimension FPT estimate. This is a difference in guarantee, not a
claim that restricted optimization or bound tightening is new.
[[belotti2009-branching-and-bounds-tightening-techniques]] pp. 2–12

The excluded-region certificate specifically needs exact **global** values
on every rational residual subbox. A feasible completion or a local NLP
minimum cannot serve as the lower bound. It also uses uniform Lipschitz
control in the core variables to transfer restricted values from one
corner to the whole surviving hull. This is stronger than an unrestricted
conditional minimizer, a local message, or ordinary feasible-region
propagation.

## Smoothed and low-dimensional optimization comparisons

Beier and Vöcking's STOC 2004 paper is a close perturbation-model analogue:
independent random objective coefficients yield winner-gap bounds and an
adaptive-precision algorithm for finite discrete optimization. It
establishes anti-concentration plus certification as a standard pattern,
but a continuous box has no positive gap between the best point and a
second-best point. Their discrete analysis does not provide the candidate's
continuous conditional-value cell count or restricted-box closure. The
readable source is the 2004 conference paper; the separately catalogued
2006 journal package is metadata-only and is not the source for this
comparison. [[beier2006-typical-properties-of-winners-and]] pp. 3–4, 9–10

Röglin and Vöcking's smoothed integer-programming results are another
important distance-to-tractability comparison. Under independent
bounded-density perturbations they bound winner gaps and use adaptive
rounding with a pseudopolynomial solver. Their polynomial smoothed-time
definition is a high-probability tail bound and an expected-power
condition, not ordinary expected running time. Their feasible decisions
are integer-valued; the result does not solve a continuous recourse
problem or certify a surviving continuous core region.
[[roglin2007-smoothed-analysis-of-integer-programming]] pp. 3–8, 21–28

Kelner and Nikolova give expected-time smoothed minimization for a
constant-rank quasi-concave objective over an integral polytope after
randomly rotating its low-rank objective subspace. This is strong prior
art for expected global optimization with a low-dimensional structural
parameter. The objective class and perturbation are different: arbitrary
independent additive linear noise on a fixed indefinite QP is not a random
rotation, and their theorem is not an exact rational Turing guarantee.
[[kelner2007-on-the-hardness-and-smoothed]] Theorem 2.9

Deterministic low-negative-inertia algorithms by Vavasis and Luo et al.
already use low-dimensional branching with convex QP recourse and certify
global approximations. Their work scales polynomially with inverse
accuracy for fixed negative inertia; it does not yield this finite-noise
expected exact result or the restricted-box closure mechanism. This
candidate has a different parameter: the core is a supplied coordinate
deletion set, which yields a particularly direct recourse oracle. A small
negative eigenspace need not give a small coordinate deletion set.
[[vavasis1992-approximation-algorithms-for-indefinite-quadratic]] pp. 1–7
[[luo2019-new-global-algorithms-for-quadratic]] pp. 1–3, 10–11

## Assessment boundary

The prior art establishes the main pieces separately: exact piecewise-
quadratic messages for forest box QPs; function-valued messages for
structured continuous optimization; optimization-based domain pruning;
deterministic low-dimensional global QP approximation; and smoothed
isolation for discrete optimization. The possible contribution is the
composition for a continuous box QP with a core and an exact recourse
solver stable under every rational coordinate restriction: conditional
semiconcavity gives a finite-law expected core-cell count, exact excluded
region tests close a local convex patch, and a fixed base-only cutoff plus
same-draw fallback gives exact output on every draw.

The closest concrete scope is FVS-deleted forests. It is stronger than the
deterministic internal FVS result in that it has no QG input, but it pays a
curvature/noise ratio and assumes a finite smoothed law. It is broader in
recourse oracle class only when another exact polynomial-bit algorithm is
known to solve all rational residual subboxes. It is not a general
treewidth algorithm, a stochastic-programming result over random
scenarios, or a new form of conditional value function. The focused
comparison found no checked source stating this same expected exact bound;
that search is not exhaustive and does not establish priority.

The sources used here are already readable in the local project packages
or prior-art notes: Del Pia–Khajavirad (2026), Hoang et al. (2020), Belotti
et al. (2009), Beier–Vöcking (2004), Röglin–Vöcking (2007), Vavasis (1992),
and Luo et al. (2019). Their primary-source locators were checked in the
existing audits. No new source or full-text request was needed, and no KB
or index files were edited. A targeted inline Python check found no trailing
whitespace and verified that the audit's local Markdown targets exist. No
project-wide checks or CI inspection were performed.
