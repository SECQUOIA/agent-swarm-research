# Confirmation check, round 2: revised bound audit

Date: 2026-09-30. Reviewed: `research-20260929/bound-audit/audit-report.md`,
as revised to address the eight problems in
`reviews/recheck-audit-confirm.md` (Section 10.2 of the report). I compared it
with the reviser's pre-revision copies in `/tmp/bound-audit-round1/`
(`audit-report.md` and the first `check_display.py`). My scripts and logs are
in `reviews/audit-confirm-r1-checks/`. I edited no audit file and no
root-maintained file. Nothing was committed.

## 1. Verdict

**All eight fixes are applied correctly.** I recomputed each one from the data
files with exact fractions and did not rely on the reviser's numbers. The one
"not applied" decision is sound.

**No class, count, margin or verdict changed, and no data file changed.**
Since the recheck backup, only `check_display.py` (10:58) and
`audit-report.md` (11:02) were modified. `summary.json` is byte-identical to
the backup.

**Nothing proven was strengthened.** The revision weakens the methanol50
claim, and all other changes add support or precision.

**Two small wording problems remain** (Section 4). Neither affects a proof, a
class or a verdict:
- the new status line says the third check "confirmed the revised text",
  although that check returned "fixes needed";
- the revision log (Section 10.2, item 5) states the emfl violation range
  without the qualifier that makes it true.

Because these are genuine, if minor, inaccuracies, the verdict is "fixes
needed". Both are one-line wording changes.

## 2. Each fix, checked from scratch

| # | issue | what I recomputed | result |
|---|---|---|---|
| 1 | "clear errors by any common tolerance" | From `results.json` (strongest point per pair): methanol50 LINDO d − f = 9.80411e-5, (d − f)/\|d\| = 0.012212, (d − f)/max(1, \|d\|) = 9.80411e-5, \|d\| = 0.00802826. glider100 (both solvers) d − f = 982587, 782.9 of \|d\|. topopt d − f = 25.0172, 0.708 of \|d\|. | Correct. Section 1 now limits the claim to gap tolerances measured against \|d\|, states the absolute margin (9.8e-5) and the max(1, \|d\|) margin (9.8e-5, below 1e-4), and says that the verdict for methanol50 depends on how the gap is measured. Section 7 says the same. The seven other gross pairs are below 1e-4 of \|d\|, so "only the four ... exceed such tolerances when the gap is measured against \|d\|" is right. Section 10.1, item 6, marks the old wording. |
| 2 | "eight of the ten solvers" / "For scale" | `pages.json`: 19 labels, 11086 duals (11031 finite). The ten labels in `results.json` hold 10321, with per-label counts exactly as listed. The other nine hold 765: ALPHAECP 358, XPRESS 316, PQCR 43, DynamicProgramming 21, Sven Mallach 17, Peter Hahn et.al. 7, Pajarito 1, TRIVIAL 1, and "Gurobi (using a MISOCP reformulation; by Miles Lubin and Emre Yamangil)" 1. The six small labels sum to 48. My own re-screen of `pages.json` (dual strictly beyond a listed point with listed infeas ≤ 1e-5) gives 158 pairs, all under the ten labels, and none under the other nine. | Correct. |
| 3 | two rounded "…" values | The verifier's variant A fraction in `reviews/bound-audit-verification/logs/nd_netgen_exact.log` (variant A is the "minimal u" point in its report) expands to 10729657.585117233985675…, so "10729657.585117233…" is a correct truncation. The ghg_3veh p2 ends in `logs/verify/ghg_3veh.p2.json` are 7.75400605004881504… and 7.75400605006432575…. Outward rounding at 14 decimals gives [7.75400605004881, 7.75400605006433], and at 12 decimals [7.754006050048, 7.754006050065]. | Correct. The numeric "…" values in the report are on lines 115, 119, 159, 161, 794, 795, 984 and 1125. All are truncations of exact values. |
| 4 | `check_display.py` weaker than described | I read the new script and ran it. It matches each "[lo, hi]" to the exact enclosure with the nearest lower end. It checks each "…" value as a truncation (toward zero, also for negative values), and each emfl "opt >=" / "≥" bound and the two "at least" differences against the exact L. It reports "≥ 0.1" as skipped. On the pre-revision report: new version ok 77, failed 9, skipped 1 (= 68 displays + 7 "…" values + 2 differences; failures = the 7 quotations + the 2 rounded values), and the first version gives ok 68, bad 7. On the current report: ok 84, failed 8, skipped 1. The 8 failures are the 7 quoted intervals and the verifier's nd_netgen value. | Correct, and the Section 9 and 10.1/10.2 descriptions now match the code. My negative controls (A–H below) confirm the claimed strictness. |
| 5 | emfl primal-section violation range | From `pages.json` and the exact L in `logs/cert_socp_*.json`, adding half a unit in the last shown digit to each listed value: the primal-section points with listed infeas below 1e-8 that lie below L are emfl050_3_3 p1 (1e-10), p2 (2e-10); emfl050_5_5 p1 (1e-10), p2 (8e-10), p3 (4e-11); emfl100_3_3 p1 (1e-10), p2 (2e-10); emfl100_5_5 p1 (1e-10). emfl050_5_5 p2 lies 2.252e-4 below L, and p3 lies 1.221e-4 below. | The Section 1 text is correct. The Section 10.2 wording is not quite (Section 4, item 2). |
| 6 | "five sssd*persp" | LINDO pair margins (strongest point): sssd20-04 7.33e-5, sssd22-08 6.93e-5, sssd25-04 3.41e-5, sssd25-08 1.24e-5, nuclear14 2.48e-5 of \|d\|. | Correct: four sssd*persp instances plus nuclear14, 1.2e-5 to 7.3e-5. |
| 7 | Section 8.2 "inside the enclosure given here" | [L, U] from `logs/cert_socp_*.json`, with U padded by 1e-14 and rounded outward at 10 decimals: emfl050_5_5 [18.9136329529, 18.9136329563]; emfl100_3_3 [18.1326531194, 18.1326531244]; emfl100_5_5 [32.6381903513, 32.6381903548]; emfl050_3_3 [10.4017521316, 10.4017521319]. `cert_socp.py` stores `str(float(ub))` with `ub` a Fraction, so the stored value is correctly rounded (within 1.8e-15 for values in [16, 32)). Each recheck interval, and the verifier's emfl050_3_3 interval, lies inside the exact [L, U] and inside the displayed enclosure. | Correct. |
| 8 | "quoted in this item" | Section 10.1, item 5 now names the ghg_3veh interval (quoted in item 1, also the recheck's suggestion) and the emfl100_5_5 interval (quoted in item 5). | Correct. |

**Negative controls** (`negative_controls.sh`, on copies in `/tmp`). Each
control changes one display in a copy of the current report. The new script
catches all eight. The first version catches only D–G:
- A: sssd22-08persp p4 interval widened to enclose p3 but not p4;
- B: a false "at least 1.43e-5" for emfl050_3_3;
- C: a "…" value rounded up in its last digit (watercontamination0303);
- D: an emfl050_3_3 "opt >=" bound 1e-11 too high;
- E: an sssd20-04persp lower end moved inward by 1e-10;
- F: the new Section 8.2 emfl050_5_5 upper end moved inward;
- G: a glider100 upper end moved inward (negative values);
- H: the nd_netgen "…" value rounded up.

**The previous round's independent script**
(`reviews/recheck-audit-confirm-checks/check_displays_indep.py`), rerun
read-only on the current report, passes 85 displays. Its failures are the
same quotations plus the Section 10.1, item 5, quotation labelled "upper end
to double precision", as Section 10.2 says. The displays new in this revision
(Section 8.2's two added enclosures and the 14-decimal ghg_3veh enclosure in
Section 10.1, item 1) pass both scripts and my `recompute.py`.

## 3. The "not applied" decision

For ghg_3veh, the reviser did not use the suggested truncation
"7.75400605006432…". Instead, Section 10.1, item 1 shows the enclosure rounded
outward at 14 decimals, without "…": [7.75400605004881, 7.75400605006433].
This is acceptable:
- The previous report offered it as an alternative ("or drop the '…' and say
  'rounded'").
- It matches the report's convention for enclosures.
- It removes the inconsistency that was the actual issue.

The recorded reason, that a truncated upper end lies below the exact end, is
correct.

## 4. Remaining problems

1. **The status line overstates the third check** (header, lines 3–4).
   - It reads: "a third check confirmed the revised text". The
     confirmation's verdict was "fixes needed". It confirmed the nine fixes
     after the recheck and the display rounding, and it found eight remaining
     text problems.
   - The status table row below states this correctly, so only the sentence
     is too strong.
   - Suggested text: "and a third check confirmed the fixes made after the
     second and found eight text problems, fixed in Section 10.2."
2. **The revision log's violation range needs its qualifier** (Section 10.2,
   item 5).
   - It says: "the emfl primal-section points with listed violation below
     1e-8 have listed violations from 4e-11 to 8e-10". emfl050_3_3 p3 is a
     primal-section point with listed infeas 3e-11, so as written the range
     is 3e-11 to 8e-10.
   - The range 4e-11 to 8e-10 holds only for the points that lie below the
     exact optimum. That is how Section 1 uses it ("This includes ..."), so
     Section 1 is correct.
   - Suggested text: "the emfl primal-section points with listed violation
     below 1e-8 that lie below the exact optimum have listed violations from
     4e-11 to 8e-10 (emfl050_3_3 p3, listed 3e-11, lies above the proven
     upper bound)".

## 5. Root-maintained notes (not edited; for the root agent)

These are outside the audit report, and I did not edit them.
`README.md` line 32 still says "14 of 19 confirmed", and
`root-research-log.md` line 231 still describes 14 of the 19 pairs as
confirmed. All 19 pairs and all four emfl instances are now confirmed
(Section 8 of the audit report). The other stale points listed in
`reviews/recheck-audit-confirm.md`, Section 6, were not rechecked here.

## 6. Commands run

All checks were targeted and read-only on the audit's data. Each finished in
seconds, single-threaded with OMP_NUM_THREADS=1. I ran no project-wide
verification, did not inspect CI, and did not rerun any certificate,
verification route, classification or download.

```
cd research-20260929/bound-audit
diff /tmp/bound-audit-round1/audit-report.md audit-report.md       # all changes are listed in Section 10.2
diff /tmp/bound-audit-round1/check_display.py check_display.py
find . -newer /tmp/bound-audit-prev/tables.md -type f               # only check_display.py and audit-report.md changed in this round
cmp /tmp/bound-audit-prev/summary.json summary.json                 # identical
python3 check_display.py                                            # ok 84, failed 8 (all quotations), skipped 1
cd ../reviews/audit-confirm-r1-checks
python3 recompute.py > recompute.log                                # items 1, 2, 3, 5, 6, 7
bash negative_controls.sh > negative_controls.log                   # item 4; copies in /tmp/audit-confirm-r1
python3 ../recheck-audit-confirm-checks/check_displays_indep.py > check_displays_indep_rerun.log
```

Read-only inspection also covered `cert_socp.py` (`primal_value`, and how the
upper bound is stored), `logs/verify/ghg_3veh.p2.json`,
`reviews/bound-audit-verification/logs/nd_netgen_exact.log` and its report
(variant A = minimal u), and `screen.json`.
