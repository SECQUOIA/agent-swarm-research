# Confirmation check of the revised bound audit

Date: 2026-09-30. Reviewed: `research-20260929/bound-audit/audit-report.md`
(revised after `reviews/bound-audit-recheck.md`). I compared it with the
reviser's pre-revision backup in `/tmp/bound-audit-prev/`, which holds the old
report, `results.json`, `results.csv`, `summary.json`, `summary.txt` and
`tables.md`. My scripts and logs are in `reviews/recheck-audit-confirm-checks/`.
I edited no audit file and no root-maintained file. Nothing was committed.

## 1. Verdict

**All nine fixes are applied correctly.** I recomputed each one from the data
files and did not rely on the reviser's statements. All the new numbers are
right:
- the ghg_3veh route and enclosure;
- the eight solvers with class (ii) pairs;
- the violation range 2e-10 to 1e-6;
- the squfl drop of 1e-5 to 5.5e-5;
- the dates;
- the factors of 3.0, 7.4 and at least 119 below 1e-6;
- the seven gross pairs at 1.24e-5 to 7.33e-5 of |d|;
- the glider100 altitude at node 1;
- the emfl listed-point claim;
- the "at least" differences.

**No class, count, margin or verdict changed.**
- In `results.json`, only `rigorous_opt_lower` changed.
- `results.csv`, `summary.json` and `logs/summary.txt` are byte-identical to
  the backup.
- In the Section 4 table, only the enclosure/bound column changed.

**Every displayed enclosure and bound of the audit's own results is now
rounded outward.** I checked this with my own script. It is stricter than the
audit's `check_display.py` (Section 3).

**Withdrawn claims are marked.** Each of the nine corrections is listed in
Section 10 of the report, with the old wording and the change.

**Remaining problems.** Eight small text problems remain (Section 5). None of
them affects a proof, a class or a verdict.
- The most substantive is new in this revision: the four pairs of glider100,
  topopt and methanol50 are called "clear errors by any common tolerance".
  For methanol50 that is too strong (item 5.1).
- Another is that the phrase "eight of the ten solvers" builds on a per-solver
  count that omits 9 of the 19 solver labels on the pages (item 5.2).

Because of these small text problems, the verdict is "fixes needed". The fixes
are wording changes only.

## 2. Each fix, checked from scratch

| # | issue | what I recomputed | result |
|---|---|---|---|
| 1 | ghg_3veh p2 called exactly feasible | `logs/verify/ghg_3veh.p2.json`: route "B (polish + Krawczyk)", `route_A_failure` "row e1 (exact value off by 5e-14)", enclosure [7.7540060500488150…, 7.7540060500643257…]. Outward rounding at 12 decimals gives [7.754006050048, 7.754006050065]. | Correct. The recheck's suggested [7.754006050049, 7.754006050064] is indeed inward at both ends, so the reviser was right not to use it. `sanity.py` calls the same `verify_point`, and its logged enclosure equals route B's. So "through route B" in Section 3.4 is right, although `logs/sanity.log` does not record the route itself. |
| 2 | "(ii) involves every solver; not errors" | Class (ii) pairs from `results.json`: ANTIGONE 4, BARON 10 + 4 proven, COUENNE 9, CPLEX 8, GUROBI 9, LINDO 11 + 4, SCIP 11 + 4, SHOT 1. That is 63 repair and 12 proven pairs over 8 solvers; AOA and BONMIN have none. Exact violations of the (ii) points run from 1.98e-10 (emfl050_3_3 p2) to 9.97e-7. The squfl drop relative to the repair is 1.02e-5 to 5.53e-5. | Correct. The text no longer says the duals are valid. It says validity is proven only for emfl*, and that (ii)-repair is evidence. The count "ten" is discussed in 5.2. |
| 3 | methanol50 p3 "earlier" | `pages.json`: methanol50 p3 and LINDO's dual are both dated 15 Feb 2022. glider100 p1 is dated 15 Aug 2014, against LINDO's 16 Aug 2014. The sssd p2 points are dated 28 Feb 2014, against LINDO's 02 Mar 2014, which is 2 days later. | Correct. |
| 4 | Section 7 dates | ghg_3veh bounds: 26 Sep 2013 (ANTIGONE) and 16 Aug 2014 (BARON). glider100 bounds: 16 Aug 2014 (LINDO) and 25 Jun 2015 (COUENNE). Points: ghg p1 29 Aug 2011, ghg p2 06 Mar 2015, glider p1 15 Aug 2014, glider p2 16 Mar 2022. topopt LINDO bound: 15 Feb 2022; p4 31 Jul 2025, p5 07 Aug 2025. | Correct. The added model-identity evidence is also right: all four sssd p2 points repair to within the display slack of LINDO's numbers (`reviews/bound-audit-recheck/logs/sssd_p2.log`, differences 6e-6 to 4.6e-5). The glider100 and ghg_3veh p1 points satisfy the current files to 1.1e-11 and 4.9e-13 (first verification). |
| 5 | outward rounding | See Section 3. The float `rigorous_opt_lower` was above the exact bound by 1.1e-15 (emfl100_3_3) and 3.9e-15 (emfl100_5_5), and below it for the other two. The new `audit.py classify` stores floor(10^30 L)/10^30 as a string. `make_tables.py` uses ROUND_FLOOR/ROUND_CEILING at 13 significant digits. I regenerated both `logs/tables.md` and the Section 4 table in `/tmp`, and they match exactly. Before the fix, nearest rounding put the nd_netgen upper end 9.1e-7 inward. | Correct. |
| 6 | caveat for 7 gross pairs | Relative margins: sssd20 7.33e-5, sssd22 6.93e-5, ghg_3veh 4.11e-5 (×2), sssd25-04 3.41e-5, nuclear14 2.48e-5, sssd25-08 1.24e-5. | Correct, and stated in Sections 1, 5, 6 and 7. See 5.1 and 5.6 for new wording that came with this fix. |
| 7 | "far below 1e-6" | 1e-6 divided by the relative margin: nd_netgen GUROBI 3.01, CPLEX 7.43, smallinvDAX*150-165 119, *200-220 140, watercontamination0303 418 (LINDO) and 523 (BONMIN). | Correct. The non-error reading is labelled as a judgment, and the text says the run settings are unknown. |
| 8 | glider100 altitude | `sol/glider100.p2.sol`: x103 = 1000, and x104 is absent, so it is 0. In the OSIL file, x104 has no bounds attribute, so its lower bound is the default 0. The block reaches its maximum of 64580.17 at node 55 and ends at x203 = 900. In the audit's proof centre, x104 = 1e-10. x104 is non-basic there, so the exact point has that value. Route C shifted the point by t = 1.755e-10. The first verifier's proof fixes y₁ = 0 on its bound (`verification-report.md`, Section 3.4). | Correct. |
| 9 | header, Rigor, Section 8 | First verification: 14 pairs, the ones named in Section 8.1. Recheck: 5 pairs over 7 points, and the emfl050_5_5, emfl100_3_3 and emfl100_5_5 bounds. Together they cover all 19 pairs. The header table, the Rigor paragraph and Sections 8.1–8.3 match both review reports. | Correct. |

**The added emfl statement (Section 1) is also correct.** I compared each
listed value, plus half a unit in its last shown digit, with the exact lower
bound L from `logs/cert_socp_*.json`.
- Every listed point of emfl050_5_5, emfl100_3_3 and emfl100_5_5 lies below
  L. So do all points of emfl050_3_3 except p3, and p3 lies above the proven
  upper bound.
- emfl050_5_5 p3 (listed infeas 4e-11) lies 1.22e-4 below L.
- The largest relative gaps are 1.05e-4 for the 1e-8 points and 4.3e-4 for
  the "other" points.
- Every listed dual of the four instances is at or below L.
- The two differences hold as "at least" statements: L − 10.40173793 =
  1.4202e-5 ≥ 1.42e-5, and L − 32.63818348 = 6.8714e-6 ≥ 6.87e-6.

**The reviser's "not applied" decisions are sound.**
- Using the outward ghg_3veh interval instead of the suggested one is
  correct.
- Keeping margins, ratios and point values rounded to nearest is acceptable
  now that Section 1 states the convention.
- The list of stale root notes is accurate (Section 6).
- The verifier's report does say "the altitude rises from 1000 m" at line
  178.

## 3. Displayed enclosures and bounds

`check_displays_indep.py` matches each "[lo, hi]" in the report to its
intended exact quantity: the one whose exact lower end is nearest to lo. It
then requires lo ≤ exact lo and exact hi ≤ hi. It also checks that each value
ending in "…" is a truncation of an exact value, and it checks every "≥",
"opt >=" and "at least" statement. The results are in
`check_displays_indep.log`.

- **The audit's own displays all pass.** This covers:
  - every enclosure in Sections 1, 4, 5 and 6, and in the Section 8 lines
    that refer to this audit;
  - every "opt >=" and "≥" lower bound;
  - both "at least" differences;
  - the truncated nd_netgen and watercontamination0303 exact values.
- **The failures are all quotations**, the same seven that `check_display.py`
  lists:
  - the first verifier's emfl050_3_3 interval and glider100 repair;
  - the recheck's three emfl intervals;
  - the recheck's suggested ghg_3veh interval;
  - the old emfl100_5_5 display.

  The Section 10 quotation "[32.638190351378666…, 32.63819035472937]" also
  fails my padded upper end. That is expected, because it is labelled "upper
  end to double precision".
- **Two "…" values are rounded, not truncated.** Section 1 says "…" marks a
  truncated exact rational (see 5.3).
- **`check_display.py` is weaker than its description.** It accepts an
  interval if it encloses *any* audit quantity, not the intended one. It also
  does not test "…" values or the "at least" differences. The stricter check
  gives the same verdict for every audit display, so no statement is affected
  (see 5.4).

## 4. Strengthened claims

I diffed the old and new report outside the Section 4 table.
- Every changed passage is listed in Section 10.
- No proven claim was strengthened without new support.
- The new claims are:
  - the emfl listed-point statement: verified above;
  - the "at least" differences: verified above;
  - "all 19 confirmed": verified above;
  - the four "clear errors by any common tolerance": see 5.1.

## 5. Remaining problems

1. **"Clear errors by any common tolerance" is too strong for methanol50**
   (new; Section 1, gross bullets, and Section 7, "Size of class (i)").
   - The statement holds for glider100 and topopt.
   - For methanol50, |d| = 0.008 and the absolute margin is 9.8e-5. Relative
     to max(1, |d|), which is the measure this report used before and still
     cites in Section 1, the margin is 9.8e-5. That is just below 1e-4.
   - So whether methanol50 exceeds a "common tolerance" depends on how the gap
     is normalized.
   - Suggested text: "are clear errors under relative gap tolerances measured
     against |d| (methanol50: 1.2% of |d|; its absolute margin is 9.8e-5)".
2. **"Eight of the ten solvers" and the "For scale" line (Section 5).**
   - `pages.json` has 19 solver labels. The "For scale" sentence lists only the
     ten with flagged pairs, which hold 10321 of the 11086 duals.
   - It omits ALPHAECP (358 duals, more than BONMIN's 348), XPRESS (316),
     PQCR (43) and six small labels (48 duals).
   - As written, it reads as the complete per-solver list, and "the ten
     solvers" inherits that reading.
   - Suggested text: "eight of the ten solvers with flagged pairs". In the
     "For scale" line, add: "ALPHAECP 358, XPRESS 316 and 7 other labels
     (91 duals) have no flagged pair."
   - The omission predates this revision, but the new phrase depends on it.
3. **Two "…" values do not follow the stated convention** ("A value ending in
   '…' is an exact rational, truncated").
   - Section 10 item 1 gives the upper end as "7.75400605006433…". The exact
     value is 7.7540060500643257…, so the display is rounded up. That is
     harmless as an upper bound, but it is not a truncation.
   - Section 8.1 gives the first verifier's value as "10729657.585117234…".
     The exact value is 10729657.585117233985…
   - Suggested text: "7.75400605006432…" and "10729657.585117233…", or drop
     the "…" and say "rounded".
4. **`check_display.py` (Section 9 and Section 10 item 5).**
   - Its matching accepts any enclosed audit quantity, and it skips "…" values
     and "at least" statements. So "tests every interval and lower bound shown
     in this report against the exact values" overstates it.
   - It also prints "lower bound not matched line 139 ≥ 0.1" for the
     histogram row. That output is harmless, but the report does not mention
     it.
   - Suggested fix: match by instance or nearest lower end (as in
     `reviews/recheck-audit-confirm-checks/check_displays_indep.py`), or
     describe the check as it is.
5. **Primal-section violation range (Section 1, emfl bullet).** "Primal-section
   points with listed violation 4e-11 to 2e-10" leaves out emfl050_5_5 p2
   (primal, listed 8e-10, 2.25e-4 below L). The range below 1e-8 is 4e-11 to
   8e-10. The wording comes from the recheck.
6. **Ambiguous count (Section 5, LINDO).** "The five sssd*persp and nuclear14
   margins" can be read as five sssd instances. There are four. Suggested
   text: "The four sssd*persp margins and the nuclear14 margin".
7. **Section 8.2, "inside the enclosure given here".** The report shows no
   upper ends for emfl050_5_5 and emfl100_3_3, only "opt >=" and "≥".
   - Either cite `logs/cert_socp_*.json`, or show the enclosures.
   - Outward-rounded, they are [18.9136329529, 18.9136329563] and
     [18.1326531194, 18.1326531244].
   - emfl050_3_3 and emfl100_5_5 are shown in Section 6.
8. **Section 10 item 5, last sub-bullet.** It says both non-review failures
   are "old inward-rounded displays quoted in this item". One of them,
   [7.754006050049, 7.754006050064], is quoted in item 1. It is both the old
   display and the recheck's suggestion.

## 6. Root-maintained notes (not edited; for the root agent)

The reviser's list is accurate.
- `SYNTHESIS.md` lines 256–259, `README.md` line 32,
  `open-instances-summary.md` lines 50–57 and `root-research-log.md` lines
  214–234 still say that 14 of 19 pairs are confirmed.
  - All 19 pairs and all four emfl instances are now confirmed.
- `SYNTHESIS.md` names ghg_3veh first among the gross errors, without the
  caveat that 7 of the 11 gross pairs are below 1e-4 of |d|.

Two more stale points in `open-instances-summary.md`:
- **Lines 58–62.** The gross list lacks the 1e-4 caveat for sssd ×4,
  nuclear14 and ghg_3veh ×2.
- **Lines 66–70.**
  - "They remain solved under MINLPLib's 1e-6 rule" is stronger than the
    audit's "do not contradict the S mark".
  - "Up to 1e-4 relative" is now incomplete. "Other" points lie up to 4.3e-4
    below. Every listed emfl point except emfl050_3_3 p3 lies below the exact
    optimum.
  - "By 1.4e-6" for emfl050_3_3 is relative. The absolute difference is at
    least 1.42e-5.

## 7. Commands run

All checks were targeted and read-only on the audit's data. Each finished in
seconds, single-threaded with OMP_NUM_THREADS=1. I ran no project-wide
verification, did not inspect CI, and did not rerun any certificate,
verification route or download.

```
cd research-20260929/bound-audit
cmp /tmp/bound-audit-prev/{results.csv,summary.json} . ; cmp /tmp/bound-audit-prev/summary.txt logs/summary.txt   # identical
python3 -c '...'                          # field-by-field diff of results.json against the backup: only rigorous_opt_lower
python3 check_display.py                  # ok 68, bad 7 (all quotations), as the report says
python3 make_tables.py > /tmp/recheck_confirm_tables.md   # identical to logs/tables.md and to the Section 4 table
python3 summarize.py > /tmp/recheck_confirm_summary.txt   # identical to logs/summary.txt; summary.json unchanged
diff (old report) (new report)            # all changes accounted for in Section 10
cd ../reviews/recheck-audit-confirm-checks
python3 check_displays_indep.py > check_displays_indep.log
python3 recompute_fixes.py > recompute_fixes.log
```

Read-only inspection also covered:
- `logs/verify/{ghg_3veh,glider100}.p2.json` and `logs/sanity.log`;
- `sol/glider100.p2.sol`, `logs/verify/glider100.p2.center.sol` and the
  glider100 OSIL variable bounds;
- `logs/cert_socp_*.json`, `pages.json` and the `audit.py` classify code;
- `reviews/bound-audit-recheck/logs/sssd_p2.log`;
- the first verification report, Sections 3.2 and 3.4.
