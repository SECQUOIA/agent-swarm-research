# Integrated OBBT experiment

The comparison does not justify enabling this additional OBBT policy by default.
Native, fixed, and adaptive policies each solved the same fourteen of forty
model-seed runs. Adaptive OBBT used fewer directional LPs than fixed OBBT, but
spent more total time in its sidecar and did not improve overall solving time.
The implementation demonstrates screening, selective continuation, and
node/incumbent retriggering; it does not establish an optimal allocation of solver
effort or superiority to every published selective OBBT method.

## Protocol and reproducibility

The [protocol](frozen/PROTOCOL.md) and [twenty-model manifest](frozen/manifest.json)
were frozen before current comparative outcomes. The manifest SHA-256 is
`efd5727e9a427a1a8238ff0ff0a34809a7c9ca64ab65476d96539cb421591b73`.
Its public candidates, deterministic ordering, family exclusions, selected names,
historical eligibility evidence, and input hashes are retained. Original OSiL
files are compressed in `frozen/osil/`; the complete experiment can run from
`frozen/models/` without the cache or reference-solution files.

The public stratum contains twelve QCQPs whose native SCIP runs in the separate
September 22 study took at least five seconds. Admission also limits dimensions
and quadratic terms. Consequently, it is a selected challenge set, not a random
sample of MINLPLib. The historical family labels separate several packing
families that remain closely related applications. The synthetic stratum has
two sizes each of point packing, coupled square budgets, bilinear cycles, and
sparse indefinite QPs. No known optimum or externally supplied feasible point
is used in the comparison.

Each model is run with seed shifts 0 and 1 under native, fixed, and adaptive
policies: 120 scheduled runs, 40 per arm. The call budget is ten seconds and
includes model construction and sidecar work. A fresh process records its full
elapsed time, including imports, parsing, validation, and output. An independent
thirty-second hard limit catches stuck calls. Exact installed versions and
machine metadata are stored in [campaign.json](runs/campaign-01/campaign.json).
This campaign uses SCIP 10.0.2 and PySCIPOpt 6.2.1, with two simultaneous workers
and one thread per solver/numerical library. Other unrelated studies run on the
same 36-logical-CPU machine. Starting load averages were 17.76, 15.65, and 14.11;
these timings describe a shared machine and do not support claims about small
timing differences.

The frozen [solver source](runs/campaign-01/source/adaptive_obbt.py),
[worker](runs/campaign-01/source/run.py),
[model validator](runs/campaign-01/source/models.py), and
[analysis](runs/campaign-01/source/analyze.py) are archived before holdout runs.
Each worker executes these archived files. A source fix would require a separate
complete campaign. Completed attempts are never silently overwritten.
During the uninterrupted campaign, a review found that an interrupted attempt
could have been overwritten by the driver's resume path. The current driver
now archives incomplete raw files and logs before retrying. This recovery-only
change did not alter the running campaign, its frozen source, its policies, or
any measured attempt; a separate focused recovery test passed.

## What the comparison changes

All arms use the same model construction and native SCIP settings. SCIP's native
LP-based OBBT remains at its default root frequency; native nonlinear OBBT is
disabled by default. The fixed and adaptive arms add a local propagator with at
most 64 directional LPs, 24 callbacks, and ten percent of the call's time budget.
Each root callback allows twelve directional LPs and each nonroot callback four.
The common scheduler considers new nodes, a one-percent incumbent improvement,
or a ten-percent local domain change; at most three callbacks per node are used.

The adaptive policy also ranks variables by their quadratic coefficients and
current widths, screens directions using revalidated feasible witnesses of the
current LP relaxation, and stops a callback after an unproductive two-direction
pilot. Its cutoff uses SCIP's own numerically accepted incumbent and an outward
objective evaluation. Local bound proposals use corrected dual lower bounds,
with conservative arithmetic in the sidecar relaxation. These features do not
make an entire SCIP solve an exact certificate.

The complete numeric configuration is stored in each raw outcome. No parameter
was tuned using held-out outcomes. The comparison measures the combined policy;
it is not a factorial ablation of each individual feature.

## Outcome definitions

Only an `optimal` status with a numerically valid original-model incumbent counts
as solved. Original bounds, integrality, quadratic rows, and objective are
checked. Row and bound residuals are reported both absolutely and with the
predeclared scaling; the acceptance threshold is 1e-6. Objective evaluation sums
the stored binary coefficients and point exactly before converting once to a
float. A material primal/dual inconsistency or discrepancy between reported and
independently evaluated objective prevents classification as solved.

This is numerical feasibility checking, not an exact feasibility proof. The
independent review additionally compares normalized inputs against a separate
direct OSiL evaluator. That checks model interpretation and reconstruction; it
does not certify all floating-point computations inside SCIP.

The primary timing summary is mean PAR-2 over **all** forty runs per arm: full
process cost for success and twenty seconds for an unsuccessful run. A timeout,
no-incumbent run, invalid incumbent, or process failure is retained. We also
report observed total process time and its one-second-shift geometric mean.
Capped shifted means use `min(process_seconds, 10)` and are diagnostic only:
they can conceal overshoot and do not penalize a fast unsuccessful termination.
No comparison selects only instances solved by every arm.

For final-gap diagnostics, use
`max(0, primal-dual)/max(1, abs(primal), abs(dual))`. The all-run gap score caps
this quantity at one and assigns one if a valid incumbent or finite, consistent
dual bound is unavailable. Paired finite-gap comparisons state their eligible
denominator separately. Two seeds are repetitions of each model, not additional
independent problem families.

## Results

All 120 scheduled attempts completed. The [frozen analysis](runs/campaign-01/summary.json),
[per-run table](runs/campaign-01/outcomes.csv),
[diagnostics](runs/campaign-01/diagnostics.json), and
[raw/log/source hashes](runs/campaign-01/artifact_hashes.json) retain the complete
evidence. The primary table is:

| Cohort | Policy | Solved | Mean PAR-2 (s) | Uncapped process shifted mean (s) | Mean gap score |
|---|---|---:|---:|---:|---:|
| All | Native | 14/40 | 13.855 | 5.957 | 0.20351 |
| All | Fixed | 14/40 | 13.988 | 6.285 | 0.18438 |
| All | Adaptive | 14/40 | 13.997 | 6.265 | 0.18806 |
| Public | Native | 2/24 | 18.964 | 10.248 | 0.33408 |
| Public | Fixed | 2/24 | 18.999 | 10.297 | 0.30209 |
| Public | Adaptive | 2/24 | 19.026 | 10.324 | 0.30798 |
| Synthetic | Native | 12/16 | 6.192 | 2.384 | 0.00767 |
| Synthetic | Fixed | 12/16 | 6.471 | 2.772 | 0.00782 |
| Synthetic | Adaptive | 12/16 | 6.453 | 2.733 | 0.00818 |

The shifted mean uses a one-second shift. Capped diagnostics are available in
the complete JSON table. There were no
new solves or lost solves under either additional policy. Across all forty
pairs, adaptive PAR-2 was more than five percent lower on two pairs and higher
on eleven; fixed PAR-2 had one such win and ten losses. These small, short-budget
timing differences on a shared machine are descriptive, not a significance claim.

The lower mean gap scores do not mean broad gap improvement. Among the 39 pairs
with a valid incumbent and finite dual bound in both runs, adaptive had four gap
improvements and twelve deteriorations exceeding 1e-4 in absolute normalized
gap; fixed had five and twelve. Much of the average improvement comes from
`bayes2_50`, where both seed runs changed from a normalized gap near one to about
0.5202. Both adaptive and fixed policies also had instances with worse final gaps.

The additional work was exercised rather than skipped throughout the study:

| Quantity | Fixed | Adaptive |
|---|---:|---:|
| Runs with directional LPs | 38/40 | 38/40 |
| Directional LPs | 2,172 | 1,719 |
| Total sidecar time (s) | 19.530 | 23.123 |
| Callbacks | 404 | 741 |
| Nonroot callbacks | 300 | 639 |
| Incumbent retriggers | 39 | 43 |
| Accepted bound changes | 112 | 308 |
| Screened directions | 0 | 2 |
| LP attempts without a usable bound | 4 | 26 |

Adaptive OBBT reduced LP count by 20.9%, while sidecar time increased by 18.4%.
Its 574 unproductive-pilot stops spread work over more callbacks, each of which
can reconstruct and check a relaxation. More accepted bounds did not yield more
solves. Reusing exact-feasible LP witnesses eliminated only two directions in
this campaign; these observations do not establish that the screening mechanism
is worth its checking cost. The fixed policy stopped 349 callbacks at an LP limit
and seven at a time limit; adaptive stopped 113 and six respectively.

Both additional policies recorded 48 unsupported callbacks: 24 callbacks on
each seed of `qp3`, whose current box remained unbounded for this sidecar.
Those four runs stayed in the comparison. Initially unbounded `powerflow0009r`
could use the sidecar after SCIP tightened its domains. There were no recorded
sidecar exceptions. The LP-failure counters above denote attempts that did not
produce a usable corrected bound. Individual reason codes were not retained,
so the evidence does not distinguish infeasibility, LP time limits, and numerical
failure within those totals. Such an attempt never supplied a bound reduction.

Every arm had one no-incumbent run: `genpooling_meyer04`, seed zero. All 117
returned incumbents passed the declared original-model numerical check. The
largest absolute residual was 9.973e-7 and the largest scaled residual 7.207e-7.
There were no process/exception failures, inconsistent primal/dual bounds, or
objective-evaluation mismatches. All 69 public incumbents were also checked
against the separate direct OSiL evaluator in the
[independent review](../reviews/solver-review.md).

The ten-second budget is a solver stopping limit, not an exact real-time
deadline. All 78 time-limited calls overshot it slightly; the largest observed
call duration was 10.093 seconds. Including startup, parsing, validation, cleanup,
and output, the largest process duration was 10.606 seconds. Total process costs
were 308.050 seconds native, 313.407 fixed, and 313.618 adaptive. Total call costs
were 288.103, 293.350, and 294.102 seconds respectively. The entire two-worker
campaign elapsed in 471.991 seconds. Capped metrics do not erase these observed
costs from the archive or the uncapped summaries.

The independent audit reproduced all task/source/model hashes and the aggregate
solved counts, PAR-2, and process costs without importing the experiment analyzer.
The recommendation from this complete cohort is to retain native SCIP as the
default and keep the additional policy as a research prototype. Lower directional
LP count, stronger bounds on a few models, and more accepted domain reductions
are insufficient evidence of a net solver benefit. This conclusion is confined
to the stated prototype, selected models, and ten-second horizon; it does not
settle longer-horizon performance, a separately trained policy, or comparison
with published learned selective OBBT.

## Separate pilot

Four tiny synthetic models, using generator seed 17 and sizes excluded from the
holdout, checked API behavior and natural-default callback coverage. The
[pilot archive](pilots/pilot-01/manifest.json) retains its earlier source snapshot,
inputs, full logs, and results. All four returned numerically valid incumbents.
The adaptive propagator executed 50–64 directional LPs per model, accepted 21–38
bound changes, entered 10–16 nonroot callbacks, and recorded one or two incumbent
retriggers. These are implementation diagnostics, not comparative performance
results, and they are excluded from every holdout table. Final arithmetic and
deadline fixes were reviewed before the holdout source was frozen.

## Commands

Run from the repository root with the existing Python environment:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  code/minlp_solver_lab/.venv/bin/python \
  research-20261003-adaptive-obbt/experiments/run.py --campaign campaign-01
```

An existing campaign is deliberately protected. To finish an interrupted one,
use `--resume`; to run a new comparison, choose a new campaign name. A fresh
campaign snapshots the current sources and must be distinguished from the
archived evidence. Recompute the archived campaign's analysis with:

```sh
code/minlp_solver_lab/.venv/bin/python \
  research-20261003-adaptive-obbt/experiments/runs/campaign-01/source/analyze.py \
  campaign-01 --experiment-root research-20261003-adaptive-obbt/experiments
```

The focused checks actually run during preparation were:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  code/minlp_solver_lab/.venv/bin/python -m unittest discover \
  -s research-20261003-adaptive-obbt/experiments -p 'test_*.py' -v
```

Eight checks passed before the campaign: interchange agreement, feasible
synthetic witnesses, all validation boundaries, objective cancellation, failed
run scoring, retention of unsolved pairs, and rejection of missing observed costs.
The later recovery check was run separately with the same discovery command
restricted to `-p 'test_run.py'` and passed one test.
No project-wide checks or CI status/logs were run for this experiment.
