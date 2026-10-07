# Prior-art audit: constrained sparse polynomial MINLP extensions

Date: 2026-10-02. This is a focused comparison of two reviewed extensions:
the polynomial graph-constraint pullback and the affine-state,
polynomial-actuator reduction. Both inherit the expected exact sparse-box
algorithm. This note classifies the reductions and the closest checked
solver precedents; it does not claim either elementary elimination step as
new.

## What the candidate covers

The [graph-constraint corollary](../new-direction/smoothed-polynomial-graph-constraints.md)
handles triangular polynomial equalities `z_j = P_j(t,z_<j)` when their
degree, number of parents, and dependency depth are fixed, all dependent
output bounds are redundant, and the supplied decomposition covers every
objective-factor and equality scope. Substitution produces a bounded-degree
polynomial objective on a mixed product box in free coordinates. Expanding
each bag to include the free ancestors of its variables preserves a valid
decomposition, with a stated bag-size increase bounded by the maximum
ancestor count. The expected exact algorithm is the sparse polynomial box
algorithm applied to that pullback.

The [actuator-dynamics result](../new-direction/smoothed-polynomial-actuator-dynamics.md)
is narrower in its constraints and different in its elimination. Its state
equations are affine in the state, the control response is a fixed-degree
univariate polynomial, and the objective is affine in dependent states
plus a sparse fixed-degree polynomial in controls and the initial state.
State intervals must be invariant and hence redundant. A backward adjoint
recurrence substitutes the state costs into unary control-polynomial terms.
After conditioning on the state-noise coefficients, the retained control
and initial-state coefficients remain independent on the original finite
grid. The result is again a sparse polynomial box instance.

These hypotheses are material. Neither construction solves general
polynomial constraints over a sparse graph. The graph case does not cover
extra nonredundant output bounds, cyclic or implicit constraints, or
arbitrary integer-affine coupling. The actuator case does not cover
nonlinear predecessor fibers, path constraints, or general state costs.
The project’s checked counterexamples show that a direct conditional-value
curvature argument can fail even for simple invariant nonlinear dynamics.

## Closest checked precedents

### Function-valued dynamic programming

Hoang, Yeoh, Yokoo, and Rabinovich, “New Algorithms for Continuous
Distributed Constraint Optimization Problems,” AAMAS 2020, pp. 502–509,
[DOI 10.5555/3398761.3398823](https://doi.org/10.5555/3398761.3398823),
is the closest continuous message-passing precedent. Their EC-DPOP
algorithm exactly eliminates continuous variables for linear or quadratic
utilities on tree-structured constraint graphs. UTIL messages are functions
of separator variables, and projection minimizes over the eliminated
variable. Their AC-DPOP handles general smooth differentiable utilities by
discretization and local moves. Theorem 5.2 bounds its utility error by
`|F|(m + |A| k alpha delta) delta` in their notation; the bound depends on
the number of utility functions, agents, update count, learning rate, and
discretization step (pp. 6–7).

This is a direct precedent for conditional value messages and exact
elimination on a tree. It does not give bit-polynomial complexity for
arbitrary polynomial message representations, independent random objective
coefficients, or the candidate's exact every-draw output and same-draw
fallback. Its approximate error bound is global and does not furnish the
specific per-corner feasible completion and certified recourse interval
needed by the local-error interface in
[`local-error-recourse-interface.md`](../new-direction/local-error-recourse-interface.md).
This comparison separates a known message-passing mechanism from the new
certification requirement; it does not imply that all other continuous
message methods lack such an oracle.

### Sparse polynomial optimization

Faenza, Muñoz, and Pokutta, “New Limits of Treewidth-Based Tractability in
Optimization,” *Mathematical Programming* 191 (2022), 559–594,
[DOI 10.1007/s10107-020-01563-5](https://doi.org/10.1007/s10107-020-01563-5),
give a width-based approximate LP for polynomial optimization. Theorem 3.3
has formulation size `O((2 rho/epsilon)^(omega+1) n log(rho/epsilon))`
for degree `rho` and intersection treewidth `omega` (pp. 6–7). Their
formulation is a strong precedent for treewidth-based polynomial
optimization, but the guarantee is approximate and its size depends on
`1/epsilon`; it does not provide expected exact optimization under finite
linear-cost noise or exploit a functional-constraint pullback.

Sparse moment/SOS hierarchies are another established route for constrained
polynomial optimization. Running-intersection assumptions can make
relaxations sparse, and convergence results apply under positivity and
compactness assumptions. Finite extraction generally needs additional
flatness or optimality conditions. These sources do not state the candidate's
randomized expected bit bound, and the hierarchy order is not the same as
the candidate's mesh refinement count. See Lasserre (2006), pp. 6–16, and
Nie (2013), pp. 2–3, 10–16, in the source set cited by the
[sparse polynomial audit](sparse-smoothed-polynomial-prior.md).

De Loera, Hemmecke, Köppe, and Weismantel, “FPTAS for optimizing polynomials
over the mixed-integer points of polytopes in fixed dimension,”
*Mathematical Programming* 115 (2008), 273–290,
[DOI 10.1007/s10107-007-0175-8](https://doi.org/10.1007/s10107-007-0175-8),
give an FPTAS in fixed total dimension for bounded mixed-integer polytopes
and nonnegative polynomial objectives. Their arbitrary-sign result is
range-relative, and the paper rules out the usual PTAS unless `P = NP` in
its model (Theorems 1–2, pp. 2–3, 11–15). It is an important mixed-integer
polynomial baseline, but it fixes total dimension, gives approximation
rather than exact output, and does not parameterize by interaction width.

## Scope and contribution boundary

The graph-constraint and actuator reductions are standard forms of
eliminating variables through an explicit functional representation. The
actuator adjoint is a finite-dimensional change of variables obtained by
repeated substitution; the pullback of triangular polynomial equalities is
direct polynomial composition. These steps alone do not establish a new
algorithmic principle.

The relevant solver claim is the resulting application of the reviewed
sparse polynomial box method under a constrained input representation, with
the proof obligations made explicit: substitution preserves bounded degree
and a supplied sparse decomposition; state-cost noise becomes only
conditioned polynomial coefficients; the remaining box-coordinate noise
stays independent with the same preselected finite law; and exact feasible
outputs are mapped back through the defining equations. This is a
restricted corollary, not a general solution of sparse polynomial MINLP.

For local-error pruning, exact conditional minimization is the classical
value-function idea used by DPOP. The additional proposed interface asks
for certified lower and upper recourse bounds at bag corners, with error
scaled to the bag mesh rather than the full dimension. The checked
AC-DPOP theorem gives a global objective-error bound, not that local
interface. The star example in the local-error note proves that replacing
the existing full-grid correction by a bag-only correction is unsound.
No efficient general recourse oracle is supplied by the current candidate.

## Source and verification status

- Read primary full texts locally: Hoang et al. (2020), Faenza et al.
  (2022), and De Loera et al. (2008).
- Lasserre (2006) and Nie (2013) are read local primary packages already
  cited in the sparse-polynomial audit; only their stated convergence and
  finite-extraction distinctions are used here.
- The two project constructions and the local-error counterexample were
  read to scope the comparison. No knowledge-base entries or main indices
  were changed. A targeted markdown whitespace check produced no
  diagnostics; no project-wide checks or CI inspection were run.
