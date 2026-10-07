# Native-model evaluation

Both scheduled campaigns are complete. **Keep native SCIP as the default.**
The new cuts produced no additional solved instance in either the prospective
comparison or the separate corrected regression cohort.

- [Original results](campaign-v2/results.md): all 282 jobs completed. All 30
  new holdout models were admitted, and baseline/all/auto each solved 25.
  There were 123 recorded cuts and 271 returned-incumbent checks. Four
  diagnostic workers failed during discovery after successful model building;
  their missing cut logs retain unknown counts.
- [Corrected regression results](repair-discovery-v1/results.md): all 75
  matched jobs completed, with 42 recorded cuts, 67 returned-incumbent checks,
  no worker errors and no unknown logs. Sparse polynomial handling and
  discovery deadline checks repair the observed defects. This selected cohort
  remains separate from the prospective table.
- [Measured coverage](campaign-v2/coverage.md) distinguishes absent callbacks,
  unsupported blocks, automatic admission and unsuccessful bounded searches.
  [Changes after the freeze](post-freeze-changes.md) records each source version
  and the reason for the [repair protocol](repair-protocol.md).

Independent replay passed all **165 recorded cuts** across the two cohorts.
All **338 returned-incumbent checks** passed. The four missing original cut
logs remain unknown and are not covered by that certification claim.

The prospective design is in [protocol.md](protocol.md). The new holdout has
30 models: ten convex, ten continuous nonconvex and ten integer nonconvex
models. Selection excludes all cases in the previous convexification campaign
and its earlier exclusions. Previous failures and synthetic examples remain
separate diagnostic populations.

`holdout-selection.json` freezes source hashes, exclusions and ranking.
`select_holdout.py` documents how the selection was obtained; do not rerun it
to replace the frozen selection after results are observed. The independent
preflight audit is in `../reviews/experiment-preflight-audit.json`.

The harness executes all 282 prespecified jobs sequentially. Application runs
have 30 seconds; synthetic examples have ten seconds; root-only runs have five
seconds and one node. Each uses one SCIP and BLAS thread. The common model
builder is identical across baseline, all and auto modes. The method adds
linear cuts to the original model without auxiliary feature equalities.

The worker independently checks every original constraint, domain, variable
bound, integrality condition and objective of a returned incumbent. These are
numerical residual checks at scaled tolerance 1e-5. Added-cut certificates have
a separate replay; they do not certify SCIP's complete solve or numerical
dual bounds.

The following commands were run from the repository root in the documented
Python environment. Existing campaign directories are protected against
overwriting. A new run needs a new output directory and uses the live source;
the exact measured implementations remain in each saved snapshot.

```bash
code/minlp_solver_lab/.venv/bin/python research-20261003-convexification/experiments/run_campaign.py --output research-20261003-convexification/experiments/campaign-v2
code/minlp_solver_lab/.venv/bin/python research-20261003-convexification/experiments/summarize.py research-20261003-convexification/experiments/campaign-v2
```

The destination must not exist. Every campaign copies the implementation,
model sources and original OSiL files before starting. It preserves worker
logs, exact parsed models, statuses, timings, cut certificates, incumbent
values and all errors. Missing cut logs mean unknown counts. A repair must
preserve the original campaign and explain any repeat.

Targeted harness verification:

```bash
code/minlp_solver_lab/.venv/bin/python -m pytest -q research-20261003-convexification/experiments/test_cases.py research-20261003-convexification/experiments/test_protocol.py research-20261003-convexification/experiments/test_summary.py
```

This command passed ten tests. Independent metrics, original-model checks and
source hashes passed for both cohorts. The independent replay outputs are
`campaign-v2/replay.json` and `repair-discovery-v1/replay.json`; they govern
the added-cut certification claims. The exact final offline checker is
archived at `../reviews/replay-final.py`, with both replay result hashes in
`../reviews/replay-final-provenance.json`. No project-wide tests or CI checks
were run for this work.

The corrected cohort was generated and run with these targeted commands:

```bash
code/minlp_solver_lab/.venv/bin/python research-20261003-convexification/experiments/freeze_repair_plan.py research-20261003-convexification/experiments/campaign-v2 research-20261003-convexification/experiments/repair-plan.json
code/minlp_solver_lab/.venv/bin/python research-20261003-convexification/experiments/run_repair.py --original research-20261003-convexification/experiments/campaign-v2 --plan research-20261003-convexification/experiments/repair-plan.json --output research-20261003-convexification/experiments/repair-discovery-v1
code/minlp_solver_lab/.venv/bin/python research-20261003-convexification/experiments/analyze_repair.py research-20261003-convexification/experiments/repair-discovery-v1
```

The two campaigns together took 2,093.12 seconds of measured campaign wall
time, excluding preparation, review and independent audit. The machine ran
unrelated jobs throughout, so small runtime differences are descriptive.
