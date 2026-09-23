# Independent review of the fixed physical grid benchmark

Date: 2026-09-12. Reviewer: `/root/physical_grid_review`, separate from the
benchmark author `/root/structured_oracle_review`.

**The completed benchmark and separate refined transfer pass this bounded
independent review.** No substantive implementation defect was found. The
results support the narrow conclusion that the tested pipeline loses its
coarse-grid performance under a fixed physical covariance and observation
budget. They establish neither necessary exponential memory nor a general
ranking of solvers. Every optimization bound here remains numerical.

The review examined the [benchmark driver](../code/research_20260912/fixed_physical_grid_benchmark.py),
[completed result](../code/research_20260912/results/fixed-physical-grid-benchmark.json),
[refined transfer driver](../code/research_20260912/fixed_physical_grid_refined_transfer.py),
[transfer result](../code/research_20260912/results/fixed-physical-grid-refined-transfer.json),
and [author note](research-20260912-fixed-physical-grid-benchmark.md), after the
original run completed. The benchmark source hash is
`12caf86c1f319dd3fe53c9b1b55b1f7d310090faf9278b15c86dd5a3e5bed136`;
the transfer source hash is
`62cf2fd22c7b186b2c2c7ae9e3e8c57b92d82a50d4cc07f27d205213b2465e05`.
The [fresh checker](../code/research_20260912/review_fixed_physical_grid_benchmark.py)
and [saved review report](../code/research_20260912/results/fixed-physical-grid-independent-review.json)
retain their hashes, input hashes, environment, checks, errors, and limitations.
No author or solver source was changed by the reviewer.

The three grids represent one physical model. Their times are exactly
`12*(j+1)/n`, with `n=48,96,192`, and all these times are exactly representable
binary numbers. The rational correlations satisfy
`rho48=(4/5)^4`, `rho96=(4/5)^2`, `rho192=4/5`, corresponding to the same
decay rate `lambda=-16*log(4/5)`. The checker verified every distinct
shared-grid covariance lag in exact rational arithmetic and bit-identical
saved sensitivity rows at all shared times. The actual solvers use floating
approximations to this declared rational covariance; rational input strings
do not make their arithmetic exact. The prior, latent and nugget variances,
three parameter coordinates, horizon, and cardinality `k=16` are fixed.

The saved mean and sensitivities also agree with an independent integration
of the augmented reaction mass balances. This check does not import the
author's analytic formula or its complex-step reference. Across 336 times,
the maximum sensitivity discrepancy is `1.61e-13` and the maximum mean
discrepancy is `9.30e-14`.

The preflight uses the correct two distinct quantities:
`-p*log(1-delta)` for an upper-bound transfer and
`p*log((1+delta)/(1-delta))` for the two-sided loss guarantee of a surrogate
optimizer. The latter concerns optimization over the same feasible family;
closing the continuous hull alone does not supply a discrete surrogate
optimizer. Neither component alone guarantees a final discrete gap of 0.01.

The checker independently rebuilt the workspace formula and all 80 saved
window rows. It evaluated the old delta using exact geometric sums and the
refined gap-one delta using a separate scalar conditional-variance recursion
and finite pair row sums. All 12 first-sufficient-window entries agree.
The refined one-sided thresholds are 7, 15, and 35; the two-sided thresholds
are 7, 17, and 38. The largest windows passing the implemented 256 MiB
workspace estimate are 14, 14, and 13. These are sufficient-bound and
implementation-workspace statements, not lower bounds on all methods.

All scheduled runs passed their workspace preflight. **There is no actual
memory refusal in the saved experiment.** Larger-window memory figures are
estimates. The reported process RSS reaches 418.41 MiB and is correctly
labeled as a cumulative process high-water mark. It cannot be compared with
the 256 MiB workspace estimate as if either were an isolated per-method
memory measurement or a hard process cap.

The seven recorded method rows reconstruct as follows. Gaps use the shared
heuristic whenever it supplies the better true feasible objective.

| Grid and method | Pipeline seconds | Original numerical gap | Refined-transfer gap |
| --- | ---: | ---: | ---: |
| 48, hull `L=8` | 0.77134 | 0.00847831 | 0.00597119 |
| 48, dense OA | 30.04823 | 0.16121869 | — |
| 96, primary hull `L=14` | 30.00165 | 2.36808189 | Unavailable |
| 96, dense OA | 30.02763 | 0.41547338 | — |
| 96, separate hull diagnostic `L=12` | 28.04587 | 0.09717224 | 0.03709665 |
| 192, primary hull `L=13` | 30.00151 | 2.68868608 | Unavailable |
| 192, dense OA | 30.02405 | 0.67249899 | — |

The checker reconstructed every returned and combined true objective by a
direct selected-covariance solve. The maximum method-objective discrepancy
is `7.11e-15`. It also exhausted all 4,608 single exchanges of the three
shared schedules. None improved its recorded incumbent, independently
confirming each returned single-exchange local-optimum status.

All 14 saved local-information support matrices and all four hull mixtures
were reconstructed from covariance principal blocks. For both completed
hull prices, the reviewer computed the global linear maximum with a separate
vectorized count/history recurrence. Stationarity allows one regression per
history mask; this checker does not call the production calendar oracle or
reuse its path cache, arc arrays, or predecessor implementation. Both ordinary
prices and both prior-aware prices agree within `8.89e-16`. Their saved
priced paths attain those maxima. The associated tangent formulas, prior
correction, spectral transfer, and minimum with the full-selection bound
reconstruct within `7.11e-15`.

The two finer-grid primary runs have one generated path and zero completed
pricing rounds. Their saved seed information shows that oracle construction
and initial evaluation completed. They are first-pricing timeouts. No
surrogate upper bound or pricing witness exists in either result, and each
retains the separately valid full-selection upper bound. The author note
preserves this distinction. The additional 96-point `L=12` run was chosen
after the primary failure, has its own charged pipeline, and remains a
separate diagnostic rather than a replacement observation.

The refined transfer routes the correct stored surrogate upper bound to
`U_surrogate-p*log(1-delta_refined)` and takes the minimum with the previous
true upper bound. The reviewer independently reproduces both exact rational
delta strings, every transferred value and gap, source hashes, and row
indices. Cases without a completed surrogate upper bound remain unavailable.
No extra spacing restriction is introduced: gap one is the distinct-time
family already used. These checks do not turn a floating-point surrogate
upper bound into an exact certificate. The recorded sub-millisecond
reanalysis times measure each row's bound computation, excluding process
startup and artifact input/output.

The pipeline accounting correctly charges the same measured shared heuristic
generation to each alternative, plus its data/preflight setup and complete
solver invocation. The outer invocation timer includes the return and
cleanup path; the dense implementation uses context-managed Gurobi resources.
Recorded postprocessing and overruns are added explicitly. The largest saved
overrun is 0.04824 seconds. This is a cooperative nominal 30-second budget,
not a hard wall-clock kill. Historical timings and RSS cannot be independently
recreated from JSON; the checker verifies their arithmetic and labels.

Controlled clock tests exercise all three grids with successful solver
returns, injected solver exceptions, and exhausted shared budgets. They
confirm deduction of shared construction time, charging of a simulated
quarter-second cleanup overrun, retention of exception details and the shared
incumbent, and absence of an invented upper bound after failure. An exhausted
shared budget prevents further solver calls. These tests also retain the
separate adaptive diagnostic in the failure branch.

Small real solver checks use eight candidates and three observations. The
56-subset enumerated optimum lies between the returned hull and dense bounds;
three independent pricing recurrences agree with exhaustive enumeration.
A tiny forced workspace refusal returns before oracle construction. No
saved 30-second MIP was rerun. The full review checker completed in about
0.82 seconds in the recorded one-thread environment; that checker timing is
not an end-to-end benchmark result or a substitute for the production runs.

The dense artifact does not retain its complete cut history or a replayable
dual certificate. Its saved upper-bound arithmetic and assumptions were
checked, and the tiny solver test provides limited additional confidence;
the three historical MIP upper bounds were not independently certified. All
three continuous roots stopped at the 200-round limit with gaps about
0.06846, 0.24890, and 0.46468. The recorded comparison therefore concerns
this prototype and these stopping rules. Faster evaluation alone does not
establish that those master gaps disappear.

This is a useful test of the scaling concern in the
[impact assessment](research-20260912-impact-assessment.md). It retains the
original stipulated small reaction model and synthetic covariance, without
fitted experimental noise or a demonstrated consequential operational
decision. Its local criterion also retains the documented rate-swap scope
limitation. One run per case cannot establish stable timing distributions.
The present findings justify a limitation claim about the tested pipeline;
they do not establish a substantial practical MINLP contribution by themselves.
No new external literature source was needed for this bounded code and
artifact review.

Reproduce the review from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
uv run --project code/research_20260912 python \
  code/research_20260912/review_fixed_physical_grid_benchmark.py
```
