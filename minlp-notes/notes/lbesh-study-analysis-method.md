# Reproducible analysis of the frozen LB-ESH study

The analysis program is `code/minlp_solver_lab/lbesh_study_analysis.py`.
It is outside the frozen solver and harness packages. It invokes no solver.
Its output describes numerical evidence; it does not certify exact optimality
or make a statistical significance claim.

Run from `code/minlp_solver_lab` after every supplied schedule is complete:

```bash
.venv/bin/python lbesh_study_analysis.py \
  results/lbesh_development/main_generated_v1.jsonl \
  --primary results/lbesh_development/main_generated_v1.jsonl \
  --out results/lbesh_development/analysis_primary_replay \
  --oracle-diagnostic results/lbesh_development/oracle_diagnostic.json \
  --plots
```

Additional result files are positional arguments, each with an adjacent
`FILE.jsonl.runs/schedule.json`. Additional continuous-cone or exhaustive
assignment reference files follow `--references`; individual JSON objects,
JSON arrays, and JSONL are supported. Preserve each repetition in its own file.
A new output directory is required for each analysis, so earlier analyses
cannot silently be overwritten. `--supplementary-plan` defaults to
`results/lbesh_development/supplementary_plan_v1.json`; the analyzer checks
provided supplementary batches against their declared instance/method lists
and randomized job order. `supplementary_coverage` lists every declared batch,
including wholly absent files. The reference collection is distinct from
benchmark Cartesian schedules: it must contain all 42 supported roots and
14 small enumerations, each with all 27 distinct fixed assignments.
Unresolved reference statuses remain visible and do not imply a failed
completeness check or an optimality certificate. For the final full-study run, add
`--require-complete-study`; this requires `--primary`, all five declared supplementary benchmark files,
and both declared reference files supplied through `--references`. The final study command must list every
planned repetition and supplementary comparison being reported. This note's
single-file example does not assert that the full study is finished.

**Completion and provenance.** The analyzer requires every scheduled
(instance, method) pair exactly once, rejects unscheduled records, and checks
that the job list matches the full Cartesian schedule. `--primary` additionally
requires the entire frozen primary schedule, including its randomized order.
Planned repetition seeds require the declared held-out set and four methods.
All schedules must retain the protocol's time limits, thread count, and
concurrency limit. Each worker's executable-source hashes and environment
lock must match `source_v1_manifest.json`; its package versions, Python, and
platform must match its schedule. A wall timeout or crash can lack worker
metadata because the harness may have killed it before a result was saved;
its enclosing schedule supplies provenance and the run remains a failure.
Current model and validation sources must also match the frozen source before
fresh-model checks run. Legacy input source hashes receive the same checks.
Changes to archived narrative notes or tests do not change executable provenance.

The separately declared `gams-gurobi-bigm-feas1e8` sensitivity may be supplied
as another positional result file. Its nine-case schedule must match
`gurobi_trig_sensitivity_plan_v1.json`, including options, order, and unchanged
validation tolerances. The current standalone wrapper hash must match the
schedule and declaration; its copied-adapter hash must match the frozen
benchmark source. Every sensitivity worker, including crashes and wall
timeouts, must retain both matching hashes. The original harness's allowance
for missing metadata on killed primary workers remains unchanged. The output
records the sensitivity declaration hash and keeps its results separate from
the original primary method.

The separate `gams-{shot,gurobi,scip}-bigm-initialized` followup uses the
reviewed `legacy_initialization_plan_v2.json`: eight named legacy models and
three solvers, with only the declared initial values changed. A distinct
method-specific gate checks its exact policy, method set, source hashes,
schedule order, and unchanged validation tolerances. The same mandatory
wrapper/copied-adapter worker hashes apply, including failures. The two
supplementary wrappers cannot be substituted for one another. Both followup
files must be explicitly listed to include them; their results are never
pooled with or substituted for primary outcomes. The complete eight-file
command appears in `code/minlp_solver_lab/LBESH_RESEARCH.md`.

The final accepted analyzer SHA-256 is
`3c207d4c570fe77a65b844f7fb5a5649f7a073755e58579bccbd04ed4db011da`.
The latest independent review covers both wrapper gates and a CSV regression:
nested JSON cells preserve mixed missing/string LP-reason count keys without
sorting incomparable Python keys. The expanded five-module targeted suite
passed 59 tests. This export fix does not change numerical classifications.

**Witnesses and contradictions.** Every supplied benchmark witness is checked
again on a newly built, original GDP model. This uses the separately reviewed
harness checker, independent of the solver's transformed model; it is not a
second implementation of that checker. The original objective, bounds,
selected disjunct constraints, logical constraints, and integer values are
re-evaluated. Saved feasibility flags are compared with the new result.
Every reported bound is then compared with every validated feasible witness
for that instance, across methods and repetitions. Validated fixed-assignment
cone witnesses are also included when reference files are supplied. A
contradictory bound or infeasibility status disqualifies the run from solved
counts and appears in the warning ledger. Ordinary invalid witnesses remain
visible even when they agree with the harness's original rejection. Reference
cone dual estimates never become certified optimum references.

The numerical solve rule requires a valid primal witness, a reported global
bound marked usable by the harness, completed worker output, and absolute
gap at most `1e-6 + 1e-4 * max(1, abs(objective))`. Revalidation retains the
protocol's row/bound and integrality tolerances. A solver status alone cannot
substitute for these checks. The analyzer returns exit status 2 after writing
the audit if it finds a validation disagreement or contradiction; the warning
ledger must then be investigated before publication.

**Tables and denominators.** `analysis.json` contains full tables, input and
schedule SHA-256 hashes, command arguments, analysis-source hash, and
interpreter/package provenance. Parallel CSV exports are `summary.csv`,
`esh_ecp_pairs.csv`, `metrics.csv`, `records.csv`, `repetitions.csv`, and
`cone_roots.csv`. Groups include the full set, family, size, split, and the
family/size/split cross-classification. Every method's scheduled count,
numerical solves, feasible witnesses, invalid witnesses, raw statuses, and
exclusive outcome categories remain available.

Matched ESH/ECP times use exactly the same common-solved instances within
one formulation, tree mode, group, variant, and repetition. The `variant`
column distinguishes `default`, `nonlp`, and `usercuts`; ablation pairs retain
the same suffix on both methods. External and generated batches remain
separate even when method names coincide. The tables record those
instance names and both solved counts. A one-second shifted geometric mean
is `exp(mean(log(1 + t))) - 1`; the reported ratio divides the two resulting
means. Lower ESH/ECP ratios favor ESH. PAR10 uses the entire scheduled set,
charges each failure 1500 seconds, and caps accepted solved times at the
150-second wall cap, matching the frozen harness summary convention. Both
arithmetic PAR10 means and shifted geometric means are exported. Solved-only
means are labeled conditional; they must not replace paired timing or PAR10
in conclusions. Related function laws, seeds, and size prefixes are not
independent samples.

The matched ECP implementation shares the interior initialization used by
ESH. Its comparison isolates the separator choice within this code; it does
not estimate the performance of an optimized standalone ECP implementation
that omits those interior solves. Repetition rows preserve all individual
times and categories, planned/available counts, and descriptive ranges.
There is no fastest-run selection, pooled independent-sample test, or
confidence interval based on the three related seeds.

Cut, LP, NLP, interior-solve, node, and component-time metrics retain their
available and scheduled denominators. Means and medians include all recorded
values in that group, including failed runs with telemetry; the per-record
CSV permits alternative explicitly labeled cohorts. Single-tree
`time_master` includes callback work. NLP and cut-generation times overlap
with it and must not be added to create a timing decomposition. LP exit
reasons and residuals remain separate; stalled or capped LP phases are not
called hull-feasible. Optional root tables compare LP bounds with conic
primal objectives and dual estimates and retain cone statuses and residuals.
These differences are numerical diagnostics, not proofs of hull equality.

**Figures.** With `--plots`, Matplotlib writes PDF, SVG, and PNG versions of
primary solved counts/PAR10 and family-level paired timing ratios. The exact
plotted aggregates and paired instance lists are in the JSON/CSV tables.
The optional actual-oracle diagnostic figure shows scalar cuts, scalar
function evaluations, and ECP/ESH normalized cut-depth ratios over every
sampled quadratic geometry. `oracle_plot_stats.json` preserves its values;
shaded extrema are sampled ranges, not confidence intervals. These fixed
geometry diagnostics explain row-representation sensitivity and root-search
work. They are not GDP speedup evidence. The diagnostic script, solver, and structure source hashes are all required
and checked before plotting. Both scalar and quadratic inputs must cover
their full declared designs; removing both policies for one quadratic
geometry is rejected. Without `--primary`, figures identify the first input
as the supplied schedule and do not claim it is the frozen primary study.

**Targeted verification performed.**

- `python -m py_compile lbesh_study_analysis.py` passed.
- `.venv/bin/python -m unittest test_lbesh_study_analysis test_lbesh_study_analysis_independent -q`
  passed the combined author and independent tests after review repairs. They cover missing whole
  methods, duplicate records, provenance failures, both objective senses in
  cross-witness bound contradictions, revalidation disagreements, absent
  witnesses, timeout provenance, common-solved/PAR10 denominators,
  supplementary batch/order checks, ablation/legacy isolation, and omitted
  paired geometries in the oracle plot.
- The main-file CLI correctly rejected an incomplete schedule (83 of 663
  records at that check), without producing output.
- An end-to-end temporary complete fixture from one saved run produced the
  JSON/CSV tables and three publication figure formats with no warnings.
- A separate read-only correctness check revalidated 84 then-available main
  witnesses and found no validation disagreements or bound contradictions.
  This was an early correctness check, not a completed-study performance
  result. Final analysis must recheck the complete inputs.

The smoke test used the existing isolated environment: Python 3.13.11,
Pyomo 6.10.1, and Matplotlib 3.11.2. No dependency files or frozen executable
files were changed. No project-wide checks or CI inspection were performed.
A fresh reviewer must audit the final complete data, analysis code, and
claims independently of this author before publication readiness is decided.
