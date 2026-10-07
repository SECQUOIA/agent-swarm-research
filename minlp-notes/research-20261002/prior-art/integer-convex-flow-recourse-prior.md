# Prior-art audit: exact separable-convex integer-flow recourse

Date: 2026-10-02. This note compares the exact recourse primitive needed by
the [native-integer recourse theorem](../new-direction/smoothed-native-integer-recourse.md)
with classical separable-convex integer optimization. It is a focused source
comparison, not a proof review or a publication-priority claim.

## Candidate oracle and its structural boundary

The proposed recourse set is a fixed bounded integral flow set
`Y={z in Z^r: Bz=b, l<=z<=u}`, where `B` is a directed node-arc incidence
matrix and the supplies and arc bounds are integral. A rational continuous
core point `v` appears in the per-arc costs `sum_e f_e(v,z_e)` but not in the
flow equations or bounds. Each `f_e(v,.)` is a convex fixed-degree rational
polynomial on its arc interval. Rational linear perturbations of the arc
costs preserve convexity. The desired oracle returns an exact attaining
integer flow and its exact rational value, or infeasibility, in polynomial
bit time; it must continue to do so after arbitrary individual arc intervals
are tightened.

This restriction to cost-only dependence matters. Fixing a rational core arc
inside a conservation equation can change the remaining supply by a
noninteger amount, so the usual integral-flow oracle would no longer apply.
The present candidate avoids that issue by keeping the feasible residual
flow set fixed.

## The direct classical result already supplies the oracle

Hochbaum and Shanthikumar's primary paper, [“Convex Separable Optimization Is
Not Much Harder than Linear Optimization”](https://hochbaum.ieor.berkeley.edu/html/pub/Hochbaum-Shanthi-JACM90.pdf),
studies bounded integer optimization of a separable convex objective
`F(x)=sum_i f_i(x_i)` under integer linear constraints `Ax>=b`. Their
Theorem 1.2 gives a scaling reduction to integer linear optimization. In
the totally-unimodular case, Algorithm 4.2 and Theorem 4.3 return an **exact
optimal integer vector** using

```text
O(log((m/n) ||b||_infinity) * T(4 n^2, m, 1))
```

where `T` is the cost of the corresponding linear program. The locators are
Theorem 1.2 (printed p. 847) and Theorem 4.3 (printed p. 858 / PDF p. 16).
The paper says its nonlinear functions need only be evaluated at a
polynomial-size prescribed grid (printed pp. 844–845). The local
[primary-source package](../../literature/papers/hochbaum1990-convex-separable-optimization-is-not/)
contains the original PDF and extracted text.

A network incidence matrix is totally unimodular. Adding the unit rows for
lower and upper arc bounds preserves total unimodularity; shifting integer
lower bounds into the node supplies also preserves integral right-hand sides.
Thus Theorem 4.3 applies to bounded capacitated flows, including any query
that tightens individual arc intervals to integer endpoints. Rational query
intervals can first be intersected with the integer domain by taking a
ceiling at the lower endpoint and a floor at the upper endpoint. An empty
intersection is detected directly.

The source is stated for a function-evaluation oracle rather than an
explicitly encoded rational polynomial. The finite-bit specialization here
is an inference: after a rational core `v` is fixed, a fixed-degree
polynomial `f_e(v,z_e)` has rational coefficients, and its exact values at
the algorithm's rational grid points have bit length polynomial in the
input and query lengths. Rational linear perturbations have the same
property. Therefore the linearized LPs have rational data of polynomial
encoding length and can use a standard polynomial-time rational LP
algorithm. The returned flow is integral, so evaluating the original
polynomial at it gives the exact rational optimum value. The scaling bound
depends logarithmically on the flow-capacity/supply magnitude; binary
capacities therefore contribute their encoding length, not their numerical
value. This is not a unit-augmentation or pseudopolynomial claim.

The result covers a broader TU separable-convex class than network flow and
requires no treewidth or decomposition parameter. It does not cover
nonseparable interactions among residual flow coordinates, non-TU side
constraints, or a core parameter that changes the integer feasibility
right-hand side. Convexity remains a promise or supplied certificate; the
algorithm does not decide convexity of arbitrary input polynomials.

## Stronger special cases and limits of mixed-integer extensions

Minoux's 1986 paper is an early dedicated capacity-scaling algorithm for
integer minimum-cost flow with separable convex arc costs. Hochbaum and
Shanthikumar cite it as a direct predecessor. Its bibliographic record is
verified, but the primary text could not be retrieved lawfully in the
targeted source check, so its exact capacity/runtime statement remains
unverified here. This audit relies on the readable
Hochbaum--Shanthikumar theorem for its precise oracle claim.

Végh's strongly-polynomial minimum-cost-flow result is a useful nearby
special case, but it is for real-valued flows. The 2012 STOC paper defines
the feasible flow polyhedron over real vectors and includes convex
quadratic costs; integrality of the network polyhedron does not make a
nonlinear convex minimizer integral. It therefore does not replace the
integer oracle required here. The same source records that general-degree
polynomial convex costs do not admit the same strong-polynomial guarantee.
The polynomial-in-input-length, logarithmic-capacity TU result above is the
direct applicable comparison. The read arXiv author text and local
[source package](../../literature/papers/vegh2016-a-strongly-polynomial-algorithm-for/)
give Theorem 4.5 on p. 15 and Theorem 6.2 on p. 24.

Parameterized algorithms for more general block-structured integer
programs are a separate line. Brand, Koutecký, Lassota, and Ordyniak's
primary ESA 2024 paper proves hardness for separable-convex mixed-integer
programming on bounded-block 2-stage stochastic and `n`-fold structures
(Theorems 3–4, printed pp. 4 and 14–15). These lower bounds do not apply to
the pure-integer TU flow recourse above, but they warn against replacing
the network/TU hypothesis with generic mixed-integer decomposability.
The candidate's continuous core is only a parameter in the cost after
conditioning, not a continuous variable coupled into those balance
constraints.

## Few continuous variables and smoothed discrete optimization

Schöbel and Scholz's 2014 paper, “A solution algorithm for non-convex mixed
integer optimization problems with only few continuous variables,” is the
closest geometric branch-and-bound comparison. The publisher abstract says
their method branches on a small set of box-constrained continuous variables
and solves or bounds a discrete subproblem at each node; it also reports a
convergence-rate analysis and exact solutions for two applications. The
local record is still metadata/abstract only, so no theorem or complexity
claim beyond that abstract is attributed here. The candidate also searches a
small continuous core with discrete recourse. Its claimed distinction is the
expected finite-noise bound on exact work, using a box-stable exact recourse
oracle and a same-draw exact closure/fallback. This is a qualified
distinction, not a claim that geometric branch-and-bound is new.

Beier and Vöcking's readable STOC 2004 paper, “Typical Properties of Winners
and Losers in Discrete Optimization,” is a direct smoothed-isolation and
adaptive-precision precedent. For binary optimization it bounds winner-gap
density, shows that the winner is determined with high probability after
logarithmically many revealed coefficient bits, and characterizes polynomial
smoothed complexity through randomized pseudopolynomial solvability. The
accessible local source is the 2004 proceedings version (DOI
10.1145/1007352.1007409), not the separate 2006 journal record. Röglin and
Vöcking's 2007 “Smoothed Analysis of Integer Programming” extends gap
arguments and adaptive rounding to integer programs, again using a
pseudopolynomial solver. Its smoothed-runtime convention is a high-probability
tail bound, not ordinary expected bit time. These are important
solver-preserving precedents, but their feasible decisions are discrete and
their perturbation model uses independent bounded-density coefficients;
neither source gives the present continuous-core search plus exact
box-stable recourse composition under a base-chosen finite rational noise
law.

Beier, Röglin, Rösner, and Vöcking's “The smoothed number of Pareto-optimal
solutions in bicriteria integer optimization” is a close expected-count
analogy. Theorem 1 bounds the expected Pareto-set size for an arbitrary
finite integer feasible set and independent bounded-density linear-profit
coefficients. The paper derives expected-running-time bounds for established
Pareto-enumeration algorithms for knapsack and shortest paths. This controls
enumeration work through a smoothed solution count, but does not optimize
over a continuous core, provide box-stable exact recourse, or use a finite
noise law with exact output on every draw.

There is also a nearby exact result in this project, the reviewed
[mixed separable-closure theorem](../new-direction/smoothed-mixed-separable-closure.md).
It treats arbitrarily many integer coordinates with separable convex
piecewise-quadratic costs and a low-rank concave quadratic coupling. It gives
expected exact work under a finite aligned-noise law and a separate
ambient-noise result at fixed coupling rank. Its scalar recourse is
separable and represented by finitely many regions. The flow theorem instead
permits coupled integer feasibility through a TU flow system and general
fixed-degree separable convex arc costs, using the exact TU oracle. Neither
result subsumes the other: their recourse geometry and oracle assumptions
differ. The mixed separable result is an internal algorithmic comparator,
not external prior art.

## What the comparison establishes

The exact convex-flow recourse operation, binary-capacity handling, and
stability under tightened individual arc bounds are classical consequences
of separable-convex optimization over totally unimodular systems. They are
not contributions of the smoothed theorem. The theorem uses this established
oracle inside a different outer mechanism: finite-noise expected search in
a small continuous core, exact tests excluding competing integer labels,
and exact closure on the remaining continuous core. I have not found a
source in this focused comparison that combines that full smoothed,
expected exact guarantee with the integer-flow recourse oracle; failure to
find one is not evidence of novelty.

## Sources checked and remaining source work

- Hochbaum and Shanthikumar, *Journal of the ACM* 37(4) (1990), 843–862.
  Primary author-hosted PDF and local
  [source package](../../literature/papers/hochbaum1990-convex-separable-optimization-is-not/);
  Theorems 1.2 and 4.3.
- Brand, Koutecký, Lassota, and Ordyniak, “Separable Convex Mixed-Integer
  Optimization: Improved Algorithms and Lower Bounds,” ESA 2024,
  [primary proceedings text](../../literature/papers/brand2024-separable-convex-mixed-integer-optimization/);
  Theorems 3–4.
- Beier and Vöcking, “Typical Properties of Winners and Losers in Discrete
  Optimization,” STOC 2004, DOI 10.1145/1007352.1007409; readable proceedings
  source package [here](../../literature/papers/beier2006-typical-properties-of-winners-and/).
  The 2006 SIAM journal record is a separate, unread package.
- Röglin and Vöcking, “Smoothed Analysis of Integer Programming,”
  *Mathematical Programming* 110(1) (2007), DOI 10.1007/s10107-006-0055-7;
  readable author manuscript and notes
  [here](../../literature/papers/roglin2007-smoothed-analysis-of-integer-programming/).
- Beier, Röglin, Rösner, and Vöcking, “The smoothed number of Pareto-optimal
  solutions in bicriteria integer optimization,” *Mathematical Programming*
  200(1) (2023; first online 2022), DOI 10.1007/s10107-022-01885-6; primary
  text and notes [here](../../literature/papers/beier2022-the-smoothed-number-of-pareto/).
- Schöbel and Scholz, “A solution algorithm for non-convex mixed integer
  optimization problems with only few continuous variables,” *European
  Journal of Operational Research* 232(2) (2014), 266–275, DOI
  10.1016/j.ejor.2013.07.003. Only the publisher abstract is currently
  available in the local [record](../../literature/papers/schobel2014-a-solution-algorithm-for-non/);
  full text and theorem statements remain unverified.
- The project's reviewed
  [mixed separable-closure result](../new-direction/smoothed-mixed-separable-closure.md),
  as an internal near-comparator.
- Végh, “A Strongly Polynomial Algorithm for a Class of Minimum-Cost Flow
  Problems with Separable Convex Objectives,” STOC 2012; the primary text
  defines real-valued flows and gives the convex-quadratic special case
  (Theorems 4.5 and 6.2 in the read arXiv author text).
  This is not the integer oracle.
- Minoux, “Solving Integer Minimum Cost Flows with Separable Convex Cost
  Objective Polynomially,” *Mathematical Programming Study* 26 (1986),
  237–239; the local record is metadata-only after the targeted lawful
  full-text search found no accessible copy. The audit's exact-oracle
  conclusion already follows from Hochbaum–Shanthikumar.
