# Weighted tree optimization controlled by the direction pattern of objective cut flows

Date: 2026-09-05. Status: verified by two independent full audits. The direction-pattern parameter strengthens the separately verified support theorem; its distinct publication priority remains unconfirmed.

## Stronger parameter

Use the same quadratic tree model, rational balanced nomination box, independent finite or interval resistance sets, and zero-sum rational objective `c` as in the [fixed-support tree theorem](potential-flow-fixed-support-weighted-tree.md). There is a unique objective cut-flow vector `w` with `Aw=c`.

Contract every edge with `w_e=0`, aggregating nomination intervals and objective coefficients as in that theorem. If no edge remains, the objective is zero. Otherwise orient every remaining edge so that its cut flow is positive. Mark exactly those vertices that do not have one incoming and one outgoing edge. Let `k` be their number. This includes all leaves and branching vertices, and those degree-two vertices where both objective-flow arrows enter or both leave.

The theorem gives exact rational joint optimization in `N^{O(k)}` bit time, with rational optimal nomination, resistance, flow, and potential outputs. Objective support need not be fixed. All uncertainty and physical-model restrictions are unchanged from the fixed-support theorem. In particular, this is an XP bound in `k`, not an asserted fixed-parameter tractable bound.

## Proof reduction to the reviewed mechanism

Suppress every unmarked vertex. Since every unmarked vertex has undirected degree two, the suppressed graph is a tree on `k` marked vertices with `k-1` paths. By construction every such path is directed consistently with positive cut flow. Its cut-flow magnitude may vary from edge to edge, and internal objective coefficients can be nonzero.

For the smoothed quadratic law with fixed resistance, the weighted objective's nomination gradient satisfies

```
h_tail-h_head=beta_e(2|x_e|+rho) w_e>0
```

on every oriented edge. Therefore `h` strictly decreases along every suppressed directed path. Constancy of `w_e`, zero internal objective coefficients, and fixed objective support are unnecessary for this conclusion.

At an optimum, the common nomination-balance multiplier implies upper-bound nominations before a threshold and lower-bound nominations after it, with at most one free internal coordinate on each path. Leave all marked coordinates free. Enumerating each path's threshold or one free pivot gives `N^{O(k)}` closed faces, each with at most

```
k+(k-1)=2k-1
```

free nominations. The same finite-face subsequence as in the support theorem removes smoothing. The family is independent of resistance values, so fixing a joint optimizing resistance vector transfers a joint optimum to one of these faces.

All remaining steps are exactly those of the support theorem: eliminate resistance variables by choosing endpoints according to the sign of `w_e x_e|x_e|`; split the fixed-dimensional nomination core by flow-sign hyperplanes; solve each rational quadratic cell by active-face stationarity and rational linear feasibility; compare exact rational values; disaggregate contracted nominations and recover the physical state. The antecedent algorithm and this structural strengthening have both been independently verified.

## Relation to support and a useful path case

If `c` has support size `p`, the contracted tree has at most `p` leaves and at most `p-2` branching vertices. A marked degree-two vertex has both objective currents entering or both leaving, so its balance coefficient is nonzero. Every marked vertex that is not a branching vertex therefore belongs to the support. Consequently

```
k<=2p-2.
```

The stronger theorem implies the support-based complexity bound, while it may apply with small `k` even when `p` grows.

For example, orient a path from left to right and define each cut weight as the cumulative sum of objective coefficients on its left. If every nonzero cumulative sum has the same sign, then after zero-weight contraction every remaining edge points in one direction and `k=2`. Thus exact joint optimization is polynomial even for arbitrarily many nonzero objective coefficients. More generally, if the nonzero cut weights change sign `t` times along the contracted path, then `k=t+2`.

This example does not contradict the growing-support tree hardness reduction: that comb has a growing number of marked leaf and branch vertices. Nor does it say that all path objectives are easy when the cut-weight direction changes an unbounded number of times.

## Independent verification and source limits

Both [the first audit](../notes/review-potential-flow-weighted-tree-sign-pattern-independent.md) and [the second audit](../notes/review-potential-flow-weighted-tree-sign-pattern-second.md) passed. They checked contraction, directed paths, threshold faces, parameter counts, and the inherited exact rational algorithm. The [support-theorem source audit](../notes/potential-flow-fixed-support-weighted-tree-novelty.md) credits prior cut-flow formulas, electrical sensitivities, and rational quadratic programming. This additional direction-pattern formulation has not received an exhaustive separate priority review.

## Reproducible checks

[`weighted_tree_sign_pattern_checks.py`](../code/potential_flow_mpd/weighted_tree_sign_pattern_checks.py) tested two five-vertex paths with objective support five but only two and three directed marks. Across 2,818 stationary candidates over all flow-sign cells, the global candidate maximum was attained on the stronger path family. Every candidate's resistance endpoint selection matched exhaustive corner evaluation. Another 148 small integer coefficient patterns verified the exact cumulative-sign count and `k<=2p-2`. The stationary systems use numerical linear algebra; the count checks use exact integer cut sums.
