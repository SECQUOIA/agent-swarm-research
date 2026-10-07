# Adversarial prior-art addendum: polynomial box recourse

Date: 2026-10-02. This supplements the
[focused prior-art audit](smoothed-polynomial-box-recourse-prior.md) for the
[smoothed polynomial recourse theorem](../new-direction/smoothed-polynomial-box-recourse.md).
The theorem has since passed independent proof review. This addendum narrows
the source comparisons and does not make a publication-priority claim.

## Strongest structural predecessor

Hooker's chapter, [“Convex Programming Methods for Global Optimization”]
(../../literature/papers/hooker2005-convex-programming-methods-for-global/paper.md),
is the direct prior art for the decomposition itself. Its general setup
assumes fixing selected variables makes the remaining continuous problem
convex. It treats continuous selected variables by discretizing them for an
approximate global solution. Theorem 2 and the BBCQ procedure give a concrete
convex quasi-relaxation and terminate for finite selected-variable domains,
but impose additional constraint-function structure; the chapter supplies
no polynomial bound on nodes or time. This fully credits selected-variable
convexification and convex-subproblem global search as established.

The present theorem fits that structural pattern, but its quantitative
guarantee is different. The selected set is a supplied coordinate core of
size `k`; fixing it leaves an arbitrary dense convex polynomial recourse
problem on each rational residual subbox. Independent finite rational noise
on every original linear coefficient yields expected bit work
`8^k [3+(1+k)L/(2 sigma)]^k poly_d(I)`. The theorem requires a charged,
verifiable recourse interface and upper core-curvature bound; it does not
find the core or recognize arbitrary polynomial convexity for free. Its
additional mechanism combines inexact certified recourse intervals, a
finite-law expected core-cell bound, residual-slab exclusion, nonlinear
convex-patch closure, and a same-draw exact fallback. Hooker's result does
not state this perturbation model, expected FPT bound, or exact every-draw
output guarantee.

## Other close solver patterns

Schöbel and Scholz, [“A solution algorithm for non-convex mixed integer
optimization problems with only few continuous variables”]
(../../literature/papers/schobel2014-a-solution-algorithm-for-non/paper.md),
is adjacent global-solver precedent. The publisher abstract describes
geometric branch-and-bound over a small number of box-constrained continuous
variables, with a discrete subproblem solved or bounded at each node. It
reports convergence-rate analysis, transfer of fixed-discrete accuracy, and
finite exact solutions for the truncated Weber and p-median examples. This
has the few-continuous-variables search pattern, but its residual problem is
discrete rather than convex continuous recourse. The article text was not
available in the checked open sources, so theorem conditions and rates are
not treated here as verified.

Standard spatial branch-and-bound, generalized Benders decomposition, and
partial-convex MINLP methods establish the solver vocabulary and broad
architecture. Their generic guarantees are convergence or accuracy-driven
global search; they do not by themselves give an expected finite-perturbation
exact bound in the core dimension and curvature-to-noise ratio. The earlier
[box-stable QP audit](smoothed-box-stable-recourse-prior.md) already compares
the relevant exact forest recourse, conditional-value messages, pruning,
low-dimensional QP, and discrete smoothed-analysis results. Those sources
should retain credit for each component they establish.

Biconvex optimization is a nearby but stronger blockwise condition. Gorski,
Pfeuffer, and Klamroth's [survey]
(https://doi.org/10.1007/s00186-007-0161-1) covers alternating convex search,
the GOP global algorithm, and convex-envelope branch-and-bound. It reports
that alternating search can stop at partial or stationary points; GOP gives
finite `epsilon`-global convergence only under additional compactness,
biconvex objective and constraints, biaffine equalities, qualification, and
multiplier assumptions. The candidate requires convexity only after fixing
its supplied core; its core slices need not be convex, so it is not generally
a biconvex problem. These methods therefore supply useful adjacent solver
prior art, but not the candidate's expected finite-noise exact guarantee.

## Smoothed nonconvex optimization comparison

Cifuentes and Moitra,
[“Polynomial time guarantees for the Burer–Monteiro method”]
(https://doi.org/10.52202/068431-1737), is an important positive precedent
for smoothed global optimization of a nonconvex formulation. Their Theorem 1
gives high-probability approximate optimality for a factorized SDP after
perturbing the cost matrix, under compactness and smoothness/LICQ assumptions
and a rank threshold above the Barvinok–Pataki bound; the iteration count is
polynomial in the dimension and inverse perturbation size. A second stage
perturbs the constraint map to obtain an end-to-end approximate SDP result.
This rules out any broad claim that smoothed polynomial-time guarantees for
nonconvex optimization are new. The guarantee is nevertheless for a special
factorized SDP, is approximate and high-probability, and does not yield exact
rational optimization of every finite-noise sample for dense convex
polynomial recourse.

The candidate's “exact” guarantee has a specific output meaning: in the
usual case a rational restricted box and verified positive Hessian modulus
implicitly specify its unique constrained minimizer; exceptional draws use
an exact algebraic fallback on the same perturbation. It does not promise a
short expanded algebraic-coordinate representation for every draw. Its
perturbation has a fixed finite rational law chosen from the base input and
is independent across all original coordinates; it is not an accuracy-
dependent continuous perturbation or repeated resampling.

## Comparison boundary

The checked sources support a conservative assessment. Partial convexity,
convex residual optimization, low-dimensional branch-and-bound, and
smoothed approximate global optimization each have clear prior art. The
possible advance is their specific combination for fixed-degree continuous
polynomial boxes with a supplied coordinate core and arbitrary certified
convex recourse, including the expected FPT count and exact same-draw output
contract. This search did not find a checked source stating that combination;
the search is scoped and does not establish novelty.

Source access: Hooker's author-hosted chapter is now promoted as open/read
in the local literature package. Schöbel–Scholz is metadata-only; the
publisher abstract was visible, but full text was not retrieved. Gorski et
al.'s author-hosted survey and the Cifuentes–Moitra NeurIPS proceedings PDF
were read online; local source promotion was requested from the sole
literature ingester. No KB or index files were edited for this addendum.
