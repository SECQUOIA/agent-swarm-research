# Prospective compact solver study

This protocol is fixed before comparative outcomes from the current campaign.
It tests a limited integrated OBBT prototype, not a claim of superiority to all
published adaptive OBBT methods. The inputs include synthetic stress cases and a
deterministic public cohort selected using historical, separate experiments.

## Admission

Public eligibility uses the September 22 study's frozen metadata and outcomes:
historical scope admission; 5–300 variables; 1–200 nonlinear variables; at most
500 distinct quadratic terms; and at least five seconds in *both* historical
native SCIP baseline runs (or every available baseline run). Sort eligible names
by SHA-256 of `adaptive-obbt-v1/` followed by the name. Take the first twelve,
at most one per historical family. Record the entire ordered eligibility list.
Neither current arm outcomes nor known optimum values enter this rule. Admission
failures and unsupported OBBT cases stay in the cohort.

Eight synthetic models use four structures and two sizes: point packing (5 and
7 points), coupled square budgets (12 and 24 variables), bilinear cycles (12 and
20 factors), and sparse indefinite QPs (20 and 36 variables). The generator seed
is 20261003. These are stress tests, not a representative application sample.

Tiny pilot models use different sizes/seeds. Pilot results check API operation,
validity, and callback coverage only; they are excluded from reported comparisons.
Policy parameters are frozen before holdout outcomes. Any subsequent policy bug
fix requires a separate source snapshot and a new complete campaign; a failed
campaign remains recorded rather than silently overwritten.

## Arms and resources

Run all twenty models with SCIP random seed shifts 0 and 1 in three arms:

- `native`: the same SCIP defaults without the additional OBBT plugin;
- `fixed`: additional integrated OBBT with a fixed directional LP allowance;
- `adaptive`: the same allowance plus prospective screening/stopping/retriggering.

The exact policies and numeric defaults are recorded in the campaign source
snapshot and configuration. Native SCIP OBBT remains enabled consistently in all
arms: this study tests an *additional* policy, not the isolated effect of OBBT.
No known optimum, reference feasible solution, or external warm start is used.

Each call has a ten-second inclusive construction/optimization budget, with all
sidecar work charged. The worker additionally measures process elapsed time,
including Python startup, parsing, output, and validation. Report that elapsed
time separately; never present the solver's optimization timer as total cost.
SCIP and numerical libraries use one thread; at most two workers run concurrently.
A process hard limit protects against a stuck call and counts as failure.
The predeclared task order is shuffled with seed 20261003 to mix arms and seeds.

## Outcomes

Retain every original solver log, input hash, incumbent, status, exception,
elapsed time, node count, primal/dual bound, gap, and OBBT trace. Validate each
returned incumbent against original variable bounds, integrality, all original
quadratic rows, and the original objective. Report absolute residuals and scaled
residuals; an incumbent passes the declared numerical check if its maximum scaled
residual and integrality residual are at most 1e-6. This is a floating-point
diagnostic, not exact certification. A solver optimal status with an invalid
incumbent is a failed run, not a success.

Report all 40 model-seed pairs per arm, as well as public and synthetic strata:
number solved, no-incumbent count, invalid-incumbent count, failures, total elapsed
time, shifted geometric mean time with one-second shift, and PAR-2 using twice
the ten-second budget for unsuccessful runs. Successful run cost includes setup
and validation; process overhead and limit overshoot remain visible separately.
Do not restrict timing comparisons to cases solved by every arm. Report paired
wins/losses and final gap comparisons only with their exact eligibility counts;
do not silently drop missing incumbents or missing finite dual bounds.

Interpretation is restricted to this small, short-budget, selected cohort. Two
seeds are repeated runs of each model, not forty independent problem families.
No speedup claim is warranted from lower node counts, stronger bounds, or a few
selected wins alone. Any follow-up must state its distinct unresolved question.
