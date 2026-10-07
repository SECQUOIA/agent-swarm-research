# Confirmation check, round 3: revised bound audit

Date: 2026-09-30. Reviewed: `research-20260929/bound-audit/audit-report.md`,
as revised to address the two wording problems in
`reviews/audit-confirm-r1.md` (a file titled "round 2"; the report's Section
10.3). I compared the report with the reviser's pre-revision copy in
`/tmp/bound-audit-round2/audit-report.md`. My script and logs are in
`reviews/audit-confirm-r2-checks/`. I edited no audit file and no
root-maintained file. Nothing was committed.

## 1. Verdict

**Verified.** Both fixes are applied correctly, and I found no remaining
problem in the report.

- I recomputed the emfl numbers from `pages.json` and
  `logs/cert_socp_*.json` with exact fractions. I did not rely on the
  reviser's figures.
- **Only the report changed in this round.** No file in `bound-audit/`
  other than `audit-report.md` is newer than the pre-revision copy.
  `check_display.py` was last changed at 10:58, in round 1. The data files
  date from 08:19 to 08:36.
- **The diff contains only the changes the reviser lists.** They are:
  - the header status line;
  - the new status-table row;
  - the "Revised after confirmation round 1/2" paragraphs;
  - the Section 9 run status;
  - the qualifier in Section 10.2, item 5;
  - the new Section 10.3.

  No other line changed.
- **Nothing was strengthened.** One change weakens a claim (the header
  sentence about the third check). The other narrows a range statement to
  the set it holds for. The remaining changes are record-keeping.
- The reviser listed no "not applied" items.

## 2. Each fix, checked from scratch

### 2.1 Header status line (lines 3–7)

- The new text says that a third check confirmed the fixes made after the
  second and found eight text problems, fixed in Section 10.2. This matches
  `reviews/recheck-audit-confirm.md`: it returned the verdict "fixes needed",
  confirmed the nine post-recheck fixes and the outward display rounding,
  and listed eight text problems.
- The new text says that a fourth check confirmed those eight fixes and
  found two wording problems, fixed in Section 10.3. This matches
  `reviews/audit-confirm-r1.md`: it returned "fixes needed", found all eight
  fixes correct, and listed exactly two wording problems.
- The new status-table row matches that report. It confirmed the eight
  fixes by recomputing them from the data files, and it confirmed the
  stricter `check_display.py` with negative controls A–H. The note
  `(titled "round 2")` resolves the mismatch between the file name and the
  title.
- The paragraph "Revised after confirmation round 2" says "no number, class
  or verdict changed, and no code or data file changed". The diff and the
  file times confirm this. The revision adds numbers only in the revision
  log (Sections 10.2 and 10.3) and changes none.

### 2.2 Section 10.2, item 5 (violation range)

I placed each emfl listed point relative to the exact bounds
(`emfl_points.py`). Each displayed value was widened by half a unit in its
last shown digit. "Below L" uses the 30-digit rounded-down lower bound, which
is at most the exact L. "Above U" uses the stored upper bound, which is
within 2e-15 of the exact value.

| instance | primal-section points with listed infeas < 1e-8 | position |
|---|---|---|
| emfl050_3_3 | p1 (1e-10), p2 (2e-10) | below L by at least 1.21e-5 and 1.42e-5 |
| emfl050_3_3 | p3 (3e-11) | above U by at least 4.913e-5 |
| emfl050_5_5 | p1 (1e-10), p2 (8e-10), p3 (4e-11) | below L by at least 1.98e-4, 2.252e-4, 1.221e-4 |
| emfl100_3_3 | p1 (1e-10), p2 (2e-10) | below L by at least 2.87e-5, 2.12e-6 |
| emfl100_5_5 | p1 (1e-10) | below L by at least 6.87e-6 |

- The list of points in Section 10.3, item 2, is complete and correct.
- The range is 3e-11 to 8e-10 over all nine points, and 4e-11 to 8e-10 over
  the eight that lie below the exact optimum. The revised Section 10.2,
  item 5, now states the second range with the qualifier "that lie below
  the exact optimum". It names emfl050_3_3 p3 as the exception, and it says
  that the qualifier was added in round 2. All of this is correct.
- "At least 4.9e-5 above the proven upper bound" (Section 10.3) is correct:
  the computed value is 4.913e-5.
- "At least 2.25e-4 below the exact lower bound" (emfl050_5_5 p2) is
  correct: the computed value is 2.252e-4.
- Section 1 was left unchanged, which is correct. Its range follows "This
  includes" and refers to points below the exact optimum. "1.2e-4 below"
  for emfl050_5_5 p3 matches the computed 1.221e-4, and "2.25e-4 below" for
  p2 matches 2.252e-4. Section 1 does not claim that the range covers all
  such points, so the 1e-8 points (emfl050_5_5 p6 and emfl100_3_3 p4) do
  not contradict it.

### 2.3 Section 9 run status

The run status says that after confirmation rounds 1 and 2 only
`check_display.py` was rerun. This is consistent with the file times. No
pipeline script, verification, certificate or download was rerun. Round 1
also ran the previous reviewer's independent script and negative controls
on copies in `/tmp`, and Section 10.2 lists those commands. They are not
reruns of this audit's pipeline, so the statement is accurate.

### 2.4 Section 10.3

- The entries correctly describe both problems, how each was verified, and
  the changes made.
- The recorded `check_display.py` result, "ok 84, failed 8, skipped 1",
  holds before and after the change. I ran the script on the current report
  and on a copy of the pre-revision report in `/tmp/audit-confirm-r2/before/`
  (with the same `results.json` and `logs/cert_socp_*.json`).
- Apart from line numbers, the two outputs are identical. The eight
  failures are the known quotations:
  - the five review intervals (the first verifier's emfl050_3_3 interval,
    its glider100 repair, and the recheck's three emfl intervals);
  - the two old inward-rounded displays quoted in Section 10.1 (ghg_3veh and
    emfl100_5_5);
  - the first verifier's nd_netgen value in Section 8.1.

  The one skipped display is the "≥ 0.1" histogram row.

## 3. Remaining problems

None in the audit report.

## 4. Root-maintained notes (not edited; for the root agent)

These notes are outside the audit report, and I did not edit them. The
previous round flagged them, and both are still stale:
- `README.md` line 32 still says "(14 of 19 confirmed)";
- `root-research-log.md` line 231 still says that the audit verification
  confirmed 14 of the 19 pairs.

All 19 class (i) pairs and all four emfl instances are now confirmed
independently (audit report, Section 8).

## 5. Commands run

All checks were targeted and read-only on the audit's data. Each finished in
seconds, single-threaded with OMP_NUM_THREADS=1. I ran no project-wide
verification, did not inspect CI, and reran no certificate, verification
route, classification or download.

```
cd research-20260929/bound-audit
diff /tmp/bound-audit-round2/audit-report.md audit-report.md     # only the listed changes
find . -newer /tmp/bound-audit-round2/audit-report.md -type f    # only audit-report.md
python3 ../reviews/audit-confirm-r2-checks/emfl_points.py > ../reviews/audit-confirm-r2-checks/emfl_points.log
python3 check_display.py > ../reviews/audit-confirm-r2-checks/check_display_after.log      # ok 84, failed 8, skipped 1
# same script on a /tmp copy of the pre-revision report, results.json and logs/cert_socp_*.json:
(cd /tmp/audit-confirm-r2/before && python3 check_display.py) > ../reviews/audit-confirm-r2-checks/check_display_before.log   # ok 84, failed 8, skipped 1
```

I also read `reviews/recheck-audit-confirm.md` and
`reviews/audit-confirm-r1.md` to check the header and the status-table rows.
