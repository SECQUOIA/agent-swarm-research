# Joint weighted cactus investigation closeout

Date: 2026-09-06.

The complete theorem, proofs, corollaries, independent reviews, and source comparison are now in [Joint continuous-resistance and weighted-potential optimization on cacti](../results/potential-flow-joint-weighted-cactus-accuracy-bits.md).

The central step eliminates every cycle resistance interval using one-equality box-LP duality. Equal objective weights are retained as one interval of aggregate contributions, avoiding exponential tied-endpoint enumeration. Optimizing each resulting quadratic over its scalar circulation produces only rational or quadratic-radical candidates with constant quadratic leading coefficients. Uniform rational approximation and a fixed-dimensional common partition then permit arbitrary weighted objectives and arbitrarily many cycles.

The reviewed result covers fixed-dimensional affine nomination families with arbitrary objective support, and composes with the independently reviewed nomination-face theorem to cover arbitrary balanced nomination boxes at fixed objective support. Both versions return rational epsilon-optimal original nomination and resistance parameters. Local arc capacities can be added to the fixed-dimensional version with exact feasibility decision and algebraic output; rational output under a supplied tightening margin is compared with the tightened optimum.

A final exact refinement is especially useful: at fixed rational nominations, even with rational local arc capacities, every feasible instance admits an exactly optimizing rational resistance profile computable in polynomial time. Irrational circulation candidates can only arise at aggregate feasibility boundaries, which force the tied resistances to rational endpoints. Flat local objectives are handled by choosing a boundary. Local values have algebraic degree at most two; the global sum is kept as a sum, without an exact global threshold-comparison claim.

Both [the first independent review](review-potential-flow-reopened-joint-weighted.md) and [the second independent review](review-potential-flow-reopened-joint-weighted-second.md) passed the complete proof and the exact fixed-nomination refinement. The [source comparison](potential-flow-reopened-weighted-literature.md) found no matching combined theorem while crediting the established affine-ray radical formulas, resistance-uncertainty models, cycle feasibility reductions, algebraic approximation, and LP duality. This is a bounded source search, not exhaustive novelty clearance.

The author [local checker](../code/potential_flow_mpd/reopened_joint_weighted_checks.py) and the two independent review checkers are retained. The exact proofs and mechanism checks do not constitute a full implemented varying-nomination optimizer.
