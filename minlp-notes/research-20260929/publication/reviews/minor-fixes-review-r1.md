Verdict: issues

# Review of the minor-issue fixes (round 1)

Reviewer: independent verifier. Date: 2026-10-03. Scope: the 57 minor issues listed in `reviews/minor-fixes/summary.md`, the four script changes, the seven point-JSON edits, the report diffs, and the integration list in `summary.md`. All paths below are relative to `research-20260929/publication/` (P) unless they start with `research-20260929/`.

## Summary

All 57 fixes are present in substance. All four script changes and all seven JSON edits are minimal and change no numerical result. Recomputation confirmed every corrected number except one: the water-ann-kan rounding claim in issue 4. Recomputed values include the chain safe-display gaps, the lnts Krawczyk widths, the powerflow slacks and displays, the water bound violations, the audit digit counts, the eg leaf counts, the SCIP 0/122 and 78/122 totals, and the camshape bound differences. The literature corrections match the saved sources.

The verdict is "issues" for three reasons:

- **Two invalid displays in the main summary.** The main summary displays two primal values below the exactly feasible point's objective (lnts100 and dtoc5). The integration list does not correct them, and the lnts report says the displays "remain valid upper bounds". These displays were wrong before this revision, but the integration step would carry them into the paper.
- **One incorrect fix.** The water-ann-kan fix says all displayed gaps are rounded upward. One gap (waterno2_12) is rounded down.
- **Minor problems.** There are 19 smaller problems: incomplete integration bullets, statements the fixes left stale, stale logs and comments, and small source-citation errors.

There are no blockers, 3 major issues and 19 minor issues.

## Issues

### Major

1. **lnts100: the main-summary primal display is not an upper bound, and the report says it is** (major)
   - **Location:**
     - `research-20260929/open-instances-summary.md:18` shows the primal display 0.5545954011669.
     - `primal/lnts/report.md:83` says: "The displayed primal values (e.g. 0.5546687649387) remain valid upper bounds."
     - `reviews/minor-fixes/summary.md` makes no change to the lnts primal displays.
   - **Evidence:** The objective enclosure in `primal/lnts/points/lnts100_point.json` is [0.5545954011669111610017828, …829]. The display is therefore 1.12e-14 below the point's value. The old double-precision point was also above the display. Group A checked the other values:
     - The lnts50, lnts200 and lnts400 primal displays are valid upper bounds.
     - All four dual displays lie below the certified N·h2.
   - **Fix:**
     - Display 0.5545954011670 for lnts100.
     - Restrict the sentence at `report.md:83` to lnts50, lnts200 and lnts400, or reword it after the correction.
     - Add the change to the integration list.

2. **dtoc5: the main-summary primal display lies below the point value and below the certified dual** (major)
   - **Location:**
     - `research-20260929/open-instances-summary.md:21` shows 5.38967211918114 in both the dual and primal columns.
     - The integration list does not mention it.
   - **Evidence:**
     - `primal/dtoc5-lukvle10/report.md:13` gives the exact objective enclosure as 5.3896721191811404674239664991… ≤ f ≤ …8314.
     - The verifier dual's lower end is 5.38967211918114046742396472…
     - As a primal display, 5.38967211918114 is about 4.67e-16 below the point value. It is valid only as the dual display.
     - The gap entry "< 1e-14" remains true; the rigorous gap is 4.675e-16.
   - **Fix:**
     - Add an integration item: show the primal as 5.389672119181141, or as 5.38967211918115 at 14 decimals.
     - Add the item to `summary.md:12` and to the dtoc5 rows.

3. **water-ann-kan issue 2: the rounding direction is misstated, so the fix is incorrect** (major)
   - **Location:**
     - `primal/water-ann-kan/report.md:28` says the gaps "10.82%, 6.89%, 4.87% and 5.90%" are "conservative upper bounds" and that "Rounding is upward".
     - The integration cell in `reviews/minor-fixes/summary.md`, issue row water 2, says "treat displayed gaps as conservative upper bounds".
   - **Evidence:**
     - For waterno2_12 the gap is 144.0667802 and gap/dual = 6.8939570e-2 (`scratch-C/gap_check.log`). The display 6.89% is below the exact value; it is rounded to nearest.
     - The other three gaps are rounded upward.
     - The author's check prints "PASS … conservative gap rounding" but does not test the displayed gaps.
   - **Fix:**
     - Display 6.90%. Alternatively, give nearest values throughout (10.81%, 6.89%, 4.87%, 5.89%) and drop "upper bounds".
     - Update the summary.md cell to match.

### Minor: integration list (`reviews/minor-fixes/summary.md`)

4. **The chain gap "≤ 1.0e-14" in the main summary is false for chain100, and the list does not correct it** (minor)
   - **Location:**
     - `research-20260929/open-instances-summary.md:33`.
     - `summary.md:13` and the chain row 1 cell say "no main-table range correction".
   - **Evidence:**
     - For chain100, the exact gap f_hi − L is 1.00276e-14.
     - For chain400 it is 9.77e-15 against the exact L, and 1.01e-14 against the display.
     - The chain report's own suggested edits already use 1.01e-14 (`primal/chain/report.md:154`).
   - **Fix:** Add an integration item: change the main-summary chain gap to ≤ 1.01e-14.

5. **The eg bullet names the wrong instance and calls boxes leaves** (minor)
   - **Location:** `summary.md:16`.
   - **Evidence:**
     - "eg_all" is not the eg-recheck instance. MINLPLib has a different instance, eg_all_s, which SCIP closes. The eg-recheck track concerns eg_disc2_s.
     - The bullet also says "the earlier 1,152,830 processed-leaf count". 1,152,830 is processed boxes; the report itself (`eg-recheck/report.md`, Section 10) says "1,152,830 processed boxes, 1,114,361 leaves".
   - **Fix:** Write "For eg_disc2_s …" and "1,152,830 processed boxes".

6. **The audit bullet omits the slack floor** (minor)
   - **Location:**
     - `summary.md:15` and the audit-ir row 2 cell.
     - `research-20260929/bound-audit/audit-report.md:271–279`.
   - **Evidence:**
     - The audit's slack is "never less than half a unit in the 10th significant digit". That floor was justified by the 10-significant-digit display limit, which the integration note now drops.
     - Group C re-derived all classes from `results.json` with and without the floor:
       - The classes are identical either way (22 (i), 17 (i-r), 63 (ii), 26 (ii, proven), 30 (iii)).
       - The floor changes the slack of 0 of the 158 screened pairs. It affects only 17 tie pairs, on fac1, fac2 and waternd_fosspoly0.
     - The author's "no class or count changes" therefore holds.
   - **Fix:** Add to the bullet: "The 10th-significant-digit slack floor no longer follows from a display limit. Keep it as an explicit conservative choice; it changes no screened pair."

7. **The MINOTAUR dtoc5 default-bound cell repeats a misdescribed rule** (minor). See issue 13; the fix also belongs in the cell for control row 2.5.

### Minor: track reports (statements left stale or inexact by the fixes)

8. **primal/lnts: the verifier duals are called "the full value" but are rounded to nearest** (minor)
   - **Location:** `primal/lnts/report.md:17, 19, 114`.
   - **Evidence:** Two of these values are 16-digit round-to-nearest displays above the certified N·h2:
     - lnts100: 0.5545954011663566 is 3.44e-17 above N·h2.
     - lnts200: 0.5545770161025291 is 4.96e-18 above N·h2.
     - The gaps are unchanged at 3 significant digits.
   - **Fix:** Call these values rounded displays, or round them down.

9. **primal/lnts: the "upward rounding" statement is not followed consistently** (minor)
   - **Location:** `primal/lnts/report.md` (Section 1 and the integration note) and the integration list.
   - **Evidence:**
     - "5.5e-13" rounds the exact 5.546e-13 to nearest; rounded upward it is 5.6e-13, or the table's own 5.55e-13 at 3 digits.
     - "5.8e-13–6.2e-13" starts above the exact low end, 5.789e-13.
     - "3.25e-15–3.54e-15" rounds 3.5437e-15 down. The body's "within 3.6e-15" is correct.
   - **Fix:** Round these values upward, or label them as approximate.

10. **primal/lnts: weak argument and stale file list** (minor)
    - **Location:** `primal/lnts/report.md:57`, and the Files section (Section 7).
    - **Evidence:**
      - Line 57 argues that no fully rational point exists. That cos θ is transcendental does not prevent Σ w cos θ from being rational, and θ = 0 is not covered. The claim is true, but the r1 review's linear-independence proof is the valid argument.
      - `logs/lnts_primal_50_100_200_400.json` and `logs/run_all.stdout` were written by the pre-change script, and the report does not say so. Group A reran the changed script on a scratch copy (5.6 s), and it reproduced all four point files byte for byte.
      - The Files section omits `minor_review_check.py` and its log.
    - **Fix:**
      - Cite or use the r1 linear-independence proof at line 57.
      - Note that the logs predate the centre change and that a rerun reproduces the point files.
      - List `minor_review_check.py` and its log in Section 7.

11. **primal/chain: the list of documents with over-rounded displays is incomplete** (minor)
    - **Location:** `primal/chain/report.md:24–26`.
    - **Evidence:**
      - `reviews/solver-campaign-review-r1.md:43` and `solver-runs/report.prev.md:39` also present 5.072261493982863 as certified. `reproduction/` also shows the value, but with a caveat.
      - The COPS verification report shows the values in a bullet list, not in "two tables".
    - **Fix:** Add the two files to the list, and describe the verification report's display correctly.

12. **primal/dtoc5-lukvle10 and primal/powerflow: wording** (minor)
    - **Location:** `primal/dtoc5-lukvle10/report.md:127`, `primal/dtoc5-lukvle10/report.md:20` and `primal/powerflow/report.md:44`.
    - **Evidence:**
      - **dtoc5 report, line 127:** it still refers to "the claim that the KKT point is a local minimizer". That text predates this revision, but the fix for issue 2 removed the claim, and line 95 says no optimality proof was attempted.
      - **dtoc5 report, line 20:** "The row violation is 3.48e-15" should say this is p5's maximum row violation.
      - **powerflow report, line 44:** it attaches the next-smallest slacks 4.3e-4, 1.08e-3 and 2.3e-3 all to 0039r. They belong to 0030p (e215), 0039p (e346) and 0039r (e306), one per instance. Group B's recomputation confirms the corrected 0039r values: e363 at 6.8e-13 and e386 at 2.1e-13.
    - **Fix:** Reword or delete line 127, qualify line 20, and split the sentence at line 44.

13. **literature/control issue 2.5: the MINOTAUR default-bound rule is misdescribed and the inference is overstated** (minor)
    - **Location:** `literature/control/report.md:296, 531, 698`, the response row, and the summary.md cell.
    - **Evidence:**
      - `QuadHandler_master_r2.cpp` (`addDefaultBounds`) does not scale "the largest finite bound magnitude". The lower default comes from the smallest finite lower bound and the upper default from the largest finite upper bound. Each is scaled by 100, or set to ∓1000 when that bound is near zero.
      - In dtoc5, 99,998 variables appear in quadratic terms and only x50001 is bounded, so both warnings should count 99,997. The log shows 99,997 for upper bounds but 99,983 for lower bounds. So 14 more variables already had finite lower bounds, probably derived in presolve, and the lower default cannot be inferred even for the master source.
      - The conclusion still holds: the rule always gives a negative lower default, and every coordinate of the reference point lies in [1.46e-5, 8.057].
    - **Fix:** Describe the rule correctly, and state that only the upper default [·, 100] is inferable. The containment argument needs only the sign of the lower default.

14. **literature/control issue 2.1: stale log and README** (minor)
    - **Location:** `literature/control/checks/qplib_camshape_compare.log` and `checks/README.md:30`.
    - **Evidence:**
      - The log is dated 2026-10-02, before the script change on 2026-10-03. It still shows lower-bound-only maxima, and 8.921e-11 for the QPLIB_2703 point instead of 4.7078e-10 at x1.up.
      - The README still says "all <= 2.5e-10".
      - The report cites the script for 4.7e-10, but the correct numbers exist only in `minor_review_check.log`.
      - The script change itself is correct (issue 2.1 in the table below).
    - **Fix:** Rerun the script (seconds) to refresh the log, and update the README.

15. **literature/network: one unqualified novelty claim remains** (minor)
    - **Location:** `literature/network/report.md:135`, in the powerflow0030p subsection.
    - **Evidence:** It says: Present ours as "the first rigorous certificate". Lines 30, 60 and 368 add "for this MINLPLib model". Without the qualifier, the sentence conflicts with the Oustry et al. 2022 certified ACOPF bounds that the fix for issue 3 added.
    - **Fix:** Add "found for this MINLPLib model".

16. **literature/network: two citation errors** (minor)
    - **Location:** `literature/network/report.md:114, 268` and `literature/network/report.md:61`.
    - **Evidence:**
      - **Müller–Serrano–Gleixner (lines 114, 268):** these lines cite pp. 42, 48, 56, 59, 69 and 72 for the 1800 s time-limit results. Only Table 5 (pp. 69, 72) shows the time limit. pp. 42/48 hold Table 3 statistics and pp. 56/59 hold Table 4 root-gap results.
      - **Göß (line 61):** it says "Göß et al. 2026". The paper (arXiv:2603.16505) has one author, Adrian Göß.
    - **Fix:** Cite pp. 69 and 72 only, and write "Göß 2026".

17. **scip-bug issue 2: two mechanism sentences are not restricted to the instrumented seeds** (minor)
    - **Location:** `scip-bug/report.md:243` and `scip-bug/report.md:38`.
    - **Evidence:**
      - Line 243 still says "All traced cutoffs involve the 0.7 station". The review asked for exactly this sentence to be restricted.
      - Line 38 says "It has the same cause", which is shown only for the instrumented seeds 8 and 14.
      - The response row claims all common-mechanism claims were restricted.
      - Seed 11's recorded behaviour is correctly described elsewhere: its first loss is b35 ≥ 1 at node 2, and b35 is the 0.85-station pump.
    - **Fix:** Write "All instrumented cutoffs in Section 5.3 …" at line 243 and "In the instrumented seeds (8, 14) …" at line 38.

18. **scip-bug issues 3 and 5: stale or general statements remain** (minor)
    - **Location:** `scip-bug/report.md:36` and `scip-bug/report.md:173`.
    - **Evidence:**
      - Line 36 still calls the case with claims of 55.69 or 65.12 "a real error, not a tolerance effect". Section 6 now says the 55.69 claims are not refuted.
      - Line 173, "So no consistent reading of the model makes SCIP's answers right", generalizes beyond the five examined binary64 solutions.
    - **Fix:** Qualify both sentences to match Section 6 and the five-solution restriction.

19. **scip-bug issues 6 and 7: the draft cites internal files, and the sources are unlisted** (minor)
    - **Location:** the draft in `scip-bug/report.md`, lines 502, 527 and 555, and the file table in Section 9.
    - **Evidence:**
      - The unsubmitted upstream draft, which is written for SCIP developers, cites `logs/minor_review_check.log`, `../reviews/scip-bug-r1/rv_runs.log` and "Review r1 proposed".
      - The new `sources/` directory (#162/#190 JSON) and `minor_review_check.py` appear nowhere in the report or its Section 9 file table.
      - The saved JSON supports the added #162/#190 statements: titles, dates, the orbitopal-symmetry discussion and the 1e-6 coefficient comment. One caveat: a #162 contributor judged the orbitopal reductions correct, so "points toward" is fair but not settled.
    - **Fix:** Rephrase the draft's internal references before filing, and list `sources/` and `minor_review_check.py` in Section 9.

20. **water-ann-kan: a stale sentence and a stale comment** (minor)
    - **Location:** `primal/water-ann-kan/report.md:5` and `primal/water-ann-kan/code/nn_exact.py:143`.
    - **Evidence:**
      - Line 5 still says "none of this has been independently reviewed". That contradicts response row 1 and the new open-issues text.
      - The code comment at line 143 still reads "every variable as interval centre and radius", although the code writes {lo, hi}. The description string was fixed, but not this comment.
    - **Fix:** Update the sentence and the comment.

21. **audit-ir: the counts need two clarifications** (minor)
    - **Location:** `audit-ir/report.md`, Section 1 (around line 62).
    - **Evidence:** Group C recounted the counts on all 1,633 saved pages with an independent parser: 35 (11–17 digits), 38 (11–19) and 46 (11–20). No value has more than 8 decimals. Two points need stating:
      - The counts are displayed entries, not distinct numbers; the 35 entries are 18 distinct strings.
      - The 46 count treats zeros such as those in "−10000000000." as significant.
      - In addition, "three are in display ties" means three instances (fac1, fac2, waternd_fosspoly0), which together have 17 tie pairs.
    - **Fix:** State both definitions where the counts are given, and write "three instances".

22. **Cosmetic** (minor)
    - **literature/control:**
      - There is no blank line before `## Response to review` (line 704).
      - "About 2e-10" for QPLIB_3177 is loose; the coefficient difference is 1.2e-10 and the bound difference 2.5e-10.
      - The 5.9/13.3/20.8% MINOTAUR gaps are computed from the logged absolute gaps, not printed in the logs.
      - `report.prev.md` is an unlinked round-0 copy.
    - **literature/network:**
      - The VSDP URL in the body differs from the one in the bibliography.
      - Section 7 omits `minor_review_check.py`.
      - "Default logs" is plural, but only the R3_H1_N4 log was checked.
      - Line 74 still cites "Schweidtmann & Mitsos 2019 … their Table 4". This is harmless.
    - **eg-recheck:** the Section 1 coverage bullets (`report.md:22–24`) could also cite the r1 tree-free proof (optional).

## Per-issue results (57)

"OK" means the fix is present and correct, and any number was independently recomputed or any source re-read. References such as "#9" point to the issues above.

| track | issue | result |
|---|---|---|
| chain | 1 display locations | OK. The three named documents contain the over-rounded displays. The old displays lie 2.54e-16 and 3.32e-16 above L; the safe displays are truncations below L. The main range is valid. List incomplete (#11) |
| chain | 2 which dual the gaps use | OK. Recomputed safe-display gaps: 9.62e-15, 1.01e-14, 9.41e-15, 1.01e-14; relative 1.90e-15, 1.99e-15, 1.86e-15, 1.98e-15 |
| chain | 3 u-distance | OK. Maximum 3.9432e-15 (chain200) ≤ 4.0e-15 |
| chain | 4 report and relative-gap wording | OK. Dividing by L < p gives an upper bound on the convention |
| dtoc5-lukvle10 | 1 report | OK |
| dtoc5-lukvle10 | 2 KKT overclaim | OK. No unconditional claim remains. x* agrees with the KKT vector to 5.8e-206 (rebuilt at 1500 digits). Stale line 127 (#12) |
| dtoc5-lukvle10 | 3 p5 comparison | OK. 4.774e-13 against the display, 5.143e-13 against the coordinates |
| dtoc5-lukvle10 | 4 sci_up carry | OK. Correct on boundary cases and on 20,000 random cases; all six reported gaps unchanged |
| lnts | 1 second Krawczyk centre | OK. mid(Z) ∈ Z; the Jacobian is enclosed over Z; any preconditioner is valid. Independent widths ≤ 1.80e-106 and objective width ≤ 1.73e-109; point files reproduced byte for byte. Stale logs (#10) |
| lnts | 2 report | OK. Weak rationality argument (#10) |
| lnts | 3 old-vector comparison | OK. Distances 3.2546e-15–3.5437e-15; only the middle control rounds differently in each instance. Display rounding (#9) |
| lnts | 4 relative-gap rounding | OK for the table. Inconsistent elsewhere (#9) |
| lnts | 5 tiny middle control | OK. Largest is 8.2e-112, below 1e-110 |
| powerflow | 1 report | OK |
| powerflow | 2 active slacks | OK. 0039r: e363 6.8e-13, e386 2.1e-13. Wording (#12) |
| powerflow | 3 p1 violations | OK. x266, x267 and x269; the seven voltage rows e307, e309–e313 and e315 |
| powerflow | 4 osilx.py | OK. Path and SHA-256 verified |
| powerflow | 5 primal displays | OK. 41869.0515113203 and 41869.0515113210 are exact upward roundings at the summary's precision. Relative gaps 2.0309e-9, 6.3221e-10, 6.6991e-10 |
| powerflow | 6 uniqueness | OK. The check is real; norms 1.93e-12, 2.855e-12, 5.376e-12; the argument holds for any C |
| water-ann-kan | 1 report | OK. Stale line 5 (#20) |
| water-ann-kan | 2 gap rounding | **Problem (#3)**. The relative-change range 3.7e-9–5.3e-9 is correct |
| water-ann-kan | 3 old bound violations | OK. 5.72648e-11, 3.0904e-10, 8.938913e-10, 9.0018923e-10 |
| water-ann-kan | 4 x650 margin | OK. Row e580 defines x650 = tanh(x670) with x670 ≈ 101.8 |
| water-ann-kan | 5 interval format | OK. The JSON bytes equal HEAD with only the description changed. Stale code comment (#20) |
| audit-ir | 1 report | OK |
| audit-ir | 2 digit counts | OK. 35, 38 and 46 recounted. Definitions (#21); slack floor (#6) |
| audit-ir | 3 spring wording | OK |
| audit-ir | 4 spring 1.0e-9 | OK. Equals SCIP's feasibility tolerance (bisection) |
| eg-recheck | 1 A1/A2 | OK |
| eg-recheck | 2 infeasibility overclaim | OK. 1,114,361 leaves; 98,234 = 85,685 + 373 + 12,176 |
| eg-recheck | 3 leaf numbering | OK. Concatenated position 69407 = part-5 index 56587, the same box |
| eg-recheck | 4 Git bullet | OK. 514a788f lists the six second-pass files |
| eg-recheck | 5 near-optimal regions | OK |
| eg-recheck | 6 tree-free proof | OK. `own_cover.log` reports "COVERAGE PROVED" for all 8 parts |
| scip-bug | 1 totals | OK. Raw logs: 0/122 with b; 78/122 for matched defaults (27/60 + 19/20 + 30/40 + 2/2). The CSV omits the two later p4 runs |
| scip-bug | 2 seed 11 | **Partial (#17)** |
| scip-bug | 3 low pair | OK. Stale line 36 (#18) |
| scip-bug | 4 hypothesis label | OK |
| scip-bug | 5 binary64 | OK in the proof summary. Line 173 generalizes (#18) |
| scip-bug | 6 #162/#190 | OK against the saved JSON. Sources unlisted (#19) |
| scip-bug | 7 draft and exact optima | OK. The inline CIPs equal the files; the fm336 and tiny2 case proofs are sound; witness acceptance confirmed in `rv_runs.log`. Internal references (#19) |
| lit-control | 2.1 upper bounds | OK. Only the regex anchor was dropped (recovered from the author's session log). Independent maxima: 4.7078e-10 (all four pairs), 2.4970e-10 (QPLIB_3177). Stale log and README (#14) |
| lit-control | 2.2 Waki | OK. PDF p. 33 = printed p. 31; −1.6e-10 to −8.1e-10; M = 600–1000 |
| lit-control | 2.3 Müller page | OK. PDF p. 40; camshape200–800 on p. 41 |
| lit-control | 2.4 camshape800 | OK. QPLIB_3177 closes in 1 node with bound inf; the smaller copies time out at 10800 s |
| lit-control | 2.5 MINOTAUR defaults | **Partial (#13)** |
| lit-control | 2.6 p1 wording | OK. 3.9132e-10 at e1562 |
| lit-control | 2.7 CONOPT 8.7e-6 | OK. All four mentions reworded |
| lit-network | 1 cumene versions | OK. arXiv v2 Table 4 p. 21 and Fig. 6 p. 22; dissertation Table 2.8: 2930, 444, 328 and the iteration counts |
| lit-network | 2 nonclosing benchmarks | OK. Page citation (#16) |
| lit-network | 3 Oustry et al. | OK. 803.127, 7896.87, 137254; PGLib v21.07. Novelty line 135 (#15) |
| lit-network | 4 0030p/0030r | OK. All transport claims corrected |
| lit-network | 5 Huang Table 5.2 | OK. 0.000470589; 6–24 periods 0.178792–1.14263 |
| lit-network | 6 bibliography | OK. Göß authorship (#16) |
| lit-network | 7 KAN tolerance | OK. p. 16 states only a zero gap tolerance and the time limit |
| lit-network | 8 duplicate commands | OK. Section 12 covers every removed item |
| lit-network | 9 unobtained sources | OK |

## Script and JSON changes

The checks below ignore path-only edits made by the parallel reproduction work.

- **`primal/dtoc5-lukvle10/gaps.py`:** the carry fix is minimal and correct. All reported gaps are identical under the old and new versions.
- **`primal/lnts/lnts_primal.py`:** only the second-step centre changed. The change is valid; see issue 1 in the lnts rows above. A scratch rerun reproduced all four point files byte for byte, so no numerical result changed.
- **`primal/water-ann-kan/code/nn_exact.py`:** only the description string changed. A related code comment is stale (#20).
- **`literature/control/checks/qplib_camshape_compare.py`:** the regex start anchor was dropped, and nothing else changed. The fix is correct. Its log was not refreshed (#14).
- **The seven point JSONs:** in each, the HEAD bytes with "(mid, rad)" replaced by "{lo, hi}" equal the current bytes. Every interval has the keys lo, hi and defined_by, with lo ≤ hi.

## Collateral damage

- Every hunk of the ten before→after report diffs was examined.
- No accidental deletions or unexplained number changes were found. The only changed number outside an issue fix is chain 3.9e-15 → 4.0e-15, which is issue 3.
- The literature/network revision removed a duplicate command list. Section 12 covers every item; only two sha256 prefixes are lost, which is immaterial.
- The recorded `reviews/minor-fixes/report_changes.patch` matches the current diffs except for hunk layout, so no edits were made after the handoff.
- The before-fix copies of the seven tracked reports are identical to git HEAD.
- The remaining problems are statements left stale by the fixes: #10, #12, #15, #17, #18 and #20.

## Integration list (item 4)

The list is correct where it speaks, with the exceptions below.

- **Missing items:**
  - the lnts100 primal display (#1);
  - the dtoc5 primal display (#2);
  - the chain gap ≤ 1.01e-14 (#4);
  - the audit slack-floor note (#6).
- **Wrong items:**
  - the eg instance name and the leaf/box wording (#5);
  - the water "conservative upper bounds" cell (#3);
  - the MINOTAUR rule cell (#13).
- **Checked and correct:**
  - the powerflow 0039p/0039r displays and the powerflow0030p display (576.8934134704 is the exact 10-decimal upward rounding);
  - the lukvle10 display (352.2380254064961 is a valid upper bound);
  - the remaining lnts50, lnts200 and lnts400 displays;
  - the removal of the obsolete "no exactly feasible point" paragraph (`open-instances-summary.md:43–46`). The paragraph's "row violations of 1e-20 to 8e-12 … measured against its value" is obsolete too; the integration step should rewrite the whole paragraph, not one clause.

## Commands run

All commands were targeted, used at most one process per verifier group at a time and were single-threaded. No main construction, solver campaign, project-wide verification or CI inspection was run. No track or author file was edited. Each group's exact command list is in `reviews/minor-fixes-review-r1/group-{A,B,C,D,E}.md` (section "Commands"), and its scripts and logs are in `scratch-{A..E}/`.

Lead (from the repository root, `research-20260929`, or P):

```sh
cat reviews/minor-fixes/{summary.md,commands.md,FILES.json,PROGRESS.json,validation.log}
git status --short .; git diff --stat -- '*/report.md'
# before copies vs HEAD, per track:
git show HEAD:research-20260929/publication/$t/report.md | cmp - reviews/minor-fixes/before/<t>.txt
git diff -- primal/dtoc5-lukvle10/gaps.py primal/lnts/lnts_primal.py primal/water-ann-kan/code/nn_exact.py
# recorded patch vs current diffs:
diff -u --label before/$t/report.md --label after/$t/report.md reviews/minor-fixes/before/<t>.txt $t/report.md >> /tmp/mfr_now.patch
diff <(grep -v '^@@' /tmp/mfr_now.patch) <(grep -v '^@@' reviews/minor-fixes/report_changes.patch)
grep -n -i "exactly feasible|41869|lukvle10|camshape|..." research-20260929/open-instances-summary.md; sed -n 40,50p, 120,150p of it
sed -n 262,285p research-20260929/bound-audit/audit-report.md
grep -rn "eg_all" --include=*.md research-20260929
python3 -c "<print objective_enclosure of primal/lnts/points/lnts100_point.json>"   # 0.5545954011669111610017828
grep -n "5.389672119181" primal/dtoc5-lukvle10/report.md
sed -n 28p primal/water-ann-kan/report.md; cat scratch-C/gap_check.log
sed -n 126,136p literature/network/report.md; head -12 literature/network/sources/goss2026_arxiv2603.16505.txt
ls -l control/checks/qplib_camshape_compare.{py,log}; grep -n 2.5e-10 control/checks/README.md
```

Main group scripts (single-threaded: `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`):

- **A:** `scratch-A/chain_gaps.py`, `lnts_check.py`, `extra_checks.py`, and a scratch rerun of `lnts_primal.py 50 100 200 400` (5.6 s).
- **B:** `scratch-B/check_dtoc5_lukvle10.py` (35 s) and `check_powerflow.py`.
- **C:** `scratch-C/water_check.py`, `gap_check.py`, `json_check.py`, `digits_check.py`, `slack_floor_check.py` and `digits_in_pairs.py`.
- **D:** `scratch-D/eg_counts.py`, `eg_perpart.py`, `eg_tightnum.py`, `scip_recount.py`, `scip_traces.py` and `fm336_cases.py`.
- **E:** `scratch-E/camshape_bounds.py`, plus `pdftotext`/`grep` reads of the saved sources and read-only arXiv API and VSDP page fetches.

These are local targeted checks, separate from CI.
