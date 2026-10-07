These targeted experiments support the geometric-grid construction in the
adjacent theorem.md. All checks in exact_checks.py and grid_geometry_checks.py
use fractions.Fraction. The separate float_scale.py is a timing prototype;
none of its floating-point bounds is a certificate.

Run from the repository root with Python 3.10 or later:

    python3 research-20261002/geometric-dp/checks/exact_checks.py
    python3 research-20261002/geometric-dp/checks/grid_geometry_checks.py
    python3 research-20261002/geometric-dp/checks/float_scale.py

The checked-in exact-results.json, geometry-results.txt, and float-results.json
record these commands' outputs on 2026-10-02. Elapsed times are observations
from one local run. No project-wide verification or CI inspection was run.

Exact model certificates

Every model has a rooted tree and the objective

    F(x) = offset + sum_i [a_i z_i^2 - k_i z_i^4 + m_i z_i]
           + sum_edges(i,j) w_ij (z_i-z_j)^2,  z_i = x_i-s_i.

The supplied s is feasible, all k_i and w_ij are nonnegative, and each linear
term is nonnegative throughout its coordinate interval. Write
R_i = max(|lower_i-s_i|, |upper_i-s_i|). The exact constants are

    cg = min_i (a_i-k_i R_i^2) > 0,
    L  = max_i (2 a_i + 2 sum_{j adjacent to i} w_ij).

The inequality a_i z_i^2-k_i z_i^4 >= (a_i-k_i R_i^2) z_i^2 proves
F(x)-F(s) >= cg ||x-s||^2 throughout the full continuous box. Edge squares
and the boundary linear terms are nonnegative. Thus s is the unique global
minimizer and F(s)=offset. Also F_ii = 2a_i-12k_i z_i^2+2 sum_j w_ij <= L,
which proves coordinate semiconcavity. L need not bound the absolute Hessian
or the Lipschitz constant of the whole gradient. The negative quartic example
has negative coordinate curvature near an endpoint and is truly nonconvex.

The six model families cover a large-linear-term boundary optimum, a nonconvex
quartic chain, two pure integer problems, a mixed chain, and a five-node
branching tree. Continuous centers and optima include non-dyadic fractions.
The integer models have integral centers, optima, and interval endpoints.

For each of 42 stages, exact_checks.py compares tree elimination with exhaustive
enumeration of the full corrected grid. Across all stages this enumerates
142,348 assignments. It also checks the analytic optimum bracket, reconstructed
DP assignment, the vertex and summed correction bounds, the contraction
recurrence, and the halving invariant. A total of 294 independent product
endpoint-rounding laws verifies unbiasedness, the semiconcavity expectation
inequality, and coverage of rounding loss by endpoint penalties. Two additional
scalar midpoint fixtures attain equality in the rounding bound and detect an
insufficient penalty coefficient. Integer unit-gap fixtures check omission of
only those intervals that contain no missing feasible integer.

The large integer example has 20,001 feasible values on each of two axes. Its
theoretical identification threshold is reached at stage 15. At stage 16,
both grids have 143 values and the exact lower and upper bounds coincide.
The check therefore exercises finite exact stopping while retaining compressed
integer grids.

grid_geometry_checks.py separately sweeps 250 grids, including singleton axes,
boundary centers, non-dyadic centers, and clipping. It checks 1,883 vertices,
four explicit boundary fixtures, 36 rational cases for the contraction
constants, and three documented input rejections. Some geometry-only slopes
exceed the theorem's theta restriction; those checks concern the local gap
inequality and do not assert the contraction theorem for those slopes.

The floating-point prototype runs 13 stages on binary-tree quadratics with
16, 64, and 128 continuous variables. At the last stage, the largest grids
have 96, 97, and 97 points, respectively. The output records numerical bounds,
pair-table evaluation counts, and elapsed times. These are size and timing
observations, not certified numerical results or an asymptotic complexity test.

Scope and limitations

These finite checks do not prove the general theorem. They exercise scalar
tree nodes (treewidth one), analytically known unique optima, and box domains.
They do not cover arbitrary tree decompositions, general constraints, or the
cost of obtaining valid model constants. Exact fractions prevent arithmetic
roundoff in the small certificate checks; they do not establish bit-complexity
bounds. The floating-point prototype has no interval enclosure or directed
rounding and must not be used to claim a certified bound.
