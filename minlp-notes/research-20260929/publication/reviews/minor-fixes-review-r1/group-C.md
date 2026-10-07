# Verifier group C: primal/water-ann-kan and audit-ir

Date: 2026-10-03. P = research-20260929/publication. Scratch scripts and logs: `scratch-C/`.
Only files in this directory were written. All runs were single processes, each under about 1 minute.
No track, author or audit files were edited, and `audit.py` was not rerun.

## Summary

| track | issue | verdict |
|---|---|---|
| water-ann-kan | 1 missing/truncated report | OK, with one stale sentence (minor, C1) |
| water-ann-kan | 2 gap rounding / relative change | **problem (major)**: the new "conservative upper bounds" sentence is false for 6.89% |
| water-ann-kan | 3 old bound violations | OK (all four values reproduced) |
| water-ann-kan | 4 x650 zero margin | OK |
| water-ann-kan | 5 interval-format description | OK for the JSONs; stale code comment in nn_exact.py (minor) |
| audit-ir | 1 missing/truncated report | OK |
| audit-ir | 2 digit-count definition | OK (35/38/46 reproduced); the integration bullet should also mention the slack floor (minor) |
| audit-ir | 3 spring wording | OK |
| audit-ir | 4 SCIP 1.0e-9 | OK |

## primal/water-ann-kan

### Issue 1: Missing and truncated report. Verdict: OK, with one stale sentence (minor)

- The full report (Sections 1–8, assumptions, commands) is on disk. "Open issues" now acknowledges review r1. The old "report.md was not written" and "No independent review" bullets were removed.
- **Problem (minor), C1.** `P/primal/water-ann-kan/report.md:5` still says "so none of this has been independently reviewed". This contradicts the new Open-issues bullet (line 174) and response row 1.
  - Suggested fix: "... by the same author; independent review r1 later verified the numerical claims with its own code."

### Issue 2: Conservative and repeated gap rounding. Verdict: **problem (major)**

- **Relative primal change.** Own script `scratch-C/water_check.py` reads the source decimal strings in `open-instances-wave2/waterno2/logs/primal_TT_w2.json`, the cached OSIL objective coefficients and the stored exact objective rationals.
  - The OSIL objective evaluated exactly at the source decimals equals the stored `obj` float.
  - Increases: 4.8872e-6, 1.0326e-5, 2.5318e-5, 2.5696e-5.
  - Relative changes: 5.34692e-9 (09), 4.62272e-9 (12), 5.03941e-9 (18), 3.68995e-9 (24). The range is 3.69e-9 to 5.35e-9, so "3.7e-9 to 5.3e-9 (exact ratios 3.6899e-9 to 5.3469e-9)" is correct. The ratios are the same to 6 digits whether divided by the old or the new objective.
- **Gap ratios.** Own script `scratch-C/gap_check.py` uses the exact objectives and the r1 reviewer's dual values.
  - gap/dual: 1.6739582e-2, 1.0811534e-1, **6.8939570e-2**, 4.8668497e-2, 5.8946908e-2.
  - gap/primal: 1.6463982e-2, 9.7566865e-2, 6.4493421e-2, 4.6409802e-2, 5.5665594e-2.
  - Every table entry (columns gap/abs(dual) and gap/abs(primal)) is at least the exact value, so the table is upward-rounded throughout. The 1.647e-2 and 6.450e-2 double-rounding examples are correct.
- **Problem (major), C2.** `P/primal/water-ann-kan/report.md:28` says "The displayed relative gaps to the dual are conservative upper bounds 10.82%, 6.89%, 4.87% and 5.90%. Rounding is upward ...". For waterno2_12 the exact ratio is 6.89396%, so **6.89% is below the exact value and is not an upper bound**. That value is rounded to nearest, not upward. The other three are upward. The same false claim is in the integration cell `P/reviews/minor-fixes/summary.md:45` ("treat displayed gaps as conservative upper bounds"), so it would enter the paper.
  - The error is small (0.004 percentage points), but it is a wrong rigour claim, which is why I rate it major rather than minor.
  - `code/minor_review_check.py` prints "PASS: ... conservative gap rounding ... checked" without asserting anything about the gaps, so it did not catch this.
  - Suggested fix (either one):
    - (a) use 10.82%, 6.90%, 4.87%, 5.90% (all upward);
    - (b) give the nearest values 10.81%, 6.89%, 4.87%, 5.89%, and drop "upper bounds" from the text sentence; the table's four-digit values remain upward.
  - Update summary.md:45 to match. The 6.89% also appears in older wave-2 documents (`open-instances-wave2/waterno2/report.md:34`, `logs/summary_tables.md:5`, `reviews/waterno2-verification/verification-report.md:412`) as a plain 2-decimal value. That use is fine if it is not described as an upper bound.

### Issue 3: Old bound violations omitted. Verdict: OK

Checked with `scratch-C/water_check.py`:
- Exact Fraction comparison of the source decimal strings with the OSIL `lb`/`ub` (defaults 0/+inf; no `mult` attributes).
- Alignment check: each source coordinate is within 8.7e-7 / 1.6e-6 / 2.8e-6 / 2.4e-6 of the exact point's value for the same OSIL name. This confirms that index order equals OSIL order.

Maximum violations:

| instance | max violation | variable and bound | number of violated bounds |
|---|---|---|---|
| waterno2_09 | 5.72648e-11 | x1443, lb .512 | 16 |
| waterno2_12 | 3.090417263e-10 | x1739, lb 0 | 20 |
| waterno2_18 | 8.938913e-10 | x2915, lb .512 | 36 |
| waterno2_24 | 9.0018923e-10 | x3633, ub .343 | 65 |

These match report line 32 and summary.md:46. The report shows 3.09042e-10, which is a rounding of 3.090417263e-10; the other three are exact decimals.

### Issue 4: Zero interval margin at x650. Verdict: OK

- OSIL row e580 is `x650 − tanh(x670) = 0`. The point JSON gives x670 ≈ 101.816. In the OSIL, x650 has bounds [−1, 1].
- 1 − tanh(101.8) ≈ 2e^{−203.6} ≈ 1e-88, which is below the 60-digit and 45-digit resolution. So the outward enclosure of x650 is [1 − 1e-45, 1] (JSON `hi` = exactly 1), and its margin to ub = 1 is 0.
- The log line `smallest proved margin of an interval value 0.000e+00 (x650 ub)` matches.
- The text's reasoning (nonnegative margin suffices for a non-strict bound) is correct.
- Not a problem: x657 = tanh(x677), x677 ≈ −125.75, has the same zero margin at lb −1, as the r1 reviewer saw. The text explains the logged case only, which is enough.

### Issue 5: Interval-format description. Verdict: OK for the JSONs; stale code comment (minor)

Checked with `scratch-C/json_check.py` against `git show HEAD:`:
- In all 7 point JSONs, the HEAD bytes with the single occurrence of "(mid, rad)" replaced by "{lo, hi}" equal the current file bytes exactly.
- Parsed-JSON comparison: the only differing leaf is `/construction`.
- Every interval entry has keys exactly {lo, hi, defined_by}, with lo ≤ hi. Widths are ≤ 1e-41, and no `hi` looks like a radius. No mid/rad keys appear anywhere. Interval/rational counts per file: 460/334, 238/891, 297/1113, 533/2001, 137/701, 227/1165, 362/1861.
- `nn_exact.py`: apart from the path-only `_REPRO_ROOT` edits, the only change is the description string (checked with `git diff`).
- **Problem (minor), C3.** `P/primal/water-ann-kan/code/nn_exact.py:143` (line 140 at HEAD) still has the comment `# point file: inputs exactly, every variable as interval centre and radius`, but the code below it writes `dict(lo=..., hi=..., defined_by=...)`. The same wrong description survives in the script whose description the fix claims to correct.
  - Suggested fix: "... every other variable as a rational or an outward interval {lo, hi}". Comment only; no rerun needed.

## audit-ir

### Issue 1: Missing and truncated report. Verdict: OK

- The full report with Sections 1–6, Commands and Open issues is on disk.
- The header changed from "partial" to "complete", and the obsolete "integration step must write report.md" bullet was removed. Both changes are justified.

### Issue 2: Digit count definition. Verdict: OK (the integration bullet should also mention the slack floor)

**Recount.** `scratch-C/digits_check.py` re-parses the 1633 saved instance pages in `bound-audit/pages/*.html` (excluding instances.html) with `html.parser`. It does not use pages.json or parse_pages.py. It takes the first token of every `<div title="Added on …">` (points) and `<div title="Last updated: …">` (duals).
- 13,847 numeric values, plus 55 "inf"; none is in exponent form. This matches the report's 13,847.
- At most 8 decimals are shown, confirming the 8-decimal limit.
- No value with a decimal part ends in 0. 3079 values end in "." and none lacks a point.

| definition | count | digit range | distinct strings | pages | points / duals |
|---|---|---|---|---|---|
| A: nonempty fractional part, digits counted from first to last nonzero digit | 35 | 11–17 | 18 | 9 | 10 / 25 |
| B: as A without the fractional-part filter | 38 | 11–19 | 19 | 12 | 10 / 28 |
| C: digits counted from first nonzero to last shown digit (trailing integer zeros count) | 46 | 11–20 | 27 | 20 | 10 / 36 |

- B − A: −99999999809999994880. (gasoil50, gasoil100, shiporig duals).
- C − B: 8 integer-valued duals: 1786850000000. (case_1scv2), −10000000000. (ex8_3_7), −335782251000. (glider200), −86500029070. (glider50), −18222634170. (rocket400), 11249462900. and 45396981180. (transswitch2383wpp/wpr), −165372160000. (uselinear).
- The report text (`P/audit-ir/report.md:60–61`) and summary.md:50 are correct.

**Ambiguities to state when integrating:**
- (1) The counts are of displayed entries, not distinct numbers. For example, fac1 alone contributes 9 entries of one string, and the 35 entries are 18 distinct strings.
- (2) Definition C counts zeros of integer-valued displays such as "−10000000000." as significant. That is what the audit's slack rule implicitly does, but it is not "significant digits" in the usual sense.

**Flagged pairs and ties.** `scratch-C/digits_in_pairs.py`: under all three definitions, 0 of the 158 screened pairs involve such a value, so none of the flagged pairs do either. 17 display-tie pairs involve one, all on fac1, fac2 and waternd_fosspoly0.
- Minor wording, not a new defect: `audit-ir/report.md:62` "three are in display ties" means three *instances* (17 tie pairs), not three values. Optional rewording: "values on three instances (fac1, fac2, waternd_fosspoly0) occur in 17 display ties".

**Audit Section 2 (current text).** `bound-audit/audit-report.md:271–279` still says "Values are shown with at most 10 significant digits and at most 8 decimals". It also defines the slack as "half a unit in its last shown digit, but never less than half a unit in the 10th significant digit". `audit.py:shown_slack` implements this; its docstring says "at most 10 significant digits are meaningful". No other passage of audit-report.md relies on the 10-digit display limit; lines 486 and 991 concern 13-digit enclosure rounding.
- The integration bullet (summary.md:15 and the audit-ir cell at summary.md:50) is correct as far as it goes: keep 8 decimals, drop the 10-digit limit, define the count. It has not yet been applied, as summary.md states.

**Lead's extra check: the 10th-significant-digit slack floor.**
- The floor `max(unit_shown, 10^(floor(log10|v|)−9))` binds exactly for values with more than 10 digits from the first nonzero digit to the last shown digit. That is definition C, so the 46 count is the one relevant to the slack.
- `scratch-C/slack_floor_check.py` re-derives each class from `results.json` (obj_lo/obj_hi, d_listed, sense) in exact Fractions, with and without the floor:
  - With the floor it reproduces every stored class: 22 (i), 17 (i-r), 63 (ii), 26 (ii proven), 30 (iii); 0 mismatches.
  - The floor changes the slack for **0 of 158** result rows and 0 of 158 screened pairs. It binds only in 17 display ties (fac1 8, fac2 8, waternd_fosspoly0 1), which are never classified.
  - Without the floor, the classes are identical. So "No audit class or flagged-pair count changes" is confirmed.
- Does the floor still make sense? Once the 10-digit display limit is dropped, its stated rationale is gone. Pages do show up to 17–20 digits, for example the binary64 print artifact 160912612.40000001. The floor can only enlarge the slack, so it can only move a pair from (i) to (i-r), never the reverse. It therefore remains a defensible *conservative convention* (treat digits beyond the 10th as not meaningful), but it should be stated as such rather than derived from a display limit.
- **Recommendation (minor), C4.** Add to the summary.md:15 bullet and the audit-ir issue-2 cell (summary.md:50): "The slack floor (never less than half a unit in the 10th significant digit) no longer follows from a display limit; keep it as an explicit conservative convention, or drop it. It binds for no screened pair (0/158; only 17 ties on fac1/fac2/waternd_fosspoly0), so classes are identical either way."

**Other check.** `audit-ir/report.md:163`, the 17 Sep 2013 dual digit histogram: my recount (`scratch-C/hist_check.py`) gives 65, 77, 36, 24, 59, 2, 17, 30, 86, 5 for 2–10 and >10 digits, as reported. The first bin is 79 if the 31 zero values are counted, against the report's 48, so the report evidently excludes zeros. The ">10 = 5" count is the same under every definition. The text is unchanged and needs no fix.

### Issue 3: spring wording. Verdict: OK

- `audit-ir/report.md:34` now reads "They need not be solver errors: display rounding explains these listed values. The listing alone cannot establish that the underlying stored solver bounds were at most the exact optimum." This matches the reviewer's suggestion and summary.md:51.
- No remaining "not solver errors" claim (grep). The heading at line 31, "spring is fully explained by rounding", is consistent with the qualified wording (it is about the listed values), so I leave it.

### Issue 4: SCIP objective tolerance. Verdict: OK

- `logs/xcheck_scip.log`: spring exact obj 0.846245665643154, SCIP obj 0.846245664643154. The difference is exactly 1.0e-9, which equals feastol.
- `xcheck_scip.py:evaluate` bisects for the smallest nlobjvar that SCIP accepts. Such a value lies about one feasibility tolerance below g(x), so the 1e-9 is the tolerance, not a disagreement.
- Report line 124 already says this, so "no change needed" holds, and summary.md:52 is correct.
- Nuance, no fix needed: the log's "rel. diff" is |Δ|/max(1, |f|). For spring (|f| < 1) it is the absolute difference; the true relative difference is 1.18e-9.

## Collateral (diff review)

**water-ann-kan** (`diff -u before/primal__water-ann-kan.txt report.md`; before == HEAD confirmed with `cmp`). Four hunks:
1. Lines 28 and 32: issue-2/3 text. The 6.89% error (C2) is in this hunk. Everything else in it checks out: the numbers match my scripts, and the log path exists.
2. Line 62: x650 explanation. Correct; the existing margins 9.98e-13 and 1.25e-12 are unchanged.
3. Open issues: two bullets replaced. Fine, but line 5 is now stale (C1).
4. Response table plus targeted-check command.
   - The relative review link `../../reviews/primal-water-ann-kan-review-r1.md` resolves.
   - The table rows equal summary.md and issues.json (checked programmatically for both tracks).
- No numbers were changed outside these hunks. The table values are unchanged, and the Section 7 Files entry already said {lo, hi}.
- Other code diffs in `code/` (gaps.py, check_nn_point.py, check_water_mp.py, test_osil_p4.py, test_qfield.py) are path-only and were ignored per the brief.

**audit-ir** (`diff -u before/audit-ir.txt report.md`; before == HEAD). Five hunks:
1. Header status: partial → complete. Justified.
2. Line 5: intro rewritten. Fine.
3. Line 34: spring wording (issue 3). OK.
4. Lines 60–62: digit counts (issue 2). OK; see the "three" wording note above.
5. Open issues and response table.
   - Obsolete bullet removed; the Section 2 bullet now defines 35/38/46.
   - The link `../reviews/audit-ir-review-r1.md` resolves.
   - The log `logs/minor_review_check.log` exists and shows 35 (11–17), 38 (11–19) and 46 (11–20).
- No other numbers changed.
- Line 13: the "Display unit = coarser of 10th significant digit and 8th decimal" definition is still valid. It describes the coarsest rounding the display could apply, not a maximum number of shown digits, so it does not depend on the dropped limit.

**summary.md:** For these tracks, the integration bullet list (line 15) covers audit-ir only. No water-ann-kan bullet is needed, because the changed water figures (relative change, bound violations) are not quoted outside the track (grep found no "4e-9 to 5e-9" elsewhere). Fixes needed: C2 at line 45; C4 at lines 15 and 50.

## Commands

All commands were run from the stated directory, one process at a time. SC = `P/reviews/minor-fixes-review-r1/scratch-C`.
1. `cat BRIEF.md && ls -la` (in P/reviews/minor-fixes-review-r1)
2. `cat reviews/minor-fixes-review-r1/PROGRESS.json; ls reviews/minor-fixes; ls reviews | head -80; grep -n -i -E "water-ann-kan|audit-ir" reviews/minor-fixes/summary.md`
3. `cat reviews/primal-water-ann-kan-review-r1.md; ls reviews/primal-water-ann-kan-review-r1/` and `cat reviews/audit-ir-review-r1.md; ls reviews/audit-ir-review-r1/`. Both directories do not exist; the real ones are `*-r1/`.
4. `ls reviews/primal-water-ann-kan-r1 reviews/audit-ir-r1 primal/water-ann-kan primal/water-ann-kan/* audit-ir audit-ir/* | head -150; ls reviews/minor-fixes/before`
5. `ls -la reviews/primal-water-ann-kan-r1 ...; ls reviews/audit-ir-r1/live | head; git -C /workspace/minlp-notes status --short -- <the three dirs>`
6. `mkdir -p reviews/minor-fixes-review-r1/scratch-C && diff -u reviews/minor-fixes/before/primal__water-ann-kan.txt primal/water-ann-kan/report.md; git diff --stat HEAD -- primal/water-ann-kan/report.md; cmp reviews/minor-fixes/before/primal__water-ann-kan.txt <(git show HEAD:research-20260929/publication/primal/water-ann-kan/report.md)`
7. `cat -n report.md | sed -n 1,60p` (water-ann-kan)
8. `cat code/minor_review_check.py; cat logs/minor_review_check.log; git diff HEAD -- code/gaps.py code/nn_exact.py`
9. Inline `python3 -c` printing the keys and types of `open-instances-wave2/waterno2/logs/primal_09_w2.json`; `head -c 600`
10. Inline `python3 -c` printing the structure of `points/waterno2_09.exact.json`; `grep` on `~/.cache/minlplib/minlplib/osil/waterno2_09.osil` (twice; the first output was too large)
11. Inline `python3 -c` listing the OSIL variable attributes and objective structure for waterno2_09/12/18/24
12. `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 timeout 300 python3 water_check.py 2>&1 | tee water_check.log` (in SC)
13. `PYTHONDONTWRITEBYTECODE=1 python3 gap_check.py | tee gap_check.log` (in SC)
14. `PYTHONDONTWRITEBYTECODE=1 python3 json_check.py | tee json_check.log`, then an inline heredoc refinement appended with `tee -a json_check.log` (in SC). The first version's "bad" list was a false alarm from the extra `defined_by` key.
15. `grep -rn -i "mid, rad\|mid/rad\|(mid\|midpoint\|radius" code/*.py report.md`; `grep -n "x650\|x657\|margin" logs/nn_exact_ann_cumene_tanh.log`; `grep` on the r1 reviewer's rev_nn log
16. `sed -n 100,175p code/nn_exact.py; git show HEAD:.../nn_exact.py | grep -n "centre and radius"`
17. Inline python: x650/x670/x657/x677/x647 intervals from `ann_cumene_tanh.point.json` and OSIL bounds; inline python printing OSIL row e580
18. `sed -n 60,172p report.md` (water-ann-kan)
19. `grep -rn --include=*.md "6\.89%" .` (research-20260929)
20. `cmp reviews/minor-fixes/before/audit-ir.txt <(git show HEAD:...audit-ir/report.md); diff -u reviews/minor-fixes/before/audit-ir.txt audit-ir/report.md; cat audit-ir/minor_review_check.py; cat audit-ir/logs/minor_review_check.log`
21. `ls bound-audit ...; ls ~/.cache/minlplib/...`; `ls pages | wc -l; du -sh pages`; inline python printing the pages.json structure; `sed -n 1,80p parse_pages.py`
22. `grep -o '<div title=...' fac1.html`; inline python printing raw HTML around fac1's bounds
23. `PYTHONDONTWRITEBYTECODE=1 timeout 300 python3 digits_check.py | tee digits_check.log` (in SC)
24. `grep -n "^#" audit-report.md; sed -n 255,300p audit-report.md`; `grep -n "10th\|10 significant\|significant digit" audit-report.md; grep -n "def \|slack\|display_unit" audit.py`; `sed -n 25,120p audit.py; sed -n 170,310p audit.py`
25. `PYTHONDONTWRITEBYTECODE=1 python3 slack_floor_check.py | tee slack_floor_check.log` (in SC)
26. `PYTHONDONTWRITEBYTECODE=1 python3 digits_in_pairs.py | tee digits_in_pairs.log` (in SC)
27. `grep -n -i "solver error\|...\|11 to 20" audit-ir/report.md`
28. `cat logs/xcheck_scip.log; grep -n ... xcheck_scip.py; sed -n 115,130p report.md`; `sed -n 1,20p xcheck_scip.py; sed -n 56,100p xcheck_scip.py`
29. `sed -n 5,70p report.md; sed -n 150,195p report.md` (audit-ir)
30. `PYTHONDONTWRITEBYTECODE=1 python3 hist_check.py | tee hist_check.log` (in SC)
31. Inline python on issues.json (first attempt printed nothing: dict layout); `grep -n` on commands.md; `sed -n 1,43p summary.md`; `head -c 400 issues.json; grep -n ... issues.json`; inline python checking that the issues.json rows equal the summary.md rows (9/9 True)
32. `grep -rn --include=*.md -e "4e-9 to 5e-9" ...` (research-20260929)
33. `git diff HEAD -- research-20260929/publication/primal/water-ann-kan/code/ | grep '^[-+]' | ... | grep -v "_REPRO_ROOT\|_repro_os"`
34. `grep -n "Audit Section 2: retain" summary.md; grep -n "three are in display ties" audit-ir/report.md; grep -n "spring is fully explained" audit-ir/report.md`

No CI or project-wide checks were run, and no solver, construction or `audit.py` run was made.
