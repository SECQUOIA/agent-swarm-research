# Prior-art audit: sparse optimization on monotone implicit polynomial graphs

Date: 2026-10-02. This audit now compares the full model in
[`smoothed-implicit-graph-constraints.md`](../new-direction/smoothed-implicit-graph-constraints.md),
not the earlier stage-actuator sketch. It is a focused source comparison,
not theorem validation or a publication-priority claim.

## The model and its boundary

The feasible set has retained coordinates in a bounded rational mixed
product box and dependent continuous coordinates `y_j` defined separately
by equations `q_j(t_{S_j},y_j)=0`. Each fixed-degree polynomial uses only
its own dependent coordinate. A supplied positive lower bound on
`partial_y q_j` and endpoint sign brackets hold over the entire real hull
of the retained box and the full interval for `y_j`. Thus each equation
defines one smooth scalar graph over every retained point. There are no
other constraints. Objective factors and graph constraints are covered by
a supplied tree decomposition; replacing each dependent variable in its
scope by the retained support gives the expanded bags used by the algorithm.

This is broader than an affine-state actuator recurrence: the retained
supports can overlap arbitrarily, and no stage ordering or acyclic
dependency graph among retained coordinates is assumed. It remains much
narrower than general coupled polynomial constraints. In particular, each
dependent variable has its own one-dimensional monotone equation, its
interval is globally bracketed for every retained point, and the equation
has no other dependent variable in it. Extra nonredundant constraints or
set-valued fibers are outside the model.

## Closest solver precedents

Wilhelm, Le, and Stuber (2019) are the closest checked source on implicit
state elimination inside global dynamic optimization. They discretize
stiff ODEs with implicit integration, use validated interval bounds and
implicit-function relaxations for a unique state branch, and apply spatial
branch-and-bound. This establishes implicit elimination, certified branch
bounds, and sparse relaxations as existing methods. Their target is a
numerical ODE discretization; the paper does not state an expected bit-time
bound for a finite law of independent linear objective perturbations or an
expected sparse bag-cell count. [[wilhelm2019-global-optimization-of-stiff-dynamical]]
pp. 8–12

Chachuat, Singer, and Barton give deterministic global decomposition for
mixed-integer dynamic optimization with nonconvex ODE subproblems. Their
primal/convex-lower-bound/master method has finite-tolerance global
guarantees and avoids enumerating every discrete design in its case study.
It is direct prior art for globally bounding dynamic models with discrete
decisions, but uses ODE relaxations and deterministic outer approximation,
not globally invertible scalar polynomial graphs or a smoothed expected
treewidth bound. The readable primary source is the 2004 AIChE version of
the 2005 journal article. [[chachuat2005-global-mixed-integer-dynamic-optimization]]
pp. 2–6

The project's [explicit polynomial graph result](../new-direction/smoothed-polynomial-graph-constraints.md)
eliminates triangular equations by substitution. Its
[polynomial-actuator result](../new-direction/smoothed-polynomial-actuator-dynamics.md)
eliminates affine-state recurrences with polynomial actuators by a backward
adjoint. Those are closer algorithmic ancestors: both reduce to a sparse
polynomial objective on free box variables and inherit the box algorithm.
Neither handles a general monotone implicit graph with algebraic, rather
than polynomial, pullback terms for dependent-coordinate noise.

Hoang, Yeoh, Yokoo, and Rabinovich's EC-DPOP exactly eliminates continuous
variables for linear or quadratic utilities on tree-structured constraint
graphs; its UTIL messages are separator value functions. Their AC-DPOP
discretizes smooth differentiable utilities and gives a gradient-and-mesh
error bound. These establish exact conditional messages and approximate
continuous message passing as classical. They do not provide the candidate's
finite-noise expected cell count, rational precision-controlled implicit
graph oracle, or exact every-draw completion. [[hoang2020-new-algorithms-for-continuous]]
pp. 3–7

## Ingredients versus the proposed composition

Monotonicity and the global brackets give a unique scalar root. Fixed-degree
univariate root isolation and implicit differentiation are standard; the
separate [oracle-interface proof](../new-direction/implicit-graph-oracle-interface.md)
accounts for their rational precision cost, uniform derivative bounds, and
implicit output representation. Those algebraic tools alone do not give a
sparse global optimizer. The algorithmic step is to condition on the noise
of dependent coordinates. The retained-coordinate perturbations remain
independent, while the pullback objective has a certified coordinate
curvature bound uniform over the conditioned noise. This permits the
existing sparse near-optimal-cell count and DP to run on the retained box.

The product-domain reduction depends on full-hull brackets. A lower bound
on `partial_y q_j` without those brackets would only give local branches;
it would not establish that every retained vector has a feasible graph
point. Similarly, curvature of the ambient polynomial objective is not
enough: the required `L` bounds the second derivatives after substitution,
including derivatives contributed by dependent-coordinate noise. These
are substantive input promises, and their verification cost must be
included if the theorem is presented as a certified input algorithm.

Qualitative genericity is not new. After fixing the finite integer labels,
the graph chart gives smooth semialgebraic objectives on compact boxes.
Lee and Phạm's generic-tilt results are relevant to generic uniqueness,
strict complementarity, and local growth in regular semialgebraic programs;
on a compact domain, local quadratic growth plus uniqueness yields some
global quadratic-growth constant. For a finite union of label slices,
tie-breaking between distinct slices must also be accounted for. None of
these qualitative facts provides a quantitative tail, a finite-grid atom
bound, the uniform implicit-oracle bit complexity, or the expected solver
work. The finite-law algorithm should therefore be compared on that
quantitative combination, not on generic uniqueness alone.
[[lee2017-generic-properties-for-semialgebraic-programs]] Theorem A,
pp. 3–4; Remark 1.1, p. 5

Exact real-algebraic optimization of the polynomial graph description is
also a standard fallback mechanism. The project's
[finite-law audit](polynomial-pruned-grid-prior.md) records the relevant
fixed-block quantifier-elimination and exact-output sources. Adding the
separate equations and interval constraints to that domain formula is a
representation-level application; it does not by itself give the
candidate's sparse expected runtime. The fallback's sampled-coefficient
bit lengths must remain separate from the base-only sampling budget.

## Comparison boundary

The checked literature establishes implicit-function elimination and
validated global search in dynamic models, exact function-valued messages
for special continuous factor graphs, sparse polynomial box optimization,
and qualitative genericity under linear tilts. The project's explicit
graph/actuator results establish the sparse-box method for triangular and
affine-state special cases. The current implicit-graph candidate composes
these ingredients for globally bracketed scalar algebraic graphs, with
noise conditioning, uniform reduced curvature, sparse DP, and exact
algebraic fallback.

The strongest defensible distinction is that full composition and its
finite-bit expected bound under a preselected finite independent-noise law,
not implicit elimination, global branch-and-bound, or conditional messages
in isolation. The search was focused and does not prove novelty. Both the
monotonicity/bracket certificates and the post-substitution curvature bound
are required assumptions; broader coupled constraints are not covered.

Primary texts checked: Wilhelm et al. (2019), Chachuat et al. (2004/2005),
Hoang et al. (2020), and the cited local Lee–Phạm and real-algebraic-
geometry sources. The actual generalized theorem and reviewed oracle
interface were read for this comparison. No KB or index files were edited;
no project-wide checks or CI inspection were performed.
