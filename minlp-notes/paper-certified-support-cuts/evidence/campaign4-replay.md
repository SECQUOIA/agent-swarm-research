# Campaign 4: replay of every recorded cut (Parts C2, C3, B2, D-root, D-full)

Run on 2026-10-03, 21:03:44Z to 21:24:37Z (UTC). Part C4 was still running and was not read, replayed or touched.

## Result

All five replays passed (exit code 0). Every recorded cut was replayed and accepted: 56,771 of 56,771. Each part had complete coverage, no Config or SCIP-parameter failures and no Gurobi-parameter failures. In every cut mode, the untampered first cut passed and all 14 archived tampering mutations were rejected. Nothing failed, so step 4 (investigating failures) did not apply.

## Commands

From `/workspace/minlp-notes/paper-certified-support-cuts/experiments/v4`, with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1`, the five replays ran at the same time as background processes in one bash command, followed by `wait`:

```
/usr/bin/time -f "%e s wall, %M KB maxrss" /workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python replay_v4.py runs/DIR > runs/replay-DIR.log 2>&1
```

Here DIR is partC2, partC3, partB2, partD-root or partD-full. The only difference from the requested command is the `/usr/bin/time` prefix. It adds a second line to each log with the wall time and peak memory. The first line of each log is the JSON summary printed by `replay_v4.py`. Each run wrote `runs/DIR/replay.json`. All five processes exited with code 0. The C4 driver (6 workers) ran on the same host throughout, so the times below are descriptive only.

All five parts used the same checker:

- Archived checker: `snapshot/research-20261003-convexification/experiments/replay.py`, SHA-256 `10115390a428ca2e...` (`replay.json` field `replay_source_sha256`).
- Support checker: imported from each part's own verified snapshot (`snapshot/research-20261003-convexification/solver/support.py`, field `checker`).
- Wrapper: `replay_v4.py`, SHA-256 `05e0138106104ee5...` (field `wrapper_source_sha256`). This matches `sha256sum` of the current file.

## Per-part results

Source: `experiments/v4/runs/DIR/replay.json`. Top-level fields: `passed`, `archived_passed`, `records`, `bound_runs`, `admitted_runs`, `cuts`, `replayed_cuts`, `missing_cut_logs`, `replay_seconds`, `wrapper_seconds`, `source_files_verified`. Fields under `v4`: `coverage_complete`, `config_failures`, `config_checked_runs`, `gurobi_failures`, `gurobi_checked_runs`. The same values appear on the first line of `runs/replay-DIR.log`. Wall time comes from the second line of that log.

| Field | partC2 | partC3 | partB2 | partD-root | partD-full |
|---|---:|---:|---:|---:|---:|
| passed | true | true | true | true | true |
| archived_passed | true | true | true | true | true |
| records | 140 | 180 | 150 | 100 | 80 |
| bound_runs | 120 | 160 | 150 | 100 | 80 |
| admitted_runs | 120 | 160 | 150 | 100 | 80 |
| cuts | 24000 | 30000 | 1007 | 1736 | 28 |
| replayed_cuts | 24000 | 30000 | 1007 | 1736 | 28 |
| failed runs (`runs[].passed` false) | 0 | 0 | 0 | 0 | 0 |
| missing_cut_logs | 0 | 0 | 0 | 0 | 0 |
| coverage_complete (scheduled = recorded; missing / unscheduled / duplicates) | true (140 = 140; 0/0/0) | true (180 = 180; 0/0/0) | true (150 = 150; 0/0/0) | true (100 = 100; 0/0/0) | true (80 = 80; 0/0/0) |
| config_failures (of config_checked_runs) | 0 of 120 | 0 of 160 | 0 of 150 | 0 of 100 | 0 of 80 |
| gurobi_failures (of gurobi_checked_runs) | 0 of 20 | 0 of 20 | 0 of 0 | 0 of 0 | 0 of 0 |
| source_files_verified (manifest) | 106 | 106 | 146 | 126 | 126 |
| replay_seconds (archived replay) | 1004.39 | 1232.88 | 38.05 | 329.46 | 108.04 |
| wrapper_seconds (whole replay_v4.py run) | 1015.26 | 1252.62 | 40.64 | 337.59 | 112.78 |
| wall time (`/usr/bin/time`, log line 2) | 1015.64 s | 1253.14 s | 41.05 s | 337.97 s | 113.19 s |

In C2 and C3, bound_runs is 20 less than records. These are the 20 `gurobi` runs in each part. As designed (v4 README, "Mode gurobi"), they have no `original_model` block, so the archived replay lists them in `omitted_runs` instead of checking them. All 20 omitted runs in each part have 0 cuts (`omitted_runs[].cuts`). Their statuses are: C2 timelimit 13, gaplimit 5, optimal 2; C3 timelimit 15, gaplimit 3, optimal 2. Their Gurobi parameters were checked by the wrapper (`v4.gurobi_checked_runs` = 20, `v4.gurobi_failures` = []).

Recorded cuts by mode, counted directly from `runs/DIR/records.jsonl` (sum of `len(cuts)` per `mode`). The totals match `cuts` above:

| Part | Cuts by mode |
|---|---|
| partC2 | frozen-wide 24000. Modes with no cuts: baseline-novarlocks, baseline-extra, gurobi |
| partC3 | rowdir-wide 24000, all-diag-mech 6000. Modes with no cuts: baseline, baseline-extra, gurobi |
| partB2 | all-diag-noaggr 450, all-diag-rowdir-noaggr 450, all-noaggr 107. Modes with no cuts: baseline-noaggr, baseline-extra |
| partD-root | all-diag 891, all-diag-rowdir 831, all 14. Modes with no cuts: baseline, baseline-extra |
| partD-full | all 14, auto 14. Modes with no cuts: baseline, baseline-extra |

## Tampering controls

Source: `runs/DIR/replay.json`, fields `v4.tamper_controls_by_mode`, `v4.modes_with_cuts`, `v4.tamper_controls_cover_all_cut_modes` and `tamper_rejections`.

Method: for each cut mode, the wrapper takes the first record in `records.jsonl` order that has cuts and passed the replay. It keeps only that record's first cut and checks it untampered (`untampered_first_cut_passed`). It then applies each of the 14 archived mutations separately and records whether the check rejects the result (`rejections`). The 14 mutations are:

- original_model_digest
- support_coefficient
- source_side_rhs
- source_side_identity
- support_feature
- support_box
- row_rhs
- local_scope
- rounding_compensation
- support_identity
- actual_coefficient
- actual_bound
- actual_mapping
- bound_proof

The archived replay also runs its own control on the first passed cut-bearing record of the part (`tamper_rejections`). The wrapper restricts that control to the first cut as well.

| Part | Tamper mode | Control record (`run_id`) | Cuts in record | Untampered first cut passed | Corruptions rejected |
|---|---|---|---:|---|---:|
| partC2 | frozen-wide | 005_interleaved_path_n40_s0__full__s0__frozen-wide | 640 | true | 14 of 14 |
| partC3 | rowdir-wide | 002_interleaved_path_n80_s7__full__s0__rowdir-wide | 1280 | true | 14 of 14 |
| partC3 | all-diag-mech | 001_interleaved_path_n80_s6__full__s0__all-diag-mech | 320 | true | 14 of 14 |
| partB2 | all-noaggr | 000_pooling_bental4tp__root__s0__all-noaggr | 3 | true | 14 of 14 |
| partB2 | all-diag-noaggr | 002_sep1__root__s0__all-diag-noaggr | 8 | true | 14 of 14 |
| partB2 | all-diag-rowdir-noaggr | 002_sep1__root__s0__all-diag-rowdir-noaggr | 8 | true | 14 of 14 |
| partD-root | all | 002_kall_ellipsoids_tc02b__root__s0__all | 11 | true | 14 of 14 |
| partD-root | all-diag | 002_kall_ellipsoids_tc02b__root__s0__all-diag | 200 | true | 14 of 14 |
| partD-root | all-diag-rowdir | 002_kall_ellipsoids_tc02b__root__s0__all-diag-rowdir | 200 | true | 14 of 14 |
| partD-full | all | 002_kall_ellipsoids_tc02b__full__s0__all | 11 | true | 14 of 14 |
| partD-full | auto | 002_kall_ellipsoids_tc02b__full__s0__auto | 11 | true | 14 of 14 |

In each of the five parts, the archived part-level control (`tamper_rejections`) also rejected 14 of 14. `v4.tamper_controls_cover_all_cut_modes` is true in every part: the tamper modes equal `v4.modes_with_cuts`. Scope (field `v4.tamper_scope`): "archived mutations applied to the first cut of the record". Across the five parts, 11 mode controls rejected 154 of 154 corruptions. With the five part-level controls (70 of 70), the total is 224 of 224.

## Totals

Campaign 4, the five finished parts. Source: `replayed_cuts` in each `experiments/v4/runs/DIR/replay.json`.

- C2 24,000 + C3 30,000 + B2 1,007 + D-root 1,736 + D-full 28 = **56,771 replayed cuts** (of 56,771 recorded).

Campaign 3 and the post hoc v3d diagnostic. Source: `replayed_cuts` on the single line of each existing log. These are the same values as `replayed_cuts` in the matching `replay.json`, all with `passed` true.

| Log | records | cuts | replayed_cuts | Cut modes (cuts, from records.jsonl) |
|---|---:|---:|---:|---|
| `experiments/v3/runs/replay-partA-full.log` | 270 | 188 | 188 | all 151, auto 37 |
| `experiments/v3/runs/replay-partA-root.log` | 120 | 465 | 465 | all-diag 403, all 50, auto 12 |
| `experiments/v3/runs/replay-partB.log` | 300 | 845 | 845 | all-diag 358, all 269, auto 218 |
| `experiments/v3/runs/replay-partC.log` | 80 | 6000 | 6000 | all-diag-mech 6000 |
| **Campaign 3 (v3) subtotal** | | | **7,498** | |
| `experiments/v3d/runs/replay-partA-root-rowdir.log` | 120 | 469 | 469 | all-diag 403, all 52, auto 14 |
| `experiments/v3d/runs/replay-partB-root-rowdir.log` | 120 | 529 | 529 | all-diag 358, all 95, auto 76 |
| `experiments/v3d/runs/replay-partC-rowdir.log` | 120 | 30000 | 30000 | all-diag-mech-wide 24000, all-diag-mech 6000 |
| **v3d diagnostic subtotal** | | | **30,998** | |

Grand totals over the parts replayed so far (C4 to be added later):

- Campaign 3 including v3d: 7,498 + 30,998 = **38,496**.
- Campaigns 3 and 4, including v3d: 38,496 + 56,771 = **95,267**.
- Campaigns 3 and 4, without v3d: 7,498 + 56,771 = 64,269.

Notes for the paper:

- The v3d runs are separate solver runs with their own records. Their cut modes ran with the row-direction variant code (`v3d/README-diagnostic.md`), so their cuts are not copies of the v3 records. A paper that keeps the post hoc diagnostic apart from the prospective campaigns should use 64,269 and state 30,998 separately.
- The same archived `replay.py` (`replay_source_sha256` `10115390a428ca2e...`) produced every count above. The v3 and v3d replay.json files record a different wrapper (`wrapper_source_sha256` `ce10b4c71a50471a...`, the campaign-3 wrapper) from campaign 4 (`05e0138106104ee5...`).
- The campaign-3 logs report no `gurobi_failures` field because campaign 3 had no Gurobi mode.

## Files written

- `experiments/v4/runs/{partC2,partC3,partB2,partD-root,partD-full}/replay.json`, written by `replay_v4.py`.
- `experiments/v4/runs/replay-{partC2,partC3,partB2,partD-root,partD-full}.log`.
- This report.

No records, cases, snapshots or code were modified. No SCIP or Gurobi solve was started.

## Verification

Commands actually run (all targeted; no project-wide tests, no CI):

- the five `replay_v4.py` runs above;
- read-only Python summaries of the five new `replay.json` files and of the five campaign-4 `records.jsonl` files (cuts per mode);
- read-only summaries of the seven campaign-3/v3d `replay.json` and `records.jsonl` files;
- `sha256sum experiments/v4/replay_v4.py`.
