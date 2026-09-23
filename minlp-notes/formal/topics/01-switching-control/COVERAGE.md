This record maps the selected mathematical claims to Lean declarations.
The verification status is recorded separately in `VERIFICATION.md`.

| Claim | Lean declaration or module |
|---|---|
| Real cumulative endpoint model and rational strict baseline | `ValidProfile`, `StrictProfile`, `baseline_valid`, `baseline_strict` in `Profile.lean` |
| Every strict real profile occurs in the history enumeration | `strict_history`, using `finite_row_history_mem` |
| Five/six ordinary chamber coverage and seven ordinary-or-exception coverage | `Finite.five_cover`, `Finite.six_cover`, `Finite.seven_cover` in `Certificates.lean` |
| Floor/ceiling counts imply real error bounds | `Geometry.fits_discrepancy_le_one` |
| All six exceptional histories have a repair of error at most 4/3 | `Geometry.exceptional_floor_permutation`, `Geometry.exceptional_repair_list` |
| Nonintegral profiles approximate all boundary profiles without losing the switch budget | `Boundary.extend_strict_bound`, `extend_to_boundary` |
| Uniform unit-grid endpoint upper bounds | `five_cells`, `six_cells`, `seven_cells` |
| Matching lower-bound inputs against every budgeted word | `SevenWitness.five_real_lower`, `six_real_lower`, `real_lower` and the list/array bridge in `Sharpness.lean` |
| Exact unit-grid endpoint minimax values | `five_grid_exact`, `six_grid_exact`, `seven_grid_exact` |
| Positive cell-length scaling | `grid_scaling`, `five_grid_scaled`, `six_grid_scaled`, `seven_grid_scaled` |
| Full-time bounds for arbitrary words and cell lengths | `GridContinuous.scaled_measurable_grid_upper_of_endpoint` |
| Exact five/six/seven measurable-input grid values at every positive cell length | `five_measurable_grid_exact`, `six_measurable_grid_exact`, `seven_measurable_grid_exact` in `GridResults.lean` |
| Measurable realization of all grid sharpness profiles | `GridWitnesses.five_realization`, `six_realization`, `seven_realization` |
| Continuous lower bound for every three-block schedule and arbitrary real switch times | `Continuous.three_block_lower_bound`, `scaled_three_block_lower_bound` |
| Measurable simplex rates are integrable and give valid cumulative controls | `Measurable.rates_integrable`, `cumulative_increments`, `cumulative_conservation` |
| Five-cell schedules give an actual continuous two-switch schedule | `ContinuousGrid.continuous_upper_of_five_grid` |
| Exact continuous value T/5 for every positive horizon, including the measurable input class | `ContinuousResults.continuous_three_mode_two_switch_minimax`, `measurable_three_mode_two_switch_minimax` |

The finite certificates contain actual witness words, and the coverage proof
checks every transition branch. They do not take the original checker output
or the Python dynamic program as axioms. The lower bounds quantify over all
competing schedules, including arbitrary real switch times for the continuous
problem; they are not comparisons against a finite sample of switch times.

The package does not prove the automaton's converse realizability statement,
the chamber-count recurrence, the optimal-switch histograms, the count of
104 words in one chamber, or the original dynamic program's optimality.
These are unnecessary for the exact minimax bounds, whose proof uses complete
coverage and explicit schedules. It also does not determine the unresolved
continuous three-switch value or verify bibliographic novelty and priority.
