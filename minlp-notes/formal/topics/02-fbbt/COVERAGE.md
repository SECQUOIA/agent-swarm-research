The selected iteration theorem is separate from the appendix's PosSLP hardness theorem.

| Claim | Formal declaration or file |
|---|---|
| Actual constant-coefficient input syntax | `CircuitVar`, `PrimitiveRhs`, `circuitRhs` |
| Exactly `4n + 4` variables and equations | `circuit_variable_count`, `circuit_equation_count` |
| At most three names per equation; distinct product arguments | `circuit_equation_names`, `circuit_product_distinct` |
| Exact paired squaring, complement, and feasible point | `bValue_inverse_power`, `cValue_succ`, `circuitPoint_solution`, `circuitPoint_mem_unit` |
| Unique feasible point | `circuitSolution_unique` |
| Only feedback variables can belong to a directed cycle | `circuit_cycle_only_feedback`, `circuit_feedback_cycle` |
| True minimal interval hull; existence by real infimum/supremum | `Box.IsHull`, `Box.hull_isHull`, `Box.contract_step` |
| Soundness, contraction, monotonicity, actual runs | `Box.step_preserves`, `step_contracts`, `step_mono`, `iterate_run` |
| Exact simultaneous product and affine feedback hulls | `Good.product_hull`, `Good.affine_hull` |
| Exact-upstream trajectory is a real full-circuit primitive run | `strongRun_isRun` in `Lift.lean` |
| Original unit-box run is no faster | `PrimitiveRun.le_strong` |
| Geometric and Bernoulli bounds after K designated updates | `PrimitiveRun.geometric_bound`, `PrimitiveRun.linear_bound` |
| Doubly exponential designated and total update lower bounds | `PrimitiveRun.threshold`, `PrimitiveRun.total_updates` |
| No finite primitive run reaches the limiting lower endpoint exactly | `PrimitiveRun.z_lt_one` |
| Full original-box fair limit | `PrimitiveRun.singleton_limit` |
| Nonvacuity: actual runs for every schedule and an explicit fair schedule | `originalRun_isRun`, `roundRobin_fair`, `canonical_slow_run` |
| Small local endpoint changes despite unit distance to the limit | `initial_small_changes`, with exact upstream initialization |

The proof does not assume forward-only updates, a prescribed sweep order,
exact upstream initialization in the original run, or a bounded fairness
delay. The stronger initialization is constructed and compared to the
original run through proved hull monotonicity.

The residual statement concerns the stronger initialization with exact
upstream values. It does not say all changes in the original uninformative
unit box are initially small. The circuit syntax contains no expanded tiny
input coefficient: repeated squaring generates it internally.

The exact equation/variable counts are formal. A binary serialization and its
`O(n log n)` bit-length estimate are not formalized. The companion PosSLP
hardness reduction, publication novelty, and claims about floating-point
implementations or accelerated global contractors are outside this package.
