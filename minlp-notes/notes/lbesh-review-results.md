# Independent review of the frozen LB-ESH numerical results

This review is independent of the solver authors and the study-analysis author.
The final numerical package is accepted: all 1,464 benchmark records, 420 cone
reference calls, final analysis tables, derived comparisons, and qualified
results narrative have been checked. No unresolved numerical contradiction
or material reporting issue remains. This acceptance concerns the stated
computational evidence, not editorial acceptance or a claim of a new cut
family. The sections below preserve the staged review history; earlier
pending statements describe the stage at which they were written.

The separate script
[`lbesh_results_independent_audit.py`](../code/minlp_solver_lab/lbesh_results_independent_audit.py)
imports neither the study-analysis program nor the harness summary routines.
It independently implements the declared numerical gap rule, both objective
senses, cross-run bound-versus-feasible-witness contradictions, common-solved
pair selection, one-second shifted geometric means, and full-cohort PAR10.
Failures pay 1500 seconds; accepted run times are capped at 150 seconds.
It checks primary and supplementary schedules against the saved declarations,
including each randomized job order and exact Cartesian identities, and checks
worker source and environment fingerprints against the frozen archive.
Generated family, size, and split labels are derived from instance names.
The script checks all 42 cone roots and 14 complete 27-assignment enumerations,
including source hashes, pinned cone-library versions, status counts, and the
explicitly uncertified status of numerical cone bounds.

`--fresh-validation` also rechecks every saved benchmark witness on a new
original GDP and rechecks fixed-assignment cone witnesses. This deliberately
reuses the separately reviewed `lbesh_research.validation` implementation;
it is independent of the solver's transformed model, but is **not** an
independent second implementation of primal constraint checking. Its arithmetic,
cohort selection, and reporting calculations are independent implementations.
Continuous fractional root witnesses are not tested as integer GDP witnesses.

The final audit must use all six declared benchmark files and both frozen cone
reference files. It must inspect every reported contradiction and validation
disagreement before a numerical solve is accepted. The `--main-only` option is
a limited intermediate check and cannot establish full-study completeness.
With `--compare-analysis`, independently calculated summary and paired fields
are compared directly with the final analysis JSON. Repetitions retain their
own file identities; they are not reduced to fastest runs. Final narrative
claims must also be checked against raw per-family, per-size, and held-out
repeat observations, rather than only aggregate winner counts.

The source scope audit remains necessary for interpreting legacy results:
its 8 extracted compact/smooth cases, 6 requiring an epigraph argument, and
13 broader stress cases must remain distinguishable. These are classifications
of mathematical data assumptions, not automatic certificates of every
convergence condition. The six generated families are related controls with
few seeds. Common-solved timing excludes failures by definition and must be
read beside full-cohort solved counts and PAR10. Solver component timings
must not be added because callback work overlaps master time. Root cone
estimates are diagnostic references, not mixed-integer runtime competitors or
exact certificates. Matched ECP includes the common interior initialization.

Targeted preparation checks:

- `python -m py_compile code/minlp_solver_lab/lbesh_results_independent_audit.py`
  passed.
- A direct independent arithmetic check passed for minimization and
  maximization, contradictory bounds, absent usable bounds, shifted means,
  paired-cohort intersection, and full-denominator PAR10.
- Running the primary-only audit rejected the then-incomplete 295/663 schedule
  before writing an output artifact. This is the expected result.

No solver runs, project-wide checks, or CI inspection were performed. Final
results, analysis comparisons, and a publication-claim verdict remain pending.

## Completed primary audit

The primary audit is accepted. It covers all 663 scheduled records, matching
frozen source hashes and randomized schedule, with fresh original-model
witness checks. No revalidation disagreements or cross-witness bound/status
contradictions were found. All 2,172 independently calculated summary and
paired fields agreed with `analysis_primary_v1/analysis.json`.
The preserved output is `results/lbesh_development/audit_primary_v1.json`.
The command, from `code/minlp_solver_lab`, was:

```sh
.venv/bin/python lbesh_results_independent_audit.py \
  --main-only --fresh-validation \
  --compare-analysis results/lbesh_development/analysis_primary_v1/analysis.json \
  --out results/lbesh_development/audit_primary_v1.json
```

The input SHA-256 was
`42500b65dc585d4652b13bd925ebf7f3f55c8d17a2e6b30caf07d99341af0a0d`.
There were 662 completed workers and one wall timeout. Six original-model
witnesses failed the unchanged validator; all were primary GAMS/Gurobi trig
runs, and none was counted as solved. These ordinary rejected witnesses are
not auditor disagreements. Every matched LB-ESH configuration returned 51
validated feasible witnesses; several retained an open numerical gap.

| Formulation/tree | ESH solved | ECP solved | Common solved | ESH/ECP paired shifted-time ratio |
| --- | ---: | ---: | ---: | ---: |
| Hull/single | 51/51 | 49/51 | 49 | 0.958260 |
| Hull/multiple | 47/51 | 47/51 | 47 | 0.960337 |
| Big-M/single | 50/51 | 48/51 | 48 | 0.962036 |
| Big-M/multiple | 46/51 | 45/51 | 45 | 0.904603 |

These are primary observations. Small aggregate timing differences require
the declared held-out repetitions and family-level interpretation; the table
does not establish a general runtime advantage or full publication readiness.

The independent audit now accepts an optional `--sensitivity FILE.jsonl` for
the separately declared all-nine-trig GAMS/Gurobi run. It checks all nine
identities, the distinct method label, the declared wrapper hash, frozen
copied-adapter hash, unchanged validator tolerance, effective feasibility
option, native GAMS/Gurobi versions, retained option/log evidence, and native
bound field. It retains these records beside the unchanged primary outcomes.
It explicitly requires wrapper provenance for timeouts as well as completed
workers. Solver-free success and rejection checks passed for changed effective
tolerance and omitted timeout provenance.

The cone audit now reports invalid fixed-assignment witnesses and missing
optimal-status witnesses explicitly, including their identities and validation
issues. Such findings return a nonzero audit status for investigation. They
are not silently removed from an optimality-reference claim. The frozen cone
collection and full supplementary study remain pending at this review stage.

## Independent review of primary explanatory cohorts

The descriptive calculations in `analysis_primary_v1/cohorts.json` and the
primary interpretation in [the results note](lbesh-study-results.md) are
accepted within their stated one-repetition scope. A separate derivation read
the raw primary JSONL, independently reassessed numerical gaps, and rebuilt
all 48 oracle cohorts and all eight formulation/tree contrasts. Every declared
cohort was present exactly once. All exact common-solved instance lists,
scheduled denominators, numerical solve counts, shifted wall means, PAR10
means, ratio directions, and LP exit-reason counts agreed. All 4,032 metric
count/mean/median fields agreed across the 12 recorded metrics and both
methods in each contrast. The review did not import or execute the author's
`derive_cohorts.py` to obtain these values.

The independent script and report are preserved as
`results/lbesh_development/audit_primary_cohorts_v1.py` and
`audit_primary_cohorts_v1.json`. The command from the lab was
`.venv/bin/python /tmp/lbesh_audit_cohorts.py`; the preserved script has identical
content and SHA-256
`c280dd71335ebff74ba876591f30f66f9155da0cdbc3ef75f86170fedfb30f35`.
It requires a new output path to preserve an existing audit. The audited
cohort JSON SHA-256 was
`5e7d096282fed76af3c347fa3557326b2f261401d8572f5674a445f96aa4e629`.
The prior complete-primary audit supplies the fresh primal revalidation;
this explanatory audit independently recomputed arithmetic from the unchanged
raw records rather than rerunning that validator.

Direct checks also confirmed:

- The five solved-status differences occur on exactly the four named
  instances; every difference favors ESH in this primary run. Every paired
  ECP result has a valid witness and `time_limit` status. The listed wall
  times round correctly.
- All 25 unaccepted primary LB-ESH outcomes have `time_limit` status. Raw
  `optimal` appears 603 times across all methods, while 550 runs satisfy the
  numerical solve rule.
- The four matched held-out mean cut reductions are approximately 6.60%,
  5.85%, 10.67%, and 18.21%. Mean ESH/ECP cut-time ratios are approximately
  6.63, 6.51, 6.13, and 5.48. Interior-time means range from 0.857 to 0.935
  seconds. These support the rounded descriptions in the note.
- Both held-out ESH hull variants record 33 stalled LP exits and maximum
  final perspective residual `1.20399e-5`. Both ECP hull variants record 30
  stalled and three no-separating-cut exits, with maximum `6.20720e-6`.
  Each big-M variant records 32 stalled exits and one iteration-limit exit.

The note correctly treats component-time measurements as overlapping and
makes no additive timing decomposition. It does not impute diagnostic
function-call counts to the GDP runs. It describes mean work reductions as
an association on matched cohorts, without identifying component-wise causal
effects. It retains near-ties, small reversals, cohort exclusions, dependent
instance structure, and pending repetition evidence. No correction to these
primary explanatory claims was required. Full-study acceptance still awaits
the remaining declared data and claims.

## Complete repeats, quadratic controls, and legacy audit stage

A further independent run accepted all 1,287 records then complete: primary
663, two held-out repeats of 132 each, nine quadratic conic controls, and
351 legacy records. It rechecked schedule identities, source provenance,
and original-model witnesses, found no cross-witness contradictions, and
matched all 4,455 independently calculated summary/pair fields against
`analysis_legacy_v1/analysis.json`. The audit is preserved as
`results/lbesh_development/audit_legacy_stage_v1.json`. The author subsequently
reported an export-only CSV error in that analysis directory and prepared a
new version. This stage accepts the complete JSON calculations actually
checked; it does not accept the incomplete CSV export or the full study.

The stage command, from the lab, was:

```sh
.venv/bin/python lbesh_results_independent_audit.py \
  --batches main_generated_v1 repeat_heldout_v1_r2 repeat_heldout_v1_r3 \
    quadratic_conic_v1 legacy_external_v1 \
  --fresh-validation \
  --compare-analysis results/lbesh_development/analysis_legacy_v1/analysis.json \
  --out results/lbesh_development/audit_legacy_stage_v1.json
```

A separate raw-data derivation also accepted every field in
`analysis_repeats_conic_v1/stability_context.json`: both fixed three-run
oracle cohorts, all 132 repeated method-instance combinations and their
individual runtime ranges, and all 42 method/split quadratic-control groups.
Its independent script and output are `audit_stability_v1.py` and
`audit_stability_v1.json` in the results directory. The command was
`.venv/bin/python results/lbesh_development/audit_stability_v1.py`.
No author's query implementation was imported. All three-run categories
are unchanged. The held-out fixed-cohort ESH/ECP ratios, individual runtime
ranges, 9/9 conic solve count, and conic versus matched quadratic timing
values in the results note agree. The note appropriately limits repetition
evidence to the single-tree configurations and reports the substantially
faster quadratic conic alternative. No correction to these claims was needed.

The full auditor now supports the separately declared 24-run legacy
initialization followup through `--legacy-initialization FILE.jsonl`. Its gate
checks the eight exact models, three distinct method labels, wrapper and
frozen adapter hashes, declaration/worker initialization records, unchanged
options, retained native versions/logs, and numerical-bound provenance.
Without optimization, it independently verified that every declared farm
initial value equals its existing positive affine-row lower bound and that
the declared trailing batch variable is absent from all checked original
algebraic/logical expressions. A solver-free declaration check passed for
all eight models. The frozen wrapper's SHOT version parser can return null
because its banner spans lines; the audit explicitly recovers SHOT 1.1 and
Git hash `a81275b4` from the retained native log. This known metadata limitation
does not replace a solver result or alter a solve decision. Completed
followup records and final reference/ablation claims remain to be reviewed.

## Full original scheduled study and frozen references

The original declared study's data audit passed after all 1,431 benchmark
records and frozen references completed. All six benchmark schedules match
exactly, including the 144 pilot ablations. Fresh original-model validation
agrees with saved feasibility decisions, and no benchmark bound or
infeasibility status contradicts any validated benchmark or fixed-assignment
reference witness. This audit is `audit_planned_study_v1.json`; the command
from the lab was:

```sh
.venv/bin/python lbesh_results_independent_audit.py --fresh-validation \
  --out results/lbesh_development/audit_planned_study_v1.json
```

All 42 supported frozen cone roots are present once. Their retained statuses
are 40 `optimal` and two `optimal_inaccurate`. The latter are
`lbesh.log.medium.s104729` and `lbesh.reciprocal.large.s104729`; their recorded
absolute cone gaps are approximately `1.67e-7` and `1.92e-7`. Neither status
is promoted to an exact certificate. The 14 small enumerations each contain
all 27 distinct mode assignments: 378 solves total, with 204 reported
infeasible and 174 optimal. Every one of the 174 saved optimal assignment
witnesses passes fresh original-GDP validation. There are no invalid fixed
witnesses or missing optimal-status witnesses. Source hashes and the pinned
reference environment match the freeze. This is numerical cross-checking,
not an independent exact infeasibility proof for the other 204 assignments.

This stage validates raw data completeness and numerical consistency. Final
derived ablation, root, and legacy claims remain to be checked against the
complete author analysis, and the separately declared nine-run tolerance and
24-run initialization followups remain separate pending cohorts.

The completed `analysis_planned_v1/analysis.json` subsequently matched all
5,951 independently computed summary and paired-comparison fields from the
accepted full raw-data audit. Input SHA-256 hashes were checked unchanged;
the already completed fresh primal checks were not needlessly rerun.
`audit_planned_analysis_comparison_v1.json` preserves the linkage between the
accepted raw audit and author analysis. This comparison covers all six
original benchmark batches, including ablations. The author analysis SHA-256
was `12df4b32ac1f6584475b9b55ff113bbd1bdbbb1c6544eab92d12054b954bc30e`.

## Final raw-data acceptance and secondary derivations

The final fresh numerical audit passed for all 1,464 benchmark records:
1,431 originally planned records, nine separate trig tolerance runs, and 24
separate legacy initialization runs. All eight schedules, frozen core hashes,
supplementary wrapper declarations, effective options/native version evidence,
and recorded initialization changes pass their respective checks. Every
saved witness was rechecked on an original model. All 174 fixed-assignment
optimal reference witnesses again pass. No bound/status contradiction occurs
across these records and references. The audit is `audit_final_v1.json` and
was produced with:

```sh
.venv/bin/python lbesh_results_independent_audit.py --fresh-validation \
  --sensitivity results/lbesh_development/gurobi_trig_sensitivity_v1.jsonl \
  --legacy-initialization results/lbesh_development/legacy_initialization_v1.jsonl \
  --out results/lbesh_development/audit_final_v1.json
```

A separate independent raw-data query audit accepts the planned secondary
artifacts: `analysis_legacy_v2/legacy_scope.json` and
`analysis_planned_v1/ablations_references.json`. It checked all 65 legacy
scope/method groups, 36 scope-conditioned pairs, eight ablation groups,
both 40-root optimal-status precision summaries, four inaccurate-root/policy
records, and 182 accepted primary comparisons with exhaustive enumerations.
All numerical values and cohorts agree. The largest enumeration discrepancy
is `0.0132119` of the declared tolerance, consistent with the stated 1.32%.
The script/output are `audit_secondary_queries_v1.py` and
`audit_secondary_queries_v1.json`; the command was
`.venv/bin/python results/lbesh_development/audit_secondary_queries_v1.py`.
A first reviewer run used a different local name for the same intersection
stratum; correcting that key to the artifact's established name resolved the
reviewer assertion without any author-data change.

One wording correction was requested: the root table's 39/40 threshold
count concerns the **absolute normalized difference**, at most `1e-4`.
Only 34/40 raw absolute cone-minus-LP differences meet `1e-4` for either
policy. The numerical artifact itself was correct. The final note must keep
this distinction explicit.

The secondary interpretations otherwise preserve the necessary limits: all
six norm-objective cases remain in their expression-defined stress stratum;
initialization followups do not replace primary failures; the integer-NLP
ablation retains interior solves; fast stalls without accepted incumbents
are failures; overlapping component times are not added; and numerical cone
comparisons do not certify hull feasibility or exact optimality. Final author
analysis and followup-sidecar arithmetic remain the last comparison step.

The final `analysis_v1/analysis.json` matches all 6,122 independently computed
summary and pair fields from the fresh 1,464-record audit. Every raw-file hash
was checked unchanged. `audit_final_analysis_comparison_v1.json` links these
artifacts; final analysis SHA-256 is
`7662bd25a0f66672e959a9a1f222014a178eff6b0b355f39ba0726ed98f6d34c`.

Final descriptive sidecars are also accepted. The legacy, ablation/reference,
and stability payloads are exactly unchanged from the independently accepted
stage sidecars apart from their final-analysis input hashes. The new
`followups.json` preserves every original/followup pair: 33 distinct pairs,
660 checked paired fields, and four complete summary groups. Independent
recomputation from raw records agrees on objectives, bounds, usable gaps,
feasibility, solve categories, timing, and validation details. The analyzer's
explicit synthetic `no_witness` issue for missing worker validation was
accounted for; it is not an invented primal residual. The script/output are
`audit_final_queries_v1.py` and `audit_final_queries_v1.json`, run with
`.venv/bin/python results/lbesh_development/audit_final_queries_v1.py`.

The separate native-log reviewer corroborates the followup results. Tightened
trig feasibility gives nine valid witnesses and six accepted numerical solves;
all three large cases remain open. Initialization gives 23 valid witnesses
and 11 accepted solves across 24 records. The invalid Gurobi farm witness
remains rejected. A batch Gurobi log may suggest a closed solver gap while
native GAMS `OBJEST` is unavailable; the declared bound rule conservatively
leaves that run unaccepted. Such a missing exported bound is an interface
evidence limitation, not proof that solver search failed. No followup result
replaces a primary row or selects a best-of outcome.

## Final numerical and reporting verdict

The complete results narrative is accepted with its explicit limits. The
normalized-root threshold wording has been corrected. A final minor scope
clarification changes “all runs” to “all benchmark runs” for the 120-second
limit, since cone references use a separate 300-second solver setting.
The followup tables preserve all original outcomes and explain the missing
native-GAMS-bound case without treating it as a search failure. No remaining
numerical or reporting issue requires further algorithm development or
additional optimization experiments for these stated claims.

The evidence supports a modest and conditional separator comparison within
this implementation: repeated generated single-tree improvements, mixed
external timing and no external accepted-count advantage, greater practical
importance of formulation and incumbent recovery, and a faster exact conic
alternative on supported controls. It does not establish a new perspective
cut family, broad algorithm superiority, robust external speed gains, or
exact numerical certificates. Publication positioning must retain those
limits; the numerical package itself is ready for use in that narrower
computational study.
