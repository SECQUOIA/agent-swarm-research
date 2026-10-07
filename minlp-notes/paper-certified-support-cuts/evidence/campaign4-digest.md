# Campaign 4 digest: parts C2, C3, B2 and D (written 2026-10-03)

This digest collects the campaign-4 numbers the paper needs, for the five
finished parts. Part C4 was still running; this digest does not read, replay
or summarize it. Timings are descriptive: the host was shared, with up to six
single-threaded workers. Bounds are SCIP's or Gurobi's numerical bounds; only
the recorded cuts are certified, and only where the replay passed.

## Commands run (targeted, local; no project-wide tests, no CI)

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
PY=/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python
cd /workspace/minlp-notes/paper-certified-support-cuts/experiments/v4
$PY summarize_v4.py runs/partC2=../v3/runs/partC runs/partC3 runs/partB2=../v3/runs/partB \
    runs/partD-root runs/partD-full --dest results          # rerun after all five replays
$PY summarize_v4.py ../v3/runs/partA-full ../v3/runs/partA-root ../v3/runs/partB ../v3/runs/partC \
    ../v3d/runs/partA-root-rowdir ../v3d/runs/partB-root-rowdir ../v3d/runs/partC-rowdir --dest results-c3
cd ../../verification
for p in C2 C3 B2 D caps; do $PY campaign4_digest.py $p; done
```

The reference syntax `DIR=REFDIR` worked for C2 and B2: 0 case mismatches
against `v3/runs/partC` and `v3/runs/partB`. The replays (`replay_v4.py`, which
writes `runs/<part>/replay.json`) were started at 17:03 by another session,
in parallel, one process per part. All five passed (17:04-17:24). The
summaries in `results/` were then regenerated; only the replay lines changed.
This session had also started a replay of partC2; it was stopped before it
wrote anything, so it did not duplicate the other session's work. No SCIP or
Gurobi solve was started. No record, case, snapshot or code under
`experiments/` was changed. New files: `experiments/v4/results/`,
`experiments/v4/results-c3/` (summarizer output),
`verification/campaign4_digest.py` (read-only analysis) and this file. Part C4:
no file in `runs/partC4` was opened. This session did list that directory once,
and read the last 3 lines of `runs/launch-c4.log`. Neither was used here.

## Sources and abbreviations

- **S** = `experiments/v4/results/summary.json`; **R** = `experiments/v4/results/results.md`.
  Paths are written as `S partC2 mechanism/root by_mode.frozen-wide.funnel.cuts`,
  meaning `parts[i]` with `part == "partC2"`, then `phases["mechanism/root"]`.
  Parts in S: partC2, partC3, partB2, partD-root, partD-full.
- **S3**, **R3** = the same files in `experiments/v4/results-c3/` (campaign 3 and v3d).
- **V:x** = output of `verification/campaign4_digest.py x`. It is computed from
  `runs/<part>/records.jsonl` and `cases/` with the definitions of
  `summarize_v4.py`, which it imports unchanged.
- Record fields: root bound = `root_dual`, or `dual` for a run that ended at the
  root without a finite `root_dual`. Solved = `status` optimal or gaplimit, plus
  `primal_check.passed` true. Time = `total_seconds + preparation_seconds`.
  SCIP time = `scip_solve_seconds` (Gurobi: `solver_runtime_seconds`).
  Callback = `separation.callback_seconds`.
- Gap closed = (root(m) - root(ref)) / (target - root(ref)). Residual closure =
  root(m) / opt; this is the closure of the gap between the pair-hull bound 0
  and the optimum. Pair-hull closure of the baseline gap = (0 - root(base)) /
  (opt - root(base)). Ranges are written as median [min, max] over the 5
  instances of each n.
- n80, n40_s1 and so on abbreviate `interleaved_path_n80_s*` and
  `interleaved_path_n40_s1`. In C2 and C3 the names are those of the case files.

## Run status and replay

| Part | Scheduled / recorded | Statuses | Failures | Replay (`runs/<part>/replay.json`) |
|---|---|---|---|---|
| C2 | 140 / 140 | optimal 35, gaplimit 5, nodelimit 60, timelimit 40 | 0 | passed; 24,000/24,000 cuts; 120 bound runs (20 Gurobi records omitted as designed); config failures 0; Gurobi failures 0; tampering rejected for frozen-wide |
| C3 | 180 / 180 | optimal 58, gaplimit 3, nodelimit 72, timelimit 47 | 0 | passed; 30,000/30,000 cuts; 160 bound runs (20 Gurobi records omitted as designed); config failures 0; Gurobi failures 0; tampering rejected for all-diag-mech, rowdir-wide |
| B2 | 150 / 150 | optimal 37, gaplimit 6, nodelimit 107 | 0 | passed; 1,007/1,007 cuts; config failures 0; tampering rejected for all-noaggr, all-diag-noaggr, all-diag-rowdir-noaggr |
| D root | 100 / 100 | nodelimit 95, timelimit 5 | 0 | passed; 1,736/1,736 cuts; config failures 0; tampering rejected for all, all-diag, all-diag-rowdir |
| D full | 80 / 80 | optimal 4, gaplimit 3, timelimit 73 | 0 | passed; 28/28 cuts; config failures 0; tampering rejected for all, auto |

Sources: S `scheduled_runs`, `recorded_runs`, `missing_runs` (empty in every part), `status_counts`, `replay`;
`runs/replay-<part>.log`. Every record has `returncode` 0 and no `worker_status`, and no cut log is missing
(S `by_mode.*.missing_cut_logs`).

## Part C2: the 20 campaign-3 path instances (n in {10, 20, 40, 80}, 5 seeds each)

Baseline and all-diag-mech come from campaign 3 (`c3:` modes, `v3/runs/partC`).
The v3d baseline root bounds equal the campaign-3 baseline root bounds on all
20 instances, and the v3d cases equal the C2 cases (V:C2). So v3d gap closure
can be measured against the same reference.

### (a) Root runs (node limit 1, 120 s)

All 20 root runs of every C2 mode and of c3:all-diag-mech ended with status
nodelimit; none was solved at the root. In every mode the root bound is better
than c3:baseline on 20/20 instances at both rtol 1e-4 and 1e-6
(S partC2 mechanism/root `bounds`).

Root gap closed relative to c3:baseline, median [min, max] (V:C2; the medians
equal S partC2 mechanism/root `root_gap_closed_median`):

| Mode | n=10 | n=20 | n=40 | n=80 | all 20 |
|---|---|---|---|---|---|
| baseline-novarlocks | 0.948 [0.813, 0.957] | 0.886 [0.861, 0.925] | 0.931 [0.901, 0.938] | 0.911 [0.884, 0.926] | 0.910 [0.813, 0.957] |
| baseline-extra | 0.640 [0.495, 0.733] | 0.580 [0.499, 0.633] | 0.659 [0.590, 0.693] | 0.591 [0.514, 0.639] | 0.610 [0.495, 0.733] |
| frozen-wide | 0.863 [0.783, 0.950] | 0.874 [0.842, 0.933] | 0.887 [0.859, 0.918] | 0.898 [0.850, 0.930] | 0.884 [0.783, 0.950] |
| c3:all-diag-mech | 0.350 [0.0808, 0.432] | 0.250 [0.0801, 0.327] | 0.191 [0.148, 0.330] | 0.224 [0.170, 0.332] | 0.260 [0.0801, 0.432] |
| pair-hull bound 0 | 0.952 [0.816, 0.960] | 0.890 [0.866, 0.928] | 0.935 [0.906, 0.942] | 0.916 [0.889, 0.930] | 0.914 [0.816, 0.960] |
| v3d all-diag-mech (row directions, mechanism limits) | 0.442 [0.255, 0.756] | 0.438 [0.354, 0.477] | 0.433 [0.364, 0.464] | 0.458 [0.371, 0.516] | 0.440 [0.255, 0.756] |
| v3d all-diag-mech-wide (row directions, wide limits) | 1 [1, 1] | 1 [1, 1] | 1 [1, 1] | 1 [1, 1] | 1 |

Closure of the residual gap, root/opt (pair-hull bound 0 gives 0, the optimum gives 1), median [min, max] (V:C2;
c3:baseline from the bracketed values in R, C2 root table):

| Mode | n=10 | n=20 | n=40 | n=80 |
|---|---|---|---|---|
| c3:baseline | -19.8 [-24.0, -4.45] | -8.09 [-12.8, -6.48] | -14.4 [-16.2, -9.68] | -10.9 [-13.2, -8.01] |
| baseline-novarlocks | -0.0739 [-0.0872, -0.0207] | -0.0385 [-0.0708, -0.0330] | -0.0571 [-0.0665, -0.0511] | -0.0537 [-0.0728, -0.0419] |
| baseline-extra | -5.17 [-8.02, -1.75] | -3.31 [-4.15, -2.14] | -4.15 [-4.75, -3.35] | -4.14 [-5.43, -2.30] |
| frozen-wide | -0.142 [-4.42, 0.405] | 0.0533 [-0.366, 0.0680] | -0.413 [-1.17, -0.210] | -0.449 [-1.09, 0.198] |
| c3:all-diag-mech | -12.5 [-16.9, -2.41] | -5.82 [-11.7, -4.03] | -10.5 [-12.1, -7.68] | -8.52 [-9.79, -6.21] |
| v3d all-diag-mech | -5.11 [-14.9, -1.45] | -4.56 [-7.69, -2.91] | -8.21 [-8.77, -4.97] | -5.43 [-6.97, -4.58] |
| v3d all-diag-mech-wide | 1 | 1 | 1 | 1 |

Root bounds, median [min, max] (V:C2). The optimum per instance is `known_optimum` in `runs/partC2/cases/`:

| Mode | n=10 | n=20 | n=40 | n=80 |
|---|---|---|---|---|
| c3:baseline | -0.2523 [-0.3413, -0.2362] | -0.5796 [-0.6480, -0.2612] | -1.226 [-1.417, -0.9454] | -1.818 [-2.383, -1.749] |
| baseline-novarlocks | -0.001101 [-0.001272, -0.0009158] | -0.002365 [-0.002569, -0.002083] | -0.005075 [-0.005375, -0.004611] | -0.009679 [-0.009947, -0.009509] |
| baseline-extra | -0.08864 [-0.09952, -0.06748] | -0.1676 [-0.2590, -0.1137] | -0.3349 [-0.4161, -0.3229] | -0.7445 [-0.7993, -0.5212] |
| frozen-wide | -0.00185 [-0.04645, 0.02153] | 0.003288 [-0.02625, 0.003585] | -0.03615 [-0.1042, -0.02056] | -0.0761 [-0.1485, 0.04272] |
| c3:all-diag-mech | -0.1775 [-0.2158, -0.1201] | -0.4171 [-0.5663, -0.1960] | -0.8743 [-1.073, -0.7480] | -1.424 [-1.533, -1.338] |
| v3d all-diag-mech | -0.1624 [-0.1944, -0.05364] | -0.2942 [-0.3718, -0.1565] | -0.6610 [-0.7784, -0.4855] | -0.9861 [-1.128, -0.8750] |
| v3d all-diag-mech-wide | 0.01721 [0.0105, 0.0531] | 0.06103 [0.0343, 0.07166] | 0.08875 [0.07776, 0.09766] | 0.1799 [0.1366, 0.2269] |

- baseline-novarlocks stays just below the pair-hull bound on every instance: root bounds from -0.009947 to -0.0009158,
  none above 0. Its median gap closed (0.910) is close to the pair-hull closure (0.914).
- frozen-wide is above the pair-hull bound 0 on 7 of 20 instances: n10_s0, n10_s4, n20_s2, n20_s3, n20_s4, n80_s1
  and n80_s4 (V:C2 per-instance list; R C2 root table).
- frozen-wide reached its cut cap of 16n cuts in 20/20 root runs (V:caps).

### (b) Full runs (300 s)

| Mode | Solved / 20 | Instances solved | Median nodes, all 20 runs |
|---|---:|---|---:|
| c3:baseline | 9 | n10_s0-s4, n20_s1-s4 | 58,222.5 |
| c3:all-diag-mech | 9 | n10_s0-s4, n20_s1-s4 | 58,105 |
| baseline-novarlocks | 10 | n10_s0-s4, n20_s0-s4 | 35,332 |
| baseline-extra | 10 | n10_s0-s4, n20_s0-s4 | 88,485 |
| frozen-wide | 13 | n10_s0-s4, n20_s0-s4, n40_s0, n40_s2, n40_s4 | 8,346 |
| gurobi | 7 (gaplimit 5, optimal 2) | n10_s0-s4, n20_s1, n20_s2 | 247,157.5 |

Sources: S partC2 mechanism/full `by_mode.<m>.solved`; instance lists and node medians from V:C2 (record fields
`status`, `primal_check`, `nodes`).

Times and nodes over the 7 instances solved by all six modes (n10_s0-s4, n20_s1, n20_s2)
(S partC2 mechanism/full `times.pooled.sgm`; nodes from V:C2):

| Mode | SGM time (s) | Median nodes | Median per-run time ratio vs c3:baseline (pairs; faster) |
|---|---:|---:|---|
| c3:baseline | 5.597 | 1,521 | - |
| c3:all-diag-mech | 3.727 | 400 | 0.773 (9; 6) |
| baseline-novarlocks | 2.709 | 879 | 0.384 (9; 8) |
| baseline-extra | 4.030 | 722 | 0.482 (9; 7) |
| frozen-wide | 4.623 | 52 | 1.171 (9; 4) |
| gurobi | 6.321 | 346 | 0.256 (7; 4) |

The ratio column is S `times.ratio_summary`; it uses all pairs that both the mode and c3:baseline solved. On the
9 instances solved by both a mode and c3:baseline, the SGM against c3:baseline's 10.270 s is: c3:all-diag-mech
6.661, novarlocks 4.817, extra 6.531, frozen-wide 5.166. Gurobi: 6.321 against 5.597 on its 7 (V:C2).

Final dual bound against c3:baseline at rtol 1e-4 (S partC2 mechanism/full `bounds["0.0001"]`; V:C2):
c3:all-diag-mech better 10, tie 9, worse 1 (n40_s1). novarlocks, extra and frozen-wide: better 11, tie 9 each.
gurobi better 11, tie 7, worse 2 (n20_s3, n20_s4; c3:baseline solved both).

Timing caveat: the campaign-3 runs started at a mean load of 16.0, the C2 runs at 6.49-6.90 (S partC2
mechanism/full `by_mode.<m>.load_start_mean`). Time comparisons between c3: modes and C2 modes are therefore
confounded by host load.

### (c) The 2x2 design: direction rule x limits

| Directions \ limits | Mechanism limits (n blocks, 4n cuts, n per callback, 20n support calls) | Wide limits (16n cuts, 4n per callback, 40n support calls) |
|---|---|---|
| Frozen (remainder-only) | c3:all-diag-mech. Root gap closed (median per n): n10 0.350, n20 0.250, n40 0.191, n80 0.224. Solved 9/20. | frozen-wide (C2). Root gap closed: 0.863, 0.874, 0.887, 0.898. Solved 13/20. |
| Row directions | v3d all-diag-mech. Root gap closed: 0.442, 0.438, 0.433, 0.458. Solved 10/20 (n10_s0-s4, n20_s0-s4). | v3d all-diag-mech-wide. Root gap closed: 1, 1, 1, 1 (all 20 instances). Solved 20/20; 12/20 of its root runs solved at the root node. |

Sources: V:C2 (same definitions as summarize_v4); the v3d cells match R3 (v3d partC, mechanism/root medians
0.442 / 0.438 / 0.433 / 0.458 and 1 / 1 / 1 / 1; mechanism/full solved 10 and 20). The gap is closed relative to
c3:baseline, which equals the v3d baseline root bound on every instance. The v3d runs are a post hoc diagnostic
with its own date and load (mean load 18.0 full, 14.4 root; R3).

Reading: wide limits alone take the frozen directions from 0.19-0.35 to 0.86-0.90 (medians per n). Row
directions alone take them to 0.43-0.46. Both together close the gap completely. Solved counts: 9 -> 13
(limits), 9 -> 10 (directions), 9 -> 20 (both).

### (d) Gurobi (C2, 300 s, one thread, MIPGap 1e-4, NonConvex 2)

Source: V:C2. Record fields: `status`, `gurobi_status_name`, `primal`, `dual`, `mip_gap`, `nodes`, `primal_check`.

| Group | Status | Final bound vs optimum | `mip_gap` | Time (s) / nodes |
|---|---|---|---|---|
| n10_s1, n10_s2 | optimal (OPTIMAL) | n10_s1 -7.6e-9; n10_s2 **+3.35e-7** (bound above the exact optimum) | 0 | 0.33, 0.35 / 346, 343 |
| n10_s3, n20_s2 | gaplimit (OPTIMAL) | -2.2e-6, -2.7e-6 | 9.5e-5, 7.5e-5 | 0.29, 0.49 / 322, 334 |
| n10_s0, n10_s4, n20_s1 | gaplimit (OPTIMAL) | -9.4e-6, -1.0e-5, -4.1e-6 | 1.0e-4, 1.0e-4, 5.75e-5 | 45.6, 77.6, 88.7 / 289,663, 488,091, 204,652 |
| n20_s0, n20_s3, n20_s4 | timelimit | -6.27e-4, -3.11e-4, -1.83e-4 | 0.00863, 0.00452, 0.00354 | 300.2 / 799,843-871,276 |
| n40_s0-s4 | timelimit | -0.0593 to -0.0687 (bounds 0.0150-0.0384) | 0.609-0.810 | 300.2 / 329,645-347,162 |
| n80_s0-s4 | timelimit | -0.155 to -0.240 (bounds -0.0211 to -0.0033) | 1.01-1.13 | 300.2 / 175,928-186,544 |

All 20 Gurobi incumbents passed the original-model check, with max scaled violation up to 9.8e-7. On 9 instances
the incumbent objective is below the exact optimum, by up to 1.14e-5 (n20_s4): the incumbents are slightly
infeasible within Gurobi's tolerances. At 300 s Gurobi's bound on n40 and n80 is better than c3:baseline's but
worse than baseline-novarlocks' (n40 0.040-0.056, n80 0.031-0.049) and frozen-wide's (R C2 full table).

## Part C3: 20 fresh path instances (seeds 5-9), prospective test

### (a) Root runs

Root gap closed relative to baseline, median [min, max] (V:C3; medians = S partC3 mechanism/root
`root_gap_closed_median`):

| Mode | n=10 | n=20 | n=40 | n=80 | all 20 |
|---|---|---|---|---|---|
| baseline-extra | 0.572 [0.488, 0.732] | 0.640 [0.539, 0.671] | 0.611 [0.423, 0.652] | 0.660 [0.574, 0.679] | 0.617 [0.423, 0.732] |
| all-diag-mech | 0.323 [0.0151, 0.456] | 0.310 [0.0958, 0.374] | 0.238 [0.117, 0.312] | 0.205 [0.158, 0.295] | 0.232 [0.0151, 0.456] |
| rowdir-wide | 1 [1, 1] | 1 [1, 1] | 1 [1, 1] | 1 [1, 1] | 1 |
| pair-hull bound 0 | 0.927 [0.821, 0.969] | 0.922 [0.878, 0.947] | 0.928 [0.894, 0.947] | 0.923 [0.893, 0.931] | 0.925 [0.821, 0.969] |

Residual closure root/opt, median [min, max] (V:C3; baseline from R C3 root table):

| Mode | n=10 | n=20 | n=40 | n=80 |
|---|---|---|---|---|
| baseline | -12.6 [-31.2, -4.57] | -11.8 [-18.0, -7.22] | -13.0 [-17.8, -8.47] | -12.0 [-13.4, -8.30] |
| baseline-extra | -4.84 [-15.5, -1.34] | -3.52 [-5.38, -2.79] | -5.01 [-5.56, -2.58] | -3.30 [-3.78, -2.96] |
| all-diag-mech | -7.77 [-30.7, -2.03] | -10.5 [-12.1, -4.15] | -8.61 [-13.3, -6.33] | -8.55 [-10.4, -6.40] |
| rowdir-wide | 1 | 1 | 1 | 1 |

Each mode's root bound is better than baseline's on 20/20 instances, at both tolerances (S partC3
mechanism/root `bounds`). The rowdir-wide root bound minus the optimum lies between -2.0e-7 and +7.1e-13 on
every instance. 8 of its 20 root runs ended optimal at the root node: n10_s5, s6, s8, s9 and n20_s5, s7, s8, s9.
SCIP then reports no `root_dual`, so the final dual bound is used. The other modes all ended with status
nodelimit (V:C3).

### (b) Full runs (300 s)

| Mode | Solved / 20 | Instances solved | Median nodes, all 20 |
|---|---:|---|---:|
| baseline | 9 | n10_s5-s9, n20_s5, s7, s8, s9 | 71,276.5 |
| all-diag-mech | 10 | n10_s5-s9, n20_s5-s9 | 81,185.5 |
| rowdir-wide | 20 | all | 1 (max 38) |
| baseline-extra | 9 | n10_s5-s9, n20_s5, s7, s8, s9 | 94,019.5 |
| gurobi | 5 (optimal 2, gaplimit 3) | n10_s5-s9 | 258,452.5 |

Over the 5 instances solved by all five modes (n10_s5-s9) (S partC3 mechanism/full `times.pooled`; nodes from
V:C3):

| Mode | SGM time (s) | SGM SCIP excl. callback (s) | Median nodes | Median per-run ratio vs baseline (pairs; faster) |
|---|---:|---:|---:|---|
| baseline | 1.698 | 1.656 (SCIP) | 1,443 | - |
| all-diag-mech | 2.104 | 1.202 | 628 | 0.858 (9; 5) |
| rowdir-wide | 3.284 | 0.1238 | 1 | 0.860 (9; 5) |
| baseline-extra | 1.061 | 1.026 (SCIP) | 559 | 0.627 (9; 6) |
| gurobi | 0.334 | 0.330 (Gurobi) | 358 | 0.235 (5; 5) |

On the 9 instances solved by both a mode and baseline, the SGM against baseline's 9.379 s is: all-diag-mech 7.267,
rowdir-wide 4.434, baseline-extra 7.067 (V:C3). rowdir-wide over all 20 runs: SGM 10.19 s; times 3.17-33.17 s
(n80 31.7-33.2 s); the callback is 268.6 s of the 279.7 s charged (S partC3 mechanism/full
`by_mode.rowdir-wide.time_decomposition`; V:C3).

Final dual bound against baseline at rtol 1e-4 (S partC3 mechanism/full `bounds`; V:C3): all-diag-mech and
rowdir-wide better 11, tie 9. baseline-extra better 10, tie 9, worse 1 (n40_s8). gurobi better 11, tie 5,
worse 4 (n20_s5, s7, s8, s9).

Gurobi in C3 (V:C3): n10 optimal (n10_s7, s8) or gaplimit (n10_s5, s6, s9) in 0.25-0.43 s. All n20 instances
hit the time limit with `mip_gap` 6.0e-4 to 0.0152 and bounds 4.4e-5 to 6.7e-4 below the optimum. n40:
`mip_gap` 0.534-0.848. n80: `mip_gap` 1.04-1.21, with negative bounds. The bound is above the exact optimum on
n10_s7 (+1.07e-6), n10_s8 (+1.16e-6) and n10_s9 (+2.43e-7). The incumbents are up to 1.55e-5 below the
optimum (n20_s6, max scaled violation 1.1e-6); all passed the 1e-5 check.

### (c) Did the post hoc finding replicate?

Yes, prospectively, on the 20 fresh instances. With row directions and wide limits (rowdir-wide), the root gap
closed is 1 on 20/20 instances, and the full runs solved 20/20 within 33.2 s with at most 38 nodes. On the same
instances baseline solved 9, all-diag-mech 10, baseline-extra 9 and Gurobi 5. This matches the v3d result on the
campaign-3 instances: gap closed 1 on 20/20 and 20/20 solved (R3 v3d partC). The frozen directions at mechanism
limits again closed only part of the root gap: medians 0.205-0.323 per n, against 0.191-0.350 in campaign 3.

## Part B2: the 30 campaign-3 Part B models, root only (60 s), no aggregation

### (a) Stored-row (row-binding) rejections and cuts

| Mode | Support calls | Cert. failures | Below threshold | Binding rej. (runs) | Causes | Cuts | Share of violated rows rejected |
|---|---:|---:|---:|---|---|---:|---:|
| c3:all | 436 | 7 | 316 | 23 (9) | not recorded in v3 records; evidence reruns: 18 presolve, 5 SCIP | 90 | 23/113 = 20.4% |
| all-noaggr | 446 | 7 | 326 | 6 (5) | coefficient_rounded_to_integer 4, column_set_differs_tiny_coefficient_dropped 1, column_set_differs_variable_not_column 1 (status FIXED) | 107 | 6/113 = 5.3% |
| c3:all-diag | 1,618 | 19 | 1,039 | 202 (17) | evidence reruns: 171 presolve (157 aggregated, 14 fixed), 31 SCIP | 358 | 202/560 = 36.1% |
| all-diag-noaggr | 1,572 | 17 | 1,058 | 47 (13) | rounded_to_integer 17, tiny_coefficient_dropped 16, variable_not_column 14 (variable statuses FIXED 17) | 450 | 47/497 = 9.5% |
| all-diag-rowdir-noaggr | 1,640 | 19 | 1,124 | 47 (13) | same as all-diag-noaggr | 450 | 47/497 = 9.5% |

Sources: S partB2 structure/root `by_mode.<m>.funnel` (fields `certification_calls`, `certification_failures`,
`below_violation_threshold`, `row_binding_rejections`, `runs_with_binding_rejections`,
`row_binding_rejection_causes`, `rejected_row_variable_statuses`, `cuts`). The campaign-3 causes come from
`evidence/funnel-and-time.md` (reruns in `verification/funnel_repro.jsonl`). Share = binding / (binding + cuts).

- Disabling aggregation removed most rejections but not all: 23 -> 6 (all) and 202 -> 47 (all-diag).
  Presolve-caused rejections fell from 18 to 1 (all) and from 171 to 14 (all-diag). The rejections that remain
  are SCIP's own coefficient handling (integer snaps, dropped coefficients with |c| <= 1e-9: 5 in all, 33 in
  all-diag) plus fixed variables (1 and 14). `donotaggr`/`donotmultaggr` do not stop presolve from fixing
  variables.
- Per model (V:B2; binding/cuts for c3:all-diag -> all-diag-noaggr): kall_circlespolygons_c1p12 127/25 -> 0/104;
  pooling_adhya4tp 17/29 -> 17/29 (14 fixed-variable, 3 integer snaps); bayes2_50 17/8 -> 12/8 (all dropped tiny
  coefficients); bayes2_30 3/0 -> 3/0 (tiny); pooling_rt2tp 4/46 -> 4/46 (integer snaps).
- Certification failures by outcome are not recorded in the v4 records (only the count). They occur on ex8_1_7
  (7 in all-noaggr; 9 in all-diag-noaggr; 11 in rowdir) and tanksize (8 in all-diag-noaggr and rowdir), the same
  models as in campaign 3 (c3:all ex8_1_7 7; c3:all-diag tanksize 10, ex8_1_7 9) (V:B2 per-model counts).
- Caps (V:caps): all-noaggr hit the 24 support-call cap in 8 runs, the 10-callback cap in 10, and the 1 s time
  budget in 9 (inferred); 4 runs hit none. all-diag-noaggr and all-diag-rowdir-noaggr hit the 10-callback cap in
  13 runs and nothing in 17.

### (b) Root bounds of the cut modes against baseline-noaggr

Source: S partB2 structure/root `bounds`; values and gap closed (against MINLPLib `reference_primal`) from V:B2.

- all-noaggr, rtol 1e-4: better 3, tie 27, worse 0. The 3: sep1 -523.8205 vs -524.4654 (gap closed 0.0448);
  ex3_1_4 -5.78975 vs -6 (0.105); pointpack04 1.151211 vs 1.164013 (0.0781). At rtol 1e-6: better 4 (adds
  ex8_1_7, -5910.599 vs -5910.615, 2.8e-6), worse 1 (prob06, 1.177099 vs 1.177121).
- all-diag-noaggr, rtol 1e-4: better 6, tie 23, worse 1. Better: pooling_bental4tp -462.7154 vs -497.3265
  (0.731); sep1 -522.8298 (0.114); ex3_1_4 -5.692308 (0.154); tanksize 0.8430595 vs 0.8424252 (0.00149);
  pooling_bental4pq -450 vs -464.934 (1.0); pointpack04 1.10903 (0.335). Worse: pooling_haverly1tp -422.2222 vs
  -414.4928 (-0.533). At rtol 1e-6, prob06 is also worse.
- all-diag-rowdir-noaggr: identical bounds to all-diag-noaggr on every model, at both tolerances.
- For comparison, campaign 3 against c3:baseline at 1e-4: c3:all better 3 (pooling_bental4tp, ex3_1_4,
  pointpack04); c3:all-diag better 4 (pooling_bental4tp, ex3_1_4, pooling_bental4pq, pointpack04); neither worse.
- Median root gap closed over the 29 models with a reference is 0 for every mode (S partB2 structure/root
  `root_gap_closed_median`). The 104 cuts now added on kall_circlespolygons_c1p12 left its root bound at 0
  (target 0.3396).

### (c) Effect of the SCIP settings themselves

- baseline-noaggr vs c3:baseline, rtol 1e-4 (same at 1e-6): worse 6, tie 24, better 0. The 6: pooling_bental4tp
  -497.3265 vs -450.2443; sep1 -524.4654 vs -522.7499; pooling_haverly2pq -857.1429 vs -617.7001; tanksize
  0.8424252 vs 0.8432474; pooling_haverly3tp -875 vs -750.7937; pooling_haverly1tp -414.4928 vs -400. Solved at
  the root: 7 vs 8 (pooling_haverly1tp lost). Disabling aggregation weakens SCIP's own root bound.
- baseline-extra vs c3:baseline, rtol 1e-4 (same at 1e-6): better 12, tie 17, worse 1. Better, with gap closed:
  pooling_bental4tp -450 (1.0), wastewater04m2 80.17429 vs 71.96239 (0.459), pooling_haverly2pq -600 (1.0),
  ex3_1_4 -4 (1.0), pooling_adhya4tp -881.9363 vs -976.4387 (0.957), tanksize 0.8473479 (0.00964),
  kall_congruentcircles_c32 0.104981 vs 0 (0.0763), ex8_1_7 -5837.857 vs -5910.615 (0.0123), pooling_bental4pq
  -450 (1.0), pooling_haverly3tp -750 (1.0), pooling_rt2tp -4933.627 vs -5528.253 (0.523), pointpack04 1.006909
  (0.958). Worse: sep1 -533.7662 vs -522.7499 (-0.87). Solved at the root: 13 vs 8.
- Sources: S partB2 structure/root `bounds`, `by_mode.<m>.solved`; V:B2.

### (d) Native separators in baseline-extra

From S partB2 structure/root `by_mode.baseline-extra.native_separators` (record field `native_statistics`).
Counts are runs with a productive call / calls / cuts found / applied:

- interminor: 21 runs / 939 / 429,680 / 1,985
- intersection cuts (quadratic nonlinear handler): 26 runs / 24,141 enforcement calls / 6,829 cuts
- RLT: 27 / 229 / 208 / 9
- minor: 4 / 145 / 320 / 110
- eccuts: 0 (no productive call)

baseline-noaggr for contrast: interminor 0, intersection 0, minor 4 / 54 / 71 / 36, RLT 27 / 164 / 129 / 5.
In the path family, baseline-extra's only productive extra separator was intersection cuts: 20 runs; root
29,210 calls / 14,907 cuts in C2 and 31,490 / 14,875 in C3. interminor and eccuts were 0, and RLT made 200
calls with 0 cuts (S partC2/partC3 mechanism/root `native_separators`).

## Part D: 20 larger hard MINLPLib models

### (a) Root runs (node limit 1, 120 s)

Source: S partD-root larger/root (`by_mode`, `bounds["0.0001"]`, `root_gap_closed_median`); V:D for lists and
values. The target is MINLPLib `reference_primal`; mpbp_31 has none, so the gap is taken over 19 models.

| Mode | Models with cuts | Cuts | Better / tie / worse at 1e-4 | Root gap closed over 19: median [min, max] |
|---|---:|---:|---|---|
| all | 2 (kall_ellipsoids_tc02b 11, kriging_peaks-full100 3) | 14 | 0 / 19 / 1 (kriging_peaks-full100 -335.418 vs -334.346) | 0 [-0.00323, 0] |
| all-diag | 13 | 891 | 1 / 14 / 5 | 0 [-0.0306, 0.0389] |
| all-diag-rowdir | 13 | 831 | 1 / 14 / 5 (same models as all-diag) | 0 [-0.0306, 0.0389] |
| baseline-extra | - | 0 | 8 / 8 / 3, plus 1 flagged | 0 [-0.243, 0.344] (the -0.243 is the flagged waternd2 run) |

- all-diag better: multiplants_mtg1c 8573.751 vs 8893.211 (gap closed 0.0389, 4 cuts). all-diag worse:
  multiplants_mtg1a 1823.402 vs 1780.952 (-0.0306, 4 cuts); hydroenergy2 379795.09 vs 379602.42 (-0.0247, 133
  cuts; rowdir 379704.95, -0.0132, 73 cuts); kriging_peaks-full100 (-0.00323, 3 cuts); crudeoil_li03 3577.653 vs
  3577.182 (-0.00523, 31 cuts); blend718 20.69113 vs 20.68767 (-0.00026, 1 cut). At 1e-6, multiplants_mtg6 is
  also worse (6870.1466 vs 6870.1214).
- all-diag cut counts per model: kall_ellipsoids_tc05a 200, kall_ellipsoids_tc02b 200, kall_circlespolygons_c1p5b
  143, hydroenergy2 133, pooling_sppa0stp 54, pooling_sppa0pq 42, multiplants_mtg6 40, kall_circlesrectangles_c6r1
  36, crudeoil_li03 31, multiplants_mtg1a 4, multiplants_mtg1c 4, kriging_peaks-full100 3, blend718 1.
- baseline-extra better (gap closed): blend480 10.67717 vs 10.79625 (0.0759); pooling_sppa0stp -37232.28 vs
  -37479.54 (0.148); camshape100 -4.771519 vs -5.027017 (0.344); kriging_peaks-full100 -279.8305 vs -334.3456
  (0.164); multiplants_mtg1c 8647.275 (0.0300); blend718 20.66851 (0.00144); pooling_sppa0pq -37288.49 vs
  -37780.20 (0.250); multiplants_mtg6 6869.284 (0.000538). Worse: multiplants_mtg1a 1798.335 (-0.0125),
  hydroenergy2 379704.87 (-0.0132), crudeoil_li03 3577.861 (-0.00754). Flagged: waternd2 (see Surprises).

Funnel and separator time (sums over the 20 runs; S partD-root `by_mode.<m>.funnel` and
`time_decomposition`; caps from V:caps):

| Mode | Callbacks | Support calls | Cert. failures | Below threshold | Binding rej. (runs) | Cuts | Callback / discovery / candidate LPs / certification (s) |
|---|---:|---:|---:|---:|---|---:|---|
| all | 22 | 176 | 2 (kriging_peaks-full100) | 149 | 11 (3): variable_not_column 11 (multiplants_mtg1c 3, blend718 5, kall_circlesrectangles_c6r1 3) | 14 | 18.4 / 15.7 / 0.4 / 1.8 |
| all-diag | 115 | 6,352 | 313 (kriging_peaks-full100 307, kall_ellipsoids_tc05a 3, kall_ellipsoids_tc02b 3) | 5,042 | 106 (8): variable_not_column 99, rounded_to_integer 7 (statuses FIXED 109, AGGREGATED 85) | 891 | 188.4 / 53.6 / 22.8 / 69.8 |
| all-diag-rowdir | 107 | 6,378 | 313 (same models) | 5,128 | 106 (8): same | 831 | 190.8 / 53.1 / 20.8 / 73.1 |

- Mode all stopped in discovery on 12 of 20 models because of the 1 s budget (`separation.discovery_incomplete`):
  blend480, kall_ellipsoids_tc05a, pooling_sppa0stp, ringpack_20_2, mpbp_31, hydroenergy2, pooling_sppa0pq,
  kall_circlespolygons_c1p5b, sonet23v4, ringpack_20_1, crudeoil_li03 and multiplants_mtg6. These are exactly the
  12 models whose scan discovery took more than 1 s (1.01-7.70 s; `scanD/records.jsonl` field
  `discovery_seconds`). On each of them the callback used 1.0 s and made no support call (V:D).
- Other caps in mode all (V:caps): time budget in 14 runs (12 of them in discovery), support-call cap (24) in 6,
  10-callback cap in 1. all-diag: cut cap (200) in 2, support-call cap (500) in 8, 10 callbacks in 8, time budget
  (30 s) in 0, none in 2. all-diag-rowdir: cut cap 2, support cap 9, 10 callbacks 7, none 2.
- Of the 8 models where discovery completed in mode all, 2 received cuts; the other 6 received none after 21-24
  support calls.

### (b) Full runs (300 s)

| Mode | Solved / 20 | Solved models | Final dual vs baseline, 1e-4: better / tie / worse |
|---|---:|---|---|
| baseline | 2 | blend480 (optimal), kriging_peaks-full100 (gaplimit) | - |
| all | 2 | same | 5 / 14 / 1 |
| auto | 2 | same | 4 / 16 / 0 |
| baseline-extra | 1 | blend480 | 7 / 6 / 7 |

Sources: S partD-full larger/full `by_mode.<m>.solved`, `bounds["0.0001"]`; V:D.

- all better: camshape100 -4.573527 vs -4.574352; multiplants_mtg1c 6586.358 vs 6602.980; blend718 10.39616 vs
  10.56384; sonet23v4 -39618.46 vs -39633.63; crudeoil_li03 3560.264 vs 3560.880. all worse: multiplants_mtg1a
  859.0551 vs 856.8424. auto better: multiplants_mtg1a 852.1695, multiplants_mtg1c 6586.358, blend718 10.35299,
  sonet23v4 -39618.46.
- **These differences are not cut effects.** In the full runs, all and auto added cuts only on
  kall_ellipsoids_tc02b (11) and kriging_peaks-full100 (3). Both tie with baseline at 1e-4. All the 1e-4
  differences above are on models that received no cuts. They reflect run-to-run variation from the presence of
  the separator under a time limit (V:D).
- baseline-extra better: pooling_sppa0stp, camshape100, hydroenergy2, blend718, pooling_sppa0pq, sonet23v4,
  crudeoil_li03. Worse: multiplants_mtg1a, mpbp_31, waternd2, kriging_peaks-full100 (no longer solved),
  multiplants_mtg1c, kall_circlesrectangles_c6r1 (0 vs 0.7848), multiplants_mtg6.
- SGM over commonly solved runs: only blend480 is solved by all four modes. baseline 63.36 s, all 63.70 (SCIP
  excl. callback 62.28, callback 1.0), auto 62.62 (61.14, 1.0), baseline-extra 49.54 (S partD-full larger/full
  `times.pooled`). Over all 20 runs (mostly at the 300 s limit): baseline 275.8 s, all 276.4 (SCIP excl.
  callback 274.3), auto 276.2 (274.1), extra 274.5; summed callback 18.8 s in each of all and auto (V:D).
- In the full runs, discovery stopped in 11 of 20 runs of all and of auto: the same models as at the root
  except multiplants_mtg6 (scan 1.31 s), which completed discovery in the full runs (V:D).

## Time decomposition (is the slowdown separator overhead?)

Common pairs: runs completed (root) or solved (full) by both the mode and its reference. The ratio is the median
per-run SCIP time excluding the callback, divided by the reference's SCIP time (V:<part>; SGMs also in S
`times.pooled` for the all-mode common sets).

| Part, phase | Mode (pairs) | SGM total | SGM SCIP excl. callback | SGM callback | Reference: SGM total / SCIP | Median SCIP-excl / ref SCIP | Median total / ref |
|---|---|---:|---:|---:|---|---:|---:|
| C2 root | c3:all-diag-mech (20) | 4.077 | 1.198 | 2.913 | c3:baseline 1.099 / 1.022 | 1.18 | 3.99 |
| C2 root | frozen-wide (20) | 10.06 | 1.161 | 8.956 | c3:baseline 1.099 / 1.022 | 1.19 | 9.49 |
| C2 full | c3:all-diag-mech (9) | 6.661 | 4.692 | 1.249 | c3:baseline 10.27 / 10.17 | 0.395 | 0.773 |
| C2 full | frozen-wide (9) | 5.166 | 1.247 | 3.828 | c3:baseline 10.27 / 10.17 | 0.144 | 1.171 |
| C3 root | all-diag-mech (20) | 3.795 | 1.140 | 2.698 | baseline 1.062 / 0.990 | 1.21 | 3.94 |
| C3 root | rowdir-wide (20) | 10.25 | 0.391 | 9.863 | baseline 1.062 / 0.990 | 0.330 | 10.99 |
| C3 full | all-diag-mech (9) | 7.267 | 5.605 | 1.152 | baseline 9.379 / 9.284 | 0.783 | 0.858 |
| C3 full | rowdir-wide (9) | 4.434 | 0.1405 | 4.252 | baseline 9.379 / 9.284 | 0.0369 | 0.860 |
| B2 root | all-noaggr (30) | 0.6493 | 0.1461 | 0.4772 | baseline-noaggr 0.1949 / 0.1511 | 0.997 | 3.91 |
| B2 root | all-diag-noaggr (30) | 1.184 | 0.1494 | 1.023 | baseline-noaggr 0.1949 / 0.1511 | 1.005 | 7.28 |
| B2 root | all-diag-rowdir-noaggr (30) | 1.240 | 0.1465 | 1.082 | baseline-noaggr 0.1949 / 0.1511 | 0.958 | 7.51 |
| D root | all (20) | 11.09 | 9.084 | 0.911 | baseline 10.07 / 9.22 | 0.995 | 1.106 |
| D root | all-diag (20) | 17.76 | 8.572 | 6.838 | baseline 10.07 / 9.22 | 0.996 | 2.134 |
| D root | all-diag-rowdir (20) | 17.92 | 8.614 | 6.940 | baseline 10.07 / 9.22 | 0.987 | 2.161 |
| D full | all (1: blend480) | 63.70 | 62.28 | 1.0 | baseline 63.36 / 62.91 | 0.990 | 1.005 |
| D full | auto (1: blend480) | 62.62 | 61.14 | 1.0 | baseline 63.36 / 62.91 | 0.972 | 0.988 |

- On the MINLPLib samples (B2, D), SCIP's own time excluding the callback is unchanged by the cut modes (median
  ratios 0.958-1.005). The slowdown in total time is the separator callback.
- On the path family, the cuts change SCIP's own time. At the root, the frozen-direction modes raise it by about
  20% (median 1.18 c3:all-diag-mech, 1.19 frozen-wide, 1.21 C3 all-diag-mech), while rowdir-wide lowers it
  (0.330). In full runs SCIP's own time falls sharply (0.0369-0.783). Most of the remaining total time with wide
  limits is callback.
- Non-cut comparators (same tables): baseline-extra raises SCIP's root time (median total ratio 1.196 C2, 1.262
  C3, 1.289 B2 vs c3:baseline, 1.396 D). baseline-novarlocks lowers it in C2 (0.229 at the root, 0.384 in full
  runs), subject to the load caveat above (S `times.ratio_summary`).

## Funnel per part and cut mode

Sums over runs. Certified = support calls - certification failures. Below threshold = certified - rounding -
binding - cuts. Rounding rejections were 0 in every part and mode. Certification failures by outcome are not
recorded in the v4 records. Source: S `<part> <phase> by_mode.<m>.funnel`; caps from V:caps. "Time budget" is
inferred as `budget_exhausted` without the cut or support-call cap; `budget_exhausted` itself is set by any of
time, support-call cap or cut cap (`integration.py`, `_expired`).

| Part, phase | Mode | Runs | Callbacks | Support calls | Cert. fail. | Below thr. | Binding rej. (runs): causes | Cuts | Runs hitting: cut cap / support cap / 10 callbacks / time budget (discovery stopped) |
|---|---|---:|---:|---:|---:|---:|---|---:|---|
| C2 root = full | frozen-wide | 20 | 122 | 13,502 | 0 | 1,189 | 313 (20): tiny_coefficient_dropped 313 | 12,000 | 20 / 0 / 0 / 0 (0) |
| C2 (c3) root = full | c3:all-diag-mech | 20 | 80 | 3,462 | 0 | 391 | 71 (13): not recorded (evidence reruns: all tiny coefficients) | 3,000 | 20 / 0 / 0 / 0 (0) |
| C3 root = full | all-diag-mech | 20 | 80 | 3,558 | 0 | 474 | 84 (16): tiny_coefficient_dropped 84 | 3,000 | 20 / 0 / 0 / 0 (0) |
| C3 root = full | rowdir-wide | 20 | 140 | 15,534 | 0 | 3,181 | 353 (20): tiny_coefficient_dropped 353 | 12,000 | 20 / 0 / 0 / 0 (0) |
| B2 root | all-noaggr | 30 | 52 | 446 | 7 | 326 | 6 (5): rounded 4, tiny 1, variable_not_column 1 | 107 | 0 / 8 / 10 / 9 (0) |
| B2 root | all-diag-noaggr | 30 | 210 | 1,572 | 17 | 1,058 | 47 (13): rounded 17, tiny 16, variable_not_column 14 | 450 | 0 / 0 / 13 / 0 (0) |
| B2 root | all-diag-rowdir-noaggr | 30 | 210 | 1,640 | 19 | 1,124 | 47 (13): same | 450 | 0 / 0 / 13 / 0 (0) |
| D root | all | 20 | 22 | 176 | 2 | 149 | 11 (3): variable_not_column 11 | 14 | 0 / 6 / 1 / 14 (12) |
| D root | all-diag | 20 | 115 | 6,352 | 313 | 5,042 | 106 (8): variable_not_column 99, rounded 7 | 891 | 2 / 8 / 8 / 0 (0) |
| D root | all-diag-rowdir | 20 | 107 | 6,378 | 313 | 5,128 | 106 (8): same | 831 | 2 / 9 / 7 / 0 (0) |
| D full | all | 20 | 22 | 180 | 2 | 153 | 11 (3): variable_not_column 11 | 14 | 0 / 6 / 1 / 14 (11) |
| D full | auto | 20 | 24 | 170 | 0 | 145 | 11 (3): variable_not_column 11 | 14 | 0 / 4 / 2 / 15 (11) |

For the path family, the root and full funnels are identical in every counter, because the separator runs only
at depth 0. Only the callback seconds differ. Every C2 and C3 cut-mode run reached its cut cap, and none
reached the support-call cap.

## Cross-check of the campaign-3 funnel and times (`results-c3` against `evidence/funnel-and-time.md`)

`summarize_v4.py` over the seven campaign-3 and v3d directories (R3) reproduces every funnel number in the
evidence file's appendix table for the C3 and v3d sets: support calls, certified, failed, insufficient
violation, rounding 0, row-binding rejections with run counts, and cuts added. Checked rows: C3 A full all/auto;
C3 A root all/auto/all-diag; C3 B full all/auto; C3 B root all/auto/all-diag; C3 C full/root; v3d A root
all/auto/all-diag; v3d B root all/auto/all-diag; v3d C full/root mech/wide. Example: C3 B full all 884 / 870 / 14
/ 646 / 0 / 45 (20) / 179 in both. The time SGMs also agree, for example C3 A full all 1.267 / 0.988 / 0.195;
C3 C full all-diag-mech 6.661 / 4.692 / 1.249; v3d C root all-diag-mech-wide 10.83 / 0.2995 / 10.50 in R3,
against 10.833 / 0.299 / 10.498 in the evidence. The only difference in content: R3 reports "not recorded" for
campaign-3 rejection causes and certification outcomes, which the evidence file obtained from reruns. Campaign 2
and the repair cohort are not campaign-3 directories and were not part of this run.

## Surprises and inconsistencies

1. **A native comparator nearly reaches the pair-hull bound.** In C2, baseline-novarlocks
   (`constraints/nonlinear/checkvarlocks = 'd'`) closes a median 0.910 of the root gap, against 0.914 for the
   pair-hull bound. Its root bounds lie 0.0009-0.0099 below 0. In all 20 of its root runs, SCIP's `minor`
   separator was productive (661 calls, 34,061 cuts found, 17,039 applied). It made no productive call in any
   other C2 or C3 mode; the campaign-3 records hold no native statistics (S partC2 mechanism/root
   `by_mode.<m>.native_separators`). Its root SGM time is 0.341 s, against 1.099 s for c3:baseline.
2. **baseline-novarlocks "optimal" values lie below the exact optimum.** All 10 solved runs report status
   optimal with primal = dual, 1.84e-6 to 6.98e-6 below the exact optimum (relative up to 3.8e-4, n10_s1). This
   is why its final bounds count as "worse" than c3:baseline at rtol 1e-6 on all 9 commonly solved instances
   (S partC2 mechanism/full `bounds["1e-06"]`). The incumbents passed the 1e-5 primal check.
3. **Gurobi bounds above the exact optimum.** C2 n10_s2 (+3.35e-7, status OPTIMAL), C3 n10_s7 (+1.07e-6), n10_s8
   (+1.16e-6) and n10_s9 (+2.43e-7). Relative excess up to 1.95e-4 (C3 n10_s7). Gurobi incumbents are up to
   1.55e-5 below the optimum (C3 n20_s6; scaled violation 1.1e-6). The reference check (absolute tolerance 1e-5)
   flagged none of these. Gurobi is fast on n = 10 (0.25-0.43 s in C3) but solved only 2/5 (C2) and 0/5 (C3) of
   the n = 20 instances in 300 s.
4. **Primal-check failure: D root, waternd2, baseline-extra.** The incumbent satisfies the constraints (max
   scaled violation 3.4e-11), but SCIP's reported primal 3,084,095.92 differs from the objective recomputed on the
   original model, 2,297,367.49 (`relative_objective_discrepancy` 0.342). The run is flagged and excluded from the
   bound comparison. However, the summarizer's root-gap table still lists its -0.243. No other primal check failed
   in any part.
5. **Five root runs hit the 120 s time limit (D root).** kall_ellipsoids_tc05a in baseline, all and
   baseline-extra; ringpack_20_2 in baseline-extra; kall_circlespolygons_c1p5b in baseline-extra. Charged time
   was up to 124.49 s (kall_circlespolygons_c1p5b, baseline-extra). The kall_ellipsoids_tc05a full runs
   (baseline, all, auto) also ended at node 1 after 300 s, without an incumbent. The path family and B2 had no
   root time-limit runs.
6. **Runs without an incumbent.** D root: blend480, kall_ellipsoids_tc05a and crudeoil_li03 in all five modes
   (15 runs). D full: kall_ellipsoids_tc05a in all four modes. B2: wastewater04m2 in all five modes (V:D, V:B2).
7. **Certified cuts worsened SCIP's root bound more often than they improved it in Part D**: all-diag 5 worse,
   1 better at 1e-4; mode all 1 worse (kriging_peaks-full100, 3 cuts). In B2, all-diag-noaggr worsened
   pooling_haverly1tp. These are SCIP's numerical root bounds after a changed separation path. They do not
   indicate invalid cuts; the replay passed.
8. **Part D full-run bound differences in modes all and auto occur only on models without cuts** (see D (b)).
9. **Row directions made no difference on the structure and larger models.** all-diag-rowdir-noaggr equals
   all-diag-noaggr on every B2 root bound and cut count (450), although the support-call counts differ (1,640
   vs 1,572). In D, all-diag-rowdir and all-diag have the same better/worse models; only the hydroenergy2 values
   and cut counts differ (73 vs 133 cuts).
10. **Soft-limit overshoots.** Every 300 s time-limit run was charged 300.19-300.36 s, which the summarizer
    lists under `soft_budget_overshoots` (C2 40 runs, C3 47, D full 73). The largest is 300.36 s
    (kriging_peaks-full100 baseline-extra, D full). No worker was killed (no `process_timeout`).
11. **Host load differs between the campaigns.** The c3: reference runs started at mean load about 16 (C2) and
    16.3 (B2), against 3.5-7.7 for the campaign-4 runs (S `by_mode.<m>.load_start_mean`). Time ratios against
    c3: modes are confounded by load.
12. **Nondeterminism at the 1 s discovery budget.** multiplants_mtg6 stopped in discovery in the D root run of
    mode all, but completed discovery in the D full runs of all and auto.
13. **Nothing missing.** Every scheduled run has one record. There are no worker errors, no missing cut logs,
    no rounding rejections, no `classifier_errors` in the rejection-cause records, and no certification
    failures in any path-family run.
