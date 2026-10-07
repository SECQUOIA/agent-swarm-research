# Review r4 of stream `multiround` (note.md revised after review round 3)

Reviewer: independent research agent (confirmation round 4), 2026-10-03. I did not write any of
this material. "Reviewed" means checked by another research agent, not journal peer review.
Scope: confirmation only. I checked r3-m1, r3-o1 and r3-o2, and looked for errors introduced by
the revision (`note.md` diff, new `code/analyze_rev3.py`, `logs/summary_rev3.log` and the other
new logs). I did not re-review unchanged material. My code is in [`r4-code/`](r4-code/), outputs
in [`r4-logs/`](r4-logs/). My script reads the raw records directly and uses no stream code.

## Verdict

**Verified.** r3-m1 is fixed: the recovery bullet now uses the continued-orbit control. Every
number of the new table, the Holm values and the descriptive figures reproduce exactly from the
raw records with my own code. The conclusions follow from them and keep gains over the orbit rule
apart from gains over SCIP's rule. Both optional items are applied. I found no new error. Two
optional remarks follow; neither needs another round.

## Status of the round-3 items

| Item | Status | Evidence |
|---|---|---|
| r3-m1 (recovery bullet lacks the continued-orbit control) | **Fixed** | Section 3.5 now reports the paired contrast `e(20) − e(3)`, `e` = rule − orbit throughout, for four rules × {6×8, 10×20, pooled}. All 12 cells (means, 95% t-intervals, p-values) match my recomputation to the printed digits, e.g. 6×8 `o1s` +0.0005793 [−0.0105776, +0.0117362], p 0.9176; 10×20 `o3s` +0.0078221 [+0.0016929, +0.0139513], p 0.01344; pooled `o3s` +0.0059779 [+0.0019855, +0.0099703], p 0.00369. Holm over the 12 cells: `0.2778` (6×8 `o2s`), `0.1479` (10×20 `o3s`), `0.0443` (pooled `o3s`). Holm over all 36: pooled `o3s` is the smallest of the 36 raw p-values, so its adjusted value is 36 × 0.00369 = `0.1328`. The supporting figures in the bullet are right: SCIP's mean remaining gap on 6×8 is `0.0802154` at round 3 and `0.0272196` at round 20, and the deficit changes are `+0.0121881` (orbit) and `+0.0127674` (`o1s`). The "repair on 6×8, none on 10×20" reading is withdrawn everywhere: Summary item 3, Section 3.5, 3.7 item 2, recommendation (Section 4), Limits, and the round-1 and round-2 entries (Sections 11, 12). No such reading remains (`grep` for repair/recovery/asymmetry). |
| r3-o1 (`alt` tie counts) | **Fixed** | Section 3.6: "`alt` (over all its rounds)". |
| r3-o2 (number of rules) | **Fixed** | Limits: "twelve losing and non-losing rules on 6×8". |

### Round indexing and pairing

- `closed[r]` is the fraction of the root gap closed after `r` rounds; `closed[0] = 0` in every
  selected record, and each record has 21 states.
- `oKs` equals orbit throughout exactly through state `K` on every instance (checked for
  `K = 1, 2, 3, 5`). So `e(3) = 0` for `o3s`, and the note is right that this contrast starts from
  the same state. `e(3) = e(5) = 0` for `o5s`, so its 3→20 and 5→20 contrasts coincide, as the
  note says.
- Pairing is per (size, instance) over the same 60 6×8 and 50 10×20 instances for all six rules.
  My script collects records from `logs/{main,new,rev1,rev2,diag}` independently of the author's
  file selection. 438 duplicate trajectories occur across those directories, and all are
  identical, so the selection does not matter.

### Dependent statements

- **Summary item 3.** It quotes the controlled contrasts and the multiplicity sensitivity and
  calls them exploratory. This matches the data.
- **Recommendation ("keep SCIP's set").** It still follows from the data. Against SCIP throughout
  at round 20, every switching rule has a negative point estimate in every group (6×8 −0.001 to
  −0.006; 10×20 −0.015 to −0.021; pooled −0.008 to −0.013, `o2s`, `o3s`, `o5s` with intervals
  below 0). So "no switching rule establishes a gain over SCIP throughout" is correct. The new
  sentences correctly say that gains over continued orbit rounds are not gains over SCIP.
- **"Limited numerical evidence for later SCIP rounds helping some schedules relative to continued
  orbit rounds."** This is an accurate description. Of 12 contrasts over 3–20, all have positive
  point estimates, and only pooled `o3s` survives the 12-test Holm adjustment, which fails at 36.

## New issues

### Major

None.

### Minor

None.

### Optional

1. **Multiplicity family and test choice (sensitivity only).** The 36-test family contains three
   duplicate tests (`o5s` 3→20 = 5→20 in each group). Over the 33 distinct tests, pooled `o3s` has
   Holm p = `0.122`, so the conclusion does not change. The choice of test matters more for the
   12-test statement:
   - With a Wilcoxon signed-rank test instead of the t-test, the 3–20 p-values are `0.0029`
     (10×20 `o3s`), `0.0049` (pooled `o2s`) and `0.0056` (pooled `o3s`).
   - Holm over the 12 cells then keeps 10×20 `o3s` (`0.035`) but not pooled `o3s` (`0.056`).

   The sentence "Neither size has a significant contrast after Holm over the 12 rule/size/pooled
   comparisons" therefore depends on using the t-test. The note's overall reading (exploratory,
   limited evidence, no established size difference) is robust to this. A clause such as "with
   paired t-tests" would make the dependence explicit.
2. **Cosmetic.**
   - Section 12, o2 entry: the revision added four spaces of indentation to the line "and
     `pertE0.1` (Section 8, item 35)…". Markdown renders it the same, but the change is
     unintended.
   - The header line "This revision has not been independently re-reviewed" (top and Section 13)
     becomes stale once this review is recorded.

## Checks actually run (by this reviewer)

All from `research-20261001/multiround/` with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
PYTHONDONTWRITEBYTECODE=1`, every Python job in the foreground under `timeout`, one at a time.
Targeted checks only; no project-wide verification, no CI.

| Command | Outcome |
|---|---|
| `/proc/*/cwd` scan and `ps` (start) | no stream process running |
| `git diff -- note.md`; reading `code/analyze_rev3.py`, `logs/summary_rev3.log`, `logs/check_rev3_comparison.log` | changes as described in Section 13 |
| `cd reviews/r4-code; timeout 900 python3 r4_control.py ../../logs > ../r4-logs/r4_control.log` | exit 0. Reads 73 files and 4350 records; 60 and 50 matched instances; `closed[0] = 0`; `oKs` = orbit through state `K`; 438 duplicates identical. It reproduces every 3–20, 5–20 and 10–20 contrast, the Holm12/Holm36 values, the SCIP remaining gaps and the deficit changes. It also reports Holm33, Wilcoxon p-values and rule − SCIP at round 20 (optional item 1). |
| `cd code; timeout 300 python3 analyze_rev3.py > ../reviews/r4-logs/rerun_analyze_rev3.log` | exit 0, ALL PASS; identical to `logs/summary_rev3.log`; empty stderr |
| `grep` over `note.md` for repair/recovery/asymmetry and the section list | the withdrawn reading remains only as a withdrawn item in the revision history; no open question about it |
| `/proc/*/cwd` scan (end) | no process of this stream or of mine running |

Not rerun: `reviews/r3-scripts/indep_rev2.py` (the author reran it; my own script covers the same
contrasts from the raw records), the loop runs, and the theory of Section 5, which this revision
did not change.
