# Convex GDP perspective-cut research

This directory contains the reviewed LB-ESH prototype and a controlled
comparison of radial supporting cuts (ESH) with point tangents (ECP).
Both are established perspective outer-approximation cuts. The research
question is their computational cost and benefit in a GDP implementation.

The study and fresh independent reviews are complete. The
[readiness assessment](../../notes/lbesh-publication-readiness.md) accepts a
focused computational publication, with modest impact and explicit limits.
The [results](../../notes/lbesh-study-results.md),
[study protocol](../../notes/lbesh-study-protocol.md), and
[development log](../../notes/lbesh-development-log.md) record the evidence.

## Environment

Use the committed project lockfile with `uv sync --frozen`. Put licensed GAMS
and Ipopt executables on `PATH`; Gurobi must be licensed in the execution
environment. The recorded run uses Python 3.13.11, Pyomo 6.10.1,
gurobipy 13.0.3, GAMS 54.3.1, SHOT 1.1, and Ipopt 3.14.20.
GAMS/Gurobi and SHOT use Gurobi 13.0.2. GAMS/SCIP is 10.0.3, with
internal Ipopt 3.14.19. Package and native solver versions are
recorded separately under `results/lbesh_development/`.

Set `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, and
`NUMEXPR_NUM_THREADS=1`.
Recheck the installation with:

```sh
uv run --frozen python -m lbesh_research.environment \
  --out results/my_environment.json
```

The optional general-cone reference has a separate environment:

```sh
uv sync --project lbesh_research/conic_reference_env --frozen
uv run --project lbesh_research/conic_reference_env --frozen \
  python -m lbesh_research.conic_reference \
  --name lbesh.exp.small.s104729 --out results/my_conic_root.json
```

That reference solves continuous hulls and enumerated small assignments; it
is not a mixed-integer conic solver. It explicitly refuses the trig family.

## Solver use and numerical contract

```python
from lbesh.solver import LBESH
from lbesh_research.instances import build

model = build("lbesh.exp.small.s104729")
solver = LBESH(model, formulation="hull", esh=True,
               threads=1, time_limit=120, verbose=False)
stats = solver.solve(single_tree=True)
print(stats.status, stats.obj, stats.bound)
```

`stats.obj` and `stats.bound` use the original objective sense. The solver
validates and writes its numerical incumbent to the supplied model; it also
performs model preprocessing, so use a clone if the untouched model is needed.
The benchmark always retains a fresh original model for independent checking.

Supported inputs have flat exclusive disjunctions, valid finite bounds where
needed by the formulation, differentiable convex inequality rows, and a
convex minimization or concave maximization objective. Convexity is an input
assumption, not a solver-certified property. Nonlinear equalities, nested/OR
disjunctions, SOS constraints, and nonfixed GDP indicators appearing inside
disjunct constraint bodies are outside the reviewed scope and are refused.
See the implementation note for the complete input contract.

An `optimal` result means numerical feasibility and a closed numerical gap
under the recorded tolerances. It is not an exact-arithmetic certificate.
Resource stops and invalid evaluations have separate statuses. Preserve the
status, bound, incumbent validation, and tolerances together.

## Reproducing the comparisons

The frozen primary source, including the imported legacy instance sources,
is retained in `results/lbesh_development/source_v1.tar.gz` with a per-file
hash manifest. The primary schedule records all instance/method pairs and
their randomized order. Raw run directories retain witnesses, statuses,
options, bounds, logs, and source fingerprints.

The harness refuses to overwrite existing output paths:

```sh
uv run --frozen python -m lbesh_research.benchmark \
  --instances lbesh.exp.small.s104729 --methods all \
  --time-limit 120 --wall-limit 150 --threads 1 --parallel 1 \
  --order-seed 20260919 --out results/my_comparison.jsonl
uv run --frozen python -m lbesh_research.summarize results/my_comparison.jsonl
```

Use the saved study schedule to reproduce the exact primary method list;
`all` is a convenience subset. Unsupported conic rows must be separated from
supported-method failures when interpreting comparisons.

The exact primary command, in a clean reproduction directory, is:

```sh
uv run --frozen --no-sync python -m lbesh_research.benchmark \
  --instances all \
  --methods lbesh-esh-hull-single,lbesh-esh-hull-multi,lbesh-esh-bigm-single,lbesh-esh-bigm-multi,lbesh-ecp-hull-single,lbesh-ecp-hull-multi,lbesh-ecp-bigm-single,lbesh-ecp-bigm-multi,gdpopt-loa,gams-shot-bigm,gams-shot-hull-convex,gams-gurobi-bigm,gams-scip-bigm \
  --time-limit 120 --wall-limit 150 --threads 1 --parallel 6 \
  --order-seed 20260919 \
  --out results/lbesh_development/main_generated_v1.jsonl
```

`lbesh_study_queue.py` reads `supplementary_plan_v1.json`, waits for all
primary records, checks unchanged executable sources, and then runs the
remaining batches sequentially. It preserves the inherited solver `PATH`.
Initialize the separate cone environment before launching the queue. Its
reference job executes 42 continuous roots (14 small, 14 medium and 14 large
models) plus all 27 assignments for each of the 14 supported small models,
preserving numerical failures without retries.
The complete plan comprises 663 primary jobs, 768 supplementary benchmark
jobs, and 420 cone-reference solves. The oracle diagnostic is a separate
solver-free experiment.

A separate, outcome-triggered sensitivity checks GAMS/Gurobi on all nine
trigonometric instances with `FeasibilityTol=1e-8`. It was declared after
the source freeze when partial primary results exposed original-row
feasibility failures. It preserves the original results and checker. Run it
after the queue releases its solver slots:

```sh
.venv/bin/python lbesh_gurobi_sensitivity.py --parallel 6 \
  --order-seed 20260926 \
  --out results/lbesh_development/gurobi_trig_sensitivity_v1.jsonl
```

The separately declared legacy initialization follow-up covers seven farm
models and the batch model with each of the three GAMS big-M baselines.
Only initial values change: positive farm widths and the unused trailing
batch tank variable. The original 351 legacy results remain intact. After
the preceding batch finishes, run:

```sh
.venv/bin/python lbesh_legacy_initialization.py --parallel 6 \
  --order-seed 20260927 \
  --out results/lbesh_development/legacy_initialization_v1.jsonl
```

The reviewed 24-pair declaration is `legacy_initialization_plan_v2.json`;
version 1 was superseded before execution. Both follow-ups retain the
primary feasibility checker and are analyzed as separate cohorts. Including
these follow-ups, the completed benchmark record count is 1,464.

The completed, independently reviewed analysis command is:

```sh
.venv/bin/python lbesh_study_analysis.py \
  results/lbesh_development/main_generated_v1.jsonl \
  results/lbesh_development/repeat_heldout_v1_r2.jsonl \
  results/lbesh_development/repeat_heldout_v1_r3.jsonl \
  results/lbesh_development/quadratic_conic_v1.jsonl \
  results/lbesh_development/legacy_external_v1.jsonl \
  results/lbesh_development/ablations_pilot_v1.jsonl \
  results/lbesh_development/gurobi_trig_sensitivity_v1.jsonl \
  results/lbesh_development/legacy_initialization_v1.jsonl \
  --primary results/lbesh_development/main_generated_v1.jsonl \
  --references results/lbesh_development/general_conic_roots_frozen_v1.jsonl \
    results/lbesh_development/general_conic_enumeration_frozen_v1.jsonl \
  --require-complete-study \
  --oracle-diagnostic results/lbesh_development/oracle_diagnostic.json \
  --plots --out results/lbesh_development/analysis_v1
```

The analyzer refuses incomplete schedules and existing output directories.
Its warning ledger must be investigated before using solved counts or plots.
Raw solver outcomes, original-model validation, and numerical gap assessments
remain separate. See the [claim register](../../notes/lbesh-claim-evidence.md)
for the limits on mathematical and empirical statements.

Targeted test commands and independent reviews are listed in the development
notes. Do not use project-wide verification to reproduce this topic.

## Completed research bundle

`results/lbesh_development/publication_bundle_v1.tar.gz` contains the topic
sources, pinned environment declarations, development and review notes,
raw runs and logs, and final analysis. Archive paths are relative to the
repository root. The original pre-experiment source archive remains inside
the bundle; its recorded hash is unchanged.

`publication_manifest_v1.json` records every bundled payload file's SHA-256
and size. The manifest itself is included in the archive; it excludes itself
and the archive/checksum files from its payload list.
`publication_bundle_v1.sha256` checks the archive. Earlier pilots, failed
exports, and stage analyses are retained for provenance. Use `analysis_v1`
and the completed study-results note for final numerical claims.
