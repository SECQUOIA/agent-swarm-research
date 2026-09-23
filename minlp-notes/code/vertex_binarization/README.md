# Vertex binarization of separable nonconvex programs

Code for [the result note](../../results/separable-vertex-binarization.md).

- `sob/functions.py` — univariate functions (sympy). A piece is tagged
  concave only when ball arithmetic (`../univariate_envelopes/uenv/curvature.py`)
  encloses the second derivative in the nonpositive reals.
- `sob/model.py` — `SeparableProblem`, a small solver-neutral representation
  (`IR`), `original_ir`, and `binarized_ir` (the reformulation; `x_i` are
  substituted into the linking rows).
- `sob/backends.py` — Gurobi, SCIP and BARON (through GAMS) backends with a
  common result record. The BARON backend runs GAMS in a temporary directory
  that is always removed.
- `sob/instances.py` — seeded families: `jeroslow`, `jeroslow_w` (asymmetric
  costs; the main lower-bound experiment), `cknap`, `power`, `sigmoid`,
  `quartic`.
- `run_one.py`, `sweep.py`, `summarize.py`, `tables.py` — one cell, a parallel
  grid with resumable JSON-lines output, a text table, and Markdown tables.
- `side_checks/` — the explicit-`x` modelling check and the box-QP check.
- `test_sob.py` — checks that both formulations have the same optimal value on
  small instances and that returned points reproduce the reported objective.

The Python environment is the solver lab's:

```
cd code/vertex_binarization
uv run --project ../minlp_solver_lab python -m pytest -q test_sob.py
uv run --project ../minlp_solver_lab python sweep.py results/jeroslow_w.jsonl \
    --families jeroslow_w --n 12 18 24 30 60 120 400 --m 1 --seeds 0 --tl 120 --workers 3
uv run --project ../minlp_solver_lab python sweep.py results/pilot.jsonl \
    --families cknap power sigmoid --n 25 50 100 --m 1 2 5 --seeds 1 --tl 60 --workers 7
uv run --project ../minlp_solver_lab python sweep.py results/composite_baselines.jsonl \
    --families quartic sigmoid --n 10 20 40 80 --m 1 3 --seeds 1 2 3 --forms orig \
    --solvers gurobi baron --tl 120 --workers 3   # baselines for ../univariate_envelopes
python3 tables.py results/jeroslow_w.jsonl
```

Versions used on 2026-09-21: Gurobi 13.0.3, PySCIPOpt 6.2.1 with SCIP 10.0,
GAMS 54.3.1 with BARON, sympy and numpy from `../minlp_solver_lab/uv.lock`.
