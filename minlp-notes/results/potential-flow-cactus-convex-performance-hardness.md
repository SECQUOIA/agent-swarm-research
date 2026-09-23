# Coupled convex worst-case flow performance is hard even on bounded-data cacti

Date: 2026-09-05. Status: verified by two full mathematical audits. The standard optimization mechanisms are credited below; mathematical verification does not establish publication priority.

## Theorem

Worst-case maximization of a rational convex quadratic function of flows is strongly NP-hard on a simple cactus of maximum degree three, with fixed unit source/sink nominations, positive resistance intervals contained in [1,16], and all fixed resistances in that same range. The construction has a unit objective gap, so absolute-error-one-quarter value approximation is NP-hard without rescaling nominations or resistances.

This contrasts with additive convex quadratic MINIMIZATION under continuous resistance intervals and with exact optimizing-scenario search for LINEAR flow objectives. Endpoint attainment for a convex worst-case objective does not make its exponentially many vertex choices easy to optimize.

## 1. Realize a rational cube by independent cactus triangles

For each vertex i of an unweighted Max-Cut instance H, create a triangle with one direct arc and an alternate path of two edges. Join the triangles in a chain by bridges, using separate triangle vertices at bridge attachments. Put nomination +1 at the first terminal and -1 at the last, and zero elsewhere.

Each triangle carries unit through-flow. Its alternate edges have fixed resistances 2 and 2, total 4. The direct arc has independent resistance beta_i in [1,16]. Give every joining bridge resistance 4. All edges can be directed along the common source-to-sink direction, so every physical flow is positive.

If x_i is the direct-arc flow, equal pressure drops give

    beta_i x_i^2=4(1-x_i)^2,
    x_i=2/(2+sqrt(beta_i)).

Therefore x_i ranges independently over [1/3,2/3]. Defining z_i=3x_i-1 gives the entire cube [0,1]^n. Its vertices are attained by choosing beta_i=16 for z_i=0 and beta_i=1 for z_i=1. Both endpoint physical states have rational flow coordinates.

The physical graph is a simple cactus. Every cycle has rank one, and bridge attachments give maximum degree three. All numerical network data are bounded constants, apart from graph size.

## 2. Max-Cut becomes a convex flow objective

Use the nonnegative convex quadratic performance function

    F(x)=9 sum_{ij in E(H)}(x_i-x_j)^2
        =sum_{ij in E(H)}(z_i-z_j)^2.

It is a sum of squares of rational linear flow expressions. A convex function on a cube has a maximizing vertex: fix coordinates successively and choose an endpoint that does not reduce the value. At a binary vector z, the objective counts exactly the cut edges of H. Hence

    max_beta F = maximum cut size of H.

The maximum is an integer. Existential weak-threshold attainment for integer K is NP-hard, and robust satisfaction F<=K-1/2 is coNP-hard. On this specific hardware-and-objective family, these are NP-complete and coNP-complete: a binary endpoint choice is a polynomial-size certificate, and its value is an integer cut size. This membership statement is not extended to arbitrary irrational cactus bounds and arbitrary coupled quadratic objectives.

All resistance and nomination magnitudes are constants. The objective has an explicit unweighted sum-of-squares representation; its expanded integer coefficients and threshold have magnitude polynomial in the graph size. Thus hardness persists under unary encoding of numerical data, giving strong NP-hardness in the usual sense. An additive estimate with error at most 1/4 recovers the integer maximum by rounding, giving the stated fixed-accuracy consequence. No claim about a fixed error after normalizing the objective to [0,1] is made.

## 3. Meaning of the coupling

The comparisons in H couple flows from different cactus blocks. If the performance were separable over the cycle coordinates, the endpoint maximization would separate into scalar problems. The example therefore identifies objective coupling, not physical graph complexity, as the source of this worst-case difficulty.

The [cactus flow-region result](../results/potential-flow-cactus-flow-region-and-optimization.md) remains valid: the attainable flow set is a parallelotope, and every convex worst-case objective has an endpoint resistance optimizer. A box is already sufficient for NP-hard convex maximization. Conversely, convex minimization on a box is tractable, and the [continuous-design theorem](potential-flow-cactus-convex-design.md) handles rational recovery from algebraic cycle bounds.

## Attribution and verification

Max-Cut and its quadratic binary formulation are classical; see Section 1.1 of [Del Pia, Dey, and Molinaro](https://arxiv.org/pdf/1407.4798). The [paired source assessment](../notes/potential-flow-cactus-convex-performance-novelty.md) treats this as an explicit passive-network realization of that established mechanism, not a new general hardness argument. No matching restricted passive-network statement was found in that bounded comparison.

Both [the first full audit](../notes/review-potential-flow-cactus-convex-performance-hardness.md) and [the second full audit](../notes/review-potential-flow-cactus-convex-performance-hardness-second.md) passed. They checked the cube realization, bounded numerical data, unit gap, and restricted-family NP/coNP membership.

## Exact checks

[`cactus_convex_performance_hardness_checks.py`](../code/potential_flow_mpd/cactus_convex_performance_hardness_checks.py) passed 5,184 exact rational grid states across all 64 simple comparison graphs on four vertices. It verified the bounded-resistance cube realization, quadratic objective identity, integer cut values at endpoints, and domination of every tested interior point by a cut value. The physical chain was also checked for cactus rank, maximum degree three and acyclic orientation.
