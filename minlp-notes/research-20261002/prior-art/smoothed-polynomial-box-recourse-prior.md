# Prior-art audit: smoothed polynomial optimization with convex residual recourse

Date: 2026-10-02. This is a focused comparison of the
[polynomial box-recourse theorem](../new-direction/smoothed-polynomial-box-recourse.md).
The theorem has since passed its independent review and targeted checks.
This note is a literature comparison, not an independent proof review or a
publication-priority claim.

## Candidate and precise assumptions

The candidate minimizes an explicit rational polynomial of fixed degree on
the continuous unit box. A supplied coordinate core has size `k`; fixing
that core leaves a globally convex polynomial in all residual coordinates
and on every rational residual subbox. The core coordinates have a supplied
upper diagonal-curvature bound `L`. One base-chosen finite rational law
perturbs every linear coefficient independently. The claimed expected bit
work is

```text
8^k [3+(1+k)L/(2 sigma)]^k poly_d(I).
```

This is an FPT bound in the joint numerical parameters `k` and `L/sigma`;
for fixed `k`, it is polynomial in input length when the numeric ratio is
polynomially bounded. It assumes no growth or uniqueness promise. It solves
every sampled instance exactly in an implicit form: usually a rational box
patch with a verified positive Hessian modulus whose unique constrained
minimizer denotes the optimizer; the same-draw algebraic fallback handles
exceptional samples. It does not expand algebraic optimizer coordinates,
optimize the unperturbed objective, or allow integer residual coordinates.

The residual convexity and curvature bounds are substantive input
conditions. They need tractable, charged certificates; convexity of an
arbitrary polynomial is not assumed to be efficiently recognized. Dense
residual interactions and large mixed derivatives are permitted. The
expected core-cell count depends on `L/sigma`, while mixed and residual
derivatives affect the polynomial-bit localization cutoff and precision.
They are not absent from the running time. The noise on residual
coefficients also matters to the current global-growth and active-bound
closure proof, so this theorem does not establish a core-only perturbation
result.

## Partial convexity and global search are established ingredients

Hooker's primary chapter, [“Convex Programming Methods for Global
Optimization”](https://doi.org/10.1007/11425076_4), is a direct conceptual
antecedent. It formulates global problems where fixing selected variables
makes the remaining problem convex; continuous selected variables are
discretized to obtain an approximate global solution (§1). Its Section 7
branches over selected values and uses convex quasi-relaxations; Theorem 2
gives a valid relaxation for particular convex/semihomogeneous constraint
structures (§7). This
credits the core/convex-residual decomposition and convex-subproblem search
as established methods. Hooker does not give the candidate's random
coefficient law, expected FPT dependence on `k` and `L/sigma`, exact
every-atom implicit output, or same-draw fallback. The theorem's concrete
residual-convex polynomial class is not the special quasi-relaxation class
in Hooker's Theorem 2.

Once the core is fixed, the recourse subproblem in the candidate is an
ordinary convex polynomial minimization over a rational box. Grötschel,
Lovász, and Schrijver's weak-separation-to-weak-optimization theorem gives
the standard rational ellipsoid route; the project has already recorded
the exact Turing-model statement and capped-epigraph construction in its
[convex-patch evaluation lemma](../new-direction/convex-patch-evaluation.md)
and [sparse polynomial audit](sparse-smoothed-polynomial-prior.md). This
oracle needs neither strict nor strong convexity. The candidate's lower
value interval and feasible rational completion are a standard use of
certified convex optimization, not a new convex minimization algorithm.

Function-valued conditional minima, restricting optimization to subboxes,
incumbent pruning, and spatial branch-and-bound are also established
solver techniques. The existing
[box-stable QP audit](smoothed-box-stable-recourse-prior.md) already checks
Del Pia–Khajavirad's exact forest-QP messages, continuous graphical-model
messages, OBBT, and low-dimensional QP search. The new polynomial theorem
does not make those mechanisms new. Its direct change from the QP result is
that certified approximate lower and feasible upper values suffice even
when conditional optima and values are irrational; the proof then combines
these intervals with finite-noise core-cell counting, excluded-region
tests on every residual slab, a nonlinear Hessian closure test, and a
same-draw exact fallback.

## Relation to low-rank and negative-inertia methods

Vavasis's low-negative-eigenvalue method and Luo, Bai, Lim, and Peng's
ADMBB algorithm are close global-optimization precedents for quadratic
objectives. They isolate a low-dimensional negative-curvature subspace,
branch over that subspace, and solve convex quadratic relaxations. Their
guarantees are accuracy-dependent approximations, with a dimension-`r`
partition count that depends polynomially on inverse accuracy; they do not
provide a finite-noise expected exact bit bound. The candidate has an
original-coordinate core and a convex residual Hessian block. For a
quadratic, the residual PSD condition bounds negative inertia by `k`, and
the negative eigenspace gives the usual fixed PSD correction of rank at most
`k`. For a general polynomial, the pointwise Hessian can have negative
inertia at most `k` while its negative eigenspace varies with the point;
there need not be a fixed PSD quadratic correction of rank at most `k`.
[[vavasis1992-approximation-algorithms-for-indefinite-quadratic]]
Theorem 2, pp. 2–7; [[luo2019-new-global-algorithms-for-quadratic]]
Theorem 3.3, pp. 13–15

The project's
[separable low-rank nonlinear method](../new-direction/approximate-convex-recourse.md)
and [separable smoothed method](../new-direction/smoothed-mixed-separable-closure.md)
are nearby nonlinear work. They handle a separable convex base plus a
fixed low-rank concave quadratic, using scalar convex recourse. The
approximation result also assumes projected quadratic growth; the smoothed
result handles a different noise model and product-domain structure. They
do not supply a solver for arbitrary dense convex polynomial residuals.
Conversely, the present theorem handles only continuous boxes and requires
convexity after fixing its supplied coordinate core; it does not inherit
the separable theorem's unrestricted integer coordinates.

The distinction between a coordinate core and a fixed low-rank quadratic
correction is real. The project's checked
[rank-separation example](../new-direction/polynomial-recourse-rank-separation.md)
has one core coordinate, dense quartic residual, and at most one negative
Hessian eigenvalue at every point, while every fixed PSD quadratic shift
that convexifies the full polynomial has rank at least the residual
dimension. This rules out treating every such instance as a fixed
low-rank concave-quadratic model. It is a representation separation, not a
hardness proof and not a claim against all nonlinear difference-of-convex
representations.

## What the focused comparison supports

The literature establishes partial-convex variable elimination, convex
optimization of the residual, low-dimensional global branching, exact
forest-QP recourse, and smoothed exact optimization on narrower discrete or
separable classes. The candidate's possible contribution is the specific
composition: independent finite perturbations on all original coordinates,
expected FPT work in the coordinate-core dimension and its positive
curvature/noise ratio, certified approximate convex recourse on arbitrary
rational residual subboxes, global excluded-region closure, and exact
implicit optimization for every draw without growth or uniqueness input.
This comparison does not establish that no equivalent result exists.

Hooker's author manuscript has been read and stored in the local
[source package](../../literature/papers/hooker2005-convex-programming-methods-for-global/).
The QP, low-rank, ellipsoid, and separable comparisons are from primary
texts already read in the local source packages and linked audits. No
KB/index changes were made by this audit.
