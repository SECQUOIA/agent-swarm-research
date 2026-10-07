# Removing variable occurrence from conditioned box-QP algorithms

Date: 2026-10-02. Status: a general conditioned-width theorem has now passed
two independent proof/arithmetic reviews and targeted actual DP checks. A
separate feedback-vertex theorem permits nonunique continuous recourse, and
restricted certificate obstructions explain why a change of algorithm was
needed. No external priority claim is made.

## Main outcome: filtered shared grids

The [min-marginal filtering theorem](pruned-coordinate-grid.md) gives an
exact algorithm for rational mixed-integer box QP in

    f(p, max(1,L/g)) poly(I),

where p is the largest supplied decomposition bag, L is the largest
positive diagonal curvature of the summed objective, and g is its global
quadratic-growth constant around the unique optimizer. Approximate
certification to error 2^(-q) takes f(p,max(1,L/g)) poly(I+q). The
polynomial exponents are absolute. Neither occurrence nor a full-Hessian
norm is needed. The growth constant need not be supplied.

The algorithm uses exact shared-coordinate point grids, followed by two
passes of DP to compute every coordinate min-marginal. These provide sound
lower bounds conditional on each adjacent coordinate interval. Discarding
intervals whose bound exceeds a feasible incumbent preserves every global
optimizer. Quadratic growth then confines all surviving coordinate hulls
to radius O(sqrt(n L/g) h), with an additional one for integer coordinates.
At the next mesh h/2, geometric grids require only O(theta^-1 log n) nodes
per coordinate, independently of the requested accuracy. The identity
(log n)^p <= f(p)n makes the table count FPT. A state cap handles
unsuccessful conditioning guesses; dyadic common denominators give the
Turing bound. The certificate retains the complete pruning history.

This resolves the occurrence-free algorithmic question under the unique
optimizer/growth hypothesis, subject to the continuing prior-art audit.
It does not repair the old overlapping-cell certificate. The
individual interpolation, DP, filtering, and reconstruction tools are
classical; the proposed contribution is their conditioned uniform bound.

The [finite-mode corollary](pruned-grid-finite-modes.md) removes fully
enumerated mode labels from the growth metric, so optimal modes can tie.
For an ordinary QP, coordinates with nonpositive Hessian diagonal can be
restricted to two endpoint modes. Projected growth is then required only
in the remaining positive-diagonal coordinates. This endpoint reduction
is standard; its role is to broaden the scope of the filtered-grid bound.

## Complementary outcome: exact forest recourse

There is an exact fixed-parameter algorithm for rational continuous box QP
when a supplied set of r coordinates leaves a forest and the reduced
optimization over those coordinates has useful quadratic growth. Its bit
complexity is

    f(r, max(1,L/g)) poly(I),

with an absolute polynomial exponent, no occurrence parameter, and no
supplied growth constant. Here L is the largest positive diagonal curvature
among the r core coordinates, and g is a growth constant for the core value
function. Approximate optimization to error 2^(-q) has complexity
f(r,max(1,L/g)) poly(I+q).

This handles fans and a clique of r universal hubs joined to an arbitrary
forest, even though each hub may occur in linearly many decomposition bags.
The number of residual continuous variables is unrestricted. The residual
quadratic may be nonconvex and arbitrarily ill-conditioned. Only the
optimal core vector must be unique; the residual optimal set may contain
a continuum.

The [full theorem and proof](fan-exploration.md) include an unconditional
endpoint case, an exact rational forest oracle, a self-contained path
oracle, the actual box count, an unknown-growth stopping procedure, and
targeted verification. The oracle for general forests is the existing
Del Pia--Khajavirad exact box-QP algorithm. The separate
[literature audit](../prior-art/geometric-grid-prior.md) verified that its
strongly polynomial statement includes the Turing model, polynomial
intermediate encoding lengths, and rational optimizer output. The present
work does not claim that oracle as new. The
[mixed-core extension](mixed-core-extension.md) also permits large-domain
integer core variables while keeping the forest residual continuous.

## How the forest result differs from the general theorem

A feedback vertex set is a stronger structural restriction than bounded
treewidth. Its size can grow arbitrarily on a sequence of disjoint cycles,
even though treewidth stays two and an ordinary decomposition has bounded
occurrence. Conversely, the hub families above have small feedback vertex
sets but an unbounded occurrence count in their natural path decompositions.
The general filtered-grid result removes this structural restriction, but
requires growth around a unique full optimizer. The forest theorem instead
needs growth only in the core: its residual optimal set may be a continuum,
and its residual curvature is not part of the parameter. These are distinct
advantages. The earlier
[occurrence-parameter FPT theorem](../geometric-dp/regridded-qp-bit.md)
remains a result about another certificate representation; it no longer
sets the best available algorithmic bound for uniquely optimized box QPs.

## Mechanism of the positive result

Write x=(h,z), with h the core, and

    v(h)=min_z F(h,z).

The feasible box for z is independent of h. If A is the Hessian of F,
then v(h)-h^T A_CC h/2 is concave because it is an infimum of affine
functions of h. Thus the nonsmooth value function inherits a one-sided
curvature bound without needing to construct its potentially large
piecewise-quadratic representation.

For any core box B of coordinate widths w_i, exact residual optimization
at its 2^r corners gives the valid lower bound

    LB(B)=min_corner v - (1/8) sum_i max(A_ii,0) w_i^2.

Independent unbiased corner rounding proves the inequality; off-diagonal
terms cancel in expectation. No value-function derivatives are used.

The algorithm refines isotropic dyadic cubes, clipped to the original
rational core box. At mesh width h_j, a box containing the optimal core
gives an incumbent gap at most L r h_j^2/8. Every box that survives
pruning consequently has a corner within O(sqrt(rL/g) h_j) of that core.
Lattice packing bounds the number of surviving boxes by

    2^r (sqrt(r max(1,L/g))+3)^r

at every level. There are only polynomially many levels in the requested
accuracy bits. Common isotropic widths are essential here: separately
bisecting coordinate intervals of very different original lengths would
introduce an aspect-ratio factor not covered by the claimed parameters.

All corners are rational with polynomial bit length, so the forest oracle
supplies exact rational values and feasible witnesses. Rational QP height
bounds isolate the exact optimum value once the interval is narrow enough.
They also reconstruct the common optimal core. A final forest solve at
that core is accepted only when its feasible objective equals the isolated
optimum. This verifies exactness without trusting a growth estimate.

The fixed-dimensional box-count argument is a standard quadratic-growth
branch-and-bound mechanism; the repository already discusses its
[cluster-free background](../../results/cluster-free-branch-and-bound-constrained-minima.md).
The possible contribution is the exact rational feedback-vertex
consequence with projected curvature and growth, the forest oracle, and
the stated uniform parameterized bit bound. This is narrower than
inventing a new global-optimization principle.

The focused literature audit also identified Theorem 4 of the same forest
QP paper as prior tractability for some sign-restricted fixed-core cases:
it combines nonpositive-diagonal endpoint variables, tractable positive
components, bounded interfaces, and bounded cross rank. In particular,
some instances with a fixed positive-diagonal core and a nonpositive
forest remainder already have a polynomial-time algorithm without the
growth assumption. Its arrangement bound has a rank-dependent polynomial
exponent. The present result must therefore be compared on arbitrary
diagonal signs, its uniform FPT bound, and projected conditioning; it is
not a first claim of fixed-feedback-vertex tractability in every special
case. The full comparison remains with the literature audit.

## Why weighted reconstruction alone does not repair the old proof

The independent [fan-certificate obstruction](weighted-drift-exploration.md)
gives a rational nonconvex box QP on a fan with

    ||Hessian F|| <= 3/2,       F(x)>=||x||^2/4,

and optimum zero. In the existing path decomposition with canonical
coefficient allocation, the prescribed slopes vanish at the exact center
zero. A sequence of locally permitted hub copies can move from zero to
one, while the linear hub cost is paid only at the root. Its configuration
value is at most -1/64, even at arbitrarily fine base meshes when the
grading ratio is fixed and the fan is sufficiently long.

This is an actual lower-bound gap. Choosing a different representative of
the copies, or weighting an error norm differently, does not change it.
It therefore rules out removing occurrence solely by reanalyzing the same
configuration set and lower-bound value.

The limits are essential. Boundary-touching intersections are used by the
construction. Strengthening both relevant incidence rules to exclude such
pairs blocks this particular witness. The result concerns the specified
closed-cell certificate and allocation at a fixed center; it is not an
iterative-runtime lower bound, an optimization hardness result, or an
obstruction to other decompositions, allocations, or convex models. The
fan is solved by the positive feedback-vertex algorithm above; its hub is
even in the endpoint-only curvature case.

## What the broader weighted approach established

Two useful algebraic observations reduce the problem but do not finish it.
First, canonical allocation of Hessian entries to bags gives

    sum_t ||H_t v_Vt||^2 <= p ||H||_2^2 ||v||^2.

Second, for a graph of degeneracy at most w,

    || entrywise_abs(H) ||_2 <= (1+2 sqrt(w)) ||H||_2.

For the second claim, orient off-diagonal edges with outdegree at most w,
write H=diag(H)+B+B^T, and apply rowwise Cauchy--Schwarz to |B|:
its squared norm is at most w times the largest squared column norm of H.
Treewidth at most w implies such an orientation. These estimates avoid
high-degree losses in some Taylor copy terms.

They do not control the entire certificate error. Isotropic bag grading
can give many private coordinates coarse intervals merely because they
share a bag with one distant hub. Summing affine-Taylor relaxation errors
then broadcasts that hub's error to many bags. Stronger local convex
models can avoid some of this loss: for an edge Hessian with a small
coupling and a positive leaf diagonal, the negative eigenvalue is of the
order of the squared coupling, while an absolute-norm affine Taylor
bound charges its first power. Turning that observation into a uniform
global algorithm through those particular local models would still require
a compatible allocation, grading rule, and aggregate proof. The
[positive-overlap study](positive-overlap-exploration.md) proves that copy
drift can be removed while a separate isotropic relaxation error persists,
even on a strongly convex star. It also establishes a full-domain tensor
cover obstruction for coordinatewise grading.

The filtered point-grid algorithm takes a different route: exact shared
coordinates remove copy drift, and certified domain reduction prevents the
tensor's logarithmic scale factor from depending on requested precision.
It therefore bypasses these obstructions without replacing occurrence by
an unspecified weighted parameter.

## Verification

For the main filtered-grid theorem, the command

    python research-20261002/new-direction/check_pruned_grid.py > research-20261002/new-direction/check_pruned_grid-results.json

passed nine instances and 70 adaptive stages, with 26,589 bag-table states
and 526 pruned intervals. A separate finite-grid oracle checked every
min-marginal on ten selected grids covering 21,034 assignments. The
[main note](pruned-coordinate-grid.md) records the fixtures, independent
global-optimum checks, explicit two-bag message trace, and verification
limits. Both mathematical and arithmetic reviews found no substantive gap.

The forest-recourse proof received a fresh adversarial review covering
the corner lower bound, isotropic packing, pruning, exact recovery,
polynomial bit exponent, and the elementary path oracle. Targeted exact
checks passed 54 path instances against active-face enumeration, 144
core-box inequalities, and 300 samples of a uniformly conditioned
nonconvex fan family. The fan example illustrates the assumptions; its
planted zero optimum is not a difficult benchmark.

The additional targeted command

    python3 -B research-20261002/new-direction/check_core_box_bb.py

passed 14 actual adaptive-refinement instances, generating 930 boxes and
855 exact residual calls. At every level it checked the returned objective
interval against independent full active-face enumeration and checked the
mesh-error bound. Cases included indefinite residual slices, a core-box
aspect ratio of 1,024, a unique core with continuum residual optima, and
the nonpositive-core-curvature case that certifies optimality at the root.
The checker uses exhaustive residual enumeration as an independent small
reference; it does not implement or benchmark the cited forest oracle.

The obstruction received a separate geometric review and exact rational
checks of 105 shell cases covering 11,718 cells, including 69 negative-gap
cases. Its proof, rather than those finite checks, establishes the general
counterexample. Actual commands and review limits are recorded in the two
linked derivations. No project-wide verification or CI inspection was run.
