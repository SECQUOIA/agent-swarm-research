# Independent check of the campaign-4 digest: MINLPLib parts (B2, D root, D full)

Checked: `evidence/campaign4-digest.md` (written 2026-10-03), sections Run status (B2, D rows), Part B2,
Part D, the B2/D rows of the time-decomposition and funnel tables, and Surprises 4-13 as far as they
concern B2 and D. Reference: campaign-3 Part B root runs, `experiments/v3/runs/partB` (phase `root`, seed 0).

## Result

348 checks were run, and 338 match. None of the 10 mismatches changes a claim.

- **2 major.** Both are the same labelling error. The digest says "10-callback cap" for the frozen
  modes (B2 all-noaggr, D root all). These modes have a 3-callback cap. The run counts are correct.
- **8 minor.** Four last-digit rounding slips, one wrong reason for excluding a model, one median
  given as 0 that is 3.27e-12, and a pair definition in the D full time row (counted as two checks).

Every other number in scope matches the raw records. This includes run status, replay, funnels,
causes, bound comparisons at 1e-4 and 1e-6, gap closed, solved counts, SGMs, native-separator counts
and the discovery-budget analysis.

## Method and commands (targeted, local; no project-wide tests, no CI)

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
PY=/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python
cd /workspace/minlp-notes/paper-certified-support-cuts/verification
$PY R8_minlplib.py --json "$(mktemp /tmp/R8_minlplib_XXXXXX.json)" > "$(mktemp /tmp/R8_minlplib_XXXXXX.txt)"
```

- **The script.** `verification/R8_minlplib.py` uses the standard library only. It reads
  `records.jsonl`, `jobs.json`, `cases/*.json` and `replay.json` of `v4/runs/partB2`, `partD-root`
  and `partD-full`, plus `v3/runs/partB`, `v4/scanD/records.jsonl` and the two `instancedata.csv`
  files. It does not import `summarize_v4`, `summarize_v3`, `campaign4_digest` or any other producer
  code. The digest's values are coded into its `compare_with_digest()`, which prints each mismatch
  and the totals.
- **Definitions.** I implemented them from the protocol and the README:
  - solved: status optimal or gaplimit, normal worker exit, `primal_check.checked` and `.passed`
    true;
  - time: `total_seconds + preparation_seconds`;
  - SGM: shift 1 s;
  - bound comparison: tolerance `rtol*max(1,|a|,|b|)`, with the sign set by `sense`;
  - root bound: `root_dual`, else `dual` for a run that ended at the root.
- **Not done.** No SCIP or Gurobi solve was run, and no replay was run (`replay.json` was only
  read). Nothing under `experiments/` was changed, and `runs/partC4` was not opened.
- **Temp-file note.** My first output file, `/tmp/r8_out.txt`, was overwritten during the session
  by another process with Part C2 output. All results here come from reruns into `mktemp` files.
  Other checkers should not use fixed `/tmp` names.

## Where the gap-closed target comes from

`summarize_v4.py` (`gap_rows`) takes the target from the case field `reference_primal`.
`make_jobs.py` (`b2_cases`, `d_cases` → `osil_case`) fills that field from the `primalbound` column
of `v4/snapshot/code/minlp_solver_lab/instances/instancedata.csv`, which is MINLPLib's best known
primal bound.

- I checked the case values against that file and against the live
  `code/minlp_solver_lab/instances/instancedata.csv`. They are identical for all 30 B2 and 20 D
  models.
- mpbp_31 has an empty `primalbound`.
- The formula (root(m) - root(ref)) / (target - root(ref)) gives the same result for maximization.
  A gap exists only where sign*(target - root(ref)) > 0.
- Maximization models: pointpack02 and pointpack04 (B2); blend480, blend718, crudeoil_li03,
  hydroenergy2, mpbp_31, multiplants_mtg1a, mtg1c and mtg6 (D).

## Mismatches

| # | Item (digest location) | Digest | Recomputed | Reason | Severity |
|---|---|---|---|---|---|
| 1 | B2 (a) Caps bullet; funnel table row "B2 root, all-noaggr", column "10 callbacks" | "hit ... the 10-callback cap in 10" | Cap is **3** callbacks; 10 runs reached it | Real error (label). Frozen `Config.max_rounds = 3` (record field `config.max_rounds` = 3 in all 30 all-noaggr runs; snapshot `integration.py` line 47). 10 is the all-diag/mechanism value. `verification/campaign4_digest.py` line 455 hard-codes the label `round_cap(10 callbacks)` while it counts `separation.calls >= config.max_rounds`. | major |
| 2 | D (a) "Other caps in mode all"; funnel table rows "D root all", "D full all", "D full auto" | "10-callback cap in 1" (D full: 1 and 2) | Cap is **3** callbacks. D root: 1 run, kall_ellipsoids_tc02b with `separation.calls` = 3. D full: all 1, auto 2 (tc02b; tc02b and blend718). | Same label error as #1 (`config.max_rounds` = 3 in every D all/auto run). | major |
| 3 | B2 (b) last bullet | "Median root gap closed ... is 0 for every mode" | baseline-extra: **3.27e-12** (29 models); other modes exactly 0 | Rounding. S `partB2 structure/root root_gap_closed_median.baseline-extra` = 3.27e-12. | minor |
| 4 | B2 (b) last bullet | "over the 29 models with a reference" | All **30** B2 cases have `reference_primal`. 29 values exist because nvs02 has no gap. | Wrong reason. nvs02 is solved at the root in every mode. The c3:baseline `dual` 5.96418452307 (`root_dual` null) already meets the target 5.964184523 (case `reference_primal`), so sign*(target - base) <= 0 and the model is excluded. | minor |
| 5 | Surprise 11 | c3: B2 runs "mean load ... 16.3" | 16.35 (rounds to 16.4) | Rounding. Mean of `load_start[0]` over the 120 campaign-3 Part B root runs: c3:baseline 16.349, all 16.345, auto 16.36, all-diag 16.357. | minor |
| 6 | D (a) all-diag worse list | blend718 "20.69113" | 20.691125 (`root_dual` 20.69112470034694) | Last-digit rounding slip; the comparison and gap closed (-0.00026) are unaffected. | minor |
| 7 | D (a) baseline-extra better list | blend480 "10.67717" | 10.677165 (`root_dual` 10.677164773267798) | Last-digit rounding slip; gap closed 0.0759 is unaffected. | minor |
| 8 | D (b) all-worse bullet | multiplants_mtg1a baseline "856.8424" | 856.84235 (`dual` 856.8423490829866) | Last-digit rounding slip; outcome unaffected. | minor |
| 9-10 | Time-decomposition table, rows "D full, all (1: blend480)" and "D full, auto (1: blend480)" | 1 pair; median SCIP-excl/ref 0.990 (all), 0.972 (auto); median total/ref 1.005, 0.988 | The table header defines pairs as "solved ... by both the mode and its reference". That gives **2** pairs (blend480 and kriging_peaks-full100). all: median SCIP-excl/ref **1.012**, total/ref **1.021**, SGM total 131.0 vs 128.3. auto: **1.004**, **1.014**, SGM 130.1 vs 128.3. | Definition inconsistency. The row uses the all-four common set (blend480 only), not the stated pairwise set. The blend480-only values are correct. S `partD-full larger/full times.ratio_summary` has count 2, median 1.0212 (all) and 1.0142 (auto). kriging_peaks-full100: all 268.48 s, baseline 258.89 s. The claim "SCIP's own time is unchanged" still holds, but "median ratios 0.958-1.005" would become 0.958-1.012. | minor |

## Important facts missing from the digest (B2 and D)

1. **Row-binding share in Part D, default presolve.** In D root mode all, the stored-row check
   rejected 11 of the 25 violated certified rows (44%).
   - All 11 have cause `column_set_differs_variable_not_column` (rejected-row variable statuses
     FIXED 22, AGGREGATED 3).
   - They fall on 3 models (multiplants_mtg1c 3, blend718 5, kall_circlesrectangles_c6r1 3), and
     none of the 3 received a cut.
   - D root all-diag: 106/997 = 10.6%. all-diag-rowdir: 106/937 = 11.3%. D full all and auto:
     11/25 each.
   - The digest gives these shares for B2 only. The digest's funnel row for D root all lists no
     rejected-row statuses.
   - Sources: records `separation.row_binding_rejections`, `separation.cuts`,
     `row_binding_rejection_causes`.
2. **Why mode all added no cuts on 18 of 20 Part D models (root).**
   - 12 models: discovery stopped at the 1 s budget, with 0 support calls and 1.000-1.006 s of
     callback each. These are exactly the 12 models whose scan `discovery_seconds` exceeded 1 s
     (1.01-7.70 s).
   - 6 models completed discovery but got no cut:
     - camshape100, multiplants_mtg1a, waternd2, blend718 and kall_circlesrectangles_c6r1 reached
       the 24-support-call cap;
     - multiplants_mtg1c reached the 1 s budget after 21 calls;
     - on blend718, mtg1c and c6r1, every violated row was rejected by the stored-row check;
     - on the other three, every certified support was below the violation threshold.
   - D full: 18 of 20 models got no cut in all, and 18 in auto. In each mode, 11 runs stopped in
     discovery and 7 completed it without a cut. multiplants_mtg6 completed discovery but made only
     4 support calls (all) or 6 (auto) before the 1 s budget ran out.
   - The digest gives the 12 and the "other 6", but not the per-model causes or the D full
     breakdown.
3. **Gap closed is ill-conditioned when the reference root bound is at the target.** This matters
   only if someone quotes min/max values from S `models_table`.
   - B2: prob06 gives -6.04 in every cut mode (a 2.2e-5 bound difference over a 3.6e-6 gap).
   - baseline-noaggr vs c3:baseline gives -7.5e6 on pooling_haverly1tp: the c3:baseline root
     -400.0000019 is within 2e-6 of the target -400. It also gives -192.8 (pooling_bental4tp),
     -156.5 (haverly3tp) and -13.5 (haverly2pq).
4. **D root baseline-extra without the flagged run.** Without the flagged waternd2 run, gap closed
   is median 0 [-0.0132, 0.344] over 18 models. The digest's [-0.243, 0.344] includes the flagged
   run (the digest says so).
5. **The c3: reference for B2 bounds is sound; for times it is not.**
   - The v3d diagnostic baseline (`v3d/runs/partB-root-rowdir`) has the same `root_dual` and `dual`
     as the campaign-3 Part B root baseline on all 30 models. Both use SCIP 10.0.2 (record field
     `scip_version`).
   - So B2 bound comparisons against c3:baseline are not affected by run-to-run variation.
   - Times are affected: mean load 16.35 for the c3: runs against 3.51-3.56 for B2 (point 5 of
     Surprise 11).
6. **Soft-budget overshoots in D root.** Surprise 10 lists the summarizer's soft-budget overshoots
   for C2, C3 and D full only.
   - D root also has 5: kall_ellipsoids_tc05a baseline 120.10 s, all 120.10 s, baseline-extra
     120.16 s; ringpack_20_2 baseline-extra 121.16 s; kall_circlespolygons_c1p5b baseline-extra
     124.49 s.
   - Sources: S `partD-root by_mode.*.soft_budget_overshoots`; records `total_seconds +
     preparation_seconds`.
   - The D full time-limit runs alone were charged 300.21-300.36 s.
7. **Wording of the B2 heading.** The heading "no aggregation" does not apply to B2 baseline-extra,
   which runs with default presolve (README mode table). This is why its reference is c3:baseline,
   as the digest uses.

## Confirmed (selection; all 338 matching checks are listed by the script)

### Run status and replay

- B2: 150/150 runs; optimal 37, gaplimit 6, nodelimit 107; 0 failures.
- D root: 100/100 runs; nodelimit 95, timelimit 5.
- D full: 80/80 runs; optimal 4, gaplimit 3, timelimit 73.
- Replay passed in all three: 1,007, 1,736 and 28 cuts, every recorded cut replayed. Config
  failures 0, and tampering was rejected in every cut mode (`replay.json` fields `passed`,
  `replayed_cuts`, `v4.config_failures`, `v4.tamper_controls_by_mode`).
- 0 classifier errors. For every v4 run, the cause counts add up to `row_binding_rejections`.

### B2 funnel

| Mode | Support calls | Cert. failures | Below threshold | Binding rejections (runs) | Cuts | Share |
|---|---:|---:|---:|---|---:|---:|
| c3:all | 436 | 7 | 316 | 23 (9) | 90 | 20.4% |
| all-noaggr | 446 | 7 | 326 | 6 (5) | 107 | 5.3% |
| c3:all-diag | 1,618 | 19 | 1,039 | 202 (17) | 358 | 36.1% |
| all-diag-noaggr | 1,572 | 17 | 1,058 | 47 (13) | 450 | 9.5% |
| all-diag-rowdir-noaggr | 1,640 | 19 | 1,124 | 47 (13) | 450 | 9.5% |

- Causes and statuses match the digest.
- Callbacks: 52, 210, 210.
- Run counts for the caps match.
- The per-model binding/cuts and certification-failure counts all match.

### B2 bounds

- all-noaggr vs baseline-noaggr: 3/27/0 at 1e-4, and 4 better, 1 worse at 1e-6.
- all-diag-noaggr: 6/23/1, and at 1e-6 6/22/2.
- all-diag-rowdir-noaggr has bit-identical root bounds and per-model cut counts to all-diag-noaggr.
- baseline-noaggr vs c3:baseline: 0/24/6.
- baseline-extra vs c3:baseline: 12/17/1.
- At 1e-4: c3:all better 3, c3:all-diag better 4, neither worse.
- All 21 quoted root-bound values match. All 24 quoted gap-closed values match (sign-adjusted for
  pointpack04).
- Solved at the root: 8 (c3:baseline), 7 (baseline-noaggr), 13 (baseline-extra).
- wastewater04m2 has no incumbent in any mode.

### B2 native separators and times

- Native separators in baseline-extra and baseline-noaggr match exactly. Example: interminor
  21/939/429,680/1,985; intersection cuts 26/24,141/6,829.
- B2 time rows match:

  | Mode | SGM total (s) | SGM SCIP excl. callback (s) | SGM callback (s) | Median SCIP-excl / ref SCIP | Median total / ref |
  |---|---:|---:|---:|---:|---:|
  | all-noaggr | 0.6493 | 0.1461 | 0.4772 | 0.997 | 3.91 |
  | all-diag-noaggr | 1.184 | 0.1494 | 1.023 | 1.005 | 7.28 |
  | all-diag-rowdir-noaggr | 1.240 | 0.1465 | 1.082 | 0.958 | 7.51 |

  Reference baseline-noaggr: SGM total 0.1949 s, SGM SCIP 0.1511 s.
- baseline-extra vs c3:baseline: median total ratio 1.289.

### D root

- Cuts: all 14 (2 models); all-diag 891 (13); all-diag-rowdir 831 (13). All per-model counts match.
- Bounds vs baseline at 1e-4: all 0/19/1; all-diag and rowdir 1/14/5; baseline-extra 8/8/3 plus
  1 flagged.
- At 1e-6, multiplants_mtg6 is also worse for all-diag.
- Gap closed over 19 models (mpbp_31 has no reference): all 0 [-0.00323, 0]; all-diag and rowdir
  0 [-0.0306, 0.0389]; baseline-extra 0 [-0.243, 0.344].
- All 19 per-model gap-closed values match. 28 of the 30 quoted bound values match; items 6 and 7
  are the exceptions.

| Mode | Callbacks | Support calls | Cert. failures | Below threshold | Binding rejections (runs) | Cuts |
|---|---:|---:|---:|---:|---|---:|
| all | 22 | 176 | 2 | 149 | 11 (3) | 14 |
| all-diag | 115 | 6,352 | 313 | 5,042 | 106 (8) | 891 |
| all-diag-rowdir | 107 | 6,378 | 313 | 5,128 | 106 (8) | 831 |

- Summed separator seconds (callback / discovery / candidate / certification): all 18.4 / 15.7 /
  0.4 / 1.8; all-diag 188.4 / 53.6 / 22.8 / 69.8; rowdir 190.8 / 53.1 / 20.8 / 73.1.
- Discovery: 12 stopped models, and they are exactly the 12 with scan discovery above 1 s.
- Time rows, as (SGM total / SGM SCIP excl. callback / SGM callback, median SCIP-excl ratio, median
  total ratio): all 11.09 / 9.084 / 0.911, 0.995, 1.106; all-diag 17.76 / 8.572 / 6.838, 0.996,
  2.134; rowdir 17.92 / 8.614 / 6.940, 0.987, 2.161. Reference baseline: 10.07 / 9.22.
- baseline-extra median total ratio: 1.396.
- waternd2 baseline-extra: SCIP primal 3,084,095.92, recomputed 2,297,367.49, discrepancy 0.342,
  max scaled violation 3.4e-11. No other primal check failed.
- Five time-limit runs, up to 124.49 s.
- 15 runs without an incumbent (blend480, crudeoil_li03, kall_ellipsoids_tc05a in all modes).
- Only hydroenergy2 differs between all-diag and rowdir, in both root bound and cuts (133 vs 73).

### D full

- Solved: 2/2/2/1, the same models as in the digest.
- Final dual vs baseline at 1e-4: all 5/14/1; auto 4/16/0; baseline-extra 7/6/7. The model sets
  match.
- All quoted dual values match except item 8.
- Cuts only on tc02b (11) and kriging (3) in both all and auto. No 1e-4 difference occurs on a model
  with cuts.
- SGM on blend480: 63.36 / 63.70 (62.28, 1.0) / 62.62 (61.14, 1.0) / 49.54.
- SGM over all 20 runs: 275.8 / 276.4 (274.3) / 276.2 (274.1) / 274.5. Summed callback 18.77 s
  (all) and 18.81 s (auto).
- Funnel all: 22 / 180 / 2 / 153 / 11 (3) / 14. Funnel auto: 24 / 170 / 0 / 145 / 11 (3) / 14.
- 11 runs stopped in discovery in each mode: the root set minus multiplants_mtg6.
- 73 time-limit runs, all overshoots; the largest is 300.358 s (kriging_peaks-full100
  baseline-extra).
- kall_ellipsoids_tc05a: baseline, all and auto ended at node 1 without an incumbent.
