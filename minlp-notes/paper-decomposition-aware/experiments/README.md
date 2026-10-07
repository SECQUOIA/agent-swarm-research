# Experiments of Section 11 (implementation and computational illustration)

This directory holds the experiments of Section 11 of the paper: accuracy
independence of the grids (E1), conditioning (E2), dimension (E3), exact
output (E4), a comparison with SCIP (E5, E5V), unplanted random instances
(E6), localized exact acceptance (S1), the expanding-box chain (`chain/`), the
recourse diagnostics (`recourse/`) and two QPLIB instances (`qplib/`).
Terminology follows the paper: CT is the capped-trials algorithm
(Algorithm `alg:ct`), TRIAL a single trial (Algorithm `alg:trial`), EX the
exact-output procedure; "nodes per coordinate" is |G_i|, "table entries" are
bag-table entries (called "states" in the solver and in CSV column names).

Where each experiment appears in the paper (the experiment names are the
same in the paper and in this directory; tables marked "App." are in the
appendix `app:computation`, "Additional computational results"):

| Paper | Experiment | Files |
| --- | --- | --- |
| 11.2 | E1, E2, E3 (planted family; Figures fig:E1, fig:E2) | `results/E1_*`, `E2_*`, `E3_*` |
| 11.3 | expanding-box chain (table tab:chain) | `chain/` |
| 11.4 | E4 exact output; S1 localized acceptance (supplement to E4) | `results/E4_exact.csv`, `S1_*`, `S1_ex_replay.csv` |
| 11.5 | E5 comparison with SCIP, E5V variants (table tab:scip, App.) | `results/E5_*`, `E5V_*` |
| 11.6 | E6 unplanted random instances (table tab:random, App.) | `results/E6_random_growth.csv` |
| 11.7 | recourse diagnostics (table tab:recourse, App.) | `recourse/` |
| 11.8 | two binary QPLIB instances | `qplib/` |

The solver is imported **unchanged** from
`research-20261002-decomposition/solver/` (nothing is copied; the path is
resolved relative to this directory). The recourse runs also import
`completion/benchmarks/corpus.py` (with `frozen/baseline/`) and
`completion/theory/piecewise-recourse/` from the same tree, and the QPLIB
runs read `solver/extra-benchmarks/{corpus.py,data/}`. All of these files are
pinned to commit `b59ed1b836e426abf1ab3ba4bd897df464019559` (2026-10-03
00:00:43 -04:00) of the `minlp-notes` repository: they are tracked there,
were unmodified in the working tree during every run below (last
modification 2026-10-02 23:18), and their SHA-256 hashes are recorded in
`results/dependencies_sha256.json`. `results/environment.json` records the
hashes of the six core solver files at run time; they agree with
`dependencies_sha256.json`. A public artifact must bundle this tree (or the
listed files), because the repository is not public.

## Reproduce (one command per experiment group)

```bash
cd paper-decomposition-aware/experiments
python3 run_all.py              # E1-E6, E5V, S1; at most 4 worker processes
python3 run_all.py --only E3    # one experiment (comma-separated list allowed)
python3 run_all.py --figures    # rebuild CSV files and figures from results/raw
python3 summarize.py            # every number quoted in Section 11 -> results/summary.json
python3 chain/run_chain.py      # table tab:chain (writes chain/results.csv, per_stage.csv)
python3 chain/run_chain_warmstart.py   # chain started at the upper corner
python3 recourse/run_recourse.py       # table tab:recourse (writes recourse/results.csv)
python3 qplib/run_qplib.py             # QPLIB_3852 / QPLIB_5881 (about 3 minutes, 4.4 GB)
python3 replay_s1_ex.py         # reruns and replays the EX certificates of S1 (about 15 s)
python3 scip_shortfall.py       # E5: splits SCIP's primal shortfall (about 1 minute)
```

Every script writes its output into its own directory (or `results/`),
whatever the current directory.

Each task runs in a worker process with one numerical thread
(`OMP/OPENBLAS/MKL_NUM_THREADS=1`). The final run of `run_all.py`
(2026-10-03 02:00-02:13, 423 tasks, 3 workers, no failures) took 768 s wall
and 2,289 s summed task time on an Intel Xeon w5-2565X (36 logical CPUs, WSL2)
shared with other long-running jobs; the 1-minute load average was 13.1 at the
start and 15.0 at the end (up to 18 during the run). S1 was then rerun alone
(`--only S1 --jobs 4`, 15 s wall; `results/environment_S1.json`) after the
single-run threshold measurement was corrected (see S1). `qplib/run_qplib.py`
took 158 s wall (load 13.6 to 18.6), `chain/run_chain_warmstart.py` 61 s.
`chain/run_chain.py` and `recourse/run_recourse.py` are from the earlier
round (load about 11) and were not rerun; on 2026-10-03 their output paths
were changed to the script directory (the computation is unchanged).
`replay_s1_ex.py` and `scip_shortfall.py` were added and run on 2026-10-03
(load about 4, 4 workers; 16 s and 63 s wall). Timings are single measurements on a
loaded machine and indicative only. Python 3.13.11, NumPy 2.5.1, Matplotlib
3.11.1, PySCIPOpt 6.2.1 with SCIP 10.0.

## Files

| File | Content |
| --- | --- |
| `instances.py` | exact rational instance generators (planted, random mixed-integer, tied, flat, random continuous for E6) |
| `analysis.py` | quantities of the analysis computed outside the solver: the height constants of (eq:exact-constants) and the growth certificate of Lemma `lem:growthcert`(a) with a kappa bracket |
| `oracle.py` | independent exact face-and-label enumeration (no solver code) |
| `localized.py` | localized exact-acceptance test of Proposition `prop:local` (S1, E6), exact arithmetic |
| `run_all.py` | experiment design, task runner, CSV export |
| `figures.py` | one grayscale PDF figure per experiment (E1 and E2 are Figures 1 and 2 of the paper) |
| `summarize.py` | all quoted numbers in `results/summary.json` |
| `replay_s1_ex.py` | reruns the 30 EX runs of S1 and replays their certificates -> `results/S1_ex_replay.csv` |
| `scip_shortfall.py` | reruns the 21 E5 SCIP runs and splits the primal shortfall into bound and epigraph parts -> `results/E5_scip_shortfall.csv` |
| `results/dependencies_sha256.json` | commit and SHA-256 hashes of every imported file outside this directory |
| `results/raw/*.json` | one record per task, including per-stage data |
| `results/*.csv` | plot-ready tables (`*_runs.csv` per run, `*_stages.csv` per stage, `E5V_scip_variants.csv`, `E6_random_growth.csv`) |
| `results/certificates/` | gzipped exact-output certificates of E4 |
| `figures/*.pdf` | figures; the paper uses copies in `../figures/` |
| `chain/`, `recourse/`, `qplib/` | scripts and results of the other experiment groups |

## Implementation versus analysis

The solver differs from the analysis in the ways listed in appendix
`app:computation` of the paper (summarized in Section 11.1):
common mesh `h_j = s 2^-j` with the Euclidean condition number (Lemma
`lem:commonmesh`); trial cap `100 * 2^mu * ceil(log2(n+2))`, 12.5 times the
analyzed cap `8 * 2^mu * ceil(log2(n+2))`; stage limit from `(7/8) L n s^2 4^-J
<= eps` instead of `9/16`; each trial centered at the incumbent instead of
`l`; coordinate-descent polishing from `l`, `u` and the midpoint and after each
stage; optional convex presolve; the lower bound used in the success test
(`upper - lower <= epsilon`) and reported at the end = maximum over all stages
and trials, including the initial interval bound (in all CT runs of E2 and E5
the last stage's own gap was also at most epsilon); "uniform" grids are theta = 0 single-center grids, not UC; the
exact wrapper uses the row-sum height constant of Remark `rem:heights`
(common denominator also clearing `A_ij/2`), starts at q = 4, doubles q,
restarts every round from the full box with the incumbent as first center
and as a descent start in place of `l` (`warm_start`), and tests three candidates (incumbent, coordinatewise
reconstruction, stationary face point). E1-E3 run single trials (TRIAL) with a
fixed theta, no cap on the nodes per coordinate and a fixed number of stages; E2's default schedule, E5, E6, S1,
the chain and the recourse runs use CT. In E2 (default schedule) and E5,
`summarize.py` checks that no trial was aborted by the cap: the 12 restarts
all follow trials that ran to their stage limit; E6 and the chain never
restart.

Checker: `verify_certificate.py` shares model parsing, decomposition validation
and objective evaluation with the solver and nothing else. The convex
value-factor and recourse checkers reuse solver code (grids, tables, lifting).
On the replayed runs with solve time >= 0.1 s, replay took 0.81 to 2.54 times
the solve time (`summary.json`, `replay_over_solve_time`).

## Instance families

**Planted nonconvex family** (E1, E2, E3, E5, and three E4 instances). Continuous box `[-1,1]^n`,
Hessian `H = 2I + C` with sparsity given by a path, a random recursive tree,
or a band of bandwidth 2 or 3. About `n/4` coordinates (set `A`) sit at a
bound at the planted point `x*`, all with inward derivative `mu`; the rest
(set `S`) are interior with `x*_i = k/21`, `|k| <= 10`. The block
`H_SS = 2I + c W_SS` has smallest eigenvalue `4/kappa_target` up to the rounding
of `c` to a multiple of `2^-12`; entries touching `A` have magnitude 2 to 4, and
`H` is indefinite in every instance (smallest eigenvalue at most -1.16; at
most -1.75 in E1-E3 and E5, and -1.161 for the planted tree instance of E4). For `kappa_target <= 2` the
generator sets `c = 0`, so `H_SS = 2I` and the free coordinates are separable;
the initial coordinate descent then returns `x*` exactly (checked for all 18
E3 instances with `kappa_target = 2`). For `d = x - x*`,
`F(x) - F* >= d'(H + mu I_A)d / 2` (Lemma `lem:growthcert`(a), since the box
width is 2), so `g >= g_lb = lambda_min(H + mu I_A)/2`, certified by an exact
rational LDL' test; a rational Rayleigh quotient of `H_SS` gives a certified
`g_ub`. With `L = 2`, `kappa` lies in `[2/g_ub, 2/g_lb]`; `kappa_ub/kappa_lb <=
1.112`, and the certified interval lies in `[0.97, 1.12] * kappa_target`. The
objective constants are 94 to 1,577 and `F* = 0`. Caveat: once `x*` is known,
the minorant certifies it directly; the grid solver does not use this.

Off-grid minimizers: within a trial every grid node of coordinate `i` is a
dyadic rational or the first center plus a dyadic rational. In E1-E3 with
`kappa_target >= 4`, 347 of 3,177 free coordinates of `x*`, counted once per
run (10.9%), were nodes of the last grid. In the 78 single-trial runs of E1
(filtered) and E3 at `kappa_target = 4`, 146 of the 153 such coordinates had
been set to `x*_i` by the initial descent, 3 had `x*_i = 0`, and 4 had a first
center at a nonzero dyadic distance from `x*_i`
(`process/w3/checks/computation-verify-offgrid.py`).

**Random unplanted mixed-integer family** (E4, S1). Random signed sparse
Hessians with rational entries (diagonals of both signs), random rational
continuous bounds, one or two integer coordinates. Optima are not planted.

**Ties.** `tied_isolated` has exactly two isolated global minimizers (an
integer sign tie). `flat_segment` has two segments of global minimizers
(`a(x0-x1)^2` term).

**Random continuous family** (E6). `[-1,1]^n`, path or band (bandwidth 2),
`n = 8, 12, 16, 24`, five seeds each; diagonal `k/2` with `k` in `{-4..8}`,
interactions `+-k/4` with `k` in `{1..6}`, linear terms `k/4` with `k` in
`{-8..8}`. Nothing about the minimizer or kappa is prescribed; all 40 Hessians
are indefinite.

## Experiments and results

All certificates produced by `run_all.py`, `chain/` and `recourse/` were
replayed, and every replay was valid, with two exceptions in S1.
`task_localized` does not replay the certificates of its EX runs, which
supply the reference values and stage counts; `replay_s1_ex.py` reruns these
30 EX runs, reproduces status, value and completed stages of every run, and
replays every certificate (all valid; `results/S1_ex_replay.csv`). The
single-run threshold runs of S1 only measure when the certified gap falls
below a threshold and were not replayed. In every run on the planted family the
certified interval contained `F* = 0` and `x*` was never removed by filtering.

**E1, accuracy** (`E1_states_vs_stage.pdf`, figure fig:E1). Path and tree
(`n=16`, bag size 2), band (`n=12`, bag size 3) and band (`n=8`, bag size 4),
`kappa` in [3.99, 4.45], three seeds, single trials with `theta = 1/8`
(satisfies `8 kappa theta^2 <= 1`), graded or uniform grids with or without
filtering, 16 stages (mesh `h_j = 2^(1-j)`), cap 100,000 table entries per
stage. Median entries per stage on the path: filtered graded about 1,000 from
stage 4 to 15; unfiltered graded 83,161 at stage 11 (then cap); unfiltered
uniform 64,879 at stage 6 (then cap); filtered uniform about 1,100.

**Constants of Lemma `lem:commonmesh`** over all stages of the runs with
`8 kappa theta^2 <= 1` (E1 graded filtered, E2 and E3 with the theorem's
theta; 876 stages; the radius ratio uses `kappa_lb`, which can only increase it):
`D(y_j)/(L n h_j^2) <= 0.155` (bound 9/16); retained radius over
`4.2 sqrt(n kappa) h_j` `<= 0.179`; `|y_j - x*|^2 / (kappa n h_j^2) <= 0.052`
(bound 1); nodes per coordinate over `8 theta^-1 ceil(log2(n+2))` `<= 0.047`
(over the implementation cap `<= 0.0038`). Figure fig:E2 uses the bound
`4.2 sqrt(n kappa)` and the gap bound 9/16.

**E2, conditioning** (`E2_plateau_vs_kappa.pdf`, figure fig:E2). Path, `n=16`,
`kappa_target` = 2, 4, ..., 256, three seeds, 12 stages. Plateau nodes per
coordinate (max over free coordinates, median of the last 4 stages and the 3
seeds): uniform 13 -> 55, graded with the theorem's `theta` (1/8 down to 1/64)
9 -> 49, graded with `theta = 1/4` 9 -> 33.5. The retained radius grows more
slowly than `sqrt(kappa)` (theorem theta: 2.1h -> 15.2h). With `theta = 1/4`
(violates `8 kappa theta^2 <= 1` for `kappa_target >= 4`) contraction fails for
`kappa_target >= 64`: last-stage gap over `L n h^2` is 4.66, 15.3, 60.5 at 64, 128,
256 (about 0.11 with the theorem's theta). CT (`epsilon = 2^-20`) succeeded in
its first trial (`theta = 1/4`) for `kappa_target <= 32`, in trial `theta = 1/8` for
64 and 128 and `theta = 1/16` for 256; Lemma `lem:commonmesh` guarantees
success only from `theta = 1/32` or `1/64` in these cases.

**E3, dimension** (`E3_plateau_vs_n.pdf`). Paths, `n` = 4, ..., 128, three
seeds, 11 stages, `kappa_target` = 4 (coupled free block, kappa in
[3.99, 4.45]) and 2 (separable). Coupled: filtered uniform 7 -> 26 nodes per
free coordinate, graded (theta = 1/8) 9 -> 19, graded (theta = 1/4) 9 -> 17.
Separable (`kappa_target = 2`): uniform exactly `4(floor(sqrt(n/4)) + 1) + 1`
(9, 9, 13, 13, 21, 25), graded 9 -> 19.

**E4, exact output** (`E4_exact_output.pdf`). Twenty instances: twelve random
mixed-integer (`n` = 3..6), three with two isolated optima, three planted
(`n=6`), two with optimal segments. `solve_exact` with up to 3,000 stages and
30 s (flat cases 5 s). Exact output was certified for 18 of 20; all 18 values
equal the enumeration and all 18 points are optimal. The three `n=3`
instances have no continuous coordinate with positive curvature (0 or 1
stage). Stages are a step function of the last round's precision q:
67-77 stages (q = 64) for 49-65 bits, 132-144 (q = 128) for 80-120 bits, 275
(q = 256) for 208 bits, 534 (q = 512) for 342 bits, where bits =
`log2(Omega W)` with the solver's row-sum constant. With the constant of
(eq:exact-constants) (`analysis.lemma_heights`) the 18 instances need 21-315
bits instead of 49-342 (`required_gap_bits_lemma` vs `required_gap_bits_code`
in `E4_exact.csv`). The flat-segment instances stopped at 5 s with certified
gaps `2^-11.8` and `2^-10.8` against required `2^-52.5` and `2^-54.9`. The
accepted point came from a recovery proposal in 6 of 18 cases.

**E5, SCIP** (`E5_scip_comparison.pdf`, table tab:scip). Planted instances with
`kappa` in [3.99, 4.45]: path/tree `n=16`, band `n=12` and `n=8`, paths
`n` = 32, 64, 128; three seeds each. SCIP 10.0 (single thread, epigraph
formulation `min t, t >= F(x)`, absolute gap 1e-6, 20 s limit) versus CT
(`epsilon = 1e-6`, 60 s limit, convex presolve on). SCIP reported its gap as
reached on the 12 instances with `n <= 16` (0.3-5.4 s) and hit the 20 s limit
on all 9 paths with `n >= 32` (dual bounds -6.0e-5 to -7.6e-4). CT reached a
replayed gap below 1e-6 on all 21 in its first trial (solve at most 6.9 s).
`task_scip` projects SCIP's point onto the box (`v = min(max(v, lo), hi)`)
before evaluating it exactly, so `exact_value_of_scip_point`, `exact_gap`,
`scip_point_excess_over_fstar` and `epigraph_shortfall` refer to the
projected point. With SCIP's incumbent projected onto the box and evaluated
exactly (`exact_gap`), the gap to SCIP's dual bound was 2.76e-6 to 6.79e-6 on
the 12 "gap reached" runs. SCIP's incumbents violate the bound of every
active coordinate by about 1e-8 (within SCIP's tolerance; SCIP's own check
accepts them); projected onto the box they are within 1.3e-14 of `F*`. Its
dual bounds are valid, but all 21 reported primal bounds lie below `F*` (by
1.8e-6 to 1.6e-5), so SCIP's reported interval never contains `F*`. Despite
its name, `epigraph_shortfall` (= F(projected x) - t) includes the effect of
the bound violations: `scip_shortfall.py` reruns the 21 SCIP runs (every
primal bound reproduced) and splits it exactly into a bound part
F(projected x) - F(x), 51-94% of the shortfall (it equals n_A * mu * 1e-8 to
about three digits), and an epigraph part F(x) - t = 9.00e-7 to 9.03e-7
(`results/E5_scip_shortfall.csv`, which also records the largest bound
violation and F at the unprojected point). The planted objectives have constants 94-1,577
and inward derivatives 23-192.5, so 1e-6 absolute is 6e-10 to 1.1e-8 of the
constant.

**E5V, SCIP robustness** (`E5V_scip_variants.csv`). Same instances: 60 s limit
(paths `n >= 32`), primal and dual feasibility tolerances 1e-9 (paths
`n >= 32`, 20 s), objective constant as an offset (all 21, 20 s). All 27 path
runs with `n >= 32` stopped at the time limit (60 s: dual bounds -5.1e-5 to
-7.5e-4); with the offset, the 12 small instances ended with SCIP status
"gaplimit" or "optimal", with exact gaps (projected incumbent) still 1.9e-6
to 5.8e-6. SCIP's reported interval contained `F*` in none of
the 39 runs.

**E6, unplanted random instances** (`E6_random_growth.csv`, table tab:random). CT
(default schedule, no convex presolve) at `epsilon = 2^-10, ..., 2^-50`. The
candidate is the stationary point of the face of the final incumbent at
`2^-50`. Lemma `lem:growthcert`(a) certifies point growth (and brackets kappa
with an upper bound from part (b) and from moving one active coordinate to its
other endpoint) on 11 of 40 instances; brackets, rounded outward: [6.2, 6.6],
[11.6, 15.7], [14.0, 22.3], [6.1, 24.4], [10.0, 28.6], [8.1, 31.6],
[5.1, 55.8], [9.5, 67.3], [6.8, 141.9], [4.5, 182.8], [8.0, 6662.2]. On the other
29, `H + 2M` is not positive definite (growth unknown); the localized test
proved the candidate optimal on 28; one candidate (path, n=16, seed 16005)
is not proved optimal. All 10 instances with `n=8` agree with the enumeration.
Every run succeeded in the first trial (`theta = 1/4`). The largest grid had
8-18 nodes per coordinate (9-11 on the 11 instances with certified growth);
from `2^-10` to `2^-50` it was unchanged on 27 instances and changed by at most
5 nodes on the others; stages grew from 7-9 to 27-29. At
`2^-50`, 42 of the 213 free coordinates of the candidates were nodes of the
last grid.

**S1, localized exact acceptance** (`S1_localized_acceptance.pdf`). The test
in `localized.py` (Proposition `prop:local`) post-processes a replayed CT
certificate (`epsilon = 2^-60`, at most 60 stages): it narrows the retained
box by node exclusion and accepts the stationary point of the face of the
incumbent if a first/second-order minorant is positive semidefinite on the
narrowed box. On 30 random unplanted mixed-integer instances (`n` = 4..16,
paths, trees, bands, one or two integer coordinates) it accepted 29 within
five stages (0-based stage index at most 4, at most 0.03 s); on 12 of them
the test also passes with the full box `X` in place of the narrowed box. With the face candidate of Definition
`def:facecand` (`localized.face_candidate`, the rule covered by Corollary
`cor:local`) the test accepted the same 29 instances within nine stages
(0-based index at most 8), with the same values. Accepted values agree with EX on all 29, and the 12
instances with `n <= 6` match the enumeration. The one failure
(`random_path_n8_s7014`) has two optimal vertices that differ in a concave
continuous coordinate. EX (`solve_exact`) used 1 to 542 stages. One CT run
reaches the threshold of Proposition `prop:accept` (first stage with
`U - beta < 1/(Omega W)`, W the denominator of the optimal value) after 40 to 72
stages with the constant of (eq:exact-constants) and 139 to 157 with the
solver's constant, on the five instances with the most EX stages (542, 542,
542, 542, 534). The first version of this measurement tested the incumbent's
own denominator, which fails when the incumbent is near-optimal but not
exactly optimal (2 instances); the gap threshold is the correct measure.

**Chain** (`chain/`, table tab:chain). `Psi_m` of Proposition `lim:prop:messages` (called `G_m` in the scripts), `m = 2..64`, CT with `epsilon = 1e-3`.
All runs succeed in the first trial (`theta = 1/4`); largest grid 5 -> 11
nodes. The minimizer 0 is the lower corner (first polishing start and a node of
every grid). Started at the upper corner (`run_chain_warmstart.py`): same
stages, same largest grid except `m = 2` (6 instead of 5 nodes), table entries
between 2% fewer and 7.5% more.

**Recourse** (`recourse/`, table tab:recourse). Plain CT versus the recourse pipeline on
six fixed diagnostic instances, `epsilon = 2^-10`, 20 s, `max_table_states =
200000`: a stage stops with status `table_limit` when the sum over bags of
the table entries of its dynamic program would exceed 2e5 (for
`dense_mincut_33` already at the first stage, hence 0 entries). Status
`epsilon_optimal` of the recourse pipeline is reported as "certified". Plain-grid replays
of the affine stars took 26.4 s and 50.9 s (solve 20 s).

**QPLIB** (`qplib/`). QPLIB_3852 (231 binary variables) and QPLIB_5881 (120):
minimum-fill bag sizes 20 and 94; stage-0 table entries `5.72e6` and `8.0e28`.
With a cap of `10^7` entries, QPLIB_3852 is solved exactly in one stage
(bounds -234 = -234, the library value 234 after sign reversal; 156 s,
4.4 GB). The certificate was not replayed: `verify_certificate.py` searches the
bag list for the home bag of every term inside its loop over table entries,
which is slow with 231 bags.

## Limits and failures recorded

* Unfiltered variants stop at the per-stage table cap (by design).
* With `theta = 1/4` and large `kappa`, single trials stop contracting (E2);
  the hypothesis of Lemma `lem:commonmesh` is violated there.
* Flat optimal segments (E4) do not reach exact output within 5 s.
* Lemma `lem:growthcert`(a) certifies growth on only 11 of the 40 E6
  instances.
* Exact rational arithmetic in Python dominates time; timings are not
  comparable with compiled solvers in absolute terms.
* The planted family is easy to certify once `x*` is known (see above).
