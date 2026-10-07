Verdict: issues

# Review of track minlplib-status (round 2)

Reviewer: independent verifier, round 2. A previous round-2 verifier was interrupted near the end. I sanity-checked its results and reused them, then finished the remaining items with my own runs. All check code, downloads and logs are in `publication/reviews/minlplib-status-r2/` (`code/`, `dl/`, `logs/`, `PROGRESS.json`). No processes of mine or of the previous verifier are still running.

## Summary

The revision fixes the round-1 major issue (M1) correctly, along with all eight round-1 minor issues. The new claims are confirmed independently with code that does not use GAMS or the author's scripts:

- **Archived listings.** All 29 complete captures equal today's .gms. The cut topopt capture of 2022-05-22 is an exact prefix: 23,479 complete lines and 1,039,259 characters.
- **Bracketing captures.** The captures were selected correctly from the CDX index. Bounds listed on the archived pages are the same then and now.
- **ghg_3veh.** The 3 constants, 6 occurrences and 4 rows are correct, as are their exact relative differences.
- **Exact .gms-to-OSIL comparison** for catmix100–800, methanol50 and lop97icx, coefficient by coefficient.
- **Objective-shift bounds:**
  - methanol50 on the box p4 ± 1: at most 3.2e-15;
  - lop97icx on the box p2 ± 1: at most 4.8e-13.

The author's two corrections to round 1 are right:

- The methanol50 objective differs in 1 constant, 104 linear and 255 quadratic coefficients; round 1's "359 linear" was wrong.
- The lop97icx OSIL objective at p2 is 4099.059953600000099; round 1's figure had one zero too many.

No verdict of the audit or the certificates changes. What remains are four minor factual or wording errors in secondary statements. All are easy to fix.

## Status of the round-1 issues

| round-1 issue | status | evidence |
|---|---|---|
| M1: archived listings not used | fixed | `logs/listing_check_author_files.log`. Own downloads of the 4 bracketing captures (methanol50 and nuclear14, 2020-01 and 2022-05) are byte-identical to the author's files. Own CDX queries (`dl/cdx_page_*.txt`) confirm the selection: there is no topopt capture between 2020-01-11 and 2022-05-22, and rocket100's earliest capture is 2018-09-23. |
| m1: ghg_3veh constants | fixed | `code/ghg_old_cur.py`, `code/ghg_patch_check.py`. Only e32, e39, e46 and e113 differ. Replacing the 3 written constants by their exact products makes all 120 rows equal. Relative differences are 1.841e-15, 8.669e-16 and 2.944e-16, with 3, 2 and 1 occurrences. |
| m2: methanol50 | fixed; the author's correction to round 1 is right | `logs/cmp_forms_methanol50.log`. 0 of 1,497 rows differ. 360 objective coefficients differ, by degree {0: 1, 1: 104, 2: 255}, by at most 1e-15 absolute and 2.383e-16 relative. The exact shift at p4 is +4.83486e-16. |
| m3: catmix | fixed | `logs/cmp_forms_catmix{100,200,400,800}.log`. Half of the rows differ, 2 coefficients each: 9/200, 9/400, 9/800 and 9/1600 are written as 0.045000000000000005, 0.022500000000000003, 0.011250000000000001 and 0.005625000000000001. Relative errors are 1.11e-16, 1.33e-16, 0.89e-16 and 1.78e-16. The objectives are identical. |
| m4: lop97icx | fixed; the author's digit correction is right | `logs/cmp_forms_lop97icx.log`. 0 of 87 rows differ. 30 objective coefficients differ (18 linear, 12 quadratic), by at most 2e-14 absolute and 1.36e-16 relative. At p2 the .gms objective is 2561912471/625000 = 4099.0599536 and the OSIL objective is 4099.059953600000099; the difference is 9.9e-14. |
| m5: MINLPLib.jl first commit | fixed, but the new wording is inaccurate | see issue 2 |
| m6: Internet Archive statement | fixed | earliest captures in `dl/cdx_domain_to2018.txt`. See the note under issue 4. |
| m7: independence of re-proofs | fixed | The report now separates checks made with the audit's `verify.py`, checks from the round-1 review, and its own exact comparisons. |
| m8: preamble | fixed | The preamble is removed. |

## Issues

1. **minor: OSIL file dates miscounted.**
   - **Location:** Part A, "File dates", first bullet: "OSIL Last-Modified is 2019-06-25 for all but 7 files: pricing050 (2024-03-25), the six KAN instances (2025-05-07) and ann_cumene_tanh (2021-11-29)."
   - **Evidence:** the list names 8 files. The author's own `data/part_a.json` gives 2019-06-25 for 61 of the 69 OSIL files, and the 8 listed files carry other dates (`logs/spotchecks.log`). The GMS bullet below it correctly says "61 of the 69".
   - **Fix:** say "all but 8" or "61 of the 69 files".

2. **minor: the contents of MINLPLib.jl's first commit are misdescribed.**
   - **Location:** Part B, Sources, MINLPLib.jl bullet: "The repository's first commit is d2ba96c (2017-11-21). It holds only GLOBALLib and MINLPLib 1 copies".
   - **Evidence:** `git ls-tree d2ba96c instances/` lists 15 collections: PODLib, bcp, global, ibm, inf, minlp, morg, mpec, mult3, mult4, poly, prince, qcqp, qcqp2 and qcqp3 (`logs/jl_first_commit.log`). `prince` is a PrincetonLib copy. The conclusion that the commit adds no earlier copies of today's MINLPLib 2 models is not affected.
   - **Fix:** "It holds older collections (15 directories, including GLOBALLib as `global`, MINLPLib 1 as `minlp` and PrincetonLib as `prince`) but no MINLPLib 2 copies."

3. **minor: the hvycrash bound difference is overstated.**
   - **Location:** Part B, "Other 47 instances", PrincetonLib table, row hvycrash: "other bounds on 167 variables".
   - **Evidence:** the count of 167 matches variables by name, but the variables are numbered differently in the two files. Compared as multisets (`code/hvy_bounds.py`, `logs/hvy_bounds.log`), the files have 203 and 202 variables. The PrincetonLib file has:
     - 51 variables in [0.005, 6.2881854], where today's file has 51 in [0, 6.2831854];
     - one extra variable fixed at 0.005.

     Both bounds of each such variable are shifted by exactly 0.005. That looks like a translation of variables, possibly with the constraints adjusted to match. So the report has not shown that the PrincetonLib file is a different model rather than a reformulation. This does not affect any audited bound, because hvycrash's 2017 copy matches today's file.
   - **Fix:** state the multiset difference: 203 against 202 variables, and 51 variable boxes shifted by 0.005. Say "different formulation (not checked for equivalence)" instead of implying a different model, or check equivalence.

4. **minor: two statements about listing equality and the earliest model file are worded too strongly.**
   - **Location 1:** "What is proved and what is not": "Listing identities (exact text equality of the HTML-unescaped archived listing with today's .gms)". Method step 2 says "identical" for "equal text".
   - **Evidence 1:** `archived_listings.py` (line 102) compares `body.strip("\n")` with `gms.strip("\n")`. Each complete listing has one more trailing newline than today's .gms, because the page puts a newline before `</PRE>` (`identical_mod_trailing_ws` in `logs/listing_check_author_files.log`). The texts are otherwise exactly equal, so this does not change the model.
   - **Fix 1:** add "apart from leading or trailing newlines" so that the paper does not claim byte identity.
   - **Location 2:** Part B, Sources: "the first is `gms/faclay75.gms`". Revision item 7 makes the same claim.
   - **Evidence 2:** the stored CDX list has `lp/faclay75.lp` at 2018-05-29 05:59:21 and `pip/faclay75.pip` at 05:59:47, both before `gms/faclay75.gms` at 06:01:21. The instance page `faclay75.html`, which embeds the full .gms, was captured on 2018-05-26 (`logs/faclay75_cdx.log`). This concerns another instance and does not affect any verdict.
   - **Fix 2:** "from 2018-05-29 on (faclay75)".

Not an issue, but worth noting: `data/tables.md` is stale. Its Table B1 says "none found" for topopt and nd_netgen. The report says this openly and states that its own Table B1 supersedes that column. Whoever writes the paper must take the table from report.md, not from `data/tables.md`. Regenerating the file or deleting the stale column would remove the risk.

## Other checks that found nothing wrong

- **Archived listings** (previous verifier's own code, `code/listing_check.py`):
  - 29 complete captures equal today's .gms.
  - topopt 2022-05-22 is cut at 1,048,576 bytes. All of its cut text is a prefix of today's file: 23,479 complete lines and 1,039,259 characters, plus a partial line of 3 characters. The author's count is right.
- **Bounds then and now** (`code/bounds_then_now.py`, `logs/bounds_then_now.log`):
  - Every flagged bound on the archived pages has the same value and date as today.
  - The four 2022 bounds are missing from the 2020-01 pages and present on the 2022-05 pages. For example, topopt LINDO is "inf" (2018-08-19) in 2018-09 and 2020-01, and 35.35267044 (2022-02-15) in 2022-05.
- **Exact .gms-to-OSIL comparison** (own parser `code/exactcmp.py`, not derived from `exact_forms.py`):
  - Beyond the six instances above, all rows and objectives are identical for glider100, ghg_3veh, eniplac, nuclear14, spring, rocket100/200/400, the four sssd instances, nd_netgen, topopt and watercontamination0303.
  - stockcycle (a `1/x13` objective term) and smallinvDAX (an assertion in my reader) were not covered by this exact check. The round-1 60-digit batch covers them.
  - This supports the report's statement that only the five families differ.
- **methanol50 objective shift** (`code/shift_bound.py`, own; `logs/shift_bound.log`):
  - The bound is Σ|δ_m|·max over p4 ± 1 of |m|, which gives 3.2352e-15. For lop97icx on p2 ± 1 it gives 4.76e-13. Both agree with the report.
  - The audit record `bound-audit/logs/verify/methanol50.p4.json` shows status proved, route B, max_move 7.39e-13 and Krawczyk rho 1e-12. The proved point therefore lies in the box.
  - The shift is about 9 orders of magnitude below the 9.8e-5 margin.
- **GAMS 54.3 rendering of methanol50** (`code/gams543_osil_obj.py`): its OSiL objective expands to exactly the .gms objective. This holds for both the author's file and the round-1 conversion.
- **Side-table examples:** methanol50's constant 5.01625659 → 5.016256589999999 and lop97icx's i257·i95 coefficient 11.2897376 → 11.289737599999999 are both among the differing coefficients (`logs/spotchecks.log`).
- **Archived statistics:** `instancedata` snapshots of 2020-02-19 and 2024-03-15 show no differences for the 22 Part B instances (`logs/stats_cmp.log`).
- **Review copies:** all 34 page heads are identical (`logs/review_copies.log`).

## Commands run

The previous round-2 verifier ran these commands. I sanity-checked their logs and reused them. All ran in `publication/reviews/minlplib-status-r2/`, using at most 2 cores.

1. `python3 code/listing_check.py` → `logs/listing_check_author_files.log`.
2. `curl` (CDX and `id_` downloads, at least 1 s delay) → `dl/cdx_page_*.txt`, `dl/page.*.html`, `dl/cdx_domain_to2018.txt`, `dl/instancedata.*.csv`.
3. `python3 code/bounds_then_now.py` → `logs/bounds_then_now.log`.
4. `python3 code/ghg_old_cur.py` → `logs/ghg_old_cur.log`; `python3 code/ghg_patch_check.py` → `logs/ghg_patch_check.log`.
5. `code/run_forms.sh`, `code/run_forms2.sh` and `code/run_forms3.sh` (sequential `timeout … python3 code/cmp_forms.py NAME [sol]`) → `logs/cmp_forms_*.log` and `.json`. All three finished: `run_forms2.out` and `run_forms3.out` end with "DONE".
6. `python3 code/shift_bound.py` → `logs/shift_bound.log`; `python3 code/gams543_osil_obj.py` → `logs/gams543_osil_obj.log`; `python3 code/stats_cmp.py` → `logs/stats_cmp.log`; `python3 code/review_copies.py` → `logs/review_copies.log`.

I ran these myself on 2026-10-03, in the foreground, one process at a time:

7. `cat PROGRESS.json logs/run_forms2.out logs/run_forms3.out logs/cmp_forms_*.log logs/shift_bound.log …` and `grep` summaries of all `cmp_forms` logs. I also ran `ps aux | grep -E "run_forms|cmp_forms"`, which showed no running jobs.
8. `python3 code/spotchecks.py | tee logs/spotchecks.log`, which checks the side-table examples, the methanol50 audit verify record and the Last-Modified counts from `data/part_a.json`.
9. `timeout 120 python3 code/hvy_bounds.py > logs/hvy_bounds.log`.
10. `git log --reverse` and `git ls-tree --name-only d2ba96c instances/` in `publication/minlplib-status/pages/sources/MINLPLib.jl` → `logs/jl_first_commit.log`.
11. `grep` of `dl/cdx_domain_to2018.txt` for faclay75 and for model-file directories → `logs/faclay75_cdx.log`.
12. `grep -n` on `publication/minlplib-status/archived_listings.py` (comparison rule) and on report.md.

All checks are targeted. No project-wide verification was run, and CI was not consulted. Nothing was committed and nobody was contacted. The track's report was not edited.
