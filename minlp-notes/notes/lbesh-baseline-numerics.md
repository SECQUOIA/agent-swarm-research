# GAMS/Gurobi nonlinear feasibility sensitivity

Read-only investigation, 2026-09-19. The primary data and frozen implementation
were not changed, and this investigation ran no optimizations.

The two inspected GAMS/Gurobi big-M solutions fail the common original-model
checker because their active nonlinear cost rows have residuals above
`1.1e-6`. The native Gurobi logs themselves warn about excessive nonlinear
constraint residuals. These are numerical feasibility failures, not evidence
of an incorrect GDP model or a static piecewise-linear approximation.

## Direct evidence

Artifacts are under
`code/minlp_solver_lab/results/lbesh_development/main_generated_v1.jsonl.runs/`.

| Instance | Artifact directory | Maximum original-row residual | Native maximum general-constraint violation | Native termination |
| --- | --- | ---: | ---: | --- |
| `lbesh.trig.large.s104729` | `14c5e5a30ac65ca7` | `6.0404468e-6` | `7.1019e-6` | `MODELSTAT=8`, `SOLVESTAT=3`, time limit |
| `lbesh.trig.medium.s155921` | `3a9d0b31eb80b503` | `7.3249773e-6` | `7.5985e-6` | `MODELSTAT=8`, `SOLVESTAT=1`, gap reached |

The large case has a reported objective of `10.008449659289742`, bound
`10.006343757309377`, and relative gap approximately `0.0210%`. It also fails
the declared `0.01%` gap target; it must not be described as a closed-gap run.
The medium case has objective `5.609221705409263`, bound
`5.608660878837181`, and meets the gap target but fails primal validation.
GAMS model status 8 alone does not resolve either issue.

Both `gams.log` files identify GAMS 54.3.1 and its Gurobi 13.0.2 library.
They report 32 and 16 **general nonlinear constraints**, respectively, then
96 and 48 added variables to disaggregate expressions. Both report a global
nonconvex MINLP search. The generated `gams/model.gms` files retain the cosine
expressions. No static PWL mode is requested. The nondefault solver parameters
are only time limit, absolute MIP gap, logging, and one thread. In particular,
no tighter primal feasibility tolerance was supplied.

All returned indicator values in these two witnesses are exactly 0 or 1, so
an almost-integer indicator multiplied by big-M is not the explanation for
these active-row violations. The original cost expressions have no big-M
term. Raw GAMS values are exported with 15 digits after the decimal point;
ordinary output rounding at that precision cannot explain residuals of this
magnitude in these moderately scaled expressions.

## Explanation and uncertainty

GAMS documents a default Gurobi primal feasibility tolerance of `1e-6`, a
default nonlinear interface, and dynamic nonlinear treatment by default.
Tightening `feasibilitytol` can reduce violations but can increase iteration
counts. [GAMS/Gurobi manual](https://gams.com/latest/docs/S_GUROBI.html).

Gurobi documents that it disaggregates nonlinear expressions into auxiliary
relations. Small auxiliary residuals can accumulate or be amplified when the
original expression is evaluated. It checks original nonlinear errors but
can still return a solution exceeding the tolerance.
[Gurobi nonlinear constraints manual](https://docs.gurobi.com/projects/optimizer/en/current/features/nonlinear.html#dealing-with-nonlinear-expressions-via-function-constraints).

This mechanism is consistent with the logs and with the size of the observed
errors. Each active cost row contains three weighted cosine terms divided by
`1-cos(0.75)`. The sums of their positive coefficient magnitudes are
`5.8805–10.8769` in the large witness and `6.1580–12.6182` in the medium
witness. Errors near `1e-6` in the cosine auxiliaries could therefore produce
original-row errors of the observed size. This is an explanation supported
by the formulation and documented solver behavior, **not a recovered trace
of the exact auxiliary errors**: those auxiliary values were not retained.
The different native and original maximum residuals are expected to refer
to different equation sets; their exact difference has not been traced.

## Supplementary sensitivity declared during the main study

The fixed checker and explicit default settings suffice for the primary
matched ESH/ECP comparison. They do not establish that Gurobi is intrinsically
less accurate. Further partial primary results subsequently showed invalid
witnesses for all three medium trigonometric seeds and large seed 104729.
The coordinator therefore requested a uniform numerical sensitivity for a
stronger baseline fairness check.

This sensitivity was designed **after source freeze, in response to partial
primary results**. It is not externally preregistered or part of the original
primary comparison. Its actual runs are deferred until the queued study
releases solver capacity. Every primary outcome remains unchanged.

The saved plan is
`code/minlp_solver_lab/results/lbesh_development/gurobi_trig_sensitivity_plan_v1.json`.
It includes all nine predeclared trigonometric instances, one setting
`feasibilitytol=1e-8`, the same 120-second solver cap, 150-second wall cap,
one solver thread, and the unchanged original-model checker. All other
settings retain their primary values, including default integer tolerance.
No `NumericFocus`, presolve, or approximation parameter was selected using
outcomes. The plan records wrapper and frozen-source hashes, creation time,
and launch-order seed `20260926`; the root allocates one through six available
workers without exceeding the overall study cap.

The separate adapter is
`code/minlp_solver_lab/lbesh_gurobi_sensitivity.py`. It reuses the frozen
instance builder, metadata, witness capture, validator, result assessment,
atomic JSON writer, and ordered-job helper. Its narrow GAMS adapter copies
the frozen big-M path and native status/load/bound gates. Its only solver
change writes `gams/gurobi.opt` with `feasibilitytol 1e-8` and enables
`GAMS_MODEL.optfile=1;`. The Gurobi log must confirm `FeasibilityTol=1e-8`
or the run is recorded as an error. Native GAMS/Gurobi versions, exact option
file hash, effective tolerance, and native log are retained. The process-cap
code copies the frozen fresh-process pattern because its original worker
module is hardcoded; this wrapper uses its own worker target.

The distinct method label is `gams-gurobi-bigm-feas1e8`. Every run writes to a
fresh artifact directory and a separate JSONL file with its own complete
`schedule.json`. Outputs cannot overwrite existing results. Each worker and
schedule record the external wrapper hash; frozen benchmark source mismatch
is rejected. The review snapshot wrapper SHA256 is
`547376f941569cffaabaa4683200ffc04892832f5a4dd8a31ec27d407efd477d`.

Five targeted solver-free tests passed using:

```sh
cd code/minlp_solver_lab
uv run --frozen --no-sync python -m unittest test_lbesh_gurobi_sensitivity
```

They exercise complete family coverage and fixed caps, native status/load
and bound handling, exact GAMS options, rejection of an invalid original
witness despite a closed reported gap, suppression of initialized witnesses
when no incumbent exists, and process-group timeout handling. An initial
file-creation command used the wrong working-directory-relative path; its
import check failed without executing tests. Correcting that command gave
the five passing tests above. No solver run was started by this author.
Fresh independent review is required before the root launches, for example:

```sh
cd code/minlp_solver_lab
PATH=/workspace/local-home/miniconda3/envs/solvers/bin:$PATH uv run --frozen --no-sync \
  python lbesh_gurobi_sensitivity.py --parallel 1 --order-seed 20260926 \
  --out results/lbesh_development/gurobi_trig_sensitivity_v1.jsonl
```

Report primary and sensitivity results separately for all nine cases,
including original successes. Do not replace primary failures, select the
better run per instance, or relax the checker. Tighter tolerance is not
guaranteed to restore feasibility or close the gap. Conclusions apply only
to this family and setting.

Checks performed: parsed the two raw results and GAMS logs/model files;
verified exact returned indicator values; read the official manuals; and
evaluated cosine coefficient sums from fresh instance data using the frozen
project environment. A partial snapshot contained 320 completed main rows,
including 22 GAMS/Gurobi rows and these two invalid witnesses; that snapshot
is not a final failure count or performance result.

## Farm-layout initialization followup

A separate issue arose in the partial legacy run. The farm builder leaves
`plot_width[i]` uninitialized, with zero as its raw variable lower bound.
Its active affine `width_bounds[i]` rows impose positive widths: 1 for the
ordinary cases, 3 for `FLay04`, and `[5, 5, 7]` for `FLay03_alt_1`. The
reciprocal area rows are smooth on those feasible domains. This is not a
nonsmooth model or an unsupported mathematical operation.

The observed tracebacks stop in Pyomo 6.10.1's GAMS
`check_expr_evaluation`, before native solver execution. That check temporarily
sets every uninitialized variable to zero, then evaluates the area expression
`plot_area[i] / plot_width[i] - plot_length[i]`. Division by zero is therefore
an avoidable interface initialization defect. Original runs remain in the
primary legacy data as interface failures and must not support claims of
solver inferiority.

The coordinator authorized a followup on **all seven farm instances × all
three GAMS big-M baselines**: SHOT, Gurobi, and SCIP. It was designed after
source freeze in response to partial legacy results. It is not a
preregistered primary comparison. The complete 21-pair declaration is
`code/minlp_solver_lab/results/lbesh_development/legacy_initialization_plan_v1.json`.
It fixes launch-order seed `20260927`, 120 seconds solver time, 150 seconds
wall time, and one solver thread. The root allocates one through six
available workers after the existing queue; no optimization was launched
by this implementation author.

The external wrapper `code/minlp_solver_lab/lbesh_legacy_initialization.py`
only sets each initial `plot_width[i]` to the positive lower bound of its
existing affine `width_bounds[i]` row, then calls the unchanged frozen
`benchmark._gams` adapter. This changes no variable bounds, constraint
expressions, disjunctions, big-M coefficients, or solver options. The GAMS
writer's existing `warmstart=True` default emits these width levels. The
initialization is domain-valid, not claimed to be a feasible incumbent.
The original-model clone is taken before initialization; returned witnesses
use the unchanged independent original-model checker.

Each method has its own label, `gams-{shot,gurobi,scip}-bigm-widthinit`, and
results are separate from both original legacy data and the trigonometric
Gurobi tolerance sensitivity. In particular, Gurobi retains its primary
**default feasibility tolerance** in this followup. SHOT retains every
frozen primary option, including its explicit primal tolerances and one
MIP thread; no declared-convexity option is added. The declaration records
the exact expected primary options for all three methods, and each actual
result inherits its native option record from `_gams`.

The wrapper uses `primary._metadata(legacy=True)` to record all 325 frozen
source/data fingerprints, and refuses source or dependency-lock mismatches
against the source manifest. Schedule and worker records include the wrapper
hash, primary adapter hash, and initialization provenance (old/new values,
source row, original bounds). Native logs and version information are
retained. New output directories and the inherited fresh-process/group-kill
pattern protect the existing data and enforce wall caps. The review snapshot
wrapper SHA256 is
`569518a458a681ada41cf01b2db9034c4e5f93ec4526568bda1ff0ad2e76adee`.

Six solver-free tests passed with:

```sh
cd code/minlp_solver_lab
uv run --frozen --no-sync python -m unittest test_lbesh_legacy_initialization
```

For all seven cases, the tests compare original and initialized algebra and
bounds before and after big-M transformation, evaluate every transformed
expression, and check that GAMS emits width starting levels. Other tests
check unchanged adapter calls/options for all three methods, suppression of
initial values when no incumbent exists, rejection of an invalid returned
witness, full 21-pair coverage and source fingerprints, refusal of an
unproved positive-width initialization, and process-group timeout handling.
Before implementation, fresh original-model validation also agreed with
12 available legacy farm witness records. These checks establish interface
and model-preservation contracts; actual solver success remains untested
until independent review and allocated-slot execution.

### Scope extension before execution: unused batch variable

The unexecuted 21-pair farm plan above is superseded by a draft 24-pair plan,
`legacy_initialization_plan_v2.json`, before any followup solver run. The
coordinator requested this extension while the primary legacy batch was
still running. Freeze and independent review will wait for its completion.

In `gdplib.batch_processing`, the source declares `storageTankSize_log` on
all ten stages, but the objective and tank-selection disjuncts use
`STAGESExceptLast`. Thus `storageTankSize_log[10]` is absent from every
expression and from the GAMS writer's symbol map. Its declared finite bounds
are `[4.605170185988092, 9.615805480084347]`, and its initial value is `None`.
The strict complete-witness checker rejected two inspected GAMS incumbents
solely because this unused variable was missing. This is an interface
completion issue; it does not affect the objective or original feasibility
of any referenced variable.

The revised plan covers **all eight models × all three GAMS baselines**,
using labels `gams-{shot,gurobi,scip}-bigm-initialized`. Farm initialization
remains exactly as described above. For batch processing, the wrapper sets
only the unused trailing tank variable to its own lower bound **before**
calling the unchanged adapter. There is no post-solve filling, no bound
change, and no relaxation of the complete-witness checker. A runtime guard
checks all constraints, objectives, named expressions, and logical
constraints, including inactive components and every disjunct, for any
reference to that variable; unexpected SOS components are refused. The
source fingerprint guard further restricts this to the reviewed model.

The read-only audit scanned all 601 constraint rows and the objective;
there were no named expressions, logical constraints, or SOS constraints.
An in-memory completion of only this variable made the two inspected
SCIP/SHOT witnesses pass the unchanged fresh original-model checker, with
unchanged objective values. Those hypothetical completions were not written
to the primary results. A solver-free Pyomo solution-loader check confirms
that a preinitialized omitted variable retains its value (marked stale);
this is appropriate only because its complete unusedness has been checked.
An initial synthetic loader check omitted Pyomo's required `_cuid` fixture
attribute and failed; the corrected regression test exercises the real
loader successfully.

Seven targeted tests now pass, including the previous farm contracts and
batch algebra/bound invariance before and after big-M transformation,
omitted-value retention, and refusal if a new row references the purportedly
unused variable. The draft wrapper hash is
`999cb26556acf8ce417b4fe304a8f48d224bb6744eb5c9236915f7a2bb5798db`.
The final review snapshot and declaration will be recorded after the main
legacy batch completes. All original farm and batch outcomes remain visible.

### Final initialization followup freeze

The full primary legacy run completed all 351 pairs. Its 81 GAMS outcomes
contain 55 valid original-model witnesses, 21 farm pre-solver division-by-zero
errors, three batch witnesses missing the unused variable, and two native
SHOT outcomes without incumbents. Those two native outcomes are an `l2`
layout time limit and an `l1` layout normal termination reporting no solution;
they are not evidence of another writer initialization defect. No further
scope expansion is warranted.

Fresh independent review accepted the unchanged wrapper hash
`999cb26556acf8ce417b4fe304a8f48d224bb6744eb5c9236915f7a2bb5798db`.
Seven author tests and five independent tests passed, with no optimizations.
The independent checks cover full algebra, Boolean/disjunction structure,
domains, bounds, transformed big-M equations for all eight models, exact
frozen-adapter calls for all 24 pairs, hidden variable references, and
refusal to fill an omitted value after a solve.

The 24-pair `legacy_initialization_plan_v2.json` is now frozen. It preserves
its original partial-results declaration time, adds a freeze time after
legacy completion, records all exact native options and source hashes, and
links the independent review. Its SHA256 is
`d350996b6ddf4d5ef0197115e73bd9cfbf694546b9bcd920c2bd76dda138225c`.
The earlier 21-pair declaration remains as an unexecuted design record.
Execution still awaits the root's solver-slot allocation:

```sh
cd code/minlp_solver_lab
PATH=/workspace/local-home/miniconda3/envs/solvers/bin:$PATH uv run --frozen --no-sync \
  python lbesh_legacy_initialization.py --parallel 1 --order-seed 20260927 \
  --out results/lbesh_development/legacy_initialization_v1.jsonl
```

The final comparison must retain all original 24 outcomes alongside these
separate followup rows. Initialization repair is not a new solver algorithm
and does not change the matched primary ESH/ECP comparison.
