Verdict: issues

# Independent review of the publication integration, round 1

Reviewer: independent final verifier. Date: 2026-10-03. Scope: the integration edits to `research-20260929/open-instances-summary.md` (S) and `research-20260929/bound-audit/audit-report.md` (A) against git HEAD, the new `publication/READINESS.md` (R), and `publication/integration/`. Paths are relative to `research-20260929/` unless they start with `publication/`-relative names inside R. Evidence: [integration-r1/](integration-r1/) — `scratch/` (lead's exact checks), `agent-lit/findings.md` (literature labels), `agent-tracks/` (solver, SCIP, eg, audit-ir, status, reproduction). I did not edit any document.

## Summary

**The numbers are right.** No displayed number in either main document is wrong.
- **The 33 replacements.** All 33 owned replacements from `minor-fixes/integration-r2.json` (identical to `minor-fixes/summary.md`) match HEAD exactly once and apply in order. Every later cell change is one of these:
  - the "≤" prefix of the round-up convention;
  - a fix of review items 2, 4, 5 or 6;
  - a link or statement for a track result.
  
  No table row was lost. No number outside these categories changed.
- **Review items 2, 4, 5 and 6.** All four are fixed:
  - gaps rounded up everywhere: 1.68% in prose; 7.27%, 1.5e-9, 4.9e-14, 2.1e-9, 6.4e-10, 0.195%, 20% and 16.1%;
  - A1/A2 defined and attached to all three eg rows;
  - the spring sentence has an antecedent;
  - KAN 0.0694, optcdeg2 "certificate value rounded down", and emfl050_3_3 1.36e-6.
- **Gap cells, recomputed independently.** My own exact rational recomputation (`scratch/my_gaps*.py`) of every gap cell from the saved points, enclosures and certificates confirms every displayed gap is an upper bound on the exact gap under the round-up convention. This covers lnts, dtoc5, lukvle10, optcdeg2, ex6_2_*, etamac, pricing050, chain, all four catmix, powerflow (relative), pindyck, eg (relative), waterno2 (all seven percentages), ann (four percentages) and the six KAN cells. Every primal display is rounded in the correct direction.
- **Dual displays.** Every dual display is at or below its certificate, with one documentation subtlety: eg_disc_s (issue 5).
- **Counts.** The solver-campaign counts (129/126/3/0/109/6/103/6/10), the eg-recheck counts (1,114,361 leaves, 0 failures, 1,152,830 boxes) and the audit counts (12 (i-r) pairs; 35/38/46 with 18 distinct strings; 0 of 158; 17 ties) all reproduce from the saved data.
- **SCIP.** The SCIP statements say correctly that three of five examined claims are refuted and that the upstream report is not submitted.

**The problems are presentation, scope wording, readiness bookkeeping and packaging:**
- The new 43-row literature table does not render.
- The reproduction package, which S says maps the certificates, does not contain the all-leaf eg_disc2_s evidence and still describes the old sample.
- No document records the computing environment of the certificate runs or a data-licence statement, although R's final gap check says nothing is missing.
- About a dozen statements overstate or leave out a caveat that the track reports state.

R omits some review facts:
- the unresolved state of the solver-campaign round-2 review;
- the major issues found in the solver-analysis and minor-fixes r2 reviews, and the fact that their fixes were not re-reviewed.

There are no blockers, 3 major issues and 12 minor issues.

## Issues

### Major

1. **The literature table in S does not render** (major; presentation of the novelty claims)
   - **Location:** S:159–162.
   - **Evidence:**
     - `sed -n 159,164p open-instances-summary.md | cat -A` shows two empty lines between the delimiter row `|---|---|---|` and the first data row (lnts50).
     - In Markdown a blank line ends a table. The 43 rows therefore render without a header, as pipe-separated text.
     - The integration's `check_integration.py` reported "Markdown table shapes pass" and did not detect this.
   - **Fix:** delete S lines 161 and 162 (the two empty lines). Add a blank-line-inside-table test to the checker.

2. **The reproduction package does not cover the eg_disc2_s all-leaf evidence** (major; packaging versus a stated claim)
   - **Location:**
     - S:344–348 ("The reproduction guide and package report map the certificates …");
     - R:48 and R:126–130;
     - `publication/reproduction/README.md:251–255`, `report.md:179–180`, `result-map.json` (eg_disc2_s entry), `tools/build_result_maps.py:52–55`.
   - **Evidence:**
     - `grep -c eg-recheck publication/reproduction/manifest.json` gives 0.
     - README:255 still reads "sample of **110,676 of 979,044 leaves**".
     - `build_result_maps.py` points the eg rows only at the older retry run, so the pending map rebuild (R:103–107) will not add the all-leaf evidence.
     - S and the eg rows of R rest on the all-leaf recheck (`publication/eg-recheck/`, review `eg-recheck-review-r1.md`).
   - **Fix:**
     - Add to R:48 (caveats) and to the "Release preparation still pending" list (R:126): "The reproduction README, report, result map and manifest still describe eg_disc2_s by the earlier 110,676-leaf sample and do not include publication/eg-recheck/ or publication/reviews/eg-recheck-r1/. The package owner must add both to the manifest scopes and the eg_disc2_s map entry, and update README.md:251–255 and report.md:179–180, before the final manifest."
     - Until that is done, change S:346 "map the certificates" to "map the certificates (the eg_disc2_s all-leaf recheck is in publication/eg-recheck/ and not yet in the package)".

3. **The computing environment of the certificate computations is not recorded anywhere, and no data-licence statement exists** (major for a computational paper; R's final gap check is incomplete)
   - **Location:** R:115–135 ("Scientific evidence still missing … none"); `publication/reproduction/environment.json`.
   - **Evidence:**
     - `environment.json` has only the keys `python`, `packages` and `scip` (SCIP 10.0.2), and records the reproduction environment, not the original certificate runs.
     - Hardware (Xeon w5-2565X, 18 cores, 47 GB) is described only for the solver campaign (`solver-runs/report.md:81`).
     - No document records, for the certificate runs, the OS or kernel, the CPU or SIMD flags, the numpy BLAS/libm backend, or the mpmath/numpy versions used at the time. Two results depend on these:
       - A2 (the exp accuracy) was sampled under one libm/SIMD dispatch;
       - the topopt p5 regeneration depends on the BLAS thread count and build.
     - Certificate run times exist only scattered across the track reports (for example eg run G ≈ 41,151 CPU-s), measured on a shared, loaded machine.
     - The package redistributes MINLPLib OSIL files and pages, but no document contains a licence or redistribution statement.
   - **Fix:**
     - Add a row to R's evidence table, "computational environment and run times", marked *not yet collected*.
     - Add to "Release preparation still pending": "collect one table of hardware/OS/BLAS/libm and Python, numpy, scipy and mpmath versions for the certificate runs (or state that only the reproduction environment is pinned), with per-certificate CPU/wall times and the shared-machine caveat; add a data-licence/redistribution statement for the MINLPLib files and pages."
     - Change R:117 to "Scientific evidence still missing: none for the stated claims; paper metadata (environment, run-time table, data licence) is still to be collected."

### Minor

4. **The gap-source exception list in S is incomplete** (minor)
   - **Location:** S:63–65.
   - **Evidence:**
     - The prose says that gaps use certificate values except for lnts, chain and pricing050.
     - `integration/check_numbers.py` and `gap-values.json` also use the displayed duals for dtoc5 (4.674e-16 against the display; 7.4e-18 against the verifier's 5.38967211918114046), lukvle10 (display 1.7e-14 below the binary64 value), pindyck and all three eg rows.
     - All the resulting cells are valid upper bounds, so this is wording only.
   - **Fix:** replace "except lnts (the displayed summary duals), chain (the safe individual dual displays), and pricing050 (…)" with "except lnts, dtoc5, lukvle10, pindyck and the three eg_* rows (their displayed duals), chain (the safe individual dual displays), and pricing050 (…)".

5. **The eg_disc_s dual display lies above the author's binary64 certificate; its validity rests on the independent decimal-target certification** (minor; documentation)
   - **Location:** S:51 (dual 5.760539610694994).
   - **Evidence:**
     - The certifier's bound is `np.float64(5.760539610694994)` (`open-instances-wave3/eg/retry/logs/disc9_p1.log:16`). Its exact value is 5.76053961069499376179…, which is 2.38e-16 below the display.
     - The display is nevertheless certified: `reviews/eg-retry-review-checks/verify_tree.py` passes θ* as a command-line string to `Fraction`. All 46,223 + 40,573 leaves were certified against the exact decimal 5.760539610694994 (`verify_disc_p0/p1.log`, minimum LP margin 2.0e-9), under the same A1/A2 standing.
     - This is the same situation as the chain50/chain200 displays, which were corrected; here the display survives only through the reviewer's run.
   - **Fix:** add to the eg paragraph (after S:87): "The eg_disc_s display 5.760539610694994 is 2.4e-16 above the certifier's binary64 bound; it is valid because the independent retry review certified every leaf against this exact decimal." Alternatively, display 5.7605396106949937.

6. **The literature-table rows need label and wording corrections** (minor; no novelty claim is contradicted by a report)
   - **Location:** S:163–201. Full evidence is in `integration-r1/agent-lit/findings.md`; I spot-checked the first four sub-items below.
   - **Fixes:**
     1. **S:163:** change "Martín" to "Martin". S:50 and S:188 already use "Martin", and the saved PDFs print "Alexander Martin".
     2. **Missing report labels.** Add the label each report gives:
        - camshape100 (S:168): "Already solved globally in floating point" (`literature/control/report.md:84, 372`).
        - eg_int_s (S:188): the same label (small report :41, :461).
        - camshape800 (S:171): "Prior global claim false (rigorously for the MINLPLib model; for the rounded QPLIB copy, strong evidence, not proof)" (control :87, :578).
     3. **catmix rows (S:178–181).** The OSIL/GAMS statement comes from `publication/minlplib-status/report.md:17`, not from the control report (which gives "not the COPS 3.0 model", :91). Add a link to it, and optionally the size: "(double rounding, at most 2.4e-16 relative)".
     4. **powerflow0030p (S:191).** Replace "polar/rectangular coefficient rounding prevents unproved exact bound transport" with "the polar and rectangular files differ by coefficient rounding, so a rigorous bound cannot be transferred between them without a perturbation argument". Add "Ours is the first rigorous certificate found for this MINLPLib model". Call Oustry et al. "certified" (network :361).
     5. **powerflow0039p/r (S:192–193).** Write "Ghaddar et al. 2016 solved tapped MATPOWER case39 globally in floating point (moment relaxation); published SDP gaps are near zero" (network :36, :141–147).
     6. **KAN n4/n5 (S:200–201).** Replace "exact network evaluation" with "60-digit evaluation of the network at SCIP's points" (network :176, :322).
     7. **eg_disc_s/eg_disc2_s (S:189–190) and R:38.** Write "CAMINO's Gurobi 13.0.0 optimality claim is refuted by a feasible point; the data do not record Gurobi's termination status, and the cause is unknown".
     8. **lnts (S:164–166).** Write "Göß 2026 PARA prints a 0.00% gap (below 0.005%)" for lnts100/200 and "0.01%" for lnts400 (control :35, :267, :533).
     9. **dtoc5 (S:167).** Scope Waki et al. to "the source model (h·y², M = 600–1000)" (control :299–313).
   - **Also for the paper:**
     - cite the Göß–Burlacu–Martin publisher correction (small :423–429);
     - credit the SIF value −0.21850 for hvycrash (small :174);
     - call the lukvle10 SOLTN value a tolerance artifact (control :415).

7. **The SCIP statements leave out the scope the SCIP report gives** (minor)
   - **Location:** S:281–286; A:927–930.
   - **Evidence:**
     - "The period problems" are periods 0, 4 and 5 of waterno2_06 only.
     - The period failures are also seed-dependent: master solves p0 correctly in 10/10 seeds (`publication/scip-bug/report.md:92–94`).
     - Two higher cell-pair claims are refuted: 65.12 on 10.0.x/10.1.0 and 56.49 on master.
     - A's paragraph omits that the low cell-pair claims are not refuted.
   - **Fix:**
     - At S:282–286, replace "supply exact rational witnesses for the period problems and the seed-dependent cell-pair problem. The higher cell-pair claim is now refuted by an exactly feasible witness; the low claim is not refuted." with "supply exactly feasible rational witnesses that refute SCIP's wrong "optimal" claims on three single-period subproblems of waterno2_06 (periods 0, 4 and 5) and on one cell-pair subproblem. The wrong claims occur only for some random seeds. The higher cell-pair claims (65.12 on 10.0.x/10.1.0, 56.49 on master) are refuted; the low claims near 55.6898 are not."
     - At A:927–930, replace "supplies exactly feasible witnesses against wrong optimality claims on the waterno2 period and cell-pair models" with "supplies exactly feasible witnesses that refute SCIP's seed-dependent wrong optimality claims on three waterno2_06 period subproblems and the higher cell-pair claims; the low cell-pair claims are not refuted".

8. **The rounding-scale bullet in S overgeneralizes; the spring sentence in A misattributes the bisection** (minor)
   - **Location:** S:262–264; A:668–673.
   - **Evidence:**
     - Page rounding explains only the five spring conflicts. For the other seven, earlier six-digit rounding is only possible (`publication/audit-ir/report.md`; A:909–912 says this correctly).
     - The bisection on the objective variable was run by the audit-ir script `publication/audit-ir/xcheck_scip.py`, not by SCIP, and found a difference of 1.0e-9 (`logs/xcheck_scip.log:8`).
     - "Solver-point pairs" is inaccurate. The 12 pairs are (instance, solver) pairs; spring's points p2 and p3 count once (audit-ir report :22).
   - **Fix:**
     - At S:262–264, write "They refute the displayed numbers taken literally. Page rounding of the proven optimum explains the five spring conflicts; earlier rounding to six significant digits could explain the other seven (evidence, not proof). The underlying solver bounds are unknown."
     - At A:668, change "solver-point pairs" to "(instance, solver) pairs".
     - At A:670–673, write "In the separate audit-ir recheck, SCIP 10 accepted the spring proof point at feasibility tolerance 1e-9; a bisection on SCIP's objective variable found accepted values down to 1.0e-9 below the exact objective. This is the feasibility tolerance, not an objective disagreement."

9. **A overstates the model-history evidence and credits the wrong review round** (minor)
   - **Location:** A:914–918, A:746–750; S:266–269.
   - **Evidence:**
     - The status report's Table B1 (`publication/minlplib-status/report.md:88–100`) shows no pre-bound copy for nine instances: four sssd*persp, watercontamination0303 and four smallinvDAX*. For these, 2014-03 to 2014-12 is not covered.
     - "Archived listings support model identity for the audited past bounds" is therefore too broad. The next sentence's generic caveat does not name these instances.
     - The refresh was confirmed in status review r1. r2's verdict is "issues", with four minor corrections later addressed.
   - **Fix:**
     - At A:916–918, replace "The [round-2 review] find … Archived listings support model identity for the audited past bounds." with "find (confirmed by [review r1](…r1.md); [review r2](…r2.md) found four minor issues, since addressed in the report) … Archived copies agree with today's model on both sides of the bound dates for most audited instances. sssd*persp, watercontamination0303 and smallinvDAX* were added days before their 2014 bounds; no copy covers March to December 2014, and their identity rests on the 2014-12 statistics and 2017 full copies."
     - At S:268–269, replace "Missing archive windows" with "Missing archive windows (no copy covers March–December 2014 for sssd*persp, watercontamination0303 and smallinvDAX*)".

10. **R omits review facts for the solver campaign, SCIP and minor-fixes rows** (minor; R:46, R:47, R:49)
    - **Evidence:**
      - **Solver analysis.** `solver-analysis-review-r1.md` has the verdict "issues", with two major issues (six BARON values without a globality guarantee; the overloaded first batch) and four minor ones. The author's response in `solver-runs/report.md:368–388` was not re-reviewed.
      - **Campaign round 2.** The campaign's round-2 review never finished: `reviews/solver-campaign-r2/PROGRESS.json` has `"done": []` and no verdict.
      - **Minor-fixes r2.** That review found one major issue (the SCIP five-solution sentence). Round 3 fixed it with the reviewer's own text, without re-review.
    - **Fix:**
      - **R:46 status cell:** "Setup review r1: **issues** (two major), addressed by the final relaunch; the campaign round-2 review stopped without findings or verdict. Final-analysis review r1: **issues** (two major: six BARON values without globality guarantee, overloaded first batch; four minor); raw values/counts confirmed. The author's response in report.md has not been re-reviewed. Integration independently recounted …".
      - **R:47:** add "Minor-fixes review r2 found one major overstatement (report line 173); round 3 applied the reviewer's exact replacement, without re-review."
      - **R:49:** write "latest verdict **issues** (one major and ten minor) … Round 3 fixed the major and the track-level minor items without further review."

11. **R's wording is imprecise in four places** (minor; R:27, R:33, R:38, R:131)
    - **Fixes:**
      - **R:27:** replace "Prior floating-point results are partly known" with "lnts is partly known: Gurobi closed lnts50 to tolerance, and Göß 2026 PARA prints 0.00–0.01% gaps (floating point)".
      - **R:33:** replace "may have earlier ε-global floating-point results" with "very likely have earlier ε-global floating-point results (McDonald–Floudas; sources not read)" (small report :36, :233).
      - **R:38:** "Coverage has an exact independent proof" holds for eg_disc2_s only. Add "(eg_disc2_s; eg_int_s and eg_disc_s coverage rests on the retry reviewer's exact tree bookkeeping)".
      - **R:131 and R:16:** after this review, change "An independent review of this final integration has not been performed" to cite this file and its verdict.

12. **Coverage paragraph: a useful fact was deleted** (minor)
    - **Location:** S:327–334 (diff against HEAD).
    - **Evidence:**
      - HEAD said that "camshape100 and lnts50 were already within 1.2e-6 and 3.8e-5 relative of closure by single-solver bounds". The new text replaces this with a generic sentence.
      - The values are correct (5.2e-6/4.284 = 1.2e-6; 2.12e-5/0.5547 = 3.8e-5) and appear only in the control report (:79, :84).
      - The dropped count "11" of first-wave instances is harmless.
    - **Fix:** after "as the per-instance table explains", add "; MINLPLib's own listed bounds were already within 1.2e-6 (camshape100) and 3.8e-5 (lnts50) relative of closure."

13. **A pre-existing S sentence conflicts with the new campaign** (minor)
    - **Location:** S:297–299.
    - **Evidence:**
      - "SCIP 10's camshape100 incumbent from our own run … lies 5.3e-5 below the exact optimum" comes from an earlier exploratory run (`reviews/closing-audit-a.md:448`).
      - The campaign's SCIP 10.0.3 point lies only 1.519e-7 below it, with row violation 7.7e-10 (`publication/solver-runs/point_checks.log:6`).
    - **Fix:** write "in an earlier exploratory SCIP 10 run (before the one-hour campaign), the camshape100 incumbent (row violation 1e-8) lay 5.3e-5 below the exact optimum (not independently checked); the campaign's SCIP 10.0.3 point lies 1.5e-7 below it."

14. **Two small audit-text points** (minor)
    - **Location:** A:284–285 (adjacent to replacement 31) and A:1360–1368.
    - **Evidence:**
      - The sentence that every 6-significant-digit entry is dated 17 or 26 Sep 2013 has one exception: methanol50 LINDO 0.00802826 (2022-02-15), which has 6 significant digits at the 8-decimal limit.
      - Section 10.4 says the owned replacements were applied, but does not mention that the spring sentence of replacement 33 was then rewritten (minor-fixes review r2, issue 5).
    - **Fix:**
      - At A:284, add "(apart from entries whose 6 digits reach the 8-decimal limit, such as methanol50 LINDO 0.00802826, 2022-02-15)".
      - In 10.4, add "The spring sentence of replacement 33 was then rewritten as minor-fixes review r2, issue 5, requested."

15. **Stale displays remain in track and package reports** (minor; for the owners, outside the integration's scope)
    - **Evidence:**
      - `literature/network/report.md:277` gives waterno2_06 as 282.888 (1.67%).
      - `literature/small/report.md:494–496` describes eg_disc2_s by the sample only.
      - `publication/reproduction/README.md:240–241` gives the primal displays 6.4531031593842274 and 5.7605396164535106, which lie below the exact objectives.
      - `solver-runs/report.prev.md` keeps its chain50 display (already recorded in R).
    - **Fix:**
      - Use 1.68% and the all-leaf statement in those reports.
      - Change …2274 to …2275 and …5106 to …5107 in the package README.
      - Or keep R's statement that S is authoritative, and list these files in R:126.

## What was confirmed

**Diff and replacements.** Both documents were checked against HEAD:
- `scratch/apply33.py` applies the 33 items to HEAD copies: each old string occurs exactly once, and each item's old/new text is present in `minor-fixes/summary.md`.
- `scratch/celldiff.py` compares cell by cell against the current table rows; prose hunks were compared by `diff`.
- Every other hunk is a header or date update, the convention text, the A1/A2 paragraph, a track-result statement or link, the 8.3 retitling, 8.4 or 10.4.

**Gap cells.** Exact value / display:

| cell | exact | display |
|---|---|---|
| lnts50/100/200/400 | 5.789 / 6.112 / 5.837 / 5.871e-13 | 5.79 / 6.12 / 5.84 / 5.88e-13 |
| lnts, against N·h2 | at most 5.5467e-13 | ≤ 5.55e-13 |
| dtoc5 | 4.674e-16 | 4.7e-16 |
| lukvle10 | 1.4172e-9 | 1.5e-9 |
| optcdeg2 (J_upper − exact certificate) | 8.978e-16 | 9e-16 |
| ex6_2_5 | 2.000e-15 | 2.1e-15 |
| ex6_2_7 | 4.818e-14 | 4.9e-14 |
| etamac | 2.576e-15 | 2.6e-15 |
| pricing050 | 4.23e-14 | 4.23e-14 |
| chain (maximum) | 1.0057e-14 | 1.01e-14 |
| catmix100/200/400/800 | 1.850e-13 / 1.896e-11 / 6.806e-11 / 1.4844e-10 | 1.85e-13 / 1.90e-11 / 6.81e-11 / 1.49e-10 |
| powerflow0030p/0039p/0039r (relative) | 2.031e-9 / 6.322e-10 / 6.699e-10 | 2.1e-9 / 6.4e-10 / 6.7e-10 |
| pindyck | 5.431e-14 | 5.44e-14 |
| eg_int_s / eg_disc_s / eg_disc2_s (relative) | 9.997e-10 / 9.996e-10 / 9.996e-10 | 1e-9 |
| waterno2 | 1.674 / 3.780 / 7.262 / 10.812 / 6.894 / 4.867 / 5.895 % | 1.68 / 3.78 / 7.27 / 10.82 / 6.90 / 4.87 / 5.90 % |
| ann_cumene_tanh | 0.19402 / 0.19364 / 19.07 / 16.01 % | 0.195 / 0.194 / 20 / 16.1 % |
| KAN | 6.89e-11, 1.073e-10, 8.96e-11, 2.4156e-8, 1.018e-10, 9.57e-11 | 6.9e-11, 1.08e-10, 9e-11, 2.42e-8, 1.02e-10, 9.6e-11 |
| emfl050_3_3 (lower bounds) | 1.4202e-5 absolute; 1.3653e-6 relative | 1.42e-5; 1.36e-6 |

The pricing050 note is accurate: the saved upper bound U and the 20-digit primal differ by 5.0e-17, and the saved digits cannot reproduce the verifier's 1.04e-17.

**Dual displays.**
- Each was checked against its certificate (exact binary64 value or exact rational): lnts (N·h2), dtoc5, lukvle10, camshape100–800, optcdeg2, ex6_2_*, etamac, pricing050 (upper), chain safe values and range, catmix range, powerflow (exact fractions), pindyck, eg_int_s, eg_disc2_s, waterno2 (all three 06 bounds), ann and KAN.
- eg_disc_s holds as described in issue 5.

**Track statements.** Confirmed against the current reports and data:
- **Solver campaign** (own recount of `results.csv`):
  - 129 rows and 126 valid; SCIP memory stops on ex6_2_5, ex6_2_7 and pindyck;
  - the only 1/1 claims are BARON camshape100 (5.26e-7 below the optimum) and camshape200 (2.05e-6 below), so the returned points are not exactly feasible;
  - 109 finite duals (35/36/38), all weaker than the certificates (91 against OSIL, 18 against R);
  - the globality warning on exactly the six named BARON rows, leaving 103;
  - the six SCIP tightened rows;
  - the first batch matches R:93–94;
  - versions and settings are as stated; BARON's limit is CPU time.
- **eg-recheck:** 38 chunk logs, 1,114,361 / 0 / 1,152,830, and the 10,404-leaf sample in parts 0 and 2–7.
- **SCIP:**
  - three of five examined claims refuted;
  - 10.0.2/10.0.3/10.1.0/master a01de2c;
  - the mechanism is limited to the traced runs;
  - not submitted (stated in bold in both documents and in R open decision 1).
- **audit-ir:**
  - 3 + 1 + 5 + 3 pairs;
  - spring rounds to 0.84624567;
  - counts and floor as stated;
  - review verdict "verified".
- **minlplib-status:**
  - refresh 2026-10-02, with all 69 instances unchanged;
  - ghg_3veh, glider100 and topopt as stated.
- **Reproduction:** topopt p5 rests on the committed certificate, the 84/8/1 display check holds, and the package commands are pending.

**Literature.**
- All 43 rows are present once.
- No "new as far as found" claim is contradicted by a report.
- The latest verdicts are reported correctly in R:45: control r2 verified, network r2 verified, small r3 issues (minor only, author-resolved).

**R open decisions.** These are correct: the SCIP filing; the reruns of the ten first-batch runs and the three memory stops (lists match the data); and commit after the map/manifest rebuild. Two optional additions:
- whether to inform the MINLPLib maintainers about invalid listed bounds;
- whether to inform BARON about the two contradicted optimality claims.

These are outward-facing user decisions similar to the SCIP filing.

## Commands run

Lead, from `research-20260929/` or `publication/reviews/integration-r1/scratch/`. Only saved data was read, with exact `Fraction` arithmetic; no scientific module was imported or run, and the main tree was not written.

```sh
git diff --stat -- research-20260929/open-instances-summary.md research-20260929/bound-audit/audit-report.md
git diff -- research-20260929/open-instances-summary.md ; git diff -- research-20260929/bound-audit/audit-report.md > /tmp/ir1_audit.diff
git show HEAD:research-20260929/open-instances-summary.md > scratch/head_summary.md
git show HEAD:research-20260929/bound-audit/audit-report.md > scratch/head_audit.md
python3 scratch/apply33.py                 # 33 replacements on HEAD copies; summary.md cross-check
python3 scratch/celldiff.py                # cell-level comparison of table rows
diff <(grep -v '^| ' scratch/applied_open-instances-summary.md) <(grep -v '^| ' open-instances-summary.md)
diff scratch/applied_bound-audit__audit-report.md bound-audit/audit-report.md
python3 scratch/my_gaps.py  > scratch/my_gaps.log    # lnts..powerflow: 19 OK, 0 FAIL
python3 scratch/my_gaps2.py > scratch/my_gaps2.log   # pindyck, eg, water, ann, emfl: 16 OK, 0 FAIL
python3 -c '...Decimal(5.760539610694994)...'        # exact binary64 values of eg duals
grep -n "theta\|argv" reviews/eg-retry-review-checks/{verify_tree,indep_cert}.py   # decimal theta via Fraction(str)
sed -n 159,164p open-instances-summary.md | cat -A   # blank lines in literature table
python3 - (link check over S, A, R: no broken relative links)
cd /tmp && python3 publication/reviews/integration-r1/agent-tracks/count_solver.py   # solver recount (rerun by lead)
sed/grep/cat reads: READINESS.md; integration/{PROGRESS.json,commands.md,gap-values.json,check_numbers.py};
  minor-fixes/{integration-r2.json,summary.md,response-r3.md,commands.md}; minor-fixes-review-r2.md;
  primal/*/points and logs; reviews/{open-instances-verification,bangbang-verification,wave2-small-verification,pindyck-review*,eg-retry-review*}/;
  publication/reproduction/{cops/logs/exact_display_checks.json,environment.json,README.md,manifest.json};
  minlplib-status/report.md:88-100; audit-ir/report.md:17-23; solver-analysis-review-r1.md; solver-campaign-r2/PROGRESS.json
```

Helper agents (read-only; their scripts and the saved findings are in `integration-r1/agent-lit/` and `integration-r1/agent-tracks/`):
- literature: `cat`/`sed`/`grep`/`awk` over S, R, the three literature reports and their reviews, and `pdftotext -l 1` on the saved Göß PDFs;
- tracks: `count_solver.py`, `sub-eg-repro/count_eg_leaves.py`, `manifest_stale.py`, and `sub-ir-status/check_ir.py`, `check_floor.py`, `check_status.py`, `check_listings.py`.

At most 4 processes at a time, one thread each. These are local targeted checks, not CI. No solver, project-wide verification or CI inspection was run; no commit, push or outside contact.
