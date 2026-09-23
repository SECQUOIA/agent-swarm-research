# Scope map for the passive-flow results

Updated: 2026-09-05. This is a map of reviewed statements, not a new
theorem. Individual files contain the models, proofs, tests, and priority
qualifications. Independent agent review is not external peer review.

All rows concern passive physical states. In the robust-validation rows,
parameter and nomination scenarios are evaluated without additional
potential or flow bounds, and the resulting flows are compared with limits.
The design and realization rows below explicitly use existential scenario
choices. These quantifiers describe different problems.

Here **block rank** means the maximum cycle rank of a biconnected block,
not the total cycle rank. **Polynomial additive** means polynomial time
in the rational input length and the requested number of accuracy bits.
The polynomial exponent may depend on a block-rank bound designated fixed.
**Series-parallel** means that the graph has no `K4` minor.

## Quadratic laws

The common law in this table is `pi_u-pi_v=beta_e x_e|x_e|`.

| Scenarios and graph class | Exact arc task | Additive optimization |
| --- | --- | --- |
| Balanced nomination boxes and independent resistance intervals; fixed block rank | [Rational capacity validation is polynomial](../results/potential-flow-exact-arc-capacity.md). | [Pressure and arc extrema are polynomial additive](../results/potential-flow-joint-resistance.md). |
| Balanced nomination boxes and independent finite resistance sets; block rank at most two | [Exact arc validation is polynomial](../results/potential-flow-series-parallel-arc-validation.md). | Arc extrema are consequently polynomial additive. Pressure optimization is a different task: the next row gives a barrier. |
| Fixed nominations and independent two-point resistance sets; block rank two | No arc hardness follows from this pressure gadget. | [Pressure optimization is NP-hard at binary precision](../results/potential-flow-discrete-resistance-hardness.md). |
| Fixed nominations and independent two-point resistance sets; one block of rank three | [Robust arc validation is coNP-complete](../results/potential-flow-discrete-arc-capacity-hardness.md). | Polynomial additive arc-extremum optimization would imply `P=NP`. |
| Fixed nominations and resistance intervals or finite sets; arbitrary series-parallel graph | No polynomial exact-comparison claim. The following row supplies an arithmetic barrier even without uncertainty. | [A target-specific envelope network gives polynomial additive arc extrema](../results/potential-flow-series-parallel-envelope-optimization.md), with a linear-size SOCP and an allowed endpoint witness. |
| Fixed unit source/sink nomination and fixed integer resistances; series-parallel probe-cactus family of unbounded block rank | [Weak lower comparison of one arc flow is SRS-complete](../results/potential-flow-series-parallel-exact-arc-barrier.md). The lower bound uses threshold `1/2`. | The preceding additive algorithm still applies. |
| Balanced nomination boxes and fixed resistances; series-parallel graphs of unbounded block rank | [Robust arc validation is coNP-hard](../results/potential-flow-series-parallel-nomination-hardness.md); membership is not asserted. | Polynomial additive arc-extremum optimization would imply `P=NP`. The pressure hardness source is Thürauf's earlier reduction. |

These statements distinguish three obstructions: exact arithmetic even
for one fixed physical state; combinatorial resistance choices on a small
non-series-parallel block; and nomination optimization on series-parallel
graphs with unbounded block rank. They are not interchangeable hardness
claims.

The positive envelope network is fixed for a prescribed target edge and
works pointwise for every balanced nomination. An original resistance
scenario realizing it can depend on that nomination. Different target
edges generally require different envelope networks. Removing resistance
uncertainty this way does not solve the remaining nomination optimization.

## Weighted potential objectives

A prescribed pairwise pressure difference has two objective terminals.
The following statements concern general zero-sum linear combinations of
potentials and therefore require their own support assumptions.

| Scenarios and objective | Reviewed guarantee or barrier |
| --- | --- |
| Fixed nominations; independent finite resistances; one cycle; three objective terminals | [Weighted potential threshold is NP-complete](../results/potential-flow-weighted-potential-cycle-hardness.md). Positive resistance scaling gives the stated absolute-error-one barrier. |
| Fixed nominations; resistance intervals; fixed total cycle rank; arbitrary weighted potential objective | [Exact algebraic optimization is polynomial](../results/potential-flow-weighted-potential-cycle-hardness.md), by the fixed-core theorem. Total rank, not maximum block rank, is fixed here. |
| Balanced nomination boxes; interval or finite resistances; any tree; arbitrary weighted objective support | [Threshold is NP-complete and robust upper-bound satisfaction is coNP-complete](../results/potential-flow-weighted-tree-np-completeness.md). Hardness already holds with fixed resistances on maximum-degree-three trees and unit-magnitude objective coefficients; absolute error one eighth is hard there. Convex knapsack hardness and rational QP certificates are credited. |

The following positive results each passed two full independent audits.

| Additional structure | Reviewed weighted-objective algorithm |
| --- | --- |
| Tree; fixed number `p` of objective terminals; nomination boxes and interval or finite resistances | [Exact rational optimization in `N^{O(p)}` time](../results/potential-flow-fixed-support-weighted-tree.md). Cut-current monotonicity reduces nominations to a polynomial family of fixed-dimensional faces. |
| Fixed total cycle rank `r` and fixed objective support `p`; nomination boxes and resistance intervals | [Exact algebraic optimization in polynomial time for fixed `r,p`](../results/potential-flow-fixed-support-global-rank.md). The polynomial exponent depends on both parameters. Discrete resistance sets are excluded. |

The tree theorem has rational outputs and permits finite resistance sets.
The cyclic theorem uses continuous intervals and returns algebraic outputs.
The argument does not replace fixed total rank by fixed maximum block rank:
inactive blocks can contribute algebraic functions of several shared loads.
Scaling every resistance preserves all flows and scales all potential
objectives. Potential-gap amplification therefore gives no corresponding
fixed absolute-error lower bound for arc-flow objectives.

## Weighted flows, realization, and design

All rows in this table have fixed nominations and quadratic laws. A cactus
can contain arbitrarily many cycles, but distinct cycles share at most one
vertex. Thus its maximum block rank is one.

| Task and assumptions | Reviewed guarantee or barrier |
| --- | --- |
| Linear flow objective; any cactus; interval or finite resistances | [A maximizing rational endpoint resistance scenario is computable in polynomial time](../results/potential-flow-cactus-flow-region-and-optimization.md). Its exact objective-value comparison is SRS-hard; additive value evaluation is polynomial in accuracy bits. |
| Linear flow objective; two-point resistances; total cycle rank two | [Exact threshold is NP-complete on the stated family](../results/potential-flow-weighted-arc-cycle-rank-hardness.md). Hardness holds for fixed small nominations, and also for unit-cost total flow on a simple maximum-degree-three DAG. Resistance scaling alone cannot amplify a flow gap. |
| Given rational target flow; finite resistance choices | [Exact realization is NP-complete already on one cycle](../results/potential-flow-discrete-flow-realization.md). Existential unit-capacity design is hard on the same family. This does not contradict polynomial robust capacity validation. |
| Given rational target flow; resistance intervals; arbitrary graph | [Exact realization is a rational LP](../results/potential-flow-discrete-flow-realization.md), since edge drops are linear in the resistance variables when flows are fixed. |
| Convex rational PSD quadratic flow objective; cactus; resistance intervals | [Minimization admits a rational epsilon-optimal resistance scenario in time polynomial in accuracy bits](../results/potential-flow-cactus-convex-design.md). The [capacity extension](../results/potential-flow-cactus-capacitated-convex-design.md) permits exact signed arc bounds and cycle-local linear flow constraints, including singleton feasible intervals. |
| Convex rational PSD quadratic flow objective; cactus; resistance intervals or two-point sets | [Maximization is strongly NP-hard](../results/potential-flow-cactus-convex-performance-hardness.md), even with constant network data and an absolute one-quarter accuracy target. This is a bounded physical realization of the classical Max-Cut box construction. |

The [correlated-cycle extension](../results/potential-flow-cycle-polytope-resistance-design.md)
replaces independent edge intervals by an arbitrary rational resistance
polytope within each cycle. Different cycles remain independent. Exact
individual extrema and rational optimizing profiles are computable in
polynomial time; exact capacity feasibility and additive convex design
also hold. Its exact recovery argument uses LP thresholds and algebraic
root separation, with publication priority separately qualified.

Arbitrary correlations **between** cycles have a sharper task-dependent
boundary. The [global-correlation arc theorem](../results/potential-flow-global-correlation-arc-validation.md)
gives one LP for exact simultaneous arc-capacity feasibility and exact
individual-arc optimization by the monotone-root lemma, including its
polynomial-law scope. The quadratic capacity halfspaces directly extend
Aßmann et al.'s existing cycle lemma. In contrast,
[maximum total arc flow](../results/potential-flow-global-correlation-total-flow-hardness.md)
and [minimum unit source-to-sink potential difference](../results/potential-flow-global-correlation-energy-design-hardness.md)
are strongly NP-hard under globally correlated resistances, already on
maximum-degree-three cacti with bounded numerical data and a constant
accuracy gap. Total arc flow is not delivered throughput; constitutive
dissipation equals b·pi and need not be literal compressor power.

The direction of energy optimization matters. On **any connected graph**,
[maximum constitutive dissipation](../results/potential-flow-global-energy-maximization.md)
over a bounded positive rational resistance polytope has an exact SOCP and
a polynomial-bit additive algorithm returning an exactly admissible rational
resistance profile. It also has an independently audited exact rational
certificate for global design quality. On a cactus, the affine capacity
filter above can be included exactly. The general-graph statement has no
additional physical capacity or potential filters. Resistance-energy
concavity and conic duality are classical: this is a supporting positive
companion to the hard **minimum**, with the precise source qualifications
retained, rather than a new general convexity principle. Exact scalar
threshold comparison is outside the additive guarantee.

The [correlated polynomial-law application](../results/potential-flow-correlated-polynomial-cycle-design.md)
extends the independent-cycle design algorithm to fixed-breakpoint,
densely encoded, continuous strictly increasing passive laws whose
coefficients depend affinely on each cycle's parameter polytope.
The [convex polynomial performance extension](../results/potential-flow-convex-polynomial-design.md)
permits dense convex polynomial objectives with growing degree. Strict
passivity and objective convexity are promises in these extensions;
no additional polynomial validation procedure is claimed.

For [fixed numbers of linear flow measurements](../results/potential-flow-cactus-few-measurement-maximization.md),
convex polynomial performance maximization admits polynomial additive
endpoint-scenario search on cacti. The exponent depends on the measurement
count. This applies classical zonotope enumeration and does not claim exact
comparison of arbitrary sums of algebraic candidate values.

For interval resistances, the cactus flow region is an affine image of a box
of independent cycle circulations. For finite resistances, its convex hull is
the same box image, but its actual attainable flows can have gaps. Convex
minimization therefore does not transfer from intervals to finite choices.
For linear optimization, returning an optimizer scenario avoids comparisons
between sums of algebraic cycle values; evaluating its exact value can still
be difficult.

## The law representation changes the answer

| Law representation and scenarios | Reviewed guarantee or barrier |
| --- | --- |
| Continuous, strictly increasing, densely encoded piecewise polynomial laws, with independent affine coefficient boxes and nomination boxes; fixed block rank | [Exact arc extrema and polynomial additive pressure optimization](../results/potential-flow-polynomial-law-uncertainty.md). Dense degrees and piece counts may grow. Uniform strict monotonicity has an explicit polynomial validation procedure. |
| Fixed law `sign(x)|x|^(3/2)`, fixed nominations and resistances; one cycle | [Exact arc comparison is SRS-hard](../results/potential-flow-fractional-power-arc-barrier.md). The extension to other specified rational exponents retains its stated parity condition. |
| A fixed finite family of rational exponents in `(1,3)`, possibly differing by edge; nomination and positive resistance boxes; fixed block rank | [Pressure and arc extrema are polynomial additive](../results/potential-flow-fractional-additive-optimization.md), with rational near-optimal scenarios. This does not remove the exact fractional-power comparison barrier. |

SRS denotes the standard Square-Root-Sum decision problem. It is not
known to be NP-hard or polynomial-time decidable. A weak lower comparison,
a strict capacity violation, and its robust complement must retain their
actual inequality conventions; the result files make equality cases explicit.

## Structure and attribution

The objective changes the universal resistance-hull boundary:

| Objective, with fixed nominations | Graphs where all finite resistance sets and their interval hulls give the same extrema |
| --- | --- |
| Each individual arc flow | [Series-parallel graphs](../results/potential-flow-series-parallel-arc-characterization.md) |
| Every linear combination of arc flows | [Cacti](../results/potential-flow-weighted-arc-cactus-characterization.md) |
| Every linear combination of normalized potentials | [Trees](../results/potential-flow-weighted-potential-tree-characterization.md) |

The [state-region characterization](../results/potential-flow-cactus-region-convexity-characterization.md)
also shows that universal convexity of the actual interval-resistance flow
region identifies cacti, whereas universal convexity of the normalized
potential or joint-state region identifies trees. This has two full audits;
the positive-width thickening corollary is existential and carries no
polynomial witness-precision claim.

The latter two hull characterizations have two full independent proof audits.
Their positive arguments extend classical circuit and cycle monotonicity;
the converse constructions and precise scope are separately documented.


The [arc uncertainty-hull characterization](../results/potential-flow-series-parallel-arc-characterization.md)
identifies series-parallel graphs through a universal equality between
finite scalar uncertainty sets and their interval hulls. Its necessity
already uses a single uncertain quadratic resistance. This structural
statement is separate from bit-time computation of the resulting extremum.

Classical nonlinear-circuit confluence and electrical sign results are
credited throughout. The [focused source audit](potential-flow-series-parallel-envelope-novelty.md)
found no matching computational theorem but could not access directly
relevant older nonlinear-tolerance papers. The envelope and positive
structural results therefore retain that publication-priority caveat.


The [reviewed signed-path refinement](potential-flow-weighted-sign-path-decomposition.md)
permits unbounded weighted-objective support when a supplied fixed-size
marked set splits the graph into paths with one coefficient sign each.
Together with fixed global cycle rank, it gives exact algebraic joint
nomination/resistance optimization. It is a supporting corollary of the
fixed-support theorem and retains its continuous-interval and unfiltered
scenario assumptions.
