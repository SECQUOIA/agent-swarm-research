# Exact envelopes for composite univariate subexpressions

Code for [the result note](../../results/composite-univariate-envelopes.md).

- `uenv/curvature.py` — certified convex/concave pieces of a sympy expression
  from ball arithmetic (python-flint `arb`) on the second derivative.
- `uenv/envelope.py` — `Univariate`: envelope cuts that are valid for every
  slope (`under`, `over`) and the exact range (`range`).
- `uenv/scip_plugin.py` — SCIP constraint handler for `w == g(x)`: envelope
  cuts, range propagation, completion heuristic. `hybrid=True` leaves
  feasibility and branching to SCIP's native copy of the constraint.
- `uenv/osil.py` — OSiL reader, detection of maximal univariate subexpressions
  with at least two nonlinear operators, presolved variable bounds, and the
  SCIP model in `native`, `split` (auxiliary variables only) or `hybrid` mode.
- `run_quartic.py`, `sweep_separable.py`, `tables_separable.py` — separable
  test families (shared with `../vertex_binarization`).
- `scan_minlplib.py`, `prepass.py`, `run_minlplib.py`, `sweep_minlplib.py`,
  `summarize_minlplib.py`, `analyze_minlplib.py`, `root_bounds.py`, `consistency.py` — MINLPLib study. `consistency.py`
  checks every run against the MINLPLib reference bounds.
- `test_envelope.py` — cuts against a brute-force hull on dense samples.
  `test_plugin.py` — handler modes against native SCIP on small instances.

MINLPLib is not stored in the repository. Download and unpack
`https://www.minlplib.org/minlplib_osil.zip` (here: `~/.cache/minlplib`). The
reference bounds come from `../minlp_solver_lab/instances/instancedata.csv`.

```
cd code/univariate_envelopes
uv run --project ../minlp_solver_lab python -m pytest -q test_envelope.py test_plugin.py
uv run --project ../minlp_solver_lab python scan_minlplib.py ~/.cache/minlplib/minlplib/osil results/scan.json
uv run --project ../minlp_solver_lab python prepass.py candidates.txt results/prepass.jsonl
uv run --project ../minlp_solver_lab python sweep_minlplib.py results/minlplib_v3.jsonl --list sweep_list.txt --modes native split hybrid --tl 120 --workers 12
uv run --project ../minlp_solver_lab python sweep_separable.py results/separable.jsonl \
    --families quartic sigmoid --n 10 20 40 80 --m 1 3 --seeds 1 2 3 --tl 120 --workers 6
python3 consistency.py results/minlplib_v3.jsonl
python3 analyze_minlplib.py results/minlplib_v3.jsonl --table
python3 root_bounds.py results/minlplib_v3.jsonl
```

Versions used on 2026-09-21: PySCIPOpt 6.2.1 with SCIP 10.0, python-flint,
sympy, scipy and numpy from `../minlp_solver_lab/uv.lock`; Gurobi 13.0.3 and
GAMS 54.3.1 with BARON for the baselines.
