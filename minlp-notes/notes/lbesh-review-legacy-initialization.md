# Independent review of the legacy initialization followup

Review date: 2026-09-19. A fresh reviewer accepts the separate legacy
initialization wrapper for the declared 24-run supplementary experiment.
No optimization was performed during this review. This acceptance concerns
the execution design and implementation; the resulting data still require
review.

The accepted source is
`code/minlp_solver_lab/lbesh_legacy_initialization.py`, SHA256
`999cb26556acf8ce417b4fe304a8f48d224bb6744eb5c9236915f7a2bb5798db`.
The declaration is
`code/minlp_solver_lab/results/lbesh_development/legacy_initialization_plan_v2.json`.
It covers all seven source-defined farm layout instances and batch processing,
each with SHOT, Gurobi, and SCIP through the frozen GAMS big-M adapter.

This is an outcome-triggered followup declared after the primary source
freeze. Preserve all primary outcomes and present these runs separately.
The followup diagnoses initial-value and interface effects; it does not
retroactively change the primary experiment or define an optimized baseline.

## Independent findings

For each of the eight original models, the reviewer recorded variables,
domains, bounds, fixed status, Booleans, every constraint/objective/named
expression/logical expression, and every disjunction. Initialization changed
only the declared variable values. The model algebra, bounds, and logic
were identical before and after initialization. Separately applying the
original big-M transformation to initialized and untouched clones produced
identical transformed model fingerprints.

Each farm width receives its existing positive affine constraint lower
bound as an initial value. This makes reciprocal evaluation at the starting
point well-defined. It does not tighten the variable's own declared bound
and is not a claim of full primal feasibility.

In batch processing, the trailing storage variable receives its own lower
bound as an initial value. The wrapper establishes that the stage is outside
the tank-selection set and scans all algebraic and logical expressions,
including named expressions and inactive disjuncts. It refuses unexpected
SOS components. Independent adversarial cases introduced a reference in an
inactive constraint, inactive disjunct, inactive objective, named expression,
and logical constraint. Every case was rejected before setting the value.

The solver's solution loader may preserve the initialized value of this
unused variable because the solver writer omits it. That is an explicitly
declared pre-solve choice of a feasible value for an unused variable. There
is no post-solve repair or witness completion. An independent mock erased
the initialized value during the solve; it remained missing in the exported
witness, and the unchanged original-model validator rejected it.

All 24 instance/method combinations were exercised with the solver call
mocked. Each delegated directly to the unchanged frozen `primary._gams`
function with its solver, big-M formulation, 120-second limit, one thread,
original objective sense, and no extra keyword options. The raw native
status/bound behavior is inherited from that exact function. Returned option
and bound fields were preserved, and no initialized point was exported when
the solver reported no incumbent. Numerical witnesses are checked against
the clone made before initialization using the original validator.

The schedule contains exactly the eight-by-three Cartesian product with
separate `-initialized` method labels. Metadata includes all legacy source
files and passes the analyzer's complete frozen-manifest check. The wrapper
also records its own hash and the source manifest hash. The process runner
uses fresh workers, exclusive directories, one BLAS/OpenMP thread per worker,
and a 150-second wall cap. The author timeout test and independent source
inspection confirm process-group cleanup and rejection of partial results
after timeout. The coordinator must keep combined concurrent batches within
six workers; this local runner caps only its own batch.

A subsequent read of existing native SHOT logs identified a metadata-only
limitation: the wrapper's version regular expression expects `SHOT` and
`version` on the same line, whereas these logs print a separate
`Version: 1.1. Git hash: a81275b4.` line. Its `native_versions.shot` field
will therefore be null for that format. The complete retained native log
and recorded study environment preserve the actual version. Keep the
accepted source freeze and recover this field explicitly during the result
audit; this does not change solver settings, outcomes, or acceptance for
execution.

## Checks and remaining boundary

From `code/minlp_solver_lab`:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
uv run --frozen --no-sync python -m unittest \
  lbesh_test_legacy_initialization_independent test_lbesh_legacy_initialization \
  lbesh_test_sensitivity_independent test_lbesh_study_analysis \
  test_lbesh_study_analysis_independent
```

The first 12 targeted tests passed: five independent tests and seven author
tests. After the analyzer extension below, the expanded command passed all
59 targeted tests, including two additional independent extension tests.
The independent test file SHA256 is
`5640fb41fd6f482fe9352352be80904d3404d65a5b18f9e69cf488bdca0b60b0`.
No frozen package, solver configuration, primary result, or validation
tolerance was changed by this reviewer. No project-wide or CI checks ran.

The fresh reviewer also accepted the analyzer extension at SHA256
`3c207d4c570fe77a65b844f7fb5a5649f7a073755e58579bccbd04ed4db011da`.
It routes initialized methods to this declaration and wrapper, while
retaining the distinct all-nine-trigonometric sensitivity gate. Independent
tests accepted all 24 synthetic timeout records and rejected changed
initialization policy, changed invariance policy, mixed method sets, changed
order, the wrong wrapper hash, and missing worker provenance. The declaration
hash recorded in analysis output links back to the frozen plan.

The same analyzer revision removes unnecessary JSON-key sorting when writing
CSV cells. Sorting mixed missing (`None`) and string LP-exit reasons had
raised an exception during export. Independent round-trip checks preserved
both counts, quoted method names, and list values. JSON represents the missing
reason key as the string `"null"`, as it did without sorting in other JSON
outputs; this is an export fix, not a change to numerical classifications.

Before reporting results, require all 24 scheduled records, source/plan/worker provenance,
fresh witness validation, native options and statuses, and unchanged primary
outcomes. Initialization alone does not ensure numerical feasibility or a
closed optimality gap.

## Completed 24-run independent data audit

All 24 declared pairs completed and passed the retained-artifact audit.
The initialization followup produced 23 numerically feasible witnesses and
11 numerically solved records under the unchanged original-model and native
GAMS-bound gates. The corresponding 24 primary records had no fully validated
witness: 21 farm pairs failed before optimization on reciprocal evaluation
at zero, and three batch-processing witnesses omitted the unused trailing
storage variable. These are interface effects, not evidence that the
underlying baseline algorithms cannot solve those models.

All native GAMS DAT statistics match the stored statuses, objective values,
and bounds. Exact solver options match the declaration and the frozen
primary adapter. Fresh original-model validation and independent gap
calculations reproduce every stored assessment. All recorded initialization
changes match an independently rebuilt original model; no model algebra or
declared bound changed.

Native logs confirm GAMS 54.3.1, Gurobi 13.0.2, SCIP 10.0.3, and SHOT 1.1
with git hash `a81275b4`. As anticipated, SHOT version fields in wrapper JSON
are null because of the documented parser limitation; the reviewer checked
the retained native version lines directly.

| Instance | Solver | Feasible | Numerically solved | Wall seconds |
| --- | --- | --- | --- | ---: |
| `batch_processing` | gurobi | yes | no | 34.23 |
| `batch_processing` | scip | yes | yes | 104.96 |
| `batch_processing` | shot | yes | no | 123.10 |
| `FLay02` | gurobi | yes | yes | 1.19 |
| `FLay02` | scip | yes | yes | 1.29 |
| `FLay02` | shot | yes | no | 1.19 |
| `FLay03` | gurobi | yes | yes | 1.44 |
| `FLay03` | scip | yes | yes | 1.54 |
| `FLay03` | shot | yes | no | 4.54 |
| `FLay03_alt_1` | gurobi | yes | yes | 1.34 |
| `FLay03_alt_1` | scip | yes | yes | 11.56 |
| `FLay03_alt_1` | shot | yes | no | 1.85 |
| `FLay03_alt_2` | gurobi | yes | yes | 1.39 |
| `FLay03_alt_2` | scip | yes | yes | 1.49 |
| `FLay03_alt_2` | shot | yes | no | 3.35 |
| `FLay04` | gurobi | yes | no | 3.20 |
| `FLay04` | scip | yes | yes | 3.90 |
| `FLay04` | shot | yes | no | 81.56 |
| `FLay05` | gurobi | no | no | 121.42 |
| `FLay05` | scip | yes | yes | 85.99 |
| `FLay05` | shot | yes | no | 121.27 |
| `FLay06` | gurobi | yes | no | 121.54 |
| `FLay06` | scip | yes | no | 121.73 |
| `FLay06` | shot | yes | no | 121.47 |

The one invalid witness is Gurobi on `FLay05`: active constraint
`no_overlap_disjuncts[34].constraint[1]` has residual `7.9358869e-6` against
tolerance `1.1e-6`. It remains invalid; no tolerance was relaxed.

The solved-count boundary needs careful interpretation. On batch processing,
the native Gurobi log reports objective `679365.3263389`, bound
`679307.9309222`, and gap `0.0084%`, but GAMS exports `OBJEST=NA`. The
declared interface-based gate therefore cannot count this record as solved.
This is missing bound information in that interface record despite a native
closed-gap report, not evidence that the solver failed to close its gap.
The audit retains those native log values as a separate diagnostic and does
not replace the recorded GAMS bound.

Normal native termination also does not imply optimality. For example, SHOT
on `FLay02` explicitly reports a feasible solution to a problem it classifies
as nonconvex, with dual/primal bounds `[7.33333, 37.9473]` and unfulfilled gap
criteria. Its stored loose bound agrees with the log. The followup retains
the default solver classification rather than asserting convexity through a
new option. Gurobi on `FLay04` narrowly misses the shared gap formula even
though its native solve terminates normally. Keep these distinct from primal
validation failures and time limits.

Reproduction command from the lab (use a new output path):

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
uv run --frozen --no-sync python lbesh_review_supplementary_results.py initialization \
  --out results/lbesh_development/independent_legacy_initialization_audit_final.json
```

The final audit artifact retains all 24 paired assessments, native statistics,
diagnostic native log bounds, original residuals, and input/primary/plan/source
hashes. The audit ran no optimization. These outcomes support reporting the
initialization/interface limitation explicitly; they do not support replacing
primary outcomes or selecting the better run per instance.
