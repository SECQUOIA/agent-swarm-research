# Independent solver and evidence review

This review checks the implemented research prototype and its evidence pipeline.
It does not certify SCIP's complete nonlinear search or establish that adaptive
allocation of solver effort is a closed research topic.

## Findings addressed before the comparative campaign

- **The construction budget was initially excluded from the SCIP time limit.**
  The solver now subtracts construction and setup from its inclusive deadline,
  avoids optimization if setup exhausts that deadline, and checks both the
  plugin budget and the overall deadline. Setup and individual external calls
  are not interruptible at arbitrary instructions; measured overshoot remains
  part of the reported cost.
- **Frozen worker code was initially copied but not executed.** The experiment
  runner now launches the archived runner with an explicit experiment root.
  Archived solver and model modules are imported by that worker. A resumed
  campaign verifies source hashes.
- **Ordinary objective summation could invalidate even a feasible incumbent's
  cutoff.** At `x=y=1`, `1e16*x^2 + x*y - 1e16*y^2` has exact value 1 for the
  stored coefficients, but sequential floating-point summation can give 0.
  A small relative pad does not repair that cancellation. The solver now
  evaluates the incumbent objective with exact dyadic arithmetic and rounds
  its cutoff upwards. Independent outcome validation also evaluates the
  objective exactly before converting its reported value to floating point.
- **Finite coordinates did not imply finite validation arithmetic.** Validation
  now rejects nonfinite row, scale, or objective evaluation. An invalid incumbent
  cannot count as a solved run.
- **A dual bound above a validated primal bound could appear to have zero gap.**
  Analysis now identifies inconsistent bounds instead of silently presenting
  them as a successful zero-gap result.

## Mathematical and implementation boundaries

The sidecar constructs outward relaxations of the original quadratic rows on a
finite local box. Its coefficient-rounding correction uses exact dyadic
arithmetic. Its LP dual bound uses nonpositive inequality multipliers and a box
minimum of the residual objective, with directed rounding. Therefore imperfect
LP dual feasibility does not justify an optimistic directional bound. A numerical
LP infeasibility or other unsuccessful LP status produces no bound and never
prunes a node.

The objective cutoff remains conditional on primal feasibility. Its value is
now evaluated conservatively, and the source point passes an original-model
numerical feasibility guard, but small feasibility residuals are not an exact
feasible-point certificate. Exact arithmetic in the sidecar does not turn this
ordinary numerical SCIP experiment into an exact global solve certificate.

Bounds are applied through SCIP's local tightening APIs to transformed
counterparts of the original variables. Each sidecar is rebuilt from the current
node's box. Sibling scheduling state is separate. Stored witnesses are checked
against the complete current LP before use; square tangents remain valid when
reused outside the box where they were generated. Screening establishes a fact
about the current LP and an endpoint tolerance, not immunity to arbitrary later
cuts, propagation, or integer rounding.

All plugin setup, LP solving, witness validation, and applied-bound work occur
inside the inclusive solver call. The plugin's detailed time counter covers its
entered work; cheap callback rejections and Python/process startup still appear
in total process time. The implementation has bounded calls, directions, cache
size, and a time allowance. These budgets do not imply a runtime advantage over
native SCIP.

## Independent checks performed

`reviews/test_solver_review.py` contains nine checks authored separately from
the implementation tests:

1. Exact rational containment of true square and bilinear graph points in signed,
   fixed, very small, and very large finite boxes.
2. One hundred arbitrary multiplier cases comparing the returned dual bound with
   an exact rational Lagrangian box bound, across three coefficient scales.
3. Actual HiGHS directional bounds with both objective senses and a nonzero
   objective constant.
4. Unsuccessful LP statuses, including numerical infeasibility, returning no bound.
5. Revalidation of stored witnesses after sibling-domain and cutoff changes.
6. Local callback applications on opposite sibling boxes and conservative integer
   domain rounding, using a controlled model double.
7. The catastrophic objective-cancellation cutoff regression above.
8. Actual SCIP solutions of a small integer QCQP whose optimum is independently
   enumerated, in all three arms, with original-variable reconstruction checked.
9. Exhausting the inclusive construction budget in each arm skips optimization
   and returns an explicit setup-limit outcome.

`reviews/check_source_models.py` interprets the archived OSiL XML directly,
without importing the historical parser. It verifies input hashes, bounds,
variable types and names, constraint constants, linear sparse-matrix orientation,
and objective/row values at five deterministic probes on each of the twelve
public models. The compressed source files and frozen interchange agree in all
these checks. This is an independent implementation check, not a formal proof
of the OSiL standard or a general parser certification.

Targeted commands actually run from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 code/minlp_solver_lab/.venv/bin/python research-20261003-adaptive-obbt/reviews/test_solver_review.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 code/minlp_solver_lab/.venv/bin/python research-20261003-adaptive-obbt/reviews/check_source_models.py
```

Results: nine solver review tests passed; twelve source models passed five
probes each. Project-wide verification and CI inspection were not performed.

## Comparative evidence review

The prospective protocol schedules every model, seed, and arm. The analysis
retains every scheduled run and charges unsuccessful runs in PAR-2. It does not
restrict runtime comparisons to instances solved by every arm. Public and
synthetic strata are kept separate, and two seeds are not treated as independent
problem families. Numerical invalidity and process/exception failure are
reported separately; both prevent a run from counting as solved.

The independent campaign audit completed successfully. It checks the complete
Cartesian product of twenty models, two seeds, and three arms; all 120 raw
results and logs; every archived source and model hash; the configuration hash;
and independently recomputed solved counts, PAR-2 means, and process-time totals.
It does not import the experiment analyzer. Direct XML evaluation also agrees
with the interchange at all 69 returned public incumbents.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 code/minlp_solver_lab/.venv/bin/python research-20261003-adaptive-obbt/reviews/check_source_models.py --campaign campaign-01
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 code/minlp_solver_lab/.venv/bin/python research-20261003-adaptive-obbt/reviews/check_campaign.py campaign-01
```

| Arm | Solved, all 40 runs | Mean PAR-2 seconds | Solved public runs | Solved synthetic runs |
|---|---:|---:|---:|---:|
| Native | 14 | 13.855128 | 2/24 | 12/16 |
| Fixed | 14 | 13.988118 | 2/24 | 12/16 |
| Adaptive | 14 | 13.996928 | 2/24 | 12/16 |

Neither added policy gained or lost a solve relative to native SCIP. Both had a
higher mean PAR-2 cost. Among 39 pairs with finite valid gap data, adaptive OBBT
had four gap improvements and twelve deteriorations at the declared absolute
threshold of `1e-4`; fixed OBBT had five improvements and twelve deteriorations.
These observations do not establish a runtime advantage or general inferiority
of adaptive OBBT beyond this short, selected cohort.

There were no process/exception failures, numerically invalid returned
incumbents, reported-objective mismatches, or inconsistent primal/dual bounds.
Each arm had one run without an incumbent. The four integrated `qp3` runs
(two arms and two seeds) retained their unsupported finite-box status: each
recorded 24 unbounded-box skips, no sidecar bound, and no plugin exception.
They remain in all aggregate comparisons.

The 78 time-limited calls exceeded the nominal ten-second call budget by at most
0.0929991 seconds. Actual process costs and unsuccessful-run penalties remain
visible; no overshoot was silently subtracted. The adaptive policy used fewer
LP calls than the fixed policy (1,719 versus 2,172) but more total measured
plugin time (23.123433 versus 19.529969 seconds), illustrating why LP counts
alone do not measure computational benefit.

One recovery-only driver defect was found after this campaign started:
resuming an incomplete task could overwrite its partial log. The current driver
now archives incomplete attempts before a retry. The campaign's archived source
was left unchanged, and this uninterrupted campaign used no retries. This
post-freeze repair therefore does not change any measured policy or outcome.

**Review conclusion:** the scoped prototype and campaign pass the checks above.
The evidence supports reproducible negative computational findings and the
stated conditional inference guarantees. It does not support recommending this
policy as a faster default or describing general adaptive effort allocation as
fully solved.
