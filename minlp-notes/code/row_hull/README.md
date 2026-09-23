# Row-hull cuts for separable concave terms on a linear row

Code for [results/row-hull-separable-concave.md](../../results/row-hull-separable-concave.md);
experiment record in [notes/row-hull-experiments.md](../../notes/row-hull-experiments.md).

## Layout

- `rowhull/rows.py` — normalization of a row to `sum z = B, 0 <= z <= width` and chord-gap functions.
- `rowhull/pricing.py` — interval subset-sum dynamic program over row vertices (valid lower bounds).
- `rowhull/separate.py` — membership linear program with column generation; cut in model variables.
- `rowhull/closedform.py` — the closed-form inequality in extended form: exact for equal widths
  (equality and inequality rows), valid with residual intervals otherwise.
- `rowhull/strengthen.py` — root cut loop for a `SeparableProblem` (from `../vertex_binarization/sob`),
  export to the solver-neutral IR, root bounds.
- `instances.py` — concave-cost transportation (`transport`), sparse transshipment (`netflow`),
  fixed charge plus concave cost (`transport_fc`).
- `run_one.py`, `sweep.py`, `table.py` — one cell, parallel sweep, tables.
- `lll_closure.py` — root bound of the tilted flow cover family of Lim–Linderoth–Luedtke at `z = 1`
  by exhaustive cover enumeration (comparison only).
- `check_lll_subfamily.py` — equal widths: full family of linearizations against the cover subfamily.
- `proto_transport.py`, `proto_general.py` — the first prototypes (brute-force vertex hulls), kept
  because the experiment record cites their numbers.
- `summarize.py` — consistency check and the family tables of the experiment record.
- `bb.py`, `bb_cf.py` — minimal spatial branch-and-bound for node counts (modes T, R, L, and C).
- `scip_sepa.py`, `sweep_sepa.sh`, `summarize_sepa.py` — PySCIPOpt separator prototype (root-only,
  depth-limited, or on every node box) and its sweep.
- `run_objform.py`, `root_bounds.py` — controls: objective form for Gurobi, solver root bounds.
- `proto_aggregate.py` — row hulls of aggregated node-pair rows (root bounds).
- `facility.py` — concave facility sizing with cuts from the implied aggregate row (negative pilot).
- `minlplib_qp.py` — the nine MINLPLib separable concave quadratic programs.
- `minlplib_scan/` — structural scan of MINLPLib (separate agent).
- `review/`, `review_code/` — scripts of the two independent reviews.
- `results/superseded_pricing_bug/` — runs made before the pricing fix of the code review; not used.
- `test_rowhull.py` — brute-force checks, including the regression test for coinciding subset sums.

## Environment

The solver lab's uv project (Gurobi 13.0.3 through gurobipy, SCIP 10 through PySCIPOpt, BARON
through GAMS 54):

```
cd code/row_hull
uv run --project ../minlp_solver_lab python -m pytest -q test_rowhull.py
```

## Reproduction

```
RUN="uv run --project ../minlp_solver_lab python"
$RUN sweep.py results/main_gurobi.jsonl --sizes 8x12 10x15 --seeds 0 1 2 3 4 \
     --caps uniform random uncap --costs quad log sqrt --solvers gurobi --tl 300 --workers 8
$RUN sweep.py results/main_gurobi.jsonl --sizes g40n3d g60n3d --seeds 0 1 2 3 4 \
     --caps uniform random --costs quad log --solvers gurobi --tl 300 --workers 8
./run_queue.sh            # fixed-charge study (Gurobi) and SCIP/BARON study
python3 summarize.py results/main_gurobi.jsonl          # tables of the experiment record
python3 table.py results/main_gurobi.jsonl              # per-instance listing
./rerun_after_fix.sh      # what was actually run for the final tables after the pricing fix
(for cap in uniform random uncap; do $RUN bb.py 5 7 $cap quad 3; done)
$RUN bb_cf.py 5 7 uniform quad 3
$RUN scip_sepa.py 8 12 0 uniform quad {native|root|tree} --tl 300 [--maxdepth d]
./sweep_sepa.sh && python3 summarize_sepa.py results/scip_sepa_sweep.jsonl
$RUN run_objform.py results/control_objform.jsonl --sizes 8x12 10x15 --caps uniform random uncap --seeds 0 1 2 3 4
$RUN root_bounds.py results/root_bounds_fc.jsonl f8x12 --caps uniform random --costs quad log --seeds 0 1 2 3 4
$RUN proto_aggregate.py 8 12 quad 3
$RUN minlplib_qp.py results/minlplib_qp.jsonl
$RUN lll_closure.py 4 6 uniform,random,uncap quad 2
$RUN check_lll_subfamily.py
```

Forms: `orig` is the model as the repository's other studies pass it to the solvers (epigraph
variables `w_i = f_i(x_i)`, linear objective); `cuts` adds the root row-hull cuts (closed-form
extended rows where the widths are equal, separated cuts otherwise); `cf` adds only the closed-form
extended rows. Reported `total_time` starts after the instance is generated and includes the cut
loop, model construction and the solve; the cut loop is charged against the 300 s limit.
Gurobi uses 4 threads; SCIP and BARON use 1. Relative gap `1e-4`. `--workers 8` with four threads
each assumes about 32 hardware threads. The `cknap` numbers of the experiment record came from an
ad hoc call of `cut_loop` on `sob.instances.concave_knapsack(n, m, 1)`.
