This package covers the mathematical disaggregation and chain-profile results,
including exact two-label and three-label hull tests. It does not certify every
claim in the network–simplex manuscript.

| Source claim | Lean statement or module | Scope |
|---|---|---|
| `prop:disaggregation` | `NetworkSimplex.mem_convexHull_graph_iff`, `disaggregation_decomposition` in `Disaggregation.lean` | Both directions for arbitrary linear balance maps, finite simplex states, capacities, and sparse observations; decomposition into at most one graph point per state |
| Original simplex coordinates and residual state | `original_mem_hull_iff`, `original_hull_iff_lift` in `SimplexEncoding.lean` | Actual hull with y nonnegative and sum at most one; residual weight is one minus the sum; observations use explicit labels |
| Zero states and empty flow systems | `flow_zero_iff`, `disaggregated_empty_of_flow_empty` | No positive-weight or nonempty-base assumption hidden in the general hull equivalence |
| Flat-chain network model | `incidence_eq_sum`, `demand_eq`, `conservation_iff`, `flow_iff` in `Chain.lean` | Incoming-minus-outgoing incidence on the actual parallel-pair chain and bypass, unit capacities and demand |
| `prop:chain-profile` | `profile_iff_stateFlows`, `mem_chainHull_iff_profile`, `ReductionData.mem_hull_iff` | Both directions, arbitrary length and observation patterns; actual convex hull, state-flow recovery, observed nonnegativity, zero weights |
| Residual elimination, equations `chain-residual-reduced` and `chain-endpoints-reduced` | `fullProfile_restore_iff`, `exists_fullProfile_iff_rows` in `Reduction.lean` | Arbitrary finite number of explicit labels; residual state unobserved; its bounds retained |
| Repeated-normal grouping | `grouped_iff_reducedProfile` in `GroupedProfile.lean` | Finite minima of matching row bounds; empty-subset zero checks retained; redundant box consequences provide any missing normal groups |
| Five-test feasibility and recovery in `thm:two-state-chain` | `five_tests_iff_feasible`, `five_tests_witness`, `two_tests_iff_fullProfile` | Exact interval feasibility and the explicit max-based witness for arbitrary real bounds |
| Two-label actual hull oracle | `mem_hull_iff_five_tests` in `Results.lean` | Domain and zero-row checks plus five tests, after substituting b-arc flow balance |
| Sixteen tests in `thm:three-state-chain` | `ThreeStateBounds.sixteen_tests_iff_feasible`, `three_tests_iff_fullProfile` | Necessary and sufficient for arbitrary real bounds, with a constructive feasibility proof |
| Displayed 7+5+3+1 circuit library | `weight_nonnegative`, `normal_cancellation`, `weight_injective`, `minimal_support`, `circuit_tests_iff_feasible` in `Circuits.lean` | All sixteen are distinct nonzero nonnegative minimal dependencies; last row has weight two on the negative total normal; their tests exactly characterize feasibility |
| Three-label actual hull oracle | `mem_hull_iff_sixteen_tests`, `mem_hull_iff_circuit_tests` in `Results.lean` | Exact mathematical hull membership, including every original row group |

The circuit library's sufficiency for all right-hand sides is proved. A separate
classification theorem saying every support-minimal positive dependence is a
scaled listed circuit is not included in this package.

Not formalized in this package: integral-flow equivalence or total unimodularity; block
factorization and state merging; the manuscript's other network families;
general-state determinant or circuit-count bounds; unit-coefficient repairs and
the sharp four-label obstruction; arithmetic-operation and bit-complexity
bounds; executable rational parsing, separation, or recovery software; novelty
and literature comparisons. The state-flow proof uses proportional interval
allocation, so it proves recovery existence without certifying the paper's
particular greedy implementation or operation count.

The later [flat-chain threshold package](../15-flat-chain-threshold/COVERAGE.md)
covers circuit classification, determinant and coefficient bounds, the sharp
four-label obstruction, observed-label state merging, and rational separation
and greedy recovery with arithmetic and bit bounds. Its coverage record states
the remaining scope limits; the exclusions above describe topic 06 only.

The proofs use real arithmetic and Mathlib's `convexHull`. They establish exact
equivalences, including sufficiency and recovery, rather than numerical checks
of selected instances. Each finite circuit calculation is checked by the Lean
kernel; no external optimization solver supplies a proof premise.
