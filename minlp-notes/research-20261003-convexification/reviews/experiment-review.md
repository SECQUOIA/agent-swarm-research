# Independent review of the prospective experiment

The original prospective campaign passes the independent record and metric
audit. All 282 scheduled records are retained, including four worker errors
with unknown cut logs. The separately selected correctness-repair supplement
also passes its record, metric, and coverage audits; it does not replace the
original results. This is internal
review, not external peer review or formal verification.

`audit_experiments.py` independently reconstructs the selection and run plan.
It does not import the campaign selector, orchestrator, summary, or incumbent
checker and never invokes an optimizer. It uses the legacy OSiL parser solely
for the syntax filter expressly required by the protocol. Variable bounds and
counts are independently extracted from XML. The auditor rebuilds exclusions
from the earlier named campaigns, metadata filters, file sizes and hashes,
strata, ranking, selected models, and parser errors.

The reconstructed selection exactly matches the frozen file: 422 eligible
models, including 85 convex, 208 continuous nonconvex, and 129 integer
nonconvex models; ten from each stratum are selected. The reconstructed run
plan has 282 jobs with 5,055 seconds of soft budgets and 8,565 seconds of
phase-specific hard limits. The 9,000-second emergency cap exceeds the sum of
hard limits. This arithmetic does not guarantee completion if orchestration
overhead itself exceeds the remaining margin; unstarted jobs must remain in
the completion table.

Four pre-freeze findings were fixed by the campaign owner:

1. Binary primal checks now enforce the implicit interval `[0, 1]` in addition
   to declared bounds and integrality.
2. Favorable comparisons require recognized solver status and explicit
   incumbent/reference-check state. Missing checks no longer pass by default.
3. Source/model preparation, including serialization and hashing, is charged
   to the soft total budget.
4. Missing-cut accounting includes an explicit incomplete-log flag, even when
   a partial cut list exists.

The harness rotates the three mode orders deterministically, runs one worker,
sets numerical-library thread counts to one, archives source and original
models, retains failures, and separates old diagnostics from the new holdout.
Its source snapshot is made before outcomes. Shared source-domain auxiliaries
belong to every mode; any later cut-specific reformulation would require a
pre-outcome protocol amendment and an appropriate control.

The final primary audit verified 156 frozen source hashes, all scheduled
records, per-run/JSONL agreement, original-file and model hashes, unchanged
parsed models across modes and phases, unknown logs, independently recomputed
incumbent residuals, reference conflicts, solved counts, paired dual comparisons,
and descriptive runtime ratios. All 271 returned incumbents pass the independent
checker; no archived-reference conflict occurs. There are 123 recorded cuts.
The four missing cut logs are the all/auto runs on `chp_partload` and
`waterno2_06`, whose discovery raised `RecursionError`; these are execution
failures after model construction, not evidence of importer rejection.

On the 30-model primary holdout, baseline, all, and auto each solve 25 models.
Relative to baseline, all has 2 better, 21 tied, and 7 worse final dual bounds;
auto has 2 better, 24 tied, and 4 worse. Both-solved median total runtime ratios
are 1.8704 for all and 1.5822 for auto. These are descriptive shared-host results
for the original implementation, whose discovery did not consistently enforce
its existing work budget. They support retaining native baseline as the default;
they do not establish a universal dominance claim.

`audit_experiment_details.py` independently reconciled every reported coverage
counter, classification, and instance record. The primary full holdout produced
cuts in seven all-mode models and three auto-mode models. Each cut mode invoked
the separator in 28 of 30 models; two solved without invoking it. Zero cuts do
not establish hull membership or identify the causal effect of native cuts.

The same independent audit reconstructed the repair selection from the original
records: 46 measured discovery-budget overruns and four identified recursion
failures trigger 25 model/phase/seed groups, with all three original modes
retained in original order. Both independently written plan files select the
same 75 jobs, with 1,575 seconds of soft budgets and 2,565 seconds of hard
limits. The runner plan binds the original records and source manifest by hash.
Selection uses these defects, not objective values, solved counts, or corrected
outcomes. The supplement is a selected regression cohort, not a new prospective
population comparison.

The completed supplement contains all 75 matched records and 103 verified
source hashes. All 67 returned incumbents pass the independent evaluator;
there are no reference conflicts, worker errors, process timeouts, or unknown
cut logs. It records 42 added cuts, whose replay is reviewed separately.
Original primary records and their source manifest retain the same hashes.
Every available matched original parsed model and configuration is unchanged.

In the selected full-run holdout subset, each mode solves four of eight models.
All has zero better, five tied, and three worse final bounds than its matched
baseline; auto has zero better, six tied, and two worse. Each mode solves four
of seven selected diagnostics. Root and seed-one comparisons all tie. These
results do not establish a reason to enable the cuts by default.

Six repaired discovery calls exceed the soft allowance and all explicitly mark
discovery incomplete. The largest excess is 0.003618 seconds. The four original
recursion failures no longer occur; their corrected runs reach the discovery
deadline, discard partial discovery, and continue with native SCIP. This is a
validated fallback, not evidence of newly supported cut blocks on those models
or a hard real-time guarantee. Supplement coverage classifications and every
reported repair-summary counter, timing, paired comparison, and overshoot were
independently reconstructed without importing the producer's analysis code.

The independent incumbent evaluator uses exact
binary rational arithmetic for polynomial operations and ordinary numerical
evaluation for transcendental operations. It is a numerical residual check,
not a proof of feasibility or of SCIP's complete solve. Cut-certificate replay
is reviewed separately.

Command run:

```text
code/minlp_solver_lab/.venv/bin/python research-20261003-convexification/reviews/audit_experiments.py --output research-20261003-convexification/reviews/experiment-preflight-audit.json
code/minlp_solver_lab/.venv/bin/python -m pytest -q research-20261003-convexification/reviews/test_experiment_review.py
code/minlp_solver_lab/.venv/bin/python research-20261003-convexification/reviews/audit_experiments.py --campaign research-20261003-convexification/experiments/campaign-v2 --output research-20261003-convexification/reviews/experiment-campaign-audit.json
code/minlp_solver_lab/.venv/bin/python research-20261003-convexification/reviews/audit_experiment_details.py research-20261003-convexification/experiments/campaign-v2 --runner-plan research-20261003-convexification/experiments/repair-plan.json --review-plan research-20261003-convexification/reviews/repair-selection.json --output research-20261003-convexification/reviews/experiment-details-audit.json
code/minlp_solver_lab/.venv/bin/python research-20261003-convexification/reviews/audit_experiments.py --campaign research-20261003-convexification/experiments/repair-discovery-v1 --repair-plan research-20261003-convexification/experiments/repair-plan.json --output research-20261003-convexification/reviews/experiment-repair-audit.json
code/minlp_solver_lab/.venv/bin/python research-20261003-convexification/reviews/audit_experiment_details.py research-20261003-convexification/experiments/campaign-v2 --runner-plan research-20261003-convexification/experiments/repair-plan.json --review-plan research-20261003-convexification/reviews/repair-selection.json --repair-campaign research-20261003-convexification/experiments/repair-discovery-v1 --output research-20261003-convexification/reviews/experiment-final-details-audit.json
```

Results: selection, schedule, all 282 primary records, all 75 matched repair
records, metrics, coverage, and repair selection passed; four independent
auditor tests passed. The tests
include all 13 analytic witnesses, implicit
binary bounds, exact constant cancellation, preservation of an undefined
subexpression multiplied by zero, and rejection of incomplete or failed check
records. No holdout optimization, project-wide checks, or CI inspection was
performed by this review.
