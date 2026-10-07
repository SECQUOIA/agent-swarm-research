# Campaign 4 digest: Part C4, path family with a binding coupling row (written 2026-10-03)

Part C4 (protocol Amendment 1) takes the 20 C3 instances and replaces the coupling row by
`sum_i y_i <= c`, with c about half of `sum_i y_i*`. This row binds, so cuts in the row directions
alone no longer give the optimum. This digest covers the replay, the root and full runs, the funnel,
the reference values and the directions of the recorded cuts. Timings are descriptive: the host was
shared, with up to six single-threaded workers. Bounds are SCIP's or Gurobi's numerical bounds. Only
the recorded cuts are certified, and they were checked by the replay, which passed.

## Main findings

- Replay passed: 48,000 of 48,000 recorded cuts were replayed and accepted. The tampering controls
  rejected 14 of 14 mutations for each cut mode. There were no config or Gurobi-parameter failures.
- Root gap closed relative to the optimum, median over 20 instances: rowdir-wide 0.986, frozen-wide
  0.953, baseline-extra 0.615. Relative to bound (ii) the medians are 0.986, 0.954 and 0.615. No root
  run reached bound (ii), and no root-run bound exceeded it. The closest a root run came is 1.1e-5
  below (rowdir-wide, n10_s6).
- Full runs (300 s): frozen-wide and rowdir-wide each solved 20/20, baseline-extra 13, baseline 10
  and Gurobi 6.
- Every cut-mode run stopped at the cut cap of 16n cuts. No run reached the support-call cap, the
  10-callback cap or the 60 s time budget.
- Directions: nearly all cuts came from the LP direction search (11,986 of 12,000 in frozen-wide,
  11,236 of 12,000 in rowdir-wide). Of these, 11,955 and 11,205 have a nonzero y_i
  coefficient. Their partial slopes in y_i are mostly negative, the sign needed when the coupling row
  binds. No cut involves only (y_i, t_i): almost all also have nonzero x_i and z_i coefficients. The
  row-direction cuts of rowdir-wide (exactly one per block in each run, 750 per phase) have a zero y_i
  coefficient. On their
  own they would give at most `sum_i min phi_i`, which is below the baseline root bound on 10 of the
  20 instances.

## Commands run (targeted, local; no project-wide tests, no CI)

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
PY=/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python
cd /workspace/minlp-notes/paper-certified-support-cuts/experiments/v4
nohup $PY replay_v4.py runs/partC4 > runs/replay-partC4.log 2>&1 &   # started 21:50:33Z, done before 22:18:45Z
$PY summarize_c4.py runs/partC4 --dest results-c4      # once while the replay ran, again after it passed
$PY summarize_v4.py runs/partC4 --dest results-c4v     # same; needed for the time decomposition and native statistics
cd ../../verification
$PY campaign4_c4_digest.py                              # read-only; rerun after the replay finished
```

`summarize_c4.py` imports `summarize_v4.py` for its definitions but does not output the callback time
split, so `summarize_v4.py` was also run. After the replay the only change in both summaries was the
replay line. Short read-only checks were also run from `mktemp` files. Their logic is now part of
`campaign4_c4_digest.py`, except for one check: the y_i coefficient of every cut is zero or nonzero
consistently in four places (a_y - lambda aff_y; the exact, exported and SCIP-stored rows; 46,376
nonzero and 1,624 zero, root and full runs together).

No SCIP or Gurobi solve was started. No record, case, snapshot or code under `experiments/` was
changed. Files written: `runs/partC4/replay.json` and `runs/replay-partC4.log` (by the replay),
`results-c4/` and `results-c4v/` (summarizer output), `verification/campaign4_c4_digest.py` (new,
read-only analysis) and this file. The manuscript was not edited.

## Sources and abbreviations

- **RP** = `experiments/v4/runs/partC4/replay.json`; **RL** = `experiments/v4/runs/replay-partC4.log`.
- **C** = `experiments/v4/results-c4/c4-summary.json` and **CR** = `results-c4/c4-results.md`
  (`summarize_c4.py`). Paths like `C root gap_closed_median` mean `phases["mechanism/root"]...`.
- **V** = `experiments/v4/results-c4v/summary.json` and **VR** = `results-c4v/results.md`
  (`summarize_v4.py`).
- **REF** = `experiments/v4/c4-references.json`. The case fields `known_optimum` and
  `reference_bound_ii` equal REF `optimum` and `bound_ii.value` on all 20 instances (P(checks)).
- **P(x)** = section x of the output of `verification/campaign4_c4_digest.py` (sections checks, a-f).
  It reads `records.jsonl`, `cases/`, RP, REF and the C3 cases, and imports the `summarize_v4.py`
  definitions unchanged.
- Definitions (as in `summarize_v4.py`): root bound = `root_dual`, or the final `dual` for a run that
  ended at the root without a finite `root_dual`. Solved = status optimal or gaplimit, with
  `primal_check.passed`. Time = `total_seconds + preparation_seconds`. SCIP time =
  `scip_solve_seconds` (Gurobi: `solver_runtime_seconds`). Callback = `separation.callback_seconds`.
  SGM = shifted geometric mean, shift 1 s.
- Gap closed = (root(m) - root(baseline)) / (ref - root(baseline)), where ref is the optimum or bound (ii).
- n10_s5 abbreviates `interleaved_path_coupled_n10_s5`. Ranges are median [min, max] over the five
  instances of each n, or over all 20.

## (a) Replay

Source: RP (also the single line of RL).

| Field | Value |
|---|---|
| passed / archived_passed | true / true |
| records / bound_runs / admitted_runs | 180 / 160 / 160 |
| cuts / replayed_cuts | 48,000 / 48,000 (frozen-wide 24,000, rowdir-wide 24,000; 12,000 per mode and phase) |
| failed runs (`runs[].passed` false) | 0 |
| missing_cut_logs | 0 |
| v4.coverage | scheduled 180 = recorded 180; missing, unscheduled, duplicates: none |
| v4.config_failures (of config_checked_runs) | 0 of 160 |
| v4.gurobi_failures (of gurobi_checked_runs) | 0 of 20 |
| omitted_runs | the 20 Gurobi records (timelimit 14, optimal 6), 0 cuts; omitted by design (no `original_model`) |
| source_files_verified | 106 |
| replay_seconds / wrapper_seconds | 1658.4 / 1684.3 |
| replay_source_sha256 / wrapper_source_sha256 | `10115390a428ca2e...` / `05e0138106104ee5...` (equals `sha256sum replay_v4.py`) |

Tampering controls (RP `v4.tamper_controls_by_mode`, `tamper_rejections`). Each control keeps only the
first cut of the record and applies each of the 14 archived mutations separately.

| Cut mode | Control record | Cuts in record | Untampered first cut passed | Mutations rejected |
|---|---|---:|---|---:|
| frozen-wide | 001_interleaved_path_coupled_n80_s6__full__s0__frozen-wide | 1280 | true | 14 of 14 |
| rowdir-wide | 002_interleaved_path_coupled_n80_s7__full__s0__rowdir-wide | 1280 | true | 14 of 14 |

The part-level control (`tamper_rejections`) also rejected 14 of 14.
`v4.tamper_controls_cover_all_cut_modes` is true.

The 48,000 replayed cuts contain each cut list twice. On every instance, the root run and the full
run of a cut mode recorded identical cut lists (same exact row, right-hand side and block; 20/20 per
mode, P(d)). So there are 24,000 distinct cut records. If the C4 count is added to the totals in
`evidence/campaign4-replay.md`: campaign 4 = 56,771 + 48,000 = 104,771 replayed cuts; campaigns 3 and 4
without v3d = 64,269 + 48,000 = 112,269; with v3d = 95,267 + 48,000 = 143,267.

## (b) Root runs (node limit 1, 120 s soft / 180 s hard)

Statuses (P(b); C root `by_mode.<m>.status_counts`): baseline and baseline-extra nodelimit 20/20.
frozen-wide and rowdir-wide nodelimit 19 and gaplimit 1 each. The gaplimit run is n10_s6 in both modes,
at 1 node. No root run ended with status optimal, and none hit the time limit. Charged time, median
[min, max]: baseline 1.082 [0.3045, 2.336] s, baseline-extra 1.278 [0.3859, 2.576] s, frozen-wide
10.77 [3.007, 33.16] s, rowdir-wide 11.12 [3.213, 34.48] s (P(b)).

n10_s6 detail (P(b)): the root bounds are 0.2546312 (frozen-wide) and 0.2546430 (rowdir-wide). The
incumbent is 0.2546538 in both. The optimum and bound (ii) are both 0.2546539.

Root bounds, median [min, max] (P(b); per-instance values in CR, "Root bounds" table):

| Mode | n=10 | n=20 | n=40 | n=80 |
|---|---|---|---|---|
| baseline | -0.0234 [-0.1117, 0.2214] | 0.09005 [-0.0242, 0.2429] | 0.0889 [-0.2923, 0.205] | 0.2171 [-0.1272, 0.7687] |
| baseline-extra | 0.01975 [-0.07763, 0.2353] | 0.2405 [0.1192, 0.4682] | 0.4817 [0.2029, 0.6438] | 0.9267 [0.6044, 1.463] |
| frozen-wide | 0.1284 [0.04714, 0.2546] | 0.3407 [0.33, 0.5257] | 0.613 [0.4903, 0.8234] | 1.273 [1.112, 1.76] |
| rowdir-wide | 0.1297 [0.06637, 0.2546] | 0.3473 [0.3301, 0.5369] | 0.6259 [0.5173, 0.8405] | 1.325 [1.166, 1.812] |
| optimum (REF) | 0.1301 [0.06988, 0.2547] | 0.3526 [0.3327, 0.5402] | 0.6300 [0.5366, 0.8541] | 1.341 [1.186, 1.840] |

Every mode's root bound is better than baseline's on 20/20 instances, at rtol 1e-4 and 1e-6
(C root `bounds`).

Root gap closed relative to the optimum, median [min, max] (P(b); the medians equal
C root `gap_closed_median.optimum`; the extreme values are from C root `gap_rows`):

| Mode | n=10 | n=20 | n=40 | n=80 | all 20 |
|---|---|---|---|---|---|
| baseline-extra | 0.287 [0.188, 0.640] | 0.600 [0.299, 0.758] | 0.685 [0.594, 0.734] | 0.655 [0.553, 0.684] | 0.615 [0.188 n10_s8, 0.758 n20_s8] |
| frozen-wide | 0.983 [0.875, 0.999] | 0.960 [0.945, 0.986] | 0.954 [0.944, 0.969] | 0.933 [0.926, 0.943] | 0.953 [0.875 n10_s8, 0.9993 n10_s6] |
| rowdir-wide | 0.997 [0.981, 0.9997] | 0.989 [0.984, 0.997] | 0.981 [0.977, 0.992] | 0.982 [0.974, 0.986] | 0.986 [0.974 n80_s5, 0.9997 n10_s6] |

Root gap closed relative to bound (ii) (P(b); C root `gap_closed_median.bound_ii`). This differs from
the table above only on the 7 instances where bound (ii) is below the optimum (see (e)):

| Mode | n=10 | n=20 | n=40 | n=80 | all 20 |
|---|---|---|---|---|---|
| baseline-extra | 0.287 [0.188, 0.641] | 0.600 [0.299, 0.760] | 0.685 [0.594, 0.734] | 0.655 [0.553, 0.684] | 0.615 [0.188, 0.760] |
| frozen-wide | 0.984 [0.875, 0.999] | 0.960 [0.945, 0.986] | 0.954 [0.944, 0.969] | 0.933 [0.926, 0.943] | 0.954 [0.875, 0.9993] |
| rowdir-wide | 0.997 [0.981, 0.9997] | 0.991 [0.985, 0.997] | 0.981 [0.977, 0.992] | 0.982 [0.974, 0.986] | 0.986 [0.974, 0.9997] |

Root bound minus bound (ii) (P(b)):

| Mode | Min (instance) | Max (instance) | n=10 median | n=20 | n=40 | n=80 |
|---|---|---|---:|---:|---:|---:|
| baseline | -1.413 (n80_s7) | -0.03328 (n10_s6) | -0.155 | -0.297 | -0.558 | -1.19 |
| baseline-extra | -0.5813 (n80_s8) | -0.01931 (n10_s6) | -0.0904 | -0.100 | -0.210 | -0.414 |
| frozen-wide | -0.1043 (n80_s7) | -2.273e-5 (n10_s6) | -0.0027 | -0.0117 | -0.0290 | -0.0735 |
| rowdir-wide | -0.02876 (n80_s9) | -1.096e-5 (n10_s6) | -0.000474 | -0.00263 | -0.0101 | -0.0251 |

- No root-run bound exceeds bound (ii) or the optimum, in any mode (P(b)). The gap to bound (ii) grows
  with n. At n=80 rowdir-wide stays 0.0158-0.0288 below it. These runs stopped at the 16n cut cap (see
  (d)).
- Root bounds of the full runs are higher on some instances (P(b), P(d)), even though their cut lists
  are identical to the root runs'. A full run's `root_dual` differs from the root run's on 1
  (baseline), 2 (baseline-extra), 4 (frozen-wide) and 12 (rowdir-wide) instances. Where both are
  finite, the full run's value is higher (example: rowdir-wide n40_s8, 0.7404318 vs 0.7504922). In
  every such run, original variables are FIXED in SCIP's transformed problem at the end
  (`native_statistics.original_variable_status`). No root run has a FIXED variable. So after the
  separator finished, SCIP did something extra at the root of the full runs, such as fixing variables
  with the incumbent's objective cutoff, possibly followed by a restart. SCIP logs were not recorded,
  so the mechanism is inferred, not verified.
- **Root-node bounds above bound (ii) occur only in full runs.** Six full runs ended with gaplimit at
  1 node with a bound above bound (ii) (P(b), "full-run root bound"): frozen-wide n10_s7 (+7.15e-6) and
  n10_s9 (+5.51e-5); rowdir-wide n10_s7 (+9.34e-6), n10_s9 (+4.75e-5), n20_s6 (+1.12e-5) and n20_s8
  (+5.92e-4). Each lies below the optimum, whose margins over bound (ii) are 1.53e-5, 6.10e-5, 2.71e-5
  and 6.47e-4. Explanation: bound (ii) limits LP relaxations built from inequalities that are each
  valid for one block (x_i, y_i, z_i, t_i) on its original box, plus the coupling row. Reductions that
  use the incumbent's objective cutoff (reduced-cost fixing, cutoff-based bound tightening) combine all
  blocks through the objective. They remove only points no better than the incumbent, so they are
  valid, but the block closure does not limit them. All six runs have FIXED variables. No SCIP final
  bound exceeds the exact optimum in any mode (P(c)).

## (c) Full runs (300 s soft / 360 s hard)

| Mode | Solved / 20 | Statuses | Instances solved | Time of solved runs (s) | Median nodes, all 20 | Solved at 1 node |
|---|---:|---|---|---|---:|---|
| baseline | 10 | optimal 10, timelimit 10 | n10_s5-s9, n20_s5-s9 | 1.598 [0.4948, 14.08] | 22,533.5 | 0 |
| baseline-extra | 13 | optimal 12, gaplimit 1, timelimit 7 | n10, n20, n40_s5, s6, s8 | 1.929 [0.4624, 98.96] | 19,584 | 1 (n10_s6) |
| frozen-wide | 20 | optimal 15, gaplimit 5 | all | 11.85 [3.267, 107.5] | 83.5 | 4 (n10_s5, s6, s7, s9) |
| rowdir-wide | 20 | optimal 9, gaplimit 11 | all | 11.04 [3.244, 133.7] | 1 | 11 (n10_s5-s9; n20_s5, s6, s8, s9; n40_s5, s8) |
| gurobi | 6 | optimal 6, timelimit 14 | n10_s5-s9, n20_s9 | 0.1103 [0.03426, 0.42] | 156,598 | - |

Sources: C full `by_mode.<m>.solved`, `status_counts`, `nodes.<m>.median_nodes_all`; instance lists,
times and 1-node runs from P(c). All runs solved at 1 node have status gaplimit.

Times over the 6 instances solved by all five modes (n10_s5-s9, n20_s9). Sources: C full `times.sgm`,
`times.sgm_solver_seconds`, `nodes.<m>.median_nodes_common_solved`, `times.ratio_summary`; SCIP time
excluding the callback and the callback SGM from VR / P(c).

| Mode | SGM time (s) | SGM SCIP/Gurobi (s) | SGM SCIP excl. callback (s) | SGM callback (s) | Median nodes | Median per-run time ratio vs baseline (pairs; faster) |
|---|---:|---:|---:|---:|---:|---|
| baseline | 0.9168 | 0.8778 | - | - | 239.5 | - |
| baseline-extra | 0.8636 | 0.8251 | - | - | 113 | 0.7346 (10; 7) |
| frozen-wide | 3.996 | 3.959 | 0.5505 | 3.41 | 1 | 3.514 (10; 2) |
| rowdir-wide | 3.737 | 3.695 | 0.2356 | 3.465 | 1 | 3.248 (10; 2) |
| gurobi | 0.1429 | 0.1386 | - | - | 70 | 0.1502 (6; 6) |

The ratio column uses all instances solved by both the mode and baseline. Over the 10 instances solved
by all four SCIP modes (n10, n20), the SGMs are baseline 2.496 s, baseline-extra 1.900 s, frozen-wide
5.126 s and rowdir-wide 4.905 s. Median nodes there: 476, 289.5, 9 and 1 (P(c)). frozen-wide and
rowdir-wide over all 20 runs: SGM 12.96 s and 12.20 s (VR). n80 times range from 37.6 to 108 s
(frozen-wide) and from 37.3 to 134 s (rowdir-wide) (CR full table).

Final dual bound against baseline at rtol 1e-4 (C full `bounds["0.0001"]`; P(c)): baseline-extra,
frozen-wide and rowdir-wide are each better on 10 (all n40 and n80) and tie on 10. Gurobi is better on
10, ties on 6 and is worse on 4 (n20_s5, s6, s7, s8, which baseline solved and Gurobi did not). At
rtol 1e-6, rowdir-wide is "worse" on all 10 commonly solved instances, because 11 of its runs stop at
the 1e-4 gap limit with a lower final bound than baseline's optimal runs (C full `bounds["1e-06"]`).

Final bounds against the exact optimum (P(c); REF `optimum_exact`):
- No SCIP run's final dual is above the exact optimum. Over solved runs, final dual minus the optimum is:
  baseline -5.05e-6 [-7.9e-6, -2.15e-6], baseline-extra -8.06e-6 [-1.96e-5, -2.91e-6], frozen-wide
  -1.13e-5 [-1.63e-4, -4.01e-6], rowdir-wide -1.97e-5 [-5.92e-5, -5.31e-6]. The largest gaps come from
  gaplimit stops; frozen-wide n80_s5, for example, has final dual 1.78331 against optimum 1.78347.
- SCIP incumbents lie up to 3.08e-5 below the exact optimum (rowdir-wide n80_s5). Gurobi incumbents lie
  up to 1.28e-5 below (n40_s9). These incumbents are slightly infeasible within tolerance. All 180
  incumbents passed the 1e-5 original-model check, with max scaled violation 9.97e-7 (P(checks)).

Gurobi (13.0.3, Threads 1, NonConvex 2, MIPGap 1e-4, Seed 0, TimeLimit = remaining soft budget; record
`gurobi_params`). Source: P(c), record fields `status`, `gurobi_status_name`, `primal`, `dual`,
`mip_gap`, `nodes`, `primal_check`.

| Instances | Status | Final bound - exact optimum | `mip_gap` | Time (s) / nodes |
|---|---|---|---|---|
| n10_s5, s6, s7, s8, s9 | optimal (OPTIMAL) | **+2.0e-8, +3.3e-8, +2.7e-8, +1.11e-9, +1.29e-8 (above the optimum)** | 0 | 0.0834, 0.0343, 0.110, 0.136, 0.111 / 39, 5, 95, 309, 45 |
| n20_s9 | optimal (OPTIMAL) | -6.89e-6 | 0 | 0.42 / 815 |
| n20_s5, s6, s7, s8 | timelimit (TIME_LIMIT) | -3.26e-4, -6.32e-4, -3.98e-4, -2.60e-4 | 9.46e-4, 1.32e-3, 1.11e-3, 4.76e-4 | 300.2 / 941,457-1,242,198 |
| n40_s5-s9 | timelimit | -3.33e-3 to -8.92e-3 | 3.89e-3 to 0.0166 | 300.2 / 377,298-441,453 |
| n80_s5-s9 | timelimit | -0.0734 to -0.113 | 0.0456 to 0.0879 | 300.2 / 126,449-162,053 |

On the five n10 runs, Gurobi's bound equals its incumbent and lies above the exact optimum by at most
3.3e-8 (n10_s6). This is within Gurobi's tolerances and much smaller than in C2/C3 (up to +1.16e-6;
`evidence/campaign4-digest.md`). The reference check flagged none of them (C `flagged` 0).

## (d) Funnel, caps and time decomposition

The separator runs only at depth 0, and the root and full runs of each cut mode recorded identical cut
lists. So the funnel is identical in the two phases; only the callback seconds differ (C and V,
`by_mode.<m>.funnel` in both phases; P(d)).

| Mode | Runs | Callbacks | Support calls | Cert. failures | Certified | Rounding rej. | Below threshold | Binding rej. (runs): causes | Cuts | Candidate LPs | Exchange samples |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|
| frozen-wide | 20 | 141 | 14,186 | 0 | 14,186 | 0 | 1,939 | 247 (20): column_set_differs_tiny_coefficient_dropped 247 | 12,000 | 14,179 | 13,079 |
| rowdir-wide | 20 | 141 | 15,204 | 0 | 15,204 | 0 | 2,989 | 215 (20): column_set_differs_tiny_coefficient_dropped 215 | 12,000 | 14,381 | 13,383 |

Below threshold = certified - rounding - binding - cuts. Sampling failures are 0. Repeat skips: 6
(frozen-wide) and 12 (rowdir-wide). No variable-status causes were recorded, and there were no
classifier errors. Share of violated rows rejected at binding: 247/12,247 = 2.0% and 215/12,215 = 1.8%.

Caps (P(d); each run's `config` and `separation`):

| Cap (config) | frozen-wide (root / full) | rowdir-wide (root / full) |
|---|---|---|
| max_cuts = 16n | reached in 20/20 / 20/20 (cuts = max_cuts in every run) | 20/20 / 20/20 |
| max_support_calls = 40n | 0 / 0 (support calls 0.448-0.505 of the cap) | 0 / 0 (0.475-0.525 of the cap) |
| max_rounds = 10 | 0 / 0 (6-8 callbacks per run) | 0 / 0 (7-8 callbacks per run) |
| time budget = min(60 s, 0.5 x limit) = 60 s | 0 / 0 (callback 2.749-31.03 s root, 2.84-33.51 s full) | 0 / 0 (3.011-32.96 s root, 2.955-35.78 s full) |

`max_cuts_per_round` is 4n and `max_blocks` is n in every run (`max_blocks`, `max_separation_seconds`
60 and `separation_budget_fraction` 0.5 checked by a one-off read of the 80 cut-mode records). `separation.budget_exhausted` is true in
all 80 cut-mode runs. In `integration.py` (`RowSeparator._expired`), the cut cap also sets this flag.
Discovery completed in every run.

Time decomposition. Pairs are runs completed (root) or solved (full) by both the mode and baseline.
The ratio is the median per-run SCIP time excluding the callback, divided by baseline's SCIP time.
Sources: P(d), "time decomposition against baseline"; the SGMs equal V `by_mode.<m>.time_decomposition`
(root) and VR (full, common runs).

| Phase | Mode (pairs) | SGM total | SGM SCIP excl. callback | SGM callback | Baseline SGM total / SCIP | Median SCIP-excl / baseline SCIP | Median total / baseline |
|---|---|---:|---:|---:|---|---:|---:|
| root | frozen-wide (20) | 10.49 | 0.864 | 9.654 | 1.078 / 1.007 | 0.884 | 10.76 |
| root | rowdir-wide (20) | 10.65 | 0.6581 | 10.02 | 1.078 / 1.007 | 0.626 | 10.44 |
| root | baseline-extra (20) | 1.213 | 1.143 (SCIP) | 0 | 1.078 / 1.007 | 1.119 | 1.129 |
| full | frozen-wide (10) | 5.126 | 0.774 | 4.325 | 2.496 / 2.444 | 0.321 | 3.514 |
| full | rowdir-wide (10) | 4.905 | 0.4177 | 4.468 | 2.496 / 2.444 | 0.2025 | 3.248 |
| full | baseline-extra (10) | 1.900 | 1.852 (SCIP) | 0 | 2.496 / 2.444 | 0.729 | 0.735 |

Sums over the 20 runs per mode (V `time_decomposition`; P(d)):

| Phase, mode | Charged | SCIP | SCIP excl. callback | Callback | Discovery | Candidate LPs | Certification | Rows | Callback not covered by these four timers |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| root frozen-wide | 283.1 | 281.3 | 19.4 | 261.9 (92.5% of charged) | 10.2 | 36.5 | 129.6 | 1.5 | 84.1 |
| root rowdir-wide | 291.2 | 289.4 | 14.5 | 274.8 (94.4%) | 10.7 | 36.6 | 137.7 | 1.4 | 88.4 |
| full frozen-wide | 430.3 | 428.4 | 162.8 | 265.6 (61.7%) | 10.6 | 37.1 | 131.6 | 1.5 | 84.8 |
| full rowdir-wide | 424.7 | 422.7 | 144.7 | 278.1 (65.5%) | 10.8 | 37.5 | 139.0 | 1.5 | 89.3 |

The last column is the callback minus discovery, candidate LPs, certification and rows. The records do
not split it further.

- As in C2 and C3, most of the cut modes' time is the separator callback. SCIP's own time falls with
  the cuts: median ratio 0.884 and 0.626 at the root, 0.321 and 0.2025 in full runs. The total time is
  higher than baseline's on the instances both solve (n10, n20). Only the cut modes solve all n40 and
  n80 instances (baseline-extra solves 3 of these 10; baseline and Gurobi solve none).
- Host load (V `by_mode.<m>.load_start_mean`): root 8.13-8.19, full 7.86-9.10. The C4 runs ran from
  20:59:57Z to 21:32:14Z (record `started_utc`, `ended_utc`). This overlaps the other parts' replays
  (21:03-21:24Z, `evidence/campaign4-replay.md`).

## (e) Reference values

Source: REF (per instance: `coupling`, `optimum`, `optimum_exact`, `bound_ii`,
`optimum_minus_bound_ii`, `optimum_certificate`, `y_exact`, `multiplier_exact`); summarized by P(e) and
by the CR reference table.

- **Optimum minus bound (ii)**: min 2.77e-61, median 2.90e-60, max 6.47e-4 (n20_s8).
  - On 13 instances it is zero up to the bisection error (below 2.4e-59): n10_s5, s6, s8; n20_s5, s9;
    n40_s5-s9; n80_s5, s6, s8. On these, REF `bound_ii.fractional_copies` = 0 and the float bound (ii)
    equals the float optimum. (REF stores `optimum - lower_exact`, the exact bisection lower bound, so
    the stored difference is about 1e-60 rather than 0.)
  - It is positive on 7 instances, each with `fractional_copies` = 1: n10_s7 1.53e-5, n10_s9 6.10e-5,
    n20_s6 2.71e-5, n20_s7 1.53e-4, n20_s8 6.47e-4, n80_s7 2.69e-4, n80_s9 6.02e-5.
- **Coupling constant** c = floor(64 * 0.5 * sum_i y_i*) / 64 (REF `coupling.c`). Values range from
  87/64 (n10_s6) to 1001/64 (n80_s5); for example n10_s5 has c = 123/64 against sum y* = 495/128, and
  n80_s5 has 1001/64 against 4005/128. c / sum y* lies in [0.4957, 0.5].
- **The coupling row binds at the optimum** on 20/20 instances:
  - REF `coupling.binds` is true (c < sum y*).
  - The exact optimal y (`y_exact`) sums to exactly c (rational check in P(e)).
  - The multiplier of the coupling row in bound (ii) is positive: `multiplier_exact` from 29/288
    (0.1007, n10_s8) to 99/256 (0.3867, n10_s6).
- **Certificates**: `optimum_certificate.certified` true and `witness_primal_check.passed` true on 20/20.
  `assignment_switches_after_gurobi` is 0 on 20/20 (one-off read of REF). Every run record's
  `reference_witness_check` passed (P(checks)).

## (f) What the cut directions were

Method (P(f); the docstring of `campaign4_c4_digest.py` gives the details):
- Each cut record has the support direction `coefficients` = (a_x, a_y, a_z, lambda) over the block
  features (x_i, y_i, z_i, and the nonlinear part of row i). It also has the source side
  `signed_sides[0].affine_terms` in exact rationals: aff(x_i, y_i, z_i) - t_i + nl <= rhs.
- Direction classes:
  - "row": a = lambda * aff on the block variables, the exact support of the whole row (rowdir only);
  - "remainder": a = 0, the frozen remainder-only direction;
  - "LP": any other direction, from `propose_direction`, the LP direction search.
- The exported row (`row_certificate.exact.coefficients`) has y_i coefficient exactly a_y - lambda
  aff_y. This holds on 12,000/12,000 cuts per mode and phase. So a cut "uses a direction other than the
  row direction in y_i" exactly when its exported y_i coefficient is nonzero.
- The partial slope of a cut in y_i is -coef(y_i) / coef(t_i), with x_i and z_i held fixed. coef(t_i)
  is positive on every cut.
- No exported row has a nonzero coefficient outside its own block.

Counts per mode (root and full runs are identical; 12,000 cuts per mode and phase):

| Mode | Class | Cuts | y_i coef. nonzero | Nonzero pattern in (x_i, y_i, z_i) | Partial y-slope: median [q1, q3]; min, max; negative / positive / zero |
|---|---|---:|---:|---|---|
| frozen-wide | LP | 11,986 | 11,955 | xyz 11,951; xz 31; yz 3; xy 1; y only 0 | -0.3125 [-0.5312, -0.0625]; -5.858, 2.281; 9,449 / 2,506 / 31 |
| frozen-wide | remainder | 14 | 14 | xyz 14 | -1.578 [-1.797, -1.344]; -2.031, -1.062; 14 / 0 / 0 |
| frozen-wide | row | 0 | - | - | - |
| rowdir-wide | LP | 11,236 | 11,205 | xyz 11,201; xz 31; yz 4; y only 0 | -0.2734 [-0.5312, -0.09375]; -5.888, 1.875; 9,285 / 1,920 / 31 |
| rowdir-wide | remainder | 14 | 14 | xyz 14 | -1.578 [-1.797, -1.344]; -2.031, -1.062; 14 / 0 / 0 |
| rowdir-wide | row | 750 | 0 | none (cut on t_i only: t_i >= min D_i) | 0 for all 750 |

Totals with a nonzero y_i coefficient: frozen-wide 11,969 of 12,000 (99.7%), rowdir-wide 11,219 of
12,000 (93.5%).

- **The LP direction search produced the sloped cuts.** In every run, every block received LP-direction
  cuts. Per run there were 16n cuts on n blocks: frozen-wide 1,278-1,279 LP cuts out of 1,280 at n=80,
  rowdir-wide 1,198-1,199 (P(f), per-run lists). 79% (frozen-wide) and 83% (rowdir-wide) of the LP cuts
  have a negative partial slope in y_i. That is the sign of the supporting lines of conv(phi_i) when
  the coupling row pushes y_i below its own minimizer. For comparison, bound (ii) has multiplier mu in
  [0.1007, 0.3867] (REF), so its supporting slopes are -mu in [-0.387, -0.101]. The median LP slopes
  (-0.31, -0.27) lie in this range. This comparison is only indicative, because the LP cuts also
  involve x_i and z_i.
- **No cut is a pure (y_i, t_i) slope cut.** Of the LP cuts, 99.7% have nonzero x_i, y_i and z_i
  coefficients. The search finds sloped cuts in the full block space, not the projected envelope cuts
  t_i >= alpha + beta y_i that define bound (ii). With 16 cuts per block on average, the root bounds
  stayed 1.1e-5 to 0.029 below bound (ii) (rowdir-wide) when the cut cap stopped the separator.
- **The row direction is of little use here.** rowdir-wide added exactly one row-direction cut per block
  (750 = 5 x (10 + 20 + 40 + 80)); later rounds skip repeated directions. These cuts give at most
  sum_i min phi_i. That is the optimum of the C3 instance with the same triples
  (`runs/partC3/cases/*.json` `known_optimum`; in C3 the coupling row does not bind). Measured against
  the C4 optimum, this bound closes median 0.0243 [-5.70, 0.693] of the baseline root gap. It is below
  the baseline root bound on 10 of 20 instances (P(f)). Every frozen-wide and rowdir-wide root bound is
  above it (asserted in P(f)). rowdir-wide's advantage over frozen-wide (median gap closed 0.986 vs 0.953)
  is therefore not the row cuts' own bound. Under the same 16n cap, rowdir-wide has 750 row cuts in
  place of 750 LP cuts, and its LP cuts follow a different sequence. The gain comes from how the row
  cuts combine with the LP cuts, or from that different sequence; the records do not separate the two.
- For comparison, in C3 (non-binding coupling) rowdir-wide closed the full root gap on 20/20 instances
  and solved 20/20 within 33.2 s (`evidence/campaign4-digest.md`, Part C3). In C4 it closes 0.974-0.9997
  of the gap and solves 20/20 within 133.7 s.

## (g) Surprises and other observations

1. **Nothing missing, nothing failed** (P(checks); C `missing_runs`, `by_mode.<m>.failures`):
   - 180 of 180 records, one per scheduled run; return code 0 everywhere; no `worker_status`;
   - no root run hit its time limit (max 34.48 s); no worker was killed (max outer wall 302.3 s against
     the 360 s hard limit);
   - no primal-check failure (max scaled violation 9.97e-7); no flagged run; all reference-witness
     checks passed;
   - no `classifier_errors`; `cut_log_complete` true and recorded cuts = `separation.cuts` in every
     cut-mode run; no certification failure and no rounding rejection.
2. **The cut cap is the binding limit in all 80 cut-mode runs.** The support-call cap, the round cap
   and the time budget were never reached (see (d)). Every root run of a cut mode therefore ended below
   bound (ii). A larger cut cap might close more of the gap; this was not tested.
3. **Root-run and full-run root bounds differ, though the cut lists are identical** (see (b)). The
   root-phase runs (node limit 1) are the root measure used in this digest and in C.
4. **SCIP root-node bounds above bound (ii) occur only in full runs** (6 runs, all below the
   optimum; see (b)).
5. **Four full runs have no finite `root_dual` although they used more than one node**: frozen-wide
   n20_s5 (optimal, 7 nodes), rowdir-wide n20_s7 (optimal, 3), baseline n10_s6 (optimal, 2) and
   baseline-extra n10_s7 (optimal, 79) (P(checks)). No metric here uses full-run root bounds except the
   observation in (b).
6. **Gurobi bounds above the exact optimum** on all five n10 runs, by 1.11e-9 to 3.3e-8 (see (c)).
   Gurobi solved only n10 and n20_s9. It is fastest where it solves (SGM 0.1429 s on the common 6), but
   it timed out on n20_s5-s8, which baseline solved in 3.95-14.1 s (CR full table).
7. **The summarize_v4 output (VR) contains path-family lines that do not apply to C4.** These are the
   pair-hull bound 0 and the "closure of the residual gap" root/opt, which use the C2/C3 definitions
   (Theorem 6.2). Its root gap closed against the optimum equals C's. Use C/CR for C4.
8. **Soft-budget overshoots**: all 31 time-limit runs were charged more than 300 s, by at most 0.198 s.
   They are listed under `soft_budget_overshoots` (baseline 10, baseline-extra 7, gurobi 14; C full).
9. **Native separators** (VR): in baseline-extra, intersection cuts were active in all 20 root runs
   (27,288 enforcement calls, 12,692 cuts) and all 20 full runs (83,316,305 calls, 12,940 cuts). eccuts,
   interminor and minor made no productive call in any C4 mode.
10. **Records are consistent with the protocol.** Every cut-mode run has max_cuts = 16n,
    max_support_calls = 40n, max_cuts_per_round = 4n, max_rounds 10, and row_directions false
    (frozen-wide) or true (rowdir-wide) (P(d)). The case references equal REF (P(checks)).
