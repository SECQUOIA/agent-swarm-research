# Independent experiment audit

The frozen corpus and completed campaign accounting pass the independent
audit. The experiment does not show a general solver performance improvement.
This review covers corpus construction, known
synthetic optima, original-model residual checks, failure retention, source
provenance, and metric interpretation. The separate `replay.py` review covers
cut validity and binding; this audit does not replace it.

The review made no optimization runs and did not choose instances or parameters
using optimization outcomes.

## Completed campaign

The [audit output](campaign-v1/experiment-audit-results.json) independently
checks all 316 scheduled records, their per-run files, all 101 snapshot hashes,
the frozen input descriptors and OSiL hashes, and every reported suite count and
dual-bound comparison. All records are retained. No synthetic case reports
infeasibility or unboundedness in conflict with its known feasible witness and
finite optimum. The 40 cases that produced model fingerprints have one
consistent fingerprint across modes and phases; the remaining case failed
during construction before returning a model record.

The campaign took 443.57 seconds. Its statuses are 162 `optimal`, 42 `gaplimit`,
12 `timelimit`, 56 `nodelimit`, 36 `source_model_mismatch`, and eight
`worker_error`. There are no hard process timeouts or omitted scheduled jobs.
The 270 returned incumbents all pass the original-model residual check, and no
returned root or final dual bound conflicts with its available reference under
the stated tolerance. Two full runs exceed the soft budget by more than 0.01
seconds: baseline `kall_circles_c6b` at 6.0153 seconds and automatic
`waterno2_06` at 6.0164 seconds.

Every held-out mode retains its denominator of 24. Twenty cases reached the
solver, three were refused by the source-domain audit (`syn15m`,
`cvxnonsep_psig30r`, and `syn10hfsg`), and one failed source construction
(`cvxnonsep_pcon40r`, with an unsupported variable-exponent expression). The
historical cases `btest14` and `ghg_2veh` were also refused for unproved source
domains, and `chp_partload` was refused because binary64 expression assembly
changed a row. These are common importer limitations, including in the baseline
mode; they do not establish that native SCIP cannot solve those instances.

The held-out numerical solved counts are 19/24 for baseline, 19/24 for control,
18/24 for all blocks, and 18/24 for automatic selection. Final dual-bound
comparisons against baseline are one better, 14 ties, five worse, and four
unavailable for all blocks; automatic selection has three better, 12 ties, five
worse, and four unavailable. Against the reformulation control, both methods
have three better, 16 ties, one worse, and four unavailable. All negative and
unavailable outcomes remain in the summaries. The synthetic solved counts are
12/13 for baseline and 13/13 for each reformulated mode, so that difference
cannot be assigned specifically to the new cuts.

There are 1,082 recorded added cuts across all phases. Four all/automatic
records lack cut logs because their workers raised construction errors. These
cut counts remain unknown in the accounting. The eight error records also lack
integration-time detail; aggregate integration times sum only recorded values,
whereas outer wall totals retain the cost of those failed workers. The separate
cut replay determines whether the saved cuts pass certificate and model-binding
checks.

## Corpus and reference checks

`audit_campaign_metrics.py` reconstructs all 123 prior-campaign exclusions and
the selection from the cached OSiL corpus and archived MINLPLib metadata. It
recovers all 279 eligible names in the
same order and the same first 24 selected names. Every archived eligible-model
SHA256 matches, and each selected primal/dual reference matches
`instancedata.csv`. The selected set contains 11 instances with integer
variables and seven marked convex in that metadata.

The metadata predicate is specifically
`int(nquadcons) + int(ngennlcons) > 0`. It excludes models with only higher-degree
polynomial or signomial constraints, even when their expression trees use
supported operators. Thus the held-out population does not represent every
supported nonlinear model. Its names were held out from the two named earlier
campaigns, not from the entire repository or from public solver development.
Expression-tree parser support also does not guarantee that the native model
builder supports every parsed expression, as the retained variable-exponent
construction error demonstrates.

All 13 synthetic known optima were checked independently. For the quadratic
star, minimizing the concave leaf coordinates at their endpoints and then
minimizing the central quadratic gives the four minima `1/32`, `9/128`, `9/32`,
and `1/128`; the last is the stated optimum. The 13 saved witnesses pass the
numerical original-model checker. The 24 held-out models use only the covered
expression operators and `B`, `C`, or `I` variable types.

## Findings addressed before optimization

The harness owner corrected these issues before the campaign source freeze:

- A killed worker could leave partial JSON that aborted the entire runner.
  Workers and the parent now replace result files atomically; malformed existing
  output is preserved separately and represented by an explicit error record.
- Missing cut logs appeared as zero cuts in per-instance comparisons. They now
  appear as unknown; aggregate totals describe recorded cuts.
- The source snapshot omitted the summary implementation and depended on
  external cached OSiL files. It now includes `summarize.py`, archived metadata,
  and all 28 application OSiL inputs, with hashes. Holdout input hashes must
  match the selection freeze.
- Solved counts could accept an unverified incumbent or a worker that failed
  after writing output. They now require a finite primal objective, a passed
  incumbent check, and successful process completion.
- The reference audit checked the final dual bound but omitted the saved root
  bound. Both now have explicit reference checks.

An additional numeric robustness finding concerns an overflowed objective in
`cases.check_primal`. With finite coefficient `1e308` and coordinate `2`, the
original checker accepted an infinite objective if no reported objective was
supplied; with a finite reported objective it produced a NaN discrepancy.
`primal-audit-checks.json` preserves this initial finding and the source hash.
No frozen-corpus failure was observed. The harness owner added explicit
nonfinite-objective rejection before the campaign freeze, and its new targeted
regression passes.

Nine adversarial records verify the solved-count guards. Separate checks verify
that a timeout with no cut log has an unknown cut count, maximization comparisons
use the correct direction, and a worse minimization bound remains a negative
outcome.

## Interpretation limits

The protocol separates the original baseline from an auxiliary-reformulation
control, so a change caused by reformulation is not automatically attributed to
new cuts. All four modes retain the same native expression constraints and use
the same time, thread, gap, and seed settings. Mode order rotates by instance.

Six-second runs on a shared host are descriptive. The soft budget includes
model parsing and integration; nonpreemptive work may exceed it, and the
20-second process cap may terminate a worker without a cut log. Ratios computed
only on cases solved by both methods are a selected subset and do not establish
population speedups. The native C kernel has a separate microbenchmark; the
full-solver workers do not load it.

Known-optimum and archived-feasible-bound comparisons can detect inconsistent
numerical solver bounds. Passing them does not certify SCIP's complete search
or its dual bounds. Likewise, scaled floating-point residual checks are not
exact feasible-point certificates.

The completed-run audit explicitly rejects an infeasible or unbounded status
for a synthetic case with a known finite optimum and feasible witness. It also
keeps the full frozen denominator and separately reports source-model refusals,
confirmed model admissions, and unknown admissions after incomplete workers.
A `source_model_mismatch` is a refusal by the common source-model audit before
optimization; it is not evidence that native SCIP itself failed on that input.

## Targeted commands

Run from the repository root:

```sh
code/minlp_solver_lab/.venv/bin/python research-20261002-convexification/experiments/audit_campaign_metrics.py --output research-20261002-convexification/experiments/experiment-audit-preflight.json
code/minlp_solver_lab/.venv/bin/python -m pytest -q research-20261002-convexification/experiments/test_cases.py
code/minlp_solver_lab/.venv/bin/python -m pytest -q research-20261002-convexification/experiments/test_cases.py::test_nonfinite_objective_is_not_accepted_as_a_feasible_primal_result
code/minlp_solver_lab/.venv/bin/python research-20261002-convexification/experiments/audit_campaign_metrics.py --campaign research-20261002-convexification/experiments/campaign-v1 --output research-20261002-convexification/experiments/campaign-v1/experiment-audit-results.json
```

The first command passed. The second passed all three tests during the
independent primal review, before the overflow fix. The third passed the added
overflow regression after that fix. The fourth passed the completed campaign
audit. No project-wide checks or CI status/log inspection were performed.
