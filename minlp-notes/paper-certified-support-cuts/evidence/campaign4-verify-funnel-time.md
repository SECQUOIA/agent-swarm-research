# Campaign 4: independent check of the funnel and time numbers in the digest (2026-10-03)

Checked document: `evidence/campaign4-digest.md`. Scope: the separator funnel,
cap counts, separator callback time and its parts, SGMs, per-run time ratios,
and native SCIP separator activity in baseline-extra, for the five finished
campaign-4 parts (C2, C3, B2, D root, D full).

Script: `verification/R8_funnel_time.py` (standard library only). It reads
`records.jsonl`, `jobs.json` and `cases/` of `experiments/v4/runs/partC2`,
`partC3`, `partB2`, `partD-root` and `partD-full`, the campaign-3 reference
records `experiments/v3/runs/partC` and `partB` (as `c3:` modes, matched by
phase, model and seed), and `experiments/v4/scanD/records.jsonl`. It does not
import `summarize_v4`, `summarize_v3`, `campaign4_digest.py` or any other
producer code. It holds each digest value next to its own recomputed value and
compares them at the digest's printed precision. It did not open
`runs/partC4`.

## Commands run (targeted, local; no project-wide tests, no CI)

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
PY=/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python
cd /workspace/minlp-notes/paper-certified-support-cuts/verification
$PY R8_funnel_time.py            # prints every check, then extra numbers not in the digest
```

Also run: one-off read-only `python3 -c` snippets to inspect the record schema
and the separator code (`v4/snapshot/research-20261003-convexification/solver/integration.py`),
and a read of `experiments/v4/results/summary.json` and of `summarize_v4.py`
(docstring; line 134) only to explain the mismatches below. No SCIP or Gurobi
solve. No file under `experiments/` was changed. No replay was run.

Result: 552 checks, 533 match, 19 do not. The 19 come from three causes,
listed below. A fourth item is a wording problem with correct numbers.

## Definitions used

Taken from the protocol and `v4/README.md`:

- Solved: status optimal or gaplimit, `returncode` 0, no `worker_status`, and
  `primal_check.checked` and `passed` both true.
- Root phase "completed": not failed, `total_seconds` present, and a root bound exists.
- Time = `total_seconds + preparation_seconds`.
- SCIP time = `scip_solve_seconds` (`solver_runtime_seconds` for Gurobi).
- Callback = `separation.callback_seconds`. This includes discovery, which runs
  inside the callback.
- SCIP time excluding the callback = SCIP time - callback. This script does not
  clip the difference at 0.
- SGM: shift 1 s.
- Below threshold = `certification_calls - certification_failures -
  row_rounding_rejections - row_binding_rejections - cuts`.
- Caps per run, using that run's `config`:
  - cut cap: `cuts >= max_cuts`;
  - support-call cap: `certification_calls >= max_support_calls`;
  - callback cap: `calls >= max_rounds`;
  - time budget (inferred): `budget_exhausted` without the cut cap or the support-call cap;
  - discovery stopped: `discovery_incomplete`.

## Mismatches

### 1. D full time-decomposition rows use the wrong run set (major)

Digest location: the table in "Time decomposition", rows "D full | all (1:
blend480)" and "D full | auto (1: blend480)".

The table header defines its run set as "runs ... solved (full) by both the mode
and its reference". In D full, baseline, all and auto each solved two models:
blend480 (optimal) and kriging_peaks-full100 (gaplimit). The record fields are
`status` and `primal_check.passed`. So the run set has 2 pairs, not 1. The
digest used the run set that all four modes solved, which is blend480 alone,
because baseline-extra did not solve kriging_peaks-full100. That set is the
right one for "SGM over commonly solved runs" in D (b), but not for this table.
The digest's own source agrees with the 2-pair set:
`results/summary.json`, partD-full `larger/full`, `times.ratio_summary` gives
all `count` 2, `median` 1.0212 and auto `count` 2, `median` 1.0142.

| Row | Digest (1 pair) | Recomputed (2 pairs) |
|---|---|---|
| all: SGM total / SCIP excl. callback / callback | 63.70 / 62.28 / 1.0 | 131.0 / 129.2 / 1.0 |
| all: reference SGM total / SCIP | 63.36 / 62.91 | 128.3 / 127.7 |
| all: median SCIP-excl / ref SCIP | 0.990 | 1.012 |
| all: median total / ref | 1.005 | 1.021 (faster in 0 of 2) |
| auto: SGM total / SCIP excl. callback | 62.62 / 61.14 | 130.1 / 128.2 |
| auto: median SCIP-excl / ref SCIP | 0.972 | 1.004 |
| auto: median total / ref | 0.988 | 1.014 (faster in 1 of 2) |

Per-run values (time / SCIP / callback, in s):

| Model | baseline | all | auto |
|---|---|---|---|
| kriging_peaks-full100 | 258.89 / 258.17 / 0 | 268.48 / 267.74 / 1.019 | 269.29 / 268.56 / 1.015 |
| blend480 | 63.36 / 62.91 / 0 | 63.70 / 63.28 / 1.0 | 62.62 / 62.14 / 1.0 |

The digest's numbers are correct for blend480 alone. The error is that the table
reports 1 pair under a definition that gives 2. One consequence: the bullet
under the table says "median ratios 0.958-1.005" for SCIP time excluding the
callback on B2 and D. With the 2-pair rows the range is 0.958-1.012. The claim
("SCIP's own time is unchanged; the slowdown is the callback") still holds. The
row "auto 0.988" should not be quoted as auto being faster: on the stated
definition auto is slower (median 1.014).

### 2. The callback cap is 3 for modes all and auto, not 10 (major)

Digest locations:
- the B2 (a) caps bullet ("the 10-callback cap in 10");
- the D (a) caps bullet ("10-callback cap in 1");
- the funnel table column "10 callbacks", in the rows B2 all-noaggr, D root all,
  D full all and D full auto.

Modes all, auto and all-noaggr use the frozen limits. Their records give
`config.max_rounds` 3, `max_support_calls` 24, `max_cuts` 12 and
`max_separation_seconds` 1.0. The counts are correct when the cap is taken as
`calls >= max_rounds` = 3:

- B2 all-noaggr: 10 runs;
- D root all: 1;
- D full all: 1;
- D full auto: 2.

Only the stated value of the cap (10) is wrong. The value 10 is correct for
the all-diag, all-diag-rowdir, all-diag-mech, frozen-wide and rowdir-wide
modes.

### 3. B2 all-diag-rowdir-noaggr: SGM of SCIP time excluding the callback (minor)

Digest: 0.1465 ("Time decomposition" table). Recomputed: 0.1459.

The cause is a definition difference. On one run, B2
all-diag-rowdir-noaggr pooling_haverly3pq, `scip_solve_seconds` is 0.3550 and
`separation.callback_seconds` is 0.3698, so the difference is -0.0148 s.
`summarize_v4.py` (line 134) clips the difference at 0, which gives 0.1465.
Without clipping the value is 0.1459. The digest's definition ("SCIP time
excluding the callback: their difference") does not mention the clipping. The
negative value arises because the two times come from different clocks:
SCIP's clock for the solve time and Python's `perf_counter` for the callback.
This is the only run in the five parts where the callback exceeds the SCIP
time.

### 4. Wording: "baseline-extra raises SCIP's root time" quotes total-time ratios (minor)

Digest location: the "Non-cut comparators" bullet. The bullet quotes the
median total-time ratios: 1.196 (C2), 1.262 (C3), 1.289 (B2, against
c3:baseline) and 1.396 (D). These numbers are correct. The median SCIP-time
ratios are 1.205, 1.268, 1.356 and 1.427, so the direction is the same. For
baseline-novarlocks at the C2 root, the total-time ratio is 0.229 (correct as
quoted) and the SCIP-time ratio is 0.161.

## Confirmed (all match)

### Run counts

The scheduled, recorded and missing counts are 140/140/0 (C2), 180/180/0 (C3),
150/150/0 (B2), 100/100/0 (D root) and 80/80/0 (D full). No record has
`returncode` other than 0 or a `worker_status`.

### Funnel table

All 12 rows of the funnel table match. The checked fields are:

- runs;
- callbacks (sum of `separation.calls`);
- support calls (`certification_calls`);
- certification failures;
- below threshold;
- binding rejections, with the number of runs that had any;
- causes (`row_binding_rejection_causes.causes`);
- cuts (`separation.cuts`, which also equals `len(cuts)` in every run);
- counts of runs that hit the cut cap, the support-call cap, the callback cap
  or the time budget, and runs where discovery stopped.

Other funnel facts that match:

- Rounding rejections are 0 in every mode, including c3:all and c3:all-diag.
- `classifier_errors` is 0 everywhere.
- In C2 and C3, the root and full funnels are identical per run in every
  counter, for frozen-wide, c3:all-diag-mech, all-diag-mech and rowdir-wide.
- Every C2 and C3 cut-mode run reached its cut cap, and none reached the
  support-call cap.

### B2 table and bullets

- c3:all: 436 support calls, 7 certification failures, 316 below threshold,
  23 binding rejections (9 runs), 90 cuts. c3:all-diag: 1,618 / 19 / 1,039 /
  202 (17) / 358. Neither has rejection causes recorded.
- Shares binding / (binding + cuts): 20.4%, 5.3%, 36.1%, 9.5% and 9.5%.
- Variable statuses in rejected rows: FIXED 1 (all-noaggr) and FIXED 17 (both
  diag modes).
- SCIP's coefficient handling (integer snaps plus dropped tiny coefficients):
  5 in all-noaggr and 33 in all-diag-noaggr.
- Per-model binding/cuts, c3:all-diag -> all-diag-noaggr:
  - kall_circlespolygons_c1p12: 127/25 -> 0/104;
  - pooling_adhya4tp: 17/29 -> 17/29 (14 variable_not_column, 3 rounded);
  - bayes2_50: 17/8 -> 12/8 (all tiny coefficients);
  - bayes2_30: 3/0 -> 3/0 (tiny coefficients);
  - pooling_rt2tp: 4/46 -> 4/46 (rounded).
- all-diag-rowdir-noaggr has the same per-model binding rejections, cuts and
  causes as all-diag-noaggr.
- Certification failures per model:
  - all-noaggr: ex8_1_7 7;
  - all-diag-noaggr: ex8_1_7 9, tanksize 8;
  - all-diag-rowdir-noaggr: ex8_1_7 11, tanksize 8;
  - c3:all: ex8_1_7 7;
  - c3:all-diag: ex8_1_7 9, tanksize 10.
- Runs that hit no cap: 4, 17 and 17.

### D root

- Callback / discovery / direction-LP / certification sums: 18.4 / 15.7 /
  0.4 / 1.8 s (all), 188.4 / 53.6 / 22.8 / 69.8 s (all-diag), and 190.8 /
  53.1 / 20.8 / 73.1 s (all-diag-rowdir).
- Certification failures per model and binding rejections per model match.
  The rejected-row statuses are FIXED 109 and AGGREGATED 85.
- The all-diag cut counts match for all 13 models, and all-diag-rowdir gave 73
  cuts on hydroenergy2.
- Mode all stopped discovery on exactly the 12 listed models. These are
  exactly the models whose scan `discovery_seconds` exceeds 1 s (1.01-7.70 s).
  On each of them the callback took 1.0 s and made 0 support calls.
- Of the 8 models where discovery completed, 2 received cuts. The other 6 made
  21-24 support calls each.
- No-cap counts: 2 (all-diag) and 2 (all-diag-rowdir).

### D full

- Discovery stopped on the 11 root models other than multiplants_mtg6, in both
  all and auto. multiplants_mtg6 has a scan discovery time of 1.31 s.
- Cuts were added only on kall_ellipsoids_tc02b (11) and kriging_peaks-full100
  (3).
- The summed callback time is 18.8 s in each of all and auto.
- The SGMs over blend480 (63.36, 63.70 (62.28, 1.0), 62.62 (61.14, 1.0),
  49.54) and over all 20 runs (275.8, 276.4 (274.3), 276.2 (274.1), 274.5)
  match.

### Time-decomposition table

All 14 rows other than D full match in every column: pairs, SGM total, SGM SCIP
time excluding the callback, SGM callback, the reference SGMs, and both median
ratios. The one exception is the B2 rowdir clipping in item 3.

### C2 full

- SGMs over the 7 instances that all six modes solved: 5.597, 3.727, 2.709,
  4.030, 4.623 and 6.321.
- Median per-run ratios (pairs; faster): 0.773 (9; 6), 0.384 (9; 8), 0.482
  (9; 7), 1.171 (9; 4) and 0.256 (7; 4).
- SGMs over the 9 pairs against c3:baseline's 10.270: 6.661, 4.817, 6.531 and
  5.166. Gurobi: 6.321 against 5.597.
- Solved counts: 9, 9, 10, 10, 13 and 7.

### C3 full

- SGMs over the 5 common instances, with SCIP time (baseline modes and Gurobi)
  or SCIP time excluding the callback (cut modes):

  | Mode | SGM time (s) | SGM SCIP or SCIP excl. callback (s) |
  |---|---:|---:|
  | baseline | 1.698 | 1.656 |
  | all-diag-mech | 2.104 | 1.202 |
  | rowdir-wide | 3.284 | 0.1238 |
  | baseline-extra | 1.061 | 1.026 |
  | gurobi | 0.334 | 0.330 |

- Median ratios: 0.858 (9; 5), 0.860 (9; 5), 0.627 (9; 6) and 0.235 (5; 5).
- SGMs over the 9 pairs: 7.267, 4.434 and 7.067, against 9.379.
- rowdir-wide over all 20 runs: SGM 10.19 s, times 3.17-33.17 s (n80
  31.7-33.2 s), callback 268.6 s of 279.7 s charged, at most 38 nodes.

### Comparators and C2 root

- baseline-extra median total-time ratios at the root: 1.196, 1.262, 1.289
  and 1.396. baseline-novarlocks: 0.229 (root) and 0.384 (full).
- C2 root SGM: baseline-novarlocks 0.341 s, c3:baseline 1.099 s.

### Native separators

- B2 baseline-extra (runs / calls / found / applied):
  - interminor: 21 / 939 / 429,680 / 1,985;
  - RLT: 27 / 229 / 208 / 9;
  - minor: 4 / 145 / 320 / 110;
  - eccuts: 0.
- B2 baseline-extra intersection cuts: the quadratic nonlinear handler
  produced cuts in 26 runs, with 24,141 `#Enforce` calls and 6,829 `Cuts`.
- B2 baseline-noaggr: interminor 0, intersection cuts 0, minor 4 / 54 / 71 /
  36, RLT 27 / 164 / 129 / 5.
- Path family, baseline-extra root runs:
  - intersection cuts in 20 runs: 29,210 calls / 14,907 cuts (C2) and
    31,490 / 14,875 (C3);
  - interminor, eccuts and minor: 0 calls;
  - RLT: 200 calls, 0 cuts.
- C2 root baseline-novarlocks, minor: 20 / 661 / 34,061 / 17,039.
- minor made no productive call in any other C2 or C3 SCIP mode, at the root
  or in full runs.
- Campaign-3 records hold no `native_statistics`.

### Load and soft-limit overshoots

- Mean load at the start (`load_start_mean`):
  - campaign-3 reference runs: 15.96-15.98 (C2 full) and 16.35-16.36 (B2);
  - C2 full campaign-4 modes: 6.49-6.90;
  - all campaign-4 runs: 3.51-7.67.
- 300 s time-limit runs: 40 (C2), 47 (C3) and 73 (D full). They were charged
  300.19-300.36 s; the maximum is kriging_peaks-full100 baseline-extra in D
  full.
- D root has five 120 s time-limit runs, as listed in the digest. The largest
  charged time is 124.49 s (kall_circlespolygons_c1p5b, baseline-extra).

## Facts in scope that the digest omits

1. **Callback parts for C2, C3, B2 and D full.** The digest gives the parts only
   for D root. The parts listed below are discovery, direction LPs and
   certification. "Unattributed" is what remains after subtracting those three
   and row insertion. It covers sample evaluation, exchange points, exact row
   rounding and other bookkeeping, and it is not small in the path family.
   All values are sums over the 20 or 30 runs, in seconds.

   | Part, phase, mode | Callback | Discovery | Direction LPs | Certification | Unattributed |
   |---|---:|---:|---:|---:|---:|
   | C2 root frozen-wide | 240.4 | 10.3 | 31.1 (13,088 LPs) | 121.3 | 76.4 |
   | C2 root c3:all-diag-mech | 73.6 | 10.6 | 9.6 (3,315 LPs) | 32.0 | 21.0 |
   | C3 root all-diag-mech | 67.9 | 10.2 | 8.1 (3,441 LPs) | 31.0 | 18.4 |
   | C3 root rowdir-wide | 269.2 | 10.3 | 32.6 (14,358 LPs) | 140.1 | 84.9 |
   | B2 all-noaggr | 15.7 | 2.0 | 1.8 | 11.2 | 0.7 |
   | B2 all-diag-noaggr | 38.6 | 2.1 | 8.6 | 25.7 | 2.2 |
   | B2 all-diag-rowdir-noaggr | 41.4 | 2.0 | 8.6 | 28.3 | 2.3 |
   | D root all-diag | 188.4 | 53.6 | 22.8 | 69.8 | 42.0 |
   | D full all | 18.8 | 15.9 | 0.4 | 1.8 | 0.6 |
   | D full auto | 18.8 | 16.0 | 0.4 | 1.7 | 0.6 |

   Full-run values for the path family are within about 4 s of the root values.
   The funnels are identical, and only the times differ.

2. **Native separators in D baseline-extra.** The digest reports B2 and the path
   family only. Counts are runs / calls / found / applied.

   - D root baseline-extra:
     - interminor: 17 / 1,082 / 900,703 / 2,582;
     - RLT: 20 / 191 / 2,297 / 65;
     - minor: 4 / 506 / 20,907 / 7,451;
     - eccuts: 0;
     - intersection cuts in 18 runs: 141,948 `#Enforce`, 32,294 cuts.
   - D root baseline, for contrast: interminor 0, minor 5 / 436 / 26,101 /
     7,965, RLT 20 / 180 / 106 / 40, intersection cuts 0.
   - D full baseline-extra: interminor 17 runs, eccuts 0, intersection cuts
     in 19 runs (37,203 cuts).
   - The sonet23v4 records hold no nonlinear-handler table
     (`native_statistics.nlhdlrs` is null in all 9 of its D records). Its
     intersection-cut count is therefore unknown, not 0.

3. **Clipping.** The summarizer clips SCIP time excluding the callback at 0
   (see mismatch 3). The digest's definition should say so, or the one
   affected value should be given unclipped.

4. **The time-budget inference.** The digest writes that `budget_exhausted` is
   set by `_expired` (time, support-call cap or cut cap). It is also set when
   discovery hits its deadline (`DiscoveryBudgetExhausted`, `integration.py`,
   `sepaexeclp`). That is still the time budget, so the counts are unaffected.
