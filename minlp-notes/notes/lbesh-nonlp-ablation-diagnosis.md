# Diagnosis of the single-tree ablation without integer-point NLPs

The completed ablation establishes a substantial limitation of the tested
single-tree policy when reduced NLP recovery is disabled. It does not establish
that NLP solves are mathematically necessary for supporting-plane methods, or
that every failure has the same numerical cause. The retained records contain
no incorrectly claimed optimum or infeasibility among these 72 runs.

## Observed outcomes

The relevant subset of
[`ablations_pilot_v1.jsonl`](../code/minlp_solver_lab/results/lbesh_development/ablations_pilot_v1.jsonl)
contains 72 `*-single-nonlp` records: four ESH/ECP and hull/big-M combinations
on 18 pilot instances. Their outcomes are:

| Recorded status | No accepted incumbent | Accepted, independently validated incumbent | Total |
|---|---:|---:|---:|
| `stalled` | 53 | 9 | 62 |
| `time_limit` | 9 | 0 | 9 |
| `optimal` | 0 | 1 | 1 |

All 72 workers completed without a recorded exception. The ten retained
incumbents pass a fresh solver-free reconstruction and original-GDP validation;
all reevaluated objectives agree with their recorded objectives within
`1e-10`. Only the single `optimal` record passes the numerical solve assessment.
It has zero reported gap and an independently checked maximum primal residual
of approximately `6.82e-7`. None of the 72 records claims infeasibility.
The 62 stalls have median process wall time 2.62 seconds, although individual
stalls range from 1.37 to 107.65 seconds; they are not simply 120-second limits.

Matching instance and method after removing `-nonlp` in
[`main_generated_v1.jsonl`](../code/minlp_solver_lab/results/lbesh_development/main_generated_v1.jsonl)
gives exactly 72 primary records on the same 18 instances: 69 numerical solves
and three time limits. The retained option dictionaries differ only in
`nlp_at_integer`. This comparison supports a strong practical dependence on
reduced NLP recovery in this implementation and test set. It measures the
whole policy change, including its effect on search, rather than isolating
one candidate-rejection mechanism.

The ablation still performs interior NLPs: all 72 records have
`nlp_solves=0`, but `interior_nlps` ranges from 7 to 49. It should be called
“without integer-point NLPs,” not an NLP-free algorithm.

## What the frozen implementation explains

The archived `lbesh/solver.py` in
[`source_v1.tar.gz`](../code/minlp_solver_lab/results/lbesh_development/source_v1.tar.gz),
the current readable copy, and all 72 records share SHA-256
`6046cf5761489f20f4496193da252feda046c741d491d017201584cf6925a36f`.
The relevant paths are
[`_single_tree`](../code/minlp_solver_lab/lbesh/solver.py#L823),
[`_validate_primal`](../code/minlp_solver_lab/lbesh/solver.py#L474), and
[`_esh_cuts`](../code/minlp_solver_lab/lbesh/solver.py#L307).

At each integer callback, the solver generates nonlinear lazy cuts. If no
cuts are generated, it attempts original-GDP incumbent validation. With
`nlp_at_integer=False`, it does not solve a reduced NLP to obtain a different
continuous point for that integer assignment. At master termination it also
attempts to validate the final master solution. Validation checks rounded
integer values, XOR selection, bounds, global rows, selected-disjunct rows,
and the original objective. Reporting `optimal` additionally requires a
closed numerical gap.

For this single-tree path, `stalled` is assigned specifically when the Gurobi
master reports `OPTIMAL` but LB-ESH's accepted-incumbent/gap condition fails.
This is an inference from the frozen status mapping; the raw native Gurobi
status is not stored separately. For the 53 stalls without an incumbent,
LB-ESH never retained an accepted original point. The other nine stalls
explicitly retained feasible points, but not points closing the gap. These
outcomes are not reported as original-GDP optima or infeasibility proofs.

There are several plausible numerical mechanisms. A nonlinear-row residual
and the violation of its affine supporting cut are different quantities;
the code can submit an ESH cut whose violation is only above `1e-7`, while
original primal validation uses `1e-6` residual and integrality tolerances.
Hull separation evaluates disaggregated `nu/lambda`, while primal validation
checks the original point after integer rounding. Big-M rows also involve
indicator values and row scaling. Thus master acceptance and original-GDP
acceptance need not coincide numerically. These source-level observations do
**not** identify the rejected row, residual magnitude, or mechanism in any
particular retained run.

## Representative artifacts

Run directories below are under
`code/minlp_solver_lab/results/lbesh_development/` and contain `final.json`,
`result.json`, `stdout.log`, and `stderr.log`.

| Instance and policy | Ablation artifact directory | Evidence and matched primary result |
|---|---|---|
| `quadratic.small.s104729`, ECP big-M | `ablations_pilot_v1.jsonl.runs/04c48849bffd9fe6/` | `stalled`, no incumbent, bound `1.9062470774`, 53 lazy callbacks. Primary `main_generated_v1.jsonl.runs/f28de27aa3005ea8/` solves at `1.9062495460`. |
| `logsumexp.small.s104729`, ESH big-M | `ablations_pilot_v1.jsonl.runs/99807fbada71705a/` | `stalled`, validated incumbent `0.1424609996`, bound `0.1239068366`, gap `0.0185541630`. Primary `main_generated_v1.jsonl.runs/25a0f408ad3ff018/` solves at `0.1239070329`. |
| `log.small.s104729`, ESH hull | `ablations_pilot_v1.jsonl.runs/bc40bcb2e36fb3cc/` | The lone numerical solve: objective and bound `2.6236796803`. Matched primary `main_generated_v1.jsonl.runs/24352f4be06a326a/` has the same objective. |
| `reciprocal.large.s104729`, ESH big-M | `ablations_pilot_v1.jsonl.runs/74009aa14c75ade1/` | `time_limit`, no incumbent, bound `12.1949356969`, 1,608 lazy callbacks. Primary `main_generated_v1.jsonl.runs/1df096887d085a6a/` solves at `12.2497938225`. |

All 72 retained standard-output files contain license/environment notices
only; all standard-error files are empty. No native master progress log,
rejected final candidate, per-candidate validation explanation, or candidate
residual history was retained. Null witness/validation fields mean no accepted
incumbent was exported; they are not feasibility tests of every point visited.
Cut counts alone cannot recover those missing data. Accordingly, this diagnosis
does not attribute all 62 stalls to lazy-constraint feasibility tolerance,
invalid cut logic, or any other single cause.

The publication can report this completed negative ablation and retain the
NLP-assisted policy as its implemented method. A robust implementation without
integer-point NLP recovery would require separate development and evidence;
it is not an established capability of the current study.

## Checks performed

Only solver-free work was performed: JSON aggregation and exact option pairing,
artifact-directory/log inspection, archive/current/record hash comparison,
frozen callback/validation source inspection, and validation of the ten saved
witnesses on newly built original models using
`lbesh_research.validation.validate_witness`. The latter used
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 uv run --no-sync python -` from
`code/minlp_solver_lab`, with no solver invocation. No frozen source or result
record was changed, and no new optimization run was performed. Fresh independent scientific review passed: the final publication reviewer
independently reconstructed the 53/9/9/1 outcome cells, the matched 69/3
primary outcomes, the single-option differences, and zero reduced-NLP counts;
read the callback, finalization, validator, and cut-generation paths; and
accepted the status inference and limits on causal interpretation. That review
is separate from this diagnosis author's ten-witness validation.
