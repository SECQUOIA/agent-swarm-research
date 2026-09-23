# Composite univariate envelopes: experiment record

Date: 2026-09-21. Companion to
[the result note](../results/composite-univariate-envelopes.md). Numbers come
from the JSON-lines files under `code/univariate_envelopes/results/` and
`code/vertex_binarization/results/`; the tables are produced by
`tables_separable.py`, `analyze_minlplib.py --table` and `root_bounds.py`.

## Setup

SCIP 10.0 through PySCIPOpt 6.2.1, one thread, relative gap `1e-4`, 120 s
limit. Times are wall clock and include reading, the presolve pass for
bounds, curvature certification and model construction. Modes:

- `native`: the model as given.
- `split`: every accepted composite univariate subexpression gets an
  auxiliary variable `w` with the native constraint `w == g(x)`; no handler.
  This isolates the effect of the reformulation.
- `hybrid`: `split` plus the envelope handler (cuts, propagation, completion
  heuristic). SCIP keeps feasibility, branching and NLP heuristics.
- `uenv` (separable families only): the handler alone enforces `w == g(x)`.

Baselines on the separable families: Gurobi 13.0.3 (4 threads) and BARON
through GAMS 54.3.1 (1 thread), on the direct model.

## Separable families

`quartic`: `min sum_i p_i(x_i)` with random two-well quartics on
`[-2.5, 2.5]`; `sigmoid`: negative logistic utilities written with `exp` on
`[0, 6]`; `m` dense linear rows; three seeds. All five columns ran while other
sweeps shared the machine, so only the contrast between seconds and time
limits is meaningful. In the SCIP columns `w` has the range of `g` as bounds;
in the Gurobi and BARON columns the bounds are 5% wider. Cells are seconds
with the node count in parentheses, or `TL` with the gap between the dual
bound and the best known value; `!` marks a returned point more than `1e-3`
worse than the best known.

| family | n | m | seed | scip native | scip hybrid | scip uenv | gurobi | baron |
|---|---|---|---|---|---|---|---|---|
| quartic | 10 | 1 | 1 | TL 0.79% | 2.0 (11) | 1.2 (3) | TL 29.20% | 75.6 (7409) |
| quartic | 10 | 1 | 2 | 3.0 (1585) | 0.7 (1) | 1.6 (5) | TL 34.92% | 55.5 (8425) |
| quartic | 10 | 1 | 3 | TL 0.02% | 1.8 (3) | 1.2 (3) | TL 11.43% | 45.3 (8081) |
| quartic | 10 | 3 | 1 | 25.6 (13971) | 4.1 (30) | 6.5 (34) | 64.6 (482672) | 30.1 (6431) |
| quartic | 10 | 3 | 2 | TL 0.08% | 0.8 (1) | 1.4 (3) | 104.1 (987263) | 5.7 (39) |
| quartic | 10 | 3 | 3 | TL 0.03% | 0.9 (1) | 1.1 (3) | 46.3 (325493) | 16.9 (2117) |
| quartic | 20 | 1 | 1 | TL 4.91%! | 1.6 (1) | 1.7 (1) | TL 73.69%! | TL 68.86%! |
| quartic | 20 | 1 | 2 | TL 3.57% | 2.5 (11) | 1.9 (3) | TL 100.25%! | TL 73.29% |
| quartic | 20 | 1 | 3 | TL 0.19% | 2.9 (11) | 2.4 (5) | TL 52.05% | TL 55.16% |
| quartic | 20 | 3 | 1 | TL 5.04%! | 5.3 (15) | 7.1 (13) | TL 72.94%! | TL 63.64% |
| quartic | 20 | 3 | 2 | TL 5.04% | 8.2 (81) | 6.6 (21) | TL 95.62%! | TL 75.97% |
| quartic | 20 | 3 | 3 | TL 2.98%! | 13.0 (41) | 4.8 (13) | TL 61.10%! | TL 51.10%! |
| quartic | 40 | 1 | 1 | TL 1.83%! | 6.5 (3) | 6.9 (6) | TL 93.58%! | TL 95.84%! |
| quartic | 40 | 1 | 2 | TL 0.01% | 4.6 (6) | 3.4 (2) | TL 46.53%! | TL 40.16% |
| quartic | 40 | 1 | 3 | TL 0.20%! | 2.4 (1) | 2.6 (1) | TL 80.60%! | TL 77.18%! |
| quartic | 40 | 3 | 1 | TL 3.89%! | 14.8 (51) | 8.5 (7) | TL 101.84%! | TL 97.93%! |
| quartic | 40 | 3 | 2 | TL 1.34%! | 11.6 (11) | 8.5 (10) | TL 50.68%! | TL 45.35%! |
| quartic | 40 | 3 | 3 | TL 0.42%! | 8.2 (11) | 7.9 (7) | TL 84.20%! | TL 79.79% |
| quartic | 80 | 1 | 1 | TL 0.99%! | 5.3 (1) | 3.6 (1) | TL 75.79%! | TL 74.93%! |
| quartic | 80 | 1 | 2 | TL 0.02%! | 2.9 (1) | 3.8 (1) | TL 64.99%! | TL 61.83%! |
| quartic | 80 | 1 | 3 | TL 0.05%! | 5.3 (1) | 3.5 (1) | TL 69.67%! | TL 69.25%! |
| quartic | 80 | 3 | 1 | TL 1.11%! | 14.5 (5) | 12.0 (6) | TL 76.13%! | TL 76.77%! |
| quartic | 80 | 3 | 2 | TL 0.64%! | 15.3 (6) | 11.4 (5) | TL 64.70%! | TL 65.50%! |
| quartic | 80 | 3 | 3 | TL 2.11%! | 8.2 (2) | 10.1 (3) | TL 71.88%! | TL 72.13%! |
| sigmoid | 10 | 1 | 1 | 4.3 (4301) | 0.4 (1) | 0.7 (5) | 0.0 (1) | 1.3 (413) |
| sigmoid | 10 | 1 | 2 | 13.5 (9856) | 0.3 (1) | 0.5 (3) | 0.0 (1) | 3.5 (2693) |
| sigmoid | 10 | 1 | 3 | 3.1 (2404) | 0.5 (1) | 0.4 (1) | 0.0 (1) | 0.9 (281) |
| sigmoid | 10 | 3 | 1 | 4.4 (3121) | 1.1 (11) | 0.6 (3) | 0.0 (193) | 1.3 (65) |
| sigmoid | 10 | 3 | 2 | 16.5 (11126) | 1.2 (7) | 1.4 (9) | 0.0 (125) | 6.8 (5395) |
| sigmoid | 10 | 3 | 3 | 2.9 (1877) | 0.4 (1) | 0.7 (5) | 0.0 (1) | 1.1 (359) |
| sigmoid | 20 | 1 | 1 | TL 28.64% | 2.5 (11) | 1.7 (5) | 0.1 (431) | TL 7.06% |
| sigmoid | 20 | 1 | 2 | TL 50.77%! | 4.3 (41) | 1.7 (5) | 0.1 (26) | TL 13.67% |
| sigmoid | 20 | 1 | 3 | TL 35.88% | 2.5 (11) | 1.4 (5) | 0.0 (15) | TL 13.39% |
| sigmoid | 20 | 3 | 1 | TL 31.59% | 8.6 (91) | 5.2 (22) | 0.1 (401) | TL 9.72% |
| sigmoid | 20 | 3 | 2 | TL 49.33%! | 2.9 (11) | 2.2 (7) | 0.1 (1175) | TL 11.19% |
| sigmoid | 20 | 3 | 3 | TL 34.82% | 3.7 (21) | 3.1 (8) | 0.1 (449) | TL 14.23% |
| sigmoid | 40 | 1 | 1 | TL 68.79%! | 2.0 (1) | 3.7 (5) | 0.4 (1569) | TL 15.36% |
| sigmoid | 40 | 1 | 2 | TL 64.11%! | 5.1 (11) | 3.8 (5) | 0.3 (1931) | TL 17.00% |
| sigmoid | 40 | 1 | 3 | TL 68.72%! | 4.8 (11) | 5.9 (10) | 0.3 (2290) | TL 16.82%! |
| sigmoid | 40 | 3 | 1 | TL 60.69% | 1.7 (1) | 3.8 (7) | 0.1 (912) | TL 15.33% |
| sigmoid | 40 | 3 | 2 | TL 59.97%! | 8.4 (27) | 11.9 (17) | 0.3 (2255) | TL 18.60% |
| sigmoid | 40 | 3 | 3 | TL 60.93%! | 4.8 (11) | 5.6 (10) | 0.3 (1945) | TL 17.39% |
| sigmoid | 80 | 1 | 1 | TL 75.53%! | 4.1 (1) | 3.4 (1) | 0.1 (1) | TL 19.89%! |
| sigmoid | 80 | 1 | 2 | TL 71.79%! | 3.7 (1) | 5.0 (2) | 0.1 (3) | TL 19.48%! |
| sigmoid | 80 | 1 | 3 | TL 82.86%! | 5.0 (1) | 5.5 (2) | 0.3 (7) | TL 21.78%! |
| sigmoid | 80 | 3 | 1 | TL 73.98%! | 10.7 (21) | 12.5 (9) | 0.4 (1466) | TL 20.21%! |
| sigmoid | 80 | 3 | 2 | TL 69.73%! | 9.7 (11) | 6.2 (4) | 0.4 (1331) | TL 20.05% |
| sigmoid | 80 | 3 | 3 | TL 80.86%! | 4.5 (1) | 4.8 (2) | 0.1 (1) | TL 22.18%! |

Solved within the limit (returned point within 1e-3 of the best known):

- quartic, baron: 6/24
- quartic, gurobi: 3/24
- quartic, scip hybrid: 24/24
- quartic, scip native: 2/24
- quartic, scip uenv: 24/24
- sigmoid, baron: 6/24
- sigmoid, gurobi: 24/24
- sigmoid, scip hybrid: 24/24
- sigmoid, scip native: 6/24
- sigmoid, scip uenv: 24/24


Reading: with the handler SCIP solves all 48 instances, in at most 15.3 s and
at most 91 nodes. Native SCIP solves 8, Gurobi 27 (all 24 sigmoid, 3
quartic), BARON 12. Python cut generation dominates the handler's time; node
counts are the better indicator of relaxation strength.

A side experiment (not stored): Gurobi's deprecated polynomial function
constraint, which treats a quartic as one function, reached a root gap of
0.01% on `quartic` `n = 20`, `m = 1`, seed 1, but needed 1.3 million nodes
and 39 s for the `1e-4` gap and did not finish `n = 40` in 60 s.

## MINLPLib

Selection. `scan_minlplib.py` parsed 1,594 of 1,632 OSiL files (38 use
`signpower`, `erf`, `tanh`, `log10`, `min`, `gammaFn`, or exceed 30 MB). 744
have general nonlinear rows and 140 contain a composite univariate
subexpression. `prepass.py` found 115 where at least one candidate has a
finite presolved domain and certifies (2 timed out, 2 use variable
exponents, the rest have only unbounded or uncertifiable candidates). The
sweep uses the 108 with at most 1,100 accepted candidates; the seven left
out are `arki0016`, `arki0017`, `arki0018`, the four `eg_*_s`. `t1000`
failed in `split` mode by harness timeout and is excluded, leaving 107.

Soundness. `consistency.py` compares every run's dual and primal bound with
the MINLPLib reference bounds at `1e-3` relative tolerance: no violation in
324 runs. The reviewer's check at `1e-4` on the earlier sweep also found none.

Aggregate (final sweep `minlplib_v3.jsonl`, idle machine, 12 concurrent
single-thread runs):

| mode | solved of 107 | shifted geometric mean time (shift 1 s, limit for unsolved) |
|---|---|---|
| native | 54 | 15.9 s |
| split | 53 | 16.6 s |
| hybrid | 51 | 21.3 s |

Hybrid against native: solved only by hybrid 2 (`arki0003`, `pricing050`),
only by native 5 (`ann_peaks_exp`, `ex1233`, `ex8_5_6`, `heatexch_spec2`,
`kan_r3_h1_n3`); both solved: hybrid more than twice as fast on 2, more than
twice as slow on 16; neither solved: hybrid's final dual bound is closer to
the reference optimum by more than 0.02 (relative, capped at 1) on 11 and
farther on 10; 61 similar. `arki0003` is also solved by `split` alone, so
that gain comes from the reformulation, not from the envelopes. `pricing050`
is solved at the root in 17 s only with the envelopes; native stops at 17%
gap and `split` at 10%.

Root bounds. root gap to reference, hybrid vs native: smaller by >10% on 35, larger by >10% on 4, similar on 42; not comparable (no root LP bound in a mode) 27 The pairs in parentheses below are
the root gap relative to the reference optimum, native then hybrid.

```
  better: ann_compressor_exp (1.41 -> 0.286); ann_cumene_exp (19.2 -> 2.46); ann_fermentation_exp (0.111 -> 0.0894); ann_peaks_exp (24.6 -> 12.3); arki0002 (1 -> 0.253); btest14 (606 -> 0.522); cesam2log (861 -> 0.513); chain100 (87.9 -> 0.865); chain200 (125 -> 0.897); chain50 (43.6 -> 1.18); ex1233 (0.298 -> 0.118); ex4_1_3 (4.98 -> 1.03e-10); ex4_1_6 (725 -> 3.49e-10); ex4_1_9 (0.269 -> 3.45e-05); ex6_1_2 (322 -> 19.8); ex6_2_9 (1.71e+04 -> 1.53e+04); gams02 (0.988 -> 0.408); ghg_1veh (0.228 -> 0.204); heatexch_spec1 (0.264 -> 0.145); inscribedsquare01 (3.04 -> 0.01); inscribedsquare02 (3.13 -> 2.51); inscribedsquare03 (5.6 -> 0.778); kriging_peaks-full010 (93.2 -> 1.33); kriging_peaks-full030 (28.6 -> 0.446); kriging_peaks-full050 (105 -> 2.23); kriging_peaks-full100 (126 -> 2.71); kriging_peaks-full200 (204 -> 4.2); kriging_peaks-full500 (334 -> 6.4); mathopt6 (0.0504 -> 0.0426); nvs01 (0.523 -> 0.258); procurement1large (3.95 -> 0.0107); procurement1mot (8.05 -> 0.213); st_e04 (0.192 -> 0.162); st_e19 (2.49 -> 0.00103); synheat (0.256 -> 0.21)
  worse: heatexch_spec2 (0.0361 -> 0.0617); heatexch_spec3 (0.193 -> 0.22); kan_peaks_h1_n5 (2.67 -> 3.04); launch (7.24e-05 -> 9.13e-05)
```

Reading. The envelopes strengthen the root relaxation on 35 of 81
comparable instances, often by orders of magnitude, and weaken it slightly on
4. Within 120 s this does not translate into more solved instances: the
Python handler makes nodes 5 to 20 times slower (for example `ex6_2_11`:
218,902 native nodes against 9,232 hybrid nodes in 120 s), it loses on
instances that SCIP already solves in seconds, and on several families
(`ex6_2_*`, `ghg_*`) the final bound is worse. Whether a native
implementation would convert the root gains into end-to-end gains is
untested.

Per-instance results (`used` = accepted candidates; `ref. gap` = distance
between the final dual bound and the reference optimum, capped at 100%):

| instance | used | native | split | hybrid |
|---|---|---|---|---|
| ann_compressor_exp | 40 | 1.4 s (127) | 1.5 s (117) | 23.8 s (191) |
| ann_cumene_exp | 249 | TL, ref. gap 88.2% | TL, ref. gap 91.9% | TL, ref. gap 70.2% |
| ann_fermentation_exp | 1 | 0.4 s (1111) | 0.2 s (451) | 10.1 s (6596) |
| ann_peaks_exp | 47 | 10.6 s (971) | 15.0 s (1041) | TL, ref. gap 4.2% |
| arki0002 | 912 | TL, ref. gap 100.0% | TL, ref. gap 100.0% | TL, ref. gap 25.3% |
| arki0003 | 1080 | TL, ref. gap 0.0% | 2.0 s (1) | 3.8 s (1) |
| arki0015 | 168 | TL, ref. gap 2.6% | TL, ref. gap 2.6% | TL, ref. gap 2.6% |
| arki0019 | 0 | TL, ref. gap 31.2% | TL, ref. gap 31.2% | TL, ref. gap 31.2% |
| arki0020 | 0 | TL, ref. gap 24.1% | TL, ref. gap 24.1% | TL, ref. gap 24.1% |
| arki0021 | 0 | TL, ref. gap 21.4% | TL, ref. gap 21.4% | TL, ref. gap 21.4% |
| btest14 | 16 | TL, ref. gap 3.2% | TL, ref. gap 2.7% | TL, ref. gap 4.1% |
| camcns | 6 | TL, ref. gap 0.0% | TL, ref. gap 0.0% | TL, ref. gap 0.0% |
| cesam2log | 157 | TL, ref. gap 100.0% | TL, ref. gap 100.0% | TL, ref. gap 38.4% |
| chain100 | 301 | TL, ref. gap 100.0% | TL, ref. gap 100.0% | TL, ref. gap 84.9% |
| chain200 | 601 | TL, ref. gap 100.0% | TL, ref. gap 100.0% | TL, ref. gap 89.7% |
| chain50 | 151 | TL, ref. gap 100.0% | TL, ref. gap 100.0% | TL, ref. gap 82.1% |
| chenery | 4 | 0.7 s (325) | 0.7 s (251) | 3.1 s (252) |
| chp_partload | 295 | TL, ref. gap 12.8% | TL, ref. gap 12.8% | TL, ref. gap 13.0% |
| cvxnonsep_nsig40r | 2 | 0.1 s (1) | 0.1 s (1) | 0.2 s (1) |
| ex1226 | 1 | 0.0 s (1) | 0.1 s (1) | 0.1 s (1) |
| ex1233 | 4 | 35.5 s (30171) | 98.2 s (138483) | TL, ref. gap 0.6% |
| ex14_1_8 | 4 | 0.0 s (1) | 0.2 s (1) | 0.3 s (1) |
| ex14_1_9 | 2 | 0.0 s (1) | 0.1 s (1) | 0.1 s (1) |
| ex4_1_1 | 1 | 0.1 s (27) | 0.1 s (1) | 0.1 s (1) |
| ex4_1_2 | 1 | 0.2 s (21) | 0.4 s (1) | 0.3 s (1) |
| ex4_1_3 | 1 | 0.1 s (31) | 0.1 s (1) | 0.1 s (1) |
| ex4_1_4 | 1 | 0.1 s (60) | 0.1 s (0) | 0.1 s (0) |
| ex4_1_6 | 1 | 0.1 s (51) | 0.1 s (1) | 0.1 s (1) |
| ex4_1_7 | 1 | 0.1 s (11) | 0.0 s (1) | 0.1 s (1) |
| ex4_1_9 | 2 | 0.1 s (37) | 0.2 s (37) | 0.1 s (1) |
| ex6_1_2 | 2 | 0.3 s (383) | TL, ref. gap 13.0% | 0.3 s (21) |
| ex6_1_4 | 3 | 0.2 s (51) | 0.2 s (55) | 0.7 s (53) |
| ex6_2_10 | 6 | TL, ref. gap 78.0% | TL, ref. gap 75.7% | TL, ref. gap 79.9% |
| ex6_2_11 | 3 | TL, ref. gap 97.2% | TL, ref. gap 98.0% | TL, ref. gap 100.0% |
| ex6_2_12 | 4 | TL, ref. gap 2.1% | TL, ref. gap 2.2% | TL, ref. gap 3.8% |
| ex6_2_13 | 6 | TL, ref. gap 86.7% | TL, ref. gap 86.5% | TL, ref. gap 93.8% |
| ex6_2_14 | 4 | 34.2 s (23281) | 35.2 s (23651) | 20.3 s (1779) |
| ex6_2_5 | 6 | TL, ref. gap 96.1% | TL, ref. gap 99.2% | TL, ref. gap 99.5% |
| ex6_2_6 | 3 | 6.2 s (12484) | 6.7 s (12023) | 60.2 s (11966) |
| ex6_2_7 | 9 | TL, ref. gap 94.6% | TL, ref. gap 95.0% | TL, ref. gap 99.2% |
| ex6_2_8 | 3 | 4.3 s (6276) | 4.3 s (6141) | 41.2 s (5928) |
| ex6_2_9 | 4 | TL, ref. gap 71.2% | TL, ref. gap 73.0% | TL, ref. gap 91.9% |
| ex8_1_2 | 1 | 0.8 s (3333) | 0.3 s (1) | 0.2 s (1) |
| ex8_3_13 | 10 | TL, ref. gap 56.9% | TL, ref. gap 56.9% | TL, ref. gap 56.9% |
| ex8_4_8_bnd | 10 | TL, ref. gap 100.0% | TL, ref. gap 100.0% | TL, ref. gap 100.0% |
| ex8_5_5 | 1 | TL, ref. gap 33.5% | TL, ref. gap 31.0% | TL, ref. gap 43.1% |
| ex8_5_6 | 1 | 8.3 s (10267) | 28.6 s (31223) | TL, ref. gap 100.0% |
| ex8_6_1 | 8 | TL, ref. gap 100.0% | TL, ref. gap 100.0% | TL, ref. gap 100.0% |
| feedtray | 54 | TL, ref. gap 80.5% | TL, ref. gap 80.5% | TL, ref. gap 80.5% |
| gams02 | 96 | TL, ref. gap 94.6% | TL, ref. gap 94.3% | TL, ref. gap 39.0% |
| gancns | 4 | TL, ref. gap 0.0% | TL, ref. gap 0.0% | TL, ref. gap 0.0% |
| ghg_1veh | 14 | 3.6 s (1552) | 3.8 s (1232) | 24.4 s (672) |
| ghg_2veh | 29 | TL, ref. gap 11.8% | TL, ref. gap 6.8% | TL, ref. gap 41.8% |
| ghg_3veh | 44 | TL, ref. gap 91.7% | TL, ref. gap 90.0% | TL, ref. gap 100.0% |
| heatexch_gen2 | 1 | TL, ref. gap 8.2% | TL, ref. gap 8.2% | TL, ref. gap 8.2% |
| heatexch_spec1 | 4 | TL, ref. gap 3.3% | TL, ref. gap 6.9% | TL, ref. gap 4.5% |
| heatexch_spec2 | 6 | 34.2 s (31023) | TL, ref. gap 0.0% | TL, ref. gap 0.4% |
| heatexch_spec3 | 10 | TL, ref. gap 12.1% | TL, ref. gap 11.3% | TL, ref. gap 13.3% |
| heatexch_trigen | 5 | TL, ref. gap 1.2% | TL, ref. gap 0.9% | TL, ref. gap 1.6% |
| hs62 | 1 | 0.6 s (901) | 1.0 s (1262) | 4.2 s (792) |
| inscribedsquare01 | 8 | 0.3 s (303) | 0.3 s (43) | 2.0 s (31) |
| inscribedsquare02 | 8 | 0.6 s (719) | 0.8 s (831) | 32.8 s (459) |
| inscribedsquare03 | 8 | 3.3 s (3480) | 2.5 s (1999) | 94.5 s (1286) |
| kan_peaks_h1_n2_g24 | 6 | 24.7 s (846) | 34.5 s (1866) | 75.4 s (1019) |
| kan_peaks_h1_n2_g3 | 6 | 1.9 s (309) | 1.9 s (266) | 6.5 s (252) |
| kan_peaks_h1_n5 | 15 | TL, ref. gap 72.7% | TL, ref. gap 72.1% | TL, ref. gap 75.2% |
| kan_r3_h1_n3 | 12 | 82.0 s (2366) | 53.1 s (1337) | TL, ref. gap 0.0% |
| kan_r3_h1_n4 | 16 | TL, ref. gap 100.0% | TL, ref. gap 100.0% | TL, ref. gap 100.0% |
| kan_r3_h1_n5 | 20 | TL, ref. gap 100.0% | TL, ref. gap 100.0% | TL, ref. gap 100.0% |
| kan_r3_h1_n9 | 36 | TL, ref. gap 100.0% | TL, ref. gap 100.0% | TL, ref. gap 100.0% |
| kan_r5_h1_n3 | 18 | TL, ref. gap 98.7% | TL, ref. gap 98.9% | TL, ref. gap 98.4% |
| kan_r5_h1_n5 | 30 | TL, ref. gap 100.0% | TL, ref. gap 100.0% | TL, ref. gap 100.0% |
| kan_r5_h1_n8 | 48 | TL, ref. gap 100.0% | TL, ref. gap 100.0% | TL, ref. gap 100.0% |
| kriging_peaks-full010 | 10 | 1.3 s (751) | 1.5 s (515) | 3.1 s (21) |
| kriging_peaks-full020 | 20 | 10.1 s (2166) | 10.3 s (1836) | 3.8 s (1) |
| kriging_peaks-full030 | 30 | 18.9 s (2757) | 13.4 s (1480) | 22.3 s (171) |
| kriging_peaks-full050 | 50 | 41.0 s (3117) | 40.0 s (2545) | 100.2 s (411) |
| kriging_peaks-full100 | 100 | TL, ref. gap 19.9% | TL, ref. gap 6.8% | TL, ref. gap 67.1% |
| kriging_peaks-full200 | 200 | TL, ref. gap 88.5% | TL, ref. gap 78.6% | TL, ref. gap 80.8% |
| kriging_peaks-full500 | 500 | TL, ref. gap 99.7% | TL, ref. gap 90.2% | TL, ref. gap 86.5% |
| launch | 4 | 0.1 s (1) | 0.1 s (1) | 0.2 s (1) |
| mathopt5_1 | 1 | 0.0 s (1) | 0.1 s (1) | 0.1 s (1) |
| mathopt5_2 | 1 | 0.0 s (1) | 0.1 s (1) | 0.3 s (1) |
| mathopt5_3 | 1 | 0.1 s (21) | 0.1 s (1) | 0.1 s (1) |
| mathopt5_4 | 1 | 2.9 s (31282) | 0.1 s (1) | 0.1 s (1) |
| mathopt5_5 | 1 | 0.1 s (25) | 0.1 s (1) | 0.2 s (1) |
| mathopt5_6 | 1 | 0.0 s (1) | 0.1 s (1) | 0.1 s (1) |
| mathopt5_7 | 1 | 0.1 s (41) | 0.1 s (1) | 0.1 s (1) |
| mathopt5_8 | 1 | 0.1 s (39) | 0.1 s (1) | 0.1 s (1) |
| mathopt6 | 2 | 0.1 s (137) | 0.6 s (83) | 19.1 s (39) |
| minlphi | 2 | 0.3 s (71) | 0.4 s (71) | 0.5 s (63) |
| nvs01 | 2 | 0.1 s (15) | 0.1 s (15) | 0.2 s (20) |
| nvs08 | 1 | 0.1 s (1) | 0.1 s (1) | 0.2 s (1) |
| nvs09 | 10 | 0.1 s (37) | 0.1 s (2) | 1.0 s (27) |
| nvs20 | 16 | 0.7 s (81) | 1.0 s (82) | 5.1 s (96) |
| pricing050 | 249 | TL, ref. gap 17.1% | TL, ref. gap 10.3% | 17.1 s (1) |
| primary | 2 | TL, ref. gap 98.7% | TL, ref. gap 98.7% | TL, ref. gap 98.7% |
| procurement1large | 680 | TL, ref. gap 78.7% | TL, ref. gap 5.3% | TL, ref. gap 1.1% |
| procurement1mot | 120 | TL, ref. gap 83.8% | TL, ref. gap 11.0% | TL, ref. gap 8.9% |
| st_e04 | 1 | 0.2 s (9) | 0.4 s (9) | 0.3 s (9) |
| st_e19 | 1 | 0.1 s (31) | 0.1 s (15) | 0.1 s (3) |
| super3t | 164 | TL, ref. gap 31.4% | TL, ref. gap 31.4% | TL, ref. gap 31.4% |
| synheat | 4 | TL, ref. gap 1.8% | TL, ref. gap 6.1% | TL, ref. gap 0.0% |
| trig | 1 | 0.0 s (3) | 0.1 s (1) | 0.2 s (1) |
| uselinear | 61 | TL, ref. gap 100.0% | TL, ref. gap 100.0% | TL, ref. gap 100.0% |
| var_con10 | 24 | TL, ref. gap 100.0% | TL, ref. gap 100.0% | TL, ref. gap 100.0% |
| var_con5 | 24 | TL, ref. gap 100.0% | TL, ref. gap 100.0% | TL, ref. gap 100.0% |


## Superseded sweep

`minlplib_v2.jsonl` (native and hybrid only) ran before the review fixes and
the certification speed-up, on a loaded machine. It is kept for the record;
its conclusions agree in direction with the final sweep.

## Review findings and their resolution

The [independent review](review-composite-univariate-envelopes.md) is kept
as written. Resolutions:

1. Local/global cut flag: a cut is now marked local whenever the node
   interval differs from the global one at all (`uenv/scip_plugin.py`).
2. Domain of `g`: certification now requires a finite ball enclosure of `g`
   itself on every interval, so `log(x)` on a negative interval or a pole is
   rejected (`test_envelope.py::test_domain_and_singular_endpoints`). The
   sympy simplification caveat is stated in the note.
3. Hanging certification: unsupported functions raise at once; expressions
   above 400 operations and certifications above 20,000 intervals are
   rejected; ball evaluation is compiled once per function; the mean-value
   form of the second derivative is used when the natural enclosure is
   undecided.
4. Domain tolerance: the presolved bounds are now imposed on `x` in the
   `split` and `hybrid` models.
5. Minor: singular endpoints other than `0` are handled (with the stated
   continuity assumption); the tiny-interval branch uses the rigorous inner
   bound with a relative shift; the standalone fallback and the unmerged OSiL
   quadratic terms are stated as limitations.
6. Wording: "exact" and "certified" are now scoped; the MINLPLib counts list
   unparsed and applicable files; Proposition 3 is attributed with its
   hypotheses and marked as not re-read.

Performance changes after profiling: cached endpoint evaluations and piece
lookup by bisection in `uenv/envelope.py`; backward trimming of `x` only when
the interval of `w` is smaller than the range of `g`.

## Reproduction

See `code/univariate_envelopes/README.md`. Targeted checks run on
2026-09-21: `test_envelope.py` (2 passed), `test_plugin.py` (4 passed),
`../vertex_binarization/test_sob.py` (14 passed), `consistency.py` on the
final sweep (0 violations). No project-wide verification was run locally.
