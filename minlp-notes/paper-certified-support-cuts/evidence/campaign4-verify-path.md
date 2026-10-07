# Independent check of the campaign-4 digest: Parts C2, C3 and the 2x2 design (2026-10-03)

Scope: the path-family numbers in `evidence/campaign4-digest.md` (Parts C2, C3, the 2x2
direction x limits design, the C2/C3 Gurobi runs, and the C2/C3 rows of the time-decomposition,
funnel, native-separator, replay and "Surprises" sections). Part C4 was not opened, listed or used.

## Result

**766 digest numbers recomputed from the raw records; 766 match, 0 numeric mismatches.**
One source attribution is imprecise (minor, below). Several facts that matter for the 2x2
attribution are missing from the digest (below).

## Method and commands (targeted, local; no project-wide tests, no CI)

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
PY=/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python
$PY verification/R8_path.py --json /tmp/r8.json          # prints the digest comparison (about 65 s)
$PY verification/R8_path.py --values                     # also prints every recomputed value
```

Besides the script, I ran only read-only `python3` inspections of the same records, of
`runs/*/replay.json`, of `experiments/v4/results/summary.json` (to check the digest's "S"
attributions) and of `evidence/funnel-and-time.md`, and `nproc`. I started no solver and
changed no file under `experiments/`.

`verification/R8_path.py` uses only the standard library. It reads `records.jsonl`, `jobs.json` and
`cases/*.json` of `experiments/v4/runs/partC2`, `partC3`, `experiments/v3/runs/partC` and
`experiments/v3d/runs/partC-rowdir`. It imports no producer code. I implemented the definitions
myself from the protocol and the runner README:

- solved: `status` optimal or gaplimit, `returncode` 0, no `worker_status`, `primal_check.checked`
  and `primal_check.passed` true;
- time: `total_seconds + preparation_seconds`; SCIP time `scip_solve_seconds` (Gurobi
  `solver_runtime_seconds`); callback `separation.callback_seconds`;
- SGM: exp(mean(log(t+1))) - 1 over the runs that every compared mode solved (full) or completed
  with a root bound (root);
- bound comparison: better or worse beyond `rtol * max(1, |a|, |b|)`;
- root bound: `root_dual`, or `dual` if the run ended at the root (node limit 1 or at most one node)
  without a finite `root_dual`;
- optimum: `known_optimum` of the case file. I checked it against `known_optimum_exact`, and
  against `reference_check.value` in every record of the four directories (all equal).

Every number in the digest's C2/C3/2x2 scope is hard-coded in `run_checks()` exactly as printed.
The tolerance is half a unit in the last printed digit. For the printed closure "1", I used
5e-4, i.e. the value rounds to 1.000. I tested the comparison on deliberately wrong values, and
it rejected them.

## What was checked (all match)

Data integrity:
- C2 140/140 and C3 180/180 runs recorded, none missing (`jobs.json` vs `records.jsonl`).
- Status counts as in the digest. 0 failures. No missing cut log. 0 primal-check failures.
- C2 cases equal the v3 and v3d cases: same `model` and `known_optimum_exact` on all 20.
- C3 names are disjoint from C2.
- Replays passed (`runs/partC2/replay.json`: 24,000/24,000 cuts, `bound_runs` 120;
  `runs/partC3/replay.json`: 30,000/30,000, 160). All 14 tampering mutations were rejected
  for frozen-wide, all-diag-mech and rowdir-wide (`v4.tamper_controls_by_mode`).
  `config_failures` and `gurobi_failures` are empty.

C2 root (records `root_dual`/`dual`, cases `known_optimum`):
- All 7 x 5 gap-closed cells (median, min, max), including pair-hull and both v3d modes.
- All 7 x 4 residual-closure cells and all 7 x 4 root-bound cells.
- All 20 root runs are nodelimit for novarlocks, extra, frozen-wide and c3:all-diag-mech.
- Each of these modes is better than c3:baseline on 20/20 at rtol 1e-4 and 1e-6.
- v3d baseline root = c3 baseline root, bit-identical on 20/20.
- novarlocks root bounds lie in [-0.009947, -0.0009158], none above 0.
- frozen-wide is above 0 on exactly n10_s0, n10_s4, n20_s2, n20_s3, n20_s4, n80_s1 and n80_s4.
- frozen-wide is at its 16n cut cap in 20/20 root runs (`separation.cuts` = `config.max_cuts`).

C2 full:
- Solved counts and instance lists for all six modes, and median nodes over all 20 runs.
- The 7-instance common set. SGM and median nodes per mode over it.
- Median time ratios vs c3:baseline (pairs, faster counts).
- The 9-pair SGMs (10.270 / 6.661 / 4.817 / 6.531 / 5.166) and Gurobi 6.321 vs 5.597.
- Final-dual counts at 1e-4, with the worse lists (n40_s1; n20_s3, n20_s4).
- Mean `load_start[0]`: c3:baseline 15.98 (digest 16.0); C2 modes 6.485-6.901.

2x2:
- Configs of the four cells differ only in `max_cuts` (4n vs 16n), `max_cuts_per_round`
  (n vs 4n) and `max_support_calls` (20n vs 40n), plus the direction code. All have
  `max_blocks` n, `max_rounds` 10, `max_separation_seconds` 60, SCIP 10.0.2, 120 s / node limit 1.
- v3d all-diag-mech solved 10 (n10_s0-s4, n20_s0-s4); v3d wide solved 20.
- 12/20 v3d wide root runs ended optimal at the root.
- v3d mean load: 18.0 (full), 14.4 (root).

C2 Gurobi:
- Every cell of the Gurobi table: status, `gurobi_status_name`, bound minus optimum, `mip_gap`,
  time, nodes, and the n40/n80 ranges.
- 20/20 incumbents passed. Max scaled violation 9.78e-7.
- 9 incumbents are below the optimum; the largest shortfall is 1.14e-5 (n20_s4).
- The bound is above the optimum only on n10_s2 (+3.35e-7).
- Gurobi's n40/n80 bound is below both baseline-novarlocks and frozen-wide on each of the 10
  instances, and above c3:baseline.

C3:
- Root: all gap-closed cells and residual-closure cells. Better than baseline 20/20 at both
  tolerances. rowdir-wide root minus optimum lies in [-2.0e-7, +7.1e-13]. The 8
  optimal-at-root runs are exactly the 8 runs without `root_dual`.
- Full: solved counts and lists, median nodes (rowdir-wide max 38), the 5-instance common set,
  SGM, SGM of SCIP time excluding the callback, nodes, ratios, and the 9-pair SGMs.
  rowdir-wide over all 20: SGM 10.19 s, times 3.17-33.17 s, n80 31.7-33.2 s, callback
  268.6 s of 279.7 s charged. Final-dual counts with worse lists (n40_s8; n20_s5, s7, s8, s9).
- Gurobi: every C3 statement, including bounds above the optimum on n10_s7, s8 and s9, the
  relative excess 1.95e-4, and the incumbent shortfall 1.55e-5 on n20_s6 (violation 1.13e-6).

Other sections, path rows only:
- All 8 path rows of the time-decomposition table (pairs and 7 values each). The baseline-extra
  ratios 1.196 / 1.262 and the novarlocks ratios 0.229 / 0.384.
- The 4 path funnel rows: callbacks, support calls, failures, below threshold, binding
  rejections (runs), causes, cuts, and caps. Root and full funnels are identical in sums and
  per run.
- novarlocks `minor` separator: 661 / 34,061 / 17,039 in 20 runs. Root SGM 0.341 vs 1.099.
- baseline-extra intersection cuts (`nlhdlrs.quadratic` `#Enforce`/`Cuts`): 29,210 / 14,907
  (C2) and 31,490 / 14,875 (C3), 20 runs each. RLT: 200 calls, 0 cuts. interminor and eccuts: 0.
- Surprise 2: the 10 novarlocks solves are optimal with primal = dual, 1.84e-6 to 6.98e-6
  below the optimum, relative up to 3.8e-4 (n10_s1). They are worse than c3:baseline at 1e-6
  on all 9 common instances.
- Time-limit runs: 40 (C2), 47 (C3). 0 root time limits, 0 certification failures,
  0 rounding rejections, 0 `classifier_errors`.

## Imprecision found (not a wrong number)

1. **Soft-budget overshoot attribution (minor).** Surprise 10 says the summarizer lists
   "C2 40 runs" under `soft_budget_overshoots`. 40 is the correct count of C2's own time-limit
   runs. But `results/summary.json` partC2 `mechanism/full` also lists 11 for `c3:baseline` and
   11 for `c3:all-diag-mech` (`by_mode.<m>.soft_budget_overshoots`), so the S total for that
   phase is 62. Also, the C2/C3 time-limit runs were charged 300.19-300.24 s; the 300.36 s
   maximum belongs to D full.

## Facts missing from the digest (within C2/C3 and the 2x2)

1. **The 2x2 cells ran at different host loads, and the digest does not say this for the
   frozen-wide cell.** Mean `load_start[0]` in the full runs: c3:all-diag-mech 15.96 (campaign 3),
   v3d cells 17.9-18.0, frozen-wide 6.65 (campaign 4). The root gap-closed part of the 2x2 is
   not affected: every run of all four cells stopped at its cut cap, with no support-call cap,
   callback cap or 60 s budget hit, and the v3 and v3d baseline root bounds are bit-identical.
   The solved counts depend on time.
   - frozen-wide's four solves that c3:all-diag-mech lacks took 8.9 s (n20_s0), 26.2 s
     (n40_s0), 38.4 s (n40_s4) and 167.5 s (n40_s2). Only n40_s2 is within a factor of 2 of
     the 300 s limit.
   - On the same 9 solved instances, v3d baseline (load 18.0) against c3:baseline (load 16.0)
     gave per-run time ratios of 0.92-1.07 (median 1.016), with SGM 10.277 vs 10.270 s.
   - `nproc` reports 36 on this host.
   So "9 -> 13 (limits)" is probably robust, but the digest should state the load difference.
2. **No times for the v3d cells.** On the C2 instances, v3d all-diag-mech-wide solved all 20
   in at most 38.6 s with at most 6 nodes. On the 9 instances that v3d baseline solved, v3d
   baseline had SGM 10.277 s, v3d all-diag-mech 2.556 s (median ratio 0.514, 6 of 9 faster) and
   v3d all-diag-mech-wide 4.752 s (median ratio 1.402, 4 of 9 faster).
3. **The "directions alone" solved-count gain is one instance:** n20_s0, which v3d
   all-diag-mech solved in 9.5 s and c3:all-diag-mech did not solve in 300 s. v3d baseline
   solved the same 9 as c3:baseline.
4. **The closure "1" is approximate.** v3d wide gap closed ranges from 0.99999932 to
   1.0000000000004, and its root bound minus the optimum from -4.0e-7 to +7.1e-13. The digest
   gives the second range only for C3 rowdir-wide.
5. **List of the 12 v3d wide root runs that ended optimal** (the digest gives only the count):
   n10_s0-s4, n20_s0-s3, n40_s0, n40_s1 and n80_s0. None of them has a `root_dual`, so the
   final dual bound is used.
6. **Gurobi at rtol 1e-6 (C2):** worse than c3:baseline on 7 instances (n10_s0, n10_s3, n10_s4
   and n20_s1-s4), because gap-limit bounds stop 2e-6 to 1e-5 below the optimum. The digest
   reports only 1e-4.
7. **The campaign-3 and v3d Part C replays passed**: `v3/runs/partC/replay.json` 6,000/6,000
   cuts and `v3d/runs/partC-rowdir/replay.json` 30,000/30,000. The 2x2 cells rely on these, but
   the digest cites replays only for the campaign-4 parts.
8. **Load caveat in the time-decomposition section:** the frozen-wide rows (root 1.19, full
   0.144 median SCIP-excl./reference ratio) compare a load-6.6 run with c3:baseline at load
   16.0-16.4. The caveat is given elsewhere in the digest but not next to these ratios.
