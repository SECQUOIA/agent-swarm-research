# Prior-art audit: smoothed core-only optimization with integer-flow recourse

Date: 2026-10-02. This focused audit compares the completed
[interior-core flow theorem](../new-direction/smoothed-interior-core-flow.md)
with exact convex-flow optimization, parametric methods, partial-convex
global search, and smoothed optimization. The theorem passed its
[independent review](../reviews/smoothed-interior-core-flow-review.md).
This note assesses prior work; it is not a proof review or a priority claim.

## The result and its restrictions

The domain is `[0,1]^k` times a fixed bounded integral network-flow set
`Y={z in Z^r: Bz=b, l<=z<=u}`. Supplies and arc bounds are integral and
binary encoded. The objective is `phi(v)+sum_a f_a(v,z_a)`, with fixed-degree
rational polynomial terms; at each core point, each arc cost is convex in
its own flow coordinate. Flow feasibility, supplies, and bounds do not
depend on the core. Only the `k` core linear coefficients receive
independent noise from one base-chosen finite rational uniform grid.

The key additional promise is global interiority: for every noise vector in
the full coefficient cube, every optimal core point lies in `(0,1)^k`.
A uniform inward-gradient margin on every core face is one sufficient
certificate. The theorem does not require a quantitative distance from the
boundary, a unique optimal flow, or a unique core point on every atom. It
returns an exact integer flow and an algebraic representation of a global
core optimizer and value on every draw, with expected work

```text
[8^k [3+(1+k/2)L/(2 sigma)]^k+c_d^k] poly_d(I).
```

This is fixed-parameter dependence on `k` and the numerical ratio
`L/sigma`; it is polynomial in the base input length when those parameters
are fixed or suitably bounded. There is no residual-noise requirement, but
the result does not cover boundary core optima or core-dependent flow
constraints. Persistent ties among flow labels are allowed.

## Exact flow optimization is a classical primitive

Hochbaum and Shanthikumar's primary paper, [“Convex Separable Optimization
Is Not Much Harder than Linear Optimization”](../../literature/papers/hochbaum1990-convex-separable-optimization-is-not/),
already gives exact algorithms for separable convex integer optimization
over totally unimodular systems. Theorem 1.2 (printed p. 847) reduces the
problem to integer linear optimization; Algorithm 4.2 and Theorem 4.3
(printed p. 858 / PDF p. 16) give the TU case with logarithmic dependence on
the right-hand-side magnitude. A directed incidence matrix with integral
arc bounds is TU. Tightening any arc interval to integer endpoints preserves
the same form, so the result gives the candidate's exact recourse oracle
and remains stable under individual arc-bound restrictions.

The paper states an evaluation-oracle and LP-operation bound. Its ordinary
polynomial bit-time specialization for the candidate is an inference:
after fixing a rational core, a fixed-degree polynomial arc cost can be
evaluated exactly at the rational points used by the scaling method with
polynomial bit length. A rational LP implementation then gives polynomial
bit time, and the integral flow gives an exact rational value. Binary
capacities contribute their encoding length through the logarithmic scaling
factor, not their numeric magnitude. This establishes the flow solver; it
does not establish the smoothed outer optimization.

The residual-graph certificate in the theorem also uses standard flow
optimality structure. At one exact optimal flow, no residual cycle has
negative cost. Shortest-path potentials make all reduced marginal costs
nonnegative. If their polynomial expressions remain nonnegative throughout
a retained core box, the same flow is optimal throughout that box. The
certificate is non-strict, so zero reduced costs and persistent ties are
allowed. The algorithm builds one such certificate from the queried flow;
it does not enumerate all feasible flows or all their parametric regions.

## Parametric charts can be large, but the algorithm does not enumerate them

Gajjar and Radhakrishnan's primary paper, [“Parametric Shortest Paths in
Planar Graphs”](https://eccc.weizmann.ac.il/report/2018/211/download),
Theorem 1, gives `n^{Omega(log n)}` lower-envelope breakpoints for a
one-parameter shortest-path problem even with a directed acyclic planar
graph and `O(log^3 n)`-bit integer affine edge coefficients. A shortest-path
instance is a unit-flow min-cost-flow instance, so even this special
parametric recourse value can have a superpolynomial number of pieces.
This is a warning against charging a solver for explicitly constructing the
full value-function envelope. It is not a lower bound for point queries,
for the theorem's expected runtime, or for a particular core objective.

Ding's thesis gives exact parametric-envelope machinery for certain
structured nonconvex quadratic programs: in the one-negative-eigenvalue
case, a scalar parameter yields a piecewise-quadratic value function and
global candidate selection (Theorem 2.3.1, PDF pp. 30–34). Patrinos and
Sarimveis likewise give exact critical-region traversal for convex
parametric piecewise-quadratic programs, including multivalued optimizer
maps; their output-sensitivity statement is qualitative. These works
establish region-based representations and search, but not a finite-noise
expected bit bound for nonconvex core optimization with integer flow
recourse. Neither is a flow-cost theorem of the exact form considered here.
The theorem's chart family can be exponentially large in the flow labels,
but it is used only to set a base-only analysis budget; the executed
algorithm obtains a single label and a single residual arborescence per
certificate attempt.

## Partial-convex and few-continuous-variable global search

Hooker's [“Convex Programming Methods for Global Optimization”](https://doi.org/10.1007/11425076_4)
treats global problems that become
convex after selected variables are fixed. It discretizes selected
continuous variables and solves convex subproblems; Section 7 and Theorem 2
give a valid quasi-relaxation for specified convex/semihomogeneous
structures. This is direct prior art for choosing a small core and using
convex recourse. It does not state the present finite-noise expected FPT
bound, exact output on every finite-law atom, or the non-strict polynomial
certificate for one flow to remain optimal over the surviving core hull.

Schöbel and Scholz's 2014 paper, [“A solution algorithm for non-convex mixed integer optimization problems with only few continuous variables”](https://doi.org/10.1016/j.ejor.2013.07.003), is a nearby application
algorithm: its publisher abstract describes branching on a small set of
continuous variables while solving or bounding the discrete subproblem.
The local source record is metadata/abstract only, so its precise theorem
and complexity assumptions are not verified here. The comparison supports
only the conceptual precedent of few-continuous-variable search with
discrete recourse.

The present model is more structured in its recourse than generic
mixed-integer optimization: fixing the core leaves separable convex costs
over a TU flow set, and core dependence changes costs but not feasibility.
Conversely, its perturbation is restricted to the core, and it requires
every global core optimum to be interior for every possible draw. It should
not be described as a general few-continuous-variable mixed-integer
algorithm.

## Smoothed optimization precedents and close internal comparisons

Beier and Vöcking's readable STOC 2004 paper, [“Typical Properties of
Winners and Losers in Discrete Optimization”](https://doi.org/10.1145/1007352.1007409),
uses independent random objective coefficients to bound winner gaps and
support adaptive precision for finite discrete optimization. This is a
direct anti-concentration precedent, but it does not optimize a continuous
core or give box-uniform flow closure. The source used is the 2004
proceedings text; the separate 2006 journal record is not the readable
source in the local package. Röglin and Vöcking's [“Smoothed Analysis of
Integer Programming”](https://doi.org/10.1007/s10107-006-0055-7) extends
gap and adaptive-rounding methods to integer programs. Their smoothed-time
definition is a high-probability tail / expected-power condition, not
ordinary expected bit time. Beier, Röglin, Rösner, and Vöcking's expected
Pareto-set-size bound is another expected-count precedent for finite
integer feasible sets under bounded-density linear perturbations; it does
not provide the continuous-core recourse algorithm here.

Two reviewed results in this project are especially close but are internal
comparators, not external prior art:

- The [native-integer recourse theorem](../new-direction/smoothed-native-integer-recourse.md)
  permits an arbitrary fixed integer feasible set and a box-stable exact
  oracle, but perturbs both core and residual objective coefficients. Its
  closure identifies one residual label by excluded-label optimization.
  The flow theorem narrows the residual class to convex-cost TU flows and
  removes residual perturbations under the stronger all-draw interiority
  promise; it instead certifies one selected flow over a core hull by
  residual potentials.
- The [mixed separable-closure theorem](../new-direction/smoothed-mixed-separable-closure.md)
  gives expected exact optimization with many integer coordinates, but its
  feasible domain is a product and its nonconvex coupling is a low-rank
  quadratic. It does not cover coupled flow feasibility. Conversely, its
  scalar separable recourse allows long integer ranges without the network
  structure or core-interiority assumption used here.

These comparisons credit established anti-concentration and recourse
ideas. The possible addition is their composition for core-only noise:
expected sparse search in a continuous core, an exact convex-cost flow
oracle, a whole-hull residual optimality certificate that tolerates ties,
and an exact same-draw fallback. The reviewed result is a guarantee for the
sampled objective under its all-draw interiority promise, not for the
unperturbed objective.

## Separate status of the constant-base component solver

The flow theorem includes an additive `c_d^k` term from the deterministic
[constant-base polynomial box solver](../new-direction/polynomial-component-primitive-limit.md).
That solver is separately reviewed and gives exact algebraic optimizer/value
output for arbitrary fixed-degree rational polynomials on a bounded box,
including ties and positive-dimensional stationary or minimizing sets, in
`c_d^k poly_d(H)` bit work. The prior-art comparison for this exact
constant-base, degeneracy-safe contract is not fully closed.

The best directly checked general baselines are Renegar's fixed-block
quantifier-elimination bounds and Basu–Pollack–Roy's Algorithm 14.9 for
global polynomial optimization. Algorithm 14.9 has an arithmetic bound of
`s^(2k+1) d^(O(k))` for `s` constraints in `k` variables; with the `O(k)`
box-face constraints this expression includes `k^{O(k)}`, not a stated
`c_d^k` bound. Renegar likewise provides exact elimination with
dimension-sensitive bounds. These methods establish general exact
real-algebraic approaches, but the checked statements do not directly give
the component solver's constant-base bit bound, one-common-root coordinate
representation, and correctness on every degenerate input. The internal
solver uses fixed-degree monomial quotient algebras, an explicit finite
family of separating linear forms, and a joint critical-limit extraction;
the review verifies that construction. This is a limited source comparison,
not evidence that the algebraic ingredients or the solver are new.

## Sources examined and limits

- Hochbaum and Shanthikumar (1990), Theorems 1.2 and 4.3; full primary text
  and exact convex-flow bit specialization discussed in the
  [flow-oracle audit](integer-convex-flow-recourse-prior.md).
- Gajjar and Radhakrishnan (2019), Theorem 1; full primary text and scope in
  the [parametric-breakpoint audit](parametric-flow-breakpoint-prior.md).
- Hooker (2005), Section 1 and Section 7/Theorem 2; full author manuscript
  in the local [source package](../../literature/papers/hooker2005-convex-programming-methods-for-global/).
- Schöbel and Scholz (2014), DOI `10.1016/j.ejor.2013.07.003`; metadata
  and publisher abstract only in the local
  [record](../../literature/papers/schobel2014-a-solution-algorithm-for-non/).
- Beier and Vöcking (2004), Röglin and Vöcking (2007), and Beier et al.
  (2023); primary-source locators and the expected-time distinctions are
  recorded in the [integer recourse audit](integer-convex-flow-recourse-prior.md).
- Ding (1996 thesis), Patrinos and Sarimveis (2011), and the internal
  smoothed results described above; exact source and review status are
  recorded in [the parametric-QP audit](smoothed-cell-closure-prior.md)
  and the linked theorem files.
- Renegar (1992), Basu–Pollack–Roy (2006), and the reviewed internal
  component solver; details appear in the
  [sparse-polynomial audit](sparse-smoothed-polynomial-prior.md) and the
  [component construction](../new-direction/polynomial-component-primitive-limit.md).

No literature-KB or index files were changed. The focused source comparison
does not identify an equivalent full theorem, but the sources checked are
not exhaustive and that fact does not establish novelty.
