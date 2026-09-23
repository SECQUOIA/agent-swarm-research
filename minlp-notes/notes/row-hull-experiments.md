# Row-hull cuts: experiment record

Date: 2026-09-21. Companion to
[results/row-hull-separable-concave.md](../results/row-hull-separable-concave.md).
Code and reproduction commands: [code/row_hull/README.md](../code/row_hull/README.md).
All numbers below come from the JSONL files named in each section. Tables are
produced by `code/row_hull/summarize.py` and `table.py`.

## Setup

- Machine: 36 logical cores, 30 GB, Linux (WSL2). Gurobi 13.0.3 (4 threads),
  SCIP 10 through PySCIPOpt (1 thread), BARON through GAMS 54 (1 thread).
  Relative gap `1e-4`, time limit 300 s. Eight Gurobi cells (or thirty
  single-thread cells) ran concurrently, so times carry machine noise; node
  counts do not.
- Forms. `orig`: the model in the repository's solver-neutral form, epigraph
  variables `w_i = f_i(x_i)` and a linear objective. `cuts`: the same model plus
  the root row-hull strengthening: closed-form extended rows (Theorem 2) for
  rows with equal widths, separated cuts (Proposition 5) for the others; only
  cuts that are binding at the last root linear program are kept, scaled to
  largest coefficient one. The solver is unmodified and receives plain linear
  rows. `total_time` starts after the instance is generated and includes the
  Python cut loop, model construction and the solve; the limit of 300 s applies
  to the total.
- Code was frozen during the final runs; hashes are in
  `code/row_hull/results/code_version.sha256`. Earlier pilot runs (different
  code states, partial) are kept in `code/row_hull/results/pilot/` and are not
  used in the tables.
- "Root gap closed" is `(LP_rowhull - LP_termwise) / (best known - LP_termwise)`
  with linear-programming bounds computed by the cut loop, not solver root
  bounds.
- Consistency check (`summarize.py`): for every instance, no dual bound of any
  run may exceed the best primal value of any run by more than `2e-4`
  relative, and no run may claim optimality at a worse value. A violation would
  indicate an invalid cut or a solver error.

## Instance families

Generators are in `code/row_hull/instances.py`; seeds 0–4.

- `transport-{uniform,random,uncap}-{quad,log,sqrt}-MxN`: `M` sources, `N`
  sinks, all arcs present, balanced supplies and demands rounded to four
  decimals. `uniform`: all arc capacities 1, supplies and demands in
  `[1.2, 3.8]` (equal widths, non-integral right-hand sides). `random`:
  capacities `U(2,8)`, two decimals. `uncap`: capacity `min(s_i, d_j)`. Costs:
  `quad` `a x - b x^2` increasing on the arc; `log` `c log(1 + 4x/u)`; `sqrt`
  `c sqrt(x)`.
- `netflow-{uniform,random}-{quad,log}-VnDd`: transshipment on a random digraph
  with `V` nodes and out-degree `D`, a third of the nodes sources and a third
  sinks, supplies at 60% of the largest feasible scale.
- `transportfc-*`: `transport` plus a fixed charge with a binary indicator on
  every arc (the structure of Lim, Linderoth and Luedtke 2018).

These are synthetic families chosen to isolate the mechanism. The MINLPLib
reach of the structure is assessed separately in
[row-hull-minlplib-scan.md](row-hull-minlplib-scan.md).

## Results

All tables below are from runs made **after** the pricing fix described under
[Review findings](#review-findings-and-their-resolution). Cells that use only
the closed form (`uniform`) and all `orig` cells were not affected and were kept;
every `cuts` cell with unequal widths was rerun. The superseded runs are in
`code/row_hull/results/superseded_pricing_bug/`.

Column legend: `n` instances with both forms recorded; solved `o/c` =
`orig`/`cuts` within 300 s at gap `1e-4` (records that fail the consistency check
are not counted as solved); time = shifted geometric mean (shift 1 s) of
`total_time`, unsolved runs at 300 s; nodes = shifted geometric mean over
instances solved by both forms; closed% = mean root gap closed; endgap% = mean
remaining gap `(best known - dual)/|best known|` of unsolved runs. Five seeds
per family, one run per cell, a loaded machine: family means support statements
about large effects, not individual ratios.

### Gurobi 13, transportation and network flow (`results/main_gurobi.jsonl`)

```
consistency: 260 records, 0 violations

solver  family                              n | solved o/c | time o   c (sgm, s) | nodes o   c (both solved) | closed% | endgap% o  c (unsolved)
gurobi  netflow-random-log-40n3d            5 |   5   5    |    16.9     2.6     |     80913      3095       |  72.6   |   nan   nan
gurobi  netflow-random-log-60n3d            5 |   0   3    |   300.0   182.0     |       nan       nan       |  74.9   | 11.05  1.66
gurobi  netflow-random-quad-40n3d           5 |   5   5    |     0.6     1.9     |      1165      1389       |  79.5   |   nan   nan
gurobi  netflow-random-quad-60n3d           5 |   5   5    |     9.4    16.6     |     22060     29391       |  80.6   |   nan   nan
gurobi  netflow-uniform-log-40n3d           5 |   3   5    |    78.2     5.0     |    159510      5751       |  65.8   |  5.52   nan
gurobi  netflow-uniform-log-60n3d           5 |   0   3    |   300.0   112.4     |       nan       nan       |  75.2   | 10.67  2.21
gurobi  netflow-uniform-quad-40n3d          5 |   5   5    |     0.6     1.2     |      1577      1919       |  71.0   |   nan   nan
gurobi  netflow-uniform-quad-60n3d          5 |   4   4    |    27.1    36.0     |     40182     32294       |  76.8   |  1.05  1.03
gurobi  transport-random-log-10x15          5 |   5   5    |    31.3    11.3     |    113103     12350       |  73.4   |   nan   nan
gurobi  transport-random-log-8x12           5 |   5   5    |     5.4     3.2     |     26361      3799       |  77.2   |   nan   nan
gurobi  transport-random-quad-10x15         5 |   5   5    |    10.0    10.9     |     27523     11193       |  81.3   |   nan   nan
gurobi  transport-random-quad-8x12          5 |   5   5    |     2.7     3.7     |     13083      3737       |  78.9   |   nan   nan
gurobi  transport-random-sqrt-10x15         5 |   3   5    |   170.1    36.4     |    343986     12247       |  72.6   |  3.53   nan
gurobi  transport-random-sqrt-8x12          5 |   5   5    |    57.5     7.3     |    277577      5939       |  79.3   |   nan   nan
gurobi  transport-uncap-log-10x15           5 |   5   5    |     5.2     7.7     |     16844      1803       |  72.1   |   nan   nan
gurobi  transport-uncap-log-8x12            5 |   5   5    |     0.8     2.8     |      3242       886       |  71.3   |   nan   nan
gurobi  transport-uncap-quad-10x15          5 |   5   5    |     1.3     5.5     |      2252       772       |  81.9   |   nan   nan
gurobi  transport-uncap-quad-8x12           5 |   5   5    |     0.5     2.4     |       933       354       |  79.8   |   nan   nan
gurobi  transport-uncap-sqrt-10x15          5 |   4   4    |    85.0    36.5     |    197963     11550       |  64.3   |  1.98  0.00
gurobi  transport-uncap-sqrt-8x12           5 |   5   5    |     4.8     7.9     |     20712      3720       |  67.6   |   nan   nan
gurobi  transport-uniform-log-10x15         5 |   0   5    |   300.0    20.3     |       nan       nan       |  80.8   |  4.34   nan
gurobi  transport-uniform-log-8x12          5 |   4   5    |    76.2     2.2     |    312396      2838       |  83.3   |  2.48   nan
gurobi  transport-uniform-quad-10x15        5 |   2   5    |   183.1    19.1     |    303166     15077       |  80.2   |  0.99   nan
gurobi  transport-uniform-quad-8x12         5 |   5   5    |    10.6     2.1     |     58923      4131       |  80.7   |   nan   nan
gurobi  transport-uniform-sqrt-10x15        5 |   0   5    |   300.0    16.6     |       nan       nan       |  85.5   |  6.04   nan
gurobi  transport-uniform-sqrt-8x12         5 |   1   5    |   160.8     3.3     |     61509       341       |  88.2   |  3.02   nan
```

Totals over 130 instance pairs: `orig` solves 96, `cuts` 124; 28 only with
cuts, none only without; mean time 22.3 s against 9.1 s. **The gain is
concentrated in the `uniform` families**, which are built so that Theorem 2
applies to every row (unit capacities, fractional supplies; with integral
supplies the residual is zero and the method adds nothing):

| Gurobi | pairs | solved `orig` | solved `cuts` | mean time `orig` | mean time `cuts` |
|---|---|---|---|---|---|
| `uniform` (closed form only) | 50 | 24 | 47 | 68.5 s | 9.6 s |
| unequal widths (separated cuts) | 80 | 72 | 77 | 10.8 s | 8.8 s |

On the 54 instances that `orig` solves in under 10 s, the run with cuts is
slower on 45. The Python cut loop takes 1.0–11.2 s for unequal widths (median
2.8 s), and the dense cuts slow the node relaxations
(`transport-random-quad-10x15`: 2.5 times fewer nodes, about the same time).
One `sqrt` run with cuts ended with Gurobi status 13 (below).

### Gurobi 13, fixed charge plus concave cost (`results/main_fc_gurobi.jsonl`)

Gurobi's own flow cover and other mixed-integer cuts are active in both forms.

```
consistency: 80 records, 0 violations

solver  family                              n | solved o/c | time o   c (sgm, s) | nodes o   c (both solved) | closed% | endgap% o  c (unsolved)
gurobi  transportfc-random-log-10x15        5 |   4   5    |    42.8    40.4     |     22526      7188       |  74.8   |  1.41   nan
gurobi  transportfc-random-log-8x12         5 |   5   5    |     3.8     6.3     |      6540      1661       |  77.4   |   nan   nan
gurobi  transportfc-random-quad-10x15       5 |   5   5    |    13.4    24.1     |     12720      6544       |  81.7   |   nan   nan
gurobi  transportfc-random-quad-8x12        5 |   5   5    |     2.0     5.7     |      1652       476       |  82.7   |   nan   nan
gurobi  transportfc-uniform-log-10x15       5 |   3   5    |   160.9     2.7     |     93927       733       |  92.4   |  1.32   nan
gurobi  transportfc-uniform-log-8x12        5 |   5   5    |     5.4     0.8     |      7613        77       |  92.4   |   nan   nan
gurobi  transportfc-uniform-quad-10x15      5 |   5   5    |    37.2    12.5     |     41392     11223       |  89.9   |   nan   nan
gurobi  transportfc-uniform-quad-8x12       5 |   5   5    |     2.9     1.1     |      2550       209       |  91.3   |   nan   nan
```

40 pairs: 37 against 40 solved; mean time 12.9 s against 6.5 s; `uniform` 18.8 s
against 2.7 s, unequal widths 8.8 s against 14.0 s. With random capacities the
node reduction (2–4 times) does not pay for the cut loop (3–15 s here) and the
denser relaxations, except on the hardest family.

### SCIP 10 and BARON (`results/main_others.jsonl`)

```
consistency: 194 records, 2 violations
  VIOLATION ('netflow-random-log-40n3d-s4', 'baron', 'orig', 72.9287731568, 66.86399570412775)
  VIOLATION ('netflow-random-log-40n3d-s4', 'baron', 'orig', 'claims optimal at', 72.9287731568, 'best', 66.86399570412775)

solver  family                              n | solved o/c | time o   c (sgm, s) | nodes o   c (both solved) | closed% | endgap% o  c (unsolved)
baron   netflow-random-log-40n3d            5 |   0   4    |   300.0    85.3     |       nan       nan       |  72.6   |  7.87  4.95
baron   netflow-random-quad-40n3d           5 |   0   4    |   300.0    54.8     |       nan       nan       |  79.5   |  7.96  3.08
baron   netflow-uniform-log-40n3d           5 |   0   2    |   300.0   275.0     |       nan       nan       |  65.8   | 11.58  4.81
baron   netflow-uniform-quad-40n3d          5 |   0   5    |   300.0    76.1     |       nan       nan       |  71.0   |  9.01   nan
baron   transport-random-log-8x12           5 |   4   5    |    89.4    37.1     |     18385      2699       |  77.2   |  5.42   nan
baron   transport-random-quad-8x12          5 |   0   4    |   300.0   137.3     |       nan       nan       |  78.9   |  4.63  2.49
baron   transport-uncap-log-8x12            5 |   5   5    |    11.4     9.3     |      1852        73       |  71.3   |   nan   nan
baron   transport-uncap-quad-8x12           5 |   5   5    |    18.6     9.6     |      1389        39       |  79.8   |   nan   nan
baron   transport-uniform-log-8x12          5 |   1   5    |   257.3    67.8     |     32953       227       |  83.3   |  5.66   nan
baron   transport-uniform-quad-8x12         5 |   0   5    |   300.0   164.3     |       nan       nan       |  80.7   |  5.13   nan
scip    netflow-random-log-40n3d            1 |   0   1    |   300.0    38.9     |       nan       nan       |  72.1   |  4.31   nan
scip    netflow-random-quad-40n3d           5 |   0   4    |   300.0    42.2     |       nan       nan       |  79.5   |  1.18  0.02
scip    netflow-uniform-log-40n3d           4 |   0   2    |   300.0   210.8     |       nan       nan       |  65.8   |  4.63  1.13
scip    netflow-uniform-quad-40n3d          5 |   0   5    |   300.0    58.6     |       nan       nan       |  71.0   |  1.39   nan
scip    transport-random-log-8x12           4 |   4   4    |    45.1    12.0     |     53205      8143       |  77.5   |   nan   nan
scip    transport-random-quad-8x12          5 |   3   5    |   203.0    25.7     |    198904     23007       |  78.9   |  0.31   nan
scip    transport-uncap-log-8x12            5 |   5   5    |     7.4     5.5     |      6653      1138       |  71.3   |   nan   nan
scip    transport-uncap-quad-8x12           5 |   5   5    |     4.8     4.7     |      5066      1102       |  79.8   |   nan   nan
scip    transport-uniform-log-8x12          5 |   1   5    |   243.0    23.4     |    117171      2531       |  83.3   |  1.91   nan
scip    transport-uniform-quad-8x12         5 |   0   5    |   300.0    19.7     |       nan       nan       |  80.7   |  0.94   nan
```

SCIP: 44 pairs with both results, 18 against 41 solved, mean time 100 s against
23 s (unequal widths: 17 against 24 of 25, 45 s against 14 s). BARON: 50 pairs,
15 valid solves against 44, mean time 144 s against 60 s (unequal widths: 14
against 27 of 30, 91 s against 37 s). No instance is solved only without cuts.
These two solvers are weak on this epigraph form to begin with (BARON solves
none of the 20 `netflow` instances without cuts), so the counts say as much
about them as about the cuts.

### Separation inside the tree: minimal branch-and-bound versus SCIP

A minimal best-bound spatial branch-and-bound written for this comparison
(`bb.py`: `T` term-wise chords, `R` plus root row-hull cuts, `L` plus exact
row-hull separation on every node box; times are for a Python loop and mean
nothing; `results/superseded_pricing_bug/bb_nodes_5x7.txt` for `uniform` and
`uncap`, which the pricing fix did not change, `results/bb_nodes_5x7_random_rerun.txt`
for `random`, identical to the earlier counts):

```
transport-uniform-quad-5x7-s0 T: nodes 6631 root 16.5143 ub 18.3010 done 32s | R: nodes 1732 root 18.0863 ub 18.3012 done 26s | L: nodes 191 root 18.0863 ub 18.3010 done 87s
transport-uniform-quad-5x7-s1 T: nodes 2064 root 19.9891 ub 21.2925 done 6s | R: nodes 614 root 21.0236 ub 21.2926 done 7s | L: nodes 21 root 21.0236 ub 21.2925 done 7s
transport-uniform-quad-5x7-s2 T: nodes 4650 root 18.4228 ub 19.7321 done 16s | R: nodes 904 root 19.4663 ub 19.7322 done 15s | L: nodes 87 root 19.4663 ub 19.7321 done 47s
transport-random-quad-5x7-s0 T: nodes 3424 root 66.9214 ub 73.8926 done 9s | R: nodes 1769 root 72.5482 ub 73.8934 done 15s | L: nodes 198 root 72.5482 ub 73.8926 done 80s
transport-random-quad-5x7-s1 T: nodes 10342 root 90.3980 ub 98.7034 done 28s | R: nodes 5230 root 97.0146 ub 98.7035 done 44s | L: nodes 254 root 97.0146 ub 98.7034 done 92s
transport-random-quad-5x7-s2 T: nodes 5409 root 54.6570 ub 62.4904 done 14s | R: nodes 1455 root 60.8378 ub 62.4908 done 11s | L: nodes 105 root 60.8378 ub 62.4904 done 39s
transport-uncap-quad-5x7-s0 T: nodes 123 root 61.8436 ub 67.0538 done 1s | R: nodes 52 root 65.8691 ub 67.0542 done 1s | L: nodes 7 root 65.8691 ub 67.0551 done 4s
transport-uncap-quad-5x7-s1 T: nodes 323 root 72.0899 ub 79.1144 done 2s | R: nodes 104 root 76.0172 ub 79.1144 done 1s | L: nodes 20 root 76.0172 ub 79.1144 done 10s
transport-uncap-quad-5x7-s2 T: nodes 144 root 65.5842 ub 72.7264 done 1s | R: nodes 43 root 72.3551 ub 72.7264 done 1s | L: nodes 5 root 72.3551 ub 72.7264 done 2s
```

The ratio of `R` to `L` nodes ranges from 5 to 29. On the three `uniform`
instances, recomputing only the closed-form inequality of Proposition 3 on
every node box (`bb_cf.py`, mode `C`, printed to the terminal only) needed 564,
243 and 586 nodes.

**Measured in SCIP (`scip_sepa.py`, `sweep_sepa.sh`, `results/scip_sepa_sweep.jsonl`).**
A PySCIPOpt separator adds row-hull cuts as local rows at every node up to a
depth limit (closed form where the local widths are equal, column generation
otherwise; after the pricing fix). Below the root, branching makes the local
widths unequal even on `uniform` instances, so node separation always runs the
column-generation path (profile: 36 of 40 s in `separate`). SCIP 10, 1 thread,
300 s, `8x12`, seeds 0–4; columns: solved / shifted geometric mean time / nodes
/ time in the separator / mean end gap of unsolved runs. Two `random-log` cells
are missing because of SCIP's "error in LP solver" on seed 1.

```
records 98 dual above best primal: []
family                         |     native |       root |    tree_d3 |    tree_d8 | tree_d1000
solved / sgm time (s) / sgm nodes / sgm sepa time (s) / mean end gap % of unsolved
transport-random-log-8x12      | 4/4    34  53205    0  0.0 | 5/5    11   7437    3  0.0 | 5/5    12   6758    4  0.0 | 5/5    18   6327   10  0.0 | 4/4    71   4955   65  0.0
transport-random-quad-8x12     | 5/5   166 302856    0  0.0 | 5/5    31  29424    3  0.0 | 5/5    31  28115    4  0.0 | 5/5    35  23250   13  0.0 | 5/5   136  14924  120  0.0
transport-uniform-log-8x12     | 2/5   217 339754    0  2.2 | 5/5    28  20917    1  0.0 | 5/5    31  21210    3  0.0 | 5/5    37  20483   10  0.0 | 2/5   137   6215  126  0.6
transport-uniform-quad-8x12    | 1/5   285 474178    0  0.9 | 5/5    23  21323    1  0.0 | 5/5    24  21803    2  0.0 | 5/5    29  17214   11  0.0 | 5/5   143  12906  127  0.0
```

Root-only separation is the best configuration on every family. Separating to
depth 3 costs about the same and changes nodes by less than 10%; to depth 8 it
reduces nodes by 5–20% and adds 8–12 s; on every node it reduces nodes by a
factor 1.3–3.4 but the callback takes 65–127 s and the runs are 4–5 times
slower than root-only, losing three `uniform-log` solves. The 5–29 fold node
reductions of the minimal branch-and-bound do not transfer to SCIP, whose own
branching, propagation and cuts already exploit much of what the local row
hull adds. Whether a native implementation with cheap local separation would
change this is untested; the closed form is not available at nodes.

### Controls

- **Objective form** (`run_objform.py`, `results/control_objform.jsonl`). For
  quadratic costs the concave quadratic was also stated directly in the
  objective (a nonconvex QP for Gurobi) instead of through epigraph variables.
  Solved / mean time for objective form, `orig`, `cuts`:
  `transport-uniform-quad-8x12` 5/5/5 and 7.5/10.6/2.1 s;
  `transport-uniform-quad-10x15` 3/2/5 and 167/183/19 s;
  `transport-random-quad-8x12` 1.9/2.7/4.5 s; `10x15` 10.1/10.0/14.9 s;
  `transport-uncap-quad` 0.4/0.5/2.7 s and 1.2/1.3/6.3 s. The epigraph form
  costs Gurobi at most about 40% and does not change any conclusion.
- **Solver root bounds with fixed charges** (`root_bounds.py`,
  `results/root_bounds_fc.jsonl`, Gurobi with `NodeLimit = 1`, its own cuts on).
  Mean root gap in percent of the best known value, for term-wise LP / row-hull
  LP / Gurobi root / Gurobi root with row-hull rows:
  `uniform-quad` 18.5 / 1.6 / 2.2 / 0.7; `uniform-log` 18.7 / 1.4 / 4.8 / 0.8;
  `random-quad` 19.4 / 3.4 / 3.5 / 2.3; `random-log` 26.2 / 6.0 / 7.0 / 3.9
  (rerun after the pricing fix).
  Gurobi's flow covers and other cuts already close most of the term-wise gap;
  the row-hull rows roughly halve what remains.
- **MINLPLib concave quadratic programs** (`minlplib_qp.py`,
  `results/minlplib_qp.jsonl`). Nine library instances are continuous separable
  concave quadratic programs with linear rows and finite bounds. Root gap
  closed: `ex2_1_1` 100%, `ex2_1_5` 3.5%, `ex2_1_6` 63%, `ex2_1_8` 98.8%,
  `st_bsj3` 0%, `st_bsj4` 100%, `st_e22` 90.5%, `st_e26` 96.1%, `st_ht` 91.7%.
  All nine are solved in under 0.1 s with or without cuts, so this shows that
  the cuts are valid and strong on real small models and nothing about time.

## Unfavorable and negative findings

1. **Easy instances get slower.** See the counts above; on `transport-uncap-*`
   and `netflow-*-quad-40n3d`, where the solvers need at most a few seconds,
   the cuts cost a factor of 2 to 5 in time for Gurobi. A default deployment
   would need a native implementation and the usual cut management.
2. **Gurobi status 13 on `sqrt` costs.** One final run with cuts
   (`transport-uncap-sqrt-10x15-s0`) ended with status `SUBOPTIMAL` at relative
   gap `1.6e-4`; it is counted as unsolved. Before the pricing fix a second
   `sqrt` run did the same, and a pilot before the cuts were scaled showed it
   on a third instance. No such run occurred without cuts or with `quad`/`log`
   costs.
3. **General-width closed form is weak.** Proposition 3 with exact residual
   intervals recovers little on rows with random widths:
   `transport-random-sqrt-8x12-s0` has term-wise bound 63.61, closed-form bound
   66.97, exact row-hull bound 73.64 (optimum 75.85); on the `uncap` instance
   of the same size 56.40, 56.66 and 62.61 (optimum 65.74), where only 5 of 20
   rows are nondegenerate.
4. **Dense rows with general coefficients gain little.** On the repository's
   `cknap` family (every variable in every row, integer coefficients 1–20) the
   cut loop closed 26% of the root gap for `n = 25, m = 2` and less than 0.01%
   for `n = 50, m = 5`; these instances are solved in a fraction of a second
   anyway. The mechanism matters for sparse network-type rows.
5. **Aggregated rows add little.** `proto_aggregate.py` adds the closed-form
   hulls of all node-pair cut rows (190 extra rows on `transport-uniform-quad-8x12`);
   the root bound moves from 29.81 to 30.09 (seed 0, optimum 30.48), from 31.45
   to 31.57 and from 24.60 to 24.65; node triples add nothing further.
6. **Strength against the tilted flow covers.** `lll_closure.py` computes the
   root bound of *all* tilted simple generalized flow covers of Lim, Linderoth
   and Luedtke at `z = 1`, both orientations of each row, by exhaustive cover
   enumeration (their implementation tilts only covers found by CPLEX, and an
   indicator-free model has none). On six `4x6` instances the closure recovers
   between 85% and 100% of the row-hull improvement (for example 11.11 / 12.07 /
   12.18 for term-wise / closure / row hull). The row hull is therefore only
   modestly stronger than that family as a relaxation; what it adds is a
   complete description, a separation routine that does not enumerate covers,
   and applicability without indicators.
7. **MINLPLib reach is small.** The [structural scan](row-hull-minlplib-scan.md)
   finds an applicable row in 77 of 1,601 instances (4.8%), mostly rows with two
   concave items; Theorem 2 applies exactly only in `ex2_1_8`. The technique
   targets concave-cost network and allocation models, which MINLPLib contains
   only in small sizes.

8. **Few concave terms: nothing to gain.** `facility.py` builds concave-cost
   facility sizing models (8 facilities with concave throughput costs, 20
   customers, linear transport costs). All concave terms lie on the *implied*
   row `sum_i y_i = total demand`, so cuts were separated on that aggregated
   row. They close 8–12 points of a root gap of 30–70%, but Gurobi solves the
   original models in 0.2–0.5 s and 21–31 nodes, because branching on eight
   concave variables is cheap; the cut loop alone took 23 s (pilot,
   `results/facility_pilot.jsonl`, 4 instances). The mechanism matters when
   many concave terms share few rows, which is the Shapley–Folkman regime, not
   when the concave terms are few.

## Solver errors observed

- BARON (GAMS 54) reports `optimal` with value 72.929 on the *original*
  `netflow-random-log-40n3d-s4`; Gurobi and BARON with cuts find 66.864. The run
  is excluded by the consistency check. In a pilot, BARON also returned wrong
  "optimal" values at zero nodes on `sqrt` costs (102.52 against 75.85 on
  `transport-random-sqrt-8x12-s0`), the behaviour already recorded for power
  terms in [the vertex-binarization record](separable-vertex-binarization-experiments.md);
  `sqrt` instances were therefore not run with BARON.
- SCIP 10 stops with "error in LP solver" on five original `log` models and on
  one model with cuts (`netflow-random-log-40n3d-s1` in the final runs); these
  cells are missing from the tables. `sweep.py` discards the solver's message
  and records an `IndexError`; the message was confirmed by hand on
  `transport-random-log-8x12-s1`.
- SCIP makes little progress on `sqrt` costs with or without cuts (depth above
  250 near `x = 0`, pilot runs); `sqrt` instances were not run with SCIP in the
  final study.

## Checks

- `test_rowhull.py`: 216 checks against brute-force vertex enumeration
  (separation equals the exact membership value, every cut valid at every
  vertex, pricing lower bounds with and without interval merging, closed form
  equals the hull for equal widths including inequality rows and indicators,
  closed form valid for general widths). Command:
  `uv run --project ../minlp_solver_lab python -m pytest -q test_rowhull.py` (216 passed,
  including the regression test for coinciding subset sums).
- The cut loop reproduces the brute-force row-hull bound of the first prototype
  (`proto_general.py`, 42.7869 on `uncap 5x7 seed 0`).
- The [independent theory review](review-row-hull-theory.md) wrote its own
  exact-arithmetic checks (`code/row_hull/review/`).
- Consistency of all final runs: no dual bound above the best primal value
  beyond `2e-4` except the BARON record above. This check is coarse: its
  tolerance is twice the gap limit, and it did not detect the pricing bug.
- `check_cuts_bruteforce.py` (`results/cuts_bruteforce_check.jsonl`): every cut
  separated on 15 study instances is compared with the minimum over all row
  vertices by plain subset enumeration (numbers under Review findings).

## Review findings and their resolution

Theory review ([report](review-row-hull-theory.md)): Theorem 2(c) lacked the
bounds `0 <= z_i <= w y_i`; "weaker otherwise" after Proposition 3 was false as a
universal claim; conventions and hypotheses were missing (nonempty `X`,
`rho = sup`, `delta = 0`, objective of Proposition 6, hypotheses of the
Shapley–Folkman bound). All corrected in the results file. A
[source check](row-hull-ktr-overlap-check.md) prompted by that review showed that
Theorem 2 is the Padberg–Van Roy–Wolsey constant-capacity description in other
variables; the novelty claim was reduced accordingly.

Code and experiment review ([report](review-row-hull-code-experiments.md)):

1. **Invalid cuts from the pricing routine (fixed).** `pricing._compress`
   removed duplicate subset sums by sorting on the exact float and keeping the
   first state. Sums that are equal in exact arithmetic but differ in the last
   place (`2.37 + 5.12` and `3.49 + 4.00`) were then ordered by rounding error,
   and the state with the larger profit could be lost. The returned "lower
   bound" was then too large and the cut invalid. Two-decimal capacities
   (`random` families) triggered it; integer and generic real widths did not,
   which is why the original tests passed. The reviewer found 91 invalid cuts
   among 9,955 on 38 study instances, 12 instances where such a cut reached the
   solver, and two cells in which the optimum of the original model violated
   kept cuts (the recorded optimal values differed by `1e-5` relative, inside
   the gap tolerance, so the consistency check could not see it). Resolution:
   near-equal sums are now grouped and the largest profit, smallest `lo` and
   largest `hi` are kept; `separate` rejects a cut whose pricing minimum exceeds
   the dual constant by more than `1e-6`; a regression test with one- and
   two-decimal widths was added (80 cases); all affected cells were rerun.
   After the fix: the reviewer's `check_pricing.py` and `check_row_cuts.py`
   report 0 failures (before: up to 49 of 300 rows and 34 of 382 cuts);
   `check_cuts_bruteforce.py` finds 0 invalid among 6,966 cuts on 15 study
   instances by plain enumeration of all row vertices;
   `review_code/check_optimum_cut_off.py` finds no kept cut violated by the
   optimum on its six cells (`results/optimum_cut_off_after_fix.jsonl`; before:
   5 and 1 violated cuts on two cells). Validity remains "up to floating
   point": no exact arithmetic is used.
2. **Numbers.** "47 of 53" was the subset also solved with cuts (now stated as
   45 of 54 for the final runs); the BARON mean time counted a wrong-optimum
   run at its own time (now 144 s); the node ratio range is 5–29, not 7–30; the
   cut loop range was understated; `total_time` does not include instance
   generation. All corrected above.
3. **Fairness.** The headline counts are driven by the `uniform` families; the
   split is now stated with the totals. The objective-form control is reported.
   Five seeds, single runs and a loaded machine limit what the means support;
   this is now said in the legend.
4. **Reproducibility.** The code README now lists every script and command.
   `run_queue.sh` rewrites the hash file at each start, so
   `results/code_version.sha256` records the code of the final reruns.
