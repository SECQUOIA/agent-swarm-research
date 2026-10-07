# Computational evaluation

The new methods produce valid, replayable cuts, but this experiment does not
justify enabling them generally. On the 24 frozen held-out instances, the
baseline and reformulation control each solve 19; `all` and `auto` each solve
18. Twenty instances reach optimization in each mode. Three are refused by
the common source-domain audit, and one uses an unsupported variable exponent.
These four exclusions are limitations of this integration, not failures of
native SCIP.

The [frozen protocol](protocol.md) covers 13 synthetic cases, 24 held-out
MINLPLib cases and four historical diagnostics. It includes native and
reformulation controls, root-only runs, a prespecified repeated seed, and
combined reuse-policy and star-merging ablations. Selection, parameters and
source code were fixed before the new optimization outcomes. All 316 scheduled
runs finished in 443.6 seconds, using one managed worker and one solver/BLAS
thread. No hard process timeout or campaign-budget omission occurred. The
six-second integration budgets are soft; each worker has a hard 20-second cap.

The primary evidence is in [the tables](campaign-v1/results.md),
[machine-readable summaries](campaign-v1/summary.json), and
[all raw records](campaign-v1/records.jsonl). The campaign retains per-run logs,
exact imported models, all 28 application OSiL inputs, frozen case descriptors,
and 101 hashed source/data files. No implementation was retuned after seeing
these results.

Automatic selection reduces held-out candidate LPs from 1,073 to 323, cuts from
230 to 106, and callback time from 5.59 to 3.05 seconds compared with `all`.
It still does not improve the solved count. Recorded integration totals for
baseline/control/all/auto are 17.40/20.66/25.41/23.01 seconds; complete outer
worker totals are 36.66/40.12/45.44/42.49 seconds. The integration totals omit
construction-error records without that timer; outer totals include every
worker. Small timing differences on this shared host are descriptive.

The eight-variable quartic is solved by the new modes while the baseline hits
six seconds, but the reformulation control also solves it. Conversely,
`genpooling_lee2` is solved by baseline and control within the budget while both
cut modes time out. On the historical `waterno2_06` diagnostic, the final dual
bounds are 26.59/21.17/7.05/2.41 for baseline/control/all/auto. The other three
historical cases are refused. These negative results remain in the record.

The [solver-independent star mechanism](star-mechanism.json) proves a gap of
1/128 between two local pair hulls and the merged star. In the solver experiment,
native SCIP already solves this small case quickly, and merging adds overhead.
The exact pair-hull example therefore does not establish a runtime improvement
or dominance over a dense PSD/RLT relaxation.

[Independent certificate replay](campaign-v1/replay.json) passed for all
1,082 recorded cuts, with model binding, all 101 archived hashes, and 12
tampering checks. It took 3.31 seconds separately from the optimization budget.
There are 308 saved model-bound run outputs. Eight construction errors for
`cvxnonsep_pcon40r` have no saved model/cut log and remain explicitly incomplete;
their logs show unsupported expressions `2^(x_i + x_(i+1))` before optimization.
Missing logs are never counted as replayed zero-cut runs. The common source
audits also refuse five other instance names whose declared boxes do not prove
logarithm/division domains, and `chp_partload` because binary64 expression
assembly changes a source row.

All 270 available incumbents pass independent numerical evaluation of original
bounds, integrality, domains, objective and rows at scaled tolerance 1e-5. No
root or final numerical dual conflicts with an analytic optimum or archived
feasible bound under the stated tolerance. These checks and the added-row
certificates do not certify SCIP's complete search or its dual bounds.
[The independent experiment audit](experiment-audit.md) and
[its complete accounting](campaign-v1/experiment-audit-results.json) verify the
corpus, all retained records, denominators and comparisons.

The `no_cache` phase disables sample caching, support-point exchange,
repeated-point skipping and automatic screening together. It cannot isolate
cache speed. The optional C sampler is evaluated by a separate
[kernel microbenchmark](../implementation/native-kernel-benchmark.json);
the full-solver workers do not compile or load that backend.

To reproduce the saved analysis and checker with the frozen sources, run from
the repository root:

```sh
code/minlp_solver_lab/.venv/bin/python research-20261002-convexification/experiments/campaign-v1/snapshot/research-20261002-convexification/experiments/summarize.py research-20261002-convexification/experiments/campaign-v1
code/minlp_solver_lab/.venv/bin/python research-20261002-convexification/experiments/campaign-v1/snapshot/research-20261002-convexification/experiments/replay.py research-20261002-convexification/experiments/campaign-v1 --output /tmp/convexification-replay.json
```

The campaign command actually run was:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 code/minlp_solver_lab/.venv/bin/python research-20261002-convexification/experiments/run_campaign.py --output research-20261002-convexification/experiments/campaign-v1 --wall-cap 1800 --worker-timeout 20
```

The output directory must be new; do not overwrite the archived campaign.
Four targeted tests in `experiments/test_cases.py` passed. The exact star
diagnostic passed, including an altered-objective rejection. No project-wide
checks or CI status/log inspection were performed for these experiments.
