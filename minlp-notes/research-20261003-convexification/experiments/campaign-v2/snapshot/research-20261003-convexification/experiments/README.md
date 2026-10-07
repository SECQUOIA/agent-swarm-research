# Native-model evaluation

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

Run the campaign from the repository root in the documented Python environment:

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

This command currently passes ten tests. Campaign results and independent
replay are pending the integration preflight; the selection and protocol are
already frozen.
