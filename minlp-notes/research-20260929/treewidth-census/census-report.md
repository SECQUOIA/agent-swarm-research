# Treewidth census of MINLPLib

Date: 2026-09-29. Status: computational census by the root agent; not
reviewed. Widths are **upper bounds** from a min-degree elimination
heuristic, so true treewidths may be smaller. Gaps are the values in
MINLPLib's `instancedata.csv` (downloaded 2026-09-29 from
<https://www.minlplib.org/instancedata.csv>), which record the best known
primal and dual bounds across solvers; they are not our runs.

## Purpose

The structure-exploiting B&B program ([PROGRAM.md](../PROGRAM.md)) predicts
that single-tree spatial B&B pays a price exponential in the number of
variables on problems whose interaction structure has small treewidth,
while decomposition-aware B&B pays only in the width. This census asks how
common small width is in a standard benchmark, and whether scalable
families of constant width become harder as they grow.

## Graphs measured

For each of the 1632 OSIL instances cached at `~/.cache/minlplib/minlplib/osil`
(read with `research-20260922/scouting/minlplib-open-data/osil.py`):

- **Factor-incidence graph** (`tw_fac_ub`). Nodes are variables, rows
  (constraints and objective) and nonlinear additive terms. A row is
  joined to its linear variables and to its term nodes; a term node
  (a quadratic product or a top-level summand of a nonlinear expression) is
  joined to its variables; single-variable terms attach directly to the row.
  This is the width relevant to a dynamic program that splits long sums
  with partial-sum variables. Plain variable–row incidence width was
  rejected because it hides the coupling inside one dense nonlinear row.
- **Nonlinear primal graph** (`tw_nlprimal_ub`): variables are adjacent
  when they occur in a common nonlinear term. Linear constraints are
  ignored, so this measures only how nonconvexities interact.

Instances without nonlinear terms are skipped. Convexity is taken from the
MINLPLib `convex` flag. Scripts: `census.py` (12 parallel parts, 90 s and
60 s elimination limits per graph), `analyze.py`; raw records in
`census_part*.jsonl` and `census_merged.json`. No run hit an error; a
few very large instances hit the time limit and have no width value.

## Aggregate results

Nonconvex instances: 1256. Among the 582 with at least 100 nonlinear
variables:

| width bound | factor-incidence width | nonlinear primal width |
|---|---|---|
| ≤ 4 | 27 (4.6%) | 278 (47.8%) |
| ≤ 8 | 40 (6.9%) | 344 (59.1%) |
| ≤ 12 | 79 (13.6%) | 365 (62.7%) |
| ≤ 20 | 114 (19.6%) | 402 (69.1%) |

Of these 582, 362 have a positive MINLPLib gap (above `1e-4`); 53 of those
have factor-incidence width at most 12.

The two columns differ because linear constraints often couple many
variables (balances, budgets, assignments). Nonconvexities themselves are
usually sparse: the median nonlinear-primal width is 2–6 in every size
class, against medians of 36–81 for the factor-incidence width of instances
with 50 or more nonlinear variables. A decomposition-aware method must
therefore either handle dense linear coupling (for example by Lagrangian
relaxation of a few coupling rows) or be limited to the smaller class.

## Scalable families of constant small width

Families with at least three sizes, constant factor-incidence width at most
12 and a growing size (MINLPLib gap in parentheses; `inf` means no finite
dual bound is recorded):

| family | sizes (nonlinear variables) | width | gaps as size grows |
|---|---|---|---|
| waterno2 (multi-period water network) | 42, 84, 126, 168, 252, 378, 504, 756, 1008 | 9 | 3e-8, 1e-7, 2e-5, 4e-6, **1.61, 5.87, 7.07, 12.7, 14.4** |
| camshape (cam design, COPS) | 100, 200, 400, 800 | 4 | 0.045, 0.129, 0.172, 0.204 |
| rocket (optimal control, COPS) | 307, 607, 1207, 2407 | 6 | 0.016, 0.014, 0.060, 8.18 |
| lnts (particle steering) | 154, 304, 604, 1204 | 11–12 | 0.055, 0.090, 0.097, 0.106 |
| kriging_peaks-full | 12 … 202, 502 | 3 | ≤ 3.3e-5 up to 202; 0.755 at 502 |
| catmix, chain (COPS control) | 303–2403; 102–802 | 4 | inf at every size |

The waterno2 family is the clearest case: instances with one to four time
periods are solved, and from six periods on the best known gap exceeds
100% and keeps growing, while the width stays 9. Discrete-time
optimal-control instances with a state dimension of one or two are also
open with essentially trivial dual bounds: dtoc5 (99999 variables, width
2, dual bound 0.00063 against primal 5.39), optcdeg2 (150002 variables,
width 4), lukvle10 (1000 variables, width 4).

## What this shows and does not show

- It shows that small interaction width is common among nonconvex
  instances when only nonlinear terms are counted, and present but less
  common (about one in seven large instances) when all constraints are
  counted.
- It shows several constant-width families whose best known gaps grow with
  size, which is what the program predicts for single-tree solvers. It
  does **not** show that width causes the difficulty: size, scaling,
  unbounded variables and solver time limits also grow with these
  families, and MINLPLib gaps reflect whichever runs were reported.
- The width values are heuristic upper bounds. A tree decomposition of
  small width is only the first requirement; separator dimension, local
  subproblem difficulty and constraint coupling decide practical cost.

## Commands run

```
python3 census.py k 12      # k = 0..11, in parallel
python3 analyze.py
python3 families.py   # family table and aggregate width counts
```

No project-wide checks were run.
